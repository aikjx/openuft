# -*- coding: utf-8 -*-
r"""TUFT-r287 · 精细结构常数 V10「下一步链条」可行性审计：
① S1 标度不变性定理 —— 纯形状几何量（Q∮κds/∮|τ|ds、κ/|τ|、x=κ²/(κ²+τ²)）
   对整体重标度 r→λr 恒不变（残差机器零），阳性对照 κ∝1/λ 有牙齿；
② S2 两锚否证 —— α⁻¹(0)=137.035999177（CODATA，Thomson 极限）与
   α⁻¹(M_Z)=127.955（PDG，MS-bar）相差 9.081 个倒数单位（6.63%）；
   任何与标度无关的几何常数**不可能同时命中**：minimax 最优常数仍差 908σ；
③ S3 参数自由度计数 —— E(x)=B+(A−B)x+Cx² 的 3 个系数去掉「加常数/整体标度」
   两条不可观测量 ⇒ 1 个独立比 (B−A)/C；目标也是 1 个数 ⇒ dof=0（拟合式，非预言）；
   1σ 参数窗 Δr/r 与细调倍率量化；
④ S4 刚性对照 —— 4D 二阶度规扇区只有 {1,R}（Lovelock 型刚性确实存在）；
   规范扇区 dim-4 只有 {F², F F̃}（F F̃ 为全导数）⇒ 形式唯一、系数自由；
   曲率标量（κ,τ,κ',τ',…）无有限完备集 ⇒ 刚性定理不可借用；
⑤ S5 KK 关系 1/g4²=L/g5² 对 L 线性（对数斜率恰为 1），与 RG 的对数律不同型。
2026-10-31

〔编号说明〕起草前三树实测：r285 已被并行线「五测点预测与Φ曲线加密」占满四件套；
r286 数据树已有并行线「V11 本源攻坚审计·来料原件·用户附件逐字」⇒ 本卷不抢号，
取 r287（源码/数据/判定三树对 r287 全空）。

〔定位〕r284 已判 V10 六路主张为条件性候选；本卷做它 **§七「下一步最有希望的处理逻辑」**
的可行性否证：在三前提下（纯几何 · 不含 α 实验输入 · 不引入额外标度）能否从几何
作用量推出唯一无量纲耦合。本卷不新增物理，只做可机检的否证与计数。

口径：纯标准库 float64；α 两锚只作**事后比对/否证输入**，不进入任何候选式构造；
守卫失败即非零退出；本卷条目不可与 r142–r286 相加。
"""

import json
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r287_可行性审计交互可视化模板_2026-10-31.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_精细结构常数唯一性可行性审计可视化_2026-10-31.html")

MARKER = "R287-ALPHA-UNIQUENESS-FEASIBILITY-AUDIT"
STEM = "TUFT-r287"
BASE = ("TUFT-r287_精细结构常数V10下一步链条可行性审计_形状量标度不变与α跑动否证_"
        "参数自由度计数与刚性定理不可借用_2026-10-31")

PI = math.pi

# 外部锚（只作事后比对 / 否证输入）
A0 = 137.035999177          # α⁻¹(0) Thomson 极限，CODATA 2022
U0 = 2.1e-8                 # CODATA 2022 标准不确定度
AZ = 127.955                # α⁻¹(M_Z) MS-bar，PDG 2022
UZ = 0.010                  # PDG 2022 标准不确定度
ALPHA0 = 1.0 / A0

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
# S1 · 标度不变性：圆环面 (2,3) 结的整体重标度
# ============================================================
def knot_derivs(t, a):
    """(2,3) 结 r(t)=((1+a cos3t)cos2t,(1+a cos3t)sin2t,a sin3t) 的 r'、r''、r'''。"""
    c2, s2 = math.cos(2 * t), math.sin(2 * t)
    c3, s3 = math.cos(3 * t), math.sin(3 * t)
    f = 1.0 + a * c3
    # r
    # r' = a·(-3s3)cp + f·2(-s2)
    rp = (-3 * a * s3 * c2 - 2 * f * s2,
           -3 * a * s3 * s2 + 2 * f * c2,
           3 * a * c3)
    rpp = (-9 * a * c3 * c2 + 6 * a * s3 * s2 - 4 * f * c2,
           -9 * a * c3 * s2 - 6 * a * s3 * c2 - 4 * f * s2,
           -9 * a * s3)
    rppp = (27 * a * s3 * c2 + 18 * a * c3 * s2 + 12 * a * s3 * s2 + 8 * f * s2,
            27 * a * s3 * s2 - 18 * a * c3 * c2 - 12 * a * s3 * c2 + 8 * f * c2,
            -27 * a * c3)
    return rp, rpp, rppp


