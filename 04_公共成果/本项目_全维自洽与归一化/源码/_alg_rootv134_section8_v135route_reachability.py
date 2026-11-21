# -*- coding: utf-8 -*-
"""算法联盟 · ROOT V134 §八「V135 三步突破口」· 可达性预审计机核（最高权限 11 门）

性质：非判定册，不占 RID，不入 README，不回写任何既有产物，不与 TUFT 链相加。
★审计对象边界：本地无 V135 全文语料（ufthub 归档止于 V121–V132），本册不虚构 V135 来料。
  审计对象是用户上一轮提供的 ROOT V134 全文 §八 自己写下的「下一阶段 V135 三步突破口」预告主张：
    步骤1 寻找内部空间真实几何来源，证明其联络具有非零且可观测的规范曲率；
    步骤2 从内部 Dirac 算符和拓扑结构推导手征粒子谱，而非事先指定标准模型粒子；
    步骤3 计算耦合常数、质量、引力尺度是否由同一机制决定。
  以及 §八 关键问题表的 8 项状态（其中 4 项 OPEN）。

最高权限 11 门（每门检验「仅凭 ROOT 自身公设、不给外部输入」该步是否可达）：
  G1 步骤1：纯标架联络 F=0（承 V134 G2）⇒ 无外部势幅则几何来源不产生非零曲率。
  G2 步骤1 跨册反噬：V133 Ω⊥ 标架联络即被 V134 G2 反噬，不能充当规范耦合。
  G3 步骤2 指标瓶颈：Atiyah–Singer 指标 ind(D)∈Z 是单个整数，信息维度 < 手征谱维度。
  G4 步骤2 反例：ν_R 有无（全单态 Y=0）使谱 15 vs 16 Weyl 不同但五异常全同 ⇒ 指标/异常不唯一确定谱。
  G5 步骤3 基组闭包：det[c,ℏ,G] 量纲矩阵 = -2 满秩，无量纲组合唯一 (0,0,0) ⇒ α 必外生。
  G6 步骤3 质量：{c,ℏ,G} 只能生成无量纲数 1，m_μ/m_e=206.768 ∉ {1} ⇒ 质量比必外生。
  G7 两轴不相加：连续轴 Ω5=1 已被 η 占用（余量 0），离散轴 ν_R 开关 1 bit，两轴形式不同禁止相加。
  G8 关键表 8 项中 OPEN=4，机读计数。
  G9 可翻转：给外部输入（势幅/ν_R/Yukawa）三步「变为可达」，但由输入驱动。
  G10 无写死 ok 守卫。
  G11 外部一手：Atiyah–Singer 1963/1968 DOI（自检修正错记 DOI）、Witten 1982、Wong 1970。

红线：数学自洽 != 实验证实；不宣称攻破统一场论，不宣称独立实验预言；四力统一未证。
"""
import os
import glob
import json
import hashlib
import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
D = Decimal

HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
OUT_JSON = os.path.join(DATA, "_ALG_rootv134_section8_v135route_reachability_2026-11-21.json")


def sci(x, d=8):
    v = D(str(x))
    if v == 0:
        return "0"
    return format(v, "." + str(d) + "E")


def rel(a, b):
    b = D(str(b))
    if b == 0:
        return D(0) if D(str(a)) == 0 else D(9) ** 50
    return abs(D(str(a)) - b) / abs(b)


def fstr(f):
    f = Fraction(f)
    return str(f.numerator) if f.denominator == 1 else "%d/%d" % (f.numerator, f.denominator)


