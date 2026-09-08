# -*- coding: utf-8 -*-
"""
R11 高精度补充：mpmath 50位精度验证梯度磁场三重奏修正
用 mpmath 克服 float64 差分精度极限（~2e-5），定量测量物理修正。
1/4 圈，dt=1e-15，g=50。
"""
from mpmath import mp, mpf

mp.dps = 50

q_m = mpf('-1.758820e11')
B0 = mpf('1.0')
g = mpf('50.0')
v_perp = mpf('1e7')
v_par = mpf('5e6')
omega0 = abs(q_m) * B0
dt = mpf('1e-15')
t_end = (mp.pi / 2) / omega0   # 1/4 圈
n = int(t_end / dt)

print("mpmath 精度: %d 位" % mp.dps)
print("步数: %d, t_end=%.6e s, ωΔt=%.6e" % (n, float(t_end), float(omega0*dt)))

def rhs(state):
    x, y, z, vx, vy, vz = state
    Bz = B0 + g * x
    ax = q_m * vy * Bz
    ay = -q_m * vx * Bz
    az = mpf('0')
    return [vx, vy, vz, ax, ay, az]

def rk4(s, dt):
    k1 = rhs(s)
    s2 = [s[i] + 0.5*dt*k1[i] for i in range(6)]
    k2 = rhs(s2)
    s3 = [s[i] + 0.5*dt*k2[i] for i in range(6)]
    k3 = rhs(s3)
    s4 = [s[i] + dt*k3[i] for i in range(6)]
    k4 = rhs(s4)
    return [s[i] + (dt/6)*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(6)]

# 积分
traj = []
state = [mpf('0'), mpf('0'), mpf('0'), v_perp, mpf('0'), v_par]
for i in range(n):
    traj.append(state[:3])
    state = rk4(state, dt)
print("积分完成，轨迹点数=%d" % len(traj))

# Frenet 差分（四阶中心差分，取中间点 i=n//2）
i = n // 2
def diff_v(i):
    return [(-traj[i+2][d]+8*traj[i+1][d]-8*traj[i-1][d]+traj[i-2][d])/(12*dt) for d in range(3)]
def diff_a(i):
    return [(-traj[i+2][d]+16*traj[i+1][d]-30*traj[i][d]+16*traj[i-1][d]-traj[i-2][d])/(12*dt**2) for d in range(3)]
def diff_j(i):
    return [(-traj[i+3][d]+8*traj[i+2][d]-13*traj[i+1][d]+13*traj[i-1][d]-8*traj[i-2][d]+traj[i-3][d])/(8*dt**3) for d in range(3)]

v = diff_v(i)
a = diff_a(i)
j = diff_j(i)
vv = [v[1]*a[2]-v[2]*a[1], v[2]*a[0]-v[0]*a[2], v[0]*a[1]-v[1]*a[0]]
nv2 = sum(vv[k]**2 for k in range(3))
v2 = sum(v[k]**2 for k in range(3))
kap2 = nv2 / v2**3
tau2 = (sum(vv[k]*j[k] for k in range(3)))**2 / nv2**2
lhs = kap2 + tau2
x_pos = traj[i][0]
w = abs(q_m) * (B0 + g * x_pos)
rhs_ = w**2 / v2
rel = abs(lhs - rhs_) / rhs_

print("")
print("=== 中间点 (i=%d, t=%.3e s) ===" % (i, float(i*dt)))
print("  x=%.6e m, B(x)=%.6f T, ω(x)=%.6e rad/s" % (float(x_pos), float(B0+g*x_pos), float(w)))
print("  |v|=%.6e m/s" % float(v2**0.5))
print("  κ²=%.10e" % float(kap2))
print("  τ²=%.10e" % float(tau2))
print("  κ²+τ²=%.10e" % float(lhs))
print("  (ω/v)²=%.10e" % float(rhs_))
print("  相对差=%.6e" % float(rel))

# 多采样点统计
print("")
print("=== 多采样点统计（10个点，均匀分布）===")
rels = []
for k in range(10):
    ii = n//4 + k * (n//2)//9
    vv2 = diff_v(ii); aa = diff_a(ii); jj = diff_j(ii)
    vvv = [vv2[1]*aa[2]-vv2[2]*aa[1], vv2[2]*aa[0]-vv2[0]*aa[2], vv2[0]*aa[1]-vv2[1]*aa[0]]
    nn2 = sum(vvv[l]**2 for l in range(3))
    vv2s = sum(vv2[l]**2 for l in range(3))
    k2 = nn2 / vv2s**3
    t2 = (sum(vvv[l]*jj[l] for l in range(3)))**2 / nn2**2
    xx = traj[ii][0]
    ww = abs(q_m)*(B0+g*xx)
    rr = ww**2/vv2s
    rels.append(float(abs(k2+t2-rr)/rr))
    print("  i=%-6d x=%-12.4e rel=%-12.4e" % (ii, float(xx), rels[-1]))
import statistics
print("  中位=%.4e  最大=%.4e  最小=%.4e" % (statistics.median(rels), max(rels), min(rels)))
print("")
print("结论: mpmath 50位精度下，梯度B(g=50)三重奏相对差中位=%.2e" % statistics.median(rels))
print("  若 >> 1e-10 则为物理修正；若 ~1e-10 则为数值噪声。")
