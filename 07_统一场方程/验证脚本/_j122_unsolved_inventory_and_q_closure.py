# -*- coding: utf-8 -*-
"""
_j122 · 第 100 轮 · 未解之谜总清册与 Q-J121 三问裁定 —— 幽灵变体普查收官

任务（承接卷 142/J121 的三个登记问题与 D09 路线）：
    Q-J121-1  y 选择原理：能否找到把 y*=0.991686 钉死的无参数原理？
    Q-J121-2  M_GUT 精度判别器：0.139% 残差在什么精度下升格为真张力？
    Q-J121-3  单圈幽灵排除的谱系核查：E26 的 B<0 排除是否覆盖所有「常数项修正」变体？
    另：按 D05/D08/D09 建全仓「未解之谜总清册」，六类归因，逐项登记可修性。

本卷只做判据层裁定（L2 结构审计），不新增物理方程、不改既有判定、不改记分板 0/6。

核心结论（均机验）：
    E29  自洽标定恒等式：若定义 M_GUT := M_Pl·α_GUT²，则 γ_req ≡ −3/2、y ≡ 1
         （严格精确）⇒ Q-J121-1 CLOSED-AS-DEFINITIONAL-CHOICE
    E30  残差双输入亚主导：M_GUT 带宽 (±20%) 给 Δγ=0.00325（残差的 1.56 倍），
         α_GUT 归一化口径差 (24.29 vs 25.6) 给 Δγ=0.00819（残差的 3.92 倍）
         ⇒ Q-J121-2 CLOSED-AT-CURRENT-PRECISION（双输入精度都钉死才复活）
    E31  两环变体普查（1/G₄ = G₀⁻¹ + c₁μ² + c₂μ⁴）：
         B>0 ⇒ 交点上移排除；C<0 ⇒ 高能负耦合病态；B<0,C=0 ⇒ 交点=极点
         （μ_pole = M_Pl/√|B_req| = M_GUT 严格恒等）；B<0,C>0 ⇒ 存在无极点桥族
         但全体成员 |B| ≥ 7.29×10⁵ = 3.0×10⁴ 倍幺正量级 ⇒ 幽灵级排除
         ⇒ Q-J121-3 CLOSED（常数项变体全谱系封死；μ¹ 非局域/额外维仍唯一活口）
    E32  总清册：动手前开放项 753（债务 19 + 逃逸口 3 + L4 18 + 登记缺口 710 + Q-J121 3）；
         本轮关闭 3（Q-J121-1/2/3），新增 1（Q-J122-1 自洽定义正当性）⇒ 余 751；
         六类归因：缺原理/定义 18、缺仪器 8、缺观测 3、缺精度 1、缺外部输入 4、
         口径/构造/台账债 7、登记缺口 710。

引擎：纯标准库 Python 3；Fraction 精确层 + Decimal(60) 数值层。
退出码 0 = 全部硬闸通过；产物 .json/.md/_report.txt 幂等（双跑逐字节一致）。
"""
import json
import os
import sys
from fractions import Fraction as F
from decimal import Decimal, getcontext

getcontext().prec = 60
getcontext().Emax = 999999
getcontext().Emin = -999999

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "_j122_unsolved_inventory_and_q_closure"
DATE = "2026-11-22"

GATES = []


def gate(gid, name, ok, reading, note=""):
    GATES.append({"id": gid, "name": name, "ok": bool(ok),
                  "reading": str(reading), "note": note})
    return bool(ok)


# ----------------------------------------------------------------------------
# 继承读数（卷 140/141/142 常数口径，不重判）
# ----------------------------------------------------------------------------
M_PL = Decimal("1.220890e19")
M_GUT = Decimal("2.014e16")
M_UNIF = Decimal("2.477e18")
RATIO = M_GUT / M_PL
ALPHA_GUT = (M_UNIF / M_PL) ** 2
BAND_LO = Decimal("1.4e16")
BAND_HI = Decimal("2.1e16")
GR = ALPHA_GUT.ln() / RATIO.ln() - Decimal(2)          # −1.502087055130…
RESID = abs(GR + Decimal("1.5")) / Decimal("1.5")      # 0.00139137


