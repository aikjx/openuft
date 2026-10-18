# -*- coding: utf-8 -*-
"""Spinor reality machine table v14 (EXACT MONOMIAL ENGINE, no solvers at all).

Every constructed gamma is a monomial matrix (one nonzero Z[i] entry per row);
the whole computation is exact integer bookkeeping on (flipvec, row-values):
 C1 Clifford relations verified on explicit Z[i] matrices (abort on fail);
 C2 even-D Omega^2: matrix product vs closed formula (abort on mismatch);
 C3 irreducibility: #distinct monomial classes of {gamma_A} == n^2 (linear
    independence of distinct monomial permutations - exact, no rank call);
 C4 Frobenius-Schur indicator over the pin group G = {+-gamma_A}:
      nu2 = (1/|G|) sum_g chi(g^2) = n * sum_A sigma_A / 2^D  (each pair +-A
      contributes tr(n*sigma_A I) once up to +- sign duplication),
    nu2 = +1 REAL / -1 QUATERNION / 0 COMPLEX, asserted in {-1,0,1};
 C5 explicit reality operator cross-channel: monomial B with gamma_a B = B gamma_a^*
    (ENTRYWISE conjugate - the J(v)=B vbar condition, verified exactly),
    sign of BBbar (constant, +-1) must AGREE with nu2 or the row ABORTS;
 C6 MW/sMW: B gamma_5 <-> Gamma commute/anticommute checked exactly as monomials;
    MW_possible = (nu2==+1 and exists invertible B commuting with Gamma).
Registered range: all (t,r) with 1 <= t+r <= 12. Exit!=0 if any anchor FAIL,
any nu2 outside {-1,0,1}, any cross-channel sign disagreement, or any
PRIME... (none needed: fully exact integers).
Anchors (published physics): D2M MW; D3M/D4M Majorana; D4M no MW; D6(2,4) MW;
D6 Mink sM not M; D4 Euclid quaternionic; D6(5,1) quaternionic; D3 Euclid
quaternionic; D1 timelike complex. 9 gates.
"""
import numpy as np, json, sys, os

ZERO = (0, 0); ONE = (1, 0); MONE = (-1, 0); IIM = (0, 1)
def cmul(x, y): return (x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def cneg(x): return (-x[0], -x[1])
def cconj(x): return (x[0], -x[1])
sx = [[ZERO, ONE], [ONE, ZERO]]
sz = [[ONE, ZERO], [ZERO, MONE]]
sy = [[ZERO, (0, -1)], [(0, 1), ZERO]]
i2m = [[ONE, ZERO], [ZERO, ONE]]

def kronl(mats):
    out = mats[0]
    for m in mats[1:]:
        a = len(out); b = len(m); n = a*b
        res = [[ZERO]*n for _ in range(n)]
        for i in range(a):
            for j in range(a):
                cij = out[i][j]
                if cij == ZERO: continue
                for k in range(b):
                    for l in range(b):
                        res[i*b+k][j*b+l] = cmul(cij, m[k][l])
        out = res
    return out

def matmul(A, B):
    n = len(A)
    res = [[ZERO]*n for _ in range(n)]
    for i in range(n):
        ri = res[i]
        for k in range(n):
            a = A[i][k]
            if a == ZERO: continue
            Bk = B[k]
            for j in range(n):
                b = Bk[j]
                if b != ZERO:
                    ri[j] = (ri[j][0]+a[0]*b[0]-a[1]*b[1], ri[j][1]+a[0]*b[1]+a[1]*b[0])
    return res

def eye_mat(n): return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]

def jw_even(k):
    g = []
    for j in range(k):
        g.append(kronl([i2m]*j + [sx] + [sz]*(k-1-j)))
        g.append(kronl([i2m]*j + [sy] + [sz]*(k-1-j)))
    return g

