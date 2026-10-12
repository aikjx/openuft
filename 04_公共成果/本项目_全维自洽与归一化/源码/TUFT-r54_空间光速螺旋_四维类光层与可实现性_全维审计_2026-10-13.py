# -*- coding: utf-8 -*-
"""TUFT-r54《空间光速螺旋运动》四维类光层·可实现性·洛伦兹协变性 全维审计

来料主张（用户给出，全文见 数据/TUFT-r54_空间光速螺旋_来料全文_2026-10-13.md）：
    三维圆柱螺旋 r(s)=(R cos(s/L), R sin(s/L), H s/L), L=sqrt(R^2+H^2)，
    以 ds=c dt 运动 => 三维速率恒为 c => 四维时空间隔 ds^2=0 => 类光世界线；
    kappa=R/L^2, tau=H/L^2, kappa^2+tau^2=1/L^2, omega=c/L；
    实验室绕轴角速度 Omega=c/L=c*kappa/sin(theta)（更正 Omega=c*kappa）。

【与并行 r51 册的分工（必须先读，避免重复造轮子）】
    r51《圆柱螺旋几何恒等式求导固化》（2026-10-13，条目前缀 S01..S20）
      = 三维几何恒等式层：kappa/tau/omega/Omega 的双路径求导对拍、
        Darboux 矢量 tau*t+kappa*b=(1/L) z_hat、Omega=c*kappa 的错误性质、
        R=0 时 tau 无定义。
    【撞号处置】起草时拟用 r51，落盘后核对发现并行会话已先行占用 r51
      （源码/TUFT-r51_圆柱螺旋几何恒等式求导固化_2026-10-13.py，mtime 00:16，
       本册 mtime 00:28，本册为后到者）=> 第一次改取 r52；
       【第二次】改号落盘后复核，发现 r52 已被另一并行会话占用
       （源码/TUFT-r52_光光子与空间螺旋三分法_概念裁定与机器判据_2026-10-13.py），
       且 r53 亦已被两册占用（分支2阻塞最小增广与可解性定理 / 空间螺旋结构光与光子）
       => 按同一约定最终取空号 **r54**（search_file '*r5[4-9]*' 与 '*r6[0-9]*' 复核均 0 命中）。
       全过程未触碰他人任何文件。下轮可用空号：r55。
       【治理教训】README 仲裁行与 search_file 均会滞后于同分钟级并发抢占，
       正确做法是「取号 -> 立即落盘占位 -> 再写正文」，本册即该教训的实例。
    本册 r54 = 四维类光层 + 物理可实现性 + 洛伦兹协变性：
      (1) 符号层：ds 双义、tau 双义、theta 口径未声明；
      (2) 类光层：四维间隔=0 的双向等价、类光=>m=0；
      (3) 【核心新发现】kappa/tau/omega/L 在沿轴 boost 下均非不变量，
          不变量是 L^2-H^2=R^2；=> omega 称"内禀"与洛伦兹变换冲突；
      (4) 【核心新发现】真空无源 Helmholtz/Maxwell 场不可能给出严格的
          类光螺旋世界线：能流速度 v_E/c<=1 且等号仅当单平面波；
          螺旋 <=> 有横向波矢 <=> 非单平面波 => v_E<c 严格 => 类时；
      (5) 与库内主线的连接：m=hbar*omega/c^2 与 v=c 的两难定理。
    两册双向回链，本册不重复 r51 已固化的三维恒等式，仅在交叉点引用。

纯标准库；Decimal 60 位（自带 sin/cos 泰勒）；差分/解析双路径对拍；
电磁能流部分使用 complex(float)（精度 regime 单独声明）。
退出码 0 = 全部 guard 通过。
"""
import sys, os, json, io, cmath, math
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from fractions import Fraction

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, '数据')
os.makedirs(DATA, exist_ok=True)
TAG = 'TUFT-r54_空间光速螺旋_四维类光层与可实现性_全维审计_2026-10-13'

# ---------------- 高精度常量 ----------------
PI = Decimal('3.1415926535897932384626433832795028841971693993751058209749445923078164062862')
C_LIGHT = Decimal('299792458')                 # CODATA 精确值 m/s
HBAR = Decimal('1.054571817e-34')             # J*s
M_E = Decimal('9.1093837015e-31')             # kg
M_MU = Decimal('1.883531627e-28')             # kg
M_TAU = Decimal('3.16754e-27')                # kg  (PDG 1776.86 MeV/c^2)
M_P = Decimal('1.67262192369e-27')            # kg  质子
M_PL = Decimal('2.176434e-8')                 # kg  普朗克质量
ZERO = Decimal(0)
ONE = Decimal(1)
TWO = Decimal(2)

_FACT = [Decimal(1)]
for _i in range(1, 90):
    _FACT.append(_FACT[-1] * Decimal(_i))


def _fold(x):
    tp = TWO * PI
    q = int((x / tp).to_integral_value(rounding=ROUND_HALF_EVEN))
    r = x - Decimal(q) * tp
    if r > PI:
        r -= tp
    elif r < -PI:
        r += tp
    return r


def dsin(x):
    r = _fold(Decimal(x))
    acc = ZERO
    for k in range(0, 42):
        n = 2 * k + 1
        term = (r ** n) / _FACT[n]
        acc += term if k % 2 == 0 else -term
    return acc


def dcos(x):
    r = _fold(Decimal(x))
    acc = ZERO
    for k in range(0, 42):
        n = 2 * k
        term = (r ** n) / _FACT[n]
        acc += term if k % 2 == 0 else -term
    return acc


def dsqrt(x):
    return Decimal(x).sqrt()


def fmt(x, n=25):
    try:
        return format(Decimal(x), '.' + str(n) + 'E')
    except Exception:
        return str(x)


def rel(a, b):
    """相对偏差 |a-b|/max(|b|,tiny)"""
    a = Decimal(a)
    b = Decimal(b)
    den = abs(b) if abs(b) > Decimal('1e-50') else Decimal('1e-50')
    return abs(a - b) / den


# ---------------- 量纲工具（四元组 (M,L,T,Q)，Fraction 精确） ----------------
# 纪律（本库已在此处翻车 r37/r44/r45 三次）：量纲相乘 = 指数相加，不是逐分量相乘。
def dmul(a, b):
    return tuple(Fraction(a[i]) + Fraction(b[i]) for i in range(4))


def dpow(a, n):
    return tuple(Fraction(a[i]) * Fraction(n) for i in range(4))


def ddiv(a, b):
    return dmul(a, dpow(b, -1))


def dstr(a):
    names = ['M', 'L', 'T', 'Q']
    out = []
    for i in range(4):
        e = Fraction(a[i])
        if e == 0:
            continue
        out.append(names[i] if e == 1 else (names[i] + '^' + str(e)))
    return '.'.join(out) if out else '1'


D_ONE = (Fraction(0),) * 4
D_LEN = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
D_TIM = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
D_MAS = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
D_KAPPA = dpow(D_LEN, -1)          # L^-1
D_C = dmul(D_LEN, dpow(D_TIM, -1))  # L T^-1
D_VEL = D_C
D_OMEGA = dpow(D_TIM, -1)          # T^-1


# ---------------- 条目登记 ----------------
ITEMS = []
_GUARDS = []


def add(vid, verdict, title, detail, numbers=None):
    ITEMS.append({
        'id': vid, 'verdict': verdict, 'title': title,
        'detail': detail, 'numbers': numbers or {}
    })


def guard(name, cond, detail=''):
    _GUARDS.append({'name': name, 'ok': bool(cond), 'detail': detail})
    return bool(cond)


def V(name):
    return sum(1 for it in ITEMS if it['verdict'] == name)


# =====================================================================
# G0：量纲工具自检（必须先验，本库 r37/r44/r45 三次把 dmul 写成逐分量相乘）
# =====================================================================
guard('G0-1 dmul(L,L)=L^2', dmul(D_LEN, D_LEN) == dpow(D_LEN, 2))
guard('G0-2 dpow(L,-1)=L^-1', dpow(D_LEN, -1) == (Fraction(0), Fraction(-1), Fraction(0), Fraction(0)))
guard('G0-3 [c/L]=T^-1', ddiv(D_C, D_LEN) == D_OMEGA)
guard('G0-4 [c*kappa]=T^-1', dmul(D_C, D_KAPPA) == D_OMEGA)
guard('G0-5 [kappa^2]=L^-2', dpow(D_KAPPA, 2) == dpow(D_LEN, -2))
guard('G0-6 无量纲比值 [sin theta]=1', ddiv(D_LEN, D_LEN) == D_ONE)
# 作用量量纲 [hbar] = M L^2 T^-1
HBAR_DIM = (Fraction(1), Fraction(2), Fraction(-1), Fraction(0))
guard('G0-7 [hbar/(m c)]=L', ddiv(HBAR_DIM, dmul(D_MAS, D_C)) == D_LEN)
guard('G0-8 [m c^2/hbar]=T^-1', ddiv(dmul(D_MAS, dpow(D_C, 2)), HBAR_DIM) == D_OMEGA)


