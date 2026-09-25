#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 `my_lib/ufthub/` 里的统一场论来源材料，整理进 openuft。

与 [`ingest_root_material.py`](ingest_root_material.py) 同构：只做**来源分箱**
（按材料自身的主题域分箱），逐件归属留给人工，登记为 `待归属`。

差异（为什么不能直接复用上一个工具）：
  1. 默认**复制**而非移动。ufthub 是仍在使用的来料中枢，就地搬空后若中途失败会
     同时丢掉两侧可追溯性；复制可保证「源不动、目标可删」。`--move` 才移动。
  2. 分箱粒度是**条目**不是根目录：ufthub 按「格式」分（md/、html/、zip/），
     同一个主题被拆散在三个目录里，直接搬会保留无意义的结构。
  3. 顶层三目录（md/html/zip）不作为分箱依据，只作为来源标记记入清单。

用法：
    python -B 00_项目治理/维护工具/ingest_ufthub_material.py            # 预演，只出清单
    python -B 00_项目治理/维护工具/ingest_ufthub_material.py --go       # 实际写入
    python -B 00_项目治理/维护工具/ingest_ufthub_material.py --go --move
    python -B 00_项目治理/维护工具/ingest_ufthub_material.py --restore  # 删除已写入的副本

写入位置：`90_历史归档/来源语料_ufthub_20260925/`，迁移记录 `90_历史归档/迁移记录/20260925_ufthub归集/`。
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------- 路径

TOOL_DIR = Path(__file__).resolve().parent
OPENUFT = TOOL_DIR.parent.parent                     # openuft/
REPO = OPENUFT.parent                                # my_lib/
SOURCE = REPO / 'ufthub'
DEST_ROOT = OPENUFT / '90_历史归档' / '来源语料_ufthub_20260925'
RECORD = OPENUFT / '90_历史归档' / '迁移记录' / '20260925_ufthub归集'
MANIFEST = RECORD / 'manifest.json'

# 遍历时剔除：可再生 / 成环 / 非语料
PRUNE = {'__pycache__', '.git', '.history', 'node_modules', '.venv', '.ipynb_checkpoints'}

# ---------------------------------------------------------------- 分箱规则
# 规则一律写成「来源分箱」，不写成体系归属。attribution 列只给"线索"，须人工核验。
# 顺序敏感：先命中先归。

BINS = [
    ('00_OpenUFT镜像快照', re.compile(r'openuft|^claims\.csv$', re.I),
     'openuft 自身的历史镜像（旧布局：00_统一场方程/ + 根级 08/09/11/12）。'
     '**不得当作来源证据重复引用**，只用于比对现行仓库缺了什么'),

    ('01_统一场论全书_版本序列', re.compile(r'统一场论全书'),
     '《统一场论》成书稿的 v1–v10 递进版本序列，线索：与 书籍/ 成书线同名'),

    ('02_GAQ与GMUFT几何统一场', re.compile(r'GAQ|GMUFT|GUFT'),
     '线索：与 S03/S07/S08/S09 GAQ 系列及几何流形路线同名'),

    ('03_螺旋与曲率挠率体系', re.compile(
        r'光速螺旋|LSSUFT|螺旋|曲率|挠率|κ\^?2|τ\^?2|Gε0|G与ε₀|引电曲率|darboux|'
        r'动量|统一场论最简求导|统一场论正确终版|统一场论总结|最简求导|精算|'
        r'四力|^S02|闭环方程组'),
     '线索：与 S01 螺旋三重奏 / S02 空间光速螺旋统一力 主题域相邻'),

    ('04_TUFT拓扑统一场论', re.compile(r'TUFT', re.I),
     '线索：与 S14 挠率统一场论 TUFT 同名'),

    ('05_数论_哥德巴赫与孪生素数', re.compile(
        r'哥德巴赫|Goldbach|孪生素数|素数|套娃分形筛|解析数论|循环论证', re.I),
     '**与统一场论不同主题域**：解析数论证明稿。线索：仓库内暂无对应体系，'
     '若立项应走 01_独立体系/新体系模板'),

    ('06_全域数学与知识生成体系', re.compile(
        r'全域数学|全域双向分形|全域统一场论|全域统一场|全域螺旋|全域拼合|'
        r'全维宇宙归一化|知识大典|omni_unified|分形宇宙|全维分形|'
        r'自动公式生成器|超宇宙全维度|完整理论文档|数据附录|宇宙光子|双向分形'),
     '线索：全域数学 / 分形知识工程，与 S13 全域双向分形统一场论同名分支'),

    ('07_常数本源与真空涡旋', re.compile(
        r'统一常量|0·1·∞|01∞|超维|百阶|真空统一常数|真空涡旋|多余G|'
        r'精细结构常数|K=3\.147'),
     '线索：常数本源与真空涡旋路线，与 S02/S12 常数议题相邻'),

    ('08_宇宙文明与工程平台包', re.compile(
        r'宇宙文明|ent-platform|算子统一系统|Win7|Playwright|佛山政数局|'
        r'magnetic_field|流程包合集|全选'),
     '线索：工程/平台交付包，部分与统一场论无关（如 RPA 流程包、政务中台对接）'),

    ('09_可视化与网页产出', re.compile(r'\.(html?|svg|png)$', re.I),
     '网页 / 可视化 / 报告页，线索：多为某一路线的前端展示或验证页'),
]

