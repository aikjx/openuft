# -*- coding: utf-8 -*-
"""TUFT V9.14 量子层定量化：螺旋 g 因子结构计算 + 可证伪性清单
A 组：螺旋轨道磁矩/自旋结构（从 {κ,τ,ω} 第一性导出）
  A1 轨道回磁比推导：μ=qωρ²/2、L_z=mωρ² ⇒ μ/L_z = q/(2m)（g=1 轨道极限）
  A2 电子数值：ρ、ω、μ、L_z（用 m_e、α 输入）
  A3 与电子观测对撞：μ_helix/μ_B、L_z/ħ、μ_e/μ_helix、g 因子缺口
  A4 判定：g=1 轨道结构 vs 电子自旋 1/2、g≈2.002319——量子层 0% 定量化
B 组：可证伪性清单（全书判别性清点，纯清单不计算）
用法：python tuft_v102_spin_gfactor.py
"""
import json, math

HBAR = 1.054571817e-34   # J·s
C    = 2.99792458e8      # m/s
ME   = 9.1093837015e-31  # kg
QE   = 1.602176634e-19   # C
ALPHA = 7.2973525693e-3
MUB  = 9.2740100783e-24  # J/T（CODATA）
GE   = 2.00231930436256  # 电子 g 因子（CODATA 2018）

# ---------- A1/A2 螺旋轨道量（第一性：m=ħω/c²、α=b/ρ、ρ=ħ/(mc√(1+α²))） ----------
rho = HBAR / (ME*C*math.sqrt(1.0+ALPHA*ALPHA))     # m
omega = ME*C*C/HBAR                                # s⁻¹（公理 m=ħω/c² ⇒ ω=mc²/ħ）
b = ALPHA*rho                                       # 螺距参数
mu   = QE*omega*rho*rho/2.0                         # μ=qωρ²/2（J/T）
Lz   = ME*omega*rho*rho                             # L_z=mωρ²（J·s）
ratio = mu/Lz                                       # 回磁比 = q/(2m)
g_orbital = 2.0*ME*ratio/QE                         # g=2m·(μ/L)/q = 1（轨道极限）

# A3 对撞
mu_over_mub = mu/MUB                                # 应 ≈ 1/(1+α²)
Lz_over_hbar = Lz/HBAR                              # 应 ≈ 1/(1+α²)（整数 ħ，非 ħ/2）
mu_e = GE*MUB/2.0                                   # 电子观测 μ_e = g_e·μ_B/2
mu_e_over_mu_helix = mu_e/mu
# 若注入自旋 S=ħ/2：μ_spin = (q/2m)(ħ/2) = qħ/4m = μ_B/2·(1/√(1+α²))·... 简化为 μ_B/2
mu_spin = QE*HBAR/(4.0*ME)
ratio_e_spin = mu_e/mu_spin                         # = g_e ≈ 2.002319

A = {
  "inputs": {"m_e_kg": ME, "alpha": ALPHA},
  "A1": {"mu": mu, "Lz": Lz, "gyromagnetic_ratio_mu_L": ratio, "g_orbital": g_orbital,
         "derivation": "μ=qωρ²/2、L_z=mωρ² ⇒ μ/L_z=q/(2m)：轨道极限 g=1"},
  "A2": {"rho_m": rho, "rho_over_lambda_bar_C": rho*ME*C/HBAR,
         "omega_s_inv": omega, "b_m": b,
         "mu_J_T": mu, "Lz_J_s": Lz},
  "A3": {"mu_over_muB": mu_over_mub, "analytic_1_over_1pa2": 1.0/(1.0+ALPHA*ALPHA),
         "Lz_over_hbar": Lz_over_hbar,
         "electron_mu_over_muB": GE/2.0,
         "mu_e_over_mu_helix": mu_e_over_mu_helix,
         "spin_injected_mu_spin": mu_spin, "mu_e_over_mu_spin": ratio_e_spin,
         "g_e": GE, "g_minus_2_over_2": (GE-2.0)/2.0},
  "A4_verdict": ("螺旋几何第一性给出 L_z≈ħ（整数）、g=1（轨道回磁比）、μ≈μ_B/(1+α²)——"
                 "μ 与电子观测仅差 ~0.12%%，但 (L,g) 分解结构不符：电子是自旋 1/2（ħ/2）且 g≈2.002319。"
                 "μ 的接近是恒等式同源（μ_B=qħ/2m 共用同一参数组合），非量子预言；"
                 "量子层 0%% 定量化：缺的是半整数量子自旋结构（Dirac 型），不是数值拟合。")
}

# ---------- B 组：可证伪性清单（判别性清点） ----------
falsifiability = [
  {"claim": "v_总=c 公理（本源场元合速度恒为 c）", "test": "本源场元不可观测，无直接检验通道", "status": "公理（不可证伪性边界）"},
  {"claim": "螺旋几何 m=ħω/c²、α=b/ρ", "test": "ω 无独立观测；α 观测为输入", "status": "恒等式（映射，非预言）"},
  {"claim": "四力同形（Yukawa 型）", "test": "QCD 线性势/禁闭", "status": "部分证伪 → σr 外源修补（V9.8/19.4）"},
  {"claim": "力程律 λ=ħ/mc", "test": "四力力程谱", "status": "恒等式（质量谱外输）"},
  {"claim": "组合比值链 F_E/F_G=α(m_P/m_p)²", "test": "质子库仑/引力比 1.24×10³⁶", "status": "恒等式（复现教科书值，16 章 PASS）"},
  {"claim": "EC 真空 ≡ GR", "test": "EHT 阴影、GW170817", "status": "继承性 PASS（判别性 0，19 章）"},
  {"claim": "螺旋 g 因子结构（本章）", "test": "电子 g=2.002319、μ_e=1.00116μ_B", "status": "结构不符：g=1、L≈ħ（量子层 0% 定量）"},
  {"claim": "LW 辐射结构（近场/辐射二分）", "test": "同步辐射、推迟功率", "status": "继承性（EM 子极限，12 章 PASS）"},
  {"claim": "潜在判别区：自旋致密物质内部", "test": "NS 内部、早期宇宙", "status": "无数值内容（B03）——无法检验"},
]
discriminative = [r for r in falsifiability if r["status"].startswith(("待检验", "真预言"))]
B = {"ledger": falsifiability,
     "discriminative_predictions_count": len(discriminative),
     "B_verdict": ("专属判别性预言 = 0 类：全部内容为公理/恒等式/继承性/已修补/无通道；"
                   "唯一可能判别区（自旋致密物质内部）无数值内容。"
                   "与 V9.12 预言性 20%（结构关联成色）一致：结构恒等式 ≠ 可证伪预言。")}

out = {"A": A, "B": B}
with open(r"D:\a10\aikjx\code\my_lib\tuft_v102_spin_gfactor_results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
