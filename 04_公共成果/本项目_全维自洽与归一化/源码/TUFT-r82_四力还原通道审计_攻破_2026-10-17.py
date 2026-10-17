# -*- coding: utf-8 -*-
"""
r82 · 2026-10-17 · 四力还原通道审计：κ,τ（自旋-0）对四力的还原能力机器判定
==============================================================================
为什么现在做这一册（与 W1/W2 裁决无关，可独立计算）：
  r80 补全的耦合项只给了【κ → 引力】一条通道；来料宣称的「四力统一」中，
  **电磁、弱、强三条通道从未被任何一册检验过**。r78 只问了引力（I02/I07），
  r81 只定价了引力的两条出路。⇒ 本册补上那三条从未被审的通道。

核心机器判据 —— 中介粒子的【自旋】决定相互作用结构：
  spin-0（标量） 耦合到 T 的迹；同号相吸；不需要规范不变；只能阿贝尔
  spin-1（矢量） 耦合到守恒流 J^μ；同号相斥（电磁即此）；必须规范不变；可非阿贝尔
  spin-2（张量） 耦合到 T_{μν}；同号相吸；= GR 的引力
  ⇒ κ,τ 作为曲率/挠率不变量是【洛伦兹标量 ⇒ spin-0】⇒ 只能走 spin-0 通道

  A 组 中介自旋门：κ,τ ⇒ spin-0（决定性前提）
  B 组 电磁门：EM 需 spin-1 + 同号相斥 + U(1) 规范 ⇒ spin-0 三重不符 ⇒ 不可还原
  C 组 弱/强门：需非阿贝尔规范（承 r75 秩门）+ 手征费米子（承 r75 手征门）⇒ 不可还原
  D 组 引力门：通道存在（r80 已补 κ–T）但 spin-0 ⇒ PPN γ=−1 ⇒ 超 Cassini ⇒ 亦未还原
  E 组 四力还原总表 + ★阳性对照（门必须可分辨）
     E2 关键：把「正确中介自旋」代入同一套门 ⇒ 四力全 PASS ⇒ 证明本门不是「什么都判 FAIL」的坏门槛
  F 组 分工与开放项

纪律（承 r64/r67/r71/r74/r75/r78/r80/r81）
 1) ★阳性对照优先：门必须在正确输入下给出 PASS，否则是坏门槛（假红同样是事故）
 2) 不自推系数登记 NS 3) 不改他人文件字节 4) 退出码 0 = 跑完；结论看 counts/verdict
 5) 分工声明先行，零重复（本册只审「四力通道可行性」，不动 r78 耦合定价、不动 r81 W1/W2 定价）
==============================================================================
"""

import sys, os, io, json
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

STEM = 'TUFT-r82_四力还原通道审计_攻破_2026-10-17'

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

CASSINI = D('2.3e-5')

# ----------------------------------------------------------------------------
# 中介自旋剖面 / 四力需求
# ----------------------------------------------------------------------------
SPIN_PROFILE = {
    0: {'name': '标量 spin-0', 'couples': 'T 的迹 T^μ_μ', 'like_sign': -1,
        'needs_gauge': False, 'note': '同号相吸'},
    1: {'name': '矢量 spin-1', 'couples': '守恒流 J^μ', 'like_sign': 1,
        'needs_gauge': True, 'note': '同号相斥（电磁）；可非阿贝尔'},
    2: {'name': '张量 spin-2', 'couples': '能动张量 T_{μν}', 'like_sign': -1,
        'needs_gauge': False, 'note': '同号相吸；即 GR 引力'},
}

# like_sign: -1 相吸 / +1 相斥 / None 不适用（非阿贝尔力无简单同号吸斥）
FORCE_REQ = {
    '引力': {'spin': 2, 'like_sign': -1, 'needs_gauge': False,
             'nonabelian': False, 'chiral': False, 'note': 'GR / spin-2'},
    '电磁': {'spin': 1, 'like_sign': 1, 'needs_gauge': True,
             'nonabelian': False, 'chiral': False, 'note': 'U(1) 规范 / spin-1'},
    '弱':   {'spin': 1, 'like_sign': None, 'needs_gauge': True,
             'nonabelian': True, 'chiral': True, 'note': 'SU(2) 非阿贝尔 + 手征'},
    '强':   {'spin': 1, 'like_sign': None, 'needs_gauge': True,
             'nonabelian': True, 'chiral': False, 'note': 'SU(3) 非阿贝尔'},
}

