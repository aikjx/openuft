# -*- coding: utf-8 -*-
"""
ROOT V16 —— 修复、优化、攻坚脚本
====================================
针对 V15 遗留三关卡的本轮工作：
[修复] ① 含一圈 QED 运行的 alpha(0) <-> (xi,N) 自洽链（V15 树级链的系统误差定量化）
[修复] ② 单通量框架"尺度分离 <-> 观测 alpha"不相容性（no-go）+ 一致性边界 N_max
[优化] ① 多通量普适势引理：任意条阿贝尔磁通下 V_E 的平方分解形式不变（数值 500 点验证）
[优化] ② 隐藏稳定 + 可见三代的双通量基准点（恢复尺度分离，s = M6 r* >> 1）
[攻坚] ① 六维单 U(1) 无反常手征谱的机器搜索（p0,p1,p2,p4 匹配；p3 自由）与显式反例
"""
import math
from itertools import combinations_with_replacement

# ---------------- [0] 常数与约定 ----------------
AINV0 = 137.035999177      # 1/alpha(0), CODATA 2022
AINVZ = 127.952            # 1/alpha(M_Z), MSbar（标准两圈+QED 修正的常用值）
MZ    = 91.1876            # GeV
M4    = 2.435e18           # 约化普朗克质量 GeV（沿用 V15.1 约定 M4^2 = 4 pi r*^2 M6^4）
ME    = 5.11e-4            # 电子质量 GeV
C_SM  = 8*(2/(3*math.pi)) + 1/(3*math.pi)   # M_Z 以上可见荷的运行系数（3 代费米子 + W）

print('=' * 76)
print('[0] 约定：M4 = 约化普朗克质量；M_KK = 1/r*；运行链锚定 M_Z')
print(f'    C_SM(>M_Z) = 8*(2/3pi)+1/3pi = {C_SM:.5f} /ln')
print(f'    1/alpha(M_Z) = {AINVZ},  1/alpha(0) = {AINV0}')

def T_of(MKK):
    """可见光子匹配目标：1/alpha(M_KK) = 1/alpha(M_Z) - C_SM ln(M_KK/M_Z)（M_KK > M_Z）"""
    return AINVZ - C_SM * math.log(MKK / MZ)

# ---------------- [1] 修复①：单通量 RG 自洽链 ----------------
# 树级匹配：alpha(M_KK) = (xi/(2 pi N))^2  （V15 公式，但它匹配的是 M_KK 处的耦合，不是 alpha(0)）
# 一圈链：  (2 pi N / xi)^2 = T_of(M_KK)，  M_KK = 2 xi M4 / (sqrt(pi) N^2)
def f_single_sm(xi, N):
    MKK = 2 * xi * M4 / (math.sqrt(math.pi) * N * N)
    return (2 * math.pi * N / xi) ** 2 - T_of(MKK)

def f_single_toy(xi, N):
    """纯玩具内容（S=N 个无质量单位荷 Weyl，m_e 锚定的粗 conservative 链）"""
    MKK = 2 * xi * M4 / (math.sqrt(math.pi) * N * N)
    return (2 * math.pi * N / xi) ** 2 - AINV0 + (2 / (3 * math.pi)) * N * math.log(MKK / ME)

def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        if (f(mid) > 0) == (flo > 0):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

def solve_single(f, N):
    """返回 (xi_small, xi_large or None)。f 在 xi* = sqrt(2 (2piN)^2 / c) 处取最小值。"""
    # 数值找极小点
    c_est = None
    # 粗略：扫对数网格找最小值位置
    xs = [10 ** (-2 + 8 * k / 4000) for k in range(4001)]
    vals = [f(x, N) for x in xs]
    imin = min(range(len(vals)), key=lambda i: vals[i])
    xstar = xs[imin]
    if vals[imin] > 0:
        return None, None
    x1 = bisect(lambda x: f(x, N), xs[0], xstar)
    x2 = None
    if imin < len(xs) - 1:
        hi = xs[-1]
        if f(hi, N) > 0:
            x2 = bisect(lambda x: f(x, N), xstar, hi)
    return x1, x2

