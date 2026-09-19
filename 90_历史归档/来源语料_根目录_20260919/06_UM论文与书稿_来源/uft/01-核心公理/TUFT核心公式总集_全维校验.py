# -*- coding: utf-8 -*-
"""
TUFT(Topological Unified Field Theory)核心公式总集 全维校验
==========================================================
对象：《TUFT 拓扑统一场论｜完整正确核心公式与理论总集》(v2)
姊妹文档：TUFT_核心公式总集与全维审计_v2.md（同目录）
上游：本源拓扑统一场论.md（v1）、O9导出_麦克斯韦_薛定谔_汤川.md（G1-G4 裁定）

判定口径（沿用 O9 脚本）：
  PASS = 声称成立且符号/数值残差为 0
  FAIL = 残差非零 / 体系内部矛盾 / 推导链断裂（真缺陷，必须改）
  OPEN = 需要外部物理输入，本体系不可导出（诚实边界，不是 bug）
  WARN = 编辑层缺陷（符号冲突、分级越权、与上游裁定不一致）

依赖：Python 3 + sympy
"""

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import sympy as sp

RESULTS = []


def record(cid, title, verdict, detail=""):
    if not isinstance(verdict, str):
        verdict = "PASS" if bool(verdict) else "FAIL"
    RESULTS.append((cid, title, verdict, detail))
    line = "[" + verdict + "] " + cid + " " + title
    if detail:
        line = line + "  |  " + str(detail)
    print(line)


def section(name):
    print("")
    print("=== " + name + " ===")


class Dim(object):
    """四维量纲 (M, L, T, I)"""

    def __init__(self, M=0, L=0, T=0, I=0):
        self.v = (M, L, T, I)

    def __mul__(self, o):
        return Dim(*[a + b for a, b in zip(self.v, o.v)])

    def __truediv__(self, o):
        return Dim(*[a - b for a, b in zip(self.v, o.v)])

    def __rtruediv__(self, o):
        if isinstance(o, (int, float)):
            return Dim(*[-a for a in self.v])
        return NotImplemented

    def __rmul__(self, o):
        return self.__mul__(o)

    def __pow__(self, n):
        return Dim(*[a * n for a in self.v])

    def __eq__(self, o):
        return tuple(self.v) == tuple(o.v)

    def __hash__(self):
        return hash(self.v)

    def __repr__(self):
        return "Dim(M=" + str(self.v[0]) + ",L=" + str(self.v[1]) + \
               ",T=" + str(self.v[2]) + ",I=" + str(self.v[3]) + ")"


MAS = Dim(M=1)
LEN = Dim(L=1)
TIM = Dim(T=1)
DIMLESS = Dim()
VEL = LEN / TIM
ACC = LEN / TIM ** 2
FOR = MAS * ACC
ENE = MAS * LEN ** 2 / TIM ** 2

C = sp.Float("299792458")
HBAR = sp.Float("1.054571817e-34")
GG = sp.Float("6.67430e-11")
M_E = sp.Float("9.1093837015e-31")
M_PION = sp.Float("2.48832e-28")


def fnum(x, n=6):
    return sp.N(x, n)


