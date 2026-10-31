
const calls=[]; const B={top:1e9,bot:-1e9};
function mkctx(H){
  const rec=(n)=>(...a)=>{for(const x of a){if(typeof x==='number'&&!isFinite(x))throw new Error(n+' non-finite: '+a);}
    calls.push(n); if(n==='lineTo'||n==='moveTo'||n==='arc'){const y=a[1]; if(y<B.top)B.top=y; if(y>B.bot)B.bot=y; if(y<0||y>H) throw new Error('OUT OF CANVAS '+n+' y='+y+' H='+H);}};
  return {clearRect:rec('clearRect'),fillRect:rec('fillRect'),beginPath:rec('beginPath'),
    moveTo:rec('moveTo'),lineTo:rec('lineTo'),stroke:rec('stroke'),fill:rec('fill'),
    arc:rec('arc'),setLineDash:rec('setLineDash'),fillText:rec('fillText')};
}
const SIZES={"c1":[1080,430],
"c2":[1080,360],
"c3":[1080,380],};
const els={};
global.document={getElementById:(id)=>{ const sz=SIZES[id]||[1080,430]; if(!els[id]) els[id]={width:sz[0],height:sz[1],getContext:()=>mkctx(sz[1])}; return els[id];}};

const C={bg:'#131a21',fg:'#e6edf3',dim:'#8b98a5',red:'#ff6b6b',grn:'#5fd38d',blu:'#6bb6ff',yel:'#ffd166'};
const G=[[0.01, 1.0, 4.5394e-14], [0.03, 1.0, 3.3014e-12], [0.1, 1.0, 2.9228e-10], [0.3, 1.0, 1.0745e-08], [1.0, 1.0, 1.9721e-07], [3.0, 1.0, 8.7476e-07], [10.0, 1.0, 1.7734e-06], [0.01, 10.0, 4.5394e-16], [0.03, 10.0, 3.3014e-14], [0.1, 10.0, 2.9228e-12], [0.3, 10.0, 1.0745e-10], [1.0, 10.0, 1.9721e-09], [3.0, 10.0, 8.7476e-09], [10.0, 10.0, 1.7734e-08], [0.01, 100.0, 4.5394e-18], [0.03, 100.0, 3.3014e-16], [0.1, 100.0, 2.9228e-14], [0.3, 100.0, 1.0745e-12], [1.0, 100.0, 1.9721e-11], [3.0, 100.0, 8.7476e-11], [10.0, 100.0, 1.7734e-10], [0.01, 1000.0, 4.5394e-20], [0.03, 1000.0, 3.3014e-18], [0.1, 1000.0, 2.9228e-16], [0.3, 1000.0, 1.0745e-14], [1.0, 1000.0, 1.9721e-13], [3.0, 1000.0, 8.7476e-13], [10.0, 1000.0, 1.7734e-12]], AR=[[1.0, 0.022025599585635245], [3.0, 0.038990496806628805], [10.0, 0.07427366581181624], [30.0, 0.13805386160486893], [100.0, 0.29277647579119814], [300.0, 0.6804542582465102], [1000.0, 3.503546457218175]], TS=[1.0, 10.0, 100.0, 246.22, 1000.0, 10000.0, 1e+16], FT=[1.9208e-05, 0.0001920797, 0.0019207975, 0.0047293876, 0.019207975, 0.1920797499, 192079749899.37592];

function T(g,s,x,y,c,sz,al){g.fillStyle=c||C.dim;g.font=(sz||11)+'px -apple-system,"Segoe UI",sans-serif';g.textAlign=al||'left';g.fillText(s,x,y);}

function frame(cv,xr,yr,xt,yt,xlab,ylab,xf,yf){
  const g=cv.getContext('2d'),W=cv.width,H=cv.height;
  const pad={l:72,r:22,t:18,b:40};
  g.clearRect(0,0,W,H);g.fillStyle=C.bg;g.fillRect(0,0,W,H);
  const X=v=>pad.l+(W-pad.l-pad.r)*(v-xr[0])/(xr[1]-xr[0]);
  const Y=v=>pad.t+(H-pad.t-pad.b)*(yr[1]-v)/(yr[1]-yr[0]);
  g.strokeStyle='#2b3542';g.lineWidth=1;
  yt.forEach(v=>{const y=Y(v);g.beginPath();g.moveTo(pad.l,y);g.lineTo(W-pad.r,y);g.stroke();
    T(g,yf(v),pad.l-8,y+4,C.dim,11,'right');});
  xt.forEach(v=>{const x=X(v);g.beginPath();g.moveTo(x,pad.t);g.lineTo(x,H-pad.b);g.stroke();
    T(g,xf(v),x,H-pad.b+16,C.dim,11,'center');});
  T(g,xlab,(pad.l+W-pad.r)/2,H-6,C.dim,12,'center');
  T(g,ylab,pad.l-56,pad.t-6,C.dim,12,'left');
  return {g:g,X:X,Y:Y,pad:pad,W:W,H:H};
}
const dec=v=>'1e'+Math.round(v);
const num=v=>(Math.abs(v)<0.01||Math.abs(v)>=1000)?v.toExponential(0):(''+v);

