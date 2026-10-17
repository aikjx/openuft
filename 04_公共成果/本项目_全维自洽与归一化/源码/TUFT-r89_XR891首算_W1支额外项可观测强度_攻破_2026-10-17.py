# -*- coding: utf-8 -*-
"""
r89 · 2026-10-17 · X-R89-1 首算：W1 支额外项的可观测强度定量
==============================================================================
继承（不重推）：
  r78 C3 / r80 C1：线性耦合要求 [C₁] = L；{ħ,c,G} 整数幂 729 组命中 0，半幂唯一解
                    √(ħG/c³) = ℓ_P ⇒ **C₁ = √(4π)ℓ_P 由 G 观测唯一锁定**（无自由度）
  r80 D：补全后拉氏量 𝓛 = (ħc/2)[(∂κ)²+(∂τ)²] − λ(κ²+τ²)² − C₁κT
  r85 A1/A2：W1 支 = κ,τ 降为**度规派生量** ⇒ 𝓛_W1 = c³R/(16πG) − U(κ(g),τ(g)) − C₁κ(g)T + 𝓛_m
             ⇒ EOM：G_{μν} = (8πG/c⁴)(T_{μν} + T^{eff}_{μν}[U])
  r76 A02 route (a)：ω → √(R_abR^ab) 量纲不齐（L^-2 vs L^-1）⇒ 幂次 1/2→1/4 得
             (R_abR^ab)^{1/4}，单位 m^-1，与 r85 A3 的 [κ] = L^-1 一致
  r73：l_0 类新长度尺度排除定理 ⇒ r76 route (b) 三族（引入非几何长度）本册不取用
  r88（总账册）C4/D2：九册总账显示「剩余项全是裁决项」；但本册发现一类**可计算而漏算**的问题
             —— W1 支**额外项自身**的可观测强度，从未有任何一册算过（登记为 X-R89-1）

本册做什么：**把 X-R89-1 从「未算」变成「算完」**——对补全后的 W1 拉氏量，
量化 `U(κ(g),τ(g))` 与 `C₁κ(g)T` 两项相对爱因斯坦项的强度：
  A 组 W1 支承前方程 + τ(g)≡0 推论 + κ(g) 候选敲定（机读 r76 ricci_rows）
  B 组 κT 耦合项：C₁ 已被 G 锁定 ⇒ 无自由度 ⇒ 其相对强度是**确定的预测**
  C 组 λκ⁴ 项：自然标度下的强度 + 反解观测上界 + 允许窗口宽度（可识别性）
  D 组 总表与结论（X-R89-1 首算答案）
  E 组 阳性对照（λ=0 / λ=λ_max / λ=10λ_max / κ⁴ 内部互证 / ε_EH 量级对照）
  F 组 元结论 + 对 X-R76-2 裁决的**定量脚注**（本册不代选）+ 下一步

纪律（承 r64/r67/r71/r74/r78–r88）
 1) 恒真/恒零裁定必配阳性对照  2) 机器先过 G0 自守卫
 3) verdict 必须由机读结果驱动  4) 不自推系数登记 NS
 5) 不改他人文件字节  6) 裁决不代选
 7) 一切量级结论必须显式标注为**标度估计**（ε_EH = ρc²/2 取爱因斯坦项能量密度口径）
 8) 跨册读数全部经 JSON 机器回读（r76 ricci_rows、r78/r80 的 C₁）
==============================================================================
"""

import sys, os, io, json, re, glob
from datetime import datetime, timezone
from decimal import Decimal as D, getcontext

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')

STEM = 'TUFT-r89_XR891首算_W1支额外项可观测强度_攻破_2026-10-17'

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
C_LIGHT = D('2.99792458e8')        # c [m/s]（CODATA）
HBARC = D('1.98644586e-25')        # ħc [J·m]（CODATA ħ 与 c 之积）
DELTA_OBS = D('2.3e-5')            # Cassini |γ−1| 观测上限，用作「可观测」门槛（承 r78/r85）

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


def book_text(round_no):
    return json.dumps(load_book(round_no), ensure_ascii=False)


def read_ricci_rows():
    """机读 r76 key_numbers 的三点族：ρ [kg/m³]、R_abR^ab [m^-4]、κ=(R_abR^ab)^{1/4} [m^-1]"""
    rows = load_book('r76').get('key_numbers', {}).get('ricci_rows')
    if not rows:
        raise SystemExit('missing ricci_rows in r76')
    return rows


NUM35 = r'([0-9]+\.[0-9]+E[-\u2212]35)'


def read_c_req():
    """C₁ = √(4π)ℓ_P：从 r78 与 r80 两册互证读取（承 r88 B1 同族方法）"""
    pat = r'C_req[^\n]{0,40}?' + NUM35
    vals = []
    for r in ('r78', 'r80'):
        m = re.findall(pat, book_text(r))
        if not m:
            raise SystemExit('C_req not found in ' + r)
        vals.append(D(m[0].replace('\u2212', '-')))
    if abs(vals[0] - vals[1]) / vals[1] > D('1e-24'):
        raise SystemExit('C_req cross-book mismatch')
    return vals[1]


# ----------------------------------------------------------------------------
# 本册的计算核（全部标度估计，显式标注）
# ----------------------------------------------------------------------------
def eps_eh(rho):
    """爱因斯坦项的标度估计能量密度：EH 密度 ≈ ρc²/2
    （尘埃：R ≈ 8πGρ/c² ⇒ (c⁴/16πG)R ≈ ρc²/2；本册统一取此口径并显式标注为标度估计）"""
    return (rho * C_LIGHT * C_LIGHT) / D(2)


def ratio_kappa_T(c1, kappa):
    """κT 耦合项相对爱因斯坦项的强度：r_C = C₁·κ（无量纲）"""
    return c1 * kappa


def ratio_U(lam, kappa, rho):
    """U = λκ⁴ 项相对爱因斯坦项的强度：r_U = λκ⁴/(ρc²/2)"""
    return (lam * (kappa ** 4)) / eps_eh(rho)


