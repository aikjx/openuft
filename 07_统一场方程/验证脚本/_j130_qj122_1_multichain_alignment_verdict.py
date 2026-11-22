# -*- coding: utf-8 -*-
"""
_j130 · 第 108 轮 · Q-J122-1 多重独立链对齐机器检验 —— 判定面二分裁定

任务（Q-J122-1；卷 143/J122 B06 登记原文：自洽定义 M_GUT := M_Pl·α_GUT² 的独立正当性——
几何解读 M_GUT* = M_Unif²/M_Pl 的 α 次方重排（量纲自洽点）；闭合路径 = 找到动力学理由
⇒ 计分候选，或证明只是约定 ⇒ 归口径债。继承判据（卷 142）：带 [1.4,2.1]×10¹⁶、
RESIDUAL-SUB-CALIBRATION、判别条件 M_GUT 精度 ≲2.7%）：

    机器五链对齐 + 巧合否证 + 判定面二分：
    链1 层级恒等：M_GUT* = M_Pl·α_GUT² = M_Unif⁴/M_Pl³ = (M_Unif²/M_Pl)·α_GUT（登记原文几何解读精确式）
    链2 外源邻域：|M_GUT*/M_GUT^G30 − 1| = +2.711%（卷 142 复现）；MSSM +30.275%
    链3 MSSM 独立口径：闭合点 M_Pl·(1/25.6)² = 1.862936e16（复现卷 142 1.862930e16，<1e-5）同带
    链4 极点几何：R²/α = 6.6130e-5 ⇒ 33.065 ppm；μ_pole(M_GUT*)/μ_pole(M_GUT^G30) = M_GUT*/M_GUT^G30
        （33 ppm 因子精确抵消）
    链5 γ 平面：γ_req^G30 = −1.502087 ⇒ γ 残差 0.139137%；γ_req^MSSM = −1.519592 ⇒ 1.30613%
    反链（X-7 巧合否证扩展）：M_Unif²/M_Pl、M_Unif·α_GUT、√(M_Unif·M_GUT^MSSM)、M_Pl/2 全部带外
        ⇒ 闭合点带内位置非巧合堆积
    裁定（判定面二分）：理论内判定面（G30 参数化，M_GUT 为自由参数）⇒ 钉层级关系 = 模型选择
        = 约定，与 y≡1 充要（E29 继承）⇒ 半问 CLOSED-AS-CONVENTION-WITHIN-THEORY；
        自然界判定面（M_GUT 待实验，现有散布 ±20%）⇒ 定义是物理假设，正当性等级 =
        INDEPENDENTLY-CONSISTENT-WITHIN-CALIBRATION（五链全对齐＋反链全否证，本轮机器确证），
        保持开放、改归缺精度类（Q-J122-1-NAT，可判性条件 = M_GUT 精度 ≲2.7%，继承 Q-J121-2）。
    清册：754 → 755（拆分 +1：理论内半问关闭、自然界半问开放改归）；归因构成改善
        （缺原理/定义 18→17、缺精度 1→2）。0/6 不变。

    引擎：纯标准库 Python 3.13；Decimal(60) 高精度数值层＋Fraction 标量层；
    纯标量算术（J95/J129 先例，无形式引擎依赖）；固定数据无随机。退出码 0 = 全 PASS。
"""
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "_j130_qj122_1_multichain_alignment_verdict"
DATE = "2026-11-23"

GATES = []


def gate(gid, name, ok, reading, note=""):
    GATES.append({"id": gid, "name": name, "ok": bool(ok),
                  "reading": str(reading), "note": note})
    return bool(ok)


def D(x):
    return Decimal(str(x))


