from pathlib import Path
import csv,json,html
base=Path(__file__).resolve().parents[1]
with (base/'data'/'astro_reference.csv').open(encoding='utf-8-sig') as f:
    rows=list(csv.DictReader(f))
for r in rows:
    for k,v in list(r.items()):
        if k in ('name','provenance','limitations'): continue
        r[k]=float(v) if v not in (None,'') else None
options='\n'.join(f'<option value="{i}">{html.escape(r["name"])}</option>' for i,r in enumerate(rows))
page=r'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ROOT V80 · 星际—微观引力联合实验室</title>
<style>
:root{--bg:#08101e;--panel:#101d30;--panel2:#14243a;--border:#31445d;--text:#edf4ff;--muted:#a8bad4;--accent:#67d8e9;--gold:#ffc67b;--green:#93e2b1}
*{box-sizing:border-box}body{margin:0;color:var(--text);background:radial-gradient(ellipse at 60% 0%,#193354,#08101e 58%);font-family:system-ui,-apple-system,"Segoe UI",sans-serif;min-height:100vh}
header{max-width:1290px;margin:auto;padding:28px 22px 10px;display:flex;align-items:center;justify-content:space-between;gap:20px}.eyebrow{color:var(--accent);letter-spacing:.17em;font-size:12px;font-weight:750}h1{font-size:clamp(24px,3vw,36px);margin:6px 0}h2{margin:0 0 15px;font-size:19px}p{color:var(--muted);line-height:1.65}header .sub{max-width:790px;margin:0}.tag{border:1px solid #496078;color:#d9e7ff;border-radius:999px;padding:7px 12px;font-size:12px;white-space:nowrap}
main{max-width:1290px;margin:auto;display:grid;grid-template-columns:365px 1fr;gap:18px;padding:18px 22px 50px}.panel{border:1px solid var(--border);background:rgba(16,29,48,.88);border-radius:18px;padding:20px;box-shadow:0 12px 28px #0003}.sidebar{display:flex;flex-direction:column;gap:16px}.controls{display:grid;gap:17px}label{color:#d6e5f7;display:block;font-weight:650;font-size:13px;margin-bottom:8px}input[type=range]{width:100%;accent-color:var(--accent)}select{background:var(--panel2);border:1px solid var(--border);color:white;border-radius:10px;padding:11px 10px;width:100%;font-size:14px}.value{color:var(--gold);font-variant-numeric:tabular-nums}.micro{font-size:12px;color:#9aaeca}.small-note{margin-top:12px;color:#b5c8dd;font-size:12px;line-height:1.55}.emphasis{background:#1a2e44;border-left:3px solid var(--gold);padding:12px 13px;border-radius:7px;color:#e2edfa;font-size:13px;line-height:1.6}.muted{color:var(--muted)}.maincontent{display:flex;flex-direction:column;gap:18px;min-width:0}.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:11px}.metric{background:var(--panel2);border-radius:12px;padding:12px;min-width:0}.metric .k{font-size:12px;color:var(--muted)}.metric .v{font-size:19px;font-weight:750;margin-top:8px;color:#fff;overflow-wrap:anywhere;font-variant-numeric:tabular-nums}.metric .unit{font-size:11px;color:#a8bad4;margin-top:5px}.flex{display:grid;grid-template-columns:1fr 1fr;gap:14px}.graph{border:1px solid var(--border);background:#0a1525;border-radius:12px;width:100%;display:block}.math{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;color:#bfeaf0}.legend{display:grid;gap:10px}.legend b{color:#ebf6ff}a{color:#8ddee9}.equation{padding:13px;border-radius:9px;background:#0d192a;line-height:1.75;overflow:auto}.eq-row{font-size:12px;color:#a6c4d6}.flexdetails{display:grid;grid-template-columns:1fr 1fr;gap:13px} .foot{font-size:12px;color:var(--muted);margin-top:12px}canvas{width:100%;height:260px}.detail{font-size:13px;line-height:1.8;color:#d2e2f3}strong{color:#f0f8ff}.status{display:inline-flex;align-items:center;gap:7px;background:#253c4e;border-radius:999px;padding:5px 10px;color:#d4f6ed;font-size:12px;font-weight:650}
@media(max-width:1030px){main{grid-template-columns:1fr}.sidebar{display:grid;grid-template-columns:1fr 1fr}.metrics{grid-template-columns:repeat(2,1fr)}}@media(max-width:630px){header{display:block}.tag{display:inline-block;margin-top:12px}.sidebar{display:flex}.flex,.flexdetails{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}}
</style></head><body>
<header><div><div class="eyebrow">ROOT / V80 RESEARCH LAB</div><h1>星际—微观统一场论检验</h1><p class="sub">太阳系 · 白矮星 · 中子星 · 磁星｜引力紧致度、曲率、QED 临界磁场与候选 G 耦合。展示理论模型与可证伪条件，不宣称完成四力统一。</p></div><div class="tag">离线运行 · 可复算 · 假说隔离</div></header>
<main><aside class="sidebar"><div class="panel controls"><h2>01 / 选择研究环境</h2><div><label for="star">参考天体</label><select id="star">__OPTIONS__</select></div>
<div><label for="bexp">假设磁场 B：<span id="bvalue" class="value"></span></label><input id="bexp" type="range" min="-6" max="11" step="0.1" value="-4.3"><div class="micro">10⁻⁶ — 10¹¹ T。滑块值始终是假设场强，不是自动获取的测量值。</div></div>
<div><label for="beta">示意新耦合 β<sub>B</sub>：<span class="value" id="betavalue"></span></label><input id="beta" type="range" min="-2" max="6" step="0.1" value="0"><div class="micro">仅演示 ΔG/G = βB · B²/(2μ₀ρc²)，无理论或实验确证。</div></div>
<div><label for="az">可视化方位：<span class="value" id="azvalue"></span></label><input id="az" type="range" min="-180" max="180" value="27" step="1"></div>
<div class="emphasis"><b>研究边界</b>：球形 Schwarzschild 曲率只作为参照。对旋转、磁化且有内部高密度物质的天体，必须求解耦合 Einstein–Maxwell–QED–EOS 模型。</div></div>
<div class="panel"><h2>02 / 已报告的观测检验</h2><div class="legend"><div><b>MICROSCOPE</b><div class="micro">Ti/Pt 自由落体：η 约 10⁻¹⁵，未发现显著偏离</div></div><div><b>Cassini</b><div class="micro">γ−1=(2.1±2.3)×10⁻⁵</div></div><div><b>双脉冲星</b><div class="micro">轨道衰减四极辐射检验：约 1.3×10⁻⁴</div></div><div><b>GW170817 与 GWTC-5.0</b><div class="micro">波速限制、强场波形与传播（模型依赖）</div></div></div></div></aside>
<section class="maincontent"><div class="panel"><div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap"><h2>03 / 跨星体研究概览</h2><span class="status">实验值 ≠ 模拟结果</span></div><div class="metrics"><div class="metric"><div class="k">牛顿表面 g（不含自转）</div><div id="metric_g" class="v">—</div><div class="unit">m/s²</div></div><div class="metric"><div class="k">引力紧致度 χg</div><div id="metric_chi" class="v">—</div><div class="unit">GM/(Rc²)</div></div><div class="metric"><div class="k">球对称外部 K</div><div id="metric_k" class="v">—</div><div class="unit">m⁻⁴</div></div><div class="metric"><div class="k">磁场与 QED 临界场比</div><div id="metric_q" class="v">—</div><div class="unit">B / BQ</div></div></div><p class="micro" id="source_note"></p></div>
<div class="flex"><div class="panel"><h2>04 / 球形天体·三维透视示意</h2><canvas id="orb" class="graph" width="660" height="380" aria-label="透视星体与磁场线"></canvas><p class="micro">示意用的空间投影和磁力线并非真实星体内部 MHD/GR 数值解。</p></div><div class="panel"><h2>05 / 量级比较</h2><canvas id="bars" class="graph" width="660" height="380" aria-label="磁能及曲率强度量级"></canvas><div class="micro">显示不同物理量的 log₁₀ 量级；非同单位量不得按条形长度直接解释为同一种力。</div></div></div>
<div class="panel"><h2>06 / 假说的独立证伪</h2><div class="flexdetails"><div><div class="math">HYPOTHESIS ONLY — not a derived physical law</div><div class="equation">ΔG/G = β<sub>B</sub> B² / (2μ₀ ρ<sub>mean</sub> c²)</div><div class="detail" style="margin-top:12px">演示磁能/静能比 χ<sub>B</sub>：<strong id="field_fraction">—</strong><br>模型给出的 ΔG/G：<strong id="deltag">—</strong><br>模型范围检查：<strong id="check_msg">—</strong></div></div><div><div class="math">ESTABLISHED / CONDITIONAL</div><div class="equation">K = 48G²M²/(c⁴R⁶)<br>K R⁴ = 48[GM/(Rc²)]²<br>B<sub>Q</sub> = m<sub>e</sub>²c²/(eℏ)</div><p class="micro">如果想证明 G 由电磁场产生，必须给出不使用已测 G 的独立推导，以及跨天体一致的新观测预测。</p></div></div></div>
<div class="panel"><h2>07 / 研究结论与复现</h2><p>在合成磁星参考模型中，B/B<sub>Q</sub> 可以大于 1，意味着强场量子电动力学重要；同时局部代表磁能与全星平均静能密度之比约为 10⁻⁹。这两件事可以同时成立，不表示 G 因磁场改变。</p><p>源码 <code>src/cosmos.py</code>；数值表 <code>data/astro_reference.csv</code>；完整证明状态与失败条件见 <code>PROOF_STATUS.md</code>。所有数据和公式均随 ZIP 离线附带。</p><div class="foot">版本 V80 · 不包含实时天文观测同步 · 基准数据包含舍入与示意输入 · 统一场论最终证明仍为开放问题。</div></div></section></main>
<script>
'use strict';
const data=__DATA__;
const mu0=1/(8.8541878188e-12*299792458**2), c=299792458, BQ=4414005230.711857;
const $=(id)=>document.getElementById(id);
const fmt=(n,p=3)=> Number.isFinite(n)?(n===0?'0':(Math.abs(n)>=1000 || Math.abs(n)<.001?n.toExponential(p):n.toPrecision(p+1))):'—';
const star=$('star'), bexp=$('bexp'), beta=$('beta'), az=$('az');
function redraw(){
 const d=data[Number(star.value)||0]; const B=10**Number(bexp.value), bcoef=10**Number(beta.value), azim=Number(az.value)*Math.PI/180;
 const chiB=(B*B/(2*mu0))/(d.mean_density_kg_m3*c*c), val=bcoef*chiB;
 $('bvalue').textContent=fmt(B)+' T'; $('betavalue').textContent=fmt(bcoef); $('azvalue').textContent=az.value+'°';
 $('metric_g').textContent=fmt(d.newtonian_g_m_s2);$('metric_chi').textContent=fmt(d.compactness);$('metric_k').textContent=fmt(d.schwarzschild_K_m4);$('metric_q').textContent=fmt(B/BQ);
 $('source_note').textContent='质量/半径：'+d.provenance+'。'+(d.limitations||'')+'。磁场滑块为用户选择的假设值。';
 $('field_fraction').textContent=fmt(chiB);$('deltag').textContent=fmt(val);
 $('check_msg').textContent=val>1?'超出微弱修正的近似域；必须用非线性理论。':'只是示意性猜想，不能解释普适引力常数。';
 drawOrb(d,azim,B); drawBars(d,B,chiB);
}
function drawOrb(d,azim,B){const canvas=$('orb'),ctx=canvas.getContext('2d'),w=canvas.width,h=canvas.height;ctx.clearRect(0,0,w,h);let bg=ctx.createLinearGradient(0,0,w,h);bg.addColorStop(0,'#122f47');bg.addColorStop(1,'#06101d');ctx.fillStyle=bg;ctx.fillRect(0,0,w,h);
 ctx.save();ctx.translate(w*.50,h*.52);const r=92;const glow=ctx.createRadialGradient(-35,-25,5,0,0,115);let b=Number(Math.log10(B)); glow.addColorStop(0,b>7?'#ffe4af':'#81b8eb');glow.addColorStop(.65,b>7?'#d59765':'#285a89');glow.addColorStop(1,'#102137');ctx.fillStyle=glow;ctx.beginPath();ctx.arc(0,0,r,0,2*Math.PI);ctx.fill();ctx.strokeStyle='#95bad5';ctx.globalAlpha=.22;ctx.lineWidth=1;for(let a=-55;a<=55;a+=27.5){ctx.beginPath();ctx.ellipse(0,0,r,Math.abs(r*Math.sin(a*Math.PI/180)),azim,0,Math.PI*2);ctx.stroke()}
 ctx.globalAlpha=.68;for(let i=0;i<7;i++){let offset=(i-3)*.22;const rx=140+Math.abs(i-3)*15,ry=45+Math.abs(i-3)*5;ctx.save();ctx.rotate(azim+offset);ctx.strokeStyle=i%2?'#69d8ec':'#bf88dd';ctx.lineWidth=1.8;ctx.beginPath();ctx.ellipse(0,0,rx,ry,0,0,Math.PI*2);ctx.stroke();ctx.restore()}
 ctx.globalAlpha=1;ctx.fillStyle='#def4ff';ctx.font='18px sans-serif';ctx.fillText(d.name,-250,-145);ctx.font='12px monospace';ctx.fillStyle='#acd0e6';ctx.fillText('3D PROJECTION / NOT SCALE',-250,-123);ctx.restore();
}
function drawBars(d,B,chiB){const cv=$('bars'),ctx=cv.getContext('2d'),w=cv.width,h=cv.height;ctx.fillStyle='#091628';ctx.fillRect(0,0,w,h);const values=[d.compactness,d.schwarzschild_K_m4,chiB,B/BQ];const names=['χg / 紧致度','K / m⁻⁴','χB / 能量密度比','B/BQ / 量子场'];const lo=-48,hi=12;ctx.font='13px sans-serif';values.forEach((v,i)=>{const y=48+i*78;ctx.fillStyle='#c0d8ea';ctx.fillText(names[i],24,y);const barx=24,bary=y+9,barw=w-52;ctx.fillStyle='#1b3147';ctx.fillRect(barx,bary,barw,19);const lg=Math.log10(Math.max(Math.abs(v),1e-70));const norm=Math.min(1,Math.max(0,(lg-lo)/(hi-lo)));ctx.fillStyle=i===1?'#d09bec':i===2?'#83d6d0':i===3?'#f2c47e':'#6cace5';ctx.fillRect(barx,bary,barw*norm,19);ctx.fillStyle='#f0f5ff';ctx.fillText(fmt(v),barx+3,bary+15)});
 ctx.fillStyle='#97b2c8';ctx.font='12px sans-serif';ctx.fillText('各量以自身 SI / 无量纲标尺的 log10 数值映射',24,h-18)
}
star.value='3'; const b0=data[3].assumed_B_T;bexp.value=Math.log10(b0);['change','input'].forEach(evt=>{[star,bexp,beta,az].forEach(el=>el.addEventListener(evt,()=>{if(el===star){const d=data[Number(star.value)];if(d.assumed_B_T) bexp.value=Math.log10(d.assumed_B_T)}redraw()}))});redraw();
</script></body></html>'''
page=page.replace('__OPTIONS__',options).replace('__DATA__',json.dumps(rows,ensure_ascii=False,separators=(',',':')))
(base/'web'/'index.html').write_text(page,encoding='utf-8')
print('created web html',len(page))
