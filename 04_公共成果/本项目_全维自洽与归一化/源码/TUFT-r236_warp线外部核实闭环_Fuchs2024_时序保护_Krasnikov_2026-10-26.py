# -*- coding: utf-8 -*-
# =============================================================================
# TUFT r236 · warp-drive 线（r64–r67）外部核实闭环
# 2026-10-26
#   ★改号：r200 已被并行会话《三维螺旋时空方程》（2026-10-25 落盘）占用
#     ⇒ 按「先占位者为权威 / 后到者整体改号」纪律，本册原稿号 r200 整体改 r236
#   承接：r64 F01 / F02 / F03 三条 BOUNDARY（离线不可核实项）
#   产出：同名 .json / .md / _report.txt
#   纯标准库；Decimal 60 位；四元组量纲 (M, L, T, Q)
#   方法论纪律（承接 r64 / r66 / r67）：
#     (1) 量纲工具自身先过 guard，再用于判定
#     (2) 「恒为负」类裁定必须配阳性对照
#     (3) 引用必须给出可复核 ID（arXiv 号 / DOI / 期刊卷页），不可复核的标 BOUNDARY
#     (4) 流行科学转述的数字（如「72%」）不算文献读数，单独登记为 BOUNDARY
#     (5) 外部核实可以确认、收紧或推翻来稿；三者都记账，不预设方向
# =============================================================================
from __future__ import annotations
import io
import os
import re
import sys
import json
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:  # pragma: no cover
    pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, '数据')
NAME = 'TUFT-r236_warp线外部核实闭环_Fuchs2024_时序保护_Krasnikov_2026-10-26'

# =============================================================================
# 0. 文献登记表（外部核实的事实底座）
#    每条必须带可复核 ID；无 ID 的论点一律不进判定
# =============================================================================
REFS = {
    'FUCHS2024': {
        'authors': ['Jared Fuchs', 'Christopher Helmerich', 'Alexey Bobrick',
                    'Luke Sellers', 'Brandon Melcher', 'Gianni Martire'],
        'title': 'Constant Velocity Physical Warp Drive Solution',
        'arxiv': '2405.02709',
        'bibcode': '2024CQGra..41i5013F',
        'journal': 'Class. Quantum Grav. 41, 095013 (2024)',
        'doi': '10.1088/1361-6382/ad26aa',
        'year': 2024, 'vol': 41, 'page': '095013',
        'abstract_claims': [
            'constant-velocity SUBLUMINAL warp drive',
            'satisfies ALL of the energy conditions',
            'stable matter shell + shift vector distribution',
            'shift vector cannot be reduced to a coordinate transformation',
            'regular matter shell with POSITIVE ADM mass',
        ],
    },
    'LE2602': {
        'authors': ['An T. Le'],
        'title': 'Observer-robust energy condition verification for warp drive spacetimes',
        'arxiv': '2602.18023',
        'bibcode': None,
        'journal': 'arXiv preprint (46 pages, v5)',
        'doi': '10.48550/arXiv.2602.18023',
        'year': 2026, 'vol': None, 'page': None,
        'abstract_claims': [
            'energy conditions must be quantified over ALL observers, not only Eulerian',
            'NEC/WEC/SEC as 4x4 linear matrix inequalities via classical S-lemma',
            'momentum constraint relates Eulerian momentum to shift-vector vorticity',
            'momentum vanishes identically iff shift = gradient field + rigid rotation',
            'Eulerian negative energy integral scales as v^2 (slices of unit time dilation)',
            'implemented in Warpax JAX toolkit; subluminal vs superluminal comparison',
        ],
    },
    'LE2605': {
        'authors': ['An T. Le'],
        'title': 'On the boundary cost of source-consistent warp shells',
        'arxiv': '2605.25417',
        'bibcode': None,
        'journal': 'arXiv preprint',
        'doi': '10.48550/arXiv.2605.25417',
        'year': 2026, 'vol': None, 'page': None,
        'abstract_claims': [
            'classical energy-condition admissibility for SUBLUMINAL positive-energy shells',
            'energy-condition failures LOCALIZED at smooth source-vacuum transition, not bulk',
            'all EIGHT canonical constructions fail the full test (boundary, not bulk)',
        ],
    },
    'LE2606': {
        'authors': ['An T. Le'],
        'title': 'Radiative steering of warp shells (v4; earlier title: '
                 'Steering a warp drive without exotic matter)',
        'arxiv': '2606.22531',
        'bibcode': None,
        'journal': 'arXiv preprint (39 pages, v4)',
        'doi': '10.48550/arXiv.2606.22531',
        'year': 2026, 'vol': None, 'page': None,
        'abstract_claims': [
            'exact timelike junctions between flat cavities and Kinnersley photon-rocket exterior',
            'shells satisfy strict SURFACE dominant energy condition',
            'steer SUBLUMINALLY under nonnegative radiation',
            'burns joined at static spheres: m_f/m_i = exp(-3L)',
            'self-similar shells require anisotropic stress + growing normal modes',
            'stress-free recoil with smooth emission requires photons ENTER the cavity',
            'self-gravitating settling after a turn remains OPEN',
        ],
    },
    'FINAZZI2010': {
        'authors': ['S. Finazzi', 'S. Liberati', 'C. Barcelo'],
        'title': 'Superluminal warp drives are semiclassically unstable',
        'arxiv': None,
        'bibcode': None,
        'journal': 'J. Phys. Conf. Ser. 222, 012046 (2010)',
        'doi': '10.1088/1742-6596/222/1/012046',
        'year': 2010, 'vol': 222, 'page': '012046',
        'abstract_claims': [
            'RSET (renormalized stress-energy tensor) of scalar field in superluminal warp spacetime',
            'semiclassical corrections make superluminal warp drives unstable',
        ],
    },
    'FINAZZI2010B': {
        'authors': ['S. Finazzi', 'S. Liberati', 'C. Barcelo'],
        'title': 'Semiclassical instability of warp drives',
        'arxiv': None,
        'bibcode': None,
        'journal': 'J. Phys. Conf. Ser. 229, 012018 (2010)',
        'doi': '10.1088/1742-6596/229/1/012018',
        'year': 2010, 'vol': 229, 'page': '012018',
        'abstract_claims': [
            'RSET behaviour in superluminal warp-drive spacetimes',
        ],
    },
    'BARcELO2010': {
        'authors': ['C. Barcelo', 'S. Finazzi', 'S. Liberati'],
        'title': 'On the Impossibility of Superluminal Travel: The Warp Drive Lesson',
        'arxiv': '1001.4960',
        'bibcode': None,
        'journal': 'arXiv preprint (9 pages)',
        'doi': '10.48550/arXiv.1001.4960',
        'year': 2010, 'vol': None, 'page': None,
        'abstract_claims': [
            'warp-drive lesson on impossibility of superluminal travel',
        ],
    },
    'KRASNIKOV2003': {
        'authors': ['S. Krasnikov'],
        'title': 'The quantum inequalities do not forbid spacetime shortcuts',
        'arxiv': 'gr-qc/0207057',
        'bibcode': None,
        'journal': 'Phys. Rev. D 67, 104013 (2003)',
        'doi': '10.1103/PhysRevD.67.104013',
        'year': 2003, 'vol': 67, 'page': '104013',
        'abstract_claims': [
            'class of spacetimes: Alcubierre bubble, Krasnikov tube, wormholes',
            'quantum inequalities DO NOT FORBID these shortcuts',
        ],
    },
    'EVERETT1997': {
        'authors': ['Allen E. Everett', 'Thomas A. Roman'],
        'title': 'Superluminal subway: The Krasnikov tube',
        'arxiv': None,
        'bibcode': None,
        'journal': 'Phys. Rev. D 56, 2100 (1997)',
        'doi': '10.1103/PhysRevD.56.2100',
        'year': 1997, 'vol': 56, 'page': '2100',
        'abstract_claims': [
            'two superluminal warp bubbles generate CTCs when relative velocity u > 2v/(1+v^2)',
        ],
    },
    'SAJEENDRAN2025': {
        'authors': ['Achintya Sajeendran', 'Timothy C. Ralph'],
        'title': 'Looping back to the past through free fall in a controlled '
                 'warp drive spacetime',
        'arxiv': '2407.18993',
        'bibcode': None,
        'journal': 'arXiv preprint (v2, Mar 2025)',
        'doi': '10.48550/arXiv.2407.18993',
        'year': 2024, 'vol': None, 'page': None,
        'abstract_claims': [
            'modification of rotating dynamical Alcubierre spacetime',
            'free-fall observers loop back to the past (CTC construction)',
        ],
    },
    'KERRSEN2025': {
        'authors': ['T. Bunyaratavej', 'P. Burikham', 'D. Senjaya'],
        'title': 'Revisiting chronology protection conjecture in the Dyonic '
                 'Kerr-Sen black hole spacetime',
        'arxiv': '2408.06023',
        'bibcode': None,
        'journal': 'Eur. Phys. J. C 85, 270 (2025)',
        'doi': '10.1140/epjc/s10052-025-13935-2',
        'year': 2025, 'vol': 85, 'page': '270',
        'abstract_claims': [
            'construct-level revisit of chronology protection conjecture (CPC)',
        ],
    },
}

