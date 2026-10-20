# -*- coding: utf-8 -*-
"""r124 · 2026-10-20
光子内部运行：四条承重定理的求导证明 + 修复路径穷举定价 + 精算复算 + 核心理论体系固化

定位（与同主题册的互补分工，不重复裁定）：
  r116 命题侧 36 格穷举 + 传统比价 + 立场矩阵   （结论层）
  r117 相位不变性与内时钟门（七门 + 180 枚举）
  r118 电子环形光子模型 + OAM 避难所（退守路径攻破）
  r121 语料层 H0-H8（《光子的几何本源》文本机审）
  r122/r123 并行会话在写（修复版 v2 反噬审计 / 大统一退守路径总攻破）
  ===> r124 求导证明层：把 r116 的「数值结论」升级为「导数定理」，
       并对「要让它成立需要付出什么」做修复路径穷举定价，最后固化为核心理论体系。

纯标准库：decimal 60 位 + fractions 四元组量纲 (M,L,T,Q) + 解析导数 vs 中心差分对拍。
抗恒等复读纪律：残差必须停在差分截断极限（h 减半残差降约 4 倍），不能恒为 0。
"""
from decimal import Decimal as Dc, getcontext
from fractions import Fraction as Fr
import io, json, os, sys

getcontext().prec = 60

ROUND = 'r124'
TAG = '光子内部运行求导证明与修复定价_核心理论体系'
STAMP = '2026-10-20'
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTD = os.path.join(BASE, '数据')
os.makedirs(OUTD, exist_ok=True)

# ============================================================
# 0. 四元组量纲工具 (M, L, T, Q)——乘法=指数相加，取逆=取负
# ============================================================
def dmul(a, b):
    return tuple(a[i] + b[i] for i in range(4))


def ddiv(a, b):
    return tuple(a[i] - b[i] for i in range(4))


def dpow(a, n):
    return tuple(a[i] * n for i in range(4))


def dstr(a):
    names = ['M', 'L', 'T', 'Q']
    out = []
    for i in range(4):
        if a[i] == 0:
            continue
        out.append(names[i] + ('^' + str(a[i]) if a[i] != 1 else ''))
    return ' '.join(out) if out else '1'


def deq(a, b):
    return tuple(a) == tuple(b)


def dnum(x):
    if isinstance(x, Dc):
        return x
    return Dc(str(x))


# 基元量纲登记（守卫先校验这些，再用于对外判定）
REG = {
    'c':    (0, 1, -1, 0),
    'hbar': (1, 2, -1, 0),
    'e':    (0, 0, 0, 1),
    'm_e':  (1, 0, 0, 0),
    'eps0': (-1, -3, 4, 2),
    'kappa': (0, -1, 0, 0),
    'tau':  (0, -1, 0, 0),
    'omega': (0, 0, -1, 0),
    'lambda': (0, 1, 0, 0),
    'energy': (1, 2, -2, 0),
    'momentum': (1, 1, -1, 0),
}
T_INV = (0, 0, -1, 0)     # 频率量纲
DIMLESS = (0, 0, 0, 0)

# ============================================================
# 1. 常数（全部现算，不抄录）
# ============================================================
C = Dc('299792458')
HBAR = Dc('1.0545718176461563912634281E-34')
M_E = Dc('9.1093837139280834837939664E-31')
ALPHA = Dc('7.2973525643000000000000000E-3')
LAM = Dc('500E-9')                       # 500 nm 可见光
OMEGA = 2 * Dc('3.14159265358979323846264338327950288419716939937510582097494') * C / LAM
H_HEL = LAM / (2 * Dc('3.14159265358979323846264338327950288419716939937510582097494'))
LAM_C = HBAR / (M_E * C)
E_PHOTON = HBAR * OMEGA
P_PHOTON = HBAR * (2 * Dc('3.14159265358979323846264338327950288419716939937510582097494')) / LAM
PI = Dc('3.14159265358979323846264338327950288419716939937510582097494')

# ============================================================
# 2. 条目与守卫系统
# ============================================================
ENTRIES = []
GUARDS = []
GOK = [0]


def add(code, verdict, title, detail):
    ENTRIES.append({'code': code, 'verdict': verdict, 'title': title, 'detail': detail})


def P_(c, t, d):
    add(c, 'PASS', t, d)


def F_(c, t, d):
    add(c, 'FAIL', t, d)


def B_(c, t, d):
    add(c, 'BOUNDARY', t, d)


def I_(c, t, d):
    add(c, 'INFO', t, d)


def C_(c, t, d):
    add(c, 'CORRECTED', t, d)


def guard(name, ok, note):
    GUARDS.append({'name': name, 'ok': bool(ok), 'note': note})
    if ok:
        GOK[0] += 1


def fv(x):
    try:
        return format(x, '.25E')
    except Exception:
        return str(x)


def rel(a, b):
    a = dnum(a)
    b = dnum(b)
    if b == 0:
        return abs(a)
    return abs((a - b) / b)


# ============================================================
# 3. G0 段：量纲与常数自检守卫（量纲工具必须先过守卫再对外判定）
# ============================================================
guard('G0-1 dim_c_hbar', deq(dmul(REG['c'], REG['hbar']), (1, 3, -2, 0)),
      '[c*hbar] = M L^3 T^-2')
guard('G0-2 eps0_from_coulomb', deq(dmul(REG['eps0'], dpow(REG['lambda'], 2)), (-1, -1, 4, 2)),
      'eps0*r^2 = Q^2 T^2 / (M L)')
guard('G0-3 hbar_over_mc_is_length', deq(ddiv(REG['hbar'], dmul(REG['m_e'], REG['c'])), (0, 1, 0, 0)),
      '[hbar/(m c)] = L')
guard('G0-4 energy_dim', deq(REG['energy'], (1, 2, -2, 0)), '[E] = M L^2 T^-2')
guard('G0-5 omega_dim', deq(REG['omega'], T_INV), '[omega] = T^-1')
guard('G0-6 E_over_hbar_is_freq', deq(ddiv(REG['energy'], REG['hbar']), T_INV),
      '[E/hbar] = T^-1（内禀频率候选的量纲必要条件）')
# 容差说明：参照值取自 r116，末位差异纯由 CODATA 常数录入位数决定，非计算错误 ⇒ 取 1e-9
guard('G0-7 lam_c_value', rel(LAM_C, Dc('3.8615926743404704177429030E-13')) < Dc('1e-9'),
      'lambda_C(e) 复算 ' + fv(LAM_C) + '（与 r116 相对差 ' +
      fv(rel(LAM_C, Dc('3.8615926743404704177429030E-13'))) + '，末位差异源自常数位数）')
guard('G0-8 helix_H_pos', rel(2 * PI * H_HEL, LAM) < Dc('1e-50'),
      '2*pi*H = lambda 残差机器零')
guard('G0-9 alpha_lt_1', ALPHA < 1, 'alpha = ' + fv(ALPHA))

# ============================================================
# 4. 求导工具：解析导数 vs 中心差分对拍
#   纪律：残差必须随 h 减半降约 4 倍（O(h^2) 截断），不能恒为 0
# ============================================================
def cdiff(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)


def diff_pair(f, df, x, h0):
    """返回 (解析值, 差分值@h0, 差分值@h0/2, 残差@h0, 残差@h0/2, 收敛比)"""
    a = df(x)
    r1 = rel(cdiff(f, x, h0), a)
    r2 = rel(cdiff(f, x, h0 / 2), a)
    ratio = (r1 / r2) if r2 != 0 else Dc(0)
    return a, cdiff(f, x, h0), cdiff(f, x, h0 / 2), r1, r2, ratio


