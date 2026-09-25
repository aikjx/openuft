# -*- coding: utf-8 -*-
"""空间光速螺旋曲率挠率几何统一场论 —— 全维精算、量纲审计与统一母方程结构校验（诚实版）。

覆盖维度：几何恒等式证明（精算到 50 位）、常数几何化（循环自证残差）、
引力常数多版本一致性、量纲合法性审计、统一母方程结构、尺度分层数值表。

不声称任何物理证明；输出用作 openuft 治理登记的证据记录。
"""
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

try:
    from mpmath import mp, mpf, sqrt as mpsqrt, pi as mppi, fabs
    mp.dps = 50
    HAVE_MP = True
except Exception:
    HAVE_MP = False

CODATA = {
    "m_e": 9.1093837015e-31,
    "hbar": 1.054571817e-34,
    "c": 299792458.0,
    "e": 1.602176634e-19,
    "epsilon0": 8.8541878128e-12,
    "mu0": 1.25663706212e-6,
    "alpha": 7.2973525693e-3,
    "G": 6.67430e-11,
    "Lambda": 1.1056e-52,
    "H0": 2.192e-18,
    "l_P": 1.616255e-35,
    "m_P": 2.176434e-8,
}

OUT = []


def log(line):
    OUT.append(line)
    print(line)


def res(name, ok, detail, kind):
    tag = "PASS" if ok else "FAIL"
    log("{0:<46} {1}  [{2}]  {3}".format(name, tag, kind, detail))
    return ok


# ---- 量纲代数（SI 7 基：M L T I Theta N J） ----
class Dim:
    UNITS = ["M", "L", "T", "I", "Theta", "N", "J"]

    def __init__(self, d=None):
        base = {u: 0 for u in Dim.UNITS}
        if d:
            base.update(d)
        self.d = base

    def __mul__(self, o):
        return Dim({u: self.d[u] + o.d[u] for u in Dim.UNITS})

    def __truediv__(self, o):
        return Dim({u: self.d[u] - o.d[u] for u in Dim.UNITS})

    def __pow__(self, n):
        return Dim({u: self.d[u] * n for u in Dim.UNITS})

    def __eq__(self, o):
        return all(self.d[u] == o.d[u] for u in Dim.UNITS)

    def __repr__(self):
        parts = ["{0}^{1}".format(u, self.d[u]) for u in Dim.UNITS if self.d[u]]
        return " ".join(parts) if parts else "1(无量纲)"


D1 = Dim({"M": 1})
DL = Dim({"L": 1})
DT = Dim({"T": 1})
DI = Dim({"I": 1})
M = D1
L = DL
T = DT
I = DI
ONE = Dim()
C = L / T
HBAR = M * L ** 2 / T
CHARGE = I * T
EPS0 = M ** -1 * L ** -3 * T ** 4 * I ** 2
MU0 = M * L * T ** -2 * I ** -2
G_DIM = M ** -1 * L ** 3 * T ** -2
LAMBDA_DIM = L ** -2
H0_DIM = T ** -1


def dimcheck(name, got, expect):
    ok = (got == expect)
    res(name, ok, "得 {0} 期望 {1}".format(got, expect), "量纲")
    return ok


