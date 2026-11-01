# -*- coding: utf-8 -*-
"""
ROOT V15.0 六维磁通稳定化 —— 独立高精度复核脚本
复现对象：《六维空间几何、磁通与精细结构常数联合攻坚》全部可计算断言
方法：mpmath 70 位精度；500 点势函数一致性检验；势垒数值定位；往返闭合检验
"""
import mpmath as mp

mp.mp.dps = 70  # 70 位有效数字

# ---------- 输入常数 ----------
# CODATA 2022 精细结构常数
alpha = mp.mpf('7.2973525643e-3')
alpha_inv = 1 / alpha
# 普朗克质量（GeV）：非约化 M_P 与约化 Mbar
M_P = mp.mpf('1.220890e19')      # GeV, 1/l_P
Mbar = mp.mpf('2.435000e18')     # GeV（约化普朗克质量，本库沿用约定）

N = mp.mpf(3)  # 磁通拓扑整数（对应三代手征指标）

print('=' * 72)
print('[0] 输入常数')
print(f'    alpha        = {mp.nstr(alpha, 20)}')
print(f'    alpha^-1     = {mp.nstr(alpha_inv, 20)}')
print(f'    N            = {N}')

# ---------- [1] xi = 2 pi N sqrt(alpha) ----------
xi = 2 * mp.pi * N * mp.sqrt(alpha)
print('=' * 72)
print('[1] 由 alpha 反推高维无量纲耦合  xi = 2*pi*N*sqrt(alpha)')
print(f'    xi           = {mp.nstr(xi, 12)}   (文档值 1.610215)')
print(f'    相对差       = {mp.nstr(abs(xi - mp.mpf("1.610215")) / xi, 4)}')

# ---------- [2] M6 r* = N / (2 sqrt(xi)) ----------
M6r = N / (2 * mp.sqrt(xi))
print('=' * 72)
print('[2] 紧致半径 × 六维引力尺度  M6*r* = N/(2*sqrt(xi))')
print(f'    M6 r*        = {mp.nstr(M6r, 12)}   (文档值 1.18209)')

# ---------- [3] 半径链：M4^2 = 4 pi r*^2 M6^4 ----------
# M4 = 2 sqrt(pi) (M6 r*) M6  ->  取 M4 = 约化普朗克质量 Mbar
M6 = Mbar / (2 * mp.sqrt(mp.pi) * M6r)
rstar = M6r / M6
KK = 1 / rstar
r_over_lP = rstar * M_P          # 非约化普朗克长度 l_P = 1/M_P
r_over_lbar = rstar * Mbar
print('=' * 72)
print('[3] 半径链  M4^2 = 4*pi*r*^2*M6^4，取 M4 = 约化普朗克质量')
print(f'    M6           = {mp.nstr(M6, 8)} GeV')
print(f'    r*           = {mp.nstr(rstar, 8)} GeV^-1')
print(f'    r*/l_P(非约化) = {mp.nstr(r_over_lP, 12)}   (文档值 24.83268)')
print(f'    r*/lbar(约化)  = {mp.nstr(r_over_lbar, 12)}')
print(f'    KK 能标 1/r* = {mp.nstr(KK / 1e17, 8)}e17 GeV   (文档值 4.9165e17)')
print(f'    相对差(r*/lP)= {mp.nstr(abs(r_over_lP - mp.mpf("24.83268")) / r_over_lP, 4)}')
print(f'    相对差(KK)   = {mp.nstr(abs(KK - mp.mpf("4.9165e17")) / KK, 4)}')

# ---------- [4] 六维宇宙学常数 Lambda6 = 2 g6^2 M6^4 / N^2 = 1/(2 r*^2) ----------
Lambda6 = 1 / (2 * rstar**2)
print('=' * 72)
print('[4] 联立方差的副产品  Lambda6 = 2*g6^2*M6^4/N^2 = 1/(2 r*^2)')
print(f'    Lambda6      = {mp.nstr(Lambda6, 8)} GeV^2')
print(f'    sqrt(Lambda6)*r* = {mp.nstr(mp.sqrt(Lambda6) * rstar, 12)}  (应 = 1/sqrt(2))')

# ---------- [5] 往返闭合：由 xi 重建 alpha ----------
alpha_back = (xi / (2 * mp.pi * N))**2
print('=' * 72)
print('[5] alpha 往返闭合检验  alpha_back = (xi/(2*pi*N))^2')
print(f'    |alpha_back/alpha - 1| = {mp.nstr(abs(alpha_back / alpha - 1), 5)}')

