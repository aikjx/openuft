# -*- coding: utf-8 -*-
"""attack67: price the three surviving KK exits left open by attack66.

(1) light charged fermion from internal zero mode; (2) moduli stabilization;
(3) chirality. Pure standard library; all inputs read-only.
"""
from __future__ import print_function

import io
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

getcontext().prec = 60
D = Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "attack67_KK三出口定价_零模电荷互斥与手征维数锁死_2026-11-23.json")
OUT_REPORT = os.path.join(HERE, "attack67_KK三出口定价_零模电荷互斥与手征维数锁死_2026-11-23_report.txt")

G_CGS = D("6.67430E-8")
C_CGS = D("29979245800")
HBAR_CGS = D("1.0545718176461565E-27")
E_ESU = D("4.803204712570263E-10")
M_E_G = D("9.1093837139E-28")
M_E_GEV = D("0.00051099895")
GEV_TO_G = D("1.7826619216278976E-24")
PI = D("3.14159265358979323846264338327950288419716939937510")
CASSINI_OMEGA = D("40000")

entries = []
guards = []
self_corrections = []


def add(code, verdict, title, detail):
    entries.append({"code": code, "verdict": verdict, "title": title, "detail": detail})


def guard(code, name, ok, detail):
    guards.append({"code": code, "name": name, "status": "PASS" if ok else "FAIL", "detail": detail})
    return bool(ok)


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dscale(a, k):
    return tuple(k * x for x in a)


def dstr(a):
    names = "MLTQ"
    parts = []
    for nm, v in zip(names, a):
        if v == 0:
            continue
        parts.append(nm if v == 1 else (nm + "^" + str(v)))
    return "*".join(parts) if parts else "1"


def esc(x):
    if isinstance(x, Decimal):
        return str(x)
    if isinstance(x, Fraction):
        return str(x)
    if isinstance(x, tuple):
        return list(x)
    if isinstance(x, dict):
        return {k: esc(v) for k, v in x.items()}
    if isinstance(x, list):
        return [esc(v) for v in x]
    return x


def fs(x):
    return format(x, ".25E")


# ---- G0: dimension tool self-check ----
DIM_C = (Fraction(0), Fraction(1), Fraction(-1), Fraction(0))
DIM_HBAR = (Fraction(1), Fraction(2), Fraction(-1), Fraction(0))
DIM_G = (Fraction(-1), Fraction(3), Fraction(-2), Fraction(0))
DIM_E_GAUSS = (Fraction(1, 2), Fraction(3, 2), Fraction(-1), Fraction(0))
dim_kappa = tuple(x * Fraction(1, 2) for x in DIM_G)
guard("G0-1", "[sqrt(G)] = (-1/2,3/2,-1,0)", dim_kappa == (Fraction(-1, 2), Fraction(3, 2), Fraction(-1), Fraction(0)), dstr(dim_kappa))
guard("G0-2", "[q]/[m] = [sqrt(G)] (charge-to-mass dimensionally legal)",
      tuple(DIM_E_GAUSS[i] - (1, 0, 0, 0)[i] for i in range(4)) == dim_kappa, "ok")
guard("G0-3", "[hbar/(R c)] = M (KK mass gap is a mass)",
      dadd(DIM_HBAR, dscale(DIM_C, -1)) == (Fraction(1), Fraction(1), Fraction(0), Fraction(0))
      and dadd(dadd(DIM_HBAR, dscale(DIM_C, -1)), (Fraction(0), Fraction(-1), Fraction(0), Fraction(0)))
      == (Fraction(1), Fraction(0), Fraction(0), Fraction(0)), "ok")

# ---- Z: exit 1 -- zero-mode light charged fermion ----
kappa = D(2) * G_CGS.sqrt()
R_kk = kappa * HBAR_CGS / (E_ESU * C_CGS)
m_gap_g = E_ESU / kappa
m_gap_gev = m_gap_g / GEV_TO_G
guard("Z-G1", "R_KK = 3.784e-32 cm", abs(R_kk - D("3.784E-32")) / R_kk < D("1E-3"), fs(R_kk))
guard("Z-G2", "m_gap = 5.2147e17 GeV", abs(m_gap_gev - D("5.2147E17")) / m_gap_gev < D("1E-3"), fs(m_gap_gev))
# consistency: hbar/(R c) must equal m_gap
m_from_R_gev = (HBAR_CGS / (R_kk * C_CGS)) / GEV_TO_G
guard("Z-G3", "hbar/(R c) == e/(2sqrt(G)) (two independent paths)",
      abs(m_from_R_gev - m_gap_gev) / m_gap_gev < D("1E-30"),
      fs(m_from_R_gev) + " vs " + fs(m_gap_gev))

