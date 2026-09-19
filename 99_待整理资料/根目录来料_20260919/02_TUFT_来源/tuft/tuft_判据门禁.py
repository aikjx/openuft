# -*- coding: utf-8 -*-
"""
TUFT 判据门禁（可复跑）
========================
把前几轮"人工判据"固化为可执行门禁，分四道：

  门禁一 量纲门禁：以精确有理指数向量 (M, L, T, Θ) 重算登记公式的量纲，与目标量纲比对
                   （可自动抓出 `αKTΩ/c²`、`ħc/(8πGM)`、`⟨T⟩²/K_sat²` 这类错误）
  门禁二 可观测锚门禁：每册报告必须出现观测锚（Planck / BICEP-Keck / CODATA / PDG / LIGO / 实测…），
                   无锚 => 不可判决
  门禁三 重述门禁：PASS 条目若全部是"标准/重述/继承/照搬/定义式"，判定为无 TUFT 增量
  门禁四 代码门禁：声称"仿真/数值模型"却未做逐行复现/与声称核对的册，标记

产物：`tuft_判据门禁.md`、`tuft_判据门禁.json`
红线：数学自洽 != 物理实验证实。量纲门禁只校验**登记公式的量纲自洽**，不校验物理正确性。
"""
from __future__ import print_function

import os
import re
import sys
import json
from fractions import Fraction as F

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_MD = os.path.join(HERE, "tuft_判据门禁.md")
OUT_JSON = os.path.join(HERE, "tuft_判据门禁.json")

M = (F(1), F(0), F(0), F(0))
ZERO = (F(0), F(0), F(0), F(0))
THETA = (F(0), F(0), F(0), F(1))
LEN = (F(0), F(1), F(0), F(0))
INV_LEN = (F(0), F(-1), F(0), F(0))
INV_LEN2 = (F(0), F(-2), F(0), F(0))
C = (F(0), F(1), F(-1), F(0))            # c
G = (F(-1), F(3), F(-2), F(0))           # G
HBAR = (F(1), F(2), F(-1), F(0))         # hbar
KB = (F(1), F(2), F(-2), F(-1))          # k_B
TORS = INV_LEN                            # 挠率/联络量纲 L^-1


def combine(powers):
    total = [F(0), F(0), F(0), F(0)]
    for _name, exp, dim in powers:
        for i in range(4):
            total[i] += F(exp) * dim[i]
    return tuple(total)


def fmt(d):
    names = ["M", "L", "T", "Θ"]
    parts = []
    for n, v in zip(names, d):
        if v == 0:
            continue
        parts.append("%s^%s" % (n, str(v)))
    return "·".join(parts) if parts else "1（无量纲）"


# ---- 量纲登记（表达式 -> 各因子幂次 -> 期望量纲）----
FORMULAS = [
    ("F-01", "m = α K T Ω / c²（续篇 §5.1 / SU(3) §5.1 / 黑洞 §3）",
     [("α", 1, ZERO), ("K", 1, INV_LEN2), ("T", 1, TORS), ("Ω", 1, ZERO), ("c", -2, C)], M),
    ("F-02", "ρ = α K T Ω（黑洞 §6 称能量密度）",
     [("α", 1, ZERO), ("K", 1, INV_LEN2), ("T", 1, TORS), ("Ω", 1, ZERO)],
     (F(1), F(-1), F(-2), F(0))),
    ("F-03", "T_H = ħ c /(8π G M)（原文式）",
     [("ħ", 1, HBAR), ("c", 1, C), ("G", -1, G), ("M", -1, M)], THETA),
    ("F-04", "T_H = ħ c³/(8π G k_B M)（正确式）",
     [("ħ", 1, HBAR), ("c", 3, C), ("G", -1, G), ("k_B", -1, KB), ("M", -1, M)], THETA),
    ("F-05", "T_H = ħ c √K(r_h)/(4π k_B)（几何式，K=1/r_h²）",
     [("ħ", 1, HBAR), ("c", 1, C), ("√K", 1, INV_LEN), ("k_B", -1, KB)], THETA),
    ("F-06", "M = c² r_h/(2G)（黑洞质量）",
     [("c", 2, C), ("r_h", 1, LEN), ("G", -1, G)], M),
    ("F-07", "F_T = 1 + ⟨T⟩²/K_sat²（挠率增强因子）",
     [("⟨T⟩", 2, TORS), ("K_sat", -2, INV_LEN2)], ZERO),
    ("F-08", "K_sat = 1/l_P²（饱和曲率）",
     [("l_P", -2, LEN)], INV_LEN2),
    ("F-09", "S_BH = A/(4 l_P²)（贝肯斯坦-霍金熵，nats）",
     [("A", 1, (F(0), F(2), F(0), F(0))), ("l_P", -2, LEN)], ZERO),
    ("F-10", "ε = (1/2κ)(V'/V)²（慢滚参数，κ 约定）",
     [("κ", -1, (F(-1), F(-1), F(2), F(0))), ("V'/V", 2, ZERO)], ZERO),
    ("F-11", "α_grav = G m²/(ħ c)（无量纲引力耦合）",
     [("G", 1, G), ("m", 2, M), ("ħ", -1, HBAR), ("c", -1, C)], ZERO),
    ("F-12", "m = ℏ√(κ²+τ²)/c（合法质量式）",
     [("ℏ", 1, HBAR), ("√", 1, INV_LEN), ("c", -1, C)], M),
]

