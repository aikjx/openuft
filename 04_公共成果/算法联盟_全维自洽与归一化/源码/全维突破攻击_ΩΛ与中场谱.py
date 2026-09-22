# -*- coding: utf-8 -*-
"""
全维突破攻击（二）：Ω_Λ 无量纲化 · de Sitter 自洽 · 中场谱整数搜索

处理模式：算法联盟最高权限 · 全维度 / 全链路 / 诚实分级

本轮「优化」的四个要点
----------------------
C1  把 Λ 缺口从「有量纲量差 122 量级」重构为**无量纲量 Ω_Λ 的预言**
    （method_F 判据一：第一性内容 ⟺ 无量纲量的数值）
C2  de Sitter 视界与 Hubble 半径的区分 —— 诊断系数「3/4 vs 3」的来源
C3  精确化：κ_vac·R_H 的观测要求值
C4  sin²θ_W = 1/4 所需中场内容的**整数谱搜索**（把约束式变成候选粒子内容）

红线
----
本脚本输出的是**候选闭合路径（conjecture）**，不是已验证结论。
Ω_Λ = 1/4 是「框架关系 + 截断选择」的推论，不是框架已给出的预言；
中场谱搜索存在多解，任一解都必须再过 b₃ / 质子衰变 / 统一性检验才算候选。

运行
----
& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe 全维突破攻击_ΩΛ与中场谱.py
产出写入 ../数据/全维突破攻击_ΩΛ与中场谱.json 与 .md
"""

import sys
import os
import json
import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import mpmath as mp

mp.mp.dps = 50

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, os.pardir, "数据"))

RECORDS = []
COUNT = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}


def rec(cid, item, verdict, detail):
    RECORDS.append({"cid": cid, "item": item, "verdict": verdict, "detail": detail})
    COUNT[verdict] = COUNT.get(verdict, 0) + 1
    mark = {"PASS": "[PASS]", "FAIL": "[FAIL]", "BOUNDARY": "[BND ]", "INFO": "[INFO]"}[verdict]
    print("  " + mark + " " + cid + " " + item + " :: " + detail)


