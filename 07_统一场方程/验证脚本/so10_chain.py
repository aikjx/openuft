# -*- coding: utf-8 -*-
"""UFE-1 · SO(10) 破缺链统一探针（L10 / L15 阶段二，零第三方依赖）。

问题：`unification_probe.py` 已证明「仅靠添加物质无法实现非 SUSY 一环三耦合统一」
（$\Delta b_3<0$ 对任何物质内容不可达），并把可行路线收窄为 SUSY 或 GUT。
本探针执行其中的 **GUT 路线的具体计算**：

    把 SM 的三个实测耦合从 M_Z 向上跑，逐条穿过 SO(10) 的极大破缺链，
    判定它们是否在一个点相遇；若相遇，给出被预言的 M_GUT、α_GUT⁻¹ 与质子衰变寿命。

与 `unification_probe.py` 的关键差别：那边的 Δb 是**自由参数**（问"需要什么内容"），
这边的新物理内容（SO(10) 的 16 旋量谱 + 中间群）是**给定的**（问"它真的统一吗"），
因此这是一个可判定的问题，而不是可行性规格。

方法上的自立性（本项目不引用文献数值，全部现场推导）：
1. 构造 D5=so(10) 权重格（16/10/45），全程用 **精确有理数 `Fraction`**；
2. U(1) 归一化因子由 $k_X=\\mathrm{Tr}_{16}(X^2)/\\mathrm{Tr}_{16}(T^3_{L}{}^2)=2|X|^2$ **算出**
   （$k_Y=5/3$、$k_{B-L}=8/3$ 是输出而非输入），并对 $k_{B-L}$ 给出两条独立路径互检；
3. **端到端回归**：仅由权重格 + 一个 Higgs 二重态重现 SM 的 $b=(41/10,-19/6,-7)$。
   通过 ⇒ 整套归一化机制可信；任一不通过 ⇒ 本探针不出任何统一结论。

一环约定（与 verify_core.py / unification_probe.py 一致）：
    α_i⁻¹(μ) = α_i⁻¹(M_Z) − (b_i/2π)·ln(μ/M_Z)
阈值匹配：单群子因子 g 相等；U(1) 乘 $k_X$；对角子群 α⁻¹ 相加（$Y=T^3_R+(B-L)/2$ ⇒
α_Y⁻¹ = α_{2R}⁻¹ + α_{B−L}⁻¹/4）。该两步匹配等于一步匹配由测试 S4.1 把守。

数学结构：在一环 + 常数匹配因子 + 阈值全并版下，
    (α_GUT⁻¹, ln M_1, ln M_2, …) ⟼ (α₁⁻¹, α₂⁻¹, α₃⁻¹)(M_Z)
是**严格仿射**映射（由测试 S5 现场验证），故统一方程用精确线性代数求解，
不需要牛顿法或二分搜索。

诚实边界（详见报告 §局限）：
- 只做**一环 + 阈值并版**；阈值修正与二环效应量级为 O(1) 的 α⁻¹，足以拉平小失配，
  因此「不统一」的结论强度受此限制；「统一」也**不**等于「自然界选了它」。
- SO(10) 必然给出质子衰变，与 UFE-1 v1 的 P4（质子绝对稳定）**直接冲突**；
  本报告把该张力量化，不做调和。
- 标量谱（16_H/45_H/126_H/120_H 及其分支规则）未被第一性推导，故按三种内容情形并列报告。

用法： python -B so10_chain.py
产出： SO10链统一报告.md / SO10链统一报告.json
"""
from fractions import Fraction as F
import itertools
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent

# --------------------------------------------------------------- 输入观测量
MZ = 91.1876
ALPHA_MZ = 1.0 / 127.952          # α_em⁻¹(M_Z)
SIN2_MS = 0.23121                 # sin²θ_W(M_Z)
ALPHAS_MZ = 0.1180                # α_s(M_Z)
MPL = 1.22e19

# GUT 归一化下的实测逆耦合（与 unification_probe.py 的 A_MZ 同口径）
A_MZ = ((3.0 / 5.0) * (1.0 - SIN2_MS) / ALPHA_MZ,
        SIN2_MS / ALPHA_MZ,
        1.0 / ALPHAS_MZ)

RESULTS = []


def rec(cid, claim, computed, expected, tol, status, unit='', note=''):
    RESULTS.append({'id': cid, 'claim': claim, 'computed': computed,
                    'expected': expected, 'tolerance': tol, 'unit': unit,
                    'status': status, 'note': note})
    return status == 'PASS'


def exact(cid, claim, computed, expected, note='', unit=''):
    """精确有理数比对：不容忍浮点。"""
    return rec(cid, claim, str(computed), str(expected), '0（精确有理数）',
               'PASS' if computed == expected else 'FAIL', unit, note)


def approx(cid, claim, computed, expected, tol, note='', unit=''):
    den = abs(expected) if expected else 1.0
    good = abs(computed - expected) / den <= tol
    return rec(cid, claim, computed, expected, tol,
               'PASS' if good else 'FAIL', unit, note)


# =============================================================== 权重格引擎
def evec(i):
    v = [F(0)] * 5
    v[i] = F(1)
    return tuple(v)


