# -*- coding: utf-8 -*-
"""
TUFT-r180｜S17 核心公式 3.20「电磁光速几何耦合常数 Z' = c/(8πε₀)」
          —— 力强度比恒等性 · Z'' 修正的量纲与效能 · Z' 双口径 · 验证脚本方法论

00. 编号与定位
  【编号】r180。★磁盘实测（2026-10-25 01:08）：r175 空间波动方程（00:24:13）、
        r176 核力场定义方程（00:30:21）、r177 引力光速统一方程（本线，00:48:39）、
        r178 S13 三公设路径四（00:54:59）、r179 物理常数总账（01:02:15）均已落盘
        ⇒ **r180 为首空号**，先落占位再写正文。
  【靶】S17/04_理论推导/核心公式集/20-电磁耦合常数/验证报告.md（7073 字节）
        + 同目录 code/{1.py, comprehensive_analysis.py, final_analysis.py,
        verify_Z_prime.py}（301 行）
    一、`Z = Gc/2 = 1.000452e−2`（注意：与 19 号靶的 1.00065e−2 不同值）
    二、`Z' = c/(8πε₀) = 1.347200e18 kg·m⁴·s⁻³·C⁻²`，量纲自称 [M L⁴ T⁻³ Q⁻²]
    三、`Z'/Z = 1.346591e20`，量纲自称 [M² Q⁻²]
    四、`F_e/F_g = (Z'/Z)·(|q₁q₂|/(m₁m₂))`，质子间「理论 = 实验 = 1.235552e36，误差 0.00%」
    五、`α = 2e²Z'/(ħc²)` 被当作「高精度吻合验证推导正确性」
    六、§4 引入修正常数 `Z'' = αħc²/(16πε₀G)`，量纲自称 [M³ L⁻² T⁵ Q⁻²]，
        自称目的 = 解决耦合常数 f 的量纲混淆（核心方程要求 [f] = [M Q⁻¹]）
  【问题】判力比公式是否恒等（零判别力）、Z'' 的量纲自评与其效能是否成立、
        Z' 是否口径唯一、验证脚本的结论是否由计算驱动。

01. 机读手段
  纯标准库。① Decimal(60) 高精度重算 Z、Z'、Z''、α、三组粒子力比；
  ② Fraction (M,L,T,Q) 四元组量纲计算器（附 I=Q/T 口径互换，防「两个口径」
     被误判为矛盾）；③ 恒等性判据（数值残差机器零 + 扰动 1e−3 负对照）；
  ④ 精确有理线性代数求解「使 f 量纲 = [M Q⁻¹] 所需的 [Z'']」并穷举验证唯一性；
  ⑤ ast 三层方法论审计（结论与计算是否耦合 / 是否真有计算 / 多份总结是否互斥）；
  ⑥ 全目录 Z' 定义式扫描（按文件去重）。

02. 红线（纪律）
  · 数学自洽 ≠ 实验证实；恒等式成立 ≠ 有新内容；数值吻合（尤其「0.00%」）须先问
    是不是恒等式的算术必然。
  · 守卫/控制组的 ok 必须由真实计算得出，禁止写死 True。
  · 分层铁律：本卷条目不与 r168（f 的量纲裁定）/ r177（Z 卷）/ r171（k′）相加；
    本卷判的是「Z'' 是否达成其自称目的」，**不裁定 f 本身的最终量纲**。
  · 靶自承优先；对靶有利的结论单列 PASS，不予否定。
"""

import ast
import io
import json
import os
import re
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
T_START = time.time()

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ============================================================
# 路径 / 登记器
# ============================================================
HERE = os.path.dirname(os.path.abspath(__file__))
NORM = os.path.dirname(HERE)
BASE = os.path.dirname(os.path.dirname(NORM))
OUT = os.path.join(NORM, "数据")
STEM = "TUFT-r180_电磁耦合常数Zprime_恒等力比与Z双素数修正_精算_2026-10-25"

TGT_DIR = os.path.join(BASE, "01_独立体系", "S17_统一场论核心公式",
                       "04_理论推导", "核心公式集", "20-电磁耦合常数")
TARGET = os.path.join(TGT_DIR, "验证报告.md")
CODE_DIR = os.path.join(TGT_DIR, "code")
SCAN_ROOT = os.path.join(BASE, "01_独立体系", "S17_统一场论核心公式")

ITEMS = []
CONTROLS = []
GUARDS = []


def add(iid, title, status, note="", **metrics):
    ITEMS.append({"id": iid, "title": title, "status": status,
                  "note": note, "metrics": metrics})


def control(cid, desc, value, expect, ok):
    CONTROLS.append({"id": cid, "desc": desc, "value": value,
                     "expect": expect, "ok": bool(ok)})


def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})


def fs(x, n=6):
    try:
        return "%.*e" % (n, float(x))
    except Exception:
        return str(x)


# ============================================================
# 03. 高精度常数（CODATA 2018，与靶文附录同一套）
# ============================================================
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494459")
C = Decimal("299792458")
G = Decimal("6.67430e-11")
EPS0 = Decimal("8.8541878128e-12")
E_CH = Decimal("1.602176634e-19")
M_P = Decimal("1.67262192369e-27")     # 质子质量（靶文附录 m_p）
M_E = Decimal("9.1093837015e-31")      # 电子质量
HBAR = Decimal("1.054571817e-34")
ALPHA = Decimal("7.2973525693e-3")
# 靶文宣称值
Z_CLAIM_MAIN = Decimal("1.000452e-2")    # 本靶 §2.1 的 Z
Z_CLAIM_19 = Decimal("1.00065e-2")       # 19 号靶（r177）的 Z 宣称值
ZP_CLAIM = Decimal("1.347200e18")        # 本靶 §2.2 的 Z'
RATIO_CLAIM = Decimal("1.346591e20")     # 本靶 §2.3 的 Z'/Z
FORCE_CLAIM = Decimal("1.235552e36")     # 本靶 §3.2 的质子间力比

# 精算
Z_EXACT = G * C / 2                       # Z = Gc/2
ZP_EXACT = C / (8 * PI * EPS0)            # Z' = c/(8πε₀)
RATIO_EXACT = ZP_EXACT / Z_EXACT          # Z'/Z
RATIO_ALT = ZP_EXACT / Z_CLAIM_19         # 用 19 号靶 Z 值时的比值
ZPP_EXACT = (ALPHA * HBAR * C * C) / (16 * PI * EPS0 * G)   # Z'' = αħc²/(16πε₀G)

Z_REL = (ZP_EXACT - ZP_CLAIM) / ZP_CLAIM
RATIO_REL = (RATIO_EXACT - RATIO_CLAIM) / RATIO_CLAIM
ZP_DUAL_RATIO = ZP_EXACT / ZPP_EXACT      # Z' 两口径之比

# α 的两条路径
ALPHA_FROM_ZP = (2 * E_CH * E_CH * ZP_EXACT) / (HBAR * C * C)   # 靶文 §verify
ALPHA_STD = E_CH * E_CH / (4 * PI * EPS0 * HBAR * C)            # 标准定义
ALPHA_REL = (ALPHA_FROM_ZP - ALPHA_STD) / ALPHA_STD
ALPHA_VS_EXPT = (ALPHA_FROM_ZP - ALPHA) / ALPHA

# ============================================================
# 04. 量纲计算器 (M,L,T,Q)，附 I = Q/T 口径
# ============================================================
DIM_NAMES = ("M", "L", "T", "Q")


def dim(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))


def dprod(a, k):
    return tuple(x * Fraction(k) for x in a)


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dfmt(a):
    parts = []
    for name, v in zip(DIM_NAMES, a):
        if v == 0:
            continue
        parts.append("%s^%s" % (name, v))
    return " ".join(parts) if parts else "1"