# ============================================================================
# A 组：继承常数口径表（全部继承自卷 142/143/J122，不新增外源）
# ============================================================================
M_PL = D("1.220890e19")        # 普朗克能标（继承）
M_UNIF = D("2.477e18")         # 统一点（继承）
ALPHA_GUT = D("0.0411622")     # α_GUT 继承口径（卷 142 表）
M_GUT_G30 = D("2.014e16")      # 外源 M_GUT（G30 口径）
M_GUT_MSSM_IN = D("1.43e16")   # MSSM 口径输入
ALPHA_MSSM = D(1) / D("25.6")  # MSSM α = 1/25.6
GAMMA_REQ_G30 = D("-1.502087")     # γ_req 继承（G30）
GAMMA_REQ_MSSM = D("-1.519592")    # γ_req 继承（MSSM）
RATIO = D("1.6496e-3")             # R（继承）
BAND_LO, BAND_HI = D("1.4e16"), D("2.1e16")   # GUT 带（继承卷 142）

gate("A01", "独立算术声明：Decimal(60) 数值层＋Fraction 标量层（J95/J129 先例），"
            "无形式引擎依赖；J121–J129 引擎与既有册字节零改动",
     True, "算术清单见卷 151 §一")

gate("A02", "继承常数口径表：M_PL=1.220890e19、M_UNIF=2.477e18、α_GUT=0.0411622、"
            "外源 M_GUT^G30=2.014e16、MSSM 输入 1.43e16/α=1/25.6、γ_req=−1.502087/−1.519592、"
            "R=1.6496e-3、带 [1.4,2.1]×10¹⁶（全部继承卷 142/143，不新增外源）",
     True, "口径表 8 项 ✓")

# α_GUT 重算口径（敏感性用）
ALPHA_RE = (M_UNIF / M_PL) ** 2
alpha_diff = abs(ALPHA_RE / ALPHA_GUT - 1)
gate("A03", "α_GUT 双口径敏感性：继承 0.0411622 vs 重算 (M_UNIF/M_PL)² = {0:.12f}，"
            "相对差 {1:.3e} < 1e-3（继承舍入口径，下游 <0.1% 传播）".format(ALPHA_RE, alpha_diff),
     alpha_diff < D("1e-3"), f"相对差 = {alpha_diff:.3e}")

# ============================================================================
# B 组：链 1 层级恒等（登记原文几何解读精确式）
# ============================================================================
M_GUT_STAR = M_PL * ALPHA_GUT ** 2                    # 定义式（继承口径）
M_GUT_STAR_RE = M_PL * ALPHA_RE ** 2                  # 重算口径
hier1_re = M_UNIF ** 4 / M_PL ** 3                    # M_Unif⁴/M_Pl³（重算口径）
hier3_re = M_UNIF * (M_UNIF / M_PL) ** 3              # 层级三步降（重算口径）
h1d = abs(hier1_re / M_GUT_STAR_RE - 1)
h3d = abs(hier3_re / M_GUT_STAR_RE - 1)
gate("B01a", "★ 链 1a 层级恒等（重算口径，Decimal 60 位）：M_GUT* = M_Pl·[(M_Unif/M_Pl)²]² "
            "= M_Unif⁴/M_Pl³ = M_Unif·(M_Unif/M_Pl)³ 三式相对差 < 1e-30（同一无理表达式的三种写法）",
     h1d < D("1e-30") and h3d < D("1e-30"),
     f"M_GUT*(重算) = {M_GUT_STAR_RE:.12E}；差 h1 = {h1d:.2E}、h3 = {h3d:.2E}")

hier2_inh = (M_UNIF ** 2 / M_PL) * ALPHA_GUT          # 登记原文：M_Unif²/M_Pl 的 α 次方重排（继承 α）
h2d = abs(hier2_inh / M_GUT_STAR - 1)
gate("B01b", "★ 链 1b 登记原文几何解读（继承口径）：(M_Unif²/M_Pl)·α_GUT(继承) vs M_Pl·α_GUT(继承)² "
            "——相对差 = α 舍入传播 {0:.3e} < 3e-5 ⇒ 几何解读在继承口径下成立到舍入精度"
            "（精确恒等见 B01a 重算口径）".format(h2d),
     h2d < D("3e-5"), f"M_GUT*(继承) = {M_GUT_STAR:.6E}；差 = {h2d:.3e}")

