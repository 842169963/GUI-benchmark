"""
Generate Track B GUI implementations from normalized Vision2Web items.

The script writes one generated HTML file plus metadata under:
    data/track_b/items/<item_id>/generated/<run_name>/

Examples:
    py -3.12 scripts/generate_track_b_ui.py --dry-run --item F01_1daycloud
    py -3.12 scripts/generate_track_b_ui.py --item F01_1daycloud --provider chatanywhere-anthropic --model claude-sonnet-4-5-20250929
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS_DIR = PROJECT_ROOT / "data" / "track_b" / "items"
DEFAULT_PROMPT_ID = "TB-GEN-v6"

SYSTEM_PROMPT = """\
You are a senior frontend engineer building a benchmark submission for a GUI evaluation study.
Create a polished, working website implementation that can be opened directly from a local index.html file.
"""

USER_PROMPT_TEMPLATES = {
    "TB-GEN-v6": """\
Prompt ID: TB-GEN-v6

Build a single-file HTML implementation for the Track B GUI item below.

Requirements:
- Return exactly one complete HTML document, including <!doctype html>, <html>, <head>, and <body>.
- The document must end with </html>. Do not stop in the middle of an element, table, script, or style block.
- Put CSS and JavaScript inside the same file. Do not require a build step, package manager, backend, or network access.
- You may use local assets from the provided resource paths. The generated index.html will be saved inside:
  data/track_b/items/{item_id}/generated/<run_name>/
  Therefore resource paths should be referenced as ../../resources/<subpath>.
- Match the supplied prototype screenshots as closely as possible while still implementing the written requirements.
- Implement the navigation and interactions needed by the workflow checks. Clickable navigation items must update visible content without requiring a server or page reload.
- Any function used by onclick, addEventListener, forms, menus, tabs, accordions, or navigation must be defined in the same HTML file before the closing </body>.
- Do not use placeholder-only controls for workflow actions. If a workflow says to click "Register to Vote", "Learn more", "Resources", or "Local Forms", that visible control must change the displayed page/section to the expected content.
- Workflow-required controls must be <a> or <button> elements. Do not use inert <div> controls for workflow actions.
- For links not required by the workflow, plain href="#" placeholders are acceptable. For workflow-required controls, href="#" is acceptable only when paired with working JavaScript.
- Keep the implementation compact enough to finish completely. Implement the workflow-required pages and content first; summarize non-required secondary content instead of producing long exhaustive tables. Use at most 6 table rows per table and at most 5 bullets per list.
- The primary evaluation viewport is desktop. Optimize for 1365px and 1920px wide browser rendering. Mobile/responsive quality is not part of the current hard gate.
- If the requirement mentions downloadable files such as PDF forms but no PDF assets are provided, represent them as visible labelled links or table entries. Do not invent real file contents.
- Secondary navigation items that are not required by the workflow may remain non-functional placeholders, but they should be visibly present when the requirement asks for them.
- Include a small self-test object on window.__TRACK_B_ROUTES listing the route ids implemented for workflow navigation.
- Use the route contract below exactly. Do not invent different route ids. Every route id must appear as an element id and in window.__TRACK_B_ROUTES.
- The first route in window.__TRACK_B_ROUTES is the default page shown on initial load. It must be the homepage/home route when one is listed.
- Put the JavaScript route handler before </body>. It must define function showPage(routeId), set the selected route visible, hide all other [data-track-route] sections, update the URL hash with history.replaceState when available, and call window.scrollTo(0, 0). Do not use location.hash assignment in a way that scrolls directly to the section anchor.
- Prefer accessible semantic HTML, visible focus states, responsive layout, and deterministic behavior.
- Do not include explanations, markdown fences, or comments outside the HTML document.

Required route contract:
{route_contract}

Required minimal JavaScript behavior:
<script>
window.__TRACK_B_ROUTES = {route_ids_json};
function showPage(routeId) {{
  if (!window.__TRACK_B_ROUTES.includes(routeId)) return;
  document.querySelectorAll('[data-track-route]').forEach(function(section) {{
    section.hidden = section.id !== routeId;
  }});
  document.querySelectorAll('[data-route-target]').forEach(function(link) {{
    link.setAttribute('aria-current', link.dataset.routeTarget === routeId ? 'page' : 'false');
  }});
  if (history.replaceState) {{
    history.replaceState(null, '', '#' + routeId);
  }}
  window.scrollTo(0, 0);
}}
document.addEventListener('DOMContentLoaded', function() {{
  var initial = location.hash ? location.hash.slice(1) : window.__TRACK_B_ROUTES[0];
  showPage(window.__TRACK_B_ROUTES.includes(initial) ? initial : window.__TRACK_B_ROUTES[0]);
}});
</script>

Item ID: {item_id}
Source task: {source_task_name}
Source level: {source_level}
Use for dynamic validation: {use_for_dynamic}

Normalized requirement:
{requirement}

Workflow checks:
{workflow}

Available local resource paths:
{resource_paths}

Prototype screenshots are attached after this text in this order:
{prototype_list}
""",
    "TB-GEN-v7": """\
Prompt ID: TB-GEN-v7

Build a compact, complete single-file HTML implementation for the Track B GUI item below.

Hard requirements:
- Return exactly one complete HTML document, including <!doctype html>, <html>, <head>, and <body>.
- The document must end with </html>. Completeness is more important than decorative detail.
- Put CSS and JavaScript inside the same file. Do not require a build step, package manager, backend, or network access.
- The generated index.html will be saved inside:
  data/track_b/items/{item_id}/generated/<run_name>/
  Local assets must be referenced as ../../resources/<subpath>.
- Use the supplied prototype screenshots for visual structure, spacing, typography, colors, and page hierarchy, but implement a compact version.
- Implement the workflow-required routes and interactions first. Do not spend tokens on exhaustive secondary pages.
- Workflow-required controls must be visible <a> or <button> elements and must change the displayed route/section with JavaScript.
- Secondary navigation items may be visible non-functional placeholders if the workflow does not require them.
- If downloadable files such as PDFs are mentioned but no files are provided, show labelled text links or table entries. Do not invent file contents.
- Primary evaluation viewport is desktop: optimize for 1365px and 1920px. Mobile responsiveness is not a hard gate.
- Keep CSS and JS short. Avoid animations, large design systems, repeated footer markup, and long prose copied from the requirement.

Compactness limits:
- For each route, use at most one main heading, one short summary paragraph, one compact key-info block, and one table or list when needed.
- Use at most 4 table rows per table and at most 4 bullets per list.
- Reuse shared header, sidebar, card, button, and footer styles.
- If output budget feels tight, reduce visual/detail text. Never omit closing tags, route sections, workflow buttons, or the route handler.

Route contract:
{route_contract}

Required minimal JavaScript behavior:
<script>
window.__TRACK_B_ROUTES = {route_ids_json};
function showPage(routeId) {{
  if (!window.__TRACK_B_ROUTES.includes(routeId)) return;
  document.querySelectorAll('[data-track-route]').forEach(function(section) {{
    section.hidden = section.id !== routeId;
  }});
  document.querySelectorAll('[data-route-target]').forEach(function(link) {{
    link.setAttribute('aria-current', link.dataset.routeTarget === routeId ? 'page' : 'false');
  }});
  if (history.replaceState) {{
    history.replaceState(null, '', '#' + routeId);
  }}
  setTimeout(function() {{ window.scrollTo(0, 0); }}, 0);
}}
document.addEventListener('DOMContentLoaded', function() {{
  var initial = location.hash ? location.hash.slice(1) : window.__TRACK_B_ROUTES[0];
  showPage(window.__TRACK_B_ROUTES.includes(initial) ? initial : window.__TRACK_B_ROUTES[0]);
}});
</script>

Item ID: {item_id}
Source task: {source_task_name}
Source level: {source_level}
Use for dynamic validation: {use_for_dynamic}

Normalized requirement:
{requirement}

Workflow checks:
{workflow}

Available local resource paths:
{resource_paths}

Prototype screenshots are attached after this text in this order:
{prototype_list}
""",
    "TB-GEN-v8": """\
