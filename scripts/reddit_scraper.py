#!/usr/bin/env python3
"""
Reddit Scraper for AI Receptionist SMB Research
Collects posts and comments from targeted subreddits using Reddit's public JSON API.
Designed to inform Central (trycentral.com) product roadmap.
"""

import json
import csv
import time
import os
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import quote_plus, urlencode
from urllib.error import HTTPError, URLError

# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reddit_data")
RAW_JSON_FILE = os.path.join(OUTPUT_DIR, "raw_posts.json")
RAW_COMMENTS_FILE = os.path.join(OUTPUT_DIR, "raw_comments.json")
COMBINED_CSV = os.path.join(OUTPUT_DIR, "all_insights.csv")
SUMMARY_FILE = os.path.join(OUTPUT_DIR, "collection_summary.md")

# Rate limiting — Reddit allows ~60 requests per minute for unauthenticated
REQUEST_DELAY = 1.5  # seconds between requests (conservative)
MAX_RETRIES = 3

USER_AGENT = "Mozilla/5.0 (research-bot/1.0; AI-Receptionist-SMB-Study)"

# Time filter: last 2-3 years
TIME_FILTER = "all"  # We'll filter by date in post-processing

# ──────────────────────────────────────────────────────────────────────
# Target Subreddits
# ──────────────────────────────────────────────────────────────────────

PRIMARY_SUBREDDITS = [
    "smallbusiness",
    "Entrepreneur",
    "freelance",
    "consulting",
    "agency",
    "sales",
    "SaaS",
    "lawfirm",
    "dentistry",
    "realtors",
    "HVAC",
    "Plumbing",
    "Electricians",
    "digital_marketing",
    "marketing",
    "bookkeeping",
    "startups",
]

# Also search across all of Reddit for specific queries
GLOBAL_SEARCH = True

# ──────────────────────────────────────────────────────────────────────
# Search Queries (organized by research bucket)
# ──────────────────────────────────────────────────────────────────────

QUERIES = {
    "needs_pain_points": [
        "AI receptionist",
        "phone answering service small business",
        "missed calls business",
        "after hours calls answering",
        "receptionist cost small business",
        "answering service recommendation",
        "voicemail losing customers",
        "never miss a call",
        "call management small business",
        "virtual receptionist",
        "automated phone answering",
        "AI phone answering",
    ],
    "competitor_mentions": [
        "smith.ai",
        "ruby receptionist",
        "ruby receptionists",
        "my ai front desk",
        "dialzara",
        "synthflow receptionist",
        "goodcall business",
        "frontdesk ai",
        "abby connect",
        "answering service best",
        "virtual receptionist which",
        "AI answering service review",
        "wing assistant",
        "rosie ai answering",
        "upfirst ai",
    ],
    "churn_dissatisfaction": [
        "stopped using answering service",
        "cancelled receptionist",
        "switched from answering service",
        "not worth it receptionist",
        "disappointed AI receptionist",
        "went back to voicemail",
        "AI receptionist problem",
        "terrible answering service",
        "waste of money receptionist",
        "sounds robotic AI",
        "customers complain automated",
        "fired answering service",
        "AI receptionist complaint",
    ],
    "pricing_willingness": [
        "how much pay receptionist",
        "worth it AI receptionist",
        "budget receptionist phone",
        "per minute flat rate receptionist",
        "pricing AI receptionist",
        "too expensive answering service",
    ],
}

# ──────────────────────────────────────────────────────────────────────
# Competitor keywords for tagging
# ──────────────────────────────────────────────────────────────────────

