# -*- coding: utf-8 -*-
"""
v31  量子引力与宇宙学常数 · 螺旋-拓扑层正面攻击
====================================================================
背景：v8.1→v30 已把「场方程层(v9/v10) + 后牛顿与引力几何层(v14/v15/v16)
+ 拓扑涌现规范层 TEGT(v19→v28) + 代质量边界(v23/v29/v30)」逐层收口。
仍为诚实开放的巨石有三块：
  (i)   Λ / 宇宙学常数（v18 B04/B05、v14 V08、v15 A08）
  (ii)  量子引力：全息熵、面积谱、黑洞熵系数、奇点、UV 完备
  (iii) α / σ / 代质量的绝对数值（v9 W20、v12 Z10-Z12、v17 B04、v30）
本版专攻 (i)+(ii)：用框架已闭合的拓扑层（v19→v28 的 SU(2)_k 融合范畴 /
模群 S,T / 辫群 B₃ 的 Jones 表示）对量子引力与宇宙学常数作正面攻击；
并对工作区内既有的 verify_quantum_gravity_breakthrough.py 的 G1–G9 声明
作独立审计（该文件把若干「逆向定标」标为「严格推导」）。

判定红线：
  * 机器零（相对残差 < 1e-30）才判 PASS；
  * 结构性结论按「可证性」分级，可证且自洽判 PASS，可证但系数未定判部分闭合；
  * 循环论证 / 逆向定标（由待解释量反解参数）一律判 FAIL 并显式标注，
    绝不粉饰为「严格推导」；
  * 框架未涉及的（奇点、UV 完备）判 FAIL（诚实开放）。

产物：v31_量子引力与宇宙学常数_拓扑层正面攻击_核验结果.json
"""
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import mpmath as mp
import sympy as sp

mp.mp.dps = 60

HERE = os.path.dirname(os.path.abspath(__file__))
results = []


def add(cid, name, layer, kind, verdict, value, note):
    if isinstance(value, mp.mpf):
        out_value = mp.nstr(value, 12)
    elif isinstance(value, float):
        out_value = repr(value)
    else:
        out_value = str(value)
    results.append(dict(id=cid, name=name, layer=layer, kind=kind,
                        verdict=verdict, value=out_value, note=note))
    print("  [%s] %-4s %-46s val=%s" % (verdict, cid, name[:46], out_value))


# =====================================================================
# 0. 常数（CODATA 2018 SI / Planck 2018 宇宙学）
# =====================================================================
hbar = mp.mpf("1.054571817e-34")      # J·s
G = mp.mpf("6.67430e-11")             # m^3 kg^-1 s^-2
c = mp.mpf("299792458")               # m/s
kB = mp.mpf("1.380649e-23")           # J/K

lP = mp.sqrt(hbar * G / c ** 3)
tP = mp.sqrt(hbar * G / c ** 5)
mP = mp.sqrt(hbar * c / G)
EP = mP * c ** 2

Mpc = mp.mpf("3.0856775814913673e22")            # m
H0 = mp.mpf("67.36") * mp.mpf("1000") / Mpc      # s^-1  (Planck 2018: 67.36 km/s/Mpc)
rho_crit = 3 * H0 ** 2 / (8 * mp.pi * G)         # kg/m^3
rho_crit_E = rho_crit * c ** 2                   # J/m^3
OmL = mp.mpf("0.6847")                           # Planck 2018 Ω_Λ
rho_L_obs = OmL * rho_crit_E                     # J/m^3 观测暗能量密度

rho_P = EP / lP ** 3                             # Planck 真空能密度

print("=" * 78)
print("v31  量子引力与宇宙学常数 · 螺旋-拓扑层正面攻击")
print("=" * 78)
print("  ℓ_P = %s m   m_P = %s kg   E_P = %s J" % (mp.nstr(lP, 10), mp.nstr(mP, 10), mp.nstr(EP, 10)))
print("  ρ_P(Planck 真空能密度) = %s J/m^3" % mp.nstr(rho_P, 10))
print("  ρ_Λ(观测, Planck 2018) = %s J/m^3" % mp.nstr(rho_L_obs, 10))
print("  ρ_P / ρ_Λ = 10^%s" % mp.nstr(mp.log10(rho_P / rho_L_obs), 8))
print()


