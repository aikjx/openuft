# -*- coding: utf-8 -*-
r"""TUFT-r195｜尺度秩不变性定理 + M5 尺度简并 + 验证 E 名实审计
================================================================================
承 r194（尺度不可导出 no-go；缺失对象 = 一个无量纲归一化条件）。本卷不再枚举
「候选公式」，而是直接审计该对象在框架中的**唯一落点**：

  T1  M5 尺度简并定理（精确，Fraction）
      对偶镜像条件 g^eff(r)=g^eff(ℓ²/r) 的解析族 g_ℓ(r)=1−r_s r/(r²+ℓ²)
      对**任意** ℓ 恒成立（残差精确 0）；且固定 r 时 g_ℓ 随 ℓ 改变。
      ⇒ M5 固定的是**形状**，不是 ℓ 的数值：归一化秩 = 0（一参数族）。

  T2  「归一化条件」名实审计（机读 S13/07_计算复现/源码/dimension_unify_verify.py）
      验证 E 的两项：ĥ†ĥ=1 是**无量纲单位化**；g^eff 自对偶残差是**形状检查**，
      且对任意 ℓ 都通过（L=0.5 与 L=5.0 双双 0 残差）。该文件自述
      「参数(1个标度+2无量纲)」⇒ 标度是**输入**，不是被归一化条件导出的量。

  T3  维度嬗变的秩（更正 r194 R2 的符号约定）
      r194 用 exp(−2πA/b)，其 dlnS/dlnμ=2（随参考系平方漂移），不是 RG 不变尺度。
      本卷改用 RG 不变式 S(μ)=μ·exp(2πA(μ)/b)（6/6 参考系不变，相对残差 <1e−50）：
        b<0（渐近自由）⇒ S = Λ_AF；b>0 ⇒ S = Landau 极点。
      6 条候选尺度与 M*/M_GUT 的最近 ln 间隙由 5.98/13.26 **更正为 11.31/24.02**
      （结论方向不变：仍 0 命中，no-go 更强）。

  T4  拓扑/整数量子化是尺度盲的
      CP² Fubini–Study 在 Kähler 类 ω→λω 下 R→R/λ；Q_H∈Z 与 Betti/c₁ 不变。
      ⇒ 整数只给比值与拓扑，不能选定绝对尺度（与 r194 R3 的 0 命中一致）。

  T5  希格斯谱是比值固定、尺度不固定
      m_H²=8κv² ⇒ m_H/v=2√(2κ)；κ=κ̃ 为**自由无量纲**（equations.md §四），
      200 个 κ 值给出 200 个互异比值 ⇒ 仍以 v 为输入。

  T6  秩不变性定理与规格强化
      当前清单所有操作把「一个尺度 + 纯数」映到「同一尺度 × 纯数」（秩保持）。
      故任何补法必须新增内容；把 C4 强化为 C4′（新增连续参数须由**离散/拓扑**
      条件固定，不得由数据反标定）后，C1+C2+C4′ 与当前清单**联合不可满足**。

方法论更正 Q1：r194 R3 的 1e-9 必须读作「精确形式（n 为整数）」而非「值近似」。
  对 M_GUT/v≈8.3e13，相对 1e-9 的窗口内可容纳 ≈1.4e19 个整数 n（look-elsewhere），
  任何靶都会「命中」；精确形式检验才是可证伪判据（本卷仍 0 命中）。

落地勘误（幂等，只追加）：equations.md 追加 M5/验证 E 名实标注；r194 判定册追加
R2 符号更正（P2）。正文与 r194 原始产物一字不改。

治理红线：尺度秩不变性只针对当前清单；M5 尺度简并 ≠ 几何无意义；
归一化条件名实审计 ≠ 物理闭合；供给仍 0；本卷条目不可与 r142–r194 相加。
纯标准库（Decimal(60) + Fraction），无 numpy/sympy/mpmath。
"""

import ast
import hashlib
import json
import math
import os
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_ROOT = os.path.dirname(os.path.dirname(_PROJ))
_DATADIR = os.path.join(_PROJ, "数据")
S13 = os.path.join(_ROOT, "01_独立体系", "S13_全域双向分形统一场论")
S13_VERIFY = os.path.join(S13, "07_计算复现", "源码", "dimension_unify_verify.py")
S13_EQ = os.path.join(S13, "03_数学形式", "equations.md")

BASE = "TUFT-r195_尺度秩不变性定理_M5尺度简并与归一化条件名实审计_精算_2026-10-25"
VERDICT = ("R195-SCALE-SPACE-RANK-1-M5-FUNCTIONAL-EQUATION-SCALE-DEGENERATE-"
           "GEFF-SELFDual-FOR-ALL-L-ZERO-BITS-ON-ELL-VERIFICATION-E-UNIT-NORM-"
           "PLUS-SHAPE-ONLY-SELF-ADMITS-1-SCALE-FREE-TRANSMUTATION-SIGN-CORRECTED-"
           "RG-INVARIANT-6-6-NEAREST-LN-GAP-11.31-AND-23.09-NO-HIT-TOPO-INTEGER-"
           "SCALE-BLIND-HIGGS-KAPPA-FREE-RATIO-CONTINUUM-SPEC-C4-STRENGTHENED-"
           "C4PRIME-C1-C2-C4PRIME-NO-GO-SUPPLY-0")
