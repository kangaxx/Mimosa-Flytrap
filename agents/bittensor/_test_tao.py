#!/usr/bin/env python3
"""Quick test to extract subnet data from tao.app."""
import cloudscraper
import re
import json

scraper = cloudscraper.create_scraper()
r = scraper.get("https://www.tao.app/explorer", timeout=30)

# Find the start of subnetScreenerItems array
marker = 'subnetScreenerItems'
idx = r.text.find(marker)
if idx < 0:
    print("subnetScreenerItems not found")
    exit(1)

# Extract from marker position - find the JSON array
# Walk forward to find the opening bracket
start = r.text.find('[', idx)
# Count brackets to find matching close
depth = 0
end = start
for i in range(start, min(start + 500000, len(r.text))):
    if r.text[i] == '[':
        depth += 1
    elif r.text[i] == ']':
        depth -= 1
        if depth == 0:
            end = i + 1
            break

raw = r.text[start:end]
print(f"Extracted JSON array, length: {len(raw)}")

# The data is in Next.js RSC format - strings may be escaped
# Try parsing directly first
try:
    items = json.loads(raw)
    print(f"Parsed directly: {len(items)} subnets")
except json.JSONDecodeError as e:
    print(f"Direct parse failed: {e}")
    # Try unescaping
    try:
        unescaped = raw.replace('\\"', '"').replace('\\\\', '\\')
        items = json.loads(unescaped)
        print(f"Parsed after unescape: {len(items)} subnets")
    except json.JSONDecodeError as e2:
        print(f"Unescaped parse also failed: {e2}")
        # Print a sample
        print("Sample:", raw[:500])
        exit(1)

# Show results
for item in items[:5]:
    netuid = item.get('netuid', '?')
    name = item.get('subnet_name', '?')
    github = item.get('github_repo', '<none>')
    print(f"  SN {netuid:>3} | {name} | github: {github}")

with_github = [i for i in items if i.get('github_repo')]
print(f"\nSubnets with github_repo: {len(with_github)} / {len(items)}")
for item in with_github[:10]:
    print(f"  SN {item['netuid']:>3} | {item['subnet_name']} | {item['github_repo']}")
