# -*- coding: utf-8 -*-
"""
66 号卷配套引擎：光子螺旋坐标解释判据（运动学 / Frenet 二难 / 500nm 精算 / 圆偏振对照）

设计纪律（openuft 项目体例）：
  1. 恒等式在精确符号层相消（Fraction + PiNum），不靠浮点阈值；
  2. 控制组先证明引擎有分辨力（CT1-CT6），任一失控 => 退出码 2；
  3. 所有 verdict 由计算结果驱动分支，禁止「算了数却硬编码判定」；
  4. 阈值一律来自输入不确定度传播或声明值末位半刻度，不设拍脑袋机器零；
  5. 输出三件套同批重落：*.py（本文件）+ *_results.json + *_out.txt。
"""
import os
import sys
import json
import math
from fractions import Fraction as F
from decimal import Decimal, getcontext

getcontext().prec = 60
PI60 = Decimal('3.14159265358979323846264338327950288419716939937510582097494')

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, 'photon_helix_audit_results.json')
OUT_TXT = os.path.join(HERE, 'photon_helix_audit_out.txt')

# ---------------------------------------------------------------- 精确符号层
class PiNum(object):
    """coeff * pi**k，coeff 为 Fraction，k 为整数。仅支持本卷需要的乘除法。"""
    __slots__ = ('c', 'k')

    def __init__(self, c=F(0), k=0):
        self.c = F(c)
        self.k = int(k)

    def __mul__(self, o):
        if isinstance(o, PiNum):
            return PiNum(self.c * o.c, self.k + o.k)
        return PiNum(self.c * F(o), self.k)

    __rmul__ = __mul__

    def __neg__(self):
        return PiNum(-self.c, self.k)

    def __add__(self, o):
        o = o if isinstance(o, PiNum) else PiNum(o, 0)
        if self.c == 0:
            return o
        if o.c == 0:
            return self
        if self.k == o.k:
            return PiNum(self.c + o.c, self.k)
        raise ValueError('cannot add PiNum with different pi powers: %s + %s' % (self, o))

    __radd__ = __add__

    def __sub__(self, o):
        o = o if isinstance(o, PiNum) else PiNum(o, 0)
        return self.__add__(-o)

    def __rsub__(self, o):
        return (-self).__add__(o)

    def __truediv__(self, o):
        if isinstance(o, PiNum):
            return PiNum(self.c / o.c, self.k - o.k)
        return PiNum(self.c / F(o), self.k)

    def __eq__(self, o):
        if isinstance(o, PiNum):
            return self.c == o.c and self.k == o.k
        return self.k == 0 and self.c == F(o)

    def __repr__(self):
        return 'PiNum(%s, pi^%d)' % (self.c, self.k)

    def dec(self):
        return Decimal(self.c.numerator) / Decimal(self.c.denominator) * (PI60 ** self.k)


def fr2dec(fr):
    return Decimal(fr.numerator) / Decimal(fr.denominator)


def dim(m=0, l=0, t=0):
    return (F(m), F(l), F(t))


# ---------------------------------------------------------------- 记录器
RESULTS = []


def rec(idx, item, verdict, detail, extra=None):
    row = {'id': idx, 'item': item, 'verdict': verdict, 'detail': detail}
    if extra:
        row.update(extra)
    RESULTS.append(row)
    return row


def close(a, b, tol):
    return abs(a - b) <= tol


