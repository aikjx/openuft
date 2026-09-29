# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-EDM  实验对接（OPEN-6）：诚实攻破
================================================================================
承接：白皮书第82章 4.1「EDM 实验对接（OPEN-6）：把 S13/S14 登记的电子 EDM
      预言精算到可提交实验对比的精度，与 ACME 等上限比对。全书唯一可立即
      被实验否决的窗口。」

TUFT 体系的电子 EDM 预言（S13/S14 登记）：
    d_e = e * α * R_C / (2 * sqrt(1 + α^2))
其中 R_C 在 TUFT 体系下是『粒子=闭合光速螺旋结』的几何半径，量级取
康普顿半径 ℏ/(m_e c)（经典电子半径的 ~1/α ≈ 137 倍），这正是 TUFT 预言
数值 2.257e-34 C·m 的来源（用经典半径会小 137 倍，得 1.6e-36，对不上）。

本攻破做『诚实』实验对接：
  (1) 用 CODATA 实算 d_e，并换算到 EDM 实验界通用的 e·cm 单位；
  (2) 用【真实】ACME 2018 上限 |d_e| < 1.1e-29 e·cm 对比；
  (3) 同时列出白皮书引用的『ACME 8.7e-34 C·m』口径，揭示其单位/量级矛盾；
  (4) 给出诚实判据：预言是否落在可证伪窗口内、是否已被实验否决。

红线：本脚本只做数值与单位换算，不主张 TUFT 物理真实性；若预言>实验上限，
      诚实结论是『TUFT 被电子 EDM 实验否决』，这正是 OPEN-6 要暴露的事实。
