r"""UFE-1 · L10 的阈值层：逐分量阈值、统一点响应，以及"补入 $126_H$ 后重跑"。

这是 [so10_reps.py](so10_reps.py)（分支规则，R6 门禁）与 [so10_chain.py](so10_chain.py)
（一环跑动，S 门禁）之间的第三块石头：前两块的输出在这里**第一次合用**——
破缺后的标量分量内容取自表示论引擎**算出**的分支表，每个分量的 $\beta$ 系数贡献取自
链探针的权重格指标机器，两者必须逐项对账（T2/T3/T4），否则不出数字。

为什么需要它：报告里 $M_{\rm GUT}$ 的摆动一直被写作"依赖标量谱"，但**没人知道依赖到什么
程度**——哪个多重态的分裂值几个 e _fold、哪个根本不动。本脚本给出
$\partial\ln M_{\rm GUT}/\partial\ln M_j$ 的分量级响应表，并执行 08 文档登记的那条待办：
"必须补入 $126_H$ 后重跑"。

门禁分七族：T0 上游全 PASS、T1 格点换算、T2 分量内容对账、T3 $\Delta b$ 逐项闭合、
T4 退化哨兵（把分量谱放回整块配置）、T5 统一点互检、T6 **完整母表示不摆动统一点**、
T7 响应表与有限搬移互检。这个对账已经在仓库里抓到一个真缺陷：链探针情形 C 的 $b_2$
把 $-(11/3)C_2$ 的规范项重复计入了一次（修复见 [so10_chain.py](so10_chain.py) 的 S3.4/S3.5）
⇒ "自检全 PASS"的模块仍可能给出错的数，能推翻它的是第二条独立代码路径。

模型（一环 + 逐步阈值，只含对数项）：
* 分量粒度 = 「$SO(10)$ 表示沿 $3221$ 的分量」再按 $Y$ 值切开，即一个 **SM 不可约多重态**
  一个质量参数；切分由权重格自动完成，不是手挑。
* 分量在其质量 $M_j$ 以上进入 $\beta$ 系数、以下退出（$\overline{\rm DR}$ 式逐步跑动）。
* 不列出的分量 = 重于 $M_{\rm GUT}$ ⇒ 贡献恰为零（不是近似，是定义）。
* 分量质量以 $t_B+\delta$ 给出（$t_B=\ln M_{B-L}$ 匹配标度，$\delta\ge0$）；轻 Higgs 二重态
  以 $M_Z$ 为锚。**全部质量是输入参数**，不是预言。

诚实边界（不做的东西）：
* **两环跑动未做**。一般群乘积的两环系数矩阵 $b_{ij}$ 需要外部公式，本次会话内在仓库里
  无法核验（网络抓取失败）⇒ **不凭记忆写**。全部结论都是一环 + 阈值。
* **只有对数项**：完整阈值修正含与方案有关的有限项（Goldstone/鬼场、匹配方案差）未计算
  ⇒ 下面的移动量是对数领先估计。
* **分裂超过一步时不追踪中间规范群**：某块重于其母多重态的其余分量时，$t_B$ 之上会出现
  "只剩部分 $LR$ 多重态"的窗口；一环对数近似下等价于把匹配标度取到最高的那块。响应系数
  因此只对**中等分裂**成立。
* Yukawa 在一环不进入规范耦合的 $\beta$ ⇒ 本脚本不需要任何 Yukawa 输入（结构事实，非简化）。
* 标量位势未定 ⇒ 分量质量是**参数**；本脚本给的是响应系数与给定分裂下的移动量。
* 全部结果只说明"若 SO(10) 成立且谱如此"，**不**提升任何体系的证据等级，也**不**意味着
  统一场论已完成；L10 仍未关闭。

运行：`python -B so10_thresholds.py`（零第三方依赖；产出 SO10阈值报告.md / .json）
"""
from fractions import Fraction as F
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import so10_chain as C                                    # noqa: E402
import so10_reps as R                                     # noqa: E402

TWOPI = 2.0 * math.pi
TZ = math.log(C.MZ)
TOL = 1e-11                                              # 退化一致性容差（绝对）
DELTA = 5.0                                              # §7 里"单个分量搬多远"（e _fold）
PHI_LR = '(1,2,2)_{0}'

RESULTS = []


def rec(cid, claim, computed, expected, tol, status, note=''):
    RESULTS.append({'id': cid, 'claim': claim, 'computed': computed, 'expected': expected,
                    'tolerance': tol, 'status': status, 'note': note})
    return status == 'PASS'


def fmt(v):
    """列表/元组里的 `Fraction` 走 `str`，报告里不出现 `Fraction(...)` 这种噪声。"""
    if isinstance(v, (list, tuple)):
        return '(' + ', '.join(fmt(x) for x in v) + ')'
    return str(v)


def exact(cid, claim, computed, expected, note=''):
    return rec(cid, claim, fmt(computed), fmt(expected), '0（精确）',
               'PASS' if computed == expected else 'FAIL', note)


def approx(cid, claim, computed, expected, tol, note='', rel=False):
    a = computed if isinstance(computed, (list, tuple)) else [computed]
    b = expected if isinstance(expected, (list, tuple)) else [expected]
    d = max(abs(x - y) / (abs(y) if rel and abs(y) > 1e-300 else 1.0) for x, y in zip(a, b))
    return rec(cid, claim, fmt(computed), fmt(expected), ('相对 ' if rel else '') + '%g' % tol,
               'PASS' if d <= tol else 'FAIL',
               '%s；最大偏差 %.3e' % (note, d))


def ok(cid, claim, cond, note=''):
    return rec(cid, claim, bool(cond), True, '布尔', 'PASS' if cond else 'FAIL', note)


# =============================================================== 两引擎的权重换算
def to_chain(gv):
    """表示论引擎的整数格点（$1\\,\\varepsilon_i=12$）→ 链探针的 Fraction 权重。"""
    return tuple(F(x, R.U) for x in gv)


def ms_of(ws):
    d = {}
    for w in ws:
        d[w] = d.get(w, 0) + 1
    return d


FACS_LR = [('SU', 3), ('SU', 2, 'L'), ('SU', 2, 'R'), ('U1', C.BL, 'B-L')]
LRN = ['b₃', 'b₂L', 'b₂R', 'b$_{B-L}$']
SMN = ['b₁', 'b₂', 'b₃']


# =============================================================== 分量清单（推导，非手抄）
SCALARS = [('10_H', (1, 0, 0, 0, 0)), ('45_H', (0, 1, 0, 0, 0)), ('126_H', (0, 0, 0, 0, 2))]


def pieces(name, cs):
    r"""$SO(10)$ 标量表示 → 逐 SM 分量：$(3221\ \text{标签},\,Y,\,\text{权重集},\,\Delta b)$。

    LR 标签与重数由 Klimyk–Springer 交错和给出（`branching`），权重集由子系统 Freudenthal
    给出（`sub_irrep`）⇒ 与 R6 门禁同源；再按 $Y$ 切一刀就是 SM 粒度。
    """
    Lam, ms, d, tot, _ = R.irrep(cs)
    assert tot == d, '%s：Freudenthal 总重数 $\\ne$ Weyl 维数' % name
    assert d == int(name.split('_')[0]), '%s：标号 %s 的维数是 %d' % (name, cs, d)
    out = []
    for row in R.branching(ms, R.SUB_3221):
        sub = R.sub_irrep(row['wt'], R.SUB_3221)
        assert sum(sub.values()) == row['dim'], '%s 分量 %s 维数账不平' % (name, row['labels'])
        groups = {}
        for w, k in sub.items():
            groups.setdefault(C.dot(to_chain(w), C.YHP), []).extend([w] * k)
        for y in sorted(groups):
            ws = [to_chain(w) for w in groups[y]] * row['n']
            db = [F(1, 3) * C.factor_T(f, ws) for f in FACS_LR]
            out.append({'rep': name, 'lr': R.fmt_3221(row), 'n': row['n'], 'bl': str(row['bl']),
                        'y': str(y), 'ndim': len(ws), 'ws': ws, 'db': db,
                        'db_sm': [F(1, 5) * C.factor_T(('U1', C.YHP, 'Y'), ws),
                                  F(1, 3) * C.factor_T(('SU', 2, 'L'), ws),
                                  F(1, 3) * C.factor_T(('SU', 3), ws)]})
    return out


PIECES = {}
for _nm, _cs in SCALARS:
    PIECES[_nm] = pieces(_nm, _cs)
BY_KEY = {}
for _nm in PIECES:
    for _pc in PIECES[_nm]:
        BY_KEY[(_pc['rep'], _pc['lr'], _pc['y'])] = _pc

# ------------------ T8 的补入候选：R9 判出"第二条闭合道的母表示缺位"的那一个 ------------------
# `SCALARS` 保持三块不动 ⇒ §4~§8 的读数仍是"声明谱"的读数，台账不因本节而改写。
REP120 = '120_H'
CS_120 = (0, 0, 1, 0, 0)
PIECES[REP120] = pieces(REP120, CS_120)
for _pc in PIECES[REP120]:
    BY_KEY[(_pc['rep'], _pc['lr'], _pc['y'])] = _pc