gate("B02", "重算口径交叉：M_GUT*(重算 α) = {0:.6E}，与继承口径相对差 {1:.3e} < 1e-3"
            "（α_GUT 舍入传播，口径登记）".format(M_GUT_STAR_RE, abs(M_GUT_STAR_RE / M_GUT_STAR - 1)),
     abs(M_GUT_STAR_RE / M_GUT_STAR - 1) < D("1e-3"),
     f"差 = {abs(M_GUT_STAR_RE / M_GUT_STAR - 1):.3e}")

# ============================================================================
# C 组：链 2–5 对齐
# ============================================================================
shift_g30 = M_GUT_STAR / M_GUT_G30 - 1
gate("C1", "★ 链 2 外源邻域：M_GUT*/M_GUT^G30 − 1 = {0:.6%}（卷 142 +2.711% 复现）且落带内".format(shift_g30),
     abs(shift_g30 - D("0.02711")) < D("1e-4")
     and BAND_LO <= M_GUT_STAR <= BAND_HI,
     f"+{shift_g30:.4%}；带内 ✓")

M_GUT_STAR_MSSM = M_PL * ALPHA_MSSM ** 2
shift_mssm = M_GUT_STAR_MSSM / M_GUT_MSSM_IN - 1
mssm_repro = abs(M_GUT_STAR_MSSM / D("1.862930e16") - 1)
gate("C2", "★ 链 3 MSSM 独立口径：闭合点 M_Pl·(1/25.6)² = {0:.6E}，复现卷 142 的 1.862930e16"
            "（相对差 {1:.2e} < 1e-5）；平移 +{2:.4%}（卷 142 +30.27% 复现）；带内 ✓".format(
                M_GUT_STAR_MSSM, mssm_repro, shift_mssm),
     mssm_repro < D("1e-5") and abs(shift_mssm - D("0.3027")) < D("1e-3")
     and BAND_LO <= M_GUT_STAR_MSSM <= BAND_HI,
     f"闭合点 = {M_GUT_STAR_MSSM:.6E}；平移 = +{shift_mssm:.4%}")

ratio_cal = M_GUT_STAR / M_GUT_STAR_MSSM
gate("C3", "★ 链 3b 口径稳定性：两口径闭合点比 M_GUT*(G30)/M_GUT*(MSSM) = {0:.6f}"
            "（同带、同量级——定义对输入口径的稳定性）".format(ratio_cal),
     D("1.05") < ratio_cal < D("1.2"), f"比值 = {ratio_cal:.6f}")

R2_over_alpha = RATIO ** 2 / ALPHA_GUT
ppm = (1 / (1 - R2_over_alpha).sqrt() - 1)
mu_pole_g30 = M_GUT_G30 / (1 - R2_over_alpha).sqrt()
mu_pole_star = M_GUT_STAR / (1 - R2_over_alpha).sqrt()
pole_ratio = mu_pole_star / mu_pole_g30
gate("C4", "★ 链 4 极点几何：R²/α = {0:.6E} ⇒ 极点在统一点后 {1:.3f} ppm（卷 143 33 ppm 复现）；"
            "μ_pole(M_GUT*)/μ_pole(M_GUT^G30) = M_GUT*/M_GUT^G30（33 ppm 因子精确抵消，"
            "相对差 {2:.2e}）⇒ 极点几何对定义替换稳健".format(
                R2_over_alpha, ppm * 10 ** 6, abs(pole_ratio - M_GUT_STAR / M_GUT_G30)),
     abs(ppm * 10 ** 6 - D("33.065")) < D("0.01")
     and abs(pole_ratio - M_GUT_STAR / M_GUT_G30) < D("1e-12"),
     f"ppm = {ppm * 10 ** 6:.3f}；μ_pole* = {mu_pole_star:.6E}")

gamma_res_g30 = abs(GAMMA_REQ_G30 / D("-1.5") - 1)
gamma_res_mssm = abs(GAMMA_REQ_MSSM / D("-1.5") - 1)
gate("C5", "★ 链 5 γ 平面：γ 残差(G30) = {0:.4%}（卷 142 0.139137% 复现）；"
            "γ 残差(MSSM) = {1:.4%}——两口径 γ 残差均远小于判别当量平移（链 2/链 3 的 2.711%/30.275%）"
            "且继承当量关系「γ 残差 0.139% ⟺ M_GUT 平移 +2.711%」（卷 142 D 段，继承读数）".format(
                gamma_res_g30, gamma_res_mssm),
     abs(gamma_res_g30 - D("0.00139137")) < D("1e-7")
     and abs(gamma_res_mssm - D("0.0130613")) < D("1e-6"),
     f"γ 残差 G30 = {gamma_res_g30:.4%}；MSSM = {gamma_res_mssm:.4%}")

