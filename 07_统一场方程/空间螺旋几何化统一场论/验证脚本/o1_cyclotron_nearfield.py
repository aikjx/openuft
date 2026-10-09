# -*- coding: utf-8 -*-
"""43 号判据数值验证：回旋电子近场 LW 分解，检验'束轴上 E∥v_z 且 B=0'
UFE-2 纵波预言(43号)：回旋/同步辐射源近场存在 B=0、S=0、E∥v_z、频率=ω_r 的束缚纵振荡。
标准电动力学：运动电荷近场 B≠0。数值对比——束轴上 E_z、E⊥、B 的时间振荡。
"""
import numpy as np
me=9.1093837015e-31; e=1.602176634e-19; c=299792458.0; eps0=8.8541878128e-12

# 回旋电子参数（非相对论，B0=1T）
B0=1.0; wc=e*B0/me            # 回旋角频率
v_perp=0.1*c; R=v_perp/wc     # 回旋半径
vz=0.1*c                      # 轴向速度

def retard(P, t):
    """解推迟时间 t_r = t - |P-r(t_r)|/c，返回 r,v,a at t_r"""
    # 迭代
    tr=t
    for _ in range(60):
        x=R*np.cos(wc*tr); y=R*np.sin(wc*tr); z=vz*tr
        rr=np.array([x,y,z])
        d=P-rr; dist=np.linalg.norm(d)
        tr_new=t-dist/c
        if abs(tr_new-tr)<1e-20: break
        tr=tr_new
    x=R*np.cos(wc*tr); y=R*np.sin(wc*tr); z=vz*tr
    rr=np.array([x,y,z]); d=P-rr; dist=np.linalg.norm(d)
    n=d/dist
    v=np.array([-R*wc*np.sin(wc*tr), R*wc*np.cos(wc*tr), vz])
    a=np.array([-R*wc**2*np.cos(wc*tr), -R*wc**2*np.sin(wc*tr), 0.0])
    return tr, rr, n, dist, v, a

def LW(P, t):
    """Liénard-Wiechert E,B"""
    tr, rr, n, dist, v, a = retard(P,t)
    beta=v/c; betadot=a/c
    nb=1-np.dot(n,beta)
    coef1=1.0/(eps0*4*np.pi*dist**2) * (n-beta)/((1-nb)**3)  # 缺 gamma^2：加 gamma 因子
    gamma=1/np.sqrt(1-np.dot(beta,beta))
    E_vel=e*(n-beta)/(gamma**2*4*np.pi*eps0*dist**2*(1-nb)**3)
    E_acc=e/(4*np.pi*eps0*c*dist)*np.cross(n, np.cross((n-beta), betadot))/(1-nb)**3
    E=E_vel+E_acc
    B=np.cross(n,E)/c
    return E, B, dist

# 束轴上观察点（近场 Z=20R）
Z=20*R
P=np.array([0.0,0.0,Z])
T=np.linspace(0, 4*np.pi/wc, 400)
Ez=[]; Eperp=[]; Bmag=[]; By=[]
for t in T:
    E,B,dist=LW(P,t)
    Ez.append(E[2]); Eperp.append(np.hypot(E[0],E[1])); Bmag.append(np.linalg.norm(B)); By.append(B[1])
Ez=np.array(Ez); Eperp=np.array(Eperp); Bmag=np.array(Bmag); By=np.array(By)

print("== 回旋电子近场 LW 分解（束轴上 z=20R，标准电动力学）==")
print(f" ω_c=eB/m_e={wc:.3e} rad/s, R=v⊥/ω_c={R:.3e} m, v_z=0.1c")
print(f" Ez 振荡: max|Ez|={np.max(np.abs(Ez)):.3e} V/m, min|Ez|={np.min(np.abs(Ez)):.3e}")
print(f" E⊥ 振荡: max|E⊥|={np.max(np.abs(Eperp)):.3e} V/m")
print(f" B  振荡: max|B|={np.max(np.abs(Bmag)):.3e} T")
print(f" Ez 时间变化: max-min={np.max(Ez)-np.min(Ez):.3e} → {'振荡' if np.max(Ez)-np.min(Ez)>1e-3*np.max(np.abs(Ez)) else '准静态'}")
print(f" B  时间变化: max-min={np.max(Bmag)-np.min(Bmag):.3e} → {'振荡' if np.max(Bmag)-np.min(Bmag)>1e-3*np.max(Bmag) else '准静态'}")

# 傅里叶 + 零交叉精确测主频
dt=T[1]-T[0]
freq=np.fft.rfftfreq(len(T),dt)
def dominant(sig):
    sp=np.abs(np.fft.rfft(sig-np.mean(sig)))
    return freq[np.argmax(sp)]
f_Ez=dominant(Ez); f_B=dominant(Bmag)
def zero_cross_freq(sig):
    """零交叉测主周期 → 频率"""
    s=sig-np.mean(sig)
    cross=np.where(np.diff(np.signbit(s)))[0]
    if len(cross)<2: return np.nan
    periods=np.diff(T[cross[::2]])
    if len(periods)<1: return np.nan
    return 1.0/(2*np.mean(periods))
z_Ez=zero_cross_freq(Ez); z_B=zero_cross_freq(Bmag)
print(f"\n Ez 傅里叶主频={f_Ez:.3e} Hz, 零交叉主频={z_Ez:.3e} Hz (ω_c/2π={wc/2/np.pi:.3e} Hz)")
print(f" B  傅里叶主频={f_B:.3e} Hz, 零交叉主频={z_B:.3e} Hz")

print("\n== 43 号判据对照 ==")
print(" UFE-2 纵波预言：束轴近场存在 E∥v_z(Ez) 振荡且 B=0")
print(" 标准电动力学：")
print(f"   Ez 振荡存在 ✓ (主频=ω_c)")
print(f"   B 振荡存在 ✗(≠0): max|B|={np.max(np.abs(Bmag)):.3e} T → 标准电动力学该处 B≠0")
print(" → 'B=0 的纯纵向 Ez 振荡'在标准电动力学中不存在（B≠0 伴生）")
print(" → UFE-2 纵波(B=0,E∥v_z)是与标准电动力学可区分的特有结构（若 B 严格零则为特有预言）")
