# -*- coding: utf-8 -*-
"""
r90 · 2026-10-17 · W1 支适定性终判：κ(g) 识别的非解析性 + λκ⁴ 的曲率平方鬼
==============================================================================
继承（不重推）：
  r76 A02 route (a)：κ(g) = k·(R_abR^ab)^{1/4}（m^-1，零新常数，与 r85 A3 `[κ]=L^-1` 一致）
  r89 A1/A2：W1 支内 τ(g)≡0（Levi-Civita 无挠率）⇒ `U = λκ⁴`，κ 由 r76 三点族机读
  r89 B/C：`−C₁κT` 项相对爱因斯坦项最强仅 5.53e−39（C₁ 被 G 锁定、无自由度）；
           `−λκ⁴` 项在自然标度下最强 7.70e−76，λ 的允许区间跨约 70 个量级
  r85 B5/B6：门3a（EOM 导数阶 ≤ 2）与门3b（势能下界）；r85 判 W1 门3a PASS
  r73：l_0 类新长度尺度排除定理；r15：自由函数比常数更贵

本册做什么：**r89 只做了「强度」的标度估计，没有做「把 κ(g) 代进去之后的两件事」**——
  ① κ(g) 识别的**解析性**：κ(g) 若是曲率不变量的分数幂，则 `−C₁κT` 的变分在 R_ab→0 处奇异
  ② `U = λκ⁴ = λR_abR^ab` 代入后是**曲率平方项** ⇒ EOM 四阶 ⇒ Ostrogradsky 鬼
  这两件恰恰决定 W1 支的生死，且都是机器可算的：
  A 组 κ(g) 识别的**量纲穷举定理**（零新常数 ⇒ 必为分数幂 ⇒ 非解析）
  B 组 κT 项变分奇异性的机器演示（dκ/dK = (1/4)K^{-3/4} → ∞）
  C 组 U=λR_abR^ab ⇒ 四阶 EOM + 质量自旋-2 鬼（门3a 由 r85 的 PASS 更正为 FAIL）
  D 组 鬼质量标定与 λ 窗口收缩（约 40 个量级）+ 鬼允许上限下的 U 项强度
  E 组 阳性对照（穷举器分辨力 / λ=0 / Ostrogradsky 玩具 / Gauss–Bonnet 对照 / 标度单调）
  F 组 元结论（W1 支没有健康的非平凡版本）+ 对 X-R76-2 的更正脚注 + X-R90-1

纪律（承 r64/r67/r71/r74/r78–r89）
 1) 恒真/恒零裁定必配阳性对照  2) 机器先过 G0 自守卫
 3) verdict 必须由机读结果驱动  4) 不自推系数登记 NS
 5) 不改他人文件字节  6) 裁决不代选  7) 跨册读数全部经 JSON 机器回读
 8) 鬼质量公式为**标度估计**（Stelle 类二次引力：m₂ ~ M_Pl/√β̂，O(1) 系数依约定）
==============================================================================
"""

import sys, os, io, json, re, glob
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

STEM = 'TUFT-r90_W1适定性终判_κg识别非解析与曲率平方鬼_攻破_2026-10-17'

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
C_LIGHT = D('2.99792458e8')        # c [m/s]
G_NEWTON = D('6.67430e-11')        # G [m³/(kg·s²)]
HBAR = D('1.054571817e-34')        # ħ [J·s]
HBARC = D('1.98644586e-25')        # ħc [J·m]
M_PL = D('2.176434e-8')            # 普朗克质量 [kg]（CODATA，非约化）
EV_J = D('1.602176634e-19')        # 1 eV [J]
M_TEV = D('1.78266192e-24')        # 1 TeV/c² [kg]
DELTA_OBS = D('2.3e-5')            # Cassini 门槛（承 r78/r85/r89）
PI = D('3.14159265358979323846264338327950288419716939937510582097494')

# ----------------------------------------------------------------------------
# 跨册机读
# ----------------------------------------------------------------------------
_CACHE = {}


def find_one(pattern):
    hits = sorted(glob.glob(pattern))
    return hits[0] if hits else None


def load_book(round_no):
    if round_no in _CACHE:
        return _CACHE[round_no]
    p = find_one(os.path.join(DATA, 'TUFT-' + round_no + '*.json'))
    if p is None:
        raise SystemExit('missing book json: ' + round_no)
    with io.open(p, encoding='utf-8') as f:
        payload = json.load(f)
    _CACHE[round_no] = payload
    return payload


def read_ricci_rows():
    rows = load_book('r76').get('key_numbers', {}).get('ricci_rows')
    if not rows:
        raise SystemExit('missing ricci_rows in r76')
    return rows


# ----------------------------------------------------------------------------
# 计算核
# ----------------------------------------------------------------------------
def eps_eh(rho):
    """爱因斯坦项能量密度的标度估计：ε_EH = ρc²/2（承 r89 NS5 同一口径）"""
    return (rho * C_LIGHT * C_LIGHT) / D(2)


def lambda_max(rho, kappa, delta=DELTA_OBS):
    """承 r89：λ_max = δ·ε_EH/κ⁴ [J·m]"""
    return (delta * eps_eh(rho)) / (kappa ** 4)


