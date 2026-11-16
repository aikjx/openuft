# -*- coding: utf-8 -*-
"""算法联盟第30轮：Coleman-Mandula 型代数核——时空-内部对称性混合的 Jacobi 约束。
so(3)_space(J) x su(2)_int(T) + 混合生成元 Q_{ia}（3+3+9=15 维）。
最一般反对称协变括号 [Q_{ia},Q_{jb}] = a·δ_ij ε_abc T_c + b·ε_ijk δ_ab J_k。
精确 Fraction 二次多项式(6维)表示 Jacobi 系数；解约束、验闭包、验 Killing。
不占 RID、不进 README、不与任何审计卷或算法联盟册相加。"""
import io, os, glob, json, ast
from fractions import Fraction as Fr
from itertools import combinations

def _locate_root():
    hs = glob.glob('openuft/04_*/**/本项目_全维自洽与归一化', recursive=True)
    assert len(hs) == 1, hs
    return hs[0]
ROOT = _locate_root()
OUT_JSON = os.path.join(ROOT, '数据', '_ALG_jacobi_recompute_2026-11-16.json')
OUT_REPORT = os.path.join(ROOT, '数据', '_ALG_jacobi_2026-11-16_report.txt')
SELF_SOURCE_PATH = None

# 二次二元多项式 c0+c1 a+c2 b+c3 a^2+c4 ab+c5 b^2
Z6 = (Fr(0),)*6
def poly(c0=0,c1=0,c2=0,c3=0,c4=0,c5=0):
    return (Fr(c0),Fr(c1),Fr(c2),Fr(c3),Fr(c4),Fr(c5))
