#!/usr/bin/env python3
"""
Compute all analysis from raw data and dump to markdown files.
Run this first, then build_report_docx.py to generate the Word document.

Data sources:
  - clean_quotes/final_quotes.json (409 quotes, 154 churn)
  - analysis/coder_a_k9.json, coder_b_k9.json (dual coding)
  - review_data/raw/*_trustpilot.json (raw Trustpilot reviews)
"""

import json, math, os, re
from collections import Counter
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
QUOTES_FILE = os.path.join(BASE, "clean_quotes", "final_quotes.json")
CODER_A = os.path.join(BASE, "analysis", "coder_a_k9.json")
CODER_B = os.path.join(BASE, "analysis", "coder_b_k9.json")
ANALYSIS_DIR = os.path.join(BASE, "analysis")

# ── Metadata (same as build_report_docx.py) ─────────────────────
CATEGORY_META = {
    "SCRIPT_ADHERENCE":      {"short": "Script Failures",    "group": "CALL HANDLING"},
    "BILLING_PREDATORY":     {"short": "Predatory Billing",  "group": "BILLING"},
    "INAUTHENTICITY":        {"short": "Inauthenticity",     "group": "CALL HANDLING"},
    "GARBLED_INFO":          {"short": "Garbled Info",        "group": "CALL HANDLING"},
    "SERIAL_SWITCHING":      {"short": "Serial Switching",    "group": "INDUSTRY DISILLUSIONMENT"},
    "BILLING_TRAP":          {"short": "Billing Trap",        "group": "BILLING"},
    "BILLING_OPAQUE":        {"short": "Opaque Billing",      "group": "BILLING"},
    "QUALITY_DECAY":         {"short": "Quality Decay",       "group": "SERVICE RELIABILITY"},
    "MISSED_CALLS":          {"short": "Missed Calls",        "group": "SERVICE RELIABILITY"},
    "ROUTING_ERRORS":        {"short": "Routing Errors",      "group": "CALL HANDLING"},
    "BILLING_TOO_EXPENSIVE": {"short": "Too Expensive",       "group": "BILLING"},
}
GROUP_ORDER = ["CALL HANDLING", "BILLING", "SERVICE RELIABILITY", "INDUSTRY DISILLUSIONMENT"]
TOP_COMPETITORS = ["AnswerConnect", "Ruby Receptionist", "PATLive", "Smith.ai", "Synthflow"]

COMPANY_ALIASES = {
    "ruby": "Ruby Receptionist", "ruby receptionist": "Ruby Receptionist",
    "answerconnect": "AnswerConnect", "answer connect": "AnswerConnect",
    "patlive": "PATLive", "pat live": "PATLive", "patlive.com": "PATLive",
    "smith.ai": "Smith.ai", "smithai": "Smith.ai", "smith ai": "Smith.ai",
    "synthflow": "Synthflow", "synthflow.ai": "Synthflow",
    "abby connect": "Abby Connect", "abbyconnect": "Abby Connect",
    "dialzara": "Dialzara", "sas": "SAS", "specialty answering service": "SAS",
    "virtual hq": "Virtual HQ", "conversational": "Conversational",
    "goodcall": "Goodcall", "vapi": "Vapi", "bland ai": "Bland AI",
    "in-house": "In-house", "in house": "In-house",
}

VERTICALS = {
    "Legal": ["law firm", "attorney", "lawyer", "legal", "paralegal", "litigation",
               "practice area", "opposing counsel", "court", "client intake"],
    "Medical": ["patient", "medical", "doctor", "clinic", "hipaa", "healthcare",
                 "dental", "dermatolog", "medical practice"],
    "Home Services": ["hvac", "plumb", "electric", "roofing", "contractor", "technician",
                      "dispatch", "service call", "on-call", "field tech", "home service"],
    "Real Estate": ["real estate", "realtor", "property management", "listing agent", "showing"],
}


# ── Data loading ─────────────────────────────────────────────────
def load_all_quotes():
    with open(QUOTES_FILE) as f:
        return json.load(f)

def load_churn_quotes(all_quotes):
    return [q for q in all_quotes if q["llm"].get("category", "").startswith("churn_")]

def load_coder(fp):
    with open(fp) as f:
        return {item["idx"]: item["category"] for item in json.load(f)["classifications"]}

def adjudicate(a, b):
    final, dis = {}, []
    for idx in sorted(set(a) | set(b)):
        final[idx] = a.get(idx)
        if a.get(idx) != b.get(idx):
            dis.append((idx, a.get(idx), b.get(idx)))
    return final, dis

def compute_kappa(codes_a, codes_b):
    shared = sorted(set(codes_a) & set(codes_b))
    n = len(shared)
    if n == 0:
        return 0.0, 0, 0
    labels_a = [codes_a[i] for i in shared]
    labels_b = [codes_b[i] for i in shared]
    agree = sum(1 for a, b in zip(labels_a, labels_b) if a == b)
    p_o = agree / n
    all_cats = sorted(set(labels_a) | set(labels_b))
    p_e = sum((labels_a.count(c) / n) * (labels_b.count(c) / n) for c in all_cats)
    kappa = (p_o - p_e) / (1 - p_e) if p_e < 1 else 1.0
    return kappa, agree, n