Prompt ID: TB-GEN-v8

Build a compact, complete single-file HTML implementation for the Track B GUI item below.

Hard requirements:
- Return exactly one complete HTML document, including <!doctype html>, <html>, <head>, and <body>.
- The document must end with </html>. Completeness is more important than decorative detail.
- Put CSS and JavaScript inside the same file. Do not require a build step, package manager, backend, or network access.
- The generated index.html will be saved inside:
  data/track_b/items/{item_id}/generated/<run_name>/
  Local assets must be referenced as ../../resources/<subpath>.
- Use the supplied prototype screenshots for visual structure, spacing, typography, colors, and page hierarchy, but implement a compact version.
- Implement workflow-required routes and interactions first. Do not spend tokens on exhaustive secondary pages.
- Primary evaluation viewport is desktop: optimize for 1365px and 1920px. Mobile responsiveness is not a hard gate.
- Keep CSS and JS short. Avoid animations, large design systems, repeated footer markup, and long prose copied from the requirement.

Mandatory workflow controls:
- Every workflow-required click target must be visible text inside an <a> or <button>. Never use <div>, <span>, <li>, or other inert elements for these labels.
- Each workflow control must include data-route-target="<route_id>" and onclick="showPage('<route_id>')".
- Required exact visible labels and route targets:
  - Register to Vote -> voter_registration
  - Learn more for the 2024 Provincial Election Report banner -> 2024_provincial_election
  - Learn more for the 2026 General Local Elections card -> 2026_local_elections
  - Resources -> resources_and_reports
  - Local Forms -> local_election_forms
- If a sidebar item is workflow-required, it must still be an <a> or <button>; style it like a sidebar item with CSS instead of using a div.
- Secondary navigation items may be visible non-functional placeholders only if they are not listed above.
- If downloadable files such as PDFs are mentioned but no files are provided, show labelled text links or table entries. Do not invent file contents.

Compactness limits:
- For each route, use at most one main heading, one short summary paragraph, one compact key-info block, and one table or list when needed.
- Use at most 4 table rows per table and at most 4 bullets per list.
- Reuse shared header, sidebar, card, button, and footer styles.
- If output budget feels tight, reduce visual/detail text. Never omit closing tags, route sections, mandatory workflow controls, or the route handler.

Route contract:
{route_contract}

Required minimal JavaScript behavior:
<script>
window.__TRACK_B_ROUTES = {route_ids_json};
function showPage(routeId) {{
  if (!window.__TRACK_B_ROUTES.includes(routeId)) return;
  document.querySelectorAll('[data-track-route]').forEach(function(section) {{
    section.hidden = section.id !== routeId;
  }});
  document.querySelectorAll('[data-route-target]').forEach(function(link) {{
    link.setAttribute('aria-current', link.dataset.routeTarget === routeId ? 'page' : 'false');
  }});
  if (history.replaceState) {{
    history.replaceState(null, '', '#' + routeId);
  }}
  setTimeout(function() {{ window.scrollTo(0, 0); }}, 0);
}}
document.addEventListener('DOMContentLoaded', function() {{
  var initial = location.hash ? location.hash.slice(1) : window.__TRACK_B_ROUTES[0];
  showPage(window.__TRACK_B_ROUTES.includes(initial) ? initial : window.__TRACK_B_ROUTES[0]);
}});
</script>

Item ID: {item_id}
Source task: {source_task_name}
Source level: {source_level}
Use for dynamic validation: {use_for_dynamic}

Normalized requirement:
{requirement}

Workflow checks:
{workflow}

Available local resource paths:
{resource_paths}

Prototype screenshots are attached after this text in this order:
{prototype_list}
""",
    "TB-GEN-v9": """\
Prompt ID: TB-GEN-v9

Build a minimal complete single-file HTML implementation for the Track B GUI item below.

Hard requirements:
- Return exactly one complete HTML document ending with </html>.
- Include inline CSS and JavaScript only. No build step, backend, network access, external CDN, or markdown.
- Local assets must be referenced as ../../resources/<subpath>.
- Use the prototype screenshots for overall structure and visual cues, but produce a minimal benchmark implementation.
- Primary viewport is desktop: 1365px and 1920px. Mobile quality is not a hard gate.
- Implement every route in the route contract as a <section id="..." data-track-route>.
- Include window.__TRACK_B_ROUTES exactly as given and a showPage(routeId) handler before </body>.

Mandatory workflow controls:
- The following exact workflow click labels were extracted from the workflow checks. Every label below must appear as visible text inside an <a> or <button> element:
{workflow_labels}
- Never use <div>, <span>, <li>, or other inert elements for workflow-required click labels.
- Every workflow control must include data-route-target="<route_id>" and onclick="showPage('<route_id>')".
- If a click target is a feature phrase such as "GitLab Duo", use that feature phrase as the visible label.
- Choose the route target from the route contract that best matches the label and workflow validation.
- Secondary navigation items may be visible non-functional placeholders only if they are not listed in the extracted workflow click labels.

Strict compactness limits:
- Use one shared header and one shared footer only.
- For each route, use at most one h1, one short paragraph, one compact card/list, and one optional tiny table.
- Use at most 3 cards per route, 3 bullets per list, and 3 rows per table.
- Do not copy long requirement text. Use short labels and short summaries.
- Avoid decorative animations, large CSS frameworks, inline SVG art, exhaustive menus, and long repeated sections.
- If output budget feels tight, remove visual detail first. Never omit routes, workflow controls, JavaScript, or closing tags.

Route contract:
{route_contract}

Required JavaScript:
<script>
window.__TRACK_B_ROUTES = {route_ids_json};
function showPage(routeId) {{
  if (!window.__TRACK_B_ROUTES.includes(routeId)) return;
  document.querySelectorAll('[data-track-route]').forEach(function(section) {{
    section.hidden = section.id !== routeId;
  }});
  document.querySelectorAll('[data-route-target]').forEach(function(link) {{
    link.setAttribute('aria-current', link.dataset.routeTarget === routeId ? 'page' : 'false');
  }});
  if (history.replaceState) history.replaceState(null, '', '#' + routeId);
  setTimeout(function() {{ window.scrollTo(0, 0); }}, 0);
}}
document.addEventListener('DOMContentLoaded', function() {{
  var initial = location.hash ? location.hash.slice(1) : window.__TRACK_B_ROUTES[0];
  showPage(window.__TRACK_B_ROUTES.includes(initial) ? initial : window.__TRACK_B_ROUTES[0]);
}});
</script>

Item ID: {item_id}
Source task: {source_task_name}
Source level: {source_level}
Use for dynamic validation: {use_for_dynamic}

Normalized requirement:
{requirement}

Workflow checks:
{workflow}

Available local resource paths:
{resource_paths}

Prototype screenshots are attached after this text in this order:
{prototype_list}
""",
    "TB-GEN-v12": """\
Prompt ID: TB-GEN-v12

Build a compact, complete single-file HTML implementation for the Track B GUI item below.

Hard requirements:
- Return exactly one complete HTML document ending with </html>.
- Include inline CSS and JavaScript only. No build step, backend, network access, external CDN, or markdown.
- Local assets must be referenced as ../../resources/<subpath>.
- Use the supplied prototype screenshots for visual structure and page hierarchy, but implement a compact benchmark version.
- Primary viewport is desktop: 1365px and 1920px. Mobile quality is not a hard gate.
- Implement every route in the route contract as a <section id="..." data-track-route>.
- Include window.__TRACK_B_ROUTES exactly as given and a showPage(routeId) handler before </body>.

Required workflow-control contract:
- The controls below are machine-checkable requirements. For each item, create an <a> or <button> whose visible text exactly matches visible_text and whose route exactly matches route_id.
- Do not replace visible_text with a synonym, longer phrase, icon-only label, or nearby non-clickable heading.
- The required_element example is the safest minimal implementation; copy its text, data-route-target, and onclick route exactly unless the surrounding layout needs <button> instead of <a>.
{workflow_controls}

