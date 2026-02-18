# GUI Usage — Ollama Local Demo

This document explains how to configure, run, and package the `gui_ollama_demo.py` desktop GUI which calls a local Ollama HTTP endpoint (used with `deepseek-r1` models).

## Requirements
- macOS with Python 3.10+ (tested with Homebrew Python 3.14).
- Ollama installed and running locally (default HTTP API: `http://127.0.0.1:11434`).
- Python modules: `requests` (the demo prefers `requests`, with `curl` as fallback). The project packaging script installs `pyinstaller` in a build venv.

Optional (voice/STT/TTS) dependencies
- For local STT/TTS features (Record / Transcribe / Speak), install the extra Python packages into the build venv or your active virtualenv. From this repository root you can run:

```bash
# use the packaged venv used by the GUI build (recommended for packaging):
examples/programming/.venv_build/bin/python -m pip install --upgrade pip
examples/programming/.venv_build/bin/python -m pip install faster-whisper sounddevice soundfile numpy pyttsx3

# or, if you prefer a development venv:
python3 -m venv .venv
source .venv/bin/activate
pip install faster-whisper sounddevice soundfile numpy pyttsx3
```

- Note: `playsound` is optional and may fail to build on some macOS/Python setups; the GUI falls back to macOS `say`/`afplay` when available. If a wheel/build fails for a package, consult the package README (for native libs you may need Xcode command-line tools or Homebrew packages).

Voice/STT model notes
- If you plan to use the faster-whisper based STT features, you can point the GUI `Model` field to a local faster-whisper model directory (a `model.bin` plus `config.json`/`tokenizer.json`). See the agents whisper README for details on model layout and supported formats: [agents/whisper/README.md](agents/whisper/README.md#L1).


## Files
- `gui_ollama_demo.py` — the Tkinter GUI application.
- `02_ollama_local_demo.py` — the demo module the GUI loads dynamically; contains `build_payload`, `call_with_requests`, and `call_with_curl` helpers.
- `build_mac_app.sh` — helper to package the GUI with PyInstaller (creates `.venv_build`).

## Environment / Configuration
The demo uses these defaults inside `02_ollama_local_demo.py`:
- `DEFAULT_BASE`: `http://127.0.0.1:11434`
- `DEFAULT_MODEL`: `deepseek-r1:8b`
- `DEFAULT_KEY`: `ollama`

If you keep different host/port or API key, either:
- edit `02_ollama_local_demo.py` defaults, or
- set the fields in the GUI at runtime (the GUI exposes `Model`, `Temperature`, and `Max tokens` inputs).

## Run in development (recommended)
1. Create and activate a virtualenv (optional but recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r examples/programming/requirements.txt
```
2. Start Ollama and ensure the model is available:
```bash
# example curl to verify
curl -sS -X GET 'http://127.0.0.1:11434/v1/models' -H 'Authorization: Bearer ollama' | jq
```
3. Run the GUI:
```bash
python3 examples/programming/gui_ollama_demo.py
```

Note: The GUI now exposes a `Timeout (s)` field (default 120) to control the request timeout for calls to the local Ollama endpoint.

## Run packaged app (what we built)
- Launch `.app` bundle:
```bash
open examples/programming/dist/OllamaLocalDemo.app
```
- Or run the standalone executable (background + log):
```bash
./examples/programming/dist/OllamaLocalDemo &>/tmp/ollama_gui_run.log & echo $!
```
Check `/tmp/ollama_gui_run.log` for stdout/stderr when running the binary directly.

## Package (build a macOS app)
1. Ensure you have Homebrew Python available or your desired Python on PATH.
2. Run the build helper:
```bash
chmod +x examples/programming/build_mac_app.sh
./examples/programming/build_mac_app.sh
```
Notes:
- PyInstaller prints a deprecation warning if using `--onefile` with macOS `.app` bundles. Consider using `--onedir` for future builds.
- Packaging may warn about a broken `tkinter` detection; ensure the system Tk is available if you see GUI problems.

## Troubleshooting
- Syntax errors while packaging usually mean the source file contains stray text/code fences — ensure `gui_ollama_demo.py` is a valid Python module.
- If the GUI shows no response, verify Ollama is running and the model exists (see `curl` above).
- If the app fails to display the GUI after packaging, run the binary in a terminal to capture logs.

## Quick test prompt
Use the GUI to enter a short prompt (for example, `Write a haiku about macOS`) and click `Send`. The response will appear in the `Response` area when the request completes.

## Where to find logs
- If you launched the binary with redirection (above), logs are in `/tmp/ollama_gui_run.log`.
- PyInstaller build logs are under `examples/programming/build/` and the final artifacts under `examples/programming/dist/`.

---
If you'd like, I can also add a small `README` header or inline comments to `gui_ollama_demo.py` explaining configuration points.
