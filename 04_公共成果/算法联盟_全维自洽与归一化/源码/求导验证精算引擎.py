# -*- coding: utf-8 -*-
"""
求导验证精算引擎
================

对 openuft 三条求导链做**独立符号复核**（不复用原作者的验证脚本）：

  A 组  圆柱螺旋链（书籍 第十编 第54章）
        r(t) -> v -> a -> Frenet-Serret (kappa, tau) -> 三重奏恒等式 -> kappa/tau 与 alpha 的关系
  B 组  Higgs 破缺链（07_统一场方程/02_变分推导 推论 4.2 / 4.3）
        质量矩阵对角化 -> m_W, m_Z, m_gamma -> rho = 1
  C 组  挠率代数方程（07_统一场方程/02_变分推导 (C') 与推论 1.1）
        24x24 线性系统 rank/nullity -> 判定"挠率不传播"是否成立
  D 组  EDM 单位换算链（书籍 第52/54章）

方法与上一轮"量纲零空间定理"同一套：rank-nullity。
零依赖第三方：仅 sympy / mpmath。

用法：
    cd openuft/04_公共成果/算法联盟_全维自洽与归一化/源码
    python -B 求导验证精算引擎.py
"""
import io
import json
import os
import sys

import sympy as sp
from mpmath import mp, mpf

try:                       # 修复：GBK 控制台无法编码非 GBK 字符时崩溃
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

mp.dps = 40

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, "数据")
os.makedirs(DATA, exist_ok=True)

CHECKS = []


def rec(cid, group, name, status, detail, evidence=None):
    CHECKS.append({
        "id": cid, "group": group, "name": name,
        "status": status, "detail": detail,
        "evidence": evidence or {},
    })


