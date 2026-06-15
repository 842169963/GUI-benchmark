"""Merge rater2's partial exports and compute inter-rater reliability.

1. Merge the two complementary rater2 exports (each browser session saved one
   half) into one file, verifying no conflicting overlaps.
2. Inter-rater (rater1 = thesis author, rater2 = independent friend) on the
   56-page extended set: item-level agreement, Cohen's kappa, page-score
   Pearson, per-subset means.
3. Judge's-Verdict-style comparison: each judge's agreement with EACH rater on
   the same extended pages vs the human-human agreement (the ceiling).

Usage:
  py -3.12 scripts/compute_interrater.py --in1 <export1> --in2 <export2>
"""

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "data" / "track_b" / "visual_human_review"
OUT_JSON = ROOT / "data" / "track_b" / "visual_jitter_validation" / "interrater_summary.json"

RUN = "gwdg_qwen36_35b_v9_smoke"
WEAK_RUNS = ["gwdg_qwen3_omni_30b_v9_smoke", "gwdg_internvl35_30b_v9_smoke",
             "openai_gpt4omini_v9_f10_smoke"]
JUDGES = ["gemma-4-31b-it", "gpt-4.1-mini", "claude-sonnet-4-5-20250929"]
ITEM_IDS = ["L1", "L2", "L3", "L4", "O1", "O2", "O3", "O4",
            "T1", "T2", "T3", "T4", "C1", "C2", "C3", "C4"]


def flatten(rec):
    dims = rec.get("dimensions")
    if not dims:
        return None
    out = {}
    for d in dims.values():
        out.update(d)
    return out  # may contain None


def key_of(p):
    return (p["run"], p["item"], p["page_id"])


def load_pages(path):
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    return data["pages"]


def answered_count(flat):
    return sum(1 for i in ITEM_IDS if flat.get(i) is not None)


def merge(path1, path2):
    merged = {}
    conflicts = []
    for path in (path1, path2):
        for p in load_pages(path):
            flat = flatten(p)
            if flat is None or answered_count(flat) == 0:
                continue
            k = key_of(p)
            if k in merged:
                if merged[k] != {i: flat.get(i) for i in ITEM_IDS}:
                    conflicts.append(k)
                continue
            merged[k] = {i: flat.get(i) for i in ITEM_IDS}
    return merged, conflicts


def score(flat):
    vals = [flat[i] for i in ITEM_IDS if flat[i] is not None]
    return sum(1 for v in vals if v) / len(vals) if vals else None


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def pearson(a, b):
    n = len(a)
    if n < 2:
        return None
    ma, mb = mean(a), mean(b)
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((x - mb) ** 2 for x in b)
    if va == 0 or vb == 0:
        return None
    return sum((a[i] - ma) * (b[i] - mb) for i in range(n)) / (va ** 0.5 * vb ** 0.5)


def kappa(pairs):
    n = len(pairs)
    if not n:
        return None
    po = sum(1 for h, l in pairs if h == l) / n
    ph = sum(1 for h, _ in pairs if h) / n
    pl = sum(1 for _, l in pairs if l) / n
    pe = ph * pl + (1 - ph) * (1 - pl)
    if pe == 1.0:
        return None
    return (po - pe) / (1 - pe)


def subset_of(run):
    if run.endswith("_jitter_mild"):
        return "mild"
    if run.endswith("_jitter_severe"):
        return "severe"
    return "weak"