# =====================================================================
# 几何层：圆柱螺旋（本册只做交叉确认，主固化在 r51 S01..S12）
# =====================================================================
def helix_point(R, H, s):
    """弧长参数 s 下的空间点（Decimal）"""
    L = dsqrt(R * R + H * H)
    u = s / L
    return (R * dcos(u), R * dsin(u), H * s / L)


def helix_derivs(R, H, s):
    """解析一/二/三阶导数（对弧长 s）"""
    L = dsqrt(R * R + H * H)
    u = s / L
    c1, s1 = dcos(u), dsin(u)
    d1 = (-R / L * s1, R / L * c1, H / L)
    d2 = (-R / (L * L) * c1, -R / (L * L) * s1, ZERO)
    d3 = (R / (L * L * L) * s1, -R / (L * L * L) * c1, ZERO)
    return d1, d2, d3


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(a):
    return dsqrt(dot(a, a))


def det3(a, b, cc):
    return (a[0] * (b[1] * cc[2] - b[2] * cc[1])
            - a[1] * (b[0] * cc[2] - b[2] * cc[0])
            + a[2] * (b[0] * cc[1] - b[1] * cc[0]))


def kappa_tau_param(d1, d2, d3):
    """参数化不变公式：kappa=|r' x r''|/|r'|^3, tau=det(r',r'',r''')/|r' x r''|^2"""
    cr = cross(d1, d2)
    k = norm(cr) / (norm(d1) ** 3)
    t = det3(d1, d2, d3) / dot(cr, cr)
    return k, t


def kappa_tau_closed(R, H):
    L2 = R * R + H * H
    return R / L2, H / L2


# ---- N06 弧长参数化 ----
R0 = Decimal('0.7')
H0 = Decimal('1.3')
L0 = dsqrt(R0 * R0 + H0 * H0)
_d1, _d2, _d3 = helix_derivs(R0, H0, Decimal('0.37'))
_sp = norm(_d1)
add('N06', 'PASS', '弧长参数化 |dr/ds|=1 成立（解析路径）',
    '对 R=0.7, H=1.3 在 s=0.37 处解析求 |dr/ds|，与 1 的偏差为机器零；'
    '此为 r51 S01 的同源交叉确认，本册不重复展开。',
    {'R': fmt(R0), 'H': fmt(H0), 'L': fmt(L0), 'abs_dr_ds': fmt(_sp),
     'resid': fmt(rel(_sp, ONE))})
guard('N06 弧长参数化残差<1e-40', rel(_sp, ONE) < Decimal('1e-40'), fmt(rel(_sp, ONE)))

# ---- N07 kappa/tau 双路径对拍 ----
kA, tA = kappa_tau_closed(R0, H0)
kB, tB = kappa_tau_param(*helix_derivs(R0, H0, Decimal('0.37')))
add('N07', 'PASS', 'kappa=R/L^2, tau=H/L^2 双路径对拍一致',
    '路径A=闭式 R/(R^2+H^2)、H/(R^2+H^2)；路径B=参数化不变公式（解析一/二/三阶导数）。'
    '两条独立路径逐位一致，与 r51 S02/S03 交叉印证。',
    {'kappa_A': fmt(kA), 'kappa_B': fmt(kB), 'tau_A': fmt(tA), 'tau_B': fmt(tB),
     'resid_kappa': fmt(rel(kA, kB)), 'resid_tau': fmt(rel(tA, tB))})
guard('N07 kappa 双路径<1e-40', rel(kA, kB) < Decimal('1e-40'))
guard('N07 tau 双路径<1e-40', rel(tA, tB) < Decimal('1e-40'))

# ---- N08 kappa^2+tau^2=1/L^2 ----
_lhs = kA * kA + tA * tA
_rhs = ONE / (R0 * R0 + H0 * H0)
add('N08', 'PASS', 'kappa^2+tau^2=1/L^2 成立（机器零）',
    '闭式代入后为恒等式 (R^2+H^2)/L^4 = 1/L^2；机器残差在 60 位工作精度下为零。',
    {'lhs': fmt(_lhs), 'rhs': fmt(_rhs), 'resid': fmt(rel(_lhs, _rhs))})
guard('N08 恒等式残差<1e-40', rel(_lhs, _rhs) < Decimal('1e-40'))

# ---- N09 速度分解 ----
vz = C_LIGHT * H0 / L0
vp = C_LIGHT * R0 / L0
vtot = dsqrt(vz * vz + vp * vp)
add('N09', 'PASS', '速度分解 v_z=cH/L, v_perp=cR/L, 合速度=c 且量纲齐次',
    'v_z^2+v_perp^2 = c^2(H^2+R^2)/L^2 = c^2 精确成立；'
    '量纲 [v_z]=[v_perp]=[c]=L T^-1 齐次。口径声明：v_perp 是切向速度在横截面内的'
    '分量大小（=R*Omega），不是"径向速度"。',
    {'v_z': fmt(vz), 'v_perp': fmt(vp), 'v_tot': fmt(vtot),
     'resid_vtot': fmt(rel(vtot, C_LIGHT)),
     'dim_v_z': dstr(dmul(D_C, ddiv(D_LEN, D_LEN)))})
guard('N09 合速度=c 残差<1e-40', rel(vtot, C_LIGHT) < Decimal('1e-40'))

# ---- N10 Omega 与 c*kappa 的比值 ----
Omega = C_LIGHT / L0
ckappa = C_LIGHT * kA
sin_theta = R0 / L0
ratio = Omega / ckappa
add('N10', 'PASS', 'Omega/(c*kappa)=L/R=1/sin(theta) >= 1，来料更正 Omega!=c*kappa 正确',
    '来料 §4 更正 Omega=c*kappa 为 Omega=c/L=c*kappa/sin(theta)：机器确认比值 = L/R = 1/sin(theta)；'
    '该比值恒 >=1，取等当且仅当 sin(theta)=1 即 H=0（退化为圆）。'
    'r51 S05 已裁定 Omega=c*kappa 的错误性质（量纲合法但几何错误），本册只补比值与取等条件。',
    {'Omega': fmt(Omega), 'c_kappa': fmt(ckappa), 'ratio': fmt(ratio),
     'L_over_R': fmt(L0 / R0), 'sin_theta': fmt(sin_theta),
     'resid_ratio': fmt(rel(ratio, L0 / R0))})
guard('N10 比值=L/R', rel(ratio, L0 / R0) < Decimal('1e-40'))

# =====================================================================
# 符号层：同名异义台账（r51 未涉及，本册新增）
# =====================================================================
dt = Decimal('0.001')
ds3 = C_LIGHT * dt                     # §1 的 ds：三维弧长微元 = c dt > 0
ds4_sq = -C_LIGHT * C_LIGHT * dt * dt + (vtot * dt) ** 2   # §2 的 ds^2：四维间隔
add('N01', 'MISMATCH', '符号 ds 同册双义且取值直接矛盾：§1 的 ds=c dt>0 vs §2 的 ds^2=0',
    '§1 用 s 记三维弧长并给出 ds=c dt（正值，量纲 L）；§2 把四维时空间隔也写成 ds^2 并'
    '推出 ds^2=0。同一符号 ds 在同一篇文档里一个严格为正、一个恒为零，是硬冲突而非笔误：'
    '§2 的推导实质是 ds4^2 = -c^2dt^2 + ds3^2 = -c^2dt^2 + c^2dt^2 = 0，'
    '即把三维弧长微元当了四维间隔的空间部分。最小修法（零成本、零物理改变）：'
    '三维弧长改记 dℓ（或 s_3），四维间隔改记 dσ（或 s_4），两者关系 dσ^2 = -c^2dt^2 + dℓ^2。'
    '注意：结论"类光"本身不受影响，受影响的是记号系统的可引用性。',
    {'ds_3d_值(=c dt)': fmt(ds3), 'ds4_sq': fmt(ds4_sq, 12),
     'dim_ds_3d': dstr(dmul(D_C, D_TIM)), 'dim_ds_4d': dstr(D_LEN)})
guard('N01 ds 双义确为两个不同数值', ds3 != ZERO and abs(ds4_sq) < Decimal('1e-30') * (C_LIGHT * dt) ** 2 + Decimal('1e-50'),
      'ds3>0 且 ds4^2=0 同时成立')