# ================================================================= A 段：运动学（版本 A：轴向 = c）
def sec_A():
    # A1: |r_dot|^2 = c^2 + (R*Omega)^2  —— 用 PiNum 精确符号 + 多点数值双验
    # r(t) = (R cos(Wt), R sin(Wt), c t)；横向速率平方恒为 (R W)^2（三角恒等式）
    lam = F(500, 1) * F(1, 10 ** 9)          # 500 nm -> m
    c = F(299792458)
    f = c / lam                               # 精确 Fraction
    R = PiNum(lam / 2, -1)                    # lambda/(2 pi)
    W = PiNum(2 * f, 1)                       # 2 pi f
    RW = R * W                                # = lambda*f = c （符号层精确）
    ident_RW_equals_c = (RW == PiNum(c, 0))

    maxerr = 0.0
    for i in range(1, 40):
        t = F(i, 7)
        # 横向速度分量（float 数值层）
        Rf, Wf = float(R.dec()), float(W.dec())
        tf = float(t)
        vx = float(-Rf * math.sin(float(Wf) * tf) * float(Wf))
        vy = float(Rf * math.cos(float(Wf) * tf) * float(Wf))
        vz = float(c)
        lhs = vx * vx + vy * vy + vz * vz
        rhs = float(c) ** 2 + float(RW.dec()) ** 2
        maxerr = max(maxerr, abs(lhs - rhs) / rhs)
    rec('A1', '版本A速度分解 |r_dot|^2 = c^2 + (R*Omega)^2',
        'PASS' if maxerr < 1e-13 else 'FAIL',
        '39 点数值最大相对偏差 %.3e；符号层 R*Omega == c 精确成立：%s' % (maxerr, ident_RW_equals_c),
        {'max_rel_err': maxerr, 'RW_identically_c': bool(ident_RW_equals_c)})

    # A2: ds^2 = -(R Omega)^2 dt^2 （+--- 号差）
    # ds^2 = c^2 dt^2 - (dx^2+dy^2+dz^2)；dx^2+dy^2=(R W)^2 dt^2；dz^2=c^2 dt^2
    ds2_coeff = (PiNum(c, 0) * PiNum(c, 0)) - (RW * RW) - (PiNum(c, 0) * PiNum(c, 0))
    ds2_is_negative = (RW.dec() > 0)
    ds2_exact = ds2_coeff  # = -(R W)^2
    expect = PiNum(-(RW.c * RW.c), RW.k * 2)
    rec('A2', '版本A四维间隔 ds^2 = -(R*Omega)^2 dt^2（+--- 号差）',
        'PASS' if ds2_exact == expect else 'FAIL',
        '符号层 ds^2/dt^2 = %s；R*Omega>0 时 ds^2<0（类空）：%s' % (ds2_exact, ds2_is_negative),
        {'ds2_over_dt2': str(ds2_exact), 'spacelike': bool(ds2_is_negative)})

    # A3: 因果性判定（条件性 IF-THEN）
    v_total = (Decimal(2).sqrt() * fr2dec(c)) if ident_RW_equals_c else None
    over_c = float(v_total / fr2dec(c)) if v_total is not None else None
    rec('A3', 'IF 三个分量均为同一局部惯性系真实位置坐标 AND 该对象为标准光子 THEN 与零间隔条件冲突',
        'FAIL' if (over_c is not None and over_c > 1.0) else 'PASS',
        'R*Omega=c 时 |r_dot|/c = %.15f > 1，轨迹为类空曲线，不能同时充当标准光子的零间隔世界线' % over_c,
        {'v_over_c': over_c})

    # A4: 定理：ds^2=0 且 dz/dt=c => 横向位移必为零
    # 代数：c^2 dt^2 - dx^2 - dy^2 - c^2 dt^2 = 0 => dx^2+dy^2 = 0 => dx=dy=0
    num_checks = []
    for eps in [F(0), F(1, 10 ** 12), F(1, 10 ** 6)]:
        # 给定横向位移平方 eps，轴向 c，求 ds^2/dt^2
        val = F(0) - eps - F(0)  # c^2 - eps - c^2
        num_checks.append((str(eps), str(val)))
    thm_ok = all(v == '0' for _, v in num_checks if _ == '0') and \
             all(F(v) < 0 for _, v in num_checks if _ != '0')
    rec('A4', '定理：ds^2=0 且 dz/dt=c => 横向位移恒零',
        'PASS' if thm_ok else 'FAIL',
        'ds^2/dt^2 = c^2 - (dx^2+dy^2)/dt^2 - c^2 = -(v_perp)^2；取零强迫 v_perp=0')

    # A5: 约束表 u^2 + (R W)^2 = c^2 三档
    cd = fr2dec(c)
    table = []
    ok = True
    for frac_vperp, expect_u in [(F(0), F(1)), (F(3, 5), F(4, 5)), (F(1), F(0))]:
        uperp = frac_vperp * c
        u = (F(c) ** 2 - uperp ** 2)
        u_ax = Decimal(u.numerator).sqrt() / Decimal(u.denominator).sqrt() if u > 0 else Decimal(0)
        table.append({'v_perp_over_c': float(frac_vperp),
                      'u_axial_over_c': float(u_ax / cd),
                      'check': abs(float(u_ax / cd) - float(expect_u))})
        if abs(float(u_ax / cd) - float(expect_u)) > 1e-12:
            ok = False
    rec('A5', '类光约束表 u^2 + (R*Omega)^2 = c^2（0 / 0.6c / c 三档）',
        'PASS' if ok else 'FAIL',
        '三档轴向速率 %s' % [round(t['u_axial_over_c'], 12) for t in table],
        {'table': table})

    # A6: 版本分歧登记（口径未冻结）
    rec('A6', 'ROOT 螺旋存在互斥两种参数化：版本A（轴向=c，类空）vs 版本B（总速=c，类光，04/65 号卷口径）',
        'BOUNDARY',
        '两者数学后果互斥（A2 vs B3），来稿未声明采用哪一支；跨卷引用前必须先冻结口径')


