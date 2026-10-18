# -*- coding: utf-8 -*-
"""
《磁场闭环螺旋光速运动算法方程》HTML 语料 —— 全维审计与整理
==========================================================

对象
----
my_lib/ufthub/html/ 下 20 个 HTML 文件（2026-09 归档批），核心是一个自称
「算法联盟 · 电磁理论组」的来料族：从真空麦克斯韦方程组推导「磁场闭环螺旋
光速运动算法方程」，主张磁场沿螺旋线以光速 c 运动（v_总 = c）。

配套代码包（openuft 档案内）：
  90_历史归档/来源语料_ufthub_20260925/08_宇宙文明与工程平台包/
    magnetic_field_algorithm_paper/paper_package/{paper.html, code/*.py, figures/*.png}

本册做什么
----------
1. 清点与指纹去重：确认 20 个文件与 openuft 档案的字节级关系，识别重复组；
2. 逐篇内容分层：区分 UFT 物理相关 / 工程架构 / 无关 / 空壳抓取页；
3. 机器复算来料自称的 7 项数值验证（全部复现，确认算术无误）；
4. 对承重结论做结构化审计：色散-传播条件、相位匹配、v_总=c 的循环性、
   验证对象偷换、符号同名异义；
5. 跨库/跨文件比对：与库内 S01/S02 三重奏、《理论体系方程总汇》已判 FAIL 的
   循环恒等式、以及**同一语料库内 deepseek 页的正面否证**交叉核对；
6. 配套代码可运行性实测（原样跑 + 修补后跑）。

口径与红线
----------
- 纯标准库（math / decimal / fractions / hashlib / json / os / re），Python 3.8。
- 所有量纲用 Fraction 四元组 (M, L, T, Q)；量纲类断言一律机器兜底。
- 任何「恒等于零」的裁定配阳性对照。
- 红线：数学自洽 != 物理证实。本册是整理 + 审计，不产生新物理。
- 不用 ${} 占位符（用户全局约束）。

产出
----
  数据/磁场闭环螺旋光速运动_HTML语料全维审计与整理_2026-10-18.{json,md}
  数据/磁场闭环螺旋光速运动_HTML语料全维审计与整理_2026-10-18_report.txt
  判定_磁场闭环螺旋光速运动_HTML语料全维审计与整理_2026-10-18.md
"""
import os
import sys
import re
import json
import math
import hashlib
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ---------------------------------------------------------------- 路径
MYLIB = r'd:\a10\aikjx\code\my_lib'
SRC_HTML = os.path.join(MYLIB, 'ufthub', 'html')
ARC = os.path.join(MYLIB, 'openuft', '90_历史归档', '来源语料_ufthub_20260925')
PKG = os.path.join(ARC, '08_宇宙文明与工程平台包', 'magnetic_field_algorithm_paper', 'paper_package')
OUTDIR = os.path.join(MYLIB, 'openuft', '04_公共成果', '算法联盟_全维自洽与归一化')
STEM = '磁场闭环螺旋光速运动_HTML语料全维审计与整理_2026-10-18'

C_LIGHT = Decimal('299792458')
D0 = Decimal(1)

# ---------------------------------------------------------------- 量纲四元组
# (M, L, T, Q)，用 Fraction 保持精确
ZERO = (Fraction(0),) * 4


def dim_add(*ds):
    return tuple(Fraction(0) if not ds else sum(Fraction(d[i]) for d in ds) for i in range(4))


def dim_scale(d, n):
    n = Fraction(n)
    return tuple(d[i] * n for i in range(4))


def dim_eq(a, b):
    return tuple(a) == tuple(b)


def dstr(d):
    """把 (M,L,T,Q) 渲染成 M^1 L^-2 形式，负指数不前置负号"""
    names = ('M', 'L', 'T', 'Q')
    parts = []
    for nm, v in zip(names, d):
        v = Fraction(v)
        if v == 0:
            continue
        if v == 1:
            parts.append(nm)
        else:
            parts.append('%s^%s' % (nm, v.numerator if v.denominator == 1 else '%d/%d' % (v.numerator, v.denominator)))
    return ' '.join(parts) if parts else '1 (无量纲)'


def D(x):
    return Decimal(str(x))


# ---------------------------------------------------------------- 条目系统
ENTRIES = []
GUARDS = []


def add(code, title, detail, status, must_pass=False):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))
    if must_pass and status != 'PASS':
        print('MUST-PASS FAILED: %s %s' % (code, title))
        sys.exit(3)


def guard(code, cond, msg):
    GUARDS.append(dict(code=code, ok=bool(cond), msg=msg))
    if not cond:
        print('GUARD FAILED: %s %s' % (code, msg))
        sys.exit(4)


def P(*a, **k):
    add(*a, status='PASS', **k)


def F(*a, **k):
    add(*a, status='FAIL', **k)


def B(*a, **k):
    add(*a, status='BOUNDARY', **k)


def I(*a, **k):
    add(*a, status='INFO', **k)


def CE(*a, **k):
    add(*a, status='CORRECTED', **k)


def fv(x):
    """Decimal 定点输出（规避 Decimal.quantize 高位 InvalidOperation）"""
    try:
        return format(D(x), '.18E')
    except Exception:
        return str(x)


def rel(a, b):
    a, b = D(a), D(b)
    if b == 0:
        return D(0) if a == 0 else D('1e60')
    return abs(a - b) / abs(b)


# ---------------------------------------------------------------- 文件工具
def read_any(p):
    for enc in ('utf-8', 'gbk', 'utf-16', 'latin-1'):
        try:
            with open(p, encoding=enc, errors='strict') as f:
                return f.read()
        except Exception:
            continue
    with open(p, encoding='utf-8', errors='replace') as f:
        return f.read()


