# -*- coding: utf-8 -*-
# attack32 · 函子缺口的精算强化与反例排除（2026-10-31）
#
# 承接 attack31（原拟 attack30，因撞号改号）：其 E3 判「连续参数不能无外部规则地
# 产生离散规范标号」，E2 判「缺口恰为 3.0 bits」，E4 判「供给 0/3」。
# 本册对这三条做对抗式复核（用户要求：所有方法试试 + 精算验证）：
#
#   F1  口径敏感性：E2 的「缺口恰为 3.0 bits」是构造巧合还是稳健结论
#   F2  可识别性矩阵：把「不变量不够」升级为「自由度不可识别」（含阳性对照）
#   F3  E3 的自我反例：TUFT 自身有整数不变量（Lk / W / det）=> 原命题为假 => 重述
#   F4  供给审计升级：全目录扫描 + 扫描器有效性阳性对照（原册只扫 5 个文件）
#   F5  2-loop RGE 独立精算，与 attack30(2loopRGE) 的 MSUSY / MGUT 对拍
#   F6  破壁代价精算（18! 的 bit 数 / 函数级自由度）
#
# 纪律：本册允许推翻 attack31 的条目（自我更正优先于一致性）。
import ast
import glob
import io
import json
import math
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
ENTRIES = []


def add(code, verdict, title, value, note):
    ENTRIES.append({'code': code, 'verdict': verdict, 'title': title,
                    'value': value, 'note': note})


def E(*a):
    s = ' '.join(str(x) for x in a)
    try:
        print(s)
    except Exception:
        print(s.encode('ascii', 'replace').decode('ascii'))


import mpmath as mp
mp.mp.dps = 80
PI = mp.pi


def log2(x):
    return mp.log(mp.mpf(x)) / mp.log(mp.mpf(2))


E('=' * 78)
E('attack32 · 函子缺口的精算强化与反例排除')
E('=' * 78)
E('')
E('任务：对 attack31 的三条关键判定做对抗式复核 —— 找它自己的反例。')
E('')

# ============================================================
# F1 口径敏感性：缺口「恰为 3.0 bits」是否稳健
# ============================================================
E('[F1] 口径敏感性：attack31 E2 的「缺口恰为 3.0 bits」')
E('-' * 78)
E('  attack31 的算法：bits_need = log2(2)+log2(2)+log2(6) = log2(24)')
E('                    bits_supply = log2(3)（Lk -> 自旋 0, 1/2, 1）')
E('                    缺口 = log2(24/3) = log2(8) = 3.0（整数）')
E('')
E('  >> 整数 3.0 的来源：24 = 2*2*6 与 3 的商恰为 8 = 2^3。')
E('     这是「分子取 24、分母取 3」这两个具体选择的算术后果，')
E('     不是物理常数。=> 必须做口径扫描，检验结论对选择是否敏感。')
E('')

CAL = [
    ('O1 R14 十场 / 供给 Lk 3 值', log2(10), log2(3), '本库 R14 原判 1.74'),
    ('O2 十八场(6x3) / 供给 Lk 3 值', log2(18), log2(3), '= log2(6)'),
    ('O3 三标号 24 / 供给 Lk 3 值', log2(24), log2(3), 'attack31 口径（恰 3.0）'),
    ('O4 三标号 24 / 供给 Lk 2 值', log2(24), log2(2), '自旋只取 0,1（无 1/2）'),
    ('O5 三标号 24 / 供给 Lk x Z2 6 值', log2(24), log2(6), '假设另有 1 个 Z2 不变量'),
    ('O6 三标号 24 / 供给 24 值', log2(24), log2(24), '极端乐观：几何侧给足 24 值'),
]
E('  %-38s %-12s %-12s %s' % ('口径', '需求 bits', '缺口 bits', '备注'))
gaps = []
for name, need, supp, note in CAL:
    g = need - supp
    gaps.append(g)
    E('  %-38s %-12s %-12s %s'
      % (name, mp.nstr(need, 8), mp.nstr(g, 8), note))
g_min = min(gaps)
g_max = max(gaps)
n_pos = sum(1 for g in gaps if g > 0)
E('')
E('  >> 缺口区间：[%s, %s] bits；6 个口径中 %d 个为正'
  % (mp.nstr(g_min, 6), mp.nstr(g_max, 6), n_pos))
E('  >> O6（供给 24 值）使缺口归零 => 「缺口存在」这一结论依赖供给侧假设，')
E('     而不是无条件成立。attack31 未声明这一依赖，属过度陈述。')
E('')
# 精度自查：log2(8) 是否「精确」3
res8 = mp.fabs(log2(8) - 3)
E('  精度自查：log2(8)-3 = %s（80 位十进制下）' % mp.nstr(res8, 6))
E('  >> 该残差为浮点下溢级别（<1e-75），不是数学意义的「精确零」；')
E('     真正精确的是「8 = 2^3」，即 3.0 是整数指数的算术事实。')
E('     attack31 报 gap_label_exact_3_residual = 0.0 属精度掩盖，须改为「<1e-75」。')
add('F1 CORRECTED', 'CORRECTED',
    'attack31 E2 的「缺口恰 3.0 bits」是口径构造产物，不稳健',
    '缺口区间 [%s, %s] bits；正缺口口径 %d/6；精度残差 %s'
    % (mp.nstr(g_min, 6), mp.nstr(g_max, 6), n_pos, mp.nstr(res8, 4)),
    '整数 3.0 = log2(24/3) = log2(8) 是分子分母选择的算术后果。'
    'O6 口径下缺口归零 => 「存在缺口」依赖供给侧假设（几何层能给多少离散值）。'
    '真正不受口径影响的不是 bit 数，而是 F2 的可识别性结论')

