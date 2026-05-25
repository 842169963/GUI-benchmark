"""List models available to the local GWDG/SAIA API key."""

import json
import os
import urllib.request
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "https://chat-ai.academiccloud.de/v1"


def load_env_file(path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def main():
    load_env_file(PROJECT_ROOT / ".env")
    api_key = os.environ.get("GWDG_API_KEY")
    if not api_key:
        raise SystemExit("ERROR: GWDG_API_KEY not found in .env or environment.")

    base_url = os.environ.get("GWDG_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    request = urllib.request.Request(
        f"{base_url}/models",
        headers={
            "accept": "application/json",
            "authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))

    models = payload.get("data", payload)
    ids = []
    for model in models:
        if isinstance(model, dict):
            ids.append(model.get("id") or model.get("name") or json.dumps(model, ensure_ascii=False))
        else:
            ids.append(str(model))

    for model_id in sorted(value for value in ids if value):
        print(model_id)


if __name__ == "__main__":
    main()