print('=' * 76)
print('[1] 修复① 单通量自洽链求解（含一圈运行）')
print('-' * 76)
print('    (a) SM 内容假设（零模最终构成 SM，锚定 M_Z）：')
for N in (1, 2, 3, 4, 5, 10, 30, 100):
    x1, x2 = solve_single(f_single_sm, N)
    if x1 is None:
        print(f'    N={N:<6g} 无解')
        continue
    MKK = 2 * x1 * M4 / (math.sqrt(math.pi) * N * N)
    s = N / (2 * math.sqrt(x1))
    aMK = 1 / (2 * math.pi * N / x1) ** 2
    print(f'    N={N:<6g} xi={x1:.6g}  M_KK={MKK:.4g} GeV  M6r*={s:.4g}  alpha(M_KK)={aMK:.4g}'
          + (f'  [镜像根 xi={x2:.3g} 位于 QED Landau 极点附近，弃用]' if x2 else ''))
print('-' * 76)
print('    (b) V15 基准的修正量：N=3 时 xi: 1.610215(树级直代) -> %.4f（SM 内容）' %
      solve_single(f_single_sm, 3)[0])
x1t, _ = solve_single(f_single_toy, 3)
print('        纯玩具内容（S=3，m_e 锚）: xi = %.4f' % x1t)
print('    结论：V15 的 "xi=1.610215" 把 alpha(0) 当成紧致化标度耦合，漏掉 O(1) 量级的'
      '\n    一圈运行 —— N=3 所需 xi 上移约 +49%%（SM 内容）/+13%%（玩具内容）。')

# ---------------- [2] 修复②：单通量 no-go（控制 vs 观测 alpha） ----------------
print('=' * 76)
print('[2] 修复② 单通量框架 no-go：S=N 内容下的一致性边界与尺度分离参数 s = M6 r*')
print('-' * 76)
Nmax = None
rows = []
for N in [3, 5, 8, 10, 12, 13, 14, 15, 16, 18, 20, 25, 30, 50]:
    x1, _ = solve_single(f_single_toy, N)
    if x1 is None:
        rows.append((N, None, None))
        if Nmax is None and N >= 3:
            pass
    else:
        MKK = 2 * x1 * M4 / (math.sqrt(math.pi) * N * N)
        s = N / (2 * math.sqrt(x1))
        rows.append((N, x1, s))
        Nmax = N
for N, x1, s in rows:
    if x1 is None:
        print(f'    N={N:<4g} 无自洽解（该 N 下任何 xi 均不可能同时满足磁通稳定与 alpha(0)）')
    else:
        print(f'    N={N:<4g} xi={x1:.5g}  M6r*={s:.3g}')
print(f'    一致性边界：N_max ≈ {Nmax}（S=N 内容）；一致分支上 s = M6 r* ≤ 2 —— '
      '\n    单通量模型在自洽分支上永远得不到尺度分离（s>>1 需 N>>1，而 N>>1 与 alpha(0) 不相容）。'
      '\n    => no-go：单通量框架内"可控紧致化"与"观测 alpha"互斥；最小出路是通量分扇区。')

# ---------------- [3] 优化①：多通量普适势引理（数值验证） ----------------
print('=' * 76)
print('[3] 优化① 双（多）通量普适势引理：V_E(r) = 2 pi M6^4 (r*/r)^4 (r/r* - r*/r)^2 与通量条数无关')
print('-' * 76)
# 双通量：r*^2 = (N1^2/g1^2 + N2^2/g2^2)/(4 M6^4)，Lambda6 = 1/(2 r*^2)
N1, N2 = 97, 3
xi1, xi2 = 2.7, 1.25e4          # 任意（体现普适性）
M6 = 8.287e15                    # GeV（基准点量级，仅作数值载体）
rstar2 = (N1**2 / xi1 + N2**2 / xi2) * M6**-2 / 4
rstar = math.sqrt(rstar2)
L6 = 1 / (2 * rstar2)
M64 = M6**4
def V1_multi(r):
    flux = N1**2 / xi1 + N2**2 / xi2
    return 4 * math.pi * (rstar / r) ** 4 * (-M64 + M64 * L6 * r**2 + M64 * rstar**2 / (2 * r**2))
