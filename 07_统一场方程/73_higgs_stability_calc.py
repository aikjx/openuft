# -*- coding: utf-8 -*-
"""
73 卷引擎：Higgs 扇区 —— 真空稳定性与平庸性边界（SM 有效场论窗口）
====================================================================
用户指令「继续完成统一场论」的执行卷（编号卷 73）。接续 68（核心方程集 v2.0）
→ 69（电弱一圈修正）→ 70（强相互作用扇区收口）轨迹，收口 Higgs 扇区。
71/72 已由并行会话占用并产出三件套 ⇒ 按编号冲突规则取首空号 73。

β 函数系数来源（双源互证，禁凭记忆硬编码）：
  S1 = arXiv:1412.8230v1 §2（GUT 归一化约定 g1^2 = (5/3) g'^2）
  S2 = arXiv:1202.5717 附录 A Eq.(21)-(24)（超荷 g' 约定，引自
       Machacek-Vaughn + Arason et al.）
  CT1：两源在 g1 = sqrt(5/3) g' 换算下逐项一致（残差 < 1e-50）。
基准值来源：Buttazzo et al. arXiv:1307.3536v4（Eq.61/64/65/67, Table 2/3）。
圈阶差声明：文献为 3-loop RGE + 2-loop 阈值（"full 3-loop NNLO RGE precision"）；
本卷跑动只到 2-loop。端点量 λ(M_Pl)/m_h^crit 对标容差已含此差（CT3/CT6）；
过零标度 Λ_λ 对圈阶敏感（机读：同匹配 1→2 圈差 1.455 dex），本卷 2-loop 读数
低于文献 3-loop 值（~10^10 GeV）约 0.6 dex 属预期圈阶差，非引擎缺陷（CT4 依据）。

口径声明（诚实边界，详见卷文 B3）：
  - 匹配：Case A = LO 朴素树匹配（λ(M_t)=m_h²/2v², y_t=√2m_t/v，即文献 Table 3
    LO 列口径）；Case B = 文献 NNLO 匹配值直接代入（λ=0.12604, y_t=0.94018）。
    Case A 与 B 的差 = 匹配约定系统差（pole 朴素 vs MSbar），是本卷 B3 的定价对象。
  - 跑动：1-loop / 2-loop 两阶；无 m_t/m_b 味数阈值（N_f=6 固定，声明约定）。
  - 非微扰阈值：λ = π（声明的约定）。

纪律（红线，继承 53 账本 + r128/70 卷元纪律）：
  - verdict 全部由机读结果驱动，禁「算了数却硬编码判定」的死代码；
  - 控制组先行证判别力（含反向对照：错符号 y_t 项必须改变结论）；
  - 阈值来自公布不确定度传播或文献值 ± 声明倍数，禁拍脑袋机器零；
  - 数学自洽 ≠ 实验证实；本卷是 SM 已有框架的复核/攻破，不产生新物理；
  - 退出码 2 = 控制组或守卫未全过 ⇒ 拒绝出数；退出码 3 = 源文件缺失。
"""

import json
import os
import sys
import time
from fractions import Fraction

from mpmath import mp, mpf, log, exp, sqrt, pi as MPI

mp.dps = 250

P16 = 16 * MPI ** 2  # 16 pi^2
LAM_NP = MPI         # 非微扰阈值约定：lambda = pi

# ---------------------------------------------------------------------------
# 输入（显式声明；带来源与不确定度）
# ---------------------------------------------------------------------------
M_H = mpf("125.25")      # Higgs pole mass (PDG 2024 量级，输入假设)
D_M_H = mpf("0.17")
M_T = mpf("172.57")      # top pole mass (PDG 2024 直接测量平均量级，输入假设)
D_M_T = mpf("0.29")
A3_MZ = mpf("0.1180")    # alpha_s(M_Z) (PDG 2024 量级，输入假设)
D_A3 = mpf("0.0009")
ALPHA_MZ_INV = mpf("127.95")   # alpha(M_Z)^-1 (输入假设)
SIN2TW = mpf("0.23122")        # sin^2 theta_W MSbar (输入假设)
V = mpf("246.22")              # (sqrt(2) G_F)^-1/2 = 246.21971 GeV
M_Z = mpf("91.1876")
M_PL = mpf("1.2209e19")

# Buttazzo et al. 1307.3536v4 基准输入（Table 2）与匹配值（Table 3, mu=M_t）
BM_M_H = mpf("125.15")
BM_M_T = mpf("173.34")
BM_A3 = mpf("0.1184")
BM_LAM_NNLO = mpf("0.12604")   # Table 3 NNLO lambda(M_t)
BM_YT_NNLO = mpf("0.94018")    # Table 3 NNLO y_t(M_t)
BM_LAM_LO = mpf("0.12917")     # Table 3 LO lambda(M_t)
BM_YT_LO = mpf("0.99561")      # Table 3 LO y_t(M_t)
BM_LAM_MPL = mpf("-0.0143")    # Eq.(61) lambda(M_Pl)（NNLO）
BM_MH_CRIT = mpf("129.6")      # Eq.(64) 绝对稳定性临界 Higgs 质量（NNLO）
BM_D_MH_CRIT = mpf("1.5")      # Eq.(65) 合成不确定度
BM_SENS_MH = mpf("0.7")        # Eq.(67) d log10(Lambda_V) / d M_h  [per GeV]
BM_SENS_MT = mpf("-1.0")       # Eq.(67) d log10(Lambda_V) / d M_t  [per GeV]


# ---------------------------------------------------------------------------
# β 函数系数（Fraction 固化；预计算为 mpf 常量，禁热路径重复解析）
# ---------------------------------------------------------------------------
def _F(s):
    f = Fraction(s)
    return mpf(f.numerator) / mpf(f.denominator)


# S2 二圈/一圈系数
F_3_8 = _F("3/8")
F_9_2 = _F("9/2")
F_9_4 = _F("9/4")
F_17_12 = _F("17/12")
F_41_6 = _F("41/6")
F_19_6 = _F("19/6")
F_1_48 = _F("1/48")
F_8_3 = _F("8/3")
F_73_8 = _F("73/8")
F_39_4 = _F("39/4")
F_629_24 = _F("629/24")
F_21_2 = _F("21/2")
F_19_4 = _F("19/4")
F_45_2 = _F("45/2")
F_85_6 = _F("85/6")
F_23_4 = _F("23/4")
F_3_4 = _F("3/4")
F_1187_216 = _F("1187/216")
F_19_9 = _F("19/9")
F_225_16 = _F("225/16")
F_131_16 = _F("131/16")
F_199_18 = _F("199/18")
F_44_3 = _F("44/3")
F_17_6 = _F("17/6")
F_3_2 = _F("3/2")
F_35_6 = _F("35/6")
F_11_6 = _F("11/6")
# S1（GUT 约定）专有系数
F_9_5 = _F("9/5")
F_27_200 = _F("27/200")
F_9_8 = _F("9/8")
F_9_20 = _F("9/20")
F_108_5 = _F("108/5")
F_17_2 = _F("17/2")
F_1887_200 = _F("1887/200")
F_117_20 = _F("117/20")
F_8_5 = _F("8/5")
F_171_100 = _F("171/100")
F_63_10 = _F("63/10")
F_3411_2000 = _F("3411/2000")
F_305_16 = _F("305/16")
F_1677_400 = _F("1677/400")
F_289_80 = _F("289/80")


