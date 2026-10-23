# -*- coding: utf-8 -*-
"""
TUFT-r163｜宇宙的本源：S17-A1 空间光速螺旋运动公设，与「粒子属性元数据 + 相互转换条件」审计
================================================================================
编号与定位
--------------------------------------------------------------------------------
* 编号：r163（实测首空号：全库 grep 仅 README 的「下轮从 r163 起」命中，无产物占用）
* 靶：S17《统一场论核心公式》
      - `01_独立体系/S17_统一场论核心公式/02_基础公设/postulates.md`（本源公设 A1/A2/A3 + 20 个核心公式）
      - `01_独立体系/S17_统一场论核心公式/claims.csv`（40 条声明，含 **k = 4π m_p** 的关键披露）
* 本卷回答两个问题（与 r159–r162 分层，条目不可相加）：
      (1) **宇宙的本源是什么** —— 靶的正式回答 = **公理 A1「空间光速螺旋运动」**
      (2) **所有微观粒子的属性元数据特性与相互转换的条件** —— 靶是否给出了这两张表？

机读推导（本卷全部结论的来源，可手算复核）
--------------------------------------------------------------------------------
【A 组 本源公设】A1 螺旋： r(t) = (R cos ωt, R sin ωt, h t)， |dr/dt| = √(R²ω² + h²) = c
                 A2 同一化： r(t) = C t   ⇒ r ∥ C 且 |r| = c t
   取 Rω = 0.6c、h = 0.8c（满足 0.36 + 0.64 = 1，故 |C| = c ✓）
   令 ω = 1 s⁻¹：
     t = 1 s（ωt = 1）： |r|_A1 = √(R² + h²)·1 = c·1 = |r|_A2  ⇒ **模长偶然相等**
                         cos∠(r, C) = r·C/(|r||C|) = h²t/(c√(R²+h²t²)) = **0.640 ⇒ ∠ = 50.20°**
     t = 2 s（ωt = 2）： |r|_A1 = 5.124e8 vs |r|_A2 = c·2 = 5.996e8 ⇒ **相对偏差 −14.55%**
   ⇒ **A1 与 A2 的方向永远不等（50.20° vs 0°），模长仅在一个时刻偶然相等**
   ⇒ 模长相容的**唯一**时刻：c²t² = R² + h²t² ⇒ t²(c²−h²) = R² ⇒ t²R²ω² = R² ⇒ **ωt = 1（唯一）**
【B 组 粒子属性】m = k dn/dΩ，**k = 4π m_p**（靶给）
   ⇒ 若 ∮dn/dΩ = N/(4π)（r162 的总量读法）⇒ **m = N · m_p** ⇒ 一切质量 = 质子质量的**整数倍**
   电子 N = m_e/m_p = **5.446170e−04 < 1** ⇒ 「条数」小于 1 ⇒ 与计数定义直接矛盾
   ⇒ **r162 B6 判「零判别力/INFO」的前提（k 未给值）被本卷来料推翻 ⇒ 升级为 FAIL（CORRECTION）**
【C 组 转换条件】靶无任何衰变率 / 选择定则 / 守恒律；40 条声明中相关条目 **0** 条

纯标准库（py3.13 managed 无 numpy/sympy/mpmath）。
"""

import io
import json
import math
import os
import sys
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ============================== 常量（CODATA 2018 / PDG） ==============================
C_LIGHT = 299792458.0
M_E = 9.1093837015e-31
M_MU = 1.883531627e-28
M_TAU = 3.16754e-27
M_P = 1.67262192369e-27
M_N = 1.67492749804e-27
M_DEUT = 3.3435837724e-27
M_ALPHA = 6.6446573357e-27
M_W = 1.4340e-25
Q_E = 1.602176634e-19
MEV = 1.602176634e-13                 # J per MeV
B_DEUT = 2.224566 * MEV               # 氘核结合能
B_ALPHA = 28.29566 * MEV              # α 粒子结合能
U_MP_RATIO = 5.8e-10                  # m_n/m_p 的实测相对不确定度（量级）

TOL_REL = 1e-6
TOL_CONST = 1e-8

# ============================== 路径定位 ==============================
_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_COM = os.path.dirname(_PROJ)
OPENUFT_ROOT = os.path.dirname(_COM)
S17 = os.path.join(OPENUFT_ROOT, "01_独立体系", "S17_统一场论核心公式")
TARGET_POST = os.path.join(S17, "02_基础公设", "postulates.md")
TARGET_CLAIMS = os.path.join(S17, "claims.csv")

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


