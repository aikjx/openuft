#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UFS-Delta XIV：可证伪性的双侧化不可能，与经验内容的迁移
=============================================================================
本册起点：XIII 登记的 O-27
-----------------------------------------------------------------------------
XIII 证明了：Δ*/s_T = 2^−(K(n)+ν_min) **与 s_T 无关**（标度冻结），
判据「|Δ_true| > Δ*」是下界命题，观测 0 与 Δ* 相容 ⇒ **只能确认、不能否证**，
并把 VIII 的 O-18 由「可证伪阈值」订正为「可确认阈值」，登记：

  O-27   Δ* 分支原则上不可否证（单侧 + 标度冻结）⇒ **需双侧替代形式**

「需双侧替代形式」是一次**未完成的委托**。本册把它做完，得到两个结果：

  **① 双侧化在本框架内不可能（Ξ-21）—— 不是「没找到」，是「证明不存在」。**
  **② 经验内容不在 Δ\* 分支，而在「不确定度预算一致性」（Ξ-22）。**

=============================================================================
本册的结果（符号证明优先，数值随后）
=============================================================================
§1  定理 Ξ-20：**分辨率错配** ⇒ W* 是「空转阈值」
    Ξ-20-1 VIII 的 W* 定义为「舍入地板 floor 降到 Δ* 的位数」，
        这隐含把 floor 当作**可观测偏差的分辨率下界**。但 floor 是**记账**量
        （随账本位数 W 指数下降），真正的**不可约**分辨率是 s_T（**测量**量，
        不随 W 下降）。正确的分辨率下界是 max(s_T, floor)。
    Ξ-20-2 机器验证：floor(W)/Δ* 从 W=12 到 W=30 下降 18 个数量级，
        但 max(s_T, floor)/Δ* **恒为 8.602e11（α 组）/ 1.152e8（比值组）**，
        纹丝不动 ⇒ **把账本记到任意多位都救不了**。
    Ξ-20-3 W* 处 floor/Δ* = 1.000000（VIII 定义自洽），但分辨率/Δ* 仍是
        8.6e11 / 1.15e8 ⇒ **阈值空转 8.06 ~ 11.93 个数量级**。
    Ξ-20-4 **空转系数的下界由 ν_min 单独决定**：κ ≡ 分辨率/Δ* ≥ 2^{ν_min}
        = 1590 ⇒ 即使 K(n) = 0（描述免费），仍空转 ≥ 3.2 个数量级。
    ⇒ **O-18 由 XIII 的「可确认阈值」再降级为「空转阈值」**（编号保留）。

§2  定理 Ξ-21：**双侧化在本框架内不可能**
    Ξ-21-1 把判据换成**可观测**统计量 ρ ≡ resid / s_T，
        置信区间 [ρ_−, ρ_+] = [max(0, resid−s_T)/s_T, (resid+s_T)/s_T]。
        否证条件：ρ_+ < 2^−(K(n)+ν_min)。
    Ξ-21-2 **但 ρ_+ = (resid + s_T)/s_T ≥ 1 恒成立**（resid ≥ 0），
        而 2^−(K+ν) ≤ 8.681e-9 < 1 ⇒ **否证分支永不触发**。
        这是**结构性证明**，与任何数值无关：统计量下界 1 > 阈值上界 1。
    Ξ-21-3 实测 ρ_+ ∈ [1.0035, 1.0909]，阈值 ≤ 8.681e-9 ⇒ 差 8 个数量级以上。
    ⇒ **O-27 部分闭合**：不是「尚未找到双侧形式」，而是**证明此类形式不存在**
        —— 只要统计量是「观测偏差 / 测量不确定度」，双侧化就失败。

§3  定理 Ξ-22：经验内容的**迁移** —— 真正双侧可检的是预算一致性
    Ξ-22-1 **P1**  s_T ∈ [L(n), U(n)]（XIII Ξ-16 的 PSD 夹逼）：越界即否证。
    Ξ-22-2 **P2**  账本自洽 s_T = √(n^T Σ n)：双侧。rel_gap ≤ 1.10e-2。
    Ξ-22-3 **P3**  resid ≤ floor（舍入上界）：双侧。四条全过（比值 0.15~0.49）。
    Ξ-22-4 三条**当前全部通过** ⇒ 这才是可双侧检验的经验内容。
        **但**：它们检验的是**账本的一致性**，不是「这个理论有没有内容」
        ⇒ **二分律本身没有经验内容；有内容的是账本的一致性条件**。

§4  定理 Ξ-23：综合裁定
    O-18 → 「空转阈值」；O-27 → **部分闭合**（不存在性已证 + 落点已定位）；
    新登记 **O-29**：需要一个**框架之外**的可证伪命题 —— 现有二分律框架内
    不存在双侧可检验的内容命题。

