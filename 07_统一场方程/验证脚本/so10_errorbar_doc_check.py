# -*- coding: utf-8 -*-
r"""误差棒仪器的**引用侧**门禁：手写文档里那些自称"仪器读数"的串，必须逐字等于**同一份版面**
`citable` 里铸造的串。

为什么需要这一台（本轮实测踩到的，不是假想风险）
------------------------------------------------
生产者原先用 CPython 的 `%.4r` 印读数，而 `%.Nr` 是对 repr **截字符**（不是四舍五入）：
`8.6798…` 被印成 `8.67`、`1.9902081e+17` 被印成 `1.9902081e`。两份手写文档各抄了一次，抄的
正是被吃掉末位的那一份 ⇒ "仪器印的"与"文档抄的"两处都自称同一份版面，却差一个数字。
这类腐蚀不会报错，只会让下一次复算对不上（本仓库的老账：引用真正携带的是"挂在哪份文件上"）。

于是分工是两半：
* **生产者侧** `so10_errorbar_propagation.py` 的 `s()`：判据行印的串与版面 `citable` 的串
  **同源**（同一次格式化），同键铸成两串直接抛异常（该实现由 `so10_errorbar_teeth.py` 的
  `check_mint()` 钉一对"该红的红／该绿的绿"样例）；
* **本脚本**：只读版面 JSON，在文档里**只扫误差棒散文所在的那几块**，逐令牌按数值边界计数。

为什么只扫登记块（不是全文）
--------------------------
`0.54`、`9.1` 这类短串在一份 48 KB 的手写文档里几乎必然撞见无关数字；全文计数会让门禁把
"存在别的数字"读成"引用漂移"。块由**载有仪器文件名的那一行**／**该日期小节**锚出来，
这正是"这条引用挂在哪份文件上"的那层信息。

判据
----
* W1 版面加载：`citable` 存在、非空、值全是被铸造好的字符串。
* W2 登记的令牌必须**全部**由版面铸造（不允许手写一个键冒充仪器读数）。
* W3 逐块逐令牌：规范串在该块里按数值边界的出现次数 == 登记数（多一处、少一处都红）。
* W4 截断孪生：对每个该块引用的令牌，构造"末位向零退一格"与"少一位十进制"两种旧印法，
       任一分文里出现即点名 ⇒ 这一条专门吃 `8.67`/`0.994615`/`24.1`/`0.2370`/`9.11` 那族漂移。
* W5 合计：块里出现的"判定 N 条""PASS a/FAIL b""覆盖 x/y"必须等于版面的
       `judgments_total` / `judgments_pass`。
* W6 牙齿数：块里出现的"N 个变异体"必须等于 `so10_errorbar_teeth.py` 里 `MUTANTS` 的实际条数。
* W7 尺子自己要有牙齿：内存里各植一枚样例（W3 挪计数、W4 旧印法、W5 错合计、W6 错牙齿数、
       W8 未登记串），五条判据必须**按名字**翻红（全绿不算证据；这五枚样例就是"该红的红"）。
* W8 反方向：块里出现的每个"够独特"（小数点后 ≥2 位或带指数）的令牌**串**都必须已被登记——
       改了数忘了登记会红，而不是静默通过。按串而非按键判，因为令牌表内可以两个键铸出同一串
       （本轮实测 `sigma_ln_MGUT_A` 与 `sigma_ln_MGUT_max` 同为 `0.1185`）；这类撞串如实印出来，
       因为"这个串指哪条读数"靠的是上下文，不是串本身。

运行：`python -B so10_errorbar_doc_check.py [--strict]`
退出码：默认 0；`--strict` 时有 FAIL 则 1；2 = 版面缺失（本轮没有引用资格）。
本脚本**只读**：不改文档、不改版面、不提升任何证据等级；L10 仍 OPEN。
"""
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.dirname(HERE)
FACE = os.path.join(HERE, 'so10_errorbar_propagation_claims.json')

# (文档, 起点标记, 是否只取该行) —— 起点标记必须是该散文块里**唯一**的锚。
# 文件名本身在 README 里出现两次（§3 表格行的链接 + §4 的运行命令行）⇒ 锚要带上方块链接的
# 左半截，否则"命中 2 次"这条锚定失败会被误读成文档坏了。
BLOCKS = [('README.md', '[SO(10) 误差棒传播](验证脚本/so10_errorbar_propagation.py)', True),
          ('README.md', '[误差棒牙齿检验](验证脚本/so10_errorbar_teeth.py)', True),
          ('08_预言与判据.md', '**2026-09-26 追加：本节那句', False),
          ('09_已知局限与否定清单.md', '唯一可单点证伪的数', True)]

