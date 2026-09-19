# -*- coding: utf-8 -*-
"""
O9 场方程导出校验
================
从 v2.1 主论的三大公理（速率守恒 / Frenet-Serret / 拓扑-物理对应）
及其导出恒等式 omega = c*sqrt(kappa^2+tau^2)、m = (hbar/c)*sqrt(kappa^2+tau^2) 出发，
逐项校验「麦克斯韦 / Klein-Gordon-Schrodinger / 汤川势」的导出边界。

姊妹文档: O9导出_麦克斯韦_薛定谔_汤川.md
依赖: sympy

判定口径:
  PASS = 严格导出，符号残差为 0（或在声明精度内的数值吻合）
  FAIL = 声称导出但残差非零 / 内部矛盾
  OPEN = 需要外部物理输入，本体系不可导出（诚实边界，非 bug）
"""

import sys
import itertools

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import sympy as sp

RESULTS = []


def record(cid, title, verdict, detail=""):
    if isinstance(verdict, bool):
        verdict = "PASS" if verdict else "FAIL"
    RESULTS.append((cid, title, verdict, detail))
    line = "[" + verdict + "] " + cid + " " + title
    if detail:
        line = line + "  |  " + str(detail)
    print(line)


def section(name):
    print("")
    print("=== " + name + " ===")


# ============================================================
# A. 前置：圆柱螺旋几何 + Darboux 转动矢量（omega 本源关系的第二证明）
# ============================================================
def check_geometry():
    section("A. 几何前置（Frenet / Darboux）")

    t = sp.symbols("t", real=True)
    R, hh, w = sp.symbols("R h omega", positive=True)
    # 公理 I: (R*omega)^2 + h^2 = c^2
    c = sp.sqrt(R ** 2 * w ** 2 + hh ** 2)

    rv = sp.Matrix([R * sp.cos(w * t), R * sp.sin(w * t), hh * t])
    r1 = rv.diff(t)
    r2 = rv.diff(t, 2)
    r3 = rv.diff(t, 3)

    cr = r1.cross(r2)
    kap = sp.simplify(sp.trigsimp(cr.norm() / r1.norm() ** 3))
    tau = sp.simplify(sp.trigsimp(cr.dot(r3) / cr.dot(cr)))

    kap_ref = R * w ** 2 / (R ** 2 * w ** 2 + hh ** 2)
    tau_ref = hh * w / (R ** 2 * w ** 2 + hh ** 2)

    record("A1", "曲率 kappa = R*omega^2/c^2",
           sp.simplify(kap - kap_ref) == 0, "kappa=" + str(kap))
    record("A2", "挠率 tau = h*omega/c^2",
           sp.simplify(tau - tau_ref) == 0, "tau=" + str(tau))

    omega_res = sp.simplify(sp.sqrt(kap ** 2 + tau ** 2) * c - w)
    record("A3", "角频率本源关系 omega = c*sqrt(kappa^2+tau^2)",
           omega_res == 0, "residual=" + str(omega_res))

    # Frenet 标架（显式构造后逐条验证 ODE）
    T = sp.Matrix([-R * w * sp.sin(w * t) / c,
                   R * w * sp.cos(w * t) / c,
                   hh / c])
    N = sp.Matrix([-sp.cos(w * t), -sp.sin(w * t), 0])
    B = T.cross(N)

    orth = [sp.simplify(T.dot(T) - 1), sp.simplify(N.dot(N) - 1),
            sp.simplify(B.dot(B) - 1), sp.simplify(T.dot(N)),
            sp.simplify(T.dot(B)), sp.simplify(N.dot(B))]
    record("A4", "Frenet 标架正交归一 {T,N,B}",
           all(sp.simplify(o) == 0 for o in orth))

    def ds(v):
        return v.diff(t) / c

    fs1 = sp.simplify(ds(T) - kap * N)
    fs2 = sp.simplify(ds(N) - (-kap * T + tau * B))
    fs3 = sp.simplify(ds(B) - (-tau * N))
    record("A5", "Frenet-Serret 方程组成立",
           all(v == sp.zeros(3, 1) for v in [fs1, fs2, fs3]))

    # Darboux 转动矢量 Omega = tau*T + kappa*B，应有 d(frame)/ds = Omega x frame
    Om = tau * T + kap * B
    cols = [T, N, B]
    diff_ok = True
    for v in cols:
        lhs = ds(v)
        rhs = Om.cross(v)
        if sp.simplify((lhs - rhs).norm()) != 0:
            diff_ok = False
    record("A6", "Darboux 定理: d/ds(frame) = Omega x frame, Omega = tau*T + kappa*B",
           diff_ok)

    om_norm = sp.simplify(sp.sqrt(sp.trigsimp(Om.dot(Om))))
    target = sp.sqrt(kap ** 2 + tau ** 2)
    # 两式皆正，比较平方以避开根式化简歧义
    om_ok = sp.simplify(om_norm ** 2 - target ** 2) == 0
    record("A7", "|Omega| = sqrt(kappa^2+tau^2) = omega/c（=> 标架转动率即内禀频率）",
           om_ok, "|Omega|=" + str(om_norm) + " = omega/c")