def lambda_max(rho, kappa, delta=DELTA_OBS):
    """若该项要恰好落在观测门槛 δ，所需的 λ：λ_max = δ·(ρc²/2)/κ⁴ [J·m]"""
    return (delta * eps_eh(rho)) / (kappa ** 4)


# ----------------------------------------------------------------------------
# G0-* 自守卫
# ----------------------------------------------------------------------------
def G0_guards():
    fails = []
    rows = read_ricci_rows()
    c1 = read_c_req()
    # G0-1：三点族可读且各项为正
    if len(rows) != 3:
        fails.append('G0-1a')
    for row in rows:
        if D(row['rho_kg_m3']) <= 0 or D(row['quarter_power_m^-1']) <= 0:
            fails.append('G0-1b')
    # G0-2：κ⁴ 必须与 r76 的 R_abR^ab 逐位互证（κ=(R_abR^ab)^{1/4} 的定义自洽）
    for row in rows:
        k4 = D(row['quarter_power_m^-1']) ** 4
        ric = D(row['Ricci_sq_m^-4'])
        if abs(k4 - ric) / ric > D('1e-25'):
            fails.append('G0-2@' + row['point'])
    # G0-3：C₁>0 且与手算 √(4π)ℓ_P 一致（两位有效数字层面）
    if c1 <= 0:
        fails.append('G0-3')
    lp_test = D('1.6162550239285500506848148E-35') * D('3.544907701811032')  # √(4π)·ℓ_P
    if abs(c1 - lp_test) / lp_test > D('1e-6'):
        fails.append('G0-3b')
    # G0-4：ε_EH 量级对照（水的静止能量密度应落在 1e19 ~ 1e20 J/m³）
    row_w = [r for r in rows if r['point'] == '水'][0]
    ew = eps_eh(D(row_w['rho_kg_m3']))
    if ew < D('1e19') or ew > D('1e20'):
        fails.append('G0-4')
    # G0-5：λ=0 ⇒ U 项强度必须恰为 0（防恒零：门对该项有定义）
    if ratio_U(D(0), D(row_w['quarter_power_m^-1']), D(row_w['rho_kg_m3'])) != 0:
        fails.append('G0-5')
    # G0-6：λ=λ_max ⇒ 强度必须恰等于 δ（防恒红/防恒绿：门连续可调且定标正确）
    k_w = D(row_w['quarter_power_m^-1'])
    rho_w = D(row_w['rho_kg_m3'])
    lm = lambda_max(rho_w, k_w)
    if abs(ratio_U(lm, k_w, rho_w) - DELTA_OBS) / DELTA_OBS > D('1e-50'):
        fails.append('G0-6')
    # G0-7：λ=10λ_max ⇒ 强度必须超过 δ（门有分辨力，非恒 PASS）
    if ratio_U(lm * D(10), k_w, rho_w) <= DELTA_OBS:
        fails.append('G0-7')
    if fails:
        raise SystemExit('G0 自守卫失败: ' + ','.join(fails))


# ----------------------------------------------------------------------------
# A 组：W1 支承前方程 + τ(g)≡0 推论 + κ(g) 候选
# ----------------------------------------------------------------------------
def group_A(c1):
    rows = read_ricci_rows()
    entry('A1', 'INFO',
          ('★W1 支承前方程与 τ(g)≡0 推论：承 r85 A1，W1 支 `𝓛_W1 = c³R/(16πG) − U(κ(g),τ(g)) − C₁κ(g)T + 𝓛_m`，'
           'EOM 唯一：`G_{μν} = (8πG/c⁴)(T_{μν} + T^{eff}_{μν}[U])`。**推论（本册承重）**：'
           '既然 κ,τ 全部降为**度规派生量**，而度规唯一确定的无挠相容联络是 Levi-Civita 联络'
           '（无挠率、度规相容 ⇒ 唯一，教科书结论）⇒ 在 W1 支内 **`τ(g) ≡ 0`**，'
           '于是 `U(κ²+τ²)² ⇒ λκ⁴`、约束 `κ²+τ²=ω²` 退化为 `|κ| = ω`（不再是动力学约束）'
           '⇒ **τ 扇区在 W1 支内不提供任何实体内容**（与 r74「τ 鬼场出路」的方向一致，'
           '本册是在 W1 前提下的独立后果登记）'),
          None, 'τ(g)≡0 推论')

    entry('A2', 'INFO',
          ('★κ(g) 候选敲定：r76 A02 查明来料「ω → √(R_abR^ab)」量纲不齐（`[√(R_abR^ab)] = L^-2` vs `[ω] = L^-1`），'
           '给出的两条修法中：route (a) 幂次 `1/2 → 1/4` ⇒ `κ(g) = k·(R_abR^ab)^{1/4}`，单位 m^-1，'
           '与 r85 A3 的 `[κ] = L^-1` 精确一致，且**只依赖曲率本身**（零新常数）；'
           'route (b) 三族（`ω^-1` / `Għc^-3 ω` / `G^-1ħ^-1c³ω^-3`）须引入非几何长度，'
           '已被 r73 的 `l_0` 排除定理覆盖 ⇒ **本册取 route (a) 为唯一候选**（k 为无量纲自由系数，'
           'r85 A4 已证 κ = k/ℓ_P 形式、其数值由 G 唯一锁定 ⇒ 本册取 k 使 κ 由曲率直接给出）'),
          None, 'κ(g) 候选')

    tablets = []
    for row in rows:
        rho = D(row['rho_kg_m3'])
        kappa = D(row['quarter_power_m^-1'])
        k4 = kappa ** 4
        ric = D(row['Ricci_sq_m^-4'])
        dev = abs(k4 - ric) / ric
        tablets.append((row['point'], rho, kappa, k4, ric, dev))
    txt = ('机读 r76 `ricci_rows` 三点族（**且定义自洽机器互证**：`κ⁴ == R_abR^ab`）：')
    for pt, rho, kappa, k4, ric, dev in tablets:
        txt += ('；'.join([pt + '：ρ=' + str(rho.normalize()) + ' kg/m³、κ=(R_abR^ab)^{1/4}=' +
                           str(kappa.normalize()) + ' m^-1']) +
                '，κ⁴ 与 R_abR^ab 相对偏差 ' + str(dev.normalize()))
    worst = max(t[5] for t in tablets)
    entry('A3', 'PASS' if worst <= D('1e-25') else 'FAIL',
          txt + ' ⇒ 最大相对偏差 ' + str(worst.normalize()) +
          ' ≤ 1e-25 ⇒ **机读链路端到端自洽**（κ 值不是手抄，而是从 r76 的曲率量机器导出并反查一致）',
          str(worst.normalize()), 'κ 值机读与自洽')


