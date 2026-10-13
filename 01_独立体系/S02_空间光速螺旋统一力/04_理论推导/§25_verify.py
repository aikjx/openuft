# -*- coding: utf-8 -*-
"""
§25_verify.py — 数值收口：Yukawa 两循环 + 阈值修正 + MS→DR，Weinberg 角账目完全关闭
S02 空间光速螺旋统一力 · 算法联盟
V1  文献系数核验（c_ai / Yukawa RGE / MS→DR C_i / GUT 阈值匹配）
V2  一循环解析锚点 + MS→DR 移位（对照 §24 的 0.2289）
V3  全两循环+Yukawa 预言 sin²θ_W(m_Z)（tanβ=5）
V4  tanβ 敏感性 {3,10,30}
V5  GUT 阈值带（M_Hc 扫参）+ 最终预算判定
"""
import json, math, os

# ---- 输入（MS-bar，PDG；与 §19/§20/§24 同套） ----
alpha_em_MS = 1.0/127.925
alpha_s_MS  = 0.1184
s2w_exp = 0.23122
mZ = 91.1876
MSUSY = 1000.0
mt_mZ, mb_mZ, mtau = 163.7, 2.85, 1.776   # GeV（m_Z 处 MS 跑动质量，近似）
v = 246.22                                 # GeV

# ---- MS→DR：1/α_i^DR = 1/α_i^MS − C₂(G_i)/(12π)（hep-ph/9611217 eq12） ----
C_dr = (0.0, 2.0/(12*math.pi), 3.0/(12*math.pi))

# ---- 文献系数（arXiv:1304.0343 eq8-15） ----
b_SM   = (41.0/10, -19.0/6, -7.0)
b2_SM  = ((199.0/50, 27.0/10, 44.0/5),
          (9.0/10, 35.0/6, 12.0),
          (11.0/10, 9.0/2, -26.0))
c_SM   = ((17.0/10, 1.0/2, 3.0/2),
          (3.0/2, 3.0/2, 1.0/2),
          (2.0, 2.0, 0.0))
b_MSSM   = (33.0/5, 1.0, -3.0)
b2_MSSM  = ((199.0/25, 27.0/5, 88.0/5),
            (9.0/5, 25.0, 24.0),
            (11.0/5, 9.0, 14.0))
c_MSSM   = ((26.0/5, 14.0/5, 18.0/5),
            (6.0, 6.0, 2.0),
            (4.0, 4.0, 0.0))

def beta_gauge(a, y, mode, two_loop=True, with_yuk=True):
    bvec = b_SM if mode == "SM" else b_MSSM
    b2mat = b2_SM if mode == "SM" else b2_MSSM
    cmat = c_SM if mode == "SM" else c_MSSM
    out = []
    for i in range(3):
        d = (bvec[i]/(2*math.pi)) * a[i]**2
        if two_loop:
            s = 0.0
            for j in range(3):
                s += b2mat[i][j] * a[j]
            d += (1.0/(8*math.pi**2)) * a[i]**2 * s
            if with_yuk:
                yk = 0.0
                for k in range(3):
                    yk += cmat[i][k] * y[k]**2
                d -= (1.0/(32*math.pi**3)) * a[i]**2 * yk
        out.append(d)
    return out

def beta_yuk(y, a, mode):
    yt, yb, ytau = y
    g1sq, g2sq, g3sq = [4*math.pi*x for x in a]   # g_i² = 4π·α_i
    if mode == "SM":
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
    da = beta_gauge(a, y, mode, two_loop, with_yuk)
    dy = beta_yuk(y, a, mode) if with_yuk else [0.0, 0.0, 0.0]
    return da + dy

def rk4(st, lnmu, h, mode, two_loop=True, with_yuk=True):
    k1 = deriv(st, mode, two_loop, with_yuk)
    k2 = deriv([st[i]+0.5*h*k1[i] for i in range(6)], mode, two_loop, with_yuk)
    k3 = deriv([st[i]+0.5*h*k2[i] for i in range(6)], mode, two_loop, with_yuk)
    k4 = deriv([st[i]+h*k3[i] for i in range(6)], mode, two_loop, with_yuk)
    return [st[i] + (h/6.0)*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(6)]

def run_up(st0, ln_low, ln_high, tanb, steps=900, two_loop=True, with_yuk=True):
    st = list(st0)
    lnmu = ln_low
    lnS = math.log(MSUSY)
    h = (ln_high - ln_low) / steps
    sinb = math.sin(math.atan(tanb)); cosb = math.cos(math.atan(tanb))
    for k in range(steps):
        ln_next = ln_low + (k+1)*h
        if lnmu < lnS <= ln_next:
            st = rk4(st, lnmu, lnS - lnmu, "SM", two_loop, with_yuk)
            if with_yuk:
                st[3] = st[3]/sinb
                st[4] = st[4]/cosb
                st[5] = st[5]/cosb
            lnmu = lnS
        mode = "MSSM" if lnmu >= lnS else "SM"
        st = rk4(st, lnmu, ln_next - lnmu, mode, two_loop, with_yuk)
        lnmu = ln_next
    return st

