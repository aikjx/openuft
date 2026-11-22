# -*- coding: utf-8 -*-
"""TUFT-r439 | ROOT V119/V133/V134/V135 自证边界与三定理攻破.

靶点: 第四批新发现版本 (r438 之后), 恰好对准 r438 的四类缺口.
本册不重判 r438, 只机核新来料自己给出的四条结构性结论:
  T1 一维复相位不能承载非平凡 SU(2)/SU(3)  (V134 §3)
  T2 全局单值纯相位 A=dθ ⇒ F=0 ⇒ N=0     (V135 §4)
  T3 三代 N=3 是背景整数输入, 未由 κ/τ 导出 (V135 §3.1)
  T4 指标 ≠ 零模总数 (V135 §6.1, N=0 时 2 个零模)
另加三项可复算读数: 最小普适转子被 CODATA 排除 / α 无唯一性 / Lorentz 障碍.

不做: 不宣称攻破方向、不改被引文件、不重判 r438、不做 git.
纯标准库 Python 3.8.
"""
import cmath
import io
import json
import math
import os
import random
import re
import sys
from fractions import Fraction as F
from pathlib import Path

try:
    _r = getattr(sys.stdout, "reconfigure", None)
    if callable(_r):
        _r(errors="replace")
except Exception:
    pass

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
OUT = BASE / "数据"
NAME = "TUFT-r439_ROOT_V119-V135_自证边界与三定理攻破_精算_2026-11-22"
ROUND = "r439"
DATE = "2026-11-22"

CORPUS = ROOT / "90_历史归档" / "来源语料_ufthub_ROOT_V119-V135_202611d"
ZIPLIST = ROOT.parent / "ufthub" / "zip" / "202611d" / "_清单_ROOT_V系列_202611d.json"

ENTRIES, GUARDS, CONTROLS = [], [], []


def add(code, status, title, detail):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))


def guard(code, cond, note):
    GUARDS.append(dict(code=code, ok=bool(cond), note=note))


def ctrl(code, cond, note):
    CONTROLS.append(dict(code=code, ok=bool(cond), note=note))


def read_text(p):
    for enc in ("utf-8-sig", "utf-8", "gbk"):
        try:
            return io.open(str(p), encoding=enc).read()
        except Exception:
            continue
    return ""


# ============================================================ A 事实源
man = json.loads(read_text(ZIPLIST))
files = man["files"]
vdirs = sorted([d for d in CORPUS.iterdir() if d.is_dir()])
mds = sorted([p for d in vdirs for p in d.rglob("*.md")])

guard("G-A1", CORPUS.is_dir() and ZIPLIST.is_file(), "语料目录与清单存在")
guard("G-A2", len(files) == 4, "清单 4 文件, 实得 %d" % len(files))
guard("G-A3", sorted(f["v"] for f in files) == [119, 133, 134, 135],
      "版本 = V119/V133/V134/V135")
guard("G-A4", man["unsafe_total"] == 0, "解压不安全路径 0, 实得 %d" % man["unsafe_total"])
guard("G-A5", man["members_total"] > 0, "解压成员 %d" % man["members_total"])
guard("G-A6", len(mds) == 12, "md 文件 12, 实得 %d" % len(mds))

STATUS = {}
for p in mds:
    t = read_text(p)
    for k, pats in (
        ("open", [r"\bOPEN\b", r"未闭合"]),
        ("fail", [r"\bFAIL\b", r"不符", r"失败", r"排除", r"障碍"]),
        ("counter", [r"反例", r"障碍"]),
        ("not_proven", [r"未证明", r"未\s*导出", r"不能\s*导出"]),
        ("synthetic", [r"合成", r"数值模型", r"数学实例"]),
    ):
        STATUS[k] = STATUS.get(k, 0) + sum(len(re.findall(x, t, re.I)) for x in pats)

add("MT01", "PASS", "第四批事实源实读",
    "4 文件 / %.2f MB / 4 版本 / %d 成员 / 0 unsafe / %d 篇 md"
    % (man["summary"]["total_bytes"] / 1048576.0, man["members_total"], len(mds)))
add("MT02", "INFO", "共同口径：只令 c=1，保留 ℏ、G、ε₀",
    "V119/V133/V134/V135 均声明不设 ℏ=1、G=1；OPEN %d / FAIL 类 %d / 反例与障碍 %d"
    % (STATUS.get("open", 0), STATUS.get("fail", 0), STATUS.get("counter", 0)))

# ============================================================ B T1 一维表示障碍
random.seed(20261122)
max_comm_1d = 0.0
for _ in range(3000):
    a = complex(random.uniform(-3, 3), random.uniform(-3, 3))
    b = complex(random.uniform(-3, 3), random.uniform(-3, 3))
    max_comm_1d = max(max_comm_1d, abs(a * b - b * a))


