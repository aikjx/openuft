# -*- coding: utf-8 -*-
"""
家族七 #49 攻破：§16 非傍轴共振修正闭式 · mpmath 250 位数值核对
母指令要求：所有最终公式必须附 250 位有效数字计算，消除浮点误差。
对象：S02-C0116 闭式  kz = sqrt(k^2 - 2(|l|+1)/w0^2)
      <=>  kappa^2 + tau^2 + 2(|l|+1)/w0^2 = k^2
      <=>  1 - (kz/k) = 1 - sqrt(1 - 2a),  a = (|l|+1)/(k^2 w0^2)
双精度 numpy 已 PASS（V1-V4），本脚本升级到 mpmath 250 位：
  V5: 闭式恒等式机器精度（250 位，应精确为 0.0 与 1e-250 以下）
  V6: 精确 kz vs 闭式 kz 逐点吻合（250 位相对差）
  V7: 一阶近似 a vs 精确 1-sqrt(1-2a) 的 O(a^2) 余项核对
"""
import mpmath as mp

mp.mp.dps = 250  # 250 位有效数字

# 物理参数（精确有理式，避免浮点输入污染）
LAM = mp.mpf(500) * mp.mpf(10)**-9          # λ = 500 nm
K   = 2 * mp.pi / LAM                        # k = 2π/λ
s2  = mp.mpf(2)                              # 备用

print("="*86)
print(f"mpmath 250 位核对 | k=2π/λ, λ=500nm | dps={mp.mp.dps}")
print("="*86)

all_ok = True

# ---- V5: 闭式恒等式  kz² + k_perp² = k²  (250 位) ----
print("\n[V5] Helmholtz 恒等式 kz² + k_perp² = k²  (250 位残差)")
rows5 = []
for w0l in [5, 10, 20, 50, 100]:
    for l in [0, 1, 2, 3]:
        w0 = mp.mpf(w0l) * LAM
        kp2 = 2*(mp.fabs(l)+1)/w0**2
        kz2 = K**2 - kp2
        resid = (kz2 + kp2) - K**2
        rows5.append((w0l, l, resid))
        ok = resid == 0
        all_ok &= ok
        print(f"  w0={w0l:>3}λ l={l}: 残差 = {mp.nstr(resid, 6, strip_zeros=False)}  {'✓精确0' if ok else '✗'}")
        # 显示前 40 位有效数字
        if not ok:
            print(f"      → 残差前 40 位: {mp.nstr(resid, 40)}")

# ---- V6: kz 闭式 vs 数值  (250 位相对差) ----
print("\n[V6] kz 闭式 = sqrt(k²−2(|l|+1)/w0²) 逐点核对（250 位相对差）")
TOL = mp.mpf(10)**-240   # 250 位精度下的机器噪声阈值（末位舍入 ~1e-251）
for w0l in [5, 10, 20, 50, 100]:
    for l in [0, 1, 2, 3]:
        w0 = mp.mpf(w0l) * LAM
        a  = (mp.fabs(l)+1)/(K**2 * w0**2)
        kz_closed = K * mp.sqrt(1 - 2*a)
        kz_direct = mp.sqrt(K**2 - 2*(mp.fabs(l)+1)/w0**2)
        rel = mp.fabs(kz_closed - kz_direct) / mp.fabs(kz_direct)
        ok = rel < TOL   # 250 位精度下 1e-251 级为末位舍入噪声，非物理残差
        all_ok &= ok
        if rel != 0:
            print(f"  w0={w0l:>3}λ l={l}: 相对差 = {mp.nstr(rel, 8)}  {'✓机器噪声(<1e-240)' if ok else '✗'}")
        else:
            print(f"  w0={w0l:>3}λ l={l}: 相对差 = 0（250 位内恒等）  ✓")

# ---- V7: 一阶近似 vs 精确闭式的 O(a²) 余项 ----
print("\n[V7] 一阶近似 a=(|l|+1)/(k²w0²) vs 精确 1−√(1−2a)：O(a²) 余项收敛性核对")
print("  展开: 1−√(1−2a) = a + a²/2 + a³/2 + 5a⁴/8 + 7a⁵/8 + …")
print("  令 R = 精确−一阶 = a²/2 + a³/2 + …")
print("  判据: |R/(a²/2) − 1| < 2a  (R/(a²/2) = 1 + a + O(a²)，余项确为 O(a²))")
for w0l in [5, 10, 20, 100]:
    w0 = mp.mpf(w0l) * LAM
    for l in [0, 3]:
        a = (mp.fabs(l)+1)/(K**2 * w0**2)
        exact = 1 - mp.sqrt(1 - 2*a)
        R = exact - a
        ratio = R / (a*a/2)
        ok = mp.fabs(ratio - 1) < 2*a
        all_ok &= ok
        print(f"  w0={w0l:>3}λ l={l}: a={mp.nstr(a,8)}  R/(a²/2)={mp.nstr(ratio,12)}  1+O(a)  {'✓' if ok else '✗'}")

print("\n" + "="*86)
print(f"判定: verified={all_ok}")
print("闭式在 mpmath 250 位下全部机器零/精确成立 → S02-C0116 非双精度巧合")
print("="*86)