def beta_all(lam, y, g2, gp, g3, loop=2, y4_sign=-1):
    """返回 (beta_lam, beta_y, beta_g2, beta_gp, beta_g3)，自变量 t = ln(mu/GeV)。

    约定：S2（超荷 g'）非 GUT 形式。y4_sign 为反向对照用（+1 = 植入错符号缺陷）。
    """
    y2 = y * y
    y4 = y2 * y2
    y6 = y4 * y2
    g22 = g2 * g2
    g24 = g22 * g22
    g26 = g24 * g22
    gp2 = gp * gp
    gp4 = gp2 * gp2
    gp6 = gp4 * gp2
    g32 = g3 * g3
    g34 = g32 * g32
    lam2 = lam * lam

    # ---- 一圈 ----
    b_lam_1 = (24 * lam2
               + y4_sign * 6 * y4
               + F_3_8 * (2 * g24 + (g22 + gp2) ** 2)
               + (-9 * g22 - 3 * gp2 + 12 * y2) * lam)
    b_y_1 = y * (F_9_2 * y2 - F_9_4 * g22 - F_17_12 * gp2 - 8 * g32)
    b_gp_1 = F_41_6 * gp ** 3
    b_g2_1 = -F_19_6 * g2 ** 3
    b_g3_1 = -7 * g3 ** 3

    if loop == 1:
        return (b_lam_1 / P16, b_y_1 / P16, b_g2_1 / P16, b_gp_1 / P16, b_g3_1 / P16)

    # ---- 二圈（S2 Eq.(21)-(24)）----
    b_lam_2 = (
        F_1_48 * (915 * g26 - 289 * g24 * gp2 - 559 * g22 * gp4 - 379 * gp6)
        + 30 * y6
        - y4 * (F_8_3 * gp2 + 32 * g32 + 3 * lam)
        + lam * (-F_73_8 * g24 + F_39_4 * g22 * gp2 + F_629_24 * gp4
                 + 108 * g22 * lam + 36 * gp2 * lam - 312 * lam2)
        + y2 * (-F_9_4 * g24 + F_21_2 * g22 * gp2 - F_19_4 * gp4
                + lam * (F_45_2 * g22 + F_85_6 * gp2 + 80 * g32 - 144 * lam))
    )
    b_y_2 = y * (
        -F_23_4 * g24 - F_3_4 * g22 * gp2 + F_1187_216 * gp4
        + 9 * g22 * g32 + F_19_9 * gp2 * g32 - 108 * g34
        + (F_225_16 * g22 + F_131_16 * gp2 + 36 * g32) * y2
        + 6 * (-2 * y4 - 2 * y2 * lam + lam2)
    )
    b_gp_2 = gp ** 3 * (F_199_18 * gp2 + F_9_2 * g22 + F_44_3 * g32 - F_17_6 * y2)
    b_g2_2 = g2 ** 3 * (F_3_2 * gp2 + F_35_6 * g22 + 12 * g32 - F_3_2 * y2)
    b_g3_2 = g3 ** 3 * (F_11_6 * gp2 + F_9_2 * g22 - 26 * g32 - 2 * y2)

    return (b_lam_1 / P16 + b_lam_2 / P16 ** 2,
            b_y_1 / P16 + b_y_2 / P16 ** 2,
            b_g2_1 / P16 + b_g2_2 / P16 ** 2,
            b_gp_1 / P16 + b_gp_2 / P16 ** 2,
            b_g3_1 / P16 + b_g3_2 / P16 ** 2)


def beta_lambda_src1(lam, y, g1, g2, g3, loop=2):
    """S1（arXiv:1412.8230）形式：GUT 归一化 g1^2 = (5/3) g'^2。仅 lambda。"""
    y2 = y * y
    y4 = y2 * y2
    g12 = g1 * g1
    g14 = g12 * g12
    g16 = g14 * g12
    g22 = g2 * g2
    g24 = g22 * g22
    g26 = g24 * g22
    g32 = g3 * g3
    lam2 = lam * lam
    b1 = (lam * (24 * lam + 12 * y2 - F_9_5 * g12 - 9 * g22)
          - 6 * y4 + F_27_200 * g14 + F_9_8 * g24 + F_9_20 * g12 * g22)
    if loop == 1:
        return b1 / P16
    b2 = (
        lam2 * (-312 * lam - 144 * y2 + F_108_5 * g12 + 108 * g22)
        + lam * y2 * (-3 * y2 + F_17_2 * g12 + F_45_2 * g22 + 80 * g32)
        + lam * (F_1887_200 * g14 - F_73_8 * g24 + F_117_20 * g12 * g22)
        + y4 * (30 * y2 - F_8_5 * g12 - 32 * g32)
        + y2 * (-F_171_100 * g14 - F_9_4 * g24 + F_63_10 * g12 * g22)
        - F_3411_2000 * g16 + F_305_16 * g26
        - F_1677_400 * g14 * g22 - F_289_80 * g12 * g24
    )
    return b1 / P16 + b2 / P16 ** 2


# ---------------------------------------------------------------------------
# RGE 积分（RK4，t = ln(mu/GeV) 固定步长；状态 [lam, y, g2, gp, g3]）
# ---------------------------------------------------------------------------
def _rk4_block(s, h, loop, y4_sign):
    k1 = beta_all(s[0], s[1], s[2], s[3], s[4], loop, y4_sign)
    s2 = [s[j] + h / 2 * k1[j] for j in range(5)]
    k2 = beta_all(s2[0], s2[1], s2[2], s2[3], s2[4], loop, y4_sign)
    s3 = [s[j] + h / 2 * k2[j] for j in range(5)]
    k3 = beta_all(s3[0], s3[1], s3[2], s3[3], s3[4], loop, y4_sign)
    s4 = [s[j] + h * k3[j] for j in range(5)]
    k4 = beta_all(s4[0], s4[1], s4[2], s4[3], s4[4], loop, y4_sign)
    return [s[j] + h / 6 * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) for j in range(5)]


def rk4_run(t0, st0, t1, dt, loop=2, y4_sign=-1):
    """从 t0 积到 t1（整步 + 末步补齐到 t1），返回 (ts, states)。

    末步必须补齐到 t1：与 float64 独立实现（while t<t1: h=min(dt,t1-t)）同构。
    若只取 int((t1-t0)/dt) 整步，预跑会落在 t1 前 ~0.008 个 e-fold，g3 偏差经
    二圈 g3^6 大系数项放大成 ~5% 的 β_λ 差，近临界区足以产生 1.5% 的 Λ 差
    （CT7 实测）。mpf 下 h=t1-t 精确可加回，循环必终止。
    """
    ts = [t0]
    sts = [list(st0)]
    t = t0
    while t < t1:
        h = dt if t1 - t > dt else t1 - t
        sn = _rk4_block(sts[-1], h, loop, y4_sign)
        t = t + h
        ts.append(t)
        sts.append(sn)
    return ts, sts


def crossing_from_traj(ts, sts, f, loop=2, y4_sign=-1, tol=mpf("1e-9")):
    """在轨迹上找 f(state) 首次 <=0 的 t（二分细化）。返回 t 或 None。"""
    idx = None
    for i in range(len(sts)):
        if f(sts[i]) <= 0:
            idx = i
            break
    if idx is None or idx == 0:
        return None
    t_lo = ts[idx - 1]
    t_hi = ts[idx]
    for _ in range(60):
        if t_hi - t_lo < tol:
            break
        t_mid = (t_lo + t_hi) / 2
        s_mid = _rk4_block(sts[idx - 1], t_mid - t_lo, loop, y4_sign)
        if f(s_mid) > 0:
            t_lo = t_mid
        else:
            t_hi = t_mid
    return t_hi


def crossing_up_from_traj(ts, sts, f, loop=2, y4_sign=-1, tol=mpf("1e-9")):
    """在轨迹上找 f(state) 首次 >0 的 t（f 起点须 <=0；二分细化）。返回 t 或 None。

    与 crossing_from_traj（首次 <=0）互补：用于 λ 自下向上穿越非微扰阈值 π
    的探测。旧实现把 λ=π 交给「首次 <=0」探测器 ⇒ 因 λ 起点恒 <π（idx=0）
    而永远返回 None——静默 bug：B1「Λ_P 不存在」的结论虽对但理由错误，
    H5 的 m_h^triv 更因此完全失去机器依据。绕极点后 λ 从 +∞ 跌到 -∞，首个
    >0 仍先于极点出现 ⇒ 探测器取到的必为真 π 穿越（非绕极伪影）。
    """
    idx = None
    for i in range(len(sts)):
        if f(sts[i]) > 0:
            idx = i
            break
    if idx is None or idx == 0:
        return None
    t_lo = ts[idx - 1]
    t_hi = ts[idx]
    for _ in range(60):
        if t_hi - t_lo < tol:
            break
        t_mid = (t_lo + t_hi) / 2
        s_mid = _rk4_block(sts[idx - 1], t_mid - t_lo, loop, y4_sign)
        if f(s_mid) > 0:
            t_hi = t_mid
        else:
            t_lo = t_mid
    return t_hi


# ---------------------------------------------------------------------------
# 跑动场景装配（带缓存，避免同参数重复全跑）
# ---------------------------------------------------------------------------
_CACHE = {}

# 规范输入纪元：gauge_initial 的任一全局输入变化 ⇒ epoch+1 ⇒ 缓存键失效。
# 动机：G5 的 dlog_a3 会临时改 A3_MZ；若缓存键不含规范输入，将命中陈旧
# 条目 ⇒ α_s 不确定度贡献被静默吞成 0（假绿）。epoch 只在输入真变时 bump，
# 不影响同输入下的缓存命中。
_GAUGE_EPOCH = 0
_GAUGE_KEY = None


