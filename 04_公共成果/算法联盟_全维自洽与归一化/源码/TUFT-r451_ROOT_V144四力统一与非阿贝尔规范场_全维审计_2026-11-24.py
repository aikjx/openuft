#!/usr/bin/env python3
"""r451 / ROOT V144 四力统一与非阿贝尔规范场全维审计。

纯标准库。复核代数维数、Yang-Mills 非阿贝尔结构、KK 质量下界、
Lichnerowicz 零模障碍；ZIP 与外链只登记不验收。
"""
from __future__ import print_function

import hashlib
import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 60

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "04_公共成果" / "算法联盟_全维自洽与归一化"
DATA = BASE / "数据"
STEM = "TUFT-r451_ROOT_V144四力统一与非阿贝尔规范场_全维审计_2026-11-24"
SOURCE = DATA / "TUFT-ROOT_V144_四力统一与非阿贝尔规范场_来料全文_2026-11-24.md"

D = Decimal
entries = []
guards = []
key_numbers = {}


def fmt(x, digits="15"):
    x = D(x)
    if x == 0:
        return "0"
    return format(x, "." + digits + "E")


def rel_diff(a, b):
    a, b = D(a), D(b)
    denom = max(abs(a), abs(b), D("1e-80"))
    return abs(a - b) / denom


def dsqrt(x):
    x = D(x)
    if x < 0:
        raise ValueError("negative Decimal sqrt")
    return (x.ln() / D(2)).exp()


def add(code, status, title, detail):
    entries.append({"id": code, "status": status, "title": title, "detail": detail})


def guard(code, ok, detail):
    guards.append({"id": code, "status": "PASS" if ok else "FAIL", "detail": detail})


def matmul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def comm(A, B):
    AB, BA = matmul(A, B), matmul(B, A)
    return [[AB[i][j] - BA[i][j] for j in range(len(A))] for i in range(len(A))]


def mat_eq(A, B, tol=0):
    return all(abs(A[i][j] - B[i][j]) <= tol for i in range(len(A)) for j in range(len(A)))


