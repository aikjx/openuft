# -*- coding: utf-8 -*-
"""
P03 GUT 第三阶段：阈值修正 vs 质子可探测 两难精算
纯标准库。用法: python p03_gut_threshold_tension.py

问题：dim-6 质子可见要求 M_X 低（Hyper-K 上界 ~5.6e15），但 2 圈良好汇聚在高尺度
（MSSM ~2e16，SM 不汇聚）。能否用 GUT 阈值修正把汇聚"搬"到质子可见的低尺度？代价多大？

方法：
 - 2 圈 RK4 跑 α_i 到任意 M，读裸倒数 a_i(M)=α_i^{-1,run}(M)。
 - 阈值：α_i^{-1,phys}(M)=a_i(M)+Δ_i，Δ_i=-(1/2π)Σ_R b_i^R ln(m_R/M)。
   物理汇聚 a_i+Δ_i=const 所需阈值差：Δ_i-Δ_j = a_j-a_i（α^-1 单位）。
 - 单个重表示 R 贡献 (Δb_ij^R/2π)ln r_R；取净系数 c_eff=|Δb|∈{0.3,0.5,1.0}，
   等效单一质量等级 r*=exp(2π D_max/c_eff)，D_max=max 相邻 a 差。
 - 同时算 dim-6 τ(e+π0)。扫描 M=1e13..1e17，求【质子可见 τ<1e35】与【自然阈值 r*<100】交集。
"""
import math
def L(k,v): print(f"{k:48s} = {v}")

aEM_inv=127.951; s2=0.23122; c2=1-s2; alphas=0.1179
A0=(1/(0.6*aEM_inv*c2),1/(aEM_inv*s2),1/(1.0/alphas))
MZ=91.1876
bSM=(41/10,-19/6,-7.0); BSM=[[199/50,27/10,44/5],[9/10,35/6,12.0],[11/10,9/2,-26.0]]
bM=(33/5,1.0,-3.0);    BM=[[199/25,27/5,88/5],[9/5,25.0,24.0],[11/5,9.0,14.0]]

def deriv(A,b,B):
    return [b[i]*A[i]**2/(2*math.pi)+A[i]**2/(8*math.pi**2)*sum(B[i][j]*A[j] for j in range(3)) for i in range(3)]
def rk4(A,dt,b,B):
    k1=deriv(A,b,B); k2=deriv([A[i]+.5*dt*k1[i] for i in range(3)],b,B)
    k3=deriv([A[i]+.5*dt*k2[i] for i in range(3)],b,B); k4=deriv([A[i]+dt*k3[i] for i in range(3)],b,B)
    return [A[i]+dt/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(3)]

def trajectory(b,B,tmax=math.log(1e17/MZ),dt=0.01):
    A=list(A0); t=0.0; pts=[(MZ,list(A))]; n=int(tmax/dt)
    for _ in range(n):
        A=rk4(A,dt,b,B); t+=dt; pts.append((MZ*math.exp(t),list(A)))
    return pts
def at_M(pts,M):
    # 线性插值取 α_i^{-1}
    for k in range(len(pts)-1):
        m0,Aa=pts[k]; m1,Ab=pts[k+1]
        if m0<=M<=m1:
            import math as _m
            f=(_m.log(M/m0))/_m.log(m1/m0) if m1>m0 else 0
            ai=[1/(Aa[i]+f*(Ab[i]-Aa[i])) for i in range(3)]
            return ai
    return [1/x for x in pts[-1][1]]

def Dmax(ai):  # 相邻 α^-1 差的最大
    return max(abs(ai[0]-ai[1]),abs(ai[1]-ai[2]),abs(ai[0]-ai[2]))
def rstar(D,c): return math.exp(2*math.pi*D/c)
def tau_dim6(M,ainv_common,a_ref_inv=1/0.024,C6=1e36):
    aG=1/ainv_common
    return C6*(M/1e16)**4*(0.024/aG)**2

ptsSM=trajectory(bSM,BSM); ptsM=trajectory(bM,BM)
HK=1.0e35; SK=2.4e34

