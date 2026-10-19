# -*- coding: utf-8 -*-
"""
================================================================================
openuft#49 攻破第六轮 · 外部候选谱在共线判据下的机检（同一把尺子量别人）
================================================================================
承接：第四轮已建立并校验的判据（一圈三耦合汇聚 <=> (A_i,b_i) 共线），
      第五轮已证明 TUFT 内部路径（空间运行方式 + 换谱/扩群）双封口。

本轮命题：既然内部路径封闭，那么**改用外部输入**（TUFT 之外的候选粒子谱），
      在同一共线判据下究竟什么谱能统一？——用第四轮那把已过 MSSM 控制组
      校验的尺子，系统机检一批外部候选谱，给出"统一需要什么"的可算账本。

方法：
  1) 复用第四轮的共线判据与 α_s 预言（逐字复制，保证口径不漂移）；
  2) 用 R12 已核验的 Δb 积木（逐场累加、与文献精确相等）搭候选谱；
  3) 三道门：共线（统一）、质子衰变（τ_p>2.4e34 年）、LHC 质量下限。

本轮的一个结构性结论（可算验证）：
  完全 GUT 多重态（三个 b_i 等量平移，如完整额外代 Δb=(4/3,4/3,4/3)）
  **不改变任何 b_i-b_j** ⇒ 不改变 det ⇒ 共线残差完全不变 ⇒ 对汇聚毫无帮助。
  能改变判决的必须是"不等量"的 Δb（如规范子 (0,4/3,2)、Higgsino 等）。

纯标准库；自检不过即退出码非 0。
================================================================================
"""
from __future__ import print_function
import json
import math
import os
import sys

MZ = 91.1876
TWO_PI = 2.0 * math.pi

# ---- 数据（与第四轮逐字一致：PDG，GUT 归一化，约定 a: Q=T3+Y）--------------
AINV = {1: 59.0209, 2: 29.5838, 3: 8.47458}
AS_MZ, AS_SIG = 0.1180, 0.0009
B_SM = {1: 41.0 / 10.0, 2: -19.0 / 6.0, 3: -7.0}
IDS = (1, 2, 3)

# 质子衰变：τ_p ≈ (M_GUT/2e16)^4 × 1e35 年（R12 所用口径；经 R12 两点复核）
TAU_P_REF_MGUT = 2.0e16
TAU_P_REF_YEARS = 1.0e35
TAU_P_LIMIT = 2.4e34  # Super-K (p→e+ π0)


# ============ 以下三个函数逐字复用第四轮（口径一致性优先，不重造）============
def ainv(i, u, b):
    return AINV[i] - (b[i] / TWO_PI) * u


def pairwise_u(i, j, b):
    den = b[i] - b[j]
    if abs(den) < 1e-15:
        return float("inf")
    return TWO_PI * (AINV[i] - AINV[j]) / den


def collinearity_det(b):
    """det = (A2-A1)(b3-b1) - (A3-A1)(b2-b1)；det=0 <=> 一圈三耦合同标度汇聚。"""
    a1, a2, a3 = AINV[1], AINV[2], AINV[3]
    b1, b2, b3 = b[1], b[2], b[3]
    return (a2 - a1) * (b3 - b1) - (a3 - a1) * (b2 - b1)


def affine_residual_normalized(b):
    det = collinearity_det(b)
    dA = max(AINV.values()) - min(AINV.values())
    db = max(b.values()) - min(b.values())
    return abs(det) / (dA * db) if dA * db > 0 else float("inf")


def predict_alpha_s(b):
    """用 α1,α2 定参（u12 处），预言 α_s(M_Z)。"""
    u12 = pairwise_u(1, 2, b)
    agut_inv = ainv(1, u12, b)
    a3_req_inv = agut_inv + (b[3] / TWO_PI) * u12
    a3_pred = 1.0 / a3_req_inv
    sigma = abs(a3_pred - AS_MZ) / AS_SIG
    return {"u12": u12, "M_GUT": MZ * math.exp(u12),
            "alpha_GUT_inv": agut_inv, "alpha_s_pred": a3_pred, "sigma": sigma}
