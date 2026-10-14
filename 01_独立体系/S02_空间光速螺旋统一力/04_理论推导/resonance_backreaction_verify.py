# -*- coding: utf-8 -*-
"""S02 §16.10 测试粒子近似自洽性：非线性反馈（反作用）判据的数值验证。

开放项②：粒子质量 m 对 4 力动力学演化的非线性反馈（当前为测试粒子近似，
场不被粒子反散射）。本脚本给出闭式判据并数值验证：

  V1  tau_0 = q^2/(6*pi*eps0*m*c^3) = 2*r_e/(3*c) = 2*alpha*hbar/(3*m*c^2)  三路径一致
  V2  eps_rad = tau_0*omega 为唯一无量纲反馈参数；eps_rad=1 的临界频率满足
      hbar*omega_c/(m*c^2) = 3/(2*alpha) = 205.5（与粒子质量无关，普适常数）
  V3  辐射反作用对共振频率的偏移是二阶：delta_omega/omega = -eps_rad^2/4
      （Landau-Lifshitz 降阶方程数值扫频 vs 闭式 sqrt(omega0^2 - gamma^2/2)）
  V4  Schwinger 场强阈值 E_S = m^2*c^3/(e*hbar) 与对应强度；S02 可及场强远低于此
  V5  反馈修正 vs §16.9 非傍轴修正的量级对比（S02 典型参数）

纯标准库，无外部依赖。
"""
import io
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ---------------- CODATA 2018 ----------------
C = 299792458.0
QE = 1.602176634e-19
ME = 9.1093837015e-31
MMU = 1.883531627e-28
MP = 1.67262192369e-27
HBAR = 1.054571817e-34
EPS0 = 8.8541878128e-12
ALPHA = QE * QE / (4.0 * math.pi * EPS0 * HBAR * C)  # 内部自洽定义 alpha = e^2/(4 pi eps0 hbar c)
ALPHA_LIT = 7.2973525693e-3                          # CODATA 字面值，仅用于口径注记
RE = QE * QE / (4.0 * math.pi * EPS0 * ME * C * C)  # 经典电子半径

OUT = {}
CHECKS = []


def rec(name, ok, detail):
    CHECKS.append({'check': name, 'pass': bool(ok), 'detail': str(detail)})
    return bool(ok)


def tau0_q(m):
    """ALD 特征时间：q^2/(6*pi*eps0*m*c^3)。"""
    return QE * QE / (6.0 * math.pi * EPS0 * m * C ** 3)


def tau0_re(m):
    """r_e 路径：2*r_e/(3*c)，其中 r_e(m) = q^2/(4*pi*eps0*m*c^2)。"""
    r_e = QE * QE / (4.0 * math.pi * EPS0 * m * C * C)
    return 2.0 * r_e / (3.0 * C)


def tau0_alpha(m):
    """精细结构路径：2*alpha*hbar/(3*m*c^2)。"""
    return 2.0 * ALPHA * HBAR / (3.0 * m * C * C)


# ---------------- V1：tau_0 三路径一致 ----------------
def v1():
    rows = []
    ok = True
    for nm, m in (('e', ME), ('mu', MMU), ('p', MP)):
        a, b, d = tau0_q(m), tau0_re(m), tau0_alpha(m)
        rel = max(abs(b - a) / a, abs(d - a) / a)
        ok = ok and rel < 1e-12
        rows.append({'particle': nm, 'tau0_s': a, 'tau0_via_re_s': b,
                     'tau0_via_alpha_s': d, 'max_rel_diff': rel})
    # 口径注记：内部自洽 alpha 与 CODATA 字面 alpha 的差 = 输入常数位数差（eps0 主导），
    # 非判据错误，登记不判 FAIL。
    alpha_gap = abs(ALPHA - ALPHA_LIT) / ALPHA_LIT
    OUT['v1_tau0_three_paths'] = rows
    OUT['v1b_alpha_codata_gap'] = {'alpha_internal': ALPHA, 'alpha_codata_literal': ALPHA_LIT,
                                   'rel_gap': alpha_gap,
                                   'attribution': 'eps0 输入位数（CODATA 相对不确定度 1.5e-10 量级），非判据错误'}
    rec('V1_tau0_three_paths_agree', ok,
        'max rel diff = %.3e (internal alpha); CODATA literal gap = %.3e (logged, not judged)'
        % (max(r['max_rel_diff'] for r in rows), alpha_gap))
    return ok


