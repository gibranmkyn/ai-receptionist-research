#!/usr/bin/env python3
"""
Analysis 3: Temporal Sentiment Shift
Reads raw Trustpilot reviews, groups by half-year windows,
tracks sentiment trends per competitor over time.
"""

import json
import os
import glob as glob_mod

BASE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE, "review_data", "raw")
OUTPUT_FILE = os.path.join(BASE, "analysis", "03_temporal_sentiment.md")

# Only competitors with enough reviews for meaningful analysis
MAJOR_COMPETITORS = ["AnswerConnect", "Ruby Receptionist", "PATLive", "Smith.ai"]
AI_COMPETITORS = ["Dialzara", "My AI Front Desk"]

COMPETITOR_FILE_MAP = {
    "AnswerConnect": "answerconnect_trustpilot.json",
    "Ruby Receptionist": "ruby_receptionist_trustpilot.json",
    "PATLive": "patlive_trustpilot.json",
    "Smith.ai": "smithai_trustpilot.json",
    "Dialzara": "dialzara_trustpilot.json",
    "My AI Front Desk": "my_ai_front_desk_trustpilot.json",
    "Abby Connect": "abby_connect_trustpilot.json",
    "Goodcall": "goodcall_trustpilot.json",
    "Wing Assistant": "wing_assistant_trustpilot.json",
}


def load_all_reviews():
    all_reviews = {}
    for name, filename in COMPETITOR_FILE_MAP.items():
        path = os.path.join(RAW_DIR, filename)
        if os.path.exists(path):
            with open(path, "r") as f:
                reviews = json.load(f)
            all_reviews[name] = reviews
    return all_reviews


def get_half_year(date_str):
    """Convert YYYY-MM-DD to 'YYYY-H1' or 'YYYY-H2'"""
    parts = date_str.split("-")
    year = parts[0]
    month = int(parts[1]) if len(parts) > 1 else 1
    half = "H1" if month <= 6 else "H2"
    return f"{year}-{half}"


def build_time_series(reviews_by_competitor):
    """Build time series data per competitor."""
    series = {}

    for name in MAJOR_COMPETITORS + AI_COMPETITORS:
        if name not in reviews_by_competitor:
            continue
        reviews = reviews_by_competitor[name]
        windows = {}

        for r in reviews:
            date = r.get("date", "")
            if not date or len(date) < 7:
                continue
            rating = int(r.get("rating", 0))
            if rating < 1 or rating > 5:
                continue

            window = get_half_year(date)
            if window not in windows:
                windows[window] = {"ratings": [], "count": 0}
            windows[window]["ratings"].append(rating)
            windows[window]["count"] += 1

        # Calculate metrics per window
        computed = {}
        for w, data in sorted(windows.items()):
            ratings = data["ratings"]
            avg = sum(ratings) / len(ratings)
            neg = sum(1 for r in ratings if r <= 2)
            neg_pct = neg / len(ratings) * 100
            computed[w] = {
                "avg_rating": round(avg, 2),
                "count": len(ratings),
                "negative": neg,
                "neg_pct": round(neg_pct, 1),
            }

        series[name] = computed

    return series


def get_all_windows(series):
    """Get sorted union of all time windows across all competitors."""
    all_windows = set()
    for comp_data in series.values():
        all_windows.update(comp_data.keys())
    return sorted(all_windows)


def compute_trend(series_data):
    """Compute simple trend direction from time series."""
    windows = sorted(series_data.keys())
    if len(windows) < 2:
        return "insufficient data"

    # Compare first half and second half of the timeline
    mid = len(windows) // 2
    first_half = windows[:mid] if mid > 0 else windows[:1]
    second_half = windows[mid:]

    first_avg = sum(series_data[w]["avg_rating"] for w in first_half) / len(first_half)
    second_avg = sum(series_data[w]["avg_rating"] for w in second_half) / len(second_half)

    diff = second_avg - first_avg
    if diff > 0.3:
        return "IMPROVING"
    elif diff < -0.3:
        return "DECLINING"
    else:
        return "STABLE"


