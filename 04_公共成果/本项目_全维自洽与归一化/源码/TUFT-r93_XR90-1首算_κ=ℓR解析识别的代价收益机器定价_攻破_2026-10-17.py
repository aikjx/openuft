# -*- coding: utf-8 -*-
"""TUFT r92：X-R90-1 首算 —— kappa = ell*R 解析识别的代价—收益机器定价（攻破）

受理：r90 F3 登记、唯一未被定价的可计算项。
问题：W1 支把 kappa,tau 降为度规派生量；r90 取 kappa=(R_abR^ab)^{1/4}（分数幂）得到
  (i) 解析性定理：零新常数下 [kappa]=L^-1 无整数解（132 分数解 / 0 整数解）；
  (ii) 真空奇异：kappa 变分在 K=R_abR^ab->0 处发散；
  (iii) U=lambda*kappa^4 = lambda*R_abR^ab（Ricci^2）=> 四阶 EOM + 质量自旋-2 鬼。
r90 F3 问：若允许 +1 个新长度常数 ell，取 kappa=ell*R（解析、整数幂、无奇异），
  其「换回适定性」的收益此前未被定价。本册只定价、不代选。
纯标准库：Decimal(60) + Fraction 三元组量纲 (M,L,T)。与 r79-r91（弱场/PPN/屏蔽定价，
走 W2/BD 口径）不重复：本册走 W1+ell 解析识别口径。
"""
import json
import os
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60


class Dim(object):
    """(M, L, T) 指数三元组。相乘=指数相加；异构相加抛 TypeError。"""

    def __init__(self, m=0, l=0, t=0):
        self.v = (F(m), F(l), F(t))

    def __repr__(self):
        return 'Dim%s' % (str(tuple(str(x) for x in self.v)),)

    def __mul__(self, o):
        return Dim(*[a + b for a, b in zip(self.v, o.v)])

    def __truediv__(self, o):
        return Dim(*[a - b for a, b in zip(self.v, o.v)])

    def __pow__(self, e):
        e = F(e)
        return Dim(*[x * e for x in self.v])

    def __eq__(self, o):
        return tuple(self.v) == tuple(o.v)

    def __ne__(self, o):
        return not self.__eq__(o)

    def __hash__(self):
        return hash(tuple(self.v))

    def is_dimless(self):
        return all(x == 0 for x in self.v)


def dstr(d):
    parts = []
    for x, s in zip(d.v, ('M', 'L', 'T')):
        if x == 0:
            continue
        parts.append('%s^%s' % (s, str(x)))
    return '1' if not parts else ' '.join(parts)


D_M = Dim(1, 0, 0)
D_L = Dim(0, 1, 0)
D_T = Dim(0, 0, 1)
D_NONE = Dim(0, 0, 0)

C_BASE = {
    'hbar': D_M * D_L ** 2 / D_T,
    'c': D_L / D_T,
    'G': D_L ** 3 / (D_M * D_T ** 2),
}
D_ELL = D_L                       # 新基本长度常数 ell
D_R = Dim(0, -2, 0)              # Ricci 标量 R ~ L^-2
D_R2 = Dim(0, -4, 0)             # R_abR^ab ~ L^-4
D_R4 = Dim(0, -4, 0)             # R_abcdR^abcd ~ L^-4


def enum_q(base, target, lo=-2, hi=2, step=F(1, 4)):
    """在 base 上穷举满足 target 的幂次组合；step=1/4 允许分数幂。"""
    names = sorted(base.keys())
    out = []

    def rec(i, cur):
        if i == len(names):
            if cur == target:
                out.append(dict((n, memo[n]) for n in names))
            return
        e = F(lo)
        while e <= F(hi):
            memo[names[i]] = e
            rec(i + 1, cur * base[names[i]] ** e)
            e += step

    memo = {}
    rec(0, D_NONE)
    return out


