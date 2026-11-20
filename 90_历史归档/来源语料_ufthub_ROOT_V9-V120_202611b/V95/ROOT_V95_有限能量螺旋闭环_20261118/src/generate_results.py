from pathlib import Path
from finite_tube import TubeModel
from symbolic_audit import checks
from dimension_audit import audit
import sys,json,csv,math,hashlib,zipfile
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.constants import mu_0
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'; FIG=ROOT/'figures'
RES.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)

def mpmath_check(dps=65):
    mp.mp.dps=dps
    RR=mp.mpf('0.010'); aa=mp.mpf('0.002'); m=2; n=3
    pi=mp.pi
    def vals(u):
        co=mp.cos(m*u); si=mp.sin(m*u)
        cn=mp.cos(n*u); sn=mp.sin(n*u)
        rho=RR+aa*cn; rp=-aa*n*sn; rpp=-aa*n*n*cn
        d=mp.matrix([rp*co-m*rho*si,rp*si+m*rho*co,aa*n*cn])
        d2=mp.matrix([(rpp-m*m*rho)*co-2*m*rp*si,(rpp-m*m*rho)*si+2*m*rp*co,-aa*n*n*sn])
        sig=mp.sqrt(sum(x*x for x in d))
        dot=sum(d[i]*d2[i] for i in range(3))
        K=[d2[i]/sig**2-d[i]*dot/sig**4 for i in range(3)]
        return sig,sig*sum(x*x for x in K)
    sections=[mp.mpf(j)*pi/6 for j in range(13)]
    L=mp.fsum(mp.quad(lambda u:vals(u)[0], [sections[j],sections[j+1]]) for j in range(12))
    K2=mp.fsum(mp.quad(lambda u:vals(u)[1], [sections[j],sections[j+1]]) for j in range(12))
    return {'digits':dps,'length_m':mp.nstr(L,60),'integral_kappa2_ds':mp.nstr(K2,60)}

def make_figures(model,energies):
    u=np.linspace(0,2*np.pi,1800)
    X,T,K,B0,spd,kap=model.geometry(u)
    plt.figure(figsize=(8,6))
    ax=plt.axes(projection='3d')
    ax.plot(X[:,0]*1000,X[:,1]*1000,X[:,2]*1000,lw=1.6)
    ax.set_xlabel('x (mm)');ax.set_ylabel('y (mm)');ax.set_zlabel('z (mm)')
    ax.set_title('Prescribed torus-knot trajectory (2,3), not an observed orbit')
    plt.tight_layout();plt.savefig(FIG/'01_prescribed_trajectory_THEORY.png',dpi=150);plt.close()
    plt.figure(figsize=(7.6,4.4))
    plt.plot(u,np.linalg.norm(B0,axis=1))
    plt.xlabel('u (dimensionless)');plt.ylabel('Required B on orbit (tesla)')
    plt.title('Compact static Maxwell field: on-curve magnitude')
    plt.grid(alpha=.2);plt.tight_layout();plt.savefig(FIG/'02_orbit_field_THEORY.png',dpi=145);plt.close()
    plt.figure(figsize=(7.6,4.4))
    x=[z['radius_m']*1000 for z in energies];y=[z['energy_J'] for z in energies]
    plt.plot(x,y,'o-',label='Gauss-Legendre volume integral')
    plt.plot(x,[y[0]*(xx/x[0])**2 for xx in x],'--',label='reference ε² scaling')
    plt.xlabel('Tube radius ε (mm)');plt.ylabel('Magnetic energy (joule)')
    plt.title('Energy–tube-width tradeoff for ideal current source')
    plt.legend();plt.grid(alpha=.2);plt.tight_layout();plt.savefig(FIG/'03_field_energy_scaling_THEORY.png',dpi=145);plt.close()
    plt.figure(figsize=(7.6,4.4))
    eps=model.eps
    X,T,K,B0,_,_=model.geometry(1.0);N=K/np.linalg.norm(K)
    radii=np.linspace(0,1.2*eps,240)
    bs=np.array([np.linalg.norm(model.field(X+rr*N)) for rr in radii])
    plt.plot(radii/eps,bs)
    plt.xlabel('Offset / ε');plt.ylabel('B (tesla)')
    plt.title('Compact support across cross-section (one radial direction)')
    plt.grid(alpha=.2);plt.tight_layout();plt.savefig(FIG/'04_cross_section_compact_support_THEORY.png',dpi=145);plt.close()


def main():
    model=TubeModel(eps=.0003)
    summary={key:float(val) for key,val in model.length_integrals(nodes=384).items()}
    benergy=[]
    for eps in [.00015,.0002,.00025,.0003,.0004,.0005,.0006]:
        mm=TubeModel(eps=eps,samples=1500)
        U=mm.energy(nu=180,nr=30,nphi=48)
        U_ind=mm.energy(nu=96,nr=22,nphi=32)
        benergy.append(dict(radius_m=eps,energy_J=U,energy_independent_mesh_J=U_ind,
                            relative_mesh_disagreement=abs(U-U_ind)/U,
                            scaled_energy_J_per_m2=U/eps**2))
    summary.update({'eps_m':model.eps,'magnetic_field_energy_J':benergy[3]['energy_J'],
         'field_energy_to_particle_kinetic_ratio':benergy[3]['energy_J']/summary['kinetic_j']})
    summary['trajectory_exact']=model.trajectory()
    summary['trajectory_2micron_perturbation']=model.trajectory([2e-6,0,0])
    c_err=[];div_err=[]
    for u in [0,.3,.8,1.6,2.4,3.3,5.2]:
        X,T,K,B0,*_=model.geometry(u);N=K/np.linalg.norm(K);H=np.cross(T,N)
        x=X+.33*model.eps*(.6*N+.8*H)
        B=model.field(x);Bn=model.curl_potential_numeric(x,h=9e-8)
        c_err.append(float(np.linalg.norm(B-Bn)/np.linalg.norm(B)))
        div_err.append(float(abs(model.divergence_B_numeric(x,h=9e-8))))
    summary['finite_difference_curl_max_relerr']=max(c_err)
    summary['finite_difference_divB_max_abs_T_per_m']=max(div_err)
    summary['symbolic_checks']=checks()
    summary['dimension_checks']=dict(total=len(audit()),pass_count=sum(row['pass'] for row in audit()),failures=[r['equation'] for r in audit() if not r['pass']])
    summary['high_precision']=mpmath_check(65)
    summary['precision_length_relative_disagreement']=float(abs((mp.mpf(summary['high_precision']['length_m'])-mp.mpf(summary['length_m']))/mp.mpf(summary['high_precision']['length_m'])))
    (RES/'V95_NUMERICAL_SUMMARY_THEORY.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    (RES/'FIELD_ENERGY_VS_TUBE_RADIUS_THEORY.csv').write_text('radius_m,energy_J,independent_mesh_J,relative_mesh_disagreement,energy_J_per_radius_m_squared\n'+''.join(','.join(str(row[x]) for x in ['radius_m','energy_J','energy_independent_mesh_J','relative_mesh_disagreement','scaled_energy_J_per_m2'])+'\n' for row in benergy),encoding='utf-8')
    with open(RES/'DIMENSION_AUDIT.csv','w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['equation','lhs','rhs','pass']);w.writeheader();w.writerows(audit())
    make_figures(model,benergy)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['symbolic_checks','high_precision']},indent=2,ensure_ascii=False))

if __name__=='__main__':main()