# ============================================================
# A. Frenet-Serret 标架 / 圆柱螺旋 / Darboux
# ============================================================
def sec_A():
    section("A. Frenet-Serret 标架 / 圆柱螺旋 / Darboux（公理Ⅱ + 定理1）")

    t = sp.symbols("t", real=True)
    R, w, hh = sp.symbols("R omega h", positive=True)
    c2 = R ** 2 * w ** 2 + hh ** 2
    cs = sp.sqrt(c2)

    rv = sp.Matrix([R * sp.cos(w * t), R * sp.sin(w * t), hh * t])
    r1 = rv.diff(t)
    r2 = rv.diff(t, 2)
    r3 = rv.diff(t, 3)
    cr = r1.cross(r2)

    kap = sp.simplify(sp.trigsimp(cr.norm() / r1.norm() ** 3))
    tau = sp.simplify(sp.trigsimp(cr.dot(r3) / cr.dot(cr)))

    record("A1", "kappa = R*omega^2/c^2", sp.simplify(kap - R * w ** 2 / c2) == 0,
           "kappa=" + str(kap))
    record("A2", "tau = h*omega/c^2", sp.simplify(tau - hh * w / c2) == 0,
           "tau=" + str(tau))
    record("A3", "omega = c*sqrt(kappa^2+tau^2)",
           sp.simplify(sp.trigsimp(cs * sp.sqrt(kap ** 2 + tau ** 2) - w)) == 0)
    record("A4", "tan(theta) = kappa/tau = v_perp/h",
           sp.simplify(kap / tau - R * w / hh) == 0)

    Tv = sp.simplify(r1 / cs)
    Nv = sp.simplify(r2 / sp.sqrt(sp.trigsimp(r2.dot(r2))))
    Bv = sp.simplify(Tv.cross(Nv))
    norms_ok = (sp.simplify(sp.trigsimp(Tv.dot(Tv)) - 1) == 0
                and sp.simplify(sp.trigsimp(Nv.dot(Nv)) - 1) == 0
                and sp.simplify(sp.trigsimp(Bv.dot(Bv)) - 1) == 0)
    orth_ok = (sp.simplify(sp.trigsimp(Tv.dot(Nv))) == 0
               and sp.simplify(sp.trigsimp(Nv.dot(Bv))) == 0
               and sp.simplify(sp.trigsimp(Bv.dot(Tv))) == 0)
    record("A5", "Frenet 标架单位正交 {T,N,B}", norms_ok and orth_ok,
           "N = (-cos, -sin, 0)：指向曲率中心（螺旋轴）")

    Om = sp.simplify(tau * Tv + kap * Bv)

    def d_ds(M):
        return sp.simplify(M.diff(t) / cs)

    record("A6", "dT/ds = Omega_D x T",
           sp.simplify(sp.trigsimp((d_ds(Tv) - Om.cross(Tv)).norm())) == 0)
    record("A7", "dN/ds = Omega_D x N (= -kappa T + tau B)",
           sp.simplify(sp.trigsimp((d_ds(Nv) - Om.cross(Nv)).norm())) == 0)
    record("A8", "dB/ds = Omega_D x B (= -tau N)",
           sp.simplify(sp.trigsimp((d_ds(Bv) - Om.cross(Bv)).norm())) == 0)
    record("A9", "|Omega_D| = sqrt(kappa^2+tau^2) = omega/c",
           sp.simplify(sp.trigsimp(Om.dot(Om) - (kap ** 2 + tau ** 2))) == 0,
           "频率 = 标架自转率 x c（O9-1 第二证明）")

    acc_ref = sp.simplify(c2 * kap * Nv)
    same = sp.simplify(sp.trigsimp((r2 - acc_ref).norm())) == 0
    record("A10", "加速度 a = +c^2 kappa N（沿主法向，指向曲率中心）", same,
           "a = " + str(sp.simplify(r2.T)))
    record("A11", "定理5 写 g = -c^2 kappa N 的符号", "FAIL" if same else "OPEN",
           "A10 证明 a 沿 +N；-c^2 kappa N 背离曲率中心 = 斥力，"
           "且与定理6 首项 +m c^2 kappa N 直接矛盾")


# ============================================================
# B. 定理2 拓扑自旋
# ============================================================
def sec_B():
    section("B. 定理2 拓扑自旋 s + Lk^2 = 1（与 O9 G3 裁定对齐）")

    record("B1", "s=sin^2(theta), Lk^2=cos^2(theta) 的代数恒等式", "PASS",
           "作为定义自洽；但 Calugareanu-White 只有 Lk=Tw+Wr（线性），不含 s+Lk^2=1")
    record("B2", "玻色孤子 theta=90deg -> Lk=0 为整数",
           sp.simplify(sp.cos(sp.pi / 2)) == 0, "Lk=0 属于 Z，OK")
    record("B3", "费米孤子 theta=45deg -> Lk=cos45 是否为整数", "FAIL",
           "Lk=" + str(sp.N(sp.cos(sp.pi / 4), 10))
           + " 非整数；闭合纽结要求 Lk 属于 Z（O9 G3 同裁定）")
    th = sp.asin(sp.sqrt(sp.Rational(3, 4)))
    record("B4", "若要 Lk=1/2（费米自旋），则 theta=60deg, kappa/tau=sqrt(3)", "FAIL",
           "与定理2「费米孤子 kappa=tau」矛盾；kappa/tau = " + str(sp.simplify(sp.tan(th))))
    record("B5", "v2 第五部分仍把定理2 列入「严格由三大公理证明」", "WARN",
           "与 O9 G3 裁定冲突，应降级为「定义 + 输入假设」，Lk 整数性登记为开放项")


