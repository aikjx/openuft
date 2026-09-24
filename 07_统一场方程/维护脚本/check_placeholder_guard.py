# -*- coding: utf-8 -*-
"""核验两条"报告排版防护"**确实在接收流量**。

为什么要有这个文件：2026-09-24 一天之内三次踩到同一族缺陷——"加了读数忘了接线""写了断言但断言
自己没被喂到流量"。植入式核验的第一版就是因为上游门禁没跑而过层，导致**假绿**。故本脚本把两类
样例固定下来：植入的槽位必须被抓、LaTeX 的花括号必须不报，并以退出码给出结论。

第二类防护（第 9~14 例）核验 `so10_reps.py` 的第 4 条排版不变量：`\lvert`/`\rvert` 后紧跟字母或
数字时，TeX 按最长匹配把它读成**一个未定义控制词**（`\lvertB`）⇒ 整段公式报错，而全部数值门禁照绿。
这一族的教训反过来用在这里：不只看正则能不能匹配，而是直接调**真的在产出报告**的那个函数
（`table_row_safe`），并把去掉分隔符后的同一行送回去，要求不变量必须命中；第 5~6 例再把同一件事做到
**整份报告**上，于是文档里"修好前留着多少处"那句话从记忆变成可重跑的读数（进 JSON 的 `retro_*`，
由 `build_tables.check_docs()` 的 `BLEED` 反向核对）。

用法： python -B check_placeholder_guard.py     （0 = 防护按预期工作）
      同时把本脚本自己的读数写进同目录的 check_placeholder_guard.json，供 build_tables.py 接线。
"""
import importlib.util
import io
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('bt', str(HERE / 'build_tables.py'))
bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bt)
spec_r = importlib.util.spec_from_file_location('reps',
                                                str(HERE.parent / '验证脚本' / 'so10_reps.py'))
reps = importlib.util.module_from_spec(spec_r)
spec_r.loader.exec_module(reps)


def scan(text):
    """与 build_tables.main() 里那段核对同一套规则（复用同一批正则与同一分块函数）。"""
    toks, odd = [], []
    for i, blk in bt.doc_blocks(text):
        prose = bt.CODE_SPAN.sub('', blk)
        if prose.count('$') % 2:
            odd.append(i)
        toks += bt.TOKEN.findall(bt.MATH_SPAN.sub('', prose))
    return sorted(set(toks)), odd


CASES = [
    ('植入未接线槽位 ⇒ 必须抓到', 'body {inv_ledger} here', ['{inv_ledger}'], []),
    (r'LaTeX 上/下标花括号 ⇒ 必须不报', r'math $\omega^{ab}$ and $U(1)_{em}$ end', [], []),
    (r'LaTeX 组 \rm ⇒ 必须不报', r'$\Delta_{\rm em}$ only', [], []),
    ('槽位与数学同段 ⇒ 只报槽位', r'$U(1)_{em}$ leaves {n_ok} out', ['{n_ok}'], []),
    ('行内代码里的 $ 不得与真数学配对', 'a `$` pair then $x^{ab}$ b', [], []),
    ('落单的 $ ⇒ 必须报（否则后半篇失去保护 = fail-open）', 'x $ y {zz}', ['{zz}'], [1]),
    ('表格行独立成块', '| a | {b} |\n| c | d |', ['{b}'], []),
    ('跨行段落归并后仍算一块', 'line one {n_ok}\n  line two $x^{ab}$', ['{n_ok}'], []),
]

# ---- 第 4 条排版不变量：\lvert/\rvert 后面必须留分隔符（防护对象 = so10_reps.table_row_safe）----
ROW = ('| $120_H$ 能否破 $B-L$ | 未判定 | 其 $(1,1,1)_{\\pm2}$ 分量带 $|Q|=1$，'
       '取期望值即破 $U(1)_{em}$ |')
REPORT = HERE.parent / '验证脚本' / 'SO10表示论报告.md'