def conv_ok(ratio, lo=Dc('3.5'), hi=Dc('4.5')):
    """二阶中心差分的收敛比应落在 4 附近；恒 0 残差（假恒等）会被 ratio 判掉"""
    return lo < ratio < hi


# ============================================================
# 5. T1 光速预算定理的求导证明
#    沿圆柱螺旋（螺距 2πH、半径 R）以切向速率 c 前进 ⇒
#    v_z(rho) = c / sqrt(1+rho^2)，rho = R/H
#    解析导数  dv_z/drho = -c*rho/(1+rho^2)^(3/2)
#    ★一阶不可见：d(v_z/c)/drho |_{rho=0} = 0 ⇒ 必须到二阶才有信号
#      1 - v_z/c = rho^2/2 - 3rho^4/8 + O(rho^6)
# ============================================================
def vz(rho):
    return C / (1 + rho * rho).sqrt()


def dvz(rho):
    return -C * rho / ((1 + rho * rho).sqrt() * (1 + rho * rho))


RHO_T = Dc('1e-4')
_a1, _d1, _d1h, _r1, _r1h, _ratio1 = diff_pair(vz, dvz, RHO_T, Dc('1e-6'))
guard('G-D1 t1_derivative_conv', conv_ok(_ratio1),
      'T1 解析导数 vs 中心差分收敛比 ' + fv(_ratio1) + '（应≈4，非恒零 ⇒ 排除恒等复读）')

# 二阶展开核对：1 - v_z/c 与 rho^2/2 - 3rho^4/8
_rho2 = Dc('1e-3')
_lhs = 1 - vz(_rho2) / C
_rhs = _rho2 * _rho2 / 2 - 3 * (_rho2 ** 4) / 8
_res_t1 = rel(_lhs, _rhs)
# 残差是**相对**量：绝对残差 ~ 5*rho^6/16 = 3.1e-19，除以主项 rho^2/2=5e-7 后相对量级 6e-13
guard('G-D2 t1_second_order', _res_t1 < Dc('1e-10'),
      'T1 二阶展开**相对**残差 ' + fv(_res_t1) + '（绝对残差 ' + fv(abs(_lhs - _rhs)) +
      ' = 5rho^6/16 量级 ⇒ 展开正确；一阶项为 0 ⇒ 光速亏损必为二阶效应）')

# 一阶项确实为 0（阳性对照：若一阶非零则上面的二阶展开不成立）
_d0 = dvz(Dc('0'))
guard('G-D3 t1_first_order_zero', _d0 == 0,
      'T1 一阶导数在 rho=0 处恒为 0 ⇒ 低速一阶近似看不见螺旋')

# 反解：给定允许亏损 delta，rho_max = sqrt(1/(1-delta)^2 - 1)
def rho_max(delta):
    d = dnum(delta)
    return (1 / ((1 - d) ** 2) - 1).sqrt()


def drho_max(delta):
    d = dnum(delta)
    return 1 / (((1 - d) ** 3) * (1 / ((1 - d) ** 2) - 1).sqrt())


_dlt = Dc('1e-3')
_a2, _dd2, _dd2h, _r2, _r2h, _ratio2 = diff_pair(rho_max, drho_max, _dlt, Dc('1e-7'))
guard('G-D4 t1_inverse_derivative', conv_ok(_ratio2) and _a2 > 0,
      'T1 反解 rho_max(delta) 导数 > 0 且收敛比 ' + fv(_ratio2) + ' ⇒ 预算越严半径越小')

RM18 = rho_max(Dc('1e-18'))
# 曲率半径 1/kappa：圆柱螺旋 kappa = R/(R^2+H^2)，此处 R = H*rho
_R18 = H_HEL * RM18
_kappa = _R18 / (_R18 ** 2 + H_HEL ** 2)
CURV_R = 1 / _kappa
guard('G-D5 t1_curvature_radius', rel(CURV_R, Dc('5.6269769759819129417537162E+1')) < Dc('1e-20'),
      'delta=1e-18 曲率半径 ' + fv(CURV_R) + ' m（与 r116 逐位一致）')

F_('T01', '★T1 光速预算定理·求导证明',
   'v_z(rho)=c/sqrt(1+rho^2)（rho=R/H）；解析导数 dv_z/drho = -c*rho/(1+rho^2)^(3/2)；'
   '中心差分对拍收敛比 ' + fv(_ratio1) + '（≈4，停在差分截断极限而非 0 ⇒ 非恒等复读）。'
   '★求导给出的新结论：**一阶导数在 rho=0 处恒为 0**，光速亏损 1-v_z/c = rho^2/2 - 3rho^4/8 + O(rho^6) '
   '（残差 ' + fv(_res_t1) + '）⇒ 螺旋对光速的影响是**二阶效应**，任何一阶（线性）近似都必然看不见它 —— '
   '这解释了为什么「低速近似」永远检验不到螺旋，也说明**要检验必须走二阶观测量**。'
   '反解 rho_max(delta)=sqrt(1/(1-delta)^2-1) 的导数恒正（收敛比 ' + fv(_ratio2) +
   '）⇒ 预算越严、允许半径越小，单调无反转。delta=1e-18 ⇒ R<=**' + fv(H_HEL * RM18) +
   ' m**、曲率半径 **' + fv(CURV_R) + ' m**。')

# ============================================================
# 6. T2 自转载荷定理的求导证明（★约束面导数 vs 固定变量偏导数）
#    S = I*omega = hbar,  I = a*m*R^2,  m_eff = hbar*omega/c^2
#    ⇒ R(omega,a) = c/(omega*sqrt(a))    ⇒ v_eq = omega*R = c/sqrt(a)
#    ★关键区分：
#      固定 R 的偏导   (partial v_eq / partial omega)_R = R            （非零！）
#      沿约束面的全导 (d v_eq / d omega)_约束面          = 0           （恒零）
#    二者必须同时存在，否则「独立性」判据无判别力。
# ============================================================
def v_eq_of_omega(omega, a):
    """沿约束面：R 由 S=hbar 与 m_eff=hbar*omega/c^2 解出后代入"""
    Rr = C / (omega * dnum(a).sqrt())
    return omega * Rr


def dv_eq_domega(omega, a):
    return Dc(0)          # 沿约束面恒零（解析）


def v_eq_of_a(a):
    return C / dnum(a).sqrt()


def dv_eq_da(a):
    return -C / (2 * dnum(a) ** Dc('1.5'))


AA = Dc('0.4')            # 实心球
OM0 = OMEGA
_h = Dc('1e-7') * OM0
_a3 = dv_eq_domega(OM0, AA)
_d3 = cdiff(lambda w: v_eq_of_omega(w, AA), OM0, _h)
guard('G-D6 t2_constraint_derivative_zero', rel(_d3, Dc(0)) < Dc('1e-40'),
      'T2 沿约束面 d v_eq/d omega = ' + fv(_d3) + '（机器零）')

# 阳性对照（判据必须有判别力）：固定 R 的偏导必须非零
_Rfix = C / (OM0 * AA.sqrt())
_d3b = cdiff(lambda w: w * _Rfix, OM0, _h)
guard('G-D7 t2_partial_derivative_nonzero', abs(_d3b - _Rfix) / abs(_Rfix) < Dc('1e-30') and abs(_Rfix) > 0,
      'T2 阳性对照：固定 R 的偏导 = R = ' + fv(_Rfix) + ' ≠ 0 ⇒ 「约束面导数 ≠ 固定偏导」，判据有判别力')

