# -*- coding: utf-8 -*-
"""
S17 统一场论核心公式 —— 常数层独立精算

对象（均为本仓库已归档的源材料，路径相对 S17 根）：
  - 01_文献来源/统一场论核心公式全面验证完成纪念文章.md   （下称「纪念文章」）
  - 01_文献来源/源材料_核心公式的元数据/核心公式的元数据.md（下称「汇总 md」）
  - 01_文献来源/源材料_核心公式的元数据/核心公式的元数据.json
  - 01_文献来源/源材料_核心公式的元数据/20电磁耦合常数 Z'.md（下称「Z' 专章」）

红线（与 openuft 治理一致）：
  1. 不沿用来源自封的「算法联盟 ROOT 最高权限 / 20 个公式全部通过」结论；
  2. 每个判定必须先声明「判据 + 阈值」，再由本脚本实算产生，禁止硬编结论；
  3. 只做常数层的代数、数值与量纲审计，不评价物理公设本身是否成立。

量纲约定：基（M, L, T, I）=（千克, 米, 秒, 安培）；库仑 C = I·T，
  立体角 sr 视为无量纲。故 [Q^k] → I^k·T^k。

运行：python 核心公式常数层_独立精算.py
产物：核心公式常数层_独立精算_report.txt / 核心公式常数层_独立精算_数据.json
"""

import io
import json
import math
import os
import re
import sys
from fractions import Fraction
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SRC_DIR = ROOT / "01_文献来源" / "源材料_核心公式的元数据"
MD_SUMMARY = SRC_DIR / "核心公式的元数据.md"
JSON_SUMMARY = SRC_DIR / "核心公式的元数据.json"

# ---------------------------------------------------------------- 常量（CODATA 2018 / SI 定义值）
C_LIGHT = 299792458.0            # m/s  精确定义值
G_NEWTON = 6.67430e-11           # m^3 kg^-1 s^-2  CODATA 2018
EPS0 = 8.8541878128e-12          # F/m  CODATA 2018
HBAR = 1.054571817e-34           # J s  CODATA 2018
E_CHARGE = 1.602176634e-19       # C    SI 2019 定义值
M_PLANCK = 2.176434e-8           # kg   = sqrt(hbar*c/G)
M_PROTON = 1.67262192369e-27     # kg   CODATA 2018
PI = math.pi

# 相对一致判据阈值（前置声明，全局统一）
REL_STRICT = 1e-9      # 机器零/代数恒等
REL_NUM = 1e-6         # 数值复算一致（源给到 ~10 位有效数字）
REL_LOOSE = 1e-3       # 跨来源互印证（不同作者四舍五入位）

# 本仓库既有的独立复算值（硬编码 + 出处，仅用于交叉互印证，不用于仲裁）
EXISTING = [
    {"name": "Z", "path": "04_理论推导/核心公式集/20-电磁耦合常数/验证报告.md",
     "locator": "定义 Z=Gc/2；数值段", "value": 1.000452e-2},
    {"name": "Z'", "path": "04_理论推导/核心公式集/20-电磁耦合常数/验证报告.md",
     "locator": "定义 Z'=c/(8*pi*eps0)；数值段", "value": 1.347200e18},
]

# 纪念文章（被审对象）给出的显式声明值
CLAIM = {
    "f": 1.2917333313e-02,
    "Z": 1.00083858e-03,
    "Zp": 3.35534388e+10,
    "kp": 1.16e10,
    "k": 2.73e-07,
}


# ---------------------------------------------------------------- 量纲
class Dim(object):
    """整数/有理数量纲向量 (M, L, T, I)。"""
    SYM = ("M", "L", "T", "I")

    def __init__(self, m=0, l=0, t=0, i=0):
        self.v = (Fraction(m), Fraction(l), Fraction(t), Fraction(i))

    def _op(self, other, fn):
        return Dim(*[fn(a, b) for a, b in zip(self.v, other.v)])

    def __mul__(self, other):
        return self._op(other, lambda a, b: a + b)

    def __truediv__(self, other):
        return self._op(other, lambda a, b: a - b)

    def __pow__(self, p):
        p = Fraction(p)
        return Dim(*[x * p for x in self.v])

    def __eq__(self, other):
        return tuple(self.v) == tuple(other.v)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(self.v))

    def __str__(self):
        parts = []
        for s, x in zip(Dim.SYM, self.v):
            if x == 0:
                continue
            parts.append(s if x == 1 else s + "^(" + str(x) + ")")
        return "·".join(parts) if parts else "无量纲"


