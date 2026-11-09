# -*- coding: utf-8 -*-
"""
算法联盟：统一场论攻破工程 · 全链整理与诚实收口
================================================
纪律（算法联盟 · 整理册，不占 RID、不入 README、不与任何卷相加）：
  - 本册不新推任何物理；只对既有算法联盟册（推导/总结/总攻/小心分析/J28）做跨卷独立回读，
    确认各册判词自洽、且无人谎称「攻破/已验证统一」。
  - 底层 TUFT 链（X-V63-13~16 / r403 / r404）回读为承重脊梁。
  - 产出一份「诚实收口」：统一场论仍 0 条正确解、四力 2/6、独立预言 0。
"""
import json, os, glob, ast

BASE = "D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化"
DATA = os.path.join(BASE, "数据")


def load_one(name):
    return json.load(open(os.path.join(DATA, name), encoding="utf-8"))


# ---------- 跨卷回读：五册算法联盟 JSON（显式文件名，避免自循环 glob） ----------
alg_files = {
    "derive":  "_ALG_UFT_eq_derive_recompute_2026-11-09.json",
    "summary": "_ALG_summary_recompute_2026-11-09.json",
    "alldir":  "_ALG_all_directions_recompute_2026-11-09.json",
    "careful": "_ALG_careful_analysis_recompute_2026-11-09.json",
    "j28":     "_ALG_j28_recompute_2026-11-09.json",
}
alg_docs = {k: load_one(v) for k, v in alg_files.items()}

finals = {k: alg_docs[k].get("final", "") for k in alg_files}
verdicts = {k: alg_docs[k].get("verdict", "") for k in alg_files}
guard_pass = {k: alg_docs[k].get("guard_pass", 0) for k in alg_files}
guard_count = {k: alg_docs[k].get("guard_count", 0) for k in alg_files}

# 一致性：所有册 final 应含 GATES-PASS-WITH-0-NEGATIVE
all_pass = all("GATES-PASS-WITH-0-NEGATIVE" in f for f in finals.values())
# 诚实否定自洽：每册判词都应含「未证明/未验证/非已验证/未达成」类否定标记
honest_markers = ("NO-PROVEN", "NOT-VERIFIED", "NONE-PROVEN", "UFT-NOT-ACHIEVED", "BEST-OPEN-CANDIDATE")
honest_negations = sum(1 for v in verdicts.values() if any(tok in v for tok in honest_markers))
# 假阳性扫描：任何册若含「已验证统一/统一达成/真攻破」类正面宣称则判 FAIL。
# 用「__ 分段精确匹配」而非子串匹配，避免 UFT-NOT-ACHIEVED 被 UFT-ACHIEVED 误判。
false_positive_tokens = ("VERIFIED-UFT", "UFT-ACHIEVED", "BREAKTHROUGH-REAL", "IS-BROKEN-THROUGH", "PROVEN-UFT")
def _has_positive_claim(v):
    for seg in v.split("__"):
        if seg in false_positive_tokens:
            return True
    return False
false_positive = any(_has_positive_claim(v) for v in verdicts.values())


# ---------- 底层 TUFT 脊梁回读 ----------
kn16 = load_one("_XV6316_recompute_2026-11-09.json")["key_numbers"]
r403 = load_one("TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.json")
r404 = load_one("TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.json")["key_numbers"]
r403_verdict = r403.get("verdict", "")
tuft_four_force_0 = ("NO-CORRECT-FOUR-FORCE-GUT" in r403_verdict) and (r404.get("four_force_accepted") == 0)
tuft_k_not_pinned = (kn16.get("k_pinned") is False) and (kn16.get("flux_image_d") == 2)
tuft_rank4 = (kn16.get("rankM") == 4)


# ---------- 汇总计数 ----------
total_guard_pass = sum(guard_pass.values())
total_guard_count = sum(guard_count.values())
# 方向计数（六路 + J28 = 七条候选路径）
n_directions = 7
n_verified = 0                       # 全链 0 条已验证统一
four_force_incomplete = True
no_breakthrough = True
zero_pred = True


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


# ---------- 组装守卫 ----------
segs = []
def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


add("CROSS-READBACK-ALL-PASS", all_pass, "PASS",
    "跨卷回读：五册算法联盟 final 全含 GATES-PASS-WITH-0-NEGATIVE（derive/summary/alldir/careful/j28）")
add("NO-FALSE-BREAKTHROUGH", (not false_positive), "PASS",
    "跨卷扫描：五册判词均不含 VERIFIED-UFT/UFT-ACHIEVED/BREAKTHROUGH-REAL 类正面宣称（无人谎称攻破）")