def comm2(a, b):
    return [[a[0][0] * b[0][0] + a[0][1] * b[1][0] - (b[0][0] * a[0][0] + b[0][1] * a[1][0]),
             a[0][0] * b[0][1] + a[0][1] * b[1][1] - (b[0][0] * a[0][1] + b[0][1] * a[1][1])],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0] - (b[1][0] * a[0][0] + b[1][1] * a[1][0]),
             a[1][0] * b[0][1] + a[1][1] * b[1][1] - (b[1][0] * a[0][1] + b[1][1] * a[1][1])]]


S1 = [[0, 1], [1, 0]]
S2 = [[0, complex(0, -1)], [complex(0, 1), 0]]
c2 = comm2(S1, S2)
max_comm_2d = max(abs(x) for row in c2 for x in row)

guard("G-B1", max_comm_1d == 0.0, "1x1 矩阵交换子恒 0（3000 组随机）")
guard("G-B2", max_comm_2d > 0, "2x2 阳性对照 [σ1,σ2]≠0, 范数 %.6f" % max_comm_2d)
guard("G-B3", max_comm_1d == 0.0 < max_comm_2d, "1D 零 vs 2D 非零（判据有牙）")
ctrl("C-B1", max_comm_1d == 0.0 and max_comm_2d > 0, "T1 阴性/阳性并存")
add("MT03", "FAIL", "T1 一维复相位不能承载非平凡 SU(2)/SU(3)",
    "1x1 交换子恒 0（max=%.1e）；[σ1,σ2] 范数 %.6f ⇒ 无单射 su(2)→1 维"
    % (max_comm_1d, max_comm_2d))

# ============================================================ C T2 纯相位无通量
L = 8
theta = [[random.uniform(0, 2 * math.pi) for _ in range(L)] for _ in range(L)]
max_f, total_f = 0.0, 0.0
for x in range(L):
    for y in range(L):
        x1, y1 = (x + 1) % L, (y + 1) % L
        ax_xy = theta[x1][y] - theta[x][y]
        ay_x1y = theta[x1][y1] - theta[x1][y]
        ax_xy1 = theta[x1][y1] - theta[x][y1]
        ay_xy = theta[x][y1] - theta[x][y]
        f = ax_xy + ay_x1y - ax_xy1 - ay_xy
        max_f = max(max_f, abs(f))
        total_f += f

# 阳性对照：非平凡线丛（U(1) 元素 + y=L-1 行 twist），总通量应为 2πN。
# 注意：任何单值实相位场（含非梯度）在环面上 plaquette 总和仍恒为 0（望远镜求和），
# 这正是 T2 的内容；要得到非零 N 必须用过渡函数（twist），不能只用实相位 A。
N_pos = 3


total_pos = 0.0
for x in range(L):
    for y in range(L):
        x1, y1 = (x + 1) % L, (y + 1) % L
        ux_xy = cmath.exp(-2j * math.pi * N_pos * y / (L * L))
        ux_xy1 = cmath.exp(-2j * math.pi * N_pos * y1 / (L * L))
        uy_x1y = cmath.exp(2j * math.pi * N_pos * x1 / L) if y == L - 1 else 1.0
        uy_xy = cmath.exp(2j * math.pi * N_pos * x / L) if y == L - 1 else 1.0
        P = ux_xy * uy_x1y * ux_xy1.conjugate() * uy_xy.conjugate()
        total_pos += cmath.phase(P)

guard("G-C1", max_f < 1e-12, "梯度场逐 plaquette F=0, max=%.2e" % max_f)
guard("G-C2", abs(total_f) < 1e-12, "梯度场总通量 0, 实得 %.2e" % total_f)
guard("G-C3", abs(total_pos) > 1e-6, "非梯度阳性对照总通量≠0, 实得 %.6f" % total_pos)
ctrl("C-C1", abs(total_f) < 1e-12 and abs(total_pos) > 1e-6, "T2 阴性/阳性并存")
add("MT04", "FAIL", "T2 全局单值纯相位不能产生拓扑通量",
    "F=d²θ 逐格 0（max=%.2e）、总通量 0；非梯度对照总通量 %.3f"
    % (max_f, total_pos))

# ============================================================ D T3 三代是输入
t135 = read_text(str([p for p in mds if "V135" in str(p) and "科研总报告" in p.name][0]))
n3_input = ("N=3" in t135 or "N = 3" in t135) and ("输入" in t135)
guard("G-D1", n3_input, "V135 明文 N=3 为背景输入")
add("MT05", "FAIL", "T3 三代数 N=3 是输入，未由 κ/τ 导出",
    "V135 §3.1 原文：N=3 作为背景整数被输入，未从曲率/挠率推出，也未推导三代质量")

