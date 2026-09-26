# -*- coding: utf-8 -*-
"""R19 可行性探针（仓库内、可重跑）：$\sigma$ 道"不增秩"这条读数，是否只在第十九项钉住的那六个偶档
（$\nu+\dot\nu\le 8$）上成立？

第十九项（$\S$14.10）的边界 (ii) 写着"更宽档（$\nu+\dot\nu>8$）没有核过"。这条边界此前只有草稿盘上
一次运行当证据，因而**不进文档**。本脚本把那台仪器搬进仓库，让它成为一份有打印机的读数：

* 逐档起子进程，每档一个硬时间盒 $\Rightarrow$ 慢档被登记为 TIMEOUT（成本本身就是读数的一部分），
  而不是把整轮挂住；
* 退出码分三档，**部分完成不许被当成通过**：0 = 全部收敛且下面四条判据全 PASS；
  1 = 有判据为假（读数错）；2 = 有档超时/未跑完（此时任何文档都不许引用本脚本的合计）。

四条判据：
G1 $\varepsilon$ 目录自检：每档 $\varepsilon$ 道秩 $=$ `cg_j0(nu)*cg_j0(nd)`（这台机器没接错线的证据）；
G2 主判据：每档"并秩 $-$ $\varepsilon$ 秩 $=0$"，即 $\sigma$ 道在该档不新增秩；
G3 正对照非退化：**截断** $\varepsilon$ 基线（只留"槽 0-1 已配对"那一族画线）下"新增"必须 $>0$，
   否则 G2 的那个 0 与"恒零计数器"不可区分。$\nu=2$ 的档例外，且例外有结构理由：$\nu=2$ 时唯一的
   $\varepsilon$ 配对就是把 $(0,1)$ 配掉，故截断集 $=$ 全集、对照必然退化 —— 该档改为要求
   截断秩 $=$ 完整秩（即"退化"这一说法本身被核过，不是被默许）。
G4 手性对称：$(\nu,\dot\nu)$ 与 $(\dot\nu,\nu)$ 的**物理读数**逐字段相等（跨手性不变量，与 $\S$14.10
   里 $\sigma$ 线两侧同用同一 $c_{j0}$ 递推的口径独立）。G3 那组截断字段不在比之内 —— 截断锚在
   不点侧的槽 $(0,1)$，它本身不是手性标量；被比的与被免的字段在代码里写成两张名单，且两名单并上
   `nu`/`nd` 必须覆盖读数表全部键（新增字段会在这里响，不会静默落到某侧）。

约定与第十九项一致：$\sigma^\mu=(I,\sigma^1,i\sigma^2\big|_{\text{实}},\sigma^3)$，带 $i$ 那条用实矩阵
$i\sigma^2=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$，度规符号并成 $G=(+1,-1,+1,-1)$；$\sigma$ 线的 $\mu$
并成传播子 $P_{ij,pq}=\sum_\mu G_\mu\sigma^\mu_{ip}\sigma^\mu_{jq}$，每分量只乘一次；全程精确分数，
无浮点、无模约化。本脚本不改引擎、不加门禁，因此不动表示论报告的 144 项合计，也不改变异台账的
`target_bytes`。

用法：`python r19_wide_tier_probe.py [--box 600] [--tiers 8x2,2x8,...] [--only-wide]`
"""
import itertools
import json
import os
import subprocess
import sys
import time
from fractions import Fraction as Q

# 第十九项钉住的那六个偶档（$\nu+\dot\nu\le 8$），用来确认"搬进仓库"没有改变读数
PINNED = ((2, 2), (4, 2), (2, 4), (4, 4), (6, 2), (2, 6))
# 边界 (ii) 说没核过的那四档；便宜的排前面（$\sigma$ 线条数 = 槽位数 $\times$ 每档枚举量）
WIDE = ((8, 2), (2, 8), (6, 4), (4, 6))

