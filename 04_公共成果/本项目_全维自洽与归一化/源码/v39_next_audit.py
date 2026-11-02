# -*- coding: utf-8 -*-
"""ROOT V39 下一阶段（主丛复合几何统一作用量）来料 · 增量机核

只做 v39_audit.py 未覆盖的五项，不重复其 Rainich / 无源对偶 / 量纲三表：
  S1 作用量符号与归一化：+1/4 Tr(F^2) vs 标准 -1/4 F^a F^a（C1+C4 下）
  S2 非阿贝尔"对偶"是否存在：d(*F) = -[A,*F] ≠ 0 ⇒ 无对偶势
  S3 null 场：F^2 = F*tF = 0 但 T^2 ≠ 0（多生成元）
  S4 模数计数：Ad-不变对称双线性型维数（su2/su3）+ 等距方向计数
  S5 Palatini "无挠"与旋量耦合的矛盾：δS_fermion/δω ≠ 0

约定（V45 章程 C1-C4）：号差 (-,+,+,+)，ε_0123=+1，Hodge=½εF，
Tr(T^aT^b)=½δ^ab，标准 YM 动能项 = -1/4 Σ_a F^a_{μν}F^{aμν} = -½ Tr(F_{μν}F^{μν})。
"""
import numpy as np
import sympy as sp

ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
EPS4 = np.zeros((4, 4, 4, 4))
for _p in __import__("itertools").permutations(range(4)):
    EPS4[_p] = np.linalg.det(np.eye(4)[list(_p)])
LC3 = np.zeros((3, 3, 3))
for _p in __import__("itertools").permutations(range(3)):
    LC3[_p] = np.linalg.det(np.eye(3)[list(_p)])

results = []


def check(name, value, cond, note=""):
    tag = "成立" if cond else "不成立"
    results.append((name, tag, value, note))
    print(f"[{tag}] {name}  value={value}  {note}")


def F_EB(E, B):
    """F_{0i}=E_i, F_{ij}=eps_{ijk}B_k（与脚本 v39_audit.py 同约定）"""
    F = np.zeros((4, 4))
    for i in range(3):
        F[0, i + 1] = E[i]
        F[i + 1, 0] = -E[i]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                F[i + 1, j + 1] += LC3[i, j, k] * B[k]
    return F


def Fsq(F):
    """F_{μν}F^{μν}（C1 号差）"""
    return sum(F[m, n] * F[m, n] * ETA[m, m] * ETA[n, n] for m in range(4) for n in range(4))


def T_munu(F):
    """标准能动张量：T_{μν}=F_{μρ}F_ν^ρ-¼g_{μν}F^2（对应 -1/4 作用量）"""
    T = F @ ETA @ F.T
    return T - 0.25 * Fsq(F) * ETA


def raise1(T):
    """T^μ_ν = eta^{μα} T_{αν}"""
    return ETA @ T


print("=" * 78)
print("[S1] 作用量符号 / 归一化：+1/4 Tr(F^2) 与 C1+C4 的冲突")
print("=" * 78)
E = np.array([1.0, 0.0, 0.0])
B = np.array([0.0, 2.0, 0.0])
F = F_EB(E, B)
f2 = Fsq(F)
Lplus = 0.25 * f2          # 来料写法 +1/4 Tr(F^2)（单生成元 T=1 时 Tr(F^2)=F^2）
Lminus = -0.25 * f2        # C1 下应有的标准系数
T = T_munu(F)
T_from_plus = -T           # 由 +1/4 作用量变分得到的能动张量 = -T_standard
print(f"    E={E}, B={B}")
print(f"    F_munu F^munu = {f2:.6f}   (= -2E^2 + 2B^2)")
print(f"    L(+1/4) = {Lplus:.6f}   ;  L(-1/4) = {Lminus:.6f}")
print(f"    T00(来料给出的 T 公式)          = {T[0,0]:.6f}   (= (E^2+B^2)/2)")
print(f"    T00(由 +1/4 作用量实际变分)      = {T_from_plus[0,0]:.6f}")
print(f"    T^mu_mu(标准)                   = {np.trace(raise1(T)):.3e}  (4维 YM 共形无迹)")
t00_plus = float(T_from_plus[0, 0])
t00_doc = float(T[0, 0])
trT = float(np.trace(raise1(T)))
check("S1a 来料 +1/4 作用量给负能/鬼态", t00_plus, t00_plus < 0, f"T00={t00_plus:.6f}")
check("S1b 来料 T 公式对应 -1/4 而非 +1/4", abs(t00_doc - t00_plus), abs(t00_doc - t00_plus) > 1,
      "同文两式符号互斥")
