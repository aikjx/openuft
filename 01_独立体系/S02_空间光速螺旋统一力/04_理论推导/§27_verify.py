# -*- coding: utf-8 -*-
"""
§27_verify.py — 阈值链补齐与 M_Hc 通道自洽化（numpy 向量化版）
S02 空间光速螺旋统一力 · 算法联盟
V1  文献参考复现：SM+gaugino 两循环 + gaugino 阈值(eq18) + GUT 阈值(eq17)
    → M_GUT, M_Hc（对照 1304.0343 Fig1: M_S=1TeV, M₂=200GeV, M₃/M₂=3.5, tanβ=3
       → M_Hc∈[8.6e14,1.4e15]）
V1b Hc 入 β 迭代（M_Hc→M_GUT 区间 Hc 一循环贡献）
V2  M_S 标度：M_Hc 随 M_S 上升（文献 Fig1 特性）；M_X²M_Σ 与 M_S 无关（eq21）
V3  §25 预言带 [0.2298,0.2318] 与阈值链交叉验证
V4  判定
"""
import json, math, os
import numpy as np

alpha_em_MS = 1.0/127.925
alpha_s_MS  = 0.1184
mZ = 91.1876
v = 246.22
mt_mZ, mb_mZ, mtau = 163.7, 2.85, 1.776
C_dr = np.array([0.0, 2.0/(12*math.pi), 3.0/(12*math.pi)])

b_SM   = np.array([41.0/10, -19.0/6, -7.0])
b_gaug = np.array([0.0, 4.0/3, 2.0])
b_SMG  = b_SM + b_gaug
b2_SM  = np.array([[199.0/50, 27.0/10, 44.0/5],[9.0/10, 35.0/6, 12.0],[11.0/10, 9.0/2, -26.0]])
b2_gaug= np.array([[0,0,0],[0,64.0/3,0],[0,0,48.0]])
b2_SMG = b2_SM + b2_gaug
c_SM   = np.array([[17.0/10, 1.0/2, 3.0/2],[3.0/2, 3.0/2, 1.0/2],[2.0, 2.0, 0.0]])
b_MSSM  = np.array([33.0/5, 1.0, -3.0])
b2_MSSM = np.array([[199.0/25, 27.0/5, 88.0/5],[9.0/5, 25.0, 24.0],[11.0/5, 9.0, 14.0]])
c_MSSM  = np.array([[26.0/5, 14.0/5, 18.0/5],[6.0, 6.0, 2.0],[4.0, 4.0, 0.0]])
b_Hc = np.array([35.0/18, 2.0/3, 1.0])

B = {"SMG": (b_SMG, b2_SMG, c_SM), "MSSM": (b_MSSM, b2_MSSM, c_MSSM),
     "MSSM_Hc": (b_MSSM + b_Hc, b2_MSSM, c_MSSM)}

def deriv(st, mode):
    a, y = st[:3], st[3:]
    bvec, b2mat, cmat = B[mode]
    d = (bvec/(2*math.pi)) * a**2
    d += (1.0/(8*math.pi**2)) * a**2 * (b2mat @ a)
    d -= (1.0/(32*math.pi**3)) * a**2 * (cmat @ (y**2))
    g1sq, g2sq, g3sq = 4*math.pi*a
    if mode == "SMG":
        dyt   = y[0]*(4.5*y[0]**2 + 1.5*y[1]**2 + y[2]**2 - (17.0/20)*g1sq - (9.0/4)*g2sq - 8*g3sq)
        dyb   = y[1]*(1.5*y[0]**2 + 4.5*y[1]**2 + y[2]**2 - (1.0/4)*g1sq - (9.0/4)*g2sq - 8*g3sq)
        dytau = y[2]*(3*y[0]**2 + 3*y[1]**2 + 2.5*y[2]**2 - (9.0/4)*g1sq - (9.0/4)*g2sq)
    else:
        dyt   = y[0]*(6*y[0]**2 + y[1]**2 - (13.0/15)*g1sq - 3*g2sq - (16.0/3)*g3sq)
        dyb   = y[1]*(6*y[1]**2 + y[0]**2 + y[2]**2 - (7.0/15)*g1sq - 3*g2sq - (16.0/3)*g3sq)
        dytau = y[2]*(3*y[1]**2 + 4*y[2]**2 - (9.0/5)*g1sq - 3*g2sq)
    return np.concatenate([d, np.array([dyt, dyb, dytau])/(16*math.pi**2)])

def rk4(st, h, mode):
    k1 = deriv(st, mode); k2 = deriv(st+0.5*h*k1, mode)
    k3 = deriv(st+0.5*h*k2, mode); k4 = deriv(st+h*k3, mode)
    return st + (h/6.0)*(k1+2*k2+2*k3+k4)