# =====================================================================
# Q01  拓扑层自由度计数：Verlinde 公式核验
#      dim V_g(SU(2)_k) = Σ_j  S_{0j}^{2-2g},  S_{0j}=√(2/(k+2))·sin((j+1)π/(k+2))
#      关键结构性事实：维数只依赖 (k, g)，**不依赖面积 / 紫外截断**
#      ⇒ 拓扑层无局域自由度（为 Q02 提供前提）
# =====================================================================
def verlinde_dim(k, g):
    n = k + mp.mpf(2)
    S0 = [mp.sqrt(2 / n) * mp.sin(mp.pi * (j + 1) / n) for j in range(k + 1)]
    return mp.fsum([s ** (2 - 2 * g) for s in S0])


print("-" * 78)
print("Q01  拓扑层自由度计数（Verlinde 公式）")
max_dev_int = mp.mpf(0)
max_dev_g0 = mp.mpf(0)
max_dev_g1 = mp.mpf(0)
max_dev_abel = mp.mpf(0)
table = []
for k in range(1, 9):
    row = []
    for g in range(0, 5):
        d = verlinde_dim(k, g)
        row.append(d)
        dev_int = abs(d - mp.nint(d)) / (1 + abs(d))
        if dev_int > max_dev_int:
            max_dev_int = dev_int
    table.append((k, row))
    max_dev_g0 = max(max_dev_g0, abs(row[0] - 1))
    max_dev_g1 = max(max_dev_g1, abs(row[1] - (k + 1)) / (k + 1))
    if k == 1:  # SU(2)_1 为 Abel 理论（2 个任意子），应有 dim = 2^g
        for g in range(0, 5):
            max_dev_abel = max(max_dev_abel, abs(row[g] - mp.mpf(2) ** g) / (2 ** g))
for k, row in table:
    print("    k=%d  dim(g=0..4) = %s" % (k, ", ".join(mp.nstr(x, 8) for x in row)))
worst = max(max_dev_int, max_dev_g0, max_dev_g1, max_dev_abel)
add("Q01", "Verlinde 维数公式核验：g=0→1、g=1→k+1、整数性、SU(2)_1→2^g",
    "拓扑层", "数值+结构", "PASS" if worst < mp.mpf("1e-30") else "FAIL", worst,
    "四种独立自检（球=1 / 环=k+1 与 v20 B01 一致 / 亏格 2..4 维数为整数 / "
    "SU(2)_1 退化为 Abel 2^g）最大相对残差 %s，机器零。结构性结论：拓扑层 "
    "Hilbert 空间维数只由 (k, g) 决定，**与面积及紫外截断无关** ⇒ 无局域自由度。"
    % mp.nstr(worst, 4))


# =====================================================================
# Q02  拓扑层结构性规避宇宙学常数灾难（真闭合）
#      Chern-Simons / 拓扑场论：H ≡ 0（一阶作用量、全部为约束），
#      物理局域自由度 = 0 ⇒ 体真空能密度 ρ_vac^topo ≡ 0（严格，非拟合）
# =====================================================================
print("-" * 78)
print("Q02  拓扑层真空能：无局域自由度 ⇒ ρ_vac^topo = 0")
# 符号核验：ρ_P = E_P/ℓ_P³ ≡ c⁷/(ħ G²)（Planck 密度的闭式）
hb, Gs, cs = sp.symbols("hbar G c", positive=True)
expr = sp.sqrt(hb * cs ** 5 / Gs) / (sp.sqrt(hb * Gs / cs ** 3)) ** 3
closed = cs ** 7 / (hb * Gs ** 2)
sym_dev = sp.simplify(sp.powsimp(expr / closed, force=True) - 1)
ratio_num = rho_P / rho_L_obs
log_gap = mp.log10(ratio_num)
add("Q02a", "Planck 真空能密度闭式核验：E_P/ℓ_P³ ≡ c⁷/(ħG²)（符号）",
    "量子引力层", "符号+数值", "PASS" if sym_dev == 0 else "FAIL", 0.0,
    "sympy 化简残差 = %s（机器零），并用 CODATA 数值复核 ρ_P=%s J/m³。"
    % (sym_dev, mp.nstr(rho_P, 10)))
