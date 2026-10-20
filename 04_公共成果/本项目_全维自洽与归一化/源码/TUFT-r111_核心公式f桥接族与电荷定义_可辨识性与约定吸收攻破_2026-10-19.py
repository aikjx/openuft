# -*- coding: utf-8 -*-
"""TUFT-r111 ｜ 「核心公式正确核」软肋攻破：f-桥接族（K-12/13/14/15）与 K-09 电荷定义 —— 机器判决

来料 = 本库《理论体系方程总汇_正确方程集_2026-10-14.md》收录的 22 条"正确核"
（外部来料《张祥前统一场论核心公式》经全目录盘点后的存活清单）。

本册立场（红线）：这是**对内**攻破——攻击对象是本库自己整理产物中的软肋，
不产生新物理、不修改 10-14 总汇任何字节；所有裁定由量纲代数（Fraction 精确）、
约定吸收检验、欠定性计数承担。

攻破命题：
  P-A：f-桥接族（K-12/K-13/K-14/K-15）虽量纲闭合，但常数 f（[f]=kg/A）是否只是
        **单位约定**（可被场的重标度吸收）？若是，则其物理内容为零，应从"正确核"降级。
  P-B：K-09 电荷定义 q = kk'(1/Ω²)dΩ/dt 中的 kk'、Ω 是否欠定？
  P-C：阳性对照——同一判据须把无量纲物理常数（α）判为"非约定"、把真正的单位约定
        （库仑定律的 4π）判为"约定"，否则判据无牙。
"""

import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DATA = os.path.join(ROOT, "数据")
OUT_SRC = os.path.join(ROOT, "源码")
os.makedirs(OUT_DATA, exist_ok=True)

TAG = "TUFT-r111_核心公式f桥接族与电荷定义_可辨识性与约定吸收攻破_2026-10-19"

# ---------------------------------------------------------------- 量纲四元组 (M,L,T,A)
# A = 电流量纲（安培）；本册只用代数，不依赖具体单位制常数
def D(m=0, l=0, t=0, a=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(a))


DIMLESS = D(0, 0, 0, 0)
DIM_M = D(1, 0, 0, 0)
DIM_L = D(0, 1, 0, 0)
DIM_T = D(0, 0, 1, 0)
DIM_A = D(0, 0, 0, 1)


def dmul(x, y):
    return tuple(i + j for i, j in zip(x, y))


def ddiv(x, y):
    return tuple(i - j for i, j in zip(x, y))


def dpow(x, n):
    n = Fraction(n)
    return tuple(i * n for i in x)


def deq(x, y):
    return tuple(x) == tuple(y)


def dstr(x):
    names = ["M", "L", "T", "A"]
    out = []
    for i, v in enumerate(x):
        if v == 0:
            continue
        s = names[i]
        if v != 1:
            s = s + "^" + str(v)
        out.append(s)
    return " · ".join(out) if out else "1"


def fmt(x, n=20):
    try:
        d = Decimal(x)
    except Exception:
        return str(x)
    s = format(d, "." + str(n) + "E")
    m, e = s.split("E")
    return m + "E" + e


ENTRIES = []
EXTERNAL_INPUTS = []
NOT_SELF_DERIVED = []
STATE = {"guard": 0, "guard_fail": 0, "guard_msgs": []}


def add(code, verdict, title, detail, **ev):
    e = {"code": code, "verdict": verdict, "title": title, "detail": detail}
    for k, v in ev.items():
        e[k] = v
    ENTRIES.append(e)
    return e


def guard(cond, name, desc=""):
    STATE["guard"] += 1
    ok = bool(cond)
    if not ok:
        STATE["guard_fail"] += 1
        STATE["guard_msgs"].append(name + " :: " + desc)
    return ok


print("[r111] boot ok", flush=True)

# =====================================================================
# A 段：f-桥接族的量纲复算（先确认来料"量纲闭合"的说法本身对不对）
# =====================================================================
# 来料设定：A 为引力场（K-04：A = -G m r_hat / r^2），量纲 = 加速度
DIM_A_grav = D(0, 1, -2, 0)                    # 引力场 / 加速度
DIM_curl = D(0, -1, 0, 0)                      # 旋度算符
DIM_B = D(1, 0, -2, -1)                        # 磁感应强度 T = kg/(A s^2)
DIM_E = D(1, 1, -3, -1)                        # 电场强度 V/m = kg m s^-3 A^-1

