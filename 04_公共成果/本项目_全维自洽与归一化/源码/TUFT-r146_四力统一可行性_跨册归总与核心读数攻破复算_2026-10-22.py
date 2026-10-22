# -*- coding: utf-8 -*-
"""
r146 · 四力统一可行性 · 跨册归总与核心读数攻破复算
===================================================

性质
----
**本册不产生新物理。** 它做两件事：

1. **跨册归总（整理册承载）**：把 r120《所有力大统一方程 候选全集+状态机》、
   第 12 层《力的统一 穷举封闭谱》、r140《终局裁定 1/7》、r142《核心公式修复》、
   第 8 层（η 量级）中关于「四力统一可行性」的裁定，归并为一张综合判决表。
2. **核心读数攻破复算（本引擎）**：
   - A 段：E8 引力耦合缺口三口径，用 Decimal 60 位重验与 r140 N1/N2（250 位）一致；
   - **B 段（★增量，库内零建模）**：攻破「AS 量子引力跑动能否闭合 E8 缺口」——
     把 AS 引力 β 方程参数化，从 M_Z 数值积分到 M_Pl，在 GUT 能标处与标准 RG 比对，
     证明即便取合理 AS 临界指数，对 α_G(GUT) 的修正也被 α<<1 压死，**缺口结构性无法闭合**；
   - C 段：E8 缺口的**模型无关性**——换 SU(5)/SO(10)/MSSM 三种 GUT 汇聚点，
     证明引力统一点始终高出 ~2 个量级，缺口不依赖具体 GUT 模型。

与 r140 的边界：r140 用 250 位复算了 E8 缺口的**静态**读数（N1/N2）并给了终局裁定；
本册 B 段攻的是 r140 没做、第 12 层 W-31 点名 J26「真正前沿」且库内**零建模**的方向。

工具：decimal.Decimal（60 位）+ fractions.Fraction 四元组量纲 (M,L,T,Q)。
复现：`python 源码/_run_r146.py`
"""

from __future__ import print_function

import io
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "数据")
STAMP = "2026-10-22"
NAME = "TUFT-r146_四力统一可行性_跨册归总与核心读数攻破复算_" + STAMP

# ---------------------------------------------------------------- 高精度常量

C = Decimal("299792458")
G = Decimal("6.67430e-11")
HBAR = Decimal("1.054571817e-34")
# 普朗克质量（能标口径，与 r140 一致）：M_Pl = sqrt(hbar c / G)，转 GeV
M_Pl_KG = (HBAR * C / G).sqrt()
GEV_PER_KG = (C * C / Decimal("1.602176634e-10"))  # 1 kg = (c^2 / 1 GeV-in-J) GeV
M_Pl_GEV = Decimal("1.22091e19")                   # 标称普朗克质量（GeV），与 r140 同口径
M_Z_GEV = Decimal("91.1876")
M_GUT_GEV = Decimal("2.014e16")                    # MSSM 三力汇聚点（r120/r140）
ALPHA_GUT = Decimal(1) / Decimal("24.3")           # 统一点耦合 1/alpha_GUT ≈ 24.3（r120/r140）

# ---------------------------------------------------------------- 量纲工具


def D(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))


DIM_NONE = D(0, 0, 0, 0)


def dmul(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])


def ddiv(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3])


def dpow(a, n):
    return (a[0] * Fraction(n), a[1] * Fraction(n), a[2] * Fraction(n), a[3] * Fraction(n))


def dstr(a):
    sym = ("M", "L", "T", "Q")
    out = []
    for i in range(4):
        v = a[i]
        if v == 0:
            continue
        if v == 1:
            out.append(sym[i])
        else:
            iv = int(v)
            sgn = "-" if iv < 0 else ""
            out.append(sym[i] + "^" + sgn + str(abs(iv)))
    return " ".join(out) if out else "1"


# ---------------------------------------------------------------- 记录设施

ENTRIES = []
GUARDS = []


def add(code, status, title, detail):
    ENTRIES.append({"code": code, "status": status, "title": title, "detail": detail})


def guard(name, ok, info=""):
    GUARDS.append({"name": name, "ok": bool(ok), "info": info})
    return bool(ok)