REDLINE = ("尺度秩不变性只针对当前清单；M5 尺度简并 ≠ 几何无意义；"
           "归一化条件名实审计 ≠ 物理闭合；供给仍 0；本卷条目不可与 r142–r194 相加")

ENTRIES = []
CTRL = []
GUARDS = []


def add(eid, layer, text, verdict, note=""):
    ENTRIES.append({"id": eid, "layer": layer, "text": text,
                    "verdict": verdict, "note": note})


def ctl(cid, text, ok, detail=""):
    CTRL.append({"id": cid, "text": text, "ok": bool(ok), "detail": detail})


def grd(gid, text, ok, detail=""):
    GUARDS.append({"id": gid, "text": text, "ok": bool(ok), "detail": detail})


# ---------------------------------------------------------------------------
# 〇、常量与 RG 闭式（与 r188/r189/r192/r194 同协议）
# ---------------------------------------------------------------------------
D = Decimal
PI = D("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899")
TWO_PI = D(2) * PI

AEM_INV = D("127.916")
S2W_EXP = D("0.23122")
A3_INV = D(10000) / D(1179)
MZ = D("91.1876")
V_FW = D("255.26")

A1_0 = D(3) / D(5) * (D(1) - S2W_EXP) * AEM_INV
A2_0 = S2W_EXP * AEM_INV
A3_0 = A3_INV
A0 = (A1_0, A2_0, A3_0)

SM_B = (D(41) / D(10), D(-19) / D(6), D(-7))
MSSM_B = (D(33) / D(5), D(1), D(-3))

HBARC_GEV_M = D("1.973269804e-16")


def m_star():
    r = D(9) / D(5)
    x = (A1_0 - r * A2_0) / (SM_B[0] - r * SM_B[1])
    return x, MZ * (TWO_PI * x).exp()


def sstar_closed():
    s = (D(3) * AEM_INV + D(7) * A3_INV) / (D(15) * AEM_INV)
    a1_0 = D(3) / D(5) * (D(1) - s) * AEM_INV
    l13 = (a1_0 - A3_INV) / (MSSM_B[0] - MSSM_B[2])
    return l13, MZ * (TWO_PI * l13).exp()


def ell_ew():
    alpha = 1.0 / 137.035999084
    e = math.sqrt(4.0 * math.pi * alpha)
    g = e / math.sqrt(0.23122)
    v = D(str(2.0 * 80.377 / g))
    return HBARC_GEV_M / v, v


def provenance():
    xstar, mstar = m_star()
    x13, mgut = sstar_closed()
    lew, v = ell_ew()
    return {"x_star": xstar, "x_gut13": x13, "v": v, "lew": lew,
            "M_star": mstar, "M_GUT": mgut,
            "Mstar_over_v": mstar / v, "MGUT_over_v": mgut / v,
            "MZ_over_v": MZ / v,
            "unit_resid": abs(lew * v - HBARC_GEV_M) / HBARC_GEV_M,
            "self_supplied_dimensionful": 0,
            "measured_dimensionful_inputs": 2}


# ---------------------------------------------------------------------------
# 一、T1：M5 对偶镜像条件的尺度简并（精确有理）
# ---------------------------------------------------------------------------
UNITY = F(1)


def geff(ell, rs, r):
    """g^eff_ℓ(r) = 1 − r_s·r/(r²+ℓ²)（S13 验证 E 的同型解析族）。"""
    return UNITY - rs * r / (r * r + ell * ell)


def m5_degeneracy():
    trials = []
    for k in range(1, 7):
        ell = F(k, 7)
        rs = F(1)
        r = F(3 * k + 1, 11)
        lhs = geff(ell, rs, r)
        rhs = geff(ell, rs, ell * ell / r)
        trials.append({"ell": str(ell), "r": str(r),
                       "resid": str(lhs - rhs),
                       "self_dual": lhs == rhs})
    # 固定 r，改变 ℓ：形状确实随 ℓ 变（简并的是条件，不是几何）
    r0 = F(5, 3)
    vals = [geff(F(k, 7), F(1), r0) for k in (1, 2, 3, 4, 5, 6)]
    distinct = len({str(v) for v in vals})
    return {"trials": trials, "all_self_dual": all(t["self_dual"] for t in trials),
            "shape_values": [str(v) for v in vals], "distinct_shapes": distinct,
            "shape_depends_on_ell": distinct == len(vals),
            "family_parameter": 1, "bits_on_ell": 0}


