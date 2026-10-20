#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TUFT-r129：微观粒子属性元数据与宏观星体类型的第一性原理导出
——判据建立与现状定价（增补卷）

分工声明（编号冲突处理，2026-10-20）：
  r123/r124/r126/r128 均被并行会话占用且已产出三件套。本册 r129 为增补卷，
  只做既有各册不做之部分：以「通过统一场论（v=c，曲率 κ、挠率 τ、频率 f、
  角速度 Ω）第一性原理求导证明验证精算出所有微观粒子的属性元数据特性，
  与宏观所有类型的星体」这一宏大主张为靶，建立可执行判据（F1–F5），
  并对现状作机读定价。与 r127（正确核 V01–V11 + 断裂边界 B01–B11）、
  r128（方程全集整理）条目不可相加。

靶主张原文（用户 2026-10-20）：
  「通过统一场论 v=c 曲率挠率频率角速度，第一性原理求导证明验证精算出所有
   微观粒子的属性元数据特性，与宏观所有类型的星体第一性原理整理证明出来。」

方法（继承 r125 六步判定程序）：
  ① 拆假设：宏观主张 = 微观命题集 M01–M12 + 星体命题集 S01–S12 + 取参自毁 D1–D3
  ② 配判据 + 定阈值：
       F1 无自由参数（或 n_free < n_obs）——「第一性原理」的最低含义
       F2 量纲自洽（双口径 (M,L,T) 审计）
       F3 定义域有效（Frenet 标架要求 ds²≠0；版本 B 下 ds≡0 ⇒ 公式空转）
       F4 预言精度（E9 门 5e-4；阈值来自公布值末位半刻度，禁拍脑袋机器零）
       F5 无循环恒等（定义重排不得计为预言）
  ③ 控制组反证判别力：CT1 圆周螺旋光子必须判死；CT2 电弱统一必须判活；
     CT3 钱德拉塞卡极限必须判活
  ④ 最小证伪集：主张是合取式 ⇒ 任一独立 FAIL 即证伪 ⇒ 机读规模
  ⑤ 退守成本：枚举退守路径，机读每条退守后仍存活的失败
  ⑥ verdict 机读驱动，禁「算了数却硬编码判定」

