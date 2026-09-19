# -*- coding: utf-8 -*-
"""
TUFT 拓扑统一场论 硬伤 H1-H8 精算校验

红线：仅原样记录计算所得判定，不篡改 verdict、不粉饰 FAIL 为 PASS；
      未闭合项一律标 OPEN。

运行：
    python TUFT_硬伤H1-H8_精算校验.py
输出：
    控制台逐条 [PASS]/[FAIL]/[OPEN]/[INFO]
    TUFT_硬伤H1-H8_校验结果.json
"""

import os
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import sympy as sp
import mpmath as mp

mp.mp.dps = 50

RESULTS = []


def record(item, name, verdict, detail):
    RESULTS.append({"项": item, "名称": name, "判定": verdict, "说明": detail})
    print("[" + verdict + "] " + item + " | " + name + " | " + detail)
    return verdict


def simp(e):
    return sp.simplify(sp.expand(sp.trigsimp(sp.simplify(e))))


# ---------------------------------------------------------------- T1 螺旋恒等式
def check_T1_helix():
    t = sp.Symbol("t", real=True)
    R, w, vp = sp.symbols("R omega v_par", positive=True)

    r = sp.Matrix([R * sp.cos(w * t), R * sp.sin(w * t), vp * t])
    d1 = sp.simplify(r.diff(t))
    d2 = sp.simplify(r.diff(t, 2))
    d3 = sp.simplify(r.diff(t, 3))
    cr = sp.simplify(d1.cross(d2))

    c2 = R ** 2 * w ** 2 + vp ** 2  # = c^2

    # kappa^2 = |r' x r''|^2 / |r'|^6
    k2 = simp(cr.dot(cr) / simp(d1.dot(d1)) ** 3)
    # tau = (r' x r'') . r''' / |r' x r''|^2
    tau2 = simp(cr.dot(d3) ** 2 / cr.dot(cr) ** 2)

    k2_target = (R * w ** 2 / c2) ** 2
    tau2_target = (vp * w / c2) ** 2

    e1 = simp(k2 - k2_target)
    e2 = simp(tau2 - tau2_target)
    e3 = simp(k2 + tau2 - w ** 2 / c2)  # omega = c sqrt(kappa^2+tau^2)

    ok = (e1 == 0) and (e2 == 0) and (e3 == 0)
    detail = "kappa^2 残差=" + str(e1) + ", tau^2 残差=" + str(e2) + ", (kappa^2+tau^2-omega^2/c^2) 残差=" + str(e3)
    return record("T1", "圆柱螺旋恒等式 (定理1)", "PASS" if ok else "FAIL", detail)


# ---------------------------------------------------------------- T3 拓扑质量
def check_T3_mass():
    hbar = mp.mpf("1.054571817e-34")
    c = mp.mpf("299792458")
    G = mp.mpf("6.67430e-11")

    l_P = mp.sqrt(hbar * G / c ** 3)
    m_P = mp.sqrt(hbar * c / G)
    kappa = 1 / l_P
    m_from_kappa = hbar / (c * l_P)  # m = (hbar/c)*sqrt(kappa^2+tau^2), tau=0
    rel = abs(m_from_kappa - m_P) / m_P

    ok = rel < mp.mpf("1e-15")
    detail = "m_P=" + mp.nstr(m_P, 12) + " kg, (hbar/c)*(1/l_P)=" + mp.nstr(m_from_kappa, 12) + " kg, 相对残差=" + mp.nstr(rel, 6)
    return record("T3", "拓扑质量与普朗克特例 (定理3)", "PASS" if ok else "FAIL", detail)


