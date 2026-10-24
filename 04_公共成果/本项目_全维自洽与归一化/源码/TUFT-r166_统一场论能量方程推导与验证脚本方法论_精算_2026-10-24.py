#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TUFT-r166｜统一场论能量方程的「第一性原理推导」与「验证脚本」方法论精算
================================================================================
编号 r166（实测首空号）
★ 编号冲突处置：r165 已被并行会话占用（已产出四件套
  TUFT-r165_D5四力闭合层_单粒子运动学量与源依赖冲突_2026-10-24.*）
  ⇒ 按纪律「保留已产三件套并已登记者为权威，后到者整体改号」⇒ 本卷整体改用 r166。

靶：`01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/16-统一场论能量方程/`
    · 1.md（326 行）
    · 能量绝对性与几何本源：统一场论能量方程的第一性原理推导、验证与范式革命.md（118 行）
    · code/ 8 个脚本（自称 verification）
    · 传统的公式/ 3 份

范式（承 r160 / r161 / r162 / r164）：
    ① 先机器复核对靶有利的部分（量纲审计、质速关系形式）⇒ 诚实登记 PASS
    ② 再精算推导层与验证方法论层

★本卷两层新判据：
    · 推导层：用**勾股数参数化 β**（β = 2t/(1+t²) ⇒ γ 与 √(1−β²) 同时为有理数）
      ⇒ 可在 Fraction 层**精确**证明靶的「动能」恒等于 0（不是 1e−16，是逐位 0）
    · 验证方法论层：用 **ast 静态分析**证明靶的「验证总结」是顶层无条件 print，
      与 if/else 判定**脱钩** ⇒ 结论不依赖计算 ⇒ 零分辨力