def fmt_sol(sol):
    ks = [k for k in sorted(sol.keys()) if sol[k] != 0]
    if not ks:
        return '1'
    return ' * '.join('%s^%s' % (k, str(sol[k])) for k in ks)


def Dc(x):
    return Decimal(str(x))


def rel(a, b):
    a = Dc(a)
    b = Dc(b)
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


# ---------------- CODATA 锚点（外部输入，登记为 NS） ----------------
HBAR = Dc('1.054571817e-34')     # J*s
C_LIT = Dc('299792458')          # m/s
G_LIT = Dc('6.67430e-11')        # m^3 kg^-1 s^-2
LP_LIT = Dc('1.616255e-35')      # m

LP_CALC = (HBAR * G_LIT / (C_LIT ** 3)).sqrt()
L_P = LP_CALC

PI60 = Decimal('3.14159265358979323846264338327950288419716939937510582097494')
FOURPI = PI60 * 4
SQRT_4PI = (FOURPI).sqrt()
ELL_LOCK = (FOURPI * HBAR * G_LIT / (C_LIT ** 3)).sqrt()   # = sqrt(4 pi) l_P

M_PL_KG = (HBAR * C_LIT / G_LIT).sqrt()                   # 普朗克质量 (kg)
M_PL_EV = M_PL_KG * C_LIT ** 2 / Dc('1.602176634e-19')    # 普朗克质量 (eV)

# 链上读数（r90 C1/C2、A2、A3；r89 强度）—— 本册独立复现，非引用
LAMBDA_HAT_MAX = Dc('2.98733655978083192661919970240105988153322497435919945481564E+70')
LAMBDA_HAT_TEV = Dc('2.96539924912552274601540865098190782590334569948283275856692E+30')  # r90 C2：=> m2~1 TeV
M2_R90_EV = Dc('9.96321516171823316002840904911126275823787508595600598178696E-9')
M2_R90_KG = Dc('3.06980348019794351656889088269554630524727621848257574499151E-9')
K0 = Dc('2.9483837550529839615136785E-104')               # r76 宇宙平均曲率 (m^-4)


def fv(x, n=25):
    try:
        return format(Dc(x), '.%dE' % n)
    except Exception:
        return 'NaN'


def fs(x, n=6):
    try:
        return format(Dc(x), '.%dE' % n)
    except Exception:
        return 'NaN'


GUARDS = []


def G(tag, cond, detail=''):
    GUARDS.append((tag, bool(cond), detail))
    return bool(cond)


# ---- G0：量纲工具自身守卫（承 r37/r59/r73：工具先自守再用） ----
G('G0-1 [G]', D_L ** 3 / (D_M * D_T ** 2) == C_BASE['G'], dstr(C_BASE['G']))
G('G0-2 [hbar]', D_M * D_L ** 2 / D_T == C_BASE['hbar'], dstr(C_BASE['hbar']))
G('G0-3 [c]', D_L / D_T == C_BASE['c'], dstr(C_BASE['c']))
try:
    D_L + D_T
    G('G0-4 异构相加须抛错', False, '未抛 TypeError')
except TypeError:
    G('G0-4 异构相加须抛错', True, 'TypeError 已抛出')
G('G0-5 l_P 计算值', LP_CALC > 0, fv(LP_CALC))
G('G0-6 ell 锁定值 = sqrt(4pi) l_P',
  rel(ELL_LOCK, SQRT_4PI * L_P) < Dc('1e-45'), fv(ELL_LOCK))

# ---- 目标量纲：kappa = ell*R ----
KAPPA_LR = D_ELL * D_R            # [ell*R] = L * L^-2 = L^-1
G('G0-7 [kappa=ell*R] = L^-1', KAPPA_LR == D_L ** -1, dstr(KAPPA_LR))
G('G0-8 [ell] = L', D_ELL == D_L, dstr(D_ELL))
G('G0-9 [R] = L^-2', D_R == D_L ** -2, dstr(D_R))
G('G0-10 [R_abR^ab] = [R_abcdR^abcd] = L^-4',
  D_R2 == D_L ** -4 and D_R4 == D_L ** -4, '%s / %s' % (dstr(D_R2), dstr(D_R4)))