QVE = tuple(a + b + c / 2 for a, b, c in zip(C.T3L, C.T3R, C.BL))     # $Q=T^3_L+T^3_R+\frac{B-L}{2}$


def label_mult(nm):
    """母表示 → $\{3221\ \text{标签}:\ \text{重数}\}$：本机按 $Y$ 切开的块必须拼回一张表。"""
    out = {}
    for p in PIECES[nm]:
        assert out.setdefault(p['lr'], p['n']) == p['n'], '同一标签的 $Y$ 切片重数不一致：%s' % p['lr']
    return out


def reps_label_mult(nm):
    """表示论引擎的 $SO(10)\downarrow3221$ 分支表（R6.7 已把它与"先 $\downarrow422$ 再 $\downarrow3221$"
    两步路径逐项对过）换成本机同一套字符串键。"""
    return dict(('(%s,%d,%d)_{%s}' % (R.su_name(a2, R.dim3(*a2)), l + 1, r + 1, bl), n)
                for (a2, l, r, bl), n in R.direct_3221(nm).items())


def reps_view():
    r"""把表示论引擎的标号、分支表、不变张量簿记与道分解取进本机内存。

    跑它的**推导函数**而不是读它写出的报告文件：那份 `.md`/`.json` 是另一次运行的产物，
    引用它不等于对账（本仓库登记过的失效族正是"结论只活在产物里"）。

    顺序照抄 `so10_reps.py` 自己 `main()` 的依赖链，一处不缺：R9 的道分解层要读 R8 的
    `INV['p4']`，而 R8 要读 Yukawa 层、分支层、`TABLE`…… ⇒ 少跑一层就是 `KeyError`，
    不是"能跳过"。这里要的是**同一次进程里现算出来的** `CSPLIT`/`TABLE`。
    """
    return (R.run_engine_tests() and R.run_identification() and R.run_tensor_identities()
            and R.run_physics_tests() and R.build_table() and R.gate_no_go()
            and R.run_branching() and R.run_cross_chain() and R.run_yukawa_layer()
            and R.run_invariant_layer() and R.run_channel_layer())


def t8_rows(nm):
    """$|\Delta(B-L)|=2$ 的色单态块 + 中性二重体块（按 $Y$ 切片后的原始行）。"""
    sg = [p for p in PIECES[nm] if p['lr'].startswith('(1,1,1)')]
    bd = [p for p in PIECES[nm] if p['lr'] == PHI_LR]
    return sg, bd


def q_spectrum(pc):
    """一个 SM 分量的电荷谱：权重是 $SU(2)$ 单态 $\Rightarrow Q=Y$，一般地按 $Q$ 方向直算。"""
    return sorted(set(C.dot(w, QVE) for w in pc['ws']))


def light_doublets(reps):
    """谱里"弱二重体 + 电中性"的块数（$Y=\pm1/2$ 的 $(1,2,2)_0$ 切片）：轻 Higgs 的含量。"""
    return sum(1 for nm in reps for p in PIECES[nm]
               if p['lr'] == PHI_LR and abs(F(p['y'])) == F(1, 2))


def key_of(pc):
    return (pc['rep'], pc['lr'], pc['y'])


def rec3_of(nm):
    r"""母表示 `nm` 的**全部**分量求和后，$\Delta b$ 在重组的三个 SM 方向上的投影。

    横坐标顺序与 `predict_th` 一致：$(\Delta b_3,\ \Delta b_{2L},\ (3/5)(\Delta b_{2R}+\Delta b_{B-L}/4))$。
    """
    tot = [sum(pc['db'][i] for pc in PIECES[nm]) for i in range(4)]
    return [tot[0], tot[1], F(3, 5) * (tot[2] + tot[3] / 4)]


TOTS = {}
for _nm, _cs in SCALARS:
    TOTS[_nm] = rec3_of(_nm)


# =============================================================== 相位基线（无标量）
BASE_LR = [C.b_of(f, C.F3, []) for f in FACS_LR]
BASE_SM = [F(3, 5) * C.b_of(('U1', C.YHP, 'Y'), C.F3, []),
           C.b_of(('SU', 2, 'L'), C.F3, []), C.b_of(('SU', 3), C.F3, [])]


def pc_t(pc, x):
    """分量的对数质量：light 以 $M_Z$ 为锚，offset 以 $t_B+\\delta$ 给出。"""
    return TZ + pc['p'] if pc['mode'] == 'light' else x[1] + pc['p']


def predict_th(spec, x):
    r"""向下跑到 $M_Z$：返回 $(\alpha_1^{-1},\alpha_2^{-1},\alpha_3^{-1})$，$x=(\alpha_G^{-1},t_B,t_G)$。

    $SU(3)_c$、$SU(2)_L$ 跨 $t_B$ 不破 ⇒ 分量的长度是 $t_G-\max(t_j,t_Z)$，与基线的
    两段拆分相加等价；阿贝尔部分在 $t_B$ 处走
    $\alpha_1^{-1}=(3/5)(\alpha_{2R}^{-1}+\alpha_{B-L}^{-1}/4)$，其初值 $(3/5)(1+k_{B-L}/4)=1$
    由链探针的 S4.1 保证。
    """
    AG, tB, tG = x
    A = [AG + ((3.0 / 5.0) * (float(BASE_LR[2]) + float(BASE_LR[3]) / 4.0) * (tG - tB)
               + float(BASE_SM[0]) * (tB - TZ)) / TWOPI,
         AG + (float(BASE_LR[1]) * (tG - tB) + float(BASE_SM[1]) * (tB - TZ)) / TWOPI,
         AG + (float(BASE_LR[0]) * (tG - tB) + float(BASE_SM[2]) * (tB - TZ)) / TWOPI]
    for pc in spec:
        tj = pc_t(pc, x)
        Lc = tG - max(tj, TZ)                                   # 不破因子：全程连续
        La = tG - max(tj, tB)                                   # 阿贝尔：只在 $t_B$ 以上
        Ls = max(0.0, tB - tj)                                  # 阿贝尔：$t_B$ 以下换 SM 基
        db = pc['db']
        A[0] += ((3.0 / 5.0) * (float(db[2]) + float(db[3]) / 4.0) * La
                 + float(pc['db_sm'][0]) * Ls) / TWOPI
        A[1] += float(db[1]) * Lc / TWOPI
        A[2] += float(db[0]) * Lc / TWOPI
    return A


X0 = [45.0, 30.0, 36.0]      # 仿射展开点：必须落在物理分支内（$t_G>t_B>t_Z$）


def jac(spec, x0):
    r"""映射在物理分支内**仿射** ⇒ 探针基给精确雅可比（与链探针同一手法）。

    展开点不能取原点：$\max(\cdot)$ 让映射分段仿射，跨分支取探针会解错 ⇒ 必须在物理侧取点。
    """
    f0 = predict_th(spec, x0)
    J = [[predict_th(spec, [x0[k] + (1.0 if k == j else 0.0) for k in range(3)])[i] - f0[i]
          for j in range(3)] for i in range(3)]
    return f0, J


def solve_th(spec):
    """解 $F(x)=\\alpha_i^{-1}(M_Z)$。"""
    f0, J = jac(spec, X0)
    rhs = [C.A_MZ[i] - f0[i] for i in range(3)]
    u = C._solve_n(J, rhs, 3)
    if u is None:
        return None
    x = [X0[k] + u[k] for k in range(3)]
    resid = [predict_th(spec, x)[i] - C.A_MZ[i] for i in range(3)]
    ordered = x[2] > x[1] > TZ and x[0] > 0
    valid = all(x[2] >= pc_t(pc, x) + 1e-12 for pc in spec)
    MGUT = math.exp(x[2])
    return {'x': x, 'AG': x[0], 'tB': x[1], 'tG': x[2], 'MGUT': MGUT, 'MB': math.exp(x[1]),
            'resid': resid, 'spread': max(abs(r) for r in resid),
            'ordered': ordered, 'decoupled_ok': valid,
            'tau_p': C.proton_tau(MGUT, x[0])[0] if ordered else float('nan')}


# =============================================================== 谱配置
def spec_of(picks):
    out = []
    for k, mode, p in picks:
        q = dict(BY_KEY[k])
        q['mode'], q['p'] = mode, p
        out.append(q)
    return out


def phi_picks(light_y='1/2'):
    return [((p['rep'], p['lr'], p['y']), 'light' if p['y'] == light_y else 'offset', 0.0)
            for p in PIECES['10_H'] if p['lr'] == PHI_LR]


def spec_B():
    return spec_of(phi_picks())


def spec_C():
    return spec_of([(k, 'light', 0.0) for k, _m, _p in phi_picks()])


def spec_full(reps=('10_H', '45_H'), extra_light=()):
    lk = ('10_H', PHI_LR, '1/2')
    return spec_of([(k, 'offset' if k != lk and k not in extra_light else 'light', 0.0)
                    for nm in reps for p in PIECES[nm] for k in [key_of(p)]])


