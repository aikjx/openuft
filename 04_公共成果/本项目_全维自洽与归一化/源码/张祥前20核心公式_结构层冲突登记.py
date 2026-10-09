# -*- coding: utf-8 -*-
"""把「结构层第一性审计」的冲突回写 S17。

幂等：按 statement 前缀标记 `[结构层]` + 编号去重，重复执行不追加。
新增 claim_id 从现有 claims.csv 的最大号 +1 起分配，避免与并行工作撞号。

产物：
  01_独立体系/S17_统一场论核心公式/11_证伪与反例/核心公式结构层_缺陷记录_2026-09-29.md
  01_独立体系/S17_统一场论核心公式/claims.csv  （追加 S17-C00NN）

用法：python 张祥前20核心公式_结构层冲突登记.py
"""
import io
import os
import re
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SYS = os.path.join(ROOT, "01_独立体系", "S17_统一场论核心公式")
CLAIMS = os.path.join(SYS, "claims.csv")
RECORD = "11_证伪与反例/核心公式结构层_缺陷记录_2026-09-29.md"
RUN_ID = "04_公共成果/本项目_全维自洽与归一化/源码/张祥前20核心公式_元数据第一性审计.py"
DATA_ID = "04_公共成果/本项目_全维自洽与归一化/数据/张祥前20核心公式_元数据第一性审计.json"

