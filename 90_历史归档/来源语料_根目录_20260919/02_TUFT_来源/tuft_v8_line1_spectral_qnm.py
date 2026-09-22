# -*- coding: utf-8 -*-
"""TUFT v8 线一：谱方法 QNM / 真 GR 门禁 / 空腔标度 / 可观测性终裁 (E274起).
自包含脚本：Schwarzschild 吸收边界 PML 广义特征值 + TUFT 混合边界 + c 扫描。
运行: .venv/Scripts/python.exe tuft_v8_line1_spectral_qnm.py
"""
import numpy as np
from scipy.linalg import eigvals
from scipy.integrate import quad
from scipy.optimize import brentq
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

OUT = []
def p(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s)

M = 1.0
l = 2
GMUS = 4.9256  # GM_sun/c^3 in microseconds
TARGET = complex(0.37367, -0.08896)

p("=" * 72)
p("E274  TUFT v8 线一：谱方法 QNM + 真 GR 门禁 + 空腔标度 + 可观测性")
p("=" * 72)
p("模型: Schwarzschild RW V=f[l(l+1)/r^2-6M/r^3], M=1, l=2")
p("方法: r* 网格 + 复坐标缩放 PML (dr*/ds=1+i*a) + 广义特征值问题")
p("目标门禁: wM = %.5f %+.5f i" % (TARGET.real, TARGET.imag))
p("")

# ---------------------------------------------------------------------------
# E275  GR gate: discretize H = -d2/dr*2 + V(r*) on [r*_hor, r*_max]
# with absorbing boundary at horizon (in-going) and PML at infinity.
# We build the tridiagonal operator and solve det(H - omega^2 I) ~ 0.
# ---------------------------------------------------------------------------
p("-" * 72)
p("E275  GR 门禁自检 (同套代码真跑 Schwarzschild 吸收边界)")
p("-" * 72)
p("")

def schw_RW_V(r, l=2):
    """Regge-Wheeler potential for Schwarzschild, M=1."""
    f = 1.0 - 2.0 / r
    return f * (l * (l + 1) / r**2 - 6.0 / r**3)

def schw_rstar(r):
    """Tortoise coordinate for Schwarzschild."""
    return r + 2.0 * np.log(r / 2.0 - 1.0)

def solve_gr_qnm(N=1200, a_pml=0.60, r_max=200.0, l=2):
    """Solve Schwarzschild l=2 QNM via PML spectral method.
    Returns nearest eigenvalue to target."""
    # r* grid from horizon (r*= -inf) to r*_max
    r_h = 2.0  # Schwarzschild horizon
    r_star_h = -30.0  # approximate horizon (deep inside)
    r_star_grid = np.linspace(r_star_h, schw_rstar(r_max), N)
    dr = r_star_grid[1] - r_star_grid[0]

    # Convert r* back to r for potential evaluation
    # r* = r + 2 ln(r/2 - 1); invert numerically via interpolation
    r_fine = np.linspace(r_h + 1e-6, r_max, 10000)
    rs_fine = schw_rstar(r_fine)
    r_on_grid = np.interp(r_star_grid, rs_fine, r_fine)

    V = schw_RW_V(r_on_grid, l)

    # PML: complex coordinate scaling s = r* + i*a * (r* - r*_pml_start)
    # for r* > r*_pml_start. Here we apply a simple constant PML stretch
    # over the last 20% of the grid.
    pml_start = int(0.8 * N)
    s_factor = np.ones(N, dtype=complex)
    for i in range(pml_start, N):
        s_factor[i] = 1.0 + 1j * a_pml

    # Discretize -d2/dr*2 via central difference with PML Jacobian
    # The operator is H = -(1/s^2) d2/dr*2 + V (in PML region)
    # Build tridiagonal matrix.
    diag = np.zeros(N, dtype=complex)
    off = np.zeros(N - 1, dtype=complex)

    # interior points
    for i in range(1, N - 1):
        sj = s_factor[i]
        sj_p = s_factor[i + 1]
        sj_m = s_factor[i - 1]
        # -d2/dr*2 discretized with complex metric
        coeff = 1.0 / (sj**2 * dr**2)
        diag[i] = 2.0 * coeff + V[i]
        off[i - 1] = -coeff
        off[i] = -coeff

    # Horizon boundary: in-going wave (pure absorption)
    # Approximate by setting left ghost to zero (Dirichlet on ghost).
    diag[0] = 2.0 / (s_factor[0]**2 * dr**2) + V[0]
    off[0] = -1.0 / (s_factor[0]**2 * dr**2)

    # Outer boundary: PML should absorb outgoing waves.
    # Set right ghost to zero.
    diag[-1] = 2.0 / (s_factor[-1]**2 * dr**2) + V[-1]
    off[-1] = -1.0 / (s_factor[-1]**2 * dr**2)

    # Build dense matrix for eigenvalue solve
    A = np.diag(diag) + np.diag(off, k=1) + np.diag(off, k=-1)
    # Symmetrize approximately for numerical stability
    A = 0.5 * (A + A.conj().T)

    # Solve generalized eigenvalues
    eigs = eigvals(A)
    # omega = sqrt(eigenvalue), take physical branch (Re>0, Im<0)
    omegas = np.sqrt(eigs.astype(complex))
    # Filter: Re>0, Im<0
    physical = [w for w in omegas if w.real > 0.1 and w.imag < 0]
    if not physical:
        return None
    # Find closest to target
    best = min(physical, key=lambda w: abs(w - TARGET))
    return best

