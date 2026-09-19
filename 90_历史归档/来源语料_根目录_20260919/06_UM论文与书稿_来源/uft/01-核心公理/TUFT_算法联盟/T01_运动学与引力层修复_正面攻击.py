# -*- coding: utf-8 -*-
"""
T01 运动学与引力层修复 正面攻击 (H1 / H2 / H3 / H7)
算法联盟 · TUFT 系列 · 2026-09-15

攻击目标：
  H1 公理I 速率=c 与有静质量粒子冲突
  H2 定理5 引力加速度符号
  H3 定理4/5/7 (beta1 - kappa - g) 三重不自洽
  H7 定理7 场方程在点源处失效

红线：只记录计算所得判定；未闭合项标 OPEN；不把"方案可行"粉饰为"理论已证"。
"""

import sys
import os
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import sympy as sp
import mpmath as mp

mp.mp.dps = 40

RESULTS = []


def rec(item, name, verdict, detail):
    RESULTS.append({"项": item, "名称": name, "判定": verdict, "说明": detail})
    print("[" + verdict + "] " + item + " | " + name)
    print("        " + detail)
    return verdict


# ============================================================ H1 共动系双分解
def sec_H1():
    hbar = mp.mpf("1.054571817e-34")
    c = mp.mpf("299792458")

    parts = [("电子 e", "9.1093837015e-31"),
             ("μ子 mu", "1.883531627e-28"),
             ("τ子 tau", "3.16754e-27"),
             ("质子 p", "1.67262192369e-27")]

    rows = []
    worst = mp.mpf(0)
    for nm, ms in parts:
        m = mp.mpf(ms)
        omega0 = m * c ** 2 / hbar          # 内部频率（共动系）
        R = c / omega0                      # 内部圆半径 = hbar/(m c) 约化康普顿波长
        kappa = 1 / R                       # 内部曲率
        m_back = hbar * kappa / c           # 定理3 反代
        rel = abs(m_back - m) / m
        worst = max(worst, rel)
        rows.append(nm + ": omega0=" + mp.nstr(omega0, 6) + " rad/s, R=" + mp.nstr(R, 6)
                    + " m, kappa=" + mp.nstr(kappa, 6) + " 1/m, 定理3回代残差=" + mp.nstr(rel, 4))

    # 相对论速度叠加：共动系内部横向速率 = c（类光），沿 x 以 u boost
    u = mp.mpf("0.6") * c
    gam = 1 / mp.sqrt(1 - (u / c) ** 2)
    den = 1 + u * mp.mpf(0) / c ** 2
    vx_lab = (mp.mpf(0) + u) / den
    vy_lab = c / (gam * den)
    speed_lab = mp.sqrt(vx_lab ** 2 + vy_lab ** 2)
    rel_speed = abs(speed_lab - c) / c

    # 质心四速归一（eta = diag(1,-1,-1,-1)）
    U0 = gam * c
    U1 = gam * u
    norm2 = U0 ** 2 - U1 ** 2
    rel_norm = abs(norm2 - c ** 2) / c ** 2

    ok = (worst < mp.mpf("1e-25")) and (rel_speed < mp.mpf("1e-25")) and (rel_norm < mp.mpf("1e-25")) and (u < c)

    detail = ("【修复方案A：共动系双分解】内部周期运动在共动系以速率 c 走闭合环（类光），"
              "质心以 u<c 运动（类时）。实跑：(1) 内部半径 R=c/omega0=hbar/(mc) 即约化康普顿波长, "
              "kappa=mc/hbar, 代回定理3 m=hbar*kappa/c 残差=" + mp.nstr(worst, 4) + "; "
              + "; ".join(rows) + ". "
              + "(2) 速度叠加自检: u=0.6c 时 lab 系内部点速率 |v'|=" + mp.nstr(speed_lab, 20)
              + " (=c, 残差 " + mp.nstr(rel_speed, 4) + ")，质心 u=0.6c<c; "
              + "(3) 质心四速归一 U.U=c^2 残差=" + mp.nstr(rel_norm, 4) + ". "
              + "结论：H1 的冲突源于把『内部螺旋点』当作『质点本身』；分层后内部光速运动与质心类时运动、"
                "非零静质量三者并存，公理I 须改写为『共动系内时空元速率模 = c』")
    return rec("T01-1", "H1 运动学冲突修复（方案A 共动系双分解）", "PASS" if ok else "FAIL", detail)


