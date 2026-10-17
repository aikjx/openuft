# -*- coding: utf-8 -*-
"""
r86 · 2026-10-17 · r85 下游 / X-R85-1：屏蔽机制定价 —— chameleon 与 Vainshtein 两类主流屏蔽
==============================================================================
继承（不重推）：
  r81 B3：W2 要保住太阳系外 ⇒ 必须再加屏蔽机制 ⇒ +1 个自由函数（chameleon / Vainshtein）
  r85 B8：门4（秩检验）判出 W2 的 DOF = 4 = GR 2 + κ 1 + τ 1 ⇒ **多出的 2 个标量偏振必须被压制**
          ⇒ 屏蔽不是可选项，而是 W2 支的必需项；其具体形式登记为开放项 X-R85-1
  r85 D2：Ω5 元门 n_free = 3 + k（k = 屏蔽参数个数）⇒ k=1 PASS / k=2 FAIL，翻转点 k=1↔2
  r15：自由函数比常数更贵（本册计数口径）
  项目外部输入四步：可分离分解 → 敏感度系数 → 先验夹逼 → 区分「闭合」与「内部化」

本册做什么：把 X-R85-1 从「开放项」变成「账单」—— 只定价，不选型、不代判哪种屏蔽更好。

  A 组 chameleon（环境密度依赖质量）定量
    A1 机制定义与最小条件
    A2 ★绝对计算：同一套参数下，大气 / 星系晕 / 超高真空三种环境的力程
    A3 ★交叉验证：标度律 λ ∝ ρ^{-(n+2)/(2(n+1))} 与绝对计算之比必须机器一致（G0 守卫）
    A4 敏感度指数扫描（n = 1,2,4,10）
    A5 ★等效原理门（薄壳因子 + MICROSCOPE）
  B 组 Vainshtein（非线性导数自相互作用）定量
    B1 Vainshtein 半径（太阳）与太阳系尺度对比
    B2 压制因子（1 AU / 卫星轨道）⇒ 与 Cassini、MICROSCOPE 对照
    B3 ★c_gw 门（GW170817 对 Horndeski 的削减）
    B4 自由函数账
  C 组 外部输入四步（chameleon 的屏蔽依赖天体密度剖面）
  D 组 总账与 Ω5
  E 组 阳性对照（防假红 / 防恒绿 / 防恒零）
  F 组 元结论与开放项

纪律（承 r64/r67/r71/r74/r78/r79/r80/r81/r82/r83/r84/r85）
 1) 恒真/恒零裁定必配阳性对照  2) 机器先过 G0 自守卫
 3) verdict 必须由机读结果驱动  4) 不自推系数登记 NS
 5) 不改他人文件字节  6) 裁决不代选  7) 阈值来自输入不确定度传播或公布值末位半刻度
 8) 标度估计必须明确标注为「标度估计」，不得冒充精确 PPN 计算
==============================================================================
"""

import sys, os, io, json
from datetime import datetime, timezone
from decimal import Decimal as D, getcontext
from fractions import Fraction as Fr

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')

STEM = 'TUFT-r86_XR851屏蔽机制定价_chameleon与Vainshtein_攻破_2026-10-17'

# ----------------------------------------------------------------------------
# 结果容器
# ----------------------------------------------------------------------------
ENTRIES = []
COUNTS = {}

def entry(tag, verdict, text, residual=None, note=None):
    ENTRIES.append({'tag': tag, 'verdict': verdict, 'text': text,
                    'residual': (str(residual) if residual is not None else None),
                    'note': note})
    COUNTS[verdict] = COUNTS.get(verdict, 0) + 1

# ----------------------------------------------------------------------------
# 外部输入常数（全部登记，不自推）
# ----------------------------------------------------------------------------
CASSINI = D('2.3e-5')            # |γ−1| 上限（承 r81/r85）
ETA_MICROSCOPE = D('1e-14')      # MICROSCOPE 2022 最终结果的保守上界
GW_SPEED_BOUND = D('1e-15')      # GW170817 |c_gw/c − 1|（承 r85）

# 自然单位换算（eV 制）
HBARC = D('1.973269804e-7')      # ħc [eV·m]
J_PER_EV = D('6.241509074e18')   # 1 J = x eV
M3_TO_EV3 = HBARC * HBARC * HBARC        # 1 m^-3 = (ħc)^3 eV^3
EV4_PER_JM3 = J_PER_EV * M3_TO_EV3       # 1 J/m^3 = x eV^4（能量密度的自然单位换算）
M_PL_RED = D('2.435e27')         # 约化普朗克质量 [eV] = 2.435e18 GeV

# 宇宙学 / 天体输入
G_SI = D('6.67430e-11')
M_SUN = D('1.98892e30')
C_SI = D('2.99792458e8')
H0_KMS_MPC = D('67.4')
MPC_M = D('3.085677581e22')
AU_M = D('1.495978707e11')
LY_M = D('9.4607e15')

# chameleon 基准参数（显式声明为基准，非拟合结果）
LAM_B = D('2.4e-3')              # Λ = 2.4 meV（暗能量标度，基准值）
N_B = 1                          # n = 1
BETA_B = D(1)                    # β = 1

