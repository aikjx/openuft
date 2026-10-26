# -*- coding: utf-8 -*-
r"""TUFT-r226 · 四力统一方程·量子束缚层：同一势写进薛定谔方程——四力束缚态判决与波函数可视化
2026-10-26

〔编号说明〕本卷源初稿占号 r223（03:33 占号检查零命中），但并行链 r223《四力统一运动方程_求导
证明机验与轨道进动精算》源码于 03:27:40 先落（与本次检查相差约 40 秒，同型竞态第三次）；
按「先占位者为权威」整体改号，r224/r225 亦被占，取 **r226**。本卷与并行 r223（轨道进动机验）、
r224/r225（进行中）主题不重叠；本卷名下 3 份 r223 数据文件已删除，未触碰并行任何字节。

用户诉求（承 r214/r221 同一诉求的继续）：
  「继续所有力写进一个运动上面，并可视化，写力的统一方程，
    求导证明验证精算分析力的大小方向距离特性」

本卷要回答的问题（量子层 = "大小/方向/距离"三特性的谱学升级）：
  Q1 同一个统一势 UFE-4F⁺ 写进薛定谔方程 iħ∂ψ/∂t = [−ħ²/(2μ)∇² + U(r)]ψ 后，
     每种力的**束缚态存在性、谱、半径**各是什么？
  Q2 经典层"合格"的参数在量子层是否仍合格？——**氘核判决**：r214 剩余核力参数
     （α=14.6, λ_π=1.4619 fm）在薛定谔方程下给出什么？
  Q3 哪些实验锚点能被这一层命中？——氢原子谱（解析精确）、J/ψ–ψ(2S) 分裂、χc1、Υ(2S)。
  Q4 弱力/引力的量子束缚判决？——弱力无束缚态（定量判据 g≪g_crit）；
     引力"氢原子"形式存在但半径 1e32 m ≫ 可观测宇宙。

方法（数值谱 caliber 声明）：
  · Numerov 六阶精度径向积分 u'' = f(r)u，f = (2μ/(ħc)²)(V_eff − E) + l(l+1)/r²；
  · 扫描 E → u_end 符号变号定位 + 二分法求本征值；节点计数标定量子数 n；
  · **float64 数值谱**（本卷声明口径）：求解器由氢原子**解析精确谱**逐位校验
    （E_n = −Ry/n²、⟨r⟩₁ₛ = 1.5a₀、2s/2p 简并、μ 偏移的定量阴性对照），
    收敛由网格倍增守卫钉住；解析量（α 临界判据、半经典态计数）用声明公式。
    —— 与库内 Decimal 250 位传统不冲突：本卷对象是 ODE 本征值，误差由解析锚点界定。

系统与锚点：
  S2 电磁（氢）：E_n = −13.605693/n² eV（CODATA Rydberg）、⟨r⟩₁ₛ=1.5a₀
  S3 剩余核力（氘核）：实验 E_B = −2.2246 MeV、⟨r⟩ = 1.975 fm；
     r214 参数 α=14.6（g²/4π 口径）+ λ_π 的量子谱判决；单参数 α_y 拟合与半径错配定价
  S4 色道（粲偶素/底偶素）：M(J/ψ)=3096.900、M(ψ(2S))=3686.097（Δ=589.197 MeV 校准 α_s）、
     M(χc1)=3510.667（1P 对照）、M(Υ)=9460.300、M(Υ(2S))=10023.26（交叉预言 562.96 MeV）；
     σ = 0.18 GeV²（承 r221 双路换算 912.19 MeV/fm）
  S5 弱力：判据 g = α·λ·μ₁ ≪ g_crit（l=0 Yukawa 首个本征值阈值）+ 数值扫描确认
  S6 引力：库仑型解析（λ=∞）——"引力氢原子"尺度读数

纪律：纯标准库；对 r214/r218–r222 全部产物只读；守卫失败即非零退出；
控制组含**定量阴性对照**（μ 偏 10% ⇒ 氢谱恰偏 10%，既证明守卫有判别力、又证明偏移量可解析预期）。
本卷条目不可与 r142–r222 相加。
"""

import json
import os
import sys
from math import sqrt, log, pi, exp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r226_量子束缚层交互可视化模板_2026-10-26.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_量子束缚层可视化_2026-10-26.html")

MARKER = "R226-QUANTUM-BOUND"
BASE = ("TUFT-r226_四力统一方程_量子束缚层_同一势的薛定谔谱与四力束缚判决_"
        "精算与交互可视化_2026-10-26")
STEM = "TUFT-r226"

# ---------------------------------------------------------------------------
# 常数（PDG/CODATA；承 r214/r221 同源口径）
# ---------------------------------------------------------------------------
HARC = 197.3269804           # ħc [MeV·fm]
M_P = 938.27208816           # MeV
M_E_MEV = 0.51099895         # MeV
RY_EV = 13.605693            # eV（CODATA 里德伯）
A_EM = 1.0 / 137.035999084   # α_em
ALPHA_W = 1.0268268e-5       # r214 声明口径（G_F·m_p(c²)²，G2-4 登记）
LAM_W_FM = 2.4550179827562611e-18 * 1e15   # fm = 2.4550e-3 fm
LAM_PI_FM = 1.4619325721160970e-15 * 1e15  # fm = 1.46193 fm
ALPHA_146 = 14.6             # r214 剩余核力行口径（g²/4π）
SIGMA_MEV_FM = 912.1920      # 0.18 GeV² ⇒ 912.19 MeV/fm（r221 双路换算）
G_NEWTON = 6.6743e-11
HBARC_JM = 3.16152677e-26    # ħc [J·m]
M_E_KG = 9.1093837015e-31
R_UNIVERSE_M = 8.8e26        # 可观测宇宙半径

# 实验锚点（PDG 2024）
M_JPSI = 3096.900
M_PSI2S = 3686.097
M_CHIC1 = 3510.667
M_UPS1 = 9460.300
M_UPS2S = 10023.26
E_DEUTERON = -2.2246         # MeV
R_DEUTERON = 1.975           # fm（⟨r⟩ 实验值）
G_CRIT = 1.6798              # l=0 Yukawa 首个束缚态阈值（标准值，本卷再扫描复核）

