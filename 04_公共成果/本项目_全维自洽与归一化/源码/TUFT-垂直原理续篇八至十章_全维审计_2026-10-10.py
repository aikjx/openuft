# -*- coding: utf-8 -*-
"""
TUFT 垂直原理四力统一 · 续篇（第八~十章 + 附录D）全维机器审计（r23）
================================================================
来料：《四力大统一：垂直原理螺旋统一场论》全维攻破续篇 V9.1
      新增第八章（数值仿真与参数扫描）、第九章（对标经典理论）、
      第十章（可观测预言、证伪判据与终审）、附录D（全维攻破审计报告）

分工声明（避免与既有册重复计数）
----------------------------------------------------------------
r22（`判定_TUFT-r22-垂直原理四力统一框架_全维审计_2026-10-10.md`，
条目 48 / 自检 14/14）已审 **L0 公设 / L1 恒等式 / L2 场论 / L3 经典极限 / L5 参数边界**。
本册**只审来料新给的第八~十章与附录D**，凡与 r22 已判条目重合者一律标注
「同 r22 Xnn，不重复计数」，只记**复发 / 未回应 / 口径订正**三类增量。

坐标与口径（与 r22 对齐）
----------------------------------------------------------------
  - κ/τ 为弧长倒数 L^-1；ω 角频率 T^-1；c 光速 L/T；ρ/b 圆柱螺旋半径与螺距 L
  - α 取 α1 = τ/κ = b/ρ ≈ 1/137.036（r22 B05 的口径一）
  - 数值一律 Decimal 60 位；量纲用 Fraction 向量 (M, L, T, I)
  - 跨册纪律：**F4 范畴一致性** 与 **E9 能标一致性** 必须显式留痕

作者：算法联盟归一化链 r23
日期：2026-10-10
"""
import json
import os
import sys
from decimal import Decimal as Dc, getcontext
from fractions import Fraction

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OUTDIR = os.path.join(BASE, "数据")

# ------------------------------------------------------------------ 常数
TWO_PI = Dc("6.283185307179586476925286766559005768394338798750211641949889")
PI = TWO_PI / Dc(2)
D0, D1, D2 = Dc(0), Dc(1), Dc(2)


class CD:
    c = Dc("299792458")
    h = Dc("6.62607015e-34")
    hbar = h / TWO_PI
    G = Dc("6.67430e-11")
    e = Dc("1.602176634e-19")
    eps0 = Dc("8.8541878128e-12")
    alpha = Dc("7.2973525693e-03")
    m_e = Dc("9.1093837015e-31")
    m_p = Dc("1.67262192369e-27")
    m_P_cd = Dc("2.176434e-8")          # CODATA 2018 公布值（用于交叉核对）
    eV = Dc("1.602176634e-19")
    m_W_GeV = Dc("80.379")
    m_pi0_MeV = Dc("134.9768")
    m_pip_MeV = Dc("139.57039")

    @classmethod
    def m_P(cls):
        return (cls.hbar * cls.c / cls.G).sqrt()

    @classmethod
    def kg_from_eV(cls, ev):
        return ev * cls.eV / (cls.c * cls.c)


ITEMS = []
_SELF = []


def add(name, verdict, detail, note=""):
    ITEMS.append({"name": name, "verdict": verdict, "detail": detail, "note": note})
    print("  [%-9s] %s" % (verdict, name))
    print("             %s" % detail)


def selfchk(name, ok, detail=""):
    _SELF.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  自检[%s] %s %s" % ("OK " if ok else "!! ", name, detail))
    return ok


def rel(a, b):
    a, b = Dc(a), Dc(b)
    if b == 0:
        return Dc(0) if a == 0 else Dc("1e99")
    return abs(a - b) / abs(b)


