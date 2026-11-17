# -*- coding: utf-8 -*-
"""单侧下界攻击面：具体 GUT 候选 × 外部一手读数 × 可翻转判据。
判据 obs_type=one-sided-lower：tau_pred < tau_bound => EXCLUDED（单侧，非双侧 sigma）。
flip 演示：把 pred 翻到 bound 之上，判词串必须变化 -> 判据可证伪、非装饰。
两路独立核对：path A 用登记的对数指数；path B 用线性 years 值，互不引用。
"""
from decimal import Decimal as D, getcontext
import json
getcontext().prec = 40

# ---- 外部一手读数（写在源码里，附出处；不来自任何判定册） ----
# Super-K p->e+pi0: tau/B > 2.4e34 yr, 90% CL, 450 kton*yr, PRD 102,112011 (2020)
# Super-K p->mu+pi0: > 1.6e34 yr (same paper)
# Super-K p->nu K+ : > 5.9e33 yr, PRD 90,072005
BOUND = {
    "p_e_pi0": dict(exp=D("2.4e34"), note="Super-K PRD102,112011(2020) 450kton*yr"),
    "p_mu_pi0": dict(exp=D("1.6e34"), note="Super-K PRD102,112011(2020)"),
    "p_nu_K":   dict(exp=D("5.9e33"), note="Super-K PRD90,072005"),
}
# 候选模型预测（区间上界用于最保守判负：即便取预测区间最大值仍低于 bound 才是稳健 EXCLUDED）
# minimal SU(5): 10^(31+-1) -> 上界 1e32 ; 中心 1e31
# minimal SUSY SU(5) dim-5: < ~1e31 (PDG: ruled out)
CAND = {
    "minimal_SU5_center": dict(pred=D("1e31"), channel="p_e_pi0", src="Georgi-Glashow tau~10^(31+-1)"),
    "minimal_SU5_upper":  dict(pred=D("1e32"), channel="p_e_pi0", src="10^(31+1) conservative upper"),
    "minimal_SUSY_SU5_d5":dict(pred=D("1e31"), channel="p_nu_K",   src="PDG minimal SUSY SU(5) <1e31 dim-5"),
}

def verdict_one_sided(pred, bound):
    """单侧下界判据：pred < bound => EXCLUDED；否则 SURVIVES(该道)。
    返回 (判词串, 裕度倍数 bound/pred)。"""
    ratio = bound / pred
    v = "EXCLUDED" if pred < bound else "SURVIVES"
    return v, ratio

# path A: 用上述 D 值直接判
out = {"pathA": {}, "pathB": {}, "flip": {}, "sources": {}}
for k, c in CAND.items():
    b = BOUND[c["channel"]]["exp"]
    v, ratio = verdict_one_sided(c["pred"], b)
    out["pathA"][k] = dict(pred=str(c["pred"]), bound=str(b),
                           channel=c["channel"], verdict=v,
                           margin=str(ratio), src=c["src"])

# path B: 独立用 log10 指数比较（不引用 pathA 的 D 对象）—— 两路须一致
import math
LOG_BOUND = {"p_e_pi0": 34 + math.log10(D("2.4")),
             "p_mu_pi0": 34 + math.log10(D("1.6")),
             "p_nu_K": 33 + math.log10(D("5.9"))}
LOG_PRED = {
    "minimal_SU5_center": 31.0,
    "minimal_SU5_upper": 32.0,
    "minimal_SUSY_SU5_d5": 31.0,
}
for k, lp in LOG_PRED.items():
    ch = CAND[k]["channel"]
    lb = LOG_BOUND[ch]
    vb = "EXCLUDED" if lp < lb else "SURVIVES"
    out["pathB"][k] = dict(log_pred=str(lp), log_bound=str(round(float(lb), 6)),
                           verdict=vb)
    out["sources"][k] = CAND[k]["src"]

# 一致性门禁：两路判词逐项相等
out["two_path_consistent"] = all(
    out["pathA"][k]["verdict"] == out["pathB"][k]["verdict"] for k in CAND
)

# flip 演示：把 minimal SU(5) 中心预测翻到 1e36（高于 bound），判词须从 EXCLUDED 变 SURVIVES
v0, _ = verdict_one_sided(D("1e31"), BOUND["p_e_pi0"]["exp"])
v1, r1 = verdict_one_sided(D("1e36"), BOUND["p_e_pi0"]["exp"])
out["flip"] = dict(original=v0, flipped=v1, flipped_pred="1e36",
                   changed=(v0 != v1),
                   verdict="FLIP-WORKS--PREDICATE-NON-DECORATIVE" if v0 != v1 else "FLIP-FAILED")

# 汇总判词：所有列出候选是否被单侧下界排除
n_excl = sum(1 for k in CAND if out["pathA"][k]["verdict"] == "EXCLUDED")
out["final"] = (
    f"ONESIDED-GUT-ATTACK--CAND-{len(CAND)}--EXCLUDED-{n_excl}"
    f"--TWOPATH-{out['two_path_consistent']}--FLIP-{out['flip']['changed']}"
    "--NOTE-EXCLUDES-SPECIFIC-MODELS-NOT-UFT"
)
print(json.dumps(out, ensure_ascii=False, indent=2))
with open("D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/_外部材料审计_2026-11-17/alg_onesided_gut_attack.json","w",encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
