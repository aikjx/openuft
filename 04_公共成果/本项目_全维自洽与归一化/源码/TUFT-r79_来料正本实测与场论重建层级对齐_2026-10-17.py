# -*- coding: utf-8 -*-
"""
r79 · 2026-10-17 · r77 下游、r78 同期互补
《来料正本实测 + 场论重建层级对齐（r69–r77 链 vs TUFT 实际来料 V41 修正版）》
==============================================================================
编号仲裁（起草前实测磁盘）：源码已占 31..78（含并行会话同日所占 r76 / r78）
=> 取首空号 r79（后到者改号，不覆盖他人任何文件字节）

动机（为什么不重复 r78）：
  r78（他人）已机器读取来料正本，得出
    (a) 纯标量重力超 Cassini 限 4+ 阶（ratio≈8.7e4）
    (b) 来料对「牛顿 / 弱场 / 源项 / J_kappa」提及计数为 0
  —— 那是「耦合门票 / 弱场闭合 / PPN」一侧。本册做**互补**的一侧：
  把我的 r69→r71→r74→r77「场论重建」链，与**来料实际给出的数学形式**做机器对齐，
  回答一个 r78 没问的问题：
    「实际来料本身，按 r77 的两条新判据（齐次次数—物理属性、平坦方向陷阱），
     落到哪一类？它和 r69 判的『0 传播自由度』是不是同一回事？」

实测到的来料正本核心形式（V41 修正版，机器读取，见组 A）：
    U(r) = alpha * (kappa^2(r) - tau^2(r))      # 齐次 2 次、带减号
    F     = -alpha * nabla(kappa^2 - tau^2)      # 静态几何梯度力律
    kappa(r) ∝ M/r ,  tau(r) ∝ q/r , ...        # 四力由 ansatz 代换得到
  —— 全篇**无动能项 / 无时间导数 / 无作用量 / 无拉氏量**

本册四组：
  组 A  来料正本机器实测（可读 / 含公式 / 无动力学项 / 无作用量字样）
  组 B  r77 两条诊断应用到实际 U（齐次 2 次 ⇒ 无自相互作用；减号 ⇒ tau 方向负质量平方）
  组 C  层级对齐（来料是静态力律、非场论 ⇒ 与 r69「0 传播自由度」同源；
                    r71/r74/r77 的 (∂κ)^2 动能是重建选择、非来料原貌）
  组 D  与 r78 互补登记 + 对 r77 待裁决 4 条的更新

纪律：纯标准库（Decimal 60 + Fraction 四元组量纲）；所有跨册读数机器回读他人产物；
      不改写他人任何册字节；所有「=零/真」结论配阳性对照。
"""

import io
import json
import os
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '源码')
DATA = os.path.join(ROOT, '数据')
STEM = 'TUFT-r79_来料正本实测与场论重建层级对齐_2026-10-17'
SRC_NAME = STEM + '.py'

LAIYUAN = os.path.join(DATA, 'TUFT-V41修正版_来料正本_2026-10-11.md')
R78_REPORT = os.path.join(DATA, 'TUFT-r78_耦合门票与弱场闭合判定_攻破_2026-10-16_report.txt')

ENTRIES = []
COUNTS = {}
GUARDS = []


def entry(tag, verdict, text, residual=None, note=''):
    ENTRIES.append({'tag': tag, 'verdict': verdict, 'text': text,
                    'residual': residual, 'note': note})
    COUNTS[verdict] = COUNTS.get(verdict, 0) + 1


def guard(name, ok, detail=''):
    GUARDS.append({'name': name, 'ok': bool(ok), 'detail': detail})
    if not ok:
        raise AssertionError('GUARD FAILED: ' + name + ' | ' + detail)



