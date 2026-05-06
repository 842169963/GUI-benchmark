"""
Track A evaluation for UI screenshot pairwise judging.

Supports two dataset shapes:
1. Paired rows with img_good/img_bad columns.
2. UIClip human rows with image/captions columns, where pairs are built by
   matching well-designed and poor-design examples with the same page caption.

Examples:
    py -3.12 scripts/track_a_eval.py --dry-run --n 50
    py -3.12 scripts/track_a_eval.py --n 50 --model gpt-4o
"""

import argparse
import base64
import json
import os
import random
import re
import time
from collections import defaultdict
from datetime import datetime
from io import BytesIO
from itertools import islice

import datasets.config as datasets_config
from datasets import load_dataset
from openai import OpenAI

# This experiment does not need PyTorch. Some local torch installs can be
# broken on Windows and otherwise interfere with HuggingFace streaming.
datasets_config.TORCH_AVAILABLE = False


DEFAULT_DATASET = "biglab/uiclip_human_data_hf"
DEFAULT_RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

PAIRWISE_PROMPT = """\
You are evaluating two user interface screenshots for visual design quality.

Image A is shown first, Image B is shown second.

Which interface has better visual design overall? Consider layout, visual
hierarchy, clarity, and aesthetic quality.

Reply with ONLY the letter A or B. Nothing else."""


def load_env_file(path):
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


def caption_text(value):
    if isinstance(value, list):
        return " ".join(str(v) for v in value)
    return str(value or "")


def caption_label(text):
    lower = text.lower()
    if "well-designed" in lower or "well designed" in lower:
        return "good"
    if "poor design" in lower or "bad contrast" in lower or "bad proximity" in lower:
        return "bad"
    return None


def normalized_description(text):
    lower = text.lower()
    replacements = [
        "ui screenshot",
        "well-designed",
        "well designed",
        "poor design",
        "bad contrast",
        "bad proximity",
    ]
    for value in replacements:
        lower = lower.replace(value, " ")
    lower = lower.replace("screen displaying", "displaying")
    lower = lower.replace("page displaying", "displaying")
    lower = lower.replace("screen shows to", "displaying")
    lower = lower.replace("screen showing", "displaying")
    lower = re.sub(r"[^a-z0-9]+", " ", lower)
    lower = re.sub(r"\b(the|a|an)\b", " ", lower)
    lower = re.sub(r"\s+", " ", lower).strip()
    return lower


def direct_paired_row(row, pair_id):
    return {
        "pair_id": pair_id,
        "source": "paired_columns",
        "group_key": str(pair_id),
        "caption_good": caption_text(row.get("caption", "")),
        "caption_bad": caption_text(row.get("caption", "")),
        "img_good": row["img_good"],
        "img_bad": row["img_bad"],
    }


def build_pairs(dataset_name, split, n_pairs, seed, max_source_rows):
    stream = load_dataset(dataset_name, split=split, streaming=True)
    first = next(iter(stream))

    if "img_good" in first and "img_bad" in first:
        stream = load_dataset(dataset_name, split=split, streaming=True)
        return [direct_paired_row(row, i) for i, row in enumerate(islice(stream, n_pairs))]

    if "image" not in first or "captions" not in first:
        raise ValueError(f"Unsupported dataset columns: {sorted(first.keys())}")

    random.seed(seed)
    stream = load_dataset(dataset_name, split=split, streaming=True)
    unmatched = defaultdict(lambda: {"good": [], "bad": []})
    pairs = []

    for source_idx, row in enumerate(stream):
        if max_source_rows and source_idx >= max_source_rows:
            break

        text = caption_text(row.get("captions", ""))
        label = caption_label(text)
        if not label:
            continue

        key = normalized_description(text)
        if not key:
            continue

        candidate = {
            "image": row["image"],
            "caption": text,
            "source_idx": source_idx,
        }
        other_label = "bad" if label == "good" else "good"
        bucket = unmatched[key]

        if bucket[other_label]:
            other = bucket[other_label].pop(0)
            if label == "good":
                good = candidate
                bad = other
            else:
                good = other
                bad = candidate
            pairs.append({
                "pair_id": len(pairs),
                "source": "caption_matched",
                "group_key": key,
                "caption_good": good["caption"],
                "caption_bad": bad["caption"],
                "source_idx_good": good["source_idx"],
                "source_idx_bad": bad["source_idx"],
                "img_good": good["image"],
                "img_bad": bad["image"],
            })
            if len(pairs) >= n_pairs:
                break
        else:
            bucket[label].append(candidate)

    random.shuffle(pairs)
    return pairs[:n_pairs]


def ask_pairwise(client, model, img_a, img_b):
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": PAIRWISE_PROMPT},
                {"type": "text", "text": "Image A:"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{pil_to_b64(img_a)}",
                    "detail": "low",
                }},
                {"type": "text", "text": "Image B:"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{pil_to_b64(img_b)}",
                    "detail": "low",
                }},
            ],
        }],
        max_tokens=5,
        temperature=0,
    )
    return response.choices[0].message.content.strip()


def parse_choice(raw):
    upper = raw.upper()
    if upper.startswith("A"):
        return "A"
    if upper.startswith("B"):
        return "B"
    return "INVALID"


def should_stop(exc):
    text = str(exc).lower()
    if "invalid_api_key" in text or "incorrect api key" in text:
        return "invalid OpenAI API key"
    if "insufficient_quota" in text or "billing" in text:
        return "no available OpenAI API quota"
    return None