FORCE_ORDER = ['引力', '电磁', '弱', '强']

def check_channel(spin, force):
    """用同一套门检验：某自旋的中介能否还原某力。返回子项布尔。"""
    p = SPIN_PROFILE[spin]
    r = FORCE_REQ[force]
    res = {}
    res['spin'] = (spin == r['spin'])
    res['sign'] = True if r['like_sign'] is None else (p['like_sign'] == r['like_sign'])
    # 规范：需求为真时中介必须具备规范结构
    res['gauge'] = (not r['needs_gauge']) or p['needs_gauge']
    # 非阿贝尔 / 手征：只有规范矢量（spin-1）能承载
    res['nonabelian'] = (not r['nonabelian']) or (spin == 1)
    res['chiral'] = (not r['chiral']) or (spin == 1)
    res['all'] = all([res['spin'], res['sign'], res['gauge'],
                      res['nonabelian'], res['chiral']])
    return res

def gamma_of_spin(spin):
    """引力通道的 PPN γ：spin-2 ⇒ 1（GR）；spin-0 ⇒ −1（纯标量，承 r78 I07）"""
    return {2: D(1), 0: D(-1)}[spin]

# ----------------------------------------------------------------------------
# G0-* 自守卫（先过守卫再用于判定；含「门必须可分辨」的守卫）
# ----------------------------------------------------------------------------
def G0_guards():
    fails = []
    # G0-1: 自旋剖面完备
    if set(SPIN_PROFILE.keys()) != {0, 1, 2}:
        fails.append('G0-1')
    # G0-2: ★守卫「门不是恒 FAIL」：正确中介自旋下四力必须全 PASS
    for f in FORCE_ORDER:
        if not check_channel(FORCE_REQ[f]['spin'], f)['all']:
            fails.append('G0-2:' + f)
    # G0-3: ★守卫「门不是恒 PASS」：TUFT 的 spin-0 中介下至少有一力 FAIL（实为四力全 FAIL）
    n_fail = sum(0 if check_channel(0, f)['all'] else 1 for f in FORCE_ORDER)
    if n_fail == 0:
        fails.append('G0-3')
    # G0-4: γ 表正确
    if gamma_of_spin(2) != D(1) or gamma_of_spin(0) != D(-1):
        fails.append('G0-4')
    # G0-5: Cassini 比值计算正确
    rat = abs(gamma_of_spin(0) - D(1)) / CASSINI
    if abs(rat - D(2) / CASSINI) > D('1e-40'):
        fails.append('G0-5')
    # G0-6: 电磁的同号相斥确为 +1、引力相吸确为 -1（守卫需求表未被写反）
    if FORCE_REQ['电磁']['like_sign'] != 1 or FORCE_REQ['引力']['like_sign'] != -1:
        fails.append('G0-6')
    if fails:
        raise SystemExit('G0 自守卫失败: ' + ','.join(fails))

# ----------------------------------------------------------------------------
# A 组：中介自旋门
# ----------------------------------------------------------------------------
def group_A():
    entry('A1', 'PASS',
          ('★决定性前提：κ（曲率）与 τ（挠率）是【洛伦兹标量】（无时空指标的不变量）⇒ 中介自旋 = 0。'
           '而自旋决定相互作用结构：spin-0 耦合 T 的迹、同号相吸、无需规范不变；'
           'spin-1 耦合守恒流 J^μ、同号相斥、需规范不变；spin-2 耦合 T_{μν}、即 GR 引力'),
          None, '自旋门前提')
    entry('A2', 'INFO',
          ('自旋剖面表（机器登记）：' +
           '；'.join(SPIN_PROFILE[s]['name'] + '→耦合' + SPIN_PROFILE[s]['couples'] +
                     '、' + SPIN_PROFILE[s]['note'] for s in (0, 1, 2))),
          None, '剖面表')

# ----------------------------------------------------------------------------
# B 组：电磁门
# ----------------------------------------------------------------------------
def group_B():
    c = check_channel(0, '电磁')
    entry('B1', 'FAIL',
          ('★电磁门：电磁力要求 ① 同号**相斥** ② U(1) 规范不变性 ③ spin-1 媒介 A_μ 耦合守恒流 J^μ。'
           'τ 是 spin-0 ⇒ 自旋不符(' + str(c['spin']) + ')、同号相斥不符(' + str(c['sign']) +
           ')、规范结构不符(' + str(c['gauge']) + ') ⇒ **三重结构性不符**'),
          None, '电磁不可还原')
    entry('B2', 'FAIL',
          ('★符号硬伤：标量交换势 V ∝ −g²/r 对同号**相吸**；电磁同号电荷 V ∝ +e²/r **相斥** ⇒ '
           '符号相反。这不是参数调不调的问题，而是**自旋选错了通道**（标量永远给吸引，给不出静电排斥）'),
          None, '结构性不符，非参数问题')