COMPETITORS = {
    "Smith.ai": ["smith.ai", "smithai", "smith ai"],
    "Ruby Receptionist": ["ruby receptionist", "ruby receptionists", "ruby.com"],
    "My AI Front Desk": ["my ai front desk", "myaifrontdesk", "ai front desk"],
    "Dialzara": ["dialzara"],
    "Synthflow": ["synthflow"],
    "Goodcall": ["goodcall"],
    "Frontdesk AI": ["frontdesk ai", "frontdesk.ai"],
    "Abby Connect": ["abby connect"],
    "Answering Agent": ["answering agent", "answeringagent"],
    "Rosie": ["rosie ai", "rosie.ai"],
    "CallBird AI": ["callbird"],
    "Upfirst": ["upfirst"],
    "Jobber": ["jobber ai receptionist", "jobber phone"],
    "Wing Assistant": ["wing assistant", "wingassistant"],
    "TrueLark": ["truelark"],
    "Quo/OpenPhone": ["openphone", "quo phone", "sona ai"],
    "Central AI": ["trycentral", "central ai receptionist"],
}

# ──────────────────────────────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────────────────────────────

def make_request(url, retries=MAX_RETRIES):
    """Make an HTTP request with retries and rate limiting."""
    for attempt in range(retries):
        try:
            req = Request(url)
            req.add_header("User-Agent", USER_AGENT)
            with urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))
            time.sleep(REQUEST_DELAY)
            return data
        except HTTPError as e:
            if e.code == 429:  # Rate limited
                wait = (attempt + 1) * 5
                print(f"  Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            elif e.code == 403:
                print(f"  403 Forbidden for {url} — skipping")
                return None
            elif e.code == 404:
                print(f"  404 Not Found — skipping")
                return None
            else:
                print(f"  HTTP {e.code} on attempt {attempt+1}/{retries}")
                time.sleep(2)
        except (URLError, TimeoutError) as e:
            print(f"  Connection error on attempt {attempt+1}/{retries}: {e}")
            time.sleep(2)
        except json.JSONDecodeError:
            print(f"  JSON decode error on attempt {attempt+1}/{retries}")
            time.sleep(2)
    return None


def search_subreddit(subreddit, query, sort="relevance", time_filter="all", limit=25):
    """Search a specific subreddit for a query."""
    params = urlencode({
        "q": query,
        "restrict_sr": "1" if subreddit else "0",
        "sort": sort,
        "t": time_filter,
        "limit": str(limit),
        "type": "link",
    })
    if subreddit:
        url = f"https://www.reddit.com/r/{subreddit}/search.json?{params}"
    else:
        url = f"https://www.reddit.com/search.json?{params}"
    return make_request(url)


def get_post_comments(permalink, limit=50):
    """Get comments for a specific post."""
    url = f"https://www.reddit.com{permalink}.json?limit={limit}&sort=top"
    return make_request(url)


def extract_post_data(post_data):
    """Extract relevant fields from a Reddit post."""
    d = post_data.get("data", {})
    created_utc = d.get("created_utc", 0)
    post_date = datetime.fromtimestamp(created_utc, tz=timezone.utc).strftime("%Y-%m-%d") if created_utc else ""

    return {
        "post_id": d.get("id", ""),
        "subreddit": d.get("subreddit", ""),
        "title": d.get("title", ""),
        "selftext": d.get("selftext", "")[:2000],  # Truncate long posts
        "author": d.get("author", ""),
        "score": d.get("score", 0),
        "num_comments": d.get("num_comments", 0),
        "created_utc": created_utc,
        "post_date": post_date,
        "permalink": d.get("permalink", ""),
        "url": f"https://www.reddit.com{d.get('permalink', '')}",
        "is_self": d.get("is_self", True),
    }


def extract_comments(comment_data, depth=0, max_depth=3):
    """Recursively extract comments from a comment tree."""
    comments = []
    if not isinstance(comment_data, dict):
        return comments

    kind = comment_data.get("kind", "")
    data = comment_data.get("data", {})

    if kind == "t1":  # Comment
        created_utc = data.get("created_utc", 0)
        comment_date = datetime.fromtimestamp(created_utc, tz=timezone.utc).strftime("%Y-%m-%d") if created_utc else ""

        comments.append({
            "comment_id": data.get("id", ""),
            "author": data.get("author", ""),
            "body": data.get("body", "")[:2000],
            "score": data.get("score", 0),
            "created_utc": created_utc,
            "comment_date": comment_date,
            "depth": depth,
            "parent_id": data.get("parent_id", ""),
        })

        # Get replies
        replies = data.get("replies", "")
        if isinstance(replies, dict) and depth < max_depth:
            children = replies.get("data", {}).get("children", [])
            for child in children:
                comments.extend(extract_comments(child, depth + 1, max_depth))

    elif kind == "Listing":
        children = data.get("children", [])
        for child in children:
            comments.extend(extract_comments(child, depth, max_depth))

    return comments


def detect_competitors(text):
    """Detect competitor mentions in text."""
    text_lower = text.lower()
    found = []
    for competitor, keywords in COMPETITORS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                found.append(competitor)
                break
    return found


def detect_bucket(text):
    """Detect which research bucket a post/comment falls into."""
    text_lower = text.lower()
    buckets = []

    churn_keywords = ["stopped using", "cancelled", "cancel", "switched from", "not worth",
                      "disappointed", "went back", "terrible", "horrible", "waste of money",
                      "doesn't work", "sounds robotic", "sounds fake", "complaint", "complain",
                      "fired", "dropped"]
    needs_keywords = ["need", "looking for", "recommend", "wish", "want", "help with",
                      "missed calls", "after hours", "can't answer", "overwhelmed",
                      "voicemail", "front desk"]
    pricing_keywords = ["how much", "cost", "pricing", "expensive", "cheap", "budget",
                        "per minute", "flat rate", "worth it", "price"]

    for kw in churn_keywords:
        if kw in text_lower:
            buckets.append("churn")
            break
    for kw in needs_keywords:
        if kw in text_lower:
            buckets.append("need")
            break
    for kw in pricing_keywords:
        if kw in text_lower:
            buckets.append("pricing")
            break

    if not buckets:
        buckets.append("general")

    return buckets


def is_relevant(text):
    """Check if text is relevant to AI receptionist / answering service research."""
    text_lower = text.lower()
    relevance_keywords = [
        "receptionist", "answering service", "answering machine", "phone answer",
        "ai phone", "virtual receptionist", "call handling", "call answering",
        "missed call", "after hours", "voicemail", "front desk", "phone system",
        "inbound call", "ai voice", "automated answer", "live answer",
        "phone agent", "call center", "phone support", "customer call",
    ]
    # Also check competitor names
    for competitor, keywords in COMPETITORS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                return True

    for kw in relevance_keywords:
        if kw in text_lower:
            return True
    return False


# ──────────────────────────────────────────────────────────────────────
# Main scraping logic
# ──────────────────────────────────────────────────────────────────────

def run_scraper():
    """Main scraper execution."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_posts = {}  # Deduplicate by post_id
    all_comments = {}  # Store comments keyed by post_id

    total_queries = sum(len(v) for v in QUERIES.values())
    total_searches = total_queries * (len(PRIMARY_SUBREDDITS) + (1 if GLOBAL_SEARCH else 0))

    print(f"=" * 60)
    print(f"AI Receptionist Reddit Research Scraper")
    print(f"=" * 60)
    print(f"Subreddits: {len(PRIMARY_SUBREDDITS)}")
    print(f"Query buckets: {len(QUERIES)}")
    print(f"Total queries: {total_queries}")
    print(f"Estimated searches: {total_searches}")
    print(f"Est. time: ~{total_searches * REQUEST_DELAY / 60:.0f} minutes")
    print(f"Output: {OUTPUT_DIR}")
    print(f"=" * 60)

    search_count = 0

    for bucket_name, queries in QUERIES.items():
        print(f"\n{'─' * 40}")
        print(f"Bucket: {bucket_name}")
        print(f"{'─' * 40}")

        for query in queries:
            # Search globally first
            if GLOBAL_SEARCH:
                search_count += 1
                print(f"\n[{search_count}/{total_searches}] Global: '{query}'")
                result = search_subreddit(None, query, limit=50)
                if result and "data" in result:
                    children = result["data"].get("children", [])
                    new_count = 0
                    for child in children:
                        post = extract_post_data(child)
                        if post["post_id"] and post["post_id"] not in all_posts:
                            combined_text = f"{post['title']} {post['selftext']}"
                            if is_relevant(combined_text):
                                post["search_query"] = query
                                post["search_bucket"] = bucket_name
                                post["competitors_mentioned"] = detect_competitors(combined_text)
                                post["insight_buckets"] = detect_bucket(combined_text)
                                all_posts[post["post_id"]] = post
                                new_count += 1
                    print(f"  Found {len(children)} posts, {new_count} new & relevant")

            # Search each subreddit
            for subreddit in PRIMARY_SUBREDDITS:
                search_count += 1
                print(f"[{search_count}/{total_searches}] r/{subreddit}: '{query}'")
                result = search_subreddit(subreddit, query, limit=25)
                if result and "data" in result:
                    children = result["data"].get("children", [])
                    new_count = 0
                    for child in children:
                        post = extract_post_data(child)
                        if post["post_id"] and post["post_id"] not in all_posts:
                            combined_text = f"{post['title']} {post['selftext']}"
                            if is_relevant(combined_text):
                                post["search_query"] = query
                                post["search_bucket"] = bucket_name
                                post["competitors_mentioned"] = detect_competitors(combined_text)
                                post["insight_buckets"] = detect_bucket(combined_text)
                                all_posts[post["post_id"]] = post
                                new_count += 1
                    if children:
                        print(f"  Found {len(children)} posts, {new_count} new & relevant")

    print(f"\n{'=' * 60}")
    print(f"Search phase complete. {len(all_posts)} unique relevant posts found.")
    print(f"{'=' * 60}")

    # Save intermediate results
    with open(RAW_JSON_FILE, "w") as f:
        json.dump(list(all_posts.values()), f, indent=2)
    print(f"Saved raw posts to {RAW_JSON_FILE}")

    # Phase 2: Collect comments for top posts (sorted by engagement)
    sorted_posts = sorted(all_posts.values(), key=lambda p: p["num_comments"] + p["score"], reverse=True)
    top_posts = sorted_posts[:150]  # Get comments for top 150 posts

    print(f"\nCollecting comments for top {len(top_posts)} posts...")

    for i, post in enumerate(top_posts):
        print(f"[{i+1}/{len(top_posts)}] Comments for: {post['title'][:60]}...")
        comment_data = get_post_comments(post["permalink"])
        if comment_data and len(comment_data) > 1:
            comments = extract_comments(comment_data[1])
            # Filter for relevant comments
            relevant_comments = []
            for c in comments:
                if c["body"] and len(c["body"]) > 20:
                    c["post_id"] = post["post_id"]
                    c["post_title"] = post["title"]
                    c["subreddit"] = post["subreddit"]
                    c["competitors_mentioned"] = detect_competitors(c["body"])
                    c["insight_buckets"] = detect_bucket(c["body"])
                    relevant_comments.append(c)
            all_comments[post["post_id"]] = relevant_comments
            print(f"  Got {len(relevant_comments)} comments")

    # Save comments
    flat_comments = []
    for post_id, comments in all_comments.items():
        flat_comments.extend(comments)

    with open(RAW_COMMENTS_FILE, "w") as f:
        json.dump(flat_comments, f, indent=2)
    print(f"Saved {len(flat_comments)} comments to {RAW_COMMENTS_FILE}")

    # Phase 3: Create combined CSV
    print(f"\nCreating combined CSV...")

    csv_rows = []

    # Add posts
    for post in all_posts.values():
        csv_rows.append({
            "type": "post",
            "id": post["post_id"],
            "subreddit": post["subreddit"],
            "date": post["post_date"],
            "author": post["author"],
            "title": post["title"],
            "text": post["selftext"][:500],
            "score": post["score"],
            "num_comments": post["num_comments"],
            "url": post["url"],
            "search_bucket": post["search_bucket"],
            "search_query": post["search_query"],
            "competitors": ", ".join(post["competitors_mentioned"]),
            "insight_buckets": ", ".join(post["insight_buckets"]),
        })

    # Add comments
    for comment in flat_comments:
        csv_rows.append({
            "type": "comment",
            "id": comment["comment_id"],
            "subreddit": comment.get("subreddit", ""),
            "date": comment["comment_date"],
            "author": comment["author"],
            "title": comment.get("post_title", ""),
            "text": comment["body"][:500],
            "score": comment["score"],
            "num_comments": 0,
            "url": "",
            "search_bucket": "",
            "search_query": "",
            "competitors": ", ".join(comment.get("competitors_mentioned", [])),
            "insight_buckets": ", ".join(comment.get("insight_buckets", [])),
        })

    # Write CSV
    if csv_rows:
        fieldnames = csv_rows[0].keys()
        with open(COMBINED_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_rows)
        print(f"Saved {len(csv_rows)} rows to {COMBINED_CSV}")

    # Phase 4: Generate collection summary
    print(f"\nGenerating summary...")

    # Stats
    subreddits_found = set(p["subreddit"] for p in all_posts.values())
    competitors_found = {}
    churn_posts = []

    for post in all_posts.values():
        for comp in post["competitors_mentioned"]:
            competitors_found[comp] = competitors_found.get(comp, 0) + 1
        if "churn" in post["insight_buckets"]:
            churn_posts.append(post)

    for comment in flat_comments:
        for comp in comment.get("competitors_mentioned", []):
            competitors_found[comp] = competitors_found.get(comp, 0) + 1

    sorted_competitors = sorted(competitors_found.items(), key=lambda x: x[1], reverse=True)

    # Date range
    dates = [p["post_date"] for p in all_posts.values() if p["post_date"]]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    summary = f"""# Reddit Scraper — Collection Summary

**Run Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Collection Stats

| Metric | Count |
|---|---|
| Unique relevant posts | {len(all_posts)} |
| Comments collected | {len(flat_comments)} |
| Total data points | {len(csv_rows)} |
| Subreddits represented | {len(subreddits_found)} |
| Date range | {date_range} |
| Churn-related posts | {len(churn_posts)} |

## Subreddits Represented

{', '.join(f'r/{s}' for s in sorted(subreddits_found))}

## Competitor Mentions

| Competitor | Mentions |
|---|---|
"""
    for comp, count in sorted_competitors:
        summary += f"| {comp} | {count} |\n"

    summary += f"""
## Posts by Search Bucket

| Bucket | Posts |
|---|---|
"""
    bucket_counts = {}
    for post in all_posts.values():
        b = post["search_bucket"]
        bucket_counts[b] = bucket_counts.get(b, 0) + 1
    for bucket, count in sorted(bucket_counts.items(), key=lambda x: x[1], reverse=True):
        summary += f"| {bucket} | {count} |\n"

    summary += f"""
## Top Posts by Engagement

"""
    for i, post in enumerate(sorted_posts[:20]):
        summary += f"{i+1}. [{post['title'][:80]}]({post['url']}) — r/{post['subreddit']} | Score: {post['score']} | Comments: {post['num_comments']}\n"

    summary += f"""
## Churn-Related Posts (Sample)

"""
    for post in churn_posts[:15]:
        summary += f"- [{post['title'][:80]}]({post['url']}) — r/{post['subreddit']}\n"

    summary += """
## Files Generated

- `raw_posts.json` — Full post data
- `raw_comments.json` — Full comment data
- `all_insights.csv` — Combined, tagged dataset for spreadsheet analysis
- `collection_summary.md` — This file
"""

    with open(SUMMARY_FILE, "w") as f:
        f.write(summary)
    print(f"Saved summary to {SUMMARY_FILE}")

    print(f"\n{'=' * 60}")
    print(f"SCRAPING COMPLETE")
    print(f"{'=' * 60}")
    print(f"Posts: {len(all_posts)}")
    print(f"Comments: {len(flat_comments)}")
    print(f"Total data points: {len(csv_rows)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    run_scraper()