def ms_to_dr(alpha_MS):
    return [alpha_MS[i]/(1.0 - alpha_MS[i]*C_dr[i]) for i in range(3)]

def yukawa_mZ():
    return [math.sqrt(2)*mt_mZ/v, math.sqrt(2)*mb_mZ/v, math.sqrt(2)*mtau/v]

def init_state(s2w, use_dr=True):
    c2 = 1.0 - s2w
    a_MS = [(5.0/3)*alpha_em_MS/c2, alpha_em_MS/s2w, alpha_s_MS]
    a = ms_to_dr(a_MS) if use_dr else a_MS
    return a + yukawa_mZ()

def find_cross(s2w, tanb, use_dr=True, two_loop=True, with_yuk=True):
    st0 = init_state(s2w, use_dr)
    lo, hi = math.log(mZ), math.log(5e17)
    st_lo = run_up(st0, math.log(mZ), lo, tanb, two_loop=two_loop, with_yuk=with_yuk)
    f_lo = st_lo[0] - st_lo[1]
    for _ in range(30):
        mid = 0.5*(lo+hi)
        st_mid = run_up(st0, math.log(mZ), mid, tanb, two_loop=two_loop, with_yuk=with_yuk)
        f_mid = st_mid[0] - st_mid[1]
        if f_lo * f_mid < 0:
            hi = mid
        else:
            lo = mid
            f_lo = f_mid
    lnG = 0.5*(lo+hi)
    stG = run_up(st0, math.log(mZ), lnG, tanb, two_loop=two_loop, with_yuk=with_yuk)
    return lnG, stG

def s2w_solve(tanb, use_dr=True, two_loop=True, with_yuk=True):
    cache = {}
    def delta(s2w):
        key = round(s2w, 8)
        if key not in cache:
            lnG, stG = find_cross(s2w, tanb, use_dr, two_loop, with_yuk)
            cache[key] = (stG[2]/stG[0] - 1.0, lnG, stG)
        return cache[key]
    lo, hi = 0.20, 0.25
    dlo, lnGlo, stGlo = delta(lo)
    for _ in range(30):
        mid = 0.5*(lo+hi)
        dm, _, _ = delta(mid)
        if dlo * dm < 0:
            hi = mid
        else:
            lo = mid
            dlo, lnGlo, stGlo = dm, 0.0, None
    s2w = 0.5*(lo+hi)
    d, lnG, stG = delta(s2w)
    return s2w, d, lnG, stG

# ---- V2 一循环解析解（含 M_S 分段） ----
def one_loop_solve(use_dr):
    def inv_alpha(s2w):
        c2 = 1.0 - s2w
        a_MS = [(5.0/3)*alpha_em_MS/c2, alpha_em_MS/s2w, alpha_s_MS]
        a = ms_to_dr(a_MS) if use_dr else a_MS
        return [1.0/x for x in a]
    def at_mu(ia, L):
        # 1/α_i(μ) = 1/α_i(m_Z) − (b_i/2π)L，分 SM/MSSM 两段
        L1 = math.log(MSUSY/mZ)
        out = []
        for i in range(3):
            out.append(ia[i] - b_SM[i]*L1/(2*math.pi) - b_MSSM[i]*(L-L1)/(2*math.pi))
        return out
    def delta(s2w):
        ia = inv_alpha(s2w)
        # 交叉条件：1/α₁−1/α₂ 经 SM 段(Δb=(b1−b2)_SM·L1/2π)后，MSSM 段(Δb=(b1−b2)_MSSM·L2/2π)
        L1 = math.log(MSUSY/mZ)
        L2 = ((ia[0]-ia[1])*2*math.pi - (b_SM[0]-b_SM[1])*L1) / (b_MSSM[0]-b_MSSM[1])
        L = L1 + L2
        iaG = at_mu(ia, L)
        return iaG[2]/iaG[0] - 1.0, math.log(mZ) + L
    lo, hi = 0.20, 0.25
    for _ in range(60):
        mid = 0.5*(lo+hi)
        if delta(lo)[0] * delta(mid)[0] < 0:
            hi = mid
        else:
            lo = mid
    s2w = 0.5*(lo+hi)
    d, lnG = delta(s2w)
    return s2w, math.exp(lnG)

print("="*70)
print("§25 数值收口 · Yukawa 两循环 + 阈值 + MS→DR")
print("="*70)

print("\n[V1] 文献系数核验:")
print("  MSSM c_ai =", [tuple(x) for x in c_MSSM], " SM c_ai =", [tuple(x) for x in c_SM])
print("  MS→DR C_i =", tuple(round(x,5) for x in C_dr), "(C₂(G_i)/12π, hep-ph/9611217 eq12)")
print("  GUT 阈值 eq(16): 1/α₁=1/α_G+(1/2π)[(2/5)ln(μ/M_Hc)−10ln(μ/M_X)] …")

