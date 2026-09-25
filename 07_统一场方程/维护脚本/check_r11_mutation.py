# -*- coding: utf-8 -*-
r"""R11、R12 与 R13 三层判据的**外部**变异核验：从引擎外面改那几条算术，看谁变红。

为什么要有这个脚本：R11 的判据（$N\mid 3Q$）此前只在引擎内部被自己的门禁对照过，
"把它写错会不会有人发现"只存在于某一次对话的口头里 —— 而一个没人能重跑的读数等于没人看守。
本脚本把 `验证脚本/so10_reps.py` 连同它的依赖 `so10_chain.py` 整份复制进临时目录，
在副本上植入缺陷，再重跑整台引擎（副本的产出只落在它自己的目录里，不碰仓库那份报告），
要求三件事同时成立：

  * 基线（未植入）全绿，且它打印的门禁总数与磁盘上 `SO10表示论报告.json` 里的 `tests`
    条数**相等** —— 这条不是装饰：引擎的层是短路接线的（`sel_ok = run_selection_layer() if res_ok`），
    依赖缺失时它会只跑前几层就退出，若只要求"退出码非 0"就会把这种夹具塌陷当成捕获；
  * 每个变异体都必须被**点名到它那一层**（R11.x、R12.x 或 R13.x，由每例自带的 `layer` 决定，
    不是"任何一个 FAIL"）抓住（崩溃不算捕获），且它打印的读数至少动一个
    —— 门禁 PASS 数、或报告 §10 那句"允许 X 条、禁戒 Y 条"、或报告 §11 的三个读数
    （$\Gamma$ 的阶、$|\Gamma|$ 三条出处那一列、§11.5 那两条独立判法的同判列）、
    或报告 §12 的六个读数（候选群阶、核 $K$ 与其阶分布、同构型种数、集合相等的通道比、
    唯一例外的承载者、物质字称实现者个数）。
    这一条不是形式：只动三条路径里浮点那条的滑倒**不动**判决表（甲/乙仍然同意），动的是"甲乙丙一致"那条断言 $\Rightarrow$
    同一个数为什么要三台互不共享算术的机器各跑一遍，这里有一次实测读数；R13 的 h1 是同一族：
    路丙的 triality 号只出现在断言里、不出现在 §12 的任何数字里 $\Rightarrow$ 它动的只有 PASS 数，
    这正好把"门禁在看守报告里看不见的断言"这件事本身变成了读数；
  * 一条良性改动（只补尾注释，语义不动）不得误报，否则这台仪器是"永远红"而不是"能红"。
    良性例现在三层各一条：只测 R11 那侧的良性改动，等于没核对 §11 与 §12 的读数在语义不动时**不**动。

R12 那四个变异体各自钉住报告 §11 的一个断言，且都落在**门禁**上而不是 `assert` 上 $\Rightarrow$
"报错"不会被当成"捕获"：色 $\mathbb Z_3$ 生成元换掉后两支不再互化（R12.1 的约定无关那条）、
阿贝尔群的元素阶多重集把单位元读成最大阶（R12.1 的"唯一命中"）、格的指数把不变因子**取和**
而不是取积（R12.2 的三条出处同数）、"在不在根格里"的第二条判法把坐标和的奇偶改成模 3
（R12.0 的两条独立判法同判）。

R13 那四个变异体同样落在门禁上，各自钉住 §12 的一个断言：路丙的标准 triality 号把 $3b$ 写成
$2b$ $\Rightarrow$ 丙与格读数不再成 $q_{\rm lat}\equiv 3q_{\rm std}$（R13.1，只动 PASS 数，见上）；
色类阶的枚举把类元读成对角粘合元（第 $ci$ 类的阶读成 $(ci,1,1)$ 的阶）$\Rightarrow$ §12.1 类表
"阶"列整体漂移、违背 `vords == [1,2,4,4]`（R13.0，动类表阶列）；注：这个位置第一轮植的是
"核的枚举少看在场谱的行"，两轮实测都是**中性变异**——少看 1 行、少看 10 行核都不动（核约束在
前 20 行已闭合），而真能把核放松的取法会先把通道循环的"陪集数 $\times|K|=$ 存活数"结构断言打断
$\Rightarrow$ 按本仪器"崩溃不算捕获"的规则，R13.2 的核枚举**无法从外面植红**，这条空白登记在
docstring 而不是台账；正向对照把"只弱 $\cap$ 只色"的两半**交集**写成**并集**
$\Rightarrow$ 半群读数退化、"全组允许 $=$ 两半交集"在多数通道不再成立（R13.6，动 §12.6 的通道比与
例外计数；第一轮这里植入的是"色半 and→or"，它把读数推到**零例外**，撞上引擎 claim 里那句
无守卫的 `exc[0]` ⇒ 引擎以 traceback 而非 FAIL 退出、被本仪器按规则判为未捕获——**这是一次
真伤，已由 `excpart` 三分支守卫修复**，仪器随后才改判得动）；
物质字称的实现者把相位判据取反（只数"逐场都 $\ne$ 目标相位"的元）$\Rightarrow$ 补集整批涌进来、
实现者个数偏离恰 2（R13.4，动 §12.4 的实现者数；注：第一版这里是"只按前 3 个场试"，实测前 3
个场就已把实现者钉成那 2 个 $\Rightarrow$ 中性变异，已换成取反版）。良性例 b3 给 `Kset = set(K)`
补尾注释，语义不动。

命名边界（如实登记）：文件名与台账名仍叫 `check_r11_mutation`，因为它从 R11 起家；它此刻覆盖
**三层**，这一件事由台账里的 `layers` 字段与每例的 `layer` 字段成文，不由文件名成文。

用法：python 维护脚本/check_r11_mutation.py    （约数分钟：一台引擎 = 一次完整自检）
产出：与维护脚本同目录的 check_r11_mutation.json（本脚本是唯一写入者）
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, '..', '验证脚本'))
TARGET = os.path.join(ENGINE, 'so10_reps.py')
DEPS = ('so10_chain.py', 'so10_reps.py')
OUT = os.path.join(HERE, 'check_r11_mutation.json')

TOTAL_RE = re.compile(r'（(\d+) 项，PASS (\d+)）')
FAIL_RE = re.compile(r'\[FAIL\]\s+(R\d+\.\d+[a-z]*)')
PAIR_RE = re.compile(r'允许 (\d+) 条、禁戒 (\d+) 条')
BLOCK = '低能算符的选择规则（R11）'
BLOCK2 = '完整残留离散规范群（R12）'
BLOCK3 = '422 链残留按 SU(4) 权格重做（R13）'
# 报告 §11 里那四个读数：每个都印自 GLOB，也就是印自被植入缺陷的那段算术的下游。
G_SIZE_RE = re.compile(r'活下来 (\d+) 个')          # |Gamma|（R12.1 的枚举）
G_FLAG_RE = re.compile(r'\*\*不成立\*\*|\*\*不同\*\*|定不出唯一的群')   # 同判/互化/定名失败
G_IDX_RE = re.compile(r'\| (\d+)（不变因子')         # R12.2 三条出处的甲那一列
G_ROOT_RE = re.compile(r'\| (是 / 是|是 / 否|否 / 是|否 / 否) \|')      # R12.0 两条独立判法
# 报告 §12 的六个读数：先切出 §12 那一节再匹配，避免与 §10/§11 的同类散文互相污染。
SEC12_A, SEC12_B = '## 12.', '## 13.'
H_SIZE_RE = re.compile(r'共 (\d+) 个元')             # 全候选群 = 类 x 弱 x 弱（R13.0 的枚举）
H_K_RE = re.compile(r'K=\\{(.+?)\\}')                # 在场谱的核（R13.2 的特征标枚举）
H_KORD_RE = re.compile(r'阶分布 \[([\d, ]+)\]')       # K 的阶分布（R13.2）
H_BY_RE = re.compile(r'商后共 (\d+) 种同构型')         # R13.3 的同构型种数
H_INT_RE = re.compile(r'在 (\d+)/(\d+) 条通道成立')    # R13.6 集合相等按通道计
H_EXC_RE = re.compile(r'唯一例外是 (.+?) 那条')        # R13.6 唯一例外的承载者
H_MP_RE = re.compile(r'实现者恰 (\d+) 个')             # R13.4 物质字称实现者个数
H_TORD_RE = re.compile(r'\| \$(.+?)\$ \| \$(.+?)\$ \| (\d+) \|')  # §12.1 类表的"阶"列（R13.0）

# 锚点：每条都必须在源文件里**恰好出现一次**，否则整轮判 INVALID（锚点漂了不等于没植入）。
A_JIA = (b'    return int(t3) % n == 0', b'    return int(t3 / 3) % n == 0')
A_BING = (b'        ang = 2.0 * math.pi * float(a) * float(q)',
          b'        ang = math.pi * float(a) * float(q)')
A_T3Q = (b'    return sum(3 * f_bl(f) for f in fl)', b'    return 3 * f_bl(fl[0])')
A_HIT = (b"    hit4 = [x for x in c4 if x['singlet'] > 0]",
         b"    hit4 = [x for x in c4 if x['zero'] > 0]")
A_OK = (b'    return None if t3.denominator != 1 else int(t3) % 3',
        b'    return None if t3.denominator != 1 else int(t3) % 3  # inert: benign case')
# R12 侧：四个各钉住 §11 的一个断言，且都落在门禁条件上（不在 assert 上）=> 崩溃不会冒充捕获。
G_TRI = (b"    tri = (p + 2 * q) if conv == 'A' else (2 * p + q)",
         b"    tri = (p + q) if conv == 'A' else (2 * p + q)")
G_OO = (b'            oo = 1 if k == 0 else d // math.gcd(k, d)',
        b'            oo = d if k == 0 else d // math.gcd(k, d)')
G_IDX = (b'        idx *= x', b'        idx += x')
G_ZB = (b'and (sum(v).numerator % 2 == 0)', b'and (sum(v).numerator % 3 == 0)')
G_OK = (b'            (x[3] + y[3]) % CEN_U_PER)',
        b'            (x[3] + y[3]) % CEN_U_PER)  # inert: benign case')
# R13 侧：四个各钉住 §12 的一个断言，同样落在门禁条件上。
H_QSTD = (b'    return (int(lab[2]) + 2 * int(lab[0]) + 3 * int(lab[1])) % 4',
          b'    return (int(lab[2]) + 2 * int(lab[0]) + 2 * int(lab[1])) % 4')
H_K = (b'    vord_pairs = [corder((ci, 0, 0)) for ci in range(len(V))]',
       b'    vord_pairs = [corder((ci, 1, 1)) for ci in range(len(V))]')
H_CLO = (b'        wcapc = wko & clo', b'        wcapc = wko | clo')
H_MP = (b"          if all(FV[k]['sig'][i] == FV[k]['mpp'] for k in sorted(FV))]",
        b"          if all(FV[k]['sig'][i] != FV[k]['mpp'] for k in sorted(FV))]")
H_OK = (b'    Kset = set(K)', b'    Kset = set(K)  # inert: benign case')

CASES = [
    ('ctl', '基线：不植入', 'baseline', None, 'both'),
    ('m1', '甲：同余式右移一位，把 N|3Q 写成 N|Q（只动三条路径里的整除那条）', 'mutant', A_JIA, 'R11'),
    ('m2', '丙：浮点那条把 2pi 周期写成 pi 半周期（只动三条路径里的浮点那条）', 'mutant', A_BING, 'R11'),
    ('m3', '荷账丢掉求和号：sum_k 3(B-L)_k 写成只取第一条场', 'mutant', A_T3Q, 'R11'),
    ('m4', '枚举改用 R11.1 那个错 projector 的零权当筛选条件', 'mutant', A_HIT, 'R11'),
    ('b1', '良性：给 f_tri 补一条尾部注释（语义不动）', 'benign', A_OK, 'both'),
    ('g1', 'R12：换掉色 Z_3 生成元的甲侧 triality（p+2q 写成 p+q）⇒ 两支不再互化',
     'mutant', G_TRI, 'R12'),
    ('g2', 'R12：阿贝尔群的元素阶多重集把单位元读成最大阶（定名那一步失去唯一命中）',
     'mutant', G_OO, 'R12'),
    ('g3', 'R12：格指数把不变因子取和而不是取积（三条出处不再同数）',
     'mutant', G_IDX, 'R12'),
    ('g4', 'R12："在不在根格里"的第二条判法把坐标和的奇偶改成模 3（两条判法不再同判）',
     'mutant', G_ZB, 'R12'),
    ('b2', '良性：给 cen_law 的 U(1) 分量补一条尾部注释（语义不动）', 'benign', G_OK, 'both'),
    ('h1', 'R13：路丙的标准 triality 号把 3b 写成 2b（丙与格读数不再成 q_lat = 3 q_std）',
     'mutant', H_QSTD, 'R13'),
    ('h2', 'R13：色类阶的枚举把类元读成对角粘合元（(ci,0,0) 写成 (ci,1,1) ⇒ 类表"阶"列漂移）',
     'mutant', H_K, 'R13'),
    ('h3', 'R13：正向对照把两半"交集"写成"并集"（半群读数退化 ⇒ 集合相等不再成立）',
     'mutant', H_CLO, 'R13'),
    ('h4', 'R13：物质字称的实现者把相位判据取反（只数逐场都 ≠ 目标相位的元 ⇒ 个数偏离恰 2）',
     'mutant', H_MP, 'R13'),
    ('b3', '良性：给 Kset 那行补一条尾部注释（语义不动）', 'benign', H_OK, 'both'),
]


def read_source():
    with open(TARGET, 'rb') as fh:
        return fh.read()


def engine_json_tests():
    """磁盘上那份报告 JSON 的 tests 条数：基线打印的门禁数必须与它相等，否则夹具塌陷。"""
    p = os.path.join(ENGINE, 'SO10表示论报告.json')
    if not os.path.exists(p):
        return None
    with io.open(p, encoding='utf-8') as fh:
        return len(json.load(fh).get('tests') or [])


def build(tag, patch):
    """临时目录 = 整台引擎的一份可跑副本；patch 为 None 时是基线。"""
    d = os.path.join(tempfile.mkdtemp(prefix='am_r11_%s_' % tag), 'engine')
    os.makedirs(d)
    hits = 0
    for f in DEPS:
        src = os.path.join(ENGINE, f)
        with open(src, 'rb') as fh:
            b = fh.read()
        if f == 'so10_reps.py' and patch:
            hits = b.count(patch[0])
            b = b.replace(patch[0], patch[1])
        with open(os.path.join(d, f), 'wb') as fh:
            fh.write(b)
    return d, hits


def run(d):
    r = subprocess.run([sys.executable, os.path.join(d, 'so10_reps.py')], cwd=d,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = r.stdout.decode('utf-8', 'replace')
    rep = ''
    rp = os.path.join(d, 'SO10表示论报告.md')
    if os.path.exists(rp):
        with io.open(rp, encoding='utf-8') as fh:
            rep = fh.read()
    a, bnd = rep.find(SEC12_A), rep.find(SEC12_B)
    sec12 = rep[a:bnd] if (a >= 0 and bnd > a) else ''
    m = TOTAL_RE.search(out)
    fails = FAIL_RE.findall(out)
    return {'exit': r.returncode,
            'gates': int(m.group(1)) if m else None,
            'pass': int(m.group(2)) if m else None,
            'fail_ids': fails,
            'r11_fail_ids': [x for x in fails if x.startswith('R11')],
            'layer_fail_ids': dict((k, [x for x in fails if x.startswith(k)])
                                   for k in ('R11', 'R12', 'R13')),
            'printed_r11_block': BLOCK in out,
            'printed_r12_block': BLOCK2 in out,
            'printed_r13_block': BLOCK3 in out,
            'report_pairs': sorted(set(tuple(int(x) for x in t) for t in PAIR_RE.findall(rep))),
            'report_global': {
                'g_size': sorted(set(int(x) for x in G_SIZE_RE.findall(rep))),
                'g_flag': len(G_FLAG_RE.findall(rep)),
                'g_idx': sorted(set(int(x) for x in G_IDX_RE.findall(rep))),
                'g_root': sorted(set(G_ROOT_RE.findall(rep)))},
            'report_r13': {
                'h_size': sorted(set(H_SIZE_RE.findall(sec12))),
                'h_k': sorted(set(H_K_RE.findall(sec12))),
                'h_kord': sorted(set(H_KORD_RE.findall(sec12))),
                'h_by': sorted(set(H_BY_RE.findall(sec12))),
                'h_int': sorted(set(tuple(x) for x in H_INT_RE.findall(sec12))),
                'h_exc': sorted(set(H_EXC_RE.findall(sec12))),
                'h_mp': sorted(set(H_MP_RE.findall(sec12))),
                'h_tord': sorted(set(m[2] for m in H_TORD_RE.findall(sec12)))},
            'traceback': 'Traceback' in out}


def judge(case, res, base):
    _tag, _name, kind, _patch, layer = case
    clean = (res['exit'] == 0 and res['pass'] == res['gates'] and not res['fail_ids']
             and not res['traceback']
             and res['printed_r11_block'] and res['printed_r12_block']
             and res['printed_r13_block']
             and bool(res['report_pairs']) and bool(res['report_global']['g_size'])
             and bool(res['report_r13']['h_size']) and bool(res['report_r13']['h_k']))
    if kind in ('baseline', 'benign'):
        return clean and (kind == 'baseline'
                          or (res['report_pairs'] == base['report_pairs']
                              and res['report_global'] == base['report_global']
                              and res['report_r13'] == base['report_r13']
                              and res['pass'] == base['pass']))
    moved = [k for k, v in (('report_pairs', res['report_pairs'] != base['report_pairs']),
                            ('report_global', res['report_global'] != base['report_global']),
                            ('report_r13', res['report_r13'] != base['report_r13']),
                            ('gates_pass', res['pass'] != base['pass'])) if v]
    res['moved'] = moved
    return (res['exit'] != 0 and bool(res['layer_fail_ids'].get(layer))
            and not res['traceback'] and bool(moved))


def main():
    src = read_source()
    anchors = {}
    for _, _, _, patch, _layer in CASES:
        if patch:
            anchors[patch[0].decode()] = src.count(patch[0])
    tests_on_disk = engine_json_tests()

    res = {}
    for tag, name, kind, patch, layer in CASES:
        d, hits = build(tag, patch)
        try:
            r = run(d)
        finally:
            shutil.rmtree(os.path.dirname(d), ignore_errors=True)
        r.update({'id': tag, 'claim': name, 'kind': kind, 'layer': layer,
                  'anchor_hits': hits if patch else 0})
        r['expect_caught'] = kind == 'mutant'
        res[tag] = r
        print('[case] %s %-14s layer=%-5s exit=%s gates=%s/%s fail=%s pairs=%s glob=%s h12=%s' %
              (tag, kind, layer, r['exit'], r['pass'], r['gates'],
               r['layer_fail_ids'].get(layer) or r['fail_ids'], r['report_pairs'],
               r['report_global']['g_size'], r['report_r13']['h_k'] and
               (r['report_r13']['h_size'], r['report_r13']['h_int'], r['report_r13']['h_mp'])))

    anchor_bad = [k for k, v in anchors.items() if v != 1]
    fixture_bad = (res['ctl']['gates'] is None or (tests_on_disk is not None
                   and res['ctl']['gates'] != tests_on_disk))
    for tag, r in res.items():
        r['ok'] = (not anchor_bad and not fixture_bad) and judge(
            next(c for c in CASES if c[0] == tag), r, res['ctl'])
        if r['expect_caught']:
            print('[moved] %s %s' % (tag, r.get('moved')))
    missed = [t for t, r in res.items() if r['expect_caught'] and not r['ok']]
    false_alarm = [t for t, r in res.items() if not r['expect_caught'] and not r['ok']]
    payload_layers = sorted(set(c[4] for c in CASES if c[4] != 'both'))
    # 覆盖面自己也要判：某一层的变异体被整批删掉时，例数的账照样自洽（baseline 1 + 变异体 + 良性），
    # 但这台仪器已经悄悄退回单层 ⇒ "三层都看守"这句话就没有仪器背书了。
    uncovered = [k for k in payload_layers
                 if not any(c[2] == 'mutant' and c[4] == k for c in CASES)]
    verdict = 'CAUGHT' if not missed and not false_alarm and not anchor_bad \
        and not fixture_bad and not uncovered else 'INVALID'
    payload = {'script': 'check_r11_mutation.py', 'target': '验证脚本/so10_reps.py',
               'layers': sorted(set(c[4] for c in CASES if c[4] != 'both')),
               'target_bytes': len(src), 'engine_json_tests': tests_on_disk,
               'anchor_counts': anchors, 'fixture_ok': not fixture_bad,
               'cases_total': len(CASES), 'mutants': sum(1 for c in CASES if c[2] == 'mutant'),
               'benign': sum(1 for c in CASES if c[2] == 'benign'),
               'caught': sum(1 for t, r in res.items() if r['expect_caught'] and r['ok']),
               'missed': missed, 'false_alarm': false_alarm,
               'uncovered_layers': uncovered,
               'baseline_pairs': res['ctl']['report_pairs'],
               'baseline_global': res['ctl']['report_global'],
               'baseline_r13': res['ctl']['report_r13'],
               'layer_mutants': dict((k, sum(1 for c in CASES if c[2] == 'mutant' and c[4] == k))
                                     for k in payload_layers),
               'verdict': verdict,
               'cases': [res[t] for t, _, _, _, _ in CASES]}
    with io.open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    print('结论：%s ｜ %d 例（变异体 %d、良性 %d）｜ 基线报告读数 %s ｜ 台账 %s' %
          (verdict, len(CASES), payload['mutants'], payload['benign'],
           res['ctl']['report_pairs'], os.path.basename(OUT)))
    print('自检：%s（%d 例，PASS %d）' %
          ('全部通过' if verdict == 'CAUGHT' else '存在未捕获或误报', len(CASES),
           sum(1 for r in res.values() if r['ok'])))
    return 0 if verdict == 'CAUGHT' else 1


if __name__ == '__main__':
    sys.exit(main())