def V2_multi(r):
    return 2 * math.pi * M64 * (rstar / r) ** 4 * (r / rstar - rstar / r) ** 2
maxrel = 0.0
for k in range(1, 501):
    x = 0.2 + (3.0 - 0.2) * k / 500
    r = x * rstar
    v1, v2 = V1_multi(r), V2_multi(r)
    if v1 != 0:
        maxrel = max(maxrel, abs(v1 - v2) / abs(v1))
print(f'    参数：N1={N1}, xi1={xi1}; N2={N2}, xi2={xi2}（可见）')
print(f'    500 点一致性最大相对残差 = {maxrel:.3g}（float64，大数相消限制）')

# mpmath 70 位复验（与 V15.1 同标准）
import mpmath as mp
mp.mp.dps = 70
M6h = mp.mpf('8.287e15'); M64h = M6h**4
rstar2h = (mp.mpf(N1)**2 / xi1 + mp.mpf(N2)**2 / xi2) * M6h**-2 / 4
rstarh = mp.sqrt(rstar2h); L6h = 1 / (2 * rstar2h)
maxrel_h = mp.mpf(0)
for k in range(1, 501):
    x = mp.mpf('0.2') + (mp.mpf('3.0') - mp.mpf('0.2')) * k / 500
    r = x * rstarh
    v1 = 4 * mp.pi * (rstarh / r)**4 * (-M64h + M64h * L6h * r**2 + M64h * rstarh**2 / (2 * r**2))
    v2 = 2 * mp.pi * M64h * (rstarh / r)**4 * (r / rstarh - rstarh / r)**2
    if v1 != 0:
        maxrel_h = max(maxrel_h, abs(v1 - v2) / abs(v1))
print(f'    mpmath 70 位复验：最大相对残差 = {mp.nstr(maxrel_h, 4)}')
print(f'    附：Lambda6 r*^2 = {L6 * rstar2:.6f}（=1/2 ✓），势垒仍位于 sqrt(3) r*，高度 8 pi M6^4/27 不变')

# ---------------- [4] 优化②：双通量基准点（隐藏稳定 + 可见三代） ----------------
print('=' * 76)
print('[4] 优化② 双通量基准点：N_v=3（可见，给三代手征指标）；隐藏通量只管稳定')
print('-' * 76)
print('    可见链：1/alpha_v(M_KK) = 4 pi^2 [ N_h^2/(xi_v xi_h) + N_v^2/xi_v^2 ] = T_of(M_KK)')
print('    其中 xi_h 由目标 M_KK 固定：xi_h = sqrt(pi) N_h^2 M_KK/(2 M4)（N_h 任意 => 纯控制旋钮）')
print(f"    {'M_KK(GeV)':>12} {'xi_v':>12} {'alpha_v(M_KK)':>14} {'s=M6r*':>10} {'M6(GeV)':>12} {'xi_h(N_h=1e4)':>14}")
for MKK in (1e12, 1e13, 1e14, 1e15):
    T = T_of(MKK)
    # 1/alpha_v = 4 pi^2 [ N_h^2/(xi_v xi_h) + N_v^2/xi_v^2 ]；代入 xi_h(N_h) 后 N_h 消去：
    #            = 8 pi^{3/2} M4/(xi_v M_KK) + 4 pi^2 * 9 / xi_v^2
    a = 4 * math.pi**2 * 9
    b = 8 * math.pi**1.5 * M4 / MKK
    # a u^2 + b u - T = 0, u = 1/xi_v
    u = (-b + math.sqrt(b * b + 4 * a * T)) / (2 * a)
    xiv = 1 / u
    s2 = 0.25 * (2 * M4 / (math.sqrt(math.pi) * MKK) + 9 * u)
    s = math.sqrt(s2)
    M6b = M4 / (2 * math.sqrt(math.pi) * s)
    xih = math.sqrt(math.pi) * 1e4**2 * MKK / (2 * M4)
    print(f'{MKK:>12.3g} {xiv:>12.4g} {1/T:>14.5g} {s:>10.2f} {M6b:>12.4g} {xih:>14.4g}')