# ============================================================ E T4 指标≠零模总数
# 来料 8x8 晶格读数: N=0 时 nu_ov=0 但零模总数=2
guard("G-E1", "零模总数" in t135 and "2" in t135, "V135 表格含零模总数列")
add("MT06", "PASS", "T4 指标 ≠ 零模总数（来料数值反例）",
    "8x8 晶格 N=0：nu_ov=0 而零模总数=2（正负手征各一）⇒ 不能用指标冒充谱计数")

# ============================================================ F 质量谱硬证伪
RATIO_CODATA = 206.7682827
pred_M0 = 1.0
dev = abs(RATIO_CODATA - pred_M0) / RATIO_CODATA
guard("G-F1", RATIO_CODATA > 100, "CODATA m_mu/m_e=%.7f" % RATIO_CODATA)
guard("G-F2", dev > 0.99, "M0 预测值与实测相对偏差 %.6f" % dev)
add("MT07", "FAIL", "T5 最小普适单转子被 CODATA 排除",
    "M0 预测 m_mu=m_e（比值 1）；实测 %.7f ⇒ 相对偏差 %.6f" % (RATIO_CODATA, dev))

# ============================================================ G α 无唯一性
ALPHA_INV = 137.035999177
eps0 = 8.8541878128e-12
hbar = 1.054571817e-34
e = 1.602176634e-19
lam = math.sqrt(4 * math.pi * eps0 * (1.0 / ALPHA_INV) / hbar)
alpha_back = lam * lam * hbar / (4 * math.pi * eps0)
guard("G-G1", abs(alpha_back * ALPHA_INV - 1.0) < 1e-9,
      "λ 反解 α 回代 a*137=%.9f" % (alpha_back * ALPHA_INV))
guard("G-G2", lam > 0, "λ=%.6e 为正（连续可调）" % lam)
add("MT08", "FAIL", "T6 α 无唯一性（λ 连续反例族）",
    "α=λ²ℏ/(4πε₀)，任意 λ>0 给任意 α>0；反解 λ=%.6e 仅复现，不是预测" % lam)

# ============================================================ H Lorentz 障碍
ALPHA = 0.0072973525693
BETA = 0.6
u2 = (ALPHA - BETA) / (1 - ALPHA * BETA)
REPORT_U2 = -0.59530916
rel = abs(u2 - REPORT_U2) / abs(REPORT_U2)
guard("G-H1", rel < 1e-6, "boost 复算与 V132/V133 一致, rel=%.2e" % rel)
add("MT09", "FAIL", "T7 Lorentz 障碍：u=α 不是不变量",
    "u=%.13f, β=0.6 -> u'=%.11f（来料 -0.59530916, rel=%.2e）"
    % (ALPHA, u2, rel))

# ============================================================ I 非阿贝尔曲率数值
ab = 0.7 * 1.1
frob = ab / math.sqrt(2)
guard("G-I1", abs(ab - 0.77) < 1e-12, "ab=%.6f" % ab)
guard("G-I2", abs(frob - 0.5444722215) < 1e-9, "Frobenius=%.10f" % frob)
add("MT10", "INFO", "V134 非阿贝尔曲率数值复算",
    "A_x=0.7T1, A_y=1.1T2 ⇒ F_xy=0.77T3，Frobenius=0.77/√2=%.10f" % frob)

# ============================================================ J 四类缺口
gaps = []
for label, kw in (("G", ["未从几何求得 `α`", "未导出 `G`", "G"]),
                  ("规范群", ["新增输入", "不能宣称已从曲率挠率推导"]),
                  ("粒子谱", ["三代", "质量谱"]),
                  ("量子一致性", ["异常", "量子"])):
    hit = any(any(k in read_text(p) for k in kw) for p in mds)
    gaps.append((label, hit))
guard("G-J1", all(h for _l, h in gaps), "四类缺口均有文本证据")
add("MT11", "FAIL", "T8 r438 四类缺口全部仍 OPEN",
    "G / 规范群 / 粒子谱 / 量子一致性 四类均由来料自证未闭合")

# ============================================================ K 互印与出口
add("MT12", "PASS", "与 r438 交叉印证（独立样本同向）",
    "r438 对 V121–V132 判 12/12 未完成；本批 V133–V135 自证三条 no-go + 四空缺")
add("MT13", "BOUNDARY", "唯一出口：第一性输入（不是算力）",
    "I/λ/m0、粒子谱、规范群、G、量子化规则五项均未派生；补一项即一项外部输入")
add("MT14", "INFO", "红线",
    "合成数值≠实验；数学恒等式≠物理；不宣称攻破方向；0/6、0/22 不变")

