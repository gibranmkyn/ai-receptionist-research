# Churn Taxonomy Codebook — k=9 (Maximum Granularity)

## Purpose
Classify each of the 137 churn quotes into exactly ONE of 9 mutually exclusive categories.

---

## 1. SCRIPT_ADHERENCE
**Agents don't follow scripts, instructions, or lack business knowledge to handle calls.**

Agents ignore, misunderstand, or forget the scripts and call-handling instructions. Includes shared-pool inconsistency (rotating agents, no one knows the business) and inability to handle anything beyond basic message-taking.

**Include when:**
- Agents don't follow the script despite training
- Business owner describes endless cycle of re-training
- "We can't do that" responses to reasonable requests
- Shared pool means different agent every time, no one learns the business
- Agent can't handle FAQs, scheduling, or anything beyond message-taking

**Exclude when:**
- Calls routed to wrong person/department → ROUTING_ERRORS
- Wrong contact info captured → GARBLED_INFO
- Callers sense it's not real staff → INAUTHENTICITY
- Quote focuses on trying multiple services → SERIAL_SWITCHING

---

## 2. ROUTING_ERRORS
**Calls sent to wrong person, wrong department, or wrong on-call tech.**

The specific failure is MISDIRECTING calls — not about script content but about WHO the call goes to. Wrong dispatch, wrong department, wrong on-call schedule followed.

**Include when:**
- Call forwarded to wrong person
- Wrong technician dispatched
- On-call schedule not followed
- Emergency call sent to non-emergency line (or vice versa)

**Exclude when:**
- Agent follows routing correctly but reads script wrong → SCRIPT_ADHERENCE
- Agent captures wrong phone number → GARBLED_INFO

---

## 3. GARBLED_INFO
**Wrong names, emails, phone numbers, or messages captured.**

Data accuracy failure. The agent captured information but it's wrong or incomplete.

**Include when:**
- Misspelled names, wrong phone numbers, garbled emails
- Incomplete messages (missing key details)
- High error rate on basic data capture (70-80% incomplete)
- Business has to re-contact every caller for correct info

**Exclude when:**
- Agent didn't attempt to capture info (script not followed) → SCRIPT_ADHERENCE
- Agent captured info fine but caller sensed inauthenticity → INAUTHENTICITY

---

## 4. INAUTHENTICITY
**Callers can tell it's not real staff.**

The caller experience of sensing the person is NOT from the actual business. Robotic, generic, can't answer basic questions, don't know the company.

**Include when:**
- Agents sound robotic / read from screen
- Can't pronounce business name
- Can't answer basic questions ("Do you have a website?")
- Callers get grumpy or conversions drop
- Agent doesn't know which company they're answering for

**Exclude when:**
- Agent sounds fine but gets info wrong → GARBLED_INFO
- Agent sounds fine but ignores instructions → SCRIPT_ADHERENCE

---

## 5. BILLING_PREDATORY
**Provider actively extracts unearned revenue through deceptive practices.**

Deliberate billing manipulation: inflating call durations, charging for spam, bait-and-switch on plans, upselling without consent.

**Include when:**
- Agents ask callers to spell things 3-4 times to inflate call time
- "After-call work" charges pad invoices
- Spam/robocalls billed as real calls
- Bot calls consuming paid minutes with no blocking
- Upsold to wrong plan or account went live without consent
- Recycled phone number generating charges for unrelated calls

**Exclude when:**
- Bill is just high/confusing but no deception implied → BILLING_OPAQUE
- Can't cancel or charged after cancelling → BILLING_TRAP
- Service works fine, just too expensive → BILLING_TOO_EXPENSIVE

**Key test:** Does the quote imply INTENTIONAL extraction? If yes → PREDATORY. If it's just confusing/unexpected → OPAQUE.

---

## 6. BILLING_OPAQUE
**Pricing is confusing, bills are unexpectedly high, or invoicing is broken.**

Not deceptive, but the pricing model creates surprise. Overages, unclear rate structures, stealth price increases, billing errors.

**Include when:**
- Bill is 7-10× expected budget
- Unclear what's being charged for
- Annual price increases without notice
- Invoicing errors or incorrect charges
- Per-minute model leads to unpredictable costs
- Lower-tier pricing options removed

**Exclude when:**
- Quote implies intentional manipulation → BILLING_PREDATORY
- Quote is about post-cancellation charges → BILLING_TRAP
- Service is fine, just too expensive on principle → BILLING_TOO_EXPENSIVE

---

## 7. BILLING_TRAP
**Post-cancellation charges, impossible exit, or weaponized cancellation process.**

The service makes it hard to leave. Charges continue months after cancelling. Cancellation requires specific channels. Accounts sent to collections.

**Include when:**
- Charged for months after cancellation
- Required to give 30-day notice even during "risk-free" trial
- Credit card charged after explicit cancellation
- Sent to collections
- Email-only cancellation process designed to be hard

**Exclude when:**
- Still an active customer complaining about billing → BILLING_PREDATORY or BILLING_OPAQUE
- Not about exit, just about price → BILLING_TOO_EXPENSIVE

---

## 8. BILLING_TOO_EXPENSIVE
**Service works but costs too much. Pure price sensitivity.**

The complaint is simply that the price is too high for what they get. No deception, no confusion — just "not worth it at this price."

**Include when:**
- "Too expensive" / "can't afford it"
- Price increased and no longer justified by service quality
- Comparing cost to alternatives and choosing cheaper
- Listing answering service as a significant overhead expense

**Exclude when:**
- Quote describes billing manipulation → BILLING_PREDATORY
- Quote describes confusing charges → BILLING_OPAQUE
- Quote describes post-cancellation charges → BILLING_TRAP

---

## 9. MISSED_CALLS
**Calls go unanswered, messages delayed, callbacks never happen.**

The fundamental promise — "we answer your calls" — is broken.

**Include when:**
- Calls ring 5+ times with no answer
- Messages delayed for hours or not delivered
- Callbacks promised but never made
- Long hold times causing hang-ups
- Lost leads/revenue because call wasn't handled in time

**Exclude when:**
- Call WAS answered but handled poorly → use the specific quality category
- The primary complaint is billing → use the billing category

---

## 10. QUALITY_DECAY
**Service used to be good but deteriorated over time.**

Requires an explicit TEMPORAL ARC: once satisfactory, now bad.

**Include when:**
- "Used to be great" / "not what it used to be"
- Long-time customer (1+ years) describing decline
- Former advocate now detractor
- "I was a big fan for X years but..."

**Exclude when:**
- Bad experience without mentioning it was ever good → use specific complaint category

---

## 11. SERIAL_SWITCHING
**Tried multiple services (2+), category-level disillusionment.**

The quote describes trying multiple services and finding the whole category unsatisfactory.

**Include when:**
- Mentions trying 2+ different services
- "Went through 5 services before finding..."
- Industry-level frustration

**Exclude when:**
- Switched from ONE specific service with a specific complaint → code the complaint
- Only mentions one product

---

## General Coding Rules
1. Read the FULL `text` field
2. Assign exactly ONE category
3. When multiple issues present, code for whichever the author spends the most words on
4. For billing ambiguity: PREDATORY requires implied INTENT. OPAQUE is confusion/surprise. TRAP is about exiting. TOO_EXPENSIVE is pure price.
5. If truly 50/50, code for whichever appears FIRST in the quote