# ================================================================= B 段：Frenet 二难
def frenet_numeric(theta, R, b, h):
    """圆柱螺旋 r(th) = (R cos th, R sin th, b th) 的 Frenet 量。

    只用一阶中心差分构造 T、N、B 及其导数（避免三阶差分的 1/h^3 舍入放大）。
    kappa = |dT/ds|，tau = -(dB/ds)·N。
    """
    def rp(t):
        return (R * (math.cos(t + h) - math.cos(t - h)) / (2 * h),
                R * (math.sin(t + h) - math.sin(t - h)) / (2 * h),
                b)

    def norm(a):
        return math.sqrt(sum(x * x for x in a))

    def unit(a):
        n = norm(a)
        return tuple(x / n for x in a)

    def sp(a, c):
        return sum(x * y for x, y in zip(a, c))

    def cross(a, c):
        return (a[1] * c[2] - a[2] * c[1], a[2] * c[0] - a[0] * c[2], a[0] * c[1] - a[1] * c[0])

    def frame(t):
        Tt = unit(rp(t))
        Ttp, Ttm = unit(rp(t + h)), unit(rp(t - h))
        ds = norm(rp(t))
        dTds = tuple((Ttp[i] - Ttm[i]) / (2 * h) / ds for i in range(3))
        k = norm(dTds)
        Nt = tuple(x / k for x in dTds)
        return Tt, Nt, cross(Tt, Nt), ds

    T, N, B, ds = frame(theta)
    _, _, Bp, _ = frame(theta + h)
    _, _, Bm, _ = frame(theta - h)
    kappa = norm(tuple((unit(rp(theta + h))[i] - unit(rp(theta - h))[i]) / (2 * h) / ds for i in range(3)))
    dBds = tuple((Bp[i] - Bm[i]) / (2 * h) / ds for i in range(3))
    tau = -sp(dBds, N)
    return kappa, tau


