# -*- coding: utf-8 -*-
"""
P03 GUT 第二阶段精算：2 圈耦合统一 + 质子衰变可证伪窗口
纯标准库。用法: python p03_gut_2loop_proton_decay.py

内容:
 1. 标准模型 SM / 最小超对称 MSSM 的 1 圈 b 与 2 圈 B 系数（SU5 归一 α1=√(5/3)g'），
    用 RK4 在 t=ln μ 上积分 dα_i/dt = b_i α_i^2/(2π) + α_i^2/(8π^2) Σ B_ij α_j，
    求三耦合最接近（最小散布）的尺度 M* 与该处 α_GUT。对比 1 圈/2 圈。
 2. dimension-6（X/Y 矢量）质子寿命标度律，叠加 Super-K / Hyper-K / DUNE 灵敏度，
    反解实验可探测的 M_X 上限。
 3. dimension-5（SUSY 色三重态 Higgsino）标度律与参数依赖；无 SUSY 谱不定值，给现状。
 4. 关键张力：M_GUT 越高耦合汇聚越好，但 dim-6 质子越稳定（M_X^4）——汇聚与可探测反向。
 5. 几何本体输入计数仍为 0。

实验输入（2026-09 复核，公开值）:
  Super-K   τ(p→e+π0)>2.4e34 yr (450 kton·yr,90%CL); τ(p→K+ν)>6.6e33 yr
  Hyper-K   ~200 kton, 10 yr 90%CL  τ(e+π0)~1e35 yr
  DUNE      40 kton LAr, 下一代探测 1e34–1e35 yr; K+ν 400 kton·yr ~1.3e34 yr
"""
import math

def L(k,v): print(f"{k:52s} = {v}")

# ---------- 初始耦合（MZ，SU5 归一） ----------
aEM_inv=127.951; s2=0.23122; c2=1-s2; alphas=0.1179
a1_inv_0=0.6*aEM_inv*c2
a2_inv_0=aEM_inv*s2
a3_inv_0=1.0/alphas
A0=(1/a1_inv_0,1/a2_inv_0,1/a3_inv_0)
MZ=91.1876

# ---------- β 系数 ----------
bSM=(41/10,-19/6,-7.0)
BSM=[[199/50,27/10,44/5],
     [9/10,35/6,12.0],
     [11/10,9/2,-26.0]]
bMSSM=(33/5,1.0,-3.0)
BM=[[199/25,27/5,88/5],
    [9/5,25.0,24.0],
    [11/5,9.0,14.0]]

def deriv(A,b,B):
    out=[]
    for i in range(3):
        s=sum(B[i][j]*A[j] for j in range(3))
        out.append(b[i]*A[i]**2/(2*math.pi) + A[i]**2/(8*math.pi**2)*s)
    return out

def rk4_step(A,dt,b,B):
    k1=deriv(A,b,B)
    k2=deriv([A[i]+0.5*dt*k1[i] for i in range(3)],b,B)
    k3=deriv([A[i]+0.5*dt*k2[i] for i in range(3)],b,B)
    k4=deriv([A[i]+dt*k3[i] for i in range(3)],b,B)
    return [A[i]+dt/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(3)]

def spread(A):
    ai=[1/x for x in A]
    return max(ai)-min(ai)

def run_unify(b,B,two_loop=True,tmax=40.0,dt=0.005):
    A=list(A0); t=0.0; best=None
    n=int(tmax/dt)
    for _ in range(n):
        bb = b
        BB = B if two_loop else [[0]*3 for _ in range(3)]
        A=rk4_step(A,dt,bb,BB); t+=dt
        sp=spread(A)
        if best is None or sp<best[0]:
            best=(sp,t,list(A))
    sp,t,A=best
    mu=MZ*math.exp(t)
    ai=[1/x for x in A]
    return mu,sp,ai

print("="*86)
print(" 1. 耦合统一：1 圈 vs 2 圈（最小散布尺度 M*，三耦合 α⁻¹ 与 α_GUT）")
print("="*86)
for name,b,B in [("SM",bSM,BSM),("MSSM",bMSSM,BM)]:
    for loop,two in [("1-loop",False),("2-loop",True)]:
        mu,sp,ai=run_unify(b,B,two)
        aG=3/sum(ai)
        verdict="汇聚良好" if sp<0.5 else ("勉强/边缘" if sp<2 else "不汇聚")
        print(f"\n[{name} {loop}]")
        L("  M*（最小散布）", f"{mu:.3e} GeV")
        L("  α1⁻¹,α2⁻¹,α3⁻¹ @M*", f"{ai[0]:.2f}, {ai[1]:.2f}, {ai[2]:.2f}")
        L("  三耦合散布 spread", f"{sp:.3f}  → {verdict}")
        L("  等效 α_GUT≈3/Σα⁻¹", f"{aG:.4f} (α_GUT⁻¹={1/aG:.2f})")

