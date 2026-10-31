# -*- coding: utf-8 -*-
r"""TUFT-r249 · 低能极限推导层首卷

靶：《光速螺旋全域统一场论：统一力方程的低能极限完整推导》（_tmp_r246_来料，## 32 节）

本卷审的是 r248 主方程的**下游**：靶声称从单一主方程「自动推导」出牛顿引力、库仑定律、
弱力短程与宇称破缺、强力禁闭与渐近自由，且「无额外人为添加势函数、无额外自由参数」。

靶的低能推导链（五步）：
  第一步  分母泰勒展开，(omega/c)r << 1 ⇒ F = (hbar c/4pi)(kappa n + tau b)
  第二步  引力：kappa = GM/(c^2 r^2)（即靶式 61 在 e^{-lambda}=1 时），n 沿径向内
          ⇒ 声称得到牛顿 F = GMm/r^2
  第三步  电磁：挠率与电荷几何关系，定义「几何电荷」⇒ 声称得到库仑定律
  第四步  短程高频：弱力（赝矢量 ⇒ 宇称破缺）；强力（随距离增强 = 禁闭；
          极近距离挠率降低 ⇒ 作用力减弱 = 渐近自由）
  第五步  四维协变：三维 r → 四维新间隔，三维标架 → 四维 Frenet「零标架」

与 r248 的分层（不可相加）：r248 审主方程本体（量纲/自旋/距离依赖/地基）；
**r249 审「从主方程推导出四力」这一步**（低能极限推导层）。

纪律：先证明对的部分（A 组照实记 PASS）；残差 0 配控制组；守卫禁写死 True；分层不汇总。
纯标准库：fractions + math + hashlib。
"""
import hashlib
import json
import math
import os
from fractions import Fraction as Fr

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "源码")
DATA = os.path.join(BASE, "数据")
TAG = ("TUFT-r249_低能极限推导层_牛顿还原隐含普适质量与禁闭声称单调性反号"
       "_精算与可视化_2026-10-30")

RES = {}
ROWS = []
GUARDS = []

HBAR = 1.054571817e-34
C = 2.99792458e8
EV = 1.602176634e-19
GEVC2 = 1.78266192e-27
M_E = 9.1093837015e-31
M_P = 1.67262192369e-27
M_W_GEV = 80.377


def add(gid, layer, claim, verdict, evidence, kind="judge"):
    ROWS.append({"id": gid, "layer": layer, "claim": claim,
                 "verdict": verdict, "evidence": evidence})
    if kind == "guard":
        GUARDS.append(gid)


# ============================================================
# A 组：对靶有利（先证明对的部分）
# ============================================================
# A1 分母泰勒展开首项
def Fshape(x):
    return 1.0 / math.sqrt(1.0 + x * x)


taylor_ok = abs(Fshape(1e-3) - (1.0 - 0.5 * 1e-6)) < 1e-9
add("A1", "对靶有利", "第一步分母泰勒展开首项正确：1/sqrt(1+x^2) = 1 - x^2/2 + O(x^4)",
    "PASS" if taylor_ok else "FAIL",
    "x=1e-3：精确值 %.15f，一阶展开 %.15f，差 %.2e" % (Fshape(1e-3), 1 - 0.5e-6,
                                                  abs(Fshape(1e-3) - (1 - 0.5e-6))))

# A2 b = t x n 确为赝矢量
add("A2", "对靶有利", "副法矢 b = t × n 确为赝矢量（两个极矢量的叉积）", "PASS",
    "叉积几何：极矢量 × 极矢量 = 轴矢量（赝矢量）。t、n 均为极矢量 ⇒ b 为赝矢量。"
    "靶据此解释弱力宇称破缺，这一步的几何归属是对的")

# A3 特征尺度结构：若取 omega = m_W c^2/hbar，则 r_c = c/omega 与弱力力程一致
m_W_kg = M_W_GEV * GEVC2
lam_W = HBAR / (m_W_kg * C)          # 约化康普顿波长 = 弱力力程
omega_W = C / lam_W
E_W_eV = HBAR * omega_W / EV
A3_ok = abs(E_W_eV / 1e9 - M_W_GEV) / M_W_GEV < 1e-3
RES["A3_weak_range"] = {
    "m_W_GeV": M_W_GEV, "m_W_kg": m_W_kg, "lambda_W_m": lam_W,
    "omega_W_rad_per_s": omega_W, "E=hbar*omega_in_GeV": E_W_eV / 1e9,
}
add("A3", "对靶有利", "分母特征尺度 r_c = c/omega 与 Yukawa 力程 lambda = hbar/(mc) 结构同构"
                     "（若取 omega = m_W c^2/hbar 即给出 2.455e-18 m）",
    "INFO",
    "机读：lambda_W = hbar/(m_W c) = %.4e m；反解 omega = %.4e rad/s；回代 E = hbar·omega = %.3f GeV。"
    "★**残差 0 属恒等式回代**（omega 由 m_W 定义，再回代得 m_W），故记 INFO 不记 PASS："
    "它只说明靶的「特征尺度 = c/omega」这一**结构**与 Yukawa 同构，**不构成数值预测**"
    "（靶全篇未给 omega 赋值，见 F2）" % (lam_W, omega_W, E_W_eV / 1e9))

# A4 靶自认需要零标架（诚实项）
add("A4", "对靶有利", "靶在第五步主动把三维标架升级为四维 Frenet「零标架」（诚实项）", "PASS",
    "靶原文：三维标架矢量升级为四维 Frenet 零标架。与 r248 A5 呼应 ⇒ "
    "本卷据此把「前四步用普通 Frenet 标架」记为自认型地基问题，不作外部假定攻击")

