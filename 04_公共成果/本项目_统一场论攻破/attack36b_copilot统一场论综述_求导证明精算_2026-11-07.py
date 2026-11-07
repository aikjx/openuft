# -*- coding: utf-8 -*-
# attack36b / 攻破㉘·求导证明精算层 —— 对 .copilot《全维统一场论》综述的变分/恒等式/ODE 第二仪器
# 与 attack36（数值宣称审计）配对：本册把论文的"求导证明"宣称逐条做成可复跑数学。
import os, sys, json
import numpy as np
np.random.seed(20261107)
HERE = os.path.dirname(os.path.abspath(__file__))
ENTRIES = []
def add(uid, claim, verdict, reading):
    ENTRIES.append({"id": uid, "claim": claim, "verdict": verdict, "reading": reading})
    print("[%-9s] %s | %s" % (verdict, uid, claim))
    print("            读数: %s" % reading)
print("== attack36b 攻破㉘·求导证明精算层 ==")

# ---------- D1 极小子超空间变分：数值梯度 vs 解析 E-L（论文 §2.1 的 δS=0 求导链） ----------
K, Lam, kk = 1.0, 0.7, 0.0
H0 = np.sqrt(Lam/3.0)
def L(a, adot): return -3*a*(adot**2 + kk) - Lam*a**3
def EL(a, adot, add): return -3*adot**2 - 6*a*add + 3*kk + 3*Lam*a**2   # E-L 表达式：d/dt ∂L/∂ȧ − ∂L/∂a
dt, N = 0.005, 800
t = np.arange(N)*dt
rng = np.random.default_rng(7)
a = np.exp(H0*t)*(1.0+0.05*np.sin(5.0*t))                             # 确定性 de Sitter 受扰路径（噪声路径会把 FD 截断放大 ~dt^-2）
def S(path):
    ad = np.gradient(path, dt, edge_order=2)
    return float(np.sum(L(path, ad)))
h = 1e-3   # S 对单点至多三次，中心差分截断 ~h²·∂³ 可忽略；h 放大一档把舍入底降两个量级
grad = np.zeros(N)
for i in range(2, N-2):
    p1 = a.copy(); p1[i] += h
    p2 = a.copy(); p2[i] -= h
    grad[i] = (S(p1)-S(p2))/(2*h)
# 同一离散作用量的精确离散梯度（两点中心模板 ad_k=(a_{k+1}−a_{k−1})/2dt）
ad = (np.roll(a,-1)-np.roll(a,1))/(2*dt)
def dL_a(a_, ad_): return -3*ad_**2 - 3*Lam*a_**2
def dL_ad(a_, ad_): return -6*a_*ad_
gd_exact = dL_a(a, ad)
gd_exact[1:-1] += (dL_ad(a[:-2], ad[:-2]) - dL_ad(a[2:], ad[2:]))/(2*dt)   # ∂S/∂a_k = L_a|_k + (L_ȧ|_{k−1} − L_ȧ|_{k+1})/2dt（S 不带 dt 测度 ⟹ 连续极限 −EL_k 同无 dt）
w = slice(10, N-10)   # 排除 np.gradient 边界模板污染的指标
d1a = float(np.max(np.abs(grad[w]-gd_exact[w])/(np.abs(gd_exact[w])+1e-30)))
add_seq = np.gradient(ad, dt, edge_order=2)
analytic = -EL(a, ad, add_seq)
d1b = float(np.max(np.abs(gd_exact[w]-analytic[w])/(np.abs(analytic[w])+1e-30)))
d1 = max(d1a, d1b)
add("D1","论文『对 g 变分得 Einstein 方程』的 minisuperspace 化复现：数值泛函梯度＝精确离散 E-L＝连续 Euler-Lagrange（双通道）","PASS" if (d1a < 1e-4 and d1b < 5e-2) else "FAIL",
    "梯度 vs 精确离散残差 %.2e（舍入级）；精确离散 vs 连续 −EL 相对残差 %.2e（O(dt²) 截断，N=%d dt=%.3f 光滑受扰路径）"%(d1a, d1b, N, dt))

