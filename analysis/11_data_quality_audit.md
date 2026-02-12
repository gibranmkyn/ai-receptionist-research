# What This Analysis Can and Can't Tell You

Every dataset has blind spots. Here are ours, and why we think the conclusions still hold.

---

## The data is mostly Trustpilot

142 of 154 churn quotes come from Trustpilot. Only 12 from Reddit. Trustpilot skews negative — people who are angry enough to write a review. This means the *complaint types* are real (these problems genuinely happen), but the *frequency* might not match the overall market. We're seeing the loudest pain, not necessarily the most common.

## Some complaints are old

34 of 154 quotes are from before 2020. Does the ranking change if we only look at recent data? Slightly — Ruby and Smith.ai move up, AnswerConnect moves down. But the complaint *types* don't change. Call handling is still ~45%, billing is still ~33% whether you look at all dates or just post-2020.

| Rank | All Dates | Post-2020 Only |
|:---:|---|---|
| 1 | AnswerConnect (36) | Ruby Receptionist (29) |
| 2 | Ruby Receptionist (36) | Smith.ai (22) |
| 3 | PATLive (28) | PATLive (21) |
| 4 | Smith.ai (23) | AnswerConnect (17) |
| 5 | Synthflow (17) | Synthflow (17) |

## Reddit is all lawyers

All 12 Reddit churn quotes come from r/LawFirm. Six other subreddits we scraped produced zero churn quotes. The "legal dominates" finding partly reflects where we looked, not just where the pain is.

## Both classifiers are AI

Two independent LLMs, 92% agreement, kappa=0.91. Strong — but they might share blind spots. If both LLMs systematically misunderstand a type of complaint, we wouldn't catch it. We manually reviewed the 12 disagreements and are comfortable with the results, but it's worth noting.

## We only know why people leave

We collected 146 positive quotes too, but didn't analyze them. This analysis tells you what makes customers *leave*. It doesn't tell you whether Central AI's current customers face the same issues, or what makes satisfied customers stay.

## The mid-2024 review surge is weird

Every major competitor saw sudden spikes of 5-star reviews starting mid-2024. We split the data into "organic" (pre-surge) and "recent" (post-surge), but the cutoff is judgment-based, not scientific.

---

## Bottom line

The specific *reasons* people churn are robust. The exact *percentages* have uncertainty around them. The competitor *ranking* shifts a bit depending on time window. But the high-level story — call handling and billing drive ~80% of churn, and AI has a structural advantage on both — holds up across every cut of the data we tried.

*Sample: 154 churn quotes. Trustpilot: 142. Reddit: 12. Total collected: 409.*