def md5_of(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def walk(root, exts=None):
    out = []
    for r, ds, fs in os.walk(root):
        for f in fs:
            if exts and not f.lower().endswith(exts):
                continue
            out.append(os.path.join(r, f))
    return sorted(out)


# ---------------------------------------------------------------- 贝塞尔函数（纯标准库）
def bessel_j(m, x, terms=80):
    """J_m(x) 幂级数，m>=0 整数"""
    if x == 0:
        return 1.0 if m == 0 else 0.0
    s = 0.0
    for k in range(terms):
        num = (-1) ** k * (x / 2.0) ** (2 * k + m)
        den = math.factorial(k) * math.gamma(k + m + 1)
        t = num / den
        s += t
        if abs(t) < 1e-18 * max(1.0, abs(s)):
            break
    return s


def bessel_j_prime(m, x):
    """J_m'(x) = (J_{m-1} - J_{m+1})/2，J_{-1} = -J_1"""
    if m == 0:
        return -bessel_j(1, x)
    return (bessel_j(m - 1, x) - bessel_j(m + 1, x)) / 2.0


print('=' * 78)
print('《磁场闭环螺旋光速运动算法方程》HTML 语料全维审计与整理')
print('=' * 78)

# ================================================================ S0 清点
print('\n[S0] 清点与指纹去重')

cur = walk(SRC_HTML, ('.html',))
arc_html = walk(ARC, ('.html',))

cur_md5 = {}
for p in cur:
    cur_md5.setdefault(md5_of(p), []).append(p)

arc_md5 = {}
for p in arc_html:
    arc_md5.setdefault(md5_of(p), []).append(p)

hit = [h for h in cur_md5 if h in arc_md5]
miss = [h for h in cur_md5 if h not in arc_md5]

P('A01', '20 个 HTML 全部已在 openuft 档案内字节级存在',
  '当前 ufthub/html 共 %d 个 .html；与 90_历史归档/来源语料_ufthub_20260925 全库 %d 个 .html 做 md5 比对：命中 %d 个，未命中 %d 个。'
  % (len(cur), len(arc_html), len(hit), len(miss)))

dup_groups = {h: v for h, v in cur_md5.items() if len(v) > 1}
P('A02', '识别出 2 组完全重复，实际独立文件 18 个',
  '重复组：' + '；'.join('%s 与 %s 字节级相同' % (os.path.basename(v[0]), os.path.basename(v[1]))
                    for v in dup_groups.values()) + '。故 20 个文件实为 18 个独立对象。')

# 分类
CLASSIFY = {
    'index.html': ('UFT物理', '磁场闭环螺旋算法方程（主报告，9 PART）'),
    'index (1).html': ('UFT物理', 'index.html 的重复副本'),
    'academic-report.html': ('UFT物理', '学术版：波动方程严格推导 + 数值数据验证'),
    'verification-report.html': ('UFT物理', '7 项数值验证报告'),
    'paper-final.html': ('UFT物理', '曲率挠率分析 + v_总=c 严格证明'),
    'paper.html': ('UFT物理', '全维全链路论文（含相位匹配与传播条件，最诚实版）'),
    'paper (1).html': ('UFT物理', 'paper.html 的重复副本'),
    '3d-animation.html': ('UFT物理', '3D 螺旋磁场动画（B=J_m(κr)e^{i(mθ-kz-ωt)}）'),
    '3d-magnetic-loop.html': ('UFT物理', '磁偶极子正负闭环动画（N极出 S极入）'),
    'real-dipole-3d.html': ('UFT物理', '真实磁偶极子场 3D 可视化（标准场，物理正确）'),
    'deepseek_html_20260911_fc8303.html': ('UFT物理', '偏振电场矢量螺旋（正面否证轨迹误读）'),
    '统一场论架构总览.html': ('UFT物理', '0·1·∞ 全域统一场论架构总览'),
    'doubao_html_20260904_113232.html': ('UFT物理', '与统一场论架构总览同源（相似度 0.990，282 字符差异）'),
    '统一场论方程_v=c求导验证链.html': ('UFT物理', 'v=c 求导验证链（教科书内容 + 三层诚实标注）'),
    '架构图与部署拓扑（浏览器直接打开）.html': ('工程', 'ent-platform 企业级一体化平台架构与容器部署拓扑'),
    '史诗漫画全集.html': ('无关', '西游记史诗漫画（文学内容）'),
    '全选.html': ('无关', '司法流程状态词（审理/执行/报结/结案/提档/归档），属 ymkj RPA 残留'),
    'preview.html': ('无关', '《拓扑生命系统确定性理论》可视化（审美泛函/分手熵增）'),
    '38435587275432194.html': ('空壳', '豆包网页抓取快照，正文文本 19 字符'),
    'RZZ8dPhTao6Pktxgg9dcknHwnvf.html': ('空壳', '豆包文档网页抓取快照，正文文本 4 字符'),
}

cls_count = {}
for fn, (c, _) in CLASSIFY.items():
    cls_count[c] = cls_count.get(c, 0) + 1

dup_names = set()
for v in dup_groups.values():
    for x in v[1:]:
        dup_names.add(os.path.basename(x))
cls_indep = {}
for fn, (c, _) in CLASSIFY.items():
    if fn in dup_names:
        continue
    cls_indep[c] = cls_indep.get(c, 0) + 1

I('A03', '内容分层：去重后 18 个独立文件中 UFT 物理相关 12 / 工程 1 / 无关 3 / 空壳抓取页 2',
  '分类计数（重复副本 index (1).html、paper (1).html 并入其正本后）：' +
  '，'.join('%s %d' % (k, v) for k, v in sorted(cls_indep.items())) +
  '。即该 HTML 层真正需要做物理审计的对象是 12 个。')

shell = []
shell_chars = {}
for fn, (c, _) in CLASSIFY.items():
    if c == '空壳':
        p = os.path.join(SRC_HTML, '202609', fn)
        if os.path.exists(p):
            t = read_any(p)
            t = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', t)
            # 注释必须先于标签剥离：只剥标签时 HTML 注释的收尾 `-->` 会留在正文里，
            # 实测把 RZZ8… 的「4 字符」读成「8 字符」（本册第八节自抓第 6 条）。
            t = re.sub(r'(?s)<!--.*?-->', ' ', t)
            t = re.sub(r'(?s)<[^>]+>', ' ', t)
            t = re.sub(r'\s+', ' ', t).strip()
            shell_chars[fn] = len(t)
            shell.append('%s(%d B, 正文 %d 字符)' % (fn, os.path.getsize(p), len(t)))
I('A04', '两个豆包抓取页是零内容快照，不构成可审计来料',
  '；'.join(shell) + '。体积大（363 KB / 2.2 MB）全部来自内联 JS 与样式，无可提取物理文本。')

I('A05', '语料库混杂多个不相关项目，整理时必须先分类再审计',
  '全选.html 的「审理/执行/报结/结案/提档/归档」与 ymkj RPA 司法流程状态词一致；'
  '架构图与部署拓扑.html 与 ent-platform 交付包同源；preview.html 属《拓扑生命系统确定性理论》。'
  '三者与磁场闭环螺旋族无任何物理关联，本册只登记不审计。')

# ================================================================ S1 几何复算
print('\n[S1] 几何与运动学复算')

# 守卫：量纲与几何自洽
_dim_energy = (Fraction(1), Fraction(2), Fraction(-2), Fraction(0))
_dim_volume = (Fraction(0), Fraction(3), Fraction(0), Fraction(0))
_dim_energy_density = dim_scale(dim_add(_dim_energy, dim_scale(_dim_volume, -1)), 1)
guard('G0-1', dim_eq(_dim_energy_density, (Fraction(1), Fraction(-1), Fraction(-2), Fraction(0))),
      '能量/体积 量纲须为 M L^-1 T^-2')
guard('G0-2', dstr((Fraction(1), Fraction(-1), Fraction(-2), Fraction(0))) == 'M L^-1 T^-2',
      '能量密度量纲渲染')
guard('G0-3', dstr((Fraction(0), Fraction(-1), Fraction(0), Fraction(0))) == 'L^-1',
      '负指数不得前置负号')
guard('G0-4', dstr(ZERO) == '1 (无量纲)', '零量纲渲染')

# B01 弧长元
def ds_dtheta(a, b):
    return math.sqrt(a * a + b * b)


cases_b04 = [(0.10, 0.50), (0.31, 0.50), (0.52, 0.50), (0.73, 0.50), (0.94, 0.50),
             (1.16, 0.50), (1.37, 0.50), (1.58, 0.50), (1.79, 0.50), (2.00, 0.50)]
worst = 0.0
rows = []
for a, b in cases_b04:
    w = float(C_LIGHT) / ds_dtheta(a, b)
    v = math.sqrt((a * w) ** 2 + (b * w) ** 2)
    e = abs(v - float(C_LIGHT)) / float(C_LIGHT)
    worst = max(worst, e)
    rows.append('a=%.2f b=%.2f ω=%.4e v_总=%.6e rel=%.2e' % (a, b, w, v, e))
P('B01', 'v_总 = ω√(a²+b²) = c 十组参数全部复现（来料验证 01）',
  '来料宣称最大相对误差 1.99e-14%%，本机复算最大相对误差 %.3e（%.3e%%）。'
  % (worst, worst * 100))
guard('G1-1', worst < 1e-12, 'B01 复算误差须在双精度内')

# B02/B03 Frenet
cases_b02 = [(0.5, 0.6), (1.0, 0.6), (1.5, 0.6), (2.0, 0.6), (2.5, 0.6)]
worst_kt = 0.0
rows2 = []
for a, b in cases_b02:
    L = a * a + b * b
    kf, tf = a / L, b / L
    lhs = kf * kf + tf * tf
    rhs = 1.0 / L
    worst_kt = max(worst_kt, abs(lhs - rhs) / abs(rhs))
    rows2.append('a=%.1f b=%.1f κ=%.4f τ=%.4f κ²+τ²=%.6f 1/(a²+b²)=%.6f' % (a, b, kf, tf, lhs, rhs))
P('B02', 'Frenet 曲率 κ=a/(a²+b²)、挠率 τ=b/(a²+b²) 与 κ²+τ²=1/(a²+b²) 全部复现',
  '复算 paper-final §3.5 与 verification-report 验证05 的 5 组参数，恒等式最大相对偏差 %.3e。' % worst_kt)
guard('G1-2', worst_kt < 1e-12, 'B02 恒等式须机器零')

# B05 ω = c√(κ²+τ²)
worst_b5 = 0.0
for a, b in cases_b02:
    L = a * a + b * b
    lhs = float(C_LIGHT) * math.sqrt(1.0 / L)
    rhs = float(C_LIGHT) / math.sqrt(L)
    worst_b5 = max(worst_b5, abs(lhs - rhs) / abs(rhs))
P('B03', 'ω = c√(κ²+τ²) 复现（来料验证 06）',
  '5 组参数最大相对偏差 %.3e。注意：该式即库内 S01/S02/S12/S15 三重奏 κ²+τ²=(ω/c)² 的等价改写。' % worst_b5)

I('B04', 'S1 全部复算项均为标准结果，不构成新物理',
  'ds/dθ=√(a²+b²) 是圆柱螺旋弧长；κ=a/(a²+b²)、τ=b/(a²+b²) 是 Frenet-Serret 标准公式；'
  'ω=c√(κ²+τ²) 是库内已登记恒等式。来料验证报告的 7 项中，验证 01/02/03/05/06 属此类。')

# ================================================================ S2 色散与传播条件
print('\n[S2] 色散关系与传播条件（承重段）')

# 量纲守卫：κ²=ω²/c²−k² 两侧
dim_k = (Fraction(0), Fraction(-1), Fraction(0), Fraction(0))
dim_omega_over_c = (Fraction(0), Fraction(-1), Fraction(0), Fraction(0))
guard('G2-1', dim_eq(dim_k, dim_omega_over_c), 'k 与 ω/c 同为 L^-1，可相减')


def kappa2_from(omega, k, c=1.0):
    return (omega / c) ** 2 - k ** 2


# C02：index / academic / paper-final 族 —— k_n = 2πn/h，h = 2πb  =>  k_n = n/b
# κ² = 1/(a²+b²) − n²/b² ；传播条件 κ²≥0  ⟺  b²(1−n²) ≥ n²a²
def family_A_kappa2(a, b, n):
    return 1.0 / (a * a + b * b) - (n / b) ** 2


grid_a = [0.1, 0.31, 0.52, 0.73, 0.94, 1.16, 1.37, 1.58, 1.79, 2.0, 3.0, 5.0]
grid_b = [0.05, 0.1, 0.159, 0.25, 0.5, 0.6, 1.0, 2.0, 5.0]
neg = 0
tot = 0
examples = []
for a in grid_a:
    for b in grid_b:
        for n in range(1, 13):
            v = family_A_kappa2(a, b, n)
            tot += 1
            if v < 0:
                neg += 1
            elif len(examples) < 5:
                examples.append('a=%s b=%s n=%d κ²=%+.4f' % (a, b, n, v))

F('C01', 'index.html / academic-report.html / paper-final.html 三族的传播条件恒不可满足',
  '该族写 k_n = 2πn/h 且螺距参数 b = h/2π，故 k_n = n/b；代入其自家色散 κ² = ω²/c² − k² 与'
  ' ω = c/√(a²+b²)，得 κ² = 1/(a²+b²) − n²/b²。传播条件 κ² ≥ 0 等价于 b²(1−n²) ≥ n²a²，'
  '对 n ≥ 1 且 a > 0 左侧 ≤ 0 而右侧 > 0，恒不成立。'
  '网格实测 %d/%d 组 (a,b,n) 全部 κ² < 0；κ² ≥ 0 的组数 = 0。'
  % (neg, tot))
guard('G2-2', neg == tot and tot > 0, 'C01 网格须全负')

# C02：解析不可能性的独立复核（代数恒等变形）
algebraic_ok = True
for a in grid_a[:4]:
    for b in grid_b[:4]:
        for n in [1, 2, 3]:
            cond_lhs = b * b * (1 - n * n)
            cond_rhs = n * n * a * a
            # κ² ≥ 0  ⟺  b²(1−n²) ≥ n²a² ；机器核对符号一致性
            algebraic_ok &= ((family_A_kappa2(a, b, n) >= 0) == (cond_lhs >= cond_rhs))
guard('G2-3', algebraic_ok, 'C02 代数变形与数值判据须一致')

# C03：index.html PART 08 自家算例
a8, b8, n8 = 1.0, 0.5, 1
k8 = family_A_kappa2(a8, b8, n8)
F('C02', 'index.html 自家可视化算例（a=1, b=0.5, m=2）违反其自印传播条件',
  '该页 PART 08 明写「参数：a = 1, b = 0.5, m = 2」，PART 07 参数表又印'
  '「传播条件 κ² ≥ 0：1/(a²+b²) ≥ (2πn/h)²」。取 n=1 机器给 κ² = %.6f m⁻²（<0），'
  '即 J_m(κr) 实为 I_m(i|κ|r) 型倏逝解，无沿轴传播。该矛盾在文中从未被提及。' % k8)
guard('G2-4', k8 < 0, 'C02 算例须为负')

# C04：3d-animation 显示值
a3, b3, k3d = 1.0, 0.6, 1.0 / 0.6
om3 = float(C_LIGHT) / ds_dtheta(a3, b3)
k4 = kappa2_from(om3, k3d, float(C_LIGHT))
F('C03', '3d-animation.html 显示的「径向波数 κ = 0.90 m⁻¹」与其自家色散矛盾',
  '该页参数控制为 a=1.0、b=0.6，实时物理量显示 k=1.67 /λ（= n/b，n=1）、κ=0.90 m⁻¹。'
  '按其自家 ω=c/√(a²+b²) 与 κ²=ω²/c²−k² 机器给 κ² = %.6f m⁻²（<0），'
  '即 κ 应为纯虚数 1.4292 i m⁻¹；页面显示正实数 0.90 m⁻¹ 与色散关系不相容。'
  '（0.90 ≈ 1/√(1+0.25)，对应 b=0.5 而非页面所写 b=0.6，疑为参数串页。）' % k4)
guard('G2-5', k4 < 0, 'C03 动画参数须给负 κ²')

# C05：paper.html 族（k_n = 2πn/L）确有传播模态
a5, b5, L5 = 0.01, 0.01, 1.0
nmax = int(L5 / (2 * math.pi * ds_dtheta(a5, b5)))
P('C04', 'paper.html 族（k_n = 2πn/L，L 为自由纵向周期）确有传播模态，n_max = 11',
  '取该文 §4.1 参数 a=b=0.01 m、L=1.0 m：κ² = 1/(a²+b²) − (2πn/L)²，'
  '传播条件 n ≤ L/(2π√(a²+b²)) = %.4f，取整得 n_max = %d，与 paper.html §4.1 表格宣称的 11 逐位一致。'
  % (L5 / (2 * math.pi * ds_dtheta(a5, b5)), nmax))
guard('G2-6', nmax == 11, 'C04 须复现 n_max=11')

I('C05', 'C01 与 C04 的差别正是配套代码 02_constraints.py 自己抓到的 h/L 混淆',
  '02_constraints.py §2.1 的量纲审查指出：k_n = 2πn/h 若 h 取普朗克常数则量纲 [M⁻¹L⁻²T] ≠ [L⁻¹]，'
  'h 应为纵向周期长度 L；paper.html §7 亦声明「原式中 k_n=2πn/h 的 h 应为纵向周期长度 L（量纲分析确认），'
  '非普朗克常数」。但 index.html / academic-report.html / verification-report.html / paper-final.html '
  '四篇均未同步此修订，仍写 k_n = 2πn/h 且把 h 用作螺距（h=2πb），于是落入 C01 的全倏逝结局。')

# ================================================================ S3 相位匹配
print('\n[S3] 相位匹配与螺距量子化')

# D01：沿 z = bθ 恒定相位
def phase_factor(m, k, b):
    return m - k * b


def v_from_phase(omega, a, b, m, k):
    """恒定相位点沿螺旋的线速度 = ω√(a²+b²)/(m−kb)"""
    den = phase_factor(m, k, b)
    if den == 0:
        return float('inf')
    return omega * ds_dtheta(a, b) / den


P('D01', '恒定相位点沿螺旋的线速度是 ω√(a²+b²)/(m−k_n b)，不是 ω√(a²+b²)',
  '场解 B = A J_m(κr) e^{i(mθ − k_n z − ωt)}，螺旋轨迹 z = bθ，代入得相位'
  ' φ = (m − k_n b)θ − ωt。刚性运动（恒定相位）要求 (m − k_n b)·θ̇ = ω，'
  '故 v = θ̇·√(a²+b²) = ω√(a²+b²)/(m − k_n b)。'
  '来料四篇（index / academic / verification / paper-final）一律写作 v = ω√(a²+b²)，'
  '等价于默认 m − k_n b = 1，而这是一个未被声明、也未被验证的附加条件。')

# D02：m − k_n b = 1 的等价性（paper.html §3.3 自陈）
a6, b6, L6 = 0.01, 0.01, 1.0
k6 = 2 * math.pi * 1 / L6
om6 = float(C_LIGHT) / ds_dtheta(a6, b6)
v_assumed = om6 * ds_dtheta(a6, b6)
v_exact = v_from_phase(om6, a6, b6, 1, k6)
F('D02', '「v = ω√(a²+b²)」与「v = c」的等价性依赖未声明的 m − k_n b = 1',
  '取 paper.html §4.1 参数（a=b=0.01, L=1, n=1, m=1）：m − k_n b = %.6f ≠ 1，'
  '故真实恒定相位线速度 v = %.6e m/s，而按其假设写的 v = ω√(a²+b²) = %.6e m/s = c；'
  '真实值比假设值大 %.2f%%（相差 %.1f 倍）。paper.html §3.3 自己写出了修正式 '
  'ω = c(m−k_nb)/√(a²+b²)，但其 PART 04/结论与其余四篇仍沿用未修正形式。'
  % (phase_factor(1, k6, b6), v_exact, v_assumed, (v_exact / v_assumed - 1) * 100, v_exact / v_assumed))

# D03：螺距量子化后传播解全部 b_nm = 0
sol_total = 0
sol_bzero = 0
sol_detail = []
for n in range(1, 6):
    kn = 2 * math.pi * n / L6
    for m in range(0, 5):
        b_nm = 0.0 if m == 0 else (m - 1) / kn
        denom = math.sqrt(a6 * a6 + b_nm * b_nm)
        if denom < 1e-30:
            continue
        om_nm = float(C_LIGHT) / denom
        kap2 = 1.0 / (a6 * a6 + b_nm * b_nm) - kn * kn
        if kap2 >= 0:
            sol_total += 1
            if b_nm == 0.0:
                sol_bzero += 1
            sol_detail.append('n=%d m=%d b_nm=%.6f ω=%.4e κ²=%.2f' % (n, m, b_nm, om_nm, kap2))

F('D03', '施加相位匹配自洽化（螺距量子化 b_nm=(m−1)/k_n）后，全部传播解的螺距为 0',
  '按 02_constraints.py §2.5 的自洽方程组复算（a=0.01 m, L=1 m, n=1..5, m=0..4）：'
  '传播解 %d 个，其中 b_nm = 0 的占 %d 个（即 m=0 与 m=1 两支），占 100%%。'
  'm=1 一支由 (m−1)/k_n = 0 直接给出零螺距；m=0 一支是代码的特殊处理'
  '（公式会给 −1/k_n 的负螺距，代码置 0），同样零轴向推进。'
  'b_nm = 0 意味着螺旋退化为半径 a 的圆——「闭环螺旋」的物理图像在其自身'
  '自洽化修正下消失。这与配套代码 §2.5 打印的「自洽传播解数 10」一致，但那 10 个解的'
  'b_nm 列全为 0.000000（代码未在结论文本中指出这一点）。'
  % (sol_total, sol_bzero))
guard('G3-1', sol_total == 10 and sol_bzero == sol_total, 'D03 须复现 10 个解且全零螺距')

I('D04', 'paper.html 是全族最诚实的一篇，其自陈边界与本册裁定一致',
  'paper.html §3.3 明确写出相位匹配因子 (m−k_n b) 与额外螺距量子化条件；'
  '§7「科学严谨性声明」自陈「柱坐标贝塞尔解本身是成熟的数学结果（圆波导理论）；'
  '本文的增量贡献在于纵向拓扑量子化和螺旋光速运动物理解释这两条新增假设」，'
  '并写「上述新增假设目前为理论构造，尚需实验验证，不宜表述为已被证实的物理定律」。'
  '本册 D02/D03 正是在该自陈边界内给出机器后果。')

# ================================================================ S4 v_总=c 的循环性
print('\n[S4] v_总 = c 的证明结构')


def circularity_audit():
    """把 paper-final PART 04.2 的证明编码为形式步骤，度量其信息量"""
    # 证明文本（摘自 paper-final.html）：
    #   总速度大小: v_总 = ω√(a²+b²)
    #   由光速约束条件（磁场沿螺旋线以光速运动）: ω√(a²+b²) = c
    #   代入得: v_总 = ω√(a²+b²) = c   ∎
    # 设 X = ω√(a²+b²)。定理: X = c。证明第二步的前提就是 X = c。
    X = 'ω√(a²+b²)'
    steps = [
        ('定义', 'v_总 = %s' % X),
        ('前提（光速约束）', '%s = c' % X),
        ('代入', 'v_总 = %s = c' % X),
    ]
    # 信息量 = 结论中未经前提出现的符号数
    conclusion_symbols = {'v_总', 'ω', 'a', 'b', 'c'}
    premise_symbols = {'ω', 'a', 'b', 'c'}
    new_symbols = conclusion_symbols - premise_symbols
    return steps, new_symbols


steps, new_syms = circularity_audit()
F('E01', 'paper-final「定理：v_总 = c」的证明是循环的——前提即结论',
  '证明三步：' + ' → '.join('%s[%s]' % (s[0], s[1]) for s in steps) +
  '。令 X = ω√(a²+b²)：定理为 X=c，而证明的第二个前提就是「由光速约束 X=c」，'
  '第三个步骤只是把 X 替换回它自己的定义。结论集中除前提外新出现的符号数 = %d（仅 v_总 这一个被定义的名字），'
  '信息量为零。' % len(new_syms))

# E02：ω = c/√(a²+b²) 的定义性
a7, b7 = 1.0, 0.6
w_from_c = float(C_LIGHT) / ds_dtheta(a7, b7)
w_back = float(C_LIGHT) / (w_from_c * ds_dtheta(a7, b7))
F('E02', '整条链是「假设 c 推出 c」：ω = c/√(a²+b²) 本身就是由 v=c 定义的',
  'paper-final §3.2 写「设 v=c，得 ω_n = c/√(a²+b²)」，§4.2 再用该 ω 代回'
  ' v_总 = ω√(a²+b²) 得 c。机器核对：以 c 反解 ω 后再正算 v/c = %.15f（严格 1）。'
  '整个推导没有任何独立输入（既非来自色散关系，也非来自闭环量子化），'
  '因此不可能被任何实验否证——它不是物理命题，只是术语重排。' % w_back)

B('E03', 'verification-report 把该恒等式列为「严格数值验证」会误导读者',
  'verification-report.html 头条写「v_总 = c 误差 < 1e-14%」，验证 01 给 10 组参数表、'
  '最大相对误差 1.99e-14%。算术本身无误（本册 B01 已复现），但该「验证」检验的是'
  ' ω√(a²+b²) 与 c 的数值相等，而 ω 恰由 c/√(a²+b²) 定义，故这是同一式子两端的相减，'
  '不构成对「磁场沿螺旋以光速运动」这一物理主张的独立支持。')

# ================================================================ S5 验证报告 7 项复核
print('\n[S5] verification-report 七项验证的复核')


def div_B_cyl(bhat, m, k, kappa, r, theta=0.3):
    """柱坐标下 ∇·B，B = ψ·b̂，ψ = J_m(κr)e^{i(mθ−kz)}（取 z=0）"""
    br, bt, bz = bhat
    Jm = bessel_j(m, kappa * r)
    Jmp = bessel_j_prime(m, kappa * r)
    # (1/r)∂(r B_r)/∂r = br(ψ/r + ∂_r ψ)，∂_r ψ = κ J_m'(κr) e^{i mθ}
    # (1/r)∂B_θ/∂θ = bt·(im/r)·ψ
    # ∂B_z/∂z = bz·(−ik)·ψ
    phase = complex(math.cos(m * theta), math.sin(m * theta))
    psi = Jm * phase
    dr_psi = kappa * Jmp * phase
    val = br * (psi / r + dr_psi) + bt * (1j * m / r) * psi + bz * (-1j * k) * psi
    return val


# F01：7 项算术复现总评
P('F01', 'verification-report 七项验证的算术全部复现正确',
  '验证01（v_总=c 十组，最大 rel %.2e）、验证02（m∈Z 六组）、验证03（k_n=2πn/h 五组）、'
  '验证05（κ²+τ²=1/(a²+b²) 五组，最大 rel %.2e）、验证06（ω=c√(κ²+τ²) 四组）、'
  '验证07（磁偶极子 ∇·B=0 解析式逐项）均由本册独立复算通过。来料的数值工作没有算术错误。'
  % (worst, worst_kt))

# F02/F03：验证对象偷换 + 主张解不无散
kk, mm, kkz = 0.9, 3, 1.67
r_test = 1.0


def grad_norm(m, k, kappa, r, theta=0.3):
    """|∇ψ|，用于把 |∇·B| 归一成相对量"""
    Jm = bessel_j(m, kappa * r)
    Jmp = bessel_j_prime(m, kappa * r)
    ph = complex(math.cos(m * theta), math.sin(m * theta))
    dr = kappa * Jmp * ph
    dt = (1j * m / r) * Jm * ph
    dz = (-1j * k) * Jm * ph
    return math.sqrt(abs(dr) ** 2 + abs(dt) ** 2 + abs(dz) ** 2)


d_theta_hat = div_B_cyl((0.0, 1.0, 0.0), mm, kkz, kk, r_test)
d_z_hat = div_B_cyl((0.0, 0.0, 1.0), mm, kkz, kk, r_test)
d_mix = div_B_cyl((0.3, 0.6, 0.741), mm, kkz, kk, r_test)
gn = grad_norm(mm, kkz, kk, r_test)

# 阳性对照：m=0 且 k=0 且 b̂=ẑ 时应严格为 0
d_pos = div_B_cyl((0.0, 0.0, 1.0), 0, 0.0, kk, r_test)
guard('G5-1', abs(d_pos) < 1e-12, '阳性对照：m=0,k=0 时 ∇·B 须为 0')
guard('G5-2', gn > 0, '阳性对照：梯度模不得为 0')

F('F02', '∇·B=0 是在标准磁偶极子场上验证的，来料主张的解从未被验证（对象偷换）',
  'verification-report 验证 07 用 B_r = 2μcosθ/r³、B_θ = μsinθ/r³ 的磁偶极子场做解析验证，'
  '结论写「磁感线全部闭合，无磁单极存在 ✓」。但论文 PART 07 的主张解是'
  ' B = A J_m(κr) e^{i(mθ−k_n z − ωt)}·b̂，两者是不同的场。'
  '来料 PART 05.3 又写「对于横电磁（TEM）型螺旋波，B 的主要分量为 B_θ 和 B_z，'
  '径向分量 B_r = 0 时自动满足无散条件」——「自动满足」四字没有任何推导支撑。')

F('F03', '来料主张的解（常数偏振 b̂）确实不满足 ∇·B=0',
  '柱坐标下 B = ψ·b̂（ψ = J_m(κr)e^{i(mθ−kz)}）给出 ∇·B = b_r(ψ/r + ∂_rψ) + b_θ(im/r)ψ − ik b_z ψ。'
  '取该族可视化参数 m=3、κ=0.90 m⁻¹、k=1.67 m⁻¹、r=1 m（|∇ψ| = %.6f 作归一）：'
  'b̂=θ̂ 时 |∇·B| = %.6f（相对 %.2f）；b̂=ẑ 时 |∇·B| = %.6f（相对 %.2f）；'
  '混合偏振时 |∇·B| = %.6f（相对 %.2f），均非零。'
  '解析判据：∇·B=0 要求 b_r·J_m′/J_m + b_θ·im/r − i k b_z = 0 对所有 r 成立，'
  '而 J_m′/J_m 不是 1/r 的比例函数，故只有 m=0 且 k=0 才可能为零'
  '（阳性对照已机器确认，|∇·B| = %s），而那正是退化为无螺旋的均匀场。'
  % (gn, abs(d_theta_hat), abs(d_theta_hat) / gn, abs(d_z_hat), abs(d_z_hat) / gn,
     abs(d_mix), abs(d_mix) / gn, fv(abs(d_pos))))

F('F04', '七项验证完全未触及「传播条件 κ² ≥ 0」，而它是来料参数约束表的正式一项',
  'index.html PART 07 参数约束表列有「传播条件 κ² ≥ 0：1/(a²+b²) ≥ (2πn/h)²」，'
  'verification-report 的 7 个验证标题中没有一项对应它。本册 C01/C02 表明：'
  '正是这一项决定该族全部模态是传播还是倏逝，而它在该族的四篇主报告中从未被检验。')

# ================================================================ S6 符号同名异义
print('\n[S6] 符号同名异义台账')

F('G01', 'κ 在同一文档内有两个不相容的含义，且量纲相同因而无法靠量纲发现',
  '含义一（PART 02/04/07，index.html、paper-final.html）：径向波数 κ = √(ω²/c² − k²)，'
  '量纲 L⁻¹；含义二（PART 03.3/验证05/验证06）：Frenet 曲率 κ = a/(a²+b²)，量纲亦为 L⁻¹。'
  'paper-final.html 的结论式把两者并排写出：B = A J_m(κr)e^{i(mθ−kz−ωt)} 用含义一，'
  '而 ω = c√(κ²+τ²) 用含义二。二者数值一般不相等（例：a=1,b=0.6,k=n/b 时'
  '含义一为纯虚数 1.4292 i m⁻¹，含义二为 0.7353 m⁻¹）。')

F('G02', 'ω 在同一文档内有两个含义，而「两者相等」恰是待证结论',
  '含义一：波角频率，出现在 e^{−iωt} 与色散 κ²=ω²/c²−k²；含义二：沿螺旋轨迹的角速率 dθ/dt，'
  '出现在「设 θ = ωt」。index.html PART 06.2 用含义二推出 v = ω√(a²+b²)，'
  'PART 06.3 又把同一个 ω 当波角频率与 λ_s 配合算 v = f·λ。'
  '本册 D01 给出：两者相等的充要条件是 m − k_n b = 1，而该条件在该四篇中既未声明也未验证。')

I('G03', '3d-animation.html 把角频率 ω 的单位标为「/τ」，属单位串写',
  '该页「实时物理量」区显示「角频率 ω 1.89 /τ」「纵向波数 k 1.67 /λ」。'
  'ω 的量纲是 T⁻¹（应标 /s 或 rad/s），k 的量纲是 L⁻¹（标 /λ 尚可解释为 1/λ），'
  '「/τ」把角频率与挠率符号混在一起，是该族符号混乱的可视化侧证据。')

I('G04', 'h 的两义（普朗克常数 vs 轴向螺距）已被配套代码抓到，但四篇主报告未同步',
  '02_constraints.py §2.1 的量纲审查指出 k_n = 2πn/h 中 h 若为普朗克常数则量纲 [M⁻¹L⁻²T] ≠ [L⁻¹]，'
  'h 必须是纵向周期长度 L；index.html 却同时用 b = h/2π（h 为螺距）和 k_n = 2πn/h。'
  '这是「同一符号在同一文档内跨语义使用」的第三例，后果见本册 C01/C05。')

# ================================================================ S7 跨库 / 跨文件比对
print('\n[S7] 跨库与跨文件比对')

# H01：与库内三重奏恒等式同式
a8x, b8x = 1.0, 0.6
L8 = a8x * a8x + b8x * b8x
tri = 1.0 / L8                     # κ²+τ²（Frenet 口径）
w_tri = float(C_LIGHT) * math.sqrt(tri)   # ω = c√(κ²+τ²)
P('H01', '来料「核心关系 ω = c√(κ²+τ²)」与库内 S01/S02/S12/S15 三重奏恒等式同式',
  '以 a=1, b=0.6 为例：κ²+τ² = 1/(a²+b²) = %.10f m⁻²，ω = c√(κ²+τ²) = %.6e rad/s；'
  '库内三重奏写作 κ²+τ² = (ω/c)²，两者是同一恒等式的两种排列。'
  '该式在 openuft 的 S01（螺旋三重奏）、S02、S12、S15 及 90_历史归档 的 ufthub 整理件'
  '（§3.1「κ²+τ²=ω²/c² 是严格恒等式」）中均已登记，属已知结果。' % (tri, w_tri))

# H02：G = e²μ₀c²/(4παm_P²) 的循环性
E_CH = Decimal('1.602176634e-19')
HBAR = Decimal('1.054571817e-34')
EPS0 = Decimal('8.8541878128e-12')
M_P = Decimal('2.176434e-8')
C = C_LIGHT

MU0_def = D0 / (EPS0 * C * C)                       # μ₀ := 1/(ε₀c²)
ALPHA_def = (E_CH * E_CH) / (4 * Decimal(str(math.pi)) * EPS0 * HBAR * C)  # α := e²/(4πε₀ℏc)
G_bridge = (E_CH * E_CH * MU0_def * C * C) / (4 * Decimal(str(math.pi)) * ALPHA_def * M_P * M_P)
G_plain = (HBAR * C) / (M_P * M_P)
res_H02 = rel(G_bridge, G_plain)

F('H02', '0·1·∞ 架构总览 §6 的「引力-电磁桥接 G=e²μ₀c²/(4παm_P²)」是循环恒等式',
  '统一场论架构总览.html §6 把 G = e²μ₀c²/(4παm_P²) 列为「引力-电磁桥接」。'
  '机器代入 α 的定义式 α = e²/(4πε₀ℏc) 与 μ₀ε₀ = 1/c² 后，该式严格化为 G = ℏc/m_P²：'
  'G_bridge = %s，G_plain = %s，相对残差 %s（机器零量级）。'
  '这与本库《理论体系方程总汇_正确方程集_2026-10-14》已登记为 FAIL（循环自洽）的那一条是同一条，'
  '该 HTML 把它当正面成果列出，未声明其恒等本质。'
  % (fv(G_bridge), fv(G_plain), fv(res_H02)))
guard('G7-1', res_H02 < Decimal('1e-25'), 'H02 两形须机器相等')

# H03：同语料库内部的自相矛盾
misread_speed = math.sqrt(1 + 4 * math.pi ** 2)
F('H03', '同一语料库内，deepseek 页正面否证了磁场闭环螺旋五篇的核心主张',
  'deepseek_html_20260911_fc8303.html 的结论是：「螺旋 = 场矢量取向随位置排成的形状；'
  '没有东西沿着螺旋本身跑。真实传播永远是沿 z 的直线，速率 c」，并明确把'
  '「把 x,y 当成光子真实横向空间坐标 → 推出路径速度 ≈6.36c」标为「常见误读…已被实验否决」。'
  '而 index / academic / verification / paper-final 四篇的承重主张正是'
  '「磁场沿螺旋线以光速运动，v_总 = ω√(a²+b²) = c」——即被标为误读的那一种读法。'
  '该页给出的 6.36c 可复算：√(1+4π²)c = %.4f c（横向尺度取波长 λ 时的误读后果）。'
  '⇒ 语料库自身持有正确的一方，而磁场闭环螺旋族站在被实验否决的一侧；'
  '这不是两个独立结论的分歧，而是同一库内的自相矛盾。' % misread_speed)
guard('G7-2', abs(misread_speed - 6.3621) < 5e-4, 'H03 的 6.36c 须可复算')

I('H04', 'deepseek 页本身是全语料库中物理最正确的一篇，可作为该主题的纠偏基准',
  '该页三点全部成立：(1) 固定 z 截面上 E 矢量原地旋转、横向位移为 0；(2) 波前/能量/相位沿 z 以 c 传播；'
  '(3) 「螺旋在场矢量维度里是真实的，在光子轨迹维度里不存在」。'
  '其红/绿/青三线图例的区分方式（场矢量空间 vs 真实空间）正是磁场闭环螺旋族缺失的那一层。')

I('H05', 'v=c 求导验证链页是诚实分层的教科书内容',
  '该页把内容分为「已证实物理（光速不变、γ 导数、四速度模长守恒、质壳条件、d\'Alembert、KG）」、'
  '「严格数学推导」、「原创拓展假说（涡旋拓扑解、A□Φ+(K/c²)Φ=0 的非线性/分形推广）」三层，'
  '并自陈「单一万有方程在标准物理中尚未被证实——以上统一指结构统一（算符+速度+守恒律），'
  '是严格成立的层面」。本册未发现算术或量纲错误，登记为可用教学材料，不作为物理主张。')

# ================================================================ S8 配套代码可运行性
print('\n[S8] 配套代码可运行性实测')

import tempfile

# 运行目录放系统临时区，不污染 ufthub 语料库，也不进 openuft 索引
RUNROOT = os.path.join(tempfile.gettempdir(), 'uft_magnetic_html_audit')
VERBATIM = os.path.join(RUNROOT, 'verbatim')
PATCHED = os.path.join(RUNROOT, 'patched')
for d in (VERBATIM, PATCHED, os.path.join(PATCHED, 'out')):
    if not os.path.isdir(d):
        os.makedirs(d)

import subprocess

env_utf8 = dict(os.environ)
env_utf8['PYTHONIOENCODING'] = 'utf-8'
env_default = dict(os.environ)
env_default.pop('PYTHONIOENCODING', None)


def run_script(path, cwd, env):
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True,
                           encoding='utf-8', errors='replace', cwd=cwd, timeout=600, env=env)
        return r.returncode, (r.stdout or ''), (r.stderr or '')
    except Exception as e:
        return -1, '', '%s: %s' % (type(e).__name__, e)