# ===========================================================================
# §8  数值仿真层
# ===========================================================================
def section8():
    print("\n" + "=" * 78)
    print("§8  数值仿真层（第八章）")
    print("=" * 78)

    # --- N01 m_P ---
    # 判据订正（**不是放松，是换成正确的判据**）：
    #   m_P = √(ħc/G) 的**可达精度由 G 决定**：G = 6.67430(15)e-11 ⇒ u_r(G) = 2.2e-5，
    #   开方后 u_r(m_P) = ½u_r(G) = 1.1e-5。原判据「相对差 < 1e-8」比输入精度还严 3 个
    #   数量级 —— 它要求一个**物理上不可能达到**的吻合度，因而是**错判据**（会把正确的
    #   公式误杀）。正确判据取两条，均非任意：
    #     (a) **末位半刻度**（严格）：CODATA 公布值 2.176434e-8 只有 7 位有效数字，
    #         末位 = 1e-14 kg，半刻度 = 5e-15 kg。计算值与公布值之差须 ≤ 半刻度，
    #         即二者在**全部公布位数上一致**（否则才说明公式错）。
    #     (b) **输入不确定度**（严格）：相对差须 ≤ u_r(m_P) = ½u_r(G) = 1.1e-5。
    mP = CD.m_P()
    ulp_cd = Dc("1e-14")                     # 2.176434e-8 的末位（7 位有效数字）
    half_ulp = ulp_cd / Dc(2)
    d_abs = abs(mP - CD.m_P_cd)
    u_r_G = Dc("0.00015") / Dc("6.67430")    # G = 6.67430(15)e-11
    u_r_mP = u_r_G / Dc(2)                   # 开方 ⇒ 不确定度减半
    ok = (d_abs <= half_ulp) and (rel(mP, CD.m_P_cd) <= u_r_mP)
    selfchk("N01 自检：m_P = √(ħc/G) 与 CODATA 在全部公布位数上一致"
            "（|Δ| ≤ 末位半刻度 5e-15 kg 且相对差 ≤ u_r = 1.1e-5）",
            ok, "Δ = %.4E kg（≤ %.1E）｜相对差 %.2E（≤ %.2E）"
            % (d_abs, half_ulp, rel(mP, CD.m_P_cd), u_r_mP))
    add("N01 8.2 `m_P = sqrt(hbar*c/G)` 数值正确（判据订正：按输入精度，非任意 1e-8）",
        "PASS" if ok else "FAIL",
        "m_P = %.12E kg（CODATA 公布 2.176434e-8；|Δ| = %.3E kg = 末位半刻度 %.1E 的 %.2f 倍）"
        " ⇒ 公式与数值在**全部 7 位公布数字**上一致，PASS。"
        "⚠️ 附带结论：u_r(m_P) = ½u_r(G) = %.2E ⇒ **m_P 实际只有约 5 位有效数字可信**，"
        "凡把它写成 17 位乃至 250 位者一律属**伪精度**（联动 N06）。"
        % (mP, d_abs, half_ulp, float(d_abs / half_ulp), u_r_mP))

    # --- N02 圆柱螺旋 κ/τ ---
    rho, b = Dc("1.0"), Dc("0.0072973525693")
    S = rho * rho + b * b
    kap, tau = rho / S, b / S
    r2 = rel(kap * kap + tau * tau, Dc(1) / S)
    selfchk("N02 自检：κ²+τ² = 1/(ρ²+b²)（残差 <1e-55）", r2 < Dc("1e-55"),
            "%.2E" % r2)
    add("N02 8.2 `kappa_tau(rho,b)` 是圆柱螺旋标准式",
        "PASS",
        "κ = ρ/(ρ²+b²) = %.12E、τ = b/(ρ²+b²) = %.12E；κ²+τ² = 1/(ρ²+b²) 残差 %.2E"
        " ⇒ 与 r22 A01–A05 同源，**PASS 且为恒等式**（零信息量，见 N05）。"
        % (kap, tau, r2))

    # --- N03 α = b/ρ ---
    a1 = tau / kap
    r3 = rel(a1, b / rho)
    selfchk("N03 自检：α = τ/κ = b/ρ 精确", r3 < Dc("1e-55"), "%.2E" % r3)
    add("N03 8.2 `alpha_from_rho_b = b/rho` 与 r22 口径一一致",
        "PASS",
        "τ/κ = %.12E = b/ρ（残差 %.2E）⇒ α1 口径正确；但 α 是**自由比**，"
        "与 r22 B06「构造族证否 α 可锁定」同源（本册不重复计数，见 N08）。" % (a1, r3))

    # --- N04 ∇κ·∇τ 符号（核心） ---
    def fields(x, y, z):
        return (1.0 + 0.3 * x + 0.2 * y * y + 0.1 * z,
                0.5 + 0.1 * y + 0.4 * z + 0.05 * x * x)

    def kt(r_, b_):
        s = r_ * r_ + b_ * b_
        return r_ / s, b_ / s

    X0, Y0, Z0, H = 0.3, -0.2, 0.15, 1e-5
    g = {}
    for nm, f in (("rho", lambda p: fields(*p)[0]), ("b", lambda p: fields(*p)[1]),
                  ("kappa", lambda p: kt(*fields(*p))[0]),
                  ("tau", lambda p: kt(*fields(*p))[1])):
        vec = []
        for i in range(3):
            pp = [X0, Y0, Z0]; pp[i] += H; a_ = f(tuple(pp))
            pm = [X0, Y0, Z0]; pm[i] -= H; c_ = f(tuple(pm))
            vec.append((a_ - c_) / (2 * H))
        g[nm] = vec
    r0, b0 = fields(X0, Y0, Z0)
    S0 = r0 * r0 + b0 * b0
    dot_num = sum(g["kappa"][i] * g["tau"][i] for i in range(3))
    gr2 = sum(v * v for v in g["rho"])
    gb2 = sum(v * v for v in g["b"])
    grb = sum(g["rho"][i] * g["b"][i] for i in range(3))
    C = (-r0 ** 4 + 6 * r0 ** 2 * b0 ** 2 - b0 ** 4) / S0 ** 4
    A = 2 * r0 * b0 * (r0 ** 2 - b0 ** 2) / S0 ** 4
    lai = A * (gb2 - gr2) + C * grb        # 8.2 代码：abs(db)^2 - abs(drho)^2
    ind = A * (gr2 - gb2) + C * grb        # 独立推导：abs(drho)^2 - abs(db)^2
    d_lai, d_ind = abs(lai - dot_num), abs(ind - dot_num)
    selfchk("N04 自检：独立式 vs 有限差分（应 <1e-9）", d_ind < Dc("1e-9"), "%.2E" % d_ind)
    selfchk("N04′ 自检：来料式 vs 有限差分（应 >1e-4，即错误可检出）",
            d_lai > Dc("1e-4"), "%.2E" % d_lai)
    add("N04 **8.2 代码固化了 r22 C08 的同一符号错误**（本册核心 FAIL）",
        "FAIL",
        "测试点 (0.3,−0.2,0.15)：有限差分 ∇κ·∇τ = %+.11E（基准）；"
        "8.2 代码式（|∇b|²−|∇ρ|²）= %+.11E（偏差 %.2E）；"
        "独立式（|∇ρ|²−|∇b|²）= %+.11E（偏差 %.2E，差分截断量级）。"
        "⇒ **r22 已列为 P0 修正项，续篇未修正，反而写进可执行代码** ⇒ 由「笔误」升级为"
        "「被固化的错误」。注意：数值仿真对此**免疫**——代码与解析式同源，"
        "故「残差趋机器零」不能用来证明公式对。"
        % (Dc(repr(dot_num)), Dc(repr(lai)), Dc(repr(d_lai)),
           Dc(repr(ind)), Dc(repr(d_ind))),
        note="与 r22 C08 同型；缺陷族第 2 次出现（首次=解析式，本次=代码）")

    # --- N05 虚假精度 ---
    dig_G, dig_alpha = 6, 11
    add("N05 **250 位高精度是虚假精度**，且「残差趋机器零」是同义反复",
        "FAIL",
        "输入有效位：G = 6.67430e−11 → **6 位**；α → 11 位 ⇒ `mp.dps=250` 中"
        "超出 min(输入位)=6 位的约 **244 位全是噪声**。且恒等式在高精度下残差趋零"
        "是**同义反复**（恒等式本就精确成立），不构成任何物理证据。"
        "⇒ 「纯几何恒等式…残差趋近机器零，PASS」这条**不能作为论据**。",
        note="高精度 ≠ 高精度物理；判别力由输入的实测不确定度决定")

    # --- N06 循环恒等 ---
    back = CD.hbar * CD.c / (CD.m_P() ** 2)
    r6 = rel(back, CD.G)
    add("N06 8.2 的 `m_P=sqrt(hbar*c/G)` 与「G 为输入」互为逆 ⇒ **循环恒等**",
        "CORRECTED",
        "反解 ħc/m_P² = %.12E 与输入 G = %.12E 相对差 %.2E ⇒ 二者是同一式的两种写法，"
        "代码把它当**独立导出常数**使用属循环记账。与 r22 D01 同族（**库内第 6 次复发**）。"
        % (back, CD.G, r6),
        note="同 r22 D01，本册只记复发计数，不重复判决")

    # --- N07 χ² ---
    add("N07 8.3 「χ²_red ≈ 1.03」**不可复核**（未给 N_data 与 dof）",
        "MISMATCH",
        "χ²_red = χ²/(N_data − N_param)，来料**未给 N_data、未给 N_param** ⇒ 数值无法复算。"
        "且口径自相矛盾：既称「对 α,G,g_s,g_W 高度敏感、**必须固定输入**」，"
        "又称「模型拟合度」——若四者固定输入则无拟合自由度；若四者拟合且数据点≈4，"
        "则 χ²=0 而非 1.03（过拟合、无预测力）。两种读法都得不到 1.03 ⇒ 待来料补口径。",
        note="统计量必须随附自由度，否则不可复核")

    # --- N08 MCMC ---
    add("N08 8.4 用 MCMC 证明「连续流形无离散定点」是**循环论证**，零增量",
        "INFO",
        "α = b/ρ 是**连续比**，ρ,b ∈ ℝ ⇒ α 可取任意实数，这是**解析上显然**的；"
        "在连续流形上抽样当然找不到孤立点。且 r22 B06 已用**构造族**给出更强结论"
        "（α ∈ [10⁻⁶,10⁶] 共 11 个值，L1 恒等式最大残差 1.0E−59 = 机器零）。"
        "⇒ MCMC 在此**零信息增量**，且其结论（「拓扑不钉死 α」）方向正确但早已被解析证否。",
        note="同 r22 B06，本册只记「数值方法重复了既有解析结论」")

    # --- N09 线性势 ---
    mus = [(Dc(1), Dc(2) / (Dc(1) ** 2)), (Dc(2), Dc(2) / (Dc(2) ** 2)),
           (Dc("0.5"), Dc(2) / (Dc("0.5") ** 2))]
    selfchk("N09 自检：μ²=2/r² 在 r=1/2/0.5 上互不相同",
            len(set(str(m[1]) for m in mus)) == 3,
            " / ".join("r=%s→μ²=%s" % (str(m[0]), "%.3E" % m[1]) for m in mus))
    add("N09 8.5 线性势结论**正确但弱于既有**：r22 D03 已升级为无解证明",
        "CORRECTED",
        "来料只写「数值代入结果不为零」。r22 D03 给出更强的**结构性证明**："
        "令 (∇²−μ²)(σr)=0 需 μ²=2/r² 对一切 r 成立，而 r=1→μ²=2、r=2→μ²=0.5、"
        "r=0.5→μ²=8 互相矛盾 ⇒ **FAIL 是结构性的，不是取值问题**。续篇未引用该更强结论。",
        note="同 r22 D03；本册记「续篇结论强度倒退」")

    # --- N10 力程 ---
    lam_W = CD.hbar / (CD.kg_from_eV(CD.m_W_GeV * Dc("1e9")) * CD.c)
    lam_pi0 = CD.hbar / (CD.kg_from_eV(CD.m_pi0_MeV * Dc("1e6")) * CD.c)
    lam_pip = CD.hbar / (CD.kg_from_eV(CD.m_pip_MeV * Dc("1e6")) * CD.c)
    ref = {"W": Dc("2.454957E-18"), "pi0": Dc("1.461933E-15"), "pip": Dc("1.413817E-15")}
    ok10 = (rel(lam_W, ref["W"]) < Dc("1e-6") and rel(lam_pi0, ref["pi0"]) < Dc("1e-6")
            and rel(lam_pip, ref["pip"]) < Dc("1e-6"))
    selfchk("N10 自检：λ 与 r22 C06/C07 读数逐位一致", ok10,
            "λ_W=%.6E λ_π⁰=%.6E λ_π±=%.6E" % (lam_W, lam_pi0, lam_pip))
    add("N10 力程 λ=ħ/(mc) 三项与 r22 逐位一致（独立交叉印证）",
        "PASS" if ok10 else "FAIL",
        "λ_W = %.6E m、λ(π⁰) = %.6E m、λ(π±) = %.6E m（r22 读数 %.6E / %.6E / %.6E）"
        " ⇒ 两册独立复算一致。但续篇**仍未声明 π⁰ 还是 π± 口径**（相对差 3.3%%），"
        "沿用 r22 C07 的 MISMATCH。" % (lam_W, lam_pi0, lam_pip,
                                    ref["W"], ref["pi0"], ref["pip"]),
        note="口径未声明问题同 r22 C07，续篇未回应")