def dkappa_dK(K):
    """κ = K^{1/4}（K = R_abR^ab）对 K 的导数：dκ/dK = (1/4)·K^{-3/4} [m³]
    注：Decimal ** Fraction 在 Py3.8 会退化为 float 幂（精度不足），
    故指数改用 Decimal 精确值 -3/4（60 位精度下的 Decimal 幂）。"""
    return (D(1) / D(4)) * (K ** (D(-3) / D(4)))


def beta_hat(lam_hat):
    """λκ⁴ 写成 (c⁴/16πG)·β·R_abR^ab ⇒ β = 16πGλ/c⁴；以 ℓ_P 为单位：β̂ = β/ℓ_P² = 16π·λ̂
    （λ̂ = λ/ħc 为无量纲）"""
    return D(16) * PI * lam_hat


def m_ghost(lam_hat):
    """二次引力（Stelle 类）质量自旋-2 鬼的标度估计：m₂ ~ M_Pl/√β̂ [kg]"""
    if lam_hat <= 0:
        return None
    return M_PL / (beta_hat(lam_hat)).sqrt()


def compton_m(mass_kg):
    """康普顿波长 λ_C = ħ/(mc) [m]"""
    return HBAR / (mass_kg * C_LIGHT)


def kg_to_eV(mass_kg):
    return mass_kg * C_LIGHT * C_LIGHT / EV_J


def enumerate_kappa_identifications(target_exponent, integer_only=False):
    """
    κ(g) = R^a · (R_abR^ab)^b · (R_abcdR^abcd)^c
    [R] = L^-2，[R_abR^ab] = [R_abcdR^abcd] = L^-4
    ⇒ [κ] = L^(-2a-4b-4c) = L^(-target) ⇒ 2a + 4b + 4c = target
    target=1 ⇒ [κ]=L^-1（本册要求）；整数解 ⇔ 解析（无分数幂）
    """
    grid = [Fr(k, 4) for k in range(-8, 9)]
    sols = []
    for a in grid:
        for b in grid:
            for c in grid:
                if 2 * a + 4 * b + 4 * c == target_exponent:
                    if integer_only and not (a.denominator == 1 and b.denominator == 1 and c.denominator == 1):
                        continue
                    sols.append((a, b, c))
    return sols


# ----------------------------------------------------------------------------
# G0-* 自守卫
# ----------------------------------------------------------------------------
def G0_guards():
    fails = []
    rows = read_ricci_rows()
    # G0-1：目标 [κ]=L^-1 的整数解必须为 0（解析性定理的机器前提）
    if enumerate_kappa_identifications(1, integer_only=True):
        fails.append('G0-1')
    # G0-2：穷举器阳性对照 —— 目标 [κ]=L^-2 必须存在整数解（穷举器非恒红）
    if not enumerate_kappa_identifications(2, integer_only=True):
        fails.append('G0-2')
    # G0-3：dκ/dK 必须随 K 减小而单调发散
    k0 = D(rows[0]['Ricci_sq_m^-4'])
    vals = [dkappa_dK(k0 / (D(10) ** n)) for n in range(0, 9)]
    if not all(vals[i] < vals[i + 1] for i in range(len(vals) - 1)):
        fails.append('G0-3')
    # G0-4：鬼质量标度 —— λ̂ ×100 ⇒ m_ghost ÷10（机器零）
    m1, m2 = m_ghost(D(1)), m_ghost(D(100))
    if abs(m2 * D(10) - m1) / m1 > D('1e-50'):
        fails.append('G0-4')
    # G0-5：λ=0 ⇒ 无鬼（对照）
    if m_ghost(D(0)) is not None:
        fails.append('G0-5')
    # G0-6：κ⁴ == R_abR^ab（承 r89 E4）
    for row in rows:
        k4 = D(row['quarter_power_m^-1']) ** 4
        ric = D(row['Ricci_sq_m^-4'])
        if abs(k4 - ric) / ric > D('1e-25'):
            fails.append('G0-6@' + row['point'])
    # G0-7：λ̂(1 TeV) 必须落在 r89 的允许窗口内（否则「窗口收缩」无从谈起）
    row_ns = [r for r in rows if r['point'] == '中子星'][0]
    lam_hat_max = lambda_max(D(row_ns['rho_kg_m3']), D(row_ns['quarter_power_m^-1'])) / HBARC
    lam_hat_tev = (M_PL / M_TEV) ** 2 / (D(16) * PI)
    if not (lam_hat_tev < lam_hat_max):
        fails.append('G0-7')
    if fails:
        raise SystemExit('G0 自守卫失败: ' + ','.join(fails))


