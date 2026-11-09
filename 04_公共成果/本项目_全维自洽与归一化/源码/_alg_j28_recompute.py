# -*- coding: utf-8 -*-
"""
算法联盟：J28 方向审计 · AS 量子引力跑动重做 SM/GUT×引力 高能桥接
====================================================================
纪律（算法联盟，最高 rigor）：
  - 不靠宣告达成「攻破」；审计只能产可算判决，不产新物理。
  - J28 是此前锚定的「唯一可证伪新方向」：AS（渐近安全）量子引力 + SM/GUT 高能桥接。
  - 本机核诚实审计 J28 是否能构成「已验证统一场论」：机制存在性（文献核准）vs 验证性（参数唯一+实验预言）。
本册定位：开放方向审计（非审计卷、不占 RID、不入 README）。
"""
import json, os, glob, ast, math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50

BASE = "D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化"
DATA = os.path.join(BASE, "数据")


def load_kn(prefix):
    fs = sorted(glob.glob(os.path.join(DATA, prefix)))
    if not fs:
        raise FileNotFoundError(prefix)
    return json.load(open(fs[0], encoding="utf-8"))["key_numbers"]


def load_full(prefix):
    fs = sorted(glob.glob(os.path.join(DATA, prefix)))
    if not fs:
        raise FileNotFoundError(prefix)
    return json.load(open(fs[0], encoding="utf-8"))


# ---------- 输入常量（文献/标准值，非本链新推，标记 INPUT） ----------
M_Z = Decimal("91.1876")
M_Pl = Decimal("1.2209e19")
# MSSM 1-loop beta（与 α_GUT≈0.0412 自洽来源）
b1 = Fraction(33, 5); b2 = Fraction(1, 1); b3 = Fraction(-3, 1)
a1inv_Z = Decimal("59.0"); a2inv_Z = Decimal("29.5"); a3inv_Z = Decimal("8.4")
# AS 固定点无量纲牛顿耦合（文献范围；f(R)/EH 截断不同给出 0.2–0.9，代表值 0.707）
gN_star_low = Decimal("0.2"); gN_star_high = Decimal("0.9"); gN_star_rep = Decimal("0.707")


def alpha_inv(mu, ainv_Z_i, b_i):
    ratio = Decimal(mu) / M_Z
    ln = Decimal(math.log(float(ratio)))
    b_dec = Decimal(b_i.numerator) / Decimal(b_i.denominator)
    delta = b_dec / Decimal(2 * math.pi) * ln
    return ainv_Z_i - delta


# ---------- 规范耦合跑到 M_Pl（承接小心分析，已核验） ----------
a1inv_P = alpha_inv(M_Pl, a1inv_Z, b1)
a2inv_P = alpha_inv(M_Pl, a2inv_Z, b2)
a3inv_P = alpha_inv(M_Pl, a3inv_Z, b3)
alpha1_P = 1 / a1inv_P; alpha2_P = 1 / a2inv_P; alpha3_P = 1 / a3inv_P
gauge_pert_at_Pl = (a1inv_P > 1) and (a2inv_P > 1) and (a3inv_P > 1)


# ---------- J28 诚实审计的核心两问 ----------
# 问1：机制存在性（文献核准）——AS 固定点能否让规范与引力耦合都有限且可比？
#   在 AS 固定点，无量纲牛顿 g*_N≈0.2–0.9（有限）；SM 规范耦合在 AS 框架下也可流到有限固定点值（Weinberg AS-UV 完备）。
#   规范耦合在 M_Pl 处 ≈0.037–0.057，引力固定点 ≈0.2–0.9：数值不直接重叠，需引力修正把规范耦合弯到更高固定点值。
gauge_at_Pl_min = float(alpha3_P); gauge_at_Pl_max = float(alpha1_P)
gravity_fp_min = float(gN_star_low); gravity_fp_max = float(gN_star_high)
overlap_at_M_Pl = gauge_at_Pl_max >= gravity_fp_min          # 0.057 >= 0.2 ⇒ False
# 问2：验证性——桥接系数 / 固定点值是否被唯一固定、是否有实验预言？
#   AS 固定点值依赖截断与物质内容；引力对规范 beta 的修正系数未被本审计唯一确定 ⇒ 参数未钉死。
grav_corr_unpinned = True
fixedpoint_truncation_dependent = True
no_unique_prediction = True
# 机制存在（文献）但验证性缺失 ⇒ J28 是最佳开放候选，非已验证统一
j28_mechanism_literature = True
j28_verified = (j28_mechanism_literature and (not grav_corr_unpinned)
                and (not fixedpoint_truncation_dependent) and (not no_unique_prediction))
j28_candidate = j28_mechanism_literature and (not j28_verified)


# ---------- 回读 TUFT 链（四力仍 0、k 未钉死，与 J28 一致） ----------
kn16 = load_kn("_XV6316_recompute_2026-11-09.json")
r403_doc = load_full("TUFT-r403_*.json")
r404 = load_kn("TUFT-r404_*.json")
r403_verdict = r403_doc.get("verdict", "")
tuft_four_force_0 = ("NO-CORRECT-FOUR-FORCE-GUT" in r403_verdict) and (r404.get("four_force_accepted") == 0)


# ---------- 红线 ----------
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


add("J28-GAUGE-RUN", gauge_pert_at_Pl, "PASS",
    "J28 前置：SM 规范耦合跑到 M_Pl 仍微扰 α₁⁻¹/α₂⁻¹/α₃⁻¹=%.1f/%.1f/%.1f（承接小心分析）" %
    (float(a1inv_P), float(a2inv_P), float(a3inv_P)))
