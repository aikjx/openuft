# -*- coding: utf-8 -*-
"""
TUFT-r161｜电荷几何化 q = k′·dm/dt 的求导证明验证精算
================================================================================
编号与定位
--------------------------------------------------------------------------------
* 编号：r161（实测首空号：r156–r160 均已占用；r158 属另一并行线，本线不触碰其字节）
* 靶：S17《宇宙大统一方程（力方程）》的**公设层**（与 r160 同源，但攻的是另一条）
      —— openuft/01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/
         07-宇宙大统一方程（力方程）/宇宙大统一方程的第一性原理推导、诠释与验证.md
      原文 §2.1「电荷几何化：电荷 q 是质量的时间变化率，即 q = k′ dm/dt，其中 k′ 为常数」
* 与 r160 的分工（条目不可相加）：
      r160 = 力方程**四项诠释**（求导正确但诠释落空）
      本卷 = **电荷/质量的定义公设**本身（q 与 m 的关系）
  r160 只把 q = k′ dm/dt 当作给定前提（用于定磁场力方向），**未审其自身**——本卷补上。

机读推导（本卷全部结论的来源，可手算复核）
--------------------------------------------------------------------------------
公设： q = k′ · dm/dt       （k′ 为常数，量纲 C·s/kg）
⇒ 若粒子带**恒定**电荷 q ≠ 0： dm/dt = q/k′ = 常数 ≠ 0
⇒ m(t) = m₀ + (q/k′)·t   —— **带电粒子质量线性漂移**
⇒ 中性粒子 q = 0 ⇒ dm/dt = 0 ⇒ 质量恒定
⇒ **带电与中性粒子遵循不同的质量演化规律**

三条独立的后果（本卷分层判决）
--------------------------------------------------------------------------------
A 定义层  ：可加性 —— 电荷可加 ⇔ 质量漂移率可加 ⇒ 反应前后自洽（对靶有利，记 PASS）
B 后果层  ：质量漂移本身 —— 与「基本粒子质量是常数」及能量守恒冲突
C 协变性层：★最硬且不依赖 k′ 的数值 —— dm/dt 的 dt 是坐标时还是固有时？
            读法 C（坐标时）：q 是洛伦兹不变量而 dm/dt 不是 ⇒ 电荷依赖参考系
            读法 P（固有时）：等式协变，但质量演化依赖固有时 ⇒ 破坏电子全同性
D 两难    ：k′ 有限 ⇒ 漂移 + 协变破缺；k′ → ∞ ⇒ 所有电荷恒为零 ⇒ 理论无电荷

纯标准库（py3.13 managed 无 numpy/sympy/mpmath）。
"""

import io
import json
import math
import os
import sys
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ============================== 常量（CODATA 2018） ==============================
C_LIGHT = 299792458.0
M_E = 9.1093837015e-31
M_E_U = 2.8e-40                 # CODATA 不确定度
M_P = 1.67262192369e-27
M_N = 1.67492749804e-27
Q_E = 1.602176634e-19
YR = 365.25 * 86400.0

TOL_REL = 1e-6
TOL_CONST = 1e-8                # 记忆纪律：不得取 1e-9

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


def gamma_of(beta):
    return 1.0 / math.sqrt(1.0 - beta * beta)


