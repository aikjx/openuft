"""Re-generate ROOT V98 numerical data, charts and self-contained visualizer."""
from pathlib import Path
from datetime import datetime, timezone
import json,csv,hashlib,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from v98_core import (shoot_3d,independent_fixed_time_orbit,boris_independent,
 vacuum_maxwell_residuals,canonical_invariant_error,classical_radiation,
 orbit_samples)
from scipy.constants import c, e, m_e
ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'results'; PLOTS=ROOT/'plots'; WEB=ROOT/'web'
for d in (RESULTS,PLOTS,WEB):d.mkdir(exist_ok=True)


def safe_json(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False,default=lambda x: x.tolist() if isinstance(x,np.ndarray) else float(x) if isinstance(x,np.generic) else str(x)),encoding='utf-8')


def main():
    convergence=[]
    solved_rows=[]
    for order in (13,17,21):
        row=shoot_3d(order=order,rtol=3e-12)
        solved_rows.append(row)
        convergence.append({
        'quadrature_order':order,'r0_m':row['r0_m'],'z_amplitude_m':row['az_m'],
        'return_pos_m':row['position_return_error_m'],
        'return_velocity_relative':row['velocity_return_error_relative'],
        'source_current_A':row['field_I_A_per_coil'],
        'solver_success':row['root_success'],'residual_verified':row['residual_verified'],'root_calls':row['root_calls']})
        print('ROOT',order,'r(mm)',row['r0_m']*1e3,'z(um)',row['az_m']*1e6,
              'closure(m)',row['position_return_error_m'],flush=True)
    row=solved_rows[-1]
    fixed=independent_fixed_time_orbit(row)
    boris=[]
    for steps in (2000,4000,8000):
        b=boris_independent(row,nsteps=steps)
        boris.append(b)
        print('BORIS',steps,'error m',b['position_difference_m'],flush=True)
    vac=[]
    for h in (16e-6,8e-6,4e-6,2e-6):
        vac.append({'difference_step_m':h,**vacuum_maxwell_residuals(row['field'],row['r0_m'],h=h)})
    canonical=canonical_invariant_error(row)
    radiated=classical_radiation(row)
    samples=orbit_samples(row,1101)
    head=['t_ns','x_mm','y_mm','z_um','radius_mm','speed_ratio']
    with (RESULTS/'3D_PERIODIC_TRAJECTORY_THEORY.csv').open('w',newline='',encoding='utf-8-sig') as ff:
        wr=csv.writer(ff);wr.writerow(head)
        for vals in zip(*(samples[h] for h in head)):
            wr.writerow([f'{float(v):.16g}' for v in vals])
    with (RESULTS/'SOURCE_CONVERGENCE_THEORY.csv').open('w',newline='',encoding='utf-8-sig') as ff:
        ww=csv.DictWriter(ff,fieldnames=list(convergence[0].keys()));ww.writeheader();ww.writerows(convergence)
    with (RESULTS/'BORIS_CROSSCHECK_THEORY.csv').open('w',newline='',encoding='utf-8-sig') as ff:
        ww=csv.DictWriter(ff,fieldnames=list(boris[0].keys()));ww.writeheader();ww.writerows(boris)
    fields={
      'classification':'THEORY_NOT_EXPERIMENT; root finding not rigorous existence proof',
      'parent':'ROOT V97, finite-cross-section two-coil source, prescribed external current',
      'conditions':{'beta':row['beta'],'initial_radial_amplitude_m':row['ar_m'],
        'initial_vertical_amplitude_m':row['az_m'], 'finite_cross_section_m':.001,
        'coil_radius_m':.01,'coil_half_separation_m':.008,
        'source_quadrature_order':21,'charge_C':-e,'electron_mass_kg':m_e},
      'orbit':{'reference_radius_m':row['r0_m'],'source_current_A_per_coil':row['field_I_A_per_coil'],
        'reference_field_T':row['reference_B_T'],'T_s':row['period_s'],
        'phi_rad':row['phi_rad'],'phi_residual_rad':row['phi_residual_rad'],
        'vz_residual':row['vz_residual_dimensionless'],
        'z_return_error_m':row['z_return_error_m'],
        'position_return_error_m':row['position_return_error_m'],
        'velocity_return_error_relative':row['velocity_return_error_relative'],
        'root_success':row['root_success'],'residual_verified':row['residual_verified'],'root_calls':row['root_calls']},
      'independent_non_event_ode':fixed,
      'independent_boris_integrations':boris,'maxwell_vacuum_residuals':vac,
      'axisymmetric_canonical_momentum':canonical,
      'classical_radiation':radiated,
      'source_quadrature_convergence':convergence,
      'limits':[
        'No rigorous existence or nonlinear all-time stability proof',
        'No finite-conductor construction, electric power, cooling or Lorentz backreaction included',
        'No radiation reaction; periodic motion in this simulation is not perpetual physical motion',
        'No knot type determined and no inference about a fundamental speed-c internal motion',
        'No four-force unification, independent G prediction or quantum gravity from this model'
      ]}
    safe_json(RESULTS/'NUMERICAL_SUMMARY_THEORY.json',fields)
    x,y,z=samples['x_mm'],samples['y_mm'],samples['z_um']*1e-3
    fig=plt.figure(figsize=(9,7)); ax=fig.add_subplot(111,projection='3d')
    ax.plot(x,y,z,lw=1.4)
    ax.scatter([x[0]],[y[0]],[z[0]],s=30)
    ax.set_xlabel('x (mm)');ax.set_ylabel('y (mm)');ax.set_zlabel('z (mm)')
    ax.set_title('ROOT V98: 3D closed orbit candidate, 5 turns (THEORY)')
    ax.set_box_aspect((1,1,.22),zoom=.92)
    fig.tight_layout();fig.savefig(PLOTS/'01_3D_ORBIT_THEORY.png',dpi=170);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,5))
    ax.plot(samples['t_ns'],(samples['radius_mm']-row['r0_m']*1e3)*1000,label='radial deviation (um)')
    ax.plot(samples['t_ns'],samples['z_um'],label='axial z (um)')
    ax.set_xlabel('time (ns)');ax.set_ylabel('displacement (um)')
    ax.set_title('3D periodic orbit: radial breathing and vertical motion (THEORY)')
    ax.grid(alpha=.25);ax.legend();fig.tight_layout()
    fig.savefig(PLOTS/'02_RADIAL_VERTICAL_THEORY.png',dpi=165);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,5))
    n=np.array([b['nsteps'] for b in boris]);error=np.array([b['position_difference_m'] for b in boris])
    ax.loglog(n,error,'o-',label='Boris fixed-time return error')
    ax.loglog(n,error[0]*(n[0]/n)**2,'--',label='N^-2 reference')
    ax.set_xlabel('Boris integration steps');ax.set_ylabel('position return error (m)')
    ax.set_title('Independent time-centered Lorentz integrator (THEORY)')
    ax.grid(alpha=.3,which='both');ax.legend();fig.tight_layout()
    fig.savefig(PLOTS/'03_BORIS_CONVERGENCE_THEORY.png',dpi=160);plt.close(fig)
    build_html(row,samples)
    print(json.dumps({'source_order':21, 'r0_mm':row['r0_m']*1e3,
       'az_um':row['az_m']*1e6,'position_return_m':row['position_return_error_m'],
       'boris_8000_m':boris[-1]['position_difference_m'],
       'canonical_max_residual':canonical['max_delta_Pphi_relative'],
       'radiation_J':radiated['energy_J_per_period']},ensure_ascii=False,indent=2))


