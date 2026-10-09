# -*- coding: utf-8 -*-
"""
TUFT-MATH-PROOF-ADD-01 实幅值差宇称通道（Path 2）数值重建【修正版】（分支 3c）
================================================================================
前置：分支 3b 裁定「相位->CP/T-odd（EDM 判死）；幅值差->宇称」。
本册落地 Path 2 修正版：在**物理 SM 基线 lambda_SM=-1.2756**（含 QCD 轴矢重整）上，
叠加 TUFT 右旋污染（V+A，幅值比 eps=g_R/g_L），产出标准实宇称不对称 deltaA。

模型（修正，物理基线）：
  lambda_SM = -1.2756（物理中子 g_A/g_V，含 QCD 重整）
  加右旋污染 eps（幅值比，实）：
    g_V 系数  ->  1 + eps
    g_A 系数  ->  lambda_SM - eps
    lambda_new = (lambda_SM - eps)/(1 + eps)
    delta_lambda = lambda_new - lambda_SM = -eps(1+lambda_SM)/(1+eps)
    deltaA = A(lambda_new) - A(lambda_SM)

关键改进：delta_lambda 只依赖 eps（右旋幅值比），**不依赖 g_SM 归一化**，
消除了分支 3 的归一化歧义。若 TUFT 右旋幅值=|Omega|（继承 B.3），则 eps=|Omega|/g_L。

口径：lambda_SM=-1.2756；DeltaA=0.001；|Omega|=alpha_W=0.01696；
      eps 天然口径：eps=|Omega|/g_SM = 0.026（g_SM=g_2=0.65）或 0.130（g_SM=sqrt_alphaW）。

退出码：0 = 全部 guard 通过；2 = 任一 guard 异常/非预期。
"""
import math
import json
import os

ALPHA_W   = 0.01696
LAMBDA_SM = -1.2756
DELTA_A   = 0.001
G_SM_G2   = 0.65
G_SM_SQ   = math.sqrt(ALPHA_W)

def A_param(lam):
    return -2.0 * lam * (lam + 1.0) / (1.0 + 3.0 * lam ** 2)

def lambda_new(eps):
    return (LAMBDA_SM - eps) / (1.0 + eps)

def delta_lambda(eps):
    return lambda_new(eps) - LAMBDA_SM

def deltaA(eps):
    return A_param(lambda_new(eps)) - A_param(LAMBDA_SM)

GUARDS = []
def guard(name, detail=""):
    def deco(fn):
        try:
            ok, note = fn()
        except Exception as e:
            ok, note = False, "EXC: %r" % e
        GUARDS.append({"name": name, "ok": ok, "note": note, "detail": detail})
        return fn
    return deco

# --- 修正模型 --------------------------------------------------------------
@guard("delta_lambda_formula",
       "delta_lambda = -eps(1+lambda_SM)/(1+eps) ~ +0.2756·eps（精确 vs 近似）")
def _():
    eps = 0.05
    exact = delta_lambda(eps)
    approx = -eps * (1.0 + LAMBDA_SM) / (1.0 + eps)
    ok = abs(exact - approx) < 1e-12
    return ok, "delta_lambda(0.05)=%.5f（≈%.4f·eps）" % (exact, exact / eps)

@guard("deltaA_scaling",
       "deltaA = 0.10·eps（物理基线下，与 g_SM 归一化无关）")
def _():
    coeff = deltaA(0.01) / 0.01
    ok = (0.05 < coeff < 0.15)
    return ok, "deltaA(0.01)=%.5f ⇒ 系数 %.3f·eps" % (deltaA(0.01), coeff)

@guard("survival_epsilon_threshold",
       "存活阈值：|deltaA|<DeltaA=0.001 需 eps < ~0.010（约 1%）")
def _():
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if abs(deltaA(mid)) < DELTA_A:
            lo = mid
        else:
            hi = mid
    ok = (0.005 < lo < 0.02)
    return ok, "eps_crit = %.4f（约 1%% 右旋污染为存活上限）" % lo

@guard("natural_epsilon_from_omega",
       "若 TUFT 右旋幅值=|Omega|（继承 B.3），eps=|Omega|/g_SM=0.026(g2)/0.130(sqrt)")
def _():
    e_g2 = ALPHA_W / G_SM_G2
    e_sq = ALPHA_W / G_SM_SQ
    ok = (e_g2 > 0.01) and (e_sq > 0.05)
    return ok, "eps_nat(g2)=%.3f, eps_nat(sqrt)=%.3f（均超存活上限 ~0.01）" % (e_g2, e_sq)

@guard("deltaA_natural_vs_precision",
       "deltaA 天然值：g2 口径 0.0027（3×ΔA），sqrt 口径 0.013（13×ΔA）——超精度")