def dfmt_I(a):
    """同一量纲用电流 I 表示（Q = I·T ⇒ I = Q/T）。"""
    m, l, t, q = a
    return dfmt((m, l, t + q, q)).replace("Q", "I")


D_G = dim(m=-1, l=3, t=-2)
D_C = dim(l=1, t=-1)
D_M = dim(m=1)
D_Q = dim(q=1)
D_EPS0 = dim(m=-1, l=-3, t=2, q=2)         # [ε₀] = M⁻¹L⁻³T²Q²
D_HBAR = dim(m=1, l=2, t=-1)
D_F = dim(m=1, l=1, t=-2)

D_Z = dmul(D_G, D_C)                        # [Gc/2] = M⁻¹L⁴T⁻³
D_ZP = ddiv(D_C, D_EPS0)                    # [c/(8πε₀)] = M L⁴ T⁻³ Q⁻²
D_RATIO = ddiv(D_ZP, D_Z)                   # [Z'/Z]
D_ZPP = ddiv(dmul(D_HBAR, dprod(D_C, 2)),
             dmul(D_EPS0, D_G))             # [αħc²/(16πε₀G)]
D_ZPP_CLAIM = dim(m=3, l=-2, t=5, q=-2)     # 靶文自称
D_F_TARGET = dim(m=1, q=-1)                 # 靶文自称核心方程要求 [f] = [M Q⁻¹]

# f = √(Z/Z'')·(c/2) 在靶文 Z'' 下的实算量纲
D_F_WITH_ZPP = dmul(dprod(ddiv(D_Z, D_ZPP), Fraction(1, 2)), D_C)
# f = √(Z/Z')·(c/2) 在原始 Z' 下的量纲（靶文 §4 自称 [M⁻¹ L I]）
D_F_WITH_ZP = dmul(dprod(ddiv(D_Z, D_ZP), Fraction(1, 2)), D_C)

DIM_SELFCHECK = [
    ("[G] = M⁻¹L³T⁻²", D_G, dim(m=-1, l=3, t=-2)),
    ("[ε₀] = M⁻¹L⁻³T²Q²", D_EPS0, dim(m=-1, l=-3, t=2, q=2)),
    ("[c/ε₀] = ML⁴T⁻³Q⁻²", D_ZP, dim(m=1, l=4, t=-3, q=-2)),
    ("[ħ] = ML²T⁻¹", D_HBAR, dim(m=1, l=2, t=-1)),
]
DIM_SELF_OK = all(a == b for _, a, b in DIM_SELFCHECK)

# ============================================================
# 05. 恒等性：F_e/F_g = (Z'/Z)·(q₁q₂/(m₁m₂))
# ============================================================
PAIRS = [("质子-质子", E_CH, E_CH, M_P, M_P),
         ("电子-电子", E_CH, E_CH, M_E, M_E),
         ("质子-电子", E_CH, E_CH, M_P, M_E)]

FORCE_ROWS = []
FORCE_MAX_RES = Decimal(0)
for name, q1, q2, m1, m2 in PAIRS:
    theo = RATIO_EXACT * (abs(q1 * q2) / (m1 * m2))
    expt = (abs(q1 * q2) / (4 * PI * EPS0)) / (G * m1 * m2)
    res = abs(theo - expt) / expt
    FORCE_ROWS.append({"pair": name, "theory": fs(theo, 6),
                       "experiment_labelled": fs(expt, 6),
                       "rel_residual": fs(res, 3)})
    FORCE_MAX_RES = max(FORCE_MAX_RES, res)
FORCE_IDENTICAL = FORCE_MAX_RES < Decimal("1e-40")

# 符号级：(Z'/Z) ≡ 1/(4πε₀ G)
D_ONE_OVER_4PI_EPS0_G = ddiv(dim(), dmul(D_EPS0, D_G))
RATIO_DIM_OK = (D_RATIO == D_ONE_OVER_4PI_EPS0_G)
RATIO_NUM_OK = abs(RATIO_EXACT - 1 / (4 * PI * EPS0 * G)) / RATIO_EXACT
RATIO_ALGEBRA_OK = RATIO_NUM_OK < Decimal("1e-40")

# 扰动负对照（判据判别力）
PERT = Decimal("1e-3")
RATIO_PERT = RATIO_EXACT * (1 + PERT)
_p = PAIRS[0]
theo_p = RATIO_PERT * (abs(_p[1] * _p[2]) / (_p[3] * _p[4]))
expt_p = (abs(_p[1] * _p[2]) / (4 * PI * EPS0)) / (G * _p[3] * _p[4])
PERT_RES = abs(theo_p - expt_p) / expt_p

ALPHA_IDENTICAL = abs(ALPHA_REL) < Decimal("1e-40")

# ============================================================
# 06. 求解「使 f 量纲 = [M Q⁻¹] 所需的 [Z'']」（精确有理线性代数）
# ============================================================
# f = √(Z/Z'')·(c/2) ⇒ [f] = ½([Z] − [Z'']) + [c]
# ⇒ [Z''] = [Z] + 2[c] − 2[f]
D_ZPP_NEED = [a + 2 * c - 2 * f
              for a, c, f in zip(D_Z, D_C, D_F_TARGET)]
D_ZPP_NEED = tuple(Fraction(x) for x in D_ZPP_NEED)
D_F_CHECK = dmul(dprod(ddiv(D_Z, D_ZPP_NEED), Fraction(1, 2)), D_C)
NEED_CHECK_OK = (D_F_CHECK == D_F_TARGET)

VEC_HBAR = (Fraction(1), Fraction(2), Fraction(-1), Fraction(0))
VEC_C = (Fraction(0), Fraction(1), Fraction(-1), Fraction(0))
VEC_EPS0 = (Fraction(-1), Fraction(-3), Fraction(2), Fraction(2))
VEC_G = (Fraction(-1), Fraction(3), Fraction(-2), Fraction(0))
NEED = D_ZPP_NEED


def solve_4x4(cols, rhs):
    """精确求解 Σ x_j·cols[j] = rhs；返回 (x, rank, unique)。"""
    m = [[Fraction(cols[j][i]) for j in range(4)] + [Fraction(rhs[i])]
         for i in range(4)]
    piv_cols = []
    r = 0
    for c in range(4):
        piv = None
        for i in range(r, 4):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(4):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv_cols.append(c)
        r += 1
    if r != 4:
        return None, r, False
    x = [Fraction(0)] * 4
    for i in range(4):
        x[piv_cols[i]] = m[i][4]
    for i in range(4):
        s = sum(Fraction(cols[j][i]) * x[j] for j in range(4))
        if s != rhs[i]:
            return None, r, False
    return x, r, True


SOL, SOL_RANK, SOL_UNIQUE = solve_4x4(
    [VEC_HBAR, VEC_C, VEC_EPS0, VEC_G], NEED)

# 穷举校验唯一性：b,d,e,g ∈ [-4,4]
EXH_HITS = []
for b in range(-4, 5):
    for d in range(-4, 5):
        for e in range(-4, 5):
            for g in range(-4, 5):
                acc = [Fraction(0)] * 4
                for k, val in ((b, VEC_HBAR), (d, VEC_C), (e, VEC_EPS0),
                               (g, VEC_G)):
                    acc = [a + Fraction(k) * c for a, c in zip(acc, val)]
                if tuple(acc) == NEED:
                    EXH_HITS.append({"hbar": b, "c": d, "eps0": e, "G": g})
EXH_UNIQUE = len(EXH_HITS) == 1
TGT_EXP = {"hbar": 1, "c": 2, "eps0": -1, "G": -1}
TGT_IN_SOLUTION = any(h == TGT_EXP for h in EXH_HITS)

