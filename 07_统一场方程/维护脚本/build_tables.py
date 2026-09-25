# -*- coding: utf-8 -*-
"""生成 UFE-1 场元数据表与现象覆盖矩阵（CSV + Markdown 双产出，单一数据源）。

用法： python -B build_tables.py
产出： ../场元数据表.csv  ../06_场元数据表.md
      ../现象覆盖矩阵.csv  ../07_现象覆盖矩阵.md
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
# Windows 控制台默认 GBK：诊断行里的 ⇒ 会让"报错本身"崩成 UnicodeEncodeError，看到的就不是结论而是栈
# （实测发生过）。以非零码退出这条路径必须可读，否则失败信号被编码错误盖住。
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = Path(__file__).resolve().parent.parent

# ========================================== SO(10) 三台仪器的机器可读输出 = 本表的单一数据源
# 这里**不抄数**。2026-09-24 一天之内"表格里的数改了、散文里的没改"复发了两次
# （链探针情形 C 的 $b_2$ 缺陷、表示论引擎把链探针的 3.8 倍写死进自己的散文），
# 覆盖矩阵是第三次传播的同一条链，所以只读仪器自己吐出的 JSON。
# 读不到 ⇒ 印 MISSING 并让本脚本以非零码退出，**绝不退回上一个字面量**（那正是失效族本身）。
VDIR = ROOT / '验证脚本'
MISSING = '（未读到 SO(10) 仪器输出：先跑 验证脚本/so10_chain.py 与 so10_reps.py、so10_thresholds.py）'
# 模板里 {token} 是"待接线"的记号，不是读数 ⇒ 生成后的文里还剩一个花括号，就是漏了 .replace。
# 但正文里本来就有 LaTeX 花括号（$\omega^{ab}$、$U(1)_{em}$），本文件首次上这条防护就是被这两处
# 假阳性挡住的 ⇒ 先在**人读到的块**里剥掉行内代码与数学，再找占位符；剥的依据是"每块 `$` 成对"，
# 出现落单的 `$` 会让该块之后的保护失效，所以它本身必须算失败，而不是悄悄少查一段。
TOKEN = re.compile(r'\{[a-z_][a-z_0-9]*\}')
CODE_SPAN = re.compile(r'`[^`]*`')
MATH_SPAN = re.compile(r'\$[^$]*\$')
# 单反斜杠接 r/l/t/b 会被 Python 当成转义：字面量 `\rvert` 落地时是一个 **CR** + "vert" ⇒ 渲染时该行
# 前缀被覆盖、Markdown 表格行被截断，而"未填槽位""`$` 落单"两类核对都看不见它。表示论引擎有同一条
# 断言（so10_reps 写盘前扫控制字符），本脚本上一版没有 —— 本轮给 GUARD_TXT 加 `\rvert` 时当场踩到，
# 生成的矩阵里真混进一个 CR。故：任何要写盘的文串先过 clean()。
CTRL = re.compile(r'[\x00-\x08\x0b-\x1f]')


def clean(text, where):
    hit = sorted(set(CTRL.findall(text)))
    assert not hit, '%s 含控制字符 %s ⇒ 有 LaTeX 反斜杠被 Python 吃掉，别让坏字符冒充通过' % (
        where, hit)
    return text


def _instr(fname):
    try:
        return json.loads((VDIR / fname).read_text(encoding='utf-8'))
    except Exception as e:
        print('[warn] %s 不可读：%r' % (fname, e))
        return None


def _gates(d):
    t = (d or {}).get('tests') or (d or {}).get('gates') or []
    return len(t), sum(1 for r in t if r.get('status') == 'PASS')


def _band(d, key, unit):
    """单阈 3221 链各**物理解**在 key 上的两端（情形并列区间，不是误差棒）。"""
    vs = []
    for r in ((d or {}).get('r3221_determined') or {}).values():
        if not r.get('physical'):
            continue
        v = r.get('scales', {}).get(key) or r.get(key)
        if v:
            vs.append(v)
    return '%.1e–%.1e %s' % (min(vs), max(vs), unit) if len(vs) >= 2 else MISSING


CHAIN_J = _instr('SO10链统一报告.json')
REPS_J = _instr('SO10表示论报告.json')
THRS_J = _instr('SO10阈值报告.json')
MGUT_BAND = _band(CHAIN_J, 'M_GUT', 'GeV')
TAU_BAND = _band(CHAIN_J, 'tau_p_yr', 'yr')
N_CHAIN, NP_CHAIN = _gates(CHAIN_J)
N_REPS, NP_REPS = _gates(REPS_J)
N_THRS, NP_THRS = _gates(THRS_J)
GATE_TOTAL = N_CHAIN + N_REPS + N_THRS
# "N 项门禁全 PASS" 是一句**断言**，不是一个计数：只数条目数会在存在 FAIL 时照样印出"全 PASS"
# ⇒ 印之前必须核对通过数，且核对不过要走到非零退出码，否则这条不变量没有出口。
GATE_FAIL = [(n, t, p) for n, t, p in (('so10_chain', N_CHAIN, NP_CHAIN),
                                       ('so10_reps', N_REPS, NP_REPS),
                                       ('so10_thresholds', N_THRS, NP_THRS))
             if t and p != t]
if not min(N_CHAIN, N_REPS, N_THRS):
    GATES_TXT = MISSING
elif GATE_FAIL:
    GATES_TXT = ('存在 FAIL：%s ⇒ 本表不引用门禁数'
                 % '、'.join('%s（PASS %d/%d）' % (n, p, t) for n, t, p in GATE_FAIL))
else:
    GATES_TXT = '%d + %d + %d = %d 项门禁全 PASS' % (N_CHAIN, N_REPS, N_THRS, GATE_TOTAL)

YUK_ROWS = (REPS_J or {}).get('yukawa') or []
YUK_CH = (REPS_J or {}).get('yukawa_channels') or {}
MAJ = [r['name'] for r in YUK_ROWS if r.get('holds_maj')]


def _slash(xs):
    return '/'.join(xs) if xs else '（无）'


YUK_TXT = ('对称 %s、反对称 %s、对消 %s；dim≤210 内唯一携带 −2ν 权重者 %s'
           % (_slash(YUK_CH.get('sym', [])), _slash(YUK_CH.get('anti', [])),
              _slash(YUK_CH.get('vec', [])), _slash(MAJ))
           if YUK_CH and MAJ else MISSING)

# 第九项（R8 不变张量簿记）的读数同样**只接线、不手抄**：缺任一项就印 MISSING，
# 而不是沿用上一次的字面量——"表跑在文前面"正是本脚本来防的那件事。
LED = (REPS_J or {}).get('singlet_ledger') or []
INV_R = (REPS_J or {}).get('invariant') or {}
TRI = INV_R.get('triple_product_singlets') or {}
ROUTES = INV_R.get('routes') or {}
_CHAN_TEX = {'$16\\otimes16$': '16⊗16', '$16\\otimes\\overline{16}$': '16⊗16̄',
             '$16^{\\otimes4}$': '16⊗4'}
_LED_TRIP = [_CHAN_TEX.get(x['product'], x['product']) for x in LED]
_PAIR4 = set([ROUTES.get(k) for k in ('decomp_I', 'decomp_II', 'pair_cc', 'pair_cf')])
INV_TXT = ('R8：荷账本／不变张量按 %s 顺序为 %s，四条不共享代码的路径对 '
           '16⊗16⊗16̄⊗16̄ 同为 %s；δ 判据在 %s 个表示对上现场核验（反例 %s）；'
           '物质-only 的 16⊗4 有 %s 个不变张量且 Δ(B−L) 恒为 0，而 16⊗16⊗H 的单态数在 '
           '126 上 %s、在 126̄ 上 %s ⇒ Δ(B−L)=±2 必须插入 126̄_H'
           % ('、'.join(_LED_TRIP),
              '、'.join('(%d,%d)' % (x['zero_weight_dirs'], x['invariants']) for x in LED),
              _slash([str(v) for v in sorted(_PAIR4)]) if len(_PAIR4) == 1 else '（不一致）',
              INV_R.get('delta_pairs_tested'),
              '有' if INV_R.get('delta_counterexamples') else '0',
              INV_R.get('matter_only_invariants'),
              TRI.get('126'), TRI.get('126̄'))
           if len(LED) == 3 and len(_PAIR4) == 1 and TRI and INV_R.get('delta_pairs_tested')
           else MISSING)

# 第十项（R9 不变张量的道分解）同样只接线、不手抄：任一读数缺失或道表与合计不咬合即 MISSING。
CS = (REPS_J or {}).get('channel_split') or {}
_INS = CS.get('ins') or {}
_PAIRS = CS.get('pairs') or {}
_MUT = CS.get('mut') or {}


def _chan(rows):
    return '、'.join('%s→%d' % (n, c) for n, _k, c in rows)


_CHAN_ALL = (CS.get('rows_chiral') or []) + (CS.get('rows_vector') or [])
CHAN_TXT = (
    'R9：手征侧 $16\\otimes16$ 的道 %s（合计 %s = R8 的数），对消侧 %s（合计 %s）；"在场却不闭合"的道'
    '只有 %s，而它正是 126̄_H 的伙伴；单个 126 或 126̄ 插不进 16⊗4（三种结合方式 %s），成对插入才非零；'
    '同一张 16⊗4⊗126⊗126 上标号路径给 %s、名字路径给 %s（%s 条登记范围外标号）⇒ "按名字查共轭"只在 '
    'dim≤210 的登记表内可用'
    % (_chan(CS['rows_chiral']), CS['tot_chiral'], _chan(CS['rows_vector']), CS['tot_vector'],
       _slash([n for n, _k, c in _CHAN_ALL if not c]),
       '、'.join('%s：%d／%d／%d' % (k, v['gI'], v['gII'], v['gIII'])
                 for k, v in sorted(_INS.items())),
       _MUT['lab'], _MUT['byname'], _MUT['unreg'])
    if CS.get('rows_chiral') and CS.get('rows_vector') and _INS and _PAIRS and _MUT
    and CS['tot_chiral'] == sum(c for _n, _k, c in CS['rows_chiral'])
    and CS['tot_vector'] == sum(c for _n, _k, c in CS['rows_vector'])
    and all(v['gI'] == 0 for v in _INS.values())
    and all(v['gI'] for v in _PAIRS.values())
    else MISSING)

# 排版防护自己的核验读数（check_placeholder_guard.py 的副作用输出）：矩阵里那句"N 例、当前 N/N PASS"
# 同样是**接线**而不是手抄 —— 上一版把 8/8 写死在模板里，本脚本给它加到第 12 例时它就成假话了。
GUARD_MISSING = '（未读到防护核验输出：先跑 维护脚本/check_placeholder_guard.py 再重跑本脚本）'
try:
    GJ = json.loads((ROOT / '维护脚本' / 'check_placeholder_guard.json')
                    .read_text(encoding='utf-8'))
except Exception as e:
    print('[warn] check_placeholder_guard.json 不可读：%r' % (e,))
    GJ = {}
GUARD_TXT = (
    '可重跑的 %(cases_total)d 例（槽位 %(cases_slot)d 例：植入的 `{}` 必须被抓、LaTeX 花括号必须不报、'
    '落单的 `$` 必须报；分隔符 %(cases_delimiter)d 例：把 `\\lvert`/`\\rvert` 后补的分隔空格再摘掉，'
    '不变量必须在摘掉后的同一行上命中 %(n_planted)d 种，而磁盘上那份真报告里 %(live_separators)d 处'
    '分隔符、命中 %(n_live)d 处；把同一次摘除做到**整份报告**上 ⇒ %(retro_hits)d 处命中 / '
    '%(n_retro_kinds)d 种（文档里那句"N 处命中 / K 种"以此为出处，不是记忆）；文档核对 '
    '%(cases_doccheck)d 例：在临时快照里**同一份**投放两处过期数字（README 的例数改错 3、'
    '08 里那句变异核验例数的变异体数改错 +3）⇒ check_docs() 必须两族各自点出一处，'
    '一族抓到不替另一族作证（那一族是后接的线，没被植过错的数字等于没被核对过）；'
    '同一组里另有两例核**这道读台账的门禁自己**：磁盘那份真台账过 `check_mutation_ledger()` 的六条分支'
    '且无违规，再把台账一次改错六处 ⇒ 六条分支各自得出一条投诉（少哪条就是哪条已经死了）'
    '⇒ 一台永不响的仪器不能替四份文档作证；表格列数 '
    '%(cases_table)d 例：把修好的表格行逐字节改回修前'
    '（裸竖线）与生成器上一版的"转义"（两个反斜杠）⇒ `check_tables()` 必须点出投放的那几行，'
    '而一个反斜杠的合法转义不得报（否则它数的是竖线，不是**没被转义**的竖线）；反斜杠翻倍 '
    '%(cases_backslash)d 例：把生成报告里每一处合法的"单反斜杠紧跟字母"逐处改回翻倍 ⇒ '
    '`check_bs_runs()` 必须点名该文件自己数出的 %(bs_planted)d 处，且折叠回去逐字节还原；'
    '再摘掉 %(bs_exempt)d 处"引用缺陷的行内代码"的反引号 ⇒ 它们必须当场变成违规'
    '（豁免的粒度是一处行内代码，不是整段）；把"两个反斜杠紧跟空格/花括号/方括号"与一处真翻倍'
    '放进同一行 ⇒ 只报后者（"范围是紧跟字母"这句话得被同一行测到，不是写在注释里）；'
    '基线此刻 %(bs_files)d 份文件：翻倍 %(bs_double)d 处（要求 0）、合法 %(bs_single)d 处、'
    '豁免 %(bs_exempt)d 处（一条从不被走到的豁免分支等于没被核对过的说法）；四类接线 '
    '%(cases_order)d 例：在临时快照里跑**真的** `build_tables.main()`，投放"台账锚点漂一位"与'
    '"README 门禁数过期"两处缺陷 ⇒ 双缺陷同投必须 `[MUT]` 与 `[DOC]` 在同一次运行里会见血，'
    '只投一处则只见血于自己那一族、另一族一条都不许多（两族不能互相顶包；上一版 `main()` 打完 '
    '`[MUT]` 就直接 return ⇒ 台账一漂就把整批文档核对藏进下一次运行 = 第十七项当天那 7 处过期门禁数的来历））'
    '⇒ 当前 %(pass)d/%(cases_total)d PASS'
    % dict(GJ, n_planted=len(GJ.get('planted_hits') or []), n_live=len(GJ.get('live_hits') or []),
           n_retro_kinds=len(GJ.get('retro_kinds') or []))
    if all(k in GJ for k in ('cases_total', 'cases_slot', 'cases_delimiter', 'cases_doccheck',
                             'cases_table', 'cases_backslash', 'cases_order',
                             'bs_files', 'bs_single', 'bs_double', 'bs_exempt', 'bs_planted',
                             'pass', 'live_separators', 'retro_hits', 'retro_safe'))
    and GJ['cases_total'] == (GJ['cases_slot'] + GJ['cases_delimiter']
                              + GJ['cases_doccheck'] + GJ['cases_table'] + GJ['cases_backslash']
                              + GJ['cases_order'])
    and GJ['all_pass'] and GJ['pass'] == GJ['cases_total'] and not GJ.get('live_hits')
    and GJ['live_separators'] > 0 and GJ.get('planted_hits')
    and GJ['retro_hits'] > 0 and GJ.get('retro_kind_counts')
    and GJ['retro_hits'] + GJ['retro_safe'] == GJ['live_separators']
    else GUARD_MISSING)


# R11 那条判据的**外部**变异核验台账（check_r11_mutation.py 的副作用输出）：文档里那句
# "N 例（变异体 K、良性 M）"与上面的 GUARD_CASES 同族 —— 每加一个变异体它就过期 ⇒ 读 JSON，不抄。
# target_bytes 是这台仪器当初切锚点时那份引擎的字节数：引擎一改，这份台账就是在为**另一份文件**作证
# ⇒ 这里现比一次，漂了就报，于是"重跑变异核验"是一个被要求的动作而不是一句记忆。
def mutation_ledger_view(wj):
    """从一份台账字典导出文档门禁要用的四个量 —— 走函数是为了**能被喂一份改错的台账**：
    这台核对自己的四条分支（字节漂／verdict／夹具／例数账）得有反例可投，不能只在磁盘那份好台账上跑过。"""
    rows = wj.get('cases') or []
    return (wj,
            (wj.get('cases_total'), wj.get('mutants'), wj.get('benign')), rows,
            dict((k, sum(1 for c in rows if c.get('kind') == k))
                 for k in ('baseline', 'mutant', 'benign')),
            next((c for c in rows if c.get('kind') == 'baseline'), {}))


try:
    _WJ0 = json.loads((ROOT / '维护脚本' / 'check_r11_mutation.json').read_text(encoding='utf-8'))
except Exception as e:
    print('[warn] check_r11_mutation.json 不可读：%r' % (e,))
    _WJ0 = {}
WJ, MUT_WANT, MUT_ROWS, MUT_KIND, MUT_BASE = mutation_ledger_view(_WJ0)


def check_mutation_ledger(wj=None):
    """台账的内部账 + 它锚定那份引擎有没有漂：读不到、不平、漂了就报（缺失不是通过）。"""
    wj, _want, rows, kinds, base = mutation_ledger_view(WJ if wj is None else wj)
    if not wj:
        return ['变异核验台账不可读 ⇒ 文档里那句"N 例（变异体…、良性…）"没有出处'
                '（先跑 维护脚本/check_r11_mutation.py）']
    bad = []
    try:
        eng = (ROOT / '验证脚本' / 'so10_reps.py').stat().st_size
    except Exception as e:
        eng = None
        bad.append('读不到 so10_reps.py 的字节数：%r' % (e,))
    if wj.get('target_bytes') != eng:
        bad.append('变异核验切锚点时那份引擎 %s 字节，此刻 %s ⇒ 台账在为另一份文件作证，'
                   '重跑 维护脚本/check_r11_mutation.py' % (wj.get('target_bytes'), eng))
    if wj.get('verdict') != 'CAUGHT' or wj.get('missed') or wj.get('false_alarm'):
        bad.append('变异核验此刻不是 CAUGHT：verdict=%s missed=%s false_alarm=%s'
                   % (wj.get('verdict'), wj.get('missed'), wj.get('false_alarm')))
    if not wj.get('fixture_ok') or not wj.get('engine_json_tests'):
        bad.append('变异核验的基线夹具不成立：fixture_ok=%s engine_json_tests=%s'
                   '（基线打印的门禁数要等于报告 JSON 的 tests 条数，否则是夹具塌陷冒充捕获）'
                   % (wj.get('fixture_ok'), wj.get('engine_json_tests')))
    if not base or (base.get('gates'), base.get('pass'), base.get('exit')) != (
            wj.get('engine_json_tests'), wj.get('engine_json_tests'), 0):
        bad.append('台账里没有一条自洽的基线行：基线=%s 而报告 JSON 的 tests=%s（要 exit=0 且 PASS=门禁数'
                   '=tests 条数）' % (base.get('id'), wj.get('engine_json_tests')))
    # 例数的账要**从台账那几行里数出来**，不是拿声明去减：上一版在这里写 `mutants + benign == cases_total`，
    # 于是把一个真实存在的第 6 行（未打补丁的基线）算丢了 ⇒ 门禁在一份自洽的台账上报了假警。
    # 这里既比声明，也比 kind 计数，两边任何一边漂移（加例不改声明／改声明不加工）都留不住。
    if (len(rows) != wj.get('cases_total')
            or kinds['baseline'] != 1
            or kinds['mutant'] != wj.get('mutants')
            or kinds['benign'] != wj.get('benign')
            or 1 + (wj.get('mutants') or 0) + (wj.get('benign') or 0) != wj.get('cases_total')):
        bad.append('台账自己账不平：%d 行 cases 的 kind 计数 %s，声明是 cases_total=%s／mutants=%s／'
                   'benign=%s ⇒ 要 baseline 恰 1 行，且 1（基线）+ 变异体 + 良性 = 例数'
                   '（文档里那句"N 例（变异体 K、良性 M）"的 N 含那一例基线：它是未打补丁的那一份，'
                   '用来证明没植错时不报）'
                   % (len(rows), kinds, wj.get('cases_total'),
                      wj.get('mutants'), wj.get('benign')))
    if wj.get('caught') != wj.get('mutants'):
        bad.append('台账自己账不平：caught=%s 而 mutants=%s（每一个变异体都要被点名抓住）'
                   % (wj.get('caught'), wj.get('mutants')))
    return bad

# 覆盖矩阵里"修好前的报告原地留着多少处未定义控制词"这一句：上一版把 20 写死在模板里，而修好前的
# 那份报告已被覆盖、报告 .md 又没进 git ⇒ 这个数字当时唯一的藏身处是一个临时目录里的见证文件。
# 现在它读自防护核验：修法是"只补一个空格"，所以把全文的分隔空格摘掉就回到修好前那一版。
_retro_detail = '、'.join('`%s`×%d' % (k, c) for k, c in (GJ.get('retro_kind_counts') or []))
RETRO_TXT = (
    '%d 处命中 / %d 种未定义控制词（%s；另有 %d 处摘掉空格后仍安全，两者相加 = 全文 %d 处分隔符）'
    % (GJ['retro_hits'], len(GJ['retro_kinds']), _retro_detail, GJ['retro_safe'],
       GJ['live_separators'])
    if GJ.get('retro_hits') and _retro_detail and GJ.get('retro_kinds')
    and len(GJ['retro_kind_counts']) == len(GJ['retro_kinds'])
    and sum(c for _k, c in GJ['retro_kind_counts']) == GJ['retro_hits']
    and GJ.get('live_separators') and GJ['retro_hits'] + GJ.get('retro_safe', -1)
    == GJ['live_separators']
    else GUARD_MISSING)

# ================================================================ 场元数据表
# 列：名称, 符号, 自旋, 统计, 质量量纲, SU3, SU2, U1_Y, Q_em, 多重态数, 在壳自由度,
#     质量, 是否传播, 传播子分母, 来源, 备注
META_HEADER = ['名称', '符号', '自旋', '统计', '质量量纲', 'SU3表示', 'SU2表示',
               'U1超荷Y', '电荷Q', '多重态数', '在壳自由度', '质量', '是否传播',
               '传播子分母', '来源', '备注']

META = [
    ['引力子（度规扰动）', 'h_μν', 2, '玻色', 0, '1', '1', 0, 0, 1, 2, '0',
     '是', 'k²', '推导', '(E) 的线性化解；两个张量极化'],
    ['vierbein', 'e^a_μ', 1, '玻色', 0, '1', '1', 0, 0, 1, 6, '—',
     '是', '—', '定义', '基本变量；16 分量减去 6 个局域洛伦兹 gauge 余 10'],
    ['自旋联络', 'ω^ab_μ', 1, '玻色', 1, '1', '1', 0, 0, 1, 0, '—',
     '否', '—', '推导', '由 (C) 代数决定，非传播'],
    ['挠率', 'T^a_μν', 1, '玻色', 1, '1', '1', 0, 0, 1, 0, '—',
     '否', '—', '推导', '代数方程 (C)；由自旋流决定，全反对称'],
    ['曲率', 'R^ab_μν', 2, '玻色', 2, '1', '1', 0, 0, 1, 0, '—',
     '否', '—', '推导', '𝔰𝔬(1,3) 分量的统一曲率 F'],
    ['胶子', 'G^A_μ', 1, '玻色', 1, '8', '1', 0, 0, 8, 16, '0',
     '是', 'k²', '推导', 'f^ABC≠0 导致三/四胶子顶点'],
    ['弱玻色子（未破缺）', 'W^i_μ', 1, '玻色', 1, '1', '3', 0, 0, 3, 6, '0',
     '是', 'k²', '推导', '幺正规范下重组为 W±/Z/γ'],
    ['超荷玻色子', 'B_μ', 1, '玻色', 1, '1', '1', 0, 0, 1, 2, '0',
     '是', 'k²', '推导', '阿贝尔，无自相互作用'],
    ['W⁺ 玻色子', 'W⁺_μ', 1, '玻色', 1, '1', '1', 0, '+1', 1, 3, '80.377 GeV',
     '是', 'k²−m_W²', '推导', 'm_W = g₂v/2；质量来自 Higgs 机制'],
    ['W⁻ 玻色子', 'W⁻_μ', 1, '玻色', 1, '1', '1', 0, '−1', 1, 3, '80.377 GeV',
     '是', 'k²−m_W²', '推导', 'W⁺ 的反粒子'],
    ['Z 玻色子', 'Z_μ', 1, '玻色', 1, '1', '1', 0, 0, 1, 3, '91.1876 GeV',
     '是', 'k²−m_Z²', '推导', 'm_Z = (v/2)√(g₂²+g₁²)'],
    ['光子', 'A_μ（γ）', 1, '玻色', 1, '1', '1', 0, 0, 1, 2, '<1e−18 eV',
     '是', 'k²', '推导', 'U(1)_em 未破缺 ⇒ 质量被对称性保护'],
    ['Higgs 二重态', 'H', 0, '玻色', 1, '1', '2', '+1/2', '0/+1', 1, 4, '—',
     '是', 'k²−m_h²', '推导', '复二重态 = 4 实分量'],
    ['物理 Higgs', 'h', 0, '玻色', 1, '1', '1', 0, 0, 1, 1, '125.25 GeV',
     '是', 'k²−m_h²', '推导', 'm_h² = 2λv² ⇒ λ = 0.129'],
    ['Goldstone 玻色子', 'G^± G⁰', 0, '玻色', 1, '1', '1', 0, '0', 3, 0, '0',
     '否', '—', '推导', '被 W±/Z 吸收为纵向极化'],
    ['左手夸克二重态', 'Q_L', '1/2', '费米', '3/2', '3', '2', '+1/6', '+2/3 −1/3', 6, 12, '输入',
     '是', 'γ·p', '输入', '质量由 Yukawa 输入，非推导'],
    ['右手上型夸克', 'u_R', '1/2', '费米', '3/2', '3', '1', '+2/3', '+2/3', 3, 6, '输入',
     '是', 'γ·p−m_u', '输入', 'm_u, m_c, m_t 为输入'],
    ['右手下型夸克', 'd_R', '1/2', '费米', '3/2', '3', '1', '−1/3', '−1/3', 3, 6, '输入',
     '是', 'γ·p−m_d', '输入', 'm_d, m_s, m_b 为输入'],
    ['左手轻子二重态', 'L_L', '1/2', '费米', '3/2', '1', '2', '−1/2', '0 −1', 2, 4, '输入',
     '是', 'γ·p', '输入', '包含 ν_L 与 e_L'],
    ['右手带电轻子', 'e_R', '1/2', '费米', '3/2', '1', '1', '−1', '−1', 1, 2, '输入',
     '是', 'γ·p−m_e', '输入', 'm_e, m_μ, m_τ 为输入'],
    ['右手中微子', 'ν_R', '1/2', '费米', '3/2', '1', '1', 0, 0, 1, 2, '输入',
     '是', 'γ·p−m_ν', '输入', '2026-09-19 L1 修复新增；Dirac 质量 m_ν=y_ν v/√2（y_ν∼3×10⁻¹³）'],
]

META_DOC = """# 场元数据表

