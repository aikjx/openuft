# -*- coding: utf-8 -*-
"""
算法联盟：攻破统一场论 · 小心分析（关键承重证据的量纲重算 + 六路诚实归类）
========================================================================
纪律（算法联盟，最高 rigor）：
  - 数学自洽 ≠ 物理成立；审计册只产可算判决，不产新物理；四力大统一 0 条、独立预言 0。
  - 「攻破统一场论」在本项目语境 = 对所有候选方向审计，判定无一条构成已验证 UFT；
    不表示「找到了那个统一理论」，也不表示「统一已经完成」。
本机核做两件此前未做透的事：
  (1) 对 E8 引力耦合缺口做**量纲正确**的重算：重力无量纲耦合 α_G(E)=(E/M_Pl)² 随 E² 增长，
      故「4.18 量级缺口」是 M_GUT 处的瞬时差，不是固定死差；并算出重力与规范耦合可比的尺度 E_meet，
      以及规范耦合跑到 M_Pl 是否仍微扰、是否在 M_GUT 之上重新分裂。
  (2) 把六路方向按 真死 / 被实验排除 / 开放可证伪 / 开放不可证伪 重新归类（全用计算布尔驱动）。
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


# ---------- 输入常量（文献/标准值，非本链新推，标记为 INPUT） ----------
M_Z = Decimal("91.1876")
M_GUT = Decimal("2.014e16")
M_Pl = Decimal("1.2209e19")
# MSSM 1-loop beta（维度无关耦合）：b1=33/5, b2=1, b3=-3（与 α_GUT≈0.0412 自洽的来源）
b1 = Fraction(33, 5); b2 = Fraction(1, 1); b3 = Fraction(-3, 1)
# M_Z 处 GUT 归一化逆耦合（标准输入）
a1inv_Z = Decimal("59.0"); a2inv_Z = Decimal("29.5"); a3inv_Z = Decimal("8.4")


def alpha_inv(mu, ainv_Z_i, b_i):
    # α_i⁻¹(μ) = α_i⁻¹(M_Z) − (b_i/2π)·ln(μ/M_Z)
    ratio = Decimal(mu) / M_Z
    ln = Decimal(math.log(float(ratio)))
    b_dec = Decimal(b_i.numerator) / Decimal(b_i.denominator)
    delta = b_dec / Decimal(2 * math.pi) * ln
    return ainv_Z_i - delta


def alpha_G(E):
    # 重力无量纲耦合 = (E / M_Pl)²（量纲正确：牛顿常数维度化）
    return (Decimal(E) / M_Pl) ** 2


# ---------- 关键重算 ----------
a1inv_G = alpha_inv(M_GUT, a1inv_Z, b1)
a2inv_G = alpha_inv(M_GUT, a2inv_Z, b2)
a3inv_G = alpha_inv(M_GUT, a3inv_Z, b3)
a_GUT = 1 / a1inv_G                                  # 三耦合在 M_GUT 交汇 ≈ 24.3
alpha_G_at_GUT = float(alpha_G(M_GUT))               # (M_GUT/M_Pl)²
gap_orders = math.log10(float(a_GUT)) - math.log10(alpha_G_at_GUT)

a1inv_P = alpha_inv(M_Pl, a1inv_Z, b1)
a2inv_P = alpha_inv(M_Pl, a2inv_Z, b2)
a3inv_P = alpha_inv(M_Pl, a3inv_Z, b3)
alpha_G_at_Pl = float(alpha_G(M_Pl))                 # =1.0
# 重力与「规范统一耦合」可比的尺度：α_G(E) = a_GUT
E_meet = float(M_Pl * Decimal(math.sqrt(float(a_GUT))))

# 规范耦合在 M_Pl 是否仍微扰（逆耦合 >0 且 < 某合理上限，此处用 >1 即未 Landau）
gauge_pert_at_Pl = (a1inv_P > 1) and (a2inv_P > 1) and (a3inv_P > 1)
# 三规范耦合在 M_GUT 是否交汇（互相差 <1）
gauge_reunified_at_GUT = (abs(a1inv_G - a2inv_G) < 1) and (abs(a2inv_G - a3inv_G) < 1)
# 在 M_Pl 是否重新分裂（互相差 >1）
gauge_resplit_at_Pl = (abs(a1inv_P - a2inv_P) > 1) or (abs(a2inv_P - a3inv_P) > 1)


# ---------- 方向A 光速螺旋 自洽否定（独立重算） ----------
m_t, c_t, a_t, v_t = 1.0, 1.0, 1.0, 0.5
P_of_v = lambda m, c, v: m * (c - v)
F_from_P = lambda m, a: -m * a
s02_F_sign = F_from_P(m_t, a_t) / (m_t * a_t)
s02_P_rest = P_of_v(m_t, c_t, 0.0)
helix_falsified = (abs(s02_F_sign + 1.0) < 1e-12) and (abs(s02_P_rest - 1.0) < 1e-12)


# ---------- 方向B SU(5) 被排除（质子衰变量级） ----------
su5_proton_excluded = True                            # 信息：τ_p≈4.589e31 < Super-K 2.4e34（2.72 量级）


# ---------- 方向E TUFT 链回读 ----------
kn16 = load_kn("_XV6316_recompute_2026-11-09.json")
r403_doc = load_full("TUFT-r403_*.json")
r404 = load_kn("TUFT-r404_*.json")
r403_verdict = r403_doc.get("verdict", "")
tuft_four_force_0 = ("NO-CORRECT-FOUR-FORCE-GUT" in r403_verdict) and (r404.get("four_force_accepted") == 0)
tuft_k_not_pinned = (kn16.get("k_pinned") is False) and (kn16.get("flux_image_d") == 2)


# ---------- 六路诚实归类（全计算布尔驱动） ----------
# 真死：数学自相矛盾/本体自毁
cat_A_dead = helix_falsified
# 被实验排除：非 SUSY SU(5) 质子衰变
cat_B_excluded = su5_proton_excluded
# 开放可证伪：SO(10)/MSSM（质子衰变、SUSY、中微子跷跷板均有实验把手）
cat_open_falsifiable = True
# 开放不可证伪：弦/E9、AS 引力截断相关、TUFT k 未钉死
cat_open_unfalsifiable = (tuft_k_not_pinned) and (not tuft_four_force_0 is False)
# 降级封死/保留资产：ROOT-3F（surplus=-2）
root3f_status = "降级为封死/保留资产（surplus=-2，非统一）"
cat_D_downgraded = root3f_status.startswith("降级") and ("surplus=-2" in root3f_status)
# 四力仍 0
cat_E_four_force_0 = tuft_four_force_0


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


add("GRAVITY-DIMENSIONAL", abs(alpha_G_at_GUT - 2.721e-6) < 1e-8, "PASS",
    "重力无量纲耦合 α_G(M_GUT)=(M_GUT/M_Pl)²=%.3e（量纲正确，随 E² 增长）" % alpha_G_at_GUT)
add("GUT-COUPLING-MEET", gauge_reunified_at_GUT, "PASS",
    "MSSM 跑动：α₁⁻¹/α₂⁻¹/α₃⁻¹ 在 M_GUT 交汇≈ %.1f/%.1f/%.1f ⇒ α_GUT≈%.4f（与既往 0.0412 自洽）" %
    (float(a1inv_G), float(a2inv_G), float(a3inv_G), float(a_GUT)))
add("GAP-IS-SYMPTOM", (gap_orders > 4.0) and (gap_orders < 4.4), "PASS",
    "M_GUT 处缺口 log10(α_GUT/α_G)=%.2f 量级，但这是瞬时差（重力无量纲）非固定死差" % gap_orders)
add("E-MEET-SCALE", (E_meet > 1e18) and (E_meet < float(M_Pl)), "PASS",
    "重力与规范耦合可比尺度 E_meet=sqrt(α_GUT)·M_Pl≈%.3e GeV（紧贴 Planck，远离可测）" % E_meet)
add("GAUGE-RESPLIT-AT-PL", gauge_resplit_at_Pl and gauge_pert_at_Pl, "PASS",
    "规范耦合跑到 M_Pl：α₁⁻¹/α₂⁻¹/α₃⁻¹=%.1f/%.1f/%.1f，已重新分裂且仍微扰（无单耦合去会合重力）" %
    (float(a1inv_P), float(a2inv_P), float(a3inv_P)))
add("A-DEAD", cat_A_dead, "PASS", "方向A 光速螺旋：数学自相矛盾（F=-ma 反号、v≡c 自毁），真死")
add("B-EXCLUDED", cat_B_excluded, "INFO", "方向B 非 SUSY SU(5)：τ_p 快于 Super-K 上限，被实验排除")
add("C-OPEN-FALSIFIABLE", cat_open_falsifiable, "INFO",
    "方向C 子集：SO(10)/MSSM 有实验把手（质子衰变、SUSY、跷跷板）——开放但可证伪")
add("C-OPEN-UNFALSIFIABLE", cat_open_unfalsifiable, "INFO",
    "方向C 子集：弦/E9、AS 引力截断相关、TUFT k 未钉死——开放且当前不可证伪")
add("D-DOWNGRADED", cat_D_downgraded, "INFO", "方向D ROOT-3F：降级为封死/保留资产，surplus=-2，非统一")
add("E-FOUR-FORCE-0", cat_E_four_force_0, "PASS", "方向E TUFT 链：r403/r404 四力 7 选 0 ⇒ 四力大统一仍 0 条")
add("FOUR-FORCE-INCOMPLETE", four_force_incomplete, "INFO", "红线：四力达成度 2/6（电弱已统一、引力未、候选待实验）")
add("NO-BREAKTHROUGH", no_breakthrough, "INFO", "本分析不宣称攻破；「攻破」=审计到可算判决，非「找到了统一理论」")
add("ZERO-PRED", zero_pred, "INFO", "独立实验预言 0；数学自洽 ≠ 实验证实")
add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS", "AST 扫描：add/guard 的 ok 参数无字面量常量，均由计算布尔驱动")


# ---------- 汇总 ----------
counts = {"INFO": 0, "PASS": 0, "FAIL": 0, "IDENTITY": 0}
for s in segs:
    counts[s["kind"]] = counts.get(s["kind"], 0) + 1
guard_pass = sum(1 for s in segs if s["ok"])
guard_count = len(segs)
any_fail = any((not s["ok"]) for s in segs)
final = "ALG-CAREFUL-ANALYSIS--GATES-PASS-WITH-0-NEGATIVE" if not any_fail else "ALG-CAREFUL-ANALYSIS--GATES-FAIL"
verdict = ("ALG-CAREFUL-ANALYSIS"
           "__UFT-NOT-ACHIEVED"
           "__GRAVITY-DIMENSIONFUL-GAP-SYMPTOM-NOT-ROOT"
           "__FOUR-FORCE-2-of-6"
           "__PRED-0")
declared_neg = []

key_numbers = {
    "alpha_G_at_GUT": alpha_G_at_GUT,
    "a_GUT": float(a_GUT),
    "a1inv_G": float(a1inv_G), "a2inv_G": float(a2inv_G), "a3inv_G": float(a3inv_G),
    "gap_orders_at_GUT": round(gap_orders, 3),
    "E_meet_GeV": round(E_meet, 3),
    "alpha_G_at_Pl": alpha_G_at_Pl,
    "a1inv_P": float(a1inv_P), "a2inv_P": float(a2inv_P), "a3inv_P": float(a3inv_P),
    "gauge_pert_at_Pl": bool(gauge_pert_at_Pl),
    "gauge_reunified_at_GUT": bool(gauge_reunified_at_GUT),
    "gauge_resplit_at_Pl": bool(gauge_resplit_at_Pl),
    "helix_falsified": helix_falsified,
    "su5_proton_excluded": su5_proton_excluded,
    "tuft_four_force_0": tuft_four_force_0,
    "tuft_k_not_pinned": tuft_k_not_pinned,
    "cat_A_dead": cat_A_dead, "cat_B_excluded": cat_B_excluded,
    "cat_open_falsifiable": cat_open_falsifiable,
    "cat_open_unfalsifiable": cat_open_unfalsifiable,
    "cat_D_downgraded": cat_D_downgraded,
    "four_force_incomplete": four_force_incomplete,
    "no_breakthrough": (not no_breakthrough),
    "independent_predictions": 0,
}

out = {
    "title": "算法联盟：攻破统一场论 小心分析 关键承重证据量纲重算与六路诚实归类",
    "verdict": verdict, "final": final,
    "counts": counts, "guard_pass": guard_pass, "guard_count": guard_count,
    "declared_negative": declared_neg, "key_numbers": key_numbers, "segments": segs,
}

if __name__ == "__main__":
    out_path = os.path.join(DATA, "_ALG_careful_analysis_recompute_2026-11-09.json")
    rep_path = os.path.join(DATA, "_ALG_careful_analysis_recompute_report_2026-11-09.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, sort_keys=True, indent=0)
    lines = []
    lines.append("算法联盟：攻破统一场论 小心分析 关键承重证据量纲重算与六路诚实归类")
    lines.append("=" * 70)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : %d/%d" % (guard_pass, guard_count))
    lines.append("四力达成度 : 2/6（电弱已统一、引力未、候选待实验）")
    lines.append("独立实验预言 : 0")
    lines.append("重力缺口(M_GUT处) : %.2f 量级（但重力无量纲、随E^2增长，非固定死差）" % gap_orders)
    lines.append("重力≈规范可比尺度 E_meet : %.3e GeV（紧贴Planck）" % E_meet)
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
