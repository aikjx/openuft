# -*- coding: utf-8 -*-
# attack37 / 攻破㉙ —— 单一母作用量·四部门同时变分（一个 S、一个变量向量、一次运行）
# 填攻破㉘上一轮点名的缺口：语料 §1.2 把 GR+YM+Dirac+Higgs 并排写在一个积分号下，却从未对它做过一次同时变分。
# 本册在 1+1D（物质）+ FLRW 极小超空间（引力）的可算截断里，把那次变分真正跑出来。
# 红线：教科书级复现（标准模型+GR 的耦合母作用量），PASS 不迁移为物理成立、不计攻破数；0/22、UFT-3=0 不变。
import os, sys, json
import numpy as np
np.random.seed(20261107)
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(37)
ENTRIES = []
def add(uid, claim, verdict, reading):
    ENTRIES.append({"id": uid, "claim": claim, "verdict": verdict, "reading": reading})
    print("[%-9s] %s | %s" % (verdict, uid, claim))
    print("            读数: %s" % reading)
print("== attack37 攻破㉙·单一母作用量四部门同时变分 ==")

# ---------- 模型与离散 ----------
Nt, Nx = 20, 10
dt, dx = 0.05, 0.3
H0, g_cpl, m_f, mu2, lam = 0.6, 0.7, 0.5, 1.0, 0.8
v_vev = mu2/np.sqrt(lam)                      # Φ†Φ = v²/2 = μ²/(2λ) 为 V 最小
rho_vac = -mu2**4/(4*lam)                     # V(v) = −μ⁴/(4λ)（负真空能）
Lam = 3*H0**2 + rho_vac                       # 调 Λ 使 3H² = Λ − ρ_vac（de Sitter 在壳）
sig = [np.array([[0,1],[1,0]],complex), np.array([[0,-1j],[1j,0]],complex), np.array([[1,0],[0,-1]],complex)]
T = [0.5*s for s in sig]
g0, g1 = sig[0], 1j*sig[2]                    # (+,−)：γ⁰=σ1, γ¹=iσ2
I2 = np.eye(2, dtype=complex)
t = np.arange(Nt)*dt
WI = slice(3, Nt-3)                           # 内点窗：避开 np.gradient edge_order=2 的单边模板
# 变量打包顺序：a(Nt) | A0(Nt,Nx,3) | A1(Nt,Nx,3) | ψ(Nt,Nx,4实) | Φ(Nt,Nx,4实)
na = Nt; nA = Nt*Nx*3; npsi = Nt*Nx*4; nphi = Nt*Nx*4
NV = na + 2*nA + npsi + nphi
def unpack(x):
    i = 0
    a = x[i:i+na]; i += na
    A0 = x[i:i+nA].reshape(Nt,Nx,3); i += nA
    A1 = x[i:i+nA].reshape(Nt,Nx,3); i += nA
    pr = x[i:i+npsi].reshape(Nt,Nx,4); i += npsi
    psi = np.stack([pr[...,0]+1j*pr[...,1], pr[...,2]+1j*pr[...,3]], axis=-1)
    phir = x[i:i+nphi].reshape(Nt,Nx,4); i += nphi
    Phi = np.stack([phir[...,0]+1j*phir[...,1], phir[...,2]+1j*phir[...,3]], axis=-1)
    return a, A0, A1, psi, Phi
def pack(a, A0, A1, psi, Phi):
    pr = np.stack([psi[...,0].real, psi[...,0].imag, psi[...,1].real, psi[...,1].imag], axis=-1)
    phir = np.stack([Phi[...,0].real, Phi[...,0].imag, Phi[...,1].real, Phi[...,1].imag], axis=-1)
    return np.concatenate([a.ravel(), A0.ravel(), A1.ravel(), pr.ravel(), phir.ravel()])
