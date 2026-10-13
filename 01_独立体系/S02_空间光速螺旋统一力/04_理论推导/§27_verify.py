# -*- coding: utf-8 -*-
"""
§27_verify.py — 阈值链补齐与 M_Hc 通道自洽化
S02 空间光速螺旋统一力 · 算法联盟
V1  文献参考复现：SM+gaugino 两循环跑动 + gaugino 阈值(eq18) + GUT 阈值(eq17)
    → M_GUT, M_Hc（对照 1304.0343 Fig1: M_S=1TeV, M₂=200GeV, M₃/M₂=3.5, tanβ=3
       → M_Hc∈[8.6e14,1.4e15]）
V1b Hc 入 β 迭代（M_Hc→M_GUT 区间加入 Hc 一循环贡献，二阶自洽）
V2  M_S 标度：M_Hc 随 M_S 上升（文献 Fig1 特性）；M_X²M_Σ 与 M_S 无关（eq21）
V3  §25 预言带 [0.2298,0.2318] 与阈值链交叉验证（s² 输入 → M_Hc 映射）
V4  判定：M_Hc 通道自洽闭合、§26 失效边界修复、S02 定级
"""
import json, math, os

# ---- 输入（与 §25 同套） ----
alpha_em_MS = 1.0/127.925
alpha_s_MS  = 0.1184
s2w_exp = 0.23122
mZ = 91.1876
v = 246.22
mt_mZ, mb_mZ, mtau = 163.7, 2.85, 1.776
C_dr = (0.0, 2.0/(12*math.pi), 3.0/(12*math.pi))

# ---- β 系数（1304.0343 eq12-15；SM+gaugino = b_SM + b_gaug） ----
b_SM   = (41.0/10, -19.0/6, -7.0)
b_gaug = (0.0, 4.0/3, 2.0)
b_SMG  = tuple(b_SM[i]+b_gaug[i] for i in range(3))
b2_SM  = ((199.0/50, 27.0/10, 44.0/5), (9.0/10, 35.0/6, 12.0), (11.0/10, 9.0/2, -26.0))
b2_gaug = ((0,0,0),(0,64.0/3,0),(0,0,48.0))
b2_SMG = tuple(tuple(b2_SM[i][j]+b2_gaug[i][j] for j in range(3)) for i in range(3))
c_SM   = ((17.0/10, 1.0/2, 3.0/2), (3.0/2, 3.0/2, 1.0/2), (2.0, 2.0, 0.0))
b_MSSM  = (33.0/5, 1.0, -3.0)
b2_MSSM = ((199.0/25, 27.0/5, 88.0/5), (9.0/5, 25.0, 24.0), (11.0/5, 9.0, 14.0))
c_MSSM  = ((26.0/5, 14.0/5, 18.0/5), (6.0, 6.0, 2.0), (4.0, 4.0, 0.0))
# Hc(5+5̄) 对 b 的一循环贡献：Δb=(35/18, 2/3, 1)（推导见文档 §2.2）
b_Hc = (35.0/18, 2.0/3, 1.0)
b_MSSM_Hc = tuple(b_MSSM[i]+b_Hc[i] for i in range(3))

def beta_gauge(a, y, mode, two_loop=True, with_yuk=True):
    if mode == "SMG":
        bvec, b2mat, cmat = b_SMG, b2_SMG, c_SM
    elif mode == "MSSM":
        bvec, b2mat, cmat = b_MSSM, b2_MSSM, c_MSSM
    else:  # MSSM_Hc
        bvec, b2mat, cmat = b_MSSM_Hc, b2_MSSM, c_MSSM
    out = []
    for i in range(3):
        d = (bvec[i]/(2*math.pi)) * a[i]**2
        if two_loop:
            s = sum(b2mat[i][j]*a[j] for j in range(3))
            d += (1.0/(8*math.pi**2)) * a[i]**2 * s
            if with_yuk:
                d -= (1.0/(32*math.pi**3)) * a[i]**2 * sum(cmat[i][k]*y[k]**2 for k in range(3))
        out.append(d)
    return out

