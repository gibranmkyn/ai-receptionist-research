#!/usr/bin/env python3
"""
Compute kappa at k=11 (the fine-grained codebook) and compare to k=7 results.
Also compute kappa at various rollup levels.
"""

import json
import math
import os
from collections import Counter
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))

def load_coder(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return {item["idx"]: item["category"] for item in data["classifications"]}

def cohens_kappa(labels_a, labels_b):
    n = len(labels_a)
    all_cats = sorted(set(labels_a) | set(labels_b))
    agree = sum(1 for a, b in zip(labels_a, labels_b) if a == b)
    po = agree / n
    pe = sum((sum(1 for l in labels_a if l == c) / n) *
             (sum(1 for l in labels_b if l == c) / n) for c in all_cats)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0, po

def kappa_bootstrap_ci(labels_a, labels_b, n_bootstrap=10000):
    np.random.seed(42)
    n = len(labels_a)
    kappas = []
    for _ in range(n_bootstrap):
        idx = np.random.choice(n, size=n, replace=True)
        ba = [labels_a[i] for i in idx]
        bb = [labels_b[i] for i in idx]
        k, _ = cohens_kappa(ba, bb)
        kappas.append(k)
    kappas.sort()
    return kappas[int(0.025 * n_bootstrap)], kappas[int(0.975 * n_bootstrap)]

# Rollup: k=11 → k=7 (merge billing sub-types back, merge routing into script)
ROLLUP_11_TO_7 = {
    "SCRIPT_ADHERENCE": "SCRIPT_FAILURES",
    "ROUTING_ERRORS": "SCRIPT_FAILURES",  # or keep separate?
    "GARBLED_INFO": "GARBLED_INFO",
    "INAUTHENTICITY": "INAUTHENTICITY",
    "BILLING_PREDATORY": "BILLING",
    "BILLING_OPAQUE": "BILLING",
    "BILLING_TRAP": "BILLING",
    "BILLING_TOO_EXPENSIVE": "BILLING",
    "MISSED_CALLS": "MISSED_CALLS",
    "QUALITY_DECAY": "QUALITY_DECAY",
    "SERIAL_SWITCHING": "SERIAL_SWITCHING",
}

# Alternative: k=11 → k=9 (keep billing splits, merge routing into script)
ROLLUP_11_TO_9 = {
    "SCRIPT_ADHERENCE": "SCRIPT_ADHERENCE",
    "ROUTING_ERRORS": "SCRIPT_ADHERENCE",
    "GARBLED_INFO": "GARBLED_INFO",
    "INAUTHENTICITY": "INAUTHENTICITY",
    "BILLING_PREDATORY": "BILLING_PREDATORY",
    "BILLING_OPAQUE": "BILLING_OPAQUE",
    "BILLING_TRAP": "BILLING_TRAP",
    "BILLING_TOO_EXPENSIVE": "BILLING_TOO_EXPENSIVE",
    "MISSED_CALLS": "MISSED_CALLS",
    "QUALITY_DECAY": "QUALITY_DECAY",
    "SERIAL_SWITCHING": "SERIAL_SWITCHING",
}

# k=11 → k=8 (merge billing trap+opaque, merge routing into script)
ROLLUP_11_TO_8 = {
    "SCRIPT_ADHERENCE": "SCRIPT_ADHERENCE",
    "ROUTING_ERRORS": "SCRIPT_ADHERENCE",
    "GARBLED_INFO": "GARBLED_INFO",
    "INAUTHENTICITY": "INAUTHENTICITY",
    "BILLING_PREDATORY": "BILLING_PREDATORY",
    "BILLING_OPAQUE": "BILLING_OPAQUE_TRAP",
    "BILLING_TRAP": "BILLING_OPAQUE_TRAP",
    "BILLING_TOO_EXPENSIVE": "BILLING_TOO_EXPENSIVE",
    "MISSED_CALLS": "MISSED_CALLS",
    "QUALITY_DECAY": "QUALITY_DECAY",
    "SERIAL_SWITCHING": "SERIAL_SWITCHING",
}

ROLLUPS = {
    11: None,  # identity
    9: ROLLUP_11_TO_9,
    8: ROLLUP_11_TO_8,
    7: ROLLUP_11_TO_7,
}

def apply_rollup(codes, rollup_map):
    if rollup_map is None:
        return codes
    return {idx: rollup_map.get(cat, cat) for idx, cat in codes.items()}

def main():
    # Load k=9 coders (actually k=11 since all 11 categories were used)
    codes_a = load_coder(os.path.join(BASE, "analysis", "coder_a_k9.json"))
    codes_b = load_coder(os.path.join(BASE, "analysis", "coder_b_k9.json"))
    common_idx = sorted(set(codes_a.keys()) & set(codes_b.keys()))

    print(f"Loaded: {len(common_idx)} common quotes\n")

    # Also load k=7 results for comparison
    codes_a_k7 = load_coder(os.path.join(BASE, "analysis", "coder_a.json"))
    codes_b_k7 = load_coder(os.path.join(BASE, "analysis", "coder_b.json"))

    print("=" * 70)
    print("KAPPA AT ALL GRANULARITY LEVELS")
    print("=" * 70)

    results = []

    # k=7 from original coding
    la7 = [codes_a_k7[i] for i in common_idx]
    lb7 = [codes_b_k7[i] for i in common_idx]
    k7, po7 = cohens_kappa(la7, lb7)
    ci7 = kappa_bootstrap_ci(la7, lb7)
    results.append(("k=7 (original)", 7, k7, po7, ci7))
    print(f"  k=7 (original coding):  κ={k7:.3f}  CI [{ci7[0]:.3f}, {ci7[1]:.3f}]  agree={po7*100:.1f}%")

    # k=11, 9, 8, 7 from new coding
    for level, rollup_map in sorted(ROLLUPS.items(), reverse=True):
        ra = apply_rollup(codes_a, rollup_map)
        rb = apply_rollup(codes_b, rollup_map)
        la = [ra[i] for i in common_idx]
        lb = [rb[i] for i in common_idx]
        k, po = cohens_kappa(la, lb)
        ci = kappa_bootstrap_ci(la, lb)
        n_cats = len(set(la) | set(lb))
        label = f"k={level} (from k11 coding)"
        results.append((label, level, k, po, ci))
        print(f"  {label}:  κ={k:.3f}  CI [{ci[0]:.3f}, {ci[1]:.3f}]  agree={po*100:.1f}%  cats={n_cats}")

    print()
    print("=" * 70)
    print("CATEGORY DISTRIBUTIONS AT k=11")
    print("=" * 70)
    dist_a = Counter(codes_a[i] for i in common_idx)
    dist_b = Counter(codes_b[i] for i in common_idx)
    all_cats = sorted(set(dist_a.keys()) | set(dist_b.keys()),
                      key=lambda c: dist_a.get(c, 0) + dist_b.get(c, 0), reverse=True)

    print(f"\n  {'Category':<25} {'Coder A':>8} {'Coder B':>8} {'Diff':>6}")
    print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*6}")
    for cat in all_cats:
        a = dist_a.get(cat, 0)
        b = dist_b.get(cat, 0)
        print(f"  {cat:<25} {a:>8} {b:>8} {abs(a-b):>6}")

    # Disagreement analysis at k=11
    disagrees = [(i, codes_a[i], codes_b[i])
                 for i in common_idx if codes_a[i] != codes_b[i]]
    print(f"\n  Disagreements at k=11: {len(disagrees)} of {len(common_idx)} ({len(disagrees)/len(common_idx)*100:.1f}%)")

    # Most common disagreement pairs
    pair_counts = Counter()
    for _, a, b in disagrees:
        pair_counts[tuple(sorted([a, b]))] += 1
    print(f"\n  Most common disagreement pairs:")
    for (a, b), count in pair_counts.most_common(10):
        print(f"    {a} vs {b}: {count}")

    print()
    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)

    # Check overlap
    all_overlap = True
    for i in range(len(results)):
        for j in range(i+1, len(results)):
            _, _, _, _, ci_i = results[i]
            _, _, _, _, ci_j = results[j]
            if not (ci_i[0] <= ci_j[1] and ci_j[0] <= ci_i[1]):
                all_overlap = False

    if all_overlap:
        print("\n  All CIs overlap → no significant difference between any levels")
    else:
        print("\n  Some CIs do NOT overlap → significant differences exist")

    best = max(results, key=lambda r: r[2])
    print(f"  Highest kappa: {best[0]} at κ={best[2]:.3f}")
    print()

if __name__ == "__main__":
    main()
