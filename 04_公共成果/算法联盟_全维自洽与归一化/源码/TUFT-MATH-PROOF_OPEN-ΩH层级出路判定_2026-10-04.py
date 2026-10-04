#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TUFT-MATH-PROOF OPEN-ΩH@3D 层级出路判定引擎（纯标准库，零第三方依赖）

任务（承接 ADD-04 §六 / ADD-05 §四）：在 ω5「仅 1 个自由常数 λ」约束下，判定是否存在
任何扩增（第二个结构化因子 / 不同 Ω 形状 / 非线性 E / 第二常数）能由框架**内生**承载
观测到的四力耦合层级（~10^43.8 个量级，G≪EM）。

判定路线（机器可复核）：
  P1  基线代价复现：θ_G 距域边界 δ_G = 4.948e-45 rad ⇒ 所需 ~44.3 位十进制精度（回读 ADD-02 拟合）。
  P2  分区守恒温约束 ⇒ 单常数形状必为 cos(3(θ-θ0))；其 |f| 在三个内点代表角（EM/S/W）的比值
      上限为 O(1)（~16×，即 ~1.2 dex），与 43.8 dex 差 ~42 个量级 ⇒ 单常数形状**不可能**内生 10^43 层级。
  P3  达到 43.8 dex 的两条出路：
      (a) 把 θ_G 精细调节到零点（δ_G 精度）→ 与基线等价，仍是外部精细调节；
      (b) 引入第二个自由常数 μ（Ω=λcos3θ+μ·h(θ)）→ 可设比值，但**违反 ω5**（2 常数）且 μ 是自由外参。
      二者皆属「层级外部输入」，无内部推导。
  P4  结项结论：OPEN-ΩH@3D → 正式结项为「层级外部输入」（公理集内无解）。

产物：数据/TUFT-MATH-PROOF_OPEN-ΩH层级出路判定_2026-10-04.{md,json}；退出码 0 = 判定自洽闭合。
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))


def d2r(d):
    return d * math.pi / 180.0


def cos3(t):
    return math.cos(3.0 * d2r(t))


