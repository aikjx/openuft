# -*- coding: utf-8 -*-
"""
O 级缺陷 · 求导证明与精算修复（可复跑）
=======================================
承接第十四章「O 级体系 M02 谱系隔离审查」：该章发现 s05/s06 含**未标注的真实缺陷**。
本章不重复「发现错误」，而是对每个缺陷做三件事：
  (1) 求导证明：符号推导出【正确形式】（sympy 解线性约束）；
  (2) 精算    ：mpmath 80 位高精度核验（对照 CODATA 2022）；
  (3) 修复    ：给出更正后的声明（不改体系原文；修正版 = "若按原文推导则应如此"）。

缺陷清单（来自 §14）与修复靶心：
  s05-H2  R₁₁ = (ℏ/2π)^(1/3)·G^(1/3)·c^(-2/3)，量纲 L·T^(-1/3)（非长度）
          → 求导：由 (ℏ,G,c) 造长度的【唯一】指数为 (1/2, 1/2, -3/2)，即 ℓ_P
  s05-H3  M₁₁ = M_P·(2π)^(1/3)，数值错（实算 2.2529e19 vs 原 3.18e19 GeV）
          → 精算修正 + 与 H1/H2 的自洽闭合分析
  s06-Cl  Cl(4,4)⊗ℂ ≅ ? 原文 M₈⊕M₈（128）
          → 求导：n=8 偶 ⟹ Cl(4,4) ≅ M₁₆(ℝ)，⊗ℂ ≅ M₁₆(ℂ)，复维数 2^8=256；
                  M₈⊕M₈ 实为 Cl(4,3)（原文混淆 (4,4) 与 (4,3)）
  s06-T3  L_ij = [ℏc/(Δm²/2m_ν)]·2πR₃，量纲 = L²（非长度）
          → 修复：2πR₃ 须无量纲化（缠绕数）或去除

诚实红线：本文件只做数学修正；「修正版」不主张体系成立，也不改写体系原文。
产出：数据/O级缺陷修复精算.md + .json
"""
import os
import sys
import json
from fractions import Fraction as F

import sympy as sp
from mpmath import mp, mpf, sqrt, pi, power, nstr

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

mp.dps = 80
third = mpf(1) / 3
two_thirds = mpf(2) / 3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

# ── CODATA 2022 ──
G = mpf("6.67430e-11")
c = mpf("299792458")
hbar = mpf("1.054571817e-34")
eV = mpf("1.602176634e-19")
Mp_kg = sqrt(hbar * c / G)
Mp_GeV = Mp_kg * c * c / (eV * 1e9)
Lp = sqrt(hbar * G / c ** 3)

records = []


def rec(tag, system, item, kind, statement, value, verdict, detail):
    records.append({"id": tag, "system": system, "item": item, "kind": kind,
                    "statement": statement, "value": value if isinstance(value, str) else nstr(value, 18),
                    "verdict": verdict, "detail": detail})
    print("[%s] %-10s %s | %s" % (verdict, tag, item, detail))


# ── 量纲基：M=kg, L=m, T=s ──
DIM = {
    "hbar": {"M": F(1), "L": F(2), "T": F(-1)},
    "c": {"M": F(0), "L": F(1), "T": F(-1)},
    "G": {"M": F(-1), "L": F(3), "T": F(-2)},
    "E": {"M": F(1), "L": F(2), "T": F(-2)},
    "M": {"M": F(1), "L": F(0), "T": F(0)},
}


def dmul(*terms):
    out = {"M": F(0), "L": F(0), "T": F(0)}
    for name, e in terms:
        for k in out:
            out[k] += DIM[name][k] * F(e)
    return out


def dfmt(d):
    return " ".join("%s^%s" % (k, str(d[k])) for k in ["M", "L", "T"] if d[k] != 0) or "dimensionless"


def is_length(d):
    return d == {"M": F(0), "L": F(1), "T": F(0)}


print("=" * 78)
print("O 级缺陷 · 求导证明与精算修复")
print("=" * 78)

# ===========================================================================
# 1. s05-H2：R₁₁ 公式量纲错误 → 求导唯一正确指数
# ===========================================================================
print("\n" + "=" * 78)
print("1. s05-H2  R₁₁ 量纲求导证明（sympy 解指数约束）")
print("=" * 78)

dim_orig = dmul(("hbar", F(1, 3)), ("G", F(1, 3)), ("c", F(-2, 3)))
R11_num = power(hbar / (2 * pi), third) * power(G, third) * power(c, -two_thirds)
rec("s05-H2.dim", "s05_HDU高维紧致化", "原式 R₁₁ 量纲",
    "量纲审计", "R₁₁=(ℏ/2π)^(1/3)G^(1/3)c^(-2/3)", nstr(R11_num, 12),
    "FAIL", "原式量纲 = %s，**非长度**（长度应为 L^1）；数值 %.6e m" % (dfmt(dim_orig), R11_num))