# ===========================================================================
# §9  对标层
# ===========================================================================
def section9():
    print("\n" + "=" * 78)
    print("§9  对标层（第九章）")
    print("=" * 78)

    add("M01 与 GR 的本体论分歧描述正确",
        "PASS",
        "「GR 弯曲时空 / TUFT 弯曲粒子自身世界线、时空背景平直」的描述准确，"
        "与 r22 A08 登记的本体冲突一致。低能弱场下二者都退化到牛顿势，重合的是**势形式**。")

    add("M02 **「无法自动还原 GR 的引力红移」过强** ⇒ 应限定为强场/高阶",
        "MISMATCH",
        "弱场引力红移 Δν/ν = ΔΦ/c² **只依赖牛顿势**，任何能给出牛顿势的理论都能还原，"
        "TUFT 的 Yukawa 在 μ→0 极限下给出 1/r 势 ⇒ **弱场红移可以还原**。"
        "⇒ 来料把「强场视界 / 引力波高阶修正」与「弱场红移」并列，属**过度承认**，"
        "应改写为「无法自动还原黑洞视界与强场/辐射高阶修正」。",
        note="过度收缩边界与过度扩张边界同为口径错误")

    add("M03 与 EC 的「符号同名、物理客体不同」判定正确",
        "PASS",
        "EC 挠率 = 时空挠率（自旋源激发）；TUFT τ = 粒子世界线挠率 ⇒ 几何对象不同，"
        "仅「普朗克尺度量级匹配」不构成理论等价。与 r22 E04「只做量级登记不核验」一致。")

    add("M04 **「质量由螺旋几何衍生」只给单一标度，给不出质量谱**",
        "BOUNDARY",
        "m = ħω/c² 只提供**一个**质量标度；而「四力统一」与 SM 对标需要的是"
        "**质量谱**：m_e/m_μ/m_p 的比值、三代结构、CKM/PMNS。来料未处理，"
        "且与 L5「α,G,g_s,g_W 无法内生」口径不一致——若质量能由几何衍生，"
        "为何耦合常数不能？⇒ 需澄清「衍生」指的是标度还是谱。",
        note="质量标度 ≠ 质量谱；这是来料对标 SM 时缺的关键一环")

    add("M05 与弦论/LQG 的「范式独立」是描述性陈述",
        "INFO",
        "「数学结构互不兼容」是定性比较，无待定量的可算断言 ⇒ 记为 INFO，不计入攻破计数。")


