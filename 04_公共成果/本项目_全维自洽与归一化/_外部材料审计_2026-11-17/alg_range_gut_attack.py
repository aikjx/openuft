# -*- coding: utf-8 -*-
"""单侧下界区间判据：对 6 个具体 GUT 模型做三态裁决（EXCLUDED / PARTIAL / SURVIVES）。
设计要点：
  - 用【预测区间 [lo,hi]】而非点值，三态判据：
        hi < bound           => EXCLUDED（整个预测区间被排除）
        lo > bound           => SURVIVES（整个预测区间存活，负对照）
        lo <= bound <= hi    => PARTIAL（区间跨越实验下界）
  - 必须存在 SURVIVES 样本（flipped SU(5) / Split SUSY），否则判据退化为"全判负"装饰门。
  - 两路独立核对：path A 线性 Decimal；path B 独立 log10 指数。
  - flip：把最小 SU(5) 区间平移到 [1e35,1e36]，判词须 EXCLUDED -> SURVIVES。
外部一手读数（写入源码，附出处）：
  p->e+pi0 : tau/B > 2.4e34 yr (90% CL), SK I-IV 450 kton*yr, PRD 102,112011(2020)
  p->nu K+ : tau/B > 5.9e33 yr (90% CL), PRD 90,072005
模型预测区间来源：PDG GUT review / 质子衰变寿命汇总表（含 SUSY SO(10)、flipped SU(5)、Split SUSY）。
"""
from decimal import Decimal as D, getcontext
import json, math
getcontext().prec = 40

BOUND = {
    "p_e_pi0": D("2.4e34"),
    "p_nu_K":  D("5.9e33"),
}

# 模型预测区间（年），来源：PDG GUT review / proton decay lifetime 汇总
MODELS = {
    "minimal_SU5":        dict(lo=D("1e30"), hi=D("1e31"), ch="p_e_pi0", label="最小 SU(5)"),
    "minimal_SUSY_SU5":   dict(lo=D("1e28"), hi=D("1e32"), ch="p_nu_K",  label="最小 SUSY SU(5)"),
    "SUSY_SO10":          dict(lo=D("1e32"), hi=D("1e35"), ch="p_e_pi0", label="SUSY SO(10)"),
    "minimal_SO10_nonSUSY":dict(lo=D("1e32"),hi=D("1e36"), ch="p_e_pi0", label="最小 SO(10) 非SUSY"),
    "flipped_SU5_MSSM":   dict(lo=D("1e35"), hi=D("1e36"), ch="p_e_pi0", label="flipped SU(5) MSSM"),
    "split_SUSY_SU5":     dict(lo=D("1e35"), hi=D("1e37"), ch="p_e_pi0", label="Split SUSY SU(5)"),
}

def verdict_range(lo, hi, bound):
    if hi < bound:  return "EXCLUDED"
    if lo > bound:  return "SURVIVES"
    return "PARTIAL"

out = {"pathA": {}, "pathB": {}, "flip": {}, "summary": {}}
for k, m in MODELS.items():
    b = BOUND[m["ch"]]
    v = verdict_range(m["lo"], m["hi"], b)
    out["pathA"][k] = dict(label=m["label"], lo=str(m["lo"]), hi=str(m["hi"]),
                           bound=str(b), ch=m["ch"], verdict=v)

# path B：独立 log10 比较
LB = {"p_e_pi0": 34 + math.log10(2.4), "p_nu_K": 33 + math.log10(5.9)}
LO = {"minimal_SU5":(30,31),"minimal_SUSY_SU5":(28,32),"SUSY_SO10":(32,35),
      "minimal_SO10_nonSUSY":(32,36),"flipped_SU5_MSSM":(35,36),"split_SUSY_SU5":(35,37)}
for k,(lo,hi) in LO.items():
    lb = LB[MODELS[k]["ch"]]
    vb = "EXCLUDED" if hi < lb else ("SURVIVES" if lo > lb else "PARTIAL")
    out["pathB"][k] = dict(log_lo=str(lo), log_hi=str(hi),
                           log_bound=str(round(float(lb),6)), verdict=vb)

out["two_path_consistent"] = all(
    out["pathA"][k]["verdict"] == out["pathB"][k]["verdict"] for k in MODELS)

# 三态统计
cnt = {"EXCLUDED":0,"PARTIAL":0,"SURVIVES":0}
for k in MODELS: cnt[out["pathA"][k]["verdict"]] += 1
out["summary"] = dict(models=len(MODELS), excluded=cnt["EXCLUDED"],
                      partial=cnt["PARTIAL"], survives=cnt["SURVIVES"],
                      negctrl_present=(cnt["SURVIVES"]>0))

# flip：最小 SU(5) 平移到 [1e35,1e36]
v0 = verdict_range(D("1e30"), D("1e31"), BOUND["p_e_pi0"])
v1 = verdict_range(D("1e35"), D("1e36"), BOUND["p_e_pi0"])
out["flip"] = dict(original=v0, flipped=v1, changed=(v0!=v1),
                   verdict="FLIP-WORKS--PREDICATE-NON-DECORATIVE" if v0!=v1 else "FLIP-FAILED")

out["final"] = (
    f"ONESIDED-RANGE-ATTACK--MODELS-{len(MODELS)}--EXCLUDED-{cnt['EXCLUDED']}"
    f"--PARTIAL-{cnt['PARTIAL']}--SURVIVES-{cnt['SURVIVES']}"
    f"--NEGCTRL-{cnt['SURVIVES']>0}--TWOPATH-{out['two_path_consistent']}"
    f"--FLIP-{out['flip']['changed']}--NOTE-SPECIFIC-MODELS-NOT-UFT"
)
print(json.dumps(out, ensure_ascii=False, indent=2))
with open("D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/_外部材料审计_2026-11-17/alg_range_gut_attack.json","w",encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
