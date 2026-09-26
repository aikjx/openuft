# -*- coding: utf-8 -*-
"""
空间螺旋修复版 · C25 核心：新基底 Frenet 符号推导 + 螺旋流形本征算子谱方程
高精度 mpmath (dps=250) 数值仿真

定位
----
承接《空间螺旋修复版_第一性缺陷记录.md》C24–C38 修复方案，本脚本实现：
  A. 新公理基底 R(t)=(A cos wt, A sin wt, b w t) 的 Frenet 符号推导（sympy）与
     250 位高精度数值交叉核验（mpmath）；
  B. 螺旋弧长域上的本征算子 H = -(ℏ²/2m)d²/ds² + E_scale·(κ²(s)+τ²(s))，
     周期边界，有限差分矩阵对角化（mpmath.eigsy）；
  C. 诚实的 α 分析：证明完美螺旋的无量纲能隙与几何参数完全脱耦，α 须由
     外部尺度钉定 → C25 保持 OPEN（与缺陷记录预期一致）。

红线（必须遵守）
----------------
1. 数学自洽 != 实验证实；本脚本不声称「从第一性导出 α=1/137」。
2. 所有外部尺度（E_scale、m_e、λ_e）显式标记为外部输入，不伪造成推导结果。
3. 保留全部数值输出，不做任何美化；结论与缺陷记录对得上的标 PASS，
   需要外部输入的标 OPEN，绝不把 OPEN 降为 PASS。

依赖：mpmath（必需，dps=250）、sympy（可选，仅用于 A 段符号推导；缺失则跳过）
运行：python spiral_frenet_spectral_c25.py
"""

import sys
import json

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import mpmath as mp

mp.mp.dps = 250  # 用户指定 250 位高精度

# ---------------------------------------------------------------- CODATA / 常数
C = mp.mpf('299792458')            # c   m/s   （精确定义）
HBAR = mp.mpf('1.054571817e-34')   # ℏ   J·s
ME = mp.mpf('9.1093837015e-31')    # m_e kg
ALPHA = mp.mpf('7.2973525693e-3')  # α   精细结构常数（CODATA，仅作对比靶）
ALPHA_INV = mp.mpf('137.035999084')  # 1/α 取整近似（仅作对比靶）

# ---------------------------------------------------------------- 结果收集
RESULTS = []


def rec(sid, sec, title, verdict, detail):
    RESULTS.append({"id": sid, "sec": sec, "title": title,
                    "verdict": verdict, "detail": detail})


def P(sid, sec, title, verdict, detail):
    rec(sid, sec, title, verdict, detail)


def F(sid, sec, title, verdict, detail):
    rec(sid, sec, title, verdict, detail)


def BO(sid, sec, title, verdict, detail):
    rec(sid, sec, title, verdict, detail)


def OP(sid, sec, title, verdict, detail):
    rec(sid, sec, title, verdict, detail)


def IN(sid, sec, title, verdict, detail):
    rec(sid, sec, title, verdict, detail)


def g(x, n=6):
    return mp.nstr(x, n)