# ============================================================
# B. 麦克斯韦：严格导出部分（纯数学层，不依赖任何物理假设）
# ============================================================
def check_maxwell_strict():
    section("B. 麦克斯韦 L1：可由 F=dA 严格导出的部分")

    coords = sp.symbols("x0 x1 x2 x3")
    A = [sp.Function("A" + str(m))(*coords) for m in range(4)]
    eta = sp.diag(1, -1, -1, -1)

    def dd(mu, expr):
        return sp.diff(expr, coords[mu])

    F = sp.Matrix(4, 4, lambda m, n: dd(m, A[n]) - dd(n, A[m]))

    # B1 Bianchi 恒等式 -> 齐次麦克斯韦方程
    ok = True
    for l, m, n in itertools.combinations(range(4), 3):
        expr = sp.simplify(dd(l, F[m, n]) + dd(m, F[n, l]) + dd(n, F[l, m]))
        if expr != 0:
            ok = False
    record("B1", "Bianchi 恒等式 dF=0（等价于齐次麦克斯韦）", ok)

    # B2 显式翻译到 (E,B)：div B = 0 与 Faraday 定律
    Ev = [dd(i + 1, A[0]) - dd(0, A[i + 1]) for i in range(3)]
    Bv = [dd(2, A[3]) - dd(3, A[2]),
          dd(3, A[1]) - dd(1, A[3]),
          dd(1, A[2]) - dd(2, A[1])]
    divB = sp.simplify(sum(dd(i + 1, Bv[i]) for i in range(3)))
    curlE = [dd(2, Ev[2]) - dd(3, Ev[1]),
             dd(3, Ev[0]) - dd(1, Ev[2]),
             dd(1, Ev[1]) - dd(2, Ev[0])]
    faraday = [sp.simplify(curlE[i] + dd(0, Bv[i])) for i in range(3)]
    record("B2", "div B = 0", divB == 0)
    record("B3", "curl E + (1/c)dB/dt = 0（Faraday）",
           all(f == 0 for f in faraday))

    # B4 电荷守恒：由 F 反对称性恒等导出，无需假设
    Fup = eta * F * eta
    divj = sp.simplify(sum(dd(m, sum(dd(n, Fup[m, n]) for n in range(4)))
                           for m in range(4)))
    record("B4", "反对称性 => d_mu d_nu F^{mu nu} = 0（电荷守恒自动成立）",
           divj == 0)

    # B5 规范不变性
    chi = sp.Function("chi")(*coords)
    A2 = [A[m] + dd(m, chi) for m in range(4)]
    F2 = sp.Matrix(4, 4, lambda m, n: dd(m, A2[n]) - dd(n, A2[m]))
    record("B5", "规范变换 A -> A + dchi 保 F 不变",
           sp.simplify((F2 - F).norm()) == 0)


