#!/usr/bin/env python3
"""
Final Pareto Analysis — MBB-Ready Format
Validated k=11 taxonomy (κ=0.917, 92.7% agreement).
Structured: Headline → Gut-punch → Proof → Zoom-in → Action → Appendix
"""

import json
import math
import os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
QUOTES_FILE = os.path.join(BASE, "clean_quotes", "final_quotes.json")
CODER_A = os.path.join(BASE, "analysis", "coder_a_k9.json")
CODER_B = os.path.join(BASE, "analysis", "coder_b_k9.json")
OUTPUT_FILE = os.path.join(BASE, "analysis", "06_final_pareto.md")

CATEGORY_META = {
    "SCRIPT_ADHERENCE": {
        "label": "Agents Ignore Scripts & Instructions",
        "short": "Script Failures",
        "group": "CALL HANDLING",
        "differentiator": "AI always follows the script — no drift, no forgetting, no re-training",
        "gtm": "\"Never re-train your receptionist again\"",
    },
    "BILLING_PREDATORY": {
        "label": "Predatory Billing Practices",
        "short": "Predatory Billing",
        "group": "BILLING",
        "differentiator": "No per-minute games — transparent, predictable pricing",
        "gtm": "Comparison page: show total cost vs. per-minute surprise",
    },
    "INAUTHENTICITY": {
        "label": "Callers Detect It's Not Real Staff",
        "short": "Inauthenticity",
        "group": "CALL HANDLING",
        "differentiator": "AI trained on YOUR business — knows your services, hours, team names",
        "gtm": "Demo: have prospect call and try to stump the AI",
    },
    "GARBLED_INFO": {
        "label": "Wrong Names, Emails & Numbers Captured",
        "short": "Garbled Info",
        "group": "CALL HANDLING",
        "differentiator": "AI captures data perfectly — no misspellings, no missing fields",
        "gtm": "Show side-by-side: human-captured vs AI-captured message",
    },
    "SERIAL_SWITCHING": {
        "label": "Tried Many Services, None Worked",
        "short": "Serial Switching",
        "group": "INDUSTRY DISILLUSIONMENT",
        "differentiator": "Fundamentally different approach — AI, not shared human pool",
        "gtm": "Position as \"the last answering service you'll ever try\"",
    },
    "BILLING_TRAP": {
        "label": "Can't Cancel / Post-Cancellation Charges",
        "short": "Billing Trap",
        "group": "BILLING",
        "differentiator": "Cancel anytime, no tricks — month-to-month, one click",
        "gtm": "Homepage: \"No contracts. Cancel in one click.\"",
    },
    "BILLING_OPAQUE": {
        "label": "Confusing Bills & Surprise Overages",
        "short": "Opaque Billing",
        "group": "BILLING",
        "differentiator": "Simple pricing dashboard — see exactly what you're paying for",
        "gtm": "Pricing page: show real-time usage dashboard screenshot",
    },
    "QUALITY_DECAY": {
        "label": "Service Deteriorated Over Time",
        "short": "Quality Decay",
        "group": "SERVICE RELIABILITY",
        "differentiator": "AI doesn't burn out, quit, or get overworked — consistent forever",
        "gtm": "Retention messaging: \"Same quality, month 12 as month 1\"",
    },
    "MISSED_CALLS": {
        "label": "Calls Go Unanswered, Messages Delayed",
        "short": "Missed Calls",
        "group": "SERVICE RELIABILITY",
        "differentiator": "AI answers every call instantly — 0% miss rate, 24/7",
        "gtm": "Live counter: \"X calls answered today, 0 missed\"",
    },
    "ROUTING_ERRORS": {
        "label": "Calls Sent to Wrong Person / Department",
        "short": "Routing Errors",
        "group": "CALL HANDLING",
        "differentiator": "AI routes based on trained rules — no human memory failures",
        "gtm": "Setup wizard: \"Tell us your team, we'll route perfectly\"",
    },
    "BILLING_TOO_EXPENSIVE": {
        "label": "Just Too Expensive",
        "short": "Too Expensive",
        "group": "BILLING",
        "differentiator": "AI at a fraction of the cost — no per-minute markup",
        "gtm": "Calculator: \"See how much you'd save switching to Central AI\"",
    },
}

