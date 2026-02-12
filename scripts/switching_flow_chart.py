#!/usr/bin/env python3
"""
Build a Sankey-style switching flow chart showing individual from→to movements.
Outputs a PNG for review.
"""

import os, math
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import numpy as np

from build_narrative import (
    load_quotes, load_coder, adjudicate, normalize_product,
    compute_weight, _detect_direction, _product_names,
    CATEGORY_META, COMPANY_ALIASES, CODER_A, CODER_B, BASE, CHART_DIR,
)

C_BLUE   = "#1B365F"
C_RED    = "#C0392B"
C_GREEN  = "#27AE60"
C_ORANGE = "#E67E22"
C_PURPLE = "#8E44AD"
C_GRAY   = "#BDC3C7"

COMP_COLORS = {
    "Ruby Receptionist": "#C0392B",
    "AnswerConnect":     "#2E75B6",
    "PATLive":           "#27AE60",
    "Smith.ai":          "#E67E22",
    "Synthflow":         "#8E44AD",
    "Abby Connect":      "#3498DB",
    "Conversational":    "#1ABC9C",
    "Dialzara":          "#F39C12",
    "SAS":               "#95A5A6",
    "Other":             "#BDC3C7",
    "In-house":          "#7F8C8D",
}


def extract_switching_pairs(quotes, final_codes):
    """Extract individual from→to pairs from switching stories."""
    switched = [(idx, quotes[idx]) for idx in final_codes
                if quotes[idx]["llm"].get("category") == "churn_switched"]

    pairs = []  # list of (from_company, to_company, quote_snippet)
    for idx, q in switched:
        prod = normalize_product(q["llm"].get("product_mentioned"))
        pain = q["llm"].get("pain_point", "")
        text = q["text"]
        is_arrival = _detect_direction(prod, pain, text)

        text_lower = text.lower()
        other_companies = set()
        for alias, canonical in COMPANY_ALIASES.items():
            if alias in text_lower and canonical != prod:
                other_companies.add(canonical)

        snippet = text.replace("\n", " ").strip()[:80]

        if is_arrival:
            # Person arrived at prod, departed from others
            if other_companies:
                for o in other_companies:
                    pairs.append((o, prod, snippet))
            else:
                pairs.append(("Unknown", prod, snippet))
        else:
            # Person departed from prod, arrived at others
            if other_companies:
                for o in other_companies:
                    pairs.append((prod, o, snippet))
            else:
                pairs.append((prod, "Unknown", snippet))

    return pairs