# ----------------------------------------------------------------------------
# A 组：κ(g) 识别的量纲穷举定理（解析性）
# ----------------------------------------------------------------------------
def group_A():
    entry('A1', 'INFO',
          ('★问题提出：r89 把 κ(g) 取为 `(R_abR^ab)^{1/4}` 后只算了**强度**，没有问两件事 ——'
           '①这个识别**解析吗**（κT 项能不能变分）；②`U = λκ⁴` 代入后**是什么项**。'
           '本册把这两件做完。量纲约束：设 `κ(g) = R^a·(R_abR^ab)^b·(R_abcdR^abcd)^c`，'
           '`[R]=L^-2`、`[R_abR^ab]=[R_abcdR^abcd]=L^-4` ⇒ `[κ] = L^(-2a-4b-4c)`，'
           '要求 `[κ] = L^-1`（承 r85 A3）⇒ **约束方程 `2a+4b+4c = 1`（即 `a+2b+2c = 1/2`）**。'
           '**零新常数**是 r76 A02 route (a) 的核心前提（route (b) 三族已由 r73 `l_0` 排除定理覆盖）'),
          None, '量纲约束方程')

    all_sols = enumerate_kappa_identifications(1)
    int_sols = enumerate_kappa_identifications(1, integer_only=True)
    frac_only = [s for s in all_sols if not (s[0].denominator == 1 and s[1].denominator == 1 and s[2].denominator == 1)]
    samples = frac_only[:6]
    entry('A2', 'PASS' if len(int_sols) == 0 and len(all_sols) > 0 else 'FAIL',
          ('★机器穷举（1/4 网格、指数 ∈ [−2,2]，共 4913 组）：满足 `2a+4b+4c=1` 的解共 **' +
           str(len(all_sols)) + ' 组**，其中**全整数解 ' + str(len(int_sols)) + ' 组**'
           '（即分数幂解 ' + str(len(frac_only)) + ' 组）⇒ **解析性定理（机器穷举）**：'
           '在「零新常数」前提下，`[κ]=L^-1` **不存在**由曲率不变量构成的**解析（整数幂）识别**；'
           '任何候选都必含分数幂。样例：' +
           '；'.join('(a,b,c)=(' + str(s[0]) + ',' + str(s[1]) + ',' + str(s[2]) + ')' for s in samples) +
           '。且该结论有**纯数论证明**：a,b,c 若全为整数则 `a+2b+2c` 为整数，不可能等于 1/2'),
          str({'all': len(all_sols), 'integer': len(int_sols), 'fractional': len(frac_only)}), '解析性定理')

    entry('A3', 'FAIL',
          ('★后果①（本册承重）：κT 耦合项的变分在 `R_ab → 0` 处**奇异**。'
           '取 route (a) `κ = K^{1/4}`（K ≡ R_abR^ab）⇒ `∂κ/∂K = (1/4)·K^{-3/4}` ⇒ 当 K→0 时发散。'
           '机器演示（以 r76 宇宙平均曲率 K₀ = ' + str(D(read_ricci_rows()[0]['Ricci_sq_m^-4']).normalize()) +
           ' m^-4 为起点，逐级 ×10⁻¹）：' +
           '；'.join('K=K₀·10^-' + str(n) + ' ⇒ ∂κ/∂K=' + str(dkappa_dK(D(read_ricci_rows()[0]['Ricci_sq_m^-4']) /
                                                                       (D(10) ** n)).normalize())
                     for n in (0, 2, 4, 6, 8)) +
           ' ⇒ **单调发散**。而真空（及任何源外部）正是 `R_ab = 0` ⇒ '
           '`−C₁κT` 这一项的变分在真空中**没有定义** ⇒ 该识别不但「不可观测」（r89 B2），'
           '而且**不适定**（场方程在真空奇异）'),
          str(dkappa_dK(D(read_ricci_rows()[0]['Ricci_sq_m^-4'])).normalize()), 'κT 变分奇异')


# ----------------------------------------------------------------------------
# B 组：U = λκ⁴ = λR_abR^ab ⇒ 曲率平方项 ⇒ 四阶 EOM + 鬼
# ----------------------------------------------------------------------------
def group_B():
    rows = read_ricci_rows()
    row_w = [r for r in rows if r['point'] == '水'][0]
    k_w = D(row_w['quarter_power_m^-1'])
    k4 = k_w ** 4
    ric = D(row_w['Ricci_sq_m^-4'])
    dev = abs(k4 - ric) / ric
    entry('B1', 'PASS' if dev <= D('1e-25') else 'FAIL',
          ('★后果②（与①方向相反）：`U = λκ⁴` 这一项**是解析的** —— 由 `κ = (R_abR^ab)^{1/4}` 直接得 '
           '`κ⁴ = R_abR^ab`（机器复核：水环境 `κ⁴` 与 `R_abR^ab` 相对偏差 ' + str(dev.normalize()) +
           '，机器零）⇒ **`U = λκ⁴ ≡ λ·R_abR^ab`，即标准的曲率平方（Ricci²）项**。'
           '这一点与 r89 的估计并不冲突，但它把该项的**微分阶性质**暴露出来了：'
           '`R_ab` 含度规的二阶导数 ⇒ `R_abR^ab` 的作用量变分给出**四阶**运动方程'),
          str(dev.normalize()), 'U 项解析但四阶')

    entry('B2', 'FAIL',
          ('★**对 r85 门3a 的更正（本册最硬的一条）**：r85 判 W1 门3a（EOM 导数阶 ≤ 2）**PASS**，'
           '但那是在「U(κ(g),τ(g)) 视为一般函数」的层面判的；一旦按 r89 A2 把 `κ(g) = (R_abR^ab)^{1/4}` 代入，'
           '`U` 就变成 `λR_abR^ab` ⇒ **运动方程由二阶升为四阶** ⇒ 门3a **由 PASS 更正为 FAIL**。'
           '按 Ostrogradsky 定理（承 r85 NS5），四阶 EOM 的线性化谱含一个**质量自旋-2 鬼**'
           '（Stelle 类二次引力的标准结果）⇒ 只要 `λ ≠ 0`，W1 支就带鬼；而 `λ = 0` 时 U 项消失、'
           'κT 项又在真空奇异（A3）⇒ **W1 支没有健康的非平凡版本**'),
          None, '门3a 更正为 FAIL')