[主方程](00_统一场方程.md) · [作用量与场内容](01_作用量与场内容.md) · [现象覆盖矩阵](07_现象覆盖矩阵.md) · [验证报告](验证脚本/验证报告.md)

本表列出 UFE-1 全部动力学场的**物理属性元数据**。数据文件：[场元数据表.csv](场元数据表.csv)

## 约定

- **质量量纲**：以能量的幂次计（$\\hbar=c=1$）。规范玻色子为 1，费米子为 $3/2$，标量与 vierbein 相关量为 1 或 0。
- **在壳自由度**：玻色子按极化数计（无质量矢量 2，有质量矢量 3，标量 1，无质量张量 2）；费米子按 Weyl 分量计（每个二分量 Weyl 旋量 = 2 个在壳实自由度，含反粒子）。
- **是否传播**：由运动方程是否含该场的时间导数决定。$\\omega^{ab}$ 与 $T^a$ 受代数方程 (C) 约束，**不传播**——这是 UFE-1 与 Poincaré 规范引力的分界线。
- **来源**：`推导` = 由主方程结构性决定；`输入` = 必须从实验取得；`定义` = 基本变量。

## 元数据总表

{table}

## 自由度核算

**破缺前**：胶子 16 + $W^i$ 6 + $B$ 2 + Higgs 4 = **28** 玻色自由度。
**破缺后**：胶子 16 + $W^{\\pm}$ 6 + $Z$ 3 + $\\gamma$ 2 + $h$ 1 = **28**。
**Higgs 机制的本质**：4 个标量自由度（其中 3 个 Goldstone）转变为 3 个有质量矢量的纵向极化，自由度总数守恒。