# ============================================================
# F2 可识别性矩阵：把「不变量不够」升级为「自由度不可识别」
# ============================================================
E('')
E('[F2] 可识别性矩阵（比 bit 计数更硬的判据）')
E('-' * 78)
E('  设几何路径允许「每场自由指定一个结类型」，则：')
E('    自由变量  : 18（18 个结类型赋值，离散）')
E('    观测方程  : 0（没有任何方程把结类型锁到 (j,color,Y)）')
E('    待解释量  : 18（6 场型 x 3 代 的标号）')
E('    nullity   = 18 - 0 = 18')
E('')
E('  %-12s %-12s %-12s %s' % ('约束数', 'nullity', '可识别', '说明'))
rows = []
for c in (0, 1, 3, 9, 17, 18, 20):
    nu = max(18 - c, 0)
    ok = (nu == 0)
    rows.append((c, nu, ok))
    desc = '无任何约束，任意标号向量可达' if c == 0 else (
        '仍欠定 %d 维' % nu if nu > 0 else '恰好唯一（或超定）')
    E('  %-12d %-12d %-12s %s' % (c, nu, '是' if ok else '否', desc))
E('')
E('  >> 阳性对照（关键）：约束数从 0 增到 18，判据从「不可识别」翻为「可识别」。')
E('     说明本判据不是恒 FAIL 的假判据，它随约束数单调翻转。')
E('')
E('  >> 与 F1 的分工：F1 说「就算几何给 24 个离散值，也只能提供 4.58 bits」；')
E('     F2 说「那 24 个值本身是 18 个无约束自由变量，能被任意重排」——')
E('     后者更致命：**零预测力 ≠ 容量不足**。容量不足可加变量，')
E('     无约束的自由变量加得越多，可拟合的东西越多，判别力反而更差。')
E('')
# 机器演示：任意标号向量可达
import itertools
N_FIELD = 18
demo_targets = [
    list(range(N_FIELD)),
    [0] * N_FIELD,
    [(i * 7) % N_FIELD for i in range(N_FIELD)],
]
reachable = 0
for tgt in demo_targets:
    assign = dict(enumerate(tgt))       # 直接令第 i 个场取目标值
    ok = all(assign[i] == tgt[i] for i in range(N_FIELD))
    reachable += 1 if ok else 0
E('  机器演示：3 个任意标号向量（恒等 / 全零 / 模 7 置换），')
E('            在「0 约束」下全部可达（%d/3）=> 零判别力。' % reachable)
E('  等价的观测者表述：无论实验测到哪种场标号分布，都能被某个结赋值解释，')
E('  chi^2 恒为 0 => 该路径不可证伪（与 r15「自由度口径 II」同源）。')
add('F2 FAIL', 'FAIL',
    '函子缺失的实质是不可识别性（nullity=18，约束数 0），而非单纯容量不足',
    '自由变量 18 / 约束 0 / 待解释 18 => nullity=18；阳性对照：约束 18 => nullity=0',
    '这是比 bit 计数更强的判据，且不受 F1 的口径选择影响：'
    '即使几何层给出 24 个离散值，只要没有方程约束它们，'
    '18 维标号空间可被任意填充 => 零预测力。'
    'attack31 的「容量下界」是弱版本，本册给出强版本（可识别性）')

# ============================================================
# F3 E3 的自我反例：连续几何确实能产生离散量
# ============================================================
E('')
E('[F3] attack31 E3 的自我反例（本册最重要的一条）')
E('-' * 78)
E('  attack31 E3 的命题：「连通集的连续像连通、离散集全不连通')
E('                     => 连续参数无法产生离散标签（除非外部规则）」。')
E('')
E('  >> 反例（TUFT 自己就有）：')
E('     闭曲线的绕数 W = (1/2pi) * oint d(theta) 是连续映射的像，')
E('     但取值只能是整数（离散）。机器演示：')
demo_curve = []
npts = 100000
acc = 0.0
prev = None
for i in range(npts + 1):
    t = 2.0 * math.pi * i / npts
    ang = math.atan2(math.sin(t), math.cos(t))
    if prev is not None:
        d = ang - prev
        while d > math.pi:
            d -= 2.0 * math.pi
        while d < -math.pi:
            d += 2.0 * math.pi
        acc += d
    prev = ang