# =====================================================================
# A 组：圆柱螺旋链（第54章）
# =====================================================================
def group_A():
    t, R, b, w, c = sp.symbols('t R b omega c', positive=True)

    # 参数方程 r(t) = (R cos wt, R sin wt, b w t)
    r = sp.Matrix([R * sp.cos(w * t), R * sp.sin(w * t), b * w * t])

    # --- A1 一阶导（速度）
    v = sp.diff(r, t)
    v_expected = sp.Matrix([-w * R * sp.sin(w * t), w * R * sp.cos(w * t), b * w])
    ok = sp.simplify(v - v_expected) == sp.zeros(3, 1)
    rec("A1", "螺旋链", "一阶导 v = dr/dt", "PASS" if ok else "FAIL",
        "v = (-ωR sin ωt, ωR cos ωt, bω)" if ok else "与书中 v 表达式不符",
        {"v": str(v.T)})

    # --- A2 光速公设 |v|^2 = w^2 (R^2 + b^2)
    v2 = sp.simplify((v.T * v)[0, 0])
    ok = sp.simplify(v2 - w ** 2 * (R ** 2 + b ** 2)) == 0
    rec("A2", "螺旋链", "光速公设 |v|² = ω²(R²+b²)", "PASS" if ok else "FAIL",
        "|v|² = %s，与 ω²(R²+b²) 恒等" % sp.simplify(v2) if ok else "不恒等",
        {"v2": str(v2)})

    # --- A3 二阶导 + v·a = 0
    a = sp.diff(v, t)
    va = sp.simplify((v.T * a)[0, 0])
    ok = va == 0
    rec("A3", "螺旋链", "v·a = 0（径向不做功）", "PASS" if ok else "FAIL",
        "v·a = 0 恒等成立" if ok else "v·a = %s ≠ 0" % va, {"va": str(va)})

    # --- A4 Frenet-Serret：kappa = |r' x r''| / |r'|^3
    cross = v.cross(a)
    kappa = sp.simplify(sp.sqrt((cross.T * cross)[0, 0]) / sp.sqrt(v2) ** 3)
    kappa_claimed = R / (R ** 2 + b ** 2)
    ok = sp.simplify(kappa - kappa_claimed) == 0
    rec("A4", "螺旋链", "曲率 κ = R/(R²+b²)", "PASS" if ok else "FAIL",
        "符号求导所得 κ 与书中闭式一致" if ok else "符号求导 κ=%s，书中=%s，不符" % (kappa, kappa_claimed),
        {"kappa_derived": str(kappa), "kappa_claimed": str(kappa_claimed)})

    # --- A5 挠率 tau = det(r',r'',r''') / |r' x r''|^2
    j = sp.diff(a, t)
    det3 = sp.Matrix.hstack(v, a, j).det()
    tau = sp.simplify(det3 / ((cross.T * cross)[0, 0]))
    tau_claimed = b / (R ** 2 + b ** 2)
    ok = sp.simplify(tau - tau_claimed) == 0
    rec("A5", "螺旋链", "挠率 τ = b/(R²+b²)", "PASS" if ok else "FAIL",
        "符号求导所得 τ 与书中闭式一致" if ok else "符号求导 τ=%s，书中=%s，不符" % (tau, tau_claimed),
        {"tau_derived": str(tau), "tau_claimed": str(tau_claimed)})

    # --- A6 三重奏恒等式 κ² + τ² = ω²/c²
    lhs = sp.simplify(kappa_claimed ** 2 + tau_claimed ** 2)
    # c² = ω²(R²+b²)  =>  ω²/c² = 1/(R²+b²)
    rhs = 1 / (R ** 2 + b ** 2)
    ok = sp.simplify(lhs - rhs) == 0
    rec("A6", "螺旋链", "三重奏恒等式 κ²+τ² = (ω/c)²", "PASS" if ok else "FAIL",
        "κ²+τ² = 1/(R²+b²) = ω²/c²，恒等成立" if ok else "不闭合",
        {"lhs": str(lhs)})

    # --- A7 关键：κ/τ = R/b = tanθ，而非 sinθ = α
    ratio = sp.simplify(kappa_claimed / tau_claimed)
    # 书中设定：R = α·ρ, b = ρ·sqrt(1-α²)  =>  R/b = α/sqrt(1-α²) = tanθ (sinθ=α)
    al = sp.symbols('alpha', positive=True)
    rho = sp.symbols('rho', positive=True)
    R_of = al * rho
    b_of = rho * sp.sqrt(1 - al ** 2)
    ratio_sub = sp.simplify(ratio.subs({R: R_of, b: b_of}))
    tan_theta = al / sp.sqrt(1 - al ** 2)
    is_tan = sp.simplify(ratio_sub - tan_theta) == 0
    is_alpha = sp.simplify(ratio_sub - al) == 0
    if is_tan and not is_alpha:
        rec("A7", "螺旋链", "κ/τ 究竟等于 tanθ 还是 sinθ(=α)", "FAIL",
            "**符号求导判定：κ/τ = R/b = α/√(1-α²) = tanθ，不等于 α = sinθ。"
            "第54章 §53.2.4 写 'α = κ/τ = ρ/b' 有误；§53.4.2 已承认此点，"
            "但 §53.3.3 数值表与 §53.7 五字段表仍在使用被自己否定的公式。**",
            {"kappa_over_tau": str(ratio_sub), "tan_theta": str(tan_theta),
             "is_tan": True, "is_alpha": False})
    elif is_alpha:
        rec("A7", "螺旋链", "κ/τ = α", "PASS", "κ/τ 恒等于 α", {})
    else:
        rec("A7", "螺旋链", "κ/τ 与 α 的关系", "INFO",
            "κ/τ = %s，既非 tanθ 亦非 α，需人工判读" % ratio_sub, {})

    # --- A8 偏差量级：tanθ - α ≈ α²/2
    alpha_num = mpf('7.2973525693e-3')  # CODATA 2022
    tan_num = mpf(alpha_num) / mp.sqrt(1 - mpf(alpha_num) ** 2)
    dev_abs = tan_num - mpf(alpha_num)
    dev_rel = dev_abs / mpf(alpha_num)
    half_a2 = mpf(alpha_num) ** 2 / 2
    ok = abs(dev_rel - half_a2) / half_a2 < mpf('1e-3')
    rec("A8", "螺旋链", "偏差 tanθ−α 是否等于 α²/2", "PASS" if ok else "FAIL",
        "tanθ−α = %s（绝对），相对偏差 %s；α²/2 = %s；二者吻合到 1e-3 以内。"
        "**这就是第54章 §53.3.3 表中 2.66e-05 的来源——它不是数值误差，是定义性系统偏差。**"
        % (mp.nstr(dev_abs, 8), mp.nstr(dev_rel, 8), mp.nstr(half_a2, 8)),
        {"tan_theta": mp.nstr(tan_num, 12), "alpha": mp.nstr(alpha_num, 12),
         "dev_rel": mp.nstr(dev_rel, 8), "alpha2_over_2": mp.nstr(half_a2, 8)})

    # --- A9 复现第54章表中数值 κ/τ = 0.0072975469
    reported = mpf('0.0072975469')
    match = abs(reported - tan_num) / tan_num < mpf('1e-7')
    rec("A9", "螺旋链", "表中 0.0072975469 的实际身份", "PASS" if match else "FAIL",
        "第54章 §53.3.3 报的 α=κ/τ=0.0072975469 与 tanθ=%s 吻合到 1e-7，"
        "与 sinθ=α=%s 差 2.66e-05。**该数值是 tanθ，不是 α。**"
        % (mp.nstr(tan_num, 10), mp.nstr(alpha_num, 10)) if match
        else "表中数值既非 tanθ 亦需复核",
        {"reported": str(reported), "tan_theta": mp.nstr(tan_num, 10)})

    # --- A10 力 F = m R ω²（数值）
    m_e = mpf('9.1093837015e-31')
    R_e = mpf('2.8179403262e-15')
    w_e = mpf('7.763441e20')
    F = m_e * R_e * w_e ** 2
    alt = m_e * mpf(alpha_num) * mpf('2.99792458e8') * w_e
    ok = abs(F - alt) / F < mpf('1e-4')
    rec("A10", "螺旋链", "螺旋恢复力 |F| = mRω² = mαcω", "PASS" if ok else "FAIL",
        "|F| = %s N，与 mαcω = %s N 一致（相对差 <1e-4）；书中报 1.5471e-3 N"
        % (mp.nstr(F, 6), mp.nstr(alt, 6)),
        {"F": mp.nstr(F, 8), "F_alt": mp.nstr(alt, 8)})


