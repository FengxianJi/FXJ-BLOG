#!/usr/bin/env python3
"""Maintain bilingual blog posts. No network, API calls, or deployment."""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / '_posts'


def post_pairs() -> dict[str, dict[str, Path]]:
    pairs: dict[str, dict[str, Path]] = {}
    for post in POSTS_DIR.glob('*.md'):
        stem = post.name[:-len('.en.md')] if post.name.endswith('.en.md') else post.stem
        lang = 'en' if post.name.endswith('.en.md') else 'zh-CN'
        if lang in pairs.setdefault(stem, {}):
            raise RuntimeError(f'{stem}: duplicate {lang} post')
        pairs[stem][lang] = post
    if not pairs:
        raise RuntimeError('No blog posts found')
    for stem, versions in pairs.items():
        if set(versions) != {'zh-CN', 'en'}:
            raise RuntimeError(f'{stem}: expected a Chinese and English post pair')
    return pairs


def check() -> None:
    pairs = post_pairs()
    for stem, versions in pairs.items():
        parsed = {}
        for lang, post in versions.items():
            text = post.read_text(encoding='utf-8')
            parts = text.split('---', 2)
            if len(parts) != 3:
                raise RuntimeError(f'{post.name}: malformed front matter')
            front = parts[1]
            for field in (f'lang: {lang}', 'translation_url:'):
                if field not in front:
                    raise RuntimeError(f'{post.name}: missing {field}')
            if 'completed-experiment-results/' in text:
                raise RuntimeError(f'{post.name}: obsolete results link')
            expected = re.search(r'^figure_count: (\d+)$', front, re.MULTILINE)
            if expected and len(re.findall(r'!\[', text)) != int(expected.group(1)):
                raise RuntimeError(f'{post.name}: figure_count does not match article images')
            for asset in re.findall(r"'/assets/([^']+)'", text):
                if not (ROOT / 'assets' / asset).is_file():
                    raise RuntimeError(f'{post.name}: missing asset {asset}')
            parsed[lang] = (front, text)

        for lang, counterpart in (('zh-CN', 'en'), ('en', 'zh-CN')):
            front, _ = parsed[lang]
            other_front, _ = parsed[counterpart]
            link = re.search(r'^translation_url:\s*(\S+)$', front, re.MULTILINE)
            other_permalink = re.search(r'^permalink:\s*(\S+)$', other_front, re.MULTILINE)
            if not link or not other_permalink or link.group(1) != other_permalink.group(1):
                raise RuntimeError(f'{versions[lang].name}: translation_url does not match counterpart permalink')

    evidence_pair = pairs.get('2026-11-17-evidence-only-appendices')
    if evidence_pair:
        for post in evidence_pair.values():
            text = post.read_text(encoding='utf-8')
            if text.count('<div class="math-display">') != 4:
                raise RuntimeError(f'{post.name}: expected four display formulas')
    for svg in (ROOT / 'assets/evidencepatch-feedback').glob('*.svg'):
        ET.parse(svg)
    print(f'OK: {len(pairs)} bilingual post pairs, translations, assets, and SVG syntax')


def sync() -> None:
    target = ROOT.parent / 'EvidencePatch/blog'
    if not target.is_dir():
        raise RuntimeError('Workspace EvidencePatch/blog directory is required for sync')
    for post in POSTS_DIR.glob('*.md'):
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