Compactness limits:
- Use one shared header and one shared footer only.
- For each route, use at most one h1, one short paragraph, one compact card/list, and one optional tiny table.
- Use at most 3 cards per route, 3 bullets per list, and 3 rows per table.
- Do not copy long requirement text. Use short labels and short summaries.
- If output budget feels tight, remove visual detail first. Never omit routes, workflow controls, JavaScript, or closing tags.

Route contract:
{route_contract}

Required JavaScript:
<script>
window.__TRACK_B_ROUTES = {route_ids_json};
function showPage(routeId) {{
  if (!window.__TRACK_B_ROUTES.includes(routeId)) return;
  document.querySelectorAll('[data-track-route]').forEach(function(section) {{
    section.hidden = section.id !== routeId;
  }});
  document.querySelectorAll('[data-route-target]').forEach(function(link) {{
    link.setAttribute('aria-current', link.dataset.routeTarget === routeId ? 'page' : 'false');
  }});
  if (history.replaceState) history.replaceState(null, '', '#' + routeId);
  setTimeout(function() {{ window.scrollTo(0, 0); }}, 0);
}}
document.addEventListener('DOMContentLoaded', function() {{
  var initial = location.hash ? location.hash.slice(1) : window.__TRACK_B_ROUTES[0];
  showPage(window.__TRACK_B_ROUTES.includes(initial) ? initial : window.__TRACK_B_ROUTES[0]);
}});
</script>

Item ID: {item_id}
Source task: {source_task_name}
Source level: {source_level}
Use for dynamic validation: {use_for_dynamic}

Normalized requirement:
{requirement}

Workflow checks:
{workflow}

Available local resource paths:
{resource_paths}

Prototype screenshots are attached after this text in this order:
{prototype_list}
""",
    "TB-GEN-v13": """\
Prompt ID: TB-GEN-v13

Build a compact, complete single-file HTML implementation for the Track B GUI item below.

Hard requirements:
- Return exactly one complete HTML document ending with </html>.
- Include inline CSS and JavaScript only. No build step, backend, network access, external CDN, or markdown.
- Local assets must be referenced as ../../resources/<subpath>.
- Use the supplied prototype screenshots for visual structure and page hierarchy, but implement a compact benchmark version.
- Primary viewport is desktop: 1365px and 1920px. Mobile quality is not a hard gate.
- Implement every route in the route contract as a <section id="..." data-track-route>.
- Include window.__TRACK_B_ROUTES exactly as given and a showPage(routeId) handler before </body>.

Required workflow-control bar:
- Copy the following HTML block into the page header or primary navigation area.
- Keep each anchor's visible text, data-route-target, and onclick route exactly as written.
- You may add CSS classes or wrap the block for layout, but do not rename, remove, hide, or replace any anchor in this block.
{workflow_control_bar}

Compactness limits:
- Use one shared header and one shared footer only.
- For each route, use at most one h1, one short paragraph, one compact card/list, and one optional tiny table.
- Use at most 3 cards per route, 3 bullets per list, and 3 rows per table.
- Do not copy long requirement text. Use short labels and short summaries.
- If output budget feels tight, remove visual detail first. Never omit routes, workflow controls, JavaScript, or closing tags.

Route contract:
{route_contract}

Required JavaScript:
<script>
window.__TRACK_B_ROUTES = {route_ids_json};
function showPage(routeId) {{
  if (!window.__TRACK_B_ROUTES.includes(routeId)) return;
  document.querySelectorAll('[data-track-route]').forEach(function(section) {{
    section.hidden = section.id !== routeId;
  }});
  document.querySelectorAll('[data-route-target]').forEach(function(link) {{
    link.setAttribute('aria-current', link.dataset.routeTarget === routeId ? 'page' : 'false');
  }});
  if (history.replaceState) history.replaceState(null, '', '#' + routeId);
  setTimeout(function() {{ window.scrollTo(0, 0); }}, 0);
}}
document.addEventListener('DOMContentLoaded', function() {{
  var initial = location.hash ? location.hash.slice(1) : window.__TRACK_B_ROUTES[0];
  showPage(window.__TRACK_B_ROUTES.includes(initial) ? initial : window.__TRACK_B_ROUTES[0]);
}});
</script>

Item ID: {item_id}
Source task: {source_task_name}
Source level: {source_level}
Use for dynamic validation: {use_for_dynamic}

Normalized requirement:
{requirement}

Workflow checks:
{workflow}

Available local resource paths:
{resource_paths}

Prototype screenshots are attached after this text in this order:
{prototype_list}
""",
    "TB-GEN-v14": """\
Prompt ID: TB-GEN-v14

Build a visually grounded, complete single-file HTML implementation for the Track B GUI item below.

Hard requirements:
- Return exactly one complete HTML document ending with </html>.
- Include inline CSS and JavaScript only. No build step, backend, network access, external CDN, or markdown.
- Local assets must be referenced exactly as ../../resources/<subpath> using paths from the resource list.
- Implement every route in the route contract as a <section id="..." data-track-route>.
- Include window.__TRACK_B_ROUTES exactly as given and a showPage(routeId) handler before </body>.
- The first route in window.__TRACK_B_ROUTES must be the default page shown on initial load.

Visual-grounding requirements:
- Use the prototype screenshots for layout, hierarchy, colors, spacing, and visible content priorities.
- Use local image assets whenever they are available. Do not replace provided images with plain text boxes, CSS placeholders, icon-only blocks, or empty cards.
- The homepage must include visible <img> elements when image assets exist.
- Product, recipe, article, service, and video card/list sections should use relevant <img> elements when matching or plausible local images exist.
- Select images by filename and requirement context. For example, filenames that resemble a recipe, cookbook, logo, video thumbnail, or banner should be used for that visible item.
- If no exact image match is obvious, choose the closest local image rather than omitting imagery.
- Reduce prose before removing images, workflow controls, route sections, or JavaScript.

Required workflow-control contract:
- The controls below are machine-checkable requirements. For each item, create an <a> or <button> whose visible text exactly matches visible_text and whose route exactly matches route_id.
- The listed visible_text values are the actual click targets. Context phrases in workflow actions, such as section names, may be headings but do not need to be clickable unless listed below.
- Do not replace visible_text with a synonym, longer phrase, icon-only label, or nearby non-clickable heading.
- Do not implement workflow-required controls as <div>, <span>, <li>, image-only controls, or any other inert element, even if onclick is present.
- If a workflow target is visually a card or image tile, wrap the card content in an <a> or <button> and keep the required visible_text inside that element.
- The required_element example is the safest minimal implementation; copy its text, data-route-target, and onclick route exactly unless the surrounding layout needs <button> instead of <a>.
{workflow_controls}

Implementation guidance:
- Build a recognizable desktop page, not a bare wireframe.
- Prefer a shared header/navigation and shared footer, with route-specific visual content.
- Include enough cards/tables/lists to satisfy the written requirement and workflow validations, but do not reproduce exhaustive long prose.
- Use semantic HTML, visible focus states, alt text for images, and accessible <a>/<button> controls.
- Secondary navigation items may be visible non-functional placeholders only if they are not workflow-required controls.

Route contract:
{route_contract}

Required JavaScript:
<script>
window.__TRACK_B_ROUTES = {route_ids_json};
function showPage(routeId) {{
  if (!window.__TRACK_B_ROUTES.includes(routeId)) return;
  document.querySelectorAll('[data-track-route]').forEach(function(section) {{
    section.hidden = section.id !== routeId;
  }});
  document.querySelectorAll('[data-route-target]').forEach(function(link) {{
    link.setAttribute('aria-current', link.dataset.routeTarget === routeId ? 'page' : 'false');
  }});
  if (history.replaceState) history.replaceState(null, '', '#' + routeId);
  setTimeout(function() {{ window.scrollTo(0, 0); }}, 0);
}}
document.addEventListener('DOMContentLoaded', function() {{
  var initial = location.hash ? location.hash.slice(1) : window.__TRACK_B_ROUTES[0];
  showPage(window.__TRACK_B_ROUTES.includes(initial) ? initial : window.__TRACK_B_ROUTES[0]);
}});
</script>

Item ID: {item_id}
Source task: {source_task_name}
Source level: {source_level}
Use for dynamic validation: {use_for_dynamic}

