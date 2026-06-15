"""Low-cost model capability probes for Track B model selection.

The default mode only lists models from the provider endpoint. Use
``--chat-smoke`` to send a tiny "OK" request. Even when ``--output-cap`` is
large, the prompt asks for a one-token answer, so the probe tests request
acceptance rather than forcing long generation.
"""

import argparse
import base64
import json
import mimetypes
import os
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "track_b" / "model_capabilities"


PROVIDERS = {
    "gwdg-openai": {
        "api_key_env": ["GWDG_API_KEY"],
        "base_url_env": ["GWDG_BASE_URL"],
        "default_base_url": "https://chat-ai.academiccloud.de/v1",
        "style": "openai-chat",
    },
    "openai": {
        "api_key_env": ["OPENAI_API_KEY"],
        "base_url_env": ["OPENAI_BASE_URL", "OPENAI_API_BASE"],
        "default_base_url": "https://api.openai.com/v1",
        "style": "openai-chat",
    },
    "tuzi-openai": {
        "api_key_env": ["TUZI_API_KEY"],
        "base_url_env": ["TUZI_BASE_URL"],
        "default_base_url": "https://api.tu-zi.com/v1",
        "style": "openai-chat",
    },
    "chatanywhere-anthropic": {
        "api_key_env": ["ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"],
        "base_url_env": ["ANTHROPIC_BASE_URL"],
        "default_base_url": "https://api.chatanywhere.org/v1",
        "style": "anthropic-messages",
    },
}


def load_env_file(path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def first_env(keys):
    for key in keys:
        value = os.environ.get(key)
        if value:
            return key, value
    return None, None


def provider_config(provider):
    config = PROVIDERS[provider]
    key_name, api_key = first_env(config["api_key_env"])
    if not api_key:
        raise SystemExit(f"ERROR: missing API key env for {provider}: {config['api_key_env']}")
    _, base_url = first_env(config["base_url_env"])
    base_url = (base_url or config["default_base_url"]).rstrip("/")
    return {
        "provider": provider,
        "api_key_env": key_name,
        "api_key": api_key,
        "base_url": base_url,
        "style": config["style"],
    }


def request_json(url, headers, payload=None, timeout=60):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    method = "GET" if payload is None else "POST"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    started = time.time()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return {
                "ok": True,
                "status": response.status,
                "elapsed_seconds": round(time.time() - started, 3),
                "json": json.loads(body),
            }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {
            "ok": False,
            "status": exc.code,
            "elapsed_seconds": round(time.time() - started, 3),
            "error": body[:2000],
        }
    except Exception as exc:
        return {
            "ok": False,
            "status": None,
            "elapsed_seconds": round(time.time() - started, 3),
            "error": repr(exc),
        }


def list_models(config):
    if config["style"] == "anthropic-messages":
        return {"ok": None, "note": "Anthropic-style ChatAnywhere endpoint has no /models probe here."}
    return request_json(
        f"{config['base_url']}/models",
        {
            "accept": "application/json",
            "authorization": f"Bearer {config['api_key']}",
            "user-agent": "master-thesis-model-probe/1.0",
        },
    )


def image_media_type(path):
    guessed, _ = mimetypes.guess_type(str(path))
    return guessed or "image/png"


def image_to_b64(path):
    return base64.b64encode(path.read_bytes()).decode("ascii")


def openai_chat_payload(model, max_tokens, vision_image=None):
    if vision_image:
        image_path = Path(vision_image)
        content = [
            {"type": "text", "text": "Reply with OK only."},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{image_media_type(image_path)};base64,{image_to_b64(image_path)}"
                },
            },
        ]
    else:
        content = "Reply with OK only."
    return {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "temperature": 0,
        "max_tokens": max_tokens,
    }


def anthropic_payload(model, max_tokens, vision_image=None):
    content = [{"type": "text", "text": "Reply with OK only."}]
    if vision_image:
        image_path = Path(vision_image)
        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": image_media_type(image_path),
                    "data": image_to_b64(image_path),
                },
            }
        )
    return {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": 0,
        "messages": [{"role": "user", "content": content}],
    }


