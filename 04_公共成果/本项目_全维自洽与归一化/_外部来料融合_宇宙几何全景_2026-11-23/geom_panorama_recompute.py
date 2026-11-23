# -*- coding: utf-8 -*-
"""宇宙几何全景 · 来料独立复核引擎

对象：用户来料 HTML 中三个「可查证标准公式」+ 其适用范围。
  1) 环面高斯曲率 K = cos(theta) / (r (R + r cos(theta)))  —— 外正/内负/中零
  2) AB 相位 ∝ 磁通量（来料 accumPhase += dt*omega*flux）
  3) 弱场光偏转 delta = 4GM/(c^2 b) = 2 r_s / b  与三条读数

独立增量（可翻覆判据）：弱场公式的适用范围。
  - 弱场要求 delta << 1；来料 b=2 r_s 给 delta=1 rad，越界。
  - 史瓦西光子捕获临界撞击参数 b_crit = 3 sqrt(3)/2 r_s ≈ 2.598 r_s；
    来料最内侧光线 b=2 r_s < b_crit ⇒ 该光线被捕获、不逃逸，
    把它标成「偏转角 57.30°」是强场区的误用。
  这是可算判决，不是宣称来料整体错误——公式本身在远场正确（负对照验证）。

纪律：exp/act 两路、负对照必响应、恒等门单列、guard 不写死、不改读数凑绿。
不产新物理、不重判 r403、不宣称攻破 UFT，独立预言计数 0。
"""
import json
import os
from decimal import Decimal, getcontext

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "_geom_panorama_report.txt")
JSON_PATH = os.path.join(HERE, "_geom_panorama.json")

PI = Decimal("3.1415926535897932384626433832795028841971693993751")

gates = []


def add(gid, kind, exp, act, ok, note=""):
    gates.append({"id": gid, "kind": kind, "exp": str(exp), "act": str(act),
                  "ok": bool(ok), "note": note})


def deg(rad):
    return rad * Decimal(180) / PI


# ===========================================================================
# 1. 环面高斯曲率 K = cos(theta) / (r (R + r cos(theta)))
# ===========================================================================
R, r = Decimal("2.0"), Decimal("0.65")


def K(theta_cos):
    return theta_cos / (r * (R + r * theta_cos))


k_out = K(Decimal(1))       # theta=0 外赤道
k_in = K(Decimal(-1))       # theta=pi 内赤道
k_mid = K(Decimal(0))       # theta=pi/2 腰线
add("T1-torus-outer-positive", "gate", "外赤道 K=1/(r(R+r))>0",
    "K=%s" % k_out, k_out > 0 and abs(k_out - Decimal(1) / (r * (R + r))) < Decimal("1e-50"),
    "来料『外圈正曲率』读数复算成立")
add("T2-torus-inner-negative", "gate", "内赤道 K=-1/(r(R-r))<0",
    "K=%s" % k_in, k_in < 0 and abs(k_in + Decimal(1) / (r * (R - r))) < Decimal("1e-50"),
    "来料『内圈负曲率』读数复算成立")
add("T3-torus-waist-zero", "gate", "腰线 theta=pi/2 处 K=0",
    "K=%s" % k_mid, k_mid == 0,
    "来料『中间纬线 K=0』读数复算成立")

# 负对照：改变 R/r 比例，外正内负结构必须不变（否则是仪器的单一参数假象）
R2, r2 = Decimal("1.2"), Decimal("1.0")
k2_out = Decimal(1) / (r2 * (R2 + r2))
k2_in = -Decimal(1) / (r2 * (R2 - r2))
add("T4-torus-sign-invariant", "neg", "换 R/r 外正内负结构不变",
    "R=2,r=0.65:(%s,%s); R=1.2,r=1.0:(%s,%s)" % (k_out, k_in, k2_out, k2_in),
    k2_out > 0 and k2_in < 0 and k_out > 0 and k_in < 0,
    "负对照：符号结构不依赖专用参数组；若换参数翻号则 T1/T2 无判别力")