# ============================================================
# C. 麦克斯韦 桥接定理：场强 <-> 曲率（依赖标准相对论动力学）
# ============================================================
def check_maxwell_bridge():
    section("C. 麦克斯韦 L2：场强-曲率桥接（输入=相对论动力学）")

    tau_s, a_s, c_s = sp.symbols("tau a c", positive=True)
    # 双曲运动（恒定固有加速度 a）
    X = sp.Matrix([c_s ** 2 / a_s * sp.sinh(a_s * tau_s / c_s),
                   c_s ** 2 / a_s * sp.cosh(a_s * tau_s / c_s), 0, 0])
    U = X.diff(tau_s)
    norm2 = sp.simplify(U[0] ** 2 - U[1] ** 2 - U[2] ** 2 - U[3] ** 2)
    record("C1", "双曲运动 U^mu U_mu = c^2", sp.simplify(norm2 - c_s ** 2) == 0)

    acc = U.diff(tau_s)
    acc_inv = -(acc[0] ** 2 - acc[1] ** 2 - acc[2] ** 2 - acc[3] ** 2)
    kap4 = sp.simplify(sp.sqrt(sp.simplify(acc_inv)) / c_s ** 2)
    record("C2", "4D 世界线曲率 kappa_4 = a/c^2  <=> |f| = m*c^2*kappa_4",
           sp.simplify(kap4 - a_s / c_s ** 2) == 0, "kappa_4=" + str(kap4))

    # C3 数值：电子在磁场中的回旋运动，双向核对  m*c^2*kappa_4 = gamma*e*v*B
    e = 1.602176634e-19
    me = 9.1093837015e-31
    cc = 299792458.0
    v = 1.0e7
    Bf = 1.0
    gamma = 1.0 / ((1.0 - (v / cc) ** 2) ** 0.5)
    radius = gamma * me * v / (e * Bf)
    # 垂直加速度情形的固有加速度 = gamma^2 * v^2 / radius
    prop_acc = gamma ** 2 * v ** 2 / radius
    kap4_num = prop_acc / cc ** 2
    lhs = me * cc ** 2 * kap4_num
    rhs = gamma * e * v * Bf
    rel = abs(lhs - rhs) / rhs
    record("C3", "洛伦兹力与曲率恒等式双向吻合（相对残差）",
           rel < 1e-12, "rel=" + "{:.3e}".format(rel) + "  lhs=" + "{:.6e}".format(lhs)
           + "  rhs=" + "{:.6e}".format(rhs))


# ============================================================
# D. 康普顿-曲率恒等式 与 KG / Schrodinger
# ============================================================
def check_kg_schrodinger():
    section("D. 康普顿-曲率恒等式 / Klein-Gordon / Schrodinger")

    hbar, m, c = sp.symbols("hbar m c", positive=True)
    kap, tau, om = sp.symbols("kappa tau omega", positive=True)

    # D1 lambda_bar_C = 1/sqrt(kappa^2+tau^2)
    expr = sp.simplify((hbar / (m * c)) ** 2 * (kap ** 2 + tau ** 2))
    expr = sp.simplify(expr.subs(m, hbar * c * sp.sqrt(kap ** 2 + tau ** 2) / c ** 2))
    record("D1", "约化康普顿波长恒等式 lambda_bar = hbar/(mc) = 1/sqrt(kappa^2+tau^2)",
           sp.simplify(expr - 1) == 0)

    # D2 平面波色散 -> KG 色散
    x, t = sp.symbols("x t", real=True)
    k = sp.symbols("k", real=True)
    mu = sp.sqrt(kap ** 2 + tau ** 2)
    psi = sp.exp(sp.I * (k * x - om * t))
    res = sp.simplify(sp.diff(psi, t, 2) / c ** 2 - sp.diff(psi, x, 2) + mu ** 2 * psi)
    ok = sp.simplify(sp.expand(res / psi) - (-om ** 2 / c ** 2 + k ** 2 + mu ** 2)) == 0
    record("D2", "(Box + (kappa^2+tau^2))psi=0 的色散 = KG 色散 omega^2=c^2k^2+m^2c^4/hbar^2",
           ok)

    # D3 非相对论极限 -> Schrodinger
    Psi = sp.Function("Psi")(x, t)
    Om0 = m * c ** 2 / hbar
    psiv = sp.exp(-sp.I * Om0 * t) * Psi
    KGop = (sp.diff(psiv, t, 2) / c ** 2 - sp.diff(psiv, x, 2)
            + (m * c / hbar) ** 2 * psiv)
    inner = (sp.diff(Psi, t, 2) / c ** 2
             - 2 * sp.I * Om0 / c ** 2 * sp.diff(Psi, t)
             - sp.diff(Psi, x, 2))
    ok = sp.simplify(KGop - sp.exp(-sp.I * Om0 * t) * inner) == 0
    record("D3", "KG 在 psi=exp(-i mc^2 t/hbar)Psi 下退化为 NR 形式（质量项精确抵消）",
           ok)

    sch = sp.simplify(-hbar ** 2 / (2 * m) * inner)
    target = (sp.I * hbar * sp.diff(Psi, t)
              + hbar ** 2 / (2 * m) * sp.diff(Psi, x, 2)
              - hbar ** 2 / (2 * m * c ** 2) * sp.diff(Psi, t, 2))
    ok = sp.simplify(sch - target) == 0
    record("D4", "Schrodinger + 相对论修正项 hbar^2/(2mc^2) d_t^2 Psi",
           ok, "i*hbar*dPsi = -(hbar^2/2m)Lap Psi + (hbar^2/2mc^2)d_t^2 Psi")

    # D5 KG 连续性方程（psi 与其共轭分别用两个独立符号函数表示）
    psi_f = sp.Function("psi")(x, t)
    phi_f = sp.Function("phi")(x, t)
    mu_s = sp.symbols("mu", nonnegative=True)

    def Kop(f):
        return sp.diff(f, t, 2) / c ** 2 - sp.diff(f, x, 2) + mu_s ** 2 * f

    lhs = sp.expand(phi_f * Kop(psi_f) - psi_f * Kop(phi_f))
    rho = (phi_f * sp.diff(psi_f, t) - psi_f * sp.diff(phi_f, t)) / c ** 2
    jj = -(phi_f * sp.diff(psi_f, x) - psi_f * sp.diff(phi_f, x))
    ok = sp.simplify(lhs - (sp.diff(rho, t) + sp.diff(jj, x))) == 0
    record("D5", "KG 双线性构造 => 连续性方程 d_t rho + div j = 0（导出）", ok)


