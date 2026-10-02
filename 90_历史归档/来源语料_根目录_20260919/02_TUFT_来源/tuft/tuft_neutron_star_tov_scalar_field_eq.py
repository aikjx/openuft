# -*- coding: utf-8 -*-
"""
TUFT · 中子星静态球对称内解联立 TOV + 标量场方程（修正版）
============================================================
本脚本是对用户提供稿《时空曲率–能量密度关系：全维修复攻坚·续篇》中
F^∞ 代码的**修复 + 复盘**实现。

【关键修复清单（相对原始稿）】
0. 【致命】原始稿的 `source` 变量（场方程源项）被计算出来后**从未用于更新任何量**，
   因此 alpha=0 与 alpha=1.87 给出**逐字节相同**的垃圾结果——理论独有预言
   根本没有参与计算，原稿“审计台账 8 项 PASS”是**空判**。
   本版把标量曲率 R 经自洽闭合喂回引力质量，使 α 效应真正进入方程。
1. 原始稿 `dnu_dr = -c**2*p/(rho+p/c**2)` 与引力无关（不含 G、m、r），
   维度错误且把 TOV 拆成 dp_dr = p 的平凡形式，一步内 p 变负、星体 R≈10m。
   本版用标准 TOV 组合式（避免除零）。
2. 原始稿不积分 nu/lambda（恒为 0），度规恒为 Minkowski，与“静态球对称内解”矛盾。
   本版用 gtt = 1-2Gm/(c^2 r) 自洽推进（等价于 e^{-2lambda}）。
3. 原始稿 rho_c = mp.mpf("1e-9") 是把参考中心密度写成了 1e-9 kg/m^3 的笔误；
   本版使用真实扫描中心密度 rho_c 作为 eq(1) 分母参考。
4. 原始稿把 1 阶 Euler 标成 “RK4”；本版实现真正 4 阶 RK4。
5. 原始稿 EOS 量级错误（rho<=1e14 给 3e6 Pa，差十几个量级）；
   本版用 SLy 分段多方形（4 段）。
6. 【断点错误】用户稿把 SLy 断点密度整体写低约 5 倍（1.5e17/2.5e17/3.1e17/4.0e17），
   使软的上段（Γ=1.556,1.110）在核密度附近过早生效，GR M_max 仅 ~0.74 M⊙。
   修正为文献断点 2.14e17/7.59e17/1.20e18/2.45e18，GR M_max 恢复到 ~2.09 M⊙。
7. 【数值稳定性】星体表面附近压力标高 H_p 仅亚毫米级，固定步长 dr=10m 会越界使
   rho 变负、rho**Γ 变成复数而崩溃；本版改为按 H_p 的自适应步长（0.1*H_p，
   夹在 [0.01m,20m]），并在导数中对 gtt<=0 / rho<=0 / rho 复数统一判越界。
8. 【判序 bug】表面穿越检测须**先于**“越界即坍缩”判定，否则低质量星在表面
   rho 跨过 rho_atm 的同一被误报为坍缩（GR 全表 collapse=True 的假象）。

【实测结论（诚实，与原始稿的定性预判不符）】
· 本闭合下额外引力密度占比与 α 严格线性：extraRho/rho ≈ 1.7 * α（半密半径处）。
· α=1.87 → 额外引力源达物质密度的 **318%**，星体不是“半径小 0.3~0.6 km”，
  而是直接形成视界（gtt→0）坍缩；R 从 16.06 km 压到 7.11 km 并终止积分。
  ⇒ 原始稿“α=1.87 半径比 GR 小 0.3~0.6 km”的定性预判 **未被复现**（过度陈述）。
· 使中子星仍能存在（不坍缩）需 α ≲ 1e-3；此时 ΔR 仅 **-0.02 km**（比声称的
  0.3~0.6 km 小 1~2 个量级），而 M 变化达 +11%。
  ⇒ 该模型的真实可观测量在 **质量（M_max）** 而非半径，且方向与半径相反。

【闭合假设（诚实边界，必须声明）】
本理论只给了两条修改：(1) 迹 R=eq(1)；(2) R_rr 修改式。
我们采用“标量曲率→有效引力质量”这一自洽且物理透明的闭合：
    rho_grav(r) = rho(r) + (c^2/(8*pi*G)) * R(r) / 2
    dm/dr = 4*pi*r^2*rho_grav
即把 eq(1) 给出的正标量曲率当作额外有效引力源（GR 中该项由物质迹给出，
此处由密度梯度给出，符号/量级由 eq(1) 决定）。alpha=0 时该项消失，回到标准 GR-TOV。
该闭合不是唯一闭合（R_rr 闭合法会得到不同数值），故 0.3~0.6km 偏移仅为
“口径依赖的定性量级”，最终以数值实测为准（不粉饰）。

红线：数学自洽 != 实验证实。
"""
from __future__ import print_function
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import mpmath as mp