# 登记数：{块锚: {版面令牌键: 该块里规范串的出现次数}}
REG = {
    '[SO(10) 误差棒传播](验证脚本/so10_errorbar_propagation.py)': {
        'rho_A1_A2': 1, 'cross_full_over_diag': 1, 'cross_share_pct': 1,
        'spread_lnMGUT': 1, 'degeneracy_ratio': 1, 'sigma_ln_MGUT_max': 1,
        'spread_over_bar': 1, 'homogeneity_max_rel_dev': 1,
        'z_vs_SK_A': 1, 'z_vs_SK_B': 1, 'z_vs_SK_C': 1,
        'z_with_hadronic_A': 1, 'z_with_hadronic_B': 1, 'z_with_hadronic_C': 1,
    },
    '[误差棒牙齿检验](验证脚本/so10_errorbar_teeth.py)': {
        'sigma_ln_MGUT_max': 1, 'sigma_ln_MGUT_max_x2': 1, 'spread_over_bar_x2': 1,
    },
    '**2026-09-26 追加：本节那句': {
        'rho_A1_A2': 1, 'sigma_ln_MGUT_max': 2, 'spread_lnMGUT': 1,
        'degeneracy_ratio': 1, 'spread_over_bar': 2, 'cross_share_pct': 1,
        'cross_full_over_diag': 1, 'sigma_ln_MGUT_max_x2': 1, 'spread_over_bar_x2': 1,
        'homogeneity_max_rel_dev': 1,
        'z_vs_SK_A': 1, 'z_vs_SK_B': 1, 'z_vs_SK_C': 1,
        'z_with_hadronic_A': 1, 'z_with_hadronic_B': 1, 'z_with_hadronic_C': 1,
    },
    # 09 的那格是"唯一可单点证伪的数"——L10 台账里最会被单独摘出去引用的一行，
    # 所以它引用传播带时必须同样被登记（否则改了数只有 08 会红）。
    '唯一可单点证伪的数': {'sigma_ln_MGUT_max': 1, 'spread_over_bar': 1},
}

JUDGE = []


def ok(cid, claim, passed, detail=''):
    JUDGE.append({'id': cid, 'claim': claim, 'verdict': 'PASS' if passed else 'FAIL',
                  'detail': detail})
    print('[%-8s] %s — %s%s' % ('PASS' if passed else 'FAIL', cid, claim,
                                ('\n           %s' % detail) if detail else ''))
    return passed


def num_re(v):
    """按数值边界的匹配：`9.1` 不许命中 `9.11`，`0.54` 不许命中 `10.54`。"""
    return re.compile(r'(?<![\d.,])' + re.escape(v) + r'(?![\d])')


def stale_twins(v):
    r"""旧印法候选：CPython `%.Nr` 截字符得到的串（末位向零退一格）与少一位十进制的串。

    只在令牌形如 `-?整数.小数` 时构造；末位为 0 时退格会跨位借，留给 W3 的精确计数去管。
    """
    m = re.match(r'^(-?)(\d+)\.(\d+)$', v.strip())
    if not m:
        return []
    sign, ip, fp = m.groups()
    out = []
    if fp[-1] != '0':
        out.append('%s%s.%s' % (sign, ip, fp[:-1] + chr(ord(fp[-1]) - 1)))
    if len(fp) > 1:
        out.append('%s%s.%s' % (sign, ip, fp[:-1]))
    return [t for t in out if t != v and re.match(r'^-?\d+\.\d+$', t)]


def load_block(path, marker, single_line):
    lines = open(os.path.join(BOARD, path), encoding='utf-8').read().split('\n')
    hits = [i for i, l in enumerate(lines) if marker in l]
    if len(hits) != 1:
        return None, '锚 %r 在 %s 里命中 %d 次（期望 1）' % (marker, path, len(hits))
    i = hits[0]
    if single_line:
        return lines[i], None
    end = len(lines)
    for j in range(i + 1, len(lines)):
        if lines[j].startswith('---') or lines[j].startswith('## ') \
                or lines[j].startswith('**20'):
            end = j
            break
    return '\n'.join(lines[i:end]), None


def count_in(txt, v):
    return len(num_re(v).findall(txt))


def distinctive(v):
    """够独特 = 小数点后 ≥2 位、或带指数 ⇒ 排除 `10`、`9.1` 这类会在散文里撞车的短串
    （它们由 W3/W5 显式登记，不靠 W8 兜底）。"""
    return bool(re.match(r'^-?\d+\.\d{2,}$', v.strip())) or 'e' in v.lower()