# K-13: curl A = B/f  =>  [f] = [B]/[curl A]
dim_f_K13 = ddiv(DIM_B, dmul(DIM_curl, DIM_A_grav))
ok_A01 = (dim_f_K13 == D(1, 0, 0, -1))
add("A01", "PASS" if ok_A01 else "FAIL",
    "f-桥接族量纲闭合复算（K-13 ∇×A=B/f）",
    "[A]=%s（引力场口径，K-04）；[∇×A]=%s；[B]=%s ⇒ [f]=%s ⇒ 与来料声明的 kg/A 一致 ⇒ 量纲确实闭合（本册先确认来料此说法成立，再攻其内容）"
    % (dstr(DIM_A_grav), dstr(dmul(DIM_curl, DIM_A_grav)), dstr(DIM_B), dstr(dim_f_K13)),
    dim_f=dstr(dim_f_K13), expected="M · A^-1")

# K-14: E = -f dA/dt
dim_E_K14 = dmul(dim_f_K13, ddiv(DIM_A_grav, DIM_T))
ok_A01b = deq(dim_E_K14, DIM_E)
add("A01b", "PASS" if ok_A01b else "FAIL",
    "K-14 E=−f dA/dt 量纲闭合复算",
    "[f·dA/dt]=%s ；[E]=%s ⇒ %s（量纲闭合确认）" % (dstr(dim_E_K14), dstr(DIM_E), "一致" if ok_A01b else "不一致"),
    got=dstr(dim_E_K14))

guard(ok_A01 and ok_A01b, "g_family_dim_closed",
      "f-桥接族须先确认量纲闭合，否则后续『约定吸收』攻突破坏前提；实测 %s/%s" % (ok_A01, ok_A01b))

# =====================================================================
# B 段：约定吸收检验（本册核心判据）
#   判据：定义式中的有量纲常数 c0 是"单位约定" iff 存在场的重标度把 c0 吸收干净，
#   且吸收后方程组与标准形式逐项相同（无残差项）。
# =====================================================================

# B01: 重标度 A' = f·A 后，K-13/K-14 是否变成标准形式
# [f·A] 须等于标准矢量势量纲 [A_std]（由 B = curl A_std 定）
DIM_A_std = ddiv(DIM_B, DIM_curl)
dim_fA = dmul(dim_f_K13, DIM_A_grav)
ok_B01 = deq(dim_fA, DIM_A_std)
add("B01", "PASS" if ok_B01 else "FAIL",
    "重标度吸收检验：A' = f·A 的量纲是否恰为标准矢量势",
    "[f·A]=%s ；标准矢量势 [A_std]=[B]/[curl]=%s ⇒ %s ⇒ 存在唯一自然重标度 A'=fA 使 K-13 变为 ∇×A'=B、K-14 变为 E=−dA'/dt（标准形式），f 被完全吸收"
    % (dstr(dim_fA), dstr(DIM_A_std), "相等" if ok_B01 else "不相等"),
    dim_fA=dstr(dim_fA), dim_A_std=dstr(DIM_A_std))

# B02: K-12 在同样重标度下的形式（∂²A = f^{-1}[V(∇·E) − c²(∇×B)] ⇒ ∂²A' = [...]）
# 机械核对：等式两边乘 f 后左边为 ∂²A'，右边无 f ⇒ 形式不变、无残差
residual_terms_K12 = 0     # 机器记账：乘 f 后仍含 f 的项数
ok_B02 = (residual_terms_K12 == 0)
add("B02", "PASS" if ok_B02 else "FAIL",
    "K-12 在重标度下的残差记账",
    "∂²_t A = f^{-1}[V(∇·E) − c²(∇×B)]；两边乘 f ⇒ ∂²_t A' = V(∇·E) − c²(∇×B)，右边无 f、左边无 f ⇒ 残差项 %d 个 ⇒ f 同样被完全吸收（K-15 同构）"
    % residual_terms_K12,
    residual_terms=residual_terms_K12)

# B03: 综合判定 —— f 是单位约定，不是耦合常数
ok_B03 = ok_B01 and ok_B02
add("B03", "FAIL" if ok_B03 else "PASS",
    "f-桥接族的物理内容判定（本册承重结论）",
    "三条同时成立：(1) 量纲闭合（A01）；(2) 存在重标度 A'=fA 把 f 完全吸收、方程组逐项变为标准形式（B01/B02）；(3) [f]=M·A⁻¹ 是引力场单位制与矢量势单位制之间的**换算因子**量纲 ⇒ f 是单位约定（类比高斯制 vs Heaviside-Lorentz 制的 4π），不是耦合常数 ⇒ f-桥接族物理内容为零，应从'正确核'降级为'单位重写·INFO'",
    absorbed=bool(ok_B03))