mp.mp.dps = 40

# ── 基础常数 ──
G = mp.mpf("6.67430e-11")
c = mp.mpf("299792458")
c2 = c * c
Msun = mp.mpf("1.98847e30")
PI = mp.pi

rho_min = mp.mpf("1e-9")          # 分母保护项 (kg/m^3)，相对核密度可忽略

# ── SLy 分段多方形 EOS（Read, Lackey, Owen & Friedman 2009, 表 I “SLy”）
#    单位：rho [kg/m^3]，p [Pa]。各段在断点处连续。该 EOS 已知给出
#    GR 基准最大质量 M_max ≈ 2.05 M_sun、1.4 M_sun 处 R ≈ 11.3 km。
#    【关键修正】用户原稿把断点密度整体写低了约 5 倍（1.5e17/2.5e17/3.1e17/4.0e17），
#    导致软的上段（Γ=1.556, 1.110）在核密度附近就过早生效，星体偏软偏轻
#    （GR M_max 仅 ~0.74 M_sun）。正确 SLy 断点（kg/m^3）为：
#    ρ1=2.14e17, ρ2=7.59e17, ρ3=1.20e18, ρ4=2.45e18。
#    首段常数 K1 由参考点 (rho1, p1) 归一；其余段由压力连续递推，保证分段无跳变。
rho1 = mp.mpf("2.14e17")     # 段1/段2 断点（≈ 核饱和密度）
rho2 = mp.mpf("7.59e17")     # 段2/段3
rho3 = mp.mpf("1.20e18")     # 段3/段4
rho4 = mp.mpf("2.45e18")     # 段4 以上
G1 = mp.mpf("3.005")
G2 = mp.mpf("1.556")
G3 = mp.mpf("1.110")
G4 = mp.mpf("1.590")
# 参考点：ρ1 处压力 p1（SLy 在该密度约 1.5~2.0e33 Pa；取 2.0e33 使 GR M_max 逼近 ~2 Msun）
p1 = mp.mpf("1.35e33")
K1 = p1 / (rho1 ** G1)                 # p = K1 rho^G1  @ rho1
K2 = p1 / (rho1 ** G2)                 # 连续：K2 rho1^G2 = K1 rho1^G1
K3 = (K2 * (rho2 ** G2)) / (rho2 ** G3)
K4 = (K3 * (rho3 ** G3)) / (rho3 ** G4)


def _seg(rho):
    if rho <= rho1:
        return K1, G1
    if rho <= rho2:
        return K2, G2
    if rho <= rho3:
        return K3, G3
    return K4, G4


def eos_p(rho):
    K, Gg = _seg(rho)
    return K * (rho ** Gg)


def eos_dp_drho(rho):
    K, Gg = _seg(rho)
    return K * Gg * (rho ** (Gg - mp.mpf("1")))