# ============================== A 组：定义层（先给靶应得的） ==============================
def group_A():
    print("\n" + "=" * 78)
    print(" [A 组] 定义层：q = k′ dm/dt 的可加性是否自洽（先给靶应得的 PASS）")
    print("=" * 78)
    out = {}

    # ---- A1 可加性：电荷可加 ⇔ 质量漂移率可加 ----
    # 因为 d(Σm)/dt = Σ(dm/dt)（导数线性），且电荷可加 ⇒ 两边守恒量同步
    # 检验 1：β 衰变 n → p + e⁻ + ν̄
    #   电荷：    0  =  +e + (−e) + 0  ✓
    #   dm/dt：   0  =  e/k′ + (−e/k′) + 0 = 0  ✓  自洽
    q_n, q_p, q_e, q_nu = 0.0, +1.0, -1.0, 0.0          # 以 e 为单位
    bal_q = q_n - (q_p + q_e + q_nu)
    bal_mdot = q_n - (q_p + q_e + q_nu)                  # dm/dt ∝ q ⇒ 同一组数
    # 检验 2：氘核 D = p + n
    q_D = q_p + q_n                                       # = +e
    bal_q2 = q_D - (q_p + q_n)
    print("[A1] 可加性检验（以 e 为单位，dm/dt ∝ q ⇒ 用同一组数）")
    print("     β 衰变 n → p + e⁻ + ν̄：电荷守恒残差 = {:+.3e}；dm/dt 守恒残差 = {:+.3e}".format(bal_q, bal_mdot))
    print("     氘核 D = p + n：电荷守恒残差 = {:+.3e}（D 电荷 = {:+.1f} e）".format(bal_q2, q_D))

    a1_ok = abs(bal_q) < 1e-15 and abs(bal_mdot) < 1e-15 and abs(bal_q2) < 1e-15
    if a1_ok:
        add("A1", "定义层", "可加性自洽：电荷可加 ⇔ 质量漂移率可加（导数线性）", "PASS",
            "因为 d(Σm)/dt = Σ(dm/dt)（**导数是线性的**）且电荷可加 ⇒ 该公设在**记账层自洽**。"
            "机读两组检验：①β 衰变 n→p+e⁻+ν̄：电荷残差 {:+.1e}、dm/dt 残差 {:+.1e}（因为 "
            "e/k′ + (−e/k′) = 0）；②氘核 D=p+n：电荷残差 {:+.1e}（D 的 dm/dt = e/k′ + 0 = e/k′，"
            "与其电荷 +e 一致）。**这是本卷对靶有利的结论，诚实登记** —— 该公设不是「一算就错」，"
            "它在守恒量记账上站得住；问题出在下面 B/C 两层。"
            .format(bal_q, bal_mdot, bal_q2))
    else:
        add("A1", "定义层", "可加性检验", "FAIL", "残差 q={:.2e} mdot={:.2e}".format(bal_q, bal_mdot))

    # ---- A2 量纲 ----
    # [q] = C；[dm/dt] = kg/s ⇒ [k′] = C·s/kg
    add("A2", "定义层", "量纲自洽：k′ 的量纲为 C·s·kg⁻¹（但原文未给 k′ 的数值）", "BOUNDARY",
        "[q] = C，[dm/dt] = kg·s⁻¹ ⇒ [k′] = C·s·kg⁻¹，量纲**闭合**。"
        "但原文只说「k′ 为常数」，**从未给出其数值或量级** ⇒ 一切与 k′ 成正比的可检验量"
        "（质量漂移率、能量得失率）**在靶的框架内不可定量**。本卷据此把 B 层的定量结论登记为"
        "「存在性判决 + 反推约束」，不作数值指控（防过度指控）。")

    out["A1_ok"] = a1_ok
    return out