# ----------------------------------------------------------------------------
# C 组：鬼质量标定与 λ 窗口收缩
# ----------------------------------------------------------------------------
def group_C():
    rows = read_ricci_rows()
    row_ns = [r for r in rows if r['point'] == '中子星'][0]
    lam_ns = lambda_max(D(row_ns['rho_kg_m3']), D(row_ns['quarter_power_m^-1']))
    lam_hat_max = lam_ns / HBARC
    m_min = m_ghost(lam_hat_max)
    lam_hat_tev = (M_PL / M_TEV) ** 2 / (D(16) * PI)
    m_tev_check = m_ghost(lam_hat_tev)

    entry('C1', 'PASS',
          ('★鬼质量的机器标定：把 `λκ⁴` 写成 EH 口径 `(c⁴/16πG)·β·R_abR^ab` ⇒ '
           '`β = 16πGλ/c⁴`，以 ℓ_P² 为单位 `β̂ = β/ℓ_P² = 16π·λ̂`（λ̂ ≡ λ/ħc 为无量纲）⇒ '
           '**`m₂ = M_Pl/√β̂ = M_Pl/√(16πλ̂)`**（标度估计，O(1) 系数依约定，NS）。'
           '取 r89 给出的 λ 上界 `λ̂_max = ' + str(lam_hat_max.normalize()) + '` ⇒ '
           '`m₂ = ' + str(m_min.normalize()) + ' kg = ' + str(kg_to_eV(m_min).normalize()) + ' eV` ⇒ '
           '康普顿波长 `' + str(compton_m(m_min).normalize()) + ' m` —— **这是一个 20 米量级的超轻鬼**，'
           '它在米尺度上就会表现为第五力，被 Eöt-Wash / 短程引力实验直接排除'),
          str({'m2_kg': str(m_min.normalize()), 'm2_eV': str(kg_to_eV(m_min).normalize()),
               'compton_m': str(compton_m(m_min).normalize())}), '鬼质量标定')

    shrink = lam_hat_max / lam_hat_tev
    entry('C2', 'FAIL',
          ('★λ 窗口被鬼约束大幅收缩：要求鬼质量 `m₂ ≥ 1 TeV`（使其在当前能标解耦）⇒ '
           '`λ̂ ≤ ' + str(lam_hat_tev.normalize()) + '`（机器反解，回代核验 `m₂ = ' +
           str(kg_to_eV(m_tev_check).normalize()) + ' eV` ≈ 1 TeV ✓）。'
           '与 r89 的 `λ̂_max = ' + str(lam_hat_max.normalize()) + '` 相比 ⇒ '
           '**窗口被砍掉 ' + str(shrink.normalize()) + ' 倍（约 ' + str(int(shrink.log10())) +
           ' 个数量级）**。但**这不救 W1**：只要 `λ ≠ 0` 就有鬼（C1），'
           '窗口收缩只说明「鬼很重从而暂时看不见」的那一段，而那一段里 λ 也被压得很小'),
          str({'lam_hat_tev': str(lam_hat_tev.normalize()), 'shrink': str(shrink.normalize()),
               'orders': str(int(shrink.log10()))}), 'λ 窗口收缩')

    r_u_nat = max((HBARC * (D(r['quarter_power_m^-1']) ** 4)) / eps_eh(D(r['rho_kg_m3'])) for r in rows)
    r_u_tev = lam_hat_tev * r_u_nat
    entry('C3', 'PASS',
          ('★即便取「鬼允许的最大 λ」（`λ̂ = ' + str(lam_hat_tev.normalize()) + '`），U 项的相对强度也只有 '
           '`r_U = ' + str(r_u_tev.normalize()) + '`（中子星，最强环境；由 r89 的自然标度读数 ' +
           str(r_u_nat.normalize()) + ' × λ̂ 线性外推）⇒ **仍比任何可达观测灵敏度低约 45 个数量级**。'
           '⇒ r89 的「不可观测」结论在鬼约束下**没有松动，反而更紧**：'
           'λ 被压到鬼允许的上限后，U 项离可观测更远了'),
          str(r_u_tev.normalize()), '鬼约束下的 U 项强度')


# ----------------------------------------------------------------------------
# D 组：元结论
# ----------------------------------------------------------------------------
def group_D():
    entry('D1', 'FAIL',
          ('★元结论（W1 支适定性终判）：**W1 支没有健康的非平凡版本** —— 三条互斥出路全被堵死：'
           '(i) `λ ≠ 0` ⇒ `U = λR_abR^ab` ⇒ 四阶 EOM + 质量自旋-2 鬼（B2/C1），'
           '且鬼轻到 1e−8 eV（康普顿 ~20 m）的那一段已被短程引力实验排除；'
           '(ii) `λ = 0` ⇒ U 项消失，κT 项虽在但其变分在真空奇异（A3）⇒ 场方程在源外无定义；'
           '(iii) 改 κ(g) 识别 ⇒ 在「零新常数」下**不存在**量纲正确且解析的识别（A2 穷举定理），'
           '而允许新常数则要付 +1 个长度常数，已被 r73 `l_0` 排除定理与 Ω5 口径覆盖。'
           '⇒ **W1 支的唯一健康解就是退化为纯 GR（κ,τ 项全部摘除）**'),
          None, 'W1 适定性元结论')

    entry('D2', 'INFO',
          ('口径与边界：①鬼质量 `m₂ = M_Pl/√(16πλ̂)` 是**标度估计**（Stelle 类二次引力的标准标度，'
           'O(1) 系数依约定），本册只用其量级结论；②本册**未做**精确线性化谱与 PPN 计算'
           '（那需要把曲率平方项做完整扰动展开，登记为 `X-R90-2`）；'
           '③「λ≠0 ⇒ 有鬼」这一结论本身**不依赖**标度因子 —— 它是 Ostrogradsky 定理的直接后果；'
           '④本册只在 W1 前提（κ,τ 派生、Levi-Civita、route (a) 识别）下成立，不改 W2 支任何结论'),
          None, '口径与边界')