# ---------- D2 de Sitter 同时满足约束与演化（G+Λg=0 的 FLRW 闭合形式） ----------
H = np.sqrt(Lam/3.0)
tt = np.linspace(0.1, 2.0, 50)
a_ds = np.exp(H*tt)
adot = H*a_ds; add_ds = H**2*a_ds
constraint = adot**2 + kk - Lam*a_ds**2/3.0
evo = -3*adot**2 - 6*a_ds*add_ds + 3*kk + 3*Lam*a_ds**2
d2 = float(max(np.max(np.abs(constraint)), np.max(np.abs(evo))))
add("D2","a(t)=e^{Ht}、H²=Λ/3 精确满足 0=ȧ²+k−Λa²/3（约束）与 E-L（演化）","PASS" if d2 < 1e-12 else "FAIL",
    "两侧 max|残差| = %.2e（机器零级）" % d2)

# ---------- D3 Bianchi 缩并：ρ̇+3H(ρ+p)=0 对任意随机 a(t) 恒成立（论文 §2.1 守恒宣称） ----------
def flrw_rho_p(a_, adot_, add_):
    rho = 3*(adot_**2 + kk)/a_**2
    p   = -(2*add_*a_ + adot_**2 + kk)/a_**2   # 几何流体口径 p_G = −G^1_1/κ²，Bianchi 恒等式只对负号闭合（本轮实测定价）
    return rho, p
a2 = np.exp(H0*t)*(1.0+0.2*np.sin(2.7*t)) + 0.3                     # 一般（非解）光滑路径
ad2 = np.gradient(a2, dt, edge_order=2); add2 = np.gradient(ad2, dt, edge_order=2)
rho, p = flrw_rho_p(a2, ad2, add2)
Hd = ad2/a2
rho_d = np.gradient(rho, dt, edge_order=2)
div = rho_d + 3*Hd*(rho + p)
scale = np.abs(rho_d).mean() + np.abs(3*Hd*(rho+p)).mean()
d3 = float(np.max(np.abs(div[5:-5]))/scale)
add("D3","∇·G=0 于 FLRW 的投影恒等式 ρ̇+3H(ρ+p)≡0 对一般（非解）路径成立","PASS" if d3 < 1e-2 else "FAIL",
    "max|div|/源项均值 = %.2e（两项各 O(源) 相消至 FD 截断底，恒等式层而非方程层）" % d3)

# ---------- D4 Clifford/Dirac：{γ,γ}=2η 与 (γ·p)²=p²（论文 §2.3 与恒等式层；号差 (−,+,+,+) 与论文 §1.1 一致） ----------
eta = np.diag([-1.,1.,1.,1.])
I2 = np.eye(2); Z2 = np.zeros((2,2))
g0 = np.block([[Z2, I2],[-I2, Z2]]).astype(complex)                  # (γ⁰)²=−I ⟺ η00=−1
sig = [np.array([[0,1],[1,0]], dtype=complex), np.array([[0,-1j],[1j,0]], dtype=complex), np.array([[1,0],[0,-1]], dtype=complex)]
gs = [np.block([[Z2, s],[s, Z2]]).astype(complex) for s in sig]      # (γⁱ)²=+I
gam = [g0]+gs
cm = np.max([np.max(np.abs(gam[m]@gam[n]+gam[n]@gam[m]-2*eta[m,n]*np.eye(4))) for m in range(4) for n in range(4)])
p4 = rng.standard_normal(4)
gp = p4[0]*gam[0]+p4[1]*gam[1]+p4[2]*gam[2]+p4[3]*gam[3]
p2 = float(-(p4[0]**2)+p4[1]**2+p4[2]**2+p4[3]**2)
fac = np.max(np.abs(gp@gp - p2*np.eye(4)))
d4 = max(float(cm), float(fac))
add("D4","Dirac 因式分解依赖的 Clifford 代数 {γμ,γν}=2ημν 与 (γ·p)²=p² I 矩阵实算","PASS" if d4 < 1e-12 else "FAIL",
    "max|反交换子−2η| = %.2e；max|(γp)²−p²I| = %.2e（随机 p=(%.3f,%.3f,%.3f,%.3f)）"%(cm, fac, p4[0], p4[1], p4[2], p4[3]))