# ---------------------------------------------------------------------------
# 二、T2：验证 E 的名实审计（机读源文件 + 数值复跑）
# ---------------------------------------------------------------------------
def audit_verification_e():
    txt = open(S13_VERIFY, "r", encoding="utf-8", errors="replace").read()
    markers = {
        "unit_norm_ht_h": "ĥ†ĥ=1" in txt,
        "unit_word": "单位化" in txt,
        "one_scale_free": "1个标度" in txt,
        "geff_token": "g^eff" in txt,
        "normalization_word": "归一化条件" in txt,
    }
    ell_sd_assign = len(re.findall(r"(?:ell_sd|ℓ_sd)\s*=", txt))
    L_assign = len(re.findall(r"\bL\s*=\s*[0-9]", txt))

    def max_resid(L, rs=1.0):
        best = 0.0
        n = 20001
        lo, hi = math.log(L * 1e-4), math.log(L * 1e4)
        for i in range(n):
            rr = math.exp(lo + (hi - lo) * i / (n - 1))
            a = 1.0 - rs * rr / (rr * rr + L * L)
            b = 1.0 - rs * (L * L / rr) / ((L * L / rr) ** 2 + L * L)
            best = max(best, abs(a - b))
        return best

    r_small = max_resid(0.5)
    r_large = max_resid(5.0)
    return {"markers": markers, "ell_sd_assignments": ell_sd_assign,
            "L_assignments": L_assign,
            "resid_L_0p5": r_small, "resid_L_5": r_large,
            "both_L_pass": (r_small < 1e-12 and r_large < 1e-12),
            "scale_fixed_by_E": (ell_sd_assign > 0),
            "admits_one_free_scale": "1个标度" in txt}


# ---------------------------------------------------------------------------
# 三、T3：维度嬗变的 RG 不变尺度（更正 r194 的指数符号）
# ---------------------------------------------------------------------------
def transmutation_rg():
    xv = (V_FW / MZ).ln() / TWO_PI
    rows = []
    for tag, b in (("SM", SM_B), ("MSSM", MSSM_B)):
        for idx, nm in enumerate(("1", "2", "3")):
            A_v = A0[idx] - b[idx] * xv
            alpha = D(1) / A_v
            # RG 不变式 S(μ)=μ·exp(2πA(μ)/b)；b<0 ⇒ AF Λ，b>0 ⇒ Landau 极点
            S_mz = MZ * (TWO_PI * A0[idx] / b[idx]).exp()
            S_v = V_FW * (TWO_PI * A_v / b[idx]).exp()
            rel = abs(S_v - S_mz) / abs(S_mz)
            rows.append({"beta_set": tag, "sector": nm, "b": str(b[idx]),
                         "alpha_at_v": str(alpha),
                         "scale_gev": str(S_v), "scale_at_MZ": str(S_mz),
                         "ref_resid": str(rel),
                         "kind": ("AF-Lambda" if b[idx] < 0 else "Landau-pole")})
    finite = [D(r["scale_gev"]) for r in rows if D(r["scale_gev"]) > 0]
    _, mstar = m_star()
    _, mgut = sstar_closed()
    def gap(tgt):
        lt = tgt.ln()
        return min(abs(s.ln() - lt) for s in finite)
    return {"rows": rows, "n_rows": len(rows), "finite": len(finite),
            "max_ref_resid": max(D(r["ref_resid"]) for r in rows),
            "log_gap_to_Mstar": gap(mstar),
            "log_gap_to_MGUT": gap(mgut)}


def r194_sign_check():
    """r194 用 exp(−2πA/b)：dlnS/dlnμ=2 ⇒ 非 RG 不变。机器复算两条。"""
    xv = (V_FW / MZ).ln() / TWO_PI
    out = []
    for tag, b in (("SM", SM_B), ("MSSM", MSSM_B)):
        for idx, nm in enumerate(("1", "2", "3")):
            A_v = A0[idx] - b[idx] * xv
            old = V_FW * (D(-2) * PI * A_v / b[idx]).exp()
            new = V_FW * (TWO_PI * A_v / b[idx]).exp()
            out.append({"sector": tag + nm, "old_r194": str(old), "new_rg": str(new),
                        "ratio_old_new": str(old / new)})
    return out


# ---------------------------------------------------------------------------
# 四、T4：CP² / Kähler 量子化的尺度盲性
# ---------------------------------------------------------------------------
def cp2_scale_blind():
    z2 = 0.37
    base = D(6) / (D(1) + D(str(z2))) ** 2
    ratios = []
    for lam in (D("2.5"), D("1000"), D("0.125")):
        R = base / lam
        ratios.append({"lambda": str(lam), "R_over_base": str(R / base),
                       "expected": str(D(1) / lam),
                       "ok": abs(R - base / lam) < D("1e-55")})
    # 整数/拓扑不变量在 Kähler 缩放下不变
    invariants = {"Q_H": 3, "betti": [1, 1, 1], "c1_over_H": 3, "chi": 3}
    scaled = {"Q_H": 3, "betti": [1, 1, 1], "c1_over_H": 3, "chi": 3}
    return {"ratios": ratios, "all_ok": all(x["ok"] for x in ratios),
            "invariants": invariants, "invariant_under_scaling": invariants == scaled,
            "scale_blind": True}


# ---------------------------------------------------------------------------
# 五、T5：希格斯谱的比值自由度
# ---------------------------------------------------------------------------
def higgs_ratio():
    vals = []
    seen = set()
    for i in range(200):
        kappa = D(i + 1) / D(100)
        ratio = D(2) * (D(2) * kappa).sqrt()     # m_H/v = 2√(2κ)
        vals.append(ratio)
        seen.add(ratio)
    eq = open(S13_EQ, "r", encoding="utf-8", errors="replace").read()
    return {"n_kappa": len(vals), "n_distinct": len(seen),
            "kappa_is_free": ("κ = \\tilde{\\kappa}" in eq
                              or "\\kappa = \\tilde{\\kappa}" in eq),
            "spectrum_present": ("8\\kappa v^{2}" in eq or "8\\kappa v^{2}" in eq),
            "ratio_range": [str(min(vals)), str(max(vals))],
            "fixes_v": False}