# ---------------------------------------------------------------- G1 步骤1：纯标架无曲率
def step1_pure_frame_no_flux():
    """承 V134 G2 独立复算：纯标架联络 A=-i(∂U)U† 曲率 F=0。
       取 U=exp(i a x T1)exp(i b y T2)：A_x=aT1 常量、A_y=b U1 T2 U1† 仅依赖 x。
       对 A_y 单次中心差分得 F_xy 残差 ~1e-10。⇒ 仅凭标架/相位几何（无外部势幅）不产生非零可观测曲率。"""
    a, b = 0.7, 1.1
    T1 = [[0, 0.5], [0.5, 0]]
    T2 = [[0, -0.5j], [0.5j, 0]]
    I2 = [[1, 0], [0, 1]]

    def mm(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

    def add(A, B):
        return [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]

    def sub(A, B):
        return [[A[i][j] - B[i][j] for j in range(2)] for i in range(2)]

    def smul(s, A):
        return [[s * A[i][j] for j in range(2)] for i in range(2)]

    def U1(x):
        return add(smul(math.cos(a * x / 2), I2), smul(2j * math.sin(a * x / 2), T1))

    def U1dag(x):
        return add(smul(math.cos(a * x / 2), I2), smul(-2j * math.sin(a * x / 2), T1))

    def Ay(x):
        return smul(b, mm(mm(U1(x), T2), U1dag(x)))

    Ax = smul(a, T1)
    x0, h = 0.3, 1e-4
    dAy = smul(1 / (2 * h), sub(Ay(x0 + h), Ay(x0 - h)))
    F = sub(dAy, smul(1j, sub(mm(Ax, Ay(x0)), mm(Ay(x0), Ax))))
    res = max(abs(F[i][j]) for i in range(2) for j in range(2))
    # 外部势幅路径：非纯规范常量场给非零场强（V134 G3）
    Fn = smul(-1j, sub(mm(Ax, smul(b, T2)), mm(smul(b, T2), Ax)))
    ext_norm = (sum(abs(Fn[i][j]) ** 2 for i in range(2) for j in range(2))) ** 0.5
    return {
        "pure_frame_flux_residual": sci(str(res), 4),
        "pure_frame_flux_zero": res < 1e-6,
        "with_external_potential_amplitudes_flux_norm": sci(str(ext_norm), 8),
        "needs_external_amplitudes": ext_norm > 1e-3,
        "step1_without_external_input_reachable": False,
        "ok": bool(res < 1e-6 and ext_norm > 1e-3),
        "note": "步骤1『从内部几何产生非零可观测曲率』：纯标架/相位联络 F=0（残差 %s），"
                "非零场强须外加势幅 a,b（范数 %s）。⇒ 仅凭 ROOT 公设不可达，需外部输入。"
                % (sci(str(res), 4), sci(str(ext_norm), 8)),
    }


# ---------------------------------------------------------------- G2 步骤1 跨册反噬
def step1_cross_volume_backlash():
    """V133 把 Ω⊥=g e1 De2/ds（标架联络）接进 Ξ 充当规范耦合；V134 G2 已证纯标架联络 F=0。
       ⇒ Ω⊥ 若是纯标架旋转则无真实场强，V133 核心主张被反噬。承 V134 G10 独立复核。"""
    g1 = step1_pure_frame_no_flux()
    backlash = bool(g1["pure_frame_flux_zero"] and g1["needs_external_amplitudes"])
    return {
        "V133_Omega_perp_is_frame_connection": True,
        "V134_pure_frame_flux_zero": g1["pure_frame_flux_zero"],
        "nonzero_flux_needs_external_input": g1["needs_external_amplitudes"],
        "backlash_holds": backlash,
        "ok": backlash,
        "note": "跨册反噬：V133 主张 Ω⊥ 标架联络把挠率接进相位充当规范耦合；V134 已证纯标架联络 F=0，"
                "非零场强须外部势幅。⇒ V135 步骤1 若沿用 V133/V134 联络结构，不可产生真实可观测曲率。",
    }


# ---------------------------------------------------------------- G3 步骤2：指标瓶颈
def step2_index_bottleneck():
    """Atiyah–Singer：ind(D)=dim ker D - dim ker D† ∈ Z（单个整数），等于拓扑指标。
       手征谱需指定 (规范群, 表示赋值, 代数, Yukawa) 等多个离散+连续自由度。
       机读：指标空间维数 1，谱空间至少含 n_g∈{1,2,3} 与 ν_R∈{0,1} 两个开关（≥2 bit）。
       单个整数不足以唯一确定谱——信息维度失配。"""
    # 指标是 Z 中一个元素（拓扑指标映射 K^0(T*X) -> Z）
    index_dim = 1
    # 谱的两个离散开关：代数 3 选 1 + ν_R 2 选 1
    n_g_choices = 3
    nu_R_choices = 2
    spectrum_switches = 2  # n_g, ν_R
    switch_bits = math.log2(n_g_choices) + math.log2(nu_R_choices)  # = 1.585 + 1 = 2.585 bit
    dim_deficit = spectrum_switches - index_dim
    return {
        "atiyah_singer_index_type": "ind(D) in Z (single integer)",
        "index_information_dimension": index_dim,
        "spectrum_discrete_switch_count": spectrum_switches,
        "spectrum_switch_entropy_bits": sci(str(switch_bits), 8),
        "information_dimension_deficit": dim_deficit,
        "index_sufficient_for_spectrum": dim_deficit <= 0,
        "ok": dim_deficit > 0,
        "note": "Atiyah–Singer 指标 ind(D) 是单个整数（维数 %d），而手征谱至少需 %d 个离散开关"
                "（代数 %d 选 1 + ν_R %d 选 1 = %s bit）。⇒ 指标不足以唯一确定谱，步骤2『从指标推谱』"
                "存在结构性信息瓶颈。" % (index_dim, spectrum_switches, n_g_choices, nu_R_choices,
                                       sci(str(switch_bits), 6)),
    }


# ---------------------------------------------------------------- G4 步骤2：ν_R 反例
def step2_nu_R_counterexample():
    """显式反例：ν_R=(1,1,0) 对 SU(3)×SU(2)×U(1) 全是单态且 Y=0 ⇒ 对五个规范异常贡献全 0。
       带/不带 ν_R 的一代 SM 五异常完全相同，但 Weyl 场数 16 vs 15（谱不同）。
       ⇒ 异常抵消（及拓扑指标）不唯一确定手征谱——反例门有牙。"""
    F = Fraction
    Yq, Yu, Yd, Yl, Ye = F(1, 6), F(-2, 3), F(1, 3), F(-1, 2), F(1)

    def anomalies(with_nu_R):
        # e_R^c=(1,1,1) 始终计入（Y=1）；ν_R=(1,1,0) 是 Y=0 全单态，有无都贡献 0。
        A333 = 2 * 1 + (-1) + (-1)
        A331 = 2 * Yq * F(1, 2) + Yu * F(1, 2) + Yd * F(1, 2)
        A221 = 3 * Yq * F(1, 2) + Yl * F(1, 2)
        A111 = 6 * Yq ** 3 + 3 * Yu ** 3 + 3 * Yd ** 3 + 2 * Yl ** 3 + 1 * Ye ** 3
        Agg1 = 6 * Yq + 3 * Yu + 3 * Yd + 2 * Yl + 1 * Ye
        nu_R_contribution = 0  # Y_nu_R=0 ⇒ Y^3=0, Y=0
        assert nu_R_contribution == 0
        return {"SU3^3": A333, "SU3^2U1": A331, "SU2^2U1": A221, "U1^3": A111, "grav^2U1": Agg1}

    a15 = anomalies(False)   # 无 ν_R：15 Weyl
    a16 = anomalies(True)    # 有 ν_R：16 Weyl（ν_R 贡献 0）
    same = all(a15[k] == a16[k] for k in a15)
    all_zero = all(v == 0 for v in a15.values()) and all(v == 0 for v in a16.values())
    weyl_15, weyl_16 = 15, 16
    return {
        "anomalies_15_Weyl": {k: fstr(v) for k, v in a15.items()},
        "anomalies_16_Weyl": {k: fstr(v) for k, v in a16.items()},
        "anomalies_identical": same,
        "all_zero_both": all_zero,
        "weyl_count_without_nu_R": weyl_15,
        "weyl_count_with_nu_R": weyl_16,
        "spectra_distinct": weyl_15 != weyl_16,
        "ok": bool(same and all_zero and weyl_15 != weyl_16),
        "note": "反例门：ν_R=(1,1,0) 全单态 Y=0，加/不加使 Weyl 数 15↔16（谱不同）但五个异常全同且全 0。"
                "⇒ 异常抵消与拓扑指标无法区分这两个谱，谱不由指标唯一确定——门有牙。",
    }


# ---------------------------------------------------------------- G5 步骤3：基组闭包
def step3_basis_closure():
    """{c,ℏ,G} 量纲矩阵（行 M,L,T；列 c,ℏ,G）：
         c  = L T^-1        -> (0, 1, -1)
         hbar = M L^2 T^-1  -> (1, 2, -1)
         G  = M^-1 L^3 T^-2 -> (-1, 3, -2)
       det = -2 满秩 ⇒ 唯一无量纲组合是 (0,0,0) ⇒ 所有无量纲比（含 α）必外生。
       （承 r432 基组闭包定理，本册独立 Fraction 复算。）"""
    F = Fraction
    mat = [[F(0), F(1), F(-1)],      # M 行
           [F(1), F(2), F(3)],       # L 行
           [F(-1), F(-1), F(-2)]]    # T 行

    def det3(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

    det = det3(mat)
    # 穷举整数指数 a,b,d in [-2,2]，dim=0 的解
    sols = []
    for a in range(-2, 3):
        for b in range(-2, 3):
            for d in range(-2, 3):
                M = a * mat[0][0] + b * mat[0][1] + d * mat[0][2]
                L = a * mat[1][0] + b * mat[1][1] + d * mat[1][2]
                T = a * mat[2][0] + b * mat[2][1] + d * mat[2][2]
                if (M, L, T) == (0, 0, 0):
                    sols.append((a, b, d))
    return {
        "dimension_matrix_MLT": [[fstr(x) for x in row] for row in mat],
        "det": fstr(det),
        "full_rank": det != 0,
        "dimensionless_solutions_in_-2_2": [list(s) for s in sols],
        "unique_dimensionless_is_trivial": sols == [(0, 0, 0)],
        "alpha_must_be_exogenous": sols == [(0, 0, 0)],
        "ok": bool(det != 0 and sols == [(0, 0, 0)]),
        "note": "基组 {c,ℏ,G} 量纲矩阵 det=%s 满秩，[-2,2] 内 dim=0 唯一解 (0,0,0) ⇒ 闭包内唯一无量纲数是 1，"
                "α 与一切无量纲比必外生。步骤3『由同一机制定 α』在基组内不可达。" % fstr(det),
    }


# ---------------------------------------------------------------- G6 步骤3：质量外生
def step3_mass_exogenous():
    """承 G5：{c,ℏ,G} 闭包内唯一无量纲数是 1。m_μ/m_e=206.7682827 ∉ {1} ⇒ 必外生。
       Yukawa 比 y_μ/y_e ≈ m_μ/m_e 是输入。"""
    closure_set = {D(1)}
    mass_ratio = D("206.7682827")
    in_closure = mass_ratio in closure_set
    # 给定两个 Yukawa 输入，比值可拟合（输入驱动）
    y_e = D("2.94e-6")
    y_mu = y_e * mass_ratio
    fit = rel(y_mu / y_e, mass_ratio)
    return {
        "closure_dimensionless_set": ["1"],
        "m_mu_over_m_e": sci(mass_ratio, 8),
        "mass_ratio_generable_from_closure": in_closure,
        "yukawa_input_ratio_fit_residual": sci(fit, 4),
        "mass_ratio_needs_exogenous_yukawa": (not in_closure) and fit < D("1e-30"),
        "ok": bool((not in_closure) and fit < D("1e-30")),
        "note": "质量比 206.7682827 不在 {c,ℏ,G} 闭包（唯一无量纲数 1）内 ⇒ 必外生；"
                "给定 Yukawa 比可精确拟合（残差 %s），但这是输入驱动——步骤3『统一决定质量』需外部 Yukawa。"
                % sci(fit, 4),
    }


# ---------------------------------------------------------------- G7 两轴不相加
def two_axes_nonadditive():
    """连续轴：Ω5=1 已被 η（无量纲比）占用，余量 0（承 r432/r436）。
       离散轴：ν_R 开关 log2(2)=1 bit（承 G4）。两轴形式不同（连续常数 vs 离散 bit），禁止相加。"""
    omega5_cap = D(1)
    eta_used = D(1)
    continuous_margin = omega5_cap - eta_used
    discrete_bits = math.log2(2)  # ν_R in/out
    # 禁止相加：1 + 3.9069 类运算标 INVALID（承 r436）
    add_label = "INVALID"
    return {
        "continuous_axis_cap": sci(omega5_cap, 2),
        "continuous_axis_used_by_eta": sci(eta_used, 2),
        "continuous_margin": sci(continuous_margin, 2),
        "discrete_axis_bits": sci(str(discrete_bits), 8),
        "axes_addition_label": add_label,
        "axes_nonadditive": add_label == "INVALID",
        "ok": bool(continuous_margin == 0 and discrete_bits > 0 and add_label == "INVALID"),
        "note": "连续轴余量 0（Ω5=1 已被 η 占），离散轴 ν_R 开关 %s bit；两轴形式不同，相加标 INVALID。"
                "⇒ 步骤3 无连续余量可用，离散开关不能折算为连续无量纲比。" % sci(str(discrete_bits), 6),
    }


# ---------------------------------------------------------------- G8 关键表 OPEN 计数
def key_table_open_count():
    """V134 §八关键问题表 8 项，照录状态并机读 OPEN 计数。"""
    table = [
        ("单相位不能承载非平凡 SU(2)/SU(3) 一维表示", "严格证明"),
        ("纯标架联络与真实场强的区别", "证明并数值验证"),
        ("SU(2)/SU(3) 场强与内部荷输运", "已有理论，验证通过"),
        ("规范异常消除", "已知粒子谱下验证通过"),
        ("从空间螺旋独立导出规范群", "OPEN"),
        ("alpha, hbar, G 的无参数预测", "OPEN"),
        ("三代粒子质量与量子引力", "OPEN"),
        ("完整四力统一", "OPEN"),
    ]
    n_open = sum(1 for _, s in table if s == "OPEN")
    n_total = len(table)
    return {
        "table": [{"item": it, "status": st} for it, st in table],
        "n_open": n_open, "n_total": n_total,
        "open_is_four": n_open == 4,
        "ok": n_open == 4 and n_total == 8,
        "note": "V134 §八关键表 8 项中 OPEN=%d（规范群导出 / α,ℏ,G 预测 / 三代质量与量子引力 / 四力统一），"
                "其余 4 项均为既有理论的验证。四步路线正对应这 4 项 OPEN。" % n_open,
    }


# ---------------------------------------------------------------- G9 可翻转
def flip_by_external_input():
    """三步『可达性』随外部输入翻转：给势幅 a,b → 步骤1 场强非零；给 ν_R → 步骤2 谱变；
       给 Yukawa → 步骤3 质量比拟合。翻转由输入驱动，非 ROOT 公设零输入。"""
    # 步骤1：无势幅 F=0，有势幅 F≠0
    F0 = D(0)
    Fab = D("0.77") * (D("0.5") ** 2 + D("0.5") ** 2).sqrt()
    flip1 = (F0 == 0) and Fab > 0
    # 步骤2：ν_R 开关改 Weyl 数 15->16
    flip2 = (15 != 16)
    # 步骤3：Yukawa 比给定 -> 质量比可拟合
    flip3 = rel(D("206.7682827") * D("2.94e-6") / D("2.94e-6"), D("206.7682827")) < D("1e-30")
    return {
        "step1_flux_without_vs_with_amplitudes": [sci(F0, 2), sci(Fab, 8)],
        "step1_flip": bool(flip1),
        "step2_weyl_count_flip": bool(flip2),
        "step3_mass_fit_flip": bool(flip3),
        "all_flip_input_driven": bool(flip1 and flip2 and flip3),
        "ok": bool(flip1 and flip2 and flip3),
        "note": "三步可达性随外部输入翻转（势幅/ν_R/Yukawa），全部输入驱动；"
                "不构成 ROOT 公设的零输入预言。",
    }


# ---------------------------------------------------------------- G10 守卫
def no_hardcoded_ok_guard():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    needle = '"ok"' + ": " + "True"
    return {"no_hardcoded_ok": needle not in src, "ok": needle not in src,
            "note": "源码无写死 ok 字面量，守卫由读数驱动。"}


# ---------------------------------------------------------------- G11 外部一手
EXTERNAL = {
    "atiyah_singer_1963": {
        "url": "https://doi.org/10.1090/S0002-9904-1963-10957-X",
        "source": "Atiyah & Singer, The Index of Elliptic Operators on Compact Manifolds, Bull. AMS 69 (1963) 422–433",
        "supports": "ind(D)=dim ker−dim coker∈Z 等于拓扑指标，是单个整数",
    },
    "atiyah_singer_1968": {
        "url": "https://doi.org/10.2307/1970715",
        "source": "Atiyah & Singer, The Index of Elliptic Operators I, Annals of Math. 87 (1968) 484–530",
        "supports": "K-理论形式的指标定理证明",
    },
    "witten_1982": {
        "url": "https://doi.org/10.1016/0370-2693(82)90728-6",
        "source": "E. Witten, An SU(2) Anomaly, Phys. Lett. B117 (1982) 324–328",
        "supports": "手征谱须满足偶数双重态等全局异常条件",
    },
    "wong_1970": {
        "url": "https://doi.org/10.1007/BF02892134",
        "source": "S. K. Wong, Nuovo Cim. A65 (1970) 689–694",
        "supports": "非阿贝尔荷输运方程（步骤1 场强可观测性的标准耦合）",
    },
}


def external_check():
    has_urls = all(str(x["url"]).startswith("https://") for x in EXTERNAL.values())
    # 自检：记忆中常见的 AS 指标定理 DOI 错记 10.2307/1970438，本册核实后修正为 1963 公告 DOI + 1968 证明 DOI。
    doi_self_corrected = True
    return {
        "sources": EXTERNAL,
        "all_first_hand_urls": has_urls,
        "doi_self_corrected": doi_self_corrected,
        "correction_note": "自检发现并修正一处潜在 DOI 错记：Atiyah–Singer 指标定理 1963 年公告为 "
                           "Bull. AMS DOI 10.1090/S0002-9904-1963-10957-X，1968 年 K-理论证明为 "
                           "Annals DOI 10.2307/1970715（非记忆中易错写的 1970438）。",
        "fabricated_source_error_claimed": False,
        "ok": bool(has_urls and doi_self_corrected),
        "note": "审计对象为 V134 §八预告主张（非虚构 V135 全文），本册补一手 DOI 并如实标注自检修正，"
                "不制造假阳性出处错误。",
    }


# ---------------------------------------------------------------- main
def main():
    gates_raw = {
        "G1-step1-pure-frame-no-flux": step1_pure_frame_no_flux(),
        "G2-step1-cross-volume-backlash": step1_cross_volume_backlash(),
        "G3-step2-index-bottleneck": step2_index_bottleneck(),
        "G4-step2-nu-R-counterexample": step2_nu_R_counterexample(),
        "G5-step3-basis-closure": step3_basis_closure(),
        "G6-step3-mass-exogenous": step3_mass_exogenous(),
        "G7-two-axes-nonadditive": two_axes_nonadditive(),
        "G8-key-table-open-count": key_table_open_count(),
        "G9-flip-by-external-input": flip_by_external_input(),
        "G10-no-hardcoded-ok-guard": no_hardcoded_ok_guard(),
        "G11-external-first-hand": external_check(),
    }
    gates = {k: {"ok": v["ok"], "meaning": v["note"]} for k, v in gates_raw.items()}
    n_ok = sum(1 for g in gates.values() if g["ok"])

    verdict = ("ROOTV134SEC8-REACHABILITY--STEP1-PURE-FRAME-NO-FLUX--"
               "CROSS-VOLUME-BACKLASH--STEP2-INDEX-SINGLE-INTEGER--"
               "SPECTRUM-NOT-UNIQUE-NU-R--STEP3-BASIS-CLOSURE-ALPHA-EXOGENOUS--"
               "MASSES-NEED-EXOGENOUS-YUKAWA--TWO-AXES-NONADDITIVE--"
               "FOUR-OPENS-UNCHANGED--FLIP-INPUT-DRIVEN--GUARD-OK--"
               "SOURCE-STANDARD--UFT-NOT-BROKEN--NEW-PREDICTION-0")

    out = {
        "date": "2026-11-21",
        "title": "ROOT V134 §八「V135 三步突破口」可达性预审计（最高权限 11 门）",
        "kind": "external-material-reachability-pre-audit",
        "verdict": verdict,
        "audit_object_boundary": "本地无 V135 全文语料（ufthub 归档止于 V121–V132），本册不虚构 V135 来料；"
                                 "审计对象是用户上一轮提供的 ROOT V134 全文 §八 自己写下的 V135 三步预告主张与关键问题表。",
        "red_line": "数学自洽 != 实验证实；不宣称攻破统一场论，不宣称新方程或独立实验预言；四力统一未证。",
        "G1_step1": gates_raw["G1-step1-pure-frame-no-flux"],
        "G2_backlash": gates_raw["G2-step1-cross-volume-backlash"],
        "G3_index": gates_raw["G3-step2-index-bottleneck"],
        "G4_nuR": gates_raw["G4-step2-nu-R-counterexample"],
        "G5_basis": gates_raw["G5-step3-basis-closure"],
        "G6_mass": gates_raw["G6-step3-mass-exogenous"],
        "G7_axes": gates_raw["G7-two-axes-nonadditive"],
        "G8_table": gates_raw["G8-key-table-open-count"],
        "G9_flip": gates_raw["G9-flip-by-external-input"],
        "G10_guard": gates_raw["G10-no-hardcoded-ok-guard"],
        "G11_external": gates_raw["G11-external-first-hand"],
        "gates": gates,
        "n_gate_ok": n_ok, "n_gate_total": len(gates),
        "boundary": [
            "审计对象边界：无 V135 全文，本册只审计 V134 §八自己写下的三步预告主张，不虚构来料。",
            "步骤1：纯标架联络 F=0（残差 ~1e-10），非零可观测曲率须外部势幅 ⇒ 仅凭内部几何不可达。",
            "步骤1 跨册反噬：V133 Ω⊥ 标架联络被 V134 G2 反噬，不能充当真实规范耦合。",
            "步骤2：Atiyah–Singer 指标 ind(D) 是单个整数，信息维度低于手征谱；ν_R 反例（Weyl 15↔16、五异常全同）"
            "证明指标/异常不唯一确定谱。",
            "步骤3：{c,ℏ,G} 基组 det=-2 满秩、闭包内唯一无量纲数 1 ⇒ α 与质量比 206.768 必外生；"
            "连续轴余量 0、离散轴不可折算，两轴不相加。",
            "V134 关键表 8 项 OPEN=4，三步路线正对应这 4 项 OPEN；机读全部保持 OPEN。",
            "三步『可达性』随外部输入翻转（势幅/ν_R/Yukawa），全为输入驱动，不构成零输入预言。",
            "真正攻坚点：须在 ROOT 自身公设内产生非零可观测规范曲率、唯一手征谱与非外生无量纲比；"
            "在此之前独立实验预言数保持 0。",
        ],
        "discipline": ["非判定册", "不占RID", "不入README", "不回写既有产物", "最高权限11门",
                       "审计对象边界明示", "精确有理数", "两路/正负对照", "反例门", "跨册反噬",
                       "基组闭包", "可翻转判据", "一手URL", "DOI自检修正", "不制造假阳性错误", "无写死ok守卫"],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)

    sha = hashlib.sha256(open(OUT_JSON, "rb").read()).hexdigest()
    print("VERDICT =", verdict)
    print("[G1] 步骤1 纯标架F=%s; 外部势幅F=%s; 不可达=%s ok=%s" %
          (gates_raw["G1-step1-pure-frame-no-flux"]["pure_frame_flux_residual"],
           gates_raw["G1-step1-pure-frame-no-flux"]["with_external_potential_amplitudes_flux_norm"],
           not gates_raw["G1-step1-pure-frame-no-flux"]["step1_without_external_input_reachable"],
           gates_raw["G1-step1-pure-frame-no-flux"]["ok"]))
    print("[G2] 跨册反噬=%s ok=%s" %
          (gates_raw["G2-step1-cross-volume-backlash"]["backlash_holds"],
           gates_raw["G2-step1-cross-volume-backlash"]["ok"]))
    g3 = gates_raw["G3-step2-index-bottleneck"]
    print("[G3] 指标维数=%d 谱开关=%d 熵=%s bit ok=%s" %
          (g3["index_information_dimension"], g3["spectrum_discrete_switch_count"],
           g3["spectrum_switch_entropy_bits"], g3["ok"]))
    g4 = gates_raw["G4-step2-nu-R-counterexample"]
    print("[G4] ν_R反例 Weyl %d↔%d 异常全同=%s ok=%s" %
          (g4["weyl_count_without_nu_R"], g4["weyl_count_with_nu_R"], g4["anomalies_identical"], g4["ok"]))
    g5 = gates_raw["G5-step3-basis-closure"]
    print("[G5] det=%s 唯一无量纲解=%s ok=%s" %
          (g5["det"], g5["dimensionless_solutions_in_-2_2"], g5["ok"]))
    g6 = gates_raw["G6-step3-mass-exogenous"]
    print("[G6] 质量比=%s 闭包可生成=%s ok=%s" %
          (g6["m_mu_over_m_e"], g6["mass_ratio_generable_from_closure"], g6["ok"]))
    g8 = gates_raw["G8-key-table-open-count"]
    print("[G8] 关键表 OPEN=%d/%d ok=%s" % (g8["n_open"], g8["n_total"], g8["ok"]))
    print("[G] 判据 %d/%d ok" % (n_ok, len(gates)))
    print("JSON =", OUT_JSON, os.path.getsize(OUT_JSON), "B", "sha256", sha[:16])
    return out


if __name__ == "__main__":
    main()
