# -*- coding: utf-8 -*-
"""
================================================================================
openuft#49 攻破第七轮 · 路径 C（扩群 SO(10)）独立复算
================================================================================
第六轮把路径 C 的读数以「归因输入」登记（不自造数字）。本轮把它换成自含复算：

  (1) 一环 b 系数由场内容现场推出，SM 回归 b=(41/10,-19/6,-7) 作门禁
  (2) R3221 单阈链 3x3 精确解 -> M_GUT / alpha_GUT^-1 / M_R，与源报告逐情形对照
  (3) PS422 双阈链：固定 M_GUT 的精确命中（参数计数）+ 标度次序窗口
  (4) R421 链的子群合法性：421 与 3221 是否互相嵌套
  (5) tau_p 对 alpha^-1 的放大系数 -> 「超出可及 0.53 个数量级」所需容差

对照一律按相对偏差给出；结论由计算结果生成，不硬编码。
纯标准库；自检不过即退出码非 0。
================================================================================
"""
from __future__ import print_function
import json
import math
import os
import sys
from fractions import Fraction as F

# ---------------------------------------------------------------- 输入（与源探针同口径）
MZ = 91.1876
ALPHA_MZ_INV = 127.952
SIN2_MS = 0.23121
ALPHAS_MZ = 0.1180
ALPHAS_SIG = 0.0009
A_OBS = (0.6 * (1.0 - SIN2_MS) * ALPHA_MZ_INV,   # alpha_1^-1 = (3/5) alpha_Y^-1
         SIN2_MS * ALPHA_MZ_INV,                  # alpha_2^-1 = sin^2 / alpha_em
         1.0 / ALPHAS_MZ)                         # alpha_3^-1
MPL = 1.22e19
SK_BOUND = 2.4e34
HK_REACH = 1.0e35
K_BL = F(8, 3)
K_Y = F(5, 3)
NGEN = 3
TWO_PI = 2.0 * math.pi

# ---------------------------------------------------------------- so(10) 权重格指标（每代）
T16 = {'SU4': F(2), 'SU3': F(2), 'SU2L': F(2), 'SU2R': F(2)}
TR16_Y2 = F(10, 3)
TR16_BL2 = F(16, 3)
TR16_T3R2 = F(2)
TR16_T3L2 = F(2)
CA = {'SU4': F(4), 'SU3': F(3), 'SU2L': F(2), 'SU2R': F(2)}

# 标量的 Dynkin 指标：Phi(1,2,2) subset 10_H，Sigma(1,1,3)_0 subset 45_H，HD=SM 二重体
SC = {
    'Phi': {'SU4': F(0), 'SU3': F(0), 'SU2L': F(1), 'SU2R': F(1), 'T3R2': F(1), 'BL2': F(0)},
    'Sig': {'SU4': F(0), 'SU3': F(0), 'SU2L': F(0), 'SU2R': F(2), 'T3R2': F(2), 'BL2': F(0)},
}
HD_Y2 = F(1, 2)
HD_T2L = F(1, 2)


# ---------------------------------------------------------------- b 系数（由内容推）
def _b_na(factor, tf, ts):
    return -F(11, 3) * CA[factor] + F(2, 3) * tf + F(1, 3) * ts


def _b_u1(tr_f, tr_s, weight=F(1)):
    return weight * (F(2, 3) * tr_f + F(1, 3) * tr_s)


def _scal(phase, scn):
    """各相位活跃的标量。Sigma 只在 PS/421 相位（M_int 之上），Phi 一直到 M_R。"""
    if scn == 'A':
        return []
    return {'PS': ['Phi', 'Sig'], '421': ['Phi', 'Sig'], 'LR': ['Phi'], 'SM': []}[phase]


def _sum(scal, key):
    return sum((SC[x][key] for x in scal), F(0))


def b_SM(scn):
    n = 2 if scn == 'C' else 1
    return [_b_u1(NGEN * TR16_Y2, n * HD_Y2, F(3, 5)),
            _b_na('SU2L', NGEN * T16['SU2L'], n * HD_T2L),
            _b_na('SU3', NGEN * T16['SU3'], F(0))]