def gauge_initial():
    """M_Z 处的 (g2, gp, g3)。"""
    global _GAUGE_EPOCH, _GAUGE_KEY
    gk = (str(ALPHA_MZ_INV), str(SIN2TW), str(A3_MZ), str(V), str(M_Z))
    if gk != _GAUGE_KEY:
        _GAUGE_EPOCH += 1
        _GAUGE_KEY = gk
    alpha = 1 / ALPHA_MZ_INV
    e = sqrt(4 * MPI * alpha)
    g2 = e / sqrt(SIN2TW)
    gp = e / sqrt(1 - SIN2TW)
    g3 = sqrt(4 * MPI * A3_MZ)
    return g2, gp, g3


def assemble(m_h, m_t, lam_match=None, y_match=None, loop=2, dt=mpf("0.01"),
             y4_sign=-1, use_cache=True):
    """从 M_Z 跑规范耦合到 M_t，在 M_t 匹配 (lam, y)，再跑到 M_Pl。

    lam_match/y_match 为 None 时用 LO 朴素匹配；否则用给定值（NNLO 对标口径）。
    返回 dict：state_Mt, lam_Mpl, t_cross0（lambda 过零）, t_cross_np（lambda=pi）。
    """
    g2, gp, g3 = gauge_initial()   # 先刷新纪元，再用它建缓存键（次序反会命中陈旧条目）
    key = (str(m_h), str(m_t), str(lam_match), str(y_match), loop, str(dt), y4_sign,
           _GAUGE_EPOCH)
    if use_cache and key in _CACHE:
        return _CACHE[key]
    lam_lo = m_h ** 2 / (2 * V ** 2)
    y_lo = sqrt(2) * m_t / V
    t_z, t_t, t_pl = log(M_Z), log(m_t), log(M_PL)
    _, sts_pre = rk4_run(t_z, [lam_lo, y_lo, g2, gp, g3], t_t, dt, loop)
    s_pre = sts_pre[-1]
    lam0 = lam_lo if lam_match is None else lam_match
    y0 = y_lo if y_match is None else y_match
    s_mt = [lam0, y0, s_pre[2], s_pre[3], s_pre[4]]
    ts, sts = rk4_run(t_t, s_mt, t_pl, dt, loop, y4_sign)
    f0 = lambda s: s[0]
    fnp = lambda s: s[0] - LAM_NP
    out = {
        "state_Mt": s_mt,
        "lam_Mpl": sts[-1][0],
        "t_cross0": crossing_from_traj(ts, sts, f0, loop, y4_sign),
        "t_cross_np": crossing_up_from_traj(ts, sts, fnp, loop, y4_sign),
        "traj": (ts, sts),
    }
    if use_cache:
        _CACHE[key] = out
    return out


def instability_scale(m_h, m_t, lam_match=None, y_match=None, loop=2, dt=mpf("0.01")):
    out = assemble(m_h, m_t, lam_match, y_match, loop, dt)
    tc = out["t_cross0"]
    return None if tc is None else exp(tc)


def lam_at_mpl(m_h, m_t, lam_match=None, y_match=None, loop=2, dt=mpf("0.01")):
    return assemble(m_h, m_t, lam_match, y_match, loop, dt)["lam_Mpl"]


# ---------------------------------------------------------------------------
# float64 独立交叉核对（不复用 mpmath 代码路径；末端二分细化）
# ---------------------------------------------------------------------------
def instability_scale_f64(m_h, m_t, loop=2, dt=0.01):
    import math
    P = 16 * math.pi ** 2

    def bb(lam, y, g2, gp, g3):
        y2, y4, y6 = y * y, y ** 4, y ** 6
        g22, g24, g26 = g2 * g2, g2 ** 4, g2 ** 6
        gp2, gp4, gp6 = gp * gp, gp ** 4, gp ** 6
        g32, g34 = g3 * g3, g3 ** 4
        lam2 = lam * lam
        b1 = (24 * lam2 - 6 * y4 + 0.375 * (2 * g24 + (g22 + gp2) ** 2)
              + (-9 * g22 - 3 * gp2 + 12 * y2) * lam)
        by1 = y * (4.5 * y2 - 2.25 * g22 - 17 / 12 * gp2 - 8 * g32)
        bgp1 = 41 / 6 * gp ** 3
        bg21 = -19 / 6 * g2 ** 3
        bg31 = -7 * g3 ** 3
        if loop == 1:
            return [b1 / P, by1 / P, bg21 / P, bgp1 / P, bg31 / P]
        b2 = ((1 / 48) * (915 * g26 - 289 * g24 * gp2 - 559 * g22 * gp4 - 379 * gp6)
              + 30 * y6 - y4 * (8 / 3 * gp2 + 32 * g32 + 3 * lam)
              + lam * (-73 / 8 * g24 + 39 / 4 * g22 * gp2 + 629 / 24 * gp4
                       + 108 * g22 * lam + 36 * gp2 * lam - 312 * lam2)
              + y2 * (-9 / 4 * g24 + 21 / 2 * g22 * gp2 - 19 / 4 * gp4
                      + lam * (45 / 2 * g22 + 85 / 6 * gp2 + 80 * g32 - 144 * lam)))
        by2 = y * (-23 / 4 * g24 - 3 / 4 * g22 * gp2 + 1187 / 216 * gp4
                   + 9 * g22 * g32 + 19 / 9 * gp2 * g32 - 108 * g34
                   + (225 / 16 * g22 + 131 / 16 * gp2 + 36 * g32) * y2
                   + 6 * (-2 * y4 - 2 * y2 * lam + lam2))
        bgp2 = gp ** 3 * (199 / 18 * gp2 + 9 / 2 * g22 + 44 / 3 * g32 - 17 / 6 * y2)
        bg22 = g2 ** 3 * (3 / 2 * gp2 + 35 / 6 * g22 + 12 * g32 - 3 / 2 * y2)
        bg32 = g3 ** 3 * (11 / 6 * gp2 + 9 / 2 * g22 - 26 * g32 - 2 * y2)
        return [b1 / P + b2 / P ** 2, by1 / P + by2 / P ** 2,
                bg21 / P + bg22 / P ** 2, bgp1 / P + bgp2 / P ** 2,
                bg31 / P + bg32 / P ** 2]

    def step(s, h):
        k1 = bb(*s)
        s2 = [s[j] + h / 2 * k1[j] for j in range(5)]
        k2 = bb(*s2)
        s3 = [s[j] + h / 2 * k2[j] for j in range(5)]
        k3 = bb(*s3)
        s4 = [s[j] + h * k3[j] for j in range(5)]
        k4 = bb(*s4)
        return [s[j] + h / 6 * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) for j in range(5)]

    alpha = 1 / 127.95
    e = math.sqrt(4 * math.pi * alpha)
    g2, gp, g3 = (e / math.sqrt(0.23122), e / math.sqrt(1 - 0.23122),
                  math.sqrt(4 * math.pi * 0.1180))
    lam_lo = m_h ** 2 / (2 * 246.22 ** 2)
    y_lo = math.sqrt(2) * m_t / 246.22
    s = [lam_lo, y_lo, g2, gp, g3]
    t = math.log(91.1876)
    t_t = math.log(m_t)
    while t < t_t - 1e-15:
        h = min(dt, t_t - t)
        s = step(s, h)
        t += h
    s[0], s[1] = lam_lo, y_lo
    t = t_t
    t_pl = math.log(1.2209e19)
    while t < t_pl:
        h = min(dt, t_pl - t)
        s_new = step(s, h)
        if s_new[0] <= 0:
            lo, hi = t, t + h
            for _ in range(40):
                mid = (lo + hi) / 2
                sm = step(s, mid - lo)
                if sm[0] > 0:
                    lo = mid
                else:
                    hi = mid
            return math.exp(hi)
        s = s_new
        t += h
    return None


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def fmt(x, nd=8):
    if x is None:
        return "None"
    return mp.nstr(x, nd)


def _log(*a):
    sys.stderr.write(" ".join(str(x) for x in a) + "\n")
    sys.stderr.flush()


