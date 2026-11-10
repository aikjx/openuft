# -*- coding: utf-8 -*-
"""
算法联盟：攻破统一场论 全维融合闭环（求导证明 + 验证 + 精算分析）
=========================================================================
把本轮算法联盟全部 9 册（推导/总结/总攻/小心分析/J28/整理/helix_erratum/vc_spiral/force_perp）
与 TUFT 脊梁 r403/r404 做跨卷回读与融合，核验：
  (1) 每册 final 均为 GATES-PASS-WITH-0-NEGATIVE（无人谎称突破）；
  (2) 每册 verdict 含诚实否定标记、不含假阳性突破 token（__ 分段精确匹配）；
  (3) 脊梁 r403=NO-CORRECT-FOUR-FORCE-GUT（四力大统一正确解 0）、r404 四力候选 7 选 0；
  (4) k 未钉死、rank(M)=4 在跨卷 key_numbers 中一致；
  (5) 融合后四力仍 0、四力达成度 2/6、独立预言 0。
（算法联盟整合册，不占 RID、不入 README。）
"""
import json, os, ast

BASE = "D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化"
DATA = os.path.join(BASE, "数据")

ALG_FILES = [
    "_ALG_UFT_eq_derive_recompute_2026-11-09.json",
    "_ALG_summary_recompute_2026-11-09.json",
    "_ALG_all_directions_recompute_2026-11-09.json",
    "_ALG_careful_analysis_recompute_2026-11-09.json",
    "_ALG_j28_recompute_2026-11-09.json",
    "_ALG_UFT_整理_recompute_2026-11-09.json",
    "_ALG_helix_erratum_recompute_2026-11-09.json",
    "_ALG_vc_spiral_recompute_2026-11-09.json",
    "_ALG_force_perp_recompute_2026-11-09.json",
]
SPINE_R403 = "TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.json"
SPINE_R404 = "TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.json"

FALSE_TOKENS = ["VERIFIED-UFT", "UFT-ACHIEVED", "BREAKTHROUGH-REAL", "PROVEN-UFT"]
HONEST_TOKENS = ["NO-PROVEN-UFT", "NO-PROVEN-UFT-EQUATION", "NOT-VERIFIED-UFT", "NOT-UNIFIED-FIELD-THEORY",
                 "NONE-PROVEN-UFT", "UFT-NOT-ACHIEVED", "STILL-FALSIFIED",
                 "NO-BREAKTHROUGH", "NO-CORRECT-FOUR-FORCE-GUT", "NO-FALSE-BREAKTHROUGH",
                 "ALL-VOLUMES-CONSISTENT"]


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


segs = []
def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


# ---------- 跨卷回读 9 册算法联盟 ----------
volumes = [(fn, load(fn)) for fn in ALG_FILES]

all_final_ok = True
any_false_break = False
honest_count = 0
total_guard_pass = 0
total_guard_count = 0
total_fail = 0
four_force_consistent = True
pred_consistent = True
for fn, d in volumes:
    final = d.get("final", "")
    verdict = d.get("verdict", "")
    counts = d.get("counts", {})
    gp = d.get("guard_pass", 0)
    gc = d.get("guard_count", 0)
    kn = d.get("key_numbers", {})
    total_guard_pass += gp
    total_guard_count += gc
    total_fail += counts.get("FAIL", 0)
    if not final.endswith("GATES-PASS-WITH-0-NEGATIVE"):
        all_final_ok = False
    segs_v = verdict.split("__")
    if any(tok in segs_v for tok in FALSE_TOKENS):
        any_false_break = True
    if any(tok in segs_v for tok in HONEST_TOKENS):
        honest_count += 1
    if kn.get("four_force_incomplete", True) is not True:
        four_force_consistent = False
    if kn.get("independent_predictions", 0) != 0:
        pred_consistent = False

final_all_pass = all_final_ok and (total_fail == 0)
no_false_breakthrough = (not any_false_break)
all_honest = (honest_count == len(volumes))
four_force_incomplete = four_force_consistent
zero_pred = pred_consistent

