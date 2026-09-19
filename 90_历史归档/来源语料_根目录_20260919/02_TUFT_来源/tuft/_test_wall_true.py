"""验证：反射壁腔模真根判据——|Psi_wall(omega, u_max)| 应随 u_max->inf 趋于 0（真 QNM），
箱模则仅在其特定 u_max 为根、随 u_max 漂移。用 tortois 坐标精确出波 BC 的射击法。"""
import numpy as np
import tuft_r26_leaver_wall_qnm as m

r_s = 2.05
V = m.make_V(2, "RW")

def shoot(omega, r_max, dr=0.04):
    M = 1.0
    u_s = r_s + 2.0 * M * np.log(r_s / (2.0 * M) - 1.0)
    u_max = float(r_max)
    n = int(round((u_max - u_s) / dr))
    if n < 1:
        n = 1
    u_edges = np.linspace(u_max, u_s, n + 1)
    r_edges = np.array([2.0*M*(1.0+float(np.exp((uu-2.0*M)/(2.0*M)))) for uu in u_edges])
    V_arr = np.array([complex(V(rr)) for rr in r_edges])
    P = 1.0+0j
    dP = 1j*omega*P
    def rhs(Pv, dPv, Vv):
        return dPv, -(omega**2 - Vv)*Pv
    for k in range(n):
        h = u_edges[k+1]-u_edges[k]
        Vv = V_arr[k]; Vv2 = V_arr[min(k+1, n)]
        k1P,k1d = rhs(P, dP, Vv)
        k2P,k2d = rhs(P+h/2*k1P, dP+h/2*k1d, Vv2)
        k3P,k3d = rhs(P+h/2*k2P, dP+h/2*k2d, Vv2)
        k4P,k4d = rhs(P+h*k3P, dP+h*k3d, Vv2)
        P = P+h/6*(k1P+2*k2P+2*k3P+4*k3P)
        dP = dP+h/6*(k1d+2*k2d+2*k3d+4*k3d)
    return P

cands = [complex(0.40794, -0.02606), complex(0.409880, -0.029576),
         complex(0.450789, -0.008711), complex(0.41, -0.03), complex(0.40, -0.10)]
print("candidate  vs  |Psi| at u_max = 200, 400, 800, 1600, 3200")
for w in cands:
    vals = []
    for um in (200, 400, 800, 1600, 3200):
        p = shoot(w, um)
        vals.append("%.3e" % abs(p))
    print("%9s%9s  | " % (("%.3f" % w.real), ("%.4f" % w.imag)), " ".join(vals))