def build_html(row,samples):
    pts=[[round(float(x),7),round(float(y),7),round(float(z),7)] for x,y,z in zip(
     samples['x_mm'][::2],samples['y_mm'][::2],samples['z_um'][::2])]
    payload=json.dumps(pts,ensure_ascii=False,separators=(',',':'))
    html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ROOT V98｜三维周期轨道离线实验室</title>
    <style>body{margin:0;background:#0c1225;color:#e8edff;font-family:system-ui,-apple-system,sans-serif}main{max-width:1120px;margin:auto;padding:22px}h1{font-size:27px}p{line-height:1.65;color:#adb9d4}.card{background:#151e36;border:1px solid #303e60;border-radius:15px;padding:16px;margin:12px 0}canvas{width:100%;height:auto;display:block;background:#090d1c;border-radius:12px}label{display:inline-block;margin:8px 12px 6px 0;font-size:14px}input{vertical-align:middle}button{background:#3556a6;color:white;border:0;border-radius:9px;padding:9px 14px;cursor:pointer}small{color:#9dacc8}.stats{display:flex;flex-wrap:wrap;gap:15px}.stats span{background:#222f50;padding:10px;border-radius:9px}</style></head><body><main>
    <h1>ROOT V98｜三维非线性闭环科研实验室</h1><p>基于有限截面双线圈的 Maxwell–Lorentz 数值轨道。仅理论模拟。并非新的四力统一或真实实验观测。</p>
    <div class="card stats"><span>电子速度：0.1c</span><span>径向初始振幅：60 μm</span><span>轴向初始振幅：AZ μm</span><span>约 5 个方位绕行</span></div>
    <div class="card"><canvas id="plot" width="1040" height="620"></canvas><div><label>水平旋转 <input id="yaw" type="range" min="0" max="360" value="35"></label><label>俯仰角 <input id="pitch" type="range" min="5" max="85" value="52"></label><label>高度夸大 <input id="boost" type="range" min="1" max="160" value="50"></label><button id="toggle">暂停</button><button id="reset">重置视角</button></div><small>轴向比例视觉夸大，仅为方便观察；真实振幅约 9 μm，而半径约 5.15 mm。</small></div>
    <div class="card"><strong>物理边界</strong><p>轨道由外部静态电流产生的磁场驱动，电子辐射反作用未纳入，数值周期解不保证无限时间稳定、真实线圈可制造或实现统一场论。</p></div>
    </main><script>const data=POINTS; const el=id=>document.getElementById(id),ctx=el('plot').getContext('2d');let running=true,idx=0;const cvs=el('plot');
    function draw(){ctx.clearRect(0,0,1040,620);ctx.fillStyle='#090d1c';ctx.fillRect(0,0,1040,620);let ya=+el('yaw').value*Math.PI/180,pi=+el('pitch').value*Math.PI/180,boost=+el('boost').value;
    let proj=p=>{let [x,y,z]=p;let xx=x*Math.cos(ya)-y*Math.sin(ya);let yy=x*Math.sin(ya)+y*Math.cos(ya);let zz=(z/1000)*boost;return [520+xx*48,310+(-yy*Math.cos(pi)+zz*Math.sin(pi))*48]};
    ctx.strokeStyle='#304568';ctx.lineWidth=1;ctx.beginPath();ctx.ellipse(520,310,252,82,0,0,7);ctx.stroke();ctx.beginPath();ctx.strokeStyle='#78b6ff';ctx.lineWidth=2;data.forEach((p,i)=>{let [x,y]=proj(p);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y)});ctx.stroke();let p=proj(data[idx]);ctx.fillStyle='#f6ae62';ctx.beginPath();ctx.arc(p[0],p[1],6,0,7);ctx.fill();}
    for(let id of ['yaw','pitch','boost'])el(id).addEventListener('input',draw);el('toggle').onclick=()=>{running=!running;el('toggle').textContent=running?'暂停':'继续';};el('reset').onclick=()=>{el('yaw').value=35;el('pitch').value=52;el('boost').value=50;draw()};function tick(){if(running)idx=(idx+2)%data.length;draw();requestAnimationFrame(tick)}tick();</script></body></html>'''
    html=html.replace('POINTS',payload).replace('AZ',f"{row['az_m']*1e6:.6f}")
    (WEB/'index.html').write_text(html,encoding='utf-8')

if __name__=='__main__':main()
