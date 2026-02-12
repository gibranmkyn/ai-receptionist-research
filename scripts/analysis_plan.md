# Quantitative Analysis Plan — AI Receptionist Research

**Purpose:** Turn 378 classified quotes + 457 Trustpilot reviews into three CPO-ready quantitative slides.

---

## The Three Slides

| # | Analysis | CPO Question | Data Source |
|---|---|---|---|
| 1 | **Churn Reason Pareto** | "What's breaking?" | 137 churn quotes from `final_quotes.json` |
| 2 | **Competitor Switching Matrix** | "Who's losing, and where do they go?" | 28 switching quotes + pain point extraction |
| 3 | **Temporal Sentiment Shift** | "Why now?" | 457 Trustpilot reviews with dates + ratings |

Together they form a narrative: **what's broken → who's losing → why now is the time to win.**

---

## Analysis 1: Churn Reason Pareto (Weighted)

### What it answers
> "Of all the reasons users churn from receptionist products, which ones matter most — not just by count, but by severity and community validation?"

### Input
- `clean_quotes/final_quotes.json` — 378 quotes
- Filter to 5 churn categories: `churn_cant_handle` (61), `churn_billing` (39), `churn_switched` (28), `churn_general` (8), `churn_voice_quality` (1)
- Total churn quotes: **137**

### Methodology

**Weighted scoring** — raw count alone is misleading. A single devastating 5-star quality quote from a business owner with 20 upvotes carries more weight than five vague 2-quality mentions.

Each quote's weight = `quote_quality (1-5)` × `engagement_multiplier`

| Source | Engagement multiplier | Rationale |
|---|---|---|
| Reddit | `max(1, log₂(score))` | Upvotes = community validation. 20 upvotes → 4.3× multiplier |
| Trustpilot | 1.0 | All reviews are deliberate acts; no upvote signal |

**Aggregation:**
1. Sum weighted scores per churn category
2. Calculate % of total weighted score
3. Sort descending → Pareto distribution
4. Mark cumulative % to find the "vital few"

### Expected output
- Pareto table with raw count, weighted score, %, cumulative %
- ASCII bar chart
- Top 3 representative quotes per category (quality 4-5, presentation-ready)
- Key insight: "X% of all churn pain is concentrated in just Y categories"

---

## Analysis 2: Competitor Switching Matrix

### What it answers
> "When users leave a receptionist service, who are they leaving and where do they go? Which competitors are most vulnerable?"

### Input
- 28 quotes classified as `churn_switched` from `final_quotes.json`
- Full text analysis to extract FROM→TO pairs

### Methodology

**Transition extraction** — read each switching quote and extract:
- **FROM:** The product/service they left
- **TO:** The product/service they switched to (or "cancelled", "in-house", "unknown")
- **Trigger:** Primary switching reason

Many quotes only mention one side (e.g., "I cancelled Ruby" with no TO, or "We went with PATLive" with no FROM). These are captured as:
- FROM X → Unknown
- Unknown → TO Y

**Matrix construction:**
- Rows = FROM (product left)
- Columns = TO (product chosen)
- Cells = count of transitions
- Margins = total outflows (row sum) and total inflows (column sum)

**Net churn score** = Inflows − Outflows per competitor
- Positive = net gainer (attracting churners)
- Negative = net loser (losing customers)

### Expected output
- Transition matrix table
- Net churn score ranking
- Top switching triggers per "FROM" competitor
- Supporting quotes for each major transition
- "Where to win" callout: which competitors' customers are most accessible

---

## Analysis 3: Temporal Sentiment Shift

### What it answers
> "Are traditional receptionist services getting worse over time? Is there a sentiment shift as AI alternatives emerge?"

### Input
- `review_data/raw/*.json` — 457 Trustpilot reviews with date, rating, competitor
- Focus on 4 major competitors with 70+ reviews: AnswerConnect (105), Ruby (102), PATLive (88), Smith.ai (73)
- Context: AI competitors (Dialzara, My AI Front Desk) for contrast

### Methodology

**Time windows:** Group reviews into half-year buckets (H1 = Jan-Jun, H2 = Jul-Dec), from 2019 through H1 2026.

**Per window, per competitor:**
- Average star rating
- Review count
- % negative (1-2 stars)

**Trend analysis:**
- Direction: is average rating trending up or down?
- Inflection: any visible shift around 2023-2024 (when AI receptionists emerged)?
- Comparison: traditional services vs AI-first entrants

**Caveats:**
- Small sample sizes per window (acknowledged explicitly)
- Trustpilot sampling bias (extremes overrepresented)
- AI competitors have too few reviews for statistical rigor — included as directional only

### Expected output
- Time series table per competitor
- ASCII trend chart (avg rating over time)
- Trend summary: improving / stable / declining per competitor
- "Why now" narrative: market context for Central AI's positioning
- Honest caveat section

---

## How They Connect

```
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│  Analysis 1: PARETO  │───▶│ Analysis 2: SWITCHING│───▶│ Analysis 3: TEMPORAL │
│                      │    │                      │    │                      │
│  "Can't Handle Calls"│    │  Ruby → In-house     │    │  Ruby: declining     │
│  is 45% of all churn │    │  Smith.ai → Ruby     │    │  since 2023          │
│  pain                │    │  AnswerConnect → ?    │    │  AI entrants: 100%   │
│                      │    │                      │    │  5-star (small n)    │
│  WHAT'S BROKEN       │    │  WHO'S LOSING        │    │  WHY NOW             │
└──────────────────────┘    └──────────────────────┘    └──────────────────────┘
```

**CPO narrative:** The shared-pool receptionist model is fundamentally broken — agents can't handle calls properly (Analysis 1). The biggest losers are Ruby and Smith.ai, whose customers actively switch away (Analysis 2). And this is accelerating — traditional service satisfaction is declining while AI alternatives are emerging with perfect early scores (Analysis 3). **Central AI is positioned to capture this transition.**

---

## Scripts & Outputs

| Script | Output |
|---|---|
| `analysis_pareto.py` | `analysis/01_churn_pareto.md` |
| `analysis_switching.py` | `analysis/02_switching_matrix.md` |
| `analysis_temporal.py` | `analysis/03_temporal_sentiment.md` |
| (manual) | `analysis/00_executive_summary.md` |

All scripts: Python 3, standard library only, read from existing JSON files.
