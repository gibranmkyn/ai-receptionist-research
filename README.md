# Market Research: Virtual Receptionist Industry

Churn analysis of the virtual receptionist / answering service market. 409 reviews scraped from Reddit and Trustpilot, 154 churn stories dual-coded into 11 categories, packaged into product strategy recommendations.

I did this as a Product Manager evaluating a market entry for an AI receptionist product. The research question was simple: **why do customers leave existing answering services, and what would make them switch?**

Instead of surveys or analyst reports, I scraped real customer reviews and used Claude to classify and analyze them at scale.

## How I Did It

### 1. Data Collection
Scraped reviews from two sources:
- **Reddit** (r/LawFirm, r/smallbusiness, r/msp, etc.) — longer switching stories, upvote-validated
- **Trustpilot** — structured reviews for 9 competitors (Ruby, Smith.ai, AnswerConnect, PATLive, Synthflow, etc.)

409 reviews total, spanning 2015–2026.

### 2. Classification
Used Claude to classify each review (churn, positive, pricing, blocker, etc.) and extract structured fields: competitor mentioned, pain point, quote quality, dollar amounts, switching direction.

### 3. Dual Coding
The 154 churn stories were the core sample. To make sure the categorization wasn't just one model's interpretation, I ran two independent LLM coders against an 11-category taxonomy and adjudicated disagreements.

Inter-rater reliability: **Cohen's kappa = 0.91** (near-perfect agreement).

### 4. Weighted Analysis
Weighted each quote by detail level (1–5) and community engagement (upvotes). A Reddit post with 50 upvotes and a detailed switching story counts more than a one-line Trustpilot review.

### 5. Report Generation
All charts, tables, and the narrative document are generated programmatically from the coded data. Every percentage and ranking is computed, not hardcoded.

## Key Findings

- **76% of churn** is call handling (43%) + billing (33%) — both solvable by AI + flat-rate pricing
- **Ruby Receptionist** loses the most customers. **Smith.ai** over-indexes on billing complaints.
- Organic Trustpilot ratings average **1.2–3.8 stars**. The high composite scores are inflated by mid-2024 5-star review surges.
- AI-native competitors (Synthflow) fix script adherence but introduce billing and reliability churn
- **72% legal vertical** — natural beachhead market

## Outputs

| File | Description |
|---|---|
| [`Virtual Receptionist Churn Analysis.pdf`](Virtual%20Receptionist%20Churn%20Analysis.pdf) | 18-slide strategy deck |
| [`Deep Dive Report.pdf`](Deep%20Dive%20Report.pdf) | Narrative report with charts and recommendations |
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
