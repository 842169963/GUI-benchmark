"""Compare human vs LLM static-visual checklist answers.

Reads the human review export and an LLM judge output (same shape) and reports
item-level agreement, per-item-id disagreement, and page-score comparison.
"""

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "data" / "track_b" / "visual_human_review"
ITEM_IDS = ["L1", "L2", "L3", "L4", "O1", "O2", "O3", "O4",
            "T1", "T2", "T3", "T4", "C1", "C2", "C3", "C4"]


def flatten(rec):
    """page -> {item_id: bool/None}."""
    dims = rec.get("dimensions")
    if not dims:
        return None
    out = {}
    for d in dims.values():
        out.update(d)
    return out


def load(path):
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    return {f"{p['item']}::{p['page_id']}": p for p in data["pages"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--human", default=str(REVIEW_DIR / "visual_human_review.json"))
    ap.add_argument("--llm", required=True)
    args = ap.parse_args()

    human = load(args.human)
    llm = load(args.llm)

    total = matches = 0
    per_item = {k: {"match": 0, "n": 0, "human_true": 0, "llm_true": 0} for k in ITEM_IDS}
    human_scores, llm_scores = [], []
    pages_compared = 0

    for key in sorted(human):
        if key not in llm:
            continue
        h = flatten(human[key])
        l = flatten(llm[key])
        if h is None or l is None:
            continue
        if any(h[k] is None for k in ITEM_IDS) or any(l[k] is None for k in ITEM_IDS):
            continue
        pages_compared += 1
        human_scores.append(sum(1 for k in ITEM_IDS if h[k]) / 16)
        llm_scores.append(sum(1 for k in ITEM_IDS if l[k]) / 16)
        for k in ITEM_IDS:
            per_item[k]["n"] += 1
            per_item[k]["human_true"] += int(h[k])
            per_item[k]["llm_true"] += int(l[k])
            if h[k] == l[k]:
                per_item[k]["match"] += 1
                matches += 1
            total += 1

    def mean(xs):
        return sum(xs) / len(xs) if xs else float("nan")

    def pearson(a, b):
        n = len(a)
        if n < 2:
            return float("nan")
        ma, mb = mean(a), mean(b)
        va = sum((x - ma) ** 2 for x in a)
        vb = sum((x - mb) ** 2 for x in b)
        if va == 0 or vb == 0:
            return float("nan")  # undefined when one side has no variance
        cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
        return cov / (va ** 0.5 * vb ** 0.5)

    print(f"Pages compared: {pages_compared}")
    print(f"Item-level agreement: {matches}/{total} = {matches/total:.3f}")
    print(f"Human mean page score: {mean(human_scores):.3f}")
    print(f"LLM   mean page score: {mean(llm_scores):.3f}")
    r = pearson(human_scores, llm_scores)
    print(f"Pearson(page_score): {'undefined (no variance)' if r != r else f'{r:.3f}'}")
    print("\nPer-item (human_true / llm_true / agreement over n):")
    for k in ITEM_IDS:
        d = per_item[k]
        if d["n"]:
            print(f"  {k}: human_true={d['human_true']:>2} llm_true={d['llm_true']:>2} "
                  f"agree={d['match']}/{d['n']} ({d['match']/d['n']:.2f})")

    out = {
        "human": pathlib.Path(args.human).name,
        "llm": pathlib.Path(args.llm).name,
        "pages_compared": pages_compared,
        "item_agreement": round(matches / total, 4) if total else None,
        "human_mean_page_score": round(mean(human_scores), 4),
        "llm_mean_page_score": round(mean(llm_scores), 4),
        "pearson_page_score": None if r != r else round(r, 4),
        "per_item": per_item,
    }
    out_path = REVIEW_DIR / "human_vs_llm_comparison.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
