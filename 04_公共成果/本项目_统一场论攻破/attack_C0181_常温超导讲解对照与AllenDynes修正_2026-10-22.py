# -*- coding: utf-8 -*-
"""
attack_C0181 · 常温超导「大白话讲解」对照审计 + Allen-Dynes f1 指数修正与攻破整理
================================================================================
来料：一份《常温超导 · 大白话全维度全链路讲解》（本质/空间结构/公式链/实验/采购/产业 + HTML 图）
      其自称口径取自库内攻破册 C0153（BCS 普适比 1.764、H3S 217.1 K、LaH10 260.7 K）
      + C0159（求导值 pi/e^gamma = 1.763877）+ 三条 2025-2026 外部进展。

本册只做三件事（不改物理结论，只改读数与公式实现）：
    A 段  BCS 弱耦合普适比：核验讲解的等号链与库内锚点是否自洽
    B 段  【承重】Allen-Dynes 强耦合修正 f1 的指数口径：库内引擎实现 vs 标准形式 vs 讲解写法
    C 段  讲解中其它可机器核验的读数（声子频段、温标、相干长度、参数口径、弱耦合近似）
    D 段  讲解中库内无记载的外部事实（[C] 级登记，不复算不代证）
    E 段  裁定 + 修正后读数表 + 治理登记

红线：本册不宣称解决/解释常温超导；实验 Tc/压力值只引用不复算；
      裁的是「讲解与库内册是否一致、库内引擎实现是否合标准式」，
      不是氢化物物理本身对错；TUFT/几何框架超导供给 = 0 维持不变。
"""
import sys
import json
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

BASE = r"d:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_统一场论攻破"
STEM = "attack_C0181_常温超导讲解对照与AllenDynes修正_2026-10-22"

# ---- 高精度常数（CODATA 口径，60 位足够）----
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494")
EULER = Decimal("0.57721566490153286060651209008240243104215933593992359880577")
KB = Decimal("1.380649e-23")        # J/K
HBAR = Decimal("1.054571817e-34")   # J*s

# ---- 库内 C0153 引擎中心参数（逐字取自 attack_C0153_*.py）----
H3S = {"lam": Decimal("2.2"), "wlog": Decimal("1250"), "mustar": Decimal("0.13")}
LAH10 = {"lam": Decimal("3.5"), "wlog": Decimal("1000"), "mustar": Decimal("0.12")}
EXP_H3S = Decimal("203")    # K @155 GPa（只引用）
EXP_LAH10 = Decimal("250")  # K @170 GPa（只引用）
BOX_H3S = {"lam": [Decimal("2.0"), Decimal("2.5")],
           "wlog": [Decimal("1100"), Decimal("1400")],
           "mustar": [Decimal("0.10"), Decimal("0.16")]}
BOX_LAH10 = {"lam": [Decimal("3.1"), Decimal("3.9")],
             "wlog": [Decimal("800"), Decimal("1200")],
             "mustar": [Decimal("0.10"), Decimal("0.15")]}

_entries = []
_guards = []


def add(code, status, title, detail):
    _entries.append({"code": code, "status": status, "title": title, "detail": detail})


def guard(name, desc, ok):
    _guards.append({"name": name, "desc": desc, "ok": bool(ok)})


def fv(x, spec="6f"):
    """Decimal -> 定点字符串（不用 quantize，避免高位数 InvalidOperation）"""
    try:
        return format(Decimal(x), "." + spec)
    except Exception:
        return str(x)


def fs(x, n=6):
    return format(Decimal(x), "." + str(n) + "E")


def droot(x, n):
    """x^(1/n) for Decimal（Py3.8 Decimal 无分数幂，走 ln/exp）"""
    return (Decimal(x).ln() / Decimal(n)).exp()


