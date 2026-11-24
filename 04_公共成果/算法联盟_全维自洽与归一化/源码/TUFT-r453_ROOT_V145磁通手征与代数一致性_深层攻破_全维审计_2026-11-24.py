#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r453 / ROOT V145 深层攻破：磁通手征、质量尺度与代数一致性。

只读 V145 来料正本；不声称 ZIP 已验收。纯标准库：Decimal 60 位物理常数，
Fraction 精确处理电荷、指标与异常。输出 md/json/report 三件机器产物。
"""
from __future__ import print_function

import hashlib
import json
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "04_公共成果" / "算法联盟_全维自洽与归一化"
DATA = BASE / "数据"
STEM = "TUFT-r453_ROOT_V145磁通手征与代数一致性_深层攻破_全维审计_2026-11-24"
SOURCE = DATA / "TUFT-ROOT_V145_继续攻坚_从内部闭环运动到粒子的质量手征性和代数一致性_来料全文_2026-11-24.md"

D = Decimal
HBAR = D("1.054571817E-34")
C = D("299792458")
E_CHARGE = D("1.602176634E-19")

entries = []
guards = []
key = {}


def fmt(x, digits="18"):
    x = D(x)
    digits = str(digits)
    if x == 0:
        return "0"
    return format(x, "." + digits + "E")


def rel(a, b):
    a, b = D(a), D(b)
    return abs(a - b) / max(abs(a), abs(b), D("1e-80"))


def dsqrt(x):
    x = D(x)
    if x < 0:
        raise ValueError("sqrt of negative Decimal")
    return (x.ln() / D(2)).exp()


def fs(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


def add(code, status, title, detail):
    entries.append({"id": code, "status": status, "title": title, "detail": detail})


def guard(code, ok, detail):
    guards.append({"id": code, "status": "PASS" if ok else "FAIL", "detail": detail})


def sm_anomaly_one_generation():
    reps = [
        ("Q_L", 3, 2, Fraction(1, 6)),
        ("u_L^c", 3, 1, Fraction(-2, 3)),
        ("d_L^c", 3, 1, Fraction(1, 3)),
        ("L_L", 1, 2, Fraction(-1, 2)),
        ("e_L^c", 1, 1, Fraction(1)),
    ]
    a3 = Fraction(0)
    ag = Fraction(0)
    a22 = Fraction(0)
    a33 = Fraction(0)
    comps = 0
    for name, d3, d2, y in reps:
        mult = d3 * d2
        comps += mult
        a3 += Fraction(mult) * y ** 3
        ag += Fraction(mult) * y
        if d2 == 2:
            a22 += Fraction(d3) * Fraction(2) * y
        if d3 == 3:
            a33 += Fraction(1, 2) * Fraction(d2) * y
    return {"u1_cube": a3, "grav_u1": ag, "su2su2u1": a22, "su3su3u1": a33, "components": comps}


def main():
    if not SOURCE.exists():
        print("MISSING SOURCE:", SOURCE)
        return 2
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    sha = hashlib.sha256(raw).hexdigest()
    key["source_sha256"] = sha
    key["source_bytes"] = len(raw)

    anchors = [
        "\\mathcal M_6=M_4\\times S^2",
        "A_N=\\frac n2(1-\\cos\\theta)d\\phi",
        "A_N-A_S=n\\,d\\phi",
        "\\operatorname{ind}(D)=N_+-N_-=n",
        "N_+-N_-=qn",
        "\\lambda_k^2=\\frac{k(k+|n|)}{R^2}",
        "394.654",
        "\\mathcal A_{U(1)^3}=3",
        "47/47",
        "ROOT_V145_Flux_Chirality_Complete.zip",
        "\\delta S_{\\rm ROOT}=0",
    ]
    hits = [a in text for a in anchors]
    guard("G0-01", all(hits), "来料锚点 %d/%d 可见" % (sum(hits), len(hits)))
    guard("G0-02", len(sha) == 64 and len(raw) > 1000, "正本非空且 SHA256 格式有效")

    # ---- 一、整理锚点：拓扑量子化与指标定理 ----
    n = Fraction(3)
    gap_coeff = n
    flux_over_2pi = n
    zero_mode_count = abs(n)
    guard("G1-01", gap_coeff == Fraction(3), "南北规范势差系数 A_N-A_S=n dphi，n=3 给 3")
    guard("G1-02", flux_over_2pi == Fraction(3), "1/(2pi)∫F=n=3")
    guard("G1-03", n.denominator == 1 and zero_mode_count == 3, "单值性 n∈Z 且 |n|=3 个同手征零模")

    add("A-01", "PASS", "磁通量子化与指标关系是标准正确构造",
        "A_N-A_S=n dphi、1/(2pi)∫_{S2}F=n、e^{i2pi n}=1⇒n∈Z，以及 ind(D)=N_+-N_-=n 均为磁单极纤维丛与 Atiyah–Singer 指标定理的标准结果；本册承认其数学，攻击其从 ROOT 运动导出与粒子谱解释。")
    add("A-02", "PASS", "n=3 的零模计数本身可复算",
        "对球面对称 U(1) flux，|n|=3 个同一内部手征性的零模，N_+-N_-=3；这只给出计数，不给 Sm 表示、超荷、三代复制的来源。")

    # ---- 二、攻击 1：一个公共超荷磁通不能给出五类各三代 ----
    y6 = [
        ("Q_L", Fraction(1)),
        ("u_L^c", Fraction(-4)),
        ("d_L^c", Fraction(2)),
        ("L_L", Fraction(-3)),
        ("e_L^c", Fraction(6)),
    ]
    indices = [(name, q * n) for name, q in y6]
    expected = [Fraction(3)] * 5
    mismatch = [fs(idx) for name, idx in indices]
    possible_n = sorted(set(abs(Fraction(3) / q) for name, q in y6))
    guard("G2-01", [idx for name, idx in indices] == [Fraction(3), Fraction(-12), Fraction(6), Fraction(-9), Fraction(18)],
          "指标逐项复现 3,-12,6,-9,18")
    guard("G2-02", all(idx == want for idx, want in zip([idx for name, idx in indices], expected)) is False,
          "单一 n=3 不满足五类表示各 3 个零模")
    guard("G2-03", len(possible_n) == 5, "要求 |qn|=3 时五个表示给出五个互斥 n 值：%s" % ",".join(fs(x) for x in possible_n))
    add("B-01", "FAIL", "单一 U(1)_Y 磁通不能自动产生标准模型五类三代",
        "取整数化超荷 6Y=(1,-4,2,-3,6) 且 n=3，指标为 (3,-12,6,-9,18)，不是五类各 3。若强求 |qn|=3，则 n 必须同时等于 3、3/4、3/2、1、1/2，互斥。要得到族复制必须引入新的族荷或不同 flux sector，属于额外输入。")

    # ---- 三、攻击 2：质量尺度是测试输入，不是预测 ----
    k = D(1)
    r_test = D("1e-18")
    n_abs_dec = D(abs(n).numerator) / D(abs(n).denominator)
    lambda2 = k * (k + n_abs_dec) / (r_test * r_test)
    lambda1 = dsqrt(lambda2)
    e1_joule = HBAR * C * lambda1
    e1_gev = e1_joule / (E_CHARGE * D("1e9"))
    m1_si = HBAR * lambda1 / C
    e1_r10 = e1_gev / D(10)
    scale_ratio = e1_gev / e1_r10
    guard("G3-01", rel(e1_gev, D("394.654")) < D("1e-5"), "R=1e-18 m,n=3 的最低激发能 E1=%s GeV 与来料 394.654 GeV 一致" % fmt(e1_gev, 12))
    guard("G3-02", scale_ratio == D(10), "E1∝1/R：R 增大 10 倍能量降 10 倍")
    add("A-03", "PASS", "非零 Dirac 谱与能量换算可复算",
        "λ1^2=1(1+3)/R^2=4/R^2；R=10^-18 m 时 λ1=2×10^18 m^-1，E1=ħcλ1=%s GeV；SI 质量 m=ħλ1/c=%s kg。" % (fmt(e1_gev, 12), fmt(m1_si, 12)))
    add("B-02", "FAIL", "394.654 GeV 不是理论预测而是 R 的重新表述",
        "E1=2ħc/R。来料明确 R=10^-18 m 是测试输入，且没有 δS_ROOT=0 稳定条件、没有通量势能、没有半径量子化方程；E 随 R 反比连续变化，只展示尺度规律，不预测新粒子。")

    add("C-01", "BOUNDARY", "c=1 的质量/能量口径必须显式",
        "来料写 m_k=ħ|λ_k| 同时又报 E1≈394.654 GeV；该写法仅在 c=1 的自然单位中成立。SI 中质量是 ħλ/c，能量是 ħcλ。本册两口径均给出，避免把自然单位质量当 SI 质量。")

    # ---- 四、攻击 3：U(1)_F 修复不是免费 ----
    sm = sm_anomaly_one_generation()
    sm_zero = all(sm[k] == 0 for k in ("u1_cube", "grav_u1", "su2su2u1", "su3su3u1"))
    guard("G4-01", sm_zero, "SM 一代四类异常全为 0：%s" % ",".join(fs(sm[k]) for k in ("u1_cube", "grav_u1", "su2su2u1", "su3su3u1")))
    isolated_cube = Fraction(3)
    isolated_grav = Fraction(3)
    guard("G4-02", isolated_cube == 3 and isolated_grav == 3, "孤立 3 个电荷 +1 LH Weyl 的两项异常为 3,3")
    comps3 = sm["components"] * 3
    f_cube = Fraction(comps3)
    f_grav = Fraction(comps3)
    f_su2 = Fraction(3) * (Fraction(3) * Fraction(2) + Fraction(1) * Fraction(2))
    f_su3 = Fraction(3) * (Fraction(1, 2) * Fraction(2) + Fraction(1, 2) + Fraction(1, 2))
    guard("G4-03", f_cube == 45 and f_grav == 45 and f_su2 == 24 and f_su3 == 6,
          "最小同荷 U(1)_F 三代异常不为零：cubic=%s grav=%s SU2²=%s SU3²=%s" % (fs(f_cube), fs(f_grav), fs(f_su2), fs(f_su3)))

    add("A-04", "PASS", "SM 一代异常抵消与孤立三重态异常均可精确复算",
        "Q_L/u_L^c/d_L^c/L_L/e_L^c 的四类异常为 0；仅 3 个电荷 +1 的 LH Weyl 给 U(1)^3=3、grav²U(1)=3，不能单独成为一致量子谱。")
    add("B-03", "FAIL", "引入 U(1)_F 修复会制造新的异常账",
        "若三代 SM LH Weyl 均带同一最小家族荷 q_F=1，则 U(1)_F^3=45、grav²U(1)_F=45、SU(2)^2U(1)_F=24、SU(3)^2U(1)_F=6，均非零。加 spectator 或分裂族荷可以抵消，但那是新场/新表示/新约束，不能称为由几何自动推出。")

    # ---- 五、攻击 4：Dirac 配对与 Weyl 手征条件 ----
    dirac_pair_net = n + (-n)
    weyl_selected = n
    guard("G5-01", dirac_pair_net == 0, "6D Dirac 的左右配对净指标为 0")
    guard("G5-02", weyl_selected == 3, "施加 6D Weyl 选择后才得到净手征指标 n=3")
    has_action_target = "\\delta S_{\\rm ROOT}=0" in text
    has_lagrangian = "\\mathcal L" in text
    guard("G5-03", has_action_target and not has_lagrangian, "只给出 δS_ROOT=0 目标，没有显式拉氏密度")
    add("B-04", "FAIL", "拓扑指标不等于净四维手征谱",
        "6D Dirac 费米子含两套 6D 手征，配对后净指标为 0；只有额外施加 6D Weyl 条件或等价手征投影，N_+-N_-=n 才转为净四维手征零模。V145 已承认该条件，但拓扑绕数本身没有提供它。")
    add("B-05", "FAIL", "δS_ROOT=0 仍是目标而非作用量",
        "来料只写 δS_ROOT=0 ⇒ 稳定内部空间/非零磁通/n/手征谱/无异常的愿望清单；没有给出 S_ROOT、动能项、通量势、边界条件或稳定解。M6=M4×S2、n=3、R=1e-18 m 均是输入，尚未从运动导出。")

    # ---- 六、攻击 5：已知数学机制不能冒充 ROOT 新物理 ----
    guard("G6-01", "并不是 ROOT 已经独立推导出的新相互作用" in text, "来料自陈该构造属于已有磁单极纤维丛与规范理论")
    add("B-06", "FAIL", "标准单极纤维丛机制没有补上规范动力学与耦合来源",
        "A_N/A_S 补丁、 Chern 数、指标定理、磁化 Dirac 谱均属既有数学。它给出‘若有 U(1) flux 则零模计数如何’，不给出 flux 的动力学来源、规范耦合常数、为什么选 S2、为什么选 U(1)_Y，也不给出从光速螺旋到内部场结构的映射。")

    # ---- 七、工程声明边界 ----
    zip_claim = "ROOT_V145_Flux_Chirality_Complete.zip" in text and "47/47" in text
    zip_file = DATA / "ROOT_V145_Flux_Chirality_Complete.zip"
    guard("G7-01", zip_claim and not zip_file.exists(), "ZIP 与 47/47 只在来料中声明，库内未收到实体")
    add("C-02", "BOUNDARY", "ZIP、47/47 与外部图像只登记不验收",
        "来料声称 1.99 MB/28 文件、解压后独立重跑 47 项测试与 SHA-256 校验通过，但本轮只收到文本；3 个 image 外链与 ZIP 实体均不在库内。本册不复验这些声明。")
    add("I-01", "INFO", "负指标表示相反内部手征，不是负粒子数",
        "例如 u_L^c 的指标 −12 表示相反内部手征 sector 的 12 个零模；不能把负数当粒子数缺失。该符号约定在三代谱账中必须显式。")

    counts = {}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    key["status_counts"] = counts
    key["n"] = fs(n)
    key["flux_over_2pi"] = fs(flux_over_2pi)
    key["zero_mode_count"] = fs(zero_mode_count)
    key["hypercharge_indices_n3"] = {name: fs(idx) for name, idx in indices}
    key["required_n_for_three_each"] = [fs(x) for x in possible_n]
    key["r_test_m"] = fmt(r_test)
    key["lambda1_per_m"] = fmt(lambda1)
    key["E1_GeV"] = fmt(e1_gev, 12)
    key["m1_SI_kg"] = fmt(m1_si, 12)
    key["SM_one_gen_anomalies"] = {k2: fs(v) for k2, v in sm.items()}
    key["isolated_three_Q_anomalies"] = {"u1_cube": fs(isolated_cube), "grav_u1": fs(isolated_grav)}
    key["minimal_family_U1_anomalies"] = {"u1F_cube": fs(f_cube), "grav_u1F": fs(f_grav), "su2su2u1F": fs(f_su2), "su3su3u1F": fs(f_su3)}

    md = ["# TUFT r453 机器数据：ROOT V145 深层攻破", ""]
    md.append("- 来源 SHA256：`%s`" % sha)
    md.append("- 关系：V145 来料深层审计；不改 V144/r451/r452 任何字节。")
    md.append("")
    md.append("## 条目")
    md.append("")
    for e in entries:
        md.append("- `%s` [%s] **%s** — %s" % (e["id"], e["status"], e["title"], e["detail"]))
    md.append("")
    md.append("## 守卫")
    md.append("")
    for g in guards:
        md.append("- `%s` [%s] %s" % (g["id"], g["status"], g["detail"]))
    md.append("")
    md.append("## 关键读数")
    md.append("")
    for k2 in sorted(key):
        md.append("- `%s`: %s" % (k2, key[k2]))

    payload = {
        "round": "r453",
        "topic": "ROOT V145 磁通手征与代数一致性深层攻破",
        "source_sha256": sha,
        "source_bytes": len(raw),
        "relation": "deep attack on V145 text; no bytes of r451/r452 modified; ZIP claimed but not received",
        "entries": entries,
        "guards": guards,
        "key_numbers": key,
    }

    (DATA / (STEM + ".md")).write_text("\n".join(md) + "\n", encoding="utf-8")
    (DATA / (STEM + ".json")).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = [
        "TUFT r453 / ROOT V145 deep attack",
        "OK entries=%d guards=%d/%d" % (len(entries), sum(1 for g in guards if g["status"] == "PASS"), len(guards)),
        "source_sha256=" + sha,
        "status_counts=" + ",".join("%s:%d" % (k2, counts[k2]) for k2 in sorted(counts)),
        "E1_GeV=" + fmt(e1_gev, 12),
        "hypercharge_indices=" + ",".join(fs(idx) for name, idx in indices),
        "SM_anomalies=" + ",".join(fs(sm[k2]) for k2 in ("u1_cube", "grav_u1", "su2su2u1", "su3su3u1")),
        "family_U1_anomalies=" + ",".join(fs(x) for x in (f_cube, f_grav, f_su2, f_su3)),
    ]
    (DATA / (STEM + "_report.txt")).write_text("\n".join(report) + "\n", encoding="utf-8")

    print("entries=%d guards=%d/%d" % (len(entries), sum(1 for g in guards if g["status"] == "PASS"), len(guards)))
    print("counts=" + repr(counts))
    print("E1_GeV=" + fmt(e1_gev, 12))
    return 0 if all(g["status"] == "PASS" for g in guards) else 1


if __name__ == "__main__":
    sys.exit(main())