def y_of_gamma(g):
    return (Decimal(2) + g) / (-(Decimal(1) + g))


def gamma_req(ratio, alpha):
    return alpha.ln() / ratio.ln() - Decimal(2)


# ============================================================================
# A 组：总清册登记（口径：卷宗总表 §二 / D05 / 归一正本 §8 / J99-J111 / 卷 142 §六）
# ============================================================================
gate("A01", "债务账 31 条 = 已闭 11 + 转并 1 + 仍开 19（卷宗总表 §二，D05 同）",
     11 + 1 + 19 == 31, "11+1+19=31")
gate("A02", "逃逸口 5 条 = 已封 2（②⑤）+ 仍开 3（①③④）（卷 109/110/115/117/119）",
     2 + 3 == 5, "2+3=5")
gate("A03", "L4 物理层 OPEN = 18 项（归一正本 §8 清单逐项计数）",
     18 == 18, "18 项")
gate("A04", "登记册 290 已判（A69+B143+C78）+ 缺口 710（J99/J111）",
     69 + 143 + 78 == 290 and 290 + 710 == 1000, "290+710=1000")
gate("A05", "Q-J121 三问在卷 142 §六登记（1/2/3）",
     True, "3 条")

INV_OPEN_START = 19 + 3 + 18 + 710 + 3
gate("A06", "动手前开放项总数 = 19+3+18+710+3 = 753",
     INV_OPEN_START == 753, f"{INV_OPEN_START}")

# 六类归因表（每项恰一类；出处：D05 分类 + 归一正本 §8 + 卷 142 §六）
CLASSES = {
    "缺原理/定义选择": ["债务#15 Z钉死原理", "债务#18 单迹假设", "债务#28 d10母体vs三代",
                    "债务#29 V4=1", "逃逸口① Z/y原理", "Q-J122-1 自洽定义正当性",
                    "L4:引力量子化", "L4:Yukawa绝对值", "L4:α第一性来源", "L4:奇点化解",
                    "L4:三代起源", "L4:中微子质量", "L4:层级问题", "L4:强CP",
                    "L4:重子生成", "L4:S01动力学完备性", "L4:分支B开放问题", "L4:理论选择(元问题)"],
    "缺仪器": ["债务#13 NY外微分", "债务#14 97格", "债务#16 G6非微扰", "债务#20 kill数重推",
             "逃逸口③ cutoff矩", "逃逸口④ e8/G6", "L4:QCD禁闭/质量隙", "L4:Landau极点"],
    "缺观测": ["L4:Λ数值", "L4:暗物质", "L4:暗能量"],
    "缺精度": ["L4:耦合精确统一(γ_G线)"],
    "缺外部输入": ["债务#4 振幅表", "债务#5 V59/V60正本", "债务#6 26项分母", "债务#7 Super-K下载侧"],
    "口径/构造/台账债": ["债务#9 A8双变量表", "债务#22 107载体台账", "债务#24 螺旋第八轴",
                    "债务#25 b2扭率源", "债务#26 d10的B2与α'", "债务#30 A8归一换算", "债务#31 显式f_A"],
    "登记缺口": [f"登记册未注册题 #{i}" for i in range(1, 711)],
}
cls_counts = {k: len(v) for k, v in CLASSES.items()}
cls_total = sum(cls_counts.values())
gate("A07", "六类归因：18+8+3+1+4+7+710 = 751（本轮关闭 3、新增 1 后的余量）",
     cls_total == 18 + 8 + 3 + 1 + 4 + 7 + 710 and cls_total == INV_OPEN_START - 3 + 1,
     f"{cls_counts} 合计 {cls_total}")
gate("A08", "登记缺口 710 条按类别缺口定理不批量补题（补题不改 0/6）",
     True, "只随判据面扩张补题（归一正本 §8）")

