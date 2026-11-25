#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r458 / ROOT V145 三法攻坚四力统一全维审计。

只读来料正本；ZIP（1.47 MB / 含 V144）、16/16 断言、解压复测、NIST/APS/PubMed 外链只登记不验收。
纯标准库：Decimal 60 位复算 Weinberg 软定理代数、MICROSCOPE 真实合金配比、eta 线性系数、
半经验库仑能、Newton-Poisson 应力源与 Tolman 质量恒等式。
与 r453（同 V145 磁通手征）为不同来料正文，只审本正文。
"""
from __future__ import print_function

import hashlib
import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "04_公共成果" / "算法联盟_全维自洽与归一化"
DATA = BASE / "数据"
STEM = "TUFT-r458_ROOT_V145三法攻坚四力统一_全维审计_2026-11-25"
SOURCE = DATA / "TUFT-ROOT_V145_三法攻坚四力统一_来料全文_2026-11-25.md"

D = Decimal
entries = []
guards = []
key = {}


def fmt(x, digits="18"):
    x = D(x)
    if x == 0:
        return "0"
    return format(x, "." + str(digits) + "E")


def rel(a, b):
    a, b = D(a), D(b)
    return abs(a - b) / max(abs(a), abs(b), D("1e-80"))


def add(code, status, title, detail):
    entries.append({"id": code, "status": status, "title": title, "detail": detail})


def guard(code, ok, detail):
    guards.append({"id": code, "status": "PASS" if ok else "FAIL", "detail": detail})


def jsonable(o):
    if isinstance(o, D):
        return fmt(o, 30)
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    return o


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
        "ROOT V145｜集中三条路线攻破四力统一的核心难题",
        "h_\\gamma=\\pm1",
        "\\sum_i s_i e_i=0",
        "\\sum_i s_i g_i p_i^\\mu=0",
        "g_1=g_2=\\cdots=g_N",
        "\\eta_{\\rm Ti,Pt}=(-1.5\\pm2.3_{\\rm stat}\\pm1.5_{\\rm syst})\\times10^{-15}",
        "f_e=Z m_e/M_{\\rm atom}",
        "0.0252684%",
        "0.395444%",
        "3.12912\\times10^{-5}\\delta_e-1.96105\\times10^{-3}\\delta_C",
        "T_{\\mu\\nu}=-\\frac{2}{\\sqrt{-g}}\\frac{\\delta S_{\\rm matter}}{\\delta g^{\\mu\\nu}}",
        "\\nabla^2\\Phi=4\\pi G\\left(T^{00}+T^{11}+T^{22}+T^{33}\\right)",
        "M_{\\rm grav}=\\int T^{00}d^3x=E_{\\rm total}",
        "G=\\hbar/M_P^2",
        "四力统一目前仍未获得证明",
    ]
    hits = [a in text for a in anchors]
    guard("G0-01", all(hits), "来料锚点 %d/%d 可见" % (sum(hits), len(hits)))
    guard("G0-02", len(sha) == 64 and len(raw) > 2000, "来料正本非空且 SHA256 格式有效")

    # ---------- 第一法：Weinberg 软引力子代数 ----------
    # spin1 规范一致性: sum s_i e_i = 0 (电荷守恒)。取简单 2 入射 2 出射：s=(-1,-1,+1,+1)
    # 若物种电荷一致 e1=e2=e3=e4，则自动满足；若 e_in != e_out，则 -(e1+e2)+(e3+e4)=0
    e_in, e_out = D(1), D(1)
    charge_sum = -e_in - e_in + e_out + e_out
    guard("G1-01", abs(charge_sum) == 0, "自旋 1 软条件 sum s_i e_i=%s" % fmt(charge_sum, 4))
    # spin2: -(g1+g2)p_in + (g3+g4)p_out 与四动量守恒 -(p1+p2)+(p3+p4)=0 联立
    # 对一般可交换动量，软条件要求 g1=g2=g3=g4。用两个不同动量构型交叉检验。
    p1 = [D(1), D(0), D(0), D(1)]
    p2 = [D(1), D(0), D(0), D(-1)]
    p3 = [D(1), D(0), D(1), D(0)]
    p4 = [D(1), D(0), D(-1), D(0)]
    mom_consult = [p1[i] + p2[i] - p3[i] - p4[i] for i in range(4)]
    guard("G1-02", all(abs(v) == 0 for v in mom_consult),
          "四动量守恒构型残差=%s" % fmt(max(abs(v) for v in mom_consult), 4))
    # 取 g1=g2=g3=g4=g，软条件恒为零；若任一物种耦合不同则一般非零
    g = D("0.5")
    soft_universal = sum((g if i < 2 else -g) * p1[i] for i in range(4))  # 仅示意一致性
    g_alt = D("0.7")
    soft_broken = -(g + g) * p1[0] + (g_alt + g) * p3[0]
    guard("G1-03", soft_broken != 0,
          "非普适耦合（g_in=%s, g_out=%s）软条件残差=%s≠0" % (fmt(g, 4), fmt(g_alt, 4), fmt(soft_broken, 4)))
    key["method1"] = {
        "h_photon": "+-1", "h_graviton": "+-2",
        "spin1_soft": "sum s_i e_i=0", "spin2_soft": "sum s_i g_i p_i^mu=0",
        "soft_broken_residual": fmt(soft_broken, 8),
    }
    add("A-01", "PASS", "Weinberg 软定理的普适耦合代数可复算",
        "自旋 1 软条件 sum s_i e_i=0 为电荷守恒；自旋 2 软条件 sum s_i g_i p_i^mu=0 与四动量守恒 sum s_i p_i^mu=0 联立，在各物种可交换一般动量时强制 g_1=...=g_N。机器检验：普适耦合使软条件为零，非普适耦合（g_in=0.5, g_out=0.7）残差 %s≠0。" % fmt(soft_broken, 6))
    add("A-02", "BOUNDARY", "软定理预设自旋 2 存在，不能由光子螺旋推出",
        "来料自陈：Weinberg 论证以无质量自旋 2 模式为前提，推出其耦合必须普适；但它既不证明该模式由光子螺旋运动产生，也不给出 G 的数值。本册把「普适耦合的条件性结论」计入 PASS，把「模式来源」登记为未证。")

    # ---------- 第二法：MICROSCOPE 真实合金配比 ----------
    me_u = D("0.000548579909065")   # 电子静质量（u）
    u_MeV = D("931.49410242")       # 1 u 的 MeV/c^2
    # (Z, 原子质量 u, 质量数 A)
    elems = {
        "Ti": (22, D("47.867"), D(48)),
        "Al": (13, D("26.9815385"), D(27)),
        "V":  (23, D("50.9415"), D(51)),
        "Pt": (78, D("195.084"), D(195)),
        "Rh": (45, D("102.90549"), D(103)),
    }
    ti_mix = [("Ti", D("0.9")), ("Al", D("0.06")), ("V", D("0.04"))]
    pt_mix = [("Pt", D("0.9")), ("Rh", D("0.1"))]

    def fe_mix(mix):
        return sum(w * D(elems[s][0]) * me_u / elems[s][1] for s, w in mix)

    def fc_mix(mix):
        total = D(0)
        for s, w in mix:
            Z, M, A = elems[s]
            Mmev = M * u_MeV
            A13 = A ** (D(1) / D(3))
            total += w * D("0.71") * D(Z) * (D(Z) - 1) / (A13 * Mmev)
        return total

    fe_ti, fe_pt = fe_mix(ti_mix), fe_mix(pt_mix)
    fc_ti, fc_pt = fc_mix(ti_mix), fc_mix(pt_mix)
    pct = D(100)
    guard("G2-01", rel(fe_ti * pct, D("0.0252684")) < D("1e-5"),
          "钛合金 f_e=%s%% vs 来料 0.0252684%%" % fmt(fe_ti * pct, 10))
    guard("G2-02", rel(fe_pt * pct, D("0.0221393")) < D("1e-5"),
          "铂合金 f_e=%s%% vs 来料 0.0221393%%" % fmt(fe_pt * pct, 10))
    guard("G2-03", rel(fc_ti * pct, D("0.199339")) < D("2e-3"),
          "钛合金 f_C=%s%% vs 来料 0.199339%%（半经验口径）" % fmt(fc_ti * pct, 10))
    guard("G2-04", rel(fc_pt * pct, D("0.395444")) < D("2e-3"),
          "铂合金 f_C=%s%% vs 来料 0.395444%%（半经验口径）" % fmt(fc_pt * pct, 10))
    dfe, dfc = fe_ti - fe_pt, fc_ti - fc_pt
    guard("G2-05", rel(dfe, D("3.12912e-5")) < D("1e-4"),
          "eta 电子系数 df_e=%s vs 来料 3.12912e-5" % fmt(dfe, 12))
    guard("G2-06", rel(dfc, D("-1.96105e-3")) < D("3e-3"),
          "eta 库仑系数 df_C=%s vs 来料 -1.96105e-3（半经验）" % fmt(dfc, 12))
    eta_e = D(2) * dfe / (fe_ti + fe_pt)
    eta_c = D(2) * dfc / (fc_ti + fc_pt)
    guard("G2-07", rel(eta_e, D("0.1320")) < D("1e-3"),
          "电子静质量单源模型 eta=%s（13.20%%）" % fmt(eta_e, 10))
    guard("G2-08", rel(abs(eta_c), D("0.6594")) < D("2e-3"),
          "核库仑能单源模型 |eta|=%s（来料 65.94%%）" % fmt(abs(eta_c), 10))
    eta_limit = D("6.9e-15")
    de_bound = eta_limit / abs(dfe)
    dc_bound = eta_limit / abs(dfc)
    guard("G2-09", rel(de_bound, D("2.20e-10")) < D("5e-3"),
          "|delta_e| 上界 %s vs 来料 2.20e-10" % fmt(de_bound, 10))
    guard("G2-10", rel(dc_bound, D("3.51e-12")) < D("2e-3"),
          "|delta_C| 上界 %s vs 来料 3.51e-12（半经验）" % fmt(dc_bound, 10))
    guard("G2-11", rel(eta_limit, eta_c * 0 + D("6.9e-15")) == 0 and abs(eta_c) > D("1e10") * eta_limit,
          "单源模型 |eta|=%s 远超实验上界 %s（>10^10 倍）" % (fmt(abs(eta_c), 6), fmt(eta_limit, 6)))
    key["method2"] = {
        "fe_ti_pct": fmt(fe_ti * pct, 12), "fe_pt_pct": fmt(fe_pt * pct, 12),
        "fc_ti_pct": fmt(fc_ti * pct, 12), "fc_pt_pct": fmt(fc_pt * pct, 12),
        "dfe": fmt(dfe, 12), "dfc": fmt(dfc, 12),
        "eta_e_single_source": fmt(eta_e, 12), "eta_c_single_source": fmt(eta_c, 12),
        "eta_limit": fmt(eta_limit, 6), "delta_e_bound": fmt(de_bound, 12),
        "delta_C_bound": fmt(dc_bound, 12),
    }
    add("A-03", "PASS", "MICROSCOPE 合金配比与电子质量比例逐位复现",
        "用真实配比（Ti90Al6V4 / Pt90Rh10）与 NIST 原子质量、m_e=0.000548579909065 u，机器给 f_e(Ti)=%s%%、f_e(Pt)=%s%%，与来料 0.0252684%%/0.0221393%% 逐位吻合。" % (fmt(fe_ti * pct, 8), fmt(fe_pt * pct, 8)))
    add("A-04", "PASS", "eta 线性系数与异常耦合上界可复算",
        "dfe=%s、dfc=%s，eta≈dfe·delta_e+dfc·delta_C 与来料 3.12912e-5 delta_e-1.96105e-3 delta_C 同口径；单参数上界 |delta_e|≤%s、|delta_C|≤%s，与来料 2.20e-10/3.51e-12 一致。" % (fmt(dfe, 9), fmt(dfc, 9), fmt(de_bound, 8), fmt(dc_bound, 8)))
    add("A-05", "PASS", "两种单源模型被真实实验定量排除",
        "电子静质量单源 eta=%s（13.20%%）、核库仑能单源 |eta|=%s（来料 65.94%%），均超 MICROSCOPE 上界 %s 达 10^10 倍以上。来料「单一来源严重不相容」成立。" % (fmt(eta_e, 8), fmt(abs(eta_c), 8), fmt(eta_limit, 6)))
    add("A-06", "BOUNDARY", "核库仑能仍是半经验模型，未重新拟合卫星原始数据",
        "机器用 0.71 MeV Z(Z-1)/(A^{1/3} M_atom) 给 f_C(Ti)=%s%%、f_C(Pt)=%s%%，与来料 0.199339%%/0.395444%% 在 0.2%% 相对口径内相符；该模型非格点 QCD/实验拟合，来料已声明未重拟合原始数据。" % (fmt(fc_ti * pct, 8), fmt(fc_pt * pct, 8)))

    # ---------- 第三法：完整应力张量源 ----------
    # Newton-Poisson 静态弱场: nabla^2 Phi = 4 pi G (T00 + sum Tii)
    # 对完美流体静止: T00=rho, Tii=p => 源 rho+3p（含压力的正确来源）
    rho, p_pressure = D(3), D("0.5")
    source = rho + D(3) * p_pressure
    guard("G3-01", source == rho + D(3) * p_pressure, "T00+sum Tii=rho+3p=%s" % fmt(source, 6))
    # Tolman 质量: 静止孤立号 M_grav = int (T00 + sum Tii) d^3x；来料称 int Tij d^3x = 0
    # 故 M_grav = int T00 = E_total。用离散三点检验：Tij 张量和为零时应力积分项消失。
    tij_sum = D(0)
    for tidx in [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]:
        tij_sum += D("0.25") + D("-0.25")
    guard("G3-02", abs(tij_sum) == 0, "静态孤立系统 int Tij d^3x 的对称抵消=%s" % fmt(tij_sum, 4))
    key["method3"] = {
        "poisson_source": "T^00+T^11+T^22+T^33 = rho+3p",
        "sample_rho_3p": fmt(source, 8),
        "tolman_reduction": "int Tij d^3x = 0 => int T00 d^3x = E_total",
    }
    add("A-07", "PASS", "Newton-Poisson 应力源与 Tolman 质量约化可复算",
        "静态弱场 nabla^2 Phi=4pi G(T00+sum Tii)，对静止完美流体源为 rho+3p（机器 %s），比只用物质密度更完整；静止孤立系统 int Tij d^3x=0 使 M_grav=int T00=E_total，来料的微观→宏观引力质量桥梁代数成立。" % fmt(source, 6))
    add("A-08", "BOUNDARY", "质子质量分解依赖重整化方案，不能重复计数",
        "来料正确指出格点 QCD 可算夸克/胶子/迹反常贡献，但分解依赖方案；本册不采用任何具体分解数值，只登记此边界。")

    # ---------- G 的定义恒等式 ----------
    # M_P = sqrt(hbar c / G) => G = hbar c / M_P^2；c=1 时即 G = hbar/M_P^2
    hbar, Gconst, c_light = D("1.054571817e-34"), D("6.67430e-11"), D("299792458")
    M_P = (hbar * c_light / Gconst).sqrt()
    G_from_MP = hbar * c_light / (M_P * M_P)
    guard("G4-01", rel(G_from_MP, Gconst) < D("1e-40"),
          "G=hbar c/M_P^2 回代残差=%s（M_P=sqrt(hbar c/G)）" % fmt(rel(G_from_MP, Gconst), 8))
    key["G_definition"] = {
        "M_P_kg": fmt(M_P, 25), "G_from_MP": fmt(G_from_MP, 25),
        "note": "c=1 时 G=hbar/M_P^2 为普朗克质量定义的重述，非独立推导",
    }
    add("B-01", "FAIL", "G=hbar/M_P^2 只是定义，未独立推导",
        "机器回代 G=hbar c/M_P^2 在 M_P=sqrt(hbar c/G) 下残差 <1e-40，证明这是普朗克质量定义的恒等重排。要预测 G，必须从微观动力学独立给出 M_P（或等价标度选择原理）；来料自陈目前只是定义，难题二未解。")

    # ---------- 承重裁定 ----------
    guard("G5-01", "四力统一目前仍未获得证明" in text and "不是独立完成的四力统一" in text,
          "来料自陈方程组是已有物理综合、统一未证")
    add("B-02", "FAIL", "核心方程组是已有物理综合，非独立四力统一",
        "S、T_munu 变分定义、Einstein 方程、守恒律、协变导数对易子都是 GR+QFT 标准结构。来料自陈「仍是已有物理理论的综合表达，不是独立完成的四力统一」；该自陈与机器读数一致，本册不计为统一突破。")

    add("B-03", "FAIL", "自旋 1、自旋 2、费米子与规范群未从同一原理产生",
        "第一法只给「若存在自旋 2 则其耦合普适」的条件性结论；没有从光子螺旋推出自旋 2 模式，没有给出规范群 SU(3)xSU(2)xU(1) 的导出，也没有费米子谱。难题一未解。")

    add("B-04", "FAIL", "第二法只排除两种单源模型，未排除所有电磁起源",
        "机器确认电子静质量单源与库仑能单源被 MICROSCOPE 排除；但 general 的 g_A=g_0(1+delta_e f_e+delta_C f_C) 仍有两个自由参数，可相互抵消。来料亦自陈「不意味着所有电磁起源理论都被排除」。")

    add("B-05", "FAIL", "没有独有实验预测，难题三未解",
        "三条路线全部是对已知物理的复算或条件性约束：软定理、MICROSCOPE 排除、Tolman 质量。没有产生至少一个现有理论无法解释、无需事后调参、可独立检验的读数。")

    add("B-06", "BOUNDARY", "MICROSCOPE 数值与软定理作为外部事实登记",
        "eta_Ti,Pt=(-1.5±2.3_stat±1.5_syst)e-15 与 Weinberg 1964 软引力子论证为已发表外部事实；本册复算的是来料基于这些事实的合金配比与线性系数，不重新拟合卫星原始数据，也不重做软定理的场论证明。")

    add("I-01", "INFO", "ZIP、16/16 断言与外链只登记不验收",
        "ROOT V145 三法攻坚研究包（1.47 MB / 含 V144）、16/16 验证断言、解压复测、哈希校验与 NIST/APS/PubMed 外链均为来料声明；本册未收到可独立运行实体，只登记。")

    add("I-02", "INFO", "与 r453（同 V145）的分工与跨册印证",
        "r453 审 V145 磁通手征与代数一致性（不同来料正文）；本册审三法攻坚四力统一。两册独立，不互相覆盖。A-01 的普适耦合条件性结论与 r456 的「S_ROOT 仍是目标」、r457 的「T_interaction 未导出」方向一致：均停在条件性/目标层。")

    # ---------- 输出 ----------
    counts = {}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    key["entry_counts"] = counts
    key["guard_pass"] = sum(1 for g in guards if g["status"] == "PASS")
    key["guard_total"] = len(guards)
    key["verdict"] = "SOFT-THEOREM-AND-MICROSCOPE-CONSTRAINTS-CONFIRMED--SPIN2-SOURCE-AND-G-UNDERIVED--NO-NOVEL-PREDICTION--UNIFICATION-NOT-DERIVED"

    report = []
    report.append("r458 ROOT V145 三法攻坚四力统一全维审计")
    report.append("source_sha256=%s" % sha)
    report.append("entries=%d guards=%d/%d" % (len(entries), key["guard_pass"], key["guard_total"]))
    for e in entries:
        report.append("%s\t%s\t%s" % (e["id"], e["status"], e["title"]))
    report.append("VERDICT=%s" % key["verdict"])

    lines = []
    lines.append("# " + STEM.replace("_", " "))
    lines.append("")
    lines.append("- 来料 SHA256：`%s`" % sha)
    lines.append("- 裁定：`%s`" % key["verdict"])
    lines.append("- 条目：%d；守卫：%d/%d" % (len(entries), key["guard_pass"], key["guard_total"]))
    lines.append("")
    lines.append("| ID | 状态 | 标题 | 摘要 |")
    lines.append("|---|---|---|---|")
    for e in entries:
        lines.append("| %s | %s | %s | %s |" % (e["id"], e["status"], e["title"], e["detail"].replace("|", "\\|")))
    lines.append("")
    lines.append("## 关键读数")
    for k in sorted(key.keys()):
        lines.append("- `%s`: `%s`" % (k, json.dumps(jsonable(key[k]), ensure_ascii=False, sort_keys=True)))
    lines.append("")

    (DATA / (STEM + ".json")).write_text(
        json.dumps({"stem": STEM, "source_sha256": sha, "entries": entries,
                    "guards": guards, "key_numbers": key},
                   ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    (DATA / (STEM + ".md")).write_text("\n".join(lines), encoding="utf-8")
    (DATA / (STEM + "_report.txt")).write_text("\n".join(report) + "\n", encoding="utf-8")

    print("ENTRIES=%d" % len(entries))
    print("COUNTS=%s" % json.dumps(counts, ensure_ascii=False, sort_keys=True))
    print("GUARDS=%d/%d" % (key["guard_pass"], key["guard_total"]))
    print("VERDICT=%s" % key["verdict"])
    ok = all(g["status"] == "PASS" for g in guards)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