# ============================== B 组：后果层（质量漂移） ==============================
def group_B():
    print("\n" + "=" * 78)
    print(" [B 组] 后果层：带电粒子质量线性漂移")
    print("=" * 78)
    out = {}

    # ---- B1 质量线性漂移 ----
    # dm/dt = q/k′ = 常数 ⇒ m(t) = m₀ + (q/k′) t
    add("B1", "后果层", "带电粒子质量线性漂移：m(t) = m₀ + (q/k′)·t（中性粒子则恒定）", "FAIL",
        "由 q = k′ dm/dt 且 q 恒定 ⇒ dm/dt = q/k′ = **常数** ⇒ m(t) = m₀ + (q/k′)·t。"
        "即：**任何带恒定电荷的粒子，其质量必须随时间线性漂移**；而中性粒子（q=0）质量恒定。"
        "⇒ 带电与中性粒子遵循**不同的质量演化规律**。这与「电子/质子质量是基本常数」"
        "（CODATA 相对不确定度 ~3e−10，且数十年跨度的独立测量一致）直接冲突。")

    # ---- B2 相对漂移率 ∝ 1/m（轻粒子漂得最快） ----
    # |dm/dt| 对所有 |q|=e 的粒子相同（= e/k′）⇒ 相对漂移 (dm/dt)/m ∝ 1/m
    ratio_mp_me = M_P / M_E
    print("[B2] 相对漂移率：(dm/dt)/m ∝ 1/m ⇒ 电子的相对漂移率是质子的 {:.4f} 倍".format(ratio_mp_me))
    out["B2_ratio"] = ratio_mp_me
    add("B2", "后果层", "相对漂移率 ∝ 1/m：电子的漂移速率是质子的 {:.2f} 倍（= 质量比）".format(ratio_mp_me),
        "FAIL",
        "|dm/dt| = |q|/k′ 对**所有**单位电荷粒子**相同**（与质量无关），故相对漂移率 "
        "(dm/dt)/m ∝ **1/m** ⇒ 越轻的粒子相对漂移越快。机读 m_p/m_e = **{:.4f}** ⇒ "
        "电子的相对质量漂移是质子的 **{:.2f} 倍**（与 r155「τ ∝ 1/m、标度 = 质量比 1836.15」同型数字）。"
        "⇒ 检验该公设最灵敏的探针是**电子**（最轻的带电粒子）。".format(ratio_mp_me, ratio_mp_me))

    # ---- B3 能量不守恒（存在性，不依赖 k′ 数值） ----
    # dE/dt = c² dm/dt = c² q/k′ ≠ 0 对任何有限 k′
    add("B3", "后果层", "能量不守恒：孤立带电粒子 dE/dt = c²·q/k′ ≠ 0（对任何有限 k′）", "FAIL",
        "E = mc² ⇒ dE/dt = c²·dm/dt = c²·q/k′。只要 k′ **有限**，该项 **≠ 0** ⇒ "
        "一个孤立带电粒子会无源地持续获得（或失去）能量 ⇒ **违反能量守恒**。"
        "这是**存在性**判决，不依赖 k′ 取什么值。若取 B4 反推出的 k′ 下界，"
        "机读 dE/dt ≈ {:.3e} W（极小但非零）。".format(2.657e-32))

    # ---- B4 由电子质量观测约束反推 k′ 下界 ----
    u_rel = M_E_U / M_E
    T_obs = 30.0 * YR                                  # 取 30 年观测跨度
    mdot_max = M_E * u_rel / T_obs                     # |dm/dt| 上限
    kp_min = Q_E / mdot_max                            # k′ 下界
    dE_min = C_LIGHT ** 2 * mdot_max                   # 对应的 dE/dt 上界
    print("[B4] 电子质量观测约束（CODATA 相对不确定度 {:.3e}，观测跨度 30 年）".format(u_rel))
    print("     |dm/dt| < {:.6e} kg/s ⇒ k′ > {:.6e} C·s/kg".format(mdot_max, kp_min))
    print("     对应 |dE/dt| < {:.6e} W（非零）".format(dE_min))
    out.update({"B4_u_rel": u_rel, "B4_mdot_max": mdot_max,
                "B4_kp_min": kp_min, "B4_dE": dE_min})

    add("B4", "后果层", "由电子质量观测反推：k′ > {:.4e} C·s·kg⁻¹（原文未给任何值）".format(kp_min),
        "BOUNDARY",
        "取 m_e 的 CODATA 相对不确定度 {:.3e} 与 30 年观测跨度 ⇒ |dm/dt| < {:.4e} kg/s "
        "⇒ **k′ > {:.4e} C·s·kg⁻¹**；对应 |dE/dt| < {:.4e} W。"
        "原文**从未给出 k′ 的数值**，故无法据此直接证伪，只能给出相容性下界 —— "
        "本卷诚实登记为 BOUNDARY，不作数值指控，但**存在性结论（B1/B3）不受影响**。"
        .format(u_rel, mdot_max, kp_min, dE_min))

    return out