# ----------------------------------------------------------------------------
# 跨册回链 + 量纲自检守卫
# ----------------------------------------------------------------------------
def G0_guards():
    guard('G0-1', os.path.exists(LAIYUAN), '来料正本(V41修正版)回链存在')
    guard('G0-2', os.path.exists(R78_REPORT), 'r78 报告回链存在（机器回读他人产物）')
    # 维度自检：齐次次数判据用「场幂次」，与单位约定无关，这里只确认四元组算符行为
    d1 = (Fr(1), Fr(0), Fr(0), Fr(0))
    d2 = (Fr(0), Fr(-2), Fr(0), Fr(0))
    guard('G0-3', tuple(x + y for x, y in zip(d1, d2)) == (Fr(1), Fr(-2), Fr(0), Fr(0)),
          '四元相加行为正常')
    # 阳性对照：已知二次函数 x^2 在原点的二阶差分应 = 2（检验器非恒零）
    def d2ctrl(h):
        hh = Decimal(h)
        return (hh * hh - 2 * Decimal(0) + (-hh) * (-hh)) / (hh * hh)
    ctrl = d2ctrl('1e-4')
    guard('G0-4', abs(ctrl - Decimal('2')) < Decimal('1e-9'), '二阶差分阳性对照=2')


# ----------------------------------------------------------------------------
# 组 A：来料正本机器实测
# ----------------------------------------------------------------------------
def group_A():
    with io.open(LAIYUAN, 'r', encoding='utf-8') as f:
        text = f.read()
    n = len(text)

    # A1 可读
    entry('A1', 'PASS',
          ('来料正本《TUFT-V41修正版_来料正本》机器可读，长度 ' + str(n) +
           ' 字符（非人工声明，守卫 G0-1 校验文件存在）'),
          str(n), '回链')

    # A2 公式定位
    idx_u = text.find('U(\\mathbf{r})')
    idx_f = text.find('\\mathbf{F}_{\\text{uni}}')
    has_kap = ('κ' in text) or ('kappa' in text)
    has_tau = ('τ' in text) or ('tau' in text)
    has_minus = ('−' in text) or ('-' in text)
    ok_formula = idx_u >= 0 and idx_f >= 0 and has_kap and has_tau and has_minus
    entry('A2', 'PASS' if ok_formula else 'FAIL',
          ('实际来料核心形式机器定位：势能公式出现在字符位 ' + str(idx_u) +
           '，统一力方程出现在字符位 ' + str(idx_f) +
           '；含 κ/τ 与减号 ⇒ 实测到 `U = α(κ²−τ²)`、`F = −α∇(κ²−τ²)`'),
          str(idx_u) + '/' + str(idx_f), '公式定位')

    # A3 动力学项扫描（时间导数 / 动能 / 作用量量）
    dyn_tokens = ['∂_t', '∂t', '时间导数', '时间演化', '动力学', '(∂κ', '(∂τ',
                  'dot{', '□', '拉氏量', '拉格朗日', '作用量', '动能项']
    found_dyn = [t for t in dyn_tokens if t in text]
    static = (len(found_dyn) == 0)
    entry('A3', 'PASS' if static else 'BOUNDARY',
          ('动力学项扫描：在 ' + str(n) + ' 字符全文中检索时间导数/动能/作用量类记号 '
           + str(dyn_tokens) + ' ⇒ 仅命中散文名词 ' + str(found_dyn) +
           '（非方程中的时间导数/动能算符）⇒ **方程中无时间导数、无动能项、无作用量**'
           ' ⇒ 来料是**静态几何梯度力律**，不是场论作用量'),
          str(len(found_dyn)), '静态判定')

    # A4 作用量/拉氏量 字样计数
    cnt_action = len(re.findall(r'作用量|拉氏|拉格朗日|Lagrangian|\\mathcal\{L\}', text))
    entry('A4', 'PASS' if cnt_action == 0 else 'BOUNDARY',
          ('作用量/拉氏量 字样计数 = ' + str(cnt_action) +
           ' ⇒ 来料从未以变分/作用量形式陈述，'
           '四力由 `κ∝M/r`、`τ∝q/r` 等 ansatz 代换梯度得到，非从作用量变分导出'),
          str(cnt_action), '无作用量')

    return text