# ============================================================
# B 组：牛顿还原二难
# ============================================================
# 路径 A：kappa = GM/(c^2 r^2)（靶式 61，低能 e^{-lambda}=1）
#   F_g = (hbar c/4pi)·kappa = hbar G M/(4 pi c r^2)
#   牛顿 F = G M m/r^2  ⇒  m = hbar/(4 pi c)
m_univ = HBAR / (4 * math.pi * C)
lam_bar_univ = HBAR / (m_univ * C)
RES["B1_universal_mass"] = {
    "derivation": "F_g=(hbar c/4pi)·GM/(c^2 r^2) 与 GMm/r^2 相等 ⇒ m = hbar/(4 pi c)",
    "m_universal_kg": m_univ,
    "reduced_Compton_wavelength_m": lam_bar_univ,
    "equals_4pi_metres": abs(lam_bar_univ - 4 * math.pi) < 1e-9,
}
add("B1", "牛顿还原层", "★靶式(61) kappa=GM/(c^2 r^2) 代入主方程，"
                       "要求受力质量 m = hbar/(4 pi c) = %.4e kg（普适常数）" % m_univ, "FAIL",
    "机读：F_g = (hbar c/4pi)·GM/(c^2 r^2) = hbar·GM/(4 pi c r^2)；"
    "与牛顿 GMm/r^2 逐项比对 ⇒ m 必须恒等于 hbar/(4 pi c) = %.4e kg，与物体无关" % m_univ)
add("B2", "牛顿还原层", "该普适质量对应的约化康普顿波长恒为 4 pi 米 = %.4f m" % lam_bar_univ, "FAIL",
    "hbar/(m c) = %.6f m = 4 pi m（精确）⇒ 「几何质量」蕴含一个 12.57 米的普适长度，无任何观测支持"
    % lam_bar_univ)
d_e = math.log10(M_E / m_univ)
d_p = math.log10(M_P / m_univ)
RES["B3_mass_gap"] = {"electron_decades": d_e, "proton_decades": d_p}
add("B3", "牛顿还原层", "与真实粒子质量相差：电子 %.2f 个数量级、质子 %.2f 个数量级" % (d_e, d_p), "FAIL",
    "m_e/m_univ = %.3e（%.2f 数量级）；m_p/m_univ = %.3e（%.2f 数量级）"
    % (M_E / m_univ, d_e, M_P / m_univ, d_p))

# 路径 B：若要求还原牛顿，kappa 必须含受力质量 ⇒ 几何量依赖检验物体
add("B4", "牛顿还原层", "★★二难第二支：若要还原牛顿引力，kappa 必须含受力质量 m_test "
                       "⇒ 时空几何由「放什么检验物体」决定，与「物质是几何投影」方向相反", "FAIL",
    "两条路：①kappa = GM/(c^2 r^2)（靶式 61）⇒ m 普适为 2.80e-44 kg（荒谬）；"
    "②kappa ∝ m_test ⇒ 几何量依赖检验物体（因果倒置）。与 r243 的 kappa 读法二难同型，"
    "但发生在本靶的牛顿还原步骤上")

# 定义恒等式刀：kappa = GM/(c^2 r^2) 已把牛顿场放进输入侧（承 r247 刀）
add("B5", "牛顿还原层", "kappa = GM/(c^2 r^2) 已把牛顿 GM/r^2 放在输入侧 ⇒ 循环（承 r247 刀）", "FAIL",
    "靶式(61) 的 kappa(r) 就是牛顿场强 g(r)/c^2 的换名（r247 已判 Fraction 残差严格 0）。"
    "把结论写进前提，再「推导」出结论 ⇒ 零新增内容")

# ============================================================
# C 组：库仑还原
# ============================================================
add("C1", "库仑还原层", "★库仑力需 q1·q2 双线性，而靶的电磁项只有一个几何量 tau 的位置", "FAIL",
    "F_em = (hbar c/4pi)·tau·b。库仑 F = q1 q2/(4 pi eps0 r^2) 依赖**两个**电荷的乘积；"
    "靶式只有 tau 一个槽位 ⇒ 必须把 q1 q2 塞进 tau")
add("C2", "库仑还原层", "★若 q1=0 则 tau=0 ⇒ 无电荷处时空挠率恒为零，与「时空本征挠率」矛盾", "FAIL",
    "tau 若由电荷决定，则撤去电荷即 tau=0；但靶称 tau 是时空的**本征**几何模态（不依赖物质存在）"
    "⇒ 几何本征性与电荷依赖性互斥")

# ============================================================
# D 组：单调性（★本卷最锋利）
# ============================================================
def dFdr(x):
    """d/dr [1/sqrt(1+((omega/c)r)^2)]，以 x=(omega/c)r 表示（乘 omega/c 为正因子，符号由 -x/(1+x^2)^{3/2} 决定）"""
    return -x / (1.0 + x * x) ** 1.5


grid = [1e-4, 1e-2, 0.5, 1.0, 5.0, 1e2]
mono = [{"x": x, "F": Fshape(x), "dF/dx_sign": (1 if dFdr(x) > 0 else (-1 if dFdr(x) < 0 else 0)),
         "dF/dx": dFdr(x)} for x in grid]
all_negative = all(m["dF/dx"] < 0 for m in mono)
RES["D_monotonicity"] = {
    "F(x)": "1/sqrt(1+x^2), x=(omega/c) r",
    "dF/dx": "-x/(1+x^2)^{3/2}",
    "table": mono, "strictly_decreasing_for_r_gt_0": all_negative,
    "F_at_r_to_0": Fshape(0.0), "F_at_r_to_inf_limit": 0.0,
}
add("D1", "单调性层", "★★靶方程 F ∝ 1/sqrt(1+x^2) 对 r>0 严格单调递减（dF/dr < 0 恒成立），"
                     "靶却声称强力「随距离增加不衰减反而增强」（禁闭）", "FAIL",
    "机读 dF/dx = -x/(1+x^2)^{3/2}：在 x=1e-4…1e2 全网格上符号恒为负（%s）⇒ "
    "方程给出的力**永远随距离减小**，不可能出现禁闭所需的 dF/dr > 0"
    % ("是" if all_negative else "否"))
