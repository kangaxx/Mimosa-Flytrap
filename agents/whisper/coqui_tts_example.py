#!/usr/bin/env python3
"""Coqui TTS example (local, higher-quality TTS)

Usage:
  python coqui_tts_example.py --text "Hello" --output out.wav [--model tts_models/en/ljspeech/tacotron2-DDC] [--gpu]

Install:
  pip install TTS

Note: Coqui TTS requires `torch` and may download model weights on first run.
"""

import argparse
import sys

def synthesize(text: str, output_path: str, model_name: str = None, use_gpu: bool = False):
    try:
        from TTS.api import TTS
    except Exception as e:
        print("Failed to import Coqui TTS. Install with: pip install TTS", file=sys.stderr)
        raise

    if model_name:
        tts = TTS(model_name=model_name, progress_bar=True, gpu=use_gpu)
    else:
        # Use default model shipped with the TTS package (may vary)
        tts = TTS(progress_bar=True, gpu=use_gpu)

    tts.tts_to_file(text=text, file_path=output_path)
    print(f"Saved Coqui TTS output to: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument("--output", default="coqui_out.wav", help="Output wav path")
    parser.add_argument("--model", default=None, help="Optional Coqui TTS model name")
    parser.add_argument("--gpu", action="store_true", help="Use GPU if available")
    args = parser.parse_args()

    synthesize(args.text, args.output, model_name=args.model, use_gpu=args.gpu)


if __name__ == "__main__":
    main()
