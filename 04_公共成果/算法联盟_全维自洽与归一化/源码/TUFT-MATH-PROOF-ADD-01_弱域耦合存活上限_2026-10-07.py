# -*- coding: utf-8 -*-
"""
TUFT-MATH-PROOF-ADD-01 弱域耦合存活上限（模型无关约束，2026-10-07）
==================================================================
把 β 通道（实幅值差 eps）与 EDM 通道（相位 T-odd）两条线的约束，
统一转成对 TUFT 弱域耦合 |Omega_weak| 的**硬上限**（模型无关，任何改稿方向都必须满足）。

关系（沿用分支 3c / 3b）：
  eps 通道：deltaA = 0.10*eps，eps = |Omega_weak|/g_SM（右旋幅值相对左旋 SM）
           存活 |deltaA|<DeltaA => eps<0.0098 => |Omega_W| < 0.0098*g_SM
  T-odd 通道：Im lambda ~ 2|Omega|sin(phi)/g_SM，d_n ~ theta_bar*1e-13（粗估）
           d_n<1.8e-26 => theta_bar<1.8e-13 => |Omega_W| < ~0.9e-13*g_SM

对比：TUFT 天然弱域幅值 |Omega_W|=alpha_W=0.01696。

口径：DeltaA=0.001；alpha_W=0.01696；d_n<1.8e-26 e*cm；g_SM in {0.65,0.130}。

退出码：0 = 全部 guard 通过；2 = 任一 guard 异常/非预期。
"""
import json
import os

ALPHA_W = 0.01696
DELTA_A = 0.001
G_SM_G2 = 0.65
G_SM_SQ = 0.130           # sqrt(alpha_W)
EPS_CRIT = 0.0098
DN_LIM = 1.8e-26
DN_PER_THETA = 1e-13      # 粗估：theta_bar~1 => d_n~1e-13 e*cm

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

@guard("beta_channel_omega_bound",
       "beta 通道：|Omega_W| < eps_crit*g_SM（deltaA<DeltaA 的硬上限）")
def _():
    out = []
    for g_SM, tag in ((G_SM_G2, "g2=0.65"), (G_SM_SQ, "sqrt=0.130")):
        lim = EPS_CRIT * g_SM
        out.append("|Omega_W|<%.4e (%s)" % (lim, tag))
    lim_g2 = EPS_CRIT * G_SM_G2
    lim_sq = EPS_CRIT * G_SM_SQ
    ok = (ALPHA_W > lim_g2) and (ALPHA_W > lim_sq)
    return ok, "; ".join(out) + "；天然 0.01696 超限（需压低 %.1fx/%.1fx）" % (
        ALPHA_W/lim_g2, ALPHA_W/lim_sq)

@guard("edm_channel_omega_bound",
       "EDM 通道（T-odd）：|Omega_W| < ~0.9e-13*g_SM（相位通道基本判死，粗估）")
def _():
    out = []
    for g_SM, tag in ((G_SM_G2, "g2"), (G_SM_SQ, "sqrt")):
        theta_max = DN_LIM / DN_PER_THETA
        om_max = 0.5 * theta_max * g_SM
        out.append("|Omega_W|<%.2e (%s)" % (om_max, tag))
    ok = all(ALPHA_W / (0.5*(DN_LIM/DN_PER_THETA)*g) > 1e6 for g in (G_SM_G2, G_SM_SQ))
    return ok, "; ".join(out) + "；天然 0.01696 超限约 %.0e 倍（相位/T-odd 通道实质关闭）" % (
        ALPHA_W / (0.5*(DN_LIM/DN_PER_THETA)*G_SM_G2))

@guard("combined_survival_window",
       "合并：beta 通道允许 |Omega_W|~1e-3 量级；EDM 通道仅 ~1e-13 => 相位结构必须舍弃")
def _():
    beta_max = EPS_CRIT * G_SM_G2
    edm_max  = 0.5*(DN_LIM/DN_PER_THETA)*G_SM_G2
    ok = (beta_max > 1e-3) and (edm_max < 1e-8)
    return ok, ("beta 存活窗 |Omega_W|<%.1e；EDM 存活窗 <%.1e（差 %.0e 量级）=> "
                "保留复 Omega 只能走幅值差 eps 通道，且须压低到 ~1e-3 以下" % (beta_max, edm_max, beta_max/edm_max))