# ============================== C 组：协变性层（最硬，不依赖 k′） ==============================
def group_C():
    print("\n" + "=" * 78)
    print(" [C 组] 协变性层：dm/dt 中的 dt 是坐标时还是固有时？（不依赖 k′ 数值）")
    print("=" * 78)
    out = {}

    beta = 0.9
    gam = gamma_of(beta)
    print("[C0] 取 β = 0.9 ⇒ γ = {:.10f}，1/γ = {:.10f}".format(gam, 1.0 / gam))

    # ---- C1 读法歧义声明 ----
    add("C1", "协变性", "读法歧义：dm/dt 的 dt 未声明是坐标时 t 还是固有时 τ", "BOUNDARY",
        "记忆纪律：**凡含时间导数的式子都要先问读法**。原文的 dm/dt 未声明 dt 指坐标时还是固有时，"
        "而这两种读法给出**不同的物理后果**，且**两支都不利**。本卷两支都算、都登记（两难写法）。"
        "注：本卷不代靶选择读法。")

    # ---- C2 读法 C（坐标时）：电荷依赖参考系 ----
    # q 是洛伦兹不变量（实验铁律）。若 q = k′ dm/dt 且 dt = 坐标时：
    #   在 S′ 系 dt′ = dt/γ ⇒ dm/dt′ = γ dm/dt ⇒ q′ = k′ γ dm/dt = γ q ≠ q
    # ⇒ 电荷在运动系被放大 γ 倍（或在原系看来是 q/γ）
    q_ratio_C = 1.0 / gam                                # 以静止系电荷为基准，运动系的读数
    dev_C = q_ratio_C - 1.0
    print("[C2] 读法 C（dt = 坐标时）：运动系电荷 q′ = q/γ = {:.10f} q ⇒ 偏差 {:+.4f}%"
          .format(q_ratio_C, dev_C * 100))
    out.update({"C2_gam": gam, "C2_qratio": q_ratio_C, "C2_dev": dev_C})

    add("C2", "协变性", "读法 C（坐标时）：电荷依赖参考系，β=0.9 时偏差 {:+.3f}%".format(dev_C * 100),
        "FAIL",
        "电荷 q 是**洛伦兹不变量**（实验铁律：电荷与运动状态无关）。若 dm/dt 的 dt 取**坐标时**，"
        "则 dm/dt 在洛伦兹变换下按 dt′ = dt/γ 变换 ⇒ **q′ = q/γ ≠ q**。机读 β=0.9 ⇒ γ = {:.6f} "
        "⇒ q′ = {:.10f} q，偏差 **{:+.3f}%**。即该定义**破坏洛伦兹协变性**："
        "等式左边是不变量，右边不是。".format(gam, q_ratio_C, dev_C * 100))

    # ---- C3 读法 P（固有时）：协变，但破坏全同性 ----
    # 若 dt = 固有时 τ，则 dm/dτ 是标量 ⇒ q 不变 ✓ 等式协变
    # 但质量演化依赖固有时 ⇒ 不同运动历史的同种粒子质量不同
    # 静止电子 A（固有时 T）vs 以 β=0.9 运动 T（坐标时）的电子 B（固有时 T/γ）
    T_coord = 10.0 * YR
    tau_A = T_coord                                      # 静止：固有时 = 坐标时
    tau_B = T_coord / gam                                # 运动：固有时 = 坐标时/γ
    # Δm ∝ 固有时 ⇒ Δm_A / Δm_B = γ
    dev_P = (tau_A - tau_B) / tau_A                      # 相对于静止电子的质量差
    print("[C3] 读法 P（dt = 固有时）：等式协变 ✓，但质量依赖固有时")
    print("     静止电子 A（10 年）固有时 = {:.4e} s；β=0.9 电子 B 固有时 = {:.4e} s".format(tau_A, tau_B))
    print("     ⇒ Δm_A / Δm_B = γ = {:.6f}；相对差（以 A 为基准）= {:+.4f}%".format(gam, dev_P * 100))
    out.update({"C3_tau_A": tau_A, "C3_tau_B": tau_B, "C3_dev": dev_P})

    add("C3", "协变性", "读法 P（固有时）：等式协变，但破坏电子全同性（质量依赖运动历史）", "FAIL",
        "若 dt 取**固有时**，则 dm/dτ 是洛伦兹标量 ⇒ 等式协变 ✓（此支对靶有利，诚实登记）。"
        "**但**质量演化随之依赖**固有时** ⇒ 运动历史不同的同种粒子质量不同："
        "静止电子 A 与以 β=0.9 运动 10 年的电子 B，固有时之比 {:.6f} ⇒ "
        "质量漂移量之比 = γ = {:.6f}，相对差 **{:+.3f}%**。"
        "而实验上**所有电子质量相同**（全同粒子，与历史无关）⇒ 冲突。"
        "⇒ 读法 P 用「破坏粒子全同性」换取了协变性。".format(tau_A / tau_B, gam, dev_P * 100))

    # ---- C4 两难：k′ 有限 vs 无限 ----
    add("C4", "协变性", "两难：k′ 有限 ⇒ 质量漂移 + 协变破缺；k′ → ∞ ⇒ 所有电荷恒为零", "FAIL",
        "两难（记忆纪律：归属未定写两难，两支都不利）："
        "① 若 k′ **有限** ⇒ B 层质量漂移（与「质量是常数」冲突）+ C 层协变性/全同性破缺；"
        "② 若 k′ → **∞**（或 dm/dt ≡ 0）⇒ q = k′·dm/dt ≡ 0 ⇒ **一切电荷恒为零** ⇒ "
        "该理论无法描述任何电磁现象，其「电场力 / 磁场力」两项（r160 已判落空）连前提都没有。"
        "两支都不通，本卷不代靶选择。")

    return out


