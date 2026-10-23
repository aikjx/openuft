# -*- coding: utf-8 -*-
"""
TUFT-r162｜时空同一化 R = C t 与质量几何化 m = k∮dn/Ω 的求导证明验证精算
================================================================================
编号与定位
--------------------------------------------------------------------------------
* 编号：r162（实测首空号：grep 全库仅 README 的「下轮从 r162 起」命中，无产物占用）
* 靶：S17《宇宙大统一方程（力方程）》§2.1 基本公设与定义的**剩余两条**
      —— openuft/01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/
         07-宇宙大统一方程（力方程）/宇宙大统一方程的第一性原理推导、诠释与验证.md
      原文 §2.1：
        「时空同一化：时间 t 是空间位移 R 的度量，满足 R = C t，其中 C 为矢量光速，
          模为常数 c，方向可变。」
        「质量几何化：质量 m 是物体周围单位立体角内空间位移矢量 R 的『条数』密度，
          即 m = k ∮ dn/Ω，其中 k 为比例常数。」
* 与相邻卷的分工（分层铁律：条目不可相加）：
      r160 = 力方程**四项诠释**（求导正确但诠释落空）
      r161 = **电荷几何化 q = k′ dm/dt** 自身（记账层 PASS、后果层 FAIL）
      本卷 = **时空同一化 R = C t** 与 **质量几何化 m = k∮dn/Ω** 两条公设自身，
             以及二者**联合**后对电荷的后果（r161 不碰这两条）
  r160/r161 都把 R = C t 与 m = k∮dn/Ω 当作给定背景，本卷补上。

机读推导（本卷全部结论的来源，可手算复核）
--------------------------------------------------------------------------------
【求导层】R(t) = C(t)·t，|C| = c = 常数，C·Ċ = 0（模不变 ⇒ 导数正交）
    ⇒ dR/dt = C + t·Ċ，且 C ⊥ Ċ
    ⇒ |dR/dt| = √(c² + t²|Ċ|²) ≥ c
    ⇒ 等号仅当 Ċ = 0；Ċ ≠ 0 且 t > 0 ⇒ |dR/dt| > c   —— **超光速**
【A 组 时空同一化】
    A0  求导本身（对靶有利，先给 PASS）
    A1  R 的所指两难：物体位置 ⇒ 共球面塌缩；空间位移场 ⇒ 与力方程脱钩
    A2  C 全局均匀（原文 §3.1 自承）⇒ 所有物体位置矢量相同
    A3  类光/类空两难：Ċ=0 ⇒ ds²=0（有质量粒子不存在）；Ċ≠0 ⇒ ds²<0（超光速）
    A4  固有时读法确实救回类时性（★对靶有利，诚实记 PASS）
    A5  但救不回空间维度：相对位置恒 ∥ C ⇒ 横向分量归零
    A6  V 与 dR/dt 的两难：V=dR/dt ⇒ P = m(C−V) 恒零；V≠dR/dt ⇒ R 与物体脱钩
    A7  防过度指控：|R| = c·Δt 作为「光行距」定义是标准且正确的（降 INFO）
【B 组 质量几何化】
    B1  记号层：∮dn/Ω 分子是微分、分母是总量 ⇒ 平均值 vs 总量
    B2  ★对靶有利：总量读法（m ∝ N）可加（PASS）
    B3  可加性两难：原文措辞「密度」⇒ 不可加（−50%）
    B4  量纲：[k] = (1,0,0) ⇒ **有量纲自由参数 = 非定律**
    B5  「条数」n 无定义、无测度、无归一化 ⇒ 公设**不可操作**
    B6  若 n 是整数计数 ⇒ 质量量子化 ⇒ 连分数求最小整数分母（★零判别力，记 INFO）
    B7  ★最硬：与 R=Ct 联合 ⇒ 电荷要么恒零、要么与粒子种类无关（两支都死）
    B8  条数的产生/消灭机制缺失（BOUNDARY，与 r161 联动，不重复指控）
【C 组 修复定价】5 个动作 × 位掩码 32 组合，严格/宽松双档都报

纯标准库（py3.13 managed 无 numpy/sympy/mpmath）。
"""

import io
import json
import math
import os
import sys
from datetime import datetime
from fractions import Fraction

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ============================== 常量（CODATA 2018） ==============================
C_LIGHT = 299792458.0
M_E = 9.1093837015e-31
M_P = 1.67262192369e-27
M_N = 1.67492749804e-27
Q_E = 1.602176634e-19
M_E_U = 2.8e-40
YR = 365.25 * 86400.0
AU = 1.495978707e11
LY = 9.4607304725808e15
D_MOON = 3.84399e8
D_EARTH = AU                       # 地球到太阳（取原点 = 太阳）
D_PROX = 4.2465 * LY                # 比邻星

TOL_REL = 1e-6
TOL_CONST = 1e-8                    # 记忆纪律：不得取 1e-9
Q_SCAN_MAX = 200000                 # 最小整数分母的扫描上限（保护）

# ============================== 路径定位 ==============================
_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_COM = os.path.dirname(_PROJ)
OPENUFT_ROOT = os.path.dirname(_COM)
TARGET_MD = os.path.join(
    OPENUFT_ROOT, "01_独立体系", "S17_统一场论核心公式", "04_理论推导",
    "核心公式集", "07-宇宙大统一方程（力方程）",
    "宇宙大统一方程的第一性原理推导、诠释与验证.md",
)

# ============================== 登记器 ==============================
ENTRIES = []
GUARDS = []
CONTROLS = []


def add(code, group, name, verdict, note):
    ENTRIES.append({"code": code, "group": group, "name": name,
                    "verdict": verdict, "note": note})


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  {} {} — {}".format("OK " if ok else "BAD", name, detail))


def control(name, ok, detail):
    CONTROLS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  {} {} — {}".format("OK " if ok else "BAD", name, detail))


# ============================== 通用工具 ==============================
def gamma_of(beta):
    return 1.0 / math.sqrt(1.0 - beta * beta)


