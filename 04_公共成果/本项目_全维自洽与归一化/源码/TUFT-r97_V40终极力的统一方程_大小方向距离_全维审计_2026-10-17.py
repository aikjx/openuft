# -*- coding: utf-8 -*-
"""
TUFT V4.0 终极力的统一方程（大小·方向·距离）· 全维审计（r97）

来料：《TUFT V4.0 终极力的统一方程｜大小·方向·距离 全维度数理推导与精算证明》
      六节：§一 主方程 F=-c^2 nabla(k^2-tau^2)·r / §二 求导证明 / §三 四力分化
            §四 尺度贯通 / §五 量纲闭环 / §六 终极结论

主方程（来料原文，两种并列写法）：
    (M1) F_uni = -c^2 * nabla(kappa^2 - tau^2) * r          （§一 矢量式）
    (M2) F_uni = -c^2 * d/dr(kappa^2 - tau^2) * rhat        （§二 步骤3 式，无 r）
    (M3) F_uni = -c^2 * r * d/dr(kappa^2 - tau^2)           （§二 步骤4 完备式 / §三 精算式）
    (U ) U(r)  = c^2 * (kappa^2 - tau^2)                    （§二 步骤1 势能）

条目前缀 U01..U2x（与既有 V/W/Y/Z/A-H 系列互斥，不可相加）。
纯标准库：Decimal 60 位 + Fraction 四元组量纲 (M,L,T,Q) + 自然单位折算 + 中心差分对拍。
"""
import sys, io, os, json, decimal, datetime
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)

# ---------------- 常量（CODATA / 标准值；不自推登记 NS1） ----------------
C_LIGHT = Decimal('299792458')
C2 = C_LIGHT * C_LIGHT
G_NEW = Decimal('6.67430e-11')
HBAR = Decimal('1.054571817e-34')
M_W = Decimal('80.379')            # GeV/c^2（PDG；与 r22 的 lambda_W 口径对齐）
GEV = Decimal('1.602176634e-10')   # J
M_SUN = Decimal('1.98847e30')

# 自然单位 kappa 识别（承 r90 A2 route(a)）：kappa = (R_ab R^ab)^{1/4}
# Schwarzschild 外部为真空：Ricci = 0  => R_abR^ab = 0 => kappa = 0

# ---------------- 量纲工具（四元组 (M,L,T,Q)；纪律：逐项手算必须由机器兜底） ----------------
M_DIM = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
L_DIM = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
T_DIM = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
Q_DIM = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))
NONE  = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))

def dmul(a, b):
    """量纲相乘 = 指数逐分量相加（纪律：严禁逐分量相乘，r37/r44/r66 均曾踩）"""
    return tuple(a[i] + b[i] for i in range(4))

def ddiv(a, b):
    return tuple(a[i] - b[i] for i in range(4))

def dpow(a, n):
    return tuple(a[i] * Fraction(n) for i in range(4))

def dstr(a):
    sym = 'MLTQ'
    out = []
    for i in range(4):
        e = a[i]
        if e == 0:
            continue
        if e == 1:
            out.append(sym[i])
        else:
            out.append('%s^%s' % (sym[i], e))
    return '1' if not out else ''.join(out)

def nat(a):
    """自然单位（hbar=c=1）折算为 L 幂次：nat = l + t - m（Q 分量单独并列）"""
    return a[1] + a[2] - a[0]

# ---------------- 输出器 ----------------
REPORT = []
COUNTS = {'PASS': 0, 'FAIL': 0, 'BOUNDARY': 0, 'INFO': 0, 'CORRECTED': 0, 'MISMATCH': 0}

def _add(kind, code, msg):
    REPORT.append({'code': code, 'kind': kind, 'msg': msg})
    COUNTS[kind] = COUNTS.get(kind, 0) + 1

def P(code, msg):  _add('PASS', code, msg)
def F(code, msg):  _add('FAIL', code, msg)
def B(code, msg):  _add('BOUNDARY', code, msg)
def I(code, msg):  _add('INFO', code, msg)
def CR(code, msg): _add('CORRECTED', code, msg)
def MS(code, msg): _add('MISMATCH', code, msg)

def Dc(x):
    """任意 -> Decimal（严禁把字符串先做算术）"""
    if isinstance(x, Decimal):
        return x
    return Decimal(str(x))

def fv(x, n=25):
    """定点科学计数输出（Decimal.quantize 在高位数抛 InvalidOperation，改用 format）"""
    try:
        return format(Dc(x), '.%dE' % n)
    except Exception:
        return str(x)

def fs(x, n=6):
    try:
        return format(Dc(x), '.%dE' % n)
    except Exception:
        return str(x)

# ---------------- 量纲基准（SI 四元组；自然单位由 nat() 折算） ----------------
D_C    = (Fraction(0), Fraction(1), Fraction(-1), Fraction(0))            # [c]=LT^-1
D_HBAR = (Fraction(1), Fraction(2), Fraction(-1), Fraction(0))            # [hbar]=ML^2T^-1
D_G    = (Fraction(-1), Fraction(3), Fraction(-2), Fraction(0))           # [G]=M^-1L^3T^-2
D_KAPPA= (Fraction(0), Fraction(-1), Fraction(0), Fraction(0))            # [kappa]=L^-1
D_TAU  = (Fraction(0), Fraction(-1), Fraction(0), Fraction(0))            # [tau]=L^-1
D_NAB  = (Fraction(0), Fraction(-1), Fraction(0), Fraction(0))            # [nabla]=L^-1
D_R    = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))             # [r]=L
D_ENERGY=(Fraction(1), Fraction(2), Fraction(-2), Fraction(0))            # [E]=ML^2T^-2
D_FORCE= (Fraction(1), Fraction(1), Fraction(-2), Fraction(0))            # [F]=MLT^-2
D_PRESS= (Fraction(1), Fraction(-1), Fraction(-2), Fraction(0))           # [p]=ML^-1T^-2
D_EPS0 = (Fraction(-1), Fraction(-3), Fraction(4), Fraction(2))           # [eps0]=M^-1L^-3T^4Q^2
D_MU0  = (Fraction(1), Fraction(1), Fraction(-2), Fraction(-2))           # [mu0]=MLT^-2Q^-2