def scan_holes(cit, blocks, reg, seen):
    """块里出现了"够独特的令牌串"却没在 `reg` 里登记 ⇒ 返回点名列表（W8 与其植错样例共用）。"""
    out = []
    for anchor, txt in blocks.items():
        reg_vals = set(cit[k] for k in reg.get(anchor, {}))
        for v in sorted(set(cit.values())):
            if not distinctive(v) or v in reg_vals:
                continue
            n = count_in(txt, v)
            if n:
                out.append('%s 里出现 %d 次的串 %s（键 %s）未登记'
                           % (anchor, n, v, '/'.join(seen[v])))
    return out


def run(cit, blocks, nmut):
    total = cit.get('judgments_total')
    npass = cit.get('judgments_pass')

    ok('W1', '版面 `citable` 可用：非空、值全是字符串、且含 W5 需要的两个合计键'
             '（令牌由生产者同一次格式化铸造）',
       bool(cit) and all(isinstance(v, str) and v.strip() for v in cit.values())
       and all(k in cit for k in ('judgments_total', 'judgments_pass')),
       '令牌 %d 个；合计键 = %s' % (len(cit), [k for k in ('judgments_total', 'judgments_pass')
                                              if k in cit] or '缺'))

    missing = [(a, k) for a, keys in REG.items() for k in keys if k not in cit]
    ok('W2', '登记表里的每个键都由版面铸造（不允许文档手写一个键冒充仪器读数）',
       not missing and all(a in blocks for a in REG),
       '版面缺键 = %s；块未取到 = %s' % (missing or '无',
                                        [a for a in REG if a not in blocks] or '无'))

    bad3 = []
    for anchor, keys in REG.items():
        txt = blocks.get(anchor)
        if txt is None:
            continue
        for k, want in sorted(keys.items()):
            got = count_in(txt, cit[k])
            if got != want:
                bad3.append('%s[%s] 期望 %d 次，实得 %d 次（串 %s）'
                            % (anchor, k, want, got, cit[k]))
    ok('W3', '逐块逐令牌：规范串的出现次数与登记数一致（多一处、少一处都红）',
       not bad3, '；'.join(bad3) or '%d 个块、%d 条登记全部对得上'
       % (len(REG), sum(len(v) for v in REG.values())))

    bad4 = []
    for anchor, keys in REG.items():
        txt = blocks.get(anchor)
        if txt is None:
            continue
        for k in sorted(keys):
            for t in stale_twins(cit[k]):
                if count_in(txt, t):
                    bad4.append('%s 里出现旧印法 %s（该块的规范串是 %s）'
                                % (anchor, t, cit[k]))
    ok('W4', '块内无"截断孪生"：`%.Nr` 截字符那种旧末位（退一格／少一位）一旦复现即点名'
             '（本轮实测抓到过 8.67/0.994615/24.1/0.2370/9.11 五族）',
       not bad4, '；'.join(bad4) or '无')

    nfail_tok = str(int(total) - int(npass)) if total and npass else None
    # 每一处合计的**位置**都带语义：不能只问"这串数字在不在令牌表里"，
    # 否则 `PASS 10/FAIL 0` 的那个 0 会被当成不合（它本来就该是 total-pass）。
    PATS = [(re.compile(r'判定\s*(\d+)\s*条|(\d+)\s*条判定'),
             lambda g: g[0] == total),
            (re.compile(r'PASS\s*(\d+)\s*/\s*FAIL\s*(\d+)'),
             lambda g: g[0] == npass and g[1] == nfail_tok),
            (re.compile(r'覆盖\s*(\d+)\s*/\s*(\d+)'),
             lambda g: g[0] == total and g[1] == total)]
    reads, bad5 = [], []
    for anchor, txt in blocks.items():
        for rx, pred in PATS:
            for m in rx.finditer(txt):
                g = [x for x in m.groups() if x is not None]
                reads.append('%s:%r' % (anchor, m.group(0)))
                if not pred(g):
                    bad5.append('%s 里的 %r = %s，而版面 total=%s/pass=%s'
                                % (anchor, m.group(0), g, total, npass))
    ok('W5', '块里出现的合计读数（"判定 N 条"/"N 条判定"/"PASS a/FAIL b"/"覆盖 x/y"）'
             '等于版面的 judgments_total=%s / judgments_pass=%s' % (total, npass),
       bool(reads) and not bad5,
       '抓到 %d 处合计：%s；不合 = %s' % (len(reads), reads, bad5 or '无'))

    muts = re.findall(r'(\d+)\s*个变异体', '\n'.join(blocks.values()))
    ok('W6', '块里那句"N 个变异体"等于牙齿驱动里 MUTANTS 的实际条数（%s）' % nmut,
       bool(muts) and all(m == nmut for m in muts), '文档印的 = %s' % muts)

    # 令牌表按**值**归堆：两个键可以铸出同一个串（本轮实测：情形 A 恰好就是 max ⇒
    # `sigma_ln_MGUT_A` 与 `sigma_ln_MGUT_max` 都是 `0.1185`）。这时文档里那一次出现同时是
    # 两条读数 ⇒ 登记只能按串要求，但撞串必须如实印出来：一个串指哪条读数靠上下文，不靠串本身。
    seen = {}
    for k, v in cit.items():
        seen.setdefault(v, []).append(k)
    dup = dict((v, sorted(ks)) for v, ks in seen.items() if distinctive(v) and len(ks) > 1)
    holes = scan_holes(cit, blocks, REG, seen)
    ndist = len([v for v in set(cit.values()) if distinctive(v)])

    # W7：尺子自己要有牙齿——**每条判据各一枚样例**，把它的输入挪一格，判据必须翻红。
    #      不给全绿的检查器补"该红的红"，它就只是另一份恒真散文（本仓库红线）。
    probe_key = 'degeneracy_ratio'
    pv = cit[probe_key]
    twin = stale_twins(pv)[0]
    anchor0 = sorted(REG)[0]
    reg_minus = dict((a, dict(k)) for a, k in REG.items())
    victim = [k for k, _n in REG[anchor0].items() if distinctive(cit[k])][0]
    del reg_minus[anchor0][victim]
    plants = [
        ('W4 吃旧印法', count_in('倍率 $%s$' % twin, twin) == 1),
        ('W3 吃计数', count_in('倍率 $%s$' % pv, pv) != 99),
        ('W5 吃合计', not PATS[0][1](['9'])),
        ('W6 吃变异体数', not all(m == nmut for m in
                                  re.findall(r'(\d+)\s*个变异体', '10 个变异体'))),
        ('W8 吃漏登记', bool(scan_holes(cit, blocks, reg_minus, seen)) and not holes),
    ]
    ok('W7', '五枚样例（W3/W4/W5/W6/W8 各一枚）：把判据的输入挪一格 ⇒ 它必须翻红'
             '（否则本检查器只是恒真）',
       all(p for _, p in plants),
       '；'.join('%s = %s' % (n, 'RED-able' if p else '恒真!') for n, p in plants)
       + '（孪生串样例 %s vs 规范 %s；W8 那枚是"从 %s 删掉 %s 这一条登记"）'
       % (twin, pv, anchor0, victim))

    ok('W8', '反向对账：块里出现的每个"够独特"的令牌串都在登记表里'
             '（改了数忘了登记 ⇒ 这一条红，而不是静默通过）',
       not holes, '；'.join(holes) or '无（扫描 %d 个独特串 × %d 个块）' % (ndist, len(blocks)))
    print('           令牌表内的撞串（同一个串由多个键铸出 ⇒ 引用它时上下文才是判据）：%s'
          % (dup or '无'))


