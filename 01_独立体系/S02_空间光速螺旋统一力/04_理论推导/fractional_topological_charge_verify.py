# -*- coding: utf-8 -*-
"""S02 §16.11 半整数拓扑荷 l 的拓展：单值性 / 自旋表示 / 无源 Maxwell 判据。

开放项③：半整数拓扑荷 l 的拓展（非标准 LG 模式，超出本 S02 整数 l 范围）。

本脚本给出**排除**的严格判据并数值验证：

  V1 单值性残差 R(l) = |exp(i*2*pi*l) - 1| = 2*|sin(pi*l)|：
     整数 l -> 0；半整数 l -> 2（场在 phi->phi+2pi 反号，多值）
  V2 自旋表示兼容性：总 2pi 变换因子 = exp(i*2*pi*l) * spin_2pi。
     Maxwell 矢量场自旋 1 -> spin_2pi=+1 => 仅整数 l 单值；
     旋量自旋 1/2 -> spin_2pi=-1 => 半整数 l 可单值，但那是旋量场，非本框架
  V3 分支切割方案的不连续幅度 |1 - exp(i*2*pi*(l - floor(l)))|：
     整数 l -> 0（场在切割处连续）；半整数 l -> 2（场在切割处完全反号/不连续）
  V4 无源 Maxwell 的"伪源"检验：对尝试解 E = exp(i*l*phi)*f(rho)，在 phi 跨越
     2pi 不连续时，partial_phi E 含跳跃项 => nabla·E / nabla×B 在切割处出现
     等效线源（delta 弦）。整数 l 无此伪源；半整数 l 的跨切割差分比发散。

纯标准库（math + cmath）。
"""
import io
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

OUT = {}
CHECKS = []


def rec(name, ok, detail):
    CHECKS.append({'check': name, 'pass': bool(ok), 'detail': str(detail)})
    return bool(ok)


# ---------------- V1：单值性残差 ----------------
def v1():
    rows = []
    ok = True
    ls = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
    for l in ls:
        import cmath
        r = abs(cmath.exp(1j * 2.0 * math.pi * l) - 1.0)
        closed = abs(r) < 1e-12
        half = abs(r - 2.0) < 1e-12
        rows.append({'l': l, 'single_valued_residual': r,
                     'integer_l_single_valued': bool(closed),
                     'half_integer_l_anti_valued': bool(half)})
        # 判据：非整数 l 必须 ~2（反号），整数 l 必须 ~0
        if abs(l - round(l)) < 1e-9:
            ok = ok and closed
        else:
            ok = ok and half
    OUT['v1_single_valued'] = rows
    rec('V1_single_valued_residual', ok,
        'integer l -> 0, half-integer l -> 2 (machine)')
    return ok


# ---------------- V2：自旋表示兼容性 ----------------
def spin_two_pi(spin):
    """绕 z 旋转 2pi 的因子 = exp(-i*2pi*spin)。自旋1 -> +1；自旋1/2 -> -1。"""
    import cmath
    return cmath.exp(-1j * 2.0 * math.pi * spin)


def v2():
    rows = []
    ok = True
    import cmath
    for l in (0.0, 1.0, 0.5, 1.5):
        for spin, nm in ((1.0, 'Maxwell_vector_s1'), (0.5, 'spinor_s1_2')):
            total = cmath.exp(1j * 2.0 * math.pi * l) * spin_two_pi(spin)
            single = abs(total - 1.0) < 1e-12
            total_abs = abs(total)
            rows.append({'l': l, 'spin': spin, 'field': nm,
                         'net_2pi_factor_real': total.real, 'net_2pi_factor_imag': total.imag,
                         'single_valued': bool(single)})
            # Maxwell 矢量场（+1）要求整数 l；旋量（-1）允许半整数 l 但非本框架
            if spin == 1.0:
                ok = ok and (abs(l - round(l)) < 1e-9) == single
    OUT['v2_spin_representation'] = rows
    rec('V2_spin1_requires_integer_l', ok,
        'spin-1 net factor=exp(i2pi l): only integer l gives +1; spin-1/2 gives -1 (off-framework)')
    return ok


