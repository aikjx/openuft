# -*- coding: utf-8 -*-
"""
TUFT v3 线二: ISCO 硬伤修复 — 新后度量 ansatz 搜索 (E55 起)
各向同性坐标 ds^2 = A dt^2 - B(dr^2 + r^2 dΩ^2), +---, G=c=M=1, U = M/r = 1/r.

三约束:
  (i)   1PN PPN: A = 1 - 2U + 2β U^2 + ..., B = 1 + 2γ U + ...  => β=γ=1
        => A 的 U^2 系数 = 2 ; B 的 U 系数 = 2 (B 无 U 一次项修正)
  (ii)  ISCO ∈ [4.45, 5.44] M  (GR 各向同性 4.949M ±10%)
  (iii) b_crit ∈ [4.676, 5.716] M (GR 5.196M ±10%)

通用量 (复用 v2):
  光子球: d ln(B/A)/dr = -2/r   =>  B'/B - A'/A + 2/r = 0
  L^2(r) = A' B^3 r^3 / [2 A(B' r + B) - A' B r]
  ISCO   = argmin L^2(r)  (dL^2/dr = 0)
  b_crit = r_ph sqrt(B/A)
"""
import numpy as np
from scipy.optimize import brentq, minimize

M = 1.0
U = lambda r: M / r