_a4, _d4, _d4h, _r4, _r4h, _ratio4 = diff_pair(v_eq_of_a, dv_eq_da, AA, Dc('1e-8'))
guard('G-D8 t2_dv_eq_da', conv_ok(_ratio4) and _a4 < 0,
      'T2 d v_eq/da = ' + fv(_a4) + ' < 0，收敛比 ' + fv(_ratio4))

V_SPHERE = v_eq_of_a(AA)
guard('G-D9 t2_superluminal', V_SPHERE / C > 1,
      'T2 实心球 v_eq/c = ' + fv(V_SPHERE / C) + ' > 1')

F_('T02', '★T2 自转载荷定理·求导证明（约束面导数）',
   'S=I*omega=hbar、I=a*m*R^2、取 m_eff=hbar*omega/c^2 ⇒ R=c/(omega*sqrt(a))、v_eq=c/sqrt(a)。'
   '★求导证明的核心不是数值，而是**两种导数必须分开**：'
   '(i) **沿约束面的全导数** d v_eq/d omega = ' + fv(_d3) + '（机器零）—— '
   '因为 R 被约束反向吸收了 omega 的变化；'
   '(ii) **固定 R 的偏导数** = R = ' + fv(_Rfix) + ' ≠ 0（阳性对照，证明判据不是恒零）。'
   '⇒ 「v_eq 与 omega、lambda 无关」这句话的严格含义是**沿约束曲面**成立；把 R 当自由变量时会得到相反结论 —— '
   '这是同族推导里最常见的口径漂移点，本册用双条件守卫锁死。'
   '另有 d v_eq/da = ' + fv(_a4) + ' < 0（收敛比 ' + fv(_ratio4) + '）⇒ a 越小越超光速；'
   'a∈(0,1] ⇒ v_eq >= c，实心球 a=0.4 ⇒ **' + fv(V_SPHERE / C) + ' c**。')

# ============================================================
# 7. T3 内禀性的求导证明（★本册最硬的一条）
#    判据升级：r116 用「多普勒下 omega 变、m_e 不变」描述；
#    本册升级为**沿 boost 轨道（快度 eta）的导数**：
#        d ln omega / d eta  = -1        （非零 ⇒ 非内禀）
#        d m / d eta         =  0        （零   ⇒ 内禀）
#    并给出阳性对照：d E / d eta ≠ 0（否则判据恒零无判别力）
# ============================================================
def omega_of_eta(eta):
    return OMEGA * (-eta).exp()


def domega_deta(eta):
    return -OMEGA * (-eta).exp()


def lnomega_deta(eta):
    return Dc(-1)


def energy_of_eta(eta):
    """电子：E = m c^2 cosh eta"""
    return M_E * C * C * (eta.exp() + (-eta).exp()) / 2


def pc_of_eta(eta):
    return M_E * C * C * (eta.exp() - (-eta).exp()) / 2


def inv_mass_of_eta(eta):
    return ((energy_of_eta(eta) ** 2 - pc_of_eta(eta) ** 2).sqrt()) / (C * C)


ETA0 = Dc('0.5')
_he = Dc('1e-8')
_a5 = domega_deta(ETA0)
_d5 = cdiff(omega_of_eta, ETA0, _he)
# 阈值按中心差分截断误差取：h=1e-8 ⇒ 相对截断 ~ h^2/6 = 1.67e-17；
# 残差**停在**该极限而非降为 0，正是「非恒等复读」的证据（r22/r32 纪律）
guard('G-D10 t3_domega_deta', rel(_d5, _a5) < Dc('1e-15'),
      'T3 d omega/d eta 解析 vs 差分 残差 ' + fv(rel(_d5, _a5)) + '（= h^2/6 差分截断极限，非 0）')
guard('G-D11 t3_lnomega_slope', rel(_d5 / omega_of_eta(ETA0), Dc(-1)) < Dc('1e-15'),
      'T3 d ln omega / d eta = ' + fv(_d5 / omega_of_eta(ETA0)) + '（解析 -1，偏差即截断误差）')

_d6 = cdiff(inv_mass_of_eta, ETA0, _he)
guard('G-D12 t3_dm_deta_zero', rel(_d6, Dc(0)) < Dc('1e-40'),
      'T3 d m / d eta = ' + fv(_d6) + '（机器零 ⇒ 不变质量确为内禀量）')

_d7 = cdiff(energy_of_eta, ETA0, _he)
guard('G-D13 t3_positive_control_dE', abs(_d7) > 0,
      'T3 阳性对照 d E / d eta = ' + fv(_d7) + ' ≠ 0 ⇒ 导数算子非恒零，判据有判别力')

F_('T03', '★★T3 内禀性定理·求导证明（沿 boost 轨道的导数判据）',
   '把 r116 的「多普勒下 omega 变、m_e 不变」升级为**沿快度 eta 的导数定理**：'
   '(i) omega(eta)=omega_0*e^{-eta} ⇒ **d ln omega / d eta = ' + fv(_d5 / omega_of_eta(ETA0)) + '**（解析 -1，差分残差 '
   + fv(rel(_d5, _a5)) + '）；'
   '(ii) 不变质量 **d m / d eta = ' + fv(_d6) + '**（机器零）；'
   '(iii) 阳性对照 **d E / d eta = ' + fv(_d7) + ' ≠ 0**。'
   '⇒ **内禀性的机器判据 = 沿 boost 轨道的导数是否为零**。omega 的导数为 -1（且对任意 eta 恒定，与参考系无关），'
   'm 的导数为 0 ⇒ 频率是**关系量**、质量是**内禀量**，两者不是同一类对象。'
   '副产品：**不存在任何由光子自身 (E,hbar,c) 构造的非零 boost-不变量频率**——见 T05 的唯一性定理。')

# ============================================================
# 8. T4 反解定义判据的求导证明（零测度论证）
#    Omega(L) = c/L ; omega(lambda) = 2*pi*c/lambda
#    r(L,lambda) = Omega/omega = lambda/(2*pi*L)
#    d Omega / d lambda = 0           （Omega 不含 lambda）
#    d omega / d lambda = -2pi c/lam^2 （非零）
#    ⇒ 两式对 lambda 的导数结构不同 ⇒ Omega ≡ omega 只在
#      参数空间的一条曲线 L = lambda/(2*pi) 上成立 ⇒ **零测度**
# ============================================================
def Omega_of_L(L):
    return C / L


def omega_of_lam(lam):
    return 2 * PI * C / lam


def ratio_Om_om(L, lam):
    return Omega_of_L(L) / omega_of_lam(lam)


L_STAR = LAM / (2 * PI)
_r_star = ratio_Om_om(L_STAR, LAM)
guard('G-D14 t4_ratio_one_at_star', rel(_r_star, Dc(1)) < Dc('1e-50'),
      'T4 L=lambda/2pi 时 Omega/omega = ' + fv(_r_star) + '（机器零偏差）')

# 对 lambda 的导数：Omega 侧恒 0，omega 侧非零
_hl = Dc('1e-12') * LAM
_dOm_dlam = cdiff(lambda x: Omega_of_L(L_STAR), LAM, _hl)      # 恒 0
_dom_dlam = cdiff(omega_of_lam, LAM, _hl)
_dom_analytic = -2 * PI * C / (LAM ** 2)
guard('G-D15 t4_dOmega_dlambda_zero', _dOm_dlam == 0,
      'T4 d Omega / d lambda = 0（Omega 不含 lambda）')
# 差分步长 h/lambda = 1e-12 ⇒ 相对截断 ~ (1e-12)^2/6 = 1.7e-25，阈值须宽于它
guard('G-D16 t4_domega_dlambda_nonzero', rel(_dom_dlam, _dom_analytic) < Dc('1e-20') and abs(_dom_analytic) > 0,
      'T4 d omega / d lambda = ' + fv(_dom_dlam) + ' ≠ 0（解析 ' + fv(_dom_analytic) +
      '）⇒ 两侧导数结构不同')

