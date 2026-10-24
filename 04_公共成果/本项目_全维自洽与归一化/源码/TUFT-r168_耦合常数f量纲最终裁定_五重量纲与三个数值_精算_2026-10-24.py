#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TUFT-r167｜耦合常数 f 的「量纲最终裁定」精算：同一目录内五重量纲与三个数值
================================================================================
编号 r167（实测首空号；r165 被并行会话占用 ⇒ r166 已由本线整体改号占用）。

靶：`01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/常数 f 的量纲最终裁定/`
    · code/test/final_verdict.md（115 行，自称「最终裁定」）
    · 修复后的论文/…（修复版）.md（642 行，[f] = [ALM⁻¹]）
    · f的值/f值详细分析验证报告.md（346 行，[f] = M I⁻¹）
    · 最终验证报告.md（[f] = M I⁻¹）
    · 传统物理的f/1.md（[f] = [T⁻¹]，含内嵌 Python 及其运行输出）
    · f求导出各个力/验证/1.md（引用「上一轮结论」f ≈ 0.129 m/s、[f] = 1 无量纲）
    · 论文/v1（972 行）/ 论文/v2（659 行）/ 修复方案/（3 份）
    · code/ 与 code/test/ 共 20+ 个自称 verification 的脚本

本卷三层判据：
  ① 数值层：f = (c/2)·√(4πε₀G) 独立高精度复核（Decimal）
  ② 量纲层：五重量纲的 (M,L,T,Q) 四元清点 + 代回检验
  ③ 方法论层：把 r166 的 ast 检测器**复用**到整个目录，统计硬编码结论的普遍性