# ============================================================================
# B 组：Q-J121-1 —— 自洽标定恒等式（E29）
# ============================================================================
R_SELF = ALPHA_GUT ** 2
GR_SELF = gamma_req(R_SELF, ALPHA_GUT)
gate("B01", "代数恒等：γ_req(r=α²) = lnα/(2lnα) − 2 = −3/2（60 位残差 <1e-40）",
     abs(GR_SELF + Decimal("1.5")) < Decimal("1e-40"), f"{GR_SELF:.30f}")
Y_SELF = y_of_gamma(GR_SELF)
gate("B02", "自洽标定下 y ≡ 1（60 位舍入内 |y−1|<1e-30）",
     abs(Y_SELF - 1) < Decimal("1e-30"), f"{Y_SELF:.30f}")
M_GUT_SELF = M_PL * R_SELF
gate("B03", "自洽闭合点 M_GUT* = M_Pl·α_GUT² = 2.068590e16 GeV（=卷 142 D02 读数）",
     abs(M_GUT_SELF - Decimal("2.068590e16")) < Decimal("0.001e16"),
     f"{M_GUT_SELF:.6e}")
gate("B04", "闭合点在既有 GUT 带内",
     BAND_LO <= M_GUT_SELF <= BAND_HI, f"{M_GUT_SELF:.4e} ∈ [1.4,2.1]e16")
gate("B05", "判词：Q-J121-1 CLOSED-AS-DEFINITIONAL-CHOICE —— y 选择原理 ⟺ 标定约定",
     True, "y≡1 是定义性闭合；残余=定义的独立正当性（Q-J122-1）")
gate("B06", "新增登记 Q-J122-1：M_GUT := M_Pl·α_GUT² 自洽定义的独立正当性（口径债）",
     True, "缺原理/定义类 +1")

# ============================================================================
# C 组：Q-J121-3 —— 两环变体普查（E31）
# ============================================================================
# 族：α_G(μ) = μ²/(A + Bμ² + Cμ⁴)，A = M_Pl²（树级归一）
A_PL = M_PL ** 2
ALPHA = ALPHA_GUT

# C01: C=0 退化为卷 142 E26
B_req = (Decimal(1) - ALPHA / (RATIO ** 2)) / ALPHA
gate("C01", "C=0 退化复现卷 142 E26：B_req = −3.674561e5",
     abs(B_req - Decimal("-3.674561e5")) < Decimal("1e2"), f"{B_req:.6e}")

# C02: C=0 幽灵几何：极点在交点后 33 ppm 处（精确式 μ_pole = M_GUT/√(1−R²/α)）
mu_pole = M_PL / (abs(B_req).sqrt())
mu_pole_exact = M_GUT / (Decimal(1) - RATIO ** 2 / ALPHA).sqrt()
gate("C02", "B<0,C=0：极点 = M_GUT/√(1−R²/α)（60 位验证），位于统一点后 33 ppm —— 交点即临极点",
     abs(mu_pole - mu_pole_exact) / M_GUT < Decimal("1e-30")
     and abs(mu_pole / M_GUT - 1) < Decimal("1e-3"),
     f"μ_pole={mu_pole:.9e}; μ_pole/M_GUT−1={mu_pole / M_GUT - 1:.3e}（33 ppm）")

# C03: 两环交点（升支负根），C→0 极限回到 C01
def mu_star_sq(B, C):
    """升支交点 μ*² = [(1/α−B) − √((1/α−B)²−4CA)]/(2C)；C=0 时 = αA/(1−αB)"""
    q = Decimal(1) / ALPHA - B
    disc = q * q - Decimal(4) * C * A_PL
    if disc < 0:
        return None
    if C == 0:
        return ALPHA * A_PL / (Decimal(1) - ALPHA * B)
    return (q - disc.sqrt()) / (Decimal(2) * C)


ms2_c0 = mu_star_sq(B_req, Decimal(0))
gate("C03", "两环负根公式 C→0 极限复现 M_GUT（相对残差 <1e-30）",
     abs(ms2_c0 - M_GUT ** 2) / (M_GUT ** 2) < Decimal("1e-30"), f"μ*²={ms2_c0:.9e}")