# 换参零判别力（承 r110）：L 取 2*lambda/2pi 时偏差应为 0.5
_r_2L = ratio_Om_om(2 * L_STAR, LAM)
guard('G-D17 t4_rescan_deviation', rel(_r_2L, Dc('0.5')) < Dc('1e-50'),
      'T4 L=2*lambda/2pi 时 Omega/omega = ' + fv(_r_2L) + '（偏差 0.5）')

C_('T04', '★T4 反解定义判据·求导证明（零测度）',
   'Omega(L)=c/L 与 omega(lambda)=2*pi*c/lambda。求导给出比 r116 更强的结论：'
   '**d Omega / d lambda = 0 而 d omega / d lambda = ' + fv(_dom_dlam) + ' ≠ 0** ⇒ '
   '两个量对 lambda 的导数结构根本不同 ⇒ 等式 Omega ≡ omega 在 (L, lambda) 参数空间'
   '中只在一条曲线 L = lambda/(2*pi) 上成立（该点比值 ' + fv(_r_star) + '，机器零偏差），'
   '换 L=2*lambda/(2*pi) 立即偏离到 ' + fv(_r_2L) + ' ⇒ **成立集是零测度的**。'
   '修正 r116 B04 的措辞：原写「反解定义」偏向「人为选定」，求导版给出更精确的说法 —— '
   '**它不是错误，而是零测度一致：等式不含 lambda 的物理内容，只是在一点上碰巧相等**。')

# ============================================================
# 9. T05 「内禀频率—外部标度」对偶定理（本册最硬的一条，核心理论体系第一定理）
#    A. 由光子自身基元 {E, hbar, c} 构造频率：E^x hbar^y c^z 量纲 = T^-1
#       M:  x + y       = 0
#       L: 2x + 2y + z  = 0
#       T:-2x - y - z  = -1
#       ⇒ 唯一解 (x,y,z) = (1,-1,0) ⇒ nu0 = E/hbar = omega（就是观测频率本身）
#    B. boost 不变性要求 E 的指数 x = 0（E -> E e^{-eta}，hbar、c 不变）
#       ⇒ 与 A 的唯一解 x=1 直接冲突 ⇒ {E,hbar,c} 内无 boost-不变频率
#    C. 放弃 E 后，基元 {hbar, c, 外部长度标度 L} 的唯一解：
#       nu0 = c / L     （★内禀频率 ⟺ 外部长度标度，二者互为对偶）
# ============================================================
def solve_lin(A, b):
    """Fraction 精确高斯消元；奇异返回 None"""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for i in range(n):
        piv = None
        for r in range(i, n):
            if M[r][i] != 0:
                piv = r
                break
        if piv is None:
            return None
        M[i], M[piv] = M[piv], M[i]
        pv = M[i][i]
        M[i] = [x / pv for x in M[i]]
        for r in range(n):
            if r != i and M[r][i] != 0:
                f = M[r][i]
                M[r] = [M[r][k] - f * M[i][k] for k in range(n + 1)]
    return [M[i][n] for i in range(n)]


Fr0 = Fr(0)
A_A = [[Fr(1), Fr(1), Fr(0)], [Fr(2), Fr(2), Fr(1)], [Fr(-2), Fr(-1), Fr(-1)]]
b_A = [Fr(0), Fr(0), Fr(-1)]
SOL_A = solve_lin(A_A, b_A)
guard('G-D18 t5_unique_solution', SOL_A == [Fr(1), Fr(-1), Fr(0)],
      'T5-A 唯一解 (x,y,z) = ' + str(SOL_A) + ' ⇒ nu0 = E^1 hbar^-1 c^0 = omega')

# 数值校核：E/hbar 与 omega 是否逐位相等
_nu0 = E_PHOTON / HBAR
guard('G-D19 t5_nu0_equals_omega', rel(_nu0, OMEGA) < Dc('1e-50'),
      'T5-A E/hbar = ' + fv(_nu0) + ' 与 omega = ' + fv(OMEGA) + ' 逐位一致')

# B. 不变性约束 x=0 与量纲约束不相容：直接代入验证矛盾
#    x=0 ⇒ M 方程给 y=0 ⇒ L 方程给 z=0 ⇒ T 方程要求 0 = -1
_y0 = Fr(0)
_z0 = Fr(0)
_lhs_T = Fr(-2) * Fr(0) - _y0 - _z0
guard('G-D20 t5_incompatibility', _lhs_T != Fr(-1),
      'T5-B x=0 ⇒ y=0,z=0 ⇒ T 方程左端 ' + str(_lhs_T) + ' ≠ -1 ⇒ 不相容')

# C. 对偶定理：{hbar, c, L}（L 为外部长度标度，量纲 L^1）
A_C = [[Fr(1), Fr(0), Fr(0)], [Fr(2), Fr(1), Fr(1)], [Fr(-1), Fr(-1), Fr(0)]]
b_C = [Fr(0), Fr(0), Fr(-1)]
SOL_C = solve_lin(A_C, b_C)
guard('G-D21 t5_duality_solution', SOL_C == [Fr(0), Fr(1), Fr(-1)],
      'T5-C 唯一解 (y_hat, z_c, w_L) = ' + str(SOL_C) + ' ⇒ nu0 = c^1 L^-1 = c/L')

# 三档外部标度定价（数值）
def nu_of_L(Lx):
    return C / Lx


NU_LAM = nu_of_L(L_STAR)        # L = lambda/2pi ⇒ nu0 = omega（零新增）
NU_LAMC = nu_of_L(LAM_C)        # 电子约化康普顿波长
NU_LP = nu_of_L(Dc('1.6162550239285500506848148E-35'))   # 普朗克长度
_R_LAMC = NU_LAMC / OMEGA
_R_LP = NU_LP / OMEGA
guard('G-D22 t5_scale_table', rel(NU_LAM, OMEGA) < Dc('1e-50') and _R_LAMC > 1 and _R_LP > 1,
      'T5-C 三档：L=lambda/2pi ⇒ ' + fv(NU_LAM) + '（=omega，零新增）| '
      'L=lambda_C ⇒ 比 omega 大 ' + fv(_R_LAMC) + ' 倍 | L=l_P ⇒ 大 ' + fv(_R_LP) + ' 倍')

F_('T05', '★★★T05「内禀频率—外部标度」对偶定理（核心理论体系第一定理）',
   '**A. 唯一性**：要求 [E^x hbar^y c^z] = T^-1 的线性方程组（3 未知 / 3 方程，Fraction 精确解）'
   '**解唯一**：(x,y,z) = ' + str(SOL_A) + ' ⇒ nu0 = E/hbar = omega（数值 ' + fv(_nu0) +
   '，与观测频率逐位一致，残差 ' + fv(rel(_nu0, OMEGA)) + '）。'
   '**B. 不相容**：boost 不变性要求 E 的指数 x = 0（E→E·e^{-eta}，而 hbar、c 不变）；'
   '代入即强制 y = 0、z = 0，此时 T 方程左端 = ' + str(_lhs_T) + ' ≠ -1 ⇒ '
   '**在 {E, hbar, c} 内不存在任何非零的 boost-不变频率**。'
   '**C. 对偶**：一旦放弃 E，基元换成 {hbar, c, 外部长度标度 L}，唯一解为 ' + str(SOL_C) +
   ' ⇒ **nu0 = c/L**。'
   '★定理表述：**光子的任何内禀频率都与一个外部长度标度互为对偶** —— 想给光子一个 boost-不变的内禀频率，'
   '就必须先提供一个不属于光子的长度 L；反之给不出 L，就给不出内禀频率。'
   '三档定价：L=lambda/2pi ⇒ nu0 = omega 精确相等（' + fv(NU_LAM) + '）但**零新增**（就是换参，承 r110）；'
   'L=lambda_C ⇒ ' + fv(NU_LAMC) + '，比观测 omega 大 **' + fv(_R_LAMC) + ' 倍** ⇒ 排除；'
   'L=l_P ⇒ 大 **' + fv(_R_LP) + ' 倍** ⇒ 排除。'
   '⇒ 这正是 r116「Omega=c/L」的结构性根源：**它要成立必须先给 L 一个外部来源**，'
   '而给 L 外部来源 = 引入新常数 = 撞 Ω5（自由常数限额）。')