def main():
    if not SOURCE.exists():
        print("MISSING SOURCE:", SOURCE)
        return 2
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    sha = hashlib.sha256(raw).hexdigest()
    key_numbers["source_sha256"] = sha
    key_numbers["source_bytes"] = len(raw)

    anchors = [
        "T\\cdot\\mathbf N",
        "\\mathfrak{su}(3)\\oplus \\mathfrak{su}(2)\\oplus \\mathfrak{u}(1)",
        "\\mathcal M=M_4\\times K",
        "\\mathcal F_{\\mu\\nu}",
        "\\mathcal F_{xy}=abT_3",
        "m_4\\geq\\sqrt{\\frac{\\alpha\\hbar}{4G}}",
        "9.29605 × 10⁻¹⁰ kg",
        "\\mathcal R_K= \\frac{6}{L_3^2}+\\frac{3}{2L_2^2}>0",
        "D_K^2=\\nabla_K^\\*\\nabla_K+\\frac{\\mathcal R_K}{4}",
        "37 项 Python 自动化测试通过",
    ]
    hit = [a in text for a in anchors]
    guard("G0-01", all(hit), "来料锚点 10/10 可见（实际 %d）" % sum(hit))
    guard("G0-02", len(sha) == 64 and len(raw) > 1000, "正本非空且 SHA256 格式有效")
    image_refs = text.count("[image]")
    key_numbers["image_refs"] = image_refs
    guard("G0-03", image_refs == 3, "外部 image 标记计数=%d" % image_refs)

    dim_su3, dim_su2, dim_u1 = 8, 3, 1
    dim_g = dim_su3 + dim_su2 + dim_u1
    dim_total = 4 + dim_g
    dim_orthonormal_rotations = 3
    key_numbers.update({
        "dim_su3": dim_su3, "dim_su2": dim_su2, "dim_u1": dim_u1,
        "dim_g_SM": dim_g, "dim_M4xG": dim_total,
        "dim_orthonormal_frame_rotations": dim_orthonormal_rotations,
    })
    guard("G1-01", dim_g == 12, "dim su(3)+su(2)+u(1)=8+3+1=12")
    guard("G1-02", dim_total == 16, "dim(M4×G)=4+12=16")
    guard("G1-03", dim_orthonormal_rotations < dim_g,
          "Frenet 三正交标架旋转自由度 3 < 规范生成元 12")

    add("A-01", "PASS", "标准模型内部规范代数维数复算通过",
        "8+3+1=12；直接群流形路线 K=SU(3)×SU(2)×U(1) 的内部维数 12，整体 M4×K 为 16 维。")
    add("A-02", "FAIL", "三方向垂直关系不足以直接承载标准模型内部对称性",
        "T,N,B 两两垂直只给 SO(3) 型三旋转自由度；从 3 维正交标架到 12 维规范代数缺少映射与动力学，不能把 T·N=N·B=B·T=0 当成四力统一推导。")
    add("A-03", "BOUNDARY", "八维 SU(3) 破缺路线只降低内部维数，不自动给出正确粒子谱",
        "来料区分了 12 维直接群流形与 8 维 SU(3) 破缺路线；维数减少不等于表示、手征、质量与耦合已被推导。")

    T1 = [[0, 0, 0], [0, 0, -1], [0, 1, 0]]
    T2 = [[0, 0, 1], [0, 0, 0], [-1, 0, 0]]
    T3 = [[0, -1, 0], [1, 0, 0], [0, 0, 0]]
    comm12 = comm(T1, T2)
    a, b = D(2), D(3)
    Fxy = [[a * b * x for x in row] for row in T3]
    from_comm = comm([[a * x for x in row] for row in T1], [[b * x for x in row] for row in T2])
    key_numbers["comm_T1_T2_equals_T3"] = mat_eq(comm12, T3)
    key_numbers["Fxy_equals_ab_T3"] = mat_eq(Fxy, from_comm)
    guard("G2-01", mat_eq(comm12, T3), "[T1,T2]=T3 的 3×3 反厄米矩阵实现成立")
    guard("G2-02", mat_eq(Fxy, from_comm), "Fxy=[aT1,bT2]=abT3 逐矩阵元成立")

    add("B-01", "PASS", "非阿贝尔场强可由不对易生成元产生",
        "取反厄米 3×3 实现，[T1,T2]=T3；A_x=aT1、A_y=bT2 时 Fxy=[A_x,A_y]=abT3，a=2,b=3 的 9 个矩阵元逐项一致。")
    add("B-02", "INFO", "该场强结构是已有 Yang–Mills 理论，不是 ROOT 新推导",
        "F=dA+A∧A 与 Fxy=abT3 可机器复现；ROOT 仍未解释 T_A、K 与耦合为何从基础螺旋运动中出现。")

    G = D("6.67430e-11")
    HBAR = D("1.054571817e-34")
    C = D("299792458")
    ALPHA = D("7.2973525643e-3")
    M_E = D("9.1093837139e-31")
    m_min_sq = ALPHA * HBAR * C / (D(4) * G)
    m_min = dsqrt(m_min_sq)
    mass_gap = m_min / M_E
    user_m_min = D("9.29605e-10")
    user_gap = D("1.02049e21")
    key_numbers.update({
        "m_min_SI": fmt(m_min),
        "m_e_SI": str(M_E),
        "mass_gap": fmt(mass_gap),
        "m_min_rel_diff_vs_user": fmt(rel_diff(m_min, user_m_min)),
        "mass_gap_rel_diff_vs_user": fmt(rel_diff(mass_gap, user_gap)),
    })
    guard("G3-01", rel_diff(m_min, user_m_min) < D("1e-5"),
          "m_min=%s 与 9.29605e−10 kg 相对差 %s" % (fmt(m_min), fmt(rel_diff(m_min, user_m_min))))
    guard("G3-02", rel_diff(mass_gap, user_gap) < D("1e-5"),
          "质量比=%s 与 1.02049e21 相对差 %s" % (fmt(mass_gap), fmt(rel_diff(mass_gap, user_gap))))

    add("C-01", "PASS", "最简 KK 带电模态质量下界复算通过",
        "由 m4²=m5²+p5²、m5²≥0 与 α=4Gp5²/ℏ 得 m4≥sqrt(αℏ/(4G))；SI 恢复光速因子后为 sqrt(αℏc/(4G))=%s kg。" % fmt(m_min))
    add("C-02", "PASS", "电子质量差距读数一致",
        "取 CODATA m_e=%s kg，m_min/m_e=%s，与来料 1.02049e21 一致。" % (str(M_E), fmt(mass_gap)))
    add("C-03", "FAIL", "最简五维纯几何带电粒子模型仍被电子反例排除",
        "该下界比电子质量高约 %s 倍；仅调闭环半径无法同时给电子质量与电荷，必须引入额外且有物理依据的物质机制。" % fmt(mass_gap))

    RK_coeff_L3 = D(6)
    RK_coeff_L2 = D(3) / D(2)
    RK_equal_coeff = RK_coeff_L3 + RK_coeff_L2
    lambda_sq_coeff = RK_equal_coeff / D(4)
    key_numbers.update({
        "R_K_coeff_L3": str(RK_coeff_L3),
        "R_K_coeff_L2": str(RK_coeff_L2),
        "R_K_equal_L0_coeff": str(RK_equal_coeff),
        "Dirac_lambda_sq_lower_coeff": str(lambda_sq_coeff),
    })
    guard("G4-01", RK_equal_coeff == D("7.5"), "L2=L3=L0 时 R_K=7.5/L0²")
    guard("G4-02", lambda_sq_coeff == D("1.875"), "Lichnerowicz 下界 λ_D²≥1.875/L0²")
    guard("G4-03", RK_coeff_L3 > 0 and RK_coeff_L2 > 0, "正定双不变度规下 R_K>0")

    add("D-01", "PASS", "内部标量曲率与 Dirac 下界算术正确",
        "R_K=6/L3²+3/(2L2²)>0；L2=L3=L0 时 R_K=7.5/L0²，D²=∇*∇+R/4 给 λ_D²≥1.875/L0²。")
    add("D-02", "PASS", "紧致无边界未扭曲条件下无非零谐和自旋零模",
        "Lichnerowicz 恒等式取内积得 ||Dψ||²=||∇ψ||²+∫R_K|ψ|²/4；R_K>0 时 Dψ=0 只容 ψ=0。")
    add("D-03", "BOUNDARY", "通量/规范扭曲可改变零模结论，须另证",
        "来料已指出未扭曲 Dirac 算子的限制；引入 flux、twist 或奇异内部几何后，Lichnerowicz 项与谱均可能改变，不能把这些理论一并排除。")

    add("E-01", "FAIL", "强/弱相互作用来源仍未从基础螺旋推出",
        "本轮给出 Yang–Mills 场强与内部流形候选，但没有从 T,N,B、光速闭环或曲率挠率独立导出 SU(3)、SU(2)、表示、手征与耦合。")
    add("E-02", "BOUNDARY", "ZIP 与测试声明只登记不验收",
        "来料声称 ROOT_V144_Geometric_Gauge_Audit_Complete.zip 约 1.97 MB、21 文件、37 项 Python 测试、5 项 SymPy 校验；本轮未收到 ZIP，不能据声明判定通过。")
    add("E-03", "INFO", "V145 三条件仍全部开放",
        "光速螺旋→规范动力学、内部几何→手征质量电荷谱、微观运动→GR与独立可测预测，均未在本轮闭合；四力统一仍未被证明。")

    status_counts = {}
    for e in entries:
        status_counts[e["status"]] = status_counts.get(e["status"], 0) + 1
    key_numbers["entries"] = len(entries)
    key_numbers["status_counts"] = status_counts
    key_numbers["guards"] = len(guards)
    key_numbers["guards_pass"] = sum(1 for g in guards if g["status"] == "PASS")

    lines = []
    lines.append("# TUFT r451 / ROOT V144 四力统一与非阿贝尔规范场全维审计")
    lines.append("")
    lines.append("## 一、总览")
    lines.append("")
    lines.append("来料正本 SHA256：`%s`" % sha)
    lines.append("")
    lines.append("条目 %d：%s" % (len(entries), " / ".join("%s=%d" % (k, v) for k, v in sorted(status_counts.items()))))
    lines.append("")
    lines.append("守卫 %d/%d PASS。" % (key_numbers["guards_pass"], len(guards)))
    lines.append("")
    lines.append("## 二、条目")
    lines.append("")
    for e in entries:
        lines.append("- **%s [%s]** %s：%s" % (e["id"], e["status"], e["title"], e["detail"]))
    lines.append("")
    lines.append("## 三、守卫")
    lines.append("")
    for g in guards:
        lines.append("- %s %s：%s" % (g["id"], g["status"], g["detail"]))
    lines.append("")
    lines.append("## 四、关键机器读数")
    lines.append("")
    lines.append("- dim(su3⊕su2⊕u1)=%d, dim(M4×G)=%d, dim(Frenet rotations)=%d" %
                 (dim_g, dim_total, dim_orthonormal_rotations))
    lines.append("- [T1,T2]=T3=%s, Fxy=abT3=%s" %
                 (key_numbers["comm_T1_T2_equals_T3"], key_numbers["Fxy_equals_ab_T3"]))
    lines.append("- m_min=%s kg, mass_gap=%s" % (fmt(m_min), fmt(mass_gap)))
    lines.append("- R_K(L2=L3=L0)=%s/L0², λ_D²≥%s/L0²" % (str(RK_equal_coeff), str(lambda_sq_coeff)))
    lines.append("")
    lines.append("## 五、红线")
    lines.append("")
    lines.append("Yang–Mills 结构与 KK 质量下界可复算不等于四力统一；ZIP 声明未验收。红线不变。")
    lines.append("")

    md_path = DATA / (STEM + ".md")
    json_path = DATA / (STEM + ".json")
    report_path = DATA / (STEM + "_report.txt")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    payload = {
        "round": "r451",
        "topic": "ROOT V144 四力统一与非阿贝尔规范场",
        "date": "2026-11-24",
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": sha,
        "entries": entries,
        "guards": guards,
        "key_numbers": key_numbers,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(
        "OK entries=%d guards=%d/%d\nsource_sha256=%s\nm_min=%s mass_gap=%s\nstatus=%s\n" %
        (len(entries), key_numbers["guards_pass"], len(guards), sha,
         fmt(m_min), fmt(mass_gap), json.dumps(status_counts, ensure_ascii=False, sort_keys=True)),
        encoding="utf-8",
    )

    print("OK entries=%d guards=%d/%d" % (len(entries), key_numbers["guards_pass"], len(guards)))
    print("source_sha256=%s" % sha)
    print("m_min=%s mass_gap=%s" % (fmt(m_min), fmt(mass_gap)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("ERROR", type(exc).__name__, str(exc))
        sys.exit(1)
