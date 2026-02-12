#!/usr/bin/env python3
"""
Reddit Research Scraper via Arctic Shift API
Collects posts and comments about AI receptionists for Central (trycentral.com).

Uses Arctic Shift (https://arctic-shift.photon-reddit.com) — a free Reddit archive API.
No credentials needed. No rate limit games. No bot detection risk.

Usage:
    python3 arctic_shift_scraper.py
"""

import json
import time
import os
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError

# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reddit_data")

RAW_POSTS_FILE = os.path.join(OUTPUT_DIR, "posts.jsonl")
RAW_COMMENTS_FILE = os.path.join(OUTPUT_DIR, "comments.jsonl")
QUOTES_DIR = os.path.join(OUTPUT_DIR, "quotes")  # one .md per bucket
SUMMARY_FILE = os.path.join(OUTPUT_DIR, "collection_summary.md")

# Arctic Shift API
BASE_URL = "https://arctic-shift.photon-reddit.com/api"

# Be respectful — 2s between requests, longer pause every 20 requests
REQUEST_DELAY = 2.0
BATCH_PAUSE_EVERY = 20
BATCH_PAUSE_SECONDS = 5

# Date filter: last 3 years
AFTER_DATE = "2023-01-01"

# ──────────────────────────────────────────────────────────────────────
# Search targets
# ──────────────────────────────────────────────────────────────────────

# Arctic Shift comment body search 422s on very active subreddits.
# Split into small (post + comment search) and large (post-only).
SMALL_SUBREDDITS = [
    "lawfirm",
    "dentistry",
    "realtors",
    "HVAC",
    "Plumbing",
    "Electricians",
    "bookkeeping",
    "VoIP",
    "msp",
    "legaltech",
    "agency",
    "consulting",
]

LARGE_SUBREDDITS = [
    "smallbusiness",
    "Entrepreneur",
    "freelance",
    "sales",
    "SaaS",
    "digital_marketing",
    "marketing",
    "startups",
]

ALL_SUBREDDITS = SMALL_SUBREDDITS + LARGE_SUBREDDITS

# ──────────────────────────────────────────────────────────────────────
# Search Queries — focused on CHURN REASONS and CONVERSION BLOCKERS
# These are the two deliverables for the CPO:
#   1. Why do users STOP using AI receptionists?
#   2. Why do potential users NEVER start?
# ──────────────────────────────────────────────────────────────────────

SEARCH_QUERIES = {
    # ── CHURN: Why they left ──
    "churn_billing": [
        "answering service bill",
        "receptionist overcharged",
        "per minute receptionist",
        "answering service expensive",
        "ruby receptionist bill",
        "answering service hidden fees",
    ],
    "churn_voice_quality": [
        "AI receptionist robotic",
        "answering service sounds fake",
        "AI phone sounds bad",
        "customers hate AI phone",
        "robotic answering service",
    ],
    "churn_cant_handle_calls": [
        "AI receptionist wrong answer",
        "answering service lost lead",
        "AI receptionist confused",
        "answering service mistake",
        "receptionist dropped call",
        "AI loop phone",
    ],
    "churn_switched_away": [
        "switched answering service",
        "cancelled receptionist",
        "stopped using answering",
        "left ruby receptionist",
        "quit answering service",
        "dropped smith.ai",
    ],
    "churn_general": [
        "answering service terrible",
        "receptionist not worth",
        "AI receptionist problem",
        "worst answering service",
        "receptionist complaint",
        "answering service disappointed",
        "waste of money receptionist",
    ],

    # ── NON-CONVERSION: Why they never started ──
    "blocker_trust": [
        "don't trust AI phone",
        "worried AI receptionist",
        "AI receptionist risk",
        "customers won't accept AI",
        "afraid AI answering",
        "AI phone unprofessional",
    ],
    "blocker_not_ready": [
        "not ready AI receptionist",
        "voicemail good enough",
        "don't need receptionist",
        "receptionist overkill",
        "too small for receptionist",
    ],
    "blocker_tried_and_rejected": [
        "tried AI receptionist",
        "tested answering service",
        "AI receptionist demo bad",
        "receptionist didn't work",
        "gave up answering service",
    ],

    # ── COMPETITOR EXPERIENCE (churn signal-rich) ──
    "competitor_experience": [
        "smith.ai review",
        "ruby receptionist review",
        "my ai front desk review",
        "dialzara review",
        "goodcall review",
        "frontdesk ai review",
        "abby connect review",
        "answering service recommendation",
        "virtual receptionist best",
        "AI receptionist which one",
    ],

    # ── PRICING (conversion + churn signal) ──
    "pricing": [
        "receptionist pricing",
        "answering service cost",
        "how much receptionist",
        "per minute vs flat rate",
        "receptionist budget",
        "AI receptionist worth it",
    ],

    # ── AI-NATIVE COMPETITOR EXPERIENCE ──
    "ai_native_experience": [
        "synthflow review",
        "dialzara review",
        "bland ai review",
        "my ai front desk review",
        "goodcall receptionist",
        "rosie ai receptionist",
        "upfirst answering",
        "AI receptionist switched from",
        "AI receptionist not good enough",
        "AI answering service problem",
    ],
}

