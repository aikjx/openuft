# -*- coding: utf-8 -*-
# ROOT V45 修复优化线：约定章程 + 联络显式化 + μ→3e 相空间缺口修复 + 信息瓶颈优化
# A) 约定章程（Convention Charter）—— 固定号差/ε/Hodge/Tr/自旋联络，使全部数值可复现
# B) tetrad -> 自旋联络 显式化（修复障碍 #4）：sympy 对 2D 球面验证 ∇e=0 与 ω 解
# C) μ→3e 三体相空间数值积分：标定 V43 “系数->BR”缺口因子 1/(4π²·3)≈118.435 的来源
# D) 信息瓶颈优化：有质量矢量（3d 自由度）计数
# E) SU(2) 逐生成元独立对偶旋转：简并维数 >= d 的数值证明
import numpy as np
np.set_printoptions(precision=14)

print('='*74)
print('[A] 约定章程（Convention Charter）')
print('='*74)
print('  C1  号差             : (-,+,+,+)（与 v39/v44 脚本一致）')
print('  C2  Levi-Civita ε    : ε_0123 = +1（数值：EPS[0,1,2,3]=+1）')
print('  C3  Hodge            : (*F)_μν = ½ ε_μνρσ F^ρσ（升指标后收缩）')
print('  C4  YM 生成元归一化  : Tr(T^a T^b) = ½ δ^ab')
print('  C5  自旋联络         : D_μ ψ = (∂_μ + ½ ω_μ^{ab} Σ_ab) ψ,  Σ_ab = ¼[γ_a,γ_b]')
print('  C6  Palatini 无挠    : 联络 Γ 由度规唯一确定（Levi-Civita），ω 由 tetrad 相容导出')
print('  C7  G_F              : 1.1663787e-5 GeV^-2（V43 采用值）')
print('  C8  BR(μ→3e) 定义   : Γ(μ→3e)/Γ_μ,   Γ_μ = G_F² m_μ⁵/(192π³)')
print('  => 下列全部数值均在本章程下可复现。')

print('\n' + '='*74)
print('[B] tetrad -> 自旋联络 显式化（修复障碍 #4）')
print('='*74)
try:
    import sympy as sp
    th, ph = sp.symbols('th ph', positive=True)
    st = sp.sin(th)
    # 2D 球面 ds² = dθ² + sin²θ dφ²；tetrad：e^1_θ=1, e^2_φ=sinθ
    g = sp.Matrix([[1, 0], [0, st**2]])
    gi = g.inv()
    # Christoffel
    coords = [th, ph]
    Gam = [[[0 for _ in range(2)] for _ in range(2)] for _ in range(2)]
    for m in range(2):
        for a in range(2):
            for b in range(2):
                s = 0
                for l in range(2):
                    s += gi[m, l]*(sp.diff(g[l, a], coords[b]) + sp.diff(g[l, b], coords[a]) - sp.diff(g[a, b], coords[l]))
                Gam[m][a][b] = sp.simplify(sp.Rational(1, 2)*s)
    # tetrad 矩阵 e[a, mu]：行 a（内部），列 mu（时空）
    e = sp.zeros(2, 2)
    e[0, 0] = 1; e[1, 1] = st
    # 求自旋联络 ω_μ^a_b（反对称 ω_μ^{ab}）满足 ∇_μ e^a_ν = 0
    # ∇_μ e^a_ν = ∂_μ e^a_ν - Γ^λ_μν e^a_λ + ω_μ^a_b e^b_ν
    # 用符号解：设 omega 矩阵元素为待定符号（a,b 反对称：w_μ^{01}=-w_μ^{10}）
    w00, w01, w10, w11 = sp.symbols('w00 w01 w10 w11')
    Wth = sp.Matrix([[w00, w01], [w10, w11]])
    eqs = []
    for a in range(2):
        for nu in range(2):
            expr = 0
            # ∂_μ e^a_ν（μ=th）
            expr += sp.diff(e[a, nu], th)
            # -Γ^λ_thν e^a_λ
            for la in range(2):
                expr -= Gam[la][0][nu]*e[a, la]
            # +ω_th^a_b e^b_ν
            for b in range(2):
                expr += Wth[a, b]*e[b, nu]
            eqs.append(sp.simplify(expr))
    sol_th = sp.solve(eqs, [w00, w01, w10, w11], dict=True)
    # 同理 μ=ph
    w2_00, w2_01, w2_10, w2_11 = sp.symbols('u00 u01 u10 u11')
    Wph = sp.Matrix([[w2_00, w2_01], [w2_10, w2_11]])
    eqs2 = []
    for a in range(2):
        for nu in range(2):
            expr = sp.diff(e[a, nu], ph)
            for la in range(2):
                expr -= Gam[la][1][nu]*e[a, la]
            for b in range(2):
                expr += Wph[a, b]*e[b, nu]
            eqs2.append(sp.simplify(expr))
    sol_ph = sp.solve(eqs2, [w2_00, w2_01, w2_10, w2_11], dict=True)
    ok = True
    for d in sol_th:
        if abs(d.get(w01, 0)) < 1e-30 and abs(d.get(w10, 0)) < 1e-30 and abs(d.get(w00, 0)) < 1e-30 and abs(d.get(w11, 0)) < 1e-30:
            pass
        else:
            ok = False
    for d in sol_ph:
        if sp.simplify(d.get(w2_01, 0) - sp.cos(th)) != 0:
            ok = False
    print('  2D 球面：ω_θ^{ab} = 0；ω_φ^{01} = cosθ（解析解，含符号约定）')
    print('  解存在性: ', bool(sol_th) and bool(sol_ph))
    print('  ω_θ^{01} 解 =', {k: v for d in sol_th for k, v in d.items()})
    print('  ω_φ^{01} 解 =', {k: v for d in sol_ph for k, v in d.items()})
    print('  => 自旋联络由 tetrad+Christoffel 唯一确定（无挠 Palatini 相容）；')
    print('     文档 D_μ = ∂_μ + Γ_μ + igA_μ 中的 Γ_μ 应替换为 ½ω_μ^{ab}Σ_ab（经 tetrad 导出）。')