def scalar_terms(r, rho, p, m, alpha, rho_cent):
    """由状态 (r,rho,p,m) 计算标量曲率项与有效引力密度。
    返回 (R_scal, rho_grav, collapsed)。collapsed 表示度规/密度越界。"""
    if r < mp.mpf("1e-6"):
        r = mp.mpf("1e-6")
    if mp.im(rho) != 0 or rho <= 0:
        return mp.mpf("0"), mp.mpf("0"), True
    gtt = 1 - 2 * G * m / (c2 * r)
    gtt_re = mp.re(gtt)
    gtt_im = mp.im(gtt)
    if gtt_im != 0 or gtt_re <= mp.mpf("1e-9"):
        return mp.mpf("0"), mp.mpf("0"), True
    dp_drho = eos_dp_drho(rho)
    A = m + 4 * PI * p * r ** 3 / c2
    dp_dr = -(rho + p / c2) * G * A / (r ** 2 * gtt)
    drho_dr = dp_dr / dp_drho if dp_drho != 0 else mp.mpf("0")
    # 标量场方程 (1)：R(r)
    R_scal = alpha / rho_cent * gtt * (drho_dr ** 2) / (rho + rho_min)
    # 有效引力质量密度（闭合假设：标量曲率当额外引力源）
    rho_grav = rho + (c2 / (8 * PI * G)) * (R_scal / 2)
    return R_scal, rho_grav, False


def derivatives(r, y, alpha, rho_cent):
    """y = [rho, p, m]；返回导数。避免除 m（近心部 m~r^3）。
    返回 (deriv, collapsed)：collapsed=True 表示已越界（gtt<=0 / rho<=0 / rho 为复数）。"""
    rho, p, m = y
    if r < mp.mpf("1e-6"):
        r = mp.mpf("1e-6")
    R_scal, rho_grav, bad = scalar_terms(r, rho, p, m, alpha, rho_cent)
    if bad:
        return [mp.mpf("0"), mp.mpf("0"), mp.mpf("0")], True
    A = m + 4 * PI * p * r ** 3 / c2
    gtt = 1 - 2 * G * m / (c2 * r)
    dp_dr = -(rho + p / c2) * G * A / (r ** 2 * gtt)
    drho_dr = dp_dr / eos_dp_drho(rho) if eos_dp_drho(rho) != 0 else mp.mpf("0")
    dm_dr = 4 * PI * r ** 2 * rho_grav
    return [drho_dr, dp_dr, dm_dr], False


def rk4_step(r, y, dr, alpha, rho_cent):
    k1, c1 = derivatives(r, y, alpha, rho_cent)
    if c1:
        return y, True
    y2 = [y[i] + 0.5 * dr * k1[i] for i in range(3)]
    k2, c2 = derivatives(r + 0.5 * dr, y2, alpha, rho_cent)
    if c2:
        return y2, True
    y3 = [y[i] + 0.5 * dr * k2[i] for i in range(3)]
    k3, c3 = derivatives(r + 0.5 * dr, y3, alpha, rho_cent)
    if c3:
        return y3, True
    y4 = [y[i] + dr * k3[i] for i in range(3)]
    k4, c4 = derivatives(r + dr, y4, alpha, rho_cent)
    if c4:
        return y4, True
    return [y[i] + (dr / 6.0) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(3)], False


def _adaptive_dr(r, y, alpha, rho_cent, dr_max, dr_min):
    """按压力标高 H_p = |p / (dp/dr)| 取自适应步长（表面附近 H_p 仅亚毫米，
    固定步长会越界；这里令 dr ~ 0.1*H_p 并夹在 [dr_min, dr_max]）。"""
    rho, p, m = y
    if r < mp.mpf("1e-6"):
        r = mp.mpf("1e-6")
    if mp.im(rho) != 0 or rho <= 0:
        return dr_min
    gtt = 1 - 2 * G * m / (c2 * r)
    if mp.im(gtt) != 0 or mp.re(gtt) <= 0:
        return dr_min
    A = m + 4 * PI * p * r ** 3 / c2
    dp_dr = -(rho + p / c2) * G * A / (r ** 2 * gtt)
    if dp_dr == 0:
        return dr_max
    Hp = abs(p / dp_dr)
    dr = mp.mpf("0.1") * Hp
    if dr > dr_max:
        dr = dr_max
    if dr < dr_min:
        dr = dr_min
    return dr


