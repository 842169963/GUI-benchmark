"""
Track A — Order-Swap Experiment
================================
Each pair is judged TWICE:
  Run 1: img_good shown as A, img_bad shown as B
  Run 2: order swapped — img_bad shown as A, img_good shown as B

Key metrics:
  - Accuracy per run (does the model pick the good image?)
  - Consistency rate (does the model pick the SAME image both times?)
  - Position bias rate (how often does the model flip when order changes?)
  - Corrected accuracy (only pairs where model was consistent)

Usage:
    set OPENAI_API_KEY=sk-...
    python scripts/track_a_order_swap.py
"""

import os, json, base64, time
from io import BytesIO
from datetime import datetime
from itertools import islice

import datasets.config as datasets_config
from datasets import load_dataset
from openai import OpenAI

datasets_config.TORCH_AVAILABLE = False

# ── Config ────────────────────────────────────────────────────────────────────
DATASET     = "biglab/jitteredwebsites-merged-224-paraphrased-paired"
N_PAIRS     = 20
MODEL       = "gpt-4o"
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

PROMPT = """\
You are evaluating two user interface screenshots for visual design quality.

Image A is shown first, Image B is shown second.

Which interface has better visual design overall? Consider layout, visual \
hierarchy, clarity, and aesthetic quality.

Reply with ONLY the letter A or B. Nothing else."""

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_env():
    path = os.path.join(PROJECT_ROOT, ".env")
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip(); v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v

def pil_to_b64(img):
    buf = BytesIO()
    img.convert("RGB").save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def ask_model(client, img_a, img_b):
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": [
            {"type": "text",      "text": PROMPT},
            {"type": "text",      "text": "Image A:"},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{pil_to_b64(img_a)}", "detail": "low"}},
            {"type": "text",      "text": "Image B:"},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{pil_to_b64(img_b)}", "detail": "low"}},
        ]}],
        max_tokens=5,
        temperature=0,
    )
    return resp.choices[0].message.content.strip()

def parse(raw):
    u = raw.upper()
    if u.startswith("A"): return "A"
    if u.startswith("B"): return "B"
    return "INVALID"

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    load_env()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("ERROR: OPENAI_API_KEY not set.")

    base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE")
    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    print(f"Loading {N_PAIRS} pairs (streaming)...")
    pairs = list(islice(load_dataset(DATASET, split="train", streaming=True), N_PAIRS))
    print(f"Loaded {len(pairs)} pairs. Each pair judged TWICE (original + swapped).\n")

    results = []
    # counters
    correct_r1 = correct_r2 = consistent = 0

    for i, item in enumerate(pairs):
        good = item["img_good"]
        bad  = item["img_bad"]
        cap  = item.get("caption", "")

        print(f"[{i+1:02d}/{N_PAIRS}]", end=" ")

        # ── Run 1: good=A, bad=B  →  correct answer is "A" ──────────────────
        raw1   = ask_model(client, good, bad)
        c1     = parse(raw1)
        ok1    = (c1 == "A")
        if ok1: correct_r1 += 1
        print(f"Run1(good=A): model={c1} {'OK' if ok1 else 'XX'}", end="   ")
        time.sleep(0.3)

        # ── Run 2: bad=A, good=B  →  correct answer is "B" ──────────────────
        raw2   = ask_model(client, bad, good)
        c2     = parse(raw2)
        ok2    = (c2 == "B")
        if ok2: correct_r2 += 1
        print(f"Run2(good=B): model={c2} {'OK' if ok2 else 'XX'}", end="   ")
        time.sleep(0.3)

        # ── Consistency: model picked same IMAGE both times? ─────────────────
        # Run1 chose "A" (=good) AND Run2 chose "B" (=good) → consistent
        # Run1 chose "B" (=bad)  AND Run2 chose "A" (=bad)  → consistent (wrong but stable)
        # Any other combo → inconsistent (position-biased)
        r1_chose_good = (c1 == "A")
        r2_chose_good = (c2 == "B")
        is_consistent = (r1_chose_good == r2_chose_good)
        if is_consistent: consistent += 1
        print(f"Consistent: {'YES' if is_consistent else 'NO-BIAS'}")

        results.append({
            "pair_id":        i,
            "caption":        cap,
            # Run 1 (good=A)
            "run1_choice":    c1,
            "run1_correct":   ok1,
            "run1_raw":       raw1,
            # Run 2 (good=B)
            "run2_choice":    c2,
            "run2_correct":   ok2,
            "run2_raw":       raw2,
            # Consistency
            "consistent":     is_consistent,
            "chose_good_r1":  r1_chose_good,
            "chose_good_r2":  r2_chose_good,
        })

    # ── Summary ───────────────────────────────────────────────────────────────
    acc_r1     = correct_r1 / N_PAIRS
    acc_r2     = correct_r2 / N_PAIRS
    cons_rate  = consistent / N_PAIRS
    bias_rate  = 1 - cons_rate

    # Corrected accuracy: only pairs the model answered consistently
    consistent_results = [r for r in results if r["consistent"]]
    corr_acc = (
        sum(1 for r in consistent_results if r["chose_good_r1"])
        / len(consistent_results)
        if consistent_results else 0
    )

    print(f"\n{'='*55}")
    print(f"Model              : {MODEL}")
    print(f"Pairs              : {N_PAIRS}")
    print(f"─────────────────────────────────────────────────────")
    print(f"Accuracy  Run1 (good=A) : {correct_r1}/{N_PAIRS} = {acc_r1:.1%}")
    print(f"Accuracy  Run2 (good=B) : {correct_r2}/{N_PAIRS} = {acc_r2:.1%}")
    print(f"─────────────────────────────────────────────────────")
    print(f"Consistency rate        : {consistent}/{N_PAIRS} = {cons_rate:.1%}")
    print(f"Position bias rate      : {N_PAIRS-consistent}/{N_PAIRS} = {bias_rate:.1%}")
    print(f"─────────────────────────────────────────────────────")
    print(f"Corrected accuracy      : {corr_acc:.1%}  "
          f"(on {len(consistent_results)} consistent pairs)")
    print(f"{'='*55}")

    # ── Save ──────────────────────────────────────────────────────────────────
    os.makedirs(RESULTS_DIR, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(RESULTS_DIR, f"track_a_orderswap_{MODEL}_{ts}.json")

    output = {
        "meta": {
            "model":   MODEL,
            "dataset": DATASET,
            "n_pairs": N_PAIRS,
            "date":    datetime.now().isoformat(),
            "prompt":  PROMPT,
        },
        "summary": {
            "accuracy_run1":       acc_r1,
            "accuracy_run2":       acc_r2,
            "consistency_rate":    cons_rate,
            "position_bias_rate":  bias_rate,
            "corrected_accuracy":  corr_acc,
            "n_consistent_pairs":  len(consistent_results),
        },
        "results": results,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved → {path}")


if __name__ == "__main__":
    main()