# ============================================================
# A 段 · BCS 弱耦合普适比（核验讲解的等号链）
# ============================================================
def seg_a():
    r_pi_eg = PI / EULER.exp()                      # 求导值 pi/e^gamma
    anchor_1 = Fraction(1000, 567)                  # 库内 C0153 锚点 1000/567
    anchor_2 = Fraction(2000, 567)                  # 2 倍 = 2*Delta0/(kB*Tc) 锚点
    r_1134 = Decimal(2) / Decimal("1.134")          # 库内 C0153 的 2/1.134

    d_abs = abs(r_pi_eg - Decimal(anchor_1.numerator) / Decimal(anchor_1.denominator))
    d_rel = d_abs / r_pi_eg

    add("A01", "PASS", "BCS 弱耦合求导值 pi/e^gamma 精算",
        "pi/e^gamma = %s（求导值）；2Delta0/(kB Tc) = %s"
        % (fv(r_pi_eg, "10f"), fv(r_pi_eg * 2, "10f")))

    add("A02", "PASS", "库内 C0153 锚点 1000/567 与求导值一致（4 位有效数字）",
        "1000/567 = %s；2/1.134 = %s；与 pi/e^gamma 绝对差 %s、相对差 %s"
        % (fv(Decimal(anchor_1.numerator) / Decimal(anchor_1.denominator), "10f"),
           fv(r_1134, "10f"), fs(d_abs, 4), fs(d_rel, 4)))

    add("A03", "PASS", "2Delta0/(kB Tc) 锚点应为 2000/567",
        "2000/567 = %s（≈3.528）；1000/567 = %s（≈1.764）——两者是 2 倍关系，不是等号"
        % (fv(Decimal(anchor_2.numerator) / Decimal(anchor_2.denominator), "10f"),
           fv(Decimal(anchor_1.numerator) / Decimal(anchor_1.denominator), "10f")))

    # 讲解写法：2Delta0/(kB Tc) = 2/1.134 = 1000/567 = 3.527337
    lhs = Decimal("3.527337")
    mid = Decimal(anchor_1.numerator) / Decimal(anchor_1.denominator)  # 1.7637
    gap = abs(mid - lhs)
    add("A04", "CORRECTED",
        "讲解的普适比等号链在数值上不成立（等式链混写两个量）",
        "讲解原文写 2Delta0/(kB Tc) = 2/1.134 = 1000/567 = 3.527337；"
        "其中 1000/567 = %s，与 3.527337 相差 %s（恰为 2 倍关系，即把单比值当成了双比值）。"
        "正确写法：Delta0/(kB Tc) = 2/1.134 = 1000/567 = %s；"
        "2Delta0/(kB Tc) = 2000/567 = %s。"
        "【错源定位】该写法逐字来自库内《常温超导_全维分析与全链路总览》§四 第 1 层"
        "（该册写 2Delta0/(kB Tc) = 1000/567 = 3.527337），而 C0153 判定册 §二(a) 是分开写的（正确）"
        "⇒ 库内两册互不一致，讲解照抄总览册，非讲解原创错误。末位结论 3.528 不受影响。"
        % (fv(mid, "10f"), fv(gap, "10f"),
           fv(mid, "10f"),
           fv(Decimal(anchor_2.numerator) / Decimal(anchor_2.denominator), "10f")))

    add("A05", "INFO", "库内两册在普适比上无冲突（C0153 锚点 / C0159 求导值并列登记）",
        "C0153 用 Fraction 锚点 1000/567=1.763668；C0159 用求导值 pi/e^gamma=%s；"
        "两者在 4 位有效数字上同为 1.764，C0159 已显式并列登记，非冲突。"
        % fv(r_pi_eg, "10f"))

    guard("G1", "pi/e^gamma 落 [1.7638,1.7639] 且与 1000/567 相对差 < 2e-4",
          Decimal("1.7638") < r_pi_eg < Decimal("1.7639") and d_rel < Decimal("2e-4"))
    guard("G2", "2Delta0/(kB Tc)：求导值 3.527754 与锚点 3.527337 相对差 < 5e-4",
          abs(r_pi_eg * 2 - Decimal(anchor_2.numerator) / Decimal(anchor_2.denominator))
          / (r_pi_eg * 2) < Decimal("5e-4"))
    guard("G3", "抓到讲解等号链错误：|1000/567 - 3.527337| > 1（确为 2 倍量级错写）",
          gap > Decimal("1"))
    return {"pi_over_e_gamma": r_pi_eg, "anchor_1": str(anchor_1), "anchor_2": str(anchor_2),
            "chain_gap": gap}


# ============================================================
# B 段 ·【承重】Allen-Dynes 强耦合修正 f1 的指数口径
# ============================================================
def mcmillan_tc(wlog, lam, mustar):
    """Tc = (wlog/1.2) * exp[-1.04(1+lam)/(lam - mu*(1+0.62 lam))]"""
    num = Decimal("1.04") * (1 + lam)
    den = lam - mustar * (1 + Decimal("0.62") * lam)
    return (wlog / Decimal("1.2")) * (-(num / den)).exp()


def ad_f1(lam, mustar, root_n):
    """f1 = [1 + (lam/Lam1)^{3/2}]^{1/root_n}，Lam1 = 2.46(1+3.8 mu*)
    root_n=2 -> 库内 C0153 引擎实现（(.sqrt())，即 1/2 次方）
    root_n=3 -> Allen-Dynes (1975) 标准形式（1/3 次方）"""
    lam1 = Decimal("2.46") * (1 + Decimal("3.8") * mustar)
    r = lam / lam1
    return droot(1 + r ** Decimal("1.5"), root_n)