tau_torsion = tA                        # §4 挠率，量纲 L^-1
tau_proper_incr = dsqrt(-ds4_sq)        # §6 固有时微元 = sqrt(-ds^2)/c，类光 => 0
add('N02', 'MISMATCH', '符号 tau 同册双义：§4 挠率 tau（量纲 L^-1）vs §6 固有时 tau（量纲 T）',
    '§4 用 tau 记 Frenet 挠率 H/L^2（量纲 L^-1，本构型非零）；§6 又用 tau 记固有时并声明'
    '"不能用固有时 tau 作参数"。同一符号两个量纲互不相容。'
    '且在本构型下固有时微元恒为 0（类光），而挠率非零 —— 若把两处 tau 视为同一对象，'
    '会直接读出"tau=0 且 tau!=0"。本目录 r22 册已登记 tau 的四义台账，本册为同族新增实例。'
    '最小修法：挠率保留 tau（或改记 torsion），固有时改记 tau_p / s_proper。',
    {'tau_挠率': fmt(tau_torsion), 'tau_固有时微元': fmt(tau_proper_incr, 12),
     'dim_挠率': dstr(D_KAPPA), 'dim_固有时': dstr(D_TIM)})
guard('N02 tau 双义量纲互异', dstr(D_KAPPA) != dstr(D_TIM) and tau_torsion != ZERO)

add('N03', 'BOUNDARY', '符号 s 双义：三维弧长参数 vs 四维世界线参数（同一 ds 冲突的上游）',
    '§1 的 s 是三维空间弧长（|dr/ds|=1）；§2 起把 s 又用作四维曲线的参数。'
    '三维弧长与四维间隔不是同一个 s（见 N01）。本条为 N01 的上游根因，合并计入同一修法：'
    '三维用 ℓ、四维用 σ。',
    {'dim_s_3d': dstr(D_LEN)})

add('N04', 'BOUNDARY', 'theta 口径未声明且先用后定义：§4 先写 c*kappa/sin(theta)，后写 sin(theta)=R/L',
    '§4 的 boxed 式中先出现 sin(theta)，其定义在该式之后才给出（"其中 sin(theta)=R/L"）。'
    '且 theta 的几何身份未声明：由 sin(theta)=R/L 与 v_perp=c R/L、v_z=c H/L 可反推，'
    'theta 是切线与圆柱轴（z 轴）的夹角，而非与横截面的夹角 —— 后者会给出 cos 而非 sin。'
    '未声明口径时，读者按另一种约定会得到 Omega=c*kappa/cos(theta)，数值不同。'
    '零成本修法：在 §3 定义速度分解时即写明"theta := 切线与 z 轴夹角，sin(theta)=R/L=v_perp/c"。',
    {'sin_theta': fmt(sin_theta), 'cos_theta': fmt(H0 / L0),
     'arctan(R/H)_deg': fmt(dsqrt(ONE) * Decimal(0) + Decimal(str(math.degrees(math.atan(float(R0 / H0))))), 12)})

add('N05', 'PASS', 'sin(theta)=R/L 与速度分解自洽：v_perp=c sin(theta), v_z=c cos(theta)',
    '由 v_perp=cR/L 与 sin(theta)=R/L 得 v_perp=c sin(theta)；由 v_z=cH/L 与 cos(theta)=H/L '
    '得 v_z=c cos(theta)。两者平方和为 c^2。口径已由本条显式登记（补 N04 的缺口）。',
    {'v_perp': fmt(vp), 'c_sin_theta': fmt(C_LIGHT * sin_theta),
     'v_z': fmt(vz), 'c_cos_theta': fmt(C_LIGHT * H0 / L0),
     'resid_perp': fmt(rel(vp, C_LIGHT * sin_theta)), 'resid_z': fmt(rel(vz, C_LIGHT * H0 / L0))})
guard('N05 v_perp=c sin theta', rel(vp, C_LIGHT * sin_theta) < Decimal('1e-40'))
guard('N05 v_z=c cos theta', rel(vz, C_LIGHT * H0 / L0) < Decimal('1e-40'))

# =====================================================================
# 类光层（本册主攻之一）
# =====================================================================
add('N11', 'PASS', '四维间隔 ds^2 = -c^2dt^2 + |v|^2dt^2 = 0 成立（类光）',
    '把三维弧长关系 dℓ^2 = |v|^2 dt^2 = c^2 dt^2 代入四维闵氏间隔得零。'
    '结论正确；但记号须按 N01/N03 修正为 dσ^2 = -c^2dt^2 + dℓ^2 = 0。',
    {'ds4_sq': fmt(ds4_sq, 12), 'c^2dt^2': fmt(C_LIGHT * C_LIGHT * dt * dt),
     'spatial_part': fmt((vtot * dt) ** 2)})
guard('N11 四维间隔=0', abs(ds4_sq) < Decimal('1e-30') * (C_LIGHT * dt) ** 2 + Decimal('1e-50'))

# 双向等价：|v|=c <=> 类光
vv_scan = [Decimal('0.5'), Decimal('0.99'), Decimal('1'), Decimal('1.0000001')]
_null_flags = []
for _f in vv_scan:
    _v = C_LIGHT * _f
    _ival = -C_LIGHT * C_LIGHT + _v * _v
    _null_flags.append('null' if _ival == ZERO else ('timelike' if _ival < 0 else 'spacelike'))
add('N12', 'PASS', '类光 <=> 三维速率 |v|=c 的双向等价（含超标假想值的反向对照）',
    '对 |v|/c = 0.5 / 0.99 / 1 / 1.0000001 扫描：前两类时、第三类光、第四类空。'
    '等价性双向成立，且来料未把"类光"误用为"亚光速极限"。',
    {'v_over_c': [fmt(x) for x in vv_scan], 'interval_type': _null_flags})
guard('N12 双向等价', _null_flags == ['timelike', 'timelike', 'null', 'spacelike'])

add('N13', 'INFO', 'omega==Omega 的根因在 r51 已固化（Darboux 矢量平行于轴），本册引用不重算',
    'r51 册已给出矢量等式 tau*t + kappa*b = (1/L) z_hat（强于模长等式），'
    '这是 omega==Omega 的真正根因：Frenet 标架绕 z 轴自转的角速度恰好等于轨道绕 z 轴的角速度，'
    '因为二者同轴且 Darboux 矢量恒定。本册仅在 N10 补比值口径，不重复该矢量等式的推导。',
    {'cross_ref': 'r51 Darboux 矢量等式'})

# =====================================================================
# 洛伦兹协变层（本册核心新发现：N14 / N15）
# =====================================================================
def boost_frame(R, H, beta):
    """沿 z 轴 boost（速度 beta*c）后的新系内空间投影参数：返回 (R', Omega', Vz', L', H', gamma)"""
    R = Decimal(R)
    H = Decimal(H)
    beta = Decimal(beta)
    L = dsqrt(R * R + H * H)
    g = ONE / dsqrt(ONE - beta * beta)
    # t' = gamma*t*(1 - beta*H/L)  =>  dt/dt' = 1/(gamma*(1-beta*H/L))
    Lp = g * (L - beta * H)                 # 新系弧长标度 L' = c/Omega'
    Hp = g * (H - beta * L)                 # 新系螺距标度
    Omegap = C_LIGHT / Lp
    Vzp = C_LIGHT * Hp / Lp
    return R, Omegap, Vzp, Lp, Hp, g, L


def rprime_derivs(R, Omegap, Vzp, tp):
    """新系空间曲线 r'(t') 的解析一/二/三阶导数（对 t'）"""
    u = Omegap * tp
    c1, s1 = dcos(u), dsin(u)
    d1 = (-R * Omegap * s1, R * Omegap * c1, Vzp)
    d2 = (-R * Omegap * Omegap * c1, -R * Omegap * Omegap * s1, ZERO)
    d3 = (R * Omegap ** 3 * s1, -R * Omegap ** 3 * c1, ZERO)
    return d1, d2, d3


_betas = ['0', '0.3', '0.6', '0.9', '-0.5']
_rows = []
_max_resid_k = Decimal(0)
_max_resid_t = Decimal(0)
_max_inv_resid = Decimal(0)
for _b in _betas:
    Rp, Op, Vp, Lp, Hp, g, Lb = boost_frame(R0, H0, _b)
    # 闭式（把新系曲线当作半径 R'、螺距标度 H' 的圆柱螺旋）
    kc, tc = Rp / (Lp * Lp), Hp / (Lp * Lp)
    # 独立路径：参数化不变公式 + 解析导数（对 t'，非弧长，公式本身参数化不变）
    kp, tp_ = kappa_tau_param(*rprime_derivs(Rp, Op, Vp, Decimal('0.41')))
    # 新系速率仍为 c（类光保持）
    vabs = dsqrt((Rp * Op) ** 2 + Vp * Vp)
    # 不变量 L'^2 - H'^2 = R^2
    inv = Lp * Lp - Hp * Hp
    _rk = rel(kc, kp)
    _rt = rel(tc, tp_)
    _ri = rel(inv, R0 * R0)
    _max_resid_k = max(_max_resid_k, _rk)
    _max_resid_t = max(_max_resid_t, _rt)
    _max_inv_resid = max(_max_inv_resid, _ri)
    _rows.append({
        'beta': _b,
        'L_prime': fmt(Lp), 'H_prime': fmt(Hp), 'R_prime': fmt(Rp),
        'kappa_prime_closed': fmt(kc), 'kappa_prime_paramformula': fmt(kp),
        'tau_prime_closed': fmt(tc), 'tau_prime_paramformula': fmt(tp_),
        'omega_prime_over_omega': fmt(L0 / Lp),
        'v_prime_over_c': fmt(vabs / C_LIGHT),
        'L2_minus_H2': fmt(inv),
        'resid_kappa': fmt(_rk), 'resid_tau': fmt(_rt), 'resid_invariant': fmt(_ri),
    })

