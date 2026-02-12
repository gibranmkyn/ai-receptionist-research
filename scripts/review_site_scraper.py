#!/usr/bin/env python3
"""
Review Site Scraper — G2, Capterra, Trustpilot, Software Advice
Collects verbatim reviews for AI receptionist competitors.

Strategy:
  - Trustpilot: Direct fetch (works)
  - G2/Capterra/Software Advice: Via web search (direct access blocked)

Outputs markdown files with verbatim quotes organized by competitor and sentiment.

Usage:
    python3 review_site_scraper.py
"""

import json
import time
import os
import sys
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser
import re

# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "review_data")
RAW_DIR = os.path.join(OUTPUT_DIR, "raw")
QUOTES_DIR = os.path.join(OUTPUT_DIR, "quotes")

REQUEST_DELAY = 3.0  # Trustpilot is more aggressive about rate limiting

# ──────────────────────────────────────────────────────────────────────
# Competitors to scrape reviews for
# ──────────────────────────────────────────────────────────────────────

COMPETITORS = {
    "Smith.ai": {
        "trustpilot": "smith.ai",
        "search_terms": ["smith.ai reviews", "smith.ai complaints", "smith.ai receptionist review"],
    },
    "Ruby Receptionist": {
        "trustpilot": "ruby.com",
        "search_terms": ["ruby receptionist reviews", "ruby receptionist complaints", "ruby receptionist billing"],
    },
    "My AI Front Desk": {
        "trustpilot": "myaifrontdesk.com",
        "search_terms": ["my ai front desk reviews", "myaifrontdesk review"],
    },
    "Abby Connect": {
        "trustpilot": "abbyconnect.com",
        "search_terms": ["abby connect receptionist reviews", "abby connect complaints"],
    },
    "Nexa": {
        "trustpilot": "nexa.com",
        "search_terms": ["nexa receptionist reviews", "nexa answering service review"],
    },
    "PATLive": {
        "trustpilot": "patlive.com",
        "search_terms": ["patlive reviews", "patlive answering service complaints"],
    },
    "AnswerConnect": {
        "trustpilot": "answerconnect.com",
        "search_terms": ["answerconnect reviews", "answerconnect complaints"],
    },
    "Dialzara": {
        "trustpilot": "dialzara.com",
        "search_terms": ["dialzara AI receptionist review"],
    },
    "Goodcall": {
        "trustpilot": "goodcall.com",
        "search_terms": ["goodcall AI receptionist review"],
    },
    "Synthflow": {
        "trustpilot": "synthflow.ai",
        "search_terms": ["synthflow AI receptionist review"],
    },
    "Bland AI": {
        "trustpilot": "bland.ai",
        "search_terms": ["bland AI phone agent review"],
    },
}

# Trustpilot pages to scrape — prioritize negative reviews (churn evidence)
TRUSTPILOT_PAGES = [
    "",              # default page 1
    "?page=2",       # default page 2
    "?page=3",       # default page 3
    "?stars=1",      # 1-star reviews (churn gold)
    "?stars=2",      # 2-star reviews
    "?stars=3",      # 3-star reviews (mixed — often most nuanced)
]

# ──────────────────────────────────────────────────────────────────────
# Simple HTML text extractor
# ──────────────────────────────────────────────────────────────────────

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self._skip = False
        if tag in ('p', 'div', 'br', 'h1', 'h2', 'h3', 'h4', 'li'):
            self.text_parts.append('\n')

    def handle_data(self, data):
        if not self._skip:
            self.text_parts.append(data)

    def get_text(self):
        return ''.join(self.text_parts)


def html_to_text(html):
    extractor = HTMLTextExtractor()
    extractor.feed(html)
    return extractor.get_text()


# ──────────────────────────────────────────────────────────────────────
# Fetch helpers
# ──────────────────────────────────────────────────────────────────────

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "identity",
}