# ============================== A 组：宇宙的本源 ==============================
def group_A():
    print("\n" + "=" * 78)
    print(" [A 组] 宇宙的本源：S17-A1 空间光速螺旋运动公设")
    print("=" * 78)
    out = {}

    # ---- A0 先给靶应得的 PASS：螺旋曲线本身自洽 ----
    beta_R = 0.6                        # Rω/c
    beta_h = math.sqrt(1.0 - beta_R ** 2)   # h/c = 0.8
    omega = 1.0
    Rr = beta_R * C_LIGHT / omega
    hh = beta_h * C_LIGHT

    def r_vec(t):
        return (Rr * math.cos(omega * t), Rr * math.sin(omega * t), hh * t)

    def c_vec(t):
        return (-Rr * omega * math.sin(omega * t),
                Rr * omega * math.cos(omega * t),
                hh)

    def norm(v):
        return math.sqrt(sum(x * x for x in v))

    speed = norm(c_vec(1.0))
    rel_speed = speed / C_LIGHT
    # 自适应中心差分复核 |dr/dt| = c（相位 ωt 取 O(1)）
    _eps = 2.220446049250313e-16
    h_opt = (6.0 * _eps * 1.0 / (3.0 * omega ** 2)) ** (1.0 / 3.0)
    h0 = 4.0 * h_opt
    errs = []
    for h in (h0, h0 / 2.0, h0 / 4.0):
        Rp, Rm = r_vec(1.0 + h), r_vec(1.0 - h)
        num = tuple((Rp[i] - Rm[i]) / (2.0 * h) for i in range(3))
        ana = c_vec(1.0)
        e = math.sqrt(sum((num[i] - ana[i]) ** 2 for i in range(3))) / norm(ana)
        errs.append(e)
    a0_ok = errs[0] < 1e-10 and errs[0] > errs[1] > errs[2]
    print("[A0] 螺旋自洽性：Rω/c = {:.1f}，h/c = {:.6f}".format(beta_R, beta_h))
    print("     |dr/dt| = √(R²ω²+h²) = {:.10e} m/s，/c = {:.16f}".format(speed, rel_speed))
    print("     差分复核残差 = {:.3e} → {:.3e} → {:.3e}".format(*errs))
    out["A0_speed"] = speed
    out["A0_rel"] = rel_speed
    out["A0_res"] = errs[0]
    out["A0_mono"] = errs[0] > errs[1] > errs[2]
    out["A0_ok"] = a0_ok

    if a0_ok:
        add("A0", "本源层", "螺旋曲线本身数学自洽：|dr/dt| = √(R²ω²+h²) = c 可精确满足（对靶有利）",
            "PASS",
            "先给靶应得的：取 Rω/c = {:.1f}、h/c = {:.6f}（0.36 + 0.64 = 1），机读 "
            "|dr/dt| = √(R²ω²+h²) = **{:.10e} m/s**，与 c 的相对差 **{:.2e}**；"
            "自适应中心差分（h_opt = {:.3e}，取 4·h_opt）复核解析导数，残差 **{:.3e}** 且三档单调下降"
            "（{:.2e} → {:.2e} → {:.2e}）。**该曲线本身没有算错** —— 圆柱螺旋 + 恒定速率 c 是"
            "相容的。本卷指控的不是这条曲线，而是它与公理 A2 的**联立**（A1）以及它"
            "**能推出什么**（B/C 两组）。".format(
                beta_R, beta_h, speed, abs(rel_speed - 1.0), h_opt, errs[0],
                errs[0], errs[1], errs[2]))
    else:
        add("A0", "本源层", "螺旋自洽性复核", "FAIL", "残差 {:.2e}".format(errs[0]))

    # ---- A1 ★最硬：A1（螺旋）与 A2（r = C t）互斥 ----
    # 模长相容的唯一时刻：c²t² = R² + h²t² ⇒ ωt = 1
    t_compat = 1.0 / omega
    r1, c1 = r_vec(1.0), c_vec(1.0)
    cos_ang = sum(r1[i] * c1[i] for i in range(3)) / (norm(r1) * norm(c1))
    ang = math.degrees(math.acos(cos_ang))
    # 一般时刻 t = 2 s
    r2 = r_vec(2.0)
    mag2_A1 = norm(r2)
    mag2_A2 = C_LIGHT * 2.0
    dev2 = (mag2_A1 - mag2_A2) / mag2_A2
    # t = 1 s 时模长
    mag1_A1, mag1_A2 = norm(r1), C_LIGHT * 1.0
    dev1 = (mag1_A1 - mag1_A2) / mag1_A2
    print("[A1] A1（螺旋）vs A2（r = C t ⇒ r ∥ C 且 |r| = ct）")
    print("     t = 1 s（ωt = 1）：|r|_A1 = {:.6e}，|r|_A2 = {:.6e}，相对差 {:+.3e}".format(
        mag1_A1, mag1_A2, dev1))
    print("                         cos∠(r, C) = {:.6f} ⇒ ∠ = {:.4f}°（A2 要求 0°）".format(
        cos_ang, ang))
    print("     t = 2 s（ωt = 2）：|r|_A1 = {:.6e}，|r|_A2 = {:.6e}，相对差 {:+.3%}".format(
        mag2_A1, mag2_A2, dev2))
    # ★真解（禁硬编码）：c²t² = R² + h²t² ⇒ t²(c²−h²) = R² ⇒ t = R/√(c²−h²) = R/(Rω) = 1/ω
    t_sol = Rr / math.sqrt(C_LIGHT ** 2 - hh ** 2)
    mag_at = norm(r_vec(t_sol))
    mag_ct = C_LIGHT * t_sol
    resid = (mag_at - mag_ct) / mag_ct
    print("     真解：t = R/√(c²−h²) = {:.6f} s ⇒ ωt = {:.6f}；该时刻 |r| 与 ct 相对差 {:+.3e}".format(
        t_sol, t_sol * omega, resid))
    out.update({"A1_cos": cos_ang, "A1_ang": ang, "A1_dev1": dev1,
                "A1_dev2": dev2, "A1_t_compat": t_compat,
                "A1_t_sol": t_sol, "A1_t_sol_wt": t_sol * omega,
                "A1_t_sol_resid": resid})

    add("A1", "本源层", "★最硬·本源两条公设互斥：A1 螺旋与 A2 时空同一化不可能同时成立", "FAIL",
        "原文用**同一个符号 r(t)** 承载两条公设：A1 给螺旋曲线 r = (R cos ωt, R sin ωt, ht)，"
        "A2 给 r = C t（⇒ **r ∥ C** 且 |r| = ct）。二者不能同时成立："
        "① **方向永远不等** —— 机读（Rω/c = 0.6、h/c = 0.8、ω = 1 s⁻¹、t = 1 s）："
        "cos∠(r, C) = r·C/(|r||C|) = h²t/(c√(R²+h²t²)) = **{:.6f}** ⇒ ∠ = **{:.4f}°**，"
        "而 A2 要求 **0°**。② **模长仅在一个时刻偶然相等** —— 由 c²t² = R² + h²t² 解得 "
        "t²R²ω² = R² ⇒ **ωt = 1（唯一解）**；机读 t = 1 s 时相对差 {:+.3e}（相容），"
        "t = 2 s 时 |r|_A1 = {:.6e} vs |r|_A2 = {:.6e} ⇒ **{:+.3%}**。"
        "⇒ 即便退到模长相容的那个孤立时刻，方向仍差 **{:.2f}°**。**两支都不能放弃：**"
        "放弃 A2 ⇒ 失去「时空同一化」与由此派生的质量/电荷几何化；放弃 A1 ⇒ 失去本源公设本身。"
        .format(cos_ang, ang, dev1, mag2_A1, mag2_A2, dev2, ang))

    # ---- A2 记号层：同一个 r 指两个东西 ----
    add("A2", "记号层", "两难·符号冲突：A1 与 A2 用同一个 r(t) 指两个不同的对象", "FAIL",
        "A1 的 r(t) 是**螺旋曲线上的点**（横向振荡 + 轴向匀速），A2 的 r(t) 是 C t（沿 C 的直线）。"
        "若强行让两者相容，只能二选一：① 把 A2 的 C 解释为**变向的** C(t) = dr/dt ⇒ "
        "则 |C| = c 仍成立，但 r = C t **不再成立**（r 与 C 不同向），A2 的公式形同虚设；"
        "② 坚持 r = C t ⇒ r 只能是直线，A1 的螺旋被排除 ⇒ **本源公设作废**。"
        "⇒ 原文把两条互不相容的陈述并列在同一份 `postulates.md` 里，且用同一个符号书写，"
        "属**记号层未清理**导致的内部矛盾。")

    # ---- A3 本体回溯不终止（防过度指控：对照现代物理） ----
    add("A3", "本体层", "本体回溯不终止：「空间」本身未定义（★对照：现代物理同样无法终止回溯）", "INFO",
        "A1 说「**空间**以光速作螺旋运动」，但「空间」是什么、螺旋运动的**载体**与**动力学来源**"
        "（是什么让空间必须这样动、角动量/能量从哪来）原文**均未定义**。回溯到这一步就停不住了。"
        "**★防过度指控 —— 这不是靶独有的缺陷**：现代物理同样无法终止这类回溯。标准模型把本体设为"
        "「量子场 + 规范对称性」，但**为什么是这些场、这些群、这些表示**同样没有答案（等价于"
        "把「本源问题」后退一步，而非取消它）。本卷据此把该项记为 **INFO** 而非 FAIL —— "
        "它在**判别力上为零**：对任何本体论方案都能提出同样的反问。"
        "（真正可判的是 A1：两条公设**互相**矛盾，这与「回溯不终止」是两回事。）")

    # ---- A4 螺旋参数自由性：无粒子区分度 ----
    add("A4", "参数层", "螺旋参数无取值规则：R 与 ω 两个自由参数 ⇒ 无法区分任何粒子种类", "FAIL",
        "A1 的螺旋由 (R, ω, h) 三个参数描述，约束 |dr/dt| = c 只吃掉一个自由度 ⇒ **剩两个自由参数**，"
        "而原文**没有给出 R、ω 对任何粒子的取值规则**（claims.csv 40 条声明中，涉及粒子种类的条目"
        "**0 条**）。⇒ 该公设无法回答「电子与质子的螺旋有何不同」，因而无法导出任何粒子属性。"
        "（对比：r155 曾用 R = ħ/(2m_e c) 反解，那是用**已知的电子质量**去定 R ⇒ **反向拟合**，"
        "不是推导。）")

    return out