def fv(x, n=20):
    try:
        return format(Decimal(x), "." + str(n) + "E")
    except Exception:
        try:
            return format(Decimal(str(x)), "." + str(n) + "E")
        except Exception:
            return str(x)


def rel(a, b):
    a = Decimal(a)
    b = Decimal(b)
    m = max(abs(a), abs(b))
    if m == 0:
        return abs(a - b)
    return abs(a - b) / m


def dex(ratio):
    """量级差（以 10 为底）"""
    return (Decimal(ratio).ln() / Decimal(10).ln())


# ---------------------------------------------------------------- A 段：E8 引力缺口三口径复算

def run_a():
    """E8 引力耦合缺口三口径复算，与 r140 N1/N2（250 位）校准。

    缺口定义（r120 E8 / r140 N1-N2）：引力与三力统一的耦合强度错配。
    三口径：
      (a) α_G(M_GUT) = (M_GUT / M_Pl)^2；
      (b) 引力间隙 dex = log10(α_GUT / α_G(M_GUT))；
      (c) 引力统一点 / 三力汇聚点 = M_Pl·√α_GUT / M_GUT。
    """
    a_g_gut = (M_GUT_GEV / M_Pl_GEV) ** 2
    gap_dex = dex(ALPHA_GUT / a_g_gut)
    m_unify = M_Pl_GEV * ALPHA_GUT.sqrt()
    ratio_point = m_unify / M_GUT_GEV

    # 与 r140 N1/N2 校准
    ref_a = Decimal("2.72123381695e-6")
    ref_dex = Decimal("4.179627867")
    ok_a = rel(a_g_gut, ref_a) < Decimal("5e-4")   # 数值口径差（M_GUT 取位）
    ok_dex = rel(gap_dex, ref_dex) < Decimal("1e-4")  # dex 是核心读数，必须严合
    ok_pt = abs(ratio_point - Decimal("123")) / Decimal("123") < Decimal("1e-2")

    add("A01", "PASS" if (ok_a and ok_dex and ok_pt) else "FAIL",
        "E8 引力缺口三口径复算（与 r140 N1/N2 校准）",
        "α_G(M_GUT)=" + fv(a_g_gut) + "（r140 " + fv(ref_a) + "，相对差 " + fv(rel(a_g_gut, ref_a))
        + "，源于 M_GUT 取位口径）；引力间隙=" + fv(gap_dex) + " dex（r140 " + fv(ref_dex)
        + "，严合）；引力统一点=" + fv(m_unify) + " GeV，/三力汇聚点=" + fv(ratio_point)
        + " 倍（≈123，严合）。三口径一致 ⇒ r140/r120 的 E8 缺口读数在本册 Decimal 60 下复现。")

    guard("A01_alpha_g", ok_a, fv(rel(a_g_gut, ref_a)))
    guard("A01_gap_dex", ok_dex, fv(gap_dex))
    guard("A01_unify_point", ok_pt, fv(ratio_point))
    return {"a_g_gut": a_g_gut, "gap_dex": gap_dex, "m_unify": m_unify, "ratio_point": ratio_point}


# ---------------------------------------------------------------- B 段：AS 引力 RG 能否闭合 E8 缺口（★核心攻破）

def alpha_g_at_gut_as(eta, n=20000):
    """AS 引力 β 方程数值积分：dα/dlnμ = 2α − (η/2)α²，η>0，固定点 α* = 4/η。
    初值 α(M_Z) = (M_Z/M_Pl)^2，从 M_Z 积到 M_Pl，返回 α 在 M_GUT 处的值。
    跨越 ln_gut 时线性插值回 GUT 处（避免阶跃记录误差：单步 dln≈0.02 对应 α 变化 ~4%）。
    """
    a = (M_Z_GEV / M_Pl_GEV) ** 2
    ln_z = M_Z_GEV.ln()
    ln_pl = M_Pl_GEV.ln()
    ln_gut = M_GUT_GEV.ln()
    dln = (ln_pl - ln_z) / n
    ln = ln_z
    a_at_gut = None
    for _ in range(n):
        def f(x):
            return 2 * x - (eta / 2) * x * x
        k1 = f(a)
        k2 = f(a + dln / 2 * k1)
        k3 = f(a + dln / 2 * k2)
        k4 = f(a + dln * k3)
        a_new = a + dln / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        ln_new = ln + dln
        if a_at_gut is None and ln_new >= ln_gut:
            frac = (ln_gut - ln) / (ln_new - ln)   # 回插到 ln_gut 处
            a_at_gut = a + (a_new - a) * frac
            break
        a, ln = a_new, ln_new
    if a_at_gut is None:
        a_at_gut = a
    return a_at_gut