# ============================================================
# 07. 靶文机读
# ============================================================
READ_OK = False
N_LINES = 0
TXT = ""
try:
    with io.open(TARGET, "r", encoding="utf-8") as f:
        TXT = f.read()
    READ_OK = True
    N_LINES = len(TXT.splitlines())
except Exception:
    TXT = ""
TXT_N = TXT.replace("\\,", " ").replace("\\;", " ").replace("\\!", " ")

HIT = {
    "Z=Gc/2": len(re.findall(r"Z\s*=\s*\\?d?frac\{?\s*G\s*c\s*\}?\s*/?\s*\{?\s*2\s*\}?", TXT_N)),
    "Z'=c/(8pi eps0)": len(re.findall(r"Z'\s*=\s*\\?d?frac\{?\s*c\s*\}?\s*/?\s*\{?\s*8\s*\\?pi\s*\\?(?:varepsilon|epsilon)", TXT_N)),
    "Z''=alpha...": len(re.findall(r"Z''\s*=\s*\\?d?frac\{?\s*\\alpha", TXT_N)),
    "force_ratio_formula": len(re.findall(r"F_e\s*/\s*F_g", TXT_N)),
}
N_ZERO_ERROR = len(re.findall(r"0\.00%", TXT_N))
N_CORRECT_CLAIM = len(re.findall(r"完全?一致|验证通过|正确|符合", TXT_N))

# ============================================================
# 08. 验证脚本方法论审计（ast 三层）
# ============================================================
CODE_FILES = ["1.py", "comprehensive_analysis.py", "final_analysis.py",
              "verify_Z_prime.py"]
CODE_AUDIT = []
CONCLUSION_WORDS = ("完全一致", "验证通过", "正确", "符合", "结论", "成功", "自洽")


def audit_code(path):
    rec = {"file": os.path.basename(path), "top_print": 0,
           "top_const_conclusion": 0, "calc_nodes": 0, "if_nodes": 0,
           "hardcoded": [], "lines": 0, "readable": False}
    try:
        with io.open(path, "r", encoding="utf-8") as f:
            src = f.read()
        tree = ast.parse(src)
        rec["readable"] = True
        rec["lines"] = len(src.splitlines())
    except Exception:
        return rec
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp):
            rec["calc_nodes"] += 1
        elif isinstance(node, ast.If):
            rec["if_nodes"] += 1
        elif isinstance(node, ast.Assign):
            rec["calc_nodes"] += 1
        elif isinstance(node, ast.Compare):
            rec["calc_nodes"] += 1
    for stmt in tree.body:
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            fn = stmt.value.func
            if isinstance(fn, ast.Name) and fn.id == "print":
                rec["top_print"] += 1
                for arg in stmt.value.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        if any(w in arg.value for w in CONCLUSION_WORDS):
                            rec["top_const_conclusion"] += 1
                            rec["hardcoded"].append(arg.value.strip()[:70])
    return rec


for fn in CODE_FILES:
    p = os.path.join(CODE_DIR, fn)
    if os.path.isfile(p):
        CODE_AUDIT.append(audit_code(p))
N_CODE = len(CODE_AUDIT)
TOTAL_TOP_CONST = sum(r["top_const_conclusion"] for r in CODE_AUDIT)
TOTAL_CALC = sum(r["calc_nodes"] for r in CODE_AUDIT)
TOTAL_IF = sum(r["if_nodes"] for r in CODE_AUDIT)

DEP_MISSING = []
for r in CODE_AUDIT:
    try:
        with io.open(os.path.join(CODE_DIR, r["file"]), "r",
                     encoding="utf-8") as f:
            s = f.read()
        for lib in ("numpy", "scipy", "pint"):
            if re.search(r"^\s*import\s+%s|^\s*from\s+%s" % (lib, lib), s, re.M):
                DEP_MISSING.append("%s:%s" % (r["file"], lib))
    except Exception:
        pass

# ============================================================
# 09. 全目录扫描：Z' 定义式与数值口径（按文件去重）
# ============================================================
SCAN = {"files": 0, "zp_orig": [], "zp_corr": [], "z_vals": [], "errors": []}
PAT_ZP_ORIG = re.compile(r"c\s*/\s*\(?\s*8\s*\\?pi\s*\\?(?:varepsilon|epsilon)")
PAT_ZP_ORIG_PY = re.compile(r"c\s*/\s*\(\s*8\s*\*\s*(?:np\.)?pi\s*\*\s*epsilon0\s*\)")
PAT_ZP_CORR = re.compile(r"\\alpha\s*\\hbar\s*c\^?2?\s*/\s*\(?\s*16\s*\\?pi\s*\\?(?:varepsilon|epsilon)")
PAT_ZP_CORR_PY = re.compile(r"alpha\s*\*\s*hbar\s*\*\s*c\s*\*\*\s*2\s*/\s*\(\s*16\s*\*\s*(?:np\.)?pi\s*\*\s*epsilon0\s*\*\s*G\s*\)")
PAT_Z_VAL = re.compile(r"1\.000(?:452|65)")

try:
    for root, dirs, files in os.walk(SCAN_ROOT):
        for fn in files:
            if not fn.lower().endswith((".md", ".py")):
                continue
            p = os.path.join(root, fn)
            try:
                with io.open(p, "r", encoding="utf-8", errors="replace") as f:
                    t = f.read()
            except Exception:
                continue
            SCAN["files"] += 1
            rel = os.path.relpath(p, BASE).replace("\\", "/")
            for i, line in enumerate(t.splitlines(), 1):
                if PAT_ZP_ORIG.search(line) or PAT_ZP_ORIG_PY.search(line):
                    SCAN["zp_orig"].append(
                        {"file": rel, "line": i, "text": line.strip()[:150]})
                if PAT_ZP_CORR.search(line) or PAT_ZP_CORR_PY.search(line):
                    SCAN["zp_corr"].append(
                        {"file": rel, "line": i, "text": line.strip()[:150]})
                if PAT_Z_VAL.search(line):
                    SCAN["z_vals"].append(
                        {"file": rel, "line": i, "text": line.strip()[:150]})
except Exception as exc:
    SCAN["errors"].append(str(exc))

F_ZP_ORIG = len(set(x["file"] for x in SCAN["zp_orig"]))
F_ZP_CORR = len(set(x["file"] for x in SCAN["zp_corr"]))
F_Z_VAL = len(set(x["file"] for x in SCAN["z_vals"]))
ZP_DUAL_DEFS = (F_ZP_ORIG >= 1) and (F_ZP_CORR >= 1)

# ============================================================
# 10. 条目 A：力强度比的恒等性
# ============================================================
add("A01",
    "力比公式 `F_e/F_g = (Z'/Z)·(q₁q₂/m₁m₂)` 与库仑-牛顿比**恒等**（三组残差机器零）",
    "FAIL",
    note="代入 Z'=c/(8πε₀)、Z=Gc/2 得 (Z'/Z) = 1/(4πε₀G)（量纲 %s、数值残差 %s），"
         "故 RHS ≡ q₁q₂/(4πε₀ G m₁m₂) ≡ F_e/F_g。三组粒子（pp/ee/pe）残差最大 %s"
         " ⇒ 所谓「理论预测与实验值完全一致、误差 0.00%%」是**恒等式的算术必然**。"
         % (dfmt(D_RATIO), fs(RATIO_NUM_OK, 3), fs(FORCE_MAX_RES, 3)),
    max_residual=fs(FORCE_MAX_RES, 3), ratio_is_1_over_4pi_eps0_G=RATIO_ALGEBRA_OK)

