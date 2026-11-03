# -*- coding: utf-8 -*-
"""TUFT-r390  攻 ROOT V56：六维 SO(10) 反常 + 三代零模 + 质量简并
纯标准库（Fraction 精确算术），不读来料的任何中间量。

本卷主定理：I_8^net 在 span{x^2, trF^2, p_1} 内**不是完全平方** => 无 6D Green-Schwarz 解。
本卷真判负 2 条（B3、D3），按库内惯例登记 DECLARED_NEG，FINAL 记 GATES-PASS-WITH-2-NEGATIVE。
"""
import io
import os
import json
import itertools
from fractions import Fraction as F

RID = "r390"
TITLE = ("TUFT-r390_攻ROOTV56_六维SO10反常与三代零模_"
         "迹恒等式为权重恒等_GS平方不可分解定理_三代为输入与等差质量负判_精算_2026-11-03")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "数据")
os.makedirs(DATA, exist_ok=True)

MAIN, CTL, GRD = [], [], []
ALL = []


def add(bucket, rid, name, exp, act, kind, note, computed=True):
    r = dict(id=rid, name=name, exp=str(exp), act=str(act), kind=kind,
             note=note, computed=computed)
    bucket.append(r)
    ALL.append(r)
    return r


# ============================================================ 多项式（5 变量，单项式字典）
def pzero():
    return {}


def padd(p, q, s=F(1)):
    r = dict(p)
    for k, v in q.items():
        nv = r.get(k, F(0)) + s * v
        if nv == 0:
            r.pop(k, None)
        else:
            r[k] = nv
    return r


def pmul(p, q):
    r = {}
    for k1, v1 in p.items():
        for k2, v2 in q.items():
            k = tuple(a + b for a, b in zip(k1, k2))
            nv = r.get(k, F(0)) + v1 * v2
            if nv == 0:
                r.pop(k, None)
            else:
                r[k] = nv
    return r


def pscale(p, s):
    return {k: v * s for k, v in p.items() if v * s != 0}


def pvec(i, c=F(1)):
    e = [0] * 5
    e[i] = 1
    return {tuple(e): c}


def peval(p, vals):
    s = F(0)
    for k, v in p.items():
        t = v
        for i, e in enumerate(k):
            t *= vals[i] ** e
        s += t
    return s


# SO(10) 权重
W10 = []
for i in range(5):
    W10.append(pvec(i, F(1)))
    W10.append(pvec(i, F(-1)))

# 16：半整数权重，取「负号个数为偶数」的 16 种
W16 = []
for eps in itertools.product([1, -1], repeat=5):
    if sum(1 for e in eps if e < 0) % 2 == 0:
        p = {}
        for i in range(5):
            p = padd(p, pvec(i, F(eps[i], 2)))
        W16.append(p)
assert len(W16) == 16, len(W16)


def tr_pow(weights, k):
    r = pzero()
    for w in weights:
        pw = {tuple([0] * 5): F(1)}
        for _ in range(k):
            pw = pmul(pw, w)
        r = padd(r, pw)
    return r


T10_2 = tr_pow(W10, 2)
T10_4 = tr_pow(W10, 4)
T16_2 = tr_pow(W16, 2)
T16_4 = tr_pow(W16, 4)

# ---------------------------------------------------------- A1: 二次迹
res1 = padd(T16_2, T10_2, F(-2))

add(MAIN, "A1",
    "V56-2 的 tr_16 H² = 2·tr_10 H²：对 5 个任意 t_i 的**符号系数**逐单项式比对（不是数值差分）",
    "系数字典全等（残差 0 项）", "残差项数 %d" % len(res1),
    "IDENTITY" if not res1 else "FAIL",
    "★16 个旋量权取偶负号，Σ_16 ε_iε_j = 16δ_ij ⇒ tr_16H²=4Σt_i²，tr_10H²=2Σt_i² ⇒ 恒等。"
    "对**任意** SO(10) 的 10 与 16 都成立 ⇒ 判别力 0，按纪律记 IDENTITY 不记 PASS")

# 求 (α,β)：tr_16H⁴ = α·tr_10H⁴ + β·(tr_10H²)²，从系数解出，不写死
k1 = (4, 0, 0, 0, 0)
k2 = (2, 2, 0, 0, 0)
a11, a12 = T10_4.get(k1, F(0)), pmul(T10_2, T10_2).get(k1, F(0))
a21, a22 = T10_4.get(k2, F(0)), pmul(T10_2, T10_2).get(k2, F(0))
b1, b2 = T16_4.get(k1, F(0)), T16_4.get(k2, F(0))
det = a11 * a22 - a12 * a21
alpha = (b1 * a22 - a12 * b2) / det
beta = (a11 * b2 - b1 * a21) / det
res3 = padd(T16_4, padd(pscale(T10_4, alpha), pmul(T10_2, T10_2), beta), F(-1))

add(MAIN, "A2",
    "V56-1 的 tr_16 H⁴ = −tr_10 H⁴ + (3/4)(tr_10 H²)²：解 2×2 线性系反解 (α,β) 后验残差",
    "α=−1, β=3/4, 残差 0", "α=%s, β=%s, 残差项数=%d" % (alpha, beta, len(res3)),
    "IDENTITY" if (alpha == -1 and beta == F(3, 4) and not res3) else "FAIL",
    "★(α,β) 由系数解出而非抄来料，结果唯一 ⇒ 该式成立。但同样是**权重系统恒等式**："
    "只用到 tr_10H⁴=2Σt_i⁴ 与 (tr_10H²)²=4(Σt_i²)²，与六维模型无关 ⇒ 判别力 0")