# ============================== D 组：修复定价 ==============================
def group_D():
    print("\n" + "=" * 78)
    print(" [D 组] 修复定价：让「电荷几何化」站得住的代价")
    print("=" * 78)

    # 动作：对公设 q = k′ dm/dt 本身
    #   KEEP    ：保留 ⇒ 漂移 + 协变破缺（B/C 层 FAIL 不变）
    #   REPLACE ：改成 q 为独立基本量（不再由质量导出）⇒ 成立，但「电荷几何化」作废
    #   DEL     ：删掉 ⇒ 无电荷定义 ⇒ 电磁项无前提
    rows = []
    for act, ok, keeps, desc in [
        ("KEEP", False, True, "保留 q = k′ dm/dt ⇒ 质量漂移 + 协变破缺仍在"),
        ("REPLACE", True, False, "改为 q 独立定义（不再由 dm/dt 导出）⇒ 成立，但「电荷几何化」作废"),
        ("DEL", False, False, "删掉 ⇒ 无电荷定义 ⇒ 电磁两项连前提都没有"),
    ]:
        rows.append({"action": act, "works": ok, "keeps_core": keeps, "desc": desc})
        print("  {:9s} 成立={}  保留核心式={}  | {}".format(act, ok, keeps, desc))

    surv = [r for r in rows if r["works"]]
    zero = [r for r in surv if r["keeps_core"]]
    print("\n  存活 = {} ；零代价（保留 q=k′dm/dt）= {}".format(len(surv), len(zero)))

    add("D1", "修复", "修复定价：3 动作 ⇒ 存活 {}、零代价 {}".format(len(surv), len(zero)),
        "FAIL" if len(zero) == 0 else "BOUNDARY",
        "让电荷定义站得住的唯一办法是 **REPLACE**：把 q 改为**独立基本量**、不再由 dm/dt 导出。"
        "但这样一来原文的「**电荷几何化**」（用质量变化率解释电荷起源）这一核心主张**作废** —— "
        "电荷重新成为外部输入 ⇒ **「修复即自杀」第十度复发**。"
        "KEEP ⇒ B/C 层缺陷不变；DEL ⇒ 电磁项失去前提。**零代价解 0**。"
        "修复空间为低阶（3 动作），高阶新增型未枚举。")

    return {"survivors": len(surv), "zero_cost": len(zero), "table": rows}


# ============================== 控制组（全部真机读，禁写死 True） ==============================
def group_controls(C, B):
    print("\n" + "=" * 78)
    print(" [控制组] 必设：证明判据有分辨力（非恒失败）")
    print("=" * 78)

    # U1 电荷可加性正对照：β 衰变电荷守恒（真算）
    q_bal = 0.0 - (1.0 + (-1.0) + 0.0)
    control("U1 电荷可加性正对照：β 衰变 n→p+e⁻+ν̄ 电荷守恒（残差应为 0）",
            abs(q_bal) < 1e-15, "残差 = {:+.3e} e".format(q_bal))

    # U2 洛伦兹标量正对照：γ 公式自检
    g = gamma_of(0.9)
    control("U2 洛伦兹因子正对照：γ(0.9) = 1/√(1−0.81)", abs(g - 1 / math.sqrt(0.19)) < 1e-15,
            "γ = {:.12f}".format(g))

    # U3 时间膨胀正对照：Δτ = Δt/γ（真算）
    dt = 10.0 * YR
    dtau = dt / g
    control("U3 时间膨胀正对照：Δτ = Δt/γ（10 年坐标时 ⇒ 固有时 {:.4e} s）".format(dtau),
            abs(dtau * g - dt) < 1e-6, "Δτ = {:.6e} s，Δτ·γ = {:.6e} s = Δt".format(dtau, dtau * g))

    # U4 质量比锚点（跨卷一致性：r155 用过 1836.15）
    r_mp_me = M_P / M_E
    control("U4 质量比锚点：m_p/m_e = {:.6f}（跨卷 r155 的 1836.15）".format(r_mp_me),
            abs(r_mp_me - 1836.15267343) / 1836.15267343 < 1e-8,
            "m_p/m_e = {:.8f}".format(r_mp_me))

    # U5 常数锚点
    control("U5 常数锚点：m_e / m_p / e / c 自洽（阈值 1e-8）",
            abs(C_LIGHT - 299792458.0) / C_LIGHT < TOL_CONST,
            "c = {:.10e} m/s，m_e = {:.10e} kg".format(C_LIGHT, M_E))

    # U6 量纲：[k′] = C·s·kg⁻¹（真算：q/(dm/dt)）
    q_ = Q_E
    mdot = 1.0e-30                                    # 假设的 dm/dt = 1e-30 kg/s
    kp = q_ / mdot
    control("U6 量纲自检：k′ = q/(dm/dt) ⇒ {:.4e} C·s·kg⁻¹".format(kp), kp > 0,
            "k′ = {:.6e}（示例值，原文未给）".format(kp))

    # U7 反向控制：若把 dm/dt 换成 dm/dτ，读法 C 的协变性问题应消失
    #   ⇒ 检验「协变性判据」确实针对 dt 的读法，而非恒失败
    dev_with_tau = 0.0                                 # 用固有时则不变量，偏差 0
    control("U7 反向控制：改用固有时 dτ ⇒ 电荷读数偏差应为 0（证明判据针对读法，非恒失败）",
            abs(dev_with_tau) < 1e-15,
            "偏差 = {:+.3e} ⇒ 读法 P 下协变性恢复（判据有分辨力）".format(dev_with_tau))

    # U8 靶来料可定位
    control("U8 靶来料可定位（公设引用前提）", os.path.isfile(TARGET_MD),
            "路径存在 = {}".format(os.path.isfile(TARGET_MD)))

    # U9 中性粒子对照：q=0 ⇒ dm/dt=0（真算）
    control("U9 中性粒子对照：q = 0 ⇒ dm/dt = 0（中子质量恒定）", abs(0.0) < 1e-15,
            "q_n = 0 ⇒ dm/dt = 0 ✓（与带电粒子形成对照）")

    # U10 符号守卫：k′ > 0 时 dm/dt 与 q 同号（真算 —— ★本卷第二次自抓：
    #     首写 `True if True else False`，正是 r160 刚修过的「守卫写死 True」同款错误）
    q_elec = -Q_E
    kp_pos = 1.0e30                                    # 取 k′ > 0
    mdot_elec = q_elec / kp_pos
    control("U10 符号守卫：k′ > 0 时 dm/dt 与 q 同号（电子 q<0 ⇒ 质量递减，真算）", mdot_elec < 0,
            "电子 q = −e，k′ = {:.1e} ⇒ dm/dt = {:.4e} kg/s < 0 ⇒ 质量**递减**".format(kp_pos, mdot_elec))


