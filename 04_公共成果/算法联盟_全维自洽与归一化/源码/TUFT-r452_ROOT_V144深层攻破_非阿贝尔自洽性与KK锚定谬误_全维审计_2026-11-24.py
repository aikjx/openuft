#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r452 / ROOT V144 深层攻破：非阿贝尔自洽性与 KK 锚定谬误。

与 r451（表面确认册）分工：r451 确认来料算术逐项成立；本册不改其任何字节，
只做它未做的深层攻击。纯标准库；矩阵用 Fraction 精确，常数用 Decimal 60 位。
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
STEM = "TUFT-r452_ROOT_V144深层攻破_非阿贝尔自洽性与KK锚定谬误_全维审计_2026-11-24"
SOURCE = DATA / "TUFT-ROOT_V144_四力统一与非阿贝尔规范场_来料全文_2026-11-24.md"

D = Decimal
entries = []
guards = []
key = {}


def fmt(x, digits="18"):
    x = D(x)
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


def add(code, status, title, detail):
    entries.append({"id": code, "status": status, "title": title, "detail": detail})


def guard(code, ok, detail):
    guards.append({"id": code, "status": "PASS" if ok else "FAIL", "detail": detail})


def mm(A, B):
    n = len(A)
    return [[sum((A[i][k] * B[k][j] for k in range(n)), Fraction(0)) for j in range(n)] for i in range(n)]


def comm(A, B):
    AB, BA = mm(A, B), mm(B, A)
    return [[AB[i][j] - BA[i][j] for j in range(len(A))] for i in range(len(A))]


def tr(A):
    return sum((A[i][i] for i in range(len(A))), Fraction(0))


def mat_zero(A):
    return all(x == 0 for row in A for x in row)


def mat_eq(A, B):
    return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A)))