def build_sankey(pairs, output_path):
    """Build a Sankey-style alluvial flow diagram."""
    # Count flows
    flow_counts = Counter()
    for frm, to, _ in pairs:
        flow_counts[(frm, to)] += 1

    # Get unique companies on each side
    from_companies = sorted(set(f for f, _, _ in pairs), key=lambda x: -sum(v for (f, t), v in flow_counts.items() if f == x))
    to_companies = sorted(set(t for _, t, _ in pairs), key=lambda x: -sum(v for (f, t), v in flow_counts.items() if t == x))

    # Remove "Unknown" or put at end
    for lst in [from_companies, to_companies]:
        if "Unknown" in lst:
            lst.remove("Unknown")
            lst.append("Unknown")

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "Calibri"],
        "font.size": 10, "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.dpi": 200, "savefig.bbox": "tight", "savefig.pad_inches": 0.4,
    })

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(-0.5, 3.5)

    # Calculate y positions for nodes
    total_from = sum(flow_counts.values())
    total_to = sum(flow_counts.values())

    y_padding = 0.3
    total_height = max(len(from_companies), len(to_companies)) * 1.5

    # FROM side: stack nodes proportional to their total outflow
    from_sizes = {c: sum(v for (f, t), v in flow_counts.items() if f == c) for c in from_companies}
    from_total = sum(from_sizes.values())
    from_y = {}  # maps company → (y_center, y_height)
    y_cursor = total_height
    for c in from_companies:
        h = max(from_sizes[c] / from_total * total_height * 0.8, 0.3)
        from_y[c] = (y_cursor - h / 2, h)
        y_cursor -= h + y_padding

    # TO side: stack nodes proportional to their total inflow
    to_sizes = {c: sum(v for (f, t), v in flow_counts.items() if t == c) for c in to_companies}
    to_total = sum(to_sizes.values())
    to_y = {}
    y_cursor = total_height
    for c in to_companies:
        h = max(to_sizes[c] / to_total * total_height * 0.8, 0.3)
        to_y[c] = (y_cursor - h / 2, h)
        y_cursor -= h + y_padding

    ax.set_ylim(-1, total_height + 1)

    # Draw nodes (rectangles)
    node_width = 0.15
    x_from = 0.5
    x_to = 2.5

    for c in from_companies:
        yc, yh = from_y[c]
        color = COMP_COLORS.get(c, C_GRAY)
        rect = mpatches.FancyBboxPatch((x_from - node_width, yc - yh / 2),
                                        node_width * 2, yh,
                                        boxstyle="round,pad=0.02",
                                        facecolor=color, edgecolor="white", linewidth=1.5, alpha=0.9)
        ax.add_patch(rect)
        ax.text(x_from - node_width - 0.08, yc,
                f"{c} ({from_sizes[c]})",
                ha="right", va="center", fontsize=10, fontweight="bold", color="#333")

    for c in to_companies:
        yc, yh = to_y[c]
        color = COMP_COLORS.get(c, C_GRAY)
        rect = mpatches.FancyBboxPatch((x_to - node_width, yc - yh / 2),
                                        node_width * 2, yh,
                                        boxstyle="round,pad=0.02",
                                        facecolor=color, edgecolor="white", linewidth=1.5, alpha=0.9)
        ax.add_patch(rect)
        ax.text(x_to + node_width + 0.08, yc,
                f"{c} ({to_sizes[c]})",
                ha="left", va="center", fontsize=10, fontweight="bold", color="#333")

    # Draw flows (bezier curves)
    # Track used y-space per node to stack flows
    from_used = {c: 0.0 for c in from_companies}
    to_used = {c: 0.0 for c in to_companies}

    # Sort flows by size (largest first for cleaner visual)
    sorted_flows = sorted(flow_counts.items(), key=lambda x: -x[1])

    for (frm, to), count in sorted_flows:
        # Calculate y positions within the node
        frm_yc, frm_yh = from_y[frm]
        to_yc, to_yh = to_y[to]

        # Proportional height of this flow within the node
        frm_flow_h = count / from_sizes[frm] * frm_yh
        to_flow_h = count / to_sizes[to] * to_yh

        # Y position (stacking from top)
        y1_top = frm_yc + frm_yh / 2 - from_used[frm]
        y1_bot = y1_top - frm_flow_h
        from_used[frm] += frm_flow_h

        y2_top = to_yc + to_yh / 2 - to_used[to]
        y2_bot = y2_top - to_flow_h
        to_used[to] += to_flow_h

        # Draw filled bezier band
        color = COMP_COLORS.get(frm, C_GRAY)
        n_pts = 50
        t_vals = np.linspace(0, 1, n_pts)
        x1 = x_from + node_width
        x2 = x_to - node_width

        # Top curve
        top_x = x1 + (x2 - x1) * t_vals
        top_y = y1_top + (y2_top - y1_top) * (3 * t_vals**2 - 2 * t_vals**3)

        # Bottom curve (reversed)
        bot_x = x1 + (x2 - x1) * t_vals
        bot_y = y1_bot + (y2_bot - y1_bot) * (3 * t_vals**2 - 2 * t_vals**3)

        # Fill between
        verts_x = np.concatenate([top_x, bot_x[::-1]])
        verts_y = np.concatenate([top_y, bot_y[::-1]])
        ax.fill(verts_x, verts_y, color=color, alpha=0.35, edgecolor=color, linewidth=0.3)

        # Add count label in the middle of the flow
        mid_y = (y1_top + y1_bot + y2_top + y2_bot) / 4
        if count > 1:
            ax.text((x1 + x2) / 2, mid_y, str(count),
                    ha="center", va="center", fontsize=8, fontweight="bold",
                    color=color, alpha=0.8)

    # Labels
    ax.text(x_from, total_height + 0.5, "LEFT", ha="center", fontsize=12,
            fontweight="bold", color=C_RED)
    ax.text(x_to, total_height + 0.5, "JOINED", ha="center", fontsize=12,
            fontweight="bold", color=C_GREEN)

    ax.set_title(f"Where customers go when they leave ({len(pairs)} switching flows from {len(flow_counts)} unique paths)",
                  fontsize=13, fontweight="bold", color="#1B365F", pad=20, loc="left")

    ax.axis("off")
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved → {output_path}")