add("A02",
    "判据判别力（负对照）：把 Z'/Z 扰动 1e−3，力比残差 = %s" % fs(PERT_RES, 4),
    "PASS",
    note="扰动后质子-质子残差 = %s，与预期 1e−3 吻合 ⇒ A01 的「残差为零」不是"
         "判据恒真的假绿，而是真恒等。" % fs(PERT_RES, 4),
    perturbed_residual=fs(PERT_RES, 4))

add("A03",
    "「实验值」实为同一批 CODATA 常数的另一种写法（零实验接触）",
    "FAIL",
    note="靶文把 `e²/(4πε₀ G m_p²)` 标为「(实验值)」、把 `(Z'/Z)·e²/m_p²` 标为"
         "「理论预测值」，两者用同一套 CODATA 常数且互为恒等 ⇒ 该栏不是实验测量"
         "数据，而是理论式的重排；表内「误差 0.00%」因而不携带实验信息。",
    force_pp=FORCE_ROWS[0]["theory"])

add("A04",
    "`α = 2e²Z'/(ħc²)` 是 α = e²/(4πε₀ħc) 的恒等重排，却被当作「验证推导正确性」",
    "FAIL",
    note="代入 Z'=c/(8πε₀)：2e²Z'/(ħc²) = e²/(4πε₀ħc) 逐项相消 ⇒ 两条路径相对差 %s"
         "（机器零）；与 CODATA α 的相对差 %s。靶文 §7 据此称「与精细结构常数的"
         "高精度吻合验证了推导的正确性」⇒ 第二处恒等被当作证据。"
         % (fs(ALPHA_REL, 3), fs(ALPHA_VS_EXPT, 4)),
    alpha_identity_residual=fs(ALPHA_REL, 3))

# ============================================================
# 11. 条目 B：Z'' 的量纲、效能与 Z' 双口径
# ============================================================
add("B01",
    "Z'' 的自称量纲错：自称 %s，实算 %s，差 %s"
    % (dfmt(D_ZPP_CLAIM), dfmt(D_ZPP), dfmt(ddiv(D_ZPP, D_ZPP_CLAIM))),
    "FAIL",
    note="`Z'' = αħc²/(16πε₀G)`：[α]=1、[ħ]=ML²T⁻¹、[c²]=L²T⁻²、"
         "[ε₀]=M⁻¹L⁻³T²Q²、[G]=M⁻¹L³T⁻² ⇒ [ε₀G]=M⁻²Q²、[ħc²]=ML⁴T⁻³"
         " ⇒ [Z'']=%s。靶文写 %s ⇒ **L 差 6 个幂次、T 差 8 个幂次**；"
         "该错误出现在「异常修复」章，即用来修别人的式子自身量纲先错。"
         % (dfmt(D_ZPP), dfmt(D_ZPP_CLAIM)),
    dim_actual=dfmt(D_ZPP), dim_claim=dfmt(D_ZPP_CLAIM),
    gap=dfmt(ddiv(D_ZPP, D_ZPP_CLAIM)))

add("B02",
    "Z'' 未达成其自称目的：用 Z'' 算出的 f 量纲仍 ≠ 核心方程要求",
    "FAIL",
    note="按靶文 §4 的 f = √(Z/Z'')·(c/2)，代入实算 [Z'']=%s 得 [f]=%s"
         "（I 口径 %s），而自称核心方程要求 [f]=[M Q⁻¹] ⇒ 差 %s。"
         "对比：用原始 Z' 时 [f]=%s（I 口径 %s，与靶文 §4 自评 [M⁻¹ L I] 一致）"
         " ⇒ 靶文的**问题诊断正确**，但**解决方案无效**。"
         % (dfmt(D_ZPP), dfmt(D_F_WITH_ZPP), dfmt_I(D_F_WITH_ZPP),
            dfmt(ddiv(D_F_WITH_ZPP, D_F_TARGET)),
            dfmt(D_F_WITH_ZP), dfmt_I(D_F_WITH_ZP)),
    f_with_zpp=dfmt(D_F_WITH_ZPP), f_target=dfmt(D_F_TARGET),
    gap=dfmt(ddiv(D_F_WITH_ZPP, D_F_TARGET)))

if SOL_UNIQUE and SOL is not None:
    _sol_txt = "ħ^%s · c^%s · ε₀^%s · G^%s" % (SOL[0], SOL[1], SOL[2], SOL[3])
else:
    _sol_txt = "（无解或解不唯一）"

add("B03",
    "在 {α,ħ,c,ε₀,G} 池内使命题成立的 Z'' 形式唯一：%s（α 指数任意）" % _sol_txt,
    "FAIL",
    note="解精确线性方程组 [Z''] = [Z] + 2[c] − 2[f]，得 %s；穷举 %d 组"
         "（ħ,c,ε₀,G ∈ [−4,4]）命中 %d 组 ⇒ %s。**靶文形式 (ħ¹c²ε₀⁻¹G⁻¹) 不在解集"
         "中**：ħ 应为 %s 次（靶文 1）、c 应为 %s 次（靶文 2）、G 应为 %s 次"
         "（靶文 −1）⇒ 结构性错位，不是系数问题。"
         % (_sol_txt, 9 ** 4, len(EXH_HITS), "唯一" if EXH_UNIQUE else "非唯一",
            SOL[0], SOL[1], SOL[3]),
    solution=_sol_txt, exhaustive_hits=len(EXH_HITS),
    target_form_in_solution=TGT_IN_SOLUTION)

add("B04",
    "Z' 双口径：%s（c/8πε₀，%d 文件）与 %s（αħc²/16πε₀G，%d 文件），差 %s 倍"
    % (fs(ZP_EXACT, 6), F_ZP_ORIG, fs(ZPP_EXACT, 6), F_ZP_CORR,
       fs(ZP_DUAL_RATIO, 6)),
    "FAIL",
    note="`comprehensive_analysis.py` §5 把 `Z'' = αħc²/(16πε₀G)` 直接称为"
         "「**修正后的电磁几何常数 Z'**」⇒ 同一符号 Z' 承载两个互斥定义，数值相差"
         " %s 倍；两者量纲亦不同（%s vs %s）⇒ 不是同一量的两种写法，而是两个不同的"
         "量。与 r177 的 m_p / Z 双口径同族（本卷不与之相加）。"
         % (fs(ZP_DUAL_RATIO, 6), dfmt(D_ZP), dfmt(D_ZPP)),
    ratio=fs(ZP_DUAL_RATIO, 6), orig_files=F_ZP_ORIG, corr_files=F_ZP_CORR)

# ============================================================
# 12. 条目 C：Z' 本身的成立面与名实
# ============================================================
add("C01",
    "Z' = c/(8πε₀) 的数值与量纲**全对**（精算 %s vs 宣称 %s，相对差 %s）"
    % (fs(ZP_EXACT, 8), fs(ZP_CLAIM, 6), fs(Z_REL, 3)),
    "PASS",
    note="[Z'] = [c]/[ε₀] = %s，与靶文自称 [M L⁴ T⁻³ Q⁻²] 逐位一致；"
         "数值 %s vs 靶文 %s ⇒ 相对差 %s。这是靶文真实且无争议的正确部分。"
         % (dfmt(D_ZP), fs(ZP_EXACT, 10), fs(ZP_CLAIM, 6), fs(Z_REL, 3)),
    zp_exact=fs(ZP_EXACT, 10), rel=fs(Z_REL, 3))

add("C02",
    "Z'/Z 的量纲 [M²Q⁻²] 与「力比无量纲」的声称**正确**",
    "PASS",
    note="[Z'/Z] = %s（与自称一致）；乘 q₁q₂/(m₁m₂) 后量纲 %s = 无量纲 ✓。"
         "即该式量纲工作是对的，A01 判的是「它恒等」，不是「它量纲错」。"
         % (dfmt(D_RATIO), dfmt(dmul(D_RATIO, ddiv(dprod(D_Q, 2),
                                                    dprod(D_M, 2))))),
    dim_ratio=dfmt(D_RATIO))

