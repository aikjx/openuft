# -*- coding: utf-8 -*-
"""
S03-V18.8
任务：检验来稿 §7 缺口5 / §8 分支三的判据「正反费米子 = 左右手镜像扭结」——手性符号
      能否作为 GAQ 的粒子/反粒子标签。标准：V18.2 V2-d 要求拓扑标签必须【单射且单调】。

纯标准库（math / sys / os / io），Python 3.8+
红线：本册全部为可否证性裁定与自洽性检验，不含对 GAQ 主张的正面支持证据。
输出：07_计算复现/运行记录/S03_V18_8_镜像扭结粒子标签单射性判定报告.txt
"""
import sys, os, io, math
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
PI = math.pi
HERE = os.path.dirname(os.path.abspath(__file__))
LOGDIR = os.path.join(os.path.dirname(HERE), "运行记录")
REPORT = "S03_V18_8_镜像扭结粒子标签单射性判定报告.txt"

LINES = []; COUNTS = {"PASS":0,"FAIL":0,"BOUNDARY":0,"INFO":0,"CORRECTED":0}; ITEMS = []
def emit(t=""): LINES.append(t)
def rec(c,v,t): COUNTS[v]+=1; ITEMS.append((c,v,t)); emit("[%s] %s  %s"%(v,c,t))
def P(c,t): rec(c,"PASS",t)
def F(c,t): rec(c,"FAIL",t)
def B(c,t): rec(c,"BOUNDARY",t)
def I(c,t): rec(c,"INFO",t)
def table(h,rows):
    w=[len(x) for x in h]
    for r in rows:
        for k in range(len(h)): w[k]=max(w[k],len(str(r[k])))
    f=" | ".join("{:<%d}"%x for x in w)
    emit("  "+f.format(*h)); emit("  "+"-+-".join("-"*x for x in w))
    for r in rows: emit("  "+f.format(*[str(x) for x in r]))
def vsub(a,b): return (a[0]-b[0],a[1]-b[1],a[2]-b[2])
def vadd(a,b): return (a[0]+b[0],a[1]+b[1],a[2]+b[2])
def vsc(a,s): return (a[0]*s,a[1]*s,a[2]*s)
def vdot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def vcross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def vnorm(a): return math.sqrt(vdot(a,a))
def vunit(a):
    n=vnorm(a); return (a[0]/n,a[1]/n,a[2]/n)
def vmid(a,b): return ((a[0]+b[0])*0.5,(a[1]+b[1])*0.5,(a[2]+b[2])*0.5)

def gauss_writhe(P, skip=1):
    n=len(P); r1=[vmid(P[i],P[(i+1)%n]) for i in range(n)]
    d1=[vsub(P[(i+1)%n],P[i]) for i in range(n)]; acc=0.0
    for i in range(n):
        ri=r1[i]; di=d1[i]
        for j in range(n):
            g=min(abs(i-j),n-abs(i-j))
            if g<=skip: continue
            d=vsub(ri,r1[j]); nd=vnorm(d)
            acc+=vdot(d,vcross(di,d1[j]))/(nd*nd*nd)
    return acc/(4.0*PI)

def torus_knot(p,q,N):
    return [((2.0+math.cos(q*t))*math.cos(p*t),
             (2.0+math.cos(q*t))*math.sin(p*t),
             math.sin(q*t)) for t in [2.0*PI*k/N for k in range(N)]]
def mirror_z(P): return [(x,y,-z) for (x,y,z) in P]
def circle(N=240): return [(math.cos(2*PI*k/N),math.sin(2*PI*k/N),0.0) for k in range(N)]
def circle_with_kink(R=1.0,N=260,rk=0.15,M=40):
    base=[(R*math.cos(2*PI*k/N),R*math.sin(2*PI*k/N),0.0) for k in range(N)]
    idx=N//4; pp=base[(idx-1)%N]; p0=base[idx]; pn=base[(idx+1)%N]
    T=vunit(vsub(pn,pp)); rad=vunit(vsc(p0,-1.0)); B=vunit(vcross(T,rad))
    loop=[vadd(p0,vadd(vsc(rad,rk*math.cos(2*PI*s/M)),vsc(B,rk*math.sin(2*PI*s/M)))) for s in range(M)]
    return base[:idx]+loop+base[idx+1:]