def compare(a, b):
    """a, b: {key: {item: bool|None}} -> stats over shared non-null cells."""
    keys = sorted(set(a) & set(b))
    pairs = []
    pa, pb = [], []
    for k in keys:
        for i in ITEM_IDS:
            if a[k].get(i) is not None and b[k].get(i) is not None:
                pairs.append((a[k][i], b[k][i]))
        sa, sb = score(a[k]), score(b[k])
        if sa is not None and sb is not None:
            pa.append(sa)
            pb.append(sb)
    agree = sum(1 for x, y in pairs if x == y) / len(pairs) if pairs else None
    return {
        "pages": len(pa),
        "item_cells": len(pairs),
        "item_agreement": round(agree, 4) if agree is not None else None,
        "cohen_kappa": round(kappa(pairs), 4) if kappa(pairs) is not None else None,
        "pearson_page_score": round(pearson(pa, pb), 4) if pearson(pa, pb) is not None else None,
        "mean_a": round(mean(pa), 4) if pa else None,
        "mean_b": round(mean(pb), 4) if pb else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in1", required=True)
    ap.add_argument("--in2", required=True)
    args = ap.parse_args()

    rater2, conflicts = merge(args.in1, args.in2)
    if conflicts:
        print(f"WARNING: {len(conflicts)} conflicting overlap pages: {conflicts}")
    full = [k for k, v in rater2.items() if answered_count(v) == 16]
    partial = [k for k, v in rater2.items() if 0 < answered_count(v) < 16]
    print(f"rater2 merged: {len(rater2)} pages with answers "
          f"({len(full)} complete, {len(partial)} partial: {partial})")

    # Persist merged rater2 file in canonical shape
    out_pages = []
    for (run, item, page_id), flat in sorted(rater2.items()):
        dims = {
            "layout_hierarchy": {i: flat[i] for i in ITEM_IDS[0:4]},
            "information_clarity": {i: flat[i] for i in ITEM_IDS[4:8]},
            "typography_readability": {i: flat[i] for i in ITEM_IDS[8:12]},
            "visual_consistency": {i: flat[i] for i in ITEM_IDS[12:16]},
        }
        out_pages.append({"item": item, "page_id": page_id, "run": run,
                          "dimensions": dims, "page_score": score(flat)})
    merged_path = REVIEW_DIR / "visual_human_review_extended_rater2.json"
    merged_path.write_text(json.dumps(
        {"run": "extended_validation_2026-06-10", "reviewer": "human:rater2",
         "pages": out_pages}, indent=2), encoding="utf-8")
    print(f"wrote merged {merged_path}")

    # rater1 extended answers
    rater1 = {}
    for p in load_pages(REVIEW_DIR / "visual_human_review_extended.json"):
        flat = flatten(p)
        if flat and answered_count(flat):
            rater1[key_of(p)] = {i: flat.get(i) for i in ITEM_IDS}

    print("\n=== Inter-rater (rater1 vs rater2, extended set) ===")
    hh = compare(rater1, rater2)
    print(json.dumps(hh, indent=2))

    print("\n=== per-subset means (rater1 / rater2) ===")
    per_subset_means = {}
    for sub in ("mild", "severe", "weak"):
        m1 = mean([score(v) for k, v in rater1.items() if subset_of(k[0]) == sub])
        m2 = mean([score(v) for k, v in rater2.items() if subset_of(k[0]) == sub])
        per_subset_means[sub] = {"rater1": round(m1, 4) if m1 else None,
                                 "rater2": round(m2, 4) if m2 else None}
        print(f"{sub}: rater1={per_subset_means[sub]['rater1']} rater2={per_subset_means[sub]['rater2']}")

    # Judges vs each rater on the same extended pages
    import re
    judges_out = {}
    for model in JUDGES:
        safe = re.sub(r"[^A-Za-z0-9._-]", "_", model)
        llm = {}
        run_files = {f"{RUN}_jitter_mild": f"llm_judge_{safe}_strict_fewshot_jitter_mild.json",
                     f"{RUN}_jitter_severe": f"llm_judge_{safe}_strict_fewshot_jitter_severe.json"}
        for run in WEAK_RUNS:
            run_files[run] = f"llm_judge_{safe}_strict_fewshot_{run}.json"
        for run, fname in run_files.items():
            path = REVIEW_DIR / fname
            if not path.exists():
                continue
            for p in load_pages(path):
                flat = flatten(p)
                if flat and answered_count(flat) == 16:
                    llm[(run, p["item"], p["page_id"])] = {i: flat[i] for i in ITEM_IDS}
        judges_out[model] = {
            "vs_rater1": compare(llm, rater1),
            "vs_rater2": compare(llm, rater2),
        }
        print(f"\n=== {model} (extended pages only) ===")
        print(f"vs rater1: kappa={judges_out[model]['vs_rater1']['cohen_kappa']} "
              f"r={judges_out[model]['vs_rater1']['pearson_page_score']} "
              f"(n={judges_out[model]['vs_rater1']['pages']})")
        print(f"vs rater2: kappa={judges_out[model]['vs_rater2']['cohen_kappa']} "
              f"r={judges_out[model]['vs_rater2']['pearson_page_score']} "
              f"(n={judges_out[model]['vs_rater2']['pages']})")

    out = {"human_human": hh, "per_subset_means": per_subset_means,
           "judges_vs_raters_extended_only": judges_out,
           "rater2_partial_pages": [list(k) for k in partial],
           "merge_conflicts": [list(k) for k in conflicts]}
    OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT_JSON}")


if __name__ == "__main__":
    main()