Normalized requirement:
{requirement}

Workflow checks:
{workflow}

Available local resource paths:
{resource_paths}

Prototype screenshots are attached after this text in this order:
{prototype_list}
""",
    "TB-GEN-v15": """\
Prompt ID: TB-GEN-v15

Build a visually grounded, complete single-file HTML implementation for the Track B GUI item below.

Hard requirements:
- Return exactly one complete HTML document ending with </html>.
- Include inline CSS and JavaScript only. No build step, backend, network access, external CDN, or markdown.
- Local assets must be referenced exactly as ../../resources/<subpath> using paths from the resource list.
- Implement every route in the route contract as a <section id="..." data-track-route>.
- Include window.__TRACK_B_ROUTES exactly as given and a showPage(routeId) handler before </body>.
- Never call showPage() with a route id that is not listed in window.__TRACK_B_ROUTES.
- Secondary menu items that do not have a route in the route contract must be plain placeholders without onclick, without data-route-target, and without showPage().

Visual-grounding requirements:
- Use the prototype screenshots for layout, hierarchy, colors, spacing, and visible content priorities.
- Use local image assets whenever they are available. Do not replace provided images with plain text boxes, CSS placeholders, icon-only blocks, or empty cards.
- The homepage must include visible <img> elements when image assets exist.
- Product, recipe, article, service, and video card/list sections should use relevant <img> elements when matching or plausible local images exist.
- Select images by filename and requirement context. If no exact image match is obvious, choose the closest local image rather than omitting imagery.
- Reduce prose before removing images, workflow controls, route sections, or JavaScript.

Required workflow-control contract:
- The controls below are machine-checkable requirements. For each item, create an <a> or <button> whose visible text exactly matches visible_text and whose route exactly matches route_id.
- Copy each required_element line into the HTML output exactly once or adapt only the tag name from <a> to <button>. Keep the visible text, data-route-target, and onclick route unchanged.
- The required clickable element's own visible text must be exactly visible_text. Do not use "View", "View Recipe", "Read more", "Open", icons, or longer phrases as the clickable text for required controls.
- The listed visible_text values are the actual click targets. Context phrases in workflow actions, such as section names, may be headings but do not need to be clickable unless listed below.
- Do not implement workflow-required controls as <div>, <span>, <li>, image-only controls, or any other inert element, even if onclick is present.
- If a workflow target is visually a card or image tile, put the required <a> or <button> inside that card, and make the card's clickable label exactly visible_text.
- Do not hide required controls in comments, scripts, templates, off-screen text, display:none, visibility:hidden, or aria-hidden content.
{workflow_controls}

Implementation guidance:
- Build a recognizable desktop page, not a bare wireframe.
- Prefer a shared header/navigation and shared footer, with route-specific visual content.
- Include enough cards/tables/lists to satisfy the written requirement and workflow validations, but do not reproduce exhaustive long prose.
- Use semantic HTML, visible focus states, alt text for images, and accessible <a>/<button> controls.
- Before returning the HTML, self-check these conditions:
  1. Every required_element visible_text appears as visible text inside an <a> or <button>.
  2. Every showPage('...') route is present in window.__TRACK_B_ROUTES and has a matching section id.
  3. The page uses local <img> assets when image assets were provided.

Route contract:
{route_contract}

Required JavaScript:
<script>
window.__TRACK_B_ROUTES = {route_ids_json};
function showPage(routeId) {{
  if (!window.__TRACK_B_ROUTES.includes(routeId)) return;
  document.querySelectorAll('[data-track-route]').forEach(function(section) {{
    section.hidden = section.id !== routeId;
  }});
  document.querySelectorAll('[data-route-target]').forEach(function(link) {{
    link.setAttribute('aria-current', link.dataset.routeTarget === routeId ? 'page' : 'false');
  }});
  if (history.replaceState) history.replaceState(null, '', '#' + routeId);
  setTimeout(function() {{ window.scrollTo(0, 0); }}, 0);
}}
document.addEventListener('DOMContentLoaded', function() {{
  var initial = location.hash ? location.hash.slice(1) : window.__TRACK_B_ROUTES[0];
  showPage(window.__TRACK_B_ROUTES.includes(initial) ? initial : window.__TRACK_B_ROUTES[0]);
}});
</script>

Item ID: {item_id}
Source task: {source_task_name}
Source level: {source_level}
Use for dynamic validation: {use_for_dynamic}

Normalized requirement:
{requirement}

Workflow checks:
{workflow}

Available local resource paths:
{resource_paths}

Prototype screenshots are attached after this text in this order:
{prototype_list}
""",
    "TB-GEN-v16": """\
Prompt ID: TB-GEN-v16

Build a visually grounded, complete single-file HTML implementation for the Track B GUI item below.

Hard requirements:
- Return exactly one complete HTML document ending with </html>.
- Include inline CSS and JavaScript only. No build step, backend, network access, external CDN, or markdown.
- Local assets must be referenced exactly as ../../resources/<subpath> using paths from the resource list.
- Implement every route in the route contract as a <section id="..." data-track-route>.
- Include window.__TRACK_B_ROUTES exactly as given and a showPage(routeId) handler before </body>.
- Never call showPage() with a route id that is not listed in window.__TRACK_B_ROUTES.
- Secondary menu items that do not have a route in the route contract must be plain placeholders without onclick, without data-route-target, and without showPage().

Visual-grounding requirements:
- Use the prototype screenshots for layout, hierarchy, colors, spacing, and visible content priorities.
- Use local image assets whenever they are available. Do not replace provided images with plain text boxes, CSS placeholders, icon-only blocks, or empty cards.
- Use a bounded number of images: include at least one relevant local image on visual routes when assets exist, but avoid exhaustive galleries.
- Product, recipe, article, service, and video card/list sections should use relevant <img> elements when matching or plausible local images exist.
- Select images by filename and requirement context. If no exact image match is obvious, choose the closest local image from the listed assets rather than omitting imagery.
- Reduce repeated prose before removing images, workflow controls, route sections, validation evidence, or JavaScript.

Required exact workflow-control contract:
- The controls below are machine-checkable exact-text requirements. For each item, create an <a> or <button> whose visible text exactly matches visible_text and whose route exactly matches route_id.
- Copy each required_element line into the HTML output exactly once or adapt only the tag name from <a> to <button>. Keep the visible text, data-route-target, and onclick route unchanged.
- The required clickable element's own visible text must be exactly visible_text. Do not use "View", "View Recipe", "Read more", "Open", icons, or longer phrases as the clickable text for required exact-text controls.
- Do not implement workflow-required exact-text controls as <div>, <span>, <li>, image-only controls, or any other inert element, even if onclick is present.
- Semantic/visual targets listed in the compact workflow summary, such as a logo click, must be clickable and route correctly, but do not render the descriptive phrase literally unless it is actual visible UI text.
{workflow_controls}

Bounded implementation guidance:
- Build a recognizable desktop page, not a bare wireframe.
- Prefer one shared header/navigation and one shared footer, with route-specific visual content.
- For each route, include one clear heading, enough validation evidence text, and at most one compact table/list plus a small card grid when needed.
- Use at most 4 cards per route, 4 rows per table, and 4 bullets per list unless a validation explicitly requires more.
- Use semantic HTML, visible focus states, alt text for images, and accessible <a>/<button> controls.
- Before returning the HTML, self-check these conditions:
  1. Every exact required_element visible_text appears as visible text inside an <a> or <button>.
  2. Every semantic/visual workflow target routes correctly without requiring its descriptive phrase as visible text.
  3. Every showPage('...') route is present in window.__TRACK_B_ROUTES and has a matching section id.
  4. Every route includes the evidence needed by the compact workflow validations.
  5. The page uses local <img> assets when image assets were provided.

Route contract:
{route_contract}

