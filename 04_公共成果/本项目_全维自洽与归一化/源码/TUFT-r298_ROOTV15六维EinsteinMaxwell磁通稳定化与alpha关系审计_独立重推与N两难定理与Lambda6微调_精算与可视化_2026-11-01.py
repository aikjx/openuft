# -*- coding: utf-8 -*-
"""
TUFT-r298 · 2026-11-01 · ROOT V15.0《六维空间几何、磁通与精细结构常数联合攻坚》全维审计
独立重推 / 数值复算 / N-两难定理 / Lambda6 微调定价 / 反常与三代继承登记

来料主张（五条）：
  T1  六维 Einstein-Maxwell 作用量 + S^2 磁通 => 半径被场方程选出 r_*^2 = N^2/(4 g6^2 M6^4)
  T2  降维势自动出现 V_E = 2*pi*M6^4*(r_*/r)^4*(r/r_* - r_*/r)^2 >= 0，极小在 r_*，势垒在 sqrt3
  T3  体积模 phi = 2*M4*ln(r/r_*)，m_phi^2 = 1/r_*^2
  T4  alpha_4 = (xi/(2*pi*N))^2，xi = g6^2*M6^2 仍自由 => 不能无参数预测 alpha
  T5  N=3 => 手征指标 3 => 三代（来料自注：电荷/表示/质量/反常仍需逐项检查）

本册做法：不引用来料代码与来料数值表，全部从作用量独立重推，
60 位 Decimal 复算 + Fraction 三元组量纲 (M,L,T) 齐次性机检。
纯标准库；rc=0；stdout 仅 ASCII 摘要（中文细节全部落盘）。
"""
from __future__ import division, print_function

import io
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

# ---------------------------------------------------------------- 常量与工具
def D(x):
    return Decimal(str(x))

def Ds(x):
    """定点输出：Decimal 到 25 位科学计数（quantize 在高位数下会抛 InvalidOperation）"""
    return format(x, '.25E')

def fs(x, n=20):
    return format(x, '.' + str(n) + 'E')

PI = D('3.141592653589793238462643383279502884197169399375105820974944')
TWO = D(2)

ALPHA_INV = D('137.035999177')          # CODATA 2022
ALPHA = D(1) / ALPHA_INV
HBARC = D('1.973269804e-16')            # GeV*m
L_PLANCK = D('1.616255e-35')            # m （非约化）
M_PL_C2 = HBARC / L_PLANCK              # GeV  非约化普朗克质能
M_P_RED = M_PL_C2 / (8 * PI).sqrt()     # GeV  约化普朗克质能 M4
RHO_LAMBDA = D('2.518e-47')             # GeV^4 观测暗能量密度（与 r292 同口径便于交叉）

# ---------------------------------------------------------------- 量纲工具 (M,L,T)
# 自然单位 hbar=c=1：质量维 = M - L - T
ZERO = (Fraction(0), Fraction(0), Fraction(0))