# 流行科学转述数字（不算文献读数，单独登记）
POPULAR_CLAIMS = [
    {'claim': 'Eulerian analysis missed about 72 percent of wall weak-energy '
              'violations in the tested Rodal geometry',
     'source': 'freeastroscience.com popular summary (not the paper abstract)',
     'paper': 'LE2602',
     'status': 'unverified'},
]

# 来稿（r64 来料）中被核实的三个外部论点
INCOMING_CLAIMS = [
    {'id': 'F01', 'text': 'Fuchs 2024 常数速度正能量解（只正能量、满足能量条件、v_s<c）',
     'paper': 'FUCHS2024'},
    {'id': 'F02', 'text': 'Hawking 时序保护猜想完全未攻破', 'paper': None},
    {'id': 'F03', 'text': 'Krasnikov：负能壳半经典不稳定', 'paper': 'KRASNIKOV2003'},
]

# =============================================================================
# 1. 四元组量纲工具（与 r64/r66 同口径，先自检再使用）
# =============================================================================
DIM0 = (Fraction(0),) * 4


def dim(m, l, t, q):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))


def dmul(*ds):
    out = DIM0
    for d in ds:
        out = tuple(out[i] + d[i] for i in range(4))
    return out


def dpow(d, n):
    n = Fraction(n)
    return tuple(d[i] * n for i in range(4))


def deq(a, b):
    return all(a[i] == b[i] for i in range(4))


DIM_c = dim(0, 1, -1, 0)
DIM_E = dim(1, 2, -2, 0)
DIM_RHO_E = dim(1, -1, -2, 0)

GUARD = []


def guard(name, ok, note=''):
    GUARD.append({'guard': name, 'ok': bool(ok), 'note': note})
    return bool(ok)


# --- G0 量纲自检（r64 A03 结论：rho ~ v_s^2 c^2 G^-1 (df/dr)^2 为能量密度）---
DIM_FP = dim(0, -1, 0, 0)
G0_OK = all([
    guard('G0-1', deq(dmul(dpow(DIM_c, 2), dpow(DIM_c, 2), dpow(DIM_FP, 2),
                           dpow(dim(-1, 3, -2, 0), -1)), DIM_RHO_E),
           '[c^2 v_s^2 (f\')^2 / G] = 能量密度（r64 A03 唯一化族）'),
    guard('G0-2', deq(dmul(DIM_E, dpow(dim(0, 1, 0, 0), -3)), DIM_RHO_E),
           '能量密度 = 能量 / 体积'),
])

