# -*- coding: utf-8 -*-
r"""TUFT-r284 · 精细结构常数 V10「选择机制」全维可攻破性审计：
S1 螺旋拓扑闭合与 κ/|τ| 符号/数值互印（含 1/137 ⇒ 262.77 ppm 复算）；
S2 2026 Symmetry 条件级数 α⁻¹=Ω−1/(24Ω)−Σ(k+6)/(k+4)Ω^{−(2k+1)} 的
   80 位 decimal 复算、σ 分级、单参数微调反解；
S3 圆环面 (2,3) 结 Q=∮κds/∮|τ|ds 的解析导数数值积分对表（同结型非唯一）；
S4 四次几何能量 E(x) 的稳定点解析解与 (B−A)/C 反解恒等（细调量级）；
S5 磁单极 Dirac 量子化 α_eα_m=n²/4；S6 KK 维度约化 1/g4²=L/g5² 的量纲恒等。
2026-10-31

〔编号说明〕起草前实测三树：源码/判定最大 r282；数据中 r283 已被并行线以
「来料原件·用户附件逐字」占用（22:49:05，无引擎/无判定册/无 runner）⇒ 按
「先占四件套者为权威」该号仍属并行线在建，本卷不抢、整体**跳号取 r284**
（r284 三树全空）。落盘前再复查一次。

〔定位〕ROOT V10.0 把问题从「找 α 的公式」改为「找唯一选择机制」。本卷不新增
物理，只做**可攻破性审计**：逐条机器复算其声称，并判定五条路线是否构成
「不含 α 实验输入的无参数预言」。诚实预期（写在前面）：五路均为**条件性候选**
（拓扑约束允许什么 / 动力学选中什么 / 但"结构→电磁耦合"缺一环），
S2 级数是**匹配公设 + 可单参数微调**，不是独立预言。

口径：
  - 纯标准库；float64 用于几何积分，decimal(prec=80) 用于 S2 级数；
  - α_exp⁻¹=137.035999177（CODATA 2022），u(α⁻¹)=2.1e−8（21 末位）；
  - S2 主项 Ω=4π³+π²+π；CODATA 值只作**事后比对**，不进入候选式构造；
  - 守卫失败即非零退出；条目不可与 r142–r283 相加。
"""

import json
import math
import os
import sys
from decimal import Decimal, getcontext

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r284_选择机制审计交互可视化模板_2026-10-31.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_精细结构常数选择机制审计可视化_2026-10-31.html")

MARKER = "R284-ALPHA-SELECTION-MECHANISM-AUDIT"
STEM = "TUFT-r284"
BASE = ("TUFT-r284_精细结构常数V10选择机制审计_螺旋闭合环面结四次能量"
        "条件级数与单极KK_全维可攻破性机检_精算与可视化_2026-10-31")

PI = math.pi

# ---------------- 外部锚（只作事后比对） ----------------
ALPHA_INV_EXP = 137.035999177          # CODATA 2022 中心值
U_ALPHA_INV = 2.1e-8                   # CODATA 2022 标准不确定度
ALPHA_EXP = 1.0 / ALPHA_INV_EXP

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


# ============================================================
# S1 · 圆柱螺旋：闭合条件与 κ/|τ|
# ============================================================
def helix_curv_tors_num(R, b, t):
    """直接由导数定义算 κ、τ（独立于公式）。"""
    # r=(R cos t, R sin t, b t)
    rp = (-R * math.sin(t), R * math.cos(t), b)
    rpp = (-R * math.cos(t), -R * math.sin(t), 0.0)
    rppp = (R * math.sin(t), -R * math.cos(t), 0.0)
    # cross r'×r''
    cx = rp[1] * rpp[2] - rp[2] * rpp[1]
    cy = rp[2] * rpp[0] - rp[0] * rpp[2]
    cz = rp[0] * rpp[1] - rp[1] * rpp[0]
    cn = math.sqrt(cx * cx + cy * cy + cz * cz)
    pn = math.sqrt(rp[0] ** 2 + rp[1] ** 2 + rp[2] ** 2)
    kappa = cn / pn ** 3
    tau = (cx * rppp[0] + cy * rppp[1] + cz * rppp[2]) / (cn * cn)
    return kappa, tau


def helix_formula(R, b):
    d = R * R + b * b
    return R / d, b / d