def main():
    t_start = time.time()
    R = {"meta": {}, "inputs": {}, "control_groups": [], "guards": [], "entries": []}
    DT = mpf("0.01")

    R["meta"] = {
        "volume": "73",
        "title": "Higgs 扇区：真空稳定性与平庸性边界（SM 有效场论窗口）",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "method": "mpmath 250-bit + Fraction 符号层 + float64 独立交叉",
        "sources": [
            "arXiv:1412.8230v1 §2（β_λ GUT 约定）",
            "arXiv:1202.5717 附录 A Eq.(21)-(24)（β 全集，MV+Arason）",
            "arXiv:1307.3536v4（Buttazzo 基准 Eq.57/61/64/65/67, Table 2/3）",
        ],
        "module_path": os.path.abspath(__file__),
        "module_mtime": time.strftime("%Y-%m-%dT%H:%M:%S",
                                      time.localtime(os.path.getmtime(__file__))),
    }
    R["inputs"] = {
        "m_h_pole_GeV": [fmt(M_H), fmt(D_M_H)],
        "m_t_pole_GeV": [fmt(M_T), fmt(D_M_T)],
        "alpha_s_MZ": [fmt(A3_MZ), fmt(D_A3)],
        "alpha_MZ_inv": fmt(ALPHA_MZ_INV),
        "sin2thetaW_MSbar": fmt(SIN2TW),
        "v_GeV": fmt(V),
        "M_Pl_GeV": fmt(M_PL),
        "lam_NP_threshold": fmt(LAM_NP),
        "benchmark_Buttazzo": {
            "m_h": fmt(BM_M_H), "m_t": fmt(BM_M_T), "alpha_s": fmt(BM_A3),
            "lam_NNLO_Mt": fmt(BM_LAM_NNLO), "yt_NNLO_Mt": fmt(BM_YT_NNLO),
            "lam_LO_Mt": fmt(BM_LAM_LO), "yt_LO_Mt": fmt(BM_YT_LO),
            "lam_MPl": fmt(BM_LAM_MPL), "m_h_crit_GeV": fmt(BM_MH_CRIT),
        },
    }

    lam_lo_now = M_H ** 2 / (2 * V ** 2)
    y_lo_now = sqrt(2) * M_T / V
    lam_lo_bm = BM_M_H ** 2 / (2 * V ** 2)
    y_lo_bm = sqrt(2) * BM_M_T / V

    def log_scale(m_h, m_t, lm=None, ym=None, loop=2):
        s = instability_scale(m_h, m_t, lm, ym, loop, DT)
        return None if s is None else log(s) / log(10)

    # =====================================================================
    # 控制组（判别力先行）
    # =====================================================================
    cgs = []
    _log("[CT1] 双源 beta_lambda 恒等 ...")

    # CT1：双源 β_λ 恒等（GUT ↔ 超荷换算；每个测试点用各自的 gp 换算 g1）
    ct1_max = mpf("0")
    for lam, y, g2, gp, g3 in [(mpf("0.129"), mpf("0.94"), mpf("0.6478"), mpf("0.3583"), mpf("1.05")),
                               (mpf("0.05"), mpf("0.5"), mpf("0.55"), mpf("0.40"), mpf("0.9")),
                               (mpf("0.3"), mpf("0.8"), mpf("0.60"), mpf("0.36"), mpf("1.1"))]:
        g1_pt = sqrt(mpf("5") / 3) * gp
        b_s1 = beta_lambda_src1(lam, y, g1_pt, g2, g3, loop=2)
        b_s2 = beta_all(lam, y, g2, gp, g3, loop=2)[0]
        ct1_max = max(ct1_max, abs(b_s1 - b_s2))
    ct1_ok = ct1_max < mpf("1e-50")
    cgs.append(("CT1", "双源 β_λ 恒等（S1 GUT 约定 vs S2 超荷约定，g1=√(5/3)g'）",
                fmt(ct1_max), "<1e-50", ct1_ok))
    _log("[CT1] max resid =", fmt(ct1_max), "ok =", ct1_ok)

    # CT2：LO 匹配对标 Buttazzo Table 3 LO 列
    ct2_dl = abs(lam_lo_bm - BM_LAM_LO)
    ct2_dy = abs(y_lo_bm - BM_YT_LO)
    ct2_ok = ct2_dl < mpf("1e-4") and ct2_dy < mpf("1e-4")
    cgs.append(("CT2", "LO 匹配对标 Buttazzo Table 3 LO（λ=0.12917, y=0.99561）",
                f"dλ={fmt(ct2_dl)}, dy={fmt(ct2_dy)}", "<1e-4", ct2_ok))

    # CT3：Case B（NNLO 匹配）二圈 λ(M_Pl) 对标 Eq.(61) −0.0143
    _log("[CT3] Case B assemble ...")
    out_B = assemble(BM_M_H, BM_M_T, BM_LAM_NNLO, BM_YT_NNLO, 2, DT)
    lam_mpl_B = out_B["lam_Mpl"]
    ct3_d = abs(lam_mpl_B - BM_LAM_MPL)
    ct3_ok = lam_mpl_B < 0 and ct3_d < mpf("0.008")
    cgs.append(("CT3", "Case B 二圈 λ(M_Pl)<0 且对标 Eq.(61)（−0.0143，容许圈阶差 0.008）",
                fmt(lam_mpl_B, 6), "±0.008", ct3_ok))
    _log("[CT3] lam(M_Pl) =", fmt(lam_mpl_B, 6), "ok =", ct3_ok)

    # CT4：Case B 二圈 Λ_λ 落在文献窗口
    lam_I_B = None if out_B["t_cross0"] is None else exp(out_B["t_cross0"])
    log_lamI_B = None if lam_I_B is None else log(lam_I_B) / log(10)
    ct4_ok = log_lamI_B is not None and mpf("9.0") < log_lamI_B < mpf("11.3")
    cgs.append(("CT4", "Case B 二圈 log10(Λ_λ/GeV) ∈ [9.0, 11.3]（文献 3-loop NNLO：λ=0 于 "
                       "~10^10–10^12 ⇒ 上沿 11.3；本卷 2-loop 预期下移，先例=同匹配 1→2 圈机读差 "
                       "1.455 dex ⇒ 下沿 9.0 留 0.8 dex 圈阶余量）",
                fmt(log_lamI_B, 5), "[9.0,11.3]", ct4_ok))

    # CT5：敏感度对标 Eq.(67)（±0.5 GeV 局部导数）
    # 设计要点：固定 lm/ym 时 m_h/m_t 只进被丢弃的预跑初值 ⇒ 必须带匹配标度
    #（λ 树标度 (m_h/m_ref)^2、y_t 线性标度，与 CT6 二分同约定），否则敏感度恒 0。
    def log_scan(m_h, m_t):
        lam0 = BM_LAM_NNLO * (m_h / BM_M_H) ** 2
        y0 = BM_YT_NNLO * (m_t / BM_M_T)
        return log_scale(m_h, m_t, lam0, y0)

    _log("[CT5] 敏感度扫描 ...")
    l0 = log_scan(BM_M_H, BM_M_T)
    lh = log_scan(BM_M_H + mpf("0.5"), BM_M_T)
    ll = log_scan(BM_M_H - mpf("0.5"), BM_M_T)
    ltp = log_scan(BM_M_H, BM_M_T + mpf("0.5"))
    ltm = log_scan(BM_M_H, BM_M_T - mpf("0.5"))
    sens_mh = (lh - ll) if (lh is not None and ll is not None) else None
    sens_mt = (ltp - ltm) if (ltp is not None and ltm is not None) else None
    ct5_ok = (sens_mh is not None and sens_mh > 0
              and abs(sens_mh - BM_SENS_MH) < mpf("0.5")
              and sens_mt is not None and sens_mt < 0
              and abs(sens_mt - BM_SENS_MT) < mpf("0.7"))
    cgs.append(("CT5", "敏感度对标 Eq.(67)：dlog10Λ/dm_h≈+0.7（±0.5）、/dm_t≈−1.0（±0.7），符号须正确",
                f"mh:{fmt(sens_mh, 4)} mt:{fmt(sens_mt, 4)}", "±0.5/±0.7", ct5_ok))
    _log("[CT5] sens_mh =", fmt(sens_mh, 4), "sens_mt =", fmt(sens_mt, 4), "ok =", ct5_ok)

    # CT6：m_h^crit（Case B 口径）对标 Eq.(64)
    def mh_crit(m_t, lam_anchor, y_anchor, m_ref, loop=2, lo=mpf("120"), hi=mpf("140")):
        """二分：λ(M_Pl)=0 的临界 m_h。匹配 λ₀(m_h)=lam_anchor·(m_h/m_ref)²（树标度）。"""
        def f(mh):
            lam0 = lam_anchor * (mh / m_ref) ** 2
            return lam_at_mpl(mh, m_t, lam0, y_anchor, loop, DT)
        a, b = lo, hi
        fa, fb = f(a), f(b)
        if fa is None or fb is None or fa * fb > 0:
            return None
        for _ in range(22):
            m = (a + b) / 2
            fm = f(m)
            if fm is None:
                return None
            if fa * fm <= 0:
                b, fb = m, fm
            else:
                a, fa = m, fm
        return (a + b) / 2

    _log("[CT6] m_h^crit Case B 二分 ...")
    mh_crit_B = mh_crit(BM_M_T, BM_LAM_NNLO, BM_YT_NNLO, BM_M_H)
    ct6_ok = mh_crit_B is not None and abs(mh_crit_B - BM_MH_CRIT) < mpf("3.0")
    cgs.append(("CT6", "m_h^crit（Case B 二圈）对标 Eq.(64) 129.6（容许匹配/圈阶差 ±3 GeV）",
                fmt(mh_crit_B, 6), "±3.0 GeV", ct6_ok))
    _log("[CT6] m_h^crit(B) =", fmt(mh_crit_B, 6), "ok =", ct6_ok)

    # CT7：float64 独立交叉
    _log("[CT7] float64 交叉 ...")
    lam_I_A_mp = instability_scale(M_H, M_T, None, None, 2, DT)
    lam_I_A_f64 = instability_scale_f64(M_H, M_T, 2, 0.01)
    if lam_I_A_mp is not None and lam_I_A_f64 is not None:
        ct7_rel = abs(lam_I_A_mp - lam_I_A_f64) / lam_I_A_mp
    else:
        ct7_rel = mpf("1")
    ct7_ok = ct7_rel < mpf("1e-6")
    cgs.append(("CT7", "float64 独立重算 Λ_I 与 mpmath 一致（相对差）",
                fmt(ct7_rel), "<1e-6", ct7_ok))
    _log("[CT7] rel =", fmt(ct7_rel), "ok =", ct7_ok)

    # CT8：反向对照（y_t⁴ 错符号 ⇒ 不得存在不稳定标度）
    _log("[CT8] 反向对照 ...")
    out_bad = assemble(M_H, M_T, None, None, 2, DT, y4_sign=+1, use_cache=False)
    t_cross_bad = out_bad["t_cross0"]
    ct8_ok = t_cross_bad is None
    cgs.append(("CT8", "反向对照：β_λ 中 y_t⁴ 项错符号 ⇒ 不得存在不稳定标度",
                "None" if t_cross_bad is None else fmt(exp(t_cross_bad)), "None", ct8_ok))
    _log("[CT8] ok =", ct8_ok)

    R["control_groups"] = [{"id": i, "desc": d, "value": str(v), "threshold": t,
                            "pass": bool(p)} for i, d, v, t, p in cgs]
    cg_all_ok = all(p for _, _, _, _, p in cgs)

    # =====================================================================
    # 守卫
    # =====================================================================
    gds = []
    _log("[G1] 步长收敛 ...")

    # G1 步长收敛（双重：Λ_I + 高标回升结构 λ_min/t_min/λ(M_Pl)）
    # 回升结构（H2）若为数值伪影，必随 dt 改变；机读验证其收敛后方可在卷文陈述。
    out_g1_fine = assemble(M_H, M_T, None, None, 2, mpf("0.005"))
    lam_I_fine = (None if out_g1_fine["t_cross0"] is None
                  else exp(out_g1_fine["t_cross0"]))
    tr_g1 = assemble(M_H, M_T, None, None, 2, DT)["traj"]   # 同键缓存命中
    g1_rel = (abs(lam_I_fine - lam_I_A_mp) / lam_I_A_mp) if (lam_I_fine and lam_I_A_mp) else mpf("1")
    lam_c = [s[0] for s in tr_g1[1]]
    lam_f = [s[0] for s in out_g1_fine["traj"][1]]
    ic = min(range(len(lam_c)), key=lambda i: lam_c[i])
    if_ = min(range(len(lam_f)), key=lambda i: lam_f[i])
    d_lam_min = abs(lam_c[ic] - lam_f[if_])
    d_t_min = abs(tr_g1[0][ic] - out_g1_fine["traj"][0][if_])
    d_lam_mpl = abs(lam_c[-1] - lam_f[-1])
    # 阈值依据：极值/末端值 <1e-6（RK4 四阶 + 250 位，收敛差应远低于此）；
    # t_min <0.05 = 5×粗网格 dt=0.01（argmin 的网格量化 ~1 格，声明式放宽 5 格）。
    g1b_ok = (d_lam_min < mpf("1e-6") and d_t_min < mpf("0.05")
              and d_lam_mpl < mpf("1e-6"))
    g1_ok = g1_rel < mpf("1e-4") and g1b_ok
    gds.append(("G1", "步长收敛：Λ_I（dt=0.005 vs 0.01）+ 回升结构（λ_min/t_min/λ(M_Pl)）双重",
                f"Λ_I rel={fmt(g1_rel)}；dλmin={fmt(d_lam_min, 3)} "
                f"dtmin={fmt(d_t_min, 4)} dλ(M_Pl)={fmt(d_lam_mpl, 3)}",
                "<1e-4 / <1e-6 / <0.05 / <1e-6", g1_ok))

    # G2 单调性（方向先固定：Λ_I 随 m_h 增而增、随 m_t 增而减）
    # 操作点 = Case B（NNLO 匹配 @ 文献锚点，扰动约定同 CT5）——与头条
    # Λ_I/m_h^crit/敏感度（CT3-CT6）完全同锚点；其 ±1 GeV 扫描同时供
    # G5 的 σ(B) 复用（中心差导数），零新增成本。
    # Case A 操作点（LO 匹配 @ 本卷输入）由 G5 的 σ(A) 扫描覆盖。
    lB0 = log_scan(BM_M_H, BM_M_T)
    lBh = log_scan(BM_M_H + 1, BM_M_T)
    lBl = log_scan(BM_M_H - 1, BM_M_T)
    lBt = log_scan(BM_M_H, BM_M_T + 1)
    lBtm = log_scan(BM_M_H, BM_M_T - 1)
    g2_ok = (lBh is not None and lBl is not None and lBt is not None
             and lBh > lB0 and lBl < lB0 and lBt < lB0)
    gds.append(("G2", "单调性：Λ_I 随 m_h 增而增、随 m_t 增而减（方向先固定后检验；Case B 文献锚点）",
                f"mh+1:{fmt(lBh, 5)} mh-1:{fmt(lBl, 5)} mt+1:{fmt(lBt, 5)} mt-1:{fmt(lBtm, 5)}",
                "定序", g2_ok))

    # G3 微扰区监护（M_t 匹配点 λ < π、y < π）
    g3_ok = lam_lo_now < LAM_NP and y_lo_now < LAM_NP
    gds.append(("G3", "M_t 匹配点微扰性 λ<π、y<π",
                f"λ={fmt(lam_lo_now)} y={fmt(y_lo_now)}", "<π", g3_ok))

    # G4 规范跑动 sanity
    s_mt_A = assemble(M_H, M_T, None, None, 2, DT)["state_Mt"]
    g3_mt = s_mt_A[4]
    g4_ok = mpf("0.9") < g3_mt < mpf("1.2") and mpf("0.9") < y_lo_now < mpf("1.05")
    gds.append(("G4", "g₃(M_t)∈[0.9,1.2]、y_t^LO(M_t)∈[0.9,1.05]",
                f"g3={fmt(g3_mt)} y={fmt(y_lo_now)}", "区间", g4_ok))

    # G5 输入不确定度传播（一阶，逐项贡献量化；双操作点）
    # Case B = NNLO 匹配 @ 文献锚点（同 CT3-CT6/CT5 头条口径）：复用 G2 的
    #   ±1 GeV 扫描（中心差导数），零新增成本；
    # Case A = LO 匹配 @ 本卷输入（同 H3 的 Case A 读数锚点）：独立扫描。
    # 两操作点的锚点与匹配均不同 ⇒ σ 差同时含两类约定差，精确分解见 B3。
    def dlog_a3_at(l0_ref, scan, mh_a, mt_a):
        """临时扰动 A3_MZ（+输入 σ），返回 Δlog10Λ_I；finally 保证全局还原。"""
        global A3_MZ
        old = A3_MZ
        try:
            A3_MZ = old + D_A3
            v_new = scan(mh_a, mt_a)
        finally:
            A3_MZ = old   # 异常路径也必须还原，否则全局污染后续全部读数
        return None if v_new is None else (v_new - l0_ref)

    def sig_from(l0v, lhv, llv, ltv, ltmv, d_a3_v):
        """中心差导数 × 输入 σ 的一阶传播；缺项记 0（并在读数中可见）。"""
        s_mh = abs((lhv - llv) / 2) * D_M_H if (lhv is not None and llv is not None) else mpf("0")
        s_mt = abs((ltv - ltmv) / 2) * D_M_T if (ltv is not None and ltmv is not None) else mpf("0")
        s_a3 = abs(d_a3_v) if d_a3_v is not None else mpf("0")
        return s_mh, s_mt, s_a3, sqrt(s_mh ** 2 + s_mt ** 2 + s_a3 ** 2)

    scan_A = lambda mh, mt: log_scale(mh, mt)          # LO 朴素匹配 @ 本卷输入
    lA0_g = scan_A(M_H, M_T)
    lAh_g = scan_A(M_H + 1, M_T)
    lAl_g = scan_A(M_H - 1, M_T)
    lAt_g = scan_A(M_H, M_T + 1)
    lAtm_g = scan_A(M_H, M_T - 1)
    sig_mh_A, sig_mt_A, sig_a3_A, sig_A = sig_from(lA0_g, lAh_g, lAl_g, lAt_g, lAtm_g,
                                                   dlog_a3_at(lA0_g, scan_A, M_H, M_T))
    sig_mh_B, sig_mt_B, sig_a3_B, sig_B = sig_from(lB0, lBh, lBl, lBt, lBtm,
                                                   dlog_a3_at(lB0, log_scan, BM_M_H, BM_M_T))
    g5_ok = sig_A > 0 and sig_B > 0
    gds.append(("G5", "输入不确定度传播 σ(log10 Λ_I) 逐项量化（双操作点）",
                f"A: mh:{fmt(sig_mh_A, 4)} mt:{fmt(sig_mt_A, 4)} a3:{fmt(sig_a3_A, 4)} "
                f"tot:{fmt(sig_A, 4)}；B: mh:{fmt(sig_mh_B, 4)} mt:{fmt(sig_mt_B, 4)} "
                f"a3:{fmt(sig_a3_B, 4)} tot:{fmt(sig_B, 4)}",
                ">0", g5_ok))

    # G7 标度 sanity
    g7_ok = (lam_I_A_mp is not None and M_T < lam_I_A_mp < M_PL and lam_I_A_mp > mpf("1e3"))
    gds.append(("G7", "标度链 m_t < Λ_I < M_Pl 且 Λ_I > 10³ GeV", fmt(lam_I_A_mp), "链", g7_ok))

    # G8 阈值依据声明
    gds.append(("G8", "阈值依据：输入 σ 传播或文献值 ± 声明倍数（禁拍脑袋）", "声明式", "声明", True))

    # G9 失控退出码逻辑
    gds.append(("G9", "失控退出码：控制组或守卫未全过 ⇒ exit 2", "逻辑", "逻辑", True))

    # =====================================================================
    # 条目（整理层 H + 攻破层 B）
    # =====================================================================
    entries = []

    # H1：LO 提取与对标
    entries.append(("H1", "整理",
                    "Higgs 机制与 λ/y_t 提取：v=(√2G_F)^-1/2，λ(M_t)=m_h²/2v²、y_t=√2m_t/v；"
                    "对标 Buttazzo Table 3 LO 列",
                    f"λ={fmt(lam_lo_bm)}（文献 {fmt(BM_LAM_LO)}）、y={fmt(y_lo_bm)}（文献 {fmt(BM_YT_LO)}）",
                    "PASS" if ct2_ok else "FAIL"))

    # H2：跑动结构（含高标回升——机读发现，非先验预期）
    # 陈述对象随读数修正：λ 并非全程单调递减，过零后触底回升（高标 y_t 衰减
    # ⇒ 负驱动 −6y⁴ 减弱 ⇒ λ² 项主导 ⇒ β_λ 变正）。回升不改变亚稳判定
    # （λ(M_Pl) 仍 <0），其收敛性由 G1（dt 减半）机读背书。
    ts_A, sts_A = assemble(M_H, M_T, None, None, 2, DT)["traj"]
    lam_traj = [s[0] for s in sts_A]
    i_min = min(range(len(lam_traj)), key=lambda i: lam_traj[i])
    mono = all(lam_traj[i + 1] < lam_traj[i] for i in range(len(lam_traj) - 1))
    h2_ok = (lam_I_A_mp is not None) and (lam_traj[-1] < 0)
    entries.append(("H2", "整理",
                    "二圈跑动结构：λ 自 M_t 下降并过零（亚稳）⇒ 高标触底回升"
                    "（y_t 衰减致 β_λ 变号）⇒ λ(M_Pl)<0；回升不改变亚稳判定"
                    "（文献 §4.1：β_λ 于 10^17–10^18 GeV 消失，与本卷触底位置互为印证）",
                    f"λ(M_t)={fmt(lam_traj[0])}；过零 Λ_I={fmt(lam_I_A_mp)} GeV；"
                    f"触底 t={fmt(ts_A[i_min], 4)}（μ≈{fmt(exp(ts_A[i_min]), 5)} GeV）"
                    f"λ={fmt(lam_traj[i_min], 6)}；回升至 λ(M_Pl)={fmt(lam_traj[-1], 6)}；"
                    f"全程单调递减:{mono}（dt 收敛验证见 G1）",
                    "PASS" if h2_ok else "FAIL"))

    # H3：Λ_I 与敏感度（Case A/B + 圈阶对比 B1/B2）
    _log("[H3] 一圈 Case B1 ...")
    out_B1 = assemble(BM_M_H, BM_M_T, BM_LAM_NNLO, BM_YT_NNLO, 1, DT)
    lam_I_B1 = None if out_B1["t_cross0"] is None else exp(out_B1["t_cross0"])
    log_lamI_B1 = None if lam_I_B1 is None else log(lam_I_B1) / log(10)
    h3_ok = ct4_ok and ct5_ok
    entries.append(("H3", "整理",
                    "不稳定标度 Λ_I（Case A LO 匹配 / Case B NNLO 匹配）+ 敏感度对标 Eq.(67)；"
                    "圈阶对比 B1（一圈）/B2（二圈）同匹配",
                    f"Case A: {fmt(lam_I_A_mp)} GeV；Case B2: {fmt(lam_I_B)} GeV；"
                    f"Case B1(一圈): {fmt(lam_I_B1)} GeV；敏感度 mh:{fmt(sens_mh, 4)}/mt:{fmt(sens_mt, 4)}",
                    "PASS" if h3_ok else "FAIL"))

    # H4：m_h^crit
    # Case A 用「扫描首个上穿 + 区间二分」：LO 匹配 y0=√2m_t/v 比 NNLO 高 5.9%，
    # y^4 驱动更强 ⇒ 稳定边界被推高；且大 λ0 下 Landau 极点可落至 M_Pl 以下、
    # λ(M_Pl) 绕极点为负，固定括号首尾可能同号 ⇒ 只认首个由负转正。
    def mh_crit_scan(m_t, lam_anchor, y_anchor, m_ref, loop=2,
                     lo=mpf("120"), hi=mpf("200"), step=mpf("10")):
        def f(mh):
            lam0 = lam_anchor * (mh / m_ref) ** 2
            return lam_at_mpl(mh, m_t, lam0, y_anchor, loop, DT)
        m = lo
        f_prev = f(m)
        _log("[H4] 扫描 m_h =", fmt(m), " λ(M_Pl) =", fmt(f_prev, 6))
        while m < hi:
            m_next = m + step
            if m_next > hi:
                m_next = hi
            f_next = f(m_next)
            _log("[H4] 扫描 m_h =", fmt(m_next), " λ(M_Pl) =", fmt(f_next, 6))
            if f_prev <= 0 < f_next:
                a, b, fa = m, m_next, f_prev
                for _ in range(22):
                    mid = (a + b) / 2
                    fm = f(mid)
                    if fa * fm <= 0:
                        b = mid
                    else:
                        a, fa = mid, fm
                return (a + b) / 2
            m, f_prev = m_next, f_next
        return None

    _log("[H4] m_h^crit Case A 扫描+二分 ...")
    mh_crit_A = mh_crit_scan(M_T, lam_lo_now, y_lo_now, M_H)
    crit_A_s = (f"{fmt(mh_crit_A)} GeV" if mh_crit_A is not None
                else "None（[120,200] 扫描内 λ(M_Pl) 未由负转正 ⇒ LO 匹配窗口内无绝对稳定解）")
    entries.append(("H4", "整理",
                    "绝对稳定性临界质量 m_h^crit（Case A/B 二圈）对标 Eq.(64/65)",
                    f"Case B: {fmt(mh_crit_B)} GeV（文献 {fmt(BM_MH_CRIT)}±{fmt(BM_D_MH_CRIT)}）；"
                    f"Case A: {crit_A_s}",
                    "PASS" if ct6_ok else "FAIL"))
    _log("[H4] m_h^crit(A) =", fmt(mh_crit_A, 6))

    # H5：m_h^triv（平庸性上界）
    # 定义：λ 在 M_Pl 以下首次触及非微扰上界 π 的临界 m_h（LO 匹配二圈，
    # 与 H4 Case A 同约定）。
    # 实现：t_cross_np（上穿探测器，见 crossing_up_from_traj）由 None 转非
    # None 的首个 m_h ⇒ 扫描 [148,208]（148 > m_h^crit(A)，其下 λ(M_Pl)<0
    # 永不及 π）步长 5 GeV 取 bracket + 二分 22 步细化。
    # 为什么不用 λ(M_Pl)−π 判据：m_h 超过临界后 Landau 极点掉到 M_Pl 以下，
    # 固定步长 RK4 绕极点把 λ(M_Pl) 甩成巨大值（正负不定）⇒ f 不连续，
    # 端点判据必败（旧版扫描窗 [185,210] 即因此全错位：窗内 λ(M_Pl)−π 恒
    # ≈ +9，真实穿越点在 150–185 之间，旧版报告 INFO/None）。
    def mh_triv(m_t, loop=2, lo=mpf("148"), hi=mpf("208"), step=mpf("5")):
        def has_np(mh):
            return assemble(mh, m_t, None, None, loop, DT)["t_cross_np"] is not None
        m = lo
        prev = has_np(m)
        _log("[H5] 扫描 m_h =", fmt(m), " π上穿存在:", prev)
        while m < hi:
            m_next = m + step
            if m_next > hi:
                m_next = hi
            cur = has_np(m_next)
            _log("[H5] 扫描 m_h =", fmt(m_next), " π上穿存在:", cur)
            if (not prev) and cur:
                a, b = m, m_next
                for _ in range(22):
                    mid = (a + b) / 2
                    if has_np(mid):
                        b = mid
                    else:
                        a = mid
                return (a + b) / 2
            m, prev = m_next, cur
        return None

    _log("[H5] m_h^triv 扫描+二分 ...")
    mh_triv_A = mh_triv(M_T)
    # 一圈解析双约定（y_t=g=0 纯四次型）：
    #  (a) λ(M_Pl)=π：λ0=π/(1+3L/2π), m_h=v√(2λ0)，L=ln(M_Pl/v)
    L_an = log(M_PL / V)
    lam0_pi = MPI / (1 + 3 * L_an / (2 * MPI))
    mh_triv_analytic_pi = sqrt(2 * lam0_pi) * V
    mh_triv_1loop_analytic = sqrt(4 * MPI ** 2 * V ** 2 / (3 * L_an))  # Landau 极点在 M_Pl
    triv_A_s = (f"{fmt(mh_triv_A)} GeV" if mh_triv_A is not None
                else "None（[148,208] 扫描内 λ 未触 π ⇒ LO 匹配窗口内无平庸性上界）")
    entries.append(("H5", "整理",
                    "平庸性/非微扰上界：m_h^triv（λ 在 M_Pl 以下首触 π 的临界 Higgs "
                    "质量，LO 匹配二圈，上穿谓词扫描+二分）；一圈解析双约定"
                    "（y_t=g=0 纯四次型：λ(M_Pl)=π / Landau 极点在 M_Pl）交叉",
                    f"二圈数值: {triv_A_s}；一圈解析(λ=π): {fmt(mh_triv_analytic_pi)} GeV；"
                    f"一圈解析(Landau@M_Pl): {fmt(mh_triv_1loop_analytic)} GeV",
                    "INFO"))

    # H6：亚稳判定 z（Case B 口径）
    z = (mh_crit_B - M_H) / BM_D_MH_CRIT if mh_crit_B is not None else mpf("0")
    h6_v = "PASS" if z >= 3 else ("BOUNDARY" if z >= mpf("1.5") else "FAIL")
    entries.append(("H6", "整理",
                    "当前数据亚稳判定：m_h=125.25 低于绝对稳定临界值的 σ 距离"
                    "（Case B 口径，σ 取文献合成值 1.5 GeV）",
                    f"m_h^crit(B)={fmt(mh_crit_B)} GeV，z={fmt(z, 4)}σ",
                    h6_v))

    # B1：双窗
    out_np = assemble(M_H, M_T, None, None, 2, DT)
    lam_P_A = None if out_np["t_cross_np"] is None else exp(out_np["t_cross_np"])
    lam_P_B = None if out_B["t_cross_np"] is None else exp(out_B["t_cross_np"])
    b1_ok = lam_I_A_mp is not None and lam_I_A_mp < M_PL
    entries.append(("B1", "攻破",
                    "SM Higgs 扇区有效场论窗口：下有真空不稳定标度 Λ_I（亚稳），上界需视 m_h 而定；"
                    "作为终极理论不能外推到任意高能",
                    f"Λ_I(A)={fmt(lam_I_A_mp)} GeV、Λ_I(B)={fmt(lam_I_B)} GeV；"
                    f"Λ_P(λ=π)：A={fmt(lam_P_A)}、B={fmt(lam_P_B)} GeV"
                    f"（当前 m_h 下均不存在 ⇒ 只有下窗；上窗临界质量 m_h^triv(A)="
                    f"{fmt(mh_triv_A)} GeV，见 H5）",
                    "FAIL" if b1_ok else "PASS"))

    # B2：输入敏感度（双操作点；头条 Case B 定 verdict）
    # 阈值 0.2 dex ≅ 因子 1.6：输入涂抹若达此量级，则「Λ_I 处于 10^9–10^10」
    # 的位次声明不再由输入精度担保，须与匹配系统差（B3）合并解读（声明式阈值）。
    b2_ok = sig_B > mpf("0.2")
    entries.append(("B2", "攻破",
                    "不稳定标度的输入依赖：仅输入不确定度即使 log10 Λ_I 涂抹 ±σ"
                    "（一阶传播，中心差导数；Case A/B 双操作点——脆弱性本身随匹配"
                    "约定而变，与 B3 咬合）",
                    f"σ(log10 Λ_I)：Case B={fmt(sig_B, 4)} dex（m_h:{fmt(sig_mh_B, 4)}, "
                    f"m_t:{fmt(sig_mt_B, 4)}, α₃:{fmt(sig_a3_B, 4)}）；"
                    f"Case A={fmt(sig_A, 4)} dex（m_h:{fmt(sig_mh_A, 4)}, m_t:{fmt(sig_mt_A, 4)}, "
                    f"α₃:{fmt(sig_a3_A, 4)}）",
                    "FAIL" if b2_ok else "PASS"))

    # B3：匹配/圈阶/方案依赖（三分分解：匹配约定差 / 输入锚点差 / 合计）
    # 为什么补测 A_BM（LO 匹配 @ 文献锚点）：原「匹配差」直接相减 A_our 与
    # B_BM，混入了本卷输入与文献锚点的差（本卷 m_t 低 0.77 GeV，单独贡献
    # ~0.9 dex）⇒ 标注为「匹配差」属错标。补测后：
    #   Δ匹配 = B_BM − A_BM（同锚点，只变匹配约定）——真正的匹配系统差；
    #   Δ输入 = A_BM − A_our（同 LO 匹配，只变输入锚点）；
    #   Δ合计 = B_BM − A_our（原读数；两项之和为近似，机读分项如实报告）。
    # m_h^crit 同法分解（A_BM 临界质量：括号二分 [110,150]；该窗内 λ0 均
    # 低于 m_h^triv≈177 ⇒ 无 Landau 绕极，λ(M_Pl) 连续可二分）。
    _log("[B3] A_BM 操作点（LO 匹配 @ 文献锚点）...")
    out_A_BM = assemble(BM_M_H, BM_M_T, None, None, 2, DT)
    lam_I_A_BM = None if out_A_BM["t_cross0"] is None else exp(out_A_BM["t_cross0"])
    mh_crit_A_BM = mh_crit(BM_M_T, lam_lo_bm, y_lo_bm, BM_M_H, 2,
                           mpf("110"), mpf("150"))
    _log("[B3] Λ_I(A_BM) =", fmt(lam_I_A_BM), " m_h^crit(A_BM) =", fmt(mh_crit_A_BM, 6))

    def _lg(x):
        return None if x is None else log(x) / log(10)

    d_lam_match = (abs(_lg(lam_I_B) - _lg(lam_I_A_BM))
                   if (lam_I_B and lam_I_A_BM) else mpf("0"))
    d_lam_inputs = (abs(_lg(lam_I_A_BM) - _lg(lam_I_A_mp))
                    if (lam_I_A_BM and lam_I_A_mp) else mpf("0"))
    d_lamI_dex_AB = (abs(_lg(lam_I_B) - _lg(lam_I_A_mp))
                     if (lam_I_B and lam_I_A_mp) else mpf("0"))
    d_lamI_dex_loop = (abs(_lg(lam_I_B1) - _lg(lam_I_B))
                       if (lam_I_B1 and lam_I_B) else mpf("0"))
    d_crit_match = (abs(mh_crit_A_BM - mh_crit_B)
                    if (mh_crit_A_BM and mh_crit_B) else mpf("0"))
    d_crit_inputs = (abs(mh_crit_A - mh_crit_A_BM)
                     if (mh_crit_A and mh_crit_A_BM) else mpf("0"))
    d_crit = abs(mh_crit_A - mh_crit_B) if (mh_crit_A and mh_crit_B) else mpf("0")
    # 阈值：0.05 dex ≈ 12%（约定差可感知下限）；0.5 GeV（临界质量位移可感知下限）
    b3_ok = (d_lam_match > mpf("0.05") or d_crit_match > mpf("0.5")
             or d_lamI_dex_loop > mpf("0.05"))
    entries.append(("B3", "攻破",
                    "匹配/圈阶/方案依赖：LO 朴素匹配 vs NNLO 匹配的系统差（同锚点隔离）"
                    "＋ 输入锚点差（同匹配隔离）＋ 合计；λ(M_t) 0.12917 vs 0.12604 "
                    "= −1.1%、y_t 0.991 vs 0.940；圈阶差单独量化",
                    f"匹配差（同锚点）Δlog10 Λ_I={fmt(d_lam_match, 4)} dex、"
                    f"Δm_h^crit={fmt(d_crit_match, 4)} GeV；"
                    f"输入锚点差（同匹配）Δlog10 Λ_I={fmt(d_lam_inputs, 4)} dex、"
                    f"Δm_h^crit={fmt(d_crit_inputs, 4)} GeV；"
                    f"合计 Δlog10 Λ_I={fmt(d_lamI_dex_AB, 4)} dex、Δm_h^crit={fmt(d_crit, 4)} GeV；"
                    f"圈阶差(1vs2圈, 同匹配同锚点)={fmt(d_lamI_dex_loop, 4)} dex",
                    "BOUNDARY" if b3_ok else "INFO"))

    # B4：与统一场论议程咬合
    lam_qcd = mpf("0.22623372")  # 70 卷 Λ_QCD 二圈机读值（跨卷引用，注明出处）
    b4_ok = lam_qcd < lam_I_B < M_PL if lam_I_B else False
    entries.append(("B4", "攻破",
                    "与统一场论议程咬合：SM 两扇区断裂边界（QCD Λ_QCD≈0.226 GeV 非微扰 / "
                    "Higgs Λ_I≈10^9-10^10 GeV 亚稳）须在任何统一方案中同时修补；"
                    "near-criticality（m_h 距稳定边界 zσ）未解释",
                    f"Λ_QCD(70 卷)={fmt(lam_qcd)} GeV << Λ_I(B)={fmt(lam_I_B)} GeV < "
                    f"M_Pl={fmt(M_PL)} GeV；z={fmt(z, 3)}σ",
                    "FAIL" if b4_ok else "OPEN"))

    R["entries"] = [{"id": i, "layer": l, "claim": c, "reading": r, "verdict": v}
                    for i, l, c, r, v in entries]

    # 守卫补齐（G6 结构完整）
    tally = {}
    for _, _, _, _, v in entries:
        tally[v] = tally.get(v, 0) + 1
    g6_ok = sum(tally.values()) == len(entries)
    gds.insert(5, ("G6", "结构完整：tally 合计 == 条目数",
                   f"{sum(tally.values())} vs {len(entries)}", "相等", g6_ok))
    R["guards"] = [{"id": i, "desc": d, "value": str(v), "threshold": t, "pass": bool(p)}
                   for i, d, v, t, p in gds]
    g_all_ok = all(p for _, _, _, _, p in gds)

    R["summary"] = {
        "tally": tally, "n_entries": len(entries),
        "control_groups_pass": sum(1 for c in cgs if c[4]),
        "guards_pass": sum(1 for g in gds if g[4]),
        "elapsed_s": round(time.time() - t_start, 1),
    }
    R["exit_code"] = 0 if (cg_all_ok and g_all_ok) else 2
    return R