# ============================================================
# C. 定理3 拓扑质量
# ============================================================
def sec_C():
    section("C. 定理3 拓扑质量 m = (hbar/c) sqrt(kappa^2+tau^2)")

    kap, tau = sp.symbols("kappa tau", positive=True)
    expr = sp.simplify(HBAR * C * sp.sqrt(kap ** 2 + tau ** 2) / C ** 2
                       - (HBAR / C) * sp.sqrt(kap ** 2 + tau ** 2))
    record("C1", "m=(hbar/c)sqrt(k^2+t^2) 与 mc^2=hbar*omega 自洽", expr == 0)

    kappa_tot = M_E * C / HBAR
    kap_e = kappa_tot / sp.sqrt(2)
    m_back = (HBAR / C) * sp.sqrt(2 * kap_e ** 2)
    rel = sp.N(abs(m_back - M_E) / M_E, 8)
    record("C2", "电子（费米孤子 kappa=tau）质量往返", rel < sp.Float("1e-12"),
           "kappa=tau=" + str(fnum(kap_e)) + " m^-1，曲率半径=" + str(fnum(1 / kap_e))
           + " m，相对残差=" + str(rel))

    l_P = sp.sqrt(HBAR * GG / C ** 3)
    m_P = sp.sqrt(HBAR * C / GG)
    m_k = (HBAR / C) * (1 / l_P)
    record("C3", "玻色普朗克孤子（tau=0, kappa=1/l_P）复现 m_Pl",
           sp.N(abs(m_k - m_P) / m_P, 12) < sp.Float("1e-12"),
           "m(kappa)=" + str(fnum(m_k)) + " kg，m_Pl=" + str(fnum(m_P)) + " kg")

    lam_C = HBAR / (M_E * C)
    record("C4", "约化康普顿波长 = 1/sqrt(kappa^2+tau^2)",
           sp.N(abs(1 / kappa_tot - lam_C) / lam_C, 12) < sp.Float("1e-12"),
           "lambda_C_bar=" + str(fnum(lam_C)) + " m")


# ============================================================
# D. 定理4 / 5 / 7 引力链
# ============================================================
def sec_D():
    section("D. 定理4(beta_1) / 定理5(g) / 定理7(场方程)")

    r, GM, cc = sp.symbols("r GM c", positive=True)

    record("D1", "beta_1=(kappa^2+tau^2)/<kappa_0^2+tau_0^2> 的方向", "PASS",
           "真空=1；近质量升高 -> beta_1>1；v2 已修正 v1 稿被 O9 G1/G2 否定的反向定义")

    f = sp.Function("f")(r)
    lap_f = sp.diff(r ** 2 * sp.diff(f, r), r) / r ** 2
    lhs = sp.simplify(f * sp.diff(r ** 2 * sp.diff(sp.log(f), r), r) / r ** 2)
    rhs = sp.simplify(lap_f - sp.diff(f, r) ** 2 / f)
    record("D2", "恒等式 beta1*lap(ln beta1) = lap(beta1) - (grad beta1)^2/beta1",
           sp.simplify(lhs - rhs) == 0)

    beta = sp.exp(2 * GM / (cc ** 2 * r))
    lap_b = sp.diff(r ** 2 * sp.diff(beta, r), r) / r ** 2
    resid = sp.simplify(lap_b - sp.diff(beta, r) ** 2 / beta)
    record("D3", "beta_1=exp(2GM/(c^2 r)) 满足真空场方程 (r>0)", resid == 0,
           "残差=" + str(resid))

    g_r = sp.simplify(cc ** 2 / 2 * sp.diff(sp.log(beta), r))
    record("D4", "g=(c^2/2) d(ln beta1)/dr = -GM/r^2（吸引）",
           sp.simplify(g_r + GM / r ** 2) == 0, "g_r=" + str(g_r))

    div_g = sp.simplify(sp.diff(r ** 2 * g_r, r) / r ** 2)
    record("D5", "真空区 div g = 0（弱场 -> 泊松 div g = -4 pi G rho_m）", div_g == 0,
           "弱场 ln beta1 = -2 phi_N/c^2，与牛顿势精确对应")
    record("D6", "场方程源项 -(8 pi G/c^2) rho_m 的第一性来源", "OPEN",
           "由牛顿极限反定（O9 G4）；强场点源处 beta1->inf 相容性未闭合")

    l_P = sp.sqrt(HBAR * GG / C ** 3)
    g5_vac = sp.N(C ** 2 / l_P, 6)
    record("D7", "定理5 |g|=c^2 kappa 的真空极限", "FAIL",
           "kappa -> kappa0 ≠ 0，取真空孤子 kappa0=1/l_Pl 则 |g|=" + str(g5_vac)
           + " m/s^2；而定理7 的 g=(c^2/2)grad ln beta1 -> 0。真空极限直接冲突")

    record("D8", "定理4+7 反解 kappa(r) 与 定理5+牛顿 kappa_N(r) 的函数形式", "FAIL",
           "kappa_beta = sqrt(K0) exp(GM/(c^2 r)) 弱场 ≈ sqrt(K0)(1 + GM/(c^2 r))，"
           "相对扰动 ~ 1/r；定理5+牛顿要求 kappa_N = GM/(c^2 r^2) ~ 1/r^2。"
           "差一个 r 的幂次，不可能同时成立")

    M_EA = sp.Float("5.972e24")
    R_EA = sp.Float("6.371e6")
    vals = []
    for rr in [sp.Float("6.371e6"), sp.Float("1.2742e7"),
               sp.Float("6.371e7"), sp.Float("6.371e8")]:
        kb = 1 + GG * M_EA / (C ** 2 * rr)
        kn = GG * M_EA / (C ** 2 * rr ** 2)
        vals.append(sp.N(kb / kn, 8))
    record("D9", "数值：弱场 kappa_beta/kappa_Newt 随 r^2 增长（地球）", "FAIL",
           "r/R_E = 1,2,10,100 -> " + ", ".join([str(v) for v in vals])
           + "（趋势 ~ r^2，非定标可吸收）")


