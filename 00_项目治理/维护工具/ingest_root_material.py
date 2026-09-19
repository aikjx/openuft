#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 my_lib 根目录里尚未进入 openuft 的统一场论来源材料，归集进 openuft。

设计约束（均来自本项目已有治理）：
  1. 不猜测归属。文件名相同不等于同一体系；把 A 体系的文件登记成 B 体系，
     等于伪造溯源，违反 00_项目治理 的诚实要求。本工具只做**来源分箱**
     （按材料自身的主题域分箱），逐件归属留给人工，登记为 `待归属`。
  2. 不搬运重型库。根目录含 code/（45 GB）、utf/（3.4 GB）、article/（2.1 GB）
     等，属开发工作区或外部资料，迁入既无意义也会毁掉仓库可用性。
     这类只**登记**，不移动。
  3. 可回滚。移动前把 (原路径, 目标路径, 字节, mtime) 全部写进 manifest.json；
     用 `--restore` 即可按 manifest 逐条搬回原位（无独立的 restore.py）。
  4. 幂等。重复运行不会产生嵌套；目标已存在则跳过并记 skip。

用法：
    python -B 00_项目治理/维护工具/ingest_root_material.py            # 预演，只出清单
    python -B 00_项目治理/维护工具/ingest_root_material.py --go       # 实际移动
    python -B 00_项目治理/维护工具/ingest_root_material.py --restore  # 撤销（读 manifest）
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
# 封存区放 90_历史归档 而非 99_待整理资料：本区语义是「已完成位置迁移、待逐件归属的
# 既有来源」，更接近历史快照；且 90_历史归档 在 verify.py 中豁免链接检查，来源自带的
# 相对链接不会误报断链。见 99_待整理资料/README.md。
DEST_ROOT = OPENUFT / '90_历史归档' / '来源语料_根目录_20260919'
RECORD = OPENUFT / '90_历史归档' / '迁移记录' / '20260919_根目录归集'
MANIFEST = RECORD / 'manifest.json'

# ---------------------------------------------------------------- 分类规则
# 规则一律写成「来源分箱」，不写成体系归属。attribution 列只给"线索"，须人工核验。

# 目录：显式白名单（未列出的一律不搬，避免误伤工作区）
DIR_BINS = {
    '整理': ('01_整理包_ZXUFT', '张祥前统一场论研究平台：React 前端 + 17 公式验证脚本 + 图 + 报告',
             '线索：ZXUFT/ZUFT/Z′ 常数，与 S02/S12「空间光速螺旋」域相邻'),
    'tuft': ('02_TUFT_来源', 'TUFT 主线脚本与产出', '线索：与 S14 挠率统一场论 TUFT 同名'),
    'GAQ-UFT_Complete_Book': ('03_GAQ_书稿来源', 'GAQ-UFT 完整书稿（LaTeX + 卷 I–VI + 补充代码）',
                              '线索：与 S03/S07/S08/S09 GAQ 系列同名'),
    'triad_uft': ('04_三重奏与螺旋_来源', 'triad_uft 三分量实现包', '线索：与 S01 三重奏域相邻'),
    'step_by_step_verification': ('04_三重奏与螺旋_来源', '分步验证脚本（螺旋→电磁→质量电荷→高斯通量）',
                                  '线索：螺旋动力学，与 S01/S02 相邻'),
    'helical_db': ('04_三重奏与螺旋_来源', '螺旋数据库核心实现', '线索：螺旋几何，与 S01/S10 相邻'),
    'utf_visualization': ('04_三重奏与螺旋_来源', 'UTF 可视化产出', '待归属'),
    'visualization_output': ('04_三重奏与螺旋_来源', '可视化输出（图/报告）', '待归属'),
    '可视化': ('04_三重奏与螺旋_来源', '螺旋运动引力生成机制配图', '待归属'),
    'formula_visualizations': ('04_三重奏与螺旋_来源', '公式 SVG', '待归属'),
    'unified-field-theory': ('05_独立路线网页_来源', '独立路线网页版（含封面/配图）', '待归属'),
    'unified-field-theory-full': ('05_独立路线网页_来源', '独立路线网页版（完整）', '待归属'),
    'tan_arctan_unified_field': ('05_独立路线网页_来源', 'tan–arctan 映射统一场论网页版', '待归属'),
    'uft': ('06_UM论文与书稿_来源', 'uft/ 原始工作目录（含 06-论文/全域数学统一场论）',
            '线索：UM 全域数学，候登记'),
    '全域统一场论_书稿': ('06_UM论文与书稿_来源', '全域统一场论书稿（outline + manuscript ch01–ch14）',
                          '线索：TUFT 全维求导链'),
}