GROUP_ORDER = ["CALL HANDLING", "BILLING", "SERVICE RELIABILITY", "INDUSTRY DISILLUSIONMENT"]

GROUP_META = {
    "CALL HANDLING": {
        "insight": "The core product promise — handling calls well — is broken for half of all churners.",
        "implication": "Table stakes. AI receptionist must nail script adherence, sound authentic, and capture data accurately before anything else.",
    },
    "BILLING": {
        "insight": "Nearly a third of churn is billing, not service quality. Customers leave even when calls are handled fine.",
        "implication": "Transparent pricing is a competitive moat. No per-minute billing, no contracts, cancel anytime. Make billing a feature, not a liability.",
    },
    "SERVICE RELIABILITY": {
        "insight": "Services that start strong deteriorate over time. Human agents burn out, quit, or get stretched thin.",
        "implication": "AI's structural advantage: consistency doesn't degrade. Year 3 is identical to Day 1. This is the long-term retention story.",
    },
    "INDUSTRY DISILLUSIONMENT": {
        "insight": "10% of churners have tried multiple services and given up on the entire category.",
        "implication": "Highest-intent prospects: they NEED the service, they've just been burned. Position as fundamentally different technology, not another answering service.",
    },
}

# Top competitors for cross-tab (normalize Ruby variants)
TOP_COMPETITORS = ["AnswerConnect", "Ruby Receptionist", "PATLive", "Smith.ai"]


def load_quotes():
    with open(QUOTES_FILE) as f:
        all_q = json.load(f)
    return [q for q in all_q if q["llm"].get("category", "").startswith("churn_")]


def load_coder(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return {item["idx"]: item["category"] for item in data["classifications"]}


def adjudicate(codes_a, codes_b):
    """Adjudicate: agree → use it. Disagree → use Coder A (flag it)."""
    final = {}
    disagreements = []
    for idx in sorted(set(codes_a.keys()) | set(codes_b.keys())):
        a = codes_a.get(idx)
        b = codes_b.get(idx)
        if a == b:
            final[idx] = a
        else:
            final[idx] = a  # default to A
            disagreements.append((idx, a, b))
    return final, disagreements


def compute_weight(quote):
    quality = quote["llm"].get("quote_quality", 1)
    if quote["source"] == "reddit":
        score = quote.get("score") or 1
        engagement = max(1.0, math.log2(max(score, 1)))
    else:
        engagement = 1.0
    return quality * engagement


def truncate(text, max_len=250):
    text = text.replace("\n", " ").strip()
    return text[:max_len] + "..." if len(text) > max_len else text


def normalize_product(product):
    """Normalize product names for consistent grouping."""
    if not product or product == "unnamed":
        return "Other"
    if product == "Ruby":
        return "Ruby Receptionist"
    return product


def devastation_score(text):
    """Score how emotionally devastating a quote is for gut-punch selection."""
    t = text.lower()
    score = 0
    if any(w in t for w in ["thousand", "hundred", "$"]):
        score += 3
    if any(w in t for w in ["lost client", "lost customer", "lost revenue", "lost lead"]):
        score += 3
    if any(w in t for w in ["years", "year"]):
        score += 2
    if any(w in t for w in ["scam", "dishonest", "beware", "fraud", "worst",
                             "terrible", "horrible", "negligence", "incompetent"]):
        score += 2
    return score


def extract_pull_quote(text, max_len=200):
    """Extract the most devastating sentence from a quote for the gut-punch section."""
    import re
    text_clean = text.replace("\n", " ").strip()
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text_clean)
    if not sentences:
        return truncate(text_clean, max_len)

    # Score each sentence
    best = None
    best_score = -1
    for s in sentences:
        if len(s) < 20:
            continue
        score = devastation_score(s)
        # Bonus for reasonable length
        if 40 < len(s) < 180:
            score += 1
        if score > best_score:
            best_score = score
            best = s

    if best and len(best) <= max_len:
        return best
    elif best:
        return best[:max_len] + "..."
    return truncate(text_clean, max_len)