def chat_smoke(config, model, max_tokens, vision_image=None):
    if config["style"] == "openai-chat":
        return request_json(
            f"{config['base_url']}/chat/completions",
            {
                "accept": "application/json",
                "authorization": f"Bearer {config['api_key']}",
                "content-type": "application/json",
                "user-agent": "master-thesis-model-probe/1.0",
            },
            openai_chat_payload(model, max_tokens, vision_image=vision_image),
            timeout=90,
        )

    endpoint = config["base_url"]
    if endpoint.endswith("/v1"):
        endpoint = f"{endpoint}/messages"
    elif not endpoint.endswith("/messages"):
        endpoint = f"{endpoint}/v1/messages"
    return request_json(
        endpoint,
        {
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": config["api_key"],
            "user-agent": "master-thesis-model-probe/1.0",
        },
        anthropic_payload(model, max_tokens, vision_image=vision_image),
        timeout=90,
    )


def unwrap_openai_payload(payload):
    if isinstance(payload, dict) and "choices" not in payload and isinstance(payload.get("data"), dict):
        return payload["data"]
    return payload


def model_ids(model_response):
    if not model_response.get("ok"):
        return []
    payload = unwrap_openai_payload(model_response.get("json", {}))
    data = payload.get("data", payload)
    ids = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                model_id = item.get("id") or item.get("name")
            else:
                model_id = str(item)
            if model_id:
                ids.append(model_id)
    return sorted(set(ids))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=sorted(PROVIDERS), required=True)
    parser.add_argument("--model", action="append", default=[], help="Model id to probe. Repeatable.")
    parser.add_argument("--chat-smoke", action="store_true", help="Send tiny one-answer chat probes.")
    parser.add_argument("--output-cap", action="append", type=int, default=[], help="Requested max_tokens to test.")
    parser.add_argument("--vision-image", help="Optional local image for a vision smoke probe.")
    parser.add_argument("--output", type=Path, help="Output JSON path.")
    args = parser.parse_args()

    load_env_file(PROJECT_ROOT / ".env")
    config = provider_config(args.provider)
    output_caps = args.output_cap or [1]

    result = {
        "schema_version": "track-b-model-capability-smoke-v1",
        "created_at": datetime.now().astimezone().isoformat(),
        "provider": args.provider,
        "base_url": config["base_url"],
        "api_key_env": config["api_key_env"],
        "note": (
            "Chat smoke prompts request 'OK' only. Large output-cap values test request "
            "acceptance, not actual long generation."
        ),
        "models_endpoint": list_models(config),
        "probes": [],
    }
    result["available_model_ids"] = model_ids(result["models_endpoint"])

    if args.chat_smoke:
        for model in args.model:
            for cap in output_caps:
                probe = {
                    "model": model,
                    "requested_max_tokens": cap,
                    "vision_image": str(Path(args.vision_image).resolve()) if args.vision_image else None,
                }
                response = chat_smoke(config, model, cap, vision_image=args.vision_image)
                probe.update(response)
                if "json" in probe:
                    payload = unwrap_openai_payload(probe.pop("json"))
                    choice = (payload.get("choices") or [{}])[0] if isinstance(payload, dict) else {}
                    probe["response_metadata"] = {
                        "id": payload.get("id") if isinstance(payload, dict) else None,
                        "model": payload.get("model") if isinstance(payload, dict) else None,
                        "finish_reason": choice.get("finish_reason"),
                        "stop_reason": payload.get("stop_reason") if isinstance(payload, dict) else None,
                        "usage": payload.get("usage") if isinstance(payload, dict) else None,
                    }
                result["probes"].append(probe)

    output_path = args.output
    if output_path is None:
        stamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
        output_path = DEFAULT_OUTPUT_DIR / f"model_capability_smoke_{args.provider}_{stamp}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