**每代费米子**：$Q_L$(12) + $u_R$(6) + $d_R$(6) + $L_L$(4) + $e_R$(2) + $\\nu_R$(2) = **32** 在壳自由度；等价于 16 个二分量 Weyl 旋量（2026-09-19 纳入 $\\nu_R$ 后由 30→32）。

## 元数据揭示的两条硬事实

1. **26 个输入参数**（$g_1,g_2,g_3,\\mu,\\lambda$、9 个费米质量、3 个中微子质量、4 个 CKM 参数、4 个 PMNS 参数、$G$）在表中标记为 `输入`。它们**不是**主方程推导出的——这是当前统一场论的真实完成度。$19\\to26$ 的 7 个增量来自 2026-09-19 的 $\\nu_R$ 纳入。
2. **挠率与自旋联络不传播**。因此 UFE-1 **不引入第五种力**，引力波极化仍是纯张量，与 GR 不可区分（在自旋非极化源的情形）。这是可检验判据，见 [预言 P2](08_预言与判据.md)。

[返回理论核心](../README.md)
"""

# ================================================================ 现象覆盖矩阵
PHEN_HEADER = ['现象', '特征尺度', '主控方程分量', '由主方程导出', '定量一致性', '证据状态', '备注']

PHEN = [
    ['自由落体 / 牛顿引力', '宏观', '(E) 弱场慢速极限', '是', '是', '已确立', '∇²Φ=4πGρ 由 (E) 推出，非独立公设'],
    ['水星近日点进动', '太阳系', '(E) Schwarzschild', '是', '是 42.98″', '已确立', 'C2：预测 42.98″/世纪，实测残差同一值'],
    ['太阳引力光线偏折', '太阳系', '(E)', '是', '是 1.751″', '已确立', 'C3：VLBI 实测 1.751±0.002″'],
    ['引力红移', '实验室 / 天文', '(E)', '是', '是', '已确立', 'Pound–Rebka；GPS 日常修正'],
    ['Shapiro 时间延迟', '太阳系', '(E)', '是', '是', '已确立', 'Cassini 测量符合到 2×10⁻⁵'],
    ['参考系拖拽（Lense–Thirring）', '地球', '(E) 旋转源解', '是', '是', '已确立', 'Gravity Probe B、LAGEOS'],
    ['引力波辐射', '致密双星', '(E) 线性化', '是', '是', '已确立', 'C4：GW150914 辐射 5.5e47 J vs 实测 5.4e47 J'],
    ['引力波以光速传播', '宇宙学', '(E) □h=0', '是', '是', '已确立', 'GW170817：|v−c|/c < 3e−15'],
    ['引力波仅两种张量极化', '天体', '(C)+(E)', '是', '未精确定量', '部分确立', 'UFE-1 判据：挠率不传播，无标量/矢量模'],
    ['黑洞阴影', '事件视界尺度', '(E) Kerr/Schwarzschild', '是', '是（~10%）', '已确立', 'EHT M87* 与 Sgr A*'],
    ['宇宙膨胀（H₀）', '宇宙学', '(E) Friedmann', '是', '参数输入', '已确立（参数未推导）', 'H₀ 张力 5σ 未解决'],
    ['宇宙加速膨胀', '宇宙学', 'Λ 项', '否（输入）', '否', '未解决', 'L7：Λ 数值与 QFT 真空能差 10¹²⁰'],
    ['库仑定律 / 1/r²', '原子到宏观', '(YM) U(1)_em', '是', '是（<1e−16）', '已确立', '由光子无质量保证'],
    ['电磁波', '全域', '(YM) U(1)_em', '是', '是', '已确立', '齐次方程由比安基恒等式给出'],
    ['静磁场 / 安培力', '宏观', '(YM) U(1)_em', '是', '是', '已确立', ''],
    ['原子光谱 / 能级', '原子', '(D)+(YM)', '树级', '是（QED）', '已确立（非本项目复算）', '本项目只给树级顶点'],
    ['Lamb 位移', '原子', 'QED 单圈', '否（未计算）', '已知一致', '未复算', '不声称本项目完成'],
    ['电子 / μ子 g−2', '精密测量', 'QED + 弱 + 强圈', '否（未计算）', '已知一致', '未复算', 'μ子 g−2 存在 4σ 级争议，未解决'],
    ['β 衰变', '核 / 粒子', '(YM) SU(2) 破缺', '是', '是', '已确立', 'G_F/√2 = g₂²/(8m_W²)'],
    ['W / Z 质量', '对撞机', '(H)+(YM)', '是', '是 0.04%', '已验证 E5.3', '由 G_F, α, m_Z, m_t 算出，非拟合'],
    ['中性流', '对撞机', '(YM) SU(2)×U(1)', '是', '是', '已确立', 'sin²θ_W 决定矢量耦合'],
    ['宇称最大破缺', '弱相互作用', '手征场内容', '是', '是', '已确立', 'Wu 实验；V−A 顶点'],
    ['CP 破坏（CKM）', '味物理', 'Yukawa 复相位', '是（相角为输入）', '是', '已确立（参数未推导）', 'CP 相不足以解释重子生成'],
    ['Higgs 玻色子', 'LHC', '(H)', '是', '是 125.25 GeV', '已确立', 'λ = m_h²/(2v²) = 0.129'],
    ['中微子振荡', '多尺度', '(Yukawa) ν_R', '是（质量为输入）', '是', '已确立（参数未推导）',
     '2026-09-19 L1 修复：纳入 ν_R 后 Dirac 质量 m_ν=y_ν v/√2≠0；质量谱与 PMNS 混合为输入。'
     '2026-09-24 表示论引擎把 ν_R 与 see-saw 的**群论部分**变成推导（so10_reps.py R7）：'
     'ν^c 是 16_F 里唯一的"色单态+弱单态+Q=0"权重，Majorana 项所需的 −2ν 权重在 dim≤210 内'
     '只由一个表示携带、而它恰是对称手征通道的成员 ⇒ 两条独立判据（能耦合手征物质 / 能破 B−L）'
     '落在同一个表示上（名字见句末通道表）；'
     '通道表（读自 SO10表示论报告.json）：' + YUK_TXT + '；系数与味结构仍为输入'],
    ['质子衰变', 'GUT 尺度', '——', '不适用', '未观测', '开放（v1）/ 互斥（SO(10)）',
     'v1 中 B−L 严格守恒 ⇒ τ_p=∞（P4）；但 SO(10) 链探针给 τ_p=' + TAU_BAND +
     '（读自 SO10链统一报告.json，非手抄）⇒ 二者不能同时为真（F5）；'
     '若走 SO(10)，B−L 破缺只能取自 126_H/126̄_H（表示论推导，F6）'],
    ['渐近自由', '高能', '(YM) SU(3)', '是', '是', '已确立', 'R2.2：α_s(200 GeV) 预测 0.1060 vs 0.1057'],
    ['喷注（jets）', '对撞机', '(YM) SU(3)', '定性', '定性', '已确立（定性）', '部分子模型 + 跑动耦合'],
    ['色禁闭', '低能', '(YM) SU(3)', '否（无解析证明）', '—', '格点数值确立', 'Clay 千禧年问题，全人类未解决'],
    ['质量隙 Δ>0', '低能', '(YM) SU(3)', '否', '—', '未解决', '同上'],
    ['强子质量谱', '低能', '(YM) SU(3)', '否', '—', '需格点计算', 'm_p=938 MeV 由 Λ_QCD 生成，未能第一性原理算'],
    ['核力与核结合能', 'fm', '残余强作用', '有效理论', '是（有效）', '已确立（有效理论）', 'π 交换 Yukawa 势，非主方程直接结果'],
    ['自旋–自旋挠率效应', '高自旋密度', '(C) 推论 1.3', '是（已推导）', '未测', '未检验', 'P3：四费米子接触项，待实验'],
    ['宇宙反弹（避免奇点）', '极早期', '(C)+(E)', '部分', '未测', '未检验', 'P3b：ρ_crit 定标未建立'],
    ['暗物质', '星系到宇宙', '——', '否', '否', '未解决', 'L8：v1 场内容无暗物质候选'],
    ['暗能量', '宇宙学', 'Λ 输入', '否', '否', '未解决', 'L7'],
    ['物质–反物质不对称', '宇宙学', 'CKM CP + sphaleron', '不足', '否', '未解决', 'CP 破坏量级差约 10⁸ 倍'],
    ['层级问题 M_Pl/M_Z', '理论', '——', '否', '否', '未解决', 'L4：比值 1.3e17 无解释'],
    ['耦合常数统一', '高能', 'β 函数', '否（v1）/ 条件性（SO(10)）', '否（SM 散布 3.66）',
     '否定性结果 R1 + L10 未闭合',
     'SM 单圈不统一；MSSM 对照可统一；2026-09-23 SO(10) 三链一环：单阈 3221 链定出 '
     'M_GUT=' + MGUT_BAND + '（三情形并列区间，读自 SO10链统一报告.json）'
     '（2026-09-24 F4 撤销后区间左端改由情形 C 给出 ⇒ 区间**变宽**）'
     '，但依赖链选择与标量谱（其中「B−L 破缺取自哪个表示」已由 so10_reps.py '
     '从 D5 权重格推出、且 2026-09-24 起 11 个表示沿 3221/422 两条链的分支规则系数与 '
     '422→3221 跨链匹配（R6.7）也都是算出来的 '
     '⇒ 无 126_H 的情形 B 不算 B−L 破缺，F6），且与 P4 互斥（F5）。'
     '同日阈值层（so10_thresholds.py）把「依赖标量谱」精确化为「依赖同一母表示内部的分量分裂」：'
     '完整多重态放在共同标度上只平移 α_i⁻¹、不动 M_GUT 与 M_R；两环仍未做 ⇒ ' + GATES_TXT],
]

PHEN_DOC = """# 现象覆盖矩阵

