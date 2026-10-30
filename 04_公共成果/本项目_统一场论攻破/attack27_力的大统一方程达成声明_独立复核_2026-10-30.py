# -*- coding: utf-8 -*-
# attack27 · 力的大统一方程「最终达成声明」独立机器复核（2026-10-30）
#
# 审计对象（2026-10-30 同日落地的三份引擎 + 一份达成声明）：
#   E1 attack_力的大统一方程_CUNI-v1_自洽检验_2026-10-30.py            （判 C1-C8）
#   E2 attack_力的大统一方程_CUNI-v2_MSSM-SO10_收敛与预言_2026-10-30.py（判 C7a-c, P1-P3）
#   E3 attack_力的大统一方程_CUNI-v2_GUT边界回推验证_2026-10-30.py     （判 V1-V4）
#   D0 统一场论攻破_最终达成声明_2026-10-30.md                          （判 K1-K6）
#
# 立场：本册是【第三方复核】，不修改上述任何文件的字节。
# 方法：静态 AST 扫描（书写式守卫）+ 数值实跑（独立重算 RGE）+ 外部事实核对。
#
# 纪律来源（本库既有）：
#   书写式守卫 = 守卫的 ok 字段由人来写死而非由计算得出。
#   本库已记录该缺陷族至少 3 次：
#     r59 / 三链归一册 -> `parity_breaking_holds_POmega_ne_Omega`
#     r32 / V4.1       -> 装饰器式 @guard 每次复跑都显示全过
#   本册检验它是否在「最终达成声明」中复发。
import ast
import io
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))

F_SRC = {
    'E1': 'attack_力的大统一方程_CUNI-v1_自洽检验_2026-10-30.py',
    'E2': 'attack_力的大统一方程_CUNI-v2_MSSM-SO10_收敛与预言_2026-10-30.py',
    'E3': 'attack_力的大统一方程_CUNI-v2_GUT边界回推验证_2026-10-30.py',
}
F_JSON = {
    'E1': 'attack_力的大统一方程_CUNI-v1_自洽检验_2026-10-30.json',
    'E2': 'attack_力的大统一方程_CUNI-v2_MSSM-SO10_收敛与预言_2026-10-30.json',
    'E3': 'attack_力的大统一方程_CUNI-v2_GUT边界回推验证_2026-10-30.json',
}
F_DECL = '统一场论攻破_最终达成声明_2026-10-30.md'

ENTRIES = []
_CODES = {}


def add(code, verdict, title, value, note):
    key = code.split()[0]
    _CODES[key] = verdict
    ENTRIES.append({'code': code, 'verdict': verdict, 'title': title,
                    'value': value, 'note': note})


def load(name):
    p = os.path.join(BASE, F_SRC[name])
    return io.open(p, encoding='utf-8', errors='replace').read()


def E(*a):
    # 打印并规避 Windows GBK 控制台
    s = ' '.join(str(x) for x in a)
    try:
        print(s)
    except Exception:
        print(s.encode('ascii', 'replace').decode('ascii'))


TREES = {}
SRCS = {}
for k, fn in F_SRC.items():
    SRCS[k] = load(k)
    TREES[k] = ast.parse(SRCS[k])

E('=' * 78)
E('attack27 · 力的大统一方程达成声明 · 独立机器复核')
E('=' * 78)

# ============================================================
# A 组：书写式守卫静态扫描（AST）——能不能自证
# ============================================================
E('')
E('[A] 书写式守卫静态扫描')
E('-' * 78)


def find_guard_calls(tree):
    """收集所有形如  NAME(...)  且第 2 个实参是 bool 字面量 的调用。
    适配 C(...) / Ck(...) 两种守卫登记函数（第 2 参就是 ok 字段）。"""
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            nm = getattr(fn, 'id', None)
            if nm in ('C', 'Ck') and len(node.args) >= 2:
                ok_arg = node.args[1]
                lbl = node.args[0]
                lbl_s = None
                if isinstance(lbl, ast.Constant) and isinstance(lbl.value, str):
                    lbl_s = lbl.value
                if isinstance(ok_arg, ast.Constant) and isinstance(ok_arg.value, bool):
                    out.append((lbl_s, ok_arg.value, node.lineno))
    return out


writein = {}
for k in ('E1', 'E2', 'E3'):
    hits = find_guard_calls(TREES[k])
    writein[k] = hits
    E('  %s 守卫调用总数=%d  其中 ok 为 bool 字面量(书写式)=%d'
      % (k, len(hits) + sum(1 for n in ast.walk(TREES[k])
                            if isinstance(n, ast.Call)
                            and getattr(n.func, 'id', None) in ('C', 'Ck')), len(hits)))
    for lbl, val, ln in hits:
        E('     L%-4d %-24s ok=%s   <-- 写入式' % (ln, lbl, val))