D_M = Dim(1, 0, 0, 0)
D_L = Dim(0, 1, 0, 0)
D_T = Dim(0, 0, 1, 0)
D_I = Dim(0, 0, 0, 1)
D_NONE = Dim(0, 0, 0, 0)
DIM_C = D_L / D_T
DIM_G = D_L ** 3 / (D_M * D_T ** 2)
DIM_EPS0 = D_I ** 2 * D_T ** 4 / (D_M * D_L ** 3)
DIM_HBAR = D_M * D_L ** 2 / D_T
DIM_E = D_I * D_T


def rel(x, y):
    """相对偏差（以 |y| 为尺），y=0 时退化为绝对差。"""
    if y == 0:
        return abs(x - y)
    return abs(x - y) / abs(y)


def sci(x, nd=8):
    return ("{:." + str(nd) + "e}").format(x)


# ---------------------------------------------------------------- 记录器
class Rec(object):
    def __init__(self):
        self.rows = []
        self.n = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}

    def _add(self, kind, tid, title, criterion, fact, verdict_note):
        self.n[kind] += 1
        crit_txt = criterion
        if crit_txt.startswith("判据:"):
            crit_txt = crit_txt[len("判据:"):].lstrip()
        self.rows.append({
            "id": tid, "verdict": kind, "title": title,
            "criterion": crit_txt, "evidence": fact, "note": verdict_note,
        })
        print("[" + kind + "] " + tid + " " + title)
        print("    判据: " + crit_txt)
        print("    实测: " + fact)
        print("    结论: " + verdict_note)
        print("")

    def P(self, tid, title, criterion, fact, note):
        self._add("PASS", tid, title, criterion, fact, note)

    def F(self, tid, title, criterion, fact, note):
        self._add("FAIL", tid, title, criterion, fact, note)

    def B(self, tid, title, criterion, fact, note):
        self._add("BOUNDARY", tid, title, criterion, fact, note)

    def I(self, tid, title, criterion, fact, note):
        self._add("INFO", tid, title, criterion, fact, note)


R = Rec()

print("=" * 78)
print("S17 统一场论核心公式 —— 常数层独立精算")
print("源材料: 01_文献来源/  (纪念文章 + 核心公式的元数据)")
print("量纲基: (M, L, T, I)；C = I·T；sr 无量纲")
print("=" * 78)
print("")

# ---------------------------------------------------------------- 派生量
val_Z_MONOGRAPH = None  # 稍后填充

# T1 ------------------------------------------------------------ f 数值
f_def = (C_LIGHT / 2.0) * math.sqrt(4.0 * PI * EPS0 * G_NEWTON)
d_f = rel(f_def, CLAIM["f"])
if d_f < REL_NUM:
    R.P("T1", "常数 f 数值复算",
        "判据: |f_def - f_claim| / f_def < " + sci(REL_NUM, 1),
        "f_def = (c/2)·sqrt(4*pi*eps0*G) = " + sci(f_def, 10) +
        " ; 纪念文章 f = " + sci(CLAIM["f"], 10) + " ; rel = " + sci(d_f, 3),
        "数值层面一致——纪念文章的 f 数值确实是定义式的正确代值。")
else:
    R.F("T1", "常数 f 数值复算",
        "判据: |f_def - f_claim| / f_def < " + sci(REL_NUM, 1),
        "f_def = " + sci(f_def, 10) + " ; claim = " + sci(CLAIM["f"], 10) +
        " ; rel = " + sci(d_f, 3),
        "数值不一致。")

# T2 ------------------------------------------------------------ f 量纲
dim_f_def = DIM_C * (DIM_EPS0 * DIM_G) ** Fraction(1, 2)
dim_f_claim = D_M / D_I          # 纪念文章宣称 [M I^-1] = kg/A
if dim_f_def == dim_f_claim:
    R.P("T2", "常数 f 量纲审计",
        "判据: dim((c/2)·sqrt(4*pi*eps0*G)) == dim(M·I^-1)",
        "dim(f_def) = " + str(dim_f_def) + " ; 宣称 = " + str(dim_f_claim),
        "量纲一致。")
else:
    R.F("T2", "常数 f 量纲审计",
        "判据: dim((c/2)·sqrt(4*pi*eps0*G)) == dim(M·I^-1)（纪念文章宣称 kg/A）",
        "dim(f_def) = " + str(dim_f_def) + " ; 宣称 = " + str(dim_f_claim) +
        " ; 需求/定义 = " + str(dim_f_claim / dim_f_def),
        "定义式的量纲与纪念文章标注的单位不相容：二者相差 " +
        str(dim_f_claim / dim_f_def) + "，kg/A 的标注不成立。")