# ----------------------------------------------------------------------------
# C 组：弱 / 强门
# ----------------------------------------------------------------------------
def group_C():
    cw = check_channel(0, '弱')
    cs = check_channel(0, '强')
    entry('C1', 'FAIL',
          ('★弱门：弱作用需 SU(2) 非阿贝尔规范(' + str(cw['nonabelian']) +
           ') + **手征费米子**（左手二重态）(' + str(cw['chiral']) +
           ')。spin-0 标量既无规范群结构也无旋量/手征结构 ⇒ 两条必要件均不成立（承 r75 秩门与手征门）'),
          None, '弱不可还原')
    entry('C2', 'FAIL',
          ('★强门：强作用需 SU(3) 非阿贝尔规范(' + str(cs['nonabelian']) +
           ')、秩 2。TUFT 无任何规范群结构 ⇒ 不成立（承 r75 秩门：SM 需秩 4，TUFT 的 κ,τ 两条原语达不到）'),
          None, '强不可还原')

# ----------------------------------------------------------------------------
# D 组：引力门
# ----------------------------------------------------------------------------
def group_D():
    c = check_channel(0, '引力')
    g0 = gamma_of_spin(0)
    rat = abs(g0 - D(1)) / CASSINI
    entry('D1', 'FAIL',
          ('★引力门：引力通道确实存在（r80 已补全 κ–T 耦合），且 spin-0 的「同号相吸」符号是对的(' +
           str(c['sign']) + ')。但中介自旋不符：引力需 spin-2，TUFT 给的是 spin-0(' + str(c['spin']) +
           ') ⇒ PPN γ = ' + str(g0) + '（承 r78 I07）⇒ |γ−1| = 2 超 Cassini 限 ' + str(rat) +
           ' 倍 ⇒ **引力亦未还原成功**（承 r78 I07 / r80 E1）'),
          str(rat), '引力通道：符号对但自旋错')

# ----------------------------------------------------------------------------
# E 组：四力还原总表 + ★阳性对照
# ----------------------------------------------------------------------------
def group_E():
    rows = []
    n_ok = 0
    for f in FORCE_ORDER:
        c = check_channel(0, f)
        ok = c['all']
        if ok:
            n_ok += 1
        sub = '自旋' + ('✓' if c['spin'] else '✗') + ' 符号' + ('✓' if c['sign'] else '✗') + \
              ' 规范' + ('✓' if c['gauge'] else '✗') + ' 非阿贝尔' + ('✓' if c['nonabelian'] else '✗') + \
              ' 手征' + ('✓' if c['chiral'] else '✗')
        rows.append(f + '[' + ('PASS' if ok else 'FAIL') + '] ' + sub)
    entry('E1', 'FAIL',
          ('★四力还原总表（TUFT 的 spin-0 中介）：' + '；'.join(rows) +
           ' ⇒ **还原成功 ' + str(n_ok) + '/4**'),
          None, '四力还原 = 0/4')

    # ★阳性对照：正确中介自旋代入同一套门
    ctrl = []
    n_ctrl_ok = 0
    for f in FORCE_ORDER:
        c = check_channel(FORCE_REQ[f]['spin'], f)
        if c['all']:
            n_ctrl_ok += 1
        ctrl.append(f + '(需 spin-' + str(FORCE_REQ[f]['spin']) + ')⇒' + ('PASS' if c['all'] else 'FAIL'))
    entry('E2', 'PASS',
          ('★阳性对照（门必须可分辨）：把每力**应有的正确中介自旋**代入同一套门 ⇒ ' +
           '；'.join(ctrl) + ' ⇒ 四力全 PASS（' + str(n_ctrl_ok) + '/4）。'
           '⇒ 本门在正确输入下给 PASS、在 TUFT 的 spin-0 下给 FAIL ⇒ **不是恒 FAIL 的坏门槛**，'
           'E1 的 0/4 是真实判据结果而非机器假红'),
          None, '★防假红：门有分辨力')

    entry('E3', 'FAIL',
          ('★元结论：来料宣称的「四力统一」，在补全耦合项（r80）之后经本册通道审计 ⇒ '
           '**四力还原 0/4**：引力（自旋错 ⇒ γ=−1 被排除）、电磁（自旋/符号/规范三重不符）、'
           '弱（无非阿贝尔+手征）、强（无非阿贝尔）。'
           '根因只有一条：κ,τ 是**自旋-0 标量**，而四力需要 spin-2(引力) + spin-1 规范(电磁/弱/强) 三种通道'),
          None, '根因归结')

