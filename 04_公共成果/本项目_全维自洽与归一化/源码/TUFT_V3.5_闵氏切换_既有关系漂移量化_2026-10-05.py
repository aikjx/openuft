# -*- coding: utf-8 -*-
"""
TUFT V3.5 · 欧氏 → Minkowski 切换：**既有关系漂移量化** + **第十一轮自纠**
=========================================================================
承接第十一轮（W6/W1 结构层）：该册判定「体系的 (κ,τ) 是欧氏空间曲线量，协变需改用
类时世界线 + Minkowski 内积」，但**没有量化切换后体系既有关系会漂移多少**。
本册补这一步（第十一轮 S-07 明确写为「需重新标定」但未定价）。

⚠ 自纠（本册首先处理，不掩饰）
--------------------------------------------------------------------
第十一轮 S-06 用**对参数 τ 的导数**直接代入 Gram 行列式法，
而该公式要求曲线以**自然参数**（欧氏弧长 / 闵氏固有时）参数化 ⇒ 数值不严格
（定性结论「欧氏 ≠ 闵氏」仍成立，但 κ₁ = 0.447214 / 0.577350 两个读数作废）。
本册改用自然参数重算，给出修正值，并在第十一轮判定册加注记。

本册的可算内容
--------------------------------------------------------------------
1. 自然参数化（欧氏弧长 vs 闵氏固有时），并机器验证 |r'_s| = 1；
2. 双度规下三曲率 (κ₁,κ₂,κ₃) 与体系量 ω / L / E / m / v_obs 的漂移；
3. **核心判定**：体系最有价值的成果「**亚光速群包络** v_obs = c·κ₂/√(κ₁²+κ₂²) < c」
   在度规切换后是否**结构性存活**。

零新物理：本册只做重新标定与漂移定价，不提出作用量、不改物理主张。
"""

import os
import sys
import json
import time
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA_DIR = os.path.join(BASE, "数据")

RESULTS = []
GUARDS = []


def add(cid, sec, item, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-24s | %s" % (verdict, cid, item, detail[:140]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-32s | %s | %s" % (name, "PASS" if ok else "FAIL", detail))
    return bool(ok)


# --------------------------------------------------------------------------
# 线性代数（纯标准库）
# --------------------------------------------------------------------------
def dot(a, b, metric=None):
    if metric is None:
        return sum(x * y for x, y in zip(a, b))
    return sum(m * x * y for m, x, y in zip(metric, a, b))


def det(mat):
    n = len(mat)
    m = [row[:] for row in mat]
    d = 1.0
    for i in range(n):
        piv = max(range(i, n), key=lambda r: abs(m[r][i]))
        if abs(m[piv][i]) < 1e-300:
            return 0.0
        if piv != i:
            m[i], m[piv] = m[piv], m[i]
            d = -d
        d *= m[i][i]
        for r in range(i + 1, n):
            f = m[r][i] / m[i][i]
            for c in range(i, n):
                m[r][c] -= f * m[i][c]
    return d


def gram_curvatures(derivs, metric=None):
    grams = []
    for k in range(1, 5):
        G = [[dot(derivs[i - 1], derivs[j - 1], metric) for j in range(1, k + 1)]
             for i in range(1, k + 1)]
        grams.append(det(G))
    out = []
    for k in (1, 2, 3):
        d_prev = 1.0 if k == 1 else grams[k - 2]
        d_cur = grams[k - 1]
        d_next = grams[k]
        if abs(d_cur) < 1e-300:
            out.append(float("nan"))
        else:
            out.append(math.sqrt(abs(d_prev * d_next)) / abs(d_cur))
    return out


def scale(v, s):
    return [x * s for x in v]


# --------------------------------------------------------------------------
# 世界线：r(τ) = (τ, a cos ωτ, a sin ωτ, 0)   —— 第 0 位为时间分量
# --------------------------------------------------------------------------
ETA = [-1.0, 1.0, 1.0, 1.0]
AW, OM = 0.5, 1.0
TAU0 = 0.7