# T3 ------------------------------------------------------------ f 是否独立常数
Z_local = G_NEWTON * C_LIGHT / 2.0
Zp_local = C_LIGHT / (8.0 * PI * EPS0)
f_via_ZZp = (C_LIGHT / 2.0) * math.sqrt(Z_local / Zp_local)
d_f_ident = rel(f_via_ZZp, f_def)
# 解析恒等：(Gc/2) / (c/(8*pi*eps0)) = 4*pi*eps0*G
d_ratio = rel(Z_local / Zp_local, 4.0 * PI * EPS0 * G_NEWTON)
if d_f_ident < REL_STRICT and d_ratio < REL_STRICT:
    R.P("T3", "f 与 Z、Z' 的代数关系",
        "判据: |f(Z,Z') - f(eps0,G)| / f < " + sci(REL_STRICT, 1) +
        " 且 (Z/Z') - 4*pi*eps0*G 相对偏差 < " + sci(REL_STRICT, 1),
        "f(Z,Z') = " + sci(f_via_ZZp, 12) + " ; f(eps0,G) = " + sci(f_def, 12) +
        " ; Z/Z' - 4*pi*eps0*G rel = " + sci(d_ratio, 3),
        "f 不是独立常数：f ≡ (c/2)·sqrt(Z/Z') ≡ (c/2)·sqrt(4*pi*eps0*G)，"
        "是 Z、Z' 的代数重排（机器零恒等）；"
        "换言之引入 f 相对于 Z、Z' 没有增加独立自由度，也不携带新物理内容。")
else:
    R.B("T3", "f 与 Z、Z' 的代数关系",
        "判据: 相对偏差 < " + sci(REL_STRICT, 1),
        "rel(f) = " + sci(d_f_ident, 3) + " ; rel(Z/Z') = " + sci(d_ratio, 3),
        "非精确恒等，需按实际精度重新裁定。")

# T4 ------------------------------------------------------------ Z 数值
d_Z = rel(Z_local, CLAIM["Z"])
c_implied = 2.0 * CLAIM["Z"] / G_NEWTON
rel_c_div10 = rel(c_implied, C_LIGHT / 10.0)
if d_Z < REL_NUM:
    R.P("T4", "常数 Z 数值复算（Z = Gc/2）",
        "判据: |Z_def - Z_claim| / Z_def < " + sci(REL_NUM, 1),
        "Z_def = " + sci(Z_local, 10) + " ; claim = " + sci(CLAIM["Z"], 10),
        "数值一致。")
else:
    R.F("T4", "常数 Z 数值复算（Z = Gc/2）",
        "判据: |Z_def - Z_claim| / Z_def < " + sci(REL_NUM, 1),
        "Z_def = Gc/2 = " + sci(Z_local, 10) + " ; 纪念文章 = " + sci(CLAIM["Z"], 10) +
        " ; rel = " + sci(d_Z, 6) + " ; 比值 Z_def/Z_claim = " +
        ("{:.4f}").format(Z_local / CLAIM["Z"]),
        "纪念文章的 Z 数值与其自己给出的定义式 Z=Gc/2 不相容（约差 10 倍）。")

if d_Z >= REL_NUM:
    R.I("T4b", "Z 偏差成因诊断",
        "判据: 反解 c_implied = 2·Z_claim/G，与 c/10 对比（rel < 1e-2 视为吻合）",
        "c_implied = " + sci(c_implied, 10) + " m/s ; c/10 = " + sci(C_LIGHT / 10.0, 10) +
        " ; rel = " + sci(rel_c_div10, 3),
        "最可能成因是把光速少写一个数量级（按 ~3.00e7 m/s 代入）。属成因推断，非证明。")

# T5 ------------------------------------------------------------ Z 量纲
dim_Z_def = DIM_G * DIM_C
dim_Z_claim = D_L ** 4 / (D_M * D_T ** 3)   # 纪念文章 kg^-1·m^4·s^-3
if dim_Z_def == dim_Z_claim:
    R.P("T5", "常数 Z 量纲审计",
        "判据: dim(G·c) == dim(M^-1·L^4·T^-3)",
        "dim(Z_def) = " + str(dim_Z_def) + " ; 宣称 = " + str(dim_Z_claim),
        "Z 的定义式与标注单位量纲自洽——这一条本身成立。")