DEFAULT_BIN = '10_未分类与杂项'
DEFAULT_CLUE = '待归属：主题域未识别，须人工读材料后判定'

BIN_DESC = {
    '00_OpenUFT镜像快照': 'openuft 自身镜像（旧布局），仅用于比对缺漏',
    '01_统一场论全书_版本序列': '《统一场论》成书稿 v1–v10 递进版本',
    '02_GAQ与GMUFT几何统一场': 'GAQ-UFT 与几何流形统一场论（GMUFT/GUFT）',
    '03_螺旋与曲率挠率体系': '空间光速螺旋 / 曲率-挠率 / 电磁引力统一主线',
    '04_TUFT拓扑统一场论': 'TUFT 拓扑统一场论完整包',
    '05_数论_哥德巴赫与孪生素数': '解析数论证明稿（哥德巴赫 / 孪生素数 / 套娃分形筛）',
    '06_全域数学与知识生成体系': '全域数学、知识大典与分形知识工程',
    '07_常数本源与真空涡旋': '统一常数、真空涡旋与本源方程组',
    '08_宇宙文明与工程平台包': '宇宙文明技术落地与工程平台交付包',
    '09_可视化与网页产出': 'HTML 报告页、可视化与演示页',
    '10_未分类与杂项': '主题域未识别的材料',
}

# ---------------------------------------------------------------- 只登记不搬
# 沿用 ingest_root_material.py 的既定口径：不是语料的东西不进仓库，否则会毁掉
# 「克隆即可校验」的对外承诺。这里三条：
MAX_BYTES = 50 * 1024 * 1024        # 大体积自动生成语料（亿字级知识大典）
ZIP_STEM_DIR = '内容已由同名解压目录收录，压缩包只登记'


def human(n: int) -> str:
    n = float(n)
    for u in ('B', 'KB', 'MB', 'GB'):
        if n < 1024 or u == 'GB':
            return '%.2f %s' % (n, u)
        n /= 1024.0
    return ''


def dir_stat(path: Path):
    n = sz = 0
    for r, d, f in os.walk(str(path)):
        d[:] = [x for x in d if x not in PRUNE]
        for y in f:
            n += 1
            try:
                sz += os.path.getsize(os.path.join(r, y))
            except OSError:
                pass
    return n, sz


def fingerprint(path: Path):
    """低成本指纹：大文件不全量哈希（2.7 GB 量级下没必要，且慢）。

    文件  -> (总字节, 头 64KB 的 sha1, 尾 64KB 的 sha1)
    目录  -> (总字节, 文件数, 相对路径+字节排序后拼串的 sha1)
    """
    import hashlib
    if path.is_file():
        sz = path.stat().st_size
        with open(str(path), 'rb') as f:
            head = hashlib.sha1(f.read(65536)).hexdigest()
            if sz > 131072:
                f.seek(sz - 65536)
                tail = hashlib.sha1(f.read(65536)).hexdigest()
            else:
                tail = '-'
        return ('f', sz, head, tail)
    n = sz = 0
    parts = []
    for r, d, fs in os.walk(str(path)):
        d[:] = [x for x in d if x not in PRUNE]
        for y in fs:
            p = Path(r) / y
            try:
                b = p.stat().st_size
            except OSError:
                continue
            n += 1
            sz += b
            parts.append('%s:%d' % (p.relative_to(path).as_posix(), b))
    import hashlib
    return ('d', sz, n, hashlib.sha1('|'.join(sorted(parts)).encode('utf-8', 'replace')).hexdigest())


