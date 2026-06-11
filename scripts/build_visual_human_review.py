"""Generate a self-contained human-review page for the static-visual checklist.

Scans the standardized per-page screenshots of the development-subset runs and
emits a single review.html. For each screenshot the reviewer answers the same
16 binary items used by LB-JUDGE-v1 (4 dimensions x 4 items). Scores are
computed live; answers can be exported to JSON for LLM-vs-human comparison.
Progress is auto-saved to the browser's localStorage.
"""

import argparse
import base64
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ITEMS = ROOT / "data" / "track_b" / "items"
RUN = "gwdg_qwen36_35b_v9_smoke"
DEV_ITEMS = ["F01_1daycloud", "F03_about_gitlab", "F10_gourmania"]
OUT_DIR = ROOT / "data" / "track_b" / "visual_human_review"

# Extended validation set (2026-06-10): jittered variants of the dev pages
# (known-degraded, see jitter_track_b_pages.py) plus real weak-model artifacts
# from the same TB-GEN-v9 prompt. Used to break range restriction in the
# human-vs-LLM correlation. The review page does NOT display the run name so
# the human rating is quasi-blind w.r.t. which variant a page comes from.
EXTENDED_RUNS = [
    f"{RUN}_jitter_mild",
    f"{RUN}_jitter_severe",
    "gwdg_qwen3_omni_30b_v9_smoke",
    "gwdg_internvl35_30b_v9_smoke",
    "openai_gpt4omini_v9_f10_smoke",
]

ITEMS_DEF = [
    ("layout_hierarchy", "Layout & Visual Hierarchy", [
        ("L1", "There is a clear primary element or focal point."),
        ("L2", "Elements are free of overlap or obvious misalignment."),
        ("L3", "Alignment follows a consistent grid/structure."),
        ("L4", "Spacing and padding are consistent across the page."),
    ]),
    ("information_clarity", "Information Organization & Clarity", [
        ("O1", "Related content is grouped into clear sections."),
        ("O2", "The page is uncluttered, not visually overwhelming."),
        ("O3", "Sections are labelled or easy to tell apart."),
        ("O4", "The main purpose/content is clear at a glance."),
    ]),
    ("typography_readability", "Typography & Readability", [
        ("T1", "Clear text hierarchy (headings vs body distinguishable)."),
        ("T2", "Body text is a comfortably readable size."),
        ("T3", "Line length / text width is reasonable."),
        ("T4", "Font usage is consistent (no clashing typefaces)."),
    ]),
    ("visual_consistency", "Visual Consistency", [
        ("C1", "Buttons and controls share a consistent style."),
        ("C2", "Colour palette is coherent (no clashing colours)."),
        ("C3", "Navigation / header styling is consistent."),
        ("C4", "Repeated components look uniform."),
    ]),
]


def collect_pages(runs=(RUN,)):
    pages = []
    for run in runs:
        for item in DEV_ITEMS:
            sdir = ITEMS / item / "generated" / run / "standard_screenshots"
            if not sdir.exists():
                continue
            for png in sorted(sdir.glob("*.png")):
                rel = pathlib.PurePosixPath(
                    "..", "items", item, "generated", run, "standard_screenshots", png.name
                )
                pages.append({"item": item, "page_id": png.stem, "run": run, "img": str(rel)})
    return pages


def stable_shuffle(pages):
    """Deterministic order that interleaves runs/variants (quasi-blind)."""
    return sorted(pages, key=lambda p: hashlib.md5(
        f"{p['run']}::{p['item']}::{p['page_id']}".encode()).hexdigest())