# ===========================================================================
# §10 预言层
# ===========================================================================
def section10():
    print("\n" + "=" * 78)
    print("§10  预言层（第十章 10.1）")
    print("=" * 78)

    add("P01 **预言1「所有相互作用都是汤川/库仑势」与 8.5/10.2 自认矛盾**",
        "MISMATCH",
        "10.1 预言1 称「**所有**相互作用都满足 U ∝ e^{−r/λ}/r」；"
        "但 8.5 与 10.2 明确承认 QCD 基本相互作用是**线性禁闭势** σr（并非汤川），"
        "并用「TUFT 划定边界」豁免。⇒ 实际被统一的是**引力 / 电磁 / 弱 / 剩余核力**"
        "（后者是介子交换的有效力，不是 QCD 基本力）⇒ **书名「四力大统一」的「四」不成立**，"
        "应为「三力 + 一个有效力」。",
        note="标题级口径问题；建议在正文显式改写作用域")

    add("P02 **预言2 λ=ħ/(mc) 对引力是极限情形，需注明**",
        "BOUNDARY",
        "引力子 μ=0 ⇒ λ=∞，严格说**不满足**「力程由康普顿波长决定」这一表述"
        "（它是 μ→0 的极限）。⇒ 四力中有一力处于退化分支，来料未注明 ⇒ 记为边界。")

    # --- P03 力强比值：恒等式 + E9 能标 + F4 范畴 ---
    FE = CD.e * CD.e / (Dc(4) * PI * CD.eps0)          # e²/(4πε₀)
    FG = CD.G * CD.m_p * CD.m_p
    ratio_direct = FE / FG
    ratio_formula = CD.alpha * (CD.m_P() / CD.m_p) ** 2
    r_id = rel(ratio_direct, ratio_formula)
    aG_mp = CD.G * CD.m_p * CD.m_p / (CD.hbar * CD.c)
    # 判据订正（**不是放松，是换成正确的判据**）：
    #   原判据「相对差 < 1e-55」是**错判据**——它要求恒等式在十进制**截断噪声**下也成立，
    #   而来料与 CODATA 用的 α = 7.2973525693e-3 是**11 位有效数字**的十进制截断值
    #   （末位 1e-13，半刻度相对量 = 5e-14/7.297e-3 = 6.85e-12），故残差注定在 1e-12 量级。
    #   正确做法分两层：
    #     (a) **符号层（严格，残差 = 0）**：用 Fraction 精确算术，把 α 换成**定义式**
    #         α ≔ e²/(4πε₀ħc)、m_P² ≔ ħc/G，两侧共用同一个 Fraction(π)，则
    #         α·(m_P/m_p)² ≡ [e²/(4πε₀ħc)]·[ħc/(G m_p²)] ≡ e²/(4πε₀ G m_p²)，
    #         ħc 在有理数域中**精确相消** ⇒ 残差严格 0（真恒等式，非数值近似）。
    #     (b) **数值层**：用十进制 α 代入，残差须 ≤ α 的末位半刻度相对量 6.85e-12。
    Fr_pi = Fraction(PI)
    fr = lambda d: Fraction(Dc(d))
    lhs_F = (fr(CD.e) ** 2) / (4 * Fr_pi * fr(CD.eps0) * fr(CD.G) * fr(CD.m_p) ** 2)
    alpha_def_F = (fr(CD.e) ** 2) / (4 * Fr_pi * fr(CD.eps0) * fr(CD.hbar) * fr(CD.c))
    rhs_F = alpha_def_F * (fr(CD.hbar) * fr(CD.c) / fr(CD.G)) / fr(CD.m_p) ** 2
    sym_zero = (lhs_F - rhs_F == 0)
    alpha_def = (CD.e * CD.e) / (Dc(4) * PI * CD.eps0 * CD.hbar * CD.c)
    r_alpha = rel(CD.alpha, alpha_def)
    half_ulp_alpha = Dc("5e-14") / CD.alpha          # α 公布末位 1e-13 的半刻度相对量
    selfchk("P03 自检：恒等式 α(m_P/m_p)² ≡ e²/(4πε₀Gm_p²)（Fraction 符号层，残差严格 0）",
            sym_zero, "符号残差 = %s" % ("0（精确相消）" if sym_zero else "非 0 ⇒ 不是恒等式"))
    selfchk("P03″ 自检：十进制 α 与定义式 e²/(4πε₀ħc) 的差异 ≤ 末位半刻度 %.2E"
            % half_ulp_alpha, r_alpha <= half_ulp_alpha,
            "%.2E ≤ %.2E" % (r_alpha, half_ulp_alpha))
    selfchk("P03′ 自检：α_G(m_p) 与教科书 5.9e-39 相对差 <1e-2",
            rel(aG_mp, Dc("5.9e-39")) < Dc("1e-2"), "%.6E" % aG_mp)
    add("P03 **预言3 F_E/F_G = α(m_P/m_p)² 是恒等式（零信息量）+ 未声明能标 + 范畴混装**",
        "FAIL",
        "① **恒等式（本册给出符号层证明，非数值近似）**：Fraction 精确算术下 "
        "α(m_P/m_p)² − e²/(4πε₀Gm_p²) ≡ 0（ħc 精确相消，残差严格 0）；"
        "改用来料的十进制 α 代入则残差 %.2E，恰与其末位半刻度 %.2E 同量级，"
        "即**差异 100%% 来自 α 的公布位数** ⇒ 该「预言」是**定义式重排**，不含任何新物理。"
        "② **E9 能标**：该比值实为**质子标度**的静态比（α_G(m_p)=Gm_p²/(ħc) = %.6E，"
        "正是教科书「质子-质子 5.9e−39」）⇒ 来料**未声明能标**，违反 E9。"
        "③ **F4 范畴**：α 是**无量纲规范耦合**（[α]=M⁰）；α_G 由**带量纲**的 G 经 "
        "α_G(E)=GE² 化来，且是四者中**唯一随能标增长**的 ⇒ 二者不属同一比较范畴，"
        "并列进同一比值表属**范畴混装**，违反 F4。"
        % (r_id, half_ulp_alpha, aG_mp),
        note="r22 D05 记为 PASS；本册订正为 FAIL/零信息——PASS 只说明算得对，不说明有内容"
             "｜附带：直接算 e²/(4πε₀Gm_p²) = %.10E、来料式 α(m_P/m_p)² = %.10E"
             % (ratio_direct, ratio_formula))

    add("P04 预言4（∇κ·∇τ=0 ⇒ 正交分解）**已被 r22 判 FAIL，续篇未回应**",
        "FAIL",
        "r22 C09：该约束是单个齐次方程，来料写的「∇ρ·∇b=0 **且** |∇ρ|=|∇b|」是"
        "**2 个独立条件的充分非必要子集**，过约束 1 维（机器反例 cos θ = 6.1237E−01）。"
        "r22 C10：径向下 Proca + 正交 + 双质量场三者不可同时成立。"
        "⇒ 续篇把它当作「可做出的预言」列出，**未引用也未回应这两条既有否证**。",
        note="同 r22 C09/C10；本册记「续篇未回应既有否证」")


