"""Create reproducible V111 numerical curves, examples and offline HTML.
No external network. Output figures are numerical toy-model plots, not observations.
"""
import json,csv,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .v111 import Params,simulate,analytic_bounds
from .floquet_counterexample import compute

ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'figures';RES=ROOT/'results';WEB=ROOT/'web'
for p in [FIG,RES,WEB]:p.mkdir(exist_ok=True,parents=True)

def save_csv(path,sim):
    o=sim['obs'];y=sim['y']
    with path.open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['t','theta','theta_dot','Aplus','Aminus','Etheta','Eem','H','Q','N_QplusIntegral'])
        for i,t in enumerate(sim['t']):
            writer.writerow([f'{t:.14g}',*[f'{v:.14g}' for v in
                [y[0,i],y[1,i],y[2,i],y[4,i],o['Etheta'][i],o['Eem'][i],o['H'][i],o['Q'][i],o['N'][i]]]])

def main():
    cases={
      'with_potential':(Params(k=1,g=.22,f=1,L4=4),[.35,0,.01,0,.009,0,0],180),
      'shift_symmetric':(Params(k=1,g=.5,f=1,L4=0),[.35,.7,.05,0,.04,0,0],160),
      'tachyonic_backreaction':(Params(k=1,g=.5,f=1,L4=0),[.35,3.,.018,0,.05,0,0],60),
    }
    outcomes={};sims={}
    for name,(p,y0,t) in cases.items():
        a=simulate(p,y0,duration=t,steps=1301,rtol=1e-10,atol=1e-12)
        sims[name]=a; save_csv(RES/f'{name}_numerical.csv',a)
        E=a['obs']['H'];Q=a['obs']['Q']; td=a['obs']['td']; Em=a['obs']['Eem'];N=a['obs']['N']
        outcomes[name]={
          'params':p.__dict__, 'initial':y0,'duration':t,'nfev':a['nfev'],
          'relative_energy_drift':a['energy_rel_drift'],
          'charge_Q_drift':a['q_absolute_range'],
          'extended_N_drift':a['noether_absolute_drift'],
          'initial_total_energy':float(E[0]),'initial_charge_Q':float(Q[0]),
          'min_theta_dot':float(np.min(td)),'max_theta_dot':float(np.max(td)),
          'min_em_energy':float(np.min(Em)),'max_em_energy':float(np.max(Em)),
          'bound':analytic_bounds(p,float(E[0]),float(Q[0]))}
    outcomes['floquet_positive_stiffness_counterexample']=compute()
    (RES/'V111_NUMERICAL_SUMMARY.json').write_text(json.dumps(outcomes,ensure_ascii=False,indent=2,default=lambda v:bool(v) if isinstance(v,np.bool_) else float(v)),encoding='utf-8')
    # plot five: positive instantaneous stiffness with Floquet instability
    c=outcomes['floquet_positive_stiffness_counterexample']
    tt=np.linspace(0,c['tperiod'],400);p0=Params(k=1,g=.16);q0=1-0.16*0.35*2*np.sin(2*tt)
    plt.figure(figsize=(10,4.8));plt.plot(tt,q0,label='instantaneous omega_h^2(t) > 0')
    plt.axhline(0,linestyle='--',linewidth=1,label='tachyonic boundary');plt.ylim(-0.1,1.3)
    plt.xlabel('Dimensionless time');plt.ylabel('Mode stiffness');
    plt.title('V111 counterexample: positive stiffness yet Floquet growth mu='+f"{c['floquet_mu']:.6f}")
    plt.legend();plt.tight_layout();plt.savefig(FIG/'06_POSITIVE_STIFFNESS_FLOQUET_UNSTABLE.png',dpi=170);plt.close()
    # plot one: exact Noether invariant, Q violation in potential, and energy exchange
    plt.figure(figsize=(10,5.2));a=sims['with_potential'];t=a['t'];o=a['obs'];
    plt.plot(t,o['Q'],label='Q (not conserved for Lambda4 > 0)',lw=1)
    plt.plot(t,o['N']-o['N'][0],label='Q + Lambda4 integral(sin(theta) dt) - initial',lw=1.3)
    plt.xlabel('Dimensionless time');plt.ylabel('Charge / residual');plt.title('V111: broken shift symmetry and corrected charge balance');plt.legend();plt.tight_layout();
    plt.savefig(FIG/'01_NOETHER_BALANCE_THEORY.png',dpi=170);plt.close()
    # plot two: tachyonic feedback
    plt.figure(figsize=(10,5.2));a=sims['tachyonic_backreaction'];t=a['t'];o=a['obs'];
    plt.plot(t,o['Etheta'],label='Internal phase kinetic energy',lw=1.5)
    plt.plot(t,o['Eem'],label='Electromagnetic mode energy',lw=1.5)
    plt.plot(t,o['H'],label='Total conserved H',linestyle='--',lw=1.4)
    plt.xlabel('Dimensionless time');plt.ylabel('Dimensionless energy');plt.title('V111: self-quenching of initial tachyonic amplification');plt.legend();plt.tight_layout();
    plt.savefig(FIG/'02_BACKREACTION_TACHYON_THEORY.png',dpi=170);plt.close()
    # plot three: bounds and charges with shift symmetry
    plt.figure(figsize=(10,5.2));a=sims['shift_symmetric'];t=a['t'];o=a['obs'];b=outcomes['shift_symmetric']['bound'];
    plt.plot(t,o['td'],label='theta_dot (computed)',lw=1.6)
    plt.plot(t,np.full_like(t,b['theta_velocity_from_Q_min']),label='rigorous lower bound',ls='--')
    plt.plot(t,np.full_like(t,b['theta_velocity_from_Q_max']),label='rigorous upper bound',ls='--')
    plt.xlabel('Dimensionless time');plt.ylabel('theta_dot');plt.title('V111: Noether + energy bounds for a winding phase');plt.legend();plt.tight_layout();
    plt.savefig(FIG/'03_NOETHER_ENERGY_BOUNDS_THEORY.png',dpi=170);plt.close()
    # plot four: conservation normalized residual at N
    plt.figure(figsize=(10,4.8))
    for name,a in sims.items():
        H=np.asarray(a['obs']['H']);plt.plot(a['t'],(H-H[0])/H[0],label=name,lw=1)
    plt.xlabel('Dimensionless time');plt.ylabel('Relative conservation residual');plt.title('V111: numerical H conservation is not the same as exact arithmetic');plt.legend();plt.tight_layout()
    plt.savefig(FIG/'04_ENERGY_RESIDUAL_THEORY.png',dpi=170);plt.close()
    build_web(sims,outcomes)
    print(json.dumps({k:({'energy_drift':x['relative_energy_drift'],'N_drift':x['extended_N_drift'],'Qrange':x['charge_Q_drift'],'Eem_max':x['max_em_energy']} if 'relative_energy_drift' in x else x) for k,x in outcomes.items()},indent=2))
    return outcomes