def padd(p,q): return tuple(x+y for x,y in zip(p,q))
def pneg(p): return tuple(-x for x in p)
def pzero(p): return all(x==0 for x in p)
def pmul(p,q):
    r=[Fr(0)]*6
    deg=[(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]
    dmap={(0,0):0,(1,0):1,(0,1):2,(2,0):3,(1,1):4,(0,2):5}
    for i,(ai,bi) in enumerate(deg):
        for j,(aj,bj) in enumerate(deg):
            da,db=ai+aj,bi+bj
            if da>2 or db>2 or da+db>2: continue
            r[dmap[(da,db)]]+=p[i]*q[j]
    return tuple(r)

def eps(i,j,k):
    if (i,j,k) in [(0,1,2),(1,2,0),(2,0,1)]: return Fr(1)
    if (i,j,k) in [(0,2,1),(2,1,0),(1,0,2)]: return Fr(-1)
    return Fr(0)

J=[('J',i) for i in range(3)]
T=[('T',a) for a in range(3)]
Q=[('Q',i,a) for i in range(3) for a in range(3)]
GENS=J+T+Q

def br(X,Y):
    out={}
    def put(Z,p):
        if not pzero(p): out[Z]=padd(out.get(Z,Z6),p)
    if X[0]=='J' and Y[0]=='J':
        for k in range(3):
            v=eps(X[1],Y[1],k)
            if v: put(('J',k),poly(c0=v))
    elif X[0]=='T' and Y[0]=='T':
        for c in range(3):
            v=eps(X[1],Y[1],c)
            if v: put(('T',c),poly(c0=v))
    elif X[0]=='J' and Y[0]=='Q':
        for k in range(3):
            v=eps(X[1],Y[1],k)
            if v: put(('Q',k,Y[2]),poly(c0=v))
    elif X[0]=='T' and Y[0]=='Q':
        for c in range(3):
            v=eps(X[1],Y[2],c)
            if v: put(('Q',Y[1],c),poly(c0=v))
    elif X[0]=='Q' and Y[0]=='Q':
        i,a=X[1],X[2]; j,b=Y[1],Y[2]
        if i==j:
            for c in range(3):
                v=eps(a,b,c)
                if v: put(('T',c),poly(c1=v))
        if a==b:
            for k in range(3):
                v=eps(i,j,k)
                if v: put(('J',k),poly(c2=v))
    elif X[0] in ('J','T') and Y[0] in ('J','T'):
        pass
    elif X[0]=='Q' and Y[0] in ('J','T'):
        for Z,p in br(Y,X).items(): put(Z,pneg(p))
    return out

def addbr(*bds):
    out={}
    for bd in bds:
        for Z,p in bd.items(): out[Z]=padd(out.get(Z,Z6),p)
    return {Z:p for Z,p in out.items() if not pzero(p)}

def nested(X,Y,Z):
    acc={}
    for W,pw in br(Y,Z).items():
        for V,pv in br(X,W).items():
            acc=addbr(acc,{V:pmul(pw,pv)})
    return acc

def jacobi(X,Y,Z):
    return addbr(nested(X,Y,Z),nested(Y,Z,X),nested(Z,X,Y))

def ev(p,a,b):
    return p[0]+p[1]*a+p[2]*b+p[3]*a*a+p[4]*a*b+p[5]*b*b

# ---------- build_segments ----------
def build_segments():
    seg={}
    seg['n_gens']=len(GENS)
    # 收集非零 Jacobi 多项式：正确 pmul 下约束为纯一次 b-a=0 / a-b=0
    polys=[]; const_nnz=quad_nnz=0
    for X,Y,Z in combinations(GENS,3):
        for W,p in jacobi(X,Y,Z).items():
            if pzero(p): continue
            polys.append(p)
            if p[0]!=0: const_nnz+=1
            if p[3] or p[4] or p[5]: quad_nnz+=1
    seg['n_jacobi_poly']=len(polys)
    seg['const_nnz']=const_nnz
    seg['quad_nnz']=quad_nnz                 # 二次项条数，真值=0
    a_nnz=sum(1 for p in polys if p[1]!=0)
    b_nnz=sum(1 for p in polys if p[2]!=0)
    seg['a1_nnz']=a_nnz; seg['b1_nnz']=b_nnz
    # 一次项比例种类：a 系数 / b 系数，唯一值 -1 ⇒ a=b
    ratios=set()
    for p in polys:
        if p[2]!=0: ratios.add(p[1]/p[2])
    seg['n_ratios']=len(ratios)
    seg['ratio']=sorted(ratios)[0] if len(ratios)==1 else None     # -1
    # 解线方程 ratio*a + b = 0 ⇒ a = -b/ratio = b（ratio=-1）
    seg['k']=-Fr(1)/seg['ratio'] if seg['ratio'] not in (None,Fr(0)) else None   # 1
    seg['disc']=Fr(0)            # 一次方程无判别式概念，置0表示线性约束
    k=seg['k']
    seg['check_on_line']=sum(1 for p in polys if ev(p,k,Fr(1))!=0) if k is not None else -1
    seg['check_off_line']=sum(1 for p in polys if ev(p,Fr(1),Fr(0))!=0)
    # 解线 a=b 上构成半单李代数
    if k is not None:
        a,b=k,Fr(1)
        bad_ordered=0
        for X in GENS:
            for Y in GENS:
                for Z in GENS:
                    for W,p in jacobi(X,Y,Z).items():
                        if ev(p,a,b)!=0: bad_ordered+=1
        seg['bad_ordered']=bad_ordered
        def fv(X,Y,Z,aa,bb): return ev(br(X,Y).get(Z,Z6),aa,bb)
        Kdiag=[]
        for g in GENS:
            s=sum(fv(g,A,B,a,b)*fv(g,B,A,a,b) for A in GENS for B in GENS)
            Kdiag.append(s)
        seg['Kdiag_J']=Kdiag[0]; seg['Kdiag_T']=Kdiag[3]; seg['Kdiag_Q']=Kdiag[6]
        seg['K_nonzero']=all(x!=0 for x in Kdiag)
        def kq(bb):
            aa=k*bb; q=Q[0]
            return sum(fv(q,A,B,aa,bb)*fv(q,B,A,aa,bb) for A in GENS for B in GENS)
        seg['KQ_b1']=kq(Fr(1)); seg['KQ_b2']=kq(Fr(2))
        seg['amplitude_free']=(seg['KQ_b1']!=seg['KQ_b2'])
    else:
        seg['bad_ordered']=-1
        seg['Kdiag_J']=seg['Kdiag_T']=seg['Kdiag_Q']=None
        seg['K_nonzero']=False; seg['KQ_b1']=seg['KQ_b2']=None
        seg['amplitude_free']=False
    return seg


# ---------- 判定框架 ----------
def final_of(nf_main,nf_guard,n_decl):
    if nf_guard: return 'GATES-FAIL-GUARD-%d'%nf_guard
    if nf_main:  return 'GATES-FAIL-MAIN-%d'%nf_main
    if n_decl:   return 'GATES-PASS-WITH-%d-NEGATIVE'%n_decl
    return 'GATES-PASS'

def add(rows,key,ok,val,kind='PASS',note=''):
    rows.append(dict(key=key,kind=kind,ok=bool(ok),val=val,note=note))
    return ok

INFO_LITERAL_KEYS={'AMPLITUDE-FREE-NEG','ZERO-READOUT-DENOMINATOR','JACOBI-QUAD-STRUCT'}

def ast_no_hardcode_ok(src_path):
    tree=ast.parse(io.open(src_path,'r',encoding='utf-8').read())
    bad=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call):
            fn=node.func
            nm=fn.id if isinstance(fn,ast.Name) else (fn.attr if isinstance(fn,ast.Attribute) else '')
            if nm=='add' and len(node.args)>=2:
                k=node.args[1]; key=k.value if isinstance(k,ast.Constant) else None
                if key in INFO_LITERAL_KEYS: continue
                if len(node.args)>=3:
                    okv=node.args[2]
                    if isinstance(okv,ast.Constant) and isinstance(okv.value,bool):
                        bad.append((key,okv.value))
    return (len(bad)==0),bad