I2 = ((Q(1), Q(0)), (Q(0), Q(1)))
S1 = ((Q(0), Q(1)), (Q(1), Q(0)))
S2R = ((Q(0), Q(-1)), (Q(1), Q(0)))
S3 = ((Q(1), Q(0)), (Q(0), Q(-1)))
SIG = (I2, S1, S2R, S3)
G = (Q(1), Q(-1), Q(1), Q(-1))
EZ = {(Q(0), Q(1)): Q(1), (Q(1), Q(0)): Q(-1)}


def matchings(rest):
    if not rest:
        yield []
        return
    i = rest[0]
    for p in range(1, len(rest)):
        for tail in matchings(rest[1:p] + rest[p + 1:]):
            yield [(i, rest[p])] + tail


def q_rank(vecs):
    piv = {}
    for v in vecs:
        row = dict((j, c) for j, c in enumerate(v) if c)
        while row:
            j = min(row)
            if j not in piv:
                piv[j] = row
                break
            base = piv[j]
            f = row[j] / base[j]
            for jj, cc in base.items():
                row[jj] = row.get(jj, Q(0)) - f * cc
            row = dict((jj, cc) for jj, cc in row.items() if cc)
    return len(piv)


def cg_j0(n):
    book = {0: 1}
    for _ in range(n):
        nb = {}
        for jj, k in book.items():
            for j2 in (jj - 1, jj + 1):
                if j2 >= 0:
                    nb[j2] = nb.get(j2, 0) + k
        book = nb
    return book.get(0, 0)


def prop(i, j, p, q):
    return sum(G[m] * SIG[m][i][p] * SIG[m][j][q] for m in range(4))


PROP = {}
for _i in range(2):
    for _j in range(2):
        for _p in range(2):
            for _q in range(2):
                PROP[(_i, _j, _p, _q)] = prop(_i, _j, _p, _q)


def structure_value(n, eps_lines, sig_lines, mpair):
    """对槽位指标串 $t$ 求值。"""
    out = [Q(0)] * (1 << n)
    for t in range(1 << n):
        b = [(t >> i) & 1 for i in range(n)]
        w = Q(1)
        for i, j in eps_lines:
            w *= EZ.get((b[i], b[j]), Q(0))
            if not w:
                break
        if not w:
            continue
        for a, c in mpair:
            ia, pa = sig_lines[a]
            ic, pc = sig_lines[c]
            w *= PROP[(b[ia], b[ic], b[pa], b[pc])]
            if not w:
                break
        out[t] = w
    return out


def catalogue(nu, nd):
    U, D = list(range(nu)), list(range(nu, nu + nd))
    eps, sig = [], []
    for pu in matchings(U):
        for pd in matchings(D):
            eps.append((list(pu) + list(pd), [], []))
    for r in range(2, min(nu, nd) + 1, 2):
        if (nu - r) % 2 or (nd - r) % 2:
            continue
        for su in itertools.combinations(U, r):
            for sd in itertools.combinations(D, r):
                for bij in itertools.permutations(sd):
                    sl = list(zip(su, bij))
                    ru = [x for x in U if x not in su]
                    rd = [x for x in D if x not in sd]
                    for pu in matchings(ru):
                        for pd in matchings(rd):
                            for mp in matchings(list(range(r))):
                                sig.append((list(pu) + list(pd), sl, list(mp)))
    return eps, sig


def dens(vecs):
    cols = max(len(v) for v in vecs)
    return [[v[j] for j in range(cols)] for v in vecs if any(v)]


def uniq_rows(sv):
    seen, out = set(), []
    for v in sv:
        k = tuple(v)
        if k not in seen:
            seen.add(k)
            out.append(v)
    return out