def d_t(f): return np.gradient(f, dt, axis=0, edge_order=2)
def d_x(f): return (np.roll(f,-1,axis=1)-np.roll(f,1,axis=1))/(2*dx)   # x 周期
def mat(A): return np.einsum('...a,aij->...ij', A, np.array(T))         # su2 分量→2×2 矩阵
def Dmu(f, Am):                                                        # D_μ f = ∂_μ f − ig A_μ f
    return d_t(f) - 1j*g_cpl*np.einsum('...ij,...j->...i', Am[0], f), \
           d_x(f) - 1j*g_cpl*np.einsum('...ij,...j->...i', Am[1], f)

def action(x, g=g_cpl, measure_pow=3, mu2_=mu2):
    a, A0, A1, psi, Phi = unpack(x)
    A0m, A1m = mat(A0), mat(A1)
    # 规范：F01 = ∂0A1 − ∂1A0 − ig[A0,A1]（Hermitian），L_gauge = Tr(F01²) = ½Σ(F^a)²
    F01 = d_t(A1m) - d_x(A0m) - 1j*g*(A0m@A1m - A1m@A0m)
    Lg = np.einsum('...ij,...ji->...', F01, F01).real
    # Dirac（Hermitian 形式）：L = −Im(ψ̄γ^μD_μψ) − m ψ̄ψ
    Dp0, Dp1 = Dmu(psi, (A0m, A1m))
    psibar = np.einsum('...i,ij->...j', psi.conj(), g0)
    z = np.einsum('...i,...i->...', psibar, np.einsum('ij,...j->...i', g0, Dp0) + np.einsum('ij,...j->...i', g1, Dp1))
    Ld = -z.imag - m_f*np.einsum('...i,...i->...', psibar, psi).real
    # Higgs：L = |D0Φ|² − |D1Φ|² + μ²|Φ|² − λ|Φ|⁴
    DPh0, DPh1 = Dmu(Phi, (A0m, A1m))
    n2 = np.einsum('...i,...i->...', Phi.conj(), Phi).real
    Lh = np.einsum('...i,...i->...', DPh0.conj(), DPh0).real - np.einsum('...i,...i->...', DPh1.conj(), DPh1).real + mu2_*n2 - lam*n2**2
    Sm = float(np.sum(Lg + Ld + Lh))*dt*dx
    # 引力 + 真空能（ρ_vac 以 a³ 耦合；物质自身在固定背景上变分，全动力学背反为 BOUNDARY）
    ad = d_t(a)
    Lgrav = -3*a*ad**2 - Lam*a**3 + rho_vac*a**measure_pow
    Sg = float(np.sum(Lgrav))*dt
    return Sg + Sm

def grad(x, h=1e-4, **kw):
    g = np.zeros(NV)
    for k in range(NV):
        xp = x.copy(); xp[k] += h
        xm = x.copy(); xm[k] -= h
        g[k] = (action(xp, **kw)-action(xm, **kw))/(2*h)
    return g
def blocks(g):
    i = 0
    ba = g[i:i+na]; i += na
    bA0 = g[i:i+nA]; i += nA
    bA1 = g[i:i+nA]; i += nA
    bpsi = g[i:i+npsi]; i += npsi
    bphi = g[i:i+nphi]; i += nphi
    return {"a": ba, "A": np.concatenate([bA0,bA1]), "psi": bpsi, "Phi": bphi}
def iblocks(g):
    # 内点窗化的部门块（去 t 边界单边模板伪响应），用于响应矩阵
    b = blocks(g)
    A0 = b["A"][:nA].reshape(Nt,Nx,3)[WI].ravel()
    A1 = b["A"][nA:].reshape(Nt,Nx,3)[WI].ravel()
    return {"a": b["a"][WI], "A": np.concatenate([A0,A1]),
            "psi": b["psi"].reshape(Nt,Nx,4)[WI].ravel(),
            "Phi": b["Phi"].reshape(Nt,Nx,4)[WI].ravel()}

def grav_EL_disc(a, measure_pow=3):
    # S_grav=Σ L(a,ȧ)dt 的精确离散泛函导数（内点）：∂S/∂a_k = dt·∂L/∂a + (∂L/∂ȧ|_{k−1} − ∂L/∂ȧ|_{k+1})/2
    ad = d_t(a)
    dL_da = -3*ad**2 - 3*Lam*a**2 + measure_pow*rho_vac*a**(measure_pow-1)
    dL_dad = -6*a*ad
    el = dt*dL_da.copy()
    el[1:-1] += (dL_dad[:-2]-dL_dad[2:])/2.0
    return el