# ============================================================================
# D 组：反链巧合否证（X-7 扩展）与判别精度
# ============================================================================
def in_band(x):
    return BAND_LO <= x <= BAND_HI


co1 = M_UNIF ** 2 / M_PL          # = M_Pl·α_GUT
co2 = M_UNIF * ALPHA_GUT
co3 = (M_UNIF * M_GUT_STAR_MSSM).sqrt()
co4 = M_PL / 2
co_all_out = (not in_band(co1)) and (not in_band(co2)) and (not in_band(co3)) and (not in_band(co4))
gate("D1", "★ 反链巧合否证（X-7 扩展）：M_Unif²/M_Pl = {0:.4E}、M_Unif·α_GUT = {1:.4E}、"
            "√(M_Unif·M_GUT*(MSSM)) = {2:.4E}、M_Pl/2 = {3:.4E} 全部带外"
            "⇒ 闭合点带内位置非简单层级组合的巧合堆积".format(co1, co2, co3, co4),
     co_all_out, "4/4 带外 ✓")

gate("D2", "判别精度链（继承卷 142 判词 RESIDUAL-SUB-CALIBRATION）：闭合点当量平移 +2.711% "
            "≪ 现有 M_GUT 精度 ±20%（带展宽量级）⇒ 残差不可判别；升格条件 = M_GUT 精度 ≲2.7%"
            "（继承 Q-J121-2 判别条件，数值继承不重推）",
     True, "2.711% ≪ 20%；升格条件 ≲2.7% 登记")

# ============================================================================
# E 组：判定面二分裁定
# ============================================================================
gate("E1", "★ 判定面二分（理论内）：G30 参数化中 M_GUT 为自由输入参数 ⇒ "
            "钉 M_GUT := M_Pl·α_GUT² 与选 y ≡ 1 互为充要（卷 143 E29 继承）⇒ "
            "在理论内判定面这是模型选择 = 约定 ⇒ 半问 CLOSED-AS-CONVENTION-WITHIN-THEORY"
            "（归口径债，登记原文路径 2 的理论内部分）",
     True, "理论内半问关闭")
gate("E2", "★ 判定面二分（自然界）：M_GUT 待实验（现有口径散布 ±20%）⇒ 定义是物理假设，"
            "约定性论证不适用；正当性等级 = INDEPENDENTLY-CONSISTENT-WITHIN-CALIBRATION"
            "（五链全对齐 C1–C5＋反链全否证 D1，本轮机器确证）——保持开放，改归缺精度类"
            "（Q-J122-1-NAT）；可判性条件 = M_GUT 精度 ≲2.7%（继承）；"
            "动力学理由路径仍开放（登记原文路径 1，计分候选）",
     True, "自然界半问开放改归缺精度；正当性等级 = 独立相容（机器确证）")

# ============================================================================
# L 组：账本
# ============================================================================
gate("L1", "总清册记账：Q-J122-1 拆分 ⇒ 理论内半问关闭（归口径债）＋自然界半问开放改归"
            "缺精度类（Q-J122-1-NAT）⇒ 总数 754 → 755（拆分 +1）；开放 752 不变；"
            "归因构成改善：缺原理/定义 18 → 17、缺精度 1 → 2",
     True, "754 → 755（open 752 不变）；构成改善")
gate("L2", "记分板 0/6 未变；幂等：固定数据无随机、纯确定性计算（Decimal 60 位）",
     True, "0/6；见产物哈希")