# =============================================================================
# 2. 文献元数据机器校验
# =============================================================================
def parse_bibcode(bc):
    """ADS bibcode：YYYY + 期刊5字符 + '..' + 卷 + 可选小写限定 + 页 + 尾字母。
    例 '2024CQGra..41i5013F' -> (2024, 'CQGra', '41', '5013')。"""
    m = re.match(r'^(\d{4})([A-Za-z&.]{5})\.{2}(\d+)[a-z]?(\d+)[A-Z]$', bc)
    if not m:
        return None
    return int(m.group(1)), m.group(2), m.group(3), m.group(4)


def arxiv_ym(aid):
    """arXiv 号 -> (year, month)。新旧格式均支持。"""
    m = re.match(r'^(\d{2})(\d{2})\.\d{4,5}$', aid)
    if m:
        yy, mm = int(m.group(1)), int(m.group(2))
        year = 2000 + yy if yy < 90 else 1900 + yy
        return year, mm
    m = re.match(r'^gr-qc/(\d{2})(\d{2})\d{3,5}$', aid)
    if m:
        yy, mm = int(m.group(1)), int(m.group(2))
        year = 2000 + yy if yy < 90 else 1900 + yy
        return year, mm
    return None


# --- V01a Fuchs bibcode / 期刊 / arXiv 三源一致性 ---
# bibcode '2024CQGra..41i5013F'：年份 2024 + 期刊缩写 CQGra + 卷 41 + 页 095013
# （bibcode 页字段丢前导零，'41'+'95013' 去分隔符后应为 '415013' 子串）
BC = parse_bibcode(REFS['FUCHS2024']['bibcode'])
FU = REFS['FUCHS2024']
_bc = FU['bibcode']
_bc_tail = re.sub(r'[^0-9A-Za-z]', '', _bc)          # 去点号等分隔符
_bc_nolow = re.sub(r'[a-z]', '', _bc_tail)           # 去卷页间小写限定字母（'i'）
V01a_ok = (
    _bc.startswith('2024')                            # (a) 年份
    and 'CQGra' in _bc                                # (b) 期刊缩写 = Class. Quantum Grav.
    and '415013' in _bc_nolow                         # (c) 卷 41 + 页 95013（去前导零）
    and BC is not None and BC[0] == 2024 and BC[1] == 'CQGra'
    and BC[2] == '41' and BC[3] == '5013'             # (d) bibcode 解析件一致
    and FU['year'] == 2024 and FU['vol'] == 41 and FU['page'] == '095013'
    and '41, 095013' in FU['journal'] and '2024' in FU['journal']  # (e) 期刊串自洽
)
AX = arxiv_ym(FU['arxiv'])
V01a_ok = bool(V01a_ok and AX == (2024, 5))           # (f) arXiv 2024-05

# --- V01b 来稿对 Fuchs 的描述逐条对照摘要原文 ---
INCOMING_F01 = {'subluminal': 'v_s<c', 'positive energy': '只正能量',
                'energy conditions': '满足能量条件'}
V01b_rows = []
for claim in FU['abstract_claims']:
    low = claim.lower()
    tag = ('subluminal' if 'subluminal' in low else
           'positive-energy' if ('positive' in low or 'all of the energy' in low) else
           'construction' if ('shell' in low or 'shift' in low) else 'other')
    V01b_rows.append((claim, tag))

# =============================================================================
# 3. 机器可复核的物理小结论
# =============================================================================
def D(x):
    return Decimal(str(x))


def sqrt(x):
    return (x.ln() / Decimal(2)).exp()


def exp(x):
    return x.exp()


def fv(x, sig=12):
    return '%.*E' % (sig, x)


# --- V04a Everett–Roman CTC 判据：u > 2v/(1+v^2)（v = 泡速/c > 1）---
CTC_V = [D('1'), D('1.5'), D('2'), D('5'), D('10'), D('200')]
CTC_ROWS = []
for v in CTC_V:
    uthr = D(2) * v / (D(1) + v * v)
    CTC_ROWS.append((v, uthr, uthr < D(1)))
CTC_SUP_GT1 = [r for r in CTC_ROWS if r[0] > 1]
CTC_ALL_SUP_LT1 = all(r[2] for r in CTC_SUP_GT1)          # v>1 全部 < 1
CTC_AT1 = [r for r in CTC_ROWS if r[0] == 1][0][1]
CTC_BOUNDARY_OK = (CTC_AT1 == D(1))                       # v=1 处恰为 1（阳性对照）

# --- V06a Le 2606 燃料界 m_f/m_i = exp(-3L) ---
FUEL_L = [D('0.1'), D('0.5'), D('1'), D('2'), D('3'), D('5')]
FUEL_ROWS = [(L, exp(-D(3) * L)) for L in FUEL_L]
FUEL_MONO = all(FUEL_ROWS[i][1] > FUEL_ROWS[i + 1][1]
                for i in range(len(FUEL_ROWS) - 1))
FUEL_AT1 = [r for r in FUEL_ROWS if r[0] == 1][0][1]

# --- V03a r64 A03（rho ~ v_s^2）与 Le 2602.18023（Euler 负能积分 ∝ v^2）互证 ---
V03a_note = ('r64 A03 用两条物理判据（恒等退化 + 线性 GR 极限）从 5 个量纲族中'
             '唯一选出 rho ~ v_s^2；Le 2602.18023 在「单位引力时间膨胀因子平直切片」上'
             '证明 Euler 负能积分严格按 v^2 缩放。两条独立路径同一指数 ⇒ 互证。')