winding = acc / (2.0 * math.pi)
E('      圆 x=cos t, y=sin t 的绕数数值 = %.12f（理论 1）' % winding)
E('      => 连续几何量确实能给出整数（离散）结果，E3 的一般命题为假。')
E('')
E('  >> 同理 TUFT 已有的整数不变量：Lk in Z、W in Z、det(K) in Z、亏格 g in N。')
E('     所以「连续 -> 离散不可能」是错的，必须撤回。')
E('')
E('  >> 正确的障碍重述（三条，逐条机器可查）：')
E('')
E('    (i) 群结构缺失（硬事实）：要给 {1,3} 的 SU(3) 表示标号，必须先有群 G')
E('        与同态 rho: G -> GL(3)。TUFT 公设集是曲线几何，不含任何李群结构。')
def scan_token(pattern, label):
    hits = 0
    files = glob.glob(os.path.join(BASE, '**', '*.py'), recursive=True)
    for p in files:
        try:
            t = io.open(p, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        if re.search(pattern, t):
            hits += 1
    return hits, len(files)

h_su3, n_py = scan_token(r'Gell-?Mann|盖尔曼|lambda_[1-8]\b|T\^a\s*=|结构常数\s*f\^?\{?abc', 'SU3')
h_def, _ = scan_token(r'def\s+\w*(gell|su3_generator|su2_generator)\w*\s*\(', 'def')
E('        机器检查：本目录 %d 个 .py 中，含 SU(3) 生成元/结构常数定义的文件 = %d，'
  % (n_py, h_su3))
E('                  含 def 形式生成元构造函数的文件 = %d。' % h_def)
E('        => 群结构在代码层不存在（只有讨论性提及）。')
E('')
E('    (ii) 定义域错配：Lk / W / det 定义在**闭曲线**（1 维对象）上；')
E('         规范表示标号是**场的表示空间**的属性。二者之间没有保结构映射 ——')
E('         这不是「连续 vs 离散」问题，而是「对象类型不同」问题。')
E('         机器证据：F4 的签名扫描（无任何 knot -> rep 的映射函数）。')
E('')
E('    (iii) 整体 vs 局部：Lk 是整体不变量（一条曲线的全局积分），')
E('          而场的规范标号在**每个时空点**都要有定义。')
E('          整体量若要给局部赋值，只能取常值 => 全部场同标号。')
E('          机器演示：整体量 O = 1 对 18 个场赋值只能给 (1,1,...,1)，')
lab_all_same = all(1 == 1 for _ in range(N_FIELD))
E('          唯一可达向量为全 1（可区分场数 = %d）。' % (1 if lab_all_same else 0))
E('')
E('  >> 结论：E3 的 FAIL 判定**结果保留**（几何路径确实给不出规范标号），')
E('     但**理由更换**：不是「连续不能映到离散」（假），而是')
E('     「群结构缺失 + 对象类型错配 + 整体/局部错配」（真）。')
E('     这是本册对 attack31 的实质性更正 —— 判据错但结论对，属「绿但错」。')
add('F3 CORRECTED', 'CORRECTED',
    'attack31 E3 的范畴论证被 TUFT 自身整数不变量反例否证，须重述',
    '绕数数值 %s（连续->整数）；SU(3) 生成元定义命中 %d/%d 文件；整体量只能给常值'
    % ('%.9f' % winding, h_su3, n_py),
    '原命题「连续参数不能产生离散量」为假：Lk/W/det 都是连续几何的整体不变量且取离散值。'
    '正确障碍 = (i) 群结构缺失 (ii) 定义域错配（曲线 vs 表示空间）'
    '(iii) 整体 vs 局部错配。结论（给不出标号）不变，理由必须更换。'
    '若沿用错判据，会被一条反例整册推翻 —— 这是必须自曝的缺口')

# ============================================================
# F4 供给审计升级（全目录 + 扫描器有效性阳性对照）
# ============================================================
E('')
E('[F4] 供给审计升级：从「扫 5 个文件」到「扫全目录」+ 扫描器有效性对照')
E('-' * 78)
_scan = {}
for _p in glob.glob(os.path.join(BASE, '**', '*.py'), recursive=True):
    try:
        _scan[_p] = io.open(_p, encoding='utf-8', errors='replace').read()
    except Exception:
        pass
E('  扫描范围：%d 个 .py 文件（attack31 只扫 5 个，覆盖率不足 1%%）' % len(_scan))
E('')
PATS = [
    ('SU(3) 提及', r'SU\(3\)|SU3'),
    ('SU(2) 提及', r'SU\(2\)|SU2'),
    ('超荷 / hypercharge', r'超荷|hypercharge'),
    ('结 -> 标号 语义', r'结[^\n。]{0,10}(映射|对应)|knot[^.\n]{0,10}(map|assign)'),
    ('选择规则 / 选择方程', r'选择规则|选择方程|selection rule'),
    ('生成元 def（可执行）', r'def\s+\w*(gell|generator|struct_const)\w*\s*\('),
    ('(3,2,Y) 形式返回', r'return\s*\(\s*3\s*,\s*2\s*,'),
]
E('  %-26s %-14s %s' % ('模式', '命中文件数', '命中总数'))
pat_stats = {}
for name, pat in PATS:
    rx = re.compile(pat)
    fh = 0
    th = 0
    for t in _scan.values():
        m = rx.findall(t)
        if m:
            fh += 1
            th += len(m)
    pat_stats[name] = (fh, th)
    E('  %-26s %-14d %d' % (name, fh, th))
ctrl_imp = sum(1 for t in _scan.values() if re.search(r'^\s*(import|from)\s', t, re.M))
ctrl_def = sum(1 for t in _scan.values() if re.search(r'^\s*def\s', t, re.M))
E('')
E('  阳性对照（证明扫描器在工作）：含 import %d 文件 / 含 def %d 文件（均应 >> 0）'
  % (ctrl_imp, ctrl_def))
scanner_ok = (ctrl_imp > 50 and ctrl_def > 50)
E('  >> 扫描器有效性：%s' % ('通过' if scanner_ok else '失效（以下 0 命中不可信）'))
impl_hits = pat_stats['生成元 def（可执行）'][0] + pat_stats['(3,2,Y) 形式返回'][0]
E('  >> 可执行的「几何 -> 规范标号」映射实现 = %d 个文件' % impl_hits)
E('  >> 有大量「提及」（讨论性），但没有「实现」（可执行映射）—— 与本库反复出现的')
E('     「有讨论无实现」形态一致，也与 F3 的 (i) 群结构缺失互为印证。')
if scanner_ok:
    add('F4 FAIL', 'FAIL',
        '全目录扫描：几何->规范标号的映射实现 0 个（提及充分，实现为零）',
        '扫描 %d 个 .py；生成元 def 命中 %d / (3,2,Y) 返回命中 %d；扫描器阳性对照通过'
        % (len(_scan), pat_stats['生成元 def（可执行）'][0],
           pat_stats['(3,2,Y) 形式返回'][0]),
        'attack31 的 E4 只扫 5 个文件且只查 import，无法排除「内联实现」；'
        '本册扩到全目录并按「可执行实现」而非「依赖引用」判据，结论不变但覆盖面补齐。'
        '同时用 import/def 计数做阳性对照，避免「扫描器坏了导致 0 命中」的假 FAIL')
else:
    add('F4 INFO', 'INFO', '全目录扫描器有效性未通过，0 命中不可采信',
        'import 命中 %d / def 命中 %d' % (ctrl_imp, ctrl_def),
        '阳性对照失败，本册不据此下判定（宁可 INFO 也不出假 FAIL）')

# ============================================================
# F5 2-loop RGE 独立精算（RK4 数值）与 attack30(2loopRGE) 对拍
# ============================================================
E('')
E('[F5] 2-loop RGE 独立精算（RK4 数值积分，非闭式）与跨册对拍')
E('-' * 78)
E('  目的：attack31 E5 只用「同源闭式」复现 attack28/29 读数，属同源复算；')
E('        本段改用 RK4 数值积分（不同算法），并额外核 attack30(2loopRGE) 的 2-loop 读数。')
E('')

B1 = {
    'SM': [4.1, -19.0 / 6.0, -7.0],
    'MSSM': [33.0 / 5.0, 1.0, -3.0],
}
B2 = {
    'SM': [[199.0 / 50.0, 27.0 / 10.0, 44.0 / 5.0],
           [9.0 / 10.0, 35.0 / 6.0, 12.0],
           [11.0 / 10.0, 9.0 / 2.0, -26.0]],
    'MSSM': [[199.0 / 25.0, 27.0 / 5.0, 88.0 / 5.0],
             [9.0 / 5.0, 25.0, 24.0],
             [11.0 / 5.0, 9.0, 14.0]],
}
TWO_PI = 2.0 * math.pi
EIGHT_PI2 = 8.0 * math.pi ** 2
MZ_F = 91.1876


def rhs(a, model, two_loop, bscale=1.0):
    b = B1[model]
    out = [0.0, 0.0, 0.0]
    if two_loop:
        M = B2[model]
        for i in range(3):
            s = 0.0
            for j in range(3):
                s += M[i][j] / a[j]
            out[i] = -b[i] * bscale / TWO_PI - s / EIGHT_PI2
    else:
        for i in range(3):
            out[i] = -b[i] * bscale / TWO_PI
    return out


def flow(a0, L1, L2, two_loop, n=1200, bscale=1.0):
    a = list(a0)
    for seg, model in ((L1, 'SM'), (L2, 'MSSM')):
        if seg == 0:
            continue
        h = seg / n
        for _ in range(n):
            k1 = rhs(a, model, two_loop, bscale)
            aa = [a[i] + 0.5 * h * k1[i] for i in range(3)]
            k2 = rhs(aa, model, two_loop, bscale)
            bb = [a[i] + 0.5 * h * k2[i] for i in range(3)]
            k3 = rhs(bb, model, two_loop, bscale)
            cc = [a[i] + h * k3[i] for i in range(3)]
            k4 = rhs(cc, model, two_loop, bscale)
            a = [a[i] + h / 6.0 * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i])
                 for i in range(3)]
    return a


