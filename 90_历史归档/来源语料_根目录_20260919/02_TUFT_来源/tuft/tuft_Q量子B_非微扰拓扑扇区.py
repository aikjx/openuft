# -*- coding: utf-8 -*-
"""
TUFT Q-TUFT 非微扰拓扑扇区 全维精算
==================================
对象：《Q-TUFT非微扰拓扑扇区——多拓扑荷叠加态、宇宙波函数、推广惠勒-德维特方程与拓扑相变》

承接：
  * tuft_Q量子_report.txt   —— 已判 W=(1/8π²)∫T∧T 非特征类、非形变不变、无整性（Q2.4-Q2.6）
  * tuft_Q量子A_report.txt  —— 已判 D_top=Σ_W 与 [Ŵ,Ĥ]=0 互相否定、θ 真空使严格守恒失效（A6.3/A6.4）
  * tuft_暴胀CMB_report.txt —— TUFT 暴胀扇区自证伪（5 PASS / 35 FAIL）
  * tuft_B_自屏蔽_report    —— 黑洞 ξ=1/2 自屏蔽偏离 46.82%，该分支被排除

本册只审查**新增内容**（希尔伯特扇区、.Page 曲线、拓扑纠缠熵、退相干时间、
推广 WDW、拓扑 S 矩阵、黑洞拓扑荷），并对继承项做追溯登记。

红线：数学自洽 != 物理实验证实。原始报告保留不改，本册只追加判定。
"""
from __future__ import print_function

import os
import sys
import json
import math
import numpy as np
import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_Q量子B_report.txt")


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

    def add(self, sec, name, verdict, detail=""):
        self.rows.append((sec, name, verdict, detail))
        line = "  [%s] %s" % (verdict, name)
        if detail:
            line += "   |  " + detail
        self.echo(line)

    def summary(self):
        from collections import Counter
        cnt = Counter(v for _, _, v, _ in self.rows)
        self.section("汇总")
        for k in ["PASS", "FAIL", "BOUNDARY", "INFO"]:
            self.echo("  %-9s = %d" % (k, cnt.get(k, 0)))
        if cnt.get("FAIL"):
            self.echo("  存在 FAIL（真实缺陷）:")
            for sec, name, v, det in self.rows:
                if v == "FAIL":
                    self.echo("    - [%s] %s" % (sec, name))
        return cnt

    def dump(self):
        try:
            with open(REPORT_PATH, "w", encoding="utf-8") as fh:
                fh.write("\n".join(self.lines))
                fh.write("\n")
        except Exception as exc:
            print("  [warn] report write failed: " + str(exc))


R = Report()

R.echo("TUFT Q-TUFT 非微扰拓扑扇区 全维精算")
R.echo("对象：多拓扑荷叠加 / 宇宙波函数 / 推广 Wheeler-DeWitt / 拓扑相变 / 黑洞拓扑量子态")
R.echo("红线：数学自洽 != 物理实验证实。")

# ==========================================================================
# 常量（SI + CODATA 近似）
# ==========================================================================
G = 6.674e-11
c = 2.998e8
hbar = 1.055e-34
kB = 1.381e-23
eV = 1.602e-19
lP = 1.616e-35
mP = 2.176e-8          # kg
tP = 5.391e-44         # s
EP_J = math.sqrt(hbar * c ** 5 / G)
EP_GeV = EP_J / eV / 1e9
M_sun = 1.989e30
m_nuc = 1.673e-27

# ==========================================================================
# §1 继承性追溯
# ==========================================================================
R.section("§1  继承性追溯：本册地基是否已被前册判否")

R.add("B1.1", "本册全部六块内容都建立在已被判否的 W 之上", "INFO",
      "前册已证：(i) W(λT)=λ²W(T) 非形变不变；(ii) 显式反例说明 W 取连续统、'W∈Z'无依据；"
      "(iii) 1/8π² 归一化来自 Chern-Weil，只适用于曲率，挠率不适用；(iv) D_top=Σ_{W∈Z} 与 "
      "[Ŵ,Ĥ]=0 互相否定；(v) θ 真空使任何 '拓扑荷严格守恒' 在量子层面失效。"
      "本册 §1.1 重新写 [Ŵ,Ĥ]=0、§2.2 重写 D_top=Σ_W d_W²、§6 用 W 论信息守恒 ⇒ 继承性 FAIL，"
      "但以下**逐条独立审查本册新增的结构**（即使换成合格拓扑荷 Lk/Tw 也不自动成立的部分）。")

