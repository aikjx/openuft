# -*- coding: utf-8 -*-
# TUFT r73 · V4.8《量纲核验报告》的口径补全与 l_0 排除定理（二次增量）
# 2026-10-15 · 承接 r61（同一份来料的一次自审：T01-T09 + 14 guard）
# 本册定位：不重复裁定 r61 已定的五条核心，只补 r61 未覆盖的两层
#   (1) 口径层：sqrt(-g) 与 d^4x 的配对、隐藏的 c、不变四体积测度下的系数量纲
#   (2) 数值层：l_0 排除定理（幂次穷举）、自能-截断定理、不同 l_0 候选的杠杆级数
import io
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, '数据')
NAME = 'TUFT-r73_V48量纲核验报告的口径补全与l0排除定理_全维审计_2026-10-15'

# ---- 常数（SI，CODATA 2018 口径；c 为定义精确值）--------------------------
c = Decimal('299792458')
G = Decimal('6.67430e-11')
hbar = Decimal('1.054571817e-34')
M_E = Decimal('9.1093837015e-31')
M_MU = Decimal('1.883531627e-28')
M_TAU = Decimal('1.77686e-27')
PI = Decimal('3.14159265358979323846264338327950288')
LP_LIT = Decimal('1.616255e-35')


def Dc(x):
    return Decimal(str(x))


def dsqrt(x):
    return (x.ln() / Decimal(2)).exp()


def fv(x, sig=12):
    try:
        return '%.*E' % (sig, x)
    except Exception:
        return str(x)


lP = dsqrt(hbar * G / (c * c * c))

GUARD = []


def guard(name, ok, note=''):
    GUARD.append({'guard': name, 'ok': bool(ok), 'note': note})
    return bool(ok)


ITEMS = []


def add(code, verdict, title, detail, evidence=''):
    ITEMS.append({'code': code, 'verdict': verdict, 'title': title,
                  'detail': detail, 'evidence': evidence})


def PA(a, t, d, e=''):
    add(a, 'PASS', t, d, e)


def FA(a, t, d, e=''):
    add(a, 'FAIL', t, d, e)


def CO(a, t, d, e=''):
    add(a, 'CORRECTED', t, d, e)


def IN(a, t, d, e=''):
    add(a, 'INFO', t, d, e)


def MI(a, t, d, e=''):
    add(a, 'MISMATCH', t, d, e)


def BO(a, t, d, e=''):
    add(a, 'BOUNDARY', t, d, e)


# =============================================================================
# 量纲代数 (M, L, T)：乘法=指数相加；加减法要求同族，异族直接抛错（r61 教训）
# =============================================================================
class Dim(object):
    def __init__(self, m=0, l=0, t=0):
        self.v = (F(m), F(l), F(t))

    def __mul__(self, o):
        return Dim(*[self.v[i] + o.v[i] for i in range(3)])

    __rmul__ = __mul__

    def __truediv__(self, o):
        return Dim(*[self.v[i] - o.v[i] for i in range(3)])

    def __rtruediv__(self, o):
        # 标量 o / self：o 视为无量纲，等价于 self 取逆
        return Dim(*[-v for v in self.v])

    def __pow__(self, k):
        k = F(k)
        return Dim(*[self.v[i] * k for i in range(3)])

    def __add__(self, o):
        if self.v != o.v:
            raise TypeError('dim family mismatch: %s + %s' % (dstr(self), dstr(o)))
        return Dim(*self.v)

    def __sub__(self, o):
        if self.v != o.v:
            raise TypeError('dim family mismatch: %s - %s' % (dstr(self), dstr(o)))
        return Dim(*self.v)

    def __eq__(self, o):
        return tuple(self.v) == tuple(o.v)

    def __ne__(self, o):
        return not self.__eq__(o)

    def __hash__(self):
        return hash(tuple(self.v))


def dstr(d):
    out = []
    for name, e in zip(('M', 'L', 'T'), d.v):
        if e == 0:
            continue
        if e == 1:
            out.append(name)
        else:
            out.append('%s^%s' % (name, e))
    return '1' if not out else ' '.join(out)


DIM_M = Dim(1, 0, 0)
DIM_L = Dim(0, 1, 0)
DIM_T = Dim(0, 0, 1)
DIM_1 = Dim(0, 0, 0)

# 基本量的机器量纲
D_hbar = DIM_M * DIM_L ** 2 / DIM_T                 # J*s
D_c = DIM_L / DIM_T
D_G = DIM_L ** 3 / (DIM_M * DIM_T ** 2)
D_kappa = 1 / DIM_L                                 # Frenet 曲率
D_grad_kappa = D_kappa / DIM_L                      # 梯度再加一次长度倒数
D_lap_kappa = D_grad_kappa / DIM_L                  # 拉普拉斯再乘一次长度倒数
D_omega = 1 / DIM_T
D_l0 = DIM_L
D_energy = DIM_M * DIM_L ** 2 / DIM_T ** 2
D_action = DIM_M * DIM_L ** 2 / DIM_T
D_edens = D_energy / DIM_L ** 3                     # J/m^3
D_force = DIM_M * DIM_L / DIM_T ** 2                # N = kg*m*s^-2

# ---- 量纲工具自身的守卫（任何判定之前先自证，r37/r61 同型纪律）------------
guard('G0-1-hbar', D_hbar == D_action, '[hbar] 必须等于作用量量纲 M L^2 T^-1')
guard('G0-2-hbar-c', D_hbar * D_c == DIM_M * DIM_L ** 3 / DIM_T ** 2,
      '[hbar c] = M L^3 T^-2')
guard('G0-3-hbar-over-c', D_hbar / D_c == DIM_M * DIM_L, '[hbar/c] = M L')
guard('G0-4-grad-kappa', D_grad_kappa ** 2 == 1 / DIM_L ** 4,
      '[|grad kappa|^2] = L^-4（kappa=L^-1 且梯度再加一次 L^-1）')
guard('G0-5-energy-density', D_edens == DIM_M / (DIM_L * DIM_T ** 2),
      '[能量密度] = M L^-1 T^-2')
guard('G0-6-dim-add-mismatch-raises', True, '')
_raised = False
try:
    _tmp = D_grad_kappa ** 2 + D_kappa ** 2          # L^-4 + L^-2 必须炸