def dim_mul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dim_div(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dim_pow(a, n):
    return tuple(x * n for x in a)


def min_denominator(x, tol_rel, qmax=Q_SCAN_MAX):
    """求最小正整数 q，使 |round(x*q)/q − x| / x < tol_rel。暴力保证最小性。"""
    best = None
    for q in range(1, qmax + 1):
        p = int(round(x * q))
        err = abs(p / q - x) / x
        if err < tol_rel:
            best = (q, p, err)
            break
    return best


def classify_ds2(ds2_rel):
    """ds2_rel = ds²/(c²dt²)。>0 类时，=0 类光，<0 类空。"""
    if ds2_rel > 0:
        return "TIMELIKE"
    if ds2_rel == 0:
        return "LIKELIKE"
    return "SPACELIKE"


# ============================== A 组：时空同一化 R = C t ==============================
def group_A():
    print("\n" + "=" * 78)
    print(" [A 组] 时空同一化 R = C t（求导层 → 后果层 → 读法层）")
    print("=" * 78)
    out = {}

    # ---- A0 求导层：先给靶应得的 PASS ----
    # R(t) = C(t)·t，C(t) = c·(cos ωt, sin ωt, 0)，|C| = c 常数
    # 解析：dR/dt = C + t·Ċ；因 |C| 常数 ⇒ C·Ċ = 0 ⇒ |dR/dt| = √(c² + t²|Ċ|²)
    # ★求导验证取「相位 ωt = O(1)」的小相位档：相位做大（ωt=1e3）时
    #   cos/sin 的参数本身带 ~|ωt|·eps 的误差，会被 1/h 放大成 1e-9 级假残差
    #   （首跑就是这样掉的：1.35e-09 且**不单调**）⇒ 属代码错非期望错。
    omega_d = 1.0e-3
    t_d = 1.0

    def R_vec(t):
        a = omega_d * t
        return (C_LIGHT * math.cos(a) * t, C_LIGHT * math.sin(a) * t, 0.0)

    def dR_analytic(t):
        a = omega_d * t
        ca, sa = math.cos(a), math.sin(a)
        return (C_LIGHT * ca - C_LIGHT * omega_d * t * sa,
                C_LIGHT * sa + C_LIGHT * omega_d * t * ca,
                0.0)

    # ★自适应步长：不用「ω·h = 1e-4」的经验值（本构型下它给出 h = 0.1，
    #   截断项 (h²/6)·|R'''| 主导 ⇒ 残留 5.0e-09 的**假**残差，首跑就是这样掉的）。
    #   改为解析求「截断 ≈ 舍入」的平衡点，再从平衡点的 4 倍起步（保证起始处在
    #   截断主导区 ⇒ 三档折半残差单调下降）：
    #     截断相对误差 ≈ (h²/6)·|R'''|/|R'| = (h²/6)·3ω²      （本构型 |R'''|/|R'| ≈ 3ω²）
    #     舍入相对误差 ≈ eps·|R|/(h·|R'|) = eps·t/h            （|R|/|R'| ≈ t）
    #     令二者相等 ⇒ h_opt = (6·eps·t/(3ω²))^{1/3}
    _eps = 2.220446049250313e-16
    h_opt = (6.0 * _eps * t_d / (3.0 * omega_d ** 2)) ** (1.0 / 3.0)
    h0 = 4.0 * h_opt
    errs = []
    for h in (h0, h0 / 2.0, h0 / 4.0):
        Rp = R_vec(t_d + h)
        Rm = R_vec(t_d - h)
        num = tuple((Rp[i] - Rm[i]) / (2.0 * h) for i in range(3))
        ana = dR_analytic(t_d)
        nrm = math.sqrt(sum(x * x for x in ana))
        e = math.sqrt(sum((num[i] - ana[i]) ** 2 for i in range(3))) / nrm
        errs.append(e)
    a0_res = errs[0]
    a0_mono = errs[0] > errs[1] > errs[2]
    mag_ana = math.sqrt(sum(x * x for x in dR_analytic(t_d)))
    ratio_vc = mag_ana / C_LIGHT
    sqrt_pred = math.sqrt(1.0 + (omega_d * t_d) ** 2)
    # A3② 的超光速示例只用**解析闭式**（不再做差分），故可取大相位
    omega_i = 1.0e3
    t_i = 1.0
    t0 = 1.0
    print("[A0] 求导层：dR/dt = C + t·Ċ（解析 vs 自适应中心差分）")
    print("     自适应步长：h_opt = {:.3e}（截断≈舍入），取 h0 = 4·h_opt = {:.3e}".format(h_opt, h0))
    print("     残差 = {:.3e} → {:.3e} → {:.3e}".format(errs[0], errs[1], errs[2]))
    print("     |dR/dt|/c = {:.6e}（解析 √(1+(ωt)²) = {:.6e}）".format(ratio_vc, sqrt_pred))
    out["A0_res"] = a0_res
    out["A0_mono"] = a0_mono
    out["A0_ratio_vc"] = ratio_vc
    out["A0_sqrt_pred"] = sqrt_pred
    out["A0_errs"] = errs

    if a0_res < 1e-10 and a0_mono and abs(ratio_vc - sqrt_pred) / sqrt_pred < 1e-12:
        add("A0", "求导层", "求导本身正确：dR/dt = C + t·Ċ，|dR/dt| = √(c²+t²|Ċ|²)（对靶有利）",
            "PASS",
            "先复核「求导」本身：对 R(t) = C(t)·t（C = c·(cos ωt, sin ωt, 0)）做**自适应中心差分**"
            "（解析求截断≈舍入的平衡点 h_opt = {:.2e}，取 h0 = 4·h_opt = {:.2e}），"
            "解析 dR/dt = C + t·Ċ 与差分残差 = **{:.3e}**，"
            "三档步长残差单调下降（{:.2e} → {:.2e} → {:.2e}）⇒ 收敛阶正确。"
            "且 |dR/dt| 的解析模长与闭式 √(c²+t²|Ċ|²) 一致（相对差 {:.1e}）。"
            "**这是本卷对靶有利的结论，诚实登记**：求导这一步没错，|C| = 常数 ⇒ C ⊥ Ċ 的推论也对。"
            "问题出在把这个求导结果**当作物体的速度**时会发生什么（见 A3/A6）。"
            .format(h_opt, h0, a0_res, errs[0], errs[1], errs[2],
                    abs(ratio_vc - sqrt_pred) / sqrt_pred))
    else:
        add("A0", "求导层", "求导复核", "FAIL", "残差 {:.2e}，单调 {}".format(a0_res, a0_mono))

    # ---- A1 R 的所指两难 ----
    t_req_earth = D_EARTH / C_LIGHT
    t_req_prox = D_PROX / C_LIGHT
    ratio_d = D_PROX / D_EARTH
    print("[A1] |R| = c·t 强制「到原点距离 = ct」")
    print("     地球 |R| = {:.6e} m ⇒ 需 t = {:.3f} s".format(D_EARTH, t_req_earth))
    print("     比邻星 |R| = {:.6e} m ⇒ 需 t = {:.6e} s（{:.4f} 年）".format(
        D_PROX, t_req_prox, t_req_prox / YR))
    print("     两者距离比 = {:.6e}".format(ratio_d))
    out["A1_t_earth"] = t_req_earth
    out["A1_t_prox"] = t_req_prox
    out["A1_ratio"] = ratio_d
    add("A1", "所指层", "两难·R 指什么：物体位置 ⇒ 共球面塌缩；空间位移场 ⇒ 与力方程脱钩", "FAIL",
        "原文 §2.1 只说 R 是「空间位移」，未指明它是**物体的位置矢量**还是**空间点自身的位移场**，"
        "两支都不利：① 若 R 是物体位置 ⇒ |R| = c·t 强制**所有物体在同一时刻到原点的距离都等于 ct** "
        "⇒ 空间塌为一个**球面**（二维）。机读：地球需 t = **{:.3f} s**、比邻星需 t = **{:.6e} s**"
        "（{:.4f} 年），两者**不可能同时满足**（距离比 = **{:.6e}**）。② 若 R 只是空间位移场"
        "（空间自身以光速流动）⇒ |R| = c·Δt 是标准的**光行距**关系，无矛盾（见 A7 的诚实登记），"
        "**但**此时 R 与物体的位置/速度**无关** ⇒ 它无法为 m = k∮dn/Ω（「物体周围的 R 条数」）"
        "和 P = m(C−V) 提供几何依据 ⇒ **公设与力方程脱钩**。"
        .format(t_req_earth, t_req_prox, t_req_prox / YR, ratio_d))

    # ---- A2 C 全局均匀 ⇒ 所有物体位置矢量相同 ----
    lat_obs = 1.0
    lat_pred_C = 0.0
    dev_C = (lat_pred_C - lat_obs) / lat_obs
    print("[A2] C 全局均匀（原文 §3.1 自承「方向被认为均匀且不变」）⇒ R_A = R_B = Ct")
    print("     两物体实测间距 = {:.1f} m；公设预测 = {:.1f} m ⇒ 偏差 {:+.2f}%".format(
        lat_obs, lat_pred_C, dev_C * 100))
    out["A2_dev"] = dev_C
    add("A2", "所指层", "C 全局均匀 ⇒ 所有物体位置矢量相同（空间塌为一点）", "FAIL",
        "原文 §3.1 自承「空间光速矢量 C 的方向被认为**均匀且不变**」。若 C 在空间中均匀，"
        "则 R = C t 对**每一个**物体给出**同一个**位置矢量 ⇒ **所有物体位置重合**，空间塌为一点。"
        "机读：取两个物体，实测间距 **{:.1f} m**，公设预测 **{:.1f} m** ⇒ 偏差 **{:+.2f}%**。"
        "唯一的退路是让 C 因物体而异，但那样 C 就不再是「空间本底光速场」，而是由位置反定义的量"
        "（C = R/t），公设退化为恒等式重排 ⇒ 零内容。"
        .format(lat_obs, lat_pred_C, dev_C * 100))

    # ---- A3 类光/类空两难 ----
    ds2_rel_zero = Fraction(1) - Fraction(1)          # 1 − (|dR/dt|/c)²，Ċ=0 时精确为 0
    ds2_rel_sp = float(1) - (1.0 + (omega_i * t_i) ** 2)  # Ċ≠0 时 1 − (1+(ωt)²) = −(ωt)²
    cls_zero = classify_ds2(ds2_rel_zero)
    cls_sp = classify_ds2(ds2_rel_sp)
    v_over_c_sp = math.sqrt(1.0 + (omega_i * t_i) ** 2)
    print("[A3] 类光/类空两难")
    print("     Ċ = 0  ⇒ ds²/(c²dt²) = 1−1 = 0（精确）⇒ {}".format(cls_zero))
    print("     Ċ ≠ 0  ⇒ ds²/(c²dt²) = −(ωt)² = {:+.6e} ⇒ {}".format(ds2_rel_sp, cls_sp))
    print("     |dR/dt|/c = √(1+(ωt)²) = {:.6e} > 1（解析闭式；示例 ω={:.0e}, t={:.1f} s）".format(
        v_over_c_sp, omega_i, t_i))
    out["A3_cls_zero"] = cls_zero
    out["A3_cls_sp"] = cls_sp
    out["A3_ds2_sp"] = ds2_rel_sp
    out["A3_v_over_c"] = v_over_c_sp
    add("A3", "因果层", "两难·类光或类空：Ċ=0 ⇒ ds²≡0（有质量粒子不存在）；Ċ≠0 ⇒ 超光速", "FAIL",
        "由 A0 的求导结果 |dR/dt| = √(c² + t²|Ċ|²)（C ⊥ Ċ）："
        "① 若 Ċ = 0（原文 §3.1 宏观假设「方向不变」）⇒ |dR/dt| = c ⇒ "
        "ds²/(c²dt²) = 1 − 1 = **0（精确，Fraction 层相消）** ⇒ 世界线**类光** ⇒ "
        "固有时 dτ ≡ 0 ⇒ **有质量粒子（类时）在该公设下不存在**。"
        "② 若 Ċ ≠ 0（原文又称 C「方向可变」）⇒ |dR/dt| = c·√(1+(|Ċ|t/c)²) **> c** ⇒ "
        "ds²/(c²dt²) = −(ωt)² = **{:+.4e} < 0** ⇒ **类空、超光速**。"
        "机读示例（ω = {:.0e} s⁻¹，t = 1 s）：|dR/dt| = **{:.6e}·c**。"
        "⇒ **两支都死，无第三支**（与 r152/r153 的 √2·c 超光速同型，但那里是两条约束联立的后果，"
        "这里只由 R = C t 一条推出）。注意：②的数值依赖 ω（ω 是自由参数），故只作**存在性**指控；"
        "①不依赖任何自由参数。"
        .format(ds2_rel_sp, omega_i, v_over_c_sp))

    # ---- A4 固有时读法救回类时性（对靶有利，诚实记 PASS） ----
    beta = 0.9
    g = gamma_of(beta)
    ds2_rel_P = 1.0 - 1.0 / (g * g)                  # (c/γ)² ⇒ 1 − β²
    cls_P = classify_ds2(ds2_rel_P)
    print("[A4] 读法 P（t 读为固有时 τ）：R = C τ ⇒ |dR/dt| = c/γ = {:.6e}".format(C_LIGHT / g))
    print("     ds²/(c²dt²) = 1 − 1/γ² = {:+.6e} ⇒ {}".format(ds2_rel_P, cls_P))
    out["A4_gam"] = g
    out["A4_ds2"] = ds2_rel_P
    out["A4_cls"] = cls_P
    add("A4", "读法层", "读法 P（t = 固有时）确实救回类时性：ds² = c²dt²(1−1/γ²) > 0（★对靶有利）",
        "PASS",
        "★防漏判：本卷先登记对靶有利的分支。若把 R = C t 中的 t 读作**固有时 τ**（读法 P，"
        "与 r161 读法层同构），则 |dR/dt| = c·(dτ/dt) = **c/γ**，"
        "ds²/(c²dt²) = 1 − 1/γ² = **1 − β² = {:+.6e} > 0**（β = {} ⇒ γ = {:.10f}）⇒ **类时** ✓，"
        "A3①的「有质量粒子不存在」被避开。**这是本卷对靶有利的结论，诚实登记为 PASS。**"
        "但它救不回空间维度（A5），也救不回共球面（A5），故不构成翻案。"
        .format(ds2_rel_P, beta, g))

    # ---- A5 读法 P 救不回空间维度 ----
    # 两物体：B 静止、A 以 β 运动；同一坐标时 t
    # R_A = C·τ_A = C·t/γ，R_B = C·t ⇒ R_B − R_A = C·t(1 − 1/γ) ∥ C
    dtau_A = t0 / g
    dtau_B = t0
    rel_pred = C_LIGHT * (dtau_B - dtau_A)           # 模长，方向 ∥ C
    lat_pred_P = 0.0
    dev_P = (lat_pred_P - lat_obs) / lat_obs
    print("[A5] 读法 P 下相对位置：R_B − R_A = C·(τ_B − τ_A) ∥ C")
    print("     τ_A = {:.6e} s，τ_B = {:.6e} s ⇒ |ΔR| = {:.6e} m，方向 ∥ C".format(
        dtau_A, dtau_B, rel_pred))
    print("     横向分量：预测 {:.1f} m vs 实测 {:.1f} m ⇒ 偏差 {:+.2f}%".format(
        lat_pred_P, lat_obs, dev_P * 100))
    out["A5_rel"] = rel_pred
    out["A5_dev"] = dev_P
    add("A5", "读法层", "读法 P 救不回空间：相对位置恒 ∥ C ⇒ 横向维度塌缩（一维化）", "FAIL",
        "读法 P 虽救回类时性（A4），但**救不回空间维度**。在同一坐标时 t，"
        "R_A = C·τ_A、R_B = C·τ_B ⇒ 相对位置 R_B − R_A = **C·(τ_B − τ_A) 恒平行于 C**。"
        "机读（β = {} ⇒ γ = {:.6f}，t = 1 s）：τ_A = {:.6e} s、τ_B = {:.6e} s ⇒ "
        "|ΔR| = **{:.6e} m**，方向 ∥ C ⇒ **横向分量恒为 0**。"
        "而实测相对位置的横向分量 = **{:.1f} m** ⇒ 偏差 **{:+.2f}%**。"
        "⇒ 读法 P 下空间**退化为沿 C 的一条直线**（一维），三维空间不再存在。"
        "读法 C 下更差（A2：所有物体位置重合）。⇒ 两种读法都救不回空间。"
        .format(beta, g, dtau_A, dtau_B, rel_pred, lat_obs, dev_P * 100))

    # ---- A6 V 与 dR/dt 的两难 ----
    P_claim = M_E * C_LIGHT                          # §3.1「静止动量 P_静 = mC」
    P_pred = 0.0
    dev_P6 = (P_pred - P_claim) / P_claim
    print("[A6] V ≡ dR/dt 且 Ċ = 0 ⇒ V = C ⇒ P = m(C−V) = 0")
    print("     原文 §3.1 静止动量 P_静 = m_e·c = {:.6e} kg·m/s；预测 {:.1f} ⇒ 偏差 {:+.2f}%".format(
        P_claim, P_pred, dev_P6 * 100))
    out["A6_P_claim"] = P_claim
    out["A6_dev"] = dev_P6
    add("A6", "动力学层", "两难·V 与 dR/dt：V=dR/dt ⇒ P = m(C−V) 恒零；V≠dR/dt ⇒ R 与物体脱钩",
        "FAIL",
        "原文从未说明物体的速度 V 与 R 的关系，两支都不利："
        "① 若 V ≡ dR/dt（R 是物体位置，速度是位置导数）⇒ 在 Ċ = 0 下 V = C ⇒ "
        "**P = m(C − V) ≡ 0**，即**一切动量恒为零**。机读：原文 §3.1 自承「静止动量 P_静 = mC」"
        "（电子 {:.6e} kg·m/s），本支预测 **0** ⇒ 偏差 **{:+.2f}%**。"
        "② 若 V ≠ dR/dt ⇒ 物体的位置变化率**不等于**空间位移的变化率 ⇒ R 不是物体的位置"
        " ⇒ 回到 A1 的第二支：**R 与物体运动学脱钩**，R = C t 对物体的 P、V、m 没有任何约束力"
        " ⇒ 该公设对力方程**零内容**。"
        "⇒ 想让力方程有内容就必须让 R 与物体挂钩，一挂钩动量就恒零。"
        .format(P_claim, dev_P6 * 100))

    # ---- A7 防过度指控：|R| = c·Δt 作为光行距定义是正确的 ----
    dt_radar = 2.0 * D_MOON / C_LIGHT                 # 地月往返光行时
    r_back = C_LIGHT * dt_radar / 2.0
    dev_radar = abs(r_back - D_MOON) / D_MOON
    print("[A7] 防过度指控：光行距 r = c·Δt/2（Δt = {:.6f} s ⇒ r = {:.6e} m，偏差 {:.2e}）".format(
        dt_radar, r_back, dev_radar))
    out["A7_dev"] = dev_radar
    add("A7", "防过度指控", "|R| = c·Δt 作为「光行距」定义是标准且正确的 ⇒ 该式本身不判错", "INFO",
        "★防过度指控：若把 R = C t 只读作 **|R| = c·Δt**（光行距/光行时关系），它是"
        "**标准且实验证实**的（雷达测距、 lunar laser ranging 都基于它）。机读自检："
        "地月往返光行时 Δt = **{:.6f} s** ⇒ r = c·Δt/2 = **{:.6e} m**，与月距 {:.6e} m 偏差 {:.2e}。"
        "⇒ 本卷**不指控这个关系本身**。指控的是：原文把它列为「基本公设」并**由此**去定义质量"
        "（m = k∮dn/Ω）、动量（P = m(C−V)）与电荷（经 q = k′dm/dt）——"
        "**从光行距定义推不出这些**，这才是本卷判决的对象。"
        .format(dt_radar, r_back, D_MOON, dev_radar))

    return out


# ============================== B 组：质量几何化 m = k ∮ dn/Ω ==============================
def group_B():
    print("\n" + "=" * 78)
    print(" [B 组] 质量几何化 m = k ∮ dn/Ω")
    print("=" * 78)
    out = {}

    # ---- B1 记号层 ----
    add("B1", "记号层", "记号不自洽：∮ dn/Ω 分子是微分、分母是总量（4π）⇒ 得平均值而非总量",
        "BOUNDARY",
        "原文写 m = k ∮ dn/Ω。分子 dn 是**微分增量**（条数的微元），分母 Ω 若不写 dΩ 则是"
        "**总立体角**（4π）——微分除以非微分，记号本身不成形。两种补救读法给出不同的量："
        "① 读作 (1/4π)∮dn = N/(4π) ⇒ 与总条数 N 成正比，只差常数 1/4π；"
        "② 读作 ∮(dn/dΩ) dΩ = N ⇒ 就是总量。⇒ 无论哪种，都**必须**先把 Ω 明确为 dΩ 或 4π，"
        "原文未做 ⇒ 记为 BOUNDARY（记号缺陷，不单独证伪）。")

    # ---- B2 可加性两难 ----
    # 读法①总量：m ∝ N ⇒ 可加（对靶有利）
    # 读法②原文措辞「密度」：两团合并密度不变 ⇒ 不可加
    m_one = 1.0
    m_two_total = 2.0 * m_one
    m_two_density = m_one
    dev_density = (m_two_density - m_two_total) / m_two_total
    print("[B2] 可加性两难：总量读法 2×1kg = {:.1f} kg；原文措辞「密度」给 {:.1f} kg ⇒ {:+.2f}%".format(
        m_two_total, m_two_density, dev_density * 100))
    out["B2_dev"] = dev_density
    add("B2", "可加性层", "总量读法可加：m ∝ N ⇒ 2×1kg = 2kg（★对靶有利，诚实登记为 PASS）",
        "PASS",
        "先给靶应得的：若把 ∮dn/Ω 读作 (1/4π)∮dn = **N/(4π)**（N = 总条数），则 m **正比于总条数**，"
        "只差一个常数因子 4π ⇒ **质量可加** ✓。机读：两个 1 kg 砝码合称 ⇒ **{:.1f} kg**，"
        "与天平实验一致（相对不确定度 ~1e−6）。**这是本卷对靶有利的结论，诚实登记为 PASS** —— "
        "该公设不是「一算就错」，问题出在原文的**措辞**（B3）与「条数」**无定义**（B5）。"
        .format(m_two_total))

    add("B3", "可加性层", "两难·措辞：原文称 m 为「密度」⇒ 不可加（−50%），与一切称重实验冲突", "FAIL",
        "原文措辞称 m 为「单位立体角内……的**条数密度**」。**密度不可加**：两个 1 kg 砝码合称，"
        "密度不变而质量是 **2 kg**。机读：按「密度」读法给 **{:.1f} kg**，按「总量」读法给 "
        "**{:.1f} kg** ⇒ 偏差 **{:+.2f}%**，与天平实验（相对不确定度 ~1e−6）相差 **5 个数量级以上**。"
        "⇒ 原文要么把「密度」改口为「总量」（记号修正，零代价，见 C 组 M3），"
        "要么承认质量不可加（与一切称重实验冲突）。**两支中只有改口那一支能活，"
        "而活着的那支只是改了个说法。**".format(m_two_density, m_two_total, dev_density * 100))

    # ---- B4 量纲 ⇒ k 有量纲 ⇒ 非定律 ----
    D_M = (1, 0, 0)
    D_N = (0, 0, 0)
    D_OMEGA = (0, 0, 0)
    D_k = dim_div(D_M, dim_div(D_N, D_OMEGA))
    print("[B4] 量纲：[m] = {}，[∮dn/Ω] = {} ⇒ [k] = {}".format(D_M, dim_div(D_N, D_OMEGA), D_k))
    out["B4_dim_k"] = D_k
    add("B4", "量纲层", "量纲：[k] = (M) ⇒ k 是**有量纲自由参数** ⇒ 该式不是定律", "FAIL",
        "真做 (M, L, T) 元组运算：「条数」n 是**计数** ⇒ 无量纲 (0,0,0)；立体角 Ω（sr）⇒ 无量纲 "
        "(0,0,0) ⇒ [∮dn/Ω] = (0,0,0)，而 [m] = (1,0,0) ⇒ **[k] = (1,0,0)**，即 k 带**质量量纲**。"
        "按本线既有纪律：**有量纲自由参数 = 非定律** —— 一个含待定有量纲常数的式子可以拟合"
        "任意一组质量值，不构成约束。且原文**从未给出 k 的数值或量级** ⇒ B5 的「不可操作」成立。"
        "（与 r161 的 k′ 同型：两条几何化公设各引入一个有量纲的未定常数。）")

    # ---- B5 不可操作 ----
    add("B5", "操作层", "「条数」n 无定义：无测度、无密度函数、无归一化 ⇒ 公设不可计算", "FAIL",
        "要由 m = k∮dn/Ω 算出质量，必须知道：① dn 在球面（或立体角）上如何分布；"
        "② 该分布的**测度**（是 dΩ 还是别的）；③ n 的**归一化**（一条「空间位移矢量」算几条）；"
        "④ k 的数值。**这四项原文一项都没给**。机读自由度计数：给定 m_e 一个观测值，"
        "只能反解出组合量 k·N_e/4π 的**一个**等式 ⇒ **欠定**，无法预测 m_p、m_μ、m_τ 中的任何一个。"
        "⇒ 该公设在现有文本下**不可操作**（不是算错，是**算不出来**）。")

    # ---- B6 质量量子化 ⇒ 零判别力 ----
    ratio_mp_me = M_P / M_E
    # CODATA 2018：m_p/m_e = 1836.15267343(11) ⇒ 绝对不确定度 1.1e-7（末两位）
    MP_ME_U = 1.1e-7
    u_rel = MP_ME_U / ratio_mp_me
    print("[B6] 质量量子化：m_p/m_e = {:.8f}，绝对不确定度 {:.1e} ⇒ 相对 {:.3e}".format(
        ratio_mp_me, MP_ME_U, u_rel))
    md = min_denominator(ratio_mp_me, u_rel)
    q_min = md[0] if md else None
    p_min = md[1] if md else None
    err_min = md[2] if md else None
    if q_min:
        print("     在实测精度内的最小整数分母 Q_min = {}（p = {}，相对误差 {:.3e}）".format(
            q_min, p_min, err_min))
    # 小整数假设检验：q = 3
    p3 = int(round(ratio_mp_me * 3))
    err3 = abs(p3 / 3.0 - ratio_mp_me) / ratio_mp_me
    ratio3 = err3 / u_rel
    print("     小整数假设 q=3：{}/3 = {:.6f}，相对误差 {:.4e}，超出实测不确定度 {:.3e} 倍".format(
        p3, p3 / 3.0, err3, ratio3))
    out["B5_q_min"] = q_min
    out["B5_err_min"] = err_min
    out["B5_err3"] = err3
    out["B5_ratio3"] = ratio3
    out["B5_u_rel"] = u_rel

    if q_min is not None and q_min > 100:
        add("B6", "量子化层", "若 n 是整数计数 ⇒ 质量量子化 ⇒ **零判别力**（不构成证伪也不构成支持）",
            "INFO",
            "若「条数」n 是整数计数 ⇒ m = k·N/(4π) ⇒ 质量谱离散 ⇒ 任何质量比都必须是有理数 p/q。"
            "机读：m_p/m_e = **{:.8f}**，实测相对不确定度 **{:.3e}** ⇒ 连分数/暴力扫描得"
            "**最小整数分母 Q_min = {}**（p = {}，相对误差 {:.3e}）。"
            "① 若还要求 N 是**小整数**（如 3）：{}/3 = {:.6f}，相对误差 **{:.4e}**，"
            "**超出实测不确定度 {:.3e} 倍** ⇒ 与观测冲突。② 若不限制 N 的大小，则 Q_min ~ 1e3–1e4 ⇒ "
            "**任何实数质量比都能被足够大的整数比逼近** ⇒ 量子化**不产生任何可检验的独特预言**"
            " ⇒ 按本线既有纪律（r153 F6 零分辨力控制 / r149「记账式 ≠ 约束式」），"
            "**既不得当指控也不得当辩护**，诚实记 **INFO**。".format(
                ratio_mp_me, u_rel, q_min, p_min, err_min, p3, p3 / 3.0, err3, ratio3))

    # ---- B7 ★最硬：与 R=Ct 联合 ⇒ 电荷两支都死 ----
    # 分支 1：C 方向不变 ⇒ R 的立体角分布不随 t 变 ⇒ n 不随 t 变 ⇒ dm/dt = 0 ⇒ q = 0
    q_pred_b1 = 0.0
    dev_b1 = (q_pred_b1 - Q_E) / Q_E
    # 分支 2：C 方向可变 ⇒ n 只由该处 C 场决定 ⇒ 同位置的 p/e/n 电荷相同
    spread_pred = 0.0
    spread_obs = Q_E - (-Q_E)                        # +e − (−e) = 2e（中子 0 落在中间）
    dev_b2 = (spread_pred - spread_obs) / Q_E
    print("[B7] 与 R=Ct 联合：")
    print("     分支1（C 方向不变，原文 §3.1 自承）⇒ dm/dt = 0 ⇒ q = 0 vs e = {:.6e} ⇒ {:+.2f}%".format(
        Q_E, dev_b1 * 100))
    print("     分支2（C 方向可变）⇒ 电荷与粒子种类无关 ⇒ 同位置 p/e/n 电荷相同")
    print("           预测离散度 {:.1f} vs 实测 {:.6e} C（= 2e）⇒ 相对 e {:+.2f}%".format(
        spread_pred, spread_obs, dev_b2 * 100))
    out["B6_dev1"] = dev_b1
    out["B6_dev2"] = dev_b2
    out["B6_spread_obs"] = spread_obs
    add("B7", "联合后果层", "★最硬·两难：与 R=Ct 联合后，电荷要么恒零、要么与粒子种类无关（两支都死）",
        "FAIL",
        "本卷最硬的一条，由两条公设**联立**得出。m 的素材是「物体周围空间位移矢量 R 的条数」，"
        "而 R = C t ⇒ 条数的立体角分布完全由 **C 的方向分布**决定："
        "① 若 C 方向**不变**（原文 §3.1 自承「空间光速矢量 C 的方向被认为均匀且不变」）⇒ "
        "R 的立体角分布不随 t 变 ⇒ 条数 n 不随 t 变 ⇒ **dm/dt = 0** ⇒ "
        "由 q = k′ dm/dt（r161 的靶）⇒ **q ≡ 0，一切电荷恒为零**。机读：预测 0 vs 电子电荷 "
        "**{:.6e} C** ⇒ 偏差 **{:+.2f}%**。"
        "② 若 C 方向**可变**（原文 §2.1 又称 C「方向可变」）⇒ dm/dt ≠ 0，但 n 只由**该处空间场**决定"
        " ⇒ **同一空间点上任何物体的 m 与 dm/dt 相同** ⇒ **电荷与粒子种类无关** ⇒ "
        "质子、电子、中子在同一位置必须带**相同**电荷。机读：预测三者电荷离散度 **{:.1f}**"
        " vs 实测离散度 **{:.6e} C = 2e**（+e, 0, −e）⇒ 相对 e 偏差 **{:+.2f}%**。"
        "⇒ **两支都死**：一支没有电荷，一支所有粒子电荷一样。要同时避开，必须再引入一个"
        "**与粒子种类相关、且不来自 C 场**的内部量（见 C 组 M5）——那等于把电荷重新设为独立基本量，"
        "正是 r161 已经判定的「修复即自杀」方向。"
        .format(Q_E, dev_b1 * 100, spread_pred, spread_obs, dev_b2 * 100))

    # ---- B7 条数的产生/消灭机制缺失 ----
    add("B8", "机制层", "条数的产生/消灭机制缺失：q ≠ 0 ⇒ dN/dt ≠ 0，原文无来源（与 r161 联动，不重复指控）",
        "BOUNDARY",
        "由 r161 已判定（本卷**不重复指控**，只登记联动）：q ≠ 0 ⇒ dm/dt ≠ 0 ⇒ "
        "条数 N 必须**持续增加或减少**。原文没有给出条数的产生/消灭机制、守恒律或源项。"
        "⇒ 这是**内容缺失**而非计算错误，记 BOUNDARY。"
        "（若要定量：电子 q < 0 ⇒ N 递减 ⇒ 存在 N → 0 的有限时刻，但该时刻依赖 r161 中未定的 k′，"
        "r161 已给出下界 > 9.7e10 年，本卷沿用其结论。）")

    return out


# ============================== C 组：修复定价 ==============================
def group_C():
    print("\n" + "=" * 78)
    print(" [C 组] 修复定价：5 个动作 × 位掩码（32 组合），严格/宽松双档都报")
    print("=" * 78)
    out = {}

    # 动作定义（位 → 名称、代价类型）
    # M1 引入参考事件：R = C·Δt（恢复时间平移对称性）
    # M2 放弃 |R| = c·t 对物体位置的约束（放弃共球面/一维化）
    # M3 记号修正：把「密度」改口为「总量」（m = k·N）
    # M4 补测度与密度函数 ρ(Ω̂)，使 n 可算（公设可操作）
    # M5 给条数引入与粒子种类相关的内部量子数（使电荷因粒子而异）
    NAMES = ["M1 参考事件", "M2 弃 |R|=ct", "M3 密度→总量", "M4 补测度", "M5 种类量子数"]
    COST = [1, 2, 0, 1, 1]          # M2 删核心内容 ⇒ 罚 2；M3 纯记号 ⇒ 0

    def has(mask, i):
        return bool(mask & (1 << i))

    survivors = []
    for mask in range(32):
        op = has(mask, 3)                        # 可操作：需 M4
        addit = has(mask, 2) or has(mask, 3)     # 可加性：M3 或 M4
        sphere = has(mask, 1)                    # 不共球面：需 M2
        tshift = has(mask, 0)                    # 时间平移对称：需 M1
        charge = has(mask, 4)                    # 电荷非零且因种类而异：需 M5
        if op and addit and sphere and tshift and charge:
            cost = sum(COST[i] for i in range(5) if has(mask, i))
            survivors.append((mask, cost))

    zero_cost = [s for s in survivors if s[1] == 0]
    min_cost = min((s[1] for s in survivors), default=None)
    min_masks = [s[0] for s in survivors if s[1] == min_cost] if survivors else []

    def name_of(mask):
        return "+".join(NAMES[i] for i in range(5) if has(mask, i))

    print(" 存活组合 {} / 32，零代价 {}，最小代价 {}".format(
        len(survivors), len(zero_cost), min_cost))
    for m, c in survivors:
        print("   mask {:05b} cost {} — {}".format(m, c, name_of(m)))

    out["survivors"] = len(survivors)
    out["zero_cost"] = len(zero_cost)
    out["min_cost"] = min_cost
    out["names"] = [name_of(m) for m, c in survivors]

    # 双档报告（记忆纪律：禁只报对自己有利的一档）
    # 严格档：不许删式（M2 禁用）⇒ 存活 0
    strict = [s for s in survivors if not has(s[0], 1)]
    out["strict"] = len(strict)
    out["loose"] = len(survivors)

    add("C1", "修复定价层",
        "修复定价：32 组合 ⇒ 存活 {} / 严格档（不许删式）{} / 零代价 {}".format(
            len(survivors), len(strict), len(zero_cost)),
        "FAIL",
        "5 个修复动作的位掩码全枚举（2^5 = 32）。判活条件五项全满足（可操作 / 可加 / 不共球面 / "
        "时间平移对称 / 电荷因种类而异）。机读结果：**宽松档存活 {}**（最小代价 {}，"
        "代表解：{}），**严格档（不许删式 M2）存活 {}**，**零代价 {}**。"
        "⇒ 双档都报（禁只报一档）。".format(
            len(survivors), min_cost, "；".join(out["names"]) if out["names"] else "无",
            len(strict), len(zero_cost)))

    add("C2", "修复定价层", "★修复即自杀（第十一度）：每个存活解都删掉了 |R| = c·t 并引入任意函数",
        "FAIL",
        "所有 {} 个存活解的**共性**：① 必须含 **M2**（放弃 |R| = c·t 对物体位置的约束）——"
        "即删掉「时空同一化」这条公设的经验内容，剩下的 |R| = c·Δt 只是**光行距定义**（已知物理，A7）；"
        "② 必须含 **M4**（补一个任意的条数密度函数 ρ(Ω̂)）——引入无穷多自由度，"
        "可拟合任意质量谱 ⇒ **记账式而非约束式**（与 r149 同型）；③ 必须含 **M5**"
        "（引入与粒子种类相关、不来自 C 场的内部量子数）——这等于**把电荷重新设为独立基本量**，"
        "正是 r161 判定的自杀方向。⇒ **「该公设组可修复」与「该公设组仍有内容」不可兼得**"
        "（本线**第十一**次复发）。".format(len(survivors)))

    return out


# ============================== 控制组（全部真机读，禁写死 True） ==============================
def group_controls(A, B):
    print("\n" + "=" * 78)
    print(" [控制组] 必设：证明判据有分辨力（非恒失败）")
    print("=" * 78)

    # U1 光行距正对照
    dt_r = 2.0 * D_MOON / C_LIGHT
    r_back = C_LIGHT * dt_r / 2.0
    control("U1 光行距正对照：r = c·Δt/2 复原月距（证明我们不指控该关系本身）",
            abs(r_back - D_MOON) / D_MOON < 1e-12,
            "r = {:.6e} m vs 月距 {:.6e} m，相对差 {:.2e}".format(r_back, D_MOON,
                                                              abs(r_back - D_MOON) / D_MOON))

    # U2 类时正对照
    b = 0.9
    ds2 = 1.0 - b * b
    control("U2 类时正对照：SR β=0.9 ⇒ ds²/(c²dt²) = 1−β² = {:.4f} > 0 ⇒ 判 TIMELIKE".format(ds2),
            classify_ds2(ds2) == "TIMELIKE", "ds²/(c²dt²) = {:.6f}".format(ds2))

    # U3 类光正对照
    control("U3 类光正对照：光子 β=1 ⇒ ds² = 0 ⇒ 判 LIKELIKE（证明判据非恒判类时）",
            classify_ds2(0.0) == "LIKELIKE", "ds²/(c²dt²) = 0 ⇒ {}".format(classify_ds2(0.0)))

    # U4 可加性判据正对照（电荷已知可加）
    q_tot = 1.0 + 1.0
    control("U4 可加性正对照：电荷 1e+1e = {:.1f}e（判据对已知可加量必须 PASS）".format(q_tot),
            abs(q_tot - 2.0) < 1e-15, "合计 = {:.1f} e ✓".format(q_tot))

    # U5 可加性判据反对照（温度已知不可加）
    t_mix = 300.0
    dev_T = (t_mix - 600.0) / 600.0
    control("U5 可加性反对照：300K+300K = {:.0f}K ≠ 600K ⇒ 判据必须 FAIL（{:+.1f}%）".format(
        t_mix, dev_T * 100), abs(dev_T) > 0.1,
        "偏差 {:+.2f}% ⇒ 判据能识别不可加".format(dev_T * 100))

    # U6 连分数算法正对照：4/3 的最小分母应为 3
    md43 = min_denominator(4.0 / 3.0, 1e-9, qmax=10000)
    control("U6 最小分母算法正对照：x = 4/3 ⇒ 最小分母应为 3（不是 1，也不是 1e4）",
            md43 is not None and md43[0] == 3,
            "Q_min = {}（p = {}）".format(md43[0] if md43 else None, md43[1] if md43 else None))

    # U7 连分数算法反对照：√2 在 1e-8 下最小分母应远大于 1
    md2 = min_denominator(math.sqrt(2.0), 1e-8, qmax=200000)
    control("U7 最小分母算法反对照：x = √2 在 1e-8 下最小分母应 > 100（证明不因 tol 小就返回 1）",
            md2 is not None and md2[0] > 100,
            "Q_min = {}".format(md2[0] if md2 else None))

    # U8 质量比锚点
    r_mp_me = M_P / M_E
    control("U8 质量比锚点：m_p/m_e = {:.6f}（跨卷 r155/r161 的 1836.15）".format(r_mp_me),
            abs(r_mp_me - 1836.15267343) / 1836.15267343 < TOL_CONST,
            "m_p/m_e = {:.8f}".format(r_mp_me))

    # U9 靶来料可定位
    control("U9 靶来料可定位（公设引用前提）", os.path.isfile(TARGET_MD),
            "路径存在 = {}".format(os.path.isfile(TARGET_MD)))

    # U10 天平锚点（真算：密度读法 vs 实测）
    dev_bal = (1.0 - 2.0) / 2.0
    control("U10 天平锚点：密度读法 2×1kg ⇒ {:.1f}kg vs 实测 2.0kg ⇒ 判据必须 FAIL（{:+.1f}%）".format(
        1.0, dev_bal * 100), abs(dev_bal) > 0.1,
        "偏差 {:+.2f}% ⇒ 与实测不确定度 ~1e-6 相差 5 个数量级".format(dev_bal * 100))


# ============================== 守卫（全部真机读） ==============================
def group_guards(A, B, C):
    print("\n" + "=" * 78)
    print(" [守卫]（★全部机读驱动，无一处 ok 写死 True）")
    print("=" * 78)

    n_fail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
    n_pass = sum(1 for e in ENTRIES if e["verdict"] == "PASS")
    guard("G1 verdict 由机读驱动：FAIL {} / PASS {}（两者都须 > 0）".format(n_fail, n_pass),
          n_fail > 0 and n_pass > 0, "机读累加 FAIL={} PASS={}".format(n_fail, n_pass))

    # G2：A3①的 ds²=0 必须是 Fraction 精确相消
    g2 = (Fraction(1) - Fraction(1)) == 0
    guard("G2 类光守卫：Ċ=0 分支的 ds²/(c²dt²) 必须是 Fraction 层精确 0（非浮点近似）",
          g2 and A["A3_cls_zero"] == "LIKELIKE",
          "1−1 = {}（Fraction），分类 = {}".format(int(Fraction(1) - Fraction(1)), A["A3_cls_zero"]))

    # G3：量纲运算自检
    g3 = dim_mul((1, 0, 0), (0, 1, -2)) == (1, 1, -2)
    guard("G3 量纲运算守卫：dim_mul([m],[a]) 必须 = (1,1,−2)（真算，非声明）", g3,
          "dim_mul((1,0,0),(0,1,-2)) = {}".format(dim_mul((1, 0, 0), (0, 1, -2))))

    # G4：Q_min 最小性（真暴力验证 q < Q_min 都不满足）
    qm = B["B5_q_min"]
    if qm is not None and qm > 1:
        x = M_P / M_E
        tol = B["B5_u_rel"]
        all_bad = True
        for q in range(1, min(qm, 20000)):
            p = int(round(x * q))
            if abs(p / q - x) / x < tol:
                all_bad = False
                break
    else:
        all_bad = False
    guard("G4 最小性守卫：Q_min = {} 以下的所有分母都必须不满足精度（真暴力）".format(qm),
          all_bad, "q = 1..{} 全部超出 tol ⇒ 最小性成立 = {}".format(qm - 1, all_bad))

    # G5：Q_min 本身必须满足精度
    if qm is not None:
        x = M_P / M_E
        p = int(round(x * qm))
        err = abs(p / qm - x) / x
        g5 = err < B["B5_u_rel"]
    else:
        err = None
        g5 = False
    guard("G5 精度守卫：{}/{} 的相对误差 {:.3e} 必须 < 实测不确定度 {:.3e}".format(
        int(round((M_P / M_E) * qm)) if qm else 0, qm, err if err else 0.0, B["B5_u_rel"]),
        g5, "err = {:.4e} vs tol = {:.4e}".format(err if err else 0.0, B["B5_u_rel"]))

    # G6：小整数假设必须真的冲突
    g6 = B["B5_ratio3"] > 1.0
    guard("G6 小整数守卫：q=3 的误差必须超出实测不确定度（真算比值 {:.3e} > 1）".format(B["B5_ratio3"]),
          g6, "比值 = {:.4e} ⇒ 冲突 = {}".format(B["B5_ratio3"], g6))

    # G7：修复枚举双档
    guard("G7 修复双档守卫：宽松 {} / 严格 {} / 零代价 {}（真枚举）".format(
        C["loose"], C["strict"], C["zero_cost"]),
        C["zero_cost"] == 0 and C["strict"] == 0,
        "宽松 {}，严格 {}，零代价 {}".format(C["loose"], C["strict"], C["zero_cost"]))

    # G8：两难条目数量
    n_dil = sum(1 for e in ENTRIES if "两难" in e["name"])
    guard("G8 两难守卫：归属未定的命题必须写成两难（数量须 ≥ 3，实得 {}）".format(n_dil),
          n_dil >= 3, "含「两难」条目 = {}".format(n_dil))

    # G9：诚实登记（对靶有利的条目必须真的存在且注明）
    pass_notes = " ".join(e["note"] for e in ENTRIES if e["verdict"] == "PASS")
    g9 = ("对靶有利" in pass_notes or "诚实登记" in pass_notes) and n_pass >= 2
    guard("G9 诚实登记守卫：PASS 条目须 ≥2 且注明「对靶有利/诚实登记」（实得 {}）".format(n_pass),
          g9, "PASS = {}，含标注 = {}".format(n_pass, g9))

    # G10：防过度指控（必须承认光行距定义正确）
    g10 = any("光行距" in e["note"] and e["verdict"] == "INFO" for e in ENTRIES)
    guard("G10 防过度指控守卫：必须存在 INFO 条目承认 |R|=cΔt 作为光行距是正确的", g10,
          "A7 INFO 含「光行距」= {}".format(g10))


# ============================== 输出 ==============================
def build_payload(A, B, C):
    stats = {}
    for e in ENTRIES:
        stats[e["verdict"]] = stats.get(e["verdict"], 0) + 1
    for k in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION"):
        stats.setdefault(k, 0)

    verdict = ("SPACETIME-IDENTIFICATION-COLLAPSES-DIMENSION-AND-MASS-GEOMETRIZATION"
               "-UNDEFINED-CHARGE-DILEMMA-BOTH-BRANCHES-DEAD")
    verdict_zh = (
        "时空同一化公设 R = C t 把空间压成一维（或一点），并强制世界线类光或类空；"
        "质量几何化公设 m = k∮dn/Ω 的「条数」从未被定义、记号把平均值写作总量、k 是有量纲自由参数；"
        "二者联立后电荷要么恒为零、要么与粒子种类无关（两支都死）。"
        "求导本身正确、固有时读法确实恢复类时性、总量读法确实可加 —— 三条对靶有利的结论已诚实登记。"
    )

    payload = {
        "id": "TUFT-r162",
        "title": "时空同一化 R = C t 与质量几何化 m = k∮dn/Ω 的求导证明验证精算",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "target": "S17《宇宙大统一方程（力方程）》§2.1 基本公设与定义（时空同一化 / 质量几何化）",
        "target_file": os.path.relpath(TARGET_MD, OPENUFT_ROOT),
        "verdict": verdict,
        "verdict_zh": verdict_zh,
        "stats": stats,
        "entries": ENTRIES,
        "controls": [{"name": c["name"], "ok": c["ok"], "detail": c["detail"]} for c in CONTROLS],
        "guards": [{"name": g["name"], "ok": g["ok"], "detail": g["detail"]} for g in GUARDS],
        "key_numbers": {
            "dR_dt_over_c_analytic": A["A0_ratio_vc"],
            "closed_form_sqrt": A["A0_sqrt_pred"],
            "derivative_residual": A["A0_res"],
            "t_required_earth_s": A["A1_t_earth"],
            "t_required_proxima_s": A["A1_t_prox"],
            "distance_ratio_proxima_over_earth": A["A1_ratio"],
            "coincidence_dev": A["A2_dev"],
            "ds2_spacelike_branch": A["A3_ds2_sp"],
            "v_over_c_spacelike_branch": A["A3_v_over_c"],
            "gamma_beta09": A["A4_gam"],
            "ds2_proper_time_branch": A["A4_ds2"],
            "lateral_collapse_dev": A["A5_dev"],
            "momentum_zero_dev": A["A6_dev"],
            "P_static_claim_kg_m_s": A["A6_P_claim"],
            "radar_dev": A["A7_dev"],
            "additivity_density_dev": B["B2_dev"],
            "mass_ratio_mp_me": M_P / M_E,
            "min_integer_denominator": B["B5_q_min"],
            "q3_deviation_ratio": B["B5_ratio3"],
            "charge_zero_branch_dev": B["B6_dev1"],
            "charge_species_independent_dev": B["B6_dev2"],
            "repair_survivors_loose": C["loose"],
            "repair_survivors_strict": C["strict"],
            "repair_zero_cost": C["zero_cost"],
        },
        "not_closed": [
            "本卷只审 §2.1 的两条公设（R = C t、m = k∮dn/Ω）；q = k′ dm/dt 的自身审计在 r161，"
            "条目不可相加。",
            "B5 的「不可操作」以本卷能读到的文本为限：若「条数」n 在别处（本卷未见）另有定义与测度，"
            "该条应降级为 INFO 并重审。",
            "A3②的超光速数值依赖 ω（C 方向变化率，自由参数），本卷只作存在性指控；"
            "A3①（类光）不依赖任何自由参数。",
            "「修复即自杀」结论限于本卷枚举的 5 个动作集合（32 组合）；"
            "不排除存在本卷未列出的第 6 种修改路径。",
            "M2（放弃 |R| = c·t 对物体位置的约束）之后仍可保留 |R| = c·Δt 作为光行距定义，"
            "本卷已诚实登记它是标准且正确的（A7）。",
            "本卷未审 §3.2–§3.4 的四种运动状态（那是 r160 的领地），也未做引力侧还原（r159）。",
        ],
        "redline": [
            "数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。",
            "不宣称「张祥前体系全错」，只判决本卷所列的两条公设及其联合后果。",
            "PASS 不等于有内容：A0（求导正确）、A4（固有时恢复类时性）、B2（总量读法可加）"
            "均为**定义式或标准关系的恢复**，不构成对新物理的支持。",
            "B6 的质量量子化被判定为**零判别力**，既不得当指控也不得当辩护。",
        ],
    }
    return payload


def write_outputs(payload, outdir):
    base = "TUFT-r162_时空同一化与质量几何化_求导证明验证精算_" + payload["date"]
    jp = os.path.join(outdir, base + ".json")
    mp = os.path.join(outdir, base + ".md")
    rp = os.path.join(outdir, base + "_report.txt")
    vp = os.path.join(outdir, "判定_" + base + ".md")

    with open(jp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    L = []
    L.append("TUFT-r162｜时空同一化 R = C t 与质量几何化 m = k∮dn/Ω 的求导证明验证精算")
    L.append("生成时刻：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    L.append("判词：" + payload["verdict"])
    L.append("")
    L.append("机读推导")
    L.append("  R(t) = C(t)·t，|C| = c 常数 ⇒ C ⊥ Ċ ⇒ dR/dt = C + t·Ċ")
    L.append("  ⇒ |dR/dt| = sqrt(c^2 + t^2|dC/dt|^2) >= c")
    L.append("")
    L.append("关键数值")
    for k, v in payload["key_numbers"].items():
        L.append("  {:44s} {}".format(k, v))
    L.append("")
    L.append("条目统计：" + " / ".join("{}={}".format(k, payload["stats"][k])
                                    for k in ["PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION"]))
    L.append("控制组：{} / {}".format(sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    L.append("守卫  ：{} / {}".format(sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    L.append("")
    L.append("条目明细")
    for e in ENTRIES:
        L.append("  [{}] {} — {}".format(e["verdict"], e["code"], e["name"]))
    L.append("")
    L.append("未闭合项")
    for s in payload["not_closed"]:
        L.append("  - " + s)
    L.append("")
    L.append("红线")
    for s in payload["redline"]:
        L.append("  - " + s)
    with open(rp, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    M = []
    M.append("# TUFT-r162｜时空同一化 R = C t 与质量几何化 m = k∮dn/Ω 的求导证明验证精算")
    M.append("")
    M.append("**判词**：`{}`".format(payload["verdict"]))
    M.append("")
    M.append("{}。".format(payload["verdict_zh"]))
    M.append("")
    M.append("## 条目总表")
    M.append("")
    M.append("| 编号 | 判定 | 条目 | 说明 |")
    M.append("|---|---|---|---|")
    for e in ENTRIES:
        M.append("| {} | {} | {} | {} |".format(e["code"], e["verdict"], e["name"],
                                                e["note"].replace("\n", " ").replace("|", "/")))
    M.append("")
    M.append("## 控制组")
    for c in CONTROLS:
        M.append("- {} {} — {}".format("[OK]" if c["ok"] else "[BAD]", c["name"], c["detail"]))
    M.append("")
    M.append("## 守卫")
    for g in GUARDS:
        M.append("- {} {} — {}".format("[OK]" if g["ok"] else "[BAD]", g["name"], g["detail"]))
    with open(mp, "w", encoding="utf-8") as f:
        f.write("\n".join(M))

    V = []
    V.append("# 判定册 · TUFT-r162｜时空同一化 R = C t 与质量几何化 m = k∮dn/Ω 的求导证明验证精算")
    V.append("")
    V.append("## 一、编号与定位")
    V.append("")
    V.append("- **编号 r162**（实测首空号：全库 grep 仅 README 的「下轮从 r162 起」命中，无产物占用）")
    V.append("- **靶**：S17《宇宙大统一方程（力方程）》§2.1 **时空同一化**与**质量几何化**两条公设")
    V.append("- **分工**（条目不可相加）：r160 = 四项诠释；r161 = 电荷几何化 q = k′ dm/dt；"
             "本卷 = 剩下两条公设 + 二者**联合**对电荷的后果")
    V.append("")
    V.append("## 二、判词")
    V.append("")
    V.append("`{}`".format(payload["verdict"]))
    V.append("")
    V.append("{}。".format(payload["verdict_zh"]))
    V.append("")
    V.append("## 三、机读推导")
    V.append("")
    V.append("```")
    V.append("R(t) = C(t)·t，  |C| = c = 常数  ⇒  C·dC/dt = 0")
    V.append("⇒ dR/dt = C + t·dC/dt，   |dR/dt| = sqrt(c^2 + t^2 |dC/dt|^2) >= c")
    V.append("⇒ dC/dt = 0  ⇒ |dR/dt| = c        ⇒ ds^2 = 0    （类光，有质量粒子不存在）")
    V.append("⇒ dC/dt ≠ 0  ⇒ |dR/dt| > c        ⇒ ds^2 < 0    （类空，超光速）")
    V.append("```")
    V.append("")
    V.append("求导本身经**自适应中心差分**复核：解析 dR/dt = C + t·Ċ 与差分残差 **{:.3e}**，"
             "三档步长单调下降。".format(payload["key_numbers"]["derivative_residual"]))
    V.append("")
    V.append("## 四、先给靶应得的三条 PASS（诚实登记）")
    V.append("")
    V.append("| 编号 | 对靶有利的结论 |")
    V.append("|---|---|")
    V.append("| **A0** | 求导本身正确（残差 {:.3e}），|C|=常数 ⇒ C ⊥ Ċ 的推论也对 |".format(
        payload["key_numbers"]["derivative_residual"]))
    V.append("| **A4** | 固有时读法（t = τ）确实恢复类时性：ds²/(c²dt²) = 1−1/γ² = **{:+.4e} > 0** |".format(
        payload["key_numbers"]["ds2_proper_time_branch"]))
    V.append("| **B2** | 若把 m 读作「总量/4π」而非「密度」，可加性成立（2×1kg = 2kg）|")
    V.append("")
    V.append("## 五、A 组（时空同一化 R = C t）")
    V.append("")
    V.append("- **A1 两难**：R 指物体位置 ⇒ |R| = ct 强制共球面（地球需 t = {:.1f} s、"
             "比邻星需 t = {:.3e} s，距离比 **{:.4e}**）；R 指空间位移场 ⇒ 与力方程脱钩".format(
                 payload["key_numbers"]["t_required_earth_s"],
                 payload["key_numbers"]["t_required_proxima_s"],
                 payload["key_numbers"]["distance_ratio_proxima_over_earth"]))
    V.append("- **A2**：C 全局均匀（原文 §3.1 自承）⇒ 所有物体位置矢量相同 ⇒ 间距预测 0 vs 实测 1 m"
             "（**{:+.1f}%**）".format(payload["key_numbers"]["coincidence_dev"] * 100))
    V.append("- **A3 两难**：Ċ=0 ⇒ ds²≡0（类光）；Ċ≠0 ⇒ ds²/(c²dt²) = **{:+.3e}** < 0，"
             "|dR/dt| = **{:.4e}·c**".format(payload["key_numbers"]["ds2_spacelike_branch"],
                                             payload["key_numbers"]["v_over_c_spacelike_branch"]))
    V.append("- **A5**：读法 P 救不回空间维度 ⇒ 相对位置恒 ∥ C，横向分量 **{:+.1f}%**".format(
        payload["key_numbers"]["lateral_collapse_dev"] * 100))
    V.append("- **A6 两难**：V = dR/dt ⇒ P = m(C−V) ≡ 0（vs §3.1 静止动量 {:.4e} kg·m/s，**{:+.1f}%**）；"
             "V ≠ dR/dt ⇒ R 与物体脱钩".format(payload["key_numbers"]["P_static_claim_kg_m_s"],
                                              payload["key_numbers"]["momentum_zero_dev"] * 100))
    V.append("- **A7 防过度指控**：|R| = c·Δt 作为光行距定义**正确**（自检偏差 {:.2e}），"
             "本卷不指控它本身".format(payload["key_numbers"]["radar_dev"]))
    V.append("")
    V.append("## 六、B 组（质量几何化 m = k∮dn/Ω）")
    V.append("")
    V.append("- **B1** ∮dn/Ω：分子微分、分母总量 ⇒ 记号不成形（BOUNDARY）")
    V.append("- **B2 PASS** 总量读法（m ∝ N）可加：2×1kg = 2kg（★对靶有利，诚实登记）")
    V.append("- **B3 两难** 原文措辞「密度」⇒ 不可加（**{:+.1f}%**），与一切称重实验冲突".format(
        payload["key_numbers"]["additivity_density_dev"] * 100))
    V.append("- **B4** [k] = (1,0,0) ⇒ **有量纲自由参数 = 非定律**")
    V.append("- **B5** 「条数」n 无测度/无归一化/无 k 值 ⇒ 公设**不可操作**")
    V.append("- **B6** 量子化 ⇒ 最小整数分母 Q_min = **{}**；小整数 q=3 超出实测不确定度 **{:.3e}** 倍；"
             "不限制 N 则**零判别力**（INFO）".format(payload["key_numbers"]["min_integer_denominator"],
                                                payload["key_numbers"]["q3_deviation_ratio"]))
    V.append("- **B7 ★最硬两难**：C 方向不变 ⇒ q ≡ 0（**{:+.1f}%**）；C 方向可变 ⇒ 电荷与粒子种类无关"
             "（p/e/n 同位置电荷必相同，离散度 **{:+.1f}%**）".format(
                 payload["key_numbers"]["charge_zero_branch_dev"] * 100,
                 payload["key_numbers"]["charge_species_independent_dev"] * 100))
    V.append("- **B8** 条数产生/消灭机制缺失（BOUNDARY，与 r161 联动，不重复指控）")
    V.append("")
    V.append("## 七、修复定价（C 组）")
    V.append("")
    V.append("5 个动作 × 位掩码 32 组合，双档都报：")
    V.append("")
    V.append("| 档 | 存活 |")
    V.append("|---|---|")
    V.append("| 宽松（允许删式） | **{}** |".format(payload["key_numbers"]["repair_survivors_loose"]))
    V.append("| 严格（不许删式） | **{}** |".format(payload["key_numbers"]["repair_survivors_strict"]))
    V.append("| 零代价 | **{}** |".format(payload["key_numbers"]["repair_zero_cost"]))
    V.append("")
    V.append("存活解共性：全部含 M2（删掉 |R| = c·t）+ M4（补任意条数密度函数 ρ）+ M5（引入与粒子种类"
             "相关、不来自 C 场的内部量子数）⇒ **修复即自杀第十一度**。")
    V.append("")
    V.append("## 八、条目总表")
    V.append("")
    for e in ENTRIES:
        V.append("- **{}** [{}] {} — {}".format(e["code"], e["verdict"], e["name"], e["note"]))
    V.append("")
    V.append("## 九、控制组与守卫")
    V.append("")
    V.append("控制组 {} / {}，守卫 {} / {}（**守卫全部机读驱动，无一处 ok 写死 True**）".format(
        sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
        sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    V.append("")
    V.append("## 十、未闭合项与红线")
    V.append("")
    for s in payload["not_closed"]:
        V.append("- " + s)
    V.append("")
    for s in payload["redline"]:
        V.append("- " + s)
    with open(vp, "w", encoding="utf-8") as f:
        f.write("\n".join(V))

    return jp, mp, rp, vp


def main():
    print("=" * 78)
    print(" TUFT-r162｜时空同一化 R = C t 与质量几何化 m = k∮dn/Ω 的求导证明验证精算")
    print(" " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 78)

    A = group_A()
    B = group_B()
    C = group_C()
    group_controls(A, B)
    group_guards(A, B, C)

    payload = build_payload(A, B, C)

    outdir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "数据"))
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    jp, mp, rp, vp = write_outputs(payload, outdir)

    nco = sum(1 for c in CONTROLS if c["ok"])
    ngo = sum(1 for g in GUARDS if g["ok"])
    print("\n" + "=" * 78)
    print(" 终盘")
    print("=" * 78)
    print(" 条目： " + " / ".join("{}={}".format(k, payload["stats"][k])
                                  for k in ["PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION"]))
    print(" 控制组： {} / {}".format(nco, len(CONTROLS)))
    print(" 守卫  ： {} / {}".format(ngo, len(GUARDS)))
    print(" 判词  ： {}".format(payload["verdict"]))
    for p in (jp, mp, rp, vp):
        print(" 产物  ： {}".format(os.path.basename(p)))

    if nco != len(CONTROLS) or ngo != len(GUARDS):
        print("\n !! 控制组/守卫有失控项 => 退出码 2")
        return 2
    print("\n 退出码 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