# =====================================================================
# B 组：Higgs 破缺链（UFE-1 推论 4.2 / 4.3）
# =====================================================================
def group_B():
    v, g1, g2 = sp.symbols('v g_1 g_2', positive=True)

    # 中性扇区质量矩阵（基 W^3, B），来自 (v²/8)(g2 W³ - g1 B)² 的二次型
    M2 = sp.Matrix([[g2 ** 2, -g2 * g1], [-g2 * g1, g1 ** 2]]) * v ** 2 / 4
    ev = M2.eigenvals()
    ev_list = sorted([sp.simplify(e) for e in ev.keys()])
    expect = [sp.Integer(0), (g2 ** 2 + g1 ** 2) * v ** 2 / 4]
    ok = all(sp.simplify(a - b) == 0 for a, b in zip(ev_list, expect))
    rec("B1", "Higgs链", "中性规范玻色子质量矩阵本征值", "PASS" if ok else "FAIL",
        "本征值 {0, (g₂²+g₁²)v²/4} —— 一个质量为 0（光子），一个为 Z"
        if ok else "本征值 = %s，与预期 {0, (g₂²+g₁²)v²/4} 不符" % ev_list,
        {"eigenvalues": [str(e) for e in ev_list]})

    mW = g2 * v / 2
    mZ = sp.sqrt(g2 ** 2 + g1 ** 2) * v / 2
    cosW = g2 / sp.sqrt(g2 ** 2 + g1 ** 2)
    rho = sp.simplify(mW ** 2 / (mZ ** 2 * cosW ** 2))
    ok = rho == 1
    rec("B2", "Higgs链", "树级 custodial 参数 ρ = m_W²/(m_Z²cos²θ_W) = 1",
        "PASS" if ok else "FAIL",
        "ρ 符号化简恒等于 1 —— 这是**结构结论**，不依赖参数数值" if ok
        else "ρ = %s ≠ 1" % rho, {"rho": str(rho)})

    # e = g2 g1 / sqrt(g2²+g1²) 与 tanθ_W = g1/g2 的自洽性
    e_def = g2 * g1 / sp.sqrt(g2 ** 2 + g1 ** 2)
    e_alt1 = g2 * (g1 / sp.sqrt(g2 ** 2 + g1 ** 2))   # g2 sinθ_W
    e_alt2 = g1 * (g2 / sp.sqrt(g2 ** 2 + g1 ** 2))   # g1 cosθ_W
    ok = sp.simplify(e_def - e_alt1) == 0 and sp.simplify(e_def - e_alt2) == 0
    rec("B3", "Higgs链", "e = g₂sinθ_W = g₁cosθ_W = g₂g₁/√(g₂²+g₁²)",
        "PASS" if ok else "FAIL",
        "三种写法符号恒等 —— 电荷是破缺后的**残留**耦合，非独立输入" if ok
        else "三种写法不自洽", {})

    # v = (sqrt(2) G_F)^{-1/2}
    GF = mpf('1.1663787e-5')   # GeV^-2
    v_num = 1 / mp.sqrt(mp.sqrt(2) * GF)
    ok = abs(v_num - mpf('246.22')) < mpf('0.05')
    rec("B4", "Higgs链", "v = (√2·G_F)^{-1/2} 的数值", "PASS" if ok else "FAIL",
        "v = %s GeV，与书中 246.22 GeV 一致" % mp.nstr(v_num, 8) if ok
        else "v = %s，与 246.22 不符" % mp.nstr(v_num, 8),
        {"v_GeV": mp.nstr(v_num, 8)})

    # v² = μ²/λ：由 dV/dH = 0 与真空期望值定义
    mu, lam, H = sp.symbols('mu lambda H', positive=True)
    V = -mu ** 2 * H ** 2 + lam * H ** 4
    sol = sp.solve(sp.diff(V, H), H)
    H_vev = [s for s in sol if s != 0][0]
    # H = (0,(v+h)/√2)  =>  |H|² = v²/2 ；此处 V 以 |H|=H 为变量
    v_from_V = sp.simplify(sp.sqrt(2) * H_vev)
    ok = sp.simplify(v_from_V ** 2 - mu ** 2 / lam) == 0
    rec("B5", "Higgs链", "v² = μ²/λ（由 ∂V/∂H = 0 推出）", "PASS" if ok else "FAIL",
        "∂V/∂H=0 给出 |H|² = μ²/(2λ)，按 H=(0,(v+h)/√2) 归一化得 v²=μ²/λ ✓"
        if ok else "v² = %s，与 μ²/λ 不符" % v_from_V ** 2,
        {"H_vev": str(H_vev)})