# ---------- D5 Yang-Mills：规范协变 F→UFU† 与 [T,T]=ifT（论文 §2.2 求导结构） ----------
T = [0.5*np.array(s, dtype=complex) for s in sig]
comm = 0.0
eps = {(0,1,2):1,(1,2,0):1,(2,0,1):1,(0,2,1):-1,(2,1,0):-1,(1,0,2):-1}
for a1 in range(3):
    for b1 in range(3):
        lhs = T[a1]@T[b1]-T[b1]@T[a1]
        rhs = sum(1j*eps.get((a1,b1,c1),0)*T[c1] for c1 in range(3))
        comm = max(comm, float(np.max(np.abs(lhs-rhs))))
# 随机 su(2) 平面波场，解析导数
cs = rng.standard_normal((4,3,3))
ks = rng.standard_normal((4,3))*0.9
def Avec(x):
    A = np.zeros((4,2,2), dtype=complex)
    for mu in range(4):
        for n in range(3):
            ph = sum(ks[mu2,n]*x[mu2] for mu2 in range(4))
            for a1 in range(3):
                A[mu] += cs[mu,n,a1]*np.sin(ph)*T[a1]
    return A
def dAvec(x, nu):
    d = np.zeros((4,2,2), dtype=complex)
    for mu in range(4):
        for n in range(3):
            ph = sum(ks[mu2,n]*x[mu2] for mu2 in range(4))
            for a1 in range(3):
                d[mu] += cs[mu,n,a1]*np.cos(ph)*ks[nu,n]*T[a1]
    return d
g_cpl = 0.8
def Fdirect(x):
    A = Avec(x); F = {}
    for m1 in range(4):
        for n1 in range(m1+1,4):
            # F_mn = ∂_m A_n − ∂_n A_m − ig[A_m,A_n]（与 D'=UDU† 变换律配套的指标序；纯规范对照排除反向混合约定）
            F[(m1,n1)] = dAvec(x, m1)[n1] - dAvec(x, n1)[m1] - 1j*g_cpl*(A[m1]@A[n1]-A[n1]@A[m1])
    return A, F
from numpy.linalg import inv
def Uat(xv):
    th = np.array([0.4*np.sin(sum(xv)+a1) for a1 in range(3)])
    n = float(np.linalg.norm(th))
    ths = sum(th[a1]*sig[a1] for a1 in range(3))
    return np.cos(n/2.0)*np.eye(2, dtype=complex) + 1j*np.sin(n/2.0)*ths/n   # exp(i θ·σ/2) 闭式（SU(2)）
HD = 1e-4   # 差分步长：嵌套 FD 的舍入放大 ~eps/H²≈2e-8，截断 ~H²≈1e-8，两侧都有余量
def Ap_at(xv):
    # A'_mu = U A_mu U^† − (i/g)(∂_mu U)U^†  （即 D'_mu = U D_mu U^†）
    Un = Uat(xv); Uinv = inv(Un)
    Ax = Avec(xv)
    dU = np.zeros((4,2,2), dtype=complex)
    for nu in range(4):
        t1 = xv.copy(); t1[nu]+=HD
        t2 = xv.copy(); t2[nu]-=HD
        dU[nu] = (Uat(t1)-Uat(t2))/(2.0*HD)
    return np.array([Un@Ax[mu]@Uinv - (1j/g_cpl)*dU[mu]@Uinv for mu in range(4)])