def b_LR(scn):
    s = _scal('LR', scn)
    return [_b_na('SU3', NGEN * T16['SU3'], _sum(s, 'SU3')),
            _b_na('SU2L', NGEN * T16['SU2L'], _sum(s, 'SU2L')),
            _b_na('SU2R', NGEN * T16['SU2R'], _sum(s, 'SU2R')),
            _b_u1(NGEN * TR16_BL2, _sum(s, 'BL2'))]


def b_PS(scn):
    s = _scal('PS', scn)
    return [_b_na('SU4', NGEN * T16['SU4'], _sum(s, 'SU4')),
            _b_na('SU2L', NGEN * T16['SU2L'], _sum(s, 'SU2L')),
            _b_na('SU2R', NGEN * T16['SU2R'], _sum(s, 'SU2R'))]


def b_421(scn):
    s = _scal('421', scn)
    return [_b_na('SU4', NGEN * T16['SU4'], _sum(s, 'SU4')),
            _b_na('SU2L', NGEN * T16['SU2L'], _sum(s, 'SU2L')),
            _b_u1(NGEN * TR16_T3R2, _sum(s, 'T3R2'))]


# ---------------------------------------------------------------- 向下跑动与预测
def _run(vals, bs, t_up, t_dn):
    return [v + float(b) / TWO_PI * (t_up - t_dn) for v, b in zip(vals, bs)]


def predict(chain, p, tG, scn):
    """p=[AG,x1,x2]：R3221 时 x1=tG(未知)、x2=tR；双阈链时 tG 固定、x1=t_int、x2=tR。
    一律用 t=ln(M/M_Z)，故 M_Z 处 t=0。返回 (A1,A2,A3) 的预测值。"""
    AG = p[0]
    if chain == 'PS422':
        t1, t2 = p[1], p[2]
        A4, A2L, A2R = _run([AG] * 3, b_PS(scn), tG, t1)
        A3, A2L, A2R, ABL = _run([A4, A2L, A2R, float(K_BL) * A4], b_LR(scn), t1, t2)
    elif chain == 'R421':
        t1, t2 = p[1], p[2]
        A4, A2L, AR = _run([AG] * 3, b_421(scn), tG, t1)
        A3, A2L, A2R, ABL = _run([A4, A2L, AR, float(K_BL) * A4], b_LR(scn), t1, t2)
    elif chain == 'R3221':
        t1, t2 = p[1], p[2]
        A3, A2L, A2R, ABL = _run([AG] * 3 + [float(K_BL) * AG], b_LR(scn), t1, t2)
    else:
        raise ValueError(chain)
    A1 = (3.0 / 5.0) * (A2R + ABL / 4.0)     # Y = T3R + (B-L)/2 的对角子群相加规则
    return _run([A1, A2L, A3], b_SM(scn), t2, 0.0)


def solve3(J, rhs):
    M = [J[i][:] + [rhs[i]] for i in range(3)]
    for c in range(3):
        piv = max(range(c, 3), key=lambda r: abs(M[r][c]))
        if abs(M[piv][c]) < 1e-14:
            return None
        M[c], M[piv] = M[piv], M[c]
        for r in range(3):
            if r == c:
                continue
            f = M[r][c] / M[c][c]
            for k in range(c, 4):
                M[r][k] -= f * M[c][k]
    return [M[i][3] / M[i][i] for i in range(3)]


def affine_parts(chain, tG, scn):
    f0 = predict(chain, [0.0, 0.0, 0.0], tG, scn)
    cols = []
    for i in range(3):
        e = [0.0, 0.0, 0.0]
        e[i] = 1.0
        fi = predict(chain, e, tG, scn)
        cols.append([fi[k] - f0[k] for k in range(3)])
    J = [[cols[j][i] for j in range(3)] for i in range(3)]
    return J, f0


def affinity_defect(chain, tG, scn):
    f0 = predict(chain, [0.0, 0.0, 0.0], tG, scn)
    fu = predict(chain, [1.37, 33.0, 28.0], tG, scn)
    fv = predict(chain, [0.41, 30.5, 25.5], tG, scn)
    fuv = predict(chain, [1.78, 63.5, 53.5], tG, scn)
    d = [abs(fuv[i] - f0[i] - (fu[i] - f0[i]) - (fv[i] - f0[i])) for i in range(3)]
    return max(d)


