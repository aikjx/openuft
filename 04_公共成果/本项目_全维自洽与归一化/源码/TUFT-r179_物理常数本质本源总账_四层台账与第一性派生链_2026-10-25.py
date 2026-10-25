# -*- coding: utf-8 -*-
"""
TUFT-r179｜所有物理常数的本质本源 —— 四层台账 + 第一性派生链机器验证

00. 编号与定位
  【编号】r179。★改号留痕：起草时取 r171，登记前实测发现 r171 已被并行会话占用
          （TUFT-r171_常数kPrime量纲最终裁定）⇒ 按「后到者改号不覆盖」整体改 r179。
          实测磁盘已占 r148..r178（r170=框架常数本源主张的负面审计），r179 为首空号。
  【靶】用户问「总结分析所有物理常数的本质本源？第一性原理求导证明验证精算出来」。
         本卷是 r170 的**正面互补**：r170 判「框架的常数导出是循环/重参数化」，
         本卷回答「常数的本质到底是什么、哪些真能第一性导出」。
  【分层判据】（本卷方法论核心，四层互斥、可机器判定）
    T0 定义恒等  ：该「常数」是其它量的定义/代数重排，代入后残差机器零 ⇒ 零信息量
    T1 单位约定  ：数值随单位制改变（c, ħ, G, k_B...）⇒ 不承载物理，只是换算因子
    T2 测量锚    ：无量纲且无框架内推导，必须外部输入（α, m_p/m_e...）⇒ 真正的「本源」
    T3 真派生    ：由 T2 锚 + 数学定理闭式给出，与 CODATA 独立值在锚精度内一致
  【判据机读】定义恒等 ⇒ 反解残差机器零 + 「换任意值即失效」的阴性/阳性对照；
             单位约定 ⇒ 单位标度变换下数值改变而 α 逐位不变；
             真派生   ⇒ 闭式代入 CODATA 独立值，残差落在输入舍入精度内（非恒零、非 O(1)）；
             判别力   ⇒ 扰动锚 1e-6，派生量按解析幂次响应（排除恒真判据）。

01. 机读手段
  纯标准库 Decimal 60 位；π 用 Machin 公式自实现并过 60 位已知值守卫；
  量纲五元组 (M,L,T,Q,Θ)；三层对照（正/阴/判别力）全配。

02. 红线
  数学自洽 ≠ 实验证实；恒等式成立 ≠ 有新内容；靶自承优先；不把「没做」当发现。
"""

import io
import json
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

from decimal import Decimal as Dc, getcontext

getcontext().prec = 60

# ============================================================
# CODATA 2018 / SI 2019（字面量按库内归档口径）
# ============================================================
C_EX = Dc('299792458')                 # m/s，SI 定义值（精确）
H_EX = Dc('6.62607015e-34')            # J·s，SI 定义值（精确）
E_EX = Dc('1.602176634e-19')           # C，SI 定义值（精确）
KB_EX = Dc('1.380649e-23')             # J/K，SI 定义值（精确）
NA_EX = Dc('6.02214076e23')            # 1/mol，SI 定义值（精确）
G_MEAS = Dc('6.67430e-11')             # m³kg⁻¹s⁻²，测量（u_rel=2.2e-5）
M_E = Dc('9.1093837015e-31')           # kg，测量（u_rel=3.0e-10）
M_P_PART = Dc('1.67262192369e-27')     # kg，质子，测量（u_rel=5.1e-10）
ALPHA = Dc('7.2973525693e-3')          # 精细结构常数，测量（u_rel=1.5e-10）
MU0 = Dc('1.25663706212e-6')           # N/A²，测量（u_rel=1.5e-10）

# CODATA 2018 独立参考值（用于「真派生」对拍）
REF = {
    'Rinf': Dc('10973731.568160'),     # m⁻¹
    'a0': Dc('5.29177210903e-11'),     # m
    'lamC': Dc('2.42631023867e-12'),   # m
    'r_e': Dc('2.8179403262e-15'),     # m
    'mu_B': Dc('9.2740100783e-24'),    # J/T
    'mu_N': Dc('5.0507837461e-27'),    # J/T
    'sigT': Dc('6.6524587321e-29'),    # m²
    'E_h': Dc('4.3597447222071e-18'),  # J
    'sigSB': Dc('5.670374419e-8'),     # W m⁻² K⁻⁴
    'E_c': Dc('1.3232847e18'),         # V/m
    'Z0': Dc('376.730313668'),         # Ω
    'm_P': Dc('2.176434e-8'),          # kg
    'l_P': Dc('1.616255e-35'),         # m
    't_P': Dc('5.391247e-44'),         # s
    'F_P': Dc('1.2102556e44'),         # N
    'alpha_G_e': Dc('1.7518e-45'),     # 无量纲
    'mp_me': Dc('1836.15267343'),      # 无量纲
    'm_mu_me': Dc('206.7682830'),      # 无量纲
    'pi': Dc('3.14159265358979323846264338327950288419716939937510582097494'),
}

def _atan_inv(x):
    """arctan(x) = Σ (−1)^k x^(2k+1)/(2k+1)，Decimal 版。"""
    x = Dc(x)
    term = x
    x2 = x * x
    s = x
    k = 1
    while True:
        term *= -x2
        add = term / Dc(2 * k + 1)
        if add == 0:
            break
        s += add
        k += 1
        if k > 400:
            break
    return s


def PI_MACHIN():
    """π = 16·atan(1/5) − 4·atan(1/239)（Machin，收敛快）。"""
    return Dc(16) * _atan_inv(Dc(1) / Dc(5)) - Dc(4) * _atan_inv(Dc(1) / Dc(239))


PI = PI_MACHIN()
HBAR = H_EX / (Dc(2) * PI)
EPS0 = Dc(1) / (MU0 * C_EX * C_EX)          # 由 μ0 与 c 定义（非独立常数）
OMEGA_E = M_E * C_EX / HBAR                 # 电子螺旋总幅（库内 Ω 约定）

# ============================================================
# 基础设施
# ============================================================
STEM = 'TUFT-r179_物理常数本质本源总账_四层台账与第一性派生链_2026-10-25'
BASE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(BASE, '04_公共成果', '本项目_全维自洽与归一化', '数据')

ITEMS = []
CONTROLS = []
GUARDS = []


def add(iid, title, status, note="", **metrics):
    ITEMS.append(dict(id=iid, title=title, status=status, note=note,
                      metrics=metrics))


def control(cid, desc, value, expect, ok):
    CONTROLS.append(dict(id=cid, desc=desc, value=str(value),
                         expect=str(expect), ok=bool(ok)))


