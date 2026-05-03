#!/usr/bin/env python3
"""Generate a Chinese comprehensive report from Bittensor subnet briefing MD files.

Reads all SN{id}_{name}.md files from the briefings/ directory, parses their
structured content, classifies hardware requirements, and produces a single
consolidated report in Chinese.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT_DIR = SCRIPT_DIR / "briefings"
DEFAULT_OUTPUT = SCRIPT_DIR / "subnet_report.md"


# ---------------------------------------------------------------------------
# MD parsing
# ---------------------------------------------------------------------------

_FILENAME_PATTERN = re.compile(r"^SN(\d+)_(.+)$")


def parse_briefing(filepath: Path) -> dict | None:
    """Parse a single briefing MD file and return structured data."""
    # Extract subnet_id and name from filename
    stem = filepath.stem
    m = _FILENAME_PATTERN.match(stem)
    if not m:
        return None
    subnet_id = int(m.group(1))

    text = filepath.read_text(encoding="utf-8")

    # Subnet name from H1 heading
    name_match = re.search(r"^# (.+)$", text, re.MULTILINE)
    subnet_name = name_match.group(1).strip() if name_match else ""

    # Git project from **Git 项目** line
    git_match = re.search(r"\*\*Git 项目\*\*:\s*\[([^\]]+)\]\(([^)]+)\)", text)
    git_name = git_match.group(1) if git_match else ""
    git_url = git_match.group(2) if git_match else ""

    # Hardware requirements: everything after "## 硬件要求"
    hw_match = re.search(r"## 硬件要求\s*\n(.*)", text, re.DOTALL)
    hw_text = hw_match.group(1).strip() if hw_match else "无要求"
    has_hw = hw_text != "无要求"

    return {
        "subnet_id": subnet_id,
        "subnet_name": subnet_name,
        "git_name": git_name,
        "git_url": git_url,
        "has_hw": has_hw,
        "hw_text": hw_text,
    }


def load_all_briefings(input_dir: Path) -> list[dict]:
    """Load and parse all briefing MD files, sorted by subnet_id."""
    items: list[dict] = []
    for filepath in sorted(input_dir.glob("SN*.md")):
        result = parse_briefing(filepath)
        if result is not None:
            items.append(result)
    items.sort(key=lambda x: x["subnet_id"])
    return items


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_hw(hw_text: str) -> str:
    """Classify hardware requirement text into a category."""
    if hw_text == "无要求":
        return "无要求"
    upper = hw_text.upper()
    if re.search(r"GPU|CUDA|VRAM|NVIDIA|A100|H100|RTX|GRAVAL", upper):
        return "GPU必需"
    if re.search(r"CPU|CORE", upper):
        return "CPU为主"
    if re.search(r"RAM|MEMORY|STORAGE|DISK|SSD", upper):
        return "仅内存存储"
    return "其他硬件需求"


def summarize(items: list[dict]) -> dict:
    """Compute summary statistics from parsed briefing items."""
    total = len(items)
    with_hw = sum(1 for i in items if i["has_hw"])
    without_hw = total - with_hw

    # Classify each item
    for item in items:
        item["category"] = classify_hw(item["hw_text"])

    category_counts: dict[str, int] = {}
    for item in items:
        cat = item["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

    return {
        "total": total,
        "with_hw": with_hw,
        "without_hw": without_hw,
        "category_counts": category_counts,
    }


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def hw_summary(hw_text: str, max_len: int = 100) -> str:
    """Return a short summary of hardware requirements, stripped of markdown."""
    # Remove markdown formatting for table display
    cleaned = re.sub(r"[#*\[\]()]", "", hw_text)
    cleaned = re.sub(r"\n+", " ", cleaned).strip()
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len] + "..."
    return cleaned


def render_report(items: list[dict], stats: dict) -> str:
    """Render the full Chinese comprehensive report."""
    lines: list[str] = []

    # Title
    lines.append("# Bittensor 子网综合报告")
    lines.append("")

    # Overview
    lines.append("## 概览")
    lines.append("")
    lines.append(f"- **总子网数**: {stats['total']}")
    lines.append(f"- **有 GitHub 项目**: {stats['total']}")
    lines.append(f"- **有硬件要求**: {stats['with_hw']}")
    lines.append(f"- **无硬件要求**: {stats['without_hw']}")
    lines.append("")

    # Category statistics
    lines.append("## 硬件需求分类统计")
    lines.append("")
    lines.append("| 分类 | 数量 |")
    lines.append("|------|------|")
    for cat, count in sorted(stats["category_counts"].items(), key=lambda x: -x[1]):
        lines.append(f"| {cat} | {count} |")
    lines.append("")

    # Full overview table
    lines.append("## 子网总览表")
    lines.append("")
    lines.append("| 子网ID | 子网名称 | Git 项目 | 硬件要求 |")
    lines.append("|--------|----------|----------|----------|")
    for item in items:
        hw_label = "有" if item["has_hw"] else "无"
        git_link = f"[{item['git_name']}]({item['git_url']})" if item["git_name"] else "-"
        lines.append(f"| {item['subnet_id']} | {item['subnet_name']} | {git_link} | {hw_label} |")
    lines.append("")

    # Detailed table for items with hardware requirements
    hw_items = [i for i in items if i["has_hw"]]
    if hw_items:
        lines.append("## 有硬件要求的子网详表")
        lines.append("")
        lines.append("| 子网ID | 子网名称 | Git 项目 | 硬件要求摘要 | 分类 |")
        lines.append("|--------|----------|----------|-------------|------|")
        for item in hw_items:
            summary = hw_summary(item["hw_text"])
            git_link = f"[{item['git_name']}]({item['git_url']})" if item["git_name"] else "-"
            lines.append(f"| {item['subnet_id']} | {item['subnet_name']} | {git_link} | {summary} | {item['category']} |")
        lines.append("")

    # GPU-required subnets detail
    gpu_items = [i for i in items if i["category"] == "GPU必需"]
    if gpu_items:
        lines.append("## GPU 必需子网详情")
        lines.append("")
        for item in gpu_items:
            lines.append(f"### SN{item['subnet_id']} {item['subnet_name']}")
            lines.append("")
            git_link = f"[{item['git_name']}]({item['git_url']})" if item["git_name"] else "-"
            lines.append(f"- **Git 项目**: {git_link}")
            lines.append(f"- **分类**: {item['category']}")
            lines.append("")
            lines.append(item["hw_text"])
            lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Chinese comprehensive report from subnet briefing files."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Directory containing briefing MD files (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output report file path (default: {DEFAULT_OUTPUT})",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.input_dir.exists():
        print(f"[error] input directory not found: {args.input_dir}", file=sys.stderr)
        return 1

    items = load_all_briefings(args.input_dir)
    if not items:
        print("[error] no briefing files found", file=sys.stderr)
        return 1

    print(f"Loaded {len(items)} briefing files")

    stats = summarize(items)
    report = render_report(items, stats)

    args.output.write_text(report, encoding="utf-8")
    print(f"\nReport generated: {args.output}")
    print(f"  Total subnets: {stats['total']}")
    print(f"  With hardware requirements: {stats['with_hw']}")
    print(f"  Without hardware requirements: {stats['without_hw']}")
    print(f"  Categories: {stats['category_counts']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