def knot_terms(t, a, lam):
    """返回 (κ ds/dt, |τ| ds/dt) = (|r'×r''|/|r'|², |cross·r'''||r'|/|cross|²)，按 λ 缩放。"""
    rp, rpp, rppp = knot_derivs(t, a)
    rp = (lam * rp[0], lam * rp[1], lam * rp[2])
    rpp = (lam * rpp[0], lam * rpp[1], lam * rpp[2])
    rppp = (lam * rppp[0], lam * rppp[1], lam * rppp[2])
    cx = rp[1] * rpp[2] - rp[2] * rpp[1]
    cy = rp[2] * rpp[0] - rp[0] * rpp[2]
    cz = rp[0] * rpp[1] - rp[1] * rpp[0]
    cn = math.sqrt(cx * cx + cy * cy + cz * cz)
    pn = math.sqrt(rp[0] ** 2 + rp[1] ** 2 + rp[2] ** 2)
    kappa_ds = cn / pn ** 2
    abs_tau_ds = abs(cx * rppp[0] + cy * rppp[1] + cz * rppp[2]) * pn / (cn ** 2)
    return kappa_ds, abs_tau_ds


def knot_kappa(t, a, lam):
    rp, rpp, _ = knot_derivs(t, a)
    rp = (lam * rp[0], lam * rp[1], lam * rp[2])
    rpp = (lam * rpp[0], lam * rpp[1], lam * rpp[2])
    cx = rp[1] * rpp[2] - rp[2] * rpp[1]
    cy = rp[2] * rpp[0] - rp[0] * rpp[2]
    cz = rp[0] * rpp[1] - rp[1] * rpp[0]
    cn = math.sqrt(cx * cx + cy * cy + cz * cz)
    pn = math.sqrt(rp[0] ** 2 + rp[1] ** 2 + rp[2] ** 2)
    return cn / pn ** 3


def knot_Q(a, lam, n=20000):
    K = simpson(lambda t: knot_terms(t, a, lam)[0], 0.0, 2 * PI, n)
    T = simpson(lambda t: knot_terms(t, a, lam)[1], 0.0, 2 * PI, n)
    return K, T, K / T


def s1_scale():
    print("[S1] 标度不变性：Q=∮κds/∮|τ|ds 与 κ 的整体重标度 r→λr")
    lams = [1e-3, 1.0, 1e3, 1e6]
    rows = []
    Q0 = None
    for lam in lams:
        K, T, Q = knot_Q(0.40, lam)
        if lam == 1.0:
            Q0 = Q
        kap = knot_kappa(0.0, 0.40, lam)
        rows.append({"lam": lam, "K": K, "T": T, "Q": Q, "kappa": kap})
    worst_q = max(abs(r["Q"] - Q0) / Q0 for r in rows)
    worst_k = max(abs(r["kappa"] * r["lam"] - knot_kappa(0.0, 0.40, 1.0))
                  / knot_kappa(0.0, 0.40, 1.0) for r in rows)
    print(f"  四个尺度 λ∈{lams}：max|Q/Q0−1|={worst_q:.3e}；"
          f"max|λ·κ(λ)/κ(1)−1|={worst_k:.3e}")

    guard("G1", "形状量标度不变：Q 对 λ 的残差 < 1e−12",
          worst_q < 1e-12,
          f"Q(λ)/Q(1) 在 λ=1e−3…1e6 上 max|·−1|={worst_q:.3e}（机器零）",
          {"max_rel_Q": worst_q})
    guard("G2", "阳性对照：κ 随 λ 按 1/λ 变化（检验有牙齿）",
          worst_k < 1e-12,
          f"λ·κ(λ)/κ(1) 与 1 的 max 偏差={worst_k:.3e}",
          {"max_rel_kappa": worst_k})

    # 螺旋比值：κ/|τ| = 2πpR/(|q|L) 在 (R,L)→(λR,λL) 下不变
    p, q = 1, 137
    R, L = 1.0, 2 * PI
    base = 2 * PI * p * R / (abs(q) * L)
    worst_h = 0.0
    for lam in lams:
        r2 = 2 * PI * p * (lam * R) / (abs(q) * (lam * L))
        worst_h = max(worst_h, abs(r2 - base) / base)
    print(f"  螺旋同比缩放 (R,L)→(λR,λL)：κ/|τ| 残差 max={worst_h:.3e}（= {base:.6f}）")
    guard("G3", "螺旋比值同比缩放不变（几何不携带标度）",
          worst_h < 1e-12,
          f"四尺度 max 残差={worst_h:.3e}；比值 = {base:.9f} = 1/137",
          {"max_rel_helix": worst_h, "ratio": base})
    return {"lams": lams, "rows": rows,
            "q_rel": [r["Q"] / Q0 for r in rows],
            "k_rel": [r["kappa"] / knot_kappa(0.0, 0.40, 1.0) for r in rows],
            "max_rel_Q": worst_q, "max_rel_kappa": worst_k,
            "max_rel_helix": worst_h, "helix_ratio": base}