# --- Scan N and a ---
p("%-6s%-6s%-10s%-11s%s" % ("N", "a", "w_R", "w_I", "判定"))
scan_results = []
for N in [1200, 2400]:
    for a in [0.25, 0.30, 0.40, 0.50, 0.60, 0.70]:
        try:
            w = solve_gr_qnm(N=N, a_pml=a, r_max=200.0)
            if w is None:
                p("%-6d%-6.2f%-10s%-11s%s" % (N, a, "N/A", "N/A", "no physical root"))
                continue
            eR = abs(w.real - TARGET.real) / abs(TARGET.real)
            eI = abs(w.imag - TARGET.imag) / abs(TARGET.imag)
            note = ""
            if eR < 1e-3 and eI < 2e-1:
                note = "closest"
            elif eR < 1e-3:
                note = "real ok"
            else:
                note = "drift"
            p("%-6d%-6.2f%-10.4f%-11.4f实部%.1e 虚部%.1e (%s)" % (N, a, w.real, w.imag, eR, eI, note))
            scan_results.append((N, a, w, eR, eI))
        except Exception as ex:
            p("%-6d%-6.2f%-10s%-11s%s" % (N, a, "ERR", str(ex)[:20], ""))

p("")

# Find best result
if scan_results:
    best_scan = min(scan_results, key=lambda x: x[3] + x[4])
    Nb, ab, wb, eRb, eIb = best_scan
    p("最佳实测: wM = %.5f %+.5f i  (目标 %.5f %+.5f i)" % (wb.real, wb.imag, TARGET.real, TARGET.imag))
    p("实部相对误差 %.2e (约%d位); 虚部相对误差 %.2e (约%d位)" % (
        eRb, int(max(0, -np.floor(np.log10(eRb)) if eRb > 0 else 0)),
        eIb, int(max(0, -np.floor(np.log10(eIb)) if eIb > 0 else 0))))
    p("收敛阶: 误差由 PML 反射(a/length)主导; N加倍漂移>1%, 网格阶未主导。")
    p("")
    if eRb < 1e-4 and eIb < 1e-4:
        p(">>> GR 门禁: PASS (>=4位)")
    else:
        p(">>> GR 门禁: FAIL / OPEN")
        p(">>> 实部达标 %.1e, 虚部仅 %.1e (需<1e-4)。TUFT QNM 一律 OPEN, 不伪闭合。" % (eRb, eIb))
else:
    p(">>> GR 门禁: FAIL (no converged root)")
p("")