# ============================================================
# E. 定理6 统一动力学
# ============================================================
def sec_E():
    section("E. 定理6 F = m c^2 kappa N + m c^2 tau B（推导链审计）")

    s = sp.Symbol("s")
    kap = sp.Function("kappa")(s)
    tau = sp.Function("tau")(s)
    m = sp.Symbol("m", positive=True)
    T_ = sp.Matrix(sp.symbols("T1 T2 T3"))
    N_ = sp.Matrix(sp.symbols("N1 N2 N3"))
    B_ = sp.Matrix(sp.symbols("B1 B2 B3"))

    F_p = C ** 2 * m * (kap * N_)
    has_tau = any(sp.diff(F_p[i], tau) != 0 for i in range(3))
    record("E1", "由 p=mcT 对固有时求导能否得到 m c^2 tau B 项", "FAIL",
           "d(mcT)/dtau_prop = c·mc·dT/ds = m c^2 kappa N；"
           "Frenet 第一式不含 tau（tau 只出现在 dN/ds 的 +tauB 与 dB/ds 的 -tauN）。"
           "含 tau 项=" + str(has_tau) + " -> 推导链断裂")

    S = sp.Symbol("S", positive=True)
    F_c = C ** 2 * (m * (kap * N_) + S * (-kap * T_ + tau * B_))
    has_tau2 = any(sp.diff(F_c[i], tau) != 0 for i in range(3))
    record("E2", "候选修复：p = mcT + S·N 可产生 tau·B 项", "PASS" if has_tau2 else "FAIL",
           "F = m c^2 kappa N + S c^2(-kappa T + tau B)：tau·B 确实出现，"
           "但附带 -S c^2 kappa T 切向分量，需额外约束消去（候选，未闭合）")

    kap_e = (M_E * C / HBAR) / sp.sqrt(2)
    F_int = sp.N(M_E * C ** 2 * kap_e, 6)
    record("E3", "力层级 F_kappa/F_tau = kappa/tau（费米孤子 = 1）", "OPEN",
           "若两项分别对应引力与电磁力，强度比为 1，与实测 ~10^42 差 42 个量级。"
           "|F| = m c^2 kappa = " + str(F_int)
           + " N 是电子康普顿尺度内禀力，与宏观四力强度的对应本体系未建立")
    record("E4", "定理6 首项与定理5 的符号一致性", "FAIL",
           "定理6 为 +m c^2 kappa N，定理5 为 -c^2 kappa N：同一物理量符号相反")


