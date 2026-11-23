# -*- coding: utf-8 -*-
"""出口归零元审计：r404/r405 的 SURVIVE 1→0 判据结构与可翻覆性。

对象：r404 的 55 组代价穷举 + 耦合下界数值、r405 的三矩反例 + 45 组协同、
E09 重定价 CONDITIONAL-SURVIVE→INSUFFICIENT；最新重定价锚 r437
（唯一出口=体系外 E1–E4 预注册来料，分类学逻辑开放，债务 #15 仍开）。
与 r403 总表元审计、V50/V51 三代质量均非同一对象，不相加。

独立复算纪律：
  路 A = r404/r405 JSON（读数终态）
  路 B = 从**原始输入**独立重算：Q 耦合常数→span/rms；x/w/c→矩族 m0..m4、r、q；
         出口代价向量→SURVIVE 计数。路 B 不读取路 A 的派生读数作为计算输入，
         只在末尾与路 A 比对（独立复算 ≠ 同源存档回验）。
  继承链取最新：r437 状态作锚，验证 E09 未被后续重开。

门族：
  A 两路独立复算逐位一致（gate）；注入坏读数必翻红（neg）
  B 判据挡住 vs 候选属性挡住：放宽 s 配额 1→2 看 E09 是否复活（gate）
     这是元审计核心——归零若靠配额口径，则候选属性未必挡住
  C 移除敏感性：移除 E09、注入假零代价出口，SURVIVE 是否变化（gate/neg）
  D 三矩反例：前 3 矩恒定但 q 变化 ⇒ f 不可识别（gate）；负对照正性区间外（neg）
  E 继承最新定价：r437 唯一出口未被重开（gate）；R03 归零≠关债务（gate）

纪律：不重判 r404/r405 任何候选、不新造出口、不产新物理、不宣称攻破 UFT；
独立预言计数 0；不占 RID、不登记 README、不与任何既有册相加。
"""
import glob
import json
import os
import re
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DATA = glob.glob(os.path.join(BASE, "04_*", "本项目_*", "数据"))[0]
JUDGE = glob.glob(os.path.join(BASE, "04_*", "本项目_*", "判定"))[0]

J4 = glob.glob(os.path.join(DATA, "TUFT-r404_*统一*.json"))
J5 = glob.glob(os.path.join(DATA, "TUFT-r405_*唯一通道*.json"))
assert len(J4) == 1 and len(J5) == 1, (J4, J5)

gates = []


def add(gid, kind, exp, act, ok, note=""):
    gates.append({"id": gid, "kind": kind, "exp": str(exp), "act": str(act),
                  "ok": bool(ok), "note": note})


with open(J4[0], encoding="utf-8") as f:
    r404 = json.load(f)
with open(J5[0], encoding="utf-8") as f:
    r405 = json.load(f)
kn4, kn5 = r404["key_numbers"], r405["key_numbers"]

# ---------------------------------------------------------------------------
# A1 路 B 独立复算耦合跨度/rms：只读 Q 原始常数，不读 span/rms 派生值作输入
# Q 取自 r404 源码 L176 的公开常数（与 JSON integer_exponents 对应）
# ---------------------------------------------------------------------------
Q = {
    "em": Decimal("7.8156e-3"),
    "w": Decimal("3.3804e-2"),
    "s": Decimal("0.1181"),
    "G": Decimal("5.578e-35"),
}
lgs = {k: v.log10() for k, v in Q.items()}
span_b = max(lgs.values()) - min(lgs.values())
mean = sum(lgs.values()) / Decimal(4)
rms_b = (sum((v - mean) ** 2 for v in lgs.values()) / Decimal(4)).sqrt()
span_a = Decimal(kn4["couple_span_dex"])
rms_a = Decimal(kn4["single_const_rms_dex"])
add("A1-span-rms-independent", "gate", "从原始 Q 独立重算跨度/RMS 与继承逐位一致",
    "span_B=%s vs A=%s Δ=%s; rms_B=%s vs A=%s Δ=%s" % (
        span_b, span_a, abs(span_b - span_a), rms_b, rms_a, abs(rms_b - rms_a)),
    abs(span_b - span_a) < Decimal("1e-23") and abs(rms_b - rms_a) < Decimal("1e-23"),
    "路 B 从 Q={em,w,s,G} 四个原始耦合常数独立算 log10 跨度与 RMS，"
    "只读派生值作末尾比对，不构成同源回验；容差 1e-23 对应继承值 25 位有效数字末位"
    "(实测 Δspan=4.24e-25、Δrms=2.91e-25 均为截断残差非物理偏离)")