def neg(a):
    return tuple(-x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


_SGS = [sg for sg in itertools.product([1, -1], repeat=5) if sg.count(-1) % 2 == 0]
_HALF = [tuple(F(s, 2) for s in sg) for sg in _SGS]


def W16():
    """旋量 16 = ½(±1)⁵（负号偶数个）：16 个权重，重数 1。"""
    return list(_HALF)


def W10():
    """向量 10 = ±ε_i。"""
    return [evec(i) for i in range(5)] + [neg(evec(i)) for i in range(5)]


def W45():
    """伴随 45 = ±ε_i±ε_j (i<j) 共 40 个 + 0 权重（重数 5）。"""
    ws = []
    for i in range(5):
        for j in range(i + 1, 5):
            for a in (1, -1):
                for b in (1, -1):
                    v = [F(0)] * 5
                    v[i] = F(a)
                    v[j] = F(b)
                    ws.append(tuple(v))
    return ws + [tuple([F(0)] * 5)] * 5


def multiset(ws):
    d = {}
    for w in ws:
        d[w] = d.get(w, 0) + 1
    return d


def dim(ms):
    return sum(ms.values())


def charges(ws, X):
    return [dot(w, X) for w in ws]


def trace_sq(ws, X):
    """Tr_R(X²) = Σ_λ (λ·X)²。"""
    return sum(c * c for c in charges(ws, X))


def k_of(X):
    """U(1) 归一化因子 k_X = Tr₁₆(X²)/Tr₁₆(T3L²) = 2|X|²（so(10) 典范归一）。"""
    return trace_sq(W16(), X) / trace_sq(W16(), T3L)


# ---- Cartan 方向：二重态荷 = ±1/2（典范归一）
T3L = tuple(F(s, 2) for s in (0, 0, 0, 1, 1))          # ½(ε4+ε5)，|·|²=1/2
T3R = tuple(F(s, 2) for s in (0, 0, 0, 1, -1))         # ½(ε4−ε5)，|·|²=1/2
BL = tuple([F(2, 3)] * 3 + [F(0), F(0)])               # (2/3)(ε1+ε2+ε3)
YHP = tuple(T3R[i] + BL[i] / 2 for i in range(5))      # Y = T3R + (B−L)/2

# 非阿贝尔因子的 Cartan 基（两两正交；长度不必为 1，指标只取比值）
B_SU4 = [evec(0), evec(1), evec(2)]
B_SU3 = [(F(1), F(-1), F(0), F(0), F(0)), (F(1), F(1), F(-2), F(0), F(0))]


def proj_sq(ws, basis):
    """Σ_λ |λ 在该因子 Cartan 子空间上投影|²（basis 两两正交）。"""
    return sum(dot(w, b) * dot(w, b) / dot(b, b) for w in ws for b in basis)


# 锚点：SU(4) 的 4（此处即 {(s4,s5)=(+,+)} 的 4 个权重：3 个色 + 1 个轻子，B−L 迹零）；
#       SU(3) 的 3 = 同组里色指标和为 −1 的那 3 个
_QUAD = [w for w, sg in zip(_HALF, _SGS) if sg[3] == 1 and sg[4] == 1]
_QUAD_SG = [sg for sg in _SGS if sg[3] == 1 and sg[4] == 1]
REF4 = _QUAD                                   # 4 of SU(4)
REF3 = [w for w, sg in zip(REF4, _QUAD_SG) if (sg[0] + sg[1] + sg[2]) == -1]


def index_of(ws, basis, ref_ws, ref_T):
    """因子 A 下多重集 ws 的指标 T(R) = ref_T · proj²(R)/proj²(R_ref)。"""
    return F(ref_T) * proj_sq(ws, basis) / proj_sq(ref_ws, basis)


# ---- 因子表：('SU', n, 手征) 用荷方向；('U1', 方向, 名)
def factor_T(fac, ws):
    """因子 fac 下多重集 ws 的 Σ T（非阿贝尔）或 Σ Q²（阿贝尔），全程有理数。"""
    if fac[0] == 'U1':
        return trace_sq(ws, fac[1])
    if fac[0] == 'SU' and fac[1] == 2:
        return trace_sq(ws, T3L if fac[2] == 'L' else T3R)
    if fac[1] == 4:
        return index_of(ws, B_SU4, REF4, F(1, 2))
    if fac[1] == 3:
        return index_of(ws, B_SU3, REF3, F(1, 2))
    raise ValueError(fac)


def b_of(fac, ferm_ws, scal_ws):
    """一环 b：b = −(11/3)C₂(G) + (2/3)Σ_Weyl T + (1/3)Σ_complex scalar T。"""
    out = F(2, 3) * factor_T(fac, ferm_ws) + F(1, 3) * factor_T(fac, scal_ws)
    if fac[0] == 'SU':
        out -= F(11, 3) * {2: F(2), 3: F(3), 4: F(4), 5: F(5)}[fac[1]]   # C₂(SU N)=N
    return out


# ---- 谱
F3 = W16() * 3                       # 三代费米子（每代 16 个 Weyl 态，含 ν^c）
# 双二重体 Φ(1,2,2)：来自 SO(10) 的 10（10→(6,1,1)⊕(1,2,2)，已验证）
BIDOUBLET = [evec(3), neg(evec(3)), evec(4), neg(evec(4))]
# Σ(1,1,3)_0：SU(2)_R 三重态，B−L=0，Y=(+1,0,−1)。三个权重全落在 45（伴随）里 ⇒ 取自 45_H。
# 注意：**不是** Δ_R(1,1,3)_{B−L=2}（那属 126_H，本探针不实现，见报告 §6）。
SIGMA_R = [tuple(F(s) for s in (0, 0, 0, 1, -1)),
           tuple(F(s) for s in (0, 0, 0, -1, 1)),
           tuple([F(0)] * 5)]
# SM Higgs 二重态 H(1,2)_{+1/2}：{ε4, −ε5} ⇒ T3L=(+½,−½)，Y=(+½,+½)
HD = [evec(3), neg(evec(4))]

# ---- 各相位标度名（供报告）
K_BL = None      # 由引擎填入（=8/3 的推导结果）
K_Y = None       # 由引擎填入（=5/3 的推导结果）


# =============================================================== 一致性测试
def run_engine_tests():
    """全部由权重格推导，不引用任何文献数值；任一 FAIL 则不出统一结论。"""
    global K_BL, K_Y
    p = True
    # --- 表示维度
    p &= exact('S0.1', '旋量 16 的权重数', dim(multiset(W16())), 16)
    p &= exact('S0.2', '向量 10 的权重数', dim(multiset(W10())), 10)
    p &= exact('S0.3', '伴随 45 的权重数（含 0 权重×5）', dim(multiset(W45())), 45)

    # --- 荷的迹：SO(10) 归一化的基准
    p &= exact('S0.4', 'Tr₁₆((T³_L)²)（4 个二重态 × 1/2）', trace_sq(W16(), T3L), 2)
    p &= exact('S0.5', 'Tr₁₆((T³_R)²)', trace_sq(W16(), T3R), 2)
    p &= exact('S0.6', 'Tr₁₆((B−L)²)（q:1/3, ℓ:−1, uᶜdᶜ:−1/3, eᶜ:1, νᶜ:−1）',
               trace_sq(W16(), BL), F(16, 3))
    p &= exact('S0.7', 'Tr₁₆(Y²)（= SM 每代 ΣY² = 10/3）', trace_sq(W16(), YHP), F(10, 3))
    cross = sum(dot(w, T3R) * dot(w, BL) / 2 for w in W16())
    p &= exact('S0.8', 'T³_R ⊥ B−L（16 上交叉项 = 0）', cross, 0,
               '保证 α_Y⁻¹ = α_{2R}⁻¹ + α_{B−L}⁻¹/4 的相加规则成立')
    # --- SM Higgs 二重态的荷：Y 必须两个分量都是 +1/2
    p &= exact('S0.9', 'H(1,2)_{1/2} = {ε₄,−ε₅}：Tr(T³_L²)=1/2', trace_sq(HD, T3L), F(1, 2))
    p &= exact('S0.10', '同一双态：Tr(Y²)=1/2（两分量 Y=+1/2）', trace_sq(HD, YHP), F(1, 2))
    p &= exact('S0.11', '同一双态：B−L=0', trace_sq(HD, BL), 0)

    # --- U(1) 归一化因子（两条独立路径）
    K_Y = k_of(YHP)
    K_BL = k_of(BL)
    p &= exact('S1.1', 'k_Y = 2|Y|² = Tr₁₆(Y²)/Tr₁₆((T³_L)²)', K_Y, F(5, 3),
               '即教科书的 GUT 归一化 5/3；此处为**推导输出**')
    p &= exact('S1.2', 'k_{B−L}（路径 A：so(10) 格点）', K_BL, F(8, 3))
    kbl_B = trace_sq(REF4, BL) / index_of(REF4, B_SU4, REF4, F(1, 2))
    p &= exact('S1.3', 'k_{B−L}（路径 B：SU(4) 内部 Tr₄(B−L)²/T(4) = (4/3)/(1/2)）',
               kbl_B, F(8, 3), '与路径 A 独立，二者必须一致')

    # --- 指标：16 破缺到各因子的 ΣT
    p &= exact('S2.1', 'T(16|SU(4)) ⇒ 16=(4,2,1)+(4̄,1,2)', factor_T(('SU', 4), W16()), 2)
    p &= exact('S2.2', 'T(16|SU(3)_c)（4 个三重态 × 1/2）', factor_T(('SU', 3), W16()), 2)
    p &= exact('S2.3', 'T(16|SU(2)_L)（4 个二重态 × 1/2）', factor_T(('SU', 2, 'L'), W16()), 2)
    p &= exact('S2.4', 'T(16|SU(2)_R)', factor_T(('SU', 2, 'R'), W16()), 2)
    p &= exact('S2.5', 'T(Φ(1,2,2)|SU(2)_L) = 2 个二重态', factor_T(('SU', 2, 'L'), BIDOUBLET), 1)
    p &= exact('S2.6', 'T(Σ(1,1,3)_0|SU(2)_R) = C₂(adj)=2（三重态含 T₃ᴿ=0 分量 ⇒ 复三重态）',
               factor_T(('SU', 2, 'R'), SIGMA_R), 2)
    p &= exact('S2.7', 'Σ(1,1,3)_0 的 $B-L$ 全为 0 且三权重 $\in W(45)$ ⇒ 取自 45_H，'
                       '不是 126_H 的 $\\Delta_R$',
               (sum(dot(w, BL) ** 2 for w in SIGMA_R), all(w in W45() for w in SIGMA_R)),
               (F(0), True),
               '本探针的标量只是**跑动内容**，不含破缺扇区 ⇒ $M_R$ 只能按 $3221\\to LR$ '
               '的匹配标度读，see-saw 推论止于量级（报告 §6）')

    # --- 决定性回归：由格点重现 SM 的 b 系数
    b1 = F(3, 5) * b_of(('U1', YHP, 'Y'), F3, HD)      # α₁=(5/3)α_Y ⇒ b₁=(3/5)b_Y
    b2 = b_of(('SU', 2, 'L'), F3, HD)
    b3 = b_of(('SU', 3), F3, [])
    p &= exact('S3.1', 'SM 的 b₁（3×16 + 1 个 Higgs 二重态）', b1, F(41, 10),
               '与 verify_core.py / unification_probe.py 的 B_SM 同源')
    p &= exact('S3.2', 'SM 的 b₂（同上）', b2, F(-19, 6))
    p &= exact('S3.3', 'SM 的 b₃（同上；νᶜ 色单态 ⇒ 无贡献）', b3, F(-7))
    # --- 情形 C 的 SM 相位增量：只允许物质项（2026-09-23：原实现把规范项重复计入）
    for _i, _fac in enumerate((('U1', YHP, 'Y'), ('SU', 2, 'L'))):
        _add = F(1, 3) * factor_T(_fac, HD) * (F(3, 5) if _fac[0] == 'U1' else 1)
        p &= exact('S3.%d' % (4 + _i),
                   '情形 C 相对情形 B 的 $b_{%d}$ 增量 = 一个二重体的物质贡献（不含规范项）' % (_i + 1),
                   b_SM('C')[_i] - b_SM('B')[_i], _add,
                   '修复前 $b_2$ 被推成 $-31/3$（多扣一份 $SU(2)_L$ 规范贡献）')
    p &= exact('S3.6', '情形 A 与情形 B 的 LR 相位差 = $\Phi(1,2,2)$ 的物质贡献',
               [b_LR('B')[i] - b_LR('A')[i] for i in range(4)],
               [F(1, 3) * factor_T(f, BIDOUBLET) for f in
                (('SU', 3), ('SU', 2, 'L'), ('SU', 2, 'R'), ('U1', BL, 'B-L'))],
               '标量谱只从 LR 相位进 $b$，与阈值探针的逐分量机器同构')

    # --- 匹配规则的自洽：SO(10)→3221→SM 两步 = 一步
    a10 = F(37)                       # 任取一个 α_GUT⁻¹ 做代数检验
    aY2 = a10 + (K_BL * a10) / 4      # α_Y⁻¹ = α_{2R}⁻¹ + α_{(B−L)/2}⁻¹
    p &= exact('S4.1', '两步匹配 (3/5)α_Y⁻¹ = α_GUT⁻¹（对角子群相加规则）',
               aY2 * F(3, 5), a10, '若此式不成立，链的匹配实现有误')
    p &= exact('S4.2', '一步匹配 α_Y⁻¹ = k_Y·α_GUT⁻¹', aY2, K_Y * a10,
               '两步与一步必须给出同一个 α_Y⁻¹')

    # --- 仿射性（保证用精确线性代数求解是合法的，而不是近似）
    #     f(u) = f(0) + J·u；f(0)≠0 是因为 ln M_Z 是常数项（SM 相位下端固定在 M_Z）
    for scn in ('A', 'B'):
        for chain in ('PS422', 'R421', 'R3221'):
            u = [1.37, 33.0, 28.0]
            v = [0.41, 30.5, 25.5]
            tG = 36.0
            f0 = predict(chain, [0.0, 0.0, 0.0], tG, scn)
            fu = predict(chain, u, tG, scn)
            fv = predict(chain, v, tG, scn)
            fuv = predict(chain, [x + y for x, y in zip(u, v)], tG, scn)
            f2 = predict(chain, [2.0 * x for x in u], tG, scn)
            dev = max([abs(fuv[i] - f0[i] - (fu[i] - f0[i]) - (fv[i] - f0[i])) for i in range(3)]
                      + [abs(f2[i] - f0[i] - 2.0 * (fu[i] - f0[i])) for i in range(3)])
            p &= approx('S5.%s' % ('1' if scn == 'A' else '2'),
                        '%s：映射严格仿射 $f(u+v)-f(0)=(f(u)-f(0))+(f(v)-f(0))$' % chain,
                        dev, 0.0, 1e-9,
                        '一环 + 常数匹配 + 阈值并版 ⇒ 无需牛顿迭代；常数项 |f(0)|=%.2f'
                        % max(abs(z) for z in f0))
    return p


# =============================================================== 相位 b 系数
# 每个相位记录：耦合名 → b（有理数）。标量内容按情形（scenario）给定。
SCENARIOS = {
    'A': '仅费米子（3×16；一切标量对 b 的贡献不计）',
    'B': '费米子 + $M_R$ 以上活跃的标量谱 $\Phi(1,2,2)\\subset 10_H$ 与 '
         '$\\Sigma(1,1,3)_0\\subset 45_H$（无 $126_H$ ⇒ 不含能破 $B-L$ 的 $\\Delta_R$）',
    'C': 'B 且 SM 相位多保留一个 Higgs 二重态（双二重体未分裂）',
}


def _scal(phase, scn):
    if scn == 'A':
        return []
    # Φ(1,2,2) 在 M_R 处破缺 ⇒ 在 LR 相位仍活跃；Σ(1,1,3)_0 只在 M_R 之上活跃。
    return {'PS': BIDOUBLET + SIGMA_R,
            '421': BIDOUBLET + SIGMA_R,
            'LR': BIDOUBLET,
            'SM': []}[phase]


def _n_ed(scn):
    return 1 if scn == 'C' else 0


def b_LR(scn):
    return _cached('LR', scn, lambda: [b_of(('SU', 3), F3, _scal('LR', scn)),
                                       b_of(('SU', 2, 'L'), F3, _scal('LR', scn)),
                                       b_of(('SU', 2, 'R'), F3, _scal('LR', scn)),
                                       b_of(('U1', BL, 'B-L'), F3, _scal('LR', scn))])


def b_PS(scn):
    return _cached('PS', scn, lambda: [b_of(('SU', 4), F3, _scal('PS', scn)),
                                       b_of(('SU', 2, 'L'), F3, _scal('PS', scn)),
                                       b_of(('SU', 2, 'R'), F3, _scal('PS', scn))])


def b_421(scn):
    return _cached('421', scn, lambda: [b_of(('SU', 4), F3, _scal('421', scn)),
                                        b_of(('SU', 2, 'L'), F3, _scal('421', scn)),
                                        b_of(('U1', T3R, 'T3R'), F3, _scal('421', scn))])


_BC = {}


def _cached(key, scn, thunk):
    k = (key, scn)
    if k not in _BC:
        _BC[k] = thunk()
    return _BC[k]


def b_SM(scn):
    return _cached('SM', scn, lambda: _b_SM_raw(scn))


def _b_SM_raw(scn):
    n = _n_ed(scn)
    # 多留一个二重体只改变**物质**项：`b_of(…, [], HD)` 会把 $-(11/3)C_2$ 的规范项也算进去，
    # 直接当增量用就等于给 SM 相位重复计入一份 $SU(2)_L$ 规范贡献（2026-09-23 由阈值探针发现）
    inc1 = F(3, 5) * F(1, 3) * factor_T(('U1', YHP, 'Y'), HD)
    inc2 = F(1, 3) * factor_T(('SU', 2, 'L'), HD)
    return [F(41, 10) + n * inc1, F(-19, 6) + n * inc2, F(-7)]


NAMES = {'PS422': ['M_GUT', 'M_PS', 'M_R'],
         'R421': ['M_GUT', 'M_421', 'M_R'],
         'R3221': ['M_GUT', 'M_R']}
NUNK = {'PS422': 3, 'R421': 3, 'R3221': 2}


# =============================================================== 向下跑动
def _run(vals, bs, t_up, t_dn):
    """一个相位内从 t_up 跑到 t_dn：α⁻¹(t_dn) = α⁻¹(t_up) + (b/2π)(t_up − t_dn)。"""
    return [v + float(b) / (2.0 * math.pi) * (t_up - t_dn) for v, b in zip(vals, bs)]


def predict(chain, u, tG, scn):
    """给定未知量 u=[α_GUT⁻¹, lnM₁, lnM₂]，向下积分到 M_Z，返回 (α₁⁻¹,α₂⁻¹,α₃⁻¹)。

    u 的槽位与 NAMES[chain] 去掉 M_GUT 后的中间标度一一对应；tG = ln M_GUT 固定。
    """
    t1 = u[1] if NUNK[chain] > 2 else tG
    t2 = u[2] if NUNK[chain] > 2 else u[1]
    AG = u[0]
    if chain == 'PS422':
        A4, A2L, A2R = _run([AG] * 3, b_PS(scn), tG, t1)
        A3, A2L, A2R, ABL = _run([A4, A2L, A2R, float(K_BL) * A4], b_LR(scn), t1, t2)
    elif chain == 'R421':
        A4, A2L, AR = _run([AG] * 3, b_421(scn), tG, t1)
        A3, A2L, A2R, ABL = _run([A4, A2L, AR, float(K_BL) * A4], b_LR(scn), t1, t2)
    elif chain == 'R3221':
        t1 = u[1]
        A3, A2L, A2R, ABL = _run([AG, AG, AG, float(K_BL) * AG], b_LR(scn), tG, t1)
    else:
        raise ValueError(chain)
    # LR → SM：Y = T3R + (B−L)/2 为对角子群 ⇒ α⁻¹ 相加；α₁⁻¹ = (3/5)α_Y⁻¹
    A1 = (3.0 / 5.0) * (A2R + ABL / 4.0)
    out = _run([A1, A2L, A3], b_SM(scn), t2, math.log(MZ))
    return out


# =============================================================== 精确线性求解
def _solve_n(J, rhs, n):
    """n×n 高斯消元（部分主元）；奇异返回 None。"""
    A = [J[i][:] + [rhs[i]] for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(A[r][c]))
        if abs(A[piv][c]) < 1e-12:
            return None
        A[c], A[piv] = A[piv], A[c]
        for r in range(n):
            if r == c:
                continue
            f = A[r][c] / A[c][c]
            for k in range(c, n + 1):
                A[r][k] -= f * A[c][k]
    return [A[i][n] / A[i][i] for i in range(n)]


def _lstsq(J, rhs, n):
    """正规方程解 m×n（m ≥ n）。"""
    m = len(J)
    A = [[sum(J[k][i] * J[k][j] for k in range(m)) for j in range(n)] for i in range(n)]
    b = [sum(J[k][i] * rhs[k] for k in range(m)) for i in range(n)]
    r = _solve_n(A, b, n)
    return r


def _condition(J, n):
    """$|\\det J|$ 除以三列范数之积 ∈ [0,1]：三列张成的平行体相对体积。

    → 0 表示方程组退化（三个观测量在该链的内容下不再独立），此时解是数值噪声放大，
    不可当结论——与"无解"不同，必须单独标记。
    """
    if n != 3:
        return None
    cols = [[J[i][j] for i in range(3)] for j in range(3)]
    nrm = [math.sqrt(sum(x * x for x in c)) for c in cols]
    if min(nrm) == 0.0:
        return 0.0
    det = (cols[0][0] * (cols[1][1] * cols[2][2] - cols[1][2] * cols[2][1])
           - cols[1][0] * (cols[0][1] * cols[2][2] - cols[0][2] * cols[2][1])
           + cols[2][0] * (cols[0][1] * cols[1][2] - cols[0][2] * cols[1][1]))
    return abs(det) / (nrm[0] * nrm[1] * nrm[2])


def solve_chain(chain, m_gut, scn):
    """固定 M_GUT，解出 (α_GUT⁻¹, 中间标度)；返回解 + 残差 + 物理性判定。"""
    tG = math.log(m_gut)
    n = NUNK[chain]
    # 映射严格仿射（测试 S5）⇒ 常数项 + 探针基向量给矩阵，无截断误差
    f0 = predict(chain, [0.0] * 3, tG, scn)
    cols = [[predict(chain, [1.0 if k == j else 0.0 for k in range(3)], tG, scn)[i] - f0[i]
             for j in range(n)] for i in range(3)]
    J = [[cols[i][j] for j in range(n)] for i in range(3)]
    rhs = [A_MZ[i] - f0[i] for i in range(3)]
    cond = _condition(J, n)
    u = _solve_n(J, rhs, n) if n == 3 else _lstsq(J, rhs, n)
    if u is None:
        return None
    pred = predict(chain, u + [0.0] * (3 - n), tG, scn)
    resid = [pred[i] - A_MZ[i] for i in range(3)]
    spread = max(abs(r) for r in resid)
    full = u + [tG] * (3 - n)
    ts = [tG] + (full[1:] if n == 3 else [full[1]])
    scales = {}
    for name, t in zip(NAMES[chain], ts):
        scales[name] = math.exp(t)
    ag = full[0]
    mr = scales['M_R']
    mid = scales[NAMES[chain][1]] if n == 3 else None
    order = (mr > MZ) and (mid is None or (mid > mr and mid < scales['M_GUT'])) \
        and (scales['M_GUT'] > mr)
    phys = (ag > 0) and order and (scales['M_GUT'] < MPL) and (spread < 1e-6) \
        and (cond is None or cond > 1e-3)
    tau, mx = proton_tau(scales['M_GUT'], ag)
    return {'chain': chain, 'scenario': scn, 'alpha_GUT_inv': ag, 'scales': scales,
            'residual': resid, 'spread': spread, 'condition': cond,
            'degenerate': bool(cond is not None and cond <= 1e-3),
            'ordered': bool(order),
            'physical': bool(phys), 'M_X': mx, 'tau_p_yr': tau,
            'survives_sk': tau > SK_BOUND}


# 每链的未知槽位：'AG'=α_GUT⁻¹, 'M1'/'M2'=中间标度, 'GUT'=M_GUT 本身
# 方程恒为 3 个（三个实测逆耦合）⇒ 未知量数 = 3 时链**预言** M_GUT，<3 时 M_GUT 是输入。
SLOTS = {'PS422': ['AG', 'M1', 'M2'],          # 3 未知 / M_GUT 自由（1 参数族）
         'R421': ['AG', 'M1', 'M2'],
         'R3221': ['AG', 'M1', 'GUT']}         # 3 未知 ⇒ M_GUT 被预言


def predict4(chain, w, scn):
    """w = [AG, t1, t2, tG]（未用槽位忽略）；仿射 ⇒ 用于按任意列装配线性系统。"""
    u = [w[0], w[1], w[2]]
    return predict(chain, u, w[3], scn)


def solve_determined(chain, scn):
    """解 3×3：未知量由 SLOTS 决定；若含 'GUT' 则本链对 M_GUT 给出**预言**。"""
    slots = SLOTS[chain]
    idx = {'AG': 0, 'M1': 1, 'M2': 2, 'GUT': 3}
    cols_i = [idx[s] for s in slots]
    w0 = [0.0, 0.0, 0.0, 36.0]              # tG 基点；映射仿射 ⇒ 基点选择不影响解
    f0 = predict4(chain, w0, scn)
    J = []
    for i in range(3):
        row = []
        for ci in cols_i:
            e = list(w0)
            e[ci] += 1.0
            row.append(predict4(chain, e, scn)[i] - f0[i])
        J.append(row)
    rhs = [A_MZ[i] - f0[i] for i in range(3)]
    cond = _condition(J, 3)
    if cond is not None and cond <= 1e-3:
        return None
    u = _solve_n(J, rhs, 3)
    if u is None:
        return None
    w = list(w0)
    for k, ci in enumerate(cols_i):
        w[ci] = w0[ci] + u[k]              # 仿射：解是相对基点 w0 的增量
    ag, t1, t2, tG = w
    if 'M2' not in slots:
        t2 = t1
    pred = predict4(chain, w, scn)
    resid = [pred[i] - A_MZ[i] for i in range(3)]
    spread = max(abs(r) for r in resid)
    names = NAMES[chain]
    ts = [tG, t1] + ([t2] if 'M2' in slots else [])
    scales = {n: math.exp(t) for n, t in zip(names, ts)}
    mr = scales['M_R']
    mid = scales[names[1]] if len(names) > 2 else None
    order = (mr > MZ) and (mr < scales['M_GUT']) and \
            (mid is None or (mr < mid < scales['M_GUT']))
    tau, mx = proton_tau(scales['M_GUT'], ag)
    return {'chain': chain, 'scenario': scn, 'slots': slots, 'predicts_mgut':
            ('GUT' in slots), 'alpha_GUT_inv': ag, 'scales': scales,
            'residual': resid, 'spread': spread, 'condition': cond,
            'degenerate': bool(cond is not None and cond <= 1e-3),
            'ordered': bool(order),
            'physical': bool((ag > 0) and order and (scales['M_GUT'] < MPL)
                             and spread < 1e-6 and not (cond is not None and cond <= 1e-3)),
            'M_X': mx, 'tau_p_yr': tau, 'survives_sk': tau > SK_BOUND}


def phys_reasons(r):
    """`physical` 为假时**到底**假在哪一条。报告与门禁都只能用它取理由，禁止手写。

    必要性由 2026-09-24 的一次翻案说明：情形 C 曾被"$M_{\\rm GUT}>M_{\\rm Pl}$"排除，
    而那句结论是硬编码的；修掉 $b_2$ 的重复计入后 $M_{\\rm GUT}=2.3\\times10^{16}$ GeV，
    表里的数已经翻了、散文还留着原判 ⇒ 只有把理由接到同一个字典上才会一起翻。
    """
    bad = []
    if not (r['alpha_GUT_inv'] > 0):
        bad.append('$\\alpha_{\\rm GUT}^{-1}\\le0$')
    if not r['ordered']:
        bad.append('标度次序不成立')
    if not (r['scales']['M_GUT'] < MPL):
        bad.append('$M_{\\rm GUT}>M_{\\rm Pl}$')
    if not (r['spread'] < 1e-6):
        bad.append('回代残差过大')
    if r['degenerate']:
        bad.append('方程组退化')
    return bad


def scale_of(r, key):
    """$M_{\\rm GUT}$/$M_R$ 在 `scales` 里、$\\alpha^{-1}$/$\\tau_p$ 在顶层：统一取法。"""
    return r['scales'][key] if key in r['scales'] else r[key]


def sci_tex(x, digits=1):
    """**不带** `$` 定界符：调用方负责包数学环境，嵌套 `$` 会把行内公式切断。"""
    e = int(math.floor(math.log10(x))) if x > 0 else 0
    return '%.*f\\times10^{%d}' % (digits, x / 10.0 ** e, e)


def band_tex(rs, key, f_=None):
    """区间的报告文本：存在的唯一理由是散文与表格必须共用同一批数。"""
    if not rs:
        return '—'
    g = f_ or (lambda x: sci_tex(x))
    lo = min(scale_of(r, key) for r in rs)
    hi = max(scale_of(r, key) for r in rs)
    return g(lo) if lo == hi else '%s,\\ %s' % (g(lo), g(hi))


def end_pair(rs, key):
    """按 `key` 排序后的两端元素（同一对，用来同时报 $M_{\\rm GUT}$ 与 $\\tau_p$ 的倍差）。"""
    if not rs:
        return None
    lo = min(rs, key=lambda r: scale_of(r, key))
    hi = max(rs, key=lambda r: scale_of(r, key))
    return lo, hi, scale_of(hi, key) / scale_of(lo, key)


# ------------------------------------------------- 质子衰变（标定式，见报告）
SU5_REF_MX = 10 ** 14.6     # GeV，最小 SU(5) 的 X 玻色子质量（被实验排除的对照）
SU5_REF_TAU = 1.0e29        # yr，最小 SU(5) 的经典量级
SU5_REF_A_GUT = 41.0
SK_BOUND = 2.4e34           # yr，Super-K τ(p→e⁺π⁰) 下限
M_X_RATIO = 1.0 / math.sqrt(2.0)


def proton_tau(m_gut, a_gut_inv):
    """τ ∝ M_X⁴/α_GUT²，以最小 SU(5) 为锚点的**量级标定**（非第一性推导）。

    未计入：重子算子短程 QCD 增强因子、强子矩阵元 α_H、手征抑制 —— 它们带来
    约 1 个数量级的系统不确定度，故这里只用于与实验下限做**量级**比较。
    """
    m_x = m_gut * M_X_RATIO
    tau = SU5_REF_TAU * (m_x / SU5_REF_MX) ** 4 * (a_gut_inv / SU5_REF_A_GUT) ** 2
    return tau, m_x


# ------------------------------------------------- I 型 see-saw（用解出的 M_R）
V_EW_GEV = 246.22
M_NU_EV = 0.050            # sqrt(Δm²_atm)，只到量级：轻中微子质量本征值未测 CP/序


def seesaw_y_nu(m_r):
    """m_ν = m_D²/M_R，m_D = y_ν v/√2 ⇒ y_ν = √(m_ν M_R)·√2/v。

    这里 $M_R$ 是**规范统一解出的** $SU(2)_R\\times U(1)_{B-L}$ 破缺标度，
    不是自由输入 —— 与 09 文档 L15 阶段二的 see-saw 表同口径（该表把 $M_R$ 当输入）。
    """
    m_nu_gev = M_NU_EV * 1e-9
    return math.sqrt(m_nu_gev * m_r) * math.sqrt(2.0) / V_EW_GEV


def min_spread_scan(chain, scn, lo=10 ** 13.0, hi=10 ** 22.0, rounds=60):
    """超定链（未知量少于方程）：对 $M_{\\rm GUT}$ 取残差散布的最小值。

    窗上界取到 $10^{22}$ GeV（远超 $M_{\\rm Pl}$），使得"根落在非物理区"的情形
    也能被窗口覆盖，从而 S6 的两方法互检不是空转。
    """
    def f(m):
        r = solve_chain(chain, m, scn)
        return r['spread'] if r else float('inf')
    a, b = math.log(lo), math.log(hi)
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = f(math.exp(c)), f(math.exp(d))
    for _ in range(rounds):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = f(math.exp(c))
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = f(math.exp(d))
    m = math.exp(0.5 * (a + b))
    r = solve_chain(chain, m, scn)
    return m, r['spread'], r


def ordering_window(chain, scn, lo=10 ** 13.0, hi=10 ** 21.0, n=160):
    """双阈链：$M_Z<M_R<M_{\\rm int}<M_{\\rm GUT}$ 成立的 $M_{\\rm GUT}$ **窗口**。

    次序对 $M_{\\rm GUT}$ **不单调**（低端 $M_R$ 反超 $M_{\\rm int}$，高端 $M_{\\rm int}$ 越过
    $M_{\\rm GUT}$）⇒ 不能用二分法定边界，先网格定位再两侧各细化一次。
    返回 (窗口下沿, 窗口上沿) 或 None；给的是**首个到末个**成立点之间的包络，
    故若成立集合内部有空洞，这里是保守（偏大）的窗口——网格上的空洞数一并打印。
    上沿取到 $10^{21}$ GeV：窗口必须**覆盖到 $M_{\\rm Pl}$ 之上**，否则"$M_{\\rm GUT}$ 越过
    $M_{\\rm Pl}$"这类判断可能只是网格端点的产物 ⇒ 端点是方法参数，不进结论。
    （情形 C 曾被判为该情形而排除，实际原因是 $b_2$ 重复计入 —— 见 `phys_reasons` 文档串。）
    """
    g = lambda m: bool(solve_chain(chain, m, scn)['ordered'])
    grid = [lo * (hi / lo) ** (k / float(n)) for k in range(n + 1)]
    ok = [g(m) for m in grid]
    if not any(ok):
        return None
    k0 = ok.index(True)
    k1 = len(ok) - 1 - ok[::-1].index(True)
    if ok[k0:k1 + 1].count(False):
        print('  [warn] %s/情形%s：次序窗口内有 %d 个网格空洞 ⇒ 窗口是包络'
              % (chain, scn, ok[k0:k1 + 1].count(False)))

    def refine(a, b):                # g(a)=False, g(b)=True ⇒ 返回边界
        for _ in range(50):
            mid = math.sqrt(a * b)
            if g(mid):
                b = mid
            else:
                a = mid
        return math.sqrt(a * b)

    wlo = refine(grid[k0 - 1], grid[k0]) if k0 > 0 else grid[0]
    whi = refine(grid[k1 + 1], grid[k1]) if k1 < len(grid) - 1 else grid[-1]
    return wlo, whi


def mgut_floor(chain, scn):
    """解出 τ_p = Super-K 下限 所对应的 M_GUT（在固定 α_GUT⁻¹ 的自洽解上扫描）。"""
    lo, hi = 10 ** 13.0, MPL
    f = lambda m: (lambda s: (math.log(s['tau_p_yr']) if s else None))(solve_chain(chain, m, scn))
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        v = f(mid)
        if v is None:
            return None
        if v < math.log(SK_BOUND):
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


def run_solution_tests(det, scan, bounds):
    """对**解**的自检（不通过则数字作废，但不影响引擎结论）。"""
    p = True
    for scn in ('A', 'B', 'C'):
        r = det[scn]
        if r is None:
            p &= rec('S6.%s1' % scn, 'R3221 情形%s：方程组是否退化' % scn,
                     '退化（相对体积 ≤1e-3）', '非退化', '—', 'FAIL', '',
                     '该情形下三个观测量不再独立 ⇒ 无有限解')
            continue
        p &= rec('S6.%s1' % scn, 'R3221 情形%s：解回代三耦合的残差' % scn,
                 r['spread'], 0.0, 1e-9,
                 'PASS' if r['spread'] < 1e-9 else 'FAIL', '',
                 'M_GUT=%.4e GeV, α_GUT⁻¹=%.3f, M_R=%.4e GeV'
                 % (r['scales']['M_GUT'], r['alpha_GUT_inv'], r['scales']['M_R']))
        m, sp, _ = scan[scn]
        rel = abs(m - r['scales']['M_GUT']) / r['scales']['M_GUT']
        p &= rec('S6.%s2' % scn, 'R3221 情形%s：两独立方法定同一 M_GUT'
                 '（3×3 精确解 vs 残差最小化）' % scn,
                 rel, 0.0, 1e-3,
                 'PASS' if rel < 1e-3 else 'FAIL', '',
                 '精确解 %.4e vs 扫描 %.4e GeV（残差 %.1e）'
                 % (r['scales']['M_GUT'], m, sp))
        for chain in ('PS422', 'R421'):
            bd = bounds.get((chain, scn))
            tag = 'a' if chain == 'PS422' else 'b'
            if not bd:
                p &= rec('S6.%s3%s' % (scn, tag), '%s 情形%s：窗口上沿 = 3221 的 $M_{\\rm GUT}$'
                         '预言' % (chain, scn), '无次序窗口', '有窗口', '—', 'FAIL', '',
                         '该链的标度次序在网格上从不成立 ⇒ 无公共上沿可比')
                continue
            rel = abs(bd[1] / r['scales']['M_GUT'] - 1.0)
            p &= rec('S6.%s3%s' % (scn, tag),
                     '%s 情形%s：次序窗口上沿 = 3221 的 $M_{\\rm GUT}$ 预言' % (chain, scn),
                     rel, 0.0, 1e-9,
                     'PASS' if rel < 1e-9 else 'FAIL', '',
                     '$M_{\\rm int}\\to M_{\\rm GUT}$ 时中间相位宽度归零，'
                     '的 $M_R\\to M_{\\rm GUT}$ 区间跑动退化为纯 $3221$ ⇒ 两量必然相等'
                     '（同一极限，不是独立的第三条信息）；'
                     '窗口 $[%.4e,%.4e]$ vs 预言 %.4e GeV'
                     % (bd[0], bd[1], r['scales']['M_GUT']))
    return p


def run_prose_gates(det):
    """钉住"结论性散文与表格同源"这件事——门禁对象是**报告写法**，不是物理。

    为什么需要：台账 F4（"情形 C 给出 $M_{\\rm GUT}>M_{\\rm Pl}$ ⇒ 非物理"）曾是写在报告模板里的
    一句**手写**结论，而它依据的数是算出来的 ⇒ 修掉 $b_2$ 的重复计入后表里的数翻了、散文留着原判，
    同一份报告自相矛盾、08 台账带着一条判据已失效的证伪。把理由接到解上（`phys_reasons`）只是必要条件；
    还需要把"当前哪些情形被判非物理"这个**集合**钉成门禁，数值一动才会同时惊动表格、散文与台账。
    """
    p = True
    phys = [r for r in det.values() if r is not None]
    desync = [r['scenario'] for r in phys if bool(phys_reasons(r)) != (not r['physical'])]
    p &= exact('S7.1', '`phys_reasons` 非空 $\\Longleftrightarrow$ `physical` 为假（理由与判据同源）',
               '、'.join(desync) or '无失联情形', '无失联情形',
               '若有人改 `physical` 的定义而漏改 `phys_reasons`，此项立刻 FAIL')
    bad = sorted(r['scenario'] for r in phys if not r['physical'])
    p &= exact('S7.2', '被三条判据（正耦合 + 次序 + $M_{\\rm GUT}<M_{\\rm Pl}$）判非物理的情形集合',
               '、'.join(bad) or '空集', '空集',
               '**这条就是 F4 撤销的钉子**：数值改动若让任一情形再次被判非物理，此项 FAIL ⇒ '
               '必须显式重写 08 的证伪台账并给出新理由，不允许散文悄悄跟着翻')
    p &= exact('S7.3', '通过 Super-K 下限（$\\tau_p>2.4\\times10^{34}$ yr，独立于 `physical`）的情形集合',
               '、'.join(sorted(r['scenario'] for r in phys if r['survives_sk'])) or '空集',
               'A、B、C', '阈值/二环修正把 $\\tau_p$ 推下到限之下时此项 FAIL ⇒ §5 的'
                          '"不被现有数据排除"必须改写')
    for tag, (want, patch) in enumerate((
            ('$\\alpha_{\\rm GUT}^{-1}\\le0$', {'alpha_GUT_inv': -1.0}),
            ('标度次序不成立', {'ordered': False}),
            ('$M_{\\rm GUT}>M_{\\rm Pl}$', {'M_GUT': MPL * 10.0}),
            ('回代残差过大', {'spread': 1.0}),
            ('方程组退化', {'degenerate': True}))):
        hit = 0
        for r in phys:
            q = dict(r)
            for k, v in patch.items():
                if k == 'M_GUT':
                    q['scales'] = dict(r['scales'], M_GUT=v)
                else:
                    q[k] = v
            if want in phys_reasons(q):
                hit += 1
        p &= exact('S7.4%s' % 'abcde'[tag],
                   '植入判据缺陷 %s 后 `phys_reasons` 必须报出该条（变异测试，防判据空转）' % want,
                   '%d/%d 命中' % (hit, len(phys)), '%d/%d 命中' % (len(phys), len(phys)),
                   '理由函数只会"报告"是不够的：必须证明它每条都真的能触发')
    return p


# =============================================================== 基准对照
def min_spread(b, a=None, lo=1e3, hi=1e19, n=6000):
    a = a or A_MZ
    best, best_mu = None, None
    for k in range(n + 1):
        lnmu = math.log(lo) + k * (math.log(hi) - math.log(lo)) / n
        vals = [a[i] - b[i] / (2.0 * math.pi) * lnmu for i in range(3)]
        s = max(vals) - min(vals)
        if best is None or s < best:
            best, best_mu = s, math.exp(lnmu)
    return best, best_mu


# =============================================================== 主流程
MGUTS = [10 ** 14.0, 10 ** 15.0, 10 ** 16.0, 10 ** 17.0, 10 ** 18.0]


def main():
    eng_ok = run_engine_tests()
    rows = []
    if eng_ok:
        for scn in ('A', 'B', 'C'):
            for chain in ('PS422', 'R421', 'R3221'):
                for m in MGUTS:
                    r = solve_chain(chain, m, scn)
                    r['mgut_input'] = m
                    rows.append(r)
    # 基准：SM 单阈散布（与 R1 / unification_probe 同口径）
    sm_spread, sm_mu = min_spread([41.0 / 10.0, -19.0 / 6.0, -7.0])
    mssm_spread, mssm_mu = min_spread([33.0 / 5.0, 1.0, -3.0])
    floors, mins, bounds = {}, {}, {}
    det, scan = {}, {}
    if eng_ok:
        for scn in ('A', 'B', 'C'):
            det[scn] = solve_determined('R3221', scn)
            scan[scn] = min_spread_scan('R3221', scn)
            for chain in ('PS422', 'R421', 'R3221'):
                floors[(chain, scn)] = mgut_floor(chain, scn)
                if chain == 'R3221':
                    mins[(chain, scn)] = scan[scn]
                else:
                    bounds[(chain, scn)] = ordering_window(chain, scn)
    sol_ok = True
    if eng_ok:
        # 分开求值再用 `and` 合并：`f() and g()` 会在 S6 失败时**跳过** S7，
        # 报告里缺的恰恰是最该被看到的那几行
        s6 = run_solution_tests(det, scan, bounds)
        s7 = run_prose_gates(det)
        sol_ok = s6 and s7

    write_report(eng_ok, sol_ok, rows, (sm_spread, sm_mu), (mssm_spread, mssm_mu),
                 floors, mins, bounds, det)
    print('SO(10) 破缺链统一探针（一环）')
    print('  全部门禁（引擎+解+散文）：%s（%d 项，PASS %d）' %
          ('全部通过 ⇒ 归一化机制可信' if eng_ok else '存在 FAIL ⇒ 不出统一结论',
           len(RESULTS), sum(1 for r in RESULTS if r['status'] == 'PASS')))
    for r in RESULTS:
        if r['status'] != 'PASS':
            print('    [FAIL] %-6s %s：算得 %s，应为 %s' %
                  (r['id'], r['claim'], r['computed'], r['expected']))
    if eng_ok:
        for chain in ('PS422', 'R421', 'R3221'):
            for scn in ('A', 'B'):
                best = [r for r in rows if r['chain'] == chain and r['scenario'] == scn
                        and r['physical']]
                tag = '%s / 情形%s' % (chain, scn)
                if not best:
                    print('  %-16s 网格上无物理解（R3221 因固定 M_GUT ⇒ 残差非零；'
                          '释放 M_GUT 后见下）' % tag)
                else:
                    r = best[0]
                    print('  %-16s 物理解 %d 个；首个 M_PS/M_421=%.2e M_R=%.2e α_GUT⁻¹=%.2f'
                          % (tag, len(best),
                             r['scales'][NAMES[chain][1]], r['scales']['M_R'],
                             r['alpha_GUT_inv']))
        for chain in ('PS422', 'R421', 'R3221'):
            for scn in ('A', 'B'):
                fl = floors.get((chain, scn))
                bd = bounds.get((chain, scn))
                mn = mins.get((chain, scn))
                extra = ('；次序窗口 M_GUT∈[%.2e,%.2e]' % bd) if bd else \
                    (('；不可约散布 %.3f @ %.2e GeV' % (mn[1], mn[0])) if mn else '')
                print('  %-16s 情形%s：τ_p 下限 ⇒ M_GUT ≳ %.2e GeV%s' %
                      (chain, scn, fl, extra))
        print('  基准：SM 单阈散布 %.4f（%.2e GeV）；MSSM %.4f（%.2e GeV）'
              % (sm_spread, sm_mu, mssm_spread, mssm_mu))
        print('  单阈链 3221 的 M_GUT 预言（3 方程 / 3 未知 ⇒ 唯一确定）：')
        for scn in ('A', 'B', 'C'):
            r = det[scn]
            if r is None:
                print('    情形%s：方程组退化 ⇒ 该情形无有限解' % scn)
                continue
            print('    情形%s：M_GUT=%.3e GeV, α_GUT⁻¹=%.2f, M_R=%.3e GeV, '
                  'τ_p=%.2e yr ⇒ %s（条件数 %.1e）' % (scn, r['scales']['M_GUT'],
                  r['alpha_GUT_inv'], r['scales']['M_R'], r['tau_p_yr'],
                  '物理解' if r['physical'] else '非物理', r['condition']))
        print('  解与散文同源自检 S6+S7：%s' % ('全部通过' if sol_ok else '存在 FAIL ⇒ 数字作废'))
    print('产出：SO10链统一报告.md / .json')
    return 0 if eng_ok else 1


def write_report(eng_ok, sol_ok, rows, base_sm, base_mssm, floors, mins, bounds, det):
    L = ['# SO(10) 破缺链一环统一探针报告', '',
         '由 [so10_chain.py](so10_chain.py) 自动生成，**零第三方依赖**。',
         '所有归一化因子由 D5=$\\mathfrak{so}(10)$ 权重格用精确有理数**现场推导**；'
         '端到端回归重现 SM 的 $b=(41/10,-19/6,-7)$ 后才出结论。', '',
         '## 0. 为什么做这个计算', '',
         '`unification_probe.py` 给出的是**可行性规格**（"要统一需要什么样的 Δb"），',
         '并证明 $\\Delta b_3<0$ 对任何物质内容不可达 ⇒ 非 SUSY 一环统一**不能**靠加粒子凑出来。',
         '本探针改做**给定内容**的判定：SO(10) 的三代 $16$ 旋量谱 + 极大破缺链是写死的，',
         '于是"统不统一"变成一个有唯一答案的问题。', '',
         '## 1. 门禁自检全表', '',
         '| 编号 | 命题 | 算得 | 应为 | 容差 | 状态 |', '|---|---|---|---|---|---|']
    for r in RESULTS:
        # 命题里出现的裸 | 会被 Markdown 当成列分隔符（$2|Y|^2$、$T(16|SU(4))$ 都曾把整行拆断）
        L.append('| %s | %s | %s | %s | %s | %s |' %
                 (r['id'], str(r['claim']).replace('|', '\\|'), r['computed'], r['expected'],
                  r['tolerance'], r['status']))
    fams = sorted({r['id'].split('.')[0] for r in RESULTS})
    n_pass = sum(1 for r in RESULTS if r['status'] == 'PASS')
    L += ['',
          '**门禁**：%s 共 %d 项，PASS %d。%s' %
          ('、'.join(fams), len(RESULTS), n_pass,
           '⇒ 归一化机制、解、以及"结论性散文与表格同源"三件事都可信，下面的数字可以给出。'
           if (eng_ok and sol_ok) else
           '**存在 FAIL ⇒ 本探针不出任何统一结论**，下表仅存档。'),
          '',
          '其中三项是关键：',
          '* **S1.1** $k_Y=5/3$ —— 教科书 GUT 归一化在此是**输出**，不是引用；',
          '* **S1.3** $k_{B-L}=8/3$ 由 so(10) 格点与 SU(4) 内部两条独立路径同时给出；',
          '* **S3.1–S3.3** 只用权重格 + 一个 Higgs 二重态重现 $b=(41/10,-19/6,-7)$ —— '
          '若归一化、指标、$C_2$、三代计数中任一处有误，这一项不可能通过。',
          '* **S4.1/S4.2** $SO(10)\\to 3221\\to SM$ 的**两步匹配等于一步匹配**，'
          '即对角子群规则 $\\alpha_Y^{-1}=\\alpha_{2R}^{-1}+\\alpha_{B-L}^{-1}/4$ 与 $k_Y$ 自洽。',
          '',
          '## 2. 三条破缺链', '',
          '| 链 | 中间群 | 未知量 | 方程数 |', '|---|---|---|---|',
          '| PS422 | $SU(4)_c\\times SU(2)_L\\times SU(2)_R$ → $3221$ → SM | '
          '$\\alpha_{\\rm GUT}^{-1},\\,M_{PS},\\,M_R$ | 3 |',
          '| R421 | $SU(4)_c\\times SU(2)_L\\times U(1)_R$ → $3221$ → SM | '
          '$\\alpha_{\\rm GUT}^{-1},\\,M_{421},\\,M_R$ | 3 |',
          '| R3221 | $SU(3)_c\\times SU(2)_L\\times SU(2)_R\\times U(1)_{B-L}$ → SM | '
          '$\\alpha_{\\rm GUT}^{-1},\\,M_R$ | 3（超定） |',
          '',
          '标度名固定为 $M_{\\rm GUT}$（输入网格）+ 表中未知标度；'
          '一环 + 常数匹配 + 阈值并版 ⇒ 映射 $(\\alpha_{\\rm GUT}^{-1},\\ln M_i)\\mapsto '
          '(\\alpha_i^{-1})(M_Z)$ **严格仿射**（测试 S5），故用精确线性代数求解。', '',
          '物质内容三种情形（费米子固定为 $3\\times 16$，含 $\\nu_R$；标量按下面处理）：', '']
    for k, v in SCENARIOS.items():
        L.append('* **情形 %s**：%s' % (k, v))
    L += ['',
          '## 3. 解（固定 $M_{\\rm GUT}$，解出其余标度与 $\\alpha_{\\rm GUT}^{-1}$）', '']
    if not rows:
        L.append('（引擎未通过自检，无输出。）')
    else:
        L += ['判定列：**次序** = $M_Z<M_R<M_{\\rm int}<M_{\\rm GUT}$；'
              '**SK** = $\\tau_p>2.4\\times10^{34}$ yr；'
              '**条件数** = 方程组三列张成平行体的相对体积，$\\le10^{-3}$ 记为"退化"'
              '（三个观测量在该内容下不再独立 ⇒ 该行数字无意义，不是解）。', '']
        for scn in ('A', 'B', 'C'):
            L += ['### 情形 %s：%s' % (scn, SCENARIOS[scn]), '',
                  '| 链 | $M_{\\rm GUT}$(GeV) | $\\alpha_{\\rm GUT}^{-1}$ | '
                  '$M_{\\rm int}$(GeV) | $M_R$(GeV) | 残差散布 | 次序 | SK | 条件数 |',
                  '|---|---|---|---|---|---|---|---|---|']
            for chain in ('PS422', 'R421', 'R3221'):
                for r in [x for x in rows if x['chain'] == chain and x['scenario'] == scn]:
                    mname = NAMES[chain][1]
                    cd = '退化' if r['degenerate'] else (
                        '%.0e' % r['condition'] if r['condition'] else '—')
                    if chain == 'R3221':
                        L.append('| %s | %.0e | %.2f | — | %.3e | %.1e | %s | %s | %s |' %
                                 (chain, r['mgut_input'], r['alpha_GUT_inv'],
                                  r['scales']['M_R'], r['spread'],
                                  '是' if r['ordered'] else '否',
                                  '是' if r['survives_sk'] else '否', cd))
                    else:
                        L.append('| %s | %.0e | %.2f | %.3e | %.3e | %.1e | %s | %s | %s |' %
                                 (chain, r['mgut_input'], r['alpha_GUT_inv'],
                                  r['scales'][mname], r['scales']['M_R'], r['spread'],
                                  '是' if r['ordered'] else '否',
                                  '是' if r['survives_sk'] else '否', cd))
            L.append('')
    L += ['',
          '## 3.5 解空间的结构（本探针真正可辩护的结论）', '',
          '把 §3 读成"链 A/B 统一、链 C 不统一"是**误读**：PS422/R421 有 3 个未知量去拟合 '
          '3 个观测量，命中是参数计数的必然，不是证据。有内容的是两个**边界**：', '',
          '### (i) 双阈链：标度次序只在一段 $M_{\\rm GUT}$ **区间**内成立', '',
          '$M_Z<M_R<M_{\\rm int}<M_{\\rm GUT}$ 不自动成立，且**两端都会坏**：$M_{\\rm GUT}$ 太低时',
          '解把 $M_R$ 顶到 $M_{\\rm int}$ 之上，太高时 $M_{\\rm int}$ 越过 $M_{\\rm GUT}$',
          '（§3 中"次序=否"的行各占一端）。⇒ 次序不是"超过某个阈值就好了"，而是一段窗口；',
          '再与 §5 的质子寿命下限取交集，才是该链真正存活的 $M_{\\rm GUT}$ 带：', '',
          '| 链 | 情形 | 次序成立的 $M_{\\rm GUT}$ 窗口 (GeV) | $\\tau_p$ 下限 | 存活带 (GeV) |',
          '|---|---|---|---|---|']
    for (chain, scn), bd in sorted(bounds.items()):
        fl = floors.get((chain, scn))
        if not bd:
            L.append('| %s | %s | 整个网格内均不成立 | %s | 空 |' %
                     (chain, scn, ('%.2e' % fl) if fl else '—'))
            continue
        lo = max(bd[0], fl) if fl else bd[0]
        L.append('| %s | %s | $[%.3e,\\ %.3e]$ | %s | %s |' %
                 (chain, scn, bd[0], bd[1], ('%.2e' % fl) if fl else '—',
                  ('$[%.3e,\\ %.3e]$' % (lo, bd[1])) if lo < bd[1] else '空'))
    L += ['',
          '**窗口上沿不是自由数**：$M_{\\rm int}\\to M_{\\rm GUT}$ 时中间相位宽度归零，',
          '$M_R\\to M_{\\rm GUT}$ 之间的跑动退化为纯 $3221$ ⇒ 上沿**必然**等于 (ii) 中',
          '$3221$ 链独自解出的 $M_{\\rm GUT}$（测试 S6.A3a … S6.C3b 共 6 项：两条链 × 三种情形，'
          '相对偏差 $\\le10^{-12}$，即浮点噪声）。这既是三链的一致性检验，也是一条**限制**：',
          '三条破缺链在此口径下只给出**一个** $M_{\\rm GUT}$ 数，不是三个互相独立的确认。', '',
          '### (ii) 单阈链 $3221$：固定 $M_{\\rm GUT}$ 时残差非零，但存在唯一零点', '',
          '$SO(10)\\to 3221\\to SM$ 只有 $M_R$ 与 $\\alpha_{\\rm GUT}^{-1}$ 两个未知量去拟合 '
          '3 个方程 ⇒ 固定 $M_{\\rm GUT}$ 时一般**超定无解**。沿 $M_{\\rm GUT}$ 扫描残差散布：', '',
          '| 情形 | 残差趋零的位置 (GeV) | 该点最小散布 $\\Delta\\alpha^{-1}$ | 该点 $M_R$ (GeV) |',
          '|---|---|---|---|']
    for (chain, scn), (m, sp, r) in sorted(mins.items()):
        L.append('| %s | %.3e | %.1e | %.3e |' % (scn, m, sp, r['scales']['M_R']))
    L += ['',
          '散布不是"压不下去的常数"，而是**在唯一一处归零** —— 这不是巧合，而是下一节的预言机制。', '',
          '## 3.6 本探针唯一的正面数字：$3221$ 链把 $M_{\\rm GUT}$ 定死', '',
          '把 $M_{\\rm GUT}$ 从输入改为未知量，参数量账本变成：', '',
          '| 链 | 未知量 | 方程数 | 结论类型 |', '|---|---|---|---|',
          '| PS422 | $\\alpha_{\\rm GUT}^{-1},M_{PS},M_R,M_{\\rm GUT}$ | 3 | '
          '1 参数族：**不**预言 $M_{\\rm GUT}$，只预言 $M_{PS}(M_{\\rm GUT})$、'
          '$M_R(M_{\\rm GUT})$ 与 $\\tau_p(M_{\\rm GUT})$ |',
          '| R421 | $\\alpha_{\\rm GUT}^{-1},M_{421},M_R,M_{\\rm GUT}$ | 3 | 同上 |',
          '| R3221 | $\\alpha_{\\rm GUT}^{-1},M_R,M_{\\rm GUT}$ | 3 | '
          '**唯一解**：$M_{\\rm GUT}$ 被三个实测耦合钉死 ⇒ 可单点证伪 |',
          '',
          '由于映射严格仿射，该解由 $3\\times3$ 线性方程组**精确**给出（测试 S6.1 回代残差 '
          '$<10^{-9}$；测试 S6.2 用独立的黄金分割残差最小化复核同一位置，两者相对偏差 $<10^{-3}$）：', '',
          '| 情形 | $M_{\\rm GUT}$ (GeV) | $\\alpha_{\\rm GUT}^{-1}$ | $M_R$ (GeV) | '
          '$\\tau(p\\to e^+\\pi^0)$ (yr) | 物理性 | 超-K 下限 |', '|---|---|---|---|---|---|---|']
    phys = [r for r in det.values() if r is not None]
    good = [r for r in phys if r['physical']]
    bad = [r for r in phys if not r['physical']]
    # `physical` 只含三条判据（①正耦合 ②次序 ③低于 $M_{\\rm Pl}$），**不含**质子寿命；
    # 任何写"不被现有数据排除"的句子都必须显式引用这个集合，不能引用 `good`。
    sk_ok = [r for r in good if r['survives_sk']]
    tau_lo = min((scale_of(r, 'tau_p_yr') for r in good), default=None)
    d_sk = math.log10(tau_lo / SK_BOUND) if tau_lo else 0.0
    names = lambda rs: '/'.join(r['scenario'] for r in rs) or '无'
    A2 = lambda x: '%.2f' % x
    pr = end_pair(good, 'M_GUT')
    HK_REACH = 1.0e35          # Hyper-K / DUNE 量级的可及范围（只到数量级）
    d_hk = math.log10(tau_lo / HK_REACH) if tau_lo else 0.0
    rel_hk = '（无物理解 ⇒ 无可及性可谈）' if tau_lo is None else \
        ('仍高出 %.1f 个数量级 ⇒ **本探针在实践上近期不可证伪**。' % d_hk if d_hk > 0 else
         '已低到其之下（差 %.1f 个数量级）⇒ 该情形**近期可检验或已被排除**，'
         '不可再宣称"近期不可证伪"。' % -d_hk)
    rel_sk = '（无物理解可比）' if tau_lo is None else (
        '高出 %.1f 个数量级。' % d_sk if d_sk > 0 else
        '低了 %.1f 个数量级 ⇒ 该情形**已被实验排除**。' % -d_sk)
    for scn in ('A', 'B', 'C'):
        r = det.get(scn)
        if r is None:
            continue
        L.append('| %s | %.3e | %.2f | %.3e | %.2e | %s | %s |' %
                 (scn, r['scales']['M_GUT'], r['alpha_GUT_inv'], r['scales']['M_R'],
                  r['tau_p_yr'],
                  '是' if r['physical'] else '否：' + '、'.join(phys_reasons(r)),
                  '通过' if r['survives_sk'] else '排除'))
    L += ['', '**读法（四句，每句都带代价；下面所有区间与倍差都由上表生成，禁止手写）**：']
    if good:
        L.append('1. 情形 %s 给出 $M_{\\rm GUT}\\in\\{%s\\}$ GeV、$M_R\\in\\{%s\\}$ GeV、'
                 '$\\alpha_{\\rm GUT}^{-1}\\in\\{%s\\}$、'
                 '$\\tau(p\\to e^+\\pi^0)\\in\\{%s\\}$ yr —— 在本探针的一环口径下'
                 '**不被任何现有数据排除**'
                 % (names(good), band_tex(good, 'M_GUT'), band_tex(good, 'M_R'),
                    band_tex(good, 'alpha_GUT_inv', A2), band_tex(good, 'tau_p_yr'))
                 + ('（$\\tau_p$ 三条判据之外的超-K 下限：情形 %s 全部通过）；'
                    % names(sk_ok) if len(sk_ok) == len(good) else
                    '。但**注意**：情形 %s 的 $\\tau_p$ 在超-K 下限之下，该句对它们不成立；'
                    % names([r for r in good if r not in sk_ok])))
    else:
        L.append('1. **没有情形**通过下面三条判据 ⇒ 本探针在当前标量谱下没有正面数字。')
    if bad:
        L.append('2. 被判非物理的情形：%s。理由一律取自 `phys_reasons`（与表格同一来源），'
                 '⇒ 每条都要回写 [08_预言与判据](../08_预言与判据.md) 的证伪台账。'
                 % '；'.join('情形 %s：%s' % (r['scenario'], '、'.join(phys_reasons(r)))
                             for r in bad))
    else:
        L.append('2. **当前没有情形被判非物理**%s —— 这不是一条正面证据，而是一次**翻案的记录**：'
                 '该情形曾被 "$M_{\\rm GUT}>M_{\\rm Pl}$" 排除并登记为 F4，而那句结论是硬编码的；'
                 '修掉 $b_2$ 的重复计入（测试 S3.4–S3.6）后它自动满足判据 ③ ⇒ F4 的**判据失效**，'
                 '已在 08 文档撤销。教训写进 `phys_reasons` 的文档串，并由测试 S7.1/S7.2 钉住。'
                 % ('，包括双二重体不分裂的情形 C'
                    if det.get('C') is not None and det['C']['physical'] else ''))
    if pr is not None:
        L.append('3. 同一对情形 %s↔%s 之间 $M_{\\rm GUT}$ 差 %.1f 倍、$\\tau_p$ 差 %.0f 倍：'
                 '**数字的可靠度上限就是标量谱的未知度**。分支规则现已由 [so10_reps.py](so10_reps.py) '
                 '第一性算出，未知的已是**位势与真空方向**（哪个分量多重、哪个拷贝耦合哪一代）；'
                 '分量质量对 $M_{\\rm GUT}$ 的定量响应见 [SO10阈值报告](SO10阈值报告.md) §6–§8 '
                 '（结论：整块多重态落在共同标度时 $M_{\\rm GUT}$ 严格不动，动的只有块内分裂）'
                 '⇒ 不应把任一具体值当作理论预言对外宣称。'
                 % (pr[0]['scenario'], pr[1]['scenario'], pr[2],
                    scale_of(pr[1], 'tau_p_yr') / scale_of(pr[0], 'tau_p_yr')))
    else:
        L.append('3. 无并列情形可比 ⇒ 倍差无从谈起。')
    L.append('4. 这一"唯一正面数字"**不额外买证据**：§3.5(i) 表明它就是双阈链次序窗口的公共上沿'
             '（同一极限，S6.3 已验证），所以三条链在此只贡献一个 $M_{\\rm GUT}$ 数；'
             '它值钱的地方是**可单点证伪**（质子衰变 + 次序 + $M_{\\rm GUT}<M_{\\rm Pl}$ 三条同时受检），'
             '不是"三链交叉确认"。')
    L += ['',
          '## 4. 与基准的同口径对照', '',
          '| 方案 | 单阈 $\\alpha^{-1}$ 最小散布 | 出现标度 (GeV) |', '|---|---|---|',
          '| SM（无新物理） | %.4f | %.3e |' % base_sm,
          '| MSSM（对照） | %.4f | %.3e |' % base_mssm,
          '| SO(10) 双阈/三阈链 | 0（线性方程组精确可解，只要 $M_{\\rm GUT}$ 自由） | — |',
          '',
          '**必须如实说明**：环数相同、且每多一个自由标度就多一个可调参数。',
          'PS422 有 $(\\alpha_{\\rm GUT}^{-1},M_{PS},M_R)$ 三个未知去拟合三个观测量 ⇒ **总是精确命中**，',
          '"命中"本身不是证据。有内容的是下面两件事：',
          '',
          '1. **解是否物理**（正耦合 + 正确标度次序 + $M_{\\rm GUT}<M_{\\rm Pl}$）；',
          '2. **质子衰变**：SO(10) 必然给出 $X/Y$ 玻色子 ⇒ $\\tau_p$ 是 $M_{\\rm GUT}$ 的**可预言函数**。',
          '',
          '## 5. 质子衰变与 P4 的张力（量化，不调和）', '',
          '以最小 $SU(5)$（$M_X\\simeq10^{14.6}$ GeV、$\\tau_p\\sim10^{29}$ yr、'
          '$\\alpha_{\\rm GUT}^{-1}\\approx41$）为锚点，按 $\\tau_p\\propto M_X^4/\\alpha_{\\rm GUT}^2$ 标定：', '',
          '| 链 | 情形 | $\\tau_p=2.4\\times10^{34}$ yr 所需的 $M_{\\rm GUT}$ 下限 |',
          '|---|---|---|']
    for (chain, scn), fl in sorted(floors.items()):
        L.append('| %s | %s | %s |' % (chain, scn,
                                       ('%.2e GeV' % fl) if fl else '—'))
    L += ['',
          '注意两件事：',
          '* 对 **PS422/R421**，$M_{\\rm GUT}$ 是输入 ⇒ 这里只有"要么高于下限、要么被排除"的约束；',
          '* 对 **R3221**，$M_{\\rm GUT}$ 是被 §3.6 解出的**预言**（$\{%s\\}$ GeV）；'
          '通过超-K 下限的情形：%s（%d/%d 个物理解）。其 $\\tau_p$ 最低端 $%s$ yr 相对'
          '现有下限（$2.4\\times10^{34}$ yr）%s'
          % (band_tex(good, 'M_GUT'), names(sk_ok), len(sk_ok), len(good),
             sci_tex(tau_lo) if tau_lo else '—', rel_sk),
          '',
          '⇒ 因此 SO(10) 路线与 P4 的矛盾**没有被消掉，只是被推到可及范围之外**：',
          '* UFE-1 v1 的 P4 说 $\\tau_p=\\infty$（$B-L$ 严格守恒、无 $X/Y$ 玻色子）；',
          '* SO(10) 说 $\\tau_p\\in\\{%s\\}$ yr（有限，但当前看不到）。' % band_tex(good, 'tau_p_yr'),
          '**二者不能同时为真；任何一次质子衰变观测都同时否证两者。**本探针不选择，只登记。', '',
          '## 5.5 附带一致性：解出的 $M_R$ 落在 see-saw 的自然区间', '',
          'I 型 see-saw $m_\\nu=m_D^2/M_R$、$m_D=y_\\nu v/\\sqrt2$ ⇒ $y_\\nu=\\sqrt2\\sqrt{m_\\nu M_R}/v$。'
          '取 $m_\\nu=\\sqrt{\\Delta m^2_{atm}}=0.05$ eV、$v=246.22$ GeV，'
          '$M_R$ **直接用 §3.6 的解**（不是输入）：', '',
          '| 情形 | 解出的 $M_R$ (GeV) | 反推 $y_\\nu$ | 对照 |', '|---|---|---|---|']
    Y_TAU = 1.0e-2
    yvals = {scn: seesaw_y_nu(det[scn]['scales']['M_R'])
             for scn in ('A', 'B', 'C') if det.get(scn) is not None}
    hit = sorted(s for s in yvals if yvals[s] > 1e-3)
    miss = sorted(s for s in yvals if yvals[s] <= 1e-3)
    for scn in ('A', 'B', 'C'):
        if scn not in yvals:
            continue
        L.append('| %s | %.3e | %.1e | %s |' % (
            scn, det[scn]['scales']['M_R'], yvals[scn],
            '$y_\\tau\\approx1.0\\times10^{-2}$（同量级）' if yvals[scn] > 1e-3 else
            '远低于 $y_\\tau$'))
    L += ['',
          '* 读法：$M_R\\in\\{%s\\}$ GeV 是三个规范耦合**解出**的（不是输入）⇒ 反推的 $y_\\nu$ '
          '逐情形为 %s。' % (band_tex(phys, 'M_R'),
                            '、'.join('%s：%.1e' % (s, yvals[s]) for s in sorted(yvals)))]
    if hit:
        L.append('  情形 %s 落在带电轻子 Yukawa 的量级（$y_\\tau\\approx1.0\\times10^{-2}$）上，'
                 '于是 [L1](../09_已知局限与否定清单.md) 登记的 $y_\\nu\\sim3\\times10^{-13}$ '
                 '极小性问题**在该标度下**不需要额外机制解释。' % names([det[s] for s in hit]))
    if miss:
        dec = [math.log10(Y_TAU / yvals[s]) for s in miss]
        L.append('  情形 %s 的 $y_\\nu$ 仍比 $y_\\tau$ 小 %.1f–%.1f 个数量级 ⇒ "抬到同量级"'
                 '**不是**普适结论：它跟着解出的 $M_R$ 走，而 $M_R$ 跟着标量谱走。'
                 % (names([det[s] for s in miss]), min(dec), max(dec)))
    L += ['* 但这**只是量级一致**：单一代主导、$m_\\nu$ 取大气标度、$O(1)$ 复系数全部忽略；'
          '且本探针的标量谱里没有能破 $B-L$ 的 $\\Delta_R$（属 $126_H$）⇒ 此处 $M_R$ 是',
          '  $3221\\to LR$ 的**匹配标度**，不是被算出的 Majorana 质量。这一条不构成预言，只构成'
          '"不矛盾"。', '',
          '## 6. 局限（不做美化）', '',
          '* **块内分裂与阈值**：本探针把同一多重体的分量放在同一标度上。分量级的对数阈值修正'
          '已在 [so10_thresholds.py](so10_thresholds.py) 算出（响应表 + 补入 $126_H$ 的重跑），'
          '其结论是"整块共同标度不动 $M_{\\rm GUT}$、只有块内分裂动"；**未做**的是有限部分阈值'
          '（Goldstone/鬼场、匹配方案差）与二环 ⇒ 二者对 $\\alpha^{-1}$ 的影响是 $O(1)$ 量级，'
          '足以移动"是否统一"的判据。',
          '* **$M_{\\rm GUT}$ 只在单阈链上是预言**：PS422/R421 有 4 个未知量对 3 个方程 ⇒ '
          '$M_{\\rm GUT}$ 是自由输入（1 参数族）；只有 R3221 因计数恰好为 3:3 而定出 $M_{\\rm GUT}$。'
          '**这个"预言"依赖链的选择本身**，是其最弱的一环。',
          '* **标量谱的位势未知**：$16_H/45_H/126_H/120_H$ 的分支规则已由 '
          '[so10_reps.py](so10_reps.py) 第一性算出（哪些分量存在不再是猜测），但**哪个分量多重、'
          '哪个拷贝耦合哪一代**要由位势与 Yukawa 定，本探针没有 ⇒ 故以情形 A/B/C 并列而不是挑一个；'
          + ('两端（情形 %s↔%s）之间 $M_{\\rm GUT}$ 差 %.1f 倍。'
             % (pr[0]['scenario'], pr[1]['scenario'], pr[2]) if pr else '（无并列情形可比）'),
          '* **情形 B 不是"最小破缺谱"**：其额外标量是 $\\Phi(1,2,2)\\subset 10_H$ 与 '
          '$\\Sigma(1,1,3)_0\\subset 45_H$（测试 S2.7 验证后者 $B-L=0$ 且三权重属于 45）。'
          '$B-L$ 的真正破缺扇区 $\\Delta_R(1,1,3)_{B-L=2}\\in 126_H$ **不在谱内** ⇒ 本探针只把标量当',
          '  **跑动内容**用，$M_R$ 读作 $3221\\to LR$ 的匹配标度而非被算出的 Majorana 质量。',
          '* **未实现 $SU(5)\\times U(1)_{B-L}$（51 链）与 $E_6$**：需要额外分支数据，'
          '不做猜测式实现。',
          '* **质子寿命是量级标定**：短程 QCD 增强与强子矩阵元未计入（约 1 个数量级）。',
          '* **$\\alpha_{\\rm GUT}^{-1}$ 与 $\\alpha$ 一样不是被"推导"出来的**：'
          '它是跑动解，输入仍是三个实测耦合（L2 未被绕过）。',
          '',
          '## 7. 红线', '',
          '* 本报告**不**宣称统一场论已完成，也**不**宣称自然界取了 $SO(10)$。',
          '* 「三耦合能在线性方程组下精确相遇」是**参数计数**的结果（未知量数 = 方程数），',
          '  不是独立证据；独立证据只能来自 $M_{\\rm GUT}$ 一旦被定死后的**质子衰变预言**。',
          '* 而该预言落在 $\\tau_p\\in\\{%s\\}$ yr；其最低端相对 Hyper-K / DUNE 的可及范围'
          % band_tex(good, 'tau_p_yr'),
          '  （$\\sim10^{35}$ yr）' + rel_hk,
          '  它的价值是把"统一 vs 质子稳定"这个二选一**登记清楚并给出数字**，不是提供一次检验。',
          '* 结论强度受 §6 每一条限制；任一条被未来计算推翻，本报告相应作废。',
          '',
          '[返回理论核心](../README.md) · [预言与判据](../08_预言与判据.md) · '
          '[已知局限 L10/L15](../09_已知局限与否定清单.md)', '']
    (ROOT / 'SO10链统一报告.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    (ROOT / 'SO10链统一报告.json').write_text(
        json.dumps({'theory': 'UFE-1', 'check': 'so10_chain',
                    'engine_pass': eng_ok, 'solution_pass': sol_ok, 'tests': RESULTS, 'rows': rows,
                    'mgut_floor': {'%s/%s' % k: v for k, v in floors.items()},
                    'ordering_window': {'%s/%s' % k: v for k, v in bounds.items()},
                    'r3221_determined': {k: (None if v is None else
                                             {kk: v[kk] for kk in
                                              ('alpha_GUT_inv', 'scales', 'spread',
                                               'condition', 'physical', 'tau_p_yr')})
                                         for k, v in det.items()},
                    'r3221_min_spread': {'%s' % k[1]: [v[0], v[1], v[2]['scales']['M_R']]
                                         for k, v in mins.items()},
                    'baseline': {'sm_spread': base_sm[0], 'mssm_spread': base_mssm[0]}},
                   ensure_ascii=False, indent=2, default=str), encoding='utf-8')


if __name__ == '__main__':
    sys.exit(main())