except TypeError:
    _raised = True
GUARD[-1] = {'guard': 'G0-6-dim-add-mismatch-raises', 'ok': _raised,
             'note': 'L^-4 与 L^-2 相加必须抛 TypeError（ Else 会被静默通过）'}
guard('G0-7-planck-length', dstr(D_lP_ := D_l0) in ('L',), '[l_0] = L')
guard('G0-8-lNewton-identity', D_hbar * D_c / D_l0 ** 2 == D_c ** 4 / D_G,
      '[hbar c / l_0^2] 与 [c^4/G] 同族（均为力）')
# =============================================================================
# 组 A · 口径层：测度约定决定「系数量纲」，而 l_0 在任何约定下都被排除
# =============================================================================
# 两条自洽实现 + 来料实际使用的「名义混合约定」
D_sqrtg_A = DIM_1                 # 约定 A：x^0 = ct
D_d4x_A = DIM_L ** 4
D_sqrtg_B = D_c                   # 约定 B：x^0 = t，g_00 = -c^2 ⇒ sqrt(-g) 携带 c
D_d4x_B = DIM_L ** 3 * DIM_T
INV_A = D_sqrtg_A * D_d4x_A
INV_B = D_sqrtg_B * D_d4x_B
guard('G1-invariant-volume', INV_A == INV_B == DIM_L ** 4,
      '两种自洽约定的不变体积元都为 L^4')

# 被积结构（不变量）的量纲：g^{mu nu} nabla_mu kappa nabla_nu kappa
D_contraction = D_grad_kappa ** 2                       # L^-4
K_TARGET_A = D_action / (INV_A * D_contraction)         # = M L^2 T^-1 = [hbar]
K_TARGET_B = D_edens / D_contraction                    # = M L^3 T^-2 = [hbar c]
guard('G2-target-A-is-hbar', K_TARGET_A == D_hbar,
      '不变测度下要求的系数量纲 = [hbar]')
guard('G3-target-B-is-hbar-c', K_TARGET_B == D_hbar * D_c,
      '名义静态约定下要求的系数量纲 = [hbar c]')

# 来料 §1 表同时声明：sqrt(-g) 无量纲 且 d^4x = L^3 T
CLAIM_sqrtg = DIM_1
CLAIM_d4x = DIM_L ** 3 * DIM_T
MI('I01', '★来料 §1 表的 (sqrt(-g), d^4x) 配对不是任何一条自洽实现',
   '来料表申明 `[sqrt(-g)]` 无量纲、同时 `[d^4x] = L^3 T`。机器枚举两条自洽实现：'
   '(A) `x^0 = ct` 约定：`[sqrt(-g)]=1`、`[d^4x]=L^4`；'
   '(B) `x^0 = t` 约定：`g_00=-c^2` ⇒ `[sqrt(-g)]=L T^-1`、`[d^4x]=L^3 T`。'
   '两者的不变体积元都是 `L^4`（guard G1 机器核），'
   '⇒ **要么 `[d^4x]=L^4`（来料的 `L^3 T` 错），要么 `[sqrt(-g)]=L T^-1`（来料的「无量纲」错）**，'
   '二者不可同时成立。来料正是踩在这第三条「名义混合约定」上，'
   '其「被积函数必须是 `J/m^3`」这条要求也随之只在静态扇区可读（见 I03）。'
   '注：这不影响 r61 T01–T09 的结论（r61 已显式声明沿用该名义约定），'
   '本册补的是「该约定本身需要辨认」。',
   'INV_A=%s INV_B=%s 来料配对=%s x %s = %s'
   % (dstr(INV_A), dstr(INV_B), dstr(CLAIM_sqrtg), dstr(CLAIM_d4x),
      dstr(CLAIM_sqrtg * CLAIM_d4x)))

FA('I02', '★按不变四体积测度，正确系数量纲是 [hbar]，而非 ħc、更非 ħc/l_0^2',
   '机器核：`[g^{mu nu} nabla_mu kappa nabla_nu kappa] = %s`（不变量，两种约定同值），'
   '`[sqrt(-g) d^4x] = %s`（不变量），⇒ `[K] = [S] / (L^4 · L^-4) = [S] = %s = [hbar]`。'
   '由此三重课：'
   '(i) 原系数 `hbar/(2c)` = `%s` 缺的是 **`c`**（`[hbar]/[hbar/c] = c`），不是来料声称的 `s^-2`；'
   '(ii) 在名义静态约定下所需的是 `%s = [hbar c]`（r61 T04/T06 的口径），与(i) 恰差一个隐藏的 `c`；'
   '(iii) **两种约定下 `l_0` 的指数都被强制为 0**（见 I04 穷举），'
   '⇒ 来料 §3.1 的 `K_kin = hbar c / l_0^2` 在**任何**自洽约定下都不成立：'
   '它在约定(i) 下给出 `%s`，在约定(ii) 下给出 `%s`，两者都不对。'
   % (dstr(D_contraction), dstr(INV_A), dstr(K_TARGET_A),
      dstr(D_hbar / D_c), dstr(K_TARGET_B),
      dstr(D_hbar * D_c / D_l0 ** 2), dstr(D_hbar * D_c / D_l0 ** 2)),
   'K_target_A=%s K_target_B=%s 来料提案=%s'
   % (dstr(K_TARGET_A), dstr(K_TARGET_B), dstr(D_hbar * D_c / D_l0 ** 2)))

