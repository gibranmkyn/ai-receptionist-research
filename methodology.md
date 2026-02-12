# Research Methodology — AI Receptionist Churn & Conversion Analysis

## Research Objective

Identify and document **external, evidence-based reasons** why users churn from AI receptionist products and why prospects fail to convert — grounded in real user verbatim quotes, not assumptions.

**Deliverable:** A curated set of verbatim quotes from real users, organized by churn reason and conversion blocker, with source links for verification.

---

## 1. Data Sources

We collected data from two independent sources to triangulate findings and reduce platform bias.

### Source A: Reddit (via Arctic Shift API)

| Parameter | Detail |
|---|---|
| **API** | Arctic Shift (`arctic-shift.photon-reddit.com`) — a free, public Reddit archive |
| **Why not Reddit API?** | Reddit's official API has strict rate limits and requires app approval. Arctic Shift provides the same data without credentials and no bot-detection risk |
| **Date range** | January 2023 — February 2026 (3 years) |
| **Subreddits searched** | 20 subreddits across SMB, professional services, trades, and tech communities |
| **Search queries** | 62 queries across 10 research buckets (see Section 2) |
| **Total API searches** | 1,984 (posts + comments) |
| **Content types** | Post titles + bodies, comment bodies |

**Subreddits covered:**
- **SMB/Entrepreneurship:** r/smallbusiness, r/Entrepreneur, r/freelance, r/startups, r/SaaS
- **Professional services:** r/lawfirm, r/dentistry, r/realtors, r/bookkeeping, r/consulting, r/agency
- **Trades:** r/HVAC, r/Plumbing, r/Electricians
- **Marketing/Sales:** r/sales, r/digital_marketing, r/marketing
- **Tech/Telecom:** r/VoIP, r/msp, r/legaltech

**Note on comment search limitations:** Arctic Shift does not support comment body search on very active subreddits (returns HTTP 422). For 8 large subreddits (r/smallbusiness, r/Entrepreneur, r/freelance, r/sales, r/SaaS, r/digital_marketing, r/marketing, r/startups), we searched post titles only. For the remaining 12 smaller subreddits, both post titles and comment bodies were searched.

### Source B: Trustpilot Reviews

