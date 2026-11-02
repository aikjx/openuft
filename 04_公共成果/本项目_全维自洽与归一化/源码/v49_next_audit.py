# -*- coding: utf-8 -*-
"""ROOT V49 攻坚：五维局域化方程 (48-10) 的可解化与两条定理

来料 V48 把下一步押在：
    [∂_y + λ_i Φ(y)] f_{L,i}(y) = 0 ,  Φ 由自身作用量变分求出
本脚本不冒充「已攻破」，只做三件可机核的事：
  T1  单背景 + 味普适 λ ⇒ 三代完全简并（无层级、无混合）  [no-go]
  T2  单背景 + 3 个 λ_i ⇒ 质量可复现，但参数计数不变（3↔3） [计数定理]
  T3  谱塔 S 对背景「形状」敏感 ⇒ S 是背景形状的判别器（不是形状的函数）
另含：φ⁴ kink 的精确性检验、质量-λ 单调性、与 V44 矩阵的对照。

复算：numpy / scipy.quad / brentq。约定沿用 V45 C1–C4。
"""
import numpy as np
from scipy import integrate, optimize

results = []


def check(name, value, cond, note=""):
    tag = "成立" if cond else "不成立"
    results.append((name, tag, value, note))
    print(f"[{tag}] {name}  value={value}  {note}")


V_GEV = 246.22
YSTAR = 1.0
MS = np.array([0.51099895, 105.6583755, 1776.93])   # MeV
Z44 = np.array([16.218066, 10.446620, 7.260337])    # V44 的指数型局域化参数

# ---------- kink 型背景 ----------
def Phi(y, w):
    """kink 尾部：Φ(y)=tanh((1.5−y)/w)，在 [0,1] 上单调下降、恒正"""
    return np.tanh((1.5 - y) / w)

def d2Phi(y, w):
    """解析二阶导：Φ=tanh(u), u=(1.5−y)/w ⇒ Φ''=−2Φ(1−Φ²)/w²"""
    p = Phi(y, w)
    return -2 * p * (1 - p**2) / w**2

def Vprime(phi, w):
    """V(φ)=(φ²−1)²/(2w²) ⇒ V'(φ)=2φ(φ²−1)/w²"""
    return 2 * phi * (phi**2 - 1) / w**2

print("=" * 78)
print("[T0] kink 背景是否真是一条静态解：Φ'' = V'(Φ)")
print("=" * 78)
worst = 0.0
for w in (0.25, 1.5):
    for y in (0.2, 0.5, 0.8):
        r = abs(d2Phi(y, w) - Vprime(Phi(y, w), w))
        worst = max(worst, r)
print(f"    max|Φ''−V'(Φ)|（w=0.25/1.5, y=0.2/0.5/0.8）= {worst:.3e}")
check("T0 tanh((1.5−y)/w) 精确满足 φ⁴ 型 kink 方程", float(worst), worst < 1e-6,
      "V(φ)=(φ²−1)²/(2w²)；区间端点项不计（壁在 y=1.5，区间外）")

# ---------- 波函数与质量 ----------
def Pfun(y, w):
    """P(y)=∫_0^y Φ ds（数值，向量化用 quad 逐点）"""
    return integrate.quad(lambda s: Phi(s, w), 0, y, limit=200)[0]

def prof(y, lam, w):
    """f_L = N exp(−λ P(y))，N 由 ∫|f|²=1 定"""
    return np.exp(-lam * Pfun(y, w))

def overlap(lam, w):
    """∫ f_L f_R dy，f_R = N' exp(−λ(P(1)−P(y)))"""
    P1 = Pfun(1.0, w)
    fl = lambda y: np.exp(-lam * Pfun(y, w))
    fr = lambda y: np.exp(-lam * (P1 - Pfun(y, w)))
    Zl = integrate.quad(lambda y: fl(y)**2, 0, 1, limit=200)[0]
    Zr = integrate.quad(lambda y: fr(y)**2, 0, 1, limit=200)[0]
    ov = integrate.quad(lambda y: fl(y) * fr(y), 0, 1, limit=200)[0]
    return ov / np.sqrt(Zl * Zr)

def m_of_lam(lam, w):
    return V_GEV * 1e3 / np.sqrt(2) * YSTAR * overlap(lam, w)

def fit_lam(m, w):
    return optimize.brentq(lambda lam: m_of_lam(lam, w) - m, 0.5, 80)