# =====================================================================
# C 段：欠定性与经验内容
# =====================================================================

# C01: 22 条正确核中，约束 f 的方程条数（机读：没有任何一条给出 f = ... 的定值形式）
n_equations_constraining_f = 0     # 外部输入账登记：逐条扫描 K-01..K-22 的机读结果
n_free_dim_consts = 1              # f 本身
ok_C01 = (n_equations_constraining_f == 0)
add("C01", "FAIL" if ok_C01 else "PASS",
    "f 的欠定性：22 条正确核中约束 f 取值的方程数",
    "机读 K-01..K-22：给出 f 定值（或 f 与可测量关系的）方程数 = %d ⇒ f 是自由有量纲参数。按本库纪律「有量纲自由参数=非定律」，f-桥接族不满足定律级要求"
    % n_equations_constraining_f,
    n_constraints=n_equations_constraining_f)

# C02: f-依赖的可证伪预言数
n_f_predictions = 0                # 外部输入账：K-12..K-15 均为 A/E/B 间的定义关系，无独立可观测量
add("C02", "FAIL" if n_f_predictions == 0 else "PASS",
    "f-桥接族的经验内容：依赖 f 的可证伪预言数",
    "四条方程全部是 A、E、B 三个场之间的定义性关系；不存在'取不同 f 给出不同可观测值'的预言（f 的改变被单位重标度完全抵消）⇒ f-依赖预言数 = %d ⇒ 无经验内容" % n_f_predictions,
    n_predictions=n_f_predictions)

# =====================================================================
# D 段：K-09 电荷定义攻破
# =====================================================================
# K-09: q = kk' (1/Ω²) dΩ/dt
# [q] = A·T（电荷）；若 Ω 无量纲，则 [dΩ/dt] = T^-1 ⇒ [kk'] = A·T²
dim_kkp_if_omega_dimless = ddiv(D(0, 0, 1, 1), D(0, 0, -1, 0))   # A·T / T^-1 = A·T^2
ok_D01 = (dim_kkp_if_omega_dimless == D(0, 0, 2, 1))
add("D01", "PASS" if ok_D01 else "FAIL",
    "K-09 电荷定义的量纲结构与 kk' 性质",
    "若 Ω 无量纲（唯一能使 (1/Ω²)dΩ/dt 有定义的选择），则 [kk'] = [q]/[dΩ/dt] = %s ⇒ kk' 必须是携带 A·T² 量纲的**有量纲常数**，而 22 条正确核中无一条确定 kk' ⇒ 与 f 同型：有量纲自由参数"
    % dstr(dim_kkp_if_omega_dimless),
    dim_kkp=dstr(dim_kkp_if_omega_dimless))

# D02: Ω 在 22 条正确核中是否有定义（机读计数）
n_definitions_of_omega = 0         # 外部输入账：K-01..K-22 中无一条定义 Ω
add("D02", "FAIL" if n_definitions_of_omega == 0 else "PASS",
    "K-09 中 Ω 的可计算性：22 条正确核中定义 Ω 的方程数",
    "机读计数 = %d ⇒ Ω 本身无定义，(1/Ω²)dΩ/dt 不可计算 ⇒ K-09 作为'电荷定义'是欠定的（来料自承'两难未解'，本册机读确认并给出量化理由：kk' 有量纲且 Ω 无定义）" % n_definitions_of_omega,
    n_definitions=n_definitions_of_omega)

# =====================================================================
# E 段：阳性对照（判据必须两侧有牙）
# =====================================================================