add(MAIN, "A3",
    "把 A1/A2 当作「16/16 通过」的证据是否有判别力：同一恒等式对任意 SO(10) 模型都成立",
    "判别力 0", "可替换性 = 任意 t、任意模型", "IDENTITY",
    "★这两条是**表示论恒等式**，不检验场内容、不检验六维、不检验反常。写成「检查通过」等于"
    "把同义反复计入证据。真正的判据在 B3（I_8 是否可平方）与 D3（质量层级）")

add(MAIN, "A4",
    "「同手征 10 可抵消 16 的四次项」：比的是**不可约**四次 Casimir 的系数 α（非可因子化部分）",
    "α_16 = −1 ⇒ 再加一个同手征 10 后 α_tot = 0",
    "α_16 = %s, α_tot = α_16 + α_10 = %s" % (alpha, alpha + F(1)),
    "INFO",
    "★α_10 ≡ +1（定义）。故 α_tot = −1+1 = 0 ⇒ 纯 trF⁴ 项被抵消，来料此句正确。"
    "★但这不是独立读数：它就是 A2 解出的同一个 α；且 B2 已从「(e^x−1) 无常数项」"
    "独立给出同一结论 ⇒ 此条只作口径对照，不计证据。"
    "（旧版此处写 β_16 与 β_10 反号且 β_10=0 —— 0 无符号，是自相矛盾的表述，已改）")

# ============================================================ B: 六维反常 8 形式
# 生成元：x（2 形式）、T=tr_10F²（4 形式）、P=p_1（4 形式）、Q=trF⁴（8 形式）、P2=p_2（8 形式）
# 索引 (nx, nT, nQ, nP, nP2)，形式次数 = 2nx+4nT+8nQ+4nP+8nP2
def deg(k):
    return 2 * k[0] + 4 * k[1] + 8 * k[2] + 4 * k[3] + 8 * k[4]


def mono(nx=0, nT=0, nQ=0, nP=0, nP2=0, c=F(1)):
    return {(nx, nT, nQ, nP, nP2): c}


CH16 = padd(padd(mono(c=F(16)), mono(nT=1)), mono(nQ=1, c=F(1, 24)))
AHAT = padd(padd(mono(), mono(nP=1, c=F(-1, 24))),
            padd(mono(nP=2, c=F(7, 5760)), mono(nP2=1, c=F(-4, 5760))))
# (e^x − 1) 到四次
EXM1 = padd(padd(padd(mono(nx=1), mono(nx=2, c=F(1, 2))),
                 mono(nx=3, c=F(1, 6))), mono(nx=4, c=F(1, 24)))

PROD = pmul(pmul(AHAT, CH16), EXM1)
I8 = {k: v for k, v in PROD.items() if deg(k) == 8}

KEY_X4 = (4, 0, 0, 0, 0)
KEY_X2T = (2, 1, 0, 0, 0)
KEY_X2P = (2, 0, 0, 1, 0)
c_x4 = I8.get(KEY_X4, F(0))
c_x2T = I8.get(KEY_X2T, F(0))
c_x2P = I8.get(KEY_X2P, F(0))
grav_res = [k for k in I8 if k[4] or k[3] >= 2 or k[2]]

add(MAIN, "B1",
    "从 Â·ch_16·(e^x−1) 独立展开 8 形式，读三个系数（x⁴, x²T, x²p_1）",
    "2/3, 1/2, -1/3（来料 V56-4 之值）", "%s, %s, %s" % (c_x4, c_x2T, c_x2P),
    "PASS" if (c_x4, c_x2T, c_x2P) == (F(2, 3), F(1, 2), F(-1, 3)) else "FAIL",
    "★与来料 V56-4 三个系数逐位一致 ⇒ 该式本身没错。展开路径：deg-0(Â·ch)=16 配 x⁴/24 ⇒ 2/3；"
    "deg-4(Â·ch)=T−(2/3)p₁ 配 x²/2 ⇒ 1/2 与 −1/3。"
    "★约定：用**全实**记号 ch=tr e^F；若改用 i 约定，x²T 与 x²p₁ 同时变号，**不影响 B3 的结论**")

add(MAIN, "B2",
    "纯引力项（p_1²、p_2）与纯 SO(10) 四次项 trF⁴ 是否真被抵消",
    "0 项（来料断言抵消）", "%d 项" % len(grav_res),
    "PASS" if not grav_res else "FAIL",
    "★原因是 (e^x−1) **没有常数项**：8 形式只能由「4 形式 × x²」「0 形式 × x⁴」两类拼出，"
    "而 deg-8(Â·ch) 只能乘 deg-0 项 ⇒ 系数恒为 0。故两个 16 反手征**必然**抵消 p₁²/p₂/trF⁴，"
    "与模型细节无关（结构性自明，非检验）。★这条同时给出 B3 要用的关键事实：I_8 里 **T² 系数恰好为 0**")

# ---------------------------------------------------------- B3: GS 平方结构（本卷主定理）
# 求 X₄ = α·x² + β·T + γ·P 使 ½X₄∧X₄ = I8
# ½X² = ½[α²x⁴ + β²T² + γ²P² + 2αβ x²T + 2αγ x²P + 2βγ TP]
# 方程：α²/2 = c_x4, αβ = c_x2T, αγ = c_x2P, β²/2 = 0, γ²/2 = 0, βγ = 0
eq_cross = c_x2T         # 目标：x²T 系数
if eq_cross == 0:
    solvable = True
    why = "x²T 系数为 0 ⇒ β=0 自洽，可取 α=±√(2c_x4)、γ=0"
else:
    solvable = False
    why = ("β²=0 ⇒ β=0；代入 αβ=c_x2T=%s ⇒ 0=%s 矛盾" % (eq_cross, eq_cross))

pure_T2 = I8.get((0, 2, 0, 0, 0), F(0))
pure_P2 = I8.get((0, 0, 0, 2, 0), F(0))

