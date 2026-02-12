# AI Receptionist Research Plan
## External Evidence: Why Users Churn & Why Prospects Don't Convert

**For:** CPO presentation
**Objective:** Build a grounded, evidence-based case for why AI receptionist users churn and why prospects don't convert — backed by real verbatim quotes from SMB owners.

**Data Sources:**
1. **Reddit** (via Arctic Shift API) — unfiltered discussions from SMB owners
2. **Trustpilot** — structured reviews with star ratings for 9 competitors

**What this is NOT:** This is not an opinion piece or competitor feature comparison. This is raw voice-of-customer data from people who have actually used (and left) these products, or considered them and walked away.

---

## The Two Questions This Research Answers

### 1. Why do users STOP using AI receptionists?
Churn reasons — real quotes from people who cancelled, switched, or downgraded.

### 2. Why do potential users NEVER START?
Conversion blockers — real quotes from people who considered AI receptionists but decided against them.

---

## Method

### Data Source
**Arctic Shift API** — a free Reddit archive with full historical search across all of Reddit. No API credentials, no bot detection, no scraping risk.

### Why Reddit?
- SMB owners discuss tools candidly in subreddits (r/smallbusiness, r/lawfirm, r/HVAC, etc.)
- Unfiltered — not curated testimonials or review site marketing
- Discussion threads capture back-and-forth that reveals nuance (not just star ratings)
- Competitor mentions are organic — people name specific products and say why they left

### Script
`arctic_shift_scraper.py` — searches 20 subreddits across 60+ queries, collects both posts and comments, auto-tags by churn reason / conversion blocker, outputs to markdown.

---

## Search Strategy

### Subreddits (20)

**General SMB**
r/smallbusiness, r/Entrepreneur, r/freelance, r/consulting, r/agency, r/sales, r/SaaS, r/startups

**Vertical-Specific (where AI receptionists are most adopted)**
r/lawfirm, r/legaltech, r/dentistry, r/realtors, r/HVAC, r/Plumbing, r/Electricians

**Tools & Tech**
r/digital_marketing, r/marketing, r/bookkeeping, r/VoIP, r/msp

### Query Buckets (focused on the two deliverables)

**Churn — Billing & Pricing (6 queries)**
answering service bill, receptionist overcharged, per minute receptionist, answering service expensive, ruby receptionist bill, answering service hidden fees

**Churn — Voice Quality (5 queries)**
AI receptionist robotic, answering service sounds fake, AI phone sounds bad, customers hate AI phone, robotic answering service

**Churn — Can't Handle Calls (6 queries)**
AI receptionist wrong answer, answering service lost lead, AI receptionist confused, answering service mistake, receptionist dropped call, AI loop phone

**Churn — Switched Away (6 queries)**
switched answering service, cancelled receptionist, stopped using answering, left ruby receptionist, quit answering service, dropped smith.ai

**Churn — General Dissatisfaction (7 queries)**
answering service terrible, receptionist not worth, AI receptionist problem, worst answering service, receptionist complaint, answering service disappointed, waste of money receptionist

**Blocker — Trust & Risk (6 queries)**
don't trust AI phone, worried AI receptionist, AI receptionist risk, customers won't accept AI, afraid AI answering, AI phone unprofessional

**Blocker — Not Ready (5 queries)**
not ready AI receptionist, voicemail good enough, don't need receptionist, receptionist overkill, too small for receptionist

**Blocker — Tried & Rejected (5 queries)**
tried AI receptionist, tested answering service, AI receptionist demo bad, receptionist didn't work, gave up answering service

**Competitor Experience (10 queries)**
smith.ai review, ruby receptionist review, my ai front desk review, dialzara review, goodcall review, frontdesk ai review, abby connect review, answering service recommendation, virtual receptionist best, AI receptionist which one

**Pricing Discussions (6 queries)**
receptionist pricing, answering service cost, how much receptionist, per minute vs flat rate, receptionist budget, AI receptionist worth it

### Total: 62 queries × 20 subreddits × 2 (posts + comments) = ~2,480 API calls

---

## Auto-Tagging

Every collected quote is automatically classified into one or more of these buckets:

### Churn Reasons
| Bucket | What It Catches |
|---|---|
| `churn_billing` | Overcharged, bill shock, per-minute surprises, hidden fees, charged for spam calls |
| `churn_voice_quality` | Sounds robotic, callers hang up, customers complain about voice, obvious it's AI |
| `churn_cant_handle` | Wrong answers, lost leads, confused callers, AI loops, can't transfer |
| `churn_switched` | Switched from X to Y, cancelled, went back to voicemail/human |
| `churn_general` | Terrible, worst, waste of money, disappointed, wouldn't recommend |

### Conversion Blockers
| Bucket | What It Catches |
|---|---|
| `blocker_trust` | Don't trust AI with customers, worried about professionalism, scared to try |
| `blocker_not_ready` | Don't need it, too small, voicemail is fine, not enough call volume |
| `blocker_tried_rejected` | Tried a demo/trial, didn't work out, gave up |

