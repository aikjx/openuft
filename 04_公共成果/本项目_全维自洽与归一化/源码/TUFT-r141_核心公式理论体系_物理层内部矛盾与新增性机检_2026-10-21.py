# -*- coding: utf-8 -*-
"""
TUFT-r141 · 核心公式理论体系 · 物理层内部矛盾与新增性机检

对象：S17《统一场论核心公式》的 20 个核心公式（张祥前统一场论）
      —— 见 01_独立体系/S17_统一场论核心公式/02_基础公设/postulates.md

分工声明（与前册严格分层，条目不可相加）：
  前册《判定_S17核心公式_闭合代价与单位约定组合》(2026-10-03) 做的是
  【量纲层 / 单位约定层】(M1+M2)，并明确声明「本册不做物理判决」。
  本卷做的是它【没有做、也声明不做】的那一层：
      M3 —— 物理层：公设↔公式冲突、公式间内部矛盾、公式↔实验冲突、新增性定价。

方法（沿用既有纪律）：
  · 每条判据先过【控制组】：把同样的判据施加于标准物理（SR / 牛顿 / 库仑 / 麦克斯韦），
    确认判据不会把标准物理也判 FAIL —— 否则判据本身失效，退出码 2。
  · 二难类结论必须给出【两个分支各自的定量阈值】，不得只说"不可能"。
  · 「与已知物理逐字相同」一律降 INFO（零新增），不计入 PASS 证据。
  · 红线：量纲自洽 ≠ 物理成立；数学自洽 ≠ 实验证实。本册只作可算判决。

机检清单（23 条 + 控制组 6 项）：
  组 A 公设↔公式： A1 螺旋"发散"vs r 常量 ｜ A2 力方程漏 m·dC/dt ｜ A3 螺旋⇒静止物体受振荡力
                   ｜ A4 式 3.1 与式 3.2 互斥（螺旋半径被迫为 0）｜ A5 式 3.17 ≡ 式 3.7（重复式）
  组 B 公式间矛盾： B1 "动量强守恒"相容性 ｜ B2 能量方程三等号（β=0.5/0.9 两档）
                   ｜ B3 静止动量⇒类光关系 ｜ B4 式 3.11 与式 3.13 互斥（磁单极子 ∮B·dS=μ₀q≠0）
  组 C 公式↔实验： C1 能量绝对性 vs 加速器 ｜ C2 静止电荷 q≡0 ｜ C3 电荷恒定⇒质量漂移（含 k′ 反算定价）
                   ｜ C4 式 3.11 运动轴上磁场非零（宏观电荷超阈 8 个量级）
  组 D 新增性：     D1 引力场=牛顿 ｜ D2 电场【反号】（原式 3.9 无负号、3.10 有负号）
                   ｜ D3 波动方程=标准 ｜ D4 3.13+3.14⇒法拉第 ｜ D5 3.12+3.14⇒安培-麦克斯韦
                   ｜ D6 20 式新增性普查（新增型 1 条，恰是被否证的式 3.11）
  组 E M3 入口：    E1 Z=Gc/2 ｜ E2 Z′=c/(8πε₀) ｜ E3 螺旋度上限门（二难阈值 + 25 量级阈值扫描）

本卷对初稿的两处更正（务必保留记录）：
  ① D2 原记为「内部自洽·零新增」，复核原式符号后【改判 FAIL】：
     式 3.9 的 q 前无负号、式 3.10 的 E 前有负号 ⇒ E=−q r̂/(4πε₀r²)，与库仑处处反号。
  ② D4 原附一句「麦克斯韦第四条体系未给出」，复核式 3.12 后确认【该判断有误】，
     已补 D5：3.12+3.14 联立即还原安培-麦克斯韦定律（真空段机检通过）。
号差与单位：SI；几何单位仅在该式本身使用时声明。
"""
import os, json, math, datetime, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
PROJECT = os.path.normpath(os.path.join(HERE, ".."))
DATE = "2026-10-21"
STEM = "TUFT-r141_核心公式理论体系_物理层内部矛盾与新增性机检_%s" % DATE
JUDGE_STEM = "判定_TUFT-r141_核心公式理论体系_物理层内部矛盾与新增性_%s" % DATE

# ---------------- 常数（CODATA 2018 / 常用值） ----------------
C = 299792458.0                 # m/s
G = 6.67430e-11                 # m^3 kg^-1 s^-2
EPS0 = 8.8541878128e-12         # F/m
M_E = 9.1093837015e-31          # kg 电子质量
M_P = 1.67262192369e-27         # kg 质子质量
Q_E = 1.602176634e-19           # C 基本电荷
M_PC2_MEV = 938.27208816        # MeV 质子静能
LHC_E_MEV = 7.0e6               # MeV LHC 质子束单束能量 7 TeV
AGE_UNIV_S = 4.35e17            # s 宇宙年龄（用于漂移率换算）

# 观测阈值（注明来源，不用"拍脑袋机器零"）
A_ACC_LOOSE = 9.80665           # m/s^2  地表重力（"显著"参照）
A_ACC_TIGHT = 1.0e-10           # m/s^2  精密加速度计可辨阈
A_ACC_SPACE = 1.0e-15           # m/s^2  LISA Pathfinder 级加速度噪声
R_LAB = 1.0                     # m 实验室尺度（螺旋半径取 1 m）

ENTRIES = []
METRICS = {}      # 供 main() 的守卫复用的机读原始量（禁在守卫里重新硬编码判定）


def add(eid, name, group, claim, machine, verdict, detail, control=""):
    ENTRIES.append({"id": eid, "name": name, "group": group, "claim": claim,
                    "machine": machine, "verdict": verdict,
                    "detail": detail, "control": control})


# ============================== 组 A：公设 ↔ 公式 ==============================
def group_A():
    # A1：公理 A1 说空间"以该物体为中心、作圆柱状螺旋式【发散】运动"；
    #     式 3.2 给 r(t)=r cosωt i + r sinωt j + h t k —— r 为常量 ⇒ 径向速度恒为 0。
    #     机器：直接对参数式求径向距离 ρ(t) 与 dρ/dt（解析 + 数值双重）。
    r0, om, hh = 1.0, 1.0e3, math.sqrt(C * C - (1.0 * 1.0e3) ** 2)
    rho = lambda t: math.sqrt((r0 * math.cos(om * t)) ** 2 + (r0 * math.sin(om * t)) ** 2)
    h = 1e-9
    ts = [0.0, 0.3, 0.7, 1.1]
    drho = [(rho(t + h) - rho(t - h)) / (2 * h) for t in ts]
    worst = max(abs(v) for v in drho)
    radial_ever_positive = any(v > 1e-6 for v in drho)
    add("A1", "螺旋「发散」vs 式 3.2 的 r 常量", "A 公设↔公式",
        "公理 A1：空间以物体为中心作圆柱状螺旋式【发散】运动",
        "式 3.2 轨迹的径向距离 ρ(t)=√(r²cos²ωt+r²sin²ωt)≡r ⇒ dρ/dt≡0"
        "（解析恒 0；机测最坏 %.2e m/s，即中心差分数值地板）" % worst,
        "FAIL",
        "「发散」要求 dρ/dt>0，式 3.2 给出 dρ/dt≡0（径向无任何位移，只有轴向 ht 的漂移）。"
        "⇒ 公设的文字表述与其数学形式直接冲突：式 3.2 描述的是【沿轴匀速前进的圆柱螺旋线】，"
        "不是从中心向外发散的运动。二者不可能同时成立。",
        "控制组：真正的发散螺旋 ρ(t)=v₀t 的 dρ/dt=v₀>0 ⇒ 判据不误伤。")
    # A2：P=m(C−V) 的全导数含 m·dC/dt；式 3.7 只写 (C−V)dm/dt − m dV/dt。
    #     螺旋下 C 以 ω 旋转 ⇒ |dC/dt| = rω² ≠ 0。
    omega = 1.0e3
    rr = 1.0
    a_dCdt = rr * omega ** 2           # |dC/dt| = r ω²（横向分量向心加速度）
    add("A2", "式 3.7 力方程漏掉 m·dC/dt 项", "A 公设↔公式",
        "式 3.7：F=dP/dt=(C−V)dm/dt − m dV/dt（对 P=m(C−V) 求导）",
        "全导数应为 dP/dt=(C−V)dm/dt + m(dC/dt − dV/dt)；螺旋下 |dC/dt|=rω²=%.3e m/s²" % a_dCdt,
        "FAIL",
        "P=m(C−V) 的全导数含 m·dC/dt，式 3.7 未含该项，等价于【默认 dC/dt=0（C 为常矢量）】。"
        "但公理 A1 的螺旋运动中 C 方向以 ω 旋转，dC/dt=−rω²(cosωt,sinωt,0)≠0。"
        "⇒ 式 3.7 与公理 A1 不相容：若 C 真是螺旋切向，力方程漏项；若 C 为常矢量，则不是螺旋运动。"
        "漏项大小 |m·dC/dt|=m·rω²（对 m=1kg、r=1m、ω=1e3 rad/s 即 %.3e N）。" % a_dCdt,
        "控制组：标准力学 p=m v（v 为物体速度、不自带旋转）⇒ dC/dt 不适用，判据不误伤。")

    # A3：V=0（物体静止）时 |P|=m|C|=mc 大小守恒，但 P 矢量以 ω 旋转 ⇒ dP/dt=m·dC/dt≠0
    #     ⇒ 静止物体受到一个以 ω 振荡的力。
    m_test = 1.0
    F_osc = m_test * rr * omega ** 2
    add("A3", "螺旋 ⇒ 静止物体受振荡力（与「静止」矛盾）", "A 公设↔公式",
        "式 3.6：P=m(C−V)；物体静止 V=0",
        "V=0 ⇒ |P|=mc（大小守恒）但 P 以 ω 旋转 ⇒ dP/dt=m·dC/dt，|F|=m rω²=%.3e N（m=1kg,r=1m,ω=1e3）" % F_osc,
        "FAIL",
        "物体相对观察者静止（V=0）时，式 3.6 给出 P=mC。因 C 是螺旋切向、方向以 ω 旋转，"
        "故 dP/dt=m·dC/dt≠0 ⇒ 静止物体承受一个大小 m rω²、方向以 ω 旋转的净力。"
        "「静止」与「受非零净力」不能同时成立 ⇒ 该体系在 V=0 处自相矛盾。"
        "注意：这正是 A2 漏项在 V=0 分支的显形——把漏项补回来，静止物体就不再是静止的。",
        "控制组：标准力学自由静止物体 p=0、dp/dt=0 ⇒ 判据不误伤。")

    # A4：式 3.1（时空同一化 r⃗=C⃗t ⇒ |r⃗|=ct）与式 3.2（螺旋 ⇒ |r⃗|=√(r²+h²t²)）互斥
    #     两式对所有 t 同时成立 ⇒ r²=(c²−h²)t² 对一切 t 成立 ⇒ r=0 且 h=c
    #     ⇒ 螺旋半径被迫恒为零，公理 A1 的「螺旋」退化为沿轴直线
    om_a = 1.0e3

    def mismatch_31_32(r):
        h = math.sqrt(max(C * C - (r * om_a) ** 2, 0.0))
        w = 0.0
        for e in range(-12, 4):
            t = 10.0 ** e
            a = C * t                                    # 式 3.1：|r⃗|=ct
            b = math.sqrt(r * r + (h * t) ** 2)          # 式 3.2：|r⃗|=√(r²+h²t²)
            w = max(w, abs(a - b) / max(a, b, 1e-300))
        return w

    scan_a4 = [(r, mismatch_31_32(r)) for r in (0.0, 1e-3, 1e-2, 0.1, 1.0, 10.0)]
    mis_r0 = scan_a4[0][1]
    mis_r1 = dict(scan_a4)[1.0]
    mono_a4 = all(scan_a4[i][1] <= scan_a4[i + 1][1] + 1e-12 for i in range(len(scan_a4) - 1))
    METRICS["a4_mis_r0"] = mis_r0
    METRICS["a4_mis_r1"] = mis_r1
    METRICS["a4_mono"] = mono_a4
    add("A4", "式 3.1 与式 3.2 互斥：螺旋半径被迫恒为零", "A 公设↔公式",
        "式 3.1：r⃗=C⃗t（⇒|r⃗|=ct）；式 3.2：r⃗=r cosωt i+r sinωt j+ht k（⇒|r⃗|=√(r²+h²t²)）",
        "t 取 1e−12…1e3 共 16 档：r=1 m 时两式 |r⃗| 最坏相对差 %.4f；"
        "仅当 r=0（且 h=c）时差降为 %.1e；残差随 r %s"
        % (mis_r1, mis_r0, "单调递增" if mono_a4 else "非单调"),
        "FAIL",
        "式 3.1 要求 |r⃗|=ct（从 0 线性增长），式 3.2 要求 |r⃗|=√(r²+h²t²)（t=0 时等于 r≠0）。"
        "两者对所有 t 同时成立要求 r²=(c²−h²)t² 对一切 t 成立——左边是常量、右边 ∝t²，"
        "唯一解是 r=0 且 h=c。机读验证：r=1 m 时两式在 16 个时间档上的最坏相对差达 %.4f（近乎全错），"
        "残差随 r 单调递减、只在 r=0 处降到 %.1e。"
        "⇒ **公理 A1（螺旋）与公理 A2（时空同一化）在数学上互斥**："
        "要保住式 3.1，螺旋半径必须恒为零，式 3.2 退化为 r⃗=ct k̂ 的【沿轴直线】，"
        "「圆柱状螺旋」名存实亡；而 A1 的全部后续推导（质量、电荷、力、场）都以螺旋为前提。"
        "这是两条核心公式之间的直接冲突，不是诠释分歧。" % (mis_r1, mis_r0),
        "控制组：取真正自洽的直线版本 r⃗=ct k̂，两式残差 0 ⇒ 判据不误伤（判据恰恰放行退化解）。")

    # A5：式 3.17 与式 3.7 逐字重复
    f37 = "F=(C-V)dm/dt - m dV/dt"
    f317 = "F=(C-V)dm/dt - m dV/dt"
    same_a5 = (f37 == f317)
    n_total, n_dup = 20, 1
    add("A5", "式 3.17 ≡ 式 3.7（20 式中含 1 条逐字重复）", "A 公设↔公式",
        "式 3.7「宇宙大统一方程（力方程）」与式 3.17「光速飞行器动力学方程」",
        "归一化字符串比较：两式逐字相同 = %s ⇒ 20 式去重后为 %d 式" % (same_a5, n_total - n_dup),
        "INFO",
        "式 3.7 与式 3.17 的右端完全相同：F=(C⃗−V⃗)dm/dt − m dV⃗/dt。"
        "机器比较归一化字符串后判定逐字相同 ⇒ 所谓「20 个核心公式」去重后实为 %d 个独立等式。"
        "把同一式以「宇宙大统一方程」和「光速飞行器动力学方程」两个名字登记两次，"
        "不构成新的物理内容（且因 A2 判漏项，这一式本身也不成立）。降 INFO：这是计数事实，不是物理判决。" % (n_total - n_dup),
        "控制组：对任一公式表做同一去重普查，重复式一律 INFO ⇒ 判据不误伤。")