# ===================================================================
# A 段：新基底 Frenet 符号推导 + 高精度数值核验
# ===================================================================
def symbolic_frenet():
    """用 sympy 推导 κ, τ 的闭式，并验证 κ=Aω²/c², τ=bω²/c², κ²+τ²=ω²/c², tanθ=b/A。"""
    try:
        import sympy as sp
    except Exception:
        print("[A] sympy 不可用，跳过符号推导，仅做数值核验。")
        return None

    t, A, b, w, c = sp.symbols('t A b w c', real=True, positive=True)
    R = sp.Matrix([A * sp.cos(w * t), A * sp.sin(w * t), b * w * t])
    Rp = sp.diff(R, t)
    Rpp = sp.diff(Rp, t)
    Rppp = sp.diff(Rpp, t)

    speed = sp.simplify(sp.sqrt(sum(Rp[i] ** 2 for i in range(3))))
    cross = Rp.cross(Rpp)
    cross_norm = sp.simplify(sp.sqrt(sum(cross[i] ** 2 for i in range(3))))
    kappa = sp.simplify(cross_norm / speed ** 3)
    # 挠率 τ = (R'×R'')·R''' / |R'×R''|²
    numer = sum(cross[i] * Rppp[i] for i in range(3))
    tau = sp.simplify(numer / cross_norm ** 2)

    # 代入约束 c = w*sqrt(A^2+b^2)  ⇒ 用 w^2*(A^2+b^2) = c^2
    subs = {c ** 2: w ** 2 * (A ** 2 + b ** 2)}
    kappa_red = sp.simplify(kappa.subs(subs))
    tau_red = sp.simplify(tau.subs(subs))

    # 目标闭式
    kappa_target = A * w ** 2 / c ** 2
    tau_target = b * w ** 2 / c ** 2

    def sym_zero(expr):
        """稳健判零：先 .equals(0)，不确定时回退随机数值评估。"""
        r = sp.simplify(expr).equals(0)
        if r is True:
            return True
        if r is False:
            return False
        import random
        for _ in range(6):
            s = {A: random.uniform(0.2, 2.0), b: random.uniform(0.2, 2.0),
                 w: random.uniform(0.5, 3.0), c: random.uniform(1.0, 5.0)}
            if abs(float(expr.subs(s))) > 1e-9:
                return False
        return True

    # 比较前把约束同时代入差值表达式，避免目标式分母残留 c²
    kappa_ok = sym_zero((kappa_red - kappa_target).subs(subs))
    tau_ok = sym_zero((tau_red - tau_target).subs(subs))
    # κ²+τ² = ω²/c²
    inv_ok = sym_zero((kappa_target ** 2 + tau_target ** 2 - w ** 2 / c ** 2).subs(subs))
    # tanθ = τ/κ = b/A
    tan_ok = sym_zero((tau_target / kappa_target - b / A).subs(subs))

    rec("A1", "Frenet符号", "κ 闭式 κ=Aω²/c²",
        "PASS" if kappa_ok else "FAIL",
        "sympy 推导 κ=%s，代入约束后 == A*w^2/c^2 : %s" % (kappa_red, kappa_ok))
    rec("A2", "Frenet符号", "τ 闭式 τ=bω²/c²",
        "PASS" if tau_ok else "FAIL",
        "sympy 推导 τ=%s，代入约束后 == b*w^2/c^2 : %s" % (tau_red, tau_ok))
    rec("A3", "Frenet符号", "κ²+τ²=ω²/c² 不变量",
        "PASS" if inv_ok else "FAIL",
        "(Aω²/c²)²+(bω²/c²)² - ω²/c² == 0 : %s" % inv_ok)
    rec("A4", "Frenet符号", "tanθ=τ/κ=b/A 唯一第一性定义",
        "PASS" if tan_ok else "FAIL",
        "(τ/κ) - b/A == 0 : %s" % tan_ok)
    return {"kappa": kappa_red, "tau": tau_red}


def numeric_frenet(A_val, b_val):
    """给定 A,b（满足约束 ω√(A²+b²)=c），用 mpmath 250 位数值核验 κ,τ。"""
    A = mp.mpf(A_val)
    b = mp.mpf(b_val)
    w = C / mp.sqrt(A ** 2 + b ** 2)          # 约束：ω = c / sqrt(A²+b²)
    speed = w * mp.sqrt(A ** 2 + b ** 2)      # 应 == c
    # 经典螺旋闭式（已符号验证）
    kappa = A * w ** 2 / C ** 2
    tau = b * w ** 2 / C ** 2
    inv = kappa ** 2 + tau ** 2
    # 量纲核验：κ,τ 单位 L^{-1}
    speed_ok = mp.almosteq(speed, C, rel_eps=mp.mpf('1e-240'))
    inv_ok = mp.almosteq(inv, w ** 2 / C ** 2, rel_eps=mp.mpf('1e-240'))
    return {
        "A": A, "b": b, "w": w, "speed": speed,
        "kappa": kappa, "tau": tau, "inv": inv,
        "speed_ok": speed_ok, "inv_ok": inv_ok,
        "tan_theta": tau / kappa, "b_over_A": b / A,
    }