def Fprim_from_Ap(xv):
    Ap = Ap_at(xv)
    dAp = np.zeros((4,4,2,2), dtype=complex)
    for nu in range(4):
        t1 = xv.copy(); t1[nu]+=HD
        t2 = xv.copy(); t2[nu]-=HD
        for mu in range(4):
            dAp[nu,mu] = (Ap_at(t1)[mu]-Ap_at(t2)[mu])/(2.0*HD)
    Fp = {}
    for m2 in range(4):
        for n2 in range(m2+1,4):
            Fp[(m2,n2)] = dAp[m2,n2] - dAp[n2,m2] - 1j*g_cpl*(Ap[m2]@Ap[n2]-Ap[n2]@Ap[m2])
    return Fp
x0 = rng.standard_normal(4)*0.3
A, F0 = Fdirect(x0)
U = Uat(x0)
Fp = Fprim_from_Ap(x0)
err_g = max([float(np.max(np.abs(Fp[key] - U@F0[key]@inv(U)))) for key in F0])
d5 = max(comm, err_g)
add("D5","YM 场强构造 F=dA−dA−ig[A,A] 在规范变换下协变 F'=UFU†，且 [T^a,T^b]=if^{abc}T^c","PASS" if d5 < 1e-6 else "FAIL",
    "max|[T,T]−ifT| = %.2e；max|F'[A']−UFU†| = %.2e（随机平面波 su(2) 场，嵌套中心差分步长 %.0e）"%(comm, err_g, HD))

# ---------- D6 Higgs 质量矩阵：本征值闭式与 ρ_PT=1（论文 §2.4） ----------
bad6 = 0.0
for trial in range(20):
    g1, g2p, v1 = rng.uniform(0.4,0.9), rng.uniform(0.2,0.5), rng.uniform(100,300)
    M = (v1**2/4)*np.array([[g1**2, -g1*g2p],[-g1*g2p, g2p**2]])
    ev = np.sort(np.linalg.eigvalsh(M))
    bad6 = max(bad6, abs(ev[0])/max(ev[1],1e-12))
    mW = g1*v1/2; mZ = np.sqrt(ev[1]); cW = g1/np.sqrt(g1**2+g2p**2)
    bad6 = max(bad6, abs(mW/mZ - cW))
d6 = bad6
add("D6","中性规范玻色 2×2 质量矩阵一个本征值为 0（光子无质量），且 m_W/m_Z=cosθ_W（ρ_PT=1）为代数恒等","PASS" if d6 < 1e-12 else "FAIL",
    "20 组随机 (g,g',v)：max 零本征值|λ0|/λ1 与 max|m_W/m_Z−cosθ_W| 合计 %.2e（矩阵级复现 U4b 的『只在树级口径』）" % d6)

# ---------- D7 跷跷板：2×2 精确对角化（mpmath 高精度）vs 闭式 −m_D²/M_R（论文 §3.3） ----------
import mpmath as mp
mp.mp.dps = 50
worst7 = 0.0; samples7 = []
for trial in range(8):
    mD = mp.mpf(rng.uniform(10, 200)); MR = mp.mpf(rng.uniform(1e13, 1e15))
    light_exact = (MR - mp.sqrt(MR*MR + 4*mD*mD))/2               # 特征方程精确根（double 的 eigvalsh 在此尺度被相消舍入吞掉，上轮实测 rel≡0）
    approx = -mD*mD/MR
    rel = float(abs(light_exact - approx)/abs(light_exact))
    worst7 = max(worst7, rel); samples7.append(rel)
d7 = float(np.median(samples7))
add("D7","seesaw 轻本征值对 −m_D²/M_R 的近似误差量级（mpmath 50 位精确对角化）","PASS" if worst7 < 1e-3 else "FAIL",
    "中位相对误差 %.2e，最坏 %.2e（m_D~10-200 GeV, M_R~1e13-1e15；论文『≈0.1 eV』的 ≈ 在此 (m_D/M_R)² 量级被定价，非 0.1 eV 本身）"%(d7, worst7))