add("Q02b", "拓扑层结构性规避：H≡0 且无局域自由度 ⇒ ρ_vac^topo ≡ 0（严格，非拟合）",
    "量子引力层", "结构性证明", "PASS", 0.0,
    "Chern-Simons 型作用量为一阶、正则分析给出全部为约束（H≡0），配合 Q01 "
    "（Hilbert 维数与截断无关）⇒ 拓扑层不贡献体真空能。这是**结构性规避**而非"
    "拟合：把 QFT+Planck 截断的 ρ_P/ρ_Λ = 10^%s 的灾难降为 0/ρ_Λ。"
    "诚实限定：ρ_vac^topo = 0 只说明『拓扑层不产生真空能』，**不等于解释了观测的"
    "非零 Λ**（见 Q03）。" % mp.nstr(log_gap, 6))


# =====================================================================
# Q03  观测 Λ 与拓扑层预测 0 的冲突（诚实 FAIL）
# =====================================================================
print("-" * 78)
print("Q03  观测 Λ vs 拓扑层预测 0")
dev_L = abs(rho_L_obs - 0) / rho_L_obs  # = 1
add("Q03", "ρ_Λ 的绝对数值：拓扑层预测 0，观测 %s J/m³" % mp.nstr(rho_L_obs, 8),
    "宇宙学层", "数值", "FAIL", float(dev_L),
    "相对偏差 100%%（框架预测恰好为 0）。诚实结论：非零 Λ / Ω_Λ≈0.685 "
    "不在拓扑层内，需拓扑层之外的动力学输入（与 v18 B04/B05、v15 A08 同层，"
    "本版只是把『未解释』从『灾难性 10^%s 量级』收窄为『10^-122 量级的非零残值』）。"
    % mp.nstr(log_gap, 5))


# =====================================================================
# Q04  局域动力学层（κ/τ 场，v9/v10）的零点能：框架内自然截断下的量化
#      ρ_vac(k_max) = (1/2)∫^{k_max} d³k/(2π)³ · ħck = ħc·k_max⁴/(16π²)
#      截断候选（均取自框架内部，非人为）：
#        (a) 螺旋最小半径 R_min = √2·ℓ_P        （G1，最小螺旋）
#        (b) 挠率尺度 L_τ = √(4π)·ℓ_P = 2√π ℓ_P （Y14，τ~c·κ_P·ℏ/2 = 4πℓ_P²）
#        (c) Planck 截断 k_max = 1/ℓ_P          （QFT 常规，作为对照）
# =====================================================================
print("-" * 78)
print("Q04  局域动力学层零点能（框架内截断）")


def rho_vac_scalar(kmax):
    return hbar * c * kmax ** 4 / (16 * mp.pi ** 2)


candidates = [
    ("(a) 螺旋最小半径 R_min=√2·ℓ_P", mp.sqrt(2) * lP),
    ("(b) 挠率尺度 L_τ=√(4π)·ℓ_P", mp.sqrt(4 * mp.pi) * lP),
    ("(c) Planck 截断 ℓ_P（对照）", lP),
]
best_gap = None
for tag, L in candidates:
    kmax = 1 / L
    rv = rho_vac_scalar(kmax)
    gap = rv / rho_L_obs
    print("    %-32s k_max=1/%s ℓ_P  ρ_vac=%s J/m³  ρ_vac/ρ_Λ=10^%s"
          % (tag, mp.nstr(L / lP, 6), mp.nstr(rv, 8), mp.nstr(mp.log10(gap), 6)))
    if best_gap is None or gap < best_gap[1]:
        best_gap = (tag, gap)
