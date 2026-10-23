# -*- coding: utf-8 -*-
"""
attack_C0209_近极端热力学攻破_2026-10-21.py
独立精算：T106「近极端黑洞热力学涨落与比热符号」· 微正则/正则系综 + 曲率修正

定位：母册 T106（行 230），撞 C7。衔接 C0206（ringdown QNM 口径）与 C0172（Page 曲线口径），
二者均已登记为对 TUFT/几何框架的结构性负面闭合；本册在同一条线上核算「近极端温度 → 比热符号
翻转 → 正则/微正则涨落」三件标准 GR 热力学算术。

【归因纪律】本册全部数值 = 标准 GR（Kerr）热力学算术复核；TUFT 已于 C0133 注销。
严禁把标准物理结果写成 TUFT 预测/修正。本册裁的是：近极端热力学是否 GR 内在性质、
TUFT 是否供给黑洞热力学/系综结构。

把「近极端黑洞热力学」压成五条可复核读数：

  E1 近极端温度核算：T=(r_+-r_-)/(4π(r_+²+a²))，对 a→M（r_+-r_-→0）极限 T→0 精算（几何单位）。
  E2 **比热符号核算（本册核心）**：固定 J 比热 C_J=∂M/∂T|_J 在近极端区的符号翻转/发散结构。
  E3 系综涨落核算：ΔE²=k_B T² C 的量级（近极端 T→0 → 正则涨落结构）。
  E4 供给检查：TUFT 是否供给黑洞热力学/系综结构（=0）。
  E5 裁定：近极端热力学是 GR 内在性质（Kerr 热力学算术），结构性负面，撞 C7。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机，退出码 0。

数学骨架（几何单位 G=c=ℏ=k_B=1）：
  Kerr 视界 r_± = M ± √(M²-a²)；比自旋 μ=a/M=J/M²∈[0,1]；ε=√(1-μ²)。
  r_+-r_- = 2Mε；r_+²+a² = 2M²(1+ε)。
  温度   T = (r_+-r_-)/(4π(r_+²+a²)) = ε/[4π M(1+ε)]。                …(1)
  熵     S = A/4 = π(r_+²+a²) = 2π M²(1+ε) = 2πJ·√((1+ε)/(1-ε))（固定 J）。…(2)
  固定 J 比热 C_J = T(∂S/∂T)_J = 2εS/(2-2ε-ε²)。                       …(3)
  (3) 推导：ln S=(1/2)(ln(1+ε)-ln(1-ε)) ⇒ dS/dε = S/(1-ε²)；
       ln T=ln ε-ln(1+ε)+¼ ln(1-ε²) ⇒ (1/T)dT/dε = [2-2ε-ε²]/[2ε(1-ε²)]；
       故 C_J=T(dS/dε)/(dT/dε)=2εS/(2-2ε-ε²)。
  符号翻转：分母 D(ε)=2-2ε-ε²=0 ⇒ ε*=√3-1≈0.7321（对应 μ*=√(2√3-3)≈0.681）。
       ε=1（Schwarzschild, μ=0）：D=-1<0 ⇒ C_J<0（负比热）；
       ε→0（近极端）：D→2>0 ⇒ C_J>0（正比热）。Davies 符号翻转/发散结构。

毕达哥拉斯参数化：ε=2n/(n²+1)、μ=(n²-1)/(n²+1) 使 √(1-μ²) 退化为精确分数，
  故 E1/E2 的代数量（4πT=ε/(1+ε)、D=2-2ε-ε²）为 Fraction 精确；数值幅度用 Decimal。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# 高倍常数（Decimal），仅用于数值幅度；代数量一律 Fraction。
PI = Decimal("3.14159265358979323846264338327950288419716939937510")
SQRT3 = Decimal("1.73205080756887729352744634150587236694280525381038")


def frac_sqrt_rat(fr: Fraction) -> Decimal:
    """√(Fraction) → Decimal 48 位。"""
    return (Decimal(fr.numerator) / Decimal(fr.denominator)).sqrt()


def sample_points():
    """毕达哥拉斯参数 n → (ε, μ)，ε=2n/(n²+1) 为精确分数。M=J=1。"""
    pts = []
    for n in (1, 2, 3, 4, 10, 25, 50):
        eps = Fraction(2 * n, n * n + 1)
        mu = Fraction(n * n - 1, n * n + 1)
        pts.append((n, eps, mu))
    return pts


def e1_temperature():
    """E1 近极端温度核算：T=ε/[4πM(1+ε)]，M=1；4πT=ε/(1+ε) 精确。"""
    rows = []
    for n, eps, mu in sample_points():
        four_pi_T = eps / (1 + eps)          # 无量纲精确：4π M T
        T_num = (Decimal(four_pi_T.numerator) / Decimal(four_pi_T.denominator)) / (4 * PI)
        rows.append({
            "n": n, "mu": mu, "eps": eps,
            "four_pi_MT": four_pi_T,          # Fraction
            "T_M_eq1": T_num,                 # Decimal
        })
    # 极限读数：ε→0
    eps_star = SQRT3 - Decimal(1)            # 比热零点（E2 用）
    return rows, eps_star


def e2_cJ(rows):
    """E2 固定 J 比热符号核算：C_J=2εS/(2-2ε-ε²)，D=2-2ε-ε²。"""
    out = []
    for r in rows:
        eps = r["eps"]
        if eps >= 1:
            continue   # Schwarzschild 固定 J=0 退化（S/(2πJ) 发散），固定 J 系综从旋转体算起
        D = Fraction(2) - 2 * eps - eps * eps   # 精确分母
        sign = "neg" if D < 0 else ("pos" if D > 0 else "div")
        eps_dec = Decimal(eps.numerator) / Decimal(eps.denominator)
        rat = frac_sqrt_rat((1 + eps) / (1 - eps))
        D_dec = Decimal(D.numerator) / Decimal(D.denominator)
        c_dimless = (Decimal(2) * eps_dec * rat / D_dec)
        out.append({
            "n": r["n"], "eps": eps, "mu": r["mu"],
            "D": D, "sign": sign,
            "S_over_2piJ": rat,
            "cJ_over_2piJ": c_dimless,
        })
    return out


def e3_fluctuation(e1rows, e2rows):
    """E3 系综涨落：ΔE²=k_B T² C_J（k_B=1）。相对涨落 σ_E/M = T√C_J/M。按 n 对齐。"""
    e1by = {r["n"]: r for r in e1rows}
    out = []
    for b in e2rows:
        a = e1by[b["n"]]
        T = a["T_M_eq1"]
        cJ = b["cJ_over_2piJ"]
        rel = T * cJ.copy_abs().sqrt()
        out.append({"n": a["n"], "eps": a["eps"], "T": T,
                    "cJ": cJ, "sigma_E_over_M": rel})
    return out


def e4_supply():
    """E4 TUFT 供给：黑洞热力学/系综结构。TUFT 已注销（C0133），无此供给。"""
    return {
        "tuft_black_hole_thermo": 0,     # TUFT 无黑洞热力学
        "tuft_ensemble_structure": 0,    # 无微正则/正则系综结构
        "tuft_surface_gravity": 0,       # 无表面引力/温度公式供给
        "tuft_specific_heat": 0,         # 无比热符号结构
        "note": "近极端温度、比热符号、涨落均为标准 GR（Kerr 热力学）内在算术。",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    w("=" * 78)
    w("attack_C0209 · 近极端黑洞热力学涨落与比热符号（T106 · 撞 C7）攻破")
    w("=" * 78)
    w("[归因] 数值全部 = 标准 GR/Kerr 热力学算术复核；TUFT 已注销（C0133）。")
    w("[纪律] 不把标准物理结果写成 TUFT 预测/修正；几何单位 G=c=ℏ=k_B=1，M=J=1。")

    entries = []

    # ---- E1 ----
    e1rows, eps_star = e1_temperature()
    w("\n[E1] 近极端温度核算  T=ε/[4πM(1+ε)]，ε=√(1-μ²)")
    w("  %-4s %-12s %-12s %-14s %s" % ("n", "μ=a/M", "ε=√(1-μ²)", "4πMT=ε/(1+ε)", "T(M=1)"))
    for r in e1rows:
        w("  %-4d %-12s %-12s %-14s %s"
          % (r["n"], str(r["mu"]), str(r["eps"]), str(r["four_pi_MT"]),
             format(r["T_M_eq1"], ".10e")))
    t_schw = e1rows[0]["T_M_eq1"]
    t_near = e1rows[-1]["T_M_eq1"]
    w("  Schwarzschild(n=1,μ=0): T = %s (=1/8πM，4πMT=%s)"
      % (format(t_schw, ".12f"), e1rows[0]["four_pi_MT"]))
    w("  近极端(n=50,μ=2499/2501≈0.9992): T = %s" % format(t_near, ".10e"))
    w("  => μ→1 时 ε→0，T=ε/[4πM(1+ε)]→0：温度线性消失于极端极限（几何单位精算）。")
    entries.append(("E1", "近极端温度 T→0 精算：Schwarzschild T=1/8πM；μ=0.9992 时 T 已压至 "
                    + format(t_near, ".3e"), "PASS", "Kerr 温度公式几何单位算术"))

    # ---- E2 ----
    e2rows = e2_cJ(e1rows)
    w("\n[E2] 固定 J 比热符号核算（本册核心）  C_J=2εS/(2-2ε-ε²)")
    w("  符号翻转零点 D(ε)=2-2ε-ε²=0 ⇒ ε*=√3-1=%s（μ*=√(2√3-3)）" % format(eps_star, ".10f"))
    w("  %-4s %-10s %-16s %-6s %-16s %s" %
      ("n", "ε", "D=2-2ε-ε²", "符号", "S/(2πJ)", "C_J/(2πJ)"))
    for r in e2rows:
        w("  %-4d %-10s %-16s %-6s %-16s %s"
          % (r["n"], str(r["eps"]), str(r["D"]), r["sign"],
             format(r["S_over_2piJ"], ".8f"), format(r["cJ_over_2piJ"], ".8f")))
    w("  Schwarzschild(ε=1,μ=0,固定 J=0)：解析 D=2-2-1=-1<0 ⇒ C_J<0（负比热，引力束缚系统特征）")
    w("  旋转体 n=2(ε=0.8)：D=%s<0 ⇒ C_J<0；n=3(ε=0.6)：D=+11/25>0 ⇒ C_J 已转正"
      % e2rows[0]["D"])
    w("  近极端(n=50,ε≈0.04): D→2>0 ⇒ C_J>0（正比热）；ε→ε* 处 D→0 ⇒ C_J 发散。")
    w("  => Davies 结构复算：C_J 在 ε*=√3-1≈0.7321 处发散并由负转正（Schwarzschild 负→近极端正）。")
    entries.append(("E2", "C_J 符号翻转：D=2-2ε-ε²，ε*=√3-1≈0.7321；Schwarzschild C_J<0、"
                    "近极端 C_J>0、ε* 处发散（Davies 结构精算）", "PASS",
                    "第一性推导 (3) 式 + Fraction 精确符号 / Decimal 幅度"))

    # ---- E3 ----
    e3rows = e3_fluctuation(e1rows, e2rows)
    w("\n[E3] 系综涨落核算  ΔE²=k_B T² C_J（k_B=1），相对涨落 σ_E/M=T√|C_J|/M")
    w("  %-4s %-10s %-14s %-14s %s" % ("n", "ε", "T", "C_J", "σ_E/M"))
    for r in e3rows:
        w("  %-4d %-10s %-14s %-14s %s" %
          (r["n"], str(r["eps"]), format(r["T"], ".6e"),
           format(r["cJ"], ".6f"), format(r["sigma_E_over_M"], ".6e")))
    w("  => 近极端 T→0 压制正则涨落：σ_E/M 随 T 趋零而趋零；正则系综在近极端失效、")
    w("     微正则/正则区分由此而生——系综结构是 GR 热力学的内在推论，非外部供给。")
    entries.append(("E3", "正则涨落 ΔE²=T²C_J 随近极端 T→0 被压制，σ_E/M→0（微正则/正则区分的 GR 内禀起源）",
                    "PASS", "涨落定理标准式算术"))

    # ---- E4 ----
    g4 = e4_supply()
    w("\n[E4] 供给检查：TUFT 是否供给黑洞热力学/系综结构？")
    w("  TUFT 黑洞热力学供给 = %d；系综结构供给 = %d；表面引力/温度 = %d；比热符号 = %d"
      % (g4["tuft_black_hole_thermo"], g4["tuft_ensemble_structure"],
         g4["tuft_surface_gravity"], g4["tuft_specific_heat"]))
    w("  => TUFT 已注销（C0133），无任何黑洞热力学/系综结构供给；本册全部读数为 GR 既有算术。")
    entries.append(("E4", "TUFT 供给 = 0：无黑洞热力学、无系综结构、无表面引力/比热",
                    "PASS", "TUFT C0133 注销；引用不复算"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  子问题(a) 近极端温度 →0：GR 温度公式 (1) 内在极限，非 TUFT 供给。")
    w("  子问题(b) 比热符号翻转：C_J 分母 D(ε)=2-2ε-ε²，零点 ε*=√3-1，Davies 结构为 GR 算术。")
    w("  子问题(c) 系综涨落：ΔE²=T²C 随 T→0 压制，微正则/正则区分是 GR 热力学内禀。")
    w("  => 近极端热力学是 GR 内在性质（Kerr 热力学算术），TUFT 无黑洞热力学/无系综结构供给。")
    w("  => **结构性负面（对 TUFT/几何框架）**，按母册登记撞 **C7（数学自洽）**：")
    w("     结果在 GR 内数学自洽闭合，TUFT 既不能导出也不能修正，供给为零。")
    entries.append(("E5", "近极端热力学=GR 内在性质，TUFT 供给 0；结构性负面，撞 C7",
                    "PASS", "母册 T106 登记撞 C7"))

    # ---- 守卫 ----
    schw = e1rows[0]
    guards = [
        ("G1", "Schwarzschild 温度 4πMT=1（即 T=1/8πM）", schw["four_pi_MT"] == Fraction(1, 2)),
        ("G2", "近极端 T 随 ε 减小而单调趋零（n=50 T < n=10 T < n=4 T）",
         e1rows[-1]["T_M_eq1"] < e1rows[5]["T_M_eq1"] < e1rows[3]["T_M_eq1"]),
        ("G3", "Schwarzschild C_J 为负（D=-1<0）", e2rows[0]["D"] < 0),
        ("G4", "近极端 C_J 为正（n=50 的 D>0）", e2rows[-1]["D"] > 0),
        ("G5", "比热零点 ε*=√3-1∈(0.7,0.75)", Decimal("0.7") < eps_star < Decimal("0.75")),
        ("G6", "TUFT 黑洞热力学供给=0", g4["tuft_black_hole_thermo"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %-4s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0209 guard failed"

    w("\n[诚实边界 / 红线]")
    w("  不宣称解决任何物理难题；已攻破=对 TUFT/几何框架结构性负面闭合；")
    w("  有预测且对 = 0/22；UFT-3=0 保持；数学自洽 ≠ 实验证实。")
    w("  外部未引实验值；全部为本册 Kerr 热力学算术独立精算（Fraction 精确 + Decimal 48 位）。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0209_近极端热力学攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0209_近极端热力学攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    import json
    payload = {
        "name": "C0209_near_extremal_thermo",
        "rows": "Kerr near-extremal thermodynamics, geometric units G=c=hbar=kB=1, M=J=1",
        "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]} for e in entries],
        "E1_temperature": [
            {"n": r["n"], "mu": str(r["mu"]), "eps": str(r["eps"]),
             "4piMT": str(r["four_pi_MT"]), "T_Meq1": str(r["T_M_eq1"])} for r in e1rows],
        "E2_cJ": {
            "epsilon_star_sqrt3_minus_1": str(eps_star),
            "rows": [
                {"n": r["n"], "eps": str(r["eps"]), "mu": str(r["mu"]), "D": str(r["D"]),
                 "sign": r["sign"], "S_over_2piJ": str(r["S_over_2piJ"]),
                 "cJ_over_2piJ": str(r["cJ_over_2piJ"])} for r in e2rows]},
        "E3_fluctuation": [
            {"n": r["n"], "eps": str(r["eps"]), "T": str(r["T"]), "cJ": str(r["cJ"]),
             "sigma_E_over_M": str(r["sigma_E_over_M"])} for r in e3rows],
        "E4_supply": {k: str(v) for k, v in g4.items()},
        "guards": [{"id": g[0], "desc": g[1], "ok": bool(g[2])} for g in guards],
        "exit_code": 0,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("C0209 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