# ---------- D8 RG 第二仪器：RK4 积分 β 方程 vs 闭式 α⁻¹ 线性于 lnμ（论文 §3.1 演化方程本体） ----------
from math import log as mlog
lnMZ, lnEnd = mlog(91.1876), mlog(2.282e16)
worst8 = 0.0
for a0, b in [(1/127.95, 4.1), (0.0338, -19/6), (0.1184, -7)]:
    steps = 4000
    hstep = (lnEnd-lnMZ)/steps
    f = lambda al: b*al**2/(2.0*np.pi)        # 与论文 §3.1 同约定：dα/dlnμ=(b/2π)α² ⟺ μdg/dμ=(b/16π²)g³
    al = a0
    for _ in range(steps):
        k1 = f(al); k2 = f(al+0.5*hstep*k1); k3 = f(al+0.5*hstep*k2); k4 = f(al+hstep*k3)
        al += hstep*(k1+2*k2+2*k3+k4)/6.0
    closed = 1.0/(a0**(-1) - b/(2.0*np.pi)*(lnEnd-lnMZ))
    worst8 = max(worst8, abs(al-closed)/abs(closed))
add("D8","一圈演化：dα/dlnμ=(b/2π)α²（即 μdg/dμ=(b/16π²)g³）数值积分（RK4，4000 步）与闭式 α⁻¹ 线性于 lnμ 逐点一致","PASS" if worst8 < 1e-6 else "FAIL",
    "max 相对偏差 = %.2e（三个耦合全程 ln(M_Z→2.282e16)；U6/U7 跑动内核确为 ODE 解，不是插值）" % worst8)

# ---------- D9 KK 约化：5×5 ansatz 行列式与逆块恒等式（论文 §4.1） ----------
worst9 = 0.0
for trial in range(12):
    Q, _ = np.linalg.qr(rng.standard_normal((4,4)))                # 良适 Lorentz 谱：|λi|∈[0.8,3]，排除近奇异度规把相对误差放大成仪器噪声
    vals = np.array([-1.0, 1.0, 1.0, 1.0])*rng.uniform(0.8, 3.0, 4)
    g4 = Q@np.diag(vals)@Q.T
    phi = rng.uniform(0.3, 3.0)
    Av = rng.standard_normal(4)*0.5
    G5 = np.zeros((5,5))
    G5[:4,:4] = g4 + np.outer(Av, Av)*phi
    G5[:4,4] = phi*Av; G5[4,:4] = phi*Av; G5[4,4] = phi
    d5det = np.linalg.det(G5)
    rhs = phi*np.linalg.det(g4)
    worst9 = max(worst9, abs(d5det-rhs)/max(abs(rhs), 1e-12))
    Gi = np.linalg.inv(G5)
    g4i = np.linalg.inv(g4)
    s_form = float(Av@g4i@Av)
    G55_exact = 1.0/phi + s_form
    worst9 = max(worst9, abs(Gi[4,4]-G55_exact)/abs(G55_exact))          # 逆闭式 G⁵⁵=1/φ+g^{μν}A_μA_ν（简写 1/φ 在 O(A²) 不成立，本仪器自纠）
    worst9 = max(worst9, float(np.max(np.abs(Gi[:4,:4]-g4i)))/float(np.max(np.abs(g4i))))
d9 = worst9
add("D9","KK ansatz ds5²=g+φ(dy+Ax)² 的 det 恒等 √−g5=√φ·√−g4，与逆闭式 G^{μν}=g^{μν}、G⁵⁵=1/φ+g^{μν}A_μA_ν","PASS" if d9 < 1e-9 else "FAIL",
    "12 组良适随机度规 max 相对误差 = %.2e；简写『g⁵⁵=1/φ』经 Schur 补判定价其在 O(A²) 不成立（本仪器自查改），5 维 Ricci 全重推不在本册（维持 U11 的 BOUNDARY 口径）" % d9)

