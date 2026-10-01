# -*- coding: utf-8 -*-
"""
tuft_htuft_blackhole_topology_v1.py
===================================
H-TUFT｜补充卷D（黑洞内部拓扑几何）**引擎核算与去重融合审计**

本脚本**不是**一个新预言的求解器，而是对补充卷D草稿 §11 引擎
（`torsion_repulsion / curvature_htuft / qnm_frequency_shift`）的**逐行复现 + 独立核算**，
并回答三个问题：
  Q1 草稿的「挠率拓扑斥力消除奇点」在自身公式下是否成立？
  Q2 草稿的 QNM 频移基线是否与已锚定的 Schwarzschild QNM 一致？
  Q3 草稿的「拓扑毛发 / 霍金拓扑修正」是否可观测、可证伪？

为何必须做本核算（去重融合的第一依据）：
  · 卷二十四《奇点消解与黑洞内禀几何》已于 2026-09-30 定稿并固化为 **CUR-08**，
    其主题（挠率正则黑洞、普朗克核心、QNM 频移、坍缩链路、霍金修正、信息悖论）
    与补充卷D草稿 §1~§4/§6~§8/§11 重叠；
  · CUR-03（ringdown 通道）真源为 **❌ 窗口已关闭**（OPEN_v3 χ²=33.00(df=2)、5.74σ），
    草稿 §6 把它写成「CUR-03 的核心预测正在等待检验」= **状态回退**（禁止）；
  · 故补充卷D 的正确处置是**去重融合**（真增量另计 CUR-16），而非新增一条重复条目。

判据：
  V1 曲率不变量恒等式自检（先在最确信的已知案例上验证公式，再用于新体系）
  V2 草稿引擎三处硬缺陷（负发散 / K≥0 不可相减 / 核心尺度非普朗克）
  V3 QNM 基线（复用 R25 Leaver 连分式真源，不重复实现）
  V4 α 与 Q_hel 双自由 ⇒ 可证伪力分析
  V5 与 Kerr 自旋的参数简并
  V6 检测阈值量级估计
  V7 霍金拓扑修正的可观测性
  V8 Birkhoff/唯一性定理 ⇒ 「拓扑毛发」的可观测性
  V9 χ²_BH 并入全局 MCMC 的一致性

红线：数学自洽 != 实验证实。本脚本**不新增物理主张**，只做核算与边界登记；
凡草稿结论不成立者直接记 FAIL，不粉饰。

依赖：Python 3.8（numpy / sympy）+ 同目录 `tuft_r25_leaver_qnm.py`（QNM 真源）。
"""

from __future__ import print_function

import hashlib
import importlib
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

OUT = os.path.join(HERE, "tuft_htuft_blackhole_topology_v1_report.txt")

# ────────────────────────────────────────────────────────────────────────────
# 草稿 §11 引擎的**逐行字面复现**（含其自身的 1e-6 正则化）
# ────────────────────────────────────────────────────────────────────────────
def draft_torsion_repulsion(r, alpha, Q_hel):
    """草稿 §11 torsion_repulsion：对 r 广播。"""
    tau = alpha * Q_hel / (np.asarray(r, dtype=float) ** 2 + 1e-6)
    return tau ** 2


def draft_curvature_htuft(r, M, alpha, Q_hel):
    """草稿 §11 curvature_htuft：返回 (raw, clipped)。raw 为去掉 jnp.maximum 的裸值。"""
    R_gr = 2.0 * M / (np.asarray(r, dtype=float) ** 3 + 1e-6)
    F = draft_torsion_repulsion(r, alpha, Q_hel)
    raw = R_gr - F
    return raw, np.maximum(raw, 0.0)


def draft_qnm_shift(M, alpha, Q_hel):
    """草稿 §11 qnm_frequency_shift。"""
    omega_gr = 1.0 / (M + 1e-6)
    d_omega = omega_gr * alpha * np.sqrt(Q_hel) / 100.0
    return omega_gr, omega_gr + d_omega


DRAFT_M = 10.0
DRAFT_ALPHA = 0.07
DRAFT_Q = 16.0

# 外部锚（[B] 级，用于量级判断；均标注来源类型）
L_PLANCK_M = 1.616255e-35          # CODATA 普朗克长度
M_SUN_KM = 1.476625                # 太阳质量对应的几何长度 G M_sun / c^2
M_SUN_KG = 1.98892e30
T_H_SUN_K = 6.169e-8               # T_H = 6.169e-8 K * (M_sun/M)
T_CMB_K = 2.72548
KERR_W220_A0 = complex(0.373672, -0.088962)     # l=m=2 基模（a=0，R25 真源）
KERR_W220_A09 = complex(0.532667, -0.080791)    # l=m=2 基模（a=0.9）[B] Berti-Cardoso-Starinets 综述量级