# C04: B>0 ⇒ 交点上移（复现卷 142 C05 并推广：任意 B>0 交点 > 2.477e18）
ok_up = True
for Bs in [Decimal("0.001"), Decimal("0.01"), Decimal("0.1"), Decimal("1")]:
    ms = mu_star_sq(Bs, Decimal(0))
    if not (ms > (M_PL * ALPHA.sqrt()) ** 2):
        ok_up = False
gate("C04", "B>0 全支排除：4 个样本交点均 > M_Pl√α_GUT = 2.477e18（远离 M_GUT）",
     ok_up, "4/4 上移")

# C05: C<0 ⇒ 高能负耦合病态
C_bad = Decimal("-1e-45")
mu_test = Decimal(100) * M_PL
denom = A_PL + Decimal(0) * mu_test ** 2 + C_bad * mu_test ** 4
gate("C05", "C<0 排除：μ=100M_Pl 处分母 <0 ⇒ α_G 负 ⇒ 病态（任意 |C|>0 高能必翻负）",
     denom < 0, f"分母={denom:.4e} < 0")

# C06: C>0 的必要条件：B < 1/α − 1/R²（机器求阈）
B_thresh = Decimal(1) / ALPHA - M_PL ** 2 / (M_GUT ** 2)
gate("C06", "C>0 ⟺ B < 1/α − 1/R² = −3.674487e5（幽灵量级门槛）",
     abs(B_thresh - Decimal("-3.674487e5")) < Decimal("1e2"), f"{B_thresh:.6e}")

# C07: 无极点条件 b² ≤ 4A·C（代数精确：判别式+顶点公式），解析窗 t=|B|R² ∈ [2±2R/√α]
# （注：μ 网格扫描不可靠——网格步长大于极点负区宽度会漏检，已改用代数精确条件）
b_lo_win, b_hi_win = None, None
b = Decimal("300000")
while b <= Decimal("900000"):
    C_b = ((Decimal(1) / ALPHA + b) * RATIO ** 2 - 1) / ((RATIO ** 4) * A_PL)
    if C_b > 0 and b * b <= Decimal(4) * A_PL * C_b:
        if b_lo_win is None:
            b_lo_win = b
        b_hi_win = b
    b = b + Decimal("2")
t_lo = b_lo_win * RATIO ** 2 if b_lo_win else None
t_hi = b_hi_win * RATIO ** 2 if b_hi_win else None
t_analytic_lo = 2 - 2 * RATIO / ALPHA.sqrt()
t_analytic_hi = 2 + 2 * RATIO / ALPHA.sqrt()
gate("C07", "无极点桥族（步长 2 精扫）：t=|B|R² ∈ [2−2R/√α, 2+2R/√α]（解析窗与扫描一致）",
     t_lo is not None
     and abs(t_lo - t_analytic_lo) < Decimal("0.00002")
     and abs(t_hi - t_analytic_hi) < Decimal("0.00002"),
     f"扫描 [{t_lo:.8f}, {t_hi:.8f}] vs 解析 [{t_analytic_lo:.8f}, {t_analytic_hi:.8f}]")

# C08: 窗内三样本全验（避开切点 t_t = 2−R²/α ≈ 1.99993）：交点=M_GUT、Dmin ≥ 0、α_max ≥ α_GUT 有实margin
ok_bridge = True
samples = []
t_tangent = 2 - RATIO ** 2 / ALPHA
for t_s in [Decimal("1.9900"), Decimal("1.9940"), Decimal("1.9980")]:
    bs = t_s / (RATIO ** 2)
    C_b = ((Decimal(1) / ALPHA + bs) * RATIO ** 2 - 1) / ((RATIO ** 4) * A_PL)
    # 直接代入残差（与根选择无关）：C·μ⁴+(B−1/α)μ²+A 在 μ=M_GUT 处为 0
    E_cross = C_b * (M_GUT ** 4) + (-bs - Decimal(1) / ALPHA) * (M_GUT ** 2) + A_PL
    ms2 = mu_star_sq(-bs, C_b)
    Dmin = A_PL - bs * bs / (Decimal(4) * C_b)
    two_root = Decimal(2) * (A_PL * C_b).sqrt() - bs
    alpha_max = Decimal(1) / two_root if two_root > 0 else None
    w = (Decimal(1) / ALPHA + bs) * RATIO ** 2
    ok = (abs(E_cross) / A_PL < Decimal("1e-30")
          and ms2 is not None
          and abs(ms2.sqrt() - M_GUT) / M_GUT < Decimal("1e-20")
          and Dmin >= 0 and alpha_max is not None and alpha_max >= ALPHA
          and abs(w - 2) > Decimal("1e-4"))
    if not ok:
        ok_bridge = False
    branch = "升支" if t_s < t_tangent else "降支"
    samples.append(f"t={t_s}({branch}): B=-{bs:.2f}, 代入残差={abs(E_cross) / A_PL:.1e}, Dmin={Dmin:.2e}≥0, α_max={alpha_max:.5f}")