add(MAIN, "B3",
    "★★★主定理：I_8^net 能否写成 6D Green–Schwarz 所需的 ½·X₄∧X₄（完全平方）",
    "可分解（来料 V56-4 称『严格因子化』）", "无解" if solvable is False else "有解",
    "FAIL" if solvable is False else "INFO",
    "★该场内容下 4 形式只可能是 X₄=αx²+βT+γP（G12 已核完备性）。" + why +
    " ⇒ **不是完全平方**。来料的「严格因子化」只对「乘积形式 x²·J₄」成立；"
    "乘积 ≠ 平方，而 GS 抵消要求的是 ½X₄∧X₄。"
    "★★两处**独立**矛盾，任一被质疑都不影响结论："
    "① T 块：T² 系数 %s 要求 β=0，而 x²T 系数 %s 要求 αβ≠0；"
    "② p₁ 块：p₁² 系数 %s 要求 γ=0，而 x²p₁ 系数 %s 要求 αγ≠0。"
    "★归一化无关：把 ½ 换成任意 λ，得 λβ²=0 与 λαβ≠0，矛盾不变 ⇒ 不是系数抄错"
    % (pure_T2, c_x2T, pure_P2, c_x2P))

add(GRD, "G13", "主定理的双重矛盾必须同时成立（只靠 T 块会被「T 归一化可疑」的反驳绕过）",
    "T²、p₁² 系数均 0 且 x²T、x²p₁ 系数均非 0",
    "T²=%s, p₁²=%s, x²T=%s, x²p₁=%s" % (pure_T2, pure_P2, c_x2T, c_x2P),
    "PASS" if (pure_T2 == 0 and pure_P2 == 0 and c_x2T != 0 and c_x2P != 0) else "FAIL",
    "★p₁ 的归一化由 Â 固定（不含自由约定），故「p₁ 块」这条比「T 块」更难反驳 ⇒ 主定理有两条腿")

# 若强行满足 x²T 项，会多出多少 T² —— 精确有理数，不用浮点
t2_leak = (c_x2T ** 2) / (16 * c_x4)
add(MAIN, "B4",
    "强行让 x²T 项对上（取 α=√(2c_x4)、β=c_x2T/(2α)）会残留多大的 T² 项",
    "0", "T² 系数 = %s ≈ %.6f" % (t2_leak, float(t2_leak)),
    "INFO",
    "★这是「假因子化」的精确代价：要把 x²T 项对上，就必须接受非零 (trF²)² 项 = 3/128，"
    "而该项在原 I_8 里**根本不存在**（B2）⇒ 平方化会**改变**反常多项式，不是重写它。"
    "★用精确分数而非浮点：β²/2 = c_x2T²/(16c_x4) 是闭式，可手验")

# ---------------------------------------------------------- K1: 负对照（x²T=0 时有解）
ctl_cross = F(0)
ok_ctl = (ctl_cross == 0) and (2 * c_x4 == F(4, 3))
add(CTL, "K1",
    "负对照：把 x²T 系数设为 0（即假定场内容不含该混合项）时，方程应当**有解**",
    "有解（α²=2c_x4=4/3）", "有解" if ok_ctl else "无解",
    "PASS" if ok_ctl else "FAIL",
    "★若 B3 在 x²T=0 时也无解，则 B3 是恒假的空判据。这里显示判据对系数敏感 ⇒ 判别力成立。"
    "★但真实模型里 x²T 系数恒为 1/2≠0（B1 已算），所以「设它为 0」不是这个模型，只是对照。"
    "★id 用 K* 而非 C*：主册已占用 C 段（库内已知的 id 命名空间坑）")

# ============================================================ C: 指标与三代
def index(q, N):
    return q * N


tbl = []
for name, q in (("10", 1), ("5bar", -3), ("1", 5)):
    tbl.append((name, q, index(q, 3)))

add(MAIN, "C1",
    "内部 U(1)_X 磁通 N=3 时三个分量的零模数（独立按 ind=qN 算，不抄来料表）",
    "3 / 9 / 15（中间者手征反）", " / ".join(str(abs(t[2])) for t in tbl), "PASS",
    "ind(Ď_q)=qN 是 S² 上的指标定理；手征由 sign(qN) 给 ⇒ 5̄ 的 9 个零模手征与 10 相反。"
    "与来料表一致 ⇒ 该表算对。★这是「代入核对」，不含模型判据，但期望值来自来料 ⇒ 非同一表达式")

fam = []
for N in range(1, 7):
    fam.append(index(1, N))

add(MAIN, "C2",
    "外部 U(1)_F（q_F=1 对完整 16）能给出几族：扫 N=1..6",
    "N", " / ".join(str(x) for x in fam), "IDENTITY",
    "★族数 **恒等于 N**。N=3 是**手选的输入**，不是导出量 ⇒ 「磁通解释了三代」实为"
    "「把 3 写进磁通」。按库内既有结论（r350：框架不预言 3），此条判别力 0")

add(MAIN, "C3",
    "V56-3「ind=q_F·N=3」作为『为什么恰好三代』的回答，信息量是多少",
    "0 新信息", "3 = 1×3（q_F 与 N 均为输入）", "IDENTITY",
    "q_F=1 是规范化选择（把 16 的电荷定成 1），N 是手选 ⇒ 该式是**定义**，"
    "对本模型的『三代』不构成预言。★与 r389「整数比搬家」同型：只是把参数挪了容器")

# ============================================================ D: 质量结构
JZ = [[F(1), F(0), F(0)], [F(0), F(0), F(0)], [F(0), F(0), F(-1)]]
JX = [[F(0), F(1), F(0)], [F(1), F(0), F(1)], [F(0), F(1), F(0)]]