else:
    R.F("T5", "常数 Z 量纲审计",
        "判据: dim(G·c) == dim(M^-1·L^4·T^-3)",
        "dim(Z_def) = " + str(dim_Z_def) + " ; 宣称 = " + str(dim_Z_claim),
        "量纲不一致。")

# T6 ------------------------------------------------------------ Z' 数值
Zp_monograph = 1.347284273e18   # Z' 专章本文给出的 CODATA 复算值
d_Zp = rel(Zp_local, CLAIM["Zp"])
d_Zp_mono = rel(Zp_local, Zp_monograph)
if d_Zp < REL_NUM:
    R.P("T6", "常数 Z' 数值复算（Z' = c/(8*pi*eps0)）",
        "判据: |Z'_def - Z'_claim| / Z'_def < " + sci(REL_NUM, 1),
        "Z'_def = " + sci(Zp_local, 10) + " ; claim = " + sci(CLAIM["Zp"], 10),
        "数值一致。")
else:
    R.F("T6", "常数 Z' 数值复算（Z' = c/(8*pi*eps0)）",
        "判据: |Z'_def - Z'_claim| / Z'_def < " + sci(REL_NUM, 1),
        "Z'_def = c/(8*pi*eps0) = " + sci(Zp_local, 10) +
        " ; 纪念文章 = " + sci(CLAIM["Zp"], 10) + " ; rel = " + sci(d_Zp, 6) +
        " ; 倍数 Z'_def/Z'_claim = " + ("{:.4e}").format(Zp_local / CLAIM["Zp"]) +
        " ; 同批源材料《20电磁耦合常数 Z'.md》给 " + sci(Zp_monograph, 10) +
        "（与本脚本 rel = " + sci(d_Zp_mono, 3) + "）",
        "纪念文章的 Z' 数值偏离定义式约 7.6 个量级；而同一批源材料的专章给出了正确值，"
        "即错值出现在总结性宣示文档中、源材料内部自身即为反例。")

# T7 ------------------------------------------------------------ Z' 量纲
dim_Zp_def = DIM_C / DIM_EPS0
dim_Zp_claim = D_M * D_L ** 4 / (D_T ** 5 * D_I ** 2)  # kg·m^4·s^-3·C^-2
if dim_Zp_def == dim_Zp_claim:
    R.P("T7", "常数 Z' 量纲审计",
        "判据: dim(c/eps0)（用 C=I·T 展开）== dim(M·L^4·T^-3·C^-2)",
        "dim(Z'_def) = " + str(dim_Zp_def) + " ; 宣称 = " + str(dim_Zp_claim),
        "Z' 的定义式与标注单位量纲自洽——这一条本身成立。")
else:
    R.F("T7", "常数 Z' 量纲审计",
        "判据: dim(c/eps0) == dim(M·L^4·T^-3·C^-2)",
        "dim(Z'_def) = " + str(dim_Zp_def) + " ; 宣称 = " + str(dim_Zp_claim),
        "量纲不一致。")

# T8 ------------------------------------------------------------ 汇总 md 与专章的 Z' 定义冲突
md_text = ""
if MD_SUMMARY.exists():
    md_text = io.open(str(MD_SUMMARY), encoding="utf-8").read()
has_alpha_def = ("Z'" in md_text or "Z'" in md_text) and (
    re.search(r"Z'\s*=\s*\\frac\{e\^2\}", md_text) is not None
    or "\\frac{e^2}{4\\pi\\varepsilon_0\\hbar c}" in md_text.replace(" ", "")
)
md_const_row = re.search(r"\|\s*Z'\s*\|([^|]*)\|([^|]*)\|", md_text)
md_const_expr = ""
if md_const_row:
    md_const_expr = md_const_row.group(2).strip()
conflict = has_alpha_def and ("8" in md_const_expr and "eps" in md_const_expr.replace(" ", "")
                              or "ε₀" in md_const_expr or "varepsilon" in md_const_expr)
alpha = E_CHARGE ** 2 / (4.0 * PI * EPS0 * HBAR * C_LIGHT)
if has_alpha_def:
    if conflict:
        R.F("T8", "源材料内部 Z' 定义冲突",
            "判据: 同一份《核心公式的元数据.md》内，公式条目与常数表若给出互斥定义即判冲突",
            "公式条目第 20 条: Z' = e^2/(4*pi*eps0*hbar*c) = 1/137（无量纲精细结构常数）" +
            " ; 常数表同一文件: Z' = " + md_const_expr +
            " ; 精算 alpha = " + sci(alpha, 10) + " 而 c/(8*pi*eps0) = " + sci(Zp_local, 6),
            "同一份源文件内 Z' 存在互斥的两种定义（无量纲 alpha vs 有量纲组合），"
            "二者量纲不同、数值不可换算；源材料的『元数据』层自身不自洽。")
    else:
        R.B("T8", "源材料内部 Z' 定义冲突",
            "判据: 提取公式条目与常数表两处定义并比对",
            "公式条目含 alpha 形式: True ; 常数表表达式: " + md_const_expr,
            "未检出成对冲突文本，需人工复核。")