BOOKS = [
    ("tuft_续篇_全维求导精算_report.txt", "续篇（自旋/泡利/手性）"),
    ("tuft_相位pi_全维求导精算_report.txt", "闭环相位 π"),
    ("tuft_色挠率_SU3_report.txt", "色挠率 SU(3)"),
    ("tuft_四力统一_report.txt", "四力统一主丛框架"),
    ("tuft_黑洞热力学_report.txt", "黑洞热力学 / 信息悖论"),
    ("tuft_暴胀CMB_report.txt", "宇宙暴胀 / CMB"),
    ("tuft_r5_report.txt", "挠率探测（R5）"),
    ("tuft_r6_report.txt", "挠率产生机制（R6）"),
    ("tuft_引力波_挠率扰动_report.txt", "B：挠率引力波"),
]

OBS_ANCHOR = r"(Planck|BICEP|Keck|CODATA|PDG|实测|实验|上限|相对偏差|偏差|σ|LIGO|ACME|LiteBIRD|CMB-S4|LZ|XENON|观测)"
RESTATE = r"(标准|重述|重述|继承|照搬|定义式|已知|教科书)"
CODE_CLAIM = r"(仿真|数值模型|代码|逐行复现|实跑)"
CODE_ACK = r"(实跑|逐行复现|复现|与声称核对|域内受限积分)"


def read(path):
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def main():
    md = []
    dim_rows, dim_fail = [], 0
    for fid, expr, powers, expect in FORMULAS:
        got = combine(powers)
        ok = got == expect
        if not ok:
            dim_fail += 1
        dim_rows.append((fid, expr, fmt(got), fmt(expect), "PASS" if ok else "FAIL"))

    gate2, gate3, gate4 = [], [], []
    for report, label in BOOKS:
        text = read(os.path.join(HERE, report))
        if not text:
            continue
        anchors = len(re.findall(OBS_ANCHOR, text))
        pass_lines = re.findall(r"\[\s*PASS[^\]]*\].*", text)
        restated = sum(1 for l in pass_lines if re.search(RESTATE, l))
        if anchors == 0:
            gate2.append((label, "无观测锚"))
        if pass_lines and restated == len(pass_lines):
            gate3.append((label, "PASS %d 条全部为重述/继承/标准（无 TUFT 增量）" % len(pass_lines)))
        if re.search(CODE_CLAIM, text) and not re.search(CODE_ACK, text):
            gate4.append((label, "声称仿真/数值模型但未做逐行复现"))

    md.append("# TUFT 判据门禁（自动生成）\n")
    md.append("> 由 `tuft_判据门禁.py` 生成（可复跑）。红线：量纲门禁只校验**登记公式的量纲自洽**，不校验物理正确性。\n")
    md.append("## 一、量纲门禁（精确有理指数向量 M/L/T/Θ）\n")
    md.append("| 编号 | 公式 | 实算量纲 | 期望量纲 | 判定 |")
    md.append("|---|---|---|---|---|")
    for fid, expr, got, exp, verdict in dim_rows:
        md.append("| %s | %s | `%s` | `%s` | %s |" % (fid, expr, got, exp, verdict))
    md.append("")
    md.append("量纲门禁：**%d/%d 通过，%d 条量纲非法**（均为前几轮已确认的真实缺陷）。\n"
              % (len(FORMULAS) - dim_fail, len(FORMULAS), dim_fail))
    md.append("## 二、可观测锚门禁\n")
    md.append("| 分册 | 结果 |")
    md.append("|---|---|")
    for label, note in gate2:
        md.append("| %s | ⚠️ %s |" % (label, note))
    if not gate2:
        md.append("| — | ✅ 全部 %d 册均有观测锚 |" % len(BOOKS))
    md.append("")
    md.append("## 三、重述门禁（PASS 是否全为标准结果重述）\n")
    for label, note in gate3:
        md.append("- %s：⚠️ %s" % (label, note))
    if not gate3:
        md.append("- ✅ 无分册的 PASS 全部来自重述（均有至少一条独立 PASS）。")
    md.append("")
    md.append("## 四、代码门禁（声称仿真 vs 逐行复现）\n")
    for label, note in gate4:
        md.append("- %s：⚠️ %s" % (label, note))
    if not gate4:
        md.append("- ✅ 声称仿真的分册均已做逐行复现/与声称核对。")
    md.append("")
    md.append("## 五、门禁判读\n")
    md.append("1. **量纲门禁最有效**：它把\"看起来专业\"的公式直接挡在门外"
              "（`αKTΩ/c²` → `L^-5T²`；`ħc/(8πGM)` → `M`；`⟨T⟩²/K_sat²` → `L²`）；")
    md.append("2. **可观测锚门禁**：无锚 = 不可判决，任何\"预言\"都失去意义；")
    md.append("3. **重述门禁**：PASS 若全为重述，则该册对 TUFT 的**证据增量为零**；")
    md.append("4. **代码门禁**：文字与代码必须逐条对齐，实跑判决优先于声明。")

    open(OUT_MD, "w", encoding="utf-8").write("\n".join(md) + "\n")
    json.dump({"dimension": [{"id": a, "expr": b, "got": c, "expect": d, "verdict": e}
                             for a, b, c, d, e in dim_rows],
               "obs_anchor_missing": [g[0] for g in gate2],
               "restate_only": [g[0] for g in gate3],
               "code_no_replay": [g[0] for g in gate4],
               "dim_fail": dim_fail},
              open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("已生成: " + OUT_MD)
    print("  量纲门禁: %d/%d 通过，%d 条非法" % (len(FORMULAS) - dim_fail, len(FORMULAS), dim_fail))
    for fid, expr, got, exp, v in dim_rows:
        if v == "FAIL":
            print("    FAIL %s: %s -> %s (expect %s)" % (fid, expr, got, exp))
    print("  无观测锚册数: %d ；PASS 全为重述册数: %d ；声称仿真未复现册数: %d"
          % (len(gate2), len(gate3), len(gate4)))


if __name__ == "__main__":
    main()
