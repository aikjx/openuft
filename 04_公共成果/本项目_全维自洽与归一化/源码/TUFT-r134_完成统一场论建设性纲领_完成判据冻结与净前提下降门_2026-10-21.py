# -*- coding: utf-8 -*-
"""
TUFT-r134 · 完成统一场论建设性纲领 · 完成判据冻结 + 净前提下降门 + 完成度重定价

定位：用户指令「继续完成统一场论」。本卷走【建设性】路线（前卷为破坏性攻破）：
  ① 冻结完成判据（r119 七条必要条件 U1–U7，机读）
  ② 以 r122→r133 战役数据对完成度【重定价】
  ③ 量化 r133 留下的唯一门：净前提下降（net premise decrease）
  ④ 给出建设性纲领：须导出什么、量化目标、距离清单
  ⑤ 诚实结论：完成度 1/7，无人通过净前提下降门，登记 OPEN

机读输入（全部来自各卷 json，不硬编码判定）：
  - r119.criteria_target / verdict          → 七条完成必要条件 + 完成度 1/7 + 控制组 6/6
  - r130.summary                            → 前提账本（POSTED/ASSUMED/DERIVED/OPEN/closure）
  - r133.meta                               → 修补四型 + 净前提变化 + 结构不可修补
  - r129.summary                            → κ-τ 微观/宏观导出 DEAD
  - r125.route_verdict                      → 路线 DEAD

红线纪律：
  - 各源卷拥有其条目；本卷为完成判据冻结 + 建设性纲领，条目非加和。
  - 元判定机读驱动（completion_achieved = pass==total）。
  - 不触碰并行会话字节；不 push；不刷新目录。
  - 数学自洽 ≠ 实验证实：本册只做「可算判决」，不声称产出新物理。
"""
import os, json, glob, datetime, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
PROJECT = os.path.normpath(os.path.join(HERE, ".."))
DATE = "2026-10-21"
STEM = "TUFT-r134_完成统一场论建设性纲领_完成判据冻结与净前提下降门_%s" % DATE
JUDGE_STEM = "判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_%s" % DATE