# ----------------------------------------------------------------------------
# F 组：分工与开放项
# ----------------------------------------------------------------------------
def group_F():
    entry('F1', 'INFO',
          ('分工声明（零重复）：r78 只审引力耦合门票与弱场（I02/I07）；r80 补全 `𝓛_int` 形式/符号/归一化；'
           'r81 只定价 W1/W2 两条引力出路。**本册首次检验电磁/弱/强三条通道**（此前无任何一册审过），'
           '并把它与引力通道放在同一自旋门下汇总 ⇒ 与 r78/r80/r81 对象不同、结论互补'),
          None, '分工')
    entry('F2', 'INFO',
          ('开放项新增：`X-R82-1`（若要还原电磁，必须把 τ 从标量升级为 **spin-1 规范场 A_μ** ⇒ '
           '已改变 τ 的几何原语定义，等价于新增一个 U(1) 规范扇区，代价须另册定价）；'
           '`X-R82-2`（弱/强需非阿贝尔规范 + 手征费米子 ⇒ 属 r75 秩门/手征门的延续，非本册可闭环）。'
           '`X-R76-2`（W1 vs W2）仍待用户裁决'),
          None, '开放项')

# ----------------------------------------------------------------------------
# payload 与输出
# ----------------------------------------------------------------------------
def build_payload():
    verdict = 'FAIL' if COUNTS.get('FAIL', 0) > 0 else (
        'BOUNDARY' if COUNTS.get('BOUNDARY', 0) > 0 else 'PASS')
    meta = ('四力还原 = 0/4：κ,τ 是自旋-0 标量，而四力需要 spin-2(引力) + spin-1 规范(电磁/弱/强)；'
            '本门经阳性对照验证有分辨力（正确自旋 ⇒ 4/4 PASS），故 0/4 是真实判据结果')
    return {
        'round': 'r82',
        'date': '2026-10-17',
        'source': '来料「四力统一」宣称 · 承 r75 秩门/手征门、r78 耦合门票、r80 耦合项补全、r81 W1/W2 定价',
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
            {'tag': 'NS1', 'text': '「标量交换同号相吸、矢量交换同号相斥、张量(GR)相吸」为量子场论教科书结论，引用不自推'},
            {'tag': 'NS2', 'text': '电磁需 U(1) 规范不变与 spin-1 媒介、弱需 SU(2)+手征、强需 SU(3) 为 SM 标准结论，引用不自推'},
            {'tag': 'NS3', 'text': 'Cassini |γ−1|<2.3×10⁻⁵ 为外部实验事实；γ=−1 属纯标量(Nordström 型)结论，承 r78 NS1/NS2'},
            {'tag': 'NS4', 'text': '「κ,τ 为曲率/挠率不变量 ⇒ 洛伦兹标量 ⇒ spin-0」为定义推论；其能否被重新诠释为其他自旋，本册不代判'},
            {'tag': 'NS5', 'text': '把 τ 升级为 spin-1 规范场的可行性与其代价本册只登记开放项，不建模不自推'},
        ],
        'red_line': '数学/数值自洽 != 物理证实。本册只做四力通道的可行性审计，不产生新物理；'
                    '「κ,τ 的 spin-0 通道还原不了四力」不等于「TUFT 方向被否证」——'
                    '若改用其他自旋/规范扇区（X-R82-1/X-R82-2）则不属本册结论范围',
    }