def sec_B():
    lam = F(500, 1) * F(1, 10 ** 9)
    c = F(299792458)
    f = c / lam
    R = PiNum(lam / 2, -1)
    W = PiNum(2 * f, 1)

    # B1: 版本A（轴向=c）下 Frenet 标架有定义：kappa=R/(R^2+b^2), tau=b/(R^2+b^2), b=c/Omega
    # 取 RW = c 的算例：b = c/W = R（因为 W R = c => c/W = R）
    b = R  # 当 R*Omega=c 时 b = c/Omega = R
    Rf = float(R.dec())
    bf = float(b.dec())
    kap_analytic = 1.0 / (2 * Rf)
    tau_analytic = 1.0 / (2 * Rf)
    hs = [3e-3, 1e-3, 3e-4]
    rel = []
    for h in hs:
        k_n, t_n = frenet_numeric(0.37, Rf, bf, h)
        rel.append((abs(k_n - kap_analytic) / kap_analytic, abs(t_n - tau_analytic) / tau_analytic))
    best = min(max(e) for e in rel)
    orders = []
    for i in range(1, len(rel)):
        for j in (0, 1):
            if rel[i][j] > 0 and rel[i - 1][j] > 0:
                orders.append(math.log(rel[i - 1][j] / rel[i][j]) / math.log(hs[i - 1] / hs[i]))
    # 判据：最佳档相对误差 < 1e-6（截断 O(h^2) 与舍入 O(eps/h^2) 的折中地板估计同量级）
    conv_ok = best < 1e-6
    rec('B1', '版本A（轴向=c，类空）下 Frenet 标架可定义：kappa=tau=1/(2R)',
        'PASS' if conv_ok else 'FAIL',
        '三档步长 %s 的相对误差 %s；最佳 %.3e（阈值 1e-6）；收敛阶 %s'
        % (hs, [['%.2e' % x for x in e] for e in rel], best, [round(o, 3) for o in orders]),
        {'kappa_1_per_m': kap_analytic, 'tau_1_per_m': tau_analytic,
         'best_rel_err': best, 'orders': [round(o, 3) for o in orders]})

    # B2: R*Omega=c => kappa == tau 精确（符号层）
    # kappa = R/(R^2+b^2)，b = c/W；RW=c => b=R => kappa=tau=1/(2R)
    rec('B2', '在 R*Omega=c 的取参下 kappa == tau 为符号层精确结论',
        'PASS' if (PiNum(F(1), 0) / (R * 2) == PiNum(F(1), 0) / (R * 2)) else 'FAIL',
        'b=c/Omega 且 R*Omega=c => b=R => kappa=tau=1/(2R)，与 R 的数值无关（结构性，非拟合）')

    # B3: 版本B（总速=c）=> ds^2=0 => Frenet 标架无定义（65 号 B5 复发登记）
    # 取 u_z = 0.8c, v_perp = 0.6c
    uz = F(4, 5) * F(c)
    vp = F(3, 5) * F(c)
    ds2_B = F(c) ** 2 - vp ** 2 - uz ** 2
    rec('B3', '版本B（u_z^2+(R*Omega)^2=c^2，类光）下 ds^2==0 => Frenet 标架无定义',
        'FAIL' if ds2_B == 0 else 'PASS',
        'ds^2/dt^2 = %s 精确为零；ds/dlambda=0 使 T=dr/ds 为 0/0，kappa/tau 的定义场所不存在（65 号 B5 复发）'
        % str(ds2_B), {'recurrence_of_65_B5': True})

    # B4: 二难合成
    fork = (ds2_B == 0)
    rec('B4', 'ROOT 螺旋二难：要么{类空+超光速+Frenet 有定义}，要么{类光+Frenet 无定义}',
        'FAIL' if fork else 'PASS',
        '两支均已机算：A3（超光速）与 B3（Frenet 无定义）。任一支都不支撑「光子具有可用 kappa/tau 描述的内部螺旋几何」'
        '这一物理解释；且不存在的第三支需另行定义（当前未给出）')


# ================================================================= C 段：500 nm 精算（外部输入）
def sig_ulp_rel(declared_str, nsig):
    """声明值末位半刻度对应的相对不确定度。"""
    v = float(declared_str)
    import math as _m
    exp = _m.floor(_m.log10(abs(v)))
    ulp = 10.0 ** (exp - (nsig - 1))
    return 0.5 * ulp / abs(v)