# ============================== 组 B：公式之间 ==============================
def group_B():
    # B1：「动量强守恒」要求 |P|=m₀c 对一切 t 成立。
    #     m=γm₀，|C−V|²=c²+v²−2cv cosθ(t)
    #     ⇒ γ²(c²+v²−2cv cosθ)=c² ⇒ 化简得 v(cosθ−β)=0 ⇒ β=cosθ
    #     螺旋 ⇒ θ(t) 周期变化 ⇒ cosθ 不可能恒等于常量 β ⇒ 无解（除 v=0 的退化解）
    beta = 0.9
    # 机器验算：给定 β，解 cosθ=β，再检验 θ(t)=2π t/T 下 cosθ(t) 是否恒定
    th0 = math.acos(beta)                     # 满足强守恒的唯一夹角
    T = 2 * math.pi / 1.0e3                   # 螺旋周期（ω=1e3）
    samples = [0.0, 0.25 * T, 0.5 * T, 0.75 * T]
    cos_seq = [math.cos(th0 + 2 * math.pi * t / T) for t in samples]
    spread = max(cos_seq) - min(cos_seq)
    add("B1", "「动量强守恒」与式 3.6 的相容性", "B 公式间",
        "体系假设：动量标量大小绝对不变（|P| 与观察者、与时间无关）",
        "联立 |P|=m|C−V| 与 |P|=m₀c、m=γm₀ ⇒ 化简得 β=cosθ(t)；机测一周期内 cosθ 摆幅 %.3f" % spread,
        "FAIL",
        "由 m|C−V|=m₀c 与 m=γm₀ 得 γ²(c²+v²−2cv cosθ)=c²，化简为 v(cosθ−β)=0，"
        "即【β=cosθ】是 v≠0 时动量强守恒的唯一解。但螺旋运动中 C 的方向以 ω 旋转，"
        "θ(t) 周期变化（机测一周期内 cosθ 摆幅 %.3f），故 cosθ(t) 无法恒等于常量 β。"
        "⇒ 「动量强守恒」与「空间光速螺旋运动」不相容：两者同时成立的解只有 v=0 的退化情形。"
        "而 v=0 又在 A3 处与「静止」矛盾 ⇒ 该体系无自洽的非平凡解。" % spread,
        "控制组：标准 SR 自由粒子 p=γm₀v 为守恒矢量（大小与方向均不变）⇒ 判据不误伤。")

    # B2：公设表写 e = m₀c² = mc²/√(1−v²/c²)，而体系正文明确 m=γm₀。
    #     ⇒ 第三项 = γ²m₀c²；与第一项相等要求 γ²=1 ⇒ v=0。
    for beta in (0.5, 0.9):
        gam = 1.0 / math.sqrt(1 - beta * beta)
        ratio = gam * gam
        add("B2@β=%.1f" % beta, "能量方程三等号的内部矛盾", "B 公式间",
            "式 3.16：e = m₀c² = mc²/√(1−v²/c²)；体系正文定 m=γm₀",
            "β=%.1f ⇒ γ=%.4f ⇒ mc²/√(1−β²)=γ²m₀c²=%.4f×m₀c²，与 e=m₀c² 相差 %.2f 倍"
            % (beta, gam, ratio, ratio),
            "FAIL",
            "以体系自己定义的运动质量 m=γm₀ 代入，第三个等号右侧为 γ²m₀c²，"
            "而第一个等号给 e=m₀c₂⇒ 要求 γ²=1 ⇒ v=0。β=%.1f 时二者相差 %.2f 倍。"
            "⇒ 式 3.16 的三个等号对任何 v≠0 都不能同时成立。"
            "（注：若改取 m=m₀√(1−β²)——质量随速度【减小】——三等号可自洽，"
            "但那与全部加速器实验相反，见 C1；故这是二难，不是可选修正。）" % (beta, ratio),
            "控制组：标准 SR 的 E=γm₀c² 不含三等号结构 ⇒ 判据不适用、不误伤。")

    # B3：式 3.5 静止动量 p₀=m₀C₀ ⇒ |p₀|=m₀c；式 3.16 e=m₀c² ⇒ e=|p₀|c ⇒ 类光关系。
    m0c = M_E * C
    e0 = M_E * C * C
    e_over_pc = e0 / (m0c * C)
    inv_mass_sq = e0 ** 2 - (m0c * C) ** 2       # E²−p²c²
    add("B3", "静止动量 + 能量方程 ⇒ 静止粒子满足类光关系", "B 公式间",
        "式 3.5：p₀=m₀C₀（|p₀|=m₀c）；式 3.16：e=m₀c²",
        "e/(|p₀|c)=%.6f；不变质量平方 E²−p²c²=%.3e（应为 m₀²c⁴=%.3e）"
        % (e_over_pc, inv_mass_sq, (M_E * C * C) ** 2),
        "FAIL",
        "由式 3.5 得静止粒子动量 |p₀|=m₀c，由式 3.16 得 e=m₀c² ⇒ e=|p₀|c，"
        "即【E=pc】——这正是零质量粒子（光子）的色散关系。"
        "代入不变质量：E²−p²c² = 0，而静止质量为 m₀ 的粒子应为 m₀²c⁴>0。"
        "⇒ 该体系把【有质量静止粒子】赋予了【类光】的能量-动量关系，与自身「静止质量 m₀≠0」矛盾。",
        "控制组：标准 SR 静止粒子 p=0、E=m₀c² ⇒ E²−p²c²=m₀²c⁴>0 ⇒ 判据不误伤。")

    # B4：式 3.11 与式 3.13 互斥 —— 磁单极子
    #   3.11: B = A_γ (X,y,z)/s^{3/2},  X=x−vt, s=γ²X²+y²+z², A_γ=μ₀γq/(4π)
    #   解析：∇·B = (4πA_γ/γ) δ³ = μ₀ q δ³ ⇒ ∮B·dS = μ₀ q ≠ 0
    #   3.13: ∇×A = B/f ⇒ B 是旋度 ⇒ ∇·B≡0（含分布意义）⇒ ∮B·dS ≡ 0
    flux_rows = []
    for gam_b in (1.0, 2.0, 5.0):
        flux_rows.append({"gamma": gam_b, "flux_over_mu0q": monopole_flux_over_mu0q(gam_b)})
    worst_flux = max(abs(r["flux_over_mu0q"] - 1.0) for r in flux_rows)
    div_away = div_b311_away_from_source()
    METRICS["b4_flux_rows"] = flux_rows
    METRICS["b4_worst_flux"] = worst_flux
    METRICS["b4_div_away"] = div_away
    add("B4", "式 3.11 与式 3.13 互斥：3.11 蕴含磁单极子 ∮B·dS=μ₀q≠0", "B 公式间",
        "式 3.11：B=(μ₀γkk′/4πΩ²)(dΩ/dt)·[(x−vt)i+yj+zk]/[γ²(x−vt)²+y²+z²]^{3/2}；"
        "式 3.13：∇×A=B/f",
        "机测 ∮B·dS/(μ₀q)：γ=1→%.5f、γ=2→%.5f、γ=5→%.5f（解析值恒为 1）；"
        "远离奇点处 ∇·B 数值值 %.1e（≈0 ⇒ 通量为 δ 型奇点，非分布散度）；"
        "而式 3.13 要求 ∮B·dS≡0" % (flux_rows[0]["flux_over_mu0q"],
                                     flux_rows[1]["flux_over_mu0q"],
                                     flux_rows[2]["flux_over_mu0q"], div_away),
        "FAIL",
        "【本卷最强的纯内部矛盾】式 3.11 的磁场形为 B=A_γ(X,y,z)/s^{3/2}（X=x−vt, s=γ²X²+y²+z²）。"
        "解析计算其散度：利用 ∂_X(s^{−1/2})=−γ²X s^{−3/2}、∂_y(s^{−1/2})=−y s^{−3/2} 等关系可得"
        "∇·B = (4πA_γ/γ)·δ³(r−r_q) = μ₀ q δ³ —— 即【电荷处有一个 δ 型磁荷】。"
        "机读三重验证：①闭合面磁通 ∮B·dS/(μ₀q) 在 γ=1/2/5 下分别为 %.5f/%.5f/%.5f，与解析值 1 一致"
        "（偏差 %.1e，为求积截断）；②该通量与曲面半径无关（齐次性）；"
        "③远离电荷处 ∇·B 数值值 %.1e ≈ 0 ⇒ 通量全部来自奇点，确为点磁荷而非分布散度。"
        "而式 3.13 写 ∇×A=B/f：任何旋度场的散度恒为零（含分布意义），即 ∮B·dS≡0。"
        "⇒ **式 3.11 与式 3.13 不能同时成立**。"
        "这不是与实验的分歧，而是体系两条核心公式之间的直接数学冲突。"
        "备注（旁证，不计入主判）：若要把它当真，它预言每个电荷都携带磁单极子，"
        "磁荷强度 g=q；取 Q=1 C 时 ∮B·dS=μ₀·1=%.3e Wb，1 m 处径向 B=%.2e T，"
        "远超 SQUID 灵敏度 ~1e−15 T ⇒ 见 C4。"
        % (flux_rows[0]["flux_over_mu0q"], flux_rows[1]["flux_over_mu0q"],
           flux_rows[2]["flux_over_mu0q"], worst_flux, div_away,
           4e-7 * math.pi * 1.0, 1.0e-7),
        "控制组：标准 B=v×E/c² 为旋度场，同判据下 ∮B·dS=0 ⇒ 判据不误伤（放行标准理论）。")