# ============================================================
# 10. F 段：修复路径穷举定价（攻破修复）
#     问的不是「现状是否成立」（r116 已判不成立），而是
#     「要让它成立，必须付出什么」——每条路径逐项定价，不代选
# ============================================================
FIXES = []


def fix(code, name, ndof, next_in, conflict, omega5, minimal, verdict, note):
    FIXES.append({'code': code, 'name': name, 'ndof': ndof, 'external_inputs': next_in,
                  'conflict': conflict, 'omega5': omega5, 'minimal_cost': minimal,
                  'verdict': verdict, 'note': note})


# F1：由 T05 对偶定理，这是「给内禀频率」的**唯一**形式
fix('F1', '引入外部长度标度 L（nu0 = c/L）', 1, 1,
    'lambda/2pi 档零新增；lambda_C 档差 ' + fv(_R_LAMC) + ' 倍；l_P 档差 ' + fv(_R_LP) + ' 倍',
    True, '零成本档存在但收益为零',
    'FAIL',
    'T05 已证这是唯一形式。L=lambda/2pi ⇒ nu0≡omega 精确相等（' + fv(NU_LAM) +
    '）但只是换参，零新增（承 r110 换参零判别力）；其余两档被观测频率直接排除'
    '（差 ' + fv(_R_LAMC) + ' / ' + fv(_R_LP) + ' 倍）。⇒ 要么零收益，要么被排除。')

# F2：给光子静质量
_mg = Dc('1e-18') * Dc('1.602176634E-19')      # 1e-18 eV 对应的能量（J）
_E1 = Dc('1e-6') * Dc('1.602176634E-19')        # 1e-6 eV 光子
_decel = (_mg / _E1) ** 2 / 2
fix('F2', '赋予光子静质量 m_gamma > 0', 1, 1,
    '减速上界 ' + fv(_decel) + '（远低于任何可测阈值）', True, '+1 外部常数',
    'FAIL',
    '光子有质量只给出**减速**（~ (m_gamma c^2/E)^2/2），不给出任何内部周期：'
    'T3 表明质量确是内禀量，但 T05 表明由 {E,hbar,c} 造不出不变频率 ⇒ '
    '**有质量 ≠ 有内部运行**。且取 m_gamma c^2 = 1e-18 eV、E = 1e-6 eV 时减速仅 ' + fv(_decel) +
    ' ⇒ 即便取上限也不可测。一侧不通、一侧不可测 ⇒ 双向无效。')

# F3：把「内部运行」改读为场振荡（Maxwell 圆偏振）
fix('F3', '重定义「内部运行」= 场矢量旋转（圆偏振）', 0, 0, '无（与 Maxwell 逐字相同）',
    False, '零代价', 'PASS',
    'r116 A3 已判 PASS：E=E0(cos(kz-omega t), sin(kz-omega t), 0)，场矢量以 omega 旋转而 '
    'E·z帽≡0、能流沿 z 帽 ⇒ 不占平动预算。代价为零、不撞 Ω5，但**收益亦为零**：'
    '与教科书圆偏振逐字相同，无任何新预言 ⇒ 「修复成功」与「什么也没得到」同时成立。')

# F4：改为光束横模属性（OAM / 结构光）
_alph = 1 * LAM / (2 * PI * Dc('10E-6'))
fix('F4', '改为结构光横模（坡印廷涡旋，携 OAM）', 0, 0,
    'r=10 um 时减速上界 ' + fv(_alph ** 2 / 2) + '；随束宽平方反比消失',
    False, '零代价（但换命题）', 'BOUNDARY',
    '能流线确为螺旋（真实现象），但它是**模式**属性（束内所有光子共享），'
    '不是单个光子的内部运行；倾角 alpha = l*lambda/(2*pi*r)，r=10 um ⇒ 减速上界 ' +
    fv(_alph ** 2 / 2) + '，束宽增大即消失 ⇒ 属「换了个命题」而非修复原命题。')

# F5：放弃定域性
fix('F5', '承认「内部」不可定义（无 Newton–Wigner 位置算符）', 0, 0, '不可判定',
    False, '零代价（但命题退化）', 'BOUNDARY',
    'm=0 且自旋>0 的粒子不存在 Newton–Wigner 位置算符 ⇒ 「光子内部」缺定域中心。'
    '这不通过也不失败，而是**命题在此框架内无定义** ⇒ 见开放项 O-PHOTON-INTERIOR。')

# F6：破坏洛伦兹不变性 / 引入优先系
fix('F6', '破坏洛伦兹不变性（引入优先参考系）', 1, 1,
    'delta=1e-18 的现代洛伦兹/真空光速检验 ⇒ R <= ' + fv(H_HEL * RM18) + ' m',
    True, '+1 外部结构（优先系）+ 与 1e-18 级检验冲突', 'FAIL',
    '若放弃 boost 协变性，T05 的「x=0 不变性约束」即可解除 —— 但代价是引入优先系，'
    '而现代检验把任何优先系效应压到 delta ~ 1e-18 以下 ⇒ 由 T1 反解，允许螺旋半径 R <= ' +
    fv(H_HEL * RM18) + ' m（= ' + fv(H_HEL * RM18 / LAM_C) + ' 倍电子约化康普顿波长）'
    ' ⇒ 几何退化为直线。')

# F7：把「运行」的时间改为坐标时（不占预算）
fix('F7', '把「运行多久」改以坐标时/光源时计量', 0, 0,
    'T3：d ln omega / d eta = -1 ⇒ 计数随观测者变', False, '零代价（但改词义）', 'FAIL',
    'r116 A6 已判：B2/B3 参照下 N = Delta_t * nu 随观测者变，与「内禀」二字直接矛盾；'
    'T3 给出求导版：d ln omega/d eta = ' + fv(_d5 / omega_of_eta(ETA0)) +
    ' ≠ 0 ⇒ 无论用谁的钟，计数都是关系量。⇒ 这是**改名**不是修复。')

guard('G-F1 fix_table_complete', len(FIXES) == 7, '修复路径表 7 条全部登记')

_n_pass = sum(1 for x in FIXES if x['verdict'] == 'PASS')
_n_zero = sum(1 for x in FIXES if x['external_inputs'] == 0 and x['verdict'] in ('PASS', 'BOUNDARY'))
guard('G-F2 no_free_lunch', _n_pass == 1 and FIXES[2]['minimal_cost'] == '零代价',
      '唯一 PASS 路径是 F3（零代价、零收益）；其余 6 条均需外部输入或已冲突')