def beta_yuk(y, a, mode):
    yt, yb, ytau = y
    g1sq, g2sq, g3sq = [4*math.pi*x for x in a]
    if mode == "SMG":
        dyt   = yt  * ((9.0/2)*yt**2 + (3.0/2)*yb**2 + ytau**2 - (17.0/20)*g1sq - (9.0/4)*g2sq - 8*g3sq)
        dyb   = yb  * ((3.0/2)*yt**2 + (9.0/2)*yb**2 + ytau**2 - (1.0/4)*g1sq - (9.0/4)*g2sq - 8*g3sq)
        dytau = ytau* (3*yt**2 + 3*yb**2 + (5.0/2)*ytau**2 - (9.0/4)*g1sq - (9.0/4)*g2sq)
    else:
        dyt   = yt  * (6*yt**2 + yb**2 - (13.0/15)*g1sq - 3*g2sq - (16.0/3)*g3sq)
        dyb   = yb  * (6*yb**2 + yt**2 + ytau**2 - (7.0/15)*g1sq - 3*g2sq - (16.0/3)*g3sq)
        dytau = ytau* (3*yb**2 + 4*ytau**2 - (9.0/5)*g1sq - 3*g2sq)
    return [dyt/(16*math.pi**2), dyb/(16*math.pi**2), dytau/(16*math.pi**2)]

def deriv(st, mode, two_loop=True, with_yuk=True):
    a, y = st[:3], st[3:]
    return beta_gauge(a, y, mode, two_loop, with_yuk) + (beta_yuk(y, a, mode) if with_yuk else [0,0,0])

def rk4(st, lnmu, h, mode, two_loop=True, with_yuk=True):
    k1 = deriv(st, mode, two_loop, with_yuk)
    k2 = deriv([st[i]+0.5*h*k1[i] for i in range(6)], mode, two_loop, with_yuk)
    k3 = deriv([st[i]+0.5*h*k2[i] for i in range(6)], mode, two_loop, with_yuk)
    k4 = deriv([st[i]+h*k3[i] for i in range(6)], mode, two_loop, with_yuk)
    return [st[i] + (h/6.0)*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(6)]

def ms_to_dr(aMS):
    return [aMS[i]/(1.0 - aMS[i]*C_dr[i]) for i in range(3)]

def yukawa_mZ():
    return [math.sqrt(2)*mt_mZ/v, math.sqrt(2)*mb_mZ/v, math.sqrt(2)*mtau/v]

def init_state(s2w):
    c2 = 1.0 - s2w
    return ms_to_dr([(5.0/3)*alpha_em_MS/c2, alpha_em_MS/s2w, alpha_s_MS]) + yukawa_mZ()

def gaugino_threshold(st, M_S, M2, M3):
    """eq(18) 换算成 1/α：1/α₂_MSSM = 1/α₂_SM − (2/(3π))ln(M_S/M₂)；1/α₃ 同理 −(1/π)ln(M_S/M₃)"""
    ia = [1.0/st[0], 1.0/st[1], 1.0/st[2]]
    ia[1] -= (2.0/(3*math.pi))*math.log(M_S/M2)
    ia[2] -= (1.0/math.pi)*math.log(M_S/M3)
    return [1.0/ia[0], 1.0/ia[1], 1.0/ia[2]] + list(st[3:])

def yukawa_match(st, tanb):
    sinb = math.sin(math.atan(tanb)); cosb = math.cos(math.atan(tanb))
    return list(st[:3]) + [st[3]/sinb, st[4]/cosb, st[5]/cosb]