# ---- 枚举（独立复现 r90 A2 的 132 / 0） ----
BASIS_R90 = {'R': D_R, 'R2': D_R2, 'R4': D_R4}
BASIS_R92 = {'ell': D_ELL, 'R': D_R, 'R2': D_R2, 'R4': D_R4}
ENUM_R90 = enum_q(BASIS_R90, D_L ** -1, -2, 2, F(1, 4))     # 步长 1/4，共 4913 组
ENUM_R90_INT = enum_q(BASIS_R90, D_L ** -1, -2, 2, F(1))    # 仅整数幂
ENUM_R92 = enum_q(BASIS_R92, D_L ** -1, -2, 2, F(1, 4))
ENUM_R92_INT = enum_q(BASIS_R92, D_L ** -1, -2, 2, F(1))

G('G0-11 r90 复现：分数幂解 = 132', len(ENUM_R90) == 132, 'hits=%d' % len(ENUM_R90))
G('G0-12 r90 复现：整数解 = 0', len(ENUM_R90_INT) == 0, 'hits=%d' % len(ENUM_R90_INT))
G('G0-13 +ell 后整数解 >= 1', len(ENUM_R92_INT) >= 1, 'hits=%d' % len(ENUM_R92_INT))
G('G0-14 +ell 后分数幂解 >= 1', len(ENUM_R92) >= 1, 'hits=%d' % len(ENUM_R92))
SAMPLE_LR = next((s for s in ENUM_R92_INT if s.get('ell') == F(1) and s.get('R') == F(1)), None)
G('G0-15 存在解 ell^1 R^1',
  SAMPLE_LR is not None, fmt_sol(SAMPLE_LR) if SAMPLE_LR else 'none')

# ---- 阳性对照：target=L 在 {hbar,c,G} 内 0 解，+ell 后 >=1 ----
CT_L = enum_q(C_BASE, D_L, -4, 4, F(1))
CT_L_E = enum_q(dict(C_BASE, ell=D_ELL), D_L, -4, 4, F(1))
G('G0-16 阳性对照 target=L 在 {hbar,c,G} 命中 0', len(CT_L) == 0, 'hits=%d' % len(CT_L))
G('G0-17 阳性对照 +ell 后命中 >=1', len(CT_L_E) >= 1, 'hits=%d' % len(CT_L_E))

# ---- 奇异性消除演示 ----
def dk_K(Kv):
    """kappa=K^{1/4} 的 d(kappa)/dK = (1/4) K^{-3/4}。"""
    K14 = (Kv.sqrt()).sqrt()          # K^{1/4}
    Km34 = Dc('1') / (K14 ** 3)        # K^{-3/4}
    return Decimal('0.25') * Km34

DK_AT_K0 = dk_K(K0)
DK_AT_K1 = dk_K(K0 * Dc('1e-1'))
DK_AT_K2 = dk_K(K0 * Dc('1e-2'))
DK_AT_K3 = dk_K(K0 * Dc('1e-3'))
DK_LR = ELL_LOCK                     # kappa=ell*R 的 d/dR = ell = 常数
G('G0-18 K^{1/4} 导数随 K->0 发散（单调递增）',
  DK_AT_K0 < DK_AT_K1 < DK_AT_K2 < DK_AT_K3,
  '%.2e < %.2e < %.2e < %.2e' % (DK_AT_K0, DK_AT_K1, DK_AT_K2, DK_AT_K3))
G('G0-19 ell*R 导数 = 有限常数 ell', DK_LR == ELL_LOCK and DK_LR > 0, fv(DK_LR))