def measure(nu, nd):
    """一次测全套：$\varepsilon$ 道、$\sigma$ 道（去重）、截断正对照。"""
    n = nu + nd
    eps, sig = catalogue(nu, nd)
    ev = dens([structure_value(n, *s) for s in eps])
    uniq = uniq_rows(dens([structure_value(n, *s) for s in sig]))
    r_e = q_rank(ev) if ev else 0
    r_all = q_rank(ev + uniq) if (ev or uniq) else 0
    sub = [e for e in eps if (0, 1) in e[0]]
    tv = dens([structure_value(n, *s) for s in sub])
    r_t = q_rank(tv) if tv else 0
    r_ta = q_rank(tv + uniq) if (tv or uniq) else 0
    pred = cg_j0(nu) * cg_j0(nd)
    return {'nu': nu, 'nd': nd, 'space': 1 << n, 'eps_n': len(ev), 'eps_rank': r_e,
            'sig_n': len(sig), 'sig_uniq': len(uniq), 'union_rank': r_all,
            'adds': r_all - r_e, 'relations': len(ev) + len(uniq) - r_all,
            'pred': pred, 'cat_ok': r_e == pred,
            'tr_sub': len(sub), 'tr_all': len(eps), 'tr_rank': r_t,
            'tr_adds': r_ta - r_t, 'tr_degenerate': len(sub) == len(eps)}


def worker(pair):
    r = measure(*pair)
    print('S2 (%d,%d) 分量空间=%d | eps 道 %d 条 秩 %d | sigma 道 %d 条(去重 %d) | 并秩 %d 新增 %d'
          ' | 关系数 %d | 特征标预测 %d | eps 目录自检 %s'
          % (pair[0], pair[1], r['space'], r['eps_n'], r['eps_rank'], r['sig_n'], r['sig_uniq'],
             r['union_rank'], r['adds'], r['relations'], r['pred'],
             'PASS' if r['cat_ok'] else '**FAIL(目录非法)**'))
    print('T2 (%d,%d) 截断 eps %d/%d 条 秩 %d | sigma 去重 %d | 截断并秩 %d 新增 %d | 对照 %s'
          % (pair[0], pair[1], r['tr_sub'], r['tr_all'], r['tr_rank'], r['sig_uniq'],
             r['tr_rank'] + r['tr_adds'], r['tr_adds'],
             '退化(截断集=全集)' if r['tr_degenerate'] else '非退化'))
    print('#JSON ' + json.dumps(r, sort_keys=True))


def sweep(tiers, box):
    """逐档子进程 + 硬时间盒；返回 (读数表, 未收敛档列表)。"""
    here = os.path.abspath(__file__)
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    res, unc = {}, []
    for pair in tiers:
        t = time.time()
        try:
            p = subprocess.run([sys.executable, here, '--tier', '%dx%d' % pair],
                               capture_output=True, text=True, timeout=box,
                               encoding='utf-8', env=env)
            print('== (%d,%d) rc=%d secs=%.1f' % (pair[0], pair[1], p.returncode,
                                                   time.time() - t), flush=True)
            print((p.stdout or '').strip(), flush=True)
            if p.stderr.strip():
                print('   stderr: %s' % p.stderr.strip()[:400], flush=True)
            line = [ln for ln in (p.stdout or '').splitlines()
                    if ln.startswith('#JSON ') and p.returncode == 0]
            if not line:
                unc.append(pair)
                continue
            res[pair] = json.loads(line[0][len('#JSON '):])
        except subprocess.TimeoutExpired as ex:
            print('== (%d,%d) TIMEOUT box=%.0fs secs=%.1f partial=%s'
                  % (pair[0], pair[1], box, time.time() - t,
                     (ex.stdout or '').strip()[-200:]), flush=True)
            unc.append(pair)
    return res, unc


# G4 只比**物理读数**那一组字段，逐字段列出、不许由 diff 反推。被排除的只有 G3 那组 `tr_*`，
# 理由写在这里而不是留在脑子里：正对照截断锚在"槽 (0,1) 已配对"，而 (0,1) 两个都是不点指标 ⇒
# 那台对照本身**不是手性标量**，$(\nu,\dot\nu)$ 与 $(\dot\nu,\nu)$ 的 `tr_*` 本来就该不同
# （实测 $(8,2)$ 截断新增 9、$(2,8)$ 的截断集 $=$ 全集）。把对照拉进手性对称判据会把一条
# 真读数判成失败。两组键的并集必须覆盖读数表的全部键 —— 于是"以后多出一个字段"会在这里响，
# 而不是悄悄落到某一侧。
PHYSICS_KEYS = ('space', 'eps_n', 'eps_rank', 'sig_n', 'sig_uniq', 'union_rank',
                'adds', 'relations', 'pred', 'cat_ok')