def ad_tc(p, root_n):
    f1 = ad_f1(p["lam"], p["mustar"], root_n)
    f2 = Decimal("1")  # 与 C0153 同口径：omega2=omega_log 取 f2=1（诚实边界）
    return f1 * f2 * mcmillan_tc(p["wlog"], p["lam"], p["mustar"]), f1, f2


def box_scan(box, root_n):
    out = []
    for la in box["lam"]:
        for wl in box["wlog"]:
            for mu in box["mustar"]:
                tc, _, _ = ad_tc({"lam": la, "wlog": wl, "mustar": mu}, root_n)
                out.append(tc)
    return min(out), max(out)


def seg_b():
    tc_h_lib, f1_h_lib, _ = ad_tc(H3S, 2)
    tc_l_lib, f1_l_lib, _ = ad_tc(LAH10, 2)
    tc_h_std, f1_h_std, _ = ad_tc(H3S, 3)
    tc_l_std, f1_l_std, _ = ad_tc(LAH10, 3)
    mc_h = mcmillan_tc(H3S["wlog"], H3S["lam"], H3S["mustar"])
    mc_l = mcmillan_tc(LAH10["wlog"], LAH10["lam"], LAH10["mustar"])

    add("B01", "PASS", "Allen-Dynes (1975) 标准形式：f1 = [1+(lam/Lam1)^{3/2}]^{1/3}",
        "库内《常温超导_核心公式理论体系》§4.2.2 与 §七 环10 均写作 1/3 次方，"
        "与 Allen & Dynes 1975 标准式一致；讲解 HTML 中亦写作 1/3（与标准式一致）。")

    add("B02", "FAIL",
        "库内 C0153/C0159 引擎实现为 f1 = [1+(lam/Lam1)^{3/2}]^{1/2}（指数错）",
        "attack_C0153_*.py 第 119 行 f1 = (1 + r ** Decimal('1.5')).sqrt()，"
        "即 1/2 次方而非标准式的 1/3 次方；判定册 §二(c) 与报告 [E2b/c] 亦随引擎写作 1/2。"
        "C0159 复算沿用同一实现（f1=1.2096 / 1.4021），故两册同源同错。"
        "这是本册唯一承重缺陷：它不是笔误级，而是让 Tc 系统性高估。")

    add("B03", "FAIL", "f1 两口径数值对照（库内 1/2 vs 标准 1/3）",
        "H3S：f1(1/2)=%s vs f1(1/3)=%s（比 %s）；"
        "LaH10：f1(1/2)=%s vs f1(1/3)=%s（比 %s）"
        % (fv(f1_h_lib, "4f"), fv(f1_h_std, "4f"), fv(f1_h_lib / f1_h_std, "4f"),
           fv(f1_l_lib, "4f"), fv(f1_l_std, "4f"), fv(f1_l_lib / f1_l_std, "4f")))

    add("B04", "FAIL", "Tc 两口径数值对照（同一组中心参数、同一 f2=1）",
        "H3S：McMillan 底值 %s K → AD(库内 1/2) %s K → AD(标准 1/3) %s K；"
        "LaH10：McMillan 底值 %s K → AD(库内 1/2) %s K → AD(标准 1/3) %s K"
        % (fv(mc_h, "1f"), fv(tc_h_lib, "1f"), fv(tc_h_std, "1f"),
           fv(mc_l, "1f"), fv(tc_l_lib, "1f"), fv(tc_l_std, "1f")))

    dev_h_lib = (tc_h_lib - EXP_H3S) / EXP_H3S
    dev_h_std = (tc_h_std - EXP_H3S) / EXP_H3S
    dev_l_lib = (tc_l_lib - EXP_LAH10) / EXP_LAH10
    dev_l_std = (tc_l_std - EXP_LAH10) / EXP_LAH10
    add("B05", "CORRECTED", "与实验对照：修正后 H3S 更吻合、LaH10 由高估翻转为低估",
        "H3S 对 203 K：库内口径偏差 %s（高估）；标准口径偏差 %s（几乎正中）。"
        "LaH10 对 ~250 K：库内口径偏差 %s（高估）；标准口径偏差 %s（低估）。"
        "⇒ 库内「两体系均与实验同量级且落区间」的判读在修正后方向性改变，"
        "但「是否落区间」这一判据本身不变（见 B06）。"
        % (fs(dev_h_lib, 3), fs(dev_h_std, 3), fs(dev_l_lib, 3), fs(dev_l_std, 3)))

    in_h_std = Decimal("180") <= tc_h_std <= Decimal("220")
    in_l_std = Decimal("230") <= tc_l_std <= Decimal("280")
    add("B06", "PASS", "区间判据不翻转（C0153 的 E2 PASS 结论在修正后仍成立）",
        "H3S 标准口径 %s K ∈[180,220] = %s；LaH10 标准口径 %s K ∈[230,280] = %s。"
        "⇒ 修正不改变 C0153 的 E2「落区间」判定与 E5「T594 结构性负面」裁定，"
        "只改变『偏差方向与量级』这一描述层读数。"
        % (fv(tc_h_std, "1f"), in_h_std, fv(tc_l_std, "1f"), in_l_std))

    add("B07", "MISMATCH", "讲解的公式写对、数值来源错（内部不自洽）",
        "讲解第 3 层写 f1 = [1+(lam/Lam1)^{3/2}]^{1/3}（标准式，对），"
        "但表格数值 217.1 K / 260.7 K 取自库内 C0153 引擎（1/2 次方实现）。"
        "按讲解自己写的公式复算应为 %s K / %s K。"
        "⇒ 讲解须二选一：要么数值改 %s/%s K（推荐，与实验更自洽），"
        "要么把公式改成 1/2 并显式说明偏离标准式（不推荐）。"
        % (fv(tc_h_std, "1f"), fv(tc_l_std, "1f"), fv(tc_h_std, "1f"), fv(tc_l_std, "1f")))

    bmin_h_2, bmax_h_2 = box_scan(BOX_H3S, 2)
    bmin_h_3, bmax_h_3 = box_scan(BOX_H3S, 3)
    bmin_l_2, bmax_l_2 = box_scan(BOX_LAH10, 2)
    bmin_l_3, bmax_l_3 = box_scan(BOX_LAH10, 3)
    add("B08", "CORRECTED", "参数盒随 f1 口径同步修正（C6 证据不变，区间收窄）",
        "H3S 盒：库内口径 %s–%s K → 标准口径 %s–%s K；"
        "LaH10 盒：库内口径 %s–%s K → 标准口径 %s–%s K。"
        "⇒ 摆动仍达数倍量级，C6（无可靠误差带）结论不受影响、反而更硬。"
        % (fv(bmin_h_2, "0f"), fv(bmax_h_2, "0f"), fv(bmin_h_3, "0f"), fv(bmax_h_3, "0f"),
           fv(bmin_l_2, "0f"), fv(bmax_l_2, "0f"), fv(bmin_l_3, "0f"), fv(bmax_l_3, "0f")))

    add("B09", "INFO", "f1 指数是比 mu*/omega_log 更便宜的系统性偏差源（本册新读数）",
        "仅把指数由 1/2 改为 1/3，H3S Tc 变化 %s、LaH10 变化 %s；"
        "而 mu* 摆动 ±0.03 对 Tc 的影响约 ±15 K（理论册 §6.3 口径）。"
        "⇒ 在引用任何解析式 Tc 前，应先核对 f1 的指数实现，再谈参数敏感性。"
        % (fs(tc_h_lib / tc_h_std - 1, 3), fs(tc_l_lib / tc_l_std - 1, 3)))

    guard("G4", "复现库内 f1 值 1.2096 / 1.4021（1/2 口径）",
          abs(f1_h_lib - Decimal("1.2096")) < Decimal("5e-4")
          and abs(f1_l_lib - Decimal("1.4021")) < Decimal("5e-4"))
    guard("G5", "复现库内 Tc 值 217.1 / 260.7 K（1/2 口径）",
          abs(tc_h_lib - Decimal("217.1")) < Decimal("0.5")
          and abs(tc_l_lib - Decimal("260.7")) < Decimal("0.5"))
    guard("G6", "标准 1/3 口径下 f1 单调性仍成立：f1(LaH10)>f1(H3S)>1",
          f1_l_std > f1_h_std > Decimal("1"))
    guard("G7", "修正后两体系仍各自落区间（C0153 区间判据不翻转）", in_h_std and in_l_std)
    guard("G8", "参数盒在两口径下均为数倍摆动（C6 证据稳健）",
          bmax_h_3 / bmin_h_3 > Decimal("1.5") and bmax_l_3 / bmin_l_3 > Decimal("1.5"))
    return {"f1_h_lib": f1_h_lib, "f1_l_lib": f1_l_lib,
            "f1_h_std": f1_h_std, "f1_l_std": f1_l_std,
            "tc_h_lib": tc_h_lib, "tc_l_lib": tc_l_lib,
            "tc_h_std": tc_h_std, "tc_l_std": tc_l_std,
            "box_h_std": [bmin_h_3, bmax_h_3], "box_l_std": [bmin_l_3, bmax_l_3],
            "box_h_lib": [bmin_h_2, bmax_h_2], "box_l_lib": [bmin_l_2, bmax_l_2],
            "dev_h_std": dev_h_std, "dev_l_std": dev_l_std,
            "dev_h_lib": dev_h_lib, "dev_l_lib": dev_l_lib}