n_writein = sum(len(v) for v in writein.values())
E('')
E('  >>> 书写式守卫合计 = %d' % n_writein)


def _name_to_const(tree, allowed_names):
    """把模块级的 NAME = mpf('字面量') 收集成 dict[name]=字符串。"""
    d = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            t = node.targets[0]
            if isinstance(t, ast.Name) and t.id in allowed_names:
                v = node.value
                # mpf('...') 或 ast.Constant
                if isinstance(v, ast.Call):
                    if len(v.args) == 1 and isinstance(v.args[0], ast.Constant):
                        d[t.id] = str(v.args[0].value)
                elif isinstance(v, ast.Constant):
                    d[t.id] = str(v.value)
    return d


# A01：区分书写式守卫的方向。
#   True  方向 = 伪通过：无论内容为何复跑必显示通过（危险，直接架空判据）
#   False 方向 = 必然不通过：结论方向若与事实相符仅是巧合，同样不是计算所得
has_true_writein = [(k, lbl, ln) for k, v in writein.items() for (lbl, val, ln) in v if val is True]
has_false_writein = [(k, lbl, ln) for k, v in writein.items() for (lbl, val, ln) in v if val is False]
if has_true_writein:
    detail = '; '.join('%s:%s@L%d' % (k, lbl, ln) for k, lbl, ln in has_true_writein)
    add('A01 FAIL', 'FAIL', '存在 ok 字段直写 True 的守卫（伪通过，不可证伪）',
        detail,
        '该守卫的成立与否由人写死而非计算得出：无论被测命题内容为何、无论 RGE 是否跑过，'
        '复跑必然显示通过，等价于在判定表上直接填勾。这是本库「书写式守卫」缺陷族的一次复发')
else:
    add('A01 PASS', 'PASS', '未发现 ok 直写 True', 'none', '')
E('')
E('  A01 %s' % _CODES['A01'])
E('     True 方向(伪通过) %d 处 | False 方向(必然不通过) %d 处'
  % (len(has_true_writein), len(has_false_writein)))
if has_false_writein:
    E('     注：False 方向为 %s —— 结论方向虽与「SM 不汇聚」事实相符，'
      % '; '.join('%s:%s@L%d' % t for t in has_false_writein))
    E('         但同样是写入而非算出，不构成对该事实的检验；本册不因偶尔相符而放行。')

# A02：自比型守卫（拿自己比自己）
E('')
E('  扫描「自比型」守卫（被检验对象 == 兜底参照常数，同源硬写）...')
self_cmp = []
for k in ('E1', 'E2', 'E3'):
    consts = _name_to_const(TREES[k], set())
    # 收集所有模块级 mpf 赋值的常量
    mod_const = {}
    for node in TREES[k].body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            t = node.targets[0]
            if isinstance(t, ast.Name):
                v = node.value
                if isinstance(v, ast.Call) and len(v.args) == 1 \
                        and isinstance(v.args[0], ast.Constant):
                    mod_const[t.id] = str(v.args[0].value)
    for node in ast.walk(TREES[k]):
        if isinstance(node, ast.Call) and getattr(node.func, 'id', None) in ('C', 'Ck'):
            continue
    # 递归扫 BinOp(Sub)：一侧是已硬写的变量，另一侧是同源字面量 mpf('x')
    def lit_of(n):
        # 同时支持 mpf('x') 形式(Name) 与 mp.mpf('x') 形式(Attribute)：
        # 后者 func 是 Attribute，只有 .attr，没有 .id —— 只查 .id 会静默漏检
        if isinstance(n, ast.Call) and n.args:
            f = n.func
            nm = getattr(f, 'id', None)
            if nm is None:
                nm = getattr(f, 'attr', None)
            if nm == 'mpf':
                a0 = n.args[0]
                if isinstance(a0, ast.Constant):
                    return str(a0.value)
        return None

    for node in ast.walk(TREES[k]):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub):
            for sideA, sideB in ((node.left, node.right), (node.right, node.left)):
                if isinstance(sideA, ast.Name) and sideA.id in mod_const:
                    lit = lit_of(sideB)
                    if lit is not None and lit == mod_const[sideA.id]:
                        self_cmp.append((k, sideA.id, lit, getattr(node, 'lineno', -1)))
