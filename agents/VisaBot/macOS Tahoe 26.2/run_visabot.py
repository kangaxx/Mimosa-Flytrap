#!/usr/bin/env python3
import argparse
import os
from typing import Optional

import requests


def load_dotenv_file(path: str = ".env") -> None:
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


load_dotenv_file()

MODEL_TYPE = os.getenv("MODEL_TYPE", "ollama").strip().lower()
VISABOT_TEMPERATURE = float(os.getenv("VISABOT_TEMPERATURE", "0.2"))

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = (
    "You are VisaBot, a visa and immigration process assistant. "
    "Provide clear checklist-style answers, mention uncertainty when needed, "
    "and remind the user to verify with official embassy/immigration websites."
)


def ask_ollama(question: str) -> str:
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        "options": {"temperature": VISABOT_TEMPERATURE},
        "stream": False,
    }
    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    return data.get("message", {}).get("content", "")


def ask_openai(question: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set in .env")

    url = f"{OPENAI_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL,
        "temperature": VISABOT_TEMPERATURE,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
    }

    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices", [])
    if not choices:
        return ""
    return choices[0].get("message", {}).get("content", "")


def ask_visabot(question: str) -> str:
    if MODEL_TYPE == "openai":
        return ask_openai(question)
    return ask_ollama(question)


def run_single(question: str) -> None:
    answer = ask_visabot(question)
    print("\n=== VisaBot ===")
    print(answer.strip() or "(empty response)")


def run_interactive() -> None:
    print("VisaBot interactive mode. Type 'exit' to quit.\n")
    while True:
        try:
            user_input = input("visa> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye")
            return

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Bye")
            return

        try:
            run_single(user_input)
        except Exception as exc:
            print(f"Error: {exc}")


def main(question: Optional[str]) -> None:
    if question:
        run_single(question)
    else:
        run_interactive()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VisaBot for macOS Tahoe 26.2")
    parser.add_argument("--question", help="Ask VisaBot a single question and exit")
    args = parser.parse_args()

    try:
        main(args.question)
    except Exception as exc:
        print(f"Fatal: {exc}")
        raise