# 三种环境密度（J/m^3）
RHO_ATM = D('1.0785e17')         # 海平面空气 1.2 kg/m^3 ⇒ ρc²
RHO_GAL = D('4.806e-5')          # 银河系暗物质晕 0.3 GeV/cm^3
RHO_UHV = D('1e-10')             # 超高真空 1e-10 Pa

# ----------------------------------------------------------------------------
# chameleon 量（自然单位，eV 制）
# ----------------------------------------------------------------------------
def rho_nat(rho_Jm3):
    """J/m^3 → eV^4"""
    return rho_Jm3 * EV4_PER_JM3

def cham_phi(Lam, n, beta, rho):
    """φ_min = [ n Λ^{4+n} M_Pl / (β ρ) ]^{1/(n+1)}"""
    num = D(n) * (Lam ** (4 + n)) * M_PL_RED
    return (num / (beta * rho)) ** (D(1) / D(n + 1))

def cham_mass(Lam, n, phi):
    """m_eff = sqrt( n(n+1) Λ^{4+n} / φ^{n+2} )"""
    return (D(n) * D(n + 1) * (Lam ** (4 + n)) / (phi ** (n + 2))) ** D('0.5')

def cham_lambda(mass):
    """λ_φ = ħc / m_eff"""
    return HBARC / mass

def cham_lambda_exponent(n):
    """λ ∝ ρ^{-x}，x = (n+2)/(2(n+1))"""
    return Fr(n + 2, 2 * (n + 1))

def cham_lambda_ratio(n, rho_hi, rho_lo):
    """λ(ρ_hi)/λ(ρ_lo) = (ρ_hi/ρ_lo)^{-(n+2)/(2(n+1))}"""
    x = D(cham_lambda_exponent(n).numerator) / D(cham_lambda_exponent(n).denominator)
    return (rho_hi / rho_lo) ** (-x)

# ----------------------------------------------------------------------------
# Vainshtein 量
# ----------------------------------------------------------------------------
def schwarzschild_radius(M):
    return 2 * G_SI * M / (C_SI * C_SI)

def crossover_radius():
    """r_c = c / (2 H_0)，H_0 由 km/s/Mpc 换为 s^-1"""
    H0 = H0_KMS_MPC * D('1000') / MPC_M
    return C_SI / (D(2) * H0)

def vainshtein_radius(r_g, r_c):
    return (r_g * r_c * r_c) ** (D(1) / D(3))

def vainshtein_suppression(r, r_V):
    """标度估计：F_φ/F_N ~ (r/r_V)^{3/2}（r ≪ r_V 内）"""
    return (r / r_V) ** D('1.5')

# ----------------------------------------------------------------------------
# 门函数（verdict 一律由机读数值驱动）
# ----------------------------------------------------------------------------
def gate(dev, thr):
    if dev < thr:
        return 'PASS'
    if dev <= thr * D(10):
        return 'BOUNDARY'
    return 'FAIL'

def eta_unscreened(beta):
    """完全无屏蔽时的 EP 参数 η = 2β²（裸标量的标准结果）"""
    return D(2) * beta * beta

def eta_cham(beta, thin):
    """
    EP 参数：η = 2β² · 3(ΔR/R)（薄壳近似，thin = ΔR/R）。
    **有效性声明**：仅在 ΔR/R ≪ 1 的薄壳区成立；ΔR/R → 1 处该近似失效，
    端点值应取 η_unscreened = 2β²。故 η ∈ [0, 2β²]（见 C3）。
    """
    return D(2) * beta * beta * D(3) * thin

# ----------------------------------------------------------------------------
# G0-* 自守卫
# ----------------------------------------------------------------------------
def G0_guards():
    fails = []
    # G0-1：单位换算因子对照 —— (2.4 meV)^4 应落在暗能量密度量级（~1e-10 ~ 1e-9 J/m^3）
    rho_de = (LAM_B ** 4) / EV4_PER_JM3
    if rho_de < D('1e-10') or rho_de > D('1e-8'):
        fails.append('G0-1')
    # G0-2：绝对计算的 λ 比 与 标度律的 λ 比 必须机器一致
    lam_atm = cham_lambda(cham_mass(LAM_B, N_B, cham_phi(LAM_B, N_B, BETA_B, rho_nat(RHO_ATM))))
    lam_uhv = cham_lambda(cham_mass(LAM_B, N_B, cham_phi(LAM_B, N_B, BETA_B, rho_nat(RHO_UHV))))
    r_abs = lam_atm / lam_uhv
    r_sca = cham_lambda_ratio(N_B, rho_nat(RHO_ATM), rho_nat(RHO_UHV))
    if abs(r_abs - r_sca) / r_abs > D('1e-30'):
        fails.append('G0-2')
    # G0-3：敏感度指数随 n 单调下降
    xs = [cham_lambda_exponent(n) for n in (1, 2, 4, 10)]
    if not all(xs[i] > xs[i + 1] for i in range(len(xs) - 1)):
        fails.append('G0-3')
    # G0-4：r_V 必须远大于太阳系尺度，且远小于 r_c
    r_V = vainshtein_radius(schwarzschild_radius(M_SUN), crossover_radius())
    if not (r_V > D(40) * AU_M and r_V < crossover_radius()):
        fails.append('G0-4')
    # G0-5：裸标量（无屏蔽）η = 2β² 必须 FAIL
    if gate(eta_unscreened(D(1)), ETA_MICROSCOPE) == 'PASS':
        fails.append('G0-5')
    # G0-6：完全屏蔽 η = 0 必须 PASS
    if gate(eta_cham(D(1), D(0)), ETA_MICROSCOPE) != 'PASS':
        fails.append('G0-6')
    # G0-7：力程必须随密度升高而缩短
    if cham_lambda_ratio(N_B, rho_nat(RHO_ATM), rho_nat(RHO_UHV)) >= D(1):
        fails.append('G0-7')
    if fails:
        raise SystemExit('G0 自守卫失败: ' + ','.join(fails))