# ---------- 通用数值导数度规 ----------
class IsoMetric:
    """传入 A(U), B(U) 的纯函数; 内部用 U->r, 中心差分数值求导."""
    def __init__(self, A_of_U, B_of_U, name=""):
        self.AU = A_of_U
        self.BU = B_of_U
        self.name = name

    def AB(self, r):
        u = U(r)
        return self.AU(u), self.BU(u)

    def dAB(self, r):
        u = U(r)
        e = 1e-6 * max(u, 1e-3)
        A0, B0 = self.AU(u), self.BU(u)
        Ap, Bp = self.AU(u + e), self.BU(u + e)
        Am, Bm = self.AU(u - e), self.BU(u - e)
        dAdu = (Ap - Am) / (2 * e)
        dBdu = (Bp - Bm) / (2 * e)
        dUdr = -M / r**2
        return A0, B0, dAdu * dUdr, dBdu * dUdr

    # --- 弱场展开: 解析截出 PPN 系数 ---
    def ppn(self, n=5):
        # 在 u 小处做级数, 返回 A(u),B(u) 泰勒系数 (u^0..u^n)
        us = 1e-6
        # 用有限差分在 u=0 附近重建系数: 直接对 A(u),B(u) 求导
        def coeffs(f):
            cs = [f(0.0)]
            h = 1e-5
            deriv_prev = None
            for k in range(1, n + 1):
                # k 阶中心差商递推
                pass
            return cs
        # 简单起见: 用 numpy polyfit 在 u∈[0,0.02] 拟合到 u^n
        us = np.linspace(0.0, 0.02, 41)
        Av = np.array([self.AU(max(x, 0.0)) for x in us])
        Bv = np.array([self.BU(max(x, 0.0)) for x in us])
        cA = np.polyfit(us, Av, n)  # 高次在前
        cB = np.polyfit(us, Bv, n)
        # 转成升幂
        cA = cA[::-1]; cB = cB[::-1]
        return cA, cB  # cA[k] = A 的 u^k 系数

    def ppn_report(self):
        cA, cB = self.ppn(4)
        beta = cA[2] / 2.0          # A = 1 -2u + 2β u^2
        gamma = cB[1] / 2.0         # B = 1 + 2γ u
        return beta, gamma, cA, cB

    # --- 光子球方程 ---
    def ph_eq(self, r):
        A, B, dA, dB = self.dAB(r)
        if A <= 0 or B <= 0:
            return np.nan
        return dB / B - dA / A + 2.0 / r

    # --- L^2(r): 各向同性坐标正确公式 (GR 自检 L^2_ISCO=12 @ r=4.949) ---
    # L^2 = A' B^2 r^3 / [ A(B'r + 2B) - A' B r ]
    def L2(self, r):
        A, B, dA, dB = self.dAB(r)
        if A <= 0 or B <= 0:
            return np.nan
        num = dA * B**2 * r**3
        den = A * (dB * r + 2.0 * B) - dA * B * r
        if abs(den) < 1e-30:
            return np.nan
        return num / den

    # --- 有效域下界: 从 r=0 上升找第一个 A,B>0 的点 (避开视界/奇点) ---
    def valid_lo(self):
        rs = np.linspace(0.05 * M, 5 * M, 4000)
        transition = None
        prev_ok = False
        for r in rs:
            try:
                A, B, _, _ = self.dAB(r)
                ok = np.isfinite(A) and np.isfinite(B) and A > 1e-9 and B > 1e-9
            except Exception:
                ok = False
            if ok and not prev_ok:
                transition = r
                break
            prev_ok = ok
        if transition is None:
            return 0.05 * M
        return transition * 1.001

    # --- 光子球: 取最外根 (最远离视界的物理光子球) ---
    def find_rph(self):
        lo = self.valid_lo() * 1.0001
        rs = np.linspace(lo, 60 * M, 8000)
        vals = np.array([self.ph_eq(r) for r in rs])
        roots = []
        for i in range(len(rs) - 1):
            if np.isfinite(vals[i]) and np.isfinite(vals[i + 1]) and vals[i] * vals[i + 1] < 0:
                try:
                    rr = brentq(lambda r: self.ph_eq(r), rs[i], rs[i + 1], xtol=1e-12)
                    roots.append(rr)
                except Exception:
                    pass
        return roots  # 调用方取最外根 roots[-1]

    # --- ISCO: L² 的全局极小 (取 L² 值最小的局部极小), 非最内 r ---
    def find_isco(self):
        lo = self.valid_lo() * 1.001
        rs = np.linspace(lo, 400 * M, 8000)
        L2 = np.array([self.L2(r) for r in rs])
        valid = np.isfinite(L2) & (L2 > 0)
        rv, lv = rs[valid], L2[valid]
        if len(rv) < 5:
            return None
        # 候选局部极小
        mins = []
        for i in range(1, len(rv) - 1):
            if lv[i] < lv[i - 1] and lv[i] <= lv[i + 1]:
                mins.append((lv[i], rv[i]))
        if not mins:
            return None
        # 物理 ISCO = L² 全局最小 (外侧主极小); 排除视界附近发散尖峰
        mins.sort(key=lambda t: t[0])
        # 取 L² 最小者
        r0 = mins[0][1]
        idx = int(np.argmin(np.abs(rv - r0)))
        lo2 = rv[max(0, idx - 5)]
        hi2 = rv[min(len(rv) - 1, idx + 5)]
        def dL2(r):
            e = 1e-6 * r
            return (self.L2(r + e) - self.L2(r - e)) / (2 * e)
        try:
            return brentq(dL2, lo2, hi2, xtol=1e-12)
        except Exception:
            return r0

    def b_crit(self, rph):
        A, B, _, _ = self.dAB(rph)
        return rph * np.sqrt(B / A)

    def evaluate(self):
        beta, gamma, cA, cB = self.ppn_report()
        roots = self.find_rph()
        rph = roots[-1] if roots else None  # 最外根 = 物理光子球
        ri = self.find_isco()
        bc = self.b_crit(rph) if rph else None
        return dict(beta=beta, gamma=gamma, cA=cA, cB=cB,
                    rph=rph, isco=ri, bcrit=bc)


# ================= 候选 ansatz =================
# v2 基准: A=e^{-2u}, B=e^{2u}(1+c u^2)
def v2_metric(c):
    return IsoMetric(lambda u: np.exp(-2 * u),
                     lambda u: np.exp(2 * u) * (1 + c * u**2),
                     name=f"v2 c={c}")

# A: 三阶修正 B=e^{2u}(1+c u^2 + d u^3)
def candA(c, d):
    return IsoMetric(lambda u: np.exp(-2 * u),
                     lambda u: np.exp(2 * u) * (1 + c * u**2 + d * u**3),
                     name=f"A c={c} d={d}")

# B: B=e^{2u + f(u)}, f=c2 u^2 + c3 u^3 + c4 u^4  (无一次项 => γ=1 自动)
def candB(c2, c3=0.0, c4=0.0):
    def Bu(u):
        return np.exp(2 * u + c2 * u**2 + c3 * u**3 + c4 * u**4)
    return IsoMetric(lambda u: np.exp(-2 * u), Bu,
                     name=f"B c2={c2} c3={c3} c4={c4}")