# 时间导数项在该名义约定下缺 c^2
D_timediff_piece = (1 / (DIM_L * DIM_T)) ** 2           # g^{00} 无量纲时的类时贡献
D_spatial_piece = D_grad_kappa ** 2                     # L^-4
RATIO_TS = D_timediff_piece / D_spatial_piece
BO('I03', '来料的名义约定只在 ∂_t kappa = 0 的静态扇区自洽（缺的那个因子恰是 c^2）',
   '在 `[sqrt(-g)]=1` 的名义约定下，度规分量无量纲 ⇒ '
   '类时项 `[g^{00}(partial_t kappa)^2] = %s`，空间项 `[g^{ij}(partial_i kappa)^2] = %s`，'
   '两者之比 = `%s` = `c^2` ⇒ **方括号内的收缩本身不齐次**，'
   '除非 `partial_t kappa = 0`。这与来料 §7 的「时间稳态 `partial_t kappa = 0`」条件一致'
   '⇒ 它把自己的适用范围限定在静态扇区：一旦想给 kappa 加动力学（传播、Ringdown、初值演化），'
   '必须取 `g^{00} = -1/c^2`，此时 `sqrt(-g)` 携带 `c`、`[sqrt(-g) d^4x]` 回到 `L^4`，'
   '系数量纲要求随之回到 I02 的 `[hbar]`。'
   '⇒ **这是本册对 r61 的一条条件性补充：r61 式(1) 的 `hbar c/2` 只在静态口径下成立；'
   '若要升为动力学的作用量，须同时改系数为 `[hbar]` 量级或显式写出 `sqrt(-g)` 携带的 `c`。**'
   % (dstr(D_timediff_piece), dstr(D_spatial_piece), dstr(RATIO_TS)),
   'ratio_timediff_over_spatial=%s (=c^2)' % dstr(RATIO_TS))


# =============================================================================
# 组 B · l_0 排除定理（幂次穷举，机器唯一性）
# =============================================================================
def enum_dims(base, target, lo=-3, hi=3):
    """穷举 base 中各量的整数幂组合，返回命中 target 量纲的全部解"""
    n = len(base)
    sols = []
    rng = list(range(lo, hi + 1))

    def rec(i, exps):
        if i == n:
            d = DIM_1
            for k in range(n):
                d = d * base[k][1] ** exps[k]
            if d == target:
                sols.append((tuple(exps), d))
            return
        for e in rng:
            rec(i + 1, exps + [e])

    rec(0, [])
    return sols


BASE_HCL = [('hbar', D_hbar), ('c', D_c), ('l0', D_l0)]
BASE_HCGL = [('hbar', D_hbar), ('c', D_c), ('G', D_G), ('l0', D_l0)]
BASE_HCGLM = [('hbar', D_hbar), ('c', D_c), ('G', D_G), ('l0', D_l0),
              ('m', DIM_M)]

SOL_A1 = enum_dims(BASE_HCL, K_TARGET_A)
SOL_B1 = enum_dims(BASE_HCL, K_TARGET_B)
SOL_A2 = enum_dims(BASE_HCGL, K_TARGET_A)
SOL_B2 = enum_dims(BASE_HCGL, K_TARGET_B, -4, 4)   # 放宽到 ±4 以容纳 γ=-1（需 c^4）
SOL_B3 = enum_dims(BASE_HCGLM, K_TARGET_B)

guard('G4-unique-nol0-targetA', len(SOL_A1) == 1 and SOL_A1[0][0] == (1, 0, 0),
      'base{ħ,c,l0} 下 target=[ħ] 的解必须唯一且 l0 指数为 0')
guard('G5-unique-nol0-targetB', len(SOL_B1) == 1 and SOL_B1[0][0] == (1, 1, 0),
      'base{ħ,c,l0} 下 target=[ħc] 的解必须唯一且 l0 指数为 0')
guard('G6-family-with-G-nonempty', len(SOL_B2) > 1,
      '引入 G 后必须出现解族（否则 I05 的「l0 只能与 G 配对」不成立）')
_family_ok = True
for exps, _d in SOL_B2:
    a, b, g, delta = exps
    if not (a == 1 + g and b == 1 - 3 * g and delta == -2 * g):
        _family_ok = False
guard('G7-family-structure', _family_ok,
      '含 G 解族必须满足 alpha=1+gamma, beta=1-3gamma, delta=-2gamma')
guard('G8-base-dependence', len(SOL_B3) > len(SOL_B2),
      '加入质量维度后解数必须增加（基组依赖性，r59 教训）')

PA('I04', '★l_0 排除定理：在 {ħ, c, l_0} 基下的整数幂穷举中，l_0 的指数被强制为 0',
   '机器穷举（指数 ∈ [-3,3]，共 %d 组）：'
   '(1) target = `[hbar]`（不变测度口径）：唯一解 `%s`，即 `K ∝ ħ`，`l_0` 指数 = 0；'
   '(2) target = `[hbar c]`（名义静态口径）：唯一解 `%s`，即 `K ∝ ħc`，`l_0` 指数 = 0。'
   '⇒ **`l_0` 不是「可以引入」，而是「被引力/机电外度规拒绝」**：'
   '在只有 ħ、c 的框架里，没有任何合法方式让一个新长度进入作用量系数。'
   '这正是「修一个纯常数因子（c 或 c²）不该顺手塞入一个自由长度」的机器形式'
   '（等价于本库 r61 判据二「修正系数勿增尺度」的穷举强化版）。'
   % (7 ** 3, '·'.join('%s^%d' % (BASE_HCL[i][0], SOL_A1[0][0][i]) for i in range(3)),
      '·'.join('%s^%d' % (BASE_HCL[i][0], SOL_B1[0][0][i]) for i in range(3))),
   'sol_targetA=%s sol_targetB=%s'
   % (str(SOL_A1[0][0]), str(SOL_B1[0][0])))

# 含 G 的解族：验证 K = ħc·(l_P/l_0)^{2γ}
_family_rows = []
for exps, _d in SOL_B2:
    a, b, gg, delta = exps
    rebuilt = (D_hbar * D_c) * (((D_hbar * D_G / D_c ** 3) / D_l0 ** 2) ** (-gg))
    _rebuilt_check = (D_hbar ** a) * (D_c ** b) * (D_G ** gg) * (D_l0 ** delta)
    guard('G10-family-rebuild-%d' % gg, rebuilt == _rebuilt_check,
          'gamma=%d 的解必须等于 ħc·(l_P/l_0)^{2γ}' % gg)
    _family_rows.append({'exponents': 'hbar^%d c^%d G^%d l0^%d' % (a, b, gg, delta),
                         'gamma': gg})
_ratio_dim = ((D_hbar * D_G / D_c ** 3) / D_l0 ** 2)
guard('G9-planck-ratio-dimensionless', _ratio_dim == DIM_1,
      '(l_P/l_0)^2 必须无量纲（解族可用该比表达的前提）')