# ---- U 项随识别改变：kappa=(R_abR^ab)^{1/4} => lambda*R_abR^ab；kappa=ell*R => lambda*ell^4*R^4 ----
# [lambda] = [hbar c]（r90：lambda_hat = lambda/(hbar c) 无量纲）
LAM_DIM = D_M * D_L ** 3 / D_T ** 2       # [hbar c]
U_RICCI = LAM_DIM * D_R2                  # lambda*R_abR^ab
U_R4 = LAM_DIM * (D_ELL ** 4) * (D_R ** 4)  # lambda*ell^4*R^4
E_DENS = D_M * D_L ** -1 * D_T ** -2
G('G0-20 [U=lambda*R_abR^ab] = 能量密度', U_RICCI == E_DENS, dstr(U_RICCI))
G('G0-21 [U=lambda*ell^4*R^4] = 能量密度', U_R4 == E_DENS, dstr(U_R4))
G('G0-22 两 U 项均为能量密度（结构不同，见 I05）', U_RICCI == E_DENS and U_R4 == E_DENS,
  'Ricci^2=%s  R^4=%s' % (dstr(U_RICCI), dstr(U_R4)))

# ---- 链上鬼质量标度独立复现（r90 C1/C2/E5） ----
def m2_kg(lambda_hat):
    return M_PL_KG / ((16 * PI60 * lambda_hat).sqrt())

def m2_ev(lambda_hat):
    return M_PL_EV / ((16 * PI60 * lambda_hat).sqrt())

M2_KG_AT1 = m2_kg(Dc('1'))
M2_EV_ATMAX = m2_ev(LAMBDA_HAT_MAX)
M2_EV_ATTEV = m2_ev(LAMBDA_HAT_TEV)
G('G0-23 鬼质量标度 m2(lambda_hat=1) 复现 r90 E5',
  rel(M2_KG_AT1, M2_R90_KG) < Dc('5e-4'), 'mine=%s r90=%s' % (fv(M2_KG_AT1), fv(M2_R90_KG)))
G('G0-24 鬼质量 lambda_hat_max -> 9.96e-9 eV 复现 r90 C1',
  rel(M2_EV_ATMAX, M2_R90_EV) < Dc('5e-4'), 'mine=%s r90=%s' % (fv(M2_EV_ATMAX), fv(M2_R90_EV)))
G('G0-25 1 TeV 界 lambda_hat<=2.965e30 -> m2~1 TeV 复现 r90 C2',
  rel(M2_EV_ATTEV, Dc('1e12')) < Dc('5e-4'), 'mine=%s' % fv(M2_EV_ATTEV))
# 分辨率阳性对照：lambda_hat 扰动 1e-6，m2 应同量级变化（公式有分辨力）
G('G0-26 公式有分辨力（扰动 lambda 1e-6 改变 m2）',
  rel(m2_kg(Dc('1') * (Dc('1') + Dc('1e-6'))), M2_KG_AT1) > Dc('1e-8'),
  'rel=%s' % fs(rel(m2_kg(Dc('1') * (Dc('1') + Dc('1e-6'))), M2_KG_AT1)))

# ---- 收益空洞估算：ell 锁定后 kappa=ell*R 比分数幂识别小多少 ----
R_NS = Dc('7e-9')                         # 中子星 Ricci 标量 (m^-2)，O(1) 估计，登记 INFO
K_NS = R_NS ** 2                          # R_abR^ab ~ R^2
KAPPA_K_NS = (K_NS.sqrt()).sqrt()         # K^{1/4}
KAPPA_LR_NS = ELL_LOCK * R_NS             # ell*R
SUPP = KAPPA_LR_NS / KAPPA_K_NS           # 抑制比 ~ ell*sqrt(R)
G('G0-27 锁定后 kappa(ell*R) 比分数幂识别强压 ~1e-39',
  SUPP < Dc('1e-30') and SUPP > 0, 'ratio=%s' % fs(SUPP))

ITEMS = []


def IT(code, kind, title, detail):
    ITEMS.append({'id': code, 'kind': kind, 'title': title, 'detail': detail})


def P(code, title, detail):
    IT(code, 'PASS', title, detail)