def classify(name: str):
    for binname, pat, clue in BINS:
        if pat.search(name):
            return binname, clue
    return DEFAULT_BIN, DEFAULT_CLUE


def collect():
    """产出 (items, register_only)。

    顺序：先按体积与「zip 已有同名解压目录」判只登记，再对余下的做去重。
    去重放在后面，是为了让「重复件」的判定落在真正会被写入的条目之间。
    """
    raw = []
    if not SOURCE.exists():
        return raw, []

    def add(path: Path, origin: str):
        if path.is_dir():
            n, sz = dir_stat(path)
        else:
            n, sz = 1, path.stat().st_size
        binname, clue = classify(path.name)
        raw.append({'kind': '目录' if path.is_dir() else '文件',
                    'rel': path.relative_to(SOURCE).as_posix(),
                    'name': path.name, 'src': path,
                    'files': n, 'bytes': sz,
                    'origin': origin, 'bin': binname, 'clue': clue})

    # md/ 与 html/：按文件入箱（格式目录本身无主题意义）
    for sub in ('md', 'html'):
        base = SOURCE / sub
        if not base.exists():
            continue
        for p in sorted(base.rglob('*')):
            if not p.is_file():
                continue
            if any(x in p.parts for x in PRUNE):
                continue
            add(p, sub)

    # zip/202609/source/*：每个分包一个条目
    zsrc = SOURCE / 'zip' / '202609' / 'source'
    if zsrc.exists():
        for p in sorted(zsrc.iterdir()):
            add(p, 'zip/解压内容')

    # zip/202609/*.zip：原始压缩包（与解压目录同名者只登记）
    zdir = SOURCE / 'zip' / '202609'
    if zdir.exists():
        for p in sorted(zdir.glob('*.zip')):
            add(p, 'zip/原始包')

    # ---- 只登记不搬
    extracted = {p.name for p in zsrc.iterdir()} if zsrc.exists() else set()
    oversize = {it['name'] for it in raw if it['bytes'] > MAX_BYTES}
    items, reg = [], []
    for it in raw:
        if it['bytes'] > MAX_BYTES:
            reg.append({'name': it['name'], 'kind': it['kind'], 'origin': it['origin'],
                        'files': it['files'], 'bytes': it['bytes'],
                        'reason': '大体积自动生成语料（%s），不进仓库，保持原位' % human(it['bytes'])})
            continue
        if it['origin'] == 'zip/原始包' and it['name'][:-4] in extracted:
            # 解压目录本身若也超阈值（同样是亿字语料），两者都不写入，理由要写清楚，
            # 否则读者会以为压缩包的内容已经在仓库里了。
            stem = it['name'][:-4]
            reason = ('同名解压目录 `%s` 亦为大体积语料只登记；两者均未写入' % stem
                      if stem in oversize else ZIP_STEM_DIR)
            reg.append({'name': it['name'], 'kind': it['kind'], 'origin': it['origin'],
                        'files': it['files'], 'bytes': it['bytes'], 'reason': reason})
            continue
        items.append(it)

    # ---- 去重：内容完全相同的只留先出现的一个
    seen, dups = {}, []
    keep = []
    for it in items:
        fp = fingerprint(it['src'])
        if fp in seen:
            dup_of = seen[fp]
            dups.append({'name': it['name'], 'kind': it['kind'], 'origin': it['origin'],
                         'files': it['files'], 'bytes': it['bytes'],
                         'reason': '与已收录条目 `%s` 内容完全相同（指纹一致）' % dup_of})
            continue
        seen[fp] = it['name']
        keep.append(it)

    return keep, reg + dups


def unique_dest(binname: str, name: str, used: set):
    dst = DEST_ROOT / binname / name
    if str(dst) in used or dst.exists():
        stem, dot, ext = name.rpartition('.')
        i = 2
        while True:
            cand = DEST_ROOT / binname / ('%s__%d%s%s' % (stem, i, dot, ext))
            if str(cand) not in used and not cand.exists():
                return cand
            i += 1
    used.add(str(dst))
    return dst