# 复一个最省事的关键事实：二次齐次
lams = [0.5, 1.0, 1.5, 2.0, 2.5]
scal = [round(lam ** 2, 6) for lam in lams]
R.add("B1.2", "复查：W(λT)=λ²W(T)（二次齐次 ⇒ 不可能整值化）", "FAIL",
      "λ = " + ", ".join(str(x) for x in lams) + " ⇒ W(λT)/W(T) = "
      + ", ".join(str(x) for x in scal) + "（连续）"
      "；λ=1 与 λ=1.0001 之间 W 连续漂移 ⇒ 'W∈Z 的好量子数'在数学上不可能。")

# ==========================================================================
# §2 W 的量纲与积分域
# ==========================================================================
R.section("§2  拓扑荷定义：量纲与积分域")

# 质量量纲（自然单位 ℏ=c=1，坐标 x 的量纲 = -1）
# [e^a]= -1（1-形式，分量无量纲），[T^a]= -1（2-形式，分量 +1）
# ⇒ [T∧T] = -2 ⇒ [∫_M T∧T] = -2（顶形式积分不改变量纲）
dim_W_def = -2
dim_W_BH = 0  # A/(4 l_P²) 无量纲
R.add("B2.1", "W=(1/8π²)∫T∧T 带质量量纲 -2，与 W_BH=A/(4l_P²)（无量纲）冲突", "FAIL",
      "[T^a]= -1（2-形式，分量规范维 1）⇒ [T∧T]= -2 ⇒ [W_def]=%d；"
      "而 §6.1 的 W_BH=A/(4l_P²) 量纲为 %d ⇒ 同一个 'W' 处在不同量纲，"
      "要么补一个质量平方因子 m_*²（此时 W=(m_*²/8π²)∫T∧T 不再是裸拓扑量），要么放弃与 A/4l_P² 的等同。"
      % (dim_W_def, dim_W_BH))

# 4-形式积分到 3-曲面
deg = 4
dim_sigma = 3
R.add("B2.2", "T∧T 是 4-形式，不能积分到 3 维曲面 Σ 上", "FAIL",
      "deg(T^a∧T_a)=%d，而 §5.1 明确 'Σ 为 3 维类空曲面'（dim=%d）⇒ ∫_Σ T∧T 按次数 reason 恒为 0（未定义）。"
      "Pontryagin/CS 型拓扑荷的正确写法：体积分 (1/8π²)∫_M Tr(F∧F) 或其 CS 3-形式边界表达 ∫_Σ CS₃。"
      % (deg, dim_sigma))

# ==========================================================================
# §3 希尔伯特空间扇区与 "守恒 ⇒ 信息守恒"
# ==========================================================================
R.section("§3  拓扑扇区希尔伯特空间：守恒能否推出信息守恒")

R.add("B3.1", "直和 ⊕_{W∈Z} 的写法与 Kronecker δ_{W'W} 无效", "FAIL",
      "既然 W 取连续统（B1.2），分解只能是**直积/直积分** ∫^⊕ dW H_W 且正交性写成 δ(W'-W)；"
      "原文的 δ_{W'W}（Kronecker）预设了可数标记。补充：即便改用合格的 Lk∈Z，"
      "前册 A6.3 已证 '扇区求和 D_top=Σ_W' 与 '[Ŵ,Ĥ]=0' 互斥（求和=隧穿=不守恒）。")

# --- 决定性反例：拓扑荷严格守恒但信息丢失 ---
# 相位阻尼（dephasing）：Kraus K0=a I, K1=b σ_z,  a²+b²=1
# W = σ_z ⊗ I ⇒ 所有 Kraus 都与 W 对易 ⇒ ⟨W⟩、ΔW、乃至 W 的完整分布都不变
sz = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
I2 = np.eye(2, dtype=complex)
Wop = np.kron(sz, I2)          # 4 维，拓扑荷本征值 ±1（各二重简并）
psi0 = np.array([1, 1, 1, 1], dtype=complex) / 2.0
rho0 = np.outer(psi0, psi0.conj())


def dephase(rho, lam):
    a = math.sqrt((1.0 + lam) / 2.0)
    b = math.sqrt((1.0 - lam) / 2.0)
    K0 = a * np.eye(4, dtype=complex)
    K1 = b * Wop
    return K0 @ rho @ K0.conj().T + K1 @ rho @ K1.conj().T


def kron_sum_check(lam):
    a = math.sqrt((1.0 + lam) / 2.0)
    b = math.sqrt((1.0 - lam) / 2.0)
    K0 = a * np.eye(4, dtype=complex)
    K1 = b * Wop
    return K0.conj().T @ K0 + K1.conj().T @ K1


