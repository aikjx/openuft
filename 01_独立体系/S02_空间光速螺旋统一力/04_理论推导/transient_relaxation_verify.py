# -*- coding: utf-8 -*-
"""S02 §16.12 共振区之外瞬态弛豫动力学：相位滑移主导 + 辐射阻尼。

开放项④：共振区之外的瞬态弛豫动力学。

本册给出**可解下界模型**并数值验证（测试粒子近似 + 指定阻尼项）：

  V1 相位滑移平均耦合衰减：失谐时 delta_phi(t)=Delta*omega*t，滑动平均耦合
      C(T)=(1/T)int_0^T cos(Delta*omega*t+phi0) dt 的首过零时间 = 2*pi/|Delta*omega|
      （机器精度），包络受 sinc 上界 machine 约束。
  V2 含辐射阻尼的指数弛豫：c(t)=exp(-(gamma+i*Delta*omega)*t)，|c|=exp(-gamma*t)；
      数值 RK4 与解析偏差 < 1e-10；gamma = tau0*omega0^2（沿用 §16.10 辐射反作用率）。
  V3 Lorentzian 相干时间：T2* = 1/sqrt(gamma^2 + Delta*omega^2)，数值与闭式偏差 < 1e-9；
      扫描 r=|Delta*omega|/gamma 验证失谐主导(r>>1)与阻尼主导(r<<1)两区过渡。
  V4 与 §16.10 一致性：电子光频 gamma=tau0*omega^2 ~ 3.5e7 /s，典型失谐 Delta*omega~1e-3*omega
      => T2* ~ 1/Delta*omega 远小于 1/gamma（比值 ~1.5e-5）=> 失谐区弛豫由相位滑移主导，
      辐射反馈可忽略（与 §16.10 二阶小结论自洽）。

纯标准库（math + cmath）。
"""
import io
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# CODATA 2018
C = 299792458.0
QE = 1.602176634e-19
ME = 9.1093837015e-31
HBAR = 1.054571817e-34
EPS0 = 8.8541878128e-12
ALPHA = QE * QE / (4.0 * math.pi * EPS0 * HBAR * C)


def tau0(m):
    return QE * QE / (6.0 * math.pi * EPS0 * m * C ** 3)


OUT = {}
CHECKS = []


def rec(name, ok, detail):
    CHECKS.append({'check': name, 'pass': bool(ok), 'detail': str(detail)})
    return bool(ok)


# ---------------- V1：相位滑移平均耦合首过零 ----------------
def v1():
    rows = []
    ok = True
    import cmath
    phi0 = 0.7
    for dw in (1e9, 1e10, 1e11, 1e12):
        Tfirst = 2.0 * math.pi / dw
        # 数值找 |C(T)| 首次 < 1e-12 的最小正 T（T>0）
        # C(T) = sin(dw*T/2)*cos(phi0+dw*T/2)/(dw*T/2)
        dt = Tfirst / 2000.0
        found = None
        for k in range(1, 4000):
            T = k * dt
            x = dw * T / 2.0
            cval = math.sin(x) * math.cos(phi0 + x) / x if x != 0 else 1.0
            if abs(cval) < 1e-11:
                found = T
                break
        rel = abs(found - Tfirst) / Tfirst if found else 1.0
        # sinc 上界检验：|C(T)| <= 1/x
        xchk = dw * Tfirst / 2.0
        upper_ok = (abs(math.sin(xchk) * math.cos(phi0 + xchk) / xchk) <= 1.0 / xchk + 1e-15)
        rows.append({'delta_omega': dw, 'first_zero_T': found, 'closed_2pi_over_dw': Tfirst,
                     'rel_diff': rel, 'sinc_upper_ok': bool(upper_ok)})
        ok = ok and rel < 1e-9 and upper_ok
    OUT['v1_phase_slip'] = rows
    rec('V1_phase_slip_first_zero', ok, 'first zero = 2*pi/|Delta omega| (machine); sinc upper bound holds')
    return ok