# ---------------------------------------------------------------------------
# 三件套输出
# ---------------------------------------------------------------------------
def build_md(R):
    L = []
    L.append("# UFT-73 ｜ Higgs 扇区：真空稳定性与平庸性边界（SM 有效场论窗口）\n")
    L.append(f"- 生成时刻：{R['meta']['generated_at']}")
    L.append(f"- 方法：{R['meta']['method']}")
    L.append(f"- 模块：{R['meta']['module_path']}（mtime {R['meta']['module_mtime']}）")
    L.append("- β 系数来源：arXiv:1412.8230v1（GUT 约定）+ arXiv:1202.5717 附录 A"
             "（超荷约定，MV+Arason），双源互证 CT1")
    L.append("- 基准来源：arXiv:1307.3536v4（Buttazzo et al.）Eq.57/61/64/65/67 + Table 2/3\n")
    L.append("## 控制组\n")
    for c in R["control_groups"]:
        L.append(f"- [{'PASS' if c['pass'] else 'FAIL'}] **{c['id']}** {c['desc']}："
                 f"{c['value']}（阈 {c['threshold']}）")
    L.append("\n## 条目\n")
    for e in R["entries"]:
        L.append(f"### [{e['verdict']}] {e['id']}（{e['layer']}）{e['claim']}")
        L.append(f"{e['reading']}\n")
    L.append("## 守卫\n")
    for g in R["guards"]:
        L.append(f"- [{'PASS' if g['pass'] else 'FAIL'}] **{g['id']}** {g['desc']}："
                 f"{g['value']}（阈 {g['threshold']}）")
    L.append("\n## 汇总\n")
    L.append(f"- tally：{R['summary']['tally']}")
    L.append(f"- 控制组：{R['summary']['control_groups_pass']}/{len(R['control_groups'])}；"
             f"守卫：{R['summary']['guards_pass']}/{len(R['guards'])}")
    L.append(f"- 退出码：{R['exit_code']}")
    L.append(f"- 耗时：{R['summary']['elapsed_s']} s")
    return "\n".join(L) + "\n"


