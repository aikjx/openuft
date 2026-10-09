# -*- coding: utf-8 -*-
"""
openuft RGE 数值仿真 —— 攻破卷八支撑
标准模型 vs 超对称 GUT 的规范耦合统一检验
纯标准库实现（无需 numpy）
"""
import math

# GUT 归一化的规范耦合倒数 a_i^-1 随 t=ln(mu/MZ) 演化: da^-1/dt = -b_i/(2*pi)
# 标准模型系数 (b1,b2,b3)
SM_B = (41.0/10.0, -19.0/6.0, -7.0)
# 超对称(MSSM)系数
SUSY_B = (33.0/5.0, 1.0, -3.0)

# 初始值(在 MZ): alpha_i^-1
ALPHA_INV_SM = (59.0, 30.0, 8.5)

MZ = 91.1876  # GeV

def integrate(b, a_inv0, t_max, dt=0.001):
    """RK4 积分 da^-1/dt = -b/(2*pi)"""
    a = list(a_inv0)
    t = 0.0
    path = []
    while t < t_max:
        path.append((t, tuple(a)))
        def f(aa, bb):
            return -bb/(2.0*math.pi)
        # RK4
        k1 = (f(a[0],b[0]), f(a[1],b[1]), f(a[2],b[2]))
        k2 = (f(a[0]+dt/2*k1[0],b[0]), f(a[1]+dt/2*k1[1],b[1]), f(a[2]+dt/2*k1[2],b[2]))
        k3 = (f(a[0]+dt/2*k2[0],b[0]), f(a[1]+dt/2*k2[1],b[1]), f(a[2]+dt/2*k2[2],b[2]))
        k4 = (f(a[0]+dt*k3[0],b[0]), f(a[1]+dt*k3[1],b[1]), f(a[2]+dt*k3[2],b[2]))
        a[0] += dt/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        a[1] += dt/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        a[2] += dt/6*(k1[2]+2*k2[2]+2*k3[2]+k4[2])
        t += dt
    return path

def min_gap(path):
    """返回路径上三点间最大间距(归一化后的不一致度)"""
    worst = (0.0, None)
    for t, a in path:
        if t == 0: continue
        d12 = abs(a[0]-a[1])
        d23 = abs(a[1]-a[2])
        d13 = abs(a[0]-a[2])
        gap = max(d12,d23,d13)
        if gap > worst[0]:
            worst = (gap, (t,a))
    return worst

def find_cross(path):
    """找三个点间距最小的位置"""
    best = (1e9, None)
    for t, a in path:
        if t == 0: continue
        gap = max(abs(a[0]-a[1]), abs(a[1]-a[2]), abs(a[0]-a[2]))
        if gap < best[0]:
            best = (gap, (t,a))
    return best

def mu_from_t(t):
    return MZ*math.exp(t)

print("="*64)
print("A. 标准模型(SM) 三线跑动: t_max=ln(1e19/MZ)")
path_sm = integrate(SM_B, ALPHA_INV_SM, math.log(1e19/MZ))
best_sm = find_cross(path_sm)
gap_sm, (ts, as_)= best_sm
print(f"   最接近交点: t={ts:.3f}  mu={mu_from_t(ts):.3e} GeV")
print(f"   该处三线间距: {gap_sm:.3f}")
print(f"   alpha1^-1={as_[0]:.2f}  alpha2^-1={as_[1]:.2f}  alpha3^-1={as_[2]:.2f}")
print(f"   是否统一(间距<0.5): {'是' if gap_sm<0.5 else '否'}")
print()

print("B. 超对称 GUT(MSSM) 三线跑动: 1TeV阈值后 t_max=ln(1e19/1TeV)")
# MSSM 在 ~1TeV 接入(取 msusy=1TeV), 初值从 SM 在 1TeV 处续接
t_tev = math.log(1000.0/MZ)
path_sm_to_tev = integrate(SM_B, ALPHA_INV_SM, t_tev)
a_at_tev = list(path_sm_to_tev[-1][1])
path_susy = integrate(SUSY_B, tuple(a_at_tev), math.log(1e19/1000.0), dt=0.001)
best_susy = find_cross(path_susy)
gap_susy, (tsu, asu) = best_susy
print(f"   SM在1TeV处: a^-1={[round(x,2) for x in a_at_tev]}")
print(f"   最接近交点: t(自1TeV)={tsu:.3f}  mu={1000*math.exp(tsu):.3e} GeV")
print(f"   该处三线间距: {gap_susy:.3f}")
print(f"   alpha1^-1={asu[0]:.2f}  alpha2^-1={asu[1]:.2f}  alpha3^-1={asu[2]:.2f}")
print(f"   是否统一(间距<0.5): {'是' if gap_susy<0.5 else '否'}")
print(f"   统一尺度 M_GUT={1000*math.exp(tsu):.2e} GeV, alpha_GUT^-1={asu[0]:.1f}")
print("="*64)
print("攻破结论: 标准模型三线不精确相交; 超对称 GUT 在 ~2e16 GeV 近似统一。")