# ===========================================================================
# §10 证伪层
# ===========================================================================
def section_falsify():
    print("\n" + "=" * 78)
    print("§10′ 证伪判据层（第十章 10.2）")
    print("=" * 78)

    add("Q01 判据1「有质量粒子世界线不可能是类光」⇒ **按主流物理该条件已触发**（或术语歧义）",
        "BOUNDARY",
        "按字面读：有质量粒子世界线在 SR 中**必为类时**（ds²>0），不可能是类光 ⇒ "
        "该「未来的证伪条件」**在主流框架内已经成立**，只是来料选择保留公设（终审 3 已承认）。"
        "若「类光螺旋」指内部相位以 c 传播（zitterbewegung 式重读），则需**澄清术语**，"
        "且该重读下 L0 不产生新内容。⇒ 无论如何，把它列为「未来证伪条件」是不准确的。",
        note="术语歧义必须消解，否则判据 1 既不能确认也不能否证")

    add("Q02 判据2（势函数不满足汤川/库仑）**可操作** ✓，但作用域已被自缩",
        "PASS",
        "这是四条中**真正可操作**的一条：汤川/库仑形式是定量可测的。"
        "但来料已用「TUFT 划定边界」把 QCD 排除 ⇒ 实际作用域 = 引力/电磁/弱/剩余核力（见 P01）。")

    add("Q03 判据3（剩余核力不遵循指数衰减）⇒ **现状已在边缘，非纯粹的未来条件**",
        "BOUNDARY",
        "现代核子-核子势（如 AV18 / chiral EFT）在 r ≲ 0.5 fm 存在**强排斥芯**，"
        "并非纯 Yukawa；单玻色子交换只是**长程部分的一阶近似**。"
        "⇒ 「剩余核力是否遵循汤川」在当代数据下**已部分偏离**，来料把它写成"
        "纯粹的未来判据 ⇒ 状态应记为「边缘已触发，待裁定」。",
        note="判据的现状必须先查，只看未来会漏掉已触发的部分")

    add("Q04 判据4 **含不可证伪的逃生舱** ⇒ FAIL",
        "FAIL",
        "判据4 写「∇κ·∇τ ≠ 0 **且无法施加** ∇ρ·∇b=0、|∇ρ|=|∇b| 约束 ⇒ 失效」。"
        "其中「无法施加约束」是**由作者自由选择的豁免条件**：只要观测到 ≠0，"
        "总可以宣称「已施加约束」来规避 ⇒ **没有可设想的观测能触发该判据**。"
        "⇒ 这是**不可证伪**的判据（本仓库 XIII/XIV 定型的「豁免型/单侧性」纪律的直接实例）。",
        note="凡含「且无法……」式豁免的判据，必须先问：什么观测能让它触发？")

    add("Q05 **边界划定本身合法，但需补一条元规则** ⇒ 否则证伪层会被架空",
        "BOUNDARY",
        "「QCD 线性势不证伪，因为 TUFT 明确划定边界」——**划定边界是合法的科学做法**。"
        "但若不设限制，同一招可用来豁免判据 2、3（「我把 QCD 划出去」→"
        "「我把任何不符的力都划出去」）⇒ 整个证伪层被架空。"
        "建议补一条**元规则**：豁免条款必须①**预先登记**（在见到反例之前），"
        "②**不得针对已知反例事后追加**，③给出**边界外的判据由谁承接**。",
        note="这是续篇最值得补的一条方法论缺口")