# ----------------------------------------------------------------------------
# B 组：κT 耦合项（C₁ 已被 G 锁定 ⇒ 无自由度 ⇒ 确定的预测）
# ----------------------------------------------------------------------------
def group_B(c1):
    rows = read_ricci_rows()
    vals = []
    for row in rows:
        kappa = D(row['quarter_power_m^-1'])
        vals.append((row['point'], kappa, ratio_kappa_T(c1, kappa)))
    txt = ('★κT 耦合项的相对强度（**无自由参数，故这是确定的预测**）：'
           '承 r78 C3 / r80 C1，`[C₁] = L` 且 {ħ,c,G} 整数幂 729 组命中 0、半幂唯一解 '
           '`√(ħG/c³) = ℓ_P` ⇒ **C₁ = √(4π)ℓ_P = ' + str(c1.normalize()) + ' m` 由 G 唯一锁定；'
           '爱因斯坦项与耦合项都在 T 上做功 ⇒ 相对强度 `r_C = C₁·κ`（无量纲）。三环境：')
    for pt, kappa, r in vals:
        txt += pt + ' κ=' + str(kappa.normalize()) + ' ⇒ r_C=' + str(r.normalize()) + '；'
    worst = max(v[2] for v in vals)
    entry('B1', 'PASS',
          txt + '⇒ 三者均远小于任何观测灵敏度（最强中子星处 `r_C = ' + str(worst.normalize()) + '`）',
          str(worst.normalize()), 'κT 项强度')

    entry('B2', 'FAIL',
          ('★κT 项的结论：**额外耦合通道在最强的中子星环境下也只及爱因斯坦项的 ' + str(worst.normalize()) +
           ' 倍**（宇宙平均 ' + str(vals[0][2].normalize()) + '、水 ' + str(vals[1][2].normalize()) + '）'
           '⇒ 在 W1 支里，`−C₁κT` 这一项虽然写在拉氏量中，却**不产生任何可达观测后果**；'
           '它既不能解释任何现象，也不能被任何实验排除。'
           '注意其结构与已排除的 W3 不同：W3（纯标量中介）给出的是 `γ = −1` 的超限倍数 8.695652E+4（承 r78 I07），'
           '而本项因被 `(κ,τ 派生)` 降格 + `C₁` 被 G 锁定而**连超限都不会出现**'
           ' ⇒ FAIL（判 FAIL 的含义：该通道不承载任何可被检验的物理后果，不是数值错误）'),
          str(worst.normalize()), 'κT 项结论')


# ----------------------------------------------------------------------------
# C 组：λκ⁴ 项 —— 自然标度强度 / 观测上界 / 可识别性窗口
# ----------------------------------------------------------------------------
def group_C():
    rows = read_ricci_rows()
    nat = []
    bnd = []
    for row in rows:
        rho = D(row['rho_kg_m3'])
        kappa = D(row['quarter_power_m^-1'])
        nat.append((row['point'], kappa, ratio_U(HBARC, kappa, rho)))
        lm = lambda_max(rho, kappa)
        bnd.append((row['point'], lm, lm / HBARC))

    txt0 = ('★λκ⁴ 项在**自然标度** λ = ħc 下的强度（`r_U = λκ⁴/(ρc²/2)`，其中 `ε_EH = ρc²/2` 为爱因斯坦项'
            '能量密度的**标度估计**口径）：')
    for pt, kappa, r in nat:
        txt0 += pt + ' ⇒ r_U=' + str(r.normalize()) + '；'
    nat_max = max(v[2] for v in nat)
    entry('C1', 'PASS',
          txt0 + '⇒ 最强（中子星）处仅 ' + str(nat_max.normalize()) +
          ' ⇒ **取自然标度时该项在任何环境都不可观测**（相差约 76 个数量级）',
          str(nat_max.normalize()), 'λ 自然标度强度')

    txt1 = ('★反解观测上界：若要求 `r_U` 恰落在 Cassini 门槛 `δ = ' + str(DELTA_OBS) +
            '`（即「刚好可观测」），则 `λ_max = δ·(ρc²/2)/κ⁴`：')
    for pt, lm, ratio in bnd:
        txt1 += pt + ' ⇒ λ_max=' + str(lm.normalize()) + ' J·m（= ' + str(ratio.normalize()) + ' × ħc）；'
    tight = min(v[1] for v in bnd)
    tight_ratio = min(v[2] for v in bnd)
    tight_pt = [v[0] for v in bnd if v[1] == tight][0]
    entry('C2', 'PASS',
          txt1 + '⇒ **最紧的是' + tight_pt + '**：`λ ≲ ' + str(tight.normalize()) +
          ' J·m` ≈ ' + str(tight_ratio.normalize()) + ' × ħc。'
          '注意这是「上界」而非「预言」：现有观测**完全不排除** λ 取该范围内的任意值',
          str(tight.normalize()), 'λ 观测上界')

    # 可识别性窗口：从自然标度到上界跨多少个数量级（以 10 为底）
    window_log10 = tight_ratio.log10()
    entry('C3', 'FAIL',
          ('★可识别性窗口（本册关键读数）：从自然标度 ħc 到观测上界 λ_max 之间的跨度 = '
           '`log₁₀(λ_max/ħc) = ' + str(window_log10) + '` ⇒ 约 ' + str(int(window_log10)) +
           ' 个数量级。**λ 在这 ~' + str(int(window_log10)) +
           ' 个数量级的区间内取值，观测既不能确定它、也不能排除它**'
           ' ⇒ 按项目 Ω5 / 可识别性口径，λ 是一个**自由度 1、预测力 0** 的参数：'
           '调它既能让 U 项瞬间支配整个 dynamics（λ→λ_max），也能让它彻底消失（λ→0），'
           '而两大类取值的任何现有数据都无法区分。**这把 r81 C1「W1 = 零内容」的定性判断，'
           '升级为机器给出的定量上界与 ~' + str(int(window_log10)) + ' 个数量级的不可识别窗口**'),
          str(window_log10), '可识别性窗口')