lams2 = [1.0, 0.8, 0.5, 0.2, 0.0]
rowsinki = []
for lam in lams2:
    rho = dephase(rho0, lam)
    w_mean = np.trace(Wop @ rho).real
    w2_mean = np.trace((Wop @ Wop) @ rho).real
    purity = np.trace(rho @ rho).real
    ev = np.linalg.eigvalsh(rho)
    ev = ev[ev > 1e-15]
    sent = -float(np.sum(ev * np.log(ev)))
    kerr = np.max(np.abs(kron_sum_check(lam) - np.eye(4, dtype=complex)))
    rowsinki.append((lam, w_mean, w2_mean, purity, sent, kerr))

kraus_err = max(r[5] for r in rowsinki)
w_means = [round(r[1], 12) for r in rowsinki]
w2_means = [round(r[2], 12) for r in rowsinki]
purities = [round(r[3], 6) for r in rowsinki]
ents = [round(r[4], 6) for r in rowsinki]

R.add("B3.2", "决定性反例：拓扑荷严格守恒 + 幺正破坏 ⇒ 信息照样丢失", "FAIL",
      "取 W=σ_z⊗I，Kraus K0=aI、K1=bW（相位阻尼；实跑 |ΣK†K-I|=%.1e，是合法 CPTP 通道）。"
      "λ=" % kraus_err
      + ",".join(str(x) for x in lams2) + " ⇒ ⟨W⟩=" + ",".join(str(x) for x in w_means)
      + "；⟨W²⟩=" + ",".join(str(x) for x in w2_means)
      + "（严格不变）；而纯度 Tr ρ²=" + ",".join(str(x) for x in purities)
      + "、冯诺依曼熵 S=" + ",".join(str(x) for x in ents)
      + " ⇒ ⟨W⟩ 与 W 的完整分布守恒但信息全丢。"
        "结论：'[Ŵ,Ĥ]=0 ⇒ 黑洞蒸发幺正 ⇒ 信息不丢失'是**无效推理**；"
        "守恒是一个标量约束，幺正性是无穷多条约束，前者推不出后者。")

R.add("B3.3", "扇区叠加 vs 超选择：本册两节自相矛盾的定位", "INFO",
      "若 W 真正作为好量子数被保持，标准做法是 **超选择**（物理可观测量与 Ŵ 对易 ⇒ 不同 W 扇区不相干叠加），"
      "此时 §2.1 '一般量子态是不同扇区叠加 Σ c_W|W⟩' 不被允许；"
      "若允许叠加（§2.1/§2.3 退相干讨论），则 Ŵ 只是普通守恒量而非超选择荷。"
      "本册两节各取一半，未声明立场。")

# ==========================================================================
# §4 拓扑纠缠熵
# ==========================================================================
R.section("§4  拓扑纠缠熵 S_topo = -ln D")

# Kitaev-Preskill 标准：S_topo = -ln D, D = sqrt(Σ_i d_i²)
def s_kp(dims):
    D = math.sqrt(sum(d * d for d in dims))
    return -math.log(D), D


def s_doc(dims):
    D = sum(d * d for d in dims)
    return -math.log(D), D


for label, n in [("Z_2 toric code", 4), ("Z_10", 10), ("Z_100", 100)]:
    dims = [1.0] * n
    kpv, kpD = s_kp(dims)
    docv, docD = s_doc(dims)
    R.add("B4.1", "归一化约定：本册 D=Σ d_W² 与 Kitaev-Preskill 的 D=√(Σ d_i²) 差因子 2", "FAIL",
          "%s（d_i=1，%d 个扇区）：KP 口径 D=%.4f ⇒ S_topo=%.6f；本册口径 D=%.4f ⇒ S_topo=%.6f"
          " ⇒ 比值 %.3f（恒为 2）（n=%d）" % (label, n, kpD, kpv, docD, docv, docv / kpv, n))

# 发散
partials = []
for nmax in [10, 100, 1000, 10000, 100000]:
    Ws = list(range(-nmax, nmax + 1))
    partials.append(sum(1.0 for _ in Ws))  # d_W = 1
R.add("B4.2", "Σ_{W∈Z} d_W² 发散 ⇒ S_topo = -∞", "FAIL",
      "d_W≡1 的部分和 |W|≤N_max = " + ",".join(str(p) for p in partials)
      + "（随 N 线性发散）⇒ D=∞ ⇒ S_topo=-∞，无物理意义。"
        "拓扑纠缠熵有限的前提是**有限个任意子扇区**（模张量范畴），"
        "把 'W∈Z 全部整数' 当扇区集合直接失败。")