# =====================================================================
# C 组：挠率代数方程 (C') 的 rank–nullity 判定
# =====================================================================
def group_C():
    """
    (C')  T^λ_{μν} + δ^λ_μ T^σ_{νσ} - δ^λ_ν T^σ_{μσ} = κ² s^λ_{μν}

    未知：T^λ_{μν} 对 (μν) 反对称 => 4 × 6 = 24 个分量
    方程：对每个 (λ, μ<ν) 一个 => 24 条
    构造 24×24 整数矩阵 M，使 M·vec(T) = κ²·vec(s)

    推论 1.1「挠率不传播」成立 <=> M 可逆 <=> nullity = 0
    若 nullity > 0，则存在 s=0 但 T≠0 的解 = 自由传播的挠率模
    """
    dim = 4
    pairs = [(m, n) for m in range(dim) for n in range(dim) if m < n]
    idx = {}
    k = 0
    for lam in range(dim):
        for (m, n) in pairs:
            idx[(lam, m, n)] = k
            k += 1
    N = k  # 24

    def T_of(vecT, a, b_, c_):
        """返回 T^a_{b c}，利用对 (b,c) 的反对称性规范化到规范序"""
        if b_ == c_:
            return 0
        if b_ < c_:
            return vecT[idx[(a, b_, c_)]]
        return -vecT[idx[(a, c_, b_)]]

    M = sp.zeros(N, N)
    for lam in range(dim):
        for (m, n) in pairs:
            row = idx[(lam, m, n)]
            # 主项 T^λ_{μν}
            M[row, idx[(lam, m, n)]] += 1
            # + δ^λ_μ · Σ_σ T^σ_{νσ}
            if lam == m:
                for s in range(dim):
                    if s == n:
                        continue
                    key = (s, n, s) if n < s else (s, s, n)
                    sign = 1 if n < s else -1
                    M[row, idx[key]] += sign
            # - δ^λ_ν · Σ_σ T^σ_{μσ}
            if lam == n:
                for s in range(dim):
                    if s == m:
                        continue
                    key = (s, m, s) if m < s else (s, s, m)
                    sign = 1 if m < s else -1
                    M[row, idx[key]] -= sign

    rank = M.rank()
    nullity = N - rank
    ok = (nullity == 0)
    rec("C1", "挠率方程", "Cartan 方程 (C') 的 rank–nullity",
        "PASS" if ok else "FAIL",
        "24×24 系统：rank = %d，nullity = %d。%s"
        % (rank, nullity,
           "**M 可逆 ⇒ T 完全由 s 代数决定 ⇒ 挠率无独立传播自由度，UFE-1 推论 1.1 成立。**"
           if ok else
           "**nullity>0 ⇒ 存在 s=0 而 T≠0 的解 ⇒ 挠率含自由传播模，推论 1.1 不成立。**"),
        {"rank": rank, "nullity": nullity, "dim": N})

    # C2 显式解：验证 s 全反对称时 T 也全反对称
    if nullity == 0:
        # 取 s^λ_{μν} = ε^{λμνρ} J_ρ，J = (0,0,0,1)
        J = [0, 0, 0, 1]

        def eps(a, b_, c_, d):
            perm = (a, b_, c_, d)
            seen = []
            sgn = 1
            for i in range(4):
                for j in range(i + 1, 4):
                    if perm[i] == perm[j]:
                        return 0
            # 直接按标准 Levi-Civita（0123）=+1 计算符号
            arr = list(perm)
            inv = 0
            for i in range(4):
                for j in range(i + 1, 4):
                    if arr[i] > arr[j]:
                        inv += 1
            return (-1) ** inv

        svec = sp.zeros(N, 1)
        for lam in range(dim):
            for (m, n) in pairs:
                val = 0
                for rho in range(dim):
                    val += eps(lam, m, n, rho) * J[rho]
                svec[idx[(lam, m, n)], 0] = val

        Tvec = M.solve(svec)
        # 检验 T 是否全反对称：T_{λμν} 应对三指标全反对称
        def Tval(a, b_, c_):
            if b_ == c_:
                return 0
            if b_ < c_:
                return Tvec[idx[(a, b_, c_)]]
            return -Tvec[idx[(a, c_, b_)]]

        antisym_ok = True
        for a in range(dim):
            for b_ in range(dim):
                for c_ in range(dim):
                    for perm_sgn, (p, q, r_) in [(1, (a, b_, c_)), (-1, (a, c_, b_)),
                                                 (-1, (b_, a, c_)), (1, (b_, c_, a)),
                                                 (1, (c_, a, b_)), (-1, (c_, b_, a))]:
                        pass
        # 更简洁：检查 T_{abc} = -T_{bac} 且 T_{abc} = -T_{acb}
        # 前者由构造保证（对后两指标反对称），只需检查 T_{abc} = -T_{bac}
        viol = []
        for a in range(dim):
            for b_ in range(dim):
                for c_ in range(dim):
                    if sp.simplify(Tval(a, b_, c_) + Tval(b_, a, c_)) != 0:
                        viol.append((a, b_, c_))
        fully_antisym = (len(viol) == 0)
        # 系数：与 (κ²/2) ε_{λμνρ} J^ρ 比较（κ²=1）
        coef = None
        if fully_antisym:
            for a in range(dim):
                for b_ in range(dim):
                    for c_ in range(dim):
                        e = eps(a, b_, c_, 3)
                        if e != 0:
                            coef = sp.nsimplify(Tval(a, b_, c_) / (sp.Rational(1, 2) * e))
                            break
                    if coef is not None:
                        break
                if coef is not None:
                    break
        rec("C2", "挠率方程", "全反对称自旋流 ⇒ 全反对称挠率（推论 1.2）",
            "PASS" if fully_antisym else "FAIL",
            "s 取全反对称 ε^{λμνρ}J_ρ 时，解出的 T %s。"
            "与书中 T_{λμν}=(κ²/2)ε_{λμνρ}J_A^ρ 的系数比为 %s（度规约定差异如实保留）。"
            % ("亦为全反对称" if fully_antisym else "**不全反对称，推论 1.2 需修正**",
               str(coef) if coef is not None else "N/A"),
            {"fully_antisymmetric": fully_antisym,
             "coefficient_ratio": str(coef) if coef is not None else None})

    # C3 与量纲零空间定理的同构性（元层次）
    rec("C3", "挠率方程", "与量纲零空间定理的方法同构性", "INFO",
        "本判定与第56章「量纲零空间定理」用的是同一套线性代数："
        "前者问 nullity(D_A)=n−rank(D_A) 是否为 0（能否由 {c,ℏ,G} 组合出无量纲量），"
        "后者问 nullity(M)=24−rank(M) 是否为 0（挠率能否由自旋流唯一决定）。"
        "**两个问题的答案都是 0，但语义相反：量纲零空间为 0 ⇒ 什么都导不出；"
        "挠率零空间为 0 ⇒ 一切都由源决定、无自由度。**",
        {"analogy": "nullity=0 has opposite meaning in the two contexts"})


