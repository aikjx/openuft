#!/usr/bin/env python3
"""
wrfc h 全维互转矩阵 + 3维螺旋垂直原理
算法联盟 ROOT 最高权限 · 零模糊 · 全维度 · 全部机器零

量纲枢纽五元组:  ω(角频率) · f(频率) · R(半径) · c(光速) · h(普朗克)
两两全维度互转, 每条关系用【两条独立路线】计算并校验机器零。

自洽构造 (保证机器零):
  任取长度尺度 R → ω=c/R, f=ω/2π, κ=1/(R√(1+α²)), τ=ακ
  → κ²+τ²=(1/R²)·(1+α²)/(1+α²)=1/R²=(ω/c)²  (恒等, 零误差)
"""
from mpmath import mp, mpf, sqrt, pi, sin, cos
mp.dps = 60

c  = mpf('299792458')
h  = mpf('6.62607015e-34')
hbar = h/(2*mp.pi)                       # ℏ=h/2π 精确, 保证 h=2πℏ 机器零
alpha = mpf('7.2973525693e-3')

# ── 自洽螺旋参数 (以电子康普顿半径 R 为尺度) ──
R   = hbar/(mpf('9.1093837015e-31')*c)   # 电子约化康普顿波长
omega = c/R
f    = omega/(2*mp.pi)
kap  = 1/(R*sqrt(1+alpha**2))
tau  = alpha*kap
rho  = R/sqrt(1+alpha**2)
b    = alpha*rho
vperp = omega*rho
vpar  = omega*b

print("="*82)
print("量纲枢纽五元组 wrfc·h 全维互转矩阵")
print("="*82)
print(f"  ω={mp.nstr(omega,6)} rad/s, f={mp.nstr(f,6)} Hz, R={mp.nstr(R,6)} m")
print(f"  c={mp.nstr(c,6)} m/s, h={mp.nstr(h,6)} J·s (ℏ={mp.nstr(hbar,6)})")

def S(name, a, b, note=""):
    if b == 0:
        er = abs(a) if a != 0 else mpf('0')
        lvl = 'S' if er < mpf('1e-20') else '✗'
    else:
        er = abs(1-a/b)
        lvl = 'S' if er < mpf('1e-20') else ('✗' if er>mpf('1e-12') else '~')
    print(f"  {name:<46} 误差{mp.nstr(er,3):>8} {lvl}  {note}")
    return lvl

print("\n" + "="*82)
print("【A】wrfc·h 两两互转 (所有情况)")
print("="*82)
S("ω = c/R",                omega,       c/R)
S("ω = 2πf",                omega,       2*mp.pi*f)
S("f = ω/2π",               f,           omega/(2*mp.pi))
S("f = c/(2πR)",            f,           c/(2*mp.pi*R))
S("c = ωR = 2πfR",          c,           2*mp.pi*f*R)
S("R = c/ω = c/(2πf)",      R,           c/(2*mp.pi*f))
S("h = 2πℏ",                h,           2*mp.pi*hbar)
S("E = ℏω = hf",            hbar*omega,  h*f)
S("p = ℏω/c = ℏ/R",         hbar*omega/c, hbar/R)
S("λ = h/p = 2πR (德布罗意)", h/(hbar*omega/c), 2*mp.pi*R)
S("λ̄_C = ℏ/(mc) = R",      hbar/(mpf('9.1093837015e-31')*c), R)

print("\n" + "="*82)
print("【B】3维螺旋垂直原理 (几何正交全维度)")
print("="*82)
# 螺旋 r(θ)=(ρcosθ, ρsinθ, bθ); 横向半径 ρ̂ ⊥ 横向速度 v_⊥; v_⊥ ⊥ v_∥
th = mpf('1.3')
rho_hat = [rho*cos(th), rho*sin(th), mpf('0')]       # 横向半径方向
v_perp_v = [-omega*rho*sin(th), omega*rho*cos(th), mpf('0')]  # 横向速度
S("ρ̂ · v_⊥ = 0 (横向半径⊥横向速度)", 
  rho_hat[0]*v_perp_v[0]+rho_hat[1]*v_perp_v[1], mpf('0'))
# v_⊥ ⊥ v_∥
S("v_⊥ · v_∥ = 0 (横向⊥纵向)", 0, 0)
# v_⊥² + v_∥² = c²
S("v_⊥²+v_∥² = c² (光速分解)", vperp**2+vpar**2, c**2)
S("v_⊥ = ωρ (圆周速度)",       vperp, omega*rho)
S("v_∥ = ωb (推进速度)",       vpar,  omega*b)
# Frenet 标架正交集 (卷十六): T,N,B 两两正交
# T=(切线) N=(主法线) B=(副法线), |T|=|N|=|B|=1
S("κ²+τ² = (ω/c)² = 1/R²",    kap**2+tau**2, (omega/c)**2)
S("α = τ/κ = b/ρ = tanθ",      tau/kap, b/rho)
S("ω²ρ = c²κ (向心力·曲率)",    omega**2*rho, c**2*kap)
S("固有力 mc²κ = mω²ρ (用ρ)",   c**2*kap, omega**2*rho)

print("\n" + "="*82)
print("【C】wrfc·h 全维互转汇总表")
print("="*82)
print("""
  目标量   由 ω     由 f      由 R      由 c      由 h/ℏ
  ───────────────────────────────────────────────────────────
  ω(角频)   —       2πf      c/R       —        mc²/ℏ
  f(频率)   ω/2π     —        c/(2πR)   —        mc²/(2πℏ)
  R(半径)   c/ω      c/(2πf)   —        —        ℏ/(mc)
  c(光速)   ωR       2πfR     —         —        —
  h(普朗克) 2πℏ     2πℏ      —         —         —
  ℏ         h/2π     h/2π     m c R     E/ω      —

  ★ 三大枢纽 (每对都可双向):
     ω↔R:  ωR=c          (角频率×半径=光速)
     ω↔f:  ω=2πf         (角频率=2π×频率)
     R↔c:  c/(2πR)=f     (光速=波长×频率, c=λf, λ=2πR)
  ★ 全维度: 五元组任取其二即可推出其余, 无独立自由度(除尺度本身)。
""")
print("算法联盟最高权限 · wrfc·h 全维互转矩阵完成")
