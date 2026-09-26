# -*- coding: utf-8 -*-
"""
空间螺旋修复版 · C25 追加：高阶本征能级 alpha_n 的高精度扫描与误差棒

问题（用户下达）
----------------
对 C25 的本征能级做"高精度扫描、输出误差棒"。

为什么这里能给出**严格**误差棒（而不是估计）
--------------------------------------------
`spiral_frenet_spectral_c25.py` 的 B 段哈密顿量是
    H = -(hbar^2/2m) d^2/ds^2 + E_scale * (kappa^2 + tau^2)
而完美圆柱螺旋的 kappa、tau 沿弧长是**常数**（kappa^2+tau^2 = w^2/c^2），
所以"势"是一个常数偏移，能谱有闭式：
    连续谱   E_n^cont = E_scale*V0 + (hbar^2/2m) * (2 pi n / L)^2
    差分谱   E_n^FD   = E_scale*V0 + (hbar^2/2m) * (4N^2/L^2) sin^2(pi n / N)
二者之比只作用在**动能项**上：
    动能相对偏差  d(n;N) = (sin x / x)^2 - 1,  x = pi n / N      (<= 0, 单调)
⇒ 误差棒不必靠收敛试验猜，它是解析的；扫描里再用 Richardson (N,2N) 独立复算一遍，
   两条路必须逐位吻合，否则是本脚本自己算错。

三件必须如实说出的事
--------------------
1. **常数偏移会稀释误差。** 按"整条能级"报相对误差，会把 d(n;N) 缩小
   offset/(offset+动能) 倍；误差棒必须报在动能/能隙上，否则是"对零而非对底"。
2. **高阶能级在点阵上会被混叠（aliasing）吃掉。** E_{N-n}^FD == E_n^FD 精确成立，
   所以 N 点网格只有约 N/2 条**互异**能级，n = N/2 之上不是"更高的能级"，
   而是低能级的镜像；n = N 混叠回 n = 0。"往高阶扫"这件事本身受点阵上限约束。
3. **扫到能读出 alpha 的那一级，需要不可实现的网格。** 能隙 r_n = n^2 * (hbar^2/2m)/E_scale
   与几何完全脱耦（B 段 C1 已证），要 r_n = alpha 需要 n* = sqrt(alpha/g1) ~ 3.1e11；
   在那一级上把动能误差压到 1% 需要 N ~ 5.7e12 格点。⇒ 本扫描的输出**加强** C25 的
   既有判定（alpha 不能由螺旋几何单独钉定），不给它升等级。

约定
----
* 只用标准库 `math`（本目录 README §1 的红线：不引入 sympy / mpmath）。
  与 B 段 mpmath 版的关系：本脚本不重做 250 位对角化，而是用**独立第二条路**
  （Rayleigh 残差 ||H v - lam v|| / |lam|，v 取解析本征向量）核验闭式确实是那台
  差分矩阵的谱。
* 退出码默认恒为 0（本目录约定：审计脚本不因发现矛盾而失败，判定写在输出里）。
  加 `--strict` 时，任何一条内部判据为 FAIL 则退出码 1（供变异检验用）。
运行：python spiral_c25_alpha_n_scan.py [--nmax 40] [--tiers 32,64,128,256,512,1024] [--strict]
"""

import json
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ------------------------------------------------------------------ 常数（CODATA 2018，外部输入）
C = 299792458.0
HBAR = 1.054571817e-34
ME = 9.1093837015e-31
ALPHA = 7.2973525693e-3
ALPHA_137 = 1.0 / 137.0            # 文献取整口径，仅作对比靶（见 README §5.3）

# ------------------------------------------------------------------ 螺旋几何（与 B 段同参数）
A_M = 1e-15
B_M = 1e-15
W = C / math.sqrt(A_M ** 2 + B_M ** 2)     # 约束 omega*sqrt(A^2+b^2)=c
L = 2.0 * math.pi * math.sqrt(A_M ** 2 + B_M ** 2)   # 一圈弧长 = c*(2pi/w)
V0 = W ** 2 / C ** 2                                # kappa^2 + tau^2（常数）
E_SCALE = ME * C ** 2                               # 外部能量尺度（电子静能），显式外部输入
OFFSET = E_SCALE * V0
KIN = HBAR ** 2 / (2.0 * ME)                        # J*m^2

