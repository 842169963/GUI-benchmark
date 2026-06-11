"""Create CSS-jittered (visually degraded) variants of generated Track B pages.

Purpose: discriminative-validity check for the LB-JUDGE visual judge under
range restriction. The dev-subset artifacts are all fairly good, so human/LLM
page scores cluster high and Pearson r is attenuated. Following the UIClip
idea (jitter functions that inject known design defects, arXiv:2404.12500),
this script produces degraded variants with a KNOWN quality ordering
(original > mild > severe), so the judge can be tested on pairwise ranking
accuracy without any new human labels.

Defect categories follow UIClip's jitter families: spacing, layout/alignment,
typography, color clash, and contrast. The CSS blocks are fixed (deterministic,
no RNG) so the experiment is exactly reproducible.

For each dev item, copies
  items/<item>/generated/<run>/index.html
to
  items/<item>/generated/<run>_jitter_<severity>/index.html
with a defect <style> block appended at the end of <head>. Relative resource
references (../../resources/...) stay valid because the new run dir sits at
the same depth.

Usage:
  py -3.12 scripts/jitter_track_b_pages.py            # both severities
  py -3.12 scripts/jitter_track_b_pages.py --severity severe
"""

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ITEMS = ROOT / "data" / "track_b" / "items"
RUN = "gwdg_qwen36_35b_v9_smoke"
DEV_ITEMS = ["F01_1daycloud", "F03_about_gitlab", "F10_gourmania"]

# Mild: subtle but real defects — uneven spacing, slight misalignment, one
# off-size heading level, mildly reduced text contrast. A careful reviewer
# should mark several checklist items false, but the page is still usable.
CSS_MILD = """
/* JITTER-MILD-v1: known injected design defects (UIClip-style). */
/* spacing: uneven section padding */
section:nth-of-type(odd), .section:nth-of-type(odd) { padding-top: 6px !important; padding-bottom: 2px !important; }
section:nth-of-type(even), .section:nth-of-type(even) { padding-top: 56px !important; padding-bottom: 64px !important; }
/* layout: slight heading misalignment */
h2 { transform: translateX(14px); }
h3 { transform: translateX(-9px); }
/* typography: one heading level smaller than body-adjacent levels */
h2 { font-size: 15px !important; }
/* contrast: body text mildly washed out */
p { color: #8a8a8a !important; }
"""

# Severe: obvious multi-category damage — clashing palette, inconsistent
# button styles, font clashes, cramped/exploded spacing, low-contrast text,
# misaligned blocks. Most checklist items should fail.
CSS_SEVERE = """
/* JITTER-SEVERE-v1: known injected design defects (UIClip-style). */
/* spacing: chaotic padding/margins */
section:nth-of-type(odd), .section:nth-of-type(odd), div[class]:nth-of-type(3n) { padding: 2px 1px !important; margin: 0 !important; }
section:nth-of-type(even), .section:nth-of-type(even) { padding: 70px 110px !important; margin-bottom: 90px !important; }
/* layout: misaligned headings and blocks */
h1, h2 { transform: translateX(48px) !important; }
h3, h4 { transform: translateX(-26px) !important; }
div[class]:nth-of-type(2n) { transform: translateX(-15px); }
img { transform: rotate(1.5deg) translateY(6px); }
/* typography: clashing fonts and sizes */
p:nth-of-type(odd), li:nth-of-type(odd) { font-family: "Courier New", monospace !important; font-size: 19px !important; }
p:nth-of-type(even), li:nth-of-type(even) { font-size: 10px !important; letter-spacing: 1.5px !important; }
h2:nth-of-type(odd) { font-family: Georgia, serif !important; font-size: 38px !important; font-style: italic !important; }
h2:nth-of-type(even) { font-size: 13px !important; text-transform: uppercase !important; }
/* color: clashing palette per section */
section:nth-of-type(3n), .section:nth-of-type(3n) { background-color: #ffd0f0 !important; }
section:nth-of-type(3n+1), .section:nth-of-type(3n+1) { background-color: #d8ffd0 !important; }
/* consistency: buttons/links styled differently by position */
button:nth-of-type(odd), .btn:nth-of-type(odd), a.button:nth-of-type(odd) { background: #ff3300 !important; color: #ffffff !important; border-radius: 0 !important; font-size: 18px !important; padding: 14px 30px !important; }
button:nth-of-type(even), .btn:nth-of-type(even), a.button:nth-of-type(even) { background: #00ffcc !important; color: #f8f8f8 !important; border-radius: 24px !important; font-size: 10px !important; padding: 3px 6px !important; border: 3px dashed #5500ff !important; }
/* contrast: low-contrast body text */
p:nth-of-type(3n), li:nth-of-type(3n) { color: #cfcfcf !important; }
"""

SEVERITIES = {"mild": CSS_MILD, "severe": CSS_SEVERE}


def inject(html: str, css: str) -> str:
    block = f"<style data-jitter>{css}</style>"
    lower = html.lower()
    idx = lower.find("</head>")
    if idx != -1:
        return html[:idx] + block + html[idx:]
    return block + html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default=RUN)
    ap.add_argument("--severity", choices=[*SEVERITIES, "all"], default="all")
    args = ap.parse_args()

    severities = list(SEVERITIES) if args.severity == "all" else [args.severity]
    written = []
    for item in DEV_ITEMS:
        src = ITEMS / item / "generated" / args.run / "index.html"
        if not src.exists():
            print(f"SKIP {item}: {src} not found")
            continue
        html = src.read_text(encoding="utf-8", errors="replace")
        for sev in severities:
            out_dir = ITEMS / item / "generated" / f"{args.run}_jitter_{sev}"
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "index.html").write_text(inject(html, SEVERITIES[sev]), encoding="utf-8")
            meta = {
                "source_run": args.run,
                "jitter_severity": sev,
                "jitter_version": f"JITTER-{sev.upper()}-v1",
                "purpose": "visual-judge discriminative-validity check (known quality ordering)",
                "ground_truth": "original > mild > severe",
            }
            (out_dir / "jitter_metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
            written.append(str(out_dir.relative_to(ROOT)))
            print(f"wrote {out_dir.relative_to(ROOT)}")
    print(f"\n{len(written)} jittered runs written")


if __name__ == "__main__":
    main()