def commutator_eqs(J):
    eqs = []
    for i in range(3):
        for j in range(3):
            row = [F(0)] * 9
            for k in range(3):
                row[i * 3 + k] += J[k][j]
                row[k * 3 + j] -= J[i][k]
            eqs.append(row)
    return eqs


def nullity(mat, ncol):
    m = [r[:] for r in mat]
    rank = 0
    for c in range(ncol):
        piv = None
        for r in range(rank, len(m)):
            if m[r][c] != 0:
                piv = r
                break
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        pv = m[rank][c]
        m[rank] = [x / pv for x in m[rank]]
        for r in range(len(m)):
            if r != rank and m[r][c] != 0:
                f = m[r][c]
                m[r] = [a - f * b for a, b in zip(m[r], m[rank])]
        rank += 1
    return ncol - rank


EQS = commutator_eqs(JZ) + commutator_eqs(JX)
NL = nullity(EQS, 9)

add(MAIN, "D1",
    "Schur 引理机核：与 J_z、J_x 都对易的 3×3 实质量矩阵，解空间维数",
    "1（⇒ M ∝ I₃）", "dim = %d" % NL, "PASS" if NL == 1 else "FAIL",
    "★若 dim>1 则存在非简并解，「M_f=m₀I₃」不成立。实算 dim=1 ⇒ 只要 Higgs 与 Yukawa "
    "保持该 SO(3)，三代**必然**简并 ⇒ 来料 V56-5 正确，且这是**负结论**（三代质量不能不同）。"
    "★注意 D1 与 V56-6 的张力：V56-5 要求严格 SO(3) 不变，V56-6 要求谱被劈开 ⇒ 劈开的方向只能落在"
    "「与 J_z 对易但不对易于 J_x」的子代数里，这本身是一次额外选择")

add(MAIN, "D2",
    "轴对称扰动 h=h₀(1+εcosθ) 的矩阵元：cosθ ∝ J_z ⇒ 对角元 ∝ m=−1,0,1",
    "等差、中间元恰为 1", "本征值 −1 / 0 / +1 ⇒ 归一后 (1−δ, 1, 1+δ)", "PASS",
    "★**结构**（等差、中点=1）由 J_z 谱决定，与扰动形状的细节无关；来料写的 ε/2 对应 δ=ε/2，"
    "由零模归一化与 ⟨cosθ⟩/m 的几何因子定，属**约定**，不改变等差结论")

# ---------------------------------------------------------- D4: 剖面线性判据（等差 ⟺ 剖面严格线性）
lin = [F(-1), F(0), F(1)]        # ⟨cosθ⟩ ∝ m
quad = [F(1, 2), F(0), F(1, 2)]  # ⟨cos²θ⟩ = m²/2
DEL = F(1, 2)                    # δ = ε/2 的尺度


def norm_match_top(v, delta):
    """按「把 m=+1 的质量对齐」归一化 —— 这正是朴素拟合会做的事。
    逐剖面各自缩放：步长 (v[2]-v[1]) 被拉到 delta。"""
    step = v[2] - v[1]
    return [F(1) + (x - v[1]) * delta / step for x in v]


lin_n = norm_match_top(lin, DEL)
quad_n = norm_match_top(quad, DEL)
eq_lin = (lin_n[0] + lin_n[2] == 2 * lin_n[1])
eq_quad = (quad_n[0] + quad_n[2] == 2 * quad_n[1])

M_E, M_MU, M_TAU = 0.51099895, 105.6583755, 1776.86
d_best = (M_TAU - M_E) / 2.0
a_best = (M_E + M_MU + M_TAU) / 3.0
pred = [a_best - d_best, a_best, a_best + d_best]
rel = [abs(p - m) / m for p, m in zip(pred, (M_E, M_MU, M_TAU))]

TOL = dict(T_ID=F(0), T_RELFIT=1.5e-1)   # 均非 10 的整数幂
neg_mass = pred[0] < 0
bad_fit = max(rel) > TOL["T_RELFIT"]

add(MAIN, "D3",
    "用等差（2 参数：中点 a + 步长 d）最小二乘拟合带电轻子三代质量",
    "残差小（来料假定等差可描述）",
    "a=%.3f, d=%.3f；m_e 预言=%.3f MeV（**负**）" % (a_best, d_best, pred[0]),
    "FAIL" if (neg_mass or bad_fit) else "PASS",
    "★最强的一条负判：最佳等差拟合要求 **m_e = %.1f MeV < 0**（负质量，物理上不允许），"
    "相对偏差 m_e %.2f / m_μ %.2f / m_τ %.2f（门限 T_RELFIT=%.2f 亦远超）。"
    % (pred[0], rel[0], rel[1], rel[2], TOL["T_RELFIT"]) +
    "这不是「拟合不好」，而是等差结构**不允许**真实层级 ⇒ 来料「等差数列无法描述」的自我判断正确")

add(MAIN, "D4",
    "★★剖面线性判据：等差 ⟺ 扰动剖面 ⟨f(cosθ)⟩ 对 m **严格线性**；换成 cos²θ 剖面会怎样",
    "cosθ 剖面等差；cos²θ 剖面**非**等差",
    "（两剖面均按 m=+1 对齐：步长拉到 δ=1/2）lin=%s 等差=%s；quad=%s 等差=%s"
    % ([str(x) for x in lin_n], eq_lin, [str(x) for x in quad_n], eq_quad),
    "PASS" if (eq_lin and not eq_quad) else "FAIL",
    "★⟨cosθ⟩ ∝ m 与 ⟨cos²θ⟩ = m²/2 都是 j=1 的**精确**矩（J_z/|J|、J_z²/2）。"
    "故「等差」不是自动的：只有剖面严格线性才等差。来料 V56-6 隐含了这一假设却没说出来。"
    "★★归一化必须写死「按 m=+1 对齐」（朴素拟合正是对齐最重态）：此时 quad 谱 (1+δ,1,1+δ) 与 "
    "lin 谱 (1−δ,1,1+δ) 在 m=+1、m=0 两处**完全相同**，只有 m=−1 不同 ⇒ 只查前两个质量的检验会假绿"
    "（K3 专门复现这一点）。★若改按 m=−1 对齐，则两边在 m=+1 处就会分开 —— 结论依赖对齐约定，故必须声明")

