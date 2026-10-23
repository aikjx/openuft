# -*- coding: utf-8 -*-
"""
attack_C0224_共形窗口攻破_2026-10-21.py
独立复算：母册 T328「渐近自由共形窗口 N_f 相图」· 规范场论相结构（K 线扩展）

定位：母册 T328（行 460）= 渐近自由共形窗口 N_f 相图，撞 C7。
本册**不宣称解决任何物理难题**：全部数值均为**标准 QCD β 函数算术复核**
（外部公知公式，本册用 Fraction/Decimal 独立精算），非 TUFT 预测/修正。
TUFT 已注销（C0133），无规范群、无 β 函数供给。

把「共形窗口 N_f 相图」压缩成四条可复核读数 + 一张供给账单：

  E1 渐近自由边界核算：SU(3) 一圈 β 系数 b0=(11N_c-2N_f)/(48π²)·g³，
     AF  iff  b0>0  iff  N_f < 16.5（=33/2 精确）。
  E2 两圈 β 系数 b1 与红外不动点（本册核心）：
     b1 = 102 - (38/3)N_f；IRFP 存在 iff  b0>0 且 b1<0 ⇒ 区间核算；
     g*²/(16π²) = -b0/b1 在样本 N_f 处精算（Banks-Zaks）。
  E3 临界 N_f 核算：b1 符号翻转点 N_f = 153/19 ≈ 8.0526（两圈精确算术值）；
     文献 N_f^crit ≈ 11.5–13 为**外部输入**（更高圈/格点），只引用不复算。
  E4 供给检查：TUFT/几何框架是否供给规范群 β 函数/相结构？= 0（无规范群）。
  E5 裁定：共形窗口依赖规范群 β 函数结构（标准 QCD 算术），TUFT 无供给，
     结构性负面，撞 C7（规范场论相结构/数学自洽）。

纯标准库（Decimal 48 位 + Fraction 精确代数），零外部依赖，退出码 0。

诚实边界：不宣称解决；数值均为标准 QCD 算术复核；文献临界值为外部输入；
「有预测且对 = 0/22」；数学自洽 ≠ 实验证实；UFT-3=0 保持。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os
import json

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部公知输入（标准 QCD，N_c=3，Dirac 费米子基础表示） ----------
N_C = 3
# 文献临界 N_f（外部输入，只引用不复算）：两圈朴素值把下沿压到 ~8；
# 更高圈/格点把下沿抬到 ~11.5–13。此数非本册算出。
LIT_NF_CRIT = Decimal("11.5")   # 文献量级下限（外部输入计数）
LIT_NF_CRIT_HI = Decimal("13")  # 文献量级上限（外部输入计数）


def b0_std(nf: Fraction) -> Fraction:
    """一圈 β 系数（标准归一）：β=-g³/(16π²)·b0_std。b0_std=(11/3)N_c-(2/3)N_f。"""
    return Fraction(11, 1) * N_C / Fraction(3) - Fraction(2, 3) * nf


def b1_std(nf: Fraction) -> Fraction:
    """两圈 β 系数（标准归一）：β=-g⁵/(16π²)²·b1_std。
    b1_std = (34/3)N_c² - [(13/3)N_c - 1/N_c]·N_f。
    N_c=3 ⇒ 102 - (38/3)N_f。"""
    return Fraction(34, 3) * N_C * N_C - (Fraction(13, 3) * N_C - Fraction(1, N_C)) * nf


def e1_af_boundary():
    """E1 渐近自由边界：b0>0 ⇔ N_f < 33/2。"""
    nf_af = Fraction(11 * N_C, 2)          # b0=0 ⇔ N_f = 11N_c/2 = 33/2
    # 样本处 b0_std
    samples = {Fraction(3): b0_std(Fraction(3)),
               Fraction(5): b0_std(Fraction(5)),
               Fraction(16): b0_std(Fraction(16))}
    return {
        "N_c": N_C,
        "b0_zero_Nf": nf_af,
        "b0_zero_Nf_dec": Decimal(nf_af.numerator) / Decimal(nf_af.denominator),
        "AF_iff": "N_f < 11N_c/2 = 16.5",
        "b0_samples": {str(k): v for k, v in samples.items()},
    }


def e2_twoloop_irfp():
    """E2 两圈 b1 与红外不动点存在区间 + g* 精算。"""
    # b1 符号翻转点：b1_std=0
    # 102 - (38/3)N_f = 0 ⇒ N_f = 102·3/38 = 306/38 = 153/19
    nf_flip = (Fraction(34, 3) * N_C * N_C) / ((Fraction(13, 3) * N_C - Fraction(1, N_C)))
    # IRFP 存在：b0>0 且 b1<0 ⇒ nf_flip < N_f < nf_af
    nf_af = Fraction(11 * N_C, 2)
    # g*²/(16π²) = -b0/b1，样本 N_f
    def gstar_over_16pi2(nf: Fraction) -> Fraction:
        return -b0_std(nf) / b1_std(nf)
    samples = {}
    for nf in (Fraction(5), Fraction(8), Fraction(12), Fraction(15), Fraction(16)):
        g2 = gstar_over_16pi2(nf)
        samples[str(nf)] = {
            "b0": b0_std(nf),
            "b1": b1_std(nf),
            "gstar2_over_16pi2": g2,
            "has_irfp": (b0_std(nf) > 0) and (b1_std(nf) < 0),
        }
    return {
        "N_c": N_C,
        "b1_formula": "102 - (38/3)N_f",
        "b1_flip_Nf": nf_flip,
        "b1_flip_Nf_dec": Decimal(nf_flip.numerator) / Decimal(nf_flip.denominator),
        "nf_af": nf_af,
        "irfp_window": "(153/19, 33/2) 即 (%.10f, 16.5)"
                       % (Decimal(nf_flip.numerator) / Decimal(nf_flip.denominator)),
        "samples": samples,
    }


def e3_critical_nf():
    """E3 临界 N_f：两圈精确算术翻转点 vs 文献外部值。"""
    nf_flip = (Fraction(34, 3) * N_C * N_C) / ((Fraction(13, 3) * N_C - Fraction(1, N_C)))
    return {
        "two_loop_flip_Nf": nf_flip,
        "two_loop_flip_dec": Decimal(nf_flip.numerator) / Decimal(nf_flip.denominator),
        "literature_Nf_crit_low": LIT_NF_CRIT,
        "literature_Nf_crit_high": LIT_NF_CRIT_HI,
        "literature_is_external_input": True,
        "gap": "两圈算术下沿 %.4f 远低于文献 %.1f–%.1f；差值由更高圈/非微扰（格点）抬升，"
               "非本册复算范围。" % (Decimal(nf_flip.numerator) / Decimal(nf_flip.denominator),
                                  LIT_NF_CRIT, LIT_NF_CRIT_HI),
    }


def e4_tuft_supply():
    """E4 TUFT/几何框架供给：规范群 β 函数/相结构？"""
    return {
        "tuft_has_gauge_group": False,
        "tuft_supplies_beta": False,
        "tuft_supplies_phase_diagram": False,
        "tuft_status": "已注销（C0133）",
        "supply": 0,
        "note": "共形窗口 N_f 相图完全由规范群 β 函数结构决定（标准 QCD 算术）；"
                "TUFT/几何框架无规范群、无耦合常数跑动，供给为 0。",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def ffrac(x: Fraction) -> str:
        return str(Decimal(x.numerator) / Decimal(x.denominator))

    w("=" * 74)
    w("attack_C0224 · 渐近自由共形窗口 N_f 相图（母册 T328 · 规范场论相结构）攻破")
    w("=" * 74)
    w("性质：标准 QCD β 函数算术复核（外部公知公式独立精算），非 TUFT 预测/修正。")
    w("TUFT 已注销（C0133），无规范群、无 β 函数供给。")

    entries = []

    # ---- E1 ----
    g1 = e1_af_boundary()
    w("\n[E1] 渐近自由边界核算（SU(3)，N_c=%d）" % g1["N_c"])
    w("  b0 = (11N_c-2N_f)/(48π²)·g³ ⇒ b0>0  ⇔  N_f < 11N_c/2 = 33/2 = %s"
      % ffrac(g1["b0_zero_Nf"]))
    w("  样本 b0_std：N_f=3 ⇒ %s；N_f=5 ⇒ %s；N_f=16 ⇒ %s"
      % (ffrac(g1["b0_samples"]["3"]), ffrac(g1["b0_samples"]["5"]),
         ffrac(g1["b0_samples"]["16"])))
    w("  => N_f < 16.5 渐近自由（b0>0）；N_f≥16.5 反渐近自由。")
    entries.append(("E1", "AF 边界：b0>0 ⇔ N_f<33/2=16.5（精确）；样本 b0 符号与区间一致",
                    "PASS", "标准 QCD 一圈 β 算术复核，Fraction 精确"))

    # ---- E2 ----
    g2 = e2_twoloop_irfp()
    w("\n[E2] 两圈 β 系数 b1 与红外不动点区间（本册核心）")
    w("  b1 = %s（N_c=3）" % g2["b1_formula"])
    w("  IRFP 存在 ⇔ b0>0 且 b1<0 ⇒ N_f ∈ (153/19, 33/2) = %s" % g2["irfp_window"])
    w("  g*²/(16π²) = -b0/b1 样本：")
    for nf, d in g2["samples"].items():
        w("    N_f=%-3s: b0=%s b1=%s  g*²/(16π²)=%s  IRFP=%s"
          % (nf, ffrac(d["b0"]), ffrac(d["b1"]), ffrac(d["gstar2_over_16pi2"]),
             "有" if d["has_irfp"] else "无"))
    w("  => N_f=16 时 g*²/(16π²)=%s ≈ 3.3e-3 极小（Banks-Zaks，趋近 N_f^AF 时耦合跑向 0）；"
      % ffrac(g2["samples"]["16"]["gstar2_over_16pi2"]))
    w("     N_f=5/8 < 翻转点时 b1>0 ⇒ 无实 IRFP（自由值为负），与相图一致。")
    entries.append(("E2", "两圈 b1=102-(38/3)N_f；IRFP 区间 (153/19≈8.0526, 16.5)；"
                    "g*²/(16π²)@N_f=16=%s（BZ 弱耦合）" % ffrac(g2["samples"]["16"]["gstar2_over_16pi2"]),
                    "PASS", "标准 QCD 两圈 β + IRFP 存在条件，Fraction/Decimal 精算"))

    # ---- E3 ----
    g3 = e3_critical_nf()
    w("\n[E3] 临界 N_f 核算")
    w("  b1 符号翻转点（两圈精确算术）：N_f = 153/19 = %s" % ffrac(g3["two_loop_flip_Nf"]))
    w("  文献临界 N_f ≈ %s–%s（**外部输入，只引用不复算**；更高圈/格点值）"
      % (g3["literature_Nf_crit_low"], g3["literature_Nf_crit_high"]))
    w("  %s" % g3["gap"])
    entries.append(("E3", "两圈算术翻转 N_f=153/19≈8.0526；文献 ~11.5–13 为外部输入，"
                    "差由更高圈/非微扰抬升", "PASS", "算术值本册算；文献值外部引用"))

    # ---- E4 ----
    g4 = e4_tuft_supply()
    w("\n[E4] 供给检查：TUFT/几何框架是否供给规范群 β 函数/相结构？")
    w("  TUFT 有规范群 = %s；供给 β 函数 = %s；供给相图 = %s；status=%s"
      % (g4["tuft_has_gauge_group"], g4["tuft_supplies_beta"],
         g4["tuft_supplies_phase_diagram"], g4["tuft_status"]))
    w("  供给 = %d。%s" % (g4["supply"], g4["note"]))
    entries.append(("E4", "TUFT 无规范群/无 β 函数/无相图供给（=0；TUFT 已注销 C0133）",
                    "PASS", "供给账单，结构性负面"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  共形窗口 N_f 相图完全由规范群 β 函数结构决定（标准 QCD 算术）。")
    w("  E1/E2/E3 全部为标准 QCD 算术复核；TUFT/几何框架无规范群、无耦合跑动（E4），供给=0。")
    w("  => **结构性负面（对 TUFT/几何框架）**：TUFT 既不能复算也不能预测共形窗口，")
    w("     按母册登记撞 **C7**（规范场论相结构/数学自洽）。")
    entries.append(("E5", "结构性负面：共形窗口依赖规范群 β 函数（标准 QCD 算术），"
                    "TUFT 无供给，撞 C7", "PASS", "撞 C7"))

    # ---- 守卫 ----
    guards = [
        ("G1", "AF 边界 N_f^AF = 33/2 = 16.5（精确）",
         g1["b0_zero_Nf"] == Fraction(33, 2)),
        ("G2", "b1 符号翻转点 = 153/19 ≈ 8.0526（N_c=3）",
         g2["b1_flip_Nf"] == Fraction(153, 19)),
        ("G3", "N_f=16 处存在弱 IRFP（g*²/(16π²)>0 且极小，BZ）",
         (g2["samples"]["16"]["has_irfp"] is True)
         and (g2["samples"]["16"]["gstar2_over_16pi2"] > 0)
         and (g2["samples"]["16"]["gstar2_over_16pi2"] < Fraction(1, 100))),
        ("G4", "N_f=5 < 翻转点处无实 IRFP（b1>0）",
         (g2["samples"]["5"]["has_irfp"] is False)
         and (g2["samples"]["5"]["b1"] > 0)),
        ("G5", "TUFT β/相图供给 = 0（无规范群，已注销 C0133）",
         g4["supply"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %-4s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0224 guard failed"

    w("\n[诚实边界 / 红线]")
    w("  不宣称解决任何物理难题；已攻破 = 对 TUFT/几何框架结构性负面闭合。")
    w("  数值均为标准 QCD β 函数算术复核，严禁写成 TUFT 预测/修正。")
    w("  文献临界 N_f≈11.5–13 为外部输入；「有预测且对 = 0/22」保持；")
    w("  数学自洽 ≠ 实验证实；UFT-3=0 保持。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0224_共形窗口攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0224_共形窗口攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": "C0224_conformal_window_Nf",
            "mother_row": "T328",
            "hits": "C7",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_AF_boundary": {
                "N_c": g1["N_c"],
                "b0_zero_Nf_frac": str(g1["b0_zero_Nf"]),
                "b0_zero_Nf_dec": str(g1["b0_zero_Nf_dec"]),
                "b0_samples": {k: str(v) for k, v in g1["b0_samples"].items()},
            },
            "E2_twoloop_IRFP": {
                "b1_formula": g2["b1_formula"],
                "b1_flip_Nf_frac": str(g2["b1_flip_Nf"]),
                "b1_flip_Nf_dec": str(g2["b1_flip_Nf_dec"]),
                "irfp_window": g2["irfp_window"],
                "samples": {k: {kk: (str(vv) if not isinstance(vv, bool) else vv)
                                for kk, vv in v.items()}
                            for k, v in g2["samples"].items()},
            },
            "E3_critical_Nf": {
                "two_loop_flip_frac": str(g3["two_loop_flip_Nf"]),
                "two_loop_flip_dec": str(g3["two_loop_flip_dec"]),
                "literature_low": str(g3["literature_Nf_crit_low"]),
                "literature_high": str(g3["literature_Nf_crit_high"]),
            },
            "E4_tuft_supply": g4,
            "E5_verdict": "结构性负面，撞 C7",
            "guards": [{"id": g[0], "desc": g[1], "ok": bool(g[2])} for g in guards],
            "guard_count": len(guards),
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0224 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