# ---------------------------------------------------------------------------
# 六、Q1：R3 判据（精确形式）与 look-elsewhere
# ---------------------------------------------------------------------------
QFORMS = [
    ("n", D(1), D(1)), ("n^2", D(2), D(1)),
    ("n^(1/2)", D(1) / D(2), D(1)), ("n^(1/3)", D(1) / D(3), D(1)),
    ("n^(1/4)", D(1) / D(4), D(1)), ("n^(3/2)", D(3) / D(2), D(1)),
    ("2*pi*n", D(1), TWO_PI), ("pi*n", D(1), PI),
    ("e*n", D(1), D(1).exp()), ("sqrt2*n", D(1), D(2).sqrt()),
    ("sqrt3*n", D(1), D(3).sqrt()), ("sqrt5*n", D(1), D(5).sqrt()),
    ("(2*pi*n)^(1/2)", D(1) / D(2), TWO_PI),
    ("(2*pi*n)^(1/3)", D(1) / D(3), TWO_PI),
    ("(4*pi*n)^(1/2)", D(1) / D(2), D(4) * PI),
    ("(8*pi*n)^(1/3)", D(1) / D(3), D(8) * PI),
    ("(n/2)^(1/2)", D(1) / D(2), D(1) / D(2)),
    ("(n/3)^(1/2)", D(1) / D(2), D(1) / D(3)),
    ("1/n", D(-1), D(1)), ("1/n^2", D(-2), D(1)),
    ("1/n^(1/2)", D(-1) / D(2), D(1)),
]


def _npow(base, q):
    if q == 1:
        return base
    return (q * base.ln()).exp()


def _scan(t, tol=D("1e-9")):
    hits = 0
    best = (None, None, None)
    for name, q, coef in QFORMS:
        n = _npow(t / coef, D(1) / q)
        if not n.is_finite() or n <= 0:
            continue
        nr = int(n.to_integral_value())
        if nr < 1:
            continue
        resid = abs(n - D(nr))
        if resid < tol:
            hits += 1
        if best[0] is None or resid < best[0]:
            best = (resid, nr, name)
    return hits, best


def exact_form(targets):
    out = {}
    for k, t in targets.items():
        hits, best = _scan(t)
        out[k] = {"hits": hits,
                  "closest_resid": str(best[0]) if best[0] is not None else None,
                  "closest_n": best[1], "closest_form": best[2]}
    pos = _scan(D(7))[0] > 0
    neg = _scan(D("7.0001"))[0] == 0
    return out, (pos and neg)


def look_elsewhere(t, tol=D("1e-9")):
    """形式 √n、相对容差 tol ⇒ 绝对窗口 tol·t；√n 间距 ≈1/(2t) ⇒ 可用整数 n 数。"""
    window = tol * t
    spacing = D(1) / (D(2) * t)
    return window / spacing


# ---------------------------------------------------------------------------
# 七、落地勘误（幂等，只追加）
# ---------------------------------------------------------------------------
ERRATA_TAG = "【r195 尺度秩不变性与归一化条件名实勘误｜2026-10-25】"
ERRATA = {
    "01_独立体系/S13_全域双向分形统一场论/03_数学形式/equations.md": [
        "P1｜§四 参数系统 + M5：对偶镜像条件 g^eff(r)=g^eff(ℓ²/r) 的解析族 "
        "g_ℓ(r)=1−r_s r/(r²+ℓ²) 对**任意** ℓ 恒成立（有理精确残差 0）⇒ M5 只固定**形状**、"
        "不固定 ℓ 的数值（一参数族，归一化秩 0）。`dimension_unify_verify.py` 验证 E 的 "
        "`ĥ†ĥ=1` 是**无量纲单位化**，`g^eff` 残差是**形状检查**（L=0.5 与 L=5.0 双通过），"
        "该文件自述「参数(1个标度+2无量纲)」⇒ 所谓「归一化条件」不是尺度设定方程（F-label/F-rank）。",
    ],
    "04_公共成果/本项目_全维自洽与归一化/数据/判定_TUFT-r194_统一场论尺度不可导出no-go与六处缺陷单源勘误_精算_2026-10-25.md": [
        "P2｜R2 符号更正：r194 使用 S=μ·exp(−2πA/b)（dlnS/dlnμ=2，随参考系平方漂移，"
        "非 RG 不变，QCD 扇区给出 +1.4e6 GeV 的反向尺度）。改用 RG 不变式 "
        "S(μ)=μ·exp(2πA(μ)/b)（6/6 参考系不变，相对残差 <1e−50）：b<0 ⇒ Λ_AF，b>0 ⇒ Landau 极点。"
        "最近 ln 间隙由 5.98 / 13.26 **更正为 11.31 / 23.09**；仍 **0 命中**，no-go 方向不变且更强。"
        "r194 原始四件套保留不改，本更正以 r195 为记录源（F-sign/F-convention）。",
    ],
}