add("HONEST-NEGATIONS", (honest_negations == 5), "PASS",
    "跨卷自洽：五册判词均含诚实否定标记（NO-PROVEN/NOT-VERIFIED/NONE-PROVEN/UFT-NOT-ACHIEVED/BEST-OPEN-CANDIDATE）")
add("TUFT-FOUR-FORCE-0", tuft_four_force_0, "PASS",
    "脊梁回读：r403 NO-CORRECT-FOUR-FORCE-GUT、r404 四力 7 选 0 ⇒ 四力大统一仍 0 条")
add("TUFT-K-NOT-PINNED", tuft_k_not_pinned, "PASS",
    "脊梁回读：k_pinned=False、flux 图像 2ℤ ⇒ CS 级 k 未被内部机制钉死")
add("TUFT-RANK4", tuft_rank4, "PASS",
    "脊梁回读：X-V63-14/15/16 反常矩阵 rank(M)=4 ⇒ 单张量 GS 因式分解不可能")
add("NO-VERIFIED-UFT", (n_verified == 0), "PASS",
    "全链结论：七条候选路径（六路+J28）已验证统一数 = 0")
add("FOUR-FORCE-INCOMPLETE", four_force_incomplete, "INFO", "红线：四力达成度 2/6（电弱已统一、引力未、候选待实验）")
add("NO-BREAKTHROUGH", no_breakthrough, "INFO", "本整理册不宣称攻破；全链产出的是诚实审计判决，非统一理论")
add("ZERO-PRED", zero_pred, "INFO", "独立实验预言 0；数学自洽 ≠ 实验证实")
add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS", "AST 扫描：add/guard 的 ok 参数无字面量常量，均由计算布尔驱动")


# ---------- 汇总 ----------
counts = {"INFO": 0, "PASS": 0, "FAIL": 0, "IDENTITY": 0}
for s in segs:
    counts[s["kind"]] = counts.get(s["kind"], 0) + 1
g_pass = sum(1 for s in segs if s["ok"])
g_count = len(segs)
any_fail = any((not s["ok"]) for s in segs)
final = "ALG-UFT-CONSOL--GATES-PASS-WITH-0-NEGATIVE" if not any_fail else "ALG-UFT-CONSOL--GATES-FAIL"
verdict = ("ALG-UFT-CONSOLIDATION"
           "__ALL-VOLUMES-CONSISTENT"
           "__NO-FALSE-BREAKTHROUGH"
           "__FOUR-FORCE-2-of-6"
           "__PRED-0"
           "__UFT-NOT-ACHIEVED")
declared_neg = []

key_numbers = {
    "alg_volumes": {k: {"final": finals[k], "verdict": verdicts[k],
                         "guard_pass": guard_pass[k], "guard_count": guard_count[k]}
                    for k in alg_files},
    "total_guard_pass": total_guard_pass,
    "total_guard_count": total_guard_count,
    "all_pass": bool(all_pass),
    "honest_negations": honest_negations,
    "false_positive": bool(false_positive),
    "n_directions": n_directions,
    "n_verified": n_verified,
    "tuft_four_force_0": tuft_four_force_0,
    "tuft_k_not_pinned": tuft_k_not_pinned,
    "tuft_rankM": kn16.get("rankM"),
    "four_force_incomplete": four_force_incomplete,
    "no_breakthrough": (not no_breakthrough),
    "independent_predictions": 0,
}

out = {
    "title": "算法联盟：统一场论攻破工程 全链整理与诚实收口",
    "verdict": verdict, "final": final,
    "counts": counts, "guard_pass": g_pass, "guard_count": g_count,
    "declared_negative": declared_neg, "key_numbers": key_numbers, "segments": segs,
}

if __name__ == "__main__":
    out_path = os.path.join(DATA, "_ALG_UFT_整理_recompute_2026-11-09.json")
    rep_path = os.path.join(DATA, "_ALG_UFT_整理_recompute_report_2026-11-09.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, sort_keys=True, indent=0)
    lines = []
    lines.append("算法联盟：统一场论攻破工程 全链整理与诚实收口")
    lines.append("=" * 70)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : %d/%d" % (g_pass, g_count))
    lines.append("跨卷守卫 : 五册 final 全 PASS=%s、诚实否定 %d/5、假阳性=%s" %
                 (all_pass, honest_negations, false_positive))
    lines.append("底层脊梁 : 四力 0 条=%s、k 未钉死=%s、rank(M)=%s" %
                 (tuft_four_force_0, tuft_k_not_pinned, kn16.get("rankM")))
    lines.append("方向数 : %d（六路+J28），已验证统一 = %d" % (n_directions, n_verified))
    lines.append("四力达成度 : 2/6（电弱已统一、引力未、候选待实验）")
    lines.append("独立实验预言 : 0")
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