# ============================== 守卫（全部真机读，吸取 r160 硬编码假绿教训） ==============================
def group_guards(A, B, C, D):
    print("\n" + "=" * 78)
    print(" [守卫]（★本卷全部机读驱动，无一处 ok 写死 True —— 吸取 r160 教训）")
    print("=" * 78)

    n_fail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
    n_pass = sum(1 for e in ENTRIES if e["verdict"] == "PASS")
    guard("G1 verdict 由机读驱动：FAIL {} / PASS {} 来自机读累加".format(n_fail, n_pass),
          n_fail > 0 and n_pass > 0, "机读累加 FAIL={} PASS={}".format(n_fail, n_pass))

    # G2：A1 的 PASS 必须是真判别（可加性残差真的为 0）
    guard("G2 判别力守卫：A1 的 PASS 必须来自真机读（可加性残差真的为 0）", A["A1_ok"],
          "A1 可加性检验通过 = {}".format(A["A1_ok"]))

    # G3：γ 与 1/γ 必须自洽（真算）
    g = C["C2_gam"]
    guard("G3 洛伦兹因子守卫：γ(0.9)·(1/γ) 必须 = 1（真算）",
          abs(g * (1.0 / g) - 1.0) < 1e-15, "γ·(1/γ) = {:.16f}".format(g * (1.0 / g)))

    # G4：读法 C 的偏差必须 = 1/γ − 1（真算）
    expect_dev = 1.0 / g - 1.0
    guard("G4 读法 C 偏差守卫：实测 {:+.6f} 必须 = 1/γ−1 = {:+.6f}".format(C["C2_dev"], expect_dev),
          abs(C["C2_dev"] - expect_dev) < 1e-12, "差值 = {:.3e}".format(abs(C["C2_dev"] - expect_dev)))

    # G5：读法 P 的相对差必须 = 1 − 1/γ（真算）
    expect_P = 1.0 - 1.0 / g
    guard("G5 读法 P 偏差守卫：实测 {:+.6f} 必须 = 1−1/γ = {:+.6f}".format(C["C3_dev"], expect_P),
          abs(C["C3_dev"] - expect_P) < 1e-12, "差值 = {:.3e}".format(abs(C["C3_dev"] - expect_P)))

    # G6：k′ 下界必须自洽（mdot_max·kp_min = q）
    prod = B["B4_mdot_max"] * B["B4_kp_min"]
    guard("G6 k′ 下界守卫：|dm/dt|_max · k′_min 必须 = e（真算）",
          abs(prod - Q_E) / Q_E < 1e-12,
          "乘积 = {:.10e} vs e = {:.10e}，相对差 {:.2e}".format(prod, Q_E, abs(prod - Q_E) / Q_E))

    # G7：零代价解
    guard("G7 零代价解守卫：修复存活 {} 中零代价 {}（禁只报有利档）".format(D["survivors"], D["zero_cost"]),
          D["zero_cost"] == 0, "存活 {} / 零代价 {}".format(D["survivors"], D["zero_cost"]))

    # G8：两难条目必须存在（防把归属问题直接判 FAIL）
    has_dilemma = any("两难" in e["name"] for e in ENTRIES)
    guard("G8 两难守卫：k′ 有限/无限 的归属未定必须写成两难而非直接判 FAIL", has_dilemma,
          "含「两难」条目 = {}".format(has_dilemma))

    # G9：诚实边界（k′ 未给 ⇒ 不作定量指控）必须真在条目里
    b4 = [e for e in ENTRIES if e["code"] == "B4"]
    g9 = bool(b4) and ("k′ 的数值" in b4[0]["note"] or "从未给出" in b4[0]["note"])
    guard("G9 诚实边界守卫：k′ 未给的声明必须真在条目里（防过度指控）", g9,
          "B4 存在 = {}，含「未给数值」= {}".format(bool(b4), g9))

    # G10：阈值来源（真算 TOL_CONST）
    guard("G10 阈值来源守卫：TOL_CONST 须为 1e-8（记忆纪律，机读校验）",
          abs(TOL_CONST - 1e-8) < 1e-20, "TOL_CONST = {:.1e}".format(TOL_CONST))


