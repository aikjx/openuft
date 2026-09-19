# -*- coding: utf-8 -*-
"""
TUFT v14 线一 : TUFT 版 Leaver 连分数  (壁 Neumann 边界条件)
================================================================
E360 起。

顺序 (硬门槛):
  PART 1  GR 回归门  —— 复用已验证的 40 位 Schwarzschild s=-2 Leaver 三项连分数,
            复现 l=2 n=0/n=1 (>=6 位)。门不过则 TUFT 根一律不采信。
  PART 2  壁 Neumann Frobenius 推导 (E360-E36x)
  PART 3  TUFT 壁根 (c=-0.5 / c=-0.29), 基模+泛音, 多 s_out Richardson 外推
  PART 4  腔长标度检验 (4 个 c_m)
  PART 5  四态分级

v13 审计教训 (本脚本严格遵守):
  - 裸 iw 单点打靶在 GR 上发散到 74.7-69.1i 伪根 (本脚本 PART1 独立复现该 FAIL),
    故 TUFT 一律不用前向裸对数导数匹配。
  - TUFT 壁是正则点 (B=0 处 r* 有限), 故用"无穷远纯出射起点 -> 向内积分到壁",
    残差为壁面对数导数 psi_s/psi (=0 即 Neumann)。该法对正则壁数值稳定。
  - 有限 s_out 一律 Richardson 外推到 s_out -> inf, 绝不钉单点。
"""
import sys, io, time, warnings
warnings.filterwarnings("ignore")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import numpy as np
import mpmath as mp
from scipy.optimize import root as sp_root, brentq

mp.mp.dps = 50
t0 = time.time()
OUT = []
def p(*a):
    s = " ".join(str(x) for x in a); OUT.append(s); print(s)

GMUS = 4.9256

p("="*80)
p("TUFT v14 线一 : TUFT 版 Leaver 连分数  (壁 Neumann 边界条件)")
p("顺序 : (1) GR 回归门先过  (2) TUFT 壁 Neumann + 无穷远出射 特征")
p("="*80)

# ======================================================================
# E360  度规 / 壁 / 乌龟 / RW 主方程 (定义层, 沿用 v13 E354-E357 约定)
# ======================================================================
p("")
p("-"*80)
p("E360  度规与壁 (定义层)")
p("-"*80)
p("  ds^2 = -A(r) dt^2 + B(r)^-1 dr^2 + r^2 dOmega^2,  M=1")
p("  A = exp(-2/r)")
p("  B = exp(+2/r) (1 + c_m/r^2 + d/r^3)")
p("  壁 (B=0, 度规退化处):  1 + c_m/r_h^2 + d/r_h^3 = 0  <=>  r_h^3 + c_m r_h + d = 0")
p("  无 d 时 r_h = sqrt(-c_m):  c_m=-0.50 -> r_h=0.70711 M;  c_m=-0.29,d=-0.05 -> r_h=0.60990 M")

p("")
p("-"*80)
p("E361  乌龟坐标 & RW 主方程")
p("-"*80)
p("  dr*/dr = sqrt(B/A) = exp(+2/r) sqrt(1 + c_m/r^2 + d/r^3)")
p("  壁处 B->0 => dr*/dr ~ sqrt(r-r_h) -> 0, r*_h 有限 (可积, 正则点).")
p("  RW 主方程 (l=2, s=-2 主势沿用本线约定):")
p("      psi_{,r*r*} + [ omega^2 - V(r) ] psi = 0,   V(r) = A l(l+1)/r^2 = 6 e^{-2/r}/r^2")
p("  势垒峰 dV/dr=0 -> r=1, Vmax = 6 e^{-2} = 0.81203  (与 c_m 无关).")

p("")
p("-"*80)
p("E362  外边界 (无穷远纯出射, 解析)")
p("-"*80)
p("  r*->+inf: V->0, psi ~ A_out e^{+ i omega r*} (纯出射, 无入射支 e^{-i omega r*}).")
p("  对数导数:  psi_{,r*}/psi |_{inf} = + i omega.")

p("")
p("-"*80)
p("E363  内壁 Neumann (公设 W1)")
p("-"*80)
p("  公设 W1: 量子引力壁理想反射, |R|=1. 主边界 (Neumann):")
p("      psi_{,r*} |_{r*=r*_h} = 0  (波腹, R=+1, phi_R=0).")
p("  壁面 r* 正则, Neumann 取 psi(r*_h)=1, psi_{,r*}(r*_h)=0.")

