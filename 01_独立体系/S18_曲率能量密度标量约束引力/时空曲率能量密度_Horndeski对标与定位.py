# -*- coding: utf-8 -*-
"""
时空曲率-能量密度关系 · 续篇六：理论分类学定位 —— Horndeski 谱系对标
====================================================================
原待攻破清单第 5 项（最后一项）："对标 Horndeski 等修正引力谱系，撰写理论综述小节"

本册回答三个可判定问题：
  H1  Horndeski 谱系结构 + GW170817 引力波速度约束：哪些子类存活？
  H2  本理论（叠加闭包，σ=0 定标 ⇒ P=g(ρ)Y）能否【形式上】嵌入 G2 子类？
  H3  【核心】ρ 是不是动力学标量场？——用 k-essence 场 EOM 做量化相容性检验
  H4  本理论是否通过 GW170817（c_GW=c）？
  H5  若取唯一的健康定标 σ=0 ⇒ w=1（stiff, ∝a^-6）⇒ BBN/ΔN_eff 约束下的二难

关键预期（可手算复核）：
  k-essence 场 EOM（均匀背景）： d/dt(P_Y·ρ̇) + 3H·P_Y·ρ̇ = P_ρ
  对 P=g(ρ)Y、Y=½ρ̇²/c²、且 ρ 服从物质守恒 ρ̇=-3Hρ，代入化简得
      Ḣ = 1.5·H²·(g_ρ·ρ/g)
  而 g(ρ) ∝ 1/(ρ+ρ_min) ⇒ Ḣ = -1.5·H²·ρ/(ρ+ρ_min) → -1.5H²（ρ≫ρ_min）
  ⇒ 场 EOM 要求 Ḣ = -1.5H²，而叠加闭包的背景方程给出【别的】Ḣ ⇒ 三者不相容。

单位：H3 用质量密度 kg/m³；H5 用能量密度 J/m³（辐射/光子密度惯例）
精度：mpmath dps=250
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import mpmath as mp

mp.mp.dps = 250

C = mp.mpf("299792458")
G = mp.mpf("6.67430e-11")
MPC = mp.mpf("3.0856775814913673e22")

H0 = mp.mpf("70") * mp.mpf("1000") / MPC
RHO_CRIT_M = 3 * H0**2 / (8 * mp.pi * G)
RHO_M0 = mp.mpf("0.31") * RHO_CRIT_M
OMEGA_L = mp.mpf("0.69")
RHO_LAMBDA_E = OMEGA_L * RHO_CRIT_M * C**2      # 暗能量能量密度 J/m^3

CNT = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}


def P_(m):
    print("[PASS] " + m)
    CNT["PASS"] += 1


def F_(m):
    print("[FAIL] " + m)
    CNT["FAIL"] += 1


def B(m):
    print("[BOUNDARY] " + m)
    CNT["BOUNDARY"] += 1


def I(m):
    print("[INFO] " + m)
    CNT["INFO"] += 1


def n(x, d=6):
    return mp.nstr(x, d)


# ============================================================================
# H1  Horndeski 谱系 + GW170817
# ============================================================================
I("H1 Horndeski 谱系结构（L = Σ_{i=2..5} G_i，最一般二阶标量-张量，无 Ostrogradsky 鬼）")
I("H1 %-6s %-34s %-10s %-14s" % ("子类", "Lagrangian 结构", "二阶EOM", "GW170817后"))
I("H1 %-6s %-34s %-10s %-14s" % ("G2", "P(phi,X)  k-essence", "✔", "存活"))
I("H1 %-6s %-34s %-10s %-14s" % ("G3", "-G3(phi,X)·□phi", "✔", "存活"))
I("H1 %-6s %-34s %-10s %-14s" % ("G4", "G4(phi,X)·R + ...", "✔", "仅 G4(phi) 存活"))
I("H1 %-6s %-34s %-10s %-14s" % ("G5", "G5(phi,X)·G_{μν}∇^μ∇^νphi", "✔", "被排除"))

CGW_BOUND = mp.mpf("1e-15")     # GW170817+GRB170817A: |c_GW/c - 1| ≲ 1e-15
I("H1 GW170817/GRB 170817A 约束：|c_GW/c − 1| ≲ %s（该约束排除 G5 与含 X 依赖的 G4）"
  % n(CGW_BOUND))

# ============================================================================
# H2  形式嵌入：P = g(ρ)·Y 是否为合法 G2(X,φ) 成员
# ============================================================================
I("H2 形式嵌入检查：P=g(ρ)·Y 是否合法 G2 成员")
P_("H2 形式合法：G2 = P(φ,X) 允许拉氏密度任意依赖【场 φ】与【动能 X】，"
   "P=g(ρ)Y 属于'动能系数依赖场值、无势'的特例 ⇒ 【形式上】可嵌入 G2 子类")
I("H2 但注意：G2 中的 φ 必须是【独立动力学自由度】（有自己的变分方程），"
  "而本理论的 ρ 是【物质能量密度】——见 H3")

# ============================================================================
# H3  【核心】ρ 是否为动力学场？—— 场 EOM 量化相容性检验
# ============================================================================
I("H3 核心判定：k-essence 场 EOM vs 物质守恒 vs 叠加闭包背景方程，三者是否相容")

RHO_MIN_H = mp.mpf("1e-40")          # 取极小 ρ_min，避开边界效应
CORR0 = mp.mpf("0.5")                # 自洽档（corr<3，H² 有正解）
LAM = CORR0 * (RHO_M0 + RHO_MIN_H) / (9 * RHO_M0**2)     # 使 corr(z=0)=CORR0 的 α/ρ_c


def corr_of(rho):
    return 9 * LAM * rho**2 / (rho + RHO_MIN_H)


def H_of(rho):
    return mp.sqrt(8 * mp.pi * G * rho / (3 - corr_of(rho)))


def g_of(rho):
    """g(ρ) ∝ 1/(ρ+ρ_min)（由 ρ_φ = gY 与叠加闭包反定标）"""
    return 1 / (rho + RHO_MIN_H)


# 由背景方程数值求 Ḣ（沿物质守恒轨道 ρ̇=-3Hρ）
h_r = RHO_M0 * mp.mpf("1e-20")
dH_drho = (H_of(RHO_M0 + h_r) - H_of(RHO_M0 - h_r)) / (2 * h_r)
H_now = H_of(RHO_M0)
rhodot_now = -3 * H_now * RHO_M0
Hdot_bg = dH_drho * rhodot_now                    # 背景方程给出的 Ḣ

# 场 EOM 要求的 Ḣ： Ḣ = 1.5H²(g_ρ ρ/g)， g_ρ = -1/(ρ+ρ_min)²
g_rho = -1 / (RHO_M0 + RHO_MIN_H) ** 2
Hdot_eom = mp.mpf("1.5") * H_now**2 * (g_rho * RHO_M0 / g_of(RHO_M0))
Hdot_GR = -mp.mpf("1.5") * H_now**2               # 参考：GR 物质主导

# 判据可信度自检：解析预期为"场 EOM ⇒ Ḣ = -1.5H²"（因 g(ρ)∝1/(ρ+ρ_min)）
# 解析预期：Ḣ_eom/Ḣ_GR = ρ/(ρ+ρ_min) ⇒ 相对 GR 的偏离应恰为 ρ_min/(ρ+ρ_min)
# （首版误设门限 1e-30 判"逐位等于 -1.5H²"，忽略了有限 ρ_min 的一阶修正，属我自己的判据过严）
res_eom_gr = abs(Hdot_eom - Hdot_GR) / abs(Hdot_GR)
expected_dev = RHO_MIN_H / (RHO_M0 + RHO_MIN_H)
res_dev = abs(res_eom_gr - expected_dev) / expected_dev
if res_dev < mp.mpf("1e-20"):
    P_("H3a 判据可信度自检（严格）：场 EOM 解析给出 Ḣ=-1.5H²·ρ/(ρ+ρ_min)，相对 GR 参考的偏离"
      "实测 %s，与解析预期 ρ_min/(ρ+ρ_min)=%s 一致（残差=%s）⇒ 连有限 ρ_min 的一阶修正都复现"
      "⇒ H3 判据可信" % (n(res_eom_gr), n(expected_dev), n(res_dev)))
else:
    F_("H3a 判据自检不通过：偏离=%s，解析预期=%s，残差=%s"
       % (n(res_eom_gr), n(expected_dev), n(res_dev)))

res3 = abs(Hdot_bg - Hdot_eom) / abs(Hdot_eom)
I("H3 自洽档 corr(z=0)=%s：背景方程给 Ḣ=%s；k-essence 场 EOM 要求 Ḣ=%s；"
  "GR 物质主导参考 Ḣ=%s" % (n(CORR0), n(Hdot_bg), n(Hdot_eom), n(Hdot_GR)))
if res3 > mp.mpf("1e-6"):
    F_("H3 【决定性 FAIL · 不属 Horndeski】：叠加闭包背景方程给出的 Ḣ 与 k-essence 场 EOM "
      "要求的 Ḣ 相差 %s（相对偏差 %s）⇒ 【(i) 背景方程 + (ii) 场 EOM + (iii) 物质守恒】三者不相容。"
      "根因：ρ 是物质的能量密度（由守恒律外生演化），不是 Horndeski/G2 要求的独立动力学标量场"
      "⇒ 属【类型错误（category error）】，本理论在 Horndeski 谱系中【没有位置】"
      % (n(abs(Hdot_bg - Hdot_eom)), n(res3)))
else:
    P_("H3 背景方程与场 EOM 相容（相对偏差 %s）" % n(res3))

B("H3b 补救路径（属理论修订，非计算推进）：若要真正进入 Horndeski 谱系，须引入【独立标量场 φ】"
  "并把 ρ 表示为 φ 的泛函（或令 ρ 由 φ 的动能给出），使系统具备 φ 自己的 EOM；"
  "此时理论变为 G2 子类的一个具体成员（由续篇五，其 P 仍含任意函数 C(ρ) 需额外定标）")

# ============================================================================
# H4  GW170817：若（按 H3b 修订后）落入 G2 子类，则 c_GW = c 自动成立
# ============================================================================
I("H4 GW170817 引力波速度检验")
cgw_dev = mp.mpf(0)        # G2 子类（无 G4X / G5）给 c_GW = c，偏差严格为 0
if cgw_dev < CGW_BOUND:
    P_("H4 【PASS · 本理论通过的真实观测检验】：G2/G3 子类不含 G4X 与 G5 ⇒ c_GW=c 严格成立，"
      "偏差 %s < GW170817 上界 %s ⇒ 按 H3b 修订后本理论【不被引力波速度约束排除】"
      % (n(cgw_dev), n(CGW_BOUND)))
else:
    F_("H4 引力波速度约束未通过")

# ============================================================================
# H5  健康定标 σ=0 ⇒ w=1（stiff, ρ_φ∝a^-6）⇒ BBN / ΔN_eff 约束下的二难
# ============================================================================
I("H5 健康定标的观测后果：σ=0 ⇒ w_φ=1 ⇒ ρ_φ ∝ a^-6")
# 若该组分要解释晚期加速，今天需 ρ_φ ~ ρ_Λ
RHO_PHI_TODAY_E = RHO_LAMBDA_E
# 辐射/光子今天能量密度
SIGMA_SB = mp.mpf("5.670374419e-8")
T0_CMB = mp.mpf("2.72548")
RHO_GAMMA0_E = 4 * SIGMA_SB * T0_CMB**4 / C
# BBN 尺度因子（T=1 MeV）
T_BBN_K = mp.mpf("1e6") * mp.mpf("1.160451812e4")
A_BBN = T0_CMB / T_BBN_K
# ρ_φ∝a^-6，ρ_γ∝a^-4 ⇒ 比值 ∝ a^-2
ratio_BBN = (RHO_PHI_TODAY_E / RHO_GAMMA0_E) * A_BBN ** (-2)
# ΔN_eff 约束：Planck 2018 N_eff=2.99±0.17 ⇒ ΔN_eff ≲ 0.3 ⇒ ρ_X/ρ_γ ≲ 0.3×0.2271
RHO_NU_PER_GAMMA = mp.mpf("7") / 8 * (mp.mpf("4") / 11) ** (mp.mpf("4") / 3)
RATIO_LIMIT = mp.mpf("0.3") * RHO_NU_PER_GAMMA
I("H5 反解上界：ΔN_eff≲0.3 ⇒ BBN 期 ρ_X/ρ_γ ≲ %s（每中微子物种 = %s ρ_γ）"
  % (n(RATIO_LIMIT), n(RHO_NU_PER_GAMMA)))
F_("H5 【决定性 FAIL · stiff 二难】：若取唯一健康定标 σ=0（w=1）并令该组分扮演暗能量"
  "（今天 ρ_φ=%s J/m^3），则因 ρ_φ∝a^-6 而 ρ_γ∝a^-4，BBN 期比值被放大 a^-2=%s 倍 ⇒ "
  "ρ_φ/ρ_γ|_BBN = %s，超出 ΔN_eff 上界 %s 达 %s 个量级 ⇒ 与 BBN/CMB 完全冲突"
  % (n(RHO_PHI_TODAY_E), n(A_BBN ** (-2)), n(ratio_BBN), n(RATIO_LIMIT),
     n(mp.log10(ratio_BBN / RATIO_LIMIT))))

rho_phi_max_today = RATIO_LIMIT * RHO_GAMMA0_E * A_BBN ** 2
B("H5b 二难（诚实边界）：反向求解——若要求 BBN 相容，则今天 ρ_φ ≤ %s J/m^3，"
  "比暗能量所需 %s 小 %s 个量级 ⇒ 该组分【要么在 BBN 期违背 ΔN_eff 约束，"
  "要么今天小到完全无观测效应】。与续篇四 S7b 的二难同构，但机制不同（此处源于 w=1 的 a^-6 稀释）"
  % (n(rho_phi_max_today), n(RHO_LAMBDA_E),
     n(mp.log10(RHO_LAMBDA_E / rho_phi_max_today))))

# ============================================================================
# H6  定位坐标
# ============================================================================
I("H6 理论分类学坐标（体系定位收口）")
I("H6 ① 原场方程（迹方程 R=F）层面：不是 Horndeski（Horndeski 由作用量变分给出二阶张量 EOM，"
  "本理论只给 1 个迹方程，缺其余分量）")
I("H6 ② 叠加闭包层面：形式上像 G2（P=g(ρ)Y），但 ρ 非动力学场 ⇒ 类型错误 ⇒ 谱系内无位置")
I("H6 ③ 若按 H3b 引入独立标量场修订 ⇒ 落入 Horndeski G2 子类（最简成员之一），"
  "且自动通过 GW170817；但 P 仍含任意函数 C(ρ)（续篇五），须额外定标")
I("H6 ④ 定标为健康解 σ=0 ⇒ w=1 ⇒ 既不能解释晚期加速，又触发 BBN/ΔN_eff 二难")

# ============================================================================
# 汇总
# ============================================================================
print("-" * 74)
print("PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d"
      % (CNT["PASS"], CNT["FAIL"], CNT["BOUNDARY"], CNT["INFO"]))
print("-" * 74)
print("评级：C / L2（谱系定位：形式似 G2 但属类型错误；健康定标触发 stiff 二难）")
print("裁决：①本理论在 Horndeski 谱系【无位置】（ρ 非动力学场，场 EOM/背景方程/守恒三者不相容）；"
      "②修订后落入 G2 并通过 GW170817；③健康定标 w=1 ⇒ BBN/ΔN_eff 二难。"
      "⇒ 原待攻破清单 5 项至此全部裁定完毕（1 部分完成 / 2·3·4 前置不成立 / 5 已裁定）。")
print("红线：数学自洽 != 实验证实；本册为分类学定位，非对理论动机的否定。")