| Parameter | Detail |
|---|---|
| **Platform** | Trustpilot (trustpilot.com) |
| **Why Trustpilot?** | G2 and Capterra block automated access (403). Trustpilot exposes structured review data via its Next.js `__NEXT_DATA__` payload |
| **Competitors scraped** | 9 direct competitors + Wing Assistant (Central's parent company) |
| **Pages per competitor** | Up to 6 (3 default pages + 1-star, 2-star, 3-star filtered pages) |
| **Review deduplication** | By review text (exact match) |

**Competitors covered:**

| Competitor | Reviews Collected | Negative (1-2★) |
|---|---|---|
| AnswerConnect | 105 | 25 |
| Ruby Receptionist | 102 | 24 |
| PATLive | 88 | 15 |
| Smith.ai | 73 | 22 |
| Wing Assistant (Central) | 45 | 6 |
| Abby Connect | 20 | 3 |
| Dialzara | 14 | 0 |
| My AI Front Desk | 8 | 0 |
| Goodcall | 2 | 1 |
| **Total** | **457** | **96** |

Each review includes a direct link to the original Trustpilot review page for verification.

---

## 2. Research Buckets

Queries and classification were organized around two CPO deliverables:

### Churn Reasons (why users leave)

| Bucket | Description | Example queries |
|---|---|---|
| `churn_billing` | Pricing surprises, overcharges, hidden fees | "answering service bill", "receptionist overcharged", "answering service hidden fees" |
| `churn_voice_quality` | AI sounds robotic, customers notice | "AI receptionist robotic", "answering service sounds fake" |
| `churn_cant_handle` | AI gives wrong answers, loses leads | "AI receptionist wrong answer", "answering service lost lead" |
| `churn_switched` | Explicitly switched to another provider | "switched answering service", "left ruby receptionist" |
| `churn_general` | General dissatisfaction | "answering service terrible", "waste of money receptionist" |

### Conversion Blockers (why prospects never start)

| Bucket | Description | Example queries |
|---|---|---|
| `blocker_trust` | Don't trust AI with their customers | "don't trust AI phone", "customers won't accept AI" |
| `blocker_not_ready` | Don't feel the need yet | "voicemail good enough", "too small for receptionist" |
| `blocker_tried_rejected` | Tried a product, decided against it | "tried AI receptionist", "AI receptionist demo bad" |

### Supporting Buckets

| Bucket | Description |
|---|---|
| `competitor_experience` | Direct reviews/experiences with named competitors |
| `pricing` | Pricing model discussions (per-minute vs flat rate, ROI, budget) |
| `positive` | What competitors do well (contrast data) |

---

## 3. Data Cleaning Pipeline

Raw scraped data contains significant noise (off-topic comments, generic mentions, low-quality posts). We applied a three-layer heuristic cascade to filter for high-quality, relevant quotes.

### Layer 1: Hard Filters (deterministic, zero cost)

| Filter | Threshold | Rationale |
|---|---|---|
| **Minimum text length** | 100 characters | Short comments ("yeah I use Ruby") carry no insight |
| **Minimum Reddit score** | ≥ 2 upvotes | Community validation — at least one other person found this valuable |
| **Deleted/removed content** | Excluded | No usable text |
| **Fuzzy deduplication** | 80% text similarity | Same person or copypasta across threads; keeps higher-scored version |

**Trustpilot reviews bypass the score filter** — all star ratings are valuable since they represent deliberate review submissions.

### Layer 2: Domain Relevance (regex-based, zero cost)

Each surviving item must match **both**:

1. **At least one domain term** — confirms the quote is about receptionists/answering services:
   - Generic: `receptionist`, `answering service`, `call answering`, `virtual receptionist`, `AI phone`, `auto attendant`, `missed call`
   - Competitor names: `smith.ai`, `ruby receptionist`, `patlive`, `dialzara`, `goodcall`, etc.

2. **At least one experience marker** — confirms the quote contains a first-person experience, not just a passing mention:
   - Pronouns: `I`, `we`, `my`, `our`
   - Actions: `tried`, `used`, `switched`, `cancelled`, `paying`
   - Evaluations: `recommend`, `worth`, `regret`, `frustrating`, `disappointing`

**Trustpilot reviews bypass this layer** — they are inherently domain-relevant (posted on a competitor's review page).

### Layer 3: LLM Classification (Claude)

Each surviving quote is classified by Claude for:

| Field | Values |
|---|---|
| `relevant` | true/false — final relevance check |
| `pain_point` | One-sentence summary of the pain point |
| `category` | Mapped to research bucket (churn_billing, blocker_trust, etc.) |
| `user_type` | business owner, employee, prospect, consultant, vendor, unknown |
| `product_mentioned` | Specific product name if any |
| `quote_quality` | 1-5 scale (see below) |
| `presentation_ready` | true/false — suitable for CPO deck |

**Quote quality scale:**

| Score | Criteria |
|---|---|
| 1 | Tangential mention, no real insight |
| 2 | Relevant but vague |
| 3 | Clear experience with some insight |
| 4 | Specific pain point with detail |
| 5 | Money quote — specific, emotional, representative, directly citable |

---

## 4. Data Flow Summary

```
┌─────────────────────────────────────────────────────────┐
│                    RAW COLLECTION                        │
├─────────────────────────────────────────────────────────┤
│  Reddit: 1,984 API searches → 9 posts + 856 comments    │
│  Trustpilot: 10 competitors × 6 pages → 457 reviews     │
│                                                         │
│  Total raw items: 1,322                                  │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              LAYER 1: Hard Filters                       │
│  - Length ≥ 100 chars              (-76 short)           │
│  - Reddit score ≥ 2               (-439 low score)      │
│  - Not deleted/removed             (-0)                  │
│  - Fuzzy dedup (80% similarity)    (-1 duplicate)        │
│                                                         │
│  Surviving: 806 (61% of raw)                             │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│           LAYER 2: Domain Relevance                      │
│  - Must mention receptionist/answering service/competitor│
│    (-257 no domain terms)                                │
│  - Must contain first-person experience marker           │
│    (-21 no experience markers)                           │
│                                                         │
│  Surviving: 528 (40% of raw)                             │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│         LAYER 3: LLM Classification (Claude)             │
│  - Final relevance check           (-150 irrelevant)     │
│  - Pain point extraction                                 │
│  - Category assignment                                   │
│  - Quality scoring (1-5)                                 │
│  - Presentation-ready flagging                           │
│                                                         │
│  Surviving: 378 (29% of raw)                             │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   FINAL OUTPUT                           │
│  378 classified quotes                                   │
│  123 presentation-ready (quality 4-5)                    │
│  Every quote linked to original source                   │
│  Structured JSON for further analysis                    │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Verification & Trustworthiness

### Every quote is traceable
- **Reddit quotes** link to the original Reddit post or comment (e.g., `reddit.com/r/lawfirm/comments/...`)
- **Trustpilot quotes** link to the individual review page (e.g., `trustpilot.com/reviews/{id}`)
- Anyone can click through and verify the quote in its original context

### Two independent sources reduce bias
- Reddit captures **organic discussions** among business owners (unprompted, peer-to-peer)
- Trustpilot captures **deliberate reviews** from actual customers (prompted, product-specific)
- Findings that appear in both sources are higher confidence

### Known limitations

| Limitation | Mitigation |
|---|---|
| **Reddit sampling bias** — Reddit users skew tech-savvy and younger | Trustpilot provides a broader demographic; we searched industry-specific subreddits (r/lawfirm, r/dentistry, r/HVAC) to capture non-tech users |
| **Survivorship bias** — We only hear from people who speak up | Acknowledged; silent churners are not captured. This data represents the *vocal* segment |
| **Astroturfing risk** — Some reviews may be fake (competitors, employees) | Trustpilot has verified review badges; Reddit comments with high scores are community-validated |
| **Temporal bias** — Older experiences may not reflect current product state | Date-filtered to 2023-2026; each quote includes its date for context |
| **No internal data contrast** — External-only research | This is intentional — the goal is external evidence to complement internal analytics |
| **Arctic Shift comment search gaps** — 8 large subreddits had post-only search | Mitigated by searching 12 smaller subreddits with both posts and comments |

---

## 6. Tools & Reproducibility

| Component | Tool |
|---|---|
| Reddit data collection | `arctic_shift_scraper.py` — Arctic Shift API |
| Review data collection | `review_site_scraper.py` — Trustpilot HTML parsing |
| Data cleaning | `clean_data.py` — 3-layer heuristic + LLM pipeline |
| LLM classification | Claude (Anthropic) |
| All scripts | Python 3, standard library only (no pip dependencies) |

All scripts are included in this repository and can be re-run to reproduce the dataset.

---

## 7. Final Output Summary

| Category | Quotes | Presentation-Ready |
|---|---|---|
| Churn: Can't Handle Calls | 61 | 32 |
| Churn: Billing/Pricing | 39 | 25 |
| Churn: Switched Away | 28 | 22 |
| Churn: General | 8 | 1 |
| Churn: Voice Quality | 1 | 1 |
| Blocker: Not Ready | 8 | 3 |
| Blocker: Trust | 5 | 2 |
| Blocker: Tried & Rejected | 5 | 3 |
| Competitor Experience | 60 | 13 |
| Positive (contrast) | 135 | 19 |
| Pricing | 16 | 2 |
| General | 12 | 0 |
| **Total** | **378** | **123** |

## 8. Quantitative Analyses

Three quantitative analyses were built on top of the classified quote dataset and raw Trustpilot reviews to answer specific CPO questions.

### Analysis 1: Churn Reason Pareto (Weighted)

| Component | Detail |
|---|---|
| **Question** | "Of all the reasons users churn, which ones matter most?" |
| **Data** | 137 churn quotes from `final_quotes.json` |
| **Method** | Weighted scoring: `quote_quality (1-5) × engagement_multiplier`. Reddit: engagement = `max(1, log₂(upvotes))`. Trustpilot: engagement = 1.0 |
| **Key finding** | 67% of weighted churn signal concentrated in 2 categories: Can't Handle Calls (40%) + Billing (28%) |
| **Script** | `analysis_pareto.py` |
| **Output** | `analysis/01_churn_pareto.md` |

### Analysis 2: Competitor Switching Matrix

| Component | Detail |
|---|---|
| **Question** | "When users leave, who are they leaving and where do they go?" |
| **Data** | 28 `churn_switched` quotes, manually coded for FROM→TO pairs |
| **Method** | Directed transition matrix. Net churn score = Inflows − Outflows per competitor |
| **Key finding** | Ruby is biggest net loser (−5). PATLive (+5) and Abby Connect (+4) are top gainers. Quality failures trigger 56% of switches |
| **Script** | `analysis_switching.py` |
| **Output** | `analysis/02_switching_matrix.md` |

### Analysis 3: Temporal Sentiment Shift

| Component | Detail |
|---|---|
| **Question** | "Are traditional services getting worse over time?" |
| **Data** | 457 Trustpilot reviews with dates and ratings across 9 competitors |
| **Method** | Half-year bucketing (H1/H2), average rating + % negative per window. Trough analysis comparing organic (pre-2024-H2) vs recent surge periods |
| **Key finding** | All 4 major competitors had devastating organic reviews 2021-2024 (avg 1.0-2.0 stars). Recent surges of 5-star reviews (2024-H2+) likely solicited. AI entrants at 100% 5-star |
| **Script** | `analysis_temporal.py` |
| **Output** | `analysis/03_temporal_sentiment.md` |

### Executive Summary

All three analyses are synthesized in `analysis/00_executive_summary.md` with the narrative: **What's broken → Who's losing → Why now → Central AI's opportunity.**

---

## 9. How to Read the Output

### Start here:
1. **`analysis/00_executive_summary.md`** — The CPO-ready executive summary tying all three analyses together
2. **`clean_quotes/final/presentation_ready.md`** — The 123 best quotes, organized by churn reason

### Quantitative analyses:
3. **`analysis/01_churn_pareto.md`** — What's breaking: Pareto distribution of churn reasons
4. **`analysis/02_switching_matrix.md`** — Who's losing: competitor switching flows
5. **`analysis/03_temporal_sentiment.md`** — Why now: sentiment trends over time

### By churn reason:
6. **`clean_quotes/final/churn_cant_handle.md`** — 61 quotes: agents gave wrong answers, lost leads
7. **`clean_quotes/final/churn_billing.md`** — 39 quotes: hidden fees, minute inflation, billing traps
8. **`clean_quotes/final/churn_switched.md`** — 28 quotes: explicitly left one service for another
9. **`clean_quotes/final/blocker_trust.md`** — 5 quotes: "my clients won't talk to AI"
10. **`clean_quotes/final/blocker_not_ready.md`** — 8 quotes: "not ready yet"

### For deeper exploration:
11. **`clean_quotes/final/competitor_experience.md`** — 60 detailed competitor experiences
12. **`review_data/quotes/negative_reviews.md`** — All 96 negative Trustpilot reviews (raw)
13. **`reddit_data/quotes/all_quotes.md`** — All Reddit quotes (pre-cleaning)

### Raw data:
14. **`reddit_data/posts.jsonl`** / **`comments.jsonl`** — Raw Reddit data
15. **`review_data/raw/*.json`** — Raw Trustpilot review data per competitor
16. **`clean_quotes/final_quotes.json`** — All 378 classified quotes with LLM metadata