# =====================================================================
# D 组：EDM 单位换算链
# =====================================================================
def group_D():
    e_charge = mpf('1.602176634e-19')      # C
    alpha = mpf('7.2973525693e-3')
    r_e = mpf('2.8179403262e-15')          # 经典电子半径（第54章修正后的横向半径）
    rho_c = mpf('3.861593e-13')            # 康普顿半径 ℏ/(m_e c)（修正前的横向半径）
    limit = mpf('4.1e-30')                 # e·cm, JILA HfF+ 2023

    def to_ecm(d_cm):
        return d_cm / (e_charge * mpf('1e-2'))

    # --- D1 ρ 取康普顿半径：复现书中 2.257e-34 C·m
    d_Cm_c = e_charge * alpha * rho_c / 2
    d_ecm_c = to_ecm(d_Cm_c)
    ok1 = abs(d_Cm_c - mpf('2.257e-34')) / mpf('2.257e-34') < mpf('1e-3')
    rec("D1", "EDM链", "d_e = eαρ/2 在 ρ = 康普顿半径下的取值",
        "PASS" if ok1 else "FAIL",
        "ρ = ℏ/(m_ec) = %s m 时，d_e = %s C·m = %s e·cm，"
        "与第54章 §53.5.4 报的 2.257e-34 C·m / 1.409e-13 e·cm 一致。"
        "**即：该数值用的是康普顿半径。**"
        % (mp.nstr(rho_c, 8), mp.nstr(d_Cm_c, 8), mp.nstr(d_ecm_c, 8)) if ok1
        else "d_e = %s C·m，与 2.257e-34 不符" % mp.nstr(d_Cm_c, 8),
        {"rho": "compton", "d_Cm": mp.nstr(d_Cm_c, 10), "d_ecm": mp.nstr(d_ecm_c, 10)})

    # --- D2 ρ 取经典电子半径（第54章自己的修正）：数值变 1/α ≈ 137 倍
    d_Cm_r = e_charge * alpha * r_e / 2
    d_ecm_r = to_ecm(d_Cm_r)
    ratio_of_radii = d_Cm_c / d_Cm_r
    ok2 = abs(ratio_of_radii - 1 / alpha) / (1 / alpha) < mpf('1e-3')
    rec("D2", "EDM链", "改用第54章修正后的 r_e 时 d_e 的变化",
        "PASS" if ok2 else "FAIL",
        "ρ = r_e = %s m 时，d_e = %s C·m = %s e·cm。"
        "两值之比 = %s ≈ 1/α = %s —— **第54章 §53.5.4 引用的 EDM 数值，"
        "用的是该章自己在 §53.3.1 判定应当替换掉的康普顿半径。**"
        % (mp.nstr(r_e, 8), mp.nstr(d_Cm_r, 8), mp.nstr(d_ecm_r, 8),
           mp.nstr(ratio_of_radii, 8), mp.nstr(1 / alpha, 8)) if ok2
        else "比值 = %s，非 1/α" % mp.nstr(ratio_of_radii, 8),
        {"rho": "classical", "d_Cm": mp.nstr(d_Cm_r, 10), "d_ecm": mp.nstr(d_ecm_r, 10),
         "ratio": mp.nstr(ratio_of_radii, 8)})

    # --- D3 稳健性：两种取值下与上限比较，结论是否一致
    r_c = d_ecm_c / limit
    r_r = d_ecm_r / limit
    both_excluded = (r_c > 1) and (r_r > 1)
    rec("D3", "EDM链", "证伪结论的稳健性（对 ρ 取值不敏感）",
        "PASS" if both_excluded else "FAIL",
        "JILA 上限 %s e·cm。ρ=康普顿时超出 %s 倍（%.1f 个数量级）；"
        "ρ=r_e 时超出 %s 倍（%.1f 个数量级）。**两种取值下结论一致：均已被证伪。"
        "预言值对横向半径敏感（差 137 倍），但证伪结论不敏感（差 2 个数量级但都远超上限）。**"
        % (mp.nstr(limit, 4), mp.nstr(r_c, 6), mp.log10(r_c),
           mp.nstr(r_r, 6), mp.log10(r_r)) if both_excluded
        else "两种取值下结论不一致，需人工判读",
        {"ratio_compton": mp.nstr(r_c, 8), "orders_compton": mp.nstr(mp.log10(r_c), 4),
         "ratio_classical": mp.nstr(r_r, 8), "orders_classical": mp.nstr(mp.log10(r_r), 4)})

    rec("D4", "EDM链", "对称性论证与数值预言的并置关系", "INFO",
        "第54章 §53.5 用螺旋对称性论证 d_e = 0（[A] 对称性结论），"
        "§53.5.4 又列出 d_e = eαρ/2（g2_EDM.py 的假设）。"
        "**二者不矛盾，但必须明确分工**：被证伪的是「破坏螺旋对称性的附加偏移假设」，"
        "不是螺旋对称性本身。书中把两者并置于同一节，未显式切割，易被误读为"
        "「螺旋模型预言了非零 EDM 并被证伪」。正确读法是："
        "**螺旋模型预言 0（与实验相容）；额外假设预言非零，该假设被证伪。**",
        {})