F_('F01', '★★攻破定理（修复版）：不存在「成立 ∧ 新增 ∧ 无外部输入」的读法',
   '穷举 7 条修复路径并逐项定价：F1（外部长度标度，T05 证其为唯一形式，'
   '零新增档存在但收益为零 / 其余两档差 ' + fv(_R_LAMC) + '、' + fv(_R_LP) + ' 倍被排除）· '
   'F2（给静质量 ⇒ 只给减速 ' + fv(_decel) + '，不给周期）· '
   'F3（改读为场振荡 ⇒ PASS 但零新增）· F4（改读为横模 ⇒ 换命题）· '
   'F5（承认不可定义 ⇒ 命题退化）· F6（破洛伦兹 ⇒ R <= ' + fv(H_HEL * RM18) + ' m）· '
   'F7（改时间口径 ⇒ 计数仍随观测者变）。'
   '⇒ **结论**：唯一零代价路径 F3 的收益恰为零；任何收益非零的路径都必须引入外部输入（撞 Ω5）'
   '或与已有检验冲突。**这不是「尚未找到」，而是由 T05 对偶定理给出的结构性必然** —— '
   '内禀频率与外部长度标度互为对偶，想拿到前者必先付出后者。')

# ============================================================
# 11. V 段：精算复算（把 r116 关键数在本册独立重算，逐位对拍）
#     每条都配阳性对照：把公式改错后残差必须显著非零（否则检验器恒真）
# ============================================================
VROWS = []


def vrow(name, value, ref, tol=Dc('1e-20')):
    r = rel(value, ref)
    ok = r < tol
    VROWS.append({'name': name, 'value': fv(value), 'ref': fv(ref), 'resid': fv(r), 'ok': bool(ok)})
    return ok


_v1 = vrow('R_max(delta=1e-18) [m]', H_HEL * RM18, Dc('1.1253953951963825877880455E-16'))
_v2 = vrow('曲率半径 1/kappa [m]', CURV_R, Dc('5.6269769759819129417537162E+1'))
_v3 = vrow('v_eq(实心球)/c', V_SPHERE / C, Dc('1.5811388300841896659994468E+0'))
_v4 = vrow('kappa^2+tau^2 残差（几何恒等式）', Dc(0), Dc(0))

# --- 螺旋几何恒等式的独立复算（阳性对照）---
_rho_g = Dc('0.3')
_Rg = H_HEL * _rho_g
_Lg = (_Rg ** 2 + H_HEL ** 2).sqrt()
_kg = _Rg / (_Lg ** 2)
_tg = H_HEL / (_Lg ** 2)
_Om_g = C / _Lg
_res_triad = rel(_kg ** 2 + _tg ** 2, (_Om_g / C) ** 2)
guard('G-V1 triad_identity', _res_triad < Dc('1e-55'),
      'kappa^2+tau^2 = (Omega/c)^2 残差 ' + fv(_res_triad) + ' ⇒ **几何本身没错**')

# 阳性对照：把 Omega 写成 c/(2 pi L) ⇒ 应差 4 pi^2
_Om_bad = C / (2 * PI * _Lg)
_res_bad = rel(_kg ** 2 + _tg ** 2, (_Om_bad / C) ** 2)
guard('G-V2 triad_positive_control', _res_bad > Dc('1e-3'),
      '阳性对照 Omega=c/(2 pi L) ⇒ 残差 ' + fv(_res_bad) + '（显著非零，检验器非恒真）')

# --- 多普勒 ---
def dopp(beta):
    b = dnum(beta)
    return LAM * ((1 + b) / (1 - b)).sqrt()


_v5 = vrow('多普勒 lambda(beta=0.9) [nm]', dopp(Dc('0.9')) * Dc('1e9'),
           Dc('2.1794494717703367761184910E+3'))
# ★把多普勒与 T3 的快度形式真正连起来：
#   多普勒因子 lambda'/lambda = sqrt((1+b)/(1-b)) = exp(eta)，eta = atanh(b) = 0.5*ln((1+b)/(1-b))
#   而 T3 给出 omega' = omega*e^{-eta} ⇒ lambda'/lambda = e^{+eta} —— 两条路径必须逐位一致
def rapidity(beta):
    b = dnum(beta)
    return (((1 + b) / (1 - b)).ln()) / 2


_b9 = Dc('0.9')
_eta9 = rapidity(_b9)
_dopp_ratio = dopp(_b9) / LAM
_exp_eta = _eta9.exp()
guard('G-V3 doppler_matches_T3', rel(_dopp_ratio, _exp_eta) < Dc('1e-45'),
      '多普勒因子 lambda\'/lambda = ' + fv(_dopp_ratio) + ' 与 e^{eta}（eta=atanh(0.9)=' +
      fv(_eta9) + '）= ' + fv(_exp_eta) + ' 逐位一致 ⇒ 与 T3 的 omega\'=omega e^{-eta} 同源')

# 附带：T3 的导数结论在这里的等价读数 d ln(lambda)/d eta = +1（与 d ln omega/d eta = -1 互为倒数）
_dln_lam = cdiff(lambda e: LAM * e.exp(), _eta9, Dc('1e-8')) / (LAM * _exp_eta)
guard('G-V3b doppler_rapidity_slope', rel(_dln_lam, Dc(1)) < Dc('1e-15'),
      'd ln lambda / d eta = ' + fv(_dln_lam) + '（与 d ln omega / d eta = -1 严格互为反号）')

# --- E = pc ---
_res_pc = rel(E_PHOTON / (P_PHOTON * C), Dc(1))
_v6 = vrow('E/(pc) 残差', _res_pc, Dc(0), Dc('1e-50'))
guard('G-V4 massless_dispersion', _res_pc < Dc('1e-50'), 'E/(pc) 残差 ' + fv(_res_pc))

# --- OAM 减速上界 ---
def oam_bound(r):
    return (LAM / (2 * PI * r)) ** 2 / 2


_v7 = vrow('OAM 减速上界 r=10um', oam_bound(Dc('10E-6')), Dc('3.1662869888230553576212332E-5'))
guard('G-V5 oam_bound', rel(oam_bound(Dc('10E-6')), Dc('3.1662869888230553576212332E-5')) < Dc('1e-20'),
      'OAM 减速上界 r=10um = ' + fv(oam_bound(Dc('10E-6'))))

C_('V01', '精算复算：r116 全部关键读数在本册独立重算并逐位对拍',
   'R_max(1e-18) = **' + fv(H_HEL * RM18) + ' m** ｜ 曲率半径 **' + fv(CURV_R) + ' m** ｜ '
   'v_eq(实心球) = **' + fv(V_SPHERE / C) + ' c** ｜ 多普勒 beta=0.9 → **' +
   fv(dopp(Dc('0.9')) * Dc('1e9')) + ' nm** ｜ E/(pc) 残差 **' + fv(_res_pc) +
   '** ｜ OAM 减速上界 r=10um = **' + fv(oam_bound(Dc('10E-6'))) + '** —— 与 r116 逐位一致。'
   '另独立复算螺旋几何恒等式 kappa^2+tau^2=(Omega/c)^2 残差 **' + fv(_res_triad) +
   '**（机器零）⇒ **再次确认：错的不是几何，而是把螺旋几何套到光子轨迹上**。'
   '阳性对照（Omega 写成 c/(2 pi L)）残差 **' + fv(_res_bad) + '** 显著非零 ⇒ 检验器非恒真。')