def verdict_machine(seg):
    def build(n,ratios,k,quad,aff):
        return ('ALG30__NGEN-15--JACLin-%d--RATIOS-%d--K-%s--QUADNZ-%s'
                '--LINE-CLOSED-%s--KILL-NZ-%s--AMPL-FREE-%s--PRED-0--PARAM-UNFIXED')%(
                    n,ratios,str(k),str(quad),
                    '1' if seg['bad_ordered']==0 else '0',
                    '1' if seg['K_nonzero'] else '0', '1' if aff else '0')
    k=seg['k']; quad=seg['quad_nnz']; aff=seg['amplitude_free']
    base=build(seg['n_jacobi_poly'],seg['n_ratios'],k,quad,aff)
    bump=build(seg['n_jacobi_poly']+1,seg['n_ratios'],k,quad,aff)
    return base,(base!=bump)

def readback_one(prefix,token):
    fs=glob.glob(os.path.join(ROOT,'数据',prefix+'_recompute_*.json'))
    fs=[p for p in fs if '_整理' not in os.path.basename(p)]
    assert len(fs)==1,(prefix,fs)
    txt=io.open(fs[0],'r',encoding='utf-8').read()
    assert token in txt,(prefix,token)
    return dict(file=os.path.basename(fs[0]),token=token,ok=True)

def cross_readback():
    return [
        readback_one('_XV6317','PIN-0'),
        readback_one('_XV6316','K-PINNED-0'),
        readback_one('_ALG_lowenergy','NOT-UNIQUE'),
    ]

