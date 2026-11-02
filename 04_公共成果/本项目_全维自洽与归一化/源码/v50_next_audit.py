# -*- coding: utf-8 -*-
"""ROOT V50（三代质量不等式 + 六维 Einstein–Maxwell 磁通真空）来料 · 全量机核

核验 (50-1)…(50-15)、§3 真空表、§4 引力—规范关系，并做五项本册补记：
T3b 单调 h 的排序引理；T3c Cauchy–Schwarz 等号可饱和（3000 组测试零判别力）；
T4 非单调非负 h 的置换反例（e 居中）；T7 「N≥4 无解」是示范参数的后果；T10 α 未被预测。

约定：脚本中 M6 记 M6^4；G6 记 g6；LAM 记 Λ6；自然单位。
"""
import numpy as np
from scipy import integrate
from scipy.special import erf

results = []
infos = []


def check(name, value, cond, note=""):
    tag = "成立" if cond else "不成立"
    results.append((name, tag, value, note))
    print(f"[{tag}] {name}  value={value}  {note}")


def info(msg):
    infos.append(msg)
    print(f"[信息] {msg}")


# ================= 一、N=3 单极零模密度 =================
def P(k, xx):
    xx = np.asarray(xx, dtype=float)
    if k == 0:
        return 3 * (1 - xx) ** 2
    if k == 1:
        return 6 * xx * (1 - xx)
    return 3 * xx ** 2


nodes, weights = np.polynomial.legendre.leggauss(600)
xt = 0.5 * (nodes + 1)
wt = 0.5 * weights

xx = np.linspace(0, 1, 2001)
d1 = np.abs(P(1, xx) - 2 * np.sqrt(P(0, xx) * P(2, xx)))
print(f"    max|P1−2√(P0P2)| = {d1.max():.3e}；ΣP_k−3 的最大差 = "
      f"{np.abs(P(0,xx)+P(1,xx)+P(2,xx)-3).max():.3e}")
check("T1a (50-1) P1=2√(P0P2) 逐点成立", float(d1.max()), d1.max() < 1e-14)
norms = [float(np.sum(wt * P(k, xt))) for k in range(3)]
check("T1b 三个零模密度各自归一化", max(abs(v - 1) for v in norms),
      max(abs(v - 1) for v in norms) < 1e-12, f"∫P_k = {np.round(norms,12)}")
check("T1c ΣP_k=3（迹和规则）", float(np.abs(P(0, xx) + P(1, xx) + P(2, xx) - 3).max()),
      np.abs(P(0, xx) + P(1, xx) + P(2, xx) - 3).max() < 1e-14,
      "⇒ m0+m1+m2 = 3m*∫h：三代质量只能通过合计形状相联系")

# ================= 二、质量不等式的机核与实测冲突 =================
ME, MMU, MTAU = 0.51099895000, 105.6583755, 1776.93  # MeV
ratio_obs = MMU ** 2 / (4 * MTAU * ME)
mmu_max = np.sqrt(4 * MTAU * ME)
print(f"    m_μ²/(4m_τm_e) = {ratio_obs:.11f}；m_μ 上限 = {mmu_max:.6f} MeV；"
      f"冲突倍数 = {MMU/mmu_max:.8f}")
check("T2a (50-2) 实测组合违反 m1²≤4m0m2", float(ratio_obs), ratio_obs > 1)
check("T2b 模型允许的 m_μ 上限与来料一致", float(mmu_max), abs(mmu_max - 60.2664) < 0.02,
      f"实测/上限 = {MMU/mmu_max:.8f}")
check("T2c 冲突倍数 1.7532（V49 单参数 p 的排除是它的特例）", float(MMU / mmu_max),
      abs(MMU / mmu_max - 1.7532) < 5e-4)

# ---- 口径依赖：V49 册登记 O-V49-q（P_k 随 q 变，V50 未声明 q） ----
from scipy.special import beta as beta_fn


def Pq(k, xx, q):
    z = np.asarray(xx, dtype=float)
    return z ** k * (1 - z) ** (2 * q - k) / beta_fn(k + 1, 2 * q - k + 1)


xs_int = xx[1:-1]
c_q1 = P(1, xs_int) / np.sqrt(P(0, xs_int) * P(2, xs_int))
check("T1d q=1 口径：P1/√(P0P2) 逐点恒为 2（即 (50-1)）", float(np.ptp(c_q1)),
      np.ptp(c_q1) < 1e-12 and abs(c_q1.mean() - 2) < 1e-12,
      "V50 的全部质量结论建立在该口径上")