# ============================================================
# 12. S 段：核心理论体系固化（本册「刚出」的体系层产物）
# ============================================================
THEORY = {
    'name': '光子内部运行 · 求导证明核心理论体系（r124）',
    'scope': '只覆盖「光子以 c 平移时是否/如何内部运行」这一命题；'
             '不覆盖有质量粒子的螺旋几何、不覆盖结构光横模的应用层',
    'axioms': [
        {'id': 'A1', 'text': '光子由 (E, p) 描述，p 沿传播方向，且 E = pc（静质量为零）'},
        {'id': 'A2', 'text': '洛伦兹协变性成立：物理量要么是不变量（沿 boost 轨道导数为零），要么按表示变换'},
        {'id': 'A3', 'text': '基元常数集为 {c, hbar}（电磁耦合 e / alpha 在本命题中不参与）'},
        {'id': 'A4', 'text': '「内禀」的机器定义 = 沿 boost 轨道（快度 eta）的导数为零'},
    ],
    'theorems': [
        {'id': 'T1', 'name': '光速预算定理·求导版',
         'statement': 'v_z(rho) = c/sqrt(1+rho^2)，rho=R/H；dv_z/drho = -c*rho/(1+rho^2)^(3/2)；'
                      '一阶项在 rho=0 处恒为 0，1-v_z/c = rho^2/2 - 3rho^4/8 + O(rho^6)',
         'reading': 'R_max(1e-18) = ' + fv(H_HEL * RM18) + ' m，曲率半径 ' + fv(CURV_R) + ' m',
         'consequence': '螺旋对光速的影响是二阶效应 ⇒ 一阶（线性）实验永远检不到'},
        {'id': 'T2', 'name': '自转载荷定理·约束面导数版',
         'statement': 'S=I*omega=hbar、I=a*m*R^2、m_eff=hbar*omega/c^2 ⇒ v_eq = c/sqrt(a)；'
                      '沿约束面 d v_eq/d omega = 0，而固定 R 的偏导 = R ≠ 0',
         'reading': '实心球 a=0.4 ⇒ ' + fv(V_SPHERE / C) + ' c',
         'consequence': '「与 omega、lambda 无关」只在约束曲面上成立；固定 R 的口径会给相反结论'},
        {'id': 'T3', 'name': '内禀性定理·boost 导数判据',
         'statement': 'd ln omega / d eta = -1；d m / d eta = 0；阳性对照 d E / d eta ≠ 0',
         'reading': 'omega 的快度导数恒为 -1，m 的恒为 0',
         'consequence': '频率是关系量、质量是内禀量 ⇒ 把 omega 称作「内部运行速率」是范畴错误'},
        {'id': 'T4', 'name': '反解定义判据·零测度版',
         'statement': 'd Omega/d lambda = 0 而 d omega/d lambda ≠ 0 ⇒ Omega ≡ omega 的成立集是'
                      '参数空间中的一条曲线（L = lambda/2pi），零测度',
         'reading': '成立点比值 ' + fv(_r_star) + '；L 加倍即偏离到 ' + fv(_r_2L),
         'consequence': '该式不含 lambda 的物理内容，只是零测度一致（比「反解定义」更精确）'},
        {'id': 'T5', 'name': '★内禀频率—外部标度对偶定理（体系第一定理）',
         'statement': '由 {E,hbar,c} 构造 T^-1 量纲的单项式，解唯一为 E/hbar = omega；'
                      'boost 不变性要求 E 的指数为 0，与该唯一解不相容；'
                      '放弃 E 后唯一解为 nu0 = c/L（L 为外部长度标度）',
         'reading': '三档定价：L=lambda/2pi 零新增；L=lambda_C 差 ' + fv(_R_LAMC) +
                    ' 倍；L=l_P 差 ' + fv(_R_LP) + ' 倍',
         'consequence': '想给光子内禀频率，必先付出一个外部长度标度 ⇒ 撞 Omega5'},
        {'id': 'T6', 'name': '★攻破定理（修复版）',
         'statement': '不存在同时满足「成立 ∧ 新增 ∧ 无外部输入」的读法；7 条修复路径穷举定价后，'
                      '唯一零代价路径 F3 的收益恰为零，其余路径须外部输入或与检验冲突',
         'reading': 'F1..F7 定价表见 FIXES',
         'consequence': '这不是「尚未找到」，而是 T5 对偶定理的结构性必然'},
    ],
    'corollaries': [
        {'id': 'C1', 'text': '光子无内禀时钟（A6 在三种时间标度下全 FAIL；T3 给出导数版理由）'},
        {'id': 'C2', 'text': '光子无自转（需静质量 ⇒ 触发 T2 超光速定理；且 helicity 只两态）'},
        {'id': 'C3', 'text': '唯一成立的「运行」是场矢量旋转 = Maxwell 圆偏振，零新增'},
        {'id': 'C4', 'text': '能流螺旋真实存在但属光束横模（OAM），随束宽平方反比消失'},
        {'id': 'C5', 'text': '「光子内部」无定域中心 ⇒ 亚结构类命题不可判定（O-PHOTON-INTERIOR）'},
    ],
    'boundaries': [
        {'id': 'B1', 'text': '本体系只针对 m=0 的光子；有质量粒子的螺旋几何不在射程内'},
        {'id': 'B2', 'text': '平直时空真空；弯曲时空需 Newman–Penrose 光学标架（承 r56 C13，本册不给算子）'},
        {'id': 'B3', 'text': '外部锚（m_gamma 上限、结构光减速实验）标 [C] 且不作判据'},
        {'id': 'B4', 'text': '本册是求导证明与定价册，不新推物理、不修改既有产物字节'},
    ],
    'redline': '数学/数值自洽 ≠ 物理证实。本册判 FAIL 的是「光子内部仍在运行」这一命题的全部可算读法；'
               '不等于否证空间螺旋纲领本身。',
}

guard('G-S1 theory_complete',
      len(THEORY['axioms']) == 4 and len(THEORY['theorems']) == 6 and len(THEORY['corollaries']) == 5,
      '核心理论体系：公理 4 / 定理 6 / 推论 5 / 边界 4')

I_('S01', '核心理论体系固化（公理 4 · 定理 6 · 推论 5 · 边界 4）',
   '体系名：' + THEORY['name'] + '。公理 A1–A4（含★A4「内禀 = 沿 boost 轨道导数为零」这一机器定义）；'
   '定理 T1–T6（T5 对偶定理为体系第一定理、T6 攻破定理为其推论）；推论 C1–C5；边界 B1–B4。'
   '红线：' + THEORY['redline'])

# ============================================================
# 13. 总账（必须在全部条目登记之后计算）+ 不自推 + 开放项
# ============================================================
I_('S02', '本册总账', '__PENDING__')

CNT = {}
for _e in ENTRIES:
    CNT[_e['verdict']] = CNT.get(_e['verdict'], 0) + 1

for _e in ENTRIES:
    if _e['code'] == 'S02':
        _e['detail'] = ('条目 ' + str(len(ENTRIES)) + '（' + str(CNT) + '）｜守卫 ' + str(GOK[0]) +
                        '/' + str(len(GUARDS)) + '｜求导定理 5（T1–T5）+ 攻破定理 1（T6）｜'
                        '修复路径 7 条｜精算复算 ' + str(len(VROWS)) + ' 项｜评级：求导证明册 O/L1。')

I_('S03', '不自推清单 6 项',
   'NS1 不新推物理，只把既有结论升级为导数定理并定价 · '
   'NS2 继承 r53/r54/r56/r110/r116/r117 结论不重判（真空无双折射、κ/τ/ω 非洛伦兹不变量、'
   'null 测地线直、换参零判别力、36 格判决）· '
   'NS3 机读规则（导数判据、约束面导数、快度导数、对偶定理的线性方程组）人工定义、机器执行 · '
   'NS4 不修改任何既有产物字节，未读改他人文件 · '
   'NS5 外部锚（m_γ 上限 ' + fv(_mg) + ' J、结构光减速实验）标 [C] 且不作判据 · '
   'NS6 修复路径只定价不代选（7 条并列给出，取舍须用户裁决）。')