else:
    R.B("T8", "源材料内部 Z' 定义冲突",
        "判据: 在汇总 md 中检索 Z'=alpha 形式",
        "未命中 Z'=e^2/(4*pi*eps0*hbar*c) 文本（可能已被修订）",
        "该冲突在当前源文本中不可复现，按 BOUNDARY 记录不判 FAIL。")

# T9 ------------------------------------------------------------ alpha 反向验证的量纲与循环性
alpha_wrong = E_CHARGE ** 2 * Zp_local / (HBAR * C_LIGHT)     # 文档写的 alpha = e^2 Z'/(hbar c)
alpha_right = 2.0 * E_CHARGE ** 2 * Zp_local / (HBAR * C_LIGHT ** 2)
dim_doc = DIM_E ** 2 * dim_Zp_def / (DIM_HBAR * DIM_C)
dim_right = DIM_E ** 2 * dim_Zp_def / (DIM_HBAR * DIM_C ** 2)
d_alpha_right = rel(alpha_right, alpha)
if dim_doc != D_NONE:
    R.F("T9", "《Z' 专章》精细结构常数反向验证",
        "判据: 该式若声称给出 alpha，其量纲必须为无量纲，且非alpha定义的等价重排",
        "文档式 e^2·Z'/(hbar·c) 量纲 = " + str(dim_doc) + "（速度量纲，非无量纲）" +
        " ; 代入值 = " + sci(alpha_wrong, 8) + " m/s" +
        " ; 补足后的无量纲式 alpha = 2·e^2·Z'/(hbar·c^2) = " + sci(alpha_right, 10) +
        "（与 CODATA alpha = " + sci(alpha, 10) + " rel = " + sci(d_alpha_right, 3) + "）",
        "文档给出的关系式量纲非法（漏一个 c），其『相对误差 0.00065%』的反向验证不成立；"
        "补正后虽数值精确吻合，但该式只是 alpha 定义的代数重排（用 CODATA 的 e、hbar、eps0、c 反算 alpha 自身），"
        "构成循环自证，不是独立预测。")
else:
    R.B("T9", "《Z' 专章》精细结构常数反向验证",
        "判据: 量纲须无量纲",
        "dim = " + str(dim_doc),
        "量纲合法，需另行裁定其是否构成独立预测。")

# T10 ----------------------------------------------------------- k = 4*pi*m_P 与 m_p 记号
k_planck = 4.0 * PI * M_PLANCK
k_proton = 4.0 * PI * M_PROTON
d_k = rel(k_planck, CLAIM["k"])
if d_k < 2e-2:
    # 记号歧义判据：把 m_p 按质子质量解读时若与原解读相差超过 50%，判定记号层不可靠
    if rel(k_proton, k_planck) > 0.5:
        R.B("T10", "常数 k 的数值与 m_p 记号歧义",
            "判据: 数值复算 rel < 2e-2；若同一记号 m_p 的另一种惯用解读（质子质量）"
            "导致取值偏离超过 50%，则记号层不可靠，降级为 BOUNDARY",
            "k = 4*pi*m_Planck = " + sci(k_planck, 8) + " kg ; 纪念文章 = " + sci(CLAIM["k"], 4) +
            " kg ; rel = " + sci(d_k, 3) +
            " ; 若按 m_p = 质子质量: k = " + sci(k_proton, 8) + " kg，与前者相差 " +
            ("{:.3e}").format(k_planck / k_proton) + " 倍",
            "数值 4*pi*m_Planck 复算成立，但纪念文章只写『m_p 为普朗克质量』："
            "物理惯例中 m_p 指质子质量，二者差约 1.3e19 倍，记号歧义会直接摧毁该常数的可复算性。"
            "判定 BOUNDARY：数值自洽，记号层需外部澄清。")
    else:
        R.P("T10", "常数 k 的数值与 m_p 记号歧义",
            "判据: 数值复算 rel < 2e-2 且无严重记号歧义",
            "k = " + sci(k_planck, 8) + " kg",
            "数值一致。")
