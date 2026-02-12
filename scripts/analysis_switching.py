#!/usr/bin/env python3
"""
Analysis 2: Competitor Switching Matrix
Extracts FROM→TO pairs from switching quotes, builds transition matrix,
calculates net churn scores per competitor.

FROM→TO pairs are manually coded from reading each of the 28 switching quotes.
"""

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
QUOTES_FILE = os.path.join(BASE, "clean_quotes", "final_quotes.json")
OUTPUT_FILE = os.path.join(BASE, "analysis", "02_switching_matrix.md")

# Manually coded FROM→TO transitions from reading all 28 churn_switched quotes.
# Each entry: (from_product, to_product, trigger_category, quote_index_in_file, key_detail)
# "Unknown" = mentioned switching but didn't name the other product
# "In-house" = hired own staff
# "Cancelled" = cancelled without switching to named competitor
# "Voicemail" = was using voicemail before (not a competitor)

TRANSITIONS = [
    # Quote 1: Virtual HQ → In-house (missed calls, inconsistent receptionists)
    ("Virtual HQ", "In-house", "quality", 1, "Missed 1 in 5 calls, clients grumpy with answering service"),
    # Quote 2: Ruby → (still using but recommends own staff for better conversions)
    ("Ruby", "In-house", "quality", 2, "People can tell the difference; conversions better with own staff"),
    # Quote 3: Smith.ai → Ruby (multiple client complaints about call quality)
    ("Smith.ai", "Ruby", "quality", 3, "4 client complaints about call quality; Ruby resolved it"),
    # Quote 4: Multiple AI providers → Dialzara (couldn't adapt, more expensive)
    ("Other AI providers", "Dialzara", "capability", 4, "AI providers couldn't adapt; more expensive"),
    # Quote 5: Answering service → Dialzara (saving $1000/mo)
    ("Answering service", "Dialzara", "pricing", 5, "Saving $1000/mo by cancelling previous service"),
    # Quote 6: Voicemail → Ruby (customers hated menu system)
    ("Voicemail", "Ruby", "upgrade", 6, "Customers hated menu-based voicemail; Ruby improved communication"),
    # Quote 7: Previous call center → PATLive ('we can't do that')
    ("Other service", "PATLive", "capability", 7, "Previous center said 'we can't do that'; PATLive customized"),
    # Quote 8: AnswerConnect → Would switch if could (wrong info captured)
    ("AnswerConnect", "Would switch", "quality", 8, "Routinely captures wrong phone numbers, addresses, emails"),
    # Quote 9: Smith.ai → Unknown competitor (overpromised AI, half the price)
    ("Smith.ai", "Unknown", "pricing", 9, "Overpromised AI; found competitor at less than half the price"),
    # Quote 10: Smith.ai → Unknown US-based (dropped calls, lost business for 2 years)
    ("Smith.ai", "Unknown (US-based)", "quality", 10, "Dropped calls, lost business over 2 years"),
    # Quote 11: AnswerConnect → In-house (script changes take days, agents robotic)
    ("AnswerConnect", "In-house", "capability", 11, "Script changes take days; agents lack common sense"),
    # Quote 12: Cheaper call center → Ruby (was costing valuable cases)
    ("Other service", "Ruby", "quality", 12, "Cheaper service was costing valuable potential cases"),
    # Quote 13: Other service → PATLive (values Jobber integration)
    ("Other service", "PATLive", "capability", 13, "Previous service unsatisfying; PATLive integrated with Jobber"),
    # Quote 14: 4 other companies → PATLive (none were professional enough)
    ("Other service", "PATLive", "quality", 14, "Tried 4 others; none provided professional support"),
    # Quote 15: SAS → PATLive (bad experience during free trial)
    ("SAS", "PATLive", "quality", 15, "Such bad SAS experience during trial they switched immediately"),
    # Quote 16: 5-6 services → Abby Connect (best by a long shot)
    ("Other service", "Abby Connect", "quality", 16, "Went through 5-6 services; Abby best by far"),
    # Quote 17: Other companies → Abby Connect (US-based, no language issues)
    ("Other service", "Abby Connect", "quality", 17, "Tried others; chose Abby for US-based call center"),
    # Quote 18: Ruby → Shopping for alternatives (service declined, price not justified)
    ("Ruby", "Shopping", "pricing", 18, "Service not what it used to be; price no longer justified"),
    # Quote 19: Ruby → Abby Connect (service declined from personalized to rote)
    ("Ruby", "Abby Connect", "quality", 19, "Highly personalized service became rote and embarrassing"),
    # Quote 20: Ruby → Conversational (Google Voice integration failed)
    ("Ruby", "Conversational", "capability", 20, "Sales promised Google Voice compatibility; tech failed"),
    # Quote 21: Unknown → Smith.ai (values call transparency)
    ("Other service", "Smith.ai", "capability", 21, "Switched for call transparency and spam blocking"),
    # Quote 22: Other service → PATLive (more flexible scenarios)
    ("Other service", "PATLive", "capability", 22, "Previous service less flexible; PATLive more accommodating"),
    # Quote 23: 3 other services → Abby Connect (helps increase conversions)
    ("Other service", "Abby Connect", "quality", 23, "Tried 3 others; Abby helps increase conversions"),
    # Quote 24: Live receptionist → Smith.ai (to cut costs)
    ("Live receptionist", "Smith.ai", "pricing", 24, "Switched to cut costs; never looked back"),
    # Quote 25: Ruby → Cancelled (too expensive)
    ("Ruby", "Cancelled", "pricing", 25, "Used for years; cancelled because too expensive"),
    # Quote 26: Ruby → Cancelled (10 rings no answer, clueless receptionist)
    ("Ruby", "Cancelled", "quality", 26, "10 rings no answer; receptionist didn't know the company"),
    # Quote 27: Ruby → Cancelled (customer service deteriorated)
    ("Ruby", "Cancelled", "quality", 27, "Customer service horrible; reps hang up; cancelled after 3 years"),
    # Quote 28: Smith.ai → Unknown (AI sounds human but too many kinks, dishonest cancellation)
    ("Smith.ai", "Cancelled", "quality", 28, "Lost calls during trial; dishonest 30-day cancellation policy"),
]