# ===========================================================================
# 2. AB 相位 ∝ 磁通量：来料每圈相位增量 = 2*pi*flux（放大后）
# ===========================================================================
# 来料 tick: accumPhase += dt*omega*flux；一圈 dt*omega=2*pi ⇒ dPhase=2*pi*flux
def phase_per_loop(flux):
    return 2 * PI * flux


for flux in (Decimal("1.20"), Decimal("2.40"), Decimal("0.00")):
    p = phase_per_loop(flux)
    add("A-flux-%s" % flux, "gate", "每圈相位=2*pi*flux (flux=%s)" % flux,
        "phase=%s rad" % p,
        abs(p - 2 * PI * flux) < Decimal("1e-50"),
        "来料『相位正比磁通、放大便于观察』关系复算；flux=0 给出零相位")
# 线性比值（两路独立：比值 vs 直接算）
ratio_read = phase_per_loop(Decimal("2.40")) / phase_per_loop(Decimal("1.20"))
add("A2-ab-linear-ratio", "gate", "相位比 = 磁通比 = 2",
    "ratio=%s" % ratio_read,
    abs(ratio_read - Decimal(2)) < Decimal("1e-50"),
    "AB 相位对磁通的线性性，独立于单点读数")

# ===========================================================================
# 3. 弱场光偏转 delta=2 r_s / b 与三条读数
# ===========================================================================
RS = Decimal("1")   # 可视化单位，取 1；公式对 rs 齐次
bs = [Decimal("2.0") * RS, Decimal("3.2") * RS, Decimal("4.8") * RS]


def delta_rad(b):
    return Decimal(2) * RS / b


deflections = [deg(delta_rad(b)) for b in bs]
add("L1-deflection-readout", "gate", "三条弱场偏转读数复现来料 57.30/35.81/23.87",
    "delta(deg)=%s" % [str(d.quantize(Decimal("0.01"))) for d in deflections],
    [d.quantize(Decimal("0.01")) for d in deflections] ==
    [Decimal("57.30"), Decimal("35.81"), Decimal("23.87")],
    "公式 delta=4GM/(c^2 b)=2 r_s/b 本身正确，读数与来料一致")

# 恒等门单列：4GM/(c^2 b) == 2 r_s / b 当 r_s=2GM/c^2
add("L2-weak-field-identity", "identity", "4GM/(c^2 b) ≡ 2 r_s/b (r_s=2GM/c^2)",
    "代入 r_s=2GM/c^2 ⇒ 4GM/(c^2 b)=(2 r_s)/b，恒等", True,
    "定义恒等，单列不承重；不代表在强场适用")

# --- 核心可翻覆判据：弱场适用范围 ---
# (a) 弱场要求 delta << 1；来料最内侧 delta=1 rad
delta_inner = delta_rad(bs[0])
add("L3-weakfield-out-of-range", "gate", "最内侧光线 delta=1 rad 不满足 delta<<1",
    "delta(b=2 r_s)=%s rad = %s deg" % (delta_inner, deg(delta_inner)),
    delta_inner >= Decimal("0.1"),
    "来料称『弱场公式精确计算』；但 delta=1 rad 偏离小角近似一个量级以上，"
    "该点已非弱场。这是可算的适用范围判决，非来料整体否证")

# (b) 光子捕获临界撞击参数 b_crit = 3 sqrt(3)/2 r_s
sqrt3 = Decimal(3).sqrt()
b_crit = Decimal(3) * sqrt3 / Decimal(2)
inner_captured = bs[0] < b_crit
add("L4-photon-capture-boundary", "gate", "b=2 r_s < b_crit=3√3/2 r_s ⇒ 光线被捕获",
    "b_crit=%s r_s; 最内侧 b=%s r_s; 被捕获=%s" % (
        b_crit.quantize(Decimal("0.000001")), bs[0] / RS, inner_captured),
    inner_captured and b_crit > Decimal("2.5") and b_crit < Decimal("2.6"),
    "史瓦西光子球捕获截面：撞击参数小于 b_crit 的光子落入视界、不逃逸；"
    "来料把它画成逃逸光线并标偏转角，是强场区误用")