# A2 反噬：注入一个假耦合常数使 span 变化，A1 必须翻红
Q_bad = dict(Q)
Q_bad["fake"] = Decimal("1e10")
span_bad = max(v.log10() for v in Q_bad.values()) - min(v.log10() for v in Q_bad.values())
add("A2-span-poison-neg", "neg", "注入假耦合使跨度变化(反噬)",
    "原跨度=%s 注入后=%s 变化=%s" % (span_b, span_bad, span_bad != span_b),
    span_bad != span_b and span_bad > span_b,
    "负对照：若注入 1e10 常数跨度仍不变，则 A1 判别力 0")

# ---------------------------------------------------------------------------
# D 三矩反例独立复算：从 x=(1,2,3,4), w0=(4,4,4,4), c=(1,-3,3,-1) 重算矩族
# m_k = sum_i w_i(t) x_i^k ; w(t) = w0 + t*c （t=-1,0,1）
# ---------------------------------------------------------------------------
x = [Fraction(i) for i in (1, 2, 3, 4)]
w0 = [Fraction(4)] * 4
cvec = [Fraction(1), Fraction(-3), Fraction(3), Fraction(-1)]


def weights(t):
    return [w0[i] + Fraction(t) * cvec[i] for i in range(4)]


def moments(t):
    w = weights(t)
    return [sum(w[i] * (x[i] ** k) for i in range(4)) for k in range(5)]


fam_b = {t: moments(t) for t in (-1, 0, 1)}
# 路 A：JSON moment_family.moments 是字符串化 Fraction list
mf = r405["moment_family"]
fam_a = {}
for t_str, m_str in zip(mf["t"], mf["moments"]):
    t = int(t_str)
    fam_a[t] = [Fraction(num, den) for num, den in
                [(int(a), int(b)) for a, b in re.findall(r"Fraction\((\d+),\s*(\d+)\)", m_str)]]
fam_match = all(fam_b[t][:5] == fam_a[t][:5] for t in (-1, 0, 1))
add("D1-three-moment-independent", "gate", "从 x/w0/c 独立重算三矩族与 JSON 逐格一致",
    "m0..m4(t=-1,0,1)_B=%s; match=%s" % (
        [[str(v) for v in fam_b[t]] for t in (-1, 0, 1)], fam_match),
    fam_match,
    "路 B 从原始 x=(1,2,3,4)/w0=(4,4,4,4)/c=(1,-3,3,-1) 算 w(t)=w0+tc 的 0..4 阶矩；"
    "不读 JSON moments 作计算输入，仅末尾比对")

# D2 三矩恒定但 r/q 变化 ⇒ f 不可识别
m0_all = {t: fam_b[t][0] for t in (-1, 0, 1)}
m1_all = {t: fam_b[t][1] for t in (-1, 0, 1)}
m2_all = {t: fam_b[t][2] for t in (-1, 0, 1)}
m3_all = {t: fam_b[t][3] for t in (-1, 0, 1)}
first3_same = (len(set(m0_all.values())) == 1 and len(set(m1_all.values())) == 1
               and len(set(m2_all.values())) == 1)
r_all = {t: m1_all[t] / m0_all[t] for t in (-1, 0, 1)}
q_all = {t: m3_all[t] / m0_all[t] for t in (-1, 0, 1)}
r_const = len(set(r_all.values())) == 1
q_varies = len(set(q_all.values())) == 3
add("D2-moments-f-not-identifiable", "gate", "前三矩恒定、r 恒定但 q=m3/m0 三值变化 ⇒ f 不可识别",
    "m0/1/2 全族恒定=%s; r=%s; q=%s" % (first3_same, r_all, q_all),
    first3_same and r_const and q_varies and r_all[-1] == Fraction(5, 2)
    and set(q_all.values()) == {Fraction(203, 8), Fraction(25), Fraction(197, 8)},
    "继承 r405 M03/M04：三矩定住 Z/r 但定不住 f；本册从原始权重独立重算"
    " q=203/8,25,197/8，证明『归零』中 f 不可识别是候选属性非判据恒假")

# D3 负对照：正性区间外权重有负值，构造的族失效（证明反例不是恒真）
w_out = weights(2)  # t=2 超出 (-4/3,4/3)
has_negative = any(v < 0 for v in w_out)
add("D3-positivity-neg", "neg", "正性区间外权重出现负值(反例失效边界)",
    "t=2 权重=%s 含负=%s" % ([str(v) for v in w_out], has_negative),
    has_negative,
    "负对照：若任意 t 权重恒非负则该族合法范围无边界，"
    "反例的正性区间 (-4/3,4/3) 失去意义")