def load_quotes():
    with open(QUOTES_FILE, "r") as f:
        return json.load(f)


def get_switching_quotes(quotes):
    return [q for q in quotes if q["llm"].get("category") == "churn_switched"]


def build_matrix():
    """Build FROM→TO transition matrix and net scores."""
    # Normalize product names
    from_counts = {}
    to_counts = {}
    transitions_by_from = {}
    transitions_by_to = {}
    trigger_counts = {}

    for frm, to, trigger, idx, detail in TRANSITIONS:
        # Skip non-competitor transitions (Voicemail→X is an upgrade, not churn)
        if frm == "Voicemail":
            continue

        from_counts[frm] = from_counts.get(frm, 0) + 1
        to_counts[to] = to_counts.get(to, 0) + 1
        trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1

        if frm not in transitions_by_from:
            transitions_by_from[frm] = []
        transitions_by_from[frm].append((to, trigger, detail))

        if to not in transitions_by_to:
            transitions_by_to[to] = []
        transitions_by_to[to].append((frm, trigger, detail))

    # Named competitors only (exclude generic categories)
    named_from = {k: v for k, v in from_counts.items()
                  if k not in ("Other service", "Other AI providers", "Answering service", "Live receptionist")}
    named_to = {k: v for k, v in to_counts.items()
                if k not in ("Unknown", "Unknown (US-based)", "Shopping", "Would switch", "Cancelled")}

    # Net churn score for named competitors
    all_named = set(list(named_from.keys()) + list(named_to.keys()))
    net_scores = {}
    for name in all_named:
        inflows = to_counts.get(name, 0)
        outflows = from_counts.get(name, 0)
        net_scores[name] = inflows - outflows

    return {
        "from_counts": from_counts,
        "to_counts": to_counts,
        "transitions_by_from": transitions_by_from,
        "transitions_by_to": transitions_by_to,
        "trigger_counts": trigger_counts,
        "net_scores": net_scores,
        "named_from": named_from,
        "named_to": named_to,
    }