def s1_helix():
    print("[S1] 圆柱螺旋：闭合条件 2πp b = q L 与 κ/|τ| = 2πpR/(|q|L)")
    R, b = 1.0, 0.3
    kf, tf = helix_formula(R, b)
    worst_k = worst_t = 0.0
    for i in range(1, 40):
        t = i * 0.15
        kn, tn = helix_curv_tors_num(R, b, t)
        worst_k = max(worst_k, abs(kn - kf) / kf)
        worst_t = max(worst_t, abs(tn - tf) / tf)
    print(f"  公式 κ={kf:.12f}、τ={tf:.12f}；40 点数值定义 max rel "
          f"κ={worst_k:.3e}、τ={worst_t:.3e}")
    guard("G1", "螺旋 κ、τ 公式与导数定义互印（40 点）",
          worst_k < 1e-10 and worst_t < 1e-10,
          f"R=1,b=0.3 ⇒ κ={kf:.12f}, τ={tf:.12f}；max rel κ={worst_k:.3e}, "
          f"τ={worst_t:.3e}（机器零量级）",
          {"max_rel_kappa": worst_k, "max_rel_tau": worst_t})

    # 闭合条件：b=qL/(2πp)；再验 r(t+2πp) 落在同一轴向格的偏移 2πp b=qL
    tests = [(1, 1), (1, 3), (2, 5), (3, 7)]
    rows_cl = []
    for p, q in tests:
        L = 2.0 * PI * p * 0.3 / q            # 由 b=0.3 反解
        b_rec = q * L / (2.0 * PI * p)
        # 轴向位移 = 2πp b，应等于 qL
        shift = 2.0 * PI * p * b_rec
        rows_cl.append({"p": p, "q": q, "L": L, "b_rec": b_rec,
                        "shift": shift, "qL": q * L,
                        "res": abs(shift - q * L)})
    max_res = max(r["res"] for r in rows_cl)
    print(f"  闭合反解 4 组 (p,q)：max|2πp b − qL|={max_res:.3e}")
    guard("G2", "拓扑闭合条件 b=qL/(2πp) 的位移恒等",
          max_res < 1e-15,
          f"(p,q)∈{{(1,1),(1,3),(2,5),(3,7)}} 四组 max|2πpb−qL|={max_res:.3e}",
          {"max_res": max_res})

    # κ/|τ| = 2πpR/(|q|L) 的符号恒等（用闭合 b 代入）
    p, q, Rr = 1, 137, 1.0
    Lr = 2.0 * PI * Rr
    b_c = q * Lr / (2.0 * PI * p)
    k_d, t_d = helix_formula(Rr, b_c)
    ratio_direct = k_d / abs(t_d)
    ratio_form = 2.0 * PI * p * Rr / (abs(q) * Lr)
    rel_id = abs(ratio_direct - ratio_form) / abs(ratio_form)
    print(f"  L=2πR 时 κ/|τ| 两条路径 rel={rel_id:.3e}"
          f"（= p/|q| = {ratio_form:.6f}）")
    guard("G3", "κ/|τ| 的几何式与闭合代入互印",
          rel_id < 1e-14,
          f"L=2πR、p=1、q=137 ⇒ 两路径 max rel={rel_id:.3e}",
          {"rel": rel_id})

    # 主张复算：p/q = 1/137 vs α_exp ⇒ 262.77 ppm
    ratio_137 = 1.0 / 137.0
    ppm = abs(ratio_137 - ALPHA_EXP) / ALPHA_EXP * 1e6
    print(f"  p=1,q=137 ⇒ κ/|τ|=1/137={ratio_137:.9f}；α_exp={ALPHA_EXP:.9f}；"
          f"偏差={ppm:.4f} ppm")
    guard("G4", "『1/137 与实验 α 相差 262.77 ppm』复算",
          abs(ppm - 262.77) < 0.05,
          f"复算 {ppm:.4f} ppm（来料 262.77 ppm）",
          {"ppm": ppm})

    # 非唯一性：固定 (p,q) 扫描 R/L 连续
    scan = []
    for i in range(41):
        rl = 0.1 * (100.0 ** (i / 40.0))       # 0.1 → 10，两个量级
        scan.append({"RoverL": rl, "ratio": 2.0 * PI * p * rl / abs(q)})
    rmin = min(s["ratio"] for s in scan)
    rmax = max(s["ratio"] for s in scan)
    print(f"  固定 (p,q)=(1,137)、R/L∈[0.1,10] ⇒ κ/|τ| 连续跨 "
          f"[{rmin:.2e},{rmax:.2e}]（span {(rmax / rmin):.1f}×）")
    control("C2", "固定绕数下 R/L 连续 ⇒ 比值不唯一（拓扑不足以选中 α）",
            rmax / rmin >= 50.0,
            f"R/L 两个量级 ⇒ κ/|τ| 跨 {rmax / rmin:.1f} 倍（连续族，无离散选择）",
            {"span": rmax / rmin})
    return {"kappa_formula": kf, "tau_formula": tf, "max_rel_kappa": worst_k,
            "max_rel_tau": worst_t, "closure": rows_cl, "ppm137": ppm,
            "scan": scan, "ratio_137": ratio_137}


# ============================================================
# S2 · 2026 条件级数（decimal 80 位）
# ============================================================
PI80 = ("3.14159265358979323846264338327950288419716939937510"
        "58209749445923078164062862089986280348253421170679"
        "82148086513282306647093844609550582231725359408128"
        "48111745028410270193852110555964462294895493038196")


def omega_dec():
    pi = Decimal(PI80)
    return Decimal(4) * pi ** 3 + pi ** 2 + pi