# Competitor detection keywords
COMPETITORS = {
    "Smith.ai": ["smith.ai", "smithai", "smith ai"],
    "Ruby Receptionist": ["ruby receptionist", "ruby receptionists"],
    "My AI Front Desk": ["my ai front desk", "myaifrontdesk"],
    "Dialzara": ["dialzara"],
    "Synthflow": ["synthflow"],
    "Goodcall": ["goodcall"],
    "Frontdesk AI": ["frontdesk ai", "frontdesk.ai"],
    "Abby Connect": ["abby connect"],
    "Rosie": ["rosie ai", "rosie.ai", "heyrosie"],
    "CallBird AI": ["callbird"],
    "Upfirst": ["upfirst"],
    "Jobber": ["jobber"],
    "TrueLark": ["truelark"],
    "OpenPhone": ["openphone"],
    "Wing Assistant": ["wing assistant", "wingassistant"],
    "Nexa": ["nexa receptionist", "nexa virtual"],
    "PATLive": ["patlive"],
    "AnswerConnect": ["answerconnect"],
    "Vonage": ["vonage"],
    "Bland AI": ["bland.ai", "bland ai"],
    "Welco AI": ["welco.ai", "welco ai"],
    "Answering Agent": ["answering agent", "answeringagent"],
}

# ──────────────────────────────────────────────────────────────────────
# API helpers
# ──────────────────────────────────────────────────────────────────────

request_count = 0