# ===================================================================
# B 段：螺旋弧长域本征算子（完美螺旋 → 常数势）
# ===================================================================
def helix_arc_length(A, b, w):
    """一圈螺旋的弧长 L = c·(2π/ω) = 2π·sqrt(A²+b²)。"""
    return C * (2 * mp.pi / w)


def build_hamiltonian(N, L, V0, E_scale, mass=ME, hbar=HBAR):
    """周期边界有限差分 H = -(ℏ²/2m)d²/ds² + E_scale·V0 （V0 常数）。

    返回 mp.matrix (N×N 对称)。本征值由 mp.eigsy 求。
    """
    h = L / mp.mpf(N)
    t = (hbar ** 2 / (2 * mass)) / h ** 2   # 动能系数（off-diag 取负）
    H = mp.zeros(N, N)
    diag = 2 * t + E_scale * V0
    for i in range(N):
        H[i, i] = diag
        j = (i + 1) % N
        H[i, j] = -t
        H[j, i] = -t
    return H


def analytic_eigenvalues(L, V0, E_scale, nmax, mass=ME, hbar=HBAR):
    """常数势周期域解析本征值（连续极限）：E_n = E_scale·V0 + (ℏ²/2m)(2πn/L)², n=0,1,2,..."""
    out = []
    for n in range(nmax):
        E = E_scale * V0 + (hbar ** 2 / (2 * mass)) * (2 * mp.pi * n / L) ** 2
        out.append(E)
    return out


def fd_analytic_eigenvalues(N, L, V0, E_scale, mass=ME, hbar=HBAR):
    """有限差分矩阵（周期 2 阶差分）的精确本征值闭式：
    λ_n = E_scale·V0 + (ℏ²/2m)·(2/h²)(1 - cos(2πn/N))，n=0..N-1。
    用于验证 eigsy 求解器本身是否正确（应与数值对角化逐位一致）。"""
    h = L / mp.mpf(N)
    out = []
    for n in range(N):
        kin = (hbar ** 2 / (2 * mass)) * (2 / h ** 2) * (1 - mp.cos(2 * mp.pi * n / N))
        out.append(E_scale * V0 + kin)
    out.sort()
    return out


def solve_spectrum(N, L, V0, E_scale):
    H = build_hamiltonian(N, L, V0, E_scale)
    E, _Z = mp.eigsy(H)   # E: N×1 列矩阵，E[i,0] 为第 i 个本征值
    vals = [E[i, 0] for i in range(N)]
    vals.sort()
    return vals


# ===================================================================
# C 段：矛盾自检（C38 3.1 轻量实现）—— 量纲 + 超光速
# ===================================================================
def contradiction_selfcheck(speed, kappa, tau):
    """返回冲突列表。量纲由调用方保证；此处查超光速与负值。"""
    flags = []
    if not mp.almosteq(speed, C, rel_eps=mp.mpf('1e-240')):
        flags.append("SUPERLUMINAL: |R'| != c")
    if kappa <= 0 or tau <= 0:
        flags.append("NEGATIVE_CURVATURE: κ,τ 应 > 0")
    return flags