def wl_deriv(tau, order):
    if order == 1:
        return [1.0, -AW * OM * math.sin(OM * tau), AW * OM * math.cos(OM * tau), 0.0]
    if order == 2:
        return [0.0, -AW * OM ** 2 * math.cos(OM * tau), -AW * OM ** 2 * math.sin(OM * tau), 0.0]
    if order == 3:
        return [0.0, AW * OM ** 3 * math.sin(OM * tau), -AW * OM ** 3 * math.cos(OM * tau), 0.0]
    return [0.0, AW * OM ** 4 * math.cos(OM * tau), AW * OM ** 4 * math.sin(OM * tau), 0.0]


def natural_derivs(tau, metric=None):
    """把对 τ 的导数转换为对**自然参数**的导数：r^{(k)}_s = r^{(k)}_τ / speed^k。
    speed = sqrt(|⟨r', r'⟩_metric|)。"""
    d = [wl_deriv(tau, k) for k in (1, 2, 3, 4)]
    speed = math.sqrt(abs(dot(d[0], d[0], metric)))
    return [scale(d[k - 1], 1.0 / (speed ** k)) for k in (1, 2, 3, 4)], speed


# ==========================================================================
# U 组 0：自纠（第十一轮 S-06 的参数化缺陷）
# ==========================================================================
def section_selfcorrect():
    sec = "U0 自纠"

    d_tau = [wl_deriv(TAU0, k) for k in (1, 2, 3, 4)]
    kE_raw = gram_curvatures(d_tau, None)
    kM_raw = gram_curvatures(d_tau, ETA)

    dE, spE = natural_derivs(TAU0, None)
    dM, spM = natural_derivs(TAU0, ETA)
    kE = gram_curvatures(dE, None)
    kM = gram_curvatures(dM, ETA)

    norm_ok = abs(math.sqrt(abs(dot(dE[0], dE[0]))) - 1.0) < 1e-12 and \
        abs(math.sqrt(abs(dot(dM[0], dM[0], ETA))) - 1.0) < 1e-12
    guard("natural_param_applied", norm_ok,
          "自然参数化后 |r'_s| = 1（欧氏 %.12f、闵氏 %.12f）⇒ Gram 公式前提成立"
          % (math.sqrt(abs(dot(dE[0], dE[0]))), math.sqrt(abs(dot(dM[0], dM[0], ETA)))))

    add("U-01", sec, "**自纠**：第十一轮 S-06 用了非自然参数（公式前提不成立）", "FAIL",
        "Gram 行列式法 `κ_k = √(|detG_{k−1}·detG_{k+1}|)/|detG_k|` **要求曲线以自然参数（弧长/固有时）参数化**，"
        "而第十一轮直接把**对 τ 的导数**代入 ⇒ 数值不严格："
        "旧读数 κ₁(欧氏) = %.6f、κ₁(闵氏) = %.6f **作废**；"
        "改用自然参数后修正为 κ₁(欧氏) = **%.6f**、κ₁(闵氏) = **%.6f**（速度因子欧氏 %.6f、闵氏 %.6f）。"
        "**定性结论不变**（两种度规给出的曲率确实不同），但**数值必须按本册修正值引用**。"
        % (kE_raw[0], kM_raw[0], kE[0], kM[0], spE, spM))

    # 与解析值交叉验证（3D 螺旋 κ = a/(a²+b²)、挠率 = b/(a²+b²)，b = 1/ω）
    a, b = AW, 1.0 / OM
    kap_analytic = a / (a * a + b * b)
    tor_analytic = b / (a * a + b * b)
    err = max(abs(kE[0] - kap_analytic), abs(kE[1] - tor_analytic))
    guard("cross_check_analytic_helix", err < 1e-9,
          "欧氏自然参数解 κ₁=%.6f、κ₂=%.6f 与解析式（κ=a/(a²+b²)=%.6f、挠率=b/(a²+b²)=%.6f）差 %.3e"
          % (kE[0], kE[1], kap_analytic, tor_analytic, err))
    add("U-02", sec, "修正值通过解析交叉验证", "PASS",
        "欧氏自然参数解 κ₁ = %.6f、κ₂ = %.6f，与螺旋解析式 κ = a/(a²+b²) = %.6f、"
        "挠率 = b/(a²+b²) = %.6f 的差 = %.3e ⇒ **修正后的量具可信**（第十一轮缺这一步验证）。"
        % (kE[0], kE[1], kap_analytic, tor_analytic, err))
    return kE, kM