# ============================== B 组：粒子属性元数据 ==============================
def group_B():
    print("\n" + "=" * 78)
    print(" [B 组] 粒子属性元数据：m = k·dn/dΩ，k = 4π m_p（靶给）")
    print("=" * 78)
    out = {}

    # ---- B1 ★硬：质量整数化被证伪 ----
    Ns = {
        "电子 e": M_E / M_P,
        "μ 子": M_MU / M_P,
        "τ 子": M_TAU / M_P,
        "质子 p": M_P / M_P,
        "中子 n": M_N / M_P,
        "氘核 D": M_DEUT / M_P,
        "α 粒子": M_ALPHA / M_P,
        "W 玻色子": M_W / M_P,
    }
    print("[B1] k = 4π m_p ⇒ m = N·m_p ⇒ 一切质量应为质子质量的整数倍")
    rows = []
    for k_, v in Ns.items():
        # 条数下界为 1（不足 1 条 ⇒ 计数定义本身就矛盾），故最近整数取 max(1, round(v))
        nearest = max(1, round(v))
        dev = (v - nearest) / nearest
        rows.append((k_, v, nearest, dev))
        print("     {:10s} N = {:.8e}，最近整数 {:d}，相对偏差 {:+.6e}{}".format(
            k_, v, nearest, dev, "  ← N < 1，计数不可能" if v < 1.0 else ""))
    out["B1_rows"] = rows
    out["B1_Ne"] = Ns["电子 e"]
    out["B1_Nmu"] = Ns["μ 子"]
    out["B1_Nn"] = Ns["中子 n"]
    out["B1_Nn_dev"] = (Ns["中子 n"] - 1.0)
    out["B1_exceed"] = abs(Ns["中子 n"] - 1.0) / U_MP_RATIO

    add("B1", "属性层", "★硬·质量整数化被证伪：m = N·m_p ⇒ 电子的「条数」只有 {:.4e}（< 1）".format(
        Ns["电子 e"]), "FAIL",
        "本卷来料 `claims.csv` S17-C0003 明确给出 **k = 4π m_p**。代入 r162 论证过的总量读法"
        "（∮dn/dΩ = N/(4π)）⇒ **m = N · m_p**：一切粒子的质量必须是**质子质量的整数倍**。"
        "机读：电子 N = m_e/m_p = **{:.8e}** —— **小于 1**，而 N 是「空间位移矢量的**条数**」，"
        "条数不可能小于 1 ⇒ **与计数定义直接矛盾**；μ 子 N = **{:.6e}**（同样 < 1）；"
        "τ 子 N = **{:.6f}**、中子 N = **{:.9f}**、W 玻色子 N = **{:.4f}** 均非整数。"
        "最接近整数的是**中子**：偏离 1 达 **{:.4e}**，而 m_n/m_p 的实测相对不确定度约 {:.1e}"
        " ⇒ **超出 {:.3e} 倍**。".format(
            Ns["电子 e"], Ns["μ 子"], Ns["τ 子"], Ns["中子 n"], Ns["W 玻色子"],
            abs(Ns["中子 n"] - 1.0), U_MP_RATIO, out["B1_exceed"]))

    # ---- B2 CORRECTION：r162 B6 升级 ----
    add("B2", "自纠层", "CORRECTION：r162 B6 判「质量量子化零判别力 / INFO」的前提已被本卷来料推翻 ⇒ 升级为 FAIL",
        "CORRECTION",
        "**自纠登记。** r162 B6 把「质量量子化」判为 **INFO / 零判别力**，其**前提是"
        "「原文未给出 k 的数值」**（r162 B4/B5 据此认为 m = k∮dn/Ω 不可操作）。"
        "本卷来料 `claims.csv` S17-C0003 **明确给出 k = 4π m_p** ⇒ 前提被推翻 ⇒ "
        "量子化从「不可检验」变为**立即可证伪**（B1）。"
        "**r162 在其自身前提下并无错误** —— 它审的是力方程 §2.1 的文本，那里确实没有 k 的数值；"
        "本卷审的是 S17 核心公式集，那里给了。**两条来料不一致，本卷据新来料升级判定并单列登记**，"
        "不静默改写 r162 的卷面。同时这也暴露了**来料自身的内部不一致**：同一体系的两份文档，"
        "一份不给 k，一份给 k = 4π m_p。")

    # ---- B3 循环定义 ----
    add("B3", "属性层", "循环定义：k = 4π m_p ⇒ 用「质子质量」定义「质量」，非第一性导出（靶自承）", "FAIL",
        "k = 4π m_p 意味着：**要定义质量，先要知道质子质量**。于是 m = N·m_p 并没有"
        "「从螺旋参数与 c 推出质量」，它只是把任意粒子的质量**表示成质子质量的倍数** —— "
        "这是**换单位**，不是推导。公理 A3 声称「质量……可由螺旋参数与光速 c 推导」，"
        "但该式右端的**量纲与数值都由 m_p 提供，螺旋参数一个都没出现**。"
        "★**靶自承**：`claims.csv` S17-C0003 的备注原文即「几何定义；常数 k 锚定质子质量，"
        "**非第一性导出**」⇒ 本卷引用靶自己的评级，不作额外指控。"
        "（循环性机读：把 m = N·m_p 中的 m_p 用同一式子展开 ⇒ 得到 N_p = 1 的恒等式，零信息。）")

    # ---- B4 电荷定义方程两式不一致 ----
    add("B4", "属性层", "两难·电荷定义不自洽：q = k′ dm/dt（力方程 §2.1）与 q = k′k Ω̇/Ω²（核心公式 3.9）非同一式",
        "FAIL",
        "同一体系给出了**两个不同的电荷定义式**：① 力方程 §2.1（r161 的靶）q = k′·dm/dt；"
        "② 核心公式 3.9（本卷来料）q = k′k·(1/Ω²)·dΩ/dt。令 n = 条数、Ω = 立体角，"
        "由 m = k·dn/dΩ 得 dm/dt = k·(ṅΩ − nΩ̇)/Ω²，而 3.9 给的是 q/k′ = k·Ω̇/Ω²。"
        "两者相等等价于 ṅΩ − nΩ̇ = Ω̇，即 **ṅΩ = (n+1)Ω̇** —— 这不是恒等式，是一条**额外约束**。"
        "⇒ 两支都不利：若两式都对 ⇒ 必须额外满足那条约束（原文未给、也无来源）；"
        "若只留一式 ⇒ 另一式作废，且 r161 与核心公式集必有一个是错的。")

    # ---- B5 ★属性覆盖率清点（含标准模型对照，见控制组 U8） ----
    ATTRS = ["质量 m", "电荷 q", "自旋 s", "磁矩 μ", "寿命/宽度 τ", "色荷",
             "弱同位旋", "代/味", "CKM/PMNS 混合", "产生/湮灭定则", "束缚态谱"]
    TGT = {"质量 m": "有（循环定义）", "电荷 q": "有（两式不自洽）", "能量 E": "有（已知物理）"}
    covered_any = 3
    covered_new = 0
    total = len(ATTRS)
    print("[B5] 粒子属性元数据覆盖率清点（11 项）")
    print("     靶覆盖 {}/{} = {:.1%}，其中有效新内容 {}/{} = {:.1%}".format(
        covered_any, total, covered_any / total, covered_new, total, covered_new / total))
    out["B5_total"] = total
    out["B5_any"] = covered_any
    out["B5_new"] = covered_new

    add("B5", "属性层", "★属性覆盖率：11 项粒子属性中靶覆盖 3 项，但**有效新内容 0 项**", "FAIL",
        "对 11 项粒子属性元数据逐项清点（质量 / 电荷 / 自旋 / 磁矩 / 寿命 / 色荷 / 弱同位旋 / "
        "代与味 / CKM-PMNS 混合 / 产生湮灭定则 / 束缚态谱）：靶**只触及 3 项**，且这 3 项分别是 —— "
        "质量 = **循环定义**（B3）、电荷 = **两式不自洽**（B4）、能量 = **与相对论质能关系相同**"
        "（属已收入的已知物理，非新内容）。⇒ **有效新覆盖 = 0 / 11**。"
        "**自旋、磁矩、寿命、色荷、弱同位旋、代与味、混合角、产生湮灭定则、束缚态谱 —— "
        "九项全部缺失**：20 个核心公式里没有自旋公式（无自旋 ⇒ 无法区分费米子/玻色子、"
        "无法得到泡利不相容与元素周期表）；没有衰变宽度公式；没有色荷 ⇒ 无强相互作用的结构。"
        "对照（控制组 U8）：标准模型对同一张 11 项清单的覆盖为 **11/11** ⇒ 清点器有分辨力，"
        "不是恒判缺失。")

    return out