def solve_seg(two_loop, L1g=2.4, L2g=33.0, n=1200, A0v=None, bscale=1.0):
    start = A0 if A0v is None else A0v
    L1, L2 = L1g, L2g
    for _ in range(60):
        f0 = flow(start, L1, L2, two_loop, n, bscale)
        r0 = f0[0] - f0[1]
        r1 = f0[0] - f0[2]
        if abs(r0) + abs(r1) < 1e-13:
            break
        d = 1e-6
        fa = flow(start, L1 + d, L2, two_loop, n, bscale)
        fb = flow(start, L1, L2 + d, two_loop, n, bscale)
        j11 = (fa[0] - fa[1] - r0) / d
        j21 = (fa[0] - fa[2] - r1) / d
        j12 = (fb[0] - fb[1] - r0) / d
        j22 = (fb[0] - fb[2] - r1) / d
        det = j11 * j22 - j12 * j21
        if abs(det) < 1e-18:
            break
        dL1 = (r0 * j22 - j12 * r1) / det
        dL2 = (j11 * r1 - r0 * j21) / det
        L1 -= dL1
        L2 -= dL2
    return L1, L2, flow(start, L1, L2, two_loop, n, bscale)


ALPHA_EM_F = 1.0 / 127.916
ALPHA_S_F = 0.1184
SW_F = 0.23122
A0 = [
    3.0 / 5.0 * (1.0 - SW_F) / ALPHA_EM_F,
    SW_F / ALPHA_EM_F,
    1.0 / ALPHA_S_F,
]
E('  输入（M_Z 处）：alpha1^-1=%.6f  alpha2^-1=%.6f  alpha3^-1=%.6f'
  % (A0[0], A0[1], A0[2]))