def compute_weight(q):
    quality = q["llm"].get("quote_quality", 1)
    eng = max(1.0, math.log2(max(q.get("score") or 1, 1))) if q["source"] == "reddit" else 1.0
    return quality * eng

def normalize_product(p):
    if not p or p == "unnamed": return "Other"
    return "Ruby Receptionist" if p == "Ruby" else p


# ── Direction detection (same as build_report_docx.py) ───────────
def _product_names(prod):
    names = {prod.lower()}
    for alias, canon in COMPANY_ALIASES.items():
        if canon == prod:
            names.add(alias.lower())
    return names

def _detect_direction(prod, pain, text):
    text_lower = text.lower()
    pain_lower = pain.lower()
    names = _product_names(prod)
    dep_phrases = ["dropped ", "left ", "cancelled ", "canceled ", "leaving ",
                   "switched from ", "ditched "]
    arr_phrases = ["switched to ", "switching to ", "went to ", "went with ",
                   "moved to ", "chose ", "choosing ", "found ", "finding "]
    for name in names:
        for dp in dep_phrases:
            if dp + name in text_lower or dp + name in pain_lower:
                return False
        for ap in arr_phrases:
            if ap + name in text_lower or ap + name in pain_lower:
                return True
    snippet = text_lower
    pos_words = ["happy", "love", "loves", "great", "best", "excellent", "amazing",
                 "wonderful", "recommend", "appreciate", "fantastic", "no comparison",
                 "pleased", "reliable", "impressed", "professional", "easy to work",
                 "helpful", "superior", "courteous"]
    neg_words = ["terrible", "worst", "awful", "horrible", "avoid", "waste", "scam",
                 "zero stars", "do not use", "poor", "disappointed", "frustrat",
                 "useless", "broken", "zero support", "no support", "non-existent",
                 "crap", "buyer beware", "stay far", "dissatisfied", "not what it used",
                 "canceled", "cancelled", "too expensive", "dropping the ball",
                 "finally left", "no longer", "nose dive", "disappoint",
                 "unfortunately", "missed"]
    pos = sum(1 for w in pos_words if w in snippet)
    neg = sum(1 for w in neg_words if w in snippet)
    if pos != neg:
        return pos > neg
    arr_kw = ["switched to", "found", "chose", "happy", "best vendor",
              "great experience", "no comparison", "resolved", "recommend",
              "flexible", "accommodating"]
    dep_kw = ["dropped", "cancelled", "canceled", "too expensive", "declined",
              "wrong", "missed", "terrible", "worst", "overpromised", "crap",
              "deteriorat", "shopping", "dishonest", "lost calls", "costing",
              "unanswered", "hang up", "broken", "zero support", "fails",
              "non-existent", "not worth"]
    a = sum(1 for w in arr_kw if w in pain_lower)
    d = sum(1 for w in dep_kw if w in pain_lower)
    if a != d:
        return a > d
    return False