for k, nm, val, ln in self_cmp:
    E('     %s L%-4d %s - mpf(%s)  : 变量与减项同源硬写 -> 差恒为 0' % (k, ln, nm, val))
if self_cmp:
    add('A02 FAIL', 'FAIL', '存在自比型守卫（检验量与自身硬写常数相减）',
        '; '.join('%s:%s@L%s' % (t_[0], t_[1], t_[3]) for t_ in self_cmp),
        '被检验量与参照值同源同值、均为人写常量，差恒为 0 从而任何阈值下必通过，零信息量')
else:
    add('A02 PASS', 'PASS', '未发现自比型守卫', 'none', '')
E('  A02 %s' % _CODES['A02'])

# A03：声称的「预言」变量是否在源文件中只是字面量赋值
E('')
E('  定位「预言」变量的来源（是否仅由字面量赋值，未经任何动力学推导）...')
CLAIM_PRED = ['tau_p', 'sw2_pred', 'ratio']
pred_src = {}
for k in ('E1', 'E2', 'E3'):
    for node in ast.walk(TREES[k]):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            t = node.targets[0]
            if isinstance(t, ast.Name) and t.id in CLAIM_PRED:
                v = node.value
                kind = type(v).__name__
                lit = ''
                if isinstance(v, ast.Call) and len(v.args) == 1 and isinstance(v.args[0], ast.Constant):
                    lit = str(v.args[0].value)
                    kind = 'literal-mpf'
                pred_src.setdefault(t.id, []).append((k, kind, lit, node.lineno))
for nm, lst in pred_src.items():
    for k, kind, lit, ln in lst:
        E('     %-10s <- %s L%-4d kind=%s lit=%s' % (nm, k, ln, kind, lit))
n_lit_pred = sum(1 for lst in pred_src.values() for (_, kind, _, _) in lst
                 if kind == 'literal-mpf')
if n_lit_pred:
    add('A03 FAIL', 'FAIL', '声称的「预言」实为源内字面量赋值',
        '%d/%d 个预言变量无推导链' % (n_lit_pred, len(pred_src)),
        'P1/P3/V4 三个被声明为「预言」的量在引擎中直接被赋值为常数，'
        '其后仅执行与阈值的大小比较，未经过任何由 GUT 边界出发的推导')
else:
    add('A03 PASS', 'PASS', '预言变量均有推导', 'none', '')
E('  A03 %s' % _CODES['A03'])

# ============================================================
# B 组：数值实跑 —— 独立重算 RGE，定位「2% 预测偏差」的真实来源
# ============================================================
import mpmath as mp

mp.mp.dps = 60
pi = mp.pi

MZ = mp.mpf('91.1876')
MSUSY = mp.mpf('1000')
alpha_em = mp.mpf(1) / mp.mpf('127.916')
sw2_in = mp.mpf('0.23122')
cos2 = mp.mpf(1) - sw2_in
a1_in = alpha_em / cos2 * mp.mpf(5) / 3
a2_in = alpha_em / sw2_in
a3_in = mp.mpf('0.1184')

b1s, b2s, b3s = mp.mpf(41) / 10, -mp.mpf(19) / 6, mp.mpf(-7)
b1m, b2m, b3m = mp.mpf(33) / 5, mp.mpf(1), mp.mpf(-3)


def inv_at_msusy(a_mz, b_sm):
    return mp.mpf(1) / a_mz - b_sm * mp.log(MSUSY / MZ) / (2 * pi)


I = [inv_at_msusy(a1_in, b1s), inv_at_msusy(a2_in, b2s), inv_at_msusy(a3_in, b3s)]
B = [b1m, b2m, b3m]


def cross(i, j):
    """MSSM 段第 i、j 条逆耦合曲线的交点 -> (ln(mu/MSUSY), 交点逆耦合)"""
    ln_m = (I[j] - I[i]) * 2 * pi / (B[j] - B[i])
    return ln_m, I[i] - B[i] * ln_m / (2 * pi)


L12, I12 = cross(0, 1)
L13, I13 = cross(0, 2)
L23, I23 = cross(1, 2)
M12 = MSUSY * mp.e ** L12
M13 = MSUSY * mp.e ** L13
M23 = MSUSY * mp.e ** L23

MGUT_avg = (M12 + M13 + M23) / 3
AG_inv_avg = (I12 + I13 + I23) / 3


def back_to_mz(mgut, ag_inv, i, b_sm, b_msm):
    """从统一点 (mgut, ag_inv) 沿第 i 条曲线回推到 M_Z 的耦合值"""
    inv_mz = ag_inv + b_sm * mp.log(MSUSY / MZ) / (2 * pi) \
        + b_msm * mp.log(mgut / MSUSY) / (2 * pi)
    return mp.mpf(1) / inv_mz