# 根文件：前缀/正则 -> 分箱
FILE_BINS = [
    (re.compile(r'^TUFT', re.I), '02_TUFT_来源', '线索：与 S14 挠率统一场论 TUFT 同名'),
    (re.compile(r'^tuft', re.I), '02_TUFT_来源', '线索：与 S14 挠率统一场论 TUFT 同名'),
    (re.compile(r'^全域统一场论'), '02_TUFT_来源', '线索：TUFT 全维求导与验证'),
    (re.compile(r'^bifuf', re.I), '07_bifuf_来源', '线索：候裁定体系（三份 JSON 结论互相矛盾）'),
    (re.compile(r'^(_diag|_dbg|_probe|_scan|_shoot|_derive|_integrate|_riccati|_audit|_check)'),
     '08_调试与临时产物', '调试/审计脚本，非结论载体'),
    (re.compile(r'^(_ma_|_coef|_ls1|_att_|_toy)'), '08_调试与临时产物', '中间产物，非结论载体'),
    (re.compile(r'^(hopf|thomas|bloch|universal_math|V21|TUFT全维)'), '08_调试与临时产物', '单篇产出'),
    (re.compile(r'^(verify_unified_theory|verify_numeric_out|debug_S_consistency|force_normalization_results)'),
     '08_调试与临时产物', '单篇验证产出'),
]

# 只登记不搬运的重型库 —— 迁入无意义（开发工作区 / 外部资料 / 体积）
REGISTER_ONLY = {
    'code': '开发工作区（397,783 文件 / 45.2 GB）',
    'utf': '外部理论库（12,102 文件 / 3.4 GB），含编号目录如「17-空间光速螺旋引力理论」',
    'article': '文章库（3,178 文件 / 2.1 GB，中英双语）',
    'math': '数学资料（1,446 文件 / 1.25 GB，含 SOM/黎曼/素数等）',
    'research': '研究数据（含 research/goldbach_pwcv）',
    'aikjxcz': '站点/静态资源（338 MB）',
    'my': '个人资料（180 MB）',
    'images': '图片库', 'img': '图片库', 'media': '媒体库',
    'output': '构建输出', 'outputs': '构建输出', 'exports': '导出产物',
    'dist': '前端构建产物', 'src': '前端源码', 'cypress': 'E2E 测试',
    'data': '数据集', 'docs': '项目文档', 'scripts': '杂项脚本',
    'tests': '测试', 'examples': '示例', 'enterprise': '企业相关',
    'git': '版本库副本', 'reports': '报告', '日志': '运行日志',
    'test_logs': '测试日志', 'temp': '临时', 'misc': '杂项',
    'novel-helper': '非本项目', 'goldbach_route': '非本项目（数论路线）',
    'directory-analysis': '目录分析', 'draft_506fa474_folder': '草稿',
    '启动脚本': '启动脚本', 'paper': '空目录', 'verification_output': '验证输出',
}
# ws_v2.* 工作区快照：整体登记不搬
WS_SNAPSHOT = re.compile(r'^ws_v2\.\d+_backup_\d{8}$')


def human(n: int) -> str:
    for u in ('B', 'KB', 'MB', 'GB'):
        if n < 1024 or u == 'GB':
            return '%.2f %s' % (n, u)
        n /= 1024.0
    return ''


def scan():
    """产出 (plan, register_only, skipped)。plan 内每项为 dict。"""
    plan, reg, skip = [], [], []
    for name in sorted(os.listdir(REPO)):
        src = REPO / name
        if name.startswith('.') and name not in ('.gitattributes', '.gitignore'):
            skip.append((name, '点目录/点文件'))
            continue
        if name in ('openuft', 'openmath', 'openmath-dev', 'openmath_sys'):
            skip.append((name, '其它项目根'))
            continue
        if WS_SNAPSHOT.match(name):
            reg.append((name, 'worktree', '工作区快照（ws_v2.*），只登记'))
            continue
        if src.is_dir():
            if name in DIR_BINS:
                binname, desc, clue = DIR_BINS[name]
                n, sz = 0, 0
                for r, d, f in os.walk(src):
                    d[:] = [x for x in d if x not in ('__pycache__', '.git', '.history', 'node_modules', '.venv')]
                    for y in f:
                        n += 1
                        try:
                            sz += os.path.getsize(os.path.join(r, y))
                        except OSError:
                            pass
                plan.append({'kind': 'dir', 'name': name, 'bin': binname,
                             'desc': desc, 'clue': clue, 'files': n, 'bytes': sz})
            elif name in REGISTER_ONLY:
                reg.append((name, 'dir', REGISTER_ONLY[name]))
            else:
                skip.append((name, '目录：未在分类表中，保持原位'))
        else:
            try:
                sz = src.stat().st_size
            except OSError:
                continue
            for pat, binname, clue in FILE_BINS:
                if pat.search(name):
                    plan.append({'kind': 'file', 'name': name, 'bin': binname,
                                 'desc': '根目录来源文件', 'clue': clue,
                                 'files': 1, 'bytes': sz})
                    break
    return plan, reg, skip