================================================================================
"""
from __future__ import print_function

import os
import sys
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_EDM_实验对接_OPEN6_report.txt")


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

    # ---- CODATA 常数
    C = 299792458.0
    HBAR = 1.054571817e-34
    M_E = 9.1093837015e-31
    E = 1.602176634e-19
    ALPHA = 7.2973525693e-3

    sec("TUFT-EDM  实验对接（OPEN-6）：诚实攻破")
    put("  run at: " + __import__("time").strftime("%Y-%m-%d %H:%M:%S"))
    put("  红线：只做数值/单位换算；若预言>实验上限，诚实结论=理论被否决。")

    # ============================================================= 1. TUFT 预言精算
    sec("1. TUFT 电子 EDM 预言精算（CODATA，复算 S13/S14 登记值）")
    r_c_tuft = HBAR / (M_E * C)                 # 康普顿半径：TUFT 几何半径
    put("  R_C(TUFT) = ℏ/(m_e c) = %.6e m  （康普顿半径；经典半径 = %.3e m，差 1/α≈137 倍）"
        % (r_c_tuft, E ** 2 / (4.0 * math.pi * 8.8541878128e-12 * M_E * C ** 2)))
    d_e_tuft = E * ALPHA * r_c_tuft / (2.0 * math.sqrt(1.0 + ALPHA ** 2))
    # 换算到 e·cm：1 C·m = (1/1.602e-19) e · 100 cm = 6.2415e20 e·cm
    C_M_TO_E_CM = 1.0 / (E * 1e-2)
    d_e_tuft_e_cm = d_e_tuft * C_M_TO_E_CM
    put("  d_e(TUFT) = e·α·R_C / (2√(1+α²))")
    put("           = %.4e C·m" % d_e_tuft)
    put("           = %.4e e·cm" % d_e_tuft_e_cm)
    rec("PASS" if abs(d_e_tuft - 2.257e-34) / 2.257e-34 < 0.02 else "FAIL",
        "复算 S13/S14 登记值",
        "得 %.3e C·m，对照登记 2.257e-34（偏差 %.2f%%）" %
        (d_e_tuft, (d_e_tuft - 2.257e-34) / 2.257e-34 * 100))

    # ============================================================= 2. 真实实验上限
    sec("2. 真实实验上限（ACME 2018，e·cm 国际通用单位）")
    acme_2018_e_cm = 1.1e-29                      # |d_e| < 1.1 × 10^{-29} e·cm
    acme_2018_c_m = acme_2018_e_cm / C_M_TO_E_CM  # 换算回 C·m
    put("  ACME 2018 (HUDSON et al., Science 364, 2019): |d_e| < 1.1e-29 e·cm")
    put("            = %.3e C·m" % acme_2018_c_m)
    # 后续实验（ACME III 预研 / 其他分子）想把上限再压 1~2 个数量级，量级同阶
    put("  近期竞争实验目标：~1e-30 ~ 1e-31 e·cm（同量级收紧，不推翻此处结论）")

    # ============================================================= 3. 白皮书引用口径
    sec("3. 白皮书引用的『ACME 8.7e-34 C·m』口径（揭示矛盾）")
    acme_wrong_c_m = 8.7e-34
    acme_wrong_e_cm = acme_wrong_c_m * C_M_TO_E_CM
    put("  白皮书写：d_e(TUFT)=2.257e-34 C·m < ACME 8.7e-34 C·m ⇒ 未排除")
    put("  换算 8.7e-34 C·m 到 e·cm = %.3e e·cm" % acme_wrong_e_cm)
    put("  真实 ACME 2018 上限 = 1.1e-29 e·cm = %.3e e·cm" % acme_2018_e_cm)
    ratio_wrong = acme_wrong_e_cm / acme_2018_e_cm
    put("  ⇒ 白皮书引用的上限比真实 ACME 宽松 %.1e 倍（~16 个量级）" % ratio_wrong)
    rec("FAIL", "白皮书对比数字可疑",
        "8.7e-34 C·m 若按 e·cm 换算为 %.1e e·cm，比真实 ACME 上限 1.1e-29 e·cm 宽松 16 个量级" %
        acme_wrong_e_cm)

    # ============================================================= 4. 诚实判定
    sec("4. 诚实判定：TUFT 是否被电子 EDM 实验否决")
    ratio_vs_acme = d_e_tuft_e_cm / acme_2018_e_cm
    put("  d_e(TUFT) / |d_e|_ACME2018 = %.2e" % ratio_vs_acme)
    if ratio_vs_acme > 1.0:
        verdict = "FAIL（被实验否决）"
        rec("FAIL", "OPEN-6 诚实结论",
            "TUFT 预言 %.2e e·cm 超真实 ACME 上限 1.1e-29 e·cm 达 %.1e 倍 ⇒ TUFT 已被电子 EDM 实验否决"
            % (d_e_tuft_e_cm, ratio_vs_acme))
    else:
        verdict = "PASS（未被排除）"
        rec("PASS", "OPEN-6 诚实结论",
            "TUFT 预言未超真实 ACME 上限")

    # 白皮书口径下（仅作对照，不采纳）
    ratio_vs_wrong = d_e_tuft / acme_wrong_c_m
    put("  [对照·不采纳] 白皮书口径：d_e/8.7e-34 = %.3f ⇒ 该口径下『未排除』但数字本身存疑"
        % ratio_vs_wrong)

    # 可证伪窗口量化
    sec("5. 可证伪窗口量化")
    # TUFT 预言固定 2.26e-34 C·m；实验上限压到该值以下即否决 TUFT
    kill_threshold_e_cm = d_e_tuft_e_cm
    put("  TUFT 预言固定 ≈ %.2e e·cm（由 α, m_e, ℏ, c 导出，无自由参数）" % d_e_tuft_e_cm)
    put("  否决阈值 = 实验把 |d_e| 上限压到 < %.2e e·cm" % kill_threshold_e_cm)
    put("  当前 ACME 2018 上限 = 1.1e-29 e·cm（已远低于 TUFT 预言 %.1e 倍）" % ratio_vs_acme)
    rec("INFO", "可证伪窗口状态",
        "窗口已『闭合且 TUFT 落在被排除侧』：非『待检验』，而是『已被检验并否决』")

    sec("6. 诚实结论（攻破坐标）")
    rec("FAIL", "OPEN-6 攻破结果",
        "TUFT 电子 EDM 预言 2.26e-34 C·m 超真实 ACME 2018 上限 16 个量级 ⇒ 理论被实验否决")
    rec("INFO", "与白皮书矛盾",
        "白皮书『未被排除』建立在可疑的 8.7e-34 C·m 对比数字上；按标准实验单位 TUFT 已失败")
    rec("INFO", "加固边界而非推翻",
        "这恰是 OPEN-6 的价值：暴露 TUFT/螺旋纲领在电子 EDM 上的硬性实验失败，"
        "与 g-2（OPEN-5，TUFT α/(8π) vs QED α/(2π) 已被否决）同属『可被实验关闭』的窗口")
    put("")
    put("  —— 本攻破把『TUFT EDM 预言』从一句『< ACME 上限』的宽松陈述，升级为：")
    put("     (a) 用 CODATA 实算 d_e = %.3e C·m = %.3e e·cm；" % (d_e_tuft, d_e_tuft_e_cm))
    put("     (b) 对比真实 ACME 2018 上限 1.1e-29 e·cm = %.2e C·m；" % acme_2018_c_m)
    put("     (c) 暴露白皮书引用的 8.7e-34 C·m 比真实上限宽松 16 个量级；")
    put("     (d) 诚实判据：TUFT 已被电子 EDM 实验否决（与 g-2 否决同构）。")
    put("  ⇒ OPEN-6 的『可立即被实验否决的窗口』——已被实验否决，窗口关闭。")

    # ---- 汇总
    sec("汇总")
    put("  PASS     = %d" % n_pass)
    put("  FAIL     = %d" % n_fail)
    put("  BOUNDARY = %d" % n_bound)
    put("  INFO     = %d" % n_info)
    put("")
    put("  TUFT d_e = %.3e C·m = %.3e e·cm" % (d_e_tuft, d_e_tuft_e_cm))
    put("  ACME2018 = 1.1e-29 e·cm = %.3e C·m" % acme_2018_c_m)
    put("  比值     = %.2e  ⇒ %s" % (ratio_vs_acme, verdict))
    put("")
    put("红线声明：数学自洽 != 实验证实。本攻破只做数值/单位换算；诚实结论是")
    put("TUFT 电子 EDM 预言超真实实验上限约 16 个数量级，理论应被否决。")

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
