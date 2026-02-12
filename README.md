# AI-Powered Market Research: Virtual Receptionist Industry

A competitive churn analysis of the virtual receptionist / answering service market, conducted by a Product Manager using AI as a force multiplier for market research. The entire pipeline — from data collection to coded analysis to final deliverables — was built and executed by one person using AI tools, producing research that would typically require a team of analysts and weeks of manual coding.

## Context

As a PM evaluating a new market entry for an AI receptionist product, I needed to answer a fundamental question: **why do customers leave existing answering services, and what would it take to win them over?**

Traditional approaches — commissioning a research agency, running surveys, buying analyst reports — are slow, expensive, and often too high-level to drive specific product decisions. Instead, I went directly to the customers' own words: hundreds of reviews on Reddit and Trustpilot where people describe exactly what went wrong, how much they paid, and where they went next.

I used AI (Claude) to turn this unstructured text into a rigorous, quantified analysis — applying the same dual-coding methodology used in academic qualitative research, but at a fraction of the time and cost.

## How I Did It

The research followed a five-step pipeline, designed so that each step is reproducible and auditable. Every script, dataset, and intermediate output is in this repo.

### 1. Data Collection
I built scrapers to pull reviews from two sources with very different signals:
- **Reddit** (r/LawFirm, r/smallbusiness, r/msp, etc.) — longer stories, community-validated via upvotes
- **Trustpilot** — structured reviews for 9 specific competitors (Ruby, Smith.ai, AnswerConnect, PATLive, Synthflow, etc.)

This gave me 409 reviews spanning 2015–2026. Reddit stories tend to be richer (switching narratives, dollar amounts, multi-paragraph rants), while Trustpilot provides volume and competitor-specific data.

### 2. AI-Assisted Classification
I used LLMs to classify each review into categories (churn, positive, pricing, blocker, etc.) and extract structured metadata: competitor mentioned, pain point, quote quality, dollar amounts, and switching direction. This turned unstructured text into a queryable dataset.

### 3. Dual Coding for Reliability
The 154 churn stories were the core analytical sample. To ensure the categorization was rigorous and not just one model's interpretation, I ran two independent LLM coders (Coder A and Coder B) against an 11-category taxonomy, then adjudicated disagreements.

**Inter-rater reliability: Cohen's kappa = 0.91** (near-perfect agreement). This is the same reliability standard used in academic qualitative research — applied here with AI coders instead of human research assistants.

### 4. Weighted Analysis
Not all reviews carry equal signal. I weighted each quote by:
- **Quote quality** (1–5): How specific, detailed, and actionable is the complaint?
- **Community engagement**: A Reddit post with 50 upvotes carries more weight than a one-line Trustpilot review

This prevents high-volume, low-quality reviews from drowning out the detailed switching stories that contain the real insight.

### 5. Report Generation
Charts, tables, and the final narrative document are all generated programmatically from the coded data. Nothing is hardcoded — every percentage, ranking, and comparison is computed dynamically, so the analysis updates if the underlying data changes.

## Key Findings

- **76% of churn** maps to two problem groups: call handling (43%) and billing (33%) — both structurally solvable by AI + flat-rate pricing
- **Ruby Receptionist** has the worst net customer flow; **Smith.ai** over-indexes on billing complaints
- Organic Trustpilot ratings average **1.2–3.8 stars** — mid-2024 5-star surges are solicited reviews, not improved service
- AI-native competitors (Synthflow) eliminate script adherence issues but introduce billing and reliability churn
- **Legal vertical** represents 72% of the sample — the natural beachhead market

## Outputs

| File | Description |
|---|---|
| [`Virtual Receptionist Churn Analysis.pdf`](Virtual%20Receptionist%20Churn%20Analysis.pdf) | 18-slide strategy deck |
| [`Deep Dive Report.pdf`](Deep%20Dive%20Report.pdf) | Full narrative report with charts and recommendations |
| [`churn_quotes_categorized.md`](churn_quotes_categorized.md) | All 154 churn quotes organized by customer-voiced category |
| [`methodology.md`](methodology.md) | Detailed methodology and data quality notes |

## Folder Structure

```
.
├── Deep Dive Report.docx/.pdf    Final narrative report
├── Virtual Receptionist...pdf    Strategy deck
├── churn_quotes_categorized.md   154 quotes by category
├── methodology.md                How the research was conducted
│
├── analysis/                     Working analysis notes
│   ├── 03_temporal_sentiment.md  Rating trends over time
│   ├── 07_competitor_profiles.md Per-competitor breakdowns
│   ├── 08_bimodality_analysis.md Review distribution analysis
│   ├── 12_ai_native_competitors.md  Synthflow / AI-native landscape
│   └── ...                       15 analysis memos total
│
├── data/                         All data assets
│   ├── charts/                   10 chart PNGs (generated)
│   ├── codebook_k9.md            11-category taxonomy
│   ├── coder_a_k9.json           Coder A assignments
│   ├── coder_b_k9.json           Coder B assignments
│   ├── final_quotes.json         409 quotes with metadata
│   └── raw/                      Source data
│       ├── reddit_data/          Reddit posts + comments
│       ├── review_data/          Trustpilot reviews (JSON)
│       └── clean_quotes/         Cleaned + classified quotes
│
└── scripts/                      Reproducible pipeline
    ├── build_narrative.py        Generates charts + docx + categorized list
    ├── *_scraper.py              Reddit + Trustpilot scrapers
    └── analysis_*.py             Analysis scripts
```

## Why This Approach

As a PM, I don't have a research team or a six-week timeline. But I do have access to AI tools and the ability to write code. This project demonstrates that a single PM can:

- **Collect primary data** at scale from public sources (409 reviews, 9 competitors)
- **Apply academic-grade methodology** (dual coding, inter-rater reliability) using AI instead of human research assistants
- **Produce quantified, defensible insights** — not vibes, not summaries, but weighted analysis with confidence levels
- **Generate publication-ready deliverables** (strategy deck, narrative report, categorized database) programmatically

The total cost was essentially zero (public data + AI API calls). The output is comparable to what a research agency would charge five figures for.

## Tools Used

- **Claude Code** (Anthropic) — AI-assisted coding, review classification, dual coding, report writing
- **Python** — data collection, analysis, and report generation
- **matplotlib** — all charts generated programmatically
- **python-docx** — Word document generation
- **Reddit API / Arctic Shift** — Reddit data collection
- **Trustpilot scraping** — review data collection