def do_copy(items, manifest, move: bool):
    done = {e['target'] for e in manifest.get('entries', [])}
    used = set(done)
    for it in items:
        if it['rel'] in {e['rel'] for e in manifest.get('entries', [])}:
            it['status'] = 'skip(已登记)'
            continue
        dst = unique_dest(it['bin'], it['name'], used)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if move:
            shutil.move(str(it['src']), str(dst))
        else:
            if it['src'].is_dir():
                if dst.exists():
                    shutil.rmtree(str(dst))
                shutil.copytree(str(it['src']), str(dst),
                                ignore=shutil.ignore_patterns(*PRUNE))
            else:
                shutil.copy2(str(it['src']), str(dst))
        manifest.setdefault('entries', []).append({
            'rel': it['rel'], 'name': it['name'], 'kind': it['kind'],
            'source': str(it['src']), 'target': str(dst),
            'bin': it['bin'], 'origin': it['origin'],
            'files': it['files'], 'bytes': it['bytes'],
            'mode': 'move' if move else 'copy',
            'attribution': '待归属（线索：%s）' % it['clue'],
        })
        it['status'] = 'moved' if move else 'copied'
    return manifest


def write_manifest(manifest, reg):
    RECORD.mkdir(parents=True, exist_ok=True)
    manifest['generated'] = '2026-09-25'
    manifest['source_root'] = str(SOURCE)
    manifest['dest_root'] = str(DEST_ROOT)
    manifest['bin_rules'] = '见 ingest_ufthub_material.py 的 BINS'
    manifest['register_only'] = reg
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    return MANIFEST


def write_csv(manifest):
    DEST_ROOT.mkdir(parents=True, exist_ok=True)
    out = DEST_ROOT / '来料清单.csv'
    rows = []
    for e in sorted(manifest.get('entries', []), key=lambda x: (x['bin'], x['name'])):
        rows.append([e['name'], e['kind'], e['origin'], e['bin'],
                     e['files'], human(e['bytes']),
                     '已写入（%s）' % e['mode'],
                     e['attribution'].replace('线索：线索：', '线索：')])
    for r in manifest.get('register_only', []):
        rows.append([r['name'], r['kind'], r.get('origin', ''), '(仅登记)',
                     r['files'], human(r['bytes']), '未写入（留在原处）', r['reason']])
    with open(out, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['来源名', '类型', '来料区', '分箱', '文件数', '大小', '状态', '归属线索 / 不写入理由'])
        w.writerows(rows)
    return out


def write_bin_readmes(manifest):
    bins = {}
    for e in manifest.get('entries', []):
        bins.setdefault(e['bin'], []).append(e)
    for b, entries in sorted(bins.items()):
        d = DEST_ROOT / b
        d.mkdir(parents=True, exist_ok=True)
        lines = ['# %s' % b, '',
                 '> %s' % BIN_DESC.get(b, ''), '',
                 '> 本目录是**来源分箱**，不是体系归属。',
                 '> 箱内材料的体系归属一律为 `待归属`，须逐件人工核验后登记；',
                 '> 禁止仅凭文件名把材料登记到某个体系——那是伪造溯源。', '',
                 '## 箱内材料', '',
                 '| 来源 | 类型 | 来料区 | 文件数 | 大小 | 归属线索（非结论） |',
                 '|---|---|---|---|---|---|']
        for e in sorted(entries, key=lambda x: x['name']):
            lines.append('| `%s` | %s | %s | %d | %s | %s |' % (
                e['name'], e['kind'], e['origin'], e['files'],
                human(e['bytes']), e['attribution']))
        lines += ['', '## 如何把它登记为体系证据', '',
                  '1. 读材料本身，确认它证明/否证了什么；',
                  '2. 在目标体系的 `claims.csv` 增行，`evidence` 指向本目录下的具体文件；',
                  '3. 若无法归入 S01–S14 中任何体系，按 `01_独立体系/新体系模板` 建新体系；',
                  '4. 归属完成后，把文件移出本目录，并在 `90_历史归档/迁移记录` 留痕。', '']
        (d / 'README.md').write_text('\n'.join(lines), encoding='utf-8')


