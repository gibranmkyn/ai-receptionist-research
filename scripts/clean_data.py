#!/usr/bin/env python3
"""
Data Cleaning Pipeline — AI Receptionist Research
Heuristic cascade + LLM structured extraction.

Layer 1: Hard filters (length, score, deleted, fuzzy dedup)
Layer 2: Domain relevance (must mention receptionist/answering service + experience marker)
Layer 3: LLM structured extraction (one Claude call per surviving quote)

Usage:
    python3 clean_data.py                  # Layers 1-2 only (no API key needed)
    ANTHROPIC_API_KEY=sk-... python3 clean_data.py   # Full pipeline with LLM
"""

import json
import os
import re
import sys
from datetime import datetime
from difflib import SequenceMatcher
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REDDIT_DIR = os.path.join(BASE_DIR, "reddit_data")
REVIEW_DIR = os.path.join(BASE_DIR, "review_data")
CLEAN_DIR = os.path.join(BASE_DIR, "clean_quotes")

POSTS_FILE = os.path.join(REDDIT_DIR, "posts.jsonl")
COMMENTS_FILE = os.path.join(REDDIT_DIR, "comments.jsonl")

# ──────────────────────────────────────────────────────────────────────
# Layer 1: Hard filter thresholds
# ──────────────────────────────────────────────────────────────────────

MIN_TEXT_LENGTH = 100       # chars — short comments rarely have insight
MIN_SCORE = 2               # Reddit score — community-validated
FUZZY_DEDUP_THRESHOLD = 0.8 # SequenceMatcher ratio

# ──────────────────────────────────────────────────────────────────────
# Layer 2: Domain relevance terms
# ──────────────────────────────────────────────────────────────────────

DOMAIN_TERMS = [
    # Core domain
    r"receptionist", r"answering service", r"call answering",
    r"phone answering", r"live answering", r"virtual receptionist",
    r"ai phone", r"auto attendant", r"call center",
    r"after.hours.call", r"missed call",
    # Competitor names (strong signal)
    r"smith\.ai", r"ruby receptionist", r"ruby receptionists",
    r"my ai front desk", r"dialzara", r"goodcall", r"frontdesk ai",
    r"abby connect", r"patlive", r"answerconnect", r"nexa",
    r"synthflow", r"rosie\.ai", r"heyrosie", r"callbird",
    r"upfirst", r"truelark", r"openphone", r"vonage",
    r"wing assistant", r"central ai",
    r"bland\.ai", r"bland ai", r"welco\.ai", r"welco ai",
    r"answering agent",
]

EXPERIENCE_MARKERS = [
    r"\bi\s", r"\bwe\s", r"\bmy\b", r"\bour\b",
    r"\btried\b", r"\bused\b", r"\busing\b",
    r"\bswitched\b", r"\bcancell?ed\b",
    r"\bpaying\b", r"\bcost\s+us\b", r"\bcost\s+me\b",
    r"\bleft\b", r"\bdropped\b", r"\bquit\b",
    r"\bsigned up\b", r"\bsubscribed\b",
    r"\brecommend\b", r"\bworth\b", r"\bregret\b",
    r"\bfrustrat", r"\bdisappoint", r"\bterrible\b",
    r"\bamazing\b", r"\bgame.changer\b",
]

# ──────────────────────────────────────────────────────────────────────
# Layer 3: LLM prompt
# ──────────────────────────────────────────────────────────────────────

LLM_SYSTEM = """You are a senior user researcher analyzing Reddit quotes about AI receptionists and answering services.
For each quote, extract structured data. Be strict — if the quote is not actually about a receptionist/answering service experience, mark relevant as false."""

LLM_PROMPT_TEMPLATE = """Analyze this Reddit quote and return ONLY valid JSON (no markdown, no explanation):

QUOTE (from r/{subreddit}, {date}, {score}pts):
\"\"\"{text}\"\"\"

Return this JSON structure:
{{
  "relevant": true/false,
  "pain_point": "one-sentence summary of the pain point, or null if none",
  "category": "churn_billing|churn_voice_quality|churn_cant_handle|churn_switched|churn_general|blocker_trust|blocker_not_ready|blocker_tried_rejected|positive|pricing|general",
  "user_type": "business owner|employee|prospect|consultant|vendor|unknown",
  "product_mentioned": "product name or null",
  "quote_quality": 1-5,
  "presentation_ready": true/false
}}

quote_quality guide:
1 = tangential mention, no insight
2 = relevant but vague
3 = clear experience, some insight
4 = specific pain point with detail
5 = money quote — specific, emotional, representative, citable in a CPO deck"""

# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────

def load_jsonl(filepath):
    """Load a JSONL file into a list of dicts."""
    items = []
    if not os.path.exists(filepath):
        return items
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return items


def extract_text(item):
    """Get the main text from a post or comment."""
    if "selftext" in item:
        # Post
        title = item.get("title", "")
        selftext = item.get("selftext", "")
        return f"{title}\n\n{selftext}".strip() if selftext else title
    else:
        # Comment
        return item.get("body", "").strip()


def extract_url(item):
    """Build a Reddit URL for a post or comment."""
    if "selftext" in item:
        return f"https://reddit.com{item.get('permalink', '')}"
    else:
        sub = item.get("subreddit", "")
        link_id = item.get("link_id", "").replace("t3_", "")
        cid = item.get("id", "")
        return f"https://reddit.com/r/{sub}/comments/{link_id}/_/{cid}"


def fuzzy_match(a, b):
    """Quick fuzzy similarity between two strings."""
    # Use first 500 chars for speed
    return SequenceMatcher(None, a[:500].lower(), b[:500].lower()).ratio()


def call_claude(text, subreddit, date, score, api_key):
    """Call Claude API for structured extraction. Returns dict or None."""
    prompt = LLM_PROMPT_TEMPLATE.format(
        subreddit=subreddit,
        date=date,
        score=score,
        text=text[:2000],
    )

    payload = json.dumps({
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 300,
        "system": LLM_SYSTEM,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = Request("https://api.anthropic.com/v1/messages", data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("x-api-key", api_key)
    req.add_header("anthropic-version", "2023-06-01")

    try:
        with urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        response_text = result["content"][0]["text"].strip()
        # Parse JSON from response (handle potential markdown wrapping)
        response_text = re.sub(r'^```json\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)
        return json.loads(response_text)
    except (HTTPError, json.JSONDecodeError, KeyError, Exception) as e:
        print(f"    LLM error: {e}")
        return None


# ──────────────────────────────────────────────────────────────────────
# Pipeline
# ──────────────────────────────────────────────────────────────────────

FINAL_QUOTES_FILE = os.path.join(CLEAN_DIR, "final_quotes.json")


def run(incremental=False):
    os.makedirs(CLEAN_DIR, exist_ok=True)

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    use_llm = bool(api_key)

    # In incremental mode, load existing final quotes to skip re-processing
    existing_quotes = []
    existing_urls = set()
    if incremental and os.path.exists(FINAL_QUOTES_FILE):
        with open(FINAL_QUOTES_FILE) as f:
            existing_quotes = json.load(f)
        existing_urls = {q["url"] for q in existing_quotes if q.get("url")}
        print(f"[INCREMENTAL] Loaded {len(existing_quotes)} existing quotes ({len(existing_urls)} unique URLs)")

    print("=" * 60)
    print("Data Cleaning Pipeline — AI Receptionist Research")
    print("=" * 60)
    if incremental:
        print(f"Mode:      INCREMENTAL (only process new items)")
    print(f"LLM layer: {'ON (Claude Sonnet)' if use_llm else 'OFF (set ANTHROPIC_API_KEY to enable)'}")
    print(f"Output:    {CLEAN_DIR}")
    print("=" * 60)

    # ── Load raw data ──
    print("\nLoading raw data...")
    posts = load_jsonl(POSTS_FILE)
    comments = load_jsonl(COMMENTS_FILE)

    # Also load Trustpilot reviews
    trustpilot_reviews = []
    tp_raw_dir = os.path.join(REVIEW_DIR, "raw")
    if os.path.exists(tp_raw_dir):
        for fname in os.listdir(tp_raw_dir):
            if fname.endswith(".json"):
                with open(os.path.join(tp_raw_dir, fname)) as f:
                    try:
                        trustpilot_reviews.extend(json.load(f))
                    except json.JSONDecodeError:
                        pass

    # Normalize into a unified format
    all_items = []

    for p in posts:
        text = extract_text(p)
        all_items.append({
            "source": "reddit",
            "type": "post",
            "text": text,
            "author": p.get("author", ""),
            "score": p.get("score", 0),
            "subreddit": p.get("subreddit", ""),
            "date": p.get("_date", ""),
            "url": extract_url(p),
            "competitors": p.get("_competitors", []),
            "original_bucket": p.get("_insight_buckets", ["general"]),
        })

    for c in comments:
        text = extract_text(c)
        all_items.append({
            "source": "reddit",
            "type": "comment",
            "text": text,
            "author": c.get("author", ""),
            "score": c.get("score", 0),
            "subreddit": c.get("subreddit", ""),
            "date": c.get("_date", ""),
            "url": extract_url(c),
            "competitors": c.get("_competitors", []),
            "original_bucket": c.get("_insight_buckets", ["general"]),
        })

    for r in trustpilot_reviews:
        try:
            rating = int(float(r.get("rating", 3)))
        except (ValueError, TypeError):
            rating = 3
        all_items.append({
            "source": "trustpilot",
            "type": "review",
            "text": r.get("text", ""),
            "author": r.get("author", "Anonymous"),
            "score": rating,  # use rating as score
            "subreddit": "",
            "date": r.get("date", ""),
            "url": r.get("review_url", "") or r.get("url", ""),
            "competitors": [r.get("competitor", "")] if r.get("competitor") else [],
            "original_bucket": ["churn_general" if rating <= 2 else "positive" if rating >= 4 else "general"],
            "competitor": r.get("competitor", ""),
            "rating": rating,
            "title": r.get("title", ""),
        })

    total_raw = len(all_items)
    print(f"  Reddit posts:      {len(posts)}")
    print(f"  Reddit comments:   {len(comments)}")
    print(f"  Trustpilot reviews: {len(trustpilot_reviews)}")
    print(f"  Total raw items:   {total_raw}")

    # ══════════════════════════════════════════════════════════════════
    # LAYER 1: Hard Filters
    # ══════════════════════════════════════════════════════════════════
    print(f"\n── Layer 1: Hard Filters ──")

    layer1 = []
    dropped_short = 0
    dropped_score = 0
    dropped_deleted = 0

    for item in all_items:
        text = item["text"]

        # Skip deleted/removed
        if text in ("[deleted]", "[removed]", ""):
            dropped_deleted += 1
            continue

        # Length check
        if len(text) < MIN_TEXT_LENGTH:
            dropped_short += 1
            continue

        # Score check (Reddit only — Trustpilot reviews are all valuable)
        if item["source"] == "reddit" and item["score"] < MIN_SCORE:
            dropped_score += 1
            continue

        layer1.append(item)

    # Fuzzy dedup
    dropped_dedup = 0
    layer1_deduped = []
    for item in layer1:
        is_dup = False
        for existing in layer1_deduped[-50:]:  # check last 50 for speed
            if fuzzy_match(item["text"], existing["text"]) >= FUZZY_DEDUP_THRESHOLD:
                is_dup = True
                # Keep the higher-scored one
                if item["score"] > existing["score"]:
                    layer1_deduped.remove(existing)
                    layer1_deduped.append(item)
                break
        if not is_dup:
            layer1_deduped.append(item)
        else:
            dropped_dedup += 1

    print(f"  Dropped: {dropped_short} too short, {dropped_score} low score, {dropped_deleted} deleted, {dropped_dedup} duplicates")
    print(f"  Surviving: {len(layer1_deduped)}/{total_raw}")

    # ══════════════════════════════════════════════════════════════════
    # LAYER 2: Domain Relevance
    # ══════════════════════════════════════════════════════════════════
    print(f"\n── Layer 2: Domain Relevance ──")

    layer2 = []
    dropped_no_domain = 0
    dropped_no_experience = 0

    for item in layer1_deduped:
        text_lower = item["text"].lower()

        # Trustpilot reviews are inherently domain-relevant (they're reviews of receptionist services)
        if item["source"] == "trustpilot":
            layer2.append(item)
            continue

        # Check domain terms
        has_domain = any(re.search(term, text_lower) for term in DOMAIN_TERMS)
        if not has_domain:
            dropped_no_domain += 1
            continue

        # Check experience markers
        has_experience = any(re.search(marker, text_lower) for marker in EXPERIENCE_MARKERS)
        if not has_experience:
            dropped_no_experience += 1
            continue

        layer2.append(item)

    reddit_surviving = sum(1 for i in layer2 if i["source"] == "reddit")
    tp_surviving = sum(1 for i in layer2 if i["source"] == "trustpilot")
    print(f"  Dropped: {dropped_no_domain} no domain terms, {dropped_no_experience} no experience markers")
    print(f"  Surviving: {len(layer2)}/{len(layer1_deduped)} ({reddit_surviving} Reddit, {tp_surviving} Trustpilot)")

    # ══════════════════════════════════════════════════════════════════
    # LAYER 3: LLM Structured Extraction (if API key available)
    # ══════════════════════════════════════════════════════════════════
    if use_llm:
        print(f"\n── Layer 3: LLM Structured Extraction ──")

        # In incremental mode, separate already-processed from new items
        if incremental and existing_urls:
            new_items = [item for item in layer2 if item["url"] not in existing_urls]
            skipped_items = len(layer2) - len(new_items)
            print(f"  Skipping {skipped_items} already-processed items")
            print(f"  Processing {len(new_items)} NEW quotes through Claude...")
        else:
            new_items = layer2

        layer3 = []
        dropped_irrelevant = 0

        for i, item in enumerate(new_items):
            sys.stdout.write(f"\r  [{i+1}/{len(new_items)}] ")
            sys.stdout.flush()

            result = call_claude(
                item["text"],
                item.get("subreddit", item.get("competitor", "")),
                item["date"],
                item["score"],
                api_key,
            )

            if result is None:
                # API error — keep the item with heuristic-only data
                item["llm"] = None
                layer3.append(item)
                continue

            if not result.get("relevant", True):
                dropped_irrelevant += 1
                continue

            item["llm"] = result
            layer3.append(item)

        print(f"\n  Dropped: {dropped_irrelevant} marked irrelevant by LLM")
        print(f"  New quotes from this run: {len(layer3)}")

        # In incremental mode, merge with existing quotes
        if incremental and existing_quotes:
            final = existing_quotes + layer3
            print(f"  Merged: {len(existing_quotes)} existing + {len(layer3)} new = {len(final)} total")
        else:
            final = layer3
            print(f"  Final: {len(final)} quotes")
    else:
        print(f"\n── Layer 3: Skipped (no API key) ──")
        for item in layer2:
            item["llm"] = None
        final = layer2

    # ══════════════════════════════════════════════════════════════════
    # OUTPUT: Clean Markdown Files
    # ══════════════════════════════════════════════════════════════════
    print(f"\n── Writing Clean Output ──")

    # Sort: LLM quality score desc, then Reddit score desc
    def sort_key(item):
        llm_q = item.get("llm", {}).get("quote_quality", 0) if item.get("llm") else 0
        return (-llm_q, -item.get("score", 0))

    final.sort(key=sort_key)

    # Group by category
    by_category = {}
    for item in final:
        if item.get("llm") and item["llm"].get("category"):
            cat = item["llm"]["category"]
        elif item["source"] == "trustpilot":
            cat = item["original_bucket"][0] if item["original_bucket"] else "general"
        else:
            cat = item["original_bucket"][0] if item["original_bucket"] else "general"
        by_category.setdefault(cat, []).append(item)

    # Write per-category files
    for cat, items in sorted(by_category.items()):
        md = f"# {cat.replace('_', ' ').title()} — Clean Quotes\n\n"
        md += f"**Quotes:** {len(items)}  \n"
        md += f"**Sources:** Reddit + Trustpilot  \n"
        md += f"**Cleaned:** {datetime.now().strftime('%Y-%m-%d')}  \n"
        md += f"**Pipeline:** Hard filters → Domain relevance"
        if use_llm:
            md += " → LLM extraction"
        md += "\n\n---\n\n"

        for i, item in enumerate(items, 1):
            llm = item.get("llm") or {}

            # Quality badge
            quality = llm.get("quote_quality", "?")
            pres = " | PRESENTATION-READY" if llm.get("presentation_ready") else ""
            pain = f"\n**Pain point:** {llm['pain_point']}" if llm.get("pain_point") else ""
            user_type = f" | {llm.get('user_type', '')}" if llm.get("user_type") else ""

            # Source line
            if item["source"] == "trustpilot":
                rating = item.get("rating", "?")
                stars = "★" * rating + "☆" * (5 - rating) if isinstance(rating, int) else "?"
                source_line = f"*— {item['author']}* | [Trustpilot]({item['url']}) | {stars}"
                header = f"### {i}. {item.get('competitor', 'Unknown')} — {item['date']} | Quality: {quality}/5{pres}"
            else:
                source_line = f"*— u/{item['author']}* | [{item['type']}]({item['url']}) | {item['score']}pts"
                header = f"### {i}. r/{item['subreddit']} — {item['date']} | Quality: {quality}/5{pres}"

            comp_str = ""
            if item.get("competitors"):
                comp_str = f" | Mentions: **{', '.join(item['competitors'])}**"
            product_str = ""
            if llm.get("product_mentioned"):
                product_str = f" | Product: **{llm['product_mentioned']}**"

            md += f"{header}{user_type}{comp_str}{product_str}\n"
            if pain:
                md += f"{pain}\n"
            md += f"\n"
            if item["source"] == "trustpilot" and item.get("title"):
                md += f"**\"{item['title']}\"**\n\n"
            md += f"> {item['text'][:3000]}\n\n"
            md += f"{source_line}\n\n"
            md += "---\n\n"

        filepath = os.path.join(CLEAN_DIR, f"{cat}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"  {cat}.md — {len(items)} quotes")

    # Write master file — all quotes sorted by quality
    md_all = f"# All Clean Quotes — AI Receptionist Research\n\n"
    md_all += f"**Total quotes:** {len(final)}  \n"
    md_all += f"**Sources:** Reddit ({sum(1 for i in final if i['source']=='reddit')}), Trustpilot ({sum(1 for i in final if i['source']=='trustpilot')})  \n"
    md_all += f"**Cleaned:** {datetime.now().strftime('%Y-%m-%d')}  \n"
    md_all += f"**Pipeline:** Hard filters → Domain relevance"
    if use_llm:
        md_all += " → LLM extraction"
    md_all += "\n\n"

    # Stats table
    md_all += "## Category Breakdown\n\n"
    md_all += "| Category | Count |\n|---|---|\n"
    for cat, items in sorted(by_category.items(), key=lambda x: -len(x[1])):
        md_all += f"| {cat} | {len(items)} |\n"
    md_all += f"\n---\n\n"

    if use_llm:
        # Presentation-ready quotes first
        pres_ready = [i for i in final if i.get("llm", {}).get("presentation_ready")]
        if pres_ready:
            md_all += f"## Presentation-Ready Quotes ({len(pres_ready)})\n\n"
            md_all += "These quotes are specific, emotional, and representative — ready for your CPO deck.\n\n"
            md_all += "---\n\n"
            for i, item in enumerate(pres_ready, 1):
                llm = item.get("llm", {})
                cat = llm.get("category", "?")
                if item["source"] == "trustpilot":
                    rating = item.get("rating", "?")
                    stars = "★" * rating + "☆" * (5 - rating) if isinstance(rating, int) else "?"
                    md_all += f"### {i}. [{cat}] {item.get('competitor', '?')} — {item['date']} | {stars}\n\n"
                else:
                    md_all += f"### {i}. [{cat}] r/{item['subreddit']} — {item['date']} | {item['score']}pts\n\n"
                if llm.get("pain_point"):
                    md_all += f"**Pain point:** {llm['pain_point']}\n\n"
                if item["source"] == "trustpilot" and item.get("title"):
                    md_all += f"**\"{item['title']}\"**\n\n"
                md_all += f"> {item['text'][:3000]}\n\n"
                if item["source"] == "trustpilot":
                    md_all += f"*— {item['author']}* | [Trustpilot]({item['url']})\n\n"
                else:
                    md_all += f"*— u/{item['author']}* | [{item['type']}]({item['url']})\n\n"
                md_all += "---\n\n"

    with open(os.path.join(CLEAN_DIR, "all_clean_quotes.md"), "w", encoding="utf-8") as f:
        f.write(md_all)
    print(f"  all_clean_quotes.md — {len(final)} quotes")

    # Save structured JSON for further analysis
    json_output = []
    for item in final:
        json_output.append({
            "source": item["source"],
            "type": item["type"],
            "text": item["text"][:3000],
            "author": item["author"],
            "score": item["score"],
            "subreddit": item.get("subreddit", ""),
            "date": item["date"],
            "url": item["url"],
            "competitors": item.get("competitors", []),
            "llm": item.get("llm"),
        })
    with open(os.path.join(CLEAN_DIR, "clean_quotes.json"), "w") as f:
        json.dump(json_output, f, indent=2)
    print(f"  clean_quotes.json — structured data")

    # Also write final_quotes.json (used by report builder)
    with open(FINAL_QUOTES_FILE, "w") as f:
        json.dump(json_output, f, indent=2)
    print(f"  final_quotes.json — {len(json_output)} quotes (report input)")

    # ── Summary ──
    print(f"\n{'=' * 60}")
    print(f"CLEANING COMPLETE")
    print(f"{'=' * 60}")
    print(f"  Raw input:     {total_raw}")
    print(f"  After Layer 1: {len(layer1_deduped)} (hard filters)")
    print(f"  After Layer 2: {len(layer2)} (domain relevance)")
    if use_llm:
        print(f"  After Layer 3: {len(final)} (LLM extraction)")
    print(f"  Final quotes:  {len(final)}")
    print(f"  Output:        {CLEAN_DIR}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    incremental = "--incremental" in sys.argv
    run(incremental=incremental)