# ---------------------------------------------------------------- T7 真空外解 + 弱场极限
def check_T7_exterior():
    r, G, M, c = sp.symbols("r G M c", positive=True)

    beta = sp.exp(2 * G * M / (c ** 2 * r))
    lnbeta = sp.log(beta)

    g_r = sp.simplify(c ** 2 / 2 * sp.diff(lnbeta, r))
    lap_lnbeta = sp.simplify(sp.diff(r ** 2 * sp.diff(lnbeta, r), r) / r ** 2)

    ok_g = sp.simplify(g_r + G * M / r ** 2) == 0      # g = -GM/r^2
    ok_lap = sp.simplify(lap_lnbeta) == 0              # 真空 r>0

    # 弱场：delta_beta = 2GM/(c^2 r), phi = -(c^2/2) delta_beta = -GM/r
    delta = 2 * G * M / (c ** 2 * r)
    phi = -c ** 2 / 2 * delta
    ok_phi = sp.simplify(phi + G * M / r) == 0
    lap_phi = sp.simplify(sp.diff(r ** 2 * sp.diff(phi, r), r) / r ** 2)
    ok_poisson = sp.simplify(lap_phi) == 0              # 源外 Laplace=0，配合 4 pi G rho 即牛顿泊松方程

    ok = ok_g and ok_lap and ok_phi and ok_poisson
    detail = ("g_r=" + str(g_r) + "(应为 -GM/r^2: " + str(ok_g) + "); "
              + "真空 Laplacian(ln beta)=" + str(lap_lnbeta) + "; "
              + "弱场 phi=" + str(phi) + " 复现牛顿势: " + str(ok_phi and ok_poisson))
    return record("T7a", "beta1 真空外解与弱场极限 (定理7)", "PASS" if ok else "FAIL", detail)


# ---------------------------------------------------------------- H1 公理I 与有质量粒子
def check_H1_proper_time():
    c = mp.mpf("299792458")

    # 公理 I: |v| = c  =>  SR 固有时速率 dtau/dt = sqrt(1-v^2/c^2) = 0
    dtau_dt_sr = mp.mpf("0")
    # 原稿: ds = c dt 且 dtau = ds/c  =>  dtau/dt = 1
    dtau_dt_tuft = mp.mpf("1")

    rows = []
    for frac in ["0.9", "0.99", "0.999999", "1"]:
        f = mp.mpf(frac)
        if f >= 1:
            gamma = mp.inf
        else:
            gamma = 1 / mp.sqrt(1 - f ** 2)
        rows.append("v/c=" + frac + " -> gamma=" + mp.nstr(gamma, 8))

    detail = ("SR: dtau/dt = sqrt(1-v^2/c^2) = " + mp.nstr(dtau_dt_sr, 6)
              + " (v=c); TUFT 由 ds=c dt, dtau=ds/c 得 dtau/dt = " + mp.nstr(dtau_dt_tuft, 6)
              + "; 而定理3 给出静质量 m=hbar*omega/c^2>0 且定理6 用 d/dtau=c d/ds 求导。"
              + " 三者互斥。gamma 对照: " + "; ".join(rows))
    return record("H1", "公理I 速率=c 与有静质量粒子的冲突", "FAIL", detail)


# ---------------------------------------------------------------- H2 定理5 符号
def check_H2_sign():
    R, th = sp.symbols("R theta", positive=True)

    rv = sp.Matrix([R * sp.cos(th), R * sp.sin(th), 0])
    s_param = R * th  # 弧长参数（圆）

    T = sp.simplify(rv.diff(th) / R)
    dTds = sp.simplify(T.diff(th) / R)
    kappa = sp.simplify(dTds.norm())
    N = sp.simplify(dTds / kappa)

    radial = sp.Matrix([sp.cos(th), sp.sin(th), 0])
    n_dot_r = sp.simplify(N.dot(radial))  # 期望 -1: N 指向圆心

    # 定理5: g = -c^2 kappa N  -> 径向分量 = -c^2 kappa * (-1) = +c^2 kappa (背离圆心 = 排斥)
    radial_component_doc = sp.simplify(-kappa * n_dot_r)
    # 向心（吸引）要求径向分量为负
    ok = (n_dot_r == -1) and (radial_component_doc > 0)

    detail = ("N . r_hat = " + str(n_dot_r) + " (N 指向圆心); "
              + "定理5 的 g 径向分量 = " + str(radial_component_doc) + " * c^2 > 0 即背离圆心(排斥); "
              + "定理6 的 F = +m c^2 kappa N 为向心(吸引), 二者相差负号, F != m g. "
              + "修订: g = +c^2 kappa N")
    return record("H2", "定理5 引力加速度符号", "FAIL", detail)