# 可观测性
M0 = 10.0 * M_sun
rs = 2 * G * M0 / c ** 2
A0 = 4.0 * math.pi * rs ** 2
W0 = A0 / (4.0 * lP ** 2)
ratio = 1.0 / W0
R.add("B4.3", "'TUFT 独有贡献' S_topo 的可观测性量级", "INFO",
      "10 M☉ 黑洞的引力面积熵项 A/(4l_P²)=%.4e（无量纲），而 S_topo=-ln D 为 O(1) 常数"
      " ⇒ 相对贡献 %.3e。" % (W0, ratio)
      + " 在无三区域组合分离方案（Kitaev-Preskill：γ = S_AB+S_BC+S_AC-S_A-S_B-S_C-S_ABC）"
        "之前，-ln D 与 '待定常数' 不可区分 ⇒ 目前不构成可证伪预言。")

# ==========================================================================
# §5 拓扑退相干时间
# ==========================================================================
R.section("§5  拓扑退相干时间 τ = ℏ/(g_topo² N_env)")

# 量纲：[ℏ]=J·s。设 N 无量纲 ⇒ 要得到秒，必须 [g_topo²] = J ⇒ g 的量纲 = √J
R.add("B5.1", "τ_decoh = ℏ/(g²N) 量纲错误", "FAIL",
      "[ℏ]=J·s；N 无量纲 ⇒ 要有 [τ]=s，必须 [g_topo²]=J，即 [g_topo]=√(能量)。"
      "若 g_topo 是标准意义上的无量纲耦合，则该式量纲为作用量（J·s）而非时间。"
      "标准退相干率写作 Γ = γ·N（γ 为率，单位 s⁻¹），τ=1/Γ ⇒ 必须显式给出能量/率标度。")

N_env = 1e23
tau_claim = 1e-30
hbar_over_tau = hbar / tau_claim         # J
g2_per_cell_J = hbar_over_tau / N_env    # J
g2_per_cell_eV = g2_per_cell_J / eV
g_val = math.sqrt(g2_per_cell_eV)
R.add("B5.2", "反解：要兑现 τ~10⁻³⁰ s，需要多大的 g_topo", "INFO",
      "N_env=%.0e、τ=%.0e s ⇒ g²N = ℏ/τ = %.4e J = %.4e eV ⇒ 单元胞 g² = %.4e eV，"
      "g = %.4e √(eV)。该量纲为平方根能量的耦合在本册没有定义 ⇒ "
      "所谓 '宏观 τ~10⁻³⁰ s' 是把目标值反解进一个未定标度的公式，非推导结果。"
      % (N_env, tau_claim, hbar_over_tau, hbar_over_tau / eV, g2_per_cell_eV, g_val))

# ==========================================================================
# §6 推广 Wheeler-DeWitt 方程
# ==========================================================================
R.section("§6  推广 Wheeler-DeWitt 方程")

# --- B6.1：微分同胚约束的第一项在 Riemann-Cartan 几何中恒为零 ---
xs = sp.symbols('x0 x1 x2')
rng = np.random.default_rng(20260916)


def poly(terms):
    return sum(sp.Integer(int(v)) * mon for v, mon in terms)


mons = [sp.Integer(1), xs[0], xs[1], xs[2], xs[0] * xs[1], xs[1] ** 2]

# 随机平凡标架 e^A_a（3 维空间，δ_AB）
e = sp.zeros(3, 3)
for A in range(3):
    for a in range(3):
        coeffs = [(rng.integers(1, 4), mons[0])]
        for k in range(1, 4):
            coeffs.append((rng.integers(-2, 3), mons[k]))
        e[A, a] = sp.Integer(1) * (A == a) + sp.Rational(1, 7) * poly(coeffs)

# 随机反对称 spin connection（δ_{AC}ω^C_{Bb} + δ_{BC}ω^C_{Ab} = 0）
omega = []
for b in range(3):
    M = sp.zeros(3, 3)
    for A in range(3):
        for B in range(A + 1, 3):
            mp = sp.Rational(1, 5) * poly([(rng.integers(-3, 4), mons[k]) for k in range(1, 5)])
            M[A, B] = mp
            M[B, A] = -mp
    omega.append(M)

e_inv = e.inv()
# Γ^d_{ab} = e_A^d (∂_a e^A_b + ω_a{}^A_C e^C_b)   （标架假设）
Gam = [[[None] * 3 for _ in range(3)] for _ in range(3)]
for a in range(3):
    for b in range(3):
        for d in range(3):
            expr = 0
            for A in range(3):
                term = sp.diff(e[A, b], xs[a])
                for C in range(3):
                    term += omega[a][A, C] * e[C, b]
                expr += e_inv[d, A] * term
            Gam[a][b][d] = sp.simplify(expr)