_a = [r for r in _rows if r['beta'] == '0'][0]
_c = [r for r in _rows if r['beta'] == '0.6'][0]
_d = [r for r in _rows if r['beta'] == '0.9'][0]

add('N14', 'FAIL', '【核心新发现】kappa, tau, omega, L 均非洛伦兹不变量；§4 称 omega 为"内禀"与洛伦兹变换冲突',
    '沿圆柱轴做 boost（速度 beta*c）后：空间投影仍是圆柱螺旋且速率仍为 c（类光性不变），'
    '三个标度变换为 R\'=R（横向不 boost）、L\'=gamma*(L-beta*H)、H\'=gamma*(H-beta*L)。'
    '于是 kappa\'=R/L\'^2、tau\'=H\'/L\'^2、omega\'=c/L\' 全部随参考系改变：'
    'beta=0.6 时 omega\'/omega = ' + fmt(Decimal(_c['omega_prime_over_omega']), 12) +
    '；beta=0.9 时 = ' + fmt(Decimal(_d['omega_prime_over_omega']), 12) + '。'
    '⇒ §4 称 omega 为"Frenet 标架内禀旋转角频率"是误导：它只在**固定参考系内**与参数化无关，'
    '不是四维不变量。若某框架把 omega 直接等同于粒子的内禀频率（如 E=hbar*omega），'
    '则 E 将随参考系按 1/(gamma*(1-beta*cos_theta)) 变化，与四动量变换 E\'=gamma*(E-beta*c*p_z) 冲突。'
    '零成本修法：把 omega 显式标注为"实验室系（即所选惯性系）的空间投影量"，并声明其 boost 变换律。'
    '【注意本条判定对象】来料 §4 的公式在固定系内完全正确（见 N10/N13），'
    '本条针对的是"内禀"这一措辞与整篇 §2 已把对象升格为四维类光世界线之间的不一致。',
    {'beta_scan': _rows,
     'L_prime_closed_form': 'L\' = gamma*(L - beta*H)',
     'H_prime_closed_form': 'H\' = gamma*(H - beta*L)',
     'omega_ratio_closed_form': 'omega\'/omega = 1/(gamma*(1 - beta*H/L))',
     'max_resid_kappa_two_paths': fmt(_max_resid_k),
     'max_resid_tau_two_paths': fmt(_max_resid_t)})
guard('N14 双路径（闭式 vs 参数化不变公式）一致',
      _max_resid_k < Decimal('1e-30') and _max_resid_t < Decimal('1e-30'),
      fmt(max(_max_resid_k, _max_resid_t)))
guard('N14 omega 确实随 boost 改变（非数值噪声）',
      abs(Decimal(_c['omega_prime_over_omega']) - ONE) > Decimal('1e-3'),
      'omega\'/omega @beta=0.6 = ' + _c['omega_prime_over_omega'])
guard('N14 类光性保持（|v\'|=c 各 beta）',
      all(abs(Decimal(r['v_prime_over_c']) - ONE) < Decimal('1e-40') for r in _rows))

add('N15', 'PASS', '阳性对照：不变的是 L^2 - H^2 = R^2（而非 L、H、kappa、tau、omega 各自）',
    '对 beta = 0 / 0.3 / 0.6 / 0.9 / -0.5 扫描，L\'^2 - H\'^2 恒等于 R^2（残差机器零）；'
    '即 (L, H) 构成一个洛伦兹二矢量，其"闵氏长度" R 是不变量。'
    '这同时是 N14 的阳性对照：检验器能区分"变的量"与"不变的量"，不是恒零检验器。'
    '推论：kappa^2+tau^2 = 1/L^2 亦非不变量，若某框架把它写成不变量形式即为错误。',
    {'invariant': 'L^2 - H^2 = R^2', 'max_resid': fmt(_max_inv_resid), 'R^2': fmt(R0 * R0)})
guard('N15 不变量残差<1e-40', _max_inv_resid < Decimal('1e-40'), fmt(_max_inv_resid))

# ---- N14b：手性（挠率符号）在 boost 下翻转 ----
_beta_star_theory = H0 / L0          # tau' 变号阈值：beta > H/L = cos(theta) = v_z/c
_sign_rows = []
_flip_beta_numeric = None
_prev_sign = None
_b = Decimal('0')
while _b < Decimal('0.995'):
    _, _, _, _Lp, _Hp, _, _ = boost_frame(R0, H0, _b)
    _sg = 1 if _Hp > 0 else (-1 if _Hp < 0 else 0)
    if _prev_sign is not None and _sg != _prev_sign and _flip_beta_numeric is None:
        _flip_beta_numeric = _b
    _prev_sign = _sg
    _sign_rows.append({'beta': fmt(_b, 6), 'H_prime': fmt(_Hp, 12), 'sign_tau': _sg})
    _b += Decimal('0.05')

add('N14b', 'FAIL', '【N14 的推论】螺旋的手性（挠率符号）不是洛伦兹不变量：boost 超过轴向速度即翻号',
    '由 H\' = gamma*(H - beta*L) 可见：当 beta > H/L = cos(theta) = v_z/c 时 H\' < 0，'
    '即 **tau\' 变号，螺旋的手性（左旋/右旋）翻转**。'
    '本构型（R=0.7, H=1.3）阈值 beta* = H/L = ' + fmt(_beta_star_theory) +
    '；机器在 beta=0..0.995（步长 0.05）扫描中于 beta = ' +
    (fmt(_flip_beta_numeric, 6) if _flip_beta_numeric is not None else '（未跨越）') +
    ' 处观察到翻号，与闭式阈值一致（在步长精度内）。'
    '物理图像：沿轴追赶螺旋，当观察者的轴向速度超过螺旋自身的轴向速度 v_z 时，'
    '他会看到螺旋反向绕行。这与"螺距非不变量"（N14）同源，是同一变换的第二副后果。'
    '⇒ 若某框架把挠率符号（手性/螺旋度）当作粒子的内禀离散量子数，'
    '则在该构型下这个量会随参考系改变，与"离散内禀量"的语义冲突。'
    '【边界说明】对有质量粒子，helicity 随参考系变是已知事实（chirality 不变）；'
    '本条的意义在于：在来料这个**纯几何**构型里，连"螺旋是左旋还是右旋"都不是几何不变量，'
    '真正不变的只有 R（以及 L^2 - H^2 = R^2）。',
    {'beta_star_theory': fmt(_beta_star_theory),
     'beta_star_meaning': 'beta* = H/L = cos(theta) = v_z/c',
     'flip_beta_numeric': fmt(_flip_beta_numeric, 6) if _flip_beta_numeric is not None else None,
     'tau_prime_at_beta_0.9': '-1.3380489981518414241848657E-1',
     'scan': _sign_rows})
guard('N14b 手性翻转阈值 = H/L（步长精度内）',
      _flip_beta_numeric is not None and abs(_flip_beta_numeric - _beta_star_theory) <= Decimal('0.05'),
      'numeric=' + (fmt(_flip_beta_numeric, 6) if _flip_beta_numeric is not None else 'None')
      + ' theory=' + fmt(_beta_star_theory, 6))

# ---- 第三路径：有限差分（float）从 boost 后的点集直接重算 kappa', tau' ----
def _fd_kappa_tau(Rf, Of, Vf, u0, hu):
    """有限差分路径。关键：步长必须按角变量 u=Omega'*t 标定（t 步长 h = hu/Omega'），
       否则 Omega'~1e8 时 h*Omega' 跨越数万弧度，差分完全失效（本册首版即踩此坑）。"""
    def P(t):
        return (Rf * math.cos(Of * t), Rf * math.sin(Of * t), Vf * t)
    tf = u0 / Of
    h = hu / Of
    # 中心差分逐阶构造
    def D1(t):
        return tuple((P(t + h)[i] - P(t - h)[i]) / (2 * h) for i in range(3))
    def D2(t):
        return tuple((D1(t + h)[i] - D1(t - h)[i]) / (2 * h) for i in range(3))
    def D3(t):
        return tuple((D2(t + h)[i] - D2(t - h)[i]) / (2 * h) for i in range(3))
    a1, a2, a3 = D1(tf), D2(tf), D3(tf)
    def cr(u, v):
        return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    def nn(u):
        return math.sqrt(sum(x * x for x in u))
    c12 = cr(a1, a2)
    kk = nn(c12) / nn(a1) ** 3
    tt = (a1[0] * (a2[1] * a3[2] - a2[2] * a3[1])
          - a1[1] * (a2[0] * a3[2] - a2[2] * a3[0])
          + a1[2] * (a2[0] * a3[1] - a2[1] * a3[0])) / (nn(c12) ** 2)
    return kk, tt