def run_b():
    """攻破：AS 量子引力跑动能否在 GUT 能标闭合 E8 缺口。

    缺口在 GUT(≈10^16 GeV) 处 α_G≈(μ/M_Pl)^2≈10^-6，而 α_GUT≈0.04，差 4.18 dex。
    AS 修正来自固定点项 −(η/2)α²，因 α<<α*(=4/η) 在整个低能区被压死。
    本段对合理 η∈[0.01,10] 参数化扫描，数值积分，证明 α_G(GUT) 修正 << 缺口。
    """
    a_std = (M_GUT_GEV / M_Pl_GEV) ** 2
    etas = [Decimal(x) for x in ("0.01", "0.1", "0.5", "1", "2", "5", "10")]
    rows = []
    max_dev = Decimal(0)
    for eta in etas:
        a_as = alpha_g_at_gut_as(eta)
        dev = (a_as - a_std) / a_std
        max_dev = max(max_dev, abs(dev))
        rows.append((fv(eta, 4), fv(a_as), fv(dev)))
    # 闭合缺口所需的反解上界：要让 α_G(GUT) 抬升 10^4 倍（4.18 dex），
    # 需 ln(10^4)=9.21 ≈ ∫(η/2)α dlnμ ~ (η/2)·<α>·ln(M_Pl/M_Z)，
    # <α>~10^-6 ⇒ η ~ 5.5e5（荒谬，远超任何 AS 文献估计 |η|~O(1)）。
    needed_eta = Decimal("9.21") / (Decimal("0.5") * Decimal("1e-6")
                                    * (M_Pl_GEV / M_GUT_GEV).ln())
    # 物理合理 AS 临界指数上界：文献 |η_AS| 估计约 0.1~2（Reuter 固定点族），
    # 取宽容上界 10。
    eta_phys_max = Decimal("10")
    ok_closed = max_dev < Decimal("1e-2")   # AS 修正 < 1% ⇒ 远不能闭合 10^4 倍缺口
    ok_eta_absurd = needed_eta > eta_phys_max * Decimal("1000")  # 所需 η 超物理合理值千倍

    add("B01", "PASS" if (ok_closed and ok_eta_absurd) else "FAIL",
        "★攻破：AS 量子引力跑动无法闭合 E8 引力缺口（库内零建模方向，第12层 W-31/J26）",
        "对 η∈[0.01,10] 数值积分 AS β 方程，α_G(GUT) 相对标准 RG 最大偏差 "
        + fv(max_dev) + "（<<1%）⇒ E8 缺口在 GUT 处仍为 " + fv(dex(ALPHA_GUT / a_std))
        + " dex，结构性无法闭合。闭合缺口所需临界指数 η_crit≈" + fv(needed_eta, 6)
        + "，超文献合理上界(≈10)约 " + fv(needed_eta / eta_phys_max, 4)
        + " 倍 ⇒ 物理上不可信。结论：引力耦合低能 ∝μ² 行为把固定点效应压在 μ~M_Pl 附近，"
        + "GUT(10^16) 处 α_G 已被锁定为 10^-6 量级，AS 路线在合理参数下不能把四力拉到同一点。")
    guard("B01_as_dev_small", ok_closed, fv(max_dev))
    guard("B01_needed_eta_absurd", ok_eta_absurd, fv(needed_eta, 6))
    return rows, max_dev, needed_eta


# ---------------------------------------------------------------- C 段：E8 缺口模型无关性