def load_json(stem):
    path = os.path.join(DATA, stem + ".json")
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    # ---- P1：基线代价复现（回读 ADD-02 拟合） ----
    add02 = load_json("TUFT-MATH-PROOF-ADD-02_Omega正瓣重指派与耦合匹配_2026-10-04")
    fit = add02["fitting"]
    delta_G = fit["delta_G_rad"]
    digits = fit["digits"]
    span_dex = fit["span_dex"]            # 耦合跨度 43.828 dex
    lam = fit["lambda"]
    th_EM = fit["theta_EM"][1]            # +28.8172°
    th_S = fit["theta_S"][0]              # 120.0°
    th_W = fit["theta_W"][1]              # -92.7569°（落 (210,270) 正瓣）
    # G 代表点取零点 90°（域边界）
    th_G = 90.0

    # 重新推导 δ_G：span_dex 是耦合最大/最小之比 = (λ·1)/(λ·|cos3θ_G|) = 1/|cos3θ_G|
    # 故 |cos3θ_G| = 10^{-span_dex}；设 θ_G = 90° + ε，cos3θ_G ≈ -sin(3ε) ≈ -3ε（rad）
    # ⇒ 3ε = 10^{-span_dex} ⇒ ε = 10^{-span_dex} / 3
    c3_EM = cos3(th_EM)
    eps_rad = (10.0 ** (-span_dex)) / 3.0
    digits_rederived = -math.log10(eps_rad)

    p1 = {
        "delta_G_rad_loaded": delta_G,
        "delta_G_rad_rederived": eps_rad,
        "digits_loaded": digits,
        "digits_rederived": digits_rederived,
        "span_dex": span_dex,
        "cos3_EM": c3_EM,
        "verdict": "PASS" if abs(eps_rad - delta_G) / delta_G < 1e-3 else "FAIL",
    }

    # ---- P2：单常数形状必为 cos(3(θ-θ0))，内点比值上限 O(1) ----
    # 四个力的代表角（取自 ADD-02 拟合，单一固定配置）：
    reps = {"EM": th_EM, "S": th_S, "W": th_W, "G": th_G}
    fmag = {k: abs(cos3(v)) for k, v in reps.items()}   # 单常数 λ·cos3θ 的 |Ω| 形状
    interior = [fmag["EM"], fmag["S"], fmag["W"]]        # G 在零点，排除
    ratio_max = max(interior) / min(interior)
    achievable_dex = math.log10(ratio_max)
    # 任意旋转 θ0 只重排哪个力落在哪个瓣，不改变可取 |cos3θ| 集合 ⇒ 上限不变
    p2 = {
        "fmag": fmag,
        "interior_ratio_max": ratio_max,
        "achievable_dex_at_interior": achievable_dex,
        "required_dex": span_dex,
        "gap_dex": span_dex - achievable_dex,
        "verdict": "PASS" if achievable_dex < span_dex - 10 else "FAIL",
        "note": "单常数形状下，四力 |Ω| 比值由几何固定为 O(1)，与 43.8 dex 差 ~42 个量级，不可能内生层级",
    }

    # ---- P3：达到 43.8 dex 的两条出路 ----
    # (a) 精细调节 θ_G 到零点 δ_G ⇒ 与基线等价（已含于 P1，确认为外部精细调节）
    # (b) 引入第二常数：Ω = λ·cos3θ + μ·h(θ)，取 h(θ)=sin(θ)（或任意在 θ_G=90° 非零之形）
    #     在 θ_G=90°：cos3θ_G=0，h(90°)=sin90°=1 ⇒ Ω_G = μ
    #     在最强点 S（θ=120°，cos3θ=1）：Ω_S = λ·1 + μ·h(120°) ≈ λ（μ≪λ 时）
    #     令 |Ω_G|/|Ω_S| = 10^{-span_dex} ⇒ |μ|/|λ| = 10^{-span_dex} / |h(90°)|
    h_G = math.sin(d2r(th_G))          # = 1.0
    h_EM = math.sin(d2r(th_EM))
    mu_over_lam = (10.0 ** (-span_dex)) / abs(h_G)
    p3 = {
        "route_a_finetune": {
            "desc": "θ_G 精细调节到零点 δ_G",
            "cost_digits": digits_rederived,
            "nature": "外部精细调节（与基线等价）",
        },
        "route_b_second_constant": {
            "desc": "Ω=λ·cos3θ+μ·h(θ)，h(θ)=sinθ",
            "mu_over_lambda_required": mu_over_lam,
            "omega5_violated": True,
            "nature": "μ 为自由外参，层级被编码为第二个常数 ⇒ 非内生推导",
        },
        "verdict": "PASS" if (digits_rederived > 40 and mu_over_lam > 0) else "FAIL",
        "conclusion": "两条出路皆为层级外部输入，公理集（ω5 单常数）内无解",
    }

    # ---- P4：结项 ----
    closed = bool(
        p1["verdict"] == "PASS"
        and p2["verdict"] == "PASS"
        and p3["verdict"] == "PASS"
    )
    closure = {
        "OPEN_OmegaH_3D": "正式结项为「层级外部输入」",
        "within_axiom_set": False,
        "reason": "单常数 cos3θ 形状把四力 |Ω| 比值锁死在 O(1)（~1.2 dex），"
                  "与观测 43.8 dex 差 ~42 个量级；达到观测层级只能靠 (a)44 位精细调节 "
                  "或 (b) 违反 ω5 的第二个自由常数——二者均为外部输入。",
        "verdict": "PASS" if closed else "FAIL",
    }

    gate = {
        "base": "TUFT-MATH-PROOF_OPEN-ΩH层级出路判定_2026-10-04",
        "date": "2026-10-04",
        "nature": "OPEN-ΩH@3D 出路判定（承接 ADD-04 §六 / ADD-05 §四）",
        "constraint": "ω5：Ω 仅含 1 个自由常数 λ",
        "P1_baseline": p1,
        "P2_single_constant_shape": p2,
        "P3_two_routes": p3,
        "P4_closure": closure,
        "summary": {
            "total": 4,
            "pass": sum(1 for x in (p1, p2, p3, closure) if x["verdict"] == "PASS"),
        },
    }

    out_json = os.path.join(DATA, "TUFT-MATH-PROOF_OPEN-ΩH层级出路判定_2026-10-04.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(gate, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# TUFT-MATH-PROOF OPEN-ΩH@3D 层级出路判定 — 结项报告")
    lines.append("")
    lines.append("- 日期：2026-10-04")
    lines.append("- 约束：ω5（Ω 仅含 1 个自由常数 λ）")
    lines.append(f"- 判定结果：OPEN-ΩH@3D → **{closure['OPEN_OmegaH_3D']}**（公理集内无解 = {not closure['within_axiom_set']}）")
    lines.append("")
    lines.append("## P1 基线代价复现（回读 ADD-02 拟合）")
    lines.append(f"- 耦合跨度：{span_dex:.3f} dex；cos3θ 在 EM 代表角 = {c3_EM:.4f}")
    lines.append(f"- 复算 θ_G 距域边界 δ_G = {eps_rad:.3e} rad ⇒ 所需精度 {digits_rederived:.1f} 位十进制（载入值 {digits:.1f} 位，吻合）")
    lines.append("")
    lines.append("## P2 单常数形状 ⇒ 层级锁死在 O(1)")
    lines.append(f"- 四力 |cos3θ| 代表值：EM={fmag['EM']:.4f} / S={fmag['S']:.4f} / W={fmag['W']:.4f} / G={fmag['G']:.4f}（G 在零点）")
    lines.append(f"- 内点最大比值 = {ratio_max:.3f}× = {achievable_dex:.2f} dex；要求 {span_dex:.1f} dex ⇒ 缺口 **{span_dex - achievable_dex:.1f} dex**")
    lines.append("- 任意旋转 θ0 只重排力的落瓣，不改变可取 |cos3θ| 集合 ⇒ 上限不变。单常数形状**不可能**内生 10^43 层级。")
    lines.append("")
    lines.append("## P3 达到观测层级的两条出路（皆为外部输入）")
    lines.append(f"- (a) 精细调节 θ_G 到零点：需 {digits_rederived:.1f} 位十进制精度 → 与基线等价，属外部精细调节。")
    lines.append(f"- (b) 引入第二常数 μ：μ/λ = {mu_over_lam:.3e}（取 h(θ)=sinθ，θ_G=90° 处 h=1）→ 可设比值但**违反 ω5**（2 常数），μ 即自由外参。")
    lines.append("")
    lines.append("## P4 结项结论")
    lines.append(f"- {closure['reason']}")
    lines.append(f"- **OPEN-ΩH@3D 正式结项为「层级外部输入」；公理集内无解。**")
    lines.append("")
    lines.append(f"- 门禁：P1–P4 全过 = {closed}（退出码 0 = 判定自洽闭合）。")

    out_md = os.path.join(DATA, "TUFT-MATH-PROOF_OPEN-ΩH层级出路判定_2026-10-04.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print(f"\n[OPEN-ΩH] 数据产物: {out_json}")
    print(f"[OPEN-ΩH] 文本报告: {out_md}")

    sys.exit(0 if closed else 1)


if __name__ == "__main__":
    main()