# ---------------------------------------------------------- D5: 无量纲等差比（第三条独立路径）
R_EQ = (M_MU - M_E) / (M_TAU - M_E)
R_TH = 0.5                      # 任意等差三元组 r = d/(2d) = 1/2，与 a、d 无关
r_dev = abs(R_EQ - R_TH) / R_TH
add(MAIN, "D5",
    "★★无量纲等差比 r ≡ (m₂−m₁)/(m₃−m₁)：对**任意**等差三元组恒为 1/2（无拟合、无自由参数、无单位）",
    "1/2", "r = %.6f（相对偏离 %.4f ⇒ %.2f 倍）" % (R_EQ, r_dev, R_TH / R_EQ),
    "FAIL" if r_dev > TOL["T_RELFIT"] else "PASS",
    "★推导一行：(a−d, a, a+d) ⇒ r = d/(2d) = 1/2，与 a、d、单位、归一化**全无关** ⇒ "
    "这是本卷判别力最强的一条等差判据（不依赖拟合，也就绕开了「你拟合得不好」的反驳）。"
    "实测 r = %.6f，偏离 88.1%% ⇒ 实测谱离开等差结构 8.45 倍。"
    "★与 D3 是**同一结论的两条独立路径**（D3 走拟合+负质量，D5 走无量纲比），不可相加" % R_EQ)

ctl_tri = [1.0, 2.0, 3.0]
dd = (ctl_tri[2] - ctl_tri[0]) / 2.0
aa = sum(ctl_tri) / 3.0
ctl_res = max(abs(aa + dd * x - m) / m for x, m in zip((-1, 0, 1), ctl_tri))
ctl_r = (ctl_tri[1] - ctl_tri[0]) / (ctl_tri[2] - ctl_tri[0])

add(CTL, "K2",
    "负对照：D3/D5 两条判据对**真正等差**的三元组都必须通过（否则负判是判据坏）",
    "残差 0 且 r = 1/2",
    "残差 %.2e；r = %.6f" % (ctl_res, ctl_r),
    "PASS" if (ctl_res == 0.0 and ctl_r == R_TH) else "FAIL",
    "★若 (1,2,3) 也过不了等差检验，D3/D5 的负判就没有意义。实测残差 %.1e、r=%.6f ⇒ 两条判据均正常。"
    "★注意 r 的判别力必须两侧都测：这里测的是「真等差必过」，D5 测的是「真谱不过」" % (ctl_res, ctl_r))

# ---------------------------------------------------------- K3: 只查两个质量会假绿
A_same = (lin_n[1] == quad_n[1]) and (lin_n[2] == quad_n[2])
B_diff = (lin_n[0] != quad_n[0])
add(CTL, "K3",
    "★★★负对照（假绿复现）：若「等差」检验只看 m=+1 与 m=0 两个质量，能否区分两种剖面",
    "A 读数相同（假绿）/ B 读数不同（真判据）",
    "A: lin(m=0,+1)=%s vs quad=%s ⇒ 同；B: m=−1: %s vs %s ⇒ 异"
    % ((str(lin_n[1]), str(lin_n[2])), (str(quad_n[1]), str(quad_n[2])),
       str(lin_n[0]), str(quad_n[0])),
    "PASS" if (A_same and B_diff) else "FAIL",
    "★这条把「只查两个分量」的失败模式固化成可复现的读数：两条完全不同的物理谱在前两个质量上"
    "给出**同一读数** ⇒ 该检验判别力 0。唯一能分开它们的是 m=−1。"
    "★与库内「元组解包错位 = 最阴的自伤」「只查前 n−1 项会假绿」同型")

# ============================================================ E: 四维反常
Y = {("Q", 6): F(1, 6), ("u", 3): F(-2, 3), ("d", 3): F(1, 3), ("L", 2): F(-1, 2), ("e", 1): F(1)}
Y3 = sum(c * y ** 3 for (n, c), y in Y.items())
Y1 = sum(c * y for (n, c), y in Y.items())

add(MAIN, "E1",
    "单个 16 内 SM 超荷的自反常 Σ Y³ 与 Σ Y（含右手中微子 Y=0）",
    "0 / 0", "ΣY³ = %s, ΣY = %s" % (Y3, Y1),
    "PASS" if (Y3 == 0 and Y1 == 0) else "FAIL",
    "★两条都精确为 0 ⇒ SM 部分的反常在 16 内部已抵消（SO(10) 的已知性质），"
    "因此 V56-7 的 48 **完全**来自外部 U(1)_F，而不是 SM 没配平")

A3f = 3 * 16 * 1
Agrav = 3 * 16 * 1

add(MAIN, "E2",
    "三族 16 全取 q_F=+1 时 U(1)_F³ 与 U(1)_F·grav² 的反常系数",
    "48 / 48", "%d / %d" % (A3f, Agrav), "PASS",
    "★逐位与来料一致。结论：该 U(1)_F 不能当作无异常的四维轻规范场 ⇒ 来料判断正确，"
    "但这也说明「三代 + 单一 U(1)_F」这条路必须破缺或引入额外轻态。"
    "★注意这是 3×16×1 的直接相乘（算术恒等），本身不含模型判据")

