# -*- coding: utf-8 -*-
"""
================================================================================
TUFT 前置 D2：挠率动力学项 —— 构造候选、健康性检验与 F1 可执行性终判
================================================================================
承接：
  - `tuft_r6_report.txt`（R6 阶段0）：挠率产生三路径全受阻（EC 自然源差 1.37e28；
    谐振需 Q~1e28；新耦合被自旋/EP 实验排除）。
  - `tuft_Q量子A_report.txt`（前置 A）：W=(1/8π²)∫T∧T 非拓扑荷；半整由 Tw 承载。
  - `tuft_O_SCALE_锚定方案_report.txt`：最小锚定定理（秩=1，绝对尺度须外部锚定），
    方案 A2 给出 L = 1.4406e8 l_P = 2.328e-27 m（唯一「半内」锚定）。
  - `tuft_范式哲学重构.md` §十二：挠率动力学项是「卡面最大」的前置（同时阻塞
    T1′/T3/T8/T9/F1/F5）。

本册回答四问：
  §1 量纲桥接：挠率的两种口径（1/m 与 1/s）是否自洽？R6 的换算是否成立？
  §2 EC 中挠率为何是代数约束（不传播）—— 符号层复现（含变分演示）
  §3 四类动力学项候选：传播性 / 无鬼 / 无 tachyon / 自由度（sympy 变分 + 计数）
  §4 尺度困境定理：动力学化后的挠率若要「承载粒子」与「宏观可探测」是否可兼容？
  §5 F1/F5 可执行性终判 + 对 T1′/T3/T8/T9 的连锁判定

红线：数学自洽 != 物理实验证实。本册只做量纲、量级与结构判定，不主张 TUFT 真伪。
================================================================================
"""
from __future__ import print_function

import os
import sys
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

try:
    import numpy as np
except Exception:
    np = None

try:
    import sympy as sp
    from sympy import symbols, Function, Rational
    from sympy.calculus.euler import euler_equations
    HAVE_SYMPY = True
except Exception:
    HAVE_SYMPY = False

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_D2_report.txt")

# ---------------------------- 常数（CODATA 2018） ----------------------------
C = 2.99792458e8          # m/s
G = 6.67430e-11           # m^3 kg^-1 s^-2
HBAR = 1.054571817e-34    # J s
EV = 1.602176634e-19      # J
LP = 1.616255e-35         # m   普朗克长度
MP = 2.176434e-8          # kg  普朗克质量

# O-SCALE 方案 A2（唯一「半内」锚定）
L_A2_IN_LP = 1.4406e8
L_A2 = L_A2_IN_LP * LP          # m

# R6 既有结论（引用，不重算）
T_TARGET_SI = 1.0e-4            # s^-1  R5/R6 的探测目标挠率强度
T_EC_NATURAL_SI = 7.32e-33      # s^-1  R6：EC 自然耦合下实验室挠率
R6_GAP = 1.37e28                # 倍数  R6：目标/自然的缺口
R6_Q_REQUIRED = 1.0e28          # R6：谐振放大所需 Q
R6_Q_BEST = 1.0e15              # R6：现有最佳 Q

# 实验室探测尺度（R5 装置量级）
R_LAB = 0.1                     # m