# ---------------- V3：分支切割不连续幅度 ----------------
def v3():
    rows = []
    ok = True
    for l in (-1.5, -0.5, 0.5, 1.5, 0.0, 1.0):
        import cmath
        frac = l - math.floor(l)
        gap = abs(1.0 - cmath.exp(1j * 2.0 * math.pi * frac))
        is_int = abs(l - round(l)) < 1e-9
        rows.append({'l': l, 'fractional_part': frac, 'discontinuity_magnitude': gap,
                     'branch_cut_continuous': bool(abs(gap) < 1e-12)})
        ok = ok and (is_int == (abs(gap) < 1e-12))
    OUT['v3_branch_cut'] = rows
    rec('V3_branch_cut_discontinuity', ok,
        'integer l -> cut continuous (gap 0); half-integer l -> cut anti-valued (gap 2)')
    return ok


# ---------------- V4：无源 Maxwell 伪源检验 ----------------
def v4():
    """跨 phi=0/2pi 切割的差分比：半整数 l 的尝试解在切割处不连续，
    导致 partial_phi E 出现跳跃尖峰（等效线源）；整数 l 无。

    用有限差分：在 phi 网格上取 E(phi)=exp(i*l*phi)，计算跨整圈的差分
    dE = E(phi+2pi) - E(phi) （即不连续性），并比对网格内相邻差分 dE_grid。
    半整数 l：dE/dE_grid ~ 2/（网格步长量级）-> 随网格加密而相对放大。
    """
    rows = []
    ok = True
    import cmath
    for l in (1.0, 1.5):
        for n in (360, 3600, 36000):
            dphi = 2.0 * math.pi / n
            # 网格内相邻差分（正则部分）
            e_a = cmath.exp(1j * l * dphi)
            e_b = 1.0
            grid_step = abs(e_a - e_b)  # |E(dphi)-E(0)|
            # 跨整圈不连续
            wrap = abs(cmath.exp(1j * l * 2.0 * math.pi) - 1.0)
            # 比值：正则网格步长按 l*dphi 缩放；跨圈不连续对整数 l=0、半整数 l=2
            ratio = wrap / (grid_step + 1e-300)
            # 归一化（乘 dphi）：半整数 l 应为 wrap/l 常数（与 n 无关），整数 l 为 0
            normalized = ratio * dphi
            is_int = abs(l - round(l)) < 1e-9
            rows.append({'l': l, 'n_grid': n, 'grid_step': grid_step,
                         'wrap_discontinuity': wrap, 'ratio': ratio,
                         'normalized_ratio': normalized, 'integer_l': bool(is_int)})
            # 整数 l：wrap=0，normalized=0；半整数 l：normalized≈wrap/l=2/l（与 n 无关）
            if is_int:
                ok = ok and wrap < 1e-12 and normalized < 1e-9
            else:
                ok = ok and wrap > 1.9 and abs(normalized - 2.0 / l) < 1e-3
    OUT['v4_pseudosource'] = rows
    rec('V4_half_integer_maxwell_pseudosource', ok,
        'integer l: wrap=0 (no source); half-integer l: wrap=2, normalized=2/l const (delta-string source)')
    return ok


def main():
    r = [v1(), v2(), v3(), v4()]
    n_pass = sum(1 for c in CHECKS if c['pass'])
    OUT['summary'] = {'checks': len(CHECKS), 'pass': n_pass,
                      'fail': len(CHECKS) - n_pass, 'verified': n_pass == len(CHECKS)}
    here = os.path.dirname(os.path.abspath(__file__))
    with io.open(os.path.join(here, '§16_半整数拓扑荷排除数据.json'), 'w',
                 encoding='utf-8', newline='\n') as fh:
        json.dump(OUT, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    for c in CHECKS:
        print('%-44s %s  %s' % (c['check'], 'PASS' if c['pass'] else 'FAIL', c['detail']))
    print('checks: %d  pass: %d  fail: %d  verified=%s'
          % (len(CHECKS), n_pass, len(CHECKS) - n_pass, n_pass == len(CHECKS)))
    return 0 if n_pass == len(CHECKS) else 1


if __name__ == '__main__':
    sys.exit(main())