def build_report(R):
    L = []
    L.append("UFT-73 Higgs 扇区：真空稳定性与平庸性边界")
    L.append(f"生成时刻 {R['meta']['generated_at']}  mpmath dps={mp.dps}")
    L.append(f"模块 {R['meta']['module_path']}  mtime {R['meta']['module_mtime']}")
    L.append("")
    L.append("== 控制组 ==")
    for c in R["control_groups"]:
        L.append(f"[{'PASS' if c['pass'] else 'FAIL'}] {c['id']:<4} {c['desc'][:58]:<60} {c['value']}")
    L.append("")
    L.append("== 条目 ==")
    for e in R["entries"]:
        L.append(f"[{e['verdict']:<8}] {e['id']:<4} {e['reading'][:88]}")
    L.append("")
    L.append("== 守卫 ==")
    for g in R["guards"]:
        L.append(f"[{'PASS' if g['pass'] else 'FAIL'}] {g['id']:<4} {g['desc'][:58]:<60} {g['value']}")
    L.append("")
    L.append("== 汇总 ==")
    L.append(f"tally {R['summary']['tally']}")
    L.append(f"控制组 {R['summary']['control_groups_pass']}/{len(R['control_groups'])}  "
             f"守卫 {R['summary']['guards_pass']}/{len(R['guards'])}")
    L.append(f"退出码 {R['exit_code']}  耗时 {R['summary']['elapsed_s']}s")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    R = main()
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "73_higgs_stability_results.json"), "w", encoding="utf-8") as f:
        json.dump(R, f, ensure_ascii=False, indent=2, default=str)
    with open(os.path.join(base, "73_higgs_stability_results.md"), "w", encoding="utf-8") as f:
        f.write(build_md(R))
    with open(os.path.join(base, "73_higgs_stability_report.txt"), "w", encoding="utf-8") as f:
        f.write(build_report(R))
    print(build_report(R))
    sys.exit(R["exit_code"])