# ============================================================
# C 段 · 讲解中其它可机器核验的读数
# ============================================================
def seg_c():
    # C01 声子频段：omega_log（以 K 给出，即 hbar*omega/kB）→ 频率
    f1250 = KB * Decimal("1250") / HBAR / (2 * PI)
    f1000 = KB * Decimal("1000") / HBAR / (2 * PI)
    f300 = KB * Decimal("300") / HBAR / (2 * PI)
    add("C01", "CORRECTED", "讲解的声子频段口径偏低约 1 个量级（未声明是常规金属还是氢化物）",
        "讲解写「声子 omega ~ 10^12–10^13 Hz（太赫兹）」。按库内中心参数换算："
        "omega_log=1250 K → %s Hz（%.2f THz）；1000 K → %s Hz（%.2f THz）；"
        "常规金属 omega_log~300 K → %s Hz（%.2f THz）。"
        "⇒ 10^12–10^13 是常规金属口径，氢化物应为 ~2×10^13 Hz；讲解未声明口径，"
        "按氢化物读则偏低约 1 个量级。【错源】该行逐字来自库内总览册 §三 3.1 表（同口径）。"
        % (fs(f1250, 4), float(f1250) / 1e12, fs(f1000, 4), float(f1000) / 1e12,
           fs(f300, 4), float(f300) / 1e12))

    # C02 温标换算
    tbl = [(Decimal("250"), "-23.15"), (Decimal("203"), "-70.15"),
           (Decimal("134"), "-139.15"), (Decimal("271"), "-2.15"),
           (Decimal("298"), "24.85")]
    txt = "；".join(["%s K = %s ℃" % (fv(k, "0f"), c) for k, c in tbl])
    add("C02", "CORRECTED", "温标换算：讲解的「-135℃」与库内常压纪录 134 K 不吻合（差 4 K）",
        "机器换算：%s。讲解第〇表写铜氧化物「常压需要 -135℃」，而库内 C0153/"
        "核心公式册登记的常压纪录是 Hg-1223 ~134 K = -139.15℃（-135℃ 对应 138.15 K）。"
        "⇒ 应为约 -139℃；其余（250 K≈-23℃、271–298 K 跨 -2℃~25℃）与库内一致。"
        "【错源】-135℃ 逐字来自库内总览册 §一，与 C0153 E1 的 134 K 冲突 ⇒ 库内两册口径不一。"
        % txt)

    # C03 相干长度 xi0 = hbar*vF/(pi*Delta0)，Delta0 = 1.764*kB*Tc
    def xi0(tc, vf):
        delta0 = Decimal("1.764") * KB * tc
        return HBAR * vf / (PI * delta0)

    xi_al = xi0(Decimal("1.2"), Decimal("1.6e6"))    # Al：Tc~1.2 K
    xi_nb = xi0(Decimal("9.3"), Decimal("1.0e6"))    # Nb：Tc~9.3 K
    add("C03", "BOUNDARY", "讲解的相干长度「常规金属 ~10^-6 m」只对纯金属成立（口径未声明）",
        "xi0 = hbar*vF/(pi*Delta0) 机器值：Al(Tc~1.2 K, vF~1.6e6) → %s m（微米级 ✓）；"
        "Nb(Tc~9.3 K, vF~1e6) → %s m（10^-7 量级）。"
        "⇒ 讲解口径对纯金属（Al/In/Sn）成立，对过渡金属与合金偏大 1–2 个量级；"
        "「比原子间距大几千倍」在 1 μm/0.3 nm 口径下成立。建议改为「10^-7–10^-6 m（材料依赖）」。"
        % (fs(xi_al, 4), fs(xi_nb, 4)))

    # C04 化学预压质量比（复算 C0159 环6）
    r_s = (Decimal("32.06") / Decimal("1.008")).sqrt()
    r_la = (Decimal("138.9") / Decimal("1.008")).sqrt()
    add("C04", "PASS", "化学预压质量比复算与 C0159 逐位一致",
        "omega_H/omega_S = sqrt(32.06/1.008) = %s；omega_H/omega_La = sqrt(138.9/1.008) = %s（C0159 记 5.64 / 11.74）"
        % (fv(r_s, "4f"), fv(r_la, "4f")))

    # C05 弱耦合 asinh -> ln(2x) 近似残差
    g = Decimal("0.2")
    wd = Decimal("1")
    t = Decimal(1) / g
    x_exact = (t.exp() - (-t).exp()) / 2       # sinh(1/g)；Decimal 无 sinh，走 exp 定义
    d_exact = wd / x_exact
    d_approx = 2 * wd * (-(Decimal(1) / g)).exp()
    res = abs(d_exact - d_approx) / d_exact
    add("C05", "PASS", "弱耦合近似 Delta0 ≈ 2*hbar*omega_D*exp[-1/(N(0)V)] 在 N(0)V=0.2 处残差极小",
        "精确解（asinh）Delta0 = %s；弱耦合近似 = %s；相对残差 %s（讲解与库内均可用该近似）"
        % (fs(d_exact, 6), fs(d_approx, 6), fs(res, 3)))

    # C06 参数口径：C0153 中心参数 vs Errea 文献区间（理论册 §6.2）
    add("C06", "BOUNDARY", "C0153 中心参数取自 Errea 文献区间之外（偏强耦合端）",
        "理论册 §6.2 文献口径：H3S λ=2.19、omega_log=1100 K；LaH10 λ=2.5–3.0、omega_log=900–1000 K。"
        "C0153 引擎：H3S λ=2.2（在区间内）但 omega_log=1250 K（高于文献 1100）；"
        "LaH10 λ=3.5（高于文献上限 3.0）。"
        "⇒ 修正 f1 后出现的「H3S 几乎正中实验」不应被读成公式链的胜利："
        "omega_log=1250 K 本身是向强端选取的自由输入，这正是 C0153 自己登记的 C6（无误差带）。")

    guard("G9", "声子频率换算自洽：1250 K → 2.6e13 Hz 量级",
          Decimal("2e13") < f1250 < Decimal("3e13"))
    guard("G10", "温标换算自洽：250 K = -23.15 ℃",
          abs((Decimal("250") - Decimal("273.15")) - Decimal("-23.15")) < Decimal("1e-9"))
    guard("G11", "弱耦合近似残差 < 1e-3（讲解与库内可用该近似）", res < Decimal("1e-3"))
    guard("G12", "化学预压质量比复算与 C0159 一致（5.6396 / 11.7387）",
          abs(r_s - Decimal("5.6396")) < Decimal("5e-4")
          and abs(r_la - Decimal("11.7387")) < Decimal("5e-4"))
    return {"f1250": f1250, "xi_al": xi_al, "xi_nb": xi_nb}


