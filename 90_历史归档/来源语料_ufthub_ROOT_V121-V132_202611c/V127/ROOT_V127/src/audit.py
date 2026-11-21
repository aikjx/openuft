import json, math
import numpy as np
from pathlib import Path

def audit(K,C,M,k):
    K=np.array(K,float);C=np.array(C,float);M=np.array(M,float)
    ek=np.linalg.eigvalsh(K)
    if ek.min()<=0:return {'status':'ghost_or_singular_kinetic','kinetic_eigenvalues':ek.tolist()}
    w,U=np.linalg.eigh(K)
    inv=U@np.diag(1/np.sqrt(w))@U.T
    grad=inv@C@inv;mass=inv@M@inv
    speeds=np.linalg.eigvalsh(grad)
    modes=np.linalg.eigvalsh(k*k*grad+mass)
    return {'status':'evaluated','kinetic_eigenvalues':ek.tolist(),'gradient_eigenvalues':speeds.tolist(),'omega_squared':modes.tolist(),'ghost_free':True,'gradient_stable':bool(speeds.min()>=-1e-10),'no_tachyon_at_k':bool(modes.min()>=-1e-10),'principal_speeds_leq_c':bool(speeds.max()<=1+1e-10)}

def main():
    cases={
    'canonical':audit(np.eye(3),np.eye(3),np.diag([0.,1.,4.]),1),
    'kinetic_ghost':audit(np.diag([1.,-1.,1.]),np.eye(3),np.eye(3),1),
    'gradient_instability':audit(np.eye(3),np.diag([1.,-0.2,1.]),np.eye(3),3),
    'tachyon_long_wavelength':audit(np.eye(3),np.eye(3),np.diag([-1.,1.,1.]),0.1),
    'superluminal_principal_speed':audit(np.eye(3),np.diag([1.,1.2,1.]),np.eye(3),1),
    'mixed_positive':audit([[2,.2,0],[.2,1.5,.1],[0,.1,1.2]],np.eye(3),np.diag([.2,.5,1]),2),
    }
    out=Path(__file__).resolve().parents[1]/'results'/'audit.json'
    out.write_text(json.dumps(cases,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(cases,indent=2))
if __name__=='__main__':main()