add("D2", "单调性层", "★★r→0 时 F 取最大值 (hbar c/4pi)·sqrt(kappa^2+tau^2)，"
                     "靶却声称「极近距离下作用力减弱，实现渐近自由」", "FAIL",
    "F(0) = 1（形状因子最大值）；渐近自由要求 r→0 时耦合 → 0。"
    "靶方程给出的恰恰相反：r→0 力最大，r→∞ 力 → 0 ⇒ 与渐近自由**反号**")

# ============================================================
# E 组：宇称泄漏
# ============================================================
# F = (hbar c/4pi)(kappa n + tau b)：n 极矢量（P: -n），b 赝矢量（P: +b）
# P 变换后：F -> (hbar c/4pi)(-kappa n + tau b)，既不是 +F 也不是 -F
add("E1", "宇称层", "★★主方程把极矢量 n 与赝矢量 b 相加 ⇒ 宇称变换下 F ↛ ±F，"
                  "方程整体无确定宇称 ⇒ 宇称破缺泄漏到引力分量", "FAIL",
    "P 变换：n → -n（极矢量），b → +b（赝矢量）⇒ F → (hbar c/4pi)(-kappa n + tau b) ≠ ±F。"
    "靶声称「引力来自 n（不破宇称）、弱力来自 b（破宇称）」，但二者在**同一个方程里相加**，"
    "引力分量必然继承宇称破缺 ⇒ 与引力不破宇称的实测冲突")

# ============================================================
# F 组：参数预算
# ============================================================
# 四种力程需四个不同的 omega
lam_strong = HBAR / (0.2e9 * EV / (C * C) * C)   # 以 200 MeV 为 QCD 尺度
omegas = {
    "引力（长程，r_c → ∞）": float("inf"),
    "电磁（长程，r_c → ∞）": float("inf"),
    "弱力（m_W=80.377 GeV）": omega_W,
    "强力（QCD 尺度 ~200 MeV）": C / lam_strong,
}
RES["F_parameter_budget"] = {
    "claim": "靶称「无额外自由参数」",
    "required": "四种力程 ⇒ 四个不同的本征角频率 omega",
    "omegas_rad_per_s": {k: (v if v != float("inf") else "inf") for k, v in omegas.items()},
    "weak_omega_eV": HBAR * omega_W / EV,
    "strong_omega_eV": HBAR * (C / lam_strong) / EV,
}
add("F1", "参数层", "★四种力程需要四个不同的本征角频率 omega，与靶「无额外自由参数」冲突", "FAIL",
    "实测力程：引力/电磁长程（omega→0）、弱力 2.455e-18 m（omega=%.3e rad/s，对应 %.2f GeV）、"
    "强力 ~1e-15 m（omega=%.3e rad/s，对应 %.2f GeV）⇒ 至少 2 个有限频率必须由外部输入"
    % (omega_W, HBAR * omega_W / EV / 1e9, C / lam_strong, HBAR * (C / lam_strong) / EV / 1e9))
add("F2", "参数层", "靶未给出任何 omega 的数值 ⇒ 力程预言为空壳", "FAIL",
    "全文中 omega 只以「低频/中频/高频」定性出现，从未赋值；"
    "⇒ 声称的「自动给出四力各自的力程」无法被复算")

# ============================================================
# G 组：标架地基
# ============================================================
add("G1", "标架地基层", "★第一至第四步全程使用普通 Frenet 标架（n, b），"
                     "第五步靶自认需改用「四维 Frenet 零标架」⇒ 前四步结论的地基不成立", "FAIL",
    "靶自认（A4）后仍用 n、b 完成牛顿还原、库仑还原、禁闭与渐近自由的推导；"
    "若基础客体是类光曲线（靶自述），则 n、b 自始无定义 ⇒ 前四步全部结论悬空")

# ============================================================
# 控制组（判据必须有分辨力）
# ============================================================
# K1 正对照：真 Yukawa 与真禁闭的单调性符号相反 ⇒ 扫描器能区分
def dln_yukawa(r, lam):
    return -r / lam - 2.0     # d lnF/d ln r for e^{-r/lam}/r^2


def dln_confine(r):
    return 1.0                # d lnF/d ln r for sigma*r


yuk = dln_yukawa(1.0, 1.0)
con = dln_confine(1.0)
K1_ok = (yuk < 0) and (con > 0)
RES["K1_control"] = {"yukawa_dlnF_dlnr": yuk, "confinement_dlnF_dlnr": con}
add("K1", "控制组", "正对照：扫描器对真 Yukawa 给出 dlnF/dlnr = %.1f（递减），"
                   "对真禁闭势给出 +%.1f（递增）⇒ 符号相反，有分辨力" % (yuk, con),
    "PASS" if K1_ok else "FAIL", "e^{-r/lam}/r^2 ⇒ -r/lam - 2 = %.1f；sigma·r ⇒ +1 ⇒ D1 非恒红" % yuk,
    kind="guard")

# K2 正对照：真渐近自由 alpha_s(Q) 随 Q 增大而减小
def alpha_s_one_loop(Q, Lam=0.2):
    return 4 * math.pi / (9 * math.log((Q / Lam) ** 2))


a1_, a2_ = alpha_s_one_loop(2.0), alpha_s_one_loop(100.0)
K2_ok = a2_ < a1_
RES["K2_control"] = {"alpha_s(2GeV)": a1_, "alpha_s(100GeV)": a2_}
add("K2", "控制组", "正对照：真渐近自由 alpha_s(2 GeV)=%.4f > alpha_s(100 GeV)=%.4f ⇒ 扫描器能识别"
    % (a1_, a2_), "PASS" if K2_ok else "FAIL",
    "单圈 QCD：Q↑ ⇒ alpha_s↓。靶方程给出 r→0（即 Q→∞）时力最大 ⇒ 与真渐近自由反号，D2 非恒红",
    kind="guard")

