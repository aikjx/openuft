# -*- coding: utf-8 -*-
"""
空间螺旋修复版 基底求导证明验证 (C24)
目标：从 R(t)=(A cosωt, A sinωt, bωt) 严格推导 κ, τ, 不变量, tanθ
     并验证 ω√(A²+b²)=c 约束下的闭式。
依赖：sympy（仅用于符号推导，与 mpmath 数值无关）
"""
import sympy as sp

t, A, b, w, c = sp.symbols('t A b w c', positive=True, real=True)

# ---- 新公理基底 ----
Rt = sp.Matrix([A*sp.cos(w*t), A*sp.sin(w*t), b*w*t])

# ---- 逐阶求导 ----
R1 = sp.diff(Rt, t)   # R'
R2 = sp.diff(R1, t)   # R''
R3 = sp.diff(R2, t)   # R'''

print("=== 逐阶导数 ===")
print("R'(t) =", R1.T)
print("R''(t)=", R2.T)
print("R'''(t)=", R3.T)

# ---- |R'| ----
speed = sp.sqrt(sp.simplify(R1.dot(R1)))
print("\n=== 速率 ===")
print("|R'| =", speed)

# 约束：ω√(A²+b²)=c  ⇒  A²+b² = c²/ω²
constr = sp.Eq(w*sp.sqrt(A**2 + b**2), c)
sub = {A**2 + b**2: c**2 / w**2}

# ---- 曲率 κ = |R'×R''| / |R'|³ ----
cross = R1.cross(R2)
cross_norm = sp.sqrt(sp.simplify(cross.dot(cross)))
kappa = sp.simplify(cross_norm / speed**3)
kappa_closed = sp.simplify(kappa.subs(sub))
print("\n=== 曲率 κ ===")
print("κ 原始表达式 =", kappa)
print("代入约束后 κ =", kappa_closed)

# ---- 挠率 τ = (R'×R'')·R''' / |R'×R''|² ----
numer = sp.simplify(cross.dot(R3))
denom = sp.simplify(cross.dot(cross))
tau = sp.simplify(numer / denom)
tau_closed = sp.simplify(tau.subs(sub))
print("\n=== 挠率 τ ===")
print("τ 原始表达式 =", tau)
print("分子 (R'×R'')·R''' =", numer)
print("代入约束后 τ =", tau_closed)

# ---- 不变量 κ²+τ² = ω²/c² ----
print("\n=== 不变量 κ²+τ² ===")
print("κ²+τ² =", sp.simplify(kappa_closed**2 + tau_closed**2))
print("ω²/c² =", sp.simplify(w**2/c**2))
print("差 =", sp.simplify(kappa_closed**2 + tau_closed**2 - w**2/c**2))

# ---- tanθ = τ/κ = b/A ----
print("\n=== 倾角 tanθ ===")
print("τ/κ =", sp.simplify(tau_closed / kappa_closed))
print("b/A =", b/A)

# ---- 量纲（sympy 不做量纲，手动声明）----
print("\n=== 量纲声明 ===")
print("[κ]=[τ]=L⁻¹ ; [κ²+τ²]=L⁻² ; [ω²/c²]=(T⁻¹)²/(L²T⁻²)=L⁻²  ✓")
print("tanθ 无量纲 ✓")

# ---- 数值核验 ----
import sympy as _sp
vals = {A: 1e-15, b: 1e-15, w: _sp.sqrt((1e-15)**2*2)/(3e8), c: 3e8}
# 用约束求 ω： ω = c/√(A²+b²)
w_num = (3e8)/_sp.sqrt(2*(1e-15)**2)
v = {A:1e-15, b:1e-15, w:float(w_num), c:3e8}
spd = float(speed.subs(v))
kap = float(kappa.subs(v))
tau_v = float(tau.subs(v))
print("\n=== 数值核验 (A=1e-15, b=1e-15) ===")
print(f"|R'|={spd:.6e},  c={v[c]:.6e}, 相对差={abs(spd-v[c])/v[c]:.3e}")
print(f"κ={kap:.6e},  κ闭式Aω²/c²={(v[A]*v[w]**2/v[c]**2):.6e}")
print(f"τ={tau_v:.6e}, τ闭式bω²/c²={(v[b]*v[w]**2/v[c]**2):.6e}")
print(f"κ²+τ²={kap**2+tau_v**2:.6e}, ω²/c²={(v[w]**2/v[c]**2):.6e}")
print(f"tanθ=τ/κ={tau_v/kap:.6e}, b/A={v[b]/v[A]:.6e}")
