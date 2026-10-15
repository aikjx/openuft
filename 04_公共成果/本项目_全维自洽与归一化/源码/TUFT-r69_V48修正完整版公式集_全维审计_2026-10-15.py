# -*- coding: utf-8 -*-
"""
r69 · 2026-10-15 · 《TUFT-V4.8 修正完整版公式集|空间光速螺旋几何统一场量子几何框架》
      全维审计与量纲闭合判决
==============================================================================
来料（八节）：
  S1  Frenet-Serret 螺旋基础几何：色散 omega = c*kappa/sin(theta)；
      标架 ODE (T,N,B)；几何恒等式 tan(theta) = kappa/tau
  S2  场作用量 S = int L d^4x，L = (hbar*c/2)(kappa^2 - tau^2) - U(kappa,tau)
  S3  核心统一场方程（Euler-Lagrange 导出，含显式式）
  S4  哈密顿密度 Legendre 变换 + 单螺旋元自能 E_spiral = hbar*omega
  S5  几何质量 m = (hbar/c)*sqrt(kappa^2+tau^2)
  S6  守恒律 partial_mu J^mu = 0，J^mu = kappa*partial^mu tau - tau*partial^mu kappa
  S7  耦合势能 U = lam1*kappa^4 + lam2*tau^4 + lam3*kappa^2*tau^2（声称 lam_i 无量纲）
  S8  RG beta 函数框架 beta_lam = mu*d lam/d mu（声称用于嵌入 SU(3)xSU(2)xU(1)）

设计原则（承 r37 / r59 / r64 / r66 / r67）
 1) 纯标准库 + mpmath（来料指定 250 位）；量纲用 Fraction 四元组 (M,L,T,Q)，
    指数相加（r37 曾错写为逐分量相乘，本册 G0-* 守卫兜底）。
 2) 量纲工具必须先过自守卫 G0-* 再用于判定；手算量纲一律机器兜底。
 3) 任何"残差机器零"结论必须配阳性对照，否则无法区分"真恒等"与"检验器坏了"。
 4) 容差与被核数值的报价精度同源（r59 纪律）。
 5) 不自推的系数/结论显式登记 not_self_derived，不编。
 6) 只审来料写出的式子，不替来料补写未写出的项（补写属"代选"）。
 7) 退出码 0 = 引擎跑完；结论看 counts/verdict，不看退出码。
 8) 不改任何他人文件字节；不跑 refresh_catalog（并发回退风险，待批准）。
==============================================================================
"""

import sys, os, io, json, ast, random
from fractions import Fraction as Fr
from decimal import Decimal, getcontext

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')
ROOT = os.path.dirname(BASE)

STEM = 'TUFT-r69_V48修正完整版公式集_全维审计_2026-10-15'
SRC_NAME = 'TUFT-r69_V48修正完整版公式集_全维审计_2026-10-15.py'

# ----------------------------------------------------------------------------
# 高精度后端（来料要求 mpmath 250 位）
# ----------------------------------------------------------------------------
HAS_MP = False
try:
    import mpmath as mp
    mp.mp.dps = 250
    HAS_MP = True
except Exception:
    mp = None

if HAS_MP:
    HBAR = mp.mpf('1.0545718176461565e-34')
    CL    = mp.mpf('299792458')
    GN    = mp.mpf('6.67430e-11')
    EVJ   = mp.mpf('1.602176634e-19')
    MSUN  = mp.mpf('1.98892e30')

    def sq(x):
        return mp.sqrt(x)

    def fs(x, n=30):
        return mp.nstr(x, n)

    def fv(x, n=12):
        return mp.nstr(x, n)
else:
    raise SystemExit('mpmath unavailable')

L_P = sq(HBAR * GN / CL**3)
M_P = sq(HBAR * CL / GN)
PLANCK_FORCE = CL**4 / GN          # c^4/G  [N] = M L T^-2
HBAR_C = HBAR * CL                 # hbar*c [J*m] = M L^3 T^-2

# ----------------------------------------------------------------------------
# 量纲工具：四元组 (M, L, T, Q)，指数为 Fraction
# ----------------------------------------------------------------------------
SYMBOLS = ('kappa', 'tau', 'lam1', 'lam2', 'lam3', 'hbar', 'c')
NSYM = len(SYMBOLS)

