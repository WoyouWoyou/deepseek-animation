"""Build the release zip. Python standard library only.

Run from the skill root:  python scripts/package.py [--out dist]

If a 风格提示词/ directory exists at the skill root it is treated as a bundled
library: the index is rebuilt from it, and the zip includes the originals.
Without it the zip ships the index snapshot only. Either way the archive is
named deepseek-animation-<version>-<library_mode>.zip so the two are not mixed up.
"""
import argparse
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style_library as lib

SKILL_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = SKILL_ROOT / 'VERSION'
EXCLUDE_DIRS = {'.git', '__pycache__', 'dist', 'node_modules', '.venv', '.pytest_cache'}
EXCLUDE_FILES = {'.DS_Store', 'Thumbs.db'}
EXCLUDE_SUFFIX = {'.pyc', '.pyo'}


def version():
    if VERSION_FILE.is_file():
        return VERSION_FILE.read_text(encoding='utf-8').strip()
    return '0.0.0'


def walk():
    for path in sorted(SKILL_ROOT.rglob('*')):
        rel = path.relative_to(SKILL_ROOT)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        if path.is_dir():
            continue
        if path.name in EXCLUDE_FILES or path.suffix in EXCLUDE_SUFFIX:
            continue
        yield path, rel


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', default='dist')
    ap.add_argument('--no-build', action='store_true', help='keep the existing index as is')
    a = ap.parse_args()

    ver = version()
    prompt_dir = SKILL_ROOT / '风格提示词'
    bundled = prompt_dir.is_dir()

    if bundled:
        if a.no_build:
            print('skip index rebuild (--no-build)')
        else:
            result = lib.index_library(str(SKILL_ROOT))
            index_path = SKILL_ROOT / 'adapters' / 'style-index.json'
            index_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print('index rebuilt: %d prompts, version %s' % (result['prompt_count'], result['library_version'][:12]))
        mode = 'bundled'
    else:
        mode = 'index-only'
        print('no 风格提示词/ at skill root: packaging index-only build')

    out_dir = (SKILL_ROOT / a.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    name = 'deepseek-animation-%s-%s.zip' % (ver, mode)
    target = out_dir / name
    prefix = 'deepseek-animation-%s/' % ver

    count = 0
    total = 0
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path, rel in walk():
            if target == path:
                continue
            arc = prefix + rel.as_posix()
            if path.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp'):
                zf.write(path, arc, compress_type=zipfile.ZIP_STORED)
            else:
                zf.write(path, arc)
            count += 1
            total += path.stat().st_size

    print('%s  %d files  %.2f MB -> %.2f MB' % (name, count, total / 1e6, target.stat().st_size / 1e6))
    print(target)


if __name__ == '__main__':
    main()