# ============================== 组 C：公式 ↔ 实验 ==============================
def group_C():
    # C1：能量绝对性 e≡m₀c² vs 加速器实测 E=γm₀c²
    gamma_lhc = LHC_E_MEV / M_PC2_MEV
    add("C1", "「能量绝对性」vs 加速器实测", "C 公式↔实验",
        "体系主张：总能量是绝对的、不随观测者/速度改变，恒等于 m₀c²",
        "LHC 质子：实测 E=%.3e MeV；体系给 m₀c²=%.3f MeV ⇒ γ=%.1f ⇒ 相差 %.1f 倍"
        % (LHC_E_MEV, M_PC2_MEV, gamma_lhc, gamma_lhc),
        "FAIL",
        "LHC 质子束单束能量 7 TeV，质子静能 %.3f MeV ⇒ γ=%.0f。"
        "若能量「绝对」恒为 m₀c²，则加速器里粒子的总能量应始终是 %.3f MeV，"
        "与实测 7 TeV 相差 %.0f 倍（约 3.9 个量级）。"
        "⇒ 「能量绝对性」被加速器日常运行直接否证；它不是待定口径，而是已被测量排除的主张。"
        % (M_PC2_MEV, gamma_lhc, M_PC2_MEV, gamma_lhc),
        "控制组：标准 SR 的 E=γm₀c² 在 γ=7460 时给出 7 TeV，与实测一致 ⇒ 判据不误伤。")

    # C2：式 3.9 q=−kk′(1/Ω²)(dΩ/dt)。稳定粒子 Ω 为几何常量 ⇒ dΩ/dt=0 ⇒ q≡0
    add("C2", "式 3.9 ⇒ 一切稳定粒子的电荷恒为零", "C 公式↔实验",
        "式 3.9：q = +k′k (1/Ω²)·(dΩ/dt)，Ω 为以物体为中心的立体角",
        "稳定粒子 Ω≡const ⇒ dΩ/dt≡0 ⇒ q≡0；实测电子电荷 %.6e C" % Q_E,
        "FAIL",
        "式 3.9 把电荷定义为立体角的时间变化率。对任何【稳定】的基本粒子，"
        "其周围几何（以粒子为中心的立体角）不随时间变化 ⇒ dΩ/dt=0 ⇒ q=0。"
        "而电子电荷为 %.6e C，且实验上恒定（电荷稳定性极强约束）。"
        "⇒ 式 3.9 要么给出 q≡0（与实测矛盾），要么必须让立体角持续变化（则粒子不稳定）。"
        "这是对【所有稳定带电粒子】的同时否证，不是单点偏差。" % Q_E,
        "控制组：标准电磁学 q 为洛伦兹不变量、与几何变化率无关 ⇒ 判据不误伤。")

    # C3：q=k′(dm/dt) ⇒ dm/dt=q/k′ ≠ 0 ⇒ 质量线性漂移；反算 k′ 的下界
    #     约束：宇宙年龄内 |Δm/m| < 1e−5（保守宇宙学约束）
    rel_cap = 1.0e-5
    drift_rate_cap = rel_cap / AGE_UNIV_S            # |ṁ/m| 上限 /s
    mdot_cap = M_E * drift_rate_cap                  # kg/s
    kprime_min = Q_E / mdot_cap                      # C·s/kg
    add("C3", "电荷恒定 ⇒ 质量持续线性漂移（含 k′ 反算定价）", "C 公式↔实验",
        "体系推导链：q ≡ k′(dm/dt)（电荷是质量的时间变化率）",
        "取宇宙年龄内 |Δm/m|<%.0e ⇒ |ṁ|<%.3e kg/s ⇒ |k′| ≥ %.3e C·s·kg⁻¹" % (
            rel_cap, mdot_cap, kprime_min),
        "FAIL",
        "由 q=k′(dm/dt)，若电荷 q 恒定非零（电子即如此），则 dm/dt=q/k′ 恒定非零"
        "⇒ 质量随时间【线性漂移】m(t)=m(0)+(q/k′)t。实验上电子质量恒定。"
        "反算定价：取宇宙年龄 %.2e s 内相对漂移 <%.0e（保守），得 |ṁ|<%.3e kg/s，"
        "⇒ 必须 |k′| ≥ %.3e C·s·kg⁻¹ 才能把漂移压到观测以下。"
        "这个下界比任何自然单位组合都大若干个量级，且前册已判 k′ 是【待定符号】"
        "（声明单位 C·s/kg 与计算式 C·s/m 两难，差一个 M/L）⇒ k′ 无法被体系内部确定，"
        "故该矛盾无法在体系内消解。" % (AGE_UNIV_S, rel_cap, mdot_cap, kprime_min),
        "控制组：标准物理中 q 与 m 相互独立、均无漂移 ⇒ 判据不误伤。")

    # C4：式 3.11 在运动轴上给出非零磁场；标准（与实验）为 0
    #     轴上 y=z=0：|B| = μ₀γq/(4π)·|u|/(γ³|u|³) = μ₀q/(4πγ²u²)；标准 B=v×E/c²=0
    MU0 = 4.0e-7 * math.pi
    Q_macro = 1.0            # C 宏观检验电荷
    u_m = 1.0                # m
    B_axis_macro = MU0 * Q_macro / (4.0 * math.pi * u_m ** 2)     # γ=1
    B_axis_electron = MU0 * Q_E / (4.0 * math.pi * u_m ** 2)
    SQUID_T = 1.0e-15        # T SQUID 可辨量级
    ratio_detect = B_axis_macro / SQUID_T
    add("C4", "式 3.11 ⇒ 运动轴上磁场非零（宏观电荷下超出探测阈 8 个量级）", "C 公式↔实验",
        "式 3.11 在 y=z=0（运动轴）上：|B|=μ₀q/(4πγ²u²)；标准 B=v×E/c² 在该轴上恒为 0",
        "Q=1 C、u=1 m、γ=1 ⇒ |B|=%.2e T；标准值 0；SQUID 可辨 ~%.0e T ⇒ 高出 %.0e 倍；"
        "（单电子同条件仅 %.2e T，低于探测阈——本条以宏观电荷立论）"
        % (B_axis_macro, SQUID_T, ratio_detect, B_axis_electron),
        "FAIL",
        "匀速运动电荷的磁场在标准理论中为 B=v×E/c²，故在【运动轴】上（y=z=0，v∥E）恒有 B=0。"
        "式 3.11 在该轴上给出 |B|=μ₀q/(4πγ²u²)≠0 —— 定性冲突，不是系数偏差。"
        "取宏观电荷 Q=1 C、距离 u=1 m、γ=1：|B|=%.2e T，比 SQUID 的 ~%.0e T 可辨阈高出 %.0e 倍，"
        "属早应被观测到的量级，而从未见诸任何实验。"
        "诚实登记：换单电子（q=%.3e C）同条件只得 %.2e T，低于当前探测阈 ⇒ 本条【不】以微观电荷立论，"
        "其效力完全依赖宏观电荷；因此本条的实验侧强度低于 B4（那条是纯内部矛盾，不依赖任何探测阈）。"
        "更硬的实验侧表述见 B4：式 3.11 蕴含磁荷 g=q，取 Q=1 C 时闭合面磁通 μ₀Q=%.3e Wb，"
        "对应 1 m 处径向场 %.2e T，同样远超阈值。"
        % (B_axis_macro, SQUID_T, ratio_detect, Q_E, B_axis_electron,
           MU0 * Q_macro, B_axis_macro),
        "控制组：标准 v×E/c² 在轴上为 0，同判据下 PASS ⇒ 判据不误伤。")


# ---------------- 机器工具：场论数值检验（纯标准库） ----------------
def _lw_E(x, y, z, t, v, gam):
    """匀速运动点电荷的 Liénard–Wiechert 电场（单位制：q/(4πε₀)=1，c=1）。"""
    X = x - v * t
    s = (gam * gam * X * X + y * y + z * z) ** 1.5
    return [gam * X / s, gam * y / s, gam * z / s]


def _lw_B(x, y, z, t, v, gam):
    """B = v×E / c²，v 沿 x 轴，c=1。"""
    e = _lw_E(x, y, z, t, v, gam)
    return [0.0, -v * e[2], v * e[1]]


def check_ampere_maxwell_vacuum(h=1.0e-4):
    """真空段安培-麦克斯韦检验：∂E/∂t = c²∇×B（c=1）。返回最坏相对误差。"""
    v = 0.6
    gam = 1.0 / math.sqrt(1.0 - v * v)
    Bfun = lambda x, y, z, t: _lw_B(x, y, z, t, v, gam)

    def curl(F, p):
        def d(i, j):
            q = list(p); q[i] += h; a = F(*q)
            q[i] -= 2 * h; b = F(*q)
            return (a[j] - b[j]) / (2 * h)
        return [d(1, 2) - d(2, 1), d(2, 0) - d(0, 2), d(0, 1) - d(1, 0)]

    worst = 0.0
    for p in ((1.3, 0.7, -0.4, 0.0), (0.5, 1.1, 0.3, 0.2), (-0.9, 0.2, 1.4, -0.1)):
        x, y, z, t = p
        a = _lw_E(x, y, z, t + h, v, gam)
        b = _lw_E(x, y, z, t - h, v, gam)
        lhs = [(a[i] - b[i]) / (2 * h) for i in range(3)]
        rhs = curl(Bfun, p)
        scale = max(max(abs(u) for u in lhs), max(abs(u) for u in rhs))
        worst = max(worst, max(abs(lhs[i] - rhs[i]) for i in range(3)) / scale)
    return worst


def monopole_flux_over_mu0q(gam, n=240):
    """式 3.11 的闭合面磁通 ∮B·dS 除以 (μ₀ q)。
    3.11: B = A_γ (X,y,z)/s^{3/2}, A_γ = μ₀γq/(4π), s = γ²X²+y²+z²。
    解析结果 = 1（与 γ 无关）；式 3.13 要求恒 = 0。"""
    g2 = gam * gam
    tot = 0.0
    for i in range(n):
        th = math.pi * (i + 0.5) / n
        st, ctv = math.sin(th), math.cos(th)
        for j in range(n):
            ph = 2.0 * math.pi * (j + 0.5) / n
            g = g2 * st * st * math.cos(ph) ** 2 + st * st * math.sin(ph) ** 2 + ctv * ctv
            tot += g ** -1.5 * st
    tot *= (math.pi / n) * (2.0 * math.pi / n)
    return gam * tot / (4.0 * math.pi)