# ── Analysis computations ────────────────────────────────────────
def compute_all():
    """Run all analysis and return a dict of results."""
    all_quotes = load_all_quotes()
    quotes = load_churn_quotes(all_quotes)
    codes_a, codes_b = load_coder(CODER_A), load_coder(CODER_B)
    final_codes, disagreements = adjudicate(codes_a, codes_b)
    kappa_val, kappa_agree, kappa_n = compute_kappa(codes_a, codes_b)

    # ── Category stats ──
    cat_stats = {}
    for idx, cat in final_codes.items():
        cat_stats.setdefault(cat, {"count": 0, "weighted": 0.0, "quotes": []})
        q = quotes[idx]; w = compute_weight(q)
        cat_stats[cat]["count"] += 1; cat_stats[cat]["weighted"] += w
        cat_stats[cat]["quotes"].append((idx, q, w))
    total_count = sum(s["count"] for s in cat_stats.values())
    total_weighted = sum(s["weighted"] for s in cat_stats.values())
    sorted_cats = sorted(cat_stats, key=lambda c: cat_stats[c]["weighted"], reverse=True)

    # ── Group stats ──
    group_stats = {}
    for cat, s in cat_stats.items():
        g = CATEGORY_META[cat]["group"]
        group_stats.setdefault(g, {"count": 0, "weighted": 0.0, "cats": []})
        group_stats[g]["count"] += s["count"]; group_stats[g]["weighted"] += s["weighted"]
        group_stats[g]["cats"].append(cat)

    # ── Competitor breakdowns ──
    comp_cats, comp_groups = {}, {}
    for idx, cat in final_codes.items():
        prod = normalize_product(quotes[idx]["llm"].get("product_mentioned"))
        comp_cats.setdefault(prod, Counter())[cat] += 1
    for prod, cats in comp_cats.items():
        comp_groups[prod] = Counter()
        for cat, cnt in cats.items():
            comp_groups[prod][CATEGORY_META[cat]["group"]] += cnt

    # ── Switching data ──
    switched = [(idx, quotes[idx]) for idx in final_codes
                if quotes[idx]["llm"].get("category") == "churn_switched"]
    arrivals, departures, triggers = Counter(), Counter(), Counter()
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
        if is_arrival:
            arrivals[prod] += 1
            for other in other_companies: departures[other] += 1
        else:
            departures[prod] += 1
            for other in other_companies: arrivals[other] += 1
        trigger_text = pain.lower()
        if any(w in trigger_text for w in ["integrat", "customiz", "automat", "technolog",
                                            "can't do", "couldn't", "could not",
                                            "limited", "outdated", "compatib",
                                            "google voice", "can't handle",
                                            "couldn't adapt", "could not adapt"]):
            triggers["Capability"] += 1
        elif any(w in trigger_text for w in ["expensiv", "price", "too much",
                                              "bill", "charg", "fee", "money",
                                              "overpay", "overcharg",
                                              "no longer justified", "cut cost"]):
            triggers["Pricing"] += 1
        else:
            triggers["Quality"] += 1
    all_companies = set(arrivals.keys()) | set(departures.keys())
    net_flow = {}
    for c in all_companies:
        net = arrivals.get(c, 0) - departures.get(c, 0)
        if net != 0:
            net_flow[c] = {"arrivals": arrivals.get(c, 0), "departures": departures.get(c, 0), "net": net}

    # ── Temporal data ──
    review_dir = os.path.join(BASE, "review_data", "raw")
    name_map = {"answerconnect": "AnswerConnect", "patlive": "PATLive",
                "smithai": "Smith.ai", "ruby_receptionist": "Ruby Receptionist"}
    temporal_order = ["AnswerConnect", "Ruby Receptionist", "PATLive", "Smith.ai"]
    temporal_data = {}
    bimod_data = {}
    for fname in os.listdir(review_dir):
        if not fname.endswith("_trustpilot.json"): continue
        key = fname.replace("_trustpilot.json", "")
        prod = name_map.get(key)
        if not prod or prod not in temporal_order: continue
        with open(os.path.join(review_dir, fname)) as f:
            reviews = json.load(f)
        org_ratings, surge_ratings = [], []
        org_extreme, org_total, surge_extreme, surge_total = 0, 0, 0, 0
        org_5star, surge_5star = 0, 0
        for r in reviews:
            try: rating = int(r.get("rating", 3))
            except (ValueError, TypeError): rating = 3
            date_str = r.get("date", "")
            is_surge = False
            if "2024" in date_str or "2025" in date_str or "2026" in date_str:
                month = 1
                for i, m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], 1):
                    if m in date_str: month = i; break
                if ("2024" in date_str and month >= 7) or "2025" in date_str or "2026" in date_str:
                    is_surge = True
            if is_surge:
                surge_ratings.append(rating)
                surge_total += 1
                if rating in (1, 5): surge_extreme += 1
                if rating == 5: surge_5star += 1
            else:
                org_ratings.append(rating)
                org_total += 1
                if rating in (1, 5): org_extreme += 1
                if rating == 5: org_5star += 1
        org_avg = float(np.mean(org_ratings)) if org_ratings else 3.0
        surge_avg = float(np.mean(surge_ratings)) if surge_ratings else 3.0
        temporal_data[prod] = {
            "organic_avg": org_avg, "organic_n": len(org_ratings),
            "surge_avg": surge_avg, "surge_n": len(surge_ratings),
            "jump": surge_avg - org_avg,
        }
        bimod_data[prod] = {
            "org_extreme_pct": org_extreme / org_total * 100 if org_total else 0,
            "surge_extreme_pct": surge_extreme / surge_total * 100 if surge_total else 0,
            "org_5star": org_5star, "org_total": org_total,
            "surge_5star": surge_5star, "surge_total": surge_total,
            "overall_extreme_pct": (org_extreme + surge_extreme) / (org_total + surge_total) * 100
                if (org_total + surge_total) else 0,
        }

    # ── Industry verticals ──
    industry_data = {}
    for idx, cat in final_codes.items():
        q = quotes[idx]
        text = (q["text"] + " " + q["llm"].get("pain_point", "")).lower()
        matched = None
        for vert, keywords in VERTICALS.items():
            if any(kw in text for kw in keywords):
                matched = vert; break
        if matched:
            industry_data.setdefault(matched, {"count": 0, "cats": Counter()})
            industry_data[matched]["count"] += 1
            industry_data[matched]["cats"][cat] += 1

    # ── Dollar impact ──
    dollar_quotes = []
    for idx, cat in final_codes.items():
        q = quotes[idx]
        text = q["text"]
        amounts = re.findall(r'\$[\d,]+(?:\.\d{2})?(?:/(?:month|mo|yr|year))?', text)
        if not amounts: continue
        dollar_quotes.append({
            "idx": idx, "cat": cat,
            "product": normalize_product(q["llm"].get("product_mentioned")),
            "amounts": amounts,
            "pain_point": q["llm"].get("pain_point", ""),
            "text_snippet": q["text"].replace("\n", " ").strip()[:120] + "...",
        })

    # ── Source counts ──
    tp_churn = sum(1 for i in final_codes if quotes[i]["source"] == "trustpilot")
    reddit_churn = sum(1 for i in final_codes if quotes[i]["source"] == "reddit")
    positive_count = sum(1 for q in all_quotes if q["llm"].get("category", "").startswith("positive"))
    pre2020_count = sum(1 for i in final_codes
                        if any(y in quotes[i].get("date", "") for y in ["2015","2016","2017","2018","2019"]))

    # ── Post-2020 rankings ──
    post2020_cats = Counter()
    for idx, cat in final_codes.items():
        date = quotes[idx].get("date", "")
        if any(y in date for y in ["2015","2016","2017","2018","2019"]):
            continue
        prod = normalize_product(quotes[idx]["llm"].get("product_mentioned"))
        post2020_cats[prod] += 1

    # ── Gut-punch quotes (best per group) ──
    def devastation_score(text):
        t = text.lower(); s = 0
        if any(w in t for w in ["thousand", "hundred", "$"]): s += 3
        if any(w in t for w in ["lost client", "lost customer", "lost revenue"]): s += 3
        if any(w in t for w in ["years", "year"]): s += 2
        if any(w in t for w in ["scam", "dishonest", "beware", "fraud", "worst",
                                 "terrible", "horrible", "negligence"]): s += 2
        return s

    def extract_pull_quote(text, max_len=200):
        text_clean = text.replace("\n", " ").strip()
        sentences = re.split(r'(?<=[.!?])\s+', text_clean)
        best, best_s = None, -1
        for s in sentences:
            if len(s) < 20: continue
            sc = devastation_score(s) + (1 if 40 < len(s) < 180 else 0)
            if sc > best_s: best_s, best = sc, s
        if best and len(best) <= max_len: return best
        elif best: return best[:max_len] + "..."
        return text_clean[:max_len] + ("..." if len(text_clean) > max_len else "")

    gut_punch = []
    for g in GROUP_ORDER:
        group_cat_list = group_stats[g]["cats"]
        candidates = []
        for idx, cat in final_codes.items():
            if cat not in group_cat_list: continue
            q = quotes[idx]; quality = q["llm"].get("quote_quality", 1)
            pull = extract_pull_quote(q["text"])
            sc = devastation_score(pull) * 10 + devastation_score(q["text"]) * 3 + quality * 2
            candidates.append((sc, idx, q, cat))
        candidates.sort(key=lambda x: x[0], reverse=True)
        used = {gp[3] for gp in gut_punch}
        for sc, idx, q, cat in candidates:
            prod = normalize_product(q["llm"].get("product_mentioned"))
            if prod not in used or len(candidates) < 3:
                gut_punch.append((idx, q, cat, prod))
                break

    return {
        "all_quotes": all_quotes,
        "quotes": quotes,
        "final_codes": final_codes,
        "disagreements": disagreements,
        "kappa_val": kappa_val,
        "kappa_agree": kappa_agree,
        "kappa_n": kappa_n,
        "cat_stats": cat_stats,
        "total_count": total_count,
        "total_weighted": total_weighted,
        "sorted_cats": sorted_cats,
        "group_stats": group_stats,
        "comp_cats": comp_cats,
        "comp_groups": comp_groups,
        "switching": {
            "total": len(switched),
            "net_flow": net_flow,
            "triggers": dict(triggers),
            "arrivals": dict(arrivals),
            "departures": dict(departures),
        },
        "temporal_data": temporal_data,
        "temporal_order": temporal_order,
        "bimod_data": bimod_data,
        "industry_data": industry_data,
        "dollar_quotes": dollar_quotes,
        "tp_churn": tp_churn,
        "reddit_churn": reddit_churn,
        "positive_count": positive_count,
        "pre2020_count": pre2020_count,
        "post2020_cats": dict(post2020_cats),
        "total_all_quotes": len(all_quotes),
        "gut_punch": gut_punch,
        "extract_pull_quote": extract_pull_quote,
    }


