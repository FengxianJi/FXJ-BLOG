#!/usr/bin/env python3
"""Maintain the final bilingual article. No network, API calls, or deployment."""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = [ROOT / '_posts' / f'2026-11-17-evidence-only-appendices{suffix}.md'
         for suffix in ('', '.en')]


def check() -> None:
    actual = set((ROOT / '_posts').glob('*.md'))
    if actual != set(POSTS):
        raise RuntimeError('Expected only the final Chinese and English article')
    for post, lang in zip(POSTS, ('zh-CN', 'en')):
        text = post.read_text(encoding='utf-8')
        front = text.split('---', 2)[1]
        for field in (f'lang: {lang}', 'translation_url:', 'math: true'):
            if field not in front:
                raise RuntimeError(f'{post.name}: missing {field}')
        if 'completed-experiment-results/' in text:
            raise RuntimeError(f'{post.name}: obsolete results link')
        if text.count('<div class="math-display">') != 4:
            raise RuntimeError(f'{post.name}: expected four display formulas')
        if len(re.findall(r'!\[', text)) != 7:
            raise RuntimeError(f'{post.name}: expected seven article figures')
        for asset in re.findall(r"'/assets/([^']+)'", text):
            if not (ROOT / 'assets' / asset).is_file():
                raise RuntimeError(f'{post.name}: missing asset {asset}')
    for svg in (ROOT / 'assets/evidencepatch-feedback').glob('*.svg'):
        ET.parse(svg)
    print('OK: final bilingual posts, formulas, figure references, and SVG syntax')


def sync() -> None:
    target = ROOT.parent / 'EvidencePatch/blog'
    if not target.is_dir():
        raise RuntimeError('Workspace EvidencePatch/blog directory is required for sync')
    for post in POSTS:
        text = post.read_text(encoding='utf-8')
        front, body = text.split('---', 2)[1:]
        title = re.search(r'^title: "(.*)"$', front, re.MULTILINE).group(1)
        body = re.sub(r"\{\{ '/assets/([^']+)' \| relative_url \}\}",
                      r'../../FXJ-BLOG/assets/\1', body.lstrip())
        (target / post.name).write_text('# ' + title + '\n\n' + body, encoding='utf-8')
    print('Updated generated mirrors in EvidencePatch/blog')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('check', 'sync', 'figures'))
    args = parser.parse_args()
    if args.command == 'figures':
        subprocess.run([sys.executable, str(ROOT / 'scripts/build_feedback_figures.py')], check=True)
    elif args.command == 'sync':
        check()
        sync()
    else:
        check()


if __name__ == '__main__':
    main()