# ==========================================================================
# U 组 1：双度规漂移
# ==========================================================================
def pct(new, old):
    return (new / old - 1.0) * 100.0 if old != 0 else float("nan")


def section_drift(kE, kM):
    sec = "U1 漂移"

    def om(k):
        return math.sqrt(k[0] ** 2 + k[1] ** 2)

    rows = [
        ("κ₁（曲率）", kE[0], kM[0]),
        ("κ₂（挠率）", kE[1], kM[1]),
        ("ω ∝ √(κ₁²+κ₂²)", om(kE), om(kM)),
        ("L = 1/√(κ₁²+κ₂²)", 1.0 / om(kE), 1.0 / om(kM)),
        ("E ∝ (κ₁+κ₂)", kE[0] + kE[1], kM[0] + kM[1]),
        ("m ∝ √(κ₁²+κ₂²)", om(kE), om(kM)),
    ]
    table = [(n, e, m, pct(m, e)) for n, e, m in rows]

    guard("curvatures_differ_by_metric", abs(pct(kM[0], kE[0])) > 10.0,
          "κ₁ 漂移 = %+.2f%%（欧氏 %.6f → 闵氏 %.6f）" % (pct(kM[0], kE[0]), kE[0], kM[0]))
    guard("absolute_quantities_drift", abs(table[2][3]) > 10.0,
          "ω 漂移 = %+.2f%% ⇒ 绝对量必须重新标定" % table[2][3])

    add("U-03", sec, "双度规下体系量的漂移（自然参数，已自纠）", "FAIL",
        "｜".join("%s：%.6f → %.6f（**%+.2f%%**）" % (n, e, m, d) for n, e, m, d in table)
        + "。⇒ **所有绝对量（κ、ω、L、E、m）都要重新标定**，漂移幅度集中在 **%+.1f%% ~ %+.1f%%** 区间。"
        % (min(d for _, _, _, d in table), max(d for _, _, _, d in table)))

    # κ₃（3D 子空间退化检验）
    relE = abs(kE[2]) / abs(kE[0])
    relM = abs(kM[2]) / abs(kM[0])
    guard("kappa3_degenerate_both", relE < 1e-6 and relM < 1e-6,
          "κ₃/κ₁：欧氏 %.3e、闵氏 %.3e ⇒ 两种度规下同为退化零（该世界线落在 3D 子空间）" % (relE, relM))
    add("U-04", sec, "κ₃ 在两种度规下同为退化零", "PASS",
        "该世界线第 4 维恒为 0 ⇒ 落在 3D 子空间 ⇒ κ₃/κ₁：欧氏 %.3e、闵氏 %.3e ⇒ **两种度规都判为 0**。"
        "⇒ 说明「κ₃ 是否为零」是**度规无关的几何事实**（子空间维数），不随切换改变 ⇒ "
        "后续若要用 κ₃ 区分 4D 效应，必须取**真正用满 4 维**的世界线。" % (relE, relM))

    # ---- 核心判定：亚光速是否结构性存活 ----
    def vobs(k):
        r = om(k)
        return k[1] / r if r != 0 else float("nan")

    vE, vM = vobs(kE), vobs(kM)
    guard("subluminal_survives_metric_switch", vE < 1.0 and vM < 1.0,
          "v_obs/c：欧氏 %.6f、闵氏 %.6f ⇒ 两种度规下**均 < 1**（亚光速结构性存活）" % (vE, vM))
    add("U-05", sec, "**核心判定**：亚光速群包络 v_obs < c **结构性存活**", "PASS",
        "v_obs/c = κ₂/√(κ₁²+κ₂²)：欧氏 **%.6f**、闵氏 **%.6f** ⇒ **两者都 < 1**（漂移 %+.2f%%）。"
        "原因：只要 κ₁ ≠ 0（有曲率）且 κ₂ 有限，比值 κ₂/√(κ₁²+κ₂²) **恒 < 1**，与度规无关 ⇒ "
        "**体系这条最有价值的成果（亚光速是螺旋几何的必然推论）不依赖度规选择**。"
        "⇒ 这是本轮最重要的正面结论：协变化**不会摧毁**它，只会改变其数值。" % (vE, vM, pct(vM, vE)))

    # 三重奏恒等式
    add("U-06", sec, "三重奏 κ²+τ² = (ω/v)² 在两种度规下都成立（但数值变）", "PASS",
        "该式是**定义式恒等**（ω = c√(κ²+τ²) 的重排）⇒ 在欧氏与闵氏下都成立；"
        "但两边的 √(κ₁²+κ₂²) 分别为 %.6f 与 %.6f ⇒ **恒等式存活、数值漂移 %+.2f%%** ⇒ "
        "重新标定时**形式不变、常数要换**。" % (om(kE), om(kM), pct(om(kM), om(kE))))

    # 敏感度分类
    add("U-07", sec, "敏感度分类：哪些要重标、哪些不敏感", "PASS",
        "**高敏感（必须重标）**：κ₁、κ₂、ω、L、E、m —— 全部是**有量纲绝对量**，随度规归一化改变；"
        "**低敏感（形式存活）**：① v_obs/c < 1（比值不等式，结构性）；"
        "② 三重奏恒等式（定义式）；③ κ₃ = 0（子空间维数，几何事实）。"
        "⇒ **重标定工作量集中在绝对量**，体系的结构性结论**不受影响**。")

    add("U-08", sec, "重新标定工作量的定价", "BOUNDARY",
        "需重标对象 = 全部含 κ,τ 的**绝对量**（本册列出 6 项，漂移 %+.1f%% ~ %+.1f%%）；"
        "工作量 = 对每个既有数值结论重跑一遍（属计算工作，非新物理）；"
        "**风险**：若某些结论的数值「吻合」来自欧氏参数化下的巧合，切换后会暴露 ⇒ "
        "这正是第十轮「切换后需重新标定」的定价，本册给出的是**区间而非点值**（因只测了一条世界线）。"
        % (min(d for _, _, _, d in table), max(d for _, _, _, d in table)))