class Report(object):
    def __init__(self):
        self.rows = []
        self.lines = []

    def echo(self, t=""):
        print(t)
        self.lines.append(t)

    def section(self, t):
        self.echo("")
        self.echo("=" * 78)
        self.echo(t)
        self.echo("=" * 78)

    def add(self, sid, name, verdict, detail=""):
        # verdict 显式传入 "PASS" / "FAIL" / "BOUNDARY"。
        # 口径（与 R6 一致）：方法/结构校验正确 ⇒ PASS；
        #                     「TUFT 目标不可达成」被证实 ⇒ FAIL（诚实负结论）。
        if isinstance(verdict, bool):
            verdict = "PASS" if verdict else "FAIL"
        self.rows.append((sid, name, verdict, detail))
        line = "  [%s] %s" % (verdict, name)
        if detail:
            line += "   |  " + detail
        self.echo(line)

    def info(self, sid, name, detail=""):
        self.rows.append((sid, name, "INFO", detail))
        line = "  [INFO] %s" % name
        if detail:
            line += "   |  " + detail
        self.echo(line)

    def summary(self):
        from collections import Counter
        cnt = Counter(r[2] for r in self.rows)
        self.echo("")
        self.echo("=" * 78)
        self.echo("汇总")
        self.echo("=" * 78)
        for k in ("PASS", "FAIL", "BOUNDARY", "INFO"):
            self.echo("  %-9s = %d" % (k, cnt.get(k, 0)))
        fails = [r for r in self.rows if r[2] == "FAIL"]
        if fails:
            self.echo("  存在 FAIL（真实缺陷）:")
            for r in fails:
                self.echo("    - [%s] %s" % (r[0], r[1]))
        return cnt


R = Report()


def fmt(x, n=4):
    if x is None:
        return "n/a"
    if isinstance(x, str):
        return x
    if x == 0:
        return "0"
    a = abs(x)
    if a >= 1e5 or a < 1e-4:
        return "%.*e" % (n - 1, x)
    return "%.*f" % (n, x)


# ==============================================================================
# §1 量纲桥接审计
# ==============================================================================
def sec1():
    R.section("§1 量纲桥接审计：挠率的两种口径（m^-1 与 s^-1）")

    # 挠率分量 T^λ_{μν} 是联络系数之差 ⇒ 量纲 1/L；自旋-挠率耦合中常写作频率
    R.info("D2-1.0", "挠率分量的量纲",
           "T^λ_{μν} = Γ^λ_{μν} − Γ^λ_{νμ}（联络差）⇒ [T] = 1/m；"
           "R5/R6 用 s^-1 口径，二者桥接为 T[s^-1] = c · T[m^-1]")

    # R6 数值的桥接复核
    t_m_inv = T_EC_NATURAL_SI / C
    t_target_m_inv = T_TARGET_SI / C
    R.info("D2-1.1", "R6 数值口径复核",
           "R6：EC 自然源 7.32e-33 s^-1 ⇒ 2.44e-41 m^-1；目标 1e-4 s^-1 ⇒ 3.33e-13 m^-1；"
           "实测换算 T_m = %s m^-1 / T_target_m = %s m^-1" % (fmt(t_m_inv), fmt(t_target_m_inv)))

    # 与 R6 记录的 2.44e-41 是否一致
    ref = 2.44e-41
    rel = abs(t_m_inv - ref) / ref
    ok = rel < 0.01
    R.add("D2-1.2", "R6 的 s^-1 → m^-1 换算自洽", ok,
          "本册换算 %s m^-1 vs R6 记录 2.44e-41 m^-1，相对偏差 %s" % (fmt(t_m_inv), fmt(rel)))

    # EC 源方程量纲：T = (8πG/c^3) · s_spin
    # [G/c^3] = s/kg ；[s_spin] = 角动量/体积 = kg/(m·s) ⇒ [乘积] = 1/m  ✓
    R.info("D2-1.3", "EC 源方程量纲闭合",
           "T = (8πG/c³)·s_spin：[G/c³]=s/kg，[s_spin]=kg/(m·s) ⇒ [T]=1/m ✓ "
           "（该式是 §4 传播解的源项基准）")
    return t_m_inv


