#!/usr/bin/env python3
"""Example LangChain agent for Ollama + deepseek-r1 (macOS example)

This is a small, self-contained example showing how to:
- load environment from .env
- select Ollama as model backend
- call a placeholder Deepseek embeddings HTTP endpoint

Replace the Deepseek wrapper with the official SDK when available.
"""
import os
import argparse
import json
import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_TEMPERATURE = float(os.environ.get("DEFAULT_TEMPERATURE", "0.2"))


class DeepseekEmbeddings:
    """Minimal placeholder client for deepseek-r1 embeddings via HTTP.
    Expects DEEPSEEK_API_URL and DEEPSEEK_API_KEY in env.
    """

    def __init__(self):
        self.url = os.environ.get("DEEPSEEK_API_URL")
        self.key = os.environ.get("DEEPSEEK_API_KEY")
        if not self.url or not self.key:
            raise ValueError("Set DEEPSEEK_API_URL and DEEPSEEK_API_KEY in .env")

    def embed(self, texts):
        resp = requests.post(
            self.url,
            headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
            json={"model": os.environ.get("DEEPSEEK_MODEL", "deepseek-r1"), "input": texts},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()


class LangChainAgent:
    def __init__(self, model_type: str = "ollama"):
        self.model_type = model_type
        self.temperature = DEFAULT_TEMPERATURE
        if model_type == "ollama":
            self._initialize_ollama()
        elif model_type == "openai":
            self._initialize_openai()
        else:
            raise ValueError("Unsupported model_type: %s" % model_type)

    def _initialize_ollama(self):
        self.ollama_base = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model = os.environ.get("OLLAMA_MODEL", "llama2-13b-chat")

    def _initialize_openai(self):
        self.openai_key = os.environ.get("OPENAI_API_KEY")
        if not self.openai_key or not self.openai_key.startswith("sk-"):
            raise ValueError("OpenAI API key missing or malformed")

    def run_simple_query(self, prompt: str):
        if self.model_type == "ollama":
            return self._call_ollama(prompt)
        else:
            return self._call_openai(prompt)

    def _call_ollama(self, prompt: str):
        url = f"{self.ollama_base}/v1/completions"
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "temperature": self.temperature,
            "max_tokens": 200,
        }
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()

    def _call_openai(self, prompt: str):
        import openai

        openai.api_key = os.environ.get("OPENAI_API_KEY")
        r = openai.ChatCompletion.create(model=os.environ.get("OPENAI_MODEL", "gpt-4o"), messages=[{"role": "user", "content": prompt}], temperature=self.temperature)
        return r


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-type", choices=["ollama", "openai"], default=os.environ.get("MODEL_TYPE", "ollama"))
    parser.add_argument("--prompt", default="Hello from macOS example")
    parser.add_argument("--interactive", action="store_true")
    args = parser.parse_args()

    agent = LangChainAgent(model_type=args.model_type)

    if args.interactive:
        while True:
            try:
                p = input("prompt> ")
            except EOFError:
                break
            if not p:
                continue
            out = agent.run_simple_query(p)
            print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        out = agent.run_simple_query(args.prompt)
        print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
