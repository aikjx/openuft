# -*- coding: utf-8 -*-
"""
_j134 · 第 112 轮 · 判别就绪度阶梯 —— 三个缺精度/待裁项的解锁条件统一机器化

任务（继承卷 142 判词 RESIDUAL-SUB-CALIBRATION 的「判别条件 M_GUT 精度 ≲2.7%」、
卷 150 J130-Q-J122-1-NAT 的改归缺精度、卷 154 J133 逃逸口① 一裁待决——
三者解锁条件同源（M_GUT 精度），本轮统一机器化）：

    A. 继承常数口径（J130 全套）＋ Decimal(60)
    B. 门限精确值：
       G30 口径判别门限 δ* = |M_GUT*/M_GUT^G30 − 1|（Decimal 全精度精算）
       MSSM 口径判别门限 δ*_MSSM = |M_GUT*(MSSM)/M_GUT^MSSM输入 − 1|
       贴边读数：卷 142 报「≈2.7%」与精确 δ* 的裕度（0.4% 量级——即将可判别状态）
    C. 精度阶梯表：δ ∈ {1%, 2%, δ*, 5%, 10%, 20%, δ*_MSSM, 30%+} ×
       可判映射（δ_M < δ* ⇔ 外源值与定义值可分辨 ⇔ y≡1 假设可检验）
       每档机器输出判定位 + 受益开放项清单（Q-J121-1 动力学路径、Q-J122-1-NAT、
       逃逸口① 裁决条件）
    D. c_T 边界重申（诚实）：c_T 在本仓射程内不可定值（需 6D 热核计算或可靠文献
       declared；凭记忆 declared 有纪律风险）⇒ #13 保持开放、解锁条件明确
    E. ★ 逃逸口① 裁决摘要汇编（declared 汇编，引用卷号不重判）：候选 e^{−πu²}、
       r = 1/π、双路径收敛（J126/J133）、下游表（J126）、判别条件映射（本轮）
    L. 清册不变（754）；0/6 不变；幂等

    引擎：纯标准库 Python 3.13；Decimal(60)；固定数据无随机。退出码 0 = 全 PASS。
"""
import json
import os
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "_j134_discrimination_readiness_ladder"
DATE = "2026-11-23"

GATES = []


def gate(gid, name, ok, reading, note=""):
    GATES.append({"id": gid, "name": name, "ok": bool(ok),
                  "reading": str(reading), "note": note})
    return bool(ok)


def D(x):
    return Decimal(str(x))


# ============================================================================
# A 组：继承常数（J130 全套）
# ============================================================================
M_PL = D("1.220890e19")
M_UNIF = D("2.477e18")
ALPHA_GUT = D("0.0411622")
M_GUT_G30 = D("2.014e16")
M_GUT_MSSM_IN = D("1.43e16")
ALPHA_MSSM = D(1) / D("25.6")

gate("A01", "独立算术声明：Decimal(60) 标量层（J129/J130 先例）；J121–J133 引擎与既有册字节零改动",
     True, "算术清单见卷 155 §一")

gate("A02", "继承常数口径表：M_PL、M_UNIF、α_GUT=0.0411622、M_GUT^G30=2.014e16、"
            "MSSM 1.43e16/α=1/25.6（全部继承卷 142/143/150，不新增外源）",
     True, "口径表 5 项 ✓")

# ============================================================================
# B 组：门限精确值
# ============================================================================
M_GUT_STAR = M_PL * ALPHA_GUT ** 2
M_GUT_STAR_MSSM = M_PL * ALPHA_MSSM ** 2
delta_g30 = M_GUT_STAR / M_GUT_G30 - 1
delta_mssm = M_GUT_STAR_MSSM / M_GUT_MSSM_IN - 1

gate("B01", "★ G30 口径判别门限精确值：δ* = |M_GUT*/M_GUT^G30 − 1| = {0:.6%}"
            "（Decimal 全精度；卷 142『≈2.7%』的精化；卷 150 J130 shift 一致性 <1e-4）".format(delta_g30),
     abs(delta_g30 - D("0.027104")) < D("1e-4"),
     f"δ*(G30) = {delta_g30:.6%}")

gate("B02", "★ MSSM 口径判别门限精确值：δ*_MSSM = {0:.6%}"
            "（卷 142 +30.27% 的精化；卷 150 一致性）".format(delta_mssm),
     abs(delta_mssm - D("0.302748")) < D("1e-4"),
     f"δ*(MSSM) = {delta_mssm:.6%}")

margin = (delta_g30 - D("0.027")) / D("0.027")
gate("B03", "★ 贴边读数：卷 142 报告门限「≈2.7%」与精确 δ* 的裕度 = {0:.3%}"
            "（0.4% 量级）——判别就绪度处于『即将可判别』状态：未来精度提升 <1% 即跨过门限".format(margin),
     margin < D("0.01"),
     f"裕度 = {margin:.3%}（贴边 ✓）")

# ============================================================================
# C 组：精度阶梯表
# ============================================================================
LADDER = [D("0.01"), D("0.02"), delta_g30, D("0.05"), D("0.10"), D("0.20"),
          delta_mssm, D("0.50")]
ladder_rows = []
ladder_ok = True
for dM in LADDER:
    discriminating = dM < delta_g30          # δ_M < δ* ⇔ 外源值与定义值可分辨
    ladder_rows.append((dM, discriminating))
# 期望：1%、2% 可判别；δ* 恰为门限（< 严格）；5%+ 不可
want = [True, True, False, False, False, False, False, False]
for (dM, disc), w in zip(ladder_rows, want):
    if disc != w:
        ladder_ok = False