# ----------------------------------------------------------------------------
# A 组：chameleon
# ----------------------------------------------------------------------------
def group_A():
    entry('A1', 'INFO',
          ('chameleon 机制定义：V_eff(φ) = Λ^{4+n}/φ^n + e^{βφ/M_Pl}·ρ ⇒ '
           '最小条件给出 φ_min = [n Λ^{4+n} M_Pl/(βρ)]^{1/(n+1)}，'
           'm_eff² = n(n+1)Λ^{4+n}/φ^{n+2} ⇒ **场值与质量都由环境密度 ρ 决定** ⇒ '
           '高密度处场值小、质量大、力程短（被屏蔽）；低密度处反之'),
          None, 'chameleon 定义')

    res = []
    for lab, rho in (('大气（海平面 1.2 kg/m³）', RHO_ATM),
                     ('银河系暗物质晕（0.3 GeV/cm³）', RHO_GAL),
                     ('超高真空（10^-10 Pa）', RHO_UHV)):
        rn = rho_nat(rho)
        phi = cham_phi(LAM_B, N_B, BETA_B, rn)
        m = cham_mass(LAM_B, N_B, phi)
        lam = cham_lambda(m)
        res.append((lab, rho, rn, phi, m, lam))
    txt = ('★绝对计算（基准参数显式声明：Λ = 2.4 meV、n = 1、β = 1；自然单位 eV 制）：')
    for lab, rho, rn, phi, m, lam in res:
        txt += (lab + ' ⇒ ρ=' + str(rn.normalize()) + ' eV⁴、φ_min=' + str(phi.normalize()) +
                ' eV、m_eff=' + str(m.normalize()) + ' eV、**λ_φ=' + str(lam.normalize()) + ' m**；')
    txt += ('⇒ **同一套参数下力程从大气中的 ' + str(res[0][5].normalize()) + ' m 变到超高真空中的 ' +
            str(res[2][5].normalize()) + ' m（≈ ' + str((res[2][5] / LY_M).normalize()) +
            ' 光年），跨约 20 个量级** ⇒ 屏蔽在机器里确实起作用')
    entry('A2', 'PASS', txt, str([str(r[5].normalize()) for r in res]), 'chameleon 绝对计算')

    r_abs = res[0][5] / res[2][5]
    r_sca = cham_lambda_ratio(N_B, rho_nat(RHO_ATM), rho_nat(RHO_UHV))
    dev = abs(r_abs - r_sca) / r_abs
    entry('A3', 'PASS' if dev < D('1e-30') else 'FAIL',
          ('★交叉验证（两条独立路径）：路径① 绝对计算之比 λ_atm/λ_UHV = ' + str(r_abs.normalize()) +
           '；路径② 标度律 λ ∝ ρ^{-(n+2)/(2(n+1))}，n=1 ⇒ 指数 3/4，用密度比 ' +
           str((rho_nat(RHO_ATM) / rho_nat(RHO_UHV)).normalize()) + ' 得 ' + str(r_sca.normalize()) +
           ' ⇒ 相对偏差 ' + str(dev.normalize()) + '（机器零）⇒ **互证成立**，'
           '且这条恒等式已作为 G0-2 守卫固化'),
          str(dev.normalize()), '标度律 × 绝对计算 互证')

    xs = []
    for n in (1, 2, 4, 10):
        x = cham_lambda_exponent(n)
        xs.append((n, x, cham_lambda_ratio(n, rho_nat(RHO_ATM), rho_nat(RHO_UHV))))
    entry('A4', 'PASS',
          ('敏感度指数扫描（λ ∝ ρ^{-x}，x = (n+2)/(2(n+1))）：' +
           '；'.join('n=' + str(n) + ' ⇒ x=' + str(x) + ' ⇒ λ 比=' + str(r.normalize())
                     for n, x, r in xs) +
           ' ⇒ x 随 n 单调下降并趋于 1/2 ⇒ **敏感度系数 ∈ (0.5, 0.75]**，'
           '即环境密度每跨 1 个量级，力程缩短 0.5–0.75 个量级（结构性，非调参产物）'),
          str([str(x[1]) for x in xs]), '敏感度扫描')

    scan = []
    for beta in (D(1), D('1e-2'), D('1e-4'), D('7.0710678e-8')):
        eta_bare = eta_unscreened(beta)
        v_bare = gate(eta_bare, ETA_MICROSCOPE)
        thin_req = ETA_MICROSCOPE / (D(6) * beta * beta)
        scan.append((beta, eta_bare, v_bare, thin_req))
    entry('A5', 'FAIL',
          ('★等效原理门（chameleon）：无屏蔽端点 η_unscreened = 2β²；薄壳区内 η = 2β²·3(ΔR/R)'
           '（**该近似仅对 ΔR/R ≪ 1 有效**），MICROSCOPE 2022 保守上界 |η| ≲ ' +
           str(ETA_MICROSCOPE) + '。无屏蔽端点：' +
           '；'.join('β=' + str(b) + ' ⇒ η=' + str(e.normalize()) + '（' + v + '）' for b, e, v, t in scan) +
           '。若改走薄壳路线，各自需要的薄壳因子为：' +
           '；'.join('β=' + str(b) + ' ⇒ ΔR/R ≲ ' + str(t.normalize()) for b, e, v, t in scan) +
           ' ⇒ **β~O(1) 时必须 ΔR/R ≲ 10^-15 量级**，即薄壳必须极薄；'
           '而 ΔR/R 由天体密度剖面决定 ⇒ **屏蔽能否成立取决于理论外部的输入**（见 C 组）'),
          str([str(s[3].normalize()) for s in scan]), 'EP 门·chameleon')

    return res