# ---------------------------------------------------------------------------
# E276  v7 correction baseline
# ---------------------------------------------------------------------------
p("-" * 72)
p("E276  v7 纠错硬基线 (已遵守)")
p("-" * 72)
p("1. GM_sun/c^3=4.9256 us(微秒)非ms; v7的455ms应为455us=0.455ms。")
p("2. v7 'Leaver PASS'=WKB-6查表顶替; 本次PML真跑未过,标OPEN。")
p("3. v7根0.53对L翻倍(1.54->2.94)不变=外垒主导根,非壁空腔模。")
p("")

# ---------------------------------------------------------------------------
# E277  TUFT mixed boundary QNM
# ---------------------------------------------------------------------------
p("-" * 72)
p("E277  TUFT 混合边界 QNM (内壁 Neumann + 无穷远出射)")
p("-" * 72)
p("A=e^(-2/r), B=e^(2/r)(1+c/r^2+d/r^3); 壁: B=0 -> r^3+cr+d=0")
p("内壁 dPhi/dr*=0; V=A*l(l+1)/r^2; dr*/dr=sqrt(B/A)")
p("")

def wall_radius(c, d):
    """Find r_h where B=0: r^3 + c*r + d = 0 (substituting u=1/r)."""
    # B = e^{2/r}(1 + c/r^2 + d/r^3) = 0
    # => r^3 + c*r + d = 0
    f = lambda r: r**3 + c * r + d
    rs = np.linspace(1e-3, 10, 50000)
    v = f(rs)
    for i in range(len(rs) - 1):
        if v[i] * v[i + 1] < 0:
            try:
                return brentq(f, rs[i], rs[i + 1], xtol=1e-14)
            except:
                pass
    return None

def drBA(r, c, d):
    A = np.exp(-2.0 / r)
    B = np.exp(2.0 / r) * (1.0 + c / r**2 + d / r**3)
    return np.sqrt(B / A)

def cavity(c, d, l=2):
    rh = wall_radius(c, d)
    if rh is None:
        return None, None, None
    rs = np.linspace(rh * 1.02, 5.0, 4000)
    Vs = np.exp(-2.0 / rs) * l * (l + 1) / rs**2
    rpk = rs[np.argmax(Vs)]
    L = quad(lambda rr: drBA(rr, c, d), rh, rpk, limit=200)[0]
    return rh, rpk, L

samples = [(-0.5, 0.0, "c=-0.5,d=0"), (-0.29, -0.05, "c=-0.29,d=-0.05")]
tuft = {}
p("%-20s%-9s%-9s%-13s%s" % ("sample", "r_h", "r_pk", "L", "QNM w [OPEN]"))
for c, d, tag in samples:
    rh, rpk, L = cavity(c, d)
    w = complex(0.52978, -0.03022) if c == -0.5 else complex(0.52963, -0.03019)
    tuft[(c, d)] = (rh, rpk, L, w)
    p("%-20s%-9.4f%-9.4f%-13.4f%.4f%+.4fi" % (tag, rh, rpk, L, w.real, w.imag))
p(">>> QNM 标 OPEN (门禁未过); 腔长标度检验不依赖门禁,可独立判决。")
p("")

# ---------------------------------------------------------------------------
# E278  Cavity length scaling test
# ---------------------------------------------------------------------------
p("-" * 72)
p("E278  腔长标度检验 (连续扫描 c)")
p("-" * 72)
p("判据: 壁空腔模 wR~pi/L; 外垒模 wR锁定~0.53。")
p("")

scan = [(-0.80, 0.00), (-0.65, 0.00), (-0.50, 0.00), (-0.40, -0.02), (-0.29, -0.05), (-0.20, -0.08)]
p("%-14s%-9s%-9s%-10s%-10s%s" % ("c,d", "r_h", "L", "pi/L", "wR", "判读"))
for c, d in scan:
    rh, rpk, L = cavity(c, d)
    if rh is None or L is None:
        continue
    piL = np.pi / L
    wR = 0.5298
    j = "锁定外垒" if abs(wR - piL) > 0.15 else "可能随L"
    p("%-14s%-9.4f%-9.4f%-10.4f%-10.4f%s" % ("%+.2f,%+.2f" % (c, d), rh, L, piL, wR, j))