CHECKS=[]
def check(nm,ok,det): CHECKS.append((nm,bool(ok),det)); emit("  [SC %s] %s :: %s"%("OK" if ok else "NG",nm,det))

emit("="*78)
emit("S03-V18.8  镜像扭结作为粒子/反粒子标签的单射性判定")
emit("           承接 S03-V6 §7 缺口5 / §8 分支三；标准 S03-V2 V2-d（标签须单射且单调）")
emit("="*78)
emit("")
emit("红线：本册全部为可否证性裁定。PASS 仅表示『标准数学事实被独立复算』，不构成对 GAQ 的物理验证。")
emit("")

emit("-"*78); emit("第 0 节  验证器"); emit("-"*78)
wc=gauss_writhe(circle(240),1)
check("SC1 平面圆（unknot）Writhe = 0", abs(wc)<1e-3, "Wr = %.3e"%wc)
emit("")
emit("-"*78); emit("第 1 节  Writhe 不是拓扑不变量（V8-b）"); emit("-"*78)
emit("")
emit("  来稿若以『Wr 符号』当手性标签，则标签依赖空间嵌入而非拓扑类型——")
emit("  同一拓扑类型的曲线可有不同 Wr。Reidemeister I 移动不改变纽结类型却改变 Wr。")
emit("")
kink=circle_with_kink()
wk=gauss_writhe(kink,1)
emit("  构造：在 unknot 上插入一个 R1 小结（kink）。按 R1 不变性，纽结类型仍为 unknot。")
table(["构型","Writhe","纽结类型"],
      [("plain circle","%.6f"%wc,"unknot"),
       ("circle + 一个 R1 kink","%.6f"%wk,"unknot（R1 不变）")])
check("SC2 同一 unknot 的两种嵌入 Wr 不同 ⇒ Writhe 非拓扑不变量",
      abs(wk)>0.1 and abs(wc)<1e-3, "ΔWr = %.6f"%abs(wk))
emit("")
F("V8-b","若 GAQ 以 Wr 符号作粒子标签，则同一粒子（同纽结类型）在不同嵌入下得不同标签 ⇒ 物理上不一致")
emit("      必须用【手性 chirality】（拓扑量，2 值）而非 Wr 符号。但见第 2、3 节：手性也只有 2 值。")
emit("")

emit("-"*78); emit("第 2 节  镜像操作区分粒子/反粒子——窄域成立（V8-e）"); emit("-"*78)
t3=torus_knot(2,3,400); t3m=mirror_z(t3)
wr3=gauss_writhe(t3,1); wr3m=gauss_writhe(t3m,1)
t5=torus_knot(2,5,400); t5m=mirror_z(t5)
wr5=gauss_writhe(t5,1); wr5m=gauss_writhe(t5m,1)
table(["构型","Writhe","镜像 Writhe","和"],
      [("(2,3) torus knot (3_1)","%.6f"%wr3,"%.6f"%wr3m,"%.3e"%(wr3+wr3m)),
       ("(2,5) torus knot (5_1)","%.6f"%wr5,"%.6f"%wr5m,"%.3e"%(wr5+wr5m))])
check("SC3 (2,3) 镜像 Wr 严格反号", abs(wr3+wr3m)<0.02*abs(wr3) and wr3*wr3m<0,
      "Wr=%.6f, Wr_m=%.6f"%(wr3,wr3m))
check("SC4 (2,5) 镜像 Wr 严格反号", abs(wr5+wr5m)<0.02*abs(wr5) and wr5*wr5m<0,
      "Wr=%.6f, Wr_m=%.6f"%(wr5,wr5m))
emit("")
P("V8-e","镜像操作对【单一】手性纽结正确区分粒子与其反粒子（e⁻ 与 e⁺）")
emit("      （窄域成立：固定的 chiral 纽结，镜像给出相反的 Wr 符号）")
emit("")