def delimiter_checks():
    """(读数行, 附带读数)：本组第 2 例（摘掉分隔符）与第 4 例（读磁盘上的真报告）一起构成
    "这条防护会见血"的证据 —— 否则"0 命中"可能只是没喂东西进来。

    第 5~6 例把同一件事做到**整份报告**上：修法是"只补一个空格"，所以把全文的分隔空格再摘掉
    就逐字节回到修好前那一版 ⇒ 文档里"修好前留着多少处"这个数由这里**算出来**，而不是记在那里。
    上一版的见证文件（修好前的报告副本）只活在临时目录里，报告本身又没进 git ⇒ 那句话当时
    没有任何读者能重跑，正是本仓库登记过的那一族。"""
    safe = reps.table_row_safe(ROW)
    # 复刻修好前的输出：把刚补上的分隔空格再摘掉 —— 不硬编码中文，避免"样例与代码各行其是"
    retro = re.sub(r'\\([lr])vert ', r'\\\1vert', safe)
    fired = sorted(set(reps.DELIM_MUNCH.findall(retro)))
    txt = REPORT.read_text(encoding='utf-8')
    live = sorted(set(reps.DELIM_MUNCH.findall(txt)))
    n_sep = len(re.findall(r'\\[lr]vert ', txt))
    bleed = reps.DELIM_MUNCH.findall(re.sub(r'\\([lr])vert ', r'\\\1vert', txt))
    kinds = sorted(set(bleed))
    n_safe = len(re.findall(r'\\[lr]vert(?![A-Za-z0-9])',
                            re.sub(r'\\([lr])vert ', r'\\\1vert', txt)))
    return [
        ('表格里的裸竖线改写为**带分隔符**的 \\lvert/\\rvert',
         '$\\lvert Q\\rvert =1$' in safe,
         'table_row_safe 给出：%s' % safe),
        ('摘掉分隔符（= 修好前那一版）⇒ 不变量必须命中，否则它是空转的',
         bool(fired), 'DELIM_MUNCH 在摘掉分隔符的同一行上命中 %s' % fired),
        ('正文行（不以 | 开头）原样返回：防护不越界改写',
         reps.table_row_safe('正文 $|Q|=1$ 结束') == '正文 $|Q|=1$ 结束',
         '被改写成：%s' % reps.table_row_safe('正文 $|Q|=1$ 结束')),
        ('此刻磁盘上的报告：确有改写发生（%d 处分隔符）且 0 处命中' % n_sep,
         n_sep > 0 and not live,
         '命中 %s ⇒ 报告里有公式会被 TeX 读成未定义控制词' % live),
        ('把整份报告的分隔空格摘掉 ⇒ 防护必须在**全文**上见血：%d 处命中 / %d 种控制词'
         % (len(bleed), len(kinds)),
         bool(bleed),
         '摘掉 %d 处分隔符后一处不命中 ⇒ 这条断言没在接收流量，而文档里那个"修好前 %d 处"'
         '就成了无从重跑的记忆' % (n_sep, len(bleed))),
        ('账要对上：命中 %d 处 + 摘掉后仍安全 %d 处 = 全文 %d 处分隔符（否则那个数不是分隔符的函数）'
         % (len(bleed), n_safe, n_sep),
         len(bleed) + n_safe == n_sep,
         '差 %d 处：摘空格这一步动了不该动的字符' % (n_sep - len(bleed) - n_safe)),
    ], {'separators': n_sep, 'hits': live, 'planted_hits': fired,
        'retro_hits': bleed, 'retro_kinds': kinds,
        'retro_kind_counts': [[k, bleed.count(k)] for k in kinds], 'retro_safe': n_safe}