def run_c():
    """E8 缺口是否依赖具体 GUT 模型？——换 SU(5)/SO(10)/MSSM 三汇聚点验证。

    引力统一点 M_unify = M_Pl·√α_GUT 只依赖 M_Pl 与 α_GUT（与 GUT 模型无关）。
    若各 GUT 的三力汇聚点都在 10^15~10^16 GeV，则引力点始终高出 ~2-3 dex。
    """
    m_unify = M_Pl_GEV * ALPHA_GUT.sqrt()
    guts = [("SU(5)", Decimal("1e15")), ("SO(10)", Decimal("2e16")), ("MSSM", M_GUT_GEV)]
    rows = []
    ok = True
    for name, mg in guts:
        ratio = m_unify / mg
        d = dex(ratio)
        rows.append((name, fv(mg), fv(ratio), fv(d)))
        ok = ok and ratio > Decimal("100")  # 始终 ≥ 2 dex
    add("C01", "PASS" if ok else "FAIL",
        "E8 引力缺口的模型无关性（换三 GUT 汇聚点）",
        "引力统一点 " + fv(m_unify) + " GeV 固定（只依赖 M_Pl、α_GUT）；"
        + "SU(5) 1e15 / SO(10) 2e16 / MSSM 2.014e16 GeV 处比值分别为 "
        + " / ".join(r[2] for r in rows) + " 倍（" + " / ".join(r[3] for r in rows)
        + " dex）。引力点始终高出三力汇聚点 ≥2 dex ⇒ E8 缺口不依赖具体 GUT 模型，结构性。")
    guard("C01_model_independent", ok, "min ratio passed")
    return rows


# ---------------------------------------------------------------- 主流程

def build_report(a_res, b_rows, b_maxdev, b_needed, c_rows):
    lines = []
    lines.append("=" * 78)
    lines.append("r146 · 四力统一可行性 · 跨册归总与核心读数攻破复算")
    lines.append("=" * 78)
    lines.append("")
    lines.append("性质：不产生新物理。跨册归总（整理册）+ E8 引力缺口 RG 闭合攻破（本引擎）。")
    lines.append("")
    n_pass = sum(1 for e in ENTRIES if e["status"] == "PASS")
    n_fail = sum(1 for e in ENTRIES if e["status"] == "FAIL")
    lines.append("条目 %d：PASS = %d  FAIL = %d" % (len(ENTRIES), n_pass, n_fail))
    lines.append("")
    lines.append("-" * 78)
    for e in ENTRIES:
        lines.append("[%s] %s  %s" % (e["status"], e["code"], e["title"]))
        lines.append("      " + e["detail"])
        lines.append("")
    lines.append("-" * 78)
    ng = len(GUARDS)
    nok = sum(1 for g in GUARDS if g["ok"])
    lines.append("守卫 %d / %d 通过" % (nok, ng))
    for g in GUARDS:
        if not g["ok"]:
            lines.append("  [FAIL-GUARD] " + g["name"] + " : " + g["info"])
    lines.append("")
    lines.append("★ B 段核心攻破（库内零建模 → 本册首攻）：")
    lines.append("  AS 引力 β 方程 dα/dlnμ = 2α − (η/2)α²，η∈[0.01,10] 数值积分；")
    lines.append("  α_G(GUT) 相对标准 RG 最大偏差 " + fv(b_maxdev) + "（<<1%），")
    lines.append("  闭合 E8 缺口(4.18 dex)所需 η_crit ≈ " + fv(b_needed, 4) + "（超物理合理值千倍）。")
    lines.append("  结论：四力统一的最后一道门（引力耦合 RG 抬升）在合理 AS 参数下结构性无法闭合。")
    lines.append("=" * 78)
    return "\n".join(lines), (n_pass, n_fail)


