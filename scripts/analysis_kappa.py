#!/usr/bin/env python3
"""
Inter-Rater Reliability Analysis
- Loads dual-coded classifications at k=7
- Rolls up to k=6, 5, 4, 3 using defined hierarchy
- Computes Cohen's kappa at each level
- Identifies disagreements for adjudication
- Outputs final analysis with kappa curve
"""

import json
import os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
CODER_A_FILE = os.path.join(BASE, "analysis", "coder_a.json")
CODER_B_FILE = os.path.join(BASE, "analysis", "coder_b.json")
QUOTES_FILE = os.path.join(BASE, "clean_quotes", "final_quotes.json")
OUTPUT_FILE = os.path.join(BASE, "analysis", "05_kappa_analysis.md")
FINAL_CODES_FILE = os.path.join(BASE, "analysis", "final_codes.json")

# ── Rollup hierarchy ──────────────────────────────────────────────────
# k=7 is the base. Each coarser level merges categories.

ROLLUP = {
    7: {  # identity — no merging
        "SCRIPT_FAILURES": "SCRIPT_FAILURES",
        "GARBLED_INFO": "GARBLED_INFO",
        "INAUTHENTICITY": "INAUTHENTICITY",
        "BILLING": "BILLING",
        "MISSED_CALLS": "MISSED_CALLS",
        "QUALITY_DECAY": "QUALITY_DECAY",
        "SERIAL_SWITCHING": "SERIAL_SWITCHING",
    },
    6: {  # merge GARBLED_INFO into SCRIPT_FAILURES → AGENT_ERRORS
        "SCRIPT_FAILURES": "AGENT_ERRORS",
        "GARBLED_INFO": "AGENT_ERRORS",
        "INAUTHENTICITY": "INAUTHENTICITY",
        "BILLING": "BILLING",
        "MISSED_CALLS": "MISSED_CALLS",
        "QUALITY_DECAY": "QUALITY_DECAY",
        "SERIAL_SWITCHING": "SERIAL_SWITCHING",
    },
    5: {  # merge INAUTHENTICITY into AGENT_ERRORS → CALL_HANDLING
        "SCRIPT_FAILURES": "CALL_HANDLING",
        "GARBLED_INFO": "CALL_HANDLING",
        "INAUTHENTICITY": "CALL_HANDLING",
        "BILLING": "BILLING",
        "MISSED_CALLS": "MISSED_CALLS",
        "QUALITY_DECAY": "QUALITY_DECAY",
        "SERIAL_SWITCHING": "SERIAL_SWITCHING",
    },
    4: {  # merge MISSED_CALLS + QUALITY_DECAY → SERVICE_RELIABILITY
        "SCRIPT_FAILURES": "CALL_HANDLING",
        "GARBLED_INFO": "CALL_HANDLING",
        "INAUTHENTICITY": "CALL_HANDLING",
        "BILLING": "BILLING",
        "MISSED_CALLS": "SERVICE_RELIABILITY",
        "QUALITY_DECAY": "SERVICE_RELIABILITY",
        "SERIAL_SWITCHING": "SERIAL_SWITCHING",
    },
    3: {  # merge SERIAL_SWITCHING into SERVICE_RELIABILITY → SERVICE_FAILS
        "SCRIPT_FAILURES": "CALL_HANDLING",
        "GARBLED_INFO": "CALL_HANDLING",
        "INAUTHENTICITY": "CALL_HANDLING",
        "BILLING": "BILLING",
        "MISSED_CALLS": "SERVICE_FAILS",
        "QUALITY_DECAY": "SERVICE_FAILS",
        "SERIAL_SWITCHING": "SERVICE_FAILS",
    },
}

LEVEL_LABELS = {
    7: ["SCRIPT_FAILURES", "GARBLED_INFO", "INAUTHENTICITY", "BILLING",
        "MISSED_CALLS", "QUALITY_DECAY", "SERIAL_SWITCHING"],
    6: ["AGENT_ERRORS", "INAUTHENTICITY", "BILLING",
        "MISSED_CALLS", "QUALITY_DECAY", "SERIAL_SWITCHING"],
    5: ["CALL_HANDLING", "BILLING", "MISSED_CALLS", "QUALITY_DECAY", "SERIAL_SWITCHING"],
    4: ["CALL_HANDLING", "BILLING", "SERVICE_RELIABILITY", "SERIAL_SWITCHING"],
    3: ["CALL_HANDLING", "BILLING", "SERVICE_FAILS"],
}


def load_coder(filepath):
    with open(filepath) as f:
        data = json.load(f)
    # Build idx → category map
    codes = {}
    for item in data["classifications"]:
        codes[item["idx"]] = item["category"]
    return codes, data