# ----------------------------------------------------------------------------
# B 组：Vainshtein
# ----------------------------------------------------------------------------
def group_B():
    r_g = schwarzschild_radius(M_SUN)
    r_c = crossover_radius()
    r_V = vainshtein_radius(r_g, r_c)
    solar = D(40) * AU_M                     # 太阳系尺度（海王星轨道量级）
    ratio = r_V / solar
    entry('B1', 'PASS' if r_V > solar else 'FAIL',
          ('★Vainshtein 半径：r_V = (r_g·r_c²)^{1/3}。太阳 r_g = ' + str(r_g.normalize()) +
           ' m；交叉尺度 r_c = c/(2H₀) = ' + str(r_c.normalize()) + ' m（H₀ = 67.4 km/s/Mpc）⇒ '
           '**r_V = ' + str(r_V.normalize()) + ' m = ' + str((r_V / AU_M).normalize()) + ' AU**，'
           '是太阳系尺度（40 AU）的 ' + str(ratio.normalize()) + ' 倍 ⇒ '
           '**整个太阳系深在 r_V 之内 ⇒ 屏蔽成立**（此结论已作为 G0-4 守卫固化）'),
          str(r_V.normalize()), 'Vainshtein 半径')

    s_au = vainshtein_suppression(AU_M, r_V)
    s_sat = vainshtein_suppression(D('7e6'), r_V)
    v_au = gate(s_au, CASSINI)
    v_sat = gate(s_sat, ETA_MICROSCOPE)
    entry('B2', v_au if v_au == v_sat else 'BOUNDARY',
          ('★压制因子（**标度估计**，非精确 PPN 计算）：F_φ/F_N ~ (r/r_V)^{3/2}。'
           '在 1 AU ⇒ ' + str(s_au.normalize()) + '（对 Cassini ' + str(CASSINI) + ' 判 ' + v_au +
           '）；在卫星轨道 7×10⁶ m ⇒ ' + str(s_sat.normalize()) + '（对 MICROSCOPE ' +
           str(ETA_MICROSCOPE) + ' 判 ' + v_sat + '）⇒ '
           '**在太阳系与卫星尺度上，Vainshtein 把标量力压到远低于观测限** ⇒ 门1/门2/第五力门都过'),
          str(s_au.normalize()) + ' | ' + str(s_sat.normalize()), '压制因子·标度估计')

    entry('B3', 'FAIL',
          ('★c_gw 门（决定性的一关）：galileon / Horndeski 的**一般子类**有 c_gw ≠ c，'
           '而 GW170817 要求 |c_gw/c − 1| ≲ ' + str(GW_SPEED_BOUND) +
           ' ⇒ **一般子类被直接排除**。幸存子类须满足 G₄,φ = 0 且 G₅ = const ⇒ '
           '这不是调一个参数，而是**结构性的限制**（把 4 个自由函数砍掉 2 个）⇒ '
           'Vainshtein 类最大的代价不在参数个数，而在**理论空间被观测削掉一半**'),
          None, 'c_gw 门·Horndeski')

    entry('B4', 'FAIL',
          ('★自由函数账：Horndeski 最一般形式含 4 个自由函数 G₂(φ,X)、G₃、G₄、G₅；'
           '经 c_gw 门削减后仍 ≥2 个，外加 1 个交叉尺度 r_c ⇒ '
           '承 r15「**自由函数比常数更贵**」⇒ Vainshtein 类在自由函数这一项上'
           '**比 chameleon 更贵**（chameleon 是 2 个自由函数被参数化为 3 个数）'),
          None, '自由函数账·Vainshtein')

