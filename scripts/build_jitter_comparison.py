"""Build a side-by-side original-vs-mild-jitter comparison page.

For each dev-subset route, shows the original screenshot next to the
JITTER-MILD-v1 screenshot, with the injected CSS perturbations documented and
the human page scores (original session vs extended session) displayed, so the
rater can re-inspect why mild was scored >= original.

Output: data/track_b/visual_human_review/jitter_mild_comparison.html
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ITEMS = ROOT / "data" / "track_b" / "items"
REVIEW_DIR = ROOT / "data" / "track_b" / "visual_human_review"
RUN = "gwdg_qwen36_35b_v9_smoke"
MILD = f"{RUN}_jitter_mild"
DEV_ITEMS = ["F01_1daycloud", "F03_about_gitlab", "F10_gourmania"]

PERTURBATIONS = [
    ("Section 间距不均", "奇数 section 上下 padding 压到 6px/2px，偶数 section 撑到 56px/64px —— 垂直节奏被打乱（对应检查项 L4）"),
    ("标题错位", "所有 h2 右移 14px、h3 左移 9px —— 与栅格不再对齐（对应 L2/L3）"),
    ("标题字号异常", "所有 h2 强制 15px，常小于正文 —— 层级感被破坏（对应 T1）"),
    ("正文对比度降低", "所有段落文字改为 #8a8a8a 浅灰 —— 可读性下降（对应 T2）"),
]


def load_scores(path, want_run):
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for p in data["pages"]:
        run = p.get("run", RUN)
        if run == want_run and p.get("page_score") is not None:
            out[f"{p['item']}::{p['page_id']}"] = p["page_score"]
    return out


def main():
    orig_scores = load_scores(REVIEW_DIR / "visual_human_review.json", RUN)
    mild_scores = load_scores(REVIEW_DIR / "visual_human_review_extended.json", MILD)

    rows = []
    for item in DEV_ITEMS:
        odir = ITEMS / item / "generated" / RUN / "standard_screenshots"
        for png in sorted(odir.glob("*.png")):
            mild_png = ITEMS / item / "generated" / MILD / "standard_screenshots" / png.name
            if not mild_png.exists():
                continue
            key = f"{item}::{png.stem}"
            rows.append({
                "item": item, "page": png.stem,
                "orig": f"../items/{item}/generated/{RUN}/standard_screenshots/{png.name}",
                "mild": f"../items/{item}/generated/{MILD}/standard_screenshots/{png.name}",
                "orig_score": orig_scores.get(key), "mild_score": mild_scores.get(key),
            })

    pert_html = "".join(
        f"<li><b>{t}</b>：{d}</li>" for t, d in PERTURBATIONS)
    cards = []
    for r in rows:
        os_ = "未标注" if r["orig_score"] is None else f"{r['orig_score']:.3f}"
        ms_ = "未标注" if r["mild_score"] is None else f"{r['mild_score']:.3f}"
        hint = ""
        if r["orig_score"] is not None and r["mild_score"] is not None:
            if r["mild_score"] > r["orig_score"]:
                hint = ' <span style="color:#dc2626">← mild 被打得更高</span>'
            elif r["mild_score"] == r["orig_score"]:
                hint = ' <span style="color:#6b7280">（持平）</span>'
        cards.append(f"""
<div class="card">
 <h3>{r['item']} · {r['page']}{hint}</h3>
 <div class="pair">
  <figure><figcaption>原版 — 你的评分: {os_}</figcaption>
   <img loading="lazy" src="{r['orig']}"></figure>
  <figure><figcaption>JITTER-MILD-v1 — 你的评分: {ms_}</figcaption>
   <img loading="lazy" src="{r['mild']}"></figure>
 </div>
</div>""")

    html = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8">
<title>原版 vs mild-jitter 对照（{len(rows)} 页）</title>
<style>
 body{{font-family:system-ui,Arial,sans-serif;margin:0;background:#f4f5f7;color:#222}}
 header{{background:#1f2937;color:#fff;padding:14px 20px}}
 header ul{{margin:8px 0 0;color:#d1d5db;font-size:14px}}
 .card{{margin:16px;background:#fff;border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,.1);padding:14px}}
 .card h3{{margin:2px 0 10px;font-size:15px}}
 .pair{{display:flex;gap:12px}}
 figure{{flex:1;margin:0;border:1px solid #e5e7eb;border-radius:8px;overflow:auto;max-height:75vh}}
 figcaption{{position:sticky;top:0;background:#f9fafb;padding:6px 10px;font-size:13px;font-weight:600;border-bottom:1px solid #e5e7eb}}
 img{{width:100%;display:block}}
</style></head><body>
<header><strong>原版 vs JITTER-MILD-v1 对照</strong>（共 {len(rows)} 页）
<div style="margin-top:6px;font-size:14px">注入的 4 类扰动（每页相同，确定性 CSS）：</div>
<ul>{pert_html}</ul>
<div style="font-size:13px;color:#9ca3af">观察建议：盯 h2 标题（是否偏小、右移）、段落文字颜色（是否发灰）、相邻 section 的留白是否一密一疏。</div>
</header>
{''.join(cards)}
</body></html>"""

    out = REVIEW_DIR / "jitter_mild_comparison.html"
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out} ({len(rows)} pairs)")


if __name__ == "__main__":
    main()