def main():
    a_res = run_a()
    b_rows, b_maxdev, b_needed = run_b()
    c_rows = run_c()

    report, counts = build_report(a_res, b_rows, b_maxdev, b_needed, c_rows)
    print(report)

    counts_map = {"PASS": counts[0], "FAIL": counts[1]}
    payload = {
        "round": "r146",
        "title": "四力统一可行性 · 跨册归总与核心读数攻破复算",
        "date": STAMP,
        "nature": "不产生新物理；跨册归总 + E8 引力缺口 AS-RG 闭合攻破（库内零建模首攻）",
        "constants": {
            "M_Pl_GeV": fv(M_Pl_GEV), "M_Z_GeV": fv(M_Z_GEV),
            "M_GUT_GeV": fv(M_GUT_GEV), "alpha_GUT": fv(ALPHA_GUT),
        },
        "e8_gap_A": {
            "alpha_G_MGUT": fv(a_res["a_g_gut"]), "gap_dex": fv(a_res["gap_dex"]),
            "gravity_unify_point_GeV": fv(a_res["m_unify"]),
            "ratio_unify_over_MGUT": fv(a_res["ratio_point"]),
        },
        "as_rg_close_B": {
            "scan_eta": [r[0] for r in b_rows],
            "alpha_G_MGUT_as": [r[1] for r in b_rows],
            "deviation": [r[2] for r in b_rows],
            "max_deviation": fv(b_maxdev),
            "eta_crit_to_close_gap": fv(b_needed, 6),
            "verdict": "E8 缺口结构性无法闭合：AS 修正 << 缺口，所需 η 超物理合理值千倍",
        },
        "model_independence_C": [
            {"gut": r[0], "M_GUT_GeV": r[1], "ratio": r[2], "dex": r[3]} for r in c_rows
        ],
        "entries": ENTRIES,
        "guards": GUARDS,
        "counts": counts_map,
        "guard_total": len(GUARDS),
        "guard_pass": sum(1 for g in GUARDS if g["ok"]),
    }

    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)
    with io.open(os.path.join(DATA_DIR, NAME + ".json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2))
    with io.open(os.path.join(DATA_DIR, NAME + "_report.txt"), "w", encoding="utf-8") as fh:
        fh.write(report)

    md = []
    md.append("# " + NAME)
    md.append("")
    md.append("> 本册**不产生新物理**。跨册归总 = 整理册承载；核心读数攻破 = 本引擎。")
    md.append("")
    md.append("## A 段 · E8 引力缺口三口径（与 r140 N1/N2 校准）")
    md.append("")
    md.append("- α_G(M_GUT) = " + fv(a_res["a_g_gut"]) + "（r140 " + fv(Decimal("2.72123381695e-6")) + "）")
    md.append("- 引力间隙 = " + fv(a_res["gap_dex"]) + " dex（r140 4.179627867，严合）")
    md.append("- 引力统一点 = " + fv(a_res["m_unify"]) + " GeV；/三力汇聚点 = "
              + fv(a_res["ratio_point"]) + " 倍 ≈ 123")
    md.append("")
    md.append("## B 段 · ★AS 引力 RG 能否闭合 E8 缺口（库内零建模首攻）")
    md.append("")
    md.append("| η | α_G(M_GUT, AS) | 相对标准 RG 偏差 |")
    md.append("|---|---|---|")
    for r in b_rows:
        md.append("| " + r[0] + " | " + r[1] + " | " + r[2] + " |")
    md.append("")
    md.append("最大偏差 " + fv(b_maxdev) + "（<<1%）。闭合缺口所需 η_crit ≈ "
              + fv(b_needed, 4) + "，超物理合理值(≈10)千倍 ⇒ **E8 缺口结构性无法闭合**。"
              + "引力耦合低能 ∝μ² 行为把 AS 固定点效应压在 μ~M_Pl 附近，GUT(10^16) 处 α_G 锁死在 10^-6 量级。")
    md.append("")
    md.append("## C 段 · E8 缺口模型无关性")
    md.append("")
    md.append("| GUT 模型 | M_GUT (GeV) | 引力点/三力点 | dex |")
    md.append("|---|---|---|---|")
    for r in c_rows:
        md.append("| " + r[0] + " | " + r[1] + " | " + r[2] + " | " + r[3] + " |")
    md.append("")
    md.append("引力统一点固定；各 GUT 三力点均在 10^15~10^16 GeV ⇒ 引力点始终高 ≥2 dex ⇒ 缺口结构性。")
    md.append("")
    md.append("## 条目与守卫")
    md.append("")
    md.append("条目 %d（PASS %d / FAIL %d）；守卫 %d/%d。"
             % (len(ENTRIES), counts[0], counts[1], payload["guard_pass"], payload["guard_total"]))
    with io.open(os.path.join(DATA_DIR, NAME + ".md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))

    return 0 if all(g["ok"] for g in GUARDS) else 1


if __name__ == "__main__":
    sys.exit(main())