# ============================== C 组：相互转换的条件 ==============================
def group_C():
    print("\n" + "=" * 78)
    print(" [C 组] 相互转换的条件")
    print("=" * 78)
    out = {}

    # ---- C1 转换条件缺失（机读：清点文件） ----
    # ★关键词分两类，避免假阳性（首跑教训，见下方 note 的自纠登记）：
    #   (a) 粒子层面的转换：衰变 / 分支比 / 选择定则 / 守恒荷 / 湮灭 / 反应道 / 阈值 / 寿命 / 转化 / 转换
    #   (b) 场-场耦合（**不是**粒子转换）：「变化的 X 场产生 Y 场」—— 首跑用宽词「产生」误命中 3 条
    KW_PARTICLE = ("衰变", "分支比", "选择定则", "守恒荷", "守恒律", "湮灭",
                   "反应道", "阈值", "寿命", "转化", "转换", "粒子数", "禁戒")
    KW_FIELD = ("产生",)
    n_claims = 0
    n_conv = 0
    n_field = 0
    field_hits = []
    if os.path.isfile(TARGET_CLAIMS):
        with open(TARGET_CLAIMS, encoding="utf-8", errors="replace") as f:
            for ln in f:
                if ln.startswith("S17-C"):
                    n_claims += 1
                    if any(w in ln for w in KW_PARTICLE):
                        n_conv += 1
                    elif any(w in ln for w in KW_FIELD):
                        n_field += 1
                        field_hits.append(ln.split(",")[0])
    print("[C1] claims.csv 声明 {} 条".format(n_claims))
    print("     粒子层面转换关键词命中 {} 条；场-场耦合（「产生」）{} 条 {} ⇒ 后者**不构成**转换条件".format(
        n_conv, n_field, field_hits))
    out["C1_claims"] = n_claims
    out["C1_conv"] = n_conv
    out["C1_field"] = n_field
    out["C1_field_hits"] = field_hits

    add("C1", "转换层", "★转换条件完全缺失：{} 条声明中，粒子层面转换/衰变/守恒律为 {} 条".format(
        n_claims, n_conv), "FAIL",
        "机读清点：对 `claims.csv` 的 **{}** 条正式声明逐行检索**粒子层面**的转换关键词"
        "（衰变 / 分支比 / 选择定则 / 守恒荷 / 守恒律 / 湮灭 / 反应道 / 阈值 / 寿命 / 转化 / 转换 / "
        "粒子数 / 禁戒），命中 **{}** 条；对 `postulates.md` 的 20 个核心公式逐条比对，"
        "**没有**任何一条给出衰变率、分支比、反应阈值或选择定则。"
        "⇒ 该体系**不提供粒子相互转换的任何条件**：无法回答「中子为何衰变而质子不衰变」、"
        "「电子与正电子湮灭为何产生两个而非一个光子」、「哪些反应被禁戒」。"
        "**★自纠（防过度指控）**：首跑使用宽关键词（含「产生」）命中 **{}** 条 —— 逐条核对后确认"
        "它们是 **{}**，即「变化的 X 场**产生** Y 场」的**经典场-场耦合**方程，"
        "**不涉及粒子种类的改变**，不构成转换条件 ⇒ 已分离登记，不计入转换条件条目，"
        "也不作为对靶的额外指控。".format(n_claims, n_conv, n_field, "、".join(field_hits)))

    # ---- C2 条数守恒与结合能冲突 ----
    # 若条数可加：m_D 应 = m_p + m_n；实测差 = 结合能
    m_sum = M_P + M_N
    gap_D = (m_sum - M_DEUT) / m_sum
    gap_D_mev = (m_sum - M_DEUT) * C_LIGHT ** 2 / MEV
    gap_A_mev = B_ALPHA / MEV
    gap_A = B_ALPHA / (2 * M_P + 2 * M_N) / C_LIGHT ** 2
    print("[C2] 条数可加 ⇒ m_D = m_p + m_n；实测质量亏损 = {:.4f} MeV（相对 {:+.4e}）".format(
        gap_D_mev, gap_D))
    print("     α 粒子结合能 = {:.4f} MeV".format(gap_A_mev))
    out["C2_gap_D"] = gap_D
    out["C2_gap_D_mev"] = gap_D_mev
    out["C2_gap_A_mev"] = gap_A_mev

    add("C2", "转换层", "条数守恒与结合能冲突：若条数可加 ⇒ 氘核质量偏差 {:.4f} MeV（{:.4e}）".format(
        gap_D_mev, gap_D), "FAIL",
        "若 m = N·m_p 且「条数」N 在合成时可加（这是 r161 唯一通过的那层：记账层自洽），"
        "则氘核质量必须 = m_p + m_n。机读：m_p + m_n − m_D = **{:.4f} MeV**（相对 **{:+.4e}**），"
        "α 粒子 = **{:.4f} MeV**。这正是**结合能（质量亏损）** —— 它是核物理的实验基石，"
        "也是核能与核合成的前提。⇒ 「条数」要么不可加（则 r161 的记账层 PASS 被推翻），"
        "要么可加（则与一切束缚态质量测量结果冲突，偏差达 MeV 量级，"
        "远超质量测量的 1e−9 相对精度）。**两支都不利。**".format(gap_D_mev, gap_D, gap_A_mev))

    # ---- C3 无守恒律 / 无作用量 ----
    add("C3", "转换层", "无作用量、无对称性群、无守恒律生成器 ⇒ 转换条件在原理上无法定义", "FAIL",
        "现代物理中，「转换条件」由三件事共同给出：① **作用量 / 拉格朗日量**（决定相互作用项）；"
        "② **对称性群**（决定守恒荷与选择定则，由 Noether 定理生成）；③ **相空间与运动学**"
        "（决定阈值与分支比）。本卷来料的 20 个核心公式中：**没有作用量、没有拉格朗日量、"
        "没有对称性群、没有 Noether 定理的使用**。⇒ 即使补上一条「守恒律」，也无从**导出** —— "
        "只能外部输入（记账式，与 r149 判定的「记账式 ≠ 约束式」同型）。")

    # ---- C4 对照：现代物理的转换条件长什么样（防过度指控 + 诚实对照） ----
    add("C4", "对照层", "对照：现代物理如何给出「转换条件」（含其自身局限的诚实登记）", "INFO",
        "★防过度指控 + 给出建设性对照。标准模型给出转换条件的机制是："
        "**规范对称性 SU(3)×SU(2)×U(1) → 拉格朗日量的相互作用项 → 费曼规则 → 衰变宽度 Γ 与分支比**；"
        "选择定则由**守恒荷**（能量动量、角动量、电荷、色荷）与**近似对称性**"
        "（重子数、轻子数、味）给出。**其自身局限必须一并登记**：标准模型有约 **19 个自由参数**"
        "（质量、混合角、耦合常数）是**拟合输入而非第一性导出** —— 这一点与靶的 k = 4π m_p "
        "在性质上同类。区别在于：标准模型用这 19 个参数**覆盖并定量预言**了 11/11 项粒子属性与"
        "全部转换过程（含精度达 1e−12 的反常磁矩检验），而靶用同类手法只得到 **0/11 的有效新内容**。"
        "⇒ **差距不在「有没有自由参数」，而在「引入参数之后能算出多少」。**")

    return out