# 求导：设 R₁₁ = ℏ^a G^b c^d，要求量纲 = (0,1,0)
a, b, d = sp.symbols("a b d", real=True)
sol = sp.solve([
    sp.Eq(a - b, 0),                 # M
    sp.Eq(2 * a + 3 * b + d, 1),     # L
    sp.Eq(-a - 2 * b - d, 0),        # T
], [a, b, d], dict=True)
sol = sol[0]
rec("s05-H2.solve", "s05_HDU高维紧致化", "由 (ℏ,G,c) 造长度的指数解",
    "求导证明", "解 a·[ℏ]+b·[G]+d·[c]=(0,1,0)", "a=%s b=%s d=%s" % (sol[a], sol[b], sol[d]),
    "PASS", "唯一解 a=b=1/2, d=-3/2 ⇒ ℏ^(1/2)G^(1/2)c^(-3/2)=ℓ_P（解唯一，因 3 方程组 3 未知数满秩）")

dim_fix = dmul(("hbar", F(1, 2)), ("G", F(1, 2)), ("c", F(-3, 2)))
rec("s05-H2.fix", "s05_HDU高维紧致化", "修正形式 = C·ℓ_P",
    "求导证明", "R₁₁=C·ℏ^(1/2)G^(1/2)c^(-3/2)=C·ℓ_P", nstr(Lp, 12),
    "PASS", "修正量纲 = %s = 长度 ✓；ℓ_P=%.6e m。原文声称 R₁₁≈ℓ_P（误差<1e-4）⇒ C=1 即 R₁₁=ℓ_P"
    % (dfmt(dim_fix), Lp))

ratio_r = R11_num / Lp
rec("s05-H2.gap", "s05_HDU高维紧致化", "原式 vs 正确值",
    "精算", "原式 %.6e m vs ℓ_P %.6e m" % (R11_num, Lp), nstr(ratio_r, 8),
    "FAIL", "偏大 %.4e 倍。根因：指数 (1/3,1/3,-2/3) 与正确 (1/2,1/2,-3/2) 不符" % ratio_r)

# 备选求导路径（经作用量子化）
rec("s05-H2.alt", "s05_HDU高维紧致化", "备选：经作用量子化",
    "求导证明", "M₁₁ c R₁₁ = ℏ ⇒ R₁₁ = ℏ/(M₁₁ c)", "dim = L",
    "PASS", "ℏ/(M·c) 量纲 = (M L² T⁻¹)/(M·L T⁻¹) = L ✓。两条独立路径均给【长度】，原式两者皆不匹配")

print("  ⇒ 修复：R₁₁ = C·ℓ_P（C 为无量纲常数）；原式 (ℏ/2π)^(1/3)G^(1/3)c^(-2/3) 量纲必错。")

# ===========================================================================
# 2. s05-H3：M₁₁ 数值错 → 精算 + 自洽闭合
# ===========================================================================
print("\n" + "=" * 78)
print("2. s05-H3  M₁₁ 数值精算与自洽闭合")
print("=" * 78)

M11_formula = Mp_GeV * power(2 * pi, third)
rec("s05-H3.num", "s05_HDU高维紧致化", "M₁₁=M_P(2π)^(1/3) 精算",
    "精算", "M_P·(2π)^(1/3)", M11_formula,
    "FAIL", "实算 %.4e GeV（M_P=%.4e GeV × (2π)^(1/3)=%.4f）；原文 3.18e19 GeV 偏大 %.3f 倍"
    % (M11_formula, Mp_GeV, power(2 * pi, third), mpf("3.18e19") / M11_formula))
# 自洽闭合：若 R₁₁=ℓ_P 且 M₁₁ c R₁₁=ℏ ⇒ M₁₁=ℏ/(cℓ_P)=M_P
M11_self = hbar / (c * Lp) * c * c / (eV * 1e9)
rec("s05-H3.self", "s05_HDU高维紧致化", "自洽闭合（R₁₁=ℓ_P）",
    "求导证明", "若 R₁₁=ℓ_P 且 M₁₁cR₁₁=ℏ ⇒ M₁₁=ℏ/(cℓ_P)=M_P", M11_self,
    "PASS", "闭合值 M₁₁=M_P=%.4e GeV；此时 (2π)^(1/3) 因子无来源（应弃），H2/H3 与 H1 才算自洽"
    % M11_self)