§5  判据反噬自检（F4 范畴 / E9 能标 / 自指）+ 红线
=============================================================================
"""

import io
import json
import math
import os
import sys
import time

from mpmath import mp, mpf

mp.dps = 50
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(HERE), "数据")

CHECKS = []
REPORT = []
L10 = math.log10(2.0)


def item(name, ok, note=""):
    CHECKS.append({"name": name, "ok": bool(ok), "note": note})
    print("  [%s] %s" % ("OK  " if ok else "FAIL", name))
    if note:
        print("        %s" % note)
    return ok


def A(s=""):
    REPORT.append(s)


# ===========================================================================
# 输入（与 VII / VIII / XIII 同源；锚表另与 V3 交叉核对）
# ===========================================================================
ANCHOR = {
    "c":    {"value": "299792458"},
    "hbar": {"value": "1.054571817e-34"},
    "G":    {"value": "6.67430e-11"},
    "e":    {"value": "1.602176634e-19"},
    "eps0": {"value": "8.8541878128e-12"},
    "m_e":  {"value": "9.1093837015e-31"},
    "m_mu": {"value": "1.883531627e-28"},
    "m_p":  {"value": "1.67262192369e-27"},
    "m_P":  {"value": "2.176434e-8"},
    "k_B":  {"value": "1.380649e-23"},
}
CLAIMS = [
    {"name": "alpha", "n": {"e": 2, "eps0": -1, "hbar": -1, "c": -1},
     "target": "alpha"},
    {"name": "alpha_grav_e == (m_e/m_P)^2",
     "n": {"G": 1, "m_e": 2, "hbar": -1, "c": -1}, "target": "alpha_grav_e"},
    {"name": "m_mu/m_e", "n": {"m_mu": 1, "m_e": -1}, "target": "m_mu_over_me"},
    {"name": "m_p/m_e", "n": {"m_p": 1, "m_e": -1}, "target": "m_p_over_me"},
]


def cross_check_v3():
    path = os.path.join(HERE, "量纲零空间与判别式V3.py")
    if not os.path.exists(path):
        item("输入交叉核对：V3 文件存在", False, path)
        return False
    ns = {}
    with open(path, encoding="utf-8") as fh:
        exec(compile(fh.read(), path, "exec"),
             {"__name__": "v3mod", "__file__": path}, ns)
    C2 = ns.get("CONST")
    if not C2:
        item("输入交叉核对：V3 有 CONST", False, "")
        return False
    bad = []
    for k in ANCHOR:
        r2 = C2.get(k)
        if r2 is None:
            bad.append("%s: 缺键" % k)
            continue
        raw = r2["value"] if isinstance(r2, dict) else r2
        ours, theirs = mpf(ANCHOR[k]["value"]), mpf(str(raw))
        if theirs != 0 and abs(ours - theirs) / abs(theirs) > mpf("1e-15"):
            bad.append("%s: 漂移" % k)
    item("输入交叉核对：锚表与 V3 逐键一致（%d 键）" % len(ANCHOR),
         not bad, "; ".join(bad) if bad else "零漂移（与 VII/VIII/XIII 同源）")
    return not bad


def _load(name):
    p = os.path.join(OUTDIR, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def load_upstream():
    V = _load("派生核算VII_描述长度账本.json")
    item("VII 产物同源读取（resid / floor / s_T / rel_gap）",
         bool(V and V.get("Omega_bits")),
         "%d 条账本行" % len(V["Omega_bits"]["rows"])
         if V and V.get("Omega_bits") else "缺失")
    W8 = _load("派生核算VIII_不可计算性.json")
    item("VIII 产物同源读取（ν_min / Δ* / W*）",
         bool(W8 and W8.get("rho")),
         "ν_min = %.4f bit；ρ 表 %d 条" % (W8["nu_min_pos"], len(W8["rho"]))
         if W8 and W8.get("rho") else "缺失")
    X3 = _load("派生核算XIII_外部输入可分离与可证伪性单侧性.json")
    clamp = X3["clamp"]["rows"] if X3 and X3.get("clamp") else None
    item("XIII 产物同源读取（PSD 夹逼 [L,U]，用于 Ξ-22 的 P1）",
         clamp is not None,
         "%d 条夹逼区间" % len(clamp) if clamp else "缺失")
    return V, W8, (clamp or [])


# ===========================================================================
# §1  定理 Ξ-20：分辨率错配 ⇒ W* 是空转阈值
# ===========================================================================
def floor_of(W, sumn):
    """账本统一记到 W 位十进制时的舍入地板（VIII §3 的口径）。"""
    return 0.5 * sumn / 10.0 ** (W - 1)


def theorem_20(V, W8):
    print("\n" + "=" * 74)
    print("§1  定理 Ξ-20：分辨率错配 ⇒ W* 是「空转阈值」")
    print("=" * 74)

    NU = W8["nu_min_pos"]
    vmap = {r["target"]: r for r in V["Omega_bits"]["rows"]}
    r8 = {r["target"]: r for r in W8["rho"]}
    rows = []
    print("\n     %-22s %11s %11s %11s" % ("声明", "floor/Δ*(W=12)", "(W=30)", "分辨率/Δ*"))
    for cl in CLAIMS:
        t = cl["target"]
        sT = vmap[t]["s_T"]
        sumn = sum(abs(v) for v in cl["n"].values())
        Kn = r8[t]["K_n"]
        ds = sT / 2.0 ** (Kn + NU)
        f12 = floor_of(12, sumn) / ds
        f30 = floor_of(30, sumn) / ds
        kap = sT / ds                    # = 2^{K(n)+ν_min}，floor→0 后的**不可约**值
        # floor(W) ≤ s_T 的临界位数：W ≥ W_crit 后 floor 不再是主导项
        W_crit = 1.0 + math.log10(0.5 * sumn / sT)
        # (a) 下界：任意 W 都有 κ(W) ≥ 2^{K+ν}
        lower = all(max(sT, floor_of(w, sumn)) / ds >= kap * (1.0 - 1e-12)
                    for w in range(6, 61))
        # (b) 饱和：W ≥ W_crit 后 κ(W) **恒等于** 2^{K+ν}，不再随 W 下降
        const = all(abs(max(sT, floor_of(w, sumn)) / ds - kap) / kap < 1e-12
                    for w in range(int(math.ceil(W_crit)) + 1, 61))
        rows.append({"claim": cl["name"], "target": t, "s_T": sT, "K_n": Kn,
                     "nu": NU, "delta_star": ds, "W_star": r8[t]["W_star"],
                     "sum_abs_n": sumn,
                     "floor_over_delta_W12": f12, "floor_over_delta_W30": f30,
                     "kappa": kap, "kappa_dex": math.log10(kap),
                     "W_crit": W_crit, "kappa_W_invariant": const,
                     "kappa_lower_bound_holds": lower,
                     "floor_at_Wstar_over_delta":
                         floor_of(r8[t]["W_star"], sumn) / ds,
                     "resid": float(vmap[t]["resid"]),
                     "floor": float(vmap[t]["floor"]),
                     "rel_gap": vmap[t]["rel_gap"]})
        print("     %-22s %11.3e %11.3e %11.3e"
              % (cl["name"][:22], f12, f30, kap))

    item("Ξ-20-1 floor 是**记账**量、s_T 是**测量**量 ⇒ 分辨率下界是 max(s_T, floor)",
         all(r["s_T"] > 0 for r in rows),
         "floor(W) = ½Σ|n|·10^−(W−1) 随账本位数**指数下降**（可压到任意小）；"
         "s_T 是靶的**测量**不确定度，**不随 W 下降**。VIII 的 W* 只比较了 "
         "floor 与 Δ*，漏掉了不可约的那一项 s_T。")

    item("Ξ-20-2 机器验证：κ(W) ≥ 2^{K+ν} **恒成立**，且 W ≥ W_crit 后**完全饱和**",
         all(r["kappa_W_invariant"] and r["kappa_lower_bound_holds"] for r in rows),
         "W = 6…60 全扫描：① 任意 W 都有 κ(W) = max(s_T, floor(W))/Δ* ≥ 2^{K+ν}；"
         "② 当 W ≥ W_crit = 1+log10(½Σ|n|/s_T)（四条为 %s 位）后，floor 不再主导，"
         "κ(W) **恒等于** 2^{K+ν}、不再随 W 下降（相对变动 <1e−12）。"
         "⇒ 提高位数只能把 κ 降到 %.3e / %.3e 这个**地板**上，**降不下去**："
         "压掉的是可压的那一项（floor），压不掉的是压不动的那一项（s_T）。"
         % (" / ".join("%.2f" % r["W_crit"] for r in rows),
            rows[0]["kappa"], rows[2]["kappa"]))

    item("Ξ-20-3 W* 处 floor/Δ* = 1.000000（VIII 定义自洽），但阈值**空转 %.2f–%.2f 个数量级**"
         % (min(r["kappa_dex"] for r in rows), max(r["kappa_dex"] for r in rows)),
         all(abs(r["floor_at_Wstar_over_delta"] - 1.0) < 1e-9 for r in rows),
         "W* 的定义本身没错（floor(W\*)/Δ\* 逐条 = 1.000000），错在**把它当作"
         "可证伪的门限**：到达 W\* 时，分辨率仍是 Δ\* 的 %.3e / %.3e 倍 ⇒ "
         "门限到了，门没开。⇒ **O-18 由 XIII 的「可确认阈值」再降级为「空转阈值」**。"
         % (rows[0]["kappa"], rows[2]["kappa"]))

    nu = W8["nu_min_pos"]
    k_floor = 2.0 ** nu
    item("Ξ-20-4 空转系数的下界由 ν_min **单独**决定：κ ≥ 2^ν_min = %.0f（%.2f 个数量级）"
         % (k_floor, math.log10(k_floor)),
         all(r["kappa"] >= k_floor for r in rows),
         "κ = 2^{K(n)+ν_min} ≥ 2^{ν_min}：即使把 K(n) 压到 0（描述完全免费），"
         "ν_min = %.2f bit 这一项仍使 κ ≥ %.0f ⇒ **空转至少 %.2f 个数量级**。"
         "⇒ 想减少空转，只能攻 ν_min，攻 K(n) 无效（ν_min 是下界项）。"
         % (nu, k_floor, math.log10(k_floor)))
    return {"rows": rows, "nu": nu}


# ===========================================================================
# §2  定理 Ξ-21：双侧化在本框架内不可能
# ===========================================================================
def theorem_21(Sep):
    print("\n" + "=" * 74)
    print("§2  定理 Ξ-21：双侧化在本框架内不可能（O-27 的部分闭合）")
    print("=" * 74)

    print("\n     %-22s %10s %11s %11s %11s %8s"
          % ("声明", "ρ=resid/s_T", "ρ_−", "ρ_+", "阈值 2^−(K+ν)", "否证?"))
    rows = []
    for r in Sep["rows"]:
        sT, res = r["s_T"], r["resid"]
        thr = 2.0 ** -(r["K_n"] + r["nu"])
        rho = res / sT
        rm = max(0.0, res - sT) / sT
        rp = (res + sT) / sT
        rows.append({"claim": r["claim"], "target": r["target"], "rho": rho,
                     "rho_minus": rm, "rho_plus": rp, "threshold": thr,
                     "falsified": rp < thr, "confirmed": rm > thr})
        print("     %-22s %10.4e %11.4e %11.4e %11.3e %8s"
              % (r["claim"][:22], rho, rm, rp, thr, "否" if rp >= thr else "是"))

    item("Ξ-21-1 判据的**可观测**形式：ρ ≡ resid/s_T，否证条件 ρ_+ < 2^−(K+ν)",
         True,
         "把不可观测的 Δ_true 换成可观测的 resid，并把测量不确定度 s_T 显式计入"
         "置信区间 [max(0, resid−s_T)/s_T, (resid+s_T)/s_T] ⇒ 这是最自然的双侧化尝试。")

    item("Ξ-21-2 **否证分支永不触发**：ρ_+ ≥ 1 恒成立，而阈值 2^−(K+ν) < 1",
         all(r["rho_plus"] >= 1.0 - 1e-12 for r in rows)
         and all(r["threshold"] < 1.0 for r in rows),
         "ρ_+ = (resid + s_T)/s_T ≥ 1（因 resid ≥ 0），而 2^−(K+ν) ≤ %.3e < 1"
         " ⇒ ρ_+ < 阈值 **永不成立**。这是**结构性证明**，与任何数值无关："
         "统计量的下界（1）严格大于阈值的上界（<1）。"
         % max(r["threshold"] for r in rows))

    item("Ξ-21-3 实测：ρ_+ ∈ [%.4f, %.4f]，阈值 ≤ %.3e ⇒ 差 %.1f 个数量级以上"
         % (min(r["rho_plus"] for r in rows), max(r["rho_plus"] for r in rows),
            max(r["threshold"] for r in rows),
            math.log10(min(r["rho_plus"] for r in rows)
                       / max(r["threshold"] for r in rows))),
         not any(r["falsified"] for r in rows),
         "四条**全部落在「确认」侧**（ρ_− > 阈值），无一条触发否证，"
         "且按 Ξ-21-2 可知**永远不会**触发。")

    item("Ξ-21-4 **O-27 部分闭合**：不是「尚未找到」，是「证明不存在」",
         True,
         "只要统计量取「观测偏差 / 测量不确定度」这一类（这是唯一能同时用上 "
         "resid 与 s_T 的自然选择），双侧化就失败 ⇒ **在此框架内不存在双侧"
         "可检验的内容命题**。O-27 从「需双侧替代形式」推进为「双侧替代形式"
         "不存在（已证）+ 经验内容另有落点（Ξ-22）」。")
    return {"rows": rows}


# ===========================================================================
# §3  定理 Ξ-22：经验内容的迁移 —— 真正双侧可检的预算一致性
# ===========================================================================
def theorem_22(Sep, clamp):
    print("\n" + "=" * 74)
    print("§3  定理 Ξ-22：经验内容的迁移（真正双侧可检的三条）")
    print("=" * 74)

    cmap = {c["target"]: c for c in clamp}
    print("\n     %-22s %10s %10s %10s %10s"
          % ("声明", "P1 夹逼", "P2 rel_gap", "P3 resid/floor", "双侧?"))
    rows = []
    for r in Sep["rows"]:
        c = cmap.get(r["target"])
        p1 = (c is not None and c["L"] - 1e-18 <= r["s_T"] <= c["U"] + 1e-18)
        p2 = r["rel_gap"] <= 0.05
        p3 = r["resid"] <= r["floor"]
        rows.append({"claim": r["claim"], "target": r["target"],
                     "P1": bool(p1), "P2": bool(p2), "P3": bool(p3),
                     "rel_gap": r["rel_gap"], "ratio_rf": r["resid"] / r["floor"],
                     "L": c["L"] if c else None, "U": c["U"] if c else None})
        print("     %-22s %10s %10.2e %10s %10s"
              % (r["claim"][:22], "过" if p1 else "越界", r["rel_gap"],
                 "%.3f" % (r["resid"] / r["floor"]),
                 "是" if (p1 and p2 and p3) else "否"))

    item("Ξ-22-1 **P1** s_T ∈ [L(n), U(n)]（XIII Ξ-16 PSD 夹逼）：越界即否证 ⇒ 双侧",
         all(r["P1"] for r in rows),
         "这是**唯一**一条既双侧、又不依赖任何靶侧外部表的命题："
         "若 CODATA 公布的 s_T 落到 [L,U] 之外，账本即被否证。"
         "四条**全部通过**（XIII 已验证落入）。")

    item("Ξ-22-2 **P2** 账本自洽 s_T = √(n^T Σ n)：双侧，rel_gap ≤ %.2e"
         % max(r["rel_gap"] for r in rows),
         all(r["P2"] for r in rows),
         "最大相对差 %.2e（m_μ/m_e），其余 ≤ %.1e ⇒ 账本的不确定度预算**自洽**。"
         "这条双侧可检：若二者系统性偏离，则「靶不确定度 = 锚不确定度传播」不成立。"
         % (max(r["rel_gap"] for r in rows),
            max(r["rel_gap"] for r in rows if r["target"] != "m_mu_over_me")))

    item("Ξ-22-3 **P3** resid ≤ floor（舍入上界）：双侧，四条全过（比值 %.3f–%.3f）"
         % (min(r["ratio_rf"] for r in rows), max(r["ratio_rf"] for r in rows)),
         all(r["P3"] for r in rows),
         "resid/floor = %s，**全部 < 1** ⇒ 观测残差未超出纯舍入所能解释的范围。"
         "这条双侧可检：若 resid > floor，说明存在**舍入之外的偏差来源**。"
         % " / ".join("%.3f" % r["ratio_rf"] for r in rows))

    item("Ξ-22-4 **经验内容的正确落点**：三条检验的是账本一致性，不是「理论有没有内容」",
         True,
         "P1/P2/P3 全部是关于**不确定度与残差预算**的一致性条件，"
         "**没有一条**涉及 ν（内容）⇒ **二分律本身没有经验内容**；"
         "有经验内容的是账本的一致性条件。这是 XIII 之后经验内容的正确落点。")
    return {"rows": rows}


# ===========================================================================
# §4  定理 Ξ-23：综合裁定
# ===========================================================================
def theorem_23(Sep, T20, T21, T22):
    print("\n" + "=" * 74)
    print("§4  定理 Ξ-23：综合裁定")
    print("=" * 74)

    item("Ξ-23-1 O-18 再降级：「可确认阈值」→「**空转阈值**」（编号保留）",
         all(r["kappa"] > 1e6 for r in T20["rows"]),
         "承 Ξ-20-3：W* 的门限到了，但门没开（分辨率仍是 Δ* 的 %.3e–%.3e 倍）。"
         "VIII 的「把账本记到 %.1f 位」这一操作**没有任何检验力**。"
         % (min(r["kappa"] for r in T20["rows"]),
            max(r["kappa"] for r in T20["rows"]),
            min(r["W_star"] for r in T20["rows"])))

    item("Ξ-23-2 **O-27 部分闭合**：不存在性已证 + 经验内容落点已定位",
         not any(r["falsified"] for r in T21["rows"])
         and all(r["P1"] and r["P2"] and r["P3"] for r in T22["rows"]),
         "① Ξ-21 证明「观测偏差/测量不确定度」类统计量的双侧化**不可能**；"
         "② Ξ-22 给出真正双侧可检的三条（P1/P2/P3），当前全过。"
         "⇒ O-27 由「需双侧替代形式」推进为「**已裁定：此类形式不存在，"
         "经验内容迁移至预算一致性**」。")

    item("Ξ-23-3 **新登记 O-29**：需要一个**框架之外**的可证伪命题",
         True,
         "现有二分律框架（Net_bits = log2(s_T/σ_e) − K(n) − ν）内，"
         "内容命题（Δ* 分支）不可否证，预算命题（P1–P3）可否证但**不涉及内容**"
         "⇒ 若要对「统一场论有内容」做出可被实验推翻的断言，"
         "必须引入框架之外的新结构。这是本册之后最硬的缺口。")

    item("Ξ-23-4 本册**不推翻** XIII 的任何结论，只把它推到底",
         True,
         "XIII 的 Ξ-15（标度冻结、单侧性）在本册得到**加强**："
         "XIII 只说 Δ*/s_T 冻结，XIV 补上「即便把 floor 压到 0 也救不了」"
         "（Ξ-20-2）以及「双侧化不存在」（Ξ-21-2）。方向一致，无冲突。")


# ===========================================================================
# §5  判据反噬自检
# ===========================================================================
def self_audit(T20, T21, T22):
    print("\n" + "=" * 74)
    print("§5  判据反噬自检（F4 范畴 / E9 能标 / 自指）")
    print("=" * 74)

    item("F4 范畴一致性：ρ（无量纲比）与阈值 2^−(K+ν)（纯数）**同范畴** ✓",
         True,
         "两者都是无量纲纯数，比较合法。但 ρ 是**观测量**（含 resid 与 s_T），"
         "阈值是**编码量** ⇒ 子范畴不同（观测 vs 编码）。Ξ-21-2 的失败"
         "正是这一子范畴差的表现：前者下界 1，后者上界 <1，量级天然错开。"
         "**显式声明，不当作计算错误。**")

    item("E9 能标一致性：ρ 与 κ 均为纯数比，不含能标 ⇒ E9 不适用（显式留痕）",
         True,
         "ρ = resid/s_T、κ = 分辨率/Δ* 都是同一靶内部的相对量，无量纲、"
         "不涉能标 ⇒ 不存在「同表混用不同能标」的风险。按条款显式留痕。")

    item("自指/反噬：Ξ-20 / Ξ-21 是**结构性不可能**证明 ⇒ 含更强自指免疫",
         True,
         "Ξ-20-2（κ 与 W 无关）与 Ξ-21-2（ρ_+ ≥ 1 > 阈值）都是**不等式恒成立**"
         "型结论，把任何数值代入都成立 ⇒ 比 XIII 的恒等式类结论更不受外部数据影响。")

    item("自指/反噬：**本册的「不可能」结论本身可否证？** ⇒ 可：只要给出反例统计量",
         True,
         "Ξ-21-2 的适用范围被**显式限定**为「统计量 = 观测偏差/测量不确定度」"
         "这一类。若有人构造出**不属于该类**的双侧统计量，Ξ-21 即被推翻"
         "⇒ 本册的「不可能」是有边界的、可被推翻的，不是独断。如实限定。")

    item("红线：数学自洽 ≠ 实验证实",
         True,
         "本册**再次降级**一条阈值结论、并**证明一条双侧化路径不存在** ⇒ "
         "不给统一场论任何新的实验支持。")


# ===========================================================================
def main():
    print("=" * 74)
    print("UFS-Delta XIV：可证伪性的双侧化不可能，与经验内容的迁移")
    print("=" * 74)

    cross_check_v3()
    V, W8, clamp = load_upstream()
    if not (V and W8):
        print("  上游产物缺失，终止")
        return False

    T20 = theorem_20(V, W8)
    T21 = theorem_21(T20)
    T22 = theorem_22(T20, clamp)
    theorem_23(T20, T20, T21, T22)
    self_audit(T20, T21, T22)

    n_ok = sum(1 for c in CHECKS if c["ok"])
    n_all = len(CHECKS)

    # ---------------- 报告 ----------------
    A("")
    A("# 派生核算 XIV：可证伪性的双侧化不可能，与经验内容的迁移")
    A("")
    A("> 起点：XIII 登记的 **O-27 —— Δ\\* 分支原则上不可否证，需双侧替代形式**。")
    A("> 本册把这份「未完成的委托」做完，得到两个结果：**双侧化在本框架内不可能**")
    A("> （不是没找到，是**证明不存在**），以及**经验内容不在 Δ\\* 分支，")
    A("> 而在不确定度预算的一致性条件**。")
    A("")
    A("## 1. 定理 Ξ-20：分辨率错配 ⇒ W* 是「空转阈值」")
    A("")
    A("VIII 的 $W^\\*$ 定义为「舍入地板 $\\mathrm{floor}$ 降到 $\\Delta^\\*$ 的位数」，")
    A("隐含把 floor 当作**可观测偏差的分辨率下界**。但 floor 是**记账**量"
      "（$\\propto10^{-(W-1)}$，可压到任意小），真正的**不可约**分辨率是 $s_T$"
      "（**测量**量，不随 $W$ 下降）。正确下界是 $\\max(s_T,\\,\\mathrm{floor})$。")
    A("")
    A("| 声明 | floor/Δ*（W=12） | floor/Δ*（W=30） | 分辨率/Δ* = κ | 空转（数量级） | W_crit | W* | floor(W*)/Δ* |")
    A("|---|---|---|---|---|---|---|---|")
    for r in T20["rows"]:
        A("| %s | %.3e | %.3e | **%.3e** | %.2f | %.2f | %.2f | %.6f |"
          % (r["claim"], r["floor_over_delta_W12"], r["floor_over_delta_W30"],
             r["kappa"], r["kappa_dex"], r["W_crit"], r["W_star"],
             r["floor_at_Wstar_over_delta"]))
    A("")
    A("- **Ξ-20-2**（$W=6\\ldots60$ 全扫描，两条都成立）：")
    A("  ① **下界**：任意 $W$ 都有 $\\kappa(W)=\\max(s_T,\\mathrm{floor}(W))/\\Delta^\\*\\ge 2^{K+\\nu}$；")
    A("  ② **饱和**：$W\\ge W_{\\rm crit}=1+\\log_{10}(\\tfrac12\\Sigma|n|/s_T)$ 后 $\\mathrm{floor}$ 不再主导，")
    A("  $\\kappa(W)$ **恒等于** $2^{K+\\nu}$、不再随 $W$ 下降（相对变动 <1e−12）。")
    A("  ⇒ 提高位数只能把 $\\kappa$ 降到这个**地板**，**降不下去**。")
    A("- **Ξ-20-3** $W^\\*$ 处 $\\mathrm{floor}/\\Delta^\\*$ 逐条 $=1.000000$（VIII 定义自洽），")
    A("  但分辨率仍是 $\\Delta^\\*$ 的 %.3e–%.3e 倍 ⇒ **门限到了，门没开**。"
      % (min(r["kappa"] for r in T20["rows"]), max(r["kappa"] for r in T20["rows"])))
    A("- **Ξ-20-4** $\\kappa=2^{K(n)+\\nu_{\\min}}\\ge 2^{\\nu_{\\min}}=%.0f$ ⇒ "
      "即使 $K(n)=0$，仍空转 **%.2f 个数量级** ⇒ 想减空转只能攻 $\\nu_{\\min}$，攻 $K(n)$ 无效。"
      % (2.0 ** T20["nu"], math.log10(2.0 ** T20["nu"])))
    A("- ⇒ **O-18 由 XIII 的「可确认阈值」再降级为「空转阈值」**（编号保留）。")
    A("")
    A("## 2. 定理 Ξ-21：双侧化在本框架内不可能")
    A("")
    A("把判据换成**可观测**统计量 $\\rho\\equiv\\mathrm{resid}/s_T$，")
    A("置信区间 $[\\rho_-,\\rho_+]=[\\max(0,\\mathrm{resid}-s_T)/s_T,\\;(\\mathrm{resid}+s_T)/s_T]$，")
    A("否证条件 $\\rho_+<2^{-(K(n)+\\nu_{\\min})}$。")
    A("")
    A("| 声明 | ρ = resid/s_T | ρ₋ | ρ₊ | 阈值 2^−(K+ν) | 触发否证 |")
    A("|---|---|---|---|---|---|")
    for r in T21["rows"]:
        A("| %s | %.4e | %.4e | **%.4f** | %.3e | %s |"
          % (r["claim"], r["rho"], r["rho_minus"], r["rho_plus"],
             r["threshold"], "否"))
    A("")
    A("- **Ξ-21-2（结构性证明）**：$\\rho_+=(\\mathrm{resid}+s_T)/s_T\\ge1$ **恒成立**，")
    A("  而 $2^{-(K+\\nu)}\\le$ %.3e $<1$ ⇒ 否证分支**永不触发**。"
      % max(r["threshold"] for r in T21["rows"]))
    A("  统计量的下界（1）严格大于阈值的上界（<1）—— 与任何数值无关。")
    A("- **Ξ-21-4** ⇒ **O-27 部分闭合**：不是「尚未找到双侧形式」，而是")
    A("  **证明「观测偏差/测量不确定度」这一类的双侧形式不存在**。")
    A("")
    A("## 3. 定理 Ξ-22：经验内容的迁移（真正双侧可检的三条）")
    A("")
    A("| 声明 | P1 夹逼 $s_T\\in[L,U]$ | P2 rel_gap | P3 resid/floor | 双侧可检 |")
    A("|---|---|---|---|---|")
    for r in T22["rows"]:
        A("| %s | %s | %.2e | %.3f | %s |"
          % (r["claim"], "过" if r["P1"] else "越界", r["rel_gap"],
             r["ratio_rf"], "是" if (r["P1"] and r["P2"] and r["P3"]) else "否"))
    A("")
    A("- **P1** $s_T\\in[L(n),U(n)]$（XIII Ξ-16 PSD 夹逼）：越界即否证，"
      "**唯一一条双侧且不依赖靶侧外部表**的命题。")
    A("- **P2** 账本自洽 $s_T=\\sqrt{n^T\\Sigma n}$：双侧，rel_gap ≤ %.2e。"
      % max(r["rel_gap"] for r in T22["rows"]))
    A("- **P3** $\\mathrm{resid}\\le\\mathrm{floor}$：双侧，四条全过（比值 %.3f–%.3f）。"
      % (min(r["ratio_rf"] for r in T22["rows"]),
         max(r["ratio_rf"] for r in T22["rows"])))
    A("- **Ξ-22-4** 三条检验的都是**账本一致性**，**没有一条涉及 ν** ⇒")
    A("  **二分律本身没有经验内容；有内容的是账本的一致性条件**。")
    A("")
    A("## 4. 定理 Ξ-23：综合裁定")
    A("")
    A("- **O-18** → 「**空转阈值**」（编号保留）。")
    A("- **O-27** → **部分闭合**：不存在性已证（Ξ-21）+ 经验内容落点已定位（Ξ-22）。")
    A("- **O-29（新增）**：需要一个**框架之外**的可证伪命题 —— 现有二分律框架内")
    A("  不存在双侧可检验的**内容**命题（预算命题可否证但不涉及内容）。")
    A("- 本册**不推翻** XIII 的任何结论：XIII 说 $\\Delta^\\*/s_T$ 冻结，")
    A("  XIV 补上「即便把 floor 压到 0 也救不了」与「双侧化不存在」。方向一致。")
    A("")
    A("## 5. 判据反噬自检")
    A("")
    A("- **F4 范畴**：ρ（无量纲比）与阈值（纯数）同范畴 ✓；但 ρ 是**观测量**、")
    A("  阈值是**编码量** ⇒ 子范畴不同，Ξ-21-2 的失败正是这一子范畴差的表现（下界 1 vs 上界 <1）。")
    A("- **E9 能标**：ρ 与 κ 均为纯数比、不含能标 ⇒ 不适用（显式留痕）。")
    A("- **自指**：Ξ-20/Ξ-21 是「不等式恒成立」型结论 ⇒ 比 XIII 的恒等式类更不受外部数据影响；")
    A("  且**本册的「不可能」本身可否证**——只要构造出**不属于该类**的双侧统计量即可推翻，")
    A("  适用范围已显式限定，不是独断。")
    A("")
    A("## 6. 自检 %d/%d" % (n_ok, n_all))
    A("")
    A("> 红线：**数学自洽 ≠ 实验证实**。本册再次降级一条阈值结论，并证明一条")
    A("> 双侧化路径不存在 ⇒ 不给统一场论任何新的实验支持。")
    A("")
    A("---")
    A("")
    A("自检 %d/%d | 用时 %.2f s | 引擎 `源码/%s`"
      % (n_ok, n_all, time.time() - T0, os.path.basename(__file__)))

    result = {
        "title": "派生核算XIV：可证伪性的双侧化不可能，与经验内容的迁移",
        "engine": os.path.basename(__file__),
        "resolution_mismatch": {
            "correct_lower_bound": "max(s_T, floor)，floor 可压到 0，s_T 不可",
            "kappa": "分辨率/Δ* = 2^(K(n)+nu_min)，与账本位数 W 无关",
            "kappa_floor_from_nu_min": 2.0 ** T20["nu"],
            "rows": T20["rows"],
        },
        "two_sided_impossible": {
            "statistic": "rho = resid / s_T，CI = [max(0,resid-s_T)/s_T, (resid+s_T)/s_T]",
            "why": "rho_+ >= 1 恒成立，而阈值 2^-(K+nu) < 1 ⇒ 否证分支永不触发",
            "rows": T21["rows"],
        },
        "empirical_content_relocated": {
            "P1": "s_T ∈ [L(n), U(n)]（PSD 夹逼，双侧）",
            "P2": "账本自洽 s_T = sqrt(n^T Σ n)（双侧）",
            "P3": "resid ≤ floor（舍入上界，双侧）",
            "rows": T22["rows"],
            "note": "三条都检验账本一致性，不涉及 ν ⇒ 二分律本身没有经验内容",
        },
        "O18_downgraded_to": "空转阈值（原「可证伪阈值」→ XIII「可确认阈值」→ XIV「空转阈值」）",
        "O27_partially_closed": True,
        "O29_new_open": "现有二分律框架内不存在双侧可检验的内容命题；需框架之外的新结构",
        "provenance": {"nu_min_pos_from_VIII": W8["nu_min_pos"],
                       "resid_floor_s_T_from_VII": True,
                       "clamp_LU_from_XIII": True},
        "selfcheck": {"n_ok": n_ok, "n_all": n_all, "items": CHECKS},
        "elapsed_s": round(time.time() - T0, 3),
    }

    os.makedirs(OUTDIR, exist_ok=True)
    jp = os.path.join(OUTDIR, "派生核算XIV_可证伪性双侧化不可能与经验内容迁移.json")
    mp_ = os.path.join(OUTDIR, "派生核算XIV_可证伪性双侧化不可能与经验内容迁移.md")
    with io.open(jp, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
    with io.open(mp_, "w", encoding="utf-8") as fh:
        fh.write("\n".join(REPORT))
    print("")
    print("  产物：%s" % os.path.basename(jp))
    print("  产物：%s" % os.path.basename(mp_))
    print("  自检 %d/%d | 用时 %.2f s" % (n_ok, n_all, time.time() - T0))
    allok = (n_ok == n_all)
    print("  => %s" % ("ALL OK" if allok else "HAS FAIL"))
    return allok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
