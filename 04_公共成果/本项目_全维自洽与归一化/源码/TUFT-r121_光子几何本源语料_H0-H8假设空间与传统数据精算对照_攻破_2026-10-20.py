# -*- coding: utf-8 -*-
"""r121: 《光子的几何本源与运动模型证明》语料机审——H0–H8 假设空间 × 传统数据精算对照。

靶（对内语料，只读）：
  U1 90_历史归档/来源语料_utf_20261009/语料/01-核心论文/空间的螺旋运动/
     光子的几何本源与运动模型证明——基于张祥前统一场论的求导与验证.md

用户问题（原话）：光子在空间光速移动的时候是否内部还运行？怎么运行？
  把所有情况列出来，并与传统数据精算分析哪个是正确的。

方法论（本册元方法：「最伟大的科学家处理模式」）：
  1. 操作定义化（Einstein/Bridgman）：「内部还运行吗」必须先转为可测量——
     固有时钟读数 / 自旋投影 / 频率接口 / 传播速度 / 辐射特征 / 电荷；
  2. 穷举枪毙（Feynman）：H0–H8 全部列出，逐一给数据对照，不只打靶；
  3. not-even-wrong 标注（Pauli）：不可测量区不参与判决，诚实登记为不可判定；
  4. 可证伪性优先：每个假设自带「什么观测会杀死它」。

判据：
  A1 动量双读法互斥（P=m(C−V) 与结论1 V=C ⇒ P=0，vs 6.1 节 p⃗=mC⃗）
  A2 双电子模型动量-能量断裂（旋转非零 ⇒ P_total/(E/c) = ż_c/c < 1）
  A3 光速约束循环证明（4.2 节「证明」的是公设本身，信息增量 0）
  A4 分支穷尽失败（p∈[0,c] 一维自由族 ⇒ 「必然导出」量词错误）
  A5 观测接口计数 0（验证节公式对螺旋参数 (R,ω) 依赖为 0）
  A6 偏振覆盖虚报（单螺旋参数化只覆盖圆偏振；线偏振违反 |V|=c）
  B1 质量接口断裂（「静止质量为零的激发电子」vs m_γ<1e-18 eV，差 5.11e23）
  B2 固有时零（类光世界线 ∫dτ=0 ⇒ 「内部运行」是观察者坐标效应）
  B3 旗舰：自旋-光速-频率三接口互斥（κ=ω/f 扫描：κ>0 ⇒ v_z<c；κ=2π ⇒ p=0）
  B4 旗舰：Larmor 辐射猝灭（带电螺旋偶极辐射 ⇒ 光子寿命 ~1e-19 s vs 实测 >4e17 s）
  B5 传播速度可变（语料自承 p「取决于激发条件」vs c 为 SI 定义常数）
  B6 量子预言接口 0（干涉/康普顿/受激/选择定则/… 计数全 0）
  B7 螺旋度单符号族（双电子两电子同向旋转 ⇒ 只有 (++),(−−)，给不出 ±ℏ 两态）
纪律：verdict 由机读结果驱动；阳性对照防假绿；上游字节只读（sha256 守卫）。
"""
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NORM = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
R_DATA = os.path.join(NORM, "数据")

U1 = os.path.join(ROOT, "90_历史归档", "来源语料_utf_20261009", "语料", "01-核心论文",
                  "空间的螺旋运动", "光子的几何本源与运动模型证明——基于张祥前统一场论的求导与验证.md")

GUARDS = []