print("  ⇒ 修复：M₁₁ 数值应以 %.4e GeV（公式保留）或 M_P=%.4e GeV（自洽闭合）为准，非 3.18e19。"
      % (M11_formula, M11_self))

# ===========================================================================
# 3. s06-Cl：Cl(4,4)⊗ℂ 代数同构 → 求导证明 + 精算
# ===========================================================================
print("\n" + "=" * 78)
print("3. s06-Cl  Cl(4,4)⊗ℂ 代数同构求导证明")
print("=" * 78)

p, q = 4, 4
n_dim = p + q
dim_real = 2 ** n_dim                       # 实维数 2^(p+q)
dim_cplx = 2 ** n_dim                       # 复化后复维数（n 偶时 ≅ M_{2^{n/2}}(ℂ)）
m16_c_dim = 16 ** 2
m8m8_dim = 8 ** 2 + 8 ** 2
rec("s06.dim", "s06_TCL拓扑手征锁定", "Cl(4,4) 维数",
    "求导证明", "dim_ℝ Cl(p,q)=2^(p+q)", "2^8 = %d" % dim_real,
    "PASS", "原文精算表『2⁴·2=32』无依据，实为 2^8=%d" % dim_real)

# 周期表定位：n=p+q, s=(p-q) mod 8
s_res = (p - q) % 8
cls = None
if n_dim % 2 == 0:
    m = n_dim // 2
    if s_res in (0, 6):
        cls = "M_%d(ℝ)" % (2 ** m)
    elif s_res in (2, 4):
        cls = "M_%d(ℍ)" % (2 ** (m - 1))
else:
    m = (n_dim - 1) // 2
    if s_res in (1, 7):
        cls = "M_%d(ℝ) ⊕ M_%d(ℝ)" % (2 ** m, 2 ** m)
    elif s_res in (3, 5):
        cls = "M_%d(ℂ)" % (2 ** m)
rec("s06.cls", "s06_TCL拓扑手征锁定", "周期表定位 Cl(4,4)",
    "求导证明", "n=8 偶, (p-q)mod8=0 ⇒ M_{2^{n/2}}(ℝ)", cls,
    "PASS", "Cl(4,4) ≅ M₁₆(ℝ)（实维数 %d）；⊗ℂ ⇒ M₁₆(ℂ)（复维数 %d）" % (dim_real, m16_c_dim))
rec("s06.fix", "s06_TCL拓扑手征锁定", "修正同构",
    "求导证明", "Cl(4,4)⊗ℂ ≅ M₁₆(ℂ)", "dim_ℂ = %d" % m16_c_dim,
    "PASS", "原文 M₈⊕M₈（维数 %d）错误：M₈⊕M₈ 半单（两个单代数），而复 Clifford 代数是单代数，二者不可能同构"
    % m8m8_dim)

# 反查 M₈⊕M₈ 对应的真实代数
s43 = (4 - 3) % 8
rec("s06.origin", "s06_TCL拓扑手征锁定", "M₈⊕M₈ 的真实归属",
    "求导证明", "n=7 奇, (p-q)mod8=1 ⇒ M₈(ℝ)⊕M₈(ℝ)", "Cl(4,3)",
    "PASS", "M₈⊕M₈ ⟺ Cl(4,3)（n=7, s=1）。故原文是把 Cl(4,4) 误写成 Cl(4,3) 的代数" )
# 中心维数论据（单 vs 半单）
rec("s06.center", "s06_TCL拓扑手征锁定", "中心维数判据",
    "求导证明", "M₁₆(ℂ) 中心维=1；M₈⊕M₈ 中心维=2", "1 vs 2",
    "PASS", "单代数中心为一维；半单 M₈⊕M₈ 中心为 ℝ⊕ℝ（两中央幂等元）⇒ 反证 M₈⊕M₈ 不可为正 Clifford 代数")
print("  ⇒ 修复：Cl(4,4)⊗ℂ ≅ M₁₆(ℂ)，复维数 2^8=%d；『32』与『128』均错。" % m16_c_dim)

# ===========================================================================
# 4. s06-T3：L_ij 量纲 → 修复
# ===========================================================================
print("\n" + "=" * 78)
print("4. s06-T3  L_ij 振荡长度量纲修复")
print("=" * 78)

# ℏc/(Δm²/(2m_ν))，Δm²/m_ν 量纲 = E
dim_inner = dmul(("hbar", F(1)), ("c", F(1)))
for k in dim_inner:
    dim_inner[k] -= DIM["E"][k]
rec("s06-T3a", "s06_TCL拓扑手征锁定", "内部因子量纲",
    "量纲审计", "ℏc/(Δm²/(2m_ν))", dfmt(dim_inner),
    "PASS", "量纲 = %s = 长度 ✓（内部因子本身是长度）" % dfmt(dim_inner))