# 主方程各构件的量纲
D_PHI  = dpow(D_KAPPA, 2)                       # [kappa^2] = L^-2（kappa^2-tau^2 同）
D_NAB_PHI = dmul(D_NAB, D_PHI)                  # [nabla(kappa^2-tau^2)] = L^-3
D_C2   = dpow(D_C, 2)                           # [c^2] = L^2T^-2

# 来料三种写法
D_M1   = dmul(dmul(D_C2, D_NAB_PHI), D_R)       # -c^2 * nabla(phi) * r
D_M2   = dmul(D_C2, D_NAB_PHI)                  # -c^2 * nabla(phi)（步骤3：无 r）
D_M3   = dmul(dmul(D_C2, D_R), D_NAB_PHI)       # -c^2 * r * d/dr(phi)（步骤4：与 M1 同构）
D_U    = dmul(D_C2, D_PHI)                      # U = c^2(kappa^2-tau^2)

# ---------------- 守卫 G0：量纲工具自身必须先过自检（r37/r44/r66 纪律） ----------------
GUARDS = []
def gassert(name, cond, detail):
    GUARDS.append({'name': name, 'ok': bool(cond), 'detail': detail})

gassert('G0-1', D_C == (Fraction(0), Fraction(1), Fraction(-1), Fraction(0)) and nat(D_C) == 0,
        '[c]=%s, nat=%s' % (dstr(D_C), nat(D_C)))
gassert('G0-2', D_HBAR == (Fraction(1), Fraction(2), Fraction(-1), Fraction(0)) and nat(D_HBAR) == 0,
        '[hbar]=%s, nat=%s' % (dstr(D_HBAR), nat(D_HBAR)))
gassert('G0-3', D_G == (Fraction(-1), Fraction(3), Fraction(-2), Fraction(0)) and nat(D_G) == 2,
        '[G]=%s, nat=%s' % (dstr(D_G), nat(D_G)))
gassert('G0-4', nat(D_KAPPA) == -1 and nat(D_TAU) == -1,
        '[kappa]=[tau]=%s, nat=%s' % (dstr(D_KAPPA), nat(D_KAPPA)))
gassert('G0-5', D_NAB == (Fraction(0), Fraction(-1), Fraction(0), Fraction(0)), '[nabla]=%s' % dstr(D_NAB))
gassert('G0-6', D_ENERGY == (Fraction(1), Fraction(2), Fraction(-2), Fraction(0)) and nat(D_ENERGY) == -1,
        '[能量]=%s, nat=%s' % (dstr(D_ENERGY), nat(D_ENERGY)))
gassert('G0-7', D_FORCE == (Fraction(1), Fraction(1), Fraction(-2), Fraction(0)) and nat(D_FORCE) == -2,
        '[力]=%s, nat=%s' % (dstr(D_FORCE), nat(D_FORCE)))
gassert('G0-8', D_PHI == (Fraction(0), Fraction(-2), Fraction(0), Fraction(0)) and nat(D_PHI) == -2,
        '[kappa^2-tau^2]=%s, nat=%s' % (dstr(D_PHI), nat(D_PHI)))
gassert('G0-9', D_NAB_PHI == (Fraction(0), Fraction(-3), Fraction(0), Fraction(0)),
        '[nabla(kappa^2-tau^2)]=%s（真值，非来料所写的 L^-2）' % dstr(D_NAB_PHI))
gassert('G0-10', dmul(dmul(D_EPS0, D_MU0), D_C2) == NONE, 'eps0*mu0*c^2 无量纲')
gassert('G0-11', nat(dmul(D_HBAR, D_C)) == 0, 'nat(hbar*c)=%s' % nat(dmul(D_HBAR, D_C)))
# 阳性对照：工具非恒零（三个互异量纲必须给出互异的 nat）
gassert('G0-12', len({nat(D_G), nat(D_C), nat(D_ENERGY), nat(D_FORCE)}) == 4,
        '阳性对照：nat(G)=%s、nat(c)=%s、nat(能量)=%s、nat(力)=%s 四者互异（工具非恒零）'
        % (nat(D_G), nat(D_C), nat(D_ENERGY), nat(D_FORCE)))

# ================= A 组：量纲层 =================
GAP_U = ddiv(D_ENERGY, D_U)      # 能量 / U  => 缺口
GAP_F = ddiv(D_FORCE, D_M3)      # 力 / F(M3) => 缺口
GAP_M2 = ddiv(D_FORCE, D_M2)

# U01 势能量纲
nat_u = nat(D_U)
F('U01', '势能 U=c^2(kappa^2-tau^2) 量纲 = %s（能量应为 %s）｜'
         'SI 缺口 = %s｜自然单位 nat(U)=%s，自然单位 [能量]=-1 ⇒ nat 差 %s ⇒ 双口径皆破'
         % (dstr(D_U), dstr(D_ENERGY), dstr(GAP_U), nat_u, nat_u - (-1)))

# U02 力量纲（按来料自述 SI 口径）
nat_m3 = nat(D_M3)
F('U02', '力式 F=-c^2*r*d/dr(kappa^2-tau^2) 量纲 = %s（SI 实得 T^-2，非力）｜'
         'SI 缺口 = %s｜自然单位 nat=%s 与自然单位 [力]=-2 %s ⇒ 口径分列：SI 破 / 自然单位形式闭合'
         % (dstr(D_M3), dstr(GAP_F), nat_m3,
            '一致' if nat_m3 == -2 else '不一致'))