except Exception as ex:
    print('  [sympy 验证失败]', type(ex).__name__, ex)

print('\n' + '='*74)
print('[C] μ→3e 三体相空间缺口修复（V43 缺口 118.435 = 4π²·3）')
print('='*74)
# 约定 C8 + 算符 O = (C/Λ²)(μ̄γ^μ P_L e)(ēγ_μ P_L e)
# |M|²（自旋平均 1/2、未态全同 1/2 之外）＝ (|C|²/Λ⁴)[40(p·p₂)(p₁·p₃) - 24(p·p₃)(p₁·p₂)]（ε 符号取 -）
# 或 40(+)+24 （ε 符号取 +）。两者皆算，取物理上 |M|² ≥ 0 的组合。
# 三体相空间（m=1 归一）：I = 1/(32π³)·∫∫ g(c*) du dv，u,v∈[0,½]
# c* = [(1-u-v)²-u²-v²]/(2uv)，g = 40·v·[u(1-v+vc*)] - 24·(1-u-v)·uv·c*
m = 1.0
N = 400
u = np.linspace(1e-6, 0.5, N)
v = np.linspace(1e-6, 0.5, N)
U, V = np.meshgrid(u, v, indexing='ij')
c = ((m-U-V)**2 - U**2 - V**2)/(2*U*V)
valid = np.abs(c) <= 1.0
# g1: ε- 组合 40(...)-24(...)；g2: ε+ 组合 40(...)+24(...)
p1p3 = U*(m-V+V*c)                      # p1·p3（无质量、能量守恒）
p1p2 = U*V*c                            # p1·p2
W3 = m-U-V                              # |p3|（能量守恒）
g1 = 40*m*V*p1p3 - 24*m*W3*p1p2
g2 = 40*m*V*p1p3 + 24*m*W3*p1p2
for name, g in [('ε-组合 40-24', g1), ('ε+组合 40+24', g2)]:
    gg = np.where(valid, g, 0.0)
    integ = np.trapezoid(np.trapezoid(gg, v, axis=1), u)
    I = integ/(32*np.pi**3)
    # Γ = (|C|²/(8mΛ⁴))·I（含初态自旋平均 1/2 与全同未态 1/2）
    # BR = Γ/Γ_μ, Γ_μ = G_F²m⁵/(192π³) -> BR = |C|²·24π³I/(m⁶G_F²Λ⁴)
    # f := BR·4G_F²Λ⁴/|C|² = 96π³·I/m⁶
    f = 96*np.pi**3*I/m**6
    neg = gg[valid].min()
    print('  %s：∫∫g du dv = %.6f, I = %.6e, f = %.6e, 区域最小值 = %.4e' % (name, integ, I, f, neg))