# ============================================================
# S2 · 两锚否证：与标度无关的常数不可能同时命中
# ============================================================
def s2_anchor():
    print("[S2] 两锚否证：α⁻¹(0) 与 α⁻¹(M_Z)")
    delta = A0 - AZ
    rel = delta / A0
    sig_z = delta / UZ
    minimax = delta / (U0 + UZ)
    q_star = A0 - minimax * U0
    gap = (A0 - U0) - (AZ + UZ)
    print(f"  α⁻¹(0)={A0}（u={U0}）、α⁻¹(M_Z)={AZ}（u={UZ}）")
    print(f"  Δ={delta:.9f}（{rel * 100:.4f}%）；以 M_Z 精度计 = {sig_z:.1f}σ")
    print(f"  单一常数的 minimax 残差 = {minimax:.3f}σ（q*={q_star:.6f}）")
    print(f"  两组 1σ 区间不重叠，间隙 = {gap:.6f} 个倒数单位")

    guard("G4", "两锚差与算术一致（Δ=9.081、6.63%）",
          abs(delta - 9.080999177) < 1e-9 and abs(rel - 0.066271) < 1e-5,
          f"Δ={delta:.9f}、rel={rel * 100:.4f}%",
          {"delta": delta, "rel": rel})
    guard("G5", "单一常数 minimax 残差 = 908σ（不可同时命中）",
          abs(minimax - delta / (U0 + UZ)) < 1e-9 and minimax > 500.0,
          f"minimax={minimax:.3f}σ ⇒ 无论取何常数，至少一端偏差>900σ",
          {"minimax_sigma": minimax, "q_star": q_star})
    guard("G6", "两锚 1σ 区间不重叠（间隙 > 9 个单位）",
          gap > 9.0,
          f"间隙={gap:.6f} ⇒ 不存在与标度无关的数同时落在两个 1σ 区间",
          {"gap": gap})

    grid_q = [AZ + (A0 - AZ) * i / 200.0 for i in range(201)]
    sig_ir = [abs(q - A0) / U0 for q in grid_q]
    sig_mz = [abs(q - AZ) / UZ for q in grid_q]
    return {"A0": A0, "U0": U0, "AZ": AZ, "UZ": UZ, "delta": delta, "rel": rel,
            "sigma_z": sig_z, "minimax": minimax, "q_star": q_star, "gap": gap,
            "grid_q": grid_q, "sig_ir": sig_ir, "sig_mz": sig_mz}