# =====================================================================
# 输出
# =====================================================================
def render_md():
    n_pass = sum(1 for c in CHECKS if c["status"] == "PASS")
    n_fail = sum(1 for c in CHECKS if c["status"] == "FAIL")
    n_info = sum(1 for c in CHECKS if c["status"] == "INFO")
    L = []
    L.append("# 求导验证精算（符号复核）")
    L.append("")
    L.append("**引擎**：`源码/求导验证精算引擎.py`（sympy + mpmath，独立复核，不复用原作者脚本）")
    L.append("")
    L.append("**总计 %d 项：PASS %d / FAIL %d / INFO %d**" % (len(CHECKS), n_pass, n_fail, n_info))
    L.append("")
    L.append("| 编号 | 组 | 检查项 | 结论 | 说明 |")
    L.append("| --- | --- | --- | --- | --- |")
    for c in CHECKS:
        mark = {"PASS": "✅", "FAIL": "❌", "INFO": "ℹ️"}[c["status"]]
        L.append("| %s | %s | %s | %s | %s |" % (c["id"], c["group"], c["name"], mark,
                                                 c["detail"].replace("\n", " ")))
    L.append("")
    L.append("## 逐项证据")
    L.append("")
    for c in CHECKS:
        L.append("### %s · %s — %s" % (c["id"], c["name"], c["status"]))
        L.append("")
        L.append(c["detail"])
        L.append("")
        if c["evidence"]:
            L.append("```json")
            L.append(json.dumps(c["evidence"], ensure_ascii=False, indent=2))
            L.append("```")
            L.append("")
    return "\n".join(L)