# (编号标记, statement, uncertainty, evidence_level, status)
NEW_CLAIMS = [
    ("F2F4",
     "【结构层】#12/#13/#14 在元数据声明的 f 无量纲下量纲全部不成立；"
     "令 A 全程取 #04 的引力场时三式反解出的 [f] 唯一且一致 = M·I^-1（kg·A^-1），"
     "而该体系自带的显式表达式 f=(c/2)·sqrt(4*pi*eps0*G) 量纲为 M^-1·L·I"
     "（见 S17-C0031，实算 1.2917e-2），与需求相差 M^2·L^-1·I^-2 ⇒"
     "f 无任何取值能同时满足方程量纲与自身表达式，三式不可计算",
     "引擎 F1/F2/F4；自检 SC-31/SC-32；跨册引用 S17-C0031", "C", "falsified"),

    ("F3",
     "【结构层】符号 A 承担两种物理角色：#04 定义为引力场（L·T^-2），"
     "#13 的 curl(A)=B/f 要求 A 为磁矢势（M·L·T^-2·I^-1）。"
     "读法 I（全程 A=引力场）使 12/13/14/15 全自洽但要求 f 带量纲；"
     "读法 II（#13 内 A=磁矢势）使 f 无量纲却打破 #15 且与 #04 定义冲突 ⇒"
     "不存在无冲突的读法，#13 无法被唯一解释",
     "引擎 F3；量纲对照 [A引力场]=L·T^-2 vs [A磁矢势]=M·L·T^-2·I^-1", "C", "falsified"),

    ("S4",
     "【结构层】第 18 式『空间波动通解』L=f(t-r/c)+g(t+r/c) 并不满足第 8 式的波动方程："
     "代入径向拉普拉斯后残差为 2(g'-f')/(c·r)，仅当两个任意函数导数恒等时才为零，"
     "即它不是两任意函数构成的通解；球对称达朗贝尔解须带 1/r 因子，"
     "即 L=[f(t-r/c)+g(t+r/c)]/r（已用符号验算确认残差恒为零）",
     "引擎 S4；sympy 符号验算残差 2(g'-f')/(c·r)，修正形式残差 0", "C", "falsified"),

    ("S1",
     "【结构层】第 7 式（宇宙大统一方程）在 dC/dt=0 且 dm/dt=0 的经典极限下给出 "
     "F=-m·dV/dt，与牛顿第二定律 F=+m·dV/dt 反号；7 号 md 声称的『C=0 时退化为"
     "牛顿第二定律』代入后符号并不改变，该声称不成立。"
     "与 S02-C0001 / S12-C0006（统一动量低速极限冲突）同族，属缺陷族传播",
     "引擎 S1；同族记录 11_证伪与反例/统一动量低速极限冲突记录.md（S02/S12）", "C", "falsified"),

    ("S3",
     "【结构层】第 17 式与第 7 式不等价：json 版 #17 只有 F=(C-V)·dm/dt，"
     "缺失 #07 的 -m·dV/dt 项，而 claims.csv 的 S17-C0017 又登记为含该项的完整式；"
     "被丢掉的恰是 dm/dt=0 时唯一能提供惯性的项，故按 json 版，"
     "质量不变的光速飞行器受力恒为零，与『推进器』语义矛盾",
     "引擎 S3；json #17 vs S17-C0017 登记串互斥", "C", "falsified"),

    ("D1D3",
     "【结构层】单位约定不闭合：把 sr 视为有量纲时 20 式中 6 式不一致"
     "（#04 #09 #10 #12 #13 #14），把 sr 视为无量纲（SI 口径）时仍有 3 式不一致"
     "（#12 #13 #14）；且 #04 的 Δs 存在二难——保 k 的单位 kg·sr 则 Δs 须为 sr·m²，"
     "保 04md 声明的 Δs=m² 则 kg·sr 标注必错 ⇒ 不存在任何单一单位约定使 20 式全部量纲自洽",
     "引擎 D1/D3；量纲引擎自检 SC-01..SC-12 全通过", "C", "falsified"),

    ("K2H1",
     "【结构层】Z 与 Z' 是孤儿常数：逐式统计 20 条 formula_latex/formula_unicode，"
     "G 出现在 1 条、eps0 出现在 2 条，而 Z 与 Z' 各只出现在定义自己的 #19、#20 一条，"
     "下游引用数为 0；同时 20 式中 19 式自标记 verification_status=verified，"
     "却没有任何一条登记 prediction_value / prediction_urel ⇒ "
     "『Z 与 Z' 是统一引力与电磁的枢纽』这一叙事在公式集内没有落实",
     "引擎 K2/H1；usage 计数来自源 json 实读", "C", "falsified"),

    ("S5X6",
     "【结构层】第 1 式与第 2 式字面互斥：#01 的 r(t)=C·t 要求 C 恒定（轨迹为直线），"
     "#02 的螺旋轨迹速度方向持续旋转；二者同时成立需把 #01 改述为微分形式 dr=C(t)dt。"
     "另：json 的可视化默认参数违反本体系核心公设——#01 的 C 默认 [1,0,0]（范围 [-1,1] m/s，"
     "取不到 c），#02 默认 r=5,omega=1,h=2 给出 |dr/dt|=5.385 m/s，"
     "而 #16 的 v 又以 c 为单位且 c 默认写 1 ⇒ 同一元数据混用两套单位口径",
     "引擎 S5/X6；|C| 应为 2.99792458e8 m/s，默认参数差 3.0e8 倍", "C", "falsified"),
]

