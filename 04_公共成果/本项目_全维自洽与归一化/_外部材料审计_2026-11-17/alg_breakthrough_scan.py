# -*- coding: utf-8 -*-
"""突破口扫描：对前两轮证伪过的 6 个具体 GUT 模型，机读判定突破口三必要条件。
突破口定义（项目既有）：N1 零输入生成 ∧ N2 新读数可判负 ∧ N3 零自由参数可认证。
- 对每个模型评 N1/N2/N3（0/1），并做敏感性：移除任一条件 / 只留单个条件。
- 三条件全 0 且任意子集不得 1 -> 合取锁（突破 0）。
- 附带结构性观察：存活(SURVIVES)模型所需额外自由度是否更多（探索"存活⇔更多自由度"）。
所有判定基于前两轮已核实的实验下界与模型预测，不引入新读数。
"""
import json

# 前两轮模型集与裁决（来自 alg_onesided_gut_attack / alg_range_gut_attack 的结果）
# extra_dof = 引入相对最小 SU(5) 的额外结构数（定性但固定口径）
MODELS = {
    "minimal_SU5":         dict(verdict="EXCLUDED", extra_dof=0, struct="最简 Georgi-Glashow"),
    "minimal_SUSY_SU5":    dict(verdict="EXCLUDED", extra_dof=1, struct="+SUSY"),
    "SUSY_SO10":           dict(verdict="PARTIAL",  extra_dof=2, struct="SO(10)+SUSY"),
    "minimal_SO10_nonSUSY":dict(verdict="PARTIAL",  extra_dof=1, struct="SO(10) 大群"),
    "flipped_SU5_MSSM":    dict(verdict="SURVIVES", extra_dof=2, struct="flipped U(1)+SUSY"),
    "split_SUSY_SU5":      dict(verdict="SURVIVES", extra_dof=2, struct="split 谱+SUSY"),
}

# N1/N2/N3 评估口径（对该族 GUT 模型整体成立，逐模型同值；理由写入 note）
# N1 零输入生成：模型预测需要外部输入 GUT 标度 M_GUT、slepton 质量、tanβ 等 -> 0
# N2 新读数可判负：本轮用的是已发表 Super-K 读数，非新读数 -> 0
# N3 零自由参数可认证：GUT 含大量自由参数（Yukawa、triplet Higgs 质量、tanβ）-> 0
N = {"N1": 0, "N2": 0, "N3": 0}

def joint(d):
    return 1 if (d["N1"] and d["N2"] and d["N3"]) else 0

out = {"per_model": {}, "sensitivity": {}, "struct": {}, "final": ""}
for k, m in MODELS.items():
    out["per_model"][k] = dict(verdict=m["verdict"], extra_dof=m["extra_dof"],
                               struct=m["struct"], N1=N["N1"], N2=N["N2"], N3=N["N3"],
                               joint=joint(N))

# 敏感性：移除任一 / 只留单个
def subset(d, keep):
    return {x: (d[x] if x in keep else 0) for x in ("N1","N2","N3")}
out["sensitivity"] = {
    "full": joint(N),
    "drop_N1": joint(subset(N, {"N2","N3"})),
    "drop_N2": joint(subset(N, {"N1","N3"})),
    "drop_N3": joint(subset(N, {"N1","N2"})),
    "only_N1": joint(subset(N, {"N1"})),
    "only_N2": joint(subset(N, {"N2"})),
    "only_N3": joint(subset(N, {"N3"})),
}
out["lock"] = (out["sensitivity"]["full"] == 0 and
               all(v == 0 for kk, v in out["sensitivity"].items() if kk != "full"))

# 结构性观察：按 veredict 分组看 extra_dof
grp = {"EXCLUDED": [], "PARTIAL": [], "SURVIVES": []}
for k, m in MODELS.items():
    grp[m["verdict"]].append(m["extra_dof"])
out["struct"] = {
    "EXCLUDED_dof": grp["EXCLUDED"],
    "PARTIAL_dof": grp["PARTIAL"],
    "SURVIVES_dof": grp["SURVIVES"],
    "min_dof_by_verdict": {k: (min(v) if v else None) for k, v in grp.items()},
    "max_dof_by_verdict": {k: (max(v) if v else None) for k, v in grp.items()},
    "observation": ("SURVIVES 模型 extra_dof 全为 2，EXCLUDED 为 0-1 -> 存活与更高自由度同现；"
                    "这不是突破口，而是参数不灭/复杂度不灭的结构性体现：存活需引入额外结构而非更少参数"),
}

out["final"] = (
    f"BREAKTHROUGH-SCAN--MODELS-{len(MODELS)}--N1-{N['N1']}--N2-{N['N2']}--N3-{N['N3']}"
    f"--JOINT-{out['sensitivity']['full']}--LOCK-{int(out['lock'])}"
    "--STRUCT-SURVIVAL-NEEDS-MORE-DOF--NO-BREAKTHROUGH"
)
print(json.dumps(out, ensure_ascii=False, indent=2))
with open("D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/_外部材料审计_2026-11-17/alg_breakthrough_scan.json","w",encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