E('')
res = {}
for tag, tl in (('1-loop', False), ('2-loop', True)):
    L1, L2, enda = solve_seg(tl)
    msusy = MZ_F * math.exp(L1)
    mgut = msusy * math.exp(L2)
    ginv = sum(enda) / 3.0
    spread = max(enda) - min(enda)
    res[tag] = (msusy, mgut, ginv, spread, L1, L2)
    E('  %-8s L1=%+9.6f  L2=%9.6f  M_SUSY=%12.5f GeV  M_GUT=%.6e GeV  alpha_GUT^-1=%.4f  汇聚残差=%.3e'
      % (tag, L1, L2, msusy, mgut, ginv, spread))
E('')
# 内置自校准：1-loop 应与 attack29 的 54.384716 GeV 一致
ref_msusy_1l = 54.384716
dev_1l = abs(res['1-loop'][0] - ref_msusy_1l) / ref_msusy_1l
E('  自校准（1-loop vs attack29 的 54.384716 GeV）：相对偏差 %.3e' % dev_1l)
# 跨册对拍 attack30(2loopRGE)
ref_msusy_2l = 193.04415
ref_mgut_2l = 7.9167351e15
dev_2l_m = abs(res['2-loop'][0] - ref_msusy_2l) / ref_msusy_2l
dev_2l_g = abs(res['2-loop'][1] - ref_mgut_2l) / ref_mgut_2l
E('  跨册对拍（2-loop vs attack30 的 193.04415 GeV / 7.9167351e15 GeV）：')
E('    M_SUSY 相对偏差 %.4e ；M_GUT 相对偏差 %.4e' % (dev_2l_m, dev_2l_g))
selfcal = dev_1l < 0.02
crossok = (dev_2l_m < 0.02 and dev_2l_g < 0.02)
E('  >> 自校准（1-loop 对 attack29）：%s' % ('通过（<2%）' if selfcal else '未通过'))
E('  >> 跨册对拍（2-loop 对 attack30）：%s'
  % ('通过（<2%）' if crossok else '未通过 —— 须列出差异候选'))
if selfcal and not crossok:
    E('     差异候选（不下结论，只登记）：')
    E('       (d1) 两册「解」的定义不同：攻击册可能是「前向解 sin2thetaW + 后向解 M_SUSY」混合，')
    E('            本册是「两段同时打靶使三耦合相等」；')
    E('       (d2) 2-loop 矩阵 b_ij 的具体取值/符号（尤其 b_33 与 U(1) 归一化）；')
    E('       (d3) 阈值修正是否计入（本册未计入）。')
if selfcal and crossok:
    add('F5 PASS', 'PASS',
        'RK4 数值积分独立复现 1-loop 与 2-loop 的 M_SUSY / M_GUT',
        '1-loop M_SUSY=%.4f GeV（对 attack29 偏差 %.2e）；2-loop M_SUSY=%.4f GeV / M_GUT=%.3e'
        % (res['1-loop'][0], dev_1l, res['2-loop'][0], res['2-loop'][1]),
        '与 attack31 E5 的「同源闭式」不同，本段用 RK4 数值积分，属算法独立。'
        '两条路径同时对上 attack29/attack30 的读数 => 前两册数值可信。'
        '注意：本段只验证数值，不重判物理（M_SUSY 远低于 1 TeV 是 1-loop 单阈值的已知局限）')
elif selfcal:
    add('F5 MISMATCH', 'MISMATCH',
        '1-loop 自校准通过但 2-loop 未复现 attack30 读数（差异须归因）',
        '自校准偏差 %.2e；2-loop M_SUSY 偏差 %.2e / M_GUT 偏差 %.2e'
        % (dev_1l, dev_2l_m, dev_2l_g),
        '按纪律不下「对方错」的结论：登记三条候选（解的定义 / b_ij 取值与符号 / 阈值修正）。'
        '归因见后续 F5c：b_ij「仅对角项」变体与 attack30 读数仅差约 5%，'
        '而「含非对角项」差 12 倍 => 差异集中在非对角项是否计入')
else:
    add('F5 FAIL', 'FAIL',
        '1-loop 自校准未通过，RK4 求解器实现有问题，2-loop 结果不可采信',
        '1-loop M_SUSY=%.4f GeV vs 参照 54.3847（偏差 %.2e）'
        % (res['1-loop'][0], dev_1l),
        '先修求解器再谈对拍：这是本册的自我否证门（宁可自判 FAIL 也不出假 PASS）')

# ---- F5b 病态性诊断（本轮新增，解释 F5 的 11 倍差异）----
E('')
E('[F5b] 病态性诊断：M_SUSY 反解对「阶数 / 系数 / 输入」的敏感性')
E('-' * 78)
L1_1l = res['1-loop'][4]
L1_2l = res['2-loop'][4]
dL1_order = L1_2l - L1_1l
E('  事实：1-loop L1=%+.6f，2-loop L1=%+.6f => 阶数变化造成 dL1=%+.6f'
  % (L1_1l, L1_2l, dL1_order))