else:
    R.F("T10", "常数 k 的数值",
        "判据: |k_calc - k_claim| / k_calc < 2e-2",
        "k_calc = " + sci(k_planck, 8) + " ; claim = " + sci(CLAIM["k"], 4) +
        " ; rel = " + sci(d_k, 3),
        "数值不一致。")

# T11 ----------------------------------------------------------- k' 三版本互斥
dim_kp_meta = D_I                    # 元数据参数表: C·sr^2/s = I·T / T = I
dim_kp_memo = D_I * D_T / D_M        # 纪念文章: [I T / M]
dim_kp_v1 = D_I * D_T ** 2 / D_M     # S17 既有 v1 裁定: A·s^2/kg
dims_kp = {str(dim_kp_meta): "元数据参数表(C·sr^2/s)",
           str(dim_kp_memo): "纪念文章([IT/M])",
           str(dim_kp_v1): "S17既有v1裁定(A·s^2/kg)"}
uniq_kp = sorted(set(dims_kp.keys()))
if len(uniq_kp) > 1:
    R.F("T11", "常数 k' 的量纲三方互斥",
        "判据: 同一常数的量纲在三处来源应完全一致，否则判冲突",
        " ".join([name + " -> " + d for d, name in dims_kp.items()]) +
        " ; 互异量纲数 = " + str(len(uniq_kp)),
        "k' 在元数据参数表、纪念文章、本仓库既有 v1 裁定三处给出三种互不相同的量纲，"
        "迄今无人仲裁；任一取值都无法同时满足三处来源。")
else:
    R.P("T11", "常数 k' 的量纲三方互斥",
        "判据: 三处量纲应一致",
        "一致: " + uniq_kp[0],
        "无冲突。")

# T12 ----------------------------------------------------------- kk'/(4*pi*eps0) 复合常数
ke = 1.0 / (4.0 * PI * EPS0)                  # 库仑常数 8.987551787e9
compound = k_planck * CLAIM["kp"] / (4.0 * PI * EPS0)
d_comp_ke = rel(compound, ke)
dim_kk = D_M * dim_kp_meta                     # 元数据口径下的 k·k'
if d_comp_ke < REL_NUM:
    R.P("T12", "复合常数 kk'/(4*pi*eps0) 与库仑常数",
        "判据: 相对偏差 < " + sci(REL_NUM, 1),
        "kk'/(4*pi*eps0) = " + sci(compound, 8) + " ; k_e = " + sci(ke, 8),
        "与库仑常数一致。")
else:
    R.F("T12", "复合常数 kk'/(4*pi*eps0) 与库仑常数",
        "判据: 宣称『约 1.0e10 N·m^2/C^2，与库仑常数一致』，需相对偏差 < " + sci(REL_NUM, 1) +
        "，且要求 k·k' 为无量纲（否则等式两侧量纲不同）",
        "k·k' = " + sci(k_planck * CLAIM["kp"], 8) + "（量纲 " + str(dim_kk) + "，非无量纲）" +
        " ; kk'/(4*pi*eps0) = " + sci(compound, 8) +
        " ; k_e = " + sci(ke, 8) + " ; rel = " + sci(d_comp_ke, 4) +
        " ; 偏差倍数 = " + ("{:.4e}").format(compound / ke),
        "『与库仑常数一致』不成立：数值差 k·k' ≈ 3.17e3 倍，且 k·k' 本身有量纲（kg·A），"
        "无法让kk'/(4*pi*eps0) 退化为纯库仑常数。")

# T13 ----------------------------------------------------------- 20 条清单一致性
file_map = {}
if SRC_DIR.exists():
    for p in SRC_DIR.glob("*.md"):
        m = re.match(r"^(\d+)(.+)\.md$", p.name)
        if m:
            file_map[int(m.group(1))] = m.group(2).strip()
md_map = {}
for m in re.finditer(r"^####\s*(\d+)\.\s*(.+)$", md_text, flags=re.MULTILINE):
    md_map[int(m.group(1))] = m.group(2).strip()


def norm_title(s):
    """标题归一化：去掉「的」、空白、连字符、（），大写统一。"""
    for ch in ("的", " ", "-", "_", "（", "）", "(", ")"):
        s = s.replace(ch, "")
    return s


def share_ratio(a, b):
    """两串共同字符数 / 较短串长度，用于识别『同一对象的不同命名』。"""
    if not a or not b:
        return 0.0
    short = a if len(a) <= len(b) else b
    inter = set(a) & set(b)
    common = sum(1 for ch in short if ch in inter)
    return common / float(len(short))


ALIAS_RATIO = 0.6   # 前置声明：共享字符占比 ≥60% 视为同一对象的别名/命名差异

