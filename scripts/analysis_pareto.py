#!/usr/bin/env python3
"""
Analysis 1: Churn Reason Pareto (Weighted)
Reads final_quotes.json, filters churn categories, applies weighted scoring,
outputs Pareto table + ASCII chart + top quotes.
"""

import json
import math
import os

BASE = os.path.dirname(os.path.abspath(__file__))
QUOTES_FILE = os.path.join(BASE, "clean_quotes", "final_quotes.json")
OUTPUT_FILE = os.path.join(BASE, "analysis", "01_churn_pareto.md")

CHURN_CATEGORIES = [
    "churn_cant_handle",
    "churn_billing",
    "churn_switched",
    "churn_general",
    "churn_voice_quality",
]

CATEGORY_LABELS = {
    "churn_cant_handle": "Can't Handle Calls",
    "churn_billing": "Billing & Pricing",
    "churn_switched": "Switched Away",
    "churn_general": "General Dissatisfaction",
    "churn_voice_quality": "Voice Quality / AI UX",
}


def load_quotes():
    with open(QUOTES_FILE, "r") as f:
        return json.load(f)


def compute_weight(quote):
    quality = quote["llm"].get("quote_quality", 1)
    if quote["source"] == "reddit":
        score = quote.get("score") or 1
        engagement = max(1.0, math.log2(max(score, 1)))
    else:
        engagement = 1.0
    return quality * engagement


def build_pareto(quotes):
    churn_quotes = [q for q in quotes if q["llm"].get("category") in CHURN_CATEGORIES]

    buckets = {}
    for cat in CHURN_CATEGORIES:
        cat_quotes = [q for q in churn_quotes if q["llm"]["category"] == cat]
        weighted_sum = sum(compute_weight(q) for q in cat_quotes)
        pres_ready = [q for q in cat_quotes if q["llm"].get("presentation_ready")]
        top_quotes = sorted(
            [q for q in cat_quotes if q["llm"].get("quote_quality", 0) >= 4],
            key=lambda q: compute_weight(q),
            reverse=True,
        )[:3]

        buckets[cat] = {
            "label": CATEGORY_LABELS[cat],
            "count": len(cat_quotes),
            "weighted_score": round(weighted_sum, 1),
            "pres_ready": len(pres_ready),
            "top_quotes": top_quotes,
        }

    total_weighted = sum(b["weighted_score"] for b in buckets.values())
    total_count = sum(b["count"] for b in buckets.values())

    sorted_cats = sorted(buckets.keys(), key=lambda c: buckets[c]["weighted_score"], reverse=True)

    cumulative = 0
    rows = []
    for cat in sorted_cats:
        b = buckets[cat]
        pct = (b["weighted_score"] / total_weighted * 100) if total_weighted else 0
        cumulative += pct
        rows.append({
            "cat": cat,
            "label": b["label"],
            "count": b["count"],
            "weighted": b["weighted_score"],
            "pct": round(pct, 1),
            "cumulative": round(cumulative, 1),
            "pres_ready": b["pres_ready"],
            "top_quotes": b["top_quotes"],
        })

    return rows, total_count, total_weighted


def format_bar(pct, max_width=30):
    filled = int(pct / 100 * max_width)
    return "\u2588" * filled + "\u2591" * (max_width - filled)


def truncate_text(text, max_len=300):
    text = text.replace("\n", " ").strip()
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text


def generate_markdown(rows, total_count, total_weighted):
    lines = []
    lines.append("# Analysis 1: Churn Reason Pareto (Weighted)")
    lines.append("")
    lines.append("> **CPO Question:** \"Of all the reasons users churn from receptionist products, which ones matter most?\"")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append("- **Data:** 378 classified quotes filtered to 5 churn categories")
    lines.append(f"- **Churn quotes analyzed:** {total_count}")
    lines.append("- **Weighting formula:** `quote_quality (1-5) x engagement_multiplier`")
    lines.append("  - Reddit: engagement = `max(1, log2(upvotes))` — community validation amplifies signal")
    lines.append("  - Trustpilot: engagement = 1.0 — all reviews are deliberate submissions")
    lines.append("- **Why weight?** Raw count alone is misleading. A devastating 5-quality quote with 20 upvotes carries more signal than five vague 2-quality mentions.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Pareto Distribution")
    lines.append("")
    lines.append("| Rank | Churn Reason | Raw Count | Weighted Score | % of Total | Cumulative % |")
    lines.append("|:---:|---|:---:|:---:|:---:|:---:|")

    for i, r in enumerate(rows, 1):
        lines.append(f"| {i} | **{r['label']}** | {r['count']} | {r['weighted']:.1f} | {r['pct']}% | {r['cumulative']}% |")

    lines.append(f"| | **Total** | **{total_count}** | **{total_weighted:.1f}** | **100%** | |")
    lines.append("")

    # ASCII bar chart
    lines.append("### Visual Distribution")
    lines.append("")
    lines.append("```")
    max_label = max(len(r["label"]) for r in rows)
    for r in rows:
        bar = format_bar(r["pct"])
        lines.append(f"  {r['label']:<{max_label}}  {bar}  {r['pct']}%")
    lines.append("```")
    lines.append("")

    # Key insight
    if len(rows) >= 2:
        top2_pct = rows[0]["cumulative"] if len(rows) == 1 else rows[1]["cumulative"]
        lines.append("---")
        lines.append("")
        lines.append("## Key Insight")
        lines.append("")
        lines.append(f"> **{top2_pct}% of all churn pain is concentrated in just 2 categories:** {rows[0]['label']} and {rows[1]['label']}.")
        lines.append(">")
        lines.append(f"> The #1 churn driver — **{rows[0]['label']}** — accounts for {rows[0]['pct']}% of weighted churn signal alone.")
        lines.append(">")
        lines.append("> This is the problem Central AI is built to solve.")
        lines.append("")

    # Top quotes per category
    lines.append("---")
    lines.append("")
    lines.append("## Representative Quotes by Churn Reason")
    lines.append("")

    for r in rows:
        if not r["top_quotes"]:
            continue
        lines.append(f"### {r['label']} ({r['count']} quotes, {r['pres_ready']} presentation-ready)")
        lines.append("")

        for j, q in enumerate(r["top_quotes"], 1):
            product = q["llm"].get("product_mentioned") or "unnamed service"
            pain = q["llm"].get("pain_point", "")
            quality = q["llm"].get("quote_quality", "?")
            source_label = q.get("subreddit", "Trustpilot")
            lines.append(f"**Quote {j}** (Quality {quality}/5 | {source_label} | Product: {product})")
            lines.append("")
            lines.append(f"*{pain}*")
            lines.append("")
            lines.append(f"> {truncate_text(q['text'])}")
            lines.append("")
            if q.get("url"):
                lines.append(f"[Source]({q['url']})")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    quotes = load_quotes()
    rows, total_count, total_weighted = build_pareto(quotes)
    md = generate_markdown(rows, total_count, total_weighted)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write(md)

    print(f"Pareto analysis written to {OUTPUT_FILE}")
    print(f"  Total churn quotes: {total_count}")
    print(f"  Total weighted score: {total_weighted:.1f}")
    for r in rows:
        print(f"  {r['label']}: {r['count']} quotes, {r['weighted']:.1f} weighted ({r['pct']}%, cumulative {r['cumulative']}%)")


if __name__ == "__main__":
    main()
