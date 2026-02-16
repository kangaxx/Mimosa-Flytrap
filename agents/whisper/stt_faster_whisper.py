#!/usr/bin/env python3
"""Simple local STT example using faster-whisper.

Usage:
  python stt_faster_whisper.py --model small --input audio.wav --output out.txt

This script is a minimal example. Install dependencies with:
  pip install faster-whisper
"""

import argparse
from faster_whisper import WhisperModel
import os


def transcribe(model_size: str, input_path: str, output_path: str, device: str = "cpu"):
    model = WhisperModel(model_size, device=device)
    segments, info = model.transcribe(input_path, beam_size=5)

    text = ""
    for segment in segments:
        text += segment.text

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text.strip())

    print(f"Saved transcription to: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="small", help="Model size (tiny, base, small, medium, large)")
    parser.add_argument("--input", required=True, help="Input audio file (wav/mp3/...)")
    parser.add_argument("--output", default="transcription.txt", help="Output text file")
    parser.add_argument("--device", default="cpu", help="Device: cpu or cuda")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise SystemExit(f"Input file not found: {args.input}")

    transcribe(args.model, args.input, args.output, device=args.device)


if __name__ == "__main__":
    main()