# ────────────────────────────────────────────────────────────────────────────
# 报告器
# ────────────────────────────────────────────────────────────────────────────
_lines = []
_CNT = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}


def P_(m):
    _CNT["PASS"] += 1
    _lines.append("[PASS] " + m)


def F_(m):
    _CNT["FAIL"] += 1
    _lines.append("[FAIL] " + m)


def B_(m):
    _CNT["BOUNDARY"] += 1
    _lines.append("[BOUNDARY] " + m)


def I_(m):
    _CNT["INFO"] += 1
    _lines.append("[INFO] " + m)


# ────────────────────────────────────────────────────────────────────────────
# V1 曲率不变量恒等式：先在最确信的已知案例上自检
# ────────────────────────────────────────────────────────────────────────────
def v1_curvature_identity():
    I_("§V1 曲率不变量恒等式自检（方法论：新体系推广前先在已知案例上验证公式）")
    r, M, g = sp.symbols("r M g", positive=True)

    # 静态球对称、g_tt g_rr = -1（Schwarzschild 与 Hayward 均满足）时，
    # 正交标架 Riemann 分量为 R_{t^r^t^r}=-f''/2、R_{t^th^t^th}=R_{r^th^r^th}=±f'/(2r)、
    # R_{th^ph^th^ph}=(1-f)/r^2 ⇒ K = (f'')^2 + 4(f'/r)^2 + 4(1-f)^2/r^4
    f = sp.symbols("f", cls=sp.Function)
    expr = sp.diff(f(r), r, 2) ** 2 + 4 * (sp.diff(f(r), r) / r) ** 2 + 4 * (1 - f(r)) ** 2 / r ** 4

    K_schw = sp.simplify(expr.subs(f(r), 1 - 2 * M / r))
    target = 48 * M ** 2 / r ** 6
    diff = sp.simplify(K_schw - target)
    I_("  解析式 K = (f'')² + 4(f'/r)² + 4(1-f)²/r⁴")
    I_("  自检（Schwarzschild f=1-2M/r）：K = %s（教科书值 48M²/r⁶）" % sp.sstr(sp.factor(K_schw)))
    if diff == 0:
        P_("V1 公式自检通过：Schwarzschild 下 K 与教科书 48M²/r⁶ **恒等**（差 = 0）"
           "⇒ 该式可用于 Hayward/正则解，不引入未核验的曲率公式")
        fam = True
    else:
        F_("V1 公式自检失败：Schwarzschild 下与 48M²/r⁶ 差 = %s" % sp.sstr(diff))
        fam = False

    # Hayward 正则解
    fH = 1 - 2 * M * r ** 2 / (r ** 3 + g ** 3)
    K_h = sp.simplify(expr.subs(f(r), fH))
    K0 = sp.limit(K_h, r, 0)
    I_("  Hayward 结构 f=1-2Mr²/(r³+g³)：K(0) = %s（有限）" % sp.sstr(sp.simplify(K0)))
    I_("  对照 Schwarzschild：K = 48M²/r⁶ 在 r→0 **发散**（∝ r⁻⁶）")
    K0_num = float(K0.subs({M: sp.Integer(1), g: sp.Rational(1, 2)}).evalf())
    schw_div = float((48 * M ** 2 / r ** 6).subs({M: sp.Integer(1), r: sp.Rational(1, 10000)}).evalf())
    I_("  数值对照：K_Hayward(0)|_(M=1,g=0.5) = %.4f（有限）；"
       "K_Schwarzschild(r=1e-4)|_(M=1) = %.4e（发散）" % (K0_num, schw_div))
    if fam and np.isfinite(K0_num) and schw_div > 1e10:
        P_("V1 正则性对照成立：Hayward K(0) 有限 = %s，Schwarzschild K→∞ ⇒ 正则解**由构造**无奇点"
           % sp.sstr(sp.simplify(K0)))
    else:
        F_("V1 正则性对照未通过（K0_num=%.4f, schw_div=%.4e）" % (K0_num, schw_div))
    return K0


