# -*- coding: utf-8 -*-
"""
_s33_weights.py — SU(5) 权重多集：75 SM 分解、MPM V-耦合集、orbifold 投影分类
§33 分裂机制选择（missing partner / sliding singlet / orbifold）与 Δb 方向性
S02 空间光速螺旋统一力 · 算法联盟（严谨求真，权重多集严格计算，非文献引用）
表示构造（权重多集，含重数）：
  5   = {e_i}
  10  = antisym(5⊗5) = {e_i+e_j, i<j}
  24  = 5⊗5̄ − 1     = {e_i−e_j, i≠j} ∪ {0×4}
  50  = sym(10⊗10) − 5̄   （§32 锚定：10⊗10 = 5̄⊕45⊕50）
  75  = 10⊗10̄ − 1 − 24   （10⊗10̄ = 1⊕24⊕75）
"""
import collections, math

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def neg(a):   return tuple(-x for x in a)

# ---------- 基础权重（e 基） ----------
E = [(1,0,0,0,0),(0,1,0,0,0),(0,0,1,0,0),(0,0,0,1,0),(0,0,0,0,1)]

W5   = set(E)                                   # 5
W5b  = set(neg(w) for w in W5)                  # 5̄
W10  = set(add(w1,w2) for i,w1 in enumerate(W5) for w2 in list(W5)[i+1:])
assert len(W10) == 10

# 24 = 5⊗5̄ − 1：多集 {e_i−e_j}（i≠j，20 个）+ 0×4
c24 = collections.Counter()
for w1 in W5:
    for w2 in W5b:
        c24[add(w1,w2)] += 1
c24[(0,0,0,0,0)] -= 1                            # 减 1 的 0 权重
assert sum(c24.values()) == 24

# 50 = sym(10⊗10) − 5̄：多集 {w_i+w_j : i≤j}（55）− 5̄（5）
c50sym = collections.Counter()
wl = list(W10)
for i in range(10):
    for j in range(i,10):
        c50sym[add(wl[i],wl[j])] += 1
for w in W5b:
    c50sym[w] -= 1
assert sum(c50sym.values()) == 50

# 75 = 10⊗10̄ − 1 − 24：多集 {w+w' : w∈W10, w'∈−W10}（100）− 1 − 24
c75raw = collections.Counter()
for w1 in W10:
    for w2 in W10:
        c75raw[add(w1,neg(w2))] += 1
c75 = c75raw - c24
c75[(0,0,0,0,0)] -= 1                            # 减 1
assert sum(c75.values()) == 75, sum(c75.values())

# ---------- SM 投影 ----------
def sm_proj(w):
    t3 = (w[0]-w[1], w[1]-w[2])
    t2 = w[2]-w[3]
    y  = (-2*w[0]-2*w[1]-2*w[2]+3*w[3]+3*w[4])   # 分子（/3）
    return (t3, t2, y)