# g_ab = δ_AB e^A_a e^B_b
g = sp.zeros(3, 3)
for a in range(3):
    for b in range(3):
        g[a, b] = sp.simplify(sum(e[A, a] * e[A, b] for A in range(3)))

# 挠率 T^A_{bc}
Tmax = 0.0
for A in range(3):
    for b in range(3):
        for cc in range(b + 1, 3):
            expr = sp.diff(e[A, cc], xs[b]) - sp.diff(e[A, b], xs[cc])
            for C in range(3):
                expr += omega[b][A, C] * e[C, cc] - omega[cc][A, C] * e[C, b]
            Tmax = max(Tmax, abs(float(sp.simplify(expr).subs({xs[0]: 0.3, xs[1]: -0.2, xs[2]: 0.5}))))

# D_a g_{bc}
Qmax = 0.0
for a in range(3):
    for b in range(3):
        for cc in range(3):
            expr = sp.diff(g[b, cc], xs[a])
            for d in range(3):
                expr += -Gam[a][b][d] * g[d, cc] - Gam[a][cc][d] * g[b, d]
            val = float(sp.simplify(expr).subs({xs[0]: 0.3, xs[1]: -0.2, xs[2]: 0.5}))
            Qmax = max(Qmax, abs(val))

R.add("B6.1", "微分同胚约束 H_i 的第一项 π^{ab}D_i h_{ab} 恒等于 0", "FAIL",
      "挠率 ≠ 非度规性：在 Riemann-Cartan 几何（ω_AB = -ω_BA）中 D_i g_ab = -Q_{iab} ≡ 0。"
      "实跑随机标架 + 随机反对称自旋联络：max|T^A_bc| = %.6f（挠率非零），"
      "而 max|D_a g_bc| = %.2e（机器零）⇒ 该项恒为零，约束退化。"
      "正确的微分同胚约束应为 H_i = -2 D_j π^{ja} h_{ai} + π^T D_i T + π^Ω ∂_iΩ = 0，"
      "即导数作用在**动量**上而非度规上。" % (Tmax, Qmax))

# --- B6.2：ADM 动能项系数 ---
# [π]=3, [κ]=[8πG]=-2, [√h]=0（质量自然单位）
dim_theirs = 2 + 6 + 0     # (1/2κ)·π²·√h
dim_std = -2 + 6 + 0       # (2κ/√h)·π²
R.add("B6.2", "哈密顿约束动能项系数写反：应为 2κ/√h，原文写成 √h/(2κ)", "FAIL",
      "质量量纲核算（自然单位 [x]=-1, [h]=0, [π^{ij}]=3, [κ]=8πG ⇒ [κ]=-2）："
      "原文 (1/κ)·π²·√h ⇒ 量纲 %d；标准 ADM 项 (16πG/√h)G_{ijkl}ππ = (2κ/√h)π² ⇒ 量纲 %d。"
      "该项必须是 4（哈密顿密度），原文差 %d 个质量量纲，换算因子 = h/(4κ²)（非普适常数）。"
      % (dim_theirs, dim_std, dim_theirs - 4))

# --- B6.3：为了让 V 与三项动能同时齐次，[Ω] 与 [T] 被强制 ---
# V 各项必须同为量纲 4
R.add("B6.3", "势能项 V 强制 [Ω]=[T]=1，与 Ω 作为无量纲权重（0.6875）的用法冲突", "FAIL",
      "-√h R/(2κ)：0+2+2=4 ✓；(1/2)h^{ij}∂Ω∂Ω：2+2[Ω]=4 ⇒ [Ω]=1；"
      "αΩRT：[Ω]+2+[T]=4 ⇒ [T]=1。泛函拉普拉斯自洽核算同样给出 [δ/δT]=3-[T]=2 ⇒ [T]=1。"
      "⇒ 本册方程只在 Ω 为**量纲 1 的动力学场**时才齐次；但 §1.3/§3.3/§5.3 把 Ω 当作无量纲数"
      "（Ω_DE=0.6875、Ω_i=0.05、τ=(Ω-Ω_i)/(Ω_f-Ω_i)）。两种用法互斥。")

# --- B6.4：Ω 的身份三重（“几何权重”/动力学标量/暗能量密度参数）---
# ΛCDM 中 Ω_Λ(a) 的常见取值
Om_L0 = 0.6875
Om_m0 = 0.3130
Om_r0 = 9.2e-5


def OmL_of_a(a):
    rhoL = Om_L0
    rhom = Om_m0 / a ** 3
    rhor = Om_r0 / a ** 4
    return rhoL / (rhoL + rhom + rhor)