/* ① Ω_sw h^2 vs α，四条 β/H 曲线 */
(function(){
  const cv=document.getElementById('c1');
  const lo=Math.floor(Math.min.apply(null,G.map(r=>Math.log10(r[2]))))-0.5;
  const hi=Math.ceil(Math.max.apply(null,G.map(r=>Math.log10(r[2]))))+0.5;
  const xt=[-2,-1.523,-1,-0.523,0,0.477,1];
  const yt=[];for(let v=Math.ceil(lo);v<=Math.floor(hi);v+=3)yt.push(v);
  const f=frame(cv,[-2.2,1.2],[lo,hi],xt,yt,'log10 α','log10 (Ω_sw h²)',dec,dec);
  const g=f.g;
  g.strokeStyle=C.yel;g.setLineDash([6,4]);g.lineWidth=1.5;g.beginPath();
  g.moveTo(f.pad.l,f.Y(Math.log10(1e-12)));g.lineTo(f.W-f.pad.r,f.Y(Math.log10(1e-12)));g.stroke();g.setLineDash([]);
  T(g,'LISA 灵敏度量级 1e-12',f.W-f.pad.r-8,f.Y(Math.log10(1e-12))-6,C.yel,11,'right');
  const cols=[C.blu,C.grn,C.yel,C.red],betas=[1,10,100,1000];
  betas.forEach((b,bi)=>{
    const pts=G.filter(r=>r[1]===b).slice().sort((p,q)=>p[0]-q[0]);
    g.strokeStyle=cols[bi];g.lineWidth=2;g.beginPath();
    pts.forEach((r,i)=>{const x=f.X(Math.log10(r[0])),y=f.Y(Math.log10(r[2]));i?g.lineTo(x,y):g.moveTo(x,y);});
    g.stroke();
    const r0=pts[0],r1=pts[pts.length-1];
    T(g,'β/H='+b,f.X(Math.log10(r1[0]))+4,f.Y(Math.log10(r1[2]))+4,cols[bi],11,'left');
    g.fillStyle=cols[bi];g.beginPath();g.arc(f.X(Math.log10(r0[0])),f.Y(Math.log10(r0[2])),2.6,0,7);g.fill();
  });
})();

/* ② α_min(β/H) */
(function(){
  const cv=document.getElementById('c2');
  const lo=Math.floor(Math.min.apply(null,AR.map(r=>Math.log10(r[1])))*10)/10-0.2;
  const hi=Math.ceil(Math.max.apply(null,AR.map(r=>Math.log10(r[1])))*10)/10+0.2;
  const xt=AR.map((r,i)=>i);
  const yt=[];for(let v=Math.ceil(lo);v<=Math.floor(hi);v+=1)yt.push(v);
  const f=frame(cv,[-0.5,AR.length-0.5],[lo,hi],xt,yt,'β/H 档（左小右大）','log10 α_min',v=>'β/H='+AR[v][0],dec);
  const g=f.g;
  g.strokeStyle=C.grn;g.lineWidth=2;g.beginPath();
  AR.forEach((r,i)=>{const x=f.X(i),y=f.Y(Math.log10(r[1]));i?g.lineTo(x,y):g.moveTo(x,y);});
  g.stroke();
  AR.forEach((r,i)=>{const x=f.X(i),y=f.Y(Math.log10(r[1]));
    g.fillStyle=C.grn;g.beginPath();g.arc(x,y,3.5,0,7);g.fill();
    T(g,r[1].toFixed(3),x,y-10,C.fg,10,'center');});
})();

/* ③ f_peak vs T_* */
(function(){
  const cv=document.getElementById('c3');
  const lo=-6,hi=13;
  const xt=[0,2,4,6,8,10,12,14,16];
  const yt=[];for(let v=lo;v<=hi;v+=3)yt.push(v);
  const f=frame(cv,[-0.5,16.5],[lo,hi],xt,yt,'log10 T_* (GeV)','log10 f_peak (Hz)',dec,dec);
  const g=f.g;
  const yb1=f.Y(Math.log10(1e-1)),yb2=f.Y(Math.log10(1e-4));
  g.fillStyle='rgba(95,211,141,0.16)';g.fillRect(f.pad.l,yb1,f.W-f.pad.l-f.pad.r,yb2-yb1);
  T(g,'LISA 带 1e-4 – 1e-1 Hz',f.pad.l+10,yb1+16,C.grn,11,'left');
  g.strokeStyle=C.blu;g.lineWidth=2;g.beginPath();
  TS.forEach((t,i)=>{const x=f.X(Math.log10(t)),y=f.Y(Math.log10(FT[i]));i?g.lineTo(x,y):g.moveTo(x,y);});
  g.stroke();
  TS.forEach((t,i)=>{const x=f.X(Math.log10(t)),y=f.Y(Math.log10(FT[i]));
    g.fillStyle=C.blu;g.beginPath();g.arc(x,y,3.2,0,7);g.fill();});
  const iEW=TS.indexOf(246.22), iG=TS.indexOf(1e16);
  T(g,'电弱 246 GeV（带内）',f.X(Math.log10(246.22)),f.Y(Math.log10(FT[iEW]))-12,C.grn,11,'center');
  T(g,'GUT 1e16 GeV（带外）',f.X(Math.log10(1e16)),f.Y(Math.log10(FT[iG]))-12,C.red,11,'right');
})();

console.log('OK ops='+calls.length+' y_range=['+B.top.toFixed(1)+','+B.bot.toFixed(1)+']');