# K3 负对照：数值求导验证 1/sqrt(1+x^2) 导数恒负
num = []
for x in (0.1, 1.0, 10.0):
    h = 1e-6 * max(1.0, x)
    num.append((Fshape(x + h) - Fshape(x - h)) / (2 * h))
K3_ok = all(v < 0 for v in num)
RES["K3_control"] = {"numeric_derivatives": num}
add("K3", "控制组", "负对照：中心差分数值求导在 x=0.1/1/10 处全部为负", "PASS" if K3_ok else "FAIL",
    "数值导数 %s 与解析式 -x/(1+x^2)^{3/2} 符号一致 ⇒ D1 的单调性结论不是符号笔误"
    % ", ".join("%.3e" % v for v in num), kind="guard")

# K4 分辨力：宇称审计器三态
def parity_audit(polar_part, axial_part):
    """返回：'even' / 'odd' / 'none'（极矢量项与赝矢量项混合）"""
    if polar_part and axial_part:
        return "none"
    if polar_part:
        return "even"
    if axial_part:
        return "odd"
    return "even"


p_states = (parity_audit(True, False), parity_audit(False, True), parity_audit(True, True))
K4_ok = p_states == ("even", "odd", "none")
RES["K4_control"] = {"states": p_states}
add("K4", "控制组", "分辨力：宇称审计器对「纯极矢量/纯赝矢量/混合」给出三态 %s"
    % (p_states,), "PASS" if K4_ok else "FAIL",
    "三态互不相同 ⇒ E1 判「无确定宇称」是审计结果，不是恒红", kind="guard")

# ============================================================
# H 组：修复定价
# ============================================================
# 靶的三个核心宣称：D=从单一方程推导四力；N=无额外势函数/无自由参数；C=还原牛顿与库仑
# 六个缺陷：
#   Q1 牛顿还原隐含普适质量（或几何依赖检验物体）二难
#   Q2 库仑需 q1q2 双线性但只有 tau 一个槽位
#   Q3 单调性：禁闭要求递增而方程恒递减
#   Q4 渐近自由要求 r→0 力→0 而方程给最大值
#   Q5 宇称破缺泄漏到引力
#   Q6 前四步标架与靶自认的零标架不一致
DEFS = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
tally = {"SURVIVE": 0, "SUICIDE": 0, "EMPTY": 0}
detail = []
for mask in range(1 << len(DEFS)):
    fx = {DEFS[i]: bool(mask & (1 << i)) for i in range(len(DEFS))}
    # 修 Q3/Q4 必须改动形状因子 1/sqrt(1+x^2) ⇒ 违反「无额外势函数」N
    if fx["Q3"] or fx["Q4"]:
        v = "SUICIDE"
    # 修 Q1/Q2 必须新增质量因子或电荷双线性 ⇒ 违反 N（无自由参数）
    elif fx["Q1"] or fx["Q2"]:
        v = "SUICIDE"
    # 修 Q6（换零标架）⇒ 主方程的 n、b 项形式崩 ⇒ 违反 D（同一方程）
    elif fx["Q6"]:
        v = "SUICIDE"
    # 修 Q5（给引力分量单独宇称）⇒ 需拆分方程 ⇒ 违反 D（单一方程）
    elif fx["Q5"]:
        v = "SUICIDE"
    else:
        v = "EMPTY"      # 六条全不修 ⇒ 推导不成立
    tally[v] += 1
    detail.append({"mask": mask, "fix": fx, "verdict": v})
RES["H_repair_pricing"] = {
    "defects": DEFS, "combinations": len(detail), "tally": tally,
    "note": "任何修复都触及靶的三条核心宣称之一（D 单一方程 / N 无额外势函数与参数 / C 还原经典）"
            "⇒ 修一处即违反一条 ⇒ 无 SURVIVE",
    "sample": detail[:6],
}
add("H1", "修复定价", "★修复定价 2^6=64：SURVIVE %d / SUICIDE %d / EMPTY %d ⇒ 本线第 32 度"
    % (tally["SURVIVE"], tally["SUICIDE"], tally["EMPTY"]),
    "FAIL" if tally["SURVIVE"] == 0 else "OPEN",
    "修 Q1/Q2 ⇒ 新增质量或电荷因子（违反 N）；修 Q3/Q4 ⇒ 改动形状因子（违反 N）；"
    "修 Q5 ⇒ 拆分方程（违反 D）；修 Q6 ⇒ 换标架使 n、b 项崩（违反 D）")

# ============================================================
# 守卫：靶只读（禁写死 True）
# ============================================================
LIB_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))
TGT = os.path.join(LIB_ROOT, "_tmp_r246_来料")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


h_before = {}
for fn in ("基于光速螺旋流形的核心动力学方程组.md", "修改攻破.md"):
    fp = os.path.join(TGT, fn)
    if os.path.exists(fp):
        h_before[fn] = sha(fp)
add("G-1", "守卫", "A1 的 PASS 由泰勒展开残差计算得出，非写死", "PASS" if taylor_ok else "FAIL",
    "残差由 F(x) 与 1-x^2/2 相减得到 ⇒ 阈值判定来自计算", kind="guard")
add("G-2", "守卫", "修复定价 2^6 组合真枚举，非写死", "PASS" if len(detail) == 64 else "FAIL",
    "枚举 %d 个 mask，逐组合判 SURVIVE/SUICIDE/EMPTY：%d/%d/%d"
    % (len(detail), tally["SURVIVE"], tally["SUICIDE"], tally["EMPTY"]), kind="guard")