# ---------- 守卫（求导仪器有牙自检） ----------
print("-- 守卫 --")
# G4: 差分收敛：D3 恒等式残量随 dt 减半应 ~4 倍改善（O(dt²)）
def d3_err(dt2, N2):
    t2 = np.arange(N2)*dt2
    a3 = np.exp(H0*t2)*(1.0+0.2*np.sin(2.7*t2)) + 0.3   # 与 D3 同一光滑母函数在细网格重采样（嵌套网格，收敛比才有定义）
    ad3 = np.gradient(a3, dt2, edge_order=2); add3 = np.gradient(ad3, dt2, edge_order=2)
    r3, p3 = flrw_rho_p(a3, ad3, add3)
    H3 = ad3/a3; div3 = np.gradient(r3, dt2, edge_order=2)+3*H3*(r3+p3)
    sc = np.abs(np.gradient(r3, dt2, edge_order=2)).mean()+np.abs(3*H3*(r3+p3)).mean()
    return float(np.max(np.abs(div3[5:-5]))/sc)
e_full, e_half = d3_err(0.01, 400), d3_err(0.005, 800)
g4 = e_full/e_half > 2.0
print("[%s] G4 差分收敛：dt 减半残量比 %.2f（>2 才配得上 O(dt²) 声明）"%("OK" if g4 else "BAD", e_full/e_half))
# G5: 破系数对照：L 的 −3 改 −2 后，D1 型解析 E-L 必须与数值梯度失配
L_bad = lambda a_, ad_: -2*a_*(ad_**2+kk) - Lam*a_**3
def S_bad(path):
    adx = np.gradient(path, dt, edge_order=2)
    return float(np.sum(L_bad(path, adx)))
gb = np.zeros(N)
for i in range(2, N-2):
    p1 = a.copy(); p1[i]+=h; p2 = a.copy(); p2[i]-=h
    gb[i] = (S_bad(p1)-S_bad(p2))/(2*h)
mismatch = float(np.max(np.abs(gb[10:-10]-analytic[10:-10]))/(np.abs(analytic[10:-10]).mean()+1e-30))
g5 = mismatch > 0.5
print("[%s] G5 破系数对照：改系数后解析-数值失配度 %.2f（>0.5 证明 D1 读的是系数不是常数）"%("OK" if g5 else "BAD", mismatch))
# G6: 零本征值对照：中性矩阵改 M[0,1]=−g*g'→0 后零本征值消失（D6 判据可破）
g1_, g2_, v_ = 0.65, 0.36, 246.2
Mfix = (v_**2/4)*np.array([[g1_**2, 0.0],[0.0, g2_**2]])
evf = np.sort(np.linalg.eigvalsh(Mfix))
g6 = abs(evf[0])/evf[1] > 0.01
print("[%s] G6 断链对照：抹掉混合项后 λ0/λ1 = %.3f（零模消失 ⇒ D6 的 0 是真判据）"%("OK" if g6 else "BAD", evf[0]/evf[1]))
guards_ok = bool(g4 and g5 and g6)
from collections import Counter
cnt = Counter(x["verdict"] for x in ENTRIES)
print("== 汇总：条目 %d；%s；守卫 %d/3 ==" % (len(ENTRIES), " / ".join("%s %d"%(k,v) for k,v in sorted(cnt.items())), sum([g4,g5,g6])))
print("红线：求导证明层全部是『教科书恒等式/变分链复现』——PASS 不迁移为物理成立，不计攻破数。")
out = {"round":"attack36b_攻破㉘求导证明层","date":"2026-11-07","entries":ENTRIES,
       "summary":dict(cnt),"guards":{"G4_conv":bool(g4),"G5_badcoef":bool(g5),"G6_zeroctrl":bool(g6)},
       "readings":{"D1":d1,"D2":d2,"D3":d3,"D4":d4,"D5":d5,"D6":d6,"D7_median":d7,"D7_worst":worst7,"D8":worst8,"D9":d9,
                   "G4_ratio":e_full/e_half,"G5_mismatch":mismatch,"G6_lambda_ratio":float(evf[0]/evf[1])},
       "exit":0 if guards_ok else 2}
json.dump(out, open(os.path.join(HERE,"attack36b_copilot统一场论综述_求导证明精算_2026-11-07.json"),"w",encoding='utf-8'), ensure_ascii=False, indent=1)
sys.exit(out["exit"])
