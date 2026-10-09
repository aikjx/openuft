# -*- coding: utf-8 -*-
"""
v42：黑洞热力学挠率熵（来稿分支④）· Wald 熵公式推导 + 数值估计
作用量（31 稿修复版非最小耦合扇区）：L = (1/16πG)R + (g/2) τ R  [+ 动力学 τ 项]
Wald 熵：S = -2π ∮_H (∂L/∂R_abcd) ε_ab ε_cd dA
∂R/∂R_abcd = (g^ac g^bd - g^ad g^bc)/2；ε_ab 为视界双法向，ε_ab ε^ab = -2
=> S = (A/4G)(1 + 8πG g τ_H)，τ_H 为视界处挠率标量。
"""
import json
import numpy as np
from sympy import symbols, Rational, pi, simplify

G = symbols('G', positive=True)
g = symbols('g', real=True)
tau = symbols('tau', real=True)
A = symbols('A', positive=True)

# ---- sympy: 缩并 (∂R/∂R_abcd) ε_ab ε_cd 常数 ----
# 双法向约定 ε_ab ε^ab = -2；g^ac g^bd ε_ab ε_cd = ε_ab ε^ab = -2
# g^ad g^bc ε_ab ε_cd = ε_ab ε^ba = +2
scontraction = Rational(1, 2) * ((-2) - (2))   # (1/2)(g^ac g^bd - g^ad g^bc)εε = (1/2)(-2-2) = -2
print("缩并 (∂R/∂R_abcd) ε_ab ε_cd =", scontraction)

# Wald 熵：S = -2π ∮ f' · (∂R/∂R_abcd)εε dA = -2π f' · (-2) · A = +4π f' A, f'=∂L/∂R
# f' = 1/(16πG) + g τ_H/2
S = 4 * pi * (1/(16*pi*G) + g*tau/2) * A
print("Wald 熵公式 S =", S, " = (A/4G)(1 + 8πG g τ_H):", simplify(S - A/(4*G)*(1 + 8*pi*G*g*tau)))

# ---- 数值估计 ----
G_norm = 1.0/(16*np.pi)   # 普朗克归一 16πG=1
def factor(gv, tv): return 1 + 8*np.pi*G_norm*gv*tv
scan = {}
for glab, gv, tv in [("g=0.01,τ=1",0.01,1.0),("g=0.1,τ=1",0.1,1.0),("g=1,τ=1",1.0,1.0),
                     ("g=0.1,τ=10",0.1,10.0),("g=0.1,τ=-1",0.1,-1.0)]:
    scan[glab] = {"g":gv,"tau_H":tv,"8piG_g_tau":8*np.pi*G_norm*gv*tv,"factor":float(factor(gv,tv))}
    print("  %-12s 8πG gτ=%+.4f  修正因子=%+.4f" % (glab, scan[glab]["8piG_g_tau"], scan[glab]["factor"]))

rec = {
    "action": "L = (1/16πG)R + (g/2) τ R (31 稿修复版非最小耦合扇区)",
    "wald_formula": "S = -2π∮(∂L/∂R_abcd) ε_ab ε_cd dA",
    "contraction": int(scontraction),
    "result_formula": "S_H = (A/4G)(1 + 8πG g τ_H)",
    "correction_factor": "1 + 8πG g τ_H  (τ_H 视界挠率标量)",
    "scan": scan,
    "caveats": ["τ_H 需黑洞内部挠率解（未做完整黑洞解）", "符号依赖双法向约定", "第一定律/Hawking 温度需进一步核对"],
}
out = r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\空间螺旋几何化统一场论\V3_15_bh_torsion_entropy.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(rec, f, ensure_ascii=False, indent=2)
print("saved V3_15_bh_torsion_entropy.json")
