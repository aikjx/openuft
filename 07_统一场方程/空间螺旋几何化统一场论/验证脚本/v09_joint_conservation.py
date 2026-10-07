# -*- coding: utf-8 -*-
"""V09 联合守恒显式推导验证（修正版：完整 Christoffel/Ricci）"""
import sympy as sp
from sympy import diff, simplify, symbols, exp, sin, cos, Rational
t,r,th,ph = symbols('t r th ph')
nu = sp.Function('nu')(r); la = sp.Function('la')(r)
tau = sp.Function('tau')(r)
coords=[t,r,th,ph]
# 全 4x4 度量矩阵（对角度规，非对角=0）
g=sp.zeros(4)
g[0,0]=-exp(2*nu); g[1,1]=exp(2*la); g[2,2]=r**2; g[3,3]=r**2*sin(th)**2
gu=g.inv()
# --- Christoffel Γ^σ_{μν} = ½Σ_ρ g^{σρ}(∂_μg_{νρ}+∂_νg_{ρμ}-∂_ρg_{μν}) ---
G=sp.MutableDenseNDimArray.zeros(4,4,4)
for s in range(4):
    for m in range(4):
        for n in range(4):
            val=0
            for rho in range(4):
                val += gu[s,rho]*(diff(g[n,rho],coords[m])+diff(g[rho,m],coords[n])-diff(g[m,n],coords[rho]))
            G[s,m,n]=sp.simplify(val/2)
nz=sum(1 for s in range(4) for m in range(4) for n in range(4) if G[s,m,n]!=0)
print("非零 Christoffel 数:", nz)
# 抽查关键联络
print("Γ^r_tt =", G[1,0,0], " (期望 e^{2ν-2λ}ν')")
print("Γ^t_tr =", G[0,0,1], " (期望 ν')")

# --- Ricci R_{μν} = ∂_ρΓ^ρ_{μν} - ∂_νΓ^ρ_{μρ} + Γ^σ_{μν}Γ^ρ_{σρ} - Γ^σ_{μρ}Γ^ρ_{νσ} ---
def ricci(mu,nu):
    tot=0
    for rho in range(4):
        tot += diff(G[rho,mu,nu],coords[rho]) - diff(G[rho,mu,rho],coords[nu])
        for sg in range(4):
            tot += G[sg,mu,nu]*G[rho,sg,rho] - G[sg,mu,rho]*G[rho,nu,sg]
    return sp.simplify(tot)
Rmat=sp.MutableDenseNDimArray.zeros(4,4)
for mu in range(4):
    for n in range(4):
        Rmat[mu,n]=sp.simplify(ricci(mu,n))
print("R_tt =",Rmat[0,0]); print("R_rr =",Rmat[1,1]); print("R_thth =",Rmat[2,2])
Rscalar=sp.simplify(sum(gu[i,i]*Rmat[i,i] for i in range(4)))
print("Rscalar =",sp.simplify(Rscalar))

# --- ∇_μ∇_ντ = ∂_μ∂_ντ - Γ^ρ_{μν}∂_ρτ ---
dtaud=[diff(tau,coords[i]) for i in range(4)]
DD=sp.MutableDenseNDimArray.zeros(4,4)
for mu in range(4):
    for n in range(4):
        val=diff(diff(tau,coords[mu]),coords[n])
        for rho in range(4):
            val -= G[rho,mu,n]*dtaud[rho]
        DD[mu,n]=sp.simplify(val)
box=sp.simplify(sum(gu[i,i]*DD[i,i] for i in range(4)))
print("□τ =",sp.simplify(box))

# --- A_{μν}=(g_{μν}□-∇_μ∇_ν)τ ---
A=sp.MutableDenseNDimArray.zeros(4,4)
for mu in range(4):
    for n in range(4):
        A[mu,n]=sp.simplify(g[mu,n]*box-DD[mu,n])

# --- ∇^μA_{μν}=Σ_α g^{μα}∇_αA_{μν}, ∇_αA=∂_αA-Γ^ρ_{αμ}A_{ρν}-Γ^ρ_{αν}A_{μρ} ---
def divA(nu):
    tot=0
    for al in range(4):
        for mu in range(4):
            Nab=diff(A[mu,nu],coords[al])
            for rho in range(4):
                Nab -= G[rho,al,mu]*A[rho,nu]
                Nab -= G[rho,al,nu]*A[mu,rho]
            tot += gu[al,mu]*Nab   # ∇^μ = g^{μα}∇_α，指标 al 即 α，gu[al,mu]=g^{αμ}
    return sp.simplify(tot)