def smul(c, A):
    return [[c * x for x in row] for row in A]


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
        "T\\cdot\\mathbf N",
        "\\mathfrak g= \\mathfrak{su}(3)\\oplus \\mathfrak{su}(2)\\oplus \\mathfrak{u}(1)",
        "\\mathcal F_{xy}=abT_3",
        "\\alpha=\\frac{4Gp_5^2}{\\hbar}",
        "\\mathcal R_K= \\frac{6}{L_3^2}+\\frac{3}{2L_2^2}>0",
        "1.02049 × 10²¹",
    ]
    hits = [a in text for a in anchors]
    guard("G0-01", all(hits), "来料锚点 %d/%d 可见" % (sum(hits), len(hits)))
    guard("G0-02", len(sha) == 64 and len(raw) > 1000, "正本非空且 SHA256 格式有效")

    # ---- 一、整理：确认来料算术（不重复 r451，仅作为攻击的锚）----
    add("A-01", "PASS", "维数与场强算术层面无误（整理锚点）",
        "8+3+1=12、dim(M4×K)=16；反厄米 so(3) 基下 [T1,T2]=T3、A_x=aT1,A_y=bT2⇒F_xy=abT3 逐元成立。本册承认这些算术，攻击其物理身份。")
    add("A-02", "PASS", "KK 质量下界与曲率算术层面无误（整理锚点）",
        "m_min=sqrt(alpha*hbar*c/(4G))≈9.29605e-10 kg、m_min/m_e≈1.02049e21、R_K=6/L3²+3/(2L2²)⇒7.5/L0²、lambda_D²≥1.875/L0²，逐项复算与来料一致。")

    # ---- 二、攻破 1：非零场强不是自洽动力学 ----
    Z, O = Fraction(0), Fraction(1)
    T1 = [[Z, Z, Z], [Z, Z, -O], [Z, O, Z]]
    T2 = [[Z, Z, O], [Z, Z, Z], [-O, Z, Z]]
    T3 = [[Z, -O, Z], [O, Z, Z], [Z, Z, Z]]
    guard("G1-01", mat_eq(comm(T1, T2), T3), "[T1,T2]=T3 精确矩阵等式")
    a, b = Fraction(2), Fraction(3)
    Fxy = smul(a * b, T3)
    guard("G1-02", mat_eq(Fxy, comm(smul(a, T1), smul(b, T2))), "F_xy=ab T3 精确矩阵等式")
    # YM: D_mu F^{mu nu} = J^nu ; F^{xy}=F_xy, F^{yx}=-F_xy
    T13 = comm(T1, T3)
    T23 = comm(T2, T3)
    Jx = smul(-a * b * b, T23)   # D_y F^{y x} = [bT2, -abT3] = -a b^2 [T2,T3] = -a b^2 T1
    Jy = smul(a * a * b, T13)    # D_x F^{x y} = [aT1, abT3] = a^2 b [T1,T3] = -a^2 b T2
    key["Jx_nonzero"] = not mat_zero(Jx)
    key["Jy_nonzero"] = not mat_zero(Jy)
    key["T1T3_is_minus_T2"] = mat_eq(T13, smul(-1, T2))
    key["T2T3_is_T1"] = mat_eq(T23, T1)
    guard("G1-03", key["T1T3_is_minus_T2"] and key["T2T3_is_T1"],
          "so(3) 结构常数自洽：[T1,T3]=-T2,[T2,T3]=T1")
    guard("G1-04", key["Jx_nonzero"] and key["Jy_nonzero"],
          "常值 ansatz 的协变散度非零 ⇒ 需外加色流，非真空解")
    key["tr_Fxy_sq"] = str(tr(mm(Fxy, Fxy)))
    guard("G1-05", tr(mm(Fxy, Fxy)) == Fraction(-2) * a * b * a * b,
          "规范不变 Casimir tr(F_xy²)=-2a²b²")
    add("B-01", "FAIL", "非零场强不等于自洽动力学：常值 ansatz 违反无源 YM 方程",
        "对 A_x=aT1,A_y=bT2,F_xy=abT3，协变散度 D_mu F^{mu x}=-ab²T1、D_mu F^{mu y}=-a²bT2 均非零；"
        "该组态不是真空解，必须外加色流 J。来料用‘出现了非零场强’代替‘出现了自洽规范动力学’，"
        "而外加的色流正是它想从几何推出的物质，构成循环。")
    add("B-02", "FAIL", "F_xy=abT3 对强/弱无判别力，且是规范依赖的表象",
        "同一交换子结构在 su(3) 的任意 su(2) 子代数中逐字成立；具体矩阵方向随规范变换改变，"
        "唯一不变量 tr(F_xy²)=-2a²b² 只含 a,b，不区分 SU(3)/SU(2)。来料以它为‘强、弱来源’的证据，"
        "实际对‘为何有两个耦合不同的规范群’零信息。")

    # ---- 三、攻破 2：KK 质量下界是普朗克锚定的重述 ----
    HBAR = D("1.054571817e-34")
    C = D("299792458")
    G = D("6.67430e-11")
    ALPHA = D("7.2973525643e-3")
    M_E = D("9.1093837139e-31")
    m_pl = dsqrt(HBAR * C / G)
    m_min = dsqrt(ALPHA * HBAR * C / (D(4) * G))
    gap = m_min / M_E
    pred_from_pl = dsqrt(ALPHA) * m_pl / D(2)
    key.update({
        "m_planck_kg": fmt(m_pl),
        "m_min_kg": fmt(m_min),
        "gap": fmt(gap),
        "m_min_over_m_pl": fmt(m_min / m_pl),
        "sqrt_alpha_over_2": fmt(dsqrt(ALPHA) / D(2)),
        "identity_rel_diff": fmt(rel(m_min, pred_from_pl)),
    })
    guard("G2-01", rel(m_min, D("9.29605e-10")) < D("1e-5"),
          "m_min=%s kg 与来料一致" % fmt(m_min))
    guard("G2-02", rel(gap, D("1.02049e21")) < D("1e-5"),
          "质量比=%s 与来料一致" % fmt(gap))
    guard("G2-03", rel(m_min, pred_from_pl) < D("1e-12"),
          "恒等式 m_min=(sqrt(alpha)/2)*m_Pl 机器成立（残差 %s）" % fmt(rel(m_min, pred_from_pl)))
    add("B-03", "FAIL", "质量下界是普朗克质量乘 sqrt(alpha)/2，不是关于电子的新信息",
        "机器恒等式 m_min=(√alpha/2)·m_Pl，残差 %s。该下界只由 alpha 与 m_Pl 决定，"
        "对任何‘引力强度的 KK 带电态’都成立；它把层级问题 m_Pl/m_e≈2.39e22 换个说法重述一遍，"
        "属于库内 M02 普朗克锚定谬误同族。来料称其为‘第二项进展’，实质零新增判别力。" % fmt(rel(m_min, pred_from_pl)))

    # ---- 四、攻破 3：电荷格与 S^1 最简纤维互斥 ----
    # R = hbar/p5 ; p5 = m_min*c ; l_P = sqrt(hbar G / c^3)
    p5 = m_min * C
    R_circle = HBAR / p5
    l_pl = dsqrt(HBAR * G / (C ** 3))
    R_over_lp = R_circle / l_pl
    analytic_2_over_sqrt_alpha = D(2) / dsqrt(ALPHA)
    key.update({
        "R_circle_m": fmt(R_circle),
        "l_planck_m": fmt(l_pl),
        "R_over_l_P": fmt(R_over_lp),
        "2_over_sqrt_alpha": fmt(analytic_2_over_sqrt_alpha),
        "R_identity_rel_diff": fmt(rel(R_over_lp, analytic_2_over_sqrt_alpha)),
    })
    guard("G3-01", rel(R_over_lp, analytic_2_over_sqrt_alpha) < D("1e-10"),
          "R/l_P=2/sqrt(alpha) 机器成立（残差 %s）" % fmt(rel(R_over_lp, analytic_2_over_sqrt_alpha)))
    # 电荷格分岔（自抓更正：n 改变的是半径 R，不是电子质量下界 m_min）
    # p5 = n*hbar/R；质量下界 m_min=(sqrt(alpha)/2)m_Pl 对应电子动量，与 n 无关。
    # 支甲 q_unit=e：电子 n=1，R=R1；夸克 ±1/3,±2/3 需非整数 n ⇒ S^1 不能容纳。
    # 支乙 q_unit=e/3：电子 n=3，R=3*R1；质量下界不变，夸克可为整数 n。
    n_electron_branch_b = 3
    R_branch_b = D(n_electron_branch_b) * R_circle
    R_branch_b_over_lp = R_branch_b / l_pl
    key.update({
        "branch_A_electron_n": 1,
        "branch_A_R_over_lP": fmt(R_over_lp),
        "branch_A_quark_charges_integer_n": False,
        "branch_B_electron_n": n_electron_branch_b,
        "branch_B_R_over_lP": fmt(R_branch_b_over_lp),
        "branch_B_mass_bound_same_as_A": True,
    })
    guard("G3-02", rel(R_branch_b_over_lp, analytic_2_over_sqrt_alpha * 3) < D("1e-10"),
          "支乙 n=3 ⇒ R/l_P=%s，与 3×2/sqrt(alpha) 一致" % fmt(R_branch_b_over_lp))
    add("B-04", "FAIL", "最简 S¹ 纤维只能给整数电荷格，与 SM 的 1/3 电荷互斥",
        "p_5=n*hbar/R 的电荷格是 n∈Z 的整格。取基本电荷单位 e：电子 n=1，但夸克 ±1/3,±2/3 需非整数 n，"
        "S¹ 无法容纳；取单位 e/3：电子须 n=3，紧致半径变为 %s l_P（支甲为 %s l_P），"
        "质量下界不变。两支必居其一且都需来料未声明的额外假设（夸克分数电荷来源或半径重标定），"
        "来料引用的单一 1.02049e21 隐含选了支甲，与其容纳 SM 电荷谱的目标冲突。" %
        (fmt(R_branch_b_over_lp), fmt(R_over_lp)))
    add("B-05", "FAIL", "KK 半径被 alpha 钉在 O(10) 个普朗克长度，无参数层级",
        "取电子 n=1 时由 p_5=hbar/R 与 m_min=(√alpha/2)m_Pl 联立得 R=(2/√alpha)·l_P≈%s l_P，"
        "与 G,hbar,c 无关；取 n=3 则 R≈%s l_P。半径不是可自由‘调整的量’，而是被 alpha 与整数 n 钉死；"
        "且 R 仅为 O(10) 倍 l_P，经典 KK 约化缺少大层级支撑，来料‘不能仅调整闭环半径’低估了约束。" %
        (fmt(R_over_lp), fmt(R_branch_b_over_lp)))

    # ---- 五、攻破 4：§二 的 flux 直接推翻 §四 的未扭曲零模定理 ----
    # 未扭曲 Lichnerowicz: D^2=∇*∇+R/4, R>0 ⇒ ker D = 0
    # 扭曲后: D_A^2=∇_A*∇_A+R/4+(1/2)γ^{mu nu}F_{mu nu}; F_xy=abT3≠0
    R_coeff = D(6) + D(3) / D(2)
    lam_coeff = R_coeff / D(4)
    flux_nonzero = not mat_zero(Fxy)
    key.update({
        "R_K_equal_coeff": str(R_coeff),
        "lambda_sq_coeff": str(lam_coeff),
        "Fxy_nonzero": flux_nonzero,
        "untwisted_theorem_applicable": (not flux_nonzero),
    })
    guard("G4-01", R_coeff == D("7.5") and lam_coeff == D("1.875"),
          "R_K=7.5/L0²、lambda_D²≥1.875/L0² 算术复算")
    guard("G4-02", flux_nonzero and not key["untwisted_theorem_applicable"],
          "§二 已有非零 flux ⇒ §四 未扭曲定理前提不成立")
    add("B-06", "FAIL", "§四‘严格障碍’是稻草人：它排除的恰是 §二 已抛弃的未扭曲构型",
        "未扭曲 Dirac 在 R_K>0 时确无零模，但 §二 已引入 F_xy=abT3≠0 的规范 flux；"
        "扭曲 Lichnerowicz 多出 (1/2)gamma^{mu nu}F_{mu nu} 项，其负本征值可抵消 R/4 并容许手征零模"
        "（这是磁化膜/通量紧化产生手征费的常规机制）。来料一面用 flux 造场强，一面用无 flux 的定理宣布障碍，"
        "两个小节前提互斥；且它自己已承认 flux 会改结论，却仍把该障碍列为‘第三项进展’。")

    # ---- 六、攻破 5：Frenet 标架的范畴错位 ----
    key["frenet_base_dim"] = 1
    key["sm_base_dim"] = 4
    key["frenet_frame_dim"] = 3
    key["sm_group_dim"] = 12
    guard("G5-01", key["frenet_base_dim"] < key["sm_base_dim"] and key["frenet_frame_dim"] < key["sm_group_dim"],
          "Frenet 标架定义在 1 维曲线，SM 内部对称性定义在 4 维流形")
    add("B-07", "FAIL", "Frenet 标架是曲线切空间标架，不是 4 维内部规范对称",
        "T,N,B 是沿一条世界线的 Frenet 标架，SO(3) 是其切空间转动；内部规范对称要求 M4 每点上"
        "作用在内部纤维上的结构群。来料未给从 1 维曲线标架到 4 维主纤维丛的构造，"
        "‘3 个旋转自由度不足’的论断虽真，但把两类不同范畴的量放在同一维数账里比较，属范畴错位。")

    # ---- 七、登记层 ----
    add("C-01", "BOUNDARY", "ZIP/测试/SymPy 声明不可验收",
        "来料声称 21 文件、37 项 Python 测试、5 项 SymPy 校验、解压重跑通过；本轮未收到实体 ZIP，只登记不判定。")
    add("C-02", "INFO", "V145 三条件仍全开放，本册不改变对外读数",
        "光速螺旋→规范动力学、内部几何→手征质量电荷谱、微观运动→GR可测预测均未闭合。")

    counts = {}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    key.update({
        "entries": len(entries),
        "status_counts": counts,
        "guards": len(guards),
        "guards_pass": sum(1 for g in guards if g["status"] == "PASS"),
    })

    lines = ["# TUFT r452 / ROOT V144 深层攻破：非阿贝尔自洽性与 KK 锚定谬误", ""]
    lines += ["## 一、总览", "", "来料正本 SHA256：`%s`" % sha, ""]
    lines += ["条目 %d：%s" % (len(entries), " / ".join("%s=%d" % (k, v) for k, v in sorted(counts.items()))), ""]
    lines += ["守卫 %d/%d PASS。" % (key["guards_pass"], len(guards)), "", "## 二、条目", ""]
    for e in entries:
        lines.append("- **%s [%s]** %s：%s" % (e["id"], e["status"], e["title"], e["detail"]))
    lines += ["", "## 三、守卫", ""]
    for g in guards:
        lines.append("- %s %s：%s" % (g["id"], g["status"], g["detail"]))
    lines += ["", "## 四、关键机器读数", ""]
    for k in ("m_planck_kg", "m_min_kg", "gap", "m_min_over_m_pl", "sqrt_alpha_over_2",
              "identity_rel_diff", "R_circle_m", "l_planck_m", "R_over_l_P",
              "2_over_sqrt_alpha", "R_identity_rel_diff", "branch_A_R_over_lP",
              "branch_B_R_over_lP", "tr_Fxy_sq"):
        lines.append("- %s = %s" % (k, key[k]))
    lines += ["", "## 五、红线", "",
              "算术无误 ≠ 物理成立。本册只做深层攻击，不修改 r451 任何字节；对外读数不变。", ""]

    (DATA / (STEM + ".md")).write_text("\n".join(lines), encoding="utf-8")
    payload = {
        "round": "r452",
        "topic": "ROOT V144 深层攻破：非阿贝尔自洽性与 KK 锚定谬误",
        "date": "2026-11-24",
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": sha,
        "relation": "deep attack on top of r451; no bytes of r451 modified",
        "entries": entries,
        "guards": guards,
        "key_numbers": key,
    }
    (DATA / (STEM + ".json")).write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    (DATA / (STEM + "_report.txt")).write_text(
        "OK entries=%d guards=%d/%d\nsource_sha256=%s\nm_min=%s gap=%s\nm_min=(sqrt(alpha)/2)*m_Pl rel=%s\nstatus=%s\n" %
        (len(entries), key["guards_pass"], len(guards), sha, fmt(m_min), fmt(gap),
         fmt(rel(m_min, pred_from_pl)), json.dumps(counts, ensure_ascii=False, sort_keys=True)),
        encoding="utf-8",
    )
    print("OK entries=%d guards=%d/%d" % (len(entries), key["guards_pass"], len(guards)))
    print("m_min=%s gap=%s" % (fmt(m_min), fmt(gap)))
    print("m_min=(sqrt(alpha)/2)*m_Pl rel=%s" % fmt(rel(m_min, pred_from_pl)))
    print("R/l_P=%s 2/sqrt(alpha)=%s" % (fmt(R_over_lp), fmt(analytic_2_over_sqrt_alpha)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("ERROR", type(exc).__name__, str(exc))
        sys.exit(1)
