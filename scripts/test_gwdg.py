"""Quick test for GWDG API key connectivity."""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GWDG_API_KEY")
base_url = os.getenv("GWDG_BASE_URL")

print(f"Key prefix: {key[:8] if key else 'NOT SET'}...")
print(f"Base URL: {base_url}")

try:
    from openai import OpenAI
except ImportError:
    print("openai package not found, trying requests...")
    import requests
    headers = {"Authorization": f"Bearer {key}"}
    r = requests.get(f"{base_url}/models", headers=headers, timeout=15)
    print(f"Status: {r.status_code}")
    if r.ok:
        data = r.json()
        models = [m["id"] for m in data.get("data", [])]
        print("Models:", models[:10])
    else:
        print("Error:", r.text[:300])
    sys.exit(0)

client = OpenAI(api_key=key, base_url=base_url)

# List models
print("\n--- Available models ---")
try:
    models = client.models.list()
    ids = [m.id for m in models.data]
    for mid in ids[:15]:
        print(f"  {mid}")
    if len(ids) > 15:
        print(f"  ... and {len(ids)-15} more")
except Exception as e:
    print(f"Model list error: {e}")
    ids = ["meta-llama-3.1-8b-instruct"]

# Pick a model to test
test_model = ids[0] if ids else "meta-llama-3.1-8b-instruct"
print(f"\n--- Chat test with {test_model} ---")
try:
    resp = client.chat.completions.create(
        model=test_model,
        messages=[{"role": "user", "content": "Say hello in one word."}],
        max_tokens=10,
    )
    print(f"Response: {resp.choices[0].message.content}")
    print("GWDG key is working!")
except Exception as e:
    print(f"Chat error: {e}")