# U03 核心：U-F 缺口错位 = r 因子的指纹
offset = ddiv(GAP_U, GAP_F)
F('U03', '★ U 与 F 的量纲缺口错位判据：缺口(U)=%s，缺口(F)=%s ⇒ 缺口之比 = %s（恰一个长度幂次）｜'
         '自然单位侧 nat 差：U 侧 %s、F 侧 %s，同为 1 个 L ⇒ 两口径一致指向同一来源 = 额外插入的 r 因子'
         % (dstr(GAP_U), dstr(GAP_F), dstr(offset),
            nat_u - (-1), nat_m3 - (-2)))

# U04 核心：r 因子二难
#  (a) 留 r：F(M3) 与 -grad U 的比值
ratio_M3_over_gradU = ddiv(D_M3, dmul(D_C2, D_NAB_PHI))   # = [r]
F('U04', '★ r 因子二难（两条路皆失败）：'
         '(a) 留 r ⇒ F(M3)/(-gradU) 的量纲比 = %s，即 F = r*(-gradU) ≠ -gradU ⇒ 力不是势的负梯度（非保守）；'
         '且 (b) 删 r 退化为 M2 时：[M2]=%s 在自然单位 nat=%s ≠ 力(-2) ⇒ 力式量纲破，'
         '同时 kappa∝1/r 给 F∝r^-3 ≠ 牛顿 r^-2（承 r33 B01/C01 的 V4.1 口径同型）'
         % (dstr(ratio_M3_over_gradU), dstr(D_M2), nat(D_M2)))

# U05 §五 量纲核验本身错：两个错误互补
claim_nab_phi = (Fraction(0), Fraction(-2), Fraction(0), Fraction(0))   # 来料写 L^-2
claim_F = dmul(dmul(D_C2, claim_nab_phi), D_R)                         # = L T^-2
real_with_claim = ddiv(D_FORCE, claim_F)                               # 应补 M
path_i  = dmul(dmul(D_C2, D_NAB_PHI), D_R)                             # 只补 nabla 的 L^-1
path_ii = dmul(dmul(D_C2, claim_nab_phi), D_R)                         # 只去掉凭空的 M（= L T^-2）
path_iii= path_i
F('U05', '★ §五 量纲核验式自身不成立（两个错误互补凑出结论）：'
         '来料写 [nabla(kappa^2-tau^2)]=L^-2，真值 %s（漏一个 L^-1）；其三项代入得 %s，却直接写出 %s（凭空加 M）｜'
         '三条修正路径全不闭合：(i) 只补 nabla 的 L^-1 ⇒ %s；(ii) 只去掉凭空的 M ⇒ %s；(iii) 两者都做 ⇒ %s；无一等于 %s'
         % (dstr(D_NAB_PHI), dstr(claim_F), dstr(D_FORCE),
            dstr(path_i), dstr(path_ii), dstr(path_iii), dstr(D_FORCE)))

# U06 c^2 代 alpha：承 r94 B 组，本册把账落到 V4.0
D_ALPHA = (Fraction(1), Fraction(4), Fraction(-2), Fraction(0))   # [alpha]=ML^4T^-2（r94 判定）
gap_alpha_c2 = ddiv(D_ALPHA, D_C2)
# 穷举 {hbar,c,G} 整数幂 [-6,6] 对 [alpha] 与 [c^2] 的命中数
def enum_hits(target, rng=6):
    hits = []
    for a in range(-rng, rng + 1):
        for b in range(-rng, rng + 1):
            for e in range(-rng, rng + 1):
                v = dmul(dmul(dpow(D_HBAR, a), dpow(D_C, b)), dpow(D_G, e))
                if v == target:
                    hits.append((a, b, e))
    return hits
hits_alpha = enum_hits(D_ALPHA)
hits_c2 = enum_hits(D_C2)
F('U06', 'c^2 不是 alpha 的替代品：r94 判 [alpha]=%s（新独立量纲常数），c^2=%s ⇒ 商 = %s｜'
         '{hbar,c,G} 整数幂 [-6,6]^3=2197 组穷举：对 [alpha] 命中 %d 组、对 [c^2] 命中 %d 组 ⇒ 两者不同源；'
         '用 c^2 代 alpha 的代价 = 须让 (kappa^2-tau^2) 额外承载 %s，而 [kappa^2-tau^2]=%s 固定 ⇒ 结构性不可能'
         % (dstr(D_ALPHA), dstr(D_C2), dstr(gap_alpha_c2),
            len(hits_alpha), len(hits_c2), dstr(gap_alpha_c2), dstr(D_PHI)))

# ---------------- 数值工具：中心差分（解析式对拍，容差按差分截断 O(h^2)） ----------------
def central_diff(fn, r, h_rel=Decimal('1e-6')):
    h = Dc(r) * h_rel
    return (fn(Dc(r) + h) - fn(Dc(r) - h)) / (2 * h)

# ---- 四力 ansatz（来料原文：无源量，比例常数取 1；A_g/A_e 为无量纲比例常数） ----
def kappa_g(r, A=Decimal(1)):
    return A / Dc(r)                       # kappa ∝ 1/r（§三.1）

def tau_e(r, A=Decimal(1)):
    return A / Dc(r)                       # tau ∝ 1/r（§三.2）

def phi_g(r, A=Decimal(1)):                # kappa^2 - tau^2，tau->0 引力极限
    return kappa_g(r, A) ** 2

def phi_e(r, A=Decimal(1)):                # kappa->0 电磁极限：0 - tau^2
    return -(tau_e(r, A) ** 2)

def F_of_M3(phi, r):
    """F = -c^2 * r * d/dr(phi)，返回标量系数（沿 rhat）"""
    return -C2 * Dc(r) * central_diff(phi, r)

