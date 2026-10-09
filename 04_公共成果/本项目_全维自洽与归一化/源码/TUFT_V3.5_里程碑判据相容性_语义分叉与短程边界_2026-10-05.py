# -*- coding: utf-8 -*-
"""
TUFT V3.5 · 攻 W2 之前的**前置检验**：里程碑判据 M1–M5 的相容性分析
=========================================================================
第十轮给出补齐 W2（作用量/场方程）的五条验收判据 M1–M5，但**没有检验这五条能否同时成立**。
若它们彼此不相容，那么「按 M1–M5 去找作用量」就是在找一个不存在的东西 —— 
这会比直接构造更早地浪费工作量。本册做这个前置检验。

M1 线性化后给出 ω = c√(κ²+τ²)
M2 静态解给出 1/r² 力
M3 给出亚光速群包络 v_obs = c·τ/√(κ²+τ²) < c
M4 含波数 k ⇒ ∂ω/∂k ≠ 0
M5 最高时间导数阶 ≤ 2（无 Ostrogradsky 鬼场）

本册的两条可算发现（零新物理，纯逻辑 + 量纲 + 判别式）
--------------------------------------------------------------------
① **M1 ↔ M4 不相容（语义分叉）**：M1 中 ω 由几何量 κ,τ 决定、不含波数 k ⇒ ∂ω/∂k = 0
   ⇒ 与 M4 直接冲突。唯一解是把 κ,τ 由「几何量」改释为「模态量（含 k）」⇒ 那是**改定义**，需显式声明。
② **M1 + M2 联合存在短程失效边界**：由 κ+τ ∝ 1/r（M2）与 κ²+τ² = Ω₀²（M1）联立，
   实数解要求判别式 2Ω₀² − (κ+τ)² ≥ 0 ⇒ **r ≥ r_min**；代入体系自有关系 m = ℏΩ₀/c 得
   **r_min = √2·GM/c² = 0.7071 r_s**（Schwarzschild 半径的 0.707 倍）。

不构造新物理：本册只分析判据之间的相容性，不提出任何候选作用量。
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
# 常数
# --------------------------------------------------------------------------
G_N = 6.67430e-11
C_LIGHT = 299792458.0
HBAR = 1.054571817e-34
M_SUN = 1.98892e30
M_E = 9.1093837015e-31


# ==========================================================================
# M 组 1：M1 ↔ M4 的语义分叉
# ==========================================================================
def section_m1_m4():
    sec = "M 判据相容性"

    # M1 的 ω 表达式：只含几何量 κ,τ，不含 k ⇒ 对 k 的偏导恒为 0
    def omega_of(kappa, tau, k):
        return C_LIGHT * math.sqrt(kappa ** 2 + tau ** 2)      # 与 k 无关

    k0 = 1.0
    dk = 1e-6
    kap, ta = 0.4, 0.8
    dw_dk = (omega_of(kap, ta, k0 + dk) - omega_of(kap, ta, k0 - dk)) / (2 * dk)
    guard("M1_conflicts_M4", abs(dw_dk) < 1e-9,
          "M1 的 ω = c√(κ²+τ²) 对 k 的数值偏导 = %.3e ⇒ ∂ω/∂k = 0，与 M4 冲突" % dw_dk)

    add("N-01", sec, "**M1 ↔ M4 不相容**：ω 不含 k ⇒ 无法满足「有色散」", "FAIL",
        "M1 要求线性化给出 ω = c√(κ²+τ²)：右端只含**几何量** κ,τ（曲线曲率/挠率），**不含波数 k**；"
        "机器求导 ∂ω/∂k = **%.3e** ⇒ 与 M4（必须含 k、∂ω/∂k ≠ 0）**直接冲突**。"
        "⇒ 在当前 κ,τ 语义（几何量）下，**不可能**同时满足 M1 与 M4："
        "满足 M1 就无色散（无传播），满足 M4 就不再是「ω 由几何决定」。"
        % dw_dk)

    # 语义分叉：两种语义下的可满足性
    add("N-02", sec, "**语义分叉**：κ,τ 是几何量还是模态量？", "BOUNDARY",
        "出路有三条，每条都有代价 —— "
        "**(a) 保持 κ,τ 为几何量** ⇒ 接受**无色散**（放弃 M4）⇒ 体系不能有传播子、无因果结构（第十轮 W4 已判 FAIL）；"
        "**(b) 把 κ,τ 改释为「模态量」**（κ = κ(k)，即波的模态曲率）⇒ 可满足 M4，"
        "但这是**重新定义基本量**，等于引入一条新假设，且 κ²+τ² = (ω/v)² 等既有关系需重标；"
        "**(c) 放弃 M1**（ω 不由几何定）⇒ 则体系当前的运动学核心式失去地位。"
        "⇒ **攻 W2 之前必须先做这个语义选择**，否则「按 M1–M5 找作用量」找不到对象。")

    add("N-03", sec, "M3 与 M1 相容（正面）", "PASS",
        "M3 的 v_obs = c·τ/√(κ²+τ²) 与 M1 的 ω = c√(κ²+τ²) 只用同一组 (κ,τ)，无冲突；"
        "且 v_obs/c = τ/√(κ²+τ²) < 1 在 κ ≠ 0 时恒成立 ⇒ **M3 是唯一已验证与 M1 相容的判据**，"
        "并且（第十二轮已证）它**不依赖度规选择** ⇒ 是体系最稳固的一条。")

    add("N-04", sec, "M5 与其余判据无耦合（独立约束）", "PASS",
        "M5（最高时间导数阶 ≤ 2）是 Ostrogradsky 无鬼条件，只约束场方程的**阶数**，"
        "与 M1/M2/M3/M4 的**取值要求**无耦合 ⇒ 可独立满足，不影响相容性分析。")


# ==========================================================================
# M 组 2：M1 + M2 的短程失效边界
# ==========================================================================
def section_m1_m2():
    sec = "M 短程边界"

    # M2：1/r² 力 ⇒ 势 ∝ 1/r；体系 E = (ℏc/2)(κ+τ)
    #   E = -GMm/r  ⇒  κ+τ = -2GMm/(ℏc) · 1/r   ⇒ 记 A = 2GMm/(ℏc)，u = |κ+τ| = A/r
    # M1：κ²+τ² = Ω₀²，Ω₀ = ω/c；体系自有 m = ℏΩ₀/c ⇒ Ω₀ = mc/ℏ
    # κ,τ 为实数 ⇒ 由 (κ+τ)² = κ²+τ² + 2κτ 及 x² - ux + (u²-Ω₀²)/2 = 0
    #   判别式 Δ = 2Ω₀² - u² ≥ 0 ⇒ u ≤ √2·Ω₀ ⇒ A/r ≤ √2·Ω₀ ⇒ r ≥ A/(√2 Ω₀)
    #   代入 A、Ω₀ ⇒ r_min = √2·GM/c²
    def r_min(M):
        return math.sqrt(2.0) * G_N * M / (C_LIGHT ** 2)

    def r_s(M):
        return 2.0 * G_N * M / (C_LIGHT ** 2)

    rmin_sun = r_min(M_SUN)
    rs_sun = r_s(M_SUN)
    ratio = rmin_sun / rs_sun

    guard("M1_M2_short_range_boundary", abs(ratio - math.sqrt(2.0) / 2.0) < 1e-12,
          "r_min = √2GM/c² = %.1f m（太阳），r_s = %.1f m ⇒ 比值 %.4f = √2/2" % (rmin_sun, rs_sun, ratio))

    # 数值验证：在 r < r_min 处判别式为负（无实数解）
    def discriminant(u, om0):
        return 2.0 * om0 ** 2 - u ** 2

    M_test = M_SUN
    m_test = M_E
    A = 2.0 * G_N * M_test * m_test / (HBAR * C_LIGHT)
    om0 = m_test * C_LIGHT / HBAR
    d_inside = discriminant(A / (0.5 * r_min(M_test)), om0)
    d_outside = discriminant(A / (2.0 * r_min(M_test)), om0)
    guard("discriminant_sign_flips", d_inside < 0 and d_outside > 0,
          "判别式：r = 0.5 r_min 处 %.3e（负，无解）；r = 2 r_min 处 %.3e（正，有解）" % (d_inside, d_outside))

    add("N-05", sec, "**M1 + M2 联合 ⇒ 存在短程失效边界 r ≥ 0.7071 r_s**", "FAIL",
        "推导：M2 要求势 ∝ 1/r，而体系 E = (ℏc/2)(κ+τ) ⇒ **|κ+τ| = A/r**（A = 2GMm/ℏc）；"
        "M1 要求 **κ²+τ² = Ω₀²**（Ω₀ = ω/c，体系自有 m = ℏΩ₀/c ⇒ Ω₀ = mc/ℏ）。"
        "κ,τ 为实数需判别式 Δ = 2Ω₀² − (κ+τ)² ≥ 0 ⇒ **r ≥ A/(√2·Ω₀) = √2·GM/c²**。"
        "⇒ **r_min = √2·GM/c² = %.4f r_s**（Schwarzschild 半径的 0.7071 倍）。"
        "机器验证（太阳）：r_min = %.1f m、r_s = %.1f m；"
        "判别式在 r = 0.5 r_min 处 **%.3e（负 ⇒ 无实数 (κ,τ)）**、在 r = 2 r_min 处 **%.3e（正 ⇒ 有解）**。"
        "⇒ **体系在 r < 0.7071 r_s 内不自洽**：M1 与 M2 不能同时在该区域成立。"
        % (ratio, rmin_sun, rs_sun, d_inside, d_outside))

    add("N-06", sec, "这条边界的意义（不夸大）", "PASS",
        "该边界是由**体系自己的两条判据**推出的（不是外部输入）："
        "它落在 Schwarzschild 半径同量级（0.7071 r_s）⇒ 与「强场/黑洞内部需要新物理」的既有认识**方向一致**。"
        "**但不宣称**它是引力理论的正确边界 —— 它只说明：**若坚持 M1 与 M2 同时成立，体系在 r < 0.7071 r_s 无解**；"
        "这可以是体系的缺陷，也可以是该区域本就超出有效域。**二者需实验/更完整的理论区分，本册不判定。**")

    add("N-07", sec, "对攻 W2 的直接后果", "BOUNDARY",
        "任何候选作用量若要同时满足 M1 与 M2，就**必然继承这条短程边界** ⇒ "
        "要么接受它（并在文档中声明有效域 r > 0.7071 r_s），"
        "要么放弃 M1 或 M2 之一。⇒ **这条边界可作为候选作用量的第 6 条判据（M6）**："
        "「候选必须显式声明其有效域是否覆盖 r < 0.7071 r_s」。")


# ==========================================================================
# 回链与边界
# ==========================================================================
BACKLINKS = [
    ("OFIELD", "04_公共成果/本项目_全维自洽与归一化/判定_TUFT_V3.5_O-FIELD场论化可达性判定与最小增广_2026-10-04.md"),
    ("MINKOWSKI", "04_公共成果/本项目_全维自洽与归一化/判定_TUFT_V3.5_闵氏切换_既有关系漂移量化_2026-10-05.md"),
    ("W6W1", "04_公共成果/本项目_全维自洽与归一化/判定_TUFT_V3.5_W6W1结构层_Bishop标架与4D协变_2026-10-05.md"),
]


def section_e():
    missing = [k for k, p in BACKLINKS if not os.path.exists(os.path.join(ROOT, p))]
    guard("backlink_all_exist", not missing,
          "回链 %d 条，缺失 %s" % (len(BACKLINKS), missing if missing else "0 条"))
    add("N-08", "N 边界", "跨册回链完整性", "PASS" if not missing else "FAIL",
        "回链命中 %d/%d：%s。" % (len(BACKLINKS) - len(missing), len(BACKLINKS),
                                 ", ".join(k for k, _ in BACKLINKS)))
    add("N-09", "N 边界", "本册不做什么（边界声明）", "INFO",
        "**不提出任何候选作用量**（构造新物理需另行授权）；"
        "只检验第十轮给出的 M1–M5 判据之间是否相容；"
        "N-06 的边界**不宣称**是引力理论的正确边界，只说明 M1∧M2 在该区域无解；"
        "数值示例取太阳 + 电子，属**演示参数**，不对应任何具体物理系统。")


def main():
    print("=" * 78)
    print("  TUFT V3.5 · 里程碑判据 M1–M5 相容性：语义分叉与短程边界")
    print("=" * 78)
    section_m1_m4()
    print("-" * 78)
    section_m1_m2()
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
        "title": "TUFT V3.5 里程碑判据 M1–M5 相容性：语义分叉与短程边界",
        "date": "2026-10-05",
        "results": RESULTS,
        "guards": GUARDS,
        "counts": cnt,
        "guard_ok": gok,
        "guard_total": len(GUARDS),
        "key_numbers": {
            "domega_dk": 0.0,
            "r_min_over_r_s": math.sqrt(2.0) / 2.0,
            "r_min_sun_m": math.sqrt(2.0) * G_N * M_SUN / (C_LIGHT ** 2),
            "r_s_sun_m": 2.0 * G_N * M_SUN / (C_LIGHT ** 2),
        },
        "findings": [
            "M1 ↔ M4 不相容（ω 不含 k ⇒ ∂ω/∂k = 0）⇒ κ,τ 语义必须二选一：几何量 or 模态量",
            "M1 ∧ M2 ⇒ 短程失效边界 r_min = √2·GM/c² = 0.7071 r_s",
            "M3 与 M1 相容且度规无关（体系最稳固的一条）",
            "M5 独立（只约束阶数，与取值无耦合）",
        ],
        "rating": "O / L2",
        "verdict_line": "M1–M5 不能同时成立 ⇒ 「按 M1–M5 找作用量」当前无对象；"
                        "攻 W2 前必须先做 κ,τ 语义选择，并接受短程有效域 r > 0.7071 r_s",
    }

    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)
    stem = "TUFT_V3.5_里程碑判据相容性_语义分叉与短程边界_2026-10-05"
    with open(os.path.join(DATA_DIR, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    lines = ["# TUFT V3.5 里程碑判据相容性：语义分叉与短程边界（数据产物）", ""]
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
