"""Reproducible results, scans, mpmath cross-checks and standalone plots."""
import csv,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import simpson
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa
from .torus_loop import TorusLoop,C
from .dimension_audit import generate

BASE=Path(__file__).resolve().parents[1]

def safe_write(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def verify_highprecision(loop):
    mp.mp.dps=85
    R=mp.mpf(str(loop.R));a=mp.mpf(str(loop.a));m=loop.m;n=loop.n
    P=2*mp.pi/math.gcd(m,n)
    sigma=lambda x:mp.sqrt((a*n)**2 + (m*(R+a*mp.cos(n*x)))**2)
    length=mp.quad(sigma,[P*j/12 for j in range(13)])
    B=mp.mpf('.001')
    flux_int=mp.quad(lambda x:B*m*(R+a*mp.cos(n*x))**2/2,[P*j/12 for j in range(13)])
    flux_exact=mp.pi*B*(m//math.gcd(m,n))*(R**2+a**2/2)
    raw={
      'precision_dps':mp.mp.dps,'arc_length_m_mpmath':mp.nstr(length,82),
      'arc_length_m_scipy':format(loop.arc_length(),'.17g'),
      'relative_difference_scipy_mpmath':mp.nstr(abs((mp.mpf(loop.arc_length())-length)/length),15),
      'magnetic_flux_Wb_mpmath_integral':mp.nstr(flux_int,82),
      'magnetic_flux_Wb_analytic':mp.nstr(flux_exact,82),
      'relative_flux_difference':mp.nstr(abs(flux_int-flux_exact)/abs(flux_exact),12),
      'physical_interpretation':'Independent numeric cross-check only; not experimental observation',
    }
    assert abs((mp.mpf(loop.arc_length())-length)/length)<mp.mpf('1e-12')
    assert abs(flux_int-flux_exact)<mp.mpf('1e-75')
    return raw

def plots(loop):
    output=BASE/'figures';output.mkdir(exist_ok=True)
    u=np.linspace(0,loop.primitive_period,2500)
    xyz=loop.pos(u);rho=loop.R+loop.a*np.cos(loop.n*u)
    fig=plt.figure(figsize=(9,7),dpi=155)
    ax=fig.add_subplot(111,projection='3d')
    for i in range(len(u)-1):
        ax.plot(xyz[i:i+2,0]*1e3,xyz[i:i+2,1]*1e3,xyz[i:i+2,2]*1e3,
                color=plt.cm.viridis((rho[i]-(loop.R-loop.a))/(2*loop.a)),lw=2)
    ax.scatter(*[v*1e3 for v in xyz[0]],c='crimson',s=50,label='Closed-loop start/end')
    ax.set(xlabel='X (mm)',ylabel='Y (mm)',zlabel='Z (mm)',title='Toroidal spiral: outward / inward closed loop (m=2, n=3)')
    ax.set_box_aspect([1,1,.6]); ax.view_init(elev=24,azim=-53)
    fig.tight_layout();fig.savefig(output/'torus_knot_3D_THEORY.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.5),dpi=155)
    ax.plot(u/(2*np.pi),rho*1e3,label='cylindrical radius (mm)')
    ax.axhline((loop.R+loop.a)*1e3,ls='--',lw=.8,c='gray');ax.axhline((loop.R-loop.a)*1e3,ls='--',lw=.8,c='gray')
    ax.set(xlabel='u / 2π (primitive parameter period)',ylabel='radius (mm)',title='Three inward/outward cycles in one spatial loop')
    ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(output/'radial_breathing_THEORY.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.5),dpi=155)
    k=loop.curvature(u);tau=loop.torsion(u)
    ax.plot(u/(2*np.pi),k,label='curvature κ (1/m)');ax.plot(u/(2*np.pi),tau,label='signed torsion τ (1/m)',alpha=.8)
    ax.set(xlabel='u / 2π',ylabel='geometry (1/m)',title='Curvature and torsion are not constant for a closed toroidal spiral')
    ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(output/'curvature_torsion_THEORY.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.5),dpi=155)
    for beta,label in [(.8,'massive electron example, β=0.8'),(1.,'light-speed geometric parametrization, β=1')]:
        vr,vt,vz,omega,vp=loop.speed_components(u,beta)
        ax.plot(u/(2*np.pi),omega/1e9,label=label)
    ax.set(xlabel='u / 2π',ylabel='azimuthal angular velocity (10⁹ rad/s)',title='Constant total speed demands varying angular velocity')
    ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(output/'omega_inner_outer_THEORY.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.5),dpi=155)
    betas=np.linspace(.05,.98,50)
    forces=[];Bs=[]
    for beta in betas:
        f,b=loop.relativistic_inverse_force(0,beta)
        forces.append(f);Bs.append(b)
    ax.plot(betas,Bs,label='Local B needed at u=0 (ideal inverse problem)')
    ax.set(xlabel='β = v/c (massive particle, β<1)',ylabel='Local B_min (T)',title='Magnetic inverse-force scaling; NOT a global Maxwell field design')
    ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(output/'inverse_B_vs_beta_THEORY.png');plt.close(fig)

def scan(loop):
    with (BASE/'data'/'PHASE_SCAN_THEORY.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(['u_rad','time_s_beta_0_8','rho_m','z_m','kappa_inv_m','torsion_inv_m','omega_rad_s_beta_0_8','radial_v_m_s','azimuth_v_m_s','z_v_m_s','F_electron_N','Bmin_local_T','record_type'])
        grid,t=loop.time_map(beta=.8,N=4001)
        for j,u in enumerate(grid):
            vr,vt,vz,omega,vp=loop.speed_components(u,beta=.8)
            force,Bmin=loop.relativistic_inverse_force(u,beta=.8)
            w.writerow([f'{u:.16g}',f'{t[j]:.16g}',f'{loop.R+loop.a*np.cos(loop.n*u):.16g}',f'{loop.a*np.sin(loop.n*u):.16g}',f'{loop.curvature(u):.16g}',f'{loop.torsion(u):.16g}',f'{omega:.16g}',f'{vr:.16g}',f'{vt:.16g}',f'{vz:.16g}',f'{force:.16g}',f'{Bmin:.16g}','SYNTHETIC_THEORY'])
    with (BASE/'data'/'PARAMETER_SWEEP_THEORY.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['R_m','a_m','m','n','arc_length_m','total_curvature','total_signed_torsion','kappa_min_inv_m','kappa_max_inv_m','closure_error_m','record_type'])
        for m,n in [(1,2),(2,3),(2,5),(3,4),(4,6)]:
            for a_R in [.05,.1,.2,.3,.5,.7]:
                x=TorusLoop(loop.R,loop.R*a_R,m,n); grid=np.linspace(0,x.primitive_period,1001)
                err=float(np.linalg.norm(x.pos(0)-x.pos(x.primitive_period)))
                k=x.curvature(grid)
                w.writerow([x.R,x.a,m,n,x.arc_length(),x.total_curvature(),x.signed_total_torsion(),np.min(k),np.max(k),err,'SYNTHETIC_THEORY'])

def main():
    (BASE/'data').mkdir(exist_ok=True);(BASE/'results').mkdir(exist_ok=True)
    loop=TorusLoop()
    summary=loop.summary(beta=.8,B=.001)
    safe_write(BASE/'results'/'NUMERICAL_SUMMARY_THEORY.json',summary)
    high=verify_highprecision(loop);safe_write(BASE/'results'/'HIGH_PRECISION_INDEPENDENT_AUDIT.json',high)
    dims=generate(BASE/'results');safe_write(BASE/'results'/'DIMENSION_SUMMARY.json',dims)
    scan(loop);plots(loop)
    print(json.dumps({'summary':summary,'dimension':dims,'highprecision':{k:high[k] for k in ['precision_dps','relative_difference_scipy_mpmath','relative_flux_difference']}},indent=2,ensure_ascii=False))
    return {'summary':summary,'dimension':dims,'highprecision':high}

if __name__=='__main__': main()