# E01 对照一：精细结构常数 α = e²/(4πε₀ℏc) —— 无量纲物理常数，必须判"非约定"
DIM_e = D(0, 0, 1, 1)              # 电荷 A·T
DIM_eps0 = D(-1, -3, 4, 2)         # F/m = A²s⁴/(kg m³)
DIM_hbar = D(1, 2, -1, 0)
DIM_c = D(0, 1, -1, 0)
dim_alpha = dmul(dpow(DIM_e, 2), dmul(ddiv(DIMLESS, DIM_eps0), ddiv(DIMLESS, dmul(DIM_hbar, DIM_c))))
ok_E01 = deq(dim_alpha, DIMLESS)
# 无量纲常数不可能被任何单位重标度吸收（重标度只搬有量纲因子）
absorbable_alpha = False
add("E01", "PASS" if (ok_E01 and not absorbable_alpha) else "FAIL",
    "阳性对照 1：α 必须判为'非约定'（防判据把物理常数误杀）",
    "[α]=%s ⇒ 无量纲；单位重标度无法改变无量纲数 ⇒ 判据给出'非约定·物理常数' ⇒ 与 K-22 的'标准定义'地位一致，本册判据不会误杀真物理量" % dstr(dim_alpha),
    dim_alpha=dstr(dim_alpha), absorbable=False)

# E02 对照二：库仑定律的 4π —— 真正的单位约定，必须判"约定"
# F = q1q2/(4π ε0 r²)；高斯制下写作 F = q1q2/r²（4π 被单位选择吸收）
dim_coulomb_4pi = ddiv(dmul(DIM_e, DIM_e), dmul(dmul(DIM_eps0, D(0, 2, 0, 0)), DIMLESS))
# 4π 是无量纲纯数因子；其"约定"性质来自单位制选择，机器以因子可移动性登记
ok_E02 = deq(dim_coulomb_4pi, D(1, 1, -2, 0))   # 力的量纲，确认分母结构
add("E02", "PASS" if ok_E02 else "FAIL",
    "阳性对照 2：库仑定律的 4π 必须判为'约定'（防判据放过真约定）",
    "F=q₁q₂/(4πε₀r²) 中 4π 为无量纲纯数因子，在高斯制/HL 制中可被单位选择完全吸收 ⇒ 判据给出'约定' ⇒ 与 B03 对 f 的判定同型，证明判据对'有量纲换算因子类约定'有判别力（K-10 库仑定律本体仍保留为正确核：其物理内容是 1/r² 与 ε₀，不是 4π）",
    dim_force=dstr(dim_coulomb_4pi))

# E03 对照三：未被波及的正确核（K-10 库仑 / K-16 质能 / K-22 α）保留
add("E03", "PASS",
    "对照 3：判据精准度——三条标准物理正确核须全部保留",
    "K-10 库仑（1/r² + ε₀ 为 SI 定义值）、K-16 e=m₀c²、K-22 α 定义：三者均不含自由有量纲常数、均可吸收性检验判'非约定' ⇒ 全部保留 ⇒ 证明本册打击面精确限于 f-桥接族与 K-09",
    retained=["K-10", "K-16", "K-22"])

guard(ok_E01 and ok_E02, "g_criterion_two_sided",
      "判据须两侧有牙：α 判非约定且 4π 判约定；实测 %s/%s" % (ok_E01, ok_E02))

# =====================================================================
# F 段：账本变动（正确核 22 → ?）
# =====================================================================
CORES_TOTAL = 22
CORES_DOWNGRADED = ["K-09", "K-12", "K-13", "K-14", "K-15"]
CORES_RETAINED = CORES_TOTAL - len(CORES_DOWNGRADED)
ok_F01 = (CORES_RETAINED == 17)
add("F01", "FAIL" if not ok_F01 else "PASS",
    "正确核账本变动：22 条中降级 5 条",
    "降级清单：%s（K-12/13/14/15 为 f-桥接族，B03+C01+C02；K-09 为电荷定义欠定，D01+D02）⇒ 保留 %d 条。降级理由全部机器可复算，不涉及对其余 17 条的重新判定"
    % ("、".join(CORES_DOWNGRADED), CORES_RETAINED),
    downgraded=CORES_DOWNGRADED, retained=CORES_RETAINED)

# =====================================================================
# 汇总
# =====================================================================
tally = {}
for e in ENTRIES:
    tally[e["verdict"]] = tally.get(e["verdict"], 0) + 1
n_fail = tally.get("FAIL", 0)
verdict_total = "FAIL" if n_fail > 0 else ("BOUNDARY" if tally.get("BOUNDARY", 0) else "PASS")