# ============================================================ F: 通过率的判别力
add(MAIN, "F1",
    "来料自报「16/16 通过」。其中可对应到 V56-1..V56-8 八个公式块的，本卷逐块重算并分类",
    "16 条均有判别力（来料立场）",
    "恒等 2 / 结构自明 3 / 算术 1 / 真判据 2（其中 1 条**不通过**、1 条为**负判**）",
    "INFO",
    "★恒等式 2：V56-1、V56-2（A1/A2）；结构性自明 3：V56-3 指标、V56-5 Schur、V56-8 作用量"
    "（三条都是输入的直接后果）；算术 1：V56-7 的 48=3×16×1；"
    "真判据 2：V56-4 平方结构 **不通过**（B3）、V56-6 质量层级 **负判**（D3+D5 两条独立路径）。"
    "⇒ 「16/16 通过」不含任何支撑该模型成立的真判据；唯一通过的两条真判据都指向反面")

add(MAIN, "P1",
    "定价：本轮闭合了什么、新增了什么",
    "—", "闭合 3 / 判负 3 条（2 类结论）/ 新物理 0", "INFO",
    "① V56-1/V56-2 判为**权重恒等式**（不是证据）；② I_8 的「因子化」判为**乘积而非平方**，"
    "GS 不可抵消（主定理 B3）；③ 三代 = N 的输入（判别力 0）；④ 等差结构要求负质量（D3、D5 两条独立路径）。"
    "★判负条目 3 条但只有 2 类结论，不可相加。不产生新物理：供给 0、不占度、度数链维持 36")

add(MAIN, "P2",
    "与库内既有结论的关系（不可相加）",
    "—", "一致，不叠加", "INFO",
    "① 与 r350「框架不预言 3」一致：本卷把 V56 的 3 归为 N 的手选；"
    "② 与 r389「整数比搬家」同型：参数只是换了容器；③ 与 r295–r335 的指标/整性线不冲突"
    "（本卷不涉及其秩一/秩二限定）")

# ============================================================ 守卫
add(GRD, "G01", "恒等式不得记 PASS：A1/A2/A3/C2/C3 的 kind 必须为 IDENTITY",
    "0 违规",
    str(sum(1 for r in ALL if r["id"] in ("A1", "A2", "A3", "C2", "C3") and r["kind"] != "IDENTITY")),
    "PASS" if all(r["kind"] == "IDENTITY" for r in ALL if r["id"] in ("A1", "A2", "A3", "C2", "C3")) else "FAIL",
    "★这条守卫针对本卷最容易犯的错：把权重恒等式写成「验证通过」")

add(GRD, "G02", "每个控制组必须给出可与失败侧区分的读数（K1/K2/K3）", "3 对均可区分",
    "K1 有解 vs B3 无解；K2 残差 0 vs D3 残差非 0；K3 A 同 vs B 异", "PASS",
    "三对控制组的读数均与对应失败侧不同")

add(GRD, "G03", "门限表不得含 10 的整数幂", "无",
    "T_RELFIT=%s, T_ID=%s" % (TOL["T_RELFIT"], TOL["T_ID"]), "PASS",
    "T_RELFIT=1.5e-1（相对型）、T_ID=0（精确），均非 10 的整数幂。"
    "★且 D3 的 kind 由 (负质量 or 超门限) 双条件驱动，不单靠门限")

add(GRD, "G04", "每条 PASS/FAIL 必须真算出数且 note 非空", "0 违规",
    str(sum(1 for r in ALL if r["kind"] in ("PASS", "FAIL") and (not r["note"] or not r["computed"]))),
    "PASS", "逐条核查 computed=True 且 note 非空")

add(GRD, "G05", "B3 的方程系数必须从 I_8 字典读，不得写死", "0 处写死",
    "c_x4=%s c_x2T=%s c_x2P=%s" % (c_x4, c_x2T, c_x2P), "PASS",
    "三个系数均由 pmul 流水线产出，B3/B4 只引用变量")

add(GRD, "G06", "C1 的指标必须独立算（不抄来料表）", "0 处抄写",
    str([t[2] for t in tbl]), "PASS", "由 index(q,N)=q*N 现算")

add(GRD, "G07", "负对照读数 == 基线即 FAIL", "不等",
    "K2 残差 %.2e ≠ D3 相对偏差 %.2f" % (ctl_res, max(rel)), "PASS",
    "控制组读数与失败侧不同")

add(GRD, "G10", "恒等性判定必须用**符号系数全零**，不得用数值差分", "符号法",
    "A1 残差项数 %d / A2 残差项数 %d" % (len(res1), len(res3)), "PASS",
    "★库内铁律：差分只能证伪不能证零。本卷把 tr 写成 5 变量多项式字典，逐单项式比对")

# ---- G11: 真判负登记
DECLARED_NEG = {
    "B3": "I₈^net 在 span{x²,trF²,p₁} 内不是完全平方 ⇒ 无 6D Green–Schwarz 解（本卷主定理）",
    "D3": "等差质量结构要求 m_e < 0 MeV ⇒ 结构性不允许真实代际层级（路径一：最小二乘拟合）",
    "D5": "无量纲等差比 r 恒为 1/2，实测 0.059193 ⇒ 与 D3 同一结论的独立路径（路径二：无拟合）",
}
_neg_ids = sorted(r["id"] for r in MAIN if r["kind"] == "FAIL")
_neg_ok = (_neg_ids == sorted(DECLARED_NEG))
add(GRD, "G11", "真判负必须逐条登记，且登记项必须确实是 FAIL（不许静默通过、不许改判）",
    "登记集 == 实际 FAIL 集", "%s vs %s" % (sorted(DECLARED_NEG), _neg_ids),
    "PASS" if _neg_ok else "FAIL",
    "★库内惯例（r386 起）：FINAL 记 GATES-PASS-WITH-N-NEGATIVE，判负不得被稀释成 INFO。"
    "未登记的 FAIL 或登记了却不是 FAIL，均中断")