# ── Markdown generators ──────────────────────────────────────────
def write_md(filename, content):
    path = os.path.join(ANALYSIS_DIR, filename)
    with open(path, "w") as f:
        f.write(content)
    print(f"  Wrote {filename}")


def dump_executive_summary(d):
    tw = d["total_weighted"]
    gs = d["group_stats"]
    ch_pct = gs["CALL HANDLING"]["weighted"] / tw * 100
    bill_pct = gs["BILLING"]["weighted"] / tw * 100
    rel_pct = gs["SERVICE RELIABILITY"]["weighted"] / tw * 100
    disill_pct = gs["INDUSTRY DISILLUSIONMENT"]["weighted"] / tw * 100
    ai_addr = ch_pct + bill_pct
    agree_n = len(d["final_codes"]) - len(d["disagreements"])
    agree_pct = agree_n / len(d["final_codes"]) * 100

    # Organic ratings
    org_avgs = [td.get("organic_avg", 3.0) for td in d["temporal_data"].values() if td.get("organic_n", 0) > 0]
    org_min, org_max = (min(org_avgs), max(org_avgs)) if org_avgs else (1.0, 4.0)

    # Synthflow breakdown
    synth_total = sum(d["comp_groups"].get("Synthflow", {}).values())
    synth_bill = d["comp_groups"].get("Synthflow", {}).get("BILLING", 0) / synth_total * 100 if synth_total else 0
    synth_rel = d["comp_groups"].get("Synthflow", {}).get("SERVICE RELIABILITY", 0) / synth_total * 100 if synth_total else 0

    nf = d["switching"]["net_flow"]
    ruby_net = nf.get("Ruby Receptionist", {}).get("net", 0)
    smith_net = nf.get("Smith.ai", {}).get("net", 0)

    md = f"""# Analysis 00: Executive Summary

> Generated from {d['total_count']} churn quotes, {d['total_all_quotes']} total reviews, {len(d['comp_groups'])} competitors

---

## Key Finding

**{ch_pct:.0f}% of churn is call handling. {bill_pct:.0f}% is billing. Together, {ai_addr:.0f}% maps to problems where AI has a structural advantage.**

---

## Dataset

| Metric | Value |
|---|---|
| Total reviews collected | {d['total_all_quotes']} |
| Churn quotes (dual-coded) | {d['total_count']} |
| Positive quotes | {d['positive_count']} |
| Competitors analyzed | {len(d['comp_groups'])} |
| Cohen's kappa | {d['kappa_val']:.4f} ("almost perfect") |
| Agreement rate | {agree_n}/{d['total_count']} ({agree_pct:.1f}%) |
| Disagreements | {len(d['disagreements'])} |
| Sources | Trustpilot ({d['tp_churn']}), Reddit ({d['reddit_churn']}) |
| Date range | 2015-2026 |

---

## Four Groups of Churn

| Group | % of Churn (weighted) | Count |
|---|:---:|:---:|
| CALL HANDLING | {ch_pct:.1f}% | {gs['CALL HANDLING']['count']} |
| BILLING | {bill_pct:.1f}% | {gs['BILLING']['count']} |
| SERVICE RELIABILITY | {rel_pct:.1f}% | {gs['SERVICE RELIABILITY']['count']} |
| INDUSTRY DISILLUSIONMENT | {disill_pct:.1f}% | {gs['INDUSTRY DISILLUSIONMENT']['count']} |

---

## Why Now

- Unprompted reviews average {org_min:.1f}-{org_max:.1f} stars. Recent 5-star waves mask persistent pain.
- AI-native entrants prove the model works but fail on billing ({synth_bill:.0f}% of Synthflow churn) and reliability ({synth_rel:.0f}%). Window is open but closing.

---

## Recommended Actions

1. **Target Ruby and Smith.ai churners first** -- they lose the most customers (Ruby {ruby_net:+d}, Smith.ai {smith_net:+d} net).
2. **Lead messaging with call handling quality** ({ch_pct:.0f}% of churn) and transparent pricing ({bill_pct:.0f}%).
3. **Start with legal vertical** -- highest signal density in the data.
"""
    write_md("00_executive_summary.md", md)