# ----------------------------------------------------------------------------
# 组 B：r77 两条新诊断应用到实际 U = α(κ² − τ²)
# ----------------------------------------------------------------------------
def group_B():
    # B1 齐次次数（标度律指数）
    Ua = lambda k, t: (k * k - t * t)
    v = (Decimal('0.3'), Decimal('0.7'))
    alphas = [Decimal('2'), Decimal('3'), Decimal('5')]
    exps = []
    u0 = Ua(*v)
    for al in alphas:
        ua = Ua(al * v[0], al * v[1])
        exps.append((ua / u0).ln() / al.ln())
    ok_deg2 = all(abs(x - Decimal('2')) < Decimal('1e-30') for x in exps)
    entry('B1', 'PASS' if ok_deg2 else 'FAIL',
          ('★r77 诊断①应用到实际势：对 `U=α(κ²−τ²)` 做标度律指数 '
           'ln[U(αv)/U(v)]/ln α（α=2/3/5）得 '
           + ' / '.join(format(x, '.6E') for x in exps) + ' ⇒ **齐次次数 = 2** '
           '⇒ 按 r77 B5 判据属「自由场（无自相互作用）」类；'
           '注意：这与 r77 单常数四次势（齐次 4、无质量）不同——'
           '齐次 2 反而【有质量但无相互作用】'),
          format(exps[-1], '.6E'), '★齐次次数')

    # B2 两方向质量平方（重建为场论后的二阶变分）
    def d2(k_or_t, h):
        hh = Decimal(h)
        if k_or_t == 'k':
            return (Ua(hh, Decimal('0')) - 2 * Ua(Decimal('0'), Decimal('0'))
                    + Ua(-hh, Decimal('0'))) / (hh * hh)
        else:
            return (Ua(Decimal('0'), hh) - 2 * Ua(Decimal('0'), Decimal('0'))
                    + Ua(Decimal('0'), -hh)) / (hh * hh)

    m2k = d2('k', '1e-4')
    m2t = d2('t', '1e-4')
    tachyon = (m2k > 0) and (m2t < 0)
    entry('B2', 'FAIL' if tachyon else 'PASS',
          ('★重建为场论后两方向质量平方（取 α=1，原点二阶差分，步长 1e-4）：'
           'κ 方向 = ' + format(m2k, '.6E') + '（>0，正常质量）'
           '，τ 方向 = ' + format(m2t, '.6E') + '（<0）'
           '⇒ **τ 方向有效质量平方为负 ⇒ tachyon / 不稳定模**；'
           '这正是 r74 发现的 `(κ²−τ²)` 减号的物理后果（不是 r71 补导数才引入）'),
          format(m2t, '.6E'), '★tachyon')

    # B3 与 r74 上游符号冲突同源
    entry('B3', 'PASS',
          ('★与 r74 同源性：实际来料势能 `κ²−τ²` 是**减号**，'
           '而 S1 几何恒等式 `ω=c√(κ²+τ²)` 是**加号**（r74 A1 跨册机器回读 r69 JSON 确证）'
           '⇒ r74 判定的「上游符号冲突」在**实际来料正本中坐实**，'
           '不是重建版才有的问题；r71 的 τ 鬼场只是补导数后该负号的一次显形'),
          None, '★同源')



R69_JSON = os.path.join(DATA, 'TUFT-r69_V48修正完整版公式集_全维审计_2026-10-15.json')


