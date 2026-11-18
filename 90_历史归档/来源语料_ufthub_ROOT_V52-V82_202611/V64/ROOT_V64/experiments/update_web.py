from pathlib import Path
src=Path(__file__).resolve().parents[1]/'web/legacy_v63.html'
out=src.with_name('index.html')
s=src.read_text(encoding='utf-8')
s=s.replace('ROOT V63','ROOT V64').replace('微观螺旋与诱导引力实验室','严格审计 · 三维空间螺旋与引力场').replace('空间螺旋与诱导引力','空间螺旋与引力审计').replace('原生 WebGL2 离线 3D · 数学与候选模型对照实验','离线 WebGL2 交互 3D · 几何/微观场/已知引力分级').replace('注意：可视化 ≠ 发现新物理定律','54项数学测试通过 ≠ 大统一已证明')
s=s.replace('<main><div class="scene">','<div style="padding:12px 22px;background:#101f31;border-bottom:1px solid #263d55;font-size:13px"><b>V64 的新证明：</b> 带螺旋相位的圆柱 KG 真解 → 正能量密度 → 在已知 G 下的柱对称引力。<a href="v64_audit.html" style="color:#75dcea;margin-left:13px">打开精算和错误审计仪表盘</a> · <a href="../research/01_失败原因逐条修复矩阵.md" style="color:#75dcea">30项失败原因</a>。地球仍是理想 toy，不是 IGRF/EGM 数据。</div><main><div class="scene">')
s=s.replace('螺旋模式中的绿色切向、橙色法向、紫色副法向展示正交几何。','螺旋模式中的绿色切向、橙色法向、紫色副法向展示正交几何。图形只作全局均匀缩放，保持所选螺旋角。')
start=s.index('function buildHelix(){')
end=s.index('\nfunction renderMesh(',start)
replacement='''function buildHelix(){
let out=[],R=+$('radius').value,a=+$('angle').value*Math.PI/180;
// Exact helix in model units: |dr/dt|=1, dtheta/dt=cos(a)/R, dz/dt=sin(a).
// Uniform display scale preserves tangent angle and all curve ratios.
let scale=1.35/Math.max(R,4*Math.sin(a),.001), points=[];
for(let i=0;i<=600;i++){
 let tt=(i/600-.5)*8, phase=tt*Math.cos(a)/R;
 points.push([scale*R*Math.cos(phase),scale*R*Math.sin(phase),scale*tt*Math.sin(a)]);
}
for(let i=0;i<points.length-1;i++)line(out,points[i],points[i+1],[.17,.83,1]);
line(out,[0,0,-1.65],[0,0,1.65],[.54,.64,.75]);
line(out,[-1.65,0,0],[1.65,0,0],[.45,.5,.55]);
line(out,[0,-1.65,0],[0,1.65,0],[.45,.5,.55]);
if(Math.cos(a)>1e-7){
 let i=420,pt=points[i],phase=(i/600-.5)*8*Math.cos(a)/R;
 let T=[-Math.cos(a)*Math.sin(phase),Math.cos(a)*Math.cos(phase),Math.sin(a)];
 let N=[-Math.cos(phase),-Math.sin(phase),0];
 let B=[T[1]*N[2]-T[2]*N[1],T[2]*N[0]-T[0]*N[2],T[0]*N[1]-T[1]*N[0]];
 arrow(out,pt,T,[.31,1,.55],.45);arrow(out,pt,N,[1,.6,.26],.45);arrow(out,pt,B,[.8,.48,1],.45);
}
return mesh(out,gl.LINES)}
'''
s=s[:start]+replacement+s[end:]
start=s.index("    }else{\n      const R=Math.min",s.index('function drawFallback'))
end=s.index('    }\n    requestAnimationFrame(drawFallback)',start)
fallback='''    }else{
      const R=+$('radius').value,a=+$('angle').value*Math.PI/180;
      const scale=1.35/Math.max(R,4*Math.sin(a),.001);
      segment([0,0,-1.65],[0,0,1.65],'#9fb8ce',2*dpr);
      segment([-1.65,0,0],[1.65,0,0],'#718fa6',1*dpr);
      segment([0,-1.65,0],[0,1.65,0],'#718fa6',1*dpr);
      let prev=null;
      for(let i=0;i<=600;i++){
        let tt=(i/600-.5)*8,theta=tt*Math.cos(a)/R;
        let q=[scale*R*Math.cos(theta),scale*R*Math.sin(theta),scale*tt*Math.sin(a)];
        if(prev)segment(prev,q,'#48d7fc',2*dpr);
        prev=q;
      }
'''
s=s[:start]+fallback+s[end:]
out.write_text(s,encoding='utf-8')
print(out, len(s))
