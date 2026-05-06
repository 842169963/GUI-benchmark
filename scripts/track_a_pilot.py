"""
Track A Pilot Experiment
========================
Zero-shot pairwise GUI quality judgement using GPT-4o.
Dataset: biglab/jitteredwebsites-merged-224-paraphrased-paired
         (img_good / img_bad pairs, algorithmically labelled)

Purpose: validate prompt template and get a baseline accuracy number.
Results are saved to scripts/results/ as JSON.

Usage:
    Option 1: set OPENAI_API_KEY=sk-...       (Windows cmd)
    Option 2: $env:OPENAI_API_KEY="sk-..."    (PowerShell)
    Option 3: create .env with OPENAI_API_KEY=sk-...
              optional: OPENAI_BASE_URL=https://api.example.com/v1
    py -3.12 scripts/track_a_pilot.py
"""

import os
import json
import random
import base64
import time
from itertools import islice
from io import BytesIO
from datetime import datetime

import datasets.config as datasets_config
from datasets import load_dataset
from openai import OpenAI

# This pilot does not use PyTorch. Disable the optional torch integration so a
# broken local torch install cannot break HuggingFace streaming.
datasets_config.TORCH_AVAILABLE = False

# ── Config ────────────────────────────────────────────────────────────────────
DATASET      = "biglab/jitteredwebsites-merged-224-paraphrased-paired"
N_PAIRS      = 20
MODEL        = "gpt-4o"
SEED         = 42
RESULTS_DIR  = os.path.join(os.path.dirname(__file__), "results")
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

PROMPT = """\
You are evaluating two user interface screenshots for visual design quality.

Image A is shown first, Image B is shown second.

Which interface has better visual design overall? Consider layout, visual \
hierarchy, clarity, and aesthetic quality.

Reply with ONLY the letter A or B. Nothing else."""

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_env_file(path):
    """Load KEY=VALUE pairs from a .env file without overriding existing env vars."""
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value

def load_env():
    load_env_file(os.path.join(PROJECT_ROOT, ".env"))
    load_env_file(os.path.join(os.path.dirname(__file__), ".env"))

def pil_to_b64(img):
    buf = BytesIO()
    img.convert("RGB").save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def ask_model(client, img_a, img_b):
    """Send two images to GPT-4o and return the raw response string."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text",      "text": PROMPT},
                {"type": "text",      "text": "Image A:"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{pil_to_b64(img_a)}",
                    "detail": "low"
                }},
                {"type": "text",      "text": "Image B:"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{pil_to_b64(img_b)}",
                    "detail": "low"
                }},
            ]
        }],
        max_tokens=5,
        temperature=0,
    )
    return response.choices[0].message.content.strip()

def parse_choice(raw):
    """Extract 'A' or 'B' from model response, or 'INVALID'."""
    upper = raw.upper()
    if upper.startswith("A"):
        return "A"
    if upper.startswith("B"):
        return "B"
    return "INVALID"

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    load_env()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit(
            "ERROR: OPENAI_API_KEY not set.\n"
            "  Windows cmd: set OPENAI_API_KEY=sk-...\n"
            "  PowerShell:  $env:OPENAI_API_KEY=\"sk-...\"\n"
            "  Or create D:\\master_thesis\\.env with OPENAI_API_KEY=sk-..."
        )

    api_base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE")
    client = OpenAI(api_key=api_key, base_url=api_base_url) if api_base_url else OpenAI(api_key=api_key)
    random.seed(SEED)

    print(f"Loading {N_PAIRS} pairs from HuggingFace with streaming...")
    ds = list(islice(load_dataset(DATASET, split="train", streaming=True), N_PAIRS))
    print(f"Loaded {len(ds)} pairs.\n")

    results = []
    correct = 0

    for i, item in enumerate(ds):
        img_good = item["img_good"]
        img_bad  = item["img_bad"]
        caption  = item.get("caption", "")

        # Randomly decide which image is A and which is B
        if random.random() > 0.5:
            img_a, img_b, ground_truth = img_good, img_bad, "A"
        else:
            img_a, img_b, ground_truth = img_bad, img_good, "B"

        print(f"[{i+1:02d}/{N_PAIRS}] Querying {MODEL}...", end=" ", flush=True)

        try:
            raw      = ask_model(client, img_a, img_b)
            choice   = parse_choice(raw)
            is_right = (choice == ground_truth)
            if is_right:
                correct += 1

            print(f"model={choice}  truth={ground_truth}  "
                  f"{'✓' if is_right else '✗'}  raw='{raw}'")

            results.append({
                "pair_id":      i,
                "caption":      caption,
                "ground_truth": ground_truth,  # which position held the good image
                "model_choice": choice,
                "raw_response": raw,
                "correct":      is_right,
            })

        except Exception as exc:
            print(f"ERROR: {exc}")
            results.append({"pair_id": i, "error": str(exc), "correct": False})
            error_text = str(exc).lower()
            if "invalid_api_key" in error_text or "incorrect api key" in error_text:
                raise SystemExit("Stopping early: invalid OpenAI API key.")
            if "insufficient_quota" in error_text or "billing" in error_text:
                raise SystemExit("Stopping early: OpenAI account has no available API quota.")

        time.sleep(0.5)   # avoid rate-limit

    # ── Summary ──────────────────────────────────────────────────────────────
    accuracy  = correct / N_PAIRS
    n_chose_a = sum(1 for r in results if r.get("model_choice") == "A")
    n_chose_b = sum(1 for r in results if r.get("model_choice") == "B")

    print(f"\n{'='*50}")
    print(f"Model       : {MODEL}")
    print(f"Pairs       : {N_PAIRS}")
    print(f"Accuracy    : {correct}/{N_PAIRS} = {accuracy:.1%}")
    print(f"Chose A     : {n_chose_a}   Chose B: {n_chose_b}")
    bias = abs(n_chose_a - n_chose_b) / N_PAIRS
    print(f"Position bias (|A-B|/N): {bias:.1%}  "
          f"{'⚠ notable' if bias > 0.3 else 'OK'}")
    print(f"{'='*50}")

    # ── Save ─────────────────────────────────────────────────────────────────
    os.makedirs(RESULTS_DIR, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(RESULTS_DIR, f"track_a_pilot_{MODEL}_{ts}.json")

    output = {
        "meta": {
            "model":   MODEL,
            "dataset": DATASET,
            "n_pairs": N_PAIRS,
            "seed":    SEED,
            "date":    datetime.now().isoformat(),
            "prompt":  PROMPT,
        },
        "summary": {
            "accuracy":  accuracy,
            "correct":   correct,
            "total":     N_PAIRS,
            "chose_a":   n_chose_a,
            "chose_b":   n_chose_b,
            "pos_bias":  bias,
        },
        "results": results,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved → {path}")


if __name__ == "__main__":
    main()