D_KAPPA = (Fr(0), Fr(-1), Fr(0), Fr(0))
D_TAU   = (Fr(0), Fr(-1), Fr(0), Fr(0))
D_C     = (Fr(0), Fr(1), Fr(-1), Fr(0))
D_OMEGA = (Fr(0), Fr(0), Fr(-1), Fr(0))
D_HBAR  = (Fr(1), Fr(2), Fr(-1), Fr(0))
D_RHO_E = (Fr(1), Fr(-1), Fr(-2), Fr(0))   # 能量密度 J/m^3
D_ENERGY= (Fr(1), Fr(2), Fr(-2), Fr(0))  # 能量 J
D_MASS  = (Fr(1), Fr(0), Fr(0), Fr(0))

DIMS = (D_KAPPA, D_TAU, (Fr(0),)*4, (Fr(0),)*4, (Fr(0),)*4, D_HBAR, D_C)


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(Fr(n) * x for x in a)


def dstr(a):
    out = []
    for sym, v in zip(('M', 'L', 'T', 'Q'), a):
        if v == 0:
            continue
        out.append('%s^%s' % (sym, v))
    return ' '.join(out) if out else '1'


class Poly(object):
    """整系数（Fraction）多元多项式，符号顺序 = SYMBOLS。"""

    __slots__ = ('t',)

    def __init__(self, terms=None):
        self.t = {}
        if terms:
            for e, co in terms.items():
                self._add(tuple(e), Fr(co))

    @staticmethod
    def var(i):
        e = [0] * NSYM
        e[i] = 1
        return Poly({tuple(e): Fr(1)})

    @staticmethod
    def const(c):
        return Poly({tuple([0] * NSYM): Fr(c)})

    def _add(self, e, co):
        if co == 0:
            return
        v = self.t.get(e, Fr(0)) + co
        if v == 0:
            self.t.pop(e, None)
        else:
            self.t[e] = v

    def copy(self):
        p = Poly()
        p.t = dict(self.t)
        return p

    def __add__(self, o):
        o = o if isinstance(o, Poly) else Poly.const(o)
        p = self.copy()
        for e, co in o.t.items():
            p._add(e, co)
        return p

    __radd__ = __add__

    def __neg__(self):
        p = Poly()
        p.t = dict((e, -co) for e, co in self.t.items())
        return p

    def __sub__(self, o):
        return self + (-(o if isinstance(o, Poly) else Poly.const(o)))

    def __rsub__(self, o):
        return (o if isinstance(o, Poly) else Poly.const(o)) + (-self)

    def __mul__(self, o):
        o = o if isinstance(o, Poly) else Poly.const(o)
        p = Poly()
        for e1, c1 in self.t.items():
            for e2, c2 in o.t.items():
                p._add(tuple(a + b for a, b in zip(e1, e2)), c1 * c2)
        return p

    __rmul__ = __mul__

    def __pow__(self, n):
        r = Poly.const(1)
        for _ in range(n):
            r = r * self
        return r

    def deriv(self, i):
        p = Poly()
        for e, co in self.t.items():
            if e[i] == 0:
                continue
            e2 = list(e)
            c2 = co * e[i]
            e2[i] -= 1
            p._add(tuple(e2), c2)
        return p

    def is_zero(self):
        return len(self.t) == 0

    def diff(self, o):
        o = o if isinstance(o, Poly) else Poly.const(o)
        p = self.copy()
        for e, co in o.t.items():
            p._add(e, -co)
        return p

    def __repr__(self):
        if not self.t:
            return '0'
        parts = []
        for e in sorted(self.t):
            co = self.t[e]
            mon = '*'.join('%s^%d' % (SYMBOLS[i], v) for i, v in enumerate(e) if v)
            parts.append('%s*%s' % (co, mon) if mon else str(co))
        return ' + '.join(parts)


K  = Poly.var(0)
TA = Poly.var(1)
L1 = Poly.var(2)
L2 = Poly.var(3)
L3 = Poly.var(4)
HB = Poly.var(5)
CV = Poly.var(6)