def do_move(plan, manifest):
    moved = manifest.get('entries', [])
    done = {e['target'] for e in moved}
    for item in plan:
        src = REPO / item['name']
        dst = DEST_ROOT / item['bin'] / item['name']
        if str(dst) in done or dst.exists():
            item['status'] = 'skip(已存在)'
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        moved.append({'name': item['name'], 'kind': item['kind'],
                      'source': str(src), 'target': str(dst),
                      'bytes': item['bytes'], 'bin': item['bin'],
                      'attribution': '待归属（%s）' % item['clue']})
        item['status'] = 'moved'
    manifest['entries'] = moved
    return manifest


def write_manifest(manifest, plan, reg, skip):
    RECORD.mkdir(parents=True, exist_ok=True)
    manifest['generated'] = '2026-09-19'
    manifest['bin_rules'] = '见 ingest_root_material.py 的 DIR_BINS / FILE_BINS'
    manifest['register_only'] = [{'name': n, 'kind': k, 'reason': r} for n, k, r in reg]
    manifest['held_back'] = [{'name': n, 'reason': r} for n, r in skip
                             if '点目录' not in r and '其它项目' not in r]
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    return MANIFEST


def write_csv(plan, manifest):
    """清单以 manifest 为唯一数据源。

    早期版本按「当次计划」写 CSV，导致重复执行（第二次计划为空）时把清单覆盖成
    只剩表头 —— 所以这里改成只读 manifest，保证任何一次运行的结果都等价。
    """
    DEST_ROOT.mkdir(parents=True, exist_ok=True)
    out = DEST_ROOT / '来料清单.csv'
    live = {it['name']: it for it in plan}
    rows = []
    for e in sorted(manifest.get('entries', []), key=lambda x: (x['bin'], x['name'])):
        it = live.get(e['name'])
        rows.append([
            e['name'],
            '目录' if e['kind'] == 'dir' else '文件',
            e['bin'],
            it['files'] if it else '',
            human(e['bytes']),
            '已迁入',
            e['attribution'].replace('线索：线索：', '线索：'),
        ])
    # 只登记未搬的重型库也进清单，否则读者会以为它们"不存在"
    for r in manifest.get('register_only', []):
        rows.append([r['name'], '目录' if r['kind'] == 'dir' else '文件',
                     '(仅登记)', '', '', '未迁入（留在原处）', r['reason']])
    for r in manifest.get('held_back', []):
        rows.append([r['name'], '—', '(未分类)', '', '', '未迁入（留在原处）', r['reason']])
    with open(out, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['来源名', '类型', '分箱', '文件数', '字节', '状态', '归属状态 / 不搬理由'])
        w.writerows(rows)
    return out


def write_readmes(plan):
    bins = {}
    for it in plan:
        bins.setdefault(it['bin'], []).append(it)
    for b, items in sorted(bins.items()):
        d = DEST_ROOT / b
        d.mkdir(parents=True, exist_ok=True)
        lines = ['# %s' % b, '',
                 '> 本目录是**来源分箱**，不是体系归属。',
                 '> 箱内材料的体系归属一律为 `待归属`，须逐件人工核验后登记；',
                 '> 禁止仅凭文件名把材料登记到某个体系——那是伪造溯源。', '',
                 '## 箱内材料', '',
                 '| 来源 | 类型 | 文件数 | 大小 | 归属线索（非结论） |',
                 '|---|---|---|---|---|']
        for it in sorted(items, key=lambda x: x['name']):
            lines.append('| `%s` | %s | %d | %s | %s |' % (
                it['name'], '目录' if it['kind'] == 'dir' else '文件',
                it['files'], human(it['bytes']), it['clue']))
        lines += ['', '## 如何把它登记为体系证据', '',
                  '1. 读材料本身，确认它证明/否证了什么；',
                  '2. 在目标体系的 `claims.csv` 增行，`evidence` 指向本目录下的具体文件；',
                  '3. 若无法归入 S01–S14 中任何体系，按 `01_独立体系/新体系模板` 建新体系；',
                  '4. 归属完成后，把文件移出本目录，并在 `90_历史归档/迁移记录` 留痕。', '']
        (d / 'README.md').write_text('\n'.join(lines), encoding='utf-8')