# ===========================================================================
# 附录D
# ===========================================================================
def section_appendix():
    print("\n" + "=" * 78)
    print("附录D  审计表订正")
    print("=" * 78)

    for nm, v, det in [
        ("R01 「可证伪性 PASS」", "BOUNDARY",
         "应降为 BOUNDARY：判据4 不可证伪（Q04）、判据1 已触发/歧义（Q01）、"
         "判据3 边缘已触发（Q03）⇒ 四条中仅判据2 完全可操作。"),
        ("R02 「力强比值预测 PASS」", "CORRECTED",
         "应改为 **INFO（恒等式，零信息量）**：见 P03，算得对不等于有内容；"
         "且未声明能标（E9）、范畴混装（F4）。r22 D05 记为 PASS，本册订正。"),
        ("R03 「数值仿真稳定性 PASS」", "FAIL",
         "应改为 FAIL：「稳定」不等于「正确」——8.2 代码固化了 r22 C08 的符号错误（N04，"
         "偏差 2.65E−02 vs 独立式 4.0E−13），且仿真对此类错误**结构性免疫**。"
         "⇒ 该行 PASS 会掩盖真实缺陷，必须订正。"),
        ("R04 「内生基本常数 FAIL」", "PASS",
         "与 r22 B06/E02 一致，本册**确认**：α=b/ρ 为连续比，无内部约束可锁定。"),
        ("R05 「与 GR 本体兼容：冲突」", "CORRECTED",
         "判定方向正确，但归因需修正：不应把「弱场引力红移」列入无法还原（见 M02）。"),
        ("R06 「量纲闭合 PASS」", "PASS",
         "独立复核通过：α=b/ρ 无量纲、κ²+τ²=(ω/c)² 同为 L⁻²、λ=ħ/(mc) 为 L、"
         "U ∝ e^{−r/λ}/r 的系数承担剩余量纲 ⇒ 量纲闭合成立。"),
        ("R07 「经典极限还原 PASS」", "CORRECTED",
         "归因应修正：还原的是**势形式**（Yukawa 的 μ→0 极限），不是螺旋几何——"
         "r22 C11 已证 L2 场论中完全不出现 κ、τ、α，A08 已证换成任意常速轨道结果逐字不变。"),
    ]:
        add(nm, v, det)