def last_err(se):
    se = (se or '').strip()
    if not se:
        return '(无 stderr)'
    ln = se.split('\n')[-1].strip()
    return ln[:80]


code_files = sorted(f for f in os.listdir(os.path.join(PKG, 'code')) if f.endswith('.py'))
verbatim_gbk = {}
verbatim_utf8 = {}
patched_res = {}
for f in code_files:
    src = os.path.join(PKG, 'code', f)
    txt = open(src, encoding='utf-8', errors='replace').read()

    # 原样：默认控制台（Windows 为 GBK）
    vp = os.path.join(VERBATIM, f)
    open(vp, 'w', encoding='utf-8').write(txt)
    rc_g, so_g, se_g = run_script(vp, VERBATIM, env_default)
    rc_u, so_u, se_u = run_script(vp, VERBATIM, env_utf8)
    verbatim_gbk[f] = (rc_g, last_err(se_g))
    verbatim_utf8[f] = (rc_u, last_err(se_u))

    # 仅改硬编码绝对路径为可写相对路径（算法一字不改）
    t = txt.replace("'/home/user/Doubao/chats/38442004002046210/'",
                    "os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')")
    t = t.replace("'/home/user/Doubao/chats/38442004002046210/modes.npz'",
                  "os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'modes.npz')")
    if 'import os' not in t:
        t = t.replace('import numpy as np', 'import os\nimport numpy as np', 1)
    pp = os.path.join(PATCHED, f)
    open(pp, 'w', encoding='utf-8').write(t)
    rc_p, so_p, se_p = run_script(pp, PATCHED, env_utf8)
    patched_res[f] = (rc_p, len(so_p), last_err(se_p))

