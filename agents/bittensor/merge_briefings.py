#!/usr/bin/env python3
"""Merge all subnet briefing MD files into a single combined MD file."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT_DIR = SCRIPT_DIR / "briefings"
DEFAULT_OUTPUT = SCRIPT_DIR / "all_briefings.md"

_CN_NUMS = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
            "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
            "二十一", "二十二", "二十三", "二十四", "二十五", "二十六", "二十七", "二十八", "二十九", "三十",
            "三十一", "三十二", "三十三", "三十四", "三十五", "三十六", "三十七", "三十八", "三十九", "四十",
            "四十一", "四十二", "四十三", "四十四", "四十五", "四十六", "四十七", "四十八", "四十九", "五十",
            "五十一", "五十二", "五十三", "五十四", "五十五", "五十六", "五十七", "五十八", "五十九", "六十",
            "六十一", "六十二", "六十三", "六十四", "六十五", "六十六", "六十七", "六十八", "六十九", "七十",
            "七十一", "七十二", "七十三", "七十四", "七十五", "七十六", "七十七", "七十八", "七十九", "八十",
            "八十一", "八十二", "八十三", "八十四", "八十五", "八十六", "八十七", "八十八", "八十九", "九十",
            "九十一", "九十二", "九十三", "九十四", "九十五", "九十六", "九十七", "九十八", "九十九", "一百",
            "一百零一", "一百零二", "一百零三", "一百零四", "一百零五", "一百零六", "一百零七", "一百零八", "一百零九", "一百一十",
            "一百一十一", "一百一十二", "一百一十三", "一百一十四", "一百一十五", "一百一十六", "一百一十七", "一百一十八", "一百一十九", "一百二十",
            "一百二十一", "一百二十二", "一百二十三", "一百二十四", "一百二十五", "一百二十六", "一百二十七", "一百二十八", "一百二十九", "一百三十"]


def to_cn_num(n: int) -> str:
    """Convert a number to Chinese numeral string."""
    if 0 <= n < len(_CN_NUMS):
        return _CN_NUMS[n]
    return str(n)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Merge all subnet briefing MD files into one."
    )
    parser.add_argument(
        "--input-dir", type=Path, default=DEFAULT_INPUT_DIR,
        help=f"Briefings directory (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help=f"Output merged MD file (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"[error] directory not found: {args.input_dir}", file=sys.stderr)
        return 1

    # Collect and sort files by subnet ID
    files: list[tuple[int, Path]] = []
    for f in sorted(args.input_dir.glob("SN*.md")):
        m = re.match(r"SN(\d+)", f.stem)
        if m:
            files.append((int(m.group(1)), f))

    files.sort(key=lambda x: x[0])

    if not files:
        print("[error] no briefing files found", file=sys.stderr)
        return 1

    # Merge
    parts: list[str] = []
    for idx, (subnet_id, filepath) in enumerate(files, start=1):
        cn_num = to_cn_num(idx)
        content = filepath.read_text(encoding="utf-8").strip()
        # Replace the original H1 with "子网{N}"
        content = re.sub(r"^# .+", f"# 子网{cn_num}", content, count=1, flags=re.MULTILINE)
        parts.append(content)

    merged = "\n\n---\n\n".join(parts) + "\n"
    args.output.write_text(merged, encoding="utf-8")

    print(f"Merged {len(files)} briefings into {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