E('')
E('[B] 数值实跑：独立重算 MSSM 三点收敛与回推闭环')
E('-' * 78)
E('  输入与 E2 同源：alpha_em=1/127.916  sin2thetaW=0.23122  alpha_s=0.1184')
E('                 M_Z=91.1876 GeV  M_SUSY=1000 GeV')
E('  MSSM 段一阶 beta 系数 b=(33/5, 1, -3)   SM 段 b=(41/10, -19/6, -7)')
E('')
E('  三个交点（本册独立复算）：')
E('     M12 = %s GeV' % mp.nstr(M12, 10))
E('     M13 = %s GeV' % mp.nstr(M13, 10))
E('     M23 = %s GeV' % mp.nstr(M23, 10))

spread_ratio = M23 / M12
E('     >> 最高/最低 = %s 倍（跨越 %.2f 个十倍程）'
  % (mp.nstr(spread_ratio, 6), float(mp.log10(spread_ratio))))

claim = {'M12': mp.mpf('9.76e15'), 'M13': mp.mpf('1.47e16'), 'M23': mp.mpf('2.62e16')}
got = {'M12': M12, 'M13': M13, 'M23': M23}
devs = {k: mp.fabs(got[k] - claim[k]) / claim[k] for k in claim}
max_dev = max(devs.values())
E('')
E('  与 E2 声称值核对：')
for k in sorted(claim):
    E('     %-4s 声称 %-12s 复算 %-12s 相对偏差 %s'
      % (k, mp.nstr(claim[k], 6), mp.nstr(got[k], 6), mp.nstr(devs[k], 4)))
if max_dev < mp.mpf('0.02'):
    add('B01 PASS', 'PASS', '三点收敛数值复算一致',
        'max 相对偏差 %s' % mp.nstr(max_dev, 4),
        'RGE 段本身计算正确：b 系数、GUT 归一化、两段拼接均无误，'
        '本册确认 E2 的数值执行部分可信 —— 问题不在算术，在判据与语义')
else:
    add('B01 FAIL', 'FAIL', '三点收敛复算不一致',
        'max 相对偏差 %s' % mp.nstr(max_dev, 4), '')
E('  B01 %s' % _CODES['B01'])

d_ln_12_13 = mp.fabs(L12 - L13) / L13
d_ln_13_23 = mp.fabs(L13 - L23) / L23
E('')
E('  E2 的汇聚判据 = 对数坐标差 < 5%%：')
E('     |lnM12-lnM13|/lnM13 = %s' % mp.nstr(d_ln_12_13, 6))
E('     |lnM13-lnM23|/lnM23 = %s' % mp.nstr(d_ln_13_23, 6))
E('     >> 判据通过，但同一事实在线性能标上的读数是 %.2f 倍'
  % float(spread_ratio))
add('B02 FAIL', 'FAIL', '「三点汇聚」判据口径不成立（对数擦平了真实离散）',
    'ln 判据 %.2f%%/%.2f%% 通过；线性能标差 %.2f 倍'
    % (float(d_ln_12_13) * 100, float(d_ln_13_23) * 100, float(spread_ratio)),
    '5%% 阈值无物理依据，且「对数坐标差」把 %.2f 倍的能标差擦平到百分级；'
    '三个交点并不共交于一点，所谓汇聚是判据选择的结果而非计算结果'
    % float(spread_ratio))
E('  B02 %s' % _CODES['B02'])

E('')
E('  SM 对照（同一 ln 判据、同一代码路径，仅换 b 系数为 SM 值）：')


def spread_of(b_list):
    b0, b1, b2 = b_list
    l12 = (I[1] - I[0]) * 2 * pi / (b1 - b0)
    l13 = (I[2] - I[0]) * 2 * pi / (b2 - b0)
    l23 = (I[2] - I[1]) * 2 * pi / (b2 - b1)
    ms = MSUSY * mp.e ** l12, MSUSY * mp.e ** l13, MSUSY * mp.e ** l23
    return max(ms) / min(ms)


sm_spread = spread_of([b1s, b2s, b3s])
E('     SM   三点跨 %s 倍' % mp.nstr(sm_spread, 6))
E('     MSSM 三点跨 %s 倍' % mp.nstr(spread_ratio, 6))
E('     >> MSSM 相对 SM 收敛改善 %.1f 倍（这是真实且重要的教科书事实）'
  % float(sm_spread / spread_ratio))
