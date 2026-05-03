#!/usr/bin/env python3
"""Scrape subnet GitHub information from Tao explorer pages.

The tao.app explorer is a Next.js SPA protected by Cloudflare.  Subnet data
(including ``github_repo``) is embedded as a JSON array in the RSC payload,
so we extract it directly from the single explorer page instead of crawling
each subnet page individually.

Requires: cloudscraper (bypasses Cloudflare challenge), requests
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

import cloudscraper


EXPLORER_URL = "https://www.tao.app/explorer"
BASE_URL = "https://www.tao.app"
DEFAULT_TIMEOUT = 30


@dataclass
class SubnetGithubInfo:
    subnet_id: int
    subnet_name: str | None
    subnet_url: str
    github_links: list[str]


def build_scraper() -> cloudscraper.CloudScraper:
    return cloudscraper.create_scraper()


def fetch_explorer_html(scraper: cloudscraper.CloudScraper, timeout: int) -> str:
    response = scraper.get(EXPLORER_URL, timeout=timeout)
    response.raise_for_status()
    return response.text


def extract_subnet_items(explorer_html: str) -> list[dict]:
    """Extract the subnetScreenerItems JSON array from the Next.js RSC payload."""
    marker = "subnetScreenerItems"
    idx = explorer_html.find(marker)
    if idx < 0:
        return []

    # Find the opening '[' after the marker
    start = explorer_html.find("[", idx)
    if start < 0:
        return []

    # Match brackets to find the end of the JSON array
    depth = 0
    end = start
    for i in range(start, min(start + 1_000_000, len(explorer_html))):
        if explorer_html[i] == "[":
            depth += 1
        elif explorer_html[i] == "]":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    raw = explorer_html[start:end]
    # Next.js RSC payloads may have escaped quotes
    raw = raw.replace('\\"', '"')

    try:
        items = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: more aggressive unescaping
        raw = raw.replace("\\\\", "\\")
        items = json.loads(raw)

    return items


def build_subnet_infos(raw_items: list[dict]) -> list[SubnetGithubInfo]:
    """Convert raw JSON items into SubnetGithubInfo dataclasses."""
    results: list[SubnetGithubInfo] = []
    for item in raw_items:
        netuid = item.get("netuid", 0)
        name = item.get("subnet_name") or None
        github_repo = item.get("github_repo", "")
        github_links = [github_repo] if github_repo else []

        results.append(
            SubnetGithubInfo(
                subnet_id=netuid,
                subnet_name=name,
                subnet_url=f"{BASE_URL}/subnets/{netuid}",
                github_links=github_links,
            )
        )
    return results


def write_json(output_path: Path, items: list[SubnetGithubInfo]) -> None:
    output_path.write_text(
        json.dumps([asdict(item) for item in items], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_csv(output_path: Path, items: list[SubnetGithubInfo]) -> None:
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["subnet_id", "subnet_name", "subnet_url", "github_links"],
        )
        writer.writeheader()
        for item in items:
            writer.writerow(
                {
                    "subnet_id": item.subnet_id,
                    "subnet_name": item.subnet_name or "",
                    "subnet_url": item.subnet_url,
                    "github_links": " | ".join(item.github_links),
                }
            )


def _safe_print(text: str) -> None:
    """Print with fallback for Windows console encoding issues."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace characters that can't be encoded in the console's encoding
        encoded = text.encode(sys.stdout.encoding or "utf-8", errors="replace")
        print(encoded.decode(sys.stdout.encoding or "utf-8", errors="replace"))


def print_summary(items: list[SubnetGithubInfo]) -> None:
    for item in items:
        github_text = ", ".join(item.github_links) if item.github_links else "<none>"
        subnet_name = item.subnet_name or "<unknown>"
        _safe_print(f"SN {item.subnet_id:>3} | {subnet_name} | {github_text}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract subnet GitHub links from the Tao explorer page."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Only output the first N subnets. 0 means all (default).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="HTTP timeout in seconds.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output file path. Supports .json and .csv.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    scraper = build_scraper()

    try:
        explorer_html = fetch_explorer_html(scraper, args.timeout)
    except Exception as exc:
        print(f"[error] explorer fetch failed: {exc}", file=sys.stderr)
        return 1

    raw_items = extract_subnet_items(explorer_html)
    if not raw_items:
        print("[error] no subnet data found in explorer page", file=sys.stderr)
        return 1

    items = build_subnet_infos(raw_items)
    if args.limit and args.limit > 0:
        items = items[: args.limit]

    print_summary(items)

    print(f"\nTotal: {len(items)} subnets, "
          f"{sum(1 for i in items if i.github_links)} with GitHub repos")

    if args.output is not None:
        suffix = args.output.suffix.lower()
        if suffix == ".json":
            write_json(args.output, items)
        elif suffix == ".csv":
            write_csv(args.output, items)
        else:
            print("[error] output path must end with .json or .csv", file=sys.stderr)
            return 1
        print(f"Output written to {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