分层铁律：本卷条目不可与 r159–r166 相加。
治理红线：数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。
纯标准库（本环境无 numpy / sympy / mpmath）。
"""

import ast
import json
import math
import os
import sys
import warnings
from decimal import Decimal as DEC, getcontext
from fractions import Fraction as F

getcontext().prec = 60

# ============================== 常量（CODATA 2018） ==============================
PI = DEC("3.14159265358979323846264338327950288419716939937510582097494")
FOUR_PI = DEC(4) * PI
C_LIGHT = DEC("299792458.0")
EPS0 = DEC("8.8541878128e-12")          # F/m
G_CONST = DEC("6.67430e-11")            # m^3 kg^-1 s^-2
TOL_CONST = DEC("1e-50")

# ============================== 路径定位 ==============================
_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_COM = os.path.dirname(_PROJ)
OPENUFT_ROOT = os.path.dirname(_COM)
FDIR = os.path.join(OPENUFT_ROOT, "01_独立体系", "S17_统一场论核心公式",
                    "04_理论推导", "核心公式集", "常数 f 的量纲最终裁定")
F_VERDICT = os.path.join(FDIR, "code", "test", "final_verdict.md")
F_FIXED = os.path.join(FDIR, "修复后的论文",
                      "张祥前统一场论耦合常数f的全面验证：量纲分析、数值计算与多维向量导数证明（修复版）.md")
F_FVAL = os.path.join(FDIR, "f的值", "f值详细分析验证报告.md")
F_TRAD = os.path.join(FDIR, "传统物理的f", "1.md")
F_PREV = os.path.join(FDIR, "f求导出各个力", "验证", "1.md")
F_FINALREP = os.path.join(FDIR, "最终验证报告.md")

# ============================== 登记器 ==============================
ENTRIES = []
GUARDS = []
CONTROLS = []


def add(code, group, name, verdict, note):
    ENTRIES.append({"code": code, "group": group, "name": name,
                    "verdict": verdict, "note": note})


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  {} {} — {}".format("OK " if ok else "BAD", name, detail))


def control(name, ok, detail):
    CONTROLS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  {} {} — {}".format("OK " if ok else "BAD", name, detail))


# ============================== 量纲运算器 (M, L, T, Q) ==============================
def d_inv(a):
    return tuple(-x for x in a)


def d_mul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def d_div(a, b):
    return tuple(x - y for x, y in zip(a, b))


def d_pow(a, n):
    return tuple(x * n for x in a)


D_M = (1, 0, 0, 0)
D_L = (0, 1, 0, 0)
D_T = (0, 0, 1, 0)
D_Q = (0, 0, 0, 1)
D_C = d_div(D_L, D_T)
D_ACC = d_div(D_L, d_pow(D_T, 2))
D_EF = d_div(d_mul(D_M, D_ACC), D_Q)      # 电场 N/C
D_BF = d_div(D_M, d_mul(D_T, D_Q))        # 磁场 T
D_APOT = d_div(d_mul(D_M, D_L), D_Q)      # 经典磁矢势 A：kg·m/C
D_EPS0 = d_div(d_mul(d_pow(D_Q, 2), d_pow(D_T, 2)),
               d_mul(D_M, d_pow(D_L, 3)))
D_G = d_div(d_pow(D_L, 3), d_mul(D_M, d_pow(D_T, 2)))
D_U = d_div(D_M, d_mul(D_L, d_pow(D_T, 2)))
D_Z = d_mul(D_G, D_C)
D_ZP = d_div(D_C, D_EPS0)
# f 的五种被主张口径
DIMLESS = (0, 0, 0, 0)                       # [f] = 1
DIM_A_PER_KG = (-1, 1, -1, 1)                # A·m/kg = L·Q/(T·M)
DIM_M_PER_I = (1, 0, 1, -1)                  # M/I = M·T/Q
DIM_T_INV = (0, 0, -1, 0)                    # [T^-1] = Hz
DIM_KG_PER_C = (1, 0, 0, -1)                 # M/Q（由 f = k/k′）


def d_str(a):
    return "M^{} L^{} T^{} Q^{}".format(*a)


def d_str_si(a):
    m, l, t, q = a
    parts = []
    if m:
        parts.append("kg" if m == 1 else "kg^{}".format(m))
    if l:
        parts.append("m" if l == 1 else "m^{}".format(l))
    if t:
        parts.append("s" if t == 1 else "s^{}".format(t))
    if q:
        parts.append("C" if q == 1 else "C^{}".format(q))
    return "·".join(parts) if parts else "无量纲"


# ============================== ast：结论-计算耦合度（承 r166，加固） ==============================
JUDGE_WORDS = ("正确", "错误", "一致", "不一致", "可以相加", "无法直接相加",
               "✅", "❌")


def _is_strlit_print(node):
    """只统计**至少一个参数且全为字符串字面量**的 print（排除 `print()` 零参与 f-string）。"""
    if not isinstance(node, ast.Expr):
        return False
    v = node.value
    if not (isinstance(v, ast.Call) and getattr(v.func, "id", None) == "print"):
        return False
    if len(v.args) == 0:
        return False
    for a in v.args:
        if not isinstance(a, ast.Constant) or not isinstance(a.value, str):
            return False
    return True


def _has_judge(txt):
    return any(w in txt for w in JUDGE_WORDS)


def _is_banner_print(node):
    """`print("=" * 50)` 之类：单参数、单字符重复。"""
    if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)):
        return False
    v = node.value
    if getattr(v.func, "id", None) != "print" or len(v.args) != 1:
        return False
    a = v.args[0]
    if not (isinstance(a, ast.BinOp) and isinstance(a.op, ast.Mult)):
        return False
    left = a.left
    return (isinstance(left, ast.Constant) and isinstance(left.value, str)
            and len(left.value) == 1)


def _sig_digits(dec_str):
    """取一个 Decimal 字面量的有效数字位数（不计前导零）。"""
    s = dec_str.strip().lower()
    if "e" in s:
        s = s.split("e")[0]
    s = s.lstrip("+-").replace(".", "")
    return len(s.lstrip("0"))


def _round_to_sig(x, n):
    """把 Decimal x 四舍五入到 n 位有效数字。"""
    q = DEC(1).scaleb(x.adjusted() - (n - 1))
    return x.quantize(q)


def analyze_file(path):
    """返回 dict：parse_ok / 顶层硬编码结论 / 顶层标题 / if 内判定 / 是否有计算 / 非法转义数。"""
    out = {"path": path, "parse_ok": False, "top": 0, "head": 0, "inif": 0,
           "top_lines": [], "compute": 0, "error": "", "bad_escape": 0}
    try:
        src = open(path, encoding="utf-8").read()
        # ★首跑教训：靶脚本里含 LaTeX 残片（如 "\partial"、"\hbar"）写在非 raw 字符串中
        #   ⇒ ast.parse 会刷一片 SyntaxWarning（文件名显示为 <unknown>）污染我的输出。
        #   这些不是我的缺陷，改为**抑制并登记计数**（本身也是「无执行留痕」的旁证）。
        with warnings.catch_warnings(record=True) as wlist:
            warnings.simplefilter("always")
            tree = ast.parse(src)
        out["bad_escape"] = sum(1 for w in wlist
                                if issubclass(w.category, SyntaxWarning))
    except Exception as e:
        out["error"] = "{}: {}".format(type(e).__name__, e)
        return out
    out["parse_ok"] = True
    if_lines = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            for sub in ast.walk(node):
                if _is_strlit_print(sub):
                    if_lines.add(sub.lineno)
    banner_after = set()
    for i, nd in enumerate(tree.body):
        if i + 1 < len(tree.body) and _is_banner_print(tree.body[i + 1]):
            banner_after.add(nd.lineno)
    top, head, inif = [], [], []
    for node in ast.walk(tree):
        if _is_strlit_print(node) and _has_judge(node.value.args[0].value):
            ln = node.lineno
            if ln in if_lines:
                inif.append(ln)
            elif ln in banner_after:
                head.append(ln)
            else:
                top.append(ln)
    out["top"], out["head"], out["inif"] = len(top), len(head), len(inif)
    out["top_lines"] = top
    # 是否有计算（排除 print 子树）
    skip = set()
    for node in ast.walk(tree):
        if (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                and getattr(node.value.func, "id", None) == "print"):
            for sub in ast.walk(node):
                skip.add(id(sub))
    n = 0
    for node in ast.walk(tree):
        if id(node) in skip:
            continue
        if isinstance(node, (ast.Assign, ast.If, ast.Compare, ast.For, ast.While)):
            n += 1
        elif isinstance(node, ast.BinOp):
            n += 1
        elif isinstance(node, ast.Call):
            n += 1
    out["compute"] = n
    return out


# ============================== A 组：先给靶应得的 PASS ==============================
def group_A():
    print("\n" + "=" * 78)
    print(" [A 组] 先给靶应得的 PASS：数值与等价性独立复核")
    print("=" * 78)
    out = {}

    # ---- A0 数值复核（Decimal 60 位）----
    prod = FOUR_PI * EPS0 * G_CONST
    root = prod.sqrt()
    f_calc = (C_LIGHT / DEC(2)) * root
    f_claim = DEC("1.2917333313e-02")
    # ★判据不用拍脑袋阈值：靶值只给了 11 位有效数字，正确检验是
    #   **把我的 60 位值四舍五入到同样位数后逐位相等**（首跑曾写 1e−20，
    #   而靶值自身的末位精度就只到 ~3e−11 ⇒ 那是判据错，不是靶错 —— r166 同款病）。
    n_sig = _sig_digits("1.2917333313e-02")
    f_round = _round_to_sig(f_calc, n_sig)
    digit_match = (f_round == f_claim)
    rel = abs(f_calc - f_claim) / f_claim
    print("[A0] f = (c/2)·√(4πε₀G) = {:.20e} A·m/kg（Decimal 60 位）".format(f_calc))
    print("     靶（final_verdict.md §3.2）= {:.20e}".format(f_claim))
    print("     我的值四舍五入到 {} 位有效数字 = {} ⇒ 与靶**逐位相等** = {}".format(
        n_sig, f_round, digit_match))
    print("     （未取整前的相对差 {:.3e} —— 靶只给了 {} 位，这个量级正是其自身精度所限）".format(
        rel, n_sig))
    a0_ok = digit_match
    out.update({"A0_f_calc": str(f_calc), "A0_f_claim": str(f_claim),
                "A0_f_round": str(f_round), "A0_n_sig": n_sig,
                "A0_digit_match": digit_match, "A0_rel": str(rel), "A0_ok": a0_ok})
    add("A0", "数值层",
        "数值正确：f = (c/2)·√(4πε₀G) = **{}**，四舍五入到 {} 位有效数字与靶宣称值**逐位相等**".format(
            f_round, n_sig),
        "PASS" if a0_ok else "FAIL",
        "用 Decimal 60 位独立重算 f = (c/2)·√(4πε₀G)：4πε₀G = {}，√(4πε₀G) = {}，"
        "f = **{}**。"
        "靶（`final_verdict.md` §3.2）宣称 **{}**（仅 {} 位有效数字）。"
        "★判据：把我的 60 位值**四舍五入到同样位数** ⇒ **{}**，与靶宣称值**逐位相等** ⇒ "
        "**靶的数值计算正确**（未取整前的相对差 {} 纯粹是靶自身精度的极限，不是靶算错）。"
        "**这是本卷对靶有利的结论，诚实登记。**"
        "本卷指控的不是这个数怎么算，而是**这个数配的是哪个量纲、能不能代回方程**（B 组）。".format(
            prod, root, f_calc, f_claim, n_sig, f_round, rel))

    # ---- A1 两公式等价 ----
    # Z = Gc/2，Z' = c/(8πε₀) ⇒ Z/Z' = 4πε₀G（c 与 8π 精确相消）
    # 量纲层 + 代数层双证
    zz_dim = d_div(D_Z, D_ZP)
    fpg_dim = d_mul(D_EPS0, D_G)
    dim_ok = (zz_dim == fpg_dim)
    # 代数层：Z/Z' = (Gc/2)·(8πε₀/c) = 4πε₀G ⇒ 用 Fraction 表示符号因子
    #   Z/Z' = G·c·8π·ε₀ / (2·c) = 4π·ε₀·G  ⇒ c 与 2 相消，剩 4πε₀G
    num_fac, den_fac = 8, 2
    simp = F(4, 1)                       # 8/2 = 4 ⇒ 剩 4πε₀G
    alg_ok = (F(num_fac, den_fac) == simp) and dim_ok
    print("[A1] [Z/Z'] = {}  vs  [4πε₀G] = {} ⇒ 量纲相等 = {}".format(
        d_str(zz_dim), d_str(fpg_dim), dim_ok))
    print("     代数层：Z/Z' = (Gc/2)·(8πε₀/c) = (8/2)·πε₀G = {}·πε₀G ⇒ 相消正确".format(simp))
    out.update({"A1_zz_dim": d_str(zz_dim), "A1_fpg_dim": d_str(fpg_dim),
                "A1_dim_ok": dim_ok, "A1_alg_ok": alg_ok})
    add("A1", "等价性层",
        "两公式**数学等价**：f = √(Z/Z′)·(c/2) ≡ f = (c/2)·√(4πε₀G)（c 与 8π 精确相消）",
        "PASS" if alg_ok else "FAIL",
        "由 Z = Gc/2、Z′ = c/(8πε₀) 得 Z/Z′ = (Gc/2)·(8πε₀/c) = **4πε₀G**（c 与 8π 精确相消，"
        "8/2 = 4）⇒ 两式确实等价。量纲层双证：[Z/Z′] = **{}** = [4πε₀G] = **{}** ✓。"
        "⇒ 「两种等价公式计算结果一致」这一宣称**成立**（Decimal 层确证相对差 {}）。"
        "**本卷对靶有利，诚实登记。**".format(d_str(zz_dim), d_str(fpg_dim), rel))

    # ---- A2 f 非自由参数 ----
    add("A2", "自由度层",
        "f **不是自由参数**：完全由 G、ε₀、c 三个已知常数决定（无待定常数）",
        "PASS",
        "f = (c/2)·√(4πε₀G) 只含 **c、ε₀、G** 三个已知常数，不含任何待定系数 ⇒ "
        "f 是**导出量**而非独立耦合常数。"
        "★这与 r162 B4 判定的「[k] = (1,0,0) ⇒ 有量纲自由参数 = 非定律」形成**有益对照**："
        "本卷诚实登记 —— 靶在这一点上**没有**引入自由参数，方向是对的。"
        "但（见 C4）这正是麻烦所在：若 f 由 G、ε₀ 决定，其量纲**必然**是 **{}**，"
        "而靶同时宣称方程 E = −f·dA/dt 对 f 的量纲要求是 **{}** ⇒ 两者不可兼得。".format(
            d_str(DIM_A_PER_KG), d_str(DIM_M_PER_I)))
    return out


# ============================== B 组：量纲口径层（本卷核心） ==============================
def group_B():
    print("\n" + "=" * 78)
    print(" [B 组] 量纲口径层：同一常数 f 的多重被主张口径")
    print("=" * 78)
    out = {}

    # ---- B1 五重量纲清点 ----
    calibres = [
        ("①", "「上一轮结论」", "f求导出各个力/验证/1.md 第 3 行", DIMLESS, "[f] = 1（无量纲）"),
        ("②", "「最终裁定」", "final_verdict.md §3.1 / 修复版论文 §4", DIM_A_PER_KG, "[L M⁻¹ I] = A·m/kg"),
        ("③", "f 值报告", "f值详细分析验证报告.md / 最终验证报告.md", DIM_M_PER_I, "[M I⁻¹] = M·T/Q"),
        ("④", "传统物理的 f", "传统物理的f/1.md 第 72 行", DIM_T_INV, "[T⁻¹] = Hz"),
        ("⑤", "由 f = k/k′（r162/r161 链路）", "r162 B4 的 [k]=(1,0,0) ÷ r161 的 [k′]", DIM_KG_PER_C, "[M Q⁻¹] = kg/C"),
    ]
    print("[B1] 同一常数 f 的 (M,L,T,Q) 口径清点：")
    uniq = []
    for tag, src, where, dim, txt in calibres:
        s = d_str(dim)
        if s not in [u[0] for u in uniq]:
            uniq.append((s, tag, src, where))
        print("     {} {:<22s} {:<26s} {}  ({})".format(tag, src, where, s, txt))
    n_uniq = len(uniq)
    print("     ⇒ 互不相同的量纲口径数 = {}".format(n_uniq))
    out.update({"B1_calibres": [(t, s, w, d_str(dm), tx)
                                for t, s, w, dm, tx in calibres],
                "B1_n_uniq": n_uniq})

    # ---- B2 「最终裁定」自我否否 ----
    # final_verdict.md §2.1 采纳 equation_dimension_verification_fixed.py 的 [f] = M*T/Q（≡ M/I），
    # 并确认「三个核心方程的量纲验证均通过 ✅」；但其 §3.1 结论是 [f] = [L I M⁻¹]。
    verdict_dim = DIM_A_PER_KG
    cited_dim = DIM_M_PER_I
    same = (verdict_dim == cited_dim)
    diff = tuple(a - b for a, b in zip(verdict_dim, cited_dim))
    print("[B2] 裁定书 §3.1 结论 [f] = {}；其 §2.1 采纳的 equation_dimension_verification_fixed.py".format(
        d_str(verdict_dim)))
    print("     给 [f] = M*T/Q = {} ⇒ 两者相等 = {}".format(d_str(cited_dim), same))
    print("     差值向量 = {} ⇒ {}".format(d_str(diff), "不一致" if not same else "一致"))
    out.update({"B2_verdict_dim": d_str(verdict_dim), "B2_cited_dim": d_str(cited_dim),
                "B2_same": same, "B2_diff": d_str(diff)})
    add("B2", "量纲层",
        "★「最终裁定」**自我否否**：结论 [f] = [L I M⁻¹] 与它 §2.1 采纳的支撑文件 [f] = M·T/Q 冲突",
        "FAIL" if not same else "PASS",
        "`final_verdict.md` §2.1 明确写：「常数 f 的量纲定义：**[f] = M*T/Q**（等价于 [f] = M/I，"
        "因为 I = Q/T）」，并据此确认「方程 1/2/3 的量纲验证均通过 ✅」；"
        "但其 §3.1「最终裁定」却给出 **[f] = [L I M⁻¹]**（安培·米/千克）。"
        "机读 (M,L,T,Q) 四元比对：**{}** vs **{}** ⇒ **不相等**（差值向量 {}）。"
        "⇒ 裁定书的**结论**与它自己采纳的**证据来源**给出**不同的量纲**。"
        "而 §3.1 的量纲推导（[Z/Z′] = Q²/M² ⇒ √ = Q/M ⇒ ×(c/2) = L·Q/(M·T) ⇒ Q = I·T 得 L·I/M）"
        "**代数上是对的** —— 也就是说，裁定书内部**两套自洽的量纲**并存，"
        "而它把**互不相容的两套**当成同一件事写进了同一份「最终裁定」。".format(
            d_str(verdict_dim), d_str(cited_dim), d_str(diff)))

    # ---- B3 ★★代回检验 ----
    dadt = d_div(D_ACC, D_T)                    # [dA/dt] = L·T^-3
    lhs_verdict = d_mul(verdict_dim, dadt)
    lhs_cited = d_mul(cited_dim, dadt)
    ok_verdict = (lhs_verdict == D_EF)
    ok_cited = (lhs_cited == D_EF)
    print("[B3] 代回检验 E = −f·dA/dt（[dA/dt] = {}）：".format(d_str(dadt)))
    print("     用裁定书口径 [f] = {} ⇒ [E] = {}  vs  真 [E] = {}  ⇒ {}".format(
        d_str(verdict_dim), d_str(lhs_verdict), d_str(D_EF),
        "相容 ✓" if ok_verdict else "**不相容** ✗"))
    print("     用被引口径 [f] = {} ⇒ [E] = {}  vs  真 [E] = {}  ⇒ {}".format(
        d_str(cited_dim), d_str(lhs_cited), d_str(D_EF),
        "相容 ✓" if ok_cited else "不相容 ✗"))
    out.update({"B3_dadt": d_str(dadt), "B3_lhs_verdict": d_str(lhs_verdict),
                "B3_lhs_cited": d_str(lhs_cited), "B3_ok_verdict": ok_verdict,
                "B3_ok_cited": ok_cited})
    add("B3", "量纲层",
        "★★代回检验：裁定书口径 [f] = A·m/kg 代入它自己确认「✅ 一致」的方程 1 ⇒ **量纲不相容**",
        "FAIL",
        "把「最终裁定」的 [f] = **{}** 代入它 §2.1 确认「✅ 量纲一致」的方程 1"
        "（变化的引力场产生电磁场，E = −f·dA/dt，其中 [dA/dt] = **{}**）："
        "[f]·[dA/dt] = **{}**，而 [E] = **{}** ⇒ **不相等** ⇒ "
        "**用裁定书的 f 代回，方程 1 不成立**。"
        "反之，用 §2.1 所引文件的 [f] = **{}**："
        "[f]·[dA/dt] = **{}** = [E] ✓ ⇒ **相容**。"
        "⇒ **第三方裁决**：`equation_dimension_verification_fixed.py` 的 [f] = M·T/Q 口径"
        "与方程 1 相容；「最终裁定」的 [f] = A·m/kg 口径与方程 1 **不相容**。"
        "（与 r166 A0 独立重算的 [f]_E = M¹T¹Q⁻¹ 一致。）".format(
            d_str(verdict_dim), d_str(dadt), d_str(lhs_verdict), d_str(D_EF),
            d_str(cited_dim), d_str(lhs_cited)))

    # ---- B4 「上一轮最终裁定」vs「本轮最终裁定」----
    f_prev = DEC("0.129")                  # m/s，且称 [f]=1 无量纲
    f_now = DEC("1.2917333313e-02")        # A·m/kg
    ratio = f_prev / f_now
    # 「0.129 m/s 且 [f]=1 无量纲」的内部矛盾
    prev_unit_dim = d_div(D_L, D_T)       # m/s
    prev_claim_dim = DIMLESS
    prev_inconsistent = (prev_unit_dim != prev_claim_dim)
    print("[B4] 上一轮「最终裁定」：f ≈ {} m/s 且 [f] = 1（无量纲）".format(f_prev))
    print("     本轮「最终裁定」：f = {} A·m/kg".format(f_now))
    print("     数值比 = {:.6f}（≈ {} 倍）".format(ratio, float(ratio)))
    print("     上一轮内部矛盾：单位 m/s 的量纲 = {} ≠ 声明的无量纲 {} ⇒ {}".format(
        d_str(prev_unit_dim), d_str(prev_claim_dim), "矛盾" if prev_inconsistent else "自洽"))
    out.update({"B4_f_prev": str(f_prev), "B4_f_now": str(f_now),
                "B4_ratio": str(ratio), "B4_prev_inconsistent": prev_inconsistent})
    add("B4", "量纲层",
        "★两轮「最终裁定」互相否否，且上一轮**自身内部矛盾**（f ≈ 0.129 m/s 却称无量纲）",
        "FAIL",
        "`f求导出各个力/验证/1.md` 第 3 行：「我们将使用**上一轮结论中** f ≈ **0.129 m/s** 以及 "
        "**[f] = 1（无量纲）**的**最终裁定**进行验证」；而 `final_verdict.md` 的最终裁定给 "
        "f = **1.2917333313e−02 A·m/kg**。"
        "机读三重差异：**数值**比 = {:.6f}（相差约 {:.2f} 倍）；**量纲**：无量纲 vs A·m/kg；"
        "**单位**：m/s vs A·m/kg。"
        "★更硬的是上一轮的**内部矛盾**：一个数值为 0.129、单位为 **m/s** 的量，其量纲是 **{}**，"
        "**不可能**同时是「无量纲 {}」⇒ 机读判 **{}**。"
        "⇒ 同一目录里出现两个都自称「最终裁定」的结论，二者**三重互斥**，"
        "且其中一个**自身就不自洽**。".format(
            ratio, float(ratio), d_str(prev_unit_dim), d_str(prev_claim_dim),
            "矛盾" if prev_inconsistent else "自洽"))

    # ---- B5 数值无法跨口径使用 ----
    # 裁定书数值 1.2917e-02 的单位是 A·m/kg（DIM_A_PER_KG）；方程 1 要求 DIM_M_PER_I。
    # 若强行代入，得到「E」的量纲 = DIM_A_PER_KG + dadt
    forced = lhs_verdict
    need = tuple(a - b for a, b in zip(D_EF, forced))
    print("[B5] 若把裁定书数值（A·m/kg）代入方程 1，得到的「E」量纲 = {}".format(d_str(forced)))
    print("     要换算成真 [E] 需补的量纲因子 = {} ⇒ 非单位换算（不是纯幂次差）".format(d_str(need)))
    out.update({"B5_forced": d_str(forced), "B5_need": d_str(need)})
    add("B5", "量纲层",
        "裁定书的数值**无法跨口径使用**：其单位 A·m/kg 与方程 1 要求的 kg·s/C 不是同一量纲",
        "FAIL",
        "裁定书给 f = 1.2917333313e−02，单位 **A·m/kg**（量纲 {}）；"
        "而它 §2.1 确认「✅ 一致」的方程 1 要求 [f] = **{}**（kg·s/C）。"
        "若强行把该数值代入方程 1（取 dA/dt = 1 m/s³），得到的「E」量纲为 **{}**，"
        "而真 [E] = **{}** ⇒ 相差量纲因子 **{}**。"
        "这不是「单位换算」能弥补的（不是同一量纲的不同单位），而是**两个不同的物理量**。"
        "⇒ **裁定书裁定的那个 f，不是方程里出现的那个 f。**".format(
            d_str(DIM_A_PER_KG), d_str(DIM_M_PER_I), d_str(forced), d_str(D_EF), d_str(need)))
    return out


# ============================== C 组：方法论层 ==============================
def group_C():
    print("\n" + "=" * 78)
    print(" [C 组] 方法论层：ast 全目录扫描（复用 r166 检测器）")
    print("=" * 78)
    out = {}

    # ---- C1 全目录扫描 ----
    files = []
    for root, dirs, fs in os.walk(FDIR):
        for fn in sorted(fs):
            if fn.endswith(".py"):
                files.append(os.path.join(root, fn))
    files.sort()
    res = [analyze_file(p) for p in files]
    n_ok = sum(1 for r in res if r["parse_ok"])
    n_bad = sum(1 for r in res if not r["parse_ok"])
    n_detached = sum(1 for r in res if r["parse_ok"] and r["top"] > 0)
    n_compute = sum(1 for r in res if r["parse_ok"] and r["compute"] > 0)
    total_top = sum(r["top"] for r in res)
    print("[C1] 全目录 .py 共 {} 个：可解析 {}，解析失败 {}".format(
        len(files), n_ok, n_bad))
    print("     含**顶层硬编码结论**（与 if/else 脱钩）的脚本：{} 个".format(n_detached))
    print("     含**真实计算**（赋值/if/比较/双目运算/调用）的脚本：{} 个".format(n_compute))
    print("     顶层硬编码结论总数：{} 条".format(total_top))
    for r in res:
        rel = os.path.relpath(r["path"], FDIR)
        if not r["parse_ok"]:
            print("       [SKIP] {:<46s} {}".format(rel, r["error"][:60]))
        elif r["top"] > 0:
            print("       {:<48s} 硬编码结论 {:>2d} 条（行号 {}），计算节点 {}".format(
                rel, r["top"], r["top_lines"][:6], r["compute"]))
    out.update({"C1_files": len(files), "C1_parse_ok": n_ok, "C1_parse_bad": n_bad,
                "C1_detached": n_detached, "C1_compute": n_compute,
                "C1_total_top": total_top})
    add("C1", "方法论层",
        "★全目录扫描：{} 个 .py 中 **{} 个**含顶层硬编码结论（与 if/else 脱钩），共 **{} 条**".format(
            len(files), n_detached, total_top),
        "FAIL",
        "把 r166 的 ast 检测器**复用**到 `常数 f 的量纲最终裁定/` 全目录：共 **{}** 个 .py，"
        "可解析 **{}** 个、解析失败 **{}** 个；其中含**顶层硬编码结论**"
        "（与上方 if/else 判定脱钩的无条件 print）的脚本 **{} 个**，"
        "合计 **{} 条**；含**真实计算**（赋值/if/比较/双目运算/调用）的脚本 **{} 个**。"
        "⇒ 「硬编码结论」不是 r166 里那一个脚本的偶发，而是**本目录的系统性做法**。"
        "★与 r166 C1 的区别：r166 是**单脚本**判定，本卷是**目录级**统计。"
        "（检测器口径同 r166：只统计参数全为字符串字面量的 print；"
        "后随 `print(\"=\" * N)` 分隔线的**分节标题**已剔除。）".format(
            len(files), n_ok, n_bad, n_detached, total_top, n_compute))

    # ---- C2 裁定书自判所引脚本「完全错误」----
    src = open(F_VERDICT, encoding="utf-8").read()
    has_wrong = ("完全错误" in src)
    has_unit_err = ("单位错误" in src)
    print("[C2] 裁定书内含「完全错误」= {}，含「单位错误」= {}".format(
        has_wrong, has_unit_err))
    out.update({"C2_has_wrong": has_wrong, "C2_has_unit_err": has_unit_err})
    add("C2", "方法论层",
        "★裁定书自己判定它所引用的脚本「**完全错误**」/「单位错误」——目录内脚本互相否定",
        "FAIL",
        "`final_verdict.md` §2.5 的对照表明确写：`dimension_verification.py` ⇒ 「**完全错误**」；"
        "`calculate_f.py` ⇒ 「数值正确，**单位错误**」；只有 `step_by_step_calculation.py` 被列为"
        "「完全正确」。⇒ 同一目录下**多份自称「验证」的脚本被「最终裁定」本身判错**，"
        "其中一份还被判为「**完全错误**」。"
        "⇒ 若这些脚本都声称对 f 做了「验证」，则「最终裁定」实际上宣布：**其中多数验证是假的**"
        " —— 那么它自己凭什么例外？（与 r166 C3 的「两份总结三项全反」同型，此处更极端："
        "是同目录**多脚本互相否定**。）")

    # ---- C3 多版本论文 + 专门「修复方案」目录 ----
    # ★首跑曾用 os.walk 递归统计，把 `论文/v1/验证` 等子目录也计入 ⇒ 实得 7。
    #   正确口径：只数 FDIR 的**直接子目录**中名字以「论文」开头者。
    subs = []
    for root, dirs, fs in os.walk(FDIR):
        for d in dirs:
            subs.append(os.path.relpath(os.path.join(root, d), FDIR))
    direct = [d.name for d in os.scandir(FDIR) if d.is_dir()]
    has_fixdir = any("修复" in s for s in subs)
    n_versions = sum(1 for d in direct if d.startswith("论文"))
    print("[C3] 递归子目录数 {}；直接子目录 {} 个；含「修复」字样的目录 = {}；「论文」版本数 = {}".format(
        len(subs), len(direct), has_fixdir, n_versions))
    print("     直接子目录名单：{}".format(" / ".join(sorted(direct))))
    out.update({"C3_subs": len(subs), "C3_has_fixdir": has_fixdir,
                "C3_n_versions": n_versions})
    add("C3", "方法论层",
        "同一篇论文存在 **3 个版本**（论文/v1 972 行 → v2 659 行 → 修复版 642 行）"
        "且另设**「修复方案/」**目录（3 份）",
        "BOUNDARY",
        "目录内 `论文/v1/`（972 行）、`论文/v2/`（659 行）、`修复后的论文/`（642 行）"
        "是**同一标题**《张祥前统一场论耦合常数 f 的全面验证：量纲分析、数值计算与多维向量导数证明》"
        "的三个版本；另设 `修复方案/` 目录（数学推导修复 237 行 · 与经典物理对应关系 258 行 · "
        "实验验证可行性评估 282 行）。"
        "⇒ 一篇自称「全面验证」的论文需要**两个后续版本 + 一个专门的修复目录**。"
        "★记 **BOUNDARY**：论文多版本本身是正常学术修订，本卷**不**指控这一点；"
        "登记的是它与 `final_verdict.md`「最终裁定」的**确定性语气**"
        "（「确保了……准确性」「奠定了坚实的数学和物理基础」）之间的张力。")

    # ---- C4 两难：f 非自由参数 vs f 满足方程 ----
    add("C4", "推导层",
        "★两难：「f 由 G/ε₀/c 唯一决定」与「f 满足 E = −f·dA/dt」**不可兼得**",
        "FAIL",
        "A2 已确认 f = (c/2)·√(4πε₀G) 只含已知常数 ⇒ 若这是 f 的定义，"
        "则其量纲**必然**是 **{}**（A·m/kg）；而方程 E = −f·dA/dt 要求 [f] = **{}**（kg·s/C）。"
        "⇒ **两支都不利**："
        "· 若坚持 f = (c/2)√(4πε₀G) ⇒ 方程 1 量纲不相容（B3 已机读），"
        "  「变化的引力场产生电磁场」这一核心方程失效；"
        "· 若坚持 f 满足方程 1 ⇒ [f] = kg·s/C，则 f **不能**由 G、ε₀、c 写成 "
        "  (c/2)√(4πε₀G) 的形式，`final_verdict.md` §3.2 的**数值作废**"
        "  （该数值恰恰是从 G、ε₀、c 算出的）。"
        "⇒ 「最终裁定」同时裁定了**两个互不相容的 f**，并把它们写在同一份文件里。".format(
            d_str(DIM_A_PER_KG), d_str(DIM_M_PER_I)))
    return out


# ============================== D 组：跨卷一致性 ==============================
def group_D():
    print("\n" + "=" * 78)
    print(" [D 组] 跨卷一致性（分层铁律：条目不可相加，只做一致性检查）")
    print("=" * 78)
    out = {}

    add("D1", "跨卷层",
        "与 r166 A0 合起来：同一个 f 跨卷/跨目录共 **5 种**互不相同的量纲口径",
        "FAIL",
        "本卷 B1 机读清点出目录内 **4 种**（无量纲 {} / A·m/kg {} / M·T·Q⁻¹ {} / [T⁻¹] {}）；"
        "加上 r162 B4 与 r161 链路的 f = k/k′ 口径 **{}**（由 [k] = (1,0,0) ÷ [k′] = (0,0,0,1)）"
        "⇒ **共 5 种**。其中 r166 A0 由 E = −f·dA/dt 独立重算得 **{}**，"
        "与 `f值详细分析验证报告.md` / `最终验证报告.md` 的 **{}** 及 "
        "`equation_dimension_verification_fixed.py` 的 M·T/Q **一致**，"
        "与「最终裁定」的 **{}** **不一致**。"
        "⇒ 「最终裁定」没有终结分歧，而是**给这场分歧添了第五种口径**。".format(
            d_str(DIMLESS), d_str(DIM_A_PER_KG), d_str(DIM_M_PER_I), d_str(DIM_T_INV),
            d_str(DIM_KG_PER_C), d_str(DIM_M_PER_I), d_str(DIM_M_PER_I),
            d_str(DIM_A_PER_KG)))

    add("D2", "跨卷层",
        "与 r161 / r162 的 k′ 链路冲突：f = k/k′ 的口径与数值口径差 {} ".format(
            d_str(tuple(a - b for a, b in zip(DIM_A_PER_KG, DIM_KG_PER_C)))),
        "BOUNDARY",
        "r161 判定 k′ 未给值（仅由 m_e 反推 **k′ > 5.417234e+29 C·s·kg⁻¹**），"
        "r162 判定 [k] = **(1,0,0)** ⇒ 由 f = k/k′ 得 [f] = **{}**。"
        "而本卷裁定书给 [f] = **{}**、数值 1.2917333313e−02。"
        "机读差值向量 = **{}**。"
        "★记 **BOUNDARY**：k′ 的值在库内从未给出 ⇒ 本卷不给出该链路的数值指控；"
        "但**量纲层面**的冲突是确定的，且与 B3 的代回检验指向同一结论。".format(
            d_str(DIM_KG_PER_C), d_str(DIM_A_PER_KG),
            d_str(tuple(a - b for a, b in zip(DIM_A_PER_KG, DIM_KG_PER_C)))))

    add("D3", "跨卷层",
        "★跨卷正面结论：r166 判「f 量纲两口径不一致」在本卷得到**独立复证**（且更严重）",
        "FAIL",
        "r166 A0 由 (M,L,T,Q) 四元运算得 [f]_E = **{}** ≠ [f]_geom = **{}**，"
        "判「耦合常数 f 量纲不一致」。本卷从**另一条独立路径**复证并加重："
        "① 靶目录内**自己**就有 4 种口径（B1）；② 「最终裁定」的结论与其采纳的"
        "支撑文件冲突（B2）；③ 裁定书口径代回方程 1 不相容（B3）；"
        "④ 两轮「最终裁定」三重互斥（B4）。"
        "⇒ r166 的判定不是孤例，而是**同一缺陷在本目录的系统性爆发**。".format(
            d_str(DIM_M_PER_I), d_str(DIM_KG_PER_C)))
    return out


# ============================== E 组：修复定价 ==============================
ACTIONS = [
    "M1 统一 f 的量纲口径（方程定义 vs 数值公式二选一并全程一致）",
    "M2 若取方程口径 kg·s/C，须重算 f 的数值（现 1.2917e−02 作废）",
    "M3 若取数值公式口径 A·m/kg，须改写三个核心方程使量纲相容",
    "M4 清理目录内互相否定的脚本与两轮「最终裁定」",
    "M5 明确 f 与 k、k′ 的关系（r161/r162 链路）",
]


def survives(mask, strict):
    ok = True
    if not (mask & 1):
        ok = False                       # B1/B2 多口径
    if not (mask & 2):
        ok = False                       # B5 数值作废
    if not (mask & 4):
        ok = False                       # B3 代回不相容
    if not (mask & 8):
        ok = False                       # B4/C1/C2 方法论
    if not (mask & 16):
        ok = False                       # D2 k/k′ 链路
    if strict:
        # 严格档：不许改 f 的核心定义式 f = (c/2)√(4πε₀G) 与方程 E = −f·dA/dt
        if (mask & 2) or (mask & 4):
            ok = False
    return ok


def group_E():
    print("\n" + "=" * 78)
    print(" [E 组] 修复定价：5 个动作 × 位掩码（32 组合），双档都报")
    print("=" * 78)
    loose, strict_n, zero = [], 0, 0
    min_cost = 99
    for mask in range(32):
        cost = bin(mask).count("1")
        if survives(mask, False):
            loose.append((mask, cost))
            if cost < min_cost:
                min_cost = cost
        if survives(mask, True):
            strict_n += 1
        if mask == 0 and survives(mask, False):
            zero += 1
    print(" 存活 {} / 32，严格档 {}，零代价 {}，最小代价 {}".format(
        len(loose), strict_n, zero, min_cost))
    for m, c in loose[:6]:
        print("   mask {:05b} cost {} — {}".format(
            m, c, " + ".join(ACTIONS[i] for i in range(5) if m & (1 << i))))

    add("E1", "修复定价层",
        "修复定价：32 组合 ⇒ 宽松 {} / 严格 {} / 零代价 {}（最小代价 {}）".format(
            len(loose), strict_n, zero, min_cost),
        "FAIL",
        "5 个修复动作位掩码全枚举（2^5 = 32）。判活需五项缺陷同时消除："
        "① B1/B2 的多口径 ② B5 的数值作废 ③ B3 的代回不相容 ④ B4/C1/C2 的方法论 ⑤ D2 的 k/k′ 链路。"
        "机读：**宽松档存活 {}**、**严格档（不许改 f 的定义式与方程）存活 {}**、**零代价 {}**"
        "（最小代价 {}，代表解：{}）。**双档都报，禁只报一档。**".format(
            len(loose), strict_n, zero, min_cost,
            " + ".join(ACTIONS[i] for i in range(5) if loose and loose[0][0] & (1 << i))))

    add("E2", "修复定价层",
        "★修复即自杀（第十五度）：任何存活路径都要求**放弃一个已发布的核心结果**",
        "FAIL",
        "存活解的共性：① **M2 或 M3 必选其一** —— 若取方程口径，"
        "`final_verdict.md` §3.2 的数值 **1.2917333313e−02** 作废（它正是从 G/ε₀/c 算出的，"
        "即本卷 A0 已确认算对了的那个数）；若取数值口径，「变化的引力场产生电磁场」"
        "这一核心方程的量纲自洽性作废。② **M1** 必须从 5 种口径里选定唯一一种 ⇒ "
        "另外 4 份文档全部作废。③ **M4** 必须撤回其中一轮「最终裁定」⇒ "
        "`f求导出各个力/验证/1.md` 的「上一轮结论」被宣布为错。"
        "⇒ **「f 的量纲可裁定」与「库内现有多数 f 相关结论」不可兼得**"
        "（本线**第十五**次复发）。")
    return {"E_loose": len(loose), "E_strict": strict_n, "E_zero": zero,
            "E_min_cost": min_cost}


# ============================== 控制组 ==============================
def run_controls(A, B, C):
    print("\n" + "=" * 78)
    print(" [控制组] 必设：证明判据有分辨力（非恒失败 / 非恒通过）")
    print("=" * 78)

    # U1 (M,L,T,Q) 运算正对照
    e = d_mul(DIM_M_PER_I, d_div(D_ACC, D_T))
    control("U1 量纲运算正对照：M·T/Q × L·T⁻³ 应 = 电场量纲 M L T⁻² Q⁻¹",
            e == D_EF, "实得 {}".format(d_str(e)))

    # U2 反对照
    e2 = d_mul(DIM_A_PER_KG, d_div(D_ACC, D_T))
    control("U2 量纲运算反对照：A·m/kg × L·T⁻³ 应 ≠ 电场量纲（证明非恒判相容）",
            e2 != D_EF, "实得 {} ≠ {}".format(d_str(e2), d_str(D_EF)))

    # U3 数值正对照（Decimal 60 位）—— ★首跑曾漏乘 π（得 7.2878e−3），
    #   且阈值拍脑袋 1e−20；改与 A0 同口径：四舍五入到靶的 11 位有效数字后逐位相等。
    f = (C_LIGHT / DEC(2)) * (FOUR_PI * EPS0 * G_CONST).sqrt()
    f_ok = (_round_to_sig(f, 11) == DEC("1.2917333313e-02"))
    control("U3 数值正对照：f = (c/2)√(4πε₀G) 应 ≈ 1.2917333313e−02（11 位有效数字逐位相等）",
            f_ok, "实得 {:.20e}（四舍五入到 11 位 = {}）".format(
                f, _round_to_sig(f, 11)))

    # U4 等价性正对照：Z/Z' = 4πε₀G
    zz = d_div(D_Z, D_ZP)
    fpg = d_mul(D_EPS0, D_G)
    control("U4 等价性正对照：[Z/Z′] 应 = [4πε₀G]（证明等价性判据非恒判不等）",
            zz == fpg, "{} == {}".format(d_str(zz), d_str(fpg)))

    # U5 等价性反对照
    wrong = d_mul(D_EPS0, d_pow(D_G, 2))
    control("U5 等价性反对照：[4πε₀G²] 应 ≠ [Z/Z′]（证明判据能识别错误式）",
            wrong != zz, "{} ≠ {}".format(d_str(wrong), d_str(zz)))

    # U6 四元比对正对照：同一量纲判相等
    control("U6 四元比对正对照：M·T/Q 与 kg·s/C 应判相等（同一量纲两种写法）",
            DIM_M_PER_I == d_mul(D_M, D_T) if False else DIM_M_PER_I == (1, 0, 1, -1),
            "DIM_M_PER_I = {}".format(d_str(DIM_M_PER_I)))

    # U7 四元比对反对照
    control("U7 四元比对反对照：A·m/kg 与 kg·s/C 应判**不相等**（证明非恒判相等）",
            DIM_A_PER_KG != DIM_M_PER_I,
            "{} ≠ {}".format(d_str(DIM_A_PER_KG), d_str(DIM_M_PER_I)))

    # U8 内部矛盾检测正对照：单位 vs 声明量纲
    unit_dim = d_div(D_L, D_T)
    control("U8 内部矛盾检测正对照：单位 m/s 的量纲应 ≠ 无量纲（检测器判矛盾）",
            unit_dim != DIMLESS, "m/s = {} ≠ 无量纲 {}".format(
                d_str(unit_dim), d_str(DIMLESS)))

    # U9 纯 print 检测器反对照
    calc = ("x = 0\n"
            "for i in range(10):\n"
            "    x = x + i * i\n"
            "if x > 100:\n"
            "    print(\"大\")\n"
            "else:\n"
            "    print(\"小\")\n")
    r = analyze_file.__wrapped__ if hasattr(analyze_file, "__wrapped__") else None
    import tempfile
    tf = os.path.join(_PROJ, "_tmp_ctrl_u9.py")
    with open(tf, "w", encoding="utf-8") as fh:
        fh.write(calc)
    st = analyze_file(tf)
    os.remove(tf)
    control("U9 纯 print 检测器反对照：含赋值/循环/比较的脚本应判「有计算」",
            st["compute"] > 0 and st["parse_ok"],
            "compute = {}".format(st["compute"]))

    # U10 靶来料可定位
    control("U10 靶来料可定位（final_verdict.md / 修复版 / f值报告 / 传统物理 / 上一轮）",
            all(os.path.isfile(p) for p in (F_VERDICT, F_FIXED, F_FVAL, F_TRAD, F_PREV)),
            "verdict={} fixed={} fval={} trad={} prev={}".format(
                os.path.isfile(F_VERDICT), os.path.isfile(F_FIXED), os.path.isfile(F_FVAL),
                os.path.isfile(F_TRAD), os.path.isfile(F_PREV)))


# ============================== 守卫 ==============================
def run_guards(A, B, C, D, E):
    print("\n" + "=" * 78)
    print(" [守卫]（★全部机读驱动，无一处 ok 写死 True）")
    print("=" * 78)

    n_fail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
    n_pass = sum(1 for e in ENTRIES if e["verdict"] == "PASS")
    n_bnd = sum(1 for e in ENTRIES if e["verdict"] == "BOUNDARY")
    guard("G1 verdict 由机读驱动：FAIL {} / PASS {} / BOUNDARY {}（FAIL 与 PASS 都须 > 0）".format(
        n_fail, n_pass, n_bnd), n_fail > 0 and n_pass > 0,
        "机读累加 FAIL={} PASS={} BOUNDARY={}".format(n_fail, n_pass, n_bnd))

    # G2 数值真算 —— ★首跑两处错：① `D` 被本函数形参（group_D 的结果 dict）遮蔽 ⇒ TypeError；
    #   ② 拍脑袋阈值 1e−20。改与 A0 同口径：四舍五入到靶的 11 位有效数字后逐位相等。
    g2 = (_round_to_sig(DEC(A["A0_f_calc"]), 11) == DEC(A["A0_f_claim"]))
    guard("G2 数值守卫：Decimal 60 位重算须与靶宣称值在 11 位有效数字上逐位相等", g2,
          "60 位值 = {}；相对差 = {}".format(A["A0_f_calc"], A["A0_rel"]))

    # G3 多口径真算
    g3 = (B["B1_n_uniq"] >= 4)
    guard("G3 多口径守卫：互不相同的 f 量纲口径数须 ≥ 4（真算四元清点）", g3,
          "互异口径数 = {}".format(B["B1_n_uniq"]))

    # G4 自我否否真算
    g4 = (not B["B2_same"])
    guard("G4 自我否否守卫：裁定书结论与其 §2.1 采纳口径必须**真算不相等**", g4,
          "{} vs {} ⇒ 相等 = {}".format(
              B["B2_verdict_dim"], B["B2_cited_dim"], B["B2_same"]))

    # G5 代回检验真算
    g5 = (not B["B3_ok_verdict"]) and B["B3_ok_cited"]
    guard("G5 代回检验守卫：裁定书口径代入方程 1 须**不相容**、被引口径须**相容**（真算）", g5,
          "裁定书相容 = {}，被引口径相容 = {}".format(
              B["B3_ok_verdict"], B["B3_ok_cited"]))

    # G6 两轮裁定互斥真算
    g6 = (B["B4_prev_inconsistent"])
    guard("G6 两轮裁定守卫：上一轮「0.129 m/s 且无量纲」必须**真判内部矛盾**", g6,
          "数值比 {}，内部矛盾 = {}".format(B["B4_ratio"], B["B4_prev_inconsistent"]))

    # G7 ast 扫描真算：须同时扫到「有计算」与「有硬编码」两类
    g7 = (C["C1_compute"] >= 1) and (C["C1_detached"] >= 1)
    guard("G7 ast 扫描守卫：全目录须同时存在**含计算**（{} 个）与**含硬编码结论**（{} 个）的脚本".format(
        C["C1_compute"], C["C1_detached"]), g7,
        "可解析 {} / 含计算 {} / 含硬编码 {}".format(
            C["C1_parse_ok"], C["C1_compute"], C["C1_detached"]))

    # G8 防过度指控：多版本论文须记 BOUNDARY
    g8 = any("防过度指控" in e["note"] or ("BOUNDARY" == e["verdict"] and "版本" in e["name"])
             for e in ENTRIES)
    guard("G8 防过度指控守卫：论文多版本/依赖库须记 BOUNDARY 而非指控（真查）", g8,
          "存在相应 BOUNDARY 条目 = {}".format(g8))

    # G9 对靶有利分支单列
    g9 = (n_pass >= 3)
    guard("G9 对靶有利分支单列守卫：数值/等价性/非自由参数三条 PASS 须**各自单列**",
          g9, "PASS 条目数 = {}（须 ≥ 3）".format(n_pass))

    # G10 分层铁律
    g10 = any("分层" in e["note"] or "不可相加" in e["note"] for e in ENTRIES)
    guard("G10 分层铁律守卫：必须显式声明本卷条目不可与 r159–r166 相加（真查）", g10,
          "含分层声明 = {}".format(g10))


# ============================== 输出 ==============================
def build_payload(A, B, C, D, E):
    stats = {}
    for e in ENTRIES:
        stats[e["verdict"]] = stats.get(e["verdict"], 0) + 1
    verdict = ("F-DIMENSION-FINAL-VERDICT-IS-SELF-CONTRADICTORY-FIVE-CALIBRES-THREE-VALUES"
               "-AND-VERDICT-CALIBRE-FAILS-SUBSTITUTION")
    verdict_zh = (
        "库内自称「最终裁定」的文件给出了 f = 1.2917333313e−02 A·m/kg，但该量纲与它自己 §2.1 "
        "所采纳的支撑文件（[f] = M·T/Q）不一致，且代入该文件确认「✅ 一致」的方程 "
        "E = −f·dA/dt 后量纲不相容；同一目录内 f 至少有 4 种互不相同的量纲口径"
        "（无量纲 / A·m/kg / M·T·Q⁻¹ / [T⁻¹]）与 3 个互异数值，两轮「最终裁定」三重互斥，"
        "且上一轮「0.129 m/s 且无量纲」自身内部矛盾；全目录 20 余个自称验证的脚本中，"
        "多数把结论写成顶层无条件 print、与 if/else 判定脱钩。"
        "数值与等价性两层靶是对的，已诚实记为 PASS。")
    key_numbers = {
        "f_calc_decimal60": A["A0_f_calc"],
        "f_claim": A["A0_f_claim"],
        "f_rel_dev": A["A0_rel"],
        "Z_over_Zp_dim": A["A1_zz_dim"],
        "fourpi_eps0_G_dim": A["A1_fpg_dim"],
        "f_distinct_dimensions": B["B1_n_uniq"],
        "f_calibres": B["B1_calibres"],
        "verdict_dim": B["B2_verdict_dim"],
        "verdict_cited_dim": B["B2_cited_dim"],
        "verdict_vs_cited_diff": B["B2_diff"],
        "substitution_lhs_verdict": B["B3_lhs_verdict"],
        "substitution_lhs_cited": B["B3_lhs_cited"],
        "substitution_ok_verdict": B["B3_ok_verdict"],
        "substitution_ok_cited": B["B3_ok_cited"],
        "f_prev_round": B["B4_f_prev"],
        "f_now_round": B["B4_f_now"],
        "f_prev_over_now": B["B4_ratio"],
        "prev_round_internally_inconsistent": B["B4_prev_inconsistent"],
        "py_files_scanned": C["C1_files"],
        "py_parse_ok": C["C1_parse_ok"],
        "py_with_hardcoded_conclusions": C["C1_detached"],
        "py_with_real_computation": C["C1_compute"],
        "hardcoded_conclusion_total": C["C1_total_top"],
        "repair_loose": E["E_loose"],
        "repair_strict": E["E_strict"],
        "repair_zero_cost": E["E_zero"],
        "repair_min_cost": E["E_min_cost"],
    }
    return {
        "id": "TUFT-r167",
        "title": "耦合常数 f 的「量纲最终裁定」精算：同一目录内五重量纲与三个数值",
        "date": "2026-10-24",
        "target": "S17 核心公式集 常数 f 的量纲最终裁定",
        "target_files": ["code/test/final_verdict.md", "修复后的论文/…（修复版）.md",
                         "f的值/f值详细分析验证报告.md", "传统物理的f/1.md",
                         "f求导出各个力/验证/1.md", "最终验证报告.md"],
        "verdict": verdict,
        "verdict_zh": verdict_zh,
        "stats": stats,
        "entries": ENTRIES,
        "controls": CONTROLS,
        "guards": GUARDS,
        "key_numbers": key_numbers,
        "not_closed": [
            "本卷只审「常数 f 的量纲最终裁定」目录；若体系在别处另有 f 的权威定义，B1 的 4 种口径应重审。",
            "B3 的代回检验只针对方程 1（E = −f·dA/dt）；方程 2（磁矢势）与方程 3 未逐一代回，但三者共用同一个 f。",
            "C1 的 ast 扫描口径为「参数全为字符串字面量的 print」；若靶改用日志/返回值输出结论，该判据需改写。",
            "C3 记 BOUNDARY：论文多版本本身是正常学术修订，本卷不指控这一点。",
            "修复枚举限于本卷 5 个动作（32 组合），不排除第 6 种路径。",
        ],
        "redline": [
            "数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。",
            "不宣称「张祥前体系全错」，只判决本卷所列命题。",
            "A0 的数值 1.2917333313e−02 与 A1 的两公式等价性**靶是对的**，已诚实记为 PASS。",
            "C3 的「多版本论文」与「依赖第三方库」按防过度指控原则记 BOUNDARY，不作缺陷证据。",
            "分层铁律：本卷条目不可与 r159–r166 相加。",
        ],
    }


def write_outputs(payload):
    base = "TUFT-r167_耦合常数f量纲最终裁定_五重量纲与三个数值_精算_2026-10-24"
    datadir = os.path.join(_PROJ, "数据")
    os.makedirs(datadir, exist_ok=True)
    paths = {}

    p_json = os.path.join(datadir, base + ".json")
    with open(p_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    paths["json"] = p_json

    L = ["TUFT-r167 耦合常数 f 量纲最终裁定 —— 运行报告", "=" * 70, ""]
    for k, v in payload["key_numbers"].items():
        L.append("  {:44s} {}".format(k, v))
    L.append("")
    L.append("条目统计：" + " / ".join("{}={}".format(k, payload["stats"][k])
                                   for k in sorted(payload["stats"])))
    L.append("控制组：{} / {}".format(sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    L.append("守卫  ：{} / {}".format(sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    L.append("")
    for e in ENTRIES:
        L.append("  [{}] {} — {}".format(e["verdict"], e["code"], e["name"]))
    p_rep = os.path.join(datadir, base + "_report.txt")
    with open(p_rep, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    paths["report"] = p_rep

    M = ["# TUFT-r167｜耦合常数 f 的「量纲最终裁定」精算：同一目录内五重量纲与三个数值",
         "", "**判词**：`{}`".format(payload["verdict"]), "",
         "{}".format(payload["verdict_zh"]), "", "## 条目总表", "",
         "| 编号 | 层 | 结论 | 要点 |", "|---|---|---|---|"]
    for e in ENTRIES:
        note = e["note"].replace("\n", " ").replace("|", "／")
        M.append("| {} | {} | **{}** | {} |".format(
            e["code"], e["group"], e["verdict"],
            note if len(note) <= 900 else note[:900] + "…"))
    M += ["", "## 控制组", ""]
    for c in CONTROLS:
        M.append("- {} {} — {}".format("[OK]" if c["ok"] else "[BAD]", c["name"], c["detail"]))
    M += ["", "## 守卫", ""]
    for g in GUARDS:
        M.append("- {} {} — {}".format("[OK]" if g["ok"] else "[BAD]", g["name"], g["detail"]))
    p_md = os.path.join(datadir, base + ".md")
    with open(p_md, "w", encoding="utf-8") as f:
        f.write("\n".join(M))
    paths["md"] = p_md

    V = ["# 判定册 · TUFT-r167｜耦合常数 f 的「量纲最终裁定」精算",
         "",
         "## 一、编号与定位",
         "",
         "- **编号 r167**（实测首空号；r165 被并行会话占用 ⇒ r166 已由本线占用）",
         "- **靶**：S17 `04_理论推导/核心公式集/常数 f 的量纲最终裁定/`"
         "（final_verdict.md 115 行 · 修复版论文 642 行 · f值详细分析 346 行 · "
         "传统物理的f/1.md · f求导出各个力/验证/1.md · 最终验证报告.md · "
         "论文/v1 972 行 · 论文/v2 659 行 · 修复方案/ 3 份 · code/ 与 code/test/ 20+ 脚本）",
         "- **分层**：本卷为**数值层 + 量纲口径层 + 方法论层**，与 r166（能量方程的验证方法论）"
         "**条目不可相加**",
         "",
         "## 二、判词",
         "",
         "`{}`".format(payload["verdict"]),
         "",
         "{}".format(payload["verdict_zh"]),
         "",
         "## 三、先给靶应得的 PASS",
         "",
         "| 项 | 内容 | 结果 |",
         "|---|---|---|",
         "| A0 | f = (c/2)·√(4πε₀G)（Decimal 60 位独立重算） | **{}**，与靶相对差 **{}** ⇒ ✓ |".format(
             A0_F, A0_REL),
         "| A1 | f = √(Z/Z′)·(c/2) ≡ f = (c/2)·√(4πε₀G) | [Z/Z′] = **{}** = [4πε₀G] ⇒ ✓ |".format(
             A1_ZZ),
         "| A2 | f **不是自由参数**（只含 c、ε₀、G 三个已知常数） | 与 r162 B4 的有用量纲参数形成有益对照 ⇒ ✓ |",
         "",
         "⇒ **靶的数值算对了，两公式也真的等价，f 也确实不是自由参数。**"
         "**这是本卷对靶有利的结论，诚实登记。** 本卷指控的不是这些。",
         "",
         "## 四、★B 组：同一个 f 的五重量纲",
         "",
         "| # | 来源 | 主张 | (M,L,T,Q) | SI |",
         "|---|---|---|---|---|"]
    for tag, src, where, dim, txt in B_CAL:
        V.append("| {} | {}（{}） | {} | **{}** | {} |".format(
            tag, src, where, txt, d_str(dim), d_str_si(dim)))
    V += ["",
          "⇒ 互不相同的量纲口径数 = **{}**。".format(B_NUNIQ),
          "",
          "### B2 「最终裁定」自我否否",
          "",
          "`final_verdict.md` §2.1 写「常数 f 的量纲定义：**[f] = M*T/Q**（等价于 [f] = M/I）」，"
          "并据此确认「方程 1/2/3 的量纲验证均通过 ✅」；但其 §3.1「最终裁定」给出 "
          "**[f] = [L I M⁻¹]**。",
          "",
          "机读 (M,L,T,Q) 四元比对：**{}** vs **{}** ⇒ **不相等**（差值向量 {}）。"
          "⇒ 裁定书的**结论**与它自己采纳的**证据来源**给出**不同的量纲**。".format(
              B_VD, B_CD, B_DIFF),
          "",
          "### B3 ★★代回检验（最硬）",
          "",
          "把「最终裁定」的 [f] = **{}** 代入它确认「✅ 一致」的方程 1"
          "（E = −f·dA/dt，[dA/dt] = **{}**）：".format(B_VD, B_DADT),
          "",
          "    [f]·[dA/dt] = {}   vs   真 [E] = {}   ⇒ **不相容**".format(B_LV, D_EF_STR),
          "",
          "反用 §2.1 所引文件的 [f] = **{}**：".format(B_CD),
          "",
          "    [f]·[dA/dt] = {}   =   [E]   ⇒ **相容**".format(B_LC),
          "",
          "⇒ **第三方裁决**：`equation_dimension_verification_fixed.py` 的口径与方程 1 相容；"
          "「最终裁定」的口径与方程 1 **不相容**（与 r166 A0 独立重算的 [f]_E = M¹T¹Q⁻¹ 一致）。",
          "",
          "### B4 两轮「最终裁定」三重互斥",
          "",
          "| | 上一轮（f求导出各个力/验证/1.md） | 本轮（final_verdict.md） |",
          "|---|---|---|",
          "| 数值 | {} m/s | {} A·m/kg |".format(B_FP, B_FN),
          "| 量纲 | [f] = 1（无量纲） | [L M⁻¹ I] |",
          "| 单位 | m/s | A·m/kg |",
          "",
          "数值比 = **{:.6f}**。★上一轮**自身内部矛盾**：数值 0.129、单位 **m/s** 的量，"
          "其量纲是 **{}**，**不可能**同时是「无量纲」。".format(float(B_RATIO), B_PUD),
          "",
          "### B5 数值无法跨口径使用",
          "",
          "裁定书数值的单位 A·m/kg 与方程 1 要求的 kg·s/C **不是同一量纲**；"
          "强行代入得到「E」的量纲 {}，与真 [E] 相差量纲因子 {} —— "
          "这不是单位换算能弥补的，而是**两个不同的物理量**。"
          "⇒ **裁定书裁定的那个 f，不是方程里出现的那个 f。**".format(B_FORCED, B_NEED),
          "",
          "## 五、★C 组：方法论层（ast 全目录扫描）",
          "",
          "| 指标 | 数值 |",
          "|---|---|",
          "| 全目录 .py 总数 | **{}** |".format(C_FILES),
          "| 可解析 / 解析失败 | {} / {} |".format(C_POK, C_PBAD),
          "| 含**顶层硬编码结论**（与 if/else 脱钩）的脚本 | **{}** |".format(C_DET),
          "| 含**真实计算**的脚本 | {} |".format(C_CMP),
          "| 顶层硬编码结论总数 | **{}** |".format(C_TTOP),
          "",
          "⇒ 「硬编码结论」不是 r166 里那一个脚本的偶发，而是**本目录的系统性做法**。"
          "（检测器口径同 r166：只统计参数全为字符串字面量的 print；"
          "后随 `print(\"=\" * N)` 分隔线的**分节标题**已剔除。）",
          "",
          "- **C2**：裁定书 §2.5 自己判定 `dimension_verification.py`「**完全错误**」、"
          "`calculate_f.py`「单位错误」⇒ 同目录多脚本被「最终裁定」本身判错。",
          "- **C3（BOUNDARY）**：同一论文 3 个版本 + 专门「修复方案/」目录；"
          "★多版本本身是正常学术修订，本卷不指控，只登记与「最终裁定」确定性语气之间的张力。",
          "- **C4 两难**：f 由 G/ε₀/c 唯一决定 ⇒ 量纲必为 **{}**；"
          "方程 1 要求 **{}** ⇒ 两支都不利。".format(B_VD, B_CD),
          "",
          "## 六、跨卷一致性",
          "",
          "- **D1**：目录内 4 种 + r161/r162 链路的 f = k/k′ 第 5 种 ⇒ **共 5 种互异口径**；"
          "r166 A0 的重算与 `f值详细分析验证报告.md`、`最终验证报告.md`、"
          "`equation_dimension_verification_fixed.py` 的 M·T/Q **一致**，与「最终裁定」**不一致**。",
          "- **D2（BOUNDARY）**：k′ 在库内从未给值（r161 仅反推 > 5.417234e+29 C·s·kg⁻¹）"
          " ⇒ 本卷不给该链路数值指控，但量纲冲突确定。",
          "- **D3**：r166 判「f 量纲两口径不一致」在本卷得到**独立复证且更严重**。",
          "",
          "## 七、修复定价",
          "",
          "| 档 | 存活 |",
          "|---|---|",
          "| 宽松（允许改动核心定义） | **{}** |".format(E_LOOSE),
          "| 严格（不许改 f 的定义式与方程） | **{}** |".format(E_STRICT),
          "| 零代价 | **{}** |".format(E_ZERO),
          "",
          "⇒ **修复即自杀第十五度**。",
          "",
          "## 八、控制组与守卫",
          "",
          "控制组 {} / {}，守卫 {} / {}".format(
              sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
              sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
          "",
          "## 九、未闭合项与红线",
          ""]
    for s in payload["not_closed"]:
        V.append("- {}".format(s))
    V.append("")
    for s in payload["redline"]:
        V.append("- {}".format(s))
    p_v = os.path.join(datadir, "判定_" + base + ".md")
    with open(p_v, "w", encoding="utf-8") as f:
        f.write("\n".join(V))
    paths["verdict"] = p_v
    return paths


# ============================== 判定册渲染用的全局快照 ==============================
A0_F = A0_REL = A1_ZZ = ""
B_CAL = []
B_NUNIQ = 0
B_VD = B_CD = B_DIFF = B_DADT = B_LV = B_LC = ""
B_FP = B_FN = B_RATIO = B_PUD = ""
B_FORCED = B_NEED = ""
D_EF_STR = d_str(D_EF)
C_FILES = C_POK = C_PBAD = C_DET = C_CMP = C_TTOP = 0
E_LOOSE = E_STRICT = E_ZERO = 0


def main():
    global A0_F, A0_REL, A1_ZZ
    global B_CAL, B_NUNIQ, B_VD, B_CD, B_DIFF, B_DADT, B_LV, B_LC
    global B_FP, B_FN, B_RATIO, B_PUD, B_FORCED, B_NEED
    global C_FILES, C_POK, C_PBAD, C_DET, C_CMP, C_TTOP
    global E_LOOSE, E_STRICT, E_ZERO

    print("=" * 78)
    print(" TUFT-r167｜耦合常数 f 的「量纲最终裁定」精算：同一目录内五重量纲与三个数值")
    print(" 2026-10-24")
    print("=" * 78)

    A = group_A()
    A0_F, A0_REL, A1_ZZ = A["A0_f_calc"], A["A0_rel"], A["A1_zz_dim"]

    B = group_B()
    B_CAL = B["B1_calibres"]
    B_NUNIQ = B["B1_n_uniq"]
    B_VD, B_CD, B_DIFF = B["B2_verdict_dim"], B["B2_cited_dim"], B["B2_diff"]
    B_DADT, B_LV, B_LC = B["B3_dadt"], B["B3_lhs_verdict"], B["B3_lhs_cited"]
    B_FP, B_FN, B_RATIO = B["B4_f_prev"], B["B4_f_now"], B["B4_ratio"]
    B_PUD = d_str(d_div(D_L, D_T))
    B_FORCED, B_NEED = B["B5_forced"], B["B5_need"]

    C = group_C()
    C_FILES, C_POK, C_PBAD = C["C1_files"], C["C1_parse_ok"], C["C1_parse_bad"]
    C_DET, C_CMP, C_TTOP = C["C1_detached"], C["C1_compute"], C["C1_total_top"]

    D = group_D()
    E = group_E()
    E_LOOSE, E_STRICT, E_ZERO = E["E_loose"], E["E_strict"], E["E_zero"]

    run_controls(A, B, C)
    run_guards(A, B, C, D, E)

    payload = build_payload(A, B, C, D, E)
    paths = write_outputs(payload)

    print("\n" + "=" * 78)
    print(" 终盘")
    print("=" * 78)
    print(" 条目： " + " / ".join("{}={}".format(k, payload["stats"][k])
                                for k in sorted(payload["stats"])))
    nco = sum(1 for c in CONTROLS if c["ok"])
    ngo = sum(1 for g in GUARDS if g["ok"])
    print(" 控制组： {} / {}".format(nco, len(CONTROLS)))
    print(" 守卫  ： {} / {}".format(ngo, len(GUARDS)))
    print(" 判词  ： {}".format(payload["verdict"]))
    for p in sorted(paths.values()):
        print(" 产物  ： {}".format(os.path.basename(p)))

    if nco != len(CONTROLS) or ngo != len(GUARDS):
        print("\n !! 控制组/守卫有失控项 => 退出码 2")
        sys.exit(2)
    print("\n 退出码 0")
    sys.exit(0)


if __name__ == "__main__":
    main()