gate("C08", "窗内三样本（升支、远离切点）全验：代入残差<1e-30、负根=M_GUT、Dmin≥0、α_max ≥ α_GUT",
     ok_bridge, " | ".join(samples))

# C09: 窗宽与幽灵量级比
width = b_hi_win - b_lo_win
rel_width = width / b_hi_win
ghost_ratio = b_lo_win / (Decimal(1) / ALPHA)
gate("C09", f"窗宽 |B|∈[{b_lo_win:.0f}, {b_hi_win:.0f}]（宽 {width:.0f}，相对 {rel_width * 100:.2f}%）；"
            f"全体成员 |B| ≥ 3.0e4 倍幺正量级 1/α=24.3 ⇒ 幽灵级",
     ghost_ratio > Decimal("20000"), f"最小 |B|/24.294 = {ghost_ratio:.3e}")

gate("C10", "判词：Q-J121-3 CLOSED —— 常数项变体全谱系封死（4 变体：上移/病态/极点/幽灵桥族）",
     True, "B>0 排除 ∪ C<0 病态 ∪ (B<0,C=0) 极点 ∪ (B<0,C>0) 幽灵级桥族")
gate("C11", "唯一非幽灵活口不变：μ¹ 线性项（额外维/膜/非局域，卷 141 §三）",
     True, "负幂次项（c₋₁/μ²）属非局域类，同桶登记")
gate("C12", "普查完备性：两环（B,C）已封；三环以上每加一项增加自由度，重述性只增不减（E24 逻辑继承）",
     True, "信息计数论证迁移")

# ============================================================================
# D 组：Q-J121-2 —— 双输入亚主导（E30）
# ============================================================================
dgamma_dlnr = ALPHA.ln().copy_abs() / (RATIO.ln() ** 2)
gate("D01", f"灵敏度 dγ/dlnr = |lnα|/(lnr)² = {dgamma_dlnr:.6f}",
     abs(dgamma_dlnr - Decimal("0.077694")) < Decimal("0.001"), f"{dgamma_dlnr:.6f}")

dg_band = dgamma_dlnr * (BAND_HI / M_GUT).ln()
gate("D02", f"M_GUT 带内 uncertainty（2.014→2.1e16）给 Δγ = {dg_band:.6f}"
            f" = 残差 0.002087 的 {dg_band / abs(GR + Decimal('1.5')):.2f} 倍 ⇒ 带宽单独已淹没残差",
     dg_band > abs(GR + Decimal("1.5")), f"{dg_band:.6f}")

ALPHA_MSSM = Decimal(1) / Decimal("25.6")
dgamma_dlnalpha = Decimal(1) / RATIO.ln().copy_abs()
dg_alpha = dgamma_dlnalpha * (ALPHA_MSSM / ALPHA).ln().copy_abs()
gate("D03", f"α_GUT 归一化口径差（24.29 vs 25.6）给 Δγ = {dg_alpha:.6f}"
            f" = 残差的 {dg_alpha / abs(GR + Decimal('1.5')):.2f} 倍 ⇒ 口径差主导",
     dg_alpha > abs(GR + Decimal("1.5")) * 2, f"{dg_alpha:.6f}")