def dmul(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def ddiv(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def dpow(a, n):
    n = Fraction(n)
    return (a[0] * n, a[1] * n, a[2] * n)

def massdim(a):
    return a[0] - a[1] - a[2]

def dstr(a):
    out = []
    for sym, v in zip('MLT', a):
        if v == 0:
            continue
        out.append('%s^%s' % (sym, v))
    return ''.join(out) if out else '1'

DIM_M6 = (Fraction(1), Fraction(0), Fraction(0))       # M6
DIM_R6 = (Fraction(0), Fraction(-2), Fraction(0))      # R_6 ~ 1/L^2
DIM_G6 = (Fraction(0), Fraction(1), Fraction(0))       # g6 (mass dim -1)
DIM_RAD = (Fraction(0), Fraction(1), Fraction(0))      # r_*
DIM_LAM6 = (Fraction(0), Fraction(-2), Fraction(0))    # Lambda_6
DIM_V4 = (Fraction(4), Fraction(0), Fraction(0))       # 4D 势密度
DIM_M4 = (Fraction(1), Fraction(0), Fraction(0))       # M4

# ---------------------------------------------------------------- 条目收集
ENTRIES = []
GUARDS = []

def add(code, verdict, title, detail, key=None):
    ENTRIES.append({
        'code': code,
        'verdict': verdict,
        'title': title,
        'detail': detail,
        'key': key or {},
    })

def guard(name, ok, detail):
    GUARDS.append({'name': name, 'ok': bool(ok), 'detail': detail})
    return bool(ok)

# ---------------------------------------------------------------- 量纲守卫（工具自身先过自检）
def _g_dim():
    ok = True
    # S6 = int d^6x sqrt(-G) [ M6^4/2 (R6 - 2 Lam6) - 1/(4 g6^2) F^2 ]，作用量无量纲
    # 注意：量纲元组的 '+' 是 tuple 拼接，必须用 dmul（本库第 N 次同款事故）
    dim_S_grav = dmul(dpow(DIM_M6, 4), dmul(DIM_R6, (Fraction(0), Fraction(6), Fraction(0))))
    ok &= guard('G0-1 引力作用量项质量维=0', massdim(dim_S_grav) == 0,
                'massdim=%s' % massdim(dim_S_grav))
    # Maxwell 项： [F]=2 => [F^2]=4 ; int d^6x = -6 ; 需 [1/g6^2] = 2
    dim_F2 = (Fraction(0), Fraction(-4), Fraction(0))
    dim_inv_g2 = dpow(DIM_G6, -2)
    ok &= guard('G0-2 [1/g6^2] 质量维=2', massdim(dim_inv_g2) == 2,
                'massdim=%s' % massdim(dim_inv_g2))
    dim_S_max = dmul((Fraction(0), Fraction(6), Fraction(0)), dmul(dim_inv_g2, dim_F2))
    ok &= guard('G0-3 Maxwell 作用量项质量维=0', massdim(dim_S_max) == 0,
                'massdim=%s' % massdim(dim_S_max))
    # r_*^2 = N^2/(4 g6^2 M6^4)：只判质量维（元组因含 M6^4 携带 M 分量，不做字面相等）
    dim_r2 = ddiv(ZERO, dmul(dpow(DIM_G6, 2), dpow(DIM_M6, 4)))
    ok &= guard('G0-4 [r_*^2] 质量维=-2',
                massdim(dim_r2) == -2 and massdim(dpow(DIM_RAD, 2)) == -2,
                'dim=%s' % dstr(dim_r2))
    # xi = g6^2 M6^2 无量纲
    dim_xi = dmul(dpow(DIM_G6, 2), dpow(DIM_M6, 2))
    ok &= guard('G0-5 xi=g6^2*M6^2 无量纲', massdim(dim_xi) == 0, 'dim=%s' % dstr(dim_xi))
    # M4^2 = 4 pi r_*^2 M6^4
    dim_M42 = dmul(dpow(DIM_RAD, 2), dpow(DIM_M6, 4))
    ok &= guard('G0-6 [M4^2] 质量维=2', massdim(dim_M42) == 2, 'dim=%s' % dstr(dim_M42))
    return ok

_G_DIM_OK = _g_dim()

# ---------------------------------------------------------------- 模型基本式（本册独立书写）
def F2_of(N, r):
    """F_AB F^{AB} = 2 F_{th,ph} F^{th,ph} = N^2/(2 r^4)"""
    return (D(N) ** 2) / (2 * r ** 4)

def T_in_coef(N, g6sq, r):
    """T_ij = coef * G_ij（内部 S^2 块）"""
    return (D(N) ** 2) / (8 * D(g6sq) * r ** 4)

def T_out_coef(N, g6sq, r):
    """T_{mu nu} = coef * G_{mu nu}（外部 4D 块）"""
    return -(D(N) ** 2) / (8 * D(g6sq) * r ** 4)

def rstar_sq(N, g6sq, M6):
    return (D(N) ** 2) / (4 * D(g6sq) * M6 ** 4)

def lam6_sol(N, g6sq, M6):
    return 2 * D(g6sq) * M6 ** 4 / (D(N) ** 2)

def V_E_open(r, rs, M6, Lam6, N, g6sq):
    """来料第二节原式（含 Weyl 因子 (r_*/r)^4）"""
    return 4 * PI * (rs / r) ** 4 * (-M6 ** 4 + M6 ** 4 * Lam6 * r ** 2
                                     + (D(N) ** 2) / (8 * D(g6sq) * r ** 2))

def V_E_closed(r, rs, M6):
    """化简闭式 2*pi*M6^4*(r_*/r)^4*(r/r_* - r_*/r)^2"""
    x = r / rs
    return 2 * PI * M6 ** 4 * x ** (-4) * (x - 1 / x) ** 2

# ---------------------------------------------------------------- 6D Ricci 数值器（供 A05/A11 独立校验）
def make_geom(r0, eps, k, torus=False):
    """ds^2 = dx_4^2(Euclid) + r(x1)^2 [dth^2 + sin^2 th dph^2]（torus=True 时内部取平直 T^2）"""
    def r_of(x1):
        return r0 * (1.0 + eps * math.sin(k * x1))
    def dr_of(x1):
        return r0 * eps * k * math.cos(k * x1)
    def d2r_of(x1):
        return -r0 * eps * k * k * math.sin(k * x1)
    def gam(x1, th):
        # ★闭包变量严禁与下方循环变量同名：曾因循环变量 c 覆盖 cos(th) 使 Christoffel 错 11 倍
        rr = r_of(x1); dr = dr_of(x1)
        sn = math.sin(th); cs = math.cos(th)
        g44 = rr * rr
        g55 = rr * rr * (1.0 if torus else sn * sn)
        i44 = 1.0 / g44; i55 = 1.0 / g55
        def dg(b, i, j):
            if b == 0:
                if i == 4 and j == 4:
                    return 2.0 * rr * dr
                if i == 5 and j == 5:
                    return 2.0 * rr * dr * (1.0 if torus else sn * sn)
                return 0.0
            if b == 4 and (not torus):
                if i == 5 and j == 5:
                    return 2.0 * rr * rr * sn * cs
                return 0.0
            return 0.0
        G = [[[0.0] * 6 for _ in range(6)] for _ in range(6)]
        for aa in range(6):
            ga = 1.0 if aa < 4 else (i44 if aa == 4 else i55)
            for bb in range(6):
                for cc in range(6):
                    G[aa][bb][cc] = 0.5 * ga * (dg(bb, aa, cc) + dg(cc, aa, bb) - dg(aa, bb, cc))
        return G, [1.0] * 4 + [i44, i55]
    return r_of, dr_of, d2r_of, gam

def ricci_scalar(geom, x1, th, h=1e-5):
    gam = geom[3]
    G, ginv = gam(x1, th)
    dmap = {}
    for lam in (0, 4):
        dx = h if lam == 0 else 0.0
        dt = h if lam == 4 else 0.0
        Gp, _ = gam(x1 + dx, th + dt)
        Gm, _ = gam(x1 - dx, th - dt)
        dmap[lam] = [[[(Gp[a][b][c] - Gm[a][b][c]) / (2.0 * h)
                       for c in range(6)] for b in range(6)] for a in range(6)]
    def dgam(lam, a, b, c):
        M = dmap.get(lam)
        return M[a][b][c] if M is not None else 0.0
    Rmn = [[0.0] * 6 for _ in range(6)]
    for m in range(6):
        for n in range(6):
            s = 0.0
            for lam in range(6):
                s += dgam(lam, lam, m, n)
                s -= dgam(n, lam, m, lam)
                for rho in range(6):
                    s += G[lam][lam][rho] * G[rho][m][n]
                    s -= G[lam][n][rho] * G[rho][m][lam]
            Rmn[m][n] = s
    Rs = 0.0
    for i in range(6):
        Rs += ginv[i] * Rmn[i][i]
    return Rs, Rmn, ginv

# ================================================================ A 段 · 独立重推与机器核对
def _simpson(f, a, b, n):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += f(a + i * h) * (4 if i % 2 else 2)
    return s * h / 3

# ---- A01 磁通量子化
def _A01():
    N = D(3); R = D('2.3')
    f = lambda th: float((N / 2) * D(str(math.sin(th))))
    val = D(str(_simpson(f, 1e-9, math.pi - 1e-9, 4000))) * 2 * PI
    target = 2 * PI * N
    rel = abs(val - target) / abs(target)
    ok = rel < D('1e-9')
    add('A01', 'PASS' if ok else 'FAIL', '磁通量子化 ∮F = 2πN 与 F_{θφ}=(N/2)sinθ 自洽',
        'Simpson(n=4000) 积分得 %s，目标 2πN=%s，相对残差 %s' % (Ds(val), Ds(target), Ds(rel)),
        {'flux_num': Ds(val), 'flux_target': Ds(target), 'rel': Ds(rel)})
    return ok

# ---- A02 F^2 不变量
def _A02():
    N = D(3); R = D('2.3')
    vals = []
    for th_s in ('0.3', '0.9', '1.4', '2.0', '2.8'):
        th = D(th_s)
        s = D(str(math.sin(float(th))))
        Fthph = (N / 2) * s
        Fup = Fthph / (R ** 2) / (R ** 2 * s ** 2)      # F^{θφ}
        vals.append(2 * Fthph * Fup)
    tgt = F2_of(N, R)
    spread = max(vals) - min(vals)
    rel = abs(vals[0] - tgt) / tgt
    ok = abs(spread) < D('1e-40') and rel < D('1e-40')
    add('A02', 'PASS' if ok else 'FAIL', 'F_{AB}F^{AB} = N^2/(2r^4) 且与 θ 无关',
        '5 个 θ 取值散布 %s；与闭式相对残差 %s（θ 依赖精确相消）' % (Ds(spread), Ds(rel)),
        {'F2': Ds(tgt), 'spread': Ds(spread), 'rel': Ds(rel)})
    return ok

# ---- A03 Maxwell 方程（含 1/sinθ 抵消）
def _A03():
    N = D(3); R = D('2.3')
    qs = []
    for th_s in ('0.3', '0.9', '1.4', '2.0', '2.8'):
        th = D(th_s)
        s = D(str(math.sin(float(th))))
        sqG = R ** 2 * s                                  # sqrt(-G)（4D 部分取 1）
        Fup = (N / 2) * s / (R ** 2) / (R ** 2 * s ** 2)   # F^{θφ}
        qs.append(sqG * Fup)
    spread = max(qs) - min(qs)
    tgt = N / (2 * R ** 2)
    rel = abs(qs[0] - tgt) / abs(tgt)
    ok = abs(spread) < D('1e-45') and rel < D('1e-45')
    add('A03', 'PASS' if ok else 'FAIL', 'Maxwell 方程 ∇_A F^{AB}=0 被单极背景满足',
        '√(-G)F^{θφ} 在 5 个 θ 上恒为 N/(2r^2)：散布 %s、与闭式相对残差 %s'
        % (Ds(spread), Ds(rel)), {'spread': Ds(spread), 'rel': Ds(rel)})
    return ok

# ---- A04/A05 Einstein 方程（内/外部块）独立重推
def _resid_pair(r, Lam6, N, g6sq, M6):
    """返回 (内部残差, 外部残差)：LHS/G - RHS/G"""
    lhs_in = M6 ** 4 * (D(1) / r ** 2 - D(1) / r ** 2 + Lam6)
    rhs_in = T_in_coef(N, g6sq, r)
    lhs_out = M6 ** 4 * (Lam6 - D(1) / r ** 2)
    rhs_out = T_out_coef(N, g6sq, r)
    return lhs_in - rhs_in, lhs_out - rhs_out

def _A04_A05():
    N = D(3); g6sq = D('0.81'); M6 = D('1.7')
    rs = (rstar_sq(N, g6sq, M6)).sqrt()
    L6 = lam6_sol(N, g6sq, M6)
    ri_in, ri_out = _resid_pair(rs, L6, N, g6sq, M6)
    scale = M6 ** 4 * L6
    rel_in = abs(ri_in) / scale
    rel_out = abs(ri_out) / scale
    # 离解控制：r 取 1.5 r_*
    ri_in2, ri_out2 = _resid_pair(rs * D('1.5'), L6, N, g6sq, M6)
    rel_in2 = abs(ri_in2) / scale
    ok = rel_in < D('1e-50') and rel_out < D('1e-50') and rel_in2 > D('1e-3')
    add('A04', 'PASS' if ok else 'FAIL',
        '内部 Einstein 方程 M6^4 Λ6 = N^2/(8 g6^2 r^4) 独立重推成立',
        '由 Ricci_ij=(1/r^2)G_ij、R6=2/r^2、T_ij=(1/g6^2)(F_ik F_j^k - 1/4 G_ij F^2) '
        '重推得 LHS/G=M6^4Λ6（Ricci 与 1/2 项精确相消）；解点相对残差 %s；'
        '离解控制 r=1.5r_* 残差 %s（判据有牙齿）' % (Ds(rel_in), Ds(rel_in2)),
        {'rel_in': Ds(rel_in), 'rel_off': Ds(rel_in2)})
    add('A05', 'PASS' if ok else 'FAIL',
        '外部 Einstein 方程 M6^4(Λ6 - 1/r^2) = -N^2/(8 g6^2 r^4) 独立重推成立',
        '外部块 Ricci=0、R6=2/r^2 ⇒ LHS/G = M6^4(Λ6-1/r^2)；解点相对残差 %s；'
        '离解控制残差 %s' % (Ds(rel_out), Ds(abs(ri_out2) / scale)),
        {'rel_out': Ds(rel_out), 'rel_off': Ds(abs(ri_out2) / scale)})
    return ok

# ---- A05b 6D Ricci 数值校验（不引用 KK 公式）
def _A05b():
    R0 = 2.3
    geom = make_geom(R0, 0.0, 1.0)
    Rs, Rmn, ginv = ricci_scalar(geom, 0.7, 1.1)
    tgt = 2.0 / R0 ** 2
    rel = abs(Rs - tgt) / tgt
    # 内部 Ricci 分量：R_θθ=1, R_φφ=sin^2 θ
    r_thth = Rmn[4][4]
    r_phph = Rmn[5][5] / (math.sin(1.1) ** 2)
    ok = rel < D('1e-8') and abs(r_thth - 1.0) < 1e-8 and abs(r_phph - 1.0) < 1e-8
    add('A05b', 'PASS' if ok else 'FAIL', '6D Ricci 数值器自检：R6=2/r^2、R_ij=(1/r^2)G_ij',
        '数值 Christoffel→Ricci 得 R6=%s，闭式 2/r^2=%s，相对残差 %s；'
        'R_θθ=%s（应 1）、R_φφ/sin^2θ=%s（应 1）'
        % (fs(D(str(Rs)), 12), fs(D(str(tgt)), 12), fs(D(str(rel)), 8),
           fs(D(str(r_thth)), 8), fs(D(str(r_phph)), 8)),
        {'R6_num': fs(D(str(Rs)), 12), 'rel': fs(D(str(rel)), 8)})
    return ok

# ---- A06 联立解
def _A06():
    N = D(3); g6sq = D('0.81'); M6 = D('1.7')
    rs2 = rstar_sq(N, g6sq, M6)
    L6 = lam6_sol(N, g6sq, M6)
    # 直接由两式相加/代入检验
    s1 = M6 ** 4 * (L6 - D(1) / rs2) + (D(N) ** 2) / (8 * g6sq * rs2 ** 2)
    s2 = M6 ** 4 * L6 - (D(N) ** 2) / (8 * g6sq * rs2 ** 2)
    sc = M6 ** 4 * L6
    r1 = abs(s1) / sc; r2 = abs(s2) / sc
    # 另一路：由两式推出 Λ6 r_*^2 = 1/2
    half = L6 * rs2
    ok = r1 < D('1e-50') and r2 < D('1e-50') and abs(half - D('0.5')) < D('1e-50')
    add('A06', 'PASS' if ok else 'FAIL', '联立解 r_*^2=N^2/(4g6^2M6^4)、Λ6=2g6^2M6^4/N^2 成立',
        '两式残差 %s / %s；且 Λ6 r_*^2 = %s = 1/2（独立副产物）'
        % (Ds(r1), Ds(r2), Ds(half)), {'rel1': Ds(r1), 'rel2': Ds(r2), 'Lam6_r2': Ds(half)})
    return ok

# ---- A07 迹方程交叉验证
def _A07():
    N = D(3); g6sq = D('0.81'); M6 = D('1.7')
    rs = (rstar_sq(N, g6sq, M6)).sqrt(); L6 = lam6_sol(N, g6sq, M6)
    R6 = D(2) / rs ** 2
    lhs_trace = M6 ** 4 * (R6 - 3 * R6 + 6 * L6)            # D=6 取迹
    T_trace = -(D(1) / (2 * g6sq)) * F2_of(N, rs)            # Maxwell 迹 = -(1/(2g6^2))F^2
    rel = abs(lhs_trace - T_trace) / abs(T_trace)
    # 分块求和交叉：4*外部 + 2*内部
    blk = 4 * T_out_coef(N, g6sq, rs) + 2 * T_in_coef(N, g6sq, rs)
    rel2 = abs(blk - T_trace) / abs(T_trace)
    ok = rel < D('1e-50') and rel2 < D('1e-50')
    add('A07', 'PASS' if ok else 'FAIL', '迹方程交叉验证（4×外部 + 2×内部 = 全迹）',
        'M6^4(-2R6+6Λ6) 与 Maxwell 迹 -(1/2g6^2)F^2 相对残差 %s；'
        '分块求和 4·(-N^2/8g6^2r^4)+2·(+N^2/8g6^2r^4) 与全迹相对残差 %s'
        % (Ds(rel), Ds(rel2)), {'rel_trace': Ds(rel), 'rel_block': Ds(rel2)})
    return ok

# ---- A08 降维势（Weyl 因子与 M4^2 归一）
def _A08():
    N = D(3); g6sq = D('0.81'); M6 = D('1.7')
    rs = (rstar_sq(N, g6sq, M6)).sqrt(); L6 = lam6_sol(N, g6sq, M6)
    M4sq = 4 * PI * rs ** 2 * M6 ** 4
    # Jordan 引力项系数 A/2 = (M6^4/2)*4πr_*^2 ⇒ A = M4^2（在 r=r_* 归一化）
    A = 4 * PI * rs ** 2 * M6 ** 4
    relA = abs(A - M4sq) / M4sq
    # B(r) = 4π[-M6^4 + M6^4 Λ6 r^2 + N^2/(8g6^2 r^2)]；V_E = Ω^{-4} B，Ω^2 = r^2/r_*^2
    r = rs * D('1.37')
    Om2 = r ** 2 / rs ** 2
    B = 4 * PI * (-M6 ** 4 + M6 ** 4 * L6 * r ** 2 + (D(N) ** 2) / (8 * g6sq * r ** 2))
    v1 = B / (Om2 ** 2)
    v2 = V_E_open(r, rs, M6, L6, N, g6sq)
    rel = abs(v1 - v2) / (abs(v2) + D('1e-60'))
    ok = relA < D('1e-50') and rel < D('1e-50')
    add('A08', 'PASS' if ok else 'FAIL', '降维势 V_E 的 Weyl 因子 (r_*/r)^4 与 M4^2=4πr_*^2M6^4 归一',
        'A=4πr_*^2M6^4=M4^2 相对残差 %s；V_E=Ω^{-4}B(r) 与来料原式相对残差 %s'
        % (Ds(relA), Ds(rel)),
        {'rel_A': Ds(relA), 'rel_V': Ds(rel), 'M4sq': Ds(M4sq)})
    return ok

# ---- A09 闭式恒等（500 点）
def _A09():
    N = D(3); g6sq = D('0.81'); M6 = D('1.7')
    rs = (rstar_sq(N, g6sq, M6)).sqrt(); L6 = lam6_sol(N, g6sq, M6)
    worst = D(0); worst_x = None
    for i in range(500):
        x = D('0.05') + D(i) * D('0.019')
        r = rs * x
        a = V_E_open(r, rs, M6, L6, N, g6sq)
        b = V_E_closed(r, rs, M6)
        rel = abs(a - b) / (abs(b) + D('1e-60'))
        if rel > worst:
            worst = rel; worst_x = x
    ok = worst < D('1e-45')
    add('A09', 'PASS' if ok else 'FAIL', 'V_E 原式 ≡ 2πM6^4 x^{-4}(x-1/x)^2（500 点）',
        '500 点最大相对残差 %s（x=%s）。注：来料称 1.07e-70，属其精度设置；'
        '本库 60 位下残差停在 %s —— 该残差是恒等式精度而非物理证据（与 r292 对 1.73e-77 同口径）'
        % (Ds(worst), Ds(worst_x), Ds(worst)), {'worst_rel': Ds(worst)})
    return ok

# ---- A10 极小点与势垒
def _A10():
    N = D(3); g6sq = D('0.81'); M6 = D('1.7')
    rs = (rstar_sq(N, g6sq, M6)).sqrt()
    # 数值扫描找极大
    best = (None, D(-1))
    for i in range(1, 4000):
        x = D(1) + D(i) * D('0.0025')
        v = V_E_closed(rs * x, rs, M6)
        if v > best[1]:
            best = (x, v)
    xmax = best[0]
    rel_bar = abs(xmax - (D(3)).sqrt()) / (D(3)).sqrt()
    # 势垒高度
    vb = V_E_closed(rs * (D(3)).sqrt(), rs, M6)
    tgt = 8 * PI * M6 ** 4 / D(27)
    rel_v = abs(vb - tgt) / tgt
    # 极小：V(1)=0 且两侧为正
    v_eps = V_E_closed(rs * D('1.01'), rs, M6)
    ok = rel_bar < D('1e-3') and rel_v < D('1e-45') and v_eps > 0 \
         and abs(V_E_closed(rs, rs, M6)) < D('1e-50')
    add('A10', 'PASS' if ok else 'FAIL', 'V_E≥0、极小在 r=r_*、去紧致化势垒在 x=√3',
        '数值极大点 x_max=%s（√3 相对偏差 %s）；V_E(√3)=8πM6^4/27 相对残差 %s；'
        'V(1.01r_*)>0、V(r_*)=0' % (Ds(xmax), Ds(rel_bar), Ds(rel_v)),
        {'x_max': Ds(xmax), 'rel_sqrt3': Ds(rel_bar), 'barrier_over_M6^4': Ds(vb / M6 ** 4)})
    return ok

# ---- A11 radion 正则化（6D 曲率分解 + Weyl 重标定）
def _A11():
    r0 = 2.3; eps = 0.02; k = 1.7
    geom = make_geom(r0, eps, k)
    r_of, dr_of, d2r_of, _ = geom
    worst = 0.0; sample = None
    for x1 in (0.3, 0.9, 1.5):
        for th in (0.7, 1.3):
            Rs, _, _ = ricci_scalar(geom, x1, th)
            r = r_of(x1); dr = dr_of(x1); d2r = d2r_of(x1)
            lap_beta = (d2r * r - dr * dr) / (r * r)      # ∇²β（4D 欧氏，仅 x1 依赖）
            db2 = (dr / r) ** 2
            form = 0.0 - 4.0 * lap_beta - 6.0 * db2 + 2.0 / r ** 2
            rel = abs(Rs - form) / max(abs(form), 1e-12)
            if rel > worst:
                worst = rel; sample = (Rs, form)
    ok_num = worst < 1e-6
    # Weyl 重标定系数（Fraction 精确）
    c_weyl = Fraction(-3)          # -3 M4^2 (∂lnΩ)^2
    c_jordan = Fraction(1)         # 4πM6^4 Ω^{-2} (∂r)^2 = M4^2 (∂ln r)^2
    total = c_weyl + c_jordan      # = -2 ⇒ -2 M4^2 (∂ln r)^2
    canon = Fraction(-1, 2) * Fraction(2) ** 2   # φ = 2 M4 ln r ⇒ -½(∂φ)^2 系数
    ok_alg = (total == canon == Fraction(-2)) and ok_num
    add('A11', 'PASS' if ok_alg else 'FAIL', '体积模 φ=2M4 ln(r/r_*) 确为正则场（独立推出）',
        '(a) 6D 曲率分解 R6=R[ĝ]-4∇²β-6(∂β)²+2e^{-2β} 数值校验：6 个采样点最大相对偏差 %s'
        '（例：数值 %s vs 闭式 %s）；(b) 由该分解得 Jordan 动能 +4πM6^4(∂r)²，'
        '经 Weyl 重标定（Ω²=4πr²M6^4/M4²）后 Einstein 框动能 = -3M4²(∂ln r)² + M4²(∂ln r)² '
        '= -2M4²(∂ln r)² = -½(∂φ)²，φ=2M4 ln r ⇒ 系数精确相等（Fraction 精确、符号健康）'
        % (fs(D(str(worst)), 8), fs(D(str(sample[0])), 10), fs(D(str(sample[1])), 10)),
        {'worst_rel': fs(D(str(worst)), 8), 'coef_total': str(total), 'coef_canon': str(canon)})
    return ok_alg

# ---- A12 体积模质量
def _A12():
    N = 3.0; g6sq = 0.81; M6 = 1.7
    rs2 = N ** 2 / (4 * g6sq * M6 ** 4)
    rs = math.sqrt(rs2)
    M4sq = 4 * math.pi * rs2 * M6 ** 4
    M4 = math.sqrt(M4sq)
    def V_of_phi(phi):
        r = rs * math.exp(phi / (2 * M4))
        x = r / rs
        return 2 * math.pi * M6 ** 4 * x ** (-4) * (x - 1.0 / x) ** 2
    h = 1e-4 * M4
    d2 = (V_of_phi(h) - 2 * V_of_phi(0.0) + V_of_phi(-h)) / (h * h)
    tgt = 1.0 / rs2
    rel = abs(d2 - tgt) / tgt
    ok = rel < 1e-6
    add('A12', 'PASS' if ok else 'FAIL', 'm_φ^2 = d²V_E/dφ²|_{r_*} = 1/r_*^2',
        '有限差分（步长 1e-4·M4）得 %s，闭式 1/r_*^2=%s，相对残差 %s'
        % (fs(D(str(d2)), 12), fs(D(str(tgt)), 12), fs(D(str(rel)), 8)),
        {'m_phi2_num': fs(D(str(d2)), 12), 'rel': fs(D(str(rel)), 8)})
    return ok

# ---- A13 四维规范耦合
def _A13():
    N = D(3); g6sq = D('0.81'); M6 = D('1.7')
    rs = (rstar_sq(N, g6sq, M6)).sqrt()
    inv_g4sq = 4 * PI * rs ** 2 / g6sq
    a1 = g6sq / (16 * PI ** 2 * rs ** 2)          # 由 1/g4^2 反推
    a2 = D(1) / (4 * PI * inv_g4sq)               # α = g4^2/(4π)
    rel = abs(a1 - a2) / a2
    ok = rel < D('1e-50')
    add('A13', 'PASS' if ok else 'FAIL', '1/g_4^2 = 4πr_*^2/g_6^2 与 α_4 = g_6^2/(16π^2 r_*^2)',
        '两路相对残差 %s。补记：4D Maxwell 项 √(-g)g^{-1}g^{-1}F² 在 Weyl 变换下不变'
        '（√-g→Ω⁴√-g、两个逆度规→Ω^{-4}），故 1/g_4² 不额外带 Ω 因子。'
        % (Ds(rel)), {'rel': Ds(rel), 'inv_g4sq': Ds(inv_g4sq)})
    return ok

# ---- A14 α 与拓扑整数
def _A14():
    N = D(3); g6sq = D('0.81'); M6 = D('1.7')
    rs = (rstar_sq(N, g6sq, M6)).sqrt()
    xi = g6sq * M6 ** 2
    a_direct = g6sq / (16 * PI ** 2 * rs ** 2)
    a_closed = (xi / (2 * PI * N)) ** 2
    rel = abs(a_direct - a_closed) / a_closed
    ok = rel < D('1e-50')
    add('A14', 'PASS' if ok else 'FAIL', 'α_4 = (ξ/(2πN))^2，ξ = g_6^2 M_6^2（消去半径）',
        '代入 r_*²=N²/(4g6²M6⁴) 后两式相对残差 %s（ξ=%s，N=%s）'
        % (Ds(rel), Ds(xi), str(N)), {'rel': Ds(rel), 'xi': Ds(xi)})
    return ok

# ---- A15 量纲总表
def _A15():
    rows = [
        ('[S_6 引力项]=0',
         dmul(dpow(DIM_M6, 4), dmul(DIM_R6, (Fraction(0), Fraction(6), Fraction(0)))), 0),
        ('[g_6]=-1', DIM_G6, -1),
        ('[r_*]=-1', DIM_RAD, -1),
        ('[ξ]=0', dmul(dpow(DIM_G6, 2), dpow(DIM_M6, 2)), 0),
        ('[Λ_6]=2', dpow(DIM_LAM6, 1), 2),
        ('[V_E]=4', DIM_V4, 4),
        ('[α_4]=0', ddiv(dpow(DIM_G6, 2), dpow(DIM_RAD, 2)), 0),
        ('[1/r_*^2]=2', dpow(DIM_RAD, -2), 2),
        ('[M_4^2]=2', dmul(dpow(DIM_RAD, 2), dpow(DIM_M6, 4)), 2),
    ]
    bad = [nm for nm, d, want in rows if massdim(d) != want]
    ok = not bad
    add('A15', 'PASS' if ok else 'FAIL', '量纲齐次性总表 9/9',
        '来料全部 9 条量纲关系在本册 (M,L,T) 三元组下逐条齐次：%s。'
        '★本库「量纲非齐次」缺陷族已复发 8 次以上，V15 是本轮少数全过者，如实记为正分。'
        % '、'.join(nm for nm, d, w in rows), {'bad': bad, 'n': len(rows)})
    return ok

# ================================================================ B 段 · 来料数值表独立复算
def _m4_rstar(N):
    """本册新增闭式：M4·r_* = N/(4√(πα))（约化普朗克单位）"""
    return D(N) / (4 * (PI * ALPHA).sqrt())

def _B():
    N = D(3)
    ok_all = True
    # B01 xi
    xi = 2 * PI * N * ALPHA.sqrt()
    rel_xi = abs(xi - D('1.610215')) / D('1.610215')
    ok1 = rel_xi < D('1e-6')
    add('B01', 'PASS' if ok1 else 'FAIL', 'ξ = 2πN√α 复算（来料 1.610215）',
        '本册 %s，来料 1.610215，相对差 %s' % (Ds(xi), Ds(rel_xi)),
        {'xi': Ds(xi), 'rel': Ds(rel_xi)})
    # B02 M6 r_*
    m4r = _m4_rstar(N)
    m6r2 = m4r / (2 * PI.sqrt())
    m6r = m6r2.sqrt()
    rel_m6 = abs(m6r - D('1.18209')) / D('1.18209')
    ok2 = rel_m6 < D('1e-4')
    add('B02', 'PASS' if ok2 else 'FAIL', 'M_6 r_* 复算（来料 1.18209）',
        '由 M4²=4πr_*²M6⁴ 与 r_*²=N²/(4g6²M6⁴) 得 (M6 r_*)² = M4 r_*/(2√π)；'
        '本册 %s，来料 1.18209，相对差 %s' % (Ds(m6r), Ds(rel_m6)),
        {'M6r': Ds(m6r), 'rel': Ds(rel_m6)})
    # B03 r_*/l_P（非约化）
    ratio = (8 * PI).sqrt() * m4r
    rel_r = abs(ratio - D('24.83268')) / D('24.83268')
    # 由来料自己的 M6r_*=1.18209 反推应为多少
    ratio_from_m6 = (8 * PI).sqrt() * 2 * PI.sqrt() * (D('1.18209') ** 2)
    spread = abs(ratio - ratio_from_m6) / ratio
    ok3 = rel_r < D('1e-6')
    add('B03', 'PASS' if ok3 else 'FAIL', 'r_*/ℓ_P（非约化）复算：来料 24.83268 与闭式逐位一致',
        '本册 %s；来料 24.83268，相对差 %s；由来料 6 位舍入的 M6 r_*=1.18209 反推 %s，'
        '与本册差 %s（纯舍入，非不自洽）。'
        '★自抓登记（本册开发期真实错误）：首版手算把 √(8π) 误取 5.0146（真值 %s），'
        '据此一度误判「来料表内三个数两两不自洽 2.6e-4」；机器复算否证该误判 —— '
        '来料四个数值（1.610215 / 1.18209 / 24.83268 / 4.9165e17）全部自洽且与本册闭式逐位相符。'
        '本条按「手算读数必须机器兜底」纪律留档。'
        % (Ds(ratio), Ds(rel_r), Ds(ratio_from_m6), Ds(spread), Ds((8 * PI).sqrt())),
        {'ratio': Ds(ratio), 'rel_vs_claim': Ds(rel_r), 'spread': Ds(spread),
         'sqrt8pi': Ds((8 * PI).sqrt())})
    # B04 KK 能标
    kk = M_P_RED / m4r
    rel_kk = abs(kk - D('4.9165e17')) / D('4.9165e17')
    ok4 = rel_kk < D('1e-3')
    add('B04', 'PASS' if ok4 else 'FAIL', 'KK 特征能标 1/r_* 复算（来料 4.9165×10^17 GeV）',
        '本册 %s GeV，来料 4.9165e17 GeV，相对差 %s' % (Ds(kk), Ds(rel_kk)),
        {'KK_GeV': Ds(kk), 'rel': Ds(rel_kk)})
    # B05 本册新增闭式
    rel_c = abs(m4r - D(N) / (4 * (PI * ALPHA).sqrt())) / m4r
    ok5 = rel_c < D('1e-50')
    add('B05', 'PASS' if ok5 else 'FAIL', '★本册新增闭式 M4·r_* = N/(4√(πα))（来料未给）',
        '给定 α 观测值后，紧致半径与 KK 能标只由整数 N 决定：M4 r_* = %s（N=3），'
        '残差 %s。⇒ r_* 与 1/r_* 随 N 线性变化，N 不被任何观测量锁定（见 C01/C05）。'
        % (Ds(m4r), Ds(rel_c)), {'M4r': Ds(m4r), 'formula': 'M4*r_* = N/(4*sqrt(pi*alpha))'})
    ok_all = ok1 and ok2 and ok4 and ok5
    return ok_all

# ================================================================ C 段 · 本册新层
def _C01():
    """α 的可达域：任何目标 α 都能被 (N, ξ) 实现 ⇒ 零判别力"""
    grid = [D(10) ** D(-k) for k in range(8, -1, -1)] + [ALPHA, D('0.5'), D('1')]
    hit = 0
    for a in grid:
        N = D(1)
        xi = 2 * PI * N * a.sqrt()          # 任意 N 都有解
        back = (xi / (2 * PI * N)) ** 2
        if abs(back - a) / a < D('1e-50'):
            hit += 1
    # 「自然」盒：ξ∈[0.1,10]、N∈[1,20] 时可达 α 区间
    a_lo = (D('0.1') / (2 * PI * D(20))) ** 2
    a_hi = (D(10) / (2 * PI * D(1))) ** 2
    inside = (a_lo <= ALPHA <= a_hi)
    ok = hit == len(grid)
    add('C01', 'FAIL' if ok else 'FAIL',
        'α_4=(ξ/2πN)² 对 α 零判别力：可达域 = (0,∞)，覆盖一切测量值',
        '机器扫描 %d 个目标 α（1e-8…1）全部可达（命中 %d/%d，残差 <1e-50）；'
        '即便加「自然性」先验 ξ∈[0.1,10]、N∈[1,20]，可达区间 [%s, %s] 仍跨 %s 个量级'
        '且包含 α_obs=%s ⇒ 该关系不是预言而是反解（把 α 写两遍），与 r287「势的双口径恒等」同型。'
        % (len(grid), hit, len(grid), Ds(a_lo), Ds(a_hi),
           Ds((a_hi / a_lo).log10()), Ds(ALPHA)),
        {'hit': hit, 'n': len(grid), 'a_lo': Ds(a_lo), 'a_hi': Ds(a_hi),
         'decades': Ds((a_hi / a_lo).log10())})
    return ok

def _N_table(N):
    m4r = _m4_rstar(D(N))
    m6r2 = m4r / (2 * PI.sqrt())
    m6r = m6r2.sqrt()
    epsR = D(2) / m6r2                     # R_6/M_6^2 = 2/(M_6 r_*)^2
    epsF = (D(N) ** 2) / (2 * m6r2 ** 2)   # F^2/M_6^4
    kk = M_P_RED / m4r
    ratio = (8 * PI).sqrt() * m4r
    return {'N': int(N), 'M4r': Ds(m4r), 'M6r': Ds(m6r), 'eps_R': Ds(epsR),
            'eps_F': Ds(epsF), 'KK_GeV': Ds(kk), 'r_over_lP': Ds(ratio)}

def _C02():
    rows = [_N_table(n) for n in (1, 2, 3, 4, 5, 6, 10, 20, 43, 48)]
    # 截断门槛：eps_R <= 0.1
    n_min = None
    for n in range(1, 400):
        if _N_table(n) and D(_N_table(n)['eps_R']) <= D('0.1'):
            n_min = n
            break
    # r294 除性定理要求 6 | N；与截断门槛的最小交集
    n_div = None
    for n in range(1, 400):
        if n % 6 == 0 and D(_N_table(n)['eps_R']) <= D('0.1'):
            n_div = n
            break
    # LEP：N_ν = 2.9840 ± 0.0082
    sig = lambda n: (D(n) - D('2.9840')) / D('0.0082')
    r3 = _N_table(3)
    ok = True
    add('C02', 'FAIL',
        '★N-两难定理：手征动机（N=3）与经典截断有效性（N≥%s）在给定 α_obs 下互斥'
        % (n_min,),
        '给定 α_obs 后 M4·r_* = N/(4√(πα)) ⇒ r_*∝N、KK∝1/N，N 是唯一剩余自由度。'
        '① N=3（来料「三代」动机）：M6 r_*=%s ⇒ 曲率展开参数 R6/M6²=%s、F²/M6⁴=%s，'
        '均为 O(1) ⇒ 高阶导数/量子修正不被压低，经典截断失效（来料已自注，本册量化）。'
        '★更强读数：F²/M6⁴ = N²/(2(M6 r_*)⁴) 而 (M6 r_*)² = M4 r_*/(2√π) ∝ N ⇒ '
        'F²/M6⁴ ≡ 2.3047 与 N 无关 ⇒ 增大 N 只能压低曲率展开参数，压不低规范扇区展开参数。'
        '② 要求 R6/M6² ≤ 0.1（勉强可称经典）需 N ≥ %s；再叠加 r294 除性定理（6|N）⇒ 最小可行 N=%s'
        ' ⇒ 手征零模 %s 个，与 LEP N_ν=2.9840±0.0082 相差 %sσ。'
        '③ 三条件（三代谱=N=3 / 截断有效 N≥%s / LEP N_ν≈3）无交集 ⇒ 该退路不是「待补」而是互斥。'
        % (r3['M6r'], r3['eps_R'], r3['eps_F'], n_min, n_div, n_div,
           Ds(sig(n_div)), n_min),
        {'N_min_truncation': n_min, 'N_min_with_divisibility': n_div,
         'sigma_LEP': Ds(sig(n_div)), 'table': rows})
    return ok

def _C03():
    N = D(3)
    m4r = _m4_rstar(N)
    # V_min/M6^4 = 4π(λ-1/2) + O(δ²)（包络定理：∂V/∂λ|_{x=1} = 4π x^{-2} = 4π）
    # V_min[GeV^4] = (λ-1/2) * M_P_red^4 / (M4 r_*)^2
    eps_needed = 2 * RHO_LAMBDA * m4r ** 2 / (M_P_RED ** 4)   # = δΛ6/Λ6
    # 量子修正保守下界：δΛ6 ~ M6^2/(64π^3)；Λ6* = 2ξM6^2/N^2 ⇒ 相对量
    xi = 2 * PI * N * ALPHA.sqrt()
    lam6_over_M6sq = 2 * xi / (N ** 2)
    loop = D(1) / (64 * PI ** 3)
    rel_quantum = loop / lam6_over_M6sq
    mismatch = rel_quantum / eps_needed
    ok = True
    add('C03', 'FAIL', '★Λ_6 微调定价：需 δΛ_6/Λ_6 ≲ %s，而量子修正 ≳ %s（差 %s 倍）'
        % (Ds(eps_needed), Ds(rel_quantum), Ds(mismatch)),
        'V15 的 Λ_4=0 不是被导出的，而是把 Λ_6 调到 2g6²M6⁴/N²（即 λ≡Λ_6 r_*²=1/2）的结果。'
        '包络定理给 ∂V_min/∂λ = 4πM6⁴·x_min^{-2} ⇒ V_min/M6⁴ = 4π(λ-1/2)。'
        '要把 V_min 压到观测 ρ_Λ=%s GeV⁴，需 λ-1/2 = %s，即 δΛ_6/Λ_6 = %s；'
        '而 Λ_6* = 2ξM6²/N² = %s·M6²，6D 圈修正保守下界 M6²/(64π³) ⇒ 相对修正 ≳ %s。'
        '⇒ 真空能灾难在 V15 内的表现形式（与 r292 P9 的 10^124 同构异源：r292 比的是 E(A*) vs ρ_Λ，'
        '本册比的是 Λ_6 微调需求 vs 量子修正，二者不得相加）。'
        % (Ds(RHO_LAMBDA), Ds(eps_needed / 2), Ds(eps_needed),
           Ds(lam6_over_M6sq), Ds(rel_quantum)),
        {'eps_Lambda6_needed': Ds(eps_needed), 'rel_quantum': Ds(rel_quantum),
         'mismatch': Ds(mismatch), 'Lambda6_over_M6sq': Ds(lam6_over_M6sq)})
    return ok

def _C04():
    N = D(3); g6sq = D('0.81'); M6 = D('1.7')
    rs = (rstar_sq(N, g6sq, M6)).sqrt(); L6 = lam6_sol(N, g6sq, M6)
    M4sq = 4 * PI * rs ** 2 * M6 ** 4
    M4_4 = M4sq ** 2                       # V_E 质量维 4，归一化必须用 M4^4（首版误用 M4^2 已修）
    v_bar = V_E_closed(rs * (D(3)).sqrt(), rs, M6)
    v_bar_over_M4 = v_bar / M4_4
    v_inf = V_E_closed(rs * D('1000'), rs, M6) / M4_4
    v_small = V_E_closed(rs * D('0.3'), rs, M6) / M4_4
    # 物理口径（N=3 + α_obs）：M6^4/M4^4 = 1/(4π (M4 r_*)^2)
    m4r = _m4_rstar(D(3))
    ratio_M6M4 = D(1) / (4 * PI * m4r ** 2)
    bar_phys = (8 * PI / D(27)) * ratio_M6M4
    inf_phys = 2 * PI * D('1e-6') * ratio_M6M4
    # 无 Weyl 因子对照（见 CTL3）
    ok = True
    add('C04', 'BOUNDARY',
        '稳定性是局部且退化的：V_E(r_*)=0 与 V_E(∞)=0 能量简并，势垒有限',
        'V_E≥0 且在 x=1 取 0；但 x→∞ 时 V_E→0（本册 x=1000 处 V/M4⁴=%s），'
        'x→0 时 V→∞（x=0.3 处 %s）⇒ r_* 是局部极小而非能量选出的真空，'
        '去紧致化方向与之简并（势垒高度 V(√3)/M4⁴=%s 有限）⇒ 亚稳，不是绝对稳定。'
        '诚实边界：这不否证来料的「局部动力学稳定性」（其措辞准确），'
        '但「稳定化」不能读作「半径被能量选出」——选出的条件是场方程（A06），不是势的全局结构。'
        % (Ds(inf_phys), Ds(v_small), Ds(bar_phys)),
        {'V_inf_over_M4^4': Ds(inf_phys), 'barrier_over_M4^4': Ds(bar_phys),
         'M6^4_over_M4^4': Ds(ratio_M6M4)})
    return ok

def _C05():
    rows = [_N_table(n) for n in range(1, 11)]
    add('C05', 'FAIL', '参数计数 dof=1：给定 α_obs 后 N 仍自由，r_* 与 KK 能标不被唯一确定',
        '输入 {g6, M6, N} + 须微调的 Λ_6 = 4 个（含 1 个整数）；'
        '输出 {r_*, M4, α, m_φ}。观测约束：M4（定单位，不计）、α（1 条，只锁 ξ/N）⇒ dof=1。'
        '⇒ r_*、KK 能标、M6 全部随 N 漂移（N=1…10 表：M4 r_* 从 %s 到 %s，'
        'KK 从 %s 到 %s GeV）⇒ 模型对紧致尺度零预言。'
        % (rows[0]['M4r'], rows[9]['M4r'], rows[9]['KK_GeV'], rows[0]['KK_GeV']),
        {'table': rows})
    return True

def _C06():
    # 3 个同电荷（q=1）左手零模的裸 U(1) 反常
    A3 = sum(D(q) ** 3 for q in (1, 1, 1))
    Agrav = sum(D(q) for q in (1, 1, 1))
    # SM 一整代四反常（Fraction 精确）。★口径：全部化为左手 Weyl 场 ——
    # 右手场须取其电荷共轭（u_R^c 的 Y=-2/3 而非 u_R 的 +2/3），否则 ΣY^3 不抵消
    # （本册首版即在此处写错，得 -4/9，机器对照后修正；引 r292 C3 / r294 P7 的 0 作锚）
    F = Fraction
    fields = [('Q_L', F(1, 6), 3, 2), ('u_R^c', F(-2, 3), 3, 1), ('d_R^c', F(1, 3), 3, 1),
              ('L_L', F(-1, 2), 1, 2), ('e_R^c', F(1, 1), 1, 1)]
    sm = sum(F(Y) ** 3 * dc * dw for _, Y, dc, dw in fields)
    sm_grav = sum(F(Y) * dc * dw for _, Y, dc, dw in fields)
    sm_su3 = sum(F(Y) * dc for _, Y, dc, dw in fields if dc == 3)
    sm_su2 = sum(F(Y) * dw for _, Y, dc, dw in fields if dw == 2)
    ok = (A3 != 0 and sm == 0 and sm_grav == 0 and sm_su3 == 0 and sm_su2 == 0)
    add('C06', 'FAIL',
        ('反常：N=3 个同电荷左手零模 ⇒ [U(1)]^3=' + Ds(A3) + '、grav^2U(1)=' + Ds(Agrav)
         + '，且作用量内无抵消机制'),
        'V15 的作用量只含 Einstein–Maxwell（无 2-形式、无 Green–Schwarz/Chern–Simons 项），'
        '故经典场内容层面没有 anomaly-inflow 的载体；SM 一整代四个反常系数'
        '（[Y]^3=' + str(sm) + '、grav²Y=' + str(sm_grav) + '、[SU(3)]²Y=' + str(sm_su3)
        + '、[SU(2)]²Y=' + str(sm_su2) + '，Fraction 精确、全为 0）'
        '⇒ 「裸 U(1) 零模」与「SM 手征谱」不是同一种对象（本册反常判据以此为牙齿）。'
        '★继承登记：与 r292 P6 同源（本册不重复计数）；r294 P7 已修正该判据的适用范围'
        '（它排除不完整谱，不排除 6 代整代重复）。诚实边界：若在框架外补入 B 场/CS 项，'
        'inflow 可抵消——那是「加场内容」，不是 V15 已有结构。',
        {'A3': str(A3), 'Agrav': str(Agrav), 'SM_Y3': str(sm),
         'SM_grav2Y': str(sm_grav), 'SM_SU3_2Y': str(sm_su3), 'SM_SU2_2Y': str(sm_su2)})
    return ok

def _C07():
    add('C07', 'FAIL',
        '三代识别：V15 的 3 个零模是「同电荷、同表示」的 3 份拷贝，不是 SM 三代（继承 r294/LEP）',
        'V15 自注「三个手征零模并不自动构成完整的标准模型三代粒子」——本册确认为真：'
        'ind(D̸)=N 只给净手征数，3 个零模电荷与表示完全相同，而 SM 一代需 6 种表示'
        '（Q_L,u_R,d_R,L_L,e_R,ν_R）各 3 份。★继承登记（本册不重算、不重复计数）：'
        'r294 除性定理 index_R=q_R·dim(R)·M ⇒ dim(R)|N_gen，SM 一代维数集 lcm=6 ⇒ N_gen=3 不可行，'
        '最小可行 6 代被 LEP N_ν=2.9840±0.0082 以 367.8σ 排除；本册 C02 又给出独立第三条'
        '（截断要求 N≥43，与 N_ν≈3 互斥）。'
        '★来料自评「电荷/规范表示/质量/反常仍需逐项检查」与机器结论一致 ⇒ 判为诚实（见 C08）。',
        {'inherited_from': ['r294-P2-divisibility', 'r294-P3-LEP', 'r292-P6-anomaly']})
    return True

def _C08():
    add('C08', 'PASS', '来料自我诚实边界与机器裁定一致（判据能给出肯定项）',
        '来料三处自评——(i)「ξ 仍是自由参数，还不能无参数确定 α」⇒ 与本册 C01/C05 完全一致；'
        '(ii)「M6 r_*≈1.18 不存在明显低曲率尺度分离，经典近似可能受很大高阶修正」'
        '⇒ 本册量化为 R6/M6²=%s、F²/M6⁴=%s（O(1)）；'
        '(iii)「三个零模不自动构成三代、反常仍需检查」⇒ 本册 C06/C07 确认为真。'
        '⇒ 来料未越界宣称「攻破 α 本源」，其自我边界准确；本册给予正分（判据非一律否定）。'
        % (_N_table(3)['eps_R'], _N_table(3)['eps_F']), {})
    return True

# ================================================================ D 段 · 控制组
def _D():
    oks = []
    # CTL1 平直 T^2 替代模型反例（来料表内自列，本册重算）
    N = D(3); g6sq = D('0.81'); M6 = D('1.7'); r = D('2.3')
    lam_in = T_in_coef(N, g6sq, r) / M6 ** 4      # 内部方程要求 Λ6 = 此值
    lam_out = T_out_coef(N, g6sq, r) / M6 ** 4    # 外部方程要求 Λ6 = 此值
    ok1 = (lam_in > 0) and (lam_out < 0)
    oks.append(ok1)
    add('CTL1', 'PASS' if ok1 else 'FAIL', '控制组：平直 T² 磁通无 Minkowski 真空（内/外方程符号互斥）',
        '内部 Ricci=0、R6=0 ⇒ 内部方程要求 Λ6=%s>0，外部方程要求 Λ6=%s<0 ⇒ N≠0 时无解'
        '（来料表内「平直二维环面替代模型反例」重算通过）' % (Ds(lam_in), Ds(lam_out)),
        {'Lambda_in': Ds(lam_in), 'Lambda_out': Ds(lam_out)})
    # CTL2 错误 F^2 系数（漏 1/2）
    rs2_true = rstar_sq(N, g6sq, M6)
    rs2_wrong = (D(N) ** 2) / (2 * g6sq * M6 ** 4)
    a_true = g6sq / (16 * PI ** 2 * rs2_true)
    a_wrong = g6sq / (16 * PI ** 2 * rs2_wrong)
    ok2 = abs(a_true / a_wrong - D(2)) < D('1e-50')
    oks.append(ok2)
    add('CTL2', 'PASS' if ok2 else 'FAIL', '控制组：F² 系数漏 1/2 ⇒ α 偏离 2 倍（判据有牙齿）',
        '若 F²=N²/r⁴（正确为 N²/2r⁴），则 r_*² 变 2 倍、α 变 %s 倍 ⇒ 与 α_obs 差 100%%，'
        '说明 α 读数对内部几何系数敏感，非恒真。' % Ds(a_true / a_wrong),
        {'ratio': Ds(a_true / a_wrong)})
    # CTL3 去掉 Weyl 因子：势垒消失、渐近行为反转
    rs = rs2_true.sqrt(); L6 = lam6_sol(N, g6sq, M6)
    def B_of(r):
        return 4 * PI * (-M6 ** 4 + M6 ** 4 * L6 * r ** 2 + (D(N) ** 2) / (8 * g6sq * r ** 2))
    # V_E 在 (r_*,10r_*) 上有极大（√3）；B 在同一区间单调增
    vmax = max(V_E_closed(rs * (D(1) + D(i) * D('0.01')), rs, M6) for i in range(1, 900))
    b_end = B_of(rs * D(10))
    b_mid = B_of(rs * D(2))
    monotone = b_end > b_mid > B_of(rs)
    ok3 = monotone and (vmax > 0)
    oks.append(ok3)
    add('CTL3', 'PASS' if ok3 else 'FAIL',
        '控制组：Weyl 因子 (r_*/r)^4 正是「√3 势垒」与「∞ 简并」的来源',
        '去掉 Weyl 因子后 B(r) 在 r>r_* 单调上升（B(2r_*)<B(10r_*)，无极大），'
        'V_E(∞)→0 而 B(∞)→∞ ⇒ 「有限势垒 + 去紧致化简并」是 Weyl 重标定的后果，'
        '不是磁通稳定化本身的性质。判据（势垒位置 √3）有牙齿：CTL3 可分辨两者。'
        , {'B_2r': Ds(b_mid), 'B_10r': Ds(b_end)})
    # CTL4 正对照：Λ6 取解值时极小值精确为 0；偏离则 >0 且极小点漂移
    def vmin_of(lam):
        xs = (D(2) - (D(4) - 6 * lam).sqrt()) / (2 * lam)
        x = xs.sqrt()
        return 4 * PI * x ** (-4) * (-D(1) + lam * x ** 2 + D(1) / (2 * x ** 2))
    v0 = vmin_of(D('0.5'))
    v1 = vmin_of(D('0.55'))
    ok4 = abs(v0) < D('1e-50') and v1 > 0
    oks.append(ok4)
    add('CTL4', 'PASS' if ok4 else 'FAIL', '控制组（正对照）：λ=1/2 时 V_min 精确为 0，λ=0.55 时为正',
        'λ≡Λ6 r_*²=1/2 ⇒ V_min=%s（机器零）；λ=0.55 ⇒ V_min/M6⁴=%s>0 且极小点漂移'
        ' ⇒ 势的极小值判据能给出肯定结论，非恒假。' % (Ds(v0), Ds(v1)),
        {'V_min_half': Ds(v0), 'V_min_055': Ds(v1)})
    # CTL5 错误内部 Ricci（R_ij=(2/r^2)G_ij）
    lam6_true = lam6_sol(N, g6sq, M6)
    lhs_wrong = M6 ** 4 * (D(2) / rs ** 2 - D(1) / rs ** 2 + lam6_true)
    rhs = T_in_coef(N, g6sq, rs)
    rel = abs(lhs_wrong - rhs) / abs(rhs)
    ok5 = rel > D('1e-3')
    oks.append(ok5)
    add('CTL5', 'PASS' if ok5 else 'FAIL',
        '控制组：内部 Ricci 写成 (2/r²)G_ij（正确 1/r²）⇒ 内部方程残差 %s' % Ds(rel),
        'd=2 球面 Ricci_ij=(d-1)/r²·G_ij=1/r²·G_ij；取 2/r² 则解点残差 %s（>1e-3）'
        ' ⇒ 内/外部方程判据对曲率系数敏感。' % Ds(rel), {'rel': Ds(rel)})
    # CTL6 Ricci 数值器负对照（平直 T² ⇒ R6=0）
    geom_t = make_geom(2.3, 0.0, 1.0, torus=True)
    Rs_t, _, _ = ricci_scalar(geom_t, 0.7, 1.1)
    ok6 = abs(Rs_t) < 1e-8
    oks.append(ok6)
    add('CTL6', 'PASS' if ok6 else 'FAIL', '控制组（负对照）：内部取平直 T² 时数值 R6=0',
        '同一数值器对平直内部空间给 R6=%s（<1e-8）⇒ A05b 的 R6=2/r² 不是数值器恒输出。'
        % fs(D(str(Rs_t)), 8), {'R6_torus': fs(D(str(Rs_t)), 8)})
    return all(oks)

# ================================================================ 主流程
NAME = ('TUFT-r298_ROOTV15六维EinsteinMaxwell磁通稳定化与alpha关系审计_'
        '独立重推与N两难定理与Lambda6微调_精算与可视化_2026-11-01')

def main():
    sections = [
        ('A01', _A01), ('A02', _A02), ('A03', _A03), ('A04/A05', _A04_A05), ('A05b', _A05b),
        ('A06', _A06), ('A07', _A07), ('A08', _A08), ('A09', _A09), ('A10', _A10),
        ('A11', _A11), ('A12', _A12), ('A13', _A13), ('A14', _A14), ('A15', _A15),
        ('B', _B), ('C01', _C01), ('C02', _C02), ('C03', _C03), ('C04', _C04),
        ('C05', _C05), ('C06', _C06), ('C07', _C07), ('C08', _C08), ('D', _D),
    ]
    failed = []
    for tag, fn in sections:
        try:
            fn()
        except Exception as exc:
            failed.append('%s: %s: %s' % (tag, type(exc).__name__, exc))
            add(tag + '-ERR', 'FAIL', '段落执行异常', '%s: %s' % (type(exc).__name__, exc))

    codes = [e['code'] for e in ENTRIES]
    guard('G9-1 条目编号唯一', len(codes) == len(set(codes)), 'n=%d uniq=%d' % (len(codes), len(set(codes))))
    guard('G9-2 段落无异常', not failed, 'failed=%s' % failed)
    guard('G9-3 量纲工具自检', _G_DIM_OK, 'G0-1..G0-6')

    counts = {}
    for e in ENTRIES:
        counts[e['verdict']] = counts.get(e['verdict'], 0) + 1
    n_guard = sum(1 for g in GUARDS if g['ok'])
    n_guard_all = len(GUARDS)

    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUT_DIR = os.path.join(BASE, '数据')
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)

    payload = {
        'round': 'r298',
        'title': 'ROOT V15.0 六维 Einstein–Maxwell 磁通稳定化与 α 关系审计',
        'date': '2026-11-01',
        'verdict_summary': counts,
        'entries': ENTRIES,
        'guards': GUARDS,
        'guard_pass': n_guard,
        'guard_total': n_guard_all,
        'constants': {
            'alpha_inv': str(ALPHA_INV), 'alpha': Ds(ALPHA),
            'M_Pl_GeV': Ds(M_PL_C2), 'M_P_reduced_GeV': Ds(M_P_RED),
            'l_Planck_m': str(L_PLANCK), 'rho_Lambda_GeV4': str(RHO_LAMBDA),
        },
        'closed_forms': {
            'r_star_sq': 'r_*^2 = N^2/(4 g_6^2 M_6^4)',
            'Lambda_6': 'Lambda_6 = 2 g_6^2 M_6^4 / N^2',
            'M4_r_star': 'M4*r_* = N/(4 sqrt(pi*alpha))  [本册新增]',
            'M6_r_star_sq': '(M_6 r_*)^2 = M_4 r_*/(2 sqrt(pi))  [本册新增]',
            'alpha': 'alpha_4 = (xi/(2 pi N))^2,  xi = g_6^2 M_6^2',
            'm_phi_sq': 'm_phi^2 = 1/r_*^2,  phi = 2 M_4 ln(r/r_*)',
        },
        'relations': {
            'r292': '同主题前册（ROOT V14 六维磁通手征与几何稳定化）',
            'r294': '磁通手征谱三代不可实现定理（本册 C02/C07 继承其二条判据，不重复计数）',
            'r290': 'V12 高维几何审计（其「半径模不是被方程选出的解」在 V15 的 S² 磁通下被修掉）',
        },
    }

    with io.open(os.path.join(OUT_DIR, NAME + '.json'), 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2))

    lines = []
    lines.append('# TUFT-r298 · ROOT V15.0 六维 Einstein–Maxwell 磁通稳定化与 α 关系审计（数据产物）')
    lines.append('')
    lines.append('- 日期：2026-11-01　条目：%d　守卫：%d/%d' % (len(ENTRIES), n_guard, n_guard_all))
    lines.append('- 判词：**REPRODUCE-TRUE / PREDICT-NULL**（数学复现成立，α 预测为零）')
    lines.append('')
    for e in ENTRIES:
        lines.append('## %s · %s · %s' % (e['code'], e['verdict'], e['title']))
        lines.append('')
        lines.append(e['detail'])
        if e['key']:
            lines.append('')
            lines.append('- 关键读数：' + '；'.join('%s=%s' % (k, v) for k, v in e['key'].items()
                                                if not isinstance(v, (list, dict))))
        lines.append('')
    lines.append('## 守卫')
    lines.append('')
    for g in GUARDS:
        lines.append('- %s：%s —— %s' % (g['name'], 'PASS' if g['ok'] else 'FAIL', g['detail']))
    with io.open(os.path.join(OUT_DIR, NAME + '.md'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))

    rep = []
    rep.append('TUFT-r298 ROOT V15.0 audit report  2026-11-01')
    rep.append('verdicts: ' + ', '.join('%s=%d' % (k, v) for k, v in sorted(counts.items())))
    rep.append('guards: %d/%d' % (n_guard, n_guard_all))
    rep.append('')
    for e in ENTRIES:
        rep.append('[%s] %s :: %s' % (e['verdict'], e['code'], e['title']))
        rep.append('    ' + e['detail'].replace('\n', ' '))
    with io.open(os.path.join(OUT_DIR, NAME + '_report.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(rep))

    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    print('r298 rc=0 entries=%d guards=%d/%d' % (len(ENTRIES), n_guard, n_guard_all))
    print('verdicts: ' + ' '.join('%s=%d' % (k, v) for k, v in sorted(counts.items())))
    print('main: alpha=%.12e  M4r*(N=3)=%s  M6r*(N=3)=%s' %
          (float(ALPHA), Ds(_m4_rstar(D(3)))[:12], Ds((_m4_rstar(D(3)) / (2 * PI.sqrt())).sqrt())[:12]))
    print('C02: eps_R(N=3)=%s  N_min(trunc)=search-in-json' % Ds(D(_N_table(3)['eps_R']))[:12])
    return 0 if (n_guard == n_guard_all and not failed) else 1

if __name__ == '__main__':
    sys.exit(main())
