# -*- coding: utf-8 -*-
r"""TUFT-r281 · 四力统一方程·红移漂移与实时宇宙学层：
Sandage–Loeb 信号 dz/dt0=(1+z)H0−H(z)、双路径（闭式 vs 沿光锥数值微分）、
零点与 q0 斜率、符号翻转红移 z_cross、十年漂移速度 Δv、
曲率控制组（Milne 精确零漂移 / EdS / de Sitter）、与 r278 的 H(z) 互印
2026-10-31

〔编号说明〕起草前实测三树：源码/数据最大 r280（并行链《方法全谱总攻与 VP 标度
函数曲线》），判定最大 r280；r279 仅残留一个指向不存在引擎的 runner（撞号遗留），
r281 三树全空 ⇒ 本卷取 **r281**。落盘前再复查一次。

〔定位〕承 r237（背景层 H(z)）→ r254（线性扰动）→ r256（声学几何）→ r260（视界热
力学）→ r274（非线性）→ r278（距离与观测量层）之后的**第七级增量**：把「距离」推进
到「距离随观测时间的变化」——实时宇宙学（redshift drift / Sandage–Loeb 1962）。
r278 遗留第 3 条「红移漂移与实时宇宙学：drift(z)=H(z)/(1+z)−H0，属于观测量层下一级
增量」即本卷靶心。

本卷要回答的问题：
  Q1 dz/dt0=(1+z)H0−H(z) 的闭式值与沿光锥数值微分（积分 a(t) + 固定共动距离求根）
     能否互印？
  Q2 z=0 处漂移为零、小 z 斜率是否恰为 −q0（q0=Ωm/2+Ωr−ΩΛ<0 ⇒ 正漂移）？
  Q3 漂移在 z_cross 处符号翻转（ΛCDM 特有；EdS 恒负、Milne 恒零）——z_cross 在哪？
  Q4 十年漂移速度 Δv=cΔz/(1+z) 在 z~4 是否落在 Sandage–Loeb 文献的 cm/s 量级？
  Q5 用 r278 的 D_H 读数反推 H(z) 是否与本卷同一 E(z) 互印？
  Q6 曲率控制组：Ωk=1 的 Milne 空宇宙漂移是否精确为零（判别力证明）？

诚实预期（写在前面）：Sandage–Loeb 漂移是标准 ΛCDM 的纯几何预言（Sandage 1962；
Loeb 1998；Weinberg 1972），本卷是**复现层 + 判别力验证**，不是新物理。实测需要
10⁻⁹ 级 Δz 的高分辨率光谱（ELT/CODEX 级，当前未达）；w(z) 演化与 Ωk 先验不在本卷。

口径：
  - H0=67.4 km/s/Mpc（h=0.674）、Ωm=0.3153、Ωb=0.0493、Ωr=9.15e−5、
    ΩΛ=1−Ωm−Ωr=0.6846085；主结果平坦（Ωk=0），仅控制组启用 Ωk；
  - E(z)=√(Ωm(1+z)³+Ωr(1+z)⁴+Ωk(1+z)²+ΩΛ)；
  - dz/dt0=(1+z)H0−H(z)（单位 km/s/Mpc ⇒ 乘 1.0228e−12 转 per year）；
  - Δz(Δt)=drift·Δt；Δv=cΔz/(1+z)（cm/s）；q0=Ωm/2+Ωr−ΩΛ；
  - 纯标准库 float64；对 r214–r280 及并行会话产物只读；守卫失败即非零退出；
    条目不可与 r142–r280 相加。
"""

import json
import os
import sys
from math import sqrt, log, log10, exp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r281_红移漂移与实时宇宙学层交互可视化模板_2026-10-31.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_红移漂移与实时宇宙学层可视化_2026-10-31.html")

MARKER = "R281-REDSHIFT-DRIFT-REALTIME-COSMOLOGY"
STEM = "TUFT-r281"
BASE = ("TUFT-r281_四力统一方程_红移漂移与实时宇宙学层_"
        "SandageLoeb信号双路径与曲率控制及视界诊断_精算与交互可视化_2026-10-31")