def write_top_readme(manifest):
    entries = manifest.get('entries', [])
    bins = {}
    for e in entries:
        bins.setdefault(e['bin'], []).append(e)
    lines = ['# ufthub 来料_20260925', '',
             '> 把 `my_lib/ufthub/`（统一场论来料中枢）的材料按**主题域**整理进 openuft。',
             '> 归集工具：[`ingest_ufthub_material.py`](../../00_项目治理/维护工具/ingest_ufthub_material.py)'
             '（默认复制，可 `--move`，可 `--restore`）。', '',
             '## 一、一句话结论', '',
             '**整理的是位置，不是结论。** 本目录内所有材料的体系归属一律为 `待归属`，',
             '只登记**线索**；逐件归属必须读材料本身后才能做。', '',
             '## 二、规模', '',
             '| 项 | 值 |', '|---|---|',
             '| 写入条目 | %d |' % len(entries),
             '| 写入文件数 | %d |' % sum(e['files'] for e in entries),
             '| 写入体积 | %s |' % human(sum(e['bytes'] for e in entries)),
             '| 逐条清单 | [来料清单.csv](来料清单.csv) |',
             '| 只登记未写入 | %d 条目 |' % len(manifest.get('register_only', [])),
             '| 迁移记录 | [20260925_ufthub归集](../../90_历史归档/迁移记录/20260925_ufthub归集/) |', '',
             '## 三、来源分箱', '',
             '分箱依据是**材料自身的主题域**，不是体系归属，也不是 ufthub 原有的',
             '`md/`、`html/`、`zip/` 格式目录——同一主题被拆散在三个目录里，',
             '按格式搬会保留无意义的结构。原格式区记入清单的「来料区」列。', '',
             '| 分箱 | 条目 | 文件数 | 体积 | 箱内是什么 |', '|---|---|---|---|---|']
    for b in sorted(bins):
        es = bins[b]
        lines.append('| [%s](%s/) | %d | %d | %s | %s |' % (
            b, b, len(es), sum(e['files'] for e in es),
            human(sum(e['bytes'] for e in es)), BIN_DESC.get(b, '')))
    lines += ['', '每个分箱各有 `README.md`，列出箱内条目与归属线索。', '',
              '## 四、只登记未写入的材料', '',
              '沿用 `ingest_root_material.py` 的口径：不是语料的东西不进仓库，',
              '否则会毁掉「克隆即可校验」的对外承诺。三类：', '',
              '| 来源名 | 大小 | 不写入的理由 |', '|---|---|---|']
    for r in sorted(manifest.get('register_only', []), key=lambda x: -x['bytes']):
        lines.append('| `%s` | %s | %s |' % (r['name'], human(r['bytes']), r['reason']))
    lines += ['', '它们留在 `my_lib/ufthub/` 原处，未搬动、未删除。', '',
              '去重保留哪一件：**沿用上游原名**（因此箱里会出现 `index (1).html` 这类带序号的名字，'
              '被它代表的那份记在表里）。不把代表件改成它上游没有的名字——改名会毁掉可追溯性，'
              '这与封存区「目录名照搬上游」是同一条规矩。', '',
              '## 五、为什么不直接写体系归属', '',
              '文件名同名不等于同一体系。已知案例：本批 `momentum_darboux.py`、',
              '`oam_tuft_couple_audit.py` 与现行 `01_独立体系/S02_空间光速螺旋统一力/04_理论推导/`',
              '下的同名文件是同源副本；而 `全域统一场论_*.md` 一类文件名带 TUFT、本体却可能是',
              '另一体系。因此本目录只做主题分箱，归属一律记 `待归属`，附**线索**而非结论。', '',
              '## 六、与现行 openuft 的差异（已核对，可据此逐件归属）', '',
              '| 材料 | 现行仓库状态 | 处置 |', '|---|---|---|',
              '| `统一场论_openuft_2026-09-25_r2` 的 S02 推导脚本（momentum_darboux / oam_tuft_couple / conservation_maxwell） | 已存在，同源 | 只归档，不覆盖 |',
              '| UFE-1 验证脚本 `ufe1_breakthrough.py` / `ufe1_round2.py` / `verify_ufe1_claims.py` | 现行 `07_统一场方程/验证脚本/` 缺 | 已合并进 `07_统一场方程/验证脚本/` |',
              '| `00_统一场方程/UFE1_场内容与验证基线.md` | 现行 `07_统一场方程/` 缺该锚点文档 | 已合并为 `07_统一场方程/UFE1_场内容与验证基线.md` |',
              '| `书籍/00_卷0_元理论`、`01_卷I_基础理论`（ch00–ch06 + 4 个 verify 脚本） | 现行 `书籍/v1_正文` 是「编」结构，此为「卷」结构，两套并存 | 只归档，未合并（结构不同，合并须人工裁定） |',
              '| 根级 `08_预言与判据/`、`09_现象覆盖矩阵/`、`11_证伪与反例/`、`12_研究结论/` | 空目录 | 只归档 |', '',
              '## 七、回滚', '',
              '```bash', 'python -B 00_项目治理/维护工具/ingest_ufthub_material.py --restore', '```', '',
              '依 `manifest.json` 删除本次写入的副本（默认复制模式，源 `my_lib/ufthub/` 不受影响）。', '',
              '[返回 90_历史归档](../README.md) · [返回总入口](../../README.md)', '']
    (DEST_ROOT / 'README.md').write_text('\n'.join(lines), encoding='utf-8')


