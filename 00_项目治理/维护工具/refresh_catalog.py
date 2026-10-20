# -*- coding: utf-8 -*-
"""Refresh current file navigation; does not assign scientific ownership."""
from pathlib import Path
import json
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / '00_项目治理/资料索引'
# 本仓库自身带 .git（openuft 同时被外层 my_lib 跟踪），裸 rglob 会把仓库记账对象
# 当成资料索引进正本索引，一次就写入数百条 .git/... 行（2026-09-23 / 2026-09-24 两次事故）。
# 名字判据按目录段逐层做、大小写不敏感，好让嵌套仓库与子模块的 .git 一并排除。
# 前端工程（openuft/code）的依赖与构建产物同理：node_modules / dist / .vite 不是本库资料，
# 索引它们会一次写入数千条第三方路径并让 verify 的断链检查被第三方 md 淹没（2026-10-20）。
IGNORE_DIRS = {'__pycache__', '.git', 'node_modules', 'dist', '.vite', '.cache'}


def is_indexable(p):
    ancestors = tuple(x.lower() for x in p.relative_to(ROOT).parts[:-1])
    return p.is_file() and not (set(ancestors) & IGNORE_DIRS)


def render(files):
    entries = [{'path': p.relative_to(ROOT).as_posix(), 'section': p.relative_to(ROOT).parts[0]} for p in files]
    man_text = json.dumps({'purpose': 'Current paths only; not scientific evidence or ownership certification',
                           'files': entries}, ensure_ascii=False, indent=2) + '\n'
    body = '# 全量文件索引\n\n按实际存放位置生成。归属待审的历史资料不因被索引而获得证据认可。\n\n'
    section = None
    for p in files:
        current = p.relative_to(ROOT).parts[0]
        if current != section:
            body += '\n## ' + current + '\n\n'
            section = current
        target = os.path.relpath(p, CATALOG).replace('\\', '/')
        # 链接目标里若有 ( ) 空格 #，Markdown 行内链接会被提前截断，verify.py 的
        # 断链检查就会报假红（它按 [^\s)]+ 取目标）。这里只转义这四类字符，
        # 中文与 / 保持原样以留住可读性；verify.py 一侧有 unquote，能原样还原。
        target = (target.replace('(', '%28').replace(')', '%29')
                        .replace(' ', '%20').replace('#', '%23'))
        body += '- [' + p.relative_to(ROOT).as_posix() + '](' + target + ')\n'
    return man_text, body, entries


def main(argv=()):
    files = sorted(p for p in ROOT.rglob('*') if is_indexable(p))
    man_text, body, entries = render(files)
    cat_path = CATALOG / 'material_catalog.md'
    man_path = CATALOG / 'structure_manifest.json'
    if '--check' in argv:
        # 只读对账：并发会话里别人正在写这两份正本时，用这一档量差值而不是落盘。
        # 整体重生成会把他人更大的索引回退（attack21/attack24 记过这条红线）。
        old_body = cat_path.read_bytes().decode('utf-8') if cat_path.exists() else ''
        old_man = json.loads(man_path.read_bytes().decode('utf-8'))['files'] if man_path.exists() else []
        old_rows = re.findall(r'(?m)^- \[([^\]]*)\]\(', old_body)
        malformed = re.findall(r'(?m)^- \[\[', old_body)
        now = set(e['path'] for e in entries)
        print('disk indexable files: %d' % len(entries))
        print('catalog rows on disk: %d (malformed "- [[": %d)' % (len(old_rows), len(malformed)))
        print('manifest entries on disk: %d' % len(old_man))
        print('not yet indexed: %d' % len(now - set(old_rows)))
        print('stale rows (file gone): %d' % len(set(old_rows) - now))
        print('git rows on disk: %d (must be 0)' % len([r for r in old_rows + [e['path'] for e in old_man]
                                                        if '.git' in [x.lower() for x in Path(r).parts]]))
        print('CHECK ONLY, nothing written')
        return 0
    man_path.write_text(man_text, encoding='utf-8')
    cat_path.write_text(body, encoding='utf-8')
    print('Indexed {} files'.format(len(files)))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