# ============================================================
# F. 3.1 / 3.2 电磁映射
# ============================================================
def sec_F():
    section("F. 3.1-3.2 电磁映射与能量动量张量")

    x, y, z, tt = sp.symbols("x y z t", real=True)
    coords = [x, y, z]
    k = sp.symbols("k", positive=True)
    tau_t = sp.Function("tau_t")(x, y, z, tt)
    tv = [sp.Function("tau_" + str(i))(x, y, z, tt) for i in range(3)]

    E = [-k * (C * sp.diff(tau_t, coords[i]) + sp.diff(tv[i], tt)) for i in range(3)]
    Bf = [k * (sp.diff(tv[2], y) - sp.diff(tv[1], z)),
          k * (sp.diff(tv[0], z) - sp.diff(tv[2], x)),
          k * (sp.diff(tv[1], x) - sp.diff(tv[0], y))]

    divB = sp.simplify(sum(sp.diff(Bf[i], coords[i]) for i in range(3)))
    record("F1", "div B = 0（由 B = k curl(tau) 自动满足）", divB == 0)

    curlE = [sp.diff(E[2], y) - sp.diff(E[1], z),
             sp.diff(E[0], z) - sp.diff(E[2], x),
             sp.diff(E[1], x) - sp.diff(E[0], y)]
    far = [sp.simplify(curlE[i] + sp.diff(Bf[i], tt)) for i in range(3)]
    record("F2", "curl E + dB/dt = 0（Faraday，由势定义自动满足）",
           all(v == 0 for v in far))

    record("F3", "能量密度与 Maxwell 应力张量形式", "PASS",
           "与标准电动力学逐项一致（形式映射，非导出）")
    record("F4", "符号冲突：B 既表 Frenet 副法向（公理Ⅱ）又表磁场（3.1）", "WARN",
           "同文档内 B 双重身份；建议磁场改记 B_em 或 mathcal{B}")
    record("F5", "A_mu 的几何构造 / eps_tau, mu_tau, k 的定标", "OPEN",
           "A ∝ tau 是 ansatz（O9 假设 C）；"
           "非齐次麦克斯韦与 eps_0/e/alpha 不可由三公理导出（O9 / O15）")


# ============================================================
# G. 3.3 汤川核力势
# ============================================================
def sec_G():
    section("G. 3.3 汤川核力势（v2 推导链审计）")

    r, mu, A, g2, cc = sp.symbols("r mu A g2 c", positive=True)

    kap_h = A * sp.exp(-mu * r) / r
    lap = sp.diff(r ** 2 * sp.diff(kap_h, r), r) / r ** 2
    record("G1", "kappa=A e^{-mu r}/r 满足 (lap - mu^2)kappa = 0 (r>0)",
           sp.simplify(lap - mu ** 2 * kap_h) == 0)

    V = -g2 * sp.exp(-mu * r) / r
    F_r = sp.simplify(-sp.diff(V, r))
    record("G2", "V=-g2 e^{-mu r}/r -> F_r = -g2 e^{-mu r}(mu/r + 1/r^2)（吸引）",
           sp.simplify(F_r + g2 * sp.exp(-mu * r) * (mu / r + 1 / r ** 2)) == 0,
           "F_r=" + str(F_r))

    g_claim = -cc ** 2 * kap_h
    ratio = sp.simplify(F_r / g_claim)
    record("G3", "桥接 g_r = -c^2 kappa(r) 与 V=-g2 e^{-mu r}/r 是否相容", "FAIL",
           "F_r / (-c^2 kappa) = " + str(ratio)
           + "，含 (mu + 1/r) 随 r 变化，无法由常数 A、g2 同时满足")

    kap_y = (g2 / cc ** 2) * sp.exp(-mu * r) * (mu / r + 1 / r ** 2)
    lap_y = sp.diff(r ** 2 * sp.diff(kap_y, r), r) / r ** 2
    resid_y = sp.simplify(lap_y - mu ** 2 * kap_y)
    record("G4", "汤川势所要求的 kappa_Y 是否满足 (lap-mu^2)kappa=0", "FAIL",
           "残差 = " + str(resid_y)
           + " 非零 -> 「Helmholtz 解 + g_r=-c^2 kappa ⇒ 汤川势」不能同时成立")

    lam_pi = sp.N(HBAR / (M_PION * C), 8)
    record("G5", "O9 已闭合路径：(lap-mu^2)phi=-g delta^3, V=-(g^2/4pi)e^{-mu r}/r",
           "PASS", "力程 1/mu = hbar/(m_pi c) = " + str(lam_pi)
           + " m，与经验核力力程 ~1.4 fm 相差约 1%；v2 应改用此版本")


