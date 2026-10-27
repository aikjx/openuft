# -*- coding: utf-8 -*-
# =============================================================================
# TUFT r238 · warp 母稿残余面攻破：爱因斯坦张量解析实算 + 中微子 / Casimir /
#            研究议程审计 + r64 C05 跨册自纠
# 2026-10-26
#   ★改号链：r200（并行占用）→ r236（本线外部核实册）→ r237（并行占用·宇宙学层）
#     ⇒ 本册取 r238（实测 r24x / r25x 全空）
#   定位：r64–r67 + r236 之后的母稿残余未攻面；本册第一次对母稿度规做
#         **完整 4 维解析曲率实算**（Christoffel → Ricci → Einstein，纯解析链）
#   产出：同名 .json / .md / _report.txt
#   纯标准库；float64 解析曲率 + Decimal 60 位精算
#   方法论纪律（承接 r64 / r66 / r236）：
#     (1) 曲率代码必须先过阳性对照（beta=0 / 泡内 / 泡外 ⇒ G_{munu}=0）再用于判定
#     (2) Christoffel 必须与独立文献（McMonigal et al. 式 8-11）逐式机读对拍
#     (3) 同一物理量必须有两条以上独立路径（本册：4 维实算 / ADM 哈密顿约束 /
#         文献公式 Varieschi-Burstein 式 15）
#     (4) 引用必须可复核（arXiv / DOI / 期刊卷页）
#     (5) 跨册更正必须显式登记（本册撤回 r64 C05 / C05b）
# =============================================================================
from __future__ import annotations
import io
import os
import sys
import json
import math
from decimal import Decimal, getcontext

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:  # pragma: no cover
    pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, '数据')
NAME = 'TUFT-r238_warp母稿残余面攻破_爱因斯坦张量实算与中微子Casimir议程审计_2026-10-26'

# 物理常数（SI，CODATA 2018）
c = Decimal('299792458')
G = Decimal('6.67430e-11')
hbar = Decimal('1.054571817e-34')
eV = Decimal('1.602176634e-19')
M_SUN = Decimal('1.98892e30')
M_UNIV = Decimal('1.5e53')
LY = Decimal('9.4607304725808e15')
PI = Decimal('3.14159265358979323846264338327950288')

GUARD = []


def guard(name, ok, note=''):
    GUARD.append({'guard': name, 'ok': bool(ok), 'note': note})
    return bool(ok)


def D(x):
    return Decimal(str(x))


def fv(x, sig=12):
    if isinstance(x, float):
        return '%.*E' % (sig, x)
    return '%.*E' % (sig, x)


# =============================================================================
# 1. Alcubierre（= 母稿）度规的 4 维解析曲率引擎
#    ds^2 = -dt^2 + (dx - beta f(r_s) dt)^2 + dy^2 + dz^2   (c = 1)
#    r_s = sqrt((x - beta t)^2 + y^2 + z^2)
#    坐标以米计，beta = v_s/c 无量纲；f 为 Alcubierre 原始 tanh 形状函数
# =============================================================================
R_BUB = 100.0          # 泡半径 m
SIGMA = 1.0            # 壳厚参数 1/m


def _sech2(x):
    """数值稳定的 sech^2(x) = 4e^{-2|x|}/(1+e^{-2|x|})^2（避免 cosh 平方溢出）。"""
    ax = abs(x)
    e = math.exp(-2.0 * ax)
    return 4.0 * e / ((1.0 + e) ** 2)


def shape_f(r):
    """Alcubierre 原始形状函数 f(r_s)。"""
    a1 = math.tanh(SIGMA * (r + R_BUB))
    a2 = math.tanh(SIGMA * (r - R_BUB))
    return (a1 - a2) / (2.0 * math.tanh(SIGMA * R_BUB))


def shape_f1(r):
    """f'(r_s)。"""
    s1 = _sech2(SIGMA * (r + R_BUB))
    s2 = _sech2(SIGMA * (r - R_BUB))
    return SIGMA * (s1 + s2) / (2.0 * math.tanh(SIGMA * R_BUB))


def shape_f2(r):
    """f''(r_s)。"""
    t1 = math.tanh(SIGMA * (r + R_BUB))
    t2 = math.tanh(SIGMA * (r - R_BUB))
    s1 = _sech2(SIGMA * (r + R_BUB))
    s2 = _sech2(SIGMA * (r - R_BUB))
    return (SIGMA * SIGMA / math.tanh(SIGMA * R_BUB)) * (s2 * t2 - s1 * t1)


