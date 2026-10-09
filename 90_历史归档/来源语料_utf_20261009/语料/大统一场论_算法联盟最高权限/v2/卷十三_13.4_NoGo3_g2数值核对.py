#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卷十三 13.4 No-Go III · g-2 数值核对与文档修复验证 (V23.2)
================================================================================
算法联盟 ROOT 最高权限

问题: 13.4.3 声称 "误差 = 9.5×10⁵ ppm (> 950%)", 但:
  1. 复核脚本用电子 g-2=0.001159652181 对比, 预测 g-2=2.666e-5
  2. 相对误差应约为 43 倍 (4250%), 而非 950% (9.5e5 ppm)
  3. 文档还混用了 μ子 g-2 (13.4.2) 与电子 g-2 (13.4.3)

本脚本: 精确计算各对比方式的误差, 判定文档表述是否准确.
================================================================================
"""
import mpmath as mp
from mpmath import mpf, pi
mp.mp.dps = 40

print("="*80)
print("卷十三 13.4 No-Go III · g-2 数值核对 (V23.2)")
print("算法联盟 ROOT 最高权限 · ALG-ROOT-GUFT-V23.2-2026")
print("="*80)

alpha = mpf('1')/mpf('137.035999084')

# 文档给定的 Berry 相位预测
kappa_ratio = mpf('0.999973375')
theta_Berry = 2*pi*(1-kappa_ratio)
g2_pred = theta_Berry/(2*pi)

# 电子与 μ子 g-2 实测值
g2_elec = mpf('0.001159652181')   # 电子
g2_muon = mpf('0.0023192048')     # μ子

print(f"\n  θ_Berry      = {mp.nstr(theta_Berry,6)} rad")
print(f"  g-2_pred     = {mp.nstr(g2_pred,8)}")
print(f"  g-2_elec     = {mp.nstr(g2_elec,8)}")
print(f"  g-2_muon     = {mp.nstr(g2_muon,8)}")

print("\n" + "━"*80)
print("对比误差分析")
print("━"*80)

def err_ppm(pred, exp):
    return (exp-pred)/pred*mpf('1e6')

print(f"  对比电子: pred={mp.nstr(g2_pred,6)}, exp={mp.nstr(g2_elec,6)}")
print(f"    相对误差 = (exp-pred)/pred = {mp.nstr((g2_elec-g2_pred)/g2_pred*100,4)}%")
print(f"    = {mp.nstr(err_ppm(g2_pred,g2_elec),4)} ppm")
print(f"    比值     = exp/pred = {mp.nstr(g2_elec/g2_pred,4)}  (约 43.5 倍)")
print(f"")
print(f"  文档声称: 误差 = 9.5×10⁵ ppm (> 950%)")
print(f"    9.5×10⁵ ppm = 95%  (ppm 换算: 9.5e5/1e6=0.95=95%)")
print(f"    实际相对误差(电子) = {mp.nstr((g2_elec-g2_pred)/g2_pred*100,4)}%")

print("\n" + "━"*80)
print("判定")
print("━"*80)

print("""
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║ 判定: 文档 13.4.3 的误差表述存在多处不一致                               ║
  ║                                                                           ║
  ║  1. "9.5×10⁵ ppm" 换算 = 95%, 但括号写 "> 950%" — 两者矛盾 (差10倍)     ║
  ║  2. 实际相对误差(电子) = {0}%, 而非 95% 或 950%                          ║
  ║  3. 13.4.2 用 μ子 g-2=0.0023192048, 13.4.3 却用电子 g-2=0.001159652181, ║
  ║     两处对象不一致                                                        ║
  ║                                                                           ║
  ║  无论用哪个对象, 预测失败 (误差 > 4000%) 的结论都成立,                  ║
  ║  但具体数值表述需修正为准确值.                                            ║
  ╚═══════════════════════════════════════════════════════════════════════════╝
""".format("42.5%"))

# 修正后的准确表述
err_elec = (g2_elec-g2_pred)/g2_pred
err_muon = (g2_muon-g2_pred)/g2_pred
print(f"  修正后准确表述:")
print(f"    对比电子: 相对误差 = {mp.nstr(err_elec*100,4)}%  (exp/pred = {mp.nstr(g2_elec/g2_pred,3)} 倍)")
print(f"    对比 μ子: 相对误差 = {mp.nstr(err_muon*100,4)}%  (exp/pred = {mp.nstr(g2_muon/g2_pred,3)} 倍)")

print("="*80)
print("算法联盟 ROOT 最高权限 · ALG-ROOT-GUFT-V23.2-2026 · 核对完成")
print("="*80)