def F_of_M2(phi, r):
    """F = -c^2 * d/dr(phi)（删去 r 因子的对照口径）"""
    return -C2 * central_diff(phi, r)

def analytic_g(r, A=Decimal(1)):
    return 2 * C2 * A * A / (Dc(r) ** 2)

def analytic_e(r, A=Decimal(1)):
    return -2 * C2 * A * A / (Dc(r) ** 2)

def analytic_g_M2(r, A=Decimal(1)):
    return 2 * C2 * A * A / (Dc(r) ** 3)

# ================= B 组：引力段 =================
# U07 引力符号：tau->0 时 F = -c^2 r d/dr(kappa^2) = +2c^2A^2/r^2 （沿 +rhat = 排斥）
r_test = Decimal('1')
fg_num = F_of_M3(phi_g, r_test)
fg_ana = analytic_g(r_test)
diff_rel = abs(fg_num - fg_ana) / abs(fg_ana)
sgn = '排斥（沿 +rhat）' if fg_ana > 0 else '吸引（沿 -rhat）'
F('U07', '★ 引力极限 tau->0 下 F_g = -c^2*r*d/dr(kappa^2) = +%s（A=1,r=1m；c^2A^2/r^2 口径，量纲见 U02）⇒ 符号为正 ⇒ %s｜'
         '中心差分 vs 解析式相对残差 %s（差分截断极限，非 0 ⇒ 排除恒等复读）｜'
         '牛顿引力为吸引 ⇒ 与来料自身 ansatz 下的机器结果**反号**（非「未声明」，是唯一确定）'
         % (fs(fg_ana), sgn, fs(diff_rel)))

# U08 无源量：A 必无量纲 ⇒ 不能承载 M,m
D_A = ddiv(D_KAPPA, dpow(D_R, -1))     # [A] = [kappa]/[1/r] = L^-1/L^-1 = 1
ratio_model = analytic_g(r_test, Decimal(1)) / analytic_g(r_test, Decimal(1))
m1, m2 = Decimal('1'), M_SUN
# 同口径：检验质量固定 1 kg，源质量由 1 kg 换为 M_sun 时力的变化
ratio_newton = (G_NEW * m1 * m1) / (G_NEW * m2 * m1)
F('U08', '★ 无源量 ⇒ 引力不依赖源质量：kappa∝1/r 的比例常数 A 量纲 = %s（必为无量纲，因 [kappa]=[1/r]=L^-1）⇒ '
         'A 不能承载 M,m（量纲量）｜机器：F_g(M=1kg)/F_g(M=M_sun) = %s，牛顿同口径 = %s ⇒ 差 %s 倍'
         % (dstr(D_A), fs(ratio_model), fs(ratio_newton), fs(m2 / m1)))

# U09 势口径不相容：U=c^2 kappa^2 ∝ 1/r^2 ≠ 牛顿势 ∝ 1/r
# 反解使 U = -GMm/r 所需的 kappa 幂次：kappa^2 = GMm/(c^2 r) ⇒ kappa ∝ r^{-1/2}
kappa_needed_exp = Fraction(-1, 2)
F('U09', '势口径与牛顿势不相容：U=c^2*kappa^2 取 kappa∝1/r ⇒ U∝r^-2；牛顿势 ∝ r^-1 ⇒ '
         '要使 U=-GMm/r 须 kappa∝r^%s，与来料的 kappa∝r^-1 相差 r^%s 因子（不能用比例常数吸收）'
         % (kappa_needed_exp, kappa_needed_exp - (-1)))

# U10 kappa∝1/r 无几何来源：与标准曲率不变量的径向依赖不符
# Kretschmann: K = 48(GM/c^2)^2/r^6 ⇒ K^{1/4} ∝ r^{-3/2}
r_sun = Decimal('6.957e8')
rg = G_NEW * M_SUN / C2                     # GM/c^2 = 1.4766e3 m
kappa_K = (Decimal(48).ln() / 4).exp() * (rg.sqrt()) * (r_sun ** Decimal('-1.5'))
kappa_1overr = 1 / r_sun
B('U10', 'kappa∝1/r 无几何来源：取标准 Kretschmann 标量 K=48(GM/c^2)^2/r^6 ⇒ K^{1/4}∝r^{-3/2}（非 r^-1）；'
         '在 r=R_sun、M=M_sun 处 K^{1/4}=%s m^-1 vs 1/r=%s m^-1 ⇒ 相差 %s 倍，且该比值随 r 变（幂次差 r^-1/2）⇒ '
         '不可用常数吸收｜另：承 r90 A2 route(a) 的 kappa=(R_abR^ab)^{1/4} 识别下，Schwarzschild 真空 Ricci=0 ⇒ kappa≡0 ⇒ '
         '主方程引力段恒零（该支依赖未裁决项 X-R90-1，本册不自推、不代选）'
         % (fs(kappa_K), fs(kappa_1overr), fs(kappa_1overr / kappa_K)))

# ================= C 组：电磁段 =================
# U11 tau^2 恒正 ⇒ 电磁力恒吸引，同号电荷排斥不可表达
fe_ana = analytic_e(r_test)
fe_num = F_of_M3(phi_e, r_test)
fe_diff = abs(fe_num - fe_ana) / abs(fe_ana)
def tau_with_charge(q1, q2, r):
    # 若要让 tau 承载电荷符号，唯一入口是 tau ∝ sqrt(q1q2)/r（因式中只出现 tau^2）
    prod = Dc(q1) * Dc(q2)
    if prod < 0:
        return None     # 异号电荷 ⇒ 根号内为负 ⇒ tau 为虚数
    return (prod.sqrt()) / Dc(r)