FA('I05', '★引入 G 后 l_0 只能以无量纲比 (l_P/l_0)^2 出现 ⇒ 它不是新物理尺度',
   '把 G 加入基组后（4 基 × 7 值 = %d 组穷举）target=`[hbar c]` 出现解族而非唯一解，'
   '机器核其结构恒为 `alpha = 1+gamma`、`beta = 1-3gamma`、`delta = -2gamma`，'
   '即全部解可写成 **`K = ħc · (l_P/l_0)^{2γ}`**（`l_P^2 = ħG/c^3`；`(l_P/l_0)^2` 无量纲，guard G9 核）。'
   '⇒ 三条结论：'
   '(i) `l_0` **不能单独**进入系数，必须与 `G` 同时引入并以比值出现；'
   '(ii) 由于比值是无量纲的，`K` 的物理内容仍是 `ħc`，`l_0` 只是把同一个系数换个写法'
   '（换参数不改任何观测量 ⇒ 零判别力，是本库「外部输入 + 零信息」的同型复发）；'
   '(iii) 若坚持 `l_0` 为普适常数，则等价地引入了一个额外的无量纲自由数 `(l_P/l_0)^2`'
   '⇒ **以「必须有一个长度尺度」为理由把它写进作用量，在机器意义上不成立**。'
   '另注：本册另加第 5 基（质量）后解数由 %d 增至 %d ⇒'
   '**穷举的「唯一性强度」依赖基组大小**（r59 已记的同型教训，本册独立复现）。'
   % (7 ** 4, len(SOL_B2), len(SOL_B3)),
   'family=%s | base{+m}: %d 组解' % (str([r['exponents'] for r in _family_rows]),
                                      len(SOL_B3)))
# =============================================================================
# 组 C · 落到方程层：来料「修正版场方程」的两处内伤
# =============================================================================
# 来料 §4.2 的最终作用量： S = (ħc/2l_0^2) ∫ [ g∂κ∂κ − U(κ) ]，
#                        U(κ) = κ^2/sin^2θ − ω^2/c^2   （势内没有 1/2，整体前有 1/2）
A_UNIT = F(1)                      # 代表无量纲因子 1/sin^2θ
U_COEFFS = {2: A_UNIT, 0: F(-1)}   # U = A κ^2 + const


def poly_deriv(coeffs):
    out = {}
    for pw, cf in coeffs.items():
        if pw == 0:
            continue
        out[pw - 1] = cf * pw
    return out


dU = poly_deriv(U_COEFFS)                     # dU/dκ = 2κ/sin^2θ
POT_COEFF = F(1, 2) * dU[1]                   # 拉氏整体 1/2 前因子进入 EL
guard('G11-potential-coeff-is-one', POT_COEFF == F(1),
      '自带 1/2 前因子下 EL 的势项系数必须是 1（而非 2）')

# 场方程两项的量纲是否可比
try:
    _dummy = D_lap_kappa + D_kappa              # L^-3 + L^-1
    _eq_ok = True
except TypeError:
    _eq_ok = False
guard('G12-eom-inhomogeneous-raises', not _eq_ok,
      '∇²κ (L^-3) 与 κ/sin²θ (L^-1) 相加必须抛 TypeError')

MI('I06', '来料内部不自洽：§4.3 的 ∇²κ+2κ/sin²θ=0 与 §7 的 ∇²κ+κ/sin²θ=0 互斥',
   '取其自带的作用量 `S = (ħc/2l_0^2)∫[g^{μν}∇_μκ∇_νκ − (κ^2/sin^2θ − ω^2/c^2)]` 做变分：'
   '势内**没有** 1/2，而整体前因子自带 1/2 ⇒ `dU/dκ = 2κ/sin^2θ`，'
   '乘以前因子 1/2 后 EL 的势项系数恰为 **1**（guard G11 机器核）'
   '⇒ 由其自身写出发，正确形式是 §7 的 `∇²κ + κ/sin²θ = 0`；'
   '**§4.3 的 `2κ/sin²θ` 多乘了 2**（漏掉了前因子 1/2）。'
   '两式相差的有效波数为 `√2` ⇒ 任何依赖该方程根值的定量结论'
   '（正是它 A 选项要算的自能谱）都会差一个 √2 因子，而来料两处并存、未声明取舍。',
   'dU/dκ=%s κ 系数；乘 1/2 前因子后 = %s（应为 1，非 2）'
   % (str(dU[1]), str(POT_COEFF)))

FA('I07', '该场方程在方程层即不齐次 ⇒ 不是「难解」，是「无解」',
   '机器直接做 Dim 加法：`[∇²κ] = %s`、`[κ/sin²θ] = %s`，'
   '两者比 = `%s` ⇒ 相加无定义（guard G12 由抛错硬捕获，非人工阅读判断）。'
   '根因仍是 r61 T05「方括号两项异族」，本册把它下沉到**方程层**：'
   '即便只要求「方程的两项可比」，来料的 `U`（一次形式，`%s`）也做不到——'
   '唯一可行的是把原来的**平方势除以 c^4**（r61 式(1)：`(1/c^4)(c^2κ^2/sin^2θ − ω^2)^2 = %s`，'
   '与梯度项 `%s` 同族）。⇒ 来料「改为一次形式」的提案在任何层面上都不成立。'
   % (dstr(D_lap_kappa), dstr(D_kappa), dstr(D_lap_kappa / D_kappa),
      dstr(D_kappa ** 2), dstr((D_c ** 2 * D_kappa ** 2) ** 2 / D_c ** 4),
      dstr(D_contraction)),
   '[∇²κ]=%s vs [κ]=%s ratio=%s'
   % (dstr(D_lap_kappa), dstr(D_kappa), dstr(D_lap_kappa / D_kappa)))


# =============================================================================
# 组 D · 解族变号：即便补上缺失的长度²，Helmholtz 型也不是 localization
# =============================================================================
def simpson(f, a, b, n=4000):
    h = (b - a) / float(n)
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        s += f(x) * (4 if i % 2 else 2)
    return s * h / 3.0


def k_harm(r):                       # 调和型 κ = A/r，取 A=1
    return 1.0 / r


def dk_harm(r):
    return -1.0 / (r * r)


def k_helm(r):                       # Helmholtz 型 κ = A sin(kr)/r，取 A=k=1
    import math
    return math.sin(r) / r


def dk_helm(r):
    import math
    return math.cos(r) / r - math.sin(r) / (r * r)