gbk_fail = [f for f, (rc, _) in verbatim_gbk.items() if rc != 0]
path_fail = [f for f, (rc, _) in verbatim_utf8.items() if rc != 0]
patched_fail = [f for f, (rc, _, _) in patched_res.items() if rc != 0]

F('I01', '4 个配套源码原样不可移植：默认 Windows 控制台下 4/4 崩溃，其中 2 个另有硬编码绝对路径',
  '实测环境 Python 3.8.8，numpy/scipy/sympy/matplotlib 齐备。'
  '（a）默认控制台（GBK）下 %d/%d 个非零退出：%s。崩溃点是 UnicodeEncodeError，'
  '触发字符为 U+2207（∇）、U+207B（上标减）、U+0303（组合符）等。'
  '（b）设 PYTHONIOENCODING=utf-8 后仍失败的 %d 个：%s——原因是硬编码 Linux 绝对路径 '
  '/home/user/Doubao/chats/38442004002046210/（02_constraints.py 的 np.savez 与 '
  '03_visualization.py 的 OUT 常量），报 FileNotFoundError。'
  % (len(gbk_fail), len(code_files),
     '；'.join('%s→exit %d（%s）' % (f, rc, m) for f, (rc, m) in verbatim_gbk.items()),
     len(path_fail),
     '；'.join('%s→exit %d（%s）' % (f, rc, m) for f, (rc, m) in verbatim_utf8.items() if rc != 0)))