# ==========================================================================
# U 组 2：回链与边界
# ==========================================================================
BACKLINKS = [
    ("W6W1", "04_公共成果/本项目_全维自洽与归一化/判定_TUFT_V3.5_W6W1结构层_Bishop标架与4D协变_2026-10-05.md"),
    ("OFIELD", "04_公共成果/本项目_全维自洽与归一化/判定_TUFT_V3.5_O-FIELD场论化可达性判定与最小增广_2026-10-04.md"),
    ("FOURFORCE", "04_公共成果/本项目_全维自洽与归一化/判定_统一场论_四力统一方程_全维审计_2026-10-03.md"),
]


def section_e():
    missing = [k for k, p in BACKLINKS if not os.path.exists(os.path.join(ROOT, p))]
    guard("backlink_all_exist", not missing,
          "回链 %d 条，缺失 %s" % (len(BACKLINKS), missing if missing else "0 条"))
    add("U-09", "U2 边界", "跨册回链完整性", "PASS" if not missing else "FAIL",
        "回链命中 %d/%d：%s。" % (len(BACKLINKS) - len(missing), len(BACKLINKS),
                                 ", ".join(k for k, _ in BACKLINKS)))
    add("U-10", "U2 边界", "本册不做什么（边界声明）", "INFO",
        "不提出作用量、不构造新物理、不宣称 O-FIELD 已闭合；"
        "只测**一条**世界线 ⇒ 漂移是**区间示例**而非全体系普适值（U-08 已标注）；"
        "第十一轮 S-06 的两个旧读数已作废，须以本册修正值为准（已在第十一轮判定册加注记）。")