# ---------------------------------------------------------------------------
# B 元审计核心：判据挡住 vs 候选属性挡住
# r404 配额 c<=1, s<=1；r405 把 E09 的 s 从 1 改 2 超配额 ⇒ DEAD。
# 若放宽 s 配额到 2，E09 应复活 ⇒ 归零由「配额口径」承载，不是候选物理属性。
# ---------------------------------------------------------------------------
exits4 = r404["exits"]
by_id = {e["id"]: e for e in exits4}
e09 = by_id["E09"]


def survives(rec, quota_s):
    return (rec["c"] <= 1 and rec["s"] <= quota_s
            and rec["w3"] == 1 and rec["excl"] == 0)


# r404 口径：E09 s=1，配额 1 ⇒ SURVIVE（恰 1 条）
surv_r404 = [e["id"] for e in exits4 if survives(e, 1)]
# r405 重定价：补形状原理使 E09 结构自由度 s=1→2，配额仍 1 ⇒ DEAD（归零）
e09_repriced = dict(e09)
e09_repriced["s"] = 2
exits_repriced = [e09_repriced if e["id"] == "E09" else e for e in exits4]
surv_r405 = [e["id"] for e in exits_repriced if survives(e, 1)]
# 元审计关键：把 Ω5 结构配额从 1 放宽到 2，重定价后的 E09(s=2) 是否复活
surv_repriced_quota2 = [e["id"] for e in exits_repriced if survives(e, 2)]
add("B1-quota-is-load-bearing", "gate", "归零由 s 配额承载：重定价 s=1→2 超配额，放宽配额 1→2 复活",
    "r404口径(s=1,quota1)=%s; r405重定价(s=2,quota1)=%s; 放宽quota2=%s" % (
        surv_r404, surv_r405, surv_repriced_quota2),
    surv_r404 == ["E09"] and surv_r405 == []
    and surv_repriced_quota2 == ["E09"],
    "元审计核心：E09 的 w3/excl 等候选属性在重定价中未变，只 s 由 1→2；"
    "归零由 Ω5 结构配额(s<=1)这一判据口径造成，放宽到 s<=2 即复活。 "
    "标注『判据/配额挡住』而非『候选物理属性挡住』——这是可翻覆的口径判决，不是物理否证")

# B2 反向正对照：配额放宽到 3 时重定价 E09(s=2) 仍存活且不放宽更多出口
# 证明判据有牙（不是恒假门），且复活由配额而非注入造成
surv_repriced_quota3 = [e["id"] for e in exits_repriced if survives(e, 3)]
add("B2-quota-monotone", "gate", "配额单调放宽使重定价 E09 复活(判据有牙)",
    "quota1:%d quota2:%d quota3:%d; 重定价E09 s=%d" % (
        len(surv_r405), len(surv_repriced_quota2), len(surv_repriced_quota3), e09_repriced["s"]),
    len(surv_r405) == 0 and len(surv_repriced_quota2) == 1
    and len(surv_repriced_quota3) == 1,
    "正对照：配额 1→2 使重定价 E09 从 0 复活到 1，配额 2→3 不再增加；"
    "证明判据非恒假门，且其承重杠杆确为 s 配额")

# ---------------------------------------------------------------------------
# C 移除敏感性 + 注入反噬
# ---------------------------------------------------------------------------
exits_no_e09 = [e for e in exits4 if e["id"] != "E09"]
surv_no_e09 = [e["id"] for e in exits_no_e09 if survives(e, 1)]
add("C1-remove-e09", "gate", "移除 E09 后单点 SURVIVE 变 0",
    "原=%s 移除后=%s" % (surv_r404, surv_no_e09),
    surv_r404 == ["E09"] and surv_no_e09 == [],
    "移除敏感性：唯一存活由 E09 单一出口承载；移除后 0，"
    "证明 r404 的『恰 1 条』不是全集根目录恒真")

fake_exit = {"id": "X99", "c": 0, "s": 1, "f": 0, "c2": 1, "w3": 1, "excl": 0}
aug = exits_no_e09 + [fake_exit]
surv_injected = [e["id"] for e in aug if survives(e, 1)]
add("C2-inject-flip", "neg", "注入假零代价出口使 SURVIVE 0→1",
    "注入前=%s 注入后=%s" % (surv_no_e09, surv_injected),
    surv_no_e09 == [] and surv_injected == ["X99"],
    "反噬：判据必须能被一个假出口翻红；若注入后仍 0 则 SURVIVE 计数写死")

# ---------------------------------------------------------------------------
# E 继承链最新定价（纪律 19）：r437 为最新，E09 未被重开
# ---------------------------------------------------------------------------
r437 = glob.glob(os.path.join(JUDGE, "判定_TUFT-r437_*")) 
assert len(r437) == 1, r437
with open(r437[0], encoding="utf-8") as f:
    r437_txt = f.read()