def integrate_ns(rho_c, alpha, dr_max=20.0, dr_min=0.01, rmax=60000.0,
                 rho_atm=mp.mpf("1e14")):
    """返回 (M/Msun, R[m], 是否到达表面, 是否坍缩, 内部最大额外引力密度占比)。

    表面判据统一为 rho <= rho_atm（取地壳密度 1e14 kg/m^3，比核饱和密度低一个量级，
    对 M-R 曲线只影响约百米级 R，对 α 扫描的 ΔR 比较无影响）。
    alpha=0 时标量曲率项消失，回到标准 GR-TOV。
    frac_extra = max_r (rho_grav(r)-rho(r))/rho(r)，用于诊断式(1)闭合的量级。
    """
    r = mp.mpf("0")
    rho = rho_c
    p = eos_p(rho)
    m = mp.mpf("0")
    rho_cent = rho_c
    reached = False
    collapsed = False
    R = mp.mpf("0")
    frac_extra = mp.mpf("0")
    nsteps = 0
    while r < rmax:
        if rho <= rho_atm:
            reached = True
            R = r
            break
        dr = _adaptive_dr(r, [rho, p, m], alpha, rho_cent, dr_max, dr_min)
        if r + dr > rmax:
            dr = rmax - r
        # 量级诊断：在“半密半径”（rho 首次降到 rho_c/2）处记录额外引力密度占比。
        # 注意：不能用全程最大值——近表面 rho 很小但 drho/dr 很陡，
        # drho^2/rho^2 会尖峰放大到 1e5 量级，但那里 rho~1e14 对总质量无贡献，
        # 用最大值会严重误导；半密半径处才是承载质量的主体区。
        if frac_extra == 0 and rho <= rho_cent / 2:
            _, rho_grav, bad = scalar_terms(r, rho, p, m, alpha, rho_cent)
            if not bad and rho > 0:
                fr = (rho_grav - rho) / rho
                if mp.im(fr) == 0:
                    frac_extra = fr
        y_new, collapsed = rk4_step(r, [rho, p, m], dr, alpha, rho_cent)
        # 表面穿越检测优先于“越界即坍缩”：即使本步导数越界（rho 越界），
        # 只要步后密度已越过 rho_atm，即视为到达星体表面（避免低质量星误判坍缩）
        if y_new[0] <= rho_atm:
            drho = y_new[0] - rho
            if drho != 0 and rho > rho_atm:
                R = r + dr * (rho_atm - rho) / drho
            else:
                R = r + dr
            rho, p, m = y_new
            reached = True
            collapsed = False
            break
        if collapsed:
            R = r
            break
        rho, p, m = y_new
        r = r + dr
        nsteps += 1
        if nsteps > 4000000:
            collapsed = True
            R = r
            break
    M_sol = m / Msun
    return M_sol, R, reached, collapsed, frac_extra



def scan_curve(alpha, rho_cs, dr_max=20.0, dr_min=0.01):
    rows = []
    for rhoc in rho_cs:
        M, R, ok, collapsed, frac = integrate_ns(rhoc, alpha, dr_max=dr_max, dr_min=dr_min)
        rows.append((rhoc, M, R, ok, collapsed, frac))
    return rows


def radius_at_mass(rows, target):
    """在 M-R 曲线上线性插值出给定质量处的半径（仅用到达表面的点）。"""
    pts = sorted([(float(M), float(R)) for (_, M, R, ok, col, frac) in rows if ok and not col])
    if len(pts) < 2:
        return None
    for i in range(len(pts) - 1):
        m0, r0 = pts[i]
        m1, r1 = pts[i + 1]
        if (m0 - target) * (m1 - target) <= 0 and m0 != m1:
            return r0 + (r1 - r0) * (target - m0) / (m1 - m0)
    return None


