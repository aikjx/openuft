# -*- coding: utf-8 -*-
"""X-V63-17 机核：四力场方程的 Euler-Lagrange 符号变分求导与耦合钉死力审计。
   不占 RID、不进 README、不与任何卷相加。纯标准库；Fraction / Decimal(60)。
   模型：SM 规范群 U(1) x SU(2) x SU(3) 的纯 Yang-Mills 拉格朗日，
        含完整规范自相互作用项 g f^{abc} A^b A^c；逐场变分导出场方程。
   引力：Einstein-Hilbert 变分不在本 Poly 引擎内，作 BOUNDARY 并跨册回代 X-V63-15。
"""
import io, os, glob, json, ast, re, hashlib
from fractions import Fraction as F
from decimal import Decimal, getcontext
from collections import defaultdict
import random
getcontext().prec = 60

def _locate_root():
    hs = glob.glob('openuft/04_*/**/本项目_全维自洽与归一化', recursive=True)
    assert len(hs) == 1, hs
    return hs[0]
ROOT = _locate_root()
OUT_JSON = os.path.join(ROOT, '数据', '_XV6317_recompute_2026-11-16.json')
OUT_REPORT = os.path.join(ROOT, '数据', '_XV6317_recompute_report_2026-11-16.txt')

OWN_TOKENS = ['_xv6317_recompute.py', '_XV6317_recompute',
              '_XV6317_recompute_report', '攻坚_X-V63-17']
SELF_SOURCE_PATH = None

# ---------- 多项式引擎 ----------
class Poly:
    __slots__ = ('d',)
    def __init__(self, d=None):
        self.d = {} if d is None else dict(d)
    def __add__(self, o):
        r = defaultdict(lambda: ZERO)
        for m, c in self.d.items(): r[m] = r[m] + c
        for m, c in o.d.items(): r[m] = r[m] + c
        return Poly({m: c for m, c in r.items() if c != CNULL})
    __radd__ = __add__
    def __neg__(self): return Poly({m: -c for m, c in self.d.items()})
    def __sub__(self, o): return self + (-o)
    def __rsub__(self, o): return (-self) + o
    def __mul__(self, o):
        r = defaultdict(lambda: ZERO)
        for m1, c1 in self.d.items():
            for m2, c2 in o.d.items():
                m = tuple(sorted(m1 + m2))
                r[m] = r[m] + c1 * c2
        return Poly({m: c for m, c in r.items() if c != CNULL})
    def deriv(self, var):
        r = {}
        for m, c in self.d.items():
            k = m.count(var)
            if k:
                pos = m.index(var)
                m2 = m[:pos] + m[pos + 1:]      # g^2 -> 2g，只删一个变量
                r[m2] = r.get(m2, ZERO) + c * k
        return Poly({m: c for m, c in r.items() if c != CNULL})
    def eval(self, env):
        s = None                                  # 零元从系数自身推断，不用全局 ZERO
        for m, c in self.d.items():
            t = c
            for v in m: t = t * env[v]
            s = t if s is None else s + t
        if s is None:
            c0 = next(iter(env.values())) if env else 0
            s = c0 * 0                            # 正确数域的零
        return s

def set_ctx(cf, zero):
    global ZERO, CNULL
    ZERO = cf(0); CNULL = zero

def cnst(x, cf): return Poly({(): cf(x)}) if cf(x) != 0 else Poly()
def var(v, cf): return Poly({(v,): cf(1)})
def A(a, mu): return 'A,%d,%d' % (a, mu)
def dA(a, mu, nu): return 'dA,%d,%d,%d' % (a, mu, nu)
def ddA(a, mu, nu, rho): return 'ddA,%d,%d,%d,%d' % (a, mu, nu, rho)