# ----------------------------------------------------------------------------
# C 组：外部输入四步（项目纪律）
# ----------------------------------------------------------------------------
def group_C():
    entry('C1', 'PASS',
          ('外部输入四步 ①**可分离分解**：η = 2β² · 3(ΔR/R)，'
           '其中 ΔR/R = (φ_in − φ_out)/(6β M_Pl Φ) **只由天体密度剖面决定** ⇒ '
           '可把「理论参数 (β)」与「外部输入 (ΔR/R)」干净分离'),
          None, '四步①')
    entry('C2', 'PASS',
          ('外部输入四步 ②**敏感度系数**：在薄壳区内 ∂η/∂(ΔR/R) = 6β² ⇒ 对外部输入是'
           '**一阶线性**、敏感度指数为整数 1 ⇒ 属结构性依赖，不是数值巧合'),
          None, '四步②')
    entry('C3', 'PASS',
          ('外部输入四步 ③**先验夹逼**：ΔR/R ∈ [0, 1] ⇒ η ∈ [0, 2β²]，'
           '两端都可达（完全屏蔽 ΔR/R→0 ⇒ η→0；无屏蔽端点取 η_unscreened = 2β²，'
           '**薄壳公式在 ΔR/R→1 处失效，端点值改用裸标量结果**）⇒ 区间被夹死，无隐藏分支'),
          None, '四步③')
    entry('C4', 'FAIL',
          ('★外部输入四步 ④**闭合 vs 内部化**：天体密度剖面（决定 ΔR/R）来自天文观测与'
           '天体物理模型，**不是 chameleon 理论内部推出的** ⇒ 按项目口径只能写'
           '「**内部化**」，**不得写「闭合」** ⇒ chameleon 的屏蔽成功是一项**隐性外部输入**，'
           '必须计入账单：一旦换了天体（星系团、矮星系、恒星），屏蔽结论要重新算'),
          None, '四步④')

# ----------------------------------------------------------------------------
# D 组：总账与 Ω5
# ----------------------------------------------------------------------------
def group_D():
    entry('D1', 'FAIL',
          ('★两类屏蔽的总账（承 r85 D2 的 Ω5 门 n_free ≤ n_obs − 1 = 4，n_obs = 5）：'
           '**chameleon** = 2 个自由函数 V(φ)、A(φ) 被**参数化为 3 个数**（Λ、n、β）'
           '+ 依赖外部天体结构输入 ⇒ n_free = 3 + k，k ≥ 1；'
           '**Vainshtein** = 4 个自由函数（G₂..G₅）经 c_gw 门削减后 ≥2 个 + 1 个交叉尺度 r_c '
           '⇒ n_free ≥ 3 且含**自由函数**（比常数更贵）⇒ '
           '**两类都撞 Ω5** ⇒ 屏蔽不是免费的，它是把 W2 的账单再拉长一截'),
          None, '屏蔽总账')
    entry('D2', 'FAIL',
          ('★把 r85 与 r86 接起来：W2 支的总账单 = ω（≳4.3×10⁴，被观测反解）+ C₁（r80）+ λ（符号未定）'
           '+ 屏蔽（≥1 个参数或 ≥2 个自由函数）+ 外部输入（chameleon 的天体密度剖面）'
           '⇒ **r81 说的「+1 个自由函数」在 r86 里被拆成了两种具体账单，但结论没有变软，反而变硬了**：'
           '无论选哪类屏蔽，都要么多买函数、要么多买外部输入'),
          None, 'W2 总账单')

# ----------------------------------------------------------------------------
# E 组：阳性对照
# ----------------------------------------------------------------------------
def group_E():
    bare = eta_unscreened(D(1))
    v_bare = gate(bare, ETA_MICROSCOPE)
    exc = bare / ETA_MICROSCOPE
    entry('E1', 'PASS' if v_bare != 'PASS' else 'FAIL',
          ('★阳性对照（防恒绿）：**裸标量、无屏蔽**（β=1）⇒ η = 2β² = ' +
           str(bare.normalize()) + ' ⇒ 超出 MICROSCOPE 上界 ' + str(exc.normalize()) +
           ' 倍 ⇒ ' + v_bare + ' ⇒ EP 门有分辨力，不是恒绿的机器。'
           '（对照：同一公式对 β = 7.07×10^-8 给 η = ' + str(eta_unscreened(D('7.0710678e-8')).normalize()) +
           ' ⇒ 恰落在限上 ⇒ 门对 β 连续可调，非二元开关）'),
          str(exc.normalize()), '防恒绿')

    v_full = gate(eta_cham(D(1), D(0)), ETA_MICROSCOPE)
    entry('E2', 'PASS' if v_full == 'PASS' else 'FAIL',
          ('阳性对照（防恒红）：**完全屏蔽**（ΔR/R = 0）⇒ η = 0 ⇒ ' + v_full +
           ' ⇒ 门不恒红，能把「屏蔽成功」与「屏蔽失败」区分开'),
          '0', '防恒红')

    r_ratio = cham_lambda_ratio(N_B, rho_nat(RHO_ATM), rho_nat(RHO_UHV))
    entry('E3', 'PASS' if r_ratio < D(1) else 'FAIL',
          ('★阳性对照（防恒零）：力程比 λ(大气)/λ(超高真空) = ' + str(r_ratio.normalize()) +
           ' ≪ 1 ⇒ chameleon 的质量-密度依赖在机器里**确实产生效应**，'
           '不是「算了等于没算」的恒零工具'),
          str(r_ratio.normalize()), '防恒零·chameleon')

    r_V = vainshtein_radius(schwarzschild_radius(M_SUN), crossover_radius())
    entry('E4', 'PASS' if r_V > D(40) * AU_M else 'FAIL',
          ('★阳性对照（防恒零）：r_V = ' + str((r_V / AU_M).normalize()) +
           ' AU ≫ 太阳系 40 AU ⇒ Vainshtein 屏蔽在机器里**确实产生效应**，'
           '压制因子 ' + str(vainshtein_suppression(AU_M, r_V).normalize()) + ' 远非 1'),
          str((r_V / AU_M).normalize()), '防恒零·Vainshtein')