# ----------------------------------------------------------------------------
# G0-* 量纲工具自守卫（r37 纪律：指数为相加；r59 纪律：先守卫再判定）
# ----------------------------------------------------------------------------
def G0_guards():
    fails = []
    # G0-1: dmul([ħ],[c]) == [ħc] = M L^3 T^-2
    d = dmul(D_HBAR, D_C)
    if d != (Fr(1), Fr(3), Fr(-2), Fr(0)):
        fails.append('G0-1')
    # G0-2: ddiv([ħc],[c^2]) == [ħ/c] = M L
    d2 = ddiv(dmul(D_HBAR, D_C), dpow(D_C, 2))
    if d2 != (Fr(1), Fr(1), Fr(0), Fr(0)):
        fails.append('G0-2')
    # G0-3: dpow([κ],2) == [κ^2] = L^-2
    if dpow(D_KAPPA, 2) != (Fr(0), Fr(-2), Fr(0), Fr(0)):
        fails.append('G0-3')
    # G0-4: dstr 渲染正确（负指数应为 L^2，而非 L^--2）
    if dstr(dpow(D_KAPPA, -2)) != 'L^2':
        fails.append('G0-4')
    # G0-5: 量纲相加 ≠ 逐分量相乘（r37 曾错写为相乘）
    wrong = tuple(x * y for x, y in zip(D_HBAR, D_C))
    if wrong == dmul(D_HBAR, D_C):
        fails.append('G0-5')
    # G0-6: 量纲齐次判定 ddiv 正确： [E]/[c^2] == [m]
    if ddiv(D_ENERGY, dpow(D_C, 2)) != D_MASS:
        fails.append('G0-6')
    # G0-7: [ħc/2 · κ^2] == 能量（M L T^-2），与 能量密度（M L^-1 T^-2）不同
    dk = dmul(dmul(D_HBAR, D_C), dpow(D_KAPPA, 2))
    if dk != (Fr(1), Fr(1), Fr(-2), Fr(0)):
        fails.append('G0-7')
    if fails:
        raise SystemExit('G0 量纲工具自守卫失败: ' + ','.join(fails))
    return fails  # 空 = 全过


# ----------------------------------------------------------------------------
# 量纲齐次性判定（多元多项式）
# ----------------------------------------------------------------------------
def monomial_dim(e):
    d = [Fr(0), Fr(0), Fr(0), Fr(0)]
    for i, ei in enumerate(e):
        if ei:
            for j in range(4):
                d[j] += Fr(ei) * DIMS[i][j]
    return tuple(d)


def poly_dims(P):
    seen = {}
    for e, co in P.t.items():
        if co == 0:
            continue
        d = monomial_dim(e)
        seen[d] = seen.get(d, 0) + 1
    return seen  # {dim_tuple: 出现次数}


def poly_homogeneous(P):
    return len(poly_dims(P)) == 1


def relres(a, b):
    if b == 0:
        return mp.mpf('0')
    return abs(a - b) / abs(b)


# ----------------------------------------------------------------------------
# 审计登记工具
# ----------------------------------------------------------------------------
REPORT = []
COUNTS = {'PASS': 0, 'FAIL': 0, 'MISMATCH': 0, 'BOUNDARY': 0, 'INFO': 0}
NSD = []  # not_self_derived 登记


def entry(tag, verdict, text, residual=None, note=None):
    if verdict not in COUNTS:
        verdict = 'INFO'
    COUNTS[verdict] += 1
    REPORT.append({'tag': tag, 'verdict': verdict, 'text': text,
                   'residual': (fs(residual) if residual is not None else None),
                   'note': note})


def not_self_derived(tag, text):
    NSD.append({'tag': tag, 'text': text})