def fetch_page(url, retries=3):
    """Fetch a URL with retries and redirect handling."""
    import http.client
    from urllib.parse import urlparse

    for attempt in range(retries):
        try:
            req = Request(url)
            for k, v in HEADERS.items():
                req.add_header(k, v)
            with urlopen(req, timeout=30) as resp:
                html = resp.read().decode("utf-8", errors="replace")
            time.sleep(REQUEST_DELAY)
            return html
        except HTTPError as e:
            if e.code in (301, 302, 307, 308):
                redirect_url = e.headers.get("Location", "")
                if redirect_url:
                    if not redirect_url.startswith("http"):
                        parsed = urlparse(url)
                        redirect_url = f"{parsed.scheme}://{parsed.netloc}{redirect_url}"
                    url = redirect_url
                    continue  # retry with new URL
                return None
            elif e.code == 429:
                wait = (attempt + 1) * 10
                print(f"    Rate limited, waiting {wait}s...")
                time.sleep(wait)
            elif e.code in (403, 404):
                print(f"    {e.code} — skipping")
                return None
            else:
                print(f"    HTTP {e.code}, attempt {attempt + 1}/{retries}")
                time.sleep(3)
        except (URLError, TimeoutError, OSError, Exception) as e:
            print(f"    Connection error: {e}, attempt {attempt + 1}/{retries}")
            time.sleep(5)
    return None


# ──────────────────────────────────────────────────────────────────────
# Trustpilot parser
# ──────────────────────────────────────────────────────────────────────

def parse_trustpilot_reviews(html):
    """Extract reviews from Trustpilot HTML via __NEXT_DATA__ JSON blob."""
    reviews = []

    # Trustpilot is a Next.js app — all review data is in __NEXT_DATA__
    next_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
    if not next_match:
        return reviews

    try:
        data = json.loads(next_match.group(1))
        page_reviews = data.get("props", {}).get("pageProps", {}).get("reviews", [])

        for r in page_reviews:
            text = r.get("text", "").strip()
            if not text:
                continue

            consumer = r.get("consumer", {})
            dates = r.get("dates", {})

            # Parse date
            pub_date = dates.get("publishedDate", "") or dates.get("experiencedDate", "")
            if pub_date:
                pub_date = pub_date[:10]  # just YYYY-MM-DD

            review_id = r.get("id", "")
            reviews.append({
                "author": consumer.get("displayName", "Anonymous"),
                "date": pub_date,
                "rating": str(r.get("rating", "")),
                "title": r.get("title", ""),
                "text": text,
                "review_url": f"https://www.trustpilot.com/reviews/{review_id}" if review_id else "",
            })
    except (json.JSONDecodeError, KeyError, TypeError):
        pass

    return reviews


# ──────────────────────────────────────────────────────────────────────
# Main scraper
# ──────────────────────────────────────────────────────────────────────