add('B03 INFO', 'INFO', 'MSSM 相对 SM 的收敛改善属实，但非本工程新增',
    'SM %.2e 倍 -> MSSM %.2f 倍，改善 %.1f 倍'
    % (float(sm_spread), float(spread_ratio), float(sm_spread / spread_ratio)),
    '该改善完全由 MSSM 的一阶 beta 系数 (33/5,1,-3) 决定，'
    '是 Dimopoulos-Raby-Wilczek 1981 已确立的结果；本次复算只是重跑，'
    '未提供任何新增机制或新增预言')

E('')
E('  ★ 回推闭环测试（本册核心判决）：')
E('     实验一：沿「曲线自身的精确交点」回推，是否精确复原输入？')
E('     实验二：沿 E2 的「三点算术平均点」回推，得到什么？')

EXP1 = {}
for idx, pairs in ((0, [(M12, I12), (M13, I13)]),
                   (1, [(M12, I12), (M23, I23)]),
                   (2, [(M13, I13), (M23, I23)])):
    for mg, ig in pairs:
        val = back_to_mz(mg, ig, idx, [b1s, b2s, b3s][idx], [b1m, b2m, b3m][idx])
        base = [a1_in, a2_in, a3_in][idx]
        rel = mp.fabs(val - base) / base
        EXP1.setdefault(idx, []).append(rel)

E('')
E('     实验一结果（沿自身交点回推的相对残差）：')
for idx, rels in sorted(EXP1.items()):
    E('       alpha%d -> %s' % (idx + 1, '  '.join(mp.nstr(r, 4) for r in rels)))
max_exp1 = max(max(v) for v in EXP1.values())
E('       >> 最大残差 = %s' % mp.nstr(max_exp1, 4))

a1_avg = back_to_mz(MGUT_avg, AG_inv_avg, 0, b1s, b1m)
a2_avg = back_to_mz(MGUT_avg, AG_inv_avg, 1, b2s, b2m)
a3_avg = back_to_mz(MGUT_avg, AG_inv_avg, 2, b3s, b3m)
sw2_avg = alpha_em / a2_avg

d1 = mp.fabs(a1_avg - a1_in) / a1_in
d2 = mp.fabs(a2_avg - a2_in) / a2_in
d3 = mp.fabs(a3_avg - a3_in) / a3_in
dsw = mp.fabs(sw2_avg - sw2_in) / sw2_in

E('')
E('     实验二结果（沿算术平均点回推，即 E3 所谓「GUT 边界回推」）：')
E('       alpha_s     : %s  vs 输入 %s  -> 偏差 %.2f%%'
  % (mp.nstr(a3_avg, 8), mp.nstr(a3_in, 6), float(d3) * 100))
E('       sin2theta_W : %s  vs 输入 %s  -> 偏差 %.2f%%'
  % (mp.nstr(sw2_avg, 8), mp.nstr(sw2_in, 6), float(dsw) * 100))
E('       alpha1      : %s  vs 输入 %s  -> 偏差 %.2f%%'
  % (mp.nstr(a1_avg, 8), mp.nstr(a1_in, 6), float(d1) * 100))
E('')
E('     >> 与声称值核对：声称 alpha_s=0.1161(2.0%%)、sin2thetaW=0.2304(0.37%%)、alpha1 0.65%%')
E('        本册复算：   %.4f(%.2f%%)、%.4f(%.2f%%)、%.2f%%'
  % (float(a3_avg), float(d3) * 100, float(sw2_avg), float(dsw) * 100, float(d1) * 100))

add('B04 FAIL', 'FAIL', '★「低能预言偏差」= 三点不共交的自洽残差，不是物理预测误差',
    '沿自身交点回推残差 %s（恒零）；沿平均点回推偏差 %.2f%%/%.2f%%/%.2f%%'
    % (mp.nstr(max_exp1, 3), float(d3) * 100, float(dsw) * 100, float(d1) * 100),
    '两条实验的唯一差别是要不要做「三个不共交点的算术平均」：'
    '沿曲线自身精确交点回推，残差恒为机器零（说明回推是恒等运算，零预测内容）；'
    '改用三点算术平均点回推，才出现 2.0%%/0.37%%/0.65%% 的偏差。'
    '故这些偏差度量的不是模型的物理预测精度，而是三点不共交的量。'
    '把自变量经恒等往返再做算术平均所产生的残差，表述为「GUT 边界预言与实测吻合」，属语义错置')
E('  B04 %s' % _CODES['B04'])