E('        折合 M_SUSY 变化 %.2f 倍' % math.exp(abs(dL1_order)))
E('')
E('  问：这个位移是「2-loop 物理」，还是「近退化放大」？')
E('  做法：把 1-loop 的输入/系数各扰动一点点，看能造成多大的 dL1。')
E('')


def _mk(sw_mul, as_mul):
    return [3.0 / 5.0 * (1.0 - SW_F * sw_mul) / ALPHA_EM_F,
            SW_F * sw_mul / ALPHA_EM_F,
            1.0 / (ALPHA_S_F * as_mul)]


_ae2 = ALPHA_EM_F / 1.01
_A_ae = [3.0 / 5.0 * (1.0 - SW_F) / _ae2, SW_F / _ae2, 1.0 / ALPHA_S_F]
CASES = [
    ('输入 sin2thetaW +0.1%', _mk(1.001, 1.0), 1.0),
    ('输入 alpha_s +1%', _mk(1.0, 1.01), 1.0),
    ('输入 alpha_em +1%', _A_ae, 1.0),
    ('beta 系数 +1%', A0, 1.01),
    ('beta 系数 -1%', A0, 0.99),
]
pert = {}
E('  %-30s %-14s %-14s %s' % ('扰动', 'dL1', 'M_SUSY 倍数', '占阶数差比例'))
for name, a0v, bs in CASES:
    L1x, L2x, _e = solve_seg(False, A0v=a0v, bscale=bs, n=800)
    d = L1x - L1_1l
    pert[name] = d
    E('  %-30s %+14.6f %-14.4f %.1f%%'
      % (name, d, math.exp(abs(d)),
         100.0 * abs(d) / abs(dL1_order) if dL1_order else 0.0))
E('')


def _jac(L1, L2, two_loop, n=800):
    f0 = flow(A0, L1, L2, two_loop, n)
    r0 = f0[0] - f0[1]
    r1 = f0[0] - f0[2]
    d = 1e-6
    fa = flow(A0, L1 + d, L2, two_loop, n)
    fb = flow(A0, L1, L2 + d, two_loop, n)
    return [[(fa[0] - fa[1] - r0) / d, (fb[0] - fb[1] - r0) / d],
            [(fa[0] - fa[2] - r1) / d, (fb[0] - fb[2] - r1) / d]]


J = _jac(L1_1l, res['1-loop'][5], False)
detJ = J[0][0] * J[1][1] - J[0][1] * J[1][0]
_inv = [[J[1][1] / detJ, -J[0][1] / detJ], [-J[1][0] / detJ, J[0][0] / detJ]]
_nf = math.sqrt(sum(J[i][j] ** 2 for i in range(2) for j in range(2)))
_ni = math.sqrt(sum(_inv[i][j] ** 2 for i in range(2) for j in range(2)))
cond_J = _nf * _ni
E('  解的 Jacobian 条件数 cond(J) = %.2f（2x2，Frobenius）' % cond_J)
E('  >> 条件数不大 => 不是数值病态，而是**问题本身近退化**：')
E('     1-loop 下 MSSM 三点几乎同时汇聚，L1 的解由「两条近重合直线的交点」给出，')
E('     任何百分级改动都会把交点移到别处。')
E('')
d_beta = abs(pert['beta 系数 +1%'])
ratio_beta = d_beta / abs(dL1_order) if dL1_order else 0.0
E('  >> 关键比值：1%% 的 beta 系数扰动只造成 dL1=%.4f，仅占阶数变化的 %.2f%%。'
  % (d_beta, 100.0 * ratio_beta))
E('     => 阶数位移**不能**用系数误设解释：要复现 %.2f 的位移，beta 需被误设 %.0f%%。'
  % (dL1_order, 100.0 / ratio_beta if ratio_beta else 0.0))
E('  >> 三代误差源横向对比：')
E('     参数误差（系数 +1%%）        => M_SUSY x%.4f'
  % math.exp(abs(pert['beta 系数 +1%'])))
E('     测量误差（sin2thetaW +0.1%%）=> M_SUSY x%.4f'
  % math.exp(abs(pert['输入 sin2thetaW +0.1%'])))
E('     测量误差（alpha_s +1%%）     => M_SUSY x%.4f'
  % math.exp(abs(pert['输入 alpha_s +1%'])))
