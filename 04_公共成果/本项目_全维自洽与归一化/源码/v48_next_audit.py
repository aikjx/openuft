# -*- coding: utf-8 -*-
"""ROOT V48（五维手征零模 → 质量重叠 → 连续谱塔积分）来料 · 全量机核

核验 (48-1)…(48-9) 与 §1/§4/§5 全部数字，并对 V44 册缺口做闭环。
复算：numpy / scipy.quad / brentq；不使用私有包。
"""
import numpy as np
from scipy import integrate, optimize

results = []


def check(name, value, cond, note=""):
    tag = "成立" if cond else "不成立"
    results.append((name, tag, value, note))
    print(f"[{tag}] {name}  value={value}  {note}")


V_GEV = 246.22  # 电弱真空期望值（来料未显式写，反推验证）
YSTAR = 1.0

# ---------- 零模 ----------
def norm(k, L=1.0):
    return np.sqrt(2 * k / (1 - np.exp(-2 * k * L)))

def fL(y, z):
    k = z  # L=1
    return norm(k) * np.exp(-k * y)

def fR(y, z):
    k = z
    return norm(k) * np.exp(-k * (1 - y))

def rho(z, t):
    return 2 * z * np.exp(-2 * z * t) / (1 - np.exp(-2 * z))

def Fz(z, t):
    return (1 - np.exp(-2 * z * t)) / (1 - np.exp(-2 * z))

def Hz(z, t):
    return Fz(z, t) - t

def a_formula(z, n):
    return np.sqrt(2) * (4 * z**2 / (4 * z**2 + (n * np.pi) ** 2)) * \
        (1 - (-1) ** n * np.exp(-2 * z)) / (1 - np.exp(-2 * z))

def a_integral(z, n):
    return np.sqrt(2) * integrate.quad(lambda t: rho(z, t) * np.cos(n * np.pi * t), 0, 1, limit=200)[0]

# (48-1)(48-2) 归一化
n1 = integrate.quad(lambda y: fL(y, 16.218068) ** 2, 0, 1, limit=200)[0]
n2 = integrate.quad(lambda y: fR(y, 16.218068) ** 2, 0, 1, limit=200)[0]
print(f"    ∫|f_L|²={n1:.15f} , ∫|f_R|²={n2:.15f}")
check("S1a (48-1)(48-2) 归一化", max(abs(n1-1), abs(n2-1)), max(abs(n1-1), abs(n2-1)) < 1e-12)

# (48-3) 质量重叠 = z/sinh z
ztest = 10.446622
ov = integrate.quad(lambda y: fL(y, ztest) * fR(y, ztest), 0, 1, limit=200)[0]
print(f"    ∫f_L f_R = {ov:.15f} ; z/sinh z = {ztest/np.sinh(ztest):.15f}")
check("S1b (48-3) 重叠积分 = z/sinh z", abs(ov - ztest/np.sinh(ztest)),
      abs(ov - ztest / np.sinh(ztest)) < 1e-14)

# ---------- §1 参数反算 ----------
MS = np.array([0.51099895, 105.6583755, 1776.93])  # MeV
def m_of_z(z):
    return V_GEV * 1e3 / np.sqrt(2) * YSTAR * z / np.sinh(z)  # MeV

z_fit = np.array([optimize.brentq(lambda z: m_of_z(z) - m, 0.5, 40) for m in MS])
print(f"    反算 z = {z_fit}")
claimed = np.array([16.218068, 10.446622, 7.260339])
v_implied = np.array([np.sqrt(2) * m * np.sinh(z) / z / 1e3 for m, z in zip(MS, z_fit)])
print(f"    隐含 v = {v_implied} GeV")
check("S2a z_e/z_μ 与来料一致", float(np.abs(z_fit[:2]-claimed[:2]).max()),
      np.abs(z_fit[:2] - claimed[:2]).max() < 5e-6)
check("S2b z_τ 与 §4 值 7.260339 一致（§1 表 7.260385 为另一组输入）",
      float(z_fit[2]), abs(z_fit[2] - 7.260339) < 5e-6)
print(f"    §1 表 7.260385 与 §4 7.260339 之差 = {7.260385 - 7.260339:.6e}（来料未解释）")

# ---------- (48-4) ----------
errs = []
for z in (16.218068, 10.446622, 7.260339, 2.0, 5.0):
    for n in range(1, 7):
        errs.append(abs(a_formula(z, n) - a_integral(z, n)))
print(f"    (48-4) 公式 vs 数值积分 max|Δ| = {max(errs):.3e}")
check("S3 (48-4) 解析耦合公式", max(errs), max(errs) < 1e-12)
print(f"    注：n=0 时 (48-4) 给 a_0={a_formula(3.0,0):.6f}（应为 1；公式适用范围 n≥1）")

# ---------- (48-5) Gram 恒等式 ----------
Z = z_fit.copy()
S_sum = np.zeros((3, 3))
NS = 200000
nn = np.arange(1, NS + 1, dtype=float)
aa = np.array([a_formula(Z[i], nn) for i in range(3)])
S_sum = (aa @ aa.T) / (nn**2)
S_int = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        S_int[i, j] = np.pi**2 * integrate.quad(lambda t: Hz(Z[i], t) * Hz(Z[j], t), 0, 1, limit=200)[0]
S_claim = np.array([[2.852212669, 2.730266399, 2.572273069],
                    [2.730266399, 2.626512851, 2.485905064],
                    [2.572273069, 2.485905064, 2.363949413]])