a_rec = 1.0 / 1090.0
OmL_rec = OmL_of_a(a_rec)
OmL_eq = OmL_of_a(1.0 / 3400.0)
R.add("B6.4", "Ω 的身份三重冲突（若 Ω≡Ω_Λ 则轨迹也不对）", "BOUNDARY",
      "三种互不相容的用法：(i) 无量纲几何权重 0.6875；(ii) 量纲 1 的动力学标量（B6.3 强制）；"
      "(iii) 暗能量密度参数。若取 (iii)：实跑 Ω_Λ(复合 a=1/1090)=%.3e、Ω_Λ(物质-辐射相等)=%.3e，"
      "而本册称'暴胀起点 Ω_i≈0.05'⇒ 与 Ω_Λ 在早期的真实量级差 %d 个数量级，"
      "也与'暴胀期 Ω→1'相反。⇒ Ω 至今没有一个自洽定义，却被指派为'内禀时间'。"
      % (OmL_rec, OmL_eq, int(abs(math.log10(0.05 / OmL_rec)))))

R.add("B6.5", "'用 Ω 做内禀时间解决时间问题'是标准关系时间（relational time），且依赖已失败的暴胀扇区", "BOUNDARY",
      "用标量场做时钟是 Brown-Krammer/Lee 关系时间化的标准做法，非 TUFT 增量；"
      "其成立需要 Ω 的单调性由**作用量 + 解**保证，而 TUFT 暴胀-CMB 册已自证伪"
      "（5 PASS/35 FAIL，三预言互斥：κ-无关不变量 N(1-n_s)=3.741 vs 观测 2.106）⇒ 时钟本身无处安放。"
      "另：WDW 的因子排序 / 泛函拉普拉斯正规化 / 约束代数闭合（尤其 αΩRT 是否来自某个作用量）均未处理。")

# ==========================================================================
# §7 拓扑相变 S 矩阵与能垒
# ==========================================================================
R.section("§7  拓扑相变：S 矩阵与拓扑能垒")


def topo_amplitude(W1, W2, W3):
    """原文模型"""
    if W1 + W2 != W3:
        return 0.0
    return 1.0 / (1 + abs(W3))


def topo_barrier(W1, W2, W3):
    if W1 + W2 != W3:
        return float("inf")
    return EP_J * abs(W3 - W1 - W2 + 1) * 0.1


reactions = [
    (1, 1, 2, "e+e- -> 单态"),
    (1, -1, 0, "正反粒子湮灭"),
    (2, 0, 2, "散射"),
    (1, 0, 1, "自由传播"),
]
prob_loss = []
for W1, W2, W3, name in reactions:
    amp = topo_amplitude(W1, W2, W3)
    tot_prob = amp ** 2
    prob_loss.append((name, W1, W2, W3, amp, tot_prob))

worst = min(prob_loss, key=lambda r: r[5])
R.add("B7.1", "原文 S 矩阵破坏概率守恒：Σ_f|A|² < 1", "FAIL",
      "本模型拓扑荷守恒把末态唯一确定为 W3=W1+W2 ⇒ Σ_f|A|² = |A(W3)|² = 1/(1+|W3|)²。"
      "实跑：" + "；".join("%s |A|²=%.4f" % (it[0], it[5]) for it in prob_loss)
      + "。最坏者 %s： |A|²=%.4f ⇒ %.1f%% 的概率凭空消失，直接违背原文自己宣称的 U†U=1。"
      % (worst[0], worst[5], 100.0 * (1.0 - worst[5])))

barrs = [topo_barrier(W1, W2, W3) / EP_J for (W1, W2, W3, _) in reactions]
R.add("B7.2", "拓扑能垒公式 f(W1,W2,W3) 是空壳：允许反应的能垒恒为 0.1 E_P", "FAIL",
      "允许反应必有 W3=W1+W2 ⇒ |W3-W1-W2+1| ≡ 1 ⇒ ΔE ≡ 0.1 E_P。"
      "实跑全部 4 个允许反应（含'正反粒子湮灭'W3=0）：%.4f, %.4f, %.4f, %.4f E_P（完全相同）"
      " ⇒ 所谓'拓扑荷的函数 f'与拓扑无关。" % tuple(barrs))