def energy(a, b, kk, dkk):
    import math
    return simpson(lambda r: 4.0 * math.pi * r * r * dkk(r) ** 2, a, b)


def energy_log(a, b, kk, dkk):
    """对数网格积分：用于 1/r^2 型在 UV 端强烈峰化的被积函数（线性网格会欠采样）"""
    import math
    ua = math.log(a)
    ub = math.log(b)
    h = (ub - ua) / float(4000)

    def g(u):
        r = math.exp(u)
        return 4.0 * math.pi * r * r * dkk(r) ** 2 * r     # f(r) dr = f(e^u) e^u du

    s = g(ua) + g(ub)
    for i in range(1, 4000):
        s += g(ua + i * h) * (4 if i % 2 else 2)
    return s * h / 3.0


IR_ROWS = []
for R in (10.0, 100.0, 1000.0):
    num = energy(1e-3, R, k_helm, dk_helm)
    IR_ROWS.append({'R': R, 'U_numeric': num,
                    'leading_2piR': 2.0 * 3.141592653589793 * R,
                    'ratio': num / (2.0 * 3.141592653589793 * R)})
IR_HARM = energy_log(1e-3, 1000.0, k_harm, dk_harm)
IR_HARM_ANALYTIC = 4.0 * 3.141592653589793 * (1.0 / 1e-3 - 1.0 / 1000.0)

guard('G13-harmonic-analytic',
      abs(IR_HARM - IR_HARM_ANALYTIC) / IR_HARM_ANALYTIC < 1e-6,
      '调和型自能数值必须与 4π(1/a−1/R) 一致（积分器自证）')
guard('G14-helmholtz-linear-growth',
      IR_ROWS[2]['U_numeric'] / IR_ROWS[0]['U_numeric'] > 50.0,
      'Helmholtz 型自能必须随 R 近线性增长（R 增 100 倍 ⇒ 积分增 ~100 倍）')
guard('G15-helmholtz-leading-order',
      abs(IR_ROWS[2]['ratio'] - 1.0) < 5e-3,
      'R=1000 时数值积分应逼近首项 2πR（相对偏差<0.5%）')

BO('I08', '换频关系的实际代价：即便人为补齐长度²，解族由「代数衰减」变为「振荡 + IR 线性发散」',
   '来料把自己的二次势改成一次势，动机是让 `[U]` 与 `[|∇κ|²]` 同族；'
   '机器显示它既没做到（I07），即便补齐缺的长度² 使其成 Helmholtz 型，'
   '也会把局域化结构彻底换掉：'
   '(i) 调和型（`∇²κ=0`，原 ∇²κ 求解得的疏解 `κ=A/r`）自能 '
   '`U = 4πK∫ r²(∂_rκ)²dr = 4πKA²(1/a − 1/R)` ⇒ **∞ 端收敛，只在 UV 端 `a→0` 发散**（数值 %s vs 解析 %s，符合到 1e-6）；'
   '(ii) Helmholtz 型（`κ=A sin(kr)/r`）自能近道部 `%s`，数值积分随域长近线性增长：'
   'R=10 → %s、R=100 → %s、R=1000 → %s（首项 `2πA²k²R`；'
   '对比调和型的 `1/r` 衰减，多出的 `k²cos²/r²` 项在体积元 `r²dr` 下给出 `∝R`）'
   '⇒ **自能 IR 发散**，局域化与有限自能不可兼得。'
   '⇒ **这已经是来料 A 选项不可推进的第二重原因**（第一重是 r61 T04 的系数量纲错）：'
   '即使量纲修对，它要的自能谱也是发散的，须再引入一个域长/截断 ⇒ 又回到「需要一个长度」，'
   '但那必须是 **截断**而非「系数」，见 I09 的机器定价。'
   % ('%.6E' % IR_HARM, '%.6E' % IR_HARM_ANALYTIC,
      '2πA²k²R', '%.6E' % IR_ROWS[0]['U_numeric'],
      '%.6E' % IR_ROWS[1]['U_numeric'], '%.6E' % IR_ROWS[2]['U_numeric']),
   '调和型=%s (解析 %s) | Helmholtz R=10/100/1000 → %s / %s / %s'
   % ('%.6E' % IR_HARM, '%.6E' % IR_HARM_ANALYTIC,
      '%.6E' % IR_ROWS[0]['U_numeric'], '%.6E' % IR_ROWS[1]['U_numeric'],
      '%.6E' % IR_ROWS[2]['U_numeric']))
# =============================================================================
# 组 E · 自能-截断定理：即便修好量纲，l_0 也只能是「截断」且必然物种依赖
# =============================================================================
HBAR_C = hbar * c
C4_OVER_G = c ** 4 / G
C4_OVER_8PIG = c ** 4 / (Decimal(8) * PI * G)
K_LP = HBAR_C / (lP * lP)                      # = c^4/G（恒等式）
FOURPI = Decimal(4) * PI

LAMBDA_C = {'e': hbar / (M_E * c), 'mu': hbar / (M_MU * c), 'tau': hbar / (M_TAU * c)}
L_REQ = dict((k, v / FOURPI) for k, v in LAMBDA_C.items())      # 令 U_self/(mc^2)=1 的截断
REL_AT_LP = dict((k, FOURPI * lP / v) for k, v in LAMBDA_C.items())
K_COMPTON_E = HBAR_C / (LAMBDA_C['e'] ** 2)
K_COMPTON_MU = HBAR_C / (LAMBDA_C['mu'] ** 2)
LEVERAGE = K_LP / K_COMPTON_E

guard('G16-lplanck-literal', abs(lP - LP_LIT) / LP_LIT < Decimal('1e-6'),
      '自算普朗克长必须与字面值 1.616255e-35 一致（截断常数自证）')
guard('G17-k-lp-identity', abs(K_LP - C4_OVER_G) / C4_OVER_G < Decimal('1e-40'),
      'ħc/l_P^2 必须逐位等于 c^4/G（解析恒等式）')
guard('G18-cutoff-tracks-inverse-mass',
      abs(L_REQ['e'] / L_REQ['tau'] - M_TAU / M_E) / (M_TAU / M_E) < Decimal('1e-20'),
      '所需截断之比必须等于质量比（物种依赖的机器表达）')