add("C03",
    "「电磁光速几何耦合常数」名实不符：Z' 是 ε₀ 的换写，数值只能由 ε₀ 反推",
    "FAIL",
    note="Z' = c/(8πε₀) 的全部经验内容来自 ε₀ 与 c；脱去 ε₀ 后 Z' 不可独立计算"
         " ⇒ 「时空旋转运动的几何强度」是标签而非导出。靶文 §5 称「超越经验常数、"
         "从时空几何本身解释力的强度差异」，但 (Z'/Z) 恰 = 1/(4πε₀G) ⇒ 力比仍由"
         " ε₀、G 两个经验常数决定（数值 %s）。" % fs(RATIO_EXACT, 8),
    ratio_equals=fs(RATIO_EXACT, 8))

# ============================================================
# 13. 条目 D：验证脚本方法论审计
# ============================================================
_hc = []
for r in CODE_AUDIT:
    _hc.extend(r["hardcoded"])
add("D01",
    "顶层无条件 print 的常量式结论 %d 处（结论与计算解耦）" % TOTAL_TOP_CONST,
    "FAIL",
    note="ast 扫描 %d 个脚本：模块级（不在 if/函数内）直接 print 常量字符串且含"
         "结论性措辞的共 %d 处。样本：%s ⇒ 结论不随计算结果改变，"
         "即脚本无论算出什么都打印「验证通过」。"
         % (N_CODE, TOTAL_TOP_CONST, " / ".join(_hc[:3])[:170] or "—"),
    top_const_conclusions=TOTAL_TOP_CONST)

add("D02",
    "脚本确有真实计算（BinOp/Assign/Compare 节点 %d 个、if 分支 %d 个）"
    % (TOTAL_CALC, TOTAL_IF),
    "PASS",
    note="不因 D01 抹掉：四份脚本确实做了数值计算与量纲打印，缺陷在于**结论不是"
         "由这些计算分支出来的**，而非「没有计算」。",
    calc_nodes=TOTAL_CALC, if_nodes=TOTAL_IF)

add("D03",
    "同目录多份总结互斥：Z' 一处用 c/(8πε₀) 称「已通过」，另一处改称「修正后的 Z'」",
    "FAIL",
    note="`final_analysis.py` 用原始 Z' 并宣称「量纲 ✓」；"
         "`comprehensive_analysis.py` 判定原始 Z' 导致 f 量纲不合格、改用"
         " αħc²/(16πε₀G) 并把它标为「修正后的 Z'」⇒ 同一目录同一符号的两个结论"
         "互斥，且修正后的量纲自评还错（B01）。",
    orig_files=F_ZP_ORIG, corrected_files=F_ZP_CORR)

add("D04",
    "脚本依赖 numpy/scipy/pint，本环境不可复现（%s）"
    % (", ".join(DEP_MISSING[:4]) or "无"),
    "INFO",
    note="托管 Python 3.13 无 numpy/scipy/pint ⇒ 本卷对四份脚本只做 ast 静态审计，"
         "**不以「跑不起来」判其错**；数值结论全部由本卷独立重算提供。",
    deps=DEP_MISSING)

# ============================================================
# 14. 条目 E：对靶有利（单列，不予否定）
# ============================================================
add("E01",
    "靶文对 f 量纲不一致的诊断**正确**（原始 Z' 下 [f] ≠ [M I⁻¹]）",
    "PASS",
    note="用原始 Z' 时 [f] = √(Z/Z')·(c/2) = %s（I 口径 %s），与靶文 §4 自评"
         " [M⁻¹ L I] 逐位一致，也确与核心方程要求的 [M I⁻¹] 不符 ⇒ 问题诊断成立"
         "（本卷不裁定 f 的最终量纲，该问题归 r168）。"
         % (dfmt(D_F_WITH_ZP), dfmt_I(D_F_WITH_ZP)),
    f_with_zp=dfmt(D_F_WITH_ZP))

add("E02",
    "靶文主动区分符号：引力场 A_g [LT⁻²] 与磁矢势 A_m [MLT⁻¹Q⁻¹]",
    "PASS",
    note="§4.1 明确指出「不同文献中对 A 的定义不同导致量纲混淆」并提出分符号 ⇒ "
         "自我纠错方向正确，与 r168 的「A 双重读法」独立同证。")

add("E03",
    "Z、Z'、Z'/Z、力比四项的量纲分析全部正确",
    "PASS",
    note="[Z]=%s、[Z']=%s、[Z'/Z]=%s、力比=无量纲，四项与自称一致。"
         "本卷 FAIL 集中在恒等性（A）、Z''（B）与名实（C），不建立在量纲错误上。"
         % (dfmt(D_Z), dfmt(D_ZP), dfmt(D_RATIO)))

add("E04",
    "I 口径与 Q 口径的量纲表述自洽（防本卷假阳性）",
    "PASS",
    note="`verify_Z_prime.py` 写 [M L⁴ T⁻⁵ I⁻²]、`final_analysis.py` 写"
         " [M L⁴ T⁻³ Q⁻²]；由 Q = I·T 互换后二者**等价**（机读：%s）⇒ 这不是两份"
         "脚本的矛盾（真矛盾见 D03）。本条用于防止把单位制差异误判为口径冲突。"
         % dfmt_I(D_ZP))

add("E05",
    "Z'/Z 数值 %s 与宣称 %s 一致（相对差 %s）" % (fs(RATIO_EXACT, 8),
                                                 fs(RATIO_CLAIM, 6),
                                                 fs(RATIO_REL, 3)),
    "PASS",
    note="本靶用 Z = 1.000452e−2（与 Gc/2 精算一致）⇒ 比值自洽；若采用 19 号靶的"
         " Z = 1.00065e−2 则比值为 %s（差 %s）⇒ 与 r177 E06 交叉印证，"
         "本卷不重判 r177。"
         % (fs(RATIO_ALT, 8), fs((RATIO_ALT - RATIO_CLAIM) / RATIO_CLAIM, 4)),
    ratio_alt=fs(RATIO_ALT, 8))

# ============================================================
# 15. 控制组（全部真算）
# ============================================================
control("K1", "Z' 精算 c/(8πε₀) 与宣称值比对", fs(Z_REL, 3), "<1e-5",
        abs(Z_REL) < Decimal("1e-5"))
control("K2", "力比恒等：三组残差机器零", fs(FORCE_MAX_RES, 3), "≈0",
        FORCE_IDENTICAL)
control("K3", "扰动 1e−3 后残差 ≈ 1e−3（判据有判别力）", fs(PERT_RES, 4),
        "≈1e-3", abs(PERT_RES - PERT) / PERT < Decimal("1e-6"))
control("K4", "α 两条路径恒等（机器零）", fs(ALPHA_REL, 3), "≈0", ALPHA_IDENTICAL)
control("K5", "α 重算与 CODATA 值比对", fs(ALPHA_VS_EXPT, 3), "<1e-6",
        abs(ALPHA_VS_EXPT) < Decimal("1e-6"))
control("K6", "量纲计算器自检 4 组已知量纲对",
        "%d/4" % sum(1 for _, a, b in DIM_SELFCHECK if a == b), "4/4", DIM_SELF_OK)
control("K7", "需求解 [Z''] 代回后 f 量纲命中目标",
        "%s → %s" % (dfmt(D_ZPP_NEED), dfmt(D_F_CHECK)), "[M Q^-1]",
        NEED_CHECK_OK)
control("K8", "线性方程组解唯一（rank=4 且回代通过）",
        "%s rank=%d" % (str(SOL_UNIQUE), SOL_RANK), "True rank=4",
        bool(SOL_UNIQUE) and SOL_RANK == 4)