def run_chain(s2w, tanb, M_S, M2, M3, ln_high, MHc=None, steps=900, two_loop=True):
    """m_Z →(SMG)→ M_S →(gaugino 阈值 + Yukawa 匹配)→(MSSM 或 MSSM+Hc)→ ln_high
       MHc 给定时 M_S→M_Hc 用 MSSM、M_Hc→ln_high 用 MSSM_Hc（Hc 入 β）。"""
    st = init_state(s2w)
    lnS = math.log(M_S); lnlo = math.log(mZ)
    h1 = (lnS - lnlo)/600
    for k in range(600):
        st = rk4(st, lnlo + k*h1, h1, "SMG", two_loop)
    st = gaugino_threshold(st, M_S, M2, M3)
    st = yukawa_match(st, tanb)
    if ln_high <= lnS + 1e-12:
        return st
    if MHc is None:
        h2 = (ln_high - lnS)/steps
        for k in range(steps):
            st = rk4(st, lnS + k*h2, h2, "MSSM", two_loop)
    else:
        lnH = math.log(MHc)
        if lnH <= lnS + 1e-12:
            h2 = (ln_high - lnS)/steps
            for k in range(steps):
                st = rk4(st, lnS + k*h2, h2, "MSSM", two_loop)
            return st
        n1 = max(1, int(round((lnH - lnS)/(ln_high - lnS)*steps)))
        h2 = (lnH - lnS)/n1
        for k in range(n1):
            st = rk4(st, lnS + k*h2, h2, "MSSM", two_loop)
        n2 = steps - n1
        h3 = (ln_high - lnH)/n2
        for k in range(n2):
            st = rk4(st, lnH + k*h3, h3, "MSSM_Hc", two_loop)
    return st

def find_cross(s2w, tanb, M_S, M2, M3, MHc=None):
    lo, hi = math.log(M_S), math.log(5e17)
    st_lo = run_chain(s2w, tanb, M_S, M2, M3, lo, MHc)
    f_lo = st_lo[0] - st_lo[1]
    for _ in range(35):
        mid = 0.5*(lo+hi)
        st_mid = run_chain(s2w, tanb, M_S, M2, M3, mid, MHc)
        f_mid = st_mid[0] - st_mid[1]
        if f_lo*f_mid < 0: hi = mid
        else: lo = mid; f_lo = f_mid
    lnG = 0.5*(lo+hi)
    stG = run_chain(s2w, tanb, M_S, M2, M3, lnG, MHc)
    return lnG, stG

def masses_from_crossing(lnG, stG):
    """eq(17) 换算 1/α 形式：3/α₂−2/α₃−1/α₁ = −(6/5π)ln(μ/M_Hc)
       5/α₁−3/α₂−2/α₃ = −(6/π)ln(μ³/(M_X²M_Σ))"""
    ia = [1.0/stG[0], 1.0/stG[1], 1.0/stG[2]]
    mu = math.exp(lnG)
    comb1 = 3*ia[1] - 2*ia[2] - ia[0]
    comb2 = 5*ia[0] - 3*ia[1] - 2*ia[2]
    MHc = mu*math.exp(-(5*math.pi/6.0)*comb1)
    MX2MS = mu**3*math.exp(-(math.pi/6.0)*comb2)
    return MHc, MX2MS**(1.0/3), comb1, comb2

def solve_chain(s2w, tanb, M_S, M2, M3, Hc_iter=2):
    """带 Hc 入 β 迭代的自洽解：M_Hc → 重跑（M_S→M_Hc MSSM, M_Hc→M_GUT MSSM+Hc）→ 新 M_Hc"""
    lnG, stG = find_cross(s2w, tanb, M_S, M2, M3, None)
    MHc, MGeff, comb1, comb2 = masses_from_crossing(lnG, stG)
    seq = [MHc]
    for _ in range(Hc_iter):
        lnG2, stG2 = find_cross(s2w, tanb, M_S, M2, M3, MHc)
        MHc2, MGeff2, c1, c2 = masses_from_crossing(lnG2, stG2)
        MHc, lnG, stG, comb1, comb2 = MHc2, lnG2, stG2, c1, c2
        seq.append(MHc)
    return math.exp(lnG), MHc, stG, comb1, comb2, seq

print("="*70)
print("§27 阈值链补齐与 M_Hc 通道自洽化")
print("="*70)