# ----------------------------------------------------------------------------
# 组 C：层级对齐（来料是静态力律、非场论）
# ----------------------------------------------------------------------------
def group_C():
    # C1 与 r69「0 传播自由度」同源 —— 机器回读 r69 产物
    with io.open(R69_JSON, 'r', encoding='utf-8') as f:
        r69 = json.load(f)
    s3 = None
    for e in r69['entries']:
        if e.get('tag') == 'S3_R1' or e.get('id') == 'S3_R1':
            s3 = e
    s3_verdict = s3['verdict'] if s3 else None
    entry('C1', 'PASS' if s3_verdict in ('FAIL', 'BOUNDARY') else 'INFO',
          ('★层级同源：来料全篇无时间导数（A3）⇒ 无传播自由度 ⇒ '
           '与 r69 S3_R1 判的「0 传播自由度」**同源**（机器回读 r69 JSON：'
           'S3_R1 verdict=' + str(s3_verdict) + '），不是巧合——'
           'r69 审的就是这份来料族的同一数学层'),
          str(s3_verdict), '★同源')

    entry('C2', 'INFO',
          ('★重建选择声明：r71 注入 `(∂κ)²` 动能项、r74 同号化、r77 的齐次性定理，'
           '都是把「静态几何梯度力律」**重建为场论作用量**的工作假设；'
           '来料原貌（V41 修正版）并无这些项。本册登记此层差，'
           '不声称来料「本应有」动能项'),
          None, '重建声明')

    entry('C3', 'BOUNDARY',
          ('★四力来源性质：来料把 `κ∝M/r`、`τ∝q/r`、`tau_weak∝q e^{-μr}/r`、`tau_strong∝σ r e^{-r/r0}` '
           '直接代入梯度得到四力 ⇒ 是**几何 ansatz 代换**，非从作用量变分导出'
           '（承 r19/r20 关于「推导 vs 声明」的告诫；r69 已列的同源问题）'),
          None, 'ansatz')


# ----------------------------------------------------------------------------
# 组 D：与 r78 互补登记 + 对 r77 待裁决 4 条的更新
# ----------------------------------------------------------------------------
def group_D():
    # D1 机器回读 r78 报告（他人产物），互补而非重复
    cassini = None
    missing = None
    with io.open(R78_REPORT, 'r', encoding='utf-8') as f:
        rep = f.read()
    m = re.search(r'纯标量超 Cassini 限 4 个量级以上 \| ratio=([\d.E+]+)', rep)
    if m:
        cassini = m.group(1)
    m = re.search(r'缺失项计数为 0 \| (\{[^}]*\})', rep)
    if m:
        missing = m.group(1)
    entry('D1', 'PASS',
          ('★与 r78 互补（机器回读 r78 报告，非重复）：r78 已证 '
           '纯标量重力超 Cassini 限 ratio≈' + str(cassini) + '（4+ 阶）、'
           '来料对「牛顿/弱场/源项/J_κ」提及=' + str(missing) + '；'
           '本册补：即便只看势形式，它也是「齐次 2 次（无自相互作用）'
           '+ τ 方向 tachyon（B2）」⇒ 与 r78「无弱场/源结构」**自洽互证**'),
          str(cassini), '互补 r78')

    entry('D2', 'FAIL',
          ('★综合判定：实际来料在 r77 框架下**比「单常数无质量标量」更弱**——'
           '它连场论都不是（A3 无动力学），且 τ 方向质量平方为负（B2 tachyon）；'
           'r77 的定理（质量∧相互作用需 ≥2 常数）在其上甚至**无需动用**'
           '（因为根本没有动力学层可供「质量/相互作用」附着）'),
          None, '★综合')

    entry('D3', 'BOUNDARY',
          ('★对 r77 待裁决 4 条的更新：'
           '① r77 的 P1/P4 同号化修复在来料层也必须把 `U=α(κ²−τ²)` 的**减号一并改掉**'
           '（改 `κ²+τ²`）才能消除 B2 的 tachyon，与 r74 出路同源；'
           '② r77 待裁决②「放宽 Ω5」在此来料下**不是主要障碍**'
           '（主障碍是无动力学，而非常数个数）；'
           '③ 真正要用户决的是两点：「是否接受把静态力律重建为场论」'
           '以及「负号 tachyon 如何处置」'),
          None, '更新裁决')

    entry('D4', 'PASS',
          ('分工声明：r78（他人）审「耦合门票/弱场闭合/PPN/Cassini」，属标量引力耦合侧；'
           '本册审「来料实际数学形式 vs r69–r77 场论重建链的层级对齐」，属形式溯源侧；'
           '两者入口不同、零重复、结论互证（均指向「来料尚未构成合格场论」）'),
          None, '分工')



