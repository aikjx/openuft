"""V84 drift-resistant ABBA, sham subtraction and weighted linear inference."""
from __future__ import annotations
from math import sqrt,isfinite
from statistics import mean, stdev
from .physics import common_amplitude,yukawa_amplitude_per_alpha,Rig


def abba_amplitude(block):
    if len(block)!=4 or [int(x['p']) for x in block] not in ([1,-1,-1,1],[-1,1,1,-1]):
        raise ValueError('exact four ABBA/BAAB records required')
    return sum(int(x['p'])*float(x['common_m_s2']) for x in block)/4


def estimate_records(rows):
    if not rows or len(rows)%4: raise ValueError('complete ABBA blocks needed')
    vals=[abba_amplitude(rows[i:i+4]) for i in range(0,len(rows),4)]
    return {'mean':mean(vals),'sem':stdev(vals)/sqrt(len(vals)) if len(vals)>1 else float('nan'),
            'blocks':len(vals),'block_values':vals}


def corrected(real_rows,sham_rows):
    r=estimate_records(real_rows);s=estimate_records(sham_rows)
    return {'signal':r['mean']-s['mean'],'sem':sqrt(r['sem']**2+s['sem']**2),
            'real_odd':r['mean'],'sham_odd':s['mean'],'blocks':r['blocks']}


def solve_linear(matrix,rhs):
    """Pivoted Gauss-Jordan, small matrices, standard library only."""
    n=len(rhs)
    if n==0 or len(matrix)!=n or any(len(row)!=n for row in matrix):raise ValueError('square matrix expected')
    a=[list(map(float,row))+[float(rhs[i])] for i,row in enumerate(matrix)]
    for col in range(n):
        pivot=max(range(col,n),key=lambda i:abs(a[i][col]))
        if abs(a[pivot][col])<1e-14:raise ValueError('singular or near-degenerate experiment design')
        a[col],a[pivot]=a[pivot],a[col]
        v=a[col][col]
        a[col]=[x/v for x in a[col]]
        for row in range(n):
            if row==col:continue
            k=a[row][col]
            a[row]=[x-k*y for x,y in zip(a[row],a[col])]
    return [row[-1] for row in a]


def fit_three_parameter(rig:Rig,distance_and_signal:list,lam:float):
    """WLS y=beta*C_N + alpha*C_Y + intercept; reference scale 1e-8 m/s².
    Inference beta=G_effective/G_reference is a fit with a calibrated mass, NOT a prediction of G.
    """
    if len(distance_and_signal)<4:raise ValueError('need at least four distances')
    matrix=[]; ys=[]; ws=[];scale=1e-8
    for rec in distance_and_signal:
        d=float(rec['distance_m']);y=float(rec['signal']);se=float(rec['sem'])
        if not (se>0 and all(isfinite(v) for v in (d,y,se))): raise ValueError('finite positive errors required')
        matrix.append([common_amplitude(rig,d)/scale,yukawa_amplitude_per_alpha(rig,d,lam)/scale,1.])
        ys.append(y/scale);ws.append((scale/se)**2)
    gram=[[sum(w*row[i]*row[j] for w,row in zip(ws,matrix)) for j in range(3)] for i in range(3)]
    rhs=[sum(w*row[i]*v for w,row,v in zip(ws,matrix,ys)) for i in range(3)]
    coeff=solve_linear(gram,rhs)
    inv_cols=[solve_linear(gram,[1. if j==i else 0. for j in range(3)]) for i in range(3)]
    errs=[sqrt(max(0.,inv_cols[i][i])) for i in range(3)]
    res=[v-sum(a*b for a,b in zip(row,coeff)) for row,v in zip(matrix,ys)]
    chisq=sum(w*z*z for w,z in zip(ws,res))
    return {'beta_G_ratio':coeff[0], 'alpha_yukawa':coeff[1], 'offset_m_s2':coeff[2]*scale,
            'beta_se':errs[0],'alpha_se':errs[1],'offset_se_m_s2':errs[2]*scale,
            'chi_square':chisq,'dof':len(distance_and_signal)-3,
            'distance_count':len(distance_and_signal),
            'status':'SYNTHETIC_FIT_NOT_PHYSICAL_DISCOVERY'}


def estimate_two_parameter(rig:Rig,measurements:list):
    """Fits C(d)=beta*N(d)+offset; weak model with no fifth force assumed."""
    x=[common_amplitude(rig,t['distance_m'])/1e-8 for t in measurements]
    y=[t['signal']/1e-8 for t in measurements]
    w=[(1e-8/t['sem'])**2 for t in measurements]
    sw=sum(w);sx=sum(a*b for a,b in zip(w,x));sy=sum(a*b for a,b in zip(w,y))
    sxx=sum(a*b*b for a,b in zip(w,x));sxy=sum(a*b*c for a,b,c in zip(w,x,y))
    det=sw*sxx-sx*sx
    if det<=0:raise ValueError('not identifiable')
    beta=(sw*sxy-sx*sy)/det; offset=(sxx*sy-sx*sxy)/det
    return {'beta_G_ratio':beta,'beta_se':sqrt(sw/det), 'offset_m_s2':offset*1e-8}