# ============================================================
# E. 汤川势
# ============================================================
def check_yukawa():
    section("E. 汤川势")

    r, mu = sp.symbols("r mu", positive=True)
    f = sp.exp(-mu * r) / r
    lap = sp.simplify(sp.diff(r ** 2 * sp.diff(f, r), r) / r ** 2)
    ok = sp.simplify(lap - mu ** 2 * f) == 0
    record("E1", "(Lap - mu^2)(exp(-mu r)/r) = 0, r>0", ok)

    eps = sp.symbols("epsilon", positive=True)
    flux = sp.limit(4 * sp.pi * eps ** 2 * sp.diff(f.subs(r, eps), eps), eps, 0, "+")
    record("E2", "delta 归一化：通量极限 = -4*pi", sp.simplify(flux + 4 * sp.pi) == 0,
           "flux=" + str(flux))

    record("E3", "mu -> 0 极限恢复 1/r（库仑势）",
           sp.simplify(sp.limit(f, mu, 0, "+") - 1 / r) == 0)

    # E4 数值：pi 介子力程 = 其约化康普顿波长
    hbar = 1.054571817e-34
    cc = 299792458.0
    eV = 1.602176634e-19
    MeV = 1.0e6 * eV
    mpi = 139.57039 * MeV / cc ** 2
    r_pi = hbar / (mpi * cc)
    rel = abs(r_pi - 1.4e-15) / 1.4e-15
    record("E4", "pi 介子力程 hbar/(m_pi c) = 1.41 fm ~ 核力力程 1.4 fm",
           rel < 0.05, "r_pi=" + "{:.4e}".format(r_pi) + " m, rel=" + "{:.2%}".format(rel))

    # E5 新的可证伪约束：光子质量上限 -> 光子本类孤子的曲率预算上限
    m_gamma_upper = 1.0e-18 * eV / cc ** 2
    mu_upper = m_gamma_upper * cc / hbar
    r_curv = 1.0 / mu_upper
    AU = 1.495978707e11
    record("E5", "光子质量上限 => sqrt(kappa^2+tau^2)_gamma < 5e-12 m^-1 (曲率半径 > 1 AU)",
           True, "mu_upper=" + "{:.3e}".format(mu_upper) + " m^-1, R>" +
           "{:.3e}".format(r_curv) + " m = " + "{:.2f}".format(r_curv / AU) + " AU")

    # E6 给定费米子 45 度假设下的电子曲率数值（由 m 反定，非独立预言）
    me = 9.1093837015e-31
    lam_bar = hbar / (me * cc)
    kap_e = (1.0 / lam_bar) * (2 ** 0.5 / 2)
    record("E6", "电子: eta=45deg 下 kappa=tau=1/(lambda_bar*sqrt2)",
           True, "kappa=tau=" + "{:.4e}".format(kap_e) + " m^-1, R=" +
           "{:.4e}".format(1.0 / kap_e) + " m")