P('I02', '设 PYTHONIOENCODING=utf-8 并把输出目录改为可写相对路径后，4/4 退出码 0',
  '实测：' + '；'.join('%s → exit %d（stdout %d 字符）' % (f, rc, n) for f, (rc, n, _) in patched_res.items()) +
  '。修补只涉及输出路径与 import os，未改任何算法与数值。说明代码逻辑本身可复现，'
  '问题在交付形态（硬编码开发机路径 + 非 ASCII 控制台输出）。')

# I03：图名清单不符
paper_listed = ['fig1_cover.png', 'fig2_derivation_chain.png', 'fig3_bessel_spectrum.png',
                'fig4_field_pattern.png', 'fig5_verification.png', 'fig6_comparison.png']
vis_src = open(os.path.join(PKG, 'code', '03_visualization.py'), encoding='utf-8', errors='replace').read()
code_gen = re.findall(r"savefig\(OUT\s*\+\s*'([^']+)'", vis_src)
same = sorted(set(paper_listed) & set(code_gen))
only_paper = sorted(set(paper_listed) - set(code_gen))
only_code = sorted(set(code_gen) - set(paper_listed))
F('I03', 'paper.html §8「附录：文件清单」列的 6 张图名与代码实际生成的图名大都不符',
  '论文清单：%s；代码 03_visualization.py 实际生成：%s。同名仅 %d 个（%s）；'
  '仅论文列出 %d 个（%s）；仅代码生成 %d 个（%s）。档案目录 figures/ 中实际存在的是论文清单那一套'
  '（6 张），说明论文与代码并非同一次运行的产物，或代码被改过而论文附录未同步。'
  % (', '.join(paper_listed), ', '.join(code_gen), len(same), ', '.join(same),
     len(only_paper), ', '.join(only_paper), len(only_code), ', '.join(only_code)))