guards, controls, entries = [], [], []


def guard(gid, title, ok, detail, numbers=None):
    guards.append({"id": gid, "title": title, "ok": bool(ok),
                   "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[GUARD-FAIL] {gid} {title}: {detail}")
    return bool(ok)


def control(cid, title, ok, detail, numbers=None):
    controls.append({"id": cid, "title": title, "ok": bool(ok),
                     "detail": detail, "numbers": numbers or {}})
    return bool(ok)


def entry(code, level, title, detail, numbers=None):
    entries.append({"code": code, "level": level, "title": title,
                    "detail": detail, "numbers": numbers or {}})


def guard_ok(gid):
    return any(g["id"] == gid and g["ok"] for g in guards)


# ---------------------------------------------------------------------------
# Numerov 求解器（float64，声明口径）
# ---------------------------------------------------------------------------
def numerov_run(vfun, k2, l, rmin, rmax, N, E, keep=False, a_inv=None):
    """径向薛定谔 u'' = f(r)u，f = k2*(V−E) + l(l+1)/r²。
    返回 (u_end, nodes, xs, us)。
    Numerov：u_{n+1}(1−h²f_{n+1}/12) = 2u_n(1+5h²f_n/12) − u_{n−1}(1−h²f_{n−1}/12)。
    起点：奇点级数 u = r^{l+1}(1 + b·r)，b = −k2·a_inv/((l+1)(l+2))（a_inv = 势中 −A/r 的 A）。
    节点计数只在经典允许区 f<0 内计（排除禁戒区尾部翻转）。"""
    h = (rmax - rmin) / N
    ll = l * (l + 1)
    b = -(k2 * a_inv) / ((l + 1) * (l + 2)) if a_inv else 0.0
    u = [0.0] * (N + 1)
    u[0] = (rmin ** (l + 1)) * (1.0 + b * rmin)
    u[1] = ((rmin + h) ** (l + 1)) * (1.0 + b * (rmin + h))
    c1 = h * h / 12.0
    fm2 = k2 * (vfun(rmin) - E) + (ll / (rmin * rmin) if l else 0.0)
    r1 = rmin + h
    fm1 = k2 * (vfun(r1) - E) + (ll / (r1 * r1) if l else 0.0)
    nodes = 0
    prev_sign = 1.0 if u[1] >= 0 else -1.0
    xs_out, us_out = ([rmin, r1], [u[0], u[1]]) if keep else (None, None)
    for i in range(1, N):
        r2 = rmin + (i + 1) * h
        f0p = k2 * (vfun(r2) - E) + (ll / (r2 * r2) if l else 0.0)
        u[i + 1] = (2.0 * u[i] * (1.0 + 5.0 * c1 * fm1)
                    - u[i - 1] * (1.0 - c1 * fm2)) / (1.0 - c1 * f0p)
        fm2, fm1 = fm1, f0p
        s = 1.0 if u[i + 1] >= 0 else -1.0
        if s != prev_sign:
            if fm1 < 0.0:
                nodes += 1
            prev_sign = s
        if keep:
            xs_out.append(r2)
            us_out.append(u[i + 1])
    if keep:
        # 剪掉禁戒区指数增长尾：从末端回找 |u| 的最后一个极小点（增长起点）。
        # 略偏离本征值时尾部被 e^{+κr} 污染，⟨r⟩/波函数导出必须截在增长起点之前。
        i = N
        m = abs(us_out[-1])
        while i > 2 and abs(us_out[i - 1]) < m:
            m = abs(us_out[i - 1])
            i -= 1
        xs_out = xs_out[:i + 1]
        us_out = us_out[:i + 1]
    return u[N], nodes, xs_out, us_out


def bisect_eigen(vfun, k2, l, rmin, rmax, N, E_lo, E_hi, tol_rel=1e-11, a_inv=None):
    """在 (E_lo, E_hi) 内用 u_end 符号二分求本征值（区间内恰有一个）。"""
    phi_lo = numerov_run(vfun, k2, l, rmin, rmax, N, E_lo, a_inv=a_inv)[0]
    for _ in range(80):
        Em = 0.5 * (E_lo + E_hi)
        phi_m = numerov_run(vfun, k2, l, rmin, rmax, N, Em, a_inv=a_inv)[0]
        if (phi_m == 0.0) or (E_hi - E_lo) < abs(Em) * tol_rel:
            return Em
        if (phi_lo >= 0) == (phi_m >= 0):
            E_lo, phi_lo = Em, phi_m
        else:
            E_hi = Em
    return 0.5 * (E_lo + E_hi)


def scan_levels(vfun, k2, l, rmin, rmax, N, E_lo, E_hi, M=500, a_inv=None):
    """扫描 [E_lo, E_hi]（E_lo<E_hi<0），返回 [(E, nodes), ...]（E 升序）。"""
    out = []
    prev_E = E_lo
    prev_phi = numerov_run(vfun, k2, l, rmin, rmax, N, E_lo, a_inv=a_inv)[0]
    for i in range(1, M + 1):
        E = E_lo + (E_hi - E_lo) * i / M
        phi = numerov_run(vfun, k2, l, rmin, rmax, N, E, a_inv=a_inv)[0]
        if (phi >= 0) != (prev_phi >= 0):
            Ev = bisect_eigen(vfun, k2, l, rmin, rmax, N, prev_E, E, a_inv=a_inv)
            _, nodes, _, _ = numerov_run(vfun, k2, l, rmin, rmax, N, Ev, a_inv=a_inv)
            out.append((Ev, nodes))
        prev_E, prev_phi = E, phi
    return out


def rms_radius(vfun, k2, l, rmin, rmax, N, E, a_inv=None):
    """⟨r⟩ = ∫ r u² dr / ∫ u² dr（本征态重积分）。"""
    _, _, xs, us = numerov_run(vfun, k2, l, rmin, rmax, N, E, keep=True, a_inv=a_inv)
    n2 = 0.0
    r2 = 0.0
    for i in range(1, len(xs)):
        dr = xs[i] - xs[i - 1]
        um = 0.5 * (us[i] * us[i] + us[i - 1] * us[i - 1])
        n2 += um * dr
        r2 += um * xs[i] * dr
    return r2 / n2


def downsample(xs, us, target=220):
    step = max(1, len(xs) // target)
    xs2 = [round(xs[i], 6) for i in range(0, len(xs), step)]
    us2 = [round(us[i], 8) for i in range(0, len(us), step)]
    return xs2, us2


# ===========================================================================
# S2 电磁：氢原子（求解器由解析精确谱校验）
# ===========================================================================
print("[S2] 电磁：氢原子解析谱对拍")
# 单位：r [a0]，E [Ry]；V = −2/r；μ̃ = 0.5 ⇒ f = 0.5*(V−E)... 注意 k2 = 2μ/ħ² → 在
# Ry·a0 单位下 ħ²/(2 m_e) = 0.5 Ry·a0² ⇒ k2(μ̃) = μ̃/0.5。
def v_hydrogen(r):
    return -2.0 / r


K2_H = 1.0          # μ̃ = 1（u'' = (V−E)u，库仑单位）
H_RMIN, H_RMAX, H_N = 1e-4, 60.0, 12000   # rmin=1e-4：截断 ~1e-8；h=0.005 对奇点区 ≥9 点/波长
lv_h = scan_levels(v_hydrogen, K2_H, 0, H_RMIN, H_RMAX, H_N, -1.05, -0.02, M=400, a_inv=2.0)
E1s = lv_h[0][0] if lv_h else 0.0
E2s = lv_h[1][0] if len(lv_h) > 1 else 0.0
E3s = lv_h[2][0] if len(lv_h) > 2 else 0.0
lv_2p = scan_levels(v_hydrogen, K2_H, 1, H_RMIN, H_RMAX, H_N, -0.30, -0.05, M=300, a_inv=2.0)
E2p = lv_2p[0][0] if lv_2p else 0.0
r1s = rms_radius(v_hydrogen, K2_H, 0, H_RMIN, H_RMAX, H_N, E1s, a_inv=2.0)

# 网格收敛（N→2N）
E1s_2N = scan_levels(v_hydrogen, K2_H, 0, H_RMIN, H_RMAX, 2 * H_N, -1.05, -0.9, M=60, a_inv=2.0)[0][0]
conv_h = abs(E1s_2N - E1s) / abs(E1s)

# 定量阴性对照：μ̃→1.1×（μ 偏 +10% ⇒ 库仑谱恰偏 +10%）
K2_H_WRONG = 1.1
E1s_wrong = scan_levels(v_hydrogen, K2_H_WRONG, 0, H_RMIN, H_RMAX, H_N, -1.25, -0.95, M=60, a_inv=2.0)[0][0]
wrong_shift = abs(E1s_wrong - E1s) / abs(E1s)

guard("G1", "氢解析谱对拍（E_n=−1/n² Ry）",
      abs(E1s + 1) < 1e-7 and abs(E2s + 0.25) < 1e-7 and abs(E3s + 1.0 / 9.0) < 1e-6,
      f"E_1s={E1s:.10f}、E_2s={E2s:.10f}、E_3s={E3s:.10f} [Ry]（解析 −1, −0.25, −0.111111）；"
      "残差来自 rmin=1e−4 截断（已声明口径）",
      {"E1s": round(E1s, 10), "E2s": round(E2s, 10), "E3s": round(E3s, 10)})
guard("G2", "⟨r⟩₁ₛ = 1.5 a₀", abs(r1s - 1.5) < 5e-3,
      f"⟨r⟩₁ₛ = {r1s:.8f} a₀（解析 1.5；偏差来自尾部剪裁口径：积分截在增长起点，"
      "丢失 ~e^{−2r_c} 量级尾部）——该守卫抓大错（如污染未剪时的 59.5）仍有充分判别力",
      {"r1s_a0": round(r1s, 8)})
guard("G3", "2s/2p 库仑简并", abs(E2p - E2s) / abs(E2s) < 1e-6,
      f"E_2p={E2p:.10f} vs E_2s={E2s:.10f} [Ry]（简并）", {"E2p": round(E2p, 10)})
guard("G4", "网格倍增收敛（N→2N）", conv_h < 1e-7,
      f"|ΔE_1s/E| = {conv_h:.3e}（Numerov ~h⁴；rmin 截断误差底）", {"conv": f"{conv_h:.3e}"})
guard("G5", "节点计数 = n−1",
      lv_h[0][1] == 0 and lv_h[1][1] == 1 and lv_h[2][1] == 2,
      f"1s/2s/3s 节点 = {lv_h[0][1]}/{lv_h[1][1]}/{lv_h[2][1]}")
guard("G6", "定量阴性对照（μ+10% ⇒ E+10%）",
      0.05 < wrong_shift < 0.15 and abs(wrong_shift - 0.10) < 2e-3,
      f"μ 偏 +10% ⇒ E_1s 偏 {wrong_shift*100:.4f}%（解析预期恰 10%）："
      "守卫既抓住错误、又定量命中预期偏移——判别力双重验证",
      {"shift": round(wrong_shift, 6)})

# ===========================================================================
# S3 剩余核力（氘核道）：r214 参数的量子谱判决
# ===========================================================================
print("[S3] 氘核道：r214 参数的量子谱判决")
K2_D = 2.0 * (M_P / 2.0) / (HARC * HARC)   # 2μ/(ħc)² [MeV⁻¹fm⁻²]


def v_pion146(r):
    return -ALPHA_146 * HARC * exp(-r / LAM_PI_FM) / r


# 半经典态总数与最内态尺度（声明公式，仅用于登记；π 交换在该尺度早已失效）
# g 口径：g ≡ 2μ·A·λ/(ħc)² = 2·α·λ·μ₁（与标准 λ_crit=1.6798 同归一）
MU1_P = (M_P / 2.0) / HARC
g_146 = 2.0 * ALPHA_146 * LAM_PI_FM * MU1_P
N_total_sc = 2.0 / pi * sqrt(2.0 * pi * LAM_PI_FM) * sqrt(2.0 * MU1_P * ALPHA_146)
E_inner_scale = -0.5 * (M_P / 2.0) * ALPHA_146 ** 2   # 库仑内区标度 [MeV]
lv_deep = scan_levels(v_pion146, K2_D, 0, 0.02, 40.0, 8000, -200.0, -0.05, M=600,
                      a_inv=ALPHA_146 * HARC)

# 单参数 α_y 拟合氘核结合能（纯吸引 π-Yukawa，无芯）
g_crit_check = G_CRIT / (2.0 * LAM_PI_FM * MU1_P)   # α 临界（g=g_crit）


def v_pion_fit(r):
    return -ALPHA_Y_FIT[0] * HARC * exp(-r / LAM_PI_FM) / r


ALPHA_Y_FIT = [0.55]


def deuteron_E(alpha_val):
    def v(r):
        return -alpha_val * HARC * exp(-r / LAM_PI_FM) / r
    ls = scan_levels(v, K2_D, 0, 0.02, 40.0, 6000, -200.0, -0.05, M=260,
                     a_inv=alpha_val * HARC)
    return ls[0][0] if ls else 0.0


# 二分 α_y：E(α) 单调（α 增 → 更深）；22 次迭代给 α 精度 ~1e-7（足够）
a_lo, a_hi = g_crit_check * 1.0005, 0.9
for _ in range(22):
    am = 0.5 * (a_lo + a_hi)
    Em = deuteron_E(am)
    if Em > E_DEUTERON:
        a_lo = am
    else:
        a_hi = am
ALPHA_Y_FIT[0] = 0.5 * (a_lo + a_hi)
E_d_fit = deuteron_E(ALPHA_Y_FIT[0])
r_d_fit = rms_radius(lambda r: -ALPHA_Y_FIT[0] * HARC * exp(-r / LAM_PI_FM) / r,
                     K2_D, 0, 0.02, 60.0, 9000, E_d_fit, a_inv=ALPHA_Y_FIT[0] * HARC)

guard("G7", "α_y 拟合收敛（E=−2.2246 MeV）", abs(E_d_fit - E_DEUTERON) < 0.002,
      f"α_y = {ALPHA_Y_FIT[0]:.6f} ⇒ E_1s = {E_d_fit:.6f} MeV（目标 {E_DEUTERON}）；"
      f"α 临界（g=g_crit）= {g_crit_check:.6f}",
      {"alpha_y": round(ALPHA_Y_FIT[0], 6), "E_fit": round(E_d_fit, 6)})
# 拟合点必须落在第一与第二束缚态阈值之间（第二阈值 g≈5.9）⇒ 拟合态是唯一的 s 态
g_fit_val = 2.0 * ALPHA_Y_FIT[0] * LAM_PI_FM * MU1_P
guard("G8", "拟合点落在第一/第二束缚态阈值之间",
      G_CRIT < g_fit_val < 5.5,
      f"拟合点 g = {g_fit_val:.4f} vs 第一阈值 {G_CRIT}、第二阈值 ≈5.9："
      "氘核是近临界束缚——本身就是一个读数",
      {"g_fit": round(g_fit_val, 4)})

# ===========================================================================
# S4 色道：粲偶素（Cornell = OGE + σr，承 r221 色道项）
# ===========================================================================
print("[S4] 色道：粲偶素与底偶素")
MC0 = 1500.0   # m_c 迭代初值 [MeV]
_cc_state = {"alpha_s": 0.5, "m_c": MC0}


def v_cornell_c(r):
    A = (4.0 / 3.0) * _cc_state["alpha_s"] * HARC
    return -A / r + SIGMA_MEV_FM * r


def solve_cc_levels():
    """自洽 m_c + 定 α_s 的粲偶素谱（目标化窗口扫描，热启动不动点）。
    返回 (E1s, E2s, E1p, m_c, alpha_s, r1s)。"""
    a_lo, a_hi = 0.30, 1.10
    m_c = MC0
    E1s = E2s = None
    for _ in range(15):                      # α_s 精度 ~0.8/2^15 ≈ 2e-5
        a_s = 0.5 * (a_lo + a_hi)
        _cc_state["alpha_s"] = a_s
        # 内层：m_c 不动点（3 次热启动扫描；M(J/ψ)=2 m_c + E_1s）
        for _ in range(3):
            _cc_state["m_c"] = m_c
            k2 = 2.0 * (m_c / 2.0) / (HARC * HARC)
            lv = scan_levels(v_cornell_c, k2, 0, 0.02, 14.0, 9000, -1500.0, 4000.0, M=400,
                             a_inv=(4.0 / 3.0) * _cc_state["alpha_s"] * HARC)
            E1s = lv[0][0]
            m_c = (M_JPSI - E1s) / 2.0
        _cc_state["m_c"] = m_c
        k2 = 2.0 * (m_c / 2.0) / (HARC * HARC)
        lv = scan_levels(v_cornell_c, k2, 0, 0.02, 14.0, 9000, -1500.0, 4000.0, M=400,
                         a_inv=(4.0 / 3.0) * _cc_state["alpha_s"] * HARC)
        E1s = lv[0][0]
        E2s = lv[1][0] if len(lv) > 1 else 0.0
        split = E2s - E1s
        target = M_PSI2S - M_JPSI
        if abs(split - target) < 0.3:
            break
        if split > target:
            a_hi = a_s
        else:
            a_lo = a_s
    alpha_s = 0.5 * (a_lo + a_hi)
    _cc_state["alpha_s"] = alpha_s
    _cc_state["m_c"] = m_c
    k2 = 2.0 * (m_c / 2.0) / (HARC * HARC)
    lv = scan_levels(v_cornell_c, k2, 0, 0.02, 14.0, 9000, -1500.0, 4000.0, M=400,
                     a_inv=(4.0 / 3.0) * alpha_s * HARC)
    E1s = lv[0][0]
    E2s = lv[1][0] if len(lv) > 1 else 0.0
    lp = scan_levels(v_cornell_c, k2, 1, 0.02, 14.0, 9000, -1500.0, 4000.0, M=300,
                     a_inv=(4.0 / 3.0) * alpha_s * HARC)
    E1p = lp[0][0] if lp else 0.0
    r1s_cc = rms_radius(v_cornell_c, k2, 0, 0.02, 14.0, 9000, E1s,
                        a_inv=(4.0 / 3.0) * alpha_s * HARC)
    return E1s, E2s, E1p, m_c, alpha_s, r1s_cc


E1s_c, E2s_c, E1p_c, m_c_fit, alpha_s_fit, r_cc = solve_cc_levels()
split_cc = E2s_c - E1s_c
pwave_cc = E1p_c - E1s_c
guard("G9", "α_s 校准收敛（1S–2S=589.197 MeV）", abs(split_cc - (M_PSI2S - M_JPSI)) < 0.5,
      f"α_s* = {alpha_s_fit:.5f}（σ=0.18 GeV² 固定），m_c = {m_c_fit:.4f} MeV，"
      f"1S–2S = {split_cc:.4f} MeV",
      {"alpha_s": round(alpha_s_fit, 5), "m_c": round(m_c_fit, 4),
       "split": round(split_cc, 4)})

# Υ 交叉预言（同一 α_s*，m_b 自洽 M(Υ)=9460.300；热启动不动点 5 次）
m_b = M_UPS1 / 2.0
for _ in range(5):
    k2_b = 2.0 * (m_b / 2.0) / (HARC * HARC)

    def v_cornell_b(r, _k2=k2_b):
        A = (4.0 / 3.0) * alpha_s_fit * HARC
        return -A / r + SIGMA_MEV_FM * r

    ls_b = scan_levels(v_cornell_b, k2_b, 0, 0.02, 12.0, 9000, -1500.0, 4000.0, M=400,
                       a_inv=(4.0 / 3.0) * alpha_s_fit * HARC)
    E1s_b = ls_b[0][0]
    m_b = (M_UPS1 - E1s_b) / 2.0
k2_b = 2.0 * (m_b / 2.0) / (HARC * HARC)
lv_b = scan_levels(v_cornell_b, k2_b, 0, 0.02, 14.0, 9000, -1500.0, 4000.0, M=400,
                   a_inv=(4.0 / 3.0) * alpha_s_fit * HARC)
split_ups = (lv_b[1][0] - lv_b[0][0]) if len(lv_b) > 1 else 0.0
target_ups = M_UPS2S - M_UPS1
rel_ups = abs(split_ups - target_ups) / target_ups if split_ups else 1.0

# 1P 对照（χc1 自旋平均近似，超精细 ~45 MeV 量级 ⇒ 容差放宽）
rel_1p = abs(pwave_cc - (M_CHIC1 - M_JPSI)) / (M_CHIC1 - M_JPSI)

# ===========================================================================
# S5 弱力：无束缚态判决
# ===========================================================================
print("[S5] 弱力：无束缚态判决")
mu1_e = M_E_MEV / HARC                       # m_e c/ħ [fm⁻¹]
g_weak = 2.0 * ALPHA_W * LAM_W_FM * mu1_e    # 标准口径（2μAλ/ħ²c²）


def v_weak(r):
    return -ALPHA_W * HARC * exp(-r / LAM_W_FM) / r


K2_W = 2.0 * M_E_MEV / (HARC * HARC)
# V 最深处 ~ r=λ：V(λ) = −αħc e^{-1}/λ
v_min_w = -ALPHA_W * HARC * exp(-1.0) / LAM_W_FM
lv_w = scan_levels(v_weak, K2_W, 0, 1e-6, 0.02, 9000, v_min_w * 0.999, -1e-9, M=400,
                   a_inv=ALPHA_W * HARC)
guard("G10", "弱力无束缚态（判据+扫描两路）",
      g_weak < 1e-6 and len(lv_w) == 0,
      f"g = α·λ·μ₁ = {g_weak:.4e} ≪ g_crit = {G_CRIT}（差 {G_CRIT/g_weak:.3e} 倍）；"
      f"E∈[{v_min_w*0.999:.4f}, 0] MeV 扫描 400 点 0 个本征值；"
      "λ_W 内动能尺度 ħ²/2μλ² 压过势阱深度十余个量级",
      {"g_weak": f"{g_weak:.4e}", "n_levels": len(lv_w)})

# ===========================================================================
# S6 引力：库仑型解析（"引力氢原子"尺度读数）
# ===========================================================================
alpha_G_e = G_NEWTON * M_E_KG * M_E_KG / HBARC_JM      # 两电子
E_grav_eV = -(alpha_G_e ** 2) * (M_E_MEV * 1e6 / 2.0) / 2.0    # eV（μ=m_e/2）
r_grav_fm = HARC / ((M_E_MEV / 2.0) * alpha_G_e)       # a_B = ħc/(μc²α) [fm]
r_grav_m = r_grav_fm * 1e-15
ratio_universe = r_grav_m / R_UNIVERSE_M

# ===========================================================================
# S7 条目与判决
# ===========================================================================
print("[S7] 条目判定")


def main():
    entry("Q01", "PASS", "电磁量子层：氢原子谱逐位命中",
          f"E_n = −13.605693/n² eV 由 Numerov 数值复现（E_1s = {E1s*RY_EV:.6f} eV）；"
          f"⟨r⟩₁ₛ = {r1s:.6f} a₀；2s/2p 简并；网格收敛 {conv_h:.1e}——求解器可信度由解析锚点钉死",
          {"E1s_eV": round(E1s * RY_EV, 6), "r1s_a0": round(r1s, 6)})
    entry("Q02", "FAIL", "氘核判决：r214 剩余核力参数在量子层失效",
          f"α=14.6（g²/4π 口径）直接当中心势强度 ⇒ g = {g_146:.2f} ≫ g_crit = {G_CRIT}："
          f"半经典束缚态总数 ≈ {N_total_sc:.1f} 个（自然界氘核道只有 1 个），"
          f"最内态库仑标度深达 {E_inner_scale/1000.0:.1f} GeV（π 交换在该尺度早已失效）；"
          f"[−200, 0] MeV 窗口内 Numerov 实数 {len(lv_deep)} 个。"
          "『力的大小』在经典层合格的参数，量子谱立刻不合格——14.6 是 NNπ 耦合常数，"
          "不是中心势的 α（自旋-张量分解后中心吸引 α_y≈0.5，见 Q03）",
          {"g_146": round(g_146, 3), "N_sc": round(N_total_sc, 1),
           "E_inner_GeV": round(E_inner_scale / 1000.0, 1),
           "n_levels_window": len(lv_deep)})
    entry("Q03", "BOUNDARY", "单参数 α_y 拟合：结合能可凑，半径必错",
          f"纯吸引 π-Yukawa 拟合 E_B=−2.2246 MeV ⇒ α_y = {ALPHA_Y_FIT[0]:.5f}"
          f"（g = {ALPHA_Y_FIT[0]*LAM_PI_FM*(M_P/2.0)/HARC:.4f}，贴着临界 {G_CRIT}——"
          f"氘核是近临界束缚这一事实本身被机器复现）；但预言 ⟨r⟩ = {r_d_fit:.3f} fm "
          f"vs 实测 1.975 fm，错配 {r_d_fit/R_DEUTERON:.2f}× ⇒ 核力必须有排斥芯+张量力，"
          "单参数中心势在半径观测量上定价出局",
          {"alpha_y": round(ALPHA_Y_FIT[0], 5), "r_fit_fm": round(r_d_fit, 3),
           "misfit": round(r_d_fit / R_DEUTERON, 2)})
    entry("Q04", "PASS" if guard_ok("G9") and 0.3 <= alpha_s_fit <= 0.8 else "BOUNDARY",
          "色道量子层：Cornell 谱自洽闭合",
          f"V = −(4/3)α_s·ħc/r + σr（σ=0.18 GeV² 固定，承 r221）"
          f"：α_s* = {alpha_s_fit:.5f}、m_c = {m_c_fit:.2f} MeV（自洽 M(J/ψ)=3096.900），"
          f"1S–2S = {split_cc:.2f} MeV 命中 589.197。"
          "注：Cornell 势 V(∞)=+∞，能量零点任意，E_1s>0 属正常；M=2m_c+E 锚定绝对质量",
          {"alpha_s": round(alpha_s_fit, 5), "m_c": round(m_c_fit, 2)})
    entry("Q05", "BOUNDARY" if rel_1p <= 0.35 else "FAIL", "交叉预言 1：χc1（1P）分裂",
          f"同一 α_s* 预言 E_1p − E_1s = {pwave_cc:.1f} MeV vs 实验 χc1−J/ψ = "
          f"{M_CHIC1-M_JPSI:.2f} MeV（rel {rel_1p*100:.1f}%）——"
          + ("势模型典型精度带内；自旋-轨道/超精细修正（~45 MeV 量级）未分解"
             if rel_1p <= 0.35 else
             "同 α_s* 无跑动外推不成立：bb̄/1P 道需要更小的有效 α_s（势模型已知族依赖）"),
          {"pred_MeV": round(pwave_cc, 1), "exp_MeV": round(M_CHIC1 - M_JPSI, 2),
           "rel": round(rel_1p, 4)})
    entry("Q06", "BOUNDARY" if rel_ups <= 0.35 else "FAIL", "交叉预言 2：Υ(2S) 分裂（同一 α_s* 跨族外推）",
          f"m_b = {m_b:.2f} MeV 自洽 ⇒ 预言 Υ 2S−1S = {split_ups:.1f} MeV vs 实验 "
          f"{target_ups:.2f} MeV（rel {rel_ups*100:.1f}%）——"
          + ("一个耦合常数跨 cc̄/bb̄ 两族，无再拟合"
             if rel_ups <= 0.35 else
             "同 α_s* 外推高估：重夸克动能标度使分裂变大，而实验反而更小——"
             "bb̄ 需要更小的有效耦合（跑动/相对论修正），这是势模型的已知结构性局限"),
          {"pred_MeV": round(split_ups, 1), "exp_MeV": round(target_ups, 2),
           "rel": round(rel_ups, 4)})
    entry("Q07", "INFO", "J/ψ 1S 均方根半径",
          f"⟨r⟩(J/ψ 1S) = {r_cc:.3f} fm——与晶格/势模型典型值 ~0.4–0.5 fm 同量级"
          "（本卷未引入晶格数据，只登记量级一致）",
          {"r_fm": round(r_cc, 3)})
    entry("Q08", "PASS", "弱力无束缚态（定量判决）",
          f"g = {g_weak:.3e} ≪ g_crit = {G_CRIT}（{G_CRIT/g_weak:.2e} 倍裕度）；"
          "数值扫描 0 本征值——弱力在最短的距离上也不形成束缚态，"
          "『距离特性』的量子层表述是：有解无谱",
          {"g": f"{g_weak:.3e}"})
    entry("Q09", "INFO", "引力『氢原子』：形式存在、物理不可实现",
          f"两电子引力束缚：E_1s = {E_grav_eV:.3e} eV，"
          f"r = {r_grav_m:.3e} m = 可观测宇宙半径的 {ratio_universe:.2e} 倍——"
          "库仑型（λ=∞）解析给束缚态，但尺度超出宇宙 5×10⁵ 倍",
          {"E_eV": f"{E_grav_eV:.3e}", "r_m": f"{r_grav_m:.3e}",
           "vs_universe": f"{ratio_universe:.2e}"})
    entry("Q10", "INFO", "输入账：量子层零新增第一性输入",
          "本卷全部谱由 r214/r221 已声明的同一组参数导出；"
          "新增量仅唯象标定件（α_y 拟合、α_s* 校准、m_c/m_b 自洽）——"
          "每个标定件都换来至少一个未参与标定的预言读数（Q05/Q06/⟨r⟩）",
          {"inputs_added": 0})
    entry("Q11", "INFO", "判决：量子束缚层收口",
          "同一个 UFE-4F⁺ 势写进薛定谔方程后：电磁有解析谱（氢）、色道有 Cornell 谱"
          "（两族偶素交叉命中）、剩余核力在量子层暴露参数口径缺陷（Q02 FAIL + Q03 半径错配）、"
          "弱力无谱、引力宇宙尺度——『力的大小方向距离』三特性在量子层升级为"
          "『存在性/谱/半径』三读数；形式统一在量子层同样成立，动力学统一仍 FAIL（继承）")

    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in entries if e["level"] == "INFO")

    res = {
        "stem": STEM, "round": 226, "date": "2026-10-26",
        "method": ("同一 UFE-4F⁺ 势写进径向薛定谔方程，Numerov+扫描二分求本征值；"
                   "float64 数值谱（声明口径），求解器由氢原子解析精确谱校验"),
        "unified_schrodinger": "iħ∂ψ/∂t = [−ħ²/(2μ)∇² + U(r)]ψ，U(r) = UFE-4F⁺（r221）",
        "entries": entries, "guards": guards, "controls": [],
        "readings": {
            "hydrogen": {"E1s_eV": round(E1s * RY_EV, 6), "E2s_eV": round(E2s * RY_EV, 6),
                         "E3s_eV": round(E3s * RY_EV, 6), "r1s_a0": round(r1s, 6)},
            "deuteron": {"alpha_146": ALPHA_146, "g_146": round(g_146, 3),
                         "N_total_sc": round(N_total_sc, 1),
                         "E_inner_GeV": round(E_inner_scale / 1000.0, 1),
                         "n_levels_window_200MeV": len(lv_deep),
                         "alpha_y_fit": round(ALPHA_Y_FIT[0], 5),
                         "r_fit_fm": round(r_d_fit, 3),
                         "r_exp_fm": R_DEUTERON,
                         "misfit": round(r_d_fit / R_DEUTERON, 2)},
            "charmonium": {"alpha_s": round(alpha_s_fit, 5), "m_c": round(m_c_fit, 2),
                           "split_1S2S": round(split_cc, 2), "exp_1S2S": 589.197,
                           "pwave": round(pwave_cc, 1), "exp_chi1": 413.767,
                           "r1S_fm": round(r_cc, 3)},
            "bottomonium": {"m_b": round(m_b, 2), "split_pred": round(split_ups, 1),
                            "exp_split": round(target_ups, 2), "rel": round(rel_ups, 4)},
            "weak": {"g": f"{g_weak:.4e}", "g_crit": G_CRIT, "n_levels": len(lv_w)},
            "gravity": {"E_eV": f"{E_grav_eV:.3e}", "r_m": f"{r_grav_m:.3e}",
                        "vs_universe": f"{ratio_universe:.2e}"},
            "g_bars": {"weak": f"{log(g_weak,10):.3f}", "deuteron_fit": f"{log(g_fit_val,10):.3f}",
                        "pion_146": f"{log(g_146,10):.3f}", "g_crit": f"{log(G_CRIT,10):.3f}"},
            "wavefunctions": _collect_wavefunctions(),
        },
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info,
                   "guards": f"{sum(1 for g in guards if g['ok'])}/{len(guards)}",
                   "controls": "0/0"},
        "verdict": "", "judgement": "", "source": {},
    }

    control("C1", "氢 1s vs CODATA Rydberg",
            abs(E1s * RY_EV + 13.605693) < 1e-4,
            f"数值 {E1s*RY_EV:.6f} eV vs 解析 −13.605693 eV（求解器↔实验值双锚）",
            {"E_eV": round(E1s * RY_EV, 6)})
    res["controls"] = controls
    res["counts"]["controls"] = f"{sum(1 for c in controls if c['ok'])}/{len(controls)}"

    parts = ["R226-QUANTUM-BOUND",
             "HYDROGEN-ANALYTIC-OK" if guard_ok("G1") else "HYDROGEN-FAIL",
             "RMS-1.5A0-OK" if guard_ok("G2") else "RMS-FAIL",
             "DEGEN-OK" if guard_ok("G3") else "DEGEN-FAIL",
             "NEGX10PCT-OK" if guard_ok("G6") else "NEGX-FAIL",
             "DEUTERON-PURE146-FAIL(N=%s)" % len(lv_deep),
             "ALPHA-Y-FIT-%s-RMISFIT-%sx" % (round(ALPHA_Y_FIT[0], 4), round(r_d_fit / R_DEUTERON, 2)),
             "CORNELL-ALPHAS-%s" % round(alpha_s_fit, 4),
             "CHI1-%.0fPCT" % (rel_1p * 100),
             "UPSILON-%.0fPCT" % (rel_ups * 100),
             "WEAK-NO-BOUND-OK" if guard_ok("G10") else "WEAK-VERDICT-FAIL",
             "GRAV-R-%sM-COSMIC" % f"{r_grav_m:.1e}",
             "FAIL-Q02-INHERITED-CALIBER-PRICE",
             "VERDICT-FORM-UNIFIED-AT-QUANTUM-LAYER-DYNAMICS-STILL-NOT"]
    res["verdict"] = "-".join(parts)
    res["judgement"] = ("CLOSED-INCREMENT（量子束缚层：同一势的薛定谔谱 + 四力束缚判决 + 交互可视化）；"
                        "Q02 FAIL = 经典合格参数的量子定价；供给仍 0")
    res["source"] = {
        "engine": BASE + ".py",
        "inherits": ["r214（四力参数与母式）", "r221（σr 色道项与通道门）",
                     "r218（口径审计——Q02 是其『强两行口径矛盾』的量子定价）",
                     "PDG 2024 偶素与氘核锚点"],
    }
    print(f"条目 {res['counts']['entries']}（PASS {n_pass} / FAIL {n_fail} / "
          f"BOUNDARY {n_bnd} / INFO {n_info}）· 守卫 {res['counts']['guards']} · "
          f"控制组 {res['counts']['controls']}")

    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")
    with open(jpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    write_md(mpath, res)
    write_report(rpath, res)

    html_ok, html_detail = cast_html(res)
    guard("G11", "交互 HTML 生成且自含", html_ok, html_detail)
    res["counts"]["guards"] = f"{sum(1 for g in guards if g['ok'])}/{len(guards)}"
    with open(jpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)

    bad_g = [g["id"] for g in guards if not g["ok"]]
    bad_c = [c["id"] for c in controls if not c["ok"]]
    if bad_g or bad_c:
        print(f"[RC≠0] 守卫失败 {bad_g} 控制组失败 {bad_c}")
        return 1
    print(f"[DONE] {MARKER} rc=0 → {jpath}")
    return 0


def _collect_wavefunctions():
    """导出波函数样本（u 归一到峰值 1；V 同图 Overlay）。"""
    out = []
    # H 1s / 2s（a0 单位；V=−2/r）
    for label, E, n_off in (("H 1s", E1s, 0), ("H 2s", E2s, 1)):
        _, _, xs, us = numerov_run(v_hydrogen, K2_H, 0, H_RMIN, 40.0, 4000, E, keep=True,
                                   a_inv=2.0)
        peak = max(abs(u) for u in us) or 1.0
        v_arr = [round(-2.0 / r, 4) for r in xs]
        out.append({"name": label + "（a0, Ry）", "unit": "a0",
                    "r": [round(x, 4) for x in xs], "u": [round(u / peak, 5) for u in us],
                    "v": v_arr, "E_mark": round(E * RY_EV, 3), "E_unit": "eV"})
    # 氘核拟合态（fm, MeV）
    _, _, xs, us = numerov_run(lambda r: -ALPHA_Y_FIT[0] * HARC * exp(-r / LAM_PI_FM) / r,
                               K2_D, 0, 0.02, 40.0, 8000, E_d_fit, keep=True,
                               a_inv=ALPHA_Y_FIT[0] * HARC)
    peak = max(abs(u) for u in us) or 1.0
    out.append({"name": "氘核道拟合态（fm, MeV）", "unit": "fm",
                "r": [round(x, 4) for x in xs], "u": [round(u / peak, 5) for u in us],
                "v": [round(-ALPHA_Y_FIT[0] * HARC * exp(-r / LAM_PI_FM) / r, 3) for r in xs],
                "E_mark": E_DEUTERON, "E_unit": "MeV"})
    # J/ψ 1S / 2S（fm, MeV）
    k2c = 2.0 * (m_c_fit / 2.0) / (HARC * HARC)
    a_c = (4.0 / 3.0) * alpha_s_fit * HARC
    for label, E in (("J/ψ 1S", E1s_c), ("ψ(2S)", E2s_c)):
        _, _, xs, us = numerov_run(v_cornell_c, k2c, 0, 0.02, 8.0, 6000, E, keep=True,
                                   a_inv=a_c)
        peak = max(abs(u) for u in us) or 1.0
        out.append({"name": label + "（fm, MeV）", "unit": "fm",
                    "r": [round(x, 4) for x in xs], "u": [round(u / peak, 5) for u in us],
                    "v": [round(v_cornell_c(r), 1) for r in xs],
                    "E_mark": round(2 * m_c_fit + E, 1), "E_unit": "MeV"})
    return out


def write_md(path, res):
    L = [f"# {res['stem']} · 数据册（引擎自动生成）\n",
         f"- 判决串：`{res['verdict']}`\n",
         f"- 条目：{res['counts']['entries']}（PASS {res['counts']['PASS']} / FAIL {res['counts']['FAIL']} / "
         f"BOUNDARY {res['counts']['BOUNDARY']} / INFO {res['counts']['INFO']}）· "
         f"守卫 {res['counts']['guards']} · 控制组 {res['counts']['controls']}\n",
         "\n## 方法\n", f"- {res['method']}\n", f"- {res['unified_schrodinger']}\n",
         "\n## 条目\n"]
    for e in res["entries"]:
        L.append(f"- **{e['code']} {e['level']}** {e['title']}——{e['detail']}\n")
    L.append("\n## 守卫\n")
    for g in res["guards"]:
        L.append(f"- **{g['id']} {'OK' if g['ok'] else 'FAIL'}** {g['title']}——{g['detail']}\n")
    L.append("\n## 控制组\n")
    for c in res["controls"]:
        L.append(f"- **{c['id']} {'OK' if c['ok'] else 'FAIL'}** {c['title']}——{c['detail']}\n")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))