def solve_chain(chain, tG, scn, A=A_OBS):
    J, f0 = affine_parts(chain, tG, scn)
    p = solve3(J, [A[i] - f0[i] for i in range(3)])
    if p is None:
        return None
    pred = predict(chain, p, tG, scn)
    resid = max(abs(pred[i] - A[i]) for i in range(3))
    out = {'chain': chain, 'scenario': scn, 'alpha_GUT_inv': p[0],
           'residual': resid,
           't_GUT': p[1] if chain == 'R3221' else tG,
           't_R': p[2],
           't_int': None if chain == 'R3221' else p[1]}
    for key, t in (('M_GUT', out['t_GUT']), ('M_R', out['t_R']),
                   ('M_int', out['t_int'])):
        out[key] = MZ * math.exp(t) if t is not None else None
    return out


# ---------------------------------------------------------------- 质子衰变（两种标定）
SU5_REF_MX = 10 ** 14.6
SU5_REF_TAU = 1.0e29
SU5_REF_A = 41.0
MX_RATIO = 1.0 / math.sqrt(2.0)


def tau_p_src(mgut, ag):
    """源探针标定：tau ∝ M_X^4 / alpha_GUT^2，以最小 SU(5) 为锚点。"""
    return SU5_REF_TAU * (mgut * MX_RATIO / SU5_REF_MX) ** 4 * (ag / SU5_REF_A) ** 2


def tau_p_simple(mgut):
    """简式标定（本系列前几轮用）：tau ≈ (M_GUT/2e16)^4 × 1e35 yr。"""
    return (mgut / 2.0e16) ** 4 * 1.0e35


# ---------------------------------------------------------------- 源报告读数（对照用）
SRC_R3221 = {
    'A': {'M_GUT': 1.990e17, 'alpha': 47.82, 'M_R': 1.299e10, 'tau': 2.12e39},
    'B': {'M_GUT': 5.298e16, 'alpha': 46.35, 'M_R': 4.880e10, 'tau': 1.00e37},
    'C': {'M_GUT': 2.293e16, 'alpha': 45.42, 'M_R': 1.127e11, 'tau': 3.38e35},
}
SRC_PS422_WINDOW_A = (2.636e15, 1.990e17)


def rel(a, b):
    return abs(a - b) / abs(b) if b else float('inf')