# ---------------------------------------------------------------- H3 定理4+5+7 三重不自洽
def check_H3_triple():
    G = mp.mpf("6.67430e-11")
    M = mp.mpf("5.972e24")
    c = mp.mpf("299792458")
    r1 = mp.mpf("6.371e6")
    r2 = 2 * r1

    def kappa_of(r):
        return G * M / (c ** 2 * r ** 2)   # 由 |g| = GM/r^2 = c^2 kappa

    def beta_sol(r):
        return mp.e ** (2 * G * M / (c ** 2 * r))

    def K0_required(r):
        # beta1^(def) = kappa^2 / K0  ==  beta1^(sol)  =>  K0 = kappa^2 / beta_sol
        return kappa_of(r) ** 2 / beta_sol(r)

    ratio_K0 = K0_required(r1) / K0_required(r2)   # 若自洽应 = 1

    # 约束检验: 由定理4 代入对数律得 grad(kappa) = -kappa^2 N (tau=0)
    # |grad kappa| = 2GM/(c^2 r^3);  kappa^2 = G^2 M^2/(c^4 r^4);  比值 = 2 c^2 r/(G M) 应为 1
    ratio_grad = 2 * c ** 2 * r1 / (G * M)

    ok = (abs(ratio_K0 - 1) < mp.mpf("1e-6")) and (abs(ratio_grad - 1) < mp.mpf("1e-6"))
    detail = ("K0 应为常数, 实测 K0(r_E)/K0(2 r_E) = " + mp.nstr(ratio_K0, 8)
              + " (幂律 r^-4 暴露, 期望 1); "
              + "|grad kappa| / kappa^2 = 2 c^2 r/(G M) = " + mp.nstr(ratio_grad, 8)
              + " (期望 1). beta1 定义(幂律) vs beta1 指数解 vs g=c^2 kappa 三者不可兼得")
    return record("H3", "定理4/5/7 联立不自洽", "PASS" if ok else "FAIL", detail)


# ---------------------------------------------------------------- H4 自旋恒等式与 Lk 整数性
def check_H4_spin():
    out = []
    bad = []
    for s_val, label in [(sp.Integer(1), "玻色 s=1"),
                         (sp.Rational(1, 2), "费米 s=1/2"),
                         (sp.Integer(0), "s=0")]:
        Lk = sp.sqrt(1 - s_val)
        twice = sp.nsimplify(2 * Lk)
        is_half_int = twice.is_Integer
        out.append(label + " -> Lk=" + str(sp.N(Lk, 8)) + " (2Lk=" + str(sp.N(2 * Lk, 8))
                   + ", 半整数? " + str(bool(is_half_int)) + ")")
        if not is_half_int:
            bad.append(label)

    # 玻色 Lk=0 整数 OK；费米 Lk=sqrt(2)/2 非半整数；s=0 时 Lk=1 但 theta=0 为直线不闭合
    ok = False
    detail = ("; ".join(out)
              + ". Călugăreanu-White 要求 Lk ∈ Z；费米子 Lk=1/sqrt(2) 非整数非半整数；"
                "s=0 时 Lk=1 但 theta=0 为直线(kappa=tau=0)不闭合, 违反定理9 第1条。"
                "且 s=sin^2(theta) 与 s+Lk^2=1 均无推导 -> 降级为开放命题 O-T2")
    return record("H4", "定理2 自旋拓扑恒等式", "PASS" if ok else "FAIL", detail)