c_q2 = Pq(1, xs_int, 1.5) / np.sqrt(Pq(0, xs_int, 1.5) * Pq(2, xs_int, 1.5))
check("T1e q=3/2 口径：比例常数由 2 变 √3（P1=√3·√(P0P2)）",
      float(c_q2.mean()), abs(c_q2.mean() - np.sqrt(3)) < 1e-12 and np.ptp(c_q2) < 1e-12,
      "⇒ (50-1) 不是形状无关恒等式，而是 q=1 的产物")
mmu_max_q2 = np.sqrt(3 * MTAU * ME)
check("T1f q=3/2 下 μ 上限收紧为 52.19 MeV，实测仍被排除", float(mmu_max_q2),
      abs(mmu_max_q2 - 52.19) < 0.05 and MMU > mmu_max_q2,
      f"冲突倍数 {MMU/mmu_max_q2:.4f}（q=1 时为 {MMU/mmu_max:.4f}）")

# m1 = 2m*∫√(P0P2) h 的跨项恒等式（对任意 h）
rng = np.random.default_rng(20261103)
worst = 0.0
for _ in range(200):
    h = np.exp(-rng.uniform(0, 6) * xt) + rng.uniform(0, 1) * xt ** rng.uniform(0, 4)
    m_direct = np.array([np.sum(wt * P(k, xt) * h) for k in range(3)])
    m_cross = 2 * np.sum(wt * np.sqrt(P(0, xt) * P(2, xt)) * h)
    worst = max(worst, abs(m_direct[1] - m_cross) / max(m_direct[1], 1e-300))
check("T2d (50-1) 使 m1 可写成 2m*∫√(P0P2)h（C-S 的代数前提）", float(worst), worst < 1e-12,
      "200 组随机 h 的相对偏差")

ratios = []
for _ in range(3000):
    h = np.zeros_like(xt)
    for _j in range(3):
        c = rng.uniform(0.05, 1.0)
        p = rng.uniform(0.1, 6.0)
        kind = rng.integers(0, 3)
        if kind == 0:
            h += c * np.exp(-p * xt)
        elif kind == 1:
            h += c * xt ** p
        else:
            ctr = rng.uniform(0.1, 0.9)
            h += c * np.exp(-(xt - ctr) ** 2 / (2 * (0.05 + 0.15 * rng.uniform()) ** 2))
    m = np.array([np.sum(wt * P(k, xt) * h) for k in range(3)])
    if m[0] * m[2] > 1e-300:
        ratios.append(m[1] ** 2 / (4 * m[0] * m[2]))
ratios = np.array(ratios)
print(f"    3000 组非负 h：ratio ∈ [{ratios.min():.3e}, {ratios.max():.6f}]")
check("T3a 3000 组随机非负 h 的 ratio ≤ 1（C-S 必然）", float(ratios.max()),
      ratios.max() <= 1 + 1e-12, "对证伪零判别力：只要数值不溢出就必过")

h_mid = np.zeros_like(xt)
h_mid[np.argmin(np.abs(xt - 0.5))] = 1.0
m_delta = np.array([np.sum(wt * P(k, xt) * h_mid) for k in range(3)])
print(f"    h=δ(x−1/2)（网格近似）：m = {np.round(m_delta,6)}，ratio = "
      f"{m_delta[1]**2/(4*m_delta[0]*m_delta[2]):.9f}")
check("T3c C-S 等号可被单峰 h 饱和（ratio→1）", float(m_delta[1] ** 2 / (4 * m_delta[0] * m_delta[2])),
      abs(m_delta[1] ** 2 / (4 * m_delta[0] * m_delta[2]) - 1) < 0.02,
      "⇒ 任意多次随机抽样都不可能产生比率 >1 的反例；3000 组测试不构成检验")

order_ok, order_slack = True, np.inf
for _ in range(500):
    h = np.zeros_like(xt)
    for _j in range(5):
        h += rng.uniform(0.05, 1.0) * (1 - xt) ** rng.uniform(0.2, 6.0)
    m = np.array([np.sum(wt * P(k, xt) * h) for k in range(3)])
    order_ok &= bool(m[0] >= m[1] >= m[2])
    order_slack = min(order_slack, float(min(m[0] - m[1], m[1] - m[2])))
print(f"    500 组单调不增 h：m0≥m1≥m2 全部成立 = {order_ok}（最小间隙 {order_slack:.3e}）")
check("T3b 单调不增 h ⇒ m0≥m1≥m2（排序引理，本册证明+机核）", float(order_ok), order_ok,
      "证明：P0−P1 在 x=1/3 变号、P1−P2 在 x=2/3 变号，配单调 h 的割线符号")