[主方程](00_统一场方程.md) · [四力还原](03_四力还原.md) · [经典极限](05_经典极限与现象推导.md) · [验证报告](验证脚本/验证报告.md)

本表回答一个朴素问题：**已知的物理现象，有多少能从这个方程推出来？** 数据文件：[现象覆盖矩阵.csv](现象覆盖矩阵.csv)

## 证据状态口径

| 状态 | 含义 |
|---|---|
| `已确立` | 由主方程（或其已确立的量子化）推导，且与实验定量一致 |
| `已验证 E5.3` 等 | 本项目验证器中有对应编号的检查项 |
| `部分确立` / `定性` | 机制正确，定量未完成 |
| `未复算` | 属已知结果，本项目**未**重新计算，不占为己有 |
| `未检验` | 已推导但无实验判定 |
| `未解决` / `矛盾` | 主方程无法覆盖或与实验冲突 |

## 覆盖矩阵

{table}

## 统计

| 状态 | 条数 | 占比 |
|---|---|---|
| 已确立（含已验证项） | {n_ok} | {p_ok}% |
| 部分确立 / 定性 | {n_part} | {p_part}% |
| 未检验（已推导） | {n_untest} | {p_untest}% |
| 未解决 / 矛盾 / 不适用 | {n_fail} | {p_fail}% |