# 真空在壳位形
a_vac = np.exp(H0*t)
A0_vac = np.zeros((Nt,Nx,3)); A1_vac = np.zeros((Nt,Nx,3))
psi_vac = np.zeros((Nt,Nx,2), complex)
Phi_vac = np.zeros((Nt,Nx,2), complex); Phi_vac[...,1] = v_vev/np.sqrt(2)
x_vac = pack(a_vac, A0_vac, A1_vac, psi_vac, Phi_vac)

print("-- 一次运行：对单一 S 的 %d 维实变量向量做中心差分梯度，四块同时输出 --" % NV)
g_vac = grad(x_vac)
bv = blocks(g_vac)
# 参考尺度：用一个 off-shell 位形的梯度幅值定价容差
x_ref = x_vac.copy()
x_ref[na:na+nA] += 0.05*rng.standard_normal(nA)
g_ref = grad(x_ref)
scale = max(float(np.max(np.abs(g_ref))), 1e-12)
# a 块只在内点窗判（边界单边模板的离散变分不为零＝边界项，非在壳残差）；其余块全场为零
vac_res = {"a": float(np.max(np.abs(bv["a"][WI])))/scale,
           "A": float(np.max(np.abs(bv["A"])))/scale,
           "psi": float(np.max(np.abs(bv["psi"])))/scale,
           "Phi": float(np.max(np.abs(bv["Phi"])))/scale}
v1 = max(vac_res.values())
add("V1","单一母作用量 S[a,A,ψ,Φ] 在真空在壳位形（A=0,ψ=0,Φ=vev,a=de Sitter 调 Λ）四部门梯度块同时为零（a 取内点窗）","PASS" if v1 < 1e-4 else "FAIL",
    "四块 max|梯度|/参考尺度：a=%.2e A=%.2e ψ=%.2e Φ=%.2e（NV=%d，一次运行；参考尺度=%.3e；a 残差为 O(dt²) 离散截断）"%(vac_res["a"],vac_res["A"],vac_res["psi"],vac_res["Phi"],NV,scale))

# ---------- V2 off-shell 规范不变性：一个群作用于全部物质部门 ----------
def Ufield(shape):
    # 长波光滑规范参数： naive 中心差分不严格满足 Leibniz，残差 O((k·dx)²)；
    # 网格尺度随机 U 会把该缺陷放大到 O(1)（实测 8.6），故取长波模 k·dx=2π/Nx 定价。
    xg = np.arange(Nx)*dx
    th = np.zeros(shape+(3,))
    for a_ in range(3):
        th[...,a_] = 0.3*np.sin(2*np.pi*xg/(Nx*dx)+0.7*a_)[None,:]*np.cos(np.pi*t/(Nt*dt)+0.4*a_)[:,None]
    n = np.linalg.norm(th, axis=-1, keepdims=True)
    ths = np.einsum('...a,aij->...ij', th, np.array(sig))
    c = np.cos(n/2)[...,None]; s = np.sin(n/2)[...,None]
    return c*I2 + 1j*s*ths/np.where(n==0,1,n)[...,None]
def gauge_transform(x):
    a, A0, A1, psi, Phi = unpack(x)
    U = Ufield((Nt,Nx)); Uinv = np.conjugate(np.swapaxes(U,-1,-2))
    dU0 = d_t(U); dU1 = d_x(U)
    A0m, A1m = mat(A0), mat(A1)
    A0p = U@A0m@Uinv - (1j/g_cpl)*dU0@Uinv
    A1p = U@A1m@Uinv - (1j/g_cpl)*dU1@Uinv
    def comp(M): return np.stack([2*np.einsum('...ij,ji->...', M, Ta).real for Ta in T], axis=-1)
    psip = np.einsum('...ij,...j->...i', U, psi)
    Phip = np.einsum('...ij,...j->...i', U, Phi)
    return pack(a, comp(A0p), comp(A1p), psip, Phip)