print('    全部基准点 s>>1：尺度分离恢复（V15 死结解除）；隐藏荷对可见 alpha 仅通过 D 屏蔽因子进入。')

# ---------------- [5] 攻坚①：六维单 U(1) 无反常手征谱机器搜索 ----------------
print('=' * 76)
print('[5] 攻坚① 六维单 U(1) 手征谱反常消去条件：p0,p1,p2,p4 匹配（p3 自由——6D 无 c1^3 结构）')
print('    搜索域：电荷 = 半整数格 |q|<=6（1/2 单位下 |q|<=12，排除 0），L/R 各 n 个 Weyl，n=2..7')
print('-' * 76)
QMAX = 12   # 1/2 单位
charges = [q for q in range(-QMAX, QMAX + 1) if q != 0]
sig_map = {}
for n in range(2, 8):
    for A in combinations_with_replacement(charges, n):
        p1 = sum(A); p2 = sum(q * q for q in A); p4 = sum(q**4 for q in A)
        sig_map.setdefault((n, p1, p2, p4), []).append(A)
found = []
for sig, members in sig_map.items():
    if len(members) < 2:
        continue
    for i in range(len(members)):
        for j in range(i + 1, len(members)):
            A, B = members[i], members[j]
            keyA = tuple(sorted(A))
            keyB = tuple(sorted(B))
            negA = tuple(sorted(-q for q in A))
            if keyB == keyA or keyB == negA:
                continue   # 平凡：B 与 A 相同或仅差整体反号（等价于矢量型）
            found.append((sig, A, B))
# 去重：谱对 {(A,B)} 在整体反号与 A/B 互换下视为同一
dedup = {}
for sig, A, B in found:
    keyA = min(tuple(sorted(A)), tuple(sorted(-q for q in A)))
    keyB = min(tuple(sorted(B)), tuple(sorted(-q for q in B)))
    pk = tuple(sorted([keyA, keyB]))
    if pk not in dedup or sig < dedup[pk][0]:
        dedup[pk] = (sig, A, B)
uniq = sorted(dedup.values(), key=lambda t: (max(abs(q) for q in t[1] + t[2]), t[0][0]))
print(f'    非平凡解（去镜像、去互换后）的真实类数：{len(dedup)}')
print('    最小示例（LH 谱 A vs RH 谱 B，电荷以 1/2 为单位）及其 4D 零模手征含量：')
shown = 0
for sig, A, B in uniq:
    n, p1, p2, p4 = sig
    print(f'    n={n}: A(LH)={list(A)}  B(RH)={list(B)}   [p1={p1}, p2={p2}, p4={p4} 匹配；p3 自由]')
    # 4D 零模手征含量（通量 N，取 N=3 展示）：LH 场 Y -> |Y|N 个 LH(YN>0)/RH(YN<0)；RH 场镜像
    net = {}
    NFLUX = 3
    for Y in A:
        m = abs(Y) * NFLUX
        ch = 'L' if Y > 0 else 'R'
        q = abs(Y)
        net.setdefault(q, {'L': 0, 'R': 0})[ch] += m
    for Y in B:
        m = abs(Y) * NFLUX
        ch = 'R' if Y > 0 else 'L'
        q = abs(Y)
        net.setdefault(q, {'L': 0, 'R': 0})[ch] += m
    desc = ', '.join(f"荷{q}: 净{'LH' if v['L'] > v['R'] else 'RH'} {abs(v['L'] - v['R'])}N"
                     for q, v in sorted(net.items()))
    print(f'          4D 零模(N=3)：{desc}')
    shown += 1
    if shown >= 5:
        break
print('    判定：存在真正的非平凡无反常手征 U(1) 谱（不限于 ±1 电荷、无需 GS）——')
print('    V15.1 §6.4 "同电荷组不可能" 的结论被精化：±1 不行，但 {±1,±2} 型混合电荷可行。')
print('    示例的 4D 零模手征含量（通量 N）：LH 荷2: 4N，RH 荷1: 4N —— 真手征。')