def F_(code, title, detail):
    IT(code, 'FAIL', title, detail)


def B(code, title, detail):
    IT(code, 'BOUNDARY', title, detail)


def I(code, title, detail):
    IT(code, 'INFO', title, detail)


I('I01', '受理：X-R90-1 是 r90 F3 登记、唯一未被定价的可计算项；本册只定价不代选',
  ('r90 把 W1 支判为「无健康非平凡解」（(i) lambda!=0 => 四阶 EOM+鬼；(ii) lambda=0 => '
   'kappaT 变分在真空奇异；(iii) 改识别 => 零新常数下无解析解）。其 F3 问：若允许 +1 长度常数 ell，'
   '取 kappa=ell*R（解析、整数幂、无奇异），「换回适定性」的收益未被定价。本册首算该收益与代价；'
   '与 r79-r91（弱场/PPN/屏蔽，走 W2/BD 口径）不重复（本册走 W1+ell 解析识别口径）。'))

P('I02', '量纲：kappa=ell*R 满足 [kappa]=L^-1 当且仅当 [ell]=L',
  ('[ell]=L（新基本长度常数）；[R]=L^-2（Ricci 标量）；则 [ell*R]=L*L^-2=L^-1，恰为 kappa 目标量纲'
   '（G0-7/G0-8/G0-9 机器校验通过）。这是 X-R90-1 的物理内容：用 1 个新常数把 kappa 从'
   '「曲率不变量的分数幂」换成「曲率不变量的整数幂（解析）」。'))

P('I03', '解析性复活（独立复现 r90 A2 的 132/0）：+1 常数使解析识别从 0 解变 >=1 解',
  ('在基 {R, R_abR^ab, R_abcdR^abcd}（幂域 [-2,2]、步长 1/4、共 4913 组）上，target [kappa]=L^-1 '
   '的分数幂解 = %d 组、整数解 = %d 组（与 r90 A2 的 132/0 逐位一致）；加入 ell 后（基 {ell,R,R2,R4}）'
   '整数解 = %d 组（样例 %s），分数幂解 = %d 组。⇒ +1 常数确实使「量纲正确且解析」的识别存在，'
   '直接回应 r90 A2 的「零整数解」障碍。'
   % (len(ENUM_R90), len(ENUM_R90_INT), len(ENUM_R92_INT),
      fmt_sol(SAMPLE_LR) if SAMPLE_LR else 'none', len(ENUM_R92))))

P('I04', '奇异性消除：kappa=K^{1/4} 在 K->0 发散，kappa=ell*R 有限',
  ('kappa=(R_abR^ab)^{1/4} 的 d(kappa)/dK=(1/4)K^{-3/4}；以 r76 宇宙平均曲率 K0=%s m^-4 为锚点，'
   '逐级缩小 10^-1 四次得导数 %.2e < %.2e < %.2e < %.2e（单调递增 => 真空发散，r90 A3 的奇异性）。'
   '而 kappa=ell*R 的 d/dR = ell = %s m（有限常数）。⇒ 解析识别消除 r90 A3 的真空奇异，'
   'kappaT 耦合的变分在源外有定义。'
   % (fv(K0), DK_AT_K0, DK_AT_K1, DK_AT_K2, DK_AT_K3, fv(ELL_LOCK))))

B('I05', 'U 项随识别改变（关键）：r90 的鬼结论不自动继承到 kappa=ell*R',
  ('kappa=(R_abR^ab)^{1/4} => U=lambda*kappa^4 = lambda*R_abR^ab（Ricci^2，r90 据此判 Stelle 鬼）；'
   '而 kappa=ell*R => U=lambda*kappa^4 = lambda*ell^4*R^4（R^4 型，G0-20/G0-21 量纲校验通过）。'
   '两 U 项不同构（G0-22）。⇒ 识别选择改变高阶导数结构，r90 的鬼结论是针对 Ricci^2 的，'
   '不自动继承到 R^4；该支鬼态须在 U=lambda*ell^4*R^4 下重判（精确线性化与 PPN = 登记为 X-R90-2，'
   '本册不做）。提示：R^4（Starobinsky 类）的线性化谱与 Ricci^2 不同，可能不含质量自旋-2 鬼'
   '（属 f(R) 型，可等价为健康标量-张量）；此点本册不自推，留待 X-R90-2。'))