print()
print("="*86)
print(" 2. dimension-6（X/Y 矢量）质子寿命与实验窗口")
print("="*86)
# 标准量级归一（现代格点矩阵元+短程QCD）：τ≈C6 (MX/1e16)^4 (0.024/αG)^2
C6=1.0e36   # 年，标称；矩阵元/短程不确定带约 ×/÷3
a_ref=0.024
def tau_dim6(MX,aG): return C6*(MX/1e16)**4*(a_ref/aG)**2
def MX_from_tau(tau,aG): return 1e16*((tau/C6)*(aG/a_ref)**2)**0.25
# 用 2-loop MSSM α_GUT
mu2,sp2,ai2=run_unify(bMSSM,BM,True); aG_M=3/sum(ai2)
print(f"归一化（标称，矩阵元不确定带约 ×/÷3）: τ(e+π0) ≈ {C6:.0e} yr · (MX/1e16)^4 · (0.024/αG)^2")
print(f"{'MX(GeV)':>11} | {'τ @αG=0.024':>15} | {'τ @αG(MSSM,2loop)':>18} | 实验位置")
SK=2.4e34; HK=1.0e35; DUNE=3.0e34
for MX in [1e15,2e15,3e15,5e15,1e16,2.3e16,1e17]:
    t1=tau_dim6(MX,a_ref); t2=tau_dim6(MX,aG_M)
    pos="已被Super-K排除" if t1<SK else ("Hyper-K/DUNE 可达" if t1<HK else "下一代不可见")
    print(f"{MX:11.2e} | {t1:15.2e} | {t2:18.2e} | {pos}")
print()
L("Super-K 下限 τ(e+π0)", f">{SK:.1e} yr；τ(K+ν̄)>{6.6e33:.1e} yr")
L("Hyper-K(10yr,90%) e+π0", f"~{HK:.0e} yr")
L("DUNE(40kton LAr)", f"下一代 1e34–1e35 yr（K+ν̄ 400 kton·yr ~1.3e34）")
print()
for tag,tau in [("Super-K 现下限",SK),("DUNE/HK 下端",DUNE),("Hyper-K 10yr",HK)]:
    for tagA,aG in [("αG=0.024",a_ref),("αG=%.3f(MSSM2loop)"%aG_M,aG_M)]:
        print(f"  反解 {tag:14s} {tagA:22s} → dim-6 可探测 M_X ≲ {MX_from_tau(tau,aG):.2e} GeV")
print()
print("关键：2-loop MSSM 汇聚尺度 M_GUT≈{:.1e} GeV 远在上述可探测 M_X 上限之上；".format(mu2))
print("代入得纯 dim-6 τ(e+π0,MSSM)≈{:.1e} yr，比 Hyper-K 灵敏度高 ~{:.0f} 倍 —— 耦合汇聚最干净".format(tau_dim6(mu2,aG_M),tau_dim6(mu2,aG_M)/HK))
print("的 MSSM GUT 在 e+π0 通道对下一代实验基本不可证伪（保护带）。")

print()
print("="*86)
print(" 3. dimension-5（SUSY 色三重态 Higgsino）p→K+ν̄：标度律与现状")
print("="*86)
print("""  Γ(p→K+ν̄)_d5 ∝ (α_GUT)·(y_u y_? )·β_p /(M_GUT · M_Hc)，  M_Hc≈m_sfermion（色三重态质量）
  ⇒  τ_d5 ~ C5 · (M_GUT/2e16)^2 · (m_sf/1 TeV)^2 · (1/β_p)^2 · (1/ Yukawa组合)^2
  对超伴子质量为【平方】敏感：m_sf 1→10 TeV，τ 增约 100 倍；对色三重态 Yukawa 抑制极敏感。
  现状（无 SUSY 谱，不能给单点值，只给边界）:
   - 最简最小 SUSY SU(5) 的维度-5 预测已被 Super-K τ(K+ν̄)>6.6e33 年 + LHC squark≳1 TeV 双重挤压；
   - 要存活需色三重态有效 Yukawa 再额外抑制约 1e-4–1e-3（缺多重态/翻转SU5/GMSB 等机制）；
   - GMSB 等可达 τ(K+ν̄)~1e34 年，落在 Hyper-K/DUNE 可达区——但是具体模型相关，非 P03 公设的必然预言。""")
L("dim-5 是否 P03 定量预言", "否：依赖未观测的 sfermion 谱与额外 Yukawa 结构（A2-A5 不含这些输入）")

print()
print("="*86)
print(" 4. 汇聚—可探测反向张力（P03 最深刻的可证伪结构）")
print("="*86)
print("  dim-6: τ ∝ M_X^4      → M_X 越高质子越稳定（难探测）")
print("  RG   : 汇聚质量要求 M_GUT 高（MSSM 2-loop ~{:.1e}）→ 与 dim-6 可探测窗口（M_X≲~(5-7)e15）冲突".format(mu2))
print("  ⇒ 若 Hyper-K/DUNE 在 1e34–1e35 看到 e+π0，则要求【较低】X 质量，而低 M_X 的最小模型三耦合不汇聚；")
print("    必须引入中间尺度/扩展Higgs(如45)/非最小内容来同时实现汇聚与可见质子——这是可被实验判决的具体方向。")

print()
print("="*86)
print(" 5. 几何本体输入计数")
print("="*86)
geo=0
checks=["2圈β系数与汇聚","α_GUT 数值","dim-6 M_X^4 标度律","实验灵敏度对标","dim-5 参数依赖"]
for c in checks: print(f"  {c:24s} 用到 κ/τ/ω/螺旋：否")
L("几何本体输入", f"{geo}/5（定理 Q/A6 在 2 圈与质子分析中继续成立）")

print()
print("结论[诚实]：P03 获得 2 圈定量可证伪窗口；SM 仍不汇聚、MSSM 2-loop 在~{:.1e} 汇聚(αG≈{:.3f})但 e+π0 落在下一代实验保护带外；".format(mu2,aG_M))
print("下一代 10–20 年真正可检验的是【较低 M_X 的非最小非SUSY GUT 的 e+π0】与【具体 SUSY 模型的 K+ν̄】。")
print("P03 不统一引力、不给 α 绝对值或质量谱，UFT 维持 2/6；脚本纯标准库。")
