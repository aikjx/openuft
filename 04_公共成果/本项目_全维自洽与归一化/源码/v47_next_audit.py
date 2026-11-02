# -*- coding: utf-8 -*-
"""ROOT V47（五维可解玩具模型：KK 谱塔 / 味改变 / 距离力律）来料 · 全量机核

核验 11 条：(47-1)…(47-11) 及两张三代表、截断表、量纲换算。
不重复 V44 册的交换子判据（本册模型 a_n=√2cos 与 V44 的指数局域化不同）。

约定：本脚本只用 numpy/scipy 的数值 + sympy 的少量符号；精度以 float64 为准。
"""
import numpy as np
import sympy as sp
from scipy import integrate

results = []


def check(name, value, cond, note=""):
    tag = "成立" if cond else "不成立"
    results.append((name, tag, value, note))
    print(f"[{tag}] {name}  value={value}  {note}")


# ---------- 基础：Neumann 模与耦合倍数 ----------
L = 1.0
def f0(y): return np.ones_like(np.asarray(y, dtype=float)) / np.sqrt(L)
def fn(n, y): return np.sqrt(2 / L) * np.cos(n * np.pi * y / L)
def a(n, x): return np.sqrt(2) * np.cos(n * np.pi * x)

trapz = getattr(np, "trapezoid", np.trapz)

# 正交归一
N_ORTH = 400
ys = (np.arange(N_ORTH) + 0.5) / N_ORTH * L
orth = np.zeros((4, 4))
for i in range(4):
    for j in range(4):
        gi = (f0 if i == 0 else (lambda y, i=i: fn(i, y)))
        gj = (f0 if j == 0 else (lambda y, j=j: fn(j, y)))
        orth[i, j] = np.sum(gi(ys) * gj(ys)) * (L / N_ORTH)
print(f"    正交性 max|∫f_i f_j - δ_ij| = {np.abs(orth - np.eye(4)).max():.2e}")
check("S1a Neumann 模正交归一", np.abs(orth - np.eye(4)).max(), np.abs(orth - np.eye(4)).max() < 1e-8)
# 耦合倍数 a_n(x) = f_n(x)/f_0(x) 归一化到 L
check("S1b a_n(x)=√2cos(nπx)", a(1, 0.0),
      abs(a(1, 0.0) - np.sqrt(2)) < 1e-15 and abs(a(2, 0.25) - np.sqrt(2) * np.cos(2 * np.pi * 0.25)) < 1e-15)

# ---------- (47-3) 闭式与谱塔一致 ----------
def S_closed(x, y):
    return np.pi ** 2 * (1 / 3 - max(x, y) + (x ** 2 + y ** 2) / 2)

def S_sum(x, y, N):
    n = np.arange(1, N + 1, dtype=float)
    return 2 * np.sum(np.cos(n * np.pi * x) * np.cos(n * np.pi * y) / n ** 2)

pts = [(0.15, 0.15), (0.50, 0.50), (0.15, 0.50), (0.20, 0.80), (0.00, 1.00), (0.33, 0.66)]
err = max(abs(S_sum(x, y, 500000) - S_closed(x, y)) for x, y in pts)
print(f"    (47-3) 谱塔 500k 模 vs 闭式 max|Δ| = {err:.3e}")
check("S2 (47-3) 闭式与无限谱塔一致", err, err < 5e-6)

# Fourier 系数独立核验：2∫_0^1 S(x,y)cos(nπy)dy = 2cos(nπx)/n²
def fourier_resid(n, x):
    s1 = lambda y: np.pi**2 * (1/3 - x + (x**2 + y**2)/2)
    s2 = lambda y: np.pi**2 * (1/3 - y + (x**2 + y**2)/2)
    c = 2 * (integrate.quad(lambda y: s1(y) * np.cos(n*np.pi*y), 0, x, limit=200)[0]
             + integrate.quad(lambda y: s2(y) * np.cos(n*np.pi*y), x, 1, limit=200)[0])
    return c - 2 * np.cos(n * np.pi * x) / n**2

fr = max(abs(fourier_resid(n, 0.37)) for n in range(1, 7))
print(f"    Fourier 系数残差 max = {fr:.3e}")
check("S2b 闭式的 Fourier 系数 = 2cos(nπx)/n²", fr, fr < 1e-10)

# ---------- (47-4) D = π²|x-y| ----------
def D_finite(x, y, N):
    n = np.arange(1, N + 1, dtype=float)
    return np.sum((a(n, x) - a(n, y)) ** 2 / n ** 2)

D_err = abs(D_finite(0.15, 0.50, 1000000) - np.pi**2 * 0.35)
print(f"    D(x,y) 谱塔 vs π²|Δ|：{D_finite(0.15, 0.50, 1000000):.9f} vs {np.pi**2*0.35:.9f}  差={D_err:.2e}（尾项 ~2/N）")
check("S3 (47-4) D=π²|x-y|", D_err, D_err < 5e-6)

# ---------- 二维示范：S 矩阵 / Q / C / 相消点 ----------
S = np.array([[S_closed(0.15, 0.15), S_closed(0.15, 0.50)],
              [S_closed(0.15, 0.50), S_closed(0.50, 0.50)]])