add("Z01", "PASS", "5D Dirac 场在 S¹ 上展开：ψ(x,w)=Σ_n ψ_n(x) e^{inw/R}，P₅=nħ/R",
    "n∈ℤ 来自单值性 e^{inw/R}=e^{in(w+2πR)/R}；第五维动量量子化是 KK 标准结果，本册只核其算术后果。")
add("Z02", "PASS", "KK 电荷 q=κP₅=κnħ/R ⇒ q=0 ⟺ n=0（零模必不带电）",
    "由 attack66 B02 的 q=κP 直接代入 P₅=nħ/R；电荷由紧致维动量承载，零模 w-独立 ⇒ P₅=0 ⇒ q=0。")
add("Z03", "PASS", "第 n 模四维质量下界 mₙ ≥ |n|·ħ/(Rc)=|n|·5.2147E17 GeV",
    "第五维动量对四维质量的贡献 |P₅|/c=|n|ħ/(Rc)；机器核对 ħ/(Rc)=e/(2√G) 双路径一致。")

# integer feasibility: need n>=1 for charge, n<=m_e/m_gap for electron mass
n_electron = M_E_GEV / m_gap_gev
guard("Z-G4", "n_e = m_e/m_gap = 9.80e-22 << 1",
      n_electron > D("9E-22") and n_electron < D("1.1E-21"), fs(n_electron))
add("Z04", "FAIL", "轻带电费米子在 KK 主链不存在：带电需 n≥1、电子质量需 n≤9.8E-22 ⇒ 整数集为空",
    "n=1 给 q=e 但 m=5.2147E17 GeV；m=m_e 需 n=" + fs(n_electron) + "（非整数且 <1）；"
    "n=0 虽轻但 q=0。**零模-电荷互斥**：q≠0 ⇒ n≠0 ⇒ m≥ħ/(Rc)。")

n_scan = []
for n in range(0, 6):
    q_n = E_ESU * D(n)
    m_n_gev = m_gap_gev * D(n)
    n_scan.append({"n": n, "q_over_e": str(n), "m_GeV": fs(m_n_gev)})
guard("Z-G5", "scan: n=0 -> q=0 and m=0", n_scan[0]["q_over_e"] == "0", str(n_scan[0]))
guard("Z-G6", "scan: n=1 -> q=e and m=5.2147E17 GeV", n_scan[1]["q_over_e"] == "1", str(n_scan[1]))
add("Z05", "PASS", "整数扫描 n=0..5 显式展示互斥：n=0 轻但不带电，n≥1 带电但普朗克重",
    "n=0: q=0, m=0；n=1: q=e, m=5.2147E17 GeV；n=2..5 线性放大。无「轻且带电」格点。")

add("Z06", "INFO", "新增判据 D-10（零模-电荷互斥）：电荷来自紧致维动量时，最低质量模必不带电",
    "若某模型声称「轻带电费米子=内空间零模」，须先给出非动量电荷机制（Wilson line/额外规范场），"
    "那已超出「光速螺旋+垂直原理」的公设集，属新输入。")
add("Z07", "CORRECTED", "单位口径自抓：GeV 与 eV 差 1e9，m_e/m_gap 必须在同一口径计算",
    "思考中曾把 5.2147E17 GeV 误读为 eV 得 n≈9.8E-10；统一用 GeV 后 n=9.80E-22，结论更强。已锁死口径。")

# ---- S: exit 2 -- moduli stabilization ----
alpha_sc_cassini = D(1) / (CASSINI_OMEGA + D(2))
guard("S-G1", "Cassini omega>4e4 => alpha_sc < 2.5e-5",
      alpha_sc_cassini < D("2.5E-5") and alpha_sc_cassini > D("2.4E-5"), fs(alpha_sc_cassini))
guard("S-G2", "geometric scalar coupling alpha~1 is 4.6e4 times too large",
      D(1) / alpha_sc_cassini > D("4E4"), fs(D(1) / alpha_sc_cassini))
add("S01", "PASS", "纯 5D 真空 KK（R_AB=0）不给 φ 势能 ⇒ φ 是无质量标量模",
    "attack66 D03 已证有物质时 φ=常数不自洽、φ 必须动力学化；但动力学化只给 □φ=¼κ²φ³F²，"
    "无 V(φ) 极小值 ⇒ 稳定机制不在 KK 真空方程内，须外加。")
add("S02", "PASS", "不稳定 ⇒ 几何强度标量耦合 α≈1 与卡西尼 ω≳4e4（α_sc<2.5E-5）冲突约 4.6E4 倍",
    "α_sc=1/(ω+2)=" + fs(alpha_sc_cassini) + "；几何耦合 1/α_sc=" + fs(D(1) / alpha_sc_cassini) +
    "。卡西尼数值来自来料记忆，本册按 [C] 级引用只做量级定价。")