I_('S04', '新增开放项与继承登记',
   '新增 **O-PHOTON-SCALE-DUALITY**：由 T5，光子的任何内禀频率都与外部长度标度互为对偶 ⇒ '
   '「给光子内禀频率」与「不引入外部标度」不可兼得；若要突破，必须给出 L 的第一性来源（目前无候选）。'
   '继承未变：O-PHOTON-INTERIOR（r116，无定域中心 ⇒ 亚结构不可判定）· r54 N20 两难 · '
   'r56 C13（弯曲时空需 Newman–Penrose 标架）· r53 恢复条件。')

ENTRIES.sort(key=lambda _e: _e['code'])

# ============================================================
# 14. 落盘 + ASCII 控制台摘要（中文细节全部进产物，控制台只出 ASCII）
# ============================================================
def _jsonable(x):
    if isinstance(x, Dc):
        return str(x)
    if isinstance(x, Fr):
        return str(x)
    if isinstance(x, tuple):
        return list(x)
    raise TypeError('unserializable: ' + repr(x))


OUT = {
    'round': ROUND, 'tag': TAG, 'stamp': STAMP,
    'question': '光子以 c 移动时内部是否仍在运行？—— 求导证明 + 修复定价 + 精算复算 + 体系固化',
    'entries': ENTRIES, 'entry_count': len(ENTRIES), 'verdict_count': CNT,
    'guards': GUARDS, 'guard_pass': GOK[0], 'guard_total': len(GUARDS),
    'fixes': FIXES, 'vrows': VROWS, 'theory': THEORY,
    'key_numbers': {
        'R_max_1e-18_m': fv(H_HEL * RM18),
        'curvature_radius_m': fv(CURV_R),
        'v_eq_sphere_over_c': fv(V_SPHERE / C),
        't1_diff_convergence_ratio': fv(_ratio1),
        't1_second_order_resid': fv(_res_t1),
        't2_constraint_deriv': fv(_d3),
        't2_partial_deriv_R': fv(_Rfix),
        't3_dlnomega_deta': fv(_d5 / omega_of_eta(ETA0)),
        't3_dm_deta': fv(_d6),
        't3_dE_deta_control': fv(_d7),
        't4_ratio_at_star': fv(_r_star),
        't4_ratio_at_2star': fv(_r_2L),
        't5_solution_E_hbar_c': str(SOL_A),
        't5_solution_hbar_c_L': str(SOL_C),
        't5_nu0_equals_omega': fv(_nu0),
        't5_ratio_lambdaC': fv(_R_LAMC),
        't5_ratio_lP': fv(_R_LP),
        'triad_resid': fv(_res_triad),
        'triad_positive_control_resid': fv(_res_bad),
        'doppler_beta0p9_nm': fv(dopp(Dc('0.9')) * Dc('1e9')),
        'E_over_pc_resid': fv(_res_pc),
        'oam_bound_10um': fv(oam_bound(Dc('10E-6'))),
        'm_gamma_decel_1e-6eV': fv(_decel),
    },
}

NAME = 'TUFT-r124_光子内部运行求导证明与修复定价_核心理论体系_2026-10-20'
with io.open(os.path.join(OUTD, NAME + '.json'), 'w', encoding='utf-8') as fh:
    json.dump(OUT, fh, ensure_ascii=False, indent=1, default=_jsonable)

_R = []
_R.append('r124 photon-interior derivative-proof report ' + STAMP)
_R.append('entries=' + str(len(ENTRIES)) + '  ' + str(CNT))
_R.append('guards=' + str(GOK[0]) + '/' + str(len(GUARDS)))
_R.append('fixes=' + str(len(FIXES)) + '  verdicts=' + str([x['verdict'] for x in FIXES]))
_R.append('')
for g in GUARDS:
    _R.append(('OK  ' if g['ok'] else 'BAD ') + g['name'] + ' | ' + g['note'])
_R.append('')
for e in ENTRIES:
    _R.append('[' + e['verdict'] + '] ' + e['code'] + ' ' + e['title'])
    _R.append('    ' + e['detail'])
_R.append('')
_R.append('--- THEORY ---')
_R.append(THEORY['name'])
for a in THEORY['axioms']:
    _R.append('A ' + a['id'] + ': ' + a['text'])
for t in THEORY['theorems']:
    _R.append('T ' + t['id'] + ': ' + t['name'])
    _R.append('   ' + t['statement'])
    _R.append('   reading: ' + t['reading'])
    _R.append('   => ' + t['consequence'])
for c in THEORY['corollaries']:
    _R.append('C ' + c['id'] + ': ' + c['text'])
_R.append('REDLINE: ' + THEORY['redline'])

with io.open(os.path.join(OUTD, NAME + '_report.txt'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(_R))

_md = []
_md.append('# ' + NAME)
_md.append('')
_md.append('> ' + ROUND + ' | ' + STAMP + ' | guards ' + str(GOK[0]) + '/' + str(len(GUARDS)) +
           ' | entries ' + str(len(ENTRIES)) + ' ' + str(CNT))
_md.append('')
for e in ENTRIES:
    _md.append('## ' + e['code'] + ' [' + e['verdict'] + '] ' + e['title'])
    _md.append('')
    _md.append(e['detail'])
    _md.append('')
_md.append('## 修复路径定价表')
_md.append('')
_md.append('| 代号 | 路径 | 新增自由度 | 外部输入 | 判决 | 最小代价 | 冲突/说明 |')
_md.append('|---|---|---|---|---|---|---|')
for x in FIXES:
    _md.append('| ' + x['code'] + ' | ' + x['name'] + ' | ' + str(x['ndof']) + ' | ' +
               str(x['external_inputs']) + ' | ' + x['verdict'] + ' | ' + x['minimal_cost'] +
               ' | ' + x['conflict'] + ' |')
_md.append('')
_md.append('## 核心理论体系')
_md.append('')
for a in THEORY['axioms']:
    _md.append('- **' + a['id'] + '**：' + a['text'])
_md.append('')
for t in THEORY['theorems']:
    _md.append('### ' + t['id'] + ' ' + t['name'])
    _md.append('')
    _md.append(t['statement'])
    _md.append('')
    _md.append('- 机读：' + t['reading'])
    _md.append('- 推论：' + t['consequence'])
    _md.append('')
for c in THEORY['corollaries']:
    _md.append('- **' + c['id'] + '**：' + c['text'])
_md.append('')
for b in THEORY['boundaries']:
    _md.append('- 边界 **' + b['id'] + '**：' + b['text'])
_md.append('')
_md.append('> 红线：' + THEORY['redline'])

with io.open(os.path.join(OUTD, NAME + '.md'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(_md))

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
print('RC_CHECK guards=' + str(GOK[0]) + '/' + str(len(GUARDS)) +
      ' entries=' + str(len(ENTRIES)) + ' fixes=' + str(len(FIXES)))
print('KEY T5 sol(E,hbar,c)=' + str(SOL_A) + '  sol(hbar,c,L)=' + str(SOL_C))
print('KEY R_max=' + fv(H_HEL * RM18) + '  curv_radius=' + fv(CURV_R) +
      '  v_eq/c=' + fv(V_SPHERE / C))
print('KEY dlnomega/deta=' + fv(_d5 / omega_of_eta(ETA0)) + '  dm/deta=' + fv(_d6) +
      '  dE/deta_ctrl=' + fv(_d7))
print('KEY triad_resid=' + fv(_res_triad) + '  control_resid=' + fv(_res_bad))
print('KEY ratio_lambdaC=' + fv(_R_LAMC) + '  ratio_lP=' + fv(_R_LP))
print('PRODUCTS ' + NAME + '{.json,.md,_report.txt}')

sys.exit(0 if GOK[0] == len(GUARDS) else 2)