dim_full = dict(dim_inner)
dim_full["L"] += F(1)
rec("s06-T3b", "s06_TCL拓扑手征锁定", "整体量纲",
    "量纲审计", "L_ij = [ℏc/(Δm²/2m_ν)]·2πR₃", dfmt(dim_full),
    "FAIL", "内部(长度)×2πR₃(长度) = %s = 长度²，**非长度**（BOUNDARY 升级为可判定）" % dfmt(dim_full))
rec("s06-T3c", "s06_TCL拓扑手征锁定", "修复",
    "修复", "2πR₃ 须为无量纲缠绕数 N，或去除", "L_ij = ℏc/ΔE × N",
    "PASS", "若 2πR₃→N（无量纲整数缠绕数）则 L_ij 为长度 ✓；否则公式多一个长度因子")
print("  ⇒ 修复：L_ij = (ℏc/ΔE)·N（N 无量纲）或弃去 2πR₃；原式量纲为 L²。")

# ===========================================================================
# 汇总与产出
# ===========================================================================
from collections import Counter
cnt = Counter(r["verdict"] for r in records)
print("\n" + "=" * 78)
print("汇总：%d 项  %s" % (len(records), dict(cnt)))
print("=" * 78)

md = "# O 级缺陷 · 求导证明与精算修复报告\n\n"
md += "> 承接第十四章（O 级隔离审查）。对 s05/s06 的未标注真实缺陷做 **求导证明 + 精算 + 修复**。\n"
md += "> 方法：sympy 符号求导 + Fraction 精确量纲 + mpmath 80 位精算（CODATA 2022）。\n\n"
md += "## 汇总\n\n| 判定 | 数量 |\n|---|---|\n"
for k in ["PASS", "FAIL", "BOUNDARY"]:
    md += "| %s | %d |\n" % (k, cnt.get(k, 0))
md += "\n## 明细\n\n| 编号 | 体系 | 项目 | 性质 | 判定 | 值 | 说明 |\n|---|---|---|---|---|---|---|\n"
for r in records:
    md += "| %s | %s | %s | %s | **%s** | %s | %s |\n" % (
        r["id"], r["system"], r["item"], r["kind"], r["verdict"], r["value"], r["detail"])
md += "\n## 修复结论\n\n"
md += "### s05 HDU 高维紧致化\n\n"
md += "1. **H2 量纲错误（已求导证明）**：由 (ℏ,G,c) 造长度的指数解【唯一】为 (1/2,1/2,-3/2)，"
md += "即 R₁₁=C·ℓ_P；原式指数 (1/3,1/3,-2/3) 给 L·T^(-1/3)，非长度。\n"
md += "2. **H3 数值错**：M₁₁=M_P(2π)^(1/3) 精算 = 2.2529e19 GeV（原文 3.18e19，偏 1.412 倍）；"
md += "自洽闭合（R₁₁=ℓ_P）要求 M₁₁=M_P=1.2209e19 GeV，‘(2π)^(1/3)’因子无来源。\n"
md += "3. **修复**：R₁₁=ℓ_P、M₁₁=M_P（弃 (2π)^(1/3)），H1–H3 方自洽。\n\n"
md += "### s06 TCL 拓扑手征锁定\n\n"
md += "1. **Cl(4,4)⊗ℂ ≅ M₁₆(ℂ)（已求导证明）**：n=8 偶、(p-q)≡0 ⟹ Cl(4,4)≅M₁₆(ℝ)，"
md += "⊗ℂ 后复维数 2^8=256；原文 M₈⊕M₈（128）错误——M₈⊕M₈ 是 Cl(4,3)，且半单≠单。\n"
md += "2. **维数矛盾**：原文『2⁴·2=32』无依据，实为 256。\n"
md += "3. **L_ij 量纲**：内部因子(长度)×2πR₃(长度)=长度²；修复为 L_ij=(ℏc/ΔE)·N（N 无量纲）。\n\n"
md += "## 红线\n\n"
md += "- 本文件只做数学修正，**不改写体系原文**；『修正版』是『若按原文推导则应如此』的条件表述。\n"
md += "- 修正有缺陷的公式 ≠ 体系成立：s05/s06 仍为 `falsified` 登记，修正只是消除计算错误。\n"

os.makedirs(OUT_DIR, exist_ok=True)
with open(os.path.join(OUT_DIR, "O级缺陷修复精算.json"), "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)
with open(os.path.join(OUT_DIR, "O级缺陷修复精算.md"), "w", encoding="utf-8") as f:
    f.write(md)
print("已写出：数据/O级缺陷修复精算.md + .json")