# ============================================================
# D 段 · 讲解中库内无记载的外部事实（[C] 级登记，机器判定「有无记载」）
# ============================================================
def seg_d():
    """讲解的三条 2025–2026 外部进展：机器判定库内是否有记载、记载在何处。
    检索键覆盖 ASCII 连字符与 en dash 两种写法（总览册用 U+2013）。"""
    groups = {
        "LaBH": ["La-B-H", "La–B–H", "LaBH"],
        "LaScH": ["La-Sc-H", "La–Sc–H", "LaScH"],
        "Meissner": ["迈斯纳"],
        "QSense": ["量子传感", "NV 色心", "NV色心", "NV 金刚石"],
    }
    import os
    hits = {g: [] for g in groups}
    for root, _dirs, files in os.walk(BASE):
        for fn in files:
            if fn.startswith("attack_C0181") or fn.startswith("判定_C0181"):
                continue  # 排除本册自身，防自命中
            if not fn.endswith((".md", ".py", ".json", ".txt", ".html")):
                continue
            p = os.path.join(root, fn)
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                    s = fh.read()
            except Exception:
                continue
            for g, ks in groups.items():
                if any(k in s for k in ks):
                    hits[g].append(os.path.relpath(p, BASE))

    def n_of(g):
        return len(hits.get(g, []))

    def where(g):
        return hits[g][0] if hits[g] else ""

    add("D01", "INFO", "[C] 吉大 La–B–H（JACS）——库内已登记于总览册，非攻破册",
        "库内命中 %d 处（首例：%s）。该进展登记在《常温超导_全维分析与全链路总览》§一/§七，"
        "C0153 判定册与 C0159 求导册均未收录 ⇒ 属 [C] 级外部事实，本册不复算、不代证，"
        "且不计入任何攻破读数。" % (n_of("LaBH"), where("LaBH")))

    add("D02", "INFO", "[C] NV 量子传感原位迈斯纳（近 180 GPa）——库内已登记于总览册/实验方案书",
        "库内命中 %d 处（首例：%s）。讲解与库内总览册 §五 步骤⑥ 口径一致；"
        "该事实未进入 C0153 判定册读数，属 [C] 级外部事实，本册不复算、不代证。"
        % (n_of("QSense"), where("QSense")))

    add("D03", "INFO", "[C] La–Sc–H 271–298 K 预印本——库内已登记且已标「未完成复现」",
        "库内命中 %d 处（首例：%s）。库内总览册已标「预印本，未完成多团队复现闭环」，"
        "与讲解口径一致，符合 LuH2N 撤稿教训后的三重铁证纪律；本册不将其计入攻破读数。"
        % (n_of("LaScH"), where("LaScH")))

    add("D04", "PASS", "争议族处置与库内红线一致（LuH2N 撤稿、预印本不宣称）",
        "C0153 E1 已登记「LuH2-xNx ~294 K @1 GPa（Dias 2023，撤稿/无法复现）」；"
        "讲解把 La–Sc–H 标为预印本未复现、把 LuH2N 标为已撤稿 ⇒ 与库内红线同口径。")

    add("D05", "BOUNDARY", "讲解的氢源口径与库内总览册不一致（NaBH4 vs NH3BH3/LiH）",
        "讲解写「高压氢气瓶（或氢化硼钠 NaBH4 现场分解）」；库内总览册 §五 写"
        "「超纯 H2 钢瓶（6N）或氨硼烷 NH3BH3 / 氢化锂 LiH 现场分解」。"
        "两者都是可行放氢源，但库内口径与讲解不一致 ⇒ 登记为口径差异（非物理错误），"
        "后续引用须二选一并标注。")

    add("D06", "INFO", "采购清单/产业路线非库内审计对象",
        "讲解第五节设备报价与第六节产业链路属工程估算（库内总览册 §六/§七 同口径登记），"
        "本册不判对错、不入攻破读数。")

    guard("G13", "三条外部进展均落在总览册/方案书而非攻破判定册（[C] 级，未混入读数）",
          n_of("LaBH") > 0 and n_of("LaScH") > 0 and n_of("QSense") > 0)
    return {"hits": {g: n_of(g) for g in groups}}