def evaluate_pair(client, model, pair, order_swap):
    results = []

    runs = [{
        "run": "good_a",
        "img_a": pair["img_good"],
        "img_b": pair["img_bad"],
        "truth": "A",
    }]
    if order_swap:
        runs.append({
            "run": "good_b",
            "img_a": pair["img_bad"],
            "img_b": pair["img_good"],
            "truth": "B",
        })

    for run in runs:
        raw = ask_pairwise(client, model, run["img_a"], run["img_b"])
        choice = parse_choice(raw)
        results.append({
            "run": run["run"],
            "ground_truth": run["truth"],
            "model_choice": choice,
            "raw_response": raw,
            "correct": choice == run["truth"],
        })

    return results


def summarize(results, n_pairs, order_swap):
    flat = [run for item in results for run in item["runs"]]
    accuracy = sum(1 for run in flat if run["correct"]) / len(flat) if flat else 0
    summary = {
        "n_pairs": n_pairs,
        "n_calls": len(flat),
        "raw_accuracy": accuracy,
    }

    if order_swap:
        consistent = 0
        corrected_correct = 0
        run1_correct = run2_correct = 0
        chose_a = chose_b = 0

        for item in results:
            r1, r2 = item["runs"]
            if r1["correct"]:
                run1_correct += 1
            if r2["correct"]:
                run2_correct += 1
            chose_a += sum(1 for r in item["runs"] if r["model_choice"] == "A")
            chose_b += sum(1 for r in item["runs"] if r["model_choice"] == "B")
            r1_chose_good = r1["model_choice"] == "A"
            r2_chose_good = r2["model_choice"] == "B"
            if r1_chose_good == r2_chose_good:
                consistent += 1
                if r1_chose_good:
                    corrected_correct += 1

        summary.update({
            "accuracy_run1_good_a": run1_correct / n_pairs if n_pairs else 0,
            "accuracy_run2_good_b": run2_correct / n_pairs if n_pairs else 0,
            "consistency_rate": consistent / n_pairs if n_pairs else 0,
            "position_bias_rate": 1 - (consistent / n_pairs if n_pairs else 0),
            "corrected_accuracy_consistent_only": (
                corrected_correct / consistent if consistent else 0
            ),
            "n_consistent_pairs": consistent,
            "chose_a": chose_a,
            "chose_b": chose_b,
        })

    return summary


def save_results(args, pairs, results, summary, base_url):
    os.makedirs(args.results_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_model = args.model.replace("/", "-").replace(":", "-")
    path = os.path.join(args.results_dir, f"track_a_eval_{safe_model}_{ts}.json")

    serializable_pairs = []
    for pair in pairs:
        serializable_pairs.append({
            key: value for key, value in pair.items()
            if key not in {"img_good", "img_bad"}
        })

    output = {
        "meta": {
            "model": args.model,
            "dataset": args.dataset,
            "split": args.split,
            "n_pairs_requested": args.n,
            "seed": args.seed,
            "date": datetime.now().isoformat(),
            "prompt": PAIRWISE_PROMPT,
            "order_swap": args.order_swap,
            "base_url": base_url or "https://api.openai.com/v1",
        },
        "summary": summary,
        "pairs": serializable_pairs,
        "results": results,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--split", default="train")
    parser.add_argument("--n", type=int, default=50)
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-source-rows", type=int, default=2500)
    parser.add_argument("--results-dir", default=DEFAULT_RESULTS_DIR)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-order-swap", dest="order_swap", action="store_false")
    parser.set_defaults(order_swap=True)
    args = parser.parse_args()

    load_env()
    print(f"Building {args.n} pairs from {args.dataset} ({args.split})...")
    pairs = build_pairs(args.dataset, args.split, args.n, args.seed, args.max_source_rows)
    print(f"Built {len(pairs)} pairs.")

    if len(pairs) < args.n:
        print(f"WARNING: requested {args.n} pairs but only built {len(pairs)}.")

    for pair in pairs[:5]:
        print(f"Pair {pair['pair_id']:03d}: {pair['group_key']}")
        print(f"  good: {pair['caption_good']}")
        print(f"  bad : {pair['caption_bad']}")

    if args.dry_run:
        print("Dry run complete. No API calls were made.")
        return

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("ERROR: OPENAI_API_KEY not set.")

    base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE")
    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    results = []
    for i, pair in enumerate(pairs):
        print(f"[{i + 1:03d}/{len(pairs):03d}] Querying {args.model}...", end=" ", flush=True)
        try:
            runs = evaluate_pair(client, args.model, pair, args.order_swap)
        except Exception as exc:
            print(f"ERROR: {exc}")
            reason = should_stop(exc)
            if reason:
                raise SystemExit(f"Stopping early: {reason}.")
            runs = [{
                "run": "error",
                "ground_truth": None,
                "model_choice": None,
                "raw_response": str(exc),
                "correct": False,
            }]

        print(" ".join(
            f"{run['run']}={run['model_choice']}/{run['ground_truth']}"
            for run in runs
        ))
        results.append({
            "pair_id": pair["pair_id"],
            "group_key": pair["group_key"],
            "caption_good": pair["caption_good"],
            "caption_bad": pair["caption_bad"],
            "runs": runs,
        })
        time.sleep(0.3)

    summary = summarize(results, len(pairs), args.order_swap)
    print("\nSummary")
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key}: {value:.3f}")
        else:
            print(f"{key}: {value}")

    path = save_results(args, pairs, results, summary, base_url)
    print(f"\nResults saved: {path}")


if __name__ == "__main__":
    main()
