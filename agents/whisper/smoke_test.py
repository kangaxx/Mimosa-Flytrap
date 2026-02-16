#!/usr/bin/env python3
"""Lightweight smoke-test for agents/whisper examples.

This script performs quick checks:
- verifies imports for `faster_whisper`, `pyttsx3`, and `TTS` (Coqui)
- optionally runs a fast pyttsx3 synthesis to a temp file
- optionally runs Coqui TTS (disabled by default because it may download models)

Usage examples:
  python smoke_test.py --run-pyttsx3
  python smoke_test.py --run-pyttsx3 --run-coqui

The script is safe for CI/local checks; Coqui run is opt-in.
"""

import argparse
import sys
import tempfile
import os


def check_import(name: str):
    try:
        mod = __import__(name)
        print(f"OK: imported {name}")
        return True
    except Exception as e:
        print(f"MISSING: {name} -> {e}")
        return False


def test_pyttsx3(tmp_dir: str):
    try:
        import pyttsx3
    except Exception as e:
        print(f"pyttsx3 not available: {e}")
        return False

    out_path = os.path.join(tmp_dir, "pyttsx3_smoke.wav")
    try:
        engine = pyttsx3.init()
        engine.save_to_file("这是一个测试。", out_path)
        engine.runAndWait()
        exists = os.path.exists(out_path)
        print(f"pyttsx3 synthesize -> {out_path} (exists={exists})")
        return exists
    except Exception as e:
        print(f"pyttsx3 synth failed: {e}")
        return False


def test_coqui(tmp_dir: str):
    try:
        from TTS.api import TTS
    except Exception as e:
        print(f"Coqui TTS not available: {e}")
        return False

    out_path = os.path.join(tmp_dir, "coqui_smoke.wav")
    try:
        print("Note: Coqui TTS may download models on first run.")
        # Use default model (may be downloaded) — user explicitly opted in to run this
        tts = TTS(progress_bar=False, gpu=False)
        tts.tts_to_file(text="这是 Coqui 的测试。", file_path=out_path)
        exists = os.path.exists(out_path)
        print(f"Coqui TTS synthesize -> {out_path} (exists={exists})")
        return exists
    except Exception as e:
        print(f"Coqui TTS synth failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-pyttsx3", action="store_true", help="Run pyttsx3 synthesis smoke test")
    parser.add_argument("--run-coqui", action="store_true", help="Run Coqui TTS smoke test (may download models)")
    parser.add_argument("--cleanup", action="store_true", help="Remove temporary files after test")
    args = parser.parse_args()

    print("Checking basic imports (no heavy downloads)...")
    check_import('faster_whisper')
    check_import('pyttsx3')
    check_import('TTS')

    tmp_dir = tempfile.mkdtemp(prefix="whisper_smoke_")
    print(f"Using temp dir: {tmp_dir}")

    results = {}
    if args.run_pyttsx3:
        results['pyttsx3'] = test_pyttsx3(tmp_dir)

    if args.run_coqui:
        results['coqui'] = test_coqui(tmp_dir)

    print("Results:")
    for k, v in results.items():
        print(f" - {k}: {v}")

    if args.cleanup:
        try:
            for f in os.listdir(tmp_dir):
                os.remove(os.path.join(tmp_dir, f))
            os.rmdir(tmp_dir)
            print("Cleaned up temp files")
        except Exception:
            pass


if __name__ == '__main__':
    main()