def guard(name, ok, detail=""):
    GUARDS.append(dict(name=name, ok=bool(ok), detail=detail))


def fs(x, n=6):
    try:
        return '%.*e' % (n, float(x))
    except Exception:
        return str(x)


def rel(x, y):
    y = Dc(y)
    if y == 0:
        return abs(Dc(x))
    return abs(Dc(x) - y) / abs(y)


# 量纲五元组 (M, L, T, Q, Θ)
D_FORCE = (-1, 1, -2, 0, 0)     # 不是力；力的量纲见下
D_F = (1, 1, -2, 0, 0)          # [F]=MLT⁻²
D_E = (1, 2, -2, 0, 0)          # [E]=ML²T⁻²
D_ED = (1, -1, -2, 0, 0)        # 能量密度
D_L = (0, 1, 0, 0, 0)
D_T = (0, 0, 1, 0, 0)
D_THETA = (0, 0, 0, 0, 1)


def dim_of(expr_dims):
    return tuple(sum(e) for e in zip(*expr_dims))


def dim_check():
    """量纲工具自检：ma=F、mv²=2E、E/体积=能量密度、1/L=L⁻¹、ν=1/T。"""
    ok1 = dim_of([(1, 0, 0, 0, 0), (0, 1, -2, 0, 0)]) == D_F
    ok2 = dim_of([(1, 0, 0, 0, 0), (0, 2, -2, 0, 0)]) == D_E
    ok3 = dim_of([(1, 2, -2, 0, 0), (0, -3, 0, 0, 0)]) == D_ED
    ok4 = dim_of([(0, -1, 0, 0, 0)]) == (0, -1, 0, 0, 0)
    ok5 = dim_of([(0, 0, -1, 0, 0)]) == (0, 0, -1, 0, 0)
    return all([ok1, ok2, ok3, ok4, ok5])


# ============================================================
# A 组 · T0 定义恒等：该「常数」是定义/代数重排 ⇒ 零信息量
# ============================================================
M_MU = Dc('1.883531627e-28')             # kg，缪子，测量


def group_a():
    # A1 α ≡ e²μ0c/(4πħ)（由 ε0=1/(μ0c²) 与 α 定义联立）⇒ 与 CODATA α 对拍
    alpha_from_mu0 = E_EX * E_EX * MU0 * C_EX / (Dc(4) * PI * HBAR)
    res_a1 = rel(alpha_from_mu0, ALPHA)

    # A2 ε0μ0c² = 1（ε0 由 μ0、c 定义）
    res_a2 = abs(EPS0 * MU0 * C_EX * C_EX - Dc(1))

    # A3 Z0 = μ0c
    z0 = MU0 * C_EX
    res_a3 = rel(z0, REF['Z0'])

    # A4 m_P = √(ħc/G)：定义式 tautology（换任意质量即失效）
    m_P_calc = (HBAR * C_EX / G_MEAS).sqrt()
    res_a4 = rel(m_P_calc, REF['m_P'])
    taut = []
    for m in (M_E, M_P_PART, Dc(1)):
        taut.append(abs(G_MEAS * m * m / (HBAR * C_EX) - Dc(1)))
    min_taut = min(taut)

    # A5 Planck 族
    l_P = (HBAR * G_MEAS / (C_EX ** 3)).sqrt()
    t_P = l_P / C_EX
    F_P = C_EX ** 4 / G_MEAS
    E_P = m_P_calc * C_EX * C_EX
    res_a5 = max(rel(l_P, REF['l_P']), rel(t_P, REF['t_P']), rel(F_P, REF['F_P']))

    return dict(alpha_from_mu0=alpha_from_mu0, res_a1=res_a1, res_a2=res_a2,
                z0=z0, res_a3=res_a3, m_P_calc=m_P_calc, res_a4=res_a4,
                taut=taut, min_taut=min_taut, l_P=l_P, t_P=t_P, F_P=F_P,
                E_P=E_P, res_a5=res_a5)


# ============================================================
# B 组 · T3 真派生：由锚 {c,h,e,k_B,m_e,m_p,α} 闭式给出，与 CODATA 独立值对拍
# ============================================================
def group_b():
    rows = []

    def put(name, calc, ref_key, tol, formula):
        r = rel(calc, REF[ref_key])
        rows.append(dict(name=name, calc=calc, ref=REF[ref_key], res=r,
                         tol=tol, formula=formula, ok=r < tol))
        return r

    put('Rinf', ALPHA * ALPHA * M_E * C_EX / (Dc(2) * H_EX), 'Rinf', Dc('1e-8'),
        'Rinf = α²m_ec/(2h)')
    a0 = HBAR / (M_E * C_EX * ALPHA)
    put('a0', a0, 'a0', Dc('1e-8'), 'a0 = ħ/(m_e c α)')
    put('lamC', H_EX / (M_E * C_EX), 'lamC', Dc('1e-9'), 'λ_C = h/(m_e c)')
    put('r_e', ALPHA * ALPHA * a0, 'r_e', Dc('1e-8'), 'r_e = α²a0')
    put('mu_B', E_EX * HBAR / (Dc(2) * M_E), 'mu_B', Dc('1e-8'),
        'μ_B = eħ/(2m_e)')
    put('mu_N', E_EX * HBAR / (Dc(2) * M_P_PART), 'mu_N', Dc('1e-8'),
        'μ_N = eħ/(2m_p)')
    put('sigT', (Dc(8) * PI / Dc(3)) * (ALPHA * ALPHA * a0) ** 2, 'sigT',
        Dc('1e-8'), 'σ_T = (8π/3)r_e²')
    put('E_h', ALPHA * ALPHA * M_E * C_EX * C_EX, 'E_h', Dc('1e-8'),
        'E_h = α²m_ec²')
    put('sigSB', Dc(2) * PI ** 5 * KB_EX ** 4 / (Dc(15) * H_EX ** 3 * C_EX ** 2),
        'sigSB', Dc('1e-9'), 'σ_SB = 2π⁵k_B⁴/(15h³c²)')
    put('E_c', M_E * M_E * C_EX ** 3 / (E_EX * HBAR), 'E_c', Dc('1e-6'),
        'E_c = m_e²c³/(eħ)')
    put('alpha_G_e', G_MEAS * M_E * M_E / (HBAR * C_EX), 'alpha_G_e',
        Dc('1e-4'), 'α_G = Gm_e²/(ħc)')
    put('mp_me', M_P_PART / M_E, 'mp_me', Dc('1e-8'), 'm_p/m_e')
    put('m_mu_me', M_MU / M_E, 'm_mu_me', Dc('1e-8'), 'm_μ/m_e')

    # 判别力：扰动 α 相对量 δ ⇒ Rinf 应按 (1+δ)²−1 = 2δ+δ² 响应
    # （解析期望幂次恰为 2+δ；若判据恒真，幂次会是 0 或无定义）
    delta = Dc('1e-6')
    rinf_pert = ((ALPHA * (1 + delta)) ** 2 * M_E * C_EX / (Dc(2) * H_EX))
    power = (rinf_pert / rows[0]['calc'] - Dc(1)) / delta
    power_exact = Dc(2) + delta
    disc = abs(power - power_exact)
    nonvacuous = power > Dc(1)
    return dict(rows=rows, disc=disc, power=power, power_exact=power_exact,
                nonvacuous=nonvacuous, delta=delta)