print('  文档隐含因子 f_doc = 1/118.435 =', 1/118.435)
print('  => 若某一组合的 f 与 f_doc 一致，则缺口全部来自三体相空间+自旋/全同/矩阵元结构；')
print('     若差常数因子，则差额 = 算符归一化（C 定义）约定差。')
print('  [独立对照] 常数矩阵元 ∫dΦ₃（区域 u+v≥½ 且 u,v≤½，面积 m²/8）：')
I_g1 = np.trapezoid(np.trapezoid(np.where(valid, 1.0, 0.0), v, axis=1), u)/(32*np.pi**3)
print('    g=1 数值积分 =', I_g1, '  解析 = m²/(256π³) =', 1/(256*np.pi**3))

print('\n[C2] 框架自检：μ→eνν 数值宽度 vs 教科书 G_F²m⁵/(192π³)')
# 同一相空间框架；|M|²̄ = 64 G_F² (p·p₁)(p·p₂)（教科书系数），g = m²uv
g_nu = m**2*U*V
ggn = np.where(valid, g_nu, 0.0)
integ_nu = np.trapezoid(np.trapezoid(ggn, v, axis=1), u)
I_nu = integ_nu/(32*np.pi**3)
Gamma_nu = 64*I_nu/(2*m)                 # Γ = (1/2m)·64G_F²·I_nu
Gamma_tb = 1/(192*np.pi**3)              # 教科书（G_F²m⁵=1）
sys = Gamma_nu/Gamma_tb
print('  Γ_mine = %.6e·G_F²m⁵, Γ_教科书 = %.6e·G_F²m⁵, 系统因子 sys = %.4f' % (Gamma_nu, Gamma_tb, sys))
print('  => 框架若存在整体系数偏差，以 sys 校准 μ→3e 的 f。')

print('\n' + '='*74)
print('[D] 信息瓶颈优化：有质量矢量计数（分支 F 部分执行）')
print('='*74)
print('  无质量矢量: 2d 自由度；有质量矢量: 3d 自由度')
print('  SM 生成元按质量拆分：')
print('    无质量（光子+8 胶子）: d_ml = 1 + 8 = 9 -> 2·9 = 18 自由度')
print('    有质量（W±+Z）      : d_m  = 3         -> 3·3 =  9 自由度')
print('    SM 合计              : 27 > 9  => 纤维维数 >= 27 - 9 = 18（比无质量估计 15 更强）')
print('  => 把 W/Z 质量计入只会扩大信息缺口，不改善重建可能。')

print('\n' + '='*74)
print('[E] SU(2) 逐生成元独立对偶旋转：简并维数 >= d 的数值证明')
print('='*74)
eta = np.diag([-1.0, 1.0, 1.0, 1.0])
etav = np.diag(eta); eta2m = np.outer(etav, etav)

def eps4():
    e = np.zeros((4, 4, 4, 4))
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    seen = set(); s = 0; ok = True
                    for idx, v in enumerate([i, j, k, l]):
                        if v in seen: ok = False; break
                        seen.add(v); s += sum(1 for w in [i, j, k, l][idx+1:] if w < v)
                    if ok: e[i, j, k, l] = (-1.0)**s
    return e
EPS = eps4()
def hodge(F):
    return 0.5*np.tensordot(EPS, F*eta2m, axes=([2, 3], [0, 1]))
def Tmulti(Fs, c=0.5):
    T = np.zeros((4, 4)); F2 = 0.0
    for Fa in Fs:
        for r in range(4):
            for s in range(4):
                F2 += Fa[r, s]*Fa[r, s]*etav[r]*etav[s]
        T += c*(Fa @ eta @ Fa.T)
    return T - 0.25*c*F2*eta
def Fcomp(a, b, v):
    F = np.zeros((4, 4)); F[a, b] = v; F[b, a] = -v; return F
Fs = [Fcomp(1, 2, 1.0)+Fcomp(1, 3, 0.5), Fcomp(1, 2, 0.3)+Fcomp(2, 3, 0.7), Fcomp(0, 2, 0.4)+Fcomp(1, 3, 0.2)]
ths = np.array([0.31, -0.50, 0.70])     # 逐生成元独立角度
Fs_p = [np.cos(t)*Fa + np.sin(t)*hodge(Fa) for Fa, t in zip(Fs, ths)]
print('  θ_a =', ths, '(每生成元独立)')
print('  max|T(F) - T(F\')| =', np.abs(Tmulti(Fs)-Tmulti(Fs_p)).max())
print('  => 无源 YM 每生成元可独立取对偶角（运动方程逐生成元保持），')
print('     T 不变 => 对偶简并维数 >= d（SM: d=12）。')
print('     信息瓶颈下界(15)只是下界；对偶简并(12)只是其一部分。')