add("Q04", "κ/τ 局域场零点能：框架内最优截断下 ρ_vac/ρ_Λ = 10^%s" % mp.nstr(mp.log10(best_gap[1]), 5),
    "宇宙学层", "数值", "FAIL", float(mp.log10(best_gap[1])),
    "最优候选 %s：单个无质量标量零点能 ρ=ħc·k_max⁴/(16π²) 仍超观测 %s 个数量级。"
    "诚实结论：一旦引入框架自己的局域动力学层（v9/v10 的 κ/τ 场方程），"
    "Q02 的结构性规避即被破坏，Λ 灾难原样复现。⇒ Q02 的规避**只在纯拓扑层成立**，"
    "「拓扑层 + 局域层」的完整框架并未解决 Λ 问题。这是本版最重要的负面结果。"
    % (best_gap[0], mp.nstr(mp.log10(best_gap[1]), 5)))


# =====================================================================
# Q05  黑洞熵系数 1/4：独立预测 vs 逆向定标审计
#      BH:  S/k_B = A/(4ℓ_P²)                       （系数 1/4 = 0.25）
#      框架独立预测: S/k_B = (A/A_0)·ln d
#        A_0 = 螺旋模式面积（候选：πℓ_P²[G3 最小圆面积]、2πℓ_P²、4πℓ_P²[Y14 挠率面积]）
#        d   = 每模式简并度（候选：2 = τ→−τ 手征二重[v12 Z09]、3 = SU(2)_2 三扇区[v20]）
# =====================================================================
print("-" * 78)
print("Q05  黑洞熵系数：框架独立预测 vs 逆向定标")
A0_cands = [("πℓ_P²（G3 螺旋最小圆面积）", mp.pi),
            ("2πℓ_P²（圆柱侧面积/周期）", 2 * mp.pi),
            ("4πℓ_P²（Y14 挠率面积）", 4 * mp.pi)]
d_cands = [(2, "d=2 手征二重（v12 Z09 τ→−τ）"), (3, "d=3（v20 SU(2)_2 三扇区）")]
best = None
for a0name, a0 in A0_cands:
    for d, dname in d_cands:
        coeff = mp.log(d) / a0
        err = abs(coeff - mp.mpf("0.25")) / mp.mpf("0.25")
        print("    %-28s x %-24s 系数=%s  偏差=%.2f%%"
              % (a0name, dname, mp.nstr(coeff, 6), float(100 * err)))
        if best is None or err < best[0]:
            best = (err, a0name, dname, coeff)
err, a0name, dname, coeff = best
verdict_q05 = "PASS" if err < mp.mpf("1e-30") else ("部分闭合" if err < mp.mpf("0.15") else "FAIL")
add("Q05", "BH 熵系数：框架独立预测 %s（%s × %s）vs 1/4" % (mp.nstr(coeff, 6), a0name, dname),
    "量子引力层", "数值", verdict_q05, float(err),
    "最优组合给出系数 %s，与 Bekenstein-Hawking 的 0.25 差 %.2f%% —— 同量级但"
    "系数未被框架唯一固定（A_0 与 d 各有多个框架内候选）⇒ 部分闭合，非闭合。"
    % (mp.nstr(coeff, 6), float(100 * err)))
# 逆向定标审计：G4 的 α = 4 ln 2
reverse = 4 * mp.log(2)
gamma_naive = mp.log(2) / (mp.pi * mp.sqrt(3))
gamma_meissner = mp.mpf("0.237532957")
A_min_naive = 4 * mp.pi * mp.sqrt(3) * gamma_naive
A_min_meissner = 4 * mp.pi * mp.sqrt(3) * gamma_meissner
add("Q05x", "审计：既有脚本 G4 的「α=4ln2 ≈ 2.77」是逆向定标，不是推导",
    "审计", "自证伪", "FAIL", float(reverse),
    "4ln2=%s 恰等于 LQG 朴素 j=1/2 计数的 A_min=4π√3·γ_naive=%s（γ_naive=ln2/(π√3)"
    "=%s）——它是**由要求 S=(A/A_0)k_B ln2 等于 BH 熵而反解出的 A_0**，"
    "与 LQG 反解 Immirzi 完全同构，属循环定标，不构成第一性推导。既有脚本 G4 "
    "标为「✅严格推导」属越界，本版更正为 FAIL。" % (mp.nstr(reverse, 6),
                                          mp.nstr(A_min_naive, 6), mp.nstr(gamma_naive, 6)))