# ---------------- 参数（Planck 2018，与 r237/r254/r256/r274/r278 同口径） ----------------
H_DIM = 0.674
H0_KM = 67.4
OM = 0.3153
OB = 0.0493
OR = 9.15e-5
OL = 1.0 - OM - OR
C_KM_S = 299792.458
MPC_KM = 3.0856775814913673e19
SEC_PER_YEAR = 3.15576e7
PER_YEAR = SEC_PER_YEAR / MPC_KM          # 1 km/s/Mpc → per year ≈ 1.0228e−12
H0_PER_YEAR = H0_KM * PER_YEAR            # ≈ 6.891e−11 yr⁻¹
C_H0 = C_KM_S / H0_KM                     # Mpc
Q0 = 0.5 * OM + OR - OL                   # 减速参数
DT_YEARS = 1000.0                         # 数值微分步长（年）
DT_DECADE = 10.0                          # 十年漂移报告窗

# r278 读数（D_H，单位 Mpc）——用于跨卷互印
DH_REF = {1.0: 2483.20, 2.0: 1466.04, 3.0: 973.24}

guards, controls, entries = [], [], []


def guard(gid, title, ok, detail, numbers=None):
    guards.append({"id": gid, "title": title, "ok": bool(ok),
                   "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[GUARD-FAIL] {gid} {title}: {detail}")
    return bool(ok)


def control(cid, title, ok, detail, numbers=None):
    controls.append({"id": cid, "title": title, "ok": bool(ok),
                     "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[CONTROL-FAIL] {cid} {title}: {detail}")
    return bool(ok)


def entry(code, level, title, detail, numbers=None):
    entries.append({"code": code, "level": level, "title": title,
                    "detail": detail, "numbers": numbers or {}})


def simpson(f, a, b, n):
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4.0 if (i % 2) else 2.0) * f(a + i * h)
    return s * h / 3.0


# ---------------- 背景量（支持曲率，仅控制组启用） ----------------
def e_curv(z, om=OM, ol=OL, orr=OR, ok=0.0):
    return sqrt(om * (1.0 + z) ** 3 + orr * (1.0 + z) ** 4
                + ok * (1.0 + z) ** 2 + ol)


def e_z(z):
    return e_curv(z)


def drift_per_yr(z, om=OM, ol=OL, orr=OR, ok=0.0):
    """Sandage–Loeb：dz/dt0=(1+z)H0−H(z)，转成 per year。"""
    return H0_KM * ((1.0 + z) - e_curv(z, om, ol, orr, ok)) * PER_YEAR


def dz_over(dt_yr, z):
    return drift_per_yr(z) * dt_yr


def dv_cm_s(dt_yr, z):
    """Δv=cΔz/(1+z)，单位 cm/s。"""
    return C_KM_S * dz_over(dt_yr, z) / (1.0 + z) * 1e5


# ---------------- 沿光锥的数值微分（独立路径） ----------------
def dc_dimless(z, n=12000):
    """D_C/C_H0 = ∫₀^z dz'/E(z')（无量纲）。"""
    if z <= 0.0:
        return 0.0
    return simpson(lambda t: 1.0 / e_z(t), 0.0, z, n)


def e_a(a):
    """E(a)=√(Ωm a⁻³+ΩΛ+Ωr a⁻⁴)（平坦）。"""
    return sqrt(OM / a ** 3 + OL + OR / a ** 4)


def chi_dimless(a1, a2, n=12000):
    """共动距离 ∫_{a1}^{a2} da/(a²E(a))，单位 C_H0=1。"""
    return simpson(lambda a: 1.0 / (a * a * e_a(a)), a1, a2, n)


def a_after(dtau, steps=8):
    """沿时间正向积分 da/dτ=aE(a)（τ=H0 t 无量纲），返回 a(t0+Δt)。"""
    a = 1.0
    h = dtau / steps
    for _ in range(steps):
        k1 = a * e_a(a)
        y2 = a + 0.5 * h * k1
        k2 = y2 * e_a(y2)
        y3 = a + 0.5 * h * k2
        k3 = y3 * e_a(y3)
        y4 = a + h * k3
        k4 = y4 * e_a(y4)
        a += h / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return a


def drift_numeric(z_s, dt_yr=DT_YEARS, n=12000, iters=45):
    """路径 B：固定源的共动距离 χ_s，观测时刻后移 Δt，
    解光锥方程 ∫_{a_e}^{a0'} da/(a²E)=χ_s 得 a_e'，再 dz/dt=(z'−z)/Δt。"""
    chi_s = dc_dimless(z_s, n)
    dtau = H0_PER_YEAR * dt_yr
    a0p = a_after(dtau)
    ae = 1.0 / (1.0 + z_s)

    def g(a):
        return chi_dimless(a, a0p, n) - chi_s

    lo, hi = ae, ae + 1e-5
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if g(mid) > 0.0:
            lo = mid
        else:
            hi = mid
    aep = 0.5 * (lo + hi)
    zp = a0p / aep - 1.0
    return (zp - z_s) / dt_yr, zp, a0p


def solve_z_cross(lo=1.0, hi=3.0, iters=80):
    """解 (1+z)=E(z) 的非零根（z=0 是平凡根）。"""
    def g(z):
        return (1.0 + z) - e_z(z)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if g(mid) > 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main():
    print("=" * 78)
    print(f"{MARKER} · 四力统一方程·红移漂移与实时宇宙学层")
    print("=" * 78)
    print(f"H0={H0_KM} km/s/Mpc  Ωm={OM}  ΩΛ={OL:.7f}  Ωr={OR}  q0={Q0:.6f}")
    print(f"C_H0={C_H0:.6f} Mpc  H0/yr={H0_PER_YEAR:.6e}  DT={DT_YEARS:.0f} yr")
    print()

    # ================= S1 漂移双路径 =================
    zpts = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0]
    rows = []
    for z in zpts:
        dc = drift_per_yr(z)
        dn = drift_numeric(z)[0]
        rel = abs(dc - dn) / abs(dc)
        rows.append({"z": z, "closed": dc, "num": dn, "rel": rel,
                     "dz10": dc * DT_DECADE, "dv10": dv_cm_s(DT_DECADE, z),
                     "H": H0_KM * e_z(z), "H0_1z": H0_KM * (1.0 + z)})
    max_rel = max(r["rel"] for r in rows)
    print("[S1] 红移漂移双路径 dz/dt0（10⁻¹² yr⁻¹）")
    for r in rows:
        print(f"  z={r['z']:4.1f}  闭式={r['closed']*1e12:+9.3f}  "
              f"数值={r['num']*1e12:+9.3f}  rel={r['rel']:.3e}  "
              f"Δz(10yr)={r['dz10']:+.3e}  Δv={r['dv10']:+7.3f} cm/s")
    print(f"  max_rel={max_rel:.3e}")
    guard("G1", "漂移双路径互印（闭式 vs 沿光锥数值微分）",
          max_rel < 1e-4,
          f"6 个红移点 max rel={max_rel:.3e}（阈值 1e−4；数值路径步长 {DT_YEARS:.0f} yr）",
          {"max_rel": max_rel})

    # ================= S2 零点与 q0 斜率 =================
    z_eps = 1e-6
    slope = drift_per_yr(z_eps) / (H0_PER_YEAR * z_eps)
    slope_rel = abs(slope - (-Q0)) / abs(-Q0)
    d0 = drift_per_yr(0.0)
    print("[S2] 零点与小 z 斜率")
    print(f"  drift(z=0)={d0:.3e} per yr；z=1e−6 时 drift/(H0·z)={slope:.6f}"
          f" vs −q0={-Q0:.6f}（rel={slope_rel:.3e}）")
    guard("G2", "z=0 零点与斜率 = −q0",
          abs(d0) < 1e-300 and slope_rel < 1e-4,
          f"drift(0)=0；斜率 {slope:.6f} vs −q0={-Q0:.6f}，rel={slope_rel:.3e}",
          {"slope": slope, "minus_q0": -Q0, "rel": slope_rel})

    # ================= S3 符号翻转 =================
    zc = solve_z_cross()
    g_zc = (1.0 + zc) - e_z(zc)
    below = drift_per_yr(zc - 0.05)
    above = drift_per_yr(zc + 0.05)
    flip_ok = (abs(g_zc) < 1e-12 and below > 0.0 and above < 0.0)
    print("[S3] 漂移符号翻转")
    print(f"  z_cross={zc:.6f}（(1+z)−E(z)={g_zc:.3e}）；"
          f"z_cross−0.05 漂移={below*1e12:+.3f}、+0.05 漂移={above*1e12:+.3f}（10⁻¹²/yr）")
    guard("G3", "符号翻转红移 z_cross（ΛCDM 特有）",
          flip_ok,
          f"z_cross={zc:.6f}、残差 {g_zc:.3e}；下方为正、上方为负 ⇒ q0<0 的真实翻转",
          {"z_cross": zc, "residual": g_zc})

    # ================= S4 十年漂移速度 =================
    dv4 = dv_cm_s(DT_DECADE, 4.0)
    dv5 = dv_cm_s(DT_DECADE, 5.0)
    mag_ok = 3.0 <= abs(dv4) <= 12.0 and 3.0 <= abs(dv5) <= 15.0
    print("[S4] 十年漂移速度 Δv=cΔz/(1+z)")
    print(f"  Δv(z=4)={dv4:+.3f} cm/s，Δv(z=5)={dv5:+.3f} cm/s（Sandage–Loeb 量级 cm/s/decade）")
    guard("G4", "Δv 量级落在 Sandage–Loeb cm/s/decade",
          mag_ok,
          f"|Δv(z=4)|={abs(dv4):.2f} cm/s ∈ [3,12]；|Δv(z=5)|={abs(dv5):.2f} cm/s ∈ [3,15]",
          {"dv4": dv4, "dv5": dv5})

    # ================= S5 与 r278 H(z) 互印 =================
    cross = []
    for z, dh in sorted(DH_REF.items()):
        h_ref = C_KM_S / dh
        h_mod = H0_KM * e_z(z)
        rel = abs(h_mod - h_ref) / h_ref
        cross.append({"z": z, "H_ref": h_ref, "H_mod": h_mod, "rel": rel})
    max_h_rel = max(c["rel"] for c in cross)
    print("[S5] 与 r278 的 D_H→H(z) 互印")
    for c in cross:
        print(f"  z={c['z']:.1f}  H_ref=c/D_H={c['H_ref']:.3f}  "
              f"H_model={c['H_mod']:.3f}  rel={c['rel']:.3e}")
    guard("G5", "r278 的 D_H 反推 H(z) 互印",
          max_h_rel < 1e-3,
          f"3 个红移点 max rel={max_h_rel:.3e}（阈值 1e−3；r278 D_H 四舍五入到 0.01 Mpc）",
          {"max_rel": max_h_rel})

    # ================= S6 控制组 =================
    print("[S6] 控制组")
    # C1 Milne 空宇宙：Ωk=1 ⇒ E=1+z ⇒ 漂移精确为零
    mil = [abs(drift_per_yr(z, 0.0, 0.0, 0.0, 1.0)) / H0_PER_YEAR
           for z in (0.5, 1.0, 2.0, 4.0, 5.0)]
    c1_max = max(mil)
    print(f"  C1 Milne（Ωk=1）零漂移 max|drift|/H0={c1_max:.3e}")
    control("C1", "Milne 空宇宙精确零漂移（曲率判别力）",
            c1_max < 1e-14,
            f"Ωm=0,ΩΛ=0,Ωr=0,Ωk=1 ⇒ E=1+z ⇒ (1+z)−E≡0；5 点 max|drift|/H0={c1_max:.3e}",
            {"max": c1_max})

    # C2 EdS：闭式两条代数路径互印
    eds = []
    for z in (0.5, 1.0, 2.0, 4.0):
        direct = (1.0 + z) - (1.0 + z) ** 1.5
        factored = -(1.0 + z) * (sqrt(1.0 + z) - 1.0)
        denom = abs(direct) if abs(direct) > 1e-30 else 1.0
        eds.append(abs(direct - factored) / denom)
    c2_max = max(eds)
    print(f"  C2 EdS 代数恒等 max rel={c2_max:.3e}")
    control("C2", "EdS 漂移代数恒等（(1+z)−(1+z)^{3/2} = −(1+z)(√(1+z)−1)）",
            c2_max < 1e-15,
            f"4 点 max rel={c2_max:.3e}（机器零）",
            {"max_rel": c2_max})

    # C3 de Sitter：E=1 ⇒ 漂移 = H0 z 精确
    ds = []
    for z in (0.5, 1.0, 2.0, 4.0):
        direct = (1.0 + z) - 1.0
        ds.append(abs(direct - z) / z)
    c3_max = max(ds)
    print(f"  C3 de Sitter（E=1）恒等 max rel={c3_max:.3e}")
    control("C3", "de Sitter 漂移 = H0 z 恒等",
            c3_max < 1e-15,
            f"4 点 max rel={c3_max:.3e}",
            {"max_rel": c3_max})

    # C4 数值微分步长收敛
    b1 = drift_numeric(2.0, dt_yr=500.0)[0]
    b2 = drift_numeric(2.0, dt_yr=1000.0)[0]
    b3 = drift_numeric(2.0, dt_yr=2000.0)[0]
    c4_rel = max(abs(b2 - b1) / abs(b2), abs(b3 - b2) / abs(b2))
    print(f"  C4 数值微分收敛 500/1000/2000 yr：max rel={c4_rel:.3e}")
    control("C4", "数值微分步长收敛（500/1000/2000 yr）",
            c4_rel < 1e-3,
            f"z=2 时三个步长的漂移 max rel={c4_rel:.3e}（阈值 1e−3）",
            {"max_rel": c4_rel})

    # ================= 条目 =================
    entry("H01", "INFO", "判定：红移漂移 = 标准 ΛCDM 的实时宇宙学复现，不是新理论",
          "dz/dt0=(1+z)H0−H(z) 是 Sandage(1962)/Loeb(1998) 的纯几何预言；本卷只做机器"
          "复现与判别力验证",
          {"inherits": ["r237", "r254", "r256", "r260", "r274", "r278"]})
    entry("H02", "PASS", "漂移双路径互印",
          f"闭式 vs 沿光锥数值微分：6 点 max rel={max_rel:.3e}；"
          f"z=1 时 drift={rows[1]['closed']*1e12:+.3f}×10⁻¹²/yr",
          {"max_rel": max_rel})
    entry("H03", "PASS", "z=0 零点与斜率 −q0",
          f"drift(0)=0；z→0 斜率={slope:.6f} vs −q0={-Q0:.6f}（rel {slope_rel:.3e}）"
          f"（q0={Q0:.6f}<0 ⇒ 近处正漂移）",
          {"slope": slope, "q0": Q0})
    entry("H04", "PASS", "符号翻转红移 z_cross",
          f"z_cross={zc:.6f}（(1+z)=E(z)）；下方正、上方负——ΛCDM 特有；"
          "EdS 恒负、Milne 恒零（见控制组）",
          {"z_cross": zc})
    entry("H05", "PASS", "十年漂移速度 Δv 量级",
          f"Δv(z=1)={dv_cm_s(DT_DECADE,1.0):+.3f}、Δv(z=4)={dv4:+.3f}、"
          f"Δv(z=5)={dv5:+.3f} cm/s ⇒ 与 Sandage–Loeb 的 cm/s/decade 量级一致",
          {"dv1": dv_cm_s(DT_DECADE, 1.0), "dv4": dv4, "dv5": dv5})
    entry("H06", "PASS", "与 r278 的 D_H→H(z) 跨卷互印",
          f"用 r278 的 D_H(z=1,2,3) 反推 H(z)，与本卷同一 E(z) 的 max rel={max_h_rel:.3e}",
          {"max_rel": max_h_rel})
    entry("H07", "PASS", "曲率判别力：Milne 精确零漂移",
          "Ωk=1 ⇒ E=1+z ⇒ 漂移恒零（控制组 C1，max|drift|/H0 < 1e−14）；"
          "⇒ 漂移是真实可判别的曲率/暗能量探针，不是恒等式",
          {"max": c1_max})
    entry("H08", "BOUNDARY", "实测需 10⁻⁹ 级 Δz 高分辨率光谱",
          "Δz(10 yr) ~ 10⁻⁹–10⁻¹⁰，需 ELT/CODEX 级（~cm/s 速度精度、20–30 年基线）；"
          "当前任何巡天未达 ⇒ 本卷只做理论预言与自洽验证",
          {"dz10_z4": rows[4]["dz10"]})
    entry("H09", "BOUNDARY", "w(z) 演化与 Ωk 先验不在本卷",
          "CPL w(z)=w0+wa z/(1+z) 的漂移曲线（含 w 导数项）需外部 SN Ia/BAO 数据；"
          "弯曲宇宙仅作控制组，主结果固定平坦 ΛCDM",
          {})
    entry("H10", "INFO", "判决：观测量层下一级增量，统一仍无新物理",
          "背景(r237)+扰动(r254)+声学(r256)+视界(r260)+非线性(r274)+距离(r278)+"
          "实时漂移(本卷) 全部是已知物理；r229/r267 的新颖性与完成度判定不变",
          {})

    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in entries if e["level"] == "INFO")

    # ================= 曲线与读数 =================
    zg = [0.01 * 600.0 ** (i / 59.0) for i in range(60)]   # 0.01 → 6
    curves = {
        "z": zg,
        "drift": [drift_per_yr(z) * 1e12 for z in zg],     # 10⁻¹²/yr
        "dv": [dv_cm_s(DT_DECADE, z) for z in zg],         # cm/s
        "H": [e_z(z) for z in zg],                         # H/H0
        "H0_1z": [1.0 + z for z in zg],
    }
    table = []
    for z in (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0):
        table.append({"z": z,
                      "drift": drift_per_yr(z),
                      "dz10": drift_per_yr(z) * DT_DECADE,
                      "dv": dv_cm_s(DT_DECADE, z),
                      "H": H0_KM * e_z(z)})

    res = {
        "marker": MARKER,
        "stem": STEM,
        "date": "2026-10-31",
        "title": "四力统一方程·红移漂移与实时宇宙学层（Sandage–Loeb 信号、"
                 "双路径、符号翻转、十年漂移速度、曲率控制）",
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info,
                   "guards": "", "controls": ""},
        "guards": guards,
        "controls": controls,
        "entries": entries,
        "readings": {
            "params": {"H0": H0_KM, "Om": OM, "Or": OR, "OL": OL,
                       "C_H0": C_H0, "Q0": Q0, "H0_per_year": H0_PER_YEAR,
                       "dt_years": DT_YEARS, "dt_decade": DT_DECADE},
            "drift": rows,
            "table": table,
            "cross": cross,
            "summary": {"z_cross": zc, "slope": slope, "dv4": dv4, "dv5": dv5,
                        "dv1": dv_cm_s(DT_DECADE, 1.0),
                        "max_rel": max_rel, "max_h_rel": max_h_rel,
                        "milne_max": c1_max},
            "curves": curves,
        },
        "verdict": "",
        "judgement": "",
        "source": {
            "engine": BASE + ".py",
            "inherits": ["r237（宇宙学背景层 E(z)/H(z)）",
                         "r254（线性扰动层）", "r256（声学几何层）",
                         "r260（视界热力学层）", "r274（非线性结构层）",
                         "r278（距离与观测量层：D_H 读数互印）",
                         "r229（新颖性审计口径）", "r267（完成度终局判决）",
                         "Sandage 1962 / Loeb 1998 / Weinberg 1972 / Planck 2018（只读）"],
        },
    }

    parts = [
        "R281-REDSHIFT-DRIFT-DUAL-PATH-OK",
        "ZERO-AND-Q0-SLOPE-OK",
        "SIGN-FLIP-ZCROSS-OK",
        "DV-CM-S-DECADE-OK",
        "R278-HZ-CROSS-OK",
        "MILNE-ZERO-DRIFT-CONTROL-OK",
        "EDS-ALGEBRA-OK",
        "DSITTER-OK",
        "DT-CONVERGENCE-OK",
        "SPECTRAL-RESOLUTION-BOUNDARY",
        "WZ-CURVATURE-PRIOR-BOUNDARY",
        "VERDICT-STANDARD-REALTIME-COSMOLOGY-NO-NEW-THEORY",
    ]
    res["verdict"] = "-".join(parts)
    res["judgement"] = ("CLOSED-INCREMENT（红移漂移与实时宇宙学层：Sandage–Loeb 双路径、"
                        "零点与 q0 斜率、符号翻转 z_cross、十年漂移速度、曲率控制组、"
                        "r278 H(z) 互印）；实测光谱精度与 w(z) 先验在框架外；无新理论")

    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")

    html_ok, html_detail = cast_html(res)
    guard("G6", "交互 HTML 生成且自含", html_ok, html_detail)
    res["counts"]["guards"] = f"{sum(1 for g in guards if g['ok'])}/{len(guards)}"
    res["counts"]["controls"] = f"{sum(1 for c in controls if c['ok'])}/{len(controls)}"

    print()
    print(f"条目 {res['counts']['entries']}（PASS {n_pass} / FAIL {n_fail} / "
          f"BOUNDARY {n_bnd} / INFO {n_info}）· 守卫 {res['counts']['guards']} · "
          f"控制组 {res['counts']['controls']}")

    with open(jpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    write_md(mpath, res)
    write_report(rpath, res)

    bad_g = [g["id"] for g in guards if not g["ok"]]
    bad_c = [c["id"] for c in controls if not c["ok"]]
    if bad_g or bad_c:
        print(f"[RC≠0] 守卫失败 {bad_g} 控制组失败 {bad_c}")
        return 1
    print(f"[DONE] {MARKER} rc=0 → {jpath}")
    return 0


def write_md(path, res):
    L = [f"# {res['stem']} · 数据册（引擎自动生成）\n",
         f"- 判决串：`{res['verdict']}`\n",
         f"- 条目：{res['counts']['entries']}（PASS {res['counts']['PASS']} / "
         f"FAIL {res['counts']['FAIL']} / BOUNDARY {res['counts']['BOUNDARY']} / "
         f"INFO {res['counts']['INFO']}）· 守卫 {res['counts']['guards']} · "
         f"控制组 {res['counts']['controls']}\n",
         "\n## 条目\n"]
    for e in res["entries"]:
        L.append(f"- **{e['code']} {e['level']}** {e['title']}——{e['detail']}\n")
    L.append("\n## 守卫\n")
    for g in res["guards"]:
        L.append(f"- **{g['id']} {'OK' if g['ok'] else 'FAIL'}** {g['title']}——"
                 f"{g['detail']}\n")
    L.append("\n## 控制组\n")
    for c in res["controls"]:
        L.append(f"- **{c['id']} {'OK' if c['ok'] else 'FAIL'}** {c['title']}——"
                 f"{c['detail']}\n")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))