def main():
    quotes = load_quotes()
    codes_a = load_coder(CODER_A)
    codes_b = load_coder(CODER_B)
    final_codes, disagreements = adjudicate(codes_a, codes_b)

    print(f"Quotes: {len(quotes)}, Codes: {len(final_codes)}, Disagreements: {len(disagreements)}")

    # Build category stats
    cat_stats = {}
    for idx, cat in final_codes.items():
        if cat not in cat_stats:
            cat_stats[cat] = {"count": 0, "weighted": 0.0, "quotes": []}
        q = quotes[idx]
        w = compute_weight(q)
        cat_stats[cat]["count"] += 1
        cat_stats[cat]["weighted"] += w
        cat_stats[cat]["quotes"].append((idx, q, w))

    total_count = sum(s["count"] for s in cat_stats.values())
    total_weighted = sum(s["weighted"] for s in cat_stats.values())

    # Sort by weighted score
    sorted_cats = sorted(cat_stats.keys(), key=lambda c: cat_stats[c]["weighted"], reverse=True)

    # Build group stats
    group_stats = {}
    for cat, s in cat_stats.items():
        g = CATEGORY_META.get(cat, {}).get("group", "OTHER")
        if g not in group_stats:
            group_stats[g] = {"count": 0, "weighted": 0.0, "cats": []}
        group_stats[g]["count"] += s["count"]
        group_stats[g]["weighted"] += s["weighted"]
        group_stats[g]["cats"].append(cat)

    # Build competitor × category cross-tab
    comp_cats = {}
    for idx, cat in final_codes.items():
        q = quotes[idx]
        prod = normalize_product(q["llm"].get("product_mentioned"))
        if prod not in comp_cats:
            comp_cats[prod] = Counter()
        comp_cats[prod][cat] += 1

    # Build competitor × group cross-tab
    comp_groups = {}
    for prod, cats in comp_cats.items():
        comp_groups[prod] = Counter()
        for cat, count in cats.items():
            g = CATEGORY_META.get(cat, {}).get("group", "OTHER")
            comp_groups[prod][g] += count

    # Select gut-punch quotes: prioritize devastation of extractable sentence + quality
    # Not engagement — a devastating Trustpilot review is better than a mildly upvoted Reddit post
    all_quotes_scored = []
    for idx, cat in final_codes.items():
        q = quotes[idx]
        quality = q["llm"].get("quote_quality", 1)
        dev = devastation_score(q["text"])
        # Also score the best extractable sentence
        pull = extract_pull_quote(q["text"])
        pull_dev = devastation_score(pull)
        # Combined: sentence devastation matters most, then overall text, then quality
        combined = pull_dev * 10 + dev * 3 + quality * 2
        all_quotes_scored.append((combined, pull_dev, idx, q, cat))
    all_quotes_scored.sort(key=lambda x: x[0], reverse=True)

    # Pick top 4 gut-punch quotes, prefer diversity across competitors
    gut_punch = []
    used_products = set()
    for combined, pull_dev, idx, q, cat in all_quotes_scored:
        prod = normalize_product(q["llm"].get("product_mentioned"))
        if prod in used_products and len(gut_punch) < 8:
            continue  # prefer different competitors
        gut_punch.append((idx, q, cat, prod))
        used_products.add(prod)
        if len(gut_punch) >= 4:
            break
    # If we didn't get 4 diverse ones, fill from top
    if len(gut_punch) < 4:
        for combined, pull_dev, idx, q, cat in all_quotes_scored:
            if any(gp[0] == idx for gp in gut_punch):
                continue
            prod = normalize_product(q["llm"].get("product_mentioned"))
            gut_punch.append((idx, q, cat, prod))
            if len(gut_punch) >= 4:
                break

    # ================================================================
    # BUILD MARKDOWN — MBB STORY FORMAT
    # ================================================================
    lines = []

    # ── Section 1: Headline ──────────────────────────────────────────
    lines.append("# Why Answering Services Lose Customers — And What It Means for Central AI")
    lines.append("")
    lines.append("> **Half of all answering service churn comes from problems AI solves on day one —**")
    lines.append("> **and incumbents structurally cannot fix them.**")
    lines.append("")
    lines.append(f"*Based on {total_count} churn quotes from real customers of Ruby, AnswerConnect, PATLive,")
    lines.append("Smith.ai, and others — scraped from Reddit and Trustpilot (2015–2026).*")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Section 2: Voice of the Customer (Gut-Punch) ─────────────────
    lines.append("## 1. The Voice of the Customer")
    lines.append("")
    lines.append("Before the data — hear what real customers are saying:")
    lines.append("")

    for idx, q, cat, prod in gut_punch:
        pain = q["llm"].get("pain_point", "")
        pull = extract_pull_quote(q["text"])
        lines.append(f"> **\"{pull}\"**")
        lines.append(f">")
        lines.append(f"> — *{prod} customer* | {pain}")
        if q.get("url"):
            lines.append(f"> [Source]({q['url']})")
        lines.append("")

    lines.append("---")
    lines.append("")

    # ── Section 3: The Proof (4-Group View) ──────────────────────────
    lines.append("## 2. Where the Pain Concentrates")
    lines.append("")
    lines.append("137 churn quotes. 4 pain clusters. One clear pattern:")
    lines.append("")

    # ASCII bar chart at group level
    lines.append("```")
    for g in GROUP_ORDER:
        if g not in group_stats:
            continue
        gs = group_stats[g]
        pct = gs["weighted"] / total_weighted * 100
        bar_len = int(pct / 100 * 40)
        lines.append(f"  {g:<25} {'█' * bar_len}{'░' * (40 - bar_len)}  {pct:.0f}%  ({gs['count']} quotes)")
    lines.append("```")
    lines.append("")

    # Group detail cards
    for g in GROUP_ORDER:
        if g not in group_stats:
            continue
        gs = group_stats[g]
        gm = GROUP_META.get(g, {})
        pct = gs["weighted"] / total_weighted * 100
        cat_labels = ", ".join(CATEGORY_META.get(c, {}).get("short", c)
                               for c in sorted(gs["cats"], key=lambda c: cat_stats[c]["weighted"], reverse=True))
        lines.append(f"**{g}** — {pct:.0f}% of all churn ({gs['count']} quotes)")
        lines.append(f"- *Includes:* {cat_labels}")
        lines.append(f"- *Insight:* {gm.get('insight', '')}")
        lines.append(f"- *Product implication:* {gm.get('implication', '')}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # ── Section 4: The Zoom-In ───────────────────────────────────────
    lines.append("## 3. The Full Picture — 11 Validated Churn Reasons")
    lines.append("")
    lines.append("Each of the 4 groups breaks down into specific, actionable failure modes:")
    lines.append("")

    lines.append("| Rank | Churn Reason | Group | Count | % | Cumul. % |")
    lines.append("|:---:|---|---|:---:|:---:|:---:|")

    cumulative = 0
    for rank, cat in enumerate(sorted_cats, 1):
        s = cat_stats[cat]
        meta = CATEGORY_META.get(cat, {})
        pct = s["weighted"] / total_weighted * 100
        cumulative += pct
        label = meta.get("short", cat)
        group = meta.get("group", "")
        lines.append(f"| {rank} | **{label}** | {group} | {s['count']} | {pct:.1f}% | {cumulative:.1f}% |")

    lines.append(f"| | **Total** | | **{total_count}** | **100%** | |")
    lines.append("")

    # Competitor Vulnerability Map
    lines.append("### Who's Most Vulnerable — And Where")
    lines.append("")
    lines.append("Not all competitors break the same way. Here's where each one's customers hurt most:")
    lines.append("")

    # Header
    header = "| Competitor | Quotes |"
    sep = "|---|:---:|"
    for g in GROUP_ORDER:
        header += f" {g} |"
        sep += " :---:|"
    lines.append(header)
    lines.append(sep)

    for prod in TOP_COMPETITORS:
        total_prod = sum(comp_groups.get(prod, {}).values())
        row = f"| **{prod}** | {total_prod} |"
        for g in GROUP_ORDER:
            count = comp_groups.get(prod, {}).get(g, 0)
            pct = count / total_prod * 100 if total_prod > 0 else 0
            row += f" {pct:.0f}% |"
        lines.append(row)

    lines.append("")

    # Competitor targeting insights — highlight what's DIFFERENT about each
    lines.append("**Targeting insights:**")
    lines.append("")

    # Compute overall average distribution for comparison
    overall_group_pcts = {g: group_stats[g]["weighted"] / total_weighted for g in GROUP_ORDER if g in group_stats}

    for prod in TOP_COMPETITORS:
        cats = comp_cats.get(prod, Counter())
        total_prod = sum(cats.values())
        if total_prod == 0:
            continue
        groups = comp_groups.get(prod, Counter())

        # Find where this competitor OVER-INDEXES vs average
        over_indexed = []
        for g in GROUP_ORDER:
            prod_pct = groups.get(g, 0) / total_prod
            avg_pct = overall_group_pcts.get(g, 0)
            if prod_pct > avg_pct + 0.05:  # >5pp above average
                over_indexed.append((g, prod_pct, avg_pct))

        # Top 2 specific categories
        top2 = cats.most_common(2)
        top2_text = " + ".join(f"{CATEGORY_META.get(c, {}).get('short', c)} ({cnt}/{total_prod})" for c, cnt in top2)

        # Build differentiated insight
        if over_indexed:
            oi = over_indexed[0]
            oi_label = oi[0].lower()
            oi_pct = oi[1] * 100
            avg_pct = oi[2] * 100
            lines.append(f"- **{prod}** ({total_prod} quotes): Over-indexed on **{oi_label}** "
                         f"({oi_pct:.0f}% vs {avg_pct:.0f}% avg). Top pains: {top2_text}.")
        else:
            lines.append(f"- **{prod}** ({total_prod} quotes): Broadly distributed. Top pains: {top2_text}.")

    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Section 5: The Action ────────────────────────────────────────
    lines.append("## 4. What This Means for Central AI")
    lines.append("")

    # 5a: Product Roadmap Signal
    lines.append("### Product Roadmap Signal")
    lines.append("")
    lines.append("Ordered by weighted impact — what to nail first:")
    lines.append("")

    # Group the categories into product capability areas
    roadmap = [
        {
            "capability": "AI Training & Business Knowledge",
            "cats": ["SCRIPT_ADHERENCE", "INAUTHENTICITY"],
            "action": "The AI must know the business cold — services, hours, team names, FAQs. No re-training, no drift, no \"we can't do that.\"",
        },
        {
            "capability": "Transparent Pricing",
            "cats": ["BILLING_PREDATORY", "BILLING_OPAQUE", "BILLING_TRAP", "BILLING_TOO_EXPENSIVE"],
            "action": "Flat-rate or simple per-call pricing. Real-time usage dashboard. Cancel in one click. No contracts, no overages, no surprises.",
        },
        {
            "capability": "Data Capture Accuracy",
            "cats": ["GARBLED_INFO"],
            "action": "AI captures names, emails, phone numbers perfectly. Zero-error message delivery.",
        },
        {
            "capability": "Consistent Availability",
            "cats": ["MISSED_CALLS", "QUALITY_DECAY", "ROUTING_ERRORS"],
            "action": "AI answers every call instantly. Same quality on day 1 and day 1,000. Rules-based routing — no human memory failures.",
        },
    ]

    for i, r in enumerate(roadmap, 1):
        cat_pct = sum(cat_stats.get(c, {}).get("weighted", 0) for c in r["cats"]) / total_weighted * 100
        cat_count = sum(cat_stats.get(c, {}).get("count", 0) for c in r["cats"])
        lines.append(f"**{i}. {r['capability']}** — {cat_pct:.0f}% of churn pain ({cat_count} quotes)")
        lines.append(f"- {r['action']}")
        lines.append("")

    # 5b: GTM Messaging Hierarchy
    lines.append("### GTM Messaging Hierarchy")
    lines.append("")
    lines.append("What to say, and where to say it:")
    lines.append("")
    lines.append("| Channel | Message | Pain It Addresses | % of Churn |")
    lines.append("|---|---|---|:---:|")

    call_handling_pct = group_stats.get("CALL HANDLING", {}).get("weighted", 0) / total_weighted * 100
    billing_pct = group_stats.get("BILLING", {}).get("weighted", 0) / total_weighted * 100
    reliability_pct = group_stats.get("SERVICE RELIABILITY", {}).get("weighted", 0) / total_weighted * 100
    disillusion_pct = group_stats.get("INDUSTRY DISILLUSIONMENT", {}).get("weighted", 0) / total_weighted * 100

    lines.append(f"| **Homepage headline** | \"An AI receptionist that actually knows your business\" | Call handling | {call_handling_pct:.0f}% |")
    lines.append(f"| **Pricing page** | \"Flat rate. No per-minute games. Cancel anytime.\" | Billing | {billing_pct:.0f}% |")
    lines.append(f"| **Comparison pages** | \"Same quality on day 1,000 as day 1\" | Reliability + decay | {reliability_pct:.0f}% |")
    lines.append(f"| **Sales calls** | \"We're not another answering service — we're a different technology\" | Serial switchers | {disillusion_pct:.0f}% |")
    lines.append(f"| **Demo CTA** | \"Call our AI right now. Try to stump it.\" | Inauthenticity | {cat_stats.get('INAUTHENTICITY', {}).get('weighted', 0) / total_weighted * 100:.0f}% |")
    lines.append("")

    # 5c: Competitive Targeting
    lines.append("### Competitive Targeting — Who to Go After First")
    lines.append("")

    for prod in TOP_COMPETITORS:
        cats = comp_cats.get(prod, Counter())
        total_prod = sum(cats.values())
        if total_prod == 0:
            continue
        groups = comp_groups.get(prod, Counter())

        # Top 3 categories for this competitor
        top3 = cats.most_common(3)

        lines.append(f"**{prod}** ({total_prod} churner quotes)")
        lines.append("")

        for cat, count in top3:
            meta = CATEGORY_META.get(cat, {})
            pct = count / total_prod * 100
            lines.append(f"- {meta.get('short', cat)}: {count} quotes ({pct:.0f}%) → {meta.get('gtm', '')}")

        # Find best quote for this competitor
        comp_quotes = [(idx, q, w) for idx, q, w in
                       [(idx, quotes[idx], compute_weight(quotes[idx]))
                        for idx in final_codes if normalize_product(quotes[idx]["llm"].get("product_mentioned")) == prod]
                       if q["llm"].get("quote_quality", 1) >= 4]
        if comp_quotes:
            comp_quotes.sort(key=lambda x: devastation_score(x[1]["text"]) * x[2], reverse=True)
            best = comp_quotes[0]
            pain = best[1]["llm"].get("pain_point", "")
            lines.append(f"- *Voice of their customer:* \"{pain}\"")

        lines.append("")

    lines.append("---")
    lines.append("")

    # ── Section 6: Representative Quotes by Category ─────────────────
    lines.append("## 5. Evidence Base — Quotes by Category")
    lines.append("")
    lines.append("*Top 2 quotes per category, ranked by engagement and quality.*")
    lines.append("")

    for cat in sorted_cats:
        s = cat_stats[cat]
        meta = CATEGORY_META.get(cat, {})
        top = sorted(s["quotes"], key=lambda x: x[2], reverse=True)[:2]
        lines.append(f"### {meta.get('label', cat)} ({s['count']} quotes, {s['weighted'] / total_weighted * 100:.1f}%)")
        lines.append("")
        for j, (idx, q, w) in enumerate(top, 1):
            product = normalize_product(q["llm"].get("product_mentioned"))
            pain = q["llm"].get("pain_point", "")
            lines.append(f"**{j}.** ({product}) *{pain}*")
            lines.append(f"> {truncate(q['text'])}")
            if q.get("url"):
                lines.append(f"> [Source]({q['url']})")
            lines.append("")
        lines.append("---")
        lines.append("")

    # ── Section 7: Appendix ──────────────────────────────────────────
    lines.append("## Appendix: Methodology & Statistical Backing")
    lines.append("")
    lines.append("*This section is for peer review. The analysis above stands on its own.*")
    lines.append("")

    lines.append("### How We Got These Numbers")
    lines.append("")
    lines.append("1. **Data collection:** Scraped Reddit (r/LawFirm, r/smallbusiness, etc.) and Trustpilot reviews")
    lines.append("   for 9 answering service competitors. 378 quotes classified, 137 tagged as churn-related.")
    lines.append("2. **Taxonomy:** Built a codebook with 11 mutually exclusive categories, each with explicit")
    lines.append("   inclusion/exclusion rules and tie-breakers (see `codebook_k9.md`).")
    lines.append("3. **Dual coding:** Two independent LLM coders classified all 137 quotes using the codebook.")
    lines.append("4. **Adjudication:** 127 of 137 (92.7%) agreed. 10 disagreements resolved by defaulting to Coder A.")
    lines.append("5. **Weighting:** Each quote weighted by `quality (1-5) × engagement`. Reddit engagement =")
    lines.append("   `log₂(upvotes)` (community validation). Trustpilot = 1.0 (all reviews equally deliberate).")
    lines.append("")

    lines.append("### Inter-Rater Reliability")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append("| Cohen's kappa (k=11) | 0.917 (almost perfect) |")
    lines.append("| 95% bootstrap CI | [0.863, 0.965] |")
    lines.append("| Raw agreement | 127/137 (92.7%) |")
    lines.append("| Disagreements | 10/137 (7.3%) — no systematic confusion patterns |")
    lines.append("| CI overlap test | CIs overlap at k=7 through k=11 — granularity is a business decision |")
    lines.append("")

    lines.append("### Why 11 Categories, Not 4 or 7")
    lines.append("")
    lines.append("We tested kappa at k=3 through k=11. All CIs overlap (no significant difference).")
    lines.append("k=11 was chosen because it's the most *actionable* — distinguishing \"predatory billing\"")
    lines.append("from \"opaque billing\" from \"billing trap\" changes what you build and what you say.")
    lines.append("The 4-group view (Section 2) provides the summary; the 11-category view (Section 3) provides the action.")
    lines.append("")

    lines.append("### Sample Composition")
    lines.append("")
    lines.append(f"| Source | Quotes | Notes |")
    lines.append("|---|:---:|---|")

    reddit_count = sum(1 for idx in final_codes if quotes[idx]["source"] == "reddit")
    tp_count = sum(1 for idx in final_codes if quotes[idx]["source"] == "trustpilot")
    lines.append(f"| Reddit | {reddit_count} | Upvotes provide community validation signal |")
    lines.append(f"| Trustpilot | {tp_count} | Verified reviews, no engagement signal |")
    lines.append(f"| **Total** | **{total_count}** | |")
    lines.append("")

    # Write
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(lines))

    print(f"\nFinal Pareto written to {OUTPUT_FILE}")
    print(f"\nRanking:")
    cumulative = 0
    for rank, cat in enumerate(sorted_cats, 1):
        s = cat_stats[cat]
        pct = s["weighted"] / total_weighted * 100
        cumulative += pct
        label = CATEGORY_META.get(cat, {}).get("short", cat)
        print(f"  {rank}. {label}: {s['count']} quotes, {pct:.1f}% (cumul {cumulative:.1f}%)")


if __name__ == "__main__":
    main()