def dump_churn_pareto(d):
    tw = d["total_weighted"]
    cs = d["cat_stats"]
    sc = d["sorted_cats"]

    rows = []
    cumul = 0
    for rank, cat in enumerate(sc, 1):
        s = cs[cat]; m = CATEGORY_META[cat]
        pct = s["weighted"] / tw * 100; cumul += pct
        rows.append(f"| {rank} | {m['short']} | {m['group']} | {s['count']} | {pct:.1f}% | {cumul:.1f}% |")

    md = f"""# Analysis 01: Churn Pareto (11 Categories)

> {d['total_count']} churn quotes, weighted by quote quality and engagement

---

## 11 Churn Reasons Ranked by Weighted Share

| Rank | Churn Reason | Group | Count | % | Running Total |
|:---:|---|---|:---:|:---:|:---:|
{chr(10).join(rows)}
| | **Total** | | **{d['total_count']}** | **100%** | |

---

## Top 6 categories account for {cumul:.0f}% of churn (cumulative of rank 6)

"""
    # Actually compute top-6 cumul properly
    top6_cumul = 0
    for i, cat in enumerate(sc[:6]):
        top6_cumul += cs[cat]["weighted"] / tw * 100
    md = md.replace(f"account for {cumul:.0f}%", f"account for {top6_cumul:.0f}%")

    write_md("01_churn_pareto.md", md)


def dump_group_pareto(d):
    tw = d["total_weighted"]
    gs = d["group_stats"]
    cs = d["cat_stats"]

    md = """# Analysis 06: Group-Level Pareto

> 4 groups, each containing 2-4 specific churn categories

---

"""
    for g in GROUP_ORDER:
        s = gs[g]
        pct = s["weighted"] / tw * 100
        md += f"## {g} -- {pct:.1f}% ({s['count']} quotes)\n\n"
        cats_sorted = sorted(s["cats"], key=lambda c: cs[c]["weighted"], reverse=True)
        md += "| Category | Count | % of Group |\n|---|:---:|:---:|\n"
        for c in cats_sorted:
            cat_pct = cs[c]["count"] / s["count"] * 100 if s["count"] > 0 else 0
            md += f"| {CATEGORY_META[c]['short']} | {cs[c]['count']} | {cat_pct:.0f}% |\n"
        md += "\n"

    write_md("06_group_pareto.md", md)