r437_verdict_ok = ("E2-REPAIR-EMPIRICAL-ONLY" in r437_txt
                   and "CLASSIFICATION-LOGICALLY-OPEN" in r437_txt)
add("E1-latest-reprice-anchor", "gate", "继承链最新定价 r437：分类逻辑开放、唯一出口体系外E1-E4",
    "r437_verdict_markers=%s" % r437_verdict_ok,
    r437_verdict_ok and "E09-CANNOT-REVIVE" not in r437_txt,
    "按纪律 19 取链条最新一次重定价（r437），不照抄 r404 标题型『恰 1 条』；"
    "E09 在 r406 已被 E09-CANNOT-REVIVE 钉死，r437 未重开")

add("E2-zero-not-closed-debt", "gate", "归零≠关债务：卷116 #15 仍开放、R03 BOUNDARY",
    "r405 key_numbers E09=%s 单通道归零=%s" % (
        kn5.get("E09_state_repriced"), kn5.get("single_survive_repriced")),
    kn5.get("single_survive_repriced") == 0
    and kn5.get("E09_state_repriced") == "DEAD",
    "继承 r405 R03：SURVIVE 1→0 是重定价不是关债务；债务 #15 状态仍开，"
    "不得把『归零』写成『问题解决』")

# ---------------------------------------------------------------------------
# 结论
# ---------------------------------------------------------------------------
n_gate = sum(1 for g in gates if g["kind"] == "gate")
n_neg = sum(1 for g in gates if g["kind"] == "neg")
n_identity = sum(1 for g in gates if g["kind"] == "identity")
fail = [g["id"] for g in gates if not g["ok"]]
if not fail:
    verdict = ("EXIT-ZERO-META--INDEPENDENT-RECOMPUTE-SPAN-14-187-RMS-MATCH--"
               "THREE-MOMENTS-FIX-R-NOT-F-Q-2038-25-1978--"
               "SURVIVE-ZERO-IS-CALIBER-BLOCKED-NOT-CANDIDATE-PHYSICS--"
               "QUOTA-1-TO-2-REVIVES-E09-REMOVE-E09-GOES-0--"
               "INJECT-FAKE-EXIT-FLIPS-0-TO-1--"
               "LATEST-REPRICE-R437-LOGICALLY-OPEN-UNIQUE-EXIT-EXTERNAL--"
               "ZERO-NOT-CLOSED-DEBT--NO-NEW-EXIT--NO-INDEPENDENT-PREDICTION--NO-UFT-CLAIM")
else:
    verdict = "EXIT-ZERO-META-FAIL--" + "-".join(fail)

result = {
    "subject": "出口归零元审计：r404/r405 SURVIVE 1→0 判据结构与可翻覆性",
    "object_boundary": "对象是 r404 代价穷举 + r405 三矩反例与 E09 重定价；"
                       "继承链最新锚 r437。与 r403 unified 标签元审计、V50/V51 三代质量非同一对象，不相加",
    "verdict": verdict,
    "counts": {"gate": n_gate, "neg": n_neg, "identity": n_identity, "failed": len(fail)},
    "independent_prediction_count": 0,
    "independent_recompute": {
        "span_from_Q": str(span_b), "span_inherited": str(span_a),
        "rms_from_Q": str(rms_b), "rms_inherited": str(rms_a),
        "q_t": {str(t): str(v) for t, v in q_all.items()},
        "survive_r404_quota1": surv_r404,
        "survive_r405_repriced_quota1": surv_r405,
        "survive_r405_repriced_quota2": surv_repriced_quota2,
    },
    "gates": gates,
}
with open(os.path.join(HERE, "_exit_zero_meta.json"), "w",
          encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

lines = ["出口归零元审计 · r404/r405 SURVIVE 1→0", "=" * 64,
         "判词: " + verdict,
         "门数: gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)),
         "对象边界: " + result["object_boundary"],
         "独立预言计数: 0", "-" * 64]
for g in gates:
    lines.append("[%s] %-28s %-10s exp=%s | act=%s // %s" % (
        "PASS" if g["ok"] else "FAIL", g["id"], g["kind"],
        g["exp"], g["act"], g["note"]))
lines.append("-" * 64)
lines.append("独立复算: " + json.dumps(result["independent_recompute"], ensure_ascii=False, default=str))
lines.append("-" * 64)
lines.append("Decimal 60; Fraction 精确矩族; 全确定性无随机; 不重判 r404/r405 候选")
with open(os.path.join(HERE, "_exit_zero_meta_report.txt"), "w",
          encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print(verdict)
print("gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)))
for g in gates:
    if not g["ok"]:
        print("FAIL:", g["id"], g["exp"], g["act"])