def _():
    d_g2 = abs(deltaA(ALPHA_W / G_SM_G2))
    d_sq = abs(deltaA(ALPHA_W / G_SM_SQ))
    ok = (d_g2 > DELTA_A) and (d_sq > 3.0 * DELTA_A)
    return ok, "deltaA_nat(g2)=%.4f（%.0f×ΔA），deltaA_nat(sqrt)=%.4f（%.0f×ΔA）" % (
        d_g2, d_g2 / DELTA_A, d_sq, d_sq / DELTA_A)

@guard("live_testable_boundary",
       "边界可测：eps=0.01 时 deltaA~0.001，恰在当前 β 精度 ~ΔA 处 ⇒ 现/近未来可探")
def _():
    d = abs(deltaA(0.01))
    ok = (0.5 * DELTA_A < d < 2.0 * DELTA_A)
    return ok, "eps=0.01 ⇒ |deltaA|=%.4f ≈ ΔA=0.001（可探边界）" % d

@guard("honest_epsilon_status",
       "诚实：eps 为右旋幅值比（新参数）；若由 |Omega| 提供则 eps~0.03-0.13 超限，需调谐")
def _():
    return True, ("deltaA=0.10·eps 为干净线性预言（物理基线下无归一化歧义）；"
                  "但 eps 由模型未定；天然 eps=|Omega|/g_SM~0.03-0.13 超存活上限，"
                  "须把右旋污染压到 ~1% 方存活")

# --- 主流程 ---------------------------------------------------------------
def main():
    results = {
        "engine": "TUFT-MATH-PROOF-ADD-01 实幅值差宇称通道（Path 2）数值重建【修正版】（分支 3c）",
        "date": "2026-10-05",
        "dependencies": ["分支3b 相位->T-odd裁定", "分支3 beta衰变数值", "审计 D-03"],
        "inputs": {"alpha_W": ALPHA_W, "lambda_SM": LAMBDA_SM, "DeltaA": DELTA_A,
                   "g_SM_g2": G_SM_G2, "g_SM_sqrt": G_SM_SQ},
        "guards": GUARDS,
        "n_guards": len(GUARDS),
        "n_pass": sum(1 for g in GUARDS if g["ok"]),
        "n_fail": sum(1 for g in GUARDS if not g["ok"]),
    }
    lines = []
    lines.append("# TUFT-MATH-PROOF-ADD-01 实幅值差宇称通道（Path 2）数值重建【修正版】报告（分支 3c）")
    lines.append("")
    lines.append("- 引擎：源码/TUFT-MATH-PROOF-ADD-01_Path2实幅值差宇称_重建_2026-10-05.py")
    lines.append("- 日期：2026-10-05")
    lines.append("- 读数：%d guard —— PASS %d / FAIL %d（退出码 %d）"
                 % (len(GUARDS), results["n_pass"], results["n_fail"],
                    0 if results["n_fail"] == 0 else 2))
    lines.append("")
    for g in GUARDS:
        lines.append("| %s | %s | %s |" % ("PASS" if g["ok"] else "FAIL",
                                           g["name"], g["note"]))
    lines.append("")
    lines.append("### 结论")
    lines.append("""
1. **修正模型**：在物理基线 lambda_SM=-1.2756 上叠加右旋污染 eps（幅值比），
   delta_lambda = -eps(1+lambda_SM)/(1+eps) ~ +0.2756·eps，**只依赖 eps，不依赖 g_SM 归一化**
   （消除分支 3 的归一化歧义）。
2. **deltaA 显式**：**deltaA = 0.10·eps**（物理基线下干净线性）。
3. **存活阈值**：|deltaA|<DeltaA=0.001 需 **eps < ~0.01（约 1% 右旋污染）**。
4. **TUFT 天然值**：若右旋幅值=|Omega|（继承 B.3），eps=|Omega|/g_SM=0.026(g2)/0.130(sqrt)
   ⇒ deltaA=0.0027(g2)/0.013(sqrt)，**超 ΔA 约 3-13 倍** ⇒ 天然假设下仍被排除，须把
   右旋污染压到 ~1%。
5. **边界可测**：eps=0.01 时 deltaA~0.001，恰在当前 β 精度 ~ΔA ⇒ 现有/近未来测量可探
   （对比相位通道 T-odd 已被 EDM 排除 ~3e11 倍，Path 2 是唯一活通道）。
6. **诚实**：eps 由模型未定；deltaA=0.10·eps 是干净可证伪预言，但需模型解释为何
   eps~1% 而非天然 3-13%。
""")
    report = "\n".join(lines)

    base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(base, "..", "数据"))
    stem = "TUFT-MATH-PROOF-ADD-01_Path2实幅值差宇称_重建_2026-10-05"
    with open(os.path.join(data_dir, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    with open(os.path.join(data_dir, stem + ".md"), "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    return 0 if results["n_fail"] == 0 else 2

if __name__ == "__main__":
    import sys
    sys.exit(main())