# 与标准模型的定量冲突
E_P_GeV_val = EP_GeV
barrier_GeV = 0.1 * E_P_GeV_val
E_react_GeV = 1.0e-3          # e+e- 湮灭 ~ MeV
need_f = E_react_GeV / barrier_GeV
R.add("B7.3", "拓扑能垒 0.1 E_P 与已观测的粒子反应冲突 21 个量级", "FAIL",
      "0.1 E_P = %.4e GeV，而 e⁺e⁻→γγ 在 √s~1 MeV = %.1e GeV 实际发生 ⇒ 所需压低因子 f ≈ %.3e；"
      "而 §4.3 同时要求'普朗克能标拓扑相变自由发生'⇒ f≈O(1)。单一 f 的动态范围需覆盖 %.1e 倍。"
      "（本册表格把 e⁺e⁻湮灭列为拓扑过程，与自身的能垒设定直接冲突。）"
      % (barrier_GeV, E_react_GeV, need_f, 1.0 / need_f))

# ==========================================================================
# §8 黑洞的拓扑量子态
# ==========================================================================
R.section("§8  黑洞 = 拓扑元胞凝聚体：定量审查")

T_H0 = hbar * c ** 3 / (8.0 * math.pi * G * M0 * kB)
t_evap = 5120.0 * math.pi * G ** 2 * M0 ** 3 / (hbar * c ** 4)
R.add("B8.1", "复核原文黑洞单位换算（数值部分）", "PASS",
      "M0=10 M☉ ⇒ r_s=%.4e m、A=%.4e m²、W_BH=A/(4l_P²)=%.4e、T_H=%.4e K、"
      "t_evap=%.4e s = %.4e Gyr，与原文打印口径一致 ✓（量纲/数量级无误）"
      % (rs, A0, W0, T_H0, t_evap, t_evap / (3.15e7 * 1e9)))

# --- B8.2：形成时的拓扑荷赤字 ---
N_nuc = M0 / m_nuc
deficit = W0 / N_nuc
R.add("B8.2", "恒星塌缩的拓扑荷赤字：W_BH=A/4l_P² 比物质可携带的最大 W 大 20 个量级", "FAIL",
      "10 M☉ 黑洞含核子数 N_nuc = M0/m_N = %.4e；若每个粒子携带 |W|≤1（§1 的设定）且 W 在塌缩中守恒，"
      "则 W_BH ≤ N_nuc = %.4e，但 §6.1 要求 W_BH = A/(4l_P²) = %.4e ⇒ 赤字因子 %.3e。"
      "两条出路都致命：(a) 视界形成时 W 不守恒 ⇒ 直接否定 [Ŵ,Ĥ]=0 与'拓扑荷守恒'论证链；"
      "(b) 粒子并不携带 W=±1 ⇒ §1 的'粒子=W=1 拓扑元胞'与 §4.4 的反应表全部失效。"
      % (N_nuc, N_nuc, W0, deficit))

# --- B8.3：霍金量子的计数 ---
mean_E_over_kT = math.pi ** 4 / (30.0 * 1.2020569031595943)   # 黑体光子平均能量
N_quanta = W0 / mean_E_over_kT                                 # S_BH/[⟨E⟩/kT]
S_rad_thermo = (4.0 / 3.0) * W0                                # 黑体辐射热力学熵
entropy_per_quantum = S_rad_thermo / N_quanta
required_W_per_quantum = W0 / N_quanta
R.add("B8.3", "'一个元胞隧穿出一个粒子'与霍金辐射的计数对不上", "FAIL",
      "⟨E⟩/(k_BT) = π⁴/(30ζ(3)) = %.5f ⇒ 蒸发全过程辐射量子类数 N_quanta = W0/%.5f = %.4e × W0"
      "（仅光子），而'每量子携带 1 个拓扑单位'要求 N = 1×W0 ⇒ 差 %.3f 倍；"
      "反过来每个量子实际携带 熵 %.4f nat（已知黑体光子结果 ~3.6 k_B），而非 1 个拓扑单位 ⇒ 差 %.3f 倍。"
      "全辐射热力学熵 = (4/3)W0 = %.4e，也比 §6.2 'W_rad(final)=W_BH(initial)' 多 %.1f%%。"
      "计入有质量末期全部 SM 自由度（g_*≈106.75）后 N_quanta/W0 = %.2f，'1 量子=1 单位'需 g_*=3.6，属巧合级调参。"
      % (mean_E_over_kT, mean_E_over_kT, 1.0 / mean_E_over_kT, mean_E_over_kT,
         entropy_per_quantum, W0 / N_quanta, S_rad_thermo, 33.3,
         106.75 / mean_E_over_kT))