# ────────────────────────────────────────────────────────────────────────────
# V2 草稿引擎三处硬缺陷
# ────────────────────────────────────────────────────────────────────────────
def v2_engine_defects(K0):
    I_("§V2 草稿 §11 引擎逐行复现（M=%.1f, alpha=%.2f, Q_hel=%.0f）" % (DRAFT_M, DRAFT_ALPHA, DRAFT_Q))

    r_list = [0.01, 0.1, 0.5, 1.0, 2.0, 5.0]
    I_("   r        R_gr         F_topo       R_ht(raw)     R_ht(clip)")
    for rv in r_list:
        raw, clip = draft_curvature_htuft(rv, DRAFT_M, DRAFT_ALPHA, DRAFT_Q)
        I_("   %-8.2f %-12.4e %-12.4e %-13.4e %-12.4e" % (rv, 2.0 * DRAFT_M / rv ** 3,
                                                          float(draft_torsion_repulsion(rv, DRAFT_ALPHA, DRAFT_Q)),
                                                          float(raw), float(clip)))

    # (a) 「曲率不再发散」的来源分解：逐层剥离代码技巧
    r_core = DRAFT_ALPHA ** 2 * DRAFT_Q ** 2 / (2.0 * DRAFT_M)
    I_("   (a1) 草稿字面版（含其自身 1e-6 正则化）在 0.01<r<r_core=%.5f 的裸值：" % r_core)
    I_("        r         R_gr(字面)     F_topo(字面)    raw(去 clip)")
    for rv in [0.05, 0.03, 0.02, 0.015, 0.0125]:
        raw, _c = draft_curvature_htuft(rv, DRAFT_M, DRAFT_ALPHA, DRAFT_Q)
        I_("        %-9.4f %-13.4e %-15.4e %-14.4e"
           % (rv, 2.0 * DRAFT_M / (rv ** 3 + 1e-6),
              float(draft_torsion_repulsion(rv, DRAFT_ALPHA, DRAFT_Q)), float(raw)))
    rawA = float(draft_curvature_htuft(0.0125, DRAFT_M, DRAFT_ALPHA, DRAFT_Q)[0])
    rawB = float(draft_curvature_htuft(0.02, DRAFT_M, DRAFT_ALPHA, DRAFT_Q)[0])
    I_("        标度检验：|raw(0.0125)|/|raw(0.02)| = %.2f（−r⁻⁴ 预期 6.55；−r⁻³ 预期 1.60）"
       % (abs(rawA) / abs(rawB)))

    I_("   (a2) 解析版（令草稿自身的 1e-6 → 0）：raw(r) = 2M/r³ − α²Q²/r⁴")
    for rv in [0.05, 0.02, 0.01, 5e-3, 1e-3]:
        I_("        r=%-9.5f raw_ana=%-14.4e"
           % (rv, 2.0 * DRAFT_M / rv ** 3 - DRAFT_ALPHA ** 2 * DRAFT_Q ** 2 / rv ** 4))
    ana1 = 2.0 * DRAFT_M / 0.01 ** 3 - DRAFT_ALPHA ** 2 * DRAFT_Q ** 2 / 0.01 ** 4
    ana2 = 2.0 * DRAFT_M / 5e-3 ** 3 - DRAFT_ALPHA ** 2 * DRAFT_Q ** 2 / 5e-3 ** 4
    I_("        标度检验：|raw_ana(5e-3)|/|raw_ana(1e-2)| = %.2f（−r⁻⁴ 预期 16.0）"
       % (abs(ana2) / abs(ana1)))

    I_("   (a3) 字面版在 r≤1e-3 处**被 ε 截断**（非物理饱和）：")
    for rv in [1e-3, 1e-4, 1e-5]:
        raw, _c = draft_curvature_htuft(rv, DRAFT_M, DRAFT_ALPHA, DRAFT_Q)
        I_("        r=%-8.0e R_gr=%-12.4e（饱和于 2M/1e-6=%.3e）  F_topo=%-12.4e（饱和于 (αQ/1e-6)²=%.3e）"
           % (rv, 2.0 * DRAFT_M / (rv ** 3 + 1e-6), 2.0 * DRAFT_M / 1e-6,
              float(draft_torsion_repulsion(rv, DRAFT_ALPHA, DRAFT_Q)),
              (DRAFT_ALPHA * DRAFT_Q / 1e-6) ** 2))

    F_("V2a 『挠率拓扑压制曲率发散，奇点消解』**不成立（三重剥离）**："
       "①去掉 jnp.maximum 后 raw = 2M/r³ − α²Q²/r⁴ 在 r<r_core=%.5f 处 **∝ −r⁻⁴ 负向发散**"
       "（a2 解析版标度检验 17.52 vs −r⁻⁴ 预期 16.0；a1 字面版 7.88，介于 −r⁻⁴ 的 6.55 与 −r⁻³ 的 1.60 之间、"
       "因 −r⁻³ 项混合而偏向 −r⁻⁴）；②草稿自身的 1e-6 正则化只是把发散**截断在 ε 尺度**"
       "（a3：r≤1e-3 时 R_gr 与 F_topo 双双饱和为常数），属代码正则化而非物理机制；"
       "③保留 clip 则曲率被硬置零（见 V2b）。⇒『曲率不再发散』完全由 max(·,0) 与 ε 两个"
       "**代码技巧**实现 = 把结论写进代码（与卷二十四 §0-2 已判定的 deus ex machina 同型）" % r_core)

    # (b) K >= 0 恒等式 ⇒ 不可「相减」
    r_probe = r_core / 2.0
    I_("   平衡半径 r_core = α²Q²/(2M) = %.6f；clip 后 r<r_core 区段 R_ht≡0" % r_core)
    I_("   r<r_core（如 r=%.5f）处草稿判为『曲率=0』，而真实不变量 K=48m(r)²/r⁶ 在该处 > 0" % r_probe)
    K_num = float(48 * DRAFT_M ** 2 / r_probe ** 6)
    I_("   该处 Schwarzschild 型 K ≈ 48M²/r⁶ = %.3e > 0（任意正交标架下 K=ΣR² 恒 ≥ 0）" % K_num)
    F_("V2b 曲率不变量**不可相减**：K = R_{μνρσ}R^{μνρσ} 是 Riemann 分量的**平方和**，"
       "逐点恒 ≥ 0 且 K=0 ⟺ 局部平坦。草稿把『挠率应力』与曲率标量直接相减并 clip 到 0，"
       "等价于宣称 r<r_core 区段**局部平坦却仍含一个带质量的核心** ⇒ 与场方程矛盾；"
       "且 max(·,0) 在 r_core 处使 R 的一阶导数跳变（C⁰ 折角，非 C¹）⇒ 不是任何光滑解")

    # (c) 「普朗克尺度核心」不自洽
    I_("   核心尺度对 M 的依赖：r_core(M) = α²Q²/(2M)")
    for Mv in [10.0, 1.0e3, 1.0e6]:
        I_("     M=%-9.0f -> r_core=%.6e（几何单位）" % (Mv, DRAFT_ALPHA ** 2 * DRAFT_Q ** 2 / (2.0 * Mv)))
    M_phys_km = 10.0 * M_SUN_KM
    r_phys_m = DRAFT_ALPHA ** 2 * DRAFT_Q ** 2 / (2.0 * M_phys_km) * 1.0e3
    orders = np.log10(r_phys_m / L_PLANCK_M)
    I_("   物理单位核算（取 M=10 M_sun = %.4f km，alpha=0.07，Q_hel=16）：" % M_phys_km)
    I_("     r_core = %.4f m ；l_Planck = %.4e m ；相差 %.1f 个量级"
       % (r_phys_m, L_PLANCK_M, orders))
    F_("V2c 『中心…特征尺度为普朗克尺度量级』**与草稿自身公式不相容**："
       "r_core = α²Q²/(2M) ∝ 1/M 随黑洞质量变化，而普朗克尺度是与 M 无关的普适常数；"
       "按草稿参数在物理单位下 r_core≈%.1f m（10 M_sun），与 l_P 差 **%.1f 个量级**"
       % (r_phys_m, orders))

    # (d) 「曲率=2M/r³」不是不变量
    I_("   草稿 R_gr=2M/r³ 与真不变量的标度差异：K_Schw/R_gr = (48M²/r⁶)/(2M/r³) = 24M/r³")
    for rv in [1.0, 1e-1, 1e-3]:
        I_("     r=%-7.0e -> K/R_gr = %.3e" % (rv, 24.0 * DRAFT_M / rv ** 3))
    F_("V2d 草稿的『曲率』R_gr=2M/r³ **不是曲率不变量**（且真空 Schwarzschild 的 Ricci 标量 R≡0）："
       "真不变量 K∝r⁻⁶，草稿量 ∝r⁻³ ⇒ 连发散阶数都低估；把它与一个应力张量分量的平方相减无几何意义")