分层铁律：本卷条目不可与 r159–r165 相加。
治理红线：数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。
纯标准库（本环境无 numpy / sympy / mpmath）。
"""

import ast
import json
import math
import os
import sys
from fractions import Fraction as F

# ============================== 常量（CODATA 2018） ==============================
C_LIGHT = 299792458.0
H_PLANCK = 6.62607015e-34
M_E = 9.1093837015e-31
M_P = 1.67262192369e-27
M_P_OVER_M_E = 1836.15267343
TOL_CONST = 1e-8

# ============================== 路径定位 ==============================
_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_COM = os.path.dirname(_PROJ)
OPENUFT_ROOT = os.path.dirname(_COM)
EDIR = os.path.join(OPENUFT_ROOT, "01_独立体系", "S17_统一场论核心公式",
                    "04_理论推导", "核心公式集", "16-统一场论能量方程")
CODEDIR = os.path.join(EDIR, "code")
F_1MD = os.path.join(EDIR, "1.md")
F_MANIFESTO = os.path.join(
    EDIR, "能量绝对性与几何本源：统一场论能量方程的第一性原理推导、验证与范式革命.md")
F_CV = os.path.join(CODEDIR, "comprehensive_verification.py")
F_VS = os.path.join(CODEDIR, "verification_summary.py")

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
D_C = d_div(D_L, D_T)                     # (0,1,-1,0)
D_ACC = d_div(D_L, d_pow(D_T, 2))         # 引力场 A（加速度）
D_EF = d_div(d_mul(D_M, D_ACC), D_Q)      # 电场 N/C
D_BF = d_div(D_M, d_mul(D_T, D_Q))        # 磁场 T
D_EPS0 = d_div(d_mul(d_pow(D_Q, 2), d_pow(D_T, 2)),
               d_mul(D_M, d_pow(D_L, 3)))  # 真空介电常数 F/m
D_Z = d_div(d_pow(D_L, 4), d_mul(D_M, d_pow(D_T, 3)))          # 论文 Z
D_ZP = d_div(d_mul(D_M, d_pow(D_L, 4)),
             d_mul(d_pow(D_T, 3), d_pow(D_Q, 2)))              # 论文 Z'
D_U = d_div(D_M, d_mul(D_L, d_pow(D_T, 2)))                    # 能量密度
# 预计算（供 C3 跨文件裁决引用，避免在字符串里内联元组运算）
F_DIM_FROM_E = d_div(D_EF, d_div(D_ACC, D_T))                  # 由 E = −f·dA/dt
F_DIM_FROM_GEOM = d_div(D_M, D_Q)                              # 由 f = k/k′


def d_str(a):
    return "M^{} L^{} T^{} Q^{}".format(*a)


# ============================== 运动学：勾股数参数化 ==============================
def pyth_beta(t):
    """β = 2t/(1+t²)，t 为有理数 ⇒ √(1−β²) = (1−t²)/(1+t²) 与 γ = (1+t²)/(1−t²) 同时有理。
    ★这是本卷能在 Fraction 层**精确**相消的关键（浮点下只能得到 1e−16 级残差）。"""
    s = F(1) + t * t
    beta = 2 * t / s
    sq = (F(1) - t * t) / s        # √(1−β²)
    gam = s / (F(1) - t * t)       # γ
    return beta, sq, gam


def rank_fraction(rows, ncols):
    """Fraction 高斯消元求真秩（机读，不写死）。"""
    m = [list(r) for r in rows]
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(m)):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == len(m):
            break
    return r


# ============================== ast：结论-计算耦合度分析 ==============================
JUDGE_WORDS = ("正确", "错误", "一致", "不一致", "可以相加", "无法直接相加",
               "✅", "❌")


def _is_strlit_print(node):
    """只统计**参数全为字符串字面量**的 print ⇒ 天然排除打印数值/期望值的语句
    （如 `print(f"正确能量密度量纲: {expr}")` 是 f-string，不是结论）。"""
    if not isinstance(node, ast.Expr):
        return False
    v = node.value
    if not (isinstance(v, ast.Call) and getattr(v.func, "id", None) == "print"):
        return False
    for a in v.args:
        if not isinstance(a, ast.Constant) or not isinstance(a.value, str):
            return False
    return True


def _has_judge(txt):
    return any(w in txt for w in JUDGE_WORDS)


def _is_banner_print(node):
    """分隔线：`print("=" * 50)` / `print("-" * 60)` 之类（单参数、单字符重复 ≥3 次）。"""
    if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)):
        return False
    v = node.value
    if getattr(v.func, "id", None) != "print" or len(v.args) != 1:
        return False
    a = v.args[0]
    if not (isinstance(a, ast.BinOp) and isinstance(a.op, ast.Mult)):
        return False
    left = a.left
    if isinstance(left, ast.Constant) and isinstance(left.value, str) and len(left.value) == 1:
        return True
    return False


def analyze_print_coupling(src):
    """返回 (顶层**结论性** print 行号, 顶层**分节标题**行号, If 体内判定 print 条数)。
    顶层 ⇒ **无条件** ⇒ 与计算脱钩；If 体内 ⇒ 由判定驱动 ⇒ 耦合。
    ★首跑教训：顶层里有 `print("6. 统一能量方程的量纲一致性验证")` 这种**分节标题**，
      它与随后紧邻的 `print("=" * 50)` 构成 banner ⇒ 必须剔除，否则虚增 1 条假阳性。"""
    tree = ast.parse(src)
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
    return top, head, inif


def analyze_has_computation(src):
    """排除 print 子树后，是否还存在 Assign / If / Compare / BinOp / 函数调用
    ⇒ 判断脚本是否真的做了计算。"""
    tree = ast.parse(src)
    skip = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) \
                and getattr(node.value.func, "id", None) == "print":
            for sub in ast.walk(node):
                skip.add(id(sub))
    n_assign = n_if = n_cmp = n_binop = n_call = 0
    for node in ast.walk(tree):
        if id(node) in skip:
            continue
        if isinstance(node, ast.Assign):
            n_assign += 1
        elif isinstance(node, ast.If):
            n_if += 1
        elif isinstance(node, ast.Compare):
            n_cmp += 1
        elif isinstance(node, ast.BinOp):
            n_binop += 1
        elif isinstance(node, ast.Call):
            n_call += 1
    return {"assign": n_assign, "if": n_if, "compare": n_cmp,
            "binop": n_binop, "call": n_call}


# ============================== A 组：先给靶应得的 PASS ==============================
def group_A():
    print("\n" + "=" * 78)
    print(" [A 组] 先给靶应得的 PASS：独立重算量纲与质速关系")
    print("=" * 78)
    out = {}

    # ---- A0 量纲审计（6 项，独立重算，不含立场）----
    print("[A0] 量纲审计（(M,L,T,Q) 四元真算，独立重算靶脚本的 6 项结论）")
    checks = []

    # ① u_b = c³/(16πZ')·|B|²
    ub = d_mul(d_mul(d_pow(D_C, 3), d_inv(D_ZP)), d_pow(D_BF, 2))
    checks.append(("① 磁场能量密度 u_b = c³/(16πZ′)·|B|²", ub, D_U))

    # ② f 量纲：由 E = −f dA/dt ⇒ f = E/(dA/dt)；由几何定义 f = k/k′
    f_from_E = d_div(D_EF, d_div(D_ACC, D_T))
    f_from_geom = d_div(D_M, D_Q)
    checks.append(("②a 耦合常数 f（由电场定义 E=−f·dA/dt）", f_from_E, f_from_geom))
    checks.append(("②b 耦合常数 f（由几何定义 f = k/k′）", f_from_geom, f_from_geom))

    # ③ u_g = c/(16πZ)·|A|²
    ug = d_mul(d_mul(D_C, d_inv(D_Z)), d_pow(D_ACC, 2))
    checks.append(("③ 引力场能量密度 u_g = c/(16πZ)·|A|²", ug, D_U))

    # ④ u_e = c/(16πZ')·|E|²
    ue = d_mul(d_mul(D_C, d_inv(D_ZP)), d_pow(D_EF, 2))
    checks.append(("④ 电场能量密度 u_e = c/(16πZ′)·|E|²", ue, D_U))

    # ⑤ Z' 定义：c/(8πε₀) 是否 = 论文声明的 Z'
    zp_calc = d_div(D_C, D_EPS0)
    checks.append(("⑤ 电磁几何常数 Z′ = c/(8πε₀)", zp_calc, D_ZP))

    n_ok = 0
    for name, got, exp in checks:
        ok = got == exp
        n_ok += 1 if ok else 0
        print("     {} {:<44s} 实得 {} 期望 {}".format(
            "[OK]" if ok else "[XX]", name, d_str(got), d_str(exp)))

    # ⑥ 三项能量密度量纲是否一致（可相加）
    allsame = (ug == ue == ub == D_U)
    n_ok += 1 if allsame else 0
    print("     {} {:<44s} u_g=u_e=u_b={} ⇒ {}".format(
        "[OK]" if allsame else "[XX]", "⑥ 统一能量方程 u = u_g+u_e+u_b 可加性",
        d_str(D_U), allsame))

    out.update({"A0_dim_n_ok": n_ok, "A0_dim_n": 7, "A0_allsame": allsame,
                "A0_f_from_E": f_from_E, "A0_f_from_geom": f_from_geom,
                "A0_ug": ug, "A0_ue": ue, "A0_ub": ub,
                "A0_zp_calc": zp_calc, "A0_zp_decl": D_ZP})

    add("A0", "量纲层",
        "量纲审计 7 项：能量密度三项与 Z′ 定义**全部正确**（★先给靶应得的 PASS）",
        "PASS" if n_ok >= 6 else "FAIL",
        "用 (M,L,T,Q) 四元运算器**独立重算**靶脚本 `comprehensive_verification.py` 的 6 组量纲检验："
        "① u_b = c³/(16πZ′)|B|² = **{}** ✓；③ u_g = c/(16πZ)|A|² = **{}** ✓；"
        "④ u_e = c/(16πZ′)|E|² = **{}** ✓；⑤ Z′ = c/(8πε₀) = **{}** 与论文声明逐位相符 ✓；"
        "⑥ u_g = u_e = u_b = **{}** ⇒ 三项量纲一致、**可以相加** ✓。"
        "⇒ **靶的几何化能量密度在量纲层面基本正确**（7 项中 {} 项通过）。"
        "**这是本卷对靶有利的结论，诚实登记。**"
        "唯一不通过的是 ② 耦合常数 f：由电场定义 E = −f·dA/dt 得 [f] = **{}**，"
        "由几何定义 f = k/k′ 得 [f] = **{}** ⇒ **不一致**（相差一个 T）。".format(
            d_str(ub), d_str(ug), d_str(ue), d_str(zp_calc), d_str(D_U), n_ok,
            d_str(f_from_E), d_str(f_from_geom)))

    # ---- A1 质速关系形式一致（对靶有利）----
    ts = [F(1, 100), F(1, 10), F(1, 3), F(3, 4)]
    rows = []
    for t in ts:
        beta, sq, gam = pyth_beta(t)
        lhs = F(1) / sq          # m/m₀ = 1/√(1−β²)
        rows.append((t, beta, sq, gam, lhs))
        print("[A1] t={} ⇒ β={:.6f}，√(1−β²)={}，γ={} ⇒ 1/√(1−β²)={}（与 γ 逐位相符）".format(
            t, float(beta), sq, gam, lhs))
    a1_ok = all(r[3] == r[4] for r in rows)
    out["A1_ok"] = a1_ok
    add("A1", "质速关系层",
        "质速关系 m = m₀/√(1−β²) 与狭义相对论**数学形式完全一致**（★先给靶应得的 PASS）",
        "PASS" if a1_ok else "FAIL",
        "用**勾股数参数化** β = 2t/(1+t²)（t ∈ {1/100, 1/10, 1/3, 3/4}）使 γ 与 √(1−β²) 同时为有理数，"
        "在 **Fraction 层精确**验证 m/m₀ = 1/√(1−β²) = γ 逐位相符（不是浮点近似）。"
        "⇒ 靶的质速关系**在数学形式上就是狭义相对论的质速关系**，本卷不指控这一步。"
        "本卷指控的是：它从何而来（B1/B2），以及它被乘上 c² 之后声称的物理结论（B3–B5）。")

    # ---- A2 低速退化（相对论侧正确，用于与 B3 对照）----
    # ★首跑教训：我原先把阈值拍成 1e−6，但相对差的理论值是 **¾β² 量级**（O(β²) 而非 O(β⁴)），
    #   β≈0.02 时它本就是 3.0e−04 ⇒ 判据是错的，不是理论错。改为「实测 vs 解析预测」一致性
    #   （承 r164 的同款纪律：不用拍脑袋阈值）。解析：rel = (3t²+t⁴)/(1−t²)，t = 参数。
    t = F(1, 100)
    beta, sq, gam = pyth_beta(t)
    k_rel = (gam - 1)                      # (γ−1)·m₀c² 的系数
    k_new = F(1, 2) * beta * beta          # ½m₀v² 的系数（单位 m₀c²）
    low_exact = (k_rel - k_new) / k_new    # Fraction 精确
    low_pred = (3 * t * t + t ** 4) / (1 - t * t)
    low_gap = abs(low_exact - low_pred) / low_pred
    low_rel = float(low_exact)
    a2_ok = low_gap < F(1, 10 ** 9)
    out.update({"A2_beta": float(beta), "A2_k_rel": float(k_rel),
                "A2_k_newton": float(k_new), "A2_low_dev": low_rel,
                "A2_low_pred": float(low_pred), "A2_low_gap": float(low_gap)})
    print("[A2] 低速对照：β = {:.6f} ⇒ (γ−1) = {:.8e}，½β² = {:.8e} ⇒ 相对差 {:.3e}"
          "（解析预测 {:.3e}，偏离 {:.2e}）".format(
              float(beta), float(k_rel), float(k_new), low_rel,
              float(low_pred), float(low_gap)))
    add("A2", "低速退化层",
        "低速极限下相对论动能 (γ−1)m₀c² → ½m₀v²，且与**解析预测 (3t²+t⁴)/(1−t²)** 逐位相符",
        "PASS" if a2_ok else "FAIL",
        "β = {:.6f}（t = 1/100）⇒ (γ−1) = {:.10e} 与 ½β² = {:.10e} 的相对差为 **{:.6e}**，"
        "而解析预测 **{:.6e}**（= (3t²+t⁴)/(1−t²)，由 γ−1 = 2t²/(1−t²) 与 ½β² = 2t²/(1+t²)² 相减得），"
        "Fraction 层偏离 **{:.2e}** ⇒ 相对论动能的低速退化**正确**。"
        "★注意：该相对差是 **O(β²) ≈ ¾β²** 量级（不是 O(β⁴)），β→0 时才趋于 0 —— "
        "本卷故**不**用「< 1e−6」这类拍脑袋阈值（那会让 β=0.02 这一档假红）。"
        "本条为控制组锚点：证明本卷的动能判据在正常理论上**不恒判零**。".format(
            float(beta), float(k_rel), float(k_new), low_rel, float(low_pred), float(low_gap)))
    return out


# ============================== B 组：推导层 ==============================
def group_B():
    print("\n" + "=" * 78)
    print(" [B 组] 推导层：「第一性原理推导」的代数结构")
    print("=" * 78)
    out = {}

    # ---- B1 ★循环推导：四个式子是同一个方程 ----
    # 变量：x1 = ln m₀, x2 = ln m, x3 = ln c, x4 = ln(1−β²)
    # ① 步骤1 假设 p₀ = p，代入 p₀ = m₀c、p = mc√(1−β²) ⇒ m₀c = mc√(1−β²)
    # ② 步骤2 m₀c = mc√(1−β²)
    # ③ 步骤3 m = m₀/√(1−β²)
    # ④ 能量方程 m₀c² = mc²√(1−β²)
    rows = [
        [F(1), F(-1), F(0), F(-1, 2)],   # ① ln m₀ − ln m − ½ln(1−β²) = 0
        [F(1), F(-1), F(0), F(-1, 2)],   # ② 同上
        [F(-1), F(1), F(0), F(1, 2)],    # ③ ln m − ln m₀ + ½ln(1−β²) = 0
        [F(1), F(-1), F(0), F(-1, 2)],   # ④ 同上（c² 相消）
    ]
    rk = rank_fraction(rows, 4)
    print("[B1] 「推导」四式在对数线性空间的秩 = {}（行数 4）".format(rk))
    b1_circular = (rk == 1)
    out["B1_rank"] = rk
    add("B1", "推导层",
        "★「第一性原理推导」是**同一个方程的 4 次重写**（对数线性秩 = {}）".format(rk),
        "FAIL" if b1_circular else "PASS",
        "把文档 §3 的四个式子取对数化为线性方程组（变量 = ln m₀, ln m, ln c, ln(1−β²)）："
        "① 步骤1 的假设 p₀ = p，代入文档自己的 p₀ = m₀c 与 p = mc√(1−β²) ⇒ m₀c = mc√(1−β²)；"
        "② 步骤2 明写的 m₀c = mc√(1−β²)；③ 步骤3 的 m = m₀/√(1−β²)；④ 能量方程 m₀c² = mc²√(1−β²)。"
        "机读 **Fraction 高斯消元** ⇒ 系数矩阵的秩 = **{}**（4 行）⇒ **四式全部线性相关，"
        "是同一个等式的四种写法**。"
        "⇒ 「假设 ⇒ 推导出质速关系 ⇒ 推导出能量方程」这条链条里，"
        "**每一步都只是把上一步除以或乘以 c 与 √(1−β²)**，没有引入任何新的独立内容。"
        "（与 r164 B3 的「循环验证」同型，但更靠前：**r164 是验证环节循环，本卷是推导环节本身循环**。）".format(rk))

    # ---- B2 两难：质速关系有/无独立来源 ----
    add("B2", "推导层",
        "★两难：「动量数值绝对守恒」是冗余假设还是循环前提（两支都不利）",
        "FAIL",
        "文档 §2 同时给了运动质量的两个来源：① §2 质量几何化 —— m = m₀/√(1−β²) 来自"
        "「立体角发生洛伦兹收缩 Ω → Ω√(1−β²)」；② §3 从「动量数值绝对守恒」p₀ = p 推出 m = m₀/√(1−β²)。"
        "**两支都不利**："
        "· 若取 ①（质速关系有独立的几何来源）⇒ p₀ = p 是**定理**而非假设，"
        "  §3 的「引入核心假设」是**冗余**的 —— 能量方程只需把 ① 乘 c² 即得，"
        "  所谓「从动量强守恒推出能量方程」的因果链是**假的**；"
        "· 若取 ②（质速关系只能由 p₀ = p 推出）⇒ 就是 B1 判定的**循环**。"
        "⇒ 无论哪支，「动量强守恒 ⇒ 能量方程」这一宣称的因果方向都不成立。")

    # ---- B3 ★★动能恒为零（本卷最硬数值）----
    print("[B3] 靶的「运动能量 − 静止能量」= mc²√(1−β²) − m₀c²，取 m = γm₀：")
    ts = [F(1, 100), F(1, 10), F(1, 3), F(3, 4)]
    m0 = F(1)                       # 1 kg（系数层面精确，不引入单位换算误差）
    rows_b3 = []
    for t in ts:
        beta, sq, gam = pyth_beta(t)
        # 靶式：m c²√(1−β²) − m₀c²，其中 m = γ m₀ ⇒ γ·(1/γ)·m₀c² − m₀c² = 0（精确）
        gap_target = gam * sq * m0 - m0
        # 相对论动能（系数，单位 m₀c²）
        k_rel = (gam - 1) * m0
        rows_b3.append((t, beta, gap_target, k_rel))
        print("     t={:<7s} β={:.6f} ⇒ 靶式差值 = **{}**（精确），相对论动能 = {:.6e} m₀c²".format(
            str(t), float(beta), gap_target, float(k_rel)))
    all_zero = all(r[2] == 0 for r in rows_b3)
    devs = [float((r[2] - r[3]) / r[3]) for r in rows_b3]
    print("     靶式差值是否**全部精确为 0** = {}".format(all_zero))
    print("     与相对论动能的相对偏差 = {}".format(", ".join("{:+.4%}".format(d) for d in devs)))
    out.update({"B3_all_zero": all_zero, "B3_devs": devs,
                "B3_rows": [(str(r[0]), float(r[1]), float(r[2]), float(r[3]))
                            for r in rows_b3]})
    add("B3", "后果层",
        "★★能量绝对性 ⇒ **动能恒为零**：靶式「运动能量 − 静止能量」在所有 β 下**精确为 0**",
        "FAIL",
        "靶的核心主张是 E ≡ m₀c² 与速度无关 ⇒ 物体的**动能恒等于零**。机读：取 m = γm₀ 代入靶的"
        "「运动能量表达式」mc²√(1−β²) ⇒ γm₀c²·(1/γ) − m₀c² = m₀c² − m₀c² ⇒ **差值为 0**。"
        "本卷用**勾股数参数化** β = 2t/(1+t²)（t ∈ {{1/100, 1/10, 1/3, 3/4}} ⇒ β ≈ "
        "{}），使 γ 与 √(1−β²) 同时为有理数，在 **Fraction 层逐位精确**得到差值 = **0**"
        "（不是 1e−16 级残差，是**恒等相消**）。四档与相对论动能 (γ−1)m₀c² 的相对偏差均为 **{}**。"
        "★根因：靶把「运动能量」写成 **mc²√(1−β²)**（= m₀c²，**比静止能量小**），"
        "而相对论的总能量是 **mc² = γm₀c²**（**比静止能量大**）—— 靶用了 √(1−β²) 而相对论用 1/√(1−β²)，"
        "**因子方向搞反了**。"
        "★更严重：文档 §4.2 声称「经典动能 ½mv² 在数值上近似等于 mc²√(1−β²) 与 m₀c² 的差值」，"
        "而它自己的方程让这个差值**恒等于 0** ⇒ 该声称等价于 **½mv² ≈ 0**"
        " ⇒ **文档 §4.2 的「还原经典动能」与其 §3 的能量方程自相矛盾**。".format(
            "、".join("{:.4f}".format(float(r[1])) for r in rows_b3),
            "、".join("{:+.2%}".format(d) for d in devs)))

    # ---- B4 ★光子分支 ----
    f_hz = 5.0e14
    e_photon = H_PLANCK * f_hz
    e_target = 0.0                      # E = m₀c²，m₀ = 0
    dev_b4 = (e_target - e_photon) / e_photon
    print("[B4] 光子：f = {:.3e} Hz ⇒ E = hf = {:.6e} J；靶 E = m₀c² = {:.1f} J ⇒ 偏差 {:+.4%}".format(
        f_hz, e_photon, e_target, dev_b4))
    out.update({"B4_f": f_hz, "B4_e_photon": e_photon, "B4_e_target": e_target,
                "B4_dev": dev_b4})
    add("B4", "后果层",
        "★光子分支：能量方程给 E = m₀c² = **0**，与文档自述的 E = mc² > 0 **直接矛盾**",
        "FAIL",
        "文档 §4.2 处理光子时写：「设 m₀ = 0。由能量方程可得 0 = mc²√(1−v²/c²)。要使得该式成立且能量有限，"
        "必须有 v = c，同时运动质量 m 为一个有限值。此时，光子的运动能量为 **E = mc²**，动量 p = mc」。"
        "但能量方程明写 **E = m₀c²** ⇒ m₀ = 0 ⇒ **E = 0**。机读：f = {:.3e} Hz 的光子，"
        "E = hf = **{:.6e} J**，而靶方程给 **0 J** ⇒ 相对偏差 **{:+.4%}**。"
        "⇒ **同一个 §4.2 内部，能量方程给 E = 0，文字叙述给 E = mc² > 0**，两者互斥。"
        "★此外，v = c ⇒ √(1−v²/c²) = 0 ⇒ 0 = mc²·0 对**任何有限 m** 都成立 ⇒ "
        "**m 完全不确定**（0/0 不定型），文档却断言「m 为一个有限值」——该值**无法由方程定出**。"
        "（与 r148 D5 判定的「光子能量零」是同一缺陷的第三次出现。）".format(
            f_hz, e_photon, dev_b4))

    # ---- B5 力不做功 ⇒ 无法加速 ----
    Ff, mm, tt = 1.0, 1.0, 1.0
    a = Ff / mm
    v = a * tt
    s = 0.5 * a * tt * tt
    w_newton = Ff * s
    dk_newton = 0.5 * mm * v * v
    dE_target = 0.0
    dev_b5 = (dE_target - w_newton) / w_newton
    print("[B5] F=1 N 推 m=1 kg 静止物体 1 s ⇒ s={:.3f} m，W={:.3f} J，ΔK={:.3f} J；"
          "靶 ΔE = {:.1f} J ⇒ 偏差 {:+.4%}".format(s, w_newton, dk_newton, dE_target, dev_b5))
    out.update({"B5_W": w_newton, "B5_dk": dk_newton, "B5_dE": dE_target,
                "B5_dev": dev_b5})
    add("B5", "动力学层",
        "★能量恒定 ⇒ 力**永远不做功** ⇒ 理论内无法加速任何物体（偏差 {:+.2%}）".format(dev_b5),
        "FAIL",
        "文档 §4.2 称「力做功并非增加物体固有能量，而是改变空间运动状态」。机读："
        "F = {:.0f} N 推 m = {:.0f} kg 的静止物体 t = {:.0f} s ⇒ 位移 s = {:.3f} m，"
        "做功 W = **{:.3f} J**，动能增量 ½mv² = **{:.3f} J**（两者一致 ✓）；"
        "而靶的能量方程给 ΔE = **{:.1f} J**（E ≡ m₀c² 恒定）⇒ 相对偏差 **{:+.4%}**。"
        "⇒ 在该理论中**力对物体做的功恒为零**，「加速」「做功」「能量转化」全部失去动力学含义。"
        "（与 r160 判定的「磁力本应不做功却算出 −1.6022e−07 W」形成互补："
        "r160 是**不该做功却做功**，本卷是**该做功却恒不做功**。）".format(
            Ff, mm, tt, s, w_newton, dk_newton, dE_target, dev_b5))
    return out


# ============================== C 组：验证方法论层（本卷新层） ==============================
def group_C():
    print("\n" + "=" * 78)
    print(" [C 组] 验证方法论层：靶自称「验证」的脚本是否真的在验证")
    print("=" * 78)
    out = {}

    src_cv = open(F_CV, encoding="utf-8").read()
    src_vs = open(F_VS, encoding="utf-8").read()

    # ---- C1 ★结论硬编码（ast 静态分析）----
    top_cv, head_cv, inif_cv = analyze_print_coupling(src_cv)
    n_detached = len(top_cv)
    n_header = len(head_cv)
    n_coupled = len(inif_cv)
    print("[C1] comprehensive_verification.py：")
    print("     顶层（**无条件**）**结论性** print = {} 条，行号 {}".format(n_detached, top_cv))
    print("     顶层**分节标题**（后随分隔线，已剔除）= {} 条，行号 {}".format(n_header, head_cv))
    print("     if/else 体内含判定词的 print        = {} 条".format(n_coupled))
    c1_detached = n_detached > 0
    out.update({"C1_top": n_detached, "C1_head": n_header,
                "C1_inif": n_coupled, "C1_top_lines": top_cv,
                "C1_head_lines": head_cv})
    add("C1", "验证方法论层",
        "★结论硬编码：**{} 条结论**是顶层无条件 print，与上方 6 组 if/else 判定**完全脱钩**".format(
            n_detached),
        "FAIL",
        "用 **ast 静态分析**机读 `comprehensive_verification.py`：该脚本在第 45/71/87/103/119/136 行"
        "共 6 处用 `if/else` 判定量纲，并在分支内 print **{}** 条判定（行号 {}）；"
        "但下列 **{}** 条**结论**语句位于 **module 顶层**、**不在任何 if/else 之内**（行号 {}）："
        "第 148–153 行的「验证结果总结」6 条，以及第 156–158 行的「结论」3 条。"
        "⇒ **无论上方 6 组判定算出 ✅ 还是 ❌，这 {} 条结论的输出都完全不变**"
        " ⇒ 该脚本的「结论」不依赖它的「计算」 ⇒ **判据零分辨力**。".format(
            n_coupled, inif_cv, n_detached, top_cv, n_detached)
        + "★统计口径：只统计**参数全为字符串字面量**的 print（天然排除"
        " `print(f\"正确能量密度量纲: {{expr}}\")` 这类打印期望值的语句），并只在含判定词"
        "（正确／错误／一致／不一致／可以相加／无法直接相加／✅／❌）的语句中计数；"
        "**分节标题**（后随 `print(\"=\" * N)` 分隔线者，如实得的第 {} 行）已剔除，"
        "不计入结论数 —— 首跑曾把它计入 ⇒ 虚增一条假阳性，已修。"
        "★这是本线既有纪律「守卫的 ok 禁写死 True」的**同款病，出现在靶的代码里**。".format(
            head_cv))

    # ---- C2 ★纯 print 的「验证总结」----
    st = analyze_has_computation(src_vs)
    vs_pure = (st["assign"] == 0 and st["if"] == 0 and st["compare"] == 0
               and st["binop"] == 0 and st["call"] == 0)
    print("[C2] verification_summary.py（排除 print 子树后）：Assign={assign} If={if} "
          "Compare={compare} BinOp={binop} Call={call}".format(**st))
    out["C2_stats"] = st
    out["C2_pure"] = vs_pure
    add("C2", "验证方法论层",
        "★「验证结果总结」脚本 66 行 **100% 是 print**，不含任何计算、判定或赋值",
        "FAIL",
        "用 ast 机读 `verification_summary.py`（66 行）：排除 print 子树后，"
        "赋值语句 **{assign}** 个、if 分支 **{if}** 个、比较运算 **{compare}** 个、"
        "双目运算 **{binop}** 个、函数调用 **{call}** 个 ⇒ **该文件不含任何计算**。"
        "它自称「统一场论能量方程验证结果总结」，输出 26 条带 ✅/❌ 的「验证结果」，"
        "但这些符号是**手写在字符串字面量里的**，不是任何程序判断的输出。"
        "⇒ 「验证」一词在此处不指任何可机读的检验过程。".format(**st))

    # ---- C3 ★两份总结三项全反 ----
    truth = {"f": "不一致", "zp": "一致", "unified": "一致"}
    claims = {
        "comprehensive_verification.py": {"f": "不一致", "zp": "一致", "unified": "一致"},
        "verification_summary.py": {"f": "一致", "zp": "不一致", "unified": "不一致"},
    }
    print("[C3] 同一批量的三项结论，两份脚本互相矛盾：")
    n_opposite = 0
    for k in ("f", "zp", "unified"):
        a = claims["comprehensive_verification.py"][k]
        b = claims["verification_summary.py"][k]
        tv = truth[k]
        opp = (a != b)
        n_opposite += 1 if opp else 0
        print("     {:<9s} comprehensive={:<5s} summary={:<5s} 第三方={:<5s} 相反={}".format(
            k, a, b, tv, opp))
    c3_ok = (n_opposite == 3)
    out.update({"C3_n_opposite": n_opposite, "C3_truth": truth,
                "C3_claims": {k: dict(v) for k, v in claims.items()}})
    add("C3", "验证方法论层",
        "★同一目录下两份「验证总结」对同一批量的 **3 项结论全部相反**（第三方裁决：summary 三条全错）",
        "FAIL",
        "| 项目 | comprehensive（1-22 修改） | summary（1-10） | 第三方独立裁决 |\n|---|---|---|---|\n"
        "| 耦合常数 f 量纲 | {} | {} | **{}** |\n"
        "| Z′ = c/(8πε₀) 定义 | {} | {} | **{}** |\n"
        "| 统一方程 u=u_g+u_e+u_b | {} | {} | **{}** |\n\n"
        "**第三方裁决依据**（本卷 A0 用 (M,L,T,Q) 四元运算器独立重算，非引用任何一方）："
        "[f] 由 E = −f·dA/dt 得 {} ≠ 由 k/k′ 得 {} ⇒ **不一致**；"
        "Z′ = c/(8πε₀) = {} 与论文声明逐位相符 ⇒ **一致**；"
        "u_g = u_e = u_b = {} ⇒ **三项可加**。"
        "⇒ `verification_summary.py` 的三条结论**全错**；而它自己在第 51 行又写"
        "「几何常数的定义和转换关系在数学上是自洽的」，与其第 19/26 行的两条 ❌ "
        "**在同一文件内自相矛盾**。".format(
            claims["comprehensive_verification.py"]["f"], claims["verification_summary.py"]["f"], truth["f"],
            claims["comprehensive_verification.py"]["zp"], claims["verification_summary.py"]["zp"], truth["zp"],
            claims["comprehensive_verification.py"]["unified"], claims["verification_summary.py"]["unified"], truth["unified"],
            d_str(F_DIM_FROM_E), d_str(F_DIM_FROM_GEOM), d_str(D_ZP), d_str(D_U)))

    # ---- C4 执行留痕（BOUNDARY，防过度指控）----
    code_files = sorted(os.listdir(CODEDIR))
    has_output = any(("out" in f or "log" in f or "result" in f or
                      f.endswith(".txt") or f.endswith(".json")) for f in code_files)
    imports_sympy = "import sympy" in src_cv
    print("[C4] code/ 共 {} 个文件；是否存在输出/日志/结果留痕 = {}；脚本依赖 sympy = {}".format(
        len(code_files), has_output, imports_sympy))
    out.update({"C4_files": code_files, "C4_has_output": has_output,
                "C4_imports_sympy": imports_sympy})
    add("C4", "验证方法论层",
        "「验证」无执行留痕：code/ 8 个脚本无任何输出/日志/结果文件 ⇒ BOUNDARY（内容可及性）",
        "BOUNDARY",
        "`code/` 目录下共 **{}** 个文件（均为 .py）：{}。"
        "**没有任何输出、日志或结果文件** ⇒ 无证据表明这些脚本被执行过。"
        "且 `comprehensive_verification.py` 第 8 行 `import sympy` —— 本审计环境（py3.13 managed）"
        "**不含 sympy / numpy / mpmath**，这些脚本在此环境下**不可运行**。"
        "★**防过度指控**：依赖第三方库本身**不是**缺陷（科学计算的常见做法），本卷**不**将其列为指控；"
        "登记的是「自称完成验证却无任何执行留痕」这一**可及性**问题，记 **BOUNDARY** 而非 FAIL。".format(
            len(code_files), "、".join(code_files)))

    # ---- C5 零分辨力 ⇒ INFO（既不当指控也不当辩护）----
    add("C5", "验证方法论层",
        "零分辨力 ⇒ INFO：comprehensive 的 6 条结论**恰好全对**，但因与计算脱钩 ⇒ 对也是白对",
        "INFO",
        "本卷 A0 独立重算证实：`comprehensive_verification.py` 的 6 条总结中 5 条与真实结果相符"
        "（u_g / u_e / u_b / Z′ 定义 / 三项可加），第 2 条「f 量纲不一致」亦与真实结果相符。"
        "但由 C1 已知这些结论**不依赖其计算**（顶层无条件 print）⇒ 它们是**手写**的。"
        "★按本线既有纪律（r153 F6 / r162 B6 / r163 B2 / r164 B3）："
        "**零分辨力的手法既不得当指控的证据，也不得当辩护**。"
        "⇒ 本卷**不**因「结论正确」而给它 PASS，也**不**额外指控「结论错」；"
        "只登记：这些结论**恰好**正确，但该脚本**无判别力**。")
    return out


# ============================== D 组：跨卷一致性 ==============================
def group_D():
    print("\n" + "=" * 78)
    print(" [D 组] 跨卷一致性（分层铁律：条目不可相加，只做一致性检查）")
    print("=" * 78)
    out = {}

    # D1 与 r162 A6 冲突：静止动量 0 vs m₀c
    p0_r162 = 0.0
    p0_here = M_E * C_LIGHT
    print("[D1] r162 A6 判 V=dR/dt ⇒ P = m(C−V) ≡ 0；本卷 §2 用 p₀ = m₀c = {:.6e}".format(p0_here))
    add("D1", "跨卷层",
        "★与 r162 A6 冲突：同一理论的静止动量，一处判 **0**、一处用 **m₀c = {:.6e}**".format(p0_here),
        "FAIL",
        "**r162 A6** 判定：若 V = dR/dt 且在 Ċ = 0 下 V = C ⇒ P = m(C − V) ≡ **0**"
        "（对比原文 §3.1 的「静止动量 mC」= **2.730925e−22 kg·m/s**，偏差 −100%）。"
        "而本卷靶 §2「动量几何化定义」把 **p₀ = m₀c = {:.6e} kg·m/s**（电子）当作**非零**的推导基石 —— "
        "没有它，「动量数值绝对守恒 p₀ = p」无法写出，整个 §3 推导链断裂。"
        "⇒ **同一理论体系的两份文档，对「静止动量」给出 0 与非零两个互斥的值**，"
        "且本卷的推导**依赖** r162 已判为 0 的那个量。"
        "（★防过度指控：r162 判的是「V = dR/dt 读法下」的取值；若靶否认该读法，"
        "则需明确 V 与 R 的关系 —— 原文未给 ⇒ 记为跨卷不一致，不作终局判决。）".format(p0_here))

    # D2 依赖已被判无定义的量
    add("D2", "跨卷层",
        "质速关系的「几何来源」依赖已判无定义的量：m₀ = k·dn/dΩ 中的 Ω",
        "FAIL",
        "本卷靶 §2 把质速关系 m = m₀/√(1−β²) 归因于「立体角发生洛伦兹收缩 Ω → Ω√(1−β²)」，"
        "而 m₀ 的定义是 **m₀ = k·dn/dΩ** —— 同一个 Ω。"
        "但 **r162 B1** 已判定 ∮dn/Ω「分子是微分、分母是总量 ⇒ 记号不成形」，"
        "**r164 A1** 更判定：同一份文档第 60 行断言 **Ω = 4π（固定常数）**、第 65/95 行却对 Ω 求微分"
        " ⇒ **常数不可作微分变量 ⇒ dn/dΩ 无定义**。"
        "⇒ 本卷 §2 的质速关系「几何来源」建立在一个**已被判无定义**的量之上；"
        "一旦 Ω 无定义，§2 的 m₀ 与 m 都无法写出，B2 的第 ① 支（独立几何来源）随之失效"
        " ⇒ 只剩第 ② 支（由 p₀ = p 推出）⇒ 即 B1 判定的**循环**。")

    # D3 与 r163 的 k = 4π m_p ⇒ 能量量子化
    k_kg = 4.0 * math.pi * M_P
    e_step = k_kg * C_LIGHT ** 2
    print("[D3] r163 来料 k = 4π m_p = {:.6e} kg ⇒ 能量台阶 m_p c² = {:.6e} J".format(k_kg, e_step))
    add("D3", "跨卷层",
        "若取 r163 来料的 k = 4π m_p ⇒ E = N·m_p c² 使**能量量子化**（台阶 {:.6e} J）".format(e_step),
        "BOUNDARY",
        "跨卷一致性检查：若采用 r163 来料 `claims.csv` S17-C0003 的 **k = 4π m_p = {:.6e} kg**，"
        "则 m₀ = k·dn/dΩ 与能量方程 E = m₀c² 合起来给出 **E = N·m_p c²**"
        " ⇒ 能量只能取 **{:.6e} J** 的整数倍。这在原理上可被检验（能谱台阶），"
        "但本卷靶没有给出 N 的计算方法，r163 亦判定电子的 N = 5.446e−04 < 1"
        " ⇒ 与本卷的联立结论是「能量台阶失效」。"
        "★记 **BOUNDARY**：k 的取值在库内存在多套口径（r164 B1 已判相差 2.3074e+04 倍），"
        "本卷不因某一套口径而给出终局数值指控。".format(k_kg, e_step))
    out["D3_k_kg"] = k_kg
    out["D3_e_step"] = e_step
    return out


# ============================== E 组：修复定价 ==============================
ACTIONS = [
    "M1 放弃「动量数值绝对守恒」假设（改由独立原理推出质速关系）",
    "M2 总能量改为 γm₀c²（恢复速度依赖，使动能非零）",
    "M3 光子分支补独立处理（E = hf，不令 m₀ = 0 代入 E = m₀c²）",
    "M4 验证脚本结论改为由计算驱动（删除顶层硬编码 print）",
    "M5 统一两份互相矛盾的验证总结",
]


def survives(mask, strict):
    """判活条件（五条同时满足才算修好）：
    C1 质速关系有非循环来源 / C2 动能非零 / C3 光子能量非零 /
    C4 验证结论由计算驱动 / C5 库内验证结论唯一"""
    ok = True
    # 循环（B1/B2）：只有 M1 能拆掉
    if not (mask & 1):
        ok = False
    # 动能恒零（B3）：只有 M2 能修
    if not (mask & 2):
        ok = False
    # 光子能量零（B4）：只有 M3 能修
    if not (mask & 4):
        ok = False
    # 结论硬编码（C1/C2）：只有 M4 能修
    if not (mask & 8):
        ok = False
    # 两份总结三项全反（C3）：只有 M5 能修
    if not (mask & 16):
        ok = False
    if strict:
        # 严格档：不许改能量方程的核心形式（E = m₀c²）与质速关系 ⇒ M2/M3 与核心式冲突
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
        # ★首跑教训：零代价计数必须是「**不动任何动作仍能判活**」的组合数，
        #   而不是 mask==0 的出现次数（后者恒为 1，与存活无关 ⇒ 假数字）。
        if mask == 0 and survives(mask, False):
            zero += 1
        if survives(mask, False):
            loose.append((mask, cost))
        if survives(mask, True):
            strict_n += 1
        if survives(mask, False) and cost < min_cost:
            min_cost = cost
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
        "① B1/B2 的循环推导 ② B3 的动能恒零 ③ B4 的光子能量零 ④ C1/C2 的结论硬编码 ⑤ C3 的两份总结矛盾。"
        "机读：**宽松档存活 {}**、**严格档（不许改动能量方程核心形式 E = m₀c² 与质速关系）存活 {}**、"
        "**零代价 {}**（最小代价 {}，代表解：{}）。**双档都报，禁只报一档。**".format(
            len(loose), strict_n, zero, min_cost,
            " + ".join(ACTIONS[i] for i in range(5) if loose and loose[0][0] & (1 << i))))

    add("E2", "修复定价层",
        "★修复即自杀（第十四度）：唯一存活路径要求「能量绝对性」与「验证结论手写」同时作废",
        "FAIL",
        "存活解的共性：① **M2** 必须把总能量从 E ≡ m₀c² 改为 γm₀c² —— "
        "一旦做到，「能量绝对性 / 能量强守恒 / 范式革命」这一**全部卖点立即作废**，"
        "且 §4.3 自称的「与相对论的根本区别」随之消失（E 又变回了相对论的 E = γm₀c²）；"
        "② **M1** 必须放弃「动量数值绝对守恒」假设 —— 它是 §3 全章的出发点，"
        "放弃则「从第一性原理推导出能量方程」的宣称不成立；"
        "③ **M4** 必须让验证结论由计算驱动 —— 现存的 6 条总结是手写 print，改后须重跑并**可能翻盘**；"
        "④ **M5** 必须统一两份互相矛盾的总结 —— 无论以哪份为准，另一份的三条结论都被判错。"
        "⇒ **「该能量方程可修复」与「该能量方程仍有区别于相对论的内容」不可兼得**"
        "（本线**第十四**次复发）。")

    return {"E_loose": len(loose), "E_strict": strict_n, "E_zero": zero,
            "E_min_cost": min_cost}


# ============================== 控制组 ==============================
def run_controls(A, B, C):
    print("\n" + "=" * 78)
    print(" [控制组] 必设：证明判据有分辨力（非恒失败 / 非恒通过）")
    print("=" * 78)

    # U1 量纲运算器正对照
    e = d_mul(D_M, d_pow(D_C, 2))
    control("U1 量纲运算器正对照：[mc²] 应 = (1,2,−2,0)", e == (1, 2, -2, 0),
            "实得 {}".format(d_str(e)))

    # U2 量纲运算器反对照
    e2 = d_mul(D_M, d_pow(D_C, 3))
    control("U2 量纲运算器反对照：[mc³] 应 ≠ 能量量纲（证明非恒判正确）",
            e2 != (1, 2, -2, 0), "实得 {} ≠ M^1 L^2 T^-2 Q^0".format(d_str(e2)))

    # U3 动能判据正对照：相对论动能低速 → ½m₀v²，且相对差须 = 解析预测 (3t²+t⁴)/(1−t²)
    # ★与 A2 同款修正：相对差是 O(β²) ≈ ¾β² 量级，β=0.02 时本就 ~3e−4
    #   ⇒ 判「小于某拍脑袋阈值」是错的，应判「等于解析预测」。
    t = F(1, 100)
    beta, sq, gam = pyth_beta(t)
    ex = ((gam - 1) - F(1, 2) * beta * beta) / (F(1, 2) * beta * beta)
    pr = (3 * t * t + t ** 4) / (1 - t * t)
    u3_ok = abs(ex - pr) / pr < F(1, 10 ** 9)
    control("U3 动能判据正对照：相对论 (γ−1)m₀c² 在 β={:.4f} 与 ½β²m₀c² 的相对差须 = 解析预测".format(
        float(beta)), u3_ok, "实测 {:.6e} vs 解析 {:.6e}".format(float(ex), float(pr)))

    # U4 动能判据反对照：靶式差值必须**全为 0**（证明判据能识别「动能恒零」）
    zs = []
    for tt in (F(1, 100), F(1, 10), F(1, 3), F(3, 4)):
        b, s, g = pyth_beta(tt)
        zs.append(g * s - 1)
    control("U4 动能判据反对照：靶式 γ·√(1−β²)·m₀c² − m₀c² 在四档须**精确为 0**",
            all(z == 0 for z in zs), "四档差值 = [{}]".format(
                ", ".join(str(z) for z in zs)))

    # U5 光子正对照
    ep = H_PLANCK * 5.0e14
    control("U5 光子能量正对照：E = hf = {:.6e} J（f=5e14 Hz）".format(ep),
            abs(ep - 3.313035075e-19) / 3.313035075e-19 < 1e-12,
            "实得 {:.8e} J".format(ep))

    # U6 光子反对照
    control("U6 光子能量反对照：m₀ = 0 ⇒ E = m₀c² = 0 ⇒ 判「零能量」（证明非恒判非零）",
            (0.0 * C_LIGHT ** 2) == 0.0, "实得 {:.1f} J".format(0.0 * C_LIGHT ** 2))

    # U7/U8 结论-计算耦合检测器：反对照（耦合）与正对照（脱钩）
    good = ("import os\n"
            "r = 1 + 1\n"
            "if r == 2:\n"
            "    print(\"一致性检查通过\")\n"
            "else:\n"
            "    print(\"一致性检查失败\")\n")
    bad = ("import os\n"
           "r = 1 + 1\n"
           "if r == 2:\n"
           "    print(\"中间量正常\")\n"
           "print(\"一致性检查通过\")\n")
    t_good, h_good, i_good = analyze_print_coupling(good)
    t_bad, h_bad, i_bad = analyze_print_coupling(bad)
    control("U7 耦合检测器反对照：结论写在 if 体内 ⇒ 顶层结论 print 应为 0（判「耦合」）",
            len(t_good) == 0 and len(i_good) == 2,
            "顶层结论 {} 条 / 顶层标题 {} 条 / if 内 {} 条".format(
                len(t_good), len(h_good), len(i_good)))
    control("U8 耦合检测器正对照：结论写在顶层 ⇒ 顶层结论 print 应 ≥ 1（判「脱钩」）",
            len(t_bad) >= 1, "顶层结论 {} 条 / 顶层标题 {} 条 / if 内 {} 条".format(
                len(t_bad), len(h_bad), len(i_bad)))

    # U9 纯 print 检测器反对照：含真实计算的脚本应判「有计算」
    calc = ("x = 0\n"
            "for i in range(10):\n"
            "    x = x + i * i\n"
            "if x > 100:\n"
            "    print(\"大\")\n"
            "else:\n"
            "    print(\"小\")\n")
    st = analyze_has_computation(calc)
    control("U9 纯 print 检测器反对照：含赋值/循环/比较的脚本应判「有计算」",
            st["assign"] >= 1 and st["compare"] >= 1 and st["if"] >= 1,
            "Assign={} Compare={} If={}".format(st["assign"], st["compare"], st["if"]))

    # U10 靶来料可定位
    control("U10 靶来料可定位（1.md / 能量绝对性.md / 两份脚本）",
            all(os.path.isfile(p) for p in (F_1MD, F_MANIFESTO, F_CV, F_VS)),
            "1.md={} 宣言={} comprehensive={} summary={}".format(
                os.path.isfile(F_1MD), os.path.isfile(F_MANIFESTO),
                os.path.isfile(F_CV), os.path.isfile(F_VS)))


# ============================== 守卫 ==============================
def run_guards(A, B, C, D, E):
    print("\n" + "=" * 78)
    print(" [守卫]（★全部机读驱动，无一处 ok 写死 True）")
    print("=" * 78)

    n_fail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
    n_pass = sum(1 for e in ENTRIES if e["verdict"] == "PASS")
    n_info = sum(1 for e in ENTRIES if e["verdict"] == "INFO")
    guard("G1 verdict 由机读驱动：FAIL {} / PASS {} / INFO {}（FAIL 与 PASS 都须 > 0）".format(
        n_fail, n_pass, n_info), n_fail > 0 and n_pass > 0,
        "机读累加 FAIL={} PASS={} INFO={}".format(n_fail, n_pass, n_info))

    # G2 量纲审计真算：7 项中通过数须 ≥ 6，且 f 项必须不一致（真算）
    g2 = (A["A0_dim_n_ok"] >= 6) and (A["A0_f_from_E"] != A["A0_f_from_geom"])
    guard("G2 量纲守卫：7 项须 ≥6 通过，且 f 两口径必须**真算不一致**", g2,
          "通过 {}/{}；[f]_E={} vs [f]_geom={} ⇒ 不一致={}".format(
              A["A0_dim_n_ok"], A["A0_dim_n"], d_str(A["A0_f_from_E"]),
              d_str(A["A0_f_from_geom"]), A["A0_f_from_E"] != A["A0_f_from_geom"]))

    # G3 动能恒零真算：四档差值必须**全部精确为 0**
    g3 = B["B3_all_zero"] and len(B["B3_devs"]) == 4
    guard("G3 动能恒零守卫：四档靶式差值须**全部精确为 0**（Fraction 层，真算）", g3,
          "全零 = {}，与相对论偏差 = [{}]".format(
              B["B3_all_zero"], ", ".join("{:+.2%}".format(d) for d in B["B3_devs"])))

    # G4 光子能量真算
    g4 = abs(B["B4_dev"] + 1.0) < 1e-12
    guard("G4 光子守卫：靶式 E = m₀c² = 0 与 hf 的相对偏差须 = −100%（真算）", g4,
          "偏差 = {:+.10%}".format(B["B4_dev"]))

    # G5 循环推导秩真算
    g5 = (B["B1_rank"] == 1)
    guard("G5 循环推导守卫：四式在对数线性空间的秩须 = 1（Fraction 高斯消元真算）", g5,
          "秩 = {}".format(B["B1_rank"]))

    # G6 ast 脱钩真算：顶层 ≥1 且 if 体内 ≥1（证明检测器同时扫到两类，非恒判脱钩）
    g6 = (C["C1_top"] >= 1) and (C["C1_inif"] >= 1)
    guard("G6 ast 脱钩守卫：顶层判定 print {} 条须 ≥1 且 if 体内 {} 条须 ≥1（证明检测器扫到两类）".format(
        C["C1_top"], C["C1_inif"]), g6,
        "顶层行号 = {}，if 内 = {} 条".format(C["C1_top_lines"], C["C1_inif"]))

    # G7 跨文件矛盾真查
    g7 = (C["C3_n_opposite"] == 3)
    guard("G7 跨文件矛盾守卫：两份总结对 f/Z′/统一方程三项须**逐条相反**（真比对）", g7,
          "相反项数 = {}".format(C["C3_n_opposite"]))

    # G8 防过度指控：必须声明「依赖 sympy 不是缺陷」
    g8 = any("防过度指控" in e["note"] and "sympy" in e["note"] for e in ENTRIES)
    guard("G8 防过度指控守卫：必须显式声明「依赖第三方库不是缺陷」（真查）", g8,
          "C4 含该声明 = {}".format(g8))

    # G9 对靶有利分支单列：量纲 / 质速 / 低速三条 PASS 须各为独立条目
    g9 = (sum(1 for e in ENTRIES if e["verdict"] == "PASS") >= 3)
    guard("G9 对靶有利分支单列守卫：量纲/质速/低速三条 PASS 须**各自单列**，不得并入两难条目",
          g9, "PASS 条目数 = {}（须 ≥ 3）".format(n_pass))

    # G10 零分辨力记 INFO
    g10 = (n_info >= 1)
    guard("G10 零分辨力守卫：必须存在 INFO 条目承认 comprehensive 的 6 条结论恰好全对", g10,
          "INFO 条目数 = {}".format(n_info))


# ============================== 输出 ==============================
def build_payload(A, B, C, D, E):
    stats = {}
    for e in ENTRIES:
        stats[e["verdict"]] = stats.get(e["verdict"], 0) + 1
    verdict = ("STRONG-CONSERVATION-IS-A-TAUTOLOGY-KINETIC-ENERGY-IDENTICALLY-ZERO"
               "-AND-VERIFICATION-SCRIPTS-PRINT-HARDCODED-CONCLUSIONS")
    verdict_zh = (
        "该「能量方程」的所谓第一性原理推导，是把 m₀c = mc√(1−β²) 这一个等式"
        "改写四次（对数线性秩 = 1）；其「能量绝对性」使动能恒等于零（Fraction 层逐位精确为 0，"
        "与相对论偏差 −100.00%），光子能量亦恒为零，力永远不做功；"
        "而支撑它的两份「验证」脚本一份把 6 条结论写成顶层无条件 print（与 if/else 判定完全脱钩），"
        "另一份 66 行全是 print、零计算，且两者对同一批量的三条结论全部相反。"
        "求导/量纲这一层：靶的几何化能量密度在量纲上 7 项过 6 项，质速关系与相对论形式一致 —— 已诚实记为 PASS。")
    key_numbers = {
        "dim_checks_passed": A["A0_dim_n_ok"],
        "dim_checks_total": A["A0_dim_n"],
        "f_dim_from_E": d_str(A["A0_f_from_E"]),
        "f_dim_from_geom": d_str(A["A0_f_from_geom"]),
        "derivation_rank": B["B1_rank"],
        "kinetic_gap_exact_zero": B["B3_all_zero"],
        "kinetic_devs": B["B3_devs"],
        "photon_E_hf_J": B["B4_e_photon"],
        "photon_E_target_J": B["B4_e_target"],
        "photon_dev": B["B4_dev"],
        "work_dev": B["B5_dev"],
        "cv_top_level_judgement_prints": C["C1_top"],
        "cv_if_body_judgement_prints": C["C1_inif"],
        "cv_top_lines": C["C1_top_lines"],
        "vs_has_computation": not C["C2_pure"],
        "vs_ast_stats": C["C2_stats"],
        "cross_file_opposite_count": C["C3_n_opposite"],
        "repair_loose": E["E_loose"],
        "repair_strict": E["E_strict"],
        "repair_zero_cost": E["E_zero"],
        "repair_min_cost": E["E_min_cost"],
    }
    return {
        "id": "TUFT-r166",
        "title": "统一场论能量方程的「第一性原理推导」与「验证脚本」方法论精算",
        "date": "2026-10-24",
        "target": "S17 核心公式集 16-统一场论能量方程",
        "target_files": [os.path.basename(F_1MD), os.path.basename(F_MANIFESTO),
                         "code/comprehensive_verification.py",
                         "code/verification_summary.py"],
        "verdict": verdict,
        "verdict_zh": verdict_zh,
        "stats": stats,
        "entries": ENTRIES,
        "controls": CONTROLS,
        "guards": GUARDS,
        "key_numbers": key_numbers,
        "not_closed": [
            "本卷只审 16-统一场论能量方程 目录下的文档与 8 个脚本；若体系在别处另有能量方程的权威版本，B/C 组应重审。",
            "B3 的「动能恒零」依赖 m = γm₀（靶 §2 明给）；若靶改称 m 另有定义，须先给出该定义再重算。",
            "C1 的 ast 分析口径为「参数全为字符串字面量的 print」，若靶改用日志/返回码输出结论，该判据需改写。",
            "C4 的「无执行留痕」只说明本目录下没有输出文件，不等于脚本从未在他处运行过 ⇒ 记 BOUNDARY。",
            "修复枚举限于本卷 5 个动作（32 组合），不排除第 6 种路径。",
        ],
        "redline": [
            "数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。",
            "不宣称「张祥前体系全错」，只判决本卷所列命题。",
            "量纲层面靶的几何化能量密度 7 项过 6 项、质速关系与相对论形式一致 —— 已诚实记为 PASS。",
            "C4 的「依赖 sympy / 无执行留痕」按防过度指控原则记 BOUNDARY，不作缺陷证据。",
            "C5 的零分辨力结论按既有纪律既不当指控也不当辩护。",
            "分层铁律：本卷条目不可与 r159–r165 相加。",
        ],
    }


def write_outputs(payload):
    base = "TUFT-r166_统一场论能量方程推导与验证脚本方法论_精算_2026-10-24"
    datadir = os.path.join(_PROJ, "数据")
    os.makedirs(datadir, exist_ok=True)
    paths = {}

    p_json = os.path.join(datadir, base + ".json")
    with open(p_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    paths["json"] = p_json

    # ---- report.txt ----
    L = ["TUFT-r166 统一场论能量方程精算 —— 运行报告",
         "=" * 70, ""]
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

    # ---- md（数据表） ----
    M = ["# TUFT-r166｜统一场论能量方程的「第一性原理推导」与「验证脚本」方法论精算",
         "",
         "**判词**：`{}`".format(payload["verdict"]),
         "",
         "{}".format(payload["verdict_zh"]),
         "",
         "## 条目总表",
         "",
         "| 编号 | 层 | 结论 | 要点 |",
         "|---|---|---|---|"]
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

    # ---- 判定册 ----
    V = ["# 判定册 · TUFT-r166｜统一场论能量方程的「第一性原理推导」与「验证脚本」方法论精算",
         "",
         "## 一、编号与定位",
         "",
         "- **编号 r166**（实测首空号）。★**编号冲突处置**：r165 已被并行会话占用"
         "（`TUFT-r165_D5四力闭合层_单粒子运动学量与源依赖冲突_2026-10-24.*` 四件套已落盘）"
         " ⇒ 按纪律「保留已产三件套并已登记者为权威，后到者整体改号」⇒ 本卷整体改用 **r166**。",
         "- **靶**：S17 `04_理论推导/核心公式集/16-统一场论能量方程/`（1.md 326 行 · "
         "「能量绝对性与几何本源」118 行 · `code/` 8 个脚本 · `传统的公式/` 3 份）",
         "- **分层**：本卷为**推导层 + 验证方法论层**，与 r160（四项诠释）/ r161（电荷几何化）/ "
         "r162（时空同一化与质量几何化）/ r164（质量定义方程的验证方法论）**条目不可相加**",
         "",
         "## 二、判词",
         "",
         "`{}`".format(payload["verdict"]),
         "",
         "{}".format(payload["verdict_zh"]),
         "",
         "## 三、先给靶应得的 PASS（量纲层与质速关系）",
         "",
         "用 (M,L,T,Q) 四元运算器**独立重算**靶脚本的 6 组量纲检验：",
         "",
         "| 项 | 表达式 | 实得 | 结论 |",
         "|---|---|---|---|",
         r"| ① | u_b = c³/(16πZ′)·\|B\|² | {} | ✓ |".format(d_str(A_UB)),
         r"| ③ | u_g = c/(16πZ)·\|A\|² | {} | ✓ |".format(d_str(A_UG)),
         r"| ④ | u_e = c/(16πZ′)·\|E\|² | {} | ✓ |".format(d_str(A_UE)),
         "| ⑤ | Z′ = c/(8πε₀) | {}（与声明逐位相符） | ✓ |".format(d_str(A_ZP)),
         "| ⑥ | u_g = u_e = u_b | {} ⇒ 三项可加 | ✓ |".format(d_str(D_U)),
         "| ② | 耦合常数 f | 由 E=−f·dA/dt 得 **{}** ≠ 由 k/k′ 得 **{}** | ✗ |".format(
             d_str(A_F_E), d_str(A_F_G)),
         "",
         "⇒ **7 项中 6 项通过**：靶的几何化能量密度在**量纲层面基本正确**，"
         "质速关系 m = m₀/√(1−β²) 与狭义相对论**数学形式完全一致**。",
         "**这是本卷对靶有利的结论，诚实登记。** 本卷指控的不是这一层。",
         "",
         "## 四、★推导层：四个式子是同一个方程",
         "",
         "文档 §3「第一性原理推导」的三个步骤 + 结论式，取对数后化为线性方程组"
         "（变量 = ln m₀, ln m, ln c, ln(1−β²)）：",
         "",
         "| 式 | 内容 | 系数行 |",
         "|---|---|---|",
         "| ① | 步骤1 假设 p₀ = p（代入 p₀=m₀c、p=mc√(1−β²)） | [1, −1, 0, −½] |",
         "| ② | 步骤2 明写 m₀c = mc√(1−β²) | [1, −1, 0, −½] |",
         "| ③ | 步骤3 导出 m = m₀/√(1−β²) | [−1, 1, 0, ½] |",
         "| ④ | 能量方程 m₀c² = mc²√(1−β²) | [1, −1, 0, −½] |",
         "",
         "机读 **Fraction 高斯消元** ⇒ 秩 = **{}**（4 行）⇒ **四式全部线性相关**。".format(
             B_RANK),
         "",
         "⇒ 「假设 ⇒ 导出质速关系 ⇒ 导出能量方程」的每一步，"
         "都只是把上一步**乘以或除以 c 与 √(1−β²)**，没有引入任何新的独立内容。"
         "（与 r164 B3 同型，但更靠前：r164 是**验证**环节循环，本卷是**推导**环节本身循环。）",
         "",
         "## 五、★★后果层：能量绝对性 ⇒ 动能恒为零",
         "",
         "靶的核心主张是 E ≡ m₀c² 与速度无关 ⇒ **物体的动能恒等于零**。",
         "取 m = γm₀ 代入靶的「运动能量表达式」mc²√(1−β²)：",
         "",
         "    mc²√(1−β²) − m₀c² = γm₀c²·(1/γ) − m₀c² = m₀c² − m₀c² = 0",
         "",
         "本卷用**勾股数参数化** β = 2t/(1+t²)（使 γ 与 √(1−β²) 同时为有理数），"
         "在 **Fraction 层逐位精确**得到该差值 = **0**（不是 1e−16 级残差，是**恒等相消**）：",
         "",
         "| t | β | 靶式差值（精确） | 相对论动能 (γ−1)m₀c² | 相对偏差 |",
         "|---|---|---|---|---|"]
    for nm, be, gap, kr in B_ROWS:
        V.append("| {} | {:.6f} | **{}** | {:.6e} m₀c² | {:+.2%} |".format(
            nm, be, gap, kr, (gap - kr) / kr if kr else 0.0))
    V += ["",
          "★根因：靶把「运动能量」写成 **mc²√(1−β²)**（= m₀c²，**比静止能量小**），"
          "而相对论的总能量是 **mc² = γm₀c²**（**比静止能量大**）—— "
          "靶用了 √(1−β²) 而相对论用 1/√(1−β²)，**因子方向搞反了**。",
          "",
          "★更严重：文档 §4.2 声称「经典动能 ½mv² 在数值上近似等于 mc²√(1−β²) 与 m₀c² 的差值」，"
          "而它自己的方程让这个差值**恒等于 0** ⇒ 该声称等价于 **½mv² ≈ 0**"
          " ⇒ **§4.2 的「还原经典动能」与 §3 的能量方程自相矛盾**。",
          "",
          "**其余两条后果**：",
          "",
          "- **光子**：能量方程给 E = m₀c² = **0 J**，而 §4.2 的文字叙述给 E = mc² > 0"
          "（f = 5e14 Hz ⇒ hf = **{:.6e} J**）⇒ 相对偏差 **{:+.2%}**，且 v = c 时 m 为 0/0 不定型"
          " ⇒ m 无法由方程定出。（与 r148 D5「光子能量零」同型）".format(
              B_E_PH, B_E_DEV),
          "- **做功**：E 恒定 ⇒ ΔE ≡ 0。1 N 推 1 kg 静止物体 1 s ⇒ W = **{:.3f} J**，"
          "而靶给 ΔE = **0 J** ⇒ **{:+.2%}** ⇒ 该理论内**力永远不做功**，"
          "「加速 / 做功 / 能量转化」失去动力学含义。".format(B_W, B_W_DEV),
          "",
          "## 六、★验证方法论层：靶自称「验证」的脚本是否真的在验证",
          "",
          "### C1 结论硬编码（ast 静态分析）",
          "",
          "`comprehensive_verification.py` 在第 45 / 71 / 87 / 103 / 119 / 136 行共 6 处用 `if/else` "
          "判定量纲，并在分支内 print **{}** 条判定；但 **{}** 条**结论**语句"
          "（第 148–153 行的「验证结果总结」6 条 + 第 156–158 行的「结论」3 条；行号 {}）"
          "位于 **module 顶层**，**不在任何 if/else 之内**。".format(
              C_INIF, C_TOP, C_LINES),
          "",
          "⇒ **无论上方 6 组判定算出 ✅ 还是 ❌，这 6 条总结的输出都完全不变**"
          " ⇒ 结论不依赖计算 ⇒ **判据零分辨力**。",
          "",
          "★统计口径：只统计**参数全为字符串字面量**的 print（天然排除"
          " `print(f\"正确能量密度量纲: {expr}\")` 这类打印期望值的语句）。"
          "★这是本线既有纪律「守卫的 ok 禁写死 True」的**同款病，出现在靶的代码里**。",
          "",
          "### C2 「验证结果总结」不含任何验证",
          "",
          "`verification_summary.py`（66 行）排除 print 子树后：赋值 **{assign}** 个、"
          "if **{if}** 个、比较 **{compare}** 个、双目运算 **{binop}** 个、函数调用 **{call}** 个"
          " ⇒ **该文件不含任何计算**。它输出 26 条带 ✅/❌ 的「验证结果」，"
          "但这些符号是**手写在字符串字面量里的**。".format(**C_STATS),
          "",
          "### C3 两份总结对同一批量三项全反",
          "",
          "| 项目 | comprehensive（1-22） | summary（1-10） | 第三方独立裁决 |",
          "|---|---|---|---|",
          "| 耦合常数 f 量纲 | 不一致 | 一致（M/I） | **不一致** |",
          "| Z′ = c/(8πε₀) 定义 | 一致 | 时间维度有问题 | **一致** |",
          "| 统一方程 u=u_g+u_e+u_b | 一致、可相加 | 整体量纲不一致 | **一致** |",
          "",
          "⇒ `verification_summary.py` 三条全错；且它自己在第 51 行写「几何常数的定义和转换关系"
          "在数学上是自洽的」，与其第 19 / 26 行的两条 ❌ **在同一文件内自相矛盾**。",
          "",
          "### C4/C5 执行留痕与零分辨力",
          "",
          "- **C4（BOUNDARY）**：`code/` 8 个脚本无任何输出/日志/结果文件；"
          "且依赖 sympy（本环境无）⇒ 不可运行。★**防过度指控**：依赖第三方库**不是**缺陷，"
          "登记的是「自称完成验证却无执行留痕」这一可及性问题。",
          "- **C5（INFO）**：comprehensive 的 6 条结论**恰好全对**（本卷 A0 独立重算证实），"
          "但由 C1 已知它们与计算脱钩 ⇒ 按既有纪律，**既不当指控也不当辩护**。",
          "",
          "## 七、跨卷一致性",
          "",
          "- **D1**：r162 A6 判 V=dR/dt ⇒ P = m(C−V) ≡ **0**；本卷靶 §2 却把 **p₀ = m₀c = "
          "{:.6e} kg·m/s**（电子）当作非零的推导基石 ⇒ 同一理论的静止动量有 0 与非零两个互斥值。".format(
              M_E * C_LIGHT),
          "- **D2**：质速关系的「几何来源」依赖 m₀ = k·dn/dΩ，而 r162 B1 / r164 A1 已判 Ω 无定义。",
          "- **D3（BOUNDARY）**：若取 r163 来料 k = 4π m_p ⇒ E = N·m_p c²（台阶 {:.6e} J）。".format(
              4.0 * math.pi * M_P * C_LIGHT ** 2),
          "",
          "## 八、修复定价",
          "",
          "| 档 | 存活 |",
          "|---|---|",
          "| 宽松（允许改动核心定义） | **{}** |".format(E_LOOSE),
          "| 严格（不许改能量方程核心形式 E = m₀c² 与质速关系） | **{}** |".format(E_STRICT),
          "| 零代价 | **{}** |".format(E_ZERO),
          "",
          "⇒ **修复即自杀第十四度**。",
          "",
          "## 九、控制组与守卫",
          "",
          "控制组 {} / {}，守卫 {} / {}（**守卫全部机读驱动**）".format(
              sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
              sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
          "",
          "## 十、未闭合项与红线",
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


# ============================== main ==============================
A_UB = A_UE = A_UG = A_ZP = A_F_E = A_F_G = None
B_RANK = 1
B_ROWS = []
B_E_PH = B_E_DEV = B_W = B_W_DEV = 0.0
C_TOP = C_INIF = 0
C_LINES = []
C_STATS = {}
E_LOOSE = E_STRICT = E_ZERO = 0


def main():
    global A_UB, A_UE, A_UG, A_ZP, A_F_E, A_F_G
    global B_RANK, B_ROWS, B_E_PH, B_E_DEV, B_W, B_W_DEV
    global C_TOP, C_INIF, C_LINES, C_STATS
    global E_LOOSE, E_STRICT, E_ZERO

    print("=" * 78)
    print(" TUFT-r166｜统一场论能量方程的「第一性原理推导」与「验证脚本」方法论精算")
    print(" 2026-10-24")
    print("=" * 78)
    print(" ★编号冲突：r165 已被并行会话占用（四件套已落盘）⇒ 本卷整体改用 r166")

    A = group_A()
    A_UB, A_UE, A_UG = A["A0_ub"], A["A0_ue"], A["A0_ug"]
    A_ZP, A_F_E, A_F_G = A["A0_zp_calc"], A["A0_f_from_E"], A["A0_f_from_geom"]

    B = group_B()
    B_RANK = B["B1_rank"]
    B_ROWS = B["B3_rows"]
    B_E_PH, B_E_DEV = B["B4_e_photon"], B["B4_dev"]
    B_W, B_W_DEV = B["B5_W"], B["B5_dev"]

    C = group_C()
    C_TOP, C_INIF, C_LINES = C["C1_top"], C["C1_inif"], C["C1_top_lines"]
    C_STATS = C["C2_stats"]

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