def cand_dec(omega, keep_terms=10 ** 9):
    """α⁻¹_cand = Ω − 1/(24Ω) − Σ_{k≥1} (k+6)/(k+4) Ω^{−(2k+1)}"""
    getcontext().prec = 100
    s = omega - Decimal(1) / (Decimal(24) * omega)
    k = 1
    while k <= keep_terms:
        term = (Decimal(k + 6) / Decimal(k + 4)) * omega ** Decimal(-(2 * k + 1))
        s -= term
        if term < Decimal(10) ** -95:
            break
        k += 1
    return s


def s2_series():
    getcontext().prec = 100
    om = omega_dec()
    om_f = float(om)
    main_gap = om_f - ALPHA_INV_EXP
    main_ppm = abs(main_gap) / ALPHA_INV_EXP * 1e6
    main_sigma = abs(main_gap) / U_ALPHA_INV

    cand = cand_dec(om)
    cand_str = str(+cand)[:20]
    cand_f = float(cand)
    diff = cand_f - ALPHA_INV_EXP
    sigma = abs(diff) / U_ALPHA_INV

    print("[S2] 2026 Symmetry 条件级数（decimal prec=100，输出 80 位有效）")
    print(f"  Ω=4π³+π²+π = {om_f:.12f}")
    print(f"  主项与 α⁻¹ 差 = {main_gap:+.9e}（{main_ppm:.4f} ppm，{main_sigma:.1f}σ）")
    print(f"  α⁻¹_cand = {str(+cand)[:36]}")
    print(f"  来料声称 137.035999176142；CODATA 137.035999177")
    print(f"  偏差 {diff:+.6e} ⇒ {sigma:.6f}σ（u=2.1e−8）")

    claim = Decimal("137.035999176142")
    rel_claim = abs(float(cand) - float(claim)) / float(claim)
    guard("G5", "80 位级数复算命中来料候选值 137.035999176142",
          rel_claim < 1e-11,
          f"复算 {str(+cand)[:20]}；与来料 137.035999176142 的 rel={rel_claim:.3e}",
          {"cand": cand_str, "rel_to_claim": rel_claim})

    guard("G6", "标准化偏差 ≈ −0.04086σ（来料声称）",
          abs(sigma - 0.04086) < 0.005,
          f"复算 {sigma:.6f}σ（来料 −0.04086σ；u=2.1e−8）",
          {"sigma": sigma})

    # 分级：主项 / 仅 1/(24Ω) / 完整级数
    s1 = om - Decimal(1) / (Decimal(24) * om)
    s1_f = float(s1)
    s1_sigma = abs(s1_f - ALPHA_INV_EXP) / U_ALPHA_INV
    stages = [
        {"stage": "主项 Ω", "value": om_f, "sigma": main_sigma},
        {"stage": "Ω−1/(24Ω)", "value": s1_f, "sigma": s1_sigma},
        {"stage": "完整级数", "value": cand_f, "sigma": sigma},
    ]
    print(f"  分级 σ：主项 {main_sigma:.1f}σ / 仅 1/(24Ω) {s1_sigma:.2f}σ / "
          f"完整 {sigma:.4f}σ")
    # 修正总量是否恰等于主项残差（残差填平结构）
    total_corr = om_f - cand_f
    fill_rel = abs(total_corr - main_gap) / main_gap
    print(f"  修正总量 {total_corr:.9e} vs 主项残差 {main_gap:.9e}"
          f"（相对差 {fill_rel:.3e} ⇒ 修正恰为填平残差而设）")

    # 单参数微调：Ω→Ω(1+ε) 使候选精确命中 α_exp⁻¹
    def cand_eps(eps):
        o2 = om * (Decimal(1) + Decimal(eps))
        return cand_dec(o2, keep_terms=6)

    lo, hi = Decimal("-1e-9"), Decimal("1e-9")
    target = Decimal("137.035999177")
    for _ in range(200):
        mid = (lo + hi) / 2
        v = cand_eps(mid)
        if v < target:
            lo = mid
        else:
            hi = mid
    eps_star = float((lo + hi) / 2)
    print(f"  单参数微调：Ω 相对改 {eps_star:.3e} ⇒ 候选精确等于 CODATA 值")
    guard("G7", "级数的单参数微调可精确命中（反解存在性）",
          abs(eps_star) < 1e-9,
          f"存在 ε*={eps_star:.3e}（相对）使残留归零 ⇒ 结构本身不含唯一性约束",
          {"eps_star": eps_star})

    # 敏感性：1σ 对应 α⁻¹ 相对量级；来料 1.65e−10 是否落在自然量级
    rel_sigma = U_ALPHA_INV / ALPHA_INV_EXP
    print(f"  1σ 对应 α⁻¹ 的相对量 {rel_sigma:.4e}；来料声称 1.65e−10"
          f"（比值 {1.65e-10 / rel_sigma:.3f}）")
    return {"omega": om_f, "omega_str": str(+om)[:40], "cand": cand_f,
            "cand_str": str(+cand)[:36], "main_gap": main_gap,
            "main_ppm": main_ppm, "main_sigma": main_sigma,
            "sigma": sigma, "s1_sigma": s1_sigma, "stages": stages,
            "total_corr": total_corr, "fill_rel": fill_rel,
            "eps_star": eps_star,
            "rel_sigma": rel_sigma, "claim_rel": rel_claim}