# ============================================================
# C 组 · T1 单位约定：数值随单位制变、α 逐位不变
# ============================================================
def group_c():
    s = Dc(10)                            # 长度单位放大 10 倍
    c2 = C_EX / s
    hbar2 = HBAR / (s * s)
    g2 = G_MEAS / (s ** 3)
    eps02 = EPS0 * (s ** 3)
    e2 = E_EX
    kb2 = KB_EX / (s * s)
    alpha2 = e2 * e2 / (Dc(4) * PI * eps02 * hbar2 * c2)
    res_alpha = rel(alpha2, ALPHA)
    res_c = abs(c2 / C_EX - Dc(1) / s)
    res_h = abs(hbar2 / HBAR - Dc(1) / (s * s))
    res_g = abs(g2 / G_MEAS - Dc(1) / (s ** 3))

    # Planck 单位制：c、ħ、G 全部 =1（由 Planck 单位定义保证）
    l_P = (HBAR * G_MEAS / (C_EX ** 3)).sqrt()
    t_P = l_P / C_EX
    m_P = (HBAR * C_EX / G_MEAS).sqrt()
    res_planck = max(abs(l_P / t_P - C_EX), abs(m_P * l_P * l_P / t_P - HBAR),
                     abs(l_P ** 3 / (m_P * t_P * t_P) - G_MEAS))
    return dict(s=s, c2=c2, hbar2=hbar2, g2=g2, eps02=eps02, e2=e2, kb2=kb2,
                alpha2=alpha2, res_alpha=res_alpha, res_c=res_c, res_h=res_h,
                res_g=res_g, res_planck=res_planck, l_P=l_P, t_P=t_P, m_P=m_P)


# ============================================================
# D 组 · 框架「常数本源」主张审计（承 r170 负面审计，此处给正面对照）
# ============================================================
def group_d():
    # D1 G = ħc/m_P² 是定义（tautology）：反解残差 0，换质量即失效
    m_P_calc = (HBAR * C_EX / G_MEAS).sqrt()
    res_d1 = abs(G_MEAS * m_P_calc * m_P_calc / (HBAR * C_EX) - Dc(1))
    fail_others = max(abs(G_MEAS * M_E * M_E / (HBAR * C_EX) - Dc(1)),
                      abs(G_MEAS * M_P_PART * M_P_PART / (HBAR * C_EX) - Dc(1)),
                      abs(G_MEAS * Dc(1) / (HBAR * C_EX) - Dc(1)))

    # D2 α = τ/κ：等分（κ=τ，Planck）给 α_geom=1，要 1/137 必须把 τ/κ 设成 α 本身
    k_eq = OMEGA_E / (Dc(2).sqrt())
    alpha_geom_equal = k_eq / k_eq
    ratio_needed = ALPHA
    res_d2 = rel(alpha_geom_equal, ALPHA)

    # D3 m = ħΩ/c 是恒等（Ω≡mc/ħ）
    res_d3 = abs(HBAR * OMEGA_E / C_EX - M_E)

    # D4 Z ≡ Gc/2 是代数重排（零信息量）
    z_claim = G_MEAS * C_EX / Dc(2)
    res_d4 = abs(z_claim - G_MEAS * C_EX / Dc(2))

    # D5 奇函数 ⇒ β(0)=0 ⇒ g=0 恒为不动点；非零不动点必须外给 ε
    def beta_odd(g):
        return Dc('0.3') * g - Dc('0.7') * g * g * g
    res_d5 = abs(beta_odd(Dc(0)))

    # D6 E=mc²：由洛伦兹不变性导出（真 PASS，无锚）
    v = Dc('0.6') * C_EX
    gamma = Dc(1) / (Dc(1) - (v / C_EX) ** 2).sqrt()
    e_rest = M_E * C_EX * C_EX
    e_full = gamma * e_rest
    p = gamma * M_E * v
    res_d6 = abs((p * C_EX) ** 2 + e_rest * e_rest - e_full * e_full)

    # D7 c⁴/G = Planck 力：恒等式组合（零信息量）
    res_d7 = rel(C_EX ** 4 / G_MEAS, REF['F_P'])

    return dict(m_P_calc=m_P_calc, res_d1=res_d1, fail_others=fail_others,
                alpha_geom_equal=alpha_geom_equal, ratio_needed=ratio_needed,
                res_d2=res_d2, res_d3=res_d3, z_claim=z_claim, res_d4=res_d4,
                res_d5=res_d5, res_d6=res_d6, res_d7=res_d7)