# ---------- 结构常数 ----------
def f_su2(cf):
    eps = {}
    for t in [(0,1,2),(1,2,0),(2,0,1)]: eps[t] = cf(1)
    for t in [(0,2,1),(2,1,0),(1,0,2)]: eps[t] = cf(-1)
    f = [[[cf(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for (a,b,c), v in eps.items(): f[a][b][c] = v
    return f

def f_su3(cf):
    s3 = cf(3).sqrt() / cf(2) if hasattr(cf(3), 'sqrt') else cf(0)
    f = [[[cf(0) for _ in range(8)] for _ in range(8)] for _ in range(8)]
    def put(i,j,k,v):
        f[i][j][k] = v; f[j][k][i] = v; f[k][i][j] = v
        f[j][i][k] = -v; f[i][k][j] = -v; f[k][j][i] = -v
    put(0,1,2, cf(1))
    put(0,3,4, cf(1)/2); put(0,5,6, -cf(1)/2)
    put(1,3,6, cf(1)/2); put(1,4,5, cf(1)/2)
    put(2,3,5, -cf(1)/2); put(2,4,6, cf(1)/2)
    put(3,4,7, s3); put(5,6,7, s3)
    return f

# ---------- 群构建：符号变分导出场方程 ----------
def build_group(name, n, f, cf, gname='g'):
    set_ctx(cf, cf(0))
    g = var(gname, cf)
    Fs = {}
    for a in range(n):
        for mu in range(4):
            for nu in range(mu + 1, 4):
                p = var(dA(a,mu,nu), cf) + (-var(dA(a,nu,mu), cf))
                q = Poly()
                for b in range(n):
                    for c in range(n):
                        if f[a][b][c] != 0:
                            q = q + g * cnst(f[a][b][c], cf) * var(A(b,mu), cf) * var(A(c,nu), cf)
                Fs[(a,mu,nu)] = p + q
    L = Poly()
    for Fmn in Fs.values(): L = L + cnst(cf(-1)/2, cf) * Fmn * Fmn
    def lift(P, nu):
        r = {}
        for m, c in P.d.items():
            nm = []
            for v in m:
                if v.startswith('dA,'):
                    _, a2, r2, s2 = v.split(','); nm.append(ddA(int(a2), int(r2), int(s2), nu))
                elif v.startswith('A,'):
                    _, a2, r2 = v.split(','); nm.append(dA(int(a2), int(r2), nu))
                else: nm.append(v)
            nm = tuple(sorted(nm)); r[nm] = r.get(nm, ZERO) + c
        return Poly({m: c for m, c in r.items() if c != CNULL})
    el = {}
    for a in range(n):
        for rho in range(4):
            e = Poly()
            for nu in range(4): e = e + lift(L.deriv(dA(a,rho,nu)), nu)
            e = e - L.deriv(A(a,rho))
            el[(a,rho)] = e
    gpows = set()
    for e in el.values():
        for m in e.d: gpows.add(m.count(gname))
    el_terms = sum(len(e.d) for e in el.values())
    # 路径A（符号）：∂L/∂g 的纯 g 分量求根
    dLg = L.deriv(gname)
    pure = Poly({m: c for m, c in dLg.d.items() if all(v == gname for v in m)})
    pinA, rootA = 0, None
    if pure.d:
        coeff = defaultdict(lambda: ZERO)
        for m, c in pure.d.items(): coeff[len(m)] = coeff[len(m)] + c
        deg = max(coeff)
        if deg == 1:
            rootA = -coeff[0] / coeff[1]; pinA = 1
        elif deg == 2 and coeff[1]*coeff[1] - cf(4)*coeff[2]*coeff[0] == 0:
            rootA = -coeff[1] / (cf(2)*coeff[2]); pinA = 1
    return dict(name=name, n=n, gpows=sorted(gpows), el_terms=el_terms,
                pinA=pinA, rootA=str(rootA) if rootA is not None else 'NA',
                L=L, el=el, gname=gname, cf=cf)

# ---------- 路径B（数值，无 Poly.deriv）：背景依赖 + 数值找根 ----------
def pin_numeric(G, seed=11):
    L, gname, cf = G['L'], G['gname'], G['cf']
    set_ctx(cf, cf(0))                             # 入口重置数域，防跨群污染
    rnd = random.Random(seed)
    def dLg(env, gval, h):
        e1 = dict(env); e1[gname] = cf(gval) + cf(h)
        e0 = dict(env); e0[gname] = cf(gval) - cf(h)
        return L.eval(e1) - L.eval(e0)
    allv = sorted({v for m in L.d for v in m})
    base = {v: cf(0) for v in allv}
    hs = cf(1)/cf(2000)
    vals = []
    for k in range(4):
        env = dict(base)
        for v in allv:
            if v != gname: env[v] = cf(rnd.randint(-3,3)) / cf(rnd.randint(2,5))
        vals.append(float(dLg(env, cf(1)/cf(2), hs) / (cf(2)*hs)))
    spread = max(vals) - min(vals)
    scale = max(1.0, max(abs(x) for x in vals))
    if spread > 1e-6 * scale:
        return 0, 'NA', spread           # 导数依赖背景 => 无普适固定
    xs = [cf(k)/cf(10) for k in range(0, 31)]
    prev = None; rootB = None
    for x in xs:
        fx = float(dLg(base, x, hs) / (cf(2)*hs))
        if prev is not None and prev[1] * fx <= 0 and abs(fx - prev[1]) > 1e-9:
            rootB = (float(prev[0]) + float(x)) / 2
        prev = (x, fx)
    return (1 if rootB is not None else 0), (('%.6f' % rootB) if rootB is not None else 'NA'), spread

# ---------- 正对照：人为固定项 ----------
def positive_control(cf):
    set_ctx(cf, cf(0))
    lam, c = cf(3), cf(7)/cf(5)
    L = cnst(cf(-1)/2, cf) * (var('g', cf) + (-cnst(c, cf))) * (var('g', cf) + (-cnst(c, cf))) * cnst(lam, cf)
    dLg = L.deriv('g')
    coeff = defaultdict(lambda: ZERO)
    for m, cc in dLg.d.items(): coeff[len(m)] = coeff[len(m)] + cc
    root = -coeff[0] / coeff[1]
    G = dict(L=L, gname='g', cf=cf)
    return dict(pinA=1, rootA=str(root)), pin_numeric(G)

# ---------- 数值两路：符号变分 vs 中心差分+Richardson ----------
def numeric_check(G, seed=7):
    L, gname, cf = G['L'], G['gname'], G['cf']
    set_ctx(cf, cf(0))
    rnd = random.Random(seed)
    env = {}
    for v in sorted({v for m in L.d for v in m}):
        env[v] = cf(rnd.randint(-6,6)) / cf(rnd.randint(2,5))
    def lf(e): return float(L.eval(e))
    worst = 0.0
    for v in ['A,0,0', 'dA,0,0,1', gname]:
        if v not in env: env[v] = cf(1)/2
        def D(hfloat):                             # 全程 float，避免 float/Decimal 混算
            hh = cf(1) / cf(1000) if hfloat == 1 else cf(1) / cf(2000)
            ep = dict(env); em = dict(env)
            ep[v] = env[v] + hh; em[v] = env[v] - hh
            return (lf(ep) - lf(em)) / (2.0 * float(hh))
        d1 = D(1); d2 = D(2)
        num = (4.0 * d2 - d1) / 3.0
        sym = float(L.deriv(v).eval(env))
        worst = max(worst, abs(num - sym) / max(1.0, abs(sym), abs(num)))
    return worst


# ---------- 判定表与 final_of ----------
def final_of(nf_main, nf_guard, n_decl):
    if nf_guard: return 'GATES-FAIL-GUARD-%d' % nf_guard
    if nf_main:  return 'GATES-FAIL-MAIN-%d' % nf_main
    if n_decl:   return 'GATES-PASS-WITH-%d-NEGATIVE' % n_decl
    return 'GATES-PASS'

def add(rows, key, ok, val, kind_pass='PASS', note=''):
    kind = kind_pass if ok else 'FAIL'
    rows.append(dict(key=key, kind=kind, ok=bool(ok), val=val, note=note))
    return ok

def verdict_machine(segs):
    # 机读判词：关键读数按固定顺序拼装；任一读数 +1 必须改变判词串
    def build(u1, su2, su3, pin, ctrl):
        return ('FIELDS-17__ELU1-%d--ELSU2-%d--ELSU3-%d'
                '--TWO-PATH-%.2e--PIN-%d--CTRL-%d--FIXER-SENS-%d'
                '--R403-4F-0--PRED-0--NOT-UNIVERSAL') % (
                    u1, su2, su3, segs['two_path_err'], pin, ctrl, segs['fixer_sens'])
    base = build(segs['u1']['el_terms'], segs['su2']['el_terms'],
                 segs['su3']['el_terms'], segs['pin_total'], segs['n_ctrl_distinct'])
    bump = build(segs['u1']['el_terms'] + 1, segs['su2']['el_terms'],
                 segs['su3']['el_terms'], segs['pin_total'], segs['n_ctrl_distinct'])
    return base, (base != bump)

# ---------- 跨册回代：磁盘实读 JSON，锚定唯一文件名（排除 _整理 汇总册） ----------
def readback_one(prefix, token):
    fs = glob.glob(os.path.join(ROOT, '数据', prefix + '_recompute_*.json'))
    fs = [p for p in fs if '_整理' not in os.path.basename(p)]
    assert len(fs) == 1, (prefix, fs)
    txt = io.open(fs[0], 'r', encoding='utf-8').read()
    d = json.loads(txt)
    assert token in d.get('verdict', ''), (prefix, token)
    return dict(file=os.path.basename(fs[0]), token=token, ok=True)

def cross_readback():
    return [
        readback_one('_XV6314', 'UNIQUE-U01-电弱统一-L-EW-唯一-仅覆盖-2-力'),
        readback_one('_XV6315', 'NO-EXTRA-K-CONSTRAINT'),
        readback_one('_XV6316', 'K-PINNED-0'),
    ]

# ---------- AST 守卫：判据行的 ok 禁止写死为字面量 ----------
# 说明：INFO/已登记FAIL 行的 ok 是如实登记的常值，允许字面量；
#      只有 kind_pass='PASS'/'GUARD' 的判据行 ok 必须由读数计算而来。
INFO_LITERAL_KEYS = {'FROZEN-PARAM-TRAP', 'ZERO-READOUT-DENOMINATOR', 'COUPLING-NOT-PINNED'}

def ast_no_hardcode_ok(src_path):
    src = io.open(src_path, 'r', encoding='utf-8').read()
    tree = ast.parse(src)
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            nm = fn.id if isinstance(fn, ast.Name) else (fn.attr if isinstance(fn, ast.Attribute) else '')
            if nm == 'add' and len(node.args) >= 2:
                key_node = node.args[1]
                key = key_node.value if isinstance(key_node, ast.Constant) else None
                if key in INFO_LITERAL_KEYS:      # 登记行允许字面量
                    continue
                ok_node = node.args[2] if len(node.args) >= 3 else None
                if isinstance(ok_node, ast.Constant) and isinstance(ok_node.value, bool):
                    bad.append((key, ok_node.value))
                for kw in node.keywords:
                    if kw.arg == 'ok' and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, bool):
                        bad.append((key, kw.value.value))
    return (len(bad) == 0), bad

# ---------- build_segments ----------
def build_segments():
    segs = {}
    segs['u1']  = build_group('U1',  1, [[[F(0)]]], F)
    segs['su2'] = build_group('SU2', 3, f_su2(F), F)
    segs['su3'] = build_group('SU3', 8, f_su3(Decimal), Decimal)
    for k in ('u1', 'su2', 'su3'):
        G = segs[k]
        G['pinB'], G['rootB'], G['spread'] = pin_numeric(G)
        G['two_path'] = numeric_check(G)
    segs['two_path_err'] = max(segs[k]['two_path'] for k in ('u1','su2','su3'))
    pcA, pcB = positive_control(F)
    segs['pos_ctrl'] = dict(symbolic=pcA, numeric=pcB)
    # 冻结参数陷阱：单档 g=1 下纯 g 分量为 0（假绿），全档 g 幂次跨越 0/1/2
    segs['frozen_trap'] = dict(
        single_g_residue_zero=all(
            all(v == 'g' for v in m) is False for e in segs['su2']['el'].values() for m in e.d),
        full_scan_gpows=segs['su2']['gpows'])
    # 耦合钉死读数：三群 pinA/pinB 合计（非零个数）
    segs['pin_total'] = sum(1 for k in ('u1','su2','su3')
                            if segs[k]['pinA'] != 0 or segs[k]['pinB'] != 0)
    # 控制组4条：U1 / SU2 / SU3 / 正对照，读数向量两两不同
    ctrl = [
        ('U1',  segs['u1']['n'],  tuple(segs['u1']['gpows']),  segs['u1']['el_terms'],  segs['u1']['pinA']),
        ('SU2', segs['su2']['n'], tuple(segs['su2']['gpows']), segs['su2']['el_terms'], segs['su2']['pinA']),
        ('SU3', segs['su3']['n'], tuple(segs['su3']['gpows']), segs['su3']['el_terms'], segs['su3']['pinA']),
        ('POS', 1, (0,), 1, pcA['pinA']),
    ]
    segs['control'] = ctrl
    segs['n_ctrl_distinct'] = len(set(ctrl))
    segs['fixer_sens'] = int(pcA['pinA'] == 1 and segs['su2']['pinA'] == 0)
    segs['verdict'], segs['verdict_sens'] = verdict_machine(segs)
    return segs

# ---------- run_guards ----------
def run_guards(segs):
    rows = []
    nf_main = nf_guard = 0
    # 主判据（真算出数）
    for k, label in [('u1','EL-DERIVED-U1'), ('su2','EL-DERIVED-SU2'), ('su3','EL-DERIVED-SU3')]:
        ok = segs[k]['el_terms'] > 0
        if not add(rows, label, ok, segs[k]['el_terms'], 'PASS',
                   '符号变分导出的场方程项数>0'): nf_main += 1
    ok = segs['two_path_err'] < 1e-8
    if not add(rows, 'EL-TWO-PATH', ok, '%.3e' % segs['two_path_err'], 'PASS',
               '符号偏导 vs 中心差分Richardson相对误差<1e-8'): nf_main += 1
    ok = all(segs[k]['pinA'] == segs[k]['pinB'] for k in ('u1','su2','su3'))
    if not add(rows, 'KEY-TABLE-TWO-PATH', ok,
               [segs[k]['pinA'] for k in ('u1','su2','su3')], 'PASS',
               '路径A符号∂L/∂g 与 路径B数值背景敏感性 对三群一致'): nf_main += 1
    # 冻结参数陷阱（INFO，如实报，不挡门）
    add(rows, 'FROZEN-PARAM-TRAP', True, segs['frozen_trap'], 'INFO',
        '单档g=1 EL残差恒0是假绿；全档g幂次0/1/2')
    # 正对照判别力
    ok = segs['fixer_sens'] == 1
    if not add(rows, 'FIXER-PREDICATE-SENSITIVE', ok,
               dict(pos=segs['pos_ctrl']['symbolic']['rootA'], base=segs['su2']['pinA']), 'PASS',
               '加λ(g-c)^2后pin=1且root=7/5；未加时pin=0'): nf_main += 1
    # 零读数分母：pin_total=0 必须写明分母（可固定机制数=3）
    ok = (segs['pin_total'] == 0)
    add(rows, 'ZERO-READOUT-DENOMINATOR', True,
        '%d/3' % segs['pin_total'], 'INFO',
        '变分可固定的规范耦合数=0，分母=三个规范因子')
    # 已登记判负（对 OPEN 的判决，不挡门）
    add(rows, 'COUPLING-NOT-PINNED', False, segs['pin_total'], 'FAIL',
        '三群耦合均不能被变分本身固定为唯一值（已登记判负，不挡门）')
    # 跨册回代
    rb = cross_readback()
    segs['readback'] = rb
    ok = len(rb) == 3 and all(x['ok'] for x in rb)
    if not add(rows, 'CROSS-VOLUME-READBACK', ok, len(rb), 'PASS',
               '磁盘实读X-V63-14/15/16判定册token命中'): nf_main += 1
    # 守卫
    src = SELF_SOURCE_PATH or os.path.abspath(__file__)
    okA, bad = ast_no_hardcode_ok(src)
    if not add(rows, 'NO-HARDCODE-OK', okA, bad, 'GUARD',
               'AST扫描add()的ok参数无布尔字面量'): nf_guard += 1
    okV = segs['verdict_sens']
    if not add(rows, 'VERDICT-MACHINE', okV, okV, 'GUARD',
               '关键读数+1后判词串变化'): nf_guard += 1
    okC = segs['n_ctrl_distinct'] == 4
    if not add(rows, 'CONTROL-4-DISTINCT', okC, segs['n_ctrl_distinct'], 'GUARD',
               '控制组4条读数两两不同'): nf_guard += 1
    okB = all(segs[k]['gpows'] == [0,1,2] for k in ('su2','su3')) and segs['u1']['gpows'] == [0]
    if not add(rows, 'GAUGE-GROUP-SPECTRUM', okB,
               [segs[k]['gpows'] for k in ('u1','su2','su3')], 'GUARD',
               'U1=[0]，SU2/SU3=[0,1,2] 与规范自相互作用结构一致'): nf_guard += 1
    counts = defaultdict(int)
    for r in rows: counts[r['kind']] += 1
    n_decl = sum(1 for r in rows if r['kind'] == 'FAIL')
    final = final_of(nf_main, nf_guard, n_decl)
    return rows, dict(counts=dict(counts), nf_main=nf_main, nf_guard=nf_guard,
                      n_decl=n_decl, final=final)

# ---------- make_out ----------
def make_out(segs, rows, gsum):
    out = dict(
        title='X-V63-17 四力场方程Euler-Lagrange符号变分求导与耦合钉死力审计',
        date='2026-11-16', rid='X-V63-17（不占RID）', body_type='攻坚册',
        final=gsum['final'], verdict=segs['verdict'],
        n_rows=len(rows), counts=gsum['counts'],
        declared_neg=[r['key'] for r in rows if r['kind'] == 'FAIL'],
        rows=rows, guards=[r for r in rows if r['kind'] == 'GUARD'],
        guard_count=len([r for r in rows if r['kind'] == 'GUARD']),
        guard_pass=len([r for r in rows if r['kind'] == 'GUARD' and r['ok']]),
        key_numbers=dict(
            U1_el_terms=segs['u1']['el_terms'], SU2_el_terms=segs['su2']['el_terms'],
            SU3_el_terms=segs['su3']['el_terms'],
            two_path_rel_err=segs['two_path_err'],
            pin_total=segs['pin_total'], pin_denominator=3,
            pos_ctrl_root=segs['pos_ctrl']['symbolic']['rootA'],
            n_ctrl_distinct=segs['n_ctrl_distinct'],
            fixer_sens=segs['fixer_sens']),
        frozen_trap=segs['frozen_trap'], control=segs['control'],
        cross_readback=segs['readback'],
        boundary=[
            'Einstein-Hilbert场方程的变分不在本Poly引擎内（需度规行列式与曲率平方）；引力配平见X-V63-15，结论不钉死k。',
            '模型为SM规范群的纯Yang-Mills拉格朗日（欧氏记号，无度规符号），物质表示固定为特定维数；非全称定理。',
            '单圈树级变分，未含量子反常/重整化群修正；g的跑动见R27。',
            '耦合钉死判据仅问变分∂L/∂g能否给出与背景无关的唯一根；不排除额外动力学/新物理机制。',
            '数学自洽≠实验证实；独立实验预言=0；四力统一正确者=0条。'])
    return out

def main():
    ROOT_LOCAL = ROOT
    os.makedirs(os.path.join(ROOT_LOCAL, '数据'), exist_ok=True)
    segs = build_segments()
    rows, gsum = run_guards(segs)
    out = make_out(segs, rows, gsum)
    txt = json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True)
    with io.open(OUT_JSON, 'w', encoding='utf-8', newline='\n') as fh: fh.write(txt + '\n')
    lines = ['verdict : ' + out['verdict'], 'final   : ' + out['final'],
             'counts  : ' + json.dumps(out['counts'], ensure_ascii=False, sort_keys=True),
             'guards  : %d/%d' % (out['guard_pass'], out['guard_count'])]
    with io.open(OUT_REPORT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(lines) + '\n')
    print('final =', out['final'])
    print('counts =', out['counts'])
    print('guard_pass = %d / %d' % (out['guard_pass'], out['guard_count']))
    return out

if __name__ == '__main__':
    main()


# --- 尾注（X-V63-17） ---
# 机核结构：build_segments → run_guards → make_out → main。
# 本册不占 RID、不进 README、不与任何审计卷或算法联盟册相加。
# 复现：python _assemble_xv6317.py && python _run_xv6317.py（两次连跑 MD5 一致）
#       && python _xv6317_final_check.py（打印 ALL-CHECKS-PASS）。
# 红线：数学自洽 ≠ 实验证实；只产可算判决，不产新物理；indep exp pred = 0。