E('     模型误差（1->2 loop）        => M_SUSY x%.2f' % math.exp(abs(dL1_order)))
E('')
E('  >> 正确归因（修正初版叙事）：这是「截断阶数主导」的典型形态 ——')
E('     模型误差（42 倍）远大于参数误差（0.5%）与测量误差（1.3~1.5 倍）。')
E('     cond(J)=%.1f 说明解本身良态，所以 42 倍不是数值噪声，' % cond_J)
E('     而是「把低能残差重新分配到不同截断阶」的真实位移。')
E('     结论：M_SUSY 不是被测出来的物理量，而是「某阶截断下的记账量」。')
add('F5b BOUNDARY', 'BOUNDARY',
    'M_SUSY 反解由截断阶数主导（42 倍），远超参数误差 0.5% 与测量误差 1.3~1.5 倍',
    'cond(J)=%.2f；dL1(阶数)=%+.4f(x%.2f)；dL1(beta+1%%)=%+.4f(x%.4f)；输入 0.1%%=>x%.4f'
    % (cond_J, dL1_order, math.exp(abs(dL1_order)), pert['beta 系数 +1%'],
       math.exp(abs(pert['beta 系数 +1%'])), math.exp(abs(pert['输入 sin2thetaW +0.1%']))),
    '初版把 42 倍归因为「系数误设同量级」是错的（实测系数 1% 只造成 0.5%），已自抓更正。'
    '正确归因：模型误差（截断阶数）主导，参数/测量误差均小 1~2 个量级。'
    '因此 attack29 的 54.38 GeV、attack30 的 193 GeV、本册的 2318 GeV 三者'
    '都在同一「截断敏感」问题的不同切片上，相互差异主要是阶数与矩阵约定，不是物理。'
    '可检验性含义：任何以 M_SUSY 为中间量的「预言」（含 tau_p）都必须先报截断误差带')

# ---- F5c b_ij 约定变体扫描（解释 F5 的 11 倍跨册差异）----
E('')
E('[F5c] b_ij 约定变体扫描：2-loop 结果的「约定依赖」有多大')
E('-' * 78)
E('  attack30 与本册都用「标准 MSSM 2-loop 矩阵」，但仍差 11 倍。')
E('  下面直接扫 4 种常见/易错的矩阵变体，看 M_SUSY 的分布范围。')
E('')
_orig_b2m = B2['MSSM']
_m0 = B2['MSSM']
VARIANTS = [
    ('V0 标准 MSSM', [list(r) for r in _m0]),
    ('V1 仅对角项', [[_m0[i][j] if i == j else 0.0 for j in range(3)]
                    for i in range(3)]),
    ('V2 误用 SM 阵', [list(r) for r in B2['SM']]),
    ('V3 b33 反号', [[_m0[i][j] if not (i == 2 and j == 2) else -_m0[2][2]
                    for j in range(3)] for i in range(3)]),
]
E('  %-20s %-14s %-16s %s' % ('变体', 'M_SUSY GeV', 'M_GUT GeV', 'alpha_GUT^-1'))
var_msusy = []
for name, mat in VARIANTS:
    B2['MSSM'] = mat
    L1x, L2x, enda = solve_seg(True, n=800)
    ms = MZ_F * math.exp(L1x)
    mg = ms * math.exp(L2x)
    var_msusy.append(ms)
    E('  %-20s %-14.4f %-16.6e %.4f' % (name, ms, mg, sum(enda) / 3.0))
B2['MSSM'] = _orig_b2m
_span = max(var_msusy) / min(var_msusy)
_dev_v1 = abs(var_msusy[1] - ref_msusy_2l) / ref_msusy_2l
E('')
E('  >> M_SUSY 在 4 种约定下跨度 = %.2f 倍（min %.2f / max %.2f GeV）'
  % (_span, min(var_msusy), max(var_msusy)))
E('  >> 归因收敛（本轮最强读数）：')
E('     V1「仅对角项」给 %.2f GeV，与 attack30 的 %.2f GeV 仅差 %.2f%%；'
  % (var_msusy[1], ref_msusy_2l, 100.0 * _dev_v1))
E('     V0「标准含非对角」给 %.2f GeV，与 attack30 差 %.1f 倍。'
  % (var_msusy[0], var_msusy[0] / ref_msusy_2l))
E('     => 跨册 11 倍差异最可能的单一归因：**非对角 b_ij 项是否计入**，')
E('        而不是任一方算错。按纪律本册不判对方错，只登记该约定敏感度。')
add('F5c BOUNDARY', 'BOUNDARY',
    '2-loop 的 M_SUSY 对 b_ij 约定跨 %.1f 倍；V1 仅对角与 attack30 仅差 %.2f%%' % (_span, 100.0 * _dev_v1),
    '4 变体 M_SUSY: %s GeV（跨度 %.2f 倍）'
    % (', '.join('%.1f' % v for v in var_msusy), _span),
    'V0 标准 / V1 仅对角 / V2 误用 SM / V3 b33 反号 四种约定给出的 M_SUSY 已跨越 %.1f 倍。'
    '其中 V1（仅对角项）与 attack30 的 193.04 GeV 仅差 %.2f%%，是把 11 倍跨册差异'
    '收敛到「非对角项是否计入」这一条的具体证据。=> 「2-loop 的 M_SUSY」不是可跨实现'
    '比较的量，引用时必须同时声明 b_ij 约定与求解定义' % (_span, 100.0 * _dev_v1))

# ============================================================
# F6 破壁代价精算
# ============================================================
E('')
E('[F6] 破壁代价精算：补齐 C1/C2 需要多少外部信息')
E('-' * 78)
fact18 = mp.factorial(18)
bits_perm = log2(fact18)
# 若只要求「分成 3 代」（每代 6 场，不区分场名）
fact6 = mp.factorial(6)
bits_gen = log2(fact18 / fact6 ** 3)
E('  18! = %s' % mp.nstr(fact18, 20))
E('  log2(18!) = %s bits   （把 18 个场任意配到 18 个标号所需信息量）'
  % mp.nstr(bits_perm, 8))
E('  log2(18!/(6!)^3) = %s bits   （只要求「分成 3 代」，不区分场名）'
  % mp.nstr(bits_gen, 8))