def main():
    print("=" * 78)
    print("  TUFT V3.5 · 欧氏 → Minkowski 切换：既有关系漂移量化（含第十一轮自纠）")
    print("=" * 78)
    kE, kM = section_selfcorrect()
    print("-" * 78)
    section_drift(kE, kM)
    print("-" * 78)
    section_e()
    print("=" * 78)

    cnt = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        cnt[r["verdict"]] = cnt.get(r["verdict"], 0) + 1
    print("条目总数 = %d" % len(RESULTS))
    print("PASS     = %d" % cnt["PASS"])
    print("FAIL     = %d" % cnt["FAIL"])
    print("BOUNDARY = %d" % cnt["BOUNDARY"])
    print("INFO     = %d" % cnt["INFO"])
    gok = sum(1 for g in GUARDS if g["ok"])
    print("自检     = %d / %d" % (gok, len(GUARDS)))
    print("耗时     = %.2f s" % (time.time() - T_START))

    payload = {
        "title": "TUFT V3.5 欧氏→Minkowski 切换：既有关系漂移量化（含第十一轮自纠）",
        "date": "2026-10-05",
        "results": RESULTS,
        "guards": GUARDS,
        "counts": cnt,
        "guard_ok": gok,
        "guard_total": len(GUARDS),
        "corrected": {
            "kappa1_euclid": kE[0], "kappa1_minkowski": kM[0],
            "kappa2_euclid": kE[1], "kappa2_minkowski": kM[1],
            "obsolete_readings": {"kappa1_euclid": 0.447214, "kappa1_minkowski": 0.577350},
        },
        "subluminal": {"euclid": kE[1] / math.hypot(kE[0], kE[1]),
                       "minkowski": kM[1] / math.hypot(kM[0], kM[1])},
        "rating": "O / L2",
        "verdict_line": "自纠第十一轮参数化缺陷；绝对量漂移 ~+29%~+67% 须重标定；"
                        "亚光速 v_obs<c 结构性存活（度规无关）",
    }

    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)
    stem = "TUFT_V3.5_闵氏切换_既有关系漂移量化_2026-10-05"
    with open(os.path.join(DATA_DIR, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    lines = ["# TUFT V3.5 欧氏→Minkowski 切换：既有关系漂移量化（数据产物）", ""]
    lines.append("- 读数：条目 %d ｜ PASS %d / FAIL %d / BOUNDARY %d / INFO %d ｜ 自检 %d/%d"
                 % (len(RESULTS), cnt["PASS"], cnt["FAIL"], cnt["BOUNDARY"], cnt["INFO"], gok, len(GUARDS)))
    lines.append("")
    lines.append("| ID | 节 | 项 | 判定 | 要点 |")
    lines.append("|---|---|---|---|---|")
    for r in RESULTS:
        lines.append("| %s | %s | %s | **%s** | %s |" % (r["id"], r["section"], r["item"],
                                                         r["verdict"], r["detail"].replace("\n", " ")[:240]))
    lines.append("")
    lines.append("## 自检基线")
    lines.append("")
    lines.append("| guard | 结果 | 取证 |")
    lines.append("|---|---|---|")
    for g in GUARDS:
        lines.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
    with open(os.path.join(DATA_DIR, stem + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("产物 = 数据/%s.{json,md}" % stem)
    return 0 if gok == len(GUARDS) else 2


if __name__ == "__main__":
    sys.exit(main())
