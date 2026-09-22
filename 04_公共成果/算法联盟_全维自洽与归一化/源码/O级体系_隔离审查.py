# -*- coding: utf-8 -*-
"""
O 级体系 · M02 谱系隔离审查（可复跑）
=====================================
对归一化总览中 O 级（欠定/高风险）的 5 个体系 s03/s04/s05/s06/s11 做
「剥离已证伪 GAQ 谱系后是否自身自洽」的第一性审查。

方法（与 method_F 一致）：
  - 量纲分析（Fraction 精确指数运算，基 M/L/T/Q）
  - mpmath 高精度数值核对（对照 CODATA 2022）
  - 代数维数核对（Cl(4,4)⊗C 的复维数）
  - 恒等式/循环判定（区分 L0 恒真、L1 回指、真实数值/量纲冲突）

诚实红线：只报告可判定的事实；不确定处标 BOUNDARY 而非武断。
产出：数据/O级体系隔离审查.md + .json
"""
import os
import sys
import json
from fractions import Fraction as F
from mpmath import mp, mpf, sqrt, pi, power

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
mp.dps = 60
third = mpf(1) / 3
two_thirds = mpf(2) / 3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

# ── CODATA 2022 ──
G = mpf('6.67430e-11')
c = mpf('299792458')
hbar = mpf('1.054571817e-34')
eps0 = mpf('8.8541878128e-12')
eV = mpf('1.602176634e-19')
Mp_kg = sqrt(hbar * c / G)               # Planck mass (kg)
Mp_GeV = Mp_kg * c * c / (eV * 1e9)      # Planck mass in GeV
Lp = sqrt(hbar * G / c ** 3)             # Planck length
Tp = sqrt(hbar * G / c ** 5)             # Planck time

results = []


def add(gid, system, item, statement, verdict, detail):
    results.append({"id": gid, "system": system, "item": item, "statement": statement,
                    "verdict": verdict, "detail": detail})
    print("[%s] %s | %s | %s" % (verdict, gid, item, detail))


# ── 量纲基：M=kg, L=m, T=s, Q=C ──
DIM = {
    "hbar": {"M": F(1), "L": F(2), "T": F(-1), "Q": F(0)},
    "c": {"M": F(0), "L": F(1), "T": F(-1), "Q": F(0)},
    "G": {"M": F(-1), "L": F(3), "T": F(-2), "Q": F(0)},
    "eps0": {"M": F(-1), "L": F(-3), "T": F(2), "Q": F(2)},
    "Lp": {"M": F(0), "L": F(1), "T": F(0), "Q": F(0)},
    "E": {"M": F(1), "L": F(2), "T": F(-2), "Q": F(0)},
}


def dmul(*terms):
    """terms: (name, exponent)"""
    out = {"M": F(0), "L": F(0), "T": F(0), "Q": F(0)}
    for name, e in terms:
        for k in out:
            out[k] += DIM[name][k] * F(e)
    return out


def dfmt(d):
    return " ".join("%s^%s" % (k, str(d[k])) for k in ["M", "L", "T", "Q"] if d[k] != 0) or "dimensionless"


# ======================= s03 GAQ 几何原子 =======================
# T1: M_p c L_p = hbar，但 M_p 的定义就是 hbar/(c L_p)（A5）→ 同义反复
lhs_s03 = (hbar / (c * Lp)) * c * Lp
add("s03-A5/T1", "s03_GAQ几何原子", "M_p c L_p = hbar",
    "M_p ≡ hbar/(c L_p)（A5 定义）代入得 M_p c L_p = hbar",
    "L0",
    "残差 %.3e（机器零）。A5 先定义 M_p=hbar/(cL_p)，T1 再回代，属同义反复（零经验内容），非『数值验证通过』" %
    abs(lhs_s03 - hbar))

# A4: c = L_p/T_p，但 L_p、T_p 用含 G 的普朗克定义
ratio = Lp / Tp
add("s03-A4", "s03_GAQ几何原子", "c = L_p/T_p",
    "以 L_p=sqrt(hbar G/c^3), T_p=sqrt(hbar G/c^5) 代入",
    "L1",
    "L_p/T_p = %.6f，c = %.6f，残差 %.3e。成立——但 L_p、T_p 的定义含 G，而 A5/T2 又主张『G 是导出量』，构成概念循环（L1 回指）" %
    (ratio, c, abs(ratio - c)))

# ======================= s04 IEG 信息熵引力 =======================
add("s04-I1", "s04_IEG信息熵引力", "Einstein 方程 <=> div J_info = 0",
    "J_info = -(1/8piG)G_munu + (1/2)T_munu，证明用 Bianchi + 守恒",
    "L1",
    "nabla^mu J = -(1/8piG)nabla^mu G_munu + (1/2)nabla^mu T_munu；Bianchi 恒有 nabla G=0，"
    "守恒恒有 nabla T=0 → nabla J=0 无条件恒成立（与 Einstein 方程是否成立无关）。"
    "故『<=>』的逆向不成立：nabla J=0 无独立信息，不能反推场方程。属恒等重述，无独立物理内容")