control("K9", "穷举命中数 = 1（唯一性交叉验证）", str(len(EXH_HITS)), "1",
        EXH_UNIQUE)
control("K10", "靶文读取 + 公式形态命中",
        "%d 行 / 命中 %d 类" % (N_LINES, sum(1 for v in HIT.values() if v > 0)),
        "≥3 类", READ_OK and sum(1 for v in HIT.values() if v > 0) >= 3)
control("K11", "ast 审计覆盖 4 个脚本且均可解析",
        "%d 个 / 可解析 %d" % (N_CODE, sum(1 for r in CODE_AUDIT
                                           if r["readable"])), "4/4",
        N_CODE == 4 and all(r["readable"] for r in CODE_AUDIT))
control("K12", "Z' 双口径按文件去重后均 ≥1",
        "orig=%d corr=%d" % (F_ZP_ORIG, F_ZP_CORR), "均 ≥1", ZP_DUAL_DEFS)
control("K13", "扫描规模守卫（防路径失效静默变 0）", str(SCAN["files"]), "≥50",
        SCAN["files"] >= 50)
control("K14", "I↔Q 口径互换自洽（E04 非声明性）",
        dfmt_I(D_ZP), "M^1 L^4 T^-5 I^-2",
        dfmt_I(D_ZP) == "M^1 L^4 T^-5 I^-2")

# ============================================================
# 16. 修复定价
# ============================================================
DEFECTS = {
    "d1_force_identity": True,
    "d2_alpha_identity": True,
    "d3_zpp_dim": True,
    "d4_zpp_ineffective": True,
    "d5_zp_dual": True,
    "d6_script_conclusion": True,
    "d7_naming": True,
}
FIXES = [
    ("R1 明示力比公式与库仑-牛顿比恒等，撤「实验值 / 0.00%」的证据地位",
     ["d1_force_identity"], 1),
    ("R2 明示 α 式是 α 标准定义的重排，撤「验证推导正确性」措辞",
     ["d2_alpha_identity"], 1),
    ("R3 更正 Z'' 的量纲为 [M³L⁴T⁻³Q⁻²]", ["d3_zpp_dim"], 1),
    ("R4 把 Z'' 换成唯一可行形式（或承认 f 需另行处理）",
     ["d4_zpp_ineffective"], 1),
    ("R5 Z' 双定义改名（修正版另称 Z''，不得沿用 Z'）", ["d5_zp_dual"], 1),
    ("R6 脚本结论改由 if 分支驱动（不再顶层无条件 print）",
     ["d6_script_conclusion"], 1),
    ("R7 撤「从时空几何导出」措辞（承认 Z'、Z 内嵌 ε₀、G）", ["d7_naming"], 1),
]
N_FIX = len(FIXES)
loose_pass = 0
strict_pass = 0
zero_cost_pass = 0
min_cost_strict = None
for mask in range(1 << N_FIX):
    fixed = set()
    cost = 0
    for i in range(N_FIX):
        if mask & (1 << i):
            fixed.update(FIXES[i][1])
            cost += FIXES[i][2]
    remaining = [d for d in DEFECTS if d not in fixed]
    loose = not remaining
    keep_claim = not (mask & (1 << 0))    # 未采用 R1
    has_new = (mask & (1 << 3))           # 采用 R4
    strict = loose and keep_claim and has_new
    if loose:
        loose_pass += 1
    if strict:
        strict_pass += 1
        if min_cost_strict is None or cost < min_cost_strict:
            min_cost_strict = cost
    if loose and cost == 0:
        zero_cost_pass += 1
REPAIR_TOTAL = 1 << N_FIX
REPAIR_ROWS = [
    {"档位": "宽松（仅要求内部自洽且无错误声称）", "通过组合": loose_pass,
     "总组合": REPAIR_TOTAL},
    {"档位": "严格（还要求「Z'/Z 解释力比」立论存活且有非恒等内容）",
     "通过组合": strict_pass, "总组合": REPAIR_TOTAL},
    {"档位": "零代价（不改任何式）", "通过组合": zero_cost_pass,
     "总组合": REPAIR_TOTAL},
]

add("F01",
    "修复定价：%d 组合中宽松 %d / 严格 %d / 零代价 %d"
    % (REPAIR_TOTAL, loose_pass, strict_pass, zero_cost_pass),
    "FAIL",
    note="严格档要求「保住 Z'/Z 解释力强度差异的立论」+「有非恒等的可证伪内容」"
         "+「全部缺陷清零」。R1（承认力比恒等）与「保住立论」互斥 ⇒ 严格档 %d；"
         "最小代价（严格档）= %s。"
         % (strict_pass, min_cost_strict if min_cost_strict is not None
            else "不存在"),
    loose=loose_pass, strict=strict_pass, zero_cost=zero_cost_pass)

# ============================================================
# 17. 守卫（全部真算）
# ============================================================
guard("G1 力比恒等：三组残差机器零且 (Z'/Z) ≡ 1/(4πε₀G)",
      FORCE_IDENTICAL and RATIO_ALGEBRA_OK and RATIO_DIM_OK,
      "max=%s algebra=%s dim=%s" % (fs(FORCE_MAX_RES, 3), RATIO_ALGEBRA_OK,
                                    RATIO_DIM_OK))
guard("G2 扰动负对照有效", abs(PERT_RES - PERT) / PERT < Decimal("1e-6"),
      "pert=%s" % fs(PERT_RES, 4))
guard("G3 α 两路径恒等且命中 CODATA",
      ALPHA_IDENTICAL and abs(ALPHA_VS_EXPT) < Decimal("1e-6"),
      "ident=%s vs_expt=%s" % (fs(ALPHA_REL, 3), fs(ALPHA_VS_EXPT, 4)))
guard("G4 Z'' 自称量纲 ≠ 实算（差 L⁶T⁻⁸）",
      D_ZPP != D_ZPP_CLAIM and ddiv(D_ZPP, D_ZPP_CLAIM) == dim(l=6, t=-8),
      "gap=%s" % dfmt(ddiv(D_ZPP, D_ZPP_CLAIM)))
guard("G5 Z'' 未达目的（f 量纲仍 ≠ [M Q⁻¹]）", D_F_WITH_ZPP != D_F_TARGET,
      "f=%s target=%s" % (dfmt(D_F_WITH_ZPP), dfmt(D_F_TARGET)))
guard("G6 需求解唯一且靶文形式不在解集中",
      bool(SOL_UNIQUE) and (not TGT_IN_SOLUTION),
      "sol=%s hits=%d tgt_in=%s" % (_sol_txt, len(EXH_HITS), TGT_IN_SOLUTION))
guard("G7 需求解代回后 f 量纲命中目标", NEED_CHECK_OK,
      "check=%s" % dfmt(D_F_CHECK))
guard("G8 Z' 双口径按文件去重后并存且数值差 > 1e10",
      ZP_DUAL_DEFS and ZP_DUAL_RATIO > Decimal("1e10"),
      "orig=%d corr=%d ratio=%s" % (F_ZP_ORIG, F_ZP_CORR, fs(ZP_DUAL_RATIO, 4)))
guard("G9 量纲自检 4/4 且 I↔Q 互换自洽",
      DIM_SELF_OK and dfmt_I(D_ZP) == "M^1 L^4 T^-5 I^-2",
      "self=%s I_form=%s" % (DIM_SELF_OK, dfmt_I(D_ZP)))