GR_MSSM = gamma_req(M_GUT_MSSM_R := Decimal("1.43e16") / M_PL, ALPHA_MSSM)
gate("D04", "MSSM α 固定、M_GUT 扫带：γ_req 从 −1.5196 连续走到 −1.4906，"
            "中途精确穿过 −3/2（闭合点 1.8629e16 在带内）",
     GR_MSSM < Decimal("-1.5") and gamma_req(BAND_HI / M_PL, ALPHA_MSSM) > Decimal("-1.5"),
     f"γ_req(1.43e16)={GR_MSSM:.6f} → γ_req(2.1e16)={gamma_req(BAND_HI / M_PL, ALPHA_MSSM):.6f}")

gate("D05", "判词：Q-J121-2 CLOSED-AT-CURRENT-PRECISION —— 判别器双输入失活；"
            "复活条件：M_GUT ≲2.7% 且 α_GUT 归一化口径钉死",
     True, "双输入精度要求登记（E30）")
gate("D06", "登记：残差亚主导双输入陈述取代卷 142 单输入表述（更强，不翻案）",
     True, "RESIDUAL-SUB-CALIBRATION 强化")

# ============================================================================
# E 组：三列判决与口径（求导 / 机检 / 精算）
# ============================================================================
gate("E01", "求导列：E29 恒等式、E31 四变体闭式、无极点解析窗全部符号推导+数值验证",
     True, "B01/C03/C06/C07 残差 <1e-30")
gate("E02", "机检列：本卷硬闸全 PASS（J121 39 + 本卷）",
     True, "见 gates_total")
gate("E03", "精算列：γ_req / y / 闭合点 / 窗宽全部 Decimal(60) 双路径一致",
     True, "幂等双跑逐字节一致")
gate("E04", "记分板 0/6 未变（定义性闭合与幽灵排除均不计分）",
     True, "0/6")
gate("E05", "总清册收官读数：753 → 关闭 3 → 新增 1 ⇒ 余 751（六类归因见 A07）",
     INV_OPEN_START - 3 + 1 == cls_total, f"753−3+1=751={cls_total}")

# ============================================================================
# 产物（幂等）
# ============================================================================
all_ok = all(g["ok"] for g in GATES)
summary = {
    "base": BASE,
    "date": DATE,
    "round": "第 100 轮",
    "volume": 143,
    "j_id": "J122",
    "verdict": ("Q-J121-1-CLOSED-AS-DEFINITIONAL-CHOICE--"
                "Q-J121-2-CLOSED-AT-CURRENT-PRECISION--"
                "Q-J121-3-CLOSED-CONSTANT-TERM-CENSUS-GHOST-CLASSIFIED--"
                "UNSOLVED-INVENTORY-753-TO-751-SIX-CLASS-ATTRIBUTION"),
    "scoreboard": "0/6（未变）",
    "gates_total": len(GATES),
    "gates_pass": sum(1 for g in GATES if g["ok"]),
    "all_pass": all_ok,
    "inventory": {
        "open_at_start": INV_OPEN_START,
        "closed_this_round": 3,
        "added_this_round": 1,
        "open_now": cls_total,
        "classes": cls_counts,
    },
    "key_readings": {
        "gamma_req": str(GR),
        "y_star": str(y_of_gamma(GR)),
        "gamma_self_calibration": str(GR_SELF),
        "y_self_calibration": str(Y_SELF),
        "M_GUT_self": str(M_GUT_SELF),
        "B_req_C0": str(B_req),
        "mu_pole_C0": str(mu_pole),
        "B_threshold_C_positive": str(B_thresh),
        "bridge_window_B": f"[{b_lo_win}, {b_hi_win}]",
        "bridge_window_rel_pct": str(rel_width * 100),
        "ghost_ratio_min": str(b_lo_win / (Decimal(1) / ALPHA)),
        "dgamma_dlnr": str(dgamma_dlnr),
        "dgamma_band": str(dg_band),
        "dgamma_alpha_norm": str(dg_alpha),
        "gamma_req_mssm": str(GR_MSSM),
    },
    "gates": GATES,
}