# ==============================================================================
# §2 EC 中挠率为何不传播（符号复现）
# ==============================================================================
def sec2():
    R.section("§2 EC 理论中挠率为何是代数约束（不传播）")

    if not HAVE_SYMPY:
        R.add("D2-2.0", "sympy 不可用，跳过符号变分", "BOUNDARY", "降级为解析论述")
    else:
        t, x, m = symbols("t x m")
        phi = Function("phi")(t, x)

        # L_A：标准二阶（传播）
        LA = (Rational(1, 2) * sp.diff(phi, t) ** 2
              - Rational(1, 2) * sp.diff(phi, x) ** 2
              - Rational(1, 2) * m ** 2 * phi ** 2)
        eA = euler_equations(LA, phi, [t, x])[0]
        has2_A = eA.has(sp.diff(phi, t, 2)) or eA.has(sp.diff(phi, x, 2))
        R.add("D2-2.1", "含 (∂φ)² 的标准拉氏量 ⇒ EOM 含二阶导数（可传播）",
              bool(has2_A), "EOM: %s" % sp.simplify(eA.lhs - eA.rhs))

        # L_B：纯质量/代数（EC 挠率的结构类比：K 只以代数二次型出现）
        LB = -Rational(1, 2) * m ** 2 * phi ** 2
        eB = euler_equations(LB, phi, [t, x])[0]
        has2_B = eB.has(sp.diff(phi, t, 2)) or eB.has(sp.diff(phi, x, 2))
        R.add("D2-2.2", "无导数项的拉氏量 ⇒ EOM 为代数方程（不传播）",
              bool(not has2_B), "EOM: %s  ← 这正是 EC 中 K(挠率) 的结构" % sp.simplify(eB.lhs - eB.rhs))

        # L_C：含 (□φ)² ⇒ 四阶 ⇒ Ostrogradsky 鬼
        box = sp.diff(phi, t, 2) - sp.diff(phi, x, 2)
        LC = Rational(1, 2) * box ** 2
        eC = euler_equations(LC, phi, [t, x])[0]
        has4_C = eC.has(sp.diff(phi, t, 4)) or eC.has(sp.diff(phi, x, 4))
        R.add("D2-2.3", "含 (□φ)² 的拉氏量 ⇒ EOM 四阶（Ostrogradsky 鬼）",
              bool(has4_C), "EOM 最高阶 = 4 ⇒ 额外自由度带负能量，须排除")

    R.info("D2-2.4", "EC 不传播的解析根因",
           "一阶（Palatini）形式中 R = dω + ω∧ω；用 T = de + ω∧e 反解 ω = ω_LC + K（K 为 contortion，"
           "与 T 代数线性相关）后，作用量中 K 只以 K² 代数项出现（∇K 项分部积分后化为边界/含 T 的代数项）"
           "⇒ δS/δK = 0 是**代数**方程 K ∝ 自旋流，不含 ∂²K/∂t² ⇒ 无色散关系、无本征模、无传播。"
           "与 §2.2 的代数 EOM 结构一致，并与 R6「EC 挠率不传播」互为印证。")