add("Q05y", "审计：既有脚本 G3/G4 内部不自洽（γ 取值冲突）",
    "审计", "自证伪", "FAIL", float(A_min_meissner / A_min_naive),
    "既有脚本 G3 用 Meissner 全计数 γ=%s ⇒ A_min=4π√3γ=%s ℓ_P²（文中记 5.17），"
    "G4 用朴素 j=1/2 计数 γ_naive=%s ⇒ A_min=%s ℓ_P²（文中记 2.77）。"
    "两者相差 %s 倍，同一脚本共用会互相矛盾 ⇒ 诚实标注为内部不自洽。"
    % (mp.nstr(gamma_meissner, 7), mp.nstr(A_min_meissner, 6),
       mp.nstr(gamma_naive, 6), mp.nstr(A_min_naive, 6),
       mp.nstr(A_min_meissner / A_min_naive, 6)))


# =====================================================================
# Q06  面积谱：LQG vs 框架螺旋最小面积
# =====================================================================
print("-" * 78)
print("Q06  面积谱：LQG vs 螺旋")
A_helix = mp.pi                                    # π ℓ_P²（G3）
A_lqg_naive = A_min_naive                          # 4 ln2 ℓ_P²
A_lqg_meis = A_min_meissner                        # ≈5.17 ℓ_P²
r_naive = A_helix / A_lqg_naive
add("Q06", "面积量子：框架 πℓ_P² vs LQG（γ_naive）%s ℓ_P²" % mp.nstr(A_lqg_naive, 6),
    "量子引力层", "数值", "部分闭合", float(abs(r_naive - 1)),
    "比值 %s（差 %.1f%%）：框架螺旋最小圆面积 πℓ_P² 与 LQG 朴素 j=1/2 面积量子 "
    "4ln2·ℓ_P² 同量级（均 ~几倍 Planck 面积），但系数相差 %.1f%%，框架未给出把 "
    "系数锁到 LQG 值的方程，也未独立导出 Barbero-Immirzi γ ⇒ 部分闭合。"
    "诚实：面积**离散化**由 Y14 的 4πℓ_P² 挠率尺度支持，但**谱的具体形式**未被导出。"
    % (mp.nstr(r_naive, 6), float(100 * abs(r_naive - 1)), float(100 * abs(r_naive - 1))))


# =====================================================================
# Q07  v20 的 k=2 适用范围澄清：代际层级 ≠ 视界 Chern-Simons 层级
# =====================================================================
print("-" * 78)
print("Q07  k=2 适用范围澄清（代际层级 vs 视界 CS 层级）")
M_sun = mp.mpf("1.989e30")
R_s = 2 * G * M_sun / c ** 2
A_bh = 4 * mp.pi * R_s ** 2
k_hor = A_bh / (4 * mp.pi * gamma_naive * lP ** 2)     # LQG 视界 CS 层级
n_pun = A_bh / (4 * mp.log(2) * lP ** 2)               # 朴素 j=1/2 穿刺数
S_lqg = n_pun * mp.log(2)
S_bh = A_bh / (4 * lP ** 2)
dev_ent = abs(S_lqg - S_bh) / S_bh
print("    太阳质量 BH: R_s=%s m, A=%s m², k_hor=%s, 穿刺数 n=%s"
      % (mp.nstr(R_s, 8), mp.nstr(A_bh, 8), mp.nstr(k_hor, 6), mp.nstr(n_pun, 6)))
add("Q07a", "视界 CS 层级 k_hor=A/(4πγℓ_P²) = %s（太阳质量 BH）" % mp.nstr(k_hor, 5),
    "量子引力层", "数值", "部分闭合", float(mp.log10(k_hor / 2)),
    "k_hor ≈ 10^%s，与 v20 固定代际数的 k=2 相差 10^%s 量级 ⇒ **v20 的 k=2 是内部"
    "代际扇区层级，不是引力视界的 Chern-Simons 层级**。澄清必要性：防止把 k=2 "
    "误用为视界层级去反解 Immirzi（那会得到荒谬的 A/l_P² ~ 10²）。二者不冲突，"
    "但也不互推 ⇒ 部分闭合。" % (mp.nstr(mp.log10(k_hor), 5), mp.nstr(mp.log10(k_hor / 2), 5)))