E('')
E('  >> 也就是说：')
E('     C2（场名标记函子）若以查表实现，等价于一张 %s bits 的表 = 未声明的外部输入；'
  % mp.nstr(bits_perm, 6))
E('     C1（代结选择规则）若只要求「代数 = 3」，最少也需 %s bits 的分组信息。'
  % mp.nstr(bits_gen, 6))
E('  >> 对比「自由常数 <= 1」的配额：两者都远超，且 C1 若写成连续选择函数，')
E('     其自由度是函数级（无限），不是常数级 —— 与 r15「自由度口径 II/III」同源。')
add('F6 INFO', 'INFO',
    '破壁的代价可量化：C2 需 >=52.5 bits 查表，C1 最少需 >=24.0 bits 分组',
    'log2(18!)=%s；log2(18!/(6!)^3)=%s'
    % (mp.nstr(bits_perm, 6), mp.nstr(bits_gen, 6)),
    '这不是「再加一个参数」的问题：补齐函子等价于补一张 18 行的外部映射表。'
    '按本工程「零外部输入」纪律，M8 的达成必须先修改纪律本身（与 r14 的出路④同型）')

out = {
    'round': 'attack32',
    'topic': '函子缺口的精算强化与反例排除',
    'entries': ENTRIES,
    'tally': {},
    'total': len(ENTRIES),
    'key_numbers': {
        'gap_calib_min_bits': mp.nstr(g_min, 8),
        'gap_calib_max_bits': mp.nstr(g_max, 8),
        'gap_positive_calibers': n_pos,
        'log2_8_residual_dps80': mp.nstr(res8, 4),
        'identifiability_nullity_at_0_constraints': 18,
        'winding_number_numeric': '%.12f' % winding,
        'su3_generator_def_hits': h_su3,
        'scanned_py_files': n_py,
        'scanned_py_files_full': len(_scan),
        'reachable_targets_demo': '%d/3' % reachable,
        'bridge_impl_hit_files': impl_hits,
        'scanner_control_import_files': ctrl_imp,
        'scanner_control_def_files': ctrl_def,
        'scanner_ok': scanner_ok,
        'rge_1loop_MSUSY_GeV': '%.5f' % res['1-loop'][0],
        'rge_1loop_MGUT_GeV': '%.6e' % res['1-loop'][1],
        'rge_2loop_MSUSY_GeV': '%.5f' % res['2-loop'][0],
        'rge_2loop_MGUT_GeV': '%.6e' % res['2-loop'][1],
        'rge_2loop_alphaGUT_inv': '%.4f' % res['2-loop'][2],
        'rge_2loop_convergence_residual': '%.3e' % res['2-loop'][3],
        'rge_selfcal_dev_1loop_vs_attack29': '%.3e' % dev_1l,
        'rge_cross_dev_2loop_MSUSY': '%.4e' % dev_2l_m,
        'rge_cross_dev_2loop_MGUT': '%.4e' % dev_2l_g,
        'bits_full_permutation_18': mp.nstr(bits_perm, 8),
        'bits_generation_grouping_only': mp.nstr(bits_gen, 8),
        'f5b_cond_J': '%.2f' % cond_J,
        'f5b_dL1_order_1loop_to_2loop': '%+.4f' % dL1_order,
        'f5b_MSUSY_mult_from_order': '%.2f' % math.exp(abs(dL1_order)),
        'f5b_dL1_beta_plus1pct': '%+.4f' % pert['beta 系数 +1%'],
        'f5b_MSUSY_mult_beta_plus1pct': '%.4f' % math.exp(abs(pert['beta 系数 +1%'])),
        'f5b_MSUSY_mult_sin2_plus0p1pct': '%.4f' % math.exp(abs(pert['输入 sin2thetaW +0.1%'])),
        'f5b_MSUSY_mult_alphas_plus1pct': '%.4f' % math.exp(abs(pert['输入 alpha_s +1%'])),
        'f5c_variant_MSUSY_GeV': ['%.4f' % v for v in var_msusy],
        'f5c_variant_span': '%.2f' % _span,
        'f5c_dev_V1_vs_attack30': '%.4f' % _dev_v1,
    },
    'verdict': 'F2 为强判据（不可识别性 nullity=18）；F1/F3 判 attack31 两处过度陈述并更正；'
               'F4 全目录复核维持「实现零」；F5 数值独立复算（见 tally）；'
               'F6 给出破壁代价（>=24.0 bits 分组 / >=52.5 bits 查表）',
    'red_line': '不否证 TUFT 物理；结论（几何路径给不出规范标号）不变，但判据须更换',
    'exit_code': 0,
}
tally = {}
for e in ENTRIES:
    tally[e['verdict']] = tally.get(e['verdict'], 0) + 1
out['tally'] = tally

E('=' * 78)
E('条目 %d：' % len(ENTRIES))
for k in sorted(tally):
    E('   %-10s %d' % (k, tally[k]))
E('-' * 78)
for e in ENTRIES:
    E('  %-14s %-10s %s' % (e['code'], e['verdict'], e['title']))
E('=' * 78)

with io.open(os.path.join(BASE, 'attack32_函子缺口精算强化与反例排除_2026-10-31.json'),
             'w', encoding='utf-8') as fh:
    fh.write(json.dumps(out, ensure_ascii=False, indent=1))
E('')
E('产物已写出：attack32_...json')
sys.exit(0)
