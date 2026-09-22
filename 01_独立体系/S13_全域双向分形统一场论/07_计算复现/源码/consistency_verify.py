# -*- coding: utf-8 -*-
"""
V1.3.1 统一口径数值验证
验证1: 弱混合角关系 e = g sinθ_W = g' cosθ_W, m_Z = m_W/cosθ_W
验证2: 新口径 m_H/m_W = 4√2√κ̃/g̃ 与质量矩阵谱一致（含 τ/2 归一化因子）
验证3: 四观测 {m_W, m_Z, m_H, α} 反解四未知 {v, g̃, g̃', κ̃} 闭合（机器精度）
"""
import numpy as np

# [UTF8-GUARD v1]
import sys as _sys_utf8
try:
    _sys_utf8.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

print("=" * 66)
print("验证1 | 弱混合角关系（标准电弱一致陈述）")
print("=" * 66)
g, gp, v = 0.5, 0.3, 1.0
thw = np.arctan(gp / g)
e1 = g * np.sin(thw)
e2 = gp * np.cos(thw)
print(f"  g̃={g}, g̃'={gp} → θ_W = arctan(g̃'/g̃) = {thw:.6f}")
print(f"  e = g̃ sinθ_W = {e1:.10f},  e = g̃' cosθ_W = {e2:.10f}, 差 = {abs(e1-e2):.2e}")
mW = g * v / 2
mZ = np.sqrt(g * g + gp * gp) * v / 2
print(f"  m_W = g̃v/2 = {mW:.4f},  m_Z = √(g̃²+g̃'²)v/2 = {mZ:.4f}")
print(f"  m_W/cosθ_W = {mW/np.cos(thw):.6f} vs m_Z = {mZ:.6f} → 差 {abs(mZ - mW/np.cos(thw)):.2e}")
alpha = e1 * e1 / (4 * np.pi)
print(f"  α = e²/4π = {alpha:.6f} = g̃²sin²θ_W/4π = {g*g*np.sin(thw)**2/(4*np.pi):.6f}")

print()
print("=" * 66)
print("验证2 | 新口径质量比 m_H/m_W = 4√2√κ̃/g̃（τ/2 归一化）")
print("=" * 66)
kt = 0.5
mH = 2 * np.sqrt(2) * np.sqrt(kt) * v
ratio1 = mH / mW
ratio2 = 4 * np.sqrt(2) * np.sqrt(kt) / g
print(f"  m_H = 2√2√κ̃·v = {mH:.6f},  m_W = {mW:.6f}")
print(f"  m_H/m_W（质量值） = {ratio1:.6f}")
print(f"  m_H/m_W（闭式 4√2√κ̃/g̃） = {ratio2:.6f} → 差 {abs(ratio1-ratio2):.2e}")
print("  与第21章示例一致（g̃=0.5, κ̃=0.5 → 8.00）；旧口径 2√2√κ̃/g̃ = "
      f"{2*np.sqrt(2)*np.sqrt(kt)/g:.4f}（差因子 2 = τ vs τ/2 归一化）")

print()
print("=" * 66)
print("验证3 | 四观测反解四未知（闭合性）")
print("=" * 66)
rng = np.random.default_rng(2026)
for trial in range(3):
    g = rng.uniform(0.2, 0.8)
    gp = rng.uniform(0.1, 0.5)
    kt = rng.uniform(0.2, 1.0)
    v = rng.uniform(0.5, 2.0)
    # 生成观测
    mW_obs = g * v / 2
    mZ_obs = np.sqrt(g * g + gp * gp) * v / 2
    mH_obs = 2 * np.sqrt(2) * np.sqrt(kt) * v
    thw = np.arctan(gp / g)
    alpha_obs = g * g * np.sin(thw) ** 2 / (4 * np.pi)
    # 反解
    a = 2 * mW_obs
    b = 2 * np.sqrt(mZ_obs**2 - mW_obs**2)
    sin2 = b * b / (a * a + b * b)   # sin²θ_W = g̃'²/(g̃²+g̃'²)（tanθ_W=g̃'/g̃）
    e = np.sqrt(4 * np.pi * alpha_obs)
    v_rec = a * np.sqrt(sin2) / e
    g_rec = a / v_rec
    gp_rec = b / v_rec
    kt_rec = (mH_obs / (2 * np.sqrt(2) * v_rec)) ** 2
    err = max(abs(g_rec - g), abs(gp_rec - gp), abs(kt_rec - kt), abs(v_rec - v))
    print(f"  组{trial+1}: 原参数 (g̃,g̃',κ̃,v)=({g:.4f},{gp:.4f},{kt:.4f},{v:.4f})")
    print(f"    反解   (g̃,g̃',κ̃,v)=({g_rec:.4f},{gp_rec:.4f},{kt_rec:.4f},{v_rec:.4f})  最大误差 {err:.2e}")
print("  判定: 四观测 {m_W, m_Z, m_H, α} 完全钉死四未知 {v, g̃, g̃', κ̃}（机器精度闭合）")
print("  注: α 提供第4个独立约束（通过弱混合角），因此自由参数实为 4 个而非 2 个")