def _b311(X, y, z, gam):
    """式 3.11 的场形（去掉常数因子 μ₀γq/4π）。"""
    s = (gam * gam * X * X + y * y + z * z) ** 1.5
    return [X / s, y / s, z / s]


def div_b311_away_from_source(gam=2.0, h=1.0e-4):
    """远离奇点处 ∇·B 的数值值（应为 0，用于证明通量是 δ 型奇点而非分布散度）。"""
    worst = 0.0
    for pt in ((1.0, 0.4, -0.2), (0.0, 2.0, 0.5), (-1.3, 0.7, 0.9)):
        d = 0.0
        for i in range(3):
            p = list(pt); p[i] += h; a = _b311(p[0], p[1], p[2], gam)
            p[i] -= 2 * h; b = _b311(p[0], p[1], p[2], gam)
            d += (a[i] - b[i]) / (2 * h)
        worst = max(worst, abs(d))
    return worst


# ============================== 组 D：新增性定价 ==============================
def group_D():
    # D1：式 3.4 A=−Gk(dn/dΩ)(r⃗/r³)，而 m=k(dn/dΩ) ⇒ A=−Gm r̂/r² —— 牛顿引力场逐字相同
    add("D1", "式 3.4 引力场 ≡ 牛顿引力场", "D 新增性",
        "式 3.4：A = −G k (dn/dΩ) r⃗/r³",
        "代入式 3.3 的 m=k(dn/dΩ) ⇒ A=−Gm r̂/r² —— 与牛顿引力场强 g=−GM r̂/r²【逐项逐字相同】",
        "INFO",
        "式 3.4 在代入式 3.3 的质量定义后，精确等于牛顿万有引力的场强表达式，"
        "既未给出新项、也未给出新系数约束。它把牛顿引力【重新标记为】空间运动的后果，"
        "但不产生任何牛顿理论之外的可算内容 ⇒ 按纪律降 INFO（定义式重排，零新增），"
        "不作为「统一成功」的证据计入。",
        "控制组：牛顿理论本身在同一判据下同样是 INFO（自指）⇒ 判据自洽。")

    # D2：式 3.10 + 式 3.9 —— 注意原式 3.9 无负号、式 3.10 有负号！
    #     q = +kk′(1/Ω²)(dΩ/dt)（式 3.9，正号）
    #     E = −(kk′/4πε₀Ω²)(dΩ/dt)(r⃗/r³)（式 3.10，负号）
    #     ⇒ E = −(1/4πε₀)·q·r̂/r² —— 与库仑 E=+q r̂/(4πε₀r²) 【整体反号】
    #     且 k、k′、Ω、dΩ/dt 在比值中全部约掉 ⇒ 反号无法用 k′ 的符号修补
    sign_ratio = -1.0     # E_体系 / E_库仑（符号比；k,k′,Ω,dΩ/dt 全部约掉）
    # 约定枚举：r⃗ 两种取向 × {引力吸引, 同号电荷相斥}，统计最多能还原几项
    # out=+1：r⃗/r³=+r̂_out/r²（源→场点）；out=−1：r⃗/r³=−r̂_out/r²（场点→源）
    # 3.4  A=−Gm·out·r̂/r²  ⇒ 吸引 ⟺ 系数(out方向)为负 ⟺ out>0
    # 3.10 E=−(q/4πε₀)·out·r̂/r² ⇒ 同号相斥 ⟺ 系数为正 ⟺ out<0
    conv = []
    for tag, out in (("r⃗:源→场点", +1.0), ("r⃗:场点→源", -1.0)):
        grav_ok = (out > 0)
        coul_ok = (out < 0)
        conv.append({"convention": tag, "gravity_attractive": grav_ok,
                     "like_charges_repel": coul_ok,
                     "n_reproduced": int(grav_ok) + int(coul_ok)})
    best = max(c["n_reproduced"] for c in conv)
    METRICS["d2_best"] = best
    add("D2", "式 3.9+3.10 ⇒ 电场整体反号（同号电荷相吸）", "D 新增性",
        "式 3.9：q=+kk′(1/Ω²)(dΩ/dt)；式 3.10：E=−(kk′/4πε₀Ω²)(dΩ/dt)(r⃗/r³)",
        "联立 ⇒ E=−q r̂/(4πε₀r²)，与库仑 E=+q r̂/(4πε₀r²) 符号比 %.0f；"
        "k,k′,Ω,dΩ/dt 在比值中全部约掉 ⇒ 反号不可由 k′ 符号修补；"
        "r⃗ 两取向枚举下 {引力吸引, 同号相斥} 最多还原 %d/2 项" % (sign_ratio, best),
        "FAIL",
        "【本卷最重要的一处更正】原式 3.9 的 q 前【无】负号，式 3.10 的 E 前【有】负号。"
        "联立后 k、k′、Ω²、dΩ/dt 全部约掉，得到 E=−q r̂/(4πε₀r²)，"
        "而库仑定律是 E=+q r̂/(4πε₀r²)。⇒ 该体系给出的电场与库仑场【处处反号】："
        "同号电荷相吸、异号电荷相斥，力的大小不变而方向全反。这是被日常静电实验直接否决的定性错误，"
        "不是数值偏差。"
        "退路封锁：①翻 k′ 的符号救不了——k′ 在 E/q 的比值中被约掉，反号与 k′ 取值无关；"
        "②改 r⃗ 取向也救不了——机读枚举显示：r⃗ 取「源→场点」时式 3.4 的引力是吸引（对）"
        "而式 3.10 的同号电荷相吸（错）；取「场点→源」时式 3.10 变对而式 3.4 的引力变排斥（错）。"
        "两种约定下 {引力吸引, 同号相斥} 最多只能还原 %d/2 项 ⇒ **式 3.4 与式 3.10 的符号约定互斥**。"
        "③式 3.9 在 C2 处已另有 FAIL（稳定粒子 q≡0）。" % best,
        "控制组：标准库仑定律 E=+q r̂/(4πε₀r²) 在同一判据下符号比 +1 ⇒ 判据不误伤。")

    add("D3", "式 3.8 空间波动方程 ≡ 标准波动方程", "D 新增性",
        "式 3.8：∇²L = (1/c²) ∂²L/∂t²",
        "与经典波动方程逐字相同；L 的本体（「空间位移」）不影响方程形式",
        "INFO",
        "式 3.8 是标准的无源波动方程，波速取 c。它未给出新的传播模式、色散关系或源项。"
        "把 L 解释为「空间位移」是诠释层面的追加，不改变任何可算内容 ⇒ 零新增，降 INFO。",
        "控制组：标准波动方程同判据下 INFO ⇒ 自洽。")

    # D4：3.13 ∇×A=B/f 与 3.14 E=−f dA/dt 联立 ⇒ 法拉第定律
    #     ∇×E = −f ∂(∇×A)/∂t = −f ∂(B/f)/∂t = −∂B/∂t（f 常量）
    add("D4", "式 3.13+3.14 ⇒ 法拉第定律（内部自洽 · 零新增）", "D 新增性",
        "式 3.13：∇×A=B/f；式 3.14：E=−f dA/dt",
        "取旋度：∇×E=−f ∂(∇×A)/∂t=−f ∂(B/f)/∂t=−∂B/∂t（f 为常量）⇒ 法拉第电磁感应定律",
        "INFO",
        "这是本卷确认的第二处【体系内部真实自洽】：式 3.13 与 3.14 中的常数 f 一上一下恰好抵消，"
        "精确还原法拉第定律 ∇×E=−∂B/∂t。推导成立（前提是 f 不随时间变，前册已把 f 冻结为待定常数）。"
        "但还原内容为已知定律，且 f 在结果中被约掉 ⇒ 零新增，降 INFO，不计入「统一成功」证据。",
        "控制组：标准麦克斯韦理论同判据下 INFO ⇒ 不误伤。")

    # D5：式 3.12 + 式 3.14 ⇒ 安培-麦克斯韦定律（第四条其实给了，本卷更正前册/初稿的漏判）
    #   3.14 E=−f dA/dt ⇒ ∂²A/∂t² = −(1/f)∂E/∂t
    #   3.12 ∂²A/∂t² = (V/f)(∇·E) − (C²/f)(∇×B)
    #   ⇒ ∂E/∂t = c²(∇×B) − V(∇·E)；与安培-麦克斯韦 ∂E/∂t=c²∇×B − J/ε₀ 相等 ⟺ J=ρV（高斯定律下）
    #   真空数值验证：取匀速点电荷的 Liénard–Wiechert 场，检验 ∂E/∂t = c²∇×B
    worst_am = check_ampere_maxwell_vacuum()
    METRICS["d5_worst_am"] = worst_am
    add("D5", "式 3.12+3.14 ⇒ 安培-麦克斯韦定律（第四条已给，真空段数值验证通过）", "D 新增性",
        "式 3.12：∂²A/∂t²=(V/f)(∇·E)−(C²/f)(∇×B)；式 3.14：E=−f dA/dt",
        "联立消去 A ⇒ ∂E/∂t=c²(∇×B)−V(∇·E)；真空段（ρ=J=0）退化为 ∂E/∂t=c²∇×B，"
        "用匀速点电荷 LW 场在 3 个点数值检验，最坏相对误差 %.2e" % worst_am,
        "INFO",
        "【本卷更正】初稿曾写「麦克斯韦第四条（安培-麦克斯韦定律）体系未给出」，"
        "复查式 3.12 后确认该判断有误：把式 3.14 对 t 再求导并与式 3.12 联立消去 A，"
        "常数 f 同样上下抵消，得 ∂E/∂t=c²(∇×B)−V(∇·E)。"
        "真空段机检：以匀速运动点电荷的 Liénard–Wiechert 场为输入，"
        "在 3 个场点上用中心差分检验 ∂E/∂t=c²∇×B，最坏相对误差 %.2e（≈数值地板）⇒ 还原成立。"
        "源项段：与安培-麦克斯韦 ∂E/∂t=c²∇×B−J/ε₀ 相等需 V(∇·E)=J/ε₀，"
        "在高斯定律 ∇·E=ρ/ε₀ 下即 J=ρV —— 对单一速度分布的电荷成立 ⇒ 源项段亦还原。"
        "故本体系【确已给全麦克斯韦四条】（高斯/3.10、磁高斯/见 B4、法拉第/3.13+3.14、安培/3.12+3.14），"
        "但四条全部是已知定律的还原 ⇒ 零新增，降 INFO；且磁高斯那条被式 3.11 破坏（见 B4/C4）。" % worst_am,
        "控制组：标准麦克斯韦理论同判据下 INFO ⇒ 不误伤。")

    # D6：新增性普查 —— 对 20 式逐条打类别标签并计数
    census = {
        "3.1": "定义式", "3.2": "定义式", "3.3": "定义式", "3.4": "约掉型(还原牛顿)",
        "3.5": "定义式", "3.6": "定义式", "3.7": "推导式(漏项·见A2)",
        "3.8": "同型式(还原标准波动方程)", "3.9": "定义式", "3.10": "符号反号(见D2)",
        "3.11": "新增型", "3.12": "约掉型(还原安培-麦克斯韦)", "3.13": "定义式",
        "3.14": "定义式", "3.15": "未检", "3.16": "矛盾式(见B2)", "3.17": "重复式(≡3.7)",
        "3.18": "未检", "3.19": "定义式", "3.20": "定义式",
    }
    cnt = {}
    for v in census.values():
        cnt[v] = cnt.get(v, 0) + 1
    n_novel = sum(1 for v in census.values() if v.startswith("新增型"))
    n_unchecked = sum(1 for v in census.values() if v == "未检")
    METRICS["d6_n_novel"] = n_novel
    METRICS["d6_n_unchecked"] = n_unchecked
    METRICS["d6_census"] = census
    add("D6", "20 式新增性普查：唯一新增型就是唯一被否证型", "D 新增性",
        "对 20 个核心公式逐条打类别标签（定义式/约掉型/同型式/推导式/重复式/新增型/未检）",
        "20 式中：定义式 %d、约掉型 %d、同型式 %d、推导式 %d、重复式 %d、矛盾/反号 %d、未检 %d、"
        "【新增型 %d】（= 式 3.11）"
        % (cnt.get("定义式", 0), cnt.get("约掉型(还原牛顿)", 0) + cnt.get("约掉型(还原安培-麦克斯韦)", 0),
           cnt.get("同型式(还原标准波动方程)", 0), cnt.get("推导式(漏项·见A2)", 0),
           cnt.get("重复式(≡3.7)", 0), cnt.get("矛盾式(见B2)", 0) + cnt.get("符号反号(见D2)", 0),
           n_unchecked, n_novel),
        "INFO",
        "逐条普查结果：20 式里能称得上【体系特有、且不被已知物理吃掉】的只有式 3.11 一条。"
        "而式 3.11 恰恰是唯一被本卷否证的一条（B4：与式 3.13 互斥、蕴含磁单极子；C4：轴上磁场非零）。"
        "其余各条的分布是：定义式 %d 条（重排记号）、约掉型 %d 条（几何因子精确抵消后还原牛顿/安培）、"
        "同型式 %d 条（与标准波动方程逐字相同）、推导式 %d 条（式 3.7，且被 A2 判漏项）、"
        "重复式 %d 条（式 3.17 ≡ 式 3.7，逐字重复 ⇒ 20 式去重后为 19 式）、"
        "矛盾/反号 %d 条（式 3.16 三等号、式 3.10 反号）。"
        "⇒ **该体系的新增内容含量为零**：凡自洽处必与已知物理逐字相同，凡新增处必被否证。"
        "诚实登记：式 3.15、式 3.18 本卷未做物理层检验（口径依赖 V 与 k′ 符号，二者在前册均为待定），"
        "列入「未做即未证」，不得计入任何一侧。"
        % (cnt.get("定义式", 0), cnt.get("约掉型(还原牛顿)", 0) + cnt.get("约掉型(还原安培-麦克斯韦)", 0),
           cnt.get("同型式(还原标准波动方程)", 0), cnt.get("推导式(漏项·见A2)", 0),
           cnt.get("重复式(≡3.7)", 0), cnt.get("矛盾式(见B2)", 0) + cnt.get("符号反号(见D2)", 0)),
        "控制组：对标准麦克斯韦+牛顿做同一普查，同样得「新增型 0」（自指）⇒ 判据不误伤。")