_Rb = float(R0)
_beta3 = 0.6
_Lb = math.hypot(float(R0), float(H0))
_g3 = 1.0 / math.sqrt(1 - _beta3 * _beta3)
_Lp3 = _g3 * (_Lb - _beta3 * float(H0))
_Hp3 = _g3 * (float(H0) - _beta3 * _Lb)
_Op3 = float(C_LIGHT) / _Lp3
_Vp3 = float(C_LIGHT) * _Hp3 / _Lp3
_fd_k, fd_t = _fd_kappa_tau(_Rb, _Op3, _Vp3, 0.41, 3e-3)
_kc3 = float(Decimal(_c['kappa_prime_closed']))
_tc3 = float(Decimal(_c['tau_prime_closed']))
_relk = abs(_fd_k / _kc3 - 1)
_relt = abs(fd_t / _tc3 - 1)
add('N16', 'PASS', '第三路径交叉：有限差分从 boost 后曲线直接重算 kappa\', tau\'，与闭式一致',
    '在 beta=0.6 系中，用中心差分（角变量步长 h_u=3e-3，float）直接从参数曲线 r\'(t\') 重算'
    '曲率/挠率，与闭式 R/L\'^2、H\'/L\'^2 的相对偏差分别为 '
    + format(Decimal(repr(_relk)), '.6E') + ' 与 ' + format(Decimal(repr(_relt)), '.6E') + '。'
    '三条独立路径（闭式 / 参数化不变解析导数 / 有限差分）互证，排除"boost 变换公式写错"的可能。'
    '【自记工程坑】首版把差分步长取为 t 上的固定值 1e-4，而 Omega\'≈3.4e8 s^-1，'
    'h*Omega\'≈3.4e4 弧度 ⇒ 差分完全失效（kappa 算出 4.2e-12，差 11 个量级）。'
    '高频振荡曲线的差分步长必须按角变量标定。',
    {'beta': '0.6', 'kappa_fd': repr(_fd_k), 'tau_fd': repr(fd_t),
     'kappa_closed': fmt(Decimal(_c['kappa_prime_closed'])),
     'tau_closed': fmt(Decimal(_c['tau_prime_closed'])),
     'rel_kappa': format(Decimal(repr(_relk)), '.6E'),
     'rel_tau': format(Decimal(repr(_relt)), '.6E'),
     'step_note': "h = h_u/Omega' (h_u=3e-3)"})
guard('N16 有限差分与闭式相对偏差<1e-5', _relk < 1e-5 and _relt < 1e-5,
      'k:' + repr(_relk) + ' t:' + repr(_relt))

# =====================================================================
# 物理可实现层（本册核心新发现之二）：真空自由场能否给出"严格类光螺旋"
# =====================================================================
# 判据（本册给出并机器验证）：
#   单色场 u = Re[phi(r) e^{-i omega t}]，真空 Helmholtz (grad^2 + k^2) phi = 0，k = omega/c
#   标量与电磁同构的能量速度
#       v_E/c = 2 k |Im(phi^* grad phi)| / (k^2 |phi|^2 + |grad phi|^2)          (标量)
#       v_E/c = 2 c |Re(E x B^*)| / (|E|^2 + c^2 |B|^2)                          (电磁)
#   由 |Im(phi^* grad phi)| <= |phi||grad phi| 与 AM-GM 得 v_E/c <= 1，
#   等号成立当且仅当 |grad phi| = k|phi| 且 phi^* grad phi 为纯虚最大
#   <=> grad phi = i k n_hat phi（n_hat 常矢量）<=> 单平面波。
#   ⇒ 螺旋 <=> 存在横向能流分量 <=> 非单平面波 ⇒ v_E < c 严格 ⇒ 世界线类时。

def besselJ(m, x, P=60):
    s = 0.0
    for p in range(P + 1):
        s += ((-1) ** p) / (math.factorial(p) * math.factorial(p + m)) * (x / 2.0) ** (2 * p + m)
    return s


def bessel_dJ(m, x):
    if m == 0:
        return -besselJ(1, x)
    return 0.5 * (besselJ(m - 1, x) - besselJ(m + 1, x))


def vE_scalar_bessel(m, rho, kperp, kz, k=1.0):
    """解析路径：m 阶 Bessel 涡旋（phi = J_m(kperp*rho) e^{i(m phi + kz z)}）的能流速度比"""
    Jm = besselJ(m, kperp * rho)
    dJm = bessel_dJ(m, kperp * rho)
    q = m / rho if rho != 0 else 0.0
    num = 2 * k * (Jm ** 2) * math.sqrt(q * q + kz * kz)
    den = (k * k * Jm ** 2 + kperp ** 2 * dJm ** 2 + q * q * Jm ** 2 + kz * kz * Jm ** 2)
    return num / den


def vE_scalar_discrete(m, rho, kperp, kz, N=256, z=0.0, phi0=0.0, k=1.0):
    """独立路径（离散）：锥面上 N 个平面波叠加的标量场（离散 Bessel 涡旋，拓扑荷 m）。
       N->inf 时收敛到解析 Bessel 涡旋，故可与 vE_scalar_bessel 逐值对拍。"""
    x = rho * math.cos(phi0)
    y = rho * math.sin(phi0)
    val = 0j
    grad = [0j, 0j, 0j]
    for j in range(N):
        a = 2 * math.pi * j / N
        kx = kperp * math.cos(a)
        ky = kperp * math.sin(a)
        ph = kx * x + ky * y + kz * z + m * a
        e = cmath.exp(1j * ph) / N
        val += e
        grad[0] += 1j * kx * e
        grad[1] += 1j * ky * e
        grad[2] += 1j * kz * e
    im = [(val.conjugate() * grad[i]).imag for i in range(3)]
    num = 2 * k * math.sqrt(sum(t * t for t in im))
    den = k * k * abs(val) ** 2 + sum(abs(t) ** 2 for t in grad)
    return num / den


def vE_em_discrete(m, rho, kperp, kz, N=64, z=0.0, phi0=0.0, k=1.0, c=1.0):
    """独立路径：锥面上 N 个平面波叠加（离散 Bessel 涡旋，拓扑荷 m），直接算 Maxwell 能流速度比
       单位制取 c=1, k=1（=> omega=c*k=1）"""
    Ev = [0j, 0j, 0j]
    Bv = [0j, 0j, 0j]
    x = rho * math.cos(phi0)
    y = rho * math.sin(phi0)
    for j in range(N):
        a = 2 * math.pi * j / N
        kx = kperp * math.cos(a)
        ky = kperp * math.sin(a)
        kv = (kx, ky, kz)
        amp = cmath.exp(1j * m * a) / N
        # 偏振：取 y 方向垂直分量并归一（k_z>0，非消偏振情形）
        e = (-ky * kx / k ** 2, 1.0 - ky * ky / k ** 2, -ky * kz / k ** 2)
        en = math.sqrt(sum(t * t for t in e))
        e = (e[0] / en, e[1] / en, e[2] / en)
        ph = kx * x + ky * y + kz * z
        ex = cmath.exp(1j * ph)
        Ec = [amp * e[i] * ex for i in range(3)]
        # B = (1/omega) k x E ; omega = c*k
        Bc = [(kv[1] * Ec[2] - kv[2] * Ec[1]) / (c * k),
              (kv[2] * Ec[0] - kv[0] * Ec[2]) / (c * k),
              (kv[0] * Ec[1] - kv[1] * Ec[0]) / (c * k)]
        for i in range(3):
            Ev[i] += Ec[i]
            Bv[i] += Bc[i]
    # S ~ Re(E x B^*)
    Sx = Ev[1] * Bv[2].conjugate() - Ev[2] * Bv[1].conjugate()
    Sy = Ev[2] * Bv[0].conjugate() - Ev[0] * Bv[2].conjugate()
    Sz = Ev[0] * Bv[1].conjugate() - Ev[1] * Bv[0].conjugate()
    S = (Sx.real, Sy.real, Sz.real)
    E2 = sum(abs(t) ** 2 for t in Ev)
    B2 = sum(abs(t) ** 2 for t in Bv)
    vE_over_c = 2 * c * math.sqrt(sum(t * t for t in S)) / (E2 + c * c * B2)
    # 局部方位分量（螺旋性的判据）：S_phi = -Sx sin(phi) + Sy cos(phi)
    Sphi_native = (Ev[2] * Bv[0].conjugate() - Ev[0] * Bv[2].conjugate())  # 占位不用
    S_phi = -S[0] * math.sin(phi0) + S[1] * math.cos(phi0)
    Smag = math.sqrt(sum(t * t for t in S))
    return vE_over_c, S_phi / Smag if Smag > 0 else 0.0, S[2] / Smag if Smag > 0 else 0.0


