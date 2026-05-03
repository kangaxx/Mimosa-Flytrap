#!/usr/bin/env python3
"""Generate briefing MD files for each Bittensor subnet's GitHub repository.

Reads result.csv (produced by scrape_tao_subnet_githubs.py), visits each
GitHub repo, fetches the README, extracts hardware requirements, and writes
a per-subnet markdown briefing.
"""

from __future__ import annotations

import argparse
import base64
import csv
import re
import sys
import time
from pathlib import Path

import cloudscraper


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = SCRIPT_DIR / "result.csv"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "briefings"
DEFAULT_TIMEOUT = 20
DEFAULT_DELAY = 1.0


# ---------------------------------------------------------------------------
# CSV reading
# ---------------------------------------------------------------------------

def load_subnet_csv(csv_path: Path) -> list[dict]:
    """Read result.csv and return rows that have github_links."""
    rows: list[dict] = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            github = row.get("github_links", "").strip()
            if not github:
                continue
            rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# GitHub URL normalization
# ---------------------------------------------------------------------------

_REPO_PATTERN = re.compile(
    r"https://github\.com/([^/]+)/([^/]+?)(?:\.git)?(?:/.*)?$"
)


def normalize_github_url(url: str) -> tuple[str, str] | None:
    """Extract (owner, repo) from a GitHub URL.

    Returns None for non-repo URLs such as github.com/orgs/...
    """
    url = url.strip().rstrip("/")
    m = _REPO_PATTERN.match(url)
    if m:
        return m.group(1), m.group(2)
    return None


# ---------------------------------------------------------------------------
# README fetching
# ---------------------------------------------------------------------------

_README_NAMES = ["README.md", "README.rst", "README.txt", "README"]


def fetch_readme_api(
    session: cloudscraper.CloudScraper, owner: str, repo: str, timeout: int
) -> str | None:
    """Fetch README via GitHub REST API (returns decoded text or None)."""
    api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    try:
        r = session.get(api_url, timeout=timeout)
    except Exception:
        return None
    if r.status_code == 200:
        try:
            data = r.json()
            return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
        except (KeyError, ValueError):
            return None
    return None


def fetch_readme_raw(
    session: cloudscraper.CloudScraper, owner: str, repo: str, timeout: int
) -> str | None:
    """Fetch README via raw.githubusercontent.com (fallback)."""
    for branch in ("main", "master"):
        for name in _README_NAMES:
            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{name}"
            try:
                r = session.get(raw_url, timeout=timeout)
            except Exception:
                continue
            if r.status_code == 200:
                return r.text
    return None


def fetch_readme(
    session: cloudscraper.CloudScraper,
    owner: str,
    repo: str,
    timeout: int,
    no_api: bool = False,
) -> str | None:
    """Fetch README content, trying API first then raw URLs."""
    if not no_api:
        text = fetch_readme_api(session, owner, repo, timeout)
        if text is not None:
            return text
    return fetch_readme_raw(session, owner, repo, timeout)


# ---------------------------------------------------------------------------
# Hardware requirements extraction
# ---------------------------------------------------------------------------

_HW_KEYWORDS = re.compile(
    r"(?i)(?:GPU|CPU|RAM|VRAM|memory|storage|disk|NVIDIA|CUDA|hardware|"
    r"requirements?|specs?|minimum|recommended|TDP|cores?)"
)

_HW_HEADING = re.compile(
    r"(?i)^#{1,4}\s+.*(?:hardware|requirements?|prerequisites?|setup|install)"
)


def extract_hardware_requirements(readme_text: str) -> str:
    """Extract hardware requirement sections from README text.

    Looks for headings containing 'hardware'/'requirements' etc. and captures
    their content until the next heading.  Also collects individual lines that
    mention hardware keywords.
    """
    lines = readme_text.split("\n")
    sections: list[str] = []
    in_hw_section = False
    current_lines: list[str] = []

    for line in lines:
        is_heading = bool(re.match(r"#{1,4}\s+", line))

        if in_hw_section:
            if is_heading:
                # End of HW section
                sections.append("\n".join(current_lines).strip())
                current_lines = []
                in_hw_section = False
                # Check if new heading is also HW-related
                if _HW_HEADING.match(line):
                    in_hw_section = True
                    current_lines.append(line)
            else:
                current_lines.append(line)
        else:
            if is_heading and _HW_HEADING.match(line):
                in_hw_section = True
                current_lines = [line]
            elif not is_heading and _HW_KEYWORDS.search(line):
                # Standalone line with HW keyword (not inside a HW heading section)
                sections.append(line.strip())

    if current_lines:
        sections.append("\n".join(current_lines).strip())

    if not sections:
        return "无要求"

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for s in sections:
        if s not in seen:
            seen.add(s)
            unique.append(s)

    result = "\n\n".join(unique)
    # Truncate if excessively long
    if len(result) > 2000:
        result = result[:2000] + "\n...(truncated)"
    return result


