# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-电子反常磁矩 g-2  诚实审计（OPEN-5）
================================================================================
承接：白皮书 OPEN-5「电子 g-2：TUFT 给 α/(8π)，QED 给 α/(2π)，已被否决」。
本册把这句松散陈述升级为可复算的诚实审计。

事实链：
  (1) QED 反常磁矩（Schwinger 1951 主导项）： a = α/(2π) + 0.765(α/π)² + ...
      对电子 a_e，实验值 a_e^exp = 0.00115965218073(28)，与 QED 在 ~10^-12 吻合。
  (2) TUFT 体系对 g-2 的预言（白皮书 OPEN-5 记载）： a_TUFT = α/(8π)
      —— 即 α/(8π) = (1/4)·α/(2π)，是 QED 主导项的 1/4。
  (3) 诚实判定：TUFT 预言比 QED 主导项小 4 倍，相对实验值偏差约 75%
      （远超实验精度 10^-12）→ TUFT g-2 已被实验否决。

本审计只做数值与对比，不主张 TUFT 物理真实性。
红线：数学自洽 ≠ 实验证实；若预言与实验不符，诚实结论是理论失败。
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
REPORT_PATH = os.path.join(HERE, "tuft_g2_电子反常磁矩_OPEN5_report.txt")


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

    sec("TUFT-电子 g-2  诚实审计（OPEN-5）")
    put("  run at: " + __import__("time").strftime("%Y-%m-%d %H:%M:%S"))

    # ---- 物理常数（CODATA 近似，足够此处量级判断）
    ALPHA = 1.0 / 137.035999084          # 精细结构常数
    # 实验值 a_e（电子反常磁矩，无量纲），取自 CODATA / 2008 精度
    A_E_EXP = 0.00115965218073

    sec("1. 三路预言/数值精算")
    a_qed_leading = ALPHA / (2.0 * 3.141592653589793)        # QED Schwinger 项
    a_tuft = ALPHA / (8.0 * 3.141592653589793)               # TUFT 预言（白皮书 OPEN-5）
    put("  α = %.6e" % ALPHA)
    put("  QED 主导项 a_QED = α/(2π) = %.6e" % a_qed_leading)
    put("  TUFT 预言  a_TUFT = α/(8π) = %.6e" % a_tuft)
    put("  实验值    a_e     = %.6e (CODATA)" % A_E_EXP)
    rec("PASS", "TUFT 预言复算",
        "α/(8π) = %.3e，为 QED 主导项的 1/4（4 倍偏差）" % a_tuft)

    sec("2. 与 QED 主导项及实验的偏差")
    rel_vs_qed = (a_qed_leading - a_tuft) / a_qed_leading
    rel_vs_exp = (A_E_EXP - a_tuft) / A_E_EXP
    put("  TUFT vs QED 主导项：偏差 = %.2f%%" % (rel_vs_qed * 100))
    put("  TUFT vs 实验值    ：偏差 = %.2f%%" % (rel_vs_exp * 100))
    put("  QED 主导项 vs 实验 ：偏差 = %.3f%%（高阶项可补，吻合 ~10^-12）"
        % ((A_E_EXP - a_qed_leading) / A_E_EXP * 100))
    rec("INFO", "偏差量级",
        "TUFT 比实验小 4 倍（偏差 ~75%）；QED 主导项已与实验吻合到 10^-12 量级")

    sec("3. 诚实判定：TUFT g-2 是否被实验否决")
    # 实验对 a_e 的相对精度 ~ 10^-12（2008 CODATA ~2.4e-12）
    exp_precision = 2.4e-12
    if abs(rel_vs_exp) > 100 * exp_precision:
        verdict = "FAIL（被实验否决）"
        rec("FAIL", "OPEN-5 诚实结论",
            "TUFT 预言偏差 ~75%，超实验精度 ~10^11 倍 ⇒ TUFT g-2 已被实验否决")
    else:
        verdict = "PASS（未被排除）"
        rec("PASS", "OPEN-5 诚实结论", "TUFT 预言在实验误差内")

    sec("4. 可证伪窗口量化")
    put("  TUFT g-2 预言固定 = α/(8π)（由 α 导出，无自由参数）")
    put("  否决阈值 = 实验把 a_e 测到偏离 α/(8π) 之外（早已满足）")
    put("  当前实验 a_e 精度 ~10^-12，TUFT 偏差 ~75% ⇒ 窗口已闭合且 TUFT 在『被排除侧』")
    rec("INFO", "可证伪窗口状态",
        "窗口已闭合；TUFT g-2 落在被实验排除侧（与 EDM 同构）")

    sec("5. 与 EDM 攻破的合流（全维突破坐标）")
    rec("FAIL", "TUFT 第二个被实验关闭的窗口",
        "g-2（OPEN-5）与 EDM（OPEN-6）独立地从两个不同实验方向否决 TUFT")
    rec("INFO", "叠加意义",
        "g-2（电磁/圈图精度）与 EDM（CP 破坏/强约束）是两个独立的可证伪窗口，"
        "TUFT 在两者均落于被排除侧 ⇒ 不是『单一实验偏差』，而是系统性的实验失败")
    put("")
    put("  —— 本攻破把『TUFT g-2 < QED』的松散陈述升级为：")
    put("     (a) 用 CODATA 精算 a_TUFT = α/(8π) = %.3e；" % a_tuft)
    put("     (b) 对比 QED 主导项 α/(2π) = %.3e（4 倍关系）与实验 a_e = %.3e；" % (a_qed_leading, A_E_EXP))
    put("     (c) 诚实判据：TUFT 偏差 ~75%，超实验精度 ~10^11 倍 ⇒ 已被实验否决；")
    put("     (d) 与 EDM 攻破合流：TUFT 已有 2 个独立实验窗口被关闭。")

    sec("汇总")
    put("  PASS     = %d" % n_pass)
    put("  FAIL     = %d" % n_fail)
    put("  BOUNDARY = %d" % n_bound)
    put("  INFO     = %d" % n_info)
    put("")
    put("  a_TUFT(α/8π) = %.3e" % a_tuft)
    put("  a_QED (α/2π) = %.3e" % a_qed_leading)
    put("  a_e(exp)     = %.3e" % A_E_EXP)
    put("  偏差(TUFT/实验) = %.2f%%  ⇒ %s" % (rel_vs_exp * 100, verdict))
    put("")
    put("红线声明：数学自洽 != 实验证实。本审计只做数值对比；")
    put("诚实结论是 TUFT 电子 g-2 预言超实验值约 4 倍（偏差 ~75%），理论应被否决。")

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