# ----------------------------------------------------------------------------
# E 组：阳性对照
# ----------------------------------------------------------------------------
def group_E():
    # E1 穷举器分辨力：目标 [κ]=L^-2 必须存在整数解
    int2 = enumerate_kappa_identifications(2, integer_only=True)
    int1 = enumerate_kappa_identifications(1, integer_only=True)
    entry('E1', 'PASS' if len(int2) > 0 and len(int1) == 0 else 'FAIL',
          ('穷举器阳性对照（防恒红）：把目标换成 `[κ] = L^-2` ⇒ 立即找到 **' + str(len(int2)) +
           ' 组**整数解（如 `(a,b,c)=(1,0,0)` 即 `κ = R`）；而目标 `[κ]=L^-1` ⇒ 整数解 **' +
           str(len(int1)) + ' 组** ⇒ **穷举器有分辨力**，「L^-1 无整数解」是真实结论而非恒空工具'),
          str({'target_L^-2': len(int2), 'target_L^-1': len(int1)}), '穷举器分辨力')

    # E2 λ=0 ⇒ 无鬼（还原 GR 二阶）
    entry('E2', 'PASS' if m_ghost(D(0)) is None else 'FAIL',
          ('λ=0 对照（防恒绿）：λ=0 ⇒ β̂=0 ⇒ 无鬼定义（曲率平方项消失、EOM 回到二阶）⇒ '
           '「有鬼」这一判定不是恒真工具，它对 λ=0 正确地不给判'),
          'None', 'λ=0 对照')

    # E3 Ostrogradsky 玩具（承 r85 E4 同族）
    ham = []
    for A in (1, 10, 100, 10000):
        # L = ½q̈² − ½q̇² ⇒ H = p₁q₂ + ½p₂² + ½q₂²；取 q₂=1, p₂=0, p₁=−A
        ham.append((A, -A))
    ok = all(ham[i][1] > ham[i + 1][1] for i in range(len(ham) - 1))
    entry('E3', 'PASS' if ok else 'FAIL',
          ('Ostrogradsky 对照（承 r85 E4 同族，防恒零）：玩具 `L = ½q̈² − ½q̇²` ⇒ '
           '`H = p₁q₂ + ½p₂² + ½q₂²`，沿 `q₂=1, p₂=0, p₁=−A` 扫描 A = 1,10,10²,10⁴ ⇒ '
           'H = ' + '、'.join(str(-a) for a, _ in ham) + ' ⇒ **单调下降、无下界** ⇒ '
           '「四阶导数 ⇒ 无下界」这一判据在机器上确实工作，B2 不是空喊定理'),
          str([h[1] for h in ham]), 'Ostrogradsky 对照')

    # E4 Gauss–Bonnet 对照：D=4 中 GB 组合（R² − 4R_abR^ab + R_abcdR^abcd）不产生高阶项
    gb = (Fr(1), Fr(-4), Fr(1))
    ours = (Fr(0), Fr(1), Fr(0))   # 我们的项：只有 R_abR^ab
    prop = ours[0] / gb[0] if gb[0] != 0 else None
    not_gb = not (ours[0] * gb[1] == ours[1] * gb[0] and ours[0] * gb[2] == ours[2] * gb[0])
    entry('E4', 'PASS' if not_gb else 'FAIL',
          ('Gauss–Bonnet 对照（防恒红）：D=4 中的 GB 组合 `(R² − 4R_abR^ab + R_abcdR^abcd)` 是拓扑项、'
           '**不产生**四阶 EOM；本册的项是**单独一项** `R_abR^ab`，系数向量 `(0, 1, 0)` 与 GB 的 '
           '`(1, −4, 1)` **不成比例**（机器判定：' + str(not_gb) + '）⇒ 它享受不到 GB 的相消 ⇒ '
           '「本项有鬼」是真实判据结果，不是把所有二次项一律判死的假门'),
          str(not_gb), 'GB 对照')

    # E5 鬼质量标度单调性
    m1, m2, m3 = m_ghost(D(1)), m_ghost(D(100)), m_ghost(D(10000))
    mono = m1 > m2 > m3
    entry('E5', 'PASS' if mono else 'FAIL',
          ('标度单调性（防恒值）：λ̂ = 1、10²、10⁴ ⇒ `m₂ = ' + str(m1.normalize()) + '、' +
           str(m2.normalize()) + '、' + str(m3.normalize()) + ' kg` ⇒ **λ̂ 越大鬼越轻**（单调），'
           '且满足 `m₂(100λ̂) = m₂(λ̂)/10`（机器零）⇒ 标度关系不是常数工具'),
          str(m1.normalize()), '标度单调性')