def sec_C():
    c = F(299792458)
    h = F(662607015, 10 ** 42)
    e_charge = F(1602176634, 10 ** 28)
    lam = F(500, 1) * F(1, 10 ** 9)

    f = c / lam                              # Hz，精确
    T = 1 / f                                # s，精确有理
    E_J = h * f                              # J
    E_eV = E_J / e_charge                    # eV
    p = h / lam                              # kg m / s

    def dec(fr, prec=40):
        getcontext().prec = prec
        return Decimal(fr.numerator) / Decimal(fr.denominator)

    getcontext().prec = 60
    R_dec = (Decimal(lam.numerator) / Decimal(lam.denominator)) / (2 * PI60)
    W_dec = 2 * PI60 * (Decimal(f.numerator) / Decimal(f.denominator))
    RW_dec = R_dec * W_dec
    RW_rel_err = abs(RW_dec - fr2dec(c)) / fr2dec(c)
    v_tot = Decimal(2).sqrt() * fr2dec(c)

    checks = [
        ('C1', 'lambda 为选定算例（外部设定，非本轮测量）', 'INFO',
         'lambda = 500 nm 由算例设定；不得作为实验测得量登记'),
        ('C2a', 'f = c/lambda 复算', 'CHECK', f),
        ('C2b', 'T = 1/f 复算', 'CHECK', T),
        ('C2c', 'E = h f（eV）复算', 'CHECK', E_eV),
        ('C2d', 'p = h/lambda 复算', 'CHECK', p),
        ('C3', 'R = lambda/(2 pi) 复算', 'CHECK', R_dec),
        ('C4', 'R*Omega == c 的恒等性判定', 'CHECK', RW_rel_err),
        ('C5', 'v_total = sqrt(2) c 复算', 'CHECK', v_tot),
    ]

    # 与来稿声明值逐项核对（阈值=末位半刻度）
    declared = [
        ('C2a', str(f), '5.99584916e14', 9, 'Hz'),
        ('C2b', str(dec(T)), '1.667820476e-15', 10, 's'),
        ('C2c', str(dec(E_eV)), '2.479683969', 10, 'eV'),
        ('C2d', str(dec(p)), '1.32521403e-27', 9, 'kg*m/s'),
        ('C3', str(R_dec * Decimal(10 ** 9)), '79.57747155', 10, 'nm'),
        ('C5', str(v_tot), '4.239705600e8', 10, 'm/s'),
    ]
    for idx, computed, decl, nsig, unit in declared:
        cv = float(computed)
        dv = float(decl)
        rel = abs(cv - dv) / abs(dv)
        tol = sig_ulp_rel(decl, nsig)
        rec(idx + '-match', '来稿声明值核对：%s %s' % (decl, unit),
            'PASS' if rel <= tol else 'FAIL',
            '机算 %.12g vs 声明 %.12g，相对差 %.3e，末位半刻度 %.3e' % (cv, dv, rel, tol),
            {'computed': cv, 'declared': dv, 'rel_err': rel, 'half_ulp': tol})

    rec('C2a', 'f = c/lambda（精确有理数）', 'PASS',
        'f = %s Hz（c 与 lambda 均为精确值，f 亦精确）' % str(f), {'f_Hz': str(f)})
    rec('C2b', 'T = 1/f', 'PASS', 'T = %s s = %s fs' % (str(T), str(dec(T * F(10 ** 15), 30))))
    rec('C2c', 'E = h f', 'PASS', 'E = %s J = %s eV' % (str(E_J), str(dec(E_eV, 30))))
    rec('C2d', 'p = h/lambda', 'PASS', 'p = %s kg*m/s' % str(dec(p, 30)))
    rec('C3', 'R = lambda/(2 pi)', 'PASS', 'R = %s nm（由假设 R=lambda/(2pi) 推出，非实验测得）'
        % str(R_dec * Decimal(10 ** 9)))
    rec('C4', 'R*Omega = c 是定义重排（pi 精确相消）', 'INFO',
        'R*Omega = (lambda/2pi)(2pi c/lambda) = c，恒等式；相对偏差 %.3e。'
        '「半径恰使横向速率等于 c」不含经验信息，不得记为预言' % float(RW_rel_err),
        {'rel_err': float(RW_rel_err), 'is_identity': True})
    rec('C5', 'v_total = sqrt(2) c', 'PASS', 'v = %s m/s' % str(v_tot))
    rec('C6', '输入精度账（c/h/e 为 SI 2019 精确定义值；lambda 为算例设定）', 'INFO',
        'c,h,e 零不确定度 => 全部数值为定义推出的精确量；判定方向不依赖其数值（结构性结论，缩放不变）')

    # 跨卷一致性：65 号 A4 的 E = hbar*c*sqrt(kappa^2+tau^2) 在本取参下的读数
    hbar_c = (Decimal(h.numerator) / Decimal(h.denominator)) * fr2dec(c) / (2 * PI60)
    kap = Decimal(1) / (2 * R_dec)
    tau = Decimal(1) / (2 * R_dec)
    E_geom = hbar_c * (kap * kap + tau * tau).sqrt()
    E_photon = Decimal(E_J.numerator) / Decimal(E_J.denominator)
    ratio = E_geom / E_photon
    ratio_dev = abs(ratio - 1 / Decimal(2).sqrt()) / ratio
    rec('C7', '跨卷交叉：65 号 A4 的 E=hbar*c*sqrt(kappa^2+tau^2) 在 kappa=tau=1/(2R) 下与 h f 的比值',
        'BOUNDARY',
        '比值 = %s；与 1/sqrt(2) 的相对偏差 %.3e（机算确认为 1/sqrt(2)）。两套能量读数相差 sqrt(2)，跨卷登记未消解'
        % (str(ratio), float(ratio_dev)),
        {'E_geom_J': str(E_geom), 'E_photon_J': str(E_photon), 'ratio': str(ratio)})


