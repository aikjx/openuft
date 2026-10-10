# -*- coding: utf-8 -*-
"""
v46：含挠率标量的黑洞解（Schwarzschild 背景 + 挠率标量场，含线性源 η）
KG（球对称静态，Schwarzschild 背景，无量纲 M=1, r_H=2）：
  (1/r^2) d/dr [ r^2 (1-2/r) τ' ] - m^2 τ - η = 0
  渐近：τ -> -η/m^2（m^2≠0），加衰减 ~e^{-mr}/r
  视界 r_H=2 正则（τ 有限）。
解出 τ_H=τ(r_H)，代入 42/45 稿：S_H=(A/4G)(1+8πG g τ_H)、T_H=T_Sch/(1+8πG g τ_H)。
诚实边界：线性化、背景固定（忽略 τ 对度规反馈）；完整 EF 球对称解为后续。
"""
import os, json
import numpy as np
from scipy.integrate import solve_bvp

def kg_fun(r, y):
    tau, tp = y
    A = 1.0 - 2.0/r
    dAp = 2.0/r**2          # d/dr[(1-2/r)] = 2/r^2
    # (1/r^2) d/dr[r^2 A τ'] = m^2 τ + η
    # = A τ'' + (2/r A + A') τ' = A τ'' + (2/r)(1-2/r) + 2/r^2 τ'
    # => τ'' = [m^2 τ + η - (2/r A + A') τ'] / A
    coef = (2.0/r)*A + dAp
    return np.vstack((tp, (m2*tau + eta - coef*tp)/A))

def bc(ya, yb):
    # 视界正则：A(r_H)=0，要求分子为零：m^2 τ + η = 0 at r_H => τ(r_H)=-η/m^2（Dirichlet）
    # 无穷远渐近：τ -> -η/m^2（同样条件）
    return np.array([ya[0] - tau_inf, yb[0] - tau_inf])

def solve_one(m, eta, rmax=60.0):
    global m2, tau_inf
    m2 = m*m
    tau_inf = -eta/m2 if m2 > 1e-12 else 0.0
    r = np.linspace(2.0001, rmax, 400)
    y0 = np.zeros((2, r.size))
    y0[0] = tau_inf; y0[1] = 0.0
    sol = solve_bvp(kg_fun, bc, r, y0, max_nodes=20000, tol=1e-8)
    if not sol.success:
        return None, None, sol.message
    tau_H = float(sol.y[0, 0])      # r=r_H(2.0001) 近似视界
    tau_inf_v = tau_inf
    return tau_H, tau_inf_v, None

results = {}
print("含挠率标量黑洞解（Schwarzschild 背景，M=1, r_H=2）")
G_norm = 1.0/(16*np.pi)
for (mlab, m), (elab, eta) in [((0.1,0.1),(0.1,0.1)), ((0.5,0.5),(0.5,0.5)),
                                ((1.0,1.0),(1.0,1.0)), ((0.5,0.5),(0.1,0.1)),
                                ((0.1,0.1),(1.0,1.0))]:
    tau_H, tau_inf, err = solve_one(m, eta)
    if err:
        print("  m=%s η=%s: %s" % (m, eta, err)); continue
    # 熵/温度修正因子（g=0.1 示例）
    g = 0.1
    C = 1 + 8*np.pi*G_norm*g*tau_H
    key = "m=%s,eta=%s" % (m, eta)
    results[key] = {"tau_H": tau_H, "tau_inf": tau_inf, "g_example": g,
                    "C": float(C), "S_ratio": float(C), "T_ratio": float(1.0/C)}
    print("  m=%-4s η=%-4s τ_H=%+.4e  τ∞=%+.4e  (g=0.1) S修正=%.4f T修正=%.4f"
          % (m, eta, tau_H, tau_inf, C, 1.0/C))

rec = {"method": "KG on Schwarzschild, linear source η, M=1, r_H=2",
       "kg": "(1/r^2)d/dr[r^2(1-2/r)τ'] - m^2 τ - η = 0",
       "results": results,
       "caveats": ["线性化、背景固定（忽略 τ 对度规反馈）", "完整 EF 球对称解为后续",
                   "τ 无量纲、需定标物理能标", "g=0.1 示例"]}
out = r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\空间螺旋几何化统一场论\V3_17_bh_torsion_profile.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(rec, f, ensure_ascii=False, indent=2)
print("saved V3_17_bh_torsion_profile.json")