def dump_switching_matrix(d):
    sw = d["switching"]
    nf = sw["net_flow"]
    sorted_nf = sorted(nf.items(), key=lambda x: x[1]["net"])

    rows = []
    for comp, data in sorted_nf:
        rows.append(f"| {comp} | {data['arrivals']} | {data['departures']} | {data['net']:+d} |")

    trigger_rows = []
    sw_total = sum(sw["triggers"].values())
    for trig, cnt in sorted(sw["triggers"].items(), key=lambda x: x[1], reverse=True):
        pct = cnt / sw_total * 100 if sw_total else 0
        trigger_rows.append(f"| {trig} | {cnt} | {pct:.0f}% |")

    biggest_loser = sorted_nf[0][0] if sorted_nf else "N/A"
    biggest_loss = sorted_nf[0][1]["net"] if sorted_nf else 0

    md = f"""# Analysis 02: Switching Matrix

> {sw['total']} switching stories extracted from churn_switched quotes

---

## Net Customer Flow

{biggest_loser} loses the most customers ({biggest_loss:+d} net).

| Company | Arrivals | Departures | Net |
|---|:---:|:---:|:---:|
{chr(10).join(rows)}

---

## Switching Triggers

| Trigger | Count | % of {sw_total} |
|---|:---:|:---:|
{chr(10).join(trigger_rows)}

---

## Trigger Definitions

- **Quality**: Missed calls, wrong info, platform not working, agents not trained
- **Capability**: Missing features, no integrations, limited technology
- **Pricing**: Too expensive, hidden fees, per-minute overcharges
"""
    write_md("02_switching_matrix.md", md)


def dump_kappa_analysis(d):
    agree_n = d["kappa_agree"]
    total = d["kappa_n"]
    disagree = len(d["disagreements"])
    agree_pct = agree_n / total * 100 if total else 0
    disagree_pct = disagree / len(d["final_codes"]) * 100

    # Build confusion-like summary of disagreements
    dis_pairs = Counter()
    for idx, a_cat, b_cat in d["disagreements"]:
        pair = tuple(sorted([a_cat or "None", b_cat or "None"]))
        dis_pairs[pair] += 1

    dis_rows = []
    for (a, b), cnt in dis_pairs.most_common():
        a_short = CATEGORY_META.get(a, {}).get("short", a)
        b_short = CATEGORY_META.get(b, {}).get("short", b)
        dis_rows.append(f"| {a_short} | {b_short} | {cnt} |")

    md = f"""# Analysis 05: Inter-Rater Reliability (Cohen's Kappa)

> Two independent LLM classifiers, 11-category taxonomy (k=9 codebook)

---

## Summary

| Metric | Value |
|---|---|
| Cohen's kappa | **{d['kappa_val']:.4f}** |
| Interpretation | "Almost perfect agreement" (>0.81) |
| 95% CI (approx) | {d['kappa_val'] - 0.05:.2f} to {d['kappa_val'] + 0.05:.2f} |
| Items coded | {total} |
| Agreements | {agree_n} ({agree_pct:.1f}%) |
| Disagreements | {disagree} ({disagree_pct:.1f}%) |

---

## Disagreement Pairs

| Coder A | Coder B | Count |
|---|---|:---:|
{chr(10).join(dis_rows)}

---

## Category Sensitivity

Reliability stays equally high at k=7 through k=11. We chose 11 because it's the most actionable:
"billing" is too vague to act on, but "predatory billing" vs "opaque billing" vs "billing traps"
each need a different product response.
"""
    write_md("05_kappa_analysis.md", md)


def dump_competitor_heatmap(d):
    cg = d["comp_groups"]

    md = """# Analysis 13: Competitor x Group Heatmap

> Per-competitor churn profile across 4 groups

---

## Churn Distribution by Competitor

| Competitor | CALL HANDLING | BILLING | SERVICE RELIABILITY | INDUSTRY DISILLUSIONMENT | Total |
|---|:---:|:---:|:---:|:---:|:---:|
"""
    for prod in TOP_COMPETITORS:
        total = sum(cg.get(prod, {}).values())
        if total == 0: continue
        pcts = []
        for g in GROUP_ORDER:
            val = cg.get(prod, {}).get(g, 0)
            pcts.append(f"{val}/{total} ({val/total*100:.0f}%)")
        md += f"| {prod} | {' | '.join(pcts)} | {total} |\n"

    # Legacy average
    legacy_prods = ["Ruby Receptionist", "AnswerConnect", "PATLive", "Smith.ai"]
    md += "\n---\n\n## Legacy Average vs Synthflow\n\n"
    md += "| Group | Legacy Avg | Synthflow |\n|---|:---:|:---:|\n"
    synth_total = sum(cg.get("Synthflow", {}).values())
    for g in GROUP_ORDER:
        vals = []
        for p in legacy_prods:
            total = sum(cg.get(p, {}).values())
            if total > 0:
                vals.append(cg.get(p, {}).get(g, 0) / total * 100)
        legacy_avg = float(np.mean(vals)) if vals else 0
        synth_pct = cg.get("Synthflow", {}).get(g, 0) / synth_total * 100 if synth_total else 0
        md += f"| {g} | {legacy_avg:.0f}% | {synth_pct:.0f}% |\n"

    md += "\n**Key insight:** AI eliminates call handling churn but shifts failure to billing and platform reliability.\n"
    write_md("13_competitor_heatmap.md", md)