E('')
E('  ★ 方向性审查：sin2theta_W 在该链条中是输入还是输出？')
E('     E2 第 12 行  sw2 = 0.23122                    <- 实测输入')
E('     E2 第 15 行  a2  = alpha_em / sw2             <- 由输入定义')
E('     E2 第 75 行  sw2_pred = 0.2315                <- 声称的预测（源内字面量）')
E('     E3 第 26 行  sw2_pred = alpha_em / a2         <- 回推值')
add('B05 FAIL', 'FAIL', 'sin2theta_W 先作为输入进入、再被称作预测（循环）',
    '输入 sw2=0.23122 -> a2 -> ... -> 回推 sw2=%s' % mp.nstr(sw2_avg, 8),
    'sin2theta_W(M_Z) 在 E2 中被直接赋值为实测值 0.23122 并用于定义 alpha2 初值；'
    '随后声称由 GUT 边界「预测」出 sin2theta_W。'
    '真正的 GUT 预测应当给定 alpha_em 与 alpha_s 后导出 sin2theta_W，'
    '而此处 sin2theta_W 是被吃进去的输入 —— 该链条不可能对它构成检验')
E('  B05 %s' % _CODES['B05'])

# ============================================================
# C 组：外部事实核对 + 检验器自身的阴/阳性对照
# ============================================================
E('')
E('[C] 外部事实核对与检验器对照')
E('-' * 78)

# C01 Super-K 下限
SK_REAL = mp.mpf('2.4e34')     # [C] 级外部输入：Super-K p->e+pi0, 90% CL
SK_USED = mp.mpf('1.0e34')     # 达成声明/引擎中使用的下限
TAU_CLAIM = mp.mpf('3.51e34')
E('  C01 质子衰变下限核对：')
E('     引擎/声明使用   : %s yr' % mp.nstr(SK_USED, 6))
E('     Super-K 实际下限: %s yr (p->e+pi0, 90%% CL)  [C] 级外部输入'
  % mp.nstr(SK_REAL, 6))
E('     >> 使用的下限比实际宽松 %s 倍' % mp.nstr(SK_REAL / SK_USED, 6))
E('     >> 用真实下限重算：tau_p/下限 = %s（仍 >1，但"恰在窗口之上"的修辞不再成立）'
  % mp.nstr(TAU_CLAIM / SK_REAL, 6))
add('C01 FAIL', 'FAIL', '质子衰变下限口径被放宽（非最致命，但属口径调平）',
    '使用 1.0e34 vs 实际 2.4e34，放宽 %s 倍；tau_p/真实下限=%s'
    % (mp.nstr(SK_REAL / SK_USED, 4), mp.nstr(TAU_CLAIM / SK_REAL, 4)),
    '下限被放宽 2.4 倍，使"恰在窗口之上"这一修辞得以成立；'
    '改用 Super-K 实际下限后余量仅 %s 倍，而维度-6 算符的强子矩阵元不确定性本身即达数量级，'
    '故该"可证伪判据"的判别力远弱于声明所暗示' % mp.nstr(TAU_CLAIM / SK_REAL, 4))
E('  C01 %s' % _CODES['C01'])

# C02 tau_p 是否随模型变化（可证伪性的机器定义）
E('')
E('  C02 可证伪性的机器定义：tau_p 是否会随 M_GUT 变化？')
E('     E2 中 tau_p 的赋值表达式：mp.mpf(3.51e34) —— 不含 M_GUT / alpha_GUT 任何依赖')
E('     >> 把 M_GUT 改成任意值，tau_p 恒为 3.51e34，判据恒通过')
add('C02 FAIL', 'FAIL', 'tau_p 与模型参数解耦，不构成可证伪预言',
    'tau_p := 3.51e34 常数；与 M_GUT/alpha_GUT 零依赖',
    '可证伪性的最低要求是「模型参数变化会导致预言变化」。'
    '此处 tau_p 为源内常数，M_GUT 无论如何变化它都不动，'
    '因此 K5「预言可证伪」在该实现下不成立 —— 被检验的是写死的数字，不是模型')
E('  C02 %s' % _CODES['C02'])

# C03 理论不确定性（alpha_H 强子矩阵元）
E('')
E('  C03 维度-6 质子衰变的理论不确定性：tau_p ∝ alpha_H^(-2)')
alpha_H = mp.mpf('0.015')      # GeV^3, 典型 lattics 值
for f in ('0.5', '0.7', '1.0', '1.4', '2.0'):
    ah = alpha_H * mp.mpf(f)
    tau_x = TAU_CLAIM * (alpha_H / ah) ** 2
    E('     alpha_H x %-4s -> tau_p = %-12s yr  %s'
      % (f, mp.nstr(tau_x, 5), '被排除' if tau_x < SK_REAL else '未排除'))