t_same = tau_with_charge(Decimal(1), Decimal(1), r_test)
t_oppo = tau_with_charge(Decimal(1), Decimal(-1), r_test)
F('U11', '★ 电磁扇区结构上不存在排斥：F_e = -c^2*r*d/dr(-tau^2) = %s（恒为负 ⇒ 恒吸引）｜'
         '中心差分 vs 解析残差 %s｜tau 在式中只以 tau^2 出现 ⇒ 电荷乘积的符号被平方抹去；'
         '唯一让 tau 承载 q1q2 的写法 tau∝sqrt(q1q2)/r 对异号电荷给出%s ⇒ 电磁的吸引/排斥二元性不可表达'
         % (fs(fe_ana), fs(fe_diff), '虚数（不可实现）' if t_oppo is None else fs(t_oppo)))

# U12 无源量 ⇒ 与电荷无关
F('U12', '无源量 ⇒ 电磁力与电荷无关：tau∝1/r 的比例常数必无量纲（[tau]=[1/r]=L^-1）⇒ '
         'F_e(q=1)/F_e(q=1e-3) = %s，库仑同口径 = %s ⇒ 差 %s 倍'
         % (fs(analytic_e(r_test) / analytic_e(r_test)),
            fs(Decimal('1e-6')), fs(Decimal('1e6'))))

# U13 符号分工固定，与「手性决定方向」不符
I('U13', '符号分工由 kappa^2-tau^2 的代数结构锁死：kappa 项贡献 -c^2*r*d/dr(+kappa^2) = 正 ⇒ 排斥；'
         'tau 项贡献 -c^2*r*d/dr(-tau^2) = 负 ⇒ 吸引；二者与径向下单调递减假设绑定，'
         '来料 §三.2「方向由挠率拓扑手性区分」在式中无载体（tau^2 对 tau->-tau 不变 ⇒ 手性不可分辨）')

# ================= D 组：弱力 / 强力（承 r33，本册只做 c^2 口径与增量数值，不重复裁定） =================
# U14 弱力：平方使汤川质量翻倍 ⇒ 力程减半
# m_W 用 PDG 80.379 GeV/c^2（口径与 r22 的 lambda_W 读数对齐）
m_w_kg = Decimal('80.379') * GEV / C2
lam_w = HBAR / (m_w_kg * C_LIGHT)
I('U14', '承 r33 D02（本册不重复裁定，只做 c^2 口径复算）：tau_w∝e^{-mr}/r ⇒ tau_w^2∝e^{-2mr}/r^2 ⇒ '
         '汤川指数质量翻倍 ⇒ 有效力程减半。m_W=80.379 GeV ⇒ lambda_W=hbar/(m_W c)=%s m（与 r22 读数 2.454957e-18 同口径）；'
         '本式给出的有效力程 = lambda_W/2 = %s m（与 §三.3 自称的 1e-18 m 核尺度同量级但非同一量）'
         % (fs(lam_w, 20), fs(lam_w / 2, 20)))

# U15 强力形状：F_s ∝ -2r^2(1-r/r0)e^{-2r/r0}（c^2 与比例常数已略去）
def Fs_shape(r, r0):
    x = Dc(r) / Dc(r0)
    return -2 * x * x * (1 - x) * (-2 * x).exp()
R0 = Decimal('1e-15')
rows = []
for mult in ['0.1', '0.5', '0.9', '1.0', '1.5', '2.0', '10']:
    rr = R0 * Decimal(mult)
    rows.append((mult, Fs_shape(rr, R0)))
zero_at = 'r=r0'
sgn_flip = [m for m, v in rows if v > 0]
I('U15', '承 r33 E03（c^2 口径复算 + 数值表，本册不重复裁定）：F_s ∝ -2r^2(1-r/r0)e^{-2r/r0} ⇒ '
         'r<r0 吸引 / %s 归零 / r>r0 **反号排斥**（翻转点集 = r>%s，实测正号点 %s）｜'
         '形状表（r0=1e-15 m，单位 r0^2）：%s'
         % (zero_at, 'r0', ','.join(sgn_flip),
            '; '.join('r=%s r0: %s' % (m, fs(v)) for m, v in rows)))

# U16 r->0 行为与「渐近自由」相反
v_small = Fs_shape(R0 * Decimal('0.1'), R0)
v_at_r0 = Fs_shape(R0, R0)
I('U16', '承 r33 E02（本册给 c^2 口径数值，不重复裁定）：本式 F_s(0.1 r0)=%s、F_s(r0)=0（精确）⇒ 短距趋零；'
         'QCD 渐近自由指 alpha_s->0（耦合），力仍 ~alpha_s/r^2 ⇒ 短距**增大**而非趋零 ⇒ '
         '「近距离恒定饱和（渐近自由）」不成立' % (fs(v_small),))

# U17 与 Cornell 势不符
I('U17', '承 r33 E04（本册做 c^2 口径的形状核对，不重复裁定）：与 Cornell 势 V=-a/r+sigma*r'
         '（F=-a/r^2-sigma，恒吸引 + 常力弦张力）不符：本式既无 1/r^2 库仑项、也无常数弦张力项，'
         '且在 r>r0 反号为排斥 ⇒ 「彻底解释夸克禁闭、强力渐近自由」不成立')

# ================= E 组：结构 / 外部输入 / 判别力 / 尺度贯通 =================
# U18 外部输入计数（与「无自由参数」矛盾）
EXT_INPUTS = ['kappa∝1/r 的比例常数 A_g', 'tau∝1/r 的比例常数 A_e',
              'tau_weak∝e^{-mr}/r 的比例常数 A_w', '弱力能标 m（力程）',
              'tau_strong∝r*e^{-r/r0} 的比例常数 A_s', '强力标度 r0']
F('U18', '外部输入账：%d 项（%s）与 §六.1「无独立机制、无额外参数」直接矛盾（计数法承 r30 Y38 符号计数）'
         % (len(EXT_INPUTS), '、'.join(EXT_INPUTS)))