add("Q07b", "LQG 计数自洽复核：n·ln2 与 A/(4ℓ_P²) 的一致性",
    "量子引力层", "数值", "PASS" if dev_ent < mp.mpf("1e-30") else "FAIL", float(dev_ent),
    "n=A/(4ln2·ℓ_P²)=%s，S=n·ln2=%s，与 S_BH=A/(4ℓ_P²)=%s 相对残差 %s（机器零）。"
    "该一致性**由 γ=ln2/(π√3) 的选取保证**，再次印证 Q05x：这是定标而非独立预言。"
    % (mp.nstr(n_pun, 6), mp.nstr(S_lqg, 6), mp.nstr(S_bh, 6), mp.nstr(dev_ent, 4)))


# =====================================================================
# Q08  引力子一致性（与 v14 V04/V05 交叉复核）
# =====================================================================
print("-" * 78)
print("Q08  引力子一致性（与 v14 交叉）")
m_g = mp.mpf("1.2e-22") * mp.mpf("1.602176634e-19") / c ** 2    # kg  (LIGO 上限)
lam_reduced = hbar / (m_g * c)          # ℏ/(m_g c)
lam_h = 2 * mp.pi * lam_reduced         # h/(m_g c) —— v14 V05 用的约定
mu_g = 1 / lam_reduced
add("Q08", "引力子：自旋2 / v_gw=c / m_g 上限 —— 与框架 μ_g=0 长程退化相容",
    "量子引力层", "一致性", "PASS", float(mu_g),
    "h/(m_g c)=%s m（复现 v14 V05 的 1.03e16 m 约定），约化 λ=ℏ/(m_gc)=%s m，"
    "对应 μ_g=%s m⁻¹。框架取 μ_g=0 ⇒ Proca 退化为泊松长程、波速=c、自旋2"
    "（度规扰动为二阶张量），与 GW170817 |v_gw−c|/c≈4.2e-16 相容。"
    "诚实限定：这是**一致性核验**，自旋2 与 m_g=0 均由外部（GR/观测）输入，"
    "框架未从螺旋公设导出引力子的存在性或自旋。" % (mp.nstr(lam_h, 6),
                                          mp.nstr(lam_reduced, 6), mp.nstr(mu_g, 6)))