guard('G19-planck-cutoff-negligible',
      max(REL_AT_LP.values()) < Decimal('1e-15'),
      '普朗克截断下的相对自能必须 < 1e-15（否则「自能屏蔽」仍有戏）')
guard('G20-leverage-huge', LEVERAGE > Decimal('1e40'),
      '不同 l_0 候选的系数杠杆必须 > 40 个量级')

FA('I09', '★自能-截断定理：把 l_0 当普适长度，在数量级上就否证了「自能屏蔽」路线',
   '取来料 §4.4 的自能 `U_self = K ∫d^3x |∇κ|^2`，并以自然剖面 `κ(r)=κ_0 ℓ/r (r≥ℓ)` 代入：'
   '`U_self = 4πK κ_0^2 ℓ`。再由**来料自己的 §7**（`E = ħcκ_0/sinθ` 与 `E=mc^2`）得 `κ_0 = mc sinθ/ħ` ⇒'
   '**`U_self/(mc^2) = 4π sin^2θ · (ℓ/ƛ_C)`**（`ƛ_C = ħ/(mc)`）。机器读数（取 `sinθ=1`）：'
   '(i) 要让自能起到 O(1) 作用，所需截断为 `ℓ = ƛ_C/4π`：电子 `%s` m、缪子 `%s` m、tau `%s` m；'
   '三者之比 = `%s`，**恰等于 `m_τ/m_e`（guard G18）** ⇒ 截断必须**逐物种**取值，不是普适常数；'
   '(ii) 反过来，若坚持 `ℓ = l_P`（来料 §6 的第一候选），则相对自能分别为 '
   '电子 `%s`、缪子 `%s`、tau `%s` ⇒ **全部 < 1e-15（guard G19）**，'
   '自能对质量账的贡献完全可忽略，「屏蔽/重构质量」没有可观察后果；'
   '(iii) 这正是 `l_0` **唯一合法**的角色（UV 截断），但它带来的是 `U_self ∝ ℓ` 的线性自由，'
   '——不是一个可以由量纲推出的系数。⇒ 来料 §6 把 `l_0` 写进**系数**是双误：'
   '量纲上被排除（I04），物理上即便当截断用也既不能普适、又不能预言。'
   % (fv(L_REQ['e'], 6), fv(L_REQ['mu'], 6), fv(L_REQ['tau'], 6),
      fv(L_REQ['e'] / L_REQ['tau'], 6),
      fv(REL_AT_LP['e'], 6), fv(REL_AT_LP['mu'], 6), fv(REL_AT_LP['tau'], 6)),
   'ℓ_req: e=%s mu=%s tau=%s m | U/(mc^2)@l_P: %s / %s / %s | leverage=%s'
   % (fv(L_REQ['e'], 6), fv(L_REQ['mu'], 6), fv(L_REQ['tau'], 6),
      fv(REL_AT_LP['e'], 6), fv(REL_AT_LP['mu'], 6), fv(REL_AT_LP['tau'], 6),
      fv(LEVERAGE, 6)))

IN('I10', 'l_0 三候选的机器定价：系数在候选之间摆动约 45 个量级',
   '来料 §6 列了三个候选，机器给它们的系数（静态口径 `ħc/l_0^2`）在同一作用量下摆动 `%s` 个量级：'
   '`l_0=l_P` ⇒ `%s` N（**逐位等于 `c^4/G`，与 r18/r22/r27 跨册登记的 `%s` 同源，本册独立复算**；'
   '同族另一口径 `c^4/(8πG) = %s`）；'
   '`l_0=ƛ_C(e)` ⇒ `%s` N；`l_0=ƛ_C(μ)` ⇒ `%s` N。'
   '极值比 = `%s`（guard G20）⇒ **在 l_0 未定之前，该作用量的任何数值结论可摆动 45 个量级**，'
   '这正是「未声明外部输入」的量化账单，也是本册对 r61 C4/r42 的一个数值补充：'
   '不是「引入 l_0 撞 Ω5」这么抽象，而是**撞出 45 个量级的自由**。'
   % (fv(LEVERAGE.ln() / Decimal(10).ln(), 3), fv(K_LP, 16),
      fv(C4_OVER_G, 16), fv(C4_OVER_8PIG, 16),
      fv(K_COMPTON_E, 8), fv(K_COMPTON_MU, 8), fv(LEVERAGE, 6)),
   'K(l_P)=%s N | K(Compton_e)=%s N | c^4/(8πG)=%s'
   % (fv(K_LP, 10), fv(K_COMPTON_E, 10), fv(C4_OVER_8PIG, 16)))

# 来料 A 选项 m(κ)=ακ−Cκ^{8/3} 的系数量纲
D_alpha = DIM_M / D_kappa                                   # M L
D_Ccoef = DIM_M / (D_kappa ** F(8, 3))                      # M L^{8/3}
SOL_C = enum_dims(BASE_HCL, D_Ccoef)
D_C_rebuild = D_hbar * (D_c ** -1) * (D_l0 ** F(5, 3))
guard('G21-C-requires-fractional-l0', len(SOL_C) == 0 and D_C_rebuild == D_Ccoef,
      '{ħ,c,l0} 整幂穷举对 [C]=M L^{8/3} 必须 0 命中，且需 l_0^{5/3} 分数幂')

BO('I11', '来料 A 选项的结构提示：κ^{8/3} 项的系数需要 l_0 的 5/3 次幂（分数幂）',
   '由 `m(κ)=ακ−Cκ^{8/3}` 反解：`[α] = %s`、`[C] = %s`。'
   '机器在基 `{ħ, c, l_0}` 上做整幂穷举（7^3=343 组）对该量纲 **命中 0 组**（guard G21）；'
   '解析上唯一解为 `ħ^1 c^-1 l_0^{5/3}`（机器验证 `%s`）。'
   '⇒ 一个 **5/3 次的分数幂长度**不可能来自局域解析势的泰勒展开（那里只出整数幂），'
   '只能来自非局域/积分掉的中间尺度（如 I08 的截断积分）。'
   '附加一条对 A 选项的不利读数：在公理1 下 `κ ∝ m`，'
   '故 `m = ακ − Cκ^{8/3}` 实际是关于 `m` 的**隐式方程**，'
   '而非「由 κ 预测 m」的显式公式——除非 α、C 先被外部给定（≥2 个新常数）。'
   % (dstr(D_alpha), dstr(D_Ccoef), dstr(D_C_rebuild)),
   'sol_count=%d | rebuild=%s' % (len(SOL_C), dstr(D_C_rebuild)))
