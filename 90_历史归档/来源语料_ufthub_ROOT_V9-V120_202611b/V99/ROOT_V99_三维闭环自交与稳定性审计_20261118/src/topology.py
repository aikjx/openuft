"""Polygon projection + Fox (-1) coloring determinant.

Only valid for CLOSED embedded polygons with generic projection and nonzero
height separation at every projected crossing. Never classify raw V98 immersion.
"""
from __future__ import annotations
import bisect
import numpy as np
from sympy import Matrix


def load_v98_xyz(csvfile):
    import csv
    with open(csvfile, encoding='utf-8-sig', newline='') as fp:
        rows=list(csv.DictReader(fp))
    p=np.array([[float(r['x_mm'])*1e-3,float(r['y_mm'])*1e-3,float(r['z_um'])*1e-6] for r in rows])
    return p[:-1]  # final V98 sample matches initial up to numerical integration error


def projected_crossings(points, view=(0.,0.,1.)):
    points=np.asarray(points,float)
    assert points.ndim==2 and points.shape[1]==3 and len(points)>=4
    norm=np.asarray(view,float);norm=norm/np.linalg.norm(norm)
    u=np.cross(norm,[0.,0.,1.])
    if np.linalg.norm(u)<0.05:
        u=np.cross(norm,[0.,1.,0.])
    u=u/np.linalg.norm(u);v=np.cross(norm,u)
    projected=np.stack((points@u,points@v),axis=1)
    heights=points@norm
    starts=projected
    steps=np.roll(projected,-1,axis=0)-starts
    N=len(points)
    results=[]
    def cross_2d(a,b):return a[...,0]*b[...,1]-a[...,1]*b[...,0]
    lo=np.minimum(starts,starts+steps); hi=np.maximum(starts,starts+steps)
    for i in range(N):
        eligible=np.arange(i+2,N-(i==0),dtype=int)
        if not len(eligible):continue
        mask=((lo[eligible,0]<=hi[i,0]) & (hi[eligible,0]>=lo[i,0]) &
              (lo[eligible,1]<=hi[i,1]) & (hi[eligible,1]>=lo[i,1]))
        js=eligible[mask]
        if not len(js):continue
        qi=starts[js]-starts[i]
        den=cross_2d(np.broadcast_to(steps[i],steps[js].shape), steps[js])
        good=np.abs(den)>1e-24
        js=js[good];qi=qi[good];den=den[good]
        if not len(js):continue
        t=cross_2d(qi,steps[js])/den
        w=cross_2d(qi,np.broadcast_to(steps[i],steps[js].shape))/den
        good=(t>1e-8)&(t<1-1e-8)&(w>1e-8)&(w<1-1e-8)
        js=js[good];t=t[good];w=w[good]
        for j,tt,ww in zip(js,t,w):
            z1=heights[i]*(1-tt)+heights[(i+1)%N]*tt
            z2=heights[j]*(1-ww)+heights[(j+1)%N]*ww
            results.append(dict(s1=float(i+tt),s2=float(j+ww),height_gap_m=float(z1-z2)))
    return results


def fox_determinant(points,view=(0.,0.,1.),tolerance=1e-10):
    """Integer |Delta(-1)| for confidently embedded polygon;
    raises if projection height difference is <= tolerance (m).

    A nontrivial determinant rules out the unknot; it does not uniquely
    identify a knot type. An exact/interval method is still needed for
    certification of the smooth physical path.
    """
    crossings=projected_crossings(points,view)
    if not crossings:
        return dict(crossings=0,determinant=1,min_height_gap_m=None)
    minheight=min(abs(x['height_gap_m']) for x in crossings)
    if minheight<=tolerance:
        raise ValueError(f'Degenerate / unresolved projected crossings: height gap {minheight:.3e} m')
    under=[];over={}
    for i,c in enumerate(crossings):
        if c['height_gap_m']>0: under.append((c['s2'],i));over[i]=c['s1']
        else: under.append((c['s1'],i));over[i]=c['s2']
    under.sort(); order=[u[0] for u in under]
    N=len(under)
    mat=[[0]*N for _ in range(N)]
    for k,(_,cross_id) in enumerate(under):
        over_arc=(bisect.bisect_right(order,over[cross_id])-1)%N
        mat[k][(k-1)%N]-=1
        mat[k][k]-=1
        mat[k][over_arc]+=2
    det=abs(int(Matrix(mat)[:-1,:-1].det(method='domain-ge'))) if N>1 else 1
    return dict(crossings=N,determinant=det,min_height_gap_m=float(minheight))


def lifted_polygon(points, amplitude_m=1e-7,periodic_harmonic=1):
    """A geometrical smoothing/perturbation, not a Maxwell-Lorentz orbit."""
    p=np.array(points,float,copy=True)
    s=np.arange(len(p))/len(p)
    p[:,2]+=amplitude_m*np.sin(2*np.pi*periodic_harmonic*s)
    return p


def torus_knot(p,q,count=1300):
    t=2*np.pi*np.arange(count)/count
    return np.array([ (2+.4*np.cos(q*t))*np.cos(p*t),
          (2+.4*np.cos(q*t))*np.sin(p*t), .4*np.sin(q*t)]).T