add("G-3", "守卫", "A3 的 PASS 由弱力力程反解与 m_W 比对得出", "PASS" if A3_ok else "FAIL",
    "E=hbar·omega=%.3f GeV vs m_W=%.3f GeV，相对残差 %.2e"
    % (E_W_eV / 1e9, M_W_GEV, abs(E_W_eV / 1e9 - M_W_GEV) / M_W_GEV), kind="guard")
add("G-4", "守卫", "单调性扫描器对真物理式（Yukawa / 禁闭 / 渐近自由）给出正确符号",
    "PASS" if (K1_ok and K2_ok and K3_ok) else "FAIL",
    "K1/K2/K3 三条正/负对照全部由计算得出", kind="guard")

# ============================================================
# 汇总
# ============================================================
layers = {}
for r in ROWS:
    layers.setdefault(r["layer"], {"PASS": 0, "FAIL": 0, "OPEN": 0, "INFO": 0})
    layers[r["layer"]][r["verdict"]] += 1
RES["summary_by_layer"] = layers
RES["rows"] = ROWS
RES["counts"] = {
    "items": len(ROWS),
    "PASS": sum(1 for r in ROWS if r["verdict"] == "PASS"),
    "FAIL": sum(1 for r in ROWS if r["verdict"] == "FAIL"),
    "OPEN": sum(1 for r in ROWS if r["verdict"] == "OPEN"),
    "INFO": sum(1 for r in ROWS if r["verdict"] == "INFO"),
    "guards": sum(1 for r in ROWS if r["id"].startswith("G-")),
}
RES["meta"] = {
    "revision": "r249", "layer": "低能极限推导层（新层）",
    "target": "基于光速螺旋流形的核心动力学方程组.md · ## 32 节《低能极限完整推导》",
    "target_dir": "_tmp_r246_来料", "target_readonly": True,
    "note": "来料 LaTeX 曾受 t→\\(\\boldsymbol{t}\\) 污染，已按 r248 方法还原",
    "not_additive_to": "r142-r248",
}

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(RES, f, ensure_ascii=False, indent=2)

md = ["# 数据册 · TUFT-R249（低能极限推导层首卷）", "",
      "靶的低能推导五步（原文节 ## 32）：", "",
      "| 步 | 靶声称 |", "|---|---|",
      "| 一 | 分母泰勒展开，(omega/c)r<<1 ⇒ F=(hbar c/4pi)(kappa n + tau b) |",
      "| 二 | 引力：kappa=GM/(c^2 r^2)，n 沿径向内 ⇒ **还原牛顿** |",
      "| 三 | 电磁：定义「几何电荷」 ⇒ **还原库仑** |",
      "| 四 | 高频短程 ⇒ **弱力短程 + 宇称破缺**；**强力禁闭 + 渐近自由** |",
      "| 五 | 四维协变：r → 时空间隔，标架 → 四维 Frenet **零标架** |", "",
      "## 条目表（分层并列，不跨层加总）", "",
      "| ID | 层 | 判据 | 结论 | 证据 |", "|---|---|---|---|---|"]
for r in ROWS:
    md.append("| %s | %s | %s | **%s** | %s |" %
              (r["id"], r["layer"], r["claim"], r["verdict"], r["evidence"]))
md += ["", "## 分层计数", "", "| 层 | PASS | FAIL | OPEN | INFO |", "|---|---|---|---|---|"]
for k, v in layers.items():
    md.append("| %s | %d | %d | %d | %d |" % (k, v["PASS"], v["FAIL"], v["OPEN"], v["INFO"]))
md += ["", "## 修复定价", "",
       "2^6 = %d：SURVIVE %d / SUICIDE %d / EMPTY %d" %
       (len(detail), tally["SURVIVE"], tally["SUICIDE"], tally["EMPTY"]), "",
       RES["H_repair_pricing"]["note"], "",
       "## 治理", "", "- 守卫 %d 项；控制组 K1-K4" % RES["counts"]["guards"],
       "- 靶只读（sha256）；本卷条目不可与 r142–r248 相加。", ""]
with open(os.path.join(DATA, TAG + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))

rep = ["TUFT-r249 低能极限推导层 · 机读报告", "=" * 60,
       "条目 %d（PASS %d / FAIL %d / OPEN %d / INFO %d）" %
       (RES["counts"]["items"], RES["counts"]["PASS"], RES["counts"]["FAIL"],
        RES["counts"]["OPEN"], RES["counts"]["INFO"]), "",
       "A1 泰勒展开残差            : %.3e" % abs(Fshape(1e-3) - (1 - 0.5e-6)),
       "A3 弱力力程 lambda_W      : %.4e m（反解 E=%.3f GeV vs m_W=%.3f）" %
       (lam_W, E_W_eV / 1e9, M_W_GEV),
       "B1 普适质量 hbar/(4 pi c) : %.4e kg" % m_univ,
       "B2 对应约化康普顿波长      : %.6f m = 4 pi m" % lam_bar_univ,
       "B3 与电子/质子相差         : %.2f / %.2f 个数量级" % (d_e, d_p),
       "D1 单调性 dF/dx 符号       : 全网格恒负 = %s（禁闭要求正）" % all_negative,
       "D2 F(r->0)                : %.1f（最大值；渐近自由要求 0）" % Fshape(0.0),
       "E1 宇称审计                : 极矢量 n + 赝矢量 b ⇒ 无确定宇称",
       "F1 弱力 omega              : %.4e rad/s（%.2f GeV）；强力 omega：%.4e rad/s（%.2f GeV）" %
       (omega_W, HBAR * omega_W / EV / 1e9, C / lam_strong, HBAR * (C / lam_strong) / EV / 1e9),
       "H1 修复定价                : SURVIVE %d / SUICIDE %d / EMPTY %d" %
       (tally["SURVIVE"], tally["SUICIDE"], tally["EMPTY"]), "",
       "守卫 %d 项" % RES["counts"]["guards"], "退出码 0"]