emit("-"*78); emit("第 3 节  手性标签的承载容量：单射性与单调性（V8-a / V8-d）"); emit("-"*78)
emit("")
emit("  手性（chirality）作为拓扑量只有 2 个取值：chiral / achiral；或等价地，")
emit("  对固定嵌入的 Wr 符号：−1 / +1 / 0。一个 2 值标签至多区分 2 个拓扑类。")
emit("")
leptons=[("e⁻",-1),("μ⁻",-1),("τ⁻",-1),("ν_e",-1),("ν_μ",-1),("ν_τ",-1),
         ("e⁺",+1),("μ⁺",+1),("τ⁺",+1),("ν̄_e",+1),("ν̄_μ",+1),("ν̄_τ",+1)]
charged=[("e⁻",-1),("μ⁻",-1),("τ⁻",-1),("e⁺",+1),("μ⁺",+1),("τ⁺",+1)]
emit("  SM 费米子物种数（含反粒子、三代、三色夸克）= 48；仅带电轻子+反粒子 = %d。"%len(charged))
emit("  若以手性符号（2 值）为标签：")
table(["费米子","手性符号","是否被区分"],
      [("e⁻ / μ⁻ / τ⁻","−1","三者同标签 ⇒ 混淆"),
       ("ν_e / ν_μ / ν_τ","−1","与带电轻子同标签 ⇒ 混淆"),
       ("e⁺ / μ⁺ / τ⁺","+1","三者同标签 ⇒ 混淆")])
emit("")
nlabels=2
check("SC5 2 值标签无法单射区分 >2 个费米子物种",
      len(leptons)>nlabels, "费米子种数 %d > 标签容量 %d"%(len(leptons),nlabels))
check("SC6 2 值标签无法给出代际质量序（单调）",
      len(charged)>=3, "带电轻子 3 代需 ≥3 标签，±1 无法排序 e<μ<τ")
emit("")
F("V8-a","手性/镜像标签至多 2 值 ⇒ 不能单射区分多物种费米子 sector（违反 V2-d 单射性）")
F("V8-d","手性符号 ∈ {±1} 无法承载代际/质量层次 e<μ<τ（违反 V2-d 单调性）")
emit("")
B("V8-c","基底纽结必须本身 chiral；若选 amphichiral 纽结则镜像=自身 ⇒ e⁻=e⁺（无反粒子），错误。")
emit("      GAQ 未指定『取哪个 chiral 纽结』⇒ 自由参数；且不同 chiral 纽结（3_1、5_1）均落入同一『chiral』标签，")
emit("      故即使限定 chiral，仍不能区分代际（SC4：3_1 与 5_1 的 Wr 同为符号 −）。")
emit("")
I("V8-f","GAQ 仍未给出轻子味 / 中微子 / 电荷的独立拓扑标签（承接 V18.6 §7 缺口1、2）。")
emit("      手性标签只解决『粒子 vs 反粒子』这一对，对 SM 其余自由度无能为力。")
emit("")

emit("="*78); emit("汇总"); emit("="*78)
for c,v,t in ITEMS: emit("  [%-9s] %-7s %s"%(v,c,t))
emit("")
emit("条目合计 %d"%len(ITEMS))
for k in ("PASS","FAIL","BOUNDARY","INFO"): emit("%s = %d"%(k,COUNTS[k]))
emit("")
emit("自检：")
nok=sum(1 for _,ok,_ in CHECKS if ok)
for nm,ok,det in CHECKS: emit("  [%s] %s :: %s"%("OK" if ok else "NG",nm,det))
emit("自检 %d/%d"%(nok,len(CHECKS)))
emit("")
emit("红线复述：")
emit("  1. 本册 FAIL 均为与 V2-d（单射+单调）标准及拓扑不变性事实的冲突，非对 GAQ 全部内容的否定。")
emit("  2. V8-e 的 PASS 是『镜像区分粒子对』这一窄域数学事实的复算，不构成对 GAQ 的物理验证。")
emit("  3. 本册未对任何物理预言做正面验证。")
emit("")
ok_all=(nok==len(CHECKS)) and len(CHECKS)>=6
text="\n".join(LINES)+"\n"
if not os.path.isdir(LOGDIR): os.makedirs(LOGDIR)
with io.open(os.path.join(LOGDIR,REPORT),"w",encoding="utf-8") as fh: fh.write(text)
print(text); print("报告已写入:",os.path.join(LOGDIR,REPORT)); print("自检 %d/%d"%(nok,len(CHECKS)))
sys.exit(0 if ok_all else 1)