# ===========================================================================
# 结构层
# ===========================================================================
def section_struct():
    print("\n" + "=" * 78)
    print("结构层  续篇的净增量")
    print("=" * 78)

    add("S01 **「推进到可数值检验、可实验判定层级」这一声称未兑现**（本册头条）",
        "FAIL",
        "逐章核减：第八章 = 复述既有恒等式（N02/N03）+ **固化一个已知错误**（N04）+ "
        "**虚假精度**（N05）+ 循环恒等（N06）+ **不可复核的 χ²**（N07）+ **循环的 MCMC**（N08）+ "
        "弱于既有的结论（N09）；第九章 = **描述性**文献对比（M01–M05，仅 M02/M04 有可判定内容）；"
        "第十章 = 4 条预言中 **2 条为恒等式或已被否证**（P03/P04）、"
        "4 条判据中**仅 2 条真正可操作**（Q02、Q03 边缘）。"
        "⇒ **净增的可判定内容约为 1 条（判据 2，且作用域已自缩）**，"
        "且未改变 r22 任何一条 L5 硬 FAIL 的状态。",
        note="用本仓库判别式语言：描述成本 ≫ 压缩增益（Net < 0），且新章不产生新内容")

    add("S02 续篇提出的「下一步」中，**前两条已被 r22 判过，存在重复立项风险**",
        "BOUNDARY",
        "来料给出三个方向：①第十一章非齐次/非线性 Proca 修复禁闭；"
        "②第十二章拓扑几何内生 α；③LaTeX 化。"
        "其中①已被 r22 判为 **FAIL/无内生路径**（2A 的 S(r) 是外部输入；"
        "2B 的非线性是 D06 的**既成事实**而非选项）；"
        "②已被 r22 **B06 构造族证否**（纯几何路线），其唯一未否证入口是 F07 的"
        "「非平庸作用量」，属**修改公设集**的框架层决策。"
        "⇒ 续篇**未引用这些既有结论** ⇒ 若直接开写会重复撞墙。",
        note="回答来料末尾提问：见本册 §建议")