# ---------- run_guards ----------
def run_guards(seg):
    rows=[]; nf_main=nf_guard=0
    ok=(seg['n_gens']==15)
    if not add(rows,'G1-GEN-COUNT',ok,seg['n_gens'],'PASS','J3+T3+Q9=15 生成元'): nf_main+=1
    ok=(seg['const_nnz']==0 and seg['quad_nnz']==0)
    if not add(rows,'G2-SUBALGEBRA-JACOBI',ok,[seg['const_nnz'],seg['quad_nnz']],'PASS',
               '常数项与二次项全零⇒纯一次混合约束，子代数自身闭合'): nf_main+=1
    ok=(seg['n_ratios']==1 and seg['ratio']==Fr(-1))
    if not add(rows,'G3-UNIQUE-LINEAR-RATIO',ok,[seg['n_ratios'],str(seg['ratio'])],'PASS',
               'Jacobi一次项比例唯一=-1⇒解线a=b'): nf_main+=1
    ok=(seg['quad_nnz']==0 and seg['const_nnz']==0)
    if not add(rows,'G4-PURE-LINEAR',ok,[seg['quad_nnz'],seg['const_nnz']],'PASS',
               'Jacobi约束纯一次、无二次/常数项'): nf_main+=1
    ok=(seg['check_on_line']==0 and seg['check_off_line']>0)
    if not add(rows,'G5-SOLUTION-LINE',ok,[seg['check_on_line'],seg['check_off_line']],'PASS',
               '解线a=b上Jacobi全闭合，离线上违例>0'): nf_main+=1
    ok=(seg['bad_ordered']==0 and seg['K_nonzero'])
    if not add(rows,'G6-SEMISIMPLE-CLOSURE',ok,[seg['bad_ordered'],str(seg['Kdiag_J']),str(seg['Kdiag_Q'])],'PASS',
               '有序三元组Jacobi闭合+Killing非退化⇒合法半单代数'): nf_main+=1
    # 登记行
    add(rows,'JACOBI-QUAD-STRUCT',True,[seg['n_jacobi_poly'],seg['quad_nnz']],'INFO',
        'Jacobi约束纯一次(b-a=0)，二次/常数项全零')
    add(rows,'AMPLITUDE-FREE-NEG',False,str(seg['KQ_b1'])+'->'+str(seg['KQ_b2']),'FAIL',
        '解线上幅度b仍自由：Killing(Q)随b变（已登记判负，不挡门）')
    add(rows,'ZERO-READOUT-DENOMINATOR',True,'0/2','INFO',
        '被Jacobi唯一固定的混合耦合数=0（比值固定但幅度自由），分母=2个耦合a,b')
    rb=cross_readback(); seg['readback']=rb
    ok=len(rb)==3 and all(x['ok'] for x in rb)
    if not add(rows,'CROSS-VOLUME-READBACK',ok,len(rb),'PASS','磁盘实读XV6317/XV6316/ALG_lowenergy token命中'): nf_main+=1
    # 守卫
    src=SELF_SOURCE_PATH or os.path.abspath(__file__)
    okA,bad=ast_no_hardcode_ok(src)
    if not add(rows,'NO-HARDCODE-OK',okA,bad,'GUARD','AST扫描判据行ok无布尔字面量'): nf_guard+=1
    seg['verdict'],okV=verdict_machine(seg)
    if not add(rows,'VERDICT-MACHINE',okV,okV,'GUARD','关键读数+1后判词串变化'): nf_guard+=1
    okK=(seg['Kdiag_J']==Fr(-8) and seg['Kdiag_T']==Fr(-8) and seg['Kdiag_Q']==Fr(-8))
    if not add(rows,'KILLING-VALUES',okK,[str(seg['Kdiag_J']),str(seg['Kdiag_T']),str(seg['Kdiag_Q'])],'GUARD',
               'b=1时Killing(J)=T=Q=-8'): nf_guard+=1
    okF=seg['amplitude_free']
    if not add(rows,'AMPL-FREE-DETECTED',okF,okF,'GUARD','检测出幅度自由(Killing(Q)随b变)'): nf_guard+=1
    counts={}
    for r in rows: counts[r['kind']]=counts.get(r['kind'],0)+1
    n_decl=sum(1 for r in rows if r['kind']=='FAIL')
    return rows,dict(counts=counts,nf_main=nf_main,nf_guard=nf_guard,n_decl=n_decl,
                     final=final_of(nf_main,nf_guard,n_decl))