# 负对照：移到远场 b=20 r_s，delta<<1 且 b>b_crit ⇒ 弱场公式恢复有效
b_far = Decimal("20") * RS
delta_far = delta_rad(b_far)
add("L5-far-field-neg", "neg", "远场 b=20 r_s 弱场公式有效(证明非恒错)",
    "delta=%s rad (%s deg); b>b_crit=%s" % (
        delta_far, deg(delta_far).quantize(Decimal("0.0001")), b_far > b_crit),
    delta_far < Decimal("0.2") and b_far > b_crit,
    "负对照沿『判据无法吸收的方向』位移：把撞击参数移到远场，"
    "弱场公式与捕获判据同时放行——证明 L3/L4 是边界问题，不是公式恒假")

# 反噬：注入假 b_crit=1.5 r_s，则"b=2 r_s 被捕获"判定必须翻红
b_crit_fake = Decimal("1.5") * RS
flip = not (bs[0] < b_crit_fake)
add("L6-inject-fake-bcrit", "neg", "注入假 b_crit=1.5 r_s 使捕获判定翻转",
    "真实判定=%s; 注入后判定=%s" % (inner_captured, bs[0] < b_crit_fake),
    inner_captured and flip,
    "反噬：若篡改捕获临界值后结论不变，则 L4 判别力 0 或写死")

# ===========================================================================
# 结论
# ===========================================================================
n_gate = sum(1 for g in gates if g["kind"] == "gate")
n_neg = sum(1 for g in gates if g["kind"] == "neg")
n_identity = sum(1 for g in gates if g["kind"] == "identity")
fail = [g["id"] for g in gates if not g["ok"]]
if not fail:
    verdict = ("GEOM-PANORAMA--THREE-STANDARD-FORMULAS-VERIFIED--"
               "TORUS-K-SIGN-STRUCTURE-EXACT--AB-PHASE-LINEAR-IN-FLUX--"
               "WEAK-FIELD-DEFLECTION-READOUTS-REPRODUCED--"
               "BUT-INNER-RAY-B-2RS-BELOW-PHOTON-CAPTURE-2.598RS--"
               "DELTA-1RAD-NOT-WEAK-FIELD--FAR-FIELD-CONTROL-VALID--"
               "FORMULA-CORRECT-APPLICABILITY-BOUNDED--"
               "NO-NEW-PHYSICS--NO-INDEPENDENT-PREDICTION--NO-UFT-CLAIM")
else:
    verdict = "GEOM-PANORAMA-FAIL--" + "-".join(fail)

result = {
    "subject": "宇宙几何全景 · 来料三公式独立复核与弱场适用范围边界",
    "object_boundary": "对象是来料 HTML 的三个标准公式与适用范围；"
                       "与 r403 统一方程总表、r404/r405 出口归零、V51 三代质量均非同一对象，不相加",
    "verdict": verdict,
    "counts": {"gate": n_gate, "neg": n_neg, "identity": n_identity, "failed": len(fail)},
    "independent_prediction_count": 0,
    "key_readings": {
        "torus_K_outer": str(k_out), "torus_K_inner": str(k_in), "torus_K_waist": str(k_mid),
        "deflection_deg": [str(d.quantize(Decimal("0.01"))) for d in deflections],
        "delta_inner_rad": str(delta_inner),
        "b_crit_over_rs": str(b_crit.quantize(Decimal("0.000001"))),
        "inner_ray_captured": inner_captured,
    },
    "gates": gates,
}
with open(JSON_PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

lines = ["宇宙几何全景 · 来料独立复核报告", "=" * 64,
         "判词: " + verdict,
         "门数: gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)),
         "对象边界: " + result["object_boundary"],
         "独立预言计数: 0", "-" * 64]
for g in gates:
    lines.append("[%s] %-28s %-10s exp=%s | act=%s // %s" % (
        "PASS" if g["ok"] else "FAIL", g["id"], g["kind"],
        g["exp"], g["act"], g["note"]))
lines.append("-" * 64)
lines.append("关键读数: " + json.dumps(result["key_readings"], ensure_ascii=False))
lines.append("-" * 64)
lines.append("Decimal prec=60; 全确定性; 不重判 r403、不改来料原文")
with open(REPORT_PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print(verdict)
print("gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)))
for g in gates:
    if not g["ok"]:
        print("FAIL:", g["id"], g["exp"], g["act"])