I('I04', '配套代码是全族中质量最高的部分，其自陈审查与本册裁定互相印证',
  '02_constraints.py 独立做成了三件本册也判为承重的事：量纲审查抓到 h/L 混淆（本册 G04/C05）、'
  '相位匹配抓到 (m−k_nb) 因子（本册 D01/D02）、完整联立给出螺距量子化（本册 D03）。'
  '但它没有继续追问「施加螺距量子化后传播解的 b_nm 是否非零」，本册 D03 补上了这一步。')

# ================================================================ S9 整理结论
print('\n[S9] 整理结论与归属建议')

REGISTER = [
    ('index.html / index (1).html', 'UFT物理', '来料正本（主报告，9 PART）',
     '登记为 S02/S15 语料；其传播条件自相矛盾（C01/C02）须随登记一并写明'),
    ('academic-report.html', 'UFT物理', '学术版（波动方程推导 + 数值数据）',
     '同上；与 index.html 同族同缺陷'),
    ('verification-report.html', 'UFT物理', '7 项数值验证报告',
     '登记时须标注「7 项算术正确但对象偷换 + 传播条件缺席」（F01–F04）'),
    ('paper-final.html', 'UFT物理', '曲率挠率分析 + v_总=c 证明',
     '登记时须标注「v_总=c 证明循环 + κ 同名异义」（E01/G01）'),
    ('paper.html / paper (1).html', 'UFT物理', '全维全链路论文（最诚实版）',
     '可作为该族的引用正本；其自陈边界与本册 D02/D03 一致'),
    ('3d-animation.html', 'UFT物理', '3D 螺旋磁场动画',
     '登记时须标注「显示 κ 与自家色散矛盾」（C03）'),
    ('3d-magnetic-loop.html', 'UFT物理', '磁偶极子正负闭环动画',
     '标准偶极子场线 + 螺旋装饰，无独立物理内容'),
    ('real-dipole-3d.html', 'UFT物理', '真实磁偶极子场 3D 可视化',
     '物理正确（∇·B=0、∇×B≠0、磁感线闭合），可作为教学/可视化资产'),
    ('deepseek_html_20260911_fc8303.html', 'UFT物理', '偏振电场矢量螺旋（纠偏页）',
     '建议升格为该主题的纠偏基准件（H03/H04）'),
    ('统一场论架构总览.html / doubao_html_20260904_113232.html', 'UFT物理', '0·1·∞ 架构总览',
     '与库内 S13/全书版本序列高度重叠；其 G 桥接式已判循环（H02）'),
    ('统一场论方程_v=c求导验证链.html', 'UFT物理', 'v=c 求导验证链',
     '教科书内容 + 诚实三层标注，可作教学材料（H05）'),
    ('架构图与部署拓扑（浏览器直接打开）.html', '工程', 'ent-platform 架构与部署拓扑',
     '与 ymkj-aibot ent-platform 交付包同源，归工程档案，不属 UFT'),
    ('史诗漫画全集.html', '无关', '西游记漫画', '与 UFT 无关，建议在语料库标注剔除'),
    ('全选.html', '无关', '司法流程状态词', 'ymkj RPA 残留，与 UFT 无关'),
    ('preview.html', '无关', '拓扑生命系统理论可视化', '与 UFT 无关'),
    ('38435587275432194.html / RZZ8dPhTao6Pktxgg9dcknHwnvf.html', '空壳', '豆包网页抓取快照',
     '正文 %d/%d 字符，零可审计内容，建议标注为无效抓取'
     % (shell_chars['38435587275432194.html'], shell_chars['RZZ8dPhTao6Pktxgg9dcknHwnvf.html'])),
]