# ────────────────────────────────────────────────────────────────────────────
# V3 QNM 基线（复用 R25 Leaver 真源）
# ────────────────────────────────────────────────────────────────────────────
def v3_qnm_baseline():
    I_("§V3 QNM 基线核算（复用 R25 `tuft_r25_leaver_qnm.py` 的 Leaver 连分式真源，不重复实现）")
    try:
        r25 = importlib.import_module("tuft_r25_leaver_qnm")
    except Exception as exc:  # pragma: no cover
        F_("V3 无法导入 R25 QNM 真源（%s）⇒ QNM 基线核算不可执行，**不产出替代数值**" % exc)
        return None, None
    t0 = time.time()
    w0 = r25.find_root(complex(0.373672, -0.088962), N=4000)
    w1 = r25.find_root(complex(0.346711, -0.273915), N=4000)
    I_("   l=2 n=0：ωM = %.12f%+.12fi（|f|=%.2e，耗时 %.1fs）"
       % (w0.real, w0.imag, abs(r25.f_leaver(w0, 4000)), time.time() - t0))
    I_("   l=2 n=1：ωM = %.12f%+.12fi（|f|=%.2e）"
       % (w1.real, w1.imag, abs(r25.f_leaver(w1, 4000))))
    # M 标度：ω = (ωM)/M，取草稿的 M=10
    w_phys_true = w0 / DRAFT_M
    I_("   按草稿 M=%.1f 标度：真实 ω_gr = %.9f%+.9fi" % (DRAFT_M, w_phys_true.real, w_phys_true.imag))

    om_gr_draft, om_ht_draft = draft_qnm_shift(DRAFT_M, DRAFT_ALPHA, DRAFT_Q)
    I_("   草稿 ω_gr = 1/M = %.6f（实部，无虚部）" % om_gr_draft)
    ratio = om_gr_draft / w_phys_true.real
    I_("   比值 草稿/真值 = %.6f（即草稿基线高出 %.2f%%）" % (ratio, (ratio - 1.0) * 100.0))
    if abs(ratio - 1.0) > 1e-3:
        F_("V3a 草稿 QNM 基线 ω_gr=1/M **错误 %.4f 倍**：真实 l=2 基模 ωM=0.373671684（R25 Leaver，"
           "与文献 0.373672 一致至 1e-7），而 1/M 对应 ωM=1 ⇒ 起草稿的『频移』前基线即偏 %.1f%%"
           % (ratio, (ratio - 1.0) * 100.0))

    # 草稿自己的 χ²_BH（按字面）
    rel_err = (om_ht_draft - w_phys_true.real) / w_phys_true.real
    sigma_rel = 0.01
    chi2 = (rel_err / sigma_rel) ** 2
    I_("   草稿 ω_ht = %.8f ⇒ 相对真实 QNM 偏差 = %+.4f (%+.1f%%)" % (om_ht_draft, rel_err, rel_err * 100.0))
    I_("   代入草稿自己的 χ²_BH = ((ω_pred-ω_obs)/σ_ω)²，取 σ_ω/ω=1%%：χ²_BH = %.3e" % chi2)
    F_("V3b 草稿引擎**按字面已被自身的似然项排除**：χ²_BH = %.3e（σ_ω/ω=1%%）⇒ p≈0；"
       "即 §8 的 χ²_BH 若与 §11 的 ω_pred 配套使用，模型在第一个事件上即自我排除" % chi2)
    return w0, w1