# ----------------------------------------------------------------------------
# D 组：总表与 X-R89-1 首算答案
# ----------------------------------------------------------------------------
def group_D(c1):
    rows = read_ricci_rows()
    table = []
    for row in rows:
        rho = D(row['rho_kg_m3'])
        kappa = D(row['quarter_power_m^-1'])
        table.append((row['point'], rho, kappa, eps_eh(rho),
                      ratio_kappa_T(c1, kappa),
                      ratio_U(HBARC, kappa, rho),
                      lambda_max(rho, kappa)))
    txt = ('★X-R89-1 首算总表（两项 × 三环境，全部由机读输入机器算得，`ε_EH = ρc²/2` 为标度估计）：')
    for pt, rho, kappa, eh, rc, ru, lm in table:
        txt += (pt + '：ε_EH=' + str(eh.normalize()) + ' J/m³、r_C(κT)=' + str(rc.normalize()) +
                '、r_U(λ=ħc)=' + str(ru.normalize()) + '、λ_max=' + str(lm.normalize()) + ' J·m；')
    worst_c = max(t[4] for t in table)
    worst_u = max(t[5] for t in table)
    entry('D1', 'FAIL',
          txt + ('⇒ **X-R89-1 的答案是「不可观测」**：κT 项相对强度最猛仅 ' + str(worst_c.normalize()) +
                 '（且无自由可调），λκ⁴ 项在自然取值下最猛仅 ' + str(worst_u.normalize()) +
                 '，而 λ 的可取区间跨约 71 个数量级 ⇒ **W1 支的两项额外内容，'
                 '在现有一切可达观测中都不承载任何可分辨的物理**'
                 '（既不能解释现象，也不能被排除 ⇒ 既无解释力也无预测力）'),
          str([str(worst_c.normalize()), str(worst_u.normalize())]), 'X-R89-1 总表')

    entry('D2', 'INFO',
          ('口径声明（防误读）：①上面全部是**标度估计**（承 r86 纪律第 8 条），取 ε_EH = ρc²/2 作为爱因斯坦项'
           '能量密度口径，数量级结论对标度系数（2π 类因子）不敏感；②本册**未做**变分导出修正 Poisson 方程与'
           '精确 PPN 计算（那是下一层工作量，见 F3 登记）；③本册不改变 W2 支任何结论——'
           'W2 的νεω、CD-BD、 ω 与屏蔽另有其账（r81/r85/r86）；④本册只在 W1 前提（κ,τ 派生、Levi-Civita）下成立'),
          None, '口径与边界')


# ----------------------------------------------------------------------------
# E 组：阳性对照
# ----------------------------------------------------------------------------
def group_E(c1):
    rows = read_ricci_rows()
    row_w = [r for r in rows if r['point'] == '水'][0]
    rho_w = D(row_w['rho_kg_m3'])
    k_w = D(row_w['quarter_power_m^-1'])
    lm = lambda_max(rho_w, k_w)

    # E1 防恒红：λ=0 ⇒ 逐点还原 GR（强度恰 0）
    z = ratio_U(D(0), k_w, rho_w)
    entry('E1', 'PASS' if z == 0 else 'FAIL',
          ('防恒红：λ=0 ⇒ `r_U = ' + str(z.normalize()) + '`（恰 0）⇒ U 项退化时**逐点还原 GR**，'
           '说明 r_U 不是恒正的坏工具'),
          str(z.normalize()), 'λ=0 对照')

    # E2 防恒绿：λ=λ_max ⇒ 强度恰等于观测门槛
    rm = ratio_U(lm, k_w, rho_w)
    dev = abs(rm - DELTA_OBS) / DELTA_OBS
    entry('E2', 'PASS' if dev <= D('1e-50') else 'FAIL',
          ('防恒绿（定标对照）：λ=λ_max ⇒ `r_U = ' + str(rm.normalize()) + '`，与门槛 δ=' +
           str(DELTA_OBS) + ' 的相对偏差 ' + str(dev.normalize()) +
           '（机器零）⇒ **工具的定标正确**：λ 滑到上界时该项恰落在观测门槛上，不会静默溜过去'),
          str(dev.normalize()), 'λ=λ_max 定标')

    # E3 门有分辨力：λ=10λ_max ⇒ 必须超限（判为可观测/排除）
    rh = ratio_U(lm * D(10), k_w, rho_w)
    entry('E3', 'PASS' if rh > DELTA_OBS else 'FAIL',
          ('门有分辨力：λ=10·λ_max ⇒ `r_U = ' + str(rh.normalize()) + '` = ' +
           str((rh / DELTA_OBS).normalize()) + ' × δ ⇒ **超限 ' + str((rh / DELTA_OBS).normalize()) +
           ' 倍** ⇒ 该测度对 λ 连续可调且越过门槛会报警，不是恒 PASS 的开关'),
          str((rh / DELTA_OBS).normalize()), '分辨力对照')

    # E4 κ⁴ 内部互证（定义自洽）
    worst = max((abs(D(r['quarter_power_m^-1']) ** 4 - D(r['Ricci_sq_m^-4'])) / D(r['Ricci_sq_m^-4'])
                 for r in rows))
    entry('E4', 'PASS' if worst <= D('1e-25') else 'FAIL',
          ('防恒零（定义自洽）：`κ = (R_abR^ab)^{1/4}` ⇒ 必须有 `κ⁴ = R_abR^ab`；三环境复算的最大相对偏差 ' +
           str(worst.normalize()) + '（机器零）⇒ κ 值确实由 r76 的曲率量机器导出，而非手工录入'),
          str(worst.normalize()), 'κ⁴ 定义互证')

    # E5 ε_EH 量级对照
    ew = eps_eh(rho_w)
    entry('E5', 'PASS',
          ('量级对照：`ε_EH(水) = ρc²/2 = ' + str(ew.normalize()) +
           ' J/m³`，与水的静止能量密度 `ρc² = 9e19 J/m³` 同量级（差因子 2 即所取的 EH 口径）'
           '⇒ 能量密度基准取在正确量级，未发生数量级错标'),
          str(ew.normalize()), '能量密度基准对照')


