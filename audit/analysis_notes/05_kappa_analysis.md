# Can You Trust These Numbers?

Before we go further — how confident should you be in this analysis?

We had two independent AI classifiers read every single churn quote and assign it to one of 11 categories. Neither could see the other's work. Then we checked how often they agreed.

**They agreed on 142 out of 154 quotes. That's a Cohen's kappa of 0.91.**

In academic terms, anything above 0.81 is "almost perfect agreement." We're well above that. The 95% confidence interval is 0.86 to 0.96 — even the worst case is still in the "almost perfect" range.

The 12 disagreements are all borderline cases where reasonable people would split:

- Is "the receptionist didn't follow the script" a **script failure** or **inauthenticity**? (2 cases)
- Is "charged for spam calls" **predatory billing** or **script failure**? (2 cases)
- Is "messages have wrong phone numbers" **garbled info** or **missed calls**? (2 cases)

These are edge cases within the same group. None of the disagreements cross group boundaries in a way that would change the story. Call handling is still 45%. Billing is still 33%. The narrative holds.

**Why 11 categories instead of fewer?** We tested k=7 and k=9 too. Kappa stays equally high at every level. We chose 11 because it's the most useful for product decisions — "billing" is too vague to act on, but "predatory billing" vs "billing traps" vs "opaque billing" each need a different product response.
