"""
Export a visual review page for Track A derived pairs.

The Track A result JSON stores source indices instead of image bytes. This
script re-loads the source dataset, saves the good/bad screenshots for each
pair, and creates an HTML page for manual pair-quality inspection.

Usage:
    py -3.12 scripts/export_pair_review.py scripts/results/track_a_eval_....json
"""

import argparse
import html
import json
import os
from itertools import islice

import datasets.config as datasets_config
from datasets import load_dataset

datasets_config.TORCH_AVAILABLE = False


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


def load_needed_rows(dataset, split, pairs):
    needed = set()
    for pair in pairs:
        if "source_idx_good" in pair:
            needed.add(pair["source_idx_good"])
        if "source_idx_bad" in pair:
            needed.add(pair["source_idx_bad"])

    if not needed:
        raise ValueError("No source_idx_good/source_idx_bad fields found in result JSON.")

    max_idx = max(needed)
    rows = {}
    stream = load_dataset(dataset, split=split, streaming=True)
    for idx, row in enumerate(islice(stream, max_idx + 1)):
        if idx in needed:
            rows[idx] = row
    return rows


def result_by_pair_id(results):
    return {item["pair_id"]: item for item in results}


def pair_result_label(item):
    if not item:
        return "no result"
    runs = item.get("runs", [])
    parts = []
    for run in runs:
        parts.append(
            f"{run.get('run')}={run.get('model_choice')}/{run.get('ground_truth')}"
        )
    return " | ".join(parts)


def export_review(result_path):
    with open(result_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data["meta"]
    pairs = data["pairs"]
    results = result_by_pair_id(data.get("results", []))

    stem = os.path.splitext(os.path.basename(result_path))[0]
    out_dir = os.path.join(os.path.dirname(result_path), f"{stem}_pair_review")
    img_dir = os.path.join(out_dir, "images")
    os.makedirs(img_dir, exist_ok=True)

    rows = load_needed_rows(meta["dataset"], meta["split"], pairs)

    cards = []
    for i, pair in enumerate(pairs, 1):
        good_idx = pair["source_idx_good"]
        bad_idx = pair["source_idx_bad"]
        good_path = os.path.join(img_dir, f"pair_{i:03d}_good.jpg")
        bad_path = os.path.join(img_dir, f"pair_{i:03d}_bad.jpg")

        rows[good_idx]["image"].convert("RGB").save(good_path, quality=92)
        rows[bad_idx]["image"].convert("RGB").save(bad_path, quality=92)

        rel_good = os.path.relpath(good_path, out_dir).replace("\\", "/")
        rel_bad = os.path.relpath(bad_path, out_dir).replace("\\", "/")
        run_label = pair_result_label(results.get(pair["pair_id"]))

        cards.append(f"""
        <section class="pair">
          <div class="pair-head">
            <h2>Pair {i:03d} <span>source pair_id={pair['pair_id']}</span></h2>
            <p class="key">{html.escape(pair['group_key'])}</p>
            <p class="run">{html.escape(run_label)}</p>
            <label><input type="checkbox" class="mismatch" data-review-id="{i:03d}" data-pair-id="{pair['pair_id']}" data-key="{html.escape(pair['group_key'])}"> mismatch / needs review</label>
          </div>
          <div class="imgs">
            <figure>
              <img src="{rel_good}" alt="good screenshot">
              <figcaption><strong>Good</strong><br>{html.escape(pair['caption_good'])}<br><small>source_idx={good_idx}</small></figcaption>
            </figure>
            <figure>
              <img src="{rel_bad}" alt="bad screenshot">
              <figcaption><strong>Bad</strong><br>{html.escape(pair['caption_bad'])}<br><small>source_idx={bad_idx}</small></figcaption>
            </figure>
          </div>
        </section>
        """)

    html_text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Track A Pair Review</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f7f4; color: #202124; }}
    header {{ position: sticky; top: 0; z-index: 1; padding: 18px 24px; background: #ffffff; border-bottom: 1px solid #ddd; }}
    h1 {{ margin: 0 0 6px; font-size: 22px; }}
    header p {{ margin: 4px 0; color: #5f6368; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 24px; }}
    .pair {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 22px; overflow: hidden; }}
    .pair-head {{ padding: 14px 16px; border-bottom: 1px solid #e6e6e6; }}
    .pair h2 {{ margin: 0 0 6px; font-size: 18px; }}
    .pair h2 span {{ color: #777; font-size: 13px; font-weight: normal; }}
    .key, .run {{ margin: 5px 0; color: #4a4f55; }}
    label {{ display: inline-flex; align-items: center; gap: 8px; margin-top: 8px; font-weight: bold; }}
    input {{ width: 18px; height: 18px; }}
    .imgs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0; }}
    figure {{ margin: 0; padding: 16px; border-right: 1px solid #eee; }}
    figure:last-child {{ border-right: 0; }}
    img {{ width: 100%; max-height: 760px; object-fit: contain; background: #f0f0f0; border: 1px solid #ddd; }}
    figcaption {{ margin-top: 10px; line-height: 1.45; }}
    small {{ color: #777; }}
    @media (max-width: 800px) {{ .imgs {{ grid-template-columns: 1fr; }} figure {{ border-right: 0; border-bottom: 1px solid #eee; }} }}
  </style>
</head>
<body>
  <header>
    <h1>Track A Pair Review</h1>
    <p>Source: {html.escape(os.path.basename(result_path))}</p>
    <p>Dataset: {html.escape(meta['dataset'])}, pairs: {len(pairs)}</p>
    <button id="copy-review">Copy checked mismatches</button>
    <textarea id="review-output" rows="4" readonly placeholder="Checked mismatch IDs will appear here."></textarea>
  </header>
  <main>
    {''.join(cards)}
  </main>
  <script>
    const button = document.getElementById('copy-review');
    const output = document.getElementById('review-output');
    button.addEventListener('click', async () => {{
      const checked = [...document.querySelectorAll('.mismatch:checked')].map(box => ({{
        review_id: box.dataset.reviewId,
        pair_id: Number(box.dataset.pairId),
        group_key: box.dataset.key
      }}));
      const text = JSON.stringify(checked, null, 2);
      output.value = text;
      try {{
        await navigator.clipboard.writeText(text);
        button.textContent = `Copied ${{checked.length}} mismatches`;
      }} catch (err) {{
        button.textContent = `Listed ${{checked.length}} mismatches`;
      }}
    }});
  </script>
</body>
</html>
"""
    html_path = os.path.join(out_dir, "review.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_text)
    return html_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("result_json")
    args = parser.parse_args()
    result_path = args.result_json
    if not os.path.isabs(result_path):
        result_path = os.path.join(PROJECT_ROOT, result_path)
    html_path = export_review(result_path)
    print(html_path)


if __name__ == "__main__":
    main()