# ---------- T4：非单调非负 h 的置换反例（e 居中） ----------
SQRT2PI = np.sqrt(2 * np.pi)


def Phi(z):
    return 0.5 * (1 + erf(z / np.sqrt(2)))


def gauss_moments(c, s):
    """∫_0^1 x^n exp(-(x-c)^2/(2s^2)) dx, n=0,1,2（截断正态的解析矩）"""
    za, zb = -c / s, (1 - c) / s
    dPhi = Phi(zb) - Phi(za)
    ga, gb = np.exp(-0.5 * za * za), np.exp(-0.5 * zb * zb)
    I0 = s * SQRT2PI * dPhi
    I1 = c * I0 + s * s * (ga - gb)
    I2 = s * (c * c * SQRT2PI * dPhi + 2 * c * s * (ga - gb)
              + s * s * ((za * ga - zb * gb) + SQRT2PI * dPhi))
    return I0, I1, I2


def B_of(sg, cs):
    Bm = np.zeros((3, 3))
    for j, c in enumerate(cs):
        I0, I1, I2 = gauss_moments(c, sg)
        Bm[0, j] = 3 * (I0 - 2 * I1 + I2)
        Bm[1, j] = 6 * (I1 - I2)
        Bm[2, j] = 3 * I2
    return Bm


# T4a：解析矩 vs 数值积分（宽峰，quad 可靠）
sg_test = 0.05
cs_test = (0.05, 0.5, 0.95)
B_an = B_of(sg_test, cs_test)
B_nu = np.array([[integrate.quad(lambda t: P(k, t) * np.exp(-(t - c) ** 2 / (2 * sg_test ** 2)),
                                0, 1, limit=300)[0] for c in cs_test] for k in range(3)])
check("T4a 截断正态矩公式与数值积分一致（σ=0.05）", float(np.abs(B_an - B_nu).max()),
      np.abs(B_an - B_nu).max() < 1e-10, "用于避开窄峰 quad 失真")

# T4b：σ=1e-4 三峰非单调 h，精确复现 (m_τ, m_e, m_μ)（e 居中）
sg = 1e-4
cs = (0.0, 0.5, 1.0)
Bm = B_of(sg, cs)
v = np.array([MTAU, ME, MMU]) / MTAU
amps = np.linalg.solve(Bm, v)
print(f"    非单调三峰 h（σ={sg:g}，峰位 0/0.5/1）权重 = {amps}")
check("T4b 非单调非负 h 精确复现三代质量集合（e 居中）", float(abs(Bm @ amps - v).max()),
      abs(Bm @ amps - v).max() < 1e-12 and amps.min() > 0,
      f"min/max 权重 = {amps.min()/amps.max():.3e}；全部为正 ⇒ 非负 h 合法")
mfit = Bm @ amps * MTAU
ratio_fit = mfit[1] ** 2 / (4 * mfit[0] * mfit[2])
print(f"    反例质量 = {np.round(mfit,6)} MeV（目标 τ,e,μ = {np.round(v*MTAU,6)}）；"
      f"ratio = {ratio_fit:.3e}")
check("T4c 反例的 ratio ≪ 1（满足 (50-2)，故 C-S 不是充分条件）", float(ratio_fit),
      ratio_fit < 1e-3, "不等式只禁『μ 居中』；禁『e 居中』需要额外的排序/对应假设")

# δ 极限（无宽度）应与上述解同构：解 3×3 的 P_k 三点取值矩阵
B_delta = np.array([[3.0, 0.75, 0.0], [0.0, 1.5, 0.0], [0.0, 0.75, 3.0]])
amps_d = np.linalg.solve(B_delta, np.array([MTAU, ME, MMU]))
alpha_d, eps_d, beta_d = amps_d
m_d = B_delta @ amps_d
print(f"    δ 极限构造：h = {alpha_d:.6g}δ0 + {eps_d:.6g}δ(1/2) + {beta_d:.6g}δ1 ；"
      f"质量 = {np.round(m_d,6)} ；α:ε:β = 1 : {eps_d/alpha_d:.6f} : {beta_d/alpha_d:.6f}")
check("T4d δ 极限的三点权重精确复现 (m_τ,m_e,m_μ)", float(np.abs(m_d - np.array([MTAU, ME, MMU])).max()),
      np.abs(m_d - np.array([MTAU, ME, MMU])).max() < 1e-9 and eps_d > 0 and alpha_d > 0,
      f"ε/β = {eps_d/beta_d:.6f}（与 σ=1e-4 全为正的解同构 ⇒ 反例是严格极限）")

