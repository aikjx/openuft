
'use strict';
const canvas=document.getElementById('globe');const gl=canvas.getContext('webgl2',{antialias:true,alpha:false});
if(!gl){document.getElementById('legend').textContent='当前浏览器未启用 WebGL2；请使用支持 WebGL2 的 Chrome / Firefox 浏览器。';}
const $=s=>document.getElementById(s);
let mode='earth',spin=true,yaw=.5,pitch=.25,zoom=1.0,drag=false,last=[0,0],frame=0;
const controls=['angle','radius','N','xi','ell'];
function update(){let a=+$('angle').value*Math.PI/180, r=+$('radius').value,n=+$('N').value,xi=+$('xi').value,ell=+$('ell').value;
$('aTxt').textContent=$('angle').value+'°';$('rTxt').textContent=r.toFixed(2)+' m';$('nTxt').textContent=n;$('xiTxt').textContent=xi.toFixed(3);$('ellTxt').textContent=ell.toFixed(2);
$('vp').textContent=Math.cos(a).toFixed(5);$('vz').textContent=Math.sin(a).toFixed(5);
$('kap').textContent=(Math.cos(a)**2/r).toFixed(5);$('tor').textContent=(Math.sin(a)*Math.cos(a)/r).toFixed(5);
let weight=1-6*xi;let G=12*Math.PI*ell*ell/(n*weight);$('gRatio').textContent=Math.abs(weight)<1e-11?'无曲率项':(G>0?'':'负符号 · ')+Math.abs(G).toPrecision(5);
}
controls.forEach(s=>$(s).addEventListener('input',update));update();
$('btnEarth').onclick=()=>{mode='earth';$('btnEarth').classList.add('sel');$('btnHelix').classList.remove('sel')};
$('btnHelix').onclick=()=>{mode='helix';$('btnHelix').classList.add('sel');$('btnEarth').classList.remove('sel')};
$('btnPause').onclick=()=>{spin=!spin;$('btnPause').textContent=spin?'暂停旋转':'继续旋转'};
canvas.addEventListener('pointerdown',e=>{drag=true;last=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId)});
canvas.addEventListener('pointermove',e=>{if(!drag)return;yaw+=(e.clientX-last[0])*.008;pitch=Math.max(-1.55,Math.min(1.55,pitch+(e.clientY-last[1])*.008));last=[e.clientX,e.clientY]});
canvas.addEventListener('pointerup',()=>drag=false);canvas.addEventListener('wheel',e=>{zoom=Math.min(3,Math.max(.5,zoom*Math.exp(-e.deltaY*.001)));e.preventDefault()},{passive:false});
if(gl){
const vs=`#version 300 es
in vec3 aPosition;in vec3 aColor;in vec3 aNormal;uniform float uYaw;uniform float uPitch;uniform float uZoom;uniform float uAspect;uniform bool uLit;out vec3 vColor;
void main(){float cy=cos(uYaw),sy=sin(uYaw),cx=cos(uPitch),sx=sin(uPitch);
vec3 p=vec3(cy*aPosition.x+sy*aPosition.z, aPosition.y,-sy*aPosition.x+cy*aPosition.z);
p=vec3(p.x,cx*p.y-sx*p.z,sx*p.y+cx*p.z);
vec3 n=vec3(cy*aNormal.x+sy*aNormal.z,aNormal.y,-sy*aNormal.x+cy*aNormal.z);
n=vec3(n.x,cx*n.y-sx*n.z,sx*n.y+cx*n.z);
float dist=max(1.2,4.0-p.z);vec2 xy=p.xy*uZoom*1.9/dist;
gl_Position=vec4(xy.x/uAspect,xy.y,-p.z/7.0,1.0);
float diffuse=0.28+0.72*max(0.0,dot(normalize(n),normalize(vec3(-0.3,0.7,0.8))));
vColor=aColor*(uLit?diffuse:1.0);
}`;
const fs=`#version 300 es
precision highp float;in vec3 vColor;out vec4 frag;void main(){frag=vec4(vColor,1.0);}`;
function mkShader(type,src){let sh=gl.createShader(type);gl.shaderSource(sh,src);gl.compileShader(sh);if(!gl.getShaderParameter(sh,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(sh));return sh}
const prog=gl.createProgram();gl.attachShader(prog,mkShader(gl.VERTEX_SHADER,vs));gl.attachShader(prog,mkShader(gl.FRAGMENT_SHADER,fs));gl.linkProgram(prog);if(!gl.getProgramParameter(prog,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(prog));gl.useProgram(prog);
const aP=gl.getAttribLocation(prog,'aPosition'),aC=gl.getAttribLocation(prog,'aColor'),aN=gl.getAttribLocation(prog,'aNormal');
const loc={yaw:gl.getUniformLocation(prog,'uYaw'),pitch:gl.getUniformLocation(prog,'uPitch'),zoom:gl.getUniformLocation(prog,'uZoom'),aspect:gl.getUniformLocation(prog,'uAspect'),lit:gl.getUniformLocation(prog,'uLit')};
function mesh(raw,how,lit=false){let buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(raw),gl.STATIC_DRAW);return{buf,count:raw.length/9,how,lit}}
function emit(out,p,c,n=[0,0,1]){out.push(...p,...c,...n)}
function line(out,a,b,c){emit(out,a,c);emit(out,b,c)}
function arrow(out,a,vec,color,len=.24){let n=Math.hypot(...vec);if(n<1e-12)return;let b=a.map((v,i)=>v+vec[i]/n*len);line(out,a,b,color);const d=vec.map(v=>v/n),o=[-d[1],d[0],.2];let on=Math.hypot(...o);o=o.map(v=>v/on);let e=b.map((v,i)=>v-.07*d[i]);line(out,b,e.map((v,i)=>v+.035*o[i]),color);line(out,b,e.map((v,i)=>v-.035*o[i]),color)}
function sphere(){let out=[],m=64,n=36;const v=(j,i)=>{const lat=-Math.PI/2+Math.PI*j/n,lon=2*Math.PI*i/m;return [Math.cos(lat)*Math.cos(lon),Math.cos(lat)*Math.sin(lon),Math.sin(lat)]};
for(let j=0;j<n;j++)for(let i=0;i<m;i++){let a=v(j,i),b=v(j+1,i),c=v(j+1,i+1),d=v(j,i+1);
for(let p of [a,b,c,a,c,d]){let land=Math.sin(2.4*p[0]+4.7*p[1])+Math.sin(6*p[0]-3.5*p[2])*.55+Math.cos(5.8*p[1]+3*p[2])*.33;
let col=land>.48?[.11,.43,.30]:land>.15?[.08,.35,.43]:[.055,.18,.43];emit(out,p,col,p)}}return mesh(out,gl.TRIANGLES,true)}
function buildEarthLines(){let out=[],pi=Math.PI;for(let lat=-60;lat<=60;lat+=30){for(let i=0;i<180;i++){let lon=i*pi/90,ln2=(i+1)*pi/90,a=lat*pi/180;line(out,[1.01*Math.cos(a)*Math.cos(lon),1.01*Math.cos(a)*Math.sin(lon),1.01*Math.sin(a)],[1.01*Math.cos(a)*Math.cos(ln2),1.01*Math.cos(a)*Math.sin(ln2),1.01*Math.sin(a)],[.18,.35,.46])}}
for(let lon=0;lon<360;lon+=30){let a=lon*pi/180;for(let j=0;j<90;j++){let b=-pi/2+j*pi/90,c=-pi/2+(j+1)*pi/90;line(out,[1.012*Math.cos(b)*Math.cos(a),1.012*Math.cos(b)*Math.sin(a),1.012*Math.sin(b)],[1.012*Math.cos(c)*Math.cos(a),1.012*Math.cos(c)*Math.sin(a),1.012*Math.sin(c)],[.17,.31,.42])}}
for(let lat=-60;lat<=60;lat+=30)for(let lon=0;lon<360;lon+=60){let a=lat*pi/180,b=lon*pi/180,x=[Math.cos(a)*Math.cos(b),Math.cos(a)*Math.sin(b),Math.sin(a)],z=x[2];let s=x.map(v=>1.25*v);
arrow(out,s,x.map(v=>-v),[1,.32,.36],.20);let B=x.map((v,i)=>3*z*v-(i===2?1:0));arrow(out,s,B,[.33,.88,1],.23)}return mesh(out,gl.LINES)}
const sphereMesh=sphere(),earthLines=buildEarthLines();
function buildHelix(){
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

function renderMesh(obj){gl.uniform1i(loc.lit,obj.lit?1:0);gl.bindBuffer(gl.ARRAY_BUFFER,obj.buf);gl.enableVertexAttribArray(aP);gl.vertexAttribPointer(aP,3,gl.FLOAT,false,36,0);gl.enableVertexAttribArray(aC);gl.vertexAttribPointer(aC,3,gl.FLOAT,false,36,12);gl.enableVertexAttribArray(aN);gl.vertexAttribPointer(aN,3,gl.FLOAT,false,36,24);gl.drawArrays(obj.how,0,obj.count)}
let oldH=null,lastH='';
function paint(){frame++;if(spin&&!drag)yaw+=.0025;
let w=Math.max(1,Math.round(canvas.clientWidth*devicePixelRatio)),h=Math.max(1,Math.round(canvas.clientHeight*devicePixelRatio));if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;gl.viewport(0,0,w,h)}
gl.clearColor(.025,.049,.085,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);gl.depthFunc(gl.LEQUAL);gl.useProgram(prog);
gl.uniform1f(loc.yaw,yaw);gl.uniform1f(loc.pitch,pitch);gl.uniform1f(loc.zoom,zoom);gl.uniform1f(loc.aspect,w/h);
if(mode==='earth'){renderMesh(sphereMesh);renderMesh(earthLines)}else{let key=$('radius').value+','+$('angle').value;if(lastH!==key){if(oldH)gl.deleteBuffer(oldH.buf);oldH=buildHelix();lastH=key}renderMesh(oldH)}requestAnimationFrame(paint)}
requestAnimationFrame(paint);
}

if(!gl){
  const ctx=canvas.getContext('2d');
  $('legend').textContent='Canvas2D 备用渲染（浏览器未启用 WebGL2） · 拖拽旋转 · 滚轮缩放 · 地球与场线为近似模型，不代表真实实测。';
  function rot(p){let cy=Math.cos(yaw),sy=Math.sin(yaw),cx=Math.cos(pitch),sx=Math.sin(pitch);
    let q=[cy*p[0]+sy*p[2],p[1],-sy*p[0]+cy*p[2]];
    return [q[0],cx*q[1]-sx*q[2],sx*q[1]+cx*q[2]]}
  function proj(p,w,h){let q=rot(p),f=Math.min(w,h)*.32*zoom;
    return [w/2+q[0]*f*3.5/(4-q[2]),h/2-q[1]*f*3.5/(4-q[2]),q[2]]}
  function segment(a,b,color,width=1){let A=proj(a,canvas.width,canvas.height),B=proj(b,canvas.width,canvas.height);
    ctx.strokeStyle=color;ctx.lineWidth=width;ctx.beginPath();ctx.moveTo(A[0],A[1]);ctx.lineTo(B[0],B[1]);ctx.stroke()}
  function drawFallback(){if(spin&&!drag)yaw+=.0025;
    let dpr=devicePixelRatio||1,w=Math.round(canvas.clientWidth*dpr),h=Math.round(canvas.clientHeight*dpr);
    if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h}
    ctx.fillStyle='#081321';ctx.fillRect(0,0,w,h);
    if(mode==='earth'){
      let c=proj([0,0,0],w,h),rad=Math.min(w,h)*.32*zoom;
      let g=ctx.createRadialGradient(c[0]-rad*.3,c[1]-rad*.3,rad*.05,c[0],c[1],rad);
      g.addColorStop(0,'#276f87');g.addColorStop(.6,'#174665');g.addColorStop(1,'#081c3a');
      ctx.beginPath();ctx.arc(c[0],c[1],rad,0,2*Math.PI);ctx.fillStyle=g;ctx.fill();
      ctx.save();ctx.beginPath();ctx.arc(c[0],c[1],rad,0,2*Math.PI);ctx.clip();
      for(let lat=-60;lat<=60;lat+=30){let prev=null;
        for(let i=0;i<=120;i++){let lon=2*Math.PI*i/120,a=lat*Math.PI/180;
          let q=[Math.cos(a)*Math.cos(lon),Math.cos(a)*Math.sin(lon),Math.sin(a)];
          if(prev)segment(prev,q,'rgba(100,180,230,.32)',.8*dpr);prev=q}}
      for(let lon=0;lon<360;lon+=30){let prev=null;
        for(let j=0;j<=70;j++){let a=lon*Math.PI/180,b=-Math.PI/2+Math.PI*j/70;
          let q=[Math.cos(b)*Math.cos(a),Math.cos(b)*Math.sin(a),Math.sin(b)];
          if(prev)segment(prev,q,'rgba(100,180,230,.25)',.8*dpr);prev=q}}
      ctx.restore();
      for(let lat=-60;lat<=60;lat+=30)for(let lon=0;lon<360;lon+=60){
        let a=lat*Math.PI/180,b=lon*Math.PI/180,q=[Math.cos(a)*Math.cos(b),Math.cos(a)*Math.sin(b),Math.sin(a)];
        if(rot(q)[2]<0)continue;
        let origin=q.map(v=>v*1.17),gvec=q.map(v=>v*-.22),B=q.map((v,i)=>3*q[2]*v-(i===2?1:0)),mag=Math.hypot(...B)||1;
        segment(origin,origin.map((v,i)=>v+gvec[i]),'#ff626e',2*dpr);
        segment(origin,origin.map((v,i)=>v+B[i]/mag*.26),'#53ddeb',2*dpr);
      }
    }else{
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
    }
    requestAnimationFrame(drawFallback);
  }
  requestAnimationFrame(drawFallback);
}
