# -*- coding: utf-8 -*-
"""Contract tests for refresh_catalog.py in isolated temporary roots.

红线：本文件只跑临时根，绝不写 openuft 的真实 material_catalog.md / structure_manifest.json
（裸 rglob 会把 openuft/.git 的对象索引进正本，2026-09-23 与 09-24 各炸过一次）。
"""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SRC = (Path(__file__).resolve().parent / 'refresh_catalog.py').read_bytes()
GOV = '00_项目治理/资料索引'


def build_root(with_git=True):
    temp = tempfile.TemporaryDirectory(prefix='openuft_refresh_')
    root = Path(temp.name).resolve()
    tool = root / '00_项目治理' / '维护工具'
    tool.mkdir(parents=True)
    (root / GOV).mkdir(parents=True)
    payload = {
        '01_独立体系/s01/README.md': '# s01\n',
        '01_独立体系/s01/claims.csv': 'id\n',
        '04_公共成果/带 空格(括号)#号.md': 'x',
        '02_跨体系研究/nested/leaf.py': 'x',
    }
    # 编译产物：修复前后都被排除，是「过滤器没把别的东西一起杀掉」的对照
    noise = {'01_独立体系/s01/__pycache__/pynoise.pyc': 'x'}
    gitfiles = {
        '.git/HEAD': 'ref: refs/heads/main\n',
        '.git/objects/pack/pack-abc.idx': 'bin',
        '.git/hooks/pre-commit': '#!/bin/sh\n',
        '01_独立体系/s01/.git/HEAD': 'ref: refs/heads/nested\n',
        '02_跨体系研究/nested/.GIT/CONFIG': 'bin',
    }
    for rel in list(payload) + list(noise) + (list(gitfiles) if with_git else []):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload.get(rel) or gitfiles.get(rel) or noise.get(rel) or '', encoding='utf-8')
    # 真实仓库里这两份正本索引本来就在盘上，工具会把它们（和它自己）一起索引；
    # 夹具若缺一开局就存在，第一次运行就会比第二次少 3 行，测的就不是幂等而是首建。
    (root / GOV / 'material_catalog.md').write_text('# 全量文件索引\n', encoding='utf-8')
    (root / GOV / 'structure_manifest.json').write_text('{"files": []}\n', encoding='utf-8')
    return temp, root, sorted(payload), sorted(gitfiles), sorted(noise)


SELF_ROWS = sorted(['00_项目治理/维护工具/refresh_catalog.py',
                    GOV + '/material_catalog.md', GOV + '/structure_manifest.json'])


def run_script(root, source=None, args=()):
    tool = root / '00_项目治理' / '维护工具' / 'refresh_catalog.py'
    tool.write_bytes(source if source is not None else SRC)
    proc = subprocess.run([sys.executable, str(tool)] + list(args), cwd=str(root),
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          encoding='utf-8', errors='replace')
    assert proc.returncode == 0, 'script failed: %s' % proc.stdout
    cat = (root / GOV / 'material_catalog.md').read_bytes().decode('utf-8')
    man = json.loads((root / GOV / 'structure_manifest.json').read_bytes().decode('utf-8'))
    return cat, [e['path'] for e in man['files']], proc.stdout


def git_rows(paths):
    return [p for p in paths if '.git' in [x.lower() for x in Path(p).parts]]


def unquote(target):
    for a, b in (('%20', ' '), ('%28', '('), ('%29', ')'), ('%23', '#')):
        target = target.replace(a, b)
    return target