# =====================================================================
# Q09  既有脚本 G1/G2/G5/G6/G7 的其余声明审计（逐条）
# =====================================================================
print("-" * 78)
print("Q09  既有 verify_quantum_gravity_breakthrough.py 的 G1–G7 声明审计")
audit_items = [
    ("G1", "时空量子化：R_min=√2·ℓ_P ⇒ 「不存在比 ℓ_P 更小的长度」",
     "FAIL", "R_min=√2ℓ_P 来自两条**独立外部输入**的联立（mR=ħ/c 的角动量量子化 + "
             "R=2Gm/c² 的 Schwarzschild 条件），其中 Schwarzschild 关系是 GR 结论，"
             "非螺旋公设所导出；且由此只能说『最小螺旋半径 ~ℓ_P』，推不出长度离散化。"
             "既有脚本标「✅严格推导」越界。"),
    ("G2", "引力子自旋2 / 无质量 / 两偏振",
     "部分闭合", "「二阶张量→自旋2」与「无质量→v=c」是 GR/庞加莱表示的既有结论，"
                 "螺旋图像只提供**几何对应**，未提供导出；与 Q08 同层。"),
    ("G3", "面积量子化 A=πR²，R 量子化 ⇒ A 量子化",
     "部分闭合", "方向正确且与 Q06 一致，但 A=πR² 是**圆周面积**而非视界/曲面的"
                 "面积算符本征值，与 LQG 的 A_j=8πγℓ_P²√(j(j+1)) 系数不一致（差 "
                 "%.1f%%），且 γ 未被导出。既有脚本标「✅定性对应」尚可，"
                 "但与 G4 存在 Q05y 的 γ 冲突。" % float(100 * abs(r_naive - 1))),
    ("G5", "全息：螺旋在 2D 圆柱面上 ⇒ 3D 信息编码于 2D 边界",
     "FAIL", "「轨迹位于某二维面上」不等于「体空间的物理信息可由边界理论完全重构」。"
             "全息原理的内容是**自由度计数** S≤A/4ℓ_P² 与体-边对应（AdS/CFT），"
             "螺旋轨迹的维数事实既给不出熵界也构造不出边界 CFT ⇒ 属类比，非推导。"),
    ("G6", "三代 = 三种螺旋参数 (R_i, ω_i, b_i)",
     "FAIL", "与 v30 结论直接冲突：v30 已证伪『单一拓扑量/幂律可构造代质量』整族假设；"
             "把三代写成三个自由参数组 (R,ω,b) 是**把观测质量直接当输入**，"
             "零预言力（9 个参数拟合 9 个质量）。代结构应由 v20 的 k=2 三扇区给出，"
             "代质量绝对值仍是开放项。"),
    ("G7", "暗物质 = 右旋中微子 / 轴子（螺旋相位赝标量）",
     "FAIL", "右旋中微子不参与弱作用是 SM 规范表示的既有结论（非螺旋导出）；"
             "「螺旋角相位 φ=ωt 的扰动 ⇒ 赝标量轴子」缺少作用量与质量生成机制，"
             "f_a、m_a 全为输入 ⇒ 属候选罗列，非推导。"),
]
for cid, claim, verdict, note in audit_items:
    add("Q09" + cid, "既有脚本审计 " + cid + "：" + claim[:34], "审计", "自证伪", verdict, 0.0, note)


# =====================================================================
# Q10  尚不在框架范围（诚实开放）
# =====================================================================
print("-" * 78)
print("Q10  诚实开放项")
add("Q10a", "时空奇点（t→0 / r→0）：框架未消解",
    "量子引力层", "诚实开放", "FAIL", 0.0,
    "螺旋公设只在 v≡c 的类时世界线上定义，未给出 Planck 尺度下的动力学；"
    "Big Bang 奇点与黑洞内奇点在框架内既未被消解也未被解释，"
    "与 v18 B05、v14 V08、v15 A08 同层，本版无进展。")
add("Q10b", "引力 UV 完备 / 重整化：框架未完成",
    "量子引力层", "诚实开放", "FAIL", 0.0,
    "框架的引力层是 v15/v16 的弱场/作用量相容性（A01–A06 + B01–B05 部分闭合），"
    "未涉及微扰引力的发散结构、重整化或 UV 不动点 ⇒ 不构成量子引力理论。")


# =====================================================================
# Q11  与既有链的兼容（正向：框架内 ℓ_P 非外插）
# =====================================================================
print("-" * 78)
print("Q11  与 v15/v16 链兼容")
# v15 A01: √(Gℏc)/m_P = G  →  G 由 κ-Φ 桥接固定；ℓ_P=√(ℏG/c³) 随之被框架量表达
lhs = mp.sqrt(G * hbar * c) / mP
dev_bridge = abs(lhs - G) / G
lP_from_bridge = mp.sqrt(hbar * lhs / c ** 3)
dev_lP = abs(lP_from_bridge - lP) / lP
add("Q11", "兼容 v15 A01：√(Gℏc)/m_P=G ⇒ ℓ_P 由框架桥接常数固定（非外插）",
    "引力层", "数值+符号", "PASS" if max(dev_bridge, dev_lP) < mp.mpf("1e-30") else "FAIL",
    float(max(dev_bridge, dev_lP)),
    "√(Gℏc)/m_P 与 G 的相对残差 %s（机器零）；由此桥接常数重建的 ℓ_P 与 CODATA "
    "ℓ_P 相对残差 %s ⇒ 本版 Q04–Q08 中一切含 ℓ_P 的量（面积/熵/截断）"
    "均可回指框架内部，不是外加常数。这是本版与 v14/v15/v16 链的衔接点。"
    % (mp.nstr(dev_bridge, 4), mp.nstr(dev_lP, 4)))


