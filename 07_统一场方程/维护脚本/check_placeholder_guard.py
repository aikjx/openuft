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

第 25~28 例是这一族第六次"先有真实缺陷、后有不变量"（`backslash_checks()`）：紧跟字母的反斜杠串长度必须为 1。翻倍有两个
来源——raw 字面量不消费转义，以及 `str(容器)`/repr 把数据里本就合法的反斜杠翻倍（本轮那 67 处全出自
后者）。它比前四条更隐蔽：**没有一条数值门禁能看见它**，且"引用缺陷的行内代码"这一族豁免本身可能
成为下一个 fail-open 现场 ⇒ 这一组除了投放正例，还专门核对豁免（摘掉反引号必须立刻见血）与
不在范围内的形态（`\\{`、`\\ ` 与一处真翻倍同放一行 ⇒ 只报那一处）。

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


def _bs_remap(text, pick, repl):
    """逐行把"满足 pick(长度) 且紧跟字母的反斜杠串"整串换成 repl，**跳过行内代码里的**那些
    （与 bs_sites 的豁免同一依据 ⇒ 投放与还原互为严格逆运算，豁免区一概不动）。"""
    out = []
    for ln in text.split('\n'):
        code = set()
        for m in bt.CODE_SPAN.finditer(ln):
            code.update(range(m.start(), m.end()))
        pieces, pos = [], 0
        for m in bt.BSRUN.finditer(ln):
            if (pick(len(m.group(0))) and m.start() not in code
                    and bt.BWORD.match(ln[m.end():])):
                pieces.append(ln[pos:m.start()])
                pieces.append(repl)
                pos = m.end()
        pieces.append(ln[pos:])
        out.append(''.join(pieces))
    return '\n'.join(out)


def _bs_unquote(text):
    """把**含有翻倍处**的行内代码的首尾反引号摘掉 ⇒ 那些翻倍从豁免区搬进核对区。
    只摘反引号、不动里面的字符，于是被豁免的那几处的位置与内容都由文件自己说出。"""
    out = []
    for ln in text.split('\n'):
        drop = set()
        for m in bt.CODE_SPAN.finditer(ln):
            span = m.group(0)
            for r in bt.BSRUN.finditer(span):
                if len(r.group(0)) >= 2 and bt.BWORD.match(span[r.end():]):
                    drop.add(m.start())
                    drop.add(m.end() - 1)
        out.append(''.join(c for i, c in enumerate(ln) if i not in drop))
    return '\n'.join(out)


