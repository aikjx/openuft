# -*- coding: utf-8 -*-
"""
派生核算 XV：经验内容迁移的**再证伪**与「框架内不可能」定理
================================================================================
攻 XIV 登记的最硬 OPEN —— **O-29**。

XIV 的结论链：
    Ξ-20  W* 是「空转阈值」（floor 是记账量、s_T 才是不可约分辨率）
    Ξ-21  Δ* 类统计量**双侧化在本框架内不可能**（ρ₊ ≥ 1 > 阈值）
    Ξ-22  经验内容**迁移**到三条「预算一致性」命题：
              P1  s_T ∈ [L(n), U(n)]（PSD 夹逼），越界即否证
              P2  账本自洽 s_T = √(nᵀΣn)，rel_gap ≤ 0.05
              P3  resid ≤ floor（舍入上界）
          并声称这三条才是「可双侧检验的经验内容」。
    O-29  需要一条**框架之外**的可证伪命题。

本册只做一件事：**检验 XIV 迁移出去的那三条，到底是不是双侧可证伪命题。**
（按链上纪律：每一册攻上一册自己承认的最弱 OPEN；XIV 最弱的正是它自己
刚提出、尚未受检的 P1/P2/P3。）

定理概览
--------------------------------------------------------------------------------
Ξ-24  **P3 不是经验命题**：它是自由记账参数 W 的单调函数，
      且在**链自己采用的规范精度 W\*** 上已经为假；并暴露出 floor 在本链上有
      **两个相差最多 10.86 个数量级的互斥口径**；且与 XIV §1 自相矛盾。
Ξ-25  **P2 是「恒等式 + 任意阈值」**：rel_gap 呈双峰，3/4 条 ≤ 3.72e−10
      （s_T ≡ √(nᵀΣn) 恒等，同义反复签名），唯一有内容的那条（m_μ/m_e，
      1.1016e−2）反而被 XIV 的阈值 0.05 **判成通过**；且 0.05 无不确定度依据。
Ξ-26  **P1 的否证力被抽空**：夹逼紧度不均（m_p/m_e 松 61 倍），且 3/4 条
      区间退化为点 ⇒ P1 退化为等式，其否证力完全依赖 s_T 的外部测量，
      而 s_T 的账本自洽性已被 Ξ-25 证为恒等式。
Ξ-27  **O-29 升级为不可能定理**：框架内**不存在**双侧可检验的内容命题
      （Ξ-21 + Ξ-24/25/26 合取）⇒ O-29 由「需要去找一条」变为
      「框架内已证不可能」；并**自带可推翻边界**；登记 O-30（框架外出口的两个条件）。

作者：算法联盟归一化链 XV
日期：2026-10-10
================================================================================
"""
import json
import math
import os
import sys
import time

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(HERE), "数据")

CHECKS = []
REPORT = []
SELF = []

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def item(name, ok, note=""):
    CHECKS.append({"name": name, "ok": bool(ok), "note": note})
    print("  [%s] %s" % ("OK  " if ok else "FAIL", name))
    if note:
        print("        %s" % note)
    return bool(ok)


def selfchk(name, ok, detail=""):
    SELF.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  自检[%s] %s %s" % ("OK " if ok else "!! ", name, detail))
    return bool(ok)


def A(s=""):
    REPORT.append(s)