class RefreshCatalogContract(unittest.TestCase):
    def setUp(self):
        self.temp, self.root, self.payload, self.gitfiles, self.noise = build_root()
        self.addCleanup(self.temp.cleanup)

    def test_git_objects_never_enter_the_index(self):
        cat, man, _ = run_script(self.root)
        self.assertEqual([], git_rows(man), 'manifest 泄漏了仓库记账行')
        self.assertEqual([], git_rows([l[3:l.index('](')] for l in cat.splitlines() if l.startswith('- [')]),
                         'catalog 泄漏了仓库记账行')
        self.assertEqual([], [x for x in man if '__pycache__' in x], '编译产物泄漏')
        self.assertEqual(len(self.payload) + len(SELF_ROWS), len(man),
                         'manifest 条数应为夹具真文件 + 工具自身两份产物')

    def test_every_real_file_is_indexed_in_both_surfaces(self):
        cat, man, _ = run_script(self.root)
        want = sorted(self.payload + SELF_ROWS)
        self.assertEqual(want, sorted(man), 'manifest 与夹具真文件集合不符')
        rows = [l[3:l.index('](')] for l in cat.splitlines() if l.startswith('- [')]
        self.assertEqual(want, sorted(rows), 'catalog 行与夹具真文件集合不符')
        self.assertEqual(len(man), len(rows), '两份索引面的条数必须相等')

    def test_link_targets_resolve_from_the_index_directory(self):
        cat, _, _ = run_script(self.root)
        broken = []
        for line in cat.splitlines():
            if line.startswith('- [') and '](' in line:
                target = line[line.index('](') + 2:line.rindex(')')]
                if not (self.root / GOV / unquote(target)).exists():
                    broken.append(target)
        self.assertEqual([], broken, '断链目标 %d 条' % len(broken))

    def test_two_runs_are_byte_identical(self):
        cat1, _, _ = run_script(self.root)
        man1 = (self.root / GOV / 'structure_manifest.json').read_bytes()
        cat2, _, _ = run_script(self.root)
        man2 = (self.root / GOV / 'structure_manifest.json').read_bytes()
        self.assertEqual(cat1, cat2)
        self.assertEqual(man1, man2)

    def test_check_mode_is_read_only_and_prices_the_delta(self):
        """--check 必须只读，且把「缺几行 / 几行已失效」量出来而不是替人写盘。"""
        run_script(self.root)
        stale = self.root / '02_跨体系研究/nested/gone.py'
        stale.write_text('x', encoding='utf-8')
        run_script(self.root)                       # 正本此刻含有它，随后删盘 ⇒ 制造陈旧行
        stale.unlink()
        (self.root / '01_独立体系/s01/fresh.md').write_text('x', encoding='utf-8')  # 未索引
        before = {f: (self.root / GOV / f).read_bytes()
                  for f in ('material_catalog.md', 'structure_manifest.json')}
        _, _, out = run_script(self.root, args=('--check',))
        for key, want in (('not yet indexed', 1), ('stale rows (file gone)', 1), ('git rows on disk', 0)):
            got = [l for l in out.splitlines() if key in l]
            self.assertEqual(1, len(got), '%s 那一格没被打印：%s' % (key, out))
            self.assertEqual(want, int(re.search(r':\s*(-?\d+)', got[0].split(key)[1]).group(1)),
                             '%s 读数应由夹具现推为 %d：%r' % (key, want, got[0]))
        mal = [l for l in out.splitlines() if 'malformed' in l]
        self.assertEqual(1, len(mal), '畸形行那一格没被打印：%s' % out)
        self.assertEqual(0, int(re.findall(r':\s*(\d+)', mal[0])[-1]), '畸形行数：%r' % mal[0])
        self.assertIn('CHECK ONLY, nothing written', out)
        for f, blob in before.items():
            self.assertEqual(blob, (self.root / GOV / f).read_bytes(), '--check 动了 %s' % f)

    def test_mutant_old_filter_leaks_git_rows(self):
        """把过滤换回修复前的形状，.git 必须重新进索引 —— 否则上面几格是空转的针。"""
        old = SRC.replace("    files = sorted(p for p in ROOT.rglob('*') if is_indexable(p))".encode(),
                          "    files = sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts)".encode())
        self.assertNotEqual(SRC, old, '变异锚点未命中，变异体等于没变异')
        temp, root, _, _, _ = build_root()
        self.addCleanup(temp.cleanup)
        cat, man, _ = run_script(root, source=old)
        leaked = git_rows(man)
        self.assertEqual(len(self.gitfiles), len(leaked),
                         '旧过滤应把夹具里 %d 个记账文件全索引进来，实测 %d' % (len(self.gitfiles), len(leaked)))
        self.assertEqual(sorted(self.gitfiles), sorted(leaked), '泄漏集合与夹具 .git 名单不一致')
        cat_leak = git_rows([l[3:l.index('](')] for l in cat.splitlines() if l.startswith('- [')])
        self.assertEqual(sorted(self.gitfiles), sorted(cat_leak), 'catalog 侧旧过滤没复现同样的污染')


if __name__ == '__main__':
    unittest.main(verbosity=2)