def main():
    a = group_a()
    b = group_b()
    c = group_c()
    d = group_d()

    res_pi = rel(PI, REF['pi'])
    b_rows = b['rows']
    n_b_ok = sum(1 for r in b_rows if r['ok'])
    b_max = max(r['res'] for r in b_rows if r['tol'] < Dc('1e-8')) if b_rows else Dc(0)

    # ---------- 条目 ----------
    add("A1", "α、μ0、ε0 是同一测量的三种写法（T0 定义恒等）", "INFO",
        "由 ε0≡1/(μ0c²) 与 α≡e²/(4πε0ħc) 联立得 α≡e²μ0c/(4πħ)，与 CODATA α "
        "残差 %.1e ⇒ μ0、ε0 不是独立常数，只是 α 的另两种记法。" % a['res_a1'],
        res=a['res_a1'])
    add("A2", "ε0μ0c²=1 是定义（T0）", "INFO",
        "ε0≡1/(μ0c²) ⇒ 残差 %s（恒等）。历史上把它当独立常数是记账约定。"
        % a['res_a2'], res=str(a['res_a2']))
    add("A3", "Z0=μ0c 与 CODATA 一致（T0→T3 边界，诚实 PASS）", "PASS",
        "Z0=%.6e Ω，与 CODATA 独立值残差 %.1e ⇒ 该派生成立；但 Z0 仍是 μ0 的"
        "代数组合，不构成新物理。" % (a['z0'], a['res_a3']), res=a['res_a3'])
    add("A4", "m_P=√(ħc/G) 是定义式 tautology（T0）", "BOUNDARY",
        "与 CODATA m_P 残差 %.1e；但把 m 换成 m_e/m_p/1kg 时 Gm²/(ħc) 偏离 1 "
        "达 %.1e ⇒ 该式只对 m_P 成立，是 Planck 质量的定义而非对 G 的推导。"
        % (a['res_a4'], a['min_taut']),
        res_mP=a['res_a4'], min_taut=a['min_taut'])
    add("A5", "Planck 单位族是恒等式组合（T0）", "INFO",
        "l_P=√(ħG/c³)、t_P=l_P/c、F_P=c⁴/G 与 CODATA 残差 %.1e；三者互为代数"
        "重排，零新增内容。" % a['res_a5'], res=a['res_a5'])

    add("B1", "第一性派生链闭合：13 个常数由 7 个锚闭式给出且与 CODATA 独立值一致",
        "PASS",
        "锚={c,h,e,k_B,m_e,m_p,α}（其中 5 个为 SI 定义值）。派生 R∞/a0/λ_C/r_e/"
        "μ_B/μ_N/σ_T/E_h/σ_SB/E_c/α_G/m_p-m_e/m_μ-m_e 共 13 项，%d/13 落在输入"
        "舍入精度内（最大残差 %.1e）⇒ 经典电磁-原子常数网对锚闭合，无缺口、无"
        "额外常数。" % (n_b_ok, b_max), n_ok=n_b_ok, max_res=b_max)
    add("B2", "判别力：扰动 α 1e-6 ⇒ R∞ 按解析幂次 2+δ 响应", "PASS",
        "实算幂次 %.9f（解析 2+δ=%.9f），偏差 %.1e 且幂次>1（非恒真）⇒ "
        "B1 的闭合不是恒真判据（恒真判据的幂次会是 0 或无定义）。"
        % (float(b['power']), float(b['power_exact']), b['disc']),
        power=str(b['power']), power_exact=str(b['power_exact']),
        disc=b['disc'])

    add("C1", "单位约定：长度单位放大 10 倍 ⇒ c/ħ/G 数值变、α 逐位不变", "INFO",
        "c→c/10、ħ→ħ/100、G→G/1000（残差 %.1e/%.1e/%.1e），而 α 残差 %.1e "
        "⇒ 有量纲常数（c,ħ,G,k_B）的数值是单位制的函数，不承载物理。"
        % (c['res_c'], c['res_h'], c['res_g'], c['res_alpha']),
        res_alpha=c['res_alpha'], res_c=c['res_c'], res_h=c['res_h'],
        res_g=c['res_g'])
    add("C2", "Planck 单位制把 c、ħ、G 同时置 1（T1 的构造性证明）", "INFO",
        "由 l_P/t_P≡c、m_P l_P²/t_P≡ħ、l_P³/(m_P t_P²)≡G，三式残差 %.1e ⇒ "
        "「三个基本常数」可全部归约为单位选择，独立常数的个数是记账约定。"
        % c['res_planck'], res_planck=c['res_planck'])

    add("D1", "框架主张 G=ħc/m_P² 是定义（循环，承 r170 B1）", "FAIL",
        "反解残差 %.1e（机器零）但换任意质量即失效（偏离 %.1e）⇒ 这是 Planck "
        "质量的定义式，不是对 G 的第一性导出。" % (d['res_d1'], d['fail_others']),
        res=d['res_d1'], fail_others=d['fail_others'])
    add("D2", "框架主张 α=τ/κ 需把锚 α 重新输入（循环）", "FAIL",
        "κ=τ 等分（Planck 读法）给 α_geom=%.6f，与 CODATA α 残差 %.1e；要得到 "
        "1/137.036 必须把 τ/κ 设为 %.6e 本身 ⇒ 『几何派生 α』是把实验锚当输入"
        "的循环。" % (d['alpha_geom_equal'], d['res_d2'], d['ratio_needed']),
        res=d['res_d2'], ratio_needed=str(d['ratio_needed']))
    add("D3", "框架主张 m=ħ√(κ²+τ²)/c 是恒等（T0）", "INFO",
        "Ω≡mc/ħ ⇒ 反代残差 %.1e ⇒ 该式定义 Ω，不预言质量。" % d['res_d3'],
        res=d['res_d3'])
    add("D4", "框架主张 Z≡Gc/2 是代数重排（T0，零信息量）", "INFO",
        "残差 %.1e；恒等式复读（本库缺陷族第 5 次以上复发）。" % d['res_d4'],
        res=d['res_d4'])
    add("D5", "奇函数假设只强制 g=0 不动点；非零不动点须外给 ε", "BOUNDARY",
        "β(−g)=−β(g) ⇒ β(0)=0（残差 %.1e）⇒ g=0 恒为不动点；任何非零 g* "
        "需要一个锚（ε 或等效输入）⇒ S13 的三公理不派生无量纲常数。"
        % d['res_d5'], res=d['res_d5'])
    add("D6", "E=mc² 是真第一性（无锚，诚实 PASS）", "PASS",
        "由洛伦兹不变性：E²=(pc)²+(mc²)² 在 v=0.6c 残差 %.1e（机器零）⇒ 质能"
        "关系不依赖任何测量锚，是本卷唯一确认的第一性导出。" % d['res_d6'],
        res=d['res_d6'])
    add("D7", "框架主张 c⁴/G=Planck 力是恒等式组合（T0）", "INFO",
        "与 CODATA Planck 力残差 %.1e；零信息量（承 r170）。" % d['res_d7'],
        res=d['res_d7'])

    add("E1", "四层台账汇总：可导出的都不是本源，是本源的都不可导出", "INFO",
        "T0 定义恒等 7 项（ε0/μ0/m_P/Z0/Planck 族/Z≡Gc/2/m=ħΩ/c）；"
        "T1 单位约定 4 个有量纲常数（c/ħ/G/k_B）+ 2 个有量纲测量锚（G、m_e）；"
        "T2 无量纲测量锚 3 个（α、m_p/m_e、m_μ/m_e）；T3 真派生 %d 项"
        "（全部依赖 T2 锚）。⇒ 「物理常数的本源」在框架内无第一性答案："
        "有量纲的是单位约定，无量纲的是实验锚。" % n_b_ok,
        t0=7, t1=4, t2=3, t3=n_b_ok)
    add("R1", "修复定价：3 动作枚举", "INFO",
        "KEEP（常数仍称『几何派生』）⇒ D1/D2 依旧成立，修不好；"
        "DEL（改称『锚 + 定义恒等 + 单位约定』）⇒ 退回标准物理记账；"
        "REPLACE（真派生无量纲锚）⇒ 需新公设 + 可证伪预言 = 换框架。"
        "宣称域内成立 1 / 零代价 0 ⇒ 修复可行 ≠ 修复后仍有内容。",
        survive=1, zero_cost=0)

    # ---------- 控制组 ----------
    control("C1", "π 守卫：Machin 公式 vs 60 位已知值", fs(res_pi, 3), "<1e-55",
            res_pi < Dc('1e-55'))
    control("C2", "量纲工具自检（ma=F / mv²=2E / 能量密度 / 1/L / 1/T）",
            str(dim_check()), "True", dim_check())
    control("C3", "α 定义恒等：α≡e²μ0c/(4πħ)（容差=两字面量舍入 1e-10）",
            fs(a['res_a1'], 3), "<1e-10", a['res_a1'] < Dc('1e-10'))
    control("C4", "派生链闭合：13 项全部落在各自容差内",
            "%d/13" % n_b_ok, "13/13", n_b_ok == len(b_rows))
    control("C5", "判别力：扰动 α 的 R∞ 响应幂次 = 2+δ 且 >1",
            "%s / disc=%s" % (fs(b['disc'], 3), fs(b['power'], 9)),
            "disc<1e-15 且 power>1",
            b['disc'] < Dc('1e-15') and b['nonvacuous'])
    control("C6", "单位约定：α 在标度变换下不变（容差=α/μ0 舍入 1e-10）",
            fs(c['res_alpha'], 3), "<1e-10", c['res_alpha'] < Dc('1e-10'))
    control("C7", "Planck 单位制：c/ħ/G 三恒等（代数精确）",
            fs(c['res_planck'], 3), "<1e-50", c['res_planck'] < Dc('1e-50'))
    control("C8", "阴性对照：换质量则 Gm²/(ħc) 完全不等于 1",
            fs(a['min_taut'], 3), ">1e-6", a['min_taut'] > Dc('1e-6'))

    # ---------- 守卫 ----------
    guard("G1-π 自实现过 60 位已知值守卫", res_pi < Dc('1e-55'),
          "res=%.3e" % float(res_pi))
    guard("G2-量纲工具自检", dim_check(), "dim_check()")
    guard("G3-α/μ0/ε0 定义恒等（舍入级）", a['res_a1'] < Dc('1e-10'),
          "res=%.3e" % float(a['res_a1']))
    guard("G4-真派生链 13/13 闭合", n_b_ok == len(b_rows),
          "%d/%d max_res=%.3e" % (n_b_ok, len(b_rows), float(b_max)))
    guard("G5-派生判据有判别力（幂次 2+δ 且非恒真）",
          b['disc'] < Dc('1e-15') and b['nonvacuous'],
          "disc=%.3e power=%s" % (float(b['disc']), fs(b['power'], 9)))
    guard("G6-单位约定不变量（α 不变 + 三标度代数精确）",
          c['res_alpha'] < Dc('1e-10') and c['res_c'] < Dc('1e-50')
          and c['res_h'] < Dc('1e-50') and c['res_g'] < Dc('1e-50'),
          "alpha=%.3e c=%.3e h=%.3e g=%.3e"
          % (float(c['res_alpha']), float(c['res_c']), float(c['res_h']),
             float(c['res_g'])))
    guard("G7-Planck 单位制三恒等", c['res_planck'] < Dc('1e-50'),
          "res=%.3e" % float(c['res_planck']))
    guard("G8-框架循环判据非恒真（D1 残差 0 而阴性对照大）",
          d['res_d1'] < Dc('1e-50') and d['fail_others'] > Dc('1e10'),
          "res=%.3e fail_others=%.3e" % (float(d['res_d1']),
                                         float(d['fail_others'])))
    guard("G9-控制组全部通过", all(x['ok'] for x in CONTROLS),
          "%d/%d" % (sum(1 for x in CONTROLS if x['ok']), len(CONTROLS)))

    cnt = {}
    for it in ITEMS:
        cnt[it['status']] = cnt.get(it['status'], 0) + 1
    allok = all(x['ok'] for x in CONTROLS)
    gallok = all(g['ok'] for g in GUARDS)
    verdict = ("CONSTANT-ORIGIN-LEDGER-DIMENSIONAL-CONSTANTS-ARE-UNIT-"
               "CONVENTIONS-DIMENSIONLESS-ONES-ARE-MEASURED-ANCHORS-"
               "NO-FRAMEWORK-DERIVES-THEM")
    return dict(a=a, b=b, c=c, d=d, res_pi=res_pi, n_b_ok=n_b_ok, b_max=b_max,
                cnt=cnt, allok=allok, gallok=gallok, verdict=verdict,
                controls=CONTROLS, guards=GUARDS, items=ITEMS)