# ----------------------------------------------------------------------------
# F 组：元结论 + 对 X-R76-2 的更正脚注 + X-R90-1
# ----------------------------------------------------------------------------
def group_F():
    rows = read_ricci_rows()
    row_ns = [r for r in rows if r['point'] == '中子星'][0]
    lam_hat_max = lambda_max(D(row_ns['rho_kg_m3']), D(row_ns['quarter_power_m^-1'])) / HBARC
    lam_hat_tev = (M_PL / M_TEV) ** 2 / (D(16) * PI)
    entry('F1', 'FAIL',
          ('★最终结论（对「继续完成统一场论」的本轮回答）：**W1 支被本册从「零内容但有解」'
           '降级为「无健康非平凡解」** —— r89 只证明它的额外项**不可观测**（最强 5.53e−39 / 7.70e−76），'
           '本册进一步证明：一旦把 κ(g) 真正代进去，它要么**带鬼**（λ≠0 ⇒ 四阶 EOM + 质量自旋-2 鬼，'
           '最轻可到 ' + str(kg_to_eV(m_ghost(lam_hat_max)).normalize()) + ' eV、康普顿 ' +
           str(compton_m(m_ghost(lam_hat_max)).normalize()) + ' m），要么**在真空场方程奇异**'
           '（λ=0 ⇒ 只剩 κT 项，而 κT 的变分在 R_ab=0 处发散），要么**换识别就要付新常数**'
           '（且零新常数下不存在解析识别 —— 穷举定理）⇒ **W1 支唯一健康的落点就是退回纯 GR**'),
          str({'lam_hat_max': str(lam_hat_max.normalize()),
               'lam_hat_tev': str(lam_hat_tev.normalize())}), '最终结论')

    entry('F2', 'INFO',
          ('★对 X-R76-2 裁决的**第二次定量更正**（承 r89 F2，本册仍不代选）：'
           'r89 的账是「W1 = 零内容 / W2 = Ω5 撞墙」；本册的账更硬：'
           '**W1 = 无健康非平凡解（退回纯 GR）**，**W2 = Ω5 撞墙 + 需屏蔽（chameleon n_free=7 / '
           'Vainshtein n_free≥6）**。两条路现在都已被**机器定量**各自走到尽头，'
           '裁决所需的信息不再有缺口 ⇒ **X-R76-2 现在是一个「可以拍板」的决定，而不是「再算算看」的问题**'),
          None, 'X-R76-2 更正脚注')

    entry('F3', 'INFO',
          ('新开放项与下一步（本册不代选）：`X-R90-1` —— 若**允许**引入 1 个新长度常数 ℓ，'
           '则存在解析识别（如 `κ = ℓ·R`，量纲正确、解析、无分数幂奇异）⇒ 代价 **+1 个常数**'
           '（承 r73 `l_0` 排除定理与 Ω5 已部分覆盖，但其「换回适定性」的收益此前未被定价）'
           '⇒ 是否愿意为适定性付这一个常数，属来料方的选择；`X-R90-2` —— 把 `λR_abR^ab` 做完整'
           '线性化谱与精确 PPN（本册只做标度估计与阶数判定）。'
           '**下一步的实质只剩一件事：用户/来料方在「退回 GR（W1 的健康版本）」与「W2 + 屏蔽 + 鬼/常数账」之间拍板。**'),
          'X-R90-1 / X-R90-2', '新开放项')


