"""Run the LB-JUDGE-v1 static-visual judge over standardized screenshots.

For each screenshot, send the 16-item binary checklist + image to a GWDG/SAIA
multimodal model and record the yes/no answers in the same shape as the human
review export, so human-vs-LLM agreement can be computed.

This is the comparison variant of LB-JUDGE-v1: it requests a flat answers map
(one boolean per item id) plus an overall confidence, which is easier to parse
and to compare against the human export.

Usage:
  python3 scripts/run_visual_judge.py --model internvl3.5-30b-a3b
"""

import argparse
import base64
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
ITEMS = ROOT / "data" / "track_b" / "items"
OUT_DIR = ROOT / "data" / "track_b" / "visual_human_review"
RUN = "gwdg_qwen36_35b_v9_smoke"
DEV_ITEMS = ["F01_1daycloud", "F03_about_gitlab", "F10_gourmania"]

PROVIDERS = {
    "gwdg": {"key_env": "GWDG_API_KEY", "url_env": "GWDG_BASE_URL",
             "default_url": "https://chat-ai.academiccloud.de/v1"},
    "chatanywhere": {"key_env": "OPENAI_API_KEY", "url_env": "OPENAI_BASE_URL",
                     "default_url": "https://api.chatanywhere.org/v1"},
}

ITEM_IDS = ["L1", "L2", "L3", "L4", "O1", "O2", "O3", "O4",
            "T1", "T2", "T3", "T4", "C1", "C2", "C3", "C4"]

SYSTEM = (
    "You are a careful visual UI reviewer. You see ONE screenshot of ONE page of "
    "a web interface. Judge ONLY what is visible. Do not guess about interactivity "
    "or pages you cannot see. Answer each checklist item strictly true or false. "
    "Return ONLY valid JSON, no prose."
)

SYSTEM_STRICT = (
    "You are a STRICT, critical visual UI reviewer evaluating an AI-generated web "
    "page. Most AI-generated pages contain at least some real visual flaws "
    "(inconsistent spacing, weak contrast, misalignment, cramped or oversized "
    "text, clashing colours, uneven components). Your job is to FIND those flaws, "
    "not to approve. Mark an item true ONLY if the criterion is clearly and fully "
    "satisfied with no visible issue. If there is ANY visible problem, or you are "
    "not clearly confident, mark it false. A page that is true on every item is "
    "rare; before answering, identify the single worst visual problem on the page "
    "and make sure the relevant item is false. Return ONLY valid JSON, no prose."
)

USER = """Answer every checklist item for this screenshot (true = page satisfies it).

Layout & Visual Hierarchy
 L1: There is a clear primary element or focal point.
 L2: Elements are free of overlap or obvious misalignment.
 L3: Alignment follows a consistent grid/structure.
 L4: Spacing and padding are consistent across the page.
Information Organization & Clarity
 O1: Related content is grouped into clear sections.
 O2: The page is uncluttered, not visually overwhelming.
 O3: Sections are labelled or easy to tell apart.
 O4: The main purpose/content is clear at a glance.
Typography & Readability
 T1: Clear text hierarchy (headings vs body distinguishable).
 T2: Body text is a comfortably readable size.
 T3: Line length / text width is reasonable.
 T4: Font usage is consistent (no clashing typefaces).
Visual Consistency
 C1: Buttons and controls share a consistent style.
 C2: Colour palette is coherent (no clashing colours).
 C3: Navigation / header styling is consistent.
 C4: Repeated components look uniform.

Return JSON exactly:
{"answers": {"L1": true, "L2": true, "L3": true, "L4": true,
 "O1": true, "O2": true, "O3": true, "O4": true,
 "T1": true, "T2": true, "T3": true, "T4": true,
 "C1": true, "C2": true, "C3": true, "C4": true}, "confidence": 0.0}
"""

DIM_MAP = {
    "layout_hierarchy": ["L1", "L2", "L3", "L4"],
    "information_clarity": ["O1", "O2", "O3", "O4"],
    "typography_readability": ["T1", "T2", "T3", "T4"],
    "visual_consistency": ["C1", "C2", "C3", "C4"],
}


def load_dotenv():
    """Read root .env into a dict without exporting (no secrets in process env)."""
    env = {}
    dotenv = ROOT / ".env"
    if dotenv.exists():
        for line in dotenv.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env

def load_provider(provider):
    """Return (api_key, base_url) for the chosen provider."""
    import os
    cfg = PROVIDERS[provider]
    env = load_dotenv()
    key = os.environ.get(cfg["key_env"]) or env.get(cfg["key_env"])
    base_url = (os.environ.get(cfg["url_env"]) or env.get(cfg["url_env"])
                or cfg["default_url"]).rstrip("/")
    if not key and provider == "gwdg":
        keyfile = ROOT / "api key free gwdg.txt"
        if keyfile.exists():
            for line in keyfile.read_text(encoding="utf-8", errors="replace").splitlines():
                m = re.search(r"API\s*Key\s*[:=]\s*([A-Za-z0-9._-]{20,})", line, re.I)
                if m:
                    key = m.group(1).strip()
                    break
    if not key:
        raise SystemExit(f"No API key for provider {provider!r} ({cfg['key_env']} in env or .env).")
    return key.strip(), base_url