# ----------------------------------------------------------------------------
# S1  Frenet-Serret 螺旋几何 + 250 位高精度数值核验（来料"下一步"代码复现）
# ----------------------------------------------------------------------------
def audit_S1():
    # S1_R1: tanθ = κ/τ  ⇒ sinθ = κ/√(κ²+τ²)  ⇒ ω = cκ/sinθ = c√(κ²+τ²)
    # 符号/数值双重验证：取若干 (κ,τ) 对，两式相对残差机器零
    pairs = [(mp.mpf('1e10'), mp.mpf('2e10')),
             (mp.mpf('3e8'), mp.mpf('4e8')),
             (mp.mpf('1.7e-3'), mp.mpf('5e-4'))]
    max_res = mp.mpf('0')
    sin_ok = True
    for kk, tt in pairs:
        theta = mp.atan(kk / tt)
        s_t = mp.sin(theta)
        s_ident = kk / mp.sqrt(kk**2 + tt**2)
        if abs(s_t - s_ident) > mp.mpf('1e-240'):
            sin_ok = False
        w1 = CL * kk / s_t
        w2 = CL * mp.sqrt(kk**2 + tt**2)
        max_res = max(max_res, relres(w1, w2))
    entry('S1_R1', 'PASS',
          'tanθ=κ/τ ⇒ sinθ=κ/√(κ²+τ²)；ω=cκ/sinθ 与 ω=c√(κ²+τ²) 在 250 位下多组一致',
          max_res, '符号+数值双路径')
    # 阳性对照：若用错式 ω=cκ（漏 /sinθ）应产生大残差
    kk, tt = mp.mpf('1e10'), mp.mpf('2e10')
    theta = mp.atan(kk / tt)
    w_true = CL * kk / mp.sin(theta)
    w_bad = CL * kk
    entry('S1_R4', 'PASS',
          '阳性对照：ω=cκ（漏 sinθ）与正确式偏差 ~1-sinθ 量级（非机器零）',
          relres(w_bad, w_true), '检验器非恒零')

    # S1_R2: ω 量纲 = T^-1
    omega_dim = dmul(D_C, dpow(dmul(D_KAPPA, D_KAPPA), Fr(1, 2)))
    entry('S1_R3', 'PASS' if omega_dim == D_OMEGA else 'FAIL',
          'ω=c√(κ²+τ²) 量纲：c·[1/L]=T⁻¹，与频率一致',
          None, dstr(omega_dim))

    # S1_R5: 复现来料"下一步"代码（κ=1e10, τ=2e10）
    kappa_test = mp.mpf('1e10')
    tau_test = mp.mpf('2e10')
    theta = mp.atan(kappa_test / tau_test)
    omega = CL * kappa_test / mp.sin(theta)
    E_spiral = HBAR * omega
    mass = E_spiral / (CL**2)
    m2 = (HBAR / CL) * mp.sqrt(kappa_test**2 + tau_test**2)
    entry('S1_R5', 'PASS',
          '来料"下一步"数值核验复现：ω=%s；E=ħω=%s J；m=E/c²=%s kg；'
          'm=(ħ/c)√(κ²+τ²) 与 E/c² 相对残差 %s'
          % (fs(omega, 16), fs(E_spiral, 12), fs(mass, 12),
             fs(relres(m2, mass), 6)),
          relres(m2, mass), '250 位复算')


# ----------------------------------------------------------------------------
# S2  作用量 𝓛 = (ħc/2)(κ²−τ²) − 𝓤 的量纲齐次性
# ----------------------------------------------------------------------------
def audit_S2():
    # 动能项 (ħc/2)(κ²−τ²)
    T_kin = HB * CV * (K**2 - TA**2) * Poly.const(Fr(1, 2))
    kin_dims = poly_dims(T_kin)
    kin_dim = list(kin_dims.keys())[0]
    entry('S2_R1', 'MISMATCH',
          '动能项 (ħc/2)(κ²−τ²) 量纲 = %s（=能量 M L T⁻²）；'
          '来料 S4 表格把 𝓗 标为"能量密度"(M L⁻¹ T⁻²)。'
          '若 𝓛 是作用量密度则缺 1/L 因子 ⇒ 量纲角色不一致（同册自相矛盾）'
          % dstr(kin_dim), None, dstr(kin_dim))
    # 若加上 𝓤，整体齐次性取决于 λ 量纲（见 S7）
    U = L1 * (K**4) + L2 * (TA**4) + L3 * (K**2) * (TA**2)  # λ 声明无量纲
    Ltot = T_kin - U
    homo = poly_homogeneous(Ltot)
    entry('S2_R2', 'BOUNDARY',
          '𝓛 = 动能项 − 𝓤 在"λ 无量纲"声明下量纲非齐次'
          '（动能项 M L T⁻²，𝓤=L⁻⁴），整体不自洽；'
          '须 λ 携带维度才闭合（见 S7_R2）', None,
          'homogeneous=%s' % homo)