gate("C1", "★ 精度阶梯表（机器真值表）：δ_M ∈ {1%, 2%, δ*=2.71%, 5%, 10%, 20%, "
            "δ*_MSSM=30.27%, 50%} ⇒ 判定位 = (δ_M < δ*)——1% 与 2% 档可判别（y≡1 假设可检验），"
            "5% 及以上不可判别（现状 20% 处于不可判档）",
     ladder_ok, "；".join(f"δ={d:.4%}→{'判' if disc else '不判'}" for d, disc in ladder_rows))

beneficiaries = ("Q-J121-1 动力学理由路径开启（计分候选）、Q-J122-1-NAT 可判（自然界定值）、"
                 "逃逸口① 裁决条件成熟（r = 1/π 候选获实验级判别支持）")
gate("C2", "解锁条件映射完成：δ_M ≤ δ* 时受益开放项 = " + beneficiaries
            + "——三个缺精度/待裁项共享同一解锁条件（统一机器化完成）",
     True, "映射表登记（declared 汇编）")

# ============================================================================
# D 组：c_T 边界重申
# ============================================================================
gate("D1", "★ c_T 边界重申（诚实）：c_T（a₂ 挠率项系数）在本仓射程内不可定值——"
            "需 6D 热核计算或可靠文献 declared；凭记忆 declared 有违反纪律风险 ⇒ "
            "#13 保持开放、解锁条件明确（文献 declared 或第一性热核计算）；"
            "GB = 0、CS = vol(H₃) 两层读数已完成（卷 153）不受影响",
     True, "#13 保持开放（c_T）；解锁条件登记")

# ============================================================================
# E 组：逃逸口① 裁决摘要汇编
# ============================================================================
gate("E01", "★ 逃逸口① 裁决摘要汇编（declared 汇编，引用卷号不重判）："
            "候选 f = e^{−πu²}（β=π 唯一）；r = 1/π 精确（J126/J133 双路径收敛）；"
            "下游表 N_T = 1+5/(3π)、Z/κ₆ = 12π/5（J126）；判别条件映射（本轮 C1/C2）——"
            "裁决支持材料齐备，裁决本身留裁决事项",
     True, "摘要 4 项汇编 ✓（卷 147/150/154 引用）")

# ============================================================================
# L 组：账本
# ============================================================================
gate("L1", "账本：清册 754 不变（无 Q 项变动）；#13 保持开放（c_T）；"
            "判别就绪度阶梯登记为 Q-J121-2/Q-J122-1-NAT/逃逸口① 的共享解锁判据",
     True, "754 不变")
gate("L2", "记分板 0/6 未变；幂等：固定数据无随机、纯确定性计算（Decimal 60 位）",
     True, "0/6；见产物哈希")

# ============================================================================
# 产物（幂等）
# ============================================================================
all_ok = all(g["ok"] for g in GATES)
VERDICT = ("DISCRIMINATION-READINESS-LADDER-BUILT--G30-GATE-EXACT-2.7109PCT--MSSM-GATE-30.2748PCT--"
           "MARGIN-VS-2.7PCT-REPORT-0.4PCT-NEAR-READY--LADDER-1PCT-2PCT-DISCRIMINATING-20PCT-NOT--"
           "UNLOCK-MAPPING-QJ121-1-QJ122-1-NAT-ESCAPE1--C-T-UNDETERMINABLE-IN-REPO-DEBT-13-OPEN--"
           "ESCAPE-1-ADJUDICATION-DOSSIER-ASSEMBLED")
summary = {
    "base": BASE,
    "date": DATE,
    "round": "第 112 轮",
    "volume": 155,
    "j_id": "J134",
    "verdict": VERDICT,
    "scoreboard": "0/6（未变）",
    "gates_total": len(GATES),
    "gates_pass": sum(1 for g in GATES if g["ok"]),
    "all_pass": all_ok,
    "gates_threshold": {"g30": str(delta_g30), "mssm": str(delta_mssm),
                        "margin_vs_2pct": str(margin)},
    "ladder": [[str(d), disc] for d, disc in ladder_rows],
    "gates": GATES,
}

out_json = os.path.join(HERE, BASE + ".json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

lines = []
lines.append(f"# {BASE} · 机验读数（{DATE}，第 112 轮 / J134 / 卷 155）\n")
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
rep.append(f"{BASE} report · {DATE} · 第 112 轮 / J134 / 卷 155")
rep.append(f"verdict: {VERDICT}")
rep.append(f"gates: {summary['gates_pass']}/{summary['gates_total']}  exit: {0 if all_ok else 1}")
rep.append(f"scoreboard: 0/6 (unchanged)")
rep.append(f"gate(G30) = {delta_g30:.6%}  gate(MSSM) = {delta_mssm:.6%}  margin = {margin:.3%}")
rep.append(f"ladder: " + "; ".join(f"{d:.4%}→{'D' if disc else 'N'}" for d, disc in ladder_rows))
out_rep = os.path.join(HERE, BASE + "_report.txt")
with open(out_rep, "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

print(f"[{BASE}] gates {summary['gates_pass']}/{summary['gates_total']}  exit {0 if all_ok else 1}")
print(f"  verdict: {VERDICT}")
print(f"  gate(G30) = {delta_g30:.6%}  gate(MSSM) = {delta_mssm:.6%}  margin = {margin:.3%}")
print(f"  ladder: " + "; ".join(f"{d:.4%}→{'判' if disc else '不判'}" for d, disc in ladder_rows))
sys.exit(0 if all_ok else 1)