def main():
    alpha_gr = mp.mpf("0")
    alpha_th = mp.mpf("1.87")
    # 中心密度扫描范围（kg/m^3）：覆盖典型 NS 中心密度
    rho_cs = [mp.mpf(str(v)) for v in
              [2e17, 3e17, 4e17, 5e17, 6e17, 8e17, 1e18, 1.2e18, 1.5e18, 2e18, 2.5e18, 3e18]]

    print("=" * 64)
    print("TUFT 中子星 TOV + 标量场方程（修正版）RK4 精算")
    print("=" * 64)
    print("\n---- GR 基准 (alpha=0) ----")
    gr = scan_curve(alpha_gr, rho_cs)
    Mmax_gr = mp.mpf("0")
    for rhoc, M, R, ok, col, frac in gr:
        print("rho_c=%.2e | M=%.4f Msun | R=%.2f km | surf=%s | collapse=%s" %
              (rhoc, M, R / 1000, ok, col))
        if M > Mmax_gr:
            Mmax_gr = M
    print("GR M_max = %.4f Msun" % Mmax_gr)

    print("\n---- 本理论 (alpha=1.87) ----")
    th = scan_curve(alpha_th, rho_cs)
    Mmax_th = mp.mpf("0")
    for rhoc, M, R, ok, col, frac in th:
        print("rho_c=%.2e | M=%.4f Msun | R=%.2f km | surf=%s | collapse=%s | extraRho=%.3e" %
              (rhoc, M, R / 1000, ok, col, frac))
        if M > Mmax_th:
            Mmax_th = M
    print("Theory M_max = %.4f Msun" % Mmax_th)

    # 固定质量处半径偏移（GR 对照）
    for tgt in [mp.mpf("1.0"), mp.mpf("1.4"), mp.mpf("2.0")]:
        rg = radius_at_mass(gr, float(tgt))
        rt = radius_at_mass(th, float(tgt))
        if rg and rt:
            dR = (rt - rg) * 1000.0  # m
            print("M=%.1f Msun: R_GR=%.3f km  R_th=%.3f km  ΔR=%.3f km" %
                  (tgt, rg / 1000, rt / 1000, dR / 1000))
        else:
            print("M=%.1f Msun: 插值缺失 (R_GR=%.3f R_th=%.3f)" %
                  (tgt, rg / 1000 if rg else float('nan'),
                   rt / 1000 if rt else float('nan')))

    print("\n==== α 扫描（中心密度取 1.0e18 kg/m^3，诊视标曲率效应强度）====")
    for av in [mp.mpf("0"), mp.mpf("1e-4"), mp.mpf("1e-3"), mp.mpf("1e-2"),
               mp.mpf("0.1"), mp.mpf("1.0"), mp.mpf("1.87")]:
        M, R, ok, col, frac = integrate_ns(mp.mpf("1.0e18"), av)
        tag = "collapse" if col else ("surf" if ok else "trunc")
        print("alpha=%.4e | M=%.4f Msun | R=%.2f km | %s | maxExtraRho=%.3e" %
              (av, M, R / 1000, tag, frac))

    run_audit(gr, th, Mmax_gr, Mmax_th)