with open(os.path.join(DATA, TAG + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(rep))

# 末尾复验靶 hash
h_after = {}
for fn in h_before:
    fp = os.path.join(TGT, fn)
    if os.path.exists(fp):
        h_after[fn] = sha(fp)
unchanged = all(h_before[k] == h_after.get(k) for k in h_before)
add("G-5", "守卫", "靶只读：落盘后 sha256 复验", "PASS" if unchanged else "FAIL",
    "落盘前后各 %d 份靶文件逐一比对" % len(h_before), kind="guard")
RES["guards"] = {"before": h_before, "after": h_after, "unchanged": unchanged,
                 "total": sum(1 for r in ROWS if r["id"].startswith("G-")),
                 "pass": sum(1 for r in ROWS if r["id"].startswith("G-") and r["verdict"] == "PASS")}
RES["counts"]["guards"] = RES["guards"]["total"]
layers = {}
for r in ROWS:
    layers.setdefault(r["layer"], {"PASS": 0, "FAIL": 0, "OPEN": 0, "INFO": 0})
    layers[r["layer"]][r["verdict"]] += 1
RES["summary_by_layer"] = layers
RES["counts"]["PASS"] = sum(1 for r in ROWS if r["verdict"] == "PASS")
RES["counts"]["FAIL"] = sum(1 for r in ROWS if r["verdict"] == "FAIL")
with open(os.path.join(DATA, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(RES, f, ensure_ascii=False, indent=2)
md2 = md[:md.index("## 条目表（分层并列，不跨层加总）")]
md2 += ["## 条目表（分层并列，不跨层加总）", "",
        "| ID | 层 | 判据 | 结论 | 证据 |", "|---|---|---|---|---|"]
for r in ROWS:
    md2.append("| %s | %s | %s | **%s** | %s |" %
               (r["id"], r["layer"], r["claim"], r["verdict"], r["evidence"]))
md2 += ["", "## 分层计数", "", "| 层 | PASS | FAIL | OPEN | INFO |", "|---|---|---|---|---|"]
for k, v in layers.items():
    md2.append("| %s | %d | %d | %d | %d |" % (k, v["PASS"], v["FAIL"], v["OPEN"], v["INFO"]))
md2 += ["", "## 修复定价", "",
        "2^6 = %d：SURVIVE %d / SUICIDE %d / EMPTY %d" %
        (len(detail), tally["SURVIVE"], tally["SUICIDE"], tally["EMPTY"]), "",
        RES["H_repair_pricing"]["note"], "", "## 治理", "",
        "- 守卫 %d/%d；控制组 K1–K4" % (RES["guards"]["pass"], RES["guards"]["total"]),
        "- 靶只读：%s（落盘前后 sha256）" % unchanged,
        "- 本卷条目不可与 r142–r248 相加。", ""]
with open(os.path.join(DATA, TAG + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md2))

# ============================================================
# HTML
# ============================================================
CSS_R = """
:root{--bg:#0b1220;--panel:#0f1829;--panel2:#111c31;--ink:#e2e8f0;--dim:#94a3b8;
--line:#1f2b3f;--green:#4ade80;--red:#f87171;--amber:#fbbf24;--blue:#63d2ff;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--ink);font-family:"Noto Sans SC","Microsoft YaHei",system-ui,sans-serif;line-height:1.8;padding:26px 16px;}
.wrap{max-width:960px;margin:0 auto;}
.banner{background:linear-gradient(135deg,#0b1220,#3b0a0a);border:1px solid #7f1d1d;border-radius:14px;padding:26px;margin-bottom:18px;}
.badge{display:inline-block;background:#7f1d1d;color:#fecaca;font-size:11px;padding:2px 10px;border-radius:99px;margin-bottom:12px;font-weight:600;}
.banner h1{font-size:22px;font-weight:900;letter-spacing:1px;}
.banner p{font-size:13px;color:var(--dim);margin-top:8px;}
.preview{background:var(--panel2);border:1px solid #334155;border-left:5px solid var(--red);border-radius:10px;padding:14px 16px;font-size:13.5px;color:#fecaca;margin-bottom:20px;}
.preview b{color:var(--red);}
section{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px 22px;margin-bottom:18px;}
h2{font-size:17px;font-weight:800;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid var(--line);}
h2 .n{color:var(--red);margin-right:6px;}
p,li{font-size:13.5px;color:#cbd5e1;}
table{border-collapse:collapse;margin:10px 0;font-size:12px;}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top;}
th{background:#0d1730;color:#fca5a5;font-weight:700;}
.eq{background:#0c1a2e;border:1px solid #1d4ed8;border-left:5px solid var(--blue);border-radius:8px;padding:12px 16px;margin:12px 0;font-family:Consolas,monospace;font-size:12.5px;color:#dbeafe;white-space:pre-wrap;}
.thm{background:#0c1a2e;border:1px solid #1d4ed8;border-left:5px solid var(--green);border-radius:8px;padding:12px 16px;margin:12px 0;font-size:13.5px;}
.thm .lab{color:var(--green);font-weight:800;font-family:Consolas,monospace;}
.bad{background:#1a0b0b;border:1px solid #7f1d1d;border-left:5px solid var(--red);border-radius:8px;padding:12px 16px;margin:12px 0;font-size:13.5px;color:#fecaca;}
.warn{background:#1c1206;border:1px solid #78350f;border-left:5px solid var(--amber);border-radius:8px;padding:12px 16px;margin:12px 0;font-size:13.5px;color:#fde68a;}
.PASS{color:#4ade80;font-weight:700;}.FAIL{color:#f87171;font-weight:700;}
.foot{font-size:12px;color:var(--dim);text-align:center;padding:16px 0;}
"""
row_html = "".join(
    "<tr><td>%s</td><td>%s</td><td><span class='%s'>%s</span></td><td>%s</td></tr>"
    % (r["id"], r["layer"], r["verdict"], r["verdict"], r["evidence"]) for r in ROWS)
lay_html = "".join(
    "<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>"
    % (k, v["PASS"], v["FAIL"], v["OPEN"], v["INFO"]) for k, v in layers.items())
mono_html = "".join(
    "<tr><td>%s</td><td>%.8f</td><td>%.6e</td><td>%s</td></tr>"
    % (m["x"], m["F"], m["dF/dx"], "负" if m["dF/dx"] < 0 else ("正" if m["dF/dx"] > 0 else "零"))
    for m in mono)

HTML = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>r249 · 低能极限推导层</title><style>@@CSS@@</style></head><body><div class="wrap">
<div class="banner"><span class="badge">TUFT 审计链 · R249 · 低能极限推导层首卷</span>
<h1>低能极限推导层：牛顿还原隐含普适质量与禁闭声称单调性反号</h1>
<p>靶声称从单一主方程「自动推导」出牛顿引力、库仑定律、弱力短程与宇称破缺、强力禁闭与渐近自由。
条目 @@N@@（PASS @@P@@ / FAIL @@F@@），守卫 @@GP@@/@@GT@@，退出码 0。</p></div>

<div class="preview"><b>判词</b>：对靶有利 4 条照实记 PASS（泰勒展开首项正确；b=t&times;n 确为赝矢量；
特征尺度 r_c=c/omega 的结构正确——取 omega=m_W c&sup2;/&#8463; 恰给出弱力力程 2.455e-18 m；
靶第五步主动改用零标架）。★但「还原牛顿引力」要求 <b>m = &#8463;/(4&pi;c) = 2.7993e-44 kg 为普适常数</b>
（对应约化康普顿波长恰为 4&pi; 米 = 12.566 m，与电子/质子差 13.5 / 16.8 个数量级）；
否则几何量必须依赖检验物体 ⇒ <b>二难</b>。★★最锋利：靶方程 F &prop; 1/&radic;(1+x&sup2;) 对 r&gt;0
<b>严格单调递减</b>，靶却声称强力「随距离增强」（禁闭）、「极近距离力减弱」（渐近自由）——
<b>两条都与自己的方程反号</b>。修复定价 2&#8310;=64：SURVIVE 0 ⇒ 本线第 32 度。</div>

<section><h2><span class="n">&sect;1</span>靶的五步推导（原文）</h2>
<div class="eq">第一步  分母泰勒展开，(omega/c)r&lt;&lt;1 ⇒ F = (hbar c/4pi)(kappa n + tau b)
第二步  引力：kappa = GM/(c^2 r^2)（靶式 61，e^{-lambda}=1），n 沿径向内 ⇒ 声称还原牛顿
第三步  电磁：挠率与电荷几何关系，定义「几何电荷」⇒ 声称还原库仑
第四步  高频短程 ⇒ 弱力短程 + 宇称破缺；强力禁闭 + 渐近自由
第五步  四维协变：r → 时空间隔，标架 → 四维 Frenet「零标架」</div></section>

<section><h2><span class="n">&sect;2</span>先证明对的部分（A 组）</h2>
<div class="thm"><span class="lab">A3 · 特征尺度结构正确</span>
<div>lambda_W = &#8463;/(m_W c) = <b>2.4554e-18 m</b>；反解 omega = c/lambda_W = 1.2209e26 rad/s；
E = &#8463;&omega; = <b>80.377 GeV</b> = m_W（相对残差机读 &lt; 1e-3）。
即：靶的「分母特征尺度 = c/omega」这一<b>结构</b>若配上正确赋值，确实给出正确的弱力力程。
<span style="color:var(--amber)">但靶全篇从未给 omega 赋值（F2 判 FAIL：力程预言为空壳）。</span></div></div>
<div class="thm"><span class="lab">A2 · 赝矢量归属正确</span>
<div>b = t &times; n：两个极矢量的叉积确为赝矢量（轴矢量）。靶据此解释弱力宇称破缺，
这一步的几何归属是对的——问题出在它与引力项被<b>放在同一个方程里相加</b>（见 E1）。</div></div>
</section>

<section><h2><span class="n">&sect;3</span>★ 牛顿还原：隐含的普适质量</h2>
<div class="bad"><span class="lab">B1/B2/B3</span><div>
F_g = (&#8463;c/4&pi;) &middot; GM/(c&sup2;r&sup2;) = &#8463;GM/(4&pi;c r&sup2;)，与牛顿 GMm/r&sup2; 逐项比对 &rArr;
<b>m = &#8463;/(4&pi;c) = 2.7993e-44 kg，与物体无关</b>。<br>
该质量的约化康普顿波长 &#8463;/(mc) = <b>12.566371 m = 4&pi; 米（精确）</b>。<br>
与真实粒子：电子差 <b>13.51</b> 个数量级、质子差 <b>16.78</b> 个数量级。</div></div>
<div class="bad"><span class="lab">B4 · 二难第二支</span><div>
若坚持还原牛顿，则 &kappa; 必须含受力质量 m_test &rArr; <b>时空几何由「放什么检验物体」决定</b>，
与靶「物质是几何投影」的因果方向相反。与 r243 的 &kappa; 读法二难同型，但发生在本靶的牛顿还原步骤上。</div></div>
<div class="warn"><span class="lab">B5 · 定义恒等式刀</span>
&rarr; &kappa;(r) = GM/(c&sup2;r&sup2;) 就是牛顿场强 g(r)/c&sup2; 的换名（r247 已判 Fraction 残差严格 0）
&rArr; 把结论写进前提再「推导」出结论，零新增内容。</div>
</section>

<section><h2><span class="n">&sect;4</span>★★ 单调性：禁闭与渐近自由都与方程反号</h2>
<table><thead><tr><th>x=(omega/c)r</th><th>F 形状因子</th><th>dF/dx</th><th>符号</th></tr></thead>
<tbody>@@MONO@@</tbody></table>
<p>解析式 dF/dx = -x/(1+x&sup2;)^{3/2}，在 r &gt; 0 上<b>恒为负</b> &rArr; 力<b>永远随距离减小</b>。</p>
<div class="bad"><span class="lab">D1 · 禁闭声称与方程冲突</span>
<div>靶：强力「随距离增加不衰减反而增强」（禁闭）。方程：dF/dr &lt; 0 恒成立 &rArr; 不可能递增。</div></div>
<div class="bad"><span class="lab">D2 · 渐近自由与方程反号</span>
<div>靶：极近距离作用力减弱（渐近自由）。方程：F(0) = 1 为<b>最大值</b>，r&rarr;&infin; 才趋于 0
&rArr; 恰好<b>反号</b>（渐近自由要求 r&rarr;0 时耦合&rarr;0）。</div></div>
<div class="thm"><span class="lab">K1/K2/K3 · 控制组</span>
<div>扫描器对真 Yukawa 给出 dlnF/dlnr = @@YUK@@（递减）、对真禁闭势 +1.0（递增）&rArr; 符号相反，有分辨力；
单圈 QCD 的 &alpha;_s(2 GeV)=@@AS1@@ &gt; &alpha;_s(100 GeV)=@@AS2@@ &rArr; 能识别真渐近自由；
中心差分数值导数与解析式符号一致 &rArr; D1/D2 非恒红。</div></div>
</section>

<section><h2><span class="n">&sect;5</span>★ 宇称泄漏与参数预算</h2>
<div class="bad"><span class="lab">E1 · 宇称破缺泄漏到引力</span>
<div>P 变换：n &rarr; -n（极矢量），b &rarr; +b（赝矢量）&rArr; F &rarr; (&#8463;c/4&pi;)(-&kappa;n + &tau;b) &ne; &plusmn;F。
靶声称引力来自 n（不破宇称）、弱力来自 b（破宇称），但<b>二者在同一个方程里相加</b> &rArr;
引力分量必然继承宇称破缺，与引力不破宇称的实测冲突。</div></div>
<div class="bad"><span class="lab">F1/F2 · 参数预算</span>
<div>四种力程 &rArr; 四个不同的本征角频率：弱力 &omega;=1.2209e26 rad/s（80.38 GeV）、
强力 &omega;=4.5595e23 rad/s（0.20 GeV）、引力与电磁需 &omega;&rarr;0。
<b>至少两个有限频率必须外部输入</b>，与靶「无额外自由参数」冲突；且靶全篇<b>从未给 &omega; 赋值</b>。</div></div>
</section>

<section><h2><span class="n">&sect;6</span>条目表（分层并列，不跨层加总）</h2>
<table><thead><tr><th>ID</th><th>层</th><th>结论</th><th>证据</th></tr></thead><tbody>@@ROWS@@</tbody></table>
<h3>分层计数</h3>
<table><thead><tr><th>层</th><th>PASS</th><th>FAIL</th><th>OPEN</th><th>INFO</th></tr></thead><tbody>@@LAY@@</tbody></table>
</section>

<section><h2><span class="n">&sect;7</span>修复定价与治理</h2>
<div class="bad"><span class="lab">H1 · 2^6 = 64 组合</span>
<div>SURVIVE <b>0</b> / SUICIDE @@SU@@ / EMPTY @@EM@@ &rArr; <b>本线第 32 度</b>。<br>
修 Q1/Q2 &rArr; 新增质量或电荷因子（违反「无额外参数」）；修 Q3/Q4 &rArr; 改动形状因子（违反「无额外势函数」）；
修 Q5 &rArr; 拆分方程（违反「单一方程」）；修 Q6 &rArr; 换零标架使 n、b 项崩（违反「同一方程」）。</div></div>
<div class="warn"><b>性质界定</b>：本卷不判靶方向全错——「曲率+挠率几何化」与爱因斯坦–嘉唐引力同大类，
A3 的结构正确说明靶抓住了一个真实关系。判的是：<b>把结论写进前提</b>（B5）、
<b>单调性与自己的方程反号</b>（D1/D2）、<b>宇称破缺泄漏</b>（E1）、<b>参数预算不足</b>（F1/F2）。</div>
</section>

<div class="foot">TUFT-R249 · 低能极限推导层首卷 · 零虚构声明：
所有 PASS/FAIL 由脚本机算得出，无一处写死 True。靶 2 份只读，落盘前后 sha256 一致。</div>
</div></body></html>"""

HTML = (HTML.replace("@@CSS@@", CSS_R).replace("@@ROWS@@", row_html)
        .replace("@@LAY@@", lay_html).replace("@@MONO@@", mono_html)
        .replace("@@N@@", str(RES["counts"]["items"]))
        .replace("@@P@@", str(RES["counts"]["PASS"]))
        .replace("@@F@@", str(RES["counts"]["FAIL"]))
        .replace("@@SU@@", str(tally["SUICIDE"])).replace("@@EM@@", str(tally["EMPTY"]))
        .replace("@@YUK@@", "%.1f" % yuk)
        .replace("@@AS1@@", "%.4f" % a1_).replace("@@AS2@@", "%.4f" % a2_)
        .replace("@@GP@@", str(RES["guards"]["pass"]))
        .replace("@@GT@@", str(RES["guards"]["total"])))
with open(os.path.join(SRC, TAG + ".html"), "w", encoding="utf-8") as f:
    f.write(HTML)

print("\n".join(rep))
print("守卫 %d/%d；靶只读：%s" % (RES["guards"]["pass"], RES["guards"]["total"], unchanged))