def write_record(manifest):
    entries = manifest.get('entries', [])
    reg = manifest.get('register_only', [])
    lines = ['# 20260925 ufthub 来料归集', '',
             '把 `my_lib/ufthub/` 的统一场论材料按主题域整理进',
             '`90_历史归档/来源语料_ufthub_20260925/`。', '',
             '## 结果', '',
             '| 项 | 值 |', '|---|---|',
             '| 写入条目 | %d |' % len(entries),
             '| 写入文件数 | %d |' % sum(e['files'] for e in entries),
             '| 写入体积 | %s |' % human(sum(e['bytes'] for e in entries)),
             '| 只登记未写入 | %d 条目 / %s |' % (len(reg), human(sum(r['bytes'] for r in reg))),
             '| 写入方式 | 复制（源 `my_lib/ufthub/` 保持原位） |',
             '| 分箱数 | %d |' % len({e['bin'] for e in entries}), '',
             '## 为什么不移动', '',
             'ufthub 是仍在使用的来料中枢。复制保证「源不动、目标可删」，',
             '任何一步失败都不会同时丢掉两侧的可追溯性；确认整理无误后，',
             '可人工清理 `my_lib/ufthub/` 或对本工具加 `--move`。', '',
             '## 为什么不按 md/html/zip 分箱', '',
             'ufthub 按格式分目录，同一主题被拆散在三个目录里。按格式搬会保留',
             '无意义的结构，故改为按材料自身的主题域分箱，原格式区记入清单「来料区」列。', '',
             '## 为什么不写体系归属', '',
             '文件名同名不等于同一体系。归属一律记 `待归属`，附线索而非结论。', '',
             '## 回滚', '',
             '```bash',
             'python -B 00_项目治理/维护工具/ingest_ufthub_material.py --restore',
             '```', '']
    (RECORD / 'README.md').write_text('\n'.join(lines), encoding='utf-8')


def do_restore():
    if not MANIFEST.exists():
        print('没有 manifest.json，无可回滚')
        return 1
    m = json.loads(MANIFEST.read_text(encoding='utf-8'))
    n = 0
    for e in m.get('entries', []):
        t = Path(e['target'])
        if not t.exists():
            continue
        if t.is_dir():
            shutil.rmtree(str(t))
        else:
            t.unlink()
        n += 1
    print('已删除 %d 条副本（源 %s 未改动）' % (n, m.get('source_root', '')))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--go', action='store_true', help='实际写入（默认只预演）')
    ap.add_argument('--move', action='store_true', help='移动而非复制（默认复制）')
    ap.add_argument('--restore', action='store_true', help='按 manifest 删除已写入副本')
    args = ap.parse_args()
    if args.restore:
        return do_restore()

    items, reg = collect()
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {}

    print('=' * 78)
    print('ufthub 分箱计划（%s）' % ('实际写入' if args.go else '预演，不落盘'))
    print('=' * 78)
    total = 0
    for b in sorted({it['bin'] for it in items}):
        group = [it for it in items if it['bin'] == b]
        sz = sum(it['bytes'] for it in group)
        nf = sum(it['files'] for it in group)
        total += sz
        print('\n[%s]  %d 条目 / %d 文件 / %s' % (b, len(group), nf, human(sz)))
        for it in sorted(group, key=lambda x: -x['bytes'])[:6]:
            print('   %-56s %s' % (it['name'][:56], human(it['bytes'])))
        if len(group) > 6:
            print('   ... 其余 %d 条目见 来料清单.csv' % (len(group) - 6))
    print('\n合计写入：%d 条目 / %d 文件 / %s' % (len(items), sum(i['files'] for i in items), human(total)))
    print('只登记不写入：%d 条目 / %s' % (len(reg), human(sum(r['bytes'] for r in reg))))
    for r in sorted(reg, key=lambda x: -x['bytes'])[:8]:
        print('   %-52s %-10s %s' % (r['name'][:52], human(r['bytes']), r['reason'][:60]))

    if not args.go:
        print('\n预演结束。确认后加 --go 执行（默认复制；加 --move 则移动）。')
        return 0

    manifest = do_copy(items, manifest, args.move)
    write_manifest(manifest, reg)
    write_csv(manifest)
    write_bin_readmes(manifest)
    write_top_readme(manifest)
    write_record(manifest)
    print('\n完成。清单：%s' % (DEST_ROOT / '来料清单.csv'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