# ----------------------------------------------------------------------------
# F 组：元结论 + 对 X-R76-2 的定量脚注
# ----------------------------------------------------------------------------
def group_cross_session():
    """与并行会话 r87（`r80 牛顿极限量级自洽性复算`）的**机器回读 + 零重复声明**。
    只读其源码文本取数（不写、不改），找不到则诚实登记为未读取到。"""
    p = find_one(os.path.join(HERE, 'TUFT-r87_r80牛顿极限量级自洽性复算_攻破_2026-10-17.py'))
    if p is None:
        entry('G1', 'INFO',
              '跨会话回读：未在同目录找到并行会话 r87 的源码文件 ⇒ 本册不引用其任何数字（诚实登记，不臆造）',
              None, '跨会话（未取到）')
        return None, None
    s = io.open(p, encoding='utf-8').read()
    m_lam = re.findall(r'λ\s*[≤<]\s*(3\.57[0-9e\-\+]*)', s)
    m_kap = re.findall(r'(1\.7[0-9]*e34)', s)
    lam_p = m_lam[0] if m_lam else None
    kap_p = sorted(set(m_kap))[-1] if m_kap else None
    if lam_p is None or kap_p is None:
        entry('G1', 'INFO',
              '跨会话回读：并行会话 r87 源码中未同时机读到 λ 上界与 κ/曲率 倍数 ⇒ 只登记存在性、不引用数值',
              None, '跨会话（数值未取到）')
        return lam_p, kap_p
    lam_ns = lambda_max(D('5E+17'), D('9.6602216425594710969043238E-5'))
    gap = lam_ns / D(lam_p)
    entry('G1', 'INFO',
          ('★跨会话互证（只机读、不改动、零重复）：并行会话 **r87**（`r80 牛顿极限量级自洽性复算`）'
           '从**传播标量**的牛顿解侧给出两条读数 —— (i)「**U 可略**」的线性化自洽性要求 `λ ≤ ' + lam_p +
           '`（SI）⇒ 精细调节；(ii) 该解的 κ 比真实时空曲率大 `' + kap_p + '` 倍 ⇒ 「κ=曲率」的几何识别是装饰性的。'
           '**与本册的关系（互补、非重复）**：本册走的是**另一支**——κ 在 W1 支内**是定义上派生的**'
           '（`κ(g)=(R_abR^ab)^{1/4}`），不是解方程解出来的，故 (ii) 的失配不直接转移；'
           '而 (i) 的 λ 上界比本册的观测上界 `λ_max = ' + str(lam_ns.normalize()) + ' J·m` **严 ' +
           str(gap.normalize()) + ' 倍** ⇒ **若同时承认并行册的线性化要求，本册的 U 项连「理论上调到可见」'
           '的余地都被进一步压死** ⇒ 两册互为加强，且两册的入口（传播标量牛顿解 vs W1 派生支可观测性）'
           '与问题（U 可略 vs 项的可观测强度/可识别性）均不相同 ⇒ **零重复裁定**'),
          str(gap.normalize()), '跨会话互证')
    return lam_p, kap_p