### Supporting Context
| Bucket | What It Catches |
|---|---|
| `pricing` | Cost discussions, per-minute vs flat-rate, ROI, budget |
| `positive` | What's working well (for competitor comparison) |
| `general` | Relevant but doesn't match a specific bucket |

### Competitor Detection (19 products)
Smith.ai, Ruby, My AI Front Desk, Dialzara, Synthflow, Goodcall, Frontdesk AI, Abby Connect, Rosie, CallBird AI, Upfirst, Jobber, TrueLark, OpenPhone, Wing Assistant, Nexa, PATLive, AnswerConnect, Vonage

---

## Output

All output goes to `reddit_data/`:

### Raw Data
- `posts.json` — every post with full metadata
- `comments.json` — every comment with full metadata

### Verbatim Quote Files (one .md per bucket)
Each file is a standalone, readable document with quotes sorted by engagement:

```
### 1. r/lawfirm — 2025-06-12 | 47pts | Mentions: Ruby Receptionist

**We cancelled Ruby after 8 months**

> The per-minute billing was killing us. We went from paying $280/mo to
> $890/mo in our busy season. When we called to ask about it they just
> said "well you used more minutes." No warning, no cap, nothing...

*— u/soloattorney* | [post](https://reddit.com/...)
```

### Files Generated
- `quotes/churn_billing.md`
- `quotes/churn_voice_quality.md`
- `quotes/churn_cant_handle.md`
- `quotes/churn_switched.md`
- `quotes/churn_general.md`
- `quotes/blocker_trust.md`
- `quotes/blocker_not_ready.md`
- `quotes/blocker_tried_rejected.md`
- `quotes/pricing.md`
- `quotes/positive.md`
- `quotes/general.md`
- `quotes/all_quotes.md` — every unique quote, sorted by engagement
- `collection_summary.md` — stats, competitor mentions, top posts

---

## How to Use This for the CPO Presentation

1. **Run the scraper** — `python3 arctic_shift_scraper.py` (~45 min)
2. **Read the churn files first** — `churn_billing.md`, `churn_voice_quality.md`, `churn_cant_handle.md`
3. **Read the blocker files** — `blocker_trust.md`, `blocker_tried_rejected.md`
4. **Pull the strongest quotes** — the ones with high engagement (score) and specific details (dollars, timelines, named competitors)
5. **Present as:** "Based on [X] real user accounts from Reddit, here are the top reasons users churn from AI receptionists, and the top reasons prospects don't convert — with verbatim quotes."

The analysis and synthesis comes AFTER reading the raw quotes. Don't jump to conclusions before seeing the data.

---

## Data Source 2: Trustpilot Reviews

### Script
`review_site_scraper.py` — scrapes Trustpilot reviews for 9 competitors, including star-filtered pages to maximize negative review coverage.

### Competitors Scraped

| Competitor | Trustpilot Slug | Type |
|---|---|---|
| Smith.ai | smith.ai | AI + Human Hybrid |
| Ruby Receptionist | ruby.com | Human-Led |
| My AI Front Desk | myaifrontdesk.com | Pure AI |
| Abby Connect | abbyconnect.com | Hybrid |
| Nexa | nexa.com | Human-Led |
| PATLive | patlive.com | Human-Led |
| AnswerConnect | answerconnect.com | Human-Led |
| Dialzara | dialzara.com | Pure AI |
| Goodcall | goodcall.com | Pure AI |

### Pages Per Competitor
- Default (most recent, 20 reviews)
- Page 2 & 3 (40 more reviews)
- 1-star filtered (all negative)
- 2-star filtered
- 3-star filtered (often most nuanced)

**Max per competitor: ~120 reviews. Total: ~1,000+ reviews across 9 competitors.**

### Output
All output goes to `review_data/`:

- `quotes/negative_reviews.md` — All 1-2 star reviews across competitors (churn evidence)
- `quotes/positive_reviews.md` — All 4-5 star reviews (what's working — for contrast)
- `quotes/[competitor].md` — Per-competitor deep dive with rating distribution
- `raw/[competitor]_trustpilot.json` — Full data per competitor
- `collection_summary.md` — Stats and overview

### Why Trustpilot Matters
- Structured "pros and cons" format — people explicitly state what they dislike
- Star ratings let you filter for churn signals (1-2 stars)
- Verified purchases reduce astroturfing risk
- Complements Reddit's unstructured discussions

---

## Execution

```bash
cd 07-ai-receptionist-research

# Step 1: Reddit data (~45 min)
python3 arctic_shift_scraper.py

# Step 2: Review site data (~15 min)
python3 review_site_scraper.py
```

Total run time: ~60 minutes. Output in `reddit_data/` and `review_data/`.

---

*Research for Central (trycentral.com) — AI-powered Business OS for SMBs.*