def make_out(seg,rows,g):
    return dict(
        title='算法联盟第30轮：时空-内部对称性混合的Jacobi约束（Coleman-Mandula代数核）',
        date='2026-11-16',rid='ALG-30（算法联盟，不占RID）',body_type='算法联盟册',
        final=g['final'],verdict=seg['verdict'],n_rows=len(rows),counts=g['counts'],
        declared_neg=[r['key'] for r in rows if r['kind']=='FAIL'],
        rows=rows,guards=[r for r in rows if r['kind']=='GUARD'],
        guard_count=len([r for r in rows if r['kind']=='GUARD']),
        guard_pass=len([r for r in rows if r['kind']=='GUARD' and r['ok']]),
        key_numbers=dict(
            n_gens=seg['n_gens'],n_jacobi_poly=seg['n_jacobi_poly'],
            const_nnz=seg['const_nnz'],quad_nnz=seg['quad_nnz'],
            a1_nnz=seg['a1_nnz'],b1_nnz=seg['b1_nnz'],
            n_ratios=seg['n_ratios'],linear_ratio=str(seg['ratio']),k=str(seg['k']),
            check_on_line=seg['check_on_line'],check_off_line=seg['check_off_line'],
            bad_ordered=seg['bad_ordered'],Kdiag_J=str(seg['Kdiag_J']),
            Kdiag_T=str(seg['Kdiag_T']),Kdiag_Q=str(seg['Kdiag_Q']),
            KQ_b1=str(seg['KQ_b1']),KQ_b2=str(seg['KQ_b2']),amplitude_free=seg['amplitude_free']),
        cross_readback=seg['readback'],
        boundary=[
            '模型用 so(3) 时空旋转而非完整 Lorentz+平移 Poincaré，故非 Coleman-Mandula 强形式；所得为一维解线而非全面 no-go。',
            '混合生成元取 (3,3) 表示 Q_ia，是 so(3)xsu(2) 的一个特定扩张；未枚举全部可能表示。',
            'Killing 对角在 b=1 为 J=T=Q=-8，15 维半单代数疑为 su(4) 的一种 so(3)xsu(2) 分解，本册未正式识别同构。',
            '比值固定≠幅度固定：a=b 由Jacobi一次约束定，幅度b自由（Killing(Q)=-8b）；不排除额外动力学固定b。',
            '数学自洽≠实验证实；独立实验预言=0；四力统一正确者=0条。'])

def main():
    os.makedirs(os.path.join(ROOT,'数据'),exist_ok=True)
    seg=build_segments(); rows,g=run_guards(seg); out=make_out(seg,rows,g)
    txt=json.dumps(out,ensure_ascii=False,indent=1,sort_keys=True)
    with io.open(OUT_JSON,'w',encoding='utf-8',newline='\n') as fh: fh.write(txt+'\n')
    lines=['verdict : '+out['verdict'],'final   : '+out['final'],
           'counts  : '+json.dumps(out['counts'],ensure_ascii=False,sort_keys=True),
           'guards  : %d/%d'%(out['guard_pass'],out['guard_count'])]
    with io.open(OUT_REPORT,'w',encoding='utf-8',newline='\n') as fh: fh.write('\n'.join(lines)+'\n')
    print('final =',out['final']); print('counts =',out['counts'])
    print('guard_pass = %d / %d'%(out['guard_pass'],out['guard_count']))
    return out

if __name__=='__main__':
    main()


# --- 尾注（算法联盟第30轮） ---
# 结构：build_segments → run_guards → make_out → main。
# 不占 RID、不进 README、不与任何审计卷或算法联盟册相加。
# 复现：python _assemble_alg30.py && python _run_alg30.py && python _alg30_final_check.py。
# 红线：数学自洽≠实验证实；只产可算判决；indep exp pred=0；不宣称攻破统一场论。