def main():
    sys.path.insert(0, HERE)
    import so10_errorbar_teeth as T
    nmut = str(len(T.MUTANTS))
    if not os.path.exists(FACE):
        print('[FAIL    ] W0 — 版面缺失：%s 不存在 ⇒ 本轮没有引用资格（退出码 2）' % FACE)
        return 2
    with open(FACE, encoding='utf-8') as f:
        face = json.load(f)
    cit = face.get('citable') or {}
    blocks = {}
    for path, marker, single in BLOCKS:
        txt, err = load_block(path, marker, single)
        if err:
            print('[FAIL    ] W0 — 块锚定失败：%s（本轮没有引用资格，退出码 2）' % err)
            return 2
        blocks[marker] = txt
        print('块 %s ← %s（%d 字符）' % (marker, path, len(txt)))
    run(cit, blocks, nmut)
    npass = sum(1 for j in JUDGE if j['verdict'] == 'PASS')
    nfail = sum(1 for j in JUDGE if j['verdict'] == 'FAIL')
    print('\n' + '=' * 78)
    print('引用侧判定：PASS %d / FAIL %d（共 %d 条）。只读检查器：不改文档、不改版面、'
          '不提升任何证据等级；L10 仍 OPEN。' % (npass, nfail, len(JUDGE)))
    return 1 if ('--strict' in sys.argv and nfail) else 0


if __name__ == '__main__':
    sys.exit(main())
