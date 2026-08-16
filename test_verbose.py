"""Test to get full error details from the API."""
import httpx
import json

BASE = "http://localhost:8000/api"


def test_create_agent_verbose():
    print("=== Testing Agent Creation (verbose) ===")
    r = httpx.post(
        f"{BASE}/agents",
        json={"prompt": "A helpful customer support agent that answers questions politely"},
        timeout=60,
    )
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")


if __name__ == "__main__":
    test_create_agent_verbose()