# --- V05a Krasnikov 归属的极性机检 ---
KR = REFS['KRASNIKOV2003']
KR_TITLE_LOW = KR['title'].lower()
KR_PERMISSIVE = ('do not forbid' in KR_TITLE_LOW)
INCOMING_F03_TEXT = 'Krasnikov：负能壳半经典不稳定'
FIN_TITLE_LOW = REFS['FINAZZI2010']['title'].lower()
FIN_RESTRICTIVE = ('unstable' in FIN_TITLE_LOW)
V05a_polarity = (KR_PERMISSIVE, FIN_RESTRICTIVE)
KR_AX = arxiv_ym(KR['arxiv'])

# --- G  guards ---
guard('G1-fuchs-bibcode-3way', V01a_ok,
      'Fuchs 2024 的 bibcode（2024CQGra..41i5013F）/ 期刊（CQG 41,095013）/ '
      'arXiv（2405.02709 = 2024-05）三源年份卷页一致')
guard('G2-arxiv-ym', arxiv_ym('2405.02709') == (2024, 5)
      and arxiv_ym('gr-qc/0207057') == (2002, 7)
      and arxiv_ym('2602.18023') == (2026, 2)
      and arxiv_ym('2605.25417') == (2026, 5)
      and arxiv_ym('2606.22531') == (2026, 6)
      and arxiv_ym('2407.18993') == (2024, 7),
      '全部 arXiv 号的 YYMM 与论文年份一致（新旧格式都过）')
guard('G3-krasnikov-polarity-ctr', KR_PERMISSIVE and FIN_RESTRICTIVE,
      '阳性对照：Krasnikov 原文标题含 do not forbid（许可向）、'
      'Finazzi 标题含 unstable（限制向）⇒ 极性检测器有判别力')
guard('G4-ctc-threshold', CTC_ALL_SUP_LT1 and CTC_BOUNDARY_OK,
      'CTC 判据 u > 2v/(1+v^2)：v=1 处阈值恰为 1（边界，阳性对照），'
      'v>1 全部 < 1 ⇒ 两个超光速泡只需亚光速相对速度即可生成 CTC')
guard('G5-fuel-mono', FUEL_MONO and FUEL_AT1 < D('0.05'),
      '燃料界 exp(-3L) 严格递减且 L=1 处已跌到 5% 以下（阳性对照：L=0 时为 1）')
guard('G6-refs-have-ids', all(r.get('arxiv') or r.get('doi') for r in REFS.values()),
      '全部 %d 条文献至少带 arXiv 号或 DOI（无 ID 不进判定）' % len(REFS))
guard('G7-popular-not-cited', all(p['status'] == 'unverified' for p in POPULAR_CLAIMS),
      '流行科学数字（72%）标记为未核实，不作文献读数使用')

# =============================================================================
# 4. 条目容器
# =============================================================================
ITEMS = []


def add(code, verdict, title, detail, ev=''):
    ITEMS.append({'code': code, 'verdict': verdict, 'title': title,
                  'detail': detail, 'evidence': ev})


def PA(code, title, detail, ev=''):
    add(code, 'PASS', title, detail, ev)


def FA(code, title, detail, ev=''):
    add(code, 'FAIL', title, detail, ev)


def CO(code, title, detail, ev=''):
    add(code, 'CORRECTED', title, detail, ev)


def IN(code, title, detail, ev=''):
    add(code, 'INFO', title, detail, ev)


def MI(code, title, detail, ev=''):
    add(code, 'MISMATCH', title, detail, ev)


def BO(code, title, detail, ev=''):
    add(code, 'BOUNDARY', title, detail, ev)


# =============================================================================
# V 组 · 外部核实（本册全部内容）
# =============================================================================
# --- V01 Fuchs 2024：来稿钥匙 2 的引用确证 --------------------------------
V01_NOTE = (
    '外部检索确证来稿钥匙 2 所引文献真实存在且描述准确：'
    '%s 等 6 位作者《%s》，arXiv:%s，%s，DOI %s。'
    '摘要原文关键句逐条与来稿对照：'
    '(1)「constant-velocity SUBLUMINAL warp drive」= 来稿「v_s<c」✓；'
    '(2)「satisfies ALL of the energy conditions」= 来稿「满足能量条件」✓；'
    '(3)「stable matter shell with a shift vector distribution」⇒ **正能量解不是 '
    'Alcubierre 型泡**，而是「物质壳 + 位移矢量」构造 ✓（与 r64 D02 的机器预测一致：'
    'r64 D02 已证明 §四 的 rho 式恒负、不可能给出正能量泡，故钥匙 2 必属不同度规族）；'
    '(4)「positive ADM mass」⇒ 正能量属性确认；'
    '(5)「shift vector cannot be reduced to a coordinate transformation」'
    '⇒ 该解不是坐标戏法（作者自设的反规避条款）。'
    '⇒ **r64 F01 从 BOUNDARY 升级为 PASS**：来稿引用为真，钥匙 2 的「纸上存在」成立。'
    '但注意：这只确认「存在亚光速正能量解」，不确认「已攻破超光速」——见 V07。'
    % ('/'.join(FU['authors'][:2]) + ' 等', FU['title'], FU['arxiv'],
       FU['journal'], FU['doi']))

PA('V01', 'Fuchs 2024 引用确证：文献真实、六作者、CQG 41,095013、亚光速 + 全能量条件',
   V01_NOTE,
   'bibcode=%s | arxiv=%s (%d-%02d) | journal=%s | doi=%s'
   % (FU['bibcode'], FU['arxiv'], AX[0], AX[1], FU['journal'], FU['doi']))