# ────────────────────────────────────────────────────────────────────────────
# V4 可证伪力：α 与 Q_hel 双自由
# ────────────────────────────────────────────────────────────────────────────
def v4_falsifiability():
    I_("§V4 可证伪力分析：δω/ω = α·sqrt(Q_hel)/100 中 α 与 Q_hel 的可约束性")
    I_("   卷二十八/补充卷A 取 α=0.07（但为**自由参量**，卷二十九 T5/H7）；Q_hel 在草稿中亦未固定")
    I_("   目标频移 δω/ω      需要 alpha（Q_hel=16）  需要 Q_hel（alpha=0.07）")
    rows = []
    for target in [1e-4, 1e-3, 2.8e-3, 1e-2, 5e-2, 1e-1]:
        a_req = target * 100.0 / np.sqrt(DRAFT_Q)
        q_req = (target * 100.0 / DRAFT_ALPHA) ** 2
        rows.append((target, a_req, q_req))
        I_("   %-18.1e %-24.4f %-22.3e" % (target, a_req, q_req))
    span = rows[-1][1] / rows[0][1]
    I_("   需 alpha 跨度 = %.1f 倍（全部落在 (0,1) 的『看起来合理』区间内）" % span)
    F_("V4 第 1 层：α 与 Q_hel **两参数自由** ⇒ 单方程 δω/ω=α√Q/100 对任意观测频移都能反解出参数组合 "
       "⇒ **无可证伪力**（与卷二十九 T5『质量公式 3 自由系数』同型结构弱点）")
    # 第 2 层：若把 alpha 固定为卷二十八/补充卷A 的 0.07，Q_hel 仍自由
    q_for = lambda t: (t * 100.0 / DRAFT_ALPHA) ** 2
    I_("   若**固定** alpha=0.07（承卷二十八/补充卷A），则 Q_hel 需为：")
    for target in [1e-3, 2.8e-3, 1e-2]:
        I_("     目标 δω/ω=%.1e -> Q_hel=%.4g" % (target, q_for(target)))
    I_("   草稿示例取 Q_hel=16 ⇒ δω/ω=%.6g（唯一定值）" % (DRAFT_ALPHA * np.sqrt(DRAFT_Q) / 100.0))
    B_("V4 第 2 层：若**额外固定 α=0.07 且 Q_hel=16**，则 δω/ω=2.8e-3 成为**唯一定值**、原则上可检验；"
       "但 Q_hel=16 是草稿随手给定的，黑洞的 Q_hel 无独立测定手段（见 V8）⇒ 可证伪性依赖一个不可独立测量的参数")


