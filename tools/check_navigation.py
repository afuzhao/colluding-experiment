#!/usr/bin/env python3
"""Check local links in the maintained repository entry points; no network/inference."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    'README.md', 'CONTRIBUTING.md', 'studies/README.md', 'papers/README.md',
    'environments/README.md', 'old/README.md', 'docs/README.md',
    'docs/REPRODUCIBILITY.md', 'repo_guide/README.md', 'repo_guide/BRANCHES.md',
)

def main():
    failures, count = [], 0
    for name in PAGES:
        page = ROOT / name
        text = re.sub(r'```.*?```', '', page.read_text(), flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', text):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            count += 1
            destination = (page.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(ROOT) or not destination.exists():
                failures.append(f'{name}: {target}')
    if failures:
        print('\n'.join(failures))
        return 1
    print(f'Passed: {count} local links across {len(PAGES)} navigation pages. External URLs and anchors are not checked.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