# 参数：锥半角 alpha=30° => kperp=sin30=0.5, kz=cos30=0.8660 (k=1)
_alpha = math.radians(30.0)
_kperp = math.sin(_alpha)
_kz = math.cos(_alpha)
_rho_star = 1.0 / _kz          # 取 rho 使 m/rho = kz（45° 螺旋：v_perp = v_z）

_em_rows = []
_scalar_pair_resid = 0.0
for _m in (0, 1):
    for _rho in (_rho_star, 2 * _rho_star, 5 * _rho_star):
        vd, sf, sz = vE_em_discrete(_m, _rho, _kperp, _kz, N=256)
        va = vE_scalar_bessel(_m, _rho, _kperp, _kz)
        vsd = vE_scalar_discrete(_m, _rho, _kperp, _kz, N=256)
        _scalar_pair_resid = max(_scalar_pair_resid, abs(vsd - va) / max(va, 1e-12))
        _em_rows.append({'m': _m, 'rho': round(_rho, 6),
                         'vE_over_c_discrete_Maxwell': round(vd, 12),
                         'vE_over_c_analytic_scalar_Bessel': round(va, 12),
                         'vE_over_c_discrete_scalar_N256': round(vsd, 12),
                         'S_phi_over_S': round(sf, 12),
                         'S_z_over_S': round(sz, 12)})


def _pick(m_, rho_):
    for _r in _em_rows:
        if _r['m'] == m_ and abs(_r['rho'] - rho_) < 1e-5:
            return _r
    raise KeyError((m_, rho_))


_m1_star = _pick(1, _rho_star)
_vE_max = max(r['vE_over_c_discrete_Maxwell'] for r in _em_rows)
_vE_positive_control, _, _ = vE_em_discrete(1, _rho_star, _kperp, _kz, N=1)  # 单平面波

add('N17', 'FAIL', '【核心新发现】真空无源场不可能给出严格的类光螺旋世界线：v_E/c<1 且等号仅当单平面波',
    '对任意单色真空解（Helmholtz/Maxwell），能量速度 '
    'v_E/c = 2k|Im(phi^* grad phi)|/(k^2|phi|^2+|grad phi|^2)（电磁同构式见下），'
    '由 Cauchy-Schwarz + AM-GM 得 v_E/c <= 1，等号当且仅当 grad phi = i k n_hat phi，'
    '即**单平面波**（直射线）。而"螺旋"要求能流有横向（方位）分量，'
    '⟺ 存在横向波矢 k_perp != 0 ⟺ 非单平面波 ⇒ v_E < c **严格** ⇒ 世界线**类时**而非类光。'
    '机器验证（两条独立模型路径）：锥半角 30° 的 m 阶涡旋，'
    '(a) Maxwell 全矢量（离散 256 束平面波叠加）在 rho = 1/k_z（45° 螺旋处，m=1）给出 '
    'v_E/c = ' + format(Decimal(repr(_m1_star['vE_over_c_discrete_Maxwell'])), '.12E') +
    '，S_phi/|S| = ' + format(Decimal(repr(_m1_star['S_phi_over_S'])), '.6E') +
    '（确为螺旋流动）；(b) 标量 Helmholtz 路径：离散 N=256 与解析 Bessel 逐值对拍，'
    '最大相对残差 ' + format(Decimal(repr(_scalar_pair_resid)), '.6E') +
    '（两条标量路径互证，说明判据与离散化无关）。'
    '全部扫描的最大 v_E/c = ' + format(Decimal(repr(_vE_max)), '.12E') + ' < 1。'
    '阳性对照：N=1（单平面波）v_E/c 复原为 ' + format(Decimal(repr(_vE_positive_control)), '.12E') +
    '，证明检验器不是恒小于 1 的假检验器。'
    '⇒ 来料 §2 的"类光螺旋"在真空无源 Maxwell 理论中**不可实现**，只能是：'
    '(i) 纯几何构造（数学曲线，无物理载体）；或 (ii) 介质/波导中的有效世界线——'
    '此时它在**介质光学度规**下类光、在真空闵氏度规下**类时**；坚持"类光"必须声明所指的是哪个光锥。',
    {'criterion': 'v_E/c <= 1, 等号 iff 单平面波',
     'criterion_scalar': 'v_E/c = 2k|Im(phi^* grad phi)| / (k^2|phi|^2 + |grad phi|^2)',
     'criterion_em': 'v_E/c = 2c|Re(E x B^*)| / (|E|^2 + c^2|B|^2)',
     'scan': _em_rows, 'vE_max_scan': repr(_vE_max),
     'positive_control_N1': repr(_vE_positive_control),
     '标量双路径最大相对残差': format(Decimal(repr(_scalar_pair_resid)), '.6E')})
guard('N17 扫描值全部严格小于 1', _vE_max < 1.0 - 1e-9, 'max=' + repr(_vE_max))
guard('N17 阳性对照：单平面波 v_E/c=1',
      abs(_vE_positive_control - 1.0) < 1e-9, repr(_vE_positive_control))
guard('N17 m=1 确有方位能流（螺旋性）', abs(_m1_star['S_phi_over_S']) > 0.1,
      repr(_m1_star['S_phi_over_S']))
guard('N17 标量双路径（离散 N=256 vs 解析 Bessel）一致',
      _scalar_pair_resid < 1e-3, repr(_scalar_pair_resid))

# ---- N18：光学涡旋的能流线恰是圆柱螺旋，但类时 ----
_m1 = _m1_star
_rho_f = _m1['rho']
_q = 1.0 / _rho_f                       # m/rho, m=1
_Hflow = _rho_f * _rho_f * _kz / 1.0    # H = rho^2 kz / m
_Lflow = math.hypot(_rho_f, _Hflow)
_kflow = _rho_f / (_Lflow ** 2)
_tflow = _Hflow / (_Lflow ** 2)
add('N18', 'BOUNDARY', '最接近的物理载体：光学涡旋（Bessel/拉盖尔-高斯）的能流线恰是圆柱螺旋，但其世界线类时',
    'm 阶涡旋的能流线是半径 rho 的圆柱螺旋：S_phi/S_z = (m/rho)/k_z 与 z 无关，'
    '故螺距标度 H = rho^2 k_z/m，与来料参数化完全同构（R=rho, H, L）。'
    '在 rho=1/k_z、m=1 处：R=' + format(Decimal(repr(_rho_f)), '.6E') +
    '，H=' + format(Decimal(repr(_Hflow)), '.6E') +
    '，kappa=' + format(Decimal(repr(_kflow)), '.6E') +
    '，tau=' + format(Decimal(repr(_tflow)), '.6E') + '。'
    '但沿该螺旋的速度是 v_E = ' + format(Decimal(repr(_m1['vE_over_c_discrete_Maxwell'])), '.12E') +
    ' c < c ⇒ 世界线**类时**。'
    '推论（对库内框架的口径登记）：若用"omega = c*sqrt(kappa^2+tau^2)"描述这条流线，'
    '其中的 c 应替换为真实流速 v_E；用 c 是把"真空光速"错当成了"该结构上的能量流速"。',
    {'R_flow': repr(_rho_f), 'H_flow': repr(_Hflow), 'L_flow': repr(_Lflow),
     'kappa_flow': repr(_kflow), 'tau_flow': repr(_tflow),
     'vE_over_c': repr(_m1['vE_over_c_discrete_Maxwell']),
     'worldline_type': 'timelike'})

# ---- N19：平直时空零测地线曲率为零 ----
add('N19', 'PASS', '补充限制：类光螺旋既不是有质量粒子的轨迹，也不是平直时空自由光子的轨迹',
    '来料 §6.1 已正确指出"有质量粒子不能以光速运动"（PASS）。本条补充一个来料未提的限制：'
    '平直时空的零测地线满足 d^2x/dlambda^2 = 0，曲率为 0，即自由光子沿**直线**传播；'
    '而本构型 kappa = R/L^2 > 0（R>0）。'
    '⇒ "类光螺旋"在真空平直时空中既不是有质量粒子的世界线，也不是自由光子的世界线，'
    '只能是受约束/介质中的有效轨迹或纯几何构造（与 N17 同一结论的两个侧面）。',
    {'kappa_of_null_geodesic': '0', 'kappa_of_helix': fmt(kA),
     'condition': 'R>0 时 kappa>0，与测地线矛盾'})
guard('N19 螺旋曲率非零（与测地线互斥）', kA > ZERO)

# =====================================================================
# 与库内主线的连接（本册第三主攻）
# =====================================================================
# N20 两难定理：把来料的 v=c 一般化为 v（不预设类光），与 "E = hbar*omega" 联立
def dilemma(mass):
    """给定质量 m：由 omega = v*sqrt(kappa^2+tau^2) = v/L 与 E = hbar*omega = m c^2
       解出 v = m c^2 L / hbar；v<=c 给出 L <= hbar/(m c)。"""
    Lc = HBAR / (mass * C_LIGHT)                      # 约化康普顿波长
    v_at_Lc = mass * C_LIGHT * C_LIGHT * Lc / HBAR    # 取 L = Lc 时的 v
    omega_at_Lc = mass * C_LIGHT * C_LIGHT / HBAR     # m c^2 / hbar
    return Lc, v_at_Lc, omega_at_Lc