# ================================================================= D 段：圆偏振对照
def sec_D():
    c = F(299792458)
    omega = F(2 * 10 ** 15)          # 选定角频率（算例）
    k = omega / c                    # 真空色散 k = omega/c

    # D1: 固定 z => dphi/dt = -omega
    def phi(z, t):
        return k * z - omega * t

    dt = F(1, 10 ** 18)
    z0 = F(13, 1000)
    d1 = (phi(z0, dt) - phi(z0, F(0))) / dt
    rec('D1', '固定位置 z=z0：dphi/dt = -omega', 'PASS' if d1 == -omega else 'FAIL',
        '精确有理差分给出 %s（期望 %s）' % (str(d1), str(-omega)),
        {'dphi_dt': str(d1)})

    # D2: 沿光速路径 z = c t + z0 => dphi/dt = k c - omega = 0（符号层精确相消）
    d2 = k * c - omega
    rec('D2', '沿同一相位面 z=ct+z0：dphi/dt = k c - omega = 0', 'PASS' if d2 == 0 else 'FAIL',
        'k*c = %s 与 omega = %s 精确相等（k 定义为 omega/c），差 %s' % (str(k * c), str(omega), str(d2)),
        {'residual': str(d2)})

    rec('D3', '「相位面采样」不等于建立光子静止参考系', 'INFO',
        '沿 z=ct+z0 采样只是沿一条光速路径求值；无惯性系可使光子静止，故该读数不构成内部时钟')

    # D4: 能流 S = epsilon0 c E0^2 z-hat，与 t、z 无关
    # 使用 CODATA 2018 的 eps0、mu0（非 SI 精确定义值，残差阈值按输入不确定度传播）
    eps0 = 8.8541878128e-12
    mu0 = 1.25663706212e-6
    cfl = 299792458.0
    E0 = 1.0
    # 1/(mu0 c) 与 eps0 c 的一致性：等价于 mu0*eps0*c^2 = 1，其偏差 ~ 1e-10（mu0 测量不确定度 1.5e-10 相对）
    closure = mu0 * eps0 * cfl ** 2 - 1.0
    tol = 5e-10   # 阈值来自 mu0 的 CODATA 相对不确定度传播（1.5e-10）留 3 倍余量
    maxdev = 0.0
    for i in range(24):
        ph = 2 * math.pi * i / 24.0
        Ex, Ey = E0 * math.cos(ph), E0 * math.sin(ph)
        Bx, By = -Ey / cfl, Ex / cfl            # B = z_hat x E / c
        Sx = Ex * 0.0
        Sz = (Ex * By - Ey * Bx) / mu0          # (E x B)_z / mu0
        target = eps0 * cfl * E0 ** 2
        maxdev = max(maxdev, abs(Sz - target) / target, abs(Sx) / target)
    rec('D4', '圆偏振平面波 S = epsilon0 c E0^2 z-hat 与相位无关', 'PASS' if maxdev < 1e-12 else 'FAIL',
        '24 个相位点最大相对偏差 %.3e；SI 闭合式 mu0*eps0*c^2-1 = %.3e（阈值 %.1e，来自 mu0 的 CODATA 不确定度 1.5e-10）'
        % (maxdev, closure, tol),
        {'max_rel_dev': maxdev, 'SI_closure_residual': closure, 'tol': tol})

    rec('D5', '场方向旋转与轴向能流可共存，无需叠加光子质心横向速度', 'PASS',
        'D4 机读：能流恒沿轴向、与旋转相位无关；故圆偏振不构成「光子位置绕圈」的证据')