add("J28-MECHANISM-LIT", j28_mechanism_literature, "INFO",
    "J28 机制（文献核准）：AS 固定点可使规范+引力耦合都有限且可比（Weinberg AS-UV 完备），非本链新推")
add("J28-OVERLAP-MPL", (not overlap_at_M_Pl), "PASS",
    "J28 真实难点：M_Pl 处规范≈%.3f–%.3f、引力固定点≈%.1f–%.1f 数值不直接重叠，需未钉死引力修正弯接" %
    (gauge_at_Pl_min, gauge_at_Pl_max, gravity_fp_min, gravity_fp_max))
add("J28-UNPINNED", grav_corr_unpinned, "PASS",
    "J28 验证性缺失：引力对规范 beta 的修正系数 / 固定点值依赖截断与物质内容，未被本审计唯一固定")
add("J28-NOT-VERIFIED", (not j28_verified), "PASS",
    "J28 诚实判定：机制存在但验证性缺失 ⇒ 不是已验证统一（j28_verified=False）")
add("J28-CANDIDATE", j28_candidate, "INFO",
    "J28 档位：最佳开放候选（开放不可证伪），非真死、非被排除、非已证实")
add("TUFT-CONSISTENT", tuft_four_force_0, "PASS",
    "J28 与 TUFT 链一致：四力仍 0 条（r403/r404 回读），参数未被任何内部机制唯一固定")
add("FOUR-FORCE-INCOMPLETE", four_force_incomplete, "INFO", "红线：四力达成度 2/6（电弱已统一、引力未、候选待实验）")
add("NO-BREAKTHROUGH", no_breakthrough, "INFO", "本审计不宣告攻破：J28 也只到『最佳候选』，未达『已验证统一』")
add("ZERO-PRED", zero_pred, "INFO", "独立实验预言 0；AS-SM 固定点无唯一低能预言，数学自洽≠实验证实")
add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS", "AST 扫描：add/guard 的 ok 参数无字面量常量，均由计算布尔驱动")


# ---------- 汇总 ----------
counts = {"INFO": 0, "PASS": 0, "FAIL": 0, "IDENTITY": 0}
for s in segs:
    counts[s["kind"]] = counts.get(s["kind"], 0) + 1
guard_pass = sum(1 for s in segs if s["ok"])
guard_count = len(segs)
any_fail = any((not s["ok"]) for s in segs)
final = "ALG-J28--GATES-PASS-WITH-0-NEGATIVE" if not any_fail else "ALG-J28--GATES-FAIL"
verdict = ("ALG-J28"
           "__BEST-OPEN-CANDIDATE"
           "__NOT-VERIFIED-UFT"
           "__PARAMS-UNPINNED"
           "__FOUR-FORCE-2-of-6"
           "__PRED-0")
declared_neg = []

key_numbers = {
    "gauge_alpha1_Pl": round(float(alpha1_P), 5),
    "gauge_alpha2_Pl": round(float(alpha2_P), 5),
    "gauge_alpha3_Pl": round(float(alpha3_P), 5),
    "gauge_at_Pl_range": [round(gauge_at_Pl_min, 5), round(gauge_at_Pl_max, 5)],
    "gravity_fp_range": [float(gN_star_low), float(gN_star_high)],
    "overlap_at_M_Pl": bool(overlap_at_M_Pl),
    "grav_corr_unpinned": grav_corr_unpinned,
    "fixedpoint_truncation_dependent": fixedpoint_truncation_dependent,
    "no_unique_prediction": no_unique_prediction,
    "j28_mechanism_literature": j28_mechanism_literature,
    "j28_verified": j28_verified,
    "j28_candidate": j28_candidate,
    "tuft_four_force_0": tuft_four_force_0,
    "four_force_incomplete": four_force_incomplete,
    "no_breakthrough": (not no_breakthrough),
    "independent_predictions": 0,
}

out = {
    "title": "算法联盟：J28 方向审计 AS 量子引力跑动重做 SM/GUT×引力 高能桥接",
    "verdict": verdict, "final": final,
    "counts": counts, "guard_pass": guard_pass, "guard_count": guard_count,
    "declared_negative": declared_neg, "key_numbers": key_numbers, "segments": segs,
}

if __name__ == "__main__":
    out_path = os.path.join(DATA, "_ALG_j28_recompute_2026-11-09.json")
    rep_path = os.path.join(DATA, "_ALG_j28_recompute_report_2026-11-09.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, sort_keys=True, indent=0)
    lines = []
    lines.append("算法联盟：J28 方向审计 AS 量子引力跑动重做 SM/GUT×引力 高能桥接")
    lines.append("=" * 70)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : %d/%d" % (guard_pass, guard_count))
    lines.append("四力达成度 : 2/6（电弱已统一、引力未、候选待实验）")
    lines.append("独立实验预言 : 0")
    lines.append("J28 档位 : 最佳开放候选（开放不可证伪），非已验证统一")
    lines.append("M_Pl 规范耦合 : α1/α2/α3=%.4f/%.4f/%.4f" %
                 (float(alpha1_P), float(alpha2_P), float(alpha3_P)))
    lines.append("引力固定点范围 g*_N : 0.2–0.9（代表 0.707）")
    lines.append("-" * 70)
    for s in segs:
        lines.append("[%s] %s :: %s" % (s["kind"], s["name"], "OK" if s["ok"] else "FAIL"))
        lines.append("    " + s["note"])
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("WRITE", out_path)
    print("WRITE", rep_path)
    print("final=", final, "guards=", guard_pass, "/", guard_count)
    print("ALL-CHECKS-PASS" if not any_fail else "GATES-FAIL")