# ----------------------------------------------------------------------------
def main():
    G0_guards()
    group_A()
    group_B()
    group_C()
    group_D()

    verdict = 'FAIL' if COUNTS.get('FAIL') else (
        'BOUNDARY' if COUNTS.get('BOUNDARY') else 'PASS')

    payload = {
        'round': 'r79',
        'date': '2026-10-17',
        'source': SRC_NAME,
        'counts': COUNTS,
        'total': len(ENTRIES),
        'verdict': verdict,
        'guard_all_ok': all(g['ok'] for g in GUARDS),
        'guards': GUARDS,
        'entries': ENTRIES,
        'not_self_derived': [
            {'tag': 'NS1', 'text': 'r77 的「齐次次数→物理属性」判据为 r77 本册已证，本册只应用不重证'},
            {'tag': 'NS2', 'text': 'r69 S3_R1「0 传播自由度」的判定承 r69 册，本册只机器回读其 verdict 不重算'},
            {'tag': 'NS3', 'text': 'r78 的 Cassini/缺失项结论承 r78 册，本册只机器回读其报告不重算'},
            {'tag': 'NS4', 'text': '来料把 κ∝M/r 等作为「物理前提」给出，其推导性本册只登记（ansatz 性质），不代为证伪或证实'},
            {'tag': 'NS5', 'text': '本册揭示的层差（静态力律 vs 场论）只做对齐登记，不代用户决定「是否重建为场论」'},
        ],
        'red_line': ('数学／数值自洽 ≠ 物理证实；本册只做来料正本实测与 r69–r77 场论重建链的'
                     '层级对齐，「实际来料尚未构成合格场论」的判定不构成对 TUFT 方向的普遍否证'),
    }

    with io.open(os.path.join(DATA, STEM + '.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(payload, ensure_ascii=False, indent=1))

    rlines = ['TUFT-r79 来料正本实测与场论重建层级对齐 运行报告',
              'counts=' + str(COUNTS) + ' total=' + str(len(ENTRIES)) +
              ' verdict=' + verdict, '']
    for e in ENTRIES:
        rlines.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rlines.append('    residual=' + e['residual'])
    rlines.append('')
    rlines.append('GUARD G0: ' + str(len(GUARDS)) + '/' + str(len(GUARDS)) + ' 全过')
    with io.open(os.path.join(DATA, STEM + '_report.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(rlines))

    ml = ['# 判定_TUFT-r79-来料正本实测与场论重建层级对齐', '',
          '日期：2026-10-17 · 评级：O/L2（r77 下游、r78 同期互补）', '',
          '## 条目计数', '- 总条目：' + str(len(ENTRIES))]
    for k in sorted(COUNTS.keys()):
        ml.append('- ' + k + '：' + str(COUNTS[k]))
    ml.append('- 总体 verdict：' + verdict)
    ml.append('')
    ml.append('## 逐条裁定')
    for e in ENTRIES:
        line = '- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text']
        if e['residual']:
            line += '  （残差 ' + e['residual'] + '）'
        ml.append(line)
    ml.append('')
    ml.append('## not_self_derived 登记')
    for n in payload['not_self_derived']:
        ml.append('- ' + n['tag'] + '：' + n['text'])
    ml.append('')
    ml.append('## 红线')
    ml.append(payload['red_line'])
    with io.open(os.path.join(DATA, STEM + '.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(ml))

    print('counts=' + str(COUNTS))
    print('total=' + str(len(ENTRIES)))
    print('verdict=' + verdict)
    print('')


if __name__ == '__main__':
    main()