# ---------------------------------------------------------------------------
# MD briefing generation
# ---------------------------------------------------------------------------

def sanitize_filename(name: str) -> str:
    """Replace characters unsafe for filenames with '_'."""
    return re.sub(r'[\\/:*?"<>|\s#+]', "_", name)


def render_briefing_md(
    subnet_name: str,
    owner: str,
    repo: str,
    hw_requirements: str,
) -> str:
    """Render the briefing markdown content."""
    return (
        f"# {subnet_name}\n\n"
        f"- **子网名称**: {subnet_name}\n"
        f"- **Git 项目**: [{owner}/{repo}](https://github.com/{owner}/{repo})\n\n"
        f"## 硬件要求\n\n{hw_requirements}\n"
    )


def write_briefing(
    output_dir: Path,
    subnet_id: int,
    subnet_name: str,
    owner: str,
    repo: str,
    hw_requirements: str,
) -> Path:
    """Write a single briefing MD file and return its path."""
    safe_name = sanitize_filename(subnet_name)
    filename = f"SN{subnet_id}_{safe_name}.md"
    filepath = output_dir / filename
    content = render_briefing_md(subnet_name, owner, repo, hw_requirements)
    filepath.write_text(content, encoding="utf-8")
    return filepath


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate briefing MD files from subnet GitHub repos."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Path to result.csv (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for briefing MD files (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="HTTP timeout in seconds.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
        help="Delay in seconds between requests to avoid rate limiting.",
    )
    parser.add_argument(
        "--no-api",
        action="store_true",
        help="Skip GitHub API; fetch README via raw URLs only.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Only process the first N subnets. 0 means all (default).",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip subnets that already have a briefing file.",
    )
    return parser.parse_args()


def _safe_print(text: str, **kwargs) -> None:
    """Print with fallback for Windows console encoding issues."""
    try:
        print(text, **kwargs)
    except UnicodeEncodeError:
        encoded = text.encode(sys.stdout.encoding or "utf-8", errors="replace")
        print(encoded.decode(sys.stdout.encoding or "utf-8", errors="replace"), **kwargs)


def main() -> int:
    args = parse_args()

    if not args.input.exists():
        print(f"[error] input file not found: {args.input}", file=sys.stderr)
        return 1

    rows = load_subnet_csv(args.input)
    if args.limit and args.limit > 0:
        rows = rows[: args.limit]
    print(f"Loaded {len(rows)} subnets with GitHub links from {args.input}")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    session = cloudscraper.create_scraper()
    session.headers.update({
        "Accept": "application/vnd.github.v3+json",
    })

    success = 0
    skipped = 0
    failed = 0

    for i, row in enumerate(rows):
        subnet_id = row.get("subnet_id", "?")
        subnet_name = row.get("subnet_name", "unknown")
        github_url = row.get("github_links", "").strip()

        # Multiple URLs may be pipe-separated
        urls = [u.strip() for u in github_url.split("|") if u.strip()]
        owner_repo = None
        for url in urls:
            owner_repo = normalize_github_url(url)
            if owner_repo:
                break

        if not owner_repo:
            _safe_print(f"  SN {subnet_id:>3} | {subnet_name} | SKIP: not a repo URL ({github_url})")
            skipped += 1
            continue

        owner, repo = owner_repo
        _safe_print(f"  SN {subnet_id:>3} | {subnet_name} | {owner}/{repo} ...", end=" ")

        # Skip if briefing already exists
        if args.skip_existing:
            safe_name = sanitize_filename(subnet_name)
            existing = args.output_dir / f"SN{subnet_id}_{safe_name}.md"
            if existing.exists():
                _safe_print("SKIP (exists)")
                skipped += 1
                continue

        readme_text = fetch_readme(session, owner, repo, args.timeout, args.no_api)
        if readme_text is None:
            _safe_print("NO README")
            hw = "无要求"
        else:
            hw = extract_hardware_requirements(readme_text)
            _safe_print("OK" if hw != "无要求" else "OK (no hw info)")

        filepath = write_briefing(
            args.output_dir, int(subnet_id), subnet_name, owner, repo, hw
        )
        success += 1

        if args.delay > 0 and i < len(rows) - 1:
            time.sleep(args.delay)

    print(f"\nDone: {success} briefings, {skipped} skipped, {failed} failed")
    print(f"Output: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