# ==============================================================================
# §3 动力学项候选与健康性
# ==============================================================================
def sec3():
    R.section("§3 挠率动力学项候选：传播性 / 无鬼 / 无 tachyon / 自由度")

    # 候选表（结构判定 + 数值/符号支撑）
    cands = [
        ("C1 纯质量项  a·T²",
         "不传播", "无导数 ⇒ 代数约束（§2.2 结构）", "0 DOF（代数）", "FAIL 作为动力学项"),
        ("C2 Proca 型  −¼ S² + ½ m_T² T²  (S = dT)",
         "传播", "二阶 EOM，无高阶导数 ⇒ 无 Ostrogradsky 鬼", "3 DOF（有质量矢量）", "唯一健康候选"),
        ("C3 一般 (∂T)² 未调谐",
         "传播", "含 (∂·T)² 未调谐项 ⇒ 额外的鬼态自由度", "3 + 鬼 DOF", "FAIL（须 Fierz–Pauli 调谐）"),
        ("C4 高阶 (∂²T)² / f(R,T) 型",
         "传播", "四阶 EOM（§2.3）⇒ Ostrogradsky 鬼", "含负能量 DOF", "FAIL"),
    ]
    for name, prop, ghost, dof, verdict in cands:
        R.info("D2-3.x", name, "传播=%s；鬼=%s；自由度=%s；判定=%s" % (prop, ghost, dof, verdict))

    R.add("D2-3.1", "C2（Proca 型）是唯一通过「传播 + 无鬼」双检的候选", "PASS",
          "需满足：① 场方程二阶；② 质量项取 −¼S²+½m²T² 的 Proca 调谐；③ m_T² > 0（无 tachyon）")

    # Nieh-Yan 项：与前置 A（T3）的接口
    R.info("D2-3.2", "Nieh–Yan 项（T³∧T − R∧e∧e）与拓扑荷的接口",
           "前置 A 已证 ∫T∧T 非拓扑；标准 NY 4-形式是 T^a∧T_a − R_ab∧e^a∧e^b，"
           "其积分为 NY 类（整）。但 NY 项**不含导数** ⇒ 只能充当拓扑项，**不能提供动力学**。"
           "⇒ 拓扑荷（T3）与挠率动力学（T1′）需要两个不同结构，TUFT 目前两者皆缺。"
           "本册未对 NY 做整性实跑（需紧致流形积分），按 INFO 处理。")

    R.add("D2-3.3", "动力学化不解决「∫T∧T 非拓扑」", "FAIL",
          "即使引入 C2 使挠率传播，∫T∧T 仍在 λ 缩放下按 λ² 漂移（前置 A §2）⇒ 拓扑荷问题独立存在")