check("S1c 4维 YM 能动张量共形无迹", trT, abs(trT) < 1e-12, f"tr={trT:.2e}")

# C4 下 Tr(F^2) = ½ Σ_a (F^a)^2 ⇒ 来料 +¼Tr = +⅛Σ(F^a)^2，标准为 -¼Σ
ratio = (0.25 * 0.5) / -0.25
print(f"    C4 下 Tr(F^2)=½Σ(F^a)^2 ⇒ 来料(+¼Tr)/标准(-¼Σ) = {ratio}")
check("S1d 归一化差因子 (符号+幅度)", ratio, abs(ratio + 0.5) < 1e-15, "应为 -1/2")

print()
print("=" * 78)
print("[S2] 非阿贝尔情形是否存在'对偶势/对偶变换'：d(*F) = -[A,*F]")
print("=" * 78)
x, y, z, t = sp.symbols('x y z t', real=True)
COORD = [t, x, y, z]
sx = sp.Matrix([[0, 1], [1, 0]])
sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
sz = sp.Matrix([[1, 0], [0, -1]])
TT = [s / 2 for s in (sx, sy, sz)]  # Tr(T^aT^b)=½δ^ab

A = [sp.zeros(2, 2) for _ in range(4)]
A[0] = x * TT[0]     # A_0 = x T^1
A[2] = x * TT[1]     # A_2 = x T^2
Fm = [[sp.zeros(2, 2) for _ in range(4)] for _ in range(4)]
for mu in range(4):
    for nu in range(4):
        Fm[mu][nu] = (sp.diff(A[nu], COORD[mu]) - sp.diff(A[mu], COORD[nu])
                      + sp.I * (A[mu] * A[nu] - A[nu] * A[mu]))

Fup = [[ETA[mu, mu] * ETA[nu, nu] * Fm[mu][nu] for nu in range(4)] for mu in range(4)]
Fd = [[sp.zeros(2, 2) for _ in range(4)] for _ in range(4)]
for mu in range(4):
    for nu in range(4):
        Fd[mu][nu] = sp.Rational(1, 2) * sum((EPS4[mu, nu, r, s] * Fup[r][s]
                                              for r in range(4) for s in range(4)),
                                             sp.zeros(2, 2))
Fdup = [[ETA[mu, mu] * ETA[nu, nu] * Fd[mu][nu] for nu in range(4)] for mu in range(4)]

div_dual = [sp.zeros(2, 2) for _ in range(4)]   # ∂_μ (*F)^{μν}
comm = [sp.zeros(2, 2) for _ in range(4)]       # i[A_μ, (*F)^{μν}]
for nu in range(4):
    for mu in range(4):
        div_dual[nu] += sp.diff(Fdup[mu][nu], COORD[mu])
        comm[nu] += sp.I * (A[mu] * Fdup[mu][nu] - Fdup[mu][nu] * A[mu])
POINT = {t: 0, x: 1, y: 2, z: 3}


def mat_max(M):
    return max(abs(complex(sp.N(sp.simplify(v.subs(POINT))))) for v in list(M))


dmax = max(mat_max(m) for m in div_dual)
bianchi = max(mat_max(div_dual[nu] + comm[nu]) for nu in range(4))
print(f"    A_0=x T^1, A_2=x T^2, g=1；F_02 = {sp.simplify(Fm[0][2])}")
print(f"    max|d(*F)| = {dmax}")
print(f"    max|d(*F)+i[A,*F]| = {bianchi}   (Bianchi 恒等式)")
check("S2a *F 非闭（非阿贝尔）", dmax, dmax != 0, "⇒ 不存在对偶势 A'")
check("S2b 同一 A 上 Bianchi 仍恒成立", bianchi, bianchi < 1e-12, f"max|D*F|={bianchi}")