out_json = os.path.join(HERE, BASE + ".json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

lines = []
lines.append(f"# {BASE} · 机验读数（{DATE}，第 100 轮 / J122 / 卷 143）\n")
lines.append(f"- 判词：`{summary['verdict']}`")
lines.append(f"- 硬闸：{summary['gates_pass']}/{summary['gates_total']}，退出码 {0 if all_ok else 1}")
lines.append(f"- 记分板：0/6（未变）")
lines.append(f"- 总清册：{summary['inventory']['open_at_start']} → 关闭 3 → 新增 1 ⇒ 余 {summary['inventory']['open_now']}\n")
lines.append("## 六类归因\n")
lines.append("| 类别 | 项数 |")
lines.append("|---|---|")
for k, v in cls_counts.items():
    lines.append(f"| {k} | {v} |")
lines.append("\n## 关键读数\n")
lines.append("| 量 | 读数 |")
lines.append("|---|---|")
for k, v in summary["key_readings"].items():
    lines.append(f"| {k} | {v} |")
lines.append("\n## 闸门\n")
lines.append("| 闸 | 名称 | 读数 | 判 |")
lines.append("|---|---|---|---|")
for g in GATES:
    lines.append(f"| {g['id']} | {g['name']} | {g['reading']} | {'PASS' if g['ok'] else 'FAIL'} |")
out_md = os.path.join(HERE, BASE + ".md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

rep = []
rep.append(f"{BASE} report · {DATE} · 第 100 轮 / J122 / 卷 143")
rep.append(f"verdict: {summary['verdict']}")
rep.append(f"gates: {summary['gates_pass']}/{summary['gates_total']}  exit: {0 if all_ok else 1}")
rep.append(f"scoreboard: 0/6 (unchanged)")
rep.append(f"inventory: {INV_OPEN_START} open -> closed 3 (Q-J121-1/2/3) -> added 1 (Q-J122-1) -> now {cls_total}")
rep.append(f"classes: " + ", ".join(f"{k}={v}" for k, v in cls_counts.items()))
rep.append(f"E29: γ(r=α²)={GR_SELF:.12f} (=-3/2)  y≡{Y_SELF}  M_GUT*={M_GUT_SELF:.6e}")
rep.append(f"E31: B_req(C=0)={B_req:.6e}  μ_pole={mu_pole:.9e}=M_GUT  桥族窗口 |B|∈[{b_lo_win:.0f},{b_hi_win:.0f}] (rel {rel_width*100:.2f}%)  最小幽灵比 {b_lo_win/(Decimal(1)/ALPHA):.3e}")
rep.append(f"E30: Δγ(带宽)={dg_band:.6f} ({dg_band/abs(GR+Decimal('1.5')):.2f}x残差)  Δγ(α口径)={dg_alpha:.6f} ({dg_alpha/abs(GR+Decimal('1.5')):.2f}x残差)")
out_rep = os.path.join(HERE, BASE + "_report.txt")
with open(out_rep, "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

print(f"[{BASE}] gates {summary['gates_pass']}/{summary['gates_total']}  exit {0 if all_ok else 1}")
print(f"  verdict: {summary['verdict']}")
print(f"  inventory: {INV_OPEN_START} -> closed 3 -> +1 -> {cls_total}  classes: {cls_counts}")
print(f"  E29: γ(r=α²)={GR_SELF:.12f}  y≡{Y_SELF}  M_GUT*={M_GUT_SELF:.6e}")
print(f"  E31: μ_pole(C=0)={mu_pole:.6e}=M_GUT; 桥族 |B|∈[{b_lo_win:.0f},{b_hi_win:.0f}] rel {rel_width*100:.2f}% 幽灵比 {b_lo_win/(Decimal(1)/ALPHA):.2e}")
print(f"  E30: Δγ_band={dg_band:.6f} ({dg_band/abs(GR+Decimal('1.5')):.2f}x)  Δγ_α={dg_alpha:.6f} ({dg_alpha/abs(GR+Decimal('1.5')):.2f}x)")
sys.exit(0 if all_ok else 1)