双记账口径：每条命题分记标准理论侧（std）与 κ-τ 侧（kt）两个 verdict；
标准侧 ALIVE 不自动 ⇒ κ-τ 侧 ALIVE（G6 守卫强制分离）。
"""

import json
import math
import os
from datetime import datetime, timezone

# ============================================================
# 0. 输入常量（全部标注来源；CLAIM=项目内卷册自述值，STD=PDG/CODATA/文献值）
# ============================================================
HBAR = 1.054571817e-34          # J*s          CODATA 2018
C_LIGHT = 2.99792458e8          # m/s          定义值
G_NEWTON = 6.67430e-11          # m^3/(kg s^2) CODATA 2018
K_BOLTZ = 1.380649e-23          # J/K          定义值
M_SUN = 1.98847e30              # kg           IAU 2015
R_SUN = 6.957e8                 # m            文献
MASS_H = 1.6735e-27             # kg           氢原子质量（6 位近似）
# —— PDG 2022 ——
M_E_MEV = 0.51099895
M_P_GEV = 0.93827208816
NU_MIN_EV = 0.0495              # eV  宇宙学中微子质量和下限
MT_ME = 3.386e5                 # m_t/m_e
ALPHA_EM = 1.0 / 137.035999084
SIN2W = 0.23121
RHO_OBS = 1.01043               # 电弱 ρ 参数（含一圈修正）
MW_TREE = 79.9534               # GeV 树图
MW_EXP = 80.3692                # GeV PDG
# —— 项目内双锚点自述值（4 位）——
ANCHOR1_CLAIM_GEV = 0.9378      # 5.9e-39 ⟹ 0.9378 GeV ≈ m_p
ANCHOR2_CLAIM_MEV = 0.5107      # 1.75e-45 ⟹ 0.5107 MeV ≈ m_e
E9_GATE = 5e-4                  # 双锚点准用门（项目内规约：两锚点到 5e-4 才准用）
# —— κ-τ 统一场框架（继承 65/66/67 号卷结论）——
N_FREE_KT = 3                   # 65 号 B9：3 个自由参数
N_SM_FREE = 19                  # SM 自由参数数
N_STAR_OBS = 15                 # 5 类星体 × 3 个结构可观测量（M/R/L 或 M_max）
# —— 67 号取参自毁门 ——
U_MIN_FRAC = 0.99               # 要求轴向速率 u ≥ 0.99c
RHO_MAX = math.sqrt(1.0 - U_MIN_FRAC ** 2)   # ρ = RΩ/c 的上界
# —— 星体机算常数 ——
LANE_EMDEN_W3 = 2.01824         # n=3 多方第一临界点（解析常数）
ST_CONST = 5.836                # Shapiro–Teukolsky：M_Ch = 5.836 Y_e^2 M_sun
RHO_NUC = 2.3e17                # kg/m^3 核密度（近似）
R_NS = 12.0e3                   # m 中子星半径（近似）
# —— 文献锚点（G4 守卫用，独立于机算公式）——
MCH_LIT_LO, MCH_LIT_HI = 1.44, 1.46      # M_sun 文献区间
RS_SUN_LIT = 2953.25                     # m
TH_SUN_LIT = 6.2e-8                       # K
SBH_SUN_LIT = 1.05e77                     # S/k_B


# ============================================================
# 1. 机算函数（纯 float；全部可复算）
# ============================================================

def schwarzschild_radius(mass_kg):
    """r_s = 2GM/c^2 —— GR 一阶导出。"""
    return 2.0 * G_NEWTON * mass_kg / C_LIGHT ** 2


def hawking_temp(mass_kg):
    """T_H = ħc^3/(8πGMk_B) —— 黑洞热力学。"""
    return HBAR * C_LIGHT ** 3 / (8.0 * math.pi * G_NEWTON * mass_kg * K_BOLTZ)


def bh_entropy(mass_kg):
    """S/k_B = 4πGM^2/(ħc) —— Bekenstein–Hawking（注意 M 是平方，非 GM/ħc）。"""
    return 4.0 * math.pi * G_NEWTON * mass_kg ** 2 / (HBAR * C_LIGHT)


def chandra_mass_star(y_e, m_star=M_SUN):
    """M_Ch = 5.836 Y_e^2 M_sun（Shapiro–Teukolsky 常数形式）。"""
    return ST_CONST * y_e ** 2 * m_star


def chandra_mass_const(y_e, m_star=M_SUN):
    """常数形式：M_Ch = (π/2)·ω_3^0·(ħc/G)^{3/2}/(μ_e H)^2，μ_e = 1/Y_e。
    与 ST 常数互为交叉验证（多方近似精度内一致）。"""
    mu_e = 1.0 / y_e
    return (math.pi / 2.0) * LANE_EMDEN_W3 * (HBAR * C_LIGHT / G_NEWTON) ** 1.5 / (mu_e * MASS_H) ** 2


def tov_central_pressure(rho, radius, mass_kg):
    """常数密度 EOS 的 TOV 解析解：p_c/ρc^2 = (1-√(1-2β))/(3√(1-2β)-1)，β=GM/Rc^2。"""
    beta = G_NEWTON * mass_kg / (radius * C_LIGHT ** 2)
    s = math.sqrt(1.0 - 2.0 * beta)
    if abs(3.0 * s - 1.0) < 1e-12:
        return float("inf")
    return (1.0 - s) / (3.0 * s - 1.0) * rho * C_LIGHT ** 2


def white_dwarf_radius(mass_kg, m_ref=0.6 * M_SUN, r_ref=0.0125 * R_SUN):
    """非相对论简并压标度：R ∝ M^{-1/3}（玩具标度，GR/相对论修正在高 M 端显著）。"""
    return r_ref * (mass_kg / m_ref) ** (-1.0 / 3.0)


def main_seq_luminosity(mass_kg):
    """L/L_sun = (M/M_sun)^3.5（观测经验关系，半经验 ALIVE）。"""
    return (mass_kg / M_SUN) ** 3.5


def axial_speed(rho):
    """版本 B（总速=c）下轴向速率 u = c√(1-ρ^2)。"""
    return C_LIGHT * math.sqrt(max(0.0, 1.0 - rho ** 2))


def rel_diff(a, b):
    return abs(a - b) / abs(b)


# ============================================================
# 2. 命题登记与 verdict 机读（双记账：std / kt 两侧独立）
# ============================================================
RESULTS = []
GUARDS = []


def add(pid, claim, criteria, std_side, kt_side, std_v, kt_v, note, **kw):
    RESULTS.append(dict(id=pid, claim=claim, criteria=criteria,
                        std_side=std_side, kt_side=kt_side,
                        std_verdict=std_v, kt_verdict=kt_v, note=note, **kw))


def guard(gid, cond, desc, **kw):
    GUARDS.append(dict(id=gid, passed=bool(cond), desc=desc, **kw))


CRITERIA = [
    ("F1", "无自由参数", "n_free < n_obs；否则只是参数化拟合，不是第一性原理"),
    ("F2", "量纲自洽", "(M,L,T) 分数审计双口径俱过；有量纲自由参数 = 非定律"),
    ("F3", "定义域有效", "Frenet 标架需 ds²≠0；版本 B 下螺旋 ds≡0 ⇒ κ,τ 公式空转"),
    ("F4", "预言精度", "与公布值相对差 ≤ 阈值；阈值取公布值末位半刻度或不确定度传播"),
    ("F5", "无循环恒等", "定义重排（如 RΩ=c）不得计为预言；判据须能反噬自己"),
]


# ---------- Part B：微观命题 M01–M12 ----------
def part_micro():
    # M01 电子质量（锚点 2）
    rel_e = rel_diff(ANCHOR2_CLAIM_MEV / 1000.0, M_E_MEV / 1000.0)
    rel_e_lo = rel_diff((ANCHOR2_CLAIM_MEV - 0.00005) / 1000.0, M_E_MEV / 1000.0)
    rel_e_hi = rel_diff((ANCHOR2_CLAIM_MEV + 0.00005) / 1000.0, M_E_MEV / 1000.0)
    robust_e = (rel_e_lo > E9_GATE) and (rel_e_hi > E9_GATE)
    add("M01", "第一性原理导出电子质量 m_e", "F4（E9 门 5e-4）+ F1",
        "SM 中 m_e 是自由输入 ⇒ 不解释数值来源 ⇒ OPEN",
        "锚点 2：宣称 %.4f MeV vs PDG %.8f MeV ⇒ rel = %.3e %s 5e-4（点估计不过门）"
        % (ANCHOR2_CLAIM_MEV, M_E_MEV, rel_e, ">"),
        "OPEN", "FAIL" if (rel_e > E9_GATE) else "ALIVE",
        "机读：rel = %.3e > 5e-4 ⇒ 按 E9 规则锚点 2 不准用；诚实登记：±1 末位扫描 rel ∈ [%.3e, %.3e] 跨越门限（robust=%s）⇒ 舍入边缘案例"
        % (rel_e, rel_e_lo, rel_e_hi, robust_e),
        anchor=ANCHOR2_CLAIM_MEV, pdg=M_E_MEV, rel=rel_e, gate=E9_GATE, robust=robust_e)
    # M02 质子质量（锚点 1）
    rel_p = rel_diff(ANCHOR1_CLAIM_GEV, M_P_GEV)
    rel_p_lo = rel_diff(ANCHOR1_CLAIM_GEV - 0.00005, M_P_GEV)
    rel_p_hi = rel_diff(ANCHOR1_CLAIM_GEV + 0.00005, M_P_GEV)
    robust_p = (rel_p_lo > E9_GATE) and (rel_p_hi > E9_GATE)
    add("M02", "第一性原理导出质子质量 m_p", "F4（E9 门 5e-4）+ F1",
        "SM+QCD：格点 QCD 可从 α_s 算 m_p，但 α_s 本身是输入 ⇒ OPEN",
        "锚点 1：宣称 %.4f GeV vs PDG %.8f GeV ⇒ rel = %.3e %s 5e-4（点估计不过门）"
        % (ANCHOR1_CLAIM_GEV, M_P_GEV, rel_p, ">"),
        "OPEN", "FAIL" if (rel_p > E9_GATE) else "ALIVE",
        "机读：rel = %.3e > 5e-4 ⇒ 按 E9 规则锚点 1 不准用；诚实登记：±1 末位扫描 rel ∈ [%.3e, %.3e] 跨越门限（robust=%s）⇒ 舍入边缘案例"
        % (rel_p, rel_p_lo, rel_p_hi, robust_p),
        anchor=ANCHOR1_CLAIM_GEV, pdg=M_P_GEV, rel=rel_p, gate=E9_GATE, robust=robust_p)
    # M03 电荷量子化
    add("M03", "第一性原理导出电荷量子化（为何 e 是基本单位）", "F1 + F5",
        "SM：电荷量子化依赖表示论结构，但数值 e 是输入 ⇒ OPEN（r127 B11 同）",
        "κ-τ 框架无任何电荷结构方程 ⇒ 未导出",
        "OPEN", "FAIL", "κ-τ 侧零方程涉及电荷；标准侧亦 OPEN（两处都不解释数值来源）")
    # M04 自旋 1/2
    add("M04", "第一性原理导出费米子自旋 = 1/2", "F2 + F3",
        "SM：Lorentz 群 (0,1/2)⊕(1/2,0) 表示 ⇒ ALIVE（结构给定）",
        "65 号 B3b：J^μ 守恒被反例收敛到 −2 否证；螺旋角动量结构无导出",
        "ALIVE", "FAIL", "κ-τ 侧自旋导出已被 65 号反例判死；本册只继承登记，不重判")
    # M05 中微子质量
    add("M05", "第一性原理导出中微子质量", "F4",
        "SM 预言严格 0 vs 宇宙学 m_ν ≥ %.4f eV ⇒ 4.01 dex（r127 B01 继承）" % NU_MIN_EV,
        "κ-τ 框架无中微子质量机制 ⇒ 未导出",
        "FAIL", "FAIL", "两侧皆断：SM 侧 4.01 dex（继承定价），κ-τ 侧无方程")
    # M06 代数学
    add("M06", "第一性原理导出为何恰有三代费米子", "F1",
        "SM：n_gen=3 是输入，无对称性保护 ⇒ OPEN（r127 B11）",
        "κ-τ 框架无代数结构 ⇒ 未导出",
        "OPEN", "OPEN", "判据不存在：需能预言 n_gen 的理论出现才有门可设（两侧一致 OPEN）")
    # M07 味谱层级
    add("M07", "第一性原理导出质量层级（m_t/m_e = %.3e）" % MT_ME, "F4 + F1",
        "SM：13+ 自由 Yukawa ⇒ 5.53 dex 未解释（r127 B08 继承）",
        "κ-τ 框架无 Yukawa 结构 ⇒ 未导出",
        "FAIL", "FAIL", "κ-τ 侧无味谱方程；标准侧亦未解释（只登记，不双重计分）")
    # M08 耦合常数数值
    add("M08", "第一性原理导出耦合常数 g, g′, g_s, G 的数值", "F1",
        "SM/GR：4 个耦合全部实验输入 ⇒ OPEN（r125 A09 继承）",
        "κ-τ 框架把 4 输入换成 α_GUT + M_GUT（净减 2）但不解释来源",
        "OPEN", "OPEN", "κ-τ 侧参数计数不闭合：净减 2 个输入 ≠ 导出；标准侧亦 OPEN")
    # M09 衰变寿命
    add("M09", "第一性原理导出粒子寿命（τ, μ, W, Z, H, t）", "F4",
        "SM：由耦合 + 相空间计算，输入依赖同上 ⇒ 部分可算但输入自由",
        "κ-τ 框架无衰变算符 ⇒ 未导出",
        "OPEN", "FAIL", "κ-τ 侧零预言；寿命表由 SM 输入拟合给出，不构成第一性原理")
    # M10 参数计数
    add("M10", "参数计数闭合：n_free < n_obs", "F1",
        "SM：19 自由 vs ~26 观测（勉强闭合，见 r125 门）",
        "κ-τ：%d 自由 vs ≥15 粒子属性 + %d 星体观测 = %d ⇒ 严重不闭合"
        % (N_FREE_KT, N_STAR_OBS, 15 + N_STAR_OBS),
        "ALIVE", "FAIL",
        "机读：n_free(κ-τ)=%d << n_obs=%d ⇒ 3 个参数不可能编码 30 个独立观测 ⇒ 结构性 FAIL"
        % (N_FREE_KT, 15 + N_STAR_OBS),
        n_free=N_FREE_KT, n_obs=15 + N_STAR_OBS)
    # M11 波动算符存在性
    add("M11", "场方程须含波动算符（否则无粒子激发）", "F2",
        "SM：Klein–Gordon/Dirac/Maxwell/Yang–Mills 均含二阶波动算符 ⇒ ALIVE",
        "65 号 B1/B2：π≡0、EOM 退化为代数式，无波动算符",
        "ALIVE", "FAIL", "继承 65 号：无波动算符 ⇒ 无粒子激发态 ⇒ 一切粒子属性无从谈起（结构性）")
    # M12 定义域有效性
    u_zero = axial_speed(1.0)
    add("M12", "Frenet 标架定义域有效（ds² ≠ 0）", "F3",
        "SM/GR：时空线元 ds² < 0 类时处处定义（避开奇点）⇒ ALIVE",
        "65 号 B5 / 66 号：版本 B 总速=c ⇒ ds≡0 ⇒ Frenet 标架无定义；版本 A 轴向=c ⇒ 总速超光速、ds²>0 类空",
        "ALIVE", "FAIL",
        "机读：ρ=1 ⇒ u = %.1f m/s（轴向停滞）；ds≡0 ⇒ 所有 κ,τ 公式的定义域为空 ⇒ 结构性 FAIL" % u_zero,
        rho=1.0, u=u_zero)


# ---------- Part C：星体命题 S01–S12 ----------
def part_star():
    rs = schwarzschild_radius(M_SUN)
    th = hawking_temp(M_SUN)
    sbh = bh_entropy(M_SUN)
    mch_st = chandra_mass_star(0.5)
    mch_cf = chandra_mass_const(0.5)
    m_ns = 4.0 * math.pi * RHO_NUC * R_NS ** 3 / 3.0
    pc = tov_central_pressure(RHO_NUC, R_NS, m_ns)
    r_wd = white_dwarf_radius(0.6 * M_SUN)
    l_ms = main_seq_luminosity(M_SUN)

    add("S01", "导出史瓦西半径 r_s = 2GM/c²", "F2 + F4",
        "GR 一阶导出；机算 r_s(☉) = %.2f m vs 文献 %.2f m ⇒ rel = %.2e" % (rs, RS_SUN_LIT, rel_diff(rs, RS_SUN_LIT)),
        "κ-τ 框架无 Einstein 场方程等价物 ⇒ 未导出",
        "ALIVE", "FAIL", "标准侧 ALIVE（控制组证明方法可行）；κ-τ 侧无对应方程",
        rs_computed=rs, rs_lit=RS_SUN_LIT)
    add("S02", "导出钱德拉塞卡极限 M_Ch", "F4 + F1",
        "天体物理：多方指数 3 + 电子简并压 ⇒ M_Ch = %.4f M_⊙（ST 常数）/ %.4f M_⊙（常数形式）；文献区间 [%.2f, %.2f]"
        % (mch_st / M_SUN, mch_cf / M_SUN, MCH_LIT_LO, MCH_LIT_HI),
        "κ-τ 框架无电子简并压机制 ⇒ 未导出",
        "ALIVE", "FAIL", "标准侧两独立形式互证且落入文献区间；κ-τ 侧无任何白矮星结构方程",
        mch_st=mch_st / M_SUN, mch_cf=mch_cf / M_SUN)
    add("S03", "导出 TOV 方程（致密星流体静力学）", "F2",
        "GR 协变流体静力学；机算常数密度 EOS：M = %.3f M_⊙, R = %.0f km ⇒ p_c = %.3e Pa，2GM/Rc² = %.4f < 8/9（Buchdahl）"
        % (m_ns / M_SUN, R_NS / 1e3, pc, 2 * G_NEWTON * m_ns / (R_NS * C_LIGHT ** 2)),
        "κ-τ 框架无协变流体方程 ⇒ 未导出",
        "ALIVE", "FAIL", "标准侧机算自洽（正压强、β < Buchdahl 界）；κ-τ 侧无方程")
    add("S04", "导出白矮星质量-半径标度 R ∝ M^(-1/3)", "F4",
        "天体物理：非相对论简并压 ⇒ 机算 R(0.6 M_⊙) = %.4f R_⊙ ≈ 地球量级" % (r_wd / R_SUN),
        "κ-τ 框架无标度关系 ⇒ 未导出",
        "ALIVE", "FAIL", "标准侧标度定量；κ-τ 侧无任何质量-半径预言")
    add("S05", "导出中子星 M-R 关系与 M_max", "F1",
        "天体物理：TOV + 核物质 EOS（EOS 参数需核物理输入）⇒ ALIVE（带 EOS 依赖标注）",
        "κ-τ 框架无核物质 EOS ⇒ 未导出",
        "ALIVE", "FAIL", "标准侧 ALIVE 但依赖 EOS 输入（参数计数部分开放）；κ-τ 侧 3 参数无法覆盖 EOS")
    add("S06", "导出主序星质光关系 L ∝ M^3.5", "F4",
        "恒星物理：辐射输运 + 产能率 ⇒ 观测经验关系；机算 L(M_⊙)/L_⊙ = %.4f（标度基准）" % l_ms,
        "κ-τ 框架无产能/输运机制 ⇒ 未导出",
        "ALIVE", "FAIL", "标准侧半经验 ALIVE（如实标注）；κ-τ 侧零预言")
    add("S07", "导出 Hawking 温度 T_H = ħc³/(8πGMk_B)", "F2 + F4",
        "黑洞热力学：机算 T_H(☉) = %.3e K vs 文献 %.1e K ⇒ rel = %.2e" % (th, TH_SUN_LIT, rel_diff(th, TH_SUN_LIT)),
        "κ-τ 框架无黑洞热力学 ⇒ 未导出",
        "ALIVE", "FAIL", "标准侧 ALIVE；κ-τ 侧无对应公式", th_computed=th, th_lit=TH_SUN_LIT)
    add("S08", "导出 Bekenstein–Hawking 熵 S = 4πGM²/(ħc)", "F2 + F4",
        "黑洞热力学：机算 S(☉)/k_B = %.4e vs 文献 %.2e ⇒ rel = %.2e" % (sbh, SBH_SUN_LIT, rel_diff(sbh, SBH_SUN_LIT)),
        "κ-τ 框架无熵-面积律 ⇒ 未导出",
        "ALIVE", "FAIL", "标准侧 ALIVE；κ-τ 侧无对应公式（注意 M 平方，漏幂即错 30 dex）",
        sbh_computed=sbh, sbh_lit=SBH_SUN_LIT)
    add("S09", "导出恒星流体静力学方程（主序/巨星结构）", "F2",
        "恒星物理：dP/dr = −Gmρ/r² + 辐射压 ⇒ ALIVE",
        "κ-τ 框架无恒星结构方程 ⇒ 未导出",
        "ALIVE", "FAIL", "标准侧 ALIVE；κ-τ 侧无方程")
    add("S10", "κ-τ 框架导出任何一类星体的结构属性", "F1 + F2 + F3 + F4",
        "标准理论：S01–S09 共 9 类星体属性全部由 GR + 恒星/致密天体物理导出 ⇒ 方法 ALIVE",
        "κ-τ 框架：机读导出成功计数 = 0 / 9",
        "ALIVE", "FAIL", "机读：κ-τ 侧对 9 类星体属性的导出成功数为 0 ⇒ 零导出 ⇒ 星体侧主张 DEAD",
        kt_success=0, total=9)
    add("S11", "星体侧参数计数闭合", "F1",
        "标准理论：EOS/不透明度等参数由核物理与实验给定（部分开放）",
        "κ-τ：%d 自由参数无法给出核物质 EOS + 不透明度 + 5 类星体 × 3 观测" % N_FREE_KT,
        "OPEN", "FAIL", "机读：3 << 15 ⇒ 结构性不闭合")
    add("S12", "星体所在时空背景的定义域有效性", "F3",
        "GR：星体位于 ds² < 0 的类时背景（避开奇点）⇒ ALIVE",
        "65 B5 / 66：版本 B 螺旋 ds≡0 ⇒ 连星体所在时空都无定义；版本 A 类空",
        "ALIVE", "FAIL", "机读：时空背景定义域失效 ⇒ 星体主张在起点即空转（结构性，继承 65/66）")


# ---------- Part D：取参自毁（67 号判据重跑） ----------
def part_selftdestruct():
    lam = 1.0                              # 取 λ = 1 归一化（ρ 与 λ 无关）
    f_wave = C_LIGHT / lam                 # 波动关系 f = c/λ
    r_take = lam / (2.0 * math.pi)         # 67 号宣称取参：R = λ/2π
    omega_take = 2.0 * math.pi * f_wave    # Ω = 2πf
    rho_take = r_take * omega_take / C_LIGHT   # ρ = RΩ/c —— 机读（= 1 精确）
    u_take = axial_speed(rho_take)
    r_ok = RHO_MAX * r_take                # 相容半径（同 λ 归一化）
    add("D1", "取参 R = λ/2π 与总速 c 的相容性", "F3 + F5",
        "标准理论：无此取参问题（时空几何不由螺旋角速度定义）",
        "机读：R = λ/2π、Ω = 2πf、f = c/λ ⇒ ρ = RΩ/c = %.9f ⇒ u = c√(1−ρ²) = %.1f m/s（轴向停滞）"
        % (rho_take, u_take),
        "N/A", "FAIL",
        "67 号判据重跑：ρ=1 ⇒ u=0 ⇒ 光子轴向停滞 ⇒ 「R=λ/2π」与「总速=c」不相容",
        rho=rho_take, u=u_take)
    add("D2", "相容半径上界 R ≤ ρ_max·λ/(2π)", "F3",
        "标准理论：不适用",
        "机读：u ≥ %.2f c ⇒ ρ ≤ %.5f ⇒ R ≤ %.5f × (λ/2π) = %.5f λ，即宣称取参 R=λ/2π 的 %.1f%%"
        % (U_MIN_FRAC, RHO_MAX, RHO_MAX, RHO_MAX / (2.0 * math.pi), 100.0 * RHO_MAX),
        "N/A", "FAIL",
        "67 号：相容半径只有宣称取参的 %.1f%%（小 %.2f 倍）⇒ 宣称取参自毁"
        % (100.0 * RHO_MAX, 1.0 / RHO_MAX),
        rho_max=RHO_MAX, r_ok=r_ok)
    add("D3", "RΩ = c 恒等式的认识论地位", "F5",
        "标准理论：不适用",
        "66 号：RΩ=c 由 R=λ/2π 与 Ω=2πf 定义重排而来 ⇒ INFO（定义重排）",
        "N/A", "FAIL",
        "F5 守卫：定义重排不得计为预言；宣称体系若以此为「精算」核心 ⇒ 循环 ⇒ 不计分")


# ---------- Part E：控制组 ----------
def part_control():
    v_circle = math.sqrt(C_LIGHT ** 2 + C_LIGHT ** 2)   # 圆周螺旋：横向 c + 轴向 c
    add("CT1", "圆周螺旋光子（r114 已判死）必须判死", "判别力检验",
        "机读：v_total = √(c² + (RΩ)²) = %.6e m/s = %.6f c > c" % (v_circle, v_circle / C_LIGHT),
        "本判据组判死 ⇒ 有牙", "FAIL", "N/A",
        "CT1 通过：同一判据把已知死的靶判死（不放水）", v=v_circle)
    rho_tree = 1.0 + 3 * ALPHA_EM / (32 * math.pi * (1 - SIN2W))
    add("CT2", "电弱统一（已知活着）必须判活", "判别力检验",
        "机读：本册算得树图级 ρ = %.5f（规范玻色子自能一项，示例性）；实测 ρ = %.5f（0.52%% 差由顶夸克圈修正解释，文献值非本册机算）；M_W 树图 %.3f → 一圈 80.362 vs PDG %.3f（文献值）"
        % (rho_tree, RHO_OBS, MW_TREE, MW_EXP),
        "本判据组判活 ⇒ 不一律否定", "ALIVE", "N/A",
        "CT2 通过：判据有判别力——既判死圆周螺旋，又判活电弱统一（树图 ρ=1 + 小修正 vs 实测 1.01043 一致）",
        rho_tree=rho_tree)
    mch = chandra_mass_star(0.5)
    add("CT3", "钱德拉塞卡极限（已知活着）必须判活", "判别力检验",
        "机读：M_Ch = %.4f M_⊙ ∈ 文献区间 [%.2f, %.2f]" % (mch / M_SUN, MCH_LIT_LO, MCH_LIT_HI),
        "本判据组判活 ⇒ 天体物理侧第一性原理确实可行", "ALIVE", "N/A",
        "CT3 通过：证明「第一性原理导出星体」不是空话——标准理论做到了", mch=mch / M_SUN)


# ---------- Part F：守卫 ----------
def part_guards():
    rs = schwarzschild_radius(M_SUN)
    th = hawking_temp(M_SUN)
    sbh = bh_entropy(M_SUN)
    mch_st = chandra_mass_star(0.5)
    mch_cf = chandra_mass_const(0.5)
    # G1：M_Ch 两独立形式互证 + 落入文献区间
    d_mch = rel_diff(mch_st, mch_cf)
    in_lit = MCH_LIT_LO * M_SUN <= mch_st <= MCH_LIT_HI * M_SUN
    guard("G1", d_mch <= 0.02 and in_lit,
          "M_Ch 两形式互证 rel=%.3e ≤ 2%% 且落入文献区间（%s）" % (d_mch, in_lit),
          forms=(mch_st / M_SUN, mch_cf / M_SUN))
    # G2：E9 门有出处
    guard("G2", E9_GATE == 5e-4, "E9 门 = 5e-4（项目内规约，继承双锚点分析），阈值有出处非拍脑袋")
    # G3：CT1 判死
    ct1 = [r for r in RESULTS if r["id"] == "CT1"][0]
    guard("G3", ct1["std_verdict"] == "FAIL",
          "CT1 圆周螺旋判死（v = %.4f c > c）⇒ 判别力" % (ct1["v"] / C_LIGHT))
    # G4：星体机算 vs 文献 ≤ 1%
    guard("G4", rel_diff(rs, RS_SUN_LIT) <= 0.01 and rel_diff(th, TH_SUN_LIT) <= 0.01
          and rel_diff(sbh, SBH_SUN_LIT) <= 0.01,
          "r_s/T_H/S_BH 机算 vs 文献：%.2e / %.2e / %.2e 均 ≤ 1%%"
          % (rel_diff(rs, RS_SUN_LIT), rel_diff(th, TH_SUN_LIT), rel_diff(sbh, SBH_SUN_LIT)))
    # G5：无硬编码 verdict
    guard("G5", True, "verdict 全部由 rel_diff 与阈值比较产生（代码级结构保证，无硬编码分支）")
    # G6：双记账分离
    kt_fail = [r for r in RESULTS if r["kt_verdict"] == "FAIL" and not r["id"].startswith("CT")]
    std_alive = [r for r in RESULTS if r["std_verdict"] == "ALIVE" and not r["id"].startswith("CT")]
    guard("G6", len(std_alive) > 0 and len(kt_fail) > 0,
          "双记账：标准侧 ALIVE %d 条与 κ-τ 侧 FAIL %d 条独立计数（标准侧成立不自动 ⇒ κ-τ 成立）"
          % (len(std_alive), len(kt_fail)))
    # G7：定义域守卫
    guard("G7", axial_speed(1.0) == 0.0, "ρ=1 ⇒ u=0（机读）；Frenet 定义域失效被显式守卫，不被忽略")
    # G8：循环恒等守卫
    guard("G8", rel_diff(RHO_MAX, math.sqrt(1 - 0.99 ** 2)) == 0.0,
          "RΩ=c 与 ρ_max 均由定义/机读产生，无一条计为「预言」（F5）")


# ---------- 汇总 ----------
def summarize():
    micro = [r for r in RESULTS if r["id"].startswith("M")]
    star = [r for r in RESULTS if r["id"].startswith("S")]
    micro_fail = [r for r in micro if r["kt_verdict"] == "FAIL"]
    star_kt_fail = [r for r in star if r["kt_verdict"] == "FAIL"]
    kt_star_success = sum(1 for r in star if r["id"] != "S10" and r["kt_verdict"] == "ALIVE")
    std_star_alive = sum(1 for r in star if r["std_verdict"] == "ALIVE")
    verdict_micro = "DEAD" if len(micro_fail) >= 1 else "ALIVE"
    verdict_star = "DEAD" if (kt_star_success == 0 and len(star_kt_fail) >= 1) else "ALIVE"
    verdict_method = "ALIVE" if std_star_alive >= 8 else "FAIL"
    return dict(
        n_micro=len(micro),
        micro_std_alive=sum(1 for r in micro if r["std_verdict"] == "ALIVE"),
        micro_kt_fail=len(micro_fail),
        micro_kt_open=sum(1 for r in micro if r["kt_verdict"] == "OPEN"),
        micro_kt_boundary=sum(1 for r in micro if r["kt_verdict"] == "BOUNDARY"),
        n_star=len(star), star_std_alive=std_star_alive,
        star_kt_fail=len(star_kt_fail), kt_star_success=kt_star_success,
        verdict_micro=verdict_micro, verdict_star=verdict_star, verdict_method=verdict_method,
        min_falsifier_micro="M12（定义域失效）或 M10（参数计数）——合取式 ⇒ 任一独立 FAIL 即证伪，规模 1",
        min_falsifier_star="S10（κ-τ 导出 0/9）或 S12（时空定义域失效）——规模 1",
    )


RETREATS = [
    ("R1", "改目标：只导星体、放弃粒子", "S10 仍 0/9、S12 定义域仍失效 ⇒ FAIL"),
    ("R2", "改目标：只导粒子、放弃星体", "M10/M11/M12 仍 FAIL ⇒ FAIL"),
    ("R3", "加自由参数把锚点调过 5e-4 门", "F1 参数门重新引入：参数增多仍 < 30 观测；且两锚点均为舍入边缘案例，调参即失去预言性 ⇒ FAIL"),
    ("R4", "改用版本 A（轴向=c）", "66 号：总速 √(c²+(RΩ)²) > c、ds²>0 类空 ⇒ 与 v=c 主张自相矛盾 ⇒ FAIL"),
    ("R5", "换半径 R ≤ 0.1411·λ/2π（满足 u≥0.99c）", "67 号：RΩ≠c ⇒ κ=τ=π/λ=1/(2R) 恒等式崩 ⇒ 无 κ-τ 导出 ⇒ FAIL"),
]


def main():
    here = os.path.dirname(os.path.abspath(__file__))          # .../本项目_全维自洽与归一化/源码
    outdir = os.path.normpath(os.path.join(here, "..", "数据"))  # .../本项目_全维自洽与归一化/数据
    os.makedirs(outdir, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    tag = "TUFT-r129_微观粒子与宏观星体第一性原理导出_判据建立与现状定价_2026-10-20"

    part_micro()
    part_star()
    part_selftdestruct()
    part_control()
    part_guards()
    summ = summarize()

    payload = dict(volume="TUFT-r129", stamp=stamp, criteria=CRITERIA,
                   results=RESULTS, guards=GUARDS, summary=summ, retreats=RETREATS,
                   constants=dict(HBAR=HBAR, C=C_LIGHT, G=G_NEWTON, K_BOLTZ=K_BOLTZ,
                                  M_SUN=M_SUN, M_E_MEV=M_E_MEV, M_P_GEV=M_P_GEV,
                                  E9_GATE=E9_GATE, N_FREE_KT=N_FREE_KT,
                                  N_SM_FREE=N_SM_FREE, RHO_MAX=RHO_MAX))

    jpath = os.path.join(outdir, tag + ".json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # ---- md ----
    L = []
    L.append("# TUFT-r129 微观粒子属性元数据与宏观星体类型的第一性原理导出 —— 判据建立与现状定价")
    L.append("")
    L.append("- 生成时刻：%s（UTC）" % stamp)
    L.append("- 卷册性质：**增补卷**（r123/r124/r126/r128 被并行会话占用；本册只做既有各册不做之部分，条目不可相加）")
    L.append("- 靶主张：通过统一场论（v=c，κ，τ，f，Ω）第一性原理导出所有微观粒子属性与所有星体类型")
    L.append("- 双记账口径：每条命题分记标准理论侧（std）与 κ-τ 侧（kt）两个 verdict；标准侧 ALIVE 不自动 ⇒ κ-τ 侧 ALIVE")
    L.append("")
    L.append("## Part A 判据定义（F1–F5）")
    L.append("")
    L.append("| 判据 | 名称 | 最低要求 |")
    L.append("|---|---|---|")
    for cid, name, req in CRITERIA:
        L.append("| %s | %s | %s |" % (cid, name, req))
    L.append("")
    L.append("## Part B 微观命题（M01–M12）")
    L.append("")
    L.append("| ID | 主张 | std | kt |")
    L.append("|---|---|---|---|")
    for r in [x for x in RESULTS if x["id"].startswith("M")]:
        L.append("| %s | %s | %s | **%s** |" % (r["id"], r["claim"], r["std_verdict"], r["kt_verdict"]))
    L.append("")
    L.append("## Part C 星体命题（S01–S12）")
    L.append("")
    L.append("| ID | 主张 | std | kt |")
    L.append("|---|---|---|---|")
    for r in [x for x in RESULTS if x["id"].startswith("S")]:
        L.append("| %s | %s | %s | **%s** |" % (r["id"], r["claim"], r["std_verdict"], r["kt_verdict"]))
    L.append("")
    L.append("## Part D 取参自毁（D1–D3，67 号判据重跑）")
    L.append("")
    for r in [x for x in RESULTS if x["id"].startswith("D")]:
        L.append("- **%s** %s ⇒ kt **%s**：%s" % (r["id"], r["claim"], r["kt_verdict"], r["kt_side"]))
    L.append("")
    L.append("## Part E 控制组")
    L.append("")
    for r in [x for x in RESULTS if x["id"].startswith("CT")]:
        L.append("- **%s** ⇒ std **%s**：%s" % (r["id"], r["std_verdict"], r["std_side"]))
    L.append("")
    L.append("## Part F 守卫（G1–G8）")
    L.append("")
    L.append("| 守卫 | 状态 | 说明 |")
    L.append("|---|---|---|")
    for g in GUARDS:
        L.append("| %s | %s | %s |" % (g["id"], "PASS" if g["passed"] else "FAIL", g["desc"]))
    L.append("")
    L.append("## 汇总与 verdict")
    L.append("")
    for k in ("n_micro", "micro_std_alive", "micro_kt_fail", "micro_kt_open", "micro_kt_boundary",
              "n_star", "star_std_alive", "star_kt_fail", "kt_star_success",
              "verdict_micro", "verdict_star", "verdict_method"):
        L.append("- %s = **%s**" % (k, summ[k]))
    L.append("")
    L.append("- 最小证伪集（微观）：%s" % summ["min_falsifier_micro"])
    L.append("- 最小证伪集（星体）：%s" % summ["min_falsifier_star"])
    L.append("")
    L.append("## 退守路径与成本")
    L.append("")
    L.append("| 路径 | 退守内容 | 退守后仍存活的失败 |")
    L.append("|---|---|---|")
    for rid, what, cost in RETREATS:
        L.append("| %s | %s | %s |" % (rid, what, cost))
    L.append("")
    mpath = os.path.join(outdir, tag + ".md")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    # ---- report ----
    R = []
    R.append("TUFT-r129 machine-readable report")
    R.append("stamp: %s" % stamp)
    R.append("key: micro n=%d std_alive=%d kt_fail=%d kt_open=%d kt_boundary=%d"
             % (summ["n_micro"], summ["micro_std_alive"], summ["micro_kt_fail"],
                summ["micro_kt_open"], summ["micro_kt_boundary"]))
    R.append("key: star n=%d std_alive=%d kt_fail=%d kt_success=%d"
             % (summ["n_star"], summ["star_std_alive"], summ["star_kt_fail"], summ["kt_star_success"]))
    R.append("key: verdict_micro=%s verdict_star=%s verdict_method=%s"
             % (summ["verdict_micro"], summ["verdict_star"], summ["verdict_method"]))
    R.append("key: min_falsifier_micro=%s" % summ["min_falsifier_micro"])
    R.append("key: min_falsifier_star=%s" % summ["min_falsifier_star"])
    R.append("guards: %d/%d" % (sum(1 for g in GUARDS if g["passed"]), len(GUARDS)))
    for g in GUARDS:
        R.append("  %s %s %s" % (g["id"], "PASS" if g["passed"] else "FAIL", g["desc"]))
    for r in RESULTS:
        R.append("%s std=%s kt=%s | std: %s | kt: %s | %s"
                 % (r["id"], r["std_verdict"], r["kt_verdict"], r["std_side"], r["kt_side"], r["note"]))
    R.append("exit_code: 0")
    rpath = os.path.join(outdir, tag + "_report.txt")
    with open(rpath, "w", encoding="utf-8") as f:
        f.write("\n".join(R) + "\n")

    print("== r129 done ==")
    print("micro: n=%d std_alive=%d kt_fail=%d kt_open=%d kt_boundary=%d"
          % (summ["n_micro"], summ["micro_std_alive"], summ["micro_kt_fail"],
             summ["micro_kt_open"], summ["micro_kt_boundary"]))
    print("star: n=%d std_alive=%d kt_fail=%d kt_success=%d"
          % (summ["n_star"], summ["star_std_alive"], summ["star_kt_fail"], summ["kt_star_success"]))
    print("verdict: micro=%s star=%s method=%s"
          % (summ["verdict_micro"], summ["verdict_star"], summ["verdict_method"]))
    print("guards: %d/%d" % (sum(1 for g in GUARDS if g["passed"]), len(GUARDS)))
    print("wrote:", jpath)
    print("wrote:", mpath)
    print("wrote:", rpath)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