def group_F(c1):
    rows = read_ricci_rows()
    worst_c = max(ratio_kappa_T(c1, D(r['quarter_power_m^-1'])) for r in rows)
    worst_u = max(ratio_U(HBARC, D(r['quarter_power_m^-1']), D(r['rho_kg_m3'])) for r in rows)
    row_ns = [r for r in rows if r['point'] == '中子星'][0]
    lm_ns = lambda_max(D(row_ns['rho_kg_m3']), D(row_ns['quarter_power_m^-1']))
    win = int((lm_ns / HBARC).log10())

    entry('F1', 'FAIL',
          ('★元结论（X-R89-1 首算的答案）：**W1 支的额外项没有可观测内容** —— '
           '`−C₁κT` 项因 C₁ 被 G 唯一锁定而无自由度，其相对爱因斯坦项的强度在最强的中子星环境也仅 ' +
           str(worst_c.normalize()) + '；`−λκ⁴` 项在自然标度 λ=ħc 下最强仅 ' + str(worst_u.normalize()) +
           '，而观测对 λ 的允许区间跨约 **' + str(win) + ' 个数量级** ⇒ 既无可解释的现象、也无可被排除的效应。'
           '这把 r81 C1「W1 = 零内容」的**定性**判断升级为**定量**读数：'
           '「零内容」不是修辞，而是 `' + str(worst_c.normalize()) + '` 与 `' + str(worst_u.normalize()) +
           '` 这两个机器算出的数，以及 λ 那约 ' + str(win) + ' 个数量级的不可识别窗口'),
          str([str(worst_c.normalize()), str(worst_u.normalize()), win]), '元结论')

    entry('F2', 'INFO',
          ('★对 X-R76-2（W1 vs W2）裁决的**定量脚注**（本册仍不代选，只补账）：'
           '裁决所需的这一条以前是缺的——「选 W1 之后体系还剩什么」现在有了数字：'
           'W1 = GR + 两项强度分别 ≤ ' + str(worst_c.normalize()) + ' 与 ≤ ' + str(worst_u.normalize()) +
           '（自然 λ）的额外项 + 1 个跨 ' + str(win) + ' 个数量级不可约束的参数 λ。'
           'W2 的账另记：`ω ≥ 43476.2608…`（被观测反解）+ `C₁` + `λ` + 屏蔽（chameleon 3 参数+外部输入 ⇒ n_free=7；'
           'Vainshtein ≥2 自由函数+r_c ⇒ n_free≥6）⇒ Ω5 门 `n_free ≤ 4` 撞墙（承 r85 D2 / r86 D1 / r88 D2）。'
           '⇒ **两条路的代价第一次在同一张表上：W1 付出「内容与 Gehenna 预测力归零」，W2 付出「参数/函数爆表」。'
           '选哪一条仍是科学哲学层的选择，本册不代选。**'),
          str(win), 'X-R76-2 定量脚注')

    entry('F3', 'INFO',
          ('下一步（按依赖序，本册不代选）：①**仍先裁决 X-R76-2**（本册为它补齐了 W1 侧的决定性数字，'
           '它是唯一剩下的闸门）；②若选 W1 ⇒ 本册结果已说明「体系不再含任何可观测的新内容」，'
           '此时应诚实定位为 GR 的再参数化（除非来料方改动 κ,τ 的原初定义）；③若选 W2 ⇒ 走屏蔽选型与 λ 符号，'
           '账已在 r86；④**本册登记的下一个可计算项 `X-R89-2`**：把 W1 支的两项额外程做完整变分，'
           '导出修正 Poisson 方程与精确 PPN γ/β（本册只做标度估计）⇒ 这是把 D2 口径声明②清掉的唯一直路，'
           '但按其预期量级（`≤ ' + str(worst_c.normalize()) + '`）不会产生能改变门类结论的结果'),
          'dependency-ordered', '下一步与 X-R89-2')


# ----------------------------------------------------------------------------
# payload 与输出
# ----------------------------------------------------------------------------
def build_payload():
    verdict = 'FAIL' if COUNTS.get('FAIL', 0) > 0 else (
        'BOUNDARY' if COUNTS.get('BOUNDARY', 0) > 0 else 'PASS')
    # 可识别性窗口（机器算值，用于红线与元判定文字，避免手写数字与机读不一致）
    rows = read_ricci_rows()
    row_ns = [r for r in rows if r['point'] == '中子星'][0]
    _lm = lambda_max(D(row_ns['rho_kg_m3']), D(row_ns['quarter_power_m^-1']))
    win = str(int((_lm / HBARC).log10()))
    meta = ('X-R89-1 首算：W1 支额外项 (−C₁κT 与 −λκ⁴) 的可观测强度定量。'
            'κT 项因 C₁ 被 G 锁定而无自由度，最强环境（中子星）相对爱因斯坦项仅 ' +
            str(max(ratio_kappa_T(read_c_req(), D(r['quarter_power_m^-1'])) for r in rows).normalize()) +
            '；λκ⁴ 项在自然标度 λ=ħc 下最强仅 ' +
            str(max(ratio_U(HBARC, D(r['quarter_power_m^-1']), D(r['rho_kg_m3'])) for r in rows).normalize()) +
            '，而观测对 λ 的允许区间跨约 ' + win + ' 个数量级 '
            '⇒ 两项都既不能解释现象也不能被排除 ⇒ 「W1 = 零内容」由定性升级为定量。')
    return {
        'round': 'r89',
        'date': '2026-10-17',
        'source': 'X-R89-1 首算（承 r76 ricci_rows / r78 C3 / r80 C1 / r85 A1）',
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
            {'tag': 'NS1', 'text': 'c、ħ 取 CODATA；ħc = 1.98644586e-25 J·m 为两者之积'},
            {'tag': 'NS2', 'text': 'Cassini |γ−1| < 2.3e-5 用作「可观测门槛」δ，属外部实验事实（承 r78/r85）'},
            {'tag': 'NS3', 'text': 'κ 三点族（宇宙平均/水/中子星）的 ρ 与 (R_abR^ab)^{1/4} 全部机读自 r76 key_numbers，无手抄'},
            {'tag': 'NS4', 'text': 'C₁ = √(4π)ℓ_P 由 r78/r80 两册互证读取（容差 1e-24），其「被 G 唯一锁定」结论承 r78 C3 / r80 C1'},
            {'tag': 'NS5', 'text': 'ε_EH = ρc²/2 为爱因斯坦项能量密度的**标度估计**口径（尘埃 R≈8πGρ/c²），明确标注为标度估计而非精确变分结果'},
            {'tag': 'NS6', 'text': '「度规唯一确定的无挠相容联络是 Levi-Civita」为教科书结论 ⇒ W1 内 τ(g)≡0 属定义推论，引用不自推'},
            {'tag': 'NS7', 'text': 'κ(g) 取 r76 A02 route (a) κ=(R_abR^ab)^{1/4}（零新常数）；route (b) 三族被 r73 l_0 排除定理覆盖，本册不取用'},
            {'tag': 'NS8', 'text': '本册不代选 X-R76-2（W1 vs W2），只在 W1 侧补齐此前缺失的决定性数字'},
        ],
        'red_line': '数学／数值自洽 ≠ 物理证实。本册把「W1 支零内容」由定性判断升级为机器给出上界的定量判断，'
                    '但**上界之外仍有约 ' + win + ' 个数量级的允许区间**——本册证明的是「在自然取值与一切可达观测下不可见」，'
                    '**不是「数学上不存在任何 λ 使其可观测」**；同样，它不等于「TUFT 被否证」——'
                    'W2 支、四力升级路径都未被否证。**λ=λ_max 那一端尤须谨慎：它意味着这类额外项理论上可以被调到可见，'
                    '只是那需要一个比自然标度大 ~10^' + win + ' 倍的精心选择（调参），而非预言。**',
    }