# --- V02 来稿「2026 正能量解」确证存在，但方向是收紧 ----------------------
LE26 = [REFS['LE2602'], REFS['LE2605'], REFS['LE2606']]
V02_NOTE = (
    '来稿写「Fuchs 2024 及 2026 正能量解」。外部检索确证 2026 年确有同一路线的新文献，'
    '且全部出自单一作者 An T. Le 的三篇预印本：'
    '(a) arXiv:%s《%s》（46 页）——把能量条件检验从「单一 Euler 观测者」升级为'
    '「全部观测者」的 4x4 线性矩阵不等式（S-lemma）判据，并实现为 Warpax 工具包；'
    '(b) arXiv:%s《%s》——对**八个经典正能量壳层构造**做完整能量条件测试，'
    '结论是违背**集中在源-真空过渡边界**而不在体内部（即正能量宣称在边界处失效）；'
    '(c) arXiv:%s《%s》（39 页）——在严格曲面主导能量条件下构造亚光速转向，'
    '但代价是 m_f/m_i = exp(-3L) 的指数燃料界。'
    '⇒ **2026 文献的净方向是收紧而非确认**：它们没有给出新的超光速正能量解，'
    '而是（i）证明 Euler 分析会漏检违背、（ii）八个构造的边界处仍违背、'
    '（iii）转向代价指数爆炸。'
    '⇒ 来稿把 2026 文献当作钥匙 2 的加强证据，属**引用方向误读**。'
    % (LE26[0]['arxiv'], LE26[0]['title'], LE26[1]['arxiv'], LE26[1]['title'],
       LE26[2]['arxiv'], LE26[2]['title']))

CO('V02', '「2026 正能量解」确证存在（An T. Le 三篇），但净方向是收紧而非确认',
   V02_NOTE,
   'le2026=' + ','.join(r['arxiv'] for r in LE26))

# --- V03 r64 D01 被 2026 文献独立确证 ------------------------------------
V03_NOTE = (
    'r64 D01 曾判 BOUNDARY：来稿「对 Euler 观测者取 u = n 即违反 WEC」需限定 n 的类时性，'
    '且泡内 f=1 处 n 是零法向量。'
    '外部检索发现该边界裁定已被 2026 年文献**独立形式化并加强**：'
    'Le 2602.18023 摘要原文——「Whether a warp drive metric requires exotic matter '
    'is decided by energy conditions quantified over ALL observers, not only the '
    'Eulerian」，并把 NEC/WEC/SEC 表为 4x4 线性矩阵不等式（经典 S-lemma），'
    'DEC 需两项此类检验；进一步给出动量约束：单位时间膨胀切片上 Euler 动量'
    '与位移矢量涡量相联系，动量恒为零当且仅当位移矢量 = 梯度场 + 刚体转动。'
    '⇒ **r64 D01 从 BOUNDARY 升级为「已被外部文献独立支持」**，'
    '且这是本册与 r64 之间最强的一条跨册互证：r64 凭量纲与逻辑指出的口径缺陷，'
    '在文献侧有对应的严格化工具（warpax）。'
    '附带互证：' + V03a_note +
    '⇒ 来稿 §四 的 WEC 论证（取 Euler 法向）按 2026 标准属**不完整检验**，'
    '虽然其「rho<0 ⇒ 违反 WEC」的结论方向仍成立（负能密度对任何观测者都违反 WEC），'
    '但论证方式已过时。')

CO('V03', 'r64 D01 的 Euler 观测者口径缺陷被 Le 2026 独立确证并形式化',
   V03_NOTE,
   'LE2602=arXiv:2602.18023 | r64 D01 联动 | rho~v_s^2 双路互证')

# --- V04 F02 措辞降级确证 ------------------------------------------------
CTC_TXT = '；'.join('v=%s -> u_thr=%s（<1: %s）' % (fv(v, 4), fv(u, 8), ok)
                   for v, u, ok in CTC_ROWS)
V04_PART1 = (
    'r64 F02 曾判 BOUNDARY：「Hawking 时序保护猜想完全未攻破」是过度陈述，'
    '逻辑上「存在部分构型级结果」即足以否证「完全未攻破」。'
    '外部检索确证该降级：'
    '(1) Everett & Roman, %s（%s）——两个超光速泡在相对速度 u > 2v/(1+v^2) 时'
    '生成闭类时曲线（曲速版时序问题的经典构型级结果，早于 Hawking 1992 之后的'
    '全部讨论）；'
    '(2) Sajeendran & Ralph, arXiv:%s（%s）——在受控旋转 Alcubierre 时空中'
    '构造自由落体观测者回到过去的显式机制；'
    '(3) Bunyaratavej 等, %s（%s）——在具体黑洞时空中重新检验时序保护猜想。'
    '⇒ 措辞应改为「**未完全证明，且已有构型级双向结果**」（既有构造 CTC 的，'
    '也有检验保护机制的）。r64 F02 的降级建议成立。')
V04_PART2 = (
    '机器扫描 CTC 判据阈值（v = 泡速/c）：' + CTC_TXT +
    '。注意 v=1 处阈值恰为 1（阳性对照），v>1 时阈值全部 < 1：'
    '**两个超光速泡只需亚光速的相对速度即可互相生成 CTC**，'
    '这把「时序风险」从边缘情形变成结构性质。')
V04_NOTE = (V04_PART1 % (REFS['EVERETT1997']['journal'],
                         REFS['EVERETT1997']['year'],
                         REFS['SAJEENDRAN2025']['arxiv'],
                         REFS['SAJEENDRAN2025']['year'],
                         REFS['KERRSEN2025']['journal'],
                         REFS['KERRSEN2025']['year'])) + V04_PART2

CO('V04', 'F02 降级确证：时序保护已有构型级双向结果（Everett-Roman / Sajeendran-Ralph 等）',
   V04_NOTE,
   'ctc_thresholds=' + ','.join(fv(u, 6) for _, u, _ in CTC_ROWS))