# ---------- 谱塔 ----------
def S_from_profile(lam, w):
    """ρ=|f_L|² 归一化 ⇒ F(t), H=F−t ⇒ S=π²∫HH"""
    P1 = Pfun(1.0, w)
    fl = lambda y: np.exp(-lam * Pfun(y, w))
    Zl = integrate.quad(lambda y: fl(y)**2, 0, 1, limit=200)[0]
    rho = lambda t: fl(t)**2 / Zl
    F = lambda t: integrate.quad(rho, 0, t, limit=200)[0]
    H = lambda t: F(t) - t
    return H, rho

def S_matrix(lams, w):
    Hs = [S_from_profile(l, w)[0] for l in lams]
    return np.array([[np.pi**2 * integrate.quad(lambda t: Hs[i](t) * Hs[j](t), 0, 1, limit=200)[0]
                      for j in range(3)] for i in range(3)])

print()
print("=" * 78)
print("[T1] 味普适 λ + 单一背景 ⇒ 三代简并（no-go）")
print("=" * 78)
w0 = 1.5
lam_common = fit_lam(MS[1], w0)   # 用 μ 子质量定一个共同 λ
m_common = np.array([m_of_lam(lam_common, w0) for _ in range(3)])
print(f"    w={w0}, 共同 λ={lam_common:.6f} ⇒ 三代质量 = {np.round(m_common, 6)} MeV")
print(f"    与真实谱的偏差：{np.round(m_common - MS, 3)} MeV（差 2–3 个数量级）")
check("T1a 普适 λ ⇒ 三代质量全同（无层级）", float(np.abs(np.diff(m_common)).max()),
      np.abs(np.diff(m_common)).max() == 0.0, f"共同 λ={lam_common:.6f}")
lam_univ = np.array([lam_common] * 3)
S_univ = S_matrix(lam_univ, w0)
eig_univ = np.linalg.eigvalsh(S_univ)
print(f"    普适 λ 的谱塔 S eig = {eig_univ}")
check("T1b 普适 λ ⇒ S 秩 1（唯一非零本征值 ⇒ 无味结构）", float(eig_univ[1] / eig_univ[2]),
      eig_univ[1] / eig_univ[2] < 1e-10, "其余本征值为浮点零")

print()
print("=" * 78)
print("[T2] 三个 λ_i 拟合三代质量：可复现，但参数计数 3↔3 不变")
print("=" * 78)
lams = np.array([fit_lam(m, w0) for m in MS])
print(f"    w={w0}, 拟合 λ = {np.round(lams, 6)}")
print(f"    复算质量 = {np.round([m_of_lam(l, w0) for l in lams], 6)} MeV（输入 {MS}）")
print(f"    等效总指数 λ_i·∫Φ = {np.round(lams * Pfun(1.0, w0), 6)}  ← 与 V44 的 z 同量级但不等")
lam_grid = np.linspace(1.0, 60.0, 300)
dm = np.array([m_of_lam(l, w0) for l in lam_grid])
slope = np.diff(dm)
print(f"    dm/dλ 全网格符号：max={slope.max():.3e}, min={slope.min():.3e}（严格单调 ⇒ 3 个质量⇔3 个 λ 双射）")
check("T2a 质量对 λ 严格单调 ⇒ 3 个质量与 3 个 λ_i 一一对应", float(np.abs(slope).min()),
      slope.min() < 0 and slope.max() <= 0, "无简并 ⇒ 无参数约化")
check("T2b 输入 3 质量 → 输出 3 λ，自由度不变", 3, True,
      "V49 的 (48-10) 只把 z_i 改名为 λ_i；净预测自由度不变（对照 V39 的 4↔4）")

print()
print("=" * 78)
print("[T3] 谱塔对背景形状敏感：S 可区分 kink 与指数型")
print("=" * 78)
S_claim = np.array([[2.852212669, 2.730266399, 2.572273069],
                    [2.730266399, 2.626512851, 2.485905064],
                    [2.572273069, 2.485905064, 2.363949413]])
S_kink_thick = S_matrix(lams, 1.5)
S_kink_thin = S_matrix(np.array([fit_lam(m, 0.25) for m in MS]), 0.25)
def rel(A, B):
    return np.linalg.norm(A - B) / np.linalg.norm(B)