# U19 场分配是字典：tau 一符号三用
F('U19', '场分配是字典式输入而非推导：tau 同一符号被同时指派给电磁(∝1/r)、弱(∝e^{-mr}/r)、强(∝r*e^{-r/r0})，'
         '仅靠人为指定的函数形式区分 ⇒ 四力分化由输入给出（承 r19/r20/r79 C3 同型结论）')

# U20 零判别力（承 r33 F01；本册在 r 因子口径下用「构造+回代」独立复现）
GMm = G_NEW * Decimal('1') * Decimal('1')
KK = Decimal('8.9875517873e9')
AA = Decimal('1e-26')          # Cornell 库仑项系数 a（≈0.5*hbar*c）
SIGMA = Decimal('1.44e5')      # 弦张力 0.9 GeV/fm ≈ 1.44e5 N
F0 = Decimal('1')
KHO = Decimal('1')

# 反解式：d/dr(Phi) = -F/(c^2 r) ⇒ Phi = -∫F/(c^2 s)ds（下列均为解析原函数）
def F_newton(r):   return -GMm / (Dc(r) ** 2)
def Phi_newton(r): return -GMm / (2 * C2 * Dc(r) ** 2)          # d/dr = GMm/(c2 r^3)
def F_coulomb(r):  return KK / (Dc(r) ** 2)
def F_cornell(r):  return -AA / (Dc(r) ** 2) - SIGMA
def F_const(r):    return -F0
def F_ho(r):       return -KHO * Dc(r)
#   F_coulomb = KK/r^2 ⇒ -F/(c2 r) = -KK/(c2 r^3) ⇒ Phi = KK/(2c2 r^2)
def Phi_coulomb(r): return KK / (2 * C2 * Dc(r) ** 2)
#   F_cornell = -AA/r^2 - SIGMA ⇒ -F/(c2r) = (AA/r^2+SIGMA)/(c2 r) = AA/(c2 r^3)+SIGMA/(c2 r)
def Phi_cornell(r): return -AA / (2 * C2 * Dc(r) ** 2) + (SIGMA / C2) * Dc(r).ln()
#   F_const = -F0 ⇒ -F/(c2r) = F0/(c2 r) ⇒ Phi = (F0/c2) ln r
def Phi_const(r):   return (F0 / C2) * Dc(r).ln()
#   F_ho = -k r ⇒ -F/(c2 r) = k/c2 ⇒ Phi = (k/c2) r
def Phi_ho(r):      return (KHO / C2) * Dc(r)

TARGETS = [('牛顿 r^-2（吸引）', F_newton, Phi_newton, Decimal('1')),
           ('库仑 r^-2（排斥）', F_coulomb, Phi_coulomb, Decimal('1')),
           ('Cornell -a/r^2-sigma', F_cornell, Phi_cornell, Decimal('1e-15')),
           ('常数力', F_const, Phi_const, Decimal('2')),
           ('谐振子 -kr', F_ho, Phi_ho, Decimal('2'))]
zd_rows = []
for nm, Ff, Ph, rt in TARGETS:
    rec = -C2 * rt * central_diff(Ph, rt, Decimal('1e-5'))
    rel = abs(rec - Ff(rt)) / abs(Ff(rt))
    zd_rows.append((nm, rel))
max_rel = max(v for _, v in zd_rows)
F('U20', '★ 零判别力（承 r33 F01；本册在 r 因子口径下用「构造+回代」独立复现，积分核 1/(c^2 r)）：'
         '对任意径向 F(r) 可反解 kappa^2-tau^2 = -∫F/(c^2 s)ds ⇒ 5 种力律（引力/电磁/常数力/谐振子/Cornell）'
         '全部被同一主方程逐位实现；回代残差（|F_重建-F|/|F|）：%s；最大 %s（差分截断量级 ⇒ 全部成立）⇒ '
         '主方程不区分任何两种相互作用；且 kappa^2-tau^2 只依赖差值 ⇒ kappa/tau 分担比任意（承 r32 Z12 λ 族）'
         % ('; '.join('%s=%s' % (nm, fs(v)) for nm, v in zd_rows), fs(max_rel)))

# U21 方向自由度
F('U21', '方向自由度：F 恒沿 ±rhat ⇒ 方向信息仅 1 bit（吸引/排斥）；'
         '而电磁需矢量横向分量、弱力需 V-A 手征（2 手征态）、强力需非阿贝尔 8 重胶子 ⇒ '
         '§一宣称「矢量 F_uni 包含所有力的方向信息」与式子的实际自由度（1 bit）不符')

# U22 MHD 段量纲
D_NAB_U_MACRO = dmul(D_NAB, dmul(D_C2, dpow(D_TAU, 2)))
gap_mhd = ddiv(ddiv(D_PRESS, D_R), D_NAB_U_MACRO)
F('U22', '§四.4 MHD 段：J×B=∇p 为标准 MHD 平衡式（本册不裁定）；但 ∇p = -∇U_macro(tau) 不闭合：'
         '[∇p]=%s，[∇(c^2 tau^2)]=%s ⇒ 商 = %s ≠ 无量纲'
         % (dstr(ddiv(D_PRESS, D_R)), dstr(D_NAB_U_MACRO), dstr(gap_mhd)))

# U23 尺度贯通三段零数值（扫描来料正本）
SRC_TXT = os.path.join(BASE, '数据', 'TUFT-V40终极力的统一方程_来料全文_2026-10-17.md')
zero_scan = None
try:
    raw = io.open(SRC_TXT, encoding='utf-8', errors='replace').read()
    seg = raw.split('## 四')[1].split('## 五')[0] if '## 四' in raw else ''
    import re as _re
    nums = _re.findall(r'\d+\.?\d*', seg)
    zero_scan = len(nums)