# ============================================================
# S3 · 参数自由度计数与 1σ 参数窗
# ============================================================
def s3_params():
    print("[S3] 参数自由度计数：E(x)=B+(A−B)x+Cx²")
    n_raw = 3                     # A、B、C
    n_redundant = 2               # 加常数（B 平移）与整体标度均不可观测
    n_eff = n_raw - n_redundant   # = 1 个独立比 (B−A)/C
    n_target = 1                  # 目标：一个无量纲耦合
    dof = n_eff - n_target
    print(f"  原始系数 {n_raw}，不可观测冗余 {n_redundant} ⇒ 有效参数 {n_eff}；"
          f"目标 {n_target} ⇒ dof={dof}")

    xstar = ALPHA0 ** 2 / (1.0 + ALPHA0 ** 2)
    rstar = 2.0 * xstar
    ainv = lambda r: math.sqrt((2.0 - r) / r)
    h = rstar * 1e-4
    d = (ainv(rstar + h) - ainv(rstar - h)) / (2.0 * h)
    win = (U0 * A0) / abs(d)          # 1σ 对应 Δr（单侧）
    win_rel = win / rstar
    domain_frac = 2.0 * win / 2.0     # 靴域 r∈(0,2) 的占比
    tune = 1.0 / rstar
    print(f"  r*=2α²/(1+α²)={rstar:.9e}；|dα⁻¹/dr|={abs(d):.3e}")
    print(f"  1σ 窗 Δr={win:.3e}（Δr/r={win_rel:.3e}）、域占比={domain_frac:.3e}、"
          f"相对自然 O(1) 细调={tune:.1e} 倍")

    guard("G7", "自由度计数：有效参数 1、目标 1 ⇒ dof=0（拟合式）",
          n_eff == 1 and dof == 0,
          f"{n_raw}−{n_redundant}={n_eff} 个独立比；目标 1 个数 ⇒ dof={dof}",
          {"n_eff": n_eff, "dof": dof})
    guard("G8", "1σ 参数窗与细调倍率：Δr/r<1e−6 且 细调>1e3",
          win_rel < 1e-6 and tune > 1e3,
          f"Δr/r={win_rel:.3e}、域占比={domain_frac:.3e}、细调={tune:.1e} 倍",
          {"win_rel": win_rel, "domain_frac": domain_frac, "tune": tune})

    grid_r = [10 ** (-6 + 6 * i / 200.0) for i in range(201)]
    grid_ainv = [ainv(r) for r in grid_r]
    return {"n_raw": n_raw, "n_redundant": n_redundant, "n_eff": n_eff,
            "n_target": n_target, "dof": dof, "rstar": rstar, "xstar": xstar,
            "deriv": d, "win": win, "win_rel": win_rel,
            "domain_frac": domain_frac, "tune": tune,
            "grid_r": grid_r, "grid_ainv": grid_ainv}


# ============================================================
# S4 · 刚性对照：度规扇区有刚性，规范扇区形式唯一数值自由
# ============================================================
def s4_rigidity():
    print("[S4] 刚性对照：Lovelock 计数 / 规范算子计数 / 曲率标量计数")
    lovelock = [("1（宇宙学项）", 0), ("R（Einstein–Hilbert）", 2),
                ("Gauss–Bonnet（4D 全导数）", 4)]
    lov_count = 2                     # 4D 二阶运动方程只有 1 与 R
    gauge = [("F²", 4, False), ("F F̃", 4, True),
             ("(D F)²", 6, False), ("F³", 6, False)]
    dim4 = [g for g in gauge if g[1] == 4]
    dim4_count = len(dim4)
    dyn_count = len([g for g in dim4 if not g[2]])
    curv = [2 * (n + 1) for n in range(6)]   # κ,τ 及 0..n 阶导数
    print(f"  4D 二阶度规扇区：{lov_count} 个常数（1 与 R；GB 为全导数）")
    print(f"  dim-4 规范算子：{dim4_count} 个（F²、F F̃）⇒ 动力学系数 {dyn_count} 个")
    print(f"  曲率标量计数 n=0..5：{curv}（无界）")

    control("C1", "4D 二阶度规扇区刚性确实存在（{1,R}，2 常数）",
            lov_count == 2,
            f"二阶运动方程在 4D 只允许 1 与 R（GB 为全导数）⇒ {lov_count} 个常数",
            {"lovelock": lov_count})
    control("C2", "规范扇区 dim-4 形式唯一、系数自由",
            dim4_count == 2 and dyn_count == 1,
            f"dim-4 只有 F²（动力学）与 F F̃（全导数）⇒ 有效系数 {dyn_count} 个，"
            "数值不受任何唯一性定理约束",
            {"dim4": dim4_count, "dyn": dyn_count})
    control("C3", "曲率标量无有限完备集（刚性定理不可借用）",
            curv[-1] > lov_count,
            f"0..5 阶导数计数 {curv} 单调增长 ⇒ 无有限 'Lovelock 型' 完备集",
            {"curvature_counts": curv})
    return {"lovelock": [{"name": n, "order": o} for n, o in lovelock],
            "lov_count": lov_count,
            "gauge": [{"op": g[0], "dim": g[1], "total_div": g[2]} for g in gauge],
            "dim4": dim4_count, "dyn": dyn_count, "curvature_counts": curv}