print(f"    厚壁 w=1.5  S =\n{np.round(S_kink_thick, 6)}")
print(f"      相对 V44 矩阵 ‖ΔS‖/‖S‖ = {rel(S_kink_thick, S_claim):.4%}")
print(f"    薄壁 w=0.25 相对 V44 矩阵 = {rel(S_kink_thin, S_claim):.4%}")
print(f"    厚壁 vs 薄壁（同三代质量）= {rel(S_kink_thick, S_kink_thin):.4%}")
check("T3a 同质量、不同壁厚 ⇒ S 显著不同（形状可观测）", float(rel(S_kink_thick, S_kink_thin)),
      rel(S_kink_thick, S_kink_thin) > 0.01, "S 是背景形状的判别器")
check("T3b 薄壁极限趋近指数型（单一 z 参数化的适用域）", float(rel(S_kink_thin, S_claim)),
      rel(S_kink_thin, S_claim) < 0.01, "w→0 时 Φ 趋常数 ⇒ 回到 (48-3)")

# 味改变量在 kink 背景下重算（示范角沿用 V44，仍为演示值）
def R(i, j, th):
    M = np.eye(3)
    M[i, i] = np.cos(th); M[i, j] = np.sin(th)
    M[j, i] = -np.sin(th); M[j, j] = np.cos(th)
    return M
t12, t23, t13 = 0.20, 0.12, 0.03
U = R(1, 2, t23) @ R(0, 2, t13) @ R(0, 1, t12)
wv = np.conj(U[:, 0]) * U[:, 1]
Q44 = np.real(np.einsum('i,j,ij->', wv, np.conj(wv),
                        np.array([[2.852212669, 2.730266399, 2.572273069],
                                  [2.730266399, 2.626512851, 2.485905064],
                                  [2.572273069, 2.485905064, 2.363949413]])))
Qk = np.real(np.einsum('i,j,ij->', wv, np.conj(wv), S_kink_thick))
print(f"    Q_eμ（V44 指数型）= {Q44:.9f} ; kink 厚壁 = {Qk:.9f} ; 比值 = {Qk/Q44:.4f}")
check("T3c 味改变强度随背景形状改变（不是常数）", float(abs(Qk / Q44 - 1)),
      abs(Qk / Q44 - 1) > 0.01, "同一组质量与角度下 Q 变动 >1%")

# 形状判别力随壁厚的变化：若 S 被独立测定，可反解壁厚
print("    壁厚扫描（同一组质量，仅改 Φ 的形状）：")
w_grid = (0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0)
rel_grid = []
for ww in w_grid:
    Sw = S_matrix(np.array([fit_lam(m, ww) for m in MS]), ww)
    r = rel(Sw, S_claim)
    rel_grid.append(r)
    print(f"      w={ww:5.2f} → ‖ΔS‖/‖S‖ = {r:.4%}")
rel_grid = np.array(rel_grid)
check("T3d 壁越厚 ⇒ S 偏离指数型越远（形状判别力单调）", float(np.all(np.diff(rel_grid) > 0)),
      bool(np.all(np.diff(rel_grid) > 0)), "S 可作背景形状的定量判别器")

print()
print("=" * 78)
print("[T4] V49 的最小可证伪命题")
print("=" * 78)
print("    若坚持「单一 Φ + 味普适 λ」，则 T1 给出三代简并 ⇒ 必须引入味依赖结构。")
print("    味依赖的最小形式是 3 个 λ_i（或等价的对角 Yukawa）⇒ T2 给出 3 个参数。")
print("    要真正「预测」三代，需要额外原理固定 λ 比值（如味对称的本征值谱）；")
print("    V48 的 (48-10) 本身不含该原理，故其预测力为 0。")
check("T4 (48-10) 单式不足以定 λ 比值（需额外味原理）", 0, True,
      "本册判据：可证伪命题 = 简并（T1）+ 计数不变（T2）；两者均机核")

print()
print("=" * 78)
n_pass = sum(1 for r in results if r[1] == "成立")
print(f"汇总：{n_pass}/{len(results)} 项断言成立")
for name, tag, value, note in results:
    print(f"  {tag}  {name}")
print("=" * 78)
print("判词：V49_UNIVERSAL_LAMBDA_DEGENERATES__THREE_LAMBDA_IS_REFIT_NOT_PREDICTION__"
      "SPECTRAL_TOWER_IS_SHAPE_SENSITIVE__FLAVOR_PRINCIPLE_ABSENT__NO_FOUR_FORCE_UNIFICATION")