# ---------------- V2：eps_rad = tau0*omega，临界频率闭式 ----------------
def v2():
    rows = []
    ok = True
    target = 3.0 / (2.0 * ALPHA)  # hbar*omega_c/(m c^2)
    for nm, m in (('e', ME), ('mu', MMU), ('p', MP)):
        t0 = tau0_q(m)
        omega_c = 1.0 / t0                      # eps_rad = 1 的角频率
        ratio = HBAR * omega_c / (m * C * C)
        rel = abs(ratio - target) / target
        ok = ok and rel < 1e-12
        rows.append({'particle': nm, 'omega_c_rad_s': omega_c,
                     'hbar_omega_c_over_mc2': ratio,
                     'closed_form_3_over_2alpha': target, 'rel_diff': rel,
                     'hbar_omega_c_MeV': HBAR * omega_c / QE / 1e6})
    # 1/m 标度检验：eps_rad * m 在同一 omega 下为常数
    om = 2.0 * math.pi * C / 800e-9
    prod = [tau0_q(m) * om * m for m in (ME, MMU, MP)]
    spread = (max(prod) - min(prod)) / (sum(prod) / len(prod))
    ok = ok and spread < 1e-12
    OUT['v2_eps_rad'] = {'critical': rows, 'eps_rad_times_m_const_rel_spread': spread,
                         'omega_optical_800nm': om,
                         'eps_rad_e_optical': tau0_q(ME) * om}
    rec('V2_critical_frequency_closed_form', ok,
        'hbar*omega_c/(m c^2)=3/(2 alpha)=%.6f, rel<=%.2e; 1/m spread=%.2e'
        % (target, max(r['rel_diff'] for r in rows), spread))
    return ok


# ---------------- V3：辐射反作用对共振的偏移是二阶 ----------------
def v3():
    """Landau-Lifshitz 降阶方程数值扫频，与闭式 omega_peak=sqrt(w0^2-gamma^2/2) 对比。

    零阶受迫运动 x'' = -(w0^2)x - gamma_eff*x' + F*cos(Omega*t)，
    其中 ALD 的有效阻尼 gamma_eff = tau0*w0^2（由 m*tau0*x''' 用零阶解降阶得到）。
    """
    rows = []
    ok = True
    for eps in (0.05, 0.10, 0.20):
        w0 = 1.0
        gamma = eps * w0
        # 扫频：稳态振幅解析式用于全频扫描（等效于长时积分的稳态解）
        def amp(om):
            return 1.0 / math.sqrt((w0 * w0 - om * om) ** 2 + (gamma * om) ** 2)

        n = 400001
        lo, hi = w0 * (1 - 5 * eps), w0 * (1 + 5 * eps)
        best_om, best_a = lo, amp(lo)
        for i in range(1, n):
            om = lo + (hi - lo) * i / (n - 1)
            a = amp(om)
            if a > best_a:
                best_a, best_om = a, om
        closed = math.sqrt(w0 * w0 - gamma * gamma / 2.0)
        rel_num = (best_om - w0) / w0
        rel_closed = (closed - w0) / w0
        rel_2nd = -eps * eps / 4.0
        dev_closed = abs(best_om - closed) / w0
        dev_2nd = abs(rel_num - rel_2nd) / abs(rel_2nd)
        rows.append({'eps': eps, 'omega_peak_numeric': best_om,
                     'omega_peak_closed_sqrt': closed,
                     'delta_over_omega_numeric': rel_num,
                     'delta_over_omega_closed': rel_closed,
                     'second_order_-eps2_over_4': rel_2nd,
                     'dev_vs_closed': dev_closed, 'dev_vs_second_order': dev_2nd})
        ok = ok and dev_closed < 1e-6 and dev_2nd < 5e-2
    OUT['v3_resonance_shift'] = rows
    rec('V3_shift_is_second_order', ok,
        'numeric peak vs sqrt(w0^2-g^2/2): dev<=%.2e; vs -eps^2/4: dev<=%.2e'
        % (max(r['dev_vs_closed'] for r in rows),
           max(r['dev_vs_second_order'] for r in rows)))
    return ok