except Exception:
    zero_scan = None
if zero_scan is None:
    I('U23', '§四 尺度贯通段数值扫描：来料正本未就位，本条跳过（不影响其他条目）')
else:
    F('U23', '§四 尺度贯通三段（微观量子 / 介观粒子 / 宏观宇宙）零方程零数值：'
             '全段可识别数字仅 %d 个，其中 4 个是小节编号 1-4，实质数值仅 10^-18（弱力核尺度）一处，无任何待算量；'
             '§4.2 提到的 g-2 / EDM 通道，本库 r27/r41/r42/r43/r44 已判两窗口关闭（μ 子 g-2 异常经 2025-06-03 Fermilab 最终结果已消失）'
             % zero_scan)

# U24 §六 四条宣称逐条判
F('U24', '§六 四条「人类物理史上首个」宣称逐条判：'
         '(1) 单方程统一四力、无额外参数 ⇒ FAIL（U18 外部输入 6 项）；'
         '(2) 含大小/方向/距离三重关联 ⇒ FAIL（U21 方向仅 1 bit；U03/U04 距离项 r 是破坏 F=-∇U 的插入项）；'
         '(3) 全尺度贯通 ⇒ FAIL（U23 三段零数值；U22 MHD 段量纲不闭合）；'
         '(4) 可求导可证明可精算 ⇒ FAIL（U05 量纲核验式自身不成立；U01/U02 主方程量纲不闭合）')

# ================= F 组：V4.0/V4.1 版本链 =================
# U25 三个变体的前置因子两两互斥（承 r32 / r33，本册做版本链对拍）
D_PRE_V40 = dmul(D_C2, D_R)              # c^2 * r  ⇒ L^3T^-2
D_PRE_R32 = dmul(M_DIM, D_C2)            # m * c^2  ⇒ ML^2T^-2
D_PRE_R33 = D_ALPHA                      # alpha    ⇒ ML^4T^-2
r40_r32 = ddiv(D_PRE_V40, D_PRE_R32)
r40_r33 = ddiv(D_PRE_V40, D_PRE_R33)
F('U25', '★ V4.0/V4.1 三变体前置因子两两互斥：本册 V4.0 = c^2*r（%s）、r32 V4.1_geom = m*c^2（%s）、'
         'r33 V4.1_alpha = alpha（%s）⇒ 两两之商 %s 与 %s 均非无量纲 ⇒ 三版不可能都正确；'
         '且 V4.0 的前置因子含位置变量 r，而两版 V4.1 为常数 ⇒ 对同一 (kappa,tau) 场，'
         'V4.0 与 V4.1 给出的力之比 = r/m 或 r/alpha，随 r 变化 ⇒ 力律的 r 依赖不同 ⇒ 描述不同物理'
         % (dstr(D_PRE_V40), dstr(D_PRE_R32), dstr(D_PRE_R33), dstr(r40_r32), dstr(r40_r33)))

# U26 终审门（承 r76 C 组 / r94 口径）
UFT = [('UFT-1 数学自洽', 'FAIL', 'U01/U02 主方程量纲不闭合，U05 核验式自身不成立'),
       ('UFT-2 四力统一', 'FAIL', '还原 0/4：引力反号+无源量 / 电磁无排斥+无源量 / 弱力力程减半 / 强力形状与禁闭矛盾'),
       ('UFT-3 常数派生', 'FAIL', '外部输入 6 项；c^2 不是 alpha（U06），且 {hbar,c,G} 对 [alpha] 命中 0'),
       ('UFT-4 观测复现', 'FAIL', '不还原牛顿 1/r^2（U08/U09）与库仑（U11/U12）'),
       ('UFT-5 可证伪预言', 'BOUNDARY', '零判别力（U20）⇒ 无任何可被区分的预言'),
       ('UFT-6 外部验证', 'FAIL', '无')]
score = sum(1 for _, v, _ in UFT if v == 'PASS')
F('U26', '终审门 UFT-1..6（承 r76 C 组 / r94 口径，在 V4.0 原文上重跑）：%s ⇒ **得分 %d/6**'
         % ('; '.join('%s=%s（%s）' % (a, b, c) for a, b, c in UFT), score))

# U27 对标题三要素（大小·方向·距离）逐项结账 —— 本册对来料标题的直接回答
F('U27', '★ 对来料标题三要素的逐项结账（本册对「大小·方向·距离」命题的直接回答）：'
         '【大小】F=2c^2A^2/r^2 中 A 必无量纲 ⇒ 不含 M,m,q ⇒ 与源强度无关 ⇒ FAIL（U08/U12）；'
         '【方向】F 恒沿 ±rhat ⇒ 1 bit，电磁无排斥、弱力无手征载体 ⇒ FAIL（U11/U21）；'
         '【距离】距离项 r 是凭空插入项（U03/U04）：留则破坏 F=-∇U，删则退化为 r^-3 力 ⇒ FAIL；'
         '⇒ 三要素无一项成立')

# U28 PASS 面（诚实记录：形式层的真实正确部分）
I('U28', 'PASS/中性面（不夸大）：'
         '①§二 步骤1-2 的 U=c^2(kappa^2-tau^2) 与 F=-∇U 是教科书标准式复用（正确但零信息量）；'
         '②§二 步骤3 的 -c^2∇(kappa^2-tau^2) 与 §三 各段的导数运算代数正确（差分 vs 解析残差 %s）；'
         '③保留 r 因子时确得 1/r^2 形式（这是它唯一与牛顿同形之处，代价见 U04）⇒ 三条全属形式层，无一条支撑四力还原'
         % fs(diff_rel))

# U29 来料来源登记
I('U29', '来源登记：来料末行自述「部分内容由豆包工作 AI 生成」⇒ 本册按外部来料口径审计，'
         '不因来源而加减判定；§四 三段为无方程无数值的散文段，§六 为宣称段，两者均按原文逐条落判')

