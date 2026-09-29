#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论核心公式 · 公式层实证突破
==================================
对象：openuft/01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/
      圆周运动正电荷产生的引力场方程/
        - V5/引力场可视化.py                      （被审代码，标注单位 m/s²）
        - circle_motion_gravity_field_derivation.md（推导 md，§4.1 量纲“一致”）
        - verify_circular_motion_gravity_field.py  （作者自验证，已发现量纲矛盾）

背景：2026-09-29 对该可视化工程做了「工程层审计」（结构/符号/冗余/图形≠方程），
      评级 C / L0–L1，发现三项硬问题。本轮突破到「公式层实证」：独立复算核心公式，
      机器验证其量纲/数值自洽性，并定位文档矛盾。

聚焦公式（张祥前统一场论核心预言「运动电荷产生引力场」）：
    A_vec(r,t) = - q / (4π ε₀ c² r) · [ â_q − (r̂·â_q) r̂ ]          （代码 V5 / 推导 md §2.3）
    代码 ylabel 标注单位 "m/s²"（引力场/加速度）。

方法：自写四维量纲系统 {M,L,T,I}（算法联盟标准口径），纯标准库、机器可复算；
      数值量级用 math 标准库；sympy 可选交叉验证（失败则跳过，不阻塞）。

输出：机器判定 PASS / FAIL / BOUNDARY / INFO + 结构化数据（与工程审计同口径）。
"""
import json, math, os, sys, datetime, traceback

# Windows GBK 控制台兜底：编码失败用 replace，绝不因打印特殊符号崩溃
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ----------------------------------------------------------------------------
# 量纲系统（基：M 质量, L 长度, T 时间, I 电流）
# ----------------------------------------------------------------------------
BASE = ["M", "L", "T", "I"]

def dim(**kw):
    return {b: kw.get(b, 0) for b in BASE}

ZERO = dim()

def _op(a, b, sign):
    return {x: a[x] + sign * b[x] for x in BASE}

def mul(a, b):
    return _op(a, b, 1)

def div(a, b):
    return _op(a, b, -1)

def power(a, n):
    return {x: a[x] * n for x in BASE}

def eq(a, b):
    return all(a[x] == b[x] for x in BASE)

def pretty(d):
    if eq(d, ZERO):
        return "1 (无量纲)"
    return "·".join(f"{b}^{d[b]}" if d[b] != 1 else b for b in BASE if d[b])

# 物理量量纲
Q    = dim(I=1, T=1)               # 电荷 C = A·s
EPS  = dim(M=-1, L=-3, T=4, I=2)  # ε₀: C²s²/(kg·m³) = M⁻¹L⁻³T⁴I²
C    = dim(L=1, T=-1)             # 光速 c
A    = dim(L=1, T=-2)             # 加速度 m/s²
R    = dim(L=1)                   # 距离 r
MASS = dim(M=1)                   # 质量 kg
Q2   = power(Q, 2)                # 电荷平方 q²

ACCEL   = A                                   # 加速度标准量纲
EFIELD  = dim(M=1, L=1, T=-3, I=-1)           # 电场强度 N/C = kg·m/(C·s²)
NEWTON  = dim(M=1, L=1, T=-2)                 # 力 N = kg·m/s²

results = []          # (verdict, code, title, detail)
def emit(verdict, code, title, detail=""):
    results.append((verdict, code, title, detail))
    tag = {"PASS": "[PASS]", "FAIL": "[FAIL]", "BOUNDARY": "[BND]", "INFO": "[INFO]"}.get(verdict, "[?]")
    print(f"[{tag}] {code}  {title}")
    if detail:
        for line in detail.strip().splitlines():
            print("        " + line)

# ----------------------------------------------------------------------------
# 自检：量纲系统正确性（库仑定律 F = q²/(4π ε₀ r²) 必须得力的量纲）
# ----------------------------------------------------------------------------
def selfcheck():
    F_dim = div(Q2, mul(EPS, power(R, 2)))
    ok = eq(F_dim, NEWTON)
    emit("PASS" if ok else "FAIL", "SELF-0",
         "量纲系统自检：库仑定律 F=q²/(4πε₀r²) 量纲 = 力",
         f"F_dim = {pretty(F_dim)}  (期望 {pretty(NEWTON)})\n"
         f"ε₀ 量纲定义正确，量纲代数可信。")

# ----------------------------------------------------------------------------
# P1：代码公式的真实量纲（机器实证）
# ----------------------------------------------------------------------------
def p1_dim_of_formula():
    factor = div(Q, mul(mul(EPS, power(C, 2)), R))   # q/(ε₀ c² r)
    A_formula = mul(factor, A)                         # × a_perp
    is_accel = eq(A_formula, ACCEL)
    is_efield = eq(A_formula, EFIELD)
    emit("FAIL" if not is_accel else "PASS", "P1-DIM",
         "公式 A = -q/(4π ε₀ c² r)·a_perp 的真实量纲",
         f"factor = q/(ε₀ c² r)  →  {pretty(factor)}\n"
         f"A_formula = factor·a   →  {pretty(A_formula)}\n"
         f"加速度标准量纲          →  {pretty(ACCEL)}\n"
         f"电场强度标准量纲        →  {pretty(EFIELD)}\n"
         f"结论：量纲 = 电场强度(N/C)，并非加速度(m/s²)；标注 m/s² 是量纲错配。")

# ----------------------------------------------------------------------------
# P2：根因 + 最小修正（要成为加速度须引入电荷-质量等价因子 q/m）
# ----------------------------------------------------------------------------
def p2_minimal_fix():
    factor = div(Q, mul(mul(EPS, power(C, 2)), R))
    A_formula = mul(factor, A)
    # 修正因子 q/m：A_corr = (q/m)·A_formula = -q²/(4π ε₀ c² r m)·a
    corr = mul(A_formula, div(Q, MASS))
    emit("INFO", "P2-FIX",
         "最小修正：乘 (q/m) 因子后量纲归位为加速度",
         f"A_corr = (q/m)·A_formula  →  {pretty(corr)}\n"
         f"即 A_corr = - q²/(4π ε₀ c² r m)·a_perp\n"
         f"物理含义：运动电荷先产生『辐射电场』(N/C)，再乘 (q/m) 才转成加速度(m/s²)。\n"
         f"原公式漏掉 (q/m) 因子 → 量纲落在电磁侧而非引力侧。")

# ----------------------------------------------------------------------------
# P3：数值量级（电子圆周运动，对照真实牛顿引力场）
# ----------------------------------------------------------------------------
def p3_numeric():
    q = 1.602176634e-19      # C
    m = 9.1093837015e-31     # kg
    eps0 = 8.8541878128e-12  # F/m
    c = 2.99792458e8         # m/s
    Rr = 1.0                 # 轨道半径 m
    omega = 1.0e6            # rad/s
    a = omega * omega * Rr   # 向心加速度 m/s²
    factor = q / (4.0 * math.pi * eps0 * c * c * Rr)
    A_code = factor * a      # 实为单位 N/C，代码误作 m/s²
    # 真实牛顿引力场：电子在 1m 处
    G = 6.67430e-11
    g_newton = G * m / (Rr * Rr)
    # 同一电子的静电场（库仑），对照辐射电场量级
    E_static = (1.0 / (4.0 * math.pi * eps0)) * q / (Rr * Rr)
    emit("FAIL", "P3-MAG",
         "数值量级：电子圆周运动的『引力场』 vs 真实牛顿引力场",
         f"向心加速度 a        = {a:.3e} m/s²\n"
         f"代码公式输出 A_code = {A_code:.3e}  （单位实为 N/C，却标 m/s²）\n"
         f"真实牛顿引力场 g     = {g_newton:.3e} m/s²  （电子@1m）\n"
         f"若强行把 A_code 当 m/s²：比真实引力场大 {A_code/g_newton:.2e} 倍\n"
         f"同一电荷静电场 E     = {E_static:.3e} N/C  → 『引力场』比静电场小 "
         f"{E_static/A_code:.2e} 倍，且形式正是辐射电场\n"
         f"结论：代码值本质是辐射电场(电磁)，与真实引力场差 ~27 个数量级且量纲错位。")

# ----------------------------------------------------------------------------
# P4：文档矛盾（推导 md 的『一致』声称 vs 机器结果 + 作者自验证）
# ----------------------------------------------------------------------------
def p4_doc_contradiction():
    factor = div(Q, mul(mul(EPS, power(C, 2)), R))
    A_formula = mul(factor, A)
    # 推导 md §4.1 声称的结果
    claimed = ACCEL  # [L T⁻²]
    md_wrong = not eq(A_formula, claimed)
    # 作者自验证脚本（verify_...py L52-58）已算出 (kg·m)/(A·s)·(m/s²) = N/C
    emit("FAIL" if md_wrong else "PASS", "P4-DOC",
         "文档矛盾：推导 md §4.1 声称量纲一致，实为错误代数",
         f"机器结果 A_formula = {pretty(A_formula)} = N/C\n"
         f"推导 md §4.1 声称  = {pretty(claimed)} = m/s²\n"
         f"作者自验证脚本 L52-58 已正确算出 = (kg·m)/(A·s)·(m/s²) = N/C，并标注『✗ 量纲可能不一致』\n"
         f"两文件互相矛盾：推导 md 用错误量纲代数把矛盾粉饰成『一致』。")

# ----------------------------------------------------------------------------
# 可选：sympy 交叉验证
# ----------------------------------------------------------------------------
def sympy_crosscheck():
    try:
        from sympy.physics.units import (coulomb, epsilon0, speed_of_light,
                                         meter, acceleration, Dimension)
        from sympy.physics.units.dimensions import dimsys_default
        expr = coulomb / (epsilon0 * speed_of_light**2 * meter) * acceleration
        d = dimsys_default.get_dimensional_dependencies(expr.dimension)
        # 映射到 M,L,T,I
        sym = dim(M=d.get('mass', 0), L=d.get('length', 0),
                  T=d.get('time', 0), I=d.get('current', 0))
        ok = eq(sym, EFIELD)
        emit("INFO", "X-SYMPY",
             "sympy.physics.units 交叉验证（公式量纲）",
             f"sympy 量纲 = {pretty(sym)}\n"
             f"与自写系统一致={ok}（均为电场强度 N/C）。")
    except Exception as e:
        emit("INFO", "X-SYMPY", "sympy 交叉验证跳过",
             f"（未安装 sympy 或行为差异，不影响结论）：{type(e).__name__}: {e}")

# ----------------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------------
def main():
    print("=" * 72)
    print("统一场论核心公式 · 公式层实证突破")
    print("对象：S17/04_理论推导/核心公式集/圆周运动正电荷产生的引力场方程")
    print("=" * 72)
    selfcheck()
    p1_dim_of_formula()
    p2_minimal_fix()
    p3_numeric()
    p4_doc_contradiction()
    sympy_crosscheck()

    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for v, _, _, _ in results:
        counts[v] += 1
    print("-" * 72)
    print(f"PASS = {counts['PASS']} | FAIL = {counts['FAIL']} | "
          f"BOUNDARY = {counts['BOUNDARY']} | INFO = {counts['INFO']}")
    print(f"评级：C / L1（公式层实证，抓出量纲错配 + 文档粉饰；属诚实边界）")

    # 结构化数据落盘
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(root, "数据")
    os.makedirs(data_dir, exist_ok=True)
    payload = {
        "title": "统一场论核心公式 · 公式层实证突破",
        "object": "S17/.../圆周运动正电荷产生的引力场方程",
        "focus_formula": "A = -q/(4π ε₀ c² r) · a_perp  （代码标注 m/s²）",
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "counts": counts,
        "verdicts": [
            {"verdict": v, "code": c, "title": t, "detail": d}
            for (v, c, t, d) in results
        ],
        "key_findings": [
            "代码公式真实量纲 = 电场强度 N/C，并非加速度 m/s²（量纲错配）",
            "根因：漏掉电荷-质量等价因子 (q/m)；修正后 A_corr=-q²/(4πε₀c²rm)·a 量纲归位",
            "电子圆周运动：『引力场』数值本质为辐射电场，比真实牛顿引力场差 ~27 个数量级",
            "文档矛盾：推导 md §4.1 用错误量纲代数把矛盾粉饰成『一致』，作者自验证脚本已发现",
        ],
    }
    with open(os.path.join(data_dir, "统一场论核心公式_公式层实证突破.json"),
              "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    # 同时落一份 Markdown 便于阅读
    md = [f"# 统一场论核心公式 · 公式层实证突破", "",
          f"- 对象：`S17/04_理论推导/核心公式集/圆周运动正电荷产生的引力场方程`",
          f"- 聚焦公式：`A = -q/(4π ε₀ c² r) · a_perp`（代码标注 m/s²）",
          f"- 时间：{payload['timestamp']}`", "",
          f"## 计数  PASS={counts['PASS']} FAIL={counts['FAIL']} "
          f"BOUNDARY={counts['BOUNDARY']} INFO={counts['INFO']}", "",
          "## 判定", ""]
    for v, c, t, d in results:
        md.append(f"### [{v}] {c} {t}")
        if d:
            md.append("```")
            md.append(d.strip())
            md.append("```")
        md.append("")
    md.append("## 关键发现")
    for k in payload["key_findings"]:
        md.append(f"- {k}")
    with open(os.path.join(data_dir, "统一场论核心公式_公式层实证突破.md"),
              "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"\n数据产物已写入：{data_dir}")
    print("  - 统一场论核心公式_公式层实证突破.json")
    print("  - 统一场论核心公式_公式层实证突破.md")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