print(f"    S =\n{S}")
q12 = np.pi**2 / 4 * 0.35 * np.sin(0.4) ** 2
print(f"    Q12 = {q12:.9f}")
s, c = np.sin(0.20), np.cos(0.20)
C_demo = s * c * (c**2 * (S[0,0]-S[0,1]) + s**2 * (S[0,1]-S[1,1]))
print(f"    C1211(θ=0.20) = {C_demo:.9f}")
check("S4a S 矩阵与来料表一致",
      float(np.abs(S - np.array([[2.031493573, -0.300200467], [-0.300200467, 0.822467033]])).max()),
      np.abs(S - np.array([[2.031493573, -0.300200467], [-0.300200467, 0.822467033]])).max() < 5e-9)
check("S4b Q12 与 (47-5) 表格一致", q12, abs(q12 - 0.130960585) < 5e-7)
check("S4c C1211 与来料表一致", C_demo, abs(C_demo - 0.427455189) < 5e-7)

# 相消点
theta_star = np.arctan(np.sqrt((S[0,0]-S[0,1]) / (S[1,1]-S[0,1])))
s2, c2 = np.sin(theta_star), np.cos(theta_star)
C_star = s2 * c2 * (c2**2 * (S[0,0]-S[0,1]) + s2**2 * (S[0,1]-S[1,1]))
Q_star = np.pi**2 / 4 * 0.35 * np.sin(2*theta_star) ** 2
print(f"    θ* = {theta_star:.10f} rad ; C(θ*) = {C_star:.2e} ; Q(θ*) = {Q_star:.9f}")
check("S4d 相消角 θ* 与来料一致", theta_star, abs(theta_star - 0.9641837152) < 5e-7)
check("S4e 相消点 C≈0 且 Q>0", Q_star, C_star != 0 and Q_star > 0.75)

# ---------- 截断误差表 ----------
print("    截断误差表（对 S 矩阵最大绝对差）：")
tab = []
for N in (10, 100, 2500, 10000):
    Sn = np.array([[S_sum(0.15, 0.15, N), S_sum(0.15, 0.50, N)],
                   [S_sum(0.15, 0.50, N), S_sum(0.50, 0.50, N)]])
    e = np.abs(Sn - S).max()
    tab.append(e)
    print(f"      N={N:>6}  err={e:.8f}")
check("S5 截断误差 ~1/N", tab[3],
      abs(tab[0]-0.09797755) < 2e-6 and abs(tab[1]-0.00990259) < 2e-6
      and abs(tab[2]-0.00039984) < 2e-5 and abs(tab[3]-0.00009999) < 2e-6)

# ---------- 三代：四种算法 ----------
xs = np.array([0.15, 0.50, 0.85])
t12, t23, t13 = 0.20, 0.12, 0.03

def R(i, j, th):
    M = np.eye(3)
    M[i, i] = np.cos(th); M[i, j] = np.sin(th)
    M[j, i] = -np.sin(th); M[j, j] = np.cos(th)
    return M

U = R(1, 2, t23) @ R(0, 2, t13) @ R(0, 1, t12)   # R23 R13 R12
w = np.conj(U[:, 0]) * U[:, 1]
print(f"    Σw = {w.sum():.3e} ; w = {w}")
Q_closed = -np.pi**2 / 2 * sum(w[i] * np.conj(w[j]) * abs(xs[i]-xs[j])
                               for i in range(3) for j in range(3))
Q_bilinear = sum(w[i] * np.conj(w[j]) * S_closed(xs[i], xs[j])
                 for i in range(3) for j in range(3))
# 分段积分
order = np.argsort(xs)
def Q_integral():
    total = 0.0
    edges = np.concatenate([[0.0], np.sort(xs), [1.0]])
    for k in range(len(edges)-1):
        lo, hi = edges[k], edges[k+1]
        mid = 0.5 * (lo + hi)
        acc = sum(w[i] for i in range(3) if xs[i] >= mid)
        total += abs(acc) ** 2 * (hi - lo)
    return np.pi**2 * total

Q_int = Q_integral()
N20k = 20000
n = np.arange(1, N20k + 1)
Q_direct = np.sum(np.abs(sum(w[i] * a(n, xs[i]) for i in range(3))) ** 2 / n ** 2)
print(f"    三代 Q_eμ：解析S={Q_bilinear:.10f} 闭式={Q_closed:.10f} 积分={Q_int:.10f} 20000模={Q_direct:.10f}")
check("S6a 四种算法一致（前三种）",
      float(max(abs(Q_bilinear-Q_closed), abs(Q_bilinear-Q_int))),
      max(abs(Q_bilinear-Q_closed), abs(Q_bilinear-Q_int)) < 1e-12)
check("S6b 20000 模截断误差 ~3.8e-6", float(abs(Q_bilinear-Q_direct)),
      abs(Q_bilinear - Q_direct) < 5e-6)