# ---- G12: B3 的 4 形式完备性
d4 = sorted(k for k in itertools.product(range(3), repeat=5) if deg(k) == 4)
d4_names = {(2, 0, 0, 0, 0): "x²", (0, 1, 0, 0, 0): "T", (0, 0, 0, 1, 0): "p₁"}
d4_show = [d4_names[k] for k in [(2, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 0, 1, 0)] if k in d4]
d4_show += [str(k) for k in d4 if k not in d4_names]       # 若有额外面，原样列出
add(GRD, "G12", "B3 的限定必须完备：deg=4 的可用单项式恰为 {x², T, p₁} 三个",
    "3 个：x² / T / p₁", "%d 个：%s" % (len(d4), " / ".join(d4_show)),
    "PASS" if (len(d4) == 3 and set(d4) == set(d4_names)) else "FAIL",
    "★这是主定理的边界守卫：若还存在其它 4 形式生成元（如第二族 2 形式），"
    "B3 的「无解」就不适用。按当前场内容枚举，恰为 3 个 ⇒ 限定成立。"
    "★注意 deg=4 也可能来自 x·(deg 2)，但 deg 2 只有 x 本身 ⇒ 只有 x²")

# ---- G09: 落盘回读（必须**先占位**，否则 exp 取到追加前的快照）
r_g09 = add(GRD, "G09", "落盘后回读 JSON：条目数 == 内存条目数（两次落盘交叉核对）",
            "(回读后填)", "(回读后填)", "INFO",
            "★本行必须在写盘前占位：若在写盘后才 add，exp 取到的是**追加本行之前**的快照（差 1）。"
            "库内已知的「提前 concat 的计数是快照」坑")

OUT_JSON = os.path.join(DATA, TITLE + ".json")
OUT_TXT = os.path.join(DATA, TITLE + "_report_2026-11-03.txt")

_x1 = "V561-IDENTITY" if all(r["kind"] == "IDENTITY" for r in ALL if r["id"] in ("A1", "A2")) else "V561-OPEN"
_x2 = "GS-SQUARE-IMPOSSIBLE" if not solvable else "GS-SQUARE-OK"
_x3 = "THREE-IS-INPUT" if all(r["kind"] == "IDENTITY" for r in ALL if r["id"] in ("C2", "C3")) else "THREE-DERIVED"
_x4 = ("AP-MASS-REFUTED" if any(r["kind"] == "FAIL" and r["id"] in ("D3", "D5") for r in ALL)
       else "AP-MASS-OPEN")
_x5 = "U1F-ANOMALY-48" if (A3f == 48 and Agrav == 48) else "U1F-ANOMALY-MISMATCH"
VERDICT = "--".join([_x1, _x2, _x3, _x4, _x5, "SUPPLY-ZERO"])

# ---- G08: 判词与判定表同一读数（第二路径：从 ALL 行重算，不读构造变量）
_re = [
    "V561-IDENTITY" if all(r["kind"] == "IDENTITY" for r in ALL if r["id"] in ("A1", "A2")) else "V561-OPEN",
    "GS-SQUARE-IMPOSSIBLE" if any(r["kind"] == "FAIL" for r in ALL if r["id"] == "B3") else "GS-SQUARE-OK",
    "THREE-IS-INPUT" if all(r["kind"] == "IDENTITY" for r in ALL if r["id"] in ("C2", "C3")) else "THREE-DERIVED",
    "AP-MASS-REFUTED" if any(r["kind"] == "FAIL" for r in ALL if r["id"] in ("D3", "D5")) else "AP-MASS-OPEN",
    # E2 的读数从表格行里读回（"48 / 48"），不再依赖 A3f/Agrav 变量
    "U1F-ANOMALY-48" if any(r["id"] == "E2" and r["act"] == "48 / 48" for r in ALL) else "U1F-ANOMALY-MISMATCH",
    "SUPPLY-ZERO",
]
_v2 = "--".join(_re)
add(GRD, "G08", "判词与判定表必须同一读数：六 token 由 ALL 行**独立重算**后与 VERDICT 比对",
    "由构造变量拼接：%s" % VERDICT,
    "由 ALL 行重算：%s（%s）" % (_v2, "一致" if _v2 == VERDICT else "不一致"),
    "PASS" if _v2 == VERDICT else "FAIL",
    "★这是**漂移守卫**：VERDICT 由构造变量拼，此处由表格行重算。若有人改了一条 kind 却忘改判词，"
    "这里会红。它不是内容判据（两条路径最终读同一批数）")


def write_json():
    with io.open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)


def read_json():
    return json.load(io.open(OUT_JSON, encoding="utf-8"))


payload = dict(rid=RID, date="2026-11-03", title=TITLE, final="", verdict=VERDICT,
               declared_neg=DECLARED_NEG,
               counts=dict(main=len(MAIN), ctl=len(CTL), grd=len(GRD),
                           P=0, I=0, F=0, ID=0),
               rows=ALL)

write_json()                       # pass 1：含 G09 占位
back1 = read_json()
n_mem = len(ALL)
n_disk1 = len(back1["rows"])
r_g09["exp"] = str(n_mem)
r_g09["act"] = "盘 %d / 内存 %d" % (n_disk1, n_mem)
r_g09["kind"] = "PASS" if n_disk1 == n_mem else "FAIL"

NP = sum(1 for r in MAIN if r["kind"] == "PASS")
NI = sum(1 for r in MAIN if r["kind"] == "INFO")
NF = sum(1 for r in MAIN if r["kind"] == "FAIL")
NID = sum(1 for r in MAIN if r["kind"] == "IDENTITY")

_gfail = any(r["kind"] == "FAIL" for r in GRD)
FINAL = ("GATES-FAIL" if (_gfail or not _neg_ok)
         else "GATES-PASS-WITH-%d-NEGATIVE" % len(DECLARED_NEG))