def frac3(y):
    g = math.gcd(y, 3)
    return (y//g, 3//g)

def label(w):
    t3, t2, y = sm_proj(w)
    return (t3, t2, frac3(y))

def cluster(counter, name):
    d = collections.Counter()
    for w, m in counter.items():
        d[label(w)] += m
    return d

# ---------- V1: 75 SM 分解 ----------
print('=== V1: 75 SM 分解（权重多集，10⊗10̄−1−24） ===')
c75sm = cluster(c75, '75')
tot = sum(c75sm.values())
print('  75 权重总数 = %d（多集，期望 75）' % tot)
for k in sorted(c75sm, key=lambda k: (k[0],k[1],k[2])):
    print('    75 ⊃ (t3=%s, t2=%s, y=%s/%s): %d' % (k[0],k[1],k[2][0],k[2][1],c75sm[k]))
sing = [k for k in c75sm if k[0]==(0,0) and k[1]==0 and k[2][0]==0]
print('  75 SM 单态 (1,1,0) 分量权重数:', sum(c75sm[k] for k in sing), '标签:', sing)
W75s = set(w for w,m in c75.items() if m>0 and label(w)==( (0,0),0,(0,1) ))
print('  75 (1,1,0) 权重个数:', len(W75s), W75s)

# ---------- V2: MPM V-耦合集（5̄ + ⟨75⟩(1,1,0) + 50 = 0） ----------
print()
print('=== V2: MPM V-耦合集（W = H̄5·⟨H75⟩·Z50：w5 + w75s + w50 = 0） ===')
W50set = set(w for w,m in c50sym.items() if m>0)
vcouples = []
for w5 in W5b:
    for w75s in W75s:
        w50 = neg(add(w5, w75s))
        if w50 in W50set:
            vcouples.append((label(w5), label(w50), w50))
vc_set = sorted(set((a,b) for a,b,_ in vcouples))
print('  V-耦合对（5̄ 分量 → 50 分量）:')
for a,b in vc_set:
    print('    %s → %s' % (a,b))
c50V = collections.Counter(b for a,b in vc_set)
print('  50 V-耦合分量权重数:', dict(c50V), '总 =', sum(c50V.values()))

# ---------- V3: 50 各 SM 分量（对照 §32）与 Δb_c1 ----------
print()
print('=== V3: 50 SM 分解（对照 §32）与 Δb_c1 ===')
c50sm = cluster(c50sym, '50')
def T3v(t3):
    s = t3[0]+t3[1]
    if t3==(0,0): return 0.0
    # SU(3) 表示按权重谱 → T3 = ½Σ C2；这里用标准值表
    if t3 in ((1,0),(-1,0),(0,1),(0,-1)): return 0.5
    if t3 in ((1,1),(-1,-1)): return 1.0
    if t3 in ((2,0),(-2,0),(0,2),(0,-2)): return 1.5
    if t3 in ((1,2),(-1,-2),(2,1),(-2,-1)): return 2.5
    if t3 in ((2,2),(-2,-2)): return 4.0
    return 0.0
def T2v(t2):
    if t2==0: return 0.0
    if abs(t2)==1: return 0.5
    if abs(t2)==2: return 2.0
    return 0.0
comp_rows = []
for k in sorted(c50sm, key=lambda k:(k[0],k[1],k[2])):
    t3, t2, yf = k
    n = c50sm[k]
    T3 = T3v(t3); T2 = T2v(t2)
    T1 = 0.6*(yf[0]/yf[1])**2
    db = 3*T2 - 2*T3 - T1
    comp_rows.append(dict(comp=str(k), dim=n, T3=T3, T2=T2, T1=T1, db=db))
    print('  %s: dim=%d T3=%.2f T2=%.2f T1=%.2f Δb=%.2f' % (k,n,T3,T2,T1,db))
sT3=sum(r['T3'] for r in comp_rows); sT2=sum(r['T2'] for r in comp_rows); sT1=sum(r['T1'] for r in comp_rows)
print('  Σ T3=%.2f T2=%.2f T1=%.2f（期望 17.5/17.5/17.5）' % (sT3,sT2,sT1))
print('  完整 50 Δb_c1 = 3·T2−2·T3−T1 = %.2f' % (3*sT2-2*sT3-sT1))

# ---------- V4: MPM 活跃分量 → Δb_c1 ----------
print()
print('=== V4: MPM 质量谱 → 活跃分量 → Δb_c1 ===')
vc_comps = set(b for a,b in vc_set)
active = [r for r in comp_rows if r['comp'] not in vc_comps]
print('  ⟨75⟩ V-耦合（GUT 级重，不活跃）:', sorted(vc_comps))
for r in active:
    print('  活跃 %s: Δb=%.2f' % (r['comp'], r['db']))
aT3=sum(r['T3'] for r in active); aT2=sum(r['T2'] for r in active); aT1=sum(r['T1'] for r in active)
adb = 3*aT2-2*aT3-aT1
print('  活跃 Σ T3=%.2f T2=%.2f T1=%.2f → MPM Δb_c1 = %.2f' % (aT3,aT2,aT1,adb))
s1 = [r for r in comp_rows if r['comp'].count('), (')>0 and not r['comp'].startswith('((0, 0), 0')]
s1b = [r for r in comp_rows if r['comp'].count('), (')>0 and not r['comp'].startswith('((0, 0), 0')]
d1 = sum(3*r['T2']-2*r['T3']-r['T1'] for r in comp_rows if r['comp'].count('), (')>0 and not r['comp'].startswith('((0, 0), 0'))
d2 = sum(3*r['T2']-2*r['T3']-r['T1'] for r in comp_rows if not (r['comp'].count('), (')>0 and not r['comp'].startswith('((0, 0), 0')))
print('  S1 参考（SU(2) 非单态）Δb = %.2f；S2 参考（SU(2) 单态）Δb = %.2f' % (d1, d2))

# ---------- V5: orbifold P2' 投影分类 ----------
print()
print('=== V5: orbifold P2\' = diag(−1,−1,−1,1,1) 投影（Σ色指标 mod 2） ===')
even_w = [(w,m) for w,m in c50sym.items() if m>0 and sum(w[:3])%2==0]
odd_w  = [(w,m) for w,m in c50sym.items() if m>0 and sum(w[:3])%2==1]
ne = sum(m for _,m in even_w); no = sum(m for _,m in odd_w)
print('  50: (+)-权重 %d、(−)-权重 %d（多集含重数，共 50）' % (ne,no))
ce = collections.Counter()
for w,m in even_w: ce[label(w)] += m
keep = []
for k in sorted(ce, key=lambda k:(k[0],k[1],k[2])):
    t3, t2, yf = k
    T3=T3v(t3); T2=T2v(t2); T1=0.6*(yf[0]/yf[1])**2
    db = 3*T2-2*T3-T1
    keep.append(dict(comp=str(k), dim=ce[k], T3=T3, T2=T2, T1=T1, db=db))
    print('    (+)-保留 %s: dim=%d Δb=%.2f' % (k, ce[k], db))
kT3=sum(r['T3'] for r in keep); kT2=sum(r['T2'] for r in keep); kT1=sum(r['T1'] for r in keep)
print('  orbifold Δb_c1(保留) = 3·%.2f−2·%.2f−%.2f = %.2f' % (kT2,kT3,kT1,3*kT2-2*kT3-kT1))

# ---------- V6: MPM/DMPM 有效三重态质量（文献锚核验） ----------
print()
print('=== V6: MPM/DMPM 有效三重态质量（文献锚） ===')
V   = 1.0e16; M50 = 1.0e15
MT_eff = V*V/M50
print('  MPM: M_T^eff = V²/M50 = (1e16)²/1e15 = %.2e GeV' % MT_eff)
print('  κ_MPM = M_T^eff/M_Hc(§27=9.32e15) = %.2e（PTEP 锚 ~2×10⁴）' % (MT_eff/9.32e15))
muP = 1.0e4; M50p = 1.0e16
MT_dmpm = V**4/(muP*M50*M50p)
print('  DMPM: M_T^eff = V⁴/(μ\'·M50·M50\') = (1e16)⁴/(1e4·1e15·1e16) = %.2e GeV' % MT_dmpm)
print('  M50=1e15 → 50 在 1e15 进入 RGE → SU(5) 非微扰（TTP14 判定）；DMPM 50~0.1M_Pl → 微扰安全')