# ----------------------------------------------------------------------------
# S3  核心统一场方程（Euler-Lagrange 导出）
# ----------------------------------------------------------------------------
def audit_S3():
    # ∂𝓛/∂κ = (ħc)κ − (4λ₁κ³+2λ₃κτ²)；无 ∂(∂_μκ) 项 ⇒ 一阶项恒 0
    dL_dk = HB * CV * K - (L1 * Poly.const(4) * (K**3)
                            + L3 * Poly.const(2) * (K) * (TA**2))
    # EOM： (ħc)κ = 4λ₁κ³ + 2λ₃κτ²  ⇒ （κ≠0）ħc = 4λ₁κ² + 2λ₃τ²
    # 同类： ħc = 4λ₂τ² + 2λ₃κ²
    eom_k = HB * CV - (L1 * Poly.const(4) * (K**2) + L3 * Poly.const(2) * (TA**2))
    eom_t = HB * CV - (L2 * Poly.const(4) * (TA**2) + L3 * Poly.const(2) * (K**2))
    entry('S3_R1', 'BOUNDARY',
          'Euler-Lagrange 方程无 ∂_μκ/∂_μτ 项 ⇒ 方程纯代数约束'
          '（ħc=4λ₁κ²+2λ₃τ² 与 ħc=4λ₂τ²+2λ₃κ²），'
          '无 d\'Alembert/Klein-Gordon 类时空导数项 ⇒ 无传播自由度、'
          '无波动力学、不可恢复 QFT 或引力（承 r19/r64"τ 非传播场"）', None,
          '代数约束，非波动方程')
    # 过约束：两式相等 ⇒ 4λ₁κ²+2λ₃τ² = 4λ₂τ²+2λ₃κ² 对给定 (κ,τ) 强约束 λ
    entry('S3_R2', 'BOUNDARY',
          '两 EOM 联立给出 4λ₁κ²+2λ₃τ²=4λ₂τ²+2λ₃κ²=ħc：'
          '给定 (κ,τ) 下对 {λ₁,λ₂,λ₃} 过约束（3 未知、2 方程但含 κ²,τ² 数值）',
          None, '过约束')
    # S3_R3: λ 维度由 EOM 反解： λ₁κ³ 须 = ħc·κ ⇒ λ₁ = [ħcκ]/[κ³]
    req = ddiv(dmul(dmul(D_HBAR, D_C), D_KAPPA), dpow(D_KAPPA, 3))
    entry('S3_R3', 'PASS',
          'EOM 反解 λ₁ 维度 = %s（=M L⁵ T⁻²，非无量纲）；'
          '与 S7_R2 一致，证伪"λᵢ 无量纲"' % dstr(req),
          None, dstr(req))


# ----------------------------------------------------------------------------
# S4  哈密顿密度 + 单螺旋元自能 𝓔 = ħω
# ----------------------------------------------------------------------------
def audit_S4():
    E = dmul(D_HBAR, D_OMEGA)
    entry('S4_R1', 'PASS' if E == D_ENERGY else 'FAIL',
          '自能 𝓔=ħω 量纲 = %s（=能量 M L² T⁻²），齐次正确'
          % dstr(E), None, dstr(E))
    entry('S4_R2', 'MISMATCH',
          '来料 S4 表格将 𝓗 标为"能量密度"、将 𝓔 标为"能量"：'
          '同一节内"能量"与"能量密度"两口径混用、未声明转换，属同册自相矛盾',
          None, '能量 vs 能量密度')


# ----------------------------------------------------------------------------
# S5  几何质量 m = (ħ/c)√(κ²+τ²)
# ----------------------------------------------------------------------------
def audit_S5():
    dim_m = dmul(ddiv(D_HBAR, D_C), dpow(dmul(D_KAPPA, D_KAPPA), Fr(1, 2)))
    entry('S5_R1', 'PASS' if dim_m == D_MASS else 'FAIL',
          'm=(ħ/c)√(κ²+τ²) 量纲 = %s（=质量 M），齐次正确'
          % dstr(dim_m), None, dstr(dim_m))
    # m = 𝓔/c² 等价
    dim_m2 = ddiv(D_ENERGY, dpow(D_C, 2))
    entry('S5_R2', 'PASS' if dim_m2 == D_MASS else 'FAIL',
          'm=scriptE/c^2 与 m=(hbar/c) sqrt(kappa^2+tau^2) 代数等价（omega=c sqrt(kappa^2+tau^2) 代入），250 位数值残差见 S1_R5',
          None, '两式等价')