# --- V05 Krasnikov 归属纠错（本册承重） -----------------------------------
V05_NOTE = (
    '**本册最重要的单项发现：来稿对 Krasnikov 的归属是错误的。**'
    '来稿钥匙 4 写「Krasnikov：负能壳半经典不稳定」。'
    '外部检索定位到 Krasnikov 关于曲速的原始论文：'
    '%s《%s》，%s，arXiv:%s（提交 %04d-%02d）。'
    '该文标题直译即「量子不等式**不禁止**时空捷径」，其摘要明确把 Alcubierre 泡、'
    'Krasnikov 管与虫洞归为一类，并论证**量子不等式不禁止它们**——'
    '这是**许可向**结果，与来稿所述的「不稳定」方向相反。'
    '半经典不稳定性的正确归属是 %s：'
    '%s（%s，DOI %s）与 %s（%s，DOI %s），'
    '以及综述向的 %s（arXiv:%s）。'
    '⇒ 三条裁定：'
    '(a) 来稿钥匙 4 的**引用必须更正**（Krasnikov 2003 不支持「不稳定」 claim）；'
    '(b) 钥匙 4 的**结论方向仍成立**——曲速泡的半经典不稳定性有真实文献支持，'
    '只是作者是 Finazzi/Liberati/Barcelo 而非 Krasnikov；'
    '(c) 更微妙的一层：Krasnikov 的许可向论文与 Finazzi 的限制向论文并存，'
    '说明「量子不等式」与「半经典稳定性」是**两道彼此独立的关卡**——'
    'QI 不禁止（Krasnikov）不等于半经典稳定（Finazzi）。'
    '来稿把两者混为一条「钥匙 4」，属于本库「不同机制并账」缺陷族的又一实例。'
    '极性机检（G3）：Krasnikov 标题含 "do not forbid" = 许可向；'
    'Finazzi 标题含 "unstable" = 限制向 ⇒ 检测器有判别力。'
    % (KR['authors'][0], KR['title'], KR['journal'], KR['arxiv'],
       KR_AX[0], KR_AX[1],
       '、'.join(REFS['FINAZZI2010']['authors']),
       REFS['FINAZZI2010']['title'], REFS['FINAZZI2010']['journal'],
       REFS['FINAZZI2010']['doi'],
       REFS['FINAZZI2010B']['title'], REFS['FINAZZI2010B']['journal'],
       REFS['FINAZZI2010B']['doi'],
       REFS['BARcELO2010']['title'], REFS['BARcELO2010']['arxiv']))

CO('V05', '★承重：来稿「Krasnikov 不稳定」归属错误——Krasnikov 原文是许可向（QI 不禁止）',
   V05_NOTE,
   'krasnikov=%s PRD 67,104013 (do not forbid) | instability=Finazzi/Liberati/Barcelo 2010')

# --- V06 燃料界与转向代价的机器读数 --------------------------------------
V06_NOTE = (
    'Le 2606.22531（v4）给出正能量曲速壳层的转向代价：静止球面上逐次点火给'
    'm_f/m_i = exp(-3L)（L = 速度空间路径长度）。机器扫描：' +
    '；'.join('L=%s -> m_f/m_i=%s' % (fv(L, 2), fv(r, 8)) for L, r in FUEL_ROWS) +
    '。L=1 时只剩 %s（约 %s%%）。'
    '⇒ 即使满足曲面主导能量条件（正能量壳层），**改变速度的代价是指数级的**，'
    '且自相似壳层需要各向异性应力并带有增长的法向模态（稳定性隐患）。'
    '这为 r64/r65 的「不可行」结论补上外部文献的工程侧证据：'
    '正能量路线的障碍不是「不可能转向」，而是「转向按 exp(-3L) 燃烧质量」。'
    '该文同时自留开放项：转弯后的自引力沉降未解决。'
    % (fv(FUEL_AT1, 6), fv(FUEL_AT1 * D(100), 4)))

IN('V06', 'Le 2026 燃料界 exp(-3L)：正能量壳层转向的指数代价（机器扫描）',
   V06_NOTE,
   'fuel=' + ','.join('%s:%s' % (fv(L, 2), fv(r, 8)) for L, r in FUEL_ROWS))

# --- V07 来稿「钥匙 2 纸上已攻破」的推论过度 ------------------------------
V07_NOTE = (
    '综合 V01–V06，来稿把钥匙 2 列为「✅ 纸上已攻破」的推论过度，三处：'
    '(1) **范围**：Fuchs 2024 与 Le 2026 的全部正能量结果都限于**亚光速**；'
    '没有任何正能量解达到 v_s >= c。来稿表格把钥匙 2 与超光速需求并列，'
    '易被读成「正能量已解决一半」。'
    '(2) **边界违背**：Le 2605.25417 对八个经典构造的完整测试显示'
    '能量条件违背集中在源-真空过渡边界——「正能量壳层」在边界处并不正能量。'
    '(3) **可控性**：Le 2606.22531 显示满足 DEC 的转向受 exp(-3L) 燃料界，'
    '且 Bobrick-Martire 早已指出曲速泡「没有任何自然方式改变速度」。'
    '⇒ 正确记账：钥匙 2 = 「**亚光速正能量解确实存在（Fuchs 2024）**」+'
    '「**其完整能量条件自洽性在 2026 年被发现在边界处失效（Le 2605）**」+'
    '「**可控性代价指数级（Le 2606）**」——是「部分存在、边界存疑、操控昂贵」的三段式，'
    '不是「已攻破」。'
    '本项不推翻 r64/r65/r66/r67 的任何结论，只修正来稿钥匙 2 的状态词。')