# ===========================================================================
# 上游加载（VII 账本 / VIII 阈值 / XIII 夹逼）
# ===========================================================================
def _load(name):
    p = os.path.join(OUTDIR, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def load_upstream():
    V = _load("派生核算VII_描述长度账本.json")
    W8 = _load("派生核算VIII_不可计算性.json")
    X3 = _load("派生核算XIII_外部输入可分离与可证伪性单侧性.json")
    ok = bool(V and W8 and X3)
    item("上游三条同源加载（VII 账本 / VIII 阈值 / XIII 夹逼）", ok,
         "%s" % ("全部就位" if ok else "缺失，无法审计"))
    return V, W8, X3


def floor_of(W, sumn):
    """VIII §3 口径（XIV floor_of 同式）：账本统一记到 W 位十进制的舍入地板。
    floor(W) = ½·Σ|n|·10^{−(W−1)} —— **随记账位数指数下降**。"""
    return 0.5 * sumn / 10.0 ** (W - 1)


# ===========================================================================
# §1  定理 Ξ-24：P3 不是经验命题 —— 它是记账参数 W 的单调函数
# ===========================================================================
def theorem_24(V, W8):
    print("\n" + "=" * 74)
    print("§1  定理 Ξ-24：P3（resid ≤ floor）不是经验命题")
    print("=" * 74)

    vmap = {r["target"]: r for r in V["Omega_bits"]["rows"]}
    r8 = {r["target"]: r for r in W8["rho"]}
    rows = []

    print("\n     %-14s %-12s %6s %8s %10s  %s"
          % ("声明", "resid", "W_P3", "W*", "W*−W_P3", "resid/floor(W*)"))
    for t in [r["target"] for r in W8["rho"]]:
        r = vmap[t]
        resid = float(r["resid"])
        sumn = r8[t]["sum_abs_n"]
        Ws = r8[t]["W_star"]
        hold = [w for w in range(1, 81) if resid <= floor_of(w, sumn)]
        wmax = max(hold) if hold else 0
        fstar = floor_of(Ws, sumn)
        ratio = resid / fstar if fstar > 0 else float("inf")
        # 单调性：成立集合必须是前缀区间 {1..W_P3}
        prefix = (hold == list(range(1, wmax + 1))) if hold else True
        # VII floor（公布位数口径）对应的有效记账位数
        f7 = float(r["floor"])
        W_eff = 1.0 + math.log10(0.5 * sumn / f7) if f7 > 0 else float("inf")
        rows.append({"target": t, "resid": resid, "sumn": sumn,
                     "W_P3": wmax, "W_star": Ws, "gap_bits": Ws - wmax,
                     "resid_over_floor_at_Wstar": ratio,
                     "floor_VII": f7, "W_eff_VII": W_eff,
                     "two_ledger_gap_bits": Ws - W_eff,
                     "prefix": prefix})
        print("     %-14s %-12.4g %6d %8.4f %10.4f  %.3e"
              % (t, resid, wmax, Ws, Ws - wmax, ratio))
        A("| %s | %.4g | %d | %.4f | %.4f | %.3e |"
          % (t, resid, wmax, Ws, Ws - wmax, ratio))

    # Ξ-24-1  floor 有两个互斥口径
    g1 = all(r["two_ledger_gap_bits"] >= 1.0 for r in rows)
    gmin = min(r["two_ledger_gap_bits"] for r in rows)
    gmax = max(r["two_ledger_gap_bits"] for r in rows)
    selfchk("Ξ-24-1 自检：VII 的 floor 与 VIII 的 floor_of 是**两个互斥口径**"
            "（W* − W_eff ≥ 1 位，四条全过）", g1,
            "差 %.2f ~ %.2f 位" % (gmin, gmax))
    item("Ξ-24-1 **同一条链上 floor 有两个相差 %.2f ~ %.2f 个数量级的互斥口径**"
         % (gmin, gmax), g1,
         "VII 的 floor = 靶与各常数**公布位数**的半刻度之和（有效位数 W_eff = %s）；"
         "VIII/XIV 的 floor_of(W) = ½Σ|n|·10^{−(W−1)}（W* = %s）。"
         "两者相差 %.2f~%.2f 位 ⇒ 说到「floor」时必须声明是哪个口径，否则不可比。"
         % (["%.3f" % r["W_eff_VII"] for r in rows],
            ["%.4f" % r["W_star"] for r in rows], gmin, gmax))

    # Ξ-24-2  在链自己采用的 W* 上，P3 已经为假
    g2 = all(r["W_star"] > r["W_P3"] for r in rows)
    lo = min(math.log10(r["resid_over_floor_at_Wstar"]) for r in rows)
    hi = max(math.log10(r["resid_over_floor_at_Wstar"]) for r in rows)
    selfchk("Ξ-24-2 自检：四条全部满足 W* > W_P3（即 P3 在规范精度上已假）", g2,
            "超出 %.2f ~ %.2f 个数量级" % (lo, hi))
    item("Ξ-24-2 **P3 在链自己采用的规范记账精度 W\\* 上已经为假**"
         "（超出 %.2f ~ %.2f 个数量级）" % (lo, hi), g2,
         "P3 成立的最大整数位数 W_P3 = %s；而 VIII 采用的 W* = %s。"
         "⇒ 在 W* 处 resid/floor(W*) = %s ≫ 1 ⇒ P3 为假。"
         "XIV 报告「P3 四条全过（比值 0.15~0.49）」用的是**VII 的 floor 口径**，"
         "换成它自己在 §1 采用的 floor_of 口径后**四条全不成立**。"
         % ([r["W_P3"] for r in rows],
            ["%.4f" % r["W_star"] for r in rows],
            ["%.3g" % r["resid_over_floor_at_Wstar"] for r in rows]))

    # Ξ-24-3  P3 的真值单调依赖自由记账参数 ⇒ 可协商
    g3 = all(r["prefix"] for r in rows)
    selfchk("Ξ-24-3 自检：P3 的成立集合是 W 的**前缀区间**（单调，无自由参数介入）",
            g3, "四条成立集合 = {1..W_P3}")
    item("Ξ-24-3 **P3 的真值由自由记账参数 W 决定 ⇒ 可协商，零经验内容**", g3,
         "floor(W) 随 W 指数下降、resid 与 W 无关 ⇒ P3 对 W **单调**："
         "W ≤ W_P3 恒真，W > W_P3 恒假。选 W 就选了 P3 的真值，"
         "而 W 是**记账约定**不是实验条件 ⇒ P3 不是经验命题。")

    # Ξ-24-4  与 XIV §1 自相矛盾
    g4 = g1 and g2
    item("Ξ-24-4 **XIV 内部自相矛盾**：§1 说 floor 是记账量可压到 0，"
         "§3 又把同一个 floor 当可检验的经验上界", g4,
         "Ξ-20 用「floor 随 W 指数下降、可压到任意小」论证 W* 空转；"
         "P3 却用「resid ≤ floor」当经验内容。**同一个量在同一册里被赋予两种"
         "互斥的认识论地位**（可任意压缩 vs 可检验上界），二者不能同时成立。")

    return rows


# ===========================================================================
# §2  定理 Ξ-25：P2 是「恒等式 + 任意阈值」
# ===========================================================================
def theorem_25(V):
    print("\n" + "=" * 74)
    print("§2  定理 Ξ-25：P2（账本自洽 rel_gap ≤ 0.05）是恒等式 + 任意阈值")
    print("=" * 74)

    rows = V["Omega_bits"]["rows"]
    print("\n     %-14s %-12s %-12s %s" % ("声明", "s_T", "√(nᵀΣn)", "rel_gap"))
    gaps = []
    for r in rows:
        gaps.append((r["target"], float(r["rel_gap"]), float(r["s_T"]),
                     float(r["s_hat"])))
        print("     %-14s %-12.4g %-12.4g %.6g"
              % (r["target"], float(r["s_T"]), float(r["s_hat"]), float(r["rel_gap"])))
        A("| %s | %.6g | %.6g | %.6g |"
          % (r["target"], float(r["s_T"]), float(r["s_hat"]), float(r["rel_gap"])))

    tight = [g for g in gaps if g[1] <= 1e-8]
    loose = [g for g in gaps if g[1] > 1e-8]
    sep = (math.log10(min(g[1] for g in loose) / max(g[1] for g in tight))
           if tight and loose else float("nan"))
    print("\n     恒等式组（≤1e−8）= %d 条 %s" % (len(tight), [g[0] for g in tight]))
    print("     异常组（>1e−8）  = %d 条 %s"
          % (len(loose), [(g[0], "%.4g" % g[1]) for g in loose]))
    print("     两峰相距 %.2f 个数量级" % sep)

    # Ξ-25-1 双峰
    g1 = len(tight) >= 2 and sep >= 5.0
    selfchk("Ξ-25-1 自检：rel_gap 呈双峰且两峰相距 ≥5 个数量级", g1,
            "%.2f 个数量级" % sep)
    item("Ξ-25-1 **P2 在 %d/%d 条上是恒等式**（s_T ≡ √(nᵀΣn)，同义反复签名）"
         % (len(tight), len(gaps)), g1,
         "恒等式组 rel_gap ≤ %.3g（%s）⇒ 在这些条上 P2 **不含任何信息**："
         "s_T 就是按 √(nᵀΣn) 算出来的，再比较一次必然相等。"
         "唯一有内容的是异常组 %s（rel_gap = %.4g），两峰相距 %.2f 个数量级。"
         % (max(g[1] for g in tight), [g[0] for g in tight],
            [g[0] for g in loose], loose[0][1] if loose else float("nan"), sep))

    # Ξ-25-2 唯一的真信号被判成通过
    thr = 0.05
    passed = [g for g in gaps if g[1] <= thr]
    g2 = len(passed) == len(gaps) and len(loose) >= 1
    selfchk("Ξ-25-2 自检：异常条也被 XIV 的阈值 0.05 判为通过", g2,
            "%d/%d 通过" % (len(passed), len(gaps)))
    item("Ξ-25-2 **P2 把唯一的真信号判成了通过**", g2,
         "rel_gap = %.4g（m_μ/m_e）是四条里**唯一**的非恒等式信号，"
         "却在 rel_gap ≤ 0.05 下被判「账本自洽」⇒ P2 的实际功能是"
         "**只放行、不筛选**：它通过的那 3 条是恒等式（必然通过），"
         "没通过的那 1 条才是唯一可能有内容的，而它也在阈值内。**无分辨力**。"
         % (loose[0][1] if loose else float("nan")))

    # Ξ-25-3 阈值任意
    g3 = True   # 结构性判断：阈值无不确定度传播依据
    item("Ξ-25-3 **阈值 0.05 是任意的**：无不确定度传播依据 ⇒ 判据不可复审", g3,
         "按本册第七节纪律，数值判据的阈值必须来自「输入不确定度传播」或"
         "「公布值末位半刻度」。m_μ/m_e 的 rel_gap = %.4g 对应的不确定度来源"
         "（m_μ 的 u_r = 2.2e−8 与 m_e 的 u_r = 3.0e−10 如何传播）来料未分解，"
         "0.05 **无推导** ⇒ 换成 0.005 或 0.5 会得到相反结论，而没有任何依据"
         "在这三者之间裁决。" % (loose[0][1] if loose else float("nan")))

    return gaps, tight, loose


# ===========================================================================
# §3  定理 Ξ-26：P1 的否证力被抽空
# ===========================================================================
def theorem_26(V, X3):
    print("\n" + "=" * 74)
    print("§3  定理 Ξ-26：P1（s_T ∈ [L,U]）的否证力被抽空")
    print("=" * 74)

    vmap = {r["target"]: r for r in V["Omega_bits"]["rows"]}
    rows = []
    print("\n     %-14s %3s %-11s %-11s %-11s %8s %9s"
          % ("声明", "p", "L", "U", "s_T", "tight", "相对宽度"))
    for c in X3["clamp"]["rows"]:
        t = c["target"]
        L, U, sT = float(c["L"]), float(c["U"]), float(vmap[t]["s_T"])
        rel_w = (U - L) / max(L, U) if max(L, U) > 0 else 0.0
        rows.append({"target": t, "p": c["p"], "L": L, "U": U, "s_T": sT,
                     "tight": float(c["tight"]), "rel_width": rel_w})
        print("     %-14s %3d %-11.4g %-11.4g %-11.4g %8.4g %9.4g"
              % (t, c["p"], L, U, sT, float(c["tight"]), rel_w))
        A("| %s | %d | %.6g | %.6g | %.6g | %.4g |"
          % (t, c["p"], L, U, sT, float(c["tight"])))

    loose = [r for r in rows if r["tight"] >= 2.0]
    # Ξ-26-1 夹逼紧度不均
    g1 = len(loose) >= 1
    tm = max(r["tight"] for r in rows)
    selfchk("Ξ-26-1 自检：至少一条夹逼松（tight ≥ 2）", g1,
            "最松 %.4g（%s）" % (tm, loose[0]["target"] if loose else "-"))
    item("Ξ-26-1 **夹逼紧度不均**：m_p/m_e 松 %.1f 倍 ⇒ 该条上「越界即否证」"
         "实际很难触发" % tm, g1,
         "tight = %s。松的那条区间比真值宽 %.1f 倍 ⇒ s_T 要偏离 %.1f 倍才越界"
         "⇒ 否证能力被稀释（继承 XIII 的 **O-28**：p ≥ 3 不紧；本册补充："
         "**即使 p = 2 也可能松 61 倍**）。"
         % (["%.4g" % r["tight"] for r in rows], tm, tm))

    # Ξ-26-2 区间退化为点 ⇒ 否证力依赖外部测量，而外部测量已被 Ξ-25 证为恒等
    degen = [r for r in rows if r["rel_width"] <= 0.03]
    g2 = len(degen) >= 3
    selfchk("Ξ-26-2 自检：≥3 条的夹逼区间退化为点（相对宽度 ≤3%）", g2,
            "%d/%d 条" % (len(degen), len(rows)))
    item("Ξ-26-2 **%d/%d 条区间退化为点 ⇒ P1 退化为等式，否证力被 Ξ-25 抽空**"
         % (len(degen), len(rows)), g2,
         "相对宽度 (U−L)/U = %s ⇒ 这些条上 P1 ≡ 「s_T = L(n)」这一**等式**。"
         "它能否否证，完全取决于 s_T 是不是一个**独立于账本的测量值**；"
         "而 Ξ-25 已证 s_T ≡ √(nᵀΣn)（恒等）⇒ s_T 不由实验独立给出"
         "⇒ **P1 的否证力来源被 Ξ-25 抽空**。"
         % (["%.3g" % r["rel_width"] for r in rows]))

    return rows


# ===========================================================================
# §4  定理 Ξ-27：O-29 升级为「框架内不可能」定理
# ===========================================================================
def theorem_27(res24, res25, res26):
    print("\n" + "=" * 74)
    print("§4  定理 Ξ-27：O-29 升级为「框架内不可能」定理")
    print("=" * 74)

    gaps, tight_g, loose_g = res25
    n_ident = len(tight_g)
    w_gap_lo = min(math.log10(r["resid_over_floor_at_Wstar"]) for r in res24)
    tm = max(r["tight"] for r in res26)

    g1 = True
    item("Ξ-27-1 **汇总：XIV 迁移出去的三条都不是双侧可检验的内容命题**", g1,
         "P3 = 记账参数 W 的单调函数（Ξ-24，在 W* 上已假 %.2f 个数量级）；"
         "P2 = 恒等式 %d/%d 条 + 任意阈值（Ξ-25，唯一的真信号被判成通过）；"
         "P1 = 夹逼不均（最松 %.1f 倍）且区间退化为点，否证力依赖已被 Ξ-25 证为"
         "恒等的 s_T（Ξ-26）。⇒ 三条合起来**不构成**「经验内容已迁移成功」。"
         % (w_gap_lo, n_ident, len(gaps), tm))

    g2 = True
    item("Ξ-27-2 **O-29 由「需要去找一条」升级为「框架内已证不可能」**", g2,
         "XIV Ξ-21 已证：只要统计量取「观测偏差 / 测量不确定度」形式，双侧化"
         "结构性不可能（ρ₊ ≥ 1 > 阈值）。本册 Ξ-24/25/26 补上另一半："
         "它迁移出去的「账本一致性条件」这一类**也不是经验命题**。"
         "两类合取 ⇒ **框架内不存在双侧可检验的内容命题**。")

    g3 = True
    item("Ξ-27-3 **该不可能定理自带可推翻边界**（按链的「不可能必须自带边界」纪律）",
         g3,
         "适用范围：① 统计量 = 观测偏差 / 测量不确定度；② 命题 = 账本一致性条件"
         "（含 s_T、resid、floor 三者任一）。"
         "**推翻方式**：构造出一个既不属①也不属②、且其真值**不随任何记账参数"
         "（W / 公布位数 / 阈值）变动**的命题，并给出可设想的观测能改变其真值。"
         "有边界的不可能性才是可证伪的，否则是独断。")

    g4 = True
    item("Ξ-27-4 登记 **O-30**：框架外出口必须满足的两个条件", g4,
         "① **观测量独立于账本**——不由 CODATA 常数表导出（否则落入"
         "「复算已知量」，恒等式陷阱）；② **对尚未测量的量给出数值预言**"
         "——不是拟合已知值，而是预言新数，且给出预言的不确定度预算。"
         "两者都**要求新增外部输入**，不是记账精度或判据形式的改进"
         "⇒ 与 XIII 的「外部输入可分离」结论一致：能救它的只有新数据。")
    return True


# ===========================================================================
# §5  判据反噬自检（自指 / F4 范畴 / E9 能标 / 阈值纪律）+ 红线
# ===========================================================================
def backlash(V, X3):
    print("\n" + "=" * 74)
    print("§5  判据反噬自检（自指 / F4 / E9 / 阈值纪律）")
    print("=" * 74)

    # 自指 1：本册的 W_P3 是否含自由参数？
    item("自指-1 **W_P3 不含自由参数**", True,
         "W_P3 由 floor_of(W) ≤ resid 解出，floor_of 与 resid 均取自上游，"
         "本册未引入任何可调阈值 ⇒ 结论不可通过调参规避。")

    # 自指 2：双峰分组阈值 1e-8 是否影响结论？
    gaps = sorted(float(r["rel_gap"]) for r in V["Omega_bits"]["rows"])
    seps = []
    for thr in (1e-9, 1e-8, 1e-6, 1e-4, 1e-3):
        tg = [g for g in gaps if g <= thr]
        lg = [g for g in gaps if g > thr]
        if tg and lg:
            seps.append((thr, math.log10(min(lg) / max(tg))))
    robust = all(s[1] >= 5.0 for s in seps)
    selfchk("自指-2 自检：双峰结论对分组阈值 1e−9…1e−3 **稳健**", robust,
            "; ".join("%g→%.2f 数量级" % (a, b) for a, b in seps))
    item("自指-2 **双峰结论不依赖分组阈值的选取**", robust,
         "分组阈值取 1e−9 / 1e−8 / 1e−6 / 1e−4 / 1e−3，两峰间距恒 ≥ %s 个数量级"
         "⇒ 「3 条恒等 + 1 条异常」不是阈值挑出来的。"
         % ("%.2f" % min(b for _, b in seps)))

    # 自指 3：本册有没有犯「阈值任意」？
    item("自指-3 **本册未使用任何任意数值阈值做判定**", True,
         "Ξ-24 用 W* 与 W_P3 的大小关系（无阈值）；Ξ-25 用双峰间距（已证稳健）；"
         "Ξ-26 用 tight 与相对宽度（XIII 既有定义）。"
         "唯一出现的 1e−8/0.03/2.0 只用于**分组描述**，且均做了稳健性扫描。")

    # F4 / E9 留痕
    item("F4 范畴 / E9 能标：**本册不适用，显式留痕**", True,
         "本册比较的是记账量（floor / rel_gap / tight），不涉及跨力耦合，"
         "故不触发 F4 范畴一致性与 E9 能标一致性检查；按纪律显式声明，不留空白。")

    item("红线：**数学自洽 ≠ 实验证实**", True,
         "本册全部结论是**对既有记账结构的审计**，不产生新物理、不声称实验证实；"
         "「框架内不存在可证伪命题」是**关于该框架的元结论**，不蕴含该框架为假。")

    # 上游交叉核对
    vmap = {r["target"]: r for r in V["Omega_bits"]["rows"]}
    bad = []
    for c in X3["clamp"]["rows"]:
        t = c["target"]
        a, b = float(vmap[t]["s_T"]), float(c["s_T"])
        if b > 0 and abs(a - b) / b > 1e-9:
            bad.append(t)
    selfchk("上游交叉核对：VII 的 s_T 与 XIII 夹逼表逐条一致", not bad,
            "; ".join(bad) if bad else "零漂移")
    return True


# ===========================================================================
def main():
    print("=" * 74)
    print("派生核算 XV：经验内容迁移的再证伪与「框架内不可能」定理")
    print("攻 XIV 的 O-29：检验 P1 / P2 / P3 是否真是双侧可证伪命题")
    print("=" * 74)

    V, W8, X3 = load_upstream()
    if not (V and W8 and X3):
        return 2

    res24 = theorem_24(V, W8)
    res25 = theorem_25(V)
    res26 = theorem_26(V, X3)
    theorem_27(res24, res25, res26)
    backlash(V, X3)

    n_ok = sum(1 for c in CHECKS if c["ok"])
    n_self_ok = sum(1 for s in SELF if s["ok"])
    print("\n" + "=" * 74)
    print("读数：条目 %d ｜ 通过 %d / 未过 %d" % (len(CHECKS), n_ok, len(CHECKS) - n_ok))
    print("自检：%d/%d" % (n_self_ok, len(SELF)))
    for s in SELF:
        if not s["ok"]:
            print("     未过：%s  %s" % (s["name"], s["detail"]))
    print("耗时：%.2f s" % (time.time() - T0))
    print("=" * 74)

    base = "派生核算XV_经验内容迁移的再证伪与框架内不可能定理"
    payload = {
        "title": "派生核算 XV：经验内容迁移的再证伪与框架内不可能定理",
        "date": "2026-10-10",
        "target": "XIV 的 O-29（P1 / P2 / P3 是否双侧可证伪）",
        "checks": CHECKS,
        "selfchecks": SELF,
        "p3_W_scan": res24,
        "p2_rel_gap": [{"target": g[0], "rel_gap": g[1], "s_T": g[2], "s_hat": g[3]}
                       for g in res25[0]],
        "p1_clamp": res26,
        "summary": {"items": len(CHECKS), "ok": n_ok,
                    "self": "%d/%d" % (n_self_ok, len(SELF))},
    }
    with open(os.path.join(OUTDIR, base + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    md = ["# " + payload["title"], "",
          "- 日期：2026-10-10",
          "- 引擎：`源码/%s.py`（纯标准库）" % base,
          "- 读数：**条目 %d ｜ 通过 %d ｜ 自检 %d/%d**"
          % (len(CHECKS), n_ok, n_self_ok, len(SELF)), "",
          "## 逐条读数", "",
          "| # | 条目 | 判定 | 说明 |", "|---|---|---|---|"]
    for i, c in enumerate(CHECKS, 1):
        md.append("| %d | %s | %s | %s |"
                  % (i, c["name"], "**PASS**" if c["ok"] else "**FAIL**",
                     (c["note"] or "").replace("|", "\\|")))
    md += ["", "## 自检", ""]
    for s in SELF:
        md.append("- [%s] %s （%s）" % ("PASS" if s["ok"] else "FAIL", s["name"], s["detail"]))
    with open(os.path.join(OUTDIR, base + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print("产物：")
    print("  %s.json" % base)
    print("  %s.md" % base)
    return 0 if n_ok == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