def metric_bundle(beta, t, x, y, z):
    """返回度规、逆度规及一/二阶导数（解析链式法则）。

    索引约定 0=t, 1=x, 2=y, 3=z。w = x - beta t；r_s = sqrt(w^2+y^2+z^2)。
    """
    w = x - beta * t
    r = math.sqrt(w * w + y * y + z * z)
    f = shape_f(r)
    f1 = shape_f1(r)
    f2 = shape_f2(r)
    B = beta * f                       # 位移矢量大小（c=1）

    # r_s 的一/二阶导数（对 (w,y,z) 用欧氏公式，再链到 (t,x,y,z)）
    # dw/dt = -beta, dw/dx = 1, dy/dy = 1, dz/dz = 1
    r1 = [0.0] * 4
    r1[0] = -beta * (w / r)
    r1[1] = (w / r)
    r1[2] = (y / r)
    r1[3] = (z / r)
    # r_ab = delta_ab - r_a r_b / r （在 (w,y,z) 子空间），映射到 4 维：
    #   d_mu d_nu r = (dmw)(dnw)/r - r1[mu]r1[nu]/r   （w 的二阶导为 0）
    r2 = [[0.0] * 4 for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            dw = ((-beta) if mu == 0 else (1.0 if mu == 1 else 0.0))
            dn = ((-beta) if nu == 0 else (1.0 if nu == 1 else 0.0))
            r2[mu][nu] = dw * dn / r - r1[mu] * r1[nu] / r

    # f 的一/二阶导
    f1v = [f1 * r1[mu] for mu in range(4)]
    f2v = [[f2 * r1[mu] * r1[nu] + f1 * r2[mu][nu] for nu in range(4)]
           for mu in range(4)]

    # 度规 g_tt = -(1-B^2), g_tx = g_xt = -B, g_xx=g_yy=g_zz=1
    g = [[0.0] * 4 for _ in range(4)]
    g[0][0] = -(1.0 - B * B)
    g[0][1] = g[1][0] = -B
    g[1][1] = g[2][2] = g[3][3] = 1.0

    # 逆度规（2x2 (t,x) 块行列式 = -1）
    gi = [[0.0] * 4 for _ in range(4)]
    gi[0][0] = -1.0
    gi[0][1] = gi[1][0] = -B
    gi[1][1] = 1.0 - B * B
    gi[2][2] = gi[3][3] = 1.0

    # g 的一阶导（只有 tt / tx 非零）
    g1 = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
    for mu in range(4):
        g1[mu][0][0] = 2.0 * B * beta * f1v[mu]
        g1[mu][0][1] = g1[mu][1][0] = -beta * f1v[mu]

    # g 的二阶导
    g2 = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            g2[mu][nu][0][0] = (2.0 * beta * beta * f1v[mu] * f1v[nu]
                                + 2.0 * B * beta * f2v[mu][nu])
            g2[mu][nu][0][1] = g2[mu][nu][1][0] = -beta * f2v[mu][nu]

    return {'g': g, 'gi': gi, 'g1': g1, 'g2': g2, 'B': B, 'f': f,
            'f1': f1, 'f2': f2, 'r': r, 'r1': r1}


def christoffels(mb):
    """Gamma^lambda_{mu nu}。"""
    g, gi, g1 = mb['g'], mb['gi'], mb['g1']
    gam = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                s = 0.0
                for sig in range(4):
                    s += gi[lam][sig] * (g1[mu][sig][nu] + g1[nu][sig][mu]
                                         - g1[sig][mu][nu])
                gam[lam][mu][nu] = 0.5 * s
    return gam


def einstein_tensor(beta, t, x, y, z, want_deriv_gam=True):
    """完整 4 维曲率：返回 G_{mu nu}（协变）与 G^{mu nu}（逆变）。

    实现：Christoffel（解析）→ ∂Gamma（解析，经 g2 与 gi1）→ Ricci → Einstein。
    """
    mb = metric_bundle(beta, t, x, y, z)
    g, gi, g1, g2 = mb['g'], mb['gi'], mb['g1'], mb['g2']
    B = mb['B']
    gam = christoffels(mb)

    # ∂_rho B（B = beta f；beta*f1v[rho]）——beta 由参数传入
    f1v = [mb['f1'] * mb['r1'][mu] for mu in range(4)]
    dB = [beta * f1v[mu] for mu in range(4)]

    # gi 的一阶导
    gi1 = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
    for rho in range(4):
        gi1[rho][0][1] = gi1[rho][1][0] = -dB[rho]
        gi1[rho][1][1] = -2.0 * B * dB[rho]

    # ∂_rho Gamma
    dgam = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for rho in range(4):
        for lam in range(4):
            for mu in range(4):
                for nu in range(4):
                    s = 0.0
                    for sig in range(4):
                        base = (g1[mu][sig][nu] + g1[nu][sig][mu]
                                - g1[sig][mu][nu])
                        s += (gi1[rho][lam][sig] * base
                              + gi[lam][sig] * (g2[rho][mu][sig][nu]
                                                + g2[rho][nu][sig][mu]
                                                - g2[rho][sig][mu][nu]))
                    dgam[rho][lam][mu][nu] = 0.5 * s

    # Ricci: R_{sigma nu} = ∂_rho G^rho_{nu sigma} - ∂_nu G^rho_{rho sigma}
    #                      + G^rho_{rho lam} G^lam_{nu sigma}
    #                      - G^rho_{nu lam} G^lam_{rho sigma}
    Ric = [[0.0] * 4 for _ in range(4)]
    for sig in range(4):
        for nu in range(4):
            s = 0.0
            for rho in range(4):
                s += dgam[rho][rho][nu][sig] - dgam[nu][rho][rho][sig]
            for rho in range(4):
                for lam in range(4):
                    s += (gam[rho][rho][lam] * gam[lam][nu][sig]
                          - gam[rho][nu][lam] * gam[lam][rho][sig])
            Ric[sig][nu] = s

    # Ricci 标量
    Rsc = 0.0
    for mu in range(4):
        for nu in range(4):
            Rsc += gi[mu][nu] * Ric[mu][nu]

    # Einstein 张量（协变）
    Gcov = [[0.0] * 4 for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            Gcov[mu][nu] = Ric[mu][nu] - 0.5 * g[mu][nu] * Rsc

    # 升指标
    Gup = [[0.0] * 4 for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            s = 0.0
            for a in range(4):
                for b in range(4):
                    s += gi[mu][a] * gi[nu][b] * Gcov[a][b]
            Gup[mu][nu] = s

    return {'Gcov': Gcov, 'Gup': Gup, 'g': g, 'gi': gi, 'B': B,
            'f': mb['f'], 'f1': mb['f1'], 'r': mb['r']}


def proj_rho_euler(res):
    """Euler 单位法向能量密度（T 值，几何单位 c=G=1）：
    T_{munu} n^mu n^nu = G_{munu} n^mu n^nu/(8 pi)，n=(1,B,0,0)。"""
    Gcov, B = res['Gcov'], res['B']
    n = [1.0, B, 0.0, 0.0]
    s = 0.0
    for mu in range(4):
        for nu in range(4):
            s += Gcov[mu][nu] * n[mu] * n[nu]
    return s / (8.0 * math.pi)


def proj_rho_mugao(res):
    """母稿处方（未归一 n=(1,-B,0,0)）对应的 T 值。"""
    Gcov, B = res['Gcov'], res['B']
    n = [1.0, -B, 0.0, 0.0]
    s = 0.0
    for mu in range(4):
        for nu in range(4):
            s += Gcov[mu][nu] * n[mu] * n[nu]
    return s / (8.0 * math.pi)


def proj_Ttt(res):
    """T^{tt}（逆变时间-时间分量，T 值，几何单位）。"""
    return res['Gup'][0][0] / (8.0 * math.pi)


def proj_Ttx(res):
    return res['Gup'][0][1] / (8.0 * math.pi)


def proj_Txx(res):
    return res['Gup'][1][1] / (8.0 * math.pi)


def adm_hamiltonian_rho(beta, t, x, y, z):
    """ADM 哈密顿约束路径（独立于 4 维实算）：
    rho_E = (K^2 - K_ij K^ij)/(16 pi)（平直空间切片，c=G=1）。
    K_ij = -(1/2)(∂_i N_j + ∂_j N_i)，N_j = -beta f delta_jx。
    """
    mb = metric_bundle(beta, t, x, y, z)
    f1, r1 = mb['f1'], mb['r1']
    # K 的非零分量（i,j 为空间指标 1,2,3；∂_1 = ∂_x, ∂_2 = ∂_y, ∂_3 = ∂_z）
    Kxx = -beta * f1 * r1[1]
    Kxy = -0.5 * beta * f1 * r1[2]
    Kxz = -0.5 * beta * f1 * r1[3]
    K = Kxx
    KijKij = Kxx * Kxx + 2 * Kxy * Kxy + 2 * Kxz * Kxz
    return (K * K - KijKij) / (16.0 * math.pi)


def alcubierre_literature_rho(beta, t, x, y, z):
    """文献公式（Alcubierre 1994；Varieschi & Burstein 2012 式 15）：
    T^{00} = -(1/8pi) (v_s^2 rho_cyl^2 / (4 r_s^2)) (df/dr_s)^2 ，rho_cyl=sqrt(y^2+z^2)。
    """
    mb = metric_bundle(beta, t, x, y, z)
    rho_cyl = math.sqrt(y * y + z * z)
    r_s = mb['r']
    return -(1.0 / (8.0 * math.pi)) * (beta * beta * rho_cyl * rho_cyl
                                       / (4.0 * r_s * r_s)) * mb['f1'] ** 2


def mugao_claim_rho(beta, t, x, y, z):
    """母稿处方声称值：rho = -(v_s^2/32 pi)(f')^2（c=G=1）。"""
    mb = metric_bundle(beta, t, x, y, z)
    return -(beta * beta * mb['f1'] ** 2) / (32.0 * math.pi)


# =============================================================================
# 2. 阳性对照与文献对拍（守卫）
# =============================================================================
BETA = 1.0   # v_s = c（母稿主算档）

# --- G-a: 平直对照 beta=0 ⇒ G_{munu} 全零 ---
res_flat = einstein_tensor(0.0, 0.0, 50.0, 30.0, 0.0)
FLAT_MAX = max(abs(res_flat['Gcov'][mu][nu])
               for mu in range(4) for nu in range(4))
guard('G-a-flat', FLAT_MAX < 1e-12,
      'beta=0 时度规恒为 Minkowski ⇒ Einstein 张量必须全零（曲率代码阳性对照），'
      '实测 max|G|=%s' % fv(FLAT_MAX, 3))

# --- G-b: 泡内 f'=0 ⇒ G_{munu} 全零 ---
res_inside = einstein_tensor(BETA, 0.0, 50.0, 0.0, 0.0)   # r_s=50 < R=100
INSIDE_MAX = max(abs(res_inside['Gcov'][mu][nu])
                 for mu in range(4) for nu in range(4))
guard('G-b-inside-flat', INSIDE_MAX < 1e-9,
      '泡内 f=const、f\'=0 ⇒ 度规为常系数（助推 Minkowski）⇒ 曲率必须全零，'
      '实测 max|G|=%s' % fv(INSIDE_MAX, 3))

# --- G-c: 泡外 f'=0 ⇒ G_{munu} 全零 ---
res_outside = einstein_tensor(BETA, 0.0, 500.0, 0.0, 0.0)  # r_s=500 >> R
OUTSIDE_MAX = max(abs(res_outside['Gcov'][mu][nu])
                  for mu in range(4) for nu in range(4))
guard('G-c-outside-flat', OUTSIDE_MAX < 1e-9,
      '泡外 f=0、f\'=0 ⇒ 度规平直 ⇒ 曲率必须全零，实测 max|G|=%s'
      % fv(OUTSIDE_MAX, 3))

# --- G-d: Christoffel 与 McMonigal-Lewis-O\'Byrne (arXiv:1202.5708) 式 (8)-(11) 对拍 ---
# 在 t-x 平面（y=z=0）常速情形：
#   (8)  Gamma^t_tt = -Gamma^x_tx = v_s^3 f^2 f'
#   (9)  Gamma^x_xx = v_s^2 f f'
#   (10) Gamma^t_xx = v_s f'
mb_axis = metric_bundle(BETA, 0.0, R_BUB, 0.0, 0.0)   # r_s=R, 轴上
gam_axis = christoffels(mb_axis)
f_ax, f1_ax = mb_axis['f'], mb_axis['f1']
CK = [
    ('Gamma^t_tt', gam_axis[0][0][0], BETA ** 3 * f_ax ** 2 * f1_ax),
    ('Gamma^x_tx', gam_axis[1][0][1], -BETA ** 3 * f_ax ** 2 * f1_ax),
    ('Gamma^x_xx', gam_axis[1][1][1], BETA ** 2 * f_ax * f1_ax),
    ('Gamma^t_xx', gam_axis[0][1][1], BETA * f1_ax),
]
CK_OK = all(abs(a - b) < 1e-9 * (1.0 + abs(b)) for _, a, b in CK)
guard('G-d-christoffel-literature', CK_OK,
      '4 个 Christoffel 与 McMonigal et al. 式 (8)(9)(10) 逐式对拍：' +
      '；'.join('%s: %.10e vs %.10e' % (nm, a, b) for nm, a, b in CK))

# =============================================================================
# 3. 三路径能量密度对比（壳层中平面 vs 轴上 vs 离轴）
# =============================================================================
SCAN_ANGLES = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0]   # 相对运动方向极角
SCAN = []
for th_deg in SCAN_ANGLES:
    th = math.radians(th_deg)
    x = R_BUB * math.cos(th)
    y = R_BUB * math.sin(th)
    res = einstein_tensor(BETA, 0.0, x, y, 0.0)
    SCAN.append({
        'theta_deg': th_deg,
        'rho_euler_4d': proj_rho_euler(res),
        'rho_euler_adm': adm_hamiltonian_rho(BETA, 0.0, x, y, 0.0),
        'rho_literature': alcubierre_literature_rho(BETA, 0.0, x, y, 0.0),
        'rho_mugao_claim': mugao_claim_rho(BETA, 0.0, x, y, 0.0),
        'Ttt': proj_Ttt(res), 'Ttx': proj_Ttx(res), 'Txx': proj_Txx(res),
    })

# 三路径一致性（最大相对偏差）
PATH_DEV = 0.0
for row in SCAN:
    a, b, cc = row['rho_euler_4d'], row['rho_euler_adm'], row['rho_literature']
    scale = max(abs(a), abs(b), abs(cc), 1e-30)
    PATH_DEV = max(PATH_DEV, abs(a - b) / scale, abs(a - cc) / scale)
guard('G-e-three-paths', PATH_DEV < 1e-8,
      '4 维实算 / ADM 哈密顿 / 文献公式（Varieschi 式 15）三路径能量密度一致，'
      '最大相对偏差 %s' % fv(PATH_DEV, 3))

# 母稿处方 vs 正确值：中平面（theta=90）应吻合；轴上（theta=0）母稿错
M_90 = [r for r in SCAN if r['theta_deg'] == 90.0][0]
M_0 = [r for r in SCAN if r['theta_deg'] == 0.0][0]
DEV_90 = abs(M_90['rho_euler_4d'] - M_90['rho_mugao_claim']) / abs(
    M_90['rho_euler_4d'])
DEV_0 = abs(M_0['rho_euler_4d'] - M_0['rho_mugao_claim'])
guard('G-f-mugao-midplane', DEV_90 < 1e-8,
      '母稿处方在中平面（theta=90）与 4 维实算吻合（相对偏差 %s）'
      '⇒ 母稿式 = 正确式的中平面切片' % fv(DEV_90, 3))
guard('G-g-mugao-axis-wrong', abs(M_0['rho_euler_4d']) < 1e-12
      and abs(M_0['rho_mugao_claim']) > 1e-6,
      '阳性对照：轴上（theta=0）4 维实算给 rho=0 而母稿式给非零 %s '
      '⇒ 母稿式的角度依赖缺失可被判出' % fv(M_0['rho_mugao_claim'], 4))

# 角因子机器积分：<rho_cyl^2/(4 r_s^2)> = <sin^2(theta)/4> 球平均 = 1/6
# 平均 = int int f sin(th) dth dphi / (4 pi) = sum f sin(th) dth * 2pi / (4 pi)
ANG_INT = 0.0
N_TH = 720
for i in range(N_TH):
    th = math.pi * (i + 0.5) / N_TH
    ANG_INT += (math.sin(th) ** 3) / 4.0
ANG_INT *= (math.pi / N_TH) * (2.0 * math.pi) / (4.0 * math.pi)
# 直接闭式：<sin^2>/4 = (2/3)/4 = 1/6
ANG_CLOSED = 1.0 / 6.0
guard('G-h-angular-average', abs(ANG_INT - ANG_CLOSED) < 1e-9,
      '角因子球平均机器积分 %s vs 闭式 1/6 = %s（偏差 %s）'
      % (fv(ANG_INT, 8), fv(ANG_CLOSED, 8),
         fv(abs(ANG_INT - ANG_CLOSED), 3)))

# =============================================================================
# 4. 中微子审计（Decimal 60 位）
# =============================================================================
M_NU = D('0.05')            # 中微子质量标度 eV（振荡实验要求 >0；宇宙学和对 <~0.1 eV）
NU_CASES = [('太阳 pp 中微子', '2.6e5'), ('反应堆中微子', '1e6'),
            ('大气中微子', '1e9'), ('IceCube TeV 中微子', '1e12')]
L_4_2LY = D('4.2') * LY
T_COORD = L_4_2LY / c
NU_ROWS = []
for lab, e_ev in NU_CASES:
    E = D(e_ev)                       # eV
    ratio = M_NU / E                  # dtau/dt = sqrt(1-beta^2) ≈ m c^2/E
    dtau = T_COORD * ratio
    NU_ROWS.append({'label': lab, 'E_eV': str(E), 'm_over_E': fv(ratio, 8),
                    'dtau_s': fv(dtau, 8), 'dtau_units': fv(dtau / D(1), 6)})
guard('G-i-neutrino-massive', all(D(r['dtau_s']) > 0 for r in NU_ROWS),
      '中微子有质量（振荡实验证明）⇒ 固有时间严格为正：'
      + '；'.join('%s dtau=%s s' % (r['label'], r['dtau_s']) for r in NU_ROWS))

# =============================================================================
# 5. Casimir 子议程可行性审计（Decimal）
# =============================================================================
CASIMIR_D = [D('1e-8'), D('1e-7'), D('1e-6')]      # 板间距 10 nm / 100 nm / 1 um
CASIMIR_ROWS = []
for d in CASIMIR_D:
    # 能量密度 u = -pi^2 hbar c / (720 d^4)；压强 p = -pi^2 hbar c / (240 d^4)
    u = -(PI ** 2) * hbar * c / (D(720) * d ** 4)
    p = -(PI ** 2) * hbar * c / (D(240) * d ** 4)
    CASIMIR_ROWS.append({'d_m': str(d), 'u_J_m3': fv(u, 8), 'p_Pa': fv(p, 8)})

# 母稿自身需求（§四式，v_s=c）：rho_alc = c^4/(32 pi G delta^2)
RHO_ALC = {}
for dl in [D('1'), D('0.1')]:
    RHO_ALC[str(dl)] = (c ** 4) / (D(32) * PI * G * dl ** 2)

# 最小间距（10 nm）下的差距
CAS_GAP = abs(RHO_ALC['1'] / D(CASIMIR_ROWS[0]['u_J_m3']))
guard('G-j-casimir-gap', CAS_GAP > D('1e30'),
      'Casimir 最强负能密度（10 nm 板）与母稿需求（delta=1 m, v_s=c）相差 %s 倍'
      % fv(CAS_GAP, 6))

# =============================================================================
# 6. 条目容器与判定
# =============================================================================
ITEMS = []


def add(code, verdict, title, detail, ev=''):
    ITEMS.append({'code': code, 'verdict': verdict, 'title': title,
                  'detail': detail, 'evidence': ev})


def PA(code, title, detail, ev=''):
    add(code, 'PASS', title, detail, ev)


def CO(code, title, detail, ev=''):
    add(code, 'CORRECTED', title, detail, ev)


def IN(code, title, detail, ev=''):
    add(code, 'INFO', title, detail, ev)


def MI(code, title, detail, ev=''):
    add(code, 'MISMATCH', title, detail, ev)


def BO(code, title, detail, ev=''):
    add(code, 'BOUNDARY', title, detail, ev)


# --- W01 承重：r64 C05/C05b 撤回；母稿度规 = Alcubierre 原始式 -------------
W01_NOTE = (
    '**本册最重要的单项发现：r64 C05 / C05b 的「度规基底错」裁定是错误的，现予撤回。**'
    'r64 C05 声称「Alcubierre 原式（及其后续全部文献变体）把形状函数作用在整个空间部分上：'
    'ds²=-c²dt²+f²(dx-v_s dt)²+g²dy²+h²dz²」，据此判母稿所写 '
    'ds²=-dt²+(dx-v_s f dt)²+dy²+dz² 为「非同一度规」并称 rho 公式不可移植。'
    '外部文献三路独立否证该前提：'
    '(1) McMonigal, Lewis & O\'Byrne（arXiv:1202.5708）式 (1) 逐字：'
    '「The Alcubierre metric Alcubierre 1994 can be described by '
    'ds²=-dt²+(dx-v_s(t)f(r_s)dt)²+dy²+dz²」——与母稿所写**完全相同**；'
    '(2) Varieschi & Burstein（arXiv:1208.3706）式 (10) 同一形式；'
    '(3) Santos-Pereira 博士论文（arXiv:2508.20348）与 Wikipedia 同。'
    'r64 引作「原式」的 f²-全空间形式实为 **Natário / van den Broeck 推广族**，'
    '不是 Alcubierre 1994 原始式。'
    '机器侧佐证：本册对母稿度规做完整 4 维解析曲率实算，其 Christoffel 与 '
    'McMonigal 等文式 (8)-(10) 逐式吻合（守卫 G-d），且泡内/泡外/平直三处'
    '曲率全零（G-a/G-b/G-c）——度规实现与文献同一。'
    '⇒ **撤回 r64 C05 / C05b**；母稿的度规书写正确，其 rho 公式确实可由该度规导出'
    '（导出方式见 W02：母稿式的角因子有缺，但不是「不可移植」）。'
    '这是本库「量纲/文献前提未核实即判 FAIL」缺陷族的又一实例，'
    '按 r66/r67 立下的跨册自纠纪律登记。')

CO('W01', '★承重：撤回 r64 C05/C05b——母稿度规就是 Alcubierre 1994 原始式（三文献源）',
   W01_NOTE,
   'christoffel_match=' + str(CK_OK) + ' | flat/inside/outside max|G|=%s/%s/%s'
   % (fv(FLAT_MAX, 2), fv(INSIDE_MAX, 2), fv(OUTSIDE_MAX, 2)))

# --- W02 承重：母稿 rho 式丢失角因子 --------------------------------------
W02_ROWS = []
for row in SCAN:
    W02_ROWS.append('theta=%g°: 实算=%s / 文献=%s / 母稿式=%s'
                    % (row['theta_deg'], fv(row['rho_euler_4d'], 6),
                       fv(row['rho_literature'], 6),
                       fv(row['rho_mugao_claim'], 6)))
W02_NOTE = (
    '母稿 §四 写 rho = -(v_s²/32πG)(df/dr_s)² ≤ 0 并称「壳层（f\'≠0）rho<0 …'
    '无法绕开的代数事实」。本册 4 维实算 + ADM 哈密顿约束 + 文献公式三路径一致给出'
    '（c=G=1）：rho_Euler = -(1/8π)(v_s² ρ_cyl²/(4 r_s²))(f\')²，'
    '其中 ρ_cyl = sqrt(y²+z²) 为到运动轴的圆柱半径——**含角因子 sin²θ/4**。'
    '逐角度机器扫描（r_s=R=100 m, v_s=c）：' + '；'.join(W02_ROWS) + '。'
    '⇒ 三条裁定：'
    '(a) **母稿式 = 正确式的中平面（θ=90°）切片**，被母稿当作全壳层均匀值使用'
    '（守卫 G-f：中平面吻合到 1e-8 以内，证明母稿式不是凭空错的，而是切片当全体）；'
    '(b) **在运动轴（θ=0°）上正确值为 0，母稿式给非零**（守卫 G-g）'
    '⇒ 母稿「只要 f\'≠0 就 rho<0」的「无法绕开」断言在轴上不成立；'
    '(c) 误差方向：母稿式在绝大多数角度上**高估** |rho|（最多在中平面之外'
    '无穷倍于轴上的真值 0），即母稿的能量障碍估计偏保守。'
    '球平均角因子 = 1/6（守卫 G-h 机器积分与闭式一致）⇒ 若母稿的 M_neg 估计'
    '用了中平面值当均匀值，真实壳层总负能量约为其 **1/6**——母稿把障碍报大了约 6 倍。'
    '此更正与 r64 A02/A03（v_s² 族唯一化）、E07（归因再定位）方向一致：'
    '母稿的精算偏大但否定结论（rho≤0、WEC 违反）不变。')

CO('W02', '★承重：母稿 rho 式丢失角因子 ρ²/(4r_s²)——中平面切片被当作全壳层值',
   W02_NOTE,
   'angular_average=%s | axis_true=%s vs mugao=%s'
   % (fv(ANG_CLOSED, 8), fv(M_0['rho_euler_4d'], 3),
      fv(M_0['rho_mugao_claim'], 6)))

# --- W03 WEC 违反方向确认且被文献加强 -------------------------------------
W03_NOTE = (
    '母稿「rho<0 ⇒ 违反 WEC」的**结论方向正确且比母稿所述更强**：'
    '机器实算确认壳层内 rho_Euler ≤ 0（中平面 = 母稿值，轴上 = 0，处处非正）；'
    '文献侧，Alcubierre 原论文经 Varieschi & Burstein 式 (15) 转述：'
    '「the energy density T^{00} is negative everywhere for any choice of the '
    'shaping function f and, therefore the WEC is violated (also DEC and SEC)」'
    '——即 **WEC / DEC / SEC 全部被违反且与形状函数选择无关**。'
    'McMonigal 等文进一步引 Lobo & Visser (2004) / Lobo (2007)：'
    '「the stress energy momentum tensor is negative for all observers, '
    'even when operating at arbitrarily low velocity」。'
    '⇒ 这同时补上了 r64 D01 标记的口径缺口：母稿只对 Euler 观测者论证，'
    '而文献早在 2004 年就给出了**对全部观测者**成立的更强版本。'
    '母稿此条 PASS（方向），但论证强度低于文献既有结果。')

PA('W03', 'WEC/DEC/SEC 违反方向确认，且文献给出比母稿更强的全观测者版本',
   W03_NOTE,
   'shell rho<=0 confirmed | literature: Varieschi eq.15 + Lobo-Visser 2004')

# --- W04 T^{tx}/T^{xx} 结构声称确认 ---------------------------------------
W04_NOTE = (
    '母稿 §四 末条声称「对应动量流 T^{tx}≠0 与应力 T^{xx} 亦非零：'
    '泡是『负能壳 + 定向动量流』结构」。本册 4 维实算（中平面壳点）给出：'
    'T^{tt} = %s、T^{tx} = %s、T^{xx} = %s（几何单位 c=G=1，乘 c⁴/G 得 SI）。'
    '⇒ T^{tx} ≠ 0 ✓、T^{xx} ≠ 0 ✓，母稿的结构声称成立。'
    '文献侧一致：Varieschi & Burstein Fig. 3 说明 T_{00}、T_{01}=T_{10}、'
    'T_{11}、T_{22}、T_{33} 在 x→-x 下对称而 T_{02}=T_{20}、T_{12}=T_{21} 不对称，'
    '即动量/应力分量确实非零且具有方向结构。'
    '（注意：此条成立**不依赖** W01 的更正——母稿结构声称本就与其度规自洽。）'
    % (fv(M_90['Ttt'], 6), fv(M_90['Ttx'], 6), fv(M_90['Txx'], 6)))

PA('W04', '母稿「负能壳 + 定向动量流」结构声称被 4 维实算确认（T^{tx}, T^{xx} 均非零）',
   W04_NOTE,
   'Ttt=%s Ttx=%s Txx=%s' % (fv(M_90['Ttt'], 8), fv(M_90['Ttx'], 8),
                             fv(M_90['Txx'], 8)))

# --- W05 中微子事实错误 ----------------------------------------------------
W05_NOTE = (
    '母稿 §一/§五 两处把**中微子**与光子并列为「质量为零 ⇒ 固有时间为 0」的'
    '「已观测」实例（「真命题、可观测（光子/中微子）」；'
    '判定矩阵「光子/中微子飞行固有时间为 0（已观测）」）。'
    '**这是事实错误**：中微子有质量——振荡实验（Super-K / SNO / Daya Bay 等）'
    '证明至少一个质量本征值 > 0（现行标度 m ≈ 0.05 eV 量级，宇宙学和对 Σm ≲ 0.1 eV）。'
    '机器精算（L = 4.2 ly，坐标时 t = %s s）：' % fv(T_COORD, 6) +
    '；'.join('%s（E=%s eV）: dτ/dt = m/E ≈ %s ⇒ dτ = %s s'
             % (r['label'], r['E_eV'], r['m_over_E'], r['dtau_s'])
             for r in NU_ROWS) + '。'
    '⇒ 中微子飞 4.2 光年的**固有时间是秒级到微秒级，不是 0**（太阳 pp 中微子约 '
    '25 秒；IceCube TeV 中微子约 7 微秒）——比光子的严格 0 差 5~8 个数量级，'
    '且**永远不为零**（只要 m>0）。只有光子（严格无质量）才满足 dτ≡0。'
    '⇒ 母稿钥匙 0 的「可观测实例」栏须删去中微子；钥匙 0 的命题本身'
    '（m=0 ⇒ 类光 ⇒ dτ=0）不受影响（光子仍成立），但 r64 B01 的补条件'
    '（E≠0）依旧必要。')

CO('W05', '中微子事实错误：有质量 ⇒ 固有时间非零（4.2 ly 上 25 秒 ~ 7 微秒）',
   W05_NOTE,
   'dtau: ' + ','.join('%s=%s s' % (r['label'], r['dtau_s'])
                       for r in NU_ROWS))

# --- W06 Casimir 子议程 ----------------------------------------------------
W06_NOTE = (
    '母稿 §五 子议程 3 提出「实验室负能『符号结构』工程：Casimir 腔 + 磁化等离子体，'
    '验证泡壳正/负应力符号可被工程化」，作为钥匙 1 的可测路径。'
    '机器审计（Casimir 能量密度 u = -π²ħc/(720d⁴)，压强 p = -π²ħc/(240d⁴)）：'
    + '；'.join('d=%s m: u=%s J/m³, p=%s Pa'
                % (r['d_m'], r['u_J_m3'], r['p_Pa']) for r in CASIMIR_ROWS) +
    '。对照母稿自身的需求（§四 式，v_s=c）：rho_alc = c⁴/(32πGδ²) = %s J/m³'
    '（δ=1 m）、%s J/m³（δ=0.1 m）。' % (RHO_ALC['1'], RHO_ALC['0.1']) +
    '⇒ 即便取实验室最强的负能密度（10 nm 板间距，已接近平版近似的失效边界），'
    '与需求相差 **%s 倍**（守卫 G-j）。' % fv(CAS_GAP, 6) +
    '⇒ 裁定：该子议程作为「应力符号结构」的**实验室类比**成立（Casimir 确有负压强，'
    '符号工程可做）；作为通往曲速泡负能量的**工程路径**不成立——差 37+ 个数量级，'
    '且量子不等式（r64 E05 已纠正的口径：压强×时长之积）对持续供给另设上限。'
    '母稿把「符号可工程化」与「能量可供给」混为一条，属本库「机制混淆并账」缺陷族。')

CO('W06', 'Casimir 子议程：符号工程可行，但能量供给差 37+ 个数量级（工程路径不成立）',
   W06_NOTE,
   'gap(10nm vs delta=1m)=%s' % fv(CAS_GAP, 6))

# --- W07 「完整量子引力才能算稳定性」逻辑错误 ------------------------------
W07_NOTE = (
    '母稿 §五 子议程 5 写「完整量子引力理论（弦/圈/因果集），才能算负能壳半经典稳定性」，'
    '并据此把钥匙 4 记为「❌ 未攻破（无完整量子引力理论）」。'
    '**这是逻辑错误：半经典稳定性恰恰不需要完整量子引力。**'
    '半经典稳定性 = 在**固定经典背景**上量化自由场并算重整化应力-能量张量（RSET），'
    '这是弯曲时空量子场论的常规计算。Finazzi, Liberati & Barceló '
    '（J. Phys. Conf. Ser. 222, 012046 (2010)；229, 012018 (2010)；'
    'arXiv:1001.4960）已经这样算了：超光速曲速泡的 RSET 显示泡的行为类似'
    '黑洞视界（产生 Hawking 型辐射），导致**半经典不稳定**。'
    '⇒ 裁定：钥匙 4 的状态应从「未攻破（等待量子引力）」改为'
    '「**半经典层次已有答案（不稳定）；完整量子引力的地位是『可能改变结论的上层建筑』'
    '而非『计算前提』**」。母稿把两层依赖性倒置了。'
    '（与 r236 V05 联动：那里纠正了 Krasnikov 的归属；这里纠正依赖链——'
    '两处合起来，钥匙 4 的文献状态是「有答案、答案是不稳定、归属不是 Krasnikov」。）')

CO('W07', '「完整量子引力才能算半经典稳定性」逻辑错误：RSET 半经典计算 2010 已给出（不稳定）',
   W07_NOTE,
   'Finazzi-Liberati-Barcelo JPCS 222,012046 / 229,012018 (2010)')

# --- W08 子议程 2 机制误指 -------------------------------------------------
W08_NOTE = (
    '母稿 §五 子议程 2 写「黑洞/德西特背景缓解：数值计算曲率泡嵌入后能量条件违背'
    '削减量（2026 方向）」，把「缓解」寄托在背景曲率上。'
    '文献检索未见「黑洞/德西特背景削减曲速泡 EC 违背」的方向；**实际存在的'
    '「缓解」文献是另外两个机制**：'
    '(1) **形状函数改写**：Varieschi & Burstein（arXiv:1208.3706）用 Hartle 形状函数'
    '（而非 Alcubierre 的 tanh 型）算出能量密度完全非负，WEC 在 v_s ≲ 2.50c 成立；'
    '(2) **修改引力**：同一工作在**共形引力**（而非 GR）框架下得到该结果——'
    '注意其 GR 框架下式 (15) 的结论是 WEC/DEC/SEC 全部违反。'
    '⇒ 双重裁定：'
    '(a) 母稿的机制指认错误（不是背景曲率缓解，是形状函数 + 修改引力）；'
    '(b) 更关键：该缓解**退出 GR**（共形引力是修改引力论），'
    '与母稿 §一/§六 自己的定性「曲率引擎完全在广义相对论内部钻空子」'
    '**自相矛盾**——母稿不能一边说缓解方向在 GR 内、一边引用必须改引力论的缓解。'
    '（与 r236 V02 联动：2026 的 Le 系列同样显示正能量路线在边界处仍违背 EC，'
    '即 2026 文献的实际方向是收紧；母稿「2026 有缓解方向」两处都指错。）')

CO('W08', '子议程 2 机制误指：实际「缓解」= Hartle 形状函数 + 共形引力（退出 GR），非背景曲率',
   W08_NOTE,
   'Varieschi-Burstein 1208.3706: HSF WEC-compliant up to v_s~2.50c IN conformal gravity')

# --- W09 七条子议程总表 ---------------------------------------------------
W09_TABLE = [
    ('1', '弯曲时空 QI 放宽（黑洞附近 Casimir 边界）', 'BOUNDARY',
     '方向本身可测，但无任何文献显示放宽量足以跨越 W02/W06 的 37+ 量级缺口'),
    ('2', '黑洞/德西特背景缓解', 'CORRECTED', '机制误指（W08）：实际是形状函数 + 修改引力，且退出 GR'),
    ('3', 'Casimir + 等离子体符号工程', 'CORRECTED', '符号工程可行；能量供给差 37+ 量级（W06）'),
    ('4', '时序保护猜想判定', 'CORRECTED', '已有构型级双向结果（r236 V04）'),
    ('5', '完整量子引力才能算稳定性', 'CORRECTED', '依赖链倒置：半经典 RSET 已给出（W07）'),
    ('6', 'Krasnikov 不稳定性量级估算', 'CORRECTED', '归属纠错（r236 V05）；量级文献在 Finazzi 等 2010'),
    ('7', '正能量亚光速泡做原型', 'CORRECTED', '仅限亚光速 + 边界违背 + exp(-3L) 燃料界（r236 V07）'),
]
W09_NOTE = (
    '母稿 §五 的 7 条子议程逐条审计（本册 W06/W07/W08 + r236 V04/V05/V07 已完成 6 条，'
    '第 1 条维持 BOUNDARY）：' +
    '；'.join('#%s %s ⇒ %s' % (n, t, v) for n, t, v, _ in W09_TABLE) +
    '⇒ **7 条中 0 条维持原判「可验证路径」原样、6 条 CORRECTED、1 条 BOUNDARY**。'
    '这不是说议程全错——第 1 条（弯曲时空 QI）仍是合法的可测方向，'
    '第 3 条的符号工程部分仍可做——而是说母稿把「可测方向」与「可攻破路径」'
    '混为一谈：可测 ≠ 能跨越数量级缺口。议程应改写为「测量计划」而非「攻破路线」。')

MI('W09', '七条子议程总审计：6 CORRECTED / 1 BOUNDARY / 0 条维持原判',
   W09_NOTE,
   'agendas=' + str(len(W09_TABLE)))

# --- W10 净立场 ------------------------------------------------------------
W10_NOTE = (
    '本册对 warp 线净立场的影响（汇总 r64–r67 + r236 + r238）：'
    '(1) **母稿的两处 factual error**：中微子固有时间（W05）、Krasnikov 归属'
    '（r236 V05，本册 W07 补依赖链）；'
    '(2) **母稿的一处 formula error**：rho 式缺角因子（W02，报大 ~6 倍，保守方向）；'
    '(3) **母稿的一处 metric 冤枉得雪**：r64 C05/C05b 撤回（W01），'
    '母稿度规书写正确——这是本库跨册自纠纪律的又一次执行（r66 撤回 E03b 之后）；'
    '(4) **母稿研究议程 7 条 6 更正**（W09），核心毛病是把「可测」当「可攻破」；'
    '(5) **四册否定结论全部维持**：C01/C04（v_s>c 泡内 dτ 虚）、E03/E06→r66/r67'
    '（QEI 五族四族排除 + 幸存族工程关闭）、r236（外部核实加强）均不受影响。'
    '⇒ 可引用的最终立场（r238 更新版）：'
    '「超光速曲率引擎在 GR 内部结构性不可行：v_s>c 使泡内运动学失去实定义；'
    'v_s→c⁻ 上 QEI 量纲闭合五族四族排除、仅存族壳厚锁死 10 ℓ_P、宏观泡负能量'
    '10⁶ 倍可观测宇宙质量；正能量路线仅限亚光速且 2026 年发现违背集中在源-真空边界、'
    '转向代价 exp(−3L)；半经典不稳定性文献归属 Finazzi-Liberati-Barceló 2010；'
    '母稿的度规书写正确（r64 C05 撤回）、rho 式缺角因子 sin²θ/4（报大约 6 倍）、'
    '中微子不是零固有时间实例。』')

IN('W10', '净立场：否定结论维持；母稿 2 事实错误 + 1 公式错误 + 1 跨册冤枉 + 议程 6 更正',
   W10_NOTE,
   'corrections_to_r64=1 (C05/C05b) | to_incoming=4 (W02/W05/W07/W08)')

# =============================================================================
# 主程序
# =============================================================================
def main():
    tally = {}
    for it in ITEMS:
        tally[it['verdict']] = tally.get(it['verdict'], 0) + 1
    order = ['PASS', 'FAIL', 'CORRECTED', 'MISMATCH', 'BOUNDARY', 'INFO']
    tally_txt = ' / '.join('%s=%d' % (k, tally.get(k, 0))
                           for k in order if k in tally)

    evidence = {
        'metric': 'ds^2 = -dt^2 + (dx - v_s f(r_s) dt)^2 + dy^2 + dz^2 '
                  '(Alcubierre 1994 original = incoming metric)',
        'positive_controls': {
            'beta0_maxG': fv(FLAT_MAX, 3),
            'inside_maxG': fv(INSIDE_MAX, 3),
            'outside_maxG': fv(OUTSIDE_MAX, 3),
        },
        'christoffel_literature_match': [[nm, fv(a, 10), fv(b, 10)]
                                         for nm, a, b in CK],
        'three_path_max_rel_dev': fv(PATH_DEV, 3),
        'angle_scan': [{'theta_deg': r['theta_deg'],
                        'rho_4d': fv(r['rho_euler_4d'], 8),
                        'rho_adm': fv(r['rho_euler_adm'], 8),
                        'rho_lit': fv(r['rho_literature'], 8),
                        'rho_mugao': fv(r['rho_mugao_claim'], 8),
                        'Ttt': fv(r['Ttt'], 8), 'Ttx': fv(r['Ttx'], 8),
                        'Txx': fv(r['Txx'], 8)} for r in SCAN],
        'angular_average_closed': fv(ANG_CLOSED, 8),
        'angular_average_numeric': fv(ANG_INT, 8),
        'midplane_match_rel_dev': fv(DEV_90, 3),
        'axis_true_vs_mugao': [fv(M_0['rho_euler_4d'], 3),
                               fv(M_0['rho_mugao_claim'], 6)],
        'neutrino_rows': NU_ROWS,
        'casimir_rows': CASIMIR_ROWS,
        'rho_alc_J_m3': {k: fv(v, 8) for k, v in RHO_ALC.items()},
        'casimir_gap': fv(CAS_GAP, 6),
        'agenda_table': [[n, t, v, d] for n, t, v, d in W09_TABLE],
        'refs': {
            'MCMONIGAL2012': 'arXiv:1202.5708 (Alcubierre metric eq.1; Christoffels eq.8-11)',
            'VARIESCHI2012': 'arXiv:1208.3706 (metric eq.10; T^00 eq.15 with angular factor)',
            'SANTOSPEREIRA2025': 'arXiv:2508.20348 (PhD thesis; warp drive metrics)',
            'FINAZZI2010': 'J.Phys.Conf.Ser. 222,012046 (2010); 229,012018 (2010); arXiv:1001.4960',
        },
    }

    summary = {
        'book': NAME,
        'date': '2026-10-26',
        'lineage': 'r64/r65/r66/r67 (audit+attack) -> r236 (external verification) '
                   '-> r238 (residual surface + cross-book self-correction)',
        'number_change': 'r200 (taken) -> r236 -> r237 (taken) -> r238',
        'rating': '母稿 2 事实错误 + 1 公式错误 + 1 跨册冤枉（r64 C05 撤回）；否定结论全部维持',
        'item_count': len(ITEMS),
        'tally': {k: tally.get(k, 0) for k in order},
        'tally_text': tally_txt,
        'guards_total': len(GUARD),
        'guards_passed': len([g for g in GUARD if g['ok']]),
        'items': ITEMS,
        'evidence': evidence,
    }

    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    with io.open(os.path.join(OUT, NAME + '.json'), 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(summary, ensure_ascii=False, indent=2))

    L = []
    L.append('# %s' % NAME)
    L.append('')
    L.append('- 日期：2026-10-26')
    L.append('- 承接：r64–r67 + r236 之后的母稿残余未攻面')
    L.append('- 方法：4 维解析曲率实算（Christoffel→Ricci→Einstein）+ 文献三源对拍')
    L.append('')
    L.append('## 汇总')
    L.append('')
    L.append('条目 %d（%s）' % (len(ITEMS), tally_txt))
    L.append('')
    L.append('守卫 %d / %d' % (len([g for g in GUARD if g['ok']]), len(GUARD)))
    L.append('')
    L.append('评级：%s' % summary['rating'])
    L.append('')
    L.append('## 守卫清单')
    L.append('')
    L.append('| 守卫 | 结果 | 说明 |')
    L.append('|---|---|---|')
    for g in GUARD:
        L.append('| %s | %s | %s |' % (g['guard'], 'PASS' if g['ok'] else 'FAIL',
                                       g['note']))
    L.append('')
    L.append('## 角度扫描（r_s=R=100 m, v_s=c，几何单位）')
    L.append('')
    L.append('| theta | 4维实算 | ADM | 文献式 | 母稿式 |')
    L.append('|---|---|---|---|---|')
    for r in SCAN:
        L.append('| %g° | %s | %s | %s | %s |'
                 % (r['theta_deg'], fv(r['rho_euler_4d'], 6),
                    fv(r['rho_euler_adm'], 6), fv(r['rho_literature'], 6),
                    fv(r['rho_mugao_claim'], 6)))
    L.append('')
    L.append('## 条目')
    L.append('')
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

    R = []
    R.append('=' * 78)
    R.append(NAME)
    R.append('2026-10-26  |  warp 母稿残余面攻破 + r64 C05 跨册自纠')
    R.append('=' * 78)
    R.append('条目: %d   %s' % (len(ITEMS), tally_txt))
    R.append('守卫: %d / %d' % (len([g for g in GUARD if g['ok']]), len(GUARD)))
    R.append('评级: %s' % summary['rating'])
    R.append('')
    R.append('-' * 78)
    R.append('守卫')
    R.append('-' * 78)
    for g in GUARD:
        R.append('[%s] %-28s %s' % ('PASS' if g['ok'] else 'FAIL', g['guard'],
                                    g['note'][:90]))
    R.append('')
    R.append('-' * 78)
    R.append('条目')
    R.append('-' * 78)
    for it in ITEMS:
        R.append('[%s] %s  %s' % (it['verdict'], it['code'], it['title']))
        R.append('')
    R.append('-' * 78)
    R.append('关键读数')
    R.append('-' * 78)
    R.append('母稿度规 = Alcubierre 1994 原始式（McMonigal eq.1 / Varieschi eq.10）')
    R.append('Christoffel 文献对拍 4/4 通过；平直/泡内/泡外曲率全零')
    R.append('rho 角因子: 母稿式=中平面值; 轴上真值 0; 球平均 1/6（母稿报大约 6 倍）')
    R.append('中微子 dtau(4.2ly): 太阳 25s ~ TeV 7us（非零！）')
    R.append('Casimir(10nm)/需求(delta=1m) = %s 倍' % fv(CAS_GAP, 6))
    R.append('')
    with io.open(os.path.join(OUT, NAME + '_report.txt'), 'w',
                 encoding='utf-8') as fh:
        fh.write('\n'.join(R) + '\n')

    print('=' * 78)
    print(NAME)
    print('条目 %d   %s' % (len(ITEMS), tally_txt))
    print('守卫 %d / %d' % (len([g for g in GUARD if g['ok']]), len(GUARD)))
    print('=' * 78)
    print('角度扫描 (theta: 4d / adm / lit / mugao):')
    for r in SCAN:
        print('  %5.1f°  %12.6e %12.6e %12.6e %12.6e'
              % (r['theta_deg'], r['rho_euler_4d'], r['rho_euler_adm'],
                 r['rho_literature'], r['rho_mugao_claim']))
    print('Christoffel 文献对拍: %s' % CK_OK)
    print('Casimir gap: %s' % fv(CAS_GAP, 6))
    print('产物: %s.json / .md / _report.txt' % NAME)
    bad = [g['guard'] for g in GUARD if not g['ok']]
    if bad:
        print('GUARD FAILED: %s' % bad)
        return 1
    print('GUARD ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