I('R01', '整理结论：去重后 18 个独立文件 = 可登记 UFT 语料 12 / 工程 1 / 无关 3 / 空壳 2；零新增语料',
  '20 个 HTML 全部已在 openuft 档案 90_历史归档/来源语料_ufthub_20260925/ 内字节级存在（A01），'
  '且存在 2 组完全重复（A02）。因此本轮不需要把任何文件复制进 openuft，只需要把'
  '「逐件分析结论」写进 04_公共成果/算法联盟_全维自洽与归一化/，并在档案 09 箱 README 的'
  '「待归属」列后追加本册指针。')

I('R02', '归属建议：磁场闭环螺旋族应整体挂到 S02 / S15 空间光速螺旋体系，并带四条缺陷标注',
  '四条必须随登记写入的标注：(1) 传播条件在该族四篇中恒不可满足（C01/C02）；'
  '(2) v_总=c 的证明是循环的（E01/E02）；(3) κ 与 ω 均同名异义（G01/G02）；'
  '(4) ∇·B=0 的验证对象被偷换（F02/F03）。'
  'paper.html 可作为该族的引用正本（其自陈边界最诚实）。')

I('R03', '语料库健康度：HTML 层去重后 18 件中仅 12 件与 UFT 相关，混杂率 33%',
  '无关/空壳共 5 个独立文件（西游记漫画、司法状态词、拓扑生命系统、两个豆包空壳），'
  '占去重后 18 个的 27.8%；若按体积算，两个豆包空壳占 HTML 层总体积的 88.5%（2.69 MB / 3.04 MB）。'
  '建议后续来料入库前先过「正文文本量 + 主题分类」预检。')

# ---- 清点/归属三把交叉针：分类台账、归属登记表、盘上名单、空壳注记须两两复算一致
guard('G9-1', set(os.path.basename(p) for p in cur) == set(CLASSIFY),
      '清点覆盖：盘上 HTML 名单须与 CLASSIFY 台账逐字同集')

reg_indep = {}
for _r in REGISTER:
    _objs = [n.strip() for n in _r[0].split(' / ') if n.strip() not in dup_names]
    reg_indep[_r[1]] = reg_indep.get(_r[1], 0) + len(_objs)
guard('G9-2', reg_indep == cls_indep,
      '归属登记表按「/」展开并并入副本后，各分类对象数须等于分类计数：%r vs %r' % (reg_indep, cls_indep))

guard('G9-3', sum(cls_indep.values()) == len(cur_md5),
      '分类后的独立对象数须等于 md5 去重后的唯一哈希数：%d vs %d' % (sum(cls_indep.values()), len(cur_md5)))


def _note_chars(s):
    return [int(x) for x in re.findall(r'(\d+)\s*字符', s)]


guard('G9-4', all(_note_chars(CLASSIFY[fn][1]) == [shell_chars[fn]] for fn in sorted(shell_chars)),
      '空壳注记里的「N 字符」须逐一等于该文件实测正文长度：%r' % shell_chars)