def spec_at_tB(reps=None):
    """把 `reps`（默认全部母表示）的**每一个**分量都放在 $t_B$：完整的母表示、单一标度。"""
    return spec_of([(key_of(p), 'offset', 0.0)
                    for nm in ([x[0] for x in SCALARS] if reps is None else reps)
                    for p in PIECES[nm]])


def moved(spec, k, delta):
    out = []
    for pc in spec:
        q = dict(pc)
        if key_of(pc) == k and q['mode'] == 'offset':
            q['p'] = delta
        out.append(q)
    return out


# =============================================================== 门禁
def run_gates():
    p = True
    c_ok = True if C.K_BL is not None else C.run_engine_tests()
    r_ok = R.run_engine_tests()
    p &= ok('T0.1', '上游 `so10_chain.py` 的 S 门禁全 PASS（荷约定 + 一环机器）', c_ok,
            '否则本脚本的 $\\Delta b$ 无意义')
    p &= ok('T0.2', '上游 `so10_reps.py` 的 R 门禁全 PASS（权重格 + 分支规则）', r_ok,
            '分量清单由这台引擎给出')
    p &= exact('T0.3', '引用的 $k_{B-L}$（链引擎推导值，$\\alpha_{B-L}^{-1}$ 的初值因子）',
               C.K_BL, F(8, 3))
    for nm, cs, ws, want in (('16', (0, 0, 0, 0, 1), C.W16(), 16),
                             ('10', (1, 0, 0, 0, 0), C.W10(), 10),
                             ('45', (0, 1, 0, 0, 0), C.W45(), 45)):
        got = ms_of(sum([[to_chain(w)] * k for w, k in R.irrep(cs)[1].items()], []))
        p &= exact('T1.%s' % nm, '格点换算后 %s 的权重多重集 = 链探针原集（含重数）' % nm,
                   sum(got.values()), want)
        p &= ok('T1.%s.b' % nm, '%s：换算后与链探针逐个权重相同' % nm,
                got == ms_of(ws), '不只是总数相同')
    phi = [pc for pc in PIECES['10_H'] if pc['lr'] == PHI_LR]
    sig = [pc for pc in PIECES['45_H'] if pc['lr'] == '(1,1,3)_{0}']
    p &= exact('T2.1', '$10_H$ 沿 $3221$ 的 $(1,2,2)_0$ 分量 = 链探针手写的 $\\Phi$',
               sorted(ms_of(sum([pc['ws'] for pc in phi], [])).items()),
               sorted(ms_of(C.BIDOUBLET).items()), '分量内容与 R6 同源，不再手写')
    p &= exact('T2.2', '$45_H$ 的 $(1,1,3)_0$ 分量 = 链探针手写的 $\\Sigma(1,1,3)_0$',
               sorted(ms_of(sum([pc['ws'] for pc in sig], [])).items()),
               sorted(ms_of(C.SIGMA_R).items()),
               '与 R6 判定一致：$\\Sigma$ 取自 $45_H$，$\\Delta_R$ 才属 $126_H$')
    dr = [pc for pc in PIECES['126_H'] if pc['lr'] == '(1,1,3)_{-2}']
    p &= exact('T2.3', '$126_H$ 的 $\\Delta_R$（此标号下 $B-L=-2$）沿 $Y$ 切成三个 $SU(2)_L$ 单态',
               sorted(pc['y'] for pc in dr), sorted(['-2', '-1', '0']),
               '$Y=T^3_R+(B-L)/2$：含双电荷分量 $Y=-2$ ⇒ 取期望值即破电磁；共轭表示给出相反号')
    hd = [pc for pc in phi if pc['y'] == '1/2']
    p &= exact('T2.4', '被切的两个二重态中 $Y=+1/2$ 者 = 链探针的 $H_D$',
               sorted(ms_of(hd[0]['ws']).items()), sorted(ms_of(C.HD).items()),
               '$M_Z$ 锚定的是它，不是整块 $\\Phi$')
    return p


def gate_T3():
    p = True
    for i, f in enumerate(FACS_LR):
        mine = BASE_LR[i] + sum(pc['db'][i] for pc in PIECES['10_H'] if pc['lr'] == PHI_LR)
        p &= exact('T3.L%d' % (i + 1), 'LR 相位 %s：基线 + 逐分量 $\\Delta b$ = 链探针 $b_{\\rm LR}(B)$'
                   % LRN[i], mine, C.b_LR('B')[i], '两台机器必须给出同一个数')
    hd = [pc for pc in PIECES['10_H'] if pc['lr'] == PHI_LR and pc['y'] == '1/2']
    for i in range(3):
        mine = BASE_SM[i] + sum(pc['db_sm'][i] for pc in hd)
        p &= exact('T3.S%d' % (i + 1), 'SM 相位 %s：基线 + $H_D$ 的 $\\Delta b$ = 链探针 $b_{\\rm SM}(B)$'
                   % SMN[i], mine, C.b_SM('B')[i],
                   '$b_{\\rm SM}(C)-b_{\\rm SM}(B)=\\Delta b(H_D)$：情形 C 只是多留一个二重态')
    p &= exact('T3.F1', '费米子跨 $t_B$ 连续：$(3/5)[T_{2R}+T_{B-L}/4](3\\times16)$ = $(3/5)T_Y(3\\times16)$',
               F(3, 5) * (C.factor_T(('SU', 2, 'R'), C.F3)
                          + C.factor_T(('U1', C.BL, 'B-L'), C.F3) / 4),
               F(3, 5) * C.factor_T(('U1', C.YHP, 'Y'), C.F3),
               '不成立就意味着费米子在 $B-L$ 破缺处漏了一项阈值')
    p &= exact('T3.F2', '费米子跨 $t_B$ 连续：$T_3(3\\times16)$ 与 $T_{2L}(3\\times16)$ 在两相位同值',
               (BASE_LR[0], BASE_LR[1]), (BASE_SM[2], BASE_SM[1]),
               '这两个因子在 $t_B$ 处不破 ⇒ 基线也必须相接')
    return p


def gate_T4():
    r"""退化哨兵：把分量谱放回链探针的整块配置，逐点复现 `C.predict(R3221)`。"""
    p = True
    for scn, mk in (('B', spec_B), ('C', spec_C)):
        for tG, tB in ((36.0, 30.0), (34.7, 27.3), (38.5, 33.1)):
            spec = mk()
            x = [7.31, tB, tG]
            p &= approx('T4.%s(%.1f)' % (scn, tG),
                        '情形 %s：逐分量机器 = `C.predict(R3221,%s)`' % (scn, scn),
                        predict_th(spec, x), list(C.predict('R3221', [x[0], x[1]], x[2], scn)),
                        TOL, '两条独立代码路径给出同一 $\\alpha_i^{-1}(M_Z)$')
    # 情形 A 不可由分量谱实现：它把 $H_D$ 与母表示 $\\Phi$ 解耦。差额必须恰为 $\\Phi$ 的贡献。
    x = [7.31, 30.0, 36.0]
    spec = spec_B()
    d = [predict_th(spec, x)[i] - C.predict('R3221', [x[0], x[1]], x[2], 'A')[i]
         for i in range(3)]
    phi = [pc for pc in PIECES['10_H'] if pc['lr'] == PHI_LR]
    D = 36.0 - 30.0
    exp = [(3.0 / 5.0) * float(sum(pc['db'][2] + pc['db'][3] / 4 for pc in phi)) * D / TWOPI,
           float(sum(pc['db'][1] for pc in phi)) * D / TWOPI,
           float(sum(pc['db'][0] for pc in phi)) * D / TWOPI]
    p &= approx('T4.A', '情形 A 与分量模型的差 = $\\Phi$ 在 $(t_B,t_G)$ 上的贡献（$H_D$ 被从母表示'
                        '上剥下来的代价）', d, exp, TOL,
                '⇒ A 不是某个分量谱的极限，而是人工配置；报告按分量模型读')
    return p


def gate_T5(base, det):
    p = True
    p &= approx('T5.1', '逐分量求解的 $M_{\\rm GUT}$ = 链探针 `solve_determined(R3221,B)`',
                [base['MGUT'], base['MB']], [det['scales']['M_GUT'], det['scales']['M_R']],
                1e-9, '同一物理配置的两条独立实现', rel=True)
    p &= approx('T5.2', '同一比较对 $\\alpha_{\\rm GUT}^{-1}$ 与 $\\tau_p$ 成立',
                [base['AG'], base['tau_p']], [det['alpha_GUT_inv'], det['tau_p_yr']],
                1e-9, '含质子寿命', rel=True)
    return p