# ============================================================
# H. 3.4 / 3.5 + 结构性张力 + 量纲表
# ============================================================
def sec_H():
    section("H. 3.4-3.5 量子/波动框架与结构性张力")

    record("H1", "(Box + kappa^2+tau^2)psi=0 的色散关系", "PASS",
           "omega^2 = c^2 k^2 + c^2(kappa^2+tau^2)，即 KG 色散（O9 D2 已 PASS）")
    record("H2", "公理Ⅰ v_perp^2+h^2=c^2 的世界线类光性", "FAIL",
           "空间速率恒为 c ⇒ 时空间隔 c^2dt^2-|dx|^2 = 0 ⇒ 固有时恒为 0；"
           "而体系又用 dtau=ds/c 作演化参数求导（定理6）。二者不相容，"
           "须明确 s 是空间弧长还是时空弧长（承接 O7）")
    record("H3", "3.5 波动方程源项 S_kappa, S_tau", "OPEN",
           "量纲要求 [S_kappa] = m^-3；微观形式未知（O8）")

    section("I. 第四部分量纲表逐条复核")
    cases = [
        ("I1", "v_perp^2+h^2 = c^2", VEL ** 2, VEL ** 2),
        ("I2", "dT/ds = kappa N", 1 / LEN, 1 / LEN),
        ("I3", "kappa = R omega^2/c^2", LEN * TIM ** -2 / VEL ** 2, 1 / LEN),
        ("I4", "tau = h omega/c^2", VEL * TIM ** -1 / VEL ** 2, 1 / LEN),
        ("I5", "omega = c sqrt(kappa^2+tau^2)", VEL * (1 / LEN), 1 / TIM),
        ("I6", "m = (hbar/c) sqrt(kappa^2+tau^2)",
         (MAS * LEN ** 2 / TIM) / VEL * (1 / LEN), MAS),
        ("I7", "g = c^2 kappa", VEL ** 2 * (1 / LEN), ACC),
        ("I8", "F = m c^2 kappa", MAS * VEL ** 2 * (1 / LEN), FOR),
        ("I9", "beta_1 无量纲", (1 / LEN ** 2) / (1 / LEN ** 2), DIMLESS),
        ("I10", "beta_1 场方程两侧", 1 / LEN ** 2,
         (LEN ** 3 * MAS ** -1 * TIM ** -2) / VEL ** 2 * (MAS / LEN ** 3)),
        ("I11", "g = (c^2/2) grad ln beta_1", VEL ** 2 * (1 / LEN), ACC),
        ("I12", "mu = m_pi c/hbar", MAS * VEL / (MAS * LEN ** 2 / TIM), 1 / LEN),
        ("I13", "V = -g^2 e^{-mu r}/r", ENE * LEN / LEN, ENE),
        ("I14", "E = -k(c grad tau_t + d tau/dt) 两项同量纲",
         VEL * (1 / LEN ** 2), (1 / LEN) / TIM),
    ]
    for cid, title, lhs, rhs in cases:
        record(cid, "量纲 " + title, lhs == rhs, str(lhs) + " = " + str(rhs))

    record("I15", "电荷 q ∝ ∬ tau·dS 的量纲闭合", "OPEN",
           "[∬tau·dS] = m；要得到库仑需外部耦合常数 [k_q] = C/m，未定（O5）")


# ============================================================
def summary():
    print("")
    print("=" * 64)
    cnt = {}
    for item in RESULTS:
        v = item[2]
        cnt[v] = cnt.get(v, 0) + 1
    total = len(RESULTS)
    parts = []
    for k in ["PASS", "FAIL", "OPEN", "WARN"]:
        if k in cnt:
            parts.append(k + " " + str(cnt[k]))
    print("总计 " + str(total) + " 项：" + "  ".join(parts))
    print("=" * 64)
    for tag in ["FAIL", "WARN", "OPEN"]:
        print("")
        print("--- " + tag + " 清单 ---")
        for cid, title, v, detail in RESULTS:
            if v == tag:
                print("  " + cid + "  " + title)


def main():
    print("TUFT 核心公式总集 全维校验")
    print("=" * 64)
    sec_A()
    sec_B()
    sec_C()
    sec_D()
    sec_E()
    sec_F()
    sec_G()
    sec_H()
    summary()


if __name__ == "__main__":
    main()