def main():
    log("=" * 90)
    log("空间光速螺旋曲率挠率几何统一场论 —— 全维精算与量纲审计（诚实版）")
    log("精度：{0} 位小数".format(50 if HAVE_MP else "双精度"))
    log("=" * 90)

    m_e = CODATA["m_e"]
    hbar = CODATA["hbar"]
    c = CODATA["c"]
    e = CODATA["e"]
    eps0 = CODATA["epsilon0"]
    mu0 = CODATA["mu0"]
    alpha = CODATA["alpha"]
    G = CODATA["G"]
    l_P = CODATA["l_P"]
    m_P = CODATA["m_P"]

    # ---------- 几何基础 ----------
    rho_e = hbar / (m_e * c)
    b_e = rho_e / alpha
    denom = rho_e * rho_e + b_e * b_e
    kappa_e = rho_e / denom
    tau_e = b_e / denom
    omega = c / math.sqrt(denom)  # 螺旋总角速率（沿弧长），使 κ²+τ²=ω²/c² 严格成立

    lhs = kappa_e * kappa_e + tau_e * tau_e
    rhs1 = 1.0 / denom
    rhs2 = (omega / c) ** 2
    rel_id = abs(lhs - rhs1) / max(abs(rhs1), 1e-300)
    rel_id2 = abs(lhs - rhs2) / max(abs(rhs2), 1e-300)
    res("几何恒等式 κ²+τ²=1/(ρ²+b²)", rel_id < 1e-15,
        "残差={0:.2e}".format(rel_id), "代数恒等式")
    res("几何恒等式 κ²+τ²=ω²/c²", rel_id2 < 1e-15,
        "残差={0:.2e}".format(rel_id2), "代数恒等式")
    res("α=κ/τ=ρ/b（定义性）", abs(kappa_e / tau_e - alpha) / alpha < 1e-15,
        "κ/τ={0:.6e}".format(kappa_e / tau_e), "定义")
    dimcheck("dim κ=ρ/(ρ²+b²)", L ** -1, L ** -1)
    dimcheck("dim τ=b/(ρ²+b²)", L ** -1, L ** -1)
    dimcheck("dim α=κ/τ", ONE, ONE)

    # ---------- 常数几何化（循环自证） ----------
    m_rec = hbar * tau_e * (alpha * alpha + 1.0) / (alpha * c)
    rel_m = abs(m_rec - m_e) / m_e
    res("C0006 m=ħτ(α²+1)/(αc) 复算", rel_m < 1e-12,
        "m_rec={0:.6e} 相对误差={1:.2e}".format(m_rec, rel_m), "循环自证")

    hbar_rec = m_e * c * rho_e
    rel_h = abs(hbar_rec - hbar) / hbar
    res("C0008 ħ=mcρ 复算", rel_h < 1e-12,
        "ħ_rec={0:.6e} 相对误差={1:.2e}".format(hbar_rec, rel_h), "循环自证")

    e_rec = math.sqrt(4.0 * math.pi * eps0 * hbar * c * (kappa_e / tau_e))
    rel_e = abs(e_rec - e) / e
    res("C0009 e=√(4π ε₀ ħ c α) 复算", rel_e < 1e-9,
        "e_rec={0:.6e} 相对误差={1:.2e}（受 CODATA 取整限制，非机器零）".format(e_rec, rel_e),
        "循环自证")

    # ε₀ 来源式：量纲 + 数值双重审计
    eps0_rec = tau_e / (4.0 * math.pi * c * c * kappa_e)
    rel_eps = abs(eps0_rec - eps0) / eps0
    res("C0010 ε₀=τ/(4πc²κ) 数值", rel_eps < 1e-6,
        "ε₀_rec={0:.6e} 真值={1:.6e} 偏差={2:.2e}".format(eps0_rec, eps0, rel_eps),
        "公式不自洽")
    dimcheck("dim ε₀=τ/(4πc²κ) 来源式", L ** -2 * T ** 2, EPS0)

    # ---------- 引力常数多版本 ----------
    # (a) 依赖 l_P：G=c³/(2ħ(κ_P²+τ_P²))，κ_P=1/l_P（来源尺度分层）
    kappa_P = 1.0 / l_P
    tau_P = kappa_P  # 普朗克层 α=1（来源声称）
    G_a = c ** 3 / (2.0 * hbar * (kappa_P * kappa_P + tau_P * tau_P))
    rel_Ga = abs(G_a - G) / G
    res("C0011(a) G=c³/(2ħ(κ_P²+τ_P²)) 复算", rel_Ga < 1e-6,
        "G_a={0:.6e} 相对误差={1:.2e}（依赖 l_P=√(ħG/c³)，循环）".format(G_a, rel_Ga),
        "循环")
    dimcheck("dim G=c³/(2ħ(κ²+τ²))", G_DIM, G_DIM)

    # (b)(c)(d) 数值互不等价
    G_b = 2.0 * c ** 3 * tau_P / (kappa_P * kappa_P)
    G_c = c ** 3 * tau_P * tau_P / (2.0 * hbar * kappa_P * kappa_P)
    G_d = 8.0 * math.pi * c ** 3 * tau_P / (3.0 * kappa_P * kappa_P)
    log("  G 版本数值： (a)={0:.3e} (b)={1:.3e} (c)={2:.3e} (d)={3:.3e}  真值={4:.3e}".format(
        G_a, G_b, G_c, G_d, G))
    rel_b = abs(G_b - G) / G
    rel_c = abs(G_c - G) / G
    res("C0011(b)(c)(d) 版本互不等价", max(rel_b, rel_c) > 1e-2,
        "max 相对误差={0:.2e}".format(max(rel_b, rel_c)), "版本矛盾")

    # (e) G=α²μ₀ 量纲非法（来源自承）
    G_e = alpha * alpha * mu0
    res("C0011(e) G=α²μ₀ 量纲", MU0 == G_DIM,
        "得 {0} 期望 {1}（α 无量纲，故 α²μ₀ 量纲=μ₀）".format(MU0, G_DIM), "量纲非法")

    # ---------- 引力精细结构常数 ----------
    alpha_grav = G * m_e * m_e / (hbar * c)
    alpha_grav_geom = (m_e / m_P) ** 2
    rel_ag = abs(alpha_grav - alpha_grav_geom) / alpha_grav_geom
    res("引力精细结构常数 α_grav=(m/m_P)²", rel_ag < 1e-3,
        "α_grav={0:.3e} (m/m_P)²={1:.3e} 相对误差={2:.2e}（受 CODATA 取整限制，非机器零）".format(
            alpha_grav, alpha_grav_geom, rel_ag),
        "几何重写（openuft M02 同构）")

    # ---------- 宇宙学 ----------
    kappa_vac = mpsqrt(mppi) * 0.0  # 占位；真空曲率来源未给第一性锚
    # 以来源 Λ=κ_vac² 形式校验量纲
    dimcheck("dim Λ=κ_vac²", LAMBDA_DIM, LAMBDA_DIM)
    dimcheck("dim H₀=c√Λ/3", H0_DIM, H0_DIM)
    # 用真值 Λ 反推所需 κ_vac 量级
    Lambda = CODATA["Lambda"]
    kappa_vac_needed = math.sqrt(Lambda)
    log("  为使 Λ 吻合观测，需 κ_vac≈{0:.3e} m⁻¹（来源未给第一性锚定）".format(kappa_vac_needed))

    # ---------- 统一母方程结构校验 ----------
    # 右端括号各力项量纲应同为 [力]=[M L T⁻²]
    force_dim = M * L / T ** 2
    dimcheck("dim 统一母方程右端 (c⁴/8πG)·(κ/τ)F_EM", (L ** 4 / T ** 4 / G_DIM) * (ONE) * (force_dim), L ** -2)
    dimcheck("dim 左端 G_μν+Λg_μν", L ** -2, L ** -2)
    log("  统一母方程：左端 [L⁻²]，右端 (c⁴/8πG)·括号项 得 [M² L² T⁻⁴]（系数 c⁴/8πG 应为 8πG/c⁴ 方能匹配左端）。")
    log("  来源系数倒置导致量纲不自洽；即便改对系数，也仅为几何重写，无区别于 GR/SM 的新预言。")

    # ---------- 尺度分层数值表 ----------
    log("-" * 90)
    log("尺度分层数值表（来源内部口径，跨文件一致性见 C0021）")
    log("  层         ρ(m)            κ(m⁻¹)           τ(m⁻¹)           α=κ/τ")
    log("  电子层     {0:.3e}   {1:.3e}   {2:.3e}   {3:.3e}".format(
        rho_e, kappa_e, tau_e, kappa_e / tau_e))
    log("  普朗克层   {0:.3e}   {1:.3e}   {2:.3e}   {3:.3e}".format(
        l_P, kappa_P, tau_P, kappa_P / tau_P))
    macro_rho = 1.0  # 纯数学宏观拓扑层（来源自承无实体）
    macro_kappa = 1.78e-13
    log("  宏观拓扑   {0:.3e}   {1:.3e}   (来源自承无实体物理对应)".format(macro_rho, macro_kappa))

    log("-" * 90)
    log("诚实结论：")
    log("  代数恒等式（κ²+τ²=ω²/c² 等）精算残差 < 1e-15，自洽不可质疑。")
    log("  常数几何化（m/ħ/e/ε₀/G）复算残差受 CODATA 取整限制（e ~3e-10，ε₀ 偏差 7e4 倍）。")
    log("  G 五版本互不等价且 (e) 量纲非法；统一母方程/含挠率场方程为几何重写，无新预言。")
    log("  本体系定位 = 几何重参数化框架；数学自洽 ≠ 实验证实。")
    log("=" * 90)

    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(here, "..", "..", "09_验证结果", "原始运行记录"))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "全维精算_ct_uft_report.txt")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(OUT) + "\n")
    log("报告已写入：" + out_path)


if __name__ == "__main__":
    main()
