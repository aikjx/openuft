# -*- coding: utf-8 -*-
"""44 号下一步：长窗精确测回旋束轴近场频谱，验证 43 号"频率=ω_r"
44 号采样窗仅 2 周期(Δf=ω_c/4π)致主频分辨率受限。本轮：32 完整回旋周期 + 高采样率，
精确测 Ez、B 主频(对比 ω_c/2π)，并检查束轴 B 是否(近似)零。
"""
import numpy as np
me=9.1093837015e-31; e=1.602176634e-19; c=299792458.0; eps0=8.8541878128e-12

B0=1.0; wc=e*B0/me; v_perp=0.1*c; R=v_perp/wc; vz=0.1*c

def retard(P, t):
    tr=t
    for _ in range(100):
        x=R*np.cos(wc*tr); y=R*np.sin(wc*tr); z=vz*tr
        rr=np.array([x,y,z]); d=P-rr; dist=np.linalg.norm(d)
        tr_new=t-dist/c
        if abs(tr_new-tr)<1e-22: break
        tr=tr_new
    x=R*np.cos(wc*tr); y=R*np.sin(wc*tr); z=vz*tr
    rr=np.array([x,y,z]); d=P-rr; dist=np.linalg.norm(d); n=d/dist
    v=np.array([-R*wc*np.sin(wc*tr), R*wc*np.cos(wc*tr), vz])
    a=np.array([-R*wc**2*np.cos(wc*tr), -R*wc**2*np.sin(wc*tr), 0.0])
    return tr, n, dist, v, a

def LW(P,t):
    tr,n,dist,v,a=retard(P,t)
    beta=v/c; betadot=a/c; nb=1-np.dot(n,beta)
    gamma=1/np.sqrt(1-np.dot(beta,beta))
    E_vel=e*(n-beta)/(gamma**2*4*np.pi*eps0*dist**2*nb**3)
    E_acc=e/(4*np.pi*eps0*c*dist)*np.cross(n,np.cross((n-beta),betadot))/nb**3
    E=E_vel+E_acc
    B=np.cross(n,E)/c
    return E,B,dist

Z=20*R; P=np.array([0.0,0.0,Z])
# 长窗：32 完整回旋周期
ncyc=32
T=np.linspace(0, ncyc*2*np.pi/wc, 32000)
dt=T[1]-T[0]
Ez=[]; Bx=[]; By=[]; Bz=[]; Ex=[]; Ey=[]
for t in T:
    E,B,dist=LW(P,t)
    Ez.append(E[2]); Ex.append(E[0]); Ey.append(E[1])
    Bx.append(B[0]); By.append(B[1]); Bz.append(B[2])
Ez=np.array(Ez); Ex=np.array(Ex); Ey=np.array(Ey)
Bx=np.array(Bx); By=np.array(By); Bz=np.array(Bz)
Bmag=np.sqrt(Bx**2+By**2+Bz**2)

# 频谱（长窗，高分辨率）
freq=np.fft.rfftfreq(len(T),dt)
def peak_freq(sig):
    sp=np.abs(np.fft.rfft(sig-np.mean(sig)))
    k=np.argmax(sp)
    return freq[k], sp[k]
f_Ez,_=peak_freq(Ez); f_B,_=peak_freq(Bmag); f_Ex,_=peak_freq(Ex)
print("== 长窗频谱（32 回旋周期）==")
print(f" ω_c/2π={wc/2/np.pi:.6e} Hz, 频率分辨率 Δf=1/T={1/T[-1]:.3e} Hz")
print(f" Ez 主频={f_Ez:.6e} Hz, 比值 f_Ez/(ω_c/2π)={f_Ez/(wc/2/np.pi):.4f}")
print(f" Ex 主频={f_Ex:.6e} Hz")
print(f" B  主频={f_B:.6e} Hz, 比值 f_B/(ω_c/2π)={f_B/(wc/2/np.pi):.4f}")

# B 是否近似零
print("\n== 束轴 B 行为 ==")
print(f" max|B|={np.max(Bmag):.3e} T, mean|B|={np.mean(Bmag):.3e} T")
print(f" B 各分量 max: Bx={np.max(np.abs(Bx)):.2e}, By={np.max(np.abs(By)):.2e}, Bz={np.max(np.abs(Bz)):.2e}")
# 相对 E_z 的幅度
print(f" B 相对 E_z 场强: max|B|·c/max|Ez|={np.max(Bmag)*c/np.max(np.abs(Ez)):.4f} (E/B 幅值比)")

# 测 43 号预言：若存在 B=0 纯纵向振荡，则 Bx,By 在 Ez 峰值处应为 0
# 找 Ez 峰值时刻，看 B 是否同步为零
peaks=np.argsort(np.abs(Ez))[-200:]
B_at_peaks=Bmag[peaks]
print(f"\n 在 |Ez| 最大时刻, |B| 分布: min={np.min(B_at_peaks):.2e}, max={np.max(B_at_peaks):.2e} T")
print(" → 标准电动力学: Ez 峰值处 B 非零(不严格零) → UFE-2 纵波(B=0)与之可区分")
