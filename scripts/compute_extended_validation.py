"""Full-range human-vs-LLM validation over the extended review set.

Combines the original dev-subset human review with the extended (jitter +
weak-model) human review, pairs every page with the corresponding LLM judge
output for the SAME run, and reports:

1. Human jitter ordering check — does the human rater actually score
   original > mild > severe? (arbitrates the constructed ground truth)
2. Full-range Pearson r on page scores, per judge, overall and per subset.
3. Item-level agreement and Cohen's kappa, per judge, over the full range.

Usage:
  py -3.12 scripts/compute_extended_validation.py
"""

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "data" / "track_b" / "visual_human_review"
OUT_PATH = ROOT / "data" / "track_b" / "visual_jitter_validation" / "extended_validation_summary.json"

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
    if any(out.get(k) is None for k in ITEM_IDS):
        return None
    return {k: bool(out[k]) for k in ITEM_IDS}


def load_review(path, default_run):
    """-> {(run, item, page_id): {item_id: bool}}"""
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for p in data["pages"]:
        flat = flatten(p)
        if flat is not None:
            out[(p.get("run", default_run), p["item"], p["page_id"])] = flat
    return out


def subset_of(run):
    if run == RUN:
        return "original"
    if run.endswith("_jitter_mild"):
        return "mild"
    if run.endswith("_jitter_severe"):
        return "severe"
    return "weak"


def score(flat):
    return sum(1 for k in ITEM_IDS if flat[k]) / 16


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


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


def judge_files(model):
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", model)
    files = {RUN: REVIEW_DIR / f"llm_judge_{safe}_strict_fewshot.json"}
    for sev in ("mild", "severe"):
        files[f"{RUN}_jitter_{sev}"] = REVIEW_DIR / f"llm_judge_{safe}_strict_fewshot_jitter_{sev}.json"
    for run in WEAK_RUNS:
        files[run] = REVIEW_DIR / f"llm_judge_{safe}_strict_fewshot_{run}.json"
    return files


def main():
    human = load_review(REVIEW_DIR / "visual_human_review.json", RUN)
    human.update(load_review(REVIEW_DIR / "visual_human_review_extended.json", None))
    human = {k: v for k, v in human.items() if k[0] is not None}

    # 1. Human jitter ordering check
    def hscore(run, item, page):
        rec = human.get((run, item, page))
        return score(rec) if rec else None

    ordering = {"orig_gt_mild": 0, "orig_eq_mild": 0, "orig_lt_mild": 0,
                "orig_gt_severe": 0, "orig_eq_severe": 0, "orig_lt_severe": 0,
                "mild_gt_severe": 0, "mild_eq_severe": 0, "mild_lt_severe": 0, "n": 0}
    for (run, item, page) in [k for k in human if k[0] == RUN]:
        o = hscore(RUN, item, page)
        m = hscore(f"{RUN}_jitter_mild", item, page)
        s = hscore(f"{RUN}_jitter_severe", item, page)
        if None in (o, m, s):
            continue
        ordering["n"] += 1
        ordering["orig_gt_mild" if o > m else "orig_eq_mild" if o == m else "orig_lt_mild"] += 1
        ordering["orig_gt_severe" if o > s else "orig_eq_severe" if o == s else "orig_lt_severe"] += 1
        ordering["mild_gt_severe" if m > s else "mild_eq_severe" if m == s else "mild_lt_severe"] += 1

    human_means = {}
    for sub in ("original", "mild", "severe", "weak"):
        vals = [score(v) for k, v in human.items() if subset_of(k[0]) == sub]
        human_means[sub] = round(mean(vals), 4) if vals else None

    print("=== Human jitter ordering (page-level, n=%d triples) ===" % ordering["n"])
    print(f"original vs mild  : >{ordering['orig_gt_mild']}  ={ordering['orig_eq_mild']}  <{ordering['orig_lt_mild']}")
    print(f"original vs severe: >{ordering['orig_gt_severe']}  ={ordering['orig_eq_severe']}  <{ordering['orig_lt_severe']}")
    print(f"mild vs severe    : >{ordering['mild_gt_severe']}  ={ordering['mild_eq_severe']}  <{ordering['mild_lt_severe']}")
    print(f"human mean by subset: {human_means}")

    # 2./3. Full-range correlation per judge
    judges_out = {}
    for model in JUDGES:
        llm = {}
        for run, path in judge_files(model).items():
            if not path.exists():
                print(f"  [warn] missing judge file for {model} run={run}: {path.name}")
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            for p in data["pages"]:
                flat = flatten(p)
                if flat is not None:
                    llm[(run, p["item"], p["page_id"])] = flat

        keys = sorted(set(human) & set(llm))
        hs = [score(human[k]) for k in keys]
        ls = [score(llm[k]) for k in keys]
        pairs = [(human[k][i], llm[k][i]) for k in keys for i in ITEM_IDS]
        agree = sum(1 for h, l in pairs if h == l) / len(pairs) if pairs else None

        per_subset = {}
        for sub in ("original", "mild", "severe", "weak"):
            sk = [k for k in keys if subset_of(k[0]) == sub]
            r_sub = pearson([score(human[k]) for k in sk], [score(llm[k]) for k in sk])
            per_subset[sub] = {"n": len(sk), "pearson": round(r_sub, 4) if r_sub is not None else None}

        r = pearson(hs, ls)
        kp = kappa(pairs)
        judges_out[model] = {
            "pages_paired": len(keys),
            "pearson_full_range": round(r, 4) if r is not None else None,
            "cohen_kappa_item_level": round(kp, 4) if kp is not None else None,
            "item_agreement": round(agree, 4) if agree is not None else None,
            "human_mean": round(mean(hs), 4) if hs else None,
            "llm_mean": round(mean(ls), 4) if ls else None,
            "per_subset_pearson": per_subset,
        }
        print(f"\n=== {model} (full range, {len(keys)} pages) ===")
        print(f"Pearson(full)={judges_out[model]['pearson_full_range']}  "
              f"kappa={judges_out[model]['cohen_kappa_item_level']}  "
              f"agreement={judges_out[model]['item_agreement']}")
        print(f"means human={judges_out[model]['human_mean']} llm={judges_out[model]['llm_mean']}")
        print("per-subset r: " + ", ".join(
            f"{s}={v['pearson']}(n={v['n']})" for s, v in per_subset.items()))

    out = {"human_jitter_ordering": ordering, "human_mean_by_subset": human_means,
           "judges": judges_out}
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()