def build_web(sims,outcomes):
    # Embedded data: works offline (file://) without CORS or CDN.
    embed={}
    for name,a in sims.items():
        sl=slice(None,None,5)
        embed[name]={'t':np.round(a['t'][sl],6).tolist(),
            'H':np.round(a['obs']['H'][sl],8).tolist(),
            'Etheta':np.round(a['obs']['Etheta'][sl],8).tolist(),
            'Eem':np.round(a['obs']['Eem'][sl],8).tolist(),
            'Q':np.round(a['obs']['Q'][sl],8).tolist(),
            'N':np.round(a['obs']['N'][sl],8).tolist()}
    script="""
const DATA = __DATA__;
const META = __META__;
const canvas = document.querySelector('#curve');
const ctx = canvas.getContext('2d');
const mode = document.querySelector('#mode');
const metric = document.querySelector('#metric');
const summary = document.querySelector('#summary');
function draw(){
 const m=mode.value, key=metric.value, s=DATA[m], vals=s[key];
 const cssW=Math.max(320,canvas.clientWidth),cssH=330;
 const dpr=Math.max(1,devicePixelRatio||1);canvas.width=Math.floor(cssW*dpr);canvas.height=cssH*dpr;
 ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,cssW,cssH);
 const pad={left:63,right:16,top:14,bottom:38};const pw=cssW-pad.left-pad.right,ph=cssH-pad.top-pad.bottom;
 const xmin=s.t[0],xmax=s.t.at(-1);let lo=Math.min(...vals),hi=Math.max(...vals);
 if(Math.abs(hi-lo)<1e-13){let span=Math.max(Math.abs(hi)*0.1,0.0001);lo-=span;hi+=span;}
 else {let d=(hi-lo)*0.08;lo-=d;hi+=d;}
 ctx.strokeStyle='#39465c';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(pad.left,pad.top);ctx.lineTo(pad.left,pad.top+ph);ctx.lineTo(pad.left+pw,pad.top+ph);ctx.stroke();
 ctx.font='12px system-ui';ctx.fillStyle='#9dafc6';ctx.fillText(hi.toPrecision(4),2,pad.top+8);ctx.fillText(lo.toPrecision(4),2,pad.top+ph);
 ctx.fillText(xmax.toFixed(0),pad.left+pw-18,pad.top+ph+23);ctx.fillText('0',pad.left,pad.top+ph+23);
 ctx.strokeStyle='#5ce2c5';ctx.lineWidth=2;ctx.beginPath();vals.forEach((y,i)=>{const x=pad.left+(s.t[i]-xmin)/(xmax-xmin)*pw;const yy=pad.top+(hi-y)/(hi-lo)*ph;if(i===0)ctx.moveTo(x,yy);else ctx.lineTo(x,yy);});ctx.stroke();
 const meta=META[m];summary.innerText=`H 初值 ${meta.initial_total_energy.toFixed(6)}  ·  H 相对漂移 ${meta.relative_energy_drift.toExponential(2)}  ·  Q 变化范围 ${meta.charge_Q_drift.toExponential(2)}  ·  扩展守恒量残差 ${meta.extended_N_drift.toExponential(2)}`;
 document.querySelector('#metric-name').textContent=key+' / '+m;
}
mode.addEventListener('change',draw);metric.addEventListener('change',draw);addEventListener('resize',draw);draw();
"""
    script=script.replace('__DATA__',json.dumps(embed)).replace('__META__',json.dumps({k:outcomes[k] for k in sims},default=lambda v:bool(v) if isinstance(v,np.bool_) else float(v)))
    html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ROOT V111 独立验收实验室</title>