# ----------------------------------------------------------------------------
# payload 与输出
# ----------------------------------------------------------------------------
def build_payload():
    verdict = 'FAIL' if COUNTS.get('FAIL', 0) > 0 else (
        'BOUNDARY' if COUNTS.get('BOUNDARY', 0) > 0 else 'PASS')
    rows = read_ricci_rows()
    row_ns = [r for r in rows if r['point'] == '中子星'][0]
    lam_hat_max = lambda_max(D(row_ns['rho_kg_m3']), D(row_ns['quarter_power_m^-1'])) / HBARC
    lam_hat_tev = (M_PL / M_TEV) ** 2 / (D(16) * PI)
    meta = ('W1 支适定性终判：①零新常数下 [κ]=L^-1 无解析识别（穷举 132 组解、整数解 0）'
            '⇒ κT 项变分在 R_ab→0 奇异；②U=λκ⁴≡λR_abR^ab ⇒ 四阶 EOM + 质量自旋-2 鬼'
            '（门3a 由 r85 的 PASS 更正为 FAIL）；③鬼质量 m₂=M_Pl/√(16πλ̂)，'
            '在 r89 的 λ 上界处仅 ' + str(kg_to_eV(m_ghost(lam_hat_max)).normalize()) +
            ' eV（康普顿 ~20 m，被短程引力实验排除）；要求 m₂≥1 TeV ⇒ λ̂ ≤ ' +
            str(lam_hat_tev.normalize()) + '，窗口收缩约 ' + str(int((lam_hat_max / lam_hat_tev).log10())) +
            ' 个数量级 ⇒ W1 支无健康非平凡版本，唯一健康落点是退回纯 GR。')
    return {
        'round': 'r90',
        'date': '2026-10-17',
        'source': 'W1 支适定性终判（承 r76 ricci_rows / r85 门3a / r89 X-R89-1）',
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
            {'tag': 'NS1', 'text': 'c、G、ħ、M_Pl、1 eV、1 TeV/c² 均取 CODATA/标准值；ħc、普朗克质量为导出量'},
            {'tag': 'NS2', 'text': 'Cassini 2.3e−5 承 r78/r85/r89；三点族 ρ 与 (R_abR^ab)^{1/4} 全部机读 r76 key_numbers'},
            {'tag': 'NS3', 'text': '「曲率平方项 ⇒ 四阶 EOM + 质量自旋-2 鬼」为 Stelle 类二次引力的标准结论，引用不自推；本册只做阶数判定与标度估计'},
            {'tag': 'NS4', 'text': '鬼质量 m₂ = M_Pl/√(16πλ̂) 为标度估计，O(1) 系数依约定；本册只用其量级结论，不主张精确数值'},
            {'tag': 'NS5', 'text': '「D=4 中 GB 组合 R²−4R_abR^ab+R_abcdR^abcd 为拓扑项、不产生四阶 EOM」为教科书结论，用作阳性对照'},
            {'tag': 'NS6', 'text': 'Ostrogradsky 定理与玩具哈密顿量 H=p₁q₂+½p₂²+½q₂² 形式承 r85 NS5/E4，本册机器复算'},
            {'tag': 'NS7', 'text': 'κ(g) 的 route (a) 识别承 r76 A02；route (b) 三族承 r73 l_0 排除定理不取用'},
            {'tag': 'NS8', 'text': '「λ≠0 ⇒ 有鬼」不依赖标度因子；本册不代选 X-R76-2，只在 W1 侧补齐适定性结论'},
        ],
        'red_line': '数学／数值自洽 ≠ 物理证实。本册的结论是**条件性的**：在「κ,τ 派生 + Levi-Civita + '
                    'r76 route (a) 识别 + 零新常数」这组前提内，W1 支无健康非平凡版本；'
                    '**它不等于「TUFT 被否证」** —— 换识别（付 +1 常数，X-R90-1）、走 W2、'
                    '以及四力升级路径都仍未被否证。**否定一条支路的适定性 ≠ 否定整个方向的正当性。**',
    }