for name,pts in [("SM (2-loop,1H)",ptsSM),("MSSM (2-loop)",ptsM)]:
    print("="*92)
    print(f" {name}：尺度 M 上 2圈裸 α⁻¹ / 所需阈值差 D / 等效质量分裂 r*(c=0.5) / dim-6 质子寿命")
    print("="*92)
    print(f"{'log10 M':>8} | {'a1':>7}{'a2':>7}{'a3':>7} | {'Dmax':>6} | {'r*(.3)':>9}{'r*(.5)':>9}{'r*(1)':>9} | {'τ(eπ)yr':>11} | 判定")
    rows=[]
    for le in [13.0,13.5,14.0,14.5,15.0,15.3,15.6,15.75,16.0,16.3,16.7,17.0]:
        M=10**le; ai=at_M(pts,M); D=Dmax(ai); ac=sum(ai)/3
        t=tau_dim6(M,ac)
        r3,r5,r1=rstar(D,.3),rstar(D,.5),rstar(D,1.0)
        rows.append((M,ai,D,(r3,r5,r1),t))
        nat = "自然" if r5<100 else ("边缘" if r5<1e3 else ("精调" if r5<1e6 else "极端"))
        vis = "可见(HK)" if t<HK else ("SK外" if t<SK else "不可见")
        print(f"{le:8.2f} | {ai[0]:7.2f}{ai[1]:7.2f}{ai[2]:7.2f} | {D:6.2f} | {r3:9.1e}{r5:9.1e}{r1:9.1e} | {t:11.2e} | {nat}/{vis}")

    print()
    # 交集扫描（细网格）
    fine=[]
    le=12.5
    while le<=17.2:
        M=10**le; ai=at_M(pts,M); D=Dmax(ai); ac=sum(ai)/3
        t=tau_dim6(M,ac); r5=rstar(D,.5); r3=rstar(D,.3)
        fine.append((le,M,D,r5,r3,t)); le+=0.02
    vis_nat=[x for x in fine if x[5]<HK and x[3]<100]      # 可见 & 自然(c=.5)
    vis_edge=[x for x in fine if x[5]<HK and x[3]<1e3]     # 可见 & 边缘
    if vis_nat:
        x=min(vis_nat,key=lambda z:z[3]); L("【可见τ<HK 且 自然r*<100】交集", f"存在：logM={x[0]:.2f}, r*={x[3]:.1e}, τ={x[5]:.1e}")
    else:
        L("【可见τ<HK 且 自然r*<100】交集", "空——二者不可兼得")
    if vis_edge:
        x=min(vis_edge,key=lambda z:z[3]); L("【可见 且 r*<1e3】交集", f"存在：logM={x[0]:.2f}, r*={x[3]:.1e}, τ={x[5]:.1e}")
    else:
        L("【可见 且 r*<1e3】交集", "空")
    # 在 HK 上界 5.6e15 处的最小阈值代价
    Mhk=5.6e15; ai=at_M(pts,Mhk); D=Dmax(ai)
    L(f"Hyper-K 上界 M=5.6e15 处裸 α⁻¹", f"{ai[0]:.2f},{ai[1]:.2f},{ai[2]:.2f}")
    L(f"  所需阈值差 Dmax", f"{D:.2f} (α⁻¹)")
    for c in (.3,.5,1.0):
        L(f"  等效质量分裂 r* (c={c})", f"{rstar(D,c):.2e}")
    # 自然汇聚点（r* 最小）
    best=min(fine,key=lambda z:z[3])
    L("最自然汇聚点 (r*(.5)最小)", f"logM={best[0]:.2f} (M={best[1]:.2e}), r*={best[3]:.1e}, D={best[2]:.2f}, τ={best[5]:.2e} yr")
    print()

print("="*92)
print(" 两难裁决与物理含义")
print("="*92)
print(""" dim-6 可见 ⇒ M_X ≲ 5.6×10^15（Hyper-K）。在该尺度：
   · SM 2圈裸 α⁻¹ 三耦合相差数单位，要阈值补齐需重表示质量等级 r* 达 10^6–10^17（极端精调）；
   · MSSM 2圈在可见尺度同样远离汇聚点，所需 r* 仍远超自然带（见上表）。
 自然汇聚（r*<100，重场在统一点 ~1/30–30 倍内）只发生在高尺度 M~2×10^16，那里 τ(eπ)~10^36–37，不可见。
 ⇒ 【质子下一代可见】与【无极端阈值的耦合汇聚】在 P03 公设 A1–A6 + 标准2圈RG 内【不可兼得】。
 要同时满足，必须引入 A1–A6 之外的新中介尺度物理（额外完整表示族/中间统一群/非最小破缺），
 那本身是新自由度、新精细调节来源——是可被 Hyper-K/DUNE 间接判决的具体模型方向，不是白来的统一。
 几何本体输入仍为 0（阈值系数来自内部表示的 Δb，与 κ/τ/ω 无关）；UFT 维持 2/6。""")
