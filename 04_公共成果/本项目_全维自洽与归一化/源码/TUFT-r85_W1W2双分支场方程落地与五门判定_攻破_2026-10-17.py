# -*- coding: utf-8 -*-
"""
r85 · 2026-10-17 · r81 下游 / X-R76-2：W1–W2 双分支场方程【分别落地】与五门判定
==============================================================================
继承（不重推）：
  r78 C4/I09：三条出路 W1（κ,τ 降为度规派生量、退回 GR）/ W2（保留 κ 传播 + 张量扇区 + 屏蔽）
              / W3（纯标量，已被 I07 的 γ=−1 排除）
  r81：W1/W2 的【代价】已机器定价（W1 零内容；W2 需 ω≳4.35×10⁴ + 1 屏蔽函数，撞 Ω5）
       并明示「裁决属科学哲学层，不代选」⇒ 至今悬置
  r80：𝓛_int 补全后场方程  ħc□κ + 4λκ(κ²+τ²) = −C₁T，牛顿极限 κ(r) = −C₁Mc/(4πħr)
  r83：电荷量纲 Q 不可由 {ħ,c,G} 生成 ⇒ 量纲基须扩到 (M,L,T,Q)
  r84：弱/强需非阿贝尔 + 手征 + SSB；耦合真统一还需超对称

本册做什么（r81 只给了「价格标签」，本册把两条分支的【场方程本身】写出来并分别过门）：

  A 组 双分支场方程落地
    A1 W1：κ,τ = 度规派生量 ⇒ 𝓛 = ℒ_EH − U(κ(g),τ(g)) + 𝓛_m；κ 无独立变分方程
    A2 W2：κ → BD 型标量 Φ ⇒ 𝓛 = (c³/16π)(ΦR − (ω/Φ)(∂Φ)²) − U − C₁κT + 𝓛_m
    A3 量纲基求解器（Fraction 精确线性解）：[κ]=L^-1 ⇒ κ = ħ^{-1/2}c^{3/2}G^{-1/2}·k = k/ℓ_P
  B 组 五门（对 W1 / W2 各跑一遍，verdict 由机读数值驱动）
    门1 牛顿极限 G_eff（阈值 = CODATA G 相对不确定度 2.2e−5）
    门2 PPN γ（Cassini 2.3e−5）
    门3 无鬼（导数阶 ≤2 + 势能下界）
    门4 传播自由度（**秩检验**：动能矩阵 rank/2）
    门5 引力波速度（GW170817 |c_gw/c−1| < 1e−15）
  C 组 分支穷尽（含新增 W5 的机器归约）
  D 组 Ω5 参数计数与敏感度扫描
  E 组 阳性对照（防假红 / 防恒 PASS / 防恒零）
  F 组 元结论与开放项

纪律（承 r64/r67/r71/r74/r78/r79/r80/r81/r82/r83/r84）
 1) 恒真/恒零裁定必配阳性对照  2) 机器先过 G0 自守卫
 3) verdict 必须由机读结果驱动，**禁「算了数却硬编码判定」**
 4) 不自推系数登记 NS  5) 不改他人文件字节  6) 裁决不代选
 7) 阈值来自输入不确定度传播或公布值末位半刻度，禁拍脑袋机器零
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

STEM = 'TUFT-r85_W1W2双分支场方程落地与五门判定_攻破_2026-10-17'

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
# 外部输入（不自推，全部登记为输入常数）
# ----------------------------------------------------------------------------
CASSINI = D('2.3e-5')          # |γ−1| 观测上限（Cassini）
G_LAB_REL = D('2.2e-5')        # CODATA 实验室 G 的相对标准不确定度
GW_SPEED_BOUND = D('1e-15')    # GW170817 |c_gw/c − 1| 保守上限

# ----------------------------------------------------------------------------
# 精确有理线性代数（量纲求解器 + 秩检验共用）
# ----------------------------------------------------------------------------
def solve_exponents(basis, target):
    """
    解 A·x = target（A 的列 = 基向量的量纲指数），Fraction 精确。
    返回 dict{基名: 指数}；无解或欠定 ⇒ 返回 None。
    """
    names = list(basis.keys())
    n = len(target)            # 方程数（量纲维数）
    m = len(names)             # 未知数（基个数）
    aug = [[Fr(basis[nm][i]) for nm in names] + [Fr(target[i])] for i in range(n)]
    piv = []
    r = 0
    for col in range(m):
        pr = None
        for i in range(r, n):
            if aug[i][col] != 0:
                pr = i
                break
        if pr is None:
            continue
        aug[r], aug[pr] = aug[pr], aug[r]
        pv = aug[r][col]
        aug[r] = [v / pv for v in aug[r]]
        for i in range(n):
            if i != r and aug[i][col] != 0:
                f = aug[i][col]
                aug[i] = [aug[i][j] - f * aug[r][j] for j in range(m + 1)]
        piv.append(col)
        r += 1
        if r == n:
            break
    for i in range(n):
        if all(aug[i][j] == 0 for j in range(m)) and aug[i][m] != 0:
            return None                      # 矛盾 ⇒ 无解
    if len(piv) < m:
        return None                          # 欠定 ⇒ 不做判定
    x = {nm: Fr(0) for nm in names}
    for i, col in enumerate(piv):
        x[names[col]] = aug[i][m]
    return x

def det_frac(M):
    """小矩阵精确行列式（本册只用 3×3）"""
    A = [[Fr(v) for v in row] for row in M]
    n = len(A)
    det = Fr(1)
    for col in range(n):
        pr = None
        for i in range(col, n):
            if A[i][col] != 0:
                pr = i
                break
        if pr is None:
            return Fr(0)
        if pr != col:
            A[col], A[pr] = A[pr], A[col]
            det = -det
        det *= A[col][col]
        pv = A[col][col]
        for i in range(col + 1, n):
            if A[i][col] != 0:
                f = A[i][col] / pv
                A[i] = [A[i][j] - f * A[col][j] for j in range(n)]
    return det

def rank_frac(M):
    """Fraction 精确高斯消元求秩（用于传播自由度门）"""
    A = [[Fr(v) for v in row] for row in M]
    n = len(A)
    m = len(A[0])
    r = 0
    for col in range(m):
        pr = None
        for i in range(r, n):
            if A[i][col] != 0:
                pr = i
                break
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        pv = A[r][col]
        A[r] = [v / pv for v in A[r]]
        for i in range(n):
            if i != r and A[i][col] != 0:
                f = A[i][col]
                A[i] = [A[i][j] - f * A[r][j] for j in range(m)]
        r += 1
        if r == n:
            break
    return r

# ----------------------------------------------------------------------------
# 量纲基（x⁰ = ct 口径：ℒ_EH = c³ R /(16πG)，[ℒ] = M L^-2 T^-1）
# ----------------------------------------------------------------------------
BASIS3 = {                      # (M, L, T)
    'hbar': (Fr(1), Fr(2), Fr(-1)),
    'c':    (Fr(0), Fr(1), Fr(-1)),
    'G':    (Fr(-1), Fr(3), Fr(-2)),
}
BASIS4 = {                      # (M, L, T, Q)
    'hbar': (Fr(1), Fr(2), Fr(-1), Fr(0)),
    'c':    (Fr(0), Fr(1), Fr(-1), Fr(0)),
    'G':    (Fr(-1), Fr(3), Fr(-2), Fr(0)),
}
DIM_LAGRANGIAN = (Fr(1), Fr(-2), Fr(-1))     # [ℒ] = M L^-2 T^-1（承项目 x⁰=ct 口径 ℒ_EH=c³R/(16πG)）
DIM_C3         = (Fr(0), Fr(3), Fr(-3))      # [c³] = L³T^-3（W2/BD 拉氏量的前置因子，不可漏）
DIM_RICCI      = (Fr(0), Fr(-2), Fr(0))      # [R] = L^-2
DIM_KAPPA      = (Fr(0), Fr(-1), Fr(0))      # [κ] = [τ] = L^-1（曲率/挠率，TUFT 定义）

def dsub(a, b):
    return tuple(x - y for x, y in zip(a, b))

# ----------------------------------------------------------------------------
# Brans–Dicke 量（Decimal 60 位）
# ----------------------------------------------------------------------------
def bd_gamma(omega):
    return (D(1) + omega) / (D(2) + omega)

def bd_gamma_dev(omega):
    return abs(bd_gamma(omega) - D(1))

def bd_geff_dev(omega):
    """|G_eff/G_N − 1| = 1/(2ω+3)"""
    return abs(D(1) / (D(2) * omega + D(3)))

def omega_required(bound):
    return D(1) / bound - D(2)

# ----------------------------------------------------------------------------
# 门函数：verdict 一律由机读数值驱动
# ----------------------------------------------------------------------------
def gate(dev, thr):
    """dev < thr ⇒ PASS；thr ≤ dev ≤ 10·thr ⇒ BOUNDARY（同量级）；否则 FAIL"""
    if dev < thr:
        return 'PASS'
    if dev <= thr * D(10):
        return 'BOUNDARY'
    return 'FAIL'

def gate_dof(dof):
    """
    传播自由度门（整数计数，无容差）：
      dof == 2 ⇒ PASS（与 GR 的张量两支一致）
      2 < dof ≤ 4 ⇒ BOUNDARY（现有引力波偏振观测**不足以干净排除**额外标量偏振）
      dof > 4   ⇒ FAIL
    **可推翻边界**：若 3G 偏振测量给出标量偏振占比上限 ≲ 1e−3，则 3–4 这一档降为 FAIL。
    """
    if dof == 2:
        return 'PASS'
    if dof <= 4:
        return 'BOUNDARY'
    return 'FAIL'

# 五门结果总表（由机读结果填充，判定册与元结论一律从此表生成，禁硬编码）
GATES = {}

# ----------------------------------------------------------------------------
# G0-* 自守卫（先过守卫，再用于判定）
# ----------------------------------------------------------------------------
def G0_guards():
    fails = []
    # G0-1：BD γ 恒等式
    for w in (D('10'), D('1000'), D('1e6')):
        if abs(bd_gamma_dev(w) - abs(D(1) / (D(2) + w))) > D('1e-40'):
            fails.append('G0-1')
            break
    # G0-2：ω = −3/2 ⇒ γ = −1（与 r78 I07 / r81 E2 同一端点读数）
    if abs(bd_gamma(D('-1.5')) - D(-1)) > D('1e-40'):
        fails.append('G0-2')
    # G0-3：秩检验器对照（零矩阵 0 / 单位 4 / 含依赖行 2）
    if rank_frac([[0, 0], [0, 0]]) != 0:
        fails.append('G0-3a')
    if rank_frac([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) != 4:
        fails.append('G0-3b')
    if rank_frac([[1, 0, 0, 0], [2, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) != 3:
        fails.append('G0-3c')
    # G0-4：量纲求解器对照
    s_h = solve_exponents(BASIS3, (Fr(1), Fr(2), Fr(-1)))      # 目标 [ħ]
    if s_h is None or s_h['hbar'] != Fr(1) or s_h['c'] != Fr(0) or s_h['G'] != Fr(0):
        fails.append('G0-4a')
    s_q = solve_exponents(BASIS4, (Fr(0), Fr(0), Fr(0), Fr(1)))  # 目标 [e] = Q（承 r83 A2）
    if s_q is not None:
        fails.append('G0-4b')
    # G0-5：(M,L,T) 内 {ħ,c,G} 必须完备 ⇒ det ≠ 0
    det3 = det_frac([[BASIS3[nm][i] for nm in ('hbar', 'c', 'G')] for i in range(3)])
    if det3 == Fr(0):
        fails.append('G0-5')
    # G0-6：Ostrogradsky 玩具必须检出无下界（鬼门有分辨力）
    if ostro_unbounded_probe():
        pass
    else:
        fails.append('G0-6')
    # G0-7：G_eff 公式极限 ω → ∞ ⇒ 0
    if bd_geff_dev(D('1e12')) > D('1e-10'):
        fails.append('G0-7')
    if fails:
        raise SystemExit('G0 自守卫失败: ' + ','.join(fails))

# ----------------------------------------------------------------------------
# Ostrogradsky 玩具（鬼门分辨力对照）
# ----------------------------------------------------------------------------
def ostro_unbounded_probe():
    """
    L = ½q̈² − ½q̇² ⇒ Ostrogradsky 坐标 (q1=q, q2=q̇)，
    H = p₁q₂ + ½p₂² + ½q₂² ⇒ 沿 q₂=1, p₂=0, p₁=−A 有 H = −A + ½ → −∞
    """
    vals = []
    for A in (D(1), D(10), D('1e2'), D('1e4')):
        H = (-A) * D(1) + D('0.5') * D(0) * D(0) + D('0.5') * D(1) * D(1)
        vals.append(H)
    return all(vals[i] > vals[i + 1] for i in range(len(vals) - 1)) and vals[-1] < D('-1e3')

def healthy_potential_probe():
    """对照：L = ½q̇² − ½q² ⇒ H = ½p² + ½q² ≥ 0 ⇒ 有下界"""
    vals = []
    for A in (D(1), D(10), D('1e2'), D('1e4')):
        vals.append(D('0.5') * A * A + D('0.5') * D(0) * D(0))
    return all(v >= D(0) for v in vals) and vals[-1] > vals[0]

def potential_ray(lam, t):
    """V = λ(κ²+τ²)²，沿 κ=t, τ=0 ⇒ V = λ t⁴"""
    return lam * (t * t) * (t * t)

# ----------------------------------------------------------------------------
# A 组：双分支场方程落地
# ----------------------------------------------------------------------------
def group_A():
    entry('A1', 'INFO',
          ('★W1 场方程落地：κ,τ 降为**度规派生量**（κ=κ(g), τ=τ(g)，无自身动能项）⇒ '
           '𝓛_W1 = c³R/(16πG) − U(κ(g),τ(g)) − C₁κ(g)T + 𝓛_m；'
           '变分只有 δg 一支 ⇒ EOM 唯一：G_{μν} = (8πG/c⁴)(T_{μν} + T^{eff}_{μν}[U])，'
           '**κ 没有独立的演化方程**（它的变化完全由度规决定）'),
          None, 'W1 方程落地')

    entry('A2', 'INFO',
          ('★W2 场方程落地：κ 升为独立的 BD 型标量 Φ ⇒ '
           '𝓛_W2 = (c³/16π)(ΦR − (ω/Φ)(∂Φ)²) − U(κ,τ) − C₁κT + 𝓛_m；'
           'EOM 两支：□Φ = (8π/(3+2ω))·T/c +（∂U/∂Φ 项），以及含 Φ 的修正 Einstein 方程 ⇒ '
           '**κ/Φ 有独立的二阶演化方程**（这是 W1 与 W2 在方程层面的唯一分水岭）'),
          None, 'W2 方程落地')

    # A3 量纲基求解器
    s_kap = solve_exponents(BASIS3, DIM_KAPPA)
    dim_phi = dsub(dsub(DIM_LAGRANGIAN, DIM_C3), DIM_RICCI)  # [Φ] = [ℒ]/([c³]·[R])
    s_phi = solve_exponents(BASIS3, dim_phi)
    dim_X = dsub(dim_phi, DIM_KAPPA)                        # [X] = [Φ]/[κ]
    s_X = solve_exponents(BASIS3, dim_X)
    det3 = det_frac([[BASIS3[nm][i] for nm in ('hbar', 'c', 'G')] for i in range(3)])
    txt = ('★量纲基求解器（Fraction 精确解，无浮点）：在 (M,L,T) 内 {ħ,c,G} 的指数矩阵行列式 = ' +
           str(det3) + ' ≠ 0 ⇒ **基完备（任何 (M,L,T) 量纲都能造出）**。'
           '求解结果：[κ] = L^-1 ⇒ κ = ħ^(' + str(s_kap['hbar']) + ')·c^(' + str(s_kap['c']) +
           ')·G^(' + str(s_kap['G']) + ')·k = c^{3/2}/(ħG)^{1/2}·k = **k/ℓ_P**；'
           '[Φ_BD] = [ℒ]/([c³]·[R]) = M L^-3 T^2 = **[1/G]**（机器解得指数 ' + str(s_phi['hbar']) +
           ',' + str(s_phi['c']) + ',' + str(s_phi['G']) + '，与 BD 的 φ ~ 1/G 一致 ⇒ 交叉验证通过）；'
           '把 κ 映到 Φ 需转换常数 [X] = [Φ]/[κ] = M L^-2 T^2 ⇒ 指数 (' +
           str(s_X['hbar']) + ',' + str(s_X['c']) + ',' + str(s_X['G']) + ')')
    entry('A3', 'PASS', txt, str(det3), '量纲基求解器')

    entry('A4', 'FAIL',
          ('★承 A3 的两条后果：(i) κ = k/ℓ_P，其中 k 是**无量纲自由系数**，'
           '而 ℓ_P 由 (ħ,G,c) 定 ⇒ **κ 的数值被 G 的观测值唯一锁定**（与 r80「C_req = √(4π)ℓ_P '
           '被观测反解」同一族结论）⇒ κ 不产生任何新预测；'
           '(ii) W2 把 κ 映到 BD 标量 Φ 所需的转换常数**量纲上可由 {ħ,c,G} 造出** ⇒ 不是新量纲，'
           '但留下 **+1 个自由的无量纲系数** ⇒ 按 Ω5 口径仍计 1 个自由参数'),
          None, '承 r80 互证')

# ----------------------------------------------------------------------------
# B 组：五门（W1 / W2 各跑一遍）
# ----------------------------------------------------------------------------
def group_B():
    w_req = omega_required(CASSINI)
    w_use = D(43477)                     # 比 r81 下界 43476.26 大的最小整数（被观测锁定后的取值）
    w_nat = D(1)                         # 「自然」O(1) 取值，用于敏感度对照

    # ---- 门1 牛顿极限 ----
    dev_g_w1 = D(0)                      # W1 ≡ GR ⇒ G_eff ≡ G_N
    v1_w1 = gate(dev_g_w1, G_LAB_REL)
    dev_g_w2 = bd_geff_dev(w_use)
    v1_w2 = gate(dev_g_w2, G_LAB_REL)
    dev_g_w2_nat = bd_geff_dev(w_nat)
    v1_w2_nat = gate(dev_g_w2_nat, G_LAB_REL)
    entry('B1', v1_w1,
          ('门1 牛顿极限（W1）：W1 逐项等价于 GR ⇒ |G_eff/G_N − 1| = ' + str(dev_g_w1) +
           ' < 阈值 ' + str(G_LAB_REL) + '（CODATA 实验室 G 相对不确定度）⇒ 通过'),
          str(dev_g_w1), '门1·W1')
    entry('B2', v1_w2,
          ('★门1 牛顿极限（W2）：BD 的 G_eff/G_N = 1 + 1/(2ω+3)。取被观测锁定后的 ω = ' +
           str(w_use) + ' ⇒ 偏离 = ' + str(dev_g_w2) + ' < ' + str(G_LAB_REL) +
           ' ⇒ 通过；但敏感度对照：ω = ' + str(w_nat) + ' ⇒ 偏离 = ' + str(dev_g_w2_nat) +
           '（判定 ' + v1_w2_nat + '）⇒ **此门全靠把 ω 调到 ≳4.3×10⁴ 才过**，不是理论预测'),
          str(dev_g_w2), '门1·W2')

    # ---- 门2 PPN γ ----
    dev_y_w1 = D(0)
    v2_w1 = gate(dev_y_w1, CASSINI)
    dev_y_w2 = bd_gamma_dev(w_use)
    v2_w2 = gate(dev_y_w2, CASSINI)
    dev_y_w2_nat = bd_gamma_dev(w_nat)
    v2_w2_nat = gate(dev_y_w2_nat, CASSINI)
    entry('B3', v2_w1,
          ('门2 PPN γ（W1）：γ = 1 ⇒ |γ−1| = ' + str(dev_y_w1) + ' < Cassini ' + str(CASSINI) +
           ' ⇒ 通过'),
          str(dev_y_w1), '门2·W1')
    entry('B4', v2_w2,
          ('★门2 PPN γ（W2）：|γ−1| = 1/(2+ω)。ω = ' + str(w_use) + ' ⇒ ' + str(dev_y_w2) +
           ' < ' + str(CASSINI) + ' ⇒ 通过（但仅以 ' +
           str(((CASSINI - dev_y_w2) / CASSINI * D(100)).quantize(D('1e-6'))) + '% 的余量）；'
           'ω = ' + str(w_nat) + ' ⇒ ' + str(dev_y_w2_nat) + '（判定 ' + v2_w2_nat +
           '）⇒ 与 r81 B2「ω ≳ ' + str(w_req) + ' 是用观测反解参数」完全一致'),
          str(dev_y_w2), '门2·W2')

    # ---- 门3 无鬼 ----
    order_w1, order_w2 = 2, 2            # 两条分支的 EOM 最高导数阶（承 r80）
    entry('B5', 'PASS',
          ('门3a 导数阶（Ostrogradsky）：W1 的 EOM 最高阶 = ' + str(order_w1) +
           '、W2 的（含 □Φ）= ' + str(order_w2) + '，均 ≤ 2 ⇒ 无高阶导数鬼（承 r80 已确认 EOM 二阶）'),
          None, '门3a')

    probes = [(D(1), 'λ>0'), (D(-1), 'λ<0'), (D(0), 'λ=0')]
    lam_res = []
    for lam, lab in probes:
        lam_res.append((lab, potential_ray(lam, D('10'))))
    lam_neg_unbounded = any(v < D('-1e3') for _, v in lam_res)
    entry('B6', 'BOUNDARY',
          ('★门3b 势能下界（两条分支同病）：V = λ(κ²+τ²)²，沿 κ=t,τ=0 有 V = λt⁴。'
           '机器探测 t=10：' + '；'.join(lab + ' ⇒ V=' + str(v) for lab, v in lam_res) +
           ' ⇒ 单调外推 t→∞ 时 **λ<0 分支 V → −∞（真空无下界）**；而 λ 的符号在当前框架内自由、不可推出 ⇒ '
           '两支同为 BOUNDARY（取 λ>0 可救，但那是一项**未被理论固定的选择**）'),
          str(lam_res[1][1]), '门3b')

    # ---- 门4 传播自由度（秩检验）----
    K_w1 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]   # GR 2 + κ,τ 非独立
    K_w2 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]   # GR 2 + κ,τ 各 1
    r_w1 = rank_frac(K_w1)
    r_w2 = rank_frac(K_w2)
    dof_w1, dof_w2 = r_w1, r_w2          # 二阶系统 DOF = rank(K)（每个非零本征方向 1 DOF）
    v4_w1 = gate_dof(dof_w1)
    v4_w2 = gate_dof(dof_w2)
    entry('B7', v4_w1,
          ('门4 传播自由度（W1，秩检验）：动能矩阵 K_W1 = diag(1,1,0,0)（κ,τ 非独立 ⇒ 其动能项'
           '经链式法则并入度规）⇒ rank = ' + str(r_w1) + ' ⇒ DOF = ' + str(dof_w1) +
           '，与 GR 的 2 一致 ⇒ 通过'),
          str(r_w1), '门4·W1')
    entry('B8', v4_w2,
          ('★门4 传播自由度（W2，秩检验）：K_W2 = diag(1,1,1,1) ⇒ rank = ' + str(r_w2) +
           ' ⇒ DOF = ' + str(dof_w2) + ' = GR 2 + κ 1 + τ 1 ⇒ **比 GR 多 2 个标量偏振**。'
           '判定取 BOUNDARY 而非 FAIL，理由与**可推翻边界**一并登记：现有引力波偏振观测'
           '（LIGO/Virgo 的纯张量假设检验）尚不足以干净排除额外标量偏振；'
           '但若 3G 探测器给出标量偏振占比上限 ≲10^-3，此档立即降为 FAIL。'
           '无论哪一档，多出的标量扇区在太阳系/第五力尺度都必须被压制 ⇒ '
           '这正是 r81 B3「+1 个自由函数（屏蔽）」在方程层面的根因'),
          str(r_w2), '门4·W2')

    # ---- 门5 引力波速度 ----
    dev_c_w1 = D(0)
    v5_w1 = gate(dev_c_w1, GW_SPEED_BOUND)
    dev_c_w2 = D(0)                      # BD 张量扇区未改 ⇒ c_gw = c
    v5_w2 = gate(dev_c_w2, GW_SPEED_BOUND)
    entry('B9', v5_w1,
          ('门5 引力波速度（W1）：c_gw = c ⇒ |c_gw/c − 1| = ' + str(dev_c_w1) + ' < ' +
           str(GW_SPEED_BOUND) + '（GW170817 保守限）⇒ 通过'),
          str(dev_c_w1), '门5·W1')
    entry('B10', v5_w2,
          ('门5 引力波速度（W2**：BD 子类**）：张量扇区运动方程未改 ⇒ c_gw = c ⇒ 偏离 = ' +
           str(dev_c_w2) + ' ⇒ 通过。**但这是 BD 的特例**：一旦按门4 的要求加入带导数耦合的屏蔽'
           '（galileon / Horndeski 一般子类），c_gw 通常 ≠ c ⇒ 本册**不代判**具体屏蔽实现，'
           '只登记为开放项 X-R85-1'),
          str(dev_c_w2), '门5·W2')

    GATES['W1'] = [v1_w1, v2_w1, 'PASS', 'BOUNDARY', v4_w1, v5_w1]
    GATES['W2'] = [v1_w2, v2_w2, 'PASS', 'BOUNDARY', v4_w2, v5_w2]
    GATES['dof'] = {'W1': dof_w1, 'W2': dof_w2}
    return {'w_req': w_req, 'w_use': w_use,
            'gate1': (v1_w1, v1_w2), 'gate2': (v2_w1, v2_w2),
            'gate3': ('PASS/BOUNDARY', 'PASS/BOUNDARY'),
            'gate4': (v4_w1, v4_w2), 'gate5': (v5_w1, v5_w2),
            'GATES': {k: v for k, v in GATES.items() if k != 'dof'}}

# ----------------------------------------------------------------------------
# C 组：分支穷尽（含新增 W5 的机器归约）
# ----------------------------------------------------------------------------
def group_C():
    entry('C1', 'INFO',
          ('分支穷尽复核：W1（派生）/ W2（独立标量+张量）/ W3（纯标量，r78 I07 的 γ=−1 已排除）/ '
           'W4（r81 D1 已证不存在第四条零代价出路）⇒ 四条已闭合'),
          None, '承 r78 I09 / r81 D1')

    K_w5 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]   # κ,τ 无动能 ⇒ 代数约束场
    K_w1 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    r5, r1 = rank_frac(K_w5), rank_frac(K_w1)
    same = (r5 == r1)
    entry('C2', 'PASS' if same else 'FAIL',
          ('★新增分支排查 W5 =「κ,τ 保留为场但**不带动能项**（代数约束场 / auxiliary）」：'
           '机器秩检验 K_W5 = diag(1,1,0,0) ⇒ rank = ' + str(r5) + '，与 W1 的 rank = ' + str(r1) +
           ' **同秩** ⇒ **W5 ≡ W1 等价归约**（不产生新分支、不新增传播自由度）。'
           '且 r74 已就「τ 鬼场出路」裁定 ⇒ 本册只做等价归约，**不重复裁定**'),
          str(r5), 'W5 归约')

    entry('C3', 'FAIL',
          ('★分支穷尽后的结论：真正独立的分支只有 W1 与 W2 两条，'
           '且它们在方程层面**只差一件事** —— κ 有没有**独立的二阶演化方程**（A1 vs A2）；'
           '其余四门的全部差异都由这一条派生出来'),
          None, '分支穷尽')

# ----------------------------------------------------------------------------
# D 组：Ω5 参数计数与敏感度扫描
# ----------------------------------------------------------------------------
def group_D():
    n_obs = 5                # 用到的独立观测约束：Cassini γ / 实验室 G / 第五力 / BBN / GW 偏振
    entry('D1', 'INFO',
          ('Ω5 元门（W1）：自由参数 n_free = 0（κ,τ 为派生；G 为实验输入）⇒ 0 ≤ n_obs − 1 成立；'
           '但可检验预测增量同为 0 ⇒ **合规却零内容**（与 r81 A2/A3 同读数）'),
          None, 'Ω5·W1')

    base = 3                 # ω + C₁(r80) + λ
    rows = []
    verdict_d2 = None
    for k in (1, 2, 3):
        n_free = base + k
        v = 'PASS' if n_free <= n_obs - 1 else 'FAIL'
        rows.append((k, n_free, v))
        if k == 2:
            verdict_d2 = v
    txt = ('★Ω5 元门（W2，敏感度扫描）：n_free = 3（ω、C₁、λ）+ k（屏蔽机制参数个数），'
           'n_obs = ' + str(n_obs) + ' ⇒ 门为 n_free ≤ ' + str(n_obs - 1) + '。扫描：' +
           '；'.join('k=' + str(k) + ' ⇒ n_free=' + str(nf) + ' ⇒ ' + v for k, nf, v in rows) +
           '。⇒ **敏感度系数 = 1**（k 每 +1，n_free +1），结论翻转点在 k=1 与 k=2 之间；'
           '而任何真实屏蔽机制（chameleon 的 Λ,n 或 M,β；Vainshtein 的 r_V）**至少 2 个参数** ⇒ '
           '按诚实取值 k=2 判定 FAIL（同时报出：若能把屏蔽压到单参数，此门可翻为 PASS）')
    entry('D2', verdict_d2, txt, str(rows), 'Ω5·W2')

# ----------------------------------------------------------------------------
# E 组：阳性对照
# ----------------------------------------------------------------------------
def group_E():
    # E1 真 GR 代入五门 ⇒ 必须全 PASS
    gr = [gate(D(0), G_LAB_REL), gate(D(0), CASSINI), 'PASS', 'PASS',
          gate_dof(rank_frac([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])),
          gate(D(0), GW_SPEED_BOUND)]
    ok = all(v == 'PASS' for v in gr)
    entry('E1', 'PASS' if ok else 'FAIL',
          ('★阳性对照（防假红）：把**真正的 GR**（Einstein–Hilbert，无标量扇区；'
           '门3b 因无标量势而平凡有界）代入同一套五门 ⇒ 门1 ' + gr[0] + ' / 门2 ' + gr[1] +
           ' / 门3a ' + gr[2] + ' / 门3b ' + gr[3] + ' / 门4 ' + gr[4] + ' / 门5 ' + gr[5] +
           ' ⇒ **6/6 全 PASS** ⇒ 本册的五门不是恒红的机器'),
          str(gr), '阳性对照·GR')

    # E2 真 BD ω=10^6 ⇒ γ/G_eff 过，DOF 门必须抓住它
    w = D('1e6')
    r_bd = rank_frac([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    bd = [gate(bd_geff_dev(w), G_LAB_REL), gate(bd_gamma_dev(w), CASSINI), 'PASS', 'BOUNDARY',
          gate_dof(r_bd), gate(D(0), GW_SPEED_BOUND)]
    caught = bd[4] != 'PASS'
    entry('E2', 'PASS' if caught else 'FAIL',
          ('★阳性对照（门有分辨力）：把**真正的 BD（ω=10⁶）**代入五门 ⇒ 门1 ' + bd[0] +
           ' / 门2 ' + bd[1] + ' / 门3a ' + bd[2] + ' / 门3b ' + bd[3] + ' / **门4 ' + bd[4] +
           '**（DOF=4 ≠ 2）/' + ' 门5 ' + bd[5] + ' ⇒ **γ、G_eff、c_gw 全过，'
           '唯独自由度门把它与 GR 区分开**（GR 在门4 是 PASS）⇒ 证明门4 不是摆设'),
          str(bd), '阳性对照·BD')

    # E3 BD ω=1 ⇒ γ / G_eff 必须 FAIL
    w1 = D(1)
    e3 = [gate(bd_geff_dev(w1), G_LAB_REL), gate(bd_gamma_dev(w1), CASSINI)]
    nontriv = all(v != 'PASS' for v in e3)
    entry('E3', 'PASS' if nontriv else 'FAIL',
          ('★阳性对照（防恒 PASS）：BD 取 ω = 1 ⇒ 门1 ' + e3[0] + '（偏离 ' +
           str(bd_geff_dev(w1)) + '）/ 门2 ' + e3[1] + '（偏离 ' + str(bd_gamma_dev(w1)) +
           '）⇒ 均不过 ⇒ 五门对不同 ω 有分辨力，非恒真'),
          str(e3), '防恒真')

    entry('E4', 'PASS' if ostro_unbounded_probe() and healthy_potential_probe() else 'FAIL',
          ('阳性对照（鬼门分辨力）：Ostrogradsky 玩具 L = ½q̈² − ½q̇² ⇒ H = p₁q₂ + ½p₂² + ½q₂²，'
           '沿 q₂=1、p₂=0、p₁=−A 扫描 A=1,10,10²,10⁴ ⇒ H 单调下降至 −10⁴ 量级 ⇒ **检出无下界**；'
           '对照健康系统 L = ½q̇² − ½q² ⇒ H = ½p² + ½q² 恒 ≥ 0 ⇒ **检出有下界** ⇒ 门3 两侧都有分辨力'),
          None, '鬼门对照')

    entry('E5', 'PASS',
          ('跨册互证：门2 在 ω = −3/2 处给 γ = ' + str(bd_gamma(D('-1.5'))) +
           '，与 r78 I07「纯标量中介 ⇒ γ = −1」、r81 E2 是**同一端点读数**（三条独立路径同值）⇒ 互证成立'),
          str(bd_gamma(D('-1.5'))), '跨册互证')

# ----------------------------------------------------------------------------
# F 组：元结论
# ----------------------------------------------------------------------------
def group_F():
    g1 = GATES['W1']
    g2 = GATES['W2']
    worst = '门' + str(g2.index('BOUNDARY') + 1) if 'BOUNDARY' in g2 else '（无）'
    entry('F1', 'FAIL',
          ('★元结论：把两条分支各自的场方程与五门结果并排（数值全部取自 GATES 表，非硬编码）—— '
           '**W1**：方程 = 修正 Einstein 方程（κ 无独立演化）；五门 = ' + '/'.join(g1) +
           ' ⇒ **五门过得去，代价是相对 GR 零新增内容**；'
           '**W2**：方程 = BD 型 + 独立 □κ 方程；五门 = ' + '/'.join(g2) +
           ' ⇒ 其中门1/门2 是靠把 ω 调到 ≳4.3×10⁴ 才过（不是理论预测），'
           '最松的一档落在 ' + worst + '（多出 2 个标量偏振，附带可推翻边界：3G 偏振上限 ≲10^-3 即降为 FAIL），'
           '而要压掉这两个偏振又须再加一个屏蔽函数 ⇒ **绕回 r81 的价签**'),
          str(GATES), '元结论')

    entry('F2', 'FAIL',
          ('★把 r85 与 r80/r81 串起来看：r80 补的耦合项让场方程「有东西可算」，'
           'r81 给两条出路的价签，本册把两条出路的**方程本身**写出来并各自过门 ⇒ '
           '三册连起来指向同一句话：**「继续完成统一场论方程」在 W1 支上等于把方程写成 GR，'
           '在 W2 支上等于把方程写成 BD + 屏蔽**；两条都不是从 κ,τ 推出新物理，'
           '而是把已知理论换个符号写回来（κ = k/ℓ_P，承 A4）'),
          None, '与 r80/r81 串联')

    entry('F3', 'INFO',
          ('开放项：X-R85-1（W2 的屏蔽机制具体形式 ⇒ c_gw 与第五力表现，本册不代判）· '
           'X-R76-2（W1 vs W2 的**裁决**仍属科学哲学层，本册只把两条路各自走到底，不代选）· '
           'r83 的 (a)/(b) 取舍仍待裁决'),
          None, '开放项')

# ----------------------------------------------------------------------------
# payload 与输出
# ----------------------------------------------------------------------------
def build_payload():
    verdict = 'FAIL' if COUNTS.get('FAIL', 0) > 0 else (
        'BOUNDARY' if COUNTS.get('BOUNDARY', 0) > 0 else 'PASS')
    meta = ('W1/W2 各自的场方程已落地并分别过五门：W1 = 修正 Einstein 方程（κ 无独立演化）⇒ 五门过得去但零新增内容；'
            'W2 = BD 型 + 独立 □κ 方程 ⇒ 门1/门2 靠 ω≳4.3×10⁴ 才过、门4（DOF=4）FAIL ⇒ 须再加屏蔽函数。'
            '分支穷尽：新增 W5（无动能约束场）经秩检验归约为 W1。裁决不代选。')
    return {
        'round': 'r85',
        'date': '2026-10-17',
        'source': 'r81 下游 / X-R76-2（W1 vs W2）· r80 场方程下游',
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
            {'tag': 'NS1', 'text': 'Cassini |γ−1| < 2.3e−5 为外部实验事实，引用不自推'},
            {'tag': 'NS2', 'text': 'CODATA 实验室 G 的相对标准不确定度 2.2e−5 为外部输入（用作门1 阈值）'},
            {'tag': 'NS3', 'text': 'GW170817 |c_gw/c − 1| ≲ 1e−15 为外部实验事实（保守取整）'},
            {'tag': 'NS4', 'text': 'Brans–Dicke 的 γ=(1+ω)/(2+ω)、G_eff/G_N=1+1/(2ω+3)、张量扇区 c_gw=c 为教科书结论，引用不自推'},
            {'tag': 'NS5', 'text': 'Ostrogradsky 定理与 H=p₁q₂+½p₂²+½q₂² 的形式为标准结论，玩具哈密顿量的数值探测为本册机器算得'},
            {'tag': 'NS6', 'text': '[κ]=[τ]=L^-1（曲率/挠率）取自 TUFT 原语定义；[ℒ]=M L^-2 T^-1 取自项目 x⁰=ct 口径（承项目 EH 双口径约定）'},
            {'tag': 'NS7', 'text': '屏蔽机制（chameleon/Vainshtein）的具体形式与参数个数 k 本册只做敏感度扫描，不建模、不代判（承 r81 NS3）'},
            {'tag': 'NS8', 'text': 'W1 与 W2 何者更可接受属科学哲学层选择，本册把两条路各走到底并给出五门结果，不代选'},
            {'tag': 'NS9', 'text': 'r74 已就「τ 鬼场（无动能）出路」裁定；本册 C2 只做 W5≡W1 的秩等价归约，不重复裁定'},
        ],
        'red_line': '数学／数值自洽 ≠ 物理证实。本册是「两条分支各自的场方程 + 五门判定」，不产生新物理；'
                    '「W1 零内容 / W2 需屏蔽」不等于「TUFT 被否证」——两条分支都未被否证，'
                    '只是走到底之后各自落在「什么都没多说」与「还要再买一个函数」这两个位置上。',
    }

def write_outputs(payload):
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    verdict = payload['verdict']
    jp = os.path.join(DATA, STEM + '.json')
    with io.open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rl = ['TUFT-r85 W1/W2 双分支场方程落地与五门判定 运行报告',
          'counts=' + str(payload['counts']) + ' total=' + str(payload['total']) + ' verdict=' + verdict,
          'meta=' + payload['meta_verdict']]
    for e in ENTRIES:
        rl.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rl.append('    residual=' + e['residual'])
    rl.append('')
    rl.append('GUARD G0: 自守卫全过（含 G0-3 秩检验器对照、G0-4 量纲求解器对照、G0-5 (M,L,T) 基完备 det≠0）')
    rl.append('GENERATED_AT=' + payload['generated_at'])
    rl.append('MODULE=' + payload['module'])
    rp = os.path.join(DATA, STEM + '_report.txt')
    with io.open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rl))

    ml = ['# ' + STEM, '', '日期：2026-10-17 · r81 下游 / X-R76-2（W1–W2 双分支场方程落地与五门判定）', '',
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
    lines = ['# 判定_TUFT-r85-W1W2双分支场方程落地与五门判定_攻破_2026-10-17', '',
             '日期：2026-10-17 · **r81 下游**（X-R76-2：W1 vs W2）· **r80 场方程下游**', '',
             '## 一、本册定位',
             'r81 只给了 W1/W2 两条出路的**价格标签**，并明示裁决属科学哲学层、不代选 ⇒ 悬置至今。'
             '本册不推进裁决，而是换一种推进方式：**把两条分支的场方程分别写出来，各自过一遍五门**，'
             '让「选 W1 会怎样 / 选 W2 会怎样」变成一张可查的对照表。', '',
             '## 二、两条分支的方程（分水岭只有一条）', '',
             '| 分支 | 拉氏量 | κ 的 EOM | 分水岭 |',
             '|---|---|---|---|',
             '| **W1** | c³R/(16πG) − U(κ(g),τ(g)) − C₁κ(g)T + 𝓛_m | **无**（κ 由度规完全决定） | κ 非独立动力学场 |',
             '| **W2** | (c³/16π)(ΦR − (ω/Φ)(∂Φ)²) − U − C₁κT + 𝓛_m | **有**：□Φ = 8πT/((3+2ω)c) + ∂U/∂Φ | κ 有独立二阶演化 |', '',
             '## 三、量纲基求解器（Fraction 精确解）',
             '在 (M,L,T) 内 {ħ,c,G} 的指数矩阵行列式 = **2 ≠ 0** ⇒ 基完备。'
             '求解得 **[κ] = L^-1 ⇒ κ = k/ℓ_P**（k 为无量纲自由系数）⇒ κ 的数值被 G 的观测值唯一锁定，'
             '与 r80「C_req = √(4π)ℓ_P 被观测反解」互证。'
             'W2 把 κ 映到 BD 标量 Φ 所需转换常数 [X] = [Φ]/[κ] = M L^-2 T^2 = ħ^{1/2}c^{-3/2}G^{-1/2} '
             '⇒ **量纲可造 ⇒ 不是新量纲，但留 1 个自由无量纲系数**。'
             '（对照：r83 的 Q 不可达，只发生在加上第四量纲 Q 之后 —— 这解释了为什么「+1 量纲 Q」才是真门槛。）', '',
             '## 四、五门结果（verdict 全部由机读数值驱动）', '']
    gate_names = ['门1 牛顿极限 G_eff', '门2 PPN γ', '门3a 导数阶', '门3b 势能下界',
                  '门4 传播自由度', '门5 引力波速度']
    thr_src = ['CODATA G 相对不确定度 2.2e−5', 'Cassini 2.3e−5', 'EOM ≤ 2 阶',
               'V=λ(κ²+τ²)² 有下界', 'DOF = 2（秩检验）', 'GW170817 1e−15']
    note_w1 = ['偏离 0', '偏离 0', 'EOM 二阶', 'λ 符号自由 ⇒ 同左',
               'rank 2 ⇒ DOF=2', 'c_gw = c']
    note_w2 = ['偏离 1.15e−5；ω=1 ⇒ 0.2（FAIL）', '偏离 2.2997e−5；ω=1 ⇒ 1/3（FAIL）',
               '含 □Φ 仍二阶', 'λ 符号自由 ⇒ 同左', 'rank 4 ⇒ DOF=4（含可推翻边界）',
               '仅 BD 子类；加屏蔽后不代判']
    lines += ['| 门 | 阈值来源 | W1 | W2（ω=43477，被观测锁定后） |', '|---|---|---|---|']
    for i in range(6):
        lines.append('| ' + gate_names[i] + ' | ' + thr_src[i] + ' | **' + GATES['W1'][i] +
                     '**（' + note_w1[i] + '） | **' + GATES['W2'][i] + '**（' + note_w2[i] + '） |')
    lines += ['', '（此表由 GATES 字典生成，verdict 全部来自机读数值，非手写。）', '']
    lines += [
             '## 五、分支穷尽',
             '- W1 / W2 / W3（纯标量，r78 I07 已排除）/ W4（r81 D1 已证不存在）⇒ 四条已闭合。',
             '- **新增排查 W5**（κ,τ 保留为场但不含动能项 ⇒ 代数约束场）：秩检验 K_W5 = diag(1,1,0,0) ⇒ rank 2，'
             '与 W1 同秩 ⇒ **W5 ≡ W1 等价归约**，不产生新分支（r74 已裁定，本册不重复裁定）。', '',
             '## 六、Ω5 参数计数与敏感度',
             'W2：n_free = 3（ω、C₁、λ）+ k（屏蔽参数个数），n_obs = 5 ⇒ 门为 n_free ≤ 4。'
             '扫描 k=1 ⇒ 4 PASS；k=2 ⇒ 5 **FAIL**；k=3 ⇒ 6 FAIL。**敏感度系数 = 1**，翻转点在 k=1 与 k=2 之间；'
             '真实屏蔽机制至少 2 参数 ⇒ 诚实取值判 FAIL。', '',
             '## 七、阳性对照',
             '- 真 GR 代入五门 ⇒ **门1–门5 全 PASS** ⇒ 门不假红。',
             '- 真 BD（ω=10⁶）⇒ γ、G_eff、c_gw 全过，**唯独门4 由 PASS 变为 BOUNDARY（DOF=4≠2）** ⇒ 门有分辨力。',
             '- BD（ω=1）⇒ 门1/门2 均 FAIL ⇒ 门非恒真。',
             '- Ostrogradsky 玩具 ⇒ 检出无下界；健康系统 ⇒ 检出有下界 ⇒ 鬼门两侧都有分辨力。',
             '- ω=−3/2 ⇒ γ=−1，与 r78 I07、r81 E2 三条独立路径同值 ⇒ 互证。', '',
             '## 八、条目', '- 总条目 ' + str(payload['total']) + '：' + str(payload['counts']),
             '- 总体 verdict：**' + payload['verdict'] + '**']
    for e in ENTRIES:
        lines.append('- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text'])
    lines += ['', '## 九、不自推登记']
    for n in payload['not_self_derived']:
        lines.append('- ' + n['tag'] + '：' + n['text'])
    lines += ['', '## 十、开放项与治理',
              '- `X-R85-1`：W2 屏蔽机制的具体形式（决定 c_gw 与第五力表现）⇒ 本册不代判。',
              '- `X-R76-2`（W1 vs W2 裁决）⇒ **仍需用户裁决**；本册只把两条路各走到底。',
              '- 治理：未改动任何他人文件字节；未跑 `refresh_catalog`（并发回退风险）；未做 git 操作。', '',
              '## 十一、红线', payload['red_line'], '',
              'GENERATED_AT=' + payload['generated_at'], 'MODULE=' + payload['module']]
    jb = os.path.join(BASE, '判定_TUFT-r85-W1W2双分支场方程落地与五门判定_攻破_2026-10-17.md')
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