def build(t, r, sab=False):
    D = t + r
    if D == 1:
        gens = [[[ONE]]]
    elif D % 2 == 0:
        gens = jw_even(D//2)
    else:
        gens = jw_even((D-1)//2)
        n = len(gens[0])
        Om = eye_mat(n)
        for g in gens:
            Om = matmul(Om, g)
        # raw Om (product of 2k raw generators, each squaring to +1):
        # anticommutes with every generator; Om^2 = (-1)^{(D-1)(D-2)/2} w.r.t.
        # raw squares. Normalize by a phase in Z[i] so that the APPENDED
        # generator has RAW square +1 before the timelike i-flips below.
        s2 = matmul(Om, Om)
        neg = all(s2[i][j] == (MONE if i == j else ZERO) for i in range(n) for j in range(n))
        pos = all(s2[i][j] == (ONE if i == j else ZERO) for i in range(n) for j in range(n))
        if neg:
            Om = [[cmul(IIM, x) for x in rr] for rr in Om]
        elif not pos:
            raise RuntimeError('Omega^2 not +-I at (%d,%d)' % (t, r))
        gens = gens + [Om]
    want = [-1]*t + [1]*r
    G = []
    for g, w in zip(gens, want):
        if w < 0:
            g = [[cmul(IIM, x) for x in rr] for rr in g]
        G.append(g)
    n = len(G[0])
    if sab:
        # C1 mutant: break gamma_0 by a factor 2 while the claimed signature
        # (want) is unchanged -- the Clifford verification MUST abort on it.
        G[0] = [[(2 * x[0], 2 * x[1]) for x in rr] for rr in G[0]]
    for a in range(D):
        for b in range(a, D):
            lhs = matmul(G[a], G[b]); rhs = matmul(G[b], G[a])
            for i in range(n):
                for j in range(n):
                    s = (lhs[i][j][0]+rhs[i][j][0], lhs[i][j][1]+rhs[i][j][1])
                    # {gamma_a,gamma_b} = 2*want[a]*delta_ab*delta_ij
                    exp = 2*want[a]*(1 if (a == b and i == j) else 0)
                    t_ = (exp, 0)
                    if s != t_:
                        raise RuntimeError('clifford fail at (%d,%d) entry (%d,%d) sig (%d,%d)' % (a, b, i, j, t, r))
    return G, want

# ---- monomial extraction and algebra ----
class Mon:
    __slots__ = ('f', 'v')
    def __init__(self, f, v):
        self.f = f; self.v = tuple(v)
    def __eq__(self, o):
        return self.f == o.f and self.v == o.v
    def key(self):
        return (self.f, self.v)

def extract_Mon(M):
    n = len(M)
    f0 = None
    v = []
    for i in range(n):
        nz = [(j, M[i][j]) for j in range(n) if M[i][j] != ZERO]
        if len(nz) != 1:
            raise RuntimeError('not monomial row %d' % i)
        j, val = nz[0]
        if f0 is None:
            f0 = i ^ j
        elif i ^ j != f0:
            raise RuntimeError('perm not xor-type')
        v.append(val)
    return Mon(f0, v)

def mmul(A, B):
    f = A.f ^ B.f
    v = [cmul(A.v[i], B.v[i ^ A.f]) for i in range(len(A.v))]
    return Mon(f, v)

def mconj(B):
    return Mon(B.f, [cconj(x) for x in B.v])

def scalar_of(M, n):
    """M must be f=0 with constant v: return that Z[i] scalar else raise."""
    if M.f != 0:
        return None
    if any(x != M.v[0] for x in M.v):
        return None
    return M.v[0]

def analyze(t, r, sab=False):
    D = t + r
    G, want = build(t, r, sab)
    n = len(G[0])
    row = {'t': t, 'r': r, 'D': D, 'size': n}
    Mons = [extract_Mon(g) for g in G]
    # gamma_A table by ascending mask recursion
    gam = [None]*(1 << D)
    gam[0] = Mon(0, [ONE]*n)
    for mask in range(1, 1 << D):
        low = mask & -mask
        a = low.bit_length() - 1
        rest = mask ^ low
        # ordered product gamma_a... keep ASCENDING order: gamma_mask = gamma_rest' ... simpler:
        # multiply in ascending index order: build directly
        M = Mon(0, [ONE]*n)
        for b in range(D):
            if mask >> b & 1:
                M = mmul(M, Mons[b])
        gam[mask] = M
    # C3 irreducibility: distinct classes
    classes = {}
    dep = False
    for mask in range(1 << D):
        key = gam[mask].key()
        if key in classes:
            dep = True
        classes[key] = mask
    row['monomial_classes'] = len(classes)
    row['span_full'] = (len(classes) == n*n)
    # C4 nu2 = (1/|G|) sum chi(g^2), G={+-gamma_A}: pairs +- have same square:
    tot = 0
    for mask in range(1 << D):
        sq = mmul(gam[mask], gam[mask])
        sc = scalar_of(sq, n)
        if sc is None or sc[1] != 0 or sc[0] not in (1, -1):
            row['abort'] = 'gamma_A^2 not real scalar (class issue)'
            return row
        tot += n * sc[0]
    from fractions import Fraction
    nu2 = Fraction(tot, 1 << D)   # |G| = 2^{D+1}, each mask twice: 2*sum/2^{D+1}=sum/2^D
    if nu2 not in (-1, 0, 1):
        row['abort'] = 'nu2 not in {-1,0,1}: %s (module not irreducible?)' % nu2
        row['nu2'] = str(nu2)
        return row
    row['nu2'] = int(nu2)
    # C5 explicit reality operators (J(v)=B vbar): gamma_a B = B gamma_a^bar
    Bs = []
    for mask in range(1 << D):
        B = gam[mask]
        good = True
        for a in range(D):
            lhs = mmul(Mons[a], B)
            rhs = mmul(B, mconj(Mons[a]))
            if lhs != rhs:
                good = False; break
        if good:
            Bs.append(B)
    row['monomial_B_count'] = len(Bs)
    # self-conjugacy channel agreement:
    selfconj_nu2 = (nu2 != 0)
    if selfconj_nu2 != (len(Bs) > 0):
        row['channel_agreement'] = 'DISAGREE nu2=%s Bcount=%d' % (nu2, len(Bs))
        row['abort'] = 'C4/C5 self-conjugacy disagreement'
        return row
    row['channel_agreement'] = 'OK'
    # BBbar sign per B vs nu2
    signs = set()
    for B in Bs:
        bb = mmul(B, mconj(B))
        sc = scalar_of(bb, n)
        if sc is None or sc[1] != 0 or sc[0] not in (1, -1):
            row['abort'] = 'BBbar not real scalar'
            return row
        signs.add(sc[0])
    row['BBbar_signs'] = sorted(signs)
    expected_sign = +1 if nu2 == 1 else (-1 if nu2 == -1 else None)
    if expected_sign is not None and signs != {expected_sign}:
        row['abort'] = 'sign vs nu2 mismatch: signs=%s nu2=%s' % (sorted(signs), nu2)
        return row
    verdict = {1: 'REAL', -1: 'COMPLEX' if False else 'QUATERNION', 0: 'COMPLEX'}[int(nu2)]
    if nu2 == -1 and Bs:
        verdict = 'QUATERNION'
    elif nu2 == 0:
        verdict = 'COMPLEX'
    else:
        verdict = 'REAL'
    row['type'] = verdict
    # C2 Omega^2 / Gamma, C6 chirality
    if D % 2 == 0:
        Om = eye_mat(n)
        for g in G:
            Om = matmul(Om, g)
        s2 = matmul(Om, Om)
        z = s2[0][0]
        w2 = 1 if z == ONE else (-1 if z == MONE else 0)
        scal_ok = all(s2[i][j] == (z if i == j else ZERO) for i in range(n) for j in range(n))
        f2 = (-1)**(D*(D-1)//2) * (-1)**t
        row['omega2'], row['omega2_formula'] = w2, f2
        row['weyl_halves'] = True
        if not scal_ok or w2 != f2:
            row['abort'] = 'omega2 channel fail'
            return row
        Gamma = gam[(1 << D) - 1]
        if w2 == -1:
            iM = Mon(0, [IIM]*n)
            Gamma = mmul(iM, Gamma)
        # chirality action per B
        pres = swap = neither = 0
        for B in Bs:
            c1 = mmul(B, Gamma); c2 = mmul(Gamma, B)
            if c1 == c2: pres += 1
            elif c1 == Mon(c2.f, [cneg(x) for x in c2.v]): swap += 1
            else: neither += 1
        row['B_preserve_count'], row['B_swap_count'] = pres, swap
        if neither:
            row['abort'] = 'B neither preserves nor swaps chirality (reducible module?)'
            return row
        if nu2 == 1:
            row['MW_possible'] = bool(pres > 0)
        else:
            row['MW_possible'] = False
        row['sMW_possible'] = bool(nu2 == -1 and pres > 0)
    else:
        row['weyl_halves'] = False
    return row

ANCHORS = [
    (1, 1, 'REAL', True), (1, 2, 'REAL', None), (1, 3, 'REAL', False),
    (1, 5, 'QUATERNION', False), (2, 4, 'REAL', None), (4, 0, 'QUATERNION', None),
    (5, 1, 'QUATERNION', None), (3, 0, 'QUATERNION', None), (1, 0, 'COMPLEX', None),
]

rows = []
sigs = [(t, r) for t in range(0, 13) for r in range(0, 13 - t) if t + r >= 1]
for t, r in sigs:
    try:
        x = analyze(t, r)
    except Exception as e:
        x = {'t': t, 'r': r, 'abort': repr(e)}
    rows.append(x)
    print(json.dumps(x, ensure_ascii=False, sort_keys=True), flush=True)

bytr = {(x['t'], x['r']): x for x in rows}
fails = []
for (t, r, tp, mw) in ANCHORS:
    x = bytr.get((t, r), {})
    got = x.get('type', 'ABSENT(%s)' % x.get('abort'))
    ok = got == tp
    if mw is not None and x.get('weyl_halves'):
        ok = ok and (x.get('MW_possible') == mw)
    if not ok: fails.append([t, r, tp, mw, got, x.get('MW_possible')])
    print('ANCHOR (%d,%d) expect %-12s got %-12s %s' % (t, r, tp, got, 'PASS' if ok else 'FAIL'), flush=True)

ab = [(x['t'], x['r'], x['abort']) for x in rows if 'abort' in x]

# C8 control (derived, not hand-typed): the type must be a FUNCTION of
# s = (r - t) mod 8 over the whole sweep; any class collision is a defect.
law = {}
law_viol = []
for x in rows:
    tp = x.get('type')
    if tp is None:
        continue
    k = (x['r'] - x['t']) % 8
    if k in law and law[k] != tp:
        law_viol.append([k, x['t'], x['r'], law[k], tp])
    law[k] = tp
law_ok = (not law_viol) and len(law) == 8
# MW/sMW (even D) must likewise be a function of the same class:
law2 = {}
law2_viol = []
for x in rows:
    if x.get('type') is None or x['D'] % 2:
        continue
    k = (x['r'] - x['t']) % 8
    v = (bool(x.get('MW_possible')), bool(x.get('sMW_possible')))
    if k in law2 and law2[k] != v:
        law2_viol.append([k, x['t'], x['r'], list(law2[k]), list(v)])
    law2[k] = v
law2_ok = (not law2_viol) and len(law2) == 4
# C1 mutant: sabotaged construction must trip the Clifford gate:
try:
    analyze(1, 3, sab=True)
    mutant_ok = False
    mutant_note = 'sabotage NOT detected'
except RuntimeError as e:
    mutant_ok = 'clifford fail' in repr(e)
    mutant_note = repr(e)[:120]
print('C8 law type(s) =', json.dumps({k: law[k] for k in sorted(law)}))
print('C8 violations:', law_viol, 'even-D MW/sMW law:',
      json.dumps({k: list(law2[k]) for k in sorted(law2)}), law2_viol)
print('C8 law_ok=%s law2_ok=%s | C1 mutant_ok=%s (%s)' % (law_ok, law2_ok, mutant_ok, mutant_note))

out = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, '数据', '旋量现实性_纯精确单项式引擎机检表_2026-10-18.json'))
with open(out, 'w', encoding='utf-8') as f:
    json.dump({'max_D': 12, 'anchors': ANCHORS, 'anchor_fails': fails,
               'aborts': ab, 'controls': {
                   'C8_type_law_by_r_minus_t_mod8': {str(k): law[k] for k in sorted(law)},
                   'C8_violations': law_viol, 'C8_law_ok': law_ok,
                   'C8_evenD_MW_sMW_law': {str(k): list(law2[k]) for k in sorted(law2)},
                   'C8_law2_violations': law2_viol, 'C8_law2_ok': law2_ok,
                   'C1_mutant_ok': mutant_ok, 'C1_mutant_note': mutant_note},
               'rows': rows}, f, ensure_ascii=False, indent=1)
print('wrote %s rows=%d anchor_fails=%d aborts=%d' % (out, len(rows), len(fails), len(ab)))
sys.exit(1 if (fails or ab or not (law_ok and law2_ok and mutant_ok)) else 0)