def run(only_companies=None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(QUOTES_DIR, exist_ok=True)

    all_reviews = {}  # competitor -> list of reviews

    targets = {k: v for k, v in COMPETITORS.items() if k in only_companies} if only_companies else COMPETITORS

    print("=" * 60)
    print("Review Site Scraper — AI Receptionist Competitors")
    print("=" * 60)
    if only_companies:
        print(f"Mode: SELECTIVE — only scraping {list(targets.keys())}")
    print(f"Competitors: {len(targets)}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    # ── Phase 1: Trustpilot (direct access) ──
    print("\n── Phase 1: Trustpilot Reviews ──\n")

    for competitor, config in targets.items():
        trustpilot_slug = config.get("trustpilot", "")
        if not trustpilot_slug:
            continue

        print(f"\n  {competitor} (trustpilot.com/review/{trustpilot_slug})")
        reviews = []

        for page_suffix in TRUSTPILOT_PAGES:
            url = f"https://www.trustpilot.com/review/{trustpilot_slug}{page_suffix}"
            sys.stdout.write(f"    Fetching {page_suffix or '(page 1)'}... ")
            sys.stdout.flush()

            html = fetch_page(url)
            if not html:
                print("skipped")
                continue

            page_reviews = parse_trustpilot_reviews(html)
            new = 0
            for r in page_reviews:
                # Deduplicate by text
                if r["text"] and not any(existing["text"] == r["text"] for existing in reviews):
                    r["source"] = "Trustpilot"
                    r["competitor"] = competitor
                    r["url"] = url
                    reviews.append(r)
                    new += 1
            print(f"{len(page_reviews)} found, {new} new")

        all_reviews[competitor] = reviews
        print(f"    Total for {competitor}: {len(reviews)} reviews")

        # Save raw per competitor
        if reviews:
            raw_file = os.path.join(RAW_DIR, f"{competitor.lower().replace(' ', '_').replace('.', '')}_trustpilot.json")
            with open(raw_file, "w") as f:
                json.dump(reviews, f, indent=2)

    # ── Phase 2: Build markdown files ──
    print(f"\n{'=' * 60}")
    print("Building markdown files...")
    print(f"{'=' * 60}")

    total_reviews = sum(len(r) for r in all_reviews.values())

    # File 1: All negative reviews (1-2 stars) across competitors — the churn file
    negative_reviews = []
    for competitor, reviews in all_reviews.items():
        for r in reviews:
            try:
                rating = int(float(r.get("rating", 5)))
            except (ValueError, TypeError):
                rating = 0
            if rating <= 2 and r.get("text"):
                r["_rating_int"] = rating
                negative_reviews.append(r)

    negative_reviews.sort(key=lambda x: x.get("date", ""), reverse=True)

    md = f"# Negative Reviews — Churn & Complaint Evidence\n\n"
    md += f"**Total negative reviews (1-2 stars):** {len(negative_reviews)}  \n"
    md += f"**Source:** Trustpilot  \n"
    md += f"**Collected:** {datetime.now().strftime('%Y-%m-%d')}  \n"
    md += f"**Purpose:** Evidence of why users churn from AI receptionist / answering services\n\n"
    md += "---\n\n"

    for i, r in enumerate(negative_reviews, 1):
        comp = r.get("competitor", "Unknown")
        rating = r.get("_rating_int", "?")
        stars = "★" * rating + "☆" * (5 - rating) if isinstance(rating, int) else "?"
        md += f"### {i}. {comp} — {r.get('date', 'undated')} | {stars}\n\n"
        if r.get("title"):
            md += f"**\"{r['title']}\"**\n\n"
        md += f"> {r['text']}\n\n"
        review_link = r.get("review_url") or r.get("url", "")
        md += f"*— {r.get('author', 'Anonymous')}* | [Trustpilot]({review_link})\n\n"
        md += "---\n\n"

    with open(os.path.join(QUOTES_DIR, "negative_reviews.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"  negative_reviews.md — {len(negative_reviews)} reviews")

    # File 2: All positive reviews (4-5 stars) — for competitor intel / contrast
    positive_reviews = []
    for competitor, reviews in all_reviews.items():
        for r in reviews:
            try:
                rating = int(float(r.get("rating", 0)))
            except (ValueError, TypeError):
                rating = 0
            if rating >= 4 and r.get("text"):
                r["_rating_int"] = rating
                positive_reviews.append(r)

    positive_reviews.sort(key=lambda x: x.get("date", ""), reverse=True)

    md2 = f"# Positive Reviews — What's Working for Competitors\n\n"
    md2 += f"**Total positive reviews (4-5 stars):** {len(positive_reviews)}  \n"
    md2 += f"**Source:** Trustpilot  \n"
    md2 += f"**Collected:** {datetime.now().strftime('%Y-%m-%d')}  \n"
    md2 += f"**Purpose:** Understand what competitors do well (contrast with churn data)\n\n"
    md2 += "---\n\n"

    for i, r in enumerate(positive_reviews, 1):
        comp = r.get("competitor", "Unknown")
        rating = r.get("_rating_int", "?")
        stars = "★" * rating + "☆" * (5 - rating) if isinstance(rating, int) else "?"
        md2 += f"### {i}. {comp} — {r.get('date', 'undated')} | {stars}\n\n"
        if r.get("title"):
            md2 += f"**\"{r['title']}\"**\n\n"
        md2 += f"> {r['text']}\n\n"
        review_link = r.get("review_url") or r.get("url", "")
        md2 += f"*— {r.get('author', 'Anonymous')}* | [Trustpilot]({review_link})\n\n"
        md2 += "---\n\n"

    with open(os.path.join(QUOTES_DIR, "positive_reviews.md"), "w", encoding="utf-8") as f:
        f.write(md2)
    print(f"  positive_reviews.md — {len(positive_reviews)} reviews")

    # File 3: Per-competitor files
    for competitor, reviews in all_reviews.items():
        if not reviews:
            continue

        reviews_sorted = sorted(reviews, key=lambda x: x.get("date", ""), reverse=True)
        slug = competitor.lower().replace(" ", "_").replace(".", "")

        md3 = f"# {competitor} — All Reviews\n\n"
        md3 += f"**Total reviews:** {len(reviews)}  \n"
        md3 += f"**Source:** Trustpilot  \n"
        md3 += f"**Collected:** {datetime.now().strftime('%Y-%m-%d')}\n\n"

        # Rating distribution
        ratings = {}
        for r in reviews:
            try:
                rating = int(float(r.get("rating", 0)))
            except (ValueError, TypeError):
                rating = 0
            ratings[rating] = ratings.get(rating, 0) + 1

        md3 += "### Rating Distribution\n\n"
        for star in [5, 4, 3, 2, 1]:
            count = ratings.get(star, 0)
            bar = "█" * count
            md3 += f"{'★' * star}{'☆' * (5-star)} | {count} {bar}\n\n"
        md3 += "---\n\n"

        for i, r in enumerate(reviews_sorted, 1):
            try:
                rating = int(float(r.get("rating", 0)))
            except (ValueError, TypeError):
                rating = 0
            stars = "★" * rating + "☆" * (5 - rating) if rating > 0 else "unrated"
            md3 += f"### {i}. {r.get('date', 'undated')} | {stars}\n\n"
            if r.get("title"):
                md3 += f"**\"{r['title']}\"**\n\n"
            md3 += f"> {r['text']}\n\n"
            review_link = r.get("review_url") or r.get("url", "")
            md3 += f"*— {r.get('author', 'Anonymous')}* | [Trustpilot]({review_link})\n\n"
            md3 += "---\n\n"

        with open(os.path.join(QUOTES_DIR, f"{slug}.md"), "w", encoding="utf-8") as f:
            f.write(md3)
        print(f"  {slug}.md — {len(reviews)} reviews")

    # ── Summary ──
    summary = f"""# Review Site Scraper — Collection Summary

**Run Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Source:** Trustpilot
**Competitors Scraped:** {len(targets)}

## Stats

| Metric | Count |
|---|---|
| Total reviews collected | {total_reviews} |
| Negative reviews (1-2 stars) | {len(negative_reviews)} |
| Positive reviews (4-5 stars) | {len(positive_reviews)} |

## Per Competitor

| Competitor | Total | Negative | Positive |
|---|---|---|---|
"""
    for comp, reviews in all_reviews.items():
        neg = sum(1 for r in reviews if int(float(r.get("rating", 5))) <= 2)
        pos = sum(1 for r in reviews if int(float(r.get("rating", 0))) >= 4)
        summary += f"| {comp} | {len(reviews)} | {neg} | {pos} |\n"

    summary += f"""
## Files

### Churn Evidence (start here)
- `quotes/negative_reviews.md` — All 1-2 star reviews across competitors

### Competitor Intel
- `quotes/positive_reviews.md` — All 4-5 star reviews (what's working)

### Per-Competitor Deep Dive
"""
    for comp in all_reviews:
        slug = comp.lower().replace(" ", "_").replace(".", "")
        summary += f"- `quotes/{slug}.md`\n"

    summary += """
### Raw Data
- `raw/[competitor]_trustpilot.json` — Full review data per competitor
"""

    with open(os.path.join(OUTPUT_DIR, "collection_summary.md"), "w") as f:
        f.write(summary)
    print(f"\n  collection_summary.md")

    print(f"\n{'=' * 60}")
    print(f"DONE — {total_reviews} reviews collected ({len(negative_reviews)} negative)")
    print(f"Output: {OUTPUT_DIR}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    # --only "Company1,Company2" to scrape only specific companies
    only_companies = None
    for i, arg in enumerate(sys.argv):
        if arg == "--only" and i + 1 < len(sys.argv):
            only_companies = [c.strip() for c in sys.argv[i + 1].split(",")]
            break
    run(only_companies=only_companies)