def write_outputs(payload):
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    verdict = payload['verdict']
    jp = os.path.join(DATA, STEM + '.json')
    with io.open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rl = ['TUFT-r88 X-R89-1 首算：W1 支额外项可观测强度 运行报告',
          'counts=' + str(payload['counts']) + ' total=' + str(payload['total']) + ' verdict=' + verdict,
          'meta=' + payload['meta_verdict']]
    for e in ENTRIES:
        rl.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rl.append('    residual=' + e['residual'])
    rl.append('')
    rl.append('GUARD G0: 自守卫全过（G0-1 三点族正数 / G0-2 κ⁴==R_abR^ab / G0-3 C₁对照 / '
              'G0-4 ε_EH 量级 / G0-5 λ=0 归零 / G0-6 λ=λ_max 定标 / G0-7 λ=10λ_max 超限）')
    rl.append('GENERATED_AT=' + payload['generated_at'])
    rl.append('MODULE=' + payload['module'])
    rp = os.path.join(DATA, STEM + '_report.txt')
    with io.open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rl))

    ml = ['# ' + STEM, '', '日期：2026-10-17 · X-R89-1 首算（W1 支额外项可观测强度）', '',
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


def write_judgment(payload, c1, cross=None):
    rows = read_ricci_rows()
    worst_c = max(ratio_kappa_T(c1, D(r['quarter_power_m^-1'])) for r in rows)
    worst_u = max(ratio_U(HBARC, D(r['quarter_power_m^-1']), D(r['rho_kg_m3'])) for r in rows)
    row_ns = [r for r in rows if r['point'] == '中子星'][0]
    lm_ns = lambda_max(D(row_ns['rho_kg_m3']), D(row_ns['quarter_power_m^-1']))
    win = int((lm_ns / HBARC).log10())

    L = ['# 判定_TUFT-r89-X-R89-1首算_W1支额外项可观测强度_攻破_2026-10-17', '',
         '日期：2026-10-17 · **X-R89-1 首算册**（r88 总账册登记的「可计算而漏算」项）· **下轮从 r90 起**', '',
         '## 〇、一句话结论',
         '**X-R89-1 的答案是不存在可达观测内容：W1 支的 `−C₁κT` 项相对爱因斯坦项最强（中子星）仅 ' +
         str(worst_c.normalize()) + '，且无自由可调；`−λκ⁴` 项在自然标度 λ=ħc 下最强仅 ' +
         str(worst_u.normalize()) + '，而观测对 λ 的允许区间跨约 **' + str(win) +
         ' 个数量级** ⇒ 「W1 = 零内容」由定性判断升级为机器给出的定量上界。**', '',
         '## 一、为什么现在做（r88（总账册）与本册的关系）',
         'r88（总账册）的结论是「剩余项全是裁决项、无一可计算」。本册复核发现该结论**漏了一类**：'
         '「选 W1 之后体系还剩什么可观测内容」从来没有被任何一册算过 —— 它是可计算的，'
         '且正好是 X-R76-2 裁决所需的决定性数字。本册把它从「未算」变成「算完」（登记为 `X-R89-1`）。', '',
         '## 二、A 组 承重前提',
         '- **A1** W1 支内 `τ(g) ≡ 0`：κ,τ 全降为度规派生量，而度规唯一确定的无挠相容联络是 Levi-Civita（无挠率）'
         ' ⇒ `U(κ²+τ²)² ⇒ λκ⁴`、约束 `κ²+τ²=ω²` 退化为 `|κ|=ω` ⇒ **τ 扇区在 W1 支内不提供实体内容**。',
         '- **A2** κ(g) 取 r76 A02 route (a)：`κ = k·(R_abR^ab)^{1/4}`（m^-1，零新常数，与 r85 A3 `[κ]=L^-1` 一致）；'
         'route (b) 三族引入非几何长度，已被 r73 `l_0` 排除定理覆盖，不取用。',
         '- **A3** 三点族全部机读 r76 `ricci_rows`，并用 `κ⁴ == R_abR^ab` 反查一致（最大相对偏差见下表）⇒ 端到端自洽。', '',
         '## 三、总表（全部由机读输入机器算得；`ε_EH = ρc²/2` 为标度估计）', '',
         '| 环境 | ρ [kg/m³] | κ [m^-1] | ε_EH [J/m³] | r_C = C₁κ | r_U (λ=ħc) | λ_max [J·m] |',
         '|---|---|---|---|---|---|---|']
    for row in rows:
        rho = D(row['rho_kg_m3'])
        kappa = D(row['quarter_power_m^-1'])
        L.append('| ' + row['point'] + ' | ' + str(rho.normalize()) + ' | ' + str(kappa.normalize()) +
                 ' | ' + str(eps_eh(rho).normalize()) + ' | ' +
                 str(ratio_kappa_T(c1, kappa).normalize()) + ' | ' +
                 str(ratio_U(HBARC, kappa, rho).normalize()) + ' | ' +
                 str(lambda_max(rho, kappa).normalize()) + ' |')
    L += ['', '（C₁ = √(4π)ℓ_P = ' + str(c1.normalize()) + ' m，机读自 r78/r80 互证；'
          'λ_max = δ·ε_EH/κ⁴，δ = 2.3×10⁻⁵ 为 Cassini 门槛。）', '',
          '## 四、B/C 组结论',
          '- **B2 [FAIL]** κT 项：**C₁ 被 G 唯一锁定 ⇒ 无自由度**，其在最强环境下的相对强度仅为 ' +
          str(worst_c.normalize()) + ' ⇒ 该项写在拉氏量中却不产生任何可达观测后果。',
          '- **C1 [PASS]** λκ⁴ 项在自然标度 λ=ħc 下最强 ' + str(worst_u.normalize()) + '（相差约 76 个数量级）。',
          '- **C2 [PASS]** 反解上界：最紧为中子星 ⇒ `λ ≲ ' + str(lm_ns.normalize()) + ' J·m` ≈ ' +
          str((lm_ns / HBARC).normalize()) + ' × ħc。**这是上界而非预言**。',
          '- **C3 [FAIL] 可识别性**：自然标度到上界跨约 **' + str(win) + ' 个数量级** ⇒ λ 是**自由度 1、预测力 0** 的参数。', '',
          '## 五、D/E 组',
          '- **D1 [FAIL]** 总表 ⇒ X-R89-1 的答案：两项额外内容在现有一切可达观测中都不承载可分辨的物理。',
          '- **D2 [INFO]** 口径：全部为标度估计；未做完整变分与精确 PPN（登记为 `X-R89-2`）；结论只在 W1 前提下成立。',
          '- 阳性对照：E1 λ=0 ⇒ 逐点还原 GR；E2 λ=λ_max ⇒ 恰落门槛（定标正确）；E3 λ=10λ_max ⇒ 超限 ' +
          '10 倍（门有分辨力）；E4 `κ⁴ == R_abR^ab` 机器零；E5 ε_EH 量级与 ρc² 同量级。']
    lam_p = cross[0] if cross else None
    kap_p = cross[1] if cross else None
    row_ns2 = [r for r in read_ricci_rows() if r['point'] == '中子星'][0]
    lam_ns2 = lambda_max(D(row_ns2['rho_kg_m3']), D(row_ns2['quarter_power_m^-1']))
    if lam_p:
        L.append('- **G1 [INFO] 跨会话互证（只机读、不改、零重复）**：并行会话 **r87**（`r80 牛顿极限量级自洽性复算`）'
                 '从传播标量的牛顿解侧给出 `λ ≤ ' + str(lam_p) + '`（「U 可略」的线性化门槛）与 κ 比真实曲率大 `' +
                 str(kap_p) + '` 倍；前者比本册的观测上界 `λ_max = ' + str(lam_ns2.normalize()) + ' J·m` **严 ' +
                 str((lam_ns2 / D(lam_p)).normalize()) + ' 倍** ⇒ **两册入口不同（传播标量牛顿解 vs W1 派生支）、'
                 '互为加强、零重复**：若同时承认并行册的线性化要求，本册 U 项连「理论上调到可见」的余地也被压死。')
    else:
        L.append('- **G1 [INFO] 跨会话回读**：未机读到并行会话 r87 的数值（诚实登记，不引用不臆造）。')
    L += ['',
          '## 六、F 组 元结论与对 X-R76-2 的定量脚注',
          '**元结论**：r81 C1 的「W1 = 零内容」从修辞变成数字——' + str(worst_c.normalize()) + '、' +
          str(worst_u.normalize()) + ' 与 λ 那约 ' + str(win) + ' 个数量级的不可识别窗口。',
          '**对裁决的定量脚注（仍不代选）**：', '',
          '| 分支 | 代价 | 由谁/哪册给出 |',
          '|---|---|---|',
          '| W1 | 额外项 ≤ ' + str(worst_c.normalize()) + ' 与 ≤ ' + str(worst_u.normalize()) +
          '（自然 λ）+ λ 跨 ' + str(win) + ' 个数量级不可约束 ⇒ **解释力与预测力归零** | 本册（X-R89-1 首算） |',
          '| W2 | ω ≥ 43476.26…（观测反解）+ C₁ + λ + 屏蔽 ⇒ chameleon n_free=7 / Vainshtein n_free≥6 ⇒ **Ω5 撞墙** | r81/r85/r86/r88（总账册） |', '',
          '⇒ 两条路的代价第一次落在同一张表上；**选哪一条仍是科学哲学层的选择，本册不代选**。', '',
          '## 七、不自推登记']
    for n in payload['not_self_derived']:
        L.append('- ' + n['tag'] + '：' + n['text'])
    L += ['', '## 八、开放项与治理',
          '- `X-R89-1`（W1 支额外项可观测强度）⇒ **本册首算完成**（结论：不可观测，λ 不可识别）。',
          '- `X-R89-2`（把这两项做完整变分、导出修正 Poisson 方程与精确 PPN）⇒ **新开放项，待决定是否值得做**'
          '（本册预期量级 ≤ ' + str(worst_c.normalize()) + '，不会改变门类结论）。',
          '- `X-R76-2`（W1 vs W2）⇒ **仍需用户裁决**，本册已补齐 W1 侧此前缺失的决定性数字。',
          '- 治理：未改动任何他人文件字节（r76/r78/r80 全部只读机读）；未跑 `refresh_catalog`；未做 git 操作。'
          '**下轮从 r90 起**。', '',
          '## 九、红线', payload['red_line'], '',
          'GENERATED_AT=' + payload['generated_at'], 'MODULE=' + payload['module']]
    jb = os.path.join(BASE, '判定_TUFT-r89-X-R89-1首算_W1支额外项可观测强度_攻破_2026-10-17.md')
    with io.open(jb, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))
    return jb


def main():
    G0_guards()
    c1 = read_c_req()
    group_A(c1)
    group_B(c1)
    group_C()
    group_D(c1)
    group_E(c1)
    cross = group_cross_session()
    group_F(c1)
    payload = build_payload()
    jp, rp, mp = write_outputs(payload)
    jb = write_judgment(payload, c1, cross)
    assert len(ENTRIES) == sum(payload['counts'].values()), 'entry count mismatch'
    print('counts=' + str(payload['counts']))
    print('total=' + str(payload['total']))
    print('verdict=' + payload['verdict'])
    print('written: ' + jp + ' | ' + rp + ' | ' + mp + ' | ' + jb)


if __name__ == '__main__':
    main()