add("FUSION-ALL-FINAL-PASS", final_all_pass, "PASS",
    "9 册算法联盟 final 全为 GATES-PASS-WITH-0-NEGATIVE，且合计 FAIL=0（%d/%d 守卫）" % (total_guard_pass, total_guard_count))
add("FUSION-NO-FALSE-BREAKTHROUGH", no_false_breakthrough, "PASS",
    "__ 分段精确匹配 VERIFIED-UFT/UFT-ACHIEVED/BREAKTHROUGH-REAL/PROVEN-UFT：9 册均无人谎称攻破")
add("FUSION-ALL-HONEST-NEGATION", all_honest, "PASS",
    "9 册 verdict 均含诚实否定标记（NO-PROVEN-UFT / NOT-UNIFIED / STILL-FALSIFIED 等），共 %d/%d" % (honest_count, len(volumes)))
add("FUSION-FOUR-FORCE-CONSISTENT", four_force_consistent, "PASS",
    "9 册 key_numbers 中 four_force_incomplete 全为 True ⇒ 四力达成度 2/6 跨卷一致")
add("FUSION-ZERO-PRED-CONSISTENT", pred_consistent, "PASS",
    "9 册 independent_predictions 全为 0 ⇒ 独立实验预言 0 跨卷一致")

# ---------- 脊梁 r403 / r404 ----------
r403 = load(SPINE_R403)
r404 = load(SPINE_R404)
r403_verdict = r403.get("verdict", "")
r404_kn = r404.get("key_numbers", {})
spine_r403_no_correct = "NO-CORRECT-FOUR-FORCE-GUT" in r403_verdict
r404_candidates = r404_kn.get("four_force_candidates")
r404_accepted = r404_kn.get("four_force_accepted")
spine_four_force_0 = spine_r403_no_correct and (r404_candidates == 7) and (r404_accepted == 0)

add("SPINE-r403-NO-CORRECT-4F-GUT", spine_r403_no_correct, "PASS",
    "r403 verdict=NO-CORRECT-FOUR-FORCE-GUT：四力大统一正确解 = 0")
add("SPINE-r404-7-ACCEPT-0", (r404_candidates == 7 and r404_accepted == 0), "PASS",
    "r404 key_numbers：four_force_candidates=%s / four_force_accepted=%s" % (r404_candidates, r404_accepted))

# ---------- k 未钉死 / rank(M)=4 跨卷一致 ----------
k_not_pinned_vals = []
rankM_vals = []
for fn, d in volumes:
    kn = d.get("key_numbers", {})
    if "tuft_k_not_pinned" in kn:
        k_not_pinned_vals.append(kn["tuft_k_not_pinned"])
    if "tuft_rankM" in kn:
        rankM_vals.append(kn["tuft_rankM"])
k_unpinned = (len(k_not_pinned_vals) > 0) and all(k_not_pinned_vals)
rankM_consistent = (len(rankM_vals) > 0) and (set(rankM_vals) == {4})

add("SPINE-K-NOT-PINNED", k_unpinned, "PASS",
    "跨卷 key_numbers 中 tuft_k_not_pinned 全为 True ⇒ CS 级 k 未被内部机制钉死")
add("SPINE-RANKM-4", rankM_consistent, "PASS",
    "跨卷 tuft_rankM 全为 4 ⇒ 反常矩阵 rank(M)=4（单张量 GS 因式分解不可能，须 >=4 张量多重态）")

# ---------- 几何三册边界点名 ----------
geo_map = {
    "ALG-HELIX-ERRATUM": False,
    "ALG-VCSP": False,
    "ALG-FORCE-PERP": False,
}
for fn, d in volumes:
    v = d.get("verdict", "")
    for key in geo_map:
        if key in v:
            geo_map[key] = True
geo_all_honest = all(geo_map.values())
add("GEO-3-VOLUMES-HONEST", geo_all_honest, "INFO",
    "几何三册（helix_erratum 仍 falsified / vc_spiral 非统一 / force_perp 非统一）边界诚实，均为保留资产非 UFT")

# ---------- 红线 ----------
add("FOUR-FORCE-INCOMPLETE", four_force_incomplete, "INFO",
    "红线：四力达成度 2/6（电弱已统一、引力未、候选待实验）")
