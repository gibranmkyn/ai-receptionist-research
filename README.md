# AI Receptionist Market Research

Churn analysis of 9 answering service competitors based on 409 reviews (Reddit + Trustpilot, 2015–2026). 154 churn stories were dual-coded into 11 failure categories with inter-rater reliability κ = 0.91.

## Deliverables

| File | What it is |
|---|---|
| `Virtual Receptionist Churn Analysis.pdf` | 18-slide MBB-style strategy deck |
| `Deep Dive Report.docx` / `.pdf` | Full narrative report with charts and recommendations |
| `churn_quotes_categorized.md` | All 154 churn quotes organized by customer-centric category |

## Key Findings

- **76% of churn** maps to two problem groups: call handling (43%) and billing (33%) — both structurally solvable by AI + flat-rate pricing.
- **Ruby Receptionist** has the worst net customer flow. **Smith.ai** over-indexes on billing complaints.
- Organic Trustpilot ratings average **1.2–3.8 stars** before mid-2024 review surges inflated scores.
- AI-native competitors (Synthflow) eliminate script adherence issues but introduce new billing and reliability churn.

## Folder Structure

```
├── audit/                     CPO audit trail
│   ├── methodology.md         Data collection + coding methodology
│   ├── codebook_k9.md         11-category taxonomy definitions
│   ├── coder_a_k9.json        Coder A assignments + reasoning
│   ├── coder_b_k9.json        Coder B assignments + reasoning
│   ├── final_quotes.json      409 quotes with full metadata
│   ├── charts/                10 chart PNGs used in the report
│   └── analysis_notes/        15 numbered analysis memos
├── scripts/                   Reproducible pipeline
│   ├── build_narrative.py     Generates charts, docx, and categorized list
│   ├── *_scraper.py           Reddit + Trustpilot data collection
│   └── analysis_*.py          Intermediate analysis scripts
└── raw_data/                  Source data
    ├── reddit_data/           Reddit posts + comments
    ├── review_data/           Trustpilot reviews (raw JSON)
    └── clean_quotes/          Cleaned + classified quotes
```

## Methodology

- **Sources:** Reddit (r/LawFirm, r/smallbusiness, r/msp, etc.) + Trustpilot reviews for 9 competitors
- **Coding:** 11-category taxonomy (K9 codebook), dual-coded by two independent LLM coders, adjudicated on disagreements
- **Reliability:** Cohen's κ = 0.91 (near-perfect agreement)
- **Weighting:** Quote quality (1–5) × community engagement (upvotes, comments)

See `audit/methodology.md` for full details.