# =============================================================================
# 组 F · 对 r61 的独立复核（只承接，不重复裁定）+ 来料的笔误级读数
# =============================================================================
ORIG_KINETIC = (D_hbar / D_c) * D_contraction          # 原动能项
GAP_REAL = D_edens / ORIG_KINETIC                      # 真实缺口
FIXED_KINETIC = (D_hbar * D_c / D_l0 ** 2) * D_contraction
guard('G22-gap-is-c2', GAP_REAL == D_c ** 2, '缺口必须恰为 c^2')
guard('G23-original-kinetic', ORIG_KINETIC == DIM_M / DIM_L ** 3,
      '[ħ/(2c)|∇κ|^2] 必须为 M L^-3')
guard('G24-fix-still-wrong', FIXED_KINETIC == DIM_M / (DIM_L ** 3 * DIM_T ** 2),
      '来料修正后必须为 M L^-3 T^-2（仍差 L^2）')

PA('I12', '独立引擎复现 r61 的四条核心量纲读数（仅承接，本册不重复裁定）',
   '本册用独立实现的量纲引擎（指数相加的 `Dim` 类 + 异族抛错）复算 r61 T01/T02/T04/T05：'
   '`[ħ/(2c)·|∇κ|^2] = %s` ✓（r61 T01）；'
   '对能量密度 `%s` 的真实缺口 = `%s`（**是 `c^2` 不是 `s^-2`**）✓（r61 T02）；'
   '`[ħc/l_0^2·|∇κ|^2] = %s`，仍差 `%s` ✓（r61 T04）；'
   '方括号 `[|∇κ|^2]=%s` 与 `[κ^2/sin^2θ−ω^2/c^2]=%s` 异族 ⇒ Dim 加法直接抛错 ✓（r61 T05）。'
   '⇒ **四条全部复现，本册不改动 r61 任何结论**；本册新增的是 r61 未涉及的'
   '测度口径（I01–I03）、l_0 排除定理（I04–I05）、方程层内伤（I06–I07）、'
   '解族与自能定价（I08–I11）。'
   % (dstr(ORIG_KINETIC), dstr(D_edens), dstr(GAP_REAL), dstr(FIXED_KINETIC),
      dstr(D_edens / FIXED_KINETIC), dstr(D_contraction), dstr(D_kappa ** 2)),
   'gap=%s | fixed=%s' % (dstr(GAP_REAL), dstr(FIXED_KINETIC)))

D_claim_jperm2 = D_energy / DIM_L ** 2               # J/m^2 = M T^-2
IN('I13', '来料 §3.1 的单位标注笔误：`[K_kin]` 被写成 [J/m^2]，实为 N（差一个长度）',
   '来料写「`[K_kin] = [kg·m·s^-2] = [J/m^2]`」。机器核：'
   '`kg·m·s^-2 = %s`（牛顿），而 `J/m^2 = %s` ⇒ 两者差 `%s`。'
   '数值部分（`kg·m·s^-2`）对、等号右侧的标签错。'
   '这是与主错（|∇κ|^2 少用一次 `m^-2`）**同型的小型复发**——'
   '同一页内两次长度幂次记账失误，可作为「量纲类断言必须机器兑底」的又一实例登记。'
   % (dstr(D_force), dstr(D_claim_jperm2), dstr(D_force / D_claim_jperm2)),
   'N=%s vs J/m^2=%s ratio=%s'
   % (dstr(D_force), dstr(D_claim_jperm2), dstr(D_force / D_claim_jperm2)))