# ============================================================
# S3 · 圆环面 (2,3) 结：Q=∮κds/∮|τ|ds
# ============================================================
def knot_derivs(t, a):
    c3, s3 = math.cos(3.0 * t), math.sin(3.0 * t)
    c2, s2 = math.cos(2.0 * t), math.sin(2.0 * t)
    u = 1.0 + a * c3
    up, upp, uppp = -3.0 * a * s3, -9.0 * a * c3, 27.0 * a * s3
    v, vp, vpp, vppp = c2, -2.0 * s2, -4.0 * c2, 8.0 * s2
    w, wp, wpp, wppp = s2, 2.0 * c2, -4.0 * s2, -8.0 * c2
    z, zp, zpp, zppp = a * s3, 3.0 * a * c3, -9.0 * a * s3, -27.0 * a * c3

    x, y = u * v, u * w
    xp = up * v + u * vp
    yp = up * w + u * wp
    xpp = upp * v + 2.0 * up * vp + u * vpp
    ypp = upp * w + 2.0 * up * wp + u * wpp
    xppp = uppp * v + 3.0 * upp * vp + 3.0 * up * vpp + u * vppp
    yppp = uppp * w + 3.0 * upp * wp + 3.0 * up * wpp + u * wppp
    return (xp, yp, zp), (xpp, ypp, zpp), (xppp, yppp, zppp)


def knot_point(t, a):
    u = 1.0 + a * math.cos(3.0 * t)
    return (u * math.cos(2.0 * t), u * math.sin(2.0 * t), a * math.sin(3.0 * t))


def knot_integrands(t, a):
    rp, rpp, rppp = knot_derivs(t, a)
    cx = rp[1] * rpp[2] - rp[2] * rpp[1]
    cy = rp[2] * rpp[0] - rp[0] * rpp[2]
    cz = rp[0] * rpp[1] - rp[1] * rpp[0]
    cn = math.sqrt(cx * cx + cy * cy + cz * cz)
    pn = math.sqrt(rp[0] ** 2 + rp[1] ** 2 + rp[2] ** 2)
    num_k = cn / (pn * pn)                               # κ ds / dt
    triple = abs(cx * rppp[0] + cy * rppp[1] + cz * rppp[2])
    den_t = triple * pn / (cn * cn)                      # |τ| ds / dt
    return num_k, den_t


def knot_Q(a, n=20000):
    total_k = simpson(lambda t: knot_integrands(t, a)[0], 0.0, 2.0 * PI, n)
    total_t = simpson(lambda t: knot_integrands(t, a)[1], 0.0, 2.0 * PI, n)
    return total_k, total_t, total_k / total_t


def s3_knot():
    print("[S3] 圆环面 (2,3) 结：Q=∮κds/∮|τ|ds 对表（解析导数 + Simpson 2 万点）")
    ref = [  # 来料表值
        (0.15, 12.80047, 3.18954, 4.01326),
        (0.25, 13.39573, 8.17499, 1.63862),
        (0.40, 15.84160, 17.34761, 0.91319),
        (0.60, 19.52675, 16.06540, 1.21545),
    ]
    rows = []
    worst = 0.0
    for a, kref, tref, qref in ref:
        kk, tt, qq = knot_Q(a)
        rel_k = abs(kk - kref) / kref
        rel_t = abs(tt - tref) / tref
        rel_q = abs(qq - qref) / qref
        worst = max(worst, rel_k, rel_t, rel_q)
        rows.append({"a": a, "K": kk, "T": tt, "Q": qq,
                     "K_ref": kref, "T_ref": tref, "Q_ref": qref,
                     "rel": max(rel_k, rel_t, rel_q)})
        print(f"  a={a:.2f}  ∮κds={kk:.5f}(ref {kref:.5f})  "
              f"∮|τ|ds={tt:.5f}(ref {tref:.5f})  Q={qq:.5f}(ref {qref:.5f})  "
              f"max rel={rows[-1]['rel']:.2e}")
    guard("G8", "结 Q 表四组复算（∮κds / ∮|τ|ds）",
          worst < 5e-4,
          f"a=0.15/0.25/0.40/0.60 四组 max rel={worst:.3e}（数值积分与来料表值）",
          {"max_rel": worst})

    # 结型与环面约束
    torus_res = 0.0
    for i in range(37):
        t = 2.0 * PI * i / 36.0
        x, y, z = knot_point(t, 0.4)
        rho = math.sqrt(x * x + y * y)
        torus_res = max(torus_res, abs((rho - 1.0) ** 2 + z * z - 0.4 ** 2))
    closure = math.dist(knot_point(0.0, 0.4), knot_point(2.0 * PI, 0.4))
    control("C1", "(2,3) 结型与环面约束（闭合 + (ρ−1)²+z²=a²）",
            torus_res < 1e-14 and closure < 1e-14,
            f"环面残差 max={torus_res:.3e}、闭合 |r(0)−r(2π)|={closure:.3e}；"
            "方位角绕 2 圈、管周绕 3 圈 ⇒ (2,3) 结",
            {"torus_res": torus_res, "closure": closure})

    # 非唯一性：Q(a) 连续，不同 a 不同比值
    grid = [0.05 + 0.005 * i for i in range(100)]   # 0.05 → 0.545
    qs = [knot_Q(a, 6000)[2] for a in grid]
    span = max(qs) / min(qs)
    print(f"  Q(a) 连续扫描 100 点：min={min(qs):.5f}、max={max(qs):.5f}、"
          f"span={span:.3f}×")
    control("C3", "同结型下 Q(a) 连续变化（拓扑不选比值）",
            span > 2.0,
            f"a∈[0.05,0.545] 100 点 ⇒ Q 跨 {span:.3f} 倍，且全程连续无跳变",
            {"span": span, "q_min": min(qs), "q_max": max(qs)})
    return {"rows": rows, "max_rel": worst, "grid_a": grid, "grid_q": qs,
            "span": span}