CONTROL_KEYS = ('tr_sub', 'tr_all', 'tr_rank', 'tr_adds', 'tr_degenerate')


def judge(res, tiers):
    covered = set(PHYSICS_KEYS) | set(CONTROL_KEYS) | {'nu', 'nd'}
    for p in res:
        miss = sorted(set(res[p]) - covered)
        if miss:
            return ['G4 读数表出现未归类字段 %s ⇒ 既没进手性对称判据、也没进对照豁免，'
                    '判据覆盖面已过期' % (miss,)]
    bad = []
    for pair in tiers:
        if pair not in res:
            continue
        r = res[pair]
        if not r['cat_ok']:
            bad.append('G1 %s eps 目录自检失败：秩 %s vs 特征标预测 %s'
                       % (pair, r['eps_rank'], r['pred']))
        if r['adds'] != 0:
            bad.append('G2 %s sigma 道新增秩 %s（应为 0）' % (pair, r['adds']))
        if r['tr_degenerate']:
            if r['nu'] != 2:
                bad.append('G3 %s 截断集=全集但 nu=%s 不为 2 ⇒ "退化"的结构理由不成立'
                           % (pair, r['nu']))
            elif r['tr_rank'] != r['eps_rank']:
                bad.append('G3 %s 自称退化却截断秩 %s 不等于完整秩 %s'
                           % (pair, r['tr_rank'], r['eps_rank']))
        elif r['tr_adds'] <= 0:
            bad.append('G3 %s 正对照退化：截断基线下新增仍读 %s ⇒ 主判据的 0 无法与恒零计数器区分'
                       % (pair, r['tr_adds']))
    for pair in tiers:
        mir = (pair[1], pair[0])
        if pair in res and mir in res:
            diff = [k for k in PHYSICS_KEYS if res[pair][k] != res[mir][k]]
            if diff:
                bad.append('G4 %s 与 %s 物理读数不等（字段 %s）⇒ 跨手性不变量断了'
                           % (pair, mir, diff))
    return bad


def main():
    box, only_wide, tiers = 600.0, False, None
    argv = sys.argv[1:]
    for i, a in enumerate(argv):
        if a == '--tier':
            nu, nd = argv[i + 1].split('x')
            worker((int(nu), int(nd)))
            return 0
        if a == '--box':
            box = float(argv[i + 1])
        elif a == '--tiers':
            tiers = tuple(tuple(int(y) for y in x.split('x'))
                          for x in argv[i + 1].split(','))
        elif a == '--only-wide':
            only_wide = True
    if tiers is None:
        tiers = WIDE if only_wide else PINNED + WIDE
    print('档集合：%s ｜ 每档时间盒 %.0f s'
          % ('、'.join('(%d,%d)' % t for t in tiers), box), flush=True)
    res, unc = sweep(tiers, box)
    for k in ('eps_rank', 'sig_uniq', 'adds', 'tr_adds', 'relations'):
        print('合计 %s：%s' % (k, '  '.join('%s=%s' % ('(%d,%d)' % p, res[p][k])
                                             for p in tiers if p in res)), flush=True)
    if unc:
        print('未收敛档：%s ⇒ 退出码 2：本次是**部分完成**，其合计不得进任何文档'
              % ('、'.join('(%d,%d)' % p for p in unc)), flush=True)
        return 2
    bad = judge(res, tiers)
    if bad:
        print('判据失败 %d 条：\n  %s' % (len(bad), '\n  '.join(bad)), flush=True)
        return 1
    print('判据：G1 目录自检 %d/%d PASS ｜ G2 各档"新增"全读 0 ｜ G3 除 nu=2 档（有结构理由）外'
          '正对照全部非退化 ｜ G4 手性对称' % (sum(1 for p in res if res[p]['cat_ok']), len(tiers)),
          flush=True)
    print('=== 全部 %d 档收敛、四条判据全 PASS ===' % len(tiers), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