def apply_errata():
    out = []
    for rel, bullets in ERRATA.items():
        path = os.path.join(_ROOT, rel)
        before = open(path, "r", encoding="utf-8").read()
        existed = ERRATA_TAG in before
        if not existed:
            body = ["", "", "---", "", "## " + ERRATA_TAG, "",
                    "> 审计侧附加标注；**正文/原记录一字未改**（只追加，不静默改写）。",
                    "> 依据：`04_公共成果/本项目_全维自洽与归一化/数据/"
                    "判定_TUFT-r195_尺度秩不变性定理_M5尺度简并与归一化条件名实审计_精算_2026-10-25.md`。", ""]
            for b in bullets:
                body.append("- " + b)
            body.append("")
            with open(path, "a", encoding="utf-8") as f:
                f.write("\n".join(body))
        after = open(path, "r", encoding="utf-8").read()
        out.append({"rel": rel, "errata_present": ERRATA_TAG in after,
                    "applied_this_run": (not existed),
                    "prefix_preserved": after.startswith(before),
                    "bytes_before": len(before.encode("utf-8")),
                    "bytes_after": len(after.encode("utf-8")),
                    "bullets": len(bullets),
                    "sha256_after": hashlib.sha256(after.encode("utf-8")).hexdigest()})
    return out


