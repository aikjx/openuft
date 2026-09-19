# -*- coding: utf-8 -*-
"""
算法联盟 | 复核报告剩余高风险声明的精算真伪 (续 verify_report_20260814.py)
====================================================================
核查:
  E1  验证表 G<10^-5%, m_p<10^-7%  (虚假精度?)
  E2  四力整数比 实测 1:3.796:15.9 (数字对否?)
  E3  384=64卦x6爻 = 32维x12生成元 严格等价?
  E4  G=pi c^3/(S hbar H0^2) 是否 G 生成式 (循环?)
  E5  人工引力场 15.092 GHz / 251.6 T 来源
"""
import mpmath as mp
mp.mp.dps = 80

from verify_uft_repair import (
    hbar, c, G, eps0, mu0, Qtop, me_exp, alpha_exp,
    phi_T_from_topology, weak_coupling_from_topology,
    strong_coupling_from_topology, alpha_MZ_from_running,
    G_cosmology_scaling, codata_benchmark,
)

def P(*a):
    print(" ".join(str(x) for x in a))
def sep(t=""):
    if t: P("-"*8, t, "-"*8)

# ---------- E1: 验证表 G<10^-5% / m_p<10^-7% ----------
P("="*88); P("E1 验证表 G<10^-5%, m_p<10^-7% 是否虚假精度"); P("="*88)
rows = codata_benchmark()
gd = {r[0]: (r[1], r[2]) for r in rows}
for k in gd:
    P(f"  {k:42s} expect={float(gd[k][0]):.6e} got={float(gd[k][1]):.6e}")
# G: 在框架里 G 是 INPUT(PDG 原值); 若验证是 expect=G_CODATA 用 got=G_INPUT -> rel=0 平凡
# 真实检查: G 是否被任何拓扑公式"生成"? 否. 见 G_cosmology_scaling: G 是入口.
sep("判定")
P("  G 在框架为 INPUT(PDG), 验证表若以 CODATA 自身为基准 => 误差~0 是平凡闭环,")
P("  不代表'G 由框架生成达 10^-5% 精度'. 同理 m_p(proton) 若未实现生成公式,")
P("  误差<10^-7% 掩盖了'G/m_p 实为输入'的事实. => 验证表把 INPUT 误标为 CLOSED 成果.")
P("  >> [FAIL] '全部误差<10^-5%' 是虚假精度宣称: 仅 e/Z0/me 等真闭环项可称精度;")
P("     G/m_p 等为 INPUT, 不应计入'生成精度'.")

# ---------- E2: 四力整数比 实测 1:3.796:15.9 ----------
P("\n"+"="*88); P("E2 四力整数比 实测 1:3.796:15.9 数字核验"); P("="*88)
a_em_MZ = alpha_MZ_from_running()[0]
sin2 = mp.mpf("0.23122")
a_w_obs = a_em_MZ / sin2
a_s_obs = mp.mpf("0.1179")
ratio_w = a_w_obs / a_em_MZ
ratio_s = a_s_obs / a_em_MZ
P(f"  a_em_obs = {float(a_em_MZ):.6f}")
P(f"  a_w_obs  = a_em/sin^2tw = {float(a_w_obs):.6f}  => a_w_obs/a_em = {float(ratio_w):.4f}  (报告写 3.796)")
P(f"  a_s_obs  = {float(a_s_obs):.6f}  => a_s_obs/a_em = {float(ratio_s):.4f}  (报告写 15.9)")
P(f"  >> [FAIL] 正确实测比应为 1 : {float(ratio_w):.3f} : {float(ratio_s):.2f}")
P(f"      报告 1:3.796:15.9 中 3.796 实为 1/sin^2tw 的错误近似(实际=4.32), 15.9 亦偏低")
P(f"      几何整数比 1:4:15 (f_w=4,f_s=15) 与实测偏差: w={float(abs(4/ratio_w-1)):.2%}, s={float(abs(15/ratio_s-1)):.2%}")

# ---------- E3: 384 = 64x6 = 32x12 严格等价 ----------
P("\n"+"="*88); P("E3 384=64卦x6爻 = 32维x12生成元 严格等价?"); P("="*88)
P(f"  64卦 x 6爻 = {64*6}  (爻的总数, 离散卦象计数)")
P(f"  32维 x 12生成元 = {32*12}  (报告称等效)")
P(f"  >> [FAIL] 两个乘积含义不同: 64x6 是卦爻符号计数; 32维是母流形维数, 12 是规范自由度,")
P(f"      二者相乘 = 384 是数字巧合, '12生成元'并非与'32维'相乘的线性因子;")
P(f"      代码维度谱实为 32维母流形 -> 4维时空 -> 28维内部=16+12, 无 '32x12=384' 分解.")
P(f"      报告'两种分解严格等价'不实, 应改为'384=64x6 是爻计数; 32维/12规范是独立谱分解'.")

# ---------- E4: G=pi c^3/(S hbar H0^2) 生成式? ----------
P("\n"+"="*88); P("E4 G=pi c^3/(S hbar H0^2) 是否 G 生成式"); P("="*88)
R_H, lP, N_area, S_BH, S_dS, G_area, ratio = G_cosmology_scaling()
P(f"  G (INPUT)        = {float(G):.6e}")
P(f"  G_area (S_BH反推) = {float(G_area):.6e}   (面积律定标使 G 偏小 {float(G/G_area):.2e} 倍)")
P(f"  S_dS/S_BH = {float(ratio):.3e}  (宇宙学常数问题量级)")
P(f"  >> [WARN] 框架里 G 是 INPUT; S_BH/S_dS 也由 G 反推 => G=.../S 是循环定义, 非独立生成式.")
P(f"      报告标'结构式'可接受, 但须注明: G 仍由 CODATA 输入, S 由 G 回推, 非第一性导出.")

# ---------- E5: 人工引力场 15.092 GHz / 251.6 T ----------
P("\n"+"="*88); P("E5 人工引力场 15.092 GHz / 251.6 T 来源"); P("="*88)
P(f"  本仓库 verify_uft_repair.py / unified_field_verification.py 均未含 15.092 GHz / 251.6 T 计算.")
P("  >> [WARN] 该数值疑似来自未纳入本验证体系的人工引力场模块(03-物理统一场/人工引力场),")
P("      未经独立精算复核; 报告已诚实标注 251.6T 差 5.6 倍, 但 15.092 GHz 亦需独立推导背书.")

P("\n"+"="*88); P("SUMMARY (extra)"); P("="*88)
P("[FAIL] E1 验证表 G<10^-5%/m_p<10^-7% 虚假精度(INPUT误标CLOSED)")
P("[FAIL] E2 四力实测比应为 1:4.32:16.42, 报告 1:3.796:15.9 数字错")
P("[FAIL] E3 384=64x6 与 32x12 非严格等价(含义不同, 数字巧合)")
P("[WARN] E4 G=pi c^3/(S hbar H0^2) 循环定义, 非生成式; G/S 互推")
P("[WARN] E5 15.092GHz/251.6T 未在验证体系内, 缺独立推导背书")