x_off = x_vac.copy()
x_off[na:na+2*nA] += 0.1*rng.standard_normal(2*nA)
x_off[na+2*nA:na+2*nA+npsi] += 0.1*rng.standard_normal(npsi)
x_off[na+2*nA+npsi:] += 0.1*rng.standard_normal(nphi)
S0 = action(x_off); S1 = action(gauge_transform(x_off))
v2 = abs(S1-S0)/max(abs(S0),1e-12)
add("V2","同一 SU(2) 规范变换同时作用于 A、ψ、Φ 而 S 不变（统一耦合的结构证据，off-shell 随机位形＋长波 U）","PASS" if v2 < 1e-3 else "FAIL",
    "|S[U·fields]−S[fields]|/|S| = %.2e（S=%.4f；长波 U，k·dx=2π/Nx，残差为 O((k·dx)²) 离散 Leibniz 缺陷）"%(v2, S0))

# ---------- V3 4×4 部门响应矩阵（变异体定价：哪块对哪个扰动响应） ----------
def perturb(x, sector):
    y = x.copy()
    if sector=="a": y[:na] *= (1+0.1*np.sin(3*t))
    elif sector=="A": y[na:na+2*nA] += 0.08*rng.standard_normal(2*nA)
    elif sector=="psi": y[na+2*nA:na+2*nA+npsi] += 0.08*rng.standard_normal(npsi)
    elif sector=="Phi": y[na+2*nA+npsi:] += 0.08*rng.standard_normal(nphi)
    return y
sectors = ["a","A","psi","Phi"]
resp = np.zeros((4,4))
for j, sec in enumerate(sectors):
    bj = iblocks(grad(perturb(x_off, sec)))     # off-shell 物质位形：交叉耦合在线性阶活跃
    for i, s in enumerate(sectors):
        resp[i,j] = float(np.max(np.abs(bj[s])))/scale
print("-- 响应矩阵（行=梯度块，列=扰动部门；元素=max|内点块|/参考尺度；基态=off-shell）--")
print("        " + "  ".join("%8s"%s for s in sectors))
for i, s in enumerate(sectors):
    print("  %-5s " % s + "  ".join("%8.2e"%resp[i,j] for j in range(4)))
diag_ok = all(resp[i,i] > 1e-3 for i in range(4))
couple_APhi = resp[3,1] > 1e-4      # A 扰动 → Φ 块（协变导数耦合）
couple_Apsi = resp[2,1] > 1e-4      # A 扰动 → ψ 块（Dirac 协变导数）
couple_psiA = resp[1,2] > 1e-4      # ψ 扰动 → A 块（Dirac 流供 Gauss）
v3ok = diag_ok and couple_APhi and couple_Apsi and couple_psiA
add("V3","四部门各有对角响应，且 A→Φ、A→ψ、ψ→A 交叉响应非零（协变导数与流耦合在梯度里可见，off-shell 内点窗）","PASS" if v3ok else "FAIL",
    "对角全 >1e-3=%s；A→Φ=%.2e A→ψ=%.2e ψ→A=%.2e（交叉阈 1e-4；引力↔物质背反按构造为零＝BOUNDARY）"%(diag_ok, resp[3,1], resp[2,1], resp[1,2]))