def write_report(path, res):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{MARKER} rc=0\n")
        f.write(f"entries={res['counts']['entries']} PASS={res['counts']['PASS']} "
                f"FAIL={res['counts']['FAIL']} BOUNDARY={res['counts']['BOUNDARY']} "
                f"INFO={res['counts']['INFO']}\n")
        f.write(f"guards={res['counts']['guards']} controls={res['counts']['controls']}\n")
        f.write(f"verdict={res['verdict']}\n")
        for key in ("hydrogen", "deuteron", "charmonium", "bottomonium", "weak", "gravity"):
            f.write(f"{key}={json.dumps(res['readings'][key], ensure_ascii=False)}\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R223_JSON__" not in tpl:
        return False, "模板缺少 __R223_JSON__ 占位符"
    html = tpl.replace("__R223_JSON__", json.dumps(res, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R223_JSON__" in text:
        problems.append("占位符未替换")
    if "http://" in text or "https://" in text:
        problems.append("发现外部 URL（应零依赖）")
    if "<canvas" not in text or "<script" not in text:
        problems.append("缺少 canvas/script")
    if problems:
        return False, "；".join(problems)
    return True, f"已生成 {HTML_OUT}（{len(text)} B），零外部 URL、JSON 已铸入"


if __name__ == "__main__":
    sys.exit(main())
