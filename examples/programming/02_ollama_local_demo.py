#!/usr/bin/env python3
"""Demo: call local Ollama OpenAI-compatible chat completions endpoint.

This script POSTs to the local Ollama HTTP API (OpenAI-compatible) to request
chat completions (e.g., generate a Python web-scraper). It prefers the
`requests` library and falls back to invoking `curl` if `requests` is not
available.

Usage:
  python examples/programming/02_ollama_local_demo.py --prompt "生成一份网页爬虫Python代码"

Environment variables:
  OLLAMA_BASE_URL    default: http://127.0.0.1:11434
  OLLAMA_API_KEY     default: ollama
  DEEPSEEK_MODEL     default: deepseek-r1:8b

"""
from __future__ import annotations

import os
import json
import argparse
import subprocess
from typing import Any, Dict


DEFAULT_BASE = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
DEFAULT_KEY = os.environ.get("OLLAMA_API_KEY", "ollama")
DEFAULT_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-r1:8b")


def build_payload(prompt: str, model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
    return {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }


def call_with_requests(url: str, headers: Dict[str, str], payload: Dict[str, Any], timeout: int = 120) -> Dict[str, Any]:
    import requests
    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    try:
        resp.raise_for_status()
    except Exception as e:
        # include response body to aid debugging (status and server message)
        body = resp.text if resp is not None else ''
        raise RuntimeError(f"HTTP {resp.status_code}: {body}") from e
    return resp.json()


def call_with_curl(url: str, headers: Dict[str, str], payload: Dict[str, Any], timeout: int = 120) -> Dict[str, Any]:
    # Build curl command similar to the user's example
    hdrs = []
    for k, v in headers.items():
        hdrs += ["-H", f"{k}: {v}"]

    data = json.dumps(payload, ensure_ascii=False)
    cmd = ["curl", "-sS", url, *hdrs, "-d", data]

    completed = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if completed.returncode != 0:
        raise RuntimeError(f"curl failed: {completed.stderr.strip()}")
    return json.loads(completed.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", "-p", default="生成一份网页爬虫Python代码")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL)
    parser.add_argument("--temperature", "-t", type=float, default=0.7)
    parser.add_argument("--max-tokens", type=int, default=2000)
    parser.add_argument("--use-curl", action="store_true", help="Force using curl instead of requests")
    args = parser.parse_args()

    endpoint = f"{DEFAULT_BASE.rstrip('/')}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEFAULT_KEY}",
    }

    payload = build_payload(args.prompt, args.model, args.temperature, args.max_tokens)

    print(f"Calling {endpoint} with model={args.model} temperature={args.temperature}")

    use_curl = args.use_curl
    if not use_curl:
        try:
            result = call_with_requests(endpoint, headers, payload)
        except Exception as e:  # fallback to curl
            print("requests call failed, falling back to curl:", e)
            use_curl = True

    if use_curl:
        result = call_with_curl(endpoint, headers, payload)

    # Pretty-print the returned JSON; try to extract content if following chat schema
    try:
        # Common OpenAI-style response: choices[0].message.content or choices[0].text
        if isinstance(result, dict) and "choices" in result:
            choice = result["choices"][0]
            content = None
            if isinstance(choice, dict):
                content = choice.get("message", {}).get("content") or choice.get("text")
            if content:
                print("\n=== Generated content ===\n")
                print(content)
            else:
                print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