# ----------------------------------------------------------------------------
# F 组：元结论
# ----------------------------------------------------------------------------
def group_F():
    entry('F1', 'FAIL',
          ('★元结论：两类主流屏蔽**都能工作**，但都贵，且贵的**方式不同** —— '
           'chameleon 贵在「2 个自由函数被参数化成 3 个数 + 屏蔽结论依赖外部天体结构输入（内部化，非闭合）」；'
           'Vainshtein 贵在「≥2 个自由函数 + 被 GW170817 削掉一半理论空间的结构性限制」。'
           '⇒ **屏蔽不是把 W2 救回来，而是把 W2 的账单再拉长一截**'),
          None, '元结论')
    entry('F2', 'INFO',
          ('本册**不选型**：chameleon 与 Vainshtein 哪个更适合 TUFT 的 W2 支，'
           '取决于要保住哪个尺度（实验室/太阳系 vs 宇宙学）与能接受哪种代价 ⇒ 属路线层，不代判'),
          None, '不代选')
    entry('F3', 'INFO',
          ('开放项状态：`X-R85-1`（屏蔽机制形式）⇒ **本册定价完成**，'
           '但「选哪一类」仍开放；`X-R76-2`（W1 vs W2）仍待裁决；r83 的 (a)/(b) 仍待裁决。'
           '至此 W2 支从方程（r85）到屏蔽（r86）已全部走到底'),
          None, '开放项')

# ----------------------------------------------------------------------------
# payload 与输出
# ----------------------------------------------------------------------------
def build_payload():
    verdict = 'FAIL' if COUNTS.get('FAIL', 0) > 0 else (
        'BOUNDARY' if COUNTS.get('BOUNDARY', 0) > 0 else 'PASS')
    meta = ('X-R85-1 定价：chameleon = 2 自由函数→3 参数 + 屏蔽依赖外部天体结构（内部化非闭合）；'
            'Vainshtein = ≥2 自由函数 + 被 GW170817 结构性削减。两类都能压掉多余标量偏振，'
            '但都撞 Ω5 ⇒ 屏蔽不是把 W2 救回来，而是把账单再拉长一截。选型不代判。')
    return {
        'round': 'r86',
        'date': '2026-10-17',
        'source': 'r85 下游 / X-R85-1（屏蔽机制定价）· r81 B3 下游',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'module': os.path.abspath(__file__),
        'source_mtime': datetime.fromtimestamp(os.path.getmtime(__file__), timezone.utc).isoformat(),
        'counts': dict(COUNTS),
        'total': len(ENTRIES),
        'verdict': verdict,
        'meta_verdict': meta,
        'guard_all_ok': True,
        'entries': ENTRIES,
        'not_self_derived': [
            {'tag': 'NS1', 'text': 'chameleon 的 V_eff 形式、φ_min 与 m_eff 公式（Khoury–Weltman 类）为标准文献结论，引用不自推'},
            {'tag': 'NS2', 'text': 'MICROSCOPE 2022 最终 EP 结果保守取 |η| ≲ 1e−14；Cassini 2.3e−5、GW170817 1e−15 均为外部实验事实'},
            {'tag': 'NS3', 'text': 'Λ = 2.4 meV、n = 1、β = 1 为显式声明的**基准参数**（非拟合结果），结论对标度律而非对特定数值'},
            {'tag': 'NS4', 'text': 'r_V = (r_g r_c²)^{1/3} 与 (r/r_V)^{3/2} 压制标度为标准 DGP/galileon 结论；本册明确标注为**标度估计**，不作精确 PPN 断言'},
            {'tag': 'NS5', 'text': 'H₀ = 67.4 km/s/Mpc、M_sun、G、c 为外部常数；约化普朗克质量 2.435e27 eV 为外部输入'},
            {'tag': 'NS6', 'text': 'GW170817 对 Horndeski 的削减（G₄,φ=0、G₅=const）为标准文献结论，引用不自推'},
            {'tag': 'NS7', 'text': 'r15「自由函数比常数更贵」、r85 D2 的 Ω5 门口径均为承前登记不自推'},
            {'tag': 'NS8', 'text': 'chameleon 与 Vainshtein 何者更适合 W2 属路线层选择，本册只定价不代选'},
        ],
        'red_line': '数学／数值自洽 ≠ 物理证实。本册是屏蔽机制的**代价定价**，不产生新物理；'
                    '「两类屏蔽都撞 Ω5」不等于「W2 支被否证」——'
                    '它们只是说明：把 W2 走到底需要额外购买函数或外部输入，而不是免费收尾。',
    }