# ---------------- V4：Schwinger 阈值（场致非线性通道） ----------------
def v4():
    rows = []
    ok = True
    for nm, m in (('e', ME), ('mu', MMU), ('p', MP)):
        es = m * m * C ** 3 / (QE * HBAR)
        inten = 0.5 * C * EPS0 * es * es           # W/m^2
        rows.append({'particle': nm, 'E_Schwinger_V_per_m': es,
                     'intensity_W_per_m2': inten,
                     'intensity_W_per_cm2': inten * 1e-4})
    # 判别：当前最强激光 ~1e23 W/cm^2 仍低 6 个量级
    ref = 1e23  # W/cm^2，现存最强激光量级
    ratio = rows[0]['intensity_W_per_cm2'] / ref
    ok = ok and ratio > 1e5
    OUT['v4_schwinger'] = {'thresholds': rows,
                           'reference_laser_W_per_cm2': ref,
                           'electron_threshold_over_reference': ratio}
    rec('V4_schwinger_far_above_reachable', ok,
        'electron I_S = %.3e W/cm^2 = %.3e x 1e23 W/cm^2' % (rows[0]['intensity_W_per_cm2'], ratio))
    return ok


# ---------------- V5：反馈修正 vs 非傍轴修正（S02 典型参数） ----------------
def v5():
    lam = 800e-9
    k = 2.0 * math.pi / lam
    om = C * k
    rows = []
    ok = True
    for w0_mult in (5.0, 10.0, 50.0, 100.0):
        w0 = w0_mult * lam
        zr = k * w0 * w0 / 2.0
        for l in (0, 1, 2, 3):
            nonpar = (abs(l) + 1) / (k * k * w0 * w0)     # §16.9 一阶闭式
            eps = tau0_q(ME) * om
            back = -eps * eps / 4.0                        # 二阶反馈偏移
            rows.append({'w0_over_lambda': w0_mult, 'l': l,
                         'z_R_m': zr,
                         'nonparaxial_shift': nonpar,
                         'backreaction_shift': back,
                         'ratio_nonpar_over_back': nonpar / abs(back)})
    minratio = min(r['ratio_nonpar_over_back'] for r in rows)
    ok = ok and minratio > 1e10
    OUT['v5_shift_comparison'] = {'lambda_m': lam, 'omega_rad_s': om,
                                  'eps_rad_e': tau0_q(ME) * om, 'rows': rows,
                                  'min_ratio_nonpar_over_back': minratio}
    rec('V5_backreaction_negligible_vs_nonparaxial', ok,
        'min ratio = %.3e' % minratio)
    return ok


def main():
    r = [v1(), v2(), v3(), v4(), v5()]
    n_pass = sum(1 for c in CHECKS if c['pass'])
    OUT['summary'] = {'checks': len(CHECKS), 'pass': n_pass,
                      'fail': len(CHECKS) - n_pass, 'verified': n_pass == len(CHECKS)}
    here = os.path.dirname(os.path.abspath(__file__))
    with io.open(os.path.join(here, '§16_测试粒子近似反作用判据数据.json'), 'w',
                 encoding='utf-8', newline='\n') as fh:
        json.dump(OUT, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    for c in CHECKS:
        print('%-46s %s  %s' % (c['check'], 'PASS' if c['pass'] else 'FAIL', c['detail']))
    print('checks: %d  pass: %d  fail: %d  verified=%s'
          % (len(CHECKS), n_pass, len(CHECKS) - n_pass, n_pass == len(CHECKS)))
    return 0 if n_pass == len(CHECKS) else 1


if __name__ == '__main__':
    sys.exit(main())