ref = dict(s2w=0.23122, tanb=3.0, M_S=1000.0, M2=200.0, M3=700.0)
print("\n[V1] 文献参考复现（M_S=1TeV, M₂=200GeV, M₃/M₂=3.5, tanβ=3）:")
MG, MHc, stG, c1, c2, seq = solve_chain(ref["s2w"], ref["tanb"], ref["M_S"], ref["M2"], ref["M3"])
ia = [1.0/stG[0], 1.0/stG[1], 1.0/stG[2]]
delta = stG[2]/stG[0] - 1.0
print("  M_GUT = %.3e GeV（α₁=α₂ 交叉）" % MG)
print("  M_Hc 迭代序列: %s" % ["%.2e" % x for x in seq])
print("  M_Hc(自洽) = %.3e GeV   comb1=%.4f" % (MHc, c1))
_, MGeff, _, _ = masses_from_crossing(math.log(MG), stG)
print("  M_X²M_Σ^(1/3) = %.3e GeV（对照 M_GUT=%.3e）" % (MGeff, MG))
# α_s 带（临时替换模块全局 α_s，函数按调用时取值）
print("  α_s=0.1184±0.0007 带:")
a_s_orig = alpha_s_MS
for das in (-0.0007, 0.0, +0.0007):
    alpha_s_MS = a_s_orig + das
    lnG_t, stG_t = find_cross(ref["s2w"], ref["tanb"], ref["M_S"], ref["M2"], ref["M3"])
    MHc_t, _, _, _ = masses_from_crossing(lnG_t, stG_t)
    print("    α_s=%.7f: M_Hc≈%.2e  M_GUT≈%.2e" % (alpha_s_MS, MHc_t, math.exp(lnG_t)))
alpha_s_MS = a_s_orig
print("  文献（1304.0343 Fig1 蓝线）: M_Hc ∈ [8.6e14, 1.4e15] GeV")

print("\n[V2] M_S 标度（M₂=200, M₃/M₂=3.5, tanβ=3, s²=0.23122）:")
for M_S in (1.0e3, 1.0e4, 1.0e5, 1.0e6):
    MG2, MHc2, _, _, _, _ = solve_chain(0.23122, 3.0, M_S, 200.0, 700.0)
    print("  M_S=%.0e TeV: M_GUT=%.3e  M_Hc=%.2e  (M_Hc/M_GUT=%.3f)" % (M_S/1000.0, MG2, MHc2, MHc2/MG2))

print("\n[V3] §25 预言带 [0.2298,0.2318] × 阈值链（参考谱）:")
for s2 in (0.2298, 0.23122, 0.2318):
    MG3, MHc3, _, _, _, _ = solve_chain(s2, 3.0, 1000.0, 200.0, 700.0)
    print("  s²=%.4f: M_GUT=%.3e  M_Hc=%.2e" % (s2, MG3, MHc3))

print("\n[V4] 判定:")
print("  若 V1 的 M_Hc 落入/贴近 [8.6e14,1.4e15] → §26 失效边界被修复（两循环+阈值补齐）")
print("  S02 零参与；定级维持组织性语言")

data = {"V1": {"M_GUT": MG, "M_Hc": MHc, "seq": seq, "comb1": c1, "delta": delta,
               "lit_lo": 8.6e14, "lit_hi": 1.4e15, "ref": ref},
        "V2": {"scan": [{"M_S": s, "M_GUT": solve_chain(0.23122,3.0,s,200.0,700.0)[0],
                         "M_Hc": solve_chain(0.23122,3.0,s,200.0,700.0)[1]} for s in (1e3,1e4,1e5,1e6)]},
        "V3": {"s2_map": [{"s2": s2, "M_Hc": solve_chain(s2,3.0,1000.0,200.0,700.0)[1]} for s2 in (0.2298,0.23122,0.2318)]},
        "V4": {"verdict": "pending"}}
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "§27_阈值链数据.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("\n数据已写入: §27_阈值链数据.json")