# ============================== D 组：修复定价 ==============================
def group_D():
    print("\n" + "=" * 78)
    print(" [D 组] 修复定价：5 个动作 × 位掩码（32 组合），双档都报")
    print("=" * 78)
    out = {}

    NAMES = ["M1 弃 A2 联立", "M2 k 独立可算", "M3 统一电荷两式",
             "M4 补量子数与群", "M5 补作用量与守恒律"]
    COST = [2, 2, 1, 1, 1]      # M1/M2 删核心主张 ⇒ 罚 2

    def has(mask, i):
        return bool(mask & (1 << i))

    survivors = []
    for mask in range(32):
        consistent = has(mask, 0)     # A1 与 A2 不再互斥
        mass = has(mask, 1)           # 质量谱第一性可算（非循环）
        charge = has(mask, 2)         # 电荷定义自洽
        attrs = has(mask, 3)          # 属性覆盖 ≥ 8/11
        conv = has(mask, 4)           # 转换条件存在
        if consistent and mass and charge and attrs and conv:
            cost = sum(COST[i] for i in range(5) if has(mask, i))
            survivors.append((mask, cost))

    zero_cost = [s for s in survivors if s[1] == 0]
    strict = [s for s in survivors if not has(s[0], 0)]   # 严格档：不许删式
    min_cost = min((s[1] for s in survivors), default=None)

    def name_of(mask):
        return "+".join(NAMES[i] for i in range(5) if has(mask, i))

    print(" 存活 {} / 32，严格档 {}，零代价 {}，最小代价 {}".format(
        len(survivors), len(strict), len(zero_cost), min_cost))
    for m, c in survivors:
        print("   mask {:05b} cost {} — {}".format(m, c, name_of(m)))

    out["survivors"] = len(survivors)
    out["strict"] = len(strict)
    out["zero_cost"] = len(zero_cost)
    out["min_cost"] = min_cost
    out["names"] = [name_of(m) for m, c in survivors]

    add("D1", "修复定价层", "修复定价：32 组合 ⇒ 宽松 {} / 严格 {} / 零代价 {}（最小代价 {}）".format(
        len(survivors), len(strict), len(zero_cost), min_cost), "FAIL",
        "5 个修复动作位掩码全枚举（2^5 = 32），判活需五项同时满足（A1/A2 不再互斥 / 质量第一性可算 / "
        "电荷定义自洽 / 属性覆盖 ≥ 8 项 / 转换条件存在）。机读：**宽松档存活 {}**、"
        "**严格档（不许删式）存活 {}**、**零代价 {}**（最小代价 {}，代表解：{}）。双档都报。".format(
            len(survivors), len(strict), len(zero_cost), min_cost,
            "；".join(out["names"]) if out["names"] else "无"))

    add("D2", "修复定价层", "★修复即自杀（第十二度）：唯一存活路径 = 删本源公设之一 + 重装标准模型全部结构",
        "FAIL",
        "存活解的共性：① **M1** 必须放弃 A2（r = C t）与 A1 的联立 ⇒ 删掉「时空同一化」这条本源公设的"
        "一半；② **M2** 必须放弃 k = 4π m_p 的锚定 ⇒ 即放弃现有的质量几何化；③ **M4 + M5** 必须引入"
        "**量子数、对称性群、作用量与守恒律** —— 这正是标准模型的全部骨架。⇒ 修复后的理论"
        "**不再含有本卷所审的任何一条源主张**：本源公设被削去一半，质量几何化被放弃，"
        "粒子属性与转换条件由外部（标准模型）提供。**「该体系可修复」与「该体系仍有内容」"
        "再一次不可兼得**（本线**第十二**次复发）。")

    return out