## 六条必须直说的结论

1. **四种力的经典与树级现象基本被覆盖**，且 $m_W$ 的预测（E5.3，0.04%精度）与三大经典检验（C2/C3/C4）是**真实计算**，不是拟合。
2. **中微子振荡已修复**（L1，2026-09-19）：纳入 $\\nu_R$ 后 Dirac 质量 $m_\\nu=y_\\nu v/\\sqrt2\\ne0$，与振荡相容；代价是参数 19→26、$y_\\nu$ 极小性未解（见 [L1](09_已知局限与否定清单.md)）。
3. **禁闭、暗物质、暗能量、层级问题、耦合统一**全部未解决。把这几项算作"统一场论已完成"是错误的；本表把它们显式登记为未解决，是为了防止这类误读。
4. **耦合统一一项在 2026-09-23 从"不可判"变为"可判定但待取舍"**：`so10_chain.py` 在 SO(10) 内容下解出
   $M_{\\rm GUT}=$ {mgut_band} 与 $\\tau_p=$ {tau_band}
   （[SO10链统一报告](验证脚本/SO10链统一报告.md)，{gates_chain} 项门禁全 PASS；区间为三情形**并列**、非误差棒，
   且 2026-09-24 撤销 F4 后左端改由情形 C 给出 ⇒ 区间**变宽**而非收窄）。它**没有**把该行改成"已确立"——统一依赖未推导的标量谱，
   且与 P4（质子绝对稳定）互斥，属本项目的自我矛盾项 F5，取舍未定。
5. **标量内容的权重层与 d=4 耦合通道全部改为推导**（2026-09-23 判定承载表示，2026-09-24 算出分支系数、跨链匹配、Yukawa 通道表并用第二条路复算不变张量）：
   `so10_reps.py`（{gates_reps} 项门禁全 PASS）由 D5 的 Dynkin 图推出
   "$B-L$ 破缺而保 $U(1)_{em}$"只能取自 $126_H/\\overline{126}_H$ 的 $\\Delta_{L/R}$ 中性分量，
   于是**情形 B（无 $126_H$）不再可称为已实现 $B-L$ 破缺**（记为 F6）；同一引擎又以
   Klimyk–Springer 交错和算出 11 个表示沿 $3221$、$422$ 两条链的完整分支规则（报告 §5），
   并把 $422\\to3221$ 的跨链匹配做成门禁 R6.7（两步限制 = 一步限制，11 个表示逐项相等）：
   $B-L$ 由此被证明是 $SU(4)_c$ 内与 $SU(3)_c$ 对易的**唯一**方向（R6.8a）且在每个 $SU(4)$
   不可约表示上无迹（R6.8）⇒ 那一步**不必另外引入 $U(1)$**。同一引擎又独立地判了第二个问题——
   d=4 可重整算符 $16_F16_FH$ 允许哪些 Higgs（R7.1–R7.9，通道表 {yuk_channels}，
   读自 SO10表示论报告.json）⇒ 承担 $SU(2)_R$ 破缺的 $\\Sigma(1,1,3)_0$ 所在的那个对消通道表示，
   对 $3\\times16$ 的手征物质**没有**可重整 Yukawa（取期望值不产生任何费米子质量），
   而 see-saw 的"能耦合手征物质"与"能破 $B-L$"两条独立判据落在同一个表示上。
   同日第九项（R8）又用**第二条不共享代码的算法**判了"哪些组合本身就是规范不变的"——把
   **荷账本**（全部 Cartan 荷为零的方向数）与**不变张量个数**分成两列记账，并按标号把上面那张
   通道表独立复算了一遍：{inv_ledger}。
   同日第十项（R9）把那个配对和**按道拆开**、并第一次改走**标号**路径：{chan_split}。详见
   [SO10表示论报告](验证脚本/SO10表示论报告.md) §6（通道表）、§7（不变张量簿记）与 §8（道分解）。该行仍是"条件性"——**二环与 $126_H$
   位势未做**（对数阈值已于 2026-09-24 在一环执行，见 [SO10阈值报告](验证脚本/SO10阈值报告.md)），
   **通道表只到"哪些表示允许出现"**，不含系数与味结构（哪个拷贝耦合哪一代），
   且 R8 数的是**不变张量的个数、不是算符的个数**（Lorentz 指标、味指标与 Fierz 恒等式三关都没过
   ⇒ "$16^{\\otimes4}$ 有 2 个不变张量"不等于"2 个质子衰变算符"，这些数**不**回填进寿命计算），
   R9 也只判到"哪一条道闭合"——"闭合的道在谱里有没有母表示"是情形文字给出的**输入**（两条闭合的手征道里
   只有 $10_H$ 被声明、$120_H$ 无人声明），不是权重算出来的结论，
   且判定依赖"$Q=0$ 才允许取期望值""$B-L$ 必须被破"这两条物理输入。