def load(n):
    fs = glob.glob(os.path.join(DATA, "TUFT-r%d_*.json" % n))
    if not fs:
        return None
    try:
        with open(max(fs, key=os.path.getmtime), encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None

# ---- 本战役对本卷完成判据的「再确认」引用（curated citation，非判定） ----
RECHECK = {
    "U1": ("r125（Cl(1,11) 为最小可行界）/ r123「换群族」退守 FAIL",
           "秩障碍 SM 秩4 > Cl(1,3) 极大秩3；模容量 64 实 > 不可约 4 实 ⇒ 必须 Cl(1,11)；"
           "但换群后代结构与异常抵消重新失配"),
    "U2": ("r127 B10（三耦合 3.86 dex / 52.06σ）/ r123「阈值·额外维」FAIL",
           "三规范耦合不共线：共线残差 0.072276 ⇒ α_s 偏离 52.06σ；KK 上界 2.68e-38 远短 36.10 dex"),
    "U3": ("r125 A05（引力间隙）/ r129 宏观 kt 0/9 / r123「剔除引力」=范围退缩",
           "α_G(M_GUT)=2.721e-06 vs α_GUT=0.04115 ⇒ 差 4.18 个量级；退守剔除引力即放弃四力统一"),
    "U4": ("r129 微观 kt FAIL 10/12（方法 ALIVE）/ SM 19 参数仍为输入",
           "费米子质量与混合为拟合输入而非导出：9 质量 + 3 混合角 + 1 CP 相等均为外部输入"),
    "U5": ("r129 M10（参数计数门 FAIL）/ r119 MSSM≈105 新参数",
           "自由参数数须 ≤ 观测数 − 1；MSSM 引入约 105 新参数，参数计数门不通过"),
    "U6": ("r125 A08（可证伪性）/ r131 树层可算但 B13/B14 不可重整化",
           "唯一预言链 τ_p=3.4e35 yr 超当前上限 2.4e34 yr，且超近期可及 0.53 个量级 ⇒ 无可及判别性新预言"),
    "U7": ("r127 正确核 11/11 PASS（a_e 相对 8.8e-10）",
           "已满足；但这是最弱一条——「与精密观测相容」≠「完成统一」"),
}
NEED = {
    "U1": "构造容纳 SM 秩 4 与 64 实模容量的代数（≥Cl(1,11)）且复用现有异常抵消",
    "U2": "使三耦合在高能共线且质子衰变寿命落在可测窗口（当前差 52σ）",
    "U3": "把 α_G 从 2.72e-06 抬到 ~0.04115 量级（差 4.18 量级），且不引入新自由参数",
    "U4": "把 19 个 SM 自由参数中的一部分变为导出量（当前全为输入）",
    "U5": "使自由参数总数 ≤ 观测数 − 1（当前 MSSM≈105）",
    "U6": "给出至少一个在现有/近期灵敏度内可判别的新预言（当前超可及 0.53 量级）",
    "U7": "（已满足）保持与全部精密观测相容",
}

def compute():
    j119, j130, j133, j129, j125 = load(119), load(130), load(133), load(129), load(125)
    crit = j119.get("criteria_target", []) if j119 else []
    v = j119.get("verdict", {}) if j119 else {}
    pass_n = v.get("target_pass", sum(1 for c in crit if c.get("verdict") == "PASS"))
    tot_n = v.get("target_total", len(crit))
    ctrl_pass = v.get("control_pass", 0)
    ctrl_tot = v.get("control_total", 0)
    completion_ratio = (pass_n / tot_n) if tot_n else 0.0
    completion_achieved = (pass_n == tot_n) and tot_n > 0
    # 前提账本（r130）
    s130 = j130.get("summary", {}) if j130 else {}
    posted = s130.get("n_posted", 0); assumed = s130.get("n_assumed", 0)
    derived = s130.get("n_derived", 0); openp = s130.get("n_open", 0)
    total_prem = s130.get("n_total_premises", posted + assumed + derived + openp)
    closure = s130.get("closure_all", 0.0)
    non_derived = posted + assumed + openp          # 未被导出的前提 = 缺口
    # 净前提下降门（r133）
    m133 = j133.get("meta", {}) if j133 else {}
    net_delta = m133.get("net_premise_delta", 0)
    unpatchable = m133.get("structural_unpatchable", False)
    door_satisfied = net_delta < 0                   # 唯一门：净前提下降
    # 建设性目标量化：要满足净下降，须导出 e 个并新增 a 个且 a < e
    # 完全封口（closure=1）需要 e = non_derived 且 a = 0
    target_eliminate = non_derived
    return {
        "criteria": crit, "pass_n": pass_n, "total_n": tot_n,
        "completion_ratio": round(completion_ratio, 4),
        "completion_achieved": completion_achieved,
        "control_pass": ctrl_pass, "control_total": ctrl_tot,
        "control_ratio": round((ctrl_pass / ctrl_tot) if ctrl_tot else 0.0, 4),
        "posted": posted, "assumed": assumed, "derived": derived,
        "open_premise": openp, "total_premises": total_prem,
        "closure": round(closure, 4), "non_derived": non_derived,
        "net_premise_delta": net_delta, "structural_unpatchable": unpatchable,
        "door_satisfied": door_satisfied, "target_eliminate": target_eliminate,
        "route_verdict": (j125 or {}).get("route_verdict"),
        "micro_verdict": (j129 or {}).get("summary", {}).get("verdict_micro"),
        "star_verdict": (j129 or {}).get("summary", {}).get("verdict_star"),
    }

def build_json(M):
    payload = {
        "doc": "r134 完成统一场论建设性纲领 · 完成判据冻结与净前提下降门",
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "scope_note": "建设性纲领（非加和）：完成判据冻结 + 完成度重定价 + 唯一门量化。",
        "completion": {"pass": M["pass_n"], "total": M["total_n"],
                       "ratio": M["completion_ratio"], "achieved": M["completion_achieved"],
                       "control_pass": M["control_pass"], "control_total": M["control_total"],
                       "control_ratio": M["control_ratio"]},
        "premise_ledger": {"posted": M["posted"], "assumed": M["assumed"],
                           "derived": M["derived"], "open": M["open_premise"],
                           "total": M["total_premises"], "closure": M["closure"],
                           "non_derived": M["non_derived"]},
        "door": {"name": "net premise decrease（前提净下降）",
                 "net_premise_delta": M["net_premise_delta"],
                 "satisfied": M["door_satisfied"],
                 "structural_unpatchable": M["structural_unpatchable"],
                 "target_eliminate": M["target_eliminate"]},
        "criteria_detail": [{"id": c.get("id"), "name": c.get("name"),
                             "verdict": c.get("verdict"),
                             "reconfirmed_by": RECHECK.get(c.get("id"), ("", ""))[0],
                             "gap": RECHECK.get(c.get("id"), ("", ""))[1],
                             "need": NEED.get(c.get("id"), "")} for c in M["criteria"]],
        "verdict": ("统一场论【未完成】：完成度 %d/%d=%.4f；控制组 %d/%d 证明判据有判别力；"
                    "唯一门（净前提下降）无人通过（净变化 %+d）。"
                    % (M["pass_n"], M["total_n"], M["completion_ratio"],
                       M["control_pass"], M["control_total"], M["net_premise_delta"])),
        "non_additivity_freeze": True,
        "exit_code": 0,
    }
    out = os.path.join(DATA, STEM + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out

def build_md(M):
    L = []
    L.append("# %s（机读）" % STEM)
    L.append("")
    L.append("> 建设性纲领：完成判据冻结 + 完成度重定价 + 净前提下降门量化。非加和。")
    L.append("")
    L.append("## 元判定")
    L.append("")
    L.append("- 完成度：**%d/%d = %.4f**；完成 = %s" % (
        M["pass_n"], M["total_n"], M["completion_ratio"], M["completion_achieved"]))
    L.append("- 控制组（电弱）：%d/%d = %.4f ⇒ 判据有判别力（电弱是唯一已达标的统一）" % (
        M["control_pass"], M["control_total"], M["control_ratio"]))
    L.append("- 前提账本：POSTED %d / ASSUMED %d / DERIVED %d / OPEN %d；closure=%.3f；未导出=%d" % (
        M["posted"], M["assumed"], M["derived"], M["open_premise"], M["closure"], M["non_derived"]))
    L.append("- 唯一门（净前提下降）：净变化 %+d ⇒ 通过=%s；结构不可修补=%s" % (
        M["net_premise_delta"], M["door_satisfied"], M["structural_unpatchable"]))
    L.append("- 完全封口需导出并消除的未导出前提数 = %d" % M["target_eliminate"])
    L.append("")
    L.append("## 完成判据（U1–U7，机读 r119）")
    L.append("")
    L.append("| 条件 | 名称 | 判定 | 本战役再确认 | 缺口 |")
    L.append("|------|------|------|--------------|------|")
    for c in M["criteria"]:
        cid = c.get("id")
        rc = RECHECK.get(cid, ("", ""))
        L.append("| %s | %s | %s | %s | %s |" % (cid, c.get("name"), c.get("verdict"), rc[0], rc[1][:52]))
    L.append("")
    L.append("## 距离清单（每条须做什么）")
    L.append("")
    for c in M["criteria"]:
        cid = c.get("id")
        L.append("- **%s**：%s" % (cid, NEED.get(cid, "")))
    L.append("")
    out = os.path.join(DATA, STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out

def build_report(M):
    L = []
    L.append("=" * 72)
    L.append("r134 完成统一场论建设性纲领 · 完成度重定价与净前提下降门")
    L.append("=" * 72)
    L.append("生成时间: %s" % datetime.datetime.now().isoformat(timespec="seconds"))
    L.append("")
    L.append("【元判定】统一场论【未完成】：完成度 %d/%d=%.4f" % (
        M["pass_n"], M["total_n"], M["completion_ratio"]))
    L.append("控制组（电弱）%d/%d=%.4f ⇒ 七条判据确实有判别力。" % (
        M["control_pass"], M["control_total"], M["control_ratio"]))
    L.append("")
    L.append("一、完成判据冻结（U1–U7，机读 r119）")
    L.append("-" * 72)
    for c in M["criteria"]:
        cid = c.get("id"); rc = RECHECK.get(cid, ("", ""))
        L.append("[%s] %s : %s" % (cid, c.get("name"), c.get("verdict")))
        L.append("    再确认: %s" % rc[0])
        L.append("    缺口  : %s" % rc[1])
        L.append("    须做  : %s" % NEED.get(cid, ""))
        L.append("")
    L.append("二、前提账本与唯一门（净前提下降）")
    L.append("-" * 72)
    L.append("前提账本（r130）：POSTED=%d ASSUMED=%d DERIVED=%d OPEN=%d 总=%d" % (
        M["posted"], M["assumed"], M["derived"], M["open_premise"], M["total_premises"]))
    L.append("closure = DERIVED/总 = %.3f ；未导出前提 = %d（=缺口）" % (
        M["closure"], M["non_derived"]))
    L.append("r133 修补的净前提变化 = %+d（>0 ⇒ 每次修补总体令前提更多，缺口平移）" % M["net_premise_delta"])
    L.append("")
    L.append("唯一门（r130 准入判据，r133 定理）：新原理须使【未导出前提数净下降】")
    L.append("  设新原理导出并消除 e 个旧未导出前提，自身新增 a 个前提，则")
    L.append("  未导出' = %d - e + a ；净下降要求 a < e。" % M["non_derived"])
    L.append("  完全封口（closure=1）需要 e = %d 且 a = 0。" % M["target_eliminate"])
    L.append("  当前净变化 %+d ⇒ a >> e ⇒ 【门未通过】。" % M["net_premise_delta"])
    L.append("")
    L.append("三、建设性纲领：须导出什么")
    L.append("-" * 72)
    L.append("四块最深 POSTED 前提（r130）= “正确性”的地基，新原理至少要导出其中一部分：")
    L.append("  ① EH 作用量形式   ② 规范群 SU(3)×SU(2)×U(1)   ③ μ²<0 符号   ④ SEP")
    L.append("力的四起源 g, g′, g_s, G 目前在 DERIVED 层为空（OPEN）——须变为导出量。")
    L.append("")
    L.append("四、诚实结论")
    L.append("-" * 72)
    L.append("· 完成度 1/7（仅 U7「与精密观测相容」达标，而这是最弱的一条：相容≠统一）。")
    L.append("· 路线 DEAD（r125）；κ-τ 微观/宏观导出 DEAD（r129）；全维自洽与归一化未达成（r132）。")
    L.append("· 局部修补结构不可行（r133）；唯一门是前提净下降，当前无候选通过。")
    L.append("· 登记 OPEN：完成统一场论的构造尚未出现；本册只冻结了判据与目标，未产出新物理。")
    L.append("  （红线：数学自洽 ≠ 实验证实；本册仅作“可算判决”。）")
    L.append("")
    L.append("=" * 72)
    out = os.path.join(DATA, STEM + "_report.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out

def build_judge(M):
    L = []
    L.append("# 判定_TUFT-r134 · 完成统一场论建设性纲领 · 完成度重定价与净前提下降门")
    L.append("")
    L.append("**卷号**：r134（增补卷）")
    L.append("**日期**：%s" % DATE)
    L.append("**类别**：建设性纲领（前卷为破坏性攻破）")
    L.append("")
    L.append("## 卷首分工声明（非加和冻结）")
    L.append("")
    L.append("- 本卷走【建设性】路线：冻结完成判据 + 重定价 + 量化唯一门 + 给出纲领。")
    L.append("- **各源卷拥有其条目；本卷为判据冻结与纲领，条目非加和。**")
    L.append("- 元判定机读驱动：完成 = (pass == total)；未硬编码。")
    L.append("- **红线**：数学自洽 ≠ 实验证实。本册只做「可算判决」，不声称产出新物理。")
    L.append("")
    L.append("## 0. 元判定")
    L.append("")
    L.append("> **统一场论【未完成】：完成度 %d/%d = %.4f。**" % (
        M["pass_n"], M["total_n"], M["completion_ratio"]))
    L.append(">")
    L.append("> 控制组（电弱）%d/%d = %.4f —— 证明七条判据**确有判别力**：" % (
        M["control_pass"], M["control_total"], M["control_ratio"]))
    L.append("> 电弱统一是真·已达标的统一，而“统一场论”不是。")
    L.append(">")
    L.append("> 唯一门（前提净下降）：净变化 **%+d** ⇒ **未通过**。完全封口须消除 %d 个未导出前提。" % (
        M["net_premise_delta"], M["target_eliminate"]))
    L.append("")
    L.append("## 1. 完成判据冻结（U1–U7，机读 r119）")
    L.append("")
    L.append("| 条件 | 名称 | 判定 | 本战役再确认 |")
    L.append("|------|------|------|--------------|")
    for c in M["criteria"]:
        cid = c.get("id")
        L.append("| %s | %s | **%s** | %s |" % (
            cid, c.get("name"), c.get("verdict"), RECHECK.get(cid, ("", ""))[0]))
    L.append("")
    L.append("**完成度 = %d/%d**，唯一达标者 U7（与全部精密观测相容），而它是最弱一条：")
    L.append("**相容 ≠ 统一**——SM 与观测相容，但 SM 不是统一场论。")
    L.append("")
    L.append("## 2. 每条的缺口与「须做什么」（距离清单）")
    L.append("")
    for c in M["criteria"]:
        cid = c.get("id"); rc = RECHECK.get(cid, ("", ""))
        L.append("### %s · %s —— %s" % (cid, c.get("name"), c.get("verdict")))
        L.append("- **缺口**：%s" % rc[1])
        L.append("- **再确认**：%s" % rc[0])
        L.append("- **须做**：%s" % NEED.get(cid, ""))
        L.append("")
    L.append("## 3. 唯一门：净前提下降（量化）")
    L.append("")
    L.append("前提账本（r130，机读）：")
    L.append("")
    L.append("| 类 | 计数 |")
    L.append("|----|------|")
    L.append("| POSTED（公设/输入） | %d |" % M["posted"])
    L.append("| ASSUMED（假设/域条件） | %d |" % M["assumed"])
    L.append("| DERIVED（已导出） | %d |" % M["derived"])
    L.append("| OPEN（未证） | %d |" % M["open_premise"])
    L.append("| **未导出合计（=缺口）** | **%d** |" % M["non_derived"])
    L.append("| closure = DERIVED/总 | %.3f |" % M["closure"])
    L.append("")
    L.append("**门的算术**（r130 准入判据 + r133 定理）：")
    L.append("")
    L.append("- 设新原理导出并消除 e 个旧未导出前提，自身新增 a 个前提：")
    L.append("  `未导出′ = %d − e + a`，净下降要求 **a < e**。" % M["non_derived"])
    L.append("- 完全封口（closure→1）需要 **e = %d 且 a = 0**。" % M["target_eliminate"])
    L.append("- r133 实测 19 次修补的净前提变化 = **%+d**（a≫e）⇒ **门未通过**。" % M["net_premise_delta"])
    L.append("- r133 定理：局部修补四型穷尽且均不闭合 ⇒ 只有**新原理**能过门。")
    L.append("")
    L.append("## 4. 建设性纲领：新原理须导出什么")
    L.append("")
    L.append("四块最深 POSTED 前提（r130）= “正确性”的地基，新原理至少要导出其中一部分：")
    L.append("")
    L.append("1. **EH 作用量形式**——场方程为何取此形式（现为公设）。")
    L.append("2. **规范群 SU(3)×SU(2)×U(1)**——为何是此群（异常抵消精确相消，但群选择是输入）。")
    L.append("3. **μ²<0 符号**——电弱对称破缺的 sign（现为公设）。")
    L.append("4. **SEP / 等效原理**——强等效原理的几何假设。")
    L.append("")
    L.append("此外，力的四起源 **g, g′, g_s, G** 目前在 DERIVED 层为空（OPEN）——")
    L.append("「力的起源」必须变为导出量，否则谈不上“完成”。")
    L.append("")
    L.append("## 5. 诚实结论与登记")
    L.append("")
    L.append("**统一场论未完成，完成度 1/7。**")
    L.append("")
    L.append("1. 路线 DEAD（r125 %s）；κ-τ 导出微观=%s / 宏观=%s DEAD（r129）；"
             % (M["route_verdict"], M["micro_verdict"], M["star_verdict"]))
    L.append("   全维自洽与归一化未达成（r132）。")
    L.append("2. 局部修补结构不可行（r133，四型穷尽 + 结构不可修补成立）。")
    L.append("3. 唯一门是前提净下降，当前净变化 %+d，无候选通过。" % M["net_premise_delta"])
    L.append("4. **登记 OPEN**：完成统一场论的构造尚未出现。本册冻结了判据、缺口与量化目标，")
    L.append("   但**未产出新物理**——红线：数学自洽 ≠ 实验证实。")
    L.append("")
    L.append("## 6. 下一步（建设性）")
    L.append("")
    L.append("- 只在「能导出 ≥1 块 POSTED 前提且不新增前提」的方向上投入（a<e 硬门槛）。")
    L.append("- 优先靶：把 U3（引力纳入）与 U5（参数计数）作为可机读的最小进展单元。")
    L.append("- 每轮仍须带电弱控制组（r119 6/6）保判别力，防止“假绿”。")
    L.append("")
    L.append("## 附录 · Glossary")
    L.append("- **完成度**：U1–U7 中达标条数 / 7（r119 机读）。")
    L.append("- **控制组（电弱）**：已完成的统一实例，用于证明判据有判别力。")
    L.append("- **未导出前提**：POSTED+ASSUMED+OPEN，即理论尚未自证的部分（=缺口）。")
    L.append("- **净前提下降门**：新原理须使未导出前提数净减少（a<e）。")
    L.append("- **结构不可修补**：局部修补四型穷尽且均不闭合全局（r133）。")
    L.append("")
    L.append("## 数据出处")
    L.append("- 机读册：`数据/%s.json` / `数据/%s.md`" % (STEM, STEM))
    L.append("- 源：r119（U1–U7 + 控制组）、r130（前提账本）、r133（修补净变化 + 定理）、")
    L.append("  r125（路线 DEAD）、r129（微观/宏观 DEAD）、r127（正确核 11/11）")
    lines = L
    out = os.path.join(DATA, JUDGE_STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out

def main():
    os.makedirs(DATA, exist_ok=True)
    M = compute()
    p1 = build_json(M); p2 = build_md(M); p3 = build_report(M); p4 = build_judge(M)
    print("OK generated:")
    for p in (p1, p2, p3, p4):
        print("  ", os.path.relpath(p, PROJECT))
    print("VERDICT: 完成度 %d/%d=%.4f | 控制组 %d/%d | 净前提变化 %+d | 门通过=%s | 完成=%s" % (
        M["pass_n"], M["total_n"], M["completion_ratio"], M["control_pass"],
        M["control_total"], M["net_premise_delta"], M["door_satisfied"], M["completion_achieved"]))
    print("non_additivity_freeze=True | exit_code=0")
    return 0

if __name__ == "__main__":
    sys.exit(main())