def api_request(endpoint, params):
    """Make a request to Arctic Shift API with pacing."""
    global request_count
    request_count += 1

    # Batch pause
    if request_count % BATCH_PAUSE_EVERY == 0:
        print(f"    [Pausing {BATCH_PAUSE_SECONDS}s after {request_count} requests...]")
        time.sleep(BATCH_PAUSE_SECONDS)

    url = f"{BASE_URL}{endpoint}?{urlencode(params)}"
    req = Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; research)")

    for attempt in range(2):  # max 2 attempts (down from 3)
        try:
            with urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            time.sleep(REQUEST_DELAY)
            return data.get("data", [])
        except HTTPError as e:
            if e.code == 422:
                # Arctic Shift returns 422 on comment body search for active subreddits
                # Fail fast — retrying won't help
                return []
            elif e.code == 400:
                body = e.read().decode("utf-8") if hasattr(e, "read") else ""
                if "Timeout" in body or "slow down" in body:
                    wait = (attempt + 1) * 5
                    print(f"    API timeout, waiting {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"    400 Bad Request: {body[:100]}")
                    return []
            elif e.code == 429:
                wait = (attempt + 1) * 10
                print(f"    Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"    HTTP {e.code}, attempt {attempt + 1}/2")
                time.sleep(3)
        except (URLError, TimeoutError, OSError, Exception) as e:
            print(f"    Connection error: {e}, attempt {attempt + 1}/2")
            time.sleep(3)

    return []


def search_posts(subreddit, query, limit=100):
    """Search posts by title in a subreddit."""
    return api_request("/posts/search", {
        "subreddit": subreddit,
        "title": query,
        "after": AFTER_DATE,
        "limit": min(limit, 100),
        "sort": "desc",
    })


def search_comments(subreddit, query, limit=100):
    """Search comments by body text in a subreddit."""
    return api_request("/comments/search", {
        "subreddit": subreddit,
        "body": query,
        "after": AFTER_DATE,
        "limit": min(limit, 100),
        "sort": "desc",
    })


# ──────────────────────────────────────────────────────────────────────
# Processing helpers
# ──────────────────────────────────────────────────────────────────────

def detect_competitors(text):
    """Find competitor mentions in text."""
    text_lower = text.lower()
    found = []
    for name, keywords in COMPETITORS.items():
        for kw in keywords:
            if kw in text_lower:
                found.append(name)
                break
    return found


def classify_bucket(text):
    """Classify text into churn-reason and conversion-blocker buckets.

    Focused on the two CPO deliverables:
      1. Why users CHURN from AI receptionists
      2. Why potential users DON'T CONVERT
    """
    text_lower = text.lower()
    buckets = []

    # ── Churn reasons (specific) ──
    billing_kw = ["overcharged", "bill shock", "per minute", "hidden fee", "billing",
                  "too expensive", "price increase", "cost too much", "surprise charge",
                  "$", "invoice", "charged for spam", "paying for robocall"]
    voice_kw = ["sounds robotic", "sounds fake", "sounds weird", "robotic voice",
                "unnatural", "callers hang up", "customers complain about voice",
                "doesn't sound human", "obvious it's ai", "can tell it's ai"]
    cant_handle_kw = ["wrong answer", "gave wrong info", "confused caller", "lost lead",
                      "couldn't handle", "got it wrong", "inaccurate", "misunderstood",
                      "ai loop", "stuck in loop", "couldn't transfer", "couldn't route"]
    switched_kw = ["switched from", "stopped using", "cancelled", "went back to",
                   "dropped", "quit using", "moved away from", "replaced with",
                   "left for", "ditched"]
    general_churn_kw = ["terrible", "horrible", "worst", "waste of money",
                        "not worth", "disappointed", "regret", "frustrating",
                        "complaint", "do not recommend", "wouldn't recommend"]

    # ── Conversion blockers ──
    trust_kw = ["don't trust", "worried about", "afraid", "risk", "unprofessional",
                "won't accept ai", "clients won't like", "customers won't accept",
                "scared to", "nervous about", "not comfortable"]
    not_ready_kw = ["don't need", "overkill", "too small", "not enough calls",
                    "voicemail is fine", "good enough without", "not worth it yet",
                    "maybe later", "not ready"]
    tried_rejected_kw = ["tried it", "tested it", "demo was bad", "didn't work out",
                         "gave up on", "it was terrible", "went back to voicemail",
                         "tried and", "tested but"]

    # ── Positive (keep for contrast / competitor intel) ──
    positive_kw = ["love it", "game changer", "highly recommend", "best thing",
                   "worth every penny", "saved us", "couldn't live without",
                   "amazing", "fantastic service", "10/10"]

    # ── Pricing discussions ──
    pricing_kw = ["pricing", "cost", "how much", "per minute", "flat rate",
                  "worth it", "budget", "roi", "pay for", "subscription"]

    # Classify — a quote can belong to multiple buckets
    for kw in billing_kw:
        if kw in text_lower:
            buckets.append("churn_billing")
            break
    for kw in voice_kw:
        if kw in text_lower:
            buckets.append("churn_voice_quality")
            break
    for kw in cant_handle_kw:
        if kw in text_lower:
            buckets.append("churn_cant_handle")
            break
    for kw in switched_kw:
        if kw in text_lower:
            buckets.append("churn_switched")
            break
    for kw in general_churn_kw:
        if kw in text_lower:
            buckets.append("churn_general")
            break
    for kw in trust_kw:
        if kw in text_lower:
            buckets.append("blocker_trust")
            break
    for kw in not_ready_kw:
        if kw in text_lower:
            buckets.append("blocker_not_ready")
            break
    for kw in tried_rejected_kw:
        if kw in text_lower:
            buckets.append("blocker_tried_rejected")
            break
    for kw in positive_kw:
        if kw in text_lower:
            buckets.append("positive")
            break
    for kw in pricing_kw:
        if kw in text_lower:
            buckets.append("pricing")
            break

    return buckets if buckets else ["general"]


def ts_to_date(ts):
    """Convert unix timestamp to date string."""
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    except (ValueError, OSError):
        return ""


# ──────────────────────────────────────────────────────────────────────
# Main scraper
# ──────────────────────────────────────────────────────────────────────

def format_quote_md(q):
    """Format a single quote as markdown."""
    comp_str = f" | Mentions: **{', '.join(q['competitors'])}**" if q["competitors"] else ""
    title_str = f"**{q['title']}**\n\n" if q.get("title") and q["type"] == "post" else ""
    return (
        f"### r/{q['subreddit']} — {q['date']} | {q['score']}pts{comp_str}\n\n"
        f"{title_str}"
        f"> {q['text']}\n\n"
        f"*— u/{q['author']}* | [{q['type']}]({q['url']})\n\n"
        f"---\n\n"
    )


def make_quote(item_type, item):
    """Turn a raw post or comment into a quote dict. Returns None if too short."""
    if item_type == "post":
        title = item.get("title", "")
        selftext = item.get("selftext", "")
        text = f"{title}\n\n{selftext}".strip() if selftext else title
        if len(text) < 30:
            return None
        return {
            "type": "post",
            "subreddit": item.get("subreddit", ""),
            "date": item.get("_date", ""),
            "author": item.get("author", ""),
            "score": item.get("score", 0),
            "num_comments": item.get("num_comments", 0),
            "title": title,
            "text": text[:3000],
            "url": f"https://reddit.com{item.get('permalink', '')}",
            "competitors": item.get("_competitors", []),
            "search_query": item.get("_search_query", ""),
            "buckets": item.get("_insight_buckets", ["general"]),
        }
    else:
        body = item.get("body", "").strip()
        if len(body) < 30 or body in ("[deleted]", "[removed]"):
            return None
        return {
            "type": "comment",
            "subreddit": item.get("subreddit", ""),
            "date": item.get("_date", ""),
            "author": item.get("author", ""),
            "score": item.get("score", 0),
            "num_comments": 0,
            "title": "",
            "text": body[:3000],
            "url": f"https://reddit.com/r/{item.get('subreddit', '')}/comments/{item.get('link_id', '').replace('t3_', '')}/_/{item.get('id', '')}",
            "competitors": item.get("_competitors", []),
            "search_query": item.get("_search_query", ""),
            "buckets": item.get("_insight_buckets", ["general"]),
        }


def append_quote_to_files(quote, quotes_dir):
    """Append a quote to its bucket markdown files and the all_quotes file immediately."""
    for bucket in quote["buckets"]:
        filepath = os.path.join(quotes_dir, f"{bucket}.md")
        # Create file with header if it doesn't exist
        if not os.path.exists(filepath):
            header = (
                f"# Verbatim Quotes — {bucket.replace('_', ' ').title()}\n\n"
                f"**Source:** Reddit (via Arctic Shift)  \n"
                f"**Collected:** {datetime.now().strftime('%Y-%m-%d')}  \n"
                f"**Status:** Collecting (updates live)\n\n"
                f"---\n\n"
            )
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(header)
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(format_quote_md(quote))

    # Also append to all_quotes.md
    all_path = os.path.join(quotes_dir, "all_quotes.md")
    if not os.path.exists(all_path):
        header = (
            f"# All Verbatim Quotes\n\n"
            f"**Source:** Reddit (via Arctic Shift)  \n"
            f"**Collected:** {datetime.now().strftime('%Y-%m-%d')}  \n"
            f"**Status:** Collecting (updates live)\n\n"
            f"---\n\n"
        )
        with open(all_path, "w", encoding="utf-8") as f:
            f.write(header)
    with open(all_path, "a", encoding="utf-8") as f:
        buckets_str = ", ".join(quote["buckets"])
        comp_str = f" | Mentions: **{', '.join(quote['competitors'])}**" if quote["competitors"] else ""
        md = (
            f"### r/{quote['subreddit']} — {quote['date']} | {quote['score']}pts | `{buckets_str}`{comp_str}\n\n"
        )
        if quote.get("title") and quote["type"] == "post":
            md += f"**{quote['title']}**\n\n"
        md += f"> {quote['text']}\n\n"
        md += f"*— u/{quote['author']}* | [{quote['type']}]({quote['url']})\n\n"
        md += "---\n\n"
        f.write(md)


def append_raw_jsonl(item, filepath):
    """Append a single item as a JSON line to a .jsonl file."""
    with open(filepath, "a") as f:
        f.write(json.dumps(item, default=str) + "\n")


def run(only_bucket=None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(QUOTES_DIR, exist_ok=True)

    # In append mode (--only-bucket), keep existing files and pre-load seen IDs
    if only_bucket:
        seen_post_ids = set()
        seen_comment_ids = set()
        # Load existing IDs to avoid duplicates
        if os.path.exists(RAW_POSTS_FILE):
            with open(RAW_POSTS_FILE, "r") as f:
                for line in f:
                    try:
                        p = json.loads(line)
                        pid = p.get("id", "")
                        if pid:
                            seen_post_ids.add(pid)
                    except json.JSONDecodeError:
                        pass
        if os.path.exists(RAW_COMMENTS_FILE):
            with open(RAW_COMMENTS_FILE, "r") as f:
                for line in f:
                    try:
                        c = json.loads(line)
                        cid = c.get("id", "")
                        if cid:
                            seen_comment_ids.add(cid)
                    except json.JSONDecodeError:
                        pass
        print(f"[APPEND MODE] Pre-loaded {len(seen_post_ids)} existing post IDs, {len(seen_comment_ids)} comment IDs")
    else:
        # Clean previous run files (full run only)
        for f in os.listdir(QUOTES_DIR):
            os.remove(os.path.join(QUOTES_DIR, f))
        for f in [RAW_POSTS_FILE, RAW_COMMENTS_FILE]:
            if os.path.exists(f):
                os.remove(f)
        seen_post_ids = set()
        seen_comment_ids = set()

    seen_quote_urls = set()  # dedup quotes across buckets for all_quotes
    total_posts = 0
    total_comments = 0
    total_quotes = 0
    bucket_counts = {}
    competitor_counts = {}
    subreddits_hit = set()

    all_queries = []
    for bucket, queries in SEARCH_QUERIES.items():
        if only_bucket and bucket != only_bucket:
            continue
        for q in queries:
            all_queries.append((bucket, q))

    # Count: posts for all subs, comments only for small subs
    n_post_searches = len(all_queries) * len(ALL_SUBREDDITS)
    n_comment_searches = len(all_queries) * len(SMALL_SUBREDDITS)
    total_searches = n_post_searches + n_comment_searches

    print("=" * 60)
    print("Arctic Shift Reddit Scraper — AI Receptionist Research")
    print("=" * 60)
    print(f"Subreddits:     {len(ALL_SUBREDDITS)} ({len(SMALL_SUBREDDITS)} with comments, {len(LARGE_SUBREDDITS)} posts-only)")
    print(f"Queries:        {len(all_queries)}")
    print(f"Post searches:  {n_post_searches}")
    print(f"Comment searches: {n_comment_searches} (small subs only)")
    print(f"Total searches: {total_searches}")
    print(f"Est. time:      ~{total_searches * REQUEST_DELAY / 60:.0f} min")
    print(f"Output:         {OUTPUT_DIR}")
    print(f"Mode:           INCREMENTAL (files update live)")
    print("=" * 60)

    search_num = 0

    for bucket, query in all_queries:
        print(f"\n── [{bucket}] \"{query}\" ──")

        for subreddit in ALL_SUBREDDITS:
            is_small = subreddit in SMALL_SUBREDDITS

            # Search posts (all subreddits)
            search_num += 1
            sys.stdout.write(f"  [{search_num}/{total_searches}] r/{subreddit} posts... ")
            sys.stdout.flush()
            posts = search_posts(subreddit, query)
            new_p = 0
            for p in posts:
                pid = p.get("id", "")
                if pid and pid not in seen_post_ids:
                    text = f"{p.get('title', '')} {p.get('selftext', '')}"
                    p["_search_query"] = query
                    p["_search_bucket"] = bucket
                    p["_competitors"] = detect_competitors(text)
                    p["_insight_buckets"] = classify_bucket(text)
                    p["_date"] = ts_to_date(p.get("created_utc"))
                    seen_post_ids.add(pid)
                    total_posts += 1
                    new_p += 1

                    # Save raw immediately
                    append_raw_jsonl(p, RAW_POSTS_FILE)

                    # Build quote and save to md immediately
                    quote = make_quote("post", p)
                    if quote and quote["url"] not in seen_quote_urls:
                        seen_quote_urls.add(quote["url"])
                        append_quote_to_files(quote, QUOTES_DIR)
                        total_quotes += 1
                        for b in quote["buckets"]:
                            bucket_counts[b] = bucket_counts.get(b, 0) + 1
                        for comp in quote["competitors"]:
                            competitor_counts[comp] = competitor_counts.get(comp, 0) + 1
                        if quote["subreddit"]:
                            subreddits_hit.add(quote["subreddit"])
            print(f"{len(posts)} found, {new_p} new")

            # Search comments (small subreddits only — large ones 422)
            if not is_small:
                continue

            search_num += 1
            sys.stdout.write(f"  [{search_num}/{total_searches}] r/{subreddit} comments... ")
            sys.stdout.flush()
            comments = search_comments(subreddit, query)
            new_c = 0
            for c in comments:
                cid = c.get("id", "")
                if cid and cid not in seen_comment_ids:
                    body = c.get("body", "")
                    c["_search_query"] = query
                    c["_search_bucket"] = bucket
                    c["_competitors"] = detect_competitors(body)
                    c["_insight_buckets"] = classify_bucket(body)
                    c["_date"] = ts_to_date(c.get("created_utc"))
                    seen_comment_ids.add(cid)
                    total_comments += 1
                    new_c += 1

                    # Save raw immediately
                    append_raw_jsonl(c, RAW_COMMENTS_FILE)

                    # Build quote and save to md immediately
                    quote = make_quote("comment", c)
                    if quote and quote["url"] not in seen_quote_urls:
                        seen_quote_urls.add(quote["url"])
                        append_quote_to_files(quote, QUOTES_DIR)
                        total_quotes += 1
                        for b in quote["buckets"]:
                            bucket_counts[b] = bucket_counts.get(b, 0) + 1
                        for comp in quote["competitors"]:
                            competitor_counts[comp] = competitor_counts.get(comp, 0) + 1
                        if quote["subreddit"]:
                            subreddits_hit.add(quote["subreddit"])
            print(f"{len(comments)} found, {new_c} new")

    # ── Final summary ──
    print(f"\n{'=' * 60}")
    print(f"Collection complete.")
    print(f"  Posts:    {total_posts}")
    print(f"  Comments: {total_comments}")
    print(f"  Quotes:   {total_quotes}")
    print(f"{'=' * 60}")

    sorted_comps = sorted(competitor_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_buckets = sorted(bucket_counts.items(), key=lambda x: x[1], reverse=True)

    summary = f"""# Reddit Scraper — Collection Summary

**Run Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Source:** Arctic Shift API (Reddit archive)
**Date Filter:** After {AFTER_DATE}

## Stats

| Metric | Count |
|---|---|
| Unique posts | {total_posts} |
| Unique comments | {total_comments} |
| Unique quotes | {total_quotes} |
| Quote buckets | {len(bucket_counts)} |
| Subreddits with data | {len(subreddits_hit)} |
| API requests made | {request_count} |

## Subreddits Represented

{', '.join(f'r/{s}' for s in sorted(subreddits_hit))}

## Competitor Mentions

| Competitor | Mentions |
|---|---|
"""
    for comp, count in sorted_comps:
        summary += f"| {comp} | {count} |\n"

    summary += f"""
## Insight Buckets

| Bucket | Count |
|---|---|
"""
    for b, count in sorted_buckets:
        summary += f"| {b} | {count} |\n"

    summary += """
## Files

- `posts.jsonl` — Raw post data (one JSON per line)
- `comments.jsonl` — Raw comment data (one JSON per line)
- `quotes/churn_billing.md` — Left because of billing / pricing surprises
- `quotes/churn_voice_quality.md` — Left because AI sounded robotic
- `quotes/churn_cant_handle.md` — Left because AI gave wrong answers / lost leads
- `quotes/churn_switched.md` — Switched to another service
- `quotes/churn_general.md` — General dissatisfaction
- `quotes/blocker_trust.md` — Never converted — don't trust AI with customers
- `quotes/blocker_not_ready.md` — Never converted — don't feel they need it yet
- `quotes/blocker_tried_rejected.md` — Tried it, rejected it
- `quotes/pricing.md` — Pricing discussions
- `quotes/positive.md` — Positive reviews (for competitor intel)
- `quotes/general.md` — Relevant but uncategorized
- `quotes/all_quotes.md` — All unique quotes
- `collection_summary.md` — This file
"""

    with open(SUMMARY_FILE, "w") as f:
        f.write(summary)
    print(f"Saved summary → {SUMMARY_FILE}")

    print(f"\n{'=' * 60}")
    print(f"DONE — {total_quotes} unique verbatim quotes collected")
    print(f"Quote files in: {QUOTES_DIR}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    # --only-bucket BUCKET_NAME to run a single query bucket (appends to existing files)
    only_bucket = None
    for i, arg in enumerate(sys.argv):
        if arg == "--only-bucket" and i + 1 < len(sys.argv):
            only_bucket = sys.argv[i + 1]
            break
    run(only_bucket=only_bucket)
