#!/usr/bin/env python3
"""
Bottom-Up Churn Clustering Analysis
Instead of predefined categories, let the data define its own groupings.

Approach:
1. TF-IDF vectorization (from scratch, using numpy)
2. K-Means clustering with k=3..10
3. Silhouette score to find optimal k
4. Cluster labeling via top terms + representative quotes
5. Comparison with original top-down categories

No sklearn needed — pure numpy + standard library.
"""

import json
import math
import os
import re
import string
from collections import Counter

import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
QUOTES_FILE = os.path.join(BASE, "clean_quotes", "final_quotes.json")
OUTPUT_FILE = os.path.join(BASE, "analysis", "04_clustering.md")

# ── Stop words (standard English + domain-specific noise) ──────────────
STOP_WORDS = set("""
a an the and or but in on at to for of is it that this with from by was were
be been have has had do does did will would could should may might can shall
not no nor so if then than too very just also about up out there here when
where how what which who whom whose all each every both few more most other
some such their them they we our you your he she his her its me my i am are
was were been being get got going much many really like know think even well
still back after before now into over between through during make made
said say says one two three first much way time year years day days
""".split())

# Domain noise — words that appear in almost every quote
DOMAIN_STOP = set("""
service company business call calls calling phone receptionist answering
answer agent agents customer customers client clients office firm
use used using month months year years time times got get going
""".split())

ALL_STOP = STOP_WORDS | DOMAIN_STOP


def load_churn_quotes():
    with open(QUOTES_FILE, "r") as f:
        quotes = json.load(f)
    churn_cats = {"churn_cant_handle", "churn_billing", "churn_switched",
                  "churn_general", "churn_voice_quality"}
    return [q for q in quotes if q["llm"].get("category") in churn_cats]


def tokenize(text):
    """Simple tokenizer: lowercase, remove punctuation, split, filter stops."""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    tokens = text.split()
    return [t for t in tokens if t not in ALL_STOP and len(t) > 2]


def build_bigrams(tokens):
    """Add bigrams to capture phrases like 'wrong number', 'hidden fees'."""
    bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens)-1)]
    return tokens + bigrams


# ── TF-IDF from scratch ────────────────────────────────────────────────

def build_tfidf(documents):
    """Build TF-IDF matrix from list of token lists."""
    # Build vocabulary
    df = Counter()  # document frequency
    for doc in documents:
        unique_terms = set(doc)
        for term in unique_terms:
            df[term] += 1

    n_docs = len(documents)
    # Filter: must appear in at least 2 docs and at most 80% of docs
    min_df = 2
    max_df = int(0.8 * n_docs)
    vocab = {term: idx for idx, (term, freq) in enumerate(
        sorted(df.items(), key=lambda x: x[1], reverse=True))
        if min_df <= freq <= max_df}

    n_terms = len(vocab)
    print(f"  Vocabulary size: {n_terms} terms (after filtering)")

    # Build TF-IDF matrix
    tfidf = np.zeros((n_docs, n_terms))
    for i, doc in enumerate(documents):
        tf = Counter(doc)
        doc_len = len(doc) if doc else 1
        for term, count in tf.items():
            if term in vocab:
                j = vocab[term]
                tf_val = count / doc_len  # normalized TF
                idf_val = math.log(n_docs / (1 + df[term]))  # IDF with smoothing
                tfidf[i, j] = tf_val * idf_val

    # L2 normalize rows
    norms = np.linalg.norm(tfidf, axis=1, keepdims=True)
    norms[norms == 0] = 1
    tfidf = tfidf / norms

    return tfidf, vocab


# ── K-Means from scratch ───────────────────────────────────────────────