def table_checks():
    r"""核验 build_tables.check_tables() 那条"表格行的分裂竖线数 == 表头"的核对会见血。

    它抓的是本轮**实测到的两处**真实缺陷（`so10_thresholds.py` 用两个反斜杠转义竖线 ⇒ 生成文里
    两行各多出一条分裂竖线；手写文档里的 `$|Δ(B−L)|=2$` ⇒ 三行同理），所以这里不凭空造样例，
    而是把修好的那一行**逐字节改回修好前**，要求核对必须点出同一处；再用"一个反斜杠"的合法转义
    作对照 —— 若那一记也被报，说明核对是在数竖线而不在数**没被转义**的竖线（空转的另一种）。
    不动仓库里的文档：把被扫的文件复制到临时目录、改完再指过去核对。
    """
    BS = chr(92)
    tmp = Path(tempfile.mkdtemp(prefix='AM_tableguard_'))
    keep = bt.ROOT
    anchor = '$' + BS + 'lvert ' + BS + 'Delta(B-L)' + BS + 'rvert =2$'
    plants = (('把修好的那一行改回本轮修前的样子（两个裸竖线）⇒ 必须被抓',
               '$' + '|' + BS + 'Delta(B-L)' + '|' + '=2$', True),
              ('把转义写成**两个**反斜杠（= 生成器上一版的缺陷）⇒ 必须被抓',
               '$' + BS + BS + '|B-L' + BS + BS + '|=2$', True),
              ('把转义写成**一个**反斜杠（合法）⇒ 不得报（否则它数的是竖线，不是没转义的竖线）',
               '$' + BS + '|B-L' + BS + '|=2$', False))
    out, notes = [], []
    srcs = {}
    try:
        for rel in bt.TABLE_DOCS:
            p = keep / rel
            if not p.exists():
                return [('被扫文件缺失：%s ⇒ 核对无法投放' % rel, False, '')], []
            srcs[rel] = p.read_text(encoding='utf-8')
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            (tmp / rel).write_text(srcs[rel], encoding='utf-8')
        rel0 = '09_已知局限与否定清单.md'
        if anchor not in srcs[rel0]:
            return [('文档里找不到锚点 %s ⇒ 取证无法投放（先改文档再核验）' % anchor, False, '')], []
        # 投放**每一处**锚点，于是"该被抓的是哪些行"由文件自己说出，而不是由我此刻记得的行号说出
        # （写死 1 处的上一版在同一次运行里就被 09 里那两处锚点证伪：它报 2 处 ⇒ 期望是我的假设错了）
        want_rows = sorted(i for i, ln in enumerate(srcs[rel0].split('\n'), 1) if anchor in ln)
        bt.ROOT = tmp
        base, ntab, nrow = bt.check_tables()
        notes.append('基线此刻扫 %d 张表 / %d 行，违规 %d 处' % (ntab, nrow, len(base)))
        out.append(('此刻磁盘上的文档与生成文：每行与其表头同列数（%d 张表 / %d 行）'
                    % (ntab, nrow), not base,
                    '违规 %d 处：%s' % (len(base), base[:2])))
        for name, repl, must in plants:
            (tmp / rel0).write_text(srcs[rel0].replace(anchor, repl), encoding='utf-8')
            bad, _, _ = bt.check_tables()
            got = sorted(int(b.split(':', 1)[1].split(' ')[0]) for b in bad if b.startswith(rel0))
            exp = want_rows if must else []
            notes.append('%s ⇒ 投放 %d 行、抓到 %s' % (name, len(want_rows), got or '无'))
            out.append((name, got == exp,
                        '抓到第 %s 行，期望第 %s 行（全文件此刻共报 %d 处）'
                        % (got or '无', exp or '无', len(bad))))
    finally:
        bt.ROOT = keep
        shutil.rmtree(tmp, ignore_errors=True)
    return out, notes