# ────────────────────────────────────────────────────────────────────────────
# V5 与 Kerr 自旋的参数简并
# ────────────────────────────────────────────────────────────────────────────
def v5_spin_degeneracy():
    I_("§V5 与 Kerr 自旋 a 的参数简并（[B] 外部锚：Berti-Cardoso-Starinets 综述量级）")
    dw_da = (KERR_W220_A09.real - KERR_W220_A0.real) / 0.9
    I_("   dω_R/da ≈ (%.6f - %.6f)/0.9 = %.4f（每个单位自旋）" % (
        KERR_W220_A09.real, KERR_W220_A0.real, dw_da))
    target = DRAFT_ALPHA * np.sqrt(DRAFT_Q) / 100.0
    da_needed = target * KERR_W220_A0.real / dw_da
    I_("   产生 δω/ω=%.4e 所需自旋偏移 Δa ≈ %.4f" % (target, da_needed))
    I_("   典型并合末态自旋测量不确定度 σ_a ~ 0.1~0.2（GW 事件量级）[B]")
    F_("V5 该可观测**与自旋参数完全简并**：所需 Δa=%.4f ≪ σ_a~0.1~0.2 ⇒ 观测到的频移可被自旋不确定性"
       "完全吸收，无法归因于 Q_hel；除非用旋进相位独立固定 (M,a)，而这会引入自身的系统性" % da_needed)


# ────────────────────────────────────────────────────────────────────────────
# V6 检测阈值量级估计
# ────────────────────────────────────────────────────────────────────────────
def v6_detection_threshold():
    I_("§V6 检测阈值量级估计（[B] 级：单事件精度取 1% 为代表性量级，非严格 forecast）")
    target = DRAFT_ALPHA * np.sqrt(DRAFT_Q) / 100.0
    sigma1 = 0.01
    need_sigma = target / 3.0
    N = (sigma1 / need_sigma) ** 2
    I_("   目标频移 δ=%.3e；单事件 σ_ω/ω=1e-2；3σ 分辨需 σ_N≤%.3e" % (target, need_sigma))
    I_("   独立事件数 N ≈ (σ_1/σ_N)² ≈ %.0f 个高信噪比 ringdown 事件" % N)
    P_("V6 量级估计完成：δ=2.8e-3 的频移需 **N≈%.0f** 个高信噪比 ringdown 事件方可 3σ 分辨"
       "⇒ 在下一代探测器（ET/CE，O(1e4) 事件/年但 ringdown 信噪比受限）下**原则上可及**（十年量级）" % N)
    B_("V6 边界：该估计把 (M,a) 视为已知（否则见 V5 简并）、假设系统性误差已被控制、"
       "且 sigma_1=1%% 为代表性量级而非来自具体事件的实测误差" % ())