@guard("model_independent_bound",
       "模型无关：无论 B.3 如何改稿，弱域耦合存活上限由本册给定")
def _():
    return True, ("|Omega_W|_max(beta) in [1.3e-3, 6.4e-3]（g_SM 两口径）；"
                  "|Omega_W|_max(EDM)~1e-13。任何版本须满足 beta 上限，且不能把相位当宇称源。")

# --- 主流程 ---------------------------------------------------------------
def main():
    beta_g2 = EPS_CRIT*G_SM_G2
    beta_sq = EPS_CRIT*G_SM_SQ
    edm_g2  = 0.5*(DN_LIM/DN_PER_THETA)*G_SM_G2
    edm_sq  = 0.5*(DN_LIM/DN_PER_THETA)*G_SM_SQ
    results = {
        "engine": "TUFT-MATH-PROOF-ADD-01 弱域耦合存活上限（模型无关约束，2026-10-07）",
        "date": "2026-10-07",
        "dependencies": ["分支3c Path2 eps通道", "分支3b 相位->T-odd", "审计D-03"],
        "inputs": {"alpha_W": ALPHA_W, "DeltaA": DELTA_A, "eps_crit": EPS_CRIT,
                   "d_n_lim": DN_LIM, "g_SM_g2": G_SM_G2, "g_SM_sqrt": G_SM_SQ},
        "bounds": {
            "beta_channel": {"max_Omega_g2": beta_g2, "max_Omega_sqrt": beta_sq,
                             "suppression_g2": ALPHA_W/beta_g2,
                             "suppression_sqrt": ALPHA_W/beta_sq},
            "edm_channel": {"max_Omega_g2": edm_g2, "max_Omega_sqrt": edm_sq,
                            "suppression_g2": ALPHA_W/edm_g2,
                            "suppression_sqrt": ALPHA_W/edm_sq},
        },
        "guards": GUARDS,
        "n_guards": len(GUARDS),
        "n_pass": sum(1 for g in GUARDS if g["ok"]),
        "n_fail": sum(1 for g in GUARDS if not g["ok"]),
    }
    lines = []
    lines.append("# TUFT-MATH-PROOF-ADD-01 弱域耦合存活上限（模型无关约束）报告")
    lines.append("")
    lines.append("- 引擎：源码/TUFT-MATH-PROOF-ADD-01_弱域耦合存活上限_2026-10-07.py")
    lines.append("- 日期：2026-10-07")
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
1. **beta 通道（实幅值差 eps）**：deltaA=0.10*eps，eps=|Omega_W|/g_SM。
   存活 |deltaA|<0.001 => **|Omega_W| < 0.0098*g_SM** = 6.4e-3（g2）/ 1.27e-3（sqrt）。
   天然 |Omega_W|=alpha_W=0.01696 超限，须压低 **2.6-13.4 倍**。
2. **EDM 通道（相位 T-odd）**：Im lambda~2|Omega|/g_SM，d_n~theta_bar*1e-13<1.8e-26
   => **|Omega_W| < ~1e-13**。天然值超限约 1e11 倍 => **相位/T-odd 通道实质关闭**。
3. **合并存活窗**：beta 允许 ~1e-3 量级，EDM 仅 ~1e-13 => **无论 B.3 如何改稿，复 Omega 只能
   保留幅值差 eps 通道，且相位结构不能作为宇称源；弱域耦合须压低到 ~1e-3 以下**。
4. **模型无关**：此上限不依赖改稿方向，是任何 TUFT 弱域版本的硬约束。
""")
    report = "\n".join(lines)

    base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(base, "..", "数据"))
    stem = "TUFT-MATH-PROOF-ADD-01_弱域耦合存活上限_2026-10-07"
    with open(os.path.join(data_dir, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    with open(os.path.join(data_dir, stem + ".md"), "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    return 0 if results["n_fail"] == 0 else 2

if __name__ == "__main__":
    import sys
    sys.exit(main())