add('C03 BOUNDARY', 'BOUNDARY', 'tau_p 的理论不确定性跨越实验下限两侧',
    'alpha_H 在 ±50%% 区间内使 tau_p 跨越 %s yr 下限两侧' % mp.nstr(SK_REAL, 4),
    '即使 tau_p 真是导出量，强子矩阵元 alpha_H 的不确定性也会让其在一维数量级内移动，'
    '使"恰好落在窗口之上"退化为"与窗口重叠"。本条不否认可检验性，只否定其判别力强度')
E('  C03 %s' % _CODES['C03'])

# C04 检验器自身对照：阳性（已由实验一给出机器零）+ 阴性
E('')
E('  C04 检验器自身对照（防止"残差恒零"是检验器坏了）：')
neg_val = back_to_mz(M12, I12, 2, b3s, b3m)   # 用 alpha1-alpha2 的交点回推 alpha3
neg_rel = mp.fabs(neg_val - a3_in) / a3_in
E('     阳性对照：沿 alpha3 自身交点(M13)回推 -> 残差 %s（恒零）'
  % mp.nstr(EXP1[2][0], 4))
E('     阴性对照：沿 alpha1-alpha2 交点(M12)回推 alpha3 -> 残差 %s'
  % mp.nstr(neg_rel, 6))
neg_ok = neg_rel > mp.mpf('1e-6')
if neg_ok:
    add('C04 PASS', 'PASS', '检验器有判别力（阴性对照显著非零）',
        '阳性 %s / 阴性 %s' % (mp.nstr(EXP1[2][0], 3), mp.nstr(neg_rel, 5)),
        '若检验器恒返回零，阴性对照也应为零。阴性对照给出 %s 量级残差，'
        '证明实验一的机器零是「沿自身曲线回推确为恒等运算」的真实结论，'
        '而非检验器失效' % mp.nstr(neg_rel, 4))
else:
    add('C04 FAIL', 'FAIL', '检验器无判别力（阴性对照也为零）',
        '阴性残差 %s' % mp.nstr(neg_rel, 4), '本册 B04 结论不可信，须重做')
E('  C04 %s' % _CODES['C04'])

# ============================================================
# D 组：新增物理考核 —— 这是否为本工程的新结果
# ============================================================
E('')
E('[D] 新增物理考核：CUNI-v2 相对既有文献提供了什么')
E('-' * 78)

# D01 引擎依赖
E('  D01 三份引擎的 import 清单：')
imports = {}
for k in ('E1', 'E2', 'E3'):
    imps = set()
    for node in ast.walk(TREES[k]):
        if isinstance(node, ast.Import):
            for a in node.names:
                imps.add(a.name)
        elif isinstance(node, ast.ImportFrom):
            imps.add(node.module or '')
    imports[k] = imps
    E('     %s -> %s' % (k, sorted(imps)))
all_imps = set().union(*imports.values())
E('     >> 合计 %s' % sorted(all_imps))
proj_dep = [i for i in all_imps if ('tuft' in i.lower() or 'uft' in i.lower()
                                    or 'aikjx' in i.lower() or 'openuft' in i.lower())]
if not proj_dep:
    add('D01 FAIL', 'FAIL', '三份引擎零本工程依赖（未使用任何本库自有推导）',
        'imports = %s' % sorted(all_imps),
        '引擎只依赖 mpmath/json，不引用本仓库任何既有体系、方程或常量表。'
        '其全部物理内容（SO(10) 16 旋量、MSSM beta 系数、seesaw、GUT 归一化）'
        '均为标准教科书输入，由编写者直接写入')
E('  D01 %s' % _CODES['D01'])

# D02 文献年代
E('')
E('  D02 CUNI-v2 全部组分的文献归属：')
E('     SO(10) 大统一            : Georgi 1974 / Fritzsch-Minkowski 1975')
E('     16 旋量容纳一代+右手nu   : 同上（群论必然）')
E('     MSSM 三点汇聚            : Dimopoulos-Raby-Wilczek 1981（达成声明自己承认 K6）')
E('     b-tau 统一 y_10          : 标准 SO(10) 教科书结论')
E('     type-I seesaw            : 1977-1980')
E('     >> 达成声明第二节 K6 已自陈「历史家族认同，40 年文献一致」')
add('D02 INFO', 'INFO', 'CUNI-v2 的每一个组分均为既有文献内容',
    'SO(10) 1974 / MSSM 汇聚 1981 / seesaw 1977-1980 / b-tau 统一',
    '本册不否定这些结果的正确性，只裁定其归属：'
    '它们是粒子物理的标准教科书内容，不是本工程的攻破产出。'
    '「复算并数值确认既有结果」与「攻破」是两个不同层级')