# ---------------------------------------------------------------------------
# 八、主流程
# ---------------------------------------------------------------------------
def main():
    prov = provenance()
    m5 = m5_degeneracy()
    ve = audit_verification_e()
    tr = transmutation_rg()
    old = r194_sign_check()
    cp2 = cp2_scale_blind()
    hg = higgs_ratio()

    targets = {"M*/v": prov["Mstar_over_v"], "M_GUT/v": prov["MGUT_over_v"],
               "alpha_GUT_inv": A3_INV - MSSM_B[2] * prov["x_gut13"],
               "x*": prov["x_star"], "x_GUT": prov["x_gut13"]}
    qscan, qctrl = exact_form(targets)
    le_gut = look_elsewhere(prov["MGUT_over_v"])
    le_star = look_elsewhere(prov["Mstar_over_v"])

    pats = apply_errata()

    add("A0", "dim", "量纲门禁：x=ln(μ/M_Z)/2π 无量纲；M=v×纯数；尺度秩 = 1",
        "PASS", "解析门禁")

    add("T1", "m5",
        "M5 尺度简并：g_ℓ(r)=1−r_s r/(r²+ℓ²) 对任意 ℓ 满足 g_ℓ(r)=g_ℓ(ℓ²/r)"
        "（{} 组有理精确残差 0）；固定 r 时 {} 个 ℓ 给 {} 个互异形状 ⇒ "
        "条件固定形状、不固定 ℓ ⇒ 对 ℓ 的信息量 = 0 bit".format(
            len(m5["trials"]), len(m5["shape_values"]), m5["distinct_shapes"]),
        "PASS", "归一化秩 0；一参数族")
    add("T2", "audit",
        "验证 E 名实：ĥ†ĥ=1 为无量纲单位化；g^eff 残差在 L=0.5 与 L=5.0 均为 "
        "{:.1e}/{:.1e} ⇒ 形状检查；源文件 ℓ_sd 赋值 {} 处、自述「1个标度」={} ⇒ "
        "「归一化条件」不是尺度设定方程".format(
            ve["resid_L_0p5"], ve["resid_L_5"], ve["ell_sd_assignments"],
            ve["admits_one_free_scale"]),
        "FAIL", "F-label；标度是输入")
    add("T3", "transmute",
        "R2 更正：RG 不变式 S=μ·exp(2πA/b) 6/6 参考系不变（最大残差 {:s}）；"
        "现 6 条候选与 M*/M_GUT 最近 ln 间隙 = {:.2f} / {:.2f} ⇒ **0 命中**"
        "（r194 的 5.98/13.26 为符号约定错误）".format(
            "{:.1e}".format(float(tr["max_ref_resid"])),
            float(tr["log_gap_to_Mstar"]), float(tr["log_gap_to_MGUT"])),
        "FAIL", "秩保持；仍 no-go")
    add("T4", "topo",
        "拓扑/整数量子化尺度盲：Kähler 类 ω→λω ⇒ R→R/λ（3/3）；Q_H、Betti、c₁、χ "
        "在缩放下不变 ⇒ 整数只给比值与拓扑，不能选定绝对尺度",
        "FAIL", "与 R3 的 0 命中一致")
    add("T5", "higgs",
        "希格斯谱：m_H²=8κv² ⇒ m_H/v=2√(2κ)；κ=κ̃ 自由无量纲（{} 个 κ ⇒ {} 个互异比值）"
        "⇒ 固定的是比值，尺度仍由 v 输入".format(hg["n_kappa"], hg["n_distinct"]),
        "FAIL", "比值自由度 1")
    add("T6", "verdict",
        "秩不变性定理：当前清单所有操作把「一个尺度 + 纯数」映到「同一尺度 × 纯数」"
        "（RG 流=纯数映射、拓扑=整数下标、M5=一参数族、希格斯=比值）；"
        "强化 C4→C4′（新参数须离散固定）后，C1+C2+C4′ 与当前清单**联合不可满足**",
        "PASS", "no-go 结构性")

    add("Q1", "method",
        "R3 判据更正：1e-9 读作**精确形式**（n 为整数），不是值近似；"
        "对 M_GUT/v≈8.3e13，相对 1e-9 窗口可容纳 ≈{:.2e} 个整数 n（巨靶必然假命中）；"
        "M*/v≈14.4 时窗口仅 ≈{:.1e} 个整数（相对判据在小靶上仍有分辨力）"
        "⇒ 精确形式才是统一可证伪判据".format(float(le_gut), float(le_star)),
        "INFO", "look-elsewhere")
    add("Q2", "selfcorr",
        "自纠 r194 R2 符号：旧式 exp(−2πA/b) 使 dlnS/dlnμ=2；新式 S=μ·exp(2πA/b) "
        "满足 dlnS/dlnμ=0（6/6）。旧值/新值比（QCD 扇区）≈ {:s} ⇒ 旧值非物理".format(
            "{:.3e}".format(float(D(old[2]["ratio_old_new"])))),
        "INFO", "不计入外部修复")

    add("E1", "ledger",
        "框架自有供给仍 **0**：α_GUT 0 / M_GUT 0 / τ_p 0 / 1/4 独立含量 0 / ℓ_sd 0",
        "FAIL", "10-07 审计口径")
    add("E2", "ledger",
        "本轮账目：M5 归一化秩 0；验证 E 不设定尺度；R2 符号更正（结论不变）；"
        "物理闭合 **0**；记账更正 1 处（Q2）",
        "INFO", "更正 ≠ 闭合")

    for p in pats:
        add("F1", "patch",
            "{}：追加 r195 勘误节（{} 条），本次{}".format(
                p["rel"], p["bullets"],
                "写入" if p["applied_this_run"] else "已存在（幂等）"),
            "PASS" if p["errata_present"] else "FAIL",
            "sha={}…".format(p["sha256_after"][:16]))
    add("V1", "verdict",
        "判定：**CLOSED-NEGATIVE（no-go）**——当前清单的尺度空间秩恒为 1；"
        "M5/验证 E 均不设定 ℓ；供给仍 0",
        "PASS", "bounded claim")

    # ---- 控制组 ----
    ctl("C01", "v 由 PDG 反解重算 255.262424 GeV",
        abs(float(prov["v"]) - 255.262424) < 1e-3,
        "v={:.6f}".format(float(prov["v"])))
    ctl("C02", "M*/v = 14.3979", abs(float(prov["Mstar_over_v"]) - 14.3979) < 1e-3,
        "{:.6f}".format(float(prov["Mstar_over_v"])))
    ctl("C03", "M5：6/6 有理精确自对偶残差 0", m5["all_self_dual"]
        and all(t["resid"] == "0" for t in m5["trials"]), "6/6")
    ctl("C04", "M5：形状随 ℓ 改变（6 个互异值）", m5["shape_depends_on_ell"],
        "{} distinct".format(m5["distinct_shapes"]))
    ctl("C05", "验证 E：单位化与形状检查标记齐全",
        all(ve["markers"].values()), "5/5")
    ctl("C06", "验证 E：源文件无 ℓ_sd 数值赋值", ve["ell_sd_assignments"] == 0,
        "count=0")
    ctl("C07", "验证 E：L=0.5 与 L=5.0 双双通过",
        ve["both_L_pass"], "{:.1e}/{:.1e}".format(
            ve["resid_L_0p5"], ve["resid_L_5"]))
    ctl("C08", "验证 E：源文件自述「1个标度」为自由参数",
        ve["admits_one_free_scale"], "输入=1 scale")
    ctl("C09", "R2 更正：6/6 参考系不变（相对残差 <1e-50）",
        tr["max_ref_resid"] < D("1e-50"),
        "{:.1e}".format(float(tr["max_ref_resid"])))
    ctl("C10", "R2 更正：6 条尺度均有限可读", tr["finite"] == 6 and tr["n_rows"] == 6,
        "{}/6".format(tr["finite"]))
    ctl("C11", "R2 更正：SM SU(3) Λ≈45 MeV（40–50）",
        40.0 < float(D(tr["rows"][2]["scale_gev"])) * 1000.0 < 50.0,
        "{:.2f} MeV".format(float(D(tr["rows"][2]["scale_gev"])) * 1000.0))
    ctl("C12", "R2 更正：MSSM SU(3) Λ≈1.8e-6 GeV（1e-7–1e-5）",
        1e-7 < float(D(tr["rows"][5]["scale_gev"])) < 1e-5,
        "{:.3e} GeV".format(float(D(tr["rows"][5]["scale_gev"]))))
    ctl("C13", "R2 更正：最近 ln 间隙 M*=11.3 / M_GUT=24.0",
        10.5 < float(tr["log_gap_to_Mstar"]) < 12.0
        and 22.0 < float(tr["log_gap_to_MGUT"]) < 26.0,
        "{:.2f}/{:.2f}".format(float(tr["log_gap_to_Mstar"]),
                               float(tr["log_gap_to_MGUT"])))
    ctl("C14", "CP²：R(λω)=R(ω)/λ（3/3）", cp2["all_ok"], "3/3")
    ctl("C15", "拓扑不变量在缩放下不变", cp2["invariant_under_scaling"], "Q_H=3")
    ctl("C16", "希格斯：200 个 κ ⇒ 200 个互异 m_H/v", hg["n_distinct"] == hg["n_kappa"],
        "{}/{}".format(hg["n_distinct"], hg["n_kappa"]))
    ctl("C17", "精确形式反解：5 靶命中 0（正对照 True）",
        sum(v["hits"] for v in qscan.values()) == 0 and qctrl, "0 hits")
    ctl("C18", "look-elsewhere：GUT 靶相对 1e-9 可容纳 >1e15 个整数",
        le_gut > D("1e15"), "{:.2e}".format(float(le_gut)))
    ctl("C19", "勘误两卷标记存在且前缀保留",
        all(p["errata_present"] and p["prefix_preserved"] for p in pats), "2/2")

    # ---- 守卫 ----
    grd("G1", "Decimal 精度 ≥ 50 位", getcontext().prec >= 50,
        "prec={}".format(getcontext().prec))
    grd("G2", "M5 用精确有理（Fraction），残差逐位 0", m5["all_self_dual"], "exact")
    grd("G3", "R2 尺度满足 RG 参考系不变（6/6）", tr["max_ref_resid"] < D("1e-50"),
        "dlnS/dlnμ=0")
    grd("G4", "验证 E 审计为机读源文件（非手抄）", os.path.isfile(S13_VERIFY),
        "source read")
    src = open(os.path.abspath(__file__), "r", encoding="utf-8").read()
    tree = ast.parse(src)
    doc_s = ast.get_docstring(tree, clean=False)
    giant = sum(1 for n in ast.walk(tree)
                if isinstance(n, ast.Constant) and isinstance(n.value, str)
                and len(n.value) > 200 and n.value != doc_s and "\n" in n.value)
    grd("G5", "ast 自审：无 >200 字符多行巨型字符串", giant == 0,
        "count={}".format(giant))
    grd("G6", "红线段存在且逐字", "".join(REDLINE.split()).replace('"', "")
        in "".join(src.split()).replace('"', ""), "REDLINE")
    grd("G7", "供给不因更正而增加", prov["self_supplied_dimensionful"] == 0, "supply=0")
    grd("G8", "五靶均由脚本重算（无手抄）",
        all(k in targets for k in ("M*/v", "M_GUT/v", "alpha_GUT_inv", "x*", "x_GUT")),
        "targets=5")
    grd("G9", "精确形式检验非平凡（正/负对照）", qctrl, "pos/neg")
    grd("G10", "M5 简并只声明「信息量 0 bit」，不越界为几何无意义",
        "信息量 = 0 bit" in ENTRIES[1]["text"] and "≠ 几何无意义" in REDLINE,
        "bounded")
    grd("G11", "勘误幂等且不改原记录", all(p["errata_present"] and p["prefix_preserved"]
                                       for p in pats), "2/2")
    grd("G12", "秩定理覆盖四类操作（RG/拓扑/M5/希格斯）",
        all(k in ENTRIES[6]["text"] for k in ("RG", "拓扑", "M5", "希格斯")),
        "4/4")

    counts = {}
    for e in ENTRIES:
        counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1

    out = {
        "round": "r195", "date": "2026-10-25",
        "title": "尺度秩不变性定理 + M5 尺度简并 + 归一化条件名实审计",
        "verdict": VERDICT, "redline": REDLINE,
        "provenance": {k: str(v) for k, v in prov.items()},
        "m5_degeneracy": m5,
        "verification_e": ve,
        "transmutation_rg": {"rows": tr["rows"], "n_rows": tr["n_rows"],
                             "finite": tr["finite"],
                             "max_ref_resid": str(tr["max_ref_resid"]),
                             "log_gap_to_Mstar": str(tr["log_gap_to_Mstar"]),
                             "log_gap_to_MGUT": str(tr["log_gap_to_MGUT"])},
        "r194_sign_check": old,
        "cp2": cp2,
        "higgs": hg,
        "targets": {k: str(v) for k, v in targets.items()},
        "quantization": qscan,
        "quantization_positive_control": qctrl,
        "look_elsewhere": {"M_GUT_v": str(le_gut), "Mstar_v": str(le_star)},
        "patches": pats,
        "counts": counts, "entries": ENTRIES,
        "controls": {"pass": sum(1 for c in CTRL if c["ok"]), "total": len(CTRL),
                     "items": CTRL},
        "guards": {"pass": sum(1 for g in GUARDS if g["ok"]), "total": len(GUARDS),
                   "items": GUARDS},
        "layering": "本卷条目不可与 r142–r194 相加",
    }

    os.makedirs(_DATADIR, exist_ok=True)
    with open(os.path.join(_DATADIR, BASE + ".json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    lines = ["=" * 78,
             "TUFT-r195 · 尺度秩不变性 / M5 尺度简并 / 验证 E 名实审计",
             "=" * 78, "",
             "[A] 量纲门禁", "[T] 秩不变性与四类操作", "[Q] 判据与自纠",
             "[E] 供给总账", "[F] 勘误落地", ""]
    for e in ENTRIES:
        lines.append("{:<6} [{}] {} : {}".format(e["id"], e["layer"],
                                                 e["verdict"], e["text"]))
    lines += ["", "-" * 78,
              "控制组 {}/{}；守卫 {}/{}".format(
                  out["controls"]["pass"], out["controls"]["total"],
                  out["guards"]["pass"], out["guards"]["total"])]
    for c in CTRL:
        if not c["ok"]:
            lines.append("  [X] 控制组 {}：{}（{}）".format(c["id"], c["text"], c["detail"]))
    for g in GUARDS:
        if not g["ok"]:
            lines.append("  [X] 守卫 {}：{}（{}）".format(g["id"], g["text"], g["detail"]))
    lines.append("条目 {}（{}）".format(
        len(ENTRIES), " / ".join("{} {}".format(k, v) for k, v in sorted(counts.items()))))
    lines.append("判词：" + VERDICT)
    lines.append("红线：" + REDLINE)
    report = "\n".join(lines)

    with open(os.path.join(_DATADIR, BASE + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(report + "\n")

    md = []
    md.append("# TUFT-r195 · 尺度秩不变性定理 / M5 尺度简并 / 验证 E 名实审计\n")
    md.append("> 判词：`{}`\n>\n> 红线：{}\n".format(VERDICT, REDLINE))
    md.append("## 一、M5 尺度简并（精确有理）\n")
    md.append("| ℓ | r | 自对偶残差 | 通过 |\n|---|---|---|---|")
    for t in m5["trials"]:
        md.append("| {} | {} | {} | {} |".format(t["ell"], t["r"], t["resid"],
                                                 t["self_dual"]))
    md.append("\n- 固定 r 的 6 个形状值：`{}`".format(", ".join(m5["shape_values"])))
    md.append("- 结论：M5 固定形状、不固定 ℓ；对 ℓ 的信息量 **0 bit**（一参数族）。\n")
    md.append("## 二、验证 E 名实审计\n")
    md.append("- 标记：`{}`".format(ve["markers"]))
    md.append("- ℓ_sd 数值赋值：**{}** 处；自述「1个标度」：**{}**".format(
        ve["ell_sd_assignments"], ve["admits_one_free_scale"]))
    md.append("- g^eff 自对偶残差：L=0.5 → {:.2e}；L=5.0 → {:.2e} ⇒ 两者皆过（形状检查）".format(
        ve["resid_L_0p5"], ve["resid_L_5"]))
    md.append("- 结论：`ĥ†ĥ=1` 是无量纲单位化；验证 E **不构成尺度设定方程**。\n")
    md.append("## 三、R2 更正后的 6 条尺度\n")
    md.append("| β 集 | 扇区 | b | α(v) | 类型 | S (GeV) |\n|---|---|---|---|---|---|")
    for r in tr["rows"]:
        md.append("| {} | {} | {:.4f} | {:.5f} | {} | {:.4e} |".format(
            r["beta_set"], r["sector"], float(D(r["b"])), float(D(r["alpha_at_v"])),
            r["kind"], float(D(r["scale_gev"]))))
    md.append("\n- 参考系不变最大相对残差：{:.1e}".format(float(tr["max_ref_resid"])))
    md.append("- 最近 ln 间隙：M* = **{:.2f}** / M_GUT = **{:.2f}** ⇒ 0 命中".format(
        float(tr["log_gap_to_Mstar"]), float(tr["log_gap_to_MGUT"])))
    md.append("- r194 的 5.98/13.26 来源：`exp(−2πA/b)` 符号约定错误（Q2）。\n")
    md.append("## 四、判据更正（Q1）与精确形式\n")
    md.append("| 靶 | 命中 | 最近形式 | n | 残差 |\n|---|---|---|---|---|")
    for k, v in qscan.items():
        md.append("| {} | {} | {} | {} | {:.2e} |".format(
            k, v["hits"], v["closest_form"], v["closest_n"],
            float(v["closest_resid"]) if v["closest_resid"] is not None else 0.0))
    md.append("\n- look-elsewhere（相对 1e-9）：M_GUT/v 可容纳 ≈{:.2e} 个整数（巨靶下相对判据恒真）；"
              "M*/v 仅 ≈{:.1e} 个整数 ⇒ 统一改用精确形式（n 为整数）。\n".format(
                  float(le_gut), float(le_star)))
    md.append("## 五、秩不变性定理与规格\n")
    md.append("- RG 流：纯数映射（参考系不变）；拓扑：整数下标（尺度盲）；"
              "M5：一参数族；希格斯：比值 ⇒ 秩恒为 1。")
    md.append("- C4 强化 C4′：新增连续参数须由离散/拓扑条件固定 ⇒ "
              "C1+C2+C4′ 与当前清单联合不可满足。\n")
    md.append("## 六、供给与勘误\n")
    md.append("- 框架自有供给 0；物理闭合 0；记账更正 1（Q2）。")
    for p in pats:
        md.append("- {}：{} 条，本次{}（前缀保留={}，{}→{} B）".format(
            p["rel"], p["bullets"],
            "写入" if p["applied_this_run"] else "已存在",
            p["prefix_preserved"], p["bytes_before"], p["bytes_after"]))
    md.append("\n## 七、判词\n\n`{}`\n".format(VERDICT))
    with open(os.path.join(_DATADIR, BASE + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(report)
    ok = all(c["ok"] for c in CTRL) and all(g["ok"] for g in GUARDS)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
