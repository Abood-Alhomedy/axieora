"""Test OpenRouter integration - agent creation."""
# pyrefly: ignore [missing-import]
import httpx
import json

BASE = "http://localhost:8000/api"


def test_health():
    r = httpx.get(f"{BASE}/health", timeout=10)
    print(f"Health: {r.status_code} - {r.json()}")
    return r.status_code == 200


def test_create_agent():
    print("\n=== Testing Agent Creation ===")
    r = httpx.post(
        f"{BASE}/agents",
        json={"prompt": "A helpful customer support agent that answers questions politely"},
        timeout=60,
    )
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        d = r.json()
        print(f"Agent Name: {d['name']}")
        print(f"Description: {d['definition']['description']}")
        valid = d['validation']['valid']
        print(f"Validation: {'PASS' if valid else 'FAIL'}")
        if not valid:
            for e in d['validation']['errors']:
                print(f"  Error: {e}")
        return d['name']
    else:
        print(f"Error: {r.text[:800]}")
        return None


if __name__ == "__main__":
    if test_health():
        test_create_agent()
    else:
        print("Server not running!")