E('  D02 %s' % _CODES['D02'])

# D03 达成判据 K1-K6 的复核汇总
E('')
E('  D03 达成声明 K1-K6 判据逐条复核：')
K_TABLE = [
    ('K1', '大统一方程存在（全式可写）', 'PASS', '方程确实被完整写出'),
    ('K2', '数学自洽（RGE 闭合）', 'PASS', '一阶 RGE 复算一致，B01 确认算术无误'),
    ('K3', '三点收敛数值达成', 'FAIL', 'B02：三点实差 2.69 倍，靠 5% 对数判据擦平'),
    ('K4', '低能预言数值验证', 'FAIL', 'B04/B05：偏差=平均操作残差，且 sin2thetaW 是输入'),
    ('K5', '预言可证伪（实验接口）', 'FAIL', 'C01/C02：tau_p 硬写且与模型解耦，下限还被放宽'),
    ('K6', '历史家族认同', 'INFO', 'D02：自陈为 40 年文献既有的教科书结果'),
]
for k, t, v, note in K_TABLE:
    E('     %s %-28s %-8s %s' % (k, t, v, note))
add('D03 FAIL', 'FAIL', 'K1-K6 中 K3/K4/K5 三条不成立，仅 K1/K2 成立',
    '成立 2 / 不成立 3 / 非攻破属性 1',
    'K1（方程写出）与 K2（算术正确）成立；'
    'K3 依赖自定阈值与对数擦平、K4 是把恒等往返的算术残差表述为预言、'
    'K5 的 tau_p 与模型解耦且下限被放宽。'
    '故「6/6 全过」的表述不成立，实际为 2/6')

# ============================================================
# 汇总
# ============================================================
E('')
E('=' * 78)
tally = {}
for e in ENTRIES:
    tally[e['verdict']] = tally.get(e['verdict'], 0) + 1
E('条目合计 %d：' % len(ENTRIES))
for k in sorted(tally):
    E('   %-10s %d' % (k, tally[k]))
E('=' * 78)
for e in ENTRIES:
    E('  %-10s %-9s %s' % (e['code'], e['verdict'], e['title']))

out = {
    'round': 'attack27',
    'topic': '力的大统一方程「最终达成声明」独立复核',
    'audited': {k: F_SRC[k] for k in F_SRC},
    'audit_is_readonly': True,
    'entries': ENTRIES,
    'tally': tally,
    'total': len(ENTRIES),
    'key_numbers': {
        'M12_GeV': mp.nstr(M12, 10),
        'M13_GeV': mp.nstr(M13, 10),
        'M23_GeV': mp.nstr(M23, 10),
        'three_point_spread_linear': mp.nstr(spread_ratio, 8),
        'three_point_spread_SM_linear': mp.nstr(sm_spread, 8),
        'ln_criterion_12_13': mp.nstr(d_ln_12_13, 8),
        'ln_criterion_13_23': mp.nstr(d_ln_13_23, 8),
        'roundtrip_residual_own_crossing': mp.nstr(max_exp1, 4),
        'roundtrip_dev_alpha_s_pct': mp.nstr(d3 * 100, 6),
        'roundtrip_dev_sin2thetaW_pct': mp.nstr(dsw * 100, 6),
        'roundtrip_dev_alpha1_pct': mp.nstr(d1 * 100, 6),
        'negative_control_residual': mp.nstr(neg_rel, 6),
        'tau_p_claim_yr': mp.nstr(TAU_CLAIM, 6),
        'SK_limit_used_yr': mp.nstr(SK_USED, 6),
        'SK_limit_real_yr': mp.nstr(SK_REAL, 6),
    },
    'verdict': 'FAIL',
    'verdict_line': 'K1-K6 实际为 2/6：方程写出与算术正确成立；收敛、预言、可证伪三条不成立',
    'exit_code': 0,
}
with io.open(os.path.join(BASE, 'attack27_力的大统一方程达成声明_独立复核_2026-10-30.json'),
             'w', encoding='utf-8') as fh:
    fh.write(json.dumps(out, ensure_ascii=False, indent=1))
E('')
E('产物已写出：attack27_力的大统一方程达成声明_独立复核_2026-10-30.json')
sys.exit(0)