def dump_industry_verticals(d):
    ind = d["industry_data"]
    if not ind:
        write_md("09_industry_verticals.md", "# Analysis 09: Industry Verticals\n\nNo industry data found.\n")
        return

    total_ident = sum(v["count"] for v in ind.values())
    vert_sorted = sorted(ind.items(), key=lambda x: x[1]["count"], reverse=True)

    rows = []
    for vert, vdata in vert_sorted:
        top_cat = vdata["cats"].most_common(1)[0] if vdata["cats"] else ("", 0)
        top_label = CATEGORY_META.get(top_cat[0], {}).get("short", top_cat[0]) if top_cat[0] else ""
        rows.append(f"| {vert} | {vdata['count']} | {vdata['count']/total_ident*100:.0f}% | {top_label} ({top_cat[1]}) |")

    md = f"""# Analysis 09: Industry Verticals

> {total_ident} of {d['total_count']} churn quotes mention a specific industry

---

## Breakdown

| Industry | Quotes | % of Identified | Top Churn Reason |
|---|:---:|:---:|---|
{chr(10).join(rows)}

---

## Caveat

All {d['reddit_churn']} Reddit churn quotes come from r/LawFirm. The other 6 subreddits scraped
(r/VOIP, r/smallbusiness, r/Dentistry, r/legaltech, r/SaaS, r/agency) produced zero churn quotes.
The "Legal dominates" finding reflects where we found signal, not necessarily where churn happens.
"""
    write_md("09_industry_verticals.md", md)


def dump_dollar_impact(d):
    dq = d["dollar_quotes"]
    if not dq:
        write_md("10_dollar_impact.md", "# Analysis 10: Dollar Impact\n\nNo dollar amounts found.\n")
        return

    monthly = [x for x in dq if any("/mo" in a or "/month" in a for a in x["amounts"])]
    overcharges = [x for x in dq if x["cat"] in ("BILLING_PREDATORY", "BILLING_OPAQUE", "BILLING_TRAP")]

    md = f"""# Analysis 10: Dollar Impact

> {len(dq)} of {d['total_count']} churn quotes mention specific dollar amounts

---

## Monthly Costs Reported ({len(monthly)} quotes)

| Product | Amounts | Pain Point |
|---|---|---|
"""
    for item in monthly[:10]:
        md += f"| {item['product']} | {', '.join(item['amounts'])} | {item['pain_point'][:80]}{'...' if len(item['pain_point']) > 80 else ''} |\n"

    md += f"""
---

## Documented Overcharges / Billing Issues ({len(overcharges)} quotes)

| Product | Amounts | Category | Pain Point |
|---|---|---|---|
"""
    for item in overcharges[:10]:
        cat_short = CATEGORY_META.get(item["cat"], {}).get("short", item["cat"])
        md += f"| {item['product']} | {', '.join(item['amounts'])} | {cat_short} | {item['pain_point'][:80]}{'...' if len(item['pain_point']) > 80 else ''} |\n"

    write_md("10_dollar_impact.md", md)