# ======================= s05 HDU 高维紧致化 =======================
# H2: R11 = (hbar/2pi)^(1/3) G^(1/3) c^(-2/3) 声称 ≈ L_p
dim_h2 = dmul(("hbar", F(1, 3)), ("G", F(1, 3)), ("c", F(-2, 3)))
R11_num = power(hbar / (2 * pi), third) * power(G, third) * power(c, -two_thirds)
add("s05-H2a", "s05_HDU高维紧致化", "R11 公式量纲",
    "R11 = (hbar/2pi)^(1/3) G^(1/3) c^(-2/3)（原文定理 H2）",
    "FAIL",
    "量纲 = %s = m·s^(-1/3)，**不是长度**（长度应为 L^1）。原文精算表 H1 称其为紧致化半径并与 L_p 比较，量纲不成立" %
    dfmt(dim_h2))
add("s05-H2b", "s05_HDU高维紧致化", "R11 数值 vs L_p",
    "原文声称 R11 ≈ 1.616e-35 m（恰好 = L_p，误差 < 1e-4）",
    "FAIL",
    "实算 R11 = %.6e m；L_p = %.6e m；比值 = %.4e（偏大 ~1.4e14 倍）。与原文精算表 H1『误差<1e-4』直接矛盾" %
    (R11_num, Lp, R11_num / Lp))
# H3: M11 = M_p (2pi)^(1/3) 声称 3.18e19 GeV
M11_num = Mp_GeV * power(2 * pi, third)
add("s05-H3", "s05_HDU高维紧致化", "M11 数值",
    "M11 = M_p (2pi)^(1/3)，原文声称 ≈ 3.18e19 GeV",
    "FAIL",
    "实算 M11 = %.4e GeV（M_p=%.4e GeV × (2pi)^(1/3)=%.4f）；原文 3.18e19 GeV 偏大 %.3f 倍。公式形式正确，数值错误" %
    (M11_num, Mp_GeV, power(2 * pi, third), mpf('3.18e19') / M11_num))

# ======================= s06 TCL 拓扑手征锁定 =======================
# Cl(4,4)⊗C 复维数
dim_cl44_real = 2 ** 8          # 实维数 2^(p+q)
dim_cl44_cplx = 2 ** 8          # 复化后仍是 2^8（n 偶时 ≅ M_{2^{n/2}}(C)，维数 2^{n/2 * 2}=2^n）
m16_dim = 16 ** 2               # M_16(C) 维数
m8m8_dim = 8 ** 2 + 8 ** 2      # 原文 M8⊕M8 维数
add("s06-A1a", "s06_TCL拓扑手征锁定", "Cl(4,4)⊗C 代数同构",
    "原文定义 4：Cl(4,4)⊗C ≅ M_8(C) ⊕ M_8(C)",
    "FAIL",
    "n=8 偶 ⟹ Cl(4,4)⊗C ≅ M_{2^(8/2)}(C) = M_16(C)（维数 %d）。M_8⊕M_8 维数 %d ≠ %d。"
    "复数 Clifford 代数是单代数，不能是 M_8⊕M_8（半单）。原文用『代数同构』符号不当" %
    (m16_dim, m8m8_dim, dim_cl44_cplx))
add("s06-A1b", "s06_TCL拓扑手征锁定", "|Cl(4,4)| 维数",
    "原文精算表 T1：|Cl(4,4)| 维 = 2^4 · 2 = 32（预测 32，实验 32，误差 0）",
    "FAIL",
    "2^4·2=32 无依据；Cl(4,4) 维数 = 2^(p+q) = 2^8 = %d。且与同文定义 4 的 M_8⊕M_8（%d）自相矛盾（32 vs 128 vs 256 三者互斥）" %
    (dim_cl44_real, m8m8_dim))
# T3: L12 量纲
dim_t3_inner = dmul(("hbar", F(1)), ("c", F(1)), ("E", F(-1)))  # hbar*c / (Δm²/(2m_ν))，Δm²/m_ν 量纲 = E
dim_t3 = dict(dim_t3_inner)
dim_t3["L"] += 1  # × 2π R3
add("s06-T3", "s06_TCL拓扑手征锁定", "L12 振荡长度量纲",
    "L_ij = [hbar c/(Δm²/(2 m_ν))] · 2π R_3",
    "BOUNDARY",
    "内部 hbar c/(Δm²/(2m_ν)) 量纲 = %s = 长度；再乘 2π R_3（长度）⟹ %s = 长度²，非长度。"
    "公式末尾多乘一个长度因子（若 R_3 无量纲才自洽）。原文未说明 2π R_3 的无量纲化，判定为『量纲可疑，需澄清』" %
    (dfmt(dim_t3_inner), dfmt(dim_t3)))