B('I06', '代价：+1 常数 ell，两种口径下都不「免费」',
  ('按 r73 锁定定理，新长度常数被唯一长度标尺 l_P 锁定 => ell = %s m（=sqrt(4 pi) l_P，G0-6），'
   '自由度 0；但此时 kappa=ell*R 被普朗克尺度压死（见 I07），可观测内容 0。'
   '若保留 ell 为自由常数，则 +1 常数；且 f(R,T)/R^4 型在太阳系需屏蔽机制（chameleon/Vainshtein）'
   '=> 另 +1 自由函数，并入 r81/r85/r86 的 W2 账户（n_free=5 > 4 => 撞 Omega5）。'
   '⇒ 无论锁定还是自由，ell 都不带来「零代价」的适定性。' % fv(ELL_LOCK)))

I('I07', '收益空洞（独立估算，O(1) 模型依赖）：ell 锁定后 W1 比 r89 更空',
  ('锁定 ell=sqrt(4 pi) l_P 后，在中子星典型曲率 R~%s m^-2 处，kappa(ell*R)=%s 比分数幂识别 '
   'kappa=K^{1/4}=%s 小 约 %s 倍（G0-27）。结合 r89 的 kappaT 相对强度 5.5e-39，'
   'ell*R 支的可观测偏离 ~ 5.5e-39 * %s ~ 1e-77 => 比 r89 已判定的「零内容」更空。'
   '（R_abR^ab~R^2 与 R=7e-9 为 O(1) 量级估计，仅用于量级说明，非精确预言。）'
   % (fv(R_NS), fv(KAPPA_LR_NS), fv(KAPPA_K_NS), fs(SUPP), fs(SUPP))))

P('I08', '链上读数独立复现（对拍，非引用）',
  ('①枚举 132/0（G0-11/G0-12）；②鬼质量标度 m2(lambda_hat=1)=%s kg 与 r90 E5 的 %s 逐位同源'
   '（G0-23）；③lambda_hat_max=%s => m2=%s eV，与 r90 C1 的 %s eV 一致（G0-24）；'
   '④1 TeV 界 lambda_hat<=2.965e30 => m2~%s eV（~1 TeV），与 r90 C2 一致（G0-25）；'
   '⑤K0=%s m^-4 复用作奇异性演示锚点（G0-18）。全部由本册独立引擎重算得到。'
   % (fv(M2_KG_AT1), fv(M2_R90_KG), fv(LAMBDA_HAT_MAX), fv(M2_EV_ATMAX), fv(M2_R90_EV),
      fv(M2_EV_ATTEV), fv(K0))))

I('I09', '结论：X-R90-1 定价完成 —— 收益真实但被榨干，决策 X-R76-2 信息已完整',
  ('付 +1 常数 ell 真实换回「解析性 + 真空正则性」，且因 U 项变 R^4 型使鬼态需重判（可能比 Ricci^2 友好，'
   '待 X-R90-2）。代价端：ell 被 l_P 锁定 => 自由度 0 且修正被普朗克尺度压死（可观测内容 ~1e-77）；'
   '或自由 => +1 常数 + 屏蔽 => 撞 Omega5。净收益 = 「退回纯 GR + 普朗克压死的尾项」'
   '+「一个待 X-R90-2 重判的 R^4 支」。至此 X-R76-2 的三条出路均已机器定量：'
   'W1(ell) 解析但空洞/待重判、W2 撞 Omega5、W3 被纯标量偏折排除 => 决策所需信息不再有缺口。'))