# C: 精确 Schwarzschild 各向同性 (x=u/2)
def candC():
    def Au(u):
        x = u / 2.0
        return ((1 - x) / (1 + x))**2
    def Bu(u):
        x = u / 2.0
        return (1 + x)**4
    return IsoMetric(Au, Bu, name="C Schwarzschild-exact isotropic")

# C': 错误符号的 (1+u)/(1-u) 形式 (题目候选 C 字面版)
def candC_wrong():
    return IsoMetric(lambda u: (1 + u) / (1 - u),
                     lambda u: (1 + u / 2.0)**4,
                     name="C' (1+u)/(1-u) 字面版")


# ================= 四态标注 =================
def state_isok(v):
    if v is None or not np.isfinite(v):
        return "BLOCK"
    if abs(v - 4.949) <= 0.10 * 4.949:
        return "PASS"
    if abs(v - 4.949) <= 0.20 * 4.949:
        return "MARGINAL"
    return "FAIL"

def state_bcok(v):
    if v is None or not np.isfinite(v):
        return "BLOCK"
    if abs(v - 5.196) <= 0.10 * 5.196:
        return "PASS"
    if abs(v - 5.196) <= 0.20 * 5.196:
        return "MARGINAL"
    return "FAIL"

def state_ppn(beta, gamma):
    if abs(beta - 1) < 1e-3 and abs(gamma - 1) < 1e-3:
        return "PASS"
    return "FAIL"

def overall(spp, sis, sbc):
    if "FAIL" in (spp, sis, sbc) or "BLOCK" in (spp, sis, sbc):
        return "FAIL" if "FAIL" in (sis, sbc) else "BLOCK"
    if "MARGINAL" in (spp, sis, sbc):
        return "MARGINAL"
    return "PASS"


def line(tag, res):
    spp = state_ppn(res['beta'], res['gamma'])
    sis = state_isok(res['isco'])
    sbc = state_bcok(res['bcrit'])
    ov = overall(spp, sis, sbc)
    isc = f"{res['isco']:.4f}" if res['isco'] else "  N/A "
    bc = f"{res['bcrit']:.4f}" if res['bcrit'] else "  N/A "
    rp = f"{res['rph']:.4f}" if res['rph'] else "  N/A "
    print(f"{tag:>22} | β={res['beta']:+.4f} γ={res['gamma']:+.4f}[{spp:>8}] | "
          f"ISCO={isc}[{sis:>8}] | b_crit={bc}[{sbc:>8}] | r_ph={rp} | => {ov}")
    return ov