def write_record(plan, manifest, reg, skip):
    RECORD.mkdir(parents=True, exist_ok=True)
    moved = manifest.get('entries', [])
    tb = sum(e['bytes'] for e in moved)
    lines = ['# 20260919 根目录来源材料归集', '',
             '把 `my_lib` 根目录中尚未进入 openuft 的统一场论来源材料，', 
             '原样封存到 `90_历史归档/来源语料_根目录_20260919/`。', '',
             '## 结果', '',
             '| 项 | 值 |', '|---|---|',
             '| 迁入条目 | %d |' % len(moved),
             '| 迁入字节 | %s |' % human(tb),
             '| 只登记未搬（重型库/快照） | %d |' % len(reg),
             '| 保持原位（未在分类表内） | %d |' % len([1 for _, r in skip if '未在分类表' in r]), '',
             '## 为什么不搬重型库', '',
             '根目录合计约 52.8 GB，其中 `code/` 45 GB、`utf/` 3.4 GB、`article/` 2.1 GB。',
             '这些是开发工作区与外部资料，不是统一场论语料；迁入会同时毁掉仓库可用性与',
             '"克隆即可用"的对外承诺。故只登记名称、规模与不搬理由，见 `manifest.json`。', '',
             '## 为什么不写体系归属', '',
             '文件名同名不等于同一体系（已知案例：`全域统一场论_*.md` 文件名带 TUFT，',
             '本体却是 S13 的阴阳对偶旋量 + Hopf 六方程闭环）。因此本目录只做主题分箱，',
             '归属一律记 `待归属`，附**线索**而非结论。', '',
             '## 回滚', '',
             '```bash',
             'python -B 00_项目治理/维护工具/ingest_root_material.py --restore',
             '```', '',
             '`manifest.json` 逐条记录了 (原路径, 目标路径, 字节, 分箱)；', 
             'restore 依此把每个条目搬回原位，不依赖 git。', '']
    (RECORD / 'README.md').write_text('\n'.join(lines), encoding='utf-8')


def do_restore():
    if not MANIFEST.exists():
        print('没有 manifest.json，无可回滚')
        return 1
    m = json.loads(MANIFEST.read_text(encoding='utf-8'))
    n = 0
    for e in m.get('entries', []):
        s, t = Path(e['source']), Path(e['target'])
        if t.exists() and not s.exists():
            s.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(t), str(s))
            n += 1
    print('已还原 %d 条' % n)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--go', action='store_true', help='实际移动（默认只预演）')
    ap.add_argument('--restore', action='store_true', help='按 manifest 回滚')
    args = ap.parse_args()
    if args.restore:
        return do_restore()

    plan, reg, skip = scan()
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {}

    print('=' * 74)
    print('来源分箱计划（%s）' % ('实际执行' if args.go else '预演，不落盘'))
    print('=' * 74)
    tb = 0
    for b in sorted({it['bin'] for it in plan}):
        items = [it for it in plan if it['bin'] == b]
        sz = sum(it['bytes'] for it in items)
        tb += sz
        print('\n[%s]  %d 条目 / %s' % (b, len(items), human(sz)))
        for it in sorted(items, key=lambda x: -x['bytes'])[:8]:
            print('   %-52s %s' % (it['name'][:52], human(it['bytes'])))
        if len(items) > 8:
            print('   ... 其余 %d 条目见 来料清单.csv' % (len(items) - 8))
    print('\n合计迁入：%d 条目 / %s' % (len(plan), human(tb)))
    print('只登记不搬：%d 项（重型库与工作区快照）' % len(reg))
    print('保持原位  ：%d 项（未在分类表内）' % len([1 for _, r in skip if '未在分类表' in r]))

    if not args.go:
        print('\n预演结束。确认后加 --go 执行。')
        return 0

    manifest = do_move(plan, manifest)
    write_manifest(manifest, plan, reg, skip)
    write_csv(plan, manifest)
    write_readmes(plan)
    write_record(plan, manifest, reg, skip)
    print('\n完成。清单：%s' % (DEST_ROOT / '来料清单.csv'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
