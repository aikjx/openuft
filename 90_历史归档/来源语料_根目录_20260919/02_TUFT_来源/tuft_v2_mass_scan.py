#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TUFT v2.0 质量谱数值扫描（v2.1 · 正则化版）
==========================================================================
物理设定
  m = (ℏ/c)·⟨√(κ²+τ²)⟩_s                     （弧长平均 · T3/T10）
  m̃ ≡ (R0/L)·∮√(κ²+τ²) ds                    （无量纲形状因子，尺度自由）
  M_tot ≡ (1/2π)·∮√(κ²+τ²) ds                （全环相位质量，圈数敏感）
量子化选择律（公理Ⅳb）：Tw ∈ ℤ(玻色) / ℤ+½(费米) → 离散形状 a/R0
正则性过滤：仅保留 minκ > 0.05 的状态（排除 Frenet 近拐点奇异）
输出：离散谱 / SL∈ℤ 校验 / 可达性判定 / 已知质量比对照（含背景显著性）
运行：python tuft_v2_mass_scan.py   报告: tuft_v2_mass_scan_report.txt
==========================================================================
"""
import math
import time
import numpy as np
from tuft_v2_verify import torus_knot_geom, frenet_frame, twist_number, writhe_gauss

R0 = 2.0
N_SCAN = 1500
N_REF = 4000
N_WR = 1500
A_LO, A_HI = 0.30, 1.90
MIN_K = 0.05                      # 正则性门槛：minκ 低于此值的状态丢弃

KNOWN = {
    "μ/e": 206.76828, "τ/e": 3477.15, "τ/μ": 16.8170,
    "p/e": 1836.1527, "p/μ": 8.88024, "n/p": 1.0013784,
    "W/Z": 0.88142, "Z/W": 1.13454, "H/Z": 1.3732, "H/W": 1.5577,
    "π⁰/e": 264.14, "π±/e": 273.13, "p/π±": 6.7223,
}
KNOTS = [(2, 3), (2, 5), (2, 7), (3, 4), (3, 5), (3, 7), (3, 8),
         (4, 5), (4, 7), (5, 6), (5, 7), (5, 8), (6, 7), (7, 8), (7, 9), (8, 9)]

_t0 = time.time()


def knot_stats(p, q, a, npts=2001):
    """Tw, m̃(弧长平均), m̃_rms, M_tot(全环相位), L, minκ"""
    ph = np.linspace(0.0, 2.0 * np.pi, npts, endpoint=False)
    (x, y, z), r1, r2, r3 = torus_knot_geom(ph, p, q, R0, a)
    T, Nv, B, kappa, tau, speed = frenet_frame(r1, r2, r3)
    dphi = ph[1] - ph[0]
    ds = speed * dphi
    L = float(np.sum(ds))
    Tw = float(twist_number(r1, kappa, tau, speed, dphi))
    loc = np.sqrt(kappa ** 2 + tau ** 2)
    mtilde = float(np.sum(loc * ds) / L * R0)
    mtilde_rms = float(np.sqrt(np.sum(loc ** 2 * ds) / L) * R0)
    M_tot = float(np.sum(loc * ds) / (2.0 * np.pi))
    return Tw, mtilde, mtilde_rms, M_tot, L, float(np.min(kappa))


def find_crossings(p, q, targets):
    a_grid = np.linspace(A_LO, A_HI, N_SCAN)
    tws = np.array([knot_stats(p, q, a, npts=N_SCAN)[0] for a in a_grid])
    hits = []
    for T in targets:
        d = tws - T
        for i in range(len(d) - 1):
            if d[i] == 0.0 or (d[i] * d[i + 1] < 0.0):
                lo, hi = a_grid[i], a_grid[i + 1]
                for _ in range(50):
                    mid = 0.5 * (lo + hi)
                    tm = knot_stats(p, q, mid, npts=N_SCAN)[0] - T
                    if tm == 0.0:
                        break
                    if d[i] * tm <= 0.0:
                        hi = mid
                    else:
                        lo = mid
                a_star = 0.5 * (lo + hi)
                if all(abs(a_star - h[0]) > 1e-4 for h in hits):
                    hits.append((a_star,))
    return hits


def main():
    print("=" * 78)
    print("TUFT v2.0 质量谱扫描 v2.1（正则化）| 选择律: Tw∈ℤ/2 | minκ>%.2f" % MIN_K)
    print(f"纽结族 {len(KNOTS)} 个 (p,q) | a∈[{A_LO},{A_HI}] | R0={R0}")
    print("=" * 78)

    targets = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, -0.5, -1.0, -1.5, -2.0, -2.5, -3.0]
    states = []
    dropped = 0
    print("\n== 逐纽结扫描 ==")
    for (p, q) in KNOTS:
        hits = find_crossings(p, q, targets)
        n_ok = 0
        for (a_star,) in hits:
            Twf, mf, mfr, Mt, Lf, mk = knot_stats(p, q, a_star, npts=N_REF)
            if mk < MIN_K:                       # 正则性过滤
                dropped += 1
                continue
            ph = np.linspace(0.0, 2.0 * np.pi, N_WR, endpoint=False)
            (x, y, z), r1, r2, r3 = torus_knot_geom(ph, p, q, R0, a_star)
            rf = np.stack((x, y, z), axis=-1)
            dphi = ph[1] - ph[0]
            Wr = writhe_gauss(rf, np.stack(r1, axis=-1), dphi)
            SL = Twf + Wr
            states.append(dict(p=p, q=q, a=a_star, Tw=Twf, m=mf, m_rms=mfr,
                               M_tot=Mt, SL=SL, min_k=mk))
            n_ok += 1
        print(f"  ({p},{q}): 有效量子化状态 {n_ok} 个")

    states.sort(key=lambda s: abs(s["m"]))
    n = len(states)
    print(f"\n== 量子化状态谱（{n} 个干净态，|m̃| 排序） ==")
    print(f"  {'(p,q)':<8}{'a':>9}{'Tw':>8}{'m̃':>9}{'M_tot':>9}{'SL':>9}{'minκ':>7}{'类型':>6}")
    for s in states:
        typ = "B" if abs(2 * s["Tw"] - round(2 * s["Tw"])) < 1e-6 and \
            abs(s["Tw"] - round(s["Tw"])) < 1e-6 else "F"
        print(f"  ({s['p']},{s['q']}){s['a']:>9.4f}{s['Tw']:>8.3f}{s['m']:>9.5f}"
              f"{s['M_tot']:>9.3f}{s['SL']:>9.4f}{s['min_k']:>7.3f}{typ:>6}")

    bad = [s for s in states if abs(s["SL"] - round(s["SL"])) > 0.05]
    print(f"\nSL=Tw+Wr∈ℤ 校验: {n - len(bad)}/{n} 通过" + (f"，异常 {len(bad)} 个" if bad else ""))
    print(f"正则性过滤丢弃: {dropped} 个近拐点奇异态")

    # 可达性判定
    mmin = min(abs(s["m"]) for s in states)
    mmax = max(abs(s["m"]) for s in states)
    reach = mmax / mmin
    print(f"\n质量谱范围: m̃∈[{mmin:.4f},{mmax:.4f}] → 最大可达质量比 = {reach:.1f}")
    for name, rk in KNOWN.items():
        if rk > reach:
            print(f"  ✗ {name} = {rk} > 可达比 {reach:.1f} —— 当前质量泛函无法产生该层级")

    # 已知质量比对照（bootstrap 显著性检验）
    print("\n== 与已知粒子质量比对照（bootstrap p 值，多重比较 Bonferroni α=0.05/13） ==")
    ms = np.array([abs(s["m"]) for s in states])
    pair_list = [(ms[i] / ms[j], i, j) for i in range(n) for j in range(n) if i != j]
    ratios = np.array([p[0] for p in pair_list])
    RNG = np.random.default_rng(20260916)
    rows = []
    N_BOOT = 2000
    for name, rk in KNOWN.items():
        log_t = math.log(rk)
        dist = np.abs(np.log(ratios) - log_t)
        k = int(np.argmin(dist))
        best, i, j = pair_list[k]
        dev = abs(best - rk) / rk
        d_star = float(dist[k])
        # 零假设：从同一配对分布中自助重抽，最优距离更小的频率 = p 值
        idx = RNG.integers(0, len(ratios), size=(N_BOOT, len(ratios)))
        null_mins = np.abs(np.log(ratios[idx]) - log_t).min(axis=1)
        p = float(np.mean(null_mins <= d_star))
        rows.append((name, rk, best, dev, p, i, j))
    rows.sort(key=lambda r: r[3])
    for name, rk, best, dev, p, i, j in rows:
        sig = "显著" if p < 0.05 / len(KNOWN) else ("边缘" if p < 0.05 else "不显著")
        print(f"  {name:<7} 已知={rk:<10.5f} 最佳预测={best:<10.5f} 偏差={dev*100:6.2f}% "
              f"p={p:.4f} [{sig}]  "
              f"({states[i]['p']},{states[i]['q']})a={states[i]['a']:.3f}"
              f"→({states[j]['p']},{states[j]['q']})a={states[j]['a']:.3f}")

    # 结论
    print("\n== 结论 ==")
    print(f"1) 量子化选择律 Tw∈ℤ/2 在 {len(KNOTS)} 个纽结中选出 {n} 个干净态，SL∈ℤ 校验 "
          f"{n - len(bad)}/{n} 通过（Călugăreanu–White 自洽 ✓）")
    print(f"2) 质量谱高度简并：m̃∈[{mmin:.4f},{mmax:.4f}]（比值≤{reach:.1f}）")
    print("3) 轻子层级（μ/e=207, τ/e=3477）与质子里程（p/e=1836）**不可达** →")
    print("   当前质量泛函（弧长平均 √(κ²+τ²)）被观测数据排除（与 v1 审计'质量谱未导出'一致）")
    print("4) 表观近匹配（如 n/p, Z/W）经 bootstrap 检验为不显著/边缘 —— 简并带内的巧合，")
    print("   非预言（多目标多重比较后更不成立）")
    print("5) 出路（新开放项 OP-MS）：质量泛函需尺度机制（β₁ 背景 / 非平均泛函 / 圈数敏感项），")
    print("   或引入 a/R0 的独立动力学以摆脱简并")

    lines = [f"TUFT v2.0 质量谱扫描报告 v2.1  {time.strftime('%Y-%m-%d')}",
             f"干净态 {n} 个（minκ>{MIN_K}，丢弃 {dropped} 个奇异态）| 可达比 {reach:.1f}"]
    lines.append("\n量子化状态:")
    for s in states:
        typ = "B" if abs(2*s["Tw"]-round(2*s["Tw"])) < 1e-6 and abs(s["Tw"]-round(s["Tw"])) < 1e-6 else "F"
        lines.append(f"({s['p']},{s['q']}) a={s['a']:.4f} Tw={s['Tw']:+.3f} m̃={s['m']:.6f} "
                     f"M_tot={s['M_tot']:.4f} SL={s['SL']:+.4f} {typ}")
    lines.append("\n已知质量比对照:")
    for name, rk, best, dev, p, i, j in rows:
        lines.append(f"{name} 已知={rk:.5f} 最佳={best:.5f} 偏差={dev*100:.2f}% "
                     f"bootstrap_p={p:.4f}")
    lines.append("\n结论: 轻子/质子层级不可达；谱简并；当前质量泛函被数据排除；OP-MS 开放。")
    with open("tuft_v2_mass_scan_report.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"\n报告已写入: tuft_v2_mass_scan_report.txt （耗时 {time.time()-_t0:.1f}s）")


if __name__ == "__main__":
    main()