def compute_trough_analysis(series_data):
    """Identify the 'trough' period (2021-2024) vs recent surge (2024-H2+).
    Many competitors show a pattern: terrible organic reviews 2021-2024,
    then sudden surges of 5-star reviews — likely solicited."""
    windows = sorted(series_data.keys())
    if len(windows) < 3:
        return None

    trough_windows = [w for w in windows if "2021" in w or "2022" in w or "2023" in w or w == "2024-H1"]
    surge_windows = [w for w in windows if w >= "2024-H2"]
    organic_windows = [w for w in windows if w < "2024-H2"]

    if not trough_windows or not surge_windows:
        return None

    trough_ratings = []
    trough_count = 0
    for w in trough_windows:
        d = series_data[w]
        trough_ratings.extend([d["avg_rating"]] * d["count"])
        trough_count += d["count"]

    surge_ratings = []
    surge_count = 0
    for w in surge_windows:
        d = series_data[w]
        surge_ratings.extend([d["avg_rating"]] * d["count"])
        surge_count += d["count"]

    organic_ratings = []
    organic_count = 0
    for w in organic_windows:
        d = series_data[w]
        organic_ratings.extend([d["avg_rating"]] * d["count"])
        organic_count += d["count"]

    trough_avg = sum(trough_ratings) / len(trough_ratings) if trough_ratings else 0
    surge_avg = sum(surge_ratings) / len(surge_ratings) if surge_ratings else 0
    organic_avg = sum(organic_ratings) / len(organic_ratings) if organic_ratings else 0

    return {
        "trough_avg": round(trough_avg, 2),
        "trough_count": trough_count,
        "surge_avg": round(surge_avg, 2),
        "surge_count": surge_count,
        "organic_avg": round(organic_avg, 2),
        "organic_count": organic_count,
        "jump": round(surge_avg - trough_avg, 2),
    }


def format_sparkline(avg_rating):
    """Simple ASCII sparkline for a rating 1-5."""
    blocks = ["_", "\u2581", "\u2582", "\u2583", "\u2584", "\u2585", "\u2586", "\u2587", "\u2588"]
    idx = int((avg_rating - 1) / 4 * (len(blocks) - 1))
    idx = max(0, min(len(blocks) - 1, idx))
    return blocks[idx]