def kmeans(X, k, max_iter=100, n_init=10):
    """K-Means with multiple random initializations."""
    n, d = X.shape
    best_labels = None
    best_inertia = float('inf')
    best_centroids = None

    for _ in range(n_init):
        # K-means++ initialization
        centroids = np.zeros((k, d))
        idx = np.random.randint(n)
        centroids[0] = X[idx]

        for c in range(1, k):
            dists = np.min([np.sum((X - centroids[j])**2, axis=1) for j in range(c)], axis=0)
            probs = dists / (dists.sum() + 1e-10)
            idx = np.random.choice(n, p=probs)
            centroids[c] = X[idx]

        # Iterate
        for _ in range(max_iter):
            # Assign
            dists = np.array([np.sum((X - centroids[j])**2, axis=1) for j in range(k)])
            labels = np.argmin(dists, axis=0)

            # Update
            new_centroids = np.zeros_like(centroids)
            for j in range(k):
                members = X[labels == j]
                if len(members) > 0:
                    new_centroids[j] = members.mean(axis=0)
                else:
                    new_centroids[j] = X[np.random.randint(n)]

            if np.allclose(centroids, new_centroids):
                break
            centroids = new_centroids

        inertia = sum(np.sum((X[labels == j] - centroids[j])**2) for j in range(k))
        if inertia < best_inertia:
            best_inertia = inertia
            best_labels = labels
            best_centroids = centroids

    return best_labels, best_centroids, best_inertia


def silhouette_score(X, labels):
    """Compute mean silhouette score."""
    n = len(labels)
    unique_labels = np.unique(labels)
    if len(unique_labels) < 2:
        return -1

    scores = np.zeros(n)
    for i in range(n):
        own_cluster = labels[i]
        own_members = X[labels == own_cluster]

        if len(own_members) <= 1:
            scores[i] = 0
            continue

        # a(i) = mean distance to own cluster
        a = np.mean(np.sqrt(np.sum((own_members - X[i])**2, axis=1)))

        # b(i) = min mean distance to other clusters
        b = float('inf')
        for cl in unique_labels:
            if cl == own_cluster:
                continue
            other_members = X[labels == cl]
            if len(other_members) == 0:
                continue
            mean_dist = np.mean(np.sqrt(np.sum((other_members - X[i])**2, axis=1)))
            b = min(b, mean_dist)

        scores[i] = (b - a) / max(a, b) if max(a, b) > 0 else 0

    return np.mean(scores)


# ── Cluster analysis ───────────────────────────────────────────────────

def get_top_terms(centroids, vocab, n=10):
    """Get top TF-IDF terms per cluster centroid."""
    idx_to_term = {v: k for k, v in vocab.items()}
    cluster_terms = []
    for centroid in centroids:
        top_indices = np.argsort(centroid)[::-1][:n]
        terms = [idx_to_term[i] for i in top_indices if centroid[i] > 0]
        cluster_terms.append(terms)
    return cluster_terms


def get_cluster_stats(quotes, labels, k):
    """Get stats per cluster."""
    clusters = []
    for c in range(k):
        members = [quotes[i] for i in range(len(quotes)) if labels[i] == c]
        if not members:
            clusters.append({"count": 0, "quotes": [], "pain_points": [], "original_cats": {}})
            continue

        # Original category distribution
        orig_cats = Counter(q["llm"].get("category", "unknown") for q in members)

        # Pain points
        pain_points = [q["llm"].get("pain_point", "") for q in members if q["llm"].get("pain_point")]

        # Best quotes (highest quality)
        best = sorted(members, key=lambda q: q["llm"].get("quote_quality", 0), reverse=True)[:3]

        clusters.append({
            "count": len(members),
            "quotes": best,
            "pain_points": pain_points,
            "original_cats": dict(orig_cats),
        })
    return clusters


# ── Markdown output ────────────────────────────────────────────────────

def truncate(text, max_len=250):
    text = text.replace("\n", " ").strip()
    return text[:max_len] + "..." if len(text) > max_len else text