def gate_T6(empty, allat):
    r"""**完整母表示**在单一中间标度上的阈值不移动 $M_{\rm GUT}$，只移动 $\alpha_{\rm GUT}^{-1}$。

    机制：一个完整 $SO(10)$ 表示沿 $3221$ 的全部分量，其 $\Delta b$ 在重新组合后的三个 SM
    方向上**逐因子相等**（$SO(10)$ 对合性）⇒ 对 $\alpha_i^{-1}$ 的影响是一个公共平移，
    被 $\alpha_{\rm GUT}^{-1}$ 吸收，统一点不动。故 $M_{\rm GUT}$ 的摆动只来自**同一母表示
    内部的分量分裂**，不是来自"多一个完整表示"。
    """
    p = True
    p &= ok('T6.0', '分量键 (母表示, 3221 标签, Y) 无碰撞 ⇒ 清单没有静默丢件',
            len(BY_KEY) == sum(len(v) for v in PIECES.values()),
            '若碰撞，下面的"全部分量求和"会少数块')
    csum = F(0)
    for nm, _cs in SCALARS:
        rec3 = TOTS[nm]
        csum += rec3[0]
        p &= exact('T6.%s' % nm, '$%s$ 全部分量求和后 $\\Delta b$ 在重组的三个 SM 方向上相等' % nm,
                   rec3, [rec3[0]] * 3,
                   '左 $=(\\Delta b_3,\\ \\Delta b_{2L},\\ (3/5)(\\Delta b_{2R}+\\Delta b_{B-L}/4))$'
                   '；逐**分量**不相等，只有整块相等')
    p &= approx('T6.4', '把 $10_H,45_H,126_H$ 的**全部**分量搬到 $t_B$：$t_G,t_B$ 一个不动',
                [allat['tG'], allat['tB']], [empty['tG'], empty['tB']], 1e-12,
                '统一点由 $\\alpha_i^{-1}$ 的**差**决定 ⇒ 公共平移被 $\\alpha_{\\rm GUT}^{-1}$ 吸收')
    p &= approx('T6.5', '$\\alpha_{\\rm GUT}^{-1}$ 的移动量 = 公共平移 $c\\,(t_G-t_B)/2\\pi$',
                (empty['AG'] - allat['AG']) * TWOPI / (empty['tG'] - empty['tB']),
                float(csum), 1e-9, '机制被定点（$c=%s$ 由整块求和给出），不是巧合' % csum, rel=True)
    p &= ok('T6.6', '上述"不动"伴随 $\\alpha_{\\rm GUT}^{-1}$ 的**明显**移动，且解仍在物理分支',
            abs(allat['AG'] - empty['AG']) > 1.0 and allat['ordered'] and allat['decoupled_ok'],
            '防"两边都没变"的空洞成立；$M_{\\rm GUT}>M_{B-L}>M_Z$ 与解耦条件仍成立')
    return p


# =============================================================== 响应
def response(spec, x):
    r"""$\partial\ln M_{\rm GUT}/\partial\ln M_j$：映射对每个 $t_j$ 也仿射 ⇒ 探针即精确导数，解 $J\dot x=-p_j$。

    $\ln M_j=t_j$、$\ln M_{\rm GUT}=t_G$ ⇒ 弹性度**就是** $\partial t_G/\partial t_j$，不额外乘
    $t_j/t_G$（那是把"对数之比"当成"对数的比"）。§7 的有限搬移与本表必须一致，由 T7 门禁钉住。
    """
    _f0, J = jac(spec, x)
    f0 = predict_th(spec, x)
    rows = []
    for j in range(len(spec)):
        sp = [dict(q) for q in spec]
        sp[j]['p'] = sp[j]['p'] + 1.0
        pcol = [predict_th(sp, x)[i] - f0[i] for i in range(3)]
        dx = C._solve_n(J, [-v for v in pcol], 3)
        tj = pc_t(spec[j], x)
        q = spec[j]
        rows.append({'rep': q['rep'], 'lr': q['lr'], 'y': q['y'], 'mode': q['mode'],
                     'lnM': tj, 'dlnMGUT_dlnMj': dx[2],
                     'dtB_dtj': dx[1], 'dAG_dtj': dx[0]})
    return rows


def pct(v):
    return '%+.4f' % v


def gate_T7(resp, split_rows, delta):
    r"""§6 的导数表与 §7 的有限搬移必须给出同一个数。

    映射分段仿射 ⇒ "弹性度 $\\times\\delta/\\ln10$" 应当**精确**等于实测 $\\Delta\\log_{10}M_{\\rm GUT}$。
    不相等就意味着 $\\delta$ 把分量推过了 $\\max(\\cdot)$ 的分段点，此时 §6 的导数在那个方向上没有意义。
    """
    p = True
    by = dict(((r['rep'], r['lr'], r['y']), r['dlnMGUT_dlnMj']) for r in resp)
    worst, hit = 0.0, 0
    for r in split_rows:
        if r['key'] in by:
            hit += 1
            worst = max(worst, abs(delta * by[r['key']] / math.log(10.0) - r['dlog10']))
    p &= ok('T7.1', '§7 的每一行都能在 §6 的响应表里找到同一个分量',
            hit > 0 and hit == len(split_rows), '匹配 %d/%d 行' % (hit, len(split_rows)))
    p &= approx('T7.2', '弹性度 $\\times\\delta/\\ln10$ = 实测 $\\Delta\\log_{10}M_{\\rm GUT}$'
                        '（$\\delta=%g$ 个 e _fold，逐行取最大偏差）' % delta,
                worst, 0.0, 1e-9, '导数表与有限实验互检 ⇒ 跨分段点就会破裂')
    return p