print()
print("=" * 78)
print("[S3] null 场：每个生成元 F^a 幂零，但多生成元 T^2 ≠ 0")
print("=" * 78)
E1, B1 = np.array([1.0, 0, 0]), np.array([0, 1.0, 0])
E2, B2 = np.array([0, 0, 1.0]), np.array([1.0, 0, 0])
Fa = [F_EB(E1, B1), F_EB(E2, B2)]
print(f"    E1·B1={np.dot(E1,B1)}, |E1|=|B1|={np.linalg.norm(E1)==np.linalg.norm(B1)}")
print(f"    E2·B2={np.dot(E2,B2)}, |E2|=|B2|={np.linalg.norm(E2)==np.linalg.norm(B2)}")
f2a = [Fsq(f) for f in Fa]
fduala = []
for f in Fa:
    fd = np.zeros((4, 4))
    for mu in range(4):
        for nu in range(4):
            fd[mu, nu] = 0.5 * sum(EPS4[mu, nu, r, s] * f[r, s] for r in range(4) for s in range(4))
    fduala.append(sum(f[mu, nu] * fd[mu, nu] for mu in range(4) for nu in range(4)))
Tnil = np.zeros((4, 4))
for f in Fa:
    Tnil += f @ ETA @ f.T
Tnil -= 0.25 * sum(f2a) * ETA
Tmix = raise1(Tnil)
T2 = Tmix @ Tmix
resid = T2 - 0.25 * np.trace(T2) * np.eye(4)
print(f"    F_a^2 = {f2a} ,  F_a *F_a = {fduala}")
print(f"    tr(T^mu_nu) = {np.trace(Tmix):.3e}")
print(f"    T^2 对角线 = {np.diag(T2)}")
print(f"    max|T^2 - ¼tr(T^2) I| = {np.abs(resid).max():.6f} ,  ||T^2||_F = {np.linalg.norm(T2):.6f}")
trTnil = float(np.trace(Tmix))
nm2 = float(np.linalg.norm(T2))
rmax = float(np.abs(resid).max())
check("S3a 每个 F^a 幂零", max(abs(v) for v in f2a + fduala),
      all(abs(v) < 1e-12 for v in f2a + fduala), f"F^2={f2a}")
check("S3b 多生成元 T^2 ≠ 0（非单场幂零）", nm2, nm2 > 1e-6, f"tr={trTnil:.2e}")
check("S3c T^2 不∝I（Rainich 二次幂失效）", rmax, rmax > 1e-3, f"resid={rmax:.6f}")

print()
print("=" * 78)
print("[S4] 模数计数：Ad-不变对称双线性型维数（=G-不变度规参数个数）")
print("=" * 78)


def f_structure(lam):
    n = len(lam)
    f = np.zeros((n, n, n))
    for a in range(n):
        for b in range(n):
            C = lam[a] @ lam[b] - lam[b] @ lam[a]
            for c in range(n):
                val = np.trace(C @ lam[c]) / (2 * sp.I)
                f[a, b, c] = complex(val).real
    return f


def invariant_form_dim(f):
    n = f.shape[0]
    pairs = [(a, b) for a in range(n) for b in range(a, n)]
    rows = []
    for d in range(n):
        for a in range(n):
            for b in range(n):
                row = np.zeros(len(pairs))
                for idx, (p, q) in enumerate(pairs):
                    s = 0.0
                    for c in range(n):
                        s += f[d, a, c] * (1.0 if (c, b) == (p, q) or (b, c) == (p, q) else 0.0)
                        s += f[d, b, c] * (1.0 if (c, a) == (p, q) or (a, c) == (p, q) else 0.0)
                    row[idx] = s
                rows.append(row)
    S = np.array(rows)
    return len(pairs) - np.linalg.matrix_rank(S, tol=1e-8)


lam_su2 = [np.array(m, dtype=complex) for m in
           [[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]]]