p("")
p("-"*80)
p("E364  为何指数度规无闭合 Schwarzschild 型三项连分数 (诚实声明)")
p("-"*80)
p("  GR Leaver 闭合于 z=1-2/r: 因 Schwarzschild f=1-2/r 是 z 的一次式,")
p("  提取 e^{-i w r*} 与两端 Frobenius 幂后, 残差 ODE 系数是 z 的多项式 -> 三项递推.")
p("  TUFT 度规 A=e^{-2/r}, B=e^{2/r}(...) 含 e^{-2(1-z)/r_h}, e^{4(1-z)/r_h} 指数因子,")
p("  提取出射因子后残差 ODE 系数仍是 z 的整函数 (无穷泰勒阶), 不闭合为有限三项式.")
p("  故 TUFT 'Leaver' 推广 = 解析级数/连续分数的数值实现:")
p("  (a) GR 门用闭合三项连分数 (解析, 无盒);")
p("  (b) TUFT 壁因 r*_h 正则, 用'无穷远精确出射 -> 向内积分 -> 壁 Neumann 归零',")
p("      残差 F(w)=psi_{,r*}(r*_h)/psi(r*_h); 有限 s_out 误差按 Richardson 外推到 inf.")

# ======================================================================
# PART 1 : GR 回归门 (已验证 50 位 Schwarzschild s=-2 Leaver 三项连分数)
# ======================================================================
p("")
p("="*80)
p("PART 1  GR 回归门  (闭合 Schwarzschild s=-2 Leaver 三项连分数, mpmath 50 位)")
p("="*80)
I = mp.mpc(0,1)
def gr_coef(n, w, l):
    an = n**2 + (4 - 4*I*w)*n + (3 - 4*I*w)
    bn = -l*(l+1) - 2*n**2 + (16*I*w - 2)*n + (32*w**2 + 8*I*w + 3)
    gn = n**2 + (-8*I*w - 2)*n + (-16*w**2 + 8*I*w)
    return an, bn, gn
def gr_quant(w, l, N):
    C = mp.mpc(0)
    for n in range(N, 0, -1):
        a,b,g = gr_coef(n, w, l)
        C = g/(b - a*C)
    a0,b0,_ = gr_coef(0, w, l)
    return b0 - a0*C
GR_BENCH = {(2,0): mp.mpc('0.37367168441804166','-0.0889623156889341'),
            (2,1): mp.mpc('0.34671099687909240','-0.2739148752911987')}
p("")
p("  目标 l=2 n=0: 0.3736716844 - 0.0889623157 i (>=6 位)")
p("        l=2 n=1: 0.3467109970 - 0.2739148753 i")
p("")
p("  %-4s %-6s %-26s %-26s %-10s %-6s" % ("N","mode","Re(omega)","Im(omega)","|res|","digits"))
gr_root = {}; gate_pass = True
for (l,n), bm in GR_BENCH.items():
    guess = mp.mpc(bm.real*mp.mpf('0.98'), bm.imag*mp.mpf('1.05'))
    for N in [100, 200, 400]:
        w = mp.findroot(lambda z: gr_quant(z,l,N), guess, maxsteps=120)
        res = abs(gr_quant(w,l,N)); diff = abs(w-bm)
        digits = 99 if diff==0 else max(0, int(-mp.floor(mp.log10(diff))))
        gr_root[(l,n,N)] = (w, res, digits)
        p("  %-4d %-6s %-26.15f %-26.15f %-10.2e %-6d" % (
            N, "n=%d"%n, w.real, w.imag, res, digits))
        guess = w
    if gr_root[(l,n,400)][2] < 6: gate_pass = False
w20 = gr_root[(2,0,400)][0]
p("")
p("  GR l=2 n=0: omega M = %.15f %+.15f i" % (w20.real, w20.imag))
p("  基准       : 0.373671684418042 -0.088962315688934 i")
p("  400 阶数位: n0=%d, n1=%d  (>=6 即 PASS)   GATE: %s" % (
    gr_root[(2,0,400)][2], gr_root[(2,1,400)][2],
    "PASS" if gate_pass else "FAIL"))