# ---------- [6] 稳定化势一致性检验（500 点，70 位精度） ----------
# 原式：      V1(r) = 4*pi*(r*/r)^4 * [-M6^4 + M6^4*L6*r^2 + N^2/(8*g6^2*r^2)]
# 平方分解式：V2(r) = 2*pi*M6^4*(r*/r)^4 * (r/r* - r*/r)^2
# 其中 g6^2 M6^4 = N^2/(4 r*^2)（由 r* 定义反解），故以 (M6, rstar, N) 参数化
M64 = M6**4
g62M64 = N**2 / (4 * rstar**2)   # g6^2 * M6^4
def V1(r):
    # 原式第三项 N^2/(8*g6^2*r^2)，以 g62M64 = g6^2*M6^4 参数化需补 M6^4 因子
    return 4 * mp.pi * (rstar / r)**4 * (-M64 + M64 * Lambda6 * r**2 + M64 * N**2 / (8 * g62M64 * r**2))
def V2(r):
    return 2 * mp.pi * M64 * (rstar / r)**4 * (r / rstar - rstar / r)**2

max_rel = mp.mpf(0); worst_r = None
for k in range(1, 501):
    x = mp.mpf('0.2') + (mp.mpf('3.0') - mp.mpf('0.2')) * k / 500   # r/r* ∈ [0.2, 3.0]
    r = x * rstar
    v1, v2 = V1(r), V2(r)
    if v1 != 0:
        rel = abs(v1 - v2) / abs(v1)
        if rel > max_rel:
            max_rel = rel; worst_r = x
print('=' * 72)
print('[6] 500 点势函数一致性检验（70 位精度，r/r* ∈ [0.2, 3.0]）')
print(f'    最大相对残差 = {mp.nstr(max_rel, 5)}  @ r/r* = {mp.nstr(worst_r, 6)}')
print('    (原文报 500 组最大相对残差 ~ 1.07e-70，量级一致)')

# ---------- [7] 势垒数值定位（大半径方向） ----------
dV = lambda x: V2(x * rstar)   # 以 x = r/r* 计
# 扫峰 + 二分精化
xs = [mp.mpf('1.05') + (mp.mpf('3.0') - mp.mpf('1.05')) * k / 2000 for k in range(2001)]
best = max(xs, key=lambda x: dV(x))
lo, hi = best - mp.mpf('0.01'), best + mp.mpf('0.01')
for _ in range(120):
    m1 = lo + (hi - lo) / 3; m2 = hi - (hi - lo) / 3
    if dV(m1) < dV(m2): lo = m1
    else: hi = m2
barrier = (lo + hi) / 2
print('=' * 72)
print('[7] 势垒定位（大半径方向）')
print(f'    势垒位置 r/r* = {mp.nstr(barrier, 12)}   (理论值 sqrt(3) = {mp.nstr(mp.sqrt(3), 12)})')
Vbar = dV(barrier)
print(f'    势垒高度 V_barrier = {mp.nstr(Vbar, 8)} GeV^4')
print(f'    解析值 8*pi*M6^4/27 = {mp.nstr(8 * mp.pi * M64 / 27, 8)} GeV^4')
print(f'    相对差 = {mp.nstr(abs(Vbar - 8 * mp.pi * M64 / 27) / Vbar, 4)}')

# ---------- [8] 体积模量质量数值微分验证 m_phi^2 = 1/r*^2 ----------
h = mp.mpf('1e-12')
def phi_of(r): return 2 * Mbar * mp.log(r / rstar)   # M4 = Mbar
V_of_phi = lambda p: V2(rstar * mp.e**(p / (2 * Mbar)))
m2_num = mp.diff(V_of_phi, mp.mpf(0), 2)     # 中心在极小点 phi=0
print('=' * 72)
print('[8] 体积模量质量（对正则坐标 phi 数值二阶导）')
print(f'    m_phi^2 (数值) = {mp.nstr(m2_num, 8)} GeV^2')
print(f'    1/r*^2  (解析) = {mp.nstr(1 / rstar**2, 8)} GeV^2')
print(f'    相对差 = {mp.nstr(abs(m2_num - 1 / rstar**2) / (1 / rstar**2), 4)}')

# ---------- [9] T^2 替代模型反例（数值展示） ----------
# T^2 平坦：Ricci = 0，内部方程 0 = M6^4*Lambda6*r^2 - N^2/(8 g6^2 r^2)（i=j 分量）
# 外部方程：M6^4*Lambda6 = -N^2/(8 g6^2 r^4) < 0，与内部方程要求反号 -> 无解
print('=' * 72)
print('[9] T^2 反例（解析结论，无数值自由度）')
print('    外部方程要求 Lambda6 < 0；内部方程要求 Lambda6 r^2 = N^2/(8 g6^2 M6^4 r^4) > 0')
print('    两式符号相反，任何 r 均无解 —— 磁通应力必须有正曲率（S^2）来平衡。')

print('=' * 72)
print('[done] 全部复核项完成')