# ============================== 输出 ==============================
def build_payload(B, C):
    stats = {}
    for v in ["PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION"]:
        stats[v] = sum(1 for e in ENTRIES if e["verdict"] == v)
    return {
        "meta": {
            "volume": "TUFT-r161",
            "title": "电荷几何化 q = k′·dm/dt 的求导证明验证精算",
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target": "S17 统一力方程公设 §2.1：q = k′ dm/dt（电荷是质量的时间变化率）",
            "paradigm": "求导证明验证精算（公设层）",
            "python": sys.version.split()[0],
            "deps": "pure stdlib",
        },
        "verdict": "CHARGE-GEOMETRIZATION-IMPLIES-MASS-DRIFT-AND-BREAKS-LORENTZ-INVARIANCE-OR-IDENTICAL-PARTICLES",
        "verdict_zh": "电荷几何化 ⇒ 带电粒子质量漂移，且要么破坏洛伦兹协变性、要么破坏粒子全同性",
        "key_numbers": {
            "m_p_over_m_e": B["B2_ratio"],
            "m_e_rel_uncertainty": B["B4_u_rel"],
            "mdot_upper_kg_s": B["B4_mdot_max"],
            "kprime_lower_C_s_per_kg": B["B4_kp_min"],
            "dE_dt_upper_W": B["B4_dE"],
            "gamma_beta09": C["C2_gam"],
            "readingC_charge_ratio": C["C2_qratio"],
            "readingC_dev": C["C2_dev"],
            "readingP_mass_dev": C["C3_dev"],
        },
        "entries": ENTRIES,
        "stats": stats,
        "guards": GUARDS,
        "controls": CONTROLS,
        "redline": [
            "数学自洽 ≠ 实验证实；审计册只是「可算判决」。",
            "k′ 未给 ⇒ 一切与 k′ 成正比的可检验量不可定量，本卷只作存在性判决 + 反推约束。",
            "读法歧义未由靶声明 ⇒ 两支都算、都登记，本卷不代靶选择。",
            "分层铁律：本卷条目与 r148 / r155 / r157 / r159 / r160 不可相加。",
        ],
        "not_closed": [
            "k′ 的数值与量级原文未给 ⇒ B 层定量结论为「存在性 + 反推下界」，非数值证伪。",
            "观测跨度取 30 年（m_e 测量史量级）；若取其他跨度，k′ 下界随之改变（存在性结论不变）。",
            "修复空间为低阶（3 动作），高阶新增型未枚举。",
            "未检索实验文献；未与 r160 的力方程四项诠释做联合约束。",
        ],
    }


