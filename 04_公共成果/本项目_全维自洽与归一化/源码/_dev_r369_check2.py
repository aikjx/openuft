# -*- coding: utf-8 -*-
"""_dev_r369_check2 —— 第二轮试算（跑通后删除）"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
import mpmath as mp
mp.mp.dps = 70

# ---------- 1) 2q = (1+q^2)a ----------
a, g = sp.symbols("a g", positive=True)
q = a / (1 + g)
expr = sp.simplify(sp.expand((2 * q - (1 + q**2) * a) * (1 + g)**2).subs(g, sp.sqrt(1 - a**2)))
print("2q identity residual =", expr)

# ---------- 2) 磁矩系数 ----------
AL = mp.mpf(1) / mp.mpf("137.035999177")
G = mp.sqrt(1 - AL * AL)
mu_rel = (1 + 2 * G) / 3
print("mu/mu_B coefficient =", mp.nstr(mu_rel, 20), " deviate from 1 =", mp.nstr(1 - mu_rel, 12))
ME = mp.mpf("9.1093837015e-31"); EE = mp.mpf("1.602176634e-19"); HB = mp.mpf("1.054571817e-34")
muB = EE * HB / (2 * ME)
print("mu_B(e,hbar,m_e) =", mp.nstr(muB, 15), " CODATA 9.2740100783e-24 rel =",
      mp.nstr((muB - mp.mpf("9.2740100783e-24")) / mp.mpf("9.2740100783e-24"), 5))

# ---------- 3) Dirac 残差 诊断：小 r 处 ----------
def mk(ALv):
    Gv = mp.sqrt(1 - ALv * ALv); Qv = ALv / (1 + Gv)
    Nv = mp.sqrt((2 * ALv) ** (2 * Gv + 1) / ((1 + Qv * Qv) * mp.gamma(2 * Gv + 1)))
    PF = Nv / mp.sqrt(4 * mp.pi)
    rad = lambda r: PF * r**(Gv - 1) * mp.e**(-ALv * r)
    def n1(x, y, z): return rad(mp.sqrt(x * x + y * y + z * z))
    def z0(x, y, z): return mp.mpf(0)
    def p3i(x, y, z):
        r = mp.sqrt(x * x + y * y + z * z); return Qv * (z / r) * rad(r)
    def p4r(x, y, z):
        r = mp.sqrt(x * x + y * y + z * z); return -Qv * (y / r) * rad(r)
    def p4i(x, y, z):
        r = mp.sqrt(x * x + y * y + z * z); return Qv * (x / r) * rad(r)
    return ALv, Gv, [(n1, z0), (z0, z0), (z0, p3i), (p4r, p4i)]

def resid(ALv, Gv, CP, pt, h):
    def pder(f, x, y, z, var):
        if var == 0:
            return (f(x - 2*h, y, z) - 8*f(x - h, y, z) + 8*f(x + h, y, z) - f(x + 2*h, y, z)) / (12*h)
        if var == 1:
            return (f(x, y - 2*h, z) - 8*f(x, y - h, z) + 8*f(x, y + h, z) - f(x, y + 2*h, z)) / (12*h)
        return (f(x, y, z - 2*h) - 8*f(x, y, z - h) + 8*f(x, y, z + h) - f(x, y, z + 2*h)) / (12*h)
    def dv(k, x, y, z, var):
        re, im = CP[k]; return mp.mpc(pder(re, x, y, z, var), pder(im, x, y, z, var))
    x, y, z = pt
    ps = [mp.mpc(CP[k][0](x, y, z), CP[k][1](x, y, z)) for k in range(4)]
    d = [[dv(k, x, y, z, v) for v in range(3)] for k in range(4)]
    r = mp.sqrt(x * x + y * y + z * z); I = mp.mpc(0, 1); E = Gv
    L = [-I * (d[2][2] + (d[3][0] - I * d[3][1])) + ps[0] - ALv / r * ps[0] - E * ps[0],
         -I * ((d[2][0] + I * d[2][1]) - d[3][2]) - ALv / r * ps[1] - E * ps[1],
         -I * (d[0][2] + (d[1][0] - I * d[1][1])) - ps[2] - ALv / r * ps[2] - E * ps[2],
         -I * ((d[0][0] + I * d[0][1]) - d[1][2]) - ps[3] - ALv / r * ps[3] - E * ps[3]]
    out = []
    for k in range(4):
        den = sum(abs(d[k][v]) for v in range(3)) + abs(ps[k]) + abs(ALv / r * ps[k]) + abs(E * ps[k])
        out.append(abs(L[k]) / den if den > 0 else mp.mpf(0))
    return max(out), [abs(q_) for q_ in L], 0

AL0, G0, CP0 = mk(AL)
for pt in [(0.5, 0.3, 0.7), (2, 1, 1), (10, 4, 9), (100, 40, 90)]:
    for h in [mp.mpf("1e-15"), mp.mpf("1e-18"), mp.mpf("1e-25")]:
        mx, ab, _ = resid(AL0, G0, CP0, pt, h)
        print("pt", pt, "h", mp.nstr(h, 3), "rel", mp.nstr(mx, 5), "abs", mp.nstr(max(ab), 5))

# ---------- 4) Raychaudhuri（带投影） ----------
t, x, y, z, W = sp.symbols("t x y z Omega", real=True)
Gs = 1 / sp.sqrt(1 - W**2 * (x**2 + y**2))
ue = sp.Matrix([Gs, -W * y * Gs, W * x * Gs, 0])
ul = sp.Matrix([Gs, W * y * Gs, -W * x * Gs, 0])
co = [t, x, y, z]
sg = [1, -1, -1, -1]
gm = sp.Matrix(4, 4, lambda i, j: sg[i] if i == j else 0)
hm = sp.Matrix(4, 4, lambda i, j: gm[i, j] + ul[i] * ul[j])
Th = sp.simplify(sum(sp.diff(ue[i], co[i]) for i in range(4)))
dd = sp.Matrix(4, 4, lambda nu, mu: sp.diff(ul[mu], co[nu]))   # dd[nu,mu]=d_nu u_mu
def proj(M):
    return sp.Matrix(4, 4, lambda mu, nu: sp.expand(sum(hm[mu, p] * hm[nu, s] * M[p, s] for p in range(4) for s in range(4))))
om = sp.Matrix(4, 4, lambda mu, nu: sp.expand((dd[nu, mu] - dd[mu, nu]) / 2))
si_raw = sp.Matrix(4, 4, lambda mu, nu: sp.expand((dd[nu, mu] + dd[mu, nu]) / 2))
om = proj(om); si = proj(si_raw)
si = sp.Matrix(4, 4, lambda mu, nu: sp.expand(si[mu, nu] - (Th / 3) * hm[mu, nu]))
om2 = sp.simplify(sum(om[i, j] * sg[i] * sg[j] * om[i, j] for i in range(4) for j in range(4)))
si2 = sp.simplify(sum(si[i, j] * sg[i] * sg[j] * si[i, j] for i in range(4) for j in range(4)))
acc = sp.Matrix([sum(ue[nu] * sp.diff(ue[mu], co[nu]) for nu in range(4)) for mu in range(4)])
diva = sp.simplify(sum(sp.diff(acc[mu], co[mu]) for mu in range(4)))
bal = sp.simplify(-Th**2 / 3 - si2 + om2 + diva)
print("Theta =", Th)
print("omega^2 =", om2)
print("sigma^2 =", si2)
print("div a   =", diva)
print("balance =", bal)
fb = sp.lambdify((x, y, W), bal, "mpmath")
fo = sp.lambdify((x, y, W), om2, "mpmath")
fs = sp.lambdify((x, y, W), si2, "mpmath")
fdi = sp.lambdify((x, y, W), diva, "mpmath")
for (xx, yy, ww) in [(mp.mpf("0.3"), mp.mpf("0.2"), mp.mpf("0.4")), (mp.mpf("1"), mp.mpf("1"), mp.mpf("0.2")),
                     (mp.mpf("0.1"), mp.mpf("0.05"), mp.mpf("0.9"))]:
    print("num:", mp.nstr(fb(xx, yy, ww), 5), "om2", mp.nstr(fo(xx, yy, ww), 8),
          "si2", mp.nstr(fs(xx, yy, ww), 8), "diva", mp.nstr(fdi(xx, yy, ww), 8))

# ---------- 5) V31 数值 ----------
G_N = mp.mpf("6.67430e-11"); MP = mp.mpf("1.67262192369e-27")
KE = mp.mpf("8.9875517873681764e9"); ECH = mp.mpf("1.602176634e-19")
MEVFM = mp.mpf("160.2176634"); HBC = mp.mpf("197.3269804")
rf = mp.mpf("1e-15")
fg = G_N * MP * MP / rf**2
fc = KE * ECH * ECH / rf**2
LamPi = HBC / mp.mpf("139.57039")   # fm
Ay = mp.mpf("50") * HBC              # MeV*fm = MeV*fm ; convert
Ay_Nm = mp.mpf("50") * MEVFM * mp.mpf("1e-15") / mp.mpf("1e-15")  # MeV*fm -> N*m^2? 见下
# A 单位 MeV*fm：V = -A e^{-r/L}/r，r、L 用 fm ⇒ V[MeV]; F = -dV/dr [MeV/fm] -> N 乘 MEVFM
fy = mp.mpf("50") * mp.e**(-mp.mpf("1") / LamPi) * (mp.mpf("1") / mp.mpf("1")**2 + 1 / (LamPi * mp.mpf("1")))
fyN = fy * MEVFM
alphaS = mp.mpf("0.30"); sig = mp.mpf("900")
k_C = mp.mpf(4) / 3 * alphaS * HBC       # MeV*fm
fcorn = (k_C / mp.mpf("1")**2 + sig * mp.mpf("1")) * MEVFM
print("F_g =", mp.nstr(fg, 10), " F_C =", mp.nstr(fc, 10))
print("LamPi fm =", mp.nstr(LamPi, 10), " F_y =", mp.nstr(fyN, 10), " F_corn =", mp.nstr(fcorn, 10))
MW = mp.mpf("80360.2")
lamW = HBC / MW   # fm
print("lambda_W =", mp.nstr(lamW * mp.mpf("1e-15"), 8), "m")
# 磁场螺旋
B = mp.mpf("0.5"); vp = mp.mpf("0.1"); uu = mp.mpf("0.05"); C = mp.mpf("299792458")
gm_ = 1 / mp.sqrt(1 - vp**2 - uu**2)
omc = ECH * B / (gm_ * ME)
Rv = vp * C / omc; pv = 2 * mp.pi * uu * C / omc
print("gamma =", mp.nstr(gm_, 10), "omega_c =", mp.nstr(omc, 10), "R mm =", mp.nstr(Rv * 1e3, 10),
      "p mm =", mp.nstr(pv * 1e3, 10), "ratio =", mp.nstr(vp / uu, 10))