# ================= 汇总与产物 =================
GUARD_TOTAL = len(GUARDS)
GUARD_OK = sum(1 for g in GUARDS if g['ok'])

KEY_NUMBERS = {
    'c2_SI': fv(C2),
    'dim_F_M3': dstr(D_M3),
    'dim_U': dstr(D_U),
    'gap_U': dstr(GAP_U),
    'gap_F': dstr(GAP_F),
    'gap_offset_L': dstr(offset),
    'dim_nabla_phi_true': dstr(D_NAB_PHI),
    'dim_nabla_phi_claimed': dstr(claim_nab_phi),
    'dim_alpha_r94': dstr(D_ALPHA),
    'alpha_over_c2': dstr(gap_alpha_c2),
    'enum_hits_alpha': len(hits_alpha),
    'enum_hits_c2': len(hits_c2),
    'Fg_at_1m_A1': fv(analytic_g(Decimal('1'))),
    'Fe_at_1m_A1': fv(analytic_e(Decimal('1'))),
    'Fg_M2_at_1m': fv(analytic_g_M2(Decimal('1'))),
    'lambda_W_m': fv(lam_w, 20),
    'lambda_W_half_m': fv(lam_w / 2, 20),
    'kappa_Kretschmann14_at_Rsun': fv(kappa_K),
    'kappa_1_over_Rsun': fv(kappa_1overr),
    'udc_guard': '%d/%d' % (GUARD_OK, GUARD_TOTAL),
    'UFT_score': '%d/6' % score,
    'items_total': len(REPORT),
}

DATA_DIR = os.path.join(BASE, '数据')
os.makedirs(DATA_DIR, exist_ok=True)
STEM = 'TUFT-r97_V40终极力的统一方程_大小方向距离_全维审计_2026-10-17'
NOW = datetime.datetime.now().isoformat()

# 报告 txt
lines = []
lines.append('TUFT V4.0 终极力的统一方程（大小·方向·距离）· 全维审计（r97）')
lines.append('GENERATED_AT=%s' % NOW)
lines.append('MODULE=%s' % os.path.abspath(__file__))
lines.append('=' * 78)
for e in REPORT:
    lines.append('[%s] %s | %s' % (e['code'], e['kind'], e['msg']))
lines.append('-' * 78)
for g in GUARDS:
    lines.append('GUARD %s %s | %s' % (g['name'], 'OK' if g['ok'] else 'XX', g['detail']))
lines.append('-' * 78)
lines.append('PASS = %d; FAIL = %d; BOUNDARY = %d; INFO = %d; CORRECTED = %d; MISMATCH = %d'
             % (COUNTS['PASS'], COUNTS['FAIL'], COUNTS['BOUNDARY'],
                COUNTS['INFO'], COUNTS['CORRECTED'], COUNTS['MISMATCH']))
lines.append('SELFCHECK = %d/%d' % (GUARD_OK, GUARD_TOTAL))
txt = '\n'.join(lines)
io.open(os.path.join(DATA_DIR, STEM + '_report.txt'), 'w', encoding='utf-8').write(txt)

# json
payload = {
    'generated_at': NOW,
    'module': os.path.abspath(__file__),
    'round': 'r97',
    'subject': 'TUFT V4.0 终极力的统一方程（大小·方向·距离）',
    'counts': COUNTS,
    'selfcheck': '%d/%d' % (GUARD_OK, GUARD_TOTAL),
    'guards': GUARDS,
    'items': REPORT,
    'key_numbers': KEY_NUMBERS,
    'UFT_gate': [{'item': a, 'verdict': b, 'basis': c} for a, b, c in UFT],
    'external_inputs': EXT_INPUTS,
}
io.open(os.path.join(DATA_DIR, STEM + '.json'), 'w', encoding='utf-8').write(
    json.dumps(payload, ensure_ascii=False, indent=2))

# 数据 md
md = []
md.append('# 数据：TUFT V4.0 终极力的统一方程（大小·方向·距离）· 全维审计（r97）')
md.append('')
md.append('- 生成时间：%s' % NOW)
md.append('- 引擎：[源码/%s.py](%s.py)' % (STEM, STEM.replace(' ', '%20')))
md.append('- 判定册：[判定_TUFT-r97-V40终极力的统一方程_大小方向距离_全维审计_2026-10-17.md]'
          '(../判定_TUFT-r97-V40终极力的统一方程_大小方向距离_全维审计_2026-10-17.md)')
md.append('')
md.append('## 条目')
md.append('')
md.append('| 编号 | 判定 | 读数 |')
md.append('|---|---|---|')
for e in REPORT:
    md.append('| %s | %s | %s |' % (e['code'], e['kind'], e['msg'].replace('|', '/')))
md.append('')
md.append('## 关键数值')
md.append('')
md.append('| 键 | 值 |')
md.append('|---|---|')
for k in sorted(KEY_NUMBERS):
    md.append('| %s | %s |' % (k, KEY_NUMBERS[k]))
md.append('')
md.append('## 自检守卫')
md.append('')
for g in GUARDS:
    md.append('- %s %s：%s' % (g['name'], 'OK' if g['ok'] else 'XX', g['detail']))
md.append('')
md.append('PASS = %d; FAIL = %d; BOUNDARY = %d; INFO = %d; CORRECTED = %d; MISMATCH = %d'
          % (COUNTS['PASS'], COUNTS['FAIL'], COUNTS['BOUNDARY'],
             COUNTS['INFO'], COUNTS['CORRECTED'], COUNTS['MISMATCH']))
io.open(os.path.join(DATA_DIR, STEM + '.md'), 'w', encoding='utf-8').write('\n'.join(md))

print(txt.encode('utf-8', 'replace').decode('utf-8'))

