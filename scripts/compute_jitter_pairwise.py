"""Pairwise ranking accuracy of the visual judge on jittered page variants.

Ground truth ordering is constructed (original > mild > severe), so this
measures discriminative validity without human labels: for each page pair the
judge is correct when it scores the better variant strictly higher; ties count
0.5 (no discrimination).

Usage:
  py -3.12 scripts/compute_jitter_pairwise.py --model gemma-4-31b-it
"""

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "data" / "track_b" / "visual_human_review"
OUT_DIR = ROOT / "data" / "track_b" / "visual_jitter_validation"


def load_scores(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return {f"{p['item']}::{p['page_id']}": p.get("page_score")
            for p in data["pages"] if p.get("page_score") is not None}


def pairwise(better, worse):
    keys = sorted(set(better) & set(worse))
    correct = sum(1.0 if better[k] > worse[k] else (0.5 if better[k] == worse[k] else 0.0)
                  for k in keys)
    return {
        "n_pairs": len(keys),
        "accuracy": round(correct / len(keys), 4) if keys else None,
        "wrong_pairs": [k for k in keys if better[k] < worse[k]],
        "tied_pairs": [k for k in keys if better[k] == worse[k]],
    }


def mean(d):
    return round(sum(d.values()) / len(d), 4) if d else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--suffix", default="strict_fewshot")
    args = ap.parse_args()

    import re
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", args.model)
    orig = load_scores(REVIEW_DIR / f"llm_judge_{safe}_{args.suffix}.json")
    mild = load_scores(REVIEW_DIR / f"llm_judge_{safe}_{args.suffix}_jitter_mild.json")
    severe = load_scores(REVIEW_DIR / f"llm_judge_{safe}_{args.suffix}_jitter_severe.json")

    result = {
        "model": args.model,
        "judge_config": args.suffix,
        "ground_truth": "original > mild > severe (constructed via JITTER-*-v1 CSS injection)",
        "mean_scores": {"original": mean(orig), "mild": mean(mild), "severe": mean(severe)},
        "pairs": {
            "original_vs_mild": pairwise(orig, mild),
            "original_vs_severe": pairwise(orig, severe),
            "mild_vs_severe": pairwise(mild, severe),
        },
    }
    accs = [p["accuracy"] for p in result["pairs"].values() if p["accuracy"] is not None]
    result["overall_pairwise_accuracy"] = round(sum(accs) / len(accs), 4) if accs else None

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"jitter_pairwise_{safe}_{args.suffix}.json"
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"model={args.model} config={args.suffix}")
    print(f"mean scores: original={result['mean_scores']['original']} "
          f"mild={result['mean_scores']['mild']} severe={result['mean_scores']['severe']}")
    for name, p in result["pairs"].items():
        print(f"{name}: accuracy={p['accuracy']} (n={p['n_pairs']}, "
              f"wrong={len(p['wrong_pairs'])}, tied={len(p['tied_pairs'])})")
    print(f"overall pairwise accuracy: {result['overall_pairwise_accuracy']}")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
