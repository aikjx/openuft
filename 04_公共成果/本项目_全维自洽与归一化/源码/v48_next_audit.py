# -*- coding: utf-8 -*-
"""ROOT V48（五维手征零模 → 质量重叠 → 连续谱塔积分）来料 · 全量机核

核验 (48-1)…(48-10) 与 §1/§4/§5 全部数字，并对 V44 册缺口做闭环。
另加四项本轮补记（S9 收敛/判别力、S10 恒等式普适性、S11 自由度与敏感度、
S12 实矩阵 CP 对照）——均标为「本册补记」，不作为来料结论。

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
L = 1.0

# ---------- 零模 ----------
def norm(k, L=L):
    return np.sqrt(2 * k / (1 - np.exp(-2 * k * L)))

def fL(y, z):
    return norm(z) * np.exp(-z * y)

def fR(y, z):
    return norm(z) * np.exp(-z * (L - y))

def rho(z, t):
    return 2 * z * np.exp(-2 * z * t) / (1 - np.exp(-2 * z))

def Fz(z, t):
    return (1 - np.exp(-2 * z * t)) / (1 - np.exp(-2 * z))

def Hz(z, t):
    return Fz(z, t) - t

def a_formula(z, n):
    n = np.asarray(n, dtype=float)
    return np.sqrt(2) * (4 * z**2 / (4 * z**2 + (n * np.pi) ** 2)) * \
        (1 - (-1) ** n * np.exp(-2 * z)) / (1 - np.exp(-2 * z))

def a_integral(z, n):
    return np.sqrt(2) * integrate.quad(lambda t: rho(z, t) * np.cos(n * np.pi * t), 0, 1, limit=200)[0]

# (48-1)(48-2) 归一化
n1 = integrate.quad(lambda y: fL(y, 16.218068) ** 2, 0, L, limit=200)[0]
n2 = integrate.quad(lambda y: fR(y, 16.218068) ** 2, 0, L, limit=200)[0]
print(f"    ∫|f_L|²={n1:.15f} , ∫|f_R|²={n2:.15f}")
check("S1a (48-1)(48-2) 归一化", max(abs(n1 - 1), abs(n2 - 1)), max(abs(n1 - 1), abs(n2 - 1)) < 1e-12)

# (48-3) 质量重叠 = z/sinh z
ztest = 10.446622
ov = integrate.quad(lambda y: fL(y, ztest) * fR(y, ztest), 0, L, limit=200)[0]
print(f"    ∫f_L f_R = {ov:.15f} ; z/sinh z = {ztest/np.sinh(ztest):.15f}")
check("S1b (48-3) 重叠积分 = z/sinh z", abs(ov - ztest / np.sinh(ztest)),
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
check("S2a z_e/z_μ 与来料一致", float(np.abs(z_fit[:2] - claimed[:2]).max()),
      np.abs(z_fit[:2] - claimed[:2]).max() < 5e-6)
check("S2b z_τ 与 §4 值 7.260339 一致（§1 表 7.260385 为另一组输入）",
      float(z_fit[2]), abs(z_fit[2] - 7.260339) < 5e-6)
print(f"    §1 表 7.260385 与 §4 7.260339 之差 = {7.260385 - 7.260339:.6e}（来料未解释）")
m_7260385 = m_of_z(7.260385)
print(f"    z=7.260385 反推 m_τ = {m_7260385:.6f} MeV；与 1776.86（旧 PDG）差 {m_7260385-1776.86:.6f}，与 1776.93（§4）差 {m_7260385-1776.93:.6f}")
check("S2c §1 表 z_τ=7.260385 的输入其实是 m_τ=1776.86（同一文本两套输入）",
      float(abs(m_7260385 - 1776.86)), abs(m_7260385 - 1776.86) < 0.02,
      "§1 与 §4 的 τ 质量输入不同，来料只称『舍入精度』")

# ---------- (48-4) ----------
errs = []
for z in (16.218068, 10.446622, 7.260339, 2.0, 5.0):
    for n in range(1, 7):
        errs.append(abs(a_formula(z, n) - a_integral(z, n)))
print(f"    (48-4) 公式 vs 数值积分 max|Δ| = {max(errs):.3e}")
check("S3 (48-4) 解析耦合公式", max(errs), max(errs) < 1e-12)
print(f"    注：n=0 时 (48-4) 给 a_0={a_formula(3.0,0):.6f}（应为 1；公式适用范围 n≥1）")
# 大 n 渐近：a_n n² → 4√2 z²/π²（说明尾部 ~n^-2）
asy = [abs(a_formula(16.218068, n) * n**2 - 4 * np.sqrt(2) * 16.218068**2 / np.pi**2) for n in (50, 100, 300)]
print(f"    a_n·n² 与 4√2z²/π² 的偏差(n=50/100/300) = {asy}")

# ---------- (48-5) Gram 恒等式 ----------
Z = z_fit.copy()
NS = 200000
nn = np.arange(1, NS + 1, dtype=float)
aa = np.array([a_formula(Z[i], nn) for i in range(3)])   # (3, NS)
S_sum = (aa / nn) @ (aa / nn).T
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
check("S4a (48-5) 积分恒等式 = 200k 求和", float(np.abs(S_int - S_sum).max()),
      np.abs(S_int - S_sum).max() < 1e-12)
check("S4b 与来料 S 矩阵在六位小数内一致（最大差 2.16e-7 来自 z 输入末位）",
      float(np.abs(S_int - S_claim).max()), np.abs(S_int - S_claim).max() < 5e-7)
# S4b2：用 V44 册的六个 z 输入重算，验证差异只是输入末位而非公式
Z44 = np.array([16.218066, 10.446620, 7.260337])
S_from44 = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        S_from44[i, j] = np.pi**2 * integrate.quad(lambda t: Hz(Z44[i], t) * Hz(Z44[j], t), 0, 1, limit=200)[0]
print(f"    用 V44 六位 z 重算 vs 来料 S 矩阵 max|Δ| = {np.abs(S_from44-S_claim).max():.3e}")
check("S4b2 差异全部由 z 输入末位解释", float(np.abs(S_from44 - S_claim).max()),
      np.abs(S_from44 - S_claim).max() < 1e-8, "公式同族、输入末位差 1e-6 ⇒ S 差 1e-7")
eigs = np.linalg.eigvalsh(S_int)
print(f"    eig(S) = {eigs}")
check("S4c 最小本征值与来料 0.00023210914 一致", float(eigs[0]),
      abs(eigs[0] - 0.00023210914) < 5e-9)
check("S4d S 严格正定（全部本征值>0）", float(eigs.min()), eigs.min() > 0,
      f"κ(S)={eigs.max()/eigs.min():.4e}, det(S)={np.linalg.det(S_int):.6e}")

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
# 法二：200k 直接求和
Gn_12 = np.zeros(NS, dtype=complex)
Gn_11 = np.zeros(NS, dtype=complex)
for i in range(3):
    Gn_12 += w[i] * aa[i]
    Gn_11 += abs(U[i, 0])**2 * aa[i]
Qn = float(np.sum(np.abs(Gn_12)**2 / nn**2))
Cn = float(np.sum(np.real(Gn_12 * np.conj(Gn_11)) / nn**2))
# 法三：一维解析积分（(48-5)(48-6) 的直接使用）
bq = np.abs(U[:, 0])**2
Q_int = np.pi**2 * integrate.quad(lambda t: abs(np.sum(w * Fz(Z, t)))**2, 0, 1, limit=200)[0]
C_int = np.pi**2 * integrate.quad(
    lambda t: np.sum(w * Fz(Z, t)) * (np.sum(bq * Fz(Z, t)) - t), 0, 1, limit=200)[0]
print(f"    Q_eμ  : 矩阵={Q:.12f}  200k={Qn:.12f}  积分={Q_int:.12f}")
print(f"    C_eμee: 矩阵={C:.12f}  200k={Cn:.12f}  积分={C_int:.12f}")
check("S5a Q_eμ 与来料一致", Q, abs(Q - 0.000683979593) < 5e-12)
check("S5b C_eμee 与来料一致", C, abs(C - 0.02347510534) < 5e-12)
check("S5c 三法（矩阵/求和/积分）最大差 ~5.33e-15",
      float(max(abs(Q - Qn), abs(C - Cn), abs(Q - Q_int), abs(C - C_int))),
      max(abs(Q - Qn), abs(C - Cn), abs(Q - Q_int), abs(C - C_int)) < 5e-14)

# ---------- §5 两代夸克下界 ----------
z1, z2 = 2.0, 5.0
D12 = np.pi**2 * integrate.quad(lambda t: (Fz(z1, t) - Fz(z2, t)) ** 2, 0, 1, limit=200)[0]
sth = 0.225
th = np.arcsin(sth)
alphas = np.linspace(0, np.pi, 1000001)
val = D12/4 * (np.sin(2*alphas)**2 + np.sin(2*alphas + 2*th)**2)
bound = D12 / 4 * (1 - abs(np.cos(2 * th)))
print(f"    D12 = {D12:.10f} ; 解析下界 = {bound:.10f} ; 1e6 扫描 min = {val.min():.10f} (α={alphas[val.argmin()]:.6f})")
check("S6a D12 与来料一致", D12, abs(D12 - 0.2852585282) < 5e-9)
check("S6b (48-7) 下界与扫描一致", float(abs(val.min()-bound)), abs(val.min() - bound) < 1e-9)
check("S6c (48-8) 等号条件（|θ|≤π/4）", float(D12/2*sth**2), abs(bound - D12/2*sth**2) < 1e-12)

# 补充：|cos2θ|<0 分支（θ=0.9 rad > π/4），验证绝对值形式
th2 = 0.9
val2 = D12/4 * (np.sin(2*alphas)**2 + np.sin(2*alphas + 2*th2)**2)
bound2 = D12 / 4 * (1 - abs(np.cos(2 * th2)))
print(f"    θ=0.9: 扫描 min = {val2.min():.10f} ; (48-7) = {bound2:.10f}（此时 1-cos2θ 会给出 {D12/4*(1-np.cos(2*th2)):.10f}，非下界）")
check("S6d (48-7) 的 |cos2θ| 形式在 θ>π/4 仍成立", float(abs(val2.min()-bound2)),
      abs(val2.min() - bound2) < 1e-9, "去绝对值会低估 → 绝对值是必需的口径")

# ---------- §6 rank ≤ 1 ----------
yH = 0.5
lvec = np.array([fL(yH, z) for z in Z])
rvec = np.array([fR(yH, z) for z in Z])
M = YSTAR * V_GEV / np.sqrt(2) * np.outer(lvec, rvec)
sv = np.linalg.svd(M, compute_uv=False)
print(f"    rank(外积) = {np.linalg.matrix_rank(M)} ; 奇异值 = {sv}")
check("S7a (48-9) rank ≤ 1", float(np.linalg.matrix_rank(M)), np.linalg.matrix_rank(M) <= 1)
Mdiag = np.diag(YSTAR * V_GEV / np.sqrt(2) * lvec * rvec)
svd = np.linalg.svd(Mdiag, compute_uv=False)
print(f"    对角 Yukawa 对照：奇异值 = {svd}（rank=3）")
check("S7b 对角 Yukawa ⇒ rank 3（(48-9) 的前提必须是普适 Yukawa）",
      float(np.linalg.matrix_rank(Mdiag)), np.linalg.matrix_rank(Mdiag) == 3)

# ---------- CP：实矩阵 ⇒ J=0 ----------
def jarlskog(V):
    return float(np.imag(V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1])))

Vreal = R(0, 1, 0.3).T @ R(0, 1, 0.7)
def R13(th, delta):
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, 0, s * np.exp(-1j * delta)],
                     [0, 1, 0],
                     [-s * np.exp(1j * delta), 0, c]])
Vcplx = R(1, 2, 0.12) @ R13(0.03, 1.1) @ R(0, 1, 0.2)
print(f"    V(实) = \n{np.round(Vreal,6)}")
print(f"    J(实) = {jarlskog(Vreal):.3e} ; J(标准参数化 δ=1.1) = {jarlskog(Vcplx):.6e}")
check("S8 实 CKM ⇒ J=0（无 CP）", jarlskog(Vreal), abs(jarlskog(Vreal)) < 1e-15,
      f"|U|=I 检查 max|Δ|={np.abs(Vreal.conj().T @ Vreal - np.eye(3)).max():.2e}")
check("S8b 一个复相位即可 J≠0（CP 相位不可由实矩阵给出）", jarlskog(Vcplx),
      abs(jarlskog(Vcplx)) > 1e-5, f"|U|=I 检查 max|Δ|={np.abs(Vcplx.conj().T @ Vcplx - np.eye(3)).max():.2e}")

# ---------- S9 本册补记：收敛与判别力 ----------
print("\n    [补记 S9] 谱塔求和的截断表（以 (48-5) 积分值为基准，max|Δ| over S）")
S_exact = S_int
for N in (5, 10, 50, 200, 1000, 2500, 10000, NS):
    nnt = np.arange(1, N + 1, dtype=float)
    aat = np.array([a_formula(Z[i], nnt) for i in range(3)])
    St = (aat / nnt) @ (aat / nnt).T
    print(f"      N={N:>6d}  max|Δ|={np.abs(St-S_exact).max():.3e}")
nnt = np.arange(1, 2501, dtype=float)
aat = np.array([a_formula(Z[i], nnt) for i in range(3)])
S2500 = (aat / nnt) @ (aat / nnt).T
check("S9a V44 口径的 2500 模已达 1e-13（200k 只多买浮点噪声）",
      float(np.abs(S2500 - S_exact).max()), np.abs(S2500 - S_exact).max() < 1e-11,
      "尾部 ~ n^-6 ⇒ 200k 无判别力")

# ---------- S10 本册补记：(48-5) 不依赖指数 profile ----------
t0, sig = 0.35, 0.12
Zg = integrate.quad(lambda t: np.exp(-(t - t0)**2 / (2 * sig**2)), 0, 1, limit=200)[0]
rho_g = lambda t: np.exp(-(t - t0)**2 / (2 * sig**2)) / Zg
F_g = lambda t: integrate.quad(rho_g, 0, t, limit=200)[0]
H_g = lambda t: F_g(t) - t
NNg = 400
ng = np.arange(1, NNg + 1, dtype=float)
ag = np.array([np.sqrt(2) * integrate.quad(lambda t: rho_g(t) * np.cos(int(n) * np.pi * t), 0, 1, limit=200)[0]
               for n in ng])
S_g_sum = float(np.sum(ag**2 / ng**2))
S_g_int = np.pi**2 * integrate.quad(lambda t: H_g(t)**2, 0, 1, limit=200)[0]
print(f"    高斯 profile：400 模和 S={S_g_sum:.12f} ; π²∫H²={S_g_int:.12f} ; Δ={abs(S_g_sum-S_g_int):.3e}")
check("S10 (48-5) 对非指数 profile 同样成立（普适 L² 完备性）",
      float(abs(S_g_sum - S_g_int)), abs(S_g_sum - S_g_int) < 1e-10)

# ---------- S11 本册补记：自由度账与 v 敏感度 ----------
for vz in (246.0, 246.22, 246.7):
    zz = np.array([optimize.brentq(lambda z: vz * 1e3 / np.sqrt(2) * z / np.sinh(z) - m, 0.5, 40) for m in MS])
    print(f"    v={vz:>6.2f} GeV → z = {np.round(zz, 6)}")
zv = 246.22 / 246.0 - 1
z_at_246 = np.array([optimize.brentq(lambda z: 246.0 * 1e3 / np.sqrt(2) * z / np.sinh(z) - m, 0.5, 40) for m in MS])
dz = (z_at_246 - z_fit) / z_fit
print(f"    δv/v = {zv:.3e} ⇒ δz/z = {np.round(dz, 8)}")
check("S11 v 变动 0.09% ⇒ z_i 变动同量级（z 是反演量，不是独立预测）",
      float(np.abs(dz).max()), np.abs(dz).max() < 2e-3)
print("    自由度账：输入 {v, y*, L, 边界条件} + 3 个质量 ⇒ 3 个 z_i；S 的 6 个独立元全由 z_i 决定 ⇒ 预测元=6，拟合参数=3")

# ---------- S12 本册补记：V44 最小本征值对照 ----------
S44_eigs = np.linalg.eigvalsh(np.array([[2.852213, 2.730266, 2.572273],
                                        [2.730266, 2.626513, 2.485905],
                                        [2.572273, 2.485905, 2.363949]]))
print(f"    V44 六位报价矩阵 eig_min = {S44_eigs[0]:.6e} ; V48 eig_min = {eigs[0]:.6e} ; 相对差 = {abs(S44_eigs[0]-eigs[0])/eigs[0]:.3e}")
check("S12 矩阵六位一致 ≠ 谱一致（最小本征值相对差 ~1e-3）",
      float(abs(S44_eigs[0]-eigs[0])/eigs[0]), abs(S44_eigs[0]-eigs[0])/eigs[0] < 5e-3,
      "报价位数放大到谱上；κ 随之改变")

# ---------- S13 本册补记：质量公式的单调性与上界 ----------
zs = np.linspace(1e-3, 40, 2000)
ms = np.array([m_of_z(z) for z in zs])
mono = bool(np.all(np.diff(ms) < 0))
m_sup = V_GEV * 1e3 / np.sqrt(2)
z_top = optimize.brentq(lambda z: m_of_z(z) - 172690.0, 1e-3, 40)
print(f"    m(z) 在 (0,40) 严格单调递减 = {mono} ; 上确界 m(0)=v/√2={m_sup:.4f} MeV ; 顶夸克 172.69 GeV ↔ z={z_top:.6f}")
check("S13 (48-3) 单调递减且上界 = v/√2（重味 ⇔ 弱局域化）", float((m_sup - ms.max()) / m_sup),
      mono and (m_sup - ms.max()) / m_sup < 1e-6, f"z_t≈{z_top:.4f}，顶夸克几乎贴着上界")

# ---------- S14 本册补记：δ 极限还原 V47 的点费米子闭式 ----------
def H_step(x, t):
    return np.where(t < x, -t, 1 - t)

def S_step(x, y):
    return np.pi**2 * integrate.quad(lambda t: H_step(x, t) * H_step(y, t), 0, 1, limit=200)[0]

def S_v47(x, y):
    return np.pi**2 * (1/3 - max(x, y) + (x**2 + y**2)/2)

err14 = max(abs(S_step(x, y) - S_v47(x, y)) for x, y in ((0.15, 0.5), (0.5, 0.85), (0.15, 0.85), (0.3, 0.3)))
D_step = np.pi**2 * integrate.quad(lambda t: (H_step(0.15, t) - H_step(0.5, t))**2, 0, 1, limit=200)[0]
print(f"    δ 极限：π²∫H_xH_y vs V47 闭式 max|Δ| = {err14:.3e}；π²∫(H_x−H_y)² = {D_step:.12f}，π²|x−y| = {np.pi**2*0.35:.12f}")
check("S14 (48-5) 在 δ 极限还原 V47 点费米子闭式", float(err14), err14 < 1e-12,
      f"D(x,y)=π²|x−y| 差 {abs(D_step-np.pi**2*0.35):.2e} ⇒ 两册同源")

# ---------- S15 本册补记：来料 S 矩阵用的是哪组 z ----------
Z1 = np.array([16.218066, 10.446620, 7.260385])  # §1「重新求解」列
S_from1 = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        S_from1[i, j] = np.pi**2 * integrate.quad(lambda t: Hz(Z1[i], t) * Hz(Z1[j], t), 0, 1, limit=200)[0]
print(f"    用 §1 列 z（7.260385）重算 vs 来料 S 矩阵 max|Δ| = {np.abs(S_from1-S_claim).max():.3e}")
check("S15 来料 S 矩阵来自 V44 的 z，不是 §1「重新求解」列", float(np.abs(S_from1 - S_claim).max()),
      np.abs(S_from1 - S_claim).max() > 1e-6,
      "同一来料的两组输出分别建立在两组输入上（S 用旧 z、Q/C 用新 z）")

print()
print("=" * 78)
n_pass = sum(1 for r in results if r[1] == "成立")
print(f"汇总：{n_pass}/{len(results)} 项断言成立")
for name, tag, value, note in results:
    print(f"  {tag}  {name}")
print("=" * 78)
print(f"判词：V48_NUMBERS_REPRODUCED_{n_pass}_{len(results)}__GRAM_IDENTITY_IS_STANDARD_PARSEVAL__"
      "V44_REBUILD_SAME_FAMILY_REINVERSION__200K_MODES_NO_DISCRIMINATING_POWER__"
      "TWO_GEN_BOUND_VALID_CONDITIONAL__RANK1_AND_CP_OBSTRUCTIONS_VALID__"
      "THREE_Z_FITTED_NOT_PREDICTED__FOUR_FORCES_NOT_UNIFIED")