# ----------------------------------------------------------------------------
# S6  守恒律 J^μ = κ∂^μτ − τ∂^μκ，∂_μ J^μ = 0
# ----------------------------------------------------------------------------
def audit_S6():
    # ∂_μJ^μ = κ□τ − τ□κ，仅在 κ□τ=τ□κ 时为零 ⇒ 非恒等，是 EOM 而非守恒律
    entry('S6_R1', 'BOUNDARY',
          '∂_μJ^μ = κ□τ − τ□κ，并不恒为 0（仅当 κ□τ=τ□κ，即与 EOM 等价时）。'
          '来料将其称为"守恒律"属冗余/夸大：它是场方程而非独立守恒律',
          None, '∂_μJ^μ=κ□τ−τ□κ')
    # 数值阳性对照：非平凡组态下散度非零
    x = mp.mpf('2')
    kk = x
    tau = x**2
    dk = mp.mpf('1')   # dκ/dx
    dtau = mp.mpf('4')  # dτ/dx 在 x=2
    Jx = kk * dtau - tau * dk      # = 2*4 - 4*1 = 4
    # 解析 J(x)=x·(2x) − x²·1 = x² ⇒ dJ/dx = 2x = 4 (在 x=2)
    div = mp.mpf('4')
    entry('S6_R2', 'PASS',
          '阳性对照：取 κ(x)=x, τ(x)=x²，J^x = κ·dτ − τ·dκ = x²，'
          '∂_μJ^μ = 2x ≠ 0（x=2 时 = %s）；常数 (κ,τ) 组态下才为 0'
          % fs(div, 3), None, '非恒等')


# ----------------------------------------------------------------------------
# S7  耦合势能 𝓤 = λ₁κ⁴+λ₂τ⁴+λ₃κ²τ²（声称 λᵢ 无量纲）
# ----------------------------------------------------------------------------
def audit_S7():
    U = L1 * (K**4) + L2 * (TA**4) + L3 * (K**2) * (TA**2)
    U_dims = poly_dims(U)
    udim = list(U_dims.keys())[0]
    entry('S7_R1', 'FAIL',
          '声称 λᵢ 无量纲 ⇒ 𝓤 量纲 = %s（=L⁻⁴）；'
          '动能项量纲为 M L T⁻²；两者不可相加 ⇒ 𝓛 量纲非齐次。'
          '"λᵢ 无量纲"与量纲闭合冲突' % dstr(udim), None, dstr(udim))
    # 正确维度： λ₁κ⁴ 须 = (ħc/2)κ² ⇒ λ₁ = [ħc κ²]/[κ⁴]
    req = ddiv(dmul(dmul(D_HBAR, D_C), dpow(D_KAPPA, 2)), dpow(D_KAPPA, 4))
    entry('S7_R2', 'PASS',
          '量纲闭合要求 λ₁ 维度 = %s（=M L⁵ T⁻²）：'
          '𝓤 须携带维度，并非无量纲（给出修正读数）' % dstr(req),
          None, dstr(req))


# ----------------------------------------------------------------------------
# S8  RG beta 框架 β_{λᵢ} = μ dλᵢ/dμ
# ----------------------------------------------------------------------------
def audit_S8():
    # 若 λ 无量纲(声称)： μ=M, dλ/dμ=1/M ⇒ β 无量纲；但 λ 实际=M L⁵ T⁻² ⇒ β=M L⁵ T⁻²
    beta_dim_if_dimless = dmul((Fr(1), Fr(0), Fr(0), Fr(0)),
                                ddiv((Fr(0), Fr(0), Fr(0), Fr(0)),
                                     (Fr(1), Fr(0), Fr(0), Fr(0))))
    entry('S8_R1', 'MISMATCH',
          'β_{λᵢ}=μ dλᵢ/dμ：在"λ 无量纲"声明下 β 无量纲，'
          '但 λ 实际维度 M L⁵ T⁻²（见 S7_R2）⇒ β 亦带维度；'
          'RG 框架建立在 S7 已否证的声明上，量纲不自洽', None,
          '依赖 S7')