# =============================================================== T8：补入 $120_H$
def gate_T8(rv, gap, three, four, split, el, delta):
    r"""R9 留下的那条缺位：**两条闭合的手征道里，$120$ 这条没有母表示**（链探针三情形只声明
    $10_H$ 与 $45_H$）。本节把 $120_H$ 补进本机同一台分量机器里重跑，给"补上它要付什么"定价。

    三条结论都是**实测**而不是断言式的安慰：整块补入按 T6 机制**不动** $M_{\\rm GUT}$，
    但它吃掉的 $\\alpha_{\\rm GUT}^{-1}$ 比三块声明谱总共吃掉的还多 ⇒ 解离开微扰分支；
    分裂补法（只留它的中性二重体在电弱标度）既动 $M_{\\rm GUT}$ 又同样出分支。
    """
    p = True
    p &= ok('T8.0', '表示论引擎的整条推导链（标号认定 → 张量恒等式 → 物理判定 → 分支规则 → '
                    '跨链匹配 → Yukawa 层 → 不变张量簿记 → 道分解）在本机进程内按它自己 `main()` '
                    '的顺序跑通；跑推导函数，不读它写出的报告产物', rv,
            'R9 道分解层要读 R8 的 $\\mathrm{inv}(16^4)$ 计数 ⇒ 跳层就是 `KeyError`，'
            '所以本节拿到的是**现算**的 `CSPLIT`/`TABLE`')
    p &= ok('T8.1', '缺位是**读出来**的：闭合的手征道 $\\setminus$ 已声明的母表示 $=120$，'
                    '且本机声明谱里也没有 $120_H$',
            gap['missing'] == ['120'] and REP120 not in [x[0] for x in SCALARS],
            '闭合道 %s；声明并集 %s；本机 SCALARS %s' %
            (gap['closed'], gap['declared'], [x[0] for x in SCALARS]))
    p &= exact('T8.2', '本机补入的标号 = 表示论引擎独立认定的 $\\wedge^2(16)=120$ 的标号'
                       '（标号由权重多重集等式选出，非引用）',
               list(CS_120), list(R.NAMED['120']))
    p &= ok('T8.3', '$120_H$ 的分量内容与表示论引擎那张 3221 分支表（R6.7 已与两步路径逐项对过）'
                    '按标签+重数一致', label_mult(REP120) == reps_label_mult('120'),
            '%d 个标签；$(1,2,2)_0$ 重数 %s；Y 切片后 %d 块' %
            (len(label_mult(REP120)), label_mult(REP120).get(PHI_LR), len(PIECES[REP120])))
    sg, bd = t8_rows(REP120)
    p &= exact('T8.4', '$120_H$ 的权重账：全部 $Y$ 切片的重数加权权重数之和 = 整块维数',
               sum(p_['ndim'] for p_ in PIECES[REP120]), R.irrep(CS_120)[2])
    qs = sorted(set(q for pc in sg for q in q_spectrum(pc)))
    row120 = [x for x in R.TABLE if x['name'] == '120'][0]
    p &= ok('T8.5', '$120_H$ 里 $\\lvert B-L\\rvert =2$ 的色单态**全部**带 $Q\\ne0$ ⇒ 补上它**给不出** '
                    '$B-L$ 破缺（本机按 Cartan 方向直算 $Q$）',
            bool(qs) and all(q != 0 for q in qs) and qs == [F(-1), F(1)],
            '$Q$ 谱 %s；与表示论引擎 R5.8 的判定对账：含 $(1,1,1)_{\\pm2}$ = %s、'
            '"能破 $B-L$ 而保 $U(1)_{em}$" = %s' %
            ('、'.join(str(q) for q in qs), row120['S2'], row120['safe']))
    m120 = label_mult(REP120)[PHI_LR]
    ld3 = light_doublets([x[0] for x in SCALARS])
    ld4 = light_doublets([x[0] for x in SCALARS] + [REP120])
    p &= ok('T8.6', '$120_H$ 的 $(1,2,2)_0$ 重数为 %s ⇒ 按 $Y$ 切成 %d 块电中性二重体'
                    '（$\\lvert Y\\rvert =1/2$，每块重数 %s）。声明谱本有 %d 块这样的切片，补入后 %d 块；'
                    '本机把"轻的那一块"钉在 $10_H$ 的 $Y=+1/2$ 上（`spec_full` 的锚点），'
                    '**没有任何机制**说明为什么是它 ⇒ 补入 $120_H$ 把"哪个二重体留在电弱标度"'
                    '从 %d 选 1 变成 %d 选 1' % (m120, len(bd), m120, ld3, ld4, ld3, ld4),
            m120 == 2 and len(bd) == 2 and all(p_['n'] == m120 for p_ in bd)
            and ld4 - ld3 == len(bd) and ld3 >= 2,
            '$120_H$ 的 $(1,2,2)_0$ 切片：$Y=$ %s；声明谱 %d 块 $\\to$ 补入后 %d 块'
            % ('、'.join(p_['y'] for p_ in bd), ld3, ld4))
    rec3 = rec3_of(REP120)
    p &= exact('T8.7', '$120_H$ 全部分量求和后 $\\Delta b$ 在重组的三个 SM 方向上相等'
                       '（T6 机制对第四块同样成立）', rec3, [rec3[0]] * 3,
               '$c(120_H)=%s$，对照 $c(10_H)=%s$、$c(45_H)=%s$、$c(126_H)=%s$' %
               (rec3[0], TOTS['10_H'][0], TOTS['45_H'][0], TOTS['126_H'][0]))
    p &= approx('T8.8', '把 $120_H$ **整块**搬到 $t_B$：$t_G,t_B$ 一个不动（与三块声明谱同解）',
                [four['tG'], four['tB']], [three['tG'], three['tB']], 1e-12,
                '统一点由 $\\alpha_i^{-1}$ 的**差**决定 ⇒ 公共平移被 $\\alpha_{\\rm GUT}^{-1}$ 吸收')
    pred = float(rec3[0]) * (three['tG'] - three['tB']) / TWOPI
    p &= approx('T8.9', '$\\alpha_{\\rm GUT}^{-1}$ 的移动量 $=c(120_H)(t_G-t_B)/2\\pi$'
                        '（机制被整块求和定点，不是拟合）',
                three['AG'] - four['AG'], pred, 1e-9,
                '实测 %.6f vs 预言 %.6f' % (three['AG'] - four['AG'], pred))
    p &= ok('T8.10', '但补入后 $\\alpha_{\\rm GUT}^{-1}<0$ ⇒ 解**离开物理分支**（一环外推落入'
                     '强耦合，$\\tau_p$ 因此无定义），而三块声明谱仍在分支内（防"两边都出界"的空洞）',
            four['AG'] < 0 and not four['ordered'] and three['AG'] > 0 and three['ordered'],
            '$\\alpha_{\\rm GUT}^{-1}$：%.2f $\\to$ %.2f（吃掉 %.1f）' %
            (three['AG'], four['AG'], three['AG'] - four['AG']))
    p &= ok('T8.11', '分裂补法（只把 $120_H$ 的 $(1,2,2)_0$，$Y=+1/2$ 那块放到 $M_Z$，其余留在 $t_B$）'
                     '同样出分支，且**这次真的动** $M_{\\rm GUT}$ ⇒ "整块不动"依赖的是完整多重态',
            split['AG'] < 0 and abs(math.log10(split['MGUT'] / three['MGUT'])) > 1e-3,
            '$\\log_{10}M_{\\rm GUT}$ 移动 %+.4f（$%.3e\\to%.3e$ GeV）、$\\alpha_{\\rm GUT}^{-1}$'
            ' $=%.2f$ ⇒ 两种补法都在一环微扰适用范围之外' %
            (math.log10(split['MGUT'] / three['MGUT']), three['MGUT'], split['MGUT'], split['AG']))
    key = (REP120, PHI_LR, '1/2')
    e = [r for r in el['resp'] if (r['rep'], r['lr'], r['y']) == key]
    p &= approx('T8.12', '新补进来的那块二重体也进 §6/§7 的互检：弹性度 $\\times\\delta/\\ln10$ '
                         '= 重解一次后的 $\\Delta\\log_{10}M_{\\rm GUT}$（$\\delta=%g$）' % delta,
                delta * e[0]['dlnMGUT_dlnMj'] / math.log(10.0), el['dlog10'], 1e-9,
                '弹性度 %s ⇒ 每 e _fold 动 %.1f%%' %
                (pct(e[0]['dlnMGUT_dlnMj']), 100.0 * (math.exp(abs(e[0]['dlnMGUT_dlnMj'])) - 1.0)))
    wrong = float(TOTS['10_H'][0]) * (three['tG'] - three['tB']) / TWOPI
    cut = [p_ for p_ in PIECES[REP120] if p_['lr'] != PHI_LR]
    tot = [sum(p_['db'][i] for p_ in cut) for i in range(4)]
    rec3c = [tot[0], tot[1], F(3, 5) * (tot[2] + tot[3] / 4)]
    p &= ok('T8.13', '两条变异测试钉住 T8.9/T8.7 不是恒真：把 $c$ 换成 $10_H$ 的 %s ⇒ 预言从 %.4f '
                     '变成 %.4f（实测 %.4f）；从整块求和里删掉 $(1,2,2)_0$ ⇒ 三方向不再相等 %s'
            % (TOTS['10_H'][0], pred, wrong, three['AG'] - four['AG'],
               '（%s）' % '、'.join(str(x) for x in rec3c)),
            abs(wrong - (three['AG'] - four['AG'])) > 1.0 and rec3c[0] != rec3c[1],
            '植入读数：错 $c$ 的预言 %.6f、删块后的三方向 %s' % (wrong, rec3c))
    p &= ok('T8.14', '$120$ 落在道分解的反对称槽 $\\wedge^2(16)$ ⇒ §9 末"只有它则三代 Yukawa '
                     '秩为偶"那句话有出处，不是从记忆里抄的（槽位由 `so10_reps.py` 的 R9 层给出）',
            gap['slot120'] == 'anti',
            'slotof[$120$] = %s；本机 $120_H$ 的标号 %s 即 $\\wedge^2(16)$ 的那个 $SO(10)$ 不可约块'
            % (gap['slot120'], tuple(CS_120)))
    return p