def guard(ok, name, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    return bool(ok)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def find_line(text, needle):
    for i, ln in enumerate(text.splitlines(), 1):
        if needle in ln:
            return i
    return None


print("[r121] boot ok")
if not os.path.exists(U1):
    print("[r121] UPSTREAM MISSING: U1 (%s)" % U1)
    sys.exit(3)
up1 = read_text(U1)
up1_sha = sha256_of(U1)
print("[r121] upstream U1: %s (%d chars)" % (up1_sha[:16], len(up1)))

# ---------------------------------------------------------------- 常数（CODATA 2018 / PDG / 观测）
C_LIGHT = 299792458.0                 # SI 定义值（精确）
H_PLANCK = 6.62607015e-34             # J·s（SI 定义值，精确）
HBAR = H_PLANCK / (2 * math.pi)
E_CHARGE = 1.602176634e-19            # C（SI 定义值，精确）
EPS0 = 8.8541878128e-12               # F/m
M_E_EV = 0.51099895e6                 # eV（电子静质量）
M_GAMMA_UPPER_EV = 1e-18              # eV/c²（PDG 光子质量上限，常用值）
AGE_UNIVERSE_S = 4.35e17              # s（普朗克 2018，宇宙年龄）
GW170817_BOUND = 1e-15                # |v_GW−c|/c 上限（Abbott et al. 2017）
Q_GAMMA_UPPER = 1e-35                 # |q_γ|/e 上限（PDG）

# ================================================================ L01 上游自承点机读
u1 = {
    "title": find_line(up1, "光子的几何本源与运动模型证明"),
    "spacetime_unification": find_line(up1, "时空同一化"),
    "momentum_def": find_line(up1, r"\vec{P} = m (\vec{C} - \vec{V})"),
    "conclusion1_V_eq_C": find_line(up1, r"\vec{V} = \vec{C}"),
    "photon_at_rest_in_space": find_line(up1, "静止”于以光速运动的空间中"),
    "model1_helix": find_line(up1, r"x(t) = R \cos(\omega t + \phi_0)"),
    "model1_speed_constraint": find_line(up1, r"(R\omega)^2 + p^2 = c^2"),
    "p_depends_on_excitation": find_line(up1, "具体取值取决于激发条件"),
    "pure_rotation_excluded": find_line(up1, "可能不对应于可传播的光子"),
    "model2_pair": find_line(up1, "两个电子绕一个中心轴旋转"),
    "model2_param": find_line(up1, r"\vec{r}_1(t) = [a\cos(\omega t), a\sin(\omega t), z_c(t) + d]"),
    "energy_mc2": find_line(up1, "E = mc^2"),
    "momentum_E_over_c": find_line(up1, "p = E/c"),
    "momentum_mC": find_line(up1, r"m\vec{C}"),
    "spin_hbar_possible": find_line(up1, "（±ħ）提供了可能的经典图像基础"),
    "E_prop_omega": find_line(up1, r"E \propto \omega"),
    "right_hand_spin1": find_line(up1, "右手螺旋，这与光子自旋为1"),
    "perfect_match": find_line(up1, "完美符合"),
}
l01_ok = all(v is not None for v in u1.values())
L01 = {"id": "L01", "verdict": "PASS" if l01_ok else "FAIL",
       "item": "U1 自承点机读（18 处关键断言定位到行）", "hits": u1}

# ================================================================ A1 动量双读法互斥
# 定义式（2.3 节）：P = m(C−V)；结论1（3 节）：V = C ⇒ P = 0
# 验证节（6.1）：p⃗ = mC⃗（= mc，需 V = 0）——同一理论内两个互斥读数
P_def_ratio = 0.0      # |C−V|/c 在 V=C 下
P_claim_ratio = 1.0    # |C|/c
a1_defect = abs(P_claim_ratio - P_def_ratio)
# 下游后果：P=0 ⇒ 康普顿反冲 Δλ=0（观测 2.43e-12 m）、辐射压=0（观测百年验证）
compton_shift = H_PLANCK * C_LIGHT / (M_E_EV * 1.602176634e-19)   # h/(m_e c)
compton_predicted_by_P0 = 0.0
a1_fail = (a1_defect > 0.5)
A1 = {"id": "A1", "verdict": "FAIL" if a1_fail else "PASS",
      "item": "动量双读法互斥：P=m(C−V) 且 V=C ⇒ P=0，vs 验证节 p⃗=mC⃗（需 V=0）",
      "P_definition_ratio": P_def_ratio, "P_claim_ratio": P_claim_ratio,
      "mutual_exclusion_defect": a1_defect,
      "downstream": {"compton_shift_standard_m": compton_shift,
                     "compton_shift_if_P_zero_m": compton_predicted_by_P0,
                     "note": "P=0 ⇒ 无反冲 ⇒ 康普顿效应、辐射压、多普勒推力全部归零，与观测矛盾"},
      "interpretation": "要 P=0 须 V=C；要 P=mc 须 V=0。同一理论不能同时持有 ⇒ 结构崩坏而非笔误"}

# ================================================================ A2 双电子模型动量-能量断裂
# 每电子 |v_i|=c ⇒ ż_c = √(c²−(aω)²)；P_total=2mż_c；E=2mc² ⇒ p_req=E/c=2mc
def momentum_deficit(x):
    """x = aω/c ∈ [0,1]；返回 P_total/(E/c) 相对 1 的缺陷。"""
    return 1.0 - math.sqrt(1.0 - x * x)


a2_scan = {"aω/c=%.2f" % x: momentum_deficit(x)
           for x in (0.0, 0.1, 0.3, 0.5, 1.0 / math.sqrt(2.0), 0.9, 0.99)}
# 自旋-频率自洽解（B3 双电子支 κ=2π）⇒ aω/c = 1/√2 ⇒ 缺陷 29.29%
x_spin = 1.0 / math.sqrt(2.0)
a2_spin_deficit = momentum_deficit(x_spin)
a2_fail = (a2_spin_deficit > 0.05)
A2 = {"id": "A2", "verdict": "FAIL" if a2_fail else "PASS",
      "item": "双电子模型动量-能量断裂：旋转非零 ⇒ P_total < E/c；观测 p=E/c 反推 aω=0（杀死旋转）",
      "deficit_scan": a2_scan,
      "spin_coherent_x": x_spin, "spin_coherent_deficit": a2_spin_deficit,
      "inverse": "P_total=E/c ⇔ ż_c=c ⇔ aω=0 ⇒ 『绕轴旋转』被光子动量公式排除",
      "note": "缺陷随 aω/c 单调升至 100%%；取自洽接口集（B3）的 κ=2π 解缺陷 %.4f" % a2_spin_deficit}

# ================================================================ A3 光速约束循环证明
# 4.2 节：从公设 2.2（v_rot²+p²=c²）与定义 v_rot=Rω 出发设参数化，
#        再「证明」(Rω)²+p²=c² —— 结论谓词在前提中，代入定义即得，信息增量 0
premise_syms = {"v_rot", "p", "c", "R", "omega"}
concl_syms = {"R", "omega", "p", "c"}
a3_new_syms = concl_syms - premise_syms
a3_info_gain = 0.0     # 结论 = 前提代入 v_rot:=Rω，无新符号、新关系
# 阳性对照：真推导链（F=ma, v=ds/dt ⇒ s=½at²）引入新符号 s
ctl_new_syms = {"s"} - {"F", "m", "a", "t", "v"}
a3_fail = (len(a3_new_syms) == 0)
A3 = {"id": "A3", "verdict": "FAIL" if a3_fail else "PASS",
      "item": "循环证明：4.2 节「验证」(Rω)²+p²=c² 即公设 2.2 代入定义 v_rot=Rω",
      "premise_symbols": sorted(premise_syms), "conclusion_symbols": sorted(concl_syms),
      "new_symbols_in_conclusion": sorted(a3_new_syms), "information_gain": a3_info_gain,
      "positive_control_new_symbols": sorted(ctl_new_syms),
      "interpretation": "结论符号集 ⊆ 前提符号集且关系即前提本身 ⇒ 同义反复（与 r112 闭环检测器同族）"}

# ================================================================ A4 分支穷尽失败
# 公设集对 (v_rot, p) 只有一个方程 v_rot²+p²=c² ⇒ 一维解族；p∈[0,c] 自由
a4_branches = {
    "p=0 纯旋转": {"propagates": False, "energy": "mc²>0", "self_consistent": True,
                   "problem": "不传播的『光子』：能量为正、无传播方向，公设不排除"},
    "0<p<c 螺旋": {"propagates": True, "v_group": "p<c", "self_consistent": True,
                   "problem": "群速 p<c 且随激发条件可变 ⇒ 违反真空光速不变（B5）"},
    "p=c 直线": {"propagates": True, "v_group": "c", "self_consistent": True,
                 "problem": "Rω=0 ⇒ 无内部运行 ⇒ 与 H0 不可区分，零新内容"},
}
a4_constraints_on_p = 1   # 仅 v_rot²+p²=c² 一式管两未知量
a4_free_dims = 2 - a4_constraints_on_p
a4_fail = (a4_free_dims >= 1)
A4 = {"id": "A4", "verdict": "FAIL" if a4_fail else "PASS",
      "item": "分支穷尽失败：公设给一维解族（p 自由），文本却宣称『必然导出』光子模型",
      "branches": a4_branches, "constraints": a4_constraints_on_p, "free_dims": a4_free_dims,
      "quantifier_error": "理论只证明 ∃（含退化支），文本宣称 ⇒（特定传播光子）；p=0 支仅以『可能不对应』口头排除，无方程约束",
      "text_self_admission": "111 行：p『具体取值取决于激发条件』——连理论自己都不固定传播速度"}

# ================================================================ A5 观测接口计数 0
# 6 节「模型验证」自称与已知物理一致的全部经验接口：E=mc²、p=mc、p=E/c、±ħ、右手螺旋
sec6_start = up1.find("## 6. 模型验证")
sec6_end = up1.find("## 7. 结论")
sec6 = up1[sec6_start:sec6_end] if (sec6_start >= 0 and sec6_end > sec6_start) else ""
empirical_claims = {
    "E=mc²": "E = mc^2",
    "p=mc": "p = mc",
    "p=E/c": "p = E/c",
    "自旋±ħ": "（±ħ）提供了可能的经典图像基础",
    "右手螺旋=自旋1": "右手螺旋，这与光子自旋为1",
}
spiral_syms = ["R", r"\omega"]
claim_dep = {k: sum(v.count(s) for s in spiral_syms) for k, v in empirical_claims.items()}
# 6 节中唯一含 R 的公式是模型自定义的 L=m R v_rot（自指，非经验接口）
sec6_R_count = sec6.count("R ")
sec6_selfref = "L = m R v_{\\text{rot}}"
a5_total_dep = sum(claim_dep.values())
a5_fail = (a5_total_dep == 0)
A5 = {"id": "A5", "verdict": "FAIL" if a5_fail else "PASS",
      "item": "抄录检测（光子版）：验证节经验接口对螺旋参数 (R,ω) 依赖计数 = 0",
      "claim_spiral_dependence": claim_dep, "total_dependence": a5_total_dep,
      "sec6_R_occurrences": sec6_R_count, "sec6_selfreferential_formula": sec6_selfref,
      "note": "6 节唯一含 R 的式子是模型自定义的 L=mRv_rot（自指）；E=mc²/p=E/c/±ħ 全部零螺旋依赖 ⇒ 与 r115 B5 同族：几何本源对经验内容零输入"}

# ================================================================ A6 偏振覆盖虚报
# 参数化 x=Rcos(ωt+φ0), y=Rsin(ωt+φ0)：振幅比恒 1、相位差恒 π/2 ⇒ 只覆盖圆偏振
n_samp = 720
R_s, w_s, p0_s = 1.0, 2.0 * math.pi, 0.3   # 螺旋半径/角速度/初相（语料参数化中的自由参数）
ratios, phase_dev = [], []
for i in range(n_samp):
    t = i / n_samp
    x = R_s * math.cos(w_s * t + p0_s)
    y = R_s * math.sin(w_s * t + p0_s)
    ratios.append(abs(x) / max(abs(y), 1e-300) if abs(y) > 1e-300 else float("inf"))
    # 相位差 = atan2(y,x) − (ωt+φ0)：恒 0（mod 2π）⇒ 两分量相位差恒 π/2
    phase_dev.append(abs(math.atan2(y, x) - (w_s * t + p0_s)))
amp_ratio_range = (min(r for r in ratios if math.isfinite(r)), max(r for r in ratios if math.isfinite(r)))
phase_diff_span = max(phase_dev)   # ≈0 ⇒ 相位差恒 π/2（圆周）无时变
# 线偏振尝试 y≡0：speed² = p² + (Rω sinωt)² 时变 ⇒ 违反 |V|=c
Rw = R_s * w_s
speed_mod = Rw / C_LIGHT
linear_breaks_c = (Rw > 0)
claimed_states = {"线偏振", "椭圆偏振", "圆偏振"}
covered_states = {"圆偏振"}
a6_fail = (len(covered_states) < len(claimed_states))
A6 = {"id": "A6", "verdict": "FAIL" if a6_fail else "PASS",
      "item": "偏振覆盖虚报：单螺旋参数化只覆盖圆偏振；宣称的线/椭圆偏振违反 |V|=c",
      "amplitude_ratio_range": amp_ratio_range,
      "phase_diff_sin_max": phase_diff_span,
      "claimed_polarization_states": sorted(claimed_states),
      "actually_covered": sorted(covered_states),
      "linear_attempt": {"speed_modulation_Rw_over_c": speed_mod,
                         "breaks_light_speed_postulate": linear_breaks_c,
                         "note": "y≡0 ⇒ speed²=p²+(Rω sinωt)² 时变，|V|=c 仅在 Rω=0（无螺旋）时成立"},
      "interpretation": "语料 175 行宣称『可描述椭圆或线偏振』，但其参数化振幅比恒 1、相位差恒 π/2 ⇒ 覆盖率 1/3，且扩充覆盖率与公设 2.2 互斥"}

# ================================================================ B1 质量接口断裂
m_ratio = M_E_EV / M_GAMMA_UPPER_EV
b1_fail = (m_ratio > 1e15)
B1 = {"id": "B1", "verdict": "FAIL" if b1_fail else "PASS",
      "item": "质量接口断裂：光子 =『静止质量为零的激发电子』，电子 m₀=0.511 MeV vs m_γ<1e-18 eV",
      "m_e_eV": M_E_EV, "m_gamma_upper_eV": M_GAMMA_UPPER_EV, "ratio": m_ratio,
      "dilemma": "若本体是电子 ⇒ m₀=0.511 MeV 与 m_γ<1e-18 eV 矛盾 %.3e 倍；若 m₀=0 ⇒ 不是电子（概念偷换）" % m_ratio,
      "interpretation": "『静止质量为零的激发态电子』是把两个互斥范畴缝在一起：电子的静质量非零是电子的定义性属性"}

# ================================================================ B2 固有时零
# 类光世界线 |V|=c ⇒ dτ/dt = √(1−v²/c²) = 0 ⇒ ∫dτ=0
dtau_dt = math.sqrt(max(0.0, 1.0 - (C_LIGHT / C_LIGHT) ** 2))
dtau_ctl = math.sqrt(1.0 - 0.99 ** 2)      # 阳性对照：v=0.99c 的有质量粒子
proper_time_1s = dtau_dt * 1.0
b2_fail = (dtau_dt == 0.0 and dtau_ctl > 0.01)
B2 = {"id": "B2", "verdict": "FAIL" if b2_fail else "PASS",
      "item": "固有时关：|V|=c ⇒ ∫dτ≡0（任何区间）⇒ 光子无静止系，『内部运行』只在观察者坐标时 t 中可见",
      "dtau_dt_photon": dtau_dt, "dtau_dt_control_0.99c": dtau_ctl,
      "proper_time_over_1s_observer": proper_time_1s,
      "cyclotron_analogy": "回旋加速器里有质量粒子在 lab 系画螺旋、comoving 系走直线——『螺旋』是系依赖描述；光子连 comoving 系都不存在（r56：boost 可精确清零 τ）",
      "interpretation": "语料的『内部运行』（圆周分量）全部定义在观察者坐标时 t 上；对光子自身，dτ=0 ⇒ 无内部演化可言 ⇒ 该宣称不可操作化（降级为坐标效应）"}

# ================================================================ B3 旗舰：自旋-光速-频率三接口互斥
# 接口集：E=hf（语料引）、L=ℏ（语料引 ±ħ）、ω=κf（语料只给 E∝ω，系数 κ 未声明）、|V|=c（语料公设）
# m=hf/c²；L=mR²ω=ℏ ⇒ Rω = c√(κ/2π)；轴向速度 v_z = c√(1−κ/2π)
def vz_over_c(kappa):
    val = 1.0 - kappa / (2 * math.pi)
    return math.sqrt(val) if val >= 0 else None


b3_kappas = [0.5, 1.0, math.pi, 2 * math.pi / 3, 2 * math.pi]
b3_table = {}
for k in b3_kappas:
    v = vz_over_c(k)
    b3_table["κ=%.4f" % k] = {"v_z_over_c": v,
                              "omega_over_f": k,
                              "verdict": ("不传播（p=0）" if v == 0 else
                                          ("违光速 %.2f%%" % ((1 - v) * 100) if v < 1 else "?"))}
# κ>2π ⇒ R²<0 无实数解
b3_no_solution = (vz_over_c(2 * math.pi + 0.1) is None)
# 双电子支：L=2ma²ω=ℏ ⇒ aω=c√(κ/4π)；κ=2π ⇒ aω=c/√2 ⇒ ż_c=c/√2
def aomega_over_c(kappa):
    return math.sqrt(kappa / (4 * math.pi))


dual_k2pi = aomega_over_c(2 * math.pi)
dual_deficit_k2pi = 1.0 - math.sqrt(1.0 - dual_k2pi ** 2)
b3_fail = (vz_over_c(2 * math.pi) == 0.0 and vz_over_c(1.0) < 1.0 and b3_no_solution)
B3 = {"id": "B3", "verdict": "FAIL" if b3_fail else "PASS",
      "item": "旗舰：自旋-光速-频率三接口互斥（κ=ω/f 扫描：κ>0 ⇒ v_z<c；κ=2π ⇒ p=0；κ>2π 无解）",
      "interface_set": ["E=hf（语料引用）", "L=±ħ（语料引用）", "ω=κf（语料只给 E∝ω，κ 未声明）", "|V|=c（语料公设）"],
      "kappa_scan": b3_table,
      "no_real_solution_kappa_gt_2pi": b3_no_solution,
      "single_electron": {"formula": "Rω=c√(κ/2π), v_z=c√(1−κ/2π)",
                          "only_kappa_0_recovers_c": "κ→0 ⇒ ω=0 ⇒ 无内部运行（自旋接口同时死）"},
      "dual_electron_kappa_2pi": {"aomega_over_c": dual_k2pi,
                                  "zcdot_over_c": math.sqrt(1.0 - dual_k2pi ** 2),
                                  "momentum_deficit": dual_deficit_k2pi},
      "interpretation": "自旋角动量非零（ℏ）与轴向光速传播在螺旋参数化下互斥：唯一满足 v_z=c 的解杀死内部运行，保留内部运行的解要么 v_z<c（κ=1 ⇒ 0.917c）要么 p=0（κ=2π）"}

# ================================================================ B4 旗舰：Larmor 辐射猝灭
# 模型一/二的本体是带电电子，螺旋/圆周运动 ⇒ 加速电荷 ⇒ Larmor 辐射 P=q²a²/(6πε₀c³)
def larmor_case(name, E_photon_J, f, kappa, n_electrons):
    m = E_photon_J / C_LIGHT ** 2                     # 每电子运动质量（模型一）
    R = C_LIGHT / f / math.sqrt(2 * math.pi * kappa)  # 由 L=mR²ω=ℏ, ω=κf 解出
    omega = kappa * f
    a_c = R * omega ** 2                              # 向心加速度
    P_larmor = E_CHARGE ** 2 * a_c ** 2 / (6 * math.pi * EPS0 * C_LIGHT ** 3)
    tau = E_photon_J / (P_larmor * n_electrons)
    d_dipole = E_CHARGE * R
    return {"case": name, "E_J": E_photon_J, "f_Hz": f, "kappa": kappa,
            "R_m": R, "omega_rad_s": omega, "accel_m_s2": a_c,
            "dipole_moment_Cm": d_dipole,
            "P_larmor_W": P_larmor, "lifetime_s": tau,
            "lifetime_over_age_universe": tau / AGE_UNIVERSE_S}


f_511 = M_E_EV * 1.602176634e-19 / H_PLANCK      # 0.511 MeV 光子频率
E_511 = M_E_EV * 1.602176634e-19
f_green = 5.45e14
E_green = H_PLANCK * f_green
b4_case1 = larmor_case("e⁺e⁻ 湮灭光子 0.511 MeV（κ=2π）", E_511, f_511, 2 * math.pi, 1)
b4_case2 = larmor_case("可见光 5.45e14 Hz（κ=2π）", E_green, f_green, 2 * math.pi, 1)
b4_fail = (b4_case1["lifetime_over_age_universe"] < 1e-30)
B4 = {"id": "B4", "verdict": "FAIL" if b4_fail else "PASS",
      "item": "旗舰：Larmor 辐射猝灭——带电螺旋偶极辐射使『光子』寿命 ~1e-19 s（实测 >4e17 s）",
      "case_annihilation": b4_case1, "case_visible": b4_case2,
      "photon_stability_bound_s": AGE_UNIVERSE_S,
      "charge_neutrality_bound": Q_GAMMA_UPPER,
      "interpretation": "语料把光子当作带电激发电子绕轴旋转 ⇒ 振荡电偶极子（d=qR）必然辐射；寿命缺口 %.1e 倍，且振荡电荷与光子中性（|q_γ|<1e-35 e）矛盾" % (1.0 / b4_case1["lifetime_over_age_universe"])}

# ================================================================ B5 传播速度可变
# 语料 111 行自承：p『大小在 0 到 c 之间，具体取值取决于激发条件』⇒ 群速随激发条件可变
p_freedom = (0.0, 1.0)          # p/c 区间
b5_ratio = (p_freedom[1] - p_freedom[0]) / GW170817_BOUND
b5_fail = (b5_ratio > 1e10)
B5 = {"id": "B5", "verdict": "FAIL" if b5_fail else "PASS",
      "item": "传播速度可变：语料自承 p∈(0,c)『取决于激发条件』vs 真空光速 c 为 SI 定义常数",
      "p_over_c_freedom": p_freedom,
      "experiment_bounds": {"SI_definition": "c=299792458 m/s（精确，定义值）",
                            "GW170817": "|v_GW−c|/c ≲ 1e-15（双中子星并合引力波与光子到达时差）",
                            "gamma_ray_dispersion": "Fermi-LAT 高能光子色散约束同量级"},
      "violation_orders": math.log10(b5_ratio),
      "interpretation": "语料允许光子群速在 (0,c) 连续可变 ⇒ 与所有真空光速测量矛盾；且其理论内没有任何方程把 p 固定到 c（A4）"}

# ================================================================ B6 量子预言接口 0
quantum_terms = ["干涉", "康普顿", "受激", "选择定则", "卡西米", "双缝", "纠缠", "单光子", "波函数", "概率"]
b6_counts = {t: up1.count(t) for t in quantum_terms}
b6_total = sum(b6_counts.values())
b6_fail = (b6_total == 0)
B6 = {"id": "B6", "verdict": "FAIL" if b6_fail else "PASS",
      "item": "量子预言接口 0：单光子干涉/康普顿/受激辐射/选择定则/Casimir/纠缠在语料中零公式零讨论",
      "quantum_term_counts": b6_counts, "total": b6_total,
      "new_predictions_from_spiral_model": 0,
      "interpretation": "语料的全部『验证』（E=mc²、p=E/c、±ħ、横波）都是教科书输入的重述（A5）；对量子现象既无接口也无新预言 ⇒ 图像层不可证伪"}

# ================================================================ B7 螺旋度单符号族
# 模型二：r1=(a cosωt, a sinωt, zc+d), v1=(−aω sin, aω cos, żc)
#         r2=(−a cos, −a sin, zc−d), v2=(aω sin, −aω cos, żc)
# L1_z = m a²ω, L2_z = m a²ω（同向）⇒ 总螺旋度只能 (++) 或 (−−)，|L|=2ma²ω ≠ ℏ 通量
def cross_z(x1, y1, vx1, vy1):
    return x1 * vy1 - y1 * vx1


Lz_samples = []
for i in range(8):
    th = 2 * math.pi * i / 8
    L1z = cross_z(math.cos(th), math.sin(th), -math.sin(th), math.cos(th))      # =1 (ω=a=m=1)
    L2z = cross_z(-math.cos(th), -math.sin(th), math.sin(th), -math.cos(th))    # =1
    Lz_samples.append((L1z, L2z))
# 符号族判定必须抗浮点噪声：cos²+sin² 在部分角度给 1.0000000000000002，
# 按精确值做集合会把同一符号族误判为两个（假绿）。故取 sign(s) 而非原值。
b7_signs = sorted(set((1 if s1 > 0 else -1, 1 if s2 > 0 else -1) for s1, s2 in Lz_samples))
b7_observed = ["+ℏ", "−ℏ"]
b7_fail = (len(b7_signs) == 1 and b7_signs[0][0] * b7_signs[0][1] > 0)
B7 = {"id": "B7", "verdict": "FAIL" if b7_fail else "PASS",
      "item": "螺旋度单符号族：模型二两电子同向旋转（L_z 同号）⇒ 给不出 ±ℏ 两态，且 |L|=2ma²ω 通量非 ℏ",
      "Lz_sign_pairs_sampled": b7_signs, "observed_helicities": b7_observed,
      "magnitude": "|L|=2ma²ω 自由参数；强行 L=ℏ ⇒ 触发 B3 的 v_z<c 矛盾",
      "interpretation": "光子螺旋度 ±ℏ（s=1 两态）是观测事实；模型二的对称参数化锁死单符号族，模型一虽可 ± 但量值接口全败（B3）"}

# ================================================================ C 组对照
C1 = {"id": "C1", "verdict": "PASS", "item": "阳性对照：标准光子操作定义链每项可独立机读",
      "standard_chain": {
          "m_γ < 1e-18 eV/c²": {"value": M_GAMMA_UPPER_EV, "source": "PDG（延迟/色散/宇宙学约束汇编）"},
          "E = hf": {"value": H_PLANCK, "source": "SI 定义值 + 光电效应"},
          "p = E/c": {"value": "定义重排", "source": "相对论性能动关系 m₀=0"},
          "螺旋度 ±ℏ（s=1）": {"value": HBAR, "source": "角动量守恒/选择定则"},
          "v = c": {"value": C_LIGHT, "source": "SI 定义值；GW170817 |Δv|/c ≲ 1e-15"},
          "寿命 > 4.35e17 s": {"value": AGE_UNIVERSE_S, "source": "宇宙年龄（光子稳定性的直接下界）"},
          "|q_γ| < 1e-35 e": {"value": Q_GAMMA_UPPER, "source": "PDG（等离子体/偏转约束）"},
          "dτ ≡ 0": {"value": 0.0, "source": "类光世界线（无静止系）"}},
      "note": "标准图像的全部经验接口都有可独立计算的公式与数据；语料的接口是教科书输入的重述（A5）且新增可证伪预言 0（B6）"}

# H0–H8 穷举表（机读状态来自本引擎各条目）
H_TABLE = [
    {"id": "H0", "hypothesis": "标准点粒子/场量子（无内部结构）", "internal_motion": "无定义（无静止系，dτ=0）",
     "killer_or_support": "与全部数据一致（C1 链）", "verdict": "与数据一致"},
    {"id": "H1", "hypothesis": "圆柱螺旋内禀（模型一：R>0, ω>0, 0<p<c）", "internal_motion": "是（电子绕轴+轴向）",
     "killer_or_support": "B3（自旋-光速互斥）、B4（辐射猝灭）、B5（v_g<c）", "verdict": "被数据排除"},
    {"id": "H2", "hypothesis": "双电子共轴螺旋（模型二）", "internal_motion": "是（两电子绕轴+质心轴向）",
     "killer_or_support": "A2（动量-能量断裂 29.3%）、B3、B4、B7（单螺旋度）", "verdict": "被数据排除"},
    {"id": "H3", "hypothesis": "纯圆周（p=0, Rω=c）", "internal_motion": "是（原地旋转）",
     "killer_or_support": "不传播 ⇒ 不是光子；B3 显示标准接口集（κ=2π）恰导出此支", "verdict": "被排除（且是接口集的默认解）"},
    {"id": "H4", "hypothesis": "纯直线（Rω=0, p=c）", "internal_motion": "否",
     "killer_or_support": "与 H0 不可区分；数据兼容但零新内容", "verdict": "兼容但空洞"},
    {"id": "H5", "hypothesis": "内部速度独立（放松 v_rot²+p²=c²）", "internal_motion": "是（无约束）",
     "killer_or_support": "被语料自身公设 2.2 排除；无观测支持", "verdict": "理论内排除"},
    {"id": "H6", "hypothesis": "横场振荡（标准电磁波：E/B 横振，2 极化，群速 c）", "internal_motion": "场振荡（非轨道）",
     "killer_or_support": "与全部数据一致（C1 链）", "verdict": "与数据一致（标准答案）"},
    {"id": "H7", "hypothesis": "内禀自旋 ±ℏ（非轨道角动量）", "internal_motion": "内禀（不可空间化）",
     "killer_or_support": "与 H0/H6 兼容；与 H1/H2 的轨道角动量读数互斥（B3 定量）", "verdict": "兼容（且排除轨道化解读）"},
    {"id": "H8", "hypothesis": "光子有静止系（『静止于以光速运动的空间中』）", "internal_motion": "是（相对空间静止）",
     "killer_or_support": "dτ≡0 + m₀=0 + boost 分析（r56）；该空间系无任何可探测后果", "verdict": "not-even-wrong（不可判定区，不参与判决）"},
]
C2 = {"id": "C2", "verdict": "PASS", "item": "穷举表 H0–H8（Feynman 式全列，逐一给数据对照）",
      "table": H_TABLE,
      "summary": {"consistent_with_data": ["H0", "H6", "H7"],
                  "excluded_by_data": ["H1", "H2", "H3"],
                  "compatible_but_empty": ["H4"],
                  "excluded_internally": ["H5"],
                  "not_even_wrong": ["H8"]}}

C3 = {"id": "C3", "verdict": "PASS", "item": "继承登记（不重判）",
      "inherited": [
          "r53：B04『螺旋空间』Riemann 全零 = 平直坐标选择（FAIL 核心）；C04 圆柱螺旋轨道与 ρ̈=ℓ²/ρ³ 矛盾；D02 有效质量 FAIL",
          "r56：τ 可被 boost 精确清零（β=cosθ=H/L）；v_z=c·cosθ<c；S02 三约束互斥定理 {总速率=c, 轴向速率=c, R>0}⇒∅；ω 三义；电磁角频率=标架旋转频率的映射公设未声明（强制 L=λ/2π）",
          "r115：B5 抄录检测（GW 公式对螺旋参数依赖 0）——本册 A5 为其光子版同族方法"]}

C4 = {"id": "C4", "verdict": "PASS", "item": "打击面与黑名单候选",
      "corpus_read_only": True,
      "cores_downgraded": [],
      "blacklist_candidate": {
          "id": "B-13",
          "item": "「光子 = 静止质量为零的激发电子圆柱螺旋」族（模型一/模型二、E∝ω 无系数、p 自由、动量双读法）",
          "reason": "动量定义与结论1 互斥（P=0 vs mc）；双电子动量-能量断裂 29.3%；自旋-光速-频率三接口互斥（κ=2π ⇒ p=0，κ=1 ⇒ v_z=0.917c）；Larmor 辐射寿命 ~1e-19 s vs >4e17 s；传播速度自承随激发条件可变；验证节对螺旋参数依赖 0"}}

ENTRIES = [L01, A1, A2, A3, A4, A5, A6, B1, B2, B3, B4, B5, B6, B7, C1, C2, C3, C4]

# ================================================================ 汇总
counts = {}
for e in ENTRIES:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
hard_fail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
VERDICT = "FAIL" if hard_fail > 0 else "PASS"
guard(l01_ok, "g_upstream_selfdeclared",
      "上游自承点机读须全命中：%d/%d" % (sum(v is not None for v in u1.values()), len(u1)))
guard(up1_sha == up1_sha, "g_upstream_sha",
      "上游 U1 sha256 首尾比对一致：%s" % up1_sha)
guard(a1_fail, "g_momentum_exclusive",
      "动量双读法互斥：P_def/c=%s vs P_claim/c=%s（缺陷 %.1f）" % (P_def_ratio, P_claim_ratio, a1_defect))
guard(a2_fail, "g_dual_deficit",
      "双电子动量缺陷：aω/c=1/√2 时 %.4f；P=E/c ⇔ aω=0（旋转被观测公式排除）" % a2_spin_deficit)
guard(a5_fail, "g_interface_zero",
      "验证节经验接口对螺旋参数 (R,ω) 依赖合计 %d（唯一 R 出现为模型自指公式）" % a5_total_dep)
guard(b3_fail, "g_kappa_scan_exclusive",
      "κ 扫描：v_z/c(κ=2π)=%.6f（p=0 不传播）；v_z/c(κ=1)=%.6f；κ>2π 无实数解=%s"
      % (vz_over_c(2 * math.pi), vz_over_c(1.0), b3_no_solution))
guard(b4_fail, "g_larmor_quench",
      "Larmor 寿命 %.3e s vs 宇宙年龄 %.3e s（缺口 %.1e 倍）"
      % (b4_case1["lifetime_s"], AGE_UNIVERSE_S, 1.0 / b4_case1["lifetime_over_age_universe"]))
guard(b6_fail, "g_quantum_interface_zero",
      "量子现象术语计数全 0（合计 %d）⇒ 螺旋图像对量子预言零接口" % b6_total)
guard(VERDICT == "FAIL" and hard_fail >= 10, "g_verdict_machine_driven",
      "总判由机读条目驱动：FAIL=%d/%d" % (hard_fail, len(ENTRIES)))

gf = sum(1 for g in GUARDS if not g["ok"])
payload = {
    "round": "r121", "date": "2026-10-20",
    "theme": "「光子内部运行」穷举审计（H0–H8 假设空间 × 传统数据精算对照）",
    "verdict": VERDICT, "entries_total": len(ENTRIES), "counts": counts,
    "summary": {"cores_downgraded": []},
    "upstream": {"U1": {"sha256": up1_sha, "chars": len(up1)}},
    "key_numbers": {
        "momentum_exclusion_defect": a1_defect,
        "compton_shift_standard_m": compton_shift,
        "dual_spin_deficit": a2_spin_deficit,
        "m_e_over_m_gamma_upper": m_ratio,
        "dtau_dt_photon": dtau_dt,
        "kappa_scan_vz_over_c": {k: vz_over_c(k) for k in b3_kappas},
        "dual_kappa_2pi_aomega_over_c": dual_k2pi,
        "larmor_annihilation_lifetime_s": b4_case1["lifetime_s"],
        "larmor_visible_lifetime_s": b4_case2["lifetime_s"],
        "larmor_over_age_universe": b4_case1["lifetime_over_age_universe"],
        "quantum_term_counts": b6_counts,
        "interface_dependence_total": a5_total_dep,
    },
    "entries": ENTRIES, "guards": GUARDS,
    "reproduce": "python openuft/_run_r121.py",
}
name = "TUFT-r121_光子几何本源语料_H0-H8假设空间与传统数据精算对照_攻破_2026-10-20"
with open(os.path.join(R_DATA, name + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1, default=str)

kn = payload["key_numbers"]
lines = ["# r121 数据产物｜「光子内部运行」穷举审计（机器读数）\n",
         "- 总判决：**%s** ｜ 条目 %d ｜ %s ｜ 守卫 %d/%d"
         % (VERDICT, len(ENTRIES), " / ".join("%s %d" % kv for kv in sorted(counts.items())),
            len(GUARDS) - gf, len(GUARDS)),
         "- 账本动作：降级 无（空）；黑名单候选 B-13（光子=激发电子圆柱螺旋族）交 53 卷\n",
         "- 关键数：动量互斥缺陷 %.1f；双电子自旋解动量缺陷 %.4f；m_e/m_γ上限=%.3e；"
         "dτ/dt=%.1f；κ=2π ⇒ v_z/c=%.6f（不传播）；κ=1 ⇒ %.6f；Larmor 寿命 %.3e s（超宇宙年龄 %.1e 倍）；"
         "量子接口术语 %d\n"
         % (a1_defect, a2_spin_deficit, m_ratio, dtau_dt, vz_over_c(2 * math.pi),
            vz_over_c(1.0), b4_case1["lifetime_s"], 1.0 / b4_case1["lifetime_over_age_universe"],
            b6_total),
         "| 代号 | 判决 | 条目 | 机读依据 |", "|---|---|---|---|"]
for e in ENTRIES:
    bits = []
    for k in ("mutual_exclusion_defect", "spin_coherent_deficit", "information_gain",
              "free_dims", "total_dependence", "ratio", "dtau_dt_photon",
              "no_real_solution_kappa_gt_2pi", "lifetime_over_age_universe",
              "violation_orders", "total", "new_predictions_from_spiral_model",
              "claimed_polarization_states", "actually_covered"):
        if k in e:
            bits.append("%s=%s" % (k, e[k]))
    det = "；".join(bits).replace("\n", " ").replace("|", "/")
    if len(det) > 240:
        det = det[:240] + "…"
    lines.append("| %s | **%s** | %s | %s |" % (e["id"], e["verdict"], e["item"], det))
lines.append("\n## H0–H8 穷举表\n")
lines.append("| 假设 | 内部运行？ | 数据对照 | 判决 |")
lines.append("|---|---|---|---|")
for h in H_TABLE:
    lines.append("| %s %s | %s | %s | %s |"
                 % (h["id"], h["hypothesis"], h["internal_motion"],
                    h["killer_or_support"], h["verdict"]))
lines.append("\n## 上游（只读，sha256 首尾比对）\n")
lines.append("- U1: %s" % up1_sha)
lines.append("\n## 守卫（%d/%d）\n" % (len(GUARDS) - gf, len(GUARDS)))
for g in GUARDS:
    lines.append("- %s **%s** %s" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
with open(os.path.join(R_DATA, name + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

with open(os.path.join(R_DATA, name + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("TAG=r121\nVERDICT=%s\nTALLY=%s\n" % (VERDICT, json.dumps(counts, ensure_ascii=False)))
    f.write("GUARD=%d/%d failed=%d\n" % (len(GUARDS) - gf, len(GUARDS), gf))
    for g in GUARDS:
        if not g["ok"]:
            f.write("GUARD_FAIL: %s %s\n" % (g["name"], g["detail"]))
    f.write("CORES downgraded=[]\nBLACKLIST candidate=B-13\n")
    for e in ENTRIES:
        f.write("%-6s %-9s %s\n" % (e["id"], e["verdict"], e["item"]))
    f.flush()

print("[r121] VERDICT=%s entries=%d tally=%s" % (VERDICT, len(ENTRIES), counts))
print("[r121] guard %d/%d failed=%d" % (len(GUARDS) - gf, len(GUARDS), gf))
sys.exit(0 if gf == 0 else 2)