# ================= 三、六维 Einstein–Maxwell 真空 =================
M6, G6, LAM = 1.0, 1.0, 2.0 / 9.0   # M6 记 M6^4
print("\n    §3 真空表复现（M6^4=1, g6=1, Λ6=2/9）")
tab = {1: (0.191578, -0.530596, 0.036769), 2: (0.825765, -0.085173, 0.035790),
       3: (2.25, 0.0, 0.032922)}
sols = {}
for N in (1, 2, 3, 4):
    disc = M6 ** 2 - 3 * LAM * N ** 2 / (8 * G6 ** 2)
    if disc < 0:
        sols[N] = None
        print(f"      N={N}: 判别式 = {disc:.6f} < 0 ⇒ 无实根")
        continue
    us = np.sort(np.real(np.roots([LAM, -2 * M6, 3 * N ** 2 / (8 * G6 ** 2)])))
    hs = [(LAM - N ** 2 / (8 * G6 ** 2 * u ** 2)) / 6 for u in us]
    sols[N] = (us, hs)
    print(f"      N={N}: R² = {np.round(us,6)} ; H² = {np.round(hs,9)}")
for N in (1, 2, 3):
    us, hs = sols[N]
    err = max(abs(us[0] - tab[N][0]), abs(hs[0] - tab[N][1]), abs(hs[1] - tab[N][2]))
    check(f"T5{chr(96+N)} §3 表 N={N} 两支 R²/H² 与来料一致", float(err), err < 1e-6)
check("T5d N=4 判别式 < 0（本组示范参数下无实根）",
      float(M6 ** 2 - 3 * LAM * 16 / (8 * G6 ** 2)),
      M6 ** 2 - 3 * LAM * 16 / (8 * G6 ** 2) < 0)

res = 0.0
for N, s in sols.items():
    if s is None:
        continue
    for u, h2 in zip(*s):
        res = max(res, abs(M6 * (3 * h2 + 1 / u) - (LAM + N ** 2 / (8 * G6 ** 2 * u ** 2))),
                  abs(6 * M6 * h2 - (LAM - N ** 2 / (8 * G6 ** 2 * u ** 2))))
print(f"    (50-5)(50-6) 全部支的残差 = {res:.3e}")
check("T5e (50-5)(50-6) 数值残差 1e-15 量级", float(res), res < 1e-13)

check("T5f (50-7)/(50-10) 同根（N=3,u=2.25 逐项为零）",
      float(abs(LAM * 2.25 ** 2 - 2 * 2.25 + 27 / 8)),
      abs(LAM * 2.25 ** 2 - 2 * 2.25 + 27 / 8) < 1e-14)

R2_flat = M6 / (2 * LAM)
print(f"    H²=0: R² = {R2_flat:.6f}（应 2.25）；N² = {2 * G6 ** 2 * M6 ** 2 / LAM:.6f}（应 9）")
check("T6a (50-8)(50-9) 平直真空关系",
      float(max(abs(R2_flat - 2.25), abs(2 * G6 ** 2 * M6 ** 2 / LAM - 9))),
      abs(R2_flat - 2.25) < 1e-12 and abs(2 * G6 ** 2 * M6 ** 2 / LAM - 9) < 1e-12)
check("T6b N=3 平直要求 Λ6=2g6²M6^8/9（示范值 2/9）",
      float(abs(2 * G6 ** 2 * M6 ** 2 / 9 - LAM)),
      abs(2 * G6 ** 2 * M6 ** 2 / 9 - LAM) < 1e-15,
      "⇒ 示范参数是按 N=3 反解，不是自然选择")

LAM2 = 0.1
disc4 = M6 ** 2 - 3 * LAM2 * 16 / (8 * G6 ** 2)
u4 = np.sort(np.real(np.roots([LAM2, -2 * M6, 3 * 16 / (8 * G6 ** 2)])))
h4 = [(LAM2 - 16 / (8 * G6 ** 2 * u ** 2)) / 6 for u in u4]
print(f"    Λ6=0.1 时 N=4：判别式={disc4:.4f}，R²={np.round(u4,6)}，H²={np.round(h4,6)}")
check("T7a 『N≥4 无解』是 Λ6=2/9 的直接后果，不是一般禁律", float(disc4), disc4 > 0,
      f"Λ6=0.1 时 N=4 有实根，H²={h4[0]:.4f}")