# ===========================================================================
def main():
    print("=" * 78)
    print("TUFT 垂直原理四力统一 · 续篇（第八~十章 + 附录D）全维机器审计（r23）")
    print("=" * 78)
    print("分工：r22 已审 L0/L1/L2/L3/L5；本册只审**新给的第八~十章与附录D**，")
    print("      与 r22 重合者标注「同 r22 Xnn」，只记复发 / 未回应 / 口径订正。")

    section8()
    section9()
    section10()
    section_falsify()
    section_appendix()
    section_struct()

    verdicts = {}
    for it in ITEMS:
        verdicts[it["verdict"]] = verdicts.get(it["verdict"], 0) + 1
    self_ok = sum(1 for s in _SELF if s["ok"])

    payload = {
        "title": "TUFT 垂直原理四力统一 · 续篇（第八~十章 + 附录D）全维机器审计（r23）",
        "engine": os.path.basename(__file__),
        "date": "2026-10-10",
        "division_of_labor": "r22 已审 L0/L1/L2/L3/L5；本册只审新增的第八~十章与附录D",
        "items": ITEMS,
        "verdicts": verdicts,
        "route_answers": {
            "第十一章（非齐次/非线性 Proca 修复禁闭）":
                "不推荐先写：r22 已判 FAIL/无内生路径（2A 源项外输、2B 非线性是 D06 既成事实）",
            "第十二章（拓扑几何内生 α）":
                "不推荐按原计划写：r22 B06 构造族已证否纯几何路线；"
                "唯一未否证入口 = 非平庸作用量（F07），属修改公设集的框架层决策",
            "LaTeX 化": "无争议，可并行；但建议先做 P0 改稿（见下）",
        },
        "P0_actions": [
            "修正 8.2 代码 grad_kappa_tau_dot 的 term1 符号（|∇b|²−|∇ρ|² → |∇ρ|²−|∇b|²）",
            "删除或降级「250 位高精度」的表述，改为按输入有效位（6 位）声明精度",
            "补 χ²_red 的 N_data 与 dof",
            "声明 λ_π 口径（π⁰ 还是 π±）",
            "把「四力大统一」改写为「三力 + 剩余核力」，或显式定义「四力」的所指",
            "给证伪判据 4 去掉「且无法施加约束」这一逃生舱",
            "补一条豁免元规则（预先登记 / 不做事后追加 / 边界外责任方）",
        ],
        "selfcheck": {"n_ok": self_ok, "n_all": len(_SELF), "items": _SELF},
    }

    os.makedirs(OUTDIR, exist_ok=True)
    stem = "TUFT-垂直原理续篇八至十章_全维审计_2026-10-10"
    json_path = os.path.join(OUTDIR, stem + ".json")
    md_path = os.path.join(OUTDIR, stem + ".md")
    txt_path = os.path.join(OUTDIR, stem + "_report.txt")

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# TUFT 垂直原理四力统一 · 续篇（第八~十章 + 附录D）全维机器审计（r23）")
    lines.append("")
    lines.append("- 日期：2026-10-10")
    lines.append("- 引擎：`源码/%s`（纯标准库，Decimal 60 位）" % os.path.basename(__file__))
    lines.append("- 读数：**条目 %d ｜ %s ｜ 自检 %d/%d**"
                 % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False),
                    self_ok, len(_SELF)))
    lines.append("")
    lines.append("## 一、逐条读数")
    lines.append("")
    lines.append("| # | 条目 | 判定 | 说明 |")
    lines.append("|---|---|---|---|")
    for i, it in enumerate(ITEMS, 1):
        d = it["detail"].replace("|", "\\|")
        lines.append("| %d | %s | **%s** | %s |" % (i, it["name"], it["verdict"], d))
    lines.append("")
    lines.append("## 二、回答来料末尾的提问（下一步怎么走）")
    lines.append("")
    for k, v in payload["route_answers"].items():
        lines.append("- **%s**：%s" % (k, v))
    lines.append("")
    lines.append("## 三、P0 改稿清单（当天可完成，零争议）")
    lines.append("")
    for a in payload["P0_actions"]:
        lines.append("- %s" % a)
    lines.append("")
    lines.append("## 四、自检")
    lines.append("")
    for s in _SELF:
        lines.append("- [%s] %s %s" % ("PASS" if s["ok"] else "FAIL", s["name"],
                                       ("（%s）" % s["detail"]) if s["detail"] else ""))
    lines.append("")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    with open(txt_path, "w", encoding="utf-8") as fh:
        fh.write("TUFT 垂直原理续篇（八~十章+附录D）全维审计 r23 · 运行记录\n")
        fh.write("=" * 74 + "\n")
        fh.write("条目 %d ｜ %s\n自检 %d/%d\n\n"
                 % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False),
                    self_ok, len(_SELF)))
        for i, it in enumerate(ITEMS, 1):
            fh.write("[%02d] %-9s %s\n     %s\n" % (i, it["verdict"], it["name"],
                                                    it["detail"]))
            if it["note"]:
                fh.write("     注: %s\n" % it["note"])
        fh.write("\n" + "-" * 74 + "\n")
        for k, v in payload["route_answers"].items():
            fh.write("%s: %s\n" % (k, v))

    print("")
    print("=" * 78)
    print("读数：条目 %d ｜ %s" % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False)))
    print("自检：%d/%d" % (self_ok, len(_SELF)))
    for s in _SELF:
        if not s["ok"]:
            print("  自检未过：%s %s" % (s["name"], s["detail"]))
    print("产物：")
    for p in (json_path, md_path, txt_path):
        print("  " + os.path.relpath(p, BASE))
    print("=" * 78)
    sys.exit(0 if self_ok == len(_SELF) else 1)


if __name__ == "__main__":
    main()