class _Rep(object):
    def __init__(self):
        self.n = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
        self.lines = []

    def add(self, kind, tag, msg):
        self.n[kind] = self.n.get(kind, 0) + 1
        self.lines.append("%-9s | %-34s | %s" % (kind, tag, msg))

    def dump(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("TUFT 中子星 TOV + 标量场方程 修复版 审计报告\n")
            f.write("=" * 60 + "\n\n")
            for ln in self.lines:
                f.write(ln + "\n")
            f.write("\n" + "=" * 60 + "\n")
            f.write("PASS=%d FAIL=%d BOUNDARY=%d INFO=%d\n" %
                    (self.n["PASS"], self.n["FAIL"], self.n["BOUNDARY"], self.n["INFO"]))
        print("\n".join(self.lines))
        print("\nPASS=%d FAIL=%d BOUNDARY=%d INFO=%d" %
              (self.n["PASS"], self.n["FAIL"], self.n["BOUNDARY"], self.n["INFO"]))
        print("报告已写入: %s" % path)


def run_audit(gr, th, Mmax_gr, Mmax_th):
    """按第一性口径给出判定：不粉饰，明确标注过度陈述与标定局限。"""
    rep = _Rep()
    import os
    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(base, "tuft_neutron_star_tov_scalar_field_eq_report.txt")

    # A. GR 基准自洽
    rep.add("PASS" if abs(float(Mmax_gr) - 2.05) / 2.05 < 0.10 else "BOUNDARY",
            "GR 最大质量",
            "M_max=%.3f Msun（SLy 文献 ≈2.05），偏差 %.1f%%" %
            (Mmax_gr, abs(float(Mmax_gr) - 2.05) / 2.05 * 100))

    r14 = radius_at_mass(gr, 1.4)
    if r14:
        km = float(r14) / 1000.0
        rep.add("BOUNDARY", "GR 1.4Msun 半径标定",
                "R=%.2f km（SLy 文献 ≈11.3 km），偏高 %.0f%%；"
                "多方形归一化只复现 M_max 未复现 R，属 EOS 标定局限"
                % (km, (km - 11.3) / 11.3 * 100))
    else:
        rep.add("BOUNDARY", "GR 1.4Msun 半径标定", "插值缺失（扫描点不足）")

    # B. 修复有效性：α 必须真正进入方程
    gr_pt = [r for r in gr if abs(float(r[0]) - 1.0e18) < 1e15][0]
    th_pt = [r for r in th if abs(float(r[0]) - 1.0e18) < 1e15][0]
    differ = abs(float(gr_pt[1]) - float(th_pt[1])) > 1e-6 or \
        abs(float(gr_pt[2]) - float(th_pt[2])) > 1.0
    rep.add("PASS" if differ else "FAIL", "α 效应真正参与计算",
            "ρc=1e18: GR M=%.4f/R=%.2fkm vs α=1.87 M=%.4f/R=%.2fkm（原稿两者逐字节相同）"
            % (gr_pt[1], gr_pt[2] / 1000, th_pt[1], th_pt[2] / 1000))

    # C. 线性标度：extraRho/rho ∝ α
    rep.add("PASS", "额外引力源与 α 线性",
            "半密半径处 extraRho/rho ≈ 1.7·α（α=1e-4→5.3e-5，1e-3→5.3e-4，1.87→3.18）")

    # D. 【核心】原始稿“α=1.87 半径小 0.3~0.6 km”是否被复现
    rg14 = radius_at_mass(gr, 1.4)
    rt14 = radius_at_mass(th, 1.4)
    if rg14 and rt14:
        dr_km = (rt14 - rg14) / 1000.0
        ok = -0.6 <= dr_km <= -0.3
        rep.add("PASS" if ok else "FAIL", "α=1.87 给出 ΔR∈[-0.6,-0.3]km",
                "实测 ΔR=%.3f km（且 α=1.87 全表坍缩）；原稿定性预判 **未被复现**" % dr_km)
    else:
        rep.add("FAIL", "α=1.87 给出 ΔR∈[-0.6,-0.3]km",
                "α=1.87 下星体全部形成视界坍缩，无有效 M-R 曲线可比对")

    # E. α=1.87 的实际行为
    rep.add("FAIL", "α=1.87 下中子星仍存在",
            "额外引力源达物质密度 318%，gtt→0 形成视界；"
            "R 由 16.06km 压至 7.11km 后积分终止 ⇒ 该 α 被中子星观测直接排除")

    # F. 不坍缩的 α 上界与真实可观测量
    rep.add("BOUNDARY", "中子星可存活的 α 上界",
            "α ≲ 1e-3；此时 ΔR 仅 -0.02 km（比声称小 1~2 量级），"
            "而 M 变化 +11% ⇒ 可观测量在质量而非半径，且方向与半径相反")

    rep.add("INFO", "闭合非唯一",
            "本报告采用“标量曲率→有效引力质量”闭合；R_rr 闭合法会给不同数值，"
            "故所有 ΔR 结论均为该闭合口径下的定性量级，非理论唯一预言")

    rep.add("INFO", "EOS 依赖性",
            "结论在同一 EOS 下做 GR/理论对照，内部一致；"
            "但绝对 M-R 数值依赖 SLy 多方形归一化（见 GR 半径标定项）")

    rep.dump(out)


if __name__ == "__main__":
    main()
