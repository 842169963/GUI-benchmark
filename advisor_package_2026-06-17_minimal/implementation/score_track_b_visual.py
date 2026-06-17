"""Production Static-Visual scorer using the FROZEN LB-JUDGE-v1 config.

Frozen judge (certified 2026-06-12, see notes/track_b_jitter_validation.md):
  model    = gpt-4.1-mini
  prompt   = strict variant
  anchors  = 3 default graded few-shot exemplars (author gold), from
             visual_human_review.json: F10 homepage 0.50 / F01 contact 0.75 /
             F01 academy 1.00
  reps     = 3 repetitions per page, ITEM-LEVEL MAJORITY VOTE (temp=0 is not
             deterministic, so repetition shrinks run-to-run variance)
  provider = chatanywhere (tuzi = validated cheaper-but-slower fallback)

For one generated artifact run it scores each standardized screenshot, writes
`standard_screenshots/visual_score.json` with per-page detail + the artifact
Static Visual Score (mean page score), which the leaderboard builder reads.

Usage:
  py -3.12 scripts/score_track_b_visual.py --item F10_gourmania --run gwdg_qwen36_35b_v9_smoke
  py -3.12 scripts/score_track_b_visual.py --all-dev        # all dev-subset runs with screenshots
"""

import argparse
import json
import sys
import time

import run_visual_judge as J  # reuse frozen low-level helpers

MODEL = "gpt-4.1-mini"
PROVIDER = "chatanywhere"
VARIANT = "strict"
REPS = 3
ANCHOR_SOURCE_RUN = J.RUN  # gwdg_qwen36_35b_v9_smoke (anchors live here)
# (item, page_id) of the 3 frozen default anchors — excluded if we ever score
# the anchor-source run itself (avoids the judge seeing its own gold).
ANCHOR_KEYS = {("F10_gourmania", "01_homepage"),
               ("F01_1daycloud", "04_contact"),
               ("F01_1daycloud", "02_academy")}


def build_frozen_anchors(user):
    """The 3 default author-gold anchors as few-shot messages (frozen)."""
    human = {f"{p['item']}::{p['page_id']}": p
             for p in json.loads((J.OUT_DIR / "visual_human_review.json").read_text("utf-8"))["pages"]}
    keys = ["F10_gourmania::01_homepage", "F01_1daycloud::04_contact", "F01_1daycloud::02_academy"]
    msgs = []
    for k in keys:
        rec = human[k]
        flat = {}
        for d in rec["dimensions"].values():
            flat.update(d)
        png = J.ITEMS / rec["item"] / "generated" / ANCHOR_SOURCE_RUN / "standard_screenshots" / f"{rec['page_id']}.png"
        msgs.append(J.img_msg(user, png))
        gold = {"answers": {it: bool(flat[it]) for it in J.ITEM_IDS}, "confidence": 1.0}
        msgs.append({"role": "assistant", "content": json.dumps(gold)})
    return msgs


def majority(rep_answers):
    """rep_answers: list of {item: bool}. Item-level majority (>=2 of 3)."""
    out = {}
    for it in J.ITEM_IDS:
        votes = [ra[it] for ra in rep_answers if ra.get(it) is not None]
        if not votes:
            out[it] = None
        else:
            out[it] = sum(1 for v in votes if v) * 2 >= len(votes)
    return out


def score_run(item, run, key, base_url, anchors):
    run_dir = J.ITEMS / item / "generated" / run / "standard_screenshots"
    pngs = sorted(run_dir.glob("*.png"))
    if not pngs:
        print(f"  no screenshots in {run_dir}", file=sys.stderr)
        return None
    user = J.USER.replace("Return JSON exactly:", "Look for problems first. Return JSON exactly:")
    pages = []
    for png in pngs:
        if run == ANCHOR_SOURCE_RUN and (item, png.stem) in ANCHOR_KEYS:
            continue  # exclude anchor pages when scoring their own source run
        reps = []
        for r in range(REPS):
            try:
                text = J.call(key, base_url, MODEL, png, J.SYSTEM_STRICT, user, anchors)
                ans, _ = J.parse_answers(text)
                if all(ans[i] is not None for i in J.ITEM_IDS):
                    reps.append({i: bool(ans[i]) for i in J.ITEM_IDS})
            except Exception as e:  # noqa: BLE001 - record and continue
                print(f"  {png.stem} rep{r}: ERROR {str(e)[:120]}", file=sys.stderr)
            time.sleep(0.5)
        if not reps:
            pages.append({"page_id": png.stem, "page_score": None, "reps_ok": 0})
            continue
        maj = majority(reps)
        ps = sum(1 for i in J.ITEM_IDS if maj[i]) / 16
        pages.append({"page_id": png.stem, "page_score": round(ps, 4),
                      "reps_ok": len(reps), "majority": maj})
        print(f"  {png.stem}: score={ps:.4f} (reps {len(reps)}/{REPS})")
    scored = [p["page_score"] for p in pages if p["page_score"] is not None]
    artifact_score = round(sum(scored) / len(scored), 4) if scored else None
    out = {
        "item": item, "run": run,
        "judge": {"model": MODEL, "provider": PROVIDER, "variant": VARIANT,
                  "anchors": "default-3 author-gold (0.50/0.75/1.00)", "reps": REPS,
                  "aggregation": "item-level majority vote", "config": "LB-JUDGE-v1-frozen"},
        "static_visual_score": artifact_score,
        "pages_scored": len(scored), "pages_total": len(pages),
        "pages": pages,
    }
    (run_dir / "visual_score.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"  -> static_visual_score={artifact_score} ({len(scored)}/{len(pages)} pages) "
          f"written to {run_dir/'visual_score.json'}")
    return out


def dev_runs_with_screenshots():
    runs = []
    for item_dir in sorted(J.ITEMS.glob("*")):
        gen = item_dir / "generated"
        if not gen.is_dir():
            continue
        for run_dir in sorted(gen.glob("*")):
            if (run_dir / "standard_screenshots").is_dir() and any((run_dir / "standard_screenshots").glob("*.png")):
                runs.append((item_dir.name, run_dir.name))
    return runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--item")
    ap.add_argument("--run")
    ap.add_argument("--all-dev", action="store_true",
                    help="score every run under items/*/generated/* that has screenshots")
    ap.add_argument("--provider", default=PROVIDER, choices=sorted(J.PROVIDERS))
    args = ap.parse_args()

    key, base_url = J.load_provider(args.provider)
    user = J.USER.replace("Return JSON exactly:", "Look for problems first. Return JSON exactly:")
    anchors = build_frozen_anchors(user)

    targets = dev_runs_with_screenshots() if args.all_dev else [(args.item, args.run)]
    if not args.all_dev and (not args.item or not args.run):
        ap.error("provide --item and --run, or --all-dev")
    for item, run in targets:
        print(f"[{item}/{run}]")
        score_run(item, run, key, base_url, anchors)


if __name__ == "__main__":
    main()