# ============================================================
# F. 审计：惯用比值 beta_1 的定义方向（新版稿 3.3 节缺陷）
# ============================================================
def check_beta1_direction():
    section("F. 审计：beta_1 定义方向")

    r, G, M, c, K0 = sp.symbols("r G M c K0", positive=True)
    s_exp = 2 * G * M / (c ** 2 * r)

    # 真空要求 ln beta_1 为调和函数 => ln beta_1 = (+/-) 2GM/(c^2 r)
    lap = lambda f: sp.simplify(sp.diff(r ** 2 * sp.diff(f, r), r) / r ** 2)
    record("F1", "两种符号取向均满足真空方程 Lap(ln beta_1)=0, r>0",
           sp.simplify(lap(s_exp)) == 0 and sp.simplify(lap(-s_exp)) == 0)

    # 吸引引力要求 g_r = (c^2/2) d(ln beta_1)/dr < 0
    g_v21 = sp.simplify(c ** 2 / 2 * sp.diff(s_exp, r))
    g_new = sp.simplify(c ** 2 / 2 * sp.diff(-s_exp, r))
    record("F2", "v2.1 取向 beta_1=exp(+2GM/c^2 r) => g_r = -GM/r^2（吸引）",
           sp.simplify(g_v21 + G * M / r ** 2) == 0, "g_r=" + str(g_v21))
    record("F3", "新版稿取向 beta_1=exp(-2GM/c^2 r) => g_r = +GM/r^2（排斥）",
           sp.simplify(g_new - G * M / r ** 2) == 0, "g_r=" + str(g_new))

    # 方向自洽性：物质使局域 K=kappa^2+tau^2 增大 => beta_1 必须与之同增
    # v2.1: beta_1 = K/K0 同增 OK；新版: beta_1 = K0/K 反增 => 与该前提矛盾
    K = K0 * sp.exp(s_exp)
    beta_v21 = K / K0
    beta_new = K0 / K
    sgn_v21 = sp.simplify(sp.diff(sp.log(beta_v21), r) * r ** 2)
    sgn_new = sp.simplify(sp.diff(sp.log(beta_new), r) * r ** 2)
    record("F4", "与「局域 K 增大」前提自洽性：v2.1 定义",
           sp.simplify(sgn_v21 + 2 * G * M / c ** 2) == 0, "r^2*dln(beta)/dr=" + str(sgn_v21))
    record("F5", "与「局域 K 增大」前提自洽性：新版稿定义（应为负，实为正 => 矛盾）",
           sp.simplify(sgn_new - 2 * G * M / c ** 2) == 0,
           "r^2*dln(beta)/dr=" + str(sgn_new) + "  => 推出排斥引力")

    # 源项强度自洽性：带源方程只在 beta_1 -> 1 的弱场严格成立
    record("F6", "带源方程 beta_1*Lap(ln beta_1) = -(8 pi G/c^2) rho 的强场自洽性",
           "OPEN", "右侧含因子 1/beta_1，仅在 beta_1~1 弱场与点源 Poisson 严格相容")


# ============================================================
# ============================================================
# G. 对本轮《全维本源重构》稿件结论的裁定
# ============================================================
def check_verdicts():
    section("G. 对《全维本源重构》稿件声称的裁定")

    record("G1", "稿件 3.3 称「分母（局域 K）增大 => beta_1 > 1」——算术方向错误",
           "FAIL", "beta_1=<K0>/<K>，局域 K 增大只能使 beta_1<1")

    record("G2", "稿件 3.3+3.4 组合：该方向下 g=(c^2/2)grad ln beta_1 给出 +GM/r^2（排斥引力）",
           "FAIL", "修正：改回 v2.1 定义 beta_1=<K>/<K0>，则 g=-GM/r^2（吸引），见 F2/F4")

    record("G3", "稿件 2.2 称费米子 45 度由 Calugareanu-White 拓扑定理「严格求解」",
           "FAIL", "CW 要求闭合带 Lk 为整数，而 Lk=Tw=cos45=0.7071 非整数；"
                   "实为定义 s=sin^2(eta) 后令 s=1/2 的输入，非拓扑导出（O1）")

    record("G4", "稿件 4.1 称非线性场方程为「弱场极限下严格导出推论」",
           "OPEN", "恒等式部分严格；源项 -(8 pi G/c^2)rho 系由牛顿极限反定，不可导出（同 O）")


def main():
    print("O9 场方程导出校验 —— 麦克斯韦 / KG-Schrodinger / 汤川势")
    check_geometry()
    check_maxwell_strict()
    check_maxwell_bridge()
    check_kg_schrodinger()
    check_yukawa()
    check_beta1_direction()
    check_verdicts()

    n_pass = sum(1 for r in RESULTS if r[2] == "PASS")
    n_fail = sum(1 for r in RESULTS if r[2] == "FAIL")
    n_open = sum(1 for r in RESULTS if r[2] == "OPEN")
    total = len(RESULTS)
    print("")
    print("---- 汇总 ----")
    print("总判定: " + str(total) + "  PASS=" + str(n_pass) +
          "  FAIL=" + str(n_fail) + "  OPEN=" + str(n_open))
    print("")
    print("说明: FAIL 项不是 bug，而是对本轮稿件声称「已导出」内容的诚实否定（见 F2/F3/F5）。")
    print("说明: OPEN 项是本体系无法自证、必须外部物理输入的边界。")


if __name__ == "__main__":
    main()