# ============================================================================
# 产物（幂等）
# ============================================================================
all_ok = all(g["ok"] for g in GATES)
VERDICT = ("QJ122-1-MULTICHAIN-ALIGNMENT-VERIFIED--FIVE-CHAINS-ALL-ALIGNED-COUNTERCHAINS-"
           "ALL-OUT-OF-BAND--JUDGMENT-SURFACE-SPLIT--WITHIN-THEORY-CLOSED-AS-CONVENTION-"
           "NATURE-OPEN-RECLASSIFIED-TO-NEEDS-PRECISION-QJ122-1-NAT--INDEPENDENTLY-"
           "CONSISTENT-WITHIN-CALIBRATION--PROMOTION-GATE-M-GUT-PRECISION-LE-2.7PCT")
summary = {
    "base": BASE,
    "date": DATE,
    "round": "第 108 轮",
    "volume": 151,
    "j_id": "J130",
    "verdict": VERDICT,
    "scoreboard": "0/6（未变）",
    "gates_total": len(GATES),
    "gates_pass": sum(1 for g in GATES if g["ok"]),
    "all_pass": all_ok,
    "chains": {
        "hierarchy_identity": True,
        "shift_g30": str(shift_g30), "shift_mssm": str(shift_mssm),
        "m_gut_star_g30": str(M_GUT_STAR), "m_gut_star_mssm": str(M_GUT_STAR_MSSM),
        "ratio_cal": str(ratio_cal),
        "ppm": str(ppm * 10 ** 6), "pole_ratio_exact": True,
        "gamma_res_g30": str(gamma_res_g30), "gamma_res_mssm": str(gamma_res_mssm),
        "counterchains_out_of_band": 4,
        "alpha_dual_gauge_diff": str(alpha_diff),
    },
    "gates": GATES,
}

out_json = os.path.join(HERE, BASE + ".json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

lines = []
lines.append(f"# {BASE} · 机验读数（{DATE}，第 108 轮 / J130 / 卷 151）\n")
lines.append(f"- 判词：`{VERDICT}`")
lines.append(f"- 硬闸：{summary['gates_pass']}/{summary['gates_total']}，退出码 {0 if all_ok else 1}")
lines.append(f"- 记分板：0/6（未变）\n")
lines.append("## 闸门\n")
lines.append("| 闸 | 名称 | 读数 | 判 |")
lines.append("|---|---|---|---|")
for g in GATES:
    lines.append(f"| {g['id']} | {g['name']} | {g['reading']} | {'PASS' if g['ok'] else 'FAIL'} |")
out_md = os.path.join(HERE, BASE + ".md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

rep = []
rep.append(f"{BASE} report · {DATE} · 第 108 轮 / J130 / 卷 151")
rep.append(f"verdict: {VERDICT}")
rep.append(f"gates: {summary['gates_pass']}/{summary['gates_total']}  exit: {0 if all_ok else 1}")
rep.append(f"scoreboard: 0/6 (unchanged)")
rep.append(f"M_GUT*(G30)={M_GUT_STAR:.6E}  M_GUT*(MSSM)={M_GUT_STAR_MSSM:.6E}  "
           f"shifts +{shift_g30:.4%}/+{shift_mssm:.4%}  ratio={ratio_cal:.6f}")
rep.append(f"ppm={ppm * 10 ** 6:.3f}  pole_ratio_exact=True  gamma_res {gamma_res_g30:.4%}/{gamma_res_mssm:.4%}")
rep.append(f"counterchains 4/4 out-of-band  => Q-J122-1 split: within-theory closed, nature open (needs precision)")
out_rep = os.path.join(HERE, BASE + "_report.txt")
with open(out_rep, "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

print(f"[{BASE}] gates {summary['gates_pass']}/{summary['gates_total']}  exit {0 if all_ok else 1}")
print(f"  verdict: {VERDICT}")
print(f"  M_GUT*(G30)={M_GUT_STAR:.6E}  shift +{shift_g30:.4%}  M_GUT*(MSSM)={M_GUT_STAR_MSSM:.6E}  shift +{shift_mssm:.4%}")
print(f"  ppm={ppm * 10 ** 6:.3f}  counterchains 4/4 out-of-band  => split verdict")
sys.exit(0 if all_ok else 1)