check("T7b 本组参数 N_max=√12", float(np.sqrt(8 * G6 ** 2 * M6 ** 2 / (3 * LAM))),
      abs(np.sqrt(8 * G6 ** 2 * M6 ** 2 / (3 * LAM)) - np.sqrt(12)) < 1e-12,
      f"整数值只到 N=3（{np.sqrt(12):.3f}）")

# ================= 四、半径模势与稳定性 =================
def V(u, N=3):
    return LAM / u - M6 / u ** 2 + N ** 2 / (8 * G6 ** 2) / u ** 3


for N in (1, 2, 3):
    us, hs = sols[N]
    for u, h2 in zip(us, hs):
        dV = -LAM / u ** 2 + 2 * M6 / u ** 3 - 3 * (N ** 2 / (8 * G6 ** 2)) / u ** 4
        d2V = 2 * LAM / u ** 3 - 6 * M6 / u ** 4 + 12 * (N ** 2 / (8 * G6 ** 2)) / u ** 5
        check(f"T8 N={N} u={u:.4f} 驻点与 V'' 符号", float(d2V),
              abs(dV) < 1e-12 and np.sign(d2V) == np.sign(M6 - LAM * u),
              f"V''={d2V:.4f} ⇒ {'极小(稳定)' if d2V > 0 else '极大(不稳定)'}")
info("V_eff 只覆盖球面整体半径模；小支为极小、大支为极大。规范场/引力/费米子全谱涨落未检查")

# ================= 五、引力—规范耦合关系 =================
R2 = 2.25
M4sq = 4 * np.pi * R2 * M6
g4sq = 1 / (4 * np.pi * R2 / G6 ** 2)
print(f"    M4²={M4sq:.6f}；g4²={g4sq:.6f}；g4²M4²={g4sq*M4sq:.6f}；g6²M6^4={G6**2*M6:.6f}")
check("T9a (50-12)(50-13)(50-14) 代数关系", float(abs(g4sq * M4sq - G6 ** 2 * M6)),
      abs(g4sq * M4sq - G6 ** 2 * M6) < 1e-12 and abs(M4sq - 4 * np.pi * R2 * M6) < 1e-12)
check("T9b 平直真空下 g6²M4²=πN²", float(G6 ** 2 * M4sq), abs(G6 ** 2 * M4sq - 9 * np.pi) < 1e-12,
      f"g6M4={np.sqrt(G6**2*M4sq):.6f}=3√π={3*np.sqrt(np.pi):.6f}")
alpha = 9 * LAM ** 2 / (16 * np.pi ** 2 * M6 ** 3)   # M6 记 M6^4，故 M6^12=(M6)^3
print(f"    模型内 α=g6²Λ6²/(16π²M6^12)={alpha:.8f} = 1/{1/alpha:.2f}（实测 1/137.036）")
check("T10 α 未被预测：示范参数给 1/355", float(alpha),
      abs(alpha - g4sq / (4 * np.pi)) < 1e-14 and abs(1 / alpha - 355.3) < 3,
      "⇒ 真空只把 α 换成 M6、Λ6 的另一个输入组合")

# ================= 六、四力结构盘点 =================
info("SO(3)≅SU(2)/Z2 维度 3=3 成立，但它是内空间等距群（全局对称），不是四维规范场")
info("尺寸账：单球面等距 dim=3 < dim SU(3)_c=8 ⇒ 无颜色载体；单个 U(1) 无手征 SU(2)_L")
info("未生成：SU(3)_c、手征 SU(2)_L、三代质量与 CKM/PMNS、光速螺旋公设")
info("ψ_k ∝ e^{ikφ} 是内部角坐标上的相位结构，未证明等于真实时间演化/传播速度")

print()
print("=" * 78)
n_pass = sum(1 for r in results if r[1] == "成立")
print(f"汇总：{n_pass}/{len(results)} 项断言成立")
for name, tag, value, note in results:
    print(f"  {tag}  {name}")
print("=" * 78)
print(f"判词：V50_NUMBERS_REPRODUCED_{n_pass}_{len(results)}__"
      "INEQUALITY_ONLY_FORBIDS_MU_IN_MIDDLE__NONMONOTONE_H_REPRODUCES_MASS_SET__"
      "3000_PROFILE_TEST_VACUOUS__VACUUM_EQUATIONS_RESIDUAL_1E-15__"
      "N4_NOGO_IS_LAMBDA_ARTIFACT__RADIUS_MOD_STABLE_ONLY__"
      "ALPHA_NOT_PREDICTED__FOUR_FORCES_NOT_UNIFIED")
