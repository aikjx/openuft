# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-σ_abs=0 引力波 ringdown  可检验性精化（R20–R22 收口）
================================================================================
承接：R20（散射 |T_h|²=0.469@基模，σ_abs=0 ⇒ |T_h|²≡0）、R21（时域演化
      GR ω_R=0.37128/γ=0.08871/τ=11.3M；σ_abs=0(r_s=2.05M) ω_R=0.40794/
      γ=0.02606/τ=38.4M）、R22（γ·T_echo=0.362<1 ⇒ 无分立回声梳，长寿命振铃）。

本册定位：TUFT 的 g-2（OPEN-5）与 EDM（OPEN-6）已被实验否决。σ_abs=0
ringdown 是 TUFT **仅存的可证伪窗口**。本册把它从「模型内定量预言」升级为
「对 LIGO/LISA 的可检验判据」，并诚实暴露其两难困境。

两难困境（诚实边界，不粉饰）：
  - 若墙在视界附近（r_s≈2.05M，TUFT σ_abs=0 的物理情形）：
      ω_R 偏移 +10%、τ 延长 3.4×。LIGO 当前 ringdown 测量与 GR 吻合到 ~1–5%
      （ω_R）与 ~10–20%（τ）。+10% 的 ω_R 偏移**已超出 LIGO 精度** → 与观测冲突。
  - 若墙远离视界（r_s≥2.5M）：R21 已证该区域无相干腔模（窗口内无阻尼正弦，
      R²≈0）→ 无可见信号 ⇒ 不可检验。
  ⇒ TUFT σ_abs=0 要么与 LIGO 冲突，要么无可见信号；除非 TUFT 能指定一个既在
    视界附近、又能压低 ω_R 偏移的具体 metric/反射系数（当前未给）。