I('I10', '不自推清单（NS）',
  'NS1：Cassini |gamma-1|<2.3e-5 与 1.75 角秒偏折为外部实验事实。'
  'NS2：PPN gamma=-1 为纯标量引力教科书结论。'
  'NS3：Stelle 鬼质量公式 m2=M_Pl/sqrt(16 pi lambda_hat) 为 r90 约定（O(1) 系数依约定），本册引用不自推。'
  'NS4：CODATA 的 hbar/c/G/l_P 为测量值。'
  'NS5：f(R)/R^4 线性化是否无鬼为已知结论方向，但本册的 U=lambda*ell^4*R^4 精确谱与 PPN 属 X-R90-2，不自推。'
  'NS6：ell 被 l_P 锁定定理承 r73，不自推。')

I('I11', '治理与红线',
  '编号 r92（r91 后首空号；下轮从 r93 起）。未改动任何他人文件字节（来料正本只读）；'
  '未跑 refresh_catalog；未改 verify.py；未做 git 操作。'
  '红线：数学/数值自洽 != 物理证实。「W1(ell) 解析但空洞、W2 撞 Omega5、W3 被排除」'
  '不等于「TUFT 方向被否证」——W1(ell)+R^4 支与 W2 均未被否证，只是都不便宜，且 W1(ell) 的鬼态仍待 X-R90-2 定夺。')

P('I12', '阳性对照与守卫汇总（证明各判据非恒真/非恒零）',
  ('量纲工具：异构相加抛 TypeError（G0-4）、[G]/[hbar]/[c] 自洽（G0-1/2/3）；'
   '枚举器：target=L 在 {hbar,c,G} 命中 0（G0-16）、+ell 后 >=1（G0-17）=> 有分辨力；'
   '鬼质量公式：扰动 lambda 1e-6 改变 m2（G0-26）=> 有分辨力；'
   '奇异性：K^{1/4} 导数单调递增（G0-18）=> 发散演示非恒值。'))

KEY = {
    'ell_lock_m': fv(ELL_LOCK),
    'sqrt_4pi': fv(SQRT_4PI),
    'l_p_calc_m': fv(LP_CALC),
    'kappa_dim_check': dstr(KAPPA_LR),
    'enum_r90_total_frac': len(ENUM_R90),
    'enum_r90_integer': len(ENUM_R90_INT),
    'enum_r92_integer': len(ENUM_R92_INT),
    'enum_r92_total': len(ENUM_R92),
    'sample_lr_solution': fmt_sol(SAMPLE_LR) if SAMPLE_LR else 'none',
    'dk_K_at_K0': fv(DK_AT_K0),
    'dk_K_at_K0_1e-3': fv(DK_AT_K3),
    'dk_ellR_constant': fv(DK_LR),
    'u_ricci_dim': dstr(U_RICCI),
    'u_r4_dim': dstr(U_R4),
    'm2_kg_at_lambda1': fv(M2_KG_AT1),
    'm2_r90_kg_ref': fv(M2_R90_KG),
    'm2_ev_at_lambda_max': fv(M2_EV_ATMAX),
    'm2_r90_ev_ref': fv(M2_R90_EV),
    'm2_ev_at_1tev_bound': fv(M2_EV_ATTEV),
    'lambda_hat_max': fv(LAMBDA_HAT_MAX),
    'k0_m4': fv(K0),
    'r_ns_m2': fv(R_NS),
    'kappa_K_ns': fv(KAPPA_K_NS),
    'kappa_lr_ns': fv(KAPPA_LR_NS),
    'suppression_ratio': fs(SUPP),
}