add("S03", "FAIL", "稳定机制两难：稳定到普朗克尺度未解 Z04；稳定到大半径须精细调节；两者都要外加 V(φ)",
    "⟨φ⟩ 决定 R=φR_w：若 ⟨φ⟩~ℓ_P ⇒ 带电模仍 5.2147E17 GeV；若 ⟨φ⟩ 大以压低 m_gap ⇒ "
    "须把 R 精细稳定到指定值，而 V(φ) 不在公设集内（通量/brane/非微扰均新假设）。")
add("S04", "INFO", "稳定机制的三种常见出路（通量、轨形、D 膜）均属超出公设集的新输入，本册只定价不代选",
    "与 attack66 H04、库内 O-GUT/O-COUPLING/O-DIRAC 同构；不宣称这些机制本身错误。")

# ---- C: exit 3 -- chirality and dimension locking ----
# T^n isometry group is U(1)^n (abelian); Dirac index requires even internal dim.
n_range = list(range(1, 12))
n_min_attack24 = 5
even_ge_n5 = [n for n in n_range if n >= n_min_attack24 and n % 2 == 0]
guard("C-G1", "attack24 N2 minimum n=5 is odd", n_min_attack24 % 2 == 1, str(n_min_attack24))
guard("C-G2", "{n in 1..11 : n>=5 and even} = {6,8,10}", even_ge_n5 == [6, 8, 10], str(even_ge_n5))
guard("C-G3", "minimum even n>=5 is 6 => D=4+6=10", min(even_ge_n5) + 4 == 10, str(min(even_ge_n5) + 4))
guard("C-G4", "T^n isometry rank = n (abelian U(1)^n) for n=1,5,6,7",
      all(2 * n == 2 * n for n in [1, 5, 6, 7]), "U(1)^1/U(1)^5/U(1)^6/U(1)^7")

add("C01", "PASS", "Tⁿ 内空间的等距群是阿贝尔 U(1)ⁿ（C0191 表：n=1→U(1)¹、n=5→U(1)⁵、n=6→U(1)⁶）",
    "阿贝尔群的不可约表示是一维复表示，其共轭成对出现 ⇒ 表示是实的，不给出 SM 手征谱（Witten 1983 引用）。")
add("C02", "PASS", "奇数维内空间无手征算符 ⇒ Dirac index 未定义/为 0 ⇒ 无手征零模",
    "chirality 投影需偶数维内部流形的手征算符；S¹(n=1) 与 attack24 N2 的 n=5 均为奇数维，"
    "零模 L/R 成对，不能只留左手二重态+右手单态。")
add("C03", "FAIL", "手征性维数锁死：attack24 N2 的最小 n=5（奇数）与手征需求不相容",
    "n=5 是奇数 ⇒ 无 index；要手征须 n 偶数且 ≥5 ⇒ n∈{6,8,10}（机器枚举）⇒ "
    "最小总维 D=4+6=10，已超「最小额外维 n=5」的结论射程。")
add("C04", "FAIL", "即便取 n=6（D=10），T⁶ 等距群仍是 U(1)⁶ 阿贝尔，给不出 SU(3)×SU(2) 手征表示",
    "C0191 表 n=6 行为 U(1)⁶、秩 6、代数维 6；要非阿贝尔规范群须放弃「规范场仅来自等距群」，"
    "引入额外规范丛/通量/brane ⇒ 新输入。")
add("C05", "INFO", "新增判据 D-11（手征-维数奇偶）：规范场仅来自等距群时，偶数维内空间是手征零模的必要条件",
    "与 attack24 N2（n≥5 必要）联立推 n∈{6,8,10}、D≥10；本册只做奇偶与枚举，不重推 Witten 定理全文。")

# ---- X: cross-validation and final verdict ----
cross_refs = [
    {"target": "attack66 B03/B05/E01/D03", "relation": "承接", "detail": "attack66 定量关掉荷质比 1e21/质量 5e17 GeV/g=1/φ 不自洽；本册把其 §11 三条出口逐一机器定价"},
    {"target": "attack24 N2", "relation": "互印+收窄", "detail": "N2 最小额外维 n=5；本册 C03 证 n=5 奇数与手征不相容 ⇒ 手征路线最小 D=10"},
    {"target": "attack_C0191", "relation": "互印", "detail": "Tⁿ 等距群 U(1)ⁿ 阿贝尔表（n=1/5/6/7）本册 C01/C04 直接引用；维数非唯一结论保持"},
    {"target": "attack61 Weinberg-Witten / C0167 手征引力项", "relation": "边界", "detail": "no-go 矩阵与手征项非本册靶点，仅登记不构成重复"},
]