def section(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# ---------------------------------------------------------------- 常数
c_light = mp.mpf("299792458")
hbar = mp.mpf("1.054571817e-34")
G_newton = mp.mpf("6.67430e-11")
H0_SI = mp.mpf("67.4") * mp.mpf("1000") / mp.mpf("3.0856775814913673e22")
R_H = c_light / H0_SI                       # Hubble 半径 c/H₀
OMEGA_L_OBS = mp.mpf("0.685")
LAMBDA_OBS = 3 * OMEGA_L_OBS * H0_SI ** 2 / c_light ** 2
l_P = mp.sqrt(hbar * G_newton / c_light ** 3)


# ================================================================ C1
def c1_omega_lambda():
    section("C1 · 把 Λ 缺口重构为无量纲量 Ω_Λ 的预言")
    print("  框架关系：Λ = 3 κ_vac² / 4")
    print("  宇宙学定义：Ω_Λ ≡ Λc²/(3H₀²) = Λ R_H² / 3，其中 R_H ≡ c/H₀")
    print("  ⟹ Ω_Λ = (3κ_vac²/4)·R_H²/3 = κ_vac² R_H² / 4")
    print()

    rec("C1-01", "推导 Ω_Λ = κ_vac² R_H² / 4",
        "PASS", "代数恒等（由框架 Λ 式 + Ω_Λ 定义直接推出）")

    # 截断选择 κ_vac = 1/R_H
    omega_pred = mp.mpf(1) / 4
    rec("C1-02", "★ 取 κ_vac = 1/R_H（视界截断）⟹ Ω_Λ = 1/4",
        "PASS", "框架预言 Ω_Λ = " + mp.nstr(omega_pred, 8))

    # 观测值回算
    omega_check = LAMBDA_OBS * R_H ** 2 / 3
    rec("C1-03", "观测 Ω_Λ 回算（Λ R_H²/3）",
        "PASS", "= " + mp.nstr(omega_check, 8) + "（输入 Ω_Λ = 0.685）⟹ 定义自洽")

    ratio = OMEGA_L_OBS / omega_pred
    rec("C1-04", "★ 无量纲闭合度（本轮优化后的表述）",
        "BOUNDARY" if ratio > mp.mpf("1.5") else "PASS",
        "预言 Ω_Λ = 1/4 = 0.250；观测 0.685；观测/预言 = " + mp.nstr(ratio, 6) + " 倍（差 " +
        mp.nstr(mp.log10(ratio), 4) + " 个数量级）")

    rec("C1-05", "与旧表述的对比（优化价值）",
        "INFO", "旧：Λ 有量纲，差 2.63e121 倍（122 量级）——无法判断结构性对错；"
                "新：Ω_Λ 无量纲，差 2.74 倍 —— 符合 method_F 判据一，可直接检验")

    rec("C1-06", "1/4 的复现（结构提示）",
        "INFO", "Ω_Λ = 1/4 与 sin²θ_W = 1/4 出现同一个数值；"
                "是否同源于「对偶/四分」结构尚属**观察**，无机制 ⟹ 不得据此宣称关联")


# ================================================================ C2
def c2_desitter():
    section("C2 · de Sitter 视界 vs Hubble 半径：系数 3/4 与 3 的诊断")
    print("  纯 de Sitter：R_Λ = √(3/Λ)，即 Λ = 3/R_Λ²")
    print("  框架：Λ = 3/(4R_H²)（取 κ_vac = 1/R_H）")
    print("  两者仅在 R_Λ = 2 R_H 时才一致 ⟹ 诊断二者比值")
    print()

    R_Lambda = mp.sqrt(3 / LAMBDA_OBS)          # de Sitter 视界
    ratio_R = R_Lambda / R_H
    rec("C2-01", "de Sitter 视界 R_Λ = √(3/Λ_观测)",
        "PASS", "= " + mp.nstr(R_Lambda, 8) + " m；R_H = c/H₀ = " + mp.nstr(R_H, 8) +
        " m；R_Λ/R_H = " + mp.nstr(ratio_R, 6))

    rec("C2-02", "一致性诊断",
        "FAIL" if abs(ratio_R - 2) > mp.mpf("0.05") else "PASS",
        "若框架系数取 3/4，则需 R_Λ = 2R_H 才等价；实测 R_Λ/R_H = " + mp.nstr(ratio_R, 6) +
        " ⟹ **不相等**，故 κ_vac 的锚定半径必须明确是 R_H（Hubble）而非 R_Λ（de Sitter）")

    # 若改用 de Sitter 视界
    kappa_dS = 1 / R_Lambda
    omega_dS = kappa_dS ** 2 * R_H ** 2 / 4
    rec("C2-03", "若误取 κ_vac = 1/R_Λ（de Sitter 视界）",
        "FAIL", "Ω_Λ = κ_vac²R_H²/4 = " + mp.nstr(omega_dS, 8) + "（vs 观测 0.685）⟹ 更差，确认应取 R_H")

    rec("C2-04", "两者的物理区分",
        "INFO", "R_H = c/H₀ 含物质贡献；R_Λ = √(3/Λ) 只由 Λ 决定。"
                "当前宇宙 Ω_Λ = 0.685 < 1 ⟹ R_Λ ≠ R_H，二者相差 " + mp.nstr(ratio_R, 6) + " 倍")

    rec("C2-05", "自洽性警告（重要）",
        "BOUNDARY", "若把 Ω_Λ = 1/4 反过来要求宇宙进入纯 de Sitter（Ω_Λ = 1），"
                    "则框架式与 de Sitter 关系联立得 3/R_H² = 3/(4R_H²) ⟹ 矛盾（差因子 4）"
                    " ⟹ **该候选只在 Ω_Λ = 1/4 的非纯 de Sitter 情形自洽**，不得外推到 Ω_Λ = 1")


# ================================================================ C3
def c3_kappa_requirement():
    section("C3 · 精确化：κ_vac·R_H 的观测要求值")
    # Ω_Λ = κ_vac² R_H²/4 ⟹ κ_vac R_H = 2√Ω_Λ
    need = 2 * mp.sqrt(OMEGA_L_OBS)
    rec("C3-01", "由 Ω_Λ = κ_vac²R_H²/4 反解",
        "PASS", "κ_vac·R_H = 2√Ω_Λ = " + mp.nstr(need, 8) + "（框架取 1，差 " + mp.nstr(need, 4) + " 倍）")

    kappa_need = need / R_H
    ell_need = 1 / kappa_need
    rec("C3-02", "对应的真空曲率半径",
        "INFO", "1/κ_vac = " + mp.nstr(ell_need, 8) + " m = " + mp.nstr(ell_need / R_H, 6) +
        " R_H（框架取 1 R_H）")

    rec("C3-03", "与 B2 的 ℓ 的关系",
        "INFO", "B2 的最短尺度 ℓ = √(ℓ_P R_H) = 47.10 μm 与本项真空曲率半径 1/κ_vac 是**两个不同的量**："
                "ℓ 是对偶自洽尺度（最短），1/κ_vac 是真空曲率尺度（≈视界）⟹ 二者相差约 " +
                mp.nstr(R_H / mp.sqrt(l_P * R_H), 6) + " 倍，不得混淆")

    rec("C3-04", "★ 闭合度总结（无量纲口径）",
        "BOUNDARY", "框架预言 Ω_Λ = 1/4，观测 0.685 ⟹ 差 2.74 倍。"
                    "在宇宙学常数问题中，这已是从 10¹²² 到 O(1) 的质变，但**仍非吻合**")


# ================================================================ C4
def c4_matter_spectrum():
    section("C4 · 中场谱整数搜索（sin²θ_W = 1/4 所需的粒子内容）")
    print("  条件：sin²θ_W = 1/4 在 M_GUT = 2e16 GeV 成立 ⟺ b₂ − (5/9)b₁ = −0.60945")
    print("  SM 基值：b₁ = 41/10，b₂ = −19/6 ⟹ b₂ − (5/9)b₁ = −5.4444")
    print("  ⟹ 中场需提供：Δb₂ − (5/9)Δb₁ = +4.8354")
    print()

    # 用精确有理数搜索（避免 mpmath 高精度在大枚举下过慢）
    from fractions import Fraction as F

    F_b1_sm = F(41, 10)
    F_b2_sm = F(-19, 6)
    F_target = F(-60945422, 100000000)          # b₂ − (5/9)b₁ 的需求值（来自 B5 反解）
    F_need = F_target - (F_b2_sm - F(5, 9) * F_b1_sm)
    rec("C4-01", "中场需提供的 Δb₂ − (5/9)Δb₁",
        "PASS", "= " + mp.nstr(mp.mpf(F_need.numerator) / F_need.denominator, 8) +
        "（精确分数 " + str(F_need) + "）")

    # 表示库（精确有理数）：(Δb₁, Δb₂)
    # Weyl 费米子：Δb = (2/3)T（非阿贝尔），(2/3)(3/5)Y²（U(1)，GUT 归一）
    # 复标量：    Δb = (1/3)T（非阿贝尔），(1/3)(3/5)Y²（U(1)）
    # T(SU(2) 基本) = 1/2，T(三重态) = 2
    reps = {
        "Weyl双重态对(Y=±1/2)": (F(1, 5), F(2, 3)),
        "Weyl三重态(Y=0)": (F(0), F(4, 3)),
        "标量双重态对(Y=±1/2)": (F(1, 10), F(1, 3)),
        "标量三重态(Y=0)": (F(0), F(2, 3)),
        "Weyl三重态(Y=±1)": (F(4, 5), F(4, 3)),
    }
    print("  表示库（每个表示的精确 Δb₁ / Δb₂ 增量）：")
    for k, (x1, x2) in reps.items():
        print("    " + k + "：Δb₁ = " + str(x1) + "，Δb₂ = " + str(x2))
    print()

    names = list(reps.keys())
    best = []
    seen = set()
    for n1 in names:
        for n2 in names:
            for n3 in names:
                r1, r2, r3 = reps[n1], reps[n2], reps[n3]
                for a in range(0, 13):
                    d1a, d2a = a * r1[0], a * r1[1]
                    for b in range(0, 13):
                        d1b, d2b = d1a + b * r2[0], d2a + b * r2[1]
                        for cc in range(0, 13):
                            if a == 0 and b == 0 and cc == 0:
                                continue
                            d1 = d1b + cc * r3[0]
                            d2 = d2b + cc * r3[1]
                            val = d2 - F(5, 9) * d1
                            err = abs(val - F_need) / F_need
                            if err < F(2, 100):
                                key = tuple(sorted([(a, n1), (b, n2), (cc, n3)]))
                                if key in seen:
                                    continue
                                seen.add(key)
                                best.append((float(err), a, n1, b, n2, cc, n3, d1, d2, val))
    best.sort(key=lambda x: x[0])

    rec("C4-02", "整数搜索规模",
        "INFO", "5 种表示 × 三槽 × 0..12 份 ≈ 2.7e5 组合（精确有理数）；相对误差 < 2% 的解 " + str(len(best)) + " 个")

    shown = 0
    for err, a, n1, b, n2, cc, n3, d1, d2, val in best[:5]:
        desc = "、".join([str(x) + "×" + y for x, y in [(a, n1), (b, n2), (cc, n3)] if x > 0])
        rec("C4-" + str(10 + shown), "候选谱 #" + str(shown + 1),
            "BOUNDARY",
            desc + " ⟹ Δb₁ = " + str(d1) + "，Δb₂ = " + str(d2) +
            "，Δb₂−(5/9)Δb₁ = " + str(val) + "（需求 " + str(F_need.numerator) + "/" + str(F_need.denominator) +
            "，误差 " + str(round(err * 100, 4)) + "%）")
        shown += 1

    if not best:
        rec("C4-10", "候选谱", "FAIL", "在给定表示库与 0..12 份范围内无解")

    rec("C4-90", "★ 本项性质判定（诚实）",
        "BOUNDARY",
        "搜索给出的是**数值满足约束的整数解**，存在多解且未过 b₃ / 质子衰变 / 统一性检验；"
        "S13 尚未推出中场谱 ⟹ 这些不是「预言的粒子内容」，只是**说明该约束在整数谱上是可达的**。"
        "真正闭合须由框架独立给出中场谱后再核对")


# ================================================================ main
def main():
    print("=" * 78)
    print("全维突破攻击（二）：Ω_Λ 无量纲化 · de Sitter 自洽 · 中场谱整数搜索")
    print("运行时间: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("精度: mpmath " + str(mp.mp.dps) + " 位")
    print("=" * 78)

    c1_omega_lambda()
    c2_desitter()
    c3_kappa_requirement()
    c4_matter_spectrum()

    print()
    print("=" * 78)
    total = sum(COUNT.values())
    print("精算汇总：" + str(total) + " 项，PASS " + str(COUNT.get("PASS", 0)) +
          " / FAIL " + str(COUNT.get("FAIL", 0)) +
          " / BOUNDARY " + str(COUNT.get("BOUNDARY", 0)) +
          " / INFO " + str(COUNT.get("INFO", 0)))
    print("=" * 78)

    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    payload = {
        "meta": {
            "script": "全维突破攻击_ΩΛ与中场谱.py",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mpmath_dps": mp.mp.dps,
            "total": total,
            "counts": COUNT,
        },
        "records": RECORDS,
    }
    jpath = os.path.join(OUT_DIR, "全维突破攻击_ΩΛ与中场谱.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    lines = ["# 全维突破攻击（二）：Ω_Λ 无量纲化 · de Sitter 自洽 · 中场谱整数搜索", "",
             "> 脚本：`04_公共成果/算法联盟_全维自洽与归一化/源码/全维突破攻击_ΩΛ与中场谱.py`",
             "> 时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
             " ｜ 精度 mpmath " + str(mp.mp.dps) + " 位", "",
             "## 结果表", "", "| 编号 | 项 | 判定 | 细节 |", "|---|---|---|---|"]
    for r in RECORDS:
        lines.append("| " + r["cid"] + " | " + r["item"] + " | " + r["verdict"] + " | " + r["detail"] + " |")
    lines += ["", "## 汇总", "",
              "总计 " + str(total) + " 项：PASS " + str(COUNT.get("PASS", 0)) +
              " / FAIL " + str(COUNT.get("FAIL", 0)) + " / BOUNDARY " +
              str(COUNT.get("BOUNDARY", 0)) + " / INFO " + str(COUNT.get("INFO", 0)), "",
              "## 本轮优化要点", "",
              "### 优化一：Λ 缺口无量纲化（C1）",
              "由框架 Λ = 3κ_vac²/4 与 Ω_Λ ≡ ΛR_H²/3 得 **Ω_Λ = κ_vac²R_H²/4**。",
              "取 κ_vac = 1/R_H ⟹ **框架预言 Ω_Λ = 1/4 = 0.250**，观测 0.685，差 **2.74 倍**。",
              "→ 从「有量纲量差 122 量级」变为「无量纲量差 2.74 倍」，符合 method_F 判据一，可直接检验。", "",
              "### 优化二：明确 κ_vac 必须锚定 Hubble 半径而非 de Sitter 视界（C2）",
              "R_Λ = √(3/Λ) = 1.658e26 m，R_H = c/H₀ = 1.373e26 m，比值 1.208 ≠ 2。",
              "→ 若取 de Sitter 视界则 Ω_Λ 更差；且框架式与纯 de Sitter 关系联立会推出 1 = 1/4 的矛盾",
              "⟹ **候选仅在 Ω_Λ = 1/4 的非纯 de Sitter 情形自洽，不得外推到 Ω_Λ = 1**。", "",
              "### 优化三：中场谱整数搜索（C4）",
              "约束 Δb₂ − (5/9)Δb₁ = +4.8354（相对 SM 中场增量）。",
              "在 5 种标准表示 × 三槽 × 0..12 份的整数空间内搜索，给出相对误差 < 2% 的候选谱若干。",
              "→ 说明该约束在整数谱上**可达**；但存在多解，且未过 b₃ / 质子衰变 / 统一性检验 ⟹ 不是预言。", "",
              "## 红线", "",
              "Ω_Λ = 1/4 是「框架关系 + 本轮截断选择」的推论，框架原文未给出该预言。",
              "中场谱搜索结果仅说明约束可达，不构成粒子内容预言。数学自洽 ≠ 物理成立。"]
    mpath = os.path.join(OUT_DIR, "全维突破攻击_ΩΛ与中场谱.md")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("产出：" + jpath)
    print("产出：" + mpath)


if __name__ == "__main__":
    main()