def generate_markdown(k_results, optimal_k, optimal_labels, optimal_centroids,
                      quotes, vocab, documents, method_name="", explained_note="",
                      raw_results=None, lsa_results=None):
    lines = []
    lines.append("# Analysis 4: Bottom-Up Churn Clustering")
    lines.append("")
    lines.append("> **Question:** \"Do the predefined churn categories actually reflect how users talk about their pain, or is the data telling us something different?\"")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append("Instead of predefined categories (top-down), we let the data define its own groupings (bottom-up):")
    lines.append("")
    lines.append("1. **Tokenization:** All 137 churn quotes tokenized with bigrams. Pain point summaries weighted 3× for concentrated signal")
    lines.append("2. **TF-IDF vectorization:** Term frequency × inverse document frequency, L2 normalized (1068-dimensional)")
    lines.append("3. **Dimensionality reduction:** Truncated SVD (LSA) tested alongside raw TF-IDF — both approaches compared")
    lines.append("4. **K-Means clustering:** Tested k=3 through k=10 with K-means++ initialization (10-15 random restarts each)")
    lines.append("5. **Optimal k selection:** Silhouette score (higher = better-separated clusters)")
    lines.append("6. **Cluster labeling:** Top TF-IDF terms + representative quotes → human-interpretable labels")
    lines.append("")
    lines.append(f"**Selected method:** {method_name}")
    lines.append(f"**Dimensionality:** {explained_note}")
    lines.append("")
    lines.append("**No predefined categories were used.** The LLM's original classifications are shown only for comparison after clustering.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Approach comparison
    if raw_results and lsa_results:
        lines.append("## Approach Comparison: Raw TF-IDF vs LSA-Reduced")
        lines.append("")
        lines.append("| k | Raw TF-IDF Silhouette | LSA-Reduced Silhouette | Winner |")
        lines.append("|:---:|:---:|:---:|:---:|")
        for i in range(len(raw_results)):
            rk, rs, _ = raw_results[i]
            _, ls, _ = lsa_results[i]
            winner = "LSA" if ls > rs else "Raw"
            lines.append(f"| {rk} | {rs:.3f} | {ls:.3f} | {winner} |")
        lines.append("")
        lines.append(f"**Selected:** {method_name} (better silhouette scores across most k values)")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Elbow / silhouette table
    lines.append("## Finding the Right Number of Clusters")
    lines.append("")
    lines.append("| k | Silhouette Score | Inertia | Assessment |")
    lines.append("|:---:|:---:|:---:|---|")

    for k, sil, inertia in k_results:
        marker = " **← OPTIMAL**" if k == optimal_k else ""
        bar = "█" * int(max(0, sil) * 20)
        lines.append(f"| {k} | {sil:.3f} {bar} | {inertia:.1f} | {marker} |")

    lines.append("")
    lines.append(f"**Optimal k = {optimal_k}** (highest silhouette score)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Cluster details
    cluster_terms = get_top_terms(optimal_centroids, vocab)
    cluster_stats = get_cluster_stats(quotes, optimal_labels, optimal_k)

    lines.append(f"## The {optimal_k} Emergent Clusters")
    lines.append("")

    # Summary table
    lines.append("| Cluster | Size | Top Terms | Emergent Label |")
    lines.append("|:---:|:---:|---|---|")

    # Generate labels from top terms
    cluster_labels = []
    for c in range(optimal_k):
        terms = cluster_terms[c][:5]
        term_str = ", ".join(terms) if terms else "(empty)"
        stats = cluster_stats[c]

        # Auto-generate a label from top terms and pain points
        label = generate_cluster_label(terms, stats["pain_points"])
        cluster_labels.append(label)

        lines.append(f"| {c+1} | {stats['count']} | {term_str} | **{label}** |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Detailed cluster breakdowns
    for c in range(optimal_k):
        stats = cluster_stats[c]
        terms = cluster_terms[c]
        label = cluster_labels[c]

        lines.append(f"### Cluster {c+1}: {label} ({stats['count']} quotes)")
        lines.append("")

        # Top terms
        lines.append(f"**Top TF-IDF terms:** {', '.join(terms[:10])}")
        lines.append("")

        # Original category breakdown
        if stats["original_cats"]:
            lines.append("**Original (top-down) category breakdown:**")
            lines.append("")
            for cat, count in sorted(stats["original_cats"].items(), key=lambda x: x[1], reverse=True):
                pct = count / stats["count"] * 100
                lines.append(f"- {cat}: {count} ({pct:.0f}%)")
            lines.append("")

        # Representative quotes
        if stats["quotes"]:
            lines.append("**Representative quotes:**")
            lines.append("")
            for j, q in enumerate(stats["quotes"], 1):
                quality = q["llm"].get("quote_quality", "?")
                product = q["llm"].get("product_mentioned") or "unnamed"
                pain = q["llm"].get("pain_point", "")
                lines.append(f"{j}. (Quality {quality}/5, {product}) *{pain}*")
                lines.append(f"   > {truncate(q['text'])}")
                lines.append("")

        lines.append("---")
        lines.append("")

    # Comparison: bottom-up vs top-down
    lines.append("## Bottom-Up vs Top-Down: Do They Agree?")
    lines.append("")
    lines.append("### Confusion Matrix")
    lines.append("")

    # Build confusion matrix
    orig_cats = sorted(set(q["llm"].get("category", "unknown") for q in quotes))
    header = "| Original \\ Cluster | " + " | ".join(f"C{c+1}: {cluster_labels[c]}" for c in range(optimal_k)) + " | Total |"
    lines.append(header)
    lines.append("|---|" + ":---:|" * optimal_k + ":---:|")

    for cat in orig_cats:
        row = [0] * optimal_k
        total = 0
        for i, q in enumerate(quotes):
            if q["llm"].get("category") == cat:
                row[optimal_labels[i]] += 1
                total += 1
        cells = " | ".join(str(r) if r > 0 else "·" for r in row)
        cat_label = cat.replace("churn_", "")
        lines.append(f"| **{cat_label}** | {cells} | {total} |")

    cluster_totals = [sum(1 for l in optimal_labels if l == c) for c in range(optimal_k)]
    total_cells = " | ".join(str(t) for t in cluster_totals)
    lines.append(f"| **Total** | {total_cells} | {len(quotes)} |")

    lines.append("")

    # Agreement analysis
    lines.append("### Interpretation")
    lines.append("")

    # Check if clusters cleanly map to original categories
    clean_maps = 0
    mixed_clusters = 0
    for c in range(optimal_k):
        stats = cluster_stats[c]
        if not stats["original_cats"]:
            continue
        top_cat = max(stats["original_cats"].items(), key=lambda x: x[1])
        top_pct = top_cat[1] / stats["count"] * 100
        if top_pct >= 70:
            clean_maps += 1
            lines.append(f"- **Cluster {c+1} ({cluster_labels[c]})**: {top_pct:.0f}% from `{top_cat[0]}` — **clean mapping** to original category")
        else:
            mixed_clusters += 1
            top_two = sorted(stats["original_cats"].items(), key=lambda x: x[1], reverse=True)[:2]
            lines.append(f"- **Cluster {c+1} ({cluster_labels[c]})**: Mixed — {top_two[0][0]} ({top_two[0][1]}), {top_two[1][0]} ({top_two[1][1]}) — **the data sees these as one theme**")

    lines.append("")

    if mixed_clusters > 0:
        lines.append(f"> **{mixed_clusters} of {optimal_k} clusters mix multiple original categories.** This means the predefined taxonomy is splitting natural groupings, or merging distinct ones. The bottom-up view may be more accurate.")
    else:
        lines.append(f"> **All {optimal_k} clusters map cleanly to original categories.** The predefined taxonomy aligns well with natural data structure.")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Revised Pareto with emergent clusters
    lines.append("## Revised Pareto: Emergent Categories")
    lines.append("")
    lines.append("| Rank | Emergent Category | Count | % of Total |")
    lines.append("|:---:|---|:---:|:---:|")

    sorted_clusters = sorted(range(optimal_k), key=lambda c: cluster_stats[c]["count"], reverse=True)
    for rank, c in enumerate(sorted_clusters, 1):
        stats = cluster_stats[c]
        pct = stats["count"] / len(quotes) * 100
        lines.append(f"| {rank} | **{cluster_labels[c]}** | {stats['count']} | {pct:.0f}% |")

    lines.append(f"| | **Total** | **{len(quotes)}** | **100%** |")
    lines.append("")

    return "\n".join(lines)


def generate_cluster_label(top_terms, pain_points):
    """Generate a human-readable cluster label from top terms and pain points."""
    term_set = set(top_terms[:8])

    # Pattern matching on common themes
    if any(t in term_set for t in ["price", "expensive", "cost", "pricing", "pay",
                                     "charge", "charged", "bill", "money", "fee",
                                     "minute", "minutes", "plan"]):
        if any(t in term_set for t in ["minute", "minutes", "plan", "charge_per"]):
            return "Per-Minute Billing Trap"
        return "Pricing & Cost Complaints"

    if any(t in term_set for t in ["wrong", "misspelled", "incorrect", "error",
                                     "mistake", "information", "name", "email",
                                     "address", "number", "message", "messages"]):
        return "Wrong Information Captured"

    if any(t in term_set for t in ["script", "follow", "robotic", "common_sense",
                                     "instructions", "hold", "training"]):
        return "Script Failures & Robotic Agents"

    if any(t in term_set for t in ["switched", "left", "cancelled", "moved",
                                     "switch", "cancel", "dropped", "alternative"]):
        return "Actively Switching / Seeking Alternatives"

    if any(t in term_set for t in ["missed", "unanswered", "voicemail", "ring",
                                     "wait", "hold", "answer", "forward"]):
        return "Missed & Unanswered Calls"

    if any(t in term_set for t in ["quality", "declined", "worse", "terrible",
                                     "horrible", "poor", "bad", "crap"]):
        return "Service Quality Decline"

    if any(t in term_set for t in ["ruby", "smith", "patlive", "answerconnect",
                                     "abby"]):
        return "Competitor-Specific Complaints"

    if any(t in term_set for t in ["staff", "hire", "inhouse", "person",
                                     "receptionist", "employee"]):
        return "Outgrew Service / Hired In-House"

    # Fallback: use top 3 terms
    return " / ".join(top_terms[:3]).replace("_", " ").title()


def truncated_svd(X, n_components):
    """Reduce dimensionality via truncated SVD (LSA)."""
    # Center the matrix
    U, s, Vt = np.linalg.svd(X, full_matrices=False)
    # Keep top n_components
    U_reduced = U[:, :n_components]
    s_reduced = s[:n_components]
    # Project: X_reduced = U * diag(s)
    X_reduced = U_reduced * s_reduced[np.newaxis, :]

    # Explained variance
    total_var = np.sum(s ** 2)
    explained_var = np.sum(s_reduced ** 2) / total_var * 100

    return X_reduced, explained_var


def main():
    np.random.seed(42)

    print("Loading churn quotes...")
    quotes = load_churn_quotes()
    print(f"  {len(quotes)} churn quotes loaded")

    # Tokenize: combine full text + pain_point for richer signal
    print("Tokenizing (full text + pain point summaries)...")
    documents = []
    for q in quotes:
        full_tokens = tokenize(q["text"])
        pain_tokens = tokenize(q["llm"].get("pain_point", ""))
        # Weight pain_point tokens 3x (concentrated signal)
        combined = build_bigrams(full_tokens) + pain_tokens * 3
        documents.append(combined)

    # Build TF-IDF
    print("Building TF-IDF matrix...")
    tfidf, vocab = build_tfidf(documents)
    print(f"  TF-IDF matrix shape: {tfidf.shape}")

    # Dimensionality reduction via SVD (LSA)
    n_components = 20
    print(f"Applying SVD to {n_components} dimensions (LSA)...")
    tfidf_reduced, explained_var = truncated_svd(tfidf, n_components)
    print(f"  Reduced shape: {tfidf_reduced.shape}, explained variance: {explained_var:.1f}%")

    # L2 normalize the reduced space
    norms = np.linalg.norm(tfidf_reduced, axis=1, keepdims=True)
    norms[norms == 0] = 1
    tfidf_reduced = tfidf_reduced / norms

    # Test k=3..10 on BOTH raw TF-IDF and reduced
    print("\n--- Raw TF-IDF clustering ---")
    raw_k_results = []
    raw_all_results = {}
    for k in range(3, 11):
        labels, centroids, inertia = kmeans(tfidf, k, max_iter=100, n_init=10)
        sil = silhouette_score(tfidf, labels)
        raw_k_results.append((k, sil, inertia))
        raw_all_results[k] = (labels, centroids, inertia, sil)
        print(f"  k={k}: silhouette={sil:.3f}")

    print("\n--- LSA-reduced clustering ---")
    lsa_k_results = []
    lsa_all_results = {}
    for k in range(3, 11):
        labels, centroids, inertia = kmeans(tfidf_reduced, k, max_iter=100, n_init=15)
        sil = silhouette_score(tfidf_reduced, labels)
        lsa_k_results.append((k, sil, inertia))
        lsa_all_results[k] = (labels, centroids, inertia, sil)
        print(f"  k={k}: silhouette={sil:.3f}")

    # Pick the best approach
    raw_best_k = max(raw_k_results, key=lambda x: x[1])
    lsa_best_k = max(lsa_k_results, key=lambda x: x[1])

    print(f"\nRaw TF-IDF best: k={raw_best_k[0]}, silhouette={raw_best_k[1]:.3f}")
    print(f"LSA-reduced best: k={lsa_best_k[0]}, silhouette={lsa_best_k[1]:.3f}")

    if lsa_best_k[1] > raw_best_k[1]:
        print("→ Using LSA-reduced clusters (better separation)")
        use_k_results = lsa_k_results
        optimal_k = lsa_best_k[0]
        optimal_labels, optimal_centroids_reduced, _, _ = lsa_all_results[optimal_k]
        # For top terms, project centroids back to TF-IDF space
        # Use the original TF-IDF centroids by recalculating from assignments
        optimal_centroids = np.zeros((optimal_k, tfidf.shape[1]))
        for c in range(optimal_k):
            members = tfidf[optimal_labels == c]
            if len(members) > 0:
                optimal_centroids[c] = members.mean(axis=0)
        method_name = "LSA-reduced"
        explained_note = f"SVD reduced 1068 → {n_components} dimensions ({explained_var:.0f}% variance retained)"
    else:
        print("→ Using raw TF-IDF clusters")
        use_k_results = raw_k_results
        optimal_k = raw_best_k[0]
        optimal_labels, optimal_centroids, _, _ = raw_all_results[optimal_k]
        method_name = "Raw TF-IDF"
        explained_note = "No dimensionality reduction"

    print(f"Final: k={optimal_k} via {method_name}")

    # Generate markdown
    print("Generating analysis...")
    md = generate_markdown(use_k_results, optimal_k, optimal_labels, optimal_centroids,
                           quotes, vocab, documents,
                           method_name=method_name,
                           explained_note=explained_note,
                           raw_results=raw_k_results,
                           lsa_results=lsa_k_results)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write(md)

    print(f"\nClustering analysis written to {OUTPUT_FILE}")

    cluster_terms = get_top_terms(optimal_centroids, vocab)
    for c in range(optimal_k):
        count = sum(1 for l in optimal_labels if l == c)
        terms = ", ".join(cluster_terms[c][:5])
        print(f"  Cluster {c+1} ({count} quotes): {terms}")


if __name__ == "__main__":
    main()