guard("G10 控制组 14/14 全绿（防声明性假绿）", all(c["ok"] for c in CONTROLS),
      "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
GROUP_EXPECT = {"A": 4, "B": 4, "C": 3, "D": 4, "E": 5, "F": 1}
N_BY_GROUP = {}
for _it in ITEMS:
    _p = _it["id"][0]
    N_BY_GROUP[_p] = N_BY_GROUP.get(_p, 0) + 1
guard("G11 条目结构：%s（合计 %d）"
      % (" ".join("%s=%d" % (k, N_BY_GROUP.get(k, 0))
                  for k in sorted(GROUP_EXPECT)), len(ITEMS)),
      N_BY_GROUP == GROUP_EXPECT and len(ITEMS) == sum(GROUP_EXPECT.values()),
      "got=%s" % N_BY_GROUP)
guard("G12 靶文宣称命中：0.00%% 措辞 %d 处、结论性措辞 %d 处"
      % (N_ZERO_ERROR, N_CORRECT_CLAIM), N_ZERO_ERROR >= 1,
      "zero_err=%d claims=%d" % (N_ZERO_ERROR, N_CORRECT_CLAIM))
guard("G13 扫描规模与双定义命中", SCAN["files"] >= 50 and ZP_DUAL_DEFS,
      "files=%d orig=%d corr=%d" % (SCAN["files"], F_ZP_ORIG, F_ZP_CORR))
guard("G14 PASS 条目含真计算（C01 的 Z' 精算命中 1e−5）",
      abs(Z_REL) < Decimal("1e-5"), "rel=%s" % fs(Z_REL, 3))


def summarize():
    cnt = {}
    for it in ITEMS:
        cnt[it["status"]] = cnt.get(it["status"], 0) + 1
    return cnt


class Tee(object):
    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            try:
                st.write(s)
            except Exception:
                pass
        return len(s)

    def flush(self):
        for st in self.streams:
            try:
                st.flush()
            except Exception:
                pass


def main():
    t0 = T_START
    cnt = summarize()
    _rp = os.path.join(OUT, STEM + "_report.txt")
    _orig = sys.stdout
    _rf = None
    try:
        os.makedirs(OUT, exist_ok=True)
        _rf = io.open(_rp, "w", encoding="utf-8")
        sys.stdout = Tee(_orig, _rf)
    except Exception:
        _rf = None

    print("=" * 78)
    print("TUFT-r180｜S17-3.20 电磁光速几何耦合常数 Z' = c/(8πε₀)"
          "—— 恒等力比 / Z'' 修正 / Z' 双口径 / 脚本方法论")
    print("=" * 78)
    print("靶文: %s" % os.path.relpath(TARGET, BASE).replace("\\", "/"))
    print("读取: %s  行数=%d  形态命中: %s"
          % ("OK" if READ_OK else "FAIL", N_LINES,
             ", ".join("%s=%d" % (k, v) for k, v in HIT.items())))
    print("-" * 78)
    for it in ITEMS:
        print("[%s] %s  %s" % (it["status"], it["id"], it["title"]))
        if it["note"]:
            print("       · %s" % it["note"])
        if it["metrics"]:
            kv = ", ".join("%s=%s" % (k, v)
                           for k, v in sorted(it["metrics"].items()))
            print("       · %s" % kv)
    print("-" * 78)
    print("力强度比（三组粒子）:")
    for r in FORCE_ROWS:
        print("  %-10s 理论=%-14s 「实验值」=%-14s 残差=%s"
              % (r["pair"], r["theory"], r["experiment_labelled"],
                 r["rel_residual"]))
    print("  (Z'/Z) = %s ；1/(4πε₀G) 恒等式残差 = %s"
          % (fs(RATIO_EXACT, 8), fs(RATIO_NUM_OK, 3)))
    print("  扰动 1e−3 后残差 = %s（判据判别力）" % fs(PERT_RES, 4))
    print("-" * 78)
    print("常数与量纲:")
    print("  Z' 精算 = %s  (宣称 %s，相对差 %s)"
          % (fs(ZP_EXACT, 10), fs(ZP_CLAIM, 6), fs(Z_REL, 3)))
    print("  Z'/Z    = %s  (宣称 %s，相对差 %s)"
          % (fs(RATIO_EXACT, 8), fs(RATIO_CLAIM, 6), fs(RATIO_REL, 3)))
    print("  若用 19 号靶 Z=1.00065e−2 ⇒ Z'/Z = %s" % fs(RATIO_ALT, 8))
    print("  Z''     = %s  ；Z'/Z'' = %s 倍（双口径差）"
          % (fs(ZPP_EXACT, 8), fs(ZP_DUAL_RATIO, 6)))
    print("  [Z''] 实算 = %s ；自称 = %s ；差 = %s"
          % (dfmt(D_ZPP), dfmt(D_ZPP_CLAIM), dfmt(ddiv(D_ZPP, D_ZPP_CLAIM))))
    print("  f 用 Z''  = %s（I 口径 %s） vs 要求 %s"
          % (dfmt(D_F_WITH_ZPP), dfmt_I(D_F_WITH_ZPP), dfmt(D_F_TARGET)))
    print("  f 用 Z'   = %s（I 口径 %s，靶文自评 [M^-1 L I] 一致）"
          % (dfmt(D_F_WITH_ZP), dfmt_I(D_F_WITH_ZP)))
    print("  使命题成立的唯一 Z'' 形式 = %s（穷举 %d 组命中 %d）"
          % (_sol_txt, 9 ** 4, len(EXH_HITS)))
    print("  α 路径：2e²Z'/(ħc²) = %s ；e²/(4πε₀ħc) = %s ；相对差 %s"
          % (fs(ALPHA_FROM_ZP, 12), fs(ALPHA_STD, 12), fs(ALPHA_REL, 3)))
    print("-" * 78)
    print("验证脚本 ast 审计（%d 份）:" % N_CODE)
    for r in CODE_AUDIT:
        print("  %-28s 行=%-5d 计算节点=%-5d if=%-3d 顶层常量结论=%d"
              % (r["file"], r["lines"], r["calc_nodes"], r["if_nodes"],
                 r["top_const_conclusion"]))
        for h in r["hardcoded"][:2]:
            print("        · 「%s」" % h)
    print("  不可复现依赖: %s" % (", ".join(DEP_MISSING) or "无"))
    print("-" * 78)
    print("扫描（%d 个文件）：Z' 原始定义 %d 文件 / 修正定义 %d 文件 / Z 数值两口径 %d 文件"
          % (SCAN["files"], F_ZP_ORIG, F_ZP_CORR, F_Z_VAL))
    print("-" * 78)
    print("修复定价（7 维 × %d 组合）:" % REPAIR_TOTAL)
    for r in REPAIR_ROWS:
        print("  %-46s %s / %s" % (r["档位"], r["通过组合"], r["总组合"]))
    print("-" * 78)
    for c in CONTROLS:
        print("  [ctl%s] %-46s 值=%-22s 期望=%-12s"
              % ("OK" if c["ok"] else "NG", c["desc"][:46], c["value"],
                 c["expect"]))
    for g in GUARDS:
        print("  [grd%s] %-52s %s"
              % ("OK" if g["ok"] else "NG", g["name"][:52], g["detail"]))
    n_guard_ok = sum(1 for g in GUARDS if g["ok"])
    n_ctl_ok = sum(1 for c in CONTROLS if c["ok"])
    print("-" * 78)
    print("条目 %d：%s" % (len(ITEMS),
                          "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt))))
    print("控制 %d/%d   守卫 %d/%d   用时 %.2fs"
          % (n_ctl_ok, len(CONTROLS), n_guard_ok, len(GUARDS), time.time() - t0))

    payload = {
        "stem": STEM, "round": "r180",
        "target": os.path.relpath(TARGET, BASE).replace("\\", "/"),
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "text_scan": {"lines": N_LINES, "forms": HIT,
                      "zero_error_claims": N_ZERO_ERROR,
                      "conclusion_claims": N_CORRECT_CLAIM},
        "verdict": {
            "core": "力强度比公式与库仑-牛顿比恒等（三组残差机器零），「实验值」"
                    "实为同一批 CODATA 常数的另一写法；α = 2e²Z'/(ħc²) 是 α 标准"
                    "定义的恒等重排却被当作推导正确性的证据；修正常数 Z'' 的自称"
                    "量纲差 L⁶T⁻⁸ 且未达成其自称目的，唯一可行形式是 ħ⁰c³ε₀G²；"
                    "同一符号 Z' 承载两个相差 5.79e17 倍的定义；四份验证脚本的结论"
                    "由顶层常量 print 输出、与计算解耦。",
            "defects": [
                "力比公式恒等（零判别力，0.00% 是算术必然）",
                "「实验值」栏非实验数据（同为 CODATA 常数重排）",
                "α 式恒等重排被当作验证证据",
                "Z'' 自称量纲错（差 L⁶T⁻⁸）",
                "Z'' 未使 f 量纲达标（ħ/c/G 指数结构性错位）",
                "Z' 双口径（1.3472e18 vs 2.3281，差 5.79e17）",
                "验证脚本结论与计算解耦",
            ],
            "favourable": [
                "Z' = c/(8πε₀) 的数值与量纲全对（相对差 <1e−5）",
                "Z'/Z 量纲 [M²Q⁻²] 与力比无量纲的声称正确",
                "Z、Z'、Z'/Z、力比四项量纲分析全对",
                "对 f 量纲不一致的诊断正确（与 r168 独立同证）",
                "主动区分 A_g / A_m 符号（自我纠错）",
            ],
        },
        "constants": {
            "Z_exact_Gc_over_2": str(Z_EXACT), "Z_claim_main": str(Z_CLAIM_MAIN),
            "Z_claim_19": str(Z_CLAIM_19),
            "Zprime_exact": str(ZP_EXACT), "Zprime_claim": str(ZP_CLAIM),
            "Zprime_rel": str(Z_REL),
            "ratio_exact": str(RATIO_EXACT), "ratio_claim": str(RATIO_CLAIM),
            "ratio_rel": str(RATIO_REL), "ratio_alt_with_19_Z": str(RATIO_ALT),
            "Zpp_exact": str(ZPP_EXACT), "Zp_over_Zpp": str(ZP_DUAL_RATIO),
            "alpha_from_Zprime": str(ALPHA_FROM_ZP),
            "alpha_standard": str(ALPHA_STD),
            "alpha_identity_rel": str(ALPHA_REL),
            "alpha_vs_codata_rel": str(ALPHA_VS_EXPT),
        },
        "force_ratio": FORCE_ROWS,
        "identity_checks": {
            "force_max_residual": str(FORCE_MAX_RES),
            "ratio_equals_1_over_4pi_eps0_G": RATIO_ALGEBRA_OK,
            "ratio_num_residual": str(RATIO_NUM_OK),
            "perturbation_1e-3_residual": str(PERT_RES),
            "alpha_identity": ALPHA_IDENTICAL,
        },
        "dimensions": {
            "Z": dfmt(D_Z), "Zprime": dfmt(D_ZP), "ratio": dfmt(D_RATIO),
            "Zpp_actual": dfmt(D_ZPP), "Zpp_claim": dfmt(D_ZPP_CLAIM),
            "Zpp_gap": dfmt(ddiv(D_ZPP, D_ZPP_CLAIM)),
            "f_with_Zpp": dfmt(D_F_WITH_ZPP),
            "f_with_Zpp_I_form": dfmt_I(D_F_WITH_ZPP),
            "f_with_Zprime": dfmt(D_F_WITH_ZP),
            "f_with_Zprime_I_form": dfmt_I(D_F_WITH_ZP),
            "f_target": dfmt(D_F_TARGET),
            "Zpp_needed": dfmt(D_ZPP_NEED),
            "f_check_after_substitution": dfmt(D_F_CHECK),
        },
        "zpp_solution": {
            "exponents": {"hbar": str(SOL[0]) if SOL else None,
                          "c": str(SOL[1]) if SOL else None,
                          "eps0": str(SOL[2]) if SOL else None,
                          "G": str(SOL[3]) if SOL else None},
            "unique": bool(SOL_UNIQUE), "rank": SOL_RANK,
            "exhaustive_hits": len(EXH_HITS),
            "target_form_exponents": TGT_EXP,
            "target_form_in_solution": TGT_IN_SOLUTION,
        },
        "code_audit": CODE_AUDIT,
        "code_deps_missing": DEP_MISSING,
        "scan": {"files_scanned": SCAN["files"],
                 "zprime_orig_files": F_ZP_ORIG,
                 "zprime_corrected_files": F_ZP_CORR,
                 "z_value_files": F_Z_VAL,
                 "samples": {"zp_orig": SCAN["zp_orig"][:6],
                             "zp_corr": SCAN["zp_corr"][:6],
                             "z_vals": SCAN["z_vals"][:6]}},
        "repair_pricing": {"fixes": [{"name": f[0], "cost": f[2],
                                      "fixes": f[1]} for f in FIXES],
                           "rows": REPAIR_ROWS,
                           "min_cost_strict": min_cost_strict},
        "items": ITEMS, "controls": CONTROLS, "guards": GUARDS,
        "counts": cnt,
        "guard_ok": "%d/%d" % (n_guard_ok, len(GUARDS)),
        "control_ok": "%d/%d" % (n_ctl_ok, len(CONTROLS)),
    }
    try:
        os.makedirs(OUT, exist_ok=True)
        jp = os.path.join(OUT, STEM + ".json")
        with io.open(jp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
        print("JSON  -> %s" % jp)

        mp = os.path.join(OUT, STEM + ".md")
        L = []
        L.append("# TUFT-r180 精算摘要")
        L.append("")
        L.append("- 靶：`%s`" % payload["target"])
        L.append("- 条目：%s" % "  ".join("%s=%d" % (k, cnt[k])
                                          for k in sorted(cnt)))
        L.append("- 控制：%d/%d　守卫：%d/%d"
                 % (n_ctl_ok, len(CONTROLS), n_guard_ok, len(GUARDS)))
        L.append("")
        L.append("| 编号 | 状态 | 判定 |")
        L.append("|---|---|---|")
        for it in ITEMS:
            L.append("| %s | %s | %s |"
                     % (it["id"], it["status"],
                        it["title"].replace("|", "\\|")))
        L.append("")
        L.append("## 力强度比（恒等性）")
        L.append("")
        L.append("| 粒子对 | 理论 | 「实验值」 | 残差 |")
        L.append("|---|---|---|---|")
        for r in FORCE_ROWS:
            L.append("| %s | %s | %s | %s |"
                     % (r["pair"], r["theory"], r["experiment_labelled"],
                        r["rel_residual"]))
        L.append("")
        L.append("## 修复定价")
        L.append("")
        L.append("| 档位 | 通过组合 / 总组合 |")
        L.append("|---|---|")
        for r in REPAIR_ROWS:
            L.append("| %s | %s / %s |" % (r["档位"], r["通过组合"],
                                           r["总组合"]))
        L.append("")
        with io.open(mp, "w", encoding="utf-8") as f:
            f.write("\n".join(L) + "\n")
        print("MD    -> %s" % mp)
    except Exception as exc:
        print("[warn] 落盘失败: %s" % exc)

    try:
        sys.stdout = _orig
        if _rf is not None:
            _rf.close()
            print("REPORT-> %s" % _rp)
    except Exception:
        pass

    return 0 if n_guard_ok == len(GUARDS) else 1


if __name__ == "__main__":
    sys.exit(main())
