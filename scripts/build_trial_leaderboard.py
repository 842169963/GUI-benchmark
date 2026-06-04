"""Trial Track B leaderboard aggregation (2026-06-04).

Combines the currently computable category scores for the 3-item development
subset into a provisional model-level leaderboard row.

TENTATIVE weights (hyper-parameters, to be sensitivity-tested; not final):
    Technical 0.20, Visual 0.25, Accessibility 0.15, Dynamic 0.40

Visual is not yet available (LB-JUDGE-v1 not run), so the provisional Overall is
computed over the available quality categories with renormalized weights, and
the full Overall is left null until the visual judge runs. Efficiency is kept as
a Pareto axis (reported raw), not folded into Overall, to avoid double-counting
cost.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ITEMS = ROOT / "data" / "track_b" / "items"
RUN = "gwdg_qwen36_35b_v9_smoke"
MODEL = "gwdg/qwen3.6-35b-a3b"
DEV_ITEMS = ["F01_1daycloud", "F03_about_gitlab", "F10_gourmania"]

WEIGHTS = {"technical": 0.20, "visual": 0.25, "accessibility": 0.15, "dynamic": 0.40}


def load(item, name):
    p = ITEMS / item / "generated" / RUN / name
    return json.loads(p.read_text(encoding="utf-8"))


def category_scores(item):
    gate = load(item, "gate_report.json")
    dyn = load(item, "browser_workflow_normalized_report.json")
    a11y = load(item, "accessibility_report.json")
    return {
        # gate pass/fail used as a placeholder until coverage submetrics exist
        "technical": 1.0 if gate.get("passed") else 0.0,
        "visual": None,  # pending LB-JUDGE-v1
        "accessibility": round(a11y["accessibility_score"], 4),
        "dynamic": round(dyn["task_success_rate"], 4),
    }


def provisional_overall(scores):
    avail = {k: v for k, v in scores.items() if v is not None and k in WEIGHTS}
    wsum = sum(WEIGHTS[k] for k in avail)
    return round(sum(WEIGHTS[k] * v for k, v in avail.items()) / wsum, 4)


def main():
    rows = []
    for item in DEV_ITEMS:
        s = category_scores(item)
        s["provisional_overall_excl_visual"] = provisional_overall(s)
        s["item"] = item
        rows.append(s)

    def mean(key):
        vals = [r[key] for r in rows if r[key] is not None]
        return round(sum(vals) / len(vals), 4) if vals else None

    model_row = {
        "model": MODEL,
        "run": RUN,
        "items": len(rows),
        "technical": mean("technical"),
        "visual": None,
        "accessibility": mean("accessibility"),
        "dynamic": mean("dynamic"),
        "provisional_overall_excl_visual": mean("provisional_overall_excl_visual"),
        "full_overall": None,  # null until visual judge runs
        "weights_tentative": WEIGHTS,
    }

    out = {"model_level": model_row, "item_level": rows}
    out_path = ROOT / "data" / "track_b" / "trial_leaderboard_2026-06-04.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"{'item':<20} {'tech':>5} {'vis':>5} {'a11y':>6} {'dyn':>6} {'prov.Overall':>12}")
    for r in rows:
        vis = "  -  " if r["visual"] is None else f"{r['visual']:.3f}"
        print(
            f"{r['item']:<20} {r['technical']:>5.2f} {vis:>5} "
            f"{r['accessibility']:>6.3f} {r['dynamic']:>6.3f} "
            f"{r['provisional_overall_excl_visual']:>12.3f}"
        )
    print("-" * 60)
    print(
        f"{MODEL:<20} {model_row['technical']:>5.2f} {'  -  ':>5} "
        f"{model_row['accessibility']:>6.3f} {model_row['dynamic']:>6.3f} "
        f"{model_row['provisional_overall_excl_visual']:>12.3f}"
    )
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