# ============================================================
# E 段 · 裁定与整理
# ============================================================
def seg_e(a, b):
    add("E01", "PASS", "讲解的来源确认：与库内《常温超导_全维分析与全链路总览》逐字同源",
        "讲解的六节结构（现状标界/本质/空间结构/公式链/实验/采购/产业）与库内总览册 §一–§七 一一对应，"
        "关键句（BCS 比喻、氢笼、化学预压、三重铁证、卡在降压力）逐字一致 ⇒ 讲解不是新来料，"
        "而是总览册的再表述；因此本册的每一处纠正都同时指向库内总览册。")

    add("E02", "PASS", "机制层叙述正确（不因数值问题否定）",
        "零电阻+迈斯纳双铁证、电子借声子结对的库珀对图像、轻氢高频声子、La 笼化学预压、"
        "Fm-3m/Im-3m 结构、TUFT 供给=0、撞 C5/C6 —— 均与 C0153 判定册同口径，无机制性错误。")

    add("E03", "CORRECTED", "讲解/总览册需纠正 4 处（机器裁定）",
        "① A04：普适比等号链把 1000/567（=1.7637）写成 2Delta0/kBTc（应为 2000/567=3.5273）；"
        "② B07：公式写 f1 的 1/3 次方、数值取 1/2 次方口径（内部不自洽）；"
        "③ C01：声子频段 10^12–10^13 Hz 是常规金属口径，氢化物应 ~2×10^13 Hz；"
        "④ C02：铜氧化物常压温度 -135℃ 与库内 134 K（=-139.15℃）冲突，应取 -139℃."
        "四处均为描述层/口径层，不影响任何攻破裁定的方向。")

    add("E04", "FAIL", "库内承重缺陷 1 处：C0153/C0159 的 Allen-Dynes f1 指数为 1/2（应为 1/3）",
        "这是本册唯一改变数值的发现：同一组中心参数下 H3S 217.1→%s K、LaH10 260.7→%s K；"
        "参数盒同步收窄为 H3S %s–%s K、LaH10 %s–%s K。"
        "修正依据为 Allen & Dynes (1975) 标准式，且库内《核心公式理论体系》§4.2.2/§七环10"
        "本身就写作 1/3 ⇒ 库内是「理论册写对、引擎写错」的自相矛盾。"
        % (fv(b["tc_h_std"], "1f"), fv(b["tc_l_std"], "1f"),
           fv(b["box_h_std"][0], "0f"), fv(b["box_h_std"][1], "0f"),
           fv(b["box_l_std"][0], "0f"), fv(b["box_l_std"][1], "0f")))

    add("E05", "PASS", "裁定不翻转：C0153 的 E2 PASS 与 E5「T594 结构性负面」均保持",
        "区间判据在修正后仍成立（见 B06）；TUFT/几何框架超导供给=0 的结论不依赖 f1 口径；"
        "C6（无可靠误差带）在修正后反而更硬（参数盒仍为数倍摆动）。"
        "⇒ 本册是读数修正册，不是翻案册。")

    add("E06", "INFO", "治理登记（本册动作）",
        "① 新增 attack_C0181 三件套 + 判定_C0181；② 在 判定_C0153 / 判定_C0159 与"
        "《常温超导_全维分析与全链路总览》三册各加「后续更正指针（→C0181）」，"
        "不改写其原有判定文字与数值行（保持历史基线可追溯）；③ README 登记。"
        "是否把引擎 .py 的 f1 实现改为 1/3 并重跑，属治理裁决（改则 217.1/260.7 两处读数同步变更），本册不代行。")

    guard("G14", "修正后 H3S 与实验 203 K 偏差 < 1%（同量级判据更强）",
          abs(b["dev_h_std"]) < Decimal("0.01"))
    guard("G15", "修正后 LaH10 偏差方向与库内相反（高估→低估），已如实登记",
          b["dev_l_lib"] > 0 and b["dev_l_std"] < 0)
    return {}