RECORD_BODY = """# 核心公式结构层缺陷记录（2026-09-29）

- 来源引擎：`04_公共成果/本项目_全维自洽与归一化/源码/张祥前20核心公式_元数据第一性审计.py`
- 机器产物：`04_公共成果/本项目_全维自洽与归一化/数据/张祥前20核心公式_元数据第一性审计.{json,md}`
- 判定报告：`04_公共成果/本项目_全维自洽与归一化/判定_张祥前20核心公式元数据_结构层第一性审计_2026-09-29.md`
- 统计：PASS = 4 / FAIL = 16 / BOUNDARY = 4 / INFO = 8；引擎自检 33/33；层级 L0/L1/L2/L3 = 7/7/6/0

本文件只登记**结构层**缺陷；常数层（Z、Z'、k、k'、f 的数值与单位标注、α 关系式）
已由 `07_计算复现/核心公式常数层_独立精算.py`（S17-C0021…C0032）登记，两册互补不重叠。

## 缺陷清单

| # | 判定 | 涉及式 | 内容 | 最小修复 |
|---|---|---|---|---|
| 1 | FAIL | #12 #13 #14 | f 无量纲声明下三式量纲不成立；唯一解 [f]=kg·A⁻¹，但与体系自带 f=(c/2)√(4πε₀G)（量纲 M⁻¹L I）互斥 | 需新物理：改 f 表达式或改方程 |
| 2 | BOUNDARY | #04 #13 #15 | 符号 A 角色重载（引力场 vs 磁矢势），两种读法各破一式 | 记号分离（A_g / A_m） |
| 3 | FAIL | #18 | 声称的通解不满足 #08，残差 2(g′−f′)/(c·r) | 加 1/r 因子 |
| 4 | FAIL | #07 | 经典极限 F = −ma 与牛顿反号（与 S02-C0001/S12-C0006 同族） | 需新约定（受力定义） |
| 5 | FAIL | #07 #17 | #17 缺失 −m dV/dt；json 与 claims 登记串互斥 | 统一登记串 |
| 6 | FAIL | 全局 | 无任一单位约定使 20 式全量纲自洽；#04 的 Δs 二难 | sr 视为无量纲 + k 单位改 kg |
| 7 | FAIL | #19 #20 | Z、Z' 下游引用数 0；19 式自称 verified 但 0 式登记数值预言 | 给出真正使用 Z/Z' 的式子，或降级为记号约定 |
| 8 | FAIL | #01 #02 | 两式字面互斥；可视化默认参数违反 \|C\|=c，且混用两套单位口径 | #01 改微分形式；参数统一以 c 为单位 |

## 与既有缺陷族的关系

- **同一缺陷族（跨体系传播）**：#07 的符号反转与 `S02-C0001`、`S12-C0006`
  （统一动量低速极限冲突）同源，是 `P = m(C−V)` 被借用时一并带入的。
- **同一结构模式（跨册）**：Z = Gc/2、ε₀ = c/(8πZ') 这类"把已知常数重新命名"
  的构造，与全仓已识别的 M02（普朗克锚定谬误 / 常数重排）同型：重排不是派生。

## 红线

结构层缺陷不等于物理判决。量纲自洽 ≠ 物理成立；本记录只声称"这套公式目前无法被
一致地读出与计算"，不声称该理论已被证伪。
"""


def read_claims():
    with io.open(CLAIMS, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def next_id(text):
    ids = [int(m) for m in re.findall(r"S17-C(\d+)", text)]
    return (max(ids) + 1) if ids else 1


def main():
    sys_cfg = json.load(io.open(os.path.join(SYS, "system.json"), encoding="utf-8"))
    rev = sys_cfg.get("hypothesis_revision", "core-formula-2026-01-23")
    text = read_claims()
    start = next_id(text)

    added, skipped = [], []
    for i, (tag, statement, unc, ev, status) in enumerate(NEW_CLAIMS):
        marker = "【结构层】"
        # 幂等：同一 tag 的条目若已存在（按内容片段判断）则跳过
        key = statement[:40]
        if key in text:
            skipped.append(tag)
            continue
        cid = "S17-C%04d" % (start + len(added))
        row = ",".join([
            cid, rev,
            '"%s"' % statement.replace('"', "'"),
            "",                       # assumptions
            "",                       # derivation
            "",                       # prediction
            "",                       # prediction_value
            "",                       # prediction_urel
            RUN_ID,
            "%s (%s)" % (DATA_ID, tag),
            unc.replace(",", "，"),
            ev, status, "",
        ])
        text = text.rstrip("\r\n") + "\r\n\r\n" + row + "\r\n\r\n"
        added.append((cid, tag))

    if added:
        with io.open(CLAIMS, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)

    rec_path = os.path.join(SYS, RECORD)
    with io.open(rec_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(RECORD_BODY)

    print("[登记] 新增 claim %d 条，跳过（已存在）%d 条" % (len(added), len(skipped)))
    for cid, tag in added:
        print("   + %s  (%s)" % (cid, tag))
    print("[登记] 缺陷记录：%s" % os.path.relpath(rec_path, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
