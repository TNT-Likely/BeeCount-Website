#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ZH_TEMPLATES = [
    '请说明文档中“{heading}”的要点。',
    '“{heading}”在 BeeCount 文档里怎么解释？',
    '我想了解“{heading}”，请基于文档回答。',
    '文档里关于“{heading}”的说明是什么？',
]

EN_TEMPLATES = [
    'What does the docs say about "{heading}"?',
    'Please summarize "{heading}" based on docs.',
    'How is "{heading}" explained in BeeCount docs?',
    'Give the key points of "{heading}" from docs.',
]

H1_RE = re.compile(r'^#\s+(.+)$', re.MULTILINE)


def first_heading(path: Path) -> str:
    text = path.read_text(encoding='utf-8', errors='ignore')
    m = H1_RE.search(text)
    if m:
        return m.group(1).strip()
    return path.stem


def to_url(path: Path, root: Path, locale: str) -> str:
    rel = path.relative_to(root).as_posix()
    slug = rel[:-3] if rel.endswith('.md') else rel
    if slug.endswith('/index'):
        slug = slug[:-6]
    prefix = '/docs/' if locale == 'zh' else '/en/docs/'
    return f'{prefix}{slug}'.replace('//', '/')


def build_cases(root: Path, locale: str, target: int, templates: list[str], case_prefix: str) -> list[dict]:
    files = sorted(root.rglob('*.md'))
    cases: list[dict] = []

    for idx in range(target):
        if not files:
            break
        file_path = files[idx % len(files)]
        heading = first_heading(file_path)
        query = templates[idx % len(templates)].format(heading=heading)
        cases.append(
            {
                'case_id': f'{case_prefix}-{idx + 1:03d}',
                'locale': locale,
                'query': query,
                'expected_urls': [to_url(file_path, root, locale)],
            }
        )
    return cases


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    zh_root = base.parent / 'docs'
    en_root = base.parent / 'i18n' / 'en' / 'docusaurus-plugin-content-docs' / 'current'

    cases = []
    cases.extend(build_cases(zh_root, 'zh', 80, ZH_TEMPLATES, 'zh'))
    cases.extend(build_cases(en_root, 'en', 40, EN_TEMPLATES, 'en'))

    payload = {
        'dataset_version': 'v1.0.0',
        'cases': cases,
    }

    output_path = base / 'eval' / 'datasets' / 'qa_gold.json'
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Generated {len(cases)} cases -> {output_path}')


if __name__ == '__main__':
    main()