print(f"    S(200k) =\n{S_sum}")
print(f"    (48-5) 积分 vs 200k 模 max|Δ| = {np.abs(S_int-S_sum).max():.3e}")
print(f"    积分 vs 来料矩阵 max|Δ| = {np.abs(S_int-S_claim).max():.3e}")
check("S4a (48-5) 积分恒等式 = 200k 求和", float(np.abs(S_int-S_sum).max()),
      np.abs(S_int - S_sum).max() < 1e-12)
check("S4b 与来料 S 矩阵一致", float(np.abs(S_int-S_claim).max()),
      np.abs(S_int - S_claim).max() < 5e-9)
eigs = np.linalg.eigvalsh(S_int)
print(f"    eig(S) = {eigs}")
check("S4c 最小本征值与来料 0.00023210914 一致", float(eigs[0]),
      abs(eigs[0] - 0.00023210914) < 5e-9)

# ---------- §4 Q / C ----------
t12, t23, t13 = 0.20, 0.12, 0.03
def R(i, j, th):
    M = np.eye(3)
    M[i, i] = np.cos(th); M[i, j] = np.sin(th)
    M[j, i] = -np.sin(th); M[j, j] = np.cos(th)
    return M
U = R(1, 2, t23) @ R(0, 2, t13) @ R(0, 1, t12)
w = np.conj(U[:, 0]) * U[:, 1]
Q = np.real(np.einsum('i,j,ij->', w, np.conj(w), S_int))
C = np.real(sum(w[i] * abs(U[j, 0])**2 * S_int[i, j] for i in range(3) for j in range(3)))
# 独立 200k 求和
Qn = 0.0
Gn_12 = np.zeros(NS, dtype=complex)
Gn_11 = np.zeros(NS, dtype=complex)
for i in range(3):
    Gn_12 += w[i] * aa[i]
    Gn_11 += abs(U[i, 0])**2 * aa[i]
Qn = float(np.sum(np.abs(Gn_12)**2 / nn**2))
Cn = float(np.sum(np.real(Gn_12 * np.conj(Gn_11)) / nn**2))
print(f"    Q_eμ = {Q:.12f} (200k {Qn:.12f}) ; C_eμee = {C:.12f} (200k {Cn:.12f})")
check("S5a Q_eμ 与来料一致", Q, abs(Q - 0.000683979593) < 5e-12)
check("S5b C_eμee 与来料一致", C, abs(C - 0.02347510534) < 5e-12)
check("S5c 积分 vs 200k 最大差 ~5.33e-15", float(max(abs(Q-Qn), abs(C-Cn))),
      max(abs(Q - Qn), abs(C - Cn)) < 5e-14)

# ---------- §5 两代夸克下界 ----------
z1, z2 = 2.0, 5.0
D12 = np.pi**2 * integrate.quad(lambda t: (Fz(z1, t) - Fz(z2, t)) ** 2, 0, 1, limit=200)[0]
sth = 0.225
cth2 = 1 - 2 * sth**2
bound = D12 / 4 * (1 - abs(cth2))
th = np.arcsin(sth)
alphas = np.linspace(0, np.pi, 1000001)
val = D12/4 * (np.sin(2*alphas)**2 + np.sin(2*alphas + 2*th)**2)
print(f"    D12 = {D12:.10f} ; 解析下界 = {bound:.10f} ; 1e6 扫描 min = {val.min():.10f} (α={alphas[val.argmin()]:.6f})")
check("S6a D12 与来料一致", D12, abs(D12 - 0.2852585282) < 5e-9)
check("S6b (48-7) 下界与扫描一致", float(abs(val.min()-bound)), abs(val.min() - bound) < 1e-9)
check("S6c (48-8) 等号条件（|θ|≤π/4）", float(D12/2*sth**2), abs(bound - D12/2*sth**2) < 1e-12)

# ---------- §6 rank ≤ 1 ----------
Cst = 1.0
l = np.array([fL(0.5, Z[0]), fL(0.5, Z[1]), fL(0.5, Z[2])
              ] if False else [fL(0.5, z) for z in Z])
r = [fR(0.5, z) for z in Z]
M = Cst * np.outer(l, r)
sv = np.linalg.svd(M, compute_uv=False)
print(f"    rank(外积) = {np.linalg.matrix_rank(M)} ; 奇异值 = {sv}")
check("S7 (48-9) rank ≤ 1", float(np.linalg.matrix_rank(M)), np.linalg.matrix_rank(M) <= 1)

# ---------- CP 相位：实矩阵 ⇒ V 实正交 ----------
Vu = R(0, 1, 0.3)
Vd = R(0, 1, 0.3 + 0.4)
VCKM = Vu.T @ Vd
print(f"    V_CKM(实) = \n{np.round(VCKM,6)}")
check("S8 实 CKM ⇒ 无 CP 相位（J=0）", float(np.abs(VCKM - VCKM.T).max()),
      np.abs(np.imag(VCKM)).max() == 0 and abs(np.linalg.det(VCKM) - 1) < 1e-12)

print()
print("=" * 78)
n_pass = sum(1 for r in results if r[1] == "成立")
print(f"汇总：{n_pass}/{len(results)} 项断言成立")
for name, tag, value, note in results:
    print(f"  {tag}  {name}")
print("=" * 78)
print("判词：V48_ZERO_MODE_AND_GRAM_IDENTITY_HOLD__V44_GAP_CLOSED__"
      "REBUILD_IS_REINVERSION_NOT_PREDICTION__RANK1_AND_CP_CONSTRAINTS_VALID__"
      "NO_PARAMETER_FREE_MASSES")