def doc_check_checks(total):
    """核验 build_tables.check_docs() 那条"手写文档里的现在时数字"核对会失败 —— 它自己也要取证。
    不动仓库里的文档：把五份手写文档复制到临时目录，**同一份快照里投放两处过期数字**（README 的
    防护例数改错 3、08 的变异核验例数改错 +3），再指过去核对。两族必须各自被抓到 —— 一族抓到
    不能替另一族作证。`total` 是本次运行的总例数 ⇒ 第 1 例同时钉住"README 里写的例数 == 本脚本
    此刻的例数"。
    为什么变异核验那一族值得单独投一处：它是本轮新接的线，而**没被植过错的数字等于没被核对过**。
    实测细节（投放位置不是随手挑的）：那句"6 例（变异体 4、良性 1）"在手写文档里有四处，四处所在
    段落**全部**被 HISTORIC 认成过去时（三处只因为段里有一个 `→`）⇒ 段落级豁免只要扩到这一族，
    它就一处都不核对。故把投放放在 08 的那一处：它被抓到同时证明了两件事 —— 线是活的、豁免吞不掉它。
    （README 那一处不能当投放点：它的句子在源码里是折行的，原文里根本没有连续的那个字符串。）"""
    tmp = Path(tempfile.mkdtemp(prefix='AM_docsguard_'))
    keep = bt.ROOT
    keep_gj = bt.GJ
    want = '%d 例固定样例' % total
    if not all(isinstance(x, int) for x in bt.MUT_WANT):
        return [('变异核验台账不可读 ⇒ 这一族的投放没有出处'
                 '（先跑 维护脚本/check_r11_mutation.py）', False,
                 'bt.MUT_WANT=%s' % (bt.MUT_WANT,))], []
    mut_want = '%d 例（变异体 %d、良性 %d）' % bt.MUT_WANT
    mut_drift = '%d 例（变异体 %d、良性 %d）' % (bt.MUT_WANT[0], bt.MUT_WANT[1] + 3,
                                                 bt.MUT_WANT[2])
    # 本组的被检对象是"文档里的例数 == 防护脚本的例数"，而**这一次**的例数只有跑到这里才知道：
    # bt.GJ 是导入时读的上一轮 JSON ⇒ 只要例数这一轮有变化，check_docs() 就必然报"文档与 JSON 不一致"
    # （上一轮 14→14 恰好把它掩盖了）。故把这一次的数字喂给被检函数；跨文件的真核对由生成器做——
    # 它读的是本脚本结尾刚写出的 JSON，依赖顺序 harness → build_tables 因此是这套取证的组成部分。
    bt.GJ = dict(bt.GJ, cases_total=total)

    def fams(bads):
        """按族分账：'例固定样例' 与 '变异核验台账' 各自出现在自己那一族的投诉文案里。"""
        return ([b for b in bads if '例固定样例' in b],
                [b for b in bads if '变异核验台账' in b])

    try:
        for rel in bt.HAND_DOCS:
            shutil.copyfile(keep / rel, tmp / rel)
        bt.ROOT = tmp
        rp, mp = tmp / 'README.md', tmp / '08_预言与判据.md'
        rtext = rp.read_text(encoding='utf-8')
        mtext = mp.read_text(encoding='utf-8')
        if want not in rtext:
            return [('README 里找不到 "%s" ⇒ 取证无法投放（先改文档再核验）' % want, False,
                     '本脚本此刻共 %d 例' % total)], []
        if mut_want not in mtext:
            return [('08 里找不到 "%s" ⇒ 取证无法投放（先改文档再核验）' % mut_want, False,
                     '变异核验台账此刻是 %s' % (bt.MUT_WANT,))], []

        def snap(r, m):
            rp.write_text(r, encoding='utf-8')
            mp.write_text(m, encoding='utf-8')
            return fams(bt.check_docs())

        clean = snap(rtext, mtext)
        drift = snap(rtext.replace(want, '%d 例固定样例' % (total - 3)),
                     mtext.replace(mut_want, mut_drift))
        # 再往**同一个句子**前头塞一个"第X项"：它是 HISTORIC 认得的阶段/台账记号。若豁免的粒度是段落
        # 而不是这个数字所在的句子，这一记就会把上面那一处一起免检 —— 本轮实测到的正是这件事
        # （README 里一句"下面第十项里…"曾把 176 项合计与防护例数同时变成不核对）。
        muted = snap(rtext.replace(want, '（第十项续）%s' % want), mtext)
        bled = snap(rtext.replace(want, '（第十项续）%d 例固定样例' % (total - 3)),
                    mtext.replace(mut_want, mut_drift))
    finally:
        bt.ROOT = keep
        bt.GJ = keep_gj
        shutil.rmtree(tmp, ignore_errors=True)
    return [
        ('手写文档里两处现在时例数与本脚本/变异台账此刻一致 ⇒ 数字核对无违规（两处都留原值）',
         not clean[0] and not clean[1],
         '违规 %d+%d 处：%s' % (len(clean[0]), len(clean[1]), (clean[0] + clean[1])[:2])),
        ('同一份快照里改错两处（README 防护例数 −3、08 变异体数 +3）⇒ 两族各自点出一处'
         '（08 那一处所在段落带 `→` 台账记号 ⇒ 顺带证明段落级豁免吞不掉它）',
         len(drift[0]) == 1 and len(drift[1]) == 1,
         '抓到 %d+%d 处：%s' % (len(drift[0]), len(drift[1]), (drift[0] + drift[1])[:2])),
        ('同段落里加一个"第X项"台账记号、数字改对 ⇒ 不得凭空报事（豁免不靠记号，数字对就是对）',
         not muted[0] and not muted[1],
         '误报 %d+%d 处：%s' % (len(muted[0]), len(muted[1]), (muted[0] + muted[1])[:2])),
        ('"第X项"与改错的数字同段落 ⇒ 两处仍必须各自被抓（段落级豁免会把它们吞掉）',
         len(bled[0]) == 1 and len(bled[1]) == 1,
         '抓到 %d+%d 处：%s' % (len(bled[0]), len(bled[1]), (bled[0] + bled[1])[:2])),
    ], [b[:120] for grp in (clean, drift, muted, bled) for b in grp[0] + grp[1]]