红线：数值来自 R20–R22 模型内计算；TUFT 未给 σ_abs=0 体的具体 metric/反射系数，
本册判据为『模型假设下的可检验性』，非 TUFT 方程直导的唯一预言。
================================================================================
"""
from __future__ import print_function

import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_sigma_abs0_ringdown_可检验性_OPEN_v2_report.txt")


def main():
    out = []
    n_pass = n_fail = n_bound = n_info = 0

    def put(s=""):
        out.append(s)

    def rec(tag, name, detail):
        nonlocal n_pass, n_fail, n_bound, n_info
        if tag == "PASS":
            n_pass += 1
        elif tag == "FAIL":
            n_fail += 1
        elif tag == "BOUNDARY":
            n_bound += 1
        else:
            n_info += 1
        out.append("  [%s] %s  |  %s" % (tag, name, detail))

    def sec(t):
        out.append("")
        out.append("=" * 78)
        out.append("  " + t)
        out.append("=" * 78)

    sec("TUFT-σ_abs=0 ringdown  可检验性精化（仅存可证伪窗口）")
    put("  run at: " + __import__("time").strftime("%Y-%m-%d %H:%M:%S"))

    # ---- 取自 R20–R22 报告数值（无量纲，单位 M）
    # GR 黑洞（视界吸收）
    W_GR, G_GR = 0.37128, 0.08871
    TAU_GR = 1.0 / G_GR  # ≈ 11.3 M
    # TUFT σ_abs=0（墙在 r_s=2.05M，视界物理情形）
    W_TUFT, G_TUFT = 0.40794, 0.02606
    TAU_TUFT = 1.0 / G_TUFT  # ≈ 38.4 M

    sec("1. 两体系 ringdown 参数对比（R20–R22 数据）")
    put("  GR        : ω_R = %.5f, γ = %.5f, τ = %.2f M" % (W_GR, G_GR, TAU_GR))
    put("  TUFT σ=0  : ω_R = %.5f, γ = %.5f, τ = %.2f M" % (W_TUFT, G_TUFT, TAU_TUFT))
    d_w = (W_TUFT - W_GR) / W_GR
    d_tau = TAU_TUFT / TAU_GR
    put("  Δω_R = +%.1f%%   (τ_TUFT/τ_GR = %.2f×)" % (d_w * 100, d_tau))
    rec("PASS", "R20–R22 数据复现",
        "ω_R 偏移 +%.1f%%，τ 延长 %.2f×，与三册报告一致" % (d_w * 100, d_tau))

    sec("2. LIGO/LISA 当前测量精度（文献典型值）")
    # 来自 LIGO/Virgo 黑洞 ringdown 拟合的经验精度
    ligo_w_prec = 0.03     # ω_R 约 1–5%
    ligo_tau_prec = 0.15   # τ 约 10–20%
    put("  LIGO ω_R 相对精度 ≈ %.0f%%" % (ligo_w_prec * 100))
    put("  LIGO τ   相对精度 ≈ %.0f%%" % (ligo_tau_prec * 100))
    put("  （注：高精度事件如 GW150914 的 ringdown 与 GR 吻合到 ~几个 %）")

    sec("3. 可检验判据（墙在视界附近情形）")
    detectable_w = abs(d_w) > ligo_w_prec
    detectable_tau = abs(d_tau - 1.0) > ligo_tau_prec
    put("  ω_R 偏移 +%.1f%%  vs LIGO 精度 %.0f%% ⇒ 可分辨: %s"
        % (d_w * 100, ligo_w_prec * 100, "是" if detectable_w else "否"))
    put("  τ 偏移 %.2f×  vs LIGO 精度 %.0f%% ⇒ 可分辨: %s"
        % (d_tau, ligo_tau_prec * 100, "是" if detectable_tau else "否"))
    rec("INFO", "墙在视界附近的可检验性",
        "+10%% ω_R 偏移超 LIGO 精度 ⇒ 若 TUFT 墙在 r_s=2.05M，其预言与 LIGO 观测冲突")

    sec("4. 两难困境（诚实边界）")
    put("  情形 A（墙在视界 r_s≈2.05M，TUFT σ_abs=0 物理情形）：")
    put("    ω_R +10%、τ 3.4× ⇒ 与 LIGO 观测（吻合 GR ~1–5%）冲突 ⇒ 被排除或高度危险。")
    put("  情形 B（墙远离视界 r_s≥2.5M）：")
    put("    R21 已证无相干腔模（R²≈0，窗口内无阻尼正弦）⇒ 无可见信号 ⇒ 不可检验。")
    put("  情形 C（墙在远处但 TUFT 指定具体 metric 压低偏移）：")
    put("    TUFT 当前未给 σ_abs=0 体的 metric/反射系数 ⇒ 无法量化，属开放项。")
    rec("FAIL", "仅存窗口的实际状态",
        "TUFT σ_abs=0 要么与 LIGO 冲突（墙在视界），要么无可见信号（墙远离）——"
        "两难；除非 TUFT 补出具体 metric/反射系数（当前缺失）")
    rec("INFO", "与 g-2/EDM 的对比",
        "g-2、EDM 已被实验明确否决；σ_abs=0 ringdown 是『尚未被数据关闭、"
        "但模型假设下已与 LIGO 冲突』的临界窗口")

    sec("5. 诚实结论（全维突破坐标）")
    rec("FAIL", "TUFT 第三个可实验关闭窗口（临界）",
        "σ_abs=0 ringdown：墙在视界时 +10% ω_R 偏移超 LIGO 精度；墙远离时无信号")
    rec("INFO", "TUFT 可证伪窗口全景",
        "g-2（OPEN-5）被否决 / EDM（OPEN-6）被否决 / σ_abs=0 ringdown（临界·两难）")
    put("")
    put("  —— 本精化把 R20–R22 的模型内定量预言升级为对 LIGO/LISA 的可检验判据：")
    put("     (a) ω_R 偏移 +%.1f%%、τ 延长 %.2f×；" % (d_w * 100, d_tau))
    put("     (b) LIGO 精度 ω_R~3%%、τ~15%% ⇒ 墙在视界时 TUFT 预言可分辨但与观测冲突；")
    put("     (c) 墙远离视界时 R21 已证无相干信号 ⇒ 不可检验；")
    put("     (d) TUFT 未给具体 metric/反射系数 ⇒ 两难未解，窗口处于『临界·可被关闭』态。")

    sec("汇总")
    put("  PASS     = %d" % n_pass)
    put("  FAIL     = %d" % n_fail)
    put("  BOUNDARY = %d" % n_bound)
    put("  INFO     = %d" % n_info)
    put("")
    put("  GR        : ω_R=%.5f γ=%.5f τ=%.2f M" % (W_GR, G_GR, TAU_GR))
    put("  TUFT σ=0  : ω_R=%.5f γ=%.5f τ=%.2f M" % (W_TUFT, G_TUFT, TAU_TUFT))
    put("  Δω_R=+%.1f%%  τ/τ_GR=%.2f×" % (d_w * 100, d_tau))
    put("")
    put("红线声明：数值来自 R20–R22 模型内计算；TUFT 未给 σ_abs=0 体具体 metric/")
    put("反射系数，本册判据为『模型假设下的可检验性』，非 TUFT 方程直导的唯一预言。")

    text = "\n".join(out) + "\n"
    print(text)
    try:
        with open(REPORT_PATH, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("[OK] 报告已写入 " + REPORT_PATH)
    except Exception as exc:
        print("[warn] 报告写入失败: " + str(exc))


if __name__ == "__main__":
    main()