# ────────────────────────────────────────────────────────────────────────────
# V7 霍金拓扑修正
# ────────────────────────────────────────────────────────────────────────────
def v7_hawking():
    I_("§V7 霍金辐射拓扑修正的可观测性（草稿 §7『辐射谱存在微小偏离黑体谱的拓扑修正项』）")
    M = 10.0
    T_H = T_H_SUN_K / M
    I_("   M=10 M_sun 时 T_H = %.6e K（对照 CMB %.3f K）" % (T_H, T_CMB_K))
    delta_T = 1.2e-10      # 卷二十四 §8 所记 T_B = 1.2e-10·g3_ir 的量级
    dT = T_H * delta_T
    I_("   若 δ_T ~ 1.2e-10（卷二十四 §8 的 T_B 量级）⇒ ΔT = %.3e K" % dT)
    I_("   ΔT/T_CMB = %.3e；对比宇宙微波背景温度测量精度 ~1e-4 量级" % (dT / T_CMB_K))
    F_("V7a 该修正**不可观测**：ΔT≈%.1e K，与 CMB 温度（2.7 K）相差 ~%.0f 个量级；"
       "且黑洞霍金温度本身远低于 CMB（10 M_sun：%.1e K vs 2.7 K）⇒ 蒸发在宇宙学上被抑制，"
       "蒸发末期『拓扑孤子释放』时间尺度 ~1e67·(M/M_sun)³ yr 亦不可检验" % (dT, np.log10(T_CMB_K / abs(dT)), T_H))
    F_("V7b **与质量重标度简并**：若 T_H^TUFT = T_H^GR(1+δ_T) 且 δ_T 为常数/低频，"
       "则以 GR 拟合时 M_fit = M/(1+δ_T) ⇒ 任何 δ_T 均被质量重新标定吸收，"
       "无独立可检验性；草稿称『偏离黑体谱』却未给谱函数 ⇒ 不可证伪")


# ────────────────────────────────────────────────────────────────────────────
# V8 Birkhoff / 唯一性 ⇒ 拓扑毛发的可观测性
# ────────────────────────────────────────────────────────────────────────────
def v8_hair():
    I_("§V8 『黑洞拓扑毛发 Q_hel』的可观测性（草稿 §5）")
    I_("   草稿主张：Q_hel 为丛同伦不变量、低能连续形变不能抹除、外部只能通过 ringdown 间接读取")
    P_("V8a 前半可判：同伦类在光滑形变下守恒 = **定义性真理**（tautology）"
       "⇒ 本身不构成物理预言、不构成可证伪内容")
    F_("V8b 后半**被定理禁止**：球对称真空情形 Birkhoff 定理 ⇒ 外部几何唯一为 Schwarzschild；"
       "旋转情形 Carter-Robinson 唯一性 ⇒ 外部唯一为 Kerr。两者均**不含任何内部拓扑信息** ⇒ "
       "『拓扑毛发』在标准 EC/GR 场方程下**不可能在外部几何留下印记**")
    F_("V8c 逃脱定理的唯一途径 = 引入**长程挠率场**使外部非真空（非最小耦合），"
       "但：①该耦合在 TUFT 中是写入项而非变分导出（卷二十四 §2 已判定）；"
       "②任何新的长程场等价于**第五力**，受 Eötvös/Cassini/LLR 等约束；"
       "③TUFT 自身挠率宏观不可用（R6：与所需尺度差 1e28）⇒ 该途径当前无候选机制")
    I_("   推论：草稿 §6『内部拓扑核振荡 ⇒ ringdown 频移』缺乏传播机制——"
       "内部振荡若无长程耦合，无法改变外部 QNM 谱")


# ────────────────────────────────────────────────────────────────────────────
# V9 χ²_BH 与全局 MCMC 一致性
# ────────────────────────────────────────────────────────────────────────────
def v9_mcmc():
    I_("§V9 χ²_BH 并入全局 MCMC 的一致性（对接 CUR-07 / CUR-13）")
    I_("   卷二十三（CUR-07）：8 通道分类 EDM/g2/ringdown=CLOSED（logL ≡ -inf）、ns/r=OPEN、"
       "CKM/PMNS/f_NL=UNVALIDATED ⇒ 全联合 Z=0（严格）")
    I_("   卷三十（CUR-13）：H-TUFT 全局 MCMC 同样得 Z=0，lnB(H-TUFT/ΛCDM) = -∞")
    P_("V9a 形式化论证成立：Z = ∫ exp(-χ²_tot/2) dθ；任一新通道只把被积函数乘以 "
       "exp(-χ²_BH/2) ≤ 1 ⇒ **不可能增大 Z**；若已有 CLOSED 通道使被积函数恒 0，"
       "则 Z 仍恒为 0 ⇒ χ²_BH **无法救回**全局拟合")
    I_("   若把 §8 的 χ²_BH 视为**替换** ringdown 通道（而非新增），则属 CUR-03 的重标号，"
       "而 CUR-03 真源为 ❌（χ²=33.00(df=2)、5.74σ）⇒ 需重新论证，不得直接声明为『新通道』")
    F_("V9b 草稿 §8 称『Q_hel 同时作为黑洞拓扑荷与暗物质孤子拓扑荷，实现跨现象统一』"
       "——但补充卷A（CUR-14）已实跑证明其暗物质丰度公式**量纲反、Ω_DM 差 ~25 量级**；"
       "把一个**已失败**通道的参数用于『跨现象统一』，属把失败当作支持（regression）")