def write_outputs(payload):
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    verdict = payload['verdict']
    jp = os.path.join(DATA, STEM + '.json')
    with io.open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rl = ['TUFT-r82 四力还原通道审计 运行报告',
          'counts=' + str(payload['counts']) + ' total=' + str(payload['total']) + ' verdict=' + verdict,
          'meta=' + payload['meta_verdict']]
    for e in ENTRIES:
        rl.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rl.append('    residual=' + e['residual'])
    rl.append('')
    rl.append('GUARD G0: 自守卫全过（含 G0-2 门必须可分辨 / G0-3 门非恒 PASS）')
    rl.append('GENERATED_AT=' + payload['generated_at'])
    rl.append('MODULE=' + payload['module'])
    rp = os.path.join(DATA, STEM + '_report.txt')
    with io.open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rl))

    ml = ['# ' + STEM, '', '日期：2026-10-17 · 四力还原通道审计（κ,τ 自旋-0）', '',
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
    lines = ['# 判定_TUFT-r82-四力还原通道审计_攻破_2026-10-17', '',
             '日期：2026-10-17 · **首次检验电磁/弱/强三条通道**（此前 r78/r80/r81 只审引力）', '',
             '## 一、为什么现在做',
             'r80 补全的耦合项只给了【κ → 引力】一条通道；来料宣称的「四力统一」中，'
             '**电磁、弱、强从未被任何一册检验**。本册补上这三条，并与引力放在同一自旋门下汇总。', '',
             '## 二、决定性前提',
             'κ（曲率）与 τ（挠率）是**洛伦兹标量 ⇒ 自旋 0**。而中介自旋决定相互作用结构：', '',
             '| 中介 | 耦合对象 | 同号作用 | 规范不变 |',
             '|---|---|---|---|',
             '| spin-0 标量 | T 的迹 | **相吸** | 不需要 |',
             '| spin-1 矢量 | 守恒流 J^μ | **相斥** | 需要 |',
             '| spin-2 张量 | T_{μν} | **相吸** | 不需要（= GR） |', '',
             '## 三、四力还原结果（TUFT 的 spin-0 中介）', '',
             '| 力 | 所需通道 | 判据子项 | 结论 |',
             '|---|---|---|---|']
    for f in FORCE_ORDER:
        c = check_channel(0, f)
        sub = '自旋' + ('✓' if c['spin'] else '✗') + ' 符号' + ('✓' if c['sign'] else '✗') + \
              ' 规范' + ('✓' if c['gauge'] else '✗') + ' 非阿贝尔' + ('✓' if c['nonabelian'] else '✗') + \
              ' 手征' + ('✓' if c['chiral'] else '✗')
        lines.append('| ' + f + ' | ' + FORCE_REQ[f]['note'] + ' | ' + sub +
                     ' | **' + ('PASS' if c['all'] else 'FAIL') + '** |')
    lines += ['', '**四力还原 = 0/4。**', '',
              '## 四、★阳性对照（门必须可分辨）',
              '把每力**应有的正确中介自旋**代入同一套门：']
    for f in FORCE_ORDER:
        c = check_channel(FORCE_REQ[f]['spin'], f)
        lines.append('- ' + f + '（需 spin-' + str(FORCE_REQ[f]['spin']) + '）⇒ **' +
                     ('PASS' if c['all'] else 'FAIL') + '**')
    lines += ['', '⇒ 四力在正确中介下**全 PASS** ⇒ 本门在正确输入给 PASS、在 TUFT 的 spin-0 给 FAIL，'
              '**不是恒 FAIL 的坏门槛**，故 0/4 是真实判据结果而非机器假红。', '',
              '## 五、根因与开放项',
              '- **根因只有一条**：κ,τ 是自旋-0 标量，而四力需要 spin-2（引力）+ spin-1 规范（电磁/弱/强）三种通道。',
              '- `X-R82-1`：若要还原电磁，须把 τ 从标量升级为 **spin-1 规范场 A_μ** ⇒ 已改变 τ 的几何原语定义'
              '（等价于新增 U(1) 规范扇区，代价须另册定价）。',
              '- `X-R82-2`：弱/强需非阿贝尔规范 + 手征费米子（承 r75 秩门/手征门），非本册可闭环。',
              '- `X-R76-2`（W1 vs W2）仍待用户裁决。', '',
              '## 六、条目', '- 总条目 ' + str(payload['total']) + '：' + str(payload['counts']),
              '- 总体 verdict：**' + payload['verdict'] + '**']
    for e in ENTRIES:
        lines.append('- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text'])
    lines += ['', '## 七、不自推登记']
    for n in payload['not_self_derived']:
        lines.append('- ' + n['tag'] + '：' + n['text'])
    lines += ['', '## 八、治理',
              '未改动任何他人文件字节；未跑 `refresh_catalog`（并发回退风险）；未做 git 操作。', '',
              '## 九、红线', payload['red_line'], '',
              'GENERATED_AT=' + payload['generated_at'], 'MODULE=' + payload['module']]
    jb = os.path.join(BASE, '判定_TUFT-r82-四力还原通道审计_攻破_2026-10-17.md')
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