# =============================================================== 报告
def write_report(rows_gate, base, full, d126, resp, split_rows, empty, allat, t8):
    L = []
    A = L.append
    A('# SO(10) 阈值层报告（逐分量 $\\Delta b$、统一点响应、补入 $126_H$/$120_H$ 后重跑）')
    A('')
    A('> 由 `so10_thresholds.py` 生成。上游：`so10_reps.py`（分支规则）、`so10_chain.py`（一环跑动）。')
    A('> 零第三方依赖；$\\Delta b$ 全程精确有理数，统一点由一次仿射求解给出。')
    A('')
    A('## 1. 这一块在 L10 里的位置')
    A('')
    A('* 链探针给出 $M_{\\rm GUT}$ 对**标量谱**的依赖是一个区间，但区间宽度没被分解过。')
    A('  本脚本把谱拆到 **SM 多重态** 粒度（分支表 + $Y$ 切分，全部推导），给出每块的')
    A('  $\\Delta b$、$\\partial\\ln M_{\\rm GUT}/\\partial\\ln M_j$，并执行 08 登记的待办'
      '"必须补入 $126_H$ 后重跑"。')
    A('* §9 用同一台机器再做一遍同体例的事：把 R9 道分解判为"闭合却没有母表示"的那条 $120$ 道'
      '（缺位由本机的门禁读出，不靠散文记忆）补进谱里重跑，给这条缺口定价。')
    A('* **两环未做**：一般群乘积的两环系数矩阵 $b_{ij}$ 需外部公式，本次会话内无法在仓库里'
      '  核验 ⇒ **不凭记忆写**。所有结论都是一环 + 阈值。')
    A('* **只有对数项**：阈值的有限部分（匹配方案、Goldstone/鬼场）未算 ⇒ §6/§7 是领先对数量级。')
    A('* **不需要 Yukawa**：一环规范 $\\beta$ 无 Yukawa 项（结构事实）。')
    A('')
    A('## 2. 门禁')
    A('')
    A('| 编号 | 命题 | 计算值 | 期望值 | 容差 | 判定 |')
    A('|---|---|---|---|---|---|')
    for r in rows_gate:
        # 表格单元格里**一个**反斜杠才算转义竖线；写两个 ⇒ GFM 把"反斜杠+反斜杠"读成一个字面
        # 反斜杠，紧跟其后的竖线就照常分裂单元格 ⇒ 行多出不存在的列、渲染错位，而门禁全 PASS。
        # 本文件上一版正是这样（`'\\\\|'`），2026-09-24 由 维护脚本/build_tables.py 的列数核对抓出。
        A('| %s | %s | %s | %s | %s | %s |' %
          (r['id'], str(r['claim']).replace('|', '\\|'), r['computed'], r['expected'],
           r['tolerance'], r['status']))
    A('')
    n_pass = sum(1 for r in rows_gate if r['status'] == 'PASS')
    A('合计 %d 项，PASS %d ⇒ **%s**。' % (len(rows_gate), n_pass,
                                        '全 PASS' if n_pass == len(rows_gate) else '存在 FAIL'))
    A('')
    A('## 3. 相位基线（纯规范 + 三代费米子，由权重格推导）')
    A('')
    A('| LR 相位因子 | 基线值（纯规范 + $3\\times16$） |')
    A('|---|---|')
    for i in range(4):
        A('| %s | %s |' % (LRN[i], BASE_LR[i]))
    A('')
    A('| SM 相位因子 | 基线值（纯规范 + 三代费米子） |')
    A('|---|---|')
    for i in range(3):
        A('| %s | %s |' % (SMN[i], BASE_SM[i]))
    A('')
    A('链探针的整块值 $b_{\\rm LR}(B)=(%s)$、$b_{\\rm SM}(B)=(%s)$ 与"基线 + 逐分量 $\\Delta b$"'
      '逐项相等（T3）⇒ 分量机器与整块机器同源。' %
      (', '.join(str(x) for x in C.b_LR('B')), ', '.join(str(x) for x in C.b_SM('B'))))
    A('')
    A('## 4. 分量清单与逐分量 $\\Delta b$（分支表 → $Y$ 切分）')
    A('')
    A('| 母表示 | $3221$ 分量 | $Y$ | 权重数 | $\\Delta b_3$ | $\\Delta b_{2L}$ | '
      '$\\Delta b_{2R}$ | $\\Delta b_{B-L}$ |')
    A('|---|---|---|---|---|---|---|---|')
    for nm, _cs in SCALARS:
        for pc in PIECES[nm]:
            A('| %s | %s | %s | %d | %s |' % (nm, pc['lr'], pc['y'], pc['ndim'],
                                              ' | '.join(str(x) for x in pc['db'])))
    A('')
    A('## 5. 统一点：退化基准、全谱简并、补入 $126_H$')
    A('')
    A('| 配置 | $\\alpha_{\\rm GUT}^{-1}$ | $M_{B-L}$ (GeV) | $M_{\\rm GUT}$ (GeV) | 残差 | '
      '$\\tau_p$ (年) | 序 |')
    A('|---|---|---|---|---|---|---|')
    A('| 链探针 `solve_determined(R3221,B)` | %s | %s | %s | %s | %s | — |' %
      ('%.4f' % D0['alpha_GUT_inv'], '%.3e' % D0['scales']['M_R'],
       '%.3e' % D0['scales']['M_GUT'], '%.1e' % D0['spread'], '%.3e' % D0['tau_p_yr']))
    for row, nm in ((base, '同一谱的逐分量版本'),
                    (full, '$10_H\\oplus45_H$ 全部分量与 $B-L$ 同标度'),
                    (d126, '$10_H\\oplus45_H\\oplus126_H$ 全部分量与 $B-L$ 同标度')):
        A('| %s | %s | %s | %s | %s | %s | %s |' %
          (nm, '%.4f' % row['AG'], '%.3e' % row['MB'], '%.3e' % row['MGUT'],
           '%.1e' % row['spread'], '%.3e' % row['tau_p'],
           'ok' if (row['ordered'] and row['decoupled_ok']) else '越界'))
    A('')
    A('第 1、2 行是**同一物理配置的两条独立实现**（T5 门禁用它对齐）。第 3、4 行换谱：'
      '把母表示的其余分量从"$M_{\\rm GUT}$ 之上"搬到 $B-L$ 标度，考察统一点与 $\\tau_p$ 的移动。')
    A('')
    A('## 6. 分量级响应 $\\partial\\ln M_{\\rm GUT}/\\partial\\ln M_j$')
    A('')
    A('在"$10_H\\oplus45_H\\oplus126_H$ 全谱简并"这一点上求导（$\\delta_j=0$）：')
    A('')
    A('| 母表示 | $3221$ 分量 | $Y$ | 所在 | $\\partial\\ln M_{\\rm GUT}/\\partial\\ln M_j$ | '
      '$\\partial\\alpha_{\\rm GUT}^{-1}/\\partial t_j$ | $\\partial t_B/\\partial t_j$ |')
    A('|---|---|---|---|---|---|---|')
    for r in resp:
        A('| %s | %s | %s | %s | %s | %s | %s |' %
          (r['rep'], r['lr'], r['y'], r['mode'], pct(r['dlnMGUT_dlnMj']), pct(r['dAG_dtj']),
           pct(r['dtB_dtj'])))
    big = max(resp, key=lambda r: abs(r['dlnMGUT_dlnMj']))
    zero = ['$%s\\ %s$（$Y=%s$）' % (r['rep'], r['lr'], r['y']) for r in resp
            if abs(r['dlnMGUT_dlnMj']) < 1e-14]
    strong = [r for r in resp if abs(r['dlnMGUT_dlnMj']) >= 0.1]
    ncol = sum(1 for r in strong if not r['lr'].startswith('(1,'))
    A('')
    A('读法：正号 = 该分量变重把统一点**推高**；数值就是对数弹性度，'
      '搬 $\\delta$ 个 e _fold 就动 $\\Delta\\ln M_{\\rm GUT}\\approx\\delta\\times$ 该值。')
    A('')
    A('* 弹性度 $\\ge0.1$ 的分量共 %d 个，其中 %d 个带色 ⇒ 统一点主要被**有色标量**的位置牵着走。'
      % (len(strong), ncol))
    A('* 最大者：%s %s（$Y=%s$）$=%s$ ⇒ 单是它每 e _fold 就能把 $M_{\\rm GUT}$ 推动 $%.0f\\%%$。'
      % (big['rep'], big['lr'], big['y'], pct(big['dlnMGUT_dlnMj']),
         100.0 * (math.exp(abs(big['dlnMGUT_dlnMj'])) - 1.0)))
    A('* 弹性度**精确为零**的分量：%s ⇒ 搬它们不改变统一点，只改变 $\\alpha_{\\rm GUT}^{-1}$。'
      % '、'.join(zero))
    A('* 本表与 §7 的有限搬移逐行对上（T7.2：最大偏差 $10^{-13}$ 量级）⇒ 导数不是在分段点之外编的。')
    A('')
    A('## 7. 单个分量上移 %g 个 e _fold 的后果' % DELTA)
    A('')
    A('| 移动的分量 | $Y$ | $\\Delta\\log_{10}M_{\\rm GUT}$ | $M_{\\rm GUT}$ (GeV) | $\\tau_p$ (年) |')
    A('|---|---|---|---|---|')
    for r in split_rows:
        A('| %s %s | %s | %s | %.3e | %.3e |' %
          (r['key'][0], r['key'][1], r['key'][2], pct(r['dlog10']), r['MGUT'], r['tau_p']))
    A('')
    drop = ['$%s\\ %s$（$Y=%s$）' % (r['rep'], r['lr'], r['y']) for r in resp
            if r['mode'] != 'light'
            and (r['rep'], r['lr'], r['y']) not in set(x['key'] for x in split_rows)]
    A('每一行是**重解一次**统一点得到的（不是乘系数），且与 §6 的弹性度逐行相符（T7.2）。'
      '被搬的是所有**不轻**的分量；唯一排除的是锚在 $M_Z$ 的轻 Higgs——搬走它就不是同一个体系了。')
    A('')
    A('* 搬 %g 个 e _fold 后**越出物理分支**（$t_j\\ge t_G$ 或序不成立）而不进表的分量：%s。'
      % (DELTA, '、'.join(drop) if drop else '（无）'))
    A('  由此表内最大 $%.2f$ 低于 §6 的 $%.2f$——这不是两表矛盾，而是最敏感的那几块已经出了定义域。'
      % (max(abs(x['dlog10']) for x in split_rows),
         max(abs(r['dlnMGUT_dlnMj']) * DELTA / math.log(10.0) for r in resp)))
    A('')
    A('## 8. 完整母表示的阈值不摆动统一点（T6）')
    A('')
    A('| 配置 | $\\alpha_{\\rm GUT}^{-1}$ | $M_{B-L}$ (GeV) | $M_{\\rm GUT}$ (GeV) |')
    A('|---|---|---|---|')
    for row, nm in ((empty, '无标量（纯规范 + 三代费米子）'),
                    (allat, '$10_H\\oplus45_H\\oplus126_H$ 的**全部**分量放在同一标度 $t_B$')):
        A('| %s | %s | %s | %s |' % (nm, '%.4f' % row['AG'], '%.4e' % row['MB'],
                                     '%.4e' % row['MGUT']))
    A('')
    A('* 逐**分量**的 $\\Delta b$ 在三个 SM 方向上不相等，但整块求和后精确相等')
    A('  （$10_H$ 为 %s、$45_H$ 为 %s、$126_H$ 为 %s，三个方向同值）⇒ 完整多重态给 '
      '$\\alpha_i^{-1}$ 的是一个**公共平移**，只被 $\\alpha_{\\rm GUT}^{-1}$ 吸收。' %
      (TOTS['10_H'][0], TOTS['45_H'][0], TOTS['126_H'][0]))
    A('* 数值后果：上表两行的 $M_{B-L}$、$M_{\\rm GUT}$ 到 1e-12 完全相同（T6.4），'
      '而 $\\alpha_{\\rm GUT}^{-1}$ 移动 $%.1f$（T6.5 把移动量定点为 $c(t_G-t_B)/2\\pi$）。'
      % (empty['AG'] - allat['AG']))
    A('* ⇒ "本报告里 $M_{\\rm GUT}$ 依赖标量谱"这句话要**改写**：依赖的是**同一母表示内部的分量分裂**'
      '（§7 的实测移动），不是"多一个完整多重态"。$SO(10)$ 的对合性把后一种依赖整体吸收了。')
    A('* 顺带一条一环层面的排除：把 $10_H\\oplus45_H\\oplus126_H$ 整体搬到 $t_B$ 会吃掉 $%.1f$ 的 '
      '$\\alpha_{\\rm GUT}^{-1}$，剩下 $%.1f$ ⇒ "全套 GUT 标度谱"使规范耦合接近强耦合区。'
      % (empty['AG'] - allat['AG'], allat['AG']))
    A('  这条只在**一环 + 只有对数项**下成立，不外推为"自然界排除了它"。')
    A('* 括号里的配置没有轻 Higgs（全部在 $t_B$），它的作用是**结构对照**，不是一个能用的谱。')
    A('')
    A('## 9. 补入 $120_H$：那条"道闭合却没有母表示"的缺口要付什么')
    A('')
    A('* 缺口是**读**出来的，不是抄漏：表示论引擎（`so10_reps.py` 的 R9 道分解层）判为闭合的手征道是 '
      '%s，链探针三个情形声明过的母表示并集只有 %s ⇒ 差集 %s。本机 `SCALARS` 比那个并集多的 '
      '$126_H$ 是 §5 的补入实验、不是链的声明（引擎同一层已把"并集 $=\\{10,45\\}$、$126$ 与 $120$ '
      '都不在其中"钉成门禁），所以这不是两份台账抄漏，而是**群论说这条道能用、谱里却没有承载它的场**'
      '（T8.1）。' %
      ('、'.join('$%s$' % R.chan_tex(n) for n in t8['gap']['closed']),
       R.higgs_tex(t8['gap']['declared']),
       '、'.join('$%s$' % R.chan_tex(n) for n in t8['gap']['missing'])))
    A('* 补入走的是**同一条流水线**，不另起公式：$120_H$ 沿 $3221$ 分支 %d 个标签、按 $Y$ 切成 %d 块、'
      '重数加权权重数合计 %d（$=$ 引擎独立给出的整块维数 %s，T8.4），标签+重数与引擎那张分支表'
      '逐条相等（T8.3，本机自己算权重，不读它写出的产物）。' %
      (len(t8['lm']), len(PIECES[REP120]), sum(p['ndim'] for p in PIECES[REP120]),
       R.irrep(CS_120)[2]))
    A('')
    k120 = (REP120, PHI_LR, '1/2')
    e120 = [r for r in t8['resp'] if (r['rep'], r['lr'], r['y']) == k120][0]
    mv = t8['three']['AG'] - t8['four']['AG']
    pred89 = float(t8['rec3'][0]) * (t8['three']['tG'] - t8['three']['tB']) / TWOPI
    A('| 配置 | $\\alpha_{\\rm GUT}^{-1}$ | $M_{B-L}$ (GeV) | $\\log_{10}M_{\\rm GUT}$ | $\\tau_p$ (年) | 一环分支 |')
    A('|---|---|---|---|---|---|')
    for row, nm in ((t8['three'], '$10_H\\oplus45_H\\oplus126_H$（§5 末行，§6/§7 的求导点）'),
                    (t8['four'], '再补 $120_H$ **整块**：它的全部分量随 $B-L$ 同标度'),
                    (t8['split'], '分裂补法：只把 $120_H$ 的 $(1,2,2)_0$（$Y=+1/2$）留在 $M_Z$'),
                    (t8['move'], '整块补入 + 把那块二重体上移 %g 个 e _fold（§7 同款）' % DELTA)):
        A('| %s | %s | %s | %s | %s | %s |' %
          (nm, '%.4f' % row['AG'], '%.3e' % row['MB'], '%.4f' % math.log10(row['MGUT']),
           '%.3e' % row['tau_p'] if row['AG'] > 0 else '—（无定义）',
           '在' if (row['ordered'] and row['decoupled_ok']) else '**外**'))
    A('')
    A('* 前两行是 T6 机制对**第四块**的复验：$120_H$ 整块补进来后 $t_G,t_B$ 到 1e-12 一个不动（T8.8），'
      '$\\alpha_{\\rm GUT}^{-1}$ 的移动量精确等于 $c(120_H)(t_G-t_B)/2\\pi$，其中 $c(120_H)=%s$ 由'
      '整块求和给出、三个重组 SM 方向同值（T8.7）⇒ 实测 %.6f 对预言 %.6f，相对偏差 1e-9 以下（T8.9）。'
      '机制被定点，不是拟合出来的巧合。' % (t8['rec3'][0], mv, pred89))
    A('* **代价全部落在 $\\alpha_{\\rm GUT}^{-1}$ 上，而这正是不能付的那一项**：三块声明谱剩 %.2f，'
      '补入 $120_H$ 整块后是 %.2f，吃掉 %.2f（对照 §8：把 $10_H\\oplus45_H\\oplus126_H$ 全谱搬到同一'
      '标度还剩 %.2f）。负号意味着一环解已离开微扰分支 ⇒ $\\tau_p$ 无定义。所以"补上这条母表示"'
      '在本层是一条**否定性定价**，不是一个候选谱：整块补不动统一点，却把耦合推出适用范围。' %
      (t8['three']['AG'], t8['four']['AG'], mv, allat['AG']))
    A('* 分裂补法（第 3 行）也救不回来：$\\alpha_{\\rm GUT}^{-1}=%.2f$ 仍为负，而这一次 '
      '$\\Delta\\log_{10}M_{\\rm GUT}=%+.4f$（$M_{\\rm GUT}$ 从 $%.3e$ 到 $%.3e$ GeV，T8.11）'
      '⇒ "整块不摆动统一点"依赖的正是**完整多重态**这个前提；只留一块二重体，T6 的公共平移论证'
      '当场失效。两种补法都在一环微扰适用范围之外。' %
      (t8['split']['AG'], math.log10(t8['split']['MGUT'] / t8['three']['MGUT']),
       t8['three']['MGUT'], t8['split']['MGUT']))
    A('* 第 4 行给这块新二重体一个 §7 同款的有限实验：它的弹性度 $%s$ ⇒ 上移 %g 个 e _fold 后实测 '
      '$\\Delta\\log_{10}M_{\\rm GUT}=%+.4f$，与"弹性度 $\\times\\delta/\\ln10$"到 1e-9 相符（T8.12）'
      '⇒ 补进来的块同样过 §6$\\leftrightarrow$§7 的互检，导数表没有在分段点之外编数。' %
      (pct(e120['dlnMGUT_dlnMj']), DELTA,
       math.log10(t8['move']['MGUT'] / t8['four']['MGUT'])))
    sg, bd = t8_rows(REP120)
    qs = sorted(set(q for pc in sg for q in q_spectrum(pc)))
    A('* 内容层面两条，都不需要重解统一点：')
    A('  1. $120_H$ 的 $|B-L|=2$ 色单态是 $(1,1,1)_{\\pm2}$，沿 Cartan 方向直算得 $Q$ 谱 $=\\{%s\\}$，'
      '没有一个中性 ⇒ **补上它给不出 $B-L$ 破缺**（T8.5；与引擎 R5.8 同源，本机独立重算了一遍）。'
      '这条道不能替 $\\overline{126}_H$ 的 $\\Delta_R$ 去担那一步。' %
      '、'.join(str(q) for q in qs))
    A('  2. 它的 $(1,2,2)_0$ 重数为 %s ⇒ 按 $Y$ 切成 %d 块电中性二重体（$|Y|=1/2$）。声明谱本有 %d '
      '块这样的切片，补入后 %d 块（T8.6），而"轻的那一块"在本机里是**手工锚定**在 $10_H$ 的 '
      '$Y=+1/2$ 上的 ⇒ 补入 $120_H$ 把"哪个二重体留在电弱标度"从 %d 选 1 变成 %d 选 1，'
      '本层没有挑它的机制。（§4~§8 的读数仍是**声明谱**的读数，台账不因本节改写。）' %
      (t8['lm'].get(PHI_LR), len(bd), light_doublets([x[0] for x in SCALARS]),
       light_doublets([x[0] for x in SCALARS] + [REP120]),
       light_doublets([x[0] for x in SCALARS]),
       light_doublets([x[0] for x in SCALARS] + [REP120])))
    A('* 三条边界（写在门禁之外，免得被读成结论）：')
    A('  * 道分解把 $120$ 放在反对称槽 $\\wedge^2(16)$（T8.14 读自引擎的 R9 层）⇒ 若味 Yukawa 只有它，'
      '三代下耦合矩阵在代指标上反对称，秩为偶（$\\le2$）。这是味层的算术事实，本机没有代自由度，'
      '故不进门禁；它只是提醒"补上 $120_H$"连味结构也要一起改。')
    A('  * R9 那条老话仍成立：**某道闭合 $\\ne$ 存在一个可重整算符**，本节只给阈值定价，没有给动力学。')
    A('  * 本节的数与 §5~§8 同属"一环 + 只有对数项"，两环与阈值有限项未算（§1）⇒ 负号不外推为'
      '"自然界排除了 $120_H$"，只排除"在一环适用范围内它能补上这个缺口"。')
    A('')
    A('## 10. 结论与仍然未闭合的部分')
    A('')
    A('* 标量谱的依赖被**定量化**了：§6 给出每块的弹性度，§7 用"搬 %g 个 e _fold"重解一次做实测，'
      '两者逐行相符（T7）⇒ 这张响应表可查可验，不是一次性输出；' % DELTA)
    A('  §8 则给出哪一类谱摆动**根本不进入** $M_{\\rm GUT}$。')
    A('* 本层与链探针的逐项对账**改掉了链上一个已经 PASS 的数**：链探针情形 C 的 $b_2$ 把 $-(11/3)C_2$ '
      '的规范项重复计入了一次 ⇒ 修复后情形 C 的 $M_{\\rm GUT}$、$M_R$、$\\tau_p$ 全部改写，'
      '链自检 44→47（新增 S3.4–S3.6 回归门禁）。情形 B 与本报告的数不受影响。')
    A('  ⇒ "自检全 PASS"只说明**未被这些检验推翻**；能推翻它的是第二条独立的代码路径。')
    A('* $126_H$ 补入后统一点与 $\\tau_p$ 的移动见 §5 末行 ⇒ 08 登记的那条待办**已执行**（一环层面）。')
    A('* R9 那条缺位（$120$ 道闭合、却没有母表示承载）已在 §9 定价：整块补入按 T6 机制不动 '
      '$M_{\\rm GUT}$，却把 $\\alpha_{\\rm GUT}^{-1}$ 吃成负数；只留它的中性二重体则既动 $M_{\\rm GUT}$ '
      '又同样出分支 ⇒ 缺口**仍在**，但从今天起带着价签，且它给不出 $B-L$ 破缺（§9 内容层面第 1 条）。')
    A('* 情形 A（链探针里 $H_D$ 与母表示 $\\Phi$ 解耦的那个极端）**不是任何分量谱的极限**：'
      'T4.A 把差额写成 $\\Phi$ 在 $(t_B,t_G)$ 上的贡献，故本层不采用 A。')
    A('* **L10 未关闭**：剩下的仍是动力学（两环、阈值有限项、位势与真空方向、Yukawa 扇区），'
      '以及"自然界是否真的选了这条链"。本脚本不提升任何体系的证据等级，也不构成统一场论的完成。')
    txt = '\n'.join([R.table_row_safe(x) for x in L]) + '\n'
    assert txt.count('\r') == 0
    bad = sorted(set(ch for ch in txt if ord(ch) < 32 and ch not in '\n\t'))
    assert not bad, '报告含控制字符 %r' % bad
    check_cols(txt)
    with open(ROOT / 'SO10阈值报告.md', 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(txt)


def check_cols(txt):
    lines = txt.split('\\n')
    for i in range(len(lines) - 1):
        if lines[i].startswith('|') and R.SEPROW.match(lines[i + 1].strip()):
            ncol = len(R.PIPE.split(lines[i]))
            j = i + 2
            while j < len(lines) and lines[j].startswith('|'):
                n = len(R.PIPE.split(lines[j]))
                assert n == ncol, '第 %d 行列数 %d != 表头 %d：%s' % (j + 1, n, ncol, lines[j][:60])
                j += 1


D0 = {}


def main():
    global D0
    p = True
    p &= run_gates()
    p &= gate_T3()
    p &= gate_T4()
    det = C.solve_determined('R3221', 'B')
    D0 = det
    base = solve_th(spec_B())
    p &= gate_T5(base, D0)
    empty, allat = solve_th([]), solve_th(spec_at_tB())
    p &= gate_T6(empty, allat)
    full = solve_th(spec_full(('10_H', '45_H')))
    d126 = solve_th(spec_full(('10_H', '45_H', '126_H')))
    sp126 = spec_full(('10_H', '45_H', '126_H'))
    resp = response(sp126, d126['x'])
    split_rows = []
    for k in [key_of(pc) for pc in sp126 if pc['mode'] != 'light']:
        r = solve_th(moved(sp126, k, DELTA))
        if r is None or not (r['ordered'] and r['decoupled_ok']):
            continue
        split_rows.append({'key': k, 'MGUT': r['MGUT'], 'tau_p': r['tau_p'],
                           'dlog10': math.log10(r['MGUT'] / d126['MGUT'])})
    p &= gate_T7(resp, split_rows, DELTA)
    # ---- T8：把 R9 判出"没有母表示"的那条闭合道（120）补进同一台分量机器重跑
    rv = reps_view()
    closed = [n for n, _k, c in R.CSPLIT['rows_chiral'] if c > 0]
    declared = list(R.CSPLIT['decl_union'])
    gap = {'closed': closed, 'declared': declared,
           'slot120': R.CSPLIT['slotof'].get('120'),
           'missing': [n for n in closed if n not in declared]}
    names4 = [x[0] for x in SCALARS] + [REP120]
    sp4 = spec_full(names4)
    four = solve_th(sp4)
    k120 = (REP120, PHI_LR, '1/2')
    split4 = solve_th(spec_full(names4, [k120]))
    resp4 = response(sp4, four['x'])
    r120 = solve_th(moved(sp4, k120, DELTA))
    el = {'resp': resp4, 'dlog10': math.log10(r120['MGUT'] / four['MGUT'])}
    p &= gate_T8(rv, gap, d126, four, split4, el, DELTA)
    t8 = {'gap': gap, 'three': d126, 'four': four, 'split': split4, 'resp': resp4,
          'move': r120, 'rec3': rec3_of(REP120), 'lm': label_mult(REP120)}
    write_report(RESULTS, base, full, d126, resp, split_rows, empty, allat, t8)
    with open(ROOT / 'SO10阈值报告.json', 'w', encoding='utf-8') as fh:
        json.dump({'gates': RESULTS,
                   'n_pass': sum(1 for r in RESULTS if r['status'] == 'PASS'),
                   'all_pass': all(r['status'] == 'PASS' for r in RESULTS),
                   'chain_probe': D0,
                   'base': {k: v for k, v in base.items() if k != 'x'},
                   'full_10_45': {k: v for k, v in full.items() if k != 'x'},
                   'full_with_126': {k: v for k, v in d126.items() if k != 'x'},
                   't6': {'no_scalar': {k: v for k, v in empty.items() if k != 'x'},
                          'all_at_tB': {k: v for k, v in allat.items() if k != 'x'},
                          'rec3_per_rep': {nm: [str(x) for x in TOTS[nm]] for nm in TOTS}},
                   'pieces': {nm: [{kk: (str(vv) if isinstance(vv, F) else
                                         ('<ws>' if kk == 'ws' else vv))
                                    for kk, vv in pc.items()} for pc in PIECES[nm]]
                              for nm in PIECES},
                   'response': resp, 'split': split_rows,
                   't8': dict(t8, three={k: v for k, v in t8['three'].items() if k != 'x'},
                              four={k: v for k, v in t8['four'].items() if k != 'x'},
                              split={k: v for k, v in t8['split'].items() if k != 'x'},
                              move={k: v for k, v in t8['move'].items() if k != 'x'})},
                  fh, ensure_ascii=False, indent=1, default=str)
    n_pass = sum(1 for r in RESULTS if r['status'] == 'PASS')
    print('[so10_thresholds] %d gates, PASS=%d' % (len(RESULTS), n_pass))
    for r in RESULTS:
        if r['status'] != 'PASS':
            print('  FAIL %s | %s | computed=%s expected=%s' %
                  (r['id'], str(r['claim'])[:70], r['computed'], r['expected']))
    print('  base MGUT=%.4e MB=%.4e AG=%.4f tau=%.3e' %
          (base['MGUT'], base['MB'], base['AG'], base['tau_p']))
    print('  +126 MGUT=%.4e MB=%.4e AG=%.4f tau=%.3e' %
          (d126['MGUT'], d126['MB'], d126['AG'], d126['tau_p']))
    print('  +120 MGUT=%.4e MB=%.4e AG=%.4f tau=%s%s' %
          (four['MGUT'], four['MB'], four['AG'],
           '—' if not four['ordered'] else '%.3e' % four['tau_p'],
           '' if four['ordered'] else '  ($\\alpha_{\\rm GUT}^{-1}<0$ ⇒ 出分支)'))
    return n_pass == len(RESULTS)


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