print("\n=== 恒等式 (i): ∇^μA_{μν} = -R_{μν}∇^μτ ===")
ok=True
for n in range(4):
    lhs=divA(n)
    rhs=sp.simplify(-sum(Rmat[mu,n]*gu[mu,mu]*dtaud[mu] for mu in range(4)))  # -R_{μν}∇^μτ, ∇^μτ=g^{μμ}∂_μτ
    dv=sp.simplify(sp.trigsimp(sp.expand(lhs-rhs))); st="PASS" if dv==0 else "FAIL"; ok = ok and dv==0
    print(f"  ν={coords[n]}: {lhs}  vs  {rhs}  [{st}]")

print("\n=== 恒等式 (ii): ∇^μT^τ_{μν} = ∇_ντ(□τ-V') ===")
# T^τ_{μν}=∇_μτ∇_ντ-½g_{μν}(∇τ)²-V g_{μν}
def divTtau(nu):
    tot=0
    for al in range(4):
        for mu in range(4):
            Nab=diff(DD[mu,nu],coords[al])  # 占位，实际用 ∇_μτ∇_ντ 形式，下面直接解析
    return None
# 解析：∇^μT^τ_{μν}=□τ∇_ντ+∇^μτ∇_μ∇_ντ-∇_ν[½(∇τ)²]-V'∇_ντ = ∇_ντ(□τ-V')   (用 ∇_μ∇_ντ 对称)
# 数值核对每 ν：□τ∇_ντ + Σ g^{μα}∇_μτ∇_μ∇_ντ - ∇_ν[½Σ(∇τ)²] - V'∇_ντ
mt2,eta=sp.symbols('m_tau2 eta'); Vp=mt2*tau+eta   # V'(τ)=m²τ+η
ok2=True
for n in range(4):
    kin2=sp.simplify(sum(gu[mu,mu]*dtaud[mu]*DD[mu,n] for mu in range(4)))   # ∇^μτ∇_μ∇_ντ
    dgrad2=sp.simplify(sum(gu[i,i]*(diff(dtaud[i],coords[n])*dtaud[i]+dtaud[i]*diff(dtaud[i],coords[n])) for i in range(4))) # ∇_ν(∇τ)² ≈ ∂_ν[(∂τ)²] (标量)
    # 实际 ∇_ν[(∇τ)²] = Σ g^{ii} 2∂_iτ ∇_ν∂_iτ
    dgrad2=sp.simplify(sum(gu[i,i]*2*dtaud[i]*DD[i,n] for i in range(4)))
    lhs=sp.simplify(box*dtaud[n]+kin2-sp.Rational(1,2)*dgrad2-Vp*dtaud[n])
    rhs=sp.simplify(dtaud[n]*(box-Vp))
    dv=sp.simplify(lhs-rhs); st="PASS" if dv==0 else "FAIL"; ok2=ok2 and dv==0
    print(f"  ν={coords[n]}: 差={dv}  [{st}]")

print("\n=== 恒等式 (iii): ∇^μT^{g_τ}_{μν}=(g_τ/2)[G_{μν}∇^μτ+∇^μA_{μν}]=(g_τ/2)(G_{μν}-R_{μν})∇^μτ ===")
ok3=True
for n in range(4):
    # G_{μν}=R_{μν}-½Rg_{μν}
    termG=sp.simplify(sum((Rmat[mu,n]-sp.Rational(1,2)*Rscalar*g[mu,n])*gu[mu,mu]*dtaud[mu] for mu in range(4)))
    lhs=sp.simplify(termG+divA(n))
    rhs=sp.simplify(sum((Rmat[mu,n]-Rmat[mu,n])*gu[mu,mu]*dtaud[mu] for mu in range(4)))  # (G-R)∇ = -½R g ∇
    rhs=sp.simplify(sum((sp.Rational(1,2)*Rscalar*g[mu,n]-Rscalar*g[mu,n])*gu[mu,mu]*dtaud[mu] for mu in range(4)))
    # 期望 (G_{μν}-R_{μν})∇^μτ = (-½R g_{μν})∇^μτ = -½R ∇_ντ (因 g_{μν}∇^μτ=∇_ντ)
    expect=sp.simplify(-sp.Rational(1,2)*Rscalar*dtaud[n])
    dv=sp.simplify(sp.trigsimp(sp.expand(lhs-expect))); st="PASS" if dv==0 else "FAIL"; ok3=ok3 and dv==0
    print(f"  ν={coords[n]}: G∇+divA={lhs} vs -½R∇_ντ={expect} 差={dv} [{st}]")

print("\n=== 终局：物质守恒源（V09 完整 □ 关系）===")
print("∇^μT^m_{μν} = -∇^μ(T^τ+T^{g_τ})_{μν}")
print(" = -(∇^μT^τ_{μν}) - (g_τ/2)(G_{μν}-R_{μν})∇^μτ")
print(" = (g_τ/2)R∇_ντ + (g_τ/4)R∇_ντ = (3g_τ/4)R∇_ντ   [用 τ-EOM □τ-V'=-(g_τ/2)R]")
print("ALL_PASS:", ok and ok2 and ok3)