Required JavaScript:
<script>
window.__TRACK_B_ROUTES = {route_ids_json};
function showPage(routeId) {{
  if (!window.__TRACK_B_ROUTES.includes(routeId)) return;
  document.querySelectorAll('[data-track-route]').forEach(function(section) {{
    section.hidden = section.id !== routeId;
  }});
  document.querySelectorAll('[data-route-target]').forEach(function(link) {{
    link.setAttribute('aria-current', link.dataset.routeTarget === routeId ? 'page' : 'false');
  }});
  if (history.replaceState) history.replaceState(null, '', '#' + routeId);
  setTimeout(function() {{ window.scrollTo(0, 0); }}, 0);
}}
document.addEventListener('DOMContentLoaded', function() {{
  var initial = location.hash ? location.hash.slice(1) : window.__TRACK_B_ROUTES[0];
  showPage(window.__TRACK_B_ROUTES.includes(initial) ? initial : window.__TRACK_B_ROUTES[0]);
}});
</script>

Item ID: {item_id}
Source task: {source_task_name}
Source level: {source_level}
Use for dynamic validation: {use_for_dynamic}

Normalized requirement:
{requirement}

Compact workflow checks, deduplicated from workflow.json:
{workflow}

Relevant local resource paths:
{resource_paths}

Prototype screenshots are attached after this text in this order:
{prototype_list}
""",
}


def load_env_file(path):
    if not path.exists():
        return
    with path.open("r", encoding="utf-8-sig") as f:
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
    load_env_file(PROJECT_ROOT / ".env")
    load_env_file(PROJECT_ROOT / "scripts" / ".env")


def safe_name(value):
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    return value.strip("._") or "run"


def read_text(path):
    return path.read_text(encoding="utf-8")


def read_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def limited_text(value, limit):
    if len(value) <= limit:
        return value
    return value[:limit] + "\n\n[TRUNCATED FOR PROMPT]"


def unique_preserve_order(values):
    seen = set()
    result = []
    for value in values:
        key = str(value).strip()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(key)
    return result


def collect_resource_paths(item_dir, limit):
    resources_dir = item_dir / "resources"
    if not resources_dir.exists():
        return []
    files = [path for path in resources_dir.rglob("*") if path.is_file()]
    files = sorted(files, key=lambda path: str(path.relative_to(resources_dir)).lower())
    return [path.relative_to(resources_dir).as_posix() for path in files[:limit]]


def collect_prototypes(item_dir, max_prototypes):
    prototype_dir = item_dir / "prototypes"
    if not prototype_dir.exists():
        return []
    files = [
        path for path in prototype_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    ]
    def route_order(path):
        stem = path.stem.lower()
        if stem in {"home", "homepage", "index", "landing"}:
            return (0, stem)
        if "home" in stem:
            return (1, stem)
        return (2, stem)

    return sorted(files, key=route_order)[:max_prototypes]


def label_from_click_action(action):
    lower = action.lower()
    if lower.startswith("browser:") or "click" not in lower:
        return None
    quoted = re.findall(r'"([^"]+)"', action)
    if quoted:
        return quoted[0].strip()
    related = re.search(r"related to ([A-Za-z0-9 .&'/-]+?)(?: in | on | from |$)", action, flags=re.IGNORECASE)
    if related:
        return re.sub(r"\s+", " ", related.group(1).strip())
    named = re.search(r"named\s+\"([^\"]+)\"", action, flags=re.IGNORECASE)
    if named:
        return named.group(1).strip()
    match = re.search(
        r"Click the (.+?)(?: button| link| option| card| navigation menu item| in the| from the|$)",
        action,
        flags=re.IGNORECASE,
    )
    if match:
        return re.sub(r"\s+", " ", match.group(1).strip())
    return None


def route_terms(route_id):
    terms = re.findall(r"[a-z0-9]+", route_id.lower())
    return [term for term in terms if term not in {"and", "the", "page", "homepage", "home"}]


def text_terms(text):
    terms = re.findall(r"[a-z0-9]+", text.lower())
    stop = {
        "a", "an", "and", "button", "card", "click", "content", "from",
        "in", "is", "link", "menu", "navigation", "on", "page", "the", "to",
    }
    return [term for term in terms if term not in stop]


def fuzzy_overlap(left_terms, right_terms):
    count = 0
    for left in left_terms:
        for right in right_terms:
            if left == right or left[:5] == right[:5] or left.startswith(right[:5]) or right.startswith(left[:5]):
                count += 1
                break
    return count


def best_route_for_control(label, action, context, route_ids, prototype_routes):
    combined = " ".join([label, action, context]).lower()
    normalized_label = label.strip().lower()
    include_home = any(
        hint in combined
        for hint in [
            "logo",
            "return to home",
            "return to homepage",
            "back to home",
            "back to homepage",
            "navigates back",
            "home page content",
            "homepage with the main hero",
        ]
    ) or normalized_label in {"home", "homepage"}
    if include_home:
        candidates = route_ids
    else:
        candidates = [route for route in route_ids if route not in {"home", "homepage", "index", "landing"}]
    if not candidates:
        candidates = route_ids
    label_terms = set(text_terms(label))
    action_terms = set(text_terms(action))
    context_terms = set(text_terms(context))
    best_route = candidates[0]
    best_score = -1
    for route in candidates:
        terms = set(route_terms(route))
        score = fuzzy_overlap(label_terms, terms) * 6
        score += fuzzy_overlap(action_terms, terms) * 4
        score += fuzzy_overlap(context_terms, terms)
        if include_home and route in {"home", "homepage", "index", "landing"}:
            score += 20
        if route in prototype_routes:
            score += 1
        if score > best_score:
            best_route = route
            best_score = score
    if best_score <= 0 and len(prototype_routes) == 1:
        only_route = next(iter(prototype_routes))
        if only_route in route_ids:
            return only_route
    return best_route


def workflow_target_kind(label, action):
    lower_action = action.lower()
    lower_label = label.lower()
    if "logo" in lower_action or lower_label.startswith("logo ") or " logo " in lower_label:
        return "semantic_visual"
    if "button or link related to" in lower_action:
        return "exact_text"
    if re.search(r'"[^"]+"', action):
        return "exact_text"
    if re.search(r"named\s+\"", action, flags=re.IGNORECASE):
        return "exact_text"
    if re.search(r"related to [A-Za-z0-9 .&'/-]+", action, flags=re.IGNORECASE):
        return "exact_text"
    return "exact_text"


def derive_workflow_controls(workflow, route_ids):
    controls = []
    seen = set()
    for block in workflow:
        prototype_routes = set((block.get("prototype") or {}).keys())
        for case in block.get("content", []):
            context = " ".join([
                str(case.get("objective", "")),
                " ".join(str(value) for value in case.get("validations", [])),
            ])
            for action in case.get("actions", []):
                if not isinstance(action, str):
                    continue
                label = label_from_click_action(action)
                if not label:
                    continue
                route = best_route_for_control(label, action, context, route_ids, prototype_routes)
                key = (label.lower(), route, action.lower())
                if key in seen:
                    continue
                seen.add(key)
                controls.append({
                    "visible_text": label,
                    "route_id": route,
                    "context": action,
                    "target_kind": workflow_target_kind(label, action),
                })
    return controls


def workflow_click_labels(workflow):
    labels = set()
    for block in workflow:
        for case in block.get("content", []):
            for action in case.get("actions", []):
                if not isinstance(action, str):
                    continue
                lower = action.lower()
                if lower.startswith("browser:") or "click" not in lower:
                    continue
                quoted = re.findall(r'"([^"]{2,80})"', action)
                if quoted:
                    labels.update(label.strip() for label in quoted)
                    continue
                related = re.search(
                    r"related to ([A-Za-z0-9 .&'/-]+?)(?: in | on | from |$)",
                    action,
                    flags=re.IGNORECASE,
                )
                if related:
                    labels.add(re.sub(r"\s+", " ", related.group(1).strip()))
                    continue
                named = re.search(r"named\s+\"([^\"]+)\"", action, flags=re.IGNORECASE)
                if named:
                    labels.add(named.group(1).strip())
                    continue
                match = re.search(
                    r"Click the (.+?)(?: button| link| option| card| navigation menu item| in the| from the|$)",
                    action,
                    flags=re.IGNORECASE,
                )
                if match:
                    label = re.sub(r"\s+", " ", match.group(1).strip())
                    if not label.lower().startswith("learn more button in"):
                        labels.add(label)
    return sorted(label for label in labels if 2 <= len(label) <= 80)


def workflow_labels_text(labels):
    if not labels:
        return "- No workflow click labels were extracted."
    return "\n".join(f"- {label}" for label in labels)


def workflow_controls_text(controls, exact_only=False):
    selected = [
        control for control in controls
        if not exact_only or control.get("target_kind", "exact_text") == "exact_text"
    ]
    if not selected:
        return "- No workflow controls were extracted."
    lines = []
    for control in selected:
        text = control["visible_text"]
        route = control["route_id"]
        lines.extend([
            f"- visible_text: {text}",
            f"  route_id: {route}",
            f"  context: {control['context']}",
            f"  required_element: <a href=\"#{route}\" data-route-target=\"{route}\" onclick=\"showPage('{route}')\">{text}</a>",
        ])
    return "\n".join(lines)


def compact_resource_paths(resources, requirement, workflow_controls, route_ids, limit):
    if not resources:
        return []
    requirement_terms = set(text_terms(requirement))
    control_terms = set()
    for control in workflow_controls:
        control_terms.update(text_terms(control.get("visible_text", "")))
        control_terms.update(text_terms(control.get("context", "")))
    route_term_set = set()
    for route_id in route_ids:
        route_term_set.update(route_terms(route_id))
    important_terms = requirement_terms | control_terms | route_term_set

    image_exts = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}
    preferred_name_terms = {
        "banner", "brand", "card", "cover", "hero", "icon", "image", "img",
        "logo", "photo", "thumbnail", "thumb", "video",
    }
    deprioritized_exts = {".otf", ".ttf", ".woff", ".woff2"}

    ranked = []
    for index, path in enumerate(resources):
        path_obj = Path(path)
        suffix = path_obj.suffix.lower()
        name_terms = set(text_terms(path_obj.stem))
        score = 0
        if suffix in image_exts:
            score += 20
        if suffix in deprioritized_exts:
            score -= 30
        score += len(name_terms & important_terms) * 5
        score += len(name_terms & preferred_name_terms) * 3
        if "logo" in name_terms:
            score += 5
        ranked.append((-score, index, path))
    ranked.sort()
    return [path for _, _, path in ranked[:limit]]


def resource_paths_text(resources, compact=False, omitted_count=0):
    if not resources:
        return "- No local resources were found."
    lines = [f"- ../../resources/{path}" for path in resources]
    if compact and omitted_count > 0:
        lines.append(f"- [omitted {omitted_count} lower-priority resource paths from the prompt]")
    return "\n".join(lines)


def route_prototype_map(route_ids, prototypes):
    return {
        route_id: path.name
        for route_id, path in zip(route_ids, prototypes)
    }


def compact_workflow_summary(workflow, route_ids, prototypes, workflow_controls):
    prototype_by_route = route_prototype_map(route_ids, prototypes)
    validations_by_route = {route_id: [] for route_id in route_ids}
    actions_by_route = {route_id: [] for route_id in route_ids}
    semantic_targets = []

    controls_by_action = {control["context"]: control for control in workflow_controls}

    for block in workflow:
        block_routes = [
            route for route in (block.get("prototype") or {}).keys()
            if route in route_ids
        ]
        fallback_route = block_routes[0] if len(block_routes) == 1 else None
        for case in block.get("content", []):
            case_validations = [
                validation for validation in case.get("validations", [])
                if isinstance(validation, str)
            ]
            destination_route = None
            for action in case.get("actions", []):
                if not isinstance(action, str):
                    continue
                control = controls_by_action.get(action)
                if control:
                    destination_route = control["route_id"]
                    actions_by_route[destination_route].append(action)
                    if control.get("target_kind") != "exact_text":
                        semantic_targets.append(
                            f"{action} -> {destination_route} ({control.get('target_kind')})"
                        )
            if destination_route is None:
                destination_route = fallback_route
            if destination_route in validations_by_route:
                validations_by_route[destination_route].extend(case_validations)

    lines = [
        "Use this compact summary as the workflow source of truth for route behavior and destination evidence.",
        "Exact text click controls are listed in the workflow-control contract above.",
    ]
    if semantic_targets:
        lines.append("Semantic/visual click targets:")
        for target in unique_preserve_order(semantic_targets):
            lines.append(f"- {target}")
    else:
        lines.append("Semantic/visual click targets: none.")

    lines.append("Route validation evidence:")
    for route_id in route_ids:
        prototype_name = prototype_by_route.get(route_id, "unknown prototype")
        lines.append(f"- route_id: {route_id} (prototype: {prototype_name})")
        route_actions = unique_preserve_order(actions_by_route.get(route_id, []))
        if route_actions:
            lines.append("  triggered_by:")
            for action in route_actions:
                lines.append(f"  - {action}")
        route_validations = unique_preserve_order(validations_by_route.get(route_id, []))
        if route_validations:
            lines.append("  required_visible_evidence:")
            for validation in route_validations:
                lines.append(f"  - {validation}")
        else:
            lines.append("  required_visible_evidence: route must exist and match its prototype/requirement.")
    return "\n".join(lines)


def workflow_control_bar_text(controls):
    if not controls:
        return '<nav data-workflow-controls aria-label="Workflow controls"></nav>'
    lines = ['<nav data-workflow-controls aria-label="Workflow controls">']
    seen = set()
    for control in controls:
        text = control["visible_text"]
        route = control["route_id"]
        key = (text.lower(), route)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f'  <a href="#{route}" data-route-target="{route}" onclick="showPage(\'{route}\')">{text}</a>')
    lines.append("</nav>")
    return "\n".join(lines)


def effective_input_profile(args):
    if args.input_profile != "auto":
        return args.input_profile
    if args.prompt_id == "TB-GEN-v16":
        return "compact"
    return "legacy"


def effective_image_max_side(args):
    if args.image_max_side is not None:
        return args.image_max_side or None
    if effective_input_profile(args) == "compact":
        return 3000
    return None


def image_to_b64(path):
    return base64.b64encode(path.read_bytes()).decode("ascii")


def image_media_type(path):
    media_type, _ = mimetypes.guess_type(path.name)
    return media_type or "image/png"


def encoded_image(path, image_max_side=None):
    if not image_max_side:
        return image_media_type(path), image_to_b64(path)
    try:
        from io import BytesIO
        from PIL import Image
    except ImportError:
        return image_media_type(path), image_to_b64(path)

    with Image.open(path) as image:
        width, height = image.size
        max_dimension = max(width, height)
        if max_dimension <= image_max_side:
            return image_media_type(path), image_to_b64(path)
        scale = image_max_side / max_dimension
        new_size = (max(1, int(width * scale)), max(1, int(height * scale)))
        resized = image.convert("RGB").resize(new_size, Image.Resampling.LANCZOS)
        buffer = BytesIO()
        resized.save(buffer, format="JPEG", quality=85, optimize=True)
        return "image/jpeg", base64.b64encode(buffer.getvalue()).decode("ascii")


def prototype_image_metadata(prototypes, image_max_side=None):
    try:
        from PIL import Image
    except ImportError:
        return [
            {"path": path.name, "image_max_side": image_max_side, "original_size": None, "sent_size": None}
            for path in prototypes
        ]

    metadata = []
    for path in prototypes:
        with Image.open(path) as image:
            width, height = image.size
        if image_max_side and max(width, height) > image_max_side:
            scale = image_max_side / max(width, height)
            sent_size = [max(1, int(width * scale)), max(1, int(height * scale))]
        else:
            sent_size = [width, height]
        metadata.append({
            "path": path.name,
            "image_max_side": image_max_side,
            "original_size": [width, height],
            "sent_size": sent_size,
        })
    return metadata


def build_prompt(item_dir, args):
    requirement = read_text(item_dir / "requirement.md")
    workflow_data = read_json(item_dir / "workflow.json")
    meta = read_json(item_dir / "source_meta.json")
    prototypes = collect_prototypes(item_dir, args.max_prototypes)
    if not prototypes:
        raise SystemExit(f"ERROR: no prototype screenshots found under {item_dir / 'prototypes'}")

    prototype_text = "\n".join(f"- {path.name}" for path in prototypes)
    route_ids = [path.stem for path in prototypes]
    workflow_controls = derive_workflow_controls(workflow_data, route_ids)
    input_profile = effective_input_profile(args)
    all_resources = collect_resource_paths(item_dir, args.max_resources)
    if input_profile == "compact":
        resources = compact_resource_paths(
            all_resources,
            requirement,
            workflow_controls,
            route_ids,
            min(args.max_resources, args.compact_max_resources),
        )
        workflow = compact_workflow_summary(workflow_data, route_ids, prototypes, workflow_controls)
        workflow_control_text = workflow_controls_text(workflow_controls, exact_only=True)
        resource_text = resource_paths_text(
            resources,
            compact=True,
            omitted_count=max(0, len(all_resources) - len(resources)),
        )
        workflow_text_format = "compact_route_evidence_v1"
        resource_text_format = "ranked_compact_v1"
    else:
        resources = all_resources
        workflow = json.dumps(workflow_data, indent=2, ensure_ascii=False)
        workflow_control_text = workflow_controls_text(workflow_controls)
        resource_text = resource_paths_text(resources)
        workflow_text_format = "full_workflow_json"
        resource_text_format = "full_sorted_paths"
    workflow_control_bar = workflow_control_bar_text(workflow_controls)
    workflow_labels = workflow_click_labels(workflow_data)
    workflow_label_text = workflow_labels_text(workflow_labels)
    route_contract = "\n".join(
        f"- Create <section id=\"{route_id}\" data-track-route> for prototype {path.name}."
        for route_id, path in zip(route_ids, prototypes)
    )
    try:
        template = USER_PROMPT_TEMPLATES[args.prompt_id]
    except KeyError as exc:
        known = ", ".join(sorted(USER_PROMPT_TEMPLATES))
        raise SystemExit(f"ERROR: unknown prompt id {args.prompt_id!r}. Choose one of: {known}") from exc

    user_prompt = template.format(
        item_id=item_dir.name,
        source_task_name=meta.get("source_task_name", item_dir.name),
        source_level=meta.get("source_level", "unknown"),
        use_for_dynamic=meta.get("use_for_dynamic", False),
        requirement=limited_text(requirement, args.requirement_char_limit),
        workflow=limited_text(workflow, args.workflow_char_limit),
        resource_paths=resource_text,
        prototype_list=prototype_text,
        route_contract=route_contract,
        route_ids_json=json.dumps(route_ids, ensure_ascii=False),
        workflow_controls=workflow_control_text,
        workflow_control_bar=workflow_control_bar,
        workflow_labels=workflow_label_text,
    )
    prompt_input_metadata = {
        "input_profile": input_profile,
        "workflow_text_format": workflow_text_format,
        "resource_text_format": resource_text_format,
        "all_resource_count": len(all_resources),
        "resource_paths_in_prompt_count": len(resources),
        "omitted_resource_count": max(0, len(all_resources) - len(resources)),
        "workflow_case_count": sum(len(block.get("content", [])) for block in workflow_data),
        "workflow_prompt_characters": len(workflow),
        "user_prompt_characters": len(user_prompt),
        "exact_workflow_control_count": sum(
            1 for control in workflow_controls
            if control.get("target_kind", "exact_text") == "exact_text"
        ),
        "semantic_workflow_control_count": sum(
            1 for control in workflow_controls
            if control.get("target_kind", "exact_text") != "exact_text"
        ),
    }
    return user_prompt, prototypes, resources, meta, workflow_controls, prompt_input_metadata


def build_client(provider):
    if provider in {"openai", "tuzi-openai"}:
        if provider == "tuzi-openai":
            api_key = os.environ.get("TUZI_API_KEY")
            key_name = "TUZI_API_KEY"
            base_url = os.environ.get("TUZI_BASE_URL") or "https://api.tu-zi.com/v1"
        else:
            api_key = os.environ.get("OPENAI_API_KEY")
            key_name = "OPENAI_API_KEY"
            base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE")
        if not api_key:
            raise SystemExit(f"ERROR: {key_name} not set.")
        endpoint = f"{(base_url or 'https://api.openai.com/v1').rstrip('/')}/chat/completions"
        return {"api_key": api_key, "endpoint": endpoint}, endpoint

    if provider == "anthropic":
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise SystemExit("ERROR: ANTHROPIC_API_KEY not set.")
        from anthropic import Anthropic
        base_url = os.environ.get("ANTHROPIC_BASE_URL")
        client = Anthropic(api_key=api_key, base_url=base_url) if base_url else Anthropic(api_key=api_key)
        return client, base_url or "https://api.anthropic.com"

    if provider == "chatanywhere-anthropic":
        api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
        if not api_key:
            raise SystemExit("ERROR: ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN not set.")
        base_url = os.environ.get("ANTHROPIC_BASE_URL") or "https://api.chatanywhere.org/v1"
        base_url = base_url.rstrip("/")
        if base_url.endswith("/v1/messages"):
            endpoint = base_url
        elif base_url.endswith("/v1"):
            endpoint = f"{base_url}/messages"
        else:
            endpoint = f"{base_url}/v1/messages"
        return {"api_key": api_key, "endpoint": endpoint}, endpoint

    if provider == "gwdg-openai":
        api_key = os.environ.get("GWDG_API_KEY")
        if not api_key:
            raise SystemExit("ERROR: GWDG_API_KEY not set.")
        base_url = os.environ.get("GWDG_BASE_URL") or "https://chat-ai.academiccloud.de/v1"
        endpoint = f"{base_url.rstrip('/')}/chat/completions"
        return {"api_key": api_key, "endpoint": endpoint}, endpoint

    raise SystemExit(f"ERROR: unsupported provider {provider!r}")


def add_optional_max_tokens(payload, max_tokens):
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens


def unwrap_openai_payload(data):
    if isinstance(data, dict) and "choices" not in data and isinstance(data.get("data"), dict):
        return data["data"]
    return data


def ask_openai(client, model, user_prompt, prototypes, max_tokens, temperature, image_max_side=None):
    content = [{"type": "text", "text": user_prompt}]
    for path in prototypes:
        media_type, image_data = encoded_image(path, image_max_side=image_max_side)
        content.append({"type": "text", "text": f"Prototype screenshot: {path.name}"})
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{media_type};base64,{image_data}",
                "detail": "high",
            },
        })

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        "temperature": temperature,
    }
    add_optional_max_tokens(payload, max_tokens)
    request = urllib.request.Request(
        client["endpoint"],
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "accept": "application/json",
            "authorization": f"Bearer {client['api_key']}",
            "content-type": "application/json",
            "user-agent": "master-thesis-track-b-generator/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=360) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc

    data = unwrap_openai_payload(data)
    choice = data.get("choices", [{}])[0]
    message = choice.get("message", {})
    content_text = message.get("content", "")
    if isinstance(content_text, list):
        content_text = "".join(part.get("text", "") for part in content_text if isinstance(part, dict))
    meta = {
        "id": data.get("id"),
        "model": data.get("model"),
        "finish_reason": choice.get("finish_reason"),
        "usage": data.get("usage"),
    }
    return str(content_text).strip(), meta


def anthropic_content(user_prompt, prototypes, image_max_side=None):
    content = [{"type": "text", "text": user_prompt}]
    for path in prototypes:
        media_type, image_data = encoded_image(path, image_max_side=image_max_side)
        content.append({"type": "text", "text": f"Prototype screenshot: {path.name}"})
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": image_data,
            },
        })
    return content


def ask_anthropic(client, model, user_prompt, prototypes, max_tokens, temperature, image_max_side=None):
    if max_tokens is None:
        raise ValueError("Anthropic requests require max_tokens; use an explicit integer cap.")
    response = client.messages.create(
        model=model,
        system=SYSTEM_PROMPT,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": anthropic_content(user_prompt, prototypes, image_max_side)}],
    )
    parts = [block.text for block in response.content if getattr(block, "type", None) == "text"]
    meta = {
        "stop_reason": getattr(response, "stop_reason", None),
        "stop_sequence": getattr(response, "stop_sequence", None),
        "usage": response.usage.model_dump() if getattr(response, "usage", None) else None,
    }
    return "".join(parts).strip(), meta


def ask_chatanywhere_anthropic(client, model, user_prompt, prototypes, max_tokens, temperature, image_max_side=None):
    if max_tokens is None:
        raise ValueError("Anthropic-compatible requests require max_tokens; use an explicit integer cap.")
    payload = {
        "model": model,
        "system": SYSTEM_PROMPT,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": anthropic_content(user_prompt, prototypes, image_max_side)}],
    }
    request = urllib.request.Request(
        client["endpoint"],
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": client["api_key"],
            "user-agent": "master-thesis-track-b-generator/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc

    parts = [
        block.get("text", "")
        for block in data.get("content", [])
        if block.get("type") == "text"
    ]
    meta = {
        "id": data.get("id"),
        "type": data.get("type"),
        "model": data.get("model"),
        "stop_reason": data.get("stop_reason"),
        "stop_sequence": data.get("stop_sequence"),
        "usage": data.get("usage"),
    }
    return "".join(parts).strip(), meta


def ask_gwdg_openai(client, model, user_prompt, prototypes, max_tokens, temperature, image_max_side=None):
    content = [{"type": "text", "text": user_prompt}]
    for path in prototypes:
        media_type, image_data = encoded_image(path, image_max_side=image_max_side)
        content.append({"type": "text", "text": f"Prototype screenshot: {path.name}"})
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{media_type};base64,{image_data}",
            },
        })

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        "temperature": temperature,
    }
    add_optional_max_tokens(payload, max_tokens)
    request = urllib.request.Request(
        client["endpoint"],
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "accept": "application/json",
            "authorization": f"Bearer {client['api_key']}",
            "content-type": "application/json",
            "user-agent": "master-thesis-track-b-generator/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=360) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc

    data = unwrap_openai_payload(data)
    choice = data.get("choices", [{}])[0]
    message = choice.get("message", {})
    content_text = message.get("content", "")
    if isinstance(content_text, list):
        content_text = "".join(part.get("text", "") for part in content_text if isinstance(part, dict))
    meta = {
        "id": data.get("id"),
        "model": data.get("model"),
        "finish_reason": choice.get("finish_reason"),
        "usage": data.get("usage"),
    }
    return str(content_text).strip(), meta


def ask_model(provider, client, model, user_prompt, prototypes, max_tokens, temperature, image_max_side=None):
    if provider in {"openai", "tuzi-openai"}:
        return ask_openai(client, model, user_prompt, prototypes, max_tokens, temperature, image_max_side)
    if provider == "anthropic":
        return ask_anthropic(client, model, user_prompt, prototypes, max_tokens, temperature, image_max_side)
    if provider == "chatanywhere-anthropic":
        return ask_chatanywhere_anthropic(client, model, user_prompt, prototypes, max_tokens, temperature, image_max_side)
    if provider == "gwdg-openai":
        return ask_gwdg_openai(client, model, user_prompt, prototypes, max_tokens, temperature, image_max_side)
    raise ValueError(provider)


def parse_max_tokens(value):
    normalized = str(value).strip().lower()
    if normalized in {"none", "omit", "omitted", "null"}:
        return None
    try:
        parsed = int(normalized)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("max tokens must be an integer or one of: none, omit, null") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("max tokens must be positive, or use 'none' to omit the field")
    return parsed


def extract_html(raw):
    match = re.search(r"```(?:html)?\s*(.*?)```", raw, flags=re.IGNORECASE | re.DOTALL)
    if match:
        raw = match.group(1).strip()

    doctype = raw.lower().find("<!doctype")
    html = raw.lower().find("<html")
    start = doctype if doctype >= 0 else html
    if start > 0:
        raw = raw[start:].strip()
    return raw


def write_run(output_dir, html, raw_response, metadata):
    output_dir.mkdir(parents=True, exist_ok=False)
    (output_dir / "index.html").write_text(html, encoding="utf-8")
    (output_dir / "raw_response.txt").write_text(raw_response, encoding="utf-8")
    with (output_dir / "generation_metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--items-dir", default=str(DEFAULT_ITEMS_DIR))
    parser.add_argument("--item", required=True, help="Normalized Track B item id, for example F01_1daycloud.")
    parser.add_argument("--provider", choices=["openai", "tuzi-openai", "anthropic", "chatanywhere-anthropic", "gwdg-openai"],
                        default="chatanywhere-anthropic")
    parser.add_argument("--model", default="claude-sonnet-4-5-20250929")
    parser.add_argument("--run-name", help="Optional output directory name under generated/.")
    parser.add_argument(
        "--max-tokens",
        type=parse_max_tokens,
        default=20000,
        help="Maximum output tokens. Use 'none'/'omit' to omit max_tokens for OpenAI-compatible providers.",
    )
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-prototypes", type=int, default=6)
    parser.add_argument("--max-resources", type=int, default=120)
    parser.add_argument("--compact-max-resources", type=int, default=60)
    parser.add_argument(
        "--image-max-side",
        type=int,
        default=None,
        help="Resize attached prototype images to this max side before API upload. Default: 3000 for compact input, original for legacy. Use 0 to disable.",
    )
    parser.add_argument("--requirement-char-limit", type=int, default=12000)
    parser.add_argument("--workflow-char-limit", type=int, default=14000)
    parser.add_argument("--prompt-id", choices=sorted(USER_PROMPT_TEMPLATES), default=DEFAULT_PROMPT_ID)
    parser.add_argument(
        "--input-profile",
        choices=["auto", "legacy", "compact"],
        default="auto",
        help="Prompt input packing policy. auto uses compact input for TB-GEN-v16 and legacy input otherwise.",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_env()
    item_dir = Path(args.items_dir).resolve() / args.item
    if not item_dir.exists():
        raise SystemExit(f"ERROR: item directory not found: {item_dir}")

    (
        user_prompt,
        prototypes,
        resources,
        source_meta,
        workflow_controls,
        prompt_input_metadata,
    ) = build_prompt(item_dir, args)
    if args.dry_run:
        print(user_prompt)
        print(f"\nAttached prototype files: {[path.name for path in prototypes]}")
        return

    image_max_side = effective_image_max_side(args)
    client, base_url = build_client(args.provider)
    started = datetime.now().astimezone()
    started_time = time.time()
    raw_response, response_metadata = ask_model(
        args.provider,
        client,
        args.model,
        user_prompt,
        prototypes,
        args.max_tokens,
        args.temperature,
        image_max_side,
    )
    elapsed = time.time() - started_time
    html = extract_html(raw_response)

    run_name = args.run_name
    if not run_name:
        stamp = started.strftime("%Y%m%d_%H%M%S")
        run_name = f"{safe_name(args.provider)}_{safe_name(args.model)}_{stamp}"
    output_dir = item_dir / "generated" / run_name

    metadata = {
        "prompt_id": args.prompt_id,
        "provider": args.provider,
        "model": args.model,
        "base_url": base_url,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "started_at": started.isoformat(),
        "elapsed_seconds": round(elapsed, 2),
        "response_metadata": response_metadata,
        "item_id": args.item,
        "source_meta": source_meta,
        "system_prompt": SYSTEM_PROMPT,
        "user_prompt": user_prompt,
        "prompt_input_metadata": prompt_input_metadata,
        "workflow_controls": workflow_controls,
        "prototype_files": [str(path.relative_to(item_dir).as_posix()) for path in prototypes],
        "prototype_image_input": prototype_image_metadata(prototypes, image_max_side=image_max_side),
        "resource_paths_in_prompt": resources,
        "output_files": {
            "html": "index.html",
            "raw_response": "raw_response.txt",
            "metadata": "generation_metadata.json",
        },
    }
    write_run(output_dir, html, raw_response, metadata)
    print(f"Wrote generated UI to {output_dir}")
    print(f"HTML: {output_dir / 'index.html'}")
    print(f"Metadata: {output_dir / 'generation_metadata.json'}")


if __name__ == "__main__":
    main()