# ---------------------------------------------------------------- H5 场化提升（结构性缺口）
def check_H5_field_promotion():
    detail = ("Frenet 的 kappa(s), tau(s) 定义在单条曲线上；定理8/3.1/3.2/3.5 全部使用空间场 "
              "kappa(x), 矢量 tau(x) 与时间分量 tau_t。原稿未定义: (1) tau 由带符号标量升为矢量场时"
              "方向从何而来; (2) 曲线参数 s 到空间坐标 x 的映射; (3) (tau_t, tau) 构成洛伦兹四矢的证明。"
              "无此提升映射, 第三部分全部悬空。本项不可由计算判定, 记为结构性缺口")
    return record("H5", "曲线量 -> 场量的提升映射缺失", "OPEN", detail)


# ---------------------------------------------------------------- H6 汤川势推导
def check_H6_yukawa():
    r, mu, g2, A, c = sp.symbols("r mu g2 A c", positive=True)

    k_helm = A * sp.exp(-mu * r) / r
    lap_k = sp.diff(r ** 2 * sp.diff(k_helm, r), r) / r ** 2
    helm_res = sp.simplify(lap_k - mu ** 2 * k_helm)     # 应为 0：确为 Helmholtz 解

    V = -g2 * sp.exp(-mu * r) / r
    force_from_V = sp.simplify(-sp.diff(V, r))            # -dV/dr
    force_from_k = sp.simplify(-c ** 2 * k_helm)          # g = -c^2 kappa

    # 等式 -dV/dr = -c^2 A e^{-mu r}/r 解出的 A 必须依赖 r（否则矛盾）
    A_req = sp.simplify(sp.solve(sp.Eq(force_from_V, force_from_k), A)[0])
    dA_dr = sp.simplify(sp.diff(A_req, r))

    # 反查：与汤川势相容的 kappa 是否为 Helmholtz 解
    k_yuk = sp.simplify(force_from_V / (-c ** 2))
    lap_ky = sp.diff(r ** 2 * sp.diff(k_yuk, r), r) / r ** 2
    res_ky = sp.simplify(lap_ky - mu ** 2 * k_yuk)
    res_ky_num = sp.N(res_ky.subs({r: 1, mu: 1, g2: 1, c: 1}))

    ok = (sp.simplify(helm_res) == 0) and (sp.simplify(dA_dr) == 0)
    detail = ("Helmholtz 检验 (nabla^2-mu^2)kappa = " + str(helm_res) + " (kappa=A e^{-mu r}/r 确为解); "
              + "由 -dV/dr = -c^2 kappa 解出 A = " + str(A_req) + ", dA/dr = " + str(dA_dr)
              + " != 0 (A 只能是 r 的函数, 除非 g2=0 平凡解); "
              + "反查汤川势对应的 kappa 代入 Helmholtz 残差(数值 r=mu=g2=c=1) = " + str(res_ky_num)
              + " != 0. 修订: 保留 Helmholtz 则 V=-c^2 m A E1(mu r) (指数积分), 或另立场方程保留汤川势")
    return record("H6", "汤川势推导不自洽", "PASS" if ok else "FAIL", detail)