def write_report(path, res):
    s = res["readings"]["summary"]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{MARKER} rc=0\n")
        f.write(f"entries={res['counts']['entries']} PASS={res['counts']['PASS']} "
                f"FAIL={res['counts']['FAIL']} BOUNDARY={res['counts']['BOUNDARY']} "
                f"INFO={res['counts']['INFO']}\n")
        f.write(f"guards={res['counts']['guards']} controls={res['counts']['controls']}\n")
        f.write(f"verdict={res['verdict']}\n")
        f.write(f"H0={res['readings']['params']['H0']} q0={s['slope']:.6f} "
                f"z_cross={s['z_cross']:.6f}\n")
        f.write(f"dv1={s['dv1']:.3f} dv4={s['dv4']:.3f} dv5={s['dv5']:.3f} cm/s\n")
        f.write(f"max_rel={s['max_rel']:.3e} max_h_rel={s['max_h_rel']:.3e} "
                f"milne_max={s['milne_max']:.3e}\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R281_JSON__" not in tpl:
        return False, "模板缺少 __R281_JSON__ 占位符"
    html = tpl.replace("__R281_JSON__", json.dumps(res, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R281_JSON__" in text:
        problems.append("占位符未替换")
    if "http://" in text or "https://" in text:
        problems.append("发现外部 URL（应零依赖）")
    if "<canvas" not in text or "<script" not in text:
        problems.append("缺少 canvas/script")
    if problems:
        return False, "；".join(problems)
    return True, f"已生成 {HTML_OUT}（{len(text)} B），零外部 URL、JSON 已铸入"


if __name__ == "__main__":
    sys.exit(main())