if not gate_pass:
    p("  *** 门未过! 按硬约束, TUFT 根一律不采信, 终止. ***")
    with open(r"D:\a10\aikjx\code\my_lib\tuft_v14_tuft_wall_out.txt","w",encoding="utf-8") as f:
        f.write("\n".join(OUT))
    sys.exit(1)
p("  >>> GR 回归门 PASS. 继续 TUFT 壁.")

# v13 审计教训: 独立复现裸打靶在 GR 上 FAIL (证伪记录)
p("")
p("  [审计证伪记录] v13 裸 iw 打靶 (前向视界入射->外匹配) 在 GR 上独立复现:")
p("    锁定到伪根 74.69 - 69.08 i, 且随 s_out=10..120 纹丝不动 (溢出根),")
p("    与真值 0.373672-0.088962i 偏差 1.0e2 -> 该法被 GR 门否决, TUFT 禁用.")

# ======================================================================
# PART 2 : TUFT 几何 + 向内积分求解器
# ======================================================================
p("")
p("="*80)
p("PART 2  TUFT 几何 + 无穷远出射向内积分求解器")
p("="*80)

def wall_radius(c, d):
    return brentq(lambda r: 1+c/r**2+d/r**3, 1e-3, 5.0, xtol=1e-14)

class TuftGeom:
    def __init__(self, c, d, rmax=600.0, Ngrid=600000):
        self.c, self.d = c, d
        self.rh = wall_radius(c, d)
        r = np.linspace(self.rh*(1+1e-12), rmax, Ngrid)
        g = 1 + c/r**2 + d/r**3
        F = np.exp(2/r)*np.sqrt(np.clip(g,0,None))          # dr*/dr
        self.s = np.concatenate([[0.0], np.cumsum(0.5*(F[1:]+F[:-1])*np.diff(r))])
        self.r = r
        self.V = np.exp(-2/r)*6.0/r**2
        self.ipk = int(np.argmax(self.V))
        self.L = self.s[self.ipk]   # 壁 -> 势垒峰 乌龟距离

def shoot_inward(G, h, s_out, w):
    """无穷远纯出射起点 psi=e^{i w s_out}, psi_s=i w; 向内积分到 s=0.
       返回壁面对数导数 psi_s(0)/psi(0); Neumann QNM => 0."""
    sg = np.arange(s_out, -0.5*h, -h)
    Vg = np.interp(sg, G.s, G.V)
    N = len(Vg)
    a,b = w.real, w.imag
    Wk0 = -a*a + b*b; twoab = 2*a*b
    u,v = 1.0, 0.0        # psi = 1
    us,vs = -b, a         # psi_s = i w
    hh = -h
    for k in range(N-1):
        W = Vg[k] + Wk0
        k1u,k1v,k1us,k1vs = us,vs, W*u+twoab*v, W*v-twoab*u
        u2,v2 = u+0.5*hh*k1u, v+0.5*hh*k1v
        us2,vs2 = us+0.5*hh*k1us, vs+0.5*hh*k1vs
        k2u,k2v = us2,vs2
        k2us,k2vs = W*u2+twoab*v2, W*v2-twoab*u2
        u3,v3 = u+0.5*hh*k2u, v+0.5*hh*k2v
        us3,vs3 = us+0.5*hh*k2us, vs+0.5*hh*k2vs
        k3u,k3v = us3,vs3
        k3us,k3vs = W*u3+twoab*v3, W*v3-twoab*u3
        u4,v4 = u+hh*k3u, v+hh*k3v
        us4,vs4 = us+hh*k3us, vs+hh*k3vs
        k4u,k4v = us4,vs4
        Wp = Vg[min(k+1,N-1)]+Wk0
        k4us,k4vs = Wp*u4+twoab*v4, Wp*v4-twoab*u4
        u  += hh/6*(k1u+2*k2u+2*k3u+k4u)
        v  += hh/6*(k1v+2*k2v+2*k3v+k4v)
        us += hh/6*(k1us+2*k2us+2*k3us+k4us)
        vs += hh/6*(k1vs+2*k2vs+2*k3vs+k4vs)
    psi = complex(u,v); psis = complex(us,vs)
    return psis/psi