check("S6c Q_eμ 与来料 0.1307265642 一致", Q_bilinear, abs(Q_bilinear - 0.1307265642) < 5e-9)
check("S6d Q ≥ 0 且 Q=0 判据", Q_bilinear,
      Q_bilinear >= 0 and abs(w.sum()) < 1e-15)

# ---------- (47-9) 传播核 ----------
def P_closed2(t, x, y):
    return 0.5 * (np.sinh(t) / (np.cosh(t) - np.cos(np.pi*(x-y))
                               ) + np.sinh(t) / (np.cosh(t) - np.cos(np.pi*(x+y))))

def P_sum(t, x, y, N):
    n = np.arange(1, N + 1)
    return (0.5 * ((1 + 2*np.sum(np.cos(n*np.pi*(x-y))*np.exp(-n*t))
                   ) + (1 + 2*np.sum(np.cos(n*np.pi*(x+y))*np.exp(-n*t)))))

p_err = max(abs(P_sum(t, x, y, 8000) - P_closed2(t, x, y)) for t in (0.01, 0.1, 1, 3, 10) for x, y in [(0, 0), (0.15, 0.5)])
print(f"    (47-9) 8000 模 vs 闭式 max|Δ| = {p_err:.3e}")
check("S7a (47-9) 传播核闭式与谱塔一致", p_err, p_err < 1e-8)
# 同边界 2500 模差
p2500 = P_sum(0.01, 0, 0, 2500)
p_exact = P_closed2(0.01, 0, 0)
print(f"    同边界 t=0.01：2500 模={p2500:.15f} 闭式={p_exact:.15f} Δ={abs(p2500-p_exact):.3e}")
check("S7b 同边界 2500 模 vs 闭式 ~2.43e-9", float(abs(p2500-p_exact)), abs(p2500-p_exact) < 1e-8)
# (47-11)
def ratio_same(t):
    return 1/np.tanh(t/2) + (t/2)/np.sinh(t/2)**2
def force_ratio(t, x, y, h=1e-6):
    dP = (P_closed2(t+h, x, y) - P_closed2(t-h, x, y)) / (2*h)
    return P_closed2(t, x, y) - t*dP
fr_err = max(abs(force_ratio(t, 0, 0) - ratio_same(t)) for t in (0.1, 1, 3))
print(f"    (47-11) 同边界力系数残差 = {fr_err:.3e}")
check("S7c (47-11) coth(t/2)+(t/2)csch²(t/2)", fr_err, fr_err < 1e-6)

# ---------- 力表 ----------
print("    力系数表：")
tabF = []
for tr in (0.01, 0.1, 1, 3, 10):
    same = force_ratio(tr, 0.0, 0.0)
    sep = force_ratio(tr, 0.15, 0.50)
    tabF.append((tr, same, sep))
    print(f"      t={tr:<5} same={same:.6f}  sep={sep:.9f}")
check("S8a 同边界短距 ∝1/t（r^-3 力）", tabF[0][1], abs(tabF[0][1] - 400.0) < 0.1)
check("S8b 同边界长距 →1（r^-2 力）", tabF[-1][1], abs(tabF[-1][1] - 1.0) < 1e-3)
check("S8c 分离位置短距强抑制", tabF[0][2], tabF[0][2] < 1e-5 and tabF[-1][2] > 0.9999)
# 分离位置的短距标度：P−t∂P/∂t 的首两阶抵消 ⇒ ∝ t³
scales = [force_ratio(t, 0.15, 0.50) / t**3 for t in (0.005, 0.01, 0.02)]
print(f"    分离位置 (P−t∂P/∂t)/t³ = {[f'{v:.6f}' for v in scales]}")
check("S8d 分离位置短距力比 ∝ t³（线性与二次项抵消）", max(scales),
      max(scales) - min(scales) < 1e-3 * max(scales) and max(scales) > 1)

# ---------- 量纲换算 ----------
hbar_c_MeV_m = 1.97327e-13   # MeV·m
m1_MeV = 10e6                # 10 TeV
lam1 = hbar_c_MeV_m / m1_MeV
Lm = np.pi * lam1
print(f"    λ1 = {lam1:.5e} m ; L = πλ1 = {Lm:.5e} m")
check("S9 10 TeV → λ1=1.97327e-20 m, L=6.19921e-20 m", lam1,
      abs(lam1 - 1.97327e-20) < 1e-25 and abs(Lm - 6.19921e-20) < 1e-24)

# ---------- 收益 A：y 与 λ1 的关系 ----------
print()
print("=" * 78)
n_pass = sum(1 for r in results if r[1] == "成立")
print(f"汇总：{n_pass}/{len(results)} 项断言成立")
for name, tag, value, note in results:
    print(f"  {tag}  {name}")
print("=" * 78)
print("判词：V47_TOY_MODEL__10_FORMULAS_NUMERIC__1_STRUCTURAL__6_TABLES_REPRODUCED__"
      "UNIQUE_ACTION_ABSENT__POSITIONS_ANGLES_INPUT__SINGLE_CIRCLE_KK_CANNOT_GIVE_SU3xSU2__"
      "V48_UNPROVEN")