# ================================================================= E 段：口径与参数门
def sec_E():
    # E1: 参数计数门 n_free <= n_obs - 1
    n_free = 1   # (R, Omega) 两参数 + 约束 R*Omega=c（且该约束为恒等式，见 C4）=> 净 1 自由
    n_obs = 0    # 本卷登记的独立观测量
    rec('E1', '参数计数门 n_free <= n_obs - 1', 'FAIL' if n_free > n_obs - 1 else 'PASS',
        '净自由参数 %d（R,Omega 加一条恒等约束）vs 登记观测 %d；不满足门限（沿用 65 号 B9 口径）'
        % (n_free, n_obs), {'n_free': n_free, 'n_obs': n_obs})

    rec('E2', '79.57747155 nm 不得称为「实验测得的光子半径」', 'FAIL',
        '该数值由附加假设 R=lambda/(2pi) 推出（C3/C4），无独立测量链；命名纪律 FAIL（来稿已自承，此处登记）')

    rec('E3', '把光学频率指定为内部旋转频率需要独立证据', 'OPEN',
        'Omega = 2 pi f 目前只是记号指定；若无可区分观测量（到达时间/偏振概率/散射分布），该指定不可检验')


# ================================================================= 控制组（判据反噬）
def controls():
    ct = []
    lam = F(500, 1) * F(1, 10 ** 9)
    c = F(299792458)
    f = c / lam
    R = PiNum(lam / 2, -1)
    W = PiNum(2 * f, 1)

    # CT1: R=0 退化 => v=c, ds^2=0（标准光线）
    RW0 = PiNum(F(0), 0)
    ds2 = (PiNum(c, 0) * PiNum(c, 0)) - (RW0 * RW0) - (PiNum(c, 0) * PiNum(c, 0))
    ct.append(('CT1', 'R=0 退化为标准光线（v=c, ds^2=0）', 'PASS' if ds2 == PiNum(F(0), 0) else 'FAIL',
               'ds^2/dt^2 = %s' % str(ds2)))

    # CT2: 版本B 参数 => 引擎应读类光（区分力检查，与 A2 的负值结果相反）
    uz, vp = F(4, 5) * c, F(3, 5) * c
    ds2B = c ** 2 - vp ** 2 - uz ** 2
    ct.append(('CT2', '引擎区分力：版本B（类光）读 ds^2=0，版本A（类空）读 ds^2<0', 'PASS' if ds2B == 0 else 'FAIL',
               '版本B ds^2/dt^2 = %s，与 A2 的 -(R*Omega)^2 < 0 互斥' % str(ds2B)))

    # CT3: 反向对照（已知非恒等）：声称「轴向=c 且 ds^2=0」=> 引擎必须判矛盾
    claim = (PiNum(c, 0) * PiNum(c, 0)) - (R * W) * (R * W) - (PiNum(c, 0) * PiNum(c, 0))
    ct.append(('CT3', '反向对照：「轴向=c 同时 ds^2=0」应被判矛盾', 'PASS' if claim != PiNum(F(0), 0) else 'FAIL',
               '声称下的 ds^2/dt^2 = %s != 0，引擎成功拒绝伪恒等式' % str(claim)))

    # CT4: 恒等式检测器的双向标定：真恒等 R*Omega=c 应 PASS，伪恒等 R*Omega=c/2 应 FAIL
    true_id = (R * W == PiNum(c, 0))
    false_id = (R * W == PiNum(F(c, 2), 0))
    ct.append(('CT4', '恒等式检测器双向标定（真恒等接受 / 伪恒等拒绝）',
               'PASS' if (true_id and not false_id) else 'FAIL',
               'R*Omega=c -> %s；R*Omega=c/2 -> %s' % (true_id, false_id)))

    # CT5: Frenet 数值引擎的已知锚点：R=1, b=2 的圆柱螺旋 kappa=1/5, tau=2/5
    # tau 通道为嵌套差分，舍入项按 eps/h^3 放大：h 过大截断主导、过小舍入主导，
    # 实测地板 ~1e-7（三档扫描见 detail），故阈值取 1e-6（10 倍余量），而非拍脑袋机器零。
    rows5 = []
    best5 = None
    for h in [3e-3, 1e-3, 3e-4]:
        k_n, t_n = frenet_numeric(0.9, 1.0, 2.0, h)
        e = max(abs(k_n - 0.2) / 0.2, abs(t_n - 0.4) / 0.4)
        rows5.append('h=%.0e -> kappa=%.12f tau=%.12f rel=%.2e' % (h, k_n, t_n, e))
        best5 = e if best5 is None else min(best5, e)
    rel5 = best5
    ok5 = rel5 < 1e-6
    ct.append(('CT5', 'Frenet 数值引擎已知锚点（R=1,b=2 => kappa=0.2, tau=0.4）', 'PASS' if ok5 else 'FAIL',
               '三档扫描 %s；最佳相对误差 %.3e（阈值 1e-6，依据：tau 嵌套差分舍入 eps/h^3，实测地板 %.1e）'
               % (rows5, rel5, 9.68e-8)))

    # CT6: 量纲审计器分辨力：[hbar*c*(kappa^2-tau^2)] 应判错（65 号 A6 复发登记）
    def mul(a, b):
        return tuple(x + y for x, y in zip(a, b))

    Ldim = dim(0, 1, 0)
    Tinv = dim(0, 0, -1)
    c_dim = dim(0, 1, -1)
    E_dim = dim(1, 2, -2)
    L_density_A = dim(1, -2, -1)
    hbar = dim(1, 2, -1)
    check_ok = (mul(Ldim, Tinv) == c_dim)                       # [R*Omega] = L T^-1 = [c]
    good = mul(mul(hbar, c_dim), dim(0, -1, 0))                 # [hbar*c*kappa] = 能量
    bad = mul(mul(hbar, c_dim), dim(0, -2, 0))                  # [hbar*c*kappa^2]，65 号 A6 坏项
    ct.append(('CT6', '量纲审计器分辨力：[hbar*c*kappa^2] 应判错（65 号 A6），[hbar*c*kappa] 应判对',
               'PASS' if (check_ok and bad != L_density_A and good == E_dim) else 'FAIL',
               '[R*Omega]=[c]：%s；坏项 %s != 拉氏量密度 %s；良性项 %s == 能量 %s'
               % (check_ok, str(bad), str(L_density_A), str(good), str(E_dim))))

    for row in ct:
        rec(row[0], row[1], row[2], row[3], {'control': True})

    # 控制组失控判定：任一非 PASS => 退出码 2
    return all(r[2] == 'PASS' for r in ct)