6. **本表的 SO(10) 数字一律读自仪器的 JSON，不再手抄**（{gates_total}）：一天之内"表格改了、散文没改"
   复发两次（链探针情形 C 的 $b_2$ 缺陷 ⇒ 台账 F4 撤销；表示论引擎把链探针的摆动倍数写死进散文 ⇒ 第七项），
   而覆盖矩阵是同一条链上的第三次传播机会。故本脚本只**接线**：读不到仪器输出、或任一仪器的
   PASS 数与其条目数不等时，以非零码退出，**不退回上一个字面量**——退回旧数本身就是那个失效族。
   （"N 项门禁全 PASS"是一句**断言**而不是一个计数：只数条目数时，存在 FAIL 也会照样印出"全 PASS"。）
   第八项在同一族里又抓到两处**排版层**的同类缺陷——报告正文里一个未闭合的 `$…$`、以及未格式化的
   Python repr 直接印进散文 ⇒ 表示论引擎写盘前新增两条断言（全文段落级 `$` 配对、正文无 repr 泄漏），
   并把命中数打进控制台与 JSON 的 `report_hygiene` 字段：不变量若没有人打印，就等于没有不变量。
   第九项补第三条断言（正文不得出现未替换的 `%d`/`%(name)s` 占位符——`%` 只绑到拼接字面量的第一段时
   就会漏，第九项当天真实踩到两次），并留下两条元层教训：**该断言自己的消息串犯了它要拦的错**（`% 参数`
   未转义 ⇒ 命中时抛 `ValueError` 而非可读消息）；**植入式核验的第一版是假绿的**——副本目录里没带
   兄弟脚本 `so10_chain.py` ⇒ 上游门禁 R2.0 未过 ⇒ R7/R8 整层不运行 ⇒ 植入的缺陷根本没进正文。
   ⇒ 核验一条防护之前，要先核验它真的在接收流量。
   第十项补第 4 条排版断言，缺陷来源不在散文而在**表格里**：把裸竖线改写为 `\\lvert`/`\\rvert` 时不留
   分隔符，而 TeX 按最长匹配切控制词 ⇒ 报告里原地留着 {retro_bleed}（整段公式渲染报错，而门禁全绿——
   这一条在数值门禁里**没有对应项**，所以门禁数涨到多少项都照样绿）。修法是补回分隔空格，且这条断言**不**豁免表格行 —— 前三条只查正文段落，
   而缺陷恰恰只在表格里。上面那个"处命中 / 种数"不是记忆：修法是**只补一个空格**，所以把全文的分隔空格
   摘掉就逐字节回到修好前那一版 ⇒ 这个数由 `check_placeholder_guard.py` 每次重跑现算，并且
   "命中 + 摘掉后仍安全 = 全文分隔符总数"这条账也在那脚本里核对。
   **本表自己也上了同一条防护**：生成的两份文里若还留着未填的 `{}` 槽位，就不写盘、直接以非零码退出。
   第一版立刻被两处 LaTeX 花括号（$\omega^{ab}$、$U(1)_{em}$）当假阳性挡住 ⇒ 核对单位仍是"人读到的块"，
   且先剥行内代码再剥数学；剥的依据要求每块 `$` 成对，**出现落单的 `$` 本身算失败**——那会让该块之后
   的保护静默失效，是同族的另一种 fail-open。这几条规则一起由
   `维护脚本/check_placeholder_guard.py` 固定成{guard_cases}。