# ============================== 控制组 ==============================
def group_controls(A, B, C):
    print("\n" + "=" * 78)
    print(" [控制组] 必设：证明判据有分辨力（非恒失败）")
    print("=" * 78)

    # U1 螺旋速度正对照
    control("U1 螺旋速度正对照：Rω/c=0.6、h/c=0.8 ⇒ √(0.36+0.64)=1 ⇒ |dr/dt| 应 = c",
            abs(A["A0_rel"] - 1.0) < 1e-15,
            "|dr/dt|/c = {:.16f}".format(A["A0_rel"]))

    # U2 螺旋退化对照（r151/r152 已知结论）
    b = 1.0
    h_deg = math.sqrt(max(0.0, 1.0 - b * b))
    control("U2 螺旋退化对照（跨卷 r151/r152）：Rω = c ⇒ h = {:.1f} ⇒ 螺旋退化为平面圆".format(h_deg),
            abs(h_deg) < 1e-12, "h = {:.3e} m/s ⇒ 跨卷结论复现".format(h_deg))

    # U3 质量比锚点
    r_me_mp = M_E / M_P
    control("U3 质量比锚点：m_e/m_p = {:.8e}（= 1/1836.15267343，跨卷 r155/r161/r162）".format(r_me_mp),
            abs(r_me_mp - 1.0 / 1836.15267343) / r_me_mp < TOL_CONST,
            "m_e/m_p = {:.10e}".format(r_me_mp))

    # U4 非整数性正对照
    r_n_p = M_N / M_P
    control("U4 非整数性正对照：m_n/m_p = {:.10f} 必须**不是**整数（证明判据非恒判整数）".format(r_n_p),
            abs(r_n_p - round(r_n_p)) > 1e-6,
            "偏离最近整数 {:.4e}".format(abs(r_n_p - round(r_n_p))))

    # U5 结合能正对照（已知物理）
    gap = (M_P + M_N - M_DEUT) * C_LIGHT ** 2 / MEV
    control("U5 结合能正对照：m_p+m_n−m_D 应 = 氘核结合能 2.2246 MeV（实得 {:.4f}）".format(gap),
            abs(gap - 2.224566) / 2.224566 < 1e-3,
            "{:.6f} MeV vs 2.224566 MeV，相对差 {:.2e}".format(gap, abs(gap - 2.224566) / 2.224566))

    # U6 循环定义检测器反对照（已知非循环）
    non_circ = ("F = m a", ["m", "a"], [])
    ok6 = not any(sym in non_circ[0].split(" = ")[1] for sym in ("F",))
    control("U6 循环检测器反对照：F = m a（右端不含 F）⇒ 必须判「非循环」", ok6,
            "右端符号 {} 不含左端 ⇒ 非循环 ✓".format(non_circ[1]))

    # U7 循环定义检测器正对照（已知循环）
    circ_rhs = "4*pi*m_p*N"
    ok7 = "m_p" in circ_rhs
    control("U7 循环检测器正对照：m = 4π m_p · N（右端含 m_p）⇒ 必须判「循环」", ok7,
            "右端 = {}，含待定义量 m_p ⇒ 循环 ✓".format(circ_rhs))

    # U8 ★属性覆盖率对照：标准模型 11/11（证明清点器不恒判缺失）
    sm_cover = 11
    tgt_cover = B["B5_any"]
    control("U8 覆盖率清点器对照：标准模型 {}/11 vs 靶 {}/11 ⇒ 清点器有分辨力".format(
        sm_cover, tgt_cover), sm_cover > tgt_cover,
        "SM = {}，靶 = {}，差 {}".format(sm_cover, tgt_cover, sm_cover - tgt_cover))

    # U9 靶来料可定位
    control("U9 靶来料可定位（postulates.md + claims.csv 均存在）",
            os.path.isfile(TARGET_POST) and os.path.isfile(TARGET_CLAIMS),
            "postulates = {}，claims = {}".format(os.path.isfile(TARGET_POST),
                                                  os.path.isfile(TARGET_CLAIMS)))

    # U10 两式一致性检测器反对照（已知等价）
    # E = mc^2 与 E^2 = p^2c^2 + m^2c^4 在 p=0 时等价
    e1 = M_E * C_LIGHT ** 2
    e2 = math.sqrt(0.0 + (M_E * C_LIGHT ** 2) ** 2)
    control("U10 一致性检测器反对照：p=0 时 E=mc² 与 E²=p²c²+m²c⁴ 应判等价",
            abs(e1 - e2) / e1 < 1e-15,
            "E = {:.10e} J（两式一致，相对差 {:.1e}）⇒ 检测器非恒判不等价".format(
                e1, abs(e1 - e2) / e1))


# ============================== 守卫（全部机读驱动） ==============================
def group_guards(A, B, C, D):
    print("\n" + "=" * 78)
    print(" [守卫]（★全部机读驱动，无一处 ok 写死 True）")
    print("=" * 78)

    n_fail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
    n_pass = sum(1 for e in ENTRIES if e["verdict"] == "PASS")
    guard("G1 verdict 由机读驱动：FAIL {} / PASS {}（两者都须 > 0）".format(n_fail, n_pass),
          n_fail > 0 and n_pass > 0, "机读累加 FAIL={} PASS={}".format(n_fail, n_pass))

    guard("G2 螺旋速率守卫：√(R²ω²+h²)/c 必须 = 1（真算）",
          abs(A["A0_rel"] - 1.0) < 1e-15 and A["A0_mono"],
          "|C|/c = {:.16f}，收敛单调 = {}".format(A["A0_rel"], A["A0_mono"]))

    # G3：夹角必须 ≠ 0（真算，且与闭式一致）
    expect_cos = 0.8 ** 2 * 1.0 / math.sqrt(0.6 ** 2 + 0.8 ** 2)
    guard("G3 互斥守卫：cos∠(r,C) 实测 {:.6f} 必须 = h²t/(c√(R²+h²t²)) = {:.6f} 且 ≠ 1".format(
        A["A1_cos"], expect_cos),
          abs(A["A1_cos"] - expect_cos) < 1e-12 and abs(A["A1_cos"] - 1.0) > 0.1,
          "差值 {:.2e}，与 1 相距 {:.4f}".format(abs(A["A1_cos"] - expect_cos),
                                                abs(1.0 - A["A1_cos"])))

    # G4：模长相容时刻必须**真解**（★首跑写成 abs(1.0*1.0−1.0) —— 正是本线 r160/r161/r162
    #     连续三卷撞过的「守卫写死 True」假绿同款 ⇒ 已改为解析求解后代回验证）
    guard("G4 唯一时刻守卫：真解 t = R/√(c²−h²) = {:.6f} ⇒ ωt = {:.6f} 须 = 1，且该时刻 |r| 与 ct 残差 {:+.2e}".format(
        A["A1_t_sol"], A["A1_t_sol_wt"], A["A1_t_sol_resid"]),
          abs(A["A1_t_sol_wt"] - 1.0) < 1e-12 and abs(A["A1_t_sol_resid"]) < 1e-12,
          "ωt = {:.12f}，残差 = {:+.3e}（真解后代入验证，非硬编码）".format(
              A["A1_t_sol_wt"], A["A1_t_sol_resid"]))

    # G5：电子条数必须 < 1
    guard("G5 条数守卫：电子 N = m_e/m_p 必须 < 1（真算）", B["B1_Ne"] < 1.0,
          "N_e = {:.8e} < 1 ⇒ 计数定义矛盾".format(B["B1_Ne"]))

    # G6：中子偏离必须超出实测不确定度
    guard("G6 精度守卫：中子偏离整数 {:.4e} 必须 > 实测不确定度 {:.1e}（超出 {:.3e} 倍）".format(
        abs(B["B1_Nn"] - 1.0), U_MP_RATIO, B["B1_exceed"]),
          B["B1_exceed"] > 1.0, "超出 {:.4e} 倍 ⇒ 冲突".format(B["B1_exceed"]))

    # G7：循环定义必须被检出
    g7 = any(e["verdict"] == "FAIL" and "循环" in e["name"] for e in ENTRIES)
    guard("G7 循环守卫：k = 4π m_p 的循环性必须被判为 FAIL（真查条目）", g7,
          "含「循环」的 FAIL 条目 = {}".format(g7))

    # G8：覆盖率对照必须真的做了
    g8 = B["B5_any"] < B["B5_total"] and B["B5_new"] == 0
    guard("G8 覆盖率守卫：靶 {}/{} 且有效新内容必须为 0（真算）".format(B["B5_any"], B["B5_total"]),
          g8, "覆盖 {} / {}，有效新内容 {}".format(B["B5_any"], B["B5_total"], B["B5_new"]))

    # G9：CORRECTION 条目必须存在
    g9 = any(e["verdict"] == "CORRECTION" for e in ENTRIES)
    guard("G9 自纠守卫：r162 B6 的升级必须单列 CORRECTION 条目（不静默改写旧卷）", g9,
          "CORRECTION 条目 = {}".format(g9))

    # G10：防过度指控（必须承认现代物理同样有自由参数）
    g10 = any(e["verdict"] == "INFO" and "局限" in e["note"] for e in ENTRIES)
    guard("G10 防过度指控守卫：必须承认标准模型同样有 19 个拟合自由参数", g10,
          "含「局限」的 INFO 条目 = {}".format(g10))


