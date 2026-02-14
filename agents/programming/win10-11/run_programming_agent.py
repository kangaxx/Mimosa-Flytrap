#!/usr/bin/env python3
"""Interactive Programming Agent for Windows 11

This file mirrors the Unix example but is placed here for convenience when
running on Windows. It supports Ollama and deepseek-r1 via HTTP.
"""
import os
import json
import argparse
import subprocess
from typing import List, Any
from dotenv import load_dotenv
import requests

load_dotenv()

OLLAMA_BASE = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama2-13b-chat")
DEFAULT_TEMPERATURE = float(os.environ.get("DEFAULT_TEMPERATURE", "0.2"))


class DeepseekClient:
    def __init__(self):
        self.url = os.environ.get("DEEPSEEK_API_URL")
        self.key = os.environ.get("DEEPSEEK_API_KEY")
        self.model = os.environ.get("DEEPSEEK_MODEL", "deepseek-r1:8b")

    def embed(self, texts: List[str]) -> Any:
        if not self.url or not self.key:
            raise RuntimeError("DEEPSEEK_API_URL/DEEPSEEK_API_KEY not set in environment")
        resp = requests.post(
            self.url,
            headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
            json={"model": self.model, "input": texts},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()


class FullStackAgent:
    def __init__(self, auto_execute: bool = False):
        self.auto = auto_execute
        self.deepseek = None
        try:
            self.deepseek = DeepseekClient()
        except RuntimeError:
            self.deepseek = None

    def call_ollama(self, system: str, user_prompt: str) -> str:
        url = f"{OLLAMA_BASE}/v1/completions"
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": f"System:\n{system}\n\nUser:\n{user_prompt}",
            "temperature": DEFAULT_TEMPERATURE,
            "max_tokens": 1024,
        }
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict) and "choices" in data:
            txt = data["choices"][0].get("text") or data["choices"][0].get("message", {}).get("content")
            return txt
        return json.dumps(data)

    def embed_texts(self, texts: List[str]):
        if not self.deepseek:
            raise RuntimeError("Deepseek client not configured (DEEPSEEK_API_URL missing)")
        return self.deepseek.embed(texts)

    def read_file(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, path: str, content: str) -> None:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def execute_shell(self, cmd: str) -> dict:
        destructive_keywords = ["Remove-Item", "Format-Volume", "shutdown", "restart-computer"]
        if not self.auto and any(k.lower() in cmd.lower() for k in destructive_keywords):
            ans = input(f"Command appears destructive. Confirm execute? [y/N]: ")
            if ans.strip().lower() != "y":
                return {"cmd": cmd, "status": "skipped", "output": "user declined"}

        try:
            completed = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            return {"cmd": cmd, "returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}
        except subprocess.SubprocessError as e:
            return {"cmd": cmd, "status": "error", "error": str(e)}


SYSTEM_PROMPT = (
    "You are a senior full-stack engineer assisting with code tasks.\n"
    "You have these tools available: shell(command) -> runs a shell command; "
    "read(path) -> returns file contents; write(path, content) -> writes file; embed(texts) -> returns embeddings.\n"
    "When you want to use a tool, return a single JSON object with an 'actions' array. "
    "Each action is an object with 'type' and 'args'. Types: 'shell','read','write','embed','message'.\n"
)


def try_parse_json(s: str):
    s = s.strip()
    try:
        return json.loads(s)
    except Exception:
        start = s.find("{")
        end = s.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(s[start:end+1])
            except Exception:
                return None
    return None


def interactive_loop(agent: FullStackAgent):
    print("Full-stack programming agent — interactive mode. Type 'exit' to quit.")
    while True:
        try:
            user = input("task> ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not user:
            continue
        if user.strip().lower() in ("exit", "quit"):
            break

        print("-> calling Ollama for plan...")
        resp = agent.call_ollama(SYSTEM_PROMPT, user)
        parsed = try_parse_json(resp)
        if not parsed:
            print("LLM response (not JSON):\n", resp)
            continue

        actions = parsed.get("actions", [])
        for a in actions:
            t = a.get("type")
            args = a.get("args", {})
            if t == "shell":
                print(json.dumps(agent.execute_shell(args.get("cmd")), indent=2, ensure_ascii=False))
            elif t == "read":
                try:
                    print(agent.read_file(args.get("path")))
                except Exception as e:
                    print("read error:", e)
            elif t == "write":
                try:
                    agent.write_file(args.get("path"), args.get("content", ""))
                    print("wrote", args.get("path"))
                except Exception as e:
                    print("write error:", e)
            elif t == "embed":
                try:
                    print(agent.embed_texts(args.get("texts", [])))
                except Exception as e:
                    print("embed error:", e)
            elif t == "message":
                print(args.get("text", ""))
            else:
                print("unknown action", a)


def run_single_task(agent: FullStackAgent, task: str):
    print("-> calling Ollama for plan...")
    resp = agent.call_ollama(SYSTEM_PROMPT, task)
    parsed = try_parse_json(resp)
    if not parsed:
        print("LLM response:\n", resp)
        return
    actions = parsed.get("actions", [])
    for a in actions:
        t = a.get("type")
        args = a.get("args", {})
        if t == "shell":
            print(json.dumps(agent.execute_shell(args.get("cmd")), indent=2, ensure_ascii=False))
        elif t == "read":
            try:
                print(agent.read_file(args.get("path")))
            except Exception as e:
                print("read error:", e)
        elif t == "write":
            try:
                agent.write_file(args.get("path"), args.get("content", ""))
                print("wrote", args.get("path"))
            except Exception as e:
                print("write error:", e)
        elif t == "embed":
            print(agent.embed_texts(args.get("texts", [])))
        elif t == "message":
            print(args.get("text", ""))
        else:
            print("unknown action", a)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", help="One-off task to run (non-interactive)")
    parser.add_argument("--auto", action="store_true", help="Auto-execute shell commands without confirmations")
    args = parser.parse_args()

    agent = FullStackAgent(auto_execute=args.auto)
    if args.task:
        run_single_task(agent, args.task)
    else:
        interactive_loop(agent)


if __name__ == "__main__":
    main()