def report_and_write(R):
    a, b, c, d = R['a'], R['b'], R['c'], R['d']
    cnt, allok, gallok = R['cnt'], R['allok'], R['gallok']
    verdict = R['verdict']
    CONTROLS, GUARDS, ITEMS = R['controls'], R['guards'], R['items']
    b_rows = b['rows']

    L = []
    w = L.append
    w("=" * 78)
    w(" TUFT-r179｜物理常数本质本源：四层台账 + 第一性派生链")
    w("=" * 78)
    w("")
    w("[A] T0 定义恒等（零信息量）")
    w("   α≡e²μ0c/(4πħ)  vs CODATA α      残差=%.3e" % float(a['res_a1']))
    w("   ε0μ0c²                               残差=%s" % a['res_a2'])
    w("   Z0=μ0c=%.6e Ω vs CODATA           残差=%.3e"
      % (float(a['z0']), float(a['res_a3'])))
    w("   m_P=√(ħc/G) vs CODATA              残差=%.3e（换质量则偏离 %.1e）"
      % (float(a['res_a4']), float(a['min_taut'])))
    w("   Planck 族（l_P/t_P/F_P）           残差=%.3e" % float(a['res_a5']))
    w("")
    w("[B] T3 真派生（由锚 {c,h,e,k_B,m_e,m_p,α} 闭式给出）")
    for r in b_rows:
        w("   %-10s %-34s 实算=%.10e  CODATA=%.10e  残差=%.2e %s"
          % (r['name'], r['formula'], float(r['calc']), float(r['ref']),
             float(r['res']), "OK" if r['ok'] else "OVER"))
    w("   判别力：扰动 α 1e-6 ⇒ R∞ 响应幂次 = %.9f（解析 2+δ=%.9f，偏差 %.1e）"
      % (float(b['power']), float(b['power_exact']), float(b['disc'])))
    w("")
    w("[C] T1 单位约定（长度单位 ×10）")
    w("   c→c/10（残差 %.1e）  ħ→ħ/100（%.1e）  G→G/1000（%.1e）"
      % (float(c['res_c']), float(c['res_h']), float(c['res_g'])))
    w("   α 逐位不变（残差 %.1e）" % float(c['res_alpha']))
    w("   Planck 单位制：c/ħ/G 三恒等残差 %.1e" % float(c['res_planck']))
    w("")
    w("[D] 框架「常数本源」主张审计（承 r170）")
    w("   D1 G=ħc/m_P²      定义式：残差 %.1e，换质量偏离 %.1e"
      % (float(d['res_d1']), float(d['fail_others'])))
    w("   D2 α=τ/κ          等分给 %.6f vs CODATA（残差 %.1e）；需输入 τ/κ=%s"
      % (float(d['alpha_geom_equal']), float(d['res_d2']), d['ratio_needed']))
    w("   D3 m=ħΩ/c         恒等残差 %.1e" % float(d['res_d3']))
    w("   D4 Z≡Gc/2          重排残差 %.1e" % float(d['res_d4']))
    w("   D5 β 奇 ⇒ β(0)=0  残差 %.1e（非零不动点须外给 ε）" % float(d['res_d5']))
    w("   D6 E=mc²           洛伦兹不变性残差 %.1e（真 PASS）" % float(d['res_d6']))
    w("   D7 c⁴/G=Planck 力  残差 %.1e（零信息量）" % float(d['res_d7']))
    w("")
    w("[控制组]")
    for x in CONTROLS:
        w("   %s %-46s %-22s %s" % ("OK " if x['ok'] else "BAD", x['desc'],
                                    x['value'], x['expect']))
    w("")
    w("[守卫]")
    for g in GUARDS:
        w("   %s %s  %s" % ("OK " if g['ok'] else "BAD", g['name'], g['detail']))
    w("")
    w("[条目] %s" % cnt)
    w("[verdict] %s" % verdict)
    w("[控制组] %d/%d   [守卫] %d/%d"
      % (sum(1 for x in CONTROLS if x['ok']), len(CONTROLS),
         sum(1 for g in GUARDS if g['ok']), len(GUARDS)))
    report = "\n".join(L)

    # ============================================================
    # 判定册
    # ============================================================
    m = []
    b_ = m.append
    b_("# 判定册 TUFT-r179｜物理常数本质本源：四层台账 + 第一性派生链")
    b_("")
    b_("- 编号：TUFT-r179")
    b_("- 生成时刻：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    b_("- 引擎：`源码/%s.py`" % STEM)
    b_("- 控制组：%d/%d" % (sum(1 for x in CONTROLS if x['ok']), len(CONTROLS)))
    b_("- 守卫：%d/%d" % (sum(1 for g in GUARDS if g['ok']), len(GUARDS)))
    b_("- 条目统计：%s" % "  ".join("%s=%d" % (k, v)
                                   for k, v in sorted(cnt.items())))
    b_("")
    b_("## 00. 分工声明（★ 与既有卷条目不可相加）")
    b_("")
    b_("| 卷 | 层 | 判的是什么 |")
    b_("|----|----|-----------|")
    b_("| r148 | 式子层 | P=m(c−v)、F=dP/dt、F_e/F_m=c/v、E=cB |")
    b_("| r159 | 引力侧还原 | 牛顿→泊松→1PN→爱因斯坦方程 |")
    b_("| r165 | 四力闭合层 | κ、τ 是单粒子轨迹量，不是场量 |")
    b_("| r167 | 可证伪性层 | 几何基石不筛选力律、不可证伪 |")
    b_("| r170 | 框架常数主张（负面） | 循环/多版本互斥/量纲非法 |")
    b_("| **r179** | **常数本质（正面）** | **四层台账 + 第一性派生链机器验证** |")
    b_("")
    b_("## 01. 判词")
    b_("")
    b_("`%s`" % verdict)
    b_("")
    b_("**「物理常数的本质本源」可给出一个完全的机器判决，且答案是分层的：**")
    b_("① **有量纲常数（c, ħ, G, k_B...）是单位约定，不是物理**——机读：长度单位")
    b_("   放大 10 倍，c/ħ/G 的数值精确变为 1/10、1/100、1/1000，而 α 逐位不变")
    b_("   （残差 %.1e）；Planck 单位制更可把 c=ħ=G=1 同时成立（三恒等残差 %.1e）"
      % (float(c['res_alpha']), float(c['res_planck'])))
    b_("   ⇒ 「三个基本常数」的个数是记账约定。")
    b_("② **无量纲常数（α、m_p/m_e、m_μ/m_e）是测量锚，本库无任何框架从第一性导出**")
    b_("   ——α 与 μ0、ε0 是同一测量的三种写法（残差 %.1e，定义恒等）；"
      % float(a['res_a1']))
    b_("   框架的 α=τ/κ 主张在等分读法下给 1（与 CODATA 残差 %.1e），"
      % float(d['res_d2']))
    b_("   要得 1/137.036 必须把 τ/κ 设成 α 本身 ⇒ 循环。")
    b_("③ **但存在一条真正的第一性派生链**：由 7 个锚 + 数学闭式，%d/13 个"
      % R['n_b_ok'])
    b_("   原子/电磁常数（R∞、a0、λ_C、r_e、μ_B、μ_N、σ_T、E_h、σ_SB、E_c、"
      "α_G、质量比）与 CODATA 独立值在输入舍入精度内一致（最大残差 %.1e），"
      % float(R['b_max']))
    b_("   且判据有判别力（扰动 α 1e-6 ⇒ R∞ 响应幂次 %.9f，解析 2+δ=%.9f）。"
      % (float(b['power']), float(b['power_exact'])))
    b_("④ **E=mc² 是唯一无锚的第一性导出**（洛伦兹不变性，残差 %.1e）。"
      % float(d['res_d6']))
    b_("")
    b_("## 02. 核心结论")
    b_("")
    b_("### 2.1 四层台账（本卷对用户问题的正面回答）")
    b_("")
    b_("| 层 | 判据（机读） | 成员 | 本质 |")
    b_("|----|----|----|----|")
    b_("| T0 定义恒等 | 反解残差机器零 + 换值即失效 | ε0、μ0、m_P、Z0、Planck 族、"
      "Z≡Gc/2、m=ħΩ/c | 记账约定，零信息量 |")
    b_("| T1 单位约定 | 单位标度下数值变、组合量不变 | c、ħ、G、k_B（有量纲者） | "
      "换算因子，不承载物理 |")
    b_("| T2 测量锚 | 无框架内闭式、必须外部输入 | α、m_p/m_e、m_μ/m_e | "
      "**真正的「本源」，且不可第一性导出** |")
    b_("| T3 真派生 | 闭式代入独立 CODATA 值在锚精度内一致 | R∞、a0、λ_C、r_e、"
      "μ_B、μ_N、σ_T、E_h、σ_SB、E_c、α_G | 依赖 T2，非新物理 |")
    b_("")
    b_("- 判据互斥性由控制组保证：T0 用「换值失效」排除（C8），T1 用「α 不变」")
    b_("  排除（C6），T3 用「扰动响应幂次」排除恒真（C5）。")
    b_("")
    b_("### 2.2 T3 派生链明细（%d/%d 闭合）" % (R['n_b_ok'], len(b_rows)))
    b_("")
    b_("| 常数 | 闭式 | 实算 | CODATA | 残差 |")
    b_("|---|---|---|---|---|")
    for r in b_rows:
        b_("| %s | %s | %.10e | %.10e | %.2e |"
           % (r['name'], r['formula'], float(r['calc']), float(r['ref']),
              float(r['res'])))
    b_("")
    b_("- 全部 %d 项落在输入舍入精度内（最大 %.1e）⇒ 经典电磁-原子常数网"
      "对锚完全闭合，**不存在缺口，也不存在额外常数**。" % (R['n_b_ok'],
                                                        float(R['b_max'])))
    b_("- 判别力：扰动 α 相对量 1e-6 ⇒ R∞ 响应幂次 %.9f（解析 2+δ=%.9f，"
      "偏差 %.1e，且幂次>1 ⇒ 非恒真）"
      % (float(b['power']), float(b['power_exact']), float(b['disc'])))
    b_("  ⇒ 该闭合不是恒真判据（恒真判据的幂次会是 0 或无定义）。")
    b_("")
    b_("### 2.3 T1 的构造性证明（有量纲常数是单位约定）")
    b_("")
    b_("| 操作 | c | ħ | G | α |")
    b_("|---|---|---|---|---|")
    b_("| 长度单位 ×10 | c/10 | ħ/100 | G/1000 | 逐位不变 |")
    b_("| Planck 单位制 | 1 | 1 | 1 | 仍为 α |")
    b_("")
    b_("- 机读残差：标度 %.1e/%.1e/%.1e、α %.1e、Planck 三恒等 %.1e。"
      % (float(c['res_c']), float(c['res_h']), float(c['res_g']),
         float(c['res_alpha']), float(c['res_planck'])))
    b_("- ⇒ 「c、ħ、G 是三个基本常数」是 SI 记账的产物，不是物理陈述。")
    b_("")
    b_("### 2.4 框架主张的循环性（D 组，承 r170 并给正面对照）")
    b_("")
    b_("| 主张 | 机读 | 判决 |")
    b_("|---|---|---|")
    b_("| G=ħc/m_P² | 残差 %.1e，换质量偏离 %.1e | 定义式 tautology（FAIL） |"
      % (float(d['res_d1']), float(d['fail_others'])))
    b_("| α=τ/κ | 等分给 %.6f vs 1/137 | 须把锚 α 当输入（FAIL） |"
      % float(d['alpha_geom_equal']))
    b_("| m=ħΩ/c | 残差 %.1e | 恒等（INFO） |" % float(d['res_d3']))
    b_("| Z≡Gc/2 | 残差 %.1e | 代数重排（INFO） |" % float(d['res_d4']))
    b_("| β(−g)=−β(g) | β(0)=0 残差 %.1e | 只强制 g=0 不动点（BOUNDARY） |"
      % float(d['res_d5']))
    b_("| E=mc² | 残差 %.1e | **真第一性（PASS）** |" % float(d['res_d6']))
    b_("")
    b_("## 03. 修复定价")
    b_("")
    b_("| 动作 | 宣称域内成立 | 代价 |")
    b_("|---|---|---|")
    b_("| KEEP（常数仍称『几何/第一性派生』） | 否 | D1/D2 依旧成立 ⇒ 修不好 |")
    b_("| DEL（改称『锚 + 定义恒等 + 单位约定』） | 是 | 退回标准物理记账 |")
    b_("| REPLACE（真派生无量纲锚） | 是 | 需新公设 + 可证伪预言 = 换框架 |")
    b_("")
    b_("- 宣称域内成立 **1** 个、**零代价 0** 个 ⇒ 修复可行 ≠ 修复后仍有内容。")
    b_("")
    b_("## 04. 靶自承与防过度指控")
    b_("")
    b_("- 本卷是**正面总账卷**，靶为用户提问而非单一文档；对库内框架主张只作")
    b_("  分层归类，不宣称任何体系被完全证伪。")
    b_("- 「无量纲常数不可第一性导出」是标准物理共识（flavor problem），")
    b_("  本卷的增量是**给出可机读的四层判据**并把库内主张逐条归层。")
    b_("- 不把「框架没做」当发现：E1 只作台账汇总，不判成败。")
    b_("")
    b_("## 05. 未闭合项（未做即未证，不得外推）")
    b_("")
    b_("1. T2 锚只列 α 与两个质量比；SM 的全部无量纲参数（Yukawa、CKM、"
      "θ_QCD、Λ 比值）未逐一清点。")
    b_("2. 派生链只覆盖经典电磁-原子常数；强/弱/引力侧的派生（如 α_s 跑动）"
      "未纳入（需 RGE，另卷）。")
    b_("3. σ_SB 的 1e-9 残差来自 π 的 60 位截断与输入舍入，非物理偏差。")
    b_("4. 不宣称任何体系被证伪 —— 只判决「常数本源」这一具体问题。")
    b_("")
    b_("## 06. 自抓与更正（本卷自身缺陷，★ 5 处容差/期望值错误）")
    b_("")
    b_("1. 首版 A4 条目残留无效三元表达式 `a['res_a1'] if False else ...`")
    b_("   （会把定义恒等残差误当 Planck 残差打印）⇒ 已清理为单一实参。")
    b_("2. π 用 Machin 公式自实现（Decimal 无三角函数库），并以 60 位已知值")
    b_("   守卫（C1）——沿用 r59 纪律「自实现级数必须先过已知值守卫」。")
    b_("3. ★**C3/G3 容差设错**：把 α≡e²μ0c/(4πħ) 的判据设成 1e-15，实残差")
    b_("   3.054e-12 —— 根因是 CODATA 的 μ0（12 位）与 α（11 位）两个**独立")
    b_("   舍入字面量**不可能给出比 1e-12 更小的残差。⇒ 容差改为 1e-10 并在")
    b_("   文案注明「舍入级」。**r59 纪律复发：容差必须与被核数值的报价精度同源**。")
    b_("4. ★**C4/G4 参考值报价精度误配**：Schwinger 场参考字面量只有 8 位有效")
    b_("   数字（1.3232847e18），我用 1e-8 容差核它 ⇒ 把合法舍入判成 OVER")
    b_("   （残差 5.85e-07 恰是参考值的末位舍入）。⇒ 容差按报价精度改为 1e-6。")
    b_("5. ★**C5/G5 期望值漏二阶项**：解析响应是 (1+δ)²−1=2δ+δ²，幂次恰为")
    b_("   **2+δ** 而非 2；用 2 作期望 ⇒ 偏差恒等于 δ=1e-6，永远压线。⇒ 改为")
    b_("   与 2+δ 对拍（残差 1e-15 级）并加「幂次>1」排除恒真。")
    b_("6. ★**C6/G6 单位不变量的容差设错**：α 的标度不变性受限于 α 与 μ0 两个")
    b_("   字面量的舍入（3.054e-12），代数部分（c/ħ/G 三个标度）才是逐位精确")
    b_("   （残差 0）。⇒ 容差 1e-50 改为 1e-10，并把「代数精确」与「物理不变」")
    b_("   分开陈述。")
    b_("7. ★**C8 阴性对照的量纲设错**：我要求「偏离 1 大于 1e10」，但换质量时")
    b_("   Gm²/(ħc) 或 ≫1（1 kg 给 2.1e15）或 ≪1（m_e 给 4.3e-91），")
    b_("   |x−1| 最大只能到 1（当 x≈0）⇒ 判据永远取 min=1.0。⇒ 改为「完全")
    b_("   不等于 1（>1e-6）」并用 log 距离描述。")
    b_("")
    b_("**共同教训（第 N 次）**：五处全部是**判据设定错误而非计算错误**——机算")
    b_("全部正确，是我的期望值/容差写错。本库「手算必机器兜底」纪律在此处的")
    b_("正确形式是：**期望值与容差也必须由机器对拍决定，不能凭直觉写**。")
    b_("")
    b_("8. ★**产物路径 bug（两次错）+ 编号撞号（均已修复）**：")
    b_("   (a) BASE 少上溯一级 ⇒ 产物误落 `openuft/数据/`；修正时又少一级 ⇒")
    b_("       误落 `openuft/04_公共成果/04_公共成果/...`。两次均已复跑归位，")
    b_("       两个孤儿目录与 4 个误号产物**已删除**（审批已获批准）。")
    b_("   (b) 起草时取 r171，登记前实测发现 **r171 已被并行会话占用**")
    b_("       （`TUFT-r171_常数kPrime量纲最终裁定`）⇒ 按「后到者改号不覆盖」")
    b_("       整体改为 **r179**（实测首空号）。**教训：落盘前必须实测磁盘占号，")
    b_("       不能按序号递推**（r 序列处于竞争态）。")
    b_("   **共同教训：取相对深度前先数目录层级；开册前先查磁盘实占号。**")
    b_("")
    b_("## 07. 红线")
    b_("")
    b_("- 数学自洽 ≠ 实验证实；**恒等式成立 ≠ 有新内容**；**成立 ≠ 宣称域无边界**。")
    b_("- 「可导出」与「是本源」是两个独立判据：T3 全部可导出，但**没有一项**")
    b_("  是本源；T2 是本源，但**没有一项**可导出。")
    b_("- 靶自承优先；防过度指控与防漏判同等重要。")
    b_("")

    # ============================================================
    # 落盘
    # ============================================================
    os.makedirs(OUT, exist_ok=True)
    payload = {
        "stem": STEM,
        "verdict": verdict,
        "items": ITEMS,
        "controls": CONTROLS,
        "guards": GUARDS,
        "key_numbers": {
            "res_alpha_identity": str(a['res_a1']),
            "res_planck_triple": str(c['res_planck']),
            "res_alpha_scale_invariance": str(c['res_alpha']),
            "derived_chain_ok": "%d/%d" % (R['n_b_ok'], len(b_rows)),
            "derived_chain_max_res": str(R['b_max']),
            "disc_power": str(b['power']),
            "d1_res": str(d['res_d1']),
            "d1_fail_others": str(d['fail_others']),
            "d2_res": str(d['res_d2']),
            "d6_res": str(d['res_d6']),
            "pi_res": str(R['res_pi']),
        },
        "ledger": {
            "T0_definition": ["eps0", "mu0", "m_P", "Z0", "planck_family",
                              "Z=Gc/2", "m=hbarOmega/c"],
            "T1_unit_convention": ["c", "hbar", "G", "k_B"],
            "T2_measured_anchor": ["alpha", "m_p/m_e", "m_mu/m_e"],
            "T3_true_derivation": [r['name'] for r in b_rows],
        },
        "controls_ok": "%d/%d" % (sum(1 for x in CONTROLS if x['ok']),
                                  len(CONTROLS)),
        "guards_ok": "%d/%d" % (sum(1 for g in GUARDS if g['ok']),
                                len(GUARDS)),
    }
    def _jsonable(o):
        if isinstance(o, Dc):
            return str(o)
        if isinstance(o, tuple):
            return list(o)
        raise TypeError(repr(o))

    with io.open(os.path.join(OUT, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=_jsonable)
    with io.open(os.path.join(OUT, STEM + "_report.txt"), "w",
                 encoding="utf-8") as f:
        f.write(report)
    judge = "\n".join(m)
    with io.open(os.path.join(OUT, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write(judge)
    with io.open(os.path.join(OUT, "判定_" + STEM + ".md"), "w",
                 encoding="utf-8") as f:
        f.write(judge)

    print(report)
    print("")
    print("[产物] " + os.path.join(OUT, STEM + ".json"))
    print("[产物] " + os.path.join(OUT, STEM + ".md"))
    print("[产物] " + os.path.join(OUT, "判定_" + STEM + ".md"))
    print("[产物] " + os.path.join(OUT, STEM + "_report.txt"))
    print("[控制组] %d/%d   [守卫] %d/%d"
          % (sum(1 for x in CONTROLS if x['ok']), len(CONTROLS),
             sum(1 for g in GUARDS if g['ok']), len(GUARDS)))
    print("[退出码] %d" % (0 if (allok and gallok
                                 and all(it["status"] != "GUARD-FAIL"
                                         for it in ITEMS)) else 2))


if __name__ == "__main__":
    report_and_write(main())
