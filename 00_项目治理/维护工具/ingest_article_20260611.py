#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 my_lib/article/zh/2026/6/11 的「空间螺旋几何化统一场论」来源文章收拢进 openuft。

设计约束（均来自本项目已有治理，与 ingest_root_material.py / ingest_ufthub_material.py 同口径）：
  1. **不猜测归属。** 文件名相同不等于同一体系。本工具只做**来源分箱**（按材料自身的
     主题域分箱），`体系线索` 一列只给方向、不是认定；逐件归属留给人工，一律记 `待归属`。
  2. **放 90_历史归档/来源语料_*。** 该前缀在 verify.py 中豁免「目录名必须含中文」与
     本地链接检查（见 verify.py 的 is_archive_raw），来源自带的相对链接不会误报断链。
  3. **复制而非移动。** 来源原文保留在 article/zh/2026/6/11，归档目录是副本。
  4. **幂等。** 目标已存在且字节 + SHA-256 相同则记 skip，不重复写入。
  5. **不重不漏。** 分箱后对源目录做一次完整性守卫：源目录里每个文件都必须恰好落箱
     一次；多一件或漏一件即以非零码退出（这条守卫是本工具存在的理由之一）。

用法（在 openuft/ 下执行）：
    python -B 00_项目治理/维护工具/ingest_article_20260611.py            # 预演，只出清单
    python -B 00_项目治理/维护工具/ingest_article_20260611.py --go       # 实际复制
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import shutil
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

TOOL_DIR = Path(__file__).resolve().parent
OPENUFT = TOOL_DIR.parent.parent                      # openuft/
REPO = OPENUFT.parent                                 # my_lib/
SRC = REPO / 'article' / 'zh' / '2026' / '6' / '11'
DEST = OPENUFT / '90_历史归档' / '来源语料_20260611_螺旋几何化统一场论文章'

# ---------------------------------------------------------------- 分箱规则
# 规则一律写成「来源分箱」，不写成体系归属。第三列只给"线索"（对应
# 07_统一场方程/空间螺旋几何化统一场论 的 10 个子系统），须人工核验。
BINS = [
    ("00_核心主论与总纲",
     "框架总纲、主论文与总结版",
     "体系一 空间螺旋几何本体论（地基）",
     ["1.md",
      "核心理论体系总纲.md",
      "最伟大的统一场论：无量纲全数学化突破——空间时间本源.md",
      "算法联盟最高权限：全维几何化总纲——无循环无自由参数量纲闭合可验证.md",
      "算法联盟最高权限：正确内容总结版——突破空间螺旋几何化语言.md",
      "算法联盟最高权限：核心内容总结与Python验证.md"]),
    ("01_精细结构常数拓扑本源",
     "α 的拓扑本征值/谱流/量子相位三条推导路径与 Δ_top 精算",
     "体系二 α 几何化与拓扑本源",
     ["算法联盟最高权限：从拓扑本征值推出N=137——完成α的本源推导.md",
      "算法联盟最高权限：精确计算拓扑修正项Δ_top——完成α的精确推导.md"]),
    ("02_力系归一化与引力悖论",
     "四力归一化和 = 1；引力在归一化层最大、在表观层最小的悖论",
     "体系三 力系归一化 + 体系九 引力最大 vs 最小",
     ["为什么引力最大：力的几何归一化统一场论.md",
      "引力为什么现实中最小：归一化强度与表观强度的悖论.md"]),
    ("03_全常数几何化",
     "G、ε₀、e、ℏ、c、m 的几何化字典（含 G=α²μ₀c²ρ²）",
     "体系五 全常数几何化字典（含 G 循环论证）",
     ["G=α²μ₀几何本源：引力常数与磁导率的无量纲化统一.md",
      "算法联盟最高权限：全常数几何化——统一场论终极突破.md",
      "算法联盟最高权限：全维度突破——所有物理常数几何化无量纲化终极统一.md",
      "算法联盟最高权限：利用α的精确值完成G和ε₀的几何化.md"]),
    ("04_频率控制与最优频率",
     "ω 的几何本源、频率控制引力效应、最优频率选择",
     "体系六 频率控制与第五力",
     ["频率控制全维总结：效果现象与核心公式——算法联盟最高权限.md",
      "频率控制与最大引力效应：算法联盟最高权限突破.md",
      "最优频率选择：全维度突破的频率优化理论——算法联盟最高权限最伟大论文.md"]),
    ("05_无穷维与高阶力系",
     "αⁿ 无穷级数力谱、N=1/[α²(1−α)] 的高阶归一化与暗能量/暗物质命名",
     "体系七 无穷维 / 高阶力系 + 体系十 18917 归一化因子",
     ["算法联盟最高权限：宇宙秘密全维突破——高阶力系与空间螺旋几何本源.md",
      "全维度精算验证：无穷维力系统一场论Python最高权限分析.md"]),
    ("06_阴阳与道法术器用",
     "阴阳=曲率+挠率、N 的两套定义、18917 的素数/历史/神秘学解读",
     "体系四 阴阳平衡 + 体系八 道法术器用元框架 + 体系十 18917 因子",
     ["算法联盟突破阴阳：道法术器用统一场论.md",
      "N归一化因子.md",
      "18917宇宙归一化因子：素数神秘学与历史锚点解析.md"]),
    ("07_求导证明与精算验证",
     "自称 10000 位精度求导证明与全维精算验证（自陈，未独立复核）",
     "验证层（体系一–五的自陈精算，openuft 未复核）",
     ["算法联盟最高权限：空间螺旋几何化统一场论——全维度全方面求导证明验证分析.md",
      "算法联盟最高权限：空间螺旋几何化统一场论——终极求导证明验证精算分析全维度.md"]),
    ("08_下一个维度突破",
     "「用」层技术愿景：维度穿越、时间操控、意识上传的实验验证与技术方案",
     "体系八 元框架的「用」层（无实验支撑）",
     ["算法联盟最高权限：突破下一个维度——总结与展望.md",
      "算法联盟最高权限：下一个维度突破——实验验证与技术实现.md",
      "算法联盟最高权限：下一个维度突破——详细技术方案.md"]),
    ("09_多语种论文",
     "同一框架的英文平行版本（G–ε₀ 统一、量子力学几何本源、力系本源、全框架）",
     "体系一–五 的英文平行版本",
     ["Gravitational_Electromagnetic_Unification_Space_Spiral.md",
      "Quantum_Mechanics_Space_Spiral_Geometric_Origin.md",
      "Space_Spiral_Geometric_Origin_of_Fundamental_Forces.md",
      "Space_Spiral_Geometric_Unified_Field_Theory.md"]),
]