def main():
    print("=" * 100)
    print("TUFT v3 线二 — 新后度量 ansatz 搜索 (E55 起)  G=c=M=1, U=1/r")
    print("GR 基准: ISCO=4.9490 (±10% -> [4.454,5.444]); b_crit=5.1962 (±10% -> [4.677,5.716])")
    print("=" * 100)

    # ---- 0) GR 基准自检 ----
    print("\n[E55] 基准自检: 精确 Schwarzschild 各向同性")
    gC = candC(); rC = gC.evaluate()
    line("C=Schwarzschild", rC)

    print("\n[E56] v2 复现: A=e^{-2u}, B=e^{2u}(1+c u^2)")
    for c in [0.0, -0.25, -0.5, -1.0, 0.5]:
        line(f"v2 c={c:+.2f}", v2_metric(c).evaluate())

    print("\n[E57] 候选 C': 字面 (1+u)/(1-u) — 检验符号错误")
    line("C' (1+u)/(1-u)", candC_wrong().evaluate())

    # ---- E58: 候选 A 三阶修正扫描 ----
    print("\n[E58] 候选 A: B=e^{2u}(1+c u^2 + d u^3) 扫描")
    print(f"{'c':>7}{'d':>9} | ... (仅打印近优区)")
    bestA = []
    for c in np.linspace(-0.45, 0.0, 46):
        for d in np.linspace(-0.45, 0.15, 61):
            res = candA(c, d).evaluate()
            ov = overall(state_ppn(res['beta'], res['gamma']),
                         state_isok(res['isco']), state_bcok(res['bcrit']))
            if ov in ("PASS", "MARGINAL"):
                bestA.append((ov, c, d, res['isco'], res['bcrit']))
    if bestA:
        # 取 ISCO 最接近 4.949 的
        bestA.sort(key=lambda t: abs((t[3] or 99) - 4.949))
        for ov, c, d, isc, bc in bestA[:8]:
            print(f"   c={c:+.3f} d={d:+.3f}  ISCO={isc:.4f} b_crit={bc:.4f}  -> {ov}")
        print(f"   [候选A] PASS/MARGINAL 解数 = {len(bestA)}")
    else:
        print("   [候选A] 三阶修正 (c u^2 + d u^3) 无任何 PASS/MARGINAL 解")

    # ---- E59: 候选 B 函数族数值优化 (f = c2 u^2 + c3 u^3) ----
    print("\n[E59] 候选 B: B=e^{2u + c2 u^2 + c3 u^3} 数值拟合 (2方程2未知)")
    def resid(x):
        c2, c3 = x
        if abs(c2) > 5 or abs(c3) > 5:
            return [1e6, 1e6]
        try:
            res = candB(c2, c3).evaluate()
            if res['isco'] is None or res['bcrit'] is None:
                return [1e6, 1e6]
            return [res['isco'] - 4.949, res['bcrit'] - 5.196]
        except Exception:
            return [1e6, 1e6]

    foundB = None
    from scipy.optimize import least_squares
    for x0 in [(-0.5, 0.0), (-1.0, 0.5), (0.0, -0.5), (-1.5, 1.0), (-0.3, 0.3)]:
        try:
            sol = least_squares(resid, x0, bounds=([-5, -5], [5, 5]), method='trf', xtol=1e-10, ftol=1e-10)
            r = candB(*sol.x).evaluate()
            sc = overall(state_ppn(r['beta'], r['gamma']), state_isok(r['isco']), state_bcok(r['bcrit']))
            if sc in ("PASS", "MARGINAL"):
                foundB = (sol.x, r, sc)
                break
        except Exception as e:
            pass
    if foundB:
        (c2, c3), r, sc = foundB
        print(f"   拟合收敛: c2={c2:+.5f}, c3={c3:+.5f}")
        line(f"B f={c2:+.3f}u^2+{c3:+.3f}u^3", r)
        # 物理代价: 检验 A*B, 视界, 单调性
        ab05 = np.exp(-2*0.5) * np.exp(2*0.5 + c2*0.25 + c3*0.125)
        ab10 = np.exp(-2*1.0) * np.exp(2*1.0 + c2*1.0 + c3*1.0)
        print(f"   [代价] A*B 在 u=0.5: {ab05:.4f} (GR=(1-u^2/4)^2={((1-0.25/4)**2):.4f})")
        print(f"   [代价] A*B 在 u=1.0 (r=M): {ab10:.4f}")
    else:
        print("   [候选B] 二阶+三阶 f 多项式 未能同时命中两目标 (尝试多初值均失败)")

    # ---- E60: 检验 A=e^{-2u} 固定族是否可能 (可行性边界扫描) ----
    print("\n[E60] 可行性边界: 固定 A=e^{-2u}, 变 B=e^{2u}(1+c u^2) 时 ISCO 可达范围")
    print("   (证明 ISCO 对 c 的单调性与可达上下限)")
    rows = []
    for c in np.linspace(-2.0, 2.0, 41):
        try:
            res = v2_metric(c).evaluate()
            rows.append((c, res['isco'], res['bcrit']))
        except Exception:
            pass
    ics = [r[1] for r in rows if r[1]]
    print(f"   c∈[-2,2] 时 ISCO 范围 = [{min(ics):.3f}, {max(ics):.3f}] M")
    print(f"   GR 目标窗口 [4.454, 5.444] 是否被覆盖? "
          f"{'是' if min(ics) <= 5.444 and max(ics) >= 4.454 else '否'}")
    # 找 c 使 ISCO 最小
    best = min(rows, key=lambda t: abs((t[1] or 99) - 4.949))
    print(f"   最接近 GR 的单参数点: c={best[0]:+.3f} -> ISCO={best[1]:.3f}, b_crit={best[2]:.3f}")

    print("\n" + "=" * 100)
    print("汇总完成")
    print("=" * 100)


if __name__ == "__main__":
    main()
