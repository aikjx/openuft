# -*- coding: utf-8 -*-
# TUFT V3.2 —— 形状通道数值定位：刚性均匀带电球壳做匀加速，逐电荷元 LW 远场辐射
# 结论（对照同目录 15B 文档 §6C）：球对称+刚性下，把球壳尺寸放大到 a_s/R_obs=0.05，
# 总辐射仍=点电荷 Larmor（偏差~1e-3，无 C~13.8 修正）。形状修正唯一合法来源：
# (1)非球对称结构（磁偶极/电四极）(2)非绝热形变。
import numpy as np
c=299792458.0; eps0=8.8541878128e-12
Q=1.0; a_acc=1e9

def P_point():
    return Q**2*a_acc**2/(6*np.pi*eps0*c**3)

def shell_E_rad_dir(n_obs, R_obs, a_s, npts=4000):
    idx=np.arange(npts)
    zz=1-2*(idx+0.5)/npts
    rr=np.sqrt(1-zz**2)
    phi=np.pi*(1+5**0.5)*idx
    sx=a_s*rr*np.cos(phi); sy=a_s*rr*np.sin(phi); sz=a_s*zz
    Rx=R_obs*n_obs[0]-sx; Ry=R_obs*n_obs[1]-sy; Rz=R_obs*n_obs[2]-sz
    R=np.sqrt(Rx**2+Ry**2+Rz**2)
    nx=Rx/R; ny=Ry/R; nz=Rz/R
    nxa=nx*a_acc
    Ex=nx*nxa-a_acc; Ey=ny*nxa; Ez=nz*nxa
    coeff=(Q/npts)/(4*np.pi*eps0*c**2)
    return np.array([np.sum(coeff*Ex/R), np.sum(coeff*Ey/R), np.sum(coeff*Ez/R)])

def P_shell(R_obs,a_s,n_th=64,n_ph=128,npts=4000):
    P=0.0
    for i in range(n_th):
        th=(i+0.5)*np.pi/n_th
        for j in range(n_ph):
            ph=j*2*np.pi/n_ph
            n=np.array([np.sin(th)*np.cos(ph),np.sin(th)*np.sin(ph),np.cos(th)])
            E=shell_E_rad_dir(n,R_obs,a_s,npts)
            dOmega=np.sin(th)*(np.pi/n_th)*(2*np.pi/n_ph)
            P+=eps0*c*np.dot(E,E)*R_obs**2*dOmega
    return P

Pp=P_point()
print(f"P_point = {Pp:.8e}")
for ratio in [1e-4,1e-3,1e-2,0.05]:
    R_obs=1e10; a_s=R_obs*ratio
    Ps=P_shell(R_obs,a_s)
    print(f"a_s/R={ratio:.0e}: P_shell/P_point = {Ps/Pp:.8f}  偏差={Ps/Pp-1:.3e}")