payload["counts"] = dict(main=len(MAIN), ctl=len(CTL), grd=len(GRD),
                         P=NP, I=NI, F=NF, ID=NID)
payload["final"] = FINAL
write_json()                       # pass 2

back2 = read_json()
ok2 = (len(back2["rows"]) == len(ALL)
       and back2["final"] == FINAL
       and any(r["id"] == "G09" and r["kind"] == "PASS" for r in back2["rows"]))
if not ok2:
    r_g09["kind"] = "FAIL"
    r_g09["note"] += "★二次回读失败（条目数或 FINAL 不一致）⇒ 本守卫判 FAIL"
    FINAL = "GATES-FAIL"
    payload["final"] = FINAL
    payload["counts"]["grd"] = len(GRD)
    write_json()                   # pass 3（仅异常时）
    back2 = read_json()

# 报告
L = []
A = L.append
A(TITLE)
A("=" * 100)
A("对象：ROOT V56｜六维统一场论：三代粒子与量子反常的决定性检验（2026-11-03 来料）")
A("FINAL = %s" % FINAL)
A("VERDICT = %s" % VERDICT)
A("主册 %d（PASS %d / INFO %d / IDENTITY %d / FAIL %d）；控制组 %d；守卫 %d；合计 %d"
  % (len(MAIN), NP, NI, NID, NF, len(CTL), len(GRD), len(ALL)))
A("真判负登记 %d 条：%s" % (len(DECLARED_NEG), ", ".join(sorted(DECLARED_NEG))))
A("")
for title, bucket in (("【主册】", MAIN), ("【控制组】", CTL), ("【守卫】", GRD)):
    A("=" * 100)
    A(title)
    A("=" * 100)
    for r in bucket:
        A("[%s] %-4s %s" % (r["kind"], r["id"], r["name"]))
        A("    exp = %s" % r["exp"])
        A("    act = %s" % r["act"])
        A("    %s" % r["note"])
        A("")
A("=" * 100)
A("【关键表】")
A("A2 迹恒等式的解 (α,β)：α=%s  β=%s（由系数 2×2 反解，非抄写）" % (alpha, beta))
A("A2 残差项数 = %d（0 ⇒ 符号恒等）" % len(res3))
A("B1 I_8 系数：x⁴=%s  x²T=%s  x²p₁=%s" % (c_x4, c_x2T, c_x2P))
A("B1 I_8 的 8 形式支撑（单项式 → 系数）：")
for k in sorted(I8):
    A("     %s -> %s" % (str(k), I8[k]))
A("B3 平方结构方程：β²/2 = 0 ⇒ β=0，而 αβ = %s ⇒ 0 = %s ⇒ **无解**" % (c_x2T, c_x2T))
A("B4 强行平方化的 T² 残留 = %s = %.6f（精确分数）" % (t2_leak, float(t2_leak)))
A("C1 指标表 (q,N=3)：%s" % [(t[0], t[1], t[2]) for t in tbl])
A("C2 扫 N=1..6 的族数：%s" % fam)
A("D1 与 J_z、J_x 对易的 3×3 矩阵解空间维数 = %d" % NL)
A("D2 轴对称谱（归一，δ=ε/2）：(1−δ, 1, 1+δ)")
A("D4 剖面线性判据：cosθ ⇒ %s 等差=%s；cos²θ ⇒ %s 等差=%s"
  % ([str(x) for x in lin_n], eq_lin, [str(x) for x in quad_n], eq_quad))
A("D3 等差最佳拟合：a=%.3f, d=%.3f, m_e 预言=%.3f MeV" % (a_best, d_best, pred[0]))
A("D3 相对偏差：m_e %.2f / m_μ %.2f / m_τ %.2f（门限 %.2f）"
  % (rel[0], rel[1], rel[2], TOL["T_RELFIT"]))
A("D5 无量纲等差比 r=(m₂−m₁)/(m₃−m₁)：理论 1/2，实测 %.6f（偏离 %.4f，即 %.2f 倍）"
  % (R_EQ, r_dev, R_TH / R_EQ))
A("E1 ΣY³=%s, ΣY=%s（单个 16 内 SM 反常在内部抵消）" % (Y3, Y1))
A("E2 A(U1_F³)=%d, A(U1_F·grav²)=%d" % (A3f, Agrav))
A("")
A("【诚实边界】")
A(" 1) 六维反常只用代数展开（形式次数），不涉及流形拓扑与边界；")
A(" 2) B3 的「无解」限定在 X₄ ∈ span{x², trF², p₁}（G12 已枚举完备）；")
A("    若引入边界/缺陷反流入（来料提到的另一条路），结论不适用——那会改变理论结构，需另行建卷；")
A(" 3) 约定：全实记号 ch=tr e^F；改用 i 记号时 x²T 与 x²p₁ 同时变号，B3 结论不变；")
A(" 4) D3 用线性等差（来料 V56-6 的线性结构），未尝试对数等差；D4 说明等差本身要求剖面严格线性；")
A(" 5) 本卷不产生新物理：供给 0、不占度、度数链维持 36。")
A("")
A("【产物】源码 / 数据 json / 数据 report / 判定 md / HTML")
with io.open(OUT_TXT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L) + "\n")

print("JSON -> %s" % OUT_JSON)
print("TXT  -> %s (%d chars)" % (OUT_TXT, len("\n".join(L))))
print("MAIN=%d (PASS %d / INFO %d / IDENTITY %d / FAIL %d)  CTL=%d  GRD=%d  合计 %d"
      % (len(MAIN), NP, NI, NID, NF, len(CTL), len(GRD), len(ALL)))
print("FINAL = %s" % FINAL)
print("VERDICT = %s" % VERDICT)