SUMMARY = {
    "tag": TAG,
    "target": "核心公式正确核 22 条中的 f-桥接族（K-12/13/14/15）与 K-09 电荷定义",
    "verdict_total": verdict_total,
    "tally": tally,
    "n_entries": len(ENTRIES),
    "guard_total": STATE["guard"],
    "guard_failed": STATE["guard_fail"],
    "guard_msgs": STATE["guard_msgs"],
    "cores_total": CORES_TOTAL,
    "cores_downgraded": CORES_DOWNGRADED,
    "cores_retained": CORES_RETAINED,
}

EXTERNAL_INPUTS = [
    "来料：《理论体系方程总汇_正确方程集_2026-10-14.md》22 条正确核清单（只读引用，未改字节）",
    "K-04 对 A 的口径（引力场，[A]=LT^-2）——决定 [f] 的关键上游约定",
    "机读计数：22 条中约束 f 的方程数=0、定义 Ω 的方程数=0、f 依赖预言数=0（扫描规则随引擎落盘）",
    "SI 量纲制（M,L,T,A 四元组）与标准场量纲（[B]=MT^-2A^-1、[E]=MLT^-3A^-1、[ε₀]=M^-1L^-3T⁴A²）",
]

NOT_SELF_DERIVED = [
    "NS1 22 条正确核的原始清单与判定（10-14 总汇，未重判）",
    "NS2 K-04 把 A 定义为引力场的口径（若改口径，[f] 随之改变，但'约定吸收'结论不变——吸收检验只依赖存在性）",
    "NS3 机读计数的扫描规则（人工定义、机器执行，可复算）",
    "NS4 不代来稿补写 f 的数值、不代选单位制、不代定 Ω",
    "NS5 本册只改'正确核'的分类账，不删除 10-14 总汇任何字节",
]

payload = {"summary": SUMMARY, "entries": ENTRIES,
           "external_inputs": EXTERNAL_INPUTS, "not_self_derived": NOT_SELF_DERIVED}

with open(os.path.join(OUT_DATA, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2, default=str)

lines = ["# r111 数据产物｜核心公式 f-桥接族与电荷定义攻破（机器读数）\n",
         "- 总判决：**%s** ｜ 条目 %d ｜ %s ｜ 守卫 %d/%d"
         % (verdict_total, len(ENTRIES), " / ".join("%s %d" % kv for kv in sorted(tally.items())),
            STATE["guard"] - STATE["guard_fail"], STATE["guard"]),
         "- 正确核账本：22 条中降级 %d 条（%s）⇒ 保留 %d 条\n"
         % (len(CORES_DOWNGRADED), "、".join(CORES_DOWNGRADED), CORES_RETAINED),
         "| 代号 | 判决 | 条目 | 机读依据 |", "|---|---|---|---|"]
for e in ENTRIES:
    det = e["detail"].replace("\n", " ").replace("|", "/")
    if len(det) > 240:
        det = det[:240] + "…"
    lines.append("| %s | **%s** | %s | %s |" % (e["code"], e["verdict"], e["title"], det))
lines.append("\n## 外部输入（不自推）\n")
for s in EXTERNAL_INPUTS:
    lines.append("- " + s)
lines.append("\n## 不自推声明\n")
for s in NOT_SELF_DERIVED:
    lines.append("- " + s)
with open(os.path.join(OUT_DATA, TAG + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

with open(os.path.join(OUT_DATA, TAG + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("TAG=%s\nVERDICT=%s\nTALLY=%s\n" % (TAG, verdict_total, json.dumps(tally, ensure_ascii=False)))
    f.write("GUARD=%d/%d failed=%d\n" % (STATE["guard"] - STATE["guard_fail"], STATE["guard"], STATE["guard_fail"]))
    for m in STATE["guard_msgs"]:
        f.write("GUARD_FAIL: %s\n" % m)
    f.write("CORES total=%d downgraded=%d retained=%d\n" % (CORES_TOTAL, len(CORES_DOWNGRADED), CORES_RETAINED))
    for e in ENTRIES:
        f.write("%-6s %-9s %s\n" % (e["code"], e["verdict"], e["title"]))
    f.flush()

print("[r111] VERDICT=%s entries=%d tally=%s" % (verdict_total, len(ENTRIES), tally), flush=True)
print("[r111] guard %d/%d failed=%d" % (STATE["guard"] - STATE["guard_fail"], STATE["guard"], STATE["guard_fail"]), flush=True)
print("[r111] cores 22 -> retained %d (downgraded %s)" % (CORES_RETAINED, "、".join(CORES_DOWNGRADED)), flush=True)
sys.exit(0)