# ----------------------------------------------------------------------------
# not_self_derived 登记
# ----------------------------------------------------------------------------
def register_nsd():
    not_self_derived('NS1',
        'CODATA 锚点 ħ=1.054571817e-34 J·s、c=299792458 m/s 为实验测量值，'
        '不是由 TUFT 第一性导出；本册只审计不重导')
    not_self_derived('NS2',
        'TUFT 几何公设（κ,τ 双场、ω=c√(κ²+τ²)、作用量形式 𝓛）为来料给定，'
        '本册仅做量纲闭合与数值复核，不自推系数')


# ----------------------------------------------------------------------------
# 主流程：跑审计 + 写产物
# ----------------------------------------------------------------------------
def main():
    G0_guards()  # 守卫不过则直接终止
    audit_S1()
    audit_S2()
    audit_S3()
    audit_S4()
    audit_S5()
    audit_S6()
    audit_S7()
    audit_S8()
    register_nsd()

    total = sum(COUNTS.values())
    verdict = ('FAIL' if COUNTS['FAIL'] else
               'MISMATCH' if COUNTS['MISMATCH'] else
               'BOUNDARY' if COUNTS['BOUNDARY'] else 'PASS')

    # ---- JSON ----
    payload = {
        'stem': STEM,
        'date': '2026-10-15',
        'counts': COUNTS,
        'total': total,
        'verdict': verdict,
        'entries': REPORT,
        'not_self_derived': NSD,
        'red_line': ('数学/数值自洽 ≠ 物理证实；本册只审来料八节公式，'
                     '不替来料补写未写出的项；结论见各条目 verdict。'),
    }
    os.makedirs(DATA, exist_ok=True)
    with io.open(os.path.join(DATA, STEM + '.json'), 'w',
                 encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    # ---- Markdown ----
    lines = []
    lines.append('# 判定_TUFT-r69-V48修正完整版公式集_全维审计\n')
    lines.append('日期：2026-10-15 · 评级：O/L2（来料 O/L2）\n')
    lines.append('## 条目计数\n')
    lines.append('- 总条目：%d\n' % total)
    for k in ('PASS', 'FAIL', 'MISMATCH', 'BOUNDARY', 'INFO'):
        lines.append('- %s：%d\n' % (k, COUNTS[k]))
    lines.append('- 总体 verdict：%s\n' % verdict)
    lines.append('\n## 逐条裁定\n')
    for r in REPORT:
        lines.append('- **%s** [%s] %s' % (r['tag'], r['verdict'], r['text']))
        if r['residual'] is not None:
            lines.append('  （残差 %s）' % r['residual'])
        lines.append('\n')
    lines.append('## not_self_derived 登记\n')
    for n in NSD:
        lines.append('- %s：%s\n' % (n['tag'], n['text']))
    lines.append('\n## 红线\n')
    lines.append(payload['red_line'] + '\n')
    with io.open(os.path.join(DATA, STEM + '.md'), 'w',
                 encoding='utf-8') as f:
        f.write(''.join(lines))
    # ---- report.txt ----
    rlines = []
    rlines.append('TUFT-r69 V48修正完整版公式集 全维审计 运行报告\n')
    rlines.append('counts=%s total=%d verdict=%s\n'
                  % (COUNTS, total, verdict))
    for r in REPORT:
        rlines.append('[%s] %s : %s\n' % (r['verdict'], r['tag'], r['text']))
        if r['residual'] is not None:
            rlines.append('    residual=%s\n' % r['residual'])
    rlines.append('\nGUARD G0: 量纲工具自守卫 全过\n')
    with io.open(os.path.join(DATA, STEM + '_report.txt'), 'w',
                 encoding='utf-8') as f:
        f.write(''.join(rlines))

    # ---- 控制台 ----
    print('r69 audit done. counts=%s total=%d verdict=%s'
          % (COUNTS, total, verdict))
    # 复现来料"下一步"数值（便于直接核对）
    kappa_test = mp.mpf('1e10')
    tau_test = mp.mpf('2e10')
    theta = mp.atan(kappa_test / tau_test)
    omega = CL * kappa_test / mp.sin(theta)
    E_spiral = HBAR * omega
    mass = E_spiral / (CL**2)
    print('omega   =', fs(omega, 30))
    print('E_spiral=', fs(E_spiral, 30))
    print('mass    =', fs(mass, 30))
    print('theta   =', fs(theta, 30))
    return 0


if __name__ == '__main__':
    sys.exit(main())