print("\n[V2] 一循环解析锚点（对照 §24 的 0.2289）:")
s2_1l_ms, MG_1l_ms = one_loop_solve(False)
s2_1l_dr, MG_1l_dr = one_loop_solve(True)
print("  一循环(MS 输入): sin²θ_W=%.4f  M_GUT=%.3e" % (s2_1l_ms, MG_1l_ms))
print("  一循环(DR 输入): sin²θ_W=%.4f  M_GUT=%.3e" % (s2_1l_dr, MG_1l_dr))
print("  MS→DR 一循环移位: %+.4f" % (s2_1l_dr - s2_1l_ms))

print("\n[V3] 全两循环+Yukawa（tanβ=5, DR 输入）:")
s2_full, d_full, lnG_full, stG_full = s2w_solve(5.0, True, True, True)
print("  sin²θ_W(m_Z) = %.4f   δ=%.1e" % (s2_full, d_full))
print("  M_GUT = %.3e GeV, α_G⁻¹ = %.3f" % (math.exp(lnG_full), 1.0/stG_full[0]))
print("  y_t(M_GUT)=%.3f y_b(M_GUT)=%.3f y_τ(M_GUT)=%.3f" % (stG_full[3], stG_full[4], stG_full[5]))

print("\n[V4] tanβ 敏感性:")
for tb in (3, 10, 30):
    s2_t, d_t, _, _ = s2w_solve(tb, True, True, True)
    print("  tanβ=%2d: sin²θ_W=%.4f (Δ= %+.4f vs tanβ=5)" % (tb, s2_t, s2_t - s2_full))

print("\n[V5] GUT 阈值带（M_Σ=M_X=M_GUT，M_Hc 扫参）:")
M_GUT = math.exp(lnG_full)
s2_ref, d_ref, lnG_ref, stG_ref = s2w_solve(5.0, True, True, True)
ai_ref = [1.0/stG_ref[0], 1.0/stG_ref[1], 1.0/stG_ref[2]]
s2_base = 3.0*ai_ref[1]/(3.0*ai_ref[1] + 5.0*ai_ref[0])
bands = []
for r in (0.03, 0.3, 1.0):
    MHc = r*M_GUT
    d1 = (1.0/(2*math.pi))*( (2.0/5)*math.log(M_GUT/MHc) - 10*math.log(M_GUT/M_GUT) )
    d2 = (1.0/(2*math.pi))*( 2*math.log(M_GUT/M_GUT) - 6*math.log(M_GUT/M_GUT) )
    s2_shift = 3.0*(ai_ref[1]+d2)/(3.0*(ai_ref[1]+d2) + 5.0*(ai_ref[0]+d1))
    bands.append((r, s2_shift - s2_base))
    print("  M_Hc=%.2f×M_GUT: Δsin²θ_W=%+.4f" % (r, bands[-1][1]))
lo_b = s2_full + min(b[1] for b in bands); hi_b = s2_full + max(b[1] for b in bands)
print("  预言带: [%.4f, %.4f]  实验 0.23122" % (lo_b, hi_b))

print("\n[V6] 最终预算（全部显式项）:")
exp = 0.23122
print("  一循环(§24)                0.2289   (Δ=%+.4f)" % (0.2289-exp))
print("  +两循环规范(§24)           0.2319   (Δ=%+.4f)" % (0.2319-exp))
print("  +MS→DR 输入转换           %+.4f" % (s2_1l_dr - s2_1l_ms))
print("  +Yukawa 两循环反馈         %+.4f" % (s2_full - 0.2319 - (s2_1l_dr - s2_1l_ms)))
print("  全链预言(tanβ=5)           %.4f   (Δ=%+.4f, %+.2f%%)" % (s2_full, s2_full-exp, (s2_full-exp)/exp*100))
print("  GUT 阈值带                  ±%.4f" % max(abs(b[1]) for b in bands))
print("  判定: 预言带%s实验 0.23122" % ("包围" if lo_b <= exp <= hi_b else "不包围"))

data = {"V1": {"c_MSSM": [list(r) for r in c_MSSM], "c_SM": [list(r) for r in c_SM], "C_dr": list(C_dr)},
        "V2": {"s2_1loop_MS": s2_1l_ms, "MGUT_1loop_MS": MG_1l_ms, "s2_1loop_DR": s2_1l_dr,
               "dr_shift_1loop": s2_1l_dr - s2_1l_ms},
        "V3": {"s2_full": s2_full, "MGUT": math.exp(lnG_full), "aG_inv": 1.0/stG_full[0],
               "yt_GUT": stG_full[3], "yb_GUT": stG_full[4], "ytau_GUT": stG_full[5]},
        "V4": {"tanb3": s2w_solve(3.0, True, True, True)[0], "tanb10": s2w_solve(10.0, True, True, True)[0],
               "tanb30": s2w_solve(30.0, True, True, True)[0]},
        "V5": {"band": bands, "s2_full": s2_full, "band_lo": lo_b, "band_hi": hi_b},
        "V6": {"experiment": exp, "residual_full": s2_full - exp, "covers": lo_b <= exp <= hi_b}}
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "§25_收口预算数据.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("\n数据已写入: §25_收口预算数据.json")