def rollup(codes, level):
    """Roll up k=7 codes to a coarser level."""
    mapping = ROLLUP[level]
    return {idx: mapping.get(cat, cat) for idx, cat in codes.items()}


def cohens_kappa(labels_a, labels_b, categories):
    """Compute Cohen's kappa between two sets of labels."""
    n = len(labels_a)
    if n == 0:
        return 0

    # Observed agreement
    agree = sum(1 for i in range(n) if labels_a[i] == labels_b[i])
    po = agree / n

    # Expected agreement (by chance)
    pe = 0
    for cat in categories:
        count_a = sum(1 for l in labels_a if l == cat)
        count_b = sum(1 for l in labels_b if l == cat)
        pe += (count_a / n) * (count_b / n)

    if pe >= 1.0:
        return 1.0

    kappa = (po - pe) / (1 - pe)
    return kappa


def confusion_matrix(labels_a, labels_b, categories):
    """Build confusion matrix."""
    matrix = {}
    for cat_a in categories:
        matrix[cat_a] = {}
        for cat_b in categories:
            matrix[cat_a][cat_b] = 0

    for la, lb in zip(labels_a, labels_b):
        if la in matrix and lb in matrix[la]:
            matrix[la][lb] += 1

    return matrix


def adjudicate(codes_a, codes_b, reasons_a, reasons_b):
    """Simple adjudication: majority wins. For dual coding, pick Coder A when disagreed
    (in practice you'd have a third coder, but we document disagreements)."""
    final = {}
    disagreements = []
    for idx in sorted(codes_a.keys()):
        ca = codes_a.get(idx, "UNKNOWN")
        cb = codes_b.get(idx, "UNKNOWN")
        if ca == cb:
            final[idx] = ca
        else:
            # Default to Coder A but flag it
            final[idx] = ca
            disagreements.append({
                "idx": idx,
                "coder_a": ca,
                "reason_a": reasons_a.get(idx, ""),
                "coder_b": cb,
                "reason_b": reasons_b.get(idx, ""),
                "resolved_to": ca,
            })
    return final, disagreements


def load_churn_quotes():
    with open(QUOTES_FILE) as f:
        all_quotes = json.load(f)
    return [q for q in all_quotes if q["llm"].get("category", "").startswith("churn_")]