# ────────────────────────────────────────────────────────────────────────────
def main():
    t_start = time.time()
    _lines.append("=" * 74)
    _lines.append("H-TUFT 补充卷D · 黑洞内部拓扑几何：引擎核算与去重融合审计")
    _lines.append("=" * 74)
    I_("几何单位 G=c=1；草稿参数 M=%.1f, alpha=%.2f, Q_hel=%.0f" % (DRAFT_M, DRAFT_ALPHA, DRAFT_Q))
    I_("本脚本对草稿 §11 引擎逐行复现（含其 1e-6 正则化），不替换、不修饰")

    K0 = v1_curvature_identity()
    v2_engine_defects(K0)
    v3_qnm_baseline()
    v4_falsifiability()
    v5_spin_degeneracy()
    v6_detection_threshold()
    v7_hawking()
    v8_hair()
    v9_mcmc()

    I_("§结论摘要")
    I_("   ① 正则黑洞（曲率有界、无中心奇点）作为**已知数学结构**成立（V1 PASS），"
       "但其正确归因是 Hayward 类正则结构，**非**草稿 §11 的 max(·,0) 引擎；")
    I_("   ② 草稿 §11 三处硬缺陷：负发散（V2a）、K≥0 恒等式不可相减（V2b）、"
       "核心尺度非普朗克（V2c）；")
    I_("   ③ QNM 基线错 %.4f 倍，草稿自带 χ²_BH≈2.8e4 ⇒ 按字面自我排除（V3）；"
       % (1.0 / KERR_W220_A0.real))
    I_("   ④ 『拓扑毛发』被 Birkhoff/唯一性定理禁止，除非引入未导出的长程挠率场（V8）；")
    I_("   ⑤ χ²_BH 不能救回 Z=0（V9）。")

    B_("边界①：仅球对称/非旋转 Schwarzschild 基线与 Hayward 正则结构；Kerr 未并入本核算。")
    B_("边界②：V5/V6 的自旋误差与单事件精度取 [B] 级代表性量级，非具体事件实测值。")
    B_("边界③：V6 的 N≈116 仅为量级估计，未做探测器响应/选择效应的完整 forecast。")
    B_("边界④：V7 的 δ_T~1.2e-10 取自卷二十四 §8 所记 T_B 量级；TUFT 未给 δ_T 的谱函数。")
    B_("边界⑤：本脚本不评估『挠率＝几何自由度』这一公理层设定本身，只核算其可检验推论。")
    B_("边界⑥：红线——数学自洽 != 实验证实。V1 的 PASS 只证明所用曲率公式正确，"
       "不构成对 H-TUFT 的任何经验支持。")

    _lines.append("-" * 74)
    _lines.append("PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d"
                  % (_CNT["PASS"], _CNT["FAIL"], _CNT["BOUNDARY"], _CNT["INFO"]))
    _lines.append("-" * 74)
    _lines.append("评级：C / L2（草稿引擎的『奇点消解』与『QNM 频移』在自身公式下不成立，"
                  "属结构性缺陷；正则黑洞结构本身成立但归因不同）")
    _lines.append("红线：数学自洽 != 实验证实；本册为核算与去重审计，不新增物理主张。")

    text = "\n".join(_lines) + "\n"
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    # 脚本自哈希（写盘后计算，供 CURATED 固化核对）
    with open(os.path.abspath(__file__), "rb") as fh:
        self_sha = hashlib.sha256(fh.read()).hexdigest()
    text2 = text + "自哈希(SHA256) = %s\n耗时 = %.1fs\n" % (self_sha, time.time() - t_start)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text2)
    print(text2)
    return _CNT


if __name__ == "__main__":
    main()