[返回理论核心](../README.md) · [已知局限](09_已知局限与否定清单.md)
"""


def md_table(header, rows):
    out = ['| ' + ' | '.join(header) + ' |',
           '|' + '|'.join(['---'] * len(header)) + '|']
    for r in rows:
        out.append('| ' + ' | '.join(str(c).replace('|', '\\|') for c in r) + ' |')
    return '\n'.join(out)


def write_csv(path, header, rows):
    clean('\n'.join(['\t'.join(header)] + ['\t'.join(map(str, r)) for r in rows]), path.name)
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


# =========================================== 手写文档里的"门禁数"是一处必然过期的复述
# 覆盖矩阵已改成只读 JSON，但 README/05/08/09 是手写散文：每写一个 "N 项门禁" 就多一个会漂移的副本
# （这一族失效在同一天复发过两次）。本函数不代写文档，只**当场核对**——文档里的数不等于仪器此刻的数
# 就打印位置并以非零码退出，让"改了表没改文"至少有一个出口。
GATE_MENTION = re.compile(r'(\d{1,3})\s*[项条]\s*门禁')
GATE_TRIPLE = re.compile(r'(\d{1,3})\s*\+\s*(\d{1,3})\s*\+\s*(\d{1,3})\s*=\s*(\d{1,3})')
# "现 N 项"是**现在时**陈述（历史行"当日 45 项自检"是合法的过去时，不核对）
GATE_NOW = re.compile(r'现\s*[*（(]{0,2}(\d{1,3})\s*项')
# "N 项自检"同样会过期（05 的 R1c 行就停在旧数上），但这族里多数是**合法的阶段记账**
# （"自检 51→54 项""该阶段 45 项""第X项，2026-09-24"）。判据：只在**没有**阶段/过去时标记的
# 行上核对 —— 宁可放过一行历史，也不把台账改成必须逐行重写。
SELFCHK = re.compile(r'(\d{1,3})\s*项\s*自检')
# "N 例固定样例"是排版防护的例数，同样会过期：本轮回护从 8 例长到 12 例，而矩阵与 README 还在说
# "8 例、当前 8/8 PASS"。故这一族按 check_placeholder_guard.json 的此刻核对，且**不因段落里出现
# 阶段标记而豁免**（豁免粒度是段落、数字粒度是句子 —— 见 check_docs 里那段反面教材）。
GUARD_CASES = re.compile(r'(\d{1,3})\s*例固定样例')
# "N 处命中 / K 种"是第 4 条排版断言"该抓多少"的读数。它今天是可重跑的（把真报告里的分隔空格摘掉就
# 回到修好前那一版），故按过去时豁免反而会把一句能核对的话放进无人看守的台账 —— 与 GUARD_CASES 同处理。
BLEED = re.compile(r'(\d{1,3})\s*处命中\s*/\s*(\d{1,3})\s*种')
# "N 例（变异体 K、良性 M）"是 R11 判据那道外部变异核验的例数，与 GUARD_CASES 同族同处理（不豁免）：
# 它的读数每次重跑 维护脚本/check_r11_mutation.py 都能现算，"过去时"在这里没有合法含义。
MUT_CASES = re.compile(r'(\d{1,3})\s*例（变异体\s*(\d{1,3})\s*、\s*良性\s*(\d{1,3})\s*）')
HISTORIC = re.compile(r'→|当时|其时|当日|首版|该阶段|\d{4}-\d{2}-\d{2}|第[一二三四五六七八九十]+项')
HAND_DOCS = ('README.md', '05_经典极限与现象推导.md', '08_预言与判据.md',
             '09_已知局限与否定清单.md', '07_现象覆盖矩阵.md')


def doc_blocks(text):
    r"""核对的单位是**人读到的一句话**，不是文件里的裸行。

    Markdown 段落里换行不断句（"（第三项）…\n 51 项自检全 PASS"是一句话），按裸行核对会把
    阶段标记和数字切在两行上、读不出那是过去时；表格行则每行独立。故：段落 = 连续非空非表格行拼接，
    表格行 = 单行，位置报该块首行的行号。
    """
    out, cur, start = [], [], 0
    for i, ln in enumerate(text.split('\n'), 1):
        if ln.startswith('|'):
            if cur:
                out.append((start, ' '.join(cur)))
                cur, start = [], 0
            out.append((i, ln))
        elif not ln.strip():
            if cur:
                out.append((start, ' '.join(cur)))
                cur, start = [], 0
        else:
            if not cur:
                start = i
            cur.append(ln)
    if cur:
        out.append((start, ' '.join(cur)))
    return out


def check_docs():
    valid = {N_CHAIN, N_REPS, N_THRS, GATE_TOTAL}
    want = (N_CHAIN, N_REPS, N_THRS, GATE_TOTAL)
    bad = []
    for rel in HAND_DOCS:
        p = ROOT / rel
        if not p.exists():
            bad.append('%s：不存在' % rel)
            continue
        for i, ln in doc_blocks(p.read_text(encoding='utf-8')):
            hist = bool(HISTORIC.search(ln))
            for m in GATE_MENTION.finditer(ln):
                if int(m.group(1)) not in valid:
                    bad.append('%s:%d 写着 "%s 项门禁"，仪器此刻只有 %s'
                               % (rel, i, m.group(1), sorted(valid)))
            # 三台仪器的**合计**是每次新增门禁族就会过期的数，而带日期/阶段标记的段落是**台账**：
            # 它记的是"那一天加完之后的合计"，重写它等于篡改记账。故只对无标记的现在时句核对。
            # 单台仪器的 "N 项门禁" 不豁免 —— 那一台没变，写错就是写错。
            for m in ([] if hist else GATE_TRIPLE.finditer(ln)):
                if tuple(int(x) for x in m.groups()) != want:
                    bad.append('%s:%d 三台仪器合计写着 "%s"，此刻应为 %d + %d + %d = %d'
                               % (rel, i, m.group(0), want[0], want[1], want[2], want[3]))
            for m in GATE_NOW.finditer(ln):
                if int(m.group(1)) not in valid:
                    bad.append('%s:%d 现在时写着 "现 %s 项"，仪器此刻只有 %s'
                               % (rel, i, m.group(1), sorted(valid)))
            if not HISTORIC.search(ln):
                for m in SELFCHK.finditer(ln):
                    if int(m.group(1)) not in valid:
                        bad.append('%s:%d 现在时写着 "%s 项自检"（该句无阶段标记），仪器此刻只有 %s'
                                   % (rel, i, m.group(1), sorted(valid)))
            # 这两族**不按段落级 HISTORIC 豁免**：它们的读数每次重跑都能现算（防护例数、摘掉分隔空格后的
            # 命中数），所以"过去时"在这里没有合法含义。本轮实测到反面教材 —— README 里一句"下面第十项里…"
            # 撞上 HISTORIC 的 第[一二三四五六七八九十]+项，把同一个 921 字符段落里的"16 例固定样例"、
            # "20 处命中 / 4 种"连同"55 + 81 + 40 = 176"一起免检了 ⇒ 豁免的粒度是段落，而数字的粒度是句子。
            for m in GUARD_CASES.finditer(ln):
                if int(m.group(1)) != GJ.get('cases_total'):
                    bad.append('%s:%d 写着 "%s 例固定样例"，防护核验此刻是 %s 例'
                               '（先跑 维护脚本/check_placeholder_guard.py）'
                               % (rel, i, m.group(1), GJ.get('cases_total')))
            for m in BLEED.finditer(ln):
                if (int(m.group(1)), int(m.group(2))) != (GJ.get('retro_hits'),
                                                          len(GJ.get('retro_kinds') or [])):
                    bad.append('%s:%d 写着 "%s 处命中 / %s 种"，把分隔空格从真报告里摘掉后此刻是 %s 处 / '
                               '%s 种（先跑 维护脚本/check_placeholder_guard.py，再看报告是不是真的变了）'
                               % (rel, i, m.group(1), m.group(2), GJ.get('retro_hits'),
                                  len(GJ.get('retro_kinds') or [])))
            # 第三族同样**不豁免过去时**：变异核验的例数每次重跑那个脚本都能现算。
            for m in MUT_CASES.finditer(ln):
                if tuple(int(x) for x in m.groups()) != MUT_WANT:
                    bad.append('%s:%d 写着 "%s"，变异核验台账此刻是 %s 例（变异体 %s、良性 %s）'
                               '（先跑 维护脚本/check_r11_mutation.py）'
                               % (rel, i, m.group(0), MUT_WANT[0], MUT_WANT[1], MUT_WANT[2]))
    return bad


# =========================================== 表格行的列数：一个竖线**是否**分裂单元格，取决于它
# 前面连续反斜杠的个数是奇还是偶 ⇒ 生成器多打一个反斜杠就等于没转义（本轮实测：
# `so10_thresholds.py` 用两个反斜杠转义裸竖线 ⇒ 报告里两行各多出 2 个不存在的列），
# 手写文档里一个 `$|B-L|=2$` 同样把行切开。两类都只错位、不变红：数值门禁与占位符核对都看不见，
# 所以这条核对按"每行的分裂竖线数 == 其表头"扫五份手写文档、两份生成的表与三份生成的报告。
SPLIT_PIPE = re.compile(r'\|')


def split_pipes(line):
    r"""返回真正分裂单元格的竖线位置：连续反斜杠个数为**奇数**者被转义（GFM 的判据）。"""
    out = []
    for m in SPLIT_PIPE.finditer(line):
        p = m.start()
        n = 0
        while p - n - 1 >= 0 and line[p - n - 1] == '\\':
            n += 1
        if n % 2 == 0:
            out.append(p)
    return out


def md_tables(text):
    r"""切表：连续的以 `|` 开头的行算一张表，至少要有表头 + 分隔行两行。"""
    cur, out = [], []
    for i, ln in enumerate(text.split('\n'), 1):
        if ln.lstrip().startswith('|'):
            cur.append((i, ln))
        else:
            if len(cur) >= 2:
                out.append(cur)
            cur = []
    if len(cur) >= 2:
        out.append(cur)
    return out


TABLE_DOCS = HAND_DOCS + ('06_场元数据表.md',
                          '验证脚本/SO10链统一报告.md', '验证脚本/SO10表示论报告.md',
                          '验证脚本/SO10阈值报告.md')


def check_tables():
    r"""(违规清单, 表数, 行数)：只判列数、不判内容 —— 内容对不对由仪器管，这里管"渲染出来还是不是一张表"。"""
    bad, ntab, nrow = [], 0, 0
    for rel in TABLE_DOCS:
        p = ROOT / rel
        if not p.exists():
            bad.append('%s：不存在 ⇒ 核对不能对着一份读不到的文件说"没问题"' % rel)
            continue
        for tb in md_tables(p.read_text(encoding='utf-8')):
            ntab += 1
            hdr_i, hdr = tb[0]
            want = len(split_pipes(hdr))
            for i, ln in tb:
                nrow += 1
                got = len(split_pipes(ln))
                if got != want:
                    bad.append('%s:%d 这一行有 %d 条分裂竖线，表头（:%d）只有 %d 条 ⇒ 有竖线没被'
                               '转义（要**奇数**个反斜杠才算转义，偶数个 = 没转义；表示绝对值请用'
                               ' \\lvert/\\rvert）' % (rel, i, got, hdr_i, want))
    return bad, ntab, nrow


# ---- 第 6 条排版不变量：紧跟字母的反斜杠串，长度必须是 1 --------------------------------
# 翻倍有两个来源：raw 字面量不消费转义（源码里手写 `$\\nu$` 就原样落地），以及 str(容器) 会把
# 元素里本就合法的反斜杠转义成两个（§13 的"算得/应为/备注"三列是 repr 转储 —— 本轮 67 处全出自这里）。
# 两条路落进文件后同形：MathJax 把 `\\` 读成换行、后面的控制词降级成斜体字母。表示论引擎写盘前判
# 自己一份（so10_reps 第五条），这里判**磁盘上此刻**的那几份 —— 理由与 check_tables() 相同：
# 翻倍是排版层的事，一条数值门禁都看不见它。
BSRUN = re.compile(r'\\+')
BWORD = re.compile(r'[A-Za-z]+')


def bs_sites(text, strip_code=True):
    r"""→ (翻倍处数, 合法单反斜杠处数, [(行号, 串)])。逐处先摘掉行内代码：文档里"写两个反斜杠 =
    一个字面反斜杠 + 一根照常分裂单元格的竖线"那类句子是在**引用**缺陷，不是缺陷。摘的时候用**等长
    空白**顶掉，行号与列位置一概不动 —— 豁免不许移动读者的坐标（否则被顶掉的段落同时逃过定位）。
    后面不跟字母的串（`\\{`、`\\ ` 这类转义花括号/换行）不在本条范围内。"""
    def blank(m):
        return ''.join('\n' if c == '\n' else ' ' for c in m.group(0))
    body = CODE_SPAN.sub(blank, text) if strip_code else text
    dbl = one = 0
    hits = []
    for i, ln in enumerate(body.split('\n'), 1):
        for m in BSRUN.finditer(ln):
            w = BWORD.match(ln[m.end():])
            if not w:
                continue
            if len(m.group(0)) == 1:
                one += 1
            else:
                dbl += 1
                hits.append((i, m.group(0) + w.group(0)))
    return dbl, one, hits


def check_bs_runs(docs=None):
    r"""(违规清单, 读数)。读数里的 `exempt` = 落在行内代码里、因而被豁免的翻倍处数 ——
    豁免必须带读数，否则"这一段本来就在引用缺陷"只是一个没人能核对的说法。"""
    bad = []
    files = dbl = one = ex = 0
    for rel in (docs or TABLE_DOCS):
        p = ROOT / rel
        if not p.exists():
            bad.append('%s：不存在 ⇒ 核对不能对着一份读不到的文件说"没问题"' % rel)
            continue
        txt = p.read_text(encoding='utf-8')
        d, s, hits = bs_sites(txt)
        raw_d, _, _ = bs_sites(txt, strip_code=False)
        files += 1
        dbl += d
        one += s
        ex += raw_d - d
        for i, tok in hits:
            bad.append('%s:%d 反斜杠翻倍成 %s ⇒ MathJax 把它读成换行、后面的控制词降级成斜体字母'
                       '（repr 转储或 raw 字面量多打一个，两条路数值门禁都看不见）' % (rel, i, tok))
    return bad, {'files': files, 'double': dbl, 'single': one, 'exempt': ex}


def main():
    write_csv(ROOT / '场元数据表.csv', META_HEADER, META)
    (ROOT / '06_场元数据表.md').write_text(
        clean(META_DOC.replace('{table}', md_table(META_HEADER, META)), '06_场元数据表.md'),
        encoding='utf-8')

    write_csv(ROOT / '现象覆盖矩阵.csv', PHEN_HEADER, PHEN)
    ok_status = ('已确立', '已验证')
    n_ok = sum(1 for r in PHEN if any(r[5].startswith(s) for s in ok_status))
    n_part = sum(1 for r in PHEN if '部分' in r[5] or '定性' in r[5])
    n_untest = sum(1 for r in PHEN if '未检验' in r[5])
    n_fail = len(PHEN) - n_ok - n_part - n_untest
    tot = len(PHEN)

    def pct(n):
        return '%.1f' % (100.0 * n / tot)

    phen_md = (PHEN_DOC.replace('{table}', md_table(PHEN_HEADER, PHEN))
               .replace('{n_ok}', str(n_ok)).replace('{p_ok}', pct(n_ok))
               .replace('{n_part}', str(n_part)).replace('{p_part}', pct(n_part))
               .replace('{n_untest}', str(n_untest)).replace('{p_untest}', pct(n_untest))
               .replace('{n_fail}', str(n_fail)).replace('{p_fail}', pct(n_fail))
               .replace('{mgut_band}', MGUT_BAND)
               .replace('{tau_band}', TAU_BAND)
               .replace('{gates_chain}', str(N_CHAIN))
               .replace('{gates_reps}', str(N_REPS))
               .replace('{yuk_channels}', YUK_TXT)
               .replace('{inv_ledger}', INV_TXT)
               .replace('{chan_split}', CHAN_TXT)
               .replace('{guard_cases}', GUARD_TXT)
               .replace('{retro_bleed}', RETRO_TXT)
               .replace('{gates_total}', GATES_TXT))
    # 新增一个读数却忘了接线 ⇒ 花括号会原样印进报告（与表示论引擎那条"未替换占位符"同一失效族）
    docs = {'06_场元数据表.md': (ROOT / '06_场元数据表.md').read_text(encoding='utf-8'),
            '07_现象覆盖矩阵.md': phen_md}
    left = {}
    for k, v in docs.items():
        toks, odd = [], []
        for i, blk in doc_blocks(v):
            prose = CODE_SPAN.sub('', blk)
            if prose.count('$') % 2:
                odd.append(i)
            toks += TOKEN.findall(MATH_SPAN.sub('', prose))
        if toks or odd:
            left[k] = '占位符 %s｜落单 $ 的块（行号）%s' % (sorted(set(toks)) or '无', odd or '无')
    if left:
        print('[FAIL] 生成的文里有未替换的模板占位符 ⇒ 接线漏了，别让花括号冒充读数：%s' % left)
        return 1
    (ROOT / '07_现象覆盖矩阵.md').write_text(clean(phen_md, '07_现象覆盖矩阵.md'), encoding='utf-8')
    print('已生成：场元数据表（{} 行）、现象覆盖矩阵（{} 行）'.format(len(META), len(PHEN)))
    # SO(10) 读数来自仪器 JSON、排版防护的例数来自 check_placeholder_guard.json：读不到就**显式失败**，
    # 而不是留着上一轮的字面量冒充通过（矩阵上一版把"8 例、当前 8/8 PASS"写死在模板里，
    # 本脚本给它加到第 12 例的那一刻，那句话就成了假话 —— 正是这一族要防的东西）
    missing = [x for x in (MGUT_BAND, TAU_BAND, GATES_TXT, YUK_TXT, INV_TXT, CHAN_TXT, GUARD_TXT,
                           RETRO_TXT)
               if x in (MISSING, GUARD_MISSING)]
    if missing:
        print('[FAIL] 仪器/防护读数缺失 ⇒ 矩阵中 %d 处为占位文本'
              '（先跑 验证脚本/so10_*.py 与 维护脚本/check_placeholder_guard.py，再重跑本脚本）'
              % len(missing))
        return 1
    if GATE_FAIL:
        print('[FAIL] 门禁未全通过：%s ⇒ 本表不得引用"全 PASS"'
              % '、'.join('%s（PASS %d/%d）' % (n, p, t) for n, t, p in GATE_FAIL))
        return 1
    # R11 判据那道**外部**变异核验的台账也走接线：读不到、账不平、或它切锚点时那份引擎已经漂了，
    # 一律非零退出 —— 一台隔了很久没再跑的仪器不能替今天的文档作证（引擎每改一次，这里就要求重跑一次）。
    mut_bad = check_mutation_ledger()
    for b in mut_bad:
        print('[MUT] %s' % b)
    tab_bad, ntab, nrow = check_tables()
    bs_bad, BS = check_bs_runs()
    doc_bad = check_docs()
    if not mut_bad:
        print('       SO(10) 读数：M_GUT %s；τ_p %s；门禁 %s' % (MGUT_BAND, TAU_BAND, GATES_TXT))
        print('       %s' % YUK_TXT)
        print('       %s' % INV_TXT)
        print('       %s' % CHAN_TXT)
        print('       排版防护的核验也走接线（缺失即非零退出）：%s' % GUARD_TXT)
        print('       "修好前留着多少处未定义控制词"同样现算（摘掉全文分隔空格 = 回到修好前）：%s'
              % RETRO_TXT)
        print('       判据的外部变异核验走接线（台账缺失／引擎漂了即非零退出）：%s 例（变异体 %s、'
              '良性 %s）verdict=%s，基线 %s/%s 项 PASS 且等于报告 JSON 的 tests 条数 %s，'
              '锚定的引擎 %s 字节（与磁盘此刻一致）'
              % (WJ['cases_total'], WJ['mutants'], WJ['benign'], WJ['verdict'],
                 MUT_BASE['pass'], MUT_BASE['gates'], WJ['engine_json_tests'],
                 WJ['target_bytes']))
    for b in doc_bad:
        print('[DOC] %s' % b)
    for b in tab_bad:
        print('[TABLE] %s' % b)
    for b in bs_bad:
        print('[BSRUN] %s' % b)
    if doc_bad or tab_bad or bs_bad or mut_bad:
        print('[FAIL] 手写文档里的门禁数与仪器不一致：%d 处；表格行的列数与表头不一致：%d 处；'
              '反斜杠翻倍：%d 处；变异核验台账不成立：%d 处（改文档，别让表跑在文前面。四类**一起**判：'
              '先返回门禁数的那一版会把列数缺陷藏进下一次运行、先返回台账的那一版会把文档里的过期'
              '门禁数藏进下一次运行 = 同族 fail-open，台账一漂就整批跳过文档核对）'
              % (len(doc_bad), len(tab_bad), len(bs_bad), len(mut_bad)))
        return 1
    now = led = 0
    for rel in HAND_DOCS:
        for _, ln in doc_blocks((ROOT / rel).read_text(encoding='utf-8')):
            if not (GATE_MENTION.search(ln) or GATE_TRIPLE.search(ln) or GATE_NOW.search(ln)
                    or SELFCHK.search(ln) or GUARD_CASES.search(ln) or BLEED.search(ln)
                    or MUT_CASES.search(ln)):
                continue
            now += 0 if HISTORIC.search(ln) else 1
            led += 1 if HISTORIC.search(ln) else 0
    print('       手写文档里 %d 处**现在时**门禁数/合计/自检数/防护例数/缺陷处数/变异核验例数'
          '（按段落与表格行归并）'
          '与仪器此刻一致；'
          '另有 %d 处带日期/阶段标记的台账段落 —— 其中的"三台合计"按当日记账保留不核对，'
          '单台仪器数与"现 N 项"仍然核对' % (now, led))
    print('       表格列数核对：%d 张表 / %d 行，每一行的分裂竖线数与其表头一致'
          '（扫描范围 = 5 份手写文档 + 2 份生成的表 + 3 份生成的报告；判据是"奇数个前导反斜杠'
          '才算转义"，两个反斜杠等于没转义 ⇒ 生成器多打一个反斜杠就会多出列，而数值门禁全绿）'
          % (ntab, nrow))
    print('       反斜杠翻倍核对：%d 份文件里"紧跟字母的反斜杠串"共 %d 处合法（长度为 1）、%d 处翻倍；'
          '另有 %d 处翻倍落在行内代码里 —— 那是在**引用**缺陷本身（如"两个反斜杠等于没转义"），'
          '按等长空白摘掉后行号与列位一概不动。判据只有一条：紧跟字母的串长度必须为 1；'
          '`\\\\{`、`\\\\ ` 这类转义花括号/换行不在范围内'
          % (BS['files'], BS['single'], BS['double'], BS['exempt']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