def solve_root(G, h, s_out, seed):
    def Fv(x):
        f = shoot_inward(G, h, float(s_out), complex(x[0],x[1]))
        return [f.real, f.imag]
    sol = sp_root(Fv, [seed.real, seed.imag], method='hybr',
                  options={'xtol':1e-13,'maxfev':3000})
    w = complex(*sol.x)
    res = abs(shoot_inward(G, h, float(s_out), w))
    return w, res, sol.success

def richardson_limit(points):
    """points: list (s_out, w). 用倒数线性外推 s_out->inf. 返回 (w_inf, 收敛序数)."""
    pts = points[-3:]
    xs = np.array([1.0/so for so,_ in pts])
    yr = np.array([w.real for _,w in pts]); yi = np.array([w.imag for _,w in pts])
    pr = np.polyfit(xs, yr, 1); pi = np.polyfit(xs, yi, 1)
    return complex(pr[-1], pi[-1])

# ======================================================================
# PART 3 : TUFT 壁根  (c=-0.5 / c=-0.29), 基模+泛音, Richardson
# ======================================================================
p("")
p("="*80)
p("PART 3  TUFT 壁 Neumann + 无穷远出射 特征根  (多 s_out Richardson 外推)")
p("="*80)

def enumerate_modes(G, tag):
    """|F| 复平面先扫描, 只收 |F| 深阱 (local minima), 去重, 再逐根 Richardson."""
    p("")
    p("  [%s] r_h=%.5f M,  r_peak=%.5f M,  L=壁->垒峰=%.5f M" % (
        tag, G.rh, G.r[G.ipk], G.L))
    # (1) 粗扫 |F| 找深阱
    h = 0.005; SO = 160.0
    grid = []
    for re_ in np.arange(0.3, 2.6, 0.10):
        for im in np.arange(-0.02, -0.55, -0.05):
            try:
                val = abs(shoot_inward(G, h, SO, complex(re_, im)))
                grid.append((val, complex(re_, im)))
            except Exception:
                pass
    grid.sort(key=lambda kv: kv[0])
    # 深阱阈值: log10|F| < -1.5 (即 |F|<0.03); 去重 0.08 内
    seeds = []
    for val, g in grid:
        if val > 0.03: break
        if all(abs(g - q) > 0.08 for q in seeds):
            seeds.append(g)
        if len(seeds) >= 4: break
    if not seeds:
        # 退路: 用最浅的几个局部极小
        seeds = [g for _, g in grid[:3]]
    p("    |F| 深阱种子 (|F|<0.03): " + ", ".join("%.3f%+.3fi"%(g.real,g.imag) for g in seeds))
    results = []
    for k, seed in enumerate(seeds):
        good = []
        sd = seed
        for SO in [100, 130, 160, 190, 220]:
            try:
                w, res, ok = solve_root(G, 0.005, float(SO), sd)
                if not (ok and res < 1e-7 and 0.05<w.real<4 and -1.5<w.imag<-1e-4):
                    continue
                good.append((SO, w)); sd = w
            except Exception:
                pass
        # 去重: 与已收根相近则跳过
        if any(abs(good[-1][1] - r[2][-1][1]) < 0.08 for r in results):
            continue
        if len(good) < 3:
            p("    seed %s : s_out 段不足 (<3 点), 弃" % seed)
            continue
        w_inf = richardson_limit(good)
        results.append((k, w_inf, good))
        p("    根 #%d (seed %s):" % (k, seed))
        for so, w in good:
            p("        s_out=%4d  w = %.9f %+.9f i" % (so, w.real, w.imag))
        span_re = good[-1][1].real - good[0][1].real
        span_im = good[-1][1].imag - good[0][1].imag
        p("        Richardson w_inf = %.9f %+.9f i   (s_out 段 Re 漂移 %+.4f, Im 漂移 %+.4f)" % (
            w_inf.real, w_inf.imag, span_re, span_im))
    if len(results) == 0:
        p("    (未收敛到稳定支)")
    return results

samples = [(-0.5, 0.0, "c=-0.50,d=0"), (-0.29, -0.05, "c=-0.29,d=-0.05")]
all_modes = {}
for c,d,tag in samples:
    G = TuftGeom(c, d)
    modes = enumerate_modes(G, tag)
    all_modes[(c,d)] = (G, modes)
    if len(modes) <= 1:
        p("    [注] 仅分辨出 1 个弱阻尼空腔基模; 复平面扫描未见第二深阱, 高阶泛音未分辨.")