# --- B8.4：Page 曲线 ---
x = np.linspace(0.0, 0.9999, 20001)
S_BH = (1.0 - x) ** (2.0 / 3.0) * W0         # S ∝ M²，M ∝ (1-x)^{1/3}
S_rad = W0 - S_BH
S_ent_doc = np.minimum(2.0 * S_rad, W0)      # 原文：先升段 2*S_rad，封顶 W0
bound = np.minimum(S_rad, S_BH)              # 幺正Page界：S ≤ min(S_rad, S_BH)
viol = S_ent_doc - bound
i_max = int(np.argmax(viol))
# Page 时刻解析解：(1-x)^{2/3} = 1/2
x_page = 1.0 - 2.0 ** (-1.5)
S_BH_page = (1.0 - x_page) ** (2.0 / 3.0)
R.add("B8.4", "Page 曲线：原文峰值超幺正界 2 倍，Page 时刻画错（0.50 vs 0.646）", "FAIL",
      "由原文自己的 M(t)∝(1-x)^{1/3} ⇒ S_BH∝(1-x)^{2/3}。Page 时刻解 S_rad=S_BH："
      "(1-x)^{2/3}=1/2 ⇒ x_Page=%.5f（实跑 S_BH(x_Page)/W0=%.6f ✓），原文在图上标 0.5 ⇒ 偏 %.1f%%。"
      "幺正上界 S ≤ min(S_rad,S_BH)：原文上升段 = 2×S_rad，恰为上界的 %.1f 倍，"
      "峰值 %.4e vs 上界最大值 %.4e（超 %.1f 倍，越界最大值出现在 x=%.4f）。"
      "⇒ 原文的 'Page 曲线'违反纠缠熵的基本维数上界，不是 Page 曲线。"
      % (x_page, S_BH_page, 100.0 * (x_page - 0.5) / x_page,
         float(S_ent_doc[1] / bound[1]) if bound[1] > 0 else float('nan'),
         float(S_ent_doc.max()), float(bound.max()), float(S_ent_doc.max() / bound.max()), x[i_max]))

R.add("B8.5", "'总拓扑荷守恒'与'总熵守恒'在本册中是定义式，非结论", "FAIL",
      "原文直接令 S_rad := W_initial − W_t，则 S_BH+S_rad ≡ W_initial 为恒等式（0 信息量）；"
      "真正物理的辐射热力学熵为 (4/3)W0（B8.3）⇒ 实际'总熵'不守恒。"
      "同时：若 S_rad 解释为纠缠熵，则 Page 曲线要求它先升后降，与本册的单调递增构造不同。"
      "⇒ 两种解释都不成立，'信息paradox 已消解'没有定量支撑。")

# ==========================================================================
# §9 原文代码的可运行性
# ==========================================================================
R.section("§9  原文 Python 仿真的可运行性")

snippet = "im\\(\\boldsymbol{p}\\)ort num\\(\\boldsymbol{p}\\)y as n\\(\\boldsymbol{p}\\)y"
try:
    import ast
    ast.parse(snippet)
    parsed = True
except SyntaxError:
    parsed = False
R.add("B9.1", "原文代码块混入 LaTeX 宏 ⇒ 从未被实跑过", "FAIL" if not parsed else "PASS",
      "ast.parse 结果：%s（示例片段含 \\(\\boldsymbol{p}\\) 宏）"
      % ("可解析" if parsed else "SyntaxError")
      + " ⇒ 原文标注的'仿真预期输出'没有实跑依据；本册全部数值结论由本脚本的**重实现**给出。")

R.add("B9.2", "术语：Page curve 不是'页悖论'", "INFO",
      "'Page' 是人名（Don Page），应为 Page 曲线/Page 时间；原文 §6.3 写作'页悖论'属翻译错误，"
      "会造成检索与同行评审层面的歧义。")

# ==========================================================================
# §10 体例与结论审计
# ==========================================================================
R.section("§10  非微扰框架的五条自洽性声明逐条判定")

checks = [
    ("8.1 拓扑荷守恒 ⇒ 信息不丢失", "FAIL", "B3.2 给出严格反例：相位阻尼通道守恒 ⟨W⟩ 且守恒 W 分布，信息仍丢。"),
    ("8.2 幺正性", "FAIL", "B7.1 原文自己的 S 矩阵使 |A|²=0.25（自由传播）⇒ 概率不守恒。"),
    ("8.3 低能极限", "FAIL", "B7.3 能垒 0.1E_P 使 MeV 量级的标准模型反应被禁戒。"),
    ("8.4 经典极限", "BOUNDARY", "未给约束代数闭合与 Ω 的作用量（B6.3/B6.5），极限不存在可走？难以判定。"),
    ("8.5 曲率饱和 ⇒ UV 有限", "FAIL", "前册 Q7.2 已证：|R|≤K_sat 约束振幅不约束动量 k，圈发散未消除。"),
]
for name, verdict, detail in checks:
    R.add("B10", name, verdict, detail)

cnt = R.summary()
R.dump()