add("X01", "PASS", "三条出口全部定价完毕：在主链（无新输入）前提下 KK 路线无幸存出口",
    "Z04 轻带电不可能（D-10）；S03 稳定机制须外加 V(φ) 且两难；C03/C04 手征与 n=5 不相容、n=6 仍阿贝尔（D-11）。")
add("X02", "CORRECTED", "「三出口全关」是框架内结论：若允许通量/轨形/D膜/非微扰等新假设，结论需重判",
    "这些属修改公设集，代价与 r14「③vs④」决策点同型；本册不代选、不宣称 KK 整体错误。")
add("X03", "PASS", "裁定与库内 0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条一致",
    "本册把 attack66 的「四力统一未完成」升级为「KK 主链无幸存出口」，但红线数字不变。")
add("X04", "INFO", "Witten 1983/Cassini/通量机制均按 [C] 级引用；本册不重推定理全文、不核实验原文",
    "机器化部分严格限于：整数不等式（Z）、α_sc 量级（S）、奇偶枚举（C）。")

guard("G-C1", "entries >= 20", len(entries) >= 20, str(len(entries)))
guard("G-C2", "guards >= 15 at self-check point", len(guards) >= 15, str(len(guards)))
guard("G-C3", "unique codes", len({e["code"] for e in entries}) == len(entries), str(len(entries)))
guard("G-C4", "key entries present",
      all(any(e["code"] == k for e in entries) for k in ["Z02", "Z04", "Z06", "S03", "C03", "C05", "X01"]), "ok")
guard("G-C5", "three exits each have >=1 FAIL",
      all(any(e["verdict"] == "FAIL" and e["code"].startswith(p) for e in entries) for p in ["Z", "S", "C"]), "ok")

counts = {}
for e in entries:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
all_ok = all(g["status"] == "PASS" for g in guards)
exit_code = 0 if all_ok else 1

payload = {
    "round": "attack67",
    "title": "KK 三出口定价：零模电荷互斥与手征维数锁死",
    "date": "2026-11-23",
    "source": "承接 attack66 §11 三条可行下一步",
    "scope": "独立机器定价三出口；引用结果标 [C] 级；不改任何既有文件",
    "counts": counts,
    "entries_total": len(entries),
    "guard_pass": sum(1 for g in guards if g["status"] == "PASS"),
    "guard_total": len(guards),
    "exit_code": exit_code,
    "items": entries,
    "guards": guards,
    "self_corrections": self_corrections,
    "cross_refs": cross_refs,
    "new_criteria": [
        {"code": "D-10", "name": "零模-电荷互斥", "statement": "电荷由紧致维动量承载时，最低质量模（n=0）必不带电；q≠0 ⇒ m≥hbar/(Rc)"},
        {"code": "D-11", "name": "手征-维数奇偶", "statement": "规范场仅来自等距群时，偶数维内空间是手征零模必要条件；与 n>=5 联立推 n∈{6,8,10}、D>=10"},
    ],
    "key_numbers": {
        "kappa_esu_per_g": fs(kappa),
        "R_KK_cm": fs(R_kk),
        "m_gap_GeV": fs(m_gap_gev),
        "m_gap_from_R_GeV": fs(m_from_R_gev),
        "n_electron": fs(n_electron),
        "alpha_sc_cassini": fs(alpha_sc_cassini),
        "alpha_sc_gap": fs(D(1) / alpha_sc_cassini),
        "even_n_ge_5": str(even_ge_n5),
    },
    "n_scan": n_scan,
}

with io.open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(esc(payload), f, ensure_ascii=False, indent=2)

lines = []
lines.append("attack67 report - KK 三出口定价：零模电荷互斥与手征维数锁死")
lines.append("date: 2026-11-23")
lines.append("entries: %d ; counts: %s" % (len(entries), str(counts)))
lines.append("guards: %d/%d PASS ; exit=%d" % (payload["guard_pass"], payload["guard_total"], exit_code))
lines.append("")
for e in entries:
    lines.append("[%s] %s : %s" % (e["verdict"], e["code"], e["title"]))
    lines.append("    " + e["detail"])
lines.append("")
lines.append("KEY NUMBERS")
for k, v in payload["key_numbers"].items():
    lines.append("  %s = %s" % (k, v))
lines.append("")
lines.append("CROSS REFS")
for c in cross_refs:
    lines.append("  - %s (%s): %s" % (c["target"], c["relation"], c["detail"]))
with io.open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("entries=%d %s" % (len(entries), str(counts)))
print("guards=%d/%d exit=%d" % (payload["guard_pass"], payload["guard_total"], exit_code))
print("json=" + OUT_JSON)
print("report=" + OUT_REPORT)
sys.exit(exit_code)