JUDGE = []


def judge(sid, title, ok, detail):
    JUDGE.append({"id": sid, "title": title,
                  "verdict": "PASS" if ok else "FAIL", "detail": detail})
    return ok


def k_cont(n):
    """连续谱动能本征值（波数平方）。"""
    return (2.0 * math.pi * n / L) ** 2


def k_fd(n, N):
    """N 点周期二阶差分矩阵的解析本征值（波数平方）。"""
    h = L / N
    return (2.0 / (h * h)) * (1.0 - math.cos(2.0 * math.pi * n / N))


def kinetic_bias(n, N):
    """d(n;N) = (sin x / x)^2 - 1，x = pi n / N；n=0 时取 0。"""
    x = math.pi * n / N
    if x == 0.0:
        return 0.0
    return (math.sin(x) / x) ** 2 - 1.0


def energy(n, N, kind):
    return OFFSET + KIN * (k_cont(n) if kind == 'cont' else k_fd(n, N))


def rayleigh_residual(n, N):
    """第二条独立路：把解析本征向量代入实际差分矩阵，量残差。

    v_j = cos(2 pi n j / N)（周期二阶差分的本征向量，退化对里取一条），
    (Hv)_j = (2t + OFFSET) v_j - t (v_{j-1} + v_{j+1})，t = KIN/h^2。
    残差归一到 |lam|。这条路与闭式公式互相独立：闭式写错就会被抓住。
    """
    h = L / N
    t = KIN / (h * h)
    lam = OFFSET + 2.0 * t * (1.0 - math.cos(2.0 * math.pi * n / N))
    worst = 0.0
    for j in range(N):
        v = math.cos(2.0 * math.pi * n * j / N)
        vm = math.cos(2.0 * math.pi * n * ((j - 1) % N) / N)
        vp = math.cos(2.0 * math.pi * n * ((j + 1) % N) / N)
        hv = (2.0 * t + OFFSET) * v - t * (vm + vp)
        rel = abs(hv - lam * v) / (abs(lam) * max(abs(v), 1e-30) + 1e-300)
        worst = max(worst, rel)
    return worst


def richardson(n, N):
    """在**动能标度**上做 O(h^2) 外推与误差棒估计。

    不在整条能级上做：OFFSET/动能 = 1/7.5e-26 ~ 1e25，双精度里整条能级相减会把
    动能连同一个网格一起吞掉（本脚本 [2] 段把这件事本身当成一条判据打印出来）。
    误差由 err(N)=c h^2 推：(k(2N)-k(N))/3 = -err(2N) ⇒ 估计量的**幅值**应等于
    N=2N 处的解析偏差，且 err(N)/err(2N) 应收敛到 4。
    """
    k1, k2 = k_fd(n, N), k_fd(n, 2 * N)
    kc = k_cont(n)
    if kc == 0.0:                       # n=0：动能本身为零，相对误差无定义，按 0 记
        return 0.0, 0.0, 0.0
    return ((k2 - k1) / 3.0 / kc, (k1 - kc) / kc, (k2 - kc) / kc)


def n_for_bias(tol, n):
    """解 1 - (sin x / x)^2 = tol 求 x，再由 x = pi n / N 反解所需网格 N。"""
    lo, hi = 0.0, math.pi / 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        f = 0.0 if mid == 0 else 1.0 - (math.sin(mid) / mid) ** 2
        if f < tol:
            lo = mid
        else:
            hi = mid
    x = 0.5 * (lo + hi)
    return x, (math.pi * n / x if x > 0 else float('inf'))