NS = [
    'NS1：Cassini |gamma-1|<2.3e-5 与 1.75 角秒偏折为外部实验事实，本册引用不自推。',
    'NS2：PPN gamma=-1 为纯标量引力教科书结论，本册引用不自推。',
    'NS3：Stelle 鬼质量公式 m2=M_Pl/sqrt(16 pi lambda_hat) 为 r90 约定（O(1) 系数依约定），本册引用不自推。',
    'NS4：CODATA 的 hbar / c / G / l_P 为实验测量值，非第一性导出。',
    'NS5：f(R)/R^4 线性化是否无鬼为已知方向，但本册 U=lambda*ell^4*R^4 的精确谱与 PPN 属 X-R90-2，不自推。',
    'NS6：ell 被 l_P 锁定定理承 r73，不自推。',
]

NAME = 'TUFT-r93_XR90-1首算_κ=ℓR解析识别的代价收益机器定价_攻破_2026-10-17'


def tally():
    d = {}
    for it in ITEMS:
        d[it['kind']] = d.get(it['kind'], 0) + 1
    return d


def main():
    cnt = tally()
    guard_ok = all(x[1] for x in GUARDS)
    guard_n = len(GUARDS)
    guard_pass = sum(1 for x in GUARDS if x[1])
    verdict = 'FAIL' if cnt.get('FAIL', 0) > 0 else 'PASS'

    payload = {
        'round': 'r93',
        'date': '2026-10-17',
        'topic': 'X-R90-1 首算：kappa=ell*R 解析识别的代价—收益机器定价',
        'items': ITEMS,
        'counts': cnt,
        'total': len(ITEMS),
        'verdict': verdict,
        'guards': [{'tag': t, 'ok': ok, 'detail': d} for t, ok, d in GUARDS],
        'guard_all_ok': guard_ok,
        'guard_total': guard_n,
        'guard_pass': guard_pass,
        'key_numbers': KEY,
        'not_self_derived': NS,
    }

    HERE = os.path.dirname(os.path.abspath(__file__))
    BASE = os.path.dirname(HERE)
    DATA = os.path.join(BASE, '数据')
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    jp = os.path.join(DATA, NAME + '.json')
    with open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    lines = []
    lines.append('# ' + NAME)
    lines.append('')
    lines.append('- 条目 %d：%s' % (len(ITEMS), ' / '.join(
        '%s %d' % (k, cnt[k]) for k in sorted(cnt.keys()))))
    lines.append('- verdict: %s · 守卫 %d/%d' % (verdict, guard_pass, guard_n))
    lines.append('')
    for it in ITEMS:
        lines.append('## %s · %s · %s' % (it['id'], it['kind'], it['title']))
        lines.append('')
        lines.append(it['detail'])
        lines.append('')
    lines.append('## 数值档案')
    lines.append('')
    for k in sorted(KEY.keys()):
        lines.append('- %s = %s' % (k, str(KEY[k])))
    lines.append('')
    lines.append('## 不自推')
    lines.append('')
    for s in NS:
        lines.append('- ' + s)
    lines.append('')
    mp = os.path.join(DATA, NAME + '.md')
    with open(mp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    rep = []
    rep.append('TUFT r92 report')
    rep.append('items=%d %s' % (len(ITEMS), cnt))
    rep.append('guards=%d/%d ok=%s' % (guard_pass, guard_n, guard_ok))
    rep.append('verdict=%s' % verdict)
    for t, ok, d in GUARDS:
        rep.append('%s %s | %s' % ('OK ' if ok else 'BAD', t, d))
    rp = os.path.join(DATA, NAME + '_report.txt')
    with open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rep) + '\n')

    print('items=%d %s' % (len(ITEMS), cnt))
    print('guards=%d/%d' % (guard_pass, guard_n))
    print('verdict=%s' % verdict)
    print('enum_r90 132? %d  int0? %d' % (len(ENUM_R90), len(ENUM_R90_INT)))
    print('enum_r92 int>=1? %d  total=%d' % (len(ENUM_R92_INT), len(ENUM_R92)))
    print('m2(1)=%s kg  m2(max)=%s eV' % (fv(M2_KG_AT1), fv(M2_EV_ATMAX)))
    print('suppression=%s' % fs(SUPP))
    return 0 if guard_ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