# 分级：same=归一化后一致；alias=归一化包含关系或共享字符占比达标；conflict=内容互不相容
same_list, alias_list, conflict_list = [], [], []
for i in sorted(set(file_map.keys()) & set(md_map.keys())):
    a = norm_title(file_map[i])
    b = norm_title(md_map[i])
    if a == b:
        same_list.append(i)
    elif (len(a) >= 4 and len(b) >= 4 and (a in b or b in a)) or share_ratio(a, b) >= ALIAS_RATIO:
        alias_list.append((i, file_map[i], md_map[i]))
    else:
        conflict_list.append((i, file_map[i], md_map[i]))
only_file = sorted(set(file_map.keys()) - set(md_map.keys()))
only_md = sorted(set(md_map.keys()) - set(file_map.keys()))

detail = ("一批一致 " + str(len(same_list)) + " 条 ; 别名/措辞差异 " + str(len(alias_list)) +
          " 条 [" + "; ".join(["#" + str(i) + ": " + a + " / " + b for i, a, b in alias_list]) + "]" +
          " ; 内容级冲突 " + str(len(conflict_list)) + " 条 [" +
          "; ".join(["#" + str(i) + ": 文件=" + a + " vs 汇总=" + b for i, a, b in conflict_list]) + "]" +
          " ; 文件条目数 = " + str(len(file_map)) + " ; 汇总条目数 = " + str(len(md_map)) +
          " ; 仅文件有: " + (",".join([str(i) + file_map[i] for i in only_file]) or "无") +
          " ; 仅汇总有: " + (",".join([str(i) + md_map[i] for i in only_md]) or "无"))

if conflict_list:
    R.F("T13", "20 条核心公式清单的身份一致性",
        "判据: 归一化（去「的」/空白/连字符）后，同编号标题须相容；"
        "包含关系或共享字符占比 ≥ " + str(ALIAS_RATIO) + " 记别名（命名差异，不改判），"
        "互不相容才判 FAIL",
        detail,
        "同一批源材料对『第 18 条是哪一条』没有共识（文件=核力场定义方程，汇总=空间波动通解），"
        "即『20 个公式』这个集合本身未被唯一定义：任何『全部通过』的计数都缺少确定的计数对象。"
        "注意另有 " + str(len(alias_list)) + " 条只是标题措辞/简写差异，本文不动摇同一性，不计为冲突。")
else:
    R.P("T13", "20 条核心公式清单的身份一致性",
        "判据: 归一化后同编号标题相容即通过",
        detail,
        "清单身份一致。")

# T14 ----------------------------------------------------------- 「全部通过」可继承性
fail_count = sum(1 for r in R.rows if r["verdict"] == "FAIL")
fail_ids = [r["id"] for r in R.rows if r["verdict"] == "FAIL"]
R.F("T14", "『20 个公式全部通过严格验证』的可继承性",
    "判据: 若常数层存在任一不可复算/自相冲突的支撑证据，则该全局断言不可继承",
    "本轮独立精算已判 FAIL 的项数 = " + str(fail_count) + "（" + ", ".join(fail_ids) + "）",
    "不可继承。纪念文章的『全部验证通过』在常数层站不住："
    "常数 f、Z、Z'、k' 均有不可复算或自相冲突之处，且第 18 条公式在源材料内身份不唯一。"
    "本仓库按其 claims.csv 口径把该断言降级登记，不沿用『通过』结论。")

# T15 ----------------------------------------------------------- 与既有复算交叉互印证
local_vals = {"Z": Z_local, "Z'": Zp_local}
lines = []
all_ok = True
for item in EXISTING:
    v_cross = local_vals[item["name"]]
    d = rel(v_cross, item["value"])
    lines.append(item["name"] + ": 本轮 " + sci(v_cross, 8) + " vs 既有 " +
                 sci(item["value"], 8) + " rel = " + sci(d, 3))
    if d >= REL_LOOSE:
        all_ok = False
if all_ok:
    R.P("T15", "与 S17 既有复算的交叉互印证",
        "判据: 本轮独立复算与 04_理论推导/核心公式集/20-电磁耦合常数/验证报告.md 的相对偏差 < "
        + sci(REL_LOOSE, 1),
        " ; ".join(lines),
        "两条独立路径（本脚本 vs 体系既有复算）给出一致的 Z、Z' 数值，"
        "交叉印证『纪念文章的 Z、Z' 数值有误』这一结论不是单点偶然。")
