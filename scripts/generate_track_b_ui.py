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
}


def load_env_file(path):
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
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


def image_to_b64(path):
    return base64.b64encode(path.read_bytes()).decode("ascii")


def image_media_type(path):
    media_type, _ = mimetypes.guess_type(path.name)
    return media_type or "image/png"


def build_prompt(item_dir, args):
    requirement = read_text(item_dir / "requirement.md")
    workflow = json.dumps(read_json(item_dir / "workflow.json"), indent=2, ensure_ascii=False)
    meta = read_json(item_dir / "source_meta.json")
    resources = collect_resource_paths(item_dir, args.max_resources)
    prototypes = collect_prototypes(item_dir, args.max_prototypes)
    if not prototypes:
        raise SystemExit(f"ERROR: no prototype screenshots found under {item_dir / 'prototypes'}")

    resource_text = "\n".join(f"- ../../resources/{path}" for path in resources)
    if not resource_text:
        resource_text = "- No local resources were found."

    prototype_text = "\n".join(f"- {path.name}" for path in prototypes)
    route_ids = [path.stem for path in prototypes]
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
    )
    return user_prompt, prototypes, resources, meta


def build_client(provider):
    if provider == "openai":
        from openai import OpenAI

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise SystemExit("ERROR: OPENAI_API_KEY not set.")
        base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE")
        client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
        return client, base_url or "https://api.openai.com/v1"

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


def ask_openai(client, model, user_prompt, prototypes, max_tokens, temperature):
    content = [{"type": "text", "text": user_prompt}]
    for path in prototypes:
        content.append({"type": "text", "text": f"Prototype screenshot: {path.name}"})
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{image_media_type(path)};base64,{image_to_b64(path)}",
                "detail": "high",
            },
        })

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    choice = response.choices[0]
    meta = {
        "finish_reason": getattr(choice, "finish_reason", None),
        "usage": response.usage.model_dump() if getattr(response, "usage", None) else None,
    }
    return choice.message.content.strip(), meta


def anthropic_content(user_prompt, prototypes):
    content = [{"type": "text", "text": user_prompt}]
    for path in prototypes:
        content.append({"type": "text", "text": f"Prototype screenshot: {path.name}"})
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": image_media_type(path),
                "data": image_to_b64(path),
            },
        })
    return content


def ask_anthropic(client, model, user_prompt, prototypes, max_tokens, temperature):
    response = client.messages.create(
        model=model,
        system=SYSTEM_PROMPT,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": anthropic_content(user_prompt, prototypes)}],
    )
    parts = [block.text for block in response.content if getattr(block, "type", None) == "text"]
    meta = {
        "stop_reason": getattr(response, "stop_reason", None),
        "stop_sequence": getattr(response, "stop_sequence", None),
        "usage": response.usage.model_dump() if getattr(response, "usage", None) else None,
    }
    return "".join(parts).strip(), meta


def ask_chatanywhere_anthropic(client, model, user_prompt, prototypes, max_tokens, temperature):
    payload = {
        "model": model,
        "system": SYSTEM_PROMPT,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": anthropic_content(user_prompt, prototypes)}],
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


def ask_gwdg_openai(client, model, user_prompt, prototypes, max_tokens, temperature):
    content = [{"type": "text", "text": user_prompt}]
    for path in prototypes:
        content.append({"type": "text", "text": f"Prototype screenshot: {path.name}"})
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{image_media_type(path)};base64,{image_to_b64(path)}",
            },
        })

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
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


def ask_model(provider, client, model, user_prompt, prototypes, max_tokens, temperature):
    if provider == "openai":
        return ask_openai(client, model, user_prompt, prototypes, max_tokens, temperature)
    if provider == "anthropic":
        return ask_anthropic(client, model, user_prompt, prototypes, max_tokens, temperature)
    if provider == "chatanywhere-anthropic":
        return ask_chatanywhere_anthropic(client, model, user_prompt, prototypes, max_tokens, temperature)
    if provider == "gwdg-openai":
        return ask_gwdg_openai(client, model, user_prompt, prototypes, max_tokens, temperature)
    raise ValueError(provider)


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
    parser.add_argument("--provider", choices=["openai", "anthropic", "chatanywhere-anthropic", "gwdg-openai"],
                        default="chatanywhere-anthropic")
    parser.add_argument("--model", default="claude-sonnet-4-5-20250929")
    parser.add_argument("--run-name", help="Optional output directory name under generated/.")
    parser.add_argument("--max-tokens", type=int, default=20000)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-prototypes", type=int, default=6)
    parser.add_argument("--max-resources", type=int, default=120)
    parser.add_argument("--requirement-char-limit", type=int, default=12000)
    parser.add_argument("--workflow-char-limit", type=int, default=14000)
    parser.add_argument("--prompt-id", choices=sorted(USER_PROMPT_TEMPLATES), default=DEFAULT_PROMPT_ID)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_env()
    item_dir = Path(args.items_dir).resolve() / args.item
    if not item_dir.exists():
        raise SystemExit(f"ERROR: item directory not found: {item_dir}")

    user_prompt, prototypes, resources, source_meta = build_prompt(item_dir, args)
    if args.dry_run:
        print(user_prompt)
        print(f"\nAttached prototype files: {[path.name for path in prototypes]}")
        return

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
        "prototype_files": [str(path.relative_to(item_dir).as_posix()) for path in prototypes],
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