# Gell-Mann（λ_a，T_a=λ_a/2；Tr(T^aT^b)=½δ^ab）
gm = []
gm.append(np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]))
gm.append(np.array([[0, -1j, 0, 0], [1j, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]))
gm.append(np.array([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]))
gm.append(np.array([[0, 0, 1, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]]))
gm.append(np.array([[0, 0, -1j, 0], [0, 0, 0, 0], [1j, 0, 0, 0], [0, 0, 0, 0]]))
gm.append(np.array([[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]]))
gm.append(np.array([[0, 0, 0, 0], [0, 0, -1j, 0], [0, 1j, 0, 0], [0, 0, 0, 0]]))
m8 = np.zeros((4, 4))
m8[0, 0] = 1; m8[1, 1] = 1; m8[2, 2] = -2
gm.append(m8 / np.sqrt(3))
lam_su3 = [np.array(m, dtype=complex) for m in gm]

d_su2 = invariant_form_dim(f_structure(lam_su2))
d_su3 = invariant_form_dim(f_structure(lam_su3))
print(f"    dim(Ad-不变对称型, su(2)) = {d_su2}")
print(f"    dim(Ad-不变对称型, su(3)) = {d_su3}")
print(f"    dim(G) = 8+3+1 = {8+3+1} ; dim(Isom) >= 2*8+2*3+1 = {2*8+2*3+1}")
moduli = d_su3 + d_su2 + 1
print(f"    ⇒ G-不变度规模数 = {d_su3}+{d_su2}+1 = {moduli}")
print(f"    ⇒ 自由参数 {{κ_D, λ3, λ2, λ1}} = {moduli+1}  ↔  {{κ4, g3, g2, g1}} = 4")
check("S4a 单因子不变型唯一（su2/su3 各 1 维）", f"{d_su2},{d_su3}",
      d_su2 == 1 and d_su3 == 1, "Killing 型唯一 ⇒ 每因子 1 个尺度")
check("S4b 参数个数守恒 4↔4（KK 只换名不约化）", moduli + 1,
      moduli == 3 and moduli + 1 == 4, "3 模数 + κ_D ↔ 3 耦合 + κ4")

print()
print("=" * 78)
print("[S5] Palatini '无挠' 与旋量耦合：δS_fermion/δω ≠ 0")
print("=" * 78)
I2 = np.eye(2)
s3 = [np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]),
      np.array([[1, 0], [0, -1]]), I2]
g0 = np.block([[np.zeros((2, 2)), I2], [I2, np.zeros((2, 2))]])
gi = [np.block([[np.zeros((2, 2)), s], [-s, np.zeros((2, 2))]]) for s in s3]
GAM = [g0] + gi
S01 = 0.25 * (GAM[0] @ GAM[1] - GAM[1] @ GAM[0])
psi = np.zeros(4, dtype=complex); psi[0] = 1.0
psibar = psi.conj() @ GAM[0]
J0_01 = psibar @ GAM[0] @ S01 @ psi
psi2 = np.array([1.0, 2.0, 3.0, 4.0], dtype=complex)
psibar2 = psi2.conj() @ GAM[0]
J_gen = [psibar2 @ GAM[mu] @ S01 @ psi2 for mu in range(4)]
Jmax = max(abs(v) for v in J_gen)
print(f"    ψ=(1,0,0,0): <ψ̄ γ^0 Σ_01 ψ> = {J0_01}")
print(f"    一般 ψ: <ψ̄ γ^μ Σ_01 ψ> = {[complex(v) for v in J_gen]}  → max|J|={Jmax}")
check("S5a 旋量对自旋联络有非零源（⇒ 挠率被激发）", Jmax, Jmax > 1e-6,
      "ψ=(1,0,0,0) 恰为零是特例，一般旋量非零")
print("    ⇒ 来料 §2 '对联络变分 → 无挠' 只在 S_matter 不含联络时成立；")
print("      同一文档的 D_μ 已含 Γ ⇒ 变分给非零挠率（须由 V45 C6 的 tetrad 相容条件强制无挠）")

print()
print("=" * 78)
n_pass = sum(1 for r in results if r[1] == "成立")
print(f"汇总：{n_pass}/{len(results)} 项断言成立")
for name, tag, value, note in results:
    print(f"  {tag}  {name}")
print("=" * 78)
print("判词：V39_NEXT_STAGE_RESTATED__STRUCTURE_SOUND_COEFFICIENTS_BROKEN__"
      "KK_MODULI_EQ_COUPLINGS__NONABELIAN_DUALITY_VACUOUS__NULL_FIELD_T2_NONZERO__"
      "COMMON_ORIGIN_UNPROVEN")