# ==============================================================================
# §4 尺度困境定理（本册核心）
# ==============================================================================
def sec4():
    R.section("§4 尺度困境定理：动力学化后的挠率无法同时「承载粒子」与「宏观可探测」")

    R.info("D2-4.0", "输入（引用，不重算）",
           "O-SCALE 方案 A2（唯一半内锚定）：L = %s l_P = %s m；"
           "R6：EC 自然源 %s s^-1，目标 %s s^-1，缺口 %s 倍"
           % (fmt(L_A2_IN_LP), fmt(L_A2), fmt(T_EC_NATURAL_SI), fmt(T_TARGET_SI), fmt(R6_GAP)))

    # (1) 若挠率元胞尺度 = L_A2 ⇒ 其 Compton 波长 λ = L_A2 ⇒ 质量与量子能量
    m_T = HBAR / (L_A2 * C)                 # kg
    E_q = m_T * C ** 2                      # J
    E_q_eV = E_q / EV
    R.info("D2-4.1", "由尺度锚定反推挠率量子",
           "λ = L = %s m ⇒ m_T = ħ/(λc) = %s kg；单量子能量 E = m_T c² = %s J = %s eV = %s GeV"
           % (fmt(L_A2), fmt(m_T), fmt(E_q), fmt(E_q_eV), fmt(E_q_eV / 1e9)))

    # (2) 宏观可探测的必要条件：Yukawa 力程 λ ≳ 实验室尺度
    m_max = HBAR / (R_LAB * C)
    E_max = m_max * C ** 2 / EV
    R.info("D2-4.2", "宏观可探测的必要条件",
           "有质量场在距离 r 处按 exp(−r/λ) 衰减；要在 r_lab = %s m 处不被压制，需 λ ≳ r_lab "
           "⇒ m_T ≤ ħ/(r_lab·c) = %s kg ⇒ E ≤ %s eV" % (fmt(R_LAB), fmt(m_max), fmt(E_max)))

    # (3) 冲突倍数
    ratio = E_q_eV / E_max
    R.add("D2-4.3", "尺度困境（核心负结论）：承载粒子所需质量 与 宏观可探测上限 冲突",
          "FAIL" if ratio > 1e3 else "BOUNDARY",
          "E_req/E_allow = %s 倍（%s eV vs %s eV）⇒ 二者相差约 %d 个数量级，不可兼得"
          % (fmt(ratio), fmt(E_q_eV), fmt(E_max), int(round(math.log10(ratio)))))

    # (4) 若坚持尺度锚定 ⇒ 宏观抑制因子
    supp = math.exp(-R_LAB / L_A2) if R_LAB / L_A2 < 700 else 0.0
    R.add("D2-4.4", "坚持尺度锚定 ⇒ 实验室尺度处挠率被 Yukawa 完全压制", "FAIL",
          "exp(−r_lab/λ) = exp(−%s) ⇒ 实际为 0（log10 ≈ −%.1f）"
          % (fmt(R_LAB / L_A2), R_LAB / L_A2 / math.log(10)))

    # (5) 扫描表
    R.echo("")
    R.echo("  λ(力程) 扫描：m_T 与宏观抑制因子 exp(−r_lab/λ)")
    R.echo("  %-12s %-14s %-16s %-22s" % ("λ [m]", "m_T [kg]", "E=m_Tc² [eV]", "exp(−0.1/λ)"))
    for lam in (1e-30, 1e-27, 1e-18, 1e-15, 1e-10, 1e-6, 1e-3, 1e-1, 1.0, 1e3):
        mm = HBAR / (lam * C)
        ee = mm * C ** 2 / EV
        e = math.exp(-R_LAB / lam) if R_LAB / lam < 700 else 0.0
        R.echo("  %-12s %-14s %-16s %-22s"
               % (fmt(lam), fmt(mm), fmt(ee), (fmt(e) if e > 0 else "0（完全压制）")))
    R.info("D2-4.5", "扫描读法",
           "λ ≲ 1e-3 m 的档位在 r=0.1 m 处全部被压制为 0；只有 λ ≳ 0.1 m（m_T ≲ %s eV）才有宏观场。"
           "而 TUFT 自身的粒子尺度锚定落在 λ ~ 1e-27 m 档 ⇒ 与宏观探测互斥。" % fmt(E_max))

    # (6) 无质量极限：回到 R6 结论
    R.add("D2-4.6", "λ→∞（无质量挠率）并不改善：退回 R6 的自然源缺口", "FAIL",
          "无质量时无 Yukawa 抑制，但源强度仍由 EC 代数约束给出 T_nat = %s s^-1，"
          "距目标 %s 倍（R6）；桥接该缺口的新耦合已被自旋/等效原理实验排除（R6）"
          % (fmt(T_EC_NATURAL_SI), fmt(R6_GAP)))

    # (7) 谐振放大路径的复核（引用 R6）
    R.add("D2-4.7", "谐振放大路径：动力学化后仍不可行", "FAIL",
          "即便 C2 使挠率有本征模，所需 Q ≈ %s ≫ 现有最佳 %s（差 %s 倍）；"
          "且动力学质量越大，模的激发能量越高（E ∝ 1/λ）⇒ 与 §4.1 同向恶化"
          % (fmt(R6_Q_REQUIRED), fmt(R6_Q_BEST), fmt(R6_Q_REQUIRED / R6_Q_BEST)))

    return ratio