MI('V07', '来稿「钥匙 2 纸上已攻破」推论过度：亚光速限定 + 边界违背 + 指数操控代价',
   V07_NOTE,
   'subluminal_only=true | boundary_violation=LE2605 | fuel=exp(-3L)')

# --- V08 遗留项清零与流行数字登记 ----------------------------------------
V08_NOTE = (
    'r64 登记的三条外部核实遗留项本册全部闭环：'
    'F01（Fuchs 2024）→ **PASS**（V01）；'
    'F02（时序保护措辞）→ **CORRECTED 且确证**（V04）；'
    'F03（Krasnikov）→ **CORRECTED 且归属纠错**（V05）。'
    '另登记一条不可用作文献读数的流行科学数字：'
    '「Euler 分析漏检约 72% 泡壁 WEC 违反（Rodal 几何）」出自 '
    'freeastroscience.com 的转述而非论文摘要，本册标 **BOUNDARY**：'
    '方向与 Le 2602.18023 的定理一致（Euler 分析不完整），但 72% 这个具体数字'
    '需查论文正文才能引用。按 r66 立下的纪律（比值/倍数读数必须先证量纲与来源），'
    '本册不把它用于任何判定。'
    '⇒ warp-drive 线（r64/r65/r66/r67 + 本册 r200）至此**无未闭环的外部核实项**。')

IN('V08', 'F01/F02/F03 三条 BOUNDARY 全部闭环；流行数字 72% 单独登记为 BOUNDARY',
   V08_NOTE,
   'F01=PASS(V01) | F02=CORRECTED(V04) | F03=CORRECTED(V05) | 72%=BOUNDARY')

BO('V09', '流行转述数字「72% 漏检」不作文献读数（需论文正文核实）',
   POPULAR_CLAIMS[0]['claim'] + '。来源：' + POPULAR_CLAIMS[0]['source'] +
   '。方向与 Le 2602.18023 定理（Euler 分析不完整）一致，但具体数值未核实。'
   '若后续要引用，须查 arXiv:2602.18023 正文中 Rodal 几何的逐点检验表。',
   'unverified=72 | paper=LE2602')

# --- V10 净立场 ------------------------------------------------------------
V10_NOTE = (
    '外部核实对 r64–r67 四册净立场的影响：**加强，不是削弱**。'
    '(1) r64 C01/C04 的「v_s>c 泡内固有时为虚」是数学事实，文献无争议；'
    '(2) r64 D02 的机器预测（正能量泡必非 Alcubierre 型）被 Fuchs 2024 的构造'
    '（物质壳 + 位移矢量，且自证非坐标变换）直接确证；'
    '(3) r64 D01 的 Euler 口径缺陷被 Le 2026 形式化（全部观测者 LMI 判据）；'
    '(4) r64 E03b 的撤回（r66 I03）不受影响——那是量纲问题，与文献无关；'
    '(5) r67 的「五族全关」针对的是 QEI 量纲闭合族，与外部文献两条线'
    '（正能量存在性 / 半经典稳定性）**互不重叠**，仍独立成立。'
    '⇒ 可引用的最终立场（更新版）：'
    '「超光速曲率引擎在 GR 内部结构性不可行：v_s>c 使泡内运动学失去实定义；'
    '唯一定义域内的 v_s→c⁻ 上，QEI 量纲闭合五族中四族被直接排除，'
    '仅存族要求壳厚锁死在 10 ℓ_P 内、宏观泡负能量跳到 10⁶ 倍可观测宇宙质量；'
    '正能量路线（Fuchs 2024 / Le 2026）仅限亚光速，且 2026 年发现其能量条件违背'
    '集中在源-真空边界、转向代价按 exp(-3L) 指数燃烧；'
    '半经典不稳定性的正确文献归属是 Finazzi-Liberati-Barcelo 2010（非 Krasnikov）。」'
    '⇒ 本册对外部文献的唯一实质更正是来稿的 Krasnikov 归属（V05），'
    '对四册结论零更正。')

IN('V10', '净立场：外部核实加强 r64–r67 结论；唯一实质更正是来稿的 Krasnikov 归属',
   V10_NOTE,
   'corrections_to_r64-r67=0 | corrections_to_incoming=1 (V05)')