# =============================================================================


def tau_proton(m_gut):
    """τ_p ≈ (M_GUT/2e16)^4 × 1e35 年（R12 口径）。"""
    return ((m_gut / TAU_P_REF_MGUT) ** 4) * TAU_P_REF_YEARS


def required_ratio():
    """共线条件等价的单一比值：R* = (b2-b1)/(b3-b1) = (A2-A1)/(A3-A1)。"""
    return (AINV[2] - AINV[1]) / (AINV[3] - AINV[1])


def ratio_of(b):
    den = b[3] - b[1]
    if abs(den) < 1e-15:
        return float("inf")
    return (b[2] - b[1]) / den


# ---- Δb 积木：全部取自 R12 已核验的逐场累加表（与文献精确相等）-------------
BLOCKS = {
    "GEN":         (4.0 / 3.0, 4.0 / 3.0, 4.0 / 3.0),   # 完整额外手征代(Q,u,d,L,e,ν)
    "GAUGINO":     (0.0, 4.0 / 3.0, 2.0),               # (8,1,0)+(1,3,0)+(1,1,0)
    "SFERMION":    (2.0, 2.0, 2.0),                     # 三代 sfermion
    "HIGGSINO":    (2.0 / 5.0, 2.0 / 3.0, 0.0),         # 2 个 (1,2,±1/2) Weyl
    "HIGGS_EXTRA": (1.0 / 10.0, 1.0 / 6.0, 0.0),        # 额外标量双重态
    "WINO":        (0.0, 4.0 / 3.0, 0.0),               # (1,3,0) Weyl
    "GLUINO":      (0.0, 0.0, 2.0),                     # (8,1,0) Weyl
    "O8":          (0.0, 0.0, 1.0),                     # (8,1,0) 标量
    "S3":          (0.0, 2.0 / 3.0, 0.0),               # (1,3,0) 标量
    "LQ":          (1.0 / 15.0, 0.0, 1.0 / 6.0),        # (3,1,-1/3) 标量
    "QLIKE":       (1.0 / 15.0, 1.0, 2.0 / 3.0),        # (3,2,1/6) Weyl
    "LLIKE":       (1.0 / 5.0, 1.0 / 3.0, 0.0),         # (1,2,-1/2) Weyl
}

# ---- 候选谱目录：SM 基线 + 积木组合 ---------------------------------------
SPECTRA = [
    ("SM（基线）",                 []),
    ("MSSM（控制组）",             ["GAUGINO", "SFERMION", "HIGGSINO", "HIGGS_EXTRA"]),
    ("Split SUSY（规范子+Higgsino）", ["GAUGINO", "HIGGSINO"]),
    ("2HDM（额外希格斯双重态）",    ["HIGGS_EXTRA"]),
    ("SM+1 完整代",               ["GEN"]),
    ("SM+2 完整代",               ["GEN", "GEN"]),
    ("SM+3 完整代",               ["GEN", "GEN", "GEN"]),
    ("SM+规范子",                 ["GAUGINO"]),
    ("SM+Higgsino",              ["HIGGSINO"]),
    ("SM+wino",                  ["WINO"]),
    ("SM+gluino",                ["GLUINO"]),
    ("SM+规范子+sfermion",        ["GAUGINO", "SFERMION"]),
    ("SM+O8（色八重态标量）",      ["O8"]),
    ("SM+S3（弱三重态标量）",      ["S3"]),
    ("SM+LQ（轻子夸克标量）",      ["LQ"]),
    ("SM+Q-like（矢量like夸克）",  ["QLIKE"]),
    ("SM+L-like",                ["LLIKE"]),
    ("SM+完整代+规范子",           ["GEN", "GAUGINO"]),
]


def build_b(blocks):
    b = {1: B_SM[1], 2: B_SM[2], 3: B_SM[3]}
    for name in blocks:
        d = BLOCKS[name]
        for i in IDS:
            b[i] = b[i] + d[i - 1]
    return b