# Single braces only; placeholders __PAGES__ / __DIMS__ / __RUN__ are replaced.
HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Static-Visual Human Review (16-item checklist)</title>
<style>
 body{font-family:system-ui,Arial,sans-serif;margin:0;background:#f4f5f7;color:#222}
 header{position:sticky;top:0;background:#1f2937;color:#fff;padding:10px 16px;display:flex;gap:12px;align-items:center;z-index:10}
 header button{padding:6px 12px;border:0;border-radius:6px;cursor:pointer;background:#2563eb;color:#fff}
 header .muted{color:#9ca3af;font-size:13px}
 .card{display:flex;gap:16px;margin:16px;background:#fff;border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,.1);padding:16px}
 .shot{flex:0 0 56%;max-height:70vh;overflow:auto;border:1px solid #e5e7eb;border-radius:8px}
 .shot img{width:100%;display:block}
 .panel{flex:1;min-width:280px}
 .dim{margin-bottom:12px}
 .dim h4{margin:6px 0;font-size:14px;color:#374151}
 .q{display:flex;justify-content:space-between;align-items:center;padding:4px 0;font-size:13px;border-bottom:1px dashed #eee}
 .q .btns button{margin-left:6px;border:1px solid #cbd5e1;background:#fff;border-radius:5px;padding:2px 10px;cursor:pointer}
 .q .btns button.yes.active{background:#16a34a;color:#fff;border-color:#16a34a}
 .q .btns button.no.active{background:#dc2626;color:#fff;border-color:#dc2626}
 .score{font-weight:600;color:#111;margin-top:6px}
 .pagettl{font-size:13px;color:#6b7280;margin-bottom:6px}
</style>
</head>
<body>
<header>
 <strong>Static-Visual Human Review</strong>
 <span class="muted" id="progress"></span>
 <span style="flex:1"></span>
 <button onclick="exportJSON()">Export JSON</button>
 <button onclick="clearAll()" style="background:#6b7280">Reset</button>
</header>
<div id="root"></div>
<script>
window.onerror = function(msg){
 var el=document.getElementById("progress");
 if(el) el.textContent = "SCRIPT ERROR: " + msg;
};
const PAGES = __PAGES__;
const DIMS = __DIMS__;
const KEY = "__KEY__";
// localStorage is blocked in some sandboxed previews; fall back to in-memory
// storage so the page still works (export still possible, just no autosave).
let storage;
try { localStorage.setItem("__probe__", "1"); localStorage.removeItem("__probe__"); storage = localStorage; }
catch (e) {
 storage = { _m: {}, getItem(k){ return this._m[k] || null; },
             setItem(k,v){ this._m[k]=v; }, removeItem(k){ delete this._m[k]; } };
}
let state = JSON.parse(storage.getItem(KEY) || "{}");

function pid(p){return (p.run? p.run+"::":"") + p.item + "::" + p.page_id;}
function setAns(i,q,v){const p=PAGES[i];(state[pid(p)]=state[pid(p)]||{})[q]=v;storage.setItem(KEY,JSON.stringify(state));render();}
function allSet(i,v){
 const p=PAGES[i];const a=state[pid(p)]=state[pid(p)]||{};
 DIMS.forEach(d=>d.items.forEach(it=>{a[it[0]]=v;}));
 storage.setItem(KEY,JSON.stringify(state));render();
 // keep the same card in view after re-render
 const el=document.getElementById("card"+i); if(el) el.scrollIntoView({block:"start"});
}
function pageScore(p){
 const a=state[pid(p)]||{};let dims=[];
 for(const d of DIMS){let s=0,n=0;for(const it of d.items){if(a[it[0]]!==undefined){n++;if(a[it[0]])s++;}}dims.push(n?s/d.items.length:null);}
 const valid=dims.filter(x=>x!==null);
 return valid.length?valid.reduce((x,y)=>x+y,0)/dims.length:null;
}
function render(){
 const root=document.getElementById("root");root.innerHTML="";let answered=0;
 PAGES.forEach((p,idx)=>{
  const a=state[pid(p)]||{};const ps=pageScore(p);
  const card=document.createElement("div");card.className="card";card.id="card"+idx;
  let panel='<div class="panel"><div class="pagettl">'+p.item+' &middot; '+p.page_id+
    ' <button style="margin-left:10px;padding:2px 12px;border:1px solid #16a34a;color:#16a34a;background:#fff;border-radius:5px;cursor:pointer" onclick="allSet('+idx+',true)">All Yes</button>'+
    ' <button style="margin-left:4px;padding:2px 12px;border:1px solid #dc2626;color:#dc2626;background:#fff;border-radius:5px;cursor:pointer" onclick="allSet('+idx+',false)">All No</button></div>';
  DIMS.forEach(d=>{
   panel+='<div class="dim"><h4>'+d.label+'</h4>';
   d.items.forEach(it=>{
    const v=a[it[0]];
    panel+='<div class="q"><span>'+it[0]+' '+it[1]+'</span><span class="btns">'+
      '<button class="yes'+(v===true?' active':'')+'" onclick="setAns('+idx+',\\''+it[0]+'\\',true)">Yes</button>'+
      '<button class="no'+(v===false?' active':'')+'" onclick="setAns('+idx+',\\''+it[0]+'\\',false)">No</button>'+
      '</span></div>';
   });
   panel+='</div>';
  });
  panel+='<div class="score">Page score: '+(ps===null?'-':ps.toFixed(3))+'</div></div>';
  card.innerHTML='<div class="shot"><img loading="lazy" src="'+p.img+'"></div>'+panel;
  root.appendChild(card);
  if(Object.keys(a).length===16)answered++;
 });
 document.getElementById("progress").textContent=answered+" / "+PAGES.length+" pages fully answered";
}
function exportJSON(){
 const out=PAGES.map(p=>{
  const a=state[pid(p)]||{};const dims={};
  DIMS.forEach(d=>{dims[d.key]={};d.items.forEach(it=>dims[d.key][it[0]]=a[it[0]]===undefined?null:a[it[0]]);});
  const rec={item:p.item,page_id:p.page_id,dimensions:dims,page_score:pageScore(p)};
  if(p.run)rec.run=p.run;
  return rec;
 });
 const blob=new Blob([JSON.stringify({run:"__RUN__",reviewer:"__REVIEWER__",pages:out},null,2)],{type:"application/json"});
 const url=URL.createObjectURL(blob);const a=document.createElement("a");a.href=url;a.download="__EXPORT__";a.click();
}
function clearAll(){if(confirm("Clear all answers?")){state={};storage.removeItem(KEY);render();}}
render();
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extended", action="store_true",
                    help="build the extended (jitter + weak-model) review page")
    ap.add_argument("--rater", default=None,
                    help="independent-rater id (e.g. rater2): separate page, storage key, and export name")
    ap.add_argument("--embed", action="store_true",
                    help="inline screenshots as base64 data URIs (self-contained file, shareable)")
    args = ap.parse_args()

    if args.extended:
        pages = stable_shuffle(collect_pages(EXTENDED_RUNS))
        out_name, key = "review_extended.html", "tb_visual_human_review_ext_v1"
        run_label, export_name = "extended_validation_2026-06-10", "visual_human_review_extended.json"
        if args.rater:
            out_name = f"review_extended_{args.rater}.html"
            key = f"tb_visual_human_review_ext_{args.rater}"
            export_name = f"visual_human_review_extended_{args.rater}.json"
    else:
        pages = collect_pages()
        out_name, key = "review.html", "tb_visual_human_review_v1"
        run_label, export_name = RUN, "visual_human_review.json"

    if args.embed:
        for p in pages:
            png = OUT_DIR / p["img"]  # img paths are relative to OUT_DIR
            b64 = base64.b64encode(png.resolve().read_bytes()).decode("ascii")
            p["img"] = f"data:image/png;base64,{b64}"
        out_name = out_name.replace(".html", "_embedded.html")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html = (
        HTML.replace("__PAGES__", json.dumps(pages))
        .replace("__DIMS__", json.dumps([
            {"key": k, "label": label, "items": items} for (k, label, items) in ITEMS_DEF
        ]))
        .replace("__RUN__", run_label)
        .replace("__KEY__", key)
        .replace("__EXPORT__", export_name)
        .replace("__REVIEWER__", f"human:{args.rater}" if args.rater else "human")
    )
    out = OUT_DIR / out_name
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out} with {len(pages)} screenshots.")
    print(f"Open in a browser: file:///{out.as_posix()}")


if __name__ == "__main__":
    main()