def main():
    group_A()
    group_B()
    group_C()
    group_D()

    payload = {
        "tool": "求导验证精算引擎",
        "total": len(CHECKS),
        "pass": sum(1 for c in CHECKS if c["status"] == "PASS"),
        "fail": sum(1 for c in CHECKS if c["status"] == "FAIL"),
        "info": sum(1 for c in CHECKS if c["status"] == "INFO"),
        "checks": CHECKS,
    }
    with io.open(os.path.join(DATA, "求导验证精算_2026-09-19.json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2))
    with io.open(os.path.join(DATA, "求导验证精算.md"), "w", encoding="utf-8") as fh:
        fh.write(render_md())

    out = []
    out.append("=" * 70)
    out.append("求导验证精算引擎")
    out.append("=" * 70)
    for c in CHECKS:
        mark = {"PASS": "[PASS]", "FAIL": "[FAIL]", "INFO": "[INFO]"}[c["status"]]
        out.append("%-4s %-8s %-6s %s" % (c["id"], mark, c["group"], c["name"]))
        if c["status"] == "FAIL":
            out.append("      -> %s" % c["detail"].replace("\n", " "))
    out.append("-" * 70)
    out.append("TOTAL %d | PASS %d | FAIL %d | INFO %d"
               % (payload["total"], payload["pass"], payload["fail"], payload["info"]))
    txt = "\n".join(out)
    with io.open(os.path.join(HERE, "_求导验证_stdout.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt)
    print("done: see 数据/求导验证精算.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