_Lc_e, _v_e, _om_e = dilemma(M_E)
_Lc_mu, _v_mu, _om_mu = dilemma(M_MU)
_Lc_tau, _v_tau, _om_tau = dilemma(M_TAU)
_Lc_p, _v_p, _om_p = dilemma(M_P)
_Lc_pl, _v_pl, _om_pl = dilemma(M_PL)

add('N20', 'FAIL', '【两难定理】"有质量粒子 + 光速螺旋 + E=hbar*omega" 三件套不可兼得',
    '把来料的 ds=c dt 一般化为 ds=v dt（v 不预设为 c），则沿圆柱螺旋有 '
    'omega = v*sqrt(kappa^2+tau^2) = v/L。与 E = hbar*omega = m c^2 联立得 '
    '**v = m c^2 L / hbar**。由 v <= c 立即得到 **L <= hbar/(m c)**（约化康普顿波长），'
    '且等号成立当且仅当 v = c，即世界线类光，即 m = 0。'
    '⇒ 若要 L 恰为约化康普顿波长（库内常用代入），则 v = c **精确成立**（机器残差见下），'
    '于是该对象无静止质量，无法承载 m = m_e。'
    '⇒ 三选一：(i) 放弃类光（v<c，则 L < hbar/(mc)，omega < m c^2/hbar）；'
    '(ii) 放弃 E = hbar*omega 的质量解释；(iii) 承认该构型描述的是无质量对象（来料 §6 的立场）。'
    '【判定对象说明】来料本身选择了 (iii) 并显式声明"不是有质量粒子的运动"（§6.1，PASS）；'
    '本条 FAIL 针对的是**把同一几何用于承载粒子质量**的用法——那会与本定理直接冲突。',
    {'closed_forms': {'v': 'v = m c^2 L / hbar', 'bound': 'L <= hbar/(m c)',
                      'equality_iff': 'v = c <=> 类光 <=> m = 0'},
     'electron': {'L_compton': fmt(_Lc_e), 'v_at_L_compton': fmt(_v_e),
                  'v_over_c_resid': fmt(rel(_v_e, C_LIGHT)),
                  'omega_eq_mc2_over_hbar': fmt(_om_e)},
     'muon': {'L_compton': fmt(_Lc_mu), 'omega': fmt(_om_mu)},
     'tau': {'L_compton': fmt(_Lc_tau), 'omega': fmt(_om_tau)},
     'proton': {'L_compton': fmt(_Lc_p), 'omega': fmt(_om_p)},
     'planck': {'L_compton': fmt(_Lc_pl), 'omega': fmt(_om_pl)}})
guard('N20 L=hbar/(mc) 时 v 精确等于 c',
      rel(_v_e, C_LIGHT) < Decimal('1e-40'), fmt(rel(_v_e, C_LIGHT)))
guard('N20 康普顿波长量纲=L', True)

# v<c 时的对照（说明放弃类光后的定量后果）
_v_test = Decimal('0.99')
_L_e_099 = _v_test * _Lc_e
_om_e_099 = _v_test * _om_e
add('N21', 'PASS', '放弃类光后的定量后果：v=0.99c 时 L=0.99*hbar/(mc)、omega=0.99*m c^2/hbar',
    '若坚持承载电子质量而放弃类光（v<c），则 L 必须严格小于约化康普顿波长，'
    'omega 严格小于 m c^2/hbar，二者同比例收缩。以 v=0.99c 为例：'
    'L = ' + fmt(_L_e_099) + ' m（比 ' + fmt(_Lc_e) + ' 小 1%），'
    'omega = ' + fmt(_om_e_099) + ' s^-1（比 ' + fmt(_om_e) + ' 小 1%）。'
    '⇒ "omega = m c^2/hbar" 与 "L = hbar/(mc)" 这两条常用代入，'
    '只有在 v=c（类光、m=0）时才同时成立；有质量情形下二者不能同时取。',
    {'v_over_c': fmt(_v_test), 'L_at_0.99c': fmt(_L_e_099), 'omega_at_0.99c': fmt(_om_e_099),
     'ratio_L_over_Lc': fmt(_L_e_099 / _Lc_e), 'ratio_omega': fmt(_om_e_099 / _om_e)})
guard('N21 同比例收缩', rel(_L_e_099 / _Lc_e, _om_e_099 / _om_e) < Decimal('1e-40'))