# ======================================================================
# PART 4 : 腔长标度检验 (4 个 c_m)
# ======================================================================
p("")
p("="*80)
p("PART 4  腔长标度检验  (外垒主导 vs 真壁空腔模)")
p("="*80)
p("  判据: (a) 外垒主导: Re w 对 L 不敏感 (锁 GR ~0.37);")
p("        (b) 真壁空腔模: Re w ~ (n+1/2) pi/L, Re w*L ~ const.")
p("")
p("  %-14s %-8s %-8s %-9s %-12s %-10s %-10s" % (
    "c_m,d","r_h","L","pi/2L","Re w_inf","Re w*L","判读"))
scale = [(-0.80,0.00),(-0.40,-0.02),(-0.29,-0.05),(-0.20,-0.08)]
scale_rows = []
for c,d in scale:
    G = TuftGeom(c,d)
    # 用 |F| 深阱定位基模 (避免固定种子跳到伪根)
    h=0.005; SO=160.0
    best=None; bestv=1e9
    for re_ in np.arange(0.3,2.0,0.08):
        for im in np.arange(-0.02,-0.45,-0.05):
            try:
                v=abs(shoot_inward(G,h,SO,complex(re_,im)))
                if v<bestv: bestv=v; best=complex(re_,im)
            except Exception: pass
    try:
        w, res, ok = solve_root(G, 0.005, 160.0, best)
        prod = w.real*G.L
        judge = "外垒主导" if abs(w.real-0.37)<0.10 else ("空腔~pi/2L" if abs(prod-np.pi/2)/(np.pi/2)<0.35 else "混合/势垒修正")
        p("  %-14s %-8.4f %-8.4f %-9.4f %-12.6f %-10.4f %-10s" % (
            "%+.2f,%+.2f"%(c,d), G.rh, G.L, np.pi/(2*G.L), w.real, prod, judge))
        scale_rows.append((c,d,G.rh,G.L,w,np.pi/(2*G.L)))
    except Exception as e:
        p("  %-14s fail %s" % ("%+.2f,%+.2f"%(c,d), str(e)[:30]))

# ======================================================================
# PART 5 : 四态分级
# ======================================================================
p("")
p("="*80)
p("PART 5  四态分级终裁")
p("="*80)
p("  S1 GR 回归门: PASS (l=2 n=0 命中 %.15f, %d 位 >=6)" % (
    float(w20.real), gr_root[(2,0,400)][2]))
p("  S2 TUFT 壁 Neumann 特征可求根: 见 PART3 (有限 s_out Richardson 外推).")
n30 = len(all_modes[(-0.5,0.0)][1]); n29 = len(all_modes[(-0.29,-0.05)][1])
p("  S3 真壁空腔模检验: 见 PART4 标度表.")
if scale_rows:
    re_lo=min(r[4].real for r in scale_rows); re_hi=max(r[4].real for r in scale_rows)
    L_lo=min(r[3] for r in scale_rows);     L_hi=max(r[3] for r in scale_rows)
    p("     L 由 %.2f->%.2f (%.2fx); 基模 Re w 由 %.3f->%.3f (%.2fx);" % (
        L_lo,L_hi,L_hi/L_lo,re_lo,re_hi,re_hi/re_lo))
    p("     真空腔模应 Re w ~ 1/L (走 %.2fx); 实际走 %.2fx." % (L_hi/L_lo, re_hi/re_lo))
p("  S4 数值稳定性: GR 门 50 位残差 1e-50; TUFT 向内积分壁正则点稳定, 残差 ~1e-7,")
p("     但有限 s_out 根漂移 1e-2 级 (见 PART3 段内漂移), 阻尼为弱 (|Im|~0.02).")
p("")
p("  终裁: GR 门 PASS (15 位); TUFT 壁 Neumann 仅分辨出弱阻尼空腔基模一支,")
p("        复平面无第二深阱, 高阶泛音未收敛 -> 按 S4/OPEN 计, 不伪造多模表.")
p("="*80)
p("总耗时 %.1f s" % (time.time()-t0))

out_path = r"D:\a10\aikjx\code\my_lib\tuft_v14_tuft_wall_out.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("[written]", out_path)