def evaluate(name, blocks):
    b = build_b(blocks)
    res = affine_residual_normalized(b)
    pr = predict_alpha_s(b)
    m_gut = pr["M_GUT"]
    tp = tau_proton(m_gut)
    rstar = required_ratio()
    r = ratio_of(b)
    # 门
    g_col = res < 0.02          # 与第四轮 MSSM 同阈值
    g_proton = tp > TAU_P_LIMIT
    return {
        "name": name,
        "blocks": list(blocks),
        "b": {"b1": b[1], "b2": b[2], "b3": b[3]},
        "collinearity_residual": res,
        "ratio_R": r,
        "ratio_required": rstar,
        "ratio_deviation": abs(r - rstar),
        "alpha_s_pred": pr["alpha_s_pred"],
        "sigma": pr["sigma"],
        "M_GUT_GeV": m_gut,
        "tau_p_years": tp,
        "gate_collinear": bool(g_col),
        "gate_proton": bool(g_proton),
        "verdict": ("UNIFY" if g_col else "NO-UNIFY"),
    }


def main():
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    # ---------- 自检 0：口径对齐第四轮 / R12 ----------
    sm = evaluate("SM", [])
    mssm = evaluate("MSSM", ["GAUGINO", "SFERMION", "HIGGSINO", "HIGGS_EXTRA"])

    check("SM 共线残差 ≈ 0.0723（对齐第四轮）",
          abs(sm["collinearity_residual"] - 0.0723) < 5e-3,
          "got %.4f" % sm["collinearity_residual"])
    check("SM α_s 偏离 ≈ 52.06σ（对齐第四轮）",
          abs(sm["sigma"] - 52.06) < 0.5, "got %.2f" % sm["sigma"])
    check("MSSM 共线残差 < 0.02（对齐第四轮）",
          mssm["collinearity_residual"] < 0.02,
          "got %.5f" % mssm["collinearity_residual"])
    check("MSSM σ ≈ 1.27（对齐第四轮）",
          abs(mssm["sigma"] - 1.27) < 0.1, "got %.2f" % mssm["sigma"])
    check("MSSM M_GUT ≈ 2.014e16（对齐第四轮）",
          abs(mssm["M_GUT_GeV"] - 2.014e16) / 2.014e16 < 0.02,
          "got %.4e" % mssm["M_GUT_GeV"])

    # ---------- 自检 1：τ_p 公式复核 R12 的两个数据点 ----------
    tp_a = tau_proton(5.146e13)   # R12: 4.38e24
    tp_b = tau_proton(1.540e16)   # R12: 3.52e34
    check("τ_p 公式复现 R12 点(M_GUT=5.146e13 → 4.38e24)",
          abs(tp_a - 4.38e24) / 4.38e24 < 0.05, "got %.3e" % tp_a)
    check("τ_p 公式复现 R12 点(M_GUT=1.540e16 → 3.52e34)",
          abs(tp_b - 3.52e34) / 3.52e34 < 0.05, "got %.3e" % tp_b)

    # ---------- 自检 2：MSSM 通过质子衰变门 ----------
    check("MSSM 通过质子衰变门（τ_p > 2.4e34）",
          mssm["tau_p_years"] > TAU_P_LIMIT,
          "τ_p=%.3e" % mssm["tau_p_years"])

    # ---------- 自检 3：结构性定理（等量平移不改变 det）----------
    gen1 = evaluate("SM+1GEN", ["GEN"])
    gen3 = evaluate("SM+3GEN", ["GEN", "GEN", "GEN"])
    same = (abs(gen1["collinearity_residual"] - sm["collinearity_residual"]) < 1e-12
            and abs(gen3["collinearity_residual"] - sm["collinearity_residual"]) < 1e-12)
    check("结构性定理：完整代（Δb 等量）不改变共线残差",
          same,
          "SM=%.6f, +1GEN=%.6f, +3GEN=%.6f"
          % (sm["collinearity_residual"], gen1["collinearity_residual"],
             gen3["collinearity_residual"]))

    # ---------- 自检 4：比值判据与 det 判据等价 ----------
    mssm_close = mssm["ratio_deviation"] < 0.01
    sm_far = sm["ratio_deviation"] > 0.05
    check("比值判据与 det 判据一致（MSSM 近 / SM 远）",
          mssm_close and sm_far,
          "SM ΔR=%.4f, MSSM ΔR=%.5f" % (sm["ratio_deviation"], mssm["ratio_deviation"]))

    # ---------- 全部候选谱 ----------
    table = [evaluate(n, bl) for (n, bl) in SPECTRA]

    rstar = required_ratio()
    summary = {
        "verdict": "PASS_external_audit" if all(c["ok"] for c in checks) else "FAIL_SELFCHECK",
        "selfcheck_passed": sum(1 for c in checks if c["ok"]),
        "selfcheck_total": len(checks),
        "required_ratio_R_star": rstar,
        "SM_residual": sm["collinearity_residual"],
        "MSSM_residual": mssm["collinearity_residual"],
        "spectra_tested": len(table),
        "spectra_unify": sum(1 for t in table if t["gate_collinear"]),
        "spectra_unify_and_proton_safe": sum(
            1 for t in table if t["gate_collinear"] and t["gate_proton"]),
        "structural_theorem": "完整 GUT 多重态（Δb 三等分量平移）不改变 b_i-b_j ⇒ 不改变 det ⇒ 对汇聚零贡献；能改变判决的必须是不等量 Δb",
    }
    data = {"summary": summary, "checks": checks, "table": table}

    # ---------- 写 JSON ----------
    here = os.path.dirname(os.path.abspath(__file__))
    jpath = os.path.join(here, "openuft_49_攻破第六轮_外部候选谱共线判据机检_data.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # ---------- 写文本报告 ----------
    L = []
    L.append("=" * 78)
    L.append("openuft#49 攻破第六轮 · 外部候选谱在共线判据下的机检")
    L.append("=" * 78)
    L.append("")
    L.append("[自检] %d/%d PASS" % (summary["selfcheck_passed"], summary["selfcheck_total"]))
    for c in checks:
        L.append("  [%s] %s  %s" % ("PASS" if c["ok"] else "FAIL", c["check"], c["detail"]))
    L.append("")
    L.append("[比值判据] 共线等价于单一比值 R=(b2-b1)/(b3-b1) = R* = (A2-A1)/(A3-A1)")
    L.append("           R* = %.6f" % rstar)
    L.append("")
    L.append("[候选谱机检] %d 个；统一 %d 个；统一且质子安全 %d 个"
             % (summary["spectra_tested"], summary["spectra_unify"],
                summary["spectra_unify_and_proton_safe"]))
    L.append("")
    hdr = ("%-30s %10s %10s %9s %8s %11s %11s %s"
           % ("谱", "残差", "R", "ΔR", "α_s预言", "M_GUT/GeV", "τ_p/年", "判决"))
    L.append(hdr)
    L.append("-" * 110)
    for t in table:
        col = "统一" if t["gate_collinear"] else "不统一"
        prot = "" if t["gate_collinear"] else ""
        if t["gate_collinear"]:
            prot = " | 质子安全" if t["gate_proton"] else " | 质子衰变排除"
        L.append("%-30s %10.5f %10.5f %9.5f %8.5f %11.4e %11.3e %s%s"
                 % (t["name"][:30], t["collinearity_residual"], t["ratio_R"],
                    t["ratio_deviation"], t["alpha_s_pred"], t["M_GUT_GeV"],
                    t["tau_p_years"], col, prot))
    L.append("")
    L.append("[结构性定理] %s" % summary["structural_theorem"])
    L.append("")
    L.append("[判决] %s" % summary["verdict"])
    text = "\n".join(L) + "\n"
    rpath = os.path.join(here, "openuft_49_攻破第六轮_外部候选谱共线判据机检_report.txt")
    with open(rpath, "w", encoding="utf-8") as f:
        f.write(text)

    try:
        sys.stdout.write(text)
    except Exception:
        sys.stdout.write(text.encode("ascii", "replace").decode("ascii"))

    if summary["verdict"] != "PASS_external_audit":
        sys.exit(1)


if __name__ == "__main__":
    main()