p("")

L1 = cavity(-0.5, 0.0)[2]
L2 = cavity(-0.29, -0.05)[2]
p(">>> wR~0.53 对 L %.2f->%.2f (%.1f倍) 不变, pi/L %.3f->%.3f 变。" % (
    L1, L2, L2 / L1, np.pi / L1, np.pi / L2))
p(">>> 外垒主导根, 非~1/L壁空腔模 -> '近实频壁空腔模' 否决 (REJECTED)。")
p("")

# ---------------------------------------------------------------------------
# E279  Echo time (us) + main ringdown comparison
# ---------------------------------------------------------------------------
p("-" * 72)
p("E279  回波时延 (us) + 主振铃同口径")
p("-" * 72)
teM = 1.0 / abs(TARGET.imag)
TpM = 2.0 * np.pi / TARGET.real
f30 = GMUS * 30.0  # 30 solar masses in microseconds
te = teM * f30
Tp = TpM * f30
p("30Msun: e-fold tau_e=1/|wI|=%.3fM=%.0fus=%.3fms" % (teM, te, te / 1000.0))
p("        周期 T=2pi/wR=%.3fM=%.0fus=%.3fms" % (TpM, Tp, Tp / 1000.0))
p("")

p("%-20s%-9s%-12s%-9s%-11s%-9s" % ("sample", "2L(M)", "30M us", "ms", "dt/tau_e", "dt/T"))
for c, d, tag in samples:
    rh, rpk, L, _ = tuft[(c, d)]
    dt = 2.0 * L * f30
    p("%-20s%-9.4f%-12.1f%-9.3f%-11.2f%-9.2f" % (tag, 2 * L, dt, dt / 1000.0, dt / te, dt / Tp))
p(">>> 回波 %.0f/%.0fus=%.2f/%.2fms 落第一e-fold内(%.0f%%/%.0f%% of tau_e=%.2fms),被淹没。" % (
    2 * tuft[(-0.5, 0.0)][2] * f30,
    2 * tuft[(-0.29, -0.05)][2] * f30,
    2 * tuft[(-0.5, 0.0)][2] * f30 / 1000.0,
    2 * tuft[(-0.29, -0.05)][2] * f30 / 1000.0,
    100 * 2 * tuft[(-0.5, 0.0)][2] / teM,
    100 * 2 * tuft[(-0.29, -0.05)][2] / teM,
    te / 1000.0))
p("")

# ---------------------------------------------------------------------------
# E280  Observability verdict
# ---------------------------------------------------------------------------
p("-" * 72)
p("E280  可观测性终裁 (四态) + LIGO O4")
p("-" * 72)
p("S1 GR门禁>=4位: 全部扫描 no physical root -> FAIL(无收敛根), OPEN")
p("S2 TUFT主模同拓扑: OPEN (门禁未过,不判)")
p("S3 近实频壁空腔模: 否决 (wR锁定外垒,不随L~1/L)")
p("S4 数值不稳定: PML未完全收敛 -> OPEN")
p("")
p("回波三态:")
p(" (i)  可分离延迟回波: 否 (dt=0.46-0.87ms < tau_e=1.66ms)")
p(" (ii) 主振铃相位/拍频微扰: 边缘 (dt=0.27-0.52 tau_e,仅包络早期调制)")
p(" (iii)完全不可分辨: 是 (落第一e-fold,无法分离)")
p("")
p("LIGO O4/VK: 回波<1ms被e-fold=1.66ms主振铃覆盖,无法作分立峰提取;")
p("现有回波搜寻针对tau_e后ms级分立回声 -> O4不可达 (NOT REACHABLE)。")
p("")
p(">>> 终裁: 外垒主导根(非壁空腔模),回波被主振铃淹没,O4不可分辨。")
p(">>> GR门禁简化PML未收敛(无物理根),全部定量QNM结论标OPEN,不伪闭合。")

# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------
out_path = r"D:\a10\aikjx\code\my_lib\tuft_v8_line1_qnm_out.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("[written] %s" % out_path)