def main():
    bad = []
    for name, text, want_toks, want_odd in CASES:
        got_toks, got_odd = scan(text)
        ok = got_toks == want_toks and bool(got_odd) == bool(want_odd)
        print('%s %s' % ('PASS' if ok else 'FAIL', name))
        if not ok:
            print('       got=%s want=%s' % ((got_toks, got_odd), (want_toks, want_odd)))
            bad.append(name)
    extra, read = delimiter_checks()
    for name, ok, detail in extra:
        print('%s %s' % ('PASS' if ok else 'FAIL', name))
        if not ok:
            print('       %s' % detail)
            bad.append(name)
    tbl_extra, tbl_notes = table_checks()
    docs_extra, notes = doc_check_checks(len(CASES) + len(extra) + 4 + len(tbl_extra))
    for name, ok, detail in docs_extra:
        print('%s %s' % ('PASS' if ok else 'FAIL', name))
        if not ok:
            print('       %s' % detail)
            bad.append(name)
    # 打印排在最后 ⇒ 新增这一组的例号是 19~22，文档里"第 15~18 例"那句仍然成立
    for name, ok, detail in tbl_extra:
        print('%s %s' % ('PASS' if ok else 'FAIL', name))
        if not ok:
            print('       %s' % detail)
            bad.append(name)
    n = len(CASES) + len(extra) + len(tbl_extra) + len(docs_extra)
    print('=== %d/%d 例符合预期；防护规则：%s ==='
          % (n - len(bad), n, '接收流量' if not bad else '失灵'))
    # 本脚本自己的读数也进 JSON：覆盖矩阵里那句"可重跑的 N 例、当前 N/N PASS"由
    # build_tables.py 从这份文件接线，而不是手抄 —— 手抄正是本仓库登记过的失效族。
    (HERE / 'check_placeholder_guard.json').write_text(json.dumps(
        {'purpose': '核验三条"只错位不变红"的排版防护（未填槽位、\\lvert 分隔符、表格列数）确实在'
                    '接收流量，并取证两条数字核对会见血',
         'cases_slot': len(CASES), 'cases_delimiter': len(extra),
         'cases_table': len(tbl_extra), 'cases_doccheck': len(docs_extra),
         'cases_total': n,
         'pass': n - len(bad), 'all_pass': not bad, 'failed': bad,
         'live_separators': read['separators'], 'live_hits': read['hits'],
         'planted_hits': read['planted_hits'], 'doc_check_notes': notes,
         'table_check_notes': tbl_notes,
         'retro_hits': len(read['retro_hits']), 'retro_kinds': read['retro_kinds'],
         'retro_kind_counts': read['retro_kind_counts'], 'retro_safe': read['retro_safe'],
         'report_file': REPORT.name,
         'rules': ['生成文里不得留未填的 {} 槽位（落单的 $ 视为防护失效）',
                   '\\lvert/\\rvert 后不得紧跟字母或数字（TeX 最长匹配 ⇒ 未定义控制词）',
                   '手写文档里"N 例固定样例"必须等于本脚本此刻的例数（check_docs 的 GUARD_CASES）',
                   '手写文档里"N 处命中 / K 种"必须等于把分隔空格从真报告里摘掉后的此刻读数'
                   '（check_docs 的 BLEED ⇒ "修好前有多少处"是可重跑的，不是记忆）',
                   '手写文档里"N 例（变异体 K、良性 M）"必须等于变异核验台账此刻的读数'
                   '（check_docs 的 MUT_CASES ⇒ 读 check_r11_mutation.json，不抄；'
                   '该族与 GUARD_CASES/BLEED 同样**不豁免过去时**段落）',
                   '每一行表格的**分裂竖线数**必须等于其表头（check_tables ⇒ 竖线前要奇数个反斜杠'
                   '才算转义，两个反斜杠 = 没转义 = 行里多出不存在的列）']},
        ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