def build_matrix(pairs, output_path):
    """Build a from→to matrix heatmap showing individual flows."""
    flow_counts = Counter()
    for frm, to, _ in pairs:
        flow_counts[(frm, to)] += 1

    # Get companies sorted by total involvement
    all_companies = sorted(set(f for f, _, _ in pairs) | set(t for _, t, _ in pairs),
                           key=lambda c: -(sum(v for (f, t), v in flow_counts.items() if f == c) +
                                           sum(v for (f, t), v in flow_counts.items() if t == c)))
    # Remove unknowns for cleaner view
    all_companies = [c for c in all_companies if c != "Unknown"]

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "Calibri"],
        "font.size": 10, "figure.facecolor": "white",
        "savefig.dpi": 200, "savefig.bbox": "tight", "savefig.pad_inches": 0.4,
    })

    n = len(all_companies)
    data = np.zeros((n, n))
    for i, frm in enumerate(all_companies):
        for j, to in enumerate(all_companies):
            data[i, j] = flow_counts.get((frm, to), 0)

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(data, cmap="Blues", aspect="auto", vmin=0)

    ax.set_xticks(range(n))
    ax.set_xticklabels(all_companies, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(n))
    ax.set_yticklabels(all_companies, fontsize=9)

    ax.set_xlabel("Joined \u2192", fontsize=11, color="#27AE60", fontweight="bold")
    ax.set_ylabel("\u2190 Left", fontsize=11, color="#C0392B", fontweight="bold")

    for i in range(n):
        for j in range(n):
            v = int(data[i, j])
            if v > 0:
                c = "white" if v >= 3 else "#333"
                ax.text(j, i, str(v), ha="center", va="center",
                        fontsize=11, fontweight="bold", color=c)

    ax.set_title(f"Switching matrix: who loses customers to whom ({len(pairs)} flows)",
                  fontsize=12, fontweight="bold", color="#1B365F", pad=12, loc="left")

    plt.colorbar(im, ax=ax, label="Number of switches", shrink=0.8)
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved → {output_path}")


def main():
    quotes, _ = load_quotes()
    codes_a, codes_b = load_coder(CODER_A), load_coder(CODER_B)
    final_codes, _ = adjudicate(codes_a, codes_b)

    pairs = extract_switching_pairs(quotes, final_codes)

    print(f"Found {len(pairs)} switching flows:")
    flow_counts = Counter()
    for frm, to, _ in pairs:
        flow_counts[(frm, to)] += 1

    for (frm, to), count in sorted(flow_counts.items(), key=lambda x: -x[1]):
        print(f"  {frm:25s} → {to:25s}  ({count})")

    os.makedirs(CHART_DIR, exist_ok=True)

    # Chart 1: Sankey-style flow
    sankey_path = os.path.join(CHART_DIR, "switching_sankey.png")
    build_sankey(pairs, sankey_path)

    # Chart 2: From→To matrix
    matrix_path = os.path.join(CHART_DIR, "switching_matrix.png")
    build_matrix(pairs, matrix_path)


if __name__ == "__main__":
    main()
