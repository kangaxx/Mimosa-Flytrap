#!/usr/bin/env python3
"""Simple offline TTS example using pyttsx3.

Usage:
  python tts_pyttsx3.py --text "Hello" --output out.wav

Install:
  pip install pyttsx3

Note: On Linux you may need `espeak` or other local engines installed.
"""

import argparse
import pyttsx3
import os


def synthesize(text: str, output_path: str, rate: int = 150, volume: float = 1.0):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', max(0.0, min(1.0, volume)))

    # Save to file
    # Note: pyttsx3 will use platform TTS backend. Some backends may not support save_to_file.
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    print(f"Saved synthesized speech to: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument("--output", default="out.wav", help="Output wav path")
    parser.add_argument("--rate", type=int, default=150, help="Speech rate")
    parser.add_argument("--volume", type=float, default=1.0, help="Volume 0.0-1.0")
    args = parser.parse_args()

    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    synthesize(args.text, args.output, rate=args.rate, volume=args.volume)


if __name__ == "__main__":
    main()