def ms_to_dr(aMS):
    return aMS/(1.0 - aMS*C_dr)

def init_state(s2w):
    c2 = 1.0 - s2w
    a = ms_to_dr(np.array([(5.0/3)*alpha_em_MS/c2, alpha_em_MS/s2w, alpha_s_MS]))
    y = np.array([math.sqrt(2)*mt_mZ/v, math.sqrt(2)*mb_mZ/v, math.sqrt(2)*mtau/v])
    return np.concatenate([a, y])

def run_chain(s2w, tanb, M_S, M2, M3, ln_high, MHc=None, steps=500, nsm=250):
    st = init_state(s2w)
    lnS = math.log(M_S); lnlo = math.log(mZ)
    h1 = (lnS - lnlo)/nsm
    for k in range(nsm):
        st = rk4(st, h1, "SMG")
    ia = 1.0/st[:3]
    ia[1] -= (2.0/(3*math.pi))*math.log(M_S/M2)
    ia[2] -= (1.0/math.pi)*math.log(M_S/M3)
    st = np.concatenate([1.0/ia, st[3:]])
    sinb = math.sin(math.atan(tanb)); cosb = math.cos(math.atan(tanb))
    st = np.concatenate([st[:3], [st[3]/sinb, st[4]/cosb, st[5]/cosb]])
    if ln_high <= lnS + 1e-12:
        return st
    if MHc is None:
        h2 = (ln_high - lnS)/steps
        for k in range(steps):
            st = rk4(st, h2, "MSSM")
    else:
        lnH = math.log(MHc)
        if lnH <= lnS + 1e-12:
            h2 = (ln_high - lnS)/steps
            for k in range(steps):
                st = rk4(st, h2, "MSSM")
            return st
        n1 = max(1, min(steps, int(round((lnH - lnS)/(ln_high - lnS)*steps))))
        h2 = (lnH - lnS)/n1
        for k in range(n1):
            st = rk4(st, h2, "MSSM")
        n2 = steps - n1
        if n2 > 0:
            h3 = (ln_high - lnH)/n2
            for k in range(n2):
                st = rk4(st, h3, "MSSM_Hc")
    return st

def find_cross(s2w, tanb, M_S, M2, M3, MHc=None, iters=24):
    lo, hi = math.log(M_S), math.log(5e17)
    st_lo = run_chain(s2w, tanb, M_S, M2, M3, lo, MHc)
    f_lo = st_lo[0] - st_lo[1]
    for _ in range(iters):
        mid = 0.5*(lo+hi)
        st_mid = run_chain(s2w, tanb, M_S, M2, M3, mid, MHc)
        f_mid = st_mid[0] - st_mid[1]
        if f_lo*f_mid < 0: hi = mid
        else: lo = mid; f_lo = f_mid
    lnG = 0.5*(lo+hi)
    return lnG, run_chain(s2w, tanb, M_S, M2, M3, lnG, MHc)

def masses_from_crossing(lnG, stG):
    ia = 1.0/stG[:3]
    mu = math.exp(lnG)
    c1 = 3*ia[1] - 2*ia[2] - ia[0]
    c2 = 5*ia[0] - 3*ia[1] - 2*ia[2]
    # eq(17) 换算 1/α：c1 = −(6/5π)ln(μ/M_Hc) → M_Hc = μ·exp(+(5π/6)c1)
    #                c2 = −(6/π)ln(μ³/(M_X²M_Σ)) → (M_X²M_Σ)^(1/3) = μ·exp(+(π/18)c2)
    MHc = mu*math.exp((5*math.pi/6.0)*c1)
    MGeff = mu*math.exp((math.pi/18.0)*c2)
    return MHc, MGeff, c1, c2

def solve_chain(s2w, tanb, M_S, M2, M3, Hc_iter=0):
    lnG, stG = find_cross(s2w, tanb, M_S, M2, M3)
    MHc, MGeff, c1, c2 = masses_from_crossing(lnG, stG)
    seq = [MHc]
    for _ in range(Hc_iter):
        lnG, stG = find_cross(s2w, tanb, M_S, M2, M3, MHc)
        MHc, MGeff, c1, c2 = masses_from_crossing(lnG, stG)
        seq.append(MHc)
    return math.exp(lnG), MHc, stG, c1, c2, seq

print("="*70)
print("§27 阈值链补齐与 M_Hc 通道自洽化（numpy）", flush=True)
print("="*70, flush=True)