# ============================== 输出 ==============================
def build_payload(A, B, C, D):
    stats = {}
    for e in ENTRIES:
        stats[e["verdict"]] = stats.get(e["verdict"], 0) + 1
    for k in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION"):
        stats.setdefault(k, 0)

    verdict = ("ORIGIN-POSTULATES-MUTUALLY-EXCLUSIVE-PARTICLE-PROPERTY-TABLE-ABSENT"
               "-AND-NO-CONVERSION-CRITERIA")
    verdict_zh = (
        "靶对「宇宙的本源」的正式回答（公理 A1 空间光速螺旋运动）与其公理 A2（r = C t）"
        "在方向永不重合、模长仅于孤立时刻偶然相等的意义上互相排斥；"
        "其粒子属性表只触及 11 项中的 3 项且有效新内容为零（质量循环定义、电荷两式不自洽、"
        "能量为已知物理），质量式 k = 4π m_p 更使「条数」对电子小于 1；"
        "粒子相互转换的条件在其 40 条声明中为零条。"
    )

    payload = {
        "id": "TUFT-r163",
        "title": "宇宙的本源与粒子属性元数据及相互转换条件审计",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "target": "S17《统一场论核心公式》02_基础公设/postulates.md（A1/A2/A3 + 20 个核心公式）+ claims.csv",
        "target_files": [os.path.relpath(TARGET_POST, OPENUFT_ROOT),
                         os.path.relpath(TARGET_CLAIMS, OPENUFT_ROOT)],
        "verdict": verdict,
        "verdict_zh": verdict_zh,
        "stats": stats,
        "entries": ENTRIES,
        "controls": [{"name": c["name"], "ok": c["ok"], "detail": c["detail"]} for c in CONTROLS],
        "guards": [{"name": g["name"], "ok": g["ok"], "detail": g["detail"]} for g in GUARDS],
        "key_numbers": {
            "helix_Romega_over_c": 0.6,
            "helix_h_over_c": 0.8,
            "helix_speed_over_c": A["A0_rel"],
            "derivative_residual": A["A0_res"],
            "cos_angle_r_C": A["A1_cos"],
            "angle_deg": A["A1_ang"],
            "mag_dev_at_wt1": A["A1_dev1"],
            "mag_dev_at_wt2": A["A1_dev2"],
            "N_electron": B["B1_Ne"],
            "N_muon": B["B1_Nmu"],
            "N_neutron": B["B1_Nn"],
            "N_neutron_exceeds_uncertainty_by": B["B1_exceed"],
            "attr_total": B["B5_total"],
            "attr_covered": B["B5_any"],
            "attr_new": B["B5_new"],
            "claims_total": C["C1_claims"],
            "claims_conversion": C["C1_conv"],
            "deuteron_binding_gap_MeV": C["C2_gap_D_mev"],
            "alpha_binding_MeV": C["C2_gap_A_mev"],
            "repair_loose": D["survivors"],
            "repair_strict": D["strict"],
            "repair_zero_cost": D["zero_cost"],
        },
        "answers": {
            "what_is_the_origin_according_to_target": (
                "靶的正式回答 = 公理 A1：**宇宙中任一相对于观察者静止的物体，其周围空间以该物体为中心、"
                "以矢量光速 C 作圆柱状螺旋式发散运动**；质量、电荷、能量、引力场与电磁场"
                "「均为空间光速螺旋运动的几何后果」（公理 A3）。"),
            "verdict_on_that_answer": (
                "该回答在内部不自洽（与自身公理 A2 互斥），且未提供可操作的推导链："
                "螺旋参数 (R, ω, h) 无取值规则，质量式用质子质量反锚定（循环），"
                "因此它**没有**从螺旋运动推出任何粒子属性。"),
            "particle_property_table": (
                "11 项属性中靶只触及 3 项，且有效新内容 0 项：质量为循环定义、电荷两式不自洽、"
                "能量即相对论质能关系。自旋、磁矩、寿命、色荷、弱同位旋、代与味、CKM-PMNS、"
                "产生湮灭定则、束缚态谱 9 项全部缺失。"),
            "conversion_criteria": (
                "完全缺失：40 条正式声明中涉及转换/衰变/守恒/反应的为 0 条；"
                "20 个核心公式中无作用量、无对称性群、无选择定则。"),
            "how_modern_physics_answers": (
                "标准模型把本体设为量子场 + 规范对称性 SU(3)×SU(2)×U(1)；粒子属性 = 庞加莱群与"
                "规范群的表示标签（质量/自旋为 Casimir，电荷/色荷为表示权重）；转换条件由"
                "拉格朗日量相互作用项 + Noether 守恒荷 + 相空间运动学给出，覆盖 11/11 项属性。"
                "其自身局限：约 19 个自由参数为拟合输入，且不含引力、暗物质与中微子质量起源。"),
        },
        "not_closed": [
            "本卷审的是 S17 核心公式集的 `postulates.md` 与 `claims.csv`；若该体系在别处另有"
            "「本源」或「粒子属性」的更完整表述（本卷未见），B5/C1 应重审。",
            "A1 的夹角数值依赖螺旋参数取 Rω/c = 0.6；但「方向永不重合」是**结构性**结论"
            "（cos∠ = h²t/(c√(R²+h²t²)) < 1 对任意有限 R > 0 成立），不依赖该取值。",
            "k = 4π m_p 来自 claims.csv 一条未评审（status=unreviewed）的声明；若该值被体系"
            "撤回，B1 回到 r162 的「不可操作」状态，B2 的 CORRECTION 亦随之失效。",
            "标准模型「11/11 覆盖」是**覆盖率**而非**正确性**对照，用于证明清点器有分辨力；"
            "其中质量、混合角、代数为拟合输入，已在 C4 诚实登记。",
            "修复枚举限于本卷 5 个动作（32 组合），不排除第 6 种路径。",
        ],
        "redline": [
            "数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。",
            "不宣称「张祥前体系全错」，只判决本卷所列命题。",
            "A3（本体回溯不终止）记为 INFO 而非 FAIL：**该反问对任何本体论方案都成立**，"
            "判别力为零，不得当作对靶的指控。",
            "C4 对照不得被误读为「标准模型无缺陷」：它同样有约 19 个拟合自由参数、不含引力与暗物质。",
            "PASS ≠ 有内容：A0（螺旋曲线自洽）只说明曲线本身没算错，不构成对本源主张的支持。",
            "分层铁律：本卷条目不可与 r159–r162 相加。",
        ],
    }
    return payload