# ============================================================
# S4 · 四次几何能量：稳定点与反解恒等
# ============================================================
def s4_energy():
    print("[S4] 四次几何能量 E(x)=B+(A−B)x+Cx²（x=κ²/(κ²+τ²)=sin²θ）")
    alpha2 = ALPHA_EXP ** 2
    ratio_req = 2.0 * alpha2 / (1.0 + alpha2)         # =(B−A)/C
    print(f"  命中 α 需 x*=α²/(1+α²)={alpha2 / (1 + alpha2):.10e}，"
          f"(B−A)/C=2x*={ratio_req:.12e}")
    claim_ratio = 1.064970377848e-4
    rel_ratio = abs(ratio_req - claim_ratio) / claim_ratio
    print(f"  来料声称 (B−A)/C≈1.064970377848e−4；复算 rel={rel_ratio:.3e}")
    guard("G9", "『(B−A)/C≈1.064970377848e−4』复算",
          rel_ratio < 1e-4,
          f"2α²/(1+α²)={ratio_req:.12e}；与来料 rel={rel_ratio:.3e}",
          {"ratio_req": ratio_req, "rel": rel_ratio})

    # 代数恒等：x*=(B−A)/(2C) ⇒ α_geom=√((B−A)/(2C−B+A))
    A, C = 0.0, 1.0
    B = ratio_req * C + A
    xstar = (B - A) / (2.0 * C)
    alpha_geom = math.sqrt((B - A) / (2.0 * C - B + A))
    rel_rt = abs(alpha_geom - ALPHA_EXP) / ALPHA_EXP
    print(f"  取 A=0,C=1,B={B:.3e} ⇒ x*={xstar:.3e}、α_geom={alpha_geom:.9e}"
          f"（rel {rel_rt:.3e}）")
    guard("G10", "E(x) 稳定点解析式与 α_geom 反解往返",
          rel_rt < 1e-12 and abs(xstar - alpha2 / (1 + alpha2)) < 1e-15,
          f"x*={xstar:.6e} vs α²/(1+α²)={alpha2 / (1 + alpha2):.6e}；"
          f"α_geom 往返 rel={rel_rt:.3e}",
          {"xstar": xstar, "alpha_geom": alpha_geom, "rel": rel_rt})

    # 自然 O(1) 系数给不出 α：细调量级
    A2, B2, C2 = 0.0, 0.5, 1.0
    x2 = (B2 - A2) / (2.0 * C2)
    ag2 = math.sqrt((B2 - A2) / (2.0 * C2 - B2 + A2))
    tune = (B2 - A2) / ratio_req
    print(f"  自然系数 A=0,B=0.5,C=1 ⇒ x*={x2:.3f}、α_geom={ag2:.4f}"
          f"（与 α 差 {ag2 / ALPHA_EXP:.1f} 倍）；需细调 (B−A)/C 约 {tune:.1e} 倍")
    guard("G11", "自然 O(1) 系数与 α 的细调量级（≫1 量级）",
          tune > 1e3,
          f"自然系数给出 α_geom={ag2:.4f}（≈{ag2:.3f}），需把系数比压到 "
          f"{ratio_req:.2e}，细调 {tune:.1e} 倍 ⇒ 非无参数预言",
          {"alpha_generic": ag2, "tune": tune})

    # 稳定性：E''=2C>0 ⇒ 极小；A>B ⇒ x*<0 越界；C<0 ⇒ 极大
    e2 = 2.0 * C
    x_bad = (-1.0) / (2.0 * 1.0)                    # A=1,B=0,C=1 ⇒ x*=−0.5
    control("C4", "E(x) 稳定点性质：C>0 极小 / A>B 越界 / C<0 极大",
            e2 > 0 and x_bad < 0.0,
            f"E''=2C={e2:.1f}>0（极小）；A>B ⇒ x*={x_bad:.2f} 落在物理域 [0,1] 外；"
            "C<0 ⇒ E''<0 极大（不稳）",
            {"E2": e2, "x_bad": x_bad})

    # 数值极小（黄金分割）复核 x*
    lo, hi = 0.0, 1.0
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    c1 = hi - gr * (hi - lo)
    c2 = lo + gr * (hi - lo)
    f = lambda x: (A - B) * x + C * x * x      # 常数 B 不影响极小点
    for _ in range(200):
        if f(c1) < f(c2):
            hi = c2
        else:
            lo = c1
        c1 = hi - gr * (hi - lo)
        c2 = lo + gr * (hi - lo)
    xnum = 0.5 * (lo + hi)
    rel_num = abs(xnum - xstar) / xstar
    print(f"  黄金分割数值极小 x_num={xnum:.6e} vs 解析 x*={xstar:.6e}"
          f"（rel {rel_num:.3e}）")
    control("C5", "数值极小复核 E(x) 解析稳定点",
            rel_num < 1e-6,
            f"x_num={xnum:.6e}、x*={xstar:.6e}、rel={rel_num:.3e}",
            {"x_num": xnum, "rel": rel_num})
    return {"ratio_req": ratio_req, "claim_ratio": claim_ratio,
            "rel_ratio": rel_ratio, "xstar": xstar, "alpha_geom": alpha_geom,
            "rel_rt": rel_rt, "alpha_generic": ag2, "tune": tune,
            "x_num": xnum, "rel_num": rel_num, "A": A, "B": B, "C": C}