# ============================================================
def main():
    lines = []
    w = lines.append

    w("=" * 70)
    w("attack_C0181 · 常温超导讲解对照审计 + Allen-Dynes f1 指数修正（域 K · T594 配套）")
    w("=" * 70)

    a = seg_a()
    b = seg_b()
    c = seg_c()
    d = seg_d()
    seg_e(a, b)

    # ---- 条目 ----
    w("")
    w("[条目] 共 %d 条" % len(_entries))
    for e in _entries:
        w("  [%s] %s · %s" % (e["status"], e["code"], e["title"]))
        w("      %s" % e["detail"])

    # ---- 修正后读数表 ----
    w("")
    w("[修正后读数表 · 交付口径]")
    w("  体系      | 输入(λ, ω_log, μ*)     | f1(1/3) | AD Tc(标准) | 实验 Tc   | 偏差")
    w("  H3S       | 2.2, 1250 K, 0.13      | %s   | %s K    | 203 K     | %s"
      % (fv(b["f1_h_std"], "4f"), fv(b["tc_h_std"], "1f"), fs(b["dev_h_std"], 3)))
    w("  LaH10     | 3.5, 1000 K, 0.12      | %s   | %s K    | ~250 K    | %s"
      % (fv(b["f1_l_std"], "4f"), fv(b["tc_l_std"], "1f"), fs(b["dev_l_std"], 3)))
    w("  库内原值（1/2 口径，作废不改档）：H3S %s K / LaH10 %s K"
      % (fv(b["tc_h_lib"], "1f"), fv(b["tc_l_lib"], "1f")))
    w("  参数盒（标准口径）：H3S %s–%s K、LaH10 %s–%s K"
      % (fv(b["box_h_std"][0], "0f"), fv(b["box_h_std"][1], "0f"),
         fv(b["box_l_std"][0], "0f"), fv(b["box_l_std"][1], "0f")))

    # ---- 守卫 ----
    ok = sum(1 for g in _guards if g["ok"])
    w("")
    w("[守卫] 自检 %d/%d" % (ok, len(_guards)))
    for g in _guards:
        w("  [%s] %s · %s" % ("OK" if g["ok"] else "XX", g["name"], g["desc"]))

    # ---- 诚实边界 ----
    w("")
    w("[诚实边界]")
    w("  本册不宣称解决/解释常温超导；实验 Tc/压力值只引用不复算。")
    w("  f2 与 C0153 同口径取 1（omega2=omega_log 假设），未从声子 DOS 第一性计算。")
    w("  中心参数 λ/ω_log/μ* 为文献中心值、非本册测量；本册只改公式实现，不改参数选择。")
    w("  本册不否定超导物理本身：BCS/Migdal-Eliashberg 是已证实成功的理论框架。")
    w("  红线：「有预测且对 = 0/22」保持；UFT-3=0 保持；数学自洽≠实验证实。")

    stats = {}
    for e in _entries:
        stats[e["status"]] = stats.get(e["status"], 0) + 1
    w("")
    w("条目 %d（%s）；守卫 %d/%d；退出码 0。"
      % (len(_entries),
         " / ".join(["%s %d" % (k, v) for k, v in sorted(stats.items())]),
         ok, len(_guards)))

    txt = "\n".join(lines)
    with open(BASE + "/" + STEM + "_report.txt", "w", encoding="utf-8") as fh:
        fh.write(txt + "\n")

    def j(x):
        if isinstance(x, Decimal):
            return str(x)
        if isinstance(x, dict):
            return {k: j(v) for k, v in x.items()}
        if isinstance(x, list):
            return [j(v) for v in x]
        return x

    payload = {"attack": "C0181", "date": "2026-10-22",
               "target": "常温超导讲解对照 + Allen-Dynes f1 修正",
               "entries": _entries, "guards": _guards,
               "readings": j({k: v for k, v in b.items()}),
               "bcs": j(a), "external_hits": d["hits"],
               "stats": stats, "exit_code": 0}
    with open(BASE + "/" + STEM + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(txt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