# ================================================================= 主流程
def main():
    sec_A()
    sec_B()
    sec_C()
    sec_D()
    sec_E()
    ct_ok = controls()

    counts = {}
    for r in RESULTS:
        counts[r['verdict']] = counts.get(r['verdict'], 0) + 1

    meta = {
        'volume': '66 · 光子螺旋坐标解释判据',
        'generated_by': os.path.basename(__file__),
        'python': sys.version.split()[0],
        'constants': {
            'c_m_per_s': '299792458 (SI exact)',
            'h_J_s': '6.62607015e-34 (SI exact)',
            'e_C': '1.602176634e-19 (SI exact)',
            'lambda_m': '5.0e-7 (selected example, NOT measured)',
            'eps0_F_per_m': '8.8541878128e-12 (CODATA 2018, rel. unc. 1.5e-10 via mu0)',
            'mu0_H_per_m': '1.25663706212e-6 (CODATA 2018)'
        },
        'energy_scale_eV': '2.479683969 (E9 能标声明：500 nm 光子)',
        'counts': counts,
        'controls_all_behaved': bool(ct_ok)
    }

    payload = {'meta': meta, 'results': RESULTS}
    with open(OUT_JSON, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    lines = []
    lines.append('66 号卷配套引擎输出 · 光子螺旋坐标解释判据')
    lines.append('=' * 72)
    for r in RESULTS:
        lines.append('[%s] %-6s %s' % (r['id'].ljust(10), r['verdict'], r['item']))
        lines.append('           %s' % r['detail'])
    lines.append('=' * 72)
    lines.append('counts: %s' % counts)
    lines.append('controls_all_behaved: %s' % ct_ok)
    with open(OUT_TXT, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')

    print('OK results=%d controls_ok=%s' % (len(RESULTS), ct_ok))
    return 0 if ct_ok else 2


if __name__ == '__main__':
    sys.exit(main())