def generate_markdown(data, switching_quotes):
    lines = []
    lines.append("# Analysis 2: Competitor Switching Matrix")
    lines.append("")
    lines.append("> **CPO Question:** \"When users leave a receptionist service, who are they leaving and where do they go?\"")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append("- **Data:** 28 quotes classified as `churn_switched` from 378 total classified quotes")
    lines.append("- **Extraction:** Each quote manually read and coded for FROM (product left) and TO (product chosen)")
    lines.append("- **Trigger categories:** quality (service failures), pricing (cost issues), capability (missing features/integrations)")
    lines.append("- **Net churn score:** Inflows (users switching TO) minus Outflows (users switching FROM)")
    lines.append("  - Positive = net gainer, Negative = net loser")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Outflow table (who users are leaving)
    lines.append("## Who Users Are Leaving (Outflows)")
    lines.append("")
    lines.append("| Competitor | Users Leaving | Key Triggers |")
    lines.append("|---|:---:|---|")

    sorted_from = sorted(data["from_counts"].items(), key=lambda x: x[1], reverse=True)
    for name, count in sorted_from:
        if name in ("Other service", "Other AI providers", "Answering service", "Voicemail", "Live receptionist"):
            continue
        triggers = data["transitions_by_from"].get(name, [])
        trigger_summary = "; ".join(set(t[1] for t in triggers))
        lines.append(f"| **{name}** | {count} | {trigger_summary} |")

    generic_count = sum(v for k, v in data["from_counts"].items()
                        if k in ("Other service", "Other AI providers", "Answering service", "Live receptionist"))
    lines.append(f"| *Unnamed services* | {generic_count} | *(various — users didn't name specific product)* |")
    lines.append("")

    # Inflow table (where users go)
    lines.append("## Where Users Go (Inflows)")
    lines.append("")
    lines.append("| Destination | Users Arriving | Coming From |")
    lines.append("|---|:---:|---|")

    sorted_to = sorted(data["to_counts"].items(), key=lambda x: x[1], reverse=True)
    for name, count in sorted_to:
        sources = data["transitions_by_to"].get(name, [])
        source_summary = ", ".join(set(t[0] for t in sources))
        lines.append(f"| **{name}** | {count} | {source_summary} |")

    lines.append("")

    # Net churn score
    lines.append("## Net Churn Score (Named Competitors Only)")
    lines.append("")
    lines.append("> Net score = users arriving − users leaving. Positive = net gainer, negative = net loser.")
    lines.append("")
    lines.append("| Competitor | Arriving | Leaving | Net Score | Status |")
    lines.append("|---|:---:|:---:|:---:|:---:|")

    sorted_net = sorted(data["net_scores"].items(), key=lambda x: x[1], reverse=True)
    for name, net in sorted_net:
        inflows = data["to_counts"].get(name, 0)
        outflows = data["from_counts"].get(name, 0)
        status = "NET GAINER" if net > 0 else ("NET LOSER" if net < 0 else "NEUTRAL")
        icon = "🟢" if net > 0 else ("🔴" if net < 0 else "⚪")
        lines.append(f"| **{name}** | {inflows} | {outflows} | {net:+d} | {icon} {status} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Switching triggers
    lines.append("## Why Users Switch — Trigger Breakdown")
    lines.append("")
    total_triggers = sum(data["trigger_counts"].values())
    trigger_labels = {
        "quality": "Service quality failures (missed calls, wrong info, declined service)",
        "pricing": "Pricing issues (too expensive, hidden fees, overcharges)",
        "capability": "Missing capabilities (no customization, no integrations, AI limitations)",
        "upgrade": "Upgrading from voicemail/nothing to a service",
    }

    lines.append("| Trigger | Count | % | Description |")
    lines.append("|---|:---:|:---:|---|")
    for trigger, count in sorted(data["trigger_counts"].items(), key=lambda x: x[1], reverse=True):
        pct = count / total_triggers * 100 if total_triggers else 0
        desc = trigger_labels.get(trigger, trigger)
        lines.append(f"| **{trigger.title()}** | {count} | {pct:.0f}% | {desc} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Detailed FROM breakdowns with quotes
    lines.append("## Detailed: Why Users Leave Each Competitor")
    lines.append("")

    focus_competitors = ["Ruby", "Smith.ai", "AnswerConnect"]
    for comp in focus_competitors:
        if comp not in data["transitions_by_from"]:
            continue
        transitions = data["transitions_by_from"][comp]
        lines.append(f"### {comp} ({len(transitions)} departures)")
        lines.append("")

        for to, trigger, detail in transitions:
            lines.append(f"- → **{to}** ({trigger}): {detail}")

        lines.append("")

        # Find matching quotes
        comp_quotes = [q for q in switching_quotes
                       if q["llm"].get("product_mentioned", "").lower().startswith(comp.lower().split(".")[0].split(" ")[0])]
        if comp_quotes:
            best = sorted(comp_quotes, key=lambda q: q["llm"].get("quote_quality", 0), reverse=True)[0]
            text = best["text"].replace("\n", " ").strip()
            if len(text) > 300:
                text = text[:300] + "..."
            lines.append(f"**Most telling quote:**")
            lines.append(f"> {text}")
            if best.get("url"):
                lines.append(f"[Source]({best['url']})")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Key insight
    lines.append("## Key Insight — Where to Win")
    lines.append("")

    # Find biggest loser
    biggest_loser = min(data["net_scores"].items(), key=lambda x: x[1]) if data["net_scores"] else None
    biggest_gainer = max(data["net_scores"].items(), key=lambda x: x[1]) if data["net_scores"] else None

    lines.append("> **Ruby's customers are the most accessible acquisition target.**")
    lines.append(">")
    if biggest_loser:
        lines.append(f"> **{biggest_loser[0]}** is the biggest net loser ({biggest_loser[1]:+d}) — users are actively leaving, citing service quality decline and rising prices.")
        lines.append(">")
    lines.append("> The dominant switching trigger is **quality failures** — missed calls, wrong information, receptionists who don't know the business. This is exactly what AI can solve with consistent, trained models.")
    lines.append(">")
    lines.append("> **For Central AI's go-to-market:** Target Ruby and Smith.ai's customer base with messaging around consistency, accuracy, and transparent pricing.")
    lines.append("")

    return "\n".join(lines)


def main():
    quotes = load_quotes()
    switching_quotes = get_switching_quotes(quotes)
    data = build_matrix()
    md = generate_markdown(data, switching_quotes)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write(md)

    print(f"Switching matrix written to {OUTPUT_FILE}")
    print(f"  Total transitions: {len(TRANSITIONS)}")
    print(f"  Named competitors leaving: {data['named_from']}")
    print(f"  Named competitors gaining: {data['named_to']}")
    print(f"  Net scores: {dict(sorted(data['net_scores'].items(), key=lambda x: x[1]))}")


if __name__ == "__main__":
    main()