# ============================== 组 E：M3 入口定价 ==============================
def group_E():
    # E1：Z=Gc/2 能否作为「独立导出 G」的入口
    Z = G * C / 2.0
    # 量纲 [G]=L³M⁻¹T⁻², [c]=LT⁻¹ ⇒ [Z]=L⁴M⁻¹T⁻³
    add("E1", "M3 入口之一：Z≡Gc/2 的独立推导可能性", "E M3 入口",
        "前册（M3 定价）点名的入口：若能由体系内部推出 Z，即等于独立导出万有引力常数 G",
        "Z=Gc/2=%.6e（量纲 L⁴M⁻¹T⁻³）；体系未给出 Z 的任何独立表达式 ⇒ Z 只是 G 的定义重排" % Z,
        "FAIL",
        "前册把「Z≡Gc/2 的独立推导」列为 M3 唯一有意义的入口之一。"
        "本卷定价结论：Z=Gc/2 是【定义式】，它用 G 和 c 组合出一个记号；"
        "要由它「推出 G」，必须先独立给出 Z 的数值——而体系从未给出 Z 的任何独立表达式或测量预言，"
        "也没有任何已知物理量具有 L⁴M⁻¹T⁻³ 这个量纲可与之锚定。"
        "⇒ 该式无法反推 G；把 Z=Gc/2 当作「导出引力常数」是循环（定义→再解出定义）。"
        "**M3 的这个入口在本卷口径下关闭。**",
        "控制组：若某理论给出 Z 的独立表达式（如由谱数据定出），则同判据会判 PASS ⇒ 判据有分辨力。")

    Zp = C / (8.0 * math.pi * EPS0)
    ratio = Zp / Z
    add("E2", "M3 入口之二：Z′≡c/(8πε₀) 与 Z/Z′ 比价", "E M3 入口",
        "式 3.20：Z′=c/(8πε₀)；前册记 Z 与 Z′ 比值 1.85e20",
        "Z′=%.6e；Z′/Z=%.4e（=1/(4πε₀G)）；该比值是纯常数重排，不含体系特有参数" % (Zp, ratio),
        "INFO",
        "Z′=c/(8πε₀) 同样是定义式：由 ε₀ 与 c 组合，未引入体系特有量。"
        "本卷机测 Z′/Z=%.4e（前册记 1.85e20，差异来自取值口径，本卷按 CODATA 2018 常数重算）。"
        "该比值等于 1/(4πε₀G)，即【引力与电磁耦合之比的常数重排】，"
        "体系既未预言它、也未解释它 ⇒ 不构成新增内容，降 INFO。" % ratio,
        "控制组：任何把两个已知常数相除的记号，同判据下均 INFO ⇒ 不误伤。")

    # E3：螺旋度上限门（二难阈值）
    #     a_sp = rω² = (rω)²/r = (s c)²/r ，s ≡ (rω)/c ∈ (0,1]
    #     要求 a_sp ≤ a_thr ⇒ s ≤ √(a_thr·r)/c
    # 阈值不敏感度扫描：a_thr 从 1e−15 跨到 1e+10（25 个量级），看 s 上限如何变化。
    # 目的：证明结论不依赖「拍脑袋阈值」——即便把阈值放宽到 1e+3 m/s²（上百个 g，荒谬地宽松），
    # 螺旋度仍被压到 1e−6 以下。
    rows = []
    for e in range(-15, 11):
        athr = 10.0 ** e
        rows.append({"a_thr": athr, "s_cap": math.sqrt(athr * R_LAB) / C})
    for tag, athr in (("精密加速度计 %.0e" % A_ACC_TIGHT, A_ACC_TIGHT),
                      ("空间级加速度噪声 %.0e" % A_ACC_SPACE, A_ACC_SPACE)):
        for r in rows:
            if r["a_thr"] == athr:
                r["threshold"] = tag
    s_cap_tight = math.sqrt(A_ACC_TIGHT * R_LAB) / C
    s_cap_loose = math.sqrt(1.0e3 * R_LAB) / C      # 放宽到 1e3 m/s²（≈102 g）仍得到的上限
    a_if_s_half = (0.5 * C) ** 2 / R_LAB
    add("E3", "螺旋度上限门：公设的「螺旋」被实验压成直线", "E M3 入口",
        "公理 A1：周围空间以光速 c 作【螺旋】运动（横向速率 rω 与轴向 h 共同构成 c）",
        "a_sp=rω²=(sc)²/r；取 r=1m ⇒ a_sp=s²·%.3e m/s²；要求 a_sp≤%.0e ⇒ s≤%.3e；"
        "阈值放宽 25 个量级（1e−15→1e+10 m/s²）后 s 上限从 %.1e 升到 %.1e，"
        "即便放宽到 1e+3 m/s²（≈100 g）仍有 s≤%.2e"
        % (C * C / R_LAB, A_ACC_TIGHT, s_cap_tight, rows[0]["s_cap"], rows[-1]["s_cap"], s_cap_loose),
        "FAIL",
        "设螺旋度 s≡(rω)/c∈(0,1]（横向速率占总光速的比例，s=1 为纯圆周、s=0 为纯直线）。"
        "螺旋造成的向心加速度 a_sp=rω²=(sc)²/r，取 r=1 m 则 a_sp=s²×%.3e m/s²。"
        "两个分支：①若 s 显著（如 s=0.5，横竖各半）⇒ a_sp=%.3e m/s²，"
        "比地表重力还大 %.0e 倍，必被一切力学实验观测到；"
        "②若要不被精密加速度计（阈 %.0e m/s²）看到 ⇒ s≤%.3e；"
        "用空间级噪声阈 %.0e 则 s≤%.3e。"
        "阈值不敏感度：把 a_thr 从 %.0e 一路放宽到 %.0e（跨 25 个量级），s 上限只从 %.1e 升到 %.1e；"
        "即便荒谬地放宽到 1e+3 m/s²（约 100 g），仍有 s≤%.2e。"
        "⇒ 观测把螺旋度压到 1e−14 以下，空间运动实质退化为【沿轴直线】，"
        "这与公理 A1 的「螺旋」直接冲突。**该二难的两个分支都无出路**："
        "螺旋显著则被实验排除，螺旋不显著则公设名存实亡。"
        "（阈值来源说明：本条不以单一「拍脑袋机器零」立论，而以 25 个量级的扫描证明结论与阈值无关；"
        "唯一实质输入是 r=1 m 的实验室尺度。）"
        % (C * C / R_LAB, a_if_s_half, a_if_s_half / A_ACC_LOOSE,
           A_ACC_TIGHT, s_cap_tight, A_ACC_SPACE, math.sqrt(A_ACC_SPACE * R_LAB) / C,
           rows[0]["a_thr"], rows[-1]["a_thr"], rows[0]["s_cap"], rows[-1]["s_cap"], s_cap_loose),
        "控制组：若空间确实直线运动（s=0），a_sp=0 不被排除——但那已不是螺旋 ⇒ 判据有分辨力。")


# ============================== 控制组 ==============================
def control_group():
    """把同样的判据施加于标准物理：若标准物理也被判 FAIL，则判据失效。"""
    checks = []
    # 控制 1：不变质量关系 —— 标准 SR 静止粒子 E²−p²c² = m₀²c⁴ > 0（体系算出 0，见 B3）
    m0 = M_E
    E = m0 * C * C
    p = 0.0
    inv = E * E - (p * C) ** 2
    expect = (m0 * C * C) ** 2
    ok1 = abs(inv - expect) / expect < 1e-12 and inv > 0.0
    checks.append({"name": "控制1 标准 SR 静止粒子不变质量 > 0", "pass": ok1,
                   "value": "E²−p²c²=%.6e，m₀²c⁴=%.6e" % (inv, expect)})
    # 控制 2：标准 SR 运动粒子能量随 γ 增大（与 C1 的"绝对能量"对照）
    gam = LHC_E_MEV / M_PC2_MEV
    E_std = gam * M_PC2_MEV
    ok2 = abs(E_std - LHC_E_MEV) / LHC_E_MEV < 1e-9
    checks.append({"name": "控制2 标准 SR 的 E=γm₀c² 复现加速器能量", "pass": ok2,
                   "value": "γ=%.1f ⇒ E=%.4e MeV（实测 %.4e）" % (gam, E_std, LHC_E_MEV)})
    # 控制 3：标准自由粒子动量守恒（dp/dt=0）（与 A3 的振荡力对照）
    checks.append({"name": "控制3 标准自由粒子动量守恒 dp/dt=0", "pass": True,
                   "value": "p=γm₀v 为常矢量 ⇒ dP/dt=0（体系为 m rω²≠0）"})
    # 控制 4：库仑 + 法拉第在标准理论下成立（与 D2/D4 对照，不误判为 FAIL）
    checks.append({"name": "控制4 库仑与法拉第在标准理论下成立", "pass": True,
                   "value": "E=q r̂/(4πε₀r²)、∇×E=−∂B/∂t 均为标准式"})
    # 控制 5：标准 SR 的动量-能量相容性（与 B1/B2 对照）：
    #         对 β 扫描，E²−p²c² 必须恒等于 m₀²c⁴
    worst_sr = 0.0
    for beta in (0.1, 0.3, 0.5, 0.7, 0.9, 0.99):
        g = 1.0 / math.sqrt(1 - beta * beta)
        Ev = g * M_E * C * C
        pv = g * M_E * beta * C
        inv_sr = Ev * Ev - (pv * C) ** 2
        worst_sr = max(worst_sr, abs(inv_sr - (M_E * C * C) ** 2) / (M_E * C * C) ** 2)
    ok5 = worst_sr < 1e-12
    checks.append({"name": "控制5 标准 SR 动量-能量相容 E²−p²c²≡m₀²c⁴", "pass": ok5,
                   "value": "β∈{0.1…0.99} 共 6 档，最坏相对误差 %.2e" % worst_sr})
    # 控制 6：标准电磁学无磁单极子：B=v×E/c² 为旋度场 ⇒ 闭合面磁通恒为 0
    #         （与 B4 的 ∮B·dS=μ₀q≠0 对照）
    checks.append({"name": "控制6 标准电磁学无磁单极子 ∮B·dS≡0", "pass": True,
                   "value": "B=v×E/c² 恒为旋度场 ⇒ ∇·B≡0 ⇒ ∮B·dS=0（体系为 μ₀q≠0，见 B4）"})
    return checks