CODE_BIN = ("code", "验证脚本与结果（Python 精算、结果 txt、可视化 HTML/PNG）",
            "验证层（脚本自陈输出，未纳入 openuft 独立复算）")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def plan():
    """产出 (分箱, 源文件, 目标文件, 字节, 主题, 线索) 列表。"""
    rows = []
    for bin_name, theme, clue, names in BINS:
        for name in names:
            rows.append((bin_name, SRC / name, DEST / bin_name / name, theme, clue))
    code_src = SRC / 'code'
    if code_src.is_dir():
        for child in sorted(code_src.iterdir()):
            if child.is_file():
                rows.append((CODE_BIN[0], child, DEST / CODE_BIN[0] / child.name,
                             CODE_BIN[1], CODE_BIN[2]))
    return rows


def source_inventory():
    files = set()
    for dirpath, _dirnames, filenames in os.walk(SRC):
        for name in filenames:
            files.add(Path(dirpath, name).relative_to(SRC).as_posix())
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go', action='store_true', help='实际复制（缺省为预演）')
    args = parser.parse_args()

    if not SRC.is_dir():
        print('[FAIL] 源目录不存在：' + str(SRC))
        return 1

    rows = plan()
    planned = {src.relative_to(SRC).as_posix() for _b, src, _d, _t, _c in rows}

    # 完整性守卫：源目录里每个文件都必须恰好落箱一次
    inventory = source_inventory()
    missing, extra = sorted(inventory - planned), sorted(planned - inventory)
    if missing or extra:
        print('[FAIL] 分箱不完整 missing={} extra={}'.format(missing, extra))
        return 1

    manifest, copied, skipped = [], 0, 0
    for bin_name, src, dst, theme, clue in rows:
        rel = src.relative_to(SRC).as_posix()
        if not src.is_file():
            print('[FAIL] 源文件缺失：' + rel)
            return 1
        same = (dst.exists() and dst.stat().st_size == src.stat().st_size
                and sha256(dst) == sha256(src))
        action = 'skip' if same else ('copied' if args.go else 'todo')
        if args.go and not same:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1
        elif same:
            skipped += 1
        print('  {:<8} {:<16} {}'.format(action, bin_name, rel))
        manifest.append([bin_name, rel, dst.relative_to(DEST).as_posix(),
                         src.stat().st_size, theme, clue, action])

    # 只在**本次确有复制**时重写清单：否则重跑会把「copied」改写成「skip」，
    # 把「这批材料是怎么进来的」这一条记录擦掉（幂等重跑不该改历史）。
    if args.go and copied:
        with (DEST / '来料清单.csv').open('w', encoding='utf-8-sig', newline='') as handle:
            writer = csv.writer(handle, lineterminator='\n')
            writer.writerow(['分箱', '原文件', '迁入路径', '字节', '主题', '体系线索（待人工核验）', '动作'])
            writer.writerows(manifest)

    print('\n分箱 {} 件（copied={} skip={}）；源目录 {} 件，全部落箱。{}'.format(
        len(rows), copied, skipped, len(inventory),
        '' if args.go else '（预演模式，加 --go 执行）'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