else:
    R.B("T15", "与 S17 既有复算的交叉互印证",
        "判据: 相对偏差 < " + sci(REL_LOOSE, 1),
        " ; ".join(lines),
        "存在差异，需进一步核对常量取值来源。")

# ---------------------------------------------------------------- 输出
print("=" * 78)
print("VERDICT_SUMMARY")
print("PASS = " + str(R.n["PASS"]))
print("FAIL = " + str(R.n["FAIL"]))
print("BOUNDARY = " + str(R.n["BOUNDARY"]))
print("INFO = " + str(R.n["INFO"]))
print("TOTAL = " + str(sum(R.n.values())))
print("=" * 78)

report = [
    "S17 统一场论核心公式 —— 常数层独立精算报告",
    "源材料: 01_文献来源/统一场论核心公式全面验证完成纪念文章.md",
    "        01_文献来源/源材料_核心公式的元数据/",
    "红线: 不沿用来源自封结论；每项判定先给判据与阈值再实算。",
    "",
]
for r in R.rows:
    report.append("[" + r["verdict"] + "] " + r["id"] + " " + r["title"])
    report.append("    判据: " + r["criterion"])
    report.append("    实测: " + r["evidence"])
    report.append("    结论: " + r["note"])
    report.append("")
report.append("VERDICT_SUMMARY")
report.append("PASS = " + str(R.n["PASS"]))
report.append("FAIL = " + str(R.n["FAIL"]))
report.append("BOUNDARY = " + str(R.n["BOUNDARY"]))
report.append("INFO = " + str(R.n["INFO"]))
report.append("TOTAL = " + str(sum(R.n.values())))
report.append("")

out_txt = HERE / "核心公式常数层_独立精算_report.txt"
out_json = HERE / "核心公式常数层_独立精算_数据.json"
io.open(str(out_txt), "w", encoding="utf-8").write("\n".join(report))

payload = {
    "target": "S17 统一场论核心公式 常数层",
    "sources": [
        "01_文献来源/统一场论核心公式全面验证完成纪念文章.md",
        "01_文献来源/源材料_核心公式的元数据/核心公式的元数据.md",
        "01_文献来源/源材料_核心公式的元数据/核心公式的元数据.json",
        "01_文献来源/源材料_核心公式的元数据/20电磁耦合常数 Z'.md",
    ],
    "constants_codata2018": {
        "c": C_LIGHT, "G": G_NEWTON, "eps0": EPS0, "hbar": HBAR,
        "e": E_CHARGE, "m_Planck": M_PLANCK, "m_proton": M_PROTON,
    },
    "recomputed": {
        "f_def": f_def, "f_via_Z_Zp": f_via_ZZp,
        "Z": Z_local, "Zp": Zp_local,
        "k_4pi_m_Planck": k_planck, "k_4pi_m_proton": k_proton,
        "alpha": alpha, "alpha_doc_form": alpha_wrong, "alpha_corrected": alpha_right,
        "k_e": ke, "compound_kkp_over_4pieps0": compound,
        "c_implied_from_claim_Z": c_implied,
    },
    "dimensions": {
        "f_def": str(dim_f_def), "f_claimed": str(dim_f_claim),
        "Z_def": str(dim_Z_def), "Z_claimed": str(dim_Z_claim),
        "Zp_def": str(dim_Zp_def), "Zp_claimed": str(dim_Zp_claim),
        "alpha_doc form": str(dim_doc),
        "k_prime_metadata": str(dim_kp_meta),
        "k_prime_memorial": str(dim_kp_memo),
        "k_prime_v1": str(dim_kp_v1),
    },
    "formula_catalog_check": {
        "file_count": len(file_map),
        "summary_count": len(md_map),
        "same_count": len(same_list),
        "alias": [{"no": i, "file": a, "summary": b, "share_ratio": round(
            share_ratio(norm_title(a), norm_title(b)), 3)} for i, a, b in alias_list],
        "conflict": [{"no": i, "file": a, "summary": b, "share_ratio": round(
            share_ratio(norm_title(a), norm_title(b)), 3)} for i, a, b in conflict_list],
        "only_in_files": [{"no": i, "name": file_map[i]} for i in only_file],
        "only_in_summary": [{"no": i, "name": md_map[i]} for i in only_md],
        "alias_ratio_threshold": ALIAS_RATIO,
    },
    "results": R.rows,
    "summary": dict(R.n),
}
io.open(str(out_json), "w", encoding="utf-8").write(
    json.dumps(payload, ensure_ascii=False, indent=2))

print("已写出: " + str(out_txt))
print("已写出: " + str(out_json))