# =============================================================================
# 主程序
# =============================================================================
def main():
    tally = {}
    for it in ITEMS:
        tally[it['verdict']] = tally.get(it['verdict'], 0) + 1
    order = ['PASS', 'FAIL', 'CORRECTED', 'MISMATCH', 'BOUNDARY', 'INFO']
    tally_txt = ' / '.join('%s=%d' % (k, tally.get(k, 0)) for k in order if k in tally)

    guard('G8-g0-dims', G0_OK, '量纲工具自检（用于 V03a 互证读数）')

    evidence = {
        'refs': {k: {'title': v['title'], 'arxiv': v.get('arxiv'),
                     'journal': v['journal'], 'doi': v.get('doi')}
                 for k, v in REFS.items()},
        'refs_total': len(REFS),
        'fuchs_bibcode_parsed': list(BC) if BC else None,
        'fuchs_arxiv_ym': list(AX),
        'fuchs_claim_matches': V01b_rows,
        'ctc_thresholds': [[fv(v, 4), fv(u, 8), bool(ok)] for v, u, ok in CTC_ROWS],
        'fuel_bounds': [[fv(L, 2), fv(r, 8)] for L, r in FUEL_ROWS],
        'krasnikov_polarity': {'krasnikov_permissive': bool(KR_PERMISSIVE),
                               'finazzi_restrictive': bool(FIN_RESTRICTIVE)},
        'krasnikov_arxiv_ym': list(KR_AX),
        'popular_claims': POPULAR_CLAIMS,
        'incoming_claims_closed': {'F01': 'PASS (V01)', 'F02': 'CORRECTED (V04)',
                                   'F03': 'CORRECTED (V05)'},
    }

    summary = {
        'book': NAME,
        'date': '2026-10-26',
        'lineage': 'r64 (structural) -> r65 (accounting) -> r66 (QEI families) '
                   '-> r67 (survivor closure) -> r200 (external verification)',
        'source_lineage': 'r64 F01/F02/F03 BOUNDARY items',
        'rating': '外部核实轮：来稿引用 2 真 1 误（Krasnikov 归属错）；'
                  '四册结论零更正、净立场加强',
        'item_count': len(ITEMS),
        'tally': {k: tally.get(k, 0) for k in order},
        'tally_text': tally_txt,
        'guards_total': len(GUARD),
        'guards_passed': len([g for g in GUARD if g['ok']]),
        'items': ITEMS,
        'evidence': evidence,
    }

    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    with io.open(os.path.join(OUT, NAME + '.json'), 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(summary, ensure_ascii=False, indent=2))

    L = []
    L.append('# %s' % NAME)
    L.append('')
    L.append('- 日期：2026-10-26')
    L.append('- 承接：r64 F01 / F02 / F03 三条 BOUNDARY（离线不可核实项）')
    L.append('- 方法：外部检索（arXiv / DOI / 期刊卷页三源核对）')
    L.append('')
    L.append('## 汇总')
    L.append('')
    L.append('条目 %d（%s）' % (len(ITEMS), tally_txt))
    L.append('')
    L.append('守卫 %d / %d' % (len([g for g in GUARD if g['ok']]), len(GUARD)))
    L.append('')
    L.append('评级：%s' % summary['rating'])
    L.append('')
    L.append('## 守卫清单')
    L.append('')
    L.append('| 守卫 | 结果 | 说明 |')
    L.append('|---|---|---|')
    for g in GUARD:
        L.append('| %s | %s | %s |' % (g['guard'], 'PASS' if g['ok'] else 'FAIL',
                                       g['note']))
    L.append('')
    L.append('## 条目')
    L.append('')
    for it in ITEMS:
        L.append('### %s · %s · %s' % (it['code'], it['verdict'], it['title']))
        L.append('')
        L.append(it['detail'])
        L.append('')
        if it['evidence']:
            L.append('- 机器读数：`%s`' % it['evidence'])
            L.append('')
    L.append('## 文献登记表')
    L.append('')
    L.append('| key | 文献 | arXiv | 期刊 | DOI |')
    L.append('|---|---|---|---|---|')
    for k, v in REFS.items():
        L.append('| %s | %s | %s | %s | %s |'
                 % (k, v['title'], v.get('arxiv') or '-', v['journal'],
                    v.get('doi') or '-'))
    L.append('')
    with io.open(os.path.join(OUT, NAME + '.md'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(L) + '\n')

    R = []
    R.append('=' * 78)
    R.append(NAME)
    R.append('2026-10-26  |  warp 线外部核实闭环（r64 F01/F02/F03）')
    R.append('=' * 78)
    R.append('条目: %d   %s' % (len(ITEMS), tally_txt))
    R.append('守卫: %d / %d' % (len([g for g in GUARD if g['ok']]), len(GUARD)))
    R.append('评级: %s' % summary['rating'])
    R.append('')
    R.append('-' * 78)
    R.append('守卫')
    R.append('-' * 78)
    for g in GUARD:
        R.append('[%s] %-26s %s' % ('PASS' if g['ok'] else 'FAIL', g['guard'],
                                    g['note']))
    R.append('')
    R.append('-' * 78)
    R.append('条目')
    R.append('-' * 78)
    for it in ITEMS:
        R.append('[%s] %s  %s' % (it['verdict'], it['code'], it['title']))
        R.append('       %s' % it['detail'][:300])
        R.append('')
    R.append('-' * 78)
    R.append('关键读数')
    R.append('-' * 78)
    R.append('Fuchs2024      = arXiv:2405.02709 / CQG 41,095013 / 6 authors / subluminal')
    R.append('LE2026 (x3)    = 2602.18023 / 2605.25417 / 2606.22531 (An T. Le)')
    R.append('Krasnikov      = PRD 67,104013 (2003) "QI do NOT forbid" (permissive!)')
    R.append('Instability    = Finazzi/Liberati/Barcelo 2010 (NOT Krasnikov)')
    R.append('CTC threshold  = u > 2v/(1+v^2)  (v=1 -> 1; v>1 -> all < 1)')
    R.append('Fuel bound     = m_f/m_i = exp(-3L)  (L=1 -> %s)' % fv(FUEL_AT1, 6))
    R.append('')
    with io.open(os.path.join(OUT, NAME + '_report.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(R) + '\n')

    print('=' * 78)
    print(NAME)
    print('条目 %d   %s' % (len(ITEMS), tally_txt))
    print('守卫 %d / %d' % (len([g for g in GUARD if g['ok']]), len(GUARD)))
    print('=' * 78)
    print('外部核实结果:')
    print('  F01 Fuchs2024      : PASS  (CQG 41,095013; subluminal; all energy conditions)')
    print('  F02 chronology     : CORRECTED confirmed (Everett-Roman CTC criterion etc.)')
    print('  F03 Krasnikov      : CORRECTED  <-- mis-attribution in incoming!')
    print('       Krasnikov PRD 67,104013 = "QI do NOT forbid" (permissive)')
    print('       instability  = Finazzi/Liberati/Barcelo 2010')
    print('  LE2026 x3          : 2602.18023 / 2605.25417 / 2606.22531 (tightening!)')
    print('  产物: %s.json / .md / _report.txt' % NAME)
    bad = [g['guard'] for g in GUARD if not g['ok']]
    if bad:
        print('GUARD FAILED: %s' % bad)
        return 1
    print('GUARD ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
