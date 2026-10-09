#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卷十三 13.5 No-Go IV · 质量比假设证伪数值核对 (V23.3)
================================================================================
算法联盟 ROOT 最高权限

核对 13.5.3 简单拓扑假设证伪的相对误差数值:
  假设 A: m_i ∝ n_i (缠绕数)
    预测 m_μ/m_e = 2,   实际 206.768283 → 相对误差?
    预测 m_τ/m_e = 3,   实际 3477.227553 → 相对误差?
  假设 C: 最佳拟合 m_μ/m_e ≈ 206.77 ≈ 6²+10² ?

本脚本: 精确计算各项相对误差, 判定文档数值是否准确.
================================================================================
"""
import mpmath as mp
from mpmath import mpf
mp.mp.dps = 30

print("="*70)
print("卷十三 13.5 No-Go IV · 质量比证伪数值核对 (V23.3)")
print("算法联盟 ROOT 最高权限 · ALG-ROOT-GUFT-V23.3-2026")
print("="*70)

m_e  = mpf('9.1093837015e-31')
m_mu = mpf('1.883531627e-28')
m_tau= mpf('3.16754e-27')

r_mue = m_mu/m_e
r_tau_e = m_tau/m_e
r_tau_mu = m_tau/m_mu

print(f"\n  实测比值:")
print(f"    m_μ/m_e = {mp.nstr(r_mue,8)}")
print(f"    m_τ/m_e = {mp.nstr(r_tau_e,8)}")
print(f"    m_τ/m_μ = {mp.nstr(r_tau_mu,8)}")

print("\n" + "━"*70)
print("假设 A 证伪 (M_i ∝ n_i, 预测 n=2,3)")
print("━"*70)
pred_mu = mpf('2')
pred_tau = mpf('3')
err_mu  = (r_mue-pred_mu)/r_mue*100
err_tau = (r_tau_e-pred_tau)/r_tau_e*100
print(f"  m_μ/m_e: 预测2, 实测{mp.nstr(r_mue,5)}, 相对误差={mp.nstr(err_mu,4)}%  (文档写 99.0%)")
print(f"  m_τ/m_e: 预测3, 实测{mp.nstr(r_tau_e,5)}, 相对误差={mp.nstr(err_tau,4)}%  (文档写 99.97%)")
print(f"    文档 m_μ/m_e '99.0%'   → 实际 {mp.nstr(err_mu,4)}%  {'✓' if abs(float(err_mu)-99.0)<0.5 else '✗'}")
print(f"    文档 m_τ/m_e '99.97%'  → 实际 {mp.nstr(err_tau,4)}%  {'✓' if abs(float(err_tau)-99.97)<0.05 else '✗'}")

print("\n" + "━"*70)
print("假设 C 证伪 (量子化 m_i ∝ n_i, 最佳拟合 6²+10²)")
print("━"*70)
fit = mpf('6')**2 + mpf('10')**2
print(f"  6²+10² = {mp.nstr(fit,6)}")
print(f"  m_μ/m_e = {mp.nstr(r_mue,6)}")
ratio = fit/r_mue
print(f"  6²+10² / (m_μ/m_e) = {mp.nstr(ratio,6)}  (偏离1的误差={mp.nstr(abs(1-ratio)*100,4)}%)")
print(f"  预测值 136 vs 实测 206.77 → 相对误差 = {mp.nstr((r_mue-fit)/r_mue*100,4)}%")

print("\n" + "━"*70)
print("判定")
print("━"*70)
print("""
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║ 判定:                                                                     ║
  ║  - 假设 A: m_μ/m_e 相对误差 99.03% (文档 99.0% ✓ 可接受)                 ║
  ║  - 假设 A: m_τ/m_e 相对误差 99.91% (文档 99.97% → 需修正为 99.91%)        ║
  ║  - 假设 C: 6²+10²=136 距 206.77 偏差 34.2%, "≈206.77" 说法夸大了吻合度,  ║
  ║            文档已谨慎标注"(巧合?)", 可保留但精确误差为 34.2%              ║
  ║                                                                           ║
  ║  结论: No-Go IV 的证伪结论完全成立, 但 m_τ/m_e 相对误差 99.97% 应为       ║
  ║        99.91%. 假设 C 的"≈"表述宜补充精确误差 34.2%.                     ║
  ╚═══════════════════════════════════════════════════════════════════════════╝
""")

print("="*70)
print("算法联盟 ROOT 最高权限 · ALG-ROOT-GUFT-V23.3-2026 · 核对完成")
print("="*70)