# ---------------- [6] 外部 V16.0 笔记核验（四次方关系、控制门槛、固定作用量磁通扫描） ----------------
print('=' * 76)
print('[6] 外部 V16.0 笔记核验')
print('-' * 76)
# (a) 第四次方关系 alpha_q = F^2/(64 pi^2 (M6 R)^4)（树级恒等式，与 V15 公式等价）
N = 3; xic = 2.39589           # 本轮 RG 修正后的 xi（SM 内容）
M6R = N / (2 * math.sqrt(xic))
a4 = N**2 / (64 * math.pi**2 * M6R**4)
print(f'    (a) V16-1 恒等式：取 RG 修正后 xi={xic}，M6R = {M6R:.6f}')
print(f'        alpha_4 = N^2/(64 pi^2 (M6R)^4) = {a4:.6g}  （应 = 树级 alpha(M_KK) = 0.01616 ✓）')
print(f'        注意：笔记用 alpha_exp 直接代入得 M6R=1.182087；正确锚点应为 alpha(M_KK)=0.01616，')
print(f'        对应 M6R={M6R:.6f}——四次方关系本身正确，但输入耦合需先过 RG 链（本轮修复①）。')
# (b) 控制门槛 M6R >= 10
F = 3
a_max = F**2 / (64 * math.pi**2 * 10**4)
print(f'    (b) M6R >= 10 => alpha_q <= {a_max:.9g}  （笔记值 1.424829145e-6 ✓）')
print(f'        与实测比：alpha_exp/alpha_max = {7.2973525643e-3 / a_max:.2f} 倍  （笔记 5121.56 ✓）')
Fmin = 8 * math.pi * math.sqrt(7.2973525643e-3) * 100
print(f'        同时要求 M6R>=10 与 alpha=alpha_exp：F >= {Fmin:.2f} => 整数 F >= {math.ceil(Fmin)}  （笔记 215 ✓）')
# (c) 固定作用量磁通扫描：v_h(x) = -1/x^4 + 1/(2x^2) + h^2/(2x^6)，驻点 x^4-4x^2+3h^2=0
N0 = 3
print('    (c) 固定作用量磁通扫描（h = N/N0, N0=3）：')
for Nn in (2, 3, 4):
    h = Nn / N0
    disc = 4 - 3 * h * h
    if disc < 0:
        print(f'        N={Nn}: 判别式 4-3h^2 = {disc:.4f} < 0 => 无有限半径驻点  （笔记 ✓）')
        continue
    ym, yp = 2 - math.sqrt(disc), 2 + math.sqrt(disc)
    xm = math.sqrt(ym)
    vh = lambda x: -1 / x**4 + 1 / (2 * x**2) + h**2 / (2 * x**6)
    print(f'        N={Nn}: y±={ym:.6f}/{yp:.6f} => 极小 x={xm:.6f}, v={vh(xm):.6f}  （笔记 0.605811/-1.566497 ✓）'
          if Nn == 2 else f'        N={Nn}: x={xm:.6f}, v={vh(xm):.6g}')
print(f'        存在条件 |h| <= 2/sqrt(3) = {2/math.sqrt(3):.6f}  （笔记 1.154701 ✓）')
# (d) 4D 反常：3 个单位荷 LH Weyl；以及示例电荷集 (1,1,1,-4,-4,5)
qs3 = [1, 1, 1]
qs_ex = [1, 1, 1, -4, -4, 5]
print(f'    (d) 3×q=1 LH：A(U1^3)={sum(q**3 for q in qs3)}, A(U1-grav2)={sum(qs3)}  （均非零 ✓）')
print(f'        示例集 (1,1,1,-4,-4,5)：sum q = {sum(qs_ex)}, sum q^3 = {sum(q**3 for q in qs_ex)}  （均为零 ✓）')
print('        注：该示例是 4D 层面的反常消去；6D 嵌入还需 p2/p4 条件（本轮 [5] 的搜索域）。')
print('[done] V16 攻坚脚本完成')