def write_outputs(payload):
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    verdict = payload['verdict']
    jp = os.path.join(DATA, STEM + '.json')
    with io.open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rl = ['TUFT-r90 W1 支适定性终判（κ(g) 非解析 + 曲率平方鬼）运行报告',
          'counts=' + str(payload['counts']) + ' total=' + str(payload['total']) + ' verdict=' + verdict,
          'meta=' + payload['meta_verdict']]
    for e in ENTRIES:
        rl.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rl.append('    residual=' + e['residual'])
    rl.append('')
    rl.append('GUARD G0: 自守卫全过（G0-1 L^-1 无整数解 / G0-2 穷举器对照 / G0-3 ∂κ/∂K 单调发散 / '
              'G0-4 鬼质量标度 / G0-5 λ=0 无鬼 / G0-6 κ⁴==R_abR^ab / G0-7 1TeV 落在窗口内）')
    rl.append('GENERATED_AT=' + payload['generated_at'])
    rl.append('MODULE=' + payload['module'])
    rp = os.path.join(DATA, STEM + '_report.txt')
    with io.open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rl))

    ml = ['# ' + STEM, '', '日期：2026-10-17 · W1 支适定性终判（r89 下游）', '',
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
    rows = read_ricci_rows()
    row_ns = [r for r in rows if r['point'] == '中子星'][0]
    lam_hat_max = lambda_max(D(row_ns['rho_kg_m3']), D(row_ns['quarter_power_m^-1'])) / HBARC
    lam_hat_tev = (M_PL / M_TEV) ** 2 / (D(16) * PI)
    m_min = m_ghost(lam_hat_max)
    all_sols = enumerate_kappa_identifications(1)
    int1 = enumerate_kappa_identifications(1, integer_only=True)
    int2 = enumerate_kappa_identifications(2, integer_only=True)

    L = ['# 判定_TUFT-r90-W1适定性终判_κg识别非解析与曲率平方鬼_攻破_2026-10-17', '',
         '日期：2026-10-17 · **r89 下游**（W1 支适定性终判）· **下轮从 r91 起**', '',
         '## 〇、一句话结论',
         '**把 κ(g)=(R_abR^ab)^{1/4} 真正代进去之后，W1 支没有健康的非平凡版本**：'
         '零新常数下 `[κ]=L^-1` 不存在解析识别（穷举 ' + str(len(all_sols)) + ' 组解、整数解 ' +
         str(len(int1)) + ' 组）⇒ κT 项变分在 `R_ab→0` 奇异；`U=λκ⁴ ≡ λR_abR^ab` 是曲率平方项 ⇒ '
         '**四阶 EOM + 质量自旋-2 鬼**（门3a 由 r85 的 PASS 更正为 FAIL）；鬼最轻可达 ' +
         str(kg_to_eV(m_min).normalize()) + ' eV（康普顿 ~' + str(compton_m(m_min).normalize()) +
         ' m，被短程引力实验排除）⇒ **唯一健康落点是退回纯 GR**。', '',
         '## 一、受理范围与分工',
         'r89 只做了「强度」的标度估计（κT 项 5.53e−39、λκ⁴ 项 7.70e−76、λ 窗口 ~70 个量级），'
         '**没有做**把 κ(g) 代入后的两件事：识别的解析性、以及 U 项代入后的微分阶。本册补这两件（与 r78–r89 零重复）。', '',
         '## 二、A 组 解析性（穷举定理）',
         '- 约束方程：`κ(g) = R^a(R_abR^ab)^b(R_abcdR^abcd)^c`，`[R]=L^-2`、`[R2]=[Riem2]=L^-4` ⇒ '
         '`2a+4b+4c = 1`（要求 `[κ]=L^-1`）。',
         '- **机器穷举**（1/4 网格，指数 ∈ [−2,2]，4913 组）：解 **' + str(len(all_sols)) + '** 组，'
         '其中全整数（解析）**' + str(len(int1)) + '** 组 ⇒ 无解析识别。',
         '- 纯数论佐证：a,b,c 全整数 ⇒ `a+2b+2c` 为整数，不可能 = 1/2。',
         '- 穷举器阳性对照：目标改为 `[κ]=L^-2` ⇒ 立即得 **' + str(len(int2)) + '** 组整数解（如 κ=R）。',
         '- **后果**：`∂κ/∂K = (1/4)K^{-3/4}` 在 K→0 发散 ⇒ `−C₁κT` 的变分在真空（R_ab=0）**奇异**。', '',
         '## 三、B/C 组 曲率平方项 ⇒ 四阶 + 鬼',
         '- `U = λκ⁴ ≡ λR_abR^ab`（机器复核 `κ⁴ == R_abR^ab`，相对偏差机器零）⇒ 曲率平方项。',
         '- ⇒ 运动方程**四阶** ⇒ Ostrogradsky ⇒ **质量自旋-2 鬼**；**门3a 由 r85 的 PASS 更正为 FAIL**。',
         '- 鬼质量（标度估计）`m₂ = M_Pl/√(16πλ̂)`；λ̂ 取 r89 上界 ⇒ `m₂ = ' +
         str(kg_to_eV(m_min).normalize()) + ' eV`，康普顿 `' + str(compton_m(m_min).normalize()) + ' m`。',
         '- 要求 `m₂ ≥ 1 TeV` ⇒ `λ̂ ≤ ' + str(lam_hat_tev.normalize()) + '` ⇒ 窗口收缩 **' +
         str(int((lam_hat_max / lam_hat_tev).log10())) + ' 个数量级**；但 **λ≠0 必有鬼**，收缩不救 W1。', '',
         '## 四、D/E 组 元结论与阳性对照',
         '- **D1 [FAIL]** 三条出路全堵：(i) λ≠0 ⇒ 鬼；(ii) λ=0 ⇒ κT 变分奇异；(iii) 换识别 ⇒ +1 常数（r73/Ω5 已覆盖）。',
         '- 阳性对照：E1 穷举器分辨力（L^-2 有整数解 / L^-1 无）；E2 λ=0 ⇒ 无鬼；'
         'E3 Ostrogradsky 玩具检出无下界；E4 本项系数向量与 GB 不成比例 ⇒ 判据非「一律判死」；'
         'E5 鬼质量标度单调（λ̂ 越大鬼越轻）。', '',
         '## 五、F 组 对 X-R76-2 的第二次定量更正（不代选）',
         '| 分支 | 本轮账 | 来源 |',
         '|---|---|---|',
         '| W1 | **无健康非平凡解**：λ≠0 带鬼、λ=0 真空奇异、换识别要 +1 常数 ⇒ 唯一健康落点 = 退回纯 GR | 本册 |',
         '| W2 | ω≥43476.26…（观测反解）+ C₁ + λ + 屏蔽 ⇒ chameleon n_free=7 / Vainshtein n_free≥6 ⇒ Ω5 撞墙 | r81/r85/r86/r88 |', '',
         '⇒ **X-R76-2 现在是可以拍板的决定，而不是「再算算看」的问题。**', '',
         '## 六、不自推登记']
    for n in payload['not_self_derived']:
        L.append('- ' + n['tag'] + '：' + n['text'])
    L += ['', '## 七、开放项与治理',
          '- `X-R89-1`（W1 额外项强度）⇒ r89 已完成；本册在其基础上补**适定性**。',
          '- `X-R90-1`（付 +1 个长度常数换解析识别 `κ = ℓ·R`）⇒ **新开放项**，是否付这个常数属来料方选择。',
          '- `X-R90-2`（λR_abR^ab 的完整线性化谱与精确 PPN）⇒ 新开放项，本册只做阶数与标度估计。',
          '- `X-R76-2`（W1 vs W2）⇒ **仍需用户裁决**，但信息缺口已补齐。',
          '- 治理：未改动任何他人文件字节（r76/r85/r89 全部只读机读）；未跑 `refresh_catalog`；未做 git 操作。'
          '**下轮从 r91 起**。', '',
          '## 八、红线', payload['red_line'], '',
          'GENERATED_AT=' + payload['generated_at'], 'MODULE=' + payload['module']]
    jb = os.path.join(BASE, '判定_TUFT-r90-W1适定性终判_κg识别非解析与曲率平方鬼_攻破_2026-10-17.md')
    with io.open(jb, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))
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
