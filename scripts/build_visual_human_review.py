"""Generate a self-contained human-review page for the static-visual checklist.

Scans the standardized per-page screenshots of the development-subset runs and
emits a single review.html. For each screenshot the reviewer answers the same
16 binary items used by LB-JUDGE-v1 (4 dimensions x 4 items). Scores are
computed live; answers can be exported to JSON for LLM-vs-human comparison.
Progress is auto-saved to the browser's localStorage.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ITEMS = ROOT / "data" / "track_b" / "items"
RUN = "gwdg_qwen36_35b_v9_smoke"
DEV_ITEMS = ["F01_1daycloud", "F03_about_gitlab", "F10_gourmania"]
OUT_DIR = ROOT / "data" / "track_b" / "visual_human_review"

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


def collect_pages():
    pages = []
    for item in DEV_ITEMS:
        sdir = ITEMS / item / "generated" / RUN / "standard_screenshots"
        if not sdir.exists():
            continue
        for png in sorted(sdir.glob("*.png")):
            rel = pathlib.PurePosixPath(
                "..", "items", item, "generated", RUN, "standard_screenshots", png.name
            )
            pages.append({"item": item, "page_id": png.stem, "img": str(rel)})
    return pages


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
const PAGES = __PAGES__;
const DIMS = __DIMS__;
const KEY = "tb_visual_human_review_v1";
let state = JSON.parse(localStorage.getItem(KEY) || "{}");

function pid(p){return p.item + "::" + p.page_id;}
function setAns(i,q,v){const p=PAGES[i];(state[pid(p)]=state[pid(p)]||{})[q]=v;localStorage.setItem(KEY,JSON.stringify(state));render();}
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
  const card=document.createElement("div");card.className="card";
  let panel='<div class="panel"><div class="pagettl">'+p.item+' &middot; '+p.page_id+'</div>';
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
  return {item:p.item,page_id:p.page_id,dimensions:dims,page_score:pageScore(p)};
 });
 const blob=new Blob([JSON.stringify({run:"__RUN__",reviewer:"human",pages:out},null,2)],{type:"application/json"});
 const url=URL.createObjectURL(blob);const a=document.createElement("a");a.href=url;a.download="visual_human_review.json";a.click();
}
function clearAll(){if(confirm("Clear all answers?")){state={};localStorage.removeItem(KEY);render();}}
render();
</script>
</body>
</html>
"""


def main():
    pages = collect_pages()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html = (
        HTML.replace("__PAGES__", json.dumps(pages))
        .replace("__DIMS__", json.dumps([
            {"key": k, "label": label, "items": items} for (k, label, items) in ITEMS_DEF
        ]))
        .replace("__RUN__", RUN)
    )
    out = OUT_DIR / "review.html"
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out} with {len(pages)} screenshots across {len(DEV_ITEMS)} items.")
    print(f"Open in a browser: file:///{out.as_posix()}")


if __name__ == "__main__":
    main()