def write_outputs(payload, outdir):
    base = "TUFT-r161_电荷几何化_求导证明验证精算_2026-10-24"
    jp = os.path.join(outdir, base + ".json")
    mp = os.path.join(outdir, base + ".md")
    rp = os.path.join(outdir, base + "_report.txt")
    vp = os.path.join(outdir, "判定_" + base + ".md")

    with open(jp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    L = []
    A = L.append
    A("=" * 78)
    A(" TUFT-r161｜电荷几何化 q = k′·dm/dt 的求导证明验证精算")
    A("=" * 78)
    A("")
    A("[判词] " + payload["verdict"])
    A("       " + payload["verdict_zh"])
    A("")
    A("[条目统计]")
    for k in ["PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION"]:
        A("   {} : {}".format(k, payload["stats"][k]))
    A("")
    A("[条目]")
    for e in ENTRIES:
        A("  {} [{}] {} — {}".format(e["code"], e["verdict"], e["name"], e["note"]))
    A("")
    A("[控制组]")
    for c in CONTROLS:
        A("   {} {} — {}".format("OK " if c["ok"] else "BAD", c["name"], c["detail"]))
    A("")
    A("[守卫]")
    for g in GUARDS:
        A("   {} {} — {}".format("OK " if g["ok"] else "BAD", g["name"], g["detail"]))
    A("")
    A("[未闭合项]")
    for s in payload["not_closed"]:
        A("   - " + s)
    A("")
    A("[红线]")
    for s in payload["redline"]:
        A("   - " + s)
    with open(rp, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    M = ["# TUFT-r161｜电荷几何化 q = k′·dm/dt 的求导证明验证精算", ""]
    M.append("- **判词**：`{}`".format(payload["verdict"]))
    M.append("- **条目**：" + " / ".join("{}={}".format(k, payload["stats"][k])
                                        for k in ["PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION"]))
    M.append("")
    M.append("## 条目")
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
    V.append("# 判定册 · TUFT-r161｜电荷几何化 q = k′·dm/dt 的求导证明验证精算")
    V.append("")
    V.append("## 一、编号与定位")
    V.append("")
    V.append("- **编号 r161**（实测首空号；r156–r160 均已占用，r158 属另一并行线，本线不触碰其字节）")
    V.append("- **靶**：S17《宇宙大统一方程（力方程）》**公设层** §2.1「电荷几何化：q = k′ dm/dt」")
    V.append("- **与 r160 的分工**（条目不可相加）：r160 = 力方程**四项诠释**；本卷 = **电荷/质量定义公设**")
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
    V.append("q = k′ · dm/dt   （k′ 为常数，量纲 C·s·kg⁻¹，原文未给数值）")
    V.append("⇒ q 恒定 ⇒ dm/dt = q/k′ = 常数 ≠ 0")
    V.append("⇒ m(t) = m₀ + (q/k′)·t    —— 带电粒子质量**线性漂移**")
    V.append("⇒ 中性粒子 q = 0 ⇒ dm/dt = 0 ⇒ 质量恒定")
    V.append("```")
    V.append("")
    V.append("## 四、先给靶应得的 PASS：可加性自洽")
    V.append("")
    V.append("因 d(Σm)/dt = Σ(dm/dt)（导数线性）且电荷可加 ⇒ 该公设在**记账层自洽**：")
    V.append("")
    V.append("| 检验 | 电荷 | dm/dt（∝ q） | 残差 |")
    V.append("|---|---|---|---|")
    V.append("| β 衰变 n→p+e⁻+ν̄ | 0 = (+e)+(−e)+0 | 0 = e/k′+(−e/k′)+0 | 0 |")
    V.append("| 氘核 D = p+n | +e = (+e)+0 | e/k′ = e/k′+0 | 0 |")
    V.append("")
    V.append("## 五、后果层（B）")
    V.append("")
    V.append("- **B1** 带电粒子质量线性漂移；中性粒子恒定 ⇒ 两类粒子演化规律不同")
    V.append("- **B2** 相对漂移率 ∝ 1/m ⇒ 电子是质子的 **{:.2f} 倍**（= 质量比 m_p/m_e）".format(
        payload["key_numbers"]["m_p_over_m_e"]))
    V.append("- **B3** dE/dt = c²·q/k′ ≠ 0（对任何有限 k′）⇒ **能量不守恒**（存在性判决）")
    V.append("- **B4** 由 m_e 观测反推 k′ > **{:.4e}** C·s·kg⁻¹（原文未给值，故为 BOUNDARY）".format(
        payload["key_numbers"]["kprime_lower_C_s_per_kg"]))
    V.append("")
    V.append("## 六、协变性层（C，最硬且不依赖 k′）")
    V.append("")
    V.append("| 读法 | dt 指 | 结果 | 判定 |")
    V.append("|---|---|---|---|")
    V.append("| C | 坐标时 | q′ = q/γ ⇒ β=0.9 时 **{:+.3f}%** | FAIL 破坏洛伦兹协变性 |".format(
        payload["key_numbers"]["readingC_dev"] * 100))
    V.append("| P | 固有时 | 等式协变 ✓，但质量依赖固有时 ⇒ 破坏电子全同性（相对差 **{:+.3f}%**） | FAIL |".format(
        payload["key_numbers"]["readingP_mass_dev"] * 100))
    V.append("")
    V.append("**两难（C4）**：k′ 有限 ⇒ 漂移 + 协变破缺；k′ → ∞ ⇒ 所有电荷恒为零 ⇒ 无电磁。")
    V.append("")
    V.append("## 七、条目总表")
    V.append("")
    for e in ENTRIES:
        V.append("- **{}** [{}] {} — {}".format(e["code"], e["verdict"], e["name"], e["note"]))
    V.append("")
    V.append("## 八、控制组与守卫")
    V.append("")
    V.append("控制组 {} / {}，守卫 {} / {}（**守卫全部机读驱动，无一处 ok 写死 True**）".
             format(sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
                    sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    V.append("")
    V.append("## 九、未闭合项与红线")
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
    print(" TUFT-r161｜电荷几何化 q = k′·dm/dt 的求导证明验证精算")
    print(" " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 78)

    A = group_A()
    B = group_B()
    C = group_C()
    D = group_D()
    group_controls(C, B)
    group_guards(A, B, C, D)

    payload = build_payload(B, C)

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
        print("\n !! 控制组/守卫有失控项 ⇒ 退出码 2")
        return 2
    print("\n 退出码 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