# ---------- V4 引力块 = 精确离散 E-L（第二独立推导）＋连续 Friedmann 对照 ----------
a_off = np.exp(H0*t)*(1+0.1*np.sin(3*t))
x_a = x_vac.copy(); x_a[:na] = a_off
ga = blocks(grad(x_a))["a"]
el_disc = grav_EL_disc(a_off)                       # 与 FD 独立的解析模板推导
v4a = float(np.max(np.abs(ga[WI]-el_disc[WI]))/(np.abs(el_disc[WI]).max()+1e-30))
ad = d_t(a_off); add2 = d_t(ad)
fried = (3*ad**2 + 6*a_off*add2 - 3*(Lam-rho_vac)*a_off**2)*dt   # ∂S/∂a = dt·(−EL_cont)
v4b = float(np.max(np.abs(ga[WI]-fried[WI]))/(np.abs(fried[WI]).max()+1e-30))
v4ok = (v4a < 1e-6) and (v4b < 5e-2)
add("V4","引力梯度块＝精确离散 E-L（独立推导，紧）且≈连续 Friedmann 残差（O(dt²)，松）","PASS" if v4ok else "FAIL",
    "FD vs 离散E-L 相对残差=%.2e（紧<1e-6）；FD vs 连续Friedmann=%.2e（松<5e-2，O(dt²)）；Λ−ρ_vac=3H²=%.3f"%(v4a, v4b, 3*H0**2))

# ---------- 守卫 ----------
print("-- 守卫 --")
# G7 断规范耦合：g→0 后 off-shell 规范不变性必须破
S0g = action(x_off, g=0.0); S1g = action(gauge_transform(x_off), g=0.0)
g7val = abs(S1g-S0g)/max(abs(S0g),1e-12)
g7 = g7val > 1e-3
print("[%s] G7 断耦合：g=0 时 |ΔS|/|S|=%.2e（>1e-3 证明 V2 读的是耦合不是常数）"%("OK" if g7 else "BAD", g7val))
# G8 破测度：ρ_vac a³→a² 后引力块必须失配
ga2 = blocks(grad(x_a, measure_pow=2))["a"]
el2 = grav_EL_disc(a_off, measure_pow=2)
g8val = float(np.max(np.abs(ga2[WI]-el_disc[WI]))/(np.abs(el_disc[WI]).max()+1e-30))
g8 = g8val > 0.1
print("[%s] G8 破测度：a³→a² 后引力块对原 E-L 失配 %.2e（>0.1 证明 V4 读的是测度）"%("OK" if g8 else "BAD", g8val))
# G9 偏离势最小：Φ=1.1·vev 后 Φ 块必须远超在壳噪声底（100×）
ph = unpack(x_vac)[4]*1.1
x_g9 = pack(a_vac, A0_vac, A1_vac, psi_vac, ph)
g9val = float(np.max(np.abs(blocks(grad(x_g9))["Phi"])))/scale
g9floor = 100*vac_res["Phi"]
g9 = g9val > max(g9floor, 1e-9)
print("[%s] G9 离壳对照：Φ=1.1·vev 时 Φ 块=%.2e（>100×在壳底 %.2e 证明 V1 的零是真在壳）"%("OK" if g9 else "BAD", g9val, g9floor))
guards_ok = bool(g7 and g8 and g9)
from collections import Counter
cnt = Counter(e["verdict"] for e in ENTRIES)
print("== 汇总：条目 %d；%s；守卫 %d/3 ==" % (len(ENTRIES), " / ".join("%s %d"%(k,v) for k,v in sorted(cnt.items())), sum([g7,g8,g9])))
print("红线：本册是标准模型+GR 耦合母作用量的教科书级变分复现；『四力在一个运行里』指四部门 E-L 由同一 S 同时输出，")
print("      不表示存在新的第一性统一原理；PASS 不计攻破数，0/22、UFT-3=0 不变。全动力学引力↔物质背反为 BOUNDARY。")
out = {"round":"attack37_攻破㉙单一母作用量四部门同时变分","date":"2026-11-07","entries":ENTRIES,"summary":dict(cnt),
       "guards":{"G7_breakcoupling":bool(g7),"G8_breakmeasure":bool(g8),"G9_offshell":bool(g9)},
       "readings":{"V1":v1,"V1_blocks":vac_res,"V2":v2,"V3_resp":resp.tolist(),"V4a":v4a,"V4b":v4b,"NV":NV,"scale":scale},
       "exit":0 if (guards_ok and all(e["verdict"]=="PASS" for e in ENTRIES)) else 2}
json.dump(out, open(os.path.join(HERE,"attack37_单一母作用量_四部门同时变分_2026-11-07.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
sys.exit(out["exit"])