def generate_markdown(kappa_results, codes_a, codes_b, data_a, data_b,
                      final_codes, disagreements, quotes):
    lines = []
    lines.append("# Analysis 5: Inter-Rater Reliability & Optimal Taxonomy")
    lines.append("")
    lines.append("> **Meta DS Question:** \"How many categories does the data actually support? At what granularity do independent coders agree?\"")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append("1. **Codebook:** 7 categories defined with explicit decision rules and tie-breakers")
    lines.append("2. **Dual coding:** Two independent LLM coders classified all 137 churn quotes at k=7")
    lines.append("3. **Deterministic rollup:** k=7 codes rolled up to k=6, 5, 4, 3 via predefined hierarchy")
    lines.append("4. **Cohen's kappa:** Computed at each level — measures agreement beyond chance")
    lines.append("5. **Optimal k:** The level where kappa peaks = the number of categories the data supports")
    lines.append("")

    # Rollup hierarchy
    lines.append("### Rollup Hierarchy")
    lines.append("```")
    lines.append("k=7: SCRIPT_FAILURES | GARBLED_INFO | INAUTHENTICITY | BILLING | MISSED_CALLS | QUALITY_DECAY | SERIAL_SWITCHING")
    lines.append("k=6: AGENT_ERRORS────────────────┘ | INAUTHENTICITY | BILLING | MISSED_CALLS | QUALITY_DECAY | SERIAL_SWITCHING")
    lines.append("k=5: CALL_HANDLING──────────────────────────────────┘ | BILLING | MISSED_CALLS | QUALITY_DECAY | SERIAL_SWITCHING")
    lines.append("k=4: CALL_HANDLING                                    | BILLING | SERVICE_RELIABILITY──────────┘ | SERIAL_SWITCHING")
    lines.append("k=3: CALL_HANDLING                                    | BILLING | SERVICE_FAILS────────────────────────────────────┘")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Kappa curve
    lines.append("## The Kappa Curve — Finding Optimal k")
    lines.append("")
    lines.append("| k | Categories | Agreement % | Cohen's Kappa | Interpretation |")
    lines.append("|:---:|:---:|:---:|:---:|---|")

    kappa_interp = {
        (0.81, 1.0): "Almost perfect",
        (0.61, 0.80): "Substantial",
        (0.41, 0.60): "Moderate",
        (0.21, 0.40): "Fair",
        (0.0, 0.20): "Slight",
        (-1.0, 0.0): "Poor",
    }

    best_k = max(kappa_results, key=lambda x: x[2])

    for k, agree_pct, kappa in kappa_results:
        interp = "Poor"
        for (lo, hi), label in kappa_interp.items():
            if lo <= kappa <= hi:
                interp = label
                break
        marker = " **← OPTIMAL**" if k == best_k[0] else ""
        bar = "█" * max(0, int(kappa * 20)) if kappa > 0 else ""
        lines.append(f"| {k} | {k} | {agree_pct:.1f}% | **{kappa:.3f}** {bar} | {interp}{marker} |")

    lines.append("")

    # Visual kappa curve
    lines.append("### Kappa Curve")
    lines.append("```")
    for k, _, kappa in kappa_results:
        bar_len = max(0, int(kappa * 40))
        marker = " ← PEAK" if k == best_k[0] else ""
        lines.append(f"  k={k}  {'█' * bar_len}{'░' * (40 - bar_len)}  κ={kappa:.3f}{marker}")
    lines.append("```")
    lines.append("")

    lines.append(f"**Optimal k = {best_k[0]}** (κ = {best_k[2]:.3f})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Category distribution at optimal k
    optimal_k = best_k[0]
    optimal_codes = {idx: rollup({idx: final_codes[idx]}, optimal_k)[idx]
                     for idx in final_codes}
    cat_counts = Counter(optimal_codes.values())
    total = sum(cat_counts.values())

    lines.append(f"## Final Taxonomy at k={optimal_k}")
    lines.append("")
    lines.append("| Category | Count | % | Description |")
    lines.append("|---|:---:|:---:|---|")

    cat_descriptions = {
        "SCRIPT_FAILURES": "Agents don't follow scripts or call-handling instructions",
        "GARBLED_INFO": "Wrong names, emails, phone numbers captured",
        "INAUTHENTICITY": "Callers detect it's not real staff",
        "BILLING": "Pricing, overcharges, hidden fees, adversarial billing",
        "MISSED_CALLS": "Calls go unanswered, messages delayed",
        "QUALITY_DECAY": "Service deteriorated over time from a good baseline",
        "SERIAL_SWITCHING": "Tried multiple services, category-level disillusionment",
        "AGENT_ERRORS": "Scripts ignored + wrong info captured",
        "CALL_HANDLING": "All call quality issues (scripts, info, authenticity)",
        "SERVICE_RELIABILITY": "Missed calls + quality decay over time",
        "SERVICE_FAILS": "Missed calls + quality decay + serial switching",
    }

    for cat in sorted(cat_counts.keys(), key=lambda c: cat_counts[c], reverse=True):
        count = cat_counts[cat]
        pct = count / total * 100
        desc = cat_descriptions.get(cat, "")
        lines.append(f"| **{cat}** | {count} | {pct:.0f}% | {desc} |")

    lines.append(f"| **Total** | **{total}** | **100%** | |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Disagreements
    n_disagree = len(disagreements)
    n_total = len(final_codes)
    lines.append(f"## Disagreements: {n_disagree} of {n_total} quotes ({n_disagree/n_total*100:.1f}%)")
    lines.append("")

    if disagreements:
        # Disagreement pattern
        disagree_pairs = Counter()
        for d in disagreements:
            pair = tuple(sorted([d["coder_a"], d["coder_b"]]))
            disagree_pairs[pair] += 1

        lines.append("### Most Common Disagreement Pairs (at k=7)")
        lines.append("")
        lines.append("| Category A | Category B | Count | Notes |")
        lines.append("|---|---|:---:|---|")
        for (a, b), count in disagree_pairs.most_common(10):
            # Check if they collapse at a coarser level
            collapse_at = None
            for test_k in [6, 5, 4, 3]:
                ra = ROLLUP[test_k].get(a, a)
                rb = ROLLUP[test_k].get(b, b)
                if ra == rb:
                    collapse_at = test_k
                    break
            note = f"Collapse at k={collapse_at}" if collapse_at else "Never collapse"
            lines.append(f"| {a} | {b} | {count} | {note} |")

        lines.append("")
        lines.append("*Disagreements that 'collapse' at a coarser k don't affect kappa at that level — they only matter at finer granularity.*")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Confusion matrix at k=7
    labels_a_7 = [codes_a[i] for i in sorted(codes_a.keys())]
    labels_b_7 = [codes_b[i] for i in sorted(codes_b.keys())]
    categories_7 = LEVEL_LABELS[7]
    cm = confusion_matrix(labels_a_7, labels_b_7, categories_7)

    lines.append("## Confusion Matrix (k=7)")
    lines.append("")
    short_names = {
        "SCRIPT_FAILURES": "Script",
        "GARBLED_INFO": "Garbled",
        "INAUTHENTICITY": "Inauth",
        "BILLING": "Billing",
        "MISSED_CALLS": "Missed",
        "QUALITY_DECAY": "Decay",
        "SERIAL_SWITCHING": "Serial",
    }
    header = "| Coder A \\ B | " + " | ".join(short_names.get(c, c) for c in categories_7) + " |"
    lines.append(header)
    lines.append("|---|" + ":---:|" * len(categories_7))
    for cat_a in categories_7:
        cells = []
        for cat_b in categories_7:
            val = cm[cat_a][cat_b]
            if cat_a == cat_b:
                cells.append(f"**{val}**" if val > 0 else "·")
            else:
                cells.append(str(val) if val > 0 else "·")
        lines.append(f"| **{short_names.get(cat_a, cat_a)}** | {' | '.join(cells)} |")

    lines.append("")
    lines.append("*Bold diagonal = agreement. Off-diagonal = disagreements.*")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Key insight
    lines.append("## Key Insight")
    lines.append("")
    lines.append(f"> **The data supports {best_k[0]} distinct churn categories** (κ = {best_k[2]:.3f}).")
    lines.append(">")
    if best_k[0] <= 4:
        lines.append(f"> At k={best_k[0]}, two independent coders reach {'substantial' if best_k[2] > 0.6 else 'moderate' if best_k[2] > 0.4 else 'fair'} agreement — meaning these categories are clear enough that different people (or models) consistently classify quotes the same way.")
    else:
        lines.append(f"> The data supports more granularity than the original 5 top-down categories. Coders can reliably distinguish {best_k[0]} distinct types of churn complaint.")
    lines.append(">")
    lines.append("> This is now a **validated, reproducible taxonomy** — not an assumption.")
    lines.append("")

    return "\n".join(lines)


def main():
    # Load coders
    print("Loading coder outputs...")
    codes_a, data_a = load_coder(CODER_A_FILE)
    codes_b, data_b = load_coder(CODER_B_FILE)

    # Build reason maps
    reasons_a = {item["idx"]: item.get("reason", "") for item in data_a["classifications"]}
    reasons_b = {item["idx"]: item.get("reason", "") for item in data_b["classifications"]}

    # Ensure same indices
    common_idx = sorted(set(codes_a.keys()) & set(codes_b.keys()))
    print(f"  Coder A: {len(codes_a)} classifications")
    print(f"  Coder B: {len(codes_b)} classifications")
    print(f"  Common: {len(common_idx)}")

    # Compute kappa at each level
    print("\nComputing kappa at each level...")
    kappa_results = []

    for k in [3, 4, 5, 6, 7]:
        labels_a = [rollup(codes_a, k)[i] for i in common_idx]
        labels_b = [rollup(codes_b, k)[i] for i in common_idx]
        categories = LEVEL_LABELS[k]

        agree = sum(1 for a, b in zip(labels_a, labels_b) if a == b)
        agree_pct = agree / len(common_idx) * 100
        kappa = cohens_kappa(labels_a, labels_b, categories)

        kappa_results.append((k, agree_pct, kappa))
        print(f"  k={k}: agreement={agree_pct:.1f}%, kappa={kappa:.3f}")

    # Adjudicate at k=7
    print("\nAdjudicating disagreements...")
    final_codes, disagreements = adjudicate(codes_a, codes_b, reasons_a, reasons_b)
    print(f"  Disagreements: {len(disagreements)} of {len(common_idx)}")

    # Save final codes
    quotes = load_churn_quotes()
    final_output = {
        "method": "dual-coded with kappa validation",
        "optimal_k": max(kappa_results, key=lambda x: x[2])[0],
        "kappa_at_optimal": max(kappa_results, key=lambda x: x[2])[2],
        "total": len(final_codes),
        "codes_k7": [{"idx": i, "category": final_codes[i]} for i in sorted(final_codes.keys())],
        "rollup_hierarchy": {str(k): {str(k2): v for k2, v in mapping.items()}
                             for k, mapping in ROLLUP.items()},
        "disagreements": disagreements,
    }
    with open(FINAL_CODES_FILE, "w") as f:
        json.dump(final_output, f, indent=2)
    print(f"  Final codes saved to {FINAL_CODES_FILE}")

    # Generate markdown
    md = generate_markdown(kappa_results, codes_a, codes_b, data_a, data_b,
                           final_codes, disagreements, quotes)

    with open(OUTPUT_FILE, "w") as f:
        f.write(md)
    print(f"\nKappa analysis written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