def backslash_checks():
    r"""核验 build_tables.check_bs_runs()（第 6 条排版不变量）会见血，并且**豁免也是被核对的**。

    判据：一行里"紧跟字母的反斜杠串"长度必须是 1。两个来源会把长度变成 ≥2 —— raw 字面量不消费
    转义（源码里手写两个就原样落地两个），以及 repr/str(容器) 把数据里本就合法的反斜杠翻倍
    （本轮实测那 67 处全出自后者：§13 的"算得/应为/备注"三列是 repr 转储）。两条路落进文件后同形，
    MathJax 把双反斜杠读成换行、后面的控制词降级成斜体字母，而**一条数值门禁都看不见**。

    四例的分工：第 1 例基线（含"豁免必须带流量"），第 2 例把报告里每一处合法单反斜杠逐处改回翻倍
    —— 期望处数由**该文件自己**的 bs_sites 读数给出（写死行号的那一版一遇重新生成就假绿），并要求
    折叠回去逐字节还原；第 3 例专打豁免的粒度：把引用缺陷的那几处反引号摘掉，它们必须立刻变成违规
    （段落级豁免正是本仓库登记过的 fail-open 族）；第 4 例把不在范围内的 `\\ `、`\\{` 与一处真翻倍
    放进**同一行**，要求只报那一处 —— 范围写在注释里不算，被同一行扫过才算。
    不动仓库里的文件：复制到临时目录、投放后指过去核对。
    """
    BS = chr(92)
    tmp = Path(tempfile.mkdtemp(prefix='AM_bsguard_'))
    keep = bt.ROOT
    target = '验证脚本/SO10表示论报告.md'
    out, notes = [], []
    read = {}
    srcs = {}
    try:
        for rel in bt.TABLE_DOCS:
            p = keep / rel
            if not p.exists():
                return [('被扫文件缺失：%s ⇒ 核对无法投放' % rel, False, '')], [], {}
            srcs[rel] = p.read_text(encoding='utf-8')
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            (tmp / rel).write_text(srcs[rel], encoding='utf-8')
        bt.ROOT = tmp
        base, R = bt.check_bs_runs()
        per = dict((rel, bt.check_bs_runs(docs=[rel])[1]) for rel in bt.TABLE_DOCS)
        quoted = [rel for rel in bt.TABLE_DOCS if per[rel]['exempt'] > 0]
        read = {'files': R['files'], 'single': R['single'], 'double': R['double'],
                'exempt': R['exempt'], 'quoted_files': quoted}
        notes.append('基线此刻扫 %d 份文件：%d 处合法、%d 处翻倍、%d 处豁免（豁免在 %s）'
                     % (R['files'], R['single'], R['double'], R['exempt'], '、'.join(quoted) or '无'))
        out.append(('此刻磁盘上的 %d 份文件：%d 处翻倍（要求 0）／%d 处合法（要求 >0，否则这条判据'
                    '只是在数空）／%d 处落在行内代码里被豁免（要求 >0：一条从不被走到的豁免分支'
                    '等于没被核对过的说法）' % (R['files'], R['double'], R['single'], R['exempt']),
                    R['files'] == len(bt.TABLE_DOCS) and not base and R['double'] == 0
                    and R['single'] > 0 and R['exempt'] > 0,
                    '违规 %d 处：%s' % (len(base), base[:2])))
        # ---- 第 2 例：投放到生成报告上，期望处数 = 该文件此刻的合法处数 ----
        txt = srcs[target]
        self_dbl, self_one, _ = bt.bs_sites(txt)
        read['planted'] = self_one
        doubled = _bs_remap(txt, lambda n: n == 1, BS * 2)
        back = _bs_remap(doubled, lambda n: n >= 2, BS)
        (tmp / target).write_text(doubled, encoding='utf-8')
        bad2, R2 = bt.check_bs_runs()
        got = [b for b in bad2 if b.startswith(target)]
        notes.append('投放 %s：%d 处合法单反斜杠逐处翻倍 ⇒ 抓到 %d 处；折叠回去逐字节还原=%s'
                     % (target, self_one, len(got), back == txt))
        out.append(('把 %s 里每一处合法的"单反斜杠+字母"改回翻倍（本轮缺陷的成因形态）⇒ 必须'
                    '逐处被点名 %d 处 = 该文件自己的合法处数，且这些投诉全部只落在这一份文件上；'
                    '折叠回去必须逐字节还原 ⇒ 投放只动了那些处' % (target, self_one),
                    self_one > 0 and len(got) == self_one and len(bad2) == self_one
                    and self_dbl == 0 and back == txt,
                    '抓到 %d 处（期望 %d），全文件共报 %d 处；基线该文件自身翻倍 %d 处；还原=%s'
                    % (len(got), self_one, len(bad2), self_dbl, back == txt)))
        # ---- 第 3 例：摘掉"引用缺陷"的行内代码的反引号 ⇒ 豁免必须当场失效 ----
        for rel in quoted:
            (tmp / rel).write_text(_bs_unquote(srcs[rel]), encoding='utf-8')
        (tmp / target).write_text(txt, encoding='utf-8')
        bad3, R3 = bt.check_bs_runs()
        notes.append('摘掉 %s 的行内代码反引号 ⇒ 违规 %d 处（基线豁免 %d 处）、此刻豁免剩 %d 处'
                     % ('、'.join(quoted), len(bad3), R['exempt'], R3['exempt']))
        out.append(('摘掉那 %d 处"引用缺陷的行内代码"的反引号 ⇒ 它们必须立刻变成违规（%s）：'
                    '豁免的粒度是**一处行内代码**，不是整段——段落级豁免一旦扩到这一族就一处都不核对'
                    % (R['exempt'], '、'.join(quoted)),
                    len(bad3) == R['exempt'] and R3['exempt'] == 0 and R3['double'] == R['exempt']
                    and all(b.split(':', 1)[0] in quoted for b in bad3),
                    '违规 %d 处（期望 %d），此刻豁免 %d 处、翻倍 %d 处：%s'
                    % (len(bad3), R['exempt'], R3['exempt'], R3['double'], bad3[:2])))
        # ---- 第 4 例：负对照与正对照同行 ----
        # 先把第 2、3 例的投放**全部撤回**：否则这一例报的是"上一例留下的缺陷 + 这一例的投放"，
        # 而它的判据是"只报我投放的那一处"⇒ 不撤回就会像本轮第一次运行那样，把 4 处残留读成
        # 判据失灵（实测：共报 5 处、豁免 0 处）。每一例从干净的快照出发，例与例才互不替证。
        for rel in bt.TABLE_DOCS:
            (tmp / rel).write_text(srcs[rel], encoding='utf-8')
        ctl = '控制行：%s%s（转义花括号）%s%s（转义方括号）%s%s （换行）%salpha（这一处在范围内）' % (
            BS * 2, '{', BS * 2, '[', BS * 2, ' ', BS * 2)
        (tmp / target).write_text(txt + ctl + '\n', encoding='utf-8')
        bad4, R4 = bt.check_bs_runs()
        toks = [re.match(r'^\S+:\d+ 反斜杠翻倍成 (\S+)', b).group(1) for b in bad4]
        notes.append('同一行放 3 处不跟字母的串 + 1 处真翻倍 ⇒ 只报 %s' % toks)
        out.append(('在同一行里放「两个反斜杠+空格」「两个反斜杠+花括号」「两个反斜杠+方括号」'
                    '与一处「两个反斜杠+alpha」⇒ 只报后者一处（范围是"紧跟字母"这句话必须是'
                    '被测到的，不是写在注释里的；而同一行被扫过 ⇒ 前三处不是漏扫）',
                    len(bad4) == 1 and toks == [BS * 2 + 'alpha'] and R4['double'] == 1
                    and R4['exempt'] == R['exempt'],
                    '共报 %d 处，命中串 %s，豁免 %d 处：%s'
                    % (len(bad4), toks, R4['exempt'], bad4[:2])))
    finally:
        bt.ROOT = keep
        shutil.rmtree(tmp, ignore_errors=True)
    return out, notes, read


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
    # 变异核验那台文档门禁（check_mutation_ledger）自己也得有反例：它判的是"台账在替另一份文件作证"，
    # 一条永远不会响的分支比没有分支更糟 —— 四份文档正引用着这台仪器。一次改错六处（字节 +1、verdict
    # 改掉、tests 归零、caught 归零、删掉基线行、mutants 虚报 1），要求六条分支**各自**出一条投诉
    # （每条文案里有一个只属于它的子串；少一条就是那一条已经死了）；另把整份台账换成空的，要求
    # "缺失不是通过"那条也出。这一段必须在把 ROOT 指向临时目录**之前**跑：字节分支要比对磁盘上的真引擎。
    led_clean = bt.check_mutation_ledger()
    led_sick = bt.check_mutation_ledger(dict(
        bt.WJ, target_bytes=(bt.WJ.get('target_bytes') or 0) + 1, verdict='MISSED',
        engine_json_tests=0, caught=0,
        cases=[c for c in (bt.WJ.get('cases') or []) if c.get('kind') != 'baseline'],
        mutants=(bt.WJ.get('mutants') or 0) + 1))
    led_none = bt.check_mutation_ledger({})
    branches = ('字节', '此刻不是 CAUGHT', '基线夹具不成立', '自洽的基线行', 'kind 计数',
                '每一个变异体都要被点名抓住')
    hit = dict((k, sum(1 for b in led_sick if k in b)) for k in branches)
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
        # 站点普查打印在这里，**不抄进 README**：文档里抄一份"N 处"，下一次加站点它就是假话，
        # 而那正是这一族存在的理由。planted_hist 则钉住夹具自己有没有电 —— 投放点若落在一个
        # 没有台账记号的段落里，"段落级豁免吞不掉这一族"这句话就没被这一记证明过。
        site_n = site_h = 0
        site_free = []
        for rel in bt.HAND_DOCS:
            for i, ln in bt.doc_blocks((tmp / rel).read_text(encoding='utf-8')):
                if bt.MUT_CASES.search(ln):
                    site_n += 1
                    if bt.HISTORIC.search(ln):
                        site_h += 1
                    else:
                        site_free.append('%s:%d' % (rel, i))
        planted_hist = any(bt.MUT_CASES.search(ln) and bt.HISTORIC.search(ln)
                           for _i, ln in bt.doc_blocks(mtext))
        census = ('站点普查：%d 处带那句例数、其中 %d 处所在段落被 HISTORIC 认成过去时（未认成的：%s）'
                  '；投放那一处带台账记号=%s' % (site_n, site_h, '、'.join(site_free) or '无',
                                                planted_hist))

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
         '（一族抓到不替另一族作证）；且这一族的**每一处**站点所在段落都被 HISTORIC 认成过去时，'
         '投放那一处也在其中 ⇒ 段落级豁免一旦扩到它就等于一处都不核对'
         '（站点普查过期时这一例先响，别把"每一处"留在散文里当记忆）',
         len(drift[0]) == 1 and len(drift[1]) == 1 and planted_hist and site_h == site_n,
         '抓到 %d+%d 处、planted_hist=%s：%s ｜ %s'
         % (len(drift[0]), len(drift[1]), planted_hist, (drift[0] + drift[1])[:2], census)),
        ('同段落里加一个"第X项"台账记号、数字改对 ⇒ 不得凭空报事（豁免不靠记号，数字对就是对）',
         not muted[0] and not muted[1],
         '误报 %d+%d 处：%s' % (len(muted[0]), len(muted[1]), (muted[0] + muted[1])[:2])),
        ('"第X项"与改错的数字同段落 ⇒ 两处仍必须各自被抓（段落级豁免会把它们吞掉）',
         len(bled[0]) == 1 and len(bled[1]) == 1,
         '抓到 %d+%d 处：%s' % (len(bled[0]), len(bled[1]), (bled[0] + bled[1])[:2])),
        ('磁盘上那份真变异核验台账过文档门禁的六条分支：此刻无违规',
         not led_clean, '违规 %d 条：%s' % (len(led_clean), led_clean[:2])),
        ('把台账一次改错六处 ⇒ 六条分支各自出一条，且台账整个换成空的时"缺失不是通过"那条也出'
         '（一条永不响的分支比没有分支更糟：文档里那句"走接线"就成了假话）',
         all(v == 1 for v in hit.values()) and len(led_sick) == len(branches)
         and len(led_none) == 1 and '没有出处' in led_none[0],
         '分支命中 %s；改错后共 %d 条：%s；空台账 %d 条：%s'
         % (hit, len(led_sick), [b[:60] for b in led_sick[:2]], len(led_none),
            [b[:60] for b in led_none])),
    ], ([census] + [b[:120] for grp in (clean, drift, muted, bled) for b in grp[0] + grp[1]]
        + [b[:120] for b in led_sick])


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
    bs_extra, bs_notes, bs_read = backslash_checks()
    docs_extra, notes = doc_check_checks(
        len(CASES) + len(extra) + 6 + len(tbl_extra) + len(bs_extra))
    for name, ok, detail in docs_extra:
        print('%s %s' % ('PASS' if ok else 'FAIL', name))
        if not ok:
            print('       %s' % detail)
            bad.append(name)
    # 打印顺序 = 例号顺序：slot 1~8、delimiter 9~14、doccheck 15~20、table 21~24、backslash 25~28。
    # 表格组排在这里（不是最后）⇒ 文档里"第 21~24 例"那句以这一行为出处；任何一组加例都要同步改
    # 那一处，而例数本身由 GUARD_CASES 核对钉住（见 build_tables.check_docs）。
    for name, ok, detail in tbl_extra:
        print('%s %s' % ('PASS' if ok else 'FAIL', name))
        if not ok:
            print('       %s' % detail)
            bad.append(name)
    # 同上：本组（反斜杠翻倍）打印在最后 ⇒ 例号 25~28，文档里"第 21~24 例"那句仍然为真
    for name, ok, detail in bs_extra:
        print('%s %s' % ('PASS' if ok else 'FAIL', name))
        if not ok:
            print('       %s' % detail)
            bad.append(name)
    n = len(CASES) + len(extra) + len(tbl_extra) + len(docs_extra) + len(bs_extra)
    print('=== %d/%d 例符合预期；防护规则：%s ==='
          % (n - len(bad), n, '接收流量' if not bad else '失灵'))
    # 本脚本自己的读数也进 JSON：覆盖矩阵里那句"可重跑的 N 例、当前 N/N PASS"由
    # build_tables.py 从这份文件接线，而不是手抄 —— 手抄正是本仓库登记过的失效族。
    (HERE / 'check_placeholder_guard.json').write_text(json.dumps(
        {'purpose': '核验四条"只错位不变红"的排版防护（未填槽位、\\lvert 分隔符、表格列数、'
                    '紧跟字母的反斜杠串长度）确实在接收流量，并取证两条数字核对会见血',
         'cases_slot': len(CASES), 'cases_delimiter': len(extra),
         'cases_table': len(tbl_extra), 'cases_doccheck': len(docs_extra),
         'cases_backslash': len(bs_extra),
         'cases_total': n,
         'pass': n - len(bad), 'all_pass': not bad, 'failed': bad,
         'live_separators': read['separators'], 'live_hits': read['hits'],
         'planted_hits': read['planted_hits'], 'doc_check_notes': notes,
         'table_check_notes': tbl_notes, 'backslash_check_notes': bs_notes,
         # 第 6 条排版不变量的基线读数：文档里那句"翻倍 0 处 / 合法 N 处 / 豁免 M 处"以此为出处
         'bs_files': bs_read.get('files'), 'bs_single': bs_read.get('single'),
         'bs_double': bs_read.get('double'), 'bs_exempt': bs_read.get('exempt'),
         'bs_planted': bs_read.get('planted'),
         'bs_quoted_files': bs_read.get('quoted_files'),
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
                   '才算转义，两个反斜杠 = 没转义 = 行里多出不存在的列）',
                   '紧跟字母的反斜杠串长度必须是 1（check_bs_runs ⇒ raw 字面量里手写翻倍、'
                   'repr/str(容器) 把数据里合法的反斜杠翻倍，两条路落进文件后同形：MathJax 读成换行、'
                   '控制词降级成斜体字母，数值门禁两条都看不见；引用缺陷的行内代码可豁免，'
                   '但豁免必须带读数且粒度是一处行内代码）']},
        ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