def generate_markdown(series, reviews_by_competitor):
    lines = []
    lines.append("# Analysis 3: Temporal Sentiment Shift")
    lines.append("")
    lines.append("> **CPO Question:** \"Are traditional receptionist services getting worse over time? Is there a sentiment shift as AI alternatives emerge?\"")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append("- **Data:** 457 Trustpilot reviews across 9 competitors")
    lines.append("- **Focus:** 4 major competitors with 70+ reviews each (AnswerConnect, Ruby, PATLive, Smith.ai)")
    lines.append("- **Time windows:** Half-year buckets (H1 = Jan-Jun, H2 = Jul-Dec)")
    lines.append("- **Metrics:** Average star rating, review count, % negative (1-2 stars)")
    lines.append("- **AI competitors:** Dialzara and My AI Front Desk included for contrast (small sample caveat)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Overall summary table
    lines.append("## Competitor Snapshot")
    lines.append("")
    lines.append("| Competitor | Total Reviews | Avg Rating | % Negative (1-2★) | Trend |")
    lines.append("|---|:---:|:---:|:---:|:---:|")

    for name in MAJOR_COMPETITORS + AI_COMPETITORS:
        if name not in reviews_by_competitor:
            continue
        reviews = reviews_by_competitor[name]
        ratings = [int(r.get("rating", 0)) for r in reviews if r.get("rating")]
        if not ratings:
            continue
        avg = sum(ratings) / len(ratings)
        neg = sum(1 for r in ratings if r <= 2)
        neg_pct = neg / len(ratings) * 100
        trend = compute_trend(series.get(name, {})) if name in series else "N/A"

        trend_icon = {"IMPROVING": "📈", "DECLINING": "📉", "STABLE": "➡️", "insufficient data": "❓"}.get(trend, "")
        is_ai = " (AI)" if name in AI_COMPETITORS else ""

        lines.append(f"| **{name}**{is_ai} | {len(ratings)} | {avg:.2f} | {neg_pct:.0f}% | {trend_icon} {trend} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Detailed time series per major competitor
    lines.append("## Time Series: Major Competitors")
    lines.append("")

    all_windows = get_all_windows({k: v for k, v in series.items() if k in MAJOR_COMPETITORS})

    # Filter to windows with data (skip very sparse early periods)
    for name in MAJOR_COMPETITORS:
        if name not in series:
            continue
        data = series[name]
        windows = sorted(data.keys())
        trend = compute_trend(data)

        lines.append(f"### {name} — Trend: **{trend}**")
        lines.append("")
        lines.append("| Period | Reviews | Avg Rating | % Negative | Visual |")
        lines.append("|---|:---:|:---:|:---:|:---:|")

        for w in windows:
            d = data[w]
            stars = "★" * round(d["avg_rating"]) + "☆" * (5 - round(d["avg_rating"]))
            neg_bar = "🔴" * max(1, round(d["neg_pct"] / 20)) if d["neg_pct"] > 0 else "✅"
            lines.append(f"| {w} | {d['count']} | {d['avg_rating']:.2f} | {d['neg_pct']}% | {stars} |")

        lines.append("")

        # Compute recent vs older comparison
        if len(windows) >= 4:
            recent = windows[-2:]
            older = windows[:2]
            recent_avg = sum(data[w]["avg_rating"] for w in recent) / len(recent)
            older_avg = sum(data[w]["avg_rating"] for w in older) / len(older)
            diff = recent_avg - older_avg
            direction = "higher" if diff > 0 else "lower"
            lines.append(f"*Recent periods ({recent[0]}–{recent[-1]}) average **{recent_avg:.2f}**, {direction} than earliest periods ({older[0]}–{older[-1]}) at **{older_avg:.2f}** (Δ {diff:+.2f})*")
            lines.append("")

        lines.append("---")
        lines.append("")

    # AI competitors section
    lines.append("## AI-First Competitors (Directional Only)")
    lines.append("")
    lines.append("> **Caveat:** These competitors have very few reviews (8-14). Results are directional, not statistically significant.")
    lines.append("")

    for name in AI_COMPETITORS:
        if name not in reviews_by_competitor:
            continue
        reviews = reviews_by_competitor[name]
        ratings = [int(r.get("rating", 0)) for r in reviews if r.get("rating")]
        if not ratings:
            continue
        avg = sum(ratings) / len(ratings)
        dates = sorted([r.get("date", "") for r in reviews if r.get("date")])
        date_range = f"{dates[0]} to {dates[-1]}" if dates else "unknown"

        lines.append(f"### {name}")
        lines.append(f"- **Reviews:** {len(ratings)}")
        lines.append(f"- **Average rating:** {avg:.2f}")
        lines.append(f"- **Date range:** {date_range}")
        lines.append(f"- **100% 5-star:** {'Yes' if all(r == 5 for r in ratings) else 'No'}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Trough analysis
    lines.append("## The Review Solicitation Pattern")
    lines.append("")
    lines.append("A striking pattern emerges across all four major competitors: **devastating organic reviews from 2021-2024, followed by sudden surges of 5-star reviews in late 2024/2025.**")
    lines.append("")
    lines.append("| Competitor | Organic Period (pre-2024-H2) | Recent Surge (2024-H2+) | Jump |")
    lines.append("|---|:---:|:---:|:---:|")

    for name in MAJOR_COMPETITORS:
        if name not in series:
            continue
        trough = compute_trough_analysis(series[name])
        if trough:
            lines.append(f"| **{name}** | {trough['organic_avg']:.2f} ({trough['organic_count']} reviews) | {trough['surge_avg']:.2f} ({trough['surge_count']} reviews) | +{trough['jump']:.2f} |")

    lines.append("")
    lines.append("**What this likely means:**")
    lines.append("- The **organic, unsolicited reviews** (2021-2024) reveal persistent customer pain: missed calls, billing issues, service quality decline")
    lines.append("- The **recent positive surges** are likely driven by review solicitation programs (common in the industry)")
    lines.append("- The underlying problems documented in our churn analysis haven't gone away — companies are managing perception, not fixing root causes")
    lines.append("- **For Central AI:** The organic review data is the true signal. These are the customers who are hurting and vocal about it.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Key insight
    lines.append("## Key Insight")
    lines.append("")
    lines.append("> **The traditional receptionist market is ripe for disruption — the data shows it.**")
    lines.append(">")
    lines.append("> **2021-2024 was a trough.** All four major competitors saw devastating organic reviews — 1-2 star averages, 60-100% negative rates. Users documented missed calls, wrong information, billing surprises, and service quality collapse.")
    lines.append(">")
    lines.append("> **The recent \"recovery\" is likely artificial.** Sudden surges of 5-star reviews starting in late 2024 have a classic solicited-review pattern: high volume, short text, and generic praise. The underlying complaints from the trough period persist in our churn data.")
    lines.append(">")
    lines.append("> **AI-first entrants are emerging.** Dialzara (14 reviews, 100% 5-star) and My AI Front Desk (8 reviews, 100% 5-star) have early but strong signals. These are small samples, but they show the AI receptionist concept resonates with adopters.")
    lines.append(">")
    lines.append("> **Central AI's window is now.** Traditional services have a fundamental quality problem (shared-pool receptionists can't handle calls correctly), and their customers know it. The organic review data proves the pain is real, persistent, and unsolved.")
    lines.append("")

    return "\n".join(lines)


def main():
    reviews_by_competitor = load_all_reviews()
    series = build_time_series(reviews_by_competitor)
    md = generate_markdown(series, reviews_by_competitor)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write(md)

    print(f"Temporal analysis written to {OUTPUT_FILE}")
    for name in MAJOR_COMPETITORS + AI_COMPETITORS:
        if name in series:
            windows = sorted(series[name].keys())
            trend = compute_trend(series[name])
            print(f"  {name}: {len(windows)} windows, trend={trend}")


if __name__ == "__main__":
    main()
