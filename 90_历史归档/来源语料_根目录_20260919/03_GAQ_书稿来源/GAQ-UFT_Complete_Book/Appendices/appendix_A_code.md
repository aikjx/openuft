# 附录 A 全部 200 位精度 Python 仿真代码（书籍内印刷版）

> 本附录收录 `Supplemental_Code/` 下的全部脚本，供读者脱离电子设备直接在书中查阅。全部脚本依赖 `mpmath`（高精度）与 `numpy/matplotlib`（可视化）。

## A.1 frenet_high_prec.py — Frenet–Serret 200 位精度求解器

```python
"""
GAQ‑UFT Supplemental: Frenet‑Serret 200‑digit precision solver
Generalized Kakeya Helical Vacuum Unified Field Theory
"""
import mpmath as mp
mp.mp.dps = 200

def diff_central(f, t, h=mp.mpf("1e-120")):
    return (f(t+h)-f(t-h))/(2*h)

def cross3(a,b):
    return mp.matrix([
        a[1]*b[2]-a[2]*b[1],
        a[2]*b[0]-a[0]*b[2],
        a[0]*b[1]-a[1]*b[0]
    ])

def frenet_decompose(curve_func, t):
    r1 = diff_central(curve_func, t)
    r2 = diff_central(lambda s: diff_central(curve_func,s), t)
    r3 = diff_central(lambda s: diff_central(lambda u: diff_central(curve_func,u),s), t)
    dr = mp.norm(r1)
    T = r1 / dr
    r1xr2 = cross3(r1,r2)
    cr_norm = mp.norm(r1xr2)
    kappa = cr_norm/(dr**3)
    N = cross3(r1, r1xr2)/(dr*cr_norm)
    B = cross3(T,N)
    triple = (r1xr2.T * r3)[0,0]
    tau = triple/(cr_norm**2)
    return T,N,B,kappa,tau

def gamma_var(t):
    Rt = mp.mpf("2.0") + mp.mpf("0.2")*mp.sin(t)
    x = Rt*mp.cos(t); y = Rt*mp.sin(t); z = mp.mpf("0.8")*t + mp.mpf("0.1")*mp.cos(t)
    return mp.matrix([x,y,z])

def helix_const(t,R=1,omega=1,c=1):
    return mp.matrix([R*mp.cos(omega*t), R*mp.sin(omega*t), c*t])

if __name__=="__main__":
    for ti in [mp.mpf("0"), mp.pi/3, mp.pi/2, mp.pi]:
        T,N,B,kap,tau = frenet_decompose(gamma_var, ti)
        print(f"t={ti:.4f}  κ={kap:.14f}  τ={tau:.14f}  τ/κ={tau/kap:.14f}")
```

## A.2 geometry_verify.py — 引电统一量纲与数值校验

```python
import mpmath as mp
mp.mp.dps=120
G = mp.mpf("6.67430e-11"); eps0 = mp.mpf("8.8541878128e-12"); c = mp.mpf("299792458")
def dim_check_Geps0():
    Geps0 = G*eps0
    print(f"G*ε0 = {Geps0:.20e}"); return Geps0
if __name__=="__main__":
    dim_check_Geps0()
```

## A.3 koide_simulation.py — Koide 关系数值扫描

```python
import mpmath as mp
mp.mp.dps = 100
me = mp.mpf("0.51099895000"); mmu = mp.mpf("105.6583755"); mtau = mp.mpf("1776.86")
def koide_formula(m1,m2,m3):
    lhs = m1+m2+m3
    rhs = (2/3)*(mp.sqrt(m1)+mp.sqrt(m2)+mp.sqrt(m3))**2
    return lhs, rhs, abs(lhs-rhs)/lhs
if __name__=="__main__":
    L,R,err = koide_formula(me,mmu,mtau)
    print(f"LHS = {L:.8f}\nRHS = {R:.8f}\nrelative error = {err:.8e}")
```

## A.4 plot_helix_3d.py — 3D 螺旋可视化

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
t = np.linspace(0, 12*np.pi, 2000)
x = np.cos(t); y = np.sin(t); z = t
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111,projection='3d')
ax.plot(x,y,z,lw=0.8)
ax.set_title("Cylindrical circular helix — GAQ‑UFT vacuum generator")
plt.show()
```

---

*（附录 A 完。完整可运行版本见 `Supplemental_Code/`，与本书同源维护。）*