# ==============================================================================
# §5 可执行性终判与连锁
# ==============================================================================
def sec5(ratio):
    R.section("§5 F1/F5 可执行性终判 + 对范式主张的连锁判定")

    R.add("D2-5.1", "F1（地面挠率探测 T>1e-3 s^-1 无信号即证伪）—— 判为不可执行", "FAIL",
          "三条动力学路径全部关闭：① 有质量（TUFT 尺度锚定）⇒ Yukawa 压制；"
          "② 无质量 ⇒ 缺口 1.37e28 且新耦合被排除；③ 谐振 ⇒ 需 Q~1e28 ≫ 1e15。"
          "⇒ F1 在 TUFT 内部实际**预期无信号**，其『被满足』不构成证伪、也不构成支持")

    R.add("D2-5.2", "F1 的性质变更：从『证伪通道』退化为『自洽推论』", "FAIL",
          "若 TUFT 尺度锚定成立，则地面无挠率信号是 TUFT 的**预测**而非反例；"
          "用它作首要证伪通道属判据错置（呼应 范式哲学重构 §6.2）")

    R.add("D2-5.3", "F5（等效原理自旋相关差异）—— 与 F1 同源，同样不可执行", "FAIL",
          "F5 依赖同一自旋-挠率耦合强度，受 §4 同一压制 ⇒ 同步失效")

    R.info("D2-5.4", "对范式主张的连锁（范式哲学重构 §三 编号）",
           "T1′（挠率是动力学自由度）→ 需 C2 且须放弃尺度锚定或放弃宏观可探测，二选一；"
           "T3（拓扑荷）→ 动力学化不修复（§3.3）；"
           "T8（黑洞信息）→ 承载分支已被 46.82% 排除 + T3 未修复，维持冻结；"
           "T9（纠缠=拓扑投影）→ 无拓扑扇区，维持冻结")

    R.add("D2-5.5", "挠率动力学化不能救 F1，反而新增一个内在冲突", "FAIL",
          "『挠率元胞 = 粒子（尺度 ~1e-27 m）』与『挠率可地面探测（λ ≳ 0.1 m）』"
          "相差 ~%d 个数量级 ⇒ 二难：保留其一必须放弃另一" % int(round(math.log10(ratio))))

    R.info("D2-5.6", "若要保留宏观可探测性的唯一出路（代价登记）",
           "把挠率质量 m_T 作为**独立自由参数**与粒子尺度 L 解耦（m_T ≲ %s eV），"
           "代价：① 挠率不再承载粒子结构，T1′ 的本体论动机落空；"
           "② 多一个自由参数，保护带增厚（反驳 范式哲学重构 §七 的奥卡姆主张）；"
           "③ 仍需解释自旋-挠率耦合为何不被 EP 实验排除（R6 第三条）"
           % fmt(HBAR / (R_LAB * C) * C ** 2 / EV))


# ==============================================================================
# §6 诚实边界
# ==============================================================================
def sec6():
    R.section("§6 诚实边界（必读）")
    R.info("D2-6.1", "本册 PASS 的性质",
           "均为标准场论/量纲分析的数值确认（传播性 = EOM 含二阶导数、Yukawa 衰减、"
           "Compton 关系），**不构成 TUFT 的独立证据**。")
    R.info("D2-6.2", "依赖的外部结论",
           "R6 的三路径受阻、O-SCALE 的 A2 尺度锚定、R5 的探测目标 1e-4 s^-1、"
           "前置 A 的 ∫T∧T 非拓扑 —— 均为既有报告结论，本册引用不重算；若其被推翻，"
           "§4/§5 的结论需同步重估。")
    R.info("D2-6.3", "未做的工作",
           "① 未对完整 EC+C2 作用量做扰动谱分析（只做结构判定）；"
           "② NY 项整性未实跑；③ 未构造 Lk̂/Tŵ 的场论算符（前置 A A7.3 待证项）；"
           "④ 未做挠率-物质耦合的实验上限重算（引用 R6）。")
    R.info("D2-6.4", "红线",
           "数学自洽 != 物理实验证实。本册结论为**内部一致性判定**，"
           "不构成对 TUFT 物理真实性或伪的断言。")


def main():
    R.section("TUFT 前置 D2：挠率动力学项 —— 构造候选、健康性检验与 F1 可执行性终判")
    R.echo("  承接：R6（产生三路径受阻）· 前置 A（W 非拓扑）· O-SCALE（尺度须外部锚定）· 范式哲学重构 §十二")
    R.echo("  红线：数学自洽 != 物理实验证实。")

    sec1()
    sec2()
    sec3()
    ratio = sec4()
    sec5(ratio)
    sec6()

    cnt = R.summary()

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(R.lines))
    print("\n报告已写入: %s" % REPORT_PATH)
    return cnt


if __name__ == "__main__":
    main()