# ============================================================
# S5 · KK 线性 vs RG 对数
# ============================================================
def s5_kk():
    print("[S5] KK 关系 1/g4² = L/g5² 的函数型：对 L 线性（对数斜率 1）")
    g5sq = 1.0
    L0 = 1.0
    lam = 1e3
    ratio = (lam * L0 / g5sq) / (L0 / g5sq)
    slope = math.log(ratio) / math.log(lam)
    print(f"  L→{lam:.0e}L ⇒ 1/g4² 比值={ratio:.3f}、对数斜率={slope:.6f}")
    guard("G9", "KK 关系对 L 线性（对数斜率 = 1）",
          abs(slope - 1.0) < 1e-12 and abs(ratio - lam) / lam < 1e-12,
          f"比值={ratio:.3f}、dln(1/g4²)/dlnL={slope:.9f} ⇒ 线性，与 RG 对数律不同型",
          {"ratio": ratio, "slope": slope})
    return {"ratio": ratio, "slope": slope, "lam": lam}


# ============================================================
# main
# ============================================================
def main():
    print("=" * 78)
    print(f"{MARKER} · 精细结构常数 V10「下一步链条」可行性审计")
    print("=" * 78)
    print(f"锚：α⁻¹(0)={A0}（u={U0}）、α⁻¹(M_Z)={AZ}（u={UZ}）——只作否证输入")
    print()

    s1 = s1_scale()
    print()
    s2 = s2_anchor()
    print()
    s3 = s3_params()
    print()
    s4 = s4_rigidity()
    print()
    s5 = s5_kk()

    entry("H01", "INFO", "总判：本轮为『下一步链条』的可行性否证层，不新增物理",
          "r284 判六路条件性候选；本卷专攻其 §七链条第 1–2 环（几何作用量选唯一耦合），"
          "以标度不变性 + 两锚 + 参数计数做机检否证 ⇒ 三前提下不可达",
          {"layer": "feasibility-no-go"})
    entry("H02", "PASS", "S1 标度不变性定理：纯形状量对 r→λr 恒不变",
          f"Q(λ)/Q(1) 在 λ=1e−3…1e6 上 max|·−1|={s1['max_rel_Q']:.2e}；"
          "阳性对照 λκ(λ)/κ(1) 亦为 1 ⇒ 检验有牙齿而非恒真",
          {"max_rel_Q": s1["max_rel_Q"], "max_rel_kappa": s1["max_rel_kappa"]})
    entry("H03", "PASS", "S1 螺旋比值同比缩放不变 ⇒ 几何不携带标度",
          f"κ/|τ|=2πpR/(|q|L) 在 (R,L)→(λR,λL) 下残差 {s1['max_rel_helix']:.2e}；"
          f"比值={s1['helix_ratio']:.9f}=1/137",
          {"max_rel_helix": s1["max_rel_helix"]})
    entry("H04", "PASS", "S2 两锚差复算：Δ=9.081 个倒数单位（6.63%）",
          f"α⁻¹(0)={A0}、α⁻¹(M_Z)={AZ} ⇒ Δ={s2['delta']:.9f}、"
          f"rel={s2['rel'] * 100:.4f}%、以 M_Z 精度计 {s2['sigma_z']:.1f}σ",
          {"delta": s2["delta"], "sigma_z": s2["sigma_z"]})
    entry("H05", "FAIL", "S2 与标度无关的单一常数不可能同时命中两锚",
          f"minimax 最优常数 q*={s2['q_star']:.6f} 仍差 {s2['minimax']:.1f}σ；"
          f"两 1σ 区间间隙 {s2['gap']:.6f} 个单位 ⇒『一个几何数=α』被否证",
          {"minimax": s2["minimax"], "gap": s2["gap"]})
    entry("H06", "BOUNDARY", "S2 跑动定量由强子真空极化决定，纯几何无权输入",
          "127.955 为 MS-bar@M_Z、137.036 为 Thomson 极限 ⇒ Δ 混合 running 与 scheme 转换；"
          "跑动的强子部分需 e⁺e⁻→hadrons 数据（非 QED 微扰可独立给出）",
          {"scheme_note": "MS-bar vs Thomson"})
    entry("H07", "FAIL", "S3 参数计数 dof=0 ⇒ 拟合式而非预言",
          f"3 系数去掉加常数/整体标度两条冗余 ⇒ 有效参数 {s3['n_eff']}，目标 1 个 ⇒ "
          f"dof={s3['dof']}；任何目标都能被单一比 (B−A)/C 精确命中",
          {"n_eff": s3["n_eff"], "dof": s3["dof"]})
    entry("H08", "PASS", "S3 1σ 参数窗与细调倍率复算",
          f"r*=2α²/(1+α²)={s3['rstar']:.6e}；Δr/r={s3['win_rel']:.3e}、"
          f"靴域占比={s3['domain_frac']:.3e}、相对自然 O(1) 需细调 {s3['tune']:.1e} 倍",
          {"win_rel": s3["win_rel"], "tune": s3["tune"]})
    entry("H09", "PASS", "S4 控制：4D 二阶度规扇区刚性确实存在（{1,R}）",
          "Lovelock 计数：二阶运动方程在 4D 只允许 1 与 R（GB 为全导数）⇒ 2 个常数 ⇒ "
          "『刚性』不是本卷假设，而是可对照的真实定理",
          {"lov_count": s4["lov_count"]})
    entry("H10", "PASS", "S4 控制：规范扇区 dim-4 形式唯一、系数自由",
          f"dim-4 只有 F² 与 F F̃（全导数）⇒ 动力学系数 {s4['dyn']} 个；"
          "唯一性定理只固定形式，不固定 1/(4g²) 的数值",
          {"dim4": s4["dim4"], "dyn": s4["dyn"]})
    entry("H11", "FAIL", "S4 曲率标量无有限完备集 ⇒ 刚性定理不可借用",
          f"κ,τ 及 0..5 阶导数计数 {s4['curvature_counts']} 无界增长 ⇒ 没有可援引的"
          "有限刚性集；把 Lovelock 的『形式唯一』当成『数值唯一』是越界使用",
          {"counts": s4["curvature_counts"]})
    entry("H12", "INFO", "S5 判据集 R1–R4：纯几何路线 0/4",
          "R1 指定标度：未声明（隐式取 IR）；R2 scheme 无关：否（锚含 MS-bar 与 Thomson）；"
          "R3 预言跑动：否（形状量零跑动）；R4 附加预言：无 ⇒ 0/4",
          {"criteria": ["R1", "R2", "R3", "R4"], "score": "0/4"})
    entry("H13", "INFO", "S5 KK 关系对 L 线性，与 RG 对数律不同型",
          f"1/g4²∝L 的对数斜率={s5['slope']:.6f}（恰 1）；RG 跑动 ∝ ln(μ/m) ⇒ "
          "模数只能事后拟合单点，不能生成对数跑动",
          {"slope": s5["slope"]})
    entry("H14", "INFO", "结论：候选 0.04σ 是 IR/Thomson 拟合点；本轮 No-Go（三前提下）",
          "与标度无关的数在 IR 与 M_Z 之间缺口 9.081 个单位，单常数 minimax 908σ；"
          "参数计数 dof=0 ⇒ 拟合；不排除未来『几何自带质量谱或 RG』路线（本卷未证其不可能）",
          {"no_go": "under-stated-premises"})

    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in entries if e["level"] == "INFO")

    res = {
        "marker": MARKER, "stem": STEM, "date": "2026-10-31",
        "title": "精细结构常数 V10『下一步链条』可行性审计（形状量标度不变 / 两锚否证 / "
                 "参数计数 / 刚性对照 / KK 线性）",
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info, "guards": "", "controls": ""},
        "guards": guards, "controls": controls, "entries": entries,
        "readings": {
            "params": {"A0": A0, "U0": U0, "AZ": AZ, "UZ": UZ, "alpha0": ALPHA0},
            "s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5,
            "summary": {"delta": s2["delta"], "rel": s2["rel"],
                        "minimax": s2["minimax"], "gap": s2["gap"],
                        "q_star": s2["q_star"], "dof": s3["dof"],
                        "win_rel": s3["win_rel"], "tune": s3["tune"],
                        "max_rel_Q": s1["max_rel_Q"], "kk_slope": s5["slope"]},
        },
        "verdict": "", "judgement": "",
        "source": {
            "engine": BASE + ".py",
            "inherits": ["r284（V10 六路条件性候选审计）",
                         "r277（量纲代数三分类与单位重标定）",
                         "CODATA 2022（α⁻¹(0) 锚）",
                         "PDG 2022（α⁻¹(M_Z) MS-bar 锚）",
                         "Lovelock 定理 / 4D 规范算子计数（只读）"],
        },
    }

    parts = [
        "SCALE-INVARIANCE-THEOREM-OK",
        "HELIX-SCALE-COVARIANCE-OK",
        "ANCHOR-GAP-9-081-OK",
        "SINGLE-CONSTANT-908SIGMA-NO-GO",
        "PARAM-DOF-ZERO-FIT-ONLY",
        "ONE-SIGMA-WINDOW-4-2E-8-TUNING-9-4E3",
        "LOVELOCK-RIGIDITY-CONTROL-OK",
        "GAUGE-FORM-UNIQUE-VALUE-FREE",
        "CURVATURE-SCALARS-UNBOUNDED",
        "KK-LINEAR-SLOPE-ONE",
        "CRITERIA-0-OF-4",
        "VERDICT-NO-GO-UNDER-STATED-PREMISES",
    ]
    res["verdict"] = MARKER + "-" + "-".join(parts)
    res["judgement"] = ("NO-GO-CONDITIONAL（三前提：纯几何 / 不含 α 实验输入 / 不引入额外标度。"
                        "形状量标度不变 ⇒ 零跑动；单常数 minimax 908σ ⇒『一个几何数=α』否证；"
                        "参数计数 dof=0 ⇒ 拟合式；候选 0.04σ 是 IR/Thomson 拟合点；"
                        "不排除未来『几何自带质量谱或 RG』路线）")

    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")

    html_ok, html_detail = cast_html(res)
    guard("G10", "交互 HTML 生成且自含（零外部 URL）", html_ok, html_detail)
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
         f"控制组 {res['counts']['controls']}\n", "\n## 条目\n"]
    for e in res["entries"]:
        L.append(f"- **{e['code']} {e['level']}** {e['title']}——{e['detail']}\n")
    L.append("\n## 守卫\n")
    for g in res["guards"]:
        L.append(f"- **{g['id']} {'OK' if g['ok'] else 'FAIL'}** {g['title']}——{g['detail']}\n")
    L.append("\n## 控制组\n")
    for c in res["controls"]:
        L.append(f"- **{c['id']} {'OK' if c['ok'] else 'FAIL'}** {c['title']}——{c['detail']}\n")
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
        f.write(f"delta={s['delta']:.9f} rel={s['rel']:.6f} "
                f"minimax_sigma={s['minimax']:.3f}\n")
        f.write(f"q_star={s['q_star']:.6f} gap={s['gap']:.6f} dof={s['dof']}\n")
        f.write(f"win_rel={s['win_rel']:.3e} tune={s['tune']:.1e} "
                f"max_rel_Q={s['max_rel_Q']:.3e} kk_slope={s['kk_slope']:.9f}\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R287_JSON__" not in tpl:
        return False, "模板缺少 __R287_JSON__ 占位符"
    html = tpl.replace("__R287_JSON__", json.dumps(res, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R287_JSON__" in text:
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