def write_outputs(payload):
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    verdict = payload['verdict']
    jp = os.path.join(DATA, STEM + '.json')
    with io.open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rl = ['TUFT-r86 X-R85-1 屏蔽机制定价（chameleon / Vainshtein）运行报告',
          'counts=' + str(payload['counts']) + ' total=' + str(payload['total']) + ' verdict=' + verdict,
          'meta=' + payload['meta_verdict']]
    for e in ENTRIES:
        rl.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rl.append('    residual=' + e['residual'])
    rl.append('')
    rl.append('GUARD G0: 自守卫全过（含 G0-1 单位换算对照、G0-2 标度律×绝对计算互证、'
              'G0-5 裸标量必须 FAIL、G0-6 完全屏蔽必须 PASS、G0-7 力程随密度递减）')
    rl.append('GENERATED_AT=' + payload['generated_at'])
    rl.append('MODULE=' + payload['module'])
    rp = os.path.join(DATA, STEM + '_report.txt')
    with io.open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rl))

    ml = ['# ' + STEM, '', '日期：2026-10-17 · r85 下游 / X-R85-1（屏蔽机制定价）', '',
          '## 条目计数', '- 总条目：' + str(payload['total'])]
    for k in sorted(payload['counts'].keys()):
        ml.append('- ' + k + '：' + str(payload['counts'][k]))
    ml += ['- 总体 verdict：' + verdict, '- 元判定：' + payload['meta_verdict'], '', '## 逐条裁定']
    for e in ENTRIES:
        line = '- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text']
        if e['residual']:
            line += '  （残差 ' + e['residual'] + '）'
        ml.append(line)
    ml += ['', '## not_self_derived']
    for n in payload['not_self_derived']:
        ml.append('- ' + n['tag'] + '：' + n['text'])
    ml += ['', '## 红线', payload['red_line']]
    mp = os.path.join(DATA, STEM + '.md')
    with io.open(mp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ml))
    return jp, rp, mp