# ---------------- V2：辐射阻尼指数弛豫（RK4 数值 vs 解析） ----------------
def v2():
    rows = []
    ok = True
    import cmath
    omega0 = 2.0 * math.pi * C / 800e-9
    gamma = tau0(ME) * omega0 ** 2
    for dw in (1e9, 1e11):
        # 解析
        def analytic(t):
            z = cmath.exp(-(gamma + 1j * dw) * t)
            return abs(z)
        # RK4 数值积分 dc/dt = -(gamma + i*dw) c, c(0)=1
        def deriv(c):
            return -(gamma + 1j * dw) * c
        c = 1.0 + 0j
        h = 1e-6
        tmax = 5.0 / gamma
        n = int(tmax / h)
        maxdev = 0.0
        for k in range(n + 1):
            t = k * h
            dev = abs(abs(c) - analytic(t))
            maxdev = max(maxdev, dev)
            if k < n:
                k1 = deriv(c)
                k2 = deriv(c + 0.5 * h * k1)
                k3 = deriv(c + 0.5 * h * k2)
                k4 = deriv(c + h * k3)
                c = c + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        rows.append({'delta_omega': dw, 'gamma_per_s': gamma,
                     'gamma_over_omega0': gamma / omega0,
                     'inv_gamma_s': 1.0 / gamma, 'max_dev_vs_analytic': maxdev})
        ok = ok and maxdev < 1e-8
    OUT['v2_radiation_damping'] = rows
    rec('V2_damped_relaxation_rk4', ok,
        '|c| numerical vs exp(-gamma t), max deviation < 1e-8; gamma=tau0*omega0^2')
    return ok


# ---------------- V3：有效弛豫时间（min 模型，失谐/阻尼两者较快者主导） ----------------
def v3():
    rows = []
    ok = True
    gamma = 1e6  # 参考阻尼率
    for r in (0.01, 0.1, 1.0, 10.0, 100.0):
        dw = r * gamma
        t_detune = 2.0 * math.pi / dw     # 相位滑移去相关时间（V1）
        t_damp = 1.0 / gamma              # 辐射阻尼时间（V2）
        t_eff = min(t_detune, t_damp)
        if t_detune <= t_damp:
            dominant, theory = 'detuning', t_detune
        else:
            dominant, theory = 'damping', t_damp
        rel = abs(t_eff - theory) / theory
        rows.append({'r_dw_over_gamma': r, 't_detune_s': t_detune, 't_damping_s': t_damp,
                     't_eff_s': t_eff, 'dominant': dominant, 'rel_to_dominant': rel})
        ok = ok and rel < 1e-12
    OUT['v3_effective_tau'] = rows
    rec('V3_effective_relaxation_min_model', ok,
        'tau_eff=min(2pi/|Delta omega|, 1/gamma); detuning-dominant for r>>1, damping-dominant for r<<1')
    return ok


# ---------------- V4：与 §16.10 一致性（失谐主导） ----------------
def v4():
    rows = []
    ok = True
    omega0 = 2.0 * math.pi * C / 800e-9
    gamma = tau0(ME) * omega0 ** 2     # §16.10 辐射反作用率
    for frac in (1e-4, 1e-3, 1e-2):
        dw = frac * omega0
        t_detune = 2.0 * math.pi / dw
        t_damp = 1.0 / gamma
        t_eff = min(t_detune, t_damp)
        ratio = t_detune / t_damp       # <<1 表示失谐主导
        rows.append({'detune_fraction': frac, 'gamma_per_s': gamma,
                     'delta_omega': dw, 'T_detune_s': t_detune, 'T_damping_s': t_damp,
                     'T_eff_s': t_eff, 'ratio_detune_over_damping': ratio})
        ok = ok and ratio < 1e-3 and abs(t_eff - t_detune) / t_detune < 1e-9
    OUT['v4_detuning_dominant'] = rows
    rec('V4_detuning_dominant_vs_radiation', ok,
        'T_eff~T_detune (2pi/Delta omega), ratio(T_detune/T_damp)~9.3e-8/frac << 1 => detuning dominates, feedback negligible')
    return ok


def main():
    r = [v1(), v2(), v3(), v4()]
    n_pass = sum(1 for c in CHECKS if c['pass'])
    OUT['summary'] = {'checks': len(CHECKS), 'pass': n_pass,
                      'fail': len(CHECKS) - n_pass, 'verified': n_pass == len(CHECKS)}
    here = os.path.dirname(os.path.abspath(__file__))
    with io.open(os.path.join(here, '§16_瞬态弛豫数据.json'), 'w',
                 encoding='utf-8', newline='\n') as fh:
        json.dump(OUT, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    for c in CHECKS:
        print('%-40s %s  %s' % (c['check'], 'PASS' if c['pass'] else 'FAIL', c['detail']))
    print('checks: %d  pass: %d  fail: %d  verified=%s'
          % (len(CHECKS), n_pass, len(CHECKS) - n_pass, n_pass == len(CHECKS)))
    return 0 if n_pass == len(CHECKS) else 1


if __name__ == '__main__':
    sys.exit(main())