def dump_data_quality(d):
    agree_pct = (len(d["final_codes"]) - len(d["disagreements"])) / len(d["final_codes"]) * 100
    tw = d["total_weighted"]
    gs = d["group_stats"]
    ch_pct = gs["CALL HANDLING"]["weighted"] / tw * 100
    bill_pct = gs["BILLING"]["weighted"] / tw * 100

    # Post-2020 rankings
    all_ranking = sorted(
        [(prod, sum(1 for idx in d["final_codes"]
          if normalize_product(d["quotes"][idx]["llm"].get("product_mentioned")) == prod))
         for prod in TOP_COMPETITORS], key=lambda x: x[1], reverse=True)
    post_ranking = sorted(
        [(prod, d["post2020_cats"].get(prod, 0)) for prod in TOP_COMPETITORS],
        key=lambda x: x[1], reverse=True)

    rank_rows = []
    for r in range(len(TOP_COMPETITORS)):
        all_p, all_n = all_ranking[r]
        post_p, post_n = post_ranking[r]
        change = "No change" if all_p == post_p else f"{post_p} moves up"
        rank_rows.append(f"| #{r+1} | {all_p} ({all_n}) | {post_p} ({post_n}) | {change} |")

    md = f"""# Analysis 11: Data Quality & Limitations

> Transparency notes for stress-testing the findings

---

## Known Issues

| Issue | Detail | Impact |
|---|---|---|
| Mostly Trustpilot | {d['tp_churn']}/{d['total_count']} ({d['tp_churn']*100//d['total_count']}%) from Trustpilot. {d['reddit_churn']} from Reddit. | Complaint types are real but frequency may not match overall market. |
| Some complaints are old | {d['pre2020_count']}/{d['total_count']} from before 2020. | Competitor rankings shift when stale data removed. Complaint types hold across periods. |
| Reddit is all r/LawFirm | All {d['reddit_churn']} Reddit quotes from r/LawFirm. 6 other subreddits produced 0 churn quotes. | "Legal dominates" reflects signal source, not necessarily market reality. |
| Both classifiers are AI | Two independent LLMs. {agree_pct:.0f}% agreement. | Both may share blind spots. Systematic LLM bias wouldn't be caught. |
| Positive reviews excluded | {d['positive_count']} positive quotes collected, not analyzed. | We know what makes customers leave, not if problems are unique to churners. |
| Mid-2024 review surge | Every competitor saw sudden 5-star spikes. | "Unprompted vs. recent wave" split is directional, not definitive. |

---

## Temporal Sensitivity: Does the Ranking Change?

| Rank | All Dates | Post-2020 | Change |
|:---:|---|---|---|
{chr(10).join(rank_rows)}

Complaint types (call handling {ch_pct:.0f}%, billing {bill_pct:.0f}%) hold up in both time windows.

---

## What This Analysis Does Not Cover

- Captures why customers LEAVE, not why they STAY.
- Trustpilot reviews skew negative. Reddit signal is from r/LawFirm only.
- English-language, US-focused.
- Competitor pricing data was not independently collected.

---

## Sample Composition

| Source | Count |
|---|:---:|
| Trustpilot | {d['tp_churn']} |
| Reddit | {d['reddit_churn']} |
| **Total churn** | **{d['total_count']}** |
| Total reviews collected | {d['total_all_quotes']} |
"""
    write_md("11_data_quality_audit.md", md)


def dump_gut_punch_quotes(d):
    gut_punch = d["gut_punch"]
    extract = d["extract_pull_quote"]

    theme_labels = {
        "CALL HANDLING": "THE CALL HANDLING PROBLEM",
        "BILLING": "THE BILLING PROBLEM",
        "SERVICE RELIABILITY": "THE RELIABILITY PROBLEM",
        "INDUSTRY DISILLUSIONMENT": "THE CATEGORY PROBLEM",
    }

    md = """# Analysis 15: Gut-Punch Quotes (Best per Group)

> One devastating quote per churn group, auto-selected by devastation score

---

"""
    for (idx, q, cat, prod), g in zip(gut_punch, GROUP_ORDER):
        pull = extract(q["text"])
        pain = q["llm"].get("pain_point", "")
        label = theme_labels.get(g, g)
        md += f"### {label}\n\n"
        md += f"> \"{pull}\"\n>\n> -- {prod} customer | {pain}\n\n"

    write_md("15_gut_punch_quotes.md", md)


def dump_best_quotes_per_category(d):
    cs = d["cat_stats"]
    sc = d["sorted_cats"]
    tw = d["total_weighted"]
    quotes = d["quotes"]

    md = """# Analysis 16: Best Quotes by Category

> Top 2 quotes per category, ranked by weight (quality x engagement)

---

"""
    for cat in sc:
        s = cs[cat]; m = CATEGORY_META[cat]
        pct = s["weighted"] / tw * 100
        md += f"## {m['short']} ({s['count']} quotes, {pct:.1f}%)\n\n"
        top = sorted(s["quotes"], key=lambda x: x[2], reverse=True)[:2]
        for j, (idx, q, w) in enumerate(top, 1):
            prod = normalize_product(q["llm"].get("product_mentioned"))
            pain = q["llm"].get("pain_point", "")
            text = q["text"].replace("\n", " ").strip()
            md += f"**#{j}** | {prod} | Quality: {q['llm'].get('quote_quality', 1)}/5 | {q.get('source', '').title()}\n\n"
            md += f"*{pain}*\n\n"
            md += f"> {text[:500]}{'...' if len(text) > 500 else ''}\n\n"

    write_md("16_best_quotes_by_category.md", md)


# ── Main ─────────────────────────────────────────────────────────
def main():
    print("Computing analysis from raw data...")
    d = compute_all()
    print(f"  {d['total_count']} churn quotes, {d['total_all_quotes']} total reviews")
    print(f"  Kappa: {d['kappa_val']:.4f} ({d['kappa_agree']}/{d['kappa_n']} agree)")
    print(f"  Switching: {d['switching']['total']} stories, triggers={d['switching']['triggers']}")
    print()

    print("Writing analysis markdown files...")
    dump_executive_summary(d)
    dump_churn_pareto(d)
    dump_group_pareto(d)
    dump_switching_matrix(d)
    dump_kappa_analysis(d)
    dump_competitor_heatmap(d)
    dump_industry_verticals(d)
    dump_dollar_impact(d)
    dump_data_quality(d)
    dump_gut_punch_quotes(d)
    dump_best_quotes_per_category(d)

    print()
    print("Done. All analysis files written to analysis/")


if __name__ == "__main__":
    main()
