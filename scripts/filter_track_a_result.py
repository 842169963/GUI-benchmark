"""
Filter manually marked mismatch pairs from a Track A result JSON.

Usage:
    py -3.12 scripts/filter_track_a_result.py result.json --exclude 0,23,33
"""

import argparse
import json
import os


def summarize(results):
    n = len(results)
    flat = [run for item in results for run in item["runs"]]
    raw = sum(run["correct"] for run in flat) / len(flat) if flat else 0
    run1 = sum(item["runs"][0]["correct"] for item in results) / n if n else 0
    run2 = sum(item["runs"][1]["correct"] for item in results) / n if n else 0

    consistent = corrected = chose_a = chose_b = 0
    for item in results:
        r1, r2 = item["runs"]
        chose_a += sum(run["model_choice"] == "A" for run in item["runs"])
        chose_b += sum(run["model_choice"] == "B" for run in item["runs"])
        r1_good = r1["model_choice"] == "A"
        r2_good = r2["model_choice"] == "B"
        if r1_good == r2_good:
            consistent += 1
            if r1_good:
                corrected += 1

    return {
        "n_pairs": n,
        "n_calls": len(flat),
        "raw_accuracy": raw,
        "accuracy_run1_good_a": run1,
        "accuracy_run2_good_b": run2,
        "consistency_rate": consistent / n if n else 0,
        "position_bias_rate": 1 - (consistent / n if n else 0),
        "corrected_accuracy_consistent_only": corrected / consistent if consistent else 0,
        "n_consistent_pairs": consistent,
        "chose_a": chose_a,
        "chose_b": chose_b,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("result_json")
    parser.add_argument("--exclude", required=True, help="Comma-separated pair_id values.")
    parser.add_argument("--suffix", default=None)
    args = parser.parse_args()

    exclude = {int(x.strip()) for x in args.exclude.split(",") if x.strip()}
    with open(args.result_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    output = dict(data)
    output["meta"] = dict(data["meta"])
    output["meta"]["review_status"] = "manual_mismatch_excluded"
    output["pairs"] = [p for p in data["pairs"] if p["pair_id"] not in exclude]
    output["results"] = [r for r in data["results"] if r["pair_id"] not in exclude]
    output["summary"] = summarize(output["results"])
    output["summary"]["excluded_pair_ids"] = sorted(exclude)
    output["manual_review"] = {
        "excluded_as_mismatch": [p for p in data["pairs"] if p["pair_id"] in exclude],
        "n_excluded": len(exclude),
    }

    stem, ext = os.path.splitext(args.result_json)
    suffix = args.suffix or f"clean{len(output['pairs'])}"
    out_path = f"{stem}_{suffix}{ext}"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(json.dumps(output["summary"], indent=2))
    print(out_path)


if __name__ == "__main__":
    main()