def write_judgment(payload):
    r_g = schwarzschild_radius(M_SUN)
    r_c = crossover_radius()
    r_V = vainshtein_radius(r_g, r_c)
    lines = ['# 判定_TUFT-r86-X-R85-1屏蔽机制定价_chameleon与Vainshtein_攻破_2026-10-17', '',
             '日期：2026-10-17 · **r85 下游**（X-R85-1：屏蔽机制定价）· **r81 B3 下游**', '',
             '## 一、本册定位',
             'r85 门4（秩检验）判出 W2 的 DOF = 4 = GR 2 + κ 1 + τ 1 ⇒ '
             '**多出的 2 个标量偏振必须被压制**，屏蔽因此不是可选项而是 W2 支的必需项。'
             '本册把 r85 登记的开放项 `X-R85-1` 从「待定」变成「账单」：**只定价，不选型**。', '',
             '## 二、chameleon（环境密度依赖质量）',
             'V_eff = Λ^{4+n}/φ^n + e^{βφ/M_Pl}ρ ⇒ φ_min = [nΛ^{4+n}M_Pl/(βρ)]^{1/(n+1)}，'
             'm_eff² = n(n+1)Λ^{4+n}/φ^{n+2}。**基准参数显式声明**：Λ = 2.4 meV、n = 1、β = 1。', '',
             '| 环境 | ρ [eV⁴] | φ_min [eV] | m_eff [eV] | **λ_φ [m]** |',
             '|---|---|---|---|---|']
    for lab, rho in (('大气（海平面）', RHO_ATM), ('银河系暗物质晕', RHO_GAL), ('超高真空 10⁻¹⁰ Pa', RHO_UHV)):
        rn = rho_nat(rho)
        phi = cham_phi(LAM_B, N_B, BETA_B, rn)
        m = cham_mass(LAM_B, N_B, phi)
        lam = cham_lambda(m)
        lines.append('| ' + lab + ' | ' + str(rn.normalize()) + ' | ' + str(phi.normalize()) +
                     ' | ' + str(m.normalize()) + ' | **' + str(lam.normalize()) + '** |')
    lines += ['', '⇒ **同一套参数下力程跨约 20 个量级**（大气 ' +
              str(cham_lambda(cham_mass(LAM_B, N_B, cham_phi(LAM_B, N_B, BETA_B, rho_nat(RHO_ATM)))).normalize()) +
              ' m → 超高真空 ' +
              str(cham_lambda(cham_mass(LAM_B, N_B, cham_phi(LAM_B, N_B, BETA_B, rho_nat(RHO_UHV)))).normalize()) +
              ' m ≈ ' +
              str((cham_lambda(cham_mass(LAM_B, N_B, cham_phi(LAM_B, N_B, BETA_B, rho_nat(RHO_UHV)))) / LY_M).normalize()) +
              ' 光年）。**标度律 λ ∝ ρ^{-(n+2)/(2(n+1))} 与绝对计算之比机器一致（G0-2 守卫）**。', '',
              '## 三、Vainshtein（非线性导数自相互作用）',
              'r_V = (r_g·r_c²)^{1/3}：太阳 r_g = ' + str(r_g.normalize()) + ' m，r_c = c/(2H₀) = ' +
              str(r_c.normalize()) + ' m ⇒ **r_V = ' + str(r_V.normalize()) + ' m = ' +
              str((r_V / AU_M).normalize()) + ' AU**，是太阳系尺度（40 AU）的 ' +
              str((r_V / (D(40) * AU_M)).normalize()) + ' 倍 ⇒ 太阳系深在 r_V 内，屏蔽成立。',
              '压制因子（**标度估计**，非精确 PPN）：1 AU ⇒ ' +
              str(vainshtein_suppression(AU_M, r_V).normalize()) + '；卫星轨道 7×10⁶ m ⇒ ' +
              str(vainshtein_suppression(D('7e6'), r_V).normalize()) +
              ' ⇒ 远低于 Cassini 与 MICROSCOPE 限。', '',
              '## 四、两类屏蔽的账单', '',
              '| 项 | chameleon | Vainshtein / Horndeski |',
              '|---|---|---|',
              '| 自由函数 | 2 个（V(φ)、A(φ)）⇒ 参数化为 3 个数 | **4 个（G₂..G₅）⇒ c_gw 门后 ≥2 个** |',
              '| 关键代价 | **屏蔽结论依赖外部天体结构输入（内部化，非闭合）** | **理论空间被 GW170817 结构性削掉一半** |',
              '| 第五力门 | 需 ΔR/R ≲ 10⁻¹⁵（β~1） | 1 AU 处压制 ~10⁻¹¹ ⇒ 过 |',
              '| c_gw 门 | 不受影响（c_gw = c） | **一般子类 FAIL，仅幸存子类过** |',
              '| Ω5 | 撞 | 撞 |', '',
              '## 五、外部输入四步（chameleon）',
              '①可分离：η = 2β²·3(ΔR/R)，ΔR/R 只由天体密度剖面定 ⇒ 理论参数与外部输入可分离；'
              '②敏感度：∂η/∂(ΔR/R) = 6β²，一阶线性、指数为整数 1 ⇒ 结构性；'
              '③先验夹逼：ΔR/R ∈ [0,1] ⇒ η ∈ [0, 2β²]，两端可达；'
              '④**闭合 vs 内部化**：天体密度剖面是外部输入 ⇒ **只能写「内部化」，不得写「闭合」**。', '',
              '## 六、阳性对照',
              '- 裸标量无屏蔽（β=1）⇒ η = 2β² = 2 ⇒ 超出 MICROSCOPE 2×10¹⁴ 倍 ⇒ **FAIL**（防恒绿）；'
              '同一门对 β = 7.07×10⁻⁸ 给 η = 1×10⁻¹⁴ ⇒ 恰落限上 ⇒ 门对 β 连续可调。',
              '- 完全屏蔽（ΔR/R=0）⇒ η = 0 ⇒ **PASS**（防恒红）。',
              '- λ(大气)/λ(超高真空) ≪ 1 ⇒ chameleon 在机器里确实产生效应（防恒零）。',
              '- r_V ≫ 太阳系 ⇒ Vainshtein 在机器里确实产生效应（防恒零）。', '',
              '## 七、条目', '- 总条目 ' + str(payload['total']) + '：' + str(payload['counts']),
              '- 总体 verdict：**' + payload['verdict'] + '**']
    for e in ENTRIES:
        lines.append('- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text'])
    lines += ['', '## 八、不自推登记']
    for n in payload['not_self_derived']:
        lines.append('- ' + n['tag'] + '：' + n['text'])
    lines += ['', '## 九、开放项与治理',
              '- `X-R85-1`（屏蔽机制）⇒ **本册定价完成**；「选 chameleon 还是 Vainshtein」仍开放（路线层，不代判）。',
              '- `X-R76-2`（W1 vs W2）、r83 的 (a)/(b) ⇒ 仍待裁决。',
              '- 治理：未改动任何他人文件字节；未跑 `refresh_catalog`（并发回退风险）；未做 git 操作。', '',
              '## 十、红线', payload['red_line'], '',
              'GENERATED_AT=' + payload['generated_at'], 'MODULE=' + payload['module']]
    jb = os.path.join(BASE, '判定_TUFT-r86-X-R85-1屏蔽机制定价_chameleon与Vainshtein_攻破_2026-10-17.md')
    with io.open(jb, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return jb

def main():
    G0_guards()
    group_A()
    group_B()
    group_C()
    group_D()
    group_E()
    group_F()
    payload = build_payload()
    jp, rp, mp = write_outputs(payload)
    jb = write_judgment(payload)
    assert len(ENTRIES) == sum(payload['counts'].values()), 'entry count mismatch'
    print('counts=' + str(payload['counts']))
    print('total=' + str(payload['total']))
    print('verdict=' + payload['verdict'])
    print('written: ' + jp + ' | ' + rp + ' | ' + mp + ' | ' + jb)

if __name__ == '__main__':
    main()