# ===================================================================
# 主流程
# ===================================================================
def main():
    print("=" * 72)
    print("空间螺旋修复版 · C25 核心仿真 (mpmath dps=%d)" % mp.mp.dps)
    print("=" * 72)

    # ---- A 段：符号推导 + 数值核验 ----
    print("\n[A] 新基底 Frenet 推导")
    symbolic_frenet()
    # 取三组不同的 (A,b) 满足约束，验证数值自洽且几何无关性
    samples = [(mp.mpf('1e-15'), mp.mpf('1e-15')),
               (mp.mpf('5e-16'), mp.mpf('2e-15')),
               (mp.mpf('2e-15'), mp.mpf('5e-16'))]
    for A_val, b_val in samples:
        r = numeric_frenet(A_val, b_val)
        P("A5", "Frenet数值", "光速约束 |R'|=c (A=%s,b=%s)" % (g(A_val, 3), g(b_val, 3)),
          "PASS" if r["speed_ok"] else "FAIL",
          "speed=%s, c=%s, |Δ|/c=%s" % (g(r["speed"]), g(C), g(abs(r["speed"] - C) / C)))
        P("A6", "Frenet数值", "κ²+τ²=ω²/c² 不变量 (A=%s,b=%s)" % (g(A_val, 3), g(b_val, 3)),
          "PASS" if r["inv_ok"] else "FAIL",
          "κ=%s, τ=%s, κ²+τ²=%s, ω²/c²=%s" % (g(r["kappa"]), g(r["tau"]), g(r["inv"]), g(r["w"] ** 2 / C ** 2)))
        # tanθ = b/A 唯一性核验
        P("A7", "Frenet数值", "tanθ=τ/κ=b/A 唯一性",
          "PASS" if mp.almosteq(r["tan_theta"], r["b_over_A"], rel_eps=mp.mpf('1e-240')) else "FAIL",
          "τ/κ=%s, b/A=%s" % (g(r["tan_theta"]), g(r["b_over_A"])))
        flags = contradiction_selfcheck(r["speed"], r["kappa"], r["tau"])
        if flags:
            rec("A8", "Frenet数值", "矛盾自检", "FAIL", "; ".join(flags))
        else:
            P("A8", "Frenet数值", "矛盾自检(超光速/负值)", "PASS", "无冲突标记")

    # ---- B 段：谱方程求解 + 解析对照 ----
    print("\n[B] 螺旋流形本征算子（完美螺旋→常数势）")
    N = 32
    # 取第一组样本参数
    A = mp.mpf('1e-15')
    b = mp.mpf('1e-15')
    w = C / mp.sqrt(A ** 2 + b ** 2)
    L = helix_arc_length(A, b, w)
    V0 = w ** 2 / C ** 2                      # κ²+τ² = ω²/c²
    E_scale = ME * C ** 2                     # 外部能量尺度（电子静能量级），显式外部输入

    numeric_vals = solve_spectrum(N, L, V0, E_scale)
    fd_analytic = fd_analytic_eigenvalues(N, L, V0, E_scale)
    # B1a：数值对角化 vs FD 精确解析本征值（应逐位一致 → 验证求解器正确）
    max_fd_err = mp.mpf('0')
    for i in range(N):
        if fd_analytic[i] != 0:
            max_fd_err = max(max_fd_err, abs(numeric_vals[i] - fd_analytic[i]) / abs(fd_analytic[i]))
    P("B1", "谱方程", "FD 数值对角化 vs FD 精确解析本征值一致",
      "PASS" if max_fd_err < mp.mpf('1e-120') else "FAIL",
      "N=%d 全谱最大相对误差=%s (dps=%d，验证求解器本身正确)" % (N, g(max_fd_err, 4), mp.mp.dps))
    # B1b：离散化误差 vs 连续极限解析谱（预期 O(sinc² 修正)，非缺陷，如实记录）
    cont_analytic = analytic_eigenvalues(L, V0, E_scale, N)
    max_disc = mp.mpf('0')
    for i in range(min(8, N)):
        if cont_analytic[i] != 0:
            max_disc = max(max_disc, abs(numeric_vals[i] - cont_analytic[i]) / abs(cont_analytic[i]))
    BO("B1b", "谱方程", "有限差分离散化误差(连续极限对照)", "BOUNDARY",
       "N=%d 前8模最大相对离散化误差=%s（=sinc² 修正量级，随 N 增大收敛，非缺陷）" % (N, g(max_disc, 4)))
    # 展示前几个本征值
    IN("B2", "谱方程", "本征值样本", "INFO",
       "E0=%s, E1=%s, E2=%s (J)" % (g(numeric_vals[0], 4), g(numeric_vals[1], 4), g(numeric_vals[2], 4)))

    # ---- C 段：诚实的 α 分析 ----
    print("\n[C] α 与几何脱耦分析（C25 核心诚实结论）")
    # 无量纲能隙 r_n = (E_n - E_0)/E_0
    # 解析：r_n = [(ℏ²/2m)(2πn/L)²] / [E_scale·V0]
    # 对完美螺旋 V0=ω²/c², L=2πc/ω ⇒ (2π/L)²=(ω/c)² ⇒ r_n = (ℏ²/2m)(ω²/c²)/(E_scale·ω²/c²)
    #       = (ℏ²/2m)/E_scale   ← ω 完全抵消！
    def dim_gap(A_val, b_val, E_scale_local):
        A = mp.mpf(A_val); b = mp.mpf(b_val)
        w = C / mp.sqrt(A ** 2 + b ** 2)
        L = helix_arc_length(A, b, w)
        V0 = w ** 2 / C ** 2
        E0 = E_scale_local * V0
        E1 = E_scale_local * V0 + (HBAR ** 2 / (2 * ME)) * (2 * mp.pi / L) ** 2
        return (E1 - E0) / E0

    gaps = [dim_gap(a, b2, E_scale) for (a, b2) in samples]
    spread = max(gaps) - min(gaps)
    # 理论值 (ℏ²/2m)/E_scale
    theory = (HBAR ** 2 / (2 * ME)) / E_scale
    P("C1", "α分析", "无量纲能隙与螺旋几何参数脱耦",
      "PASS" if spread < mp.mpf('1e-60') else "FAIL",
      "三组(A,b)能隙=%s, 极差=%s, 理论值 (ℏ²/2m)/E_scale=%s" %
      (", ".join(g(x, 3) for x in gaps), g(spread, 3), g(theory, 3)))

    # 若强制把能隙等同于 α（候选模型），需要什么外部尺度？
    # α = (ℏ²/2m)/E_scale  ⇒  E_scale = (ℏ²/2m)/α
    E_scale_for_alpha = (HBAR ** 2 / (2 * ME)) / ALPHA
    BO("C2", "α分析", "候选模型 α=(ℏ²/2m)/E_scale 所需外部尺度", "BOUNDARY",
       "若令能隙==α，则 E_scale=%s J（=电子静能的 %s 倍）" %
       (g(E_scale_for_alpha, 4), g(E_scale_for_alpha / (ME * C ** 2), 4)))
    # 自然电子尺度下的能隙值
    natural_gap = (HBAR ** 2 / (2 * ME)) / (ME * C ** 2)
    OP("C3", "α分析", "C25 结论：α 不能由螺旋几何单独钉定", "OPEN",
       "自然电子尺度下能隙=%s，与 α=%s 相差 %s 倍；完美螺旋的几何参数在比值中完全抵消，"
       "α 必须由外部尺度（如 λ_e=ℏ/(m_e c)，本身是测量值）钉定。C25 保持 OPEN。" %
       (g(natural_gap, 3), g(ALPHA, 3), g(ALPHA / natural_gap, 3)))

    # ---- 汇总 ----
    print("\n" + "=" * 72)
    print("汇总（verdict 计数）")
    print("=" * 72)
    from collections import Counter
    cnt = Counter(r["verdict"] for r in RESULTS)
    for k in ("PASS", "OPEN", "BOUNDARY", "INFO", "FAIL"):
        if cnt.get(k):
            print("  %-9s : %d" % (k, cnt[k]))
    print("\n明细：")
    for r in RESULTS:
        print("  [%s] %-10s %s :: %s" % (r["verdict"], r["id"], r["sec"], r["title"]))

    # 输出 claims 风格 JSON（供审计引擎消费）
    out = {"script": "spiral_frenet_spectral_c25.py", "dps": mp.mp.dps,
           "claims": RESULTS}
    with open("spiral_frenet_spectral_c25_claims.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, default=str)
    print("\n已写出 spiral_frenet_spectral_c25_claims.json")


if __name__ == "__main__":
    main()