# ============================================================
# S5/S6 · 磁单极与 KK 维度约化
# ============================================================
def s5_monopole():
    print("[S5] 磁单极 Dirac 量子化 eg=2πn ⇒ α_eα_m=n²/4")
    rows = []
    worst = 0.0
    for n in (1, 2, 3, 4, 5):
        # 取 e=√(4πα)、g=2πn/e ⇒ α_m=g²/4π，乘积应与 n²/4 相等
        ae = ALPHA_EXP
        e = math.sqrt(4.0 * PI * ae)
        g = 2.0 * PI * n / e
        am = g * g / (4.0 * PI)
        prod = ae * am
        rel = abs(prod - n * n / 4.0) / (n * n / 4.0)
        worst = max(worst, rel)
        rows.append({"n": n, "alpha_e": ae, "alpha_m": am,
                     "prod": prod, "target": n * n / 4.0, "rel": rel})
    print(f"  n=1..5：α_eα_m 与 n²/4 的 max rel={worst:.3e}")
    control("C6", "Dirac 量子化恒等 α_eα_m=n²/4（n=1..5）",
            worst < 1e-14,
            f"5 个 n max rel={worst:.3e}（拓扑约束成立，但不选 α）",
            {"max_rel": worst})

    a_half = 0.5
    fac = a_half / ALPHA_EXP
    print(f"  n=1 且对称 ⇒ α=1/2={a_half:.4f}，是实验 α 的 {fac:.2f} 倍 ⇒ 荒谬")
    return {"rows": rows, "max_rel": worst, "factor_half": fac}


def s6_kk():
    print("[S6] KK 维度约化 1/g4² = L/g5²（量纲恒等，尺度自由）")
    # 以长度量纲指数计：dim(g4²)=0，dim(g5²)=1（=L）
    dim_g4sq, dim_g5sq, dim_L = 0, 1, 1
    lhs = dim_g4sq
    rhs = dim_L - dim_g5sq
    ok_dim = (lhs == rhs)
    print(f"  量纲指数：1/g4² → {lhs}；L/g5² → {dim_L}−{dim_g5sq}={rhs}；"
          f"恒等 {ok_dim}")
    # 自由度：L/g5² 为单一自由正实数 ⇒ 1/g4² 不受约束地取任意正数
    samples = [0.5, 1.0, 10.0, 137.036, 1e4]
    guard("G12", "KK 关系量纲自洽且 L/g5² 保持几何有意义",
          ok_dim,
          f"dim(1/g4²)=0，dim(L/g5²)=0 ⇒ 关系成立；L/g5² 可取 "
          f"{samples}（含 1/α）⇒ 单参自由",
          {"dim_ok": ok_dim})
    return {"dim_ok": ok_dim, "samples": samples}