print("\n[V1] 文献参考复现（M_S=1TeV, M₂=200GeV, M₃/M₂=3.5, tanβ=3, s²=0.23122）:", flush=True)
MG, MHc, stG, c1, c2, seq = solve_chain(0.23122, 3.0, 1000.0, 200.0, 700.0)
print("  M_GUT = %.4e GeV（α₁=α₂ 交叉, 无 Hc 入 β）" % MG, flush=True)
print("  δ=α₃/α₁−1 = %+.2e（交叉处失配，由 Hc 阈值吸收）" % (stG[2]/stG[0]-1.0), flush=True)
print("  M_Hc(无 Hc 入 β) = %.3e GeV   comb1=%+.4f" % (MHc, c1), flush=True)
_, MGeff, _, _ = masses_from_crossing(math.log(MG), stG)
print("  M_X²M_Σ^(1/3) = %.3e GeV（对照 M_GUT=%.3e）" % (MGeff, MG), flush=True)
a_s_orig = alpha_s_MS
print("  α_s=0.1184±0.0007 带:", flush=True)
band = []
for das in (-0.0007, 0.0, +0.0007):
    alpha_s_MS = a_s_orig + das
    lnG_t, stG_t = find_cross(0.23122, 3.0, 1000.0, 200.0, 700.0)
    MHc_t, _, _, _ = masses_from_crossing(lnG_t, stG_t)
    band.append(MHc_t)
    print("    α_s=%.7f: M_Hc≈%.2e  M_GUT≈%.2e" % (alpha_s_MS, MHc_t, math.exp(lnG_t)), flush=True)
alpha_s_MS = a_s_orig
print("  文献（1304.0343 Fig1 蓝线）: M_Hc ∈ [8.6e14, 1.4e15] GeV", flush=True)
print("  ★ 复现判定: 计算带 [%.2e, %.2e] vs 文献 [8.6e14, 1.4e15]" % (min(band), max(band)), flush=True)

print("\n[V1b] Hc 入 β 迭代敏感性与文献 M_GUT≈2e16 对照:", flush=True)
MGb, MHcb, _, _, _, seqb = solve_chain(0.23122, 3.0, 1000.0, 200.0, 700.0, Hc_iter=1)
print("  M_Hc 迭代: %s → %s" % ("%.2e"%seqb[0], "%.2e"%seqb[1]), flush=True)
print("  Hc 入 β 后: M_GUT=%.3e  M_Hc=%.3e（约定差异一个量级，如实披露）" % (MGb, MHcb), flush=True)

print("\n[V2] M_S 标度（M₂=200, M₃/M₂=3.5, tanβ=3, s²=0.23122, 无 Hc 链）:", flush=True)
rows = []
for M_S in (1.0e3, 1.0e4, 1.0e5, 1.0e6):
    MG2, MHc2, _, _, _, _ = solve_chain(0.23122, 3.0, M_S, 200.0, 700.0)
    rows.append((M_S, MG2, MHc2))
    print("  M_S=%.0e TeV: M_GUT=%.3e  M_Hc=%.2e  (M_Hc/M_GUT=%.3f)" % (M_S/1000.0, MG2, MHc2, MHc2/MG2), flush=True)

print("\n[V3] §25 预言带 [0.2298,0.2318] × 阈值链（参考谱, 无 Hc 链）:", flush=True)
s2map = []
for s2 in (0.2298, 0.23122, 0.2318):
    MG3, MHc3, _, _, _, _ = solve_chain(s2, 3.0, 1000.0, 200.0, 700.0)
    s2map.append((s2, MG3, MHc3))
    print("  s²=%.4f: M_GUT=%.3e  M_Hc=%.2e" % (s2, MG3, MHc3), flush=True)

print("\n[V4] 判定:", flush=True)
hit = min(band) <= 1.4e15 and max(band) >= 8.6e14
print("  M_Hc 计算带 [%.2e, %.2e] %s 文献 [8.6e14,1.4e15] → §26 失效边界修复判定: %s"
      % (min(band), max(band), "命中" if hit else "未命中", "已修复" if hit else "未修复"), flush=True)
print("  S02 零参与；定级维持组织性语言", flush=True)

data = {"V1": {"M_GUT": MG, "M_Hc": MHc, "seq": seq, "comb1": c1, "delta": stG[2]/stG[0]-1.0,
               "MGeff": MGeff, "lit_lo": 8.6e14, "lit_hi": 1.4e15},
        "V2": [{"M_S": r[0], "M_GUT": r[1], "M_Hc": r[2]} for r in rows],
        "V3": [{"s2": s2, "M_Hc": solve_chain(s2,3.0,1000.0,200.0,700.0)[1]} for s2 in (0.2298,0.23122,0.2318)]}
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "§27_阈值链数据.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("\n数据已写入: §27_阈值链数据.json")