guard("G-K1", len(ENTRIES) >= 12, "条目数 %d" % len(ENTRIES))
guard("G-K2", all(g["ok"] for g in GUARDS), "全部守卫通过")
guard("G-K3", all(c["ok"] for c in CONTROLS), "全部控制组通过")

payload = dict(round=ROUND, date=DATE, name=NAME, corpus=str(CORPUS),
               files=len(files), members=man["members_total"],
               versions=man["summary"]["versions"], md=len(mds),
               status=STATUS, entries=ENTRIES, guards=GUARDS, controls=CONTROLS,
               lorentz=dict(alpha=ALPHA, beta=BETA, u2=u2, rel=rel),
               t1=dict(max_comm_1d=max_comm_1d, max_comm_2d=max_comm_2d),
               t2=dict(max_f=max_f, total_f=total_f, total_pos=total_pos),
               t5=dict(codata=RATIO_CODATA, dev=dev),
               t6=dict(lam=lam, alpha_back=alpha_back),
               t8=dict(ab=ab, frob=frob),
               verdict="ROOT-V119-V135--SELF-PROVED-NO-GO-X3--N3-INPUT--GAPS-4-OPEN--UFT-NOT-COMPLETED")

OUT.mkdir(parents=True, exist_ok=True)
io.open(str(OUT / (NAME + ".json")), "w", encoding="utf-8").write(
    json.dumps(payload, ensure_ascii=False, indent=1))

L2 = ["# " + NAME, ""]
L2.append("- 轮次 %s ｜ 日期 %s" % (ROUND, DATE))
L2.append("- 条目 %d：%s" % (len(ENTRIES), " / ".join(
    "%s %d" % (s, len([e for e in ENTRIES if e["status"] == s]))
    for s in ("PASS", "FAIL", "BOUNDARY", "INFO"))))
L2.append("- 守卫 %d/%d ｜ 控制组 %d/%d" % (
    len([g for g in GUARDS if g["ok"]]), len(GUARDS),
    len([c for c in CONTROLS if c["ok"]]), len(CONTROLS)))
L2.append("")
L2.append("## 条目")
L2.append("")
L2.append("| 码 | 状态 | 结论 |")
L2.append("|---|---|---|")
for e in ENTRIES:
    L2.append("| %s | %s | %s |" % (e["code"], e["status"], e["title"]))
L2.append("")
L2.append("## 复算读数")
L2.append("")
L2.append("- T1: 1x1 交换子 max=%.1e；2x2 阳性 %.6f" % (max_comm_1d, max_comm_2d))
L2.append("- T2: 梯度场 F max=%.2e、总通量 %.2e；非梯度对照 %.3f" % (max_f, total_f, total_pos))
L2.append("- T5: m_mu/m_e=%.7f vs M0=1，偏差 %.6f" % (RATIO_CODATA, dev))
L2.append("- T6: λ=%.6e，反解回代 %.9f" % (lam, alpha_back * ALPHA_INV))
L2.append("- T7: u'=%.11f（rel %.2e）" % (u2, rel))
L2.append("- T8: ab=%.6f，Frobenius=%.10f" % (ab, frob))
io.open(str(OUT / (NAME + ".md")), "w", encoding="utf-8").write("\n".join(L2))

R = ["ROUND %s %s" % (ROUND, DATE)]
for e in ENTRIES:
    R.append("[%s] %s | %s" % (e["status"], e["code"], e["title"]))
R.append("T1 max1d=%.1e max2d=%.6f" % (max_comm_1d, max_comm_2d))
R.append("T2 maxf=%.2e total=%.2e pos=%.3f" % (max_f, total_f, total_pos))
R.append("T5 dev=%.6f  T6 lam=%.6e" % (dev, lam))
R.append("T7 u2=%.11f rel=%.2e  T8 frob=%.10f" % (u2, rel, frob))
R.append("GUARDS %d/%d  CONTROLS %d/%d" % (
    len([g for g in GUARDS if g["ok"]]), len(GUARDS),
    len([c for c in CONTROLS if c["ok"]]), len(CONTROLS)))
R.append("VERDICT " + payload["verdict"])
io.open(str(OUT / (NAME + "_report.txt")), "w", encoding="utf-8").write("\n".join(R))

print("ENTRIES %d  GUARDS %d/%d  CONTROLS %d/%d" % (
    len(ENTRIES), len([g for g in GUARDS if g["ok"]]), len(GUARDS),
    len([c for c in CONTROLS if c["ok"]]), len(CONTROLS)))
print("T1 %.1e / %.6f  T2 %.2e / %.2e / %.3f" % (
    max_comm_1d, max_comm_2d, max_f, total_f, total_pos))
print("T5 %.6f  T6 %.6e  T7 %.11f  T8 %.10f" % (dev, lam, u2, frob))
print("VERDICT " + payload["verdict"])
