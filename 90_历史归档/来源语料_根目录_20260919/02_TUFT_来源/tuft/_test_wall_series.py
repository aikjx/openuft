"""临时验证：Leaver 连分式确定最小解首比 a1/a0，再前向递推，级数在墙 x_s 处求值。"""
import numpy as np
import tuft_r26_leaver_wall_qnm as m


def wall_series(omega, x_s, N, af, bf, gf, M_cf=4000):
    # 连分式尾 R_0 = a1/a0（最小解），R_{n-1} = -gamma_n/(beta_n + alpha_n R_n)
    t = 0.0 + 0j
    for n in range(M_cf, 0, -1):
        an = complex(af(n, omega))
        bn = complex(bf(n, omega))
        gn = complex(gf(n, omega))
        t = -gn / (bn + an * t)
    R0 = t
    # 前向递推最小解系数
    a = [0.0 + 0j] * (N + 1)
    a[0] = 1.0 + 0j
    a[1] = R0
    for n in range(1, N):
        an = complex(af(n, omega))
        bn = complex(bf(n, omega))
        gn = complex(gf(n, omega))
        a[n + 1] = -(bn * a[n] + gn * a[n - 1]) / an
    S = 0.0 + 0j
    xp = 1.0 + 0j
    for n in range(N + 1):
        S = S + a[n] * xp
        xp = xp * x_s
    return S


ga, gb, gc, _ = m.make_solver(2)
x_s = 1.0 - 2.0 / 2.05
print("x_s =", x_s)
wgr = complex(0.373672, -0.088962)
print("GR QNM 处墙级数 =", wall_series(wgr, x_s, 1500, ga, gb, gc))

best = None
bestv = 1e30
bw = None
for wr in np.linspace(0.36, 0.46, 51):
    for wi in np.linspace(-0.06, -0.005, 56):
        w = complex(wr, wi)
        v = abs(wall_series(w, x_s, 1500, ga, gb, gc))
        if v < bestv:
            bestv = v
            bw = w
print("粗扫最小 |S| @", bw, "=", bestv)
for N in (800, 1500, 3000, 6000):
    v = abs(wall_series(bw, x_s, N, ga, gb, gc))
    print("N=%d |S|=%.3e" % (N, v))
