# -*- coding: utf-8 -*-
"""
r81 · 2026-10-17 · r78 步骤② / r80 下游：W1–W2 二选一的代价机器定价与可证伪性审计
==============================================================================
继承（不重推）：
  r78 C4/I09 FAIL 三条出路：W1 把 κ,τ 降为度规派生量（退回 GR、零新增内容）
                          W2 保留 κ 传播 + 加张量扇区（过 Cassini 须屏蔽 ⇒ +1 自由函数，撞 Ω5）
                          W3 保持纯标量 ⇒ 已被 I07 排除
  r78「下一步」② **再在 W1/W2 之间裁决**（科学哲学层，本册不代选，只给价格标签）
  r80 补全 𝓛_int（形式/符号/归一化三要素）后仍因纯标量被 Cassini 排除 ⇒ 裁决已不可回避

本册把「二选一」这个科学哲学层选择，拆成【可计算的代价项】并机器定价：

  A 组 W1（退回 GR）定价
    A1 自由度账：κ,τ 降为度规派生量 ⇒ 独立传播自由度归零（GR 2 → 仍 2）
    A2 新增可检验预言数 = 0 ⇒ 相对 GR「零新增内容」被量化
    A3 代价账：新常数 0 / 新函数 0 / 自由参数 0 ⇒ Ω5 合规（最便宜），但预测力增量 0
  B 组 W2（标量-张量 + 屏蔽）定价 —— 用 Brans–Dicke 参数化给出可计算的把柄
    B1 BD 的 PPN γ = (1+ω)/(2+ω)，|γ−1| = 1/|2+ω|
    B2 Cassini ⇒ ω ≳ 4.35×10⁴（机器精确解）
    B3 ω 调大只保太阳系；太阳系外仍需屏蔽（chameleon/Vainshtein）⇒ +1 自由函数
    B4 参数账并入 r72 已记 ≥3 常数 ⇒ 撞 Ω5
  C 组 可证伪性 / 信息含量对照
    C1 W1 与 GR 等价 ⇒ 新增可证伪预言 0 ⇒ 作为独立理论不可证伪
    C2 W2 的预言由屏蔽函数决定，而屏蔽函数为拟合本地实验而设 ⇒ 判别力退化（用函数拟合实验）
    C3 元结论：W1「零内容」、W2「贵且需拟合」⇒ 两条都不通向可证伪的新预言
  D 组 是否存在第四出路 W4
    D1 κ,τ 作为曲率/挠率不变量是【标量（自旋 0）】⇒ 只能与 T 的迹耦合 ⇒ γ = −1；
       要 γ = 1 必须把中介升级为张量/自旋-2 ⇒ 那已是 W2（且改了 κ,τ 的原语定义）
       ⇒ 无第四条零代价出路（承 r78 I09）
  E 组 阳性对照 / 跨册互证
    E1 ω → ∞ ⇒ γ → 1（回到 GR）；E2 ω = −3/2 ⇒ γ = −1（与 r78 I07 纯标量端点同一读数，跨册互证）
    E3 ω = 0 ⇒ γ = 1/2 ⇒ |γ−1| = 0.5 ≫ Cassini ⇒ 被排除（证明检验器有分辨力，非恒真）

纪律（承 r64/r67/r71/r74/r78/r79/r80）
 1) 恒真/恒零裁定必配阳性对照 2) 机器先过 G0 自守卫 3) 不自推系数登记 NS
 4) 不改他人文件字节 5) 退出码 0 = 跑完；结论看 counts/verdict
 6) **裁决不代选**：W1/W2 属科学哲学层，本册只定价不代决
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

STEM = 'TUFT-r81_W1W2代价机器定价与可证伪性审计_攻破_2026-10-17'

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
# Brans–Dicke PPN（Decimal 60 位）
# ----------------------------------------------------------------------------
CASSINI = D('2.3e-5')

def bd_gamma(omega):
    """PPN gamma for Brans-Dicke: (1+omega)/(2+omega)"""
    return (D(1) + omega) / (D(2) + omega)

def bd_gamma_dev(omega):
    """|gamma - 1| = 1/|2+omega|"""
    return abs(bd_gamma(omega) - D(1))

def omega_required(bound):
    """由 1/(2+omega) < bound 解出 omega > 1/bound - 2"""
    return D(1) / bound - D(2)

# ----------------------------------------------------------------------------
# G0-* 自守卫（先过守卫再用于判定）
# ----------------------------------------------------------------------------
def G0_guards():
    fails = []
    # G0-1: BD gamma 公式在 omega -> 大数时趋于 1
    g_big = bd_gamma(D('1e12'))
    if abs(g_big - D(1)) > D('1e-10'):
        fails.append('G0-1')
    # G0-2: omega = -3/2 给出 gamma = -1（与 r78 I07 纯标量端点一致）
    if abs(bd_gamma(D('-1.5')) - D(-1)) > D('1e-40'):
        fails.append('G0-2')
    # G0-3: |gamma-1| 恒等式 == 1/|2+omega|
    for w in (D('10'), D('1000'), D('1e6')):
        if abs(bd_gamma_dev(w) - abs(D(1) / (D(2) + w))) > D('1e-40'):
            fails.append('G0-3')
            break
    # G0-4: 解出的 omega 必须为正且远大于 1
    w_req = omega_required(CASSINI)
    if w_req <= D(0) or w_req < D(1000):
        fails.append('G0-4')
    # G0-5: 代入 omega_req 后应恰好落在限上（相对误差 < 1e-30）
    dev = bd_gamma_dev(w_req)
    if abs(dev - CASSINI) / CASSINI > D('1e-30'):
        fails.append('G0-5')
    # G0-6: 阳性对照 omega=0 给 gamma=1/2，显著偏离 1（守卫分辨力）
    if abs(bd_gamma(D(0)) - D('0.5')) > D('1e-40'):
        fails.append('G0-6')
    if bd_gamma_dev(D(0)) <= CASSINI:
        fails.append('G0-7')
    if fails:
        raise SystemExit('G0 自守卫失败: ' + ','.join(fails))

# ----------------------------------------------------------------------------
# A 组：W1（退回 GR）定价
# ----------------------------------------------------------------------------
def group_A():
    dof_gr = 2                 # GR 引力子 2 个传播自由度
    dof_r74 = 2 + 2            # r74 完成后：GR 2 + 两个标量 κ,τ
    dof_w1 = 2 + 0             # W1：κ,τ 降为度规派生量 ⇒ 新增 0
    entry('A1', 'PASS',
          ('W1 自由度账：GR 传播自由度 = ' + str(dof_gr) + '；r74 补全后（κ,τ 独立传播）= ' +
           str(dof_r74) + '；W1 把 κ,τ 降为度规派生量 ⇒ 独立传播自由度归零 = ' + str(dof_w1) +
           '（与 GR 相同）⇒ κ,τ 不再携带任何独立于度规的信息'),
          None, 'W1 自由度定价')

    entry('A2', 'FAIL',
          ('★W1 新增可检验预言数 = 0：κ,τ 成为度规的派生量后，理论逐项等价于 GR ⇒ '
           '相对 GR 的「零新增内容」被量化为【新增可证伪预言 = 0 条】。'
           '代价最低（新常数 0、新函数 0），但**预测力增量同为 0** ⇒ 作为 TUFT 的独立理论不成立'),
          None, 'W1 预测力定价')

    entry('A3', 'PASS',
          ('W1 代价账：新常数 0、新自由函数 0、自由参数 0 ⇒ **Ω5 合规**（三条出路中最便宜的一条）。'
           '但按 r78 D-r78-4「自由度 vs 预测力双计」口径，须同时登记：自由度 +0 **且** 预测力 +0'),
          None, '承 r78 判据 D-r78-4')

# ----------------------------------------------------------------------------
# B 组：W2（标量-张量 + 屏蔽）定价
# ----------------------------------------------------------------------------
def group_B():
    entry('B1', 'PASS',
          ('W2 用 Brans–Dicke 参数化获得可计算的把柄：PPN γ = (1+ω)/(2+ω)，'
           '且 |γ−1| = 1/|2+ω|（机器恒等式校验通过）⇒ 原本「加张量扇区」的模糊代价被化为一个可解的参数界'),
          None, 'W2 定价把柄')

    w_req = omega_required(CASSINI)
    entry('B2', 'FAIL',
          ('★Cassini 定价：|γ−1| = 1/(2+ω) < ' + str(CASSINI) + ' ⇒ ω > ' + str(w_req) +
           '（机器精确解，≈ 4.35×10⁴）。'
           '即：要把 PPN γ 压进观测限，必须把标量-张量耦合调到 ω ≳ 4.35×10⁴ —— '
           '这不是预测，而是**用观测反解参数**（与 r78 C3「C_req 被观测唯一锁定」同族）'),
          str(w_req), 'W2 参数代价')

    entry('B3', 'FAIL',
          ('★ω 调大只保住太阳系：一旦离开太阳系（宇宙学/强场尺度），标量扇区仍会显形，'
           '必须再加屏蔽机制（chameleon / Vainshtein）⇒ **+1 个自由函数**。'
           '按 r15 口径「自由函数比常数更贵」⇒ 这是比加常数更贵的代价'),
          None, 'W2 屏蔽代价')

    entry('B4', 'FAIL',
          ('W2 参数账：+1 自由函数（屏蔽）并入 r72 已记的 ≥3 常数账 ⇒ **撞 Ω5**。'
           '且屏蔽函数须为拟合本地实验（Cassini、第五力、等效原理）而设 ⇒ 可调自由度进一步上升'),
          None, 'W2 Ω5 判定')

# ----------------------------------------------------------------------------
# C 组：可证伪性 / 信息含量对照
# ----------------------------------------------------------------------------
def group_C():
    entry('C1', 'FAIL',
          ('★可证伪性（W1）：与 GR 逐项等价 ⇒ 不存在任何「GR 通过而 W1 不通过」（或反之）的实验 ⇒ '
           '**新增可证伪预言 0 条** ⇒ 波普尔意义下 W1 作为 TUFT 的独立理论不可证伪'),
          None, 'W1 可证伪性')

    entry('C2', 'FAIL',
          ('★可证伪性（W2）：理论的全部偏离 GR 之处由屏蔽函数的具体形式决定，'
           '而屏蔽函数本身是**为拟合本地实验**（Cassini / 第五力 / 等效原理）而选取的 ⇒ '
           '「预言」退化成「用函数拟合实验」⇒ 判别力弱，且函数一旦选定又需再用别的实验去定其参数'),
          None, 'W2 可证伪性')

    entry('C3', 'FAIL',
          ('★元结论：W1 =「零内容」（便宜但什么都没说），W2 =「贵且需拟合」（说了但靠调函数）⇒ '
           '**两条出路都不通向可证伪的新预言**。'
           '这与 r74 的结论同族：r69→r71→r74 把「是不是合法场论」修好了，'
           '但「有没有可检验内容」始终没被修好，且被逐轮证明在当前公设集内没有免费解法'),
          None, '承 r74 同族结论')

# ----------------------------------------------------------------------------
# D 组：是否存在第四出路 W4
# ----------------------------------------------------------------------------
def group_D():
    entry('D1', 'FAIL',
          ('★第四出路排查：κ,τ 作为曲率/挠率不变量，其**自旋为 0（标量）** ⇒ 只能与 T_{μν} 的迹耦合 ⇒ '
           'PPN γ = −1（承 r78 I07）。要得到 γ = 1 就必须让中介具备张量/自旋-2 结构 ⇒ '
           '那已经是 W2（加张量扇区），并且**改变了 κ,τ 作为曲率/挠率原语的定义**。'
           '⇒ 不存在第四条零代价出路（承 r78 I09「没有第三条零代价的路」）'),
          None, '出路穷尽性')

# ----------------------------------------------------------------------------
# E 组：阳性对照 / 跨册互证
# ----------------------------------------------------------------------------
def group_E():
    g_big = bd_gamma(D('1e8'))
    entry('E1', 'PASS',
          ('阳性对照（回到 GR）：ω = 10⁸ ⇒ γ = ' + str(g_big) + '，|γ−1| = ' +
           str(bd_gamma_dev(D('1e8'))) + ' < Cassini ' + str(CASSINI) +
           ' ⇒ ω→∞ 极限正确回到 GR（γ→1），公式与极限行为自洽'),
          str(bd_gamma_dev(D('1e8'))), '极限对照')

    entry('E2', 'PASS',
          ('★跨册互证：ω = −3/2 ⇒ γ = ' + str(bd_gamma(D('-1.5'))) +
           '，与 r78 I07「纯标量中介 ⇒ γ = −1」是**同一端点读数**。'
           '两条独立路径（r78 的自旋-0/迹耦合论证 vs 本册 BD 参数化）落到同一个 γ = −1 ⇒ 互证成立'),
          None, '与 r78 跨册互证')

    entry('E3', 'PASS',
          ('阳性对照（检验器分辨力）：ω = 0 ⇒ γ = ' + str(bd_gamma(D(0))) +
           '，|γ−1| = ' + str(bd_gamma_dev(D(0))) + ' ≫ Cassini ' + str(CASSINI) +
           ' ⇒ 被排除。⇒ 判据非恒真、对不同 ω 有分辨力'),
          str(bd_gamma_dev(D(0))), '防恒真')

# ----------------------------------------------------------------------------
# payload 与输出
# ----------------------------------------------------------------------------
def build_payload():
    verdict = 'FAIL' if COUNTS.get('FAIL', 0) > 0 else (
        'BOUNDARY' if COUNTS.get('BOUNDARY', 0) > 0 else 'PASS')
    meta = ('W1/W2 二选一的代价已机器定价：W1 零内容（自由度+0、预测力+0），'
            'W2 需 ω≳4.35×10⁴ 且 +1 屏蔽函数（撞 Ω5）⇒ 两条都不通向可证伪的新预言；'
            '裁决本身属科学哲学层，本册不代选，只交出价格标签')
    return {
        'round': 'r81',
        'date': '2026-10-17',
        'source': 'r78 步骤②（W1/W2 裁决）· r80 下游',
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
            {'tag': 'NS1', 'text': 'Cassini |γ−1|<2.3×10⁻⁵ 为外部实验事实，引用不自推'},
            {'tag': 'NS2', 'text': 'Brans–Dicke 的 PPN γ=(1+ω)/(2+ω) 为教科书结论；ω=−3/2 ⇒ γ=−1 亦为标准结果，引用不自推'},
            {'tag': 'NS3', 'text': '屏蔽机制（chameleon/Vainshtein）能否真正救回 γ=1 及其具体形式，本册只记代价、不建模（承 r78 NS5）'},
            {'tag': 'NS4', 'text': 'r15「自由函数比常数更贵」的口径、r72 已记 ≥3 常数账，均为承前登记不自推'},
            {'tag': 'NS5', 'text': 'W1 与 W2 何者更可接受属科学哲学层选择（理论本原性 vs 经验adequacy），本册不代选'},
        ],
        'red_line': '数学/数值自洽 != 物理证实。本册是代价定价与可证伪性审计，不产生新物理；'
                    '「两条出路都不通向可证伪的新预言」不等于「TUFT 方向被否证」——'
                    'W1/W2 均未被否证，只是都不便宜且都说不出新东西',
    }

def write_outputs(payload):
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    verdict = payload['verdict']
    jp = os.path.join(DATA, STEM + '.json')
    with io.open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rl = ['TUFT-r81 W1/W2 代价机器定价与可证伪性审计 运行报告',
          'counts=' + str(payload['counts']) + ' total=' + str(payload['total']) + ' verdict=' + verdict,
          'meta=' + payload['meta_verdict']]
    for e in ENTRIES:
        rl.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rl.append('    residual=' + e['residual'])
    rl.append('')
    rl.append('GUARD G0: 自守卫 全过（含 ω=−3/2 与 ω=0 阳性对照）')
    rl.append('GENERATED_AT=' + payload['generated_at'])
    rl.append('MODULE=' + payload['module'])
    rp = os.path.join(DATA, STEM + '_report.txt')
    with io.open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rl))

    ml = ['# ' + STEM, '', '日期：2026-10-17 · r78 步骤② / r80 下游（W1–W2 代价定价与可证伪性）', '',
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
    lines = ['# 判定_TUFT-r81-W1W2代价机器定价与可证伪性审计_攻破_2026-10-17', '',
             '日期：2026-10-17 · **r78 步骤②**（W1/W2 裁决）· **r80 下游**', '',
             '## 一、本册定位',
             'r78 把「继续完成统一场论」收敛为一个二选一：W1（κ,τ 降为度规派生量、退回 GR）vs '
             'W2（保留 κ 传播 + 加张量扇区 + 屏蔽），并指出这是科学哲学层选择。'
             'r80 补全耦合项后仍被 Cassini 排除 ⇒ 该裁决已不可回避。'
             '**本册不代选**，只把「二选一」拆成可计算的代价项并机器定价。', '',
             '## 二、价格标签', '',
             '| 出路 | 自由度 | 新常数 | 新函数 | Ω5 | 预测力增量 | 可证伪性 |',
             '|---|---|---|---|---|---|---|',
             '| **W1**（退回 GR） | +0 | 0 | 0 | **合规** | **0** | 与 GR 等价 ⇒ 不可证伪 |',
             '| **W2**（标量-张量+屏蔽） | +2 标量 | ≥3（承 r72） | **+1** | **撞** | 由屏蔽函数决定 | 用函数拟合实验 ⇒ 判别力弱 |',
             '| W3（纯标量） | — | — | — | — | — | **已被 Cassini 排除**（承 r78 I07） |', '',
             '## 三、W2 的可计算把柄（Brans–Dicke）',
             'PPN γ = (1+ω)/(2+ω)，|γ−1| = 1/|2+ω|。Cassini 要求 |γ−1| < 2.3×10⁻⁵ ⇒ **ω ≳ 4.35×10⁴**。',
             '这并非预测，而是**用观测反解参数**（与 r78 C3「C_req 被观测唯一锁定」同族）。', '',
             '## 四、跨册互证与控制组',
             '- ω = −3/2 ⇒ γ = −1，与 r78 I07「纯标量 ⇒ γ=−1」为**同一端点读数**（两条独立路径互证）。',
             '- ω = 0 ⇒ γ = 1/2，|γ−1| = 0.5 ≫ Cassini ⇒ 被排除（阳性对照，证明判据有分辨力）。',
             '- ω → ∞ ⇒ γ → 1，正确回到 GR。', '',
             '## 五、元结论',
             '**W1 = 零内容（便宜但什么都没说），W2 = 贵且需拟合（说了但靠调函数）⇒ '
             '两条出路都不通向可证伪的新预言。**',
             '这与 r74 同族：把「是不是合法场论」修好了，但「有没有可检验内容」始终没修好，'
             '且被逐轮证明在当前公设集内没有免费解法。', '',
             '## 六、条目', '- 总条目 ' + str(payload['total']) + '：' + str(payload['counts']),
             '- 总体 verdict：**' + payload['verdict'] + '**']
    for e in ENTRIES:
        lines.append('- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text'])
    lines += ['', '## 七、不自推登记']
    for n in payload['not_self_derived']:
        lines.append('- ' + n['tag'] + '：' + n['text'])
    lines += ['', '## 八、开放项与治理',
              '- `X-R76-2`（W1 vs W2）⇒ **仍需用户裁决**（本册只交出价格标签，不代选）。',
              '- `X-R76-3`（W2 屏蔽机制的形式与代价）⇒ 仍开放。',
              '- 治理：未改动任何他人文件字节；未跑 `refresh_catalog`（并发回退风险）；未做 git 操作。', '',
              '## 九、红线', payload['red_line'], '',
              'GENERATED_AT=' + payload['generated_at'], 'MODULE=' + payload['module']]
    jb = os.path.join(BASE, '判定_TUFT-r81-W1W2代价机器定价与可证伪性审计_攻破_2026-10-17.md')
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