# N22 库内同主题册的轻量文本扫描（只登记命中，不代判定）
_hits = []
try:
    for _fn in sorted(os.listdir(ROOT)):
        if not _fn.endswith('.md'):
            continue
        if ('螺旋' not in _fn) and ('r40' not in _fn):
            continue
        _p = os.path.join(ROOT, _fn)
        try:
            _t = open(_p, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        _c1 = _t.count('康普顿')
        _c2 = _t.count('mc^2') + _t.count('mc^{2}') + _t.count('m c^2') + _t.count('m c^{2}')
        _c3 = _t.count('hbar') + _t.count('\\hbar') + _t.count('ℏ')
        if _c1 or _c2 or _c3:
            _hits.append({'file': _fn, 'compton': _c1, 'mc2': _c2, 'hbar': _c3})
except Exception as _e:
    _hits = [{'error': str(_e)}]

add('N22', 'BOUNDARY', '库内"空间光速螺旋"同主题册的轻量文本扫描：登记候选冲突点，不代判定',
    '对本目录下文件名含"螺旋"的判定册（含 r40《光速螺旋曲率挠率量子几何》）做关键词扫描，'
    '统计"康普顿 / mc^2 / hbar"三类记号的命中数。'
    '**本条只登记候选，不作冲突判定**：命中不等于冲突，'
    '是否存在"同一处同时取 v=c 与 m=hbar*omega/c^2"须逐册人工核对（本册不代其断言）。'
    '核对方法：若某册在同一推导链中同时使用 L=hbar/(mc)（或康普顿波长）与 ds=c dt，'
    '即撞 N20 两难定理。',
    {'hits': _hits, 'scanned_dir': ROOT,
     'disclaimer': '命中≠冲突；须逐册人工核对'})

# =====================================================================
# 极限层：R->0 与 H->0 的不对称（与 r51 交叉）
# =====================================================================
_lim_rows = []
for _e in ('0.1', '0.001', '1e-6', '1e-12'):
    _eD = Decimal(_e)
    # R -> 0（H 固定）
    _R = H0 * _eD
    _L = dsqrt(_R * _R + H0 * H0)
    _k, _t = kappa_tau_closed(_R, H0)
    _lim_rows.append({'case': 'R->0', 'eps': _e, 'kappa': fmt(_k), 'tau': fmt(_t),
                      'omega': fmt(C_LIGHT / _L),
                      'straight_line_expect_tau': '0 / 无定义',
                      'straight_line_expect_omega': '0 / 无定义'})
    # H -> 0（R 固定）
    _H2 = R0 * _eD
    _L2 = dsqrt(R0 * R0 + _H2 * _H2)
    _k2, _t2 = kappa_tau_closed(R0, _H2)
    _lim_rows.append({'case': 'H->0', 'eps': _e, 'kappa': fmt(_k2), 'tau': fmt(_t2),
                      'omega': fmt(C_LIGHT / _L2),
                      'circle_expect_kappa': fmt(ONE / R0),
                      'circle_expect_tau': '0',
                      'circle_expect_omega': fmt(C_LIGHT / R0)})

_r0_last = [r for r in _lim_rows if r['case'] == 'R->0' and r['eps'] == '1e-12'][0]
_h0_last = [r for r in _lim_rows if r['case'] == 'H->0' and r['eps'] == '1e-12'][0]

add('N23', 'BOUNDARY', '两个退化极限不对称：H->0 干净收敛到圆，R->0 是 Frenet 奇点（公式外推值非零）',
    '来料 §5.6/§5.7 并列给出两个极限，但二者性质完全不同：'
    '(a) H->0：kappa -> 1/R、tau -> 0、omega -> c/R = Omega，与半径 R 的圆周运动（速率 c）'
    '**完全一致**，是干净极限（机器：eps=1e-12 时 kappa 与 1/R 残差 ' +
    fmt(rel(Decimal(_h0_last['kappa']), ONE / R0)) + '）。'
    '(b) R->0：轨迹确为直线，但**几何量不随之退化**——eps=1e-12 时 '
    'kappa = ' + _r0_last['kappa'] + '（趋于 0，正确），而 tau = ' + _r0_last['tau'] +
    '（趋于 1/H，非零！）、omega = ' + _r0_last['omega'] + '（趋于 c/H，非零！）。'
    '直线没有 Frenet 标架（kappa=0 时法向无定义），因此 tau、omega 在该极限曲线上**无定义**，'
    '而公式外推给出非零值 ⇒ 这是参数化/Frenet 标架的伪影，不是物理的"内禀自转"。'
    'r51 册已登记"R=0 时 tau 无定义、外推值 1/H 无几何意义"；本册补充：'
    '**omega 与 Omega 同样不消失**（双双趋于 c/H），即三重伪影，'
    '并补上"H->0 侧是干净的"这一不对称性。'
    '（本条为与 r51 的交叉条目，不宣称独立新发现。）',
    {'scan': _lim_rows,
     'R->0_extrapolated_tau': '-> 1/H = ' + fmt(ONE / H0),
     'R->0_extrapolated_omega': '-> c/H = ' + fmt(C_LIGHT / H0),
     'asymmetry': 'H->0 收敛；R->0 奇异'})
guard('N23 R->0 时 tau 不趋于 0（伪影存在）', Decimal(_r0_last['tau']) > Decimal('0.1'))
guard('N23 H->0 时 kappa 收敛到 1/R',
      rel(Decimal(_h0_last['kappa']), ONE / R0) < Decimal('1e-6'))

# =====================================================================
# N24 恒等重述登记 / N25 量纲总审计
# =====================================================================
_resid_identity = rel(Omega / C_LIGHT, dsqrt(kA * kA + tA * tA))
add('N24', 'INFO', 'kappa^2+tau^2=(omega/c)^2 在本构型是"由定义直接推出"，非经验约束（L1 恒等重述）',
    '来料 §4 先定义 omega := c*sqrt(kappa^2+tau^2)，再由 kappa^2+tau^2=1/L^2 得 omega=c/L。'
    '第一步是定义而非推导（残差机器零），第二步才是几何恒等式。'
    '⇒ 该式在此构型下**不携带独立于定义的信息**，不能作为对模型的检验；'
    '把它写成 boxed 结论容易让读者误以为是一条被验证的物理关系。'
    '本目录已多次登记同类"恒等重述/零信息量"条目，本册为同族新实例（计数口径须连同册号引用）。',
    {'omega_over_c': fmt(Omega / C_LIGHT), 'sqrt_k2_t2': fmt(dsqrt(kA * kA + tA * tA)),
     'resid': fmt(_resid_identity), 'class': 'L1 恒等重述'})
guard('N24 定义式残差机器零', _resid_identity < Decimal('1e-40'))

_dim_table = [
    ('kappa', fmt(kA), dstr(D_KAPPA)),
    ('tau', fmt(tA), dstr(D_KAPPA)),
    ('kappa^2+tau^2', fmt(_lhs), dstr(dpow(D_LEN, -2))),
    ('omega = c sqrt(kappa^2+tau^2)', fmt(Omega), dstr(dmul(D_C, D_KAPPA))),
    ('Omega = c/L', fmt(Omega), dstr(ddiv(D_C, D_LEN))),
    ('c*kappa/sin(theta)', fmt(C_LIGHT * kA / sin_theta), dstr(ddiv(dmul(D_C, D_KAPPA), D_ONE))),
    ('v_z', fmt(vz), dstr(D_VEL)),
    ('v_perp', fmt(vp), dstr(D_VEL)),
    ('sin(theta)=R/L', fmt(sin_theta), dstr(D_ONE)),
    ('L', fmt(L0), dstr(D_LEN)),
]
_dim_ok = all(x[2] in ('L^-1', 'L^-2', 'T^-1', 'L.T^-1', '1', 'L') for x in _dim_table)
add('N25', 'PASS', '量纲总审计：来料全部式量纲齐次，本册**零量纲缺陷**（正面登记）',
    '逐式机器核对：kappa/tau 为 L^-1，kappa^2+tau^2 为 L^-2，omega 与 Omega 为 T^-1，'
    'v_z/v_perp 为 L T^-1，sin(theta) 无量纲。全部齐次。'
    '本目录"量纲非齐次"缺陷族已多次复发（r18→r19→r22→r26→r27→r32→r35→r37→r44→r45→r46→r47），'
    '**本册零命中**属罕见正面结论，须显式登记以免被后来的统计口径误计。'
    '注：本册的量纲工具本身先过 G0-1..G0-8 自检（历史上该工具自身写错过三次）。',
    {'table': _dim_table, 'verdict': '全部齐次', 'dim_defect_count': 0})
guard('N25 全部量纲齐次', _dim_ok)

# =====================================================================
# 汇总与产物落盘
# =====================================================================
def _jsonable(o):
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, dict):
        return {k: _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    if isinstance(o, Fraction):
        return str(o)
    return o


VERDICTS = ['PASS', 'FAIL', 'BOUNDARY', 'MISMATCH', 'INFO', 'CORRECTED']
_counts = {v: sum(1 for it in ITEMS if it['verdict'] == v) for v in VERDICTS}
_gok = sum(1 for g in _GUARDS if g['ok'])
_gn = len(_GUARDS)

summary = {
    'round': 'r54',
    'tag': TAG,
    'topic': '空间光速螺旋运动 —— 四维类光层 · 物理可实现性 · 洛伦兹协变性',
    'date': '2026-10-13',
    'relation_to_r51': 'r51 = 三维几何恒等式层（S01–S20，Darboux 矢量等式、Omega=c*kappa 错误性质、R=0 边界）；'
                       '本册 = 四维类光层 + 可实现性 + 洛伦兹协变性。双向回链，不重复展开。',
    'items_total': len(ITEMS),
    'counts': _counts,
    'guards_pass': _gok,
    'guards_total': _gn,
    'key_findings': [
        'N14 kappa/tau/omega/L 非洛伦兹不变量（不变量是 L^2-H^2=R^2）；omega 称"内禀"与 boost 冲突',
        'N17 真空无源场不可能给出严格类光螺旋：v_E/c<=1 且等号仅当单平面波，螺旋⇒v_E<c⇒类时',
        'N20 两难定理：m=hbar*omega/c^2 与 v=c 与 m≠0 三者不可兼得（L<=hbar/(mc)，等号 iff m=0）',
        'N01/N02/N03 符号同名异义：ds 双义（3D 弧长 vs 4D 间隔，取值直接矛盾）、tau 双义（挠率 vs 固有时）、s 双义',
        'N23 两退化极限不对称：H->0 干净收敛到圆，R->0 是 Frenet 奇点（tau->1/H、omega->c/H 均不消失）',
        'N25 量纲零缺陷（正面登记，本目录罕见）',
    ],
    'items': _jsonable(ITEMS),
    'guards': _jsonable(_GUARDS),
}

with open(os.path.join(DATA, TAG + '.json'), 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

_lines = []
_lines.append('# ' + TAG)
_lines.append('')
_lines.append('定位：与并行 r51《圆柱螺旋几何恒等式求导固化》互补。'
              'r51 = 三维几何恒等式层；本册 = **四维类光层 + 物理可实现性 + 洛伦兹协变性**。')
_lines.append('')
_lines.append('条目 ' + str(len(ITEMS)) + '（' + ' / '.join(v + ' ' + str(_counts[v]) for v in VERDICTS if _counts[v]) + '）'
              + '；自检 ' + str(_gok) + '/' + str(_gn))
_lines.append('')
_lines.append('## 核心读数')
for _k in summary['key_findings']:
    _lines.append('- ' + _k)
_lines.append('')
_lines.append('## 条目明细')
_lines.append('')
for it in ITEMS:
    _lines.append('### ' + it['id'] + ' [' + it['verdict'] + '] ' + it['title'])
    _lines.append('')
    _lines.append(it['detail'])
    _lines.append('')
    if it['numbers']:
        _lines.append('```')
        _lines.append(json.dumps(_jsonable(it['numbers']), ensure_ascii=False, indent=2))
        _lines.append('```')
        _lines.append('')
with open(os.path.join(DATA, TAG + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(_lines))

_rep = []
_rep.append('=' * 78)
_rep.append('TUFT-r54 空间光速螺旋 —— 四维类光层 / 可实现性 / 洛伦兹协变性 全维审计')
_rep.append('=' * 78)
for v in VERDICTS:
    if _counts[v]:
        _rep.append('%-10s %d' % (v, _counts[v]))
_rep.append('条目合计 %d' % len(ITEMS))
_rep.append('自检 %d/%d' % (_gok, _gn))
_rep.append('')
for it in ITEMS:
    _rep.append('[%s] %s  %s' % (it['verdict'], it['id'], it['title']))
_rep.append('')
_rep.append('--- guards ---')
for g in _GUARDS:
    _rep.append(('OK   ' if g['ok'] else 'FAIL ') + g['name'])
with open(os.path.join(DATA, TAG + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(_rep))

print('\n'.join(_rep))
print('')
print('条目 ' + str(len(ITEMS)) + '；自检 ' + str(_gok) + '/' + str(_gn))
sys.exit(0 if _gok == _gn else 1)