def main(argv):
    strict = '--strict' in argv
    nmax = 40
    tiers = [32, 64, 128, 256, 512, 1024, 2048]
    for i, a in enumerate(argv):
        if a == '--nmax':
            nmax = int(argv[i + 1])
        elif a == '--tiers':
            tiers = sorted(int(x) for x in argv[i + 1].split(','))
    print('=' * 78)
    print('C25 追加：高阶本征能级 alpha_n 扫描与误差棒（标准库 math；dps 无关，双精度）')
    print('=' * 78)
    print('几何：A=%g m、b=%g m、omega=%g rad/s、一圈弧长 L=%g m' % (A_M, B_M, W, L))
    print('常数势偏移 OFFSET=E_scale*(k^2+t^2)=%g J；动能系数 KIN=%g J*m^2' % (OFFSET, KIN))
    g1 = KIN / E_SCALE
    print('单层能隙系数 g1=(hbar^2/2m)/E_scale = %r' % g1)

    # ---- 1) 闭式 == 矩阵谱（Rayleigh 残差），并复核 B 段口径 ----
    print('\n[1] 闭式与本征矩阵的一致性（独立第二条路：Rayleigh 残差）')
    for N in (32, 128, 1024):
        worst = max(rayleigh_residual(n, N) for n in range(1, min(N // 2, 12) + 1))
        judge('S1-N%d' % N, 'N=%d 前 12 条解析本征向量代入矩阵，最大相对残差 < 1e-12' % N,
              worst < 1e-12, 'max rel residual = %r' % worst)
        print('  N=%-5d max ||Hv-lam v||/|lam| = %r  %s'
              % (N, worst, 'PASS' if worst < 1e-12 else 'FAIL'))
    # 与 B 段完全同一个 N=32 的最低几条能级对照（口径必须一致）
    b_row = [(n, energy(n, 32, 'fd'), energy(n, 32, 'cont')) for n in range(4)]
    print('  N=32 前 4 条：E_FD / E_cont')
    for n, efd, eco in b_row:
        print('    n=%d  E_FD=%r  E_cont=%r  相对偏差=%r' % (n, efd, eco, (efd - eco) / eco))

    # ---- 2) 逐阶扫描 + 误差棒（全部在动能标度上做）----
    Nref = tiers[len(tiers) // 2]
    print('\n[2] 高阶扫描：动能误差棒（闭式 / 由差分本征值实测 / Richardson 估计），N=%d、2N=%d'
          % (Nref, 2 * Nref))
    print('  %-4s %-22s %-16s %-16s %-16s %-9s %s'
          % ('n', 'dE_n=E_n-E_0 [J]', 'd_kin 实测(N)', 'd_kin 闭式(N)', 'Richardson(=d(2N))',
             '阶比 d(N)/d(2N)', '备注'))
    rows = []
    closed_gap = []
    for n in range(0, nmax + 1):
        dE = KIN * k_cont(n)                       # 连续谱上第 n 条与基态之差（可分辨量）
        est, d_meas, d_meas2 = richardson(n, Nref)
        d_ana = kinetic_bias(n, Nref)
        ratio = (d_meas / d_meas2) if d_meas2 else float('nan')
        aliased = n > Nref // 2
        note = '已越过 Nyquist（混叠区，非新能级）' if aliased else ''
        rows.append({'n': n, 'dE_cont_J': dE, 'd_kin_measured': d_meas,
                     'd_kin_closed_form': d_ana, 'richardson_est': est,
                     'order_ratio': ratio, 'N': Nref, 'aliased': aliased})
        # n=0 的动能本身为零，相对量无定义，按「—」显示（勿读成 0 误差）
        print('  %-4d %-22r %-16r %-16r %-16r %-9s %s'
              % (n, dE, d_meas, d_ana, est, '—' if n == 0 else '%.9r' % ratio, note))
        if 1 <= n <= Nref // 2:
            closed_gap.append(abs(d_meas - d_ana))
    judge('S2a', '闭式 d=(sin x/x)^2-1 与差分本征值实测逐条吻合（<1e-12，非混叠区）',
          closed_gap and max(closed_gap) < 1e-12,
          'max |实测 - 闭式| = %r（n=1..%d）' % (max(closed_gap), Nref // 2))
    # 阶比不是恒等于 4：展开参数是 x=pi n/N，d(x) = -x^2/3 + 2x^4/45 - ...，
    # 所以 d(x)/d(x/2) -> 4 只在 x->0 成立。正确的判据是"实测阶比 == 闭式阶比"，
    # 而 x->4 的偏离量本身就是 Richardson 误差棒**自身**的误差，见 S2c/S2e。
    ratio_gap = []
    for r in rows:
        if 1 <= r['n'] <= Nref // 2:
            ana = kinetic_bias(r['n'], Nref) / kinetic_bias(r['n'], 2 * Nref)
            ratio_gap.append(abs(r['order_ratio'] - ana) / abs(ana))
    judge('S2b', '实测阶比 d(N)/d(2N) 与闭式阶比逐条一致（<1e-9）；趋 4 只在小 x 端成立（勿把'
                 'O(h^2) 当成全区间事实）', max(ratio_gap) < 1e-9,
          'max 相对失配 = %r；n=%d 处阶比 = %r（x = %r）'
          % (max(ratio_gap), nmax, rows[nmax]['order_ratio'], math.pi * nmax / Nref))
    ric_err = []
    for r in rows:
        if 1 <= r['n'] <= Nref // 2:
            true2 = kinetic_bias(r['n'], 2 * Nref)
            x2 = math.pi * r['n'] / (2 * Nref)
            ric_err.append((abs(abs(r['richardson_est']) - abs(true2)) / abs(true2),
                            0.2667 * x2 * x2, r['n']))
    worst = max(ric_err, key=lambda t: t[0] / max(t[1], 1e-300))
    judge('S2c', 'Richardson 估计量的自身误差被先验界 0.2667 x^2 卡住（x=pi n/2N）⇒ 误差棒'
                 '可只用两张网格算出，且**它自己的**误差棒有解析上界',
          all(e <= b * 1.02 for e, b, _n in ric_err),
          '最紧一例 n=%d：自身相对失配 %r vs 界 %r' % (worst[2], worst[0], worst[1]))
    # Richardson 可信区：自身失配 <= tol 的最大 n（先验式，不依赖本次扫描结果）
    for tol in (0.01, 0.05):
        xz = math.sqrt(tol / 0.2667)
        print('  Richardson 误差棒自身失配 <= %g%% 要求 x <= %r ⇒ n <= %r（N=%d 时；'
              '越过此线只有闭式偏差仍可用）' % (100 * tol, xz, xz * 2 * Nref / math.pi, Nref))
    zero_at_total = all(energy(n, Nref, 'fd') == energy(n, Nref, 'cont')
                        for n in range(1, Nref // 2 + 1))
    judge('S2d', '按"整条能级"报误差棒在双精度下直接归零（OFFSET/动能 ~ %r）⇒ '
                 '误差棒必须报在动能/能隙标度上；这不是"误差很小"，是"该口径看不见误差"'
                 % (1.0 / g1), zero_at_total,
                 'n=1..%d 全部 E_FD == E_cont（逐位相等）；g1 = %r' % (Nref // 2, g1))
    print('  口径判据：OFFSET=%r J 对 KIN*k(1)=%r J 之比 = %r ⇒ 整条能级相减在双精度下恒为 0'
          % (OFFSET, KIN * k_cont(1), OFFSET / (KIN * k_cont(1))))

    # ---- 3) 混叠上限：点阵上"往高阶"没有东西可扫 ----
    print('\n[3] 混叠结构：E_{N-n}^FD == E_n^FD 精确成立 ⇒ 互异能级只有约 N/2 条')
    for N in (32, 1024):
        m = max(abs(k_fd(N - n, N) - k_fd(n, N)) / k_fd(n, N) for n in range(1, N // 2))
        top = abs(k_fd(N, N)) / OFFSET
        judge('S3-N%d' % N, 'N=%d：镜像简并 E_{N-n}=E_n 成立（<1e-12）且 n=N 混叠回 n=0' % N,
              m < 1e-12 and top < 1e-15,
              'max |k(N-n)-k(n)|/k(n) = %r；k_FD(n=N)/OFFSET = %r' % (m, top))
        print('  N=%-5d max 镜像失配 = %r   k_FD(n=%d)/OFFSET = %r（应为 0）' % (N, m, N, top))
    nyq = 1.0 - (2.0 / math.pi) ** 2
    print('  n=N/2 处动能被低估 %r（(2/pi)^2 = %r 的剩余比例）⇒  Nyquist 之上的"高阶"是镜像' %
          (nyq, (2.0 / math.pi) ** 2))

    # ---- 4) 要读出 alpha 需要哪一级、哪张网格 ----
    print('\n[4] 把 alpha 放到这条梯子上：所需能级序号与所需网格（这是 C25 的实质结论）')
    nstar = math.sqrt(ALPHA / g1)
    nstar_137 = math.sqrt(ALPHA_137 / g1)
    print('  r_n = n^2 * g1（与几何脱耦）⇒ r_n = alpha 需要 n* = %r（取 1/137 口径则 %r）'
          % (nstar, nstar_137))
    for tol in (0.01, 0.001, 1e-4, 1e-6):
        x, Nneed = n_for_bias(tol, nstar)
        print('  动能误差棒 <= %g：允许 x <= %r ⇒ 需要网格 N >= %r（n* = %r）'
              % (tol, x, Nneed, nstar))
    x, Nneed_1pct = n_for_bias(0.01, nstar)
    judge('S4a', '在自然电子尺度下读出 alpha 所需网格 N >= 1e12（即点阵上不可实现）',
          Nneed_1pct > 1e12, 'tol=1%% 时 N >= %r' % Nneed_1pct)
    # n 与 E_scale 的简并：任意 n 都能被 E_scale 吸收 ⇒ 两未知量一方程（C25 原判据）
    print('  任给能级 n，令 r_n = alpha 所需 E_scale = n^2*KIN/alpha：')
    for n in (1, 2, 5, 10):
        es = n * n * KIN / ALPHA
        print('    n=%-3d E_scale = %r J = %r * 电子静能' % (n, es, es / E_SCALE))
    judge('S4b', 'n 与 E_scale 完全简并（换 n 只换所需的 E_scale，无任何约束剩下）⇒ C25 判定不升级',
          abs((KIN * 1 / (ALPHA / 1)) / (KIN * 4 / ALPHA) - 0.25) < 1e-12,
          'n=1 与 n=2 所需 E_scale 之比 = %r（= 1/4，纯整数因子）' % ((KIN * 1 / ALPHA) / (KIN * 4 / ALPHA)))

    # ---- 汇总 ----
    npass = sum(1 for j in JUDGE if j['verdict'] == 'PASS')
    nfail = len(JUDGE) - npass
    print('\n' + '=' * 78)
    print('判定汇总：PASS %d / FAIL %d（共 %d 条；本脚本不改变 claims.csv 里 C25 的 status）'
          % (npass, nfail, len(JUDGE)))
    for j in JUDGE:
        print('  [%s] %-8s %s' % (j['verdict'], j['id'], j['title']))
    print('  明细：')
    for j in JUDGE:
        print('    %s :: %s' % (j['id'], j['detail']))
    out = {"script": "spiral_c25_alpha_n_scan.py", "judgments": JUDGE,
           "inputs": {"A_m": A_M, "b_m": B_M, "L_m": L, "omega": W, "V0": V0,
                      "E_scale_J": E_SCALE, "OFFSET_J": OFFSET, "KIN_Jm2": KIN,
                      "g1": g1, "N_ref": Nref, "nmax": nmax, "tiers": tiers},
           "n_star_alpha": nstar, "N_needed_1pct": Nneed_1pct,
           "scan_rows": rows}
    face = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'spiral_c25_alpha_n_scan_claims.json')
    with open(face, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print('\n已写出 %s（**钉在脚本自己旁边**，不像 B 段那样落在 CWD：'
          '一份可被引用的版面必须能从文件名找回它）' % face)
    return 1 if (strict and nfail) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
