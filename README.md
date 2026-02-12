# Market Research: Virtual Receptionists in the US

Churn analysis of the US virtual receptionist / answering service market. 409 reviews scraped from Reddit and Trustpilot, 154 churn stories dual-coded into 11 categories, packaged into product strategy recommendations.

I did this as a Product Manager evaluating a market entry for an AI receptionist product. The research question was simple: **why do customers leave existing answering services, and what would make them switch?**

Instead of surveys or analyst reports, I scraped real customer reviews and used Claude to classify and analyze them at scale.

## How I Did It

### 1. Data Collection
Two Reddit scrapers (live API + Arctic Shift archive) covered 20 subreddits across SMB verticals — law, dental, HVAC, real estate, MSPs, etc. Search queries were organized into churn buckets (billing, voice quality, call handling, switching) and blocker buckets (trust, not ready, tried and rejected).

For Trustpilot, I scraped 11 company profiles and specifically targeted 1-2 star review pages for churn signal. The 9 competitors in the final analysis: Ruby Receptionist, Smith.ai, AnswerConnect, PATLive, Synthflow, Abby Connect, Dialzara, SAS, and Virtual HQ.

409 reviews total, spanning 2015–2026. Sample composition: 92% Trustpilot, 8% Reddit.

### 2. Cleaning
Three-pass pipeline before anything gets classified:
1. **Hard filters** — drop deleted posts, text under 100 characters, Reddit posts with score < 2, and fuzzy duplicates (0.8 similarity threshold)
2. **Domain relevance** — must mention an answering service/receptionist AND contain first-person experience markers ("I switched", "we cancelled", "cost us", etc.). Trustpilot reviews skip this check since they're inherently on-topic.
3. **LLM classification** — Claude (Sonnet 4.5) reads each surviving quote and extracts: category, competitor mentioned, pain point summary, quality score (1–5), dollar amounts, and a presentation-ready flag

### 3. Dual Coding
The 154 churn stories were the core sample. Two independent LLM coders classified each one against an 11-category taxonomy grouped into four themes:

| Group | Categories |
|---|---|
| **Call Handling** | "They don't follow my instructions", "They don't know my business", "They get the details wrong", "Calls go to the wrong place" |
| **Billing** | "Hidden charges on my bill", "I can't cancel", "Surprise charges I can't explain", "It costs too much" |
| **Service Reliability** | "They don't pick up", "It used to be good, then got worse" |
| **Industry Disillusionment** | "I've tried everyone, nobody works" |

Disagreements were adjudicated manually. Inter-rater reliability: **Cohen's kappa = 0.91**.

One limitation worth noting: both coders are AI, so they may share blind spots that two human coders wouldn't.

### 4. Weighted Analysis
Weight = quote quality (1–5) × engagement. For Reddit, engagement is log₂(upvotes) — so a 50-upvote post with a detailed switching story outweighs dozens of one-line Trustpilot reviews. Trustpilot reviews get a flat 1.0 engagement multiplier since there's no comparable signal.

### 5. Switching Direction Detection
For the 30 switching stories, I needed to figure out direction: did the reviewer leave Company X, or arrive at it? The script tries four strategies in order:
1. **Departure phrases** — "left Ruby", "cancelled Smith.ai", "ditched AnswerConnect"
2. **Arrival phrases** — "switched to PATLive", "went with Dialzara", "found Abby Connect"
3. **Sentiment balance** — count positive vs negative words near the company name
4. **Keyword fallback** — if all else ties, default to departure

### 6. Temporal Analysis
To test whether Trustpilot ratings are trustworthy, I split reviews at mid-2024 (July). Before that: organic reviews averaging 1.2–3.8 stars. After: sudden 5-star surges that doubled or tripled company scores. The cutoff is judgment-based, chosen by eyeballing where the pattern shifts.

### 7. Report Generation
All charts, tables, and the narrative document are generated programmatically. Every percentage and ranking is computed from the coded data, not hardcoded. The 72% legal vertical figure comes with a caveat: Reddit churn data skews heavily toward r/LawFirm, so that number partly reflects where the data came from.

## Key Findings

- **76% of churn** is call handling (43%) + billing (33%) — both solvable by AI + flat-rate pricing
- **Ruby Receptionist** loses the most customers. **Smith.ai** over-indexes on billing complaints.
- Organic Trustpilot ratings average **1.2–3.8 stars**. The high composite scores are inflated by mid-2024 5-star review surges.
- AI-native competitors (Synthflow) fix script adherence but introduce billing and reliability churn
- **72% legal vertical** — natural beachhead market (with the Reddit caveat above)

## Outputs

| File | Description |
|---|---|
| [`Virtual Receptionist Churn Analysis.pdf`](Virtual%20Receptionist%20Churn%20Analysis.pdf) | **Final deliverable** — 18-slide strategy deck (built with NotebookLM) |
| [`Deep Dive Report.pdf`](Deep%20Dive%20Report.pdf) | Supporting narrative report with charts and recommendations |
| [`churn_quotes_categorized.md`](churn_quotes_categorized.md) | All 154 churn quotes by category |
| [`methodology.md`](methodology.md) | Methodology and data quality notes |

## Folder Structure

```
.
├── Deep Dive Report.docx/.pdf    Narrative report
├── Virtual Receptionist...pdf    Strategy deck
├── churn_quotes_categorized.md   154 quotes by category
├── methodology.md                Research methodology
│
├── analysis/                     15 working analysis memos
├── data/                         Coded data, charts, raw sources
│   ├── charts/                   10 chart PNGs
│   ├── codebook_k9.md            11-category taxonomy
│   ├── coder_a_k9.json           Coder A assignments
│   ├── coder_b_k9.json           Coder B assignments
│   ├── final_quotes.json         409 quotes with metadata
│   └── raw/                      Reddit + Trustpilot source data
└── scripts/                      Scrapers, analysis, report generation
```

## Tools

- **Claude Code** — classification, dual coding, analysis, report writing
- **NotebookLM** (Google) — strategy deck creation
- **Python** — scrapers, data pipeline, chart generation (matplotlib, python-docx)
- **Reddit API / Arctic Shift** + **Trustpilot** — data sources