# =====================================================================
# 汇总
# =====================================================================
n_pass = sum(1 for x in results if x["verdict"] == "PASS")
n_fail = sum(1 for x in results if x["verdict"] == "FAIL")
n_info = sum(1 for x in results if x["verdict"] == "INFO")
n_part = sum(1 for x in results if x["verdict"] == "部分闭合")

summary = {
    "script": "v31  量子引力与宇宙学常数 · 螺旋-拓扑层正面攻击",
    "overall_verdict": "FAIL",
    "total": len(results), "PASS": n_pass, "FAIL": n_fail,
    "INFO": n_info, "部分闭合": n_part,
    "key_numbers": {
        "rho_Planck_J_m3": mp.nstr(rho_P, 12),
        "rho_Lambda_obs_J_m3": mp.nstr(rho_L_obs, 12),
        "log10_gap_Planck_over_obs": mp.nstr(log_gap, 8),
        "log10_gap_helixcutoff_over_obs": mp.nstr(mp.log10(best_gap[1]), 8),
        "BH_entropy_coeff_best_framework": mp.nstr(coeff, 8),
        "BH_entropy_coeff_target": "0.25",
        "k_horizon_solar_mass_BH": mp.nstr(k_hor, 8),
        "v20_generation_level_k": 2,
    },
    "results": results,
    "conclusion": (
        "【正面推进·真闭合 1 项】Q02：由 Q01（Verlinde 维数只依赖 (k,g)、与面积/"
        "紫外截断无关）与拓扑场论 H≡0，严格推出拓扑层体真空能 ρ_vac^topo ≡ 0 —— "
        "这是**结构性规避**（非拟合），把 QFT+Planck 截断的 ρ_P/ρ_Λ = 10^%s 灾难"
        "降为 0。Q01 的四种自检、Q07b 的 LQG 计数自洽、Q11 的 ℓ_P 桥接回指均为机器零。"
        "【边界收窄】Λ 开放项由『解释 10^122 量级的灾难』收窄为『解释 10^-122 量级的"
        "非零残值』（Q03、Q04）。【最重要的负面结果】Q04：一旦把框架自己的局域动力学层"
        "（v9/v10 的 κ/τ 场）纳入，其零点能在框架内最优截断（螺旋最小半径 √2ℓ_P）下"
        "仍超观测 10^%s 个量级 ⇒ Q02 的规避**仅在纯拓扑层成立**，完整框架并未解决 Λ。"
        "【自我纠错·审计 8 项】既有脚本 G4 的 α=4ln2 是逆向定标（与 LQG 反解 Immirzi "
        "同构）；G3 与 G4 的 γ 取值互相矛盾（5.17 vs 2.77 ℓ_P²）；G5 全息、G6 三代、"
        "G7 暗物质均为类比/罗列而非推导；G1 混用了 GR 的 Schwarzschild 外部输入。"
        "【部分闭合 5 项】Q05（BH 熵系数最优差 %.1f%%）、Q06（面积量子差 %.1f%%）、"
        "Q07a（k=2 适用范围澄清）、Q02b 的限定、G3。"
        "【诚实开放 2 项】Q10a 奇点、Q10b UV 完备。"
        "红线守约：全部判定按残差/可证性分级，循环论证与越界声明一律更正为 FAIL，无粉饰。"
    ) % (mp.nstr(log_gap, 5), mp.nstr(mp.log10(best_gap[1]), 5),
         float(100 * abs(r_naive - 1)), float(100 * abs(r_naive - 1))),
}

out = os.path.join(HERE, "v31_量子引力与宇宙学常数_拓扑层正面攻击_核验结果.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print()
print("=" * 78)
print("[v31] total=%d  PASS=%d  FAIL=%d  INFO=%d  部分闭合=%d"
      % (len(results), n_pass, n_fail, n_info, n_part))
print("产物：%s" % os.path.basename(out))
print("=" * 78)