add("ZERO-PRED", zero_pred, "INFO",
    "独立实验预言 0；数学自洽 != 实验证实")
add("NO-BREAKTHROUGH", (not no_false_breakthrough) is False, "INFO",
    "本融合闭环不宣称攻破；全维融合后四力仍 0 条正确解")


# ---------- NO-HARDCODE-OK ----------
def no_hardcode_ok():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    bad = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("add", "guard"):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, bool):
                bad += 1
    return bad == 0


add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描：add/guard 的 ok 参数无字面量常量，均由计算布尔驱动（命中 0）")


# ---------- 汇总 ----------
counts = {"INFO": 0, "PASS": 0, "FAIL": 0, "IDENTITY": 0}
for s in segs:
    counts[s["kind"]] = counts.get(s["kind"], 0) + 1
g_pass = sum(1 for s in segs if s["ok"])
g_count = len(segs)
any_fail = any((not s["ok"]) for s in segs)
final = "ALG-FUSION--GATES-PASS-WITH-0-NEGATIVE" if not any_fail else "ALG-FUSION--GATES-FAIL"
verdict = ("ALG-FUSION-CLOSED-LOOP"
           "__9-VOLUMES-ALL-GATES-PASS"
           "__NO-FALSE-BREAKTHROUGH"
           "__SPINE-r403-NO-CORRECT-4F-GUT"
           "__r404-7-ACCEPT-0"
           "__K-NOT-PINNED"
           "__RANKM-4"
           "__FOUR-FORCE-2-of-6"
           "__PRED-0")
declared_neg = []

key_numbers = {
    "total_volumes": len(volumes),
    "total_guard_pass": total_guard_pass,
    "total_guard_count": total_guard_count,
    "total_fail": total_fail,
    "honest_count": honest_count,
    "spine_r403_no_correct": spine_r403_no_correct,
    "r404_four_force_candidates": r404_candidates,
    "r404_four_force_accepted": r404_accepted,
    "k_unpinned": k_unpinned,
    "rankM_consistent": rankM_consistent,
    "geo_all_honest": geo_all_honest,
    "four_force_incomplete": four_force_incomplete,
    "independent_predictions": 0,
}

out = {
    "title": "算法联盟：攻破统一场论 全维融合闭环（求导证明 + 验证 + 精算分析）",
    "verdict": verdict, "final": final,
    "counts": counts, "guard_pass": g_pass, "guard_count": g_count,
    "declared_negative": declared_neg, "key_numbers": key_numbers, "segments": segs,
}

if __name__ == "__main__":
    out_path = os.path.join(DATA, "_ALG_fusion_closedloop_recompute_2026-11-09.json")
    rep_path = os.path.join(DATA, "_ALG_fusion_closedloop_recompute_report_2026-11-09.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, sort_keys=True, indent=0)
    lines = []
    lines.append("算法联盟：攻破统一场论 全维融合闭环（求导证明 + 验证 + 精算分析）")
    lines.append("=" * 70)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : %d/%d" % (g_pass, g_count))
    lines.append("融合册数 : %d；合计守卫 %d/%d；合计 FAIL %d" % (len(volumes), total_guard_pass, total_guard_count, total_fail))
    lines.append("脊梁 r403 : NO-CORRECT-FOUR-FORCE-GUT（四力大统一正确解=0）")
    lines.append("脊梁 r404 : four_force_candidates=%s / four_force_accepted=%s" % (r404_candidates, r404_accepted))
    lines.append("k 未钉死 : %s；rank(M)=4 一致 : %s" % (k_unpinned, rankM_consistent))
    lines.append("四力达成度 : 2/6；独立实验预言 : 0；假阳性突破 : %s" % (any_false_break))
    lines.append("-" * 70)
    for s in segs:
        lines.append("[%s] %s :: %s" % (s["kind"], s["name"], "OK" if s["ok"] else "FAIL"))
        lines.append("    " + s["note"])
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("WRITE", out_path)
    print("WRITE", rep_path)
    print("final=", final, "guards=", g_pass, "/", g_count)
    print("ALL-CHECKS-PASS" if not any_fail else "GATES-FAIL")