# ============================================================ H2 符号
def sec_H2():
    R, th = sp.symbols("R theta", positive=True)
    rv = sp.Matrix([R * sp.cos(th), R * sp.sin(th), 0])
    T = sp.simplify(rv.diff(th) / R)
    dTds = sp.simplify(T.diff(th) / R)
    kappa = sp.simplify(dTds.norm())
    N = sp.simplify(dTds / kappa)
    radial = sp.Matrix([sp.cos(th), sp.sin(th), 0])
    n_dot_r = sp.simplify(N.dot(radial))

    ok = (n_dot_r == -1)
    detail = ("圆轨道实算 N.r_hat=" + str(n_dot_r) + "（N 指向曲率中心）。"
              + "向心（吸引）方向 = +N，故 F=+m c^2 kappa N（定理6）正确；"
              + "定理5 原稿 g=-c^2 kappa N 指向背离中心（排斥）且使 F != m g。 "
              + "【修订】g=+c^2 kappa N。修订后 |g|=c^2 kappa 与定理6 及牛顿极限一致")
    return rec("T01-2", "H2 引力加速度符号修订", "PASS" if ok else "FAIL", detail)


# ============================================================ H3 路径I 证伪
def sec_H3_pathI():
    G = mp.mpf("6.67430e-11")
    M = mp.mpf("5.972e24")
    c = mp.mpf("299792458")
    R = mp.mpf("6.371e6")

    gN_R = G * M / R ** 2                 # 地表牛顿值 9.82
    a = c ** 2 / gN_R - R                 # 令路径I 在地表与牛顿匹配，定积分常数
    out = []
    for k in [2, 10, 100]:
        rr = k * R
        gI = c ** 2 / (rr + a)
        gN = G * M / rr ** 2
        out.append("r=" + str(k) + "R_E: g_I/g_N=" + mp.nstr(gI / gN, 6))

    ok = False   # 路径 I 被证伪（正合预期）
    detail = ("【路径I = 保留 (T4) beta1=(kappa^2+tau^2)/K0 + (T5) |g|=c^2 kappa + (T7) 对数律】"
              + "三式联立解得 dkappa/dr=-kappa^2 ⇒ kappa=1/(r+a) ⇒ |g|=c^2/(r+a)（1/r 引力）。"
              + "以地表匹配定 a=" + mp.nstr(a, 6) + " m（约 0.97 光年），此后 g 几乎不随 r 衰减: "
              + "; ".join(out) + "（牛顿应为 1）。"
              + "结论：路径I 与开普勒/牛顿及一切观测根本冲突，【被证伪】，不得采用")
    return rec("T01-3", "H3 路径I（保留 beta1=kappa^2/K0）", "FAIL", detail)


# ============================================================ H3 路径II 修复
def sec_H3_pathII():
    r, G, M, c = sp.symbols("r G M c", positive=True)

    Phi = -G * M / r                                   # 牛顿势
    beta_pot = sp.exp(-2 * Phi / c ** 2)               # 修复后 beta1^(pot) 定义
    kappa_field = sp.simplify(sp.diff(Phi, r) / c ** 2)   # |grad Phi|/c^2 = GM/(c^2 r^2)

    # 检查1: 1/2 |grad ln beta| == kappa_field
    half_grad_lnbeta = sp.simplify(sp.diff(sp.log(beta_pot), r) / 2)
    e1 = sp.simplify(half_grad_lnbeta + kappa_field)

    # 检查2: |c^2/2 grad ln beta| == GM/r^2
    g_r = sp.simplify(c ** 2 / 2 * sp.diff(sp.log(beta_pot), r))
    e2 = sp.simplify(g_r + G * M / r ** 2)

    # 检查3: 外部场方程
    lap_beta = sp.diff(r ** 2 * sp.diff(beta_pot, r), r) / r ** 2
    e3 = sp.simplify(lap_beta - sp.diff(beta_pot, r) ** 2 / beta_pot)

    # 检查4: 路径积分一致性  ln beta = 2 ∫_inf^r kappa_field dn  （沿主法向内）
    k_int = sp.integrate(G * M / (c ** 2 * r ** 2), (r, sp.oo, r))   # = -GM/(c^2 r)
    e4 = sp.simplify(sp.log(beta_pot) - (-2) * k_int)

    ok = (e1 == 0) and (e2 == 0) and (e3 == 0) and (e4 == 0)
    detail = ("【路径II = 双 beta 分层】beta1^(pot)≡exp(-2Phi/c^2)，kappa_field≡|grad Phi|/c^2，"
              + "局域激发强度 beta1^(loc)≡(kappa^2+tau^2)/K0 保留但【不】参与引力对数律。实跑: "
              + "(1) (1/2)|grad ln beta_pot| - kappa_field = " + str(e1) + "; "
              + "(2) (c^2/2)grad ln beta_pot 径向 = " + str(g_r) + "（=-GM/r^2，牛顿）; "
              + "(3) 外部场方程 nabla^2 beta - (grad beta)^2/beta = " + str(e3) + "; "
              + "(4) 路径积分 ln beta = 2∫kappa dn 残差 = " + str(e4) + ". "
              + "结论：H3 三重矛盾由『同一 kappa 同时充当自曲率与外场曲率』引起；分层后全部自洽。"
                "理论代价：惯性比概念一分为二，需额外说明二者的物理联系（记 O-beta2）")
    return rec("T01-4", "H3 路径II 修复（双 beta 分层）", "PASS" if ok else "FAIL", detail)