# ======================= s11 GMUFT 几何自由度 =======================
dim_qm = dmul(("eps0", F(1, 2)), ("G", F(1, 2)))
QM = sqrt(4 * pi * eps0 * G)
e_me = mpf('1.75882001076e11')  # 电子荷质比 C/kg
add("s11-A4a", "s11_GMUFT几何自由度", "Q/M 量纲",
    "Q/M = sqrt(4 pi eps0 G)",
    "PASS",
    "量纲 = %s = C·kg^-1，与荷质比 [Q/M] 匹配（原文 4.3 节已自检）" % dfmt(dim_qm))
add("s11-A4b", "s11_GMUFT几何自由度", "Q/M 物理对应",
    "该对偶荷质比是否对应基本粒子",
    "BOUNDARY",
    "sqrt(4 pi eps0 G) = %.6e C/kg；电子荷质比 = %.6e C/kg，相差 %.3e 倍。原文 8.1 节 OPEN-2 **已诚实标注**"
    "『对偶定义式、不对应任何已知粒子』——属已披露的欠定，非隐藏缺陷" %
    (QM, e_me, e_me / QM))

# ── 汇总 ──
from collections import Counter
cnt = Counter(r["verdict"] for r in results)
print("\n=== 汇总：%d 项 ===" % len(results), dict(cnt))

md = "# O 级体系 · M02 谱系隔离审查报告\n\n"
md += "> 目的：判定 O 级 5 体系（s03/s04/s05/s06/s11）剥离已证伪 GAQ/G（M02）谱系后是否自身自洽。\n"
md += "> 方法：Fraction 精确量纲 + mpmath 60 位数值（CODATA 2022）+ 代数维数核对。\n\n"
md += "判定口径：**FAIL**=与自身声明矛盾的真实缺陷；**BOUNDARY**=需澄清或已诚实标注的欠定；"
md += "**L0**=同义反复（恒真零内容）；**L1**=循环/回指；**PASS**=成立。\n\n"
md += "## 汇总\n\n| 判定 | 数量 |\n|---|---|\n"
for k in ["FAIL", "BOUNDARY", "L1", "L0", "PASS"]:
    md += "| %s | %d |\n" % (k, cnt.get(k, 0))
md += "\n## 明细\n\n| 编号 | 体系 | 检查项 | 判定 | 说明 |\n|---|---|---|---|---|\n"
for r in results:
    md += "| %s | %s | %s | **%s** | %s |\n" % (r["id"], r["system"], r["item"], r["verdict"], r["detail"])
md += "\n## 隔离审查结论\n\n"
md += "- **s03**：A5/T1 为同义反复（L0），A4 为含 G 定义的概念循环（L1）→ 隔离 M02 后**可验证内容为零**，"
md += "原文『100% 数值与量纲验证通过』属 H01c 循环自证，非独立证据。仍为自洽（未产生硬矛盾）。\n"
md += "- **s04**：I1 的『等价』实为恒等重述（nabla J=0 无条件成立）→ 自洽但无独立物理内容（欠定）。\n"
md += "- **s05**：**H2 量纲错误 + 数值偏 ~1.4e14 倍；H3 数值错误**——两处均与自身精算表『误差<1e-4/0』直接矛盾，"
md += "是**独立于 M02 的真实缺陷**（应登记）。\n"
md += "- **s06**：**Cl(4,4)⊗C 代数同构错误（应 M_16(C)）+ 维数自相矛盾（32/128/256 三者互斥）**，"
md += "T3 量纲可疑——为**独立于 M02 的真实缺陷**（应登记）。\n"
md += "- **s11**：一阶恒等式（g=rω²、dg/dr=-2ω²）正确，唯一非标准式 Q/M=sqrt(4 pi eps0 G) 在原文 8.1 节**已诚实标注**"
md += "为对偶定义式、不对应任何粒子 → 属**已披露的欠定**，无隐藏缺陷。\n\n"
md += "**净结论**：O 级 5 体系中 3 个（s03/s04/s11）的欠定是内在且（部分）已诚实标注的；"
md += "**2 个（s05/s06）含未标注的真实计算缺陷**，应在各自体系登记 `falsified` 并升级为 C 级。\n"

os.makedirs(OUT_DIR, exist_ok=True)
json.dump(results, open(os.path.join(OUT_DIR, "O级体系隔离审查.json"), "w", encoding='utf-8'),
          ensure_ascii=False, indent=2)
open(os.path.join(OUT_DIR, "O级体系隔离审查.md"), "w", encoding='utf-8').write(md)
print("已写出：数据/O级体系隔离审查.md + .json")