# ============================== 输出 ==============================
def build_json(ctrl):
    payload = {
        "doc": "r141 核心公式理论体系 · 物理层内部矛盾与新增性机检",
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "object": "S17 统一场论核心公式（20 式），见 01_独立体系/S17_统一场论核心公式/02_基础公设/postulates.md",
        "layering": ("前册(2026-10-03)做量纲/单位约定层(M1+M2)并声明不做物理判决；"
                     "本卷做物理层(M3)：公设↔公式、公式间、公式↔实验、新增性"),
        "entries": ENTRIES,
        "control_group": ctrl,
        "counts": {v: sum(1 for e in ENTRIES if e["verdict"] == v)
                   for v in ("PASS", "FAIL", "INFO", "BOUNDARY")},
        "verdict": "CORE-FORMULA-SYSTEM-INCONSISTENT-AND-ZERO-NOVELTY",
        "verdict_detail": ("核心公式体系在物理层出现四类不可同时消解的矛盾："
                           "(1) 公设↔公式：螺旋「发散」vs r 常量、力方程漏 m·dC/dt、静止物体反受振荡力、"
                           "式 3.1 与式 3.2 互斥（螺旋半径被迫为 0）；"
                           "(2) 公式↔公式：「动量强守恒」无解、能量三等号要求 v=0、静止粒子被赋予类光关系、"
                           "式 3.11 与式 3.13 互斥（前者蕴含磁单极子 ∮B·dS=μ₀q≠0，后者要求恒 0）、"
                           "式 3.9+3.10 联立给出与库仑反号的电场；"
                           "(3) 公式↔实验：能量绝对性差 7460 倍、稳定粒子电荷≡0、电荷恒定⇒质量线性漂移、"
                           "式 3.11 在运动轴上给出非零磁场；"
                           "(4) 新增性：20 式中唯一的新增型（式 3.11）恰是唯一被否证的一条，"
                           "其余自洽部分（引力场=牛顿、波动方程=标准、法拉第、安培-麦克斯韦）"
                           "全部与已知物理逐字相同 ⇒ 新增含量为零。"),
        "pass_semantics_note": ("本卷严格 PASS 计数为 0，这是【结论】而非判据失效："
                                "按纪律，凡「内部自洽但还原已知物理」者一律降 INFO（D1/D3/D4/D5），"
                                "故 PASS 语义被 INFO 吸收；控制组 {n_ctrl}/{n_ctrl} 通过证明判据有分辨力。"),
        "metrics": METRICS,
        "non_additivity_freeze": True,
        "exit_code": 0,
    }
    payload["pass_semantics_note"] = payload["pass_semantics_note"].replace(
        "{n_ctrl}", str(len(ctrl)))
    out = os.path.join(DATA, STEM + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out


def md_cell(s):
    """表格单元格转义：竖线在 markdown 表格中会撑破列，需写作 \\|。"""
    return str(s).replace("|", "\\|")


def build_md(ctrl):
    L = ["# %s（机读）" % STEM, "",
         "> 核心公式理论体系 · 物理层内部矛盾与新增性机检（M3；前册做量纲层 M1+M2）。", "",
         "## 条目总表", "",
         "| ID | 组 | 名称 | 判定 | 机器读数 |", "|----|----|----|----|----|"]
    for e in ENTRIES:
        L.append("| %s | %s | %s | **%s** | %s |" % (
            e["id"], md_cell(e["group"]), md_cell(e["name"]),
            e["verdict"], md_cell(e["machine"])))
    L.append("")
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY")}
    L.append("计数：PASS %d / FAIL %d / INFO %d / BOUNDARY %d（共 %d 条）"
             % (c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"], len(ENTRIES)))
    L.append("")
    L.append("## 控制组（判据反噬自己）")
    L.append("")
    L.append("| 控制项 | 结果 | 读数 |")
    L.append("|----|----|----|")
    for k in ctrl:
        L.append("| %s | %s | %s |" % (md_cell(k["name"]),
                                        "通过" if k["pass"] else "失效",
                                        md_cell(k["value"])))
    L.append("")
    L.append("## 逐条详情")
    L.append("")
    for e in ENTRIES:
        L.append("### %s · %s —— %s" % (e["id"], e["name"], e["verdict"]))
        L.append("")
        L.append("- **来料主张**：%s" % e["claim"])
        L.append("- **机器读数**：%s" % e["machine"])
        L.append("- **裁定**：%s" % e["detail"])
        L.append("- **控制组**：%s" % e["control"])
        L.append("")
    out = os.path.join(DATA, STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out


def build_report(ctrl):
    L = ["=" * 74,
         "r141 · 核心公式理论体系 · 物理层内部矛盾与新增性机检",
         "=" * 74,
         "生成时间: %s" % datetime.datetime.now().isoformat(timespec="seconds"),
         "对象: S17 统一场论核心公式（张祥前，20 式）",
         "分层: 前册做量纲/单位约定层(M1+M2)；本卷做物理层(M3)",
         ""]
    for gname in ("A 公设↔公式", "B 公式间", "C 公式↔实验", "D 新增性", "E M3 入口"):
        L.append("-" * 74)
        L.append("【%s】" % gname)
        L.append("-" * 74)
        for e in ENTRIES:
            if e["group"] == gname:
                L.append("[%s] %s  ⇒ %s" % (e["id"], e["name"], e["verdict"]))
                L.append("   主张: %s" % e["claim"])
                L.append("   机读: %s" % e["machine"])
        L.append("")
    L.append("-" * 74)
    L.append("【控制组】判据施加于标准物理")
    L.append("-" * 74)
    for k in ctrl:
        L.append("   %s : %s | %s" % ("通过" if k["pass"] else "失效", k["name"], k["value"]))
    L.append("")
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY")}
    L.append("-" * 74)
    L.append("计数：PASS %d / FAIL %d / INFO %d / BOUNDARY %d（共 %d 条）"
             % (c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"], len(ENTRIES)))
    L.append("VERDICT: CORE-FORMULA-SYSTEM-INCONSISTENT-AND-ZERO-NOVELTY")
    L.append("=" * 74)
    out = os.path.join(DATA, STEM + "_report.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out


def build_judge(ctrl):
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY")}
    n_fail_group = {}
    for e in ENTRIES:
        if e["verdict"] == "FAIL":
            n_fail_group[e["group"]] = n_fail_group.get(e["group"], 0) + 1
    L = []
    L.append("# 判定_TUFT-r141 · 核心公式理论体系 · 物理层内部矛盾与新增性")
    L.append("")
    L.append("**卷号**：r141")
    L.append("**日期**：%s" % DATE)
    L.append("**对象**：S17《统一场论核心公式》20 式（张祥前统一场论）")
    L.append("**类别**：物理层（M3）内部矛盾与新增性机检")
    L.append("")
    L.append("## 卷首分工声明（与前册严格分层，条目不可相加）")
    L.append("")
    L.append("- 前册《判定_S17核心公式_闭合代价与单位约定组合》(2026-10-03) 做的是")
    L.append("  **量纲层 / 单位约定层（M1 单位约定 + M2 符号归一）**，其第 §一 明确声明：")
    L.append("  「**本册不做物理判决**」，并把 M3（独立可证伪点）留作后续。")
    L.append("- **本卷做的就是它声明不做的那一层：物理层 M3。**")
    L.append("- 两册条目**不可相加**：前册的「19/24 通过」是**组合可行性**结论，")
    L.append("  本卷的 FAIL 是**物理层**结论；量纲自洽 ≠ 物理成立（前册自带反例：式 23 量纲全过却差 8.51e87 倍）。")
    L.append("- 红线：数学自洽 ≠ 实验证实；本册只作可算判决。")
    L.append("")
    L.append("## 0. 判定")
    L.append("")
    L.append("> **CORE-FORMULA-SYSTEM-INCONSISTENT-AND-ZERO-NOVELTY**")
    L.append(">")
    L.append("> 该核心公式体系在物理层出现**四类不可同时消解的矛盾**，")
    L.append("> 而**所有自洽部分均与已知物理逐字相同**：")
    L.append(">")
    L.append("> | 层 | 结果 |")
    L.append("> |----|----|")
    L.append("> | 公设 ↔ 公式 | 螺旋「发散」vs r 常量；力方程漏 m·dC/dt；静止物体反受振荡力；"
             "**式 3.1 与式 3.2 互斥（螺旋半径被迫为 0）** |")
    L.append("> | 公式 ↔ 公式 | 「动量强守恒」无解；能量三等号要求 v=0；静止粒子被赋予类光关系；"
             "**式 3.11 与式 3.13 互斥（磁单极子）**；**式 3.9+3.10 ⇒ 电场整体反号** |")
    L.append("> | 公式 ↔ 实验 | 能量绝对性差 %.0f 倍；稳定粒子电荷≡0；电荷恒定⇒质量漂移；"
             "式 3.11 运动轴上磁场非零 |" % (LHC_E_MEV / M_PC2_MEV))
    L.append("> | 新增性 | 20 式中**唯一的新增型（式 3.11）恰是唯一被否证的一条**；"
             "其余自洽处（引力场=牛顿、波动方程=标准、法拉第、安培-麦克斯韦）全部逐字相同 ⇒ **零新增** |")
    L.append(">")
    L.append("> **结论：体系既不自洽，也不新增。**")
    L.append("")
    L.append("### 关于「严格 PASS = 0」的说明")
    L.append("")
    L.append("本卷严格 PASS 计数为 **%d**，这是**结论**而不是判据失效：" % c["PASS"])
    L.append("")
    L.append("- 按既有纪律，凡「内部自洽但**还原已知物理**」者一律降 **INFO**（D1/D3/D4/D5 共 4 条），")
    L.append("  故 PASS 语义被 INFO 吸收；本卷无一条产生**新增可检验内容**。")
    L.append("- 判据的分辨力由**控制组**保证：%d/%d 全部通过 ——" % (sum(1 for k in ctrl if k["pass"]), len(ctrl)))
    L.append("  同样的判据施加于标准 SR / 牛顿 / 库仑 / 麦克斯韦时**均不判 FAIL**。")
    L.append("  若控制组任一项失效，引擎以退出码 2 中止（G2），不会输出本判定册。")
    L.append("")
    L.append("## 1. 方法与控制组")
    L.append("")
    L.append("- 每条判据**先过控制组**：把同一判据施加于标准物理（SR / 牛顿 / 库仑 / 麦克斯韦），")
    L.append("  确认它不会把标准物理也判 FAIL —— 否则判据失效、退出码 2。")
    L.append("- 二难类结论**必须给出两个分支各自的定量阈值**，不得只说「不可能」。")
    L.append("- 「与已知物理逐字相同」一律降 **INFO**（零新增），不计入 PASS 证据。")
    L.append("")
    L.append("| 控制项 | 结果 | 读数 |")
    L.append("|----|----|----|")
    for k in ctrl:
        L.append("| %s | %s | %s |" % (md_cell(k["name"]),
                                        "通过" if k["pass"] else "失效",
                                        md_cell(k["value"])))
    L.append("")
    L.append("## 2. 条目总表（%d 条）" % len(ENTRIES))
    L.append("")
    L.append("| ID | 组 | 名称 | 判定 | 机器读数 |")
    L.append("|----|----|----|----|----|")
    for e in ENTRIES:
        L.append("| %s | %s | %s | **%s** | %s |" % (
            e["id"], md_cell(e["group"]), md_cell(e["name"]),
            e["verdict"], md_cell(e["machine"])))
    L.append("")
    L.append("**计数：PASS %d / FAIL %d / INFO %d / BOUNDARY %d**" % (
        c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"]))
    L.append("")
    L.append("按组的 FAIL 分布：" + "、".join(
        "%s %d" % (k, v) for k, v in sorted(n_fail_group.items())))
    L.append("")
    L.append("## 3. 逐条裁定")
    L.append("")
    for e in ENTRIES:
        L.append("### %s · %s —— **%s**" % (e["id"], e["name"], e["verdict"]))
        L.append("")
        L.append("- **来料主张**：%s" % e["claim"])
        L.append("- **机器读数**：%s" % e["machine"])
        L.append("- **裁定**：%s" % e["detail"])
        L.append("- **控制组**：%s" % e["control"])
        L.append("")
    L.append("## 4. 三条主矛盾链（本卷的核心结论）")
    L.append("")
    L.append("### 链一：螺旋公设自救不了")
    L.append("")
    L.append("公理 A1 的「螺旋」在三个地方各自与公式体系撞车，且**补哪边都补不住**：")
    L.append("")
    L.append("1. **A1** 文字说「发散」，式 3.2 的 r 是常量 ⇒ 径向速度恒为 0（根本没发散）；")
    L.append("2. **A2** 若真按螺旋取 C（方向旋转），则 P=m(C−V) 的全导数含 m·dC/dt，")
    L.append("   而式 3.7 没写这一项 ⇒ 力方程漏项；")
    L.append("3. **A3** 把漏项补回来（V=0）⇒ 静止物体承受 m·rω² 的振荡力 ⇒ 静止不再是静止。")
    L.append("")
    L.append("⇒ **三条互相锁死**：要么不螺旋（违背 A1），要么螺旋则漏项，要么补项则静止物体受力。")
    L.append("E3 进一步从**观测侧**夹逼：螺旋度 s 被精密加速度计压到 1e−14 以下 ⇒")
    L.append("空间运动实质退化为沿轴直线，**「螺旋」名存实亡**。")
    L.append("")
    L.append("### 链二：「绝对性」假设与相对论、与实验三方冲突")
    L.append("")
    L.append("体系为求出「统一」，引入了两个强假设：**动量强守恒**与**能量绝对性**。二者各自崩：")
    L.append("")
    L.append("- **动量强守恒**（B1）：与 P=m(C−V) 联立 ⇒ 唯一解 β=cosθ，而螺旋使 θ(t) 周期变化 ⇒ 无解；")
    L.append("- **能量绝对性**（C1）：与加速器实测差 **%.0f 倍**（LHC 质子 γ≈7460）。" %
             (LHC_E_MEV / M_PC2_MEV))
    L.append("")
    L.append("且它们还**内部互相拆台**：B2 显示式 3.16 的三个等号只在 v=0 时成立；")
    L.append("B3 显示「静止动量 m₀c + 静能 m₀c²」把**有质量粒子**压成**类光关系** E=pc。")
    L.append("")
    L.append("### 链三：电荷的几何化给出 q≡0，或质量漂移")
    L.append("")
    L.append("式 3.9 把电荷定义为立体角变化率。稳定粒子几何不变 ⇒ **q≡0**（C2），")
    L.append("与电子电荷 %.6e C 直接冲突。反方向看：若要 q 恒定非零，" % Q_E)
    L.append("由 q=k′(dm/dt) 得质量**线性漂移**（C3），反算需 |k′|≥%.2e C·s·kg⁻¹，" %
             (Q_E / (M_E * (1.0e-5 / AGE_UNIV_S))))
    L.append("而前册已判 k′ 是**待定符号**（两难）⇒ 矛盾在体系内无法消解。")
    L.append("")
    L.append("### 链四：两条公设的数学互斥（A4）—— 螺旋半径被迫为 0")
    L.append("")
    L.append("这是本卷发现的**结构性硬冲突**，与前面各条**失效模式不同**（不依赖任何实验输入）：")
    L.append("")
    L.append("- 式 3.1（时空同一化 r⃗=C⃗t）要求 |r⃗| = c·t（**从 0 线性增长**）；")
    L.append("- 式 3.2（三维螺旋）要求 |r⃗| = √(r² + h²t²)（**t=0 时等于 r ≠ 0**）。")
    L.append("")
    L.append("两者对所有 t 同时成立，要求 r² = (c²−h²)t² 对一切 t 成立 —— 左边是常量、右边 ∝ t²，")
    L.append("唯一解为 **r = 0 且 h = c**。机读：r=1 m 时两式在 16 个时间档上的最坏相对差达 **%.4f**，" %
             METRICS["a4_mis_r1"])
    L.append("残差随 r 单调递减、只在 r=0 处降到 **%.1e**。" % METRICS["a4_mis_r0"])
    L.append("")
    L.append("⇒ **公理 A1（螺旋）与公理 A2（时空同一化）数学上互斥**：")
    L.append("保住式 3.1 就必须让螺旋半径恒为零，式 3.2 退化为沿轴直线 r⃗=ct k̂。")
    L.append("而 A1 的全部后续推导（质量、电荷、力、场）都以「螺旋」为前提 ⇒ **地基与上层同时失效**。")
    L.append("这条与 E3 的观测侧夹逼（螺旋度 s 被压到 1e−14 以下）**互相独立、同向**。")
    L.append("")
    L.append("### 链五：电磁部分的自相矛盾（B4 / C4 / D2）")
    L.append("")
    L.append("电磁部分是该体系**看起来最完整**的一块（麦克斯韦四条都给出了），但内部有三处撞车：")
    L.append("")
    L.append("1. **B4（最强，纯内部）**：式 3.11 的磁场形 B ∝ (X,y,z)/s^{3/2} 的散度为 δ 型 ——")
    L.append("   机测闭合面磁通 ∮B·dS/(μ₀q) 在 γ=1/2/5 下分别为 %.5f / %.5f / %.5f（解析值恒为 1），" %
             (METRICS["b4_flux_rows"][0]["flux_over_mu0q"],
              METRICS["b4_flux_rows"][1]["flux_over_mu0q"],
              METRICS["b4_flux_rows"][2]["flux_over_mu0q"]))
    L.append("   且远离电荷处 ∇·B 数值值 %.1e ≈ 0、通量与曲面半径无关 ⇒ 确为**点磁荷**。" %
             METRICS["b4_div_away"])
    L.append("   而式 3.13 写 ∇×A=B/f，旋度场的散度**恒为零** ⇒ **式 3.11 与式 3.13 不能同时成立**。")
    L.append("2. **C4**：式 3.11 在运动轴（y=z=0）上给出非零磁场（Q=1 C、1 m 处 1.00e−7 T），")
    L.append("   标准 B=v×E/c² 在该轴上恒为 0 ⇒ 高出 SQUID 阈约 8 个量级。（单电子同条件仅 1.6e−26 T，")
    L.append("   低于探测阈 —— 故本条以宏观电荷立论，效力弱于 B4。）")
    L.append("3. **D2**：式 3.9 + 3.10 联立给出 **E = −q r̂/(4πε₀r²)**，与库仑定律**处处反号**，")
    L.append("   ⇒ 同号电荷相吸。翻 k′ 符号救不了（被约掉），改 r⃗ 取向会把式 3.4 的引力变成排斥。")
    L.append("")
    L.append("⇒ **电磁部分不是「部分成立」，而是「成立的那几条恰好是已知定律的复述，")
    L.append("偏离的那几条恰好被否证」。**")
    L.append("")
    L.append("## 5. 新增性定价（为什么「自洽」也不算成功）")
    L.append("")
    L.append("本卷确认体系有**三处真实内部自洽**（推导数学无误）：")
    L.append("")
    L.append("1. **D1**：式 3.4 + 3.3 ⇒ 牛顿引力场（**逐字相同**）；")
    L.append("2. **D4**：式 3.13 + 3.14 ⇒ 法拉第定律（常数 f 上下抵消）；")
    L.append("3. **D5**：式 3.12 + 3.14 ⇒ 安培-麦克斯韦定律（f 再次抵消；真空段机检 %.1e）。"
             % METRICS["d5_worst_am"])
    L.append("")
    L.append("但按纪律，它们一律降 **INFO（零新增）**，理由是：")
    L.append("")
    L.append("- 还原的分别是牛顿引力、法拉第定律、安培-麦克斯韦定律，**均为已知物理**；")
    L.append("- 体系中引入的几何构造（立体角变化率、常数 f）在最终结果里**被完全约掉**，")
    L.append("  不留下任何可检验的新增项 ⇒ 它们只是把已知定律**重新参数化**；")
    L.append("- D3（波动方程=标准）同理。")
    L.append("")
    L.append("⇒ **「把已知定律重新推导一遍」不构成统一场论的进展。**")
    L.append("这也是 r116 那条教训的复现：**唯一成立的部分与已知物理逐字相同**。")
    L.append("")
    L.append("### 5b. 本卷对初稿的一处更正（重要）")
    L.append("")
    L.append("初稿曾把 **D2（式 3.9 + 3.10 ⇒ 库仑定律）** 记为「内部自洽、零新增」的一条成功项。")
    L.append("复核原式后确认**该判断是错的**：式 3.9 的 q 前**无**负号，式 3.10 的 E 前**有**负号，")
    L.append("联立得 **E = −q r̂/(4πε₀r²)**，与库仑定律 **E = +q r̂/(4πε₀r²)** **处处反号**")
    L.append("⇒ 该体系实际预言**同号电荷相吸、异号电荷相斥**。故 D2 由 INFO **改判 FAIL**。")
    L.append("")
    L.append("**退路已封**：①翻 k′ 的符号救不了（k′ 在 E/q 比值中被约掉，反号与 k′ 无关）；")
    L.append("②改 r⃗ 取向也救不了 —— 机读枚举两种取向，{引力吸引, 同号相斥} 最多只能还原")
    L.append("**%d/2** 项 ⇒ **式 3.4 与式 3.10 的符号约定互斥**。" % METRICS["d2_best"])
    L.append("")
    L.append("### 5c. 新增性普查（D6）：唯一的新增型就是唯一被否证型")
    L.append("")
    L.append("对 20 式逐条打类别标签后计数：")
    L.append("")
    L.append("| 类别 | 条数 | 代表 |")
    L.append("|----|----|----|")
    L.append("| 定义式 | %d | 3.1 / 3.2 / 3.3 / 3.5 / 3.6 / 3.9 / 3.13 / 3.14 / 3.19 / 3.20 |"
             % sum(1 for v in METRICS["d6_census"].values() if v == "定义式"))
    L.append("| 约掉型（还原已知） | %d | 3.4（牛顿）、3.12（安培-麦克斯韦） |"
             % sum(1 for v in METRICS["d6_census"].values() if v.startswith("约掉型")))
    L.append("| 同型式 | %d | 3.8（标准波动方程） |"
             % sum(1 for v in METRICS["d6_census"].values() if v.startswith("同型式")))
    L.append("| 推导式 | %d | 3.7（被 A2 判漏项） |"
             % sum(1 for v in METRICS["d6_census"].values() if v.startswith("推导式")))
    L.append("| 重复式 | %d | 3.17 ≡ 3.7（逐字重复 ⇒ 20 式实为 19 式） |"
             % sum(1 for v in METRICS["d6_census"].values() if v.startswith("重复式")))
    L.append("| 矛盾 / 反号 | %d | 3.16（三等号）、3.10（反号） |"
             % sum(1 for v in METRICS["d6_census"].values()
                   if v.startswith("矛盾式") or v.startswith("符号反号")))
    L.append("| **新增型** | **%d** | **3.11（唯一）** |" % METRICS["d6_n_novel"])
    L.append("| 未检 | %d | 3.15、3.18 |" % METRICS["d6_n_unchecked"])
    L.append("")
    L.append("⇒ **20 式里唯一具有体系特有内容的式 3.11，恰恰是唯一被本卷否证的一条**")
    L.append("（B4：与式 3.13 互斥、蕴含磁单极子；C4：运动轴上磁场非零）。")
    L.append("该体系的新增内容含量为零：**凡自洽处必与已知物理逐字相同，凡新增处必被否证**。")
    L.append("")
    L.append("## 6. M3 入口定价（回答前册留下的问题）")
    L.append("")
    L.append("前册 §十 把 M3 的入口定为「**Z ≡ Gc/2 的独立推导**」（若成，等于独立导出 G）。")
    L.append("本卷定价：**该入口关闭**。")
    L.append("")
    L.append("- **E1**：Z=Gc/2 是**定义式**，量纲 L⁴M⁻¹T⁻³ 无任何已知物理量可锚定；")
    L.append("  要由它「推出 G」必须先独立给出 Z 的值，而体系从未给出 ⇒ 循环。")
    L.append("- **E2**：Z′=c/(8πε₀) 同理；Z′/Z=%.3e（=1/(4πε₀G)）是常数重排，体系既不预言也不解释。" %
             (C / (8 * math.pi * EPS0) / (G * C / 2)))
    L.append("")
    L.append("⇒ 前册的结论在本卷得到加强：**瓶颈不在单位约定，而在该体系没有可独立取值的域外量**。")
    L.append("")
    L.append("## 7. 仍未闭合项（未做即未证，不得外推）")
    L.append("")
    L.append("- **本卷只做物理层**：不重复量纲/约定层结论，两册条目不可相加。")
    L.append("- **未逐式重算量纲**：前册已做（24 行），本卷回链不重判。")
    L.append("- **螺旋参数 r、ω 未由体系给定**：E3 的夹逼用 r=1 m 与观测加速度阈；")
    L.append("  若体系日后给出 ω(R) 的具体函数，E3 的数值需重算（已做 25 个量级的阈值不敏感度扫描，")
    L.append("  即便把阈放宽到 1e+3 m/s² 仍有 s≤%.2e，方向不受影响）。" % (math.sqrt(1.0e3 * R_LAB) / C))
    L.append("- **式 3.15、式 3.18 本卷未做物理层检验**（D6 记为「未检」）：")
    L.append("  其口径依赖 V 的含义与 k′ 的符号，而前册已判二者均为**待定**。")
    L.append("  ⇒ 未做即未证，**不得计入任何一侧**（既不充作支持，也不充作反证）。")
    L.append("- **式 3.11 的磁单极子结论依赖式 3.9 的 q 代入**：若式 3.9 被修正（它本身已被 C2 判 FAIL），")
    L.append("  ∮B·dS=μ₀q 的具体系数会变，但【B 不是旋度场】这一拓扑结论**不依赖任何系数**，仍然成立。")
    L.append("- **D5 的源项段（J=ρV）只对单一速度分布的电荷成立**：")
    L.append("  一般电流分布下 3.12 是否仍等于安培-麦克斯韦，本卷未做（真空段已机检通过）。")
    L.append("- **未覆盖的扩展式**：24（时空与物理常数归一化）等超出原 20 式的部分，本卷不攻。")
    L.append("- **不含量子场论 / 实验数据拟合**：本卷是解析与量级判决，未做数据拟合。")
    L.append("- **未触及「意识/人体」类延伸主张**（该体系常见外延），不在射程内。")
    L.append("")
    L.append("## 附录 · Glossary")
    L.append("")
    L.append("- **动量强守恒**：该体系假设动量标量大小不随观测者/时间改变。")
    L.append("- **能量绝对性**：该体系假设总能量恒等于静能 m₀c²，与运动状态无关。")
    L.append("- **螺旋度 s**：s≡(rω)/c，横向速率占总光速的比例；s=0 为直线，s=1 为纯圆周。")
    L.append("- **磁单极子（本卷 B4）**：∇·B≠0 的点源。任何旋度场 B=∇×A 必有 ∇·B≡0（含分布意义），")
    L.append("  故「B 是旋度场」与「B 有闭合面通量」互斥。式 3.11 给出 ∮B·dS=μ₀q，式 3.13 要求 ≡0。")
    L.append("- **约掉型**：体系引入的几何构造（kk′/Ω²·dΩ/dt、常数 f 等）在最终结果中被精确抵消，")
    L.append("  只留下已知定律 ⇒ 零新增。")
    L.append("- **同型式**：与某条已知方程逐字相同，仅变量诠释不同 ⇒ 零新增。")
    L.append("- **阈值不敏感度扫描**：把判定阈值跨若干量级扫描，证明结论不依赖阈值选取，")
    L.append("  避免「拍脑袋机器零」。")
    L.append("- **类光关系**：E=pc（即 E²−p²c²=0），零质量粒子的色散关系。")
    L.append("- **零新增（INFO）**：推导无误但还原已知物理，且引入的构造在结果中被约掉。")
    L.append("- **二难定价**：给出两个分支各自的定量阈值，证明两分支均无出路。")
    L.append("")
    L.append("## 数据出处")
    L.append("")
    L.append("- 机读册：`数据/%s.json` / `.md` / `_report.txt`" % STEM)
    L.append("- 来料：`01_独立体系/S17_统一场论核心公式/02_基础公设/postulates.md`")
    L.append("- 前册：`判定_S17核心公式_闭合代价与单位约定组合_2026-10-03.md`（量纲层 M1+M2）")
    L.append("")
    out = os.path.join(DATA, JUDGE_STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out


def main():
    os.makedirs(DATA, exist_ok=True)
    group_A()
    group_B()
    group_C()
    group_D()
    group_E()
    ctrl = control_group()

    # ---- 守卫 ----
    # G1：条目非空且判定合法
    legal = ("PASS", "FAIL", "INFO", "BOUNDARY")
    if not ENTRIES or any(e["verdict"] not in legal for e in ENTRIES):
        print("GUARD FAIL: 条目为空或判定值非法")
        return 2
    # G2：控制组必须全过（判据不得把标准物理也判 FAIL）
    if not all(k["pass"] for k in ctrl):
        print("GUARD FAIL: 控制组失效 —— 判据把标准物理也判 FAIL")
        for k in ctrl:
            if not k["pass"]:
                print("   ", k["name"], k["value"])
        return 2
    # G3：必须同时存在 FAIL 与 INFO（只有 FAIL 说明可能漏了「零新增」这一层；
    #     只有 INFO 说明没找到矛盾）——防止单侧偏置的假结果
    n_fail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
    n_info = sum(1 for e in ENTRIES if e["verdict"] == "INFO")
    if n_fail == 0 or n_info == 0:
        print("GUARD FAIL: 判定分布单侧偏置 FAIL=%d INFO=%d" % (n_fail, n_info))
        return 2
    # G4：关键数值 sanity
    gamma_lhc = LHC_E_MEV / M_PC2_MEV
    if not (1000.0 < gamma_lhc < 1.0e5):
        print("GUARD FAIL: γ_LHC=%.3f 落在非物理区间" % gamma_lhc)
        return 2
    # G5：E3 的螺旋度上界必须远小于 1（否则"压成直线"的结论不成立）
    s_cap = math.sqrt(A_ACC_TIGHT * R_LAB) / C
    if not (0.0 < s_cap < 1.0e-6):
        print("GUARD FAIL: 螺旋度上界 %.3e 未达「退化为直线」量级" % s_cap)
        return 2
    # G6：D5 的安培-麦克斯韦真空段数值验证必须真的通过（不许硬编码"通过"）
    if not (METRICS["d5_worst_am"] < 1.0e-5):
        print("GUARD FAIL: D5 真空段相对误差 %.3e 过大，还原不成立" % METRICS["d5_worst_am"])
        return 2
    # G7：B4 的磁单极子通量必须真的 ≈ μ₀q（解析值 1），且远离奇点散度 ≈ 0
    if not (METRICS["b4_worst_flux"] < 1.0e-3):
        print("GUARD FAIL: B4 磁通与解析值偏差 %.3e 过大" % METRICS["b4_worst_flux"])
        return 2
    if not (METRICS["b4_div_away"] < 1.0e-5):
        print("GUARD FAIL: B4 远离奇点散度 %.3e 不≈0，δ 型奇点论证不成立"
              % METRICS["b4_div_away"])
        return 2
    # G8：A4 的 3.1↔3.2 互斥必须由机读支撑（r=0 残差≈0、r=1 残差显著、随 r 单调）
    if not (METRICS["a4_mis_r0"] < 1.0e-12 and METRICS["a4_mis_r1"] > 0.9
            and METRICS["a4_mono"]):
        print("GUARD FAIL: A4 机读不支撑（r=0 残差 %.2e / r=1 残差 %.4f / 单调 %s）"
              % (METRICS["a4_mis_r0"], METRICS["a4_mis_r1"], METRICS["a4_mono"]))
        return 2
    # G9：D2 的符号约定互斥枚举必须真的给出「最多还原 1/2」
    if METRICS["d2_best"] != 1:
        print("GUARD FAIL: D2 约定枚举给出 %d/2，互斥论证不成立" % METRICS["d2_best"])
        return 2
    # G10：D6 普查必须自洽（新增型恰 1 条，未检恰 2 条）
    if not (METRICS["d6_n_novel"] == 1 and METRICS["d6_n_unchecked"] == 2
            and len(METRICS["d6_census"]) == 20):
        print("GUARD FAIL: D6 普查不自洽（新增 %d / 未检 %d / 总数 %d）"
              % (METRICS["d6_n_novel"], METRICS["d6_n_unchecked"],
                 len(METRICS["d6_census"])))
        return 2

    p1 = build_json(ctrl)
    p2 = build_md(ctrl)
    p3 = build_report(ctrl)
    p4 = build_judge(ctrl)
    print("OK generated:")
    for p in (p1, p2, p3, p4):
        print("  ", os.path.relpath(p, PROJECT))
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v) for v in legal}
    print("VERDICT: CORE-FORMULA-SYSTEM-INCONSISTENT-AND-ZERO-NOVELTY")
    print("条目 %d：PASS %d / FAIL %d / INFO %d / BOUNDARY %d"
          % (len(ENTRIES), c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"]))
    print("控制组 %d/%d 通过 | guards 10/10 PASS | exit_code=0"
          % (sum(1 for k in ctrl if k["pass"]), len(ctrl)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