def collect_pages(run=RUN):
    pages = []
    for item in DEV_ITEMS:
        sdir = ITEMS / item / "generated" / run / "standard_screenshots"
        for png in sorted(sdir.glob("*.png")):
            pages.append({"item": item, "page_id": png.stem, "path": png})
    return pages


def parse_answers(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("no JSON object in response")
    obj = json.loads(m.group(0))
    ans = obj.get("answers", obj)
    out = {}
    for k in ITEM_IDS:
        v = ans.get(k)
        out[k] = bool(v) if isinstance(v, bool) else (None if v is None else bool(v))
    return out, obj.get("confidence")


def img_msg(text, png):
    b64 = base64.b64encode(png.read_bytes()).decode("ascii")
    return {"role": "user", "content": [
        {"type": "text", "text": text},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
    ]}


def call(key, base_url, model, png, system, user, fewshot_msgs=None):
    messages = [{"role": "system", "content": system}]
    if fewshot_msgs:
        messages.extend(fewshot_msgs)
    messages.append(img_msg(user, png))
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 800,
        "temperature": 0.0,
    }
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"authorization": f"Bearer {key}", "content-type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="internvl3.5-30b-a3b")
    ap.add_argument("--run", default=RUN,
                    help="run directory name under items/<item>/generated/ to judge")
    ap.add_argument("--provider", choices=sorted(PROVIDERS), default="gwdg")
    ap.add_argument("--variant", choices=["base", "strict"], default="base")
    ap.add_argument("--fewshot", action="store_true",
                    help="prepend human-labelled example screenshots as calibration")
    args = ap.parse_args()

    system = SYSTEM_STRICT if args.variant == "strict" else SYSTEM
    user = USER
    if args.variant == "strict":
        user = USER.replace(
            "Return JSON exactly:",
            "Look for problems first. Return JSON exactly:",
        )

    # Curated calibration examples (mix of weak and strong pages), pulled from
    # the human review. These pages are excluded from evaluation.
    EXAMPLE_KEYS = [
        "F10_gourmania::01_homepage",   # human 0.50 (many false)
        "F01_1daycloud::04_contact",    # human 0.75
        "F01_1daycloud::02_academy",    # human 1.00 (all true)
    ]
    fewshot_msgs, example_keys = None, set()
    if args.fewshot:
        human = {f"{p['item']}::{p['page_id']}": p
                 for p in json.loads((OUT_DIR / "visual_human_review.json").read_text("utf-8"))["pages"]}
        fewshot_msgs = []
        for k in EXAMPLE_KEYS:
            rec = human[k]
            flat = {}
            for d in rec["dimensions"].values():
                flat.update(d)
            png = ITEMS / rec["item"] / "generated" / RUN / "standard_screenshots" / f"{rec['page_id']}.png"
            fewshot_msgs.append(img_msg(user, png))
            gold = {"answers": {it: bool(flat[it]) for it in ITEM_IDS}, "confidence": 1.0}
            fewshot_msgs.append({"role": "assistant", "content": json.dumps(gold)})
            example_keys.add(k)

    key, base_url = load_provider(args.provider)
    pages = collect_pages(args.run)
    results = []
    for i, p in enumerate(pages, 1):
        key_pp = f"{p['item']}::{p['page_id']}"
        if key_pp in example_keys:
            continue
        rec = {"item": p["item"], "page_id": p["page_id"]}
        try:
            text = call(key, base_url, args.model, p["path"], system, user, fewshot_msgs)
            ans, conf = parse_answers(text)
            dims = {dk: {it: ans[it] for it in ids} for dk, ids in DIM_MAP.items()}
            valid = [v for v in ans.values() if v is not None]
            rec["dimensions"] = dims
            rec["page_score"] = round(sum(1 for v in valid if v) / 16, 4) if len(valid) == 16 else None
            rec["confidence"] = conf
            print(f"[{i}/{len(pages)}] {p['item']}/{p['page_id']}: score={rec['page_score']} conf={conf}")
        except (urllib.error.URLError, ValueError, KeyError, TimeoutError) as e:
            rec["error"] = str(e)[:200]
            rec["dimensions"] = None
            rec["page_score"] = None
            print(f"[{i}/{len(pages)}] {p['item']}/{p['page_id']}: ERROR {rec['error']}", file=sys.stderr)
        results.append(rec)
        time.sleep(1.0)

    out = {"run": args.run, "reviewer": f"llm:{args.model}:{args.variant}", "pages": results}
    safe_model = re.sub(r"[^A-Za-z0-9._-]", "_", args.model)
    suffix = "" if args.variant == "base" else f"_{args.variant}"
    if args.fewshot:
        suffix += "_fewshot"
    if args.run != RUN:
        run_tag = re.sub(r"[^A-Za-z0-9._-]", "_", args.run.replace(RUN, "").strip("_"))
        suffix += f"_{run_tag}"
    out_path = OUT_DIR / f"llm_judge_{safe_model}{suffix}.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    ok = sum(1 for r in results if r["page_score"] is not None)
    print(f"\nWrote {out_path} ({ok}/{len(results)} pages judged)")


if __name__ == "__main__":
    main()