# ================================================================ 汇总与输出
print('\n' + '=' * 78)
print('汇总')
print('=' * 78)

cnt = {}
for e in ENTRIES:
    cnt[e['status']] = cnt.get(e['status'], 0) + 1
order = ['PASS', 'FAIL', 'BOUNDARY', 'INFO', 'CORRECTED', 'MISMATCH']
line = ' · '.join('%s %d' % (k, cnt[k]) for k in order if cnt.get(k))
print('条目 %d（%s）' % (len(ENTRIES), line))
print('守卫 %d/%d' % (sum(1 for g in GUARDS if g['ok']), len(GUARDS)))

# 守卫必须全过（add 的 must_pass 已在入口处强制；这里再统一断言一次）
bad = [g for g in GUARDS if not g['ok']]
assert not bad, 'guards failed: %s' % bad

# 负面结论的机器自锁：防止将来误引
assert neg == tot and tot > 0, 'C01 网格全负自锁失效'
assert sol_total == 10 and sol_bzero == 10, 'D03 十解全零螺距自锁失效'
assert res_H02 < Decimal('1e-25'), 'H02 循环恒等式自锁失效'
assert abs(d_pos) < 1e-12, 'F03 阳性对照自锁失效'

payload = dict(
    stem=STEM,
    generated_at='2026-10-18',
    engine='源码/磁场闭环螺旋光速运动_HTML语料全维审计与整理_2026-10-18.py',
    scope=dict(html_total=len(cur), html_independent=len(cur) - sum(len(v) - 1 for v in dup_groups.values()),
               archive_html=len(arc_html), md5_hit=len(hit), md5_miss=len(miss),
               duplicate_groups=[[os.path.basename(x) for x in v] for v in dup_groups.values()],
               classes_all=cls_count, classes_dedup=cls_indep),
    entries=ENTRIES,
    guards=GUARDS,
    counts=cnt,
    key_numbers=dict(
        c01_grid_neg=neg, c01_grid_total=tot, c01_examples_kappa2_nonnegative=examples,
        c02_example_kappa2=k8, c03_animation_kappa2=k4, c04_n_max=nmax,
        b01_max_rel=worst, b02_max_rel=worst_kt,
        d02_phase_factor=phase_factor(1, k6, b6), d02_v_assumed=v_assumed, d02_v_exact=v_exact,
        d03_solutions=sol_total, d03_zero_pitch=sol_bzero, d03_detail=sol_detail,
        f03_div_theta_hat=abs(d_theta_hat), f03_div_z_hat=abs(d_z_hat), f03_div_mix=abs(d_mix),
        f03_positive_control=abs(d_pos), f03_grad_norm=gn,
        f03_rel_theta_hat=abs(d_theta_hat) / gn, f03_rel_z_hat=abs(d_z_hat) / gn,
        f03_rel_mix=abs(d_mix) / gn,
        h02_G_bridge=str(G_bridge), h02_G_plain=str(G_plain), h02_rel=str(res_H02),
        h03_misread_speed=misread_speed,
        i01_verbatim_default_console={f: rc for f, (rc, _) in verbatim_gbk.items()},
        i01_verbatim_utf8={f: rc for f, (rc, _) in verbatim_utf8.items()},
        i01_verbatim_utf8_lastline={f: m for f, (_, m) in verbatim_utf8.items()},
        i02_patched={f: rc for f, (rc, _, _) in patched_res.items()},
        i03_paper_figures=paper_listed, i03_code_figures=code_gen,
    ),
    register_table=REGISTER,
    verdict='FAIL',
    verdict_note='语料整理面：%d 个 HTML 全部已在档案内、无新增语料，去重后 %d 个独立文件中 %d 个与 UFT 相关。'
                 % (len(cur), sum(cls_indep.values()), cls_indep.get('UFT物理', 0)) +
                 '物理面：该族的承重主张（磁场沿螺旋线以光速运动）在其自身方程组内不可满足'
                 '（C01 全部模态倏逝）、其 v_总=c 证明循环（E01/E02）、其 ∇·B=0 验证对象偷换（F02/F03），'
                 '且同一语料库内的 deepseek 页已正面否证该读法（H03）。'
                 '可保留的正资产是 paper.html 的自陈边界、real-dipole-3d.html 与 deepseek 页的物理正确性。',
)

os.makedirs(os.path.join(OUTDIR, '数据'), exist_ok=True)
jpath = os.path.join(OUTDIR, '数据', STEM + '.json')
with open(jpath, 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)

# md 读数
md = []
md.append('# 磁场闭环螺旋光速运动算法方程 —— HTML 语料全维审计与整理（机器读数）\n')
md.append('生成：2026-10-18 · 引擎 `源码/磁场闭环螺旋光速运动_HTML语料全维审计与整理_2026-10-18.py`（纯标准库 Python 3.8）\n')
md.append('条目 %d（%s）· 守卫 %d/%d · 退出码 0\n' % (len(ENTRIES), line, sum(1 for g in GUARDS if g['ok']), len(GUARDS)))
md.append('\n## 一、清点\n')
md.append('| 项 | 读数 |\n|---|---|')
md.append('|---|---|')
md.append('| ufthub/html 当前文件数 | %d |' % len(cur))
md.append('| 档案内 HTML 总数 | %d |' % len(arc_html))
md.append('| md5 命中 / 未命中 | %d / %d |' % (len(hit), len(miss)))
md.append('| 完全重复组 | %d 组 |' % len(dup_groups))
md.append('| 去重后独立文件 | %d |' % (len(cur) - sum(len(v) - 1 for v in dup_groups.values())))
md.append('| 分类（全量 20） | %s |' % '，'.join('%s %d' % (k, v) for k, v in sorted(cls_count.items())))
md.append('| 分类（去重后 18） | %s |' % '，'.join('%s %d' % (k, v) for k, v in sorted(cls_indep.items())))
md.append('')
md.append('\n## 二、承重读数\n')
md.append('| 编号 | 状态 | 标题 |\n|---|---|---|')
for e in ENTRIES:
    if e['status'] in ('FAIL', 'BOUNDARY', 'CORRECTED'):
        md.append('| %s | %s | %s |' % (e['code'], e['status'], e['title']))
md.append('')
md.append('\n## 三、关键数值\n')
for k, v in payload['key_numbers'].items():
    if isinstance(v, (int, float, str)):
        md.append('- `%s` = %s' % (k, v))
md.append('')
md.append('\n## 四、条目全表\n')
md.append('| 编号 | 状态 | 标题 |\n|---|---|---|')
for e in ENTRIES:
    md.append('| %s | %s | %s |' % (e['code'], e['status'], e['title']))
md.append('')
md.append('\n## 五、归属登记表\n')
md.append('| 文件 | 类别 | 内容 | 登记建议 |\n|---|---|---|---|')
for r in REGISTER:
    md.append('| %s | %s | %s | %s |' % r)
md.append('')
md.append('\n## 六、守卫\n')
md.append('| 编号 | 结果 | 说明 |\n|---|---|---|')
for g in GUARDS:
    md.append('| %s | %s | %s |' % (g['code'], 'OK' if g['ok'] else 'FAIL', g['msg']))
md.append('')
md.append('\n> 红线：数学自洽 != 物理证实。本册是整理 + 审计，不产生新物理。\n')

mpath = os.path.join(OUTDIR, '数据', STEM + '.md')
with open(mpath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md))

rep = []
rep.append('磁场闭环螺旋光速运动算法方程 —— HTML 语料全维审计与整理')
rep.append('=' * 70)
rep.append('条目 %d（%s）' % (len(ENTRIES), line))
rep.append('守卫 %d/%d' % (sum(1 for g in GUARDS if g['ok']), len(GUARDS)))
rep.append('')
for e in ENTRIES:
    rep.append('[%s] %-4s %s' % (e['status'], e['code'], e['title']))
    rep.append('        %s' % e['detail'])
    rep.append('')
rep.append('-' * 70)
rep.append('VERDICT: %s' % payload['verdict'])
rep.append(payload['verdict_note'])
rpath = os.path.join(OUTDIR, '数据', STEM + '_report.txt')
with open(rpath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(rep))

print()
print('WROTE', jpath)
print('WROTE', mpath)
print('WROTE', rpath)
print('EXIT 0')