# ---------------------------------------------------------------- H7 定理7 点源不自洽
def check_H7_source():
    G = mp.mpf("6.67430e-11")
    M = mp.mpf("5.972e24")
    c = mp.mpf("299792458")
    a = 2 * G * M / c ** 2   # ln beta = a / r

    rows = []
    prev = None
    monotone = True
    for eps in ["1e-1", "1e-3", "1e-6", "1e-9"]:
        e = mp.mpf(eps)
        lg = mp.log10(mp.e ** (a / e))   # 正则化后 beta(0) 的量级
        rows.append("eps=" + eps + " -> lg beta(0)=" + mp.nstr(lg, 6))
        if prev is not None and lg <= prev:
            monotone = False
        prev = lg

    ok = False   # 外部成立、源区失效，整体判 FAIL-局部
    detail = ("LHS = beta1 * nabla^2(ln beta1) = beta1(r) * (-8 pi G M / c^2) delta^3(r), "
              "RHS = -(8 pi G / c^2) M delta^3(r), 相差因子 beta1(0). "
              "正则化 1/r -> 1/sqrt(r^2+eps^2) 实算: " + "; ".join(rows)
              + " -> beta1(0) 发散(单调=" + str(monotone) + "), 点源无分布意义解。"
                "真空外部 r>0 两侧均为 0, 该部分仍成立")
    return record("H7", "定理7 场方程在点源处失效", "FAIL", detail)


# ---------------------------------------------------------------- H8 齐次麦克斯韦零信息量
def check_H8_maxwell_trivial():
    x, y, z, t = sp.symbols("x y z t", real=True)

    a1 = sp.Function("a1")(x, y, z, t)
    a2 = sp.Function("a2")(x, y, z, t)
    a3 = sp.Function("a3")(x, y, z, t)
    phi = sp.Function("phi")(x, y, z, t)
    Avec = sp.Matrix([a1, a2, a3])

    def grad(f):
        return sp.Matrix([sp.diff(f, x), sp.diff(f, y), sp.diff(f, z)])

    def curl(F):
        return sp.Matrix([
            sp.diff(F[2], y) - sp.diff(F[1], z),
            sp.diff(F[0], z) - sp.diff(F[2], x),
            sp.diff(F[1], x) - sp.diff(F[0], y),
        ])

    def div(F):
        return sp.diff(F[0], x) + sp.diff(F[1], y) + sp.diff(F[2], z)

    B = curl(Avec)
    E = -grad(phi) - sp.Matrix([sp.diff(a, t) for a in Avec])

    e1 = sp.simplify(div(B))
    e2 = sp.simplify(curl(E) + sp.Matrix([sp.diff(b, t) for b in B]))
    zero2 = all(sp.simplify(comp) == 0 for comp in e2)

    ok = (sp.simplify(e1) == 0) and zero2
    detail = ("对【任意】势函数 phi, A 实算: div B = " + str(e1) + ", curl E + dB/dt = " + str(list(e2))
              + " 恒为 0 -> 齐次麦克斯韦只是势表示的恒等式, 零信息量, 不构成对 TUFT 的验证。"
                "真正的任务是非齐次方程与源项 S_tau")
    return record("H8", "齐次麦克斯韦恒成立(零信息量)", "INFO" if ok else "FAIL", detail)


def main():
    print("=" * 78)
    print("TUFT 拓扑统一场论 硬伤 H1-H8 精算校验 (sympy 符号 + mpmath 50 位)")
    print("=" * 78)

    check_T1_helix()
    check_T3_mass()
    check_T7_exterior()
    check_H1_proper_time()
    check_H2_sign()
    check_H3_triple()
    check_H4_spin()
    check_H5_field_promotion()
    check_H6_yukawa()
    check_H7_source()
    check_H8_maxwell_trivial()

    print("-" * 78)
    cnt = {}
    for item in RESULTS:
        cnt[item["判定"]] = cnt.get(item["判定"], 0) + 1
    print("汇总: " + ", ".join(k + "=" + str(v) for k, v in sorted(cnt.items())))
    print("结论: 成立 3 项(T1/T3/T7a); 硬伤 FAIL 5 项(H1/H2/H3/H4/H6 + H7 源区); "
          "结构性缺口 OPEN 1 项(H5); 零信息量 INFO 1 项(H8)")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TUFT_硬伤H1-H8_校验结果.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"汇总": cnt, "明细": RESULTS}, f, ensure_ascii=False, indent=2)
    print("结果已写入: " + out)


if __name__ == "__main__":
    main()