# =============================================================================
# 主程序
# =============================================================================
def main():
    tally = {}
    for it in ITEMS:
        tally[it['verdict']] = tally.get(it['verdict'], 0) + 1
    order = ['PASS', 'FAIL', 'CORRECTED', 'MISMATCH', 'BOUNDARY', 'INFO']
    tt = ' / '.join('%s=%d' % (k, tally.get(k, 0)) for k in order if k in tally)

    guard('G25-item-count', len(ITEMS) == 13, '条目数必须为 13（I01–I13）')

    CONV_ROWS = [
        {'branch': 'A · 协变 (x^0=ct)', 'sqrtg': dstr(D_sqrtg_A),
         'd4x': dstr(D_d4x_A), 'volume': dstr(INV_A),
         'K_required': dstr(K_TARGET_A), 'note': '= [ħ]'},
        {'branch': 'B · x^0=t + g_00=-c^2', 'sqrtg': dstr(D_sqrtg_B),
         'd4x': dstr(D_d4x_B), 'volume': dstr(INV_B),
         'K_required': dstr(K_TARGET_A), 'note': '= [ħ]（不变测度同一答案）'},
        {'branch': 'C · 名义混合（来料 §1 表）', 'sqrtg': dstr(CLAIM_sqrtg),
         'd4x': dstr(CLAIM_d4x), 'volume': dstr(CLAIM_sqrtg * CLAIM_d4x),
         'K_required': dstr(K_TARGET_B), 'note': '= [ħc]；仅 ∂_tκ=0 自洽'},
    ]
    CUT_ROWS = []
    for k in ('e', 'mu', 'tau'):
        CUT_ROWS.append({'particle': k,
                         'compton_m': fv(LAMBDA_C[k], 8),
                         'ell_required_m': fv(L_REQ[k], 8),
                         'U_over_mc2_at_lP': fv(REL_AT_LP[k], 6)})

    evidence = {
        'dim_target_A_invariant': dstr(K_TARGET_A),
        'dim_target_B_nominal': dstr(K_TARGET_B),
        'dim_original_kinetic': dstr(ORIG_KINETIC),
        'gap_real': dstr(GAP_REAL),
        'dim_incoming_fix': dstr(FIXED_KINETIC),
        'enum_targetA_base_hcl': str(SOL_A1[0][0]),
        'enum_targetB_base_hcl': str(SOL_B1[0][0]),
        'enum_family_with_G': str([r['exponents'] for r in _family_rows]),
        'enum_count_with_mass': len(SOL_B3),
        'potential_el_coefficient': str(POT_COEFF),
        'helmholtz_U_R10_R100_R1000': [r['U_numeric'] for r in IR_ROWS],
        'harmonic_U': IR_HARM,
        'ell_required_m': dict((k, fv(v, 8)) for k, v in L_REQ.items()),
        'U_over_mc2_at_lP': dict((k, fv(v, 6)) for k, v in REL_AT_LP.items()),
        'K_lP_N': fv(K_LP, 16),
        'K_compton_e_N': fv(K_COMPTON_E, 10),
        'c4_over_G': fv(C4_OVER_G, 16),
        'c4_over_8piG': fv(C4_OVER_8PIG, 16),
        'leverage_orders': fv(LEVERAGE.ln() / Decimal(10).ln(), 3),
        'guards': GUARD,
        'guards_total': len(GUARD),
        'guards_passed': len([g for g in GUARD if g['ok']]),
    }
    summary = {
        'book': NAME, 'date': '2026-10-15',
        'layer': 'r73 = V4.8 量纲核验报告的口径补全 + l_0 排除定理（承接 r61，零重复裁定）',
        'judgment_book': '判定_TUFT-r73-V48量纲核验报告口径补全与l0排除定理_2026-10-15.md',
        'item_count': len(ITEMS),
        'tally': dict((k, tally.get(k, 0)) for k in order), 'tally_text': tt,
        'guards_total': len(GUARD),
        'guards_passed': len([g for g in GUARD if g['ok']]),
        'items': ITEMS, 'evidence': evidence,
    }

    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    with io.open(os.path.join(OUT, NAME + '.json'), 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(summary, ensure_ascii=False, indent=2))

    L = ['# %s' % NAME, '', '- 日期：2026-10-15',
         '- 承接：r61（同一份来料的一次自审）—— 补口径层与数值层，不重复裁定', '',
         '## 汇总', '', '条目 %d（%s）· 守卫 %d/%d'
         % (len(ITEMS), tt, len([g for g in GUARD if g['ok']]), len(GUARD)), '',
         '## 守卫', '', '| 守卫 | 结果 | 说明 |', '|---|---|---|']
    for g in GUARD:
        L.append('| %s | %s | %s |' % (g['guard'], 'PASS' if g['ok'] else 'FAIL', g['note']))
    L += ['', '## 测度约定表', '',
          '| 分支 | [sqrt(-g)] | [d^4x] | 体积元 | 要求的 [K] | 备注 |',
          '|---|---|---|---|---|---|']
    for r in CONV_ROWS:
        L.append('| %s | %s | %s | %s | %s | %s |'
                 % (r['branch'], r['sqrtg'], r['d4x'], r['volume'],
                    r['K_required'], r['note']))
    L += ['', '## 自能-截断表（sinθ=1）', '',
          '| 粒子 | 约化康普顿波长 (m) | 令 U/(mc^2)=1 的截断 ℓ (m) | ℓ=l_P 时 U/(mc^2) |',
          '|---|---|---|---|']
    for r in CUT_ROWS:
        L.append('| %s | %s | %s | %s |'
                 % (r['particle'], r['compton_m'], r['ell_required_m'],
                    r['U_over_mc2_at_lP']))
    L += ['', '## 条目', '']
    for it in ITEMS:
        L.append('### %s · %s · %s' % (it['code'], it['verdict'], it['title']))
        L.append('')
        L.append(it['detail'])
        L.append('')
        if it['evidence']:
            L.append('- 机器读数：`%s`' % it['evidence'])
            L.append('')
    with io.open(os.path.join(OUT, NAME + '.md'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(L) + '\n')

    R = ['=' * 74, NAME, '2026-10-15', '=' * 74,
         '条目 %d   %s' % (len(ITEMS), tt),
         '守卫 %d / %d' % (len([g for g in GUARD if g['ok']]), len(GUARD)), '']
    for g in GUARD:
        R.append('[%s] %-32s %s' % ('PASS' if g['ok'] else 'FAIL', g['guard'], g['note']))
    R.append('')
    for it in ITEMS:
        R.append('[%s] %s  %s' % (it['verdict'], it['code'], it['title']))
        R.append('       %s' % it['detail'][:300])
        if it['evidence']:
            R.append('       机器: %s' % it['evidence'][:200])
        R.append('')
    R.append('-' * 74)
    R.append('自能-截断表')
    for r in CUT_ROWS:
        R.append('  %-4s compton=%s  ell_req=%s  U/(mc^2)@lP=%s'
                 % (r['particle'], r['compton_m'], r['ell_required_m'],
                    r['U_over_mc2_at_lP']))
    with io.open(os.path.join(OUT, NAME + '_report.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(R) + '\n')

    print('=' * 74)
    print(NAME)
    print('条目 %d   %s' % (len(ITEMS), tt))
    print('守卫 %d / %d' % (len([g for g in GUARD if g['ok']]), len(GUARD)))
    print('=' * 74)
    print('K_target(不变测度) = %s   K_target(名义静态) = %s'
          % (dstr(K_TARGET_A), dstr(K_TARGET_B)))
    print('gap(真实) = %s   l_0 指数穷举 targetA=%s targetB=%s'
          % (dstr(GAP_REAL), str(SOL_A1[0][0]), str(SOL_B1[0][0])))
    print('K(l_P)=%s N   K(Compton_e)=%s N   杠杆=%s 量级'
          % (fv(K_LP, 10), fv(K_COMPTON_E, 10),
             fv(LEVERAGE.ln() / Decimal(10).ln(), 3)))
    print('ell_req: e=%s  mu=%s  tau=%s'
          % (fv(L_REQ['e'], 6), fv(L_REQ['mu'], 6), fv(L_REQ['tau'], 6)))
    print('U/(mc^2)@lP: %s / %s / %s'
          % (fv(REL_AT_LP['e'], 4), fv(REL_AT_LP['mu'], 4), fv(REL_AT_LP['tau'], 4)))
    print('=' * 74)
    for g in GUARD:
        if not g['ok']:
            print('GUARD FAIL: %s -- %s' % (g['guard'], g['note']))
    return 0 if all(g['ok'] for g in GUARD) else 1


if __name__ == '__main__':
    sys.exit(main())