<style>body{background:#0e1524;color:#e9f1ff;font:16px system-ui,-apple-system,sans-serif;max-width:1000px;padding:34px;margin:auto;line-height:1.7}h1{font-size:27px}article{padding:20px;border:1px solid #314358;border-radius:12px;margin:20px 0;background:#162237}label{display:inline-flex;gap:8px;margin:10px 20px 14px 0;align-items:center}select{background:#0e1524;color:white;border:1px solid #7889ab;padding:9px;border-radius:6px}canvas{width:100%;display:block}small{color:#aebdd2}code{font-size:14px;color:#5ce2c5}</style></head><body>
<h1>ROOT V111 · Noether 守恒与引力变分</h1>
<p>数值模型为轴子样电动力学的有限模截断。只展示数学与玩具模型结果，不代表新相互作用或真实实验。</p>
<article><h2>数值能量与相位电荷</h2><label>模型：<select id="mode"><option value="with_potential">有周期相位势</option><option value="shift_symmetric">无相位势 · 温和耦合</option><option value="tachyonic_backreaction">无相位势 · 初始不稳定模式</option></select></label>
<label>观察量：<select id="metric"><option value="Q">正则相位电荷 Q</option><option value="N">Q + Λ⁴∫sinθdt</option><option value="Eem">电磁模式能量</option><option value="Etheta">相位能量</option><option value="H">总能量 H</option></select></label>
<h3 id="metric-name">Q</h3><canvas id="curve" role="img" aria-label="能量与守恒荷数值曲线"></canvas><small id="summary"></small></article>
<article><h2>精确数学约束</h2><p><code>dQ/dt = −Λ⁴sinθ</code>　　<code>dH/dt = 0</code></p><p><code>|Q−f² θ̇| ≤ |λ| H/k</code></p><p>当 Λ=0，Q 守恒；当 Λ≠0，Q 的变化正好由相位势解释。</p></article>
<article><h2>引力审计</h2><p>在 θ 与 F 独立于度规的前提下，<code>√−g θ Fμν F̃μν</code> 是与度规无关的四形式密度。它对 Einstein 方程没有额外的直接应力能量贡献；相位与 Maxwell 标准动能仍贡献引力。</p><p>因此这一模型不能无参数导出 Newton G，也不能证明四力统一。</p></article>
<script>'''+script+'''</script></body></html>'''
    (WEB/'index.html').write_text(html,encoding='utf-8')

if __name__=='__main__':main()