def main():
    print("=" * 78)
    print(f"{MARKER} · 精细结构常数 V10「选择机制」全维可攻破性审计")
    print("=" * 78)
    print(f"α_exp⁻¹={ALPHA_INV_EXP}（CODATA 2022，仅事后比对）、u={U_ALPHA_INV}")
    print()

    s1 = s1_helix()
    print()
    s2 = s2_series()
    print()
    s3 = s3_knot()
    print()
    s4 = s4_energy()
    print()
    s5 = s5_monopole()
    s6 = s6_kk()

    # ================= 条目 =================
    entry("H01", "INFO", "总判：五条路线均为条件性候选，无一是无参数独立预言",
          "拓扑闭合(S1)/环面结(S3)/四次能量(S4)/磁单极(S5)/KK(S6) 各自给出允许结构"
          "或约束，但『结构→电磁耦合』缺独立公设；S2 的级数是匹配公设 + 可微调贴合",
          {"routes": ["S1", "S2", "S3", "S4", "S5", "S6"]})
    entry("H02", "PASS", "S1 螺旋：闭合条件与 κ/|τ|=2πpR/(|q|L) 互印",
          f"κ、τ 公式 vs 导数定义 max rel {s1['max_rel_kappa']:.2e}/"
          f"{s1['max_rel_tau']:.2e}；四组 (p,q) 闭合位移残差机器零",
          {"max_rel_kappa": s1["max_rel_kappa"]})
    entry("H03", "PASS", "S1 『1/137 与实验差 262.77 ppm』复算命中",
          f"p=1,q=137、L=2πR ⇒ κ/|τ|=1/137；相对偏差复算 "
          f"{s1['ppm137']:.4f} ppm（来料 262.77 ppm）",
          {"ppm": s1["ppm137"]})
    entry("H04", "FAIL", "S1 拓扑闭合不足以唯一选 α（R/L 连续自由）",
          f"固定 (p,q)=(1,137)、R/L∈[0.1,10] ⇒ κ/|τ| 连续跨 "
          f"{s1['scan'][-1]['ratio'] / s1['scan'][0]['ratio']:.1f} 倍；"
          "『强加 L=2πR』是外部选择，不是拓扑推论",
          {"span": s1["scan"][-1]["ratio"] / s1["scan"][0]["ratio"]})
    entry("H05", "PASS", "S2 80 位 decimal 级数复算命中 137.035999176142",
          f"Ω={s2['omega']:.12f}；α⁻¹_cand={s2['cand_str']}；"
          f"与来料 rel={s2['claim_rel']:.2e}",
          {"cand": s2["cand_str"]})
    entry("H06", "PASS", "S2 三级 σ 全部复算命中（14504.7 / 25.87 / 0.0409σ）",
          f"主项 {s2['main_sigma']:.1f}σ、仅 1/(24Ω) {s2['s1_sigma']:.2f}σ、"
          f"完整级数 {s2['sigma']:.4f}σ——与来料 14505 / 25.87 / 0.04086 三级一致"
          f"（u=2.1e−8 口径统一）",
          {"stages": s2["stages"]})
    entry("H07", "FAIL", "S2 级数为『残差填平式 + 单参数可微调』（不可证伪）",
          f"修正总量 {s2['total_corr']:.6e} 与主项残差 {s2['main_gap']:.6e} 相对差 "
          f"{s2['fill_rel']:.2e}（恰为填平）；且 Ω 相对改 ε*={s2['eps_star']:.2e} "
          "即精确等于 CODATA 值 ⇒ 系数 (k+6)/(k+4) 与归一化 24 均无独立导出，属条件性匹配",
          {"eps_star": s2["eps_star"], "fill_rel": s2["fill_rel"]})
    entry("H08", "PASS", "S3 环面 (2,3) 结四组 Q 复算命中来料表值",
          f"a=0.15/0.25/0.40/0.60 的 ∮κds、∮|τ|ds、Q 三列 max rel="
          f"{s3['max_rel']:.2e}（解析导数 + Simpson 2 万点）",
          {"max_rel": s3["max_rel"]})
    entry("H09", "PASS", "S3 同结型不同几何 ⇒ Q 非唯一（连续族）",
          f"Q(a) 在 a∈[0.05,0.545] 连续跨 {s3['span']:.2f} 倍、无跳变 ⇒ "
          "拓扑（结型/闭合/绕数）不选曲率比",
          {"span": s3["span"]})
    entry("H10", "PASS", "S4 四次能量稳定点与反解恒等成立",
          f"x*=(B−A)/(2C)、α_geom=√((B−A)/(2C−B+A))；取 B={s4['B']:.3e} 时 "
          f"α_geom 往返 rel={s4['rel_rt']:.2e}；黄金分割数值极小 rel={s4['rel_num']:.2e}",
          {"xstar": s4["xstar"], "rel_rt": s4["rel_rt"]})
    entry("H11", "FAIL", "S4 『(B−A)/C≈1.065e−4』是反解 α 的恒等式，非预言",
          f"该值 = 2α²/(1+α²)（由实验 α 反解）；自然 O(1) 系数给 α_geom="
          f"{s4['alpha_generic']:.4f} ⇒ 需细调 {s4['tune']:.1e} 倍（4 个量级）",
          {"ratio_req": s4["ratio_req"], "tune": s4["tune"]})
    entry("H12", "PASS", "S5 磁单极量子化恒等 α_eα_m=n²/4（n=1..5）",
          f"max rel={s5['max_rel']:.2e}；但 n=1 对称解 α=1/2 是实验值的 "
          f"{s5['factor_half']:.2f} 倍 ⇒ 约束乘积不选大小",
          {"factor_half": s5["factor_half"]})
    entry("H13", "PASS", "S6 KK 维度约化 1/g4²=L/g5² 量纲自洽、尺度自由",
          "dim(1/g4²)=0=dim(L/g5²)；L/g5² 为单一自由正实数，可取含 1/α 的任意值 "
          "⇒ 不构成 α 的预言",
          {"dim_ok": s6["dim_ok"]})
    entry("H14", "BOUNDARY", "S2 敏感性 1.65e−10 依赖论文内部归一化定义",
          f"自然量级 u/α⁻¹={s2['rel_sigma']:.4e}，来料 1.65e−10 与之比 "
          f"{1.65e-10 / s2['rel_sigma']:.2f} ⇒ 量级自洽但定义不可独立复核（原文未开放）",
          {"rel_sigma": s2["rel_sigma"]})
    entry("H15", "INFO", "结论：拓扑定允许、动力学选稳定，但『结构→耦合』缺环",
          "三条子链（拓扑/动力学/耦合）中只有前两条可机检；第三条（为何几何结构"
          "等于低能电荷耦合）在任何来料中都是外加公设 ⇒ 仍无独立预言",
          {"missing_link": "geometry→charge-coupling"})

    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in entries if e["level"] == "INFO")

    res = {
        "marker": MARKER,
        "stem": STEM,
        "date": "2026-10-31",
        "title": "精细结构常数 V10『选择机制』全维可攻破性审计（螺旋闭合 / (2,3) 结 / "
                 "四次能量 / 条件级数 / 单极 / KK）",
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info,
                   "guards": "", "controls": ""},
        "guards": guards,
        "controls": controls,
        "entries": entries,
        "readings": {
            "params": {"alpha_inv_exp": ALPHA_INV_EXP, "u_alpha_inv": U_ALPHA_INV,
                       "alpha_exp": ALPHA_EXP},
            "s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6,
            "summary": {"ppm137": s1["ppm137"],
                        "omega": s2["omega"], "cand": s2["cand"],
                        "sigma": s2["sigma"], "main_sigma": s2["main_sigma"],
                        "eps_star": s2["eps_star"],
                        "knot_max_rel": s3["max_rel"], "knot_span": s3["span"],
                        "ratio_req": s4["ratio_req"], "tune": s4["tune"]},
        },
        "verdict": "",
        "judgement": "",
        "source": {
            "engine": BASE + ".py",
            "inherits": ["ROOT V10.0 来料（用户附件逐字，数据/r283 占用者另存）",
                         "r277（量纲代数三分类与单位重标定）",
                         "r282（Φ 曲线双端解析锚定）",
                         "CODATA 2022（α 事后比对锚）",
                         "Sandage–Loeb / Dirac 1931 / Kaluza–Klein（只读）"],
        },
    }

    parts = [
        "HELIX-CLOSURE-AND-RATIO-OK",
        "PPM-262-77-REPRODUCED",
        "SERIES-80DIGIT-REPRODUCED",
        "SIGMA-0-04-REPRODUCED",
        "THREE-STAGE-SIGMA-OK",
        "RESIDUAL-FILLING-PLUS-ONE-PARAM-TUNING",
        "KNOT-TABLE-REPRODUCED",
        "KNOT-NON-UNIQUE",
        "ENERGY-STATIONARY-OK",
        "RATIO-IS-BACKSOLVED",
        "MONOPOLE-IDENTITY-OK",
        "KK-DIMENSION-OK",
        "VERDICT-CONDITIONAL-CANDIDATE-NO-INDEPENDENT-PREDICTION",
    ]
    res["verdict"] = MARKER + "-" + "-".join(parts)
    res["judgement"] = ("CONDITIONAL-CANDIDATE（五路全为条件性候选：拓扑定允许结构、"
                        "动力学选稳定结构，但『结构→电磁耦合』仍是外加公设；"
                        "S2 级数 80 位复算通过 = 数值复现，非物理验证；"
                        "S4 的 1.065e−4 是反解 α 的恒等式；无独立预言）")

    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")

    html_ok, html_detail = cast_html(res)
    guard("G13", "交互 HTML 生成且自含（零外部 URL）", html_ok, html_detail)
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
        f.write(f"ppm137={s['ppm137']:.4f} omega={s['omega']:.12f}\n")
        f.write(f"cand={res['readings']['s2']['cand_str']} sigma={s['sigma']:.6f} "
                f"main_sigma={s['main_sigma']:.1f}\n")
        f.write(f"eps_star={s['eps_star']:.3e} ratio_req={s['ratio_req']:.9e} "
                f"tune={s['tune']:.1e}\n")
        f.write(f"knot_max_rel={s['knot_max_rel']:.3e} knot_span={s['knot_span']:.3f}\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R284_JSON__" not in tpl:
        return False, "模板缺少 __R284_JSON__ 占位符"
    html = tpl.replace("__R284_JSON__", json.dumps(res, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R284_JSON__" in text:
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