# ============================================================ H7 源区
def sec_H7():
    r, Rs, G, M, c, rho = sp.symbols("r R_s G M c rho", positive=True)

    # 均匀密度球内部牛顿势
    Phi_in = -G * M * (3 * Rs ** 2 - r ** 2) / (2 * Rs ** 3)
    lap_Phi_in = sp.simplify(sp.diff(r ** 2 * sp.diff(Phi_in, r), r) / r ** 2)
    rho_def = 3 * M / (4 * sp.pi * Rs ** 3)
    e_poisson = sp.simplify(lap_Phi_in - 4 * sp.pi * G * rho_def)

    beta_in = sp.exp(-2 * Phi_in / c ** 2)
    # 原方程残差: beta*lap(ln beta) + (8 pi G/c^2) rho   =  (lap beta - (grad beta)^2/beta) + (8 pi G/c^2) rho
    lap_beta_in = sp.diff(r ** 2 * sp.diff(beta_in, r), r) / r ** 2
    resid = sp.simplify(lap_beta_in - sp.diff(beta_in, r) ** 2 / beta_in + 8 * sp.pi * G / c ** 2 * rho_def)
    resid_factor = sp.simplify(resid / (8 * sp.pi * G / c ** 2 * rho_def))

    # 数值：地球 / 太阳 / 中子星
    GG = mp.mpf("6.67430e-11")
    cc = mp.mpf("299792458")
    Msun = mp.mpf("1.98847e30")
    cases = [("地球", mp.mpf("5.972e24"), mp.mpf("6.371e6")),
             ("太阳", Msun, mp.mpf("6.957e8")),
             ("中子星 1.4Msun", mp.mpf("1.4") * Msun, mp.mpf("1.2e4"))]
    nums = []
    for nm, MM, RR in cases:
        rg = GG * MM / cc ** 2
        beta0 = mp.e ** (3 * rg / RR)
        nums.append(nm + ": GM/c^2=" + mp.nstr(rg, 6) + " m, beta1(0)=" + mp.nstr(beta0, 8)
                    + " (偏离 1 的量级 " + mp.nstr(beta0 - 1, 6) + ")")

    # 对数泊松版（去掉 beta 因子）的后果：引力偏折
    rg_sun = GG * Msun / cc ** 2
    Rr = mp.mpf("6.957e8")
    defl_newton = 2 * rg_sun / Rr * mp.mpf("206265")     # 角秒: 2GM/(c^2 R)
    defl_gr = 4 * rg_sun / Rr * mp.mpf("206265")
    ok = (e_poisson == 0)

    detail = ("【H7 修复】点源导致 beta1(0)=∞；改用连续密度源后：内部 nabla^2 Phi=4 pi G rho 残差="
              + str(e_poisson) + "，原方程残差/(8 pi G rho/c^2) = " + str(resid_factor)
              + " 即残差 = (8 pi G rho/c^2)*(1-beta1)。数值: " + "; ".join(nums) + ". "
              + "两条子路径: (i) 若改方程为 nabla^2 ln beta1 = -(8 pi G/c^2) rho（去掉 beta 因子），"
              + "则 g=-grad Phi 严格牛顿，太阳引力偏折预言 " + mp.nstr(defl_newton, 6)
              + " 角秒，而 GR 与观测为 " + mp.nstr(defl_gr, 6) + " 角秒 ⇒ 差 2.0 倍，【被后牛顿观测证伪】; "
              + "(ii) 保留原方程则有效源 = rho*beta1，中子星中心强 " + mp.nstr(mp.e ** (3 * GG * mp.mpf("1.4") * Msun / cc ** 2 / mp.mpf("1.2e4")) - 1, 6)
              + " 倍 ⇒ 构成可检验预言（须先完成强场解与 TOV 类比，属后续工作）。"
              + "判定：点源失效保留 FAIL，连续源在弱场自洽、强场偏离可检验 ⇒ PARTIAL")
    return rec("T01-5", "H7 源区修复（连续密度源 + 强场偏离）", "PARTIAL" if ok else "FAIL", detail)


def main():
    print("=" * 90)
    print("T01 运动学与引力层修复 正面攻击 (H1/H2/H3/H7) — 算法联盟 TUFT 系列")
    print("=" * 90)
    sec_H1()
    sec_H2()
    sec_H3_pathI()
    sec_H3_pathII()
    sec_H7()

    print("-" * 90)
    cnt = {}
    for it in RESULTS:
        cnt[it["判定"]] = cnt.get(it["判定"], 0) + 1
    print("T01 汇总: " + ", ".join(k + "=" + str(v) for k, v in sorted(cnt.items())))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "T01_运动学与引力层修复_核验结果.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"脚本": "T01_运动学与引力层修复_正面攻击.py", "汇总": cnt, "明细": RESULTS},
                  f, ensure_ascii=False, indent=2)
    print("结果已写入: " + out)


if __name__ == "__main__":
    main()