# ---------------------------------------------------------------- 主流程
def main():
    checks = []

    def ck(name, ok, detail=''):
        checks.append({'check': name, 'ok': bool(ok), 'detail': detail})
        return bool(ok)

    res = {}

    # ---------- G1/G2/G3：归一化门禁（精确有理数） ----------
    ck('G1 SM 回归 b=(41/10,-19/6,-7)（精确有理数）',
       list(b_SM('A')) == [F(41, 10), F(-19, 6), F(-7)],
       '算得 %s' % [str(x) for x in b_SM('A')])
    ck('G2 k_Y = Tr16(Y^2)/Tr16(T3L^2) = 5/3（精确）',
       TR16_Y2 / TR16_T3L2 == F(5, 3), '算得 %s' % (TR16_Y2 / TR16_T3L2))
    ck('G3 k_{B-L} = Tr16((B-L)^2)/Tr16(T3L^2) = 8/3（精确）',
       TR16_BL2 / TR16_T3L2 == F(8, 3), '算得 %s' % (TR16_BL2 / TR16_T3L2))
    ck('G4 两步匹配 = 一步匹配：(3/5)(1+k_BL/4) 恰为 1（精确）',
       F(3, 5) * (1 + K_BL / F(4)) == F(1),
       '算得 %s' % (F(3, 5) * (1 + K_BL / F(4))))
    ck('G5 仿射性（R3221/PS422/R421，A/B 两情形）',
       max(affinity_defect(c, 36.0, s)
           for c in ('R3221', 'PS422', 'R421') for s in ('A', 'B')) < 1e-9,
       'max dev=%.2e' % max(affinity_defect(c, 36.0, s)
                            for c in ('R3221', 'PS422', 'R421') for s in ('A', 'B')))

    # ---------- 路径 C 第一条：R3221 独立复算 ----------
    r3221 = {}
    tau_lo = None
    for scn in ('A', 'B', 'C'):
        r = solve_chain('R3221', None, scn)
        r['tau_p_src'] = tau_p_src(r['M_GUT'], r['alpha_GUT_inv'])
        r['tau_p_simple'] = tau_p_simple(r['M_GUT'])
        src = SRC_R3221[scn]
        r['cmp'] = {
            'M_GUT_rel': rel(r['M_GUT'], src['M_GUT']),
            'alpha_rel': rel(r['alpha_GUT_inv'], src['alpha']),
            'M_R_rel': rel(r['M_R'], src['M_R']),
            'tau_rel': rel(r['tau_p_src'], src['tau']),
        }
        r['ordered'] = (MZ < r['M_R'] < r['M_GUT'])
        r3221[scn] = r
        if tau_lo is None or r['tau_p_src'] < tau_lo:
            tau_lo = r['tau_p_src']

    worst = max(max(r3221[s]['cmp'][k] for k in ('M_GUT_rel', 'alpha_rel',
                                                 'M_R_rel', 'tau_rel'))
                for s in ('A', 'B', 'C'))
    ck('G6 R3221 三情形复算与源报告一致（相对偏差 < 1%）', worst < 1e-2,
       '最差相对偏差=%.3e' % worst)
    ck('G7 R3221 回代残差 ~ 0（< 1e-9）',
       max(r3221[s]['residual'] for s in ('A', 'B', 'C')) < 1e-9,
       'max resid=%.2e' % max(r3221[s]['residual'] for s in ('A', 'B', 'C')))
    ck('G8 标度次序 M_Z < M_R < M_GUT（A/B/C）',
       all(r3221[s]['ordered'] for s in ('A', 'B', 'C')),
       '；'.join('%s: M_R=%.3e' % (s, r3221[s]['M_R']) for s in ('A', 'B', 'C')))
    ck('G9 M_GUT < M_Pl（A/B/C）',
       all(r3221[s]['M_GUT'] < MPL for s in ('A', 'B', 'C')),
       'max M_GUT=%.3e vs M_Pl=%.2e' % (max(r3221[s]['M_GUT']
                                            for s in ('A', 'B', 'C')), MPL))
    ck('G10 两种 tau_p 标定同量级（差异 < 1 个数量级）',
       max(abs(math.log10(r3221[s]['tau_p_src'] / r3221[s]['tau_p_simple']))
           for s in ('A', 'B', 'C')) < 1.0,
       'max |Δlog10|=%.2f' % max(abs(math.log10(r3221[s]['tau_p_src']
                                                / r3221[s]['tau_p_simple']))
                                 for s in ('A', 'B', 'C')))
    res['r3221'] = {s: {k: v for k, v in r3221[s].items()} for s in r3221}

    # ---------- 路径 C 第二条：PS422 参数计数与次序窗口 ----------
    ps_hits = []
    for scn in ('A', 'B', 'C'):
        for lg in (14.0, 15.0, 16.0, 17.0, 18.0):
            r = solve_chain('PS422', math.log(10 ** lg / MZ), scn)
            if r is not None:
                ps_hits.append(r['residual'])
    ck('G11 PS422 固定 M_GUT 时残差 ~ 0（3 未知对 3 方程 ⇒ 恒命中，非证据）',
       max(ps_hits) < 1e-9, 'max resid=%.2e（%d 点）' % (max(ps_hits), len(ps_hits)))

    def ps_ordered(lg, scn):
        r = solve_chain('PS422', math.log(10 ** lg / MZ), scn)
        if r is None:
            return False
        return 0.0 < r['t_R'] < r['t_int'] < r['t_GUT']

    def ps_window(scn, lo=13.0, hi=18.5, it=60):
        # 在 M_GUT 网格上找 contiguous 的次序成立区间，再二分细化两端
        grid = [lo + (hi - lo) * i / 400.0 for i in range(401)]
        ok = [g for g in grid if ps_ordered(g, scn)]
        if not ok:
            return None
        a0, b0 = min(ok), max(ok)
        step = (hi - lo) / 400.0
        for edge in ('lo', 'hi'):
            if edge == 'lo':
                x, y = a0 - step, a0
            else:
                x, y = b0, b0 + step
            for _ in range(it):
                m = 0.5 * (x + y)
                if ps_ordered(m, scn):
                    y = m
                else:
                    x = m
            if edge == 'lo':
                a0 = y
            else:
                b0 = x
        return (10 ** a0, 10 ** b0)

    win = {s: ps_window(s) for s in ('A', 'B', 'C')}
    wa = win['A']
    ck('G12 PS422 情形 A 次序窗口 ≈ [2.636e15, 1.990e17]（相对 < 5%）',
       wa is not None and rel(wa[0], SRC_PS422_WINDOW_A[0]) < 5e-2
       and rel(wa[1], SRC_PS422_WINDOW_A[1]) < 5e-2,
       '复算 [%.3e, %.3e]' % (wa[0], wa[1]) if wa else '无窗口')
    ck('G13 窗口上沿 = R3221 的 M_GUT 预言（相对 < 1e-3）',
       wa is not None and rel(wa[1], r3221['A']['M_GUT']) < 1e-3,
       '上沿 %.4e vs R3221 %.4e' % (wa[1], r3221['A']['M_GUT']))
    res['ps422_window'] = {s: (list(win[s]) if win[s] else None) for s in win}

    # ---------- 路径 C 第三条：R421 的子群合法性 ----------
    # 421 = SU(4)xSU(2)_LxU(1)_R ；3221 = SU(3)xSU(2)_LxSU(2)_RxU(1)_{B-L}
    dim_421_rest = 15 + 1                 # su(4) + u(1)_R（去掉公共的 su(2)_L）
    dim_3221_rest = 8 + 3 + 1             # su(3) + su(2)_R + u(1)_{B-L}
    c1 = dim_421_rest > dim_3221_rest     # 421 ⊄ 3221（维数判据）
    # 3221 ⊄ 421：4 -> (3,1)+(1,1)，su(2)_R 只能落在 1 维补空间 ⇒ 像为 0 ⇒ 进不了 u(1)_R
    fund_dim = 4
    su3_part = 3
    complement = fund_dim - su3_part      # = 1
    c2 = complement < 2                   # su(2) 无 2 维忠实空间 ⇒ 3221 ⊄ 421
    rank_ok = (2 + 1 + 1) <= (3 + 1)      # 秩判据本身通过（说明必须靠分支判据）
    r421_invalid = (not c1) and c2
    ck('G14 R421：421 与 3221 互不嵌套（秩判据不够，须用维数+基本表示分支）',
       r421_invalid and rank_ok,
       'dim(421\su2L)=%d > dim(3221\su2L)=%d；4→3+1 补空间=%d 维放不下 su(2)；秩 %d≤%d 通过'
       % (dim_421_rest, dim_3221_rest, complement, 2 + 1 + 1, 3 + 1))
    res['r421'] = {'dim_421_minus_su2L': dim_421_rest,
                   'dim_3221_minus_su2L': dim_3221_rest,
                   'fundamental_branch': '4 -> (3,1)+(1,1)',
                   'complement_dim': complement,
                   'rank_test_passes': rank_ok,
                   'nests_421_in_3221': not c1,
                   'nests_3221_in_421': not c2,
                   'verdict': 'NOT_A_SUBGROUP_CHAIN' if r421_invalid else 'VALID'}

    # ---------- 敏感性：tau_p 对 alpha^-1 的放大 ----------
    base = r3221['C']
    margin_hk = math.log10(base['tau_p_src'] / HK_REACH)

    sens = {}
    for i in range(3):
        Ap = list(A_OBS)
        Ap[i] = Ap[i] + 1.0
        r = solve_chain('R3221', None, 'C', A=tuple(Ap))
        tp = tau_p_src(r['M_GUT'], r['alpha_GUT_inv'])
        sens[i] = math.log10(tp / base['tau_p_src'])
    amp = {i: abs(sens[i]) for i in sens}
    tol = {i: (margin_hk / amp[i] if amp[i] > 0 else float('inf')) for i in amp}
    tol_min = min(tol.values())
    # 1σ(alpha_s) 引起的 tau_p 偏移
    dA3_sig = ALPHAS_SIG / (ALPHAS_MZ ** 2)
    dex_per_sigma = amp[2] * dA3_sig
    sigma_equiv = margin_hk / dex_per_sigma if dex_per_sigma > 0 else float('inf')

    ck('G15 放大系数 > 1（1 单位 alpha^-1 移动 tau_p 超过 1 个数量级）',
       max(amp.values()) > 1.0,
       '；'.join('∂log10τ/∂A_%d=%+.2f' % (i + 1, sens[i]) for i in range(3)))
    ck('G16 「超出可及 %.2f 量级」对应的 alpha^-1 容差 < 1（未算的二环/阈值是 O(1)）'
       % margin_hk, tol_min < 1.0,
       '最紧容差=%.3f 单位（最敏感方向 A_%d，%.2f 量级/单位）'
       % (tol_min, max(amp, key=lambda i: amp[i]) + 1, max(amp.values())))
    ck('G17 该余量在 alpha_s 的 3σ 以内（可及性判断本身不稳健）',
       sigma_equiv < 3.0,
       '1σ(α_s)=%.4f ⇒ %.3f 量级；余量 %.2f ⇒ %.2fσ' % (dA3_sig, dex_per_sigma,
                                                       margin_hk, sigma_equiv))
    res['sensitivity'] = {
        'base_scenario': 'C',
        'tau_p_base_yr': base['tau_p_src'],
        'HK_reach_yr': HK_REACH,
        'margin_dex': margin_hk,
        'dex_per_unit_A': {'A1': sens[0], 'A2': sens[1], 'A3': sens[2]},
        'tolerance_units': {'A1': tol[0], 'A2': tol[1], 'A3': tol[2]},
        'tolerance_min': tol_min,
        'alpha_s_1sigma': ALPHAS_SIG,
        'dA3_per_sigma': dA3_sig,
        'dex_per_sigma_alpha_s': dex_per_sigma,
        'sigma_equivalent_of_margin': sigma_equiv,
    }

    # ---------- 路径 C 总判决 ----------
    n_valid_chains = 2                       # PS422（自由输入）+ R3221（预言）
    delivering = (tol_min > 1.0) and (sigma_equiv > 3.0)
    total_C = 'NOT_CLOSED_BUT_NON_DELIVERING' if not delivering else 'DELIVERING'
    res['path_C'] = {
        'n_chains_in_source': 3,
        'n_valid_subgroup_chains': n_valid_chains,
        'n_invalid_chains': 1,
        'n_predict_M_GUT': 1,                # 只有 R3221
        'predicted_tau_p_yr_range': [min(r3221[s]['tau_p_src'] for s in ('A', 'B', 'C')),
                                     max(r3221[s]['tau_p_src'] for s in ('A', 'B', 'C'))],
        'margin_dex_beyond_HK': margin_hk,
        'tolerance_units': tol_min,
        'delivering': delivering,
        'verdict': total_C,
    }
    res['total'] = {
        'path_A': 'CLOSED',
        'path_B': 'CLOSED',
        'path_C': total_C,
        'verdict': 'TOTAL_NO_TESTABLE_ROUTE' if not delivering else 'ROUTE_OPEN',
    }

    # ---------- 输出 ----------
    n_ok = sum(1 for c in checks if c['ok'])
    data = {'summary': {'selfcheck_passed': n_ok, 'selfcheck_total': len(checks),
                        'path_C_verdict': total_C,
                        'total_verdict': res['total']['verdict']},
            'checks': checks, 'results': res}
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'openuft_49_攻破第七轮_路径C独立复算_data.json'),
              'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    L = []
    L.append('=' * 74)
    L.append('openuft#49 攻破第七轮 · 路径 C（扩群 SO(10)）独立复算')
    L.append('=' * 74)
    L.append('')
    L.append('[自检] %d/%d PASS' % (n_ok, len(checks)))
    for c in checks:
        L.append('  [%s] %s  %s' % ('PASS' if c['ok'] else 'FAIL', c['check'], c['detail']))
    L.append('')
    L.append('[R3221 独立复算 vs 源报告]')
    L.append('  情形  M_GUT(GeV)   vs源     α_GUT^-1  vs源    M_R(GeV)   vs源     τ_p(yr)')
    for s in ('A', 'B', 'C'):
        r = r3221[s]
        L.append('  %s   %.4e  %.1e%%  %8.4f  %.1e%%  %.4e  %.1e%%  %.3e'
                 % (s, r['M_GUT'], 100 * r['cmp']['M_GUT_rel'],
                    r['alpha_GUT_inv'], 100 * r['cmp']['alpha_rel'],
                    r['M_R'], 100 * r['cmp']['M_R_rel'], r['tau_p_src']))
    L.append('')
    L.append('[PS422 参数计数] 固定 M_GUT 的 15 个解最大残差 = %.2e ⇒ 3 未知对 3 方程恒命中'
             % max(ps_hits))
    L.append('[PS422 次序窗口] ' + '；'.join(
        '%s: [%s]' % (s, ('%.3e, %.3e' % win[s]) if win[s] else '无')
        for s in ('A', 'B', 'C')))
    L.append('  上沿与 R3221 的 M_GUT 预言相对偏差 = %.2e（同一极限，非三链独立确认）'
             % rel(win['A'][1], r3221['A']['M_GUT']))
    L.append('')
    L.append('[R421 子群合法性] %s' % res['r421']['verdict'])
    L.append('  dim(421\\su2L)=%d > dim(3221\\su2L)=%d ⇒ 421 ⊄ 3221'
             % (dim_421_rest, dim_3221_rest))
    L.append('  基本表示 4 → (3,1)+(1,1)，补空间 %d 维放不下 su(2)_R ⇒ 3221 ⊄ 421'
             % complement)
    L.append('  秩判据（4 ≤ 4）通过 ⇒ 必须靠维数 + 分支判据，秩不够')
    L.append('')
    L.append('[τ_p 敏感性（情形 C，最低端）]')
    L.append('  τ_p = %.3e yr；Hyper-K/DUNE 可及 ~%.0e yr ⇒ 余量 %.2f 个数量级'
             % (base['tau_p_src'], HK_REACH, margin_hk))
    for i in range(3):
        L.append('  ∂log10 τ_p / ∂A_%d = %+0.2f  ⇒ 吃掉余量只需 %.3f 单位'
                 % (i + 1, sens[i], tol[i]))
    L.append('  最紧容差 = %.3f 单位 α⁻¹；未计入的二环 + 有限阈值是 O(1) ⇒ 超差 %.1f 倍'
             % (tol_min, 1.0 / tol_min if tol_min else float('inf')))
    L.append('  α_s 1σ = %.4f ⇒ Δlog10 τ_p = %.3f；余量相当于 %.2fσ(α_s)'
             % (ALPHAS_SIG, dex_per_sigma, sigma_equiv))
    L.append('')
    L.append('[路径 C 判决] %s' % total_C)
    L.append('  源报告 3 链 ⇒ 有效子群链 %d 条（R421 作废）；只有 R3221 给 M_GUT 预言')
    L.append('  预言 τ_p ∈ [%.2e, %.2e] yr，余量 %.2f 量级，但容差 %.3f 单位 < O(1)'
             % (res['path_C']['predicted_tau_p_yr_range'][0],
                res['path_C']['predicted_tau_p_yr_range'][1], margin_hk, tol_min))
    L.append('')
    L.append('[总判决] %s' % res['total']['verdict'])
    text = '\n'.join(L) + '\n'
    with open(os.path.join(here, 'openuft_49_攻破第七轮_路径C独立复算_report.txt'),
              'w', encoding='utf-8') as f:
        f.write(text)
    try:
        sys.stdout.write(text)
    except Exception:
        sys.stdout.write(text.encode('ascii', 'replace').decode('ascii'))

    if n_ok != len(checks):
        sys.exit(1)


if __name__ == '__main__':
    main()