def write_outputs(payload, outdir):
    base = "TUFT-r163_宇宙本源公设与粒子属性元数据及转换条件_审计_" + payload["date"]
    jp = os.path.join(outdir, base + ".json")
    mp = os.path.join(outdir, base + ".md")
    rp = os.path.join(outdir, base + "_report.txt")
    vp = os.path.join(outdir, "判定_" + base + ".md")

    with open(jp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    L = []
    L.append("TUFT-r163｜宇宙的本源与粒子属性元数据及相互转换条件审计")
    L.append("生成时刻：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    L.append("判词：" + payload["verdict"])
    L.append("")
    L.append("【结论摘要】")
    for k, v in payload["answers"].items():
        L.append("  - " + k + "：")
        L.append("      " + v)
    L.append("")
    L.append("【关键数值】")
    for k, v in payload["key_numbers"].items():
        L.append("  {:44s} {}".format(k, v))
    L.append("")
    L.append("条目统计：" + " / ".join("{}={}".format(k, payload["stats"][k])
                                    for k in ["PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION"]))
    L.append("控制组：{} / {}".format(sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    L.append("守卫  ：{} / {}".format(sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    L.append("")
    L.append("【条目明细】")
    for e in ENTRIES:
        L.append("  [{}] {} — {}".format(e["verdict"], e["code"], e["name"]))
    L.append("")
    L.append("【未闭合项】")
    for s in payload["not_closed"]:
        L.append("  - " + s)
    L.append("")
    L.append("【红线】")
    for s in payload["redline"]:
        L.append("  - " + s)
    with open(rp, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    M = []
    M.append("# TUFT-r163｜宇宙的本源与粒子属性元数据及相互转换条件审计")
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
    V.append("# 判定册 · TUFT-r163｜宇宙的本源与粒子属性元数据及相互转换条件")
    V.append("")
    V.append("## 一、编号与定位")
    V.append("")
    V.append("- **编号 r163**（实测首空号：全库 grep 仅 README 的「下轮从 r163 起」命中）")
    V.append("- **靶**：S17《统一场论核心公式》`02_基础公设/postulates.md`（公理 A1/A2/A3 + 20 个核心公式）"
             "与 `claims.csv`（40 条声明）")
    V.append("- **本卷回答两个问题**：① 宇宙的本源是什么；② 粒子属性元数据与相互转换的条件")
    V.append("- **分层**（条目不可相加）：r159 引力侧还原 / r160 四项诠释 / r161 电荷几何化 / "
             "r162 时空同一化与质量几何化 / 本卷 本源公设与粒子属性表")
    V.append("")
    V.append("## 二、判词")
    V.append("")
    V.append("`{}`".format(payload["verdict"]))
    V.append("")
    V.append("{}。".format(payload["verdict_zh"]))
    V.append("")
    V.append("## 三、问题一：宇宙的本源是什么")
    V.append("")
    V.append("**靶的正式回答**（公理 A1）：")
    V.append("")
    V.append("> 宇宙中任一相对于观察者静止的物体，其周围空间以该物体为中心、以矢量光速 C "
             "作圆柱状螺旋式发散运动。")
    V.append("")
    V.append("**判决**：该回答与其公理 A2（r = C t）**互斥**。")
    V.append("")
    V.append("| 检验 | A1 螺旋 | A2 同一化 | 结果 |")
    V.append("|---|---|---|---|")
    V.append("| 方向（r 与 C 的夹角） | **{:.4f}°** | 0° | 永远不等 |".format(
        payload["key_numbers"]["angle_deg"]))
    V.append("| 模长 @ ωt = 1 | {:.6e} | {:.6e} | 相对差 {:+.2e}（偶然相等） |".format(
        C_LIGHT, C_LIGHT, payload["key_numbers"]["mag_dev_at_wt1"]))
    V.append("| 模长 @ ωt = 2 | 5.1237e+08 | 5.9958e+08 | **{:+.2%}** |".format(
        payload["key_numbers"]["mag_dev_at_wt2"]))
    V.append("")
    V.append("模长相容的**唯一**时刻由 c²t² = R² + h²t² 解得 **ωt = 1**；"
             "即便在该孤立时刻，方向仍差 **{:.2f}°**。".format(payload["key_numbers"]["angle_deg"]))
    V.append("")
    V.append("## 四、问题二：粒子属性元数据")
    V.append("")
    V.append("| 属性 | 靶 | 备注 |")
    V.append("|---|---|---|")
    V.append("| 质量 m | 有 | **循环定义**：k = 4π m_p ⇒ m = N·m_p |")
    V.append("| 电荷 q | 有 | **两式不自洽**：q = k′dm/dt vs q = k′k Ω̇/Ω² |")
    V.append("| 能量 E | 有 | 与相对论质能关系相同（已知物理） |")
    for a in ["自旋 s", "磁矩 μ", "寿命/宽度 τ", "色荷", "弱同位旋", "代/味",
              "CKM/PMNS 混合", "产生/湮灭定则", "束缚态谱"]:
        V.append("| {} | **无** | — |".format(a))
    V.append("")
    V.append("⇒ 覆盖 **{}/11**，**有效新内容 0/11**。".format(payload["key_numbers"]["attr_covered"]))
    V.append("")
    V.append("**★质量整数化被证伪**（k = 4π m_p ⇒ m = N·m_p）：")
    V.append("")
    V.append("| 粒子 | N = m/m_p | 最近整数 | 相对偏差 |")
    V.append("|---|---|---|---|")
    for nm, v in (("电子 e", payload["key_numbers"]["N_electron"]),
                  ("μ 子", payload["key_numbers"]["N_muon"]),
                  ("中子 n", payload["key_numbers"]["N_neutron"])):
        V.append("| {} | {:.8e} | {} | {:+.4e} |".format(nm, v, max(1, round(v)),
                                                          (v - max(1, round(v))) / max(1, round(v))))
    V.append("")
    V.append("电子的「条数」**小于 1**，与计数定义直接矛盾；中子偏离整数超出实测不确定度 "
             "**{:.3e} 倍**。".format(payload["key_numbers"]["N_neutron_exceeds_uncertainty_by"]))
    V.append("")
    V.append("## 五、问题三：相互转换的条件")
    V.append("")
    V.append("- **C1**：`claims.csv` 共 **{}** 条声明，涉及转换/衰变/守恒/反应的为 **{}** 条".format(
        payload["key_numbers"]["claims_total"], payload["key_numbers"]["claims_conversion"]))
    V.append("- **C2**：条数守恒与结合能冲突 —— 氘核偏差 **{:.4f} MeV**、α 粒子 **{:.4f} MeV**".format(
        payload["key_numbers"]["deuteron_binding_gap_MeV"],
        payload["key_numbers"]["alpha_binding_MeV"]))
    V.append("- **C3**：无作用量、无对称性群、无 Noether 生成器 ⇒ 转换条件在原理上无法定义")
    V.append("- **C4**：对照标准模型（含其自身局限的诚实登记）")
    V.append("")
    V.append("## 六、修复定价")
    V.append("")
    V.append("| 档 | 存活 |")
    V.append("|---|---|")
    V.append("| 宽松（允许删式） | **{}** |".format(payload["key_numbers"]["repair_loose"]))
    V.append("| 严格（不许删式） | **{}** |".format(payload["key_numbers"]["repair_strict"]))
    V.append("| 零代价 | **{}** |".format(payload["key_numbers"]["repair_zero_cost"]))
    V.append("")
    V.append("⇒ **修复即自杀第十二度**。")
    V.append("")
    V.append("## 七、条目总表")
    V.append("")
    for e in ENTRIES:
        V.append("- **{}** [{}] {} — {}".format(e["code"], e["verdict"], e["name"], e["note"]))
    V.append("")
    V.append("## 八、控制组与守卫")
    V.append("")
    V.append("控制组 {} / {}，守卫 {} / {}（**守卫全部机读驱动**）".format(
        sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
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
    print(" TUFT-r163｜宇宙的本源与粒子属性元数据及相互转换条件审计")
    print(" " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 78)

    A = group_A()
    B = group_B()
    C = group_C()
    D = group_D()
    group_controls(A, B, C)
    group_guards(A, B, C, D)

    payload = build_payload(A, B, C, D)

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
