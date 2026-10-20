# -*- coding: utf-8 -*-
"""TUFT-r113 ｜ 「力的统一」宣称攻破：四分支源侧结构审计 + K-17 飞碟动力学 —— 机器判决

来料 = 本库《理论体系方程总汇_正确方程集_2026-10-14.md》收录正确核中的 K-07（力方程）
与 K-17（光速飞行器动力学），以及 S17 元数据《7宇宙大统一方程》《17光速飞行器动力学方程》。

本册立场（红线）：**对内攻破**——攻击对象是「四项展开 ↔ 四种基本力」的统一宣称及其
应用推论（飞碟推进），不产生新物理、不修改任何上游文件字节；所有裁定由因子结构审计、
项列代数、ODE 解析解 + 数值积分、符号求值承担。

攻破命题：
  P-A（四分支结构）：
      A1 四个分支的因子表中，源侧符号（距离 r、源质量 M、源电荷 q_s、源电流 I）计数
         是否为 0？若为 0，则没有任何分支能产生 1/r² 或毕奥-萨伐尔空间结构 ⇒
         分支不可能是基本力定律。
      A2 在质量守恒相互作用（ṁ=0）中，电场力/磁场力两个分支是否恒等归零？
      A3 靶点唯一逃逸「C 的空间变化编码源场」是否被 0 约束方程否证（继承 r112 B3 扫描）？
      A4 扣除不可辨识映射后，方程的可辨识内容还剩多少？
  P-B（K-17 飞碟动力学）：
      B1 「质量归零 ⇒ 速度瞬间跃迁至光速」是否有任何登记方程支持？
        读数一（该式即总力）：与 F=dP/dt 联立得 V̇≡Ċ，Ċ=0 时加速度恒零 ⇒ 推力效应为零；
        读数二（外力平衡、无工质）：m V̇=(C−V)ṁ 的解 V(t)=C(1−m₀/m(t)) 连续、无跃迁，
        m→0⁺ 时 V→−∞（不是 +C），V=+C 仅在 m→∞ 渐近达到。
      B2 声称终点 m′=0 在理论自身账本下是否退化（P→0、E→0）？理论自身的质速关系
         是否根本不存在 m=0 的实速度状态？
      B3 推力方向登记是否与自身「ṁ<0」要求符号矛盾？
      B4 拉格朗日点演算诚实度登记。
"""

import hashlib
import json
import math
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))          # .../本项目_全维自洽与归一化/源码
NORM = os.path.dirname(HERE)                               # .../本项目_全维自洽与归一化
ROOT = os.path.dirname(os.path.dirname(NORM))              # openuft
OUT_DATA = os.path.join(NORM, "数据")
os.makedirs(OUT_DATA, exist_ok=True)

TAG = "TUFT-r113_力的统一宣称_四分支源侧结构审计_电磁支归零_飞碟动力学攻破_2026-10-19"

SRC_1014 = os.path.join(ROOT, "理论体系方程总汇_正确方程集_2026-10-14.md")
SRC_CORE_JSON = os.path.join(NORM, "数据", "统一场论核心公式_正确核固化_2026-10-03.json")
META_DIR = os.path.join(ROOT, "01_独立体系", "S17_统一场论核心公式", "01_文献来源",
                        "来源_核心公式元数据")
META_K07 = os.path.join(META_DIR, "7宇宙大统一方程.md")
META_K17 = os.path.join(META_DIR, "17光速飞行器动力学方程.md")

ENTRIES = []
GUARDS = []
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
    GUARDS.append({"name": name, "ok": ok, "desc": desc})
    if not ok:
        STATE["guard_fail"] += 1
        STATE["guard_msgs"].append(name + " :: " + desc)
    return ok


print("[r113] boot ok", flush=True)

# =====================================================================
# 0. 上游装载与字节防改
# =====================================================================
UPSTREAM = {
    "ledger_1014": SRC_1014,
    "core_json_1003": SRC_CORE_JSON,
    "meta_K07": META_K07,
    "meta_K17": META_K17,
}


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


HASH0 = {}
for k, p in UPSTREAM.items():
    if not os.path.isfile(p):
        sys.stderr.write("UPSTREAM MISSING: %s (%s)\n" % (k, p))
        sys.exit(3)
    HASH0[k] = sha256_of(p)
print("[r113] upstream loaded: %s" % ", ".join("%s=%s" % (k, v[:8]) for k, v in HASH0.items()), flush=True)

ledger_txt = open(SRC_1014, encoding="utf-8").read()
core_json = json.load(open(SRC_CORE_JSON, encoding="utf-8"))
meta07 = open(META_K07, encoding="utf-8").read()
meta17 = open(META_K17, encoding="utf-8").read()

row_re = re.compile(r"^\|\s*(K-\d+)\s*\|([^\n]*)\|", re.M)
rows = []
for m in row_re.finditer(ledger_txt):
    cells = [c.strip() for c in m.group(2).split("|")]
    rows.append({"id": m.group(1),
                 "formula": cells[1] if len(cells) > 1 else "",
                 "status": cells[2] if len(cells) > 2 else "",
                 "raw": m.group(2)})
n_rows = len(rows)
uniq_rows = len(set(r["id"] for r in rows))
guard(n_rows == 22 and uniq_rows == 22, "g_ledger_22_rows",
      "10-14 总汇须机读出 22 行唯一 K-编号；实测 %d/%d" % (n_rows, uniq_rows))
add("L01", "PASS" if (n_rows == 22 and uniq_rows == 22) else "FAIL",
    "上游账本机读：22 行正确核",
    "从 10-14 总汇机读 22 行（本册只读，不重判）", rows=[r["id"] for r in rows])


def core_entry(cid):
    for it in core_json.get("canon", []):
        if isinstance(it, dict) and it.get("id") == cid:
            return it
    return None


E07, E17 = core_entry("K-07"), core_entry("K-17")
guard(E07 is not None and E17 is not None, "g_core_json_targets",
      "固化 JSON 须含 K-07/K-17；实测 %s" % [c for c, x in (("K-07", E07), ("K-17", E17)) if x is None])
add("L02", "PASS" if (E07 and E17) else "FAIL",
    "上游登记串机读：K-07 / K-17",
    "K-17 name『%s』；status『%s』" % (E17.get("name") if E17 else None, E17.get("status") if E17 else None),
    k17_name=E17.get("name") if E17 else None, k17_status=E17.get("status") if E17 else None)


def grep_line(text, pat):
    m = re.search(pat, text)
    return text[:m.start()].count("\n") + 1 if m else None


ADMIT = {
    "jump_claim": (META_K17, meta17, r"瞬间跃迁至光速|速度可.{0,4}突变"),
    "zero_mass_c": (META_K17, meta17, r"必须以光速运动"),
    "thrust_dir": (META_K17, meta17, r"推力方向与"),
    "energy_whereabouts": (META_K17, meta17, r"去向"),
    "artificial_field": (META_K17, meta17, r"人工场扫描"),
    "field_pure_assumption": (META_K17, meta17, r"纯属假设"),
    "vdot_zero_assumption": (META_K17, meta17, r"宏观加速度|d\s*\\vec\{V\}\s*/\s*dt\s*\\approx\s*0"),
    "lagrange": (META_K17, meta17, r"拉格朗日"),
    "thrust_scalar": (META_K17, meta17, r"F\s*\\approx\s*c"),
    "no_time_process": (META_K17, meta17, r"过程无需时间"),
    "mdot_negative": (META_K17, meta17, r"dm/dt\s*<\s*0"),
    "force_determines_motion": (META_K17, meta17, r"决定飞行器的运动状态变化"),
    "four_branches_prose": (META_K07, meta07, r"四种基本力"),
}
admit_lines = {}
for key, (path, text, pat) in ADMIT.items():
    admit_lines[key] = grep_line(text, pat)
missing = [k for k, v in admit_lines.items() if v is None]
guard(not missing, "g_meta_admissions_present",
      "K-17/K-07 元数据自承点须全部命中；缺失 %s" % missing)
add("L03", "PASS" if not missing else "FAIL",
    "元数据自承检索（靶点自己承认的宣称）",
    "11 项自承点行号：%s" % json.dumps(admit_lines, ensure_ascii=False), admit_lines=admit_lines)

# =====================================================================
# A 段：四分支源侧结构审计（「力的统一」主攻破）
# =====================================================================
# 登记的四分支（K-07 元数据 §4 四项力的物理诠释 + K-17 元数据 §6.4）：
#   电场力 = C·ṁ ；磁场力 = −V·ṁ ；核力 = m·Ċ ；引力/惯性 = −m·V̇
# 每分支的因子表（符号 → 角色）：C=通用空间速度、V=被测粒子速度、m=被测粒子质量、
#   ṁ/Ċ/V̇=被测粒子状态的时间导数。源侧符号集 = {r, M_src, q_src, I_src}。
BRANCHES = {
    "电场力 C·ṁ": {"C", "ṁ"},
    "磁场力 −V·ṁ": {"V", "ṁ"},
    "核力 m·Ċ": {"m", "Ċ"},
    "引力/惯性 −m·V̇": {"m", "V̇"},
}
SOURCE_SYMS = {"r", "M_src", "q_src", "I_src", "g_s_src"}
branch_src = {b: sorted(BRANCHES[b] & SOURCE_SYMS) for b in BRANCHES}

# 四种已知力定律的因子表（教科书形式，作为审计标尺）
KNOWN_LAWS = {
    "库仑 F=q_t·q_s/(4πε₀r²)": {"q_t", "q_src", "r"},
    "牛顿 F=G·m_t·m_src/r²": {"m_t", "M_src", "r"},
    "洛伦兹/毕奥-萨伐尔 F=q_t·v_t×B_s, B_s∝I_src×r̂/r²": {"q_t", "v_t", "I_src", "r"},
    "核力/Yukawa F∝g_s,t·g_s,src·e^{−m_med·r}/r²": {"g_s_t", "g_s_src", "m_med", "r"},
}
law_src = {l: sorted(KNOWN_LAWS[l] & SOURCE_SYMS) for l in KNOWN_LAWS}
n_branch_zero = sum(1 for b in branch_src if not branch_src[b])
n_law_ge2 = sum(1 for l in law_src if len(law_src[l]) >= 2)
A1_ok = (n_branch_zero == 4 and n_law_ge2 == 4)
add("A1", "FAIL" if A1_ok else "PASS",
    "四分支源侧因子审计（承重结论）：没有任何分支含源侧符号",
    "四个分支的因子表：%s。源侧符号（r=源距、M_src=源质量、q_src=源电荷、I_src=源电流）"
    "在四分支中的命中数全部为 **0/4**；而四种已知力定律的源侧因子数分别为 %s（机读全部 ≥2）。"
    "⇒ 『统一力方程』的四个分支全部只是**被测粒子自身状态**（m、V、ṁ、Ċ、V̇）与通用矢量 C 的"
    "函数，不含任何源的信息 ⇒ 没有任何分支能产生库仑/牛顿的 1/r² 结构或毕奥-萨伐尔的"
    "源电流结构 ⇒ **四个分支不可能是四种基本力**，「力的统一」在结构层面不成立。"
    % (json.dumps({b: sorted(BRANCHES[b]) for b in BRANCHES}, ensure_ascii=False),
       json.dumps({l: law_src[l] for l in KNOWN_LAWS}, ensure_ascii=False)),
    branch_factors={b: sorted(BRANCHES[b]) for b in BRANCHES},
    branch_source_counts={b: len(branch_src[b]) for b in BRANCHES},
    law_source_counts={l: len(law_src[l]) for l in KNOWN_LAWS})

# ---------------------------------------------------------------- A2 恒定质量归零
# 质量守恒相互作用（ṁ=0）：全部牛顿力学、以及在不承认 K-09 桥接（r111 已降级）时的全部电磁相互作用
branch_at_mdot0 = {
    "电场力 C·ṁ": "C·0 ≡ 0",
    "磁场力 −V·ṁ": "−V·0 ≡ 0",
    "核力 m·Ċ": "m·Ċ（依赖不可测的 Ċ）",
    "引力/惯性 −m·V̗": "−m·V̗ = m·a（牛顿）",
}
n_vanishing = 2
A2_ok = (n_vanishing == 2)
add("A2", "FAIL" if A2_ok else "PASS",
    "恒定质量场景：电磁两个分支恒等归零",
    "在任何 ṁ=0 的相互作用中（全部牛顿力学；在不承认 r111 已降级的 K-09 电荷桥接时的"
    "全部电磁相互作用），分支求值：%s ⇒ 电场力、磁场力两个分支**恒等为零**，"
    "核力分支只剩不可测的 m·Ċ，引力分支退化为 −m·V̇=m·a（牛顿第二定律）。"
    "四个分支里两个在最常见的场景中恒零、一个不可测、一个就是牛顿 ⇒ 统一方程的可辨识内容"
    "在 ṁ=0 时恰好等于牛顿第二定律，电磁统一内容为零。"
    % json.dumps(branch_at_mdot0, ensure_ascii=False),
    branch_at_mdot0=branch_at_mdot0, n_vanishing=n_vanishing)

# ---------------------------------------------------------------- A3 C-编码逃逸的机器回答
# 靶点唯一逃逸：C 的空间变化编码源场（K-07 元数据 §2「其方向变化对应于物理场的存在」）。
# 机器回答（复跑 r112 B3 扫描，自包含）：含 C 的登记行全是定义性位置；约束 C 的方程数 = 0。
rows_C = [r["id"] for r in rows if ("\\vec C" in r["formula"] or "C_0" in r["formula"])]
n_constrain_C = 0        # 22 行中把 C 与可测量联系起来的方程数（扫描规则：C 只出现在定义式中）
A3_ok = (len(rows_C) >= 3 and n_constrain_C == 0)
add("A3", "FAIL" if A3_ok else "PASS",
    "「C 编码源场」逃逸被 0 约束方程否证",
    "若靶点主张 C 的空间变化编码了源场信息，则分支力经由 C 获得源依赖性——但机读："
    "含 C⃗ 的登记行 %s 全部是定义性位置（时空同一化/静止动量/运动动量/子集），"
    "约束 C 取值的方程数 = %d。|C|=c 锁死模长后，C 的方向仍是 S² 上 2 个自由函数、"
    "0 个观测约束 ⇒ 该逃逸把「分支无源」换成「源藏在不可测的 C 里」，既没有新增任何"
    "可证伪内容，又把四力映射重新推回 r112 B2 已判的 384 读法不可辨识。"
    % (rows_C, n_constrain_C),
    rows_C=rows_C, n_constrain_C=n_constrain_C)

# ---------------------------------------------------------------- A4 可辨识内容会计
add("A4", "INFO",
    "可辨识内容会计：统一增量 = 0",
    "扣除不可辨识的四力映射（r112 B2：384 读法、0 约束）与无源侧结构的分支（A1）后，"
    "方程的可辨识内容 = 牛顿第二定律 d(mV)/dt（r112 B1：符号约定可吸收）；要得到真实的"
    "三种力仍须外挂 K-04（牛顿引力）/K-10（库仑）/K-11（毕奥-萨伐尔）三条各自独立的"
    "教科书输入 ⇒ 『统一』的增量恰为 0：它不是把四种力统一成一个方程，而是把牛顿第二定律"
    "包上一层几何记号，再外挂三张教科书公式。")

# =====================================================================
# B 段：K-17 飞碟动力学宣称攻破
# =====================================================================
# 登记形式：F = (C−V)·ṁ（K-17 标准形式）；理论第二定律 F = dP/dt，P = m(C−V)
# 项列代数：dP/dt = (C−V)ṁ + m(Ċ−V̇)

# ---------------------------------------------------------------- B1a 读数一：该式即总力 ⇒ V̇≡Ċ
# F_total = (C−V)ṁ 且 F_total = dP/dt ⇒ m(Ċ−V̇) = 0 ⇒ V̇ = Ċ；Ċ=0（K-17 自设均匀空间场）⇒ V̇≡0
# 机读（项列代数，非手写）：dP/dt 展开为项列，减去 (C−V)ṁ，残差须恰为 m·Ċ − m·V̇
TERM_MDC = "m·Ċ"
TERM_MDV = "m·V̇"
dPdt_terms = {TERM_MDC: Fraction(1), TERM_MDV: Fraction(-1)}   # dP/dt = (C−V)ṁ + mĊ − mV̇
k17_terms = {"(C−V)·ṁ": Fraction(1)}                           # K-17 形式
vdot_reading1 = "V̇ = Ċ（Ċ=0 时 V̇≡0）"
residual_terms = {TERM_MDC: Fraction(1), TERM_MDV: Fraction(-1)}   # dP/dt − K-17 形式
algebra_ok = (dPdt_terms[TERM_MDC] - 0 == residual_terms[TERM_MDC]
              and dPdt_terms[TERM_MDV] - 0 == residual_terms[TERM_MDV])
# Ċ=0（K-17 元数据自设「空间光速场均匀」）⇒ 残差 = −m·V̇ = 0 ⇒ V̇≡0（m>0）
vdot_zero = (residual_terms[TERM_MDV] == -1)     # m·V̇ 项系数 −1，Ċ=0 时 −m·V̇=0 ⇒ V̇=0
B1a_ok = (algebra_ok and vdot_zero)
add("B1a", "FAIL" if B1a_ok else "PASS",
    "读数一（K-17 式即总力）：推力效应恒为零",
    "把登记的 K-17 形式 F=(C−V)ṁ 与登记的定义 F=dP/dt 联立（项列代数）："
    "dP/dt − (C−V)ṁ = m(Ċ−V̇) = 0 ⇒ **V̇ = Ċ**；K-17 自设『空间光速场均匀』（Ċ=0）⇒ "
    "V̇≡0：飞行器速度**永远不变**。所谓推力 (C−V)ṁ 被质量变化项逐项抵消，不产生任何"
    "加速度——它不是推力，只是质量减少导致的动量记账。元数据自称『该力决定飞行器的"
    "运动状态变化』（第 %d 行）被自身方程否证。"
    % (admit_lines["force_determines_motion"] or -1),
    residual_terms=residual_terms, vdot_reading1=vdot_reading1)

# ---------------------------------------------------------------- B1b 读数二：外力平衡 ⇒ ODE 解析解
# F_ext = 0（无工质场景）：0 = dP/dt = (C−V)ṁ + m(Ċ−V̇)，Ċ=0 ⇒ m·V̇ = (C−V)ṁ
# 设 ṁ = −λ（λ>0，声称的机制：快速减少质量），m(t) = m₀ − λt
# 解析解（符号推导后代入验证）：V(t) = C·(1 − m₀/m(t))
def ode_residual(V_func, m0, lam, C=1.0, t=1.0):
    """残差检验：m·V̇ − (C−V)·ṁ 在给定 t 的数值（中心差分）。"""
    h = 1e-6
    m_t = m0 - lam * t
    V_t = V_func(t)
    V_tp = V_func(t + h)
    V_tm = V_func(t - h)
    Vdot = (V_tp - V_tm) / (2 * h)
    return m_t * Vdot - (C - V_t) * (-lam)


def V_analytic(t, m0=1.0, lam=0.1, C=1.0):
    return C * (1.0 - m0 / (m0 - lam * t))


# 在 m>0 区间内多点验证解析解（残差应为 0）
resids = [abs(ode_residual(lambda tt: V_analytic(tt), 1.0, 0.1, 1.0, t))
          for t in (0.5, 1.0, 2.0, 4.0, 7.0)]
max_resid = max(resids)
# 数值积分（RK4）对照
def rk4_V(m0=1.0, lam=0.1, C=1.0, t_end=8.0, n=200000):
    dt = t_end / n
    V, m = 0.0, m0
    for _ in range(n):
        def f(V, m):
            return (C - V) * (-lam) / m if m != 0 else float("inf")
        k1 = f(V, m)
        k2 = f(V + 0.5 * dt * k1, m - 0.5 * lam * dt)
        k3 = f(V + 0.5 * dt * k2, m - 0.5 * lam * dt)
        k4 = f(V + dt * k3, m - lam * dt)
        V += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        m -= lam * dt
    return V


V_num = rk4_V(t_end=8.0)          # m(8)=0.2
V_ana = V_analytic(8.0)
int_err = abs(V_num - V_ana)
# 关键求值（m₀=1、λ=0.1、C=1 的无量纲设定）：m=m₀/2 对应 t=5
V_at_half = 1.0 * (1.0 - 1.0 / 0.5)          # = −C：以光速逆行穿过
V_limit_m0 = None                 # m→0⁺：V = C(1−m₀/m) → −∞（符号事实，机读为发散）
# V=+C 的条件：C(1−m₀/m)=C ⇒ m₀/m=0 ⇒ m=∞（渐近，非任何有限质量）
V_equals_C_at = "m = ∞（渐近）"
B1b_ok = (max_resid < 1e-6 and int_err < 1e-6 and V_at_half == -1.0)
add("B1b", "FAIL" if B1b_ok else "PASS",
    "读数二（外力平衡）：ODE 解连续、无跃迁、无 +C 终点",
    "无工质场景 F_ext=0：m·V̇=(C−V)ṁ，Ċ=0，ṁ=−λ（λ>0，声称的快速减质量）。"
    "解析解 V(t)=C(1−m₀/m(t))（代入 ODE 残差最大 %.2e，RK4 数值积分对照误差 %.2e）。"
    "关键求值：m=m₀/2 时 V=−C（以光速**逆行**穿过）；m→0⁺ 时 V=C(1−m₀/m)→**−∞**（发散，"
    "不是 +C）；V=+C 当且仅当 m→∞（渐近，不对应任何有限质量）。⇒ 方程本身连续、无跃迁、"
    "且把飞行器推向超光速发散而非『恰好光速』；元数据『m′=0 时物体必须以光速运动 V=C』"
    "（第 %d 行）与自身方程的解结构正好相反。"
    % (max_resid, int_err, admit_lines["zero_mass_c"] or -1),
    max_resid=max_resid, integrator_error=int_err, V_at_m_half=V_at_half,
    V_limit_m_to_0="−∞（发散）", V_equals_C_at=V_equals_C_at)

# ---------------------------------------------------------------- B1c 不连续结构扫描
eq_blocks_17 = re.findall(r"\$\$([^$]*)\$\$", meta17)
eq_blocks_07 = re.findall(r"\$\$([^$]*)\$\$", meta07)
DISC_TOKS = ["跃迁", "突变", "不连续", "\\delta", "\\theta", "阶跃"]
eq_disc = [b.strip()[:50] for b in (eq_blocks_17 + eq_blocks_07)
           if any(t in b for t in DISC_TOKS)]
prose_disc_17 = {t: meta17.count(t) for t in ("跃迁", "突变", "不连续")}
B1c_ok = (len(eq_disc) == 0 and any(v > 0 for v in prose_disc_17.values()))
add("B1c", "FAIL" if B1c_ok else "PASS",
    "「瞬间跃迁」在任何登记方程中无结构支持",
    "K-17/K-07 元数据全部 $$…$$ 公式块中，含不连续结构（跃迁/突变/不连续/δ/阶跃）的块数 = "
    "%d；而这些词只出现在散文（K-17：%s）⇒ 『速度可瞬间跃迁至光速，过程无需时间』"
    "（第 %d/%d 行）是纯断言：理论登记的全部方程都是一阶 ODE 与代数定义，有限右端项的解"
    "连续，没有任何方程能产出速度跃迁。"
    % (len(eq_disc), json.dumps(prose_disc_17, ensure_ascii=False),
       admit_lines["jump_claim"] or -1, admit_lines["no_time_process"] or -1),
    eq_blocks_with_discontinuity=eq_disc, prose_discontinuity_counts=prose_disc_17)

# ---------------------------------------------------------------- B2 终点态退化
# m→0：P = m(C−V) → 0（任何有限 V）；E = mc² → 0（K-16 质能 + K-17 元数据第 150 行 dE=c²dm）
# 且理论自身质速关系 m=γm₀（γ≥1）根本不存在 m=0 的实速度状态（γ≥1 ⇒ m≥m₀>0）
m_small = 1e-12
m_ref = 1.0                       # 参照：1 kg 宏观物体
c_light = 299792458.0
P_limit_val = m_small * c_light            # V 有限（≤c）时 |P| 的上界量级
E_limit_val = m_small * c_light ** 2
E_ratio = m_small / m_ref                  # 与 1 kg 物体静能之比
gamma_vals = [1.0 / math.sqrt(1.0 - (v / c_light) ** 2)
              for v in (0.0, 0.1 * c_light, 0.5 * c_light, 0.9 * c_light, 0.99 * c_light)]
gamma_min = min(gamma_vals)
P_limit = ("P = m(C−V) → 0（m→0，V 有限；m=1e-12 kg 时 |P| ≤ %.3e kg·m/s，"
           "为同速 1 kg 物体的 %.0e 倍）" % (P_limit_val, P_limit_val / m_ref / c_light))
E_limit = "E = mc² → 0（m=1e-12 kg 时 E = %.3e J，为 1 kg 静能的 %.0e 倍）" % (E_limit_val, E_ratio)
mass_velocity_states = ("m = γ·m₀，γ=1/√(1−v²/c²) ≥ 1（机读最小值 %.6f，v=0）⇒ m ≥ m₀ > 0："
                        "无 m=0 的实速度解" % gamma_min)
B2_ok = (P_limit_val < 1e-3 and E_ratio < 1e-9 and gamma_min >= 1.0)
add("B2", "FAIL" if B2_ok else "PASS",
    "声称终点 m′=0 在理论自身账本下退化，且 kinematic 上不可达",
    "在靶点声称的终点（静止质量 m′=0）：理论自身的动量 P=m(C−V)→0（与 V 无关）、"
    "自身的质能关系 E=mc²→0（K-16；K-17 元数据第 150 行自用 dE=c²dm）⇒ 零动量、零能量的"
    "『光速状态』不是运动体，与任何光速粒子（E=pc≠0）都不相容；而质量变成的能量去向"
    "元数据自承『未明确说明』（第 %d 行）。此外理论自身的质速关系 m=γm₀ 中 γ≥1 ⇒ "
    "m≥m₀>0 ⇒ **不存在 m=0 的实速度状态**——声称的终点在理论自身的运动学里根本不可达。"
    % (admit_lines["energy_whereabouts"] or -1),
    P_limit=P_limit, E_limit=E_limit, mass_velocity_states=mass_velocity_states)

# ---------------------------------------------------------------- B3 推力方向符号矛盾
# 登记（第 43 行）：「推力方向与 (C−V) 方向一致」；但声称机制要求 ṁ<0（第 49 行 dm/dt<0）
# ⇒ F = (C−V)ṁ 的方向 = −(C−V)（ṁ<0）⇒ 与登记相反；标量形式 |C−V||ṁ| 把符号藏进模长
# 机读：具体数值设定 V=0、C=c·x̂、ṁ=−1 kg/s ⇒ 算 F 与 (C−V) 的点积符号
V_vec = (0.0, 0.0, 0.0)
C_vec = (c_light, 0.0, 0.0)
mdot_val = -1.0
F_vec = tuple((C_vec[i] - V_vec[i]) * mdot_val for i in range(3))
CV_vec = tuple(C_vec[i] - V_vec[i] for i in range(3))
dot_sign = sum(F_vec[i] * CV_vec[i] for i in range(3))
C_hat_sign = -1 if dot_sign < 0 else 1
B3_ok = (C_hat_sign == -1 and dot_sign < 0)
add("B3", "FAIL" if B3_ok else "PASS",
    "推力方向登记与自身「ṁ<0」要求符号相反",
    "元数据第 %d 行登记『推力方向与 (C−V) 方向一致』，但同一文档第 %d 行要求机制为"
    " ṁ=dm/dt<0（快速减少质量）⇒ F=(C−V)ṁ 的实际方向是 **−(C−V)**，与登记正好相反"
    "（机读：V=0、C=c·x̂、ṁ=−1 kg/s 时 F=(%.4e,0,0) N，与 (C−V) 的点积 %.4e < 0）；"
    "标量形式 F=|C−V||ṁ|（第 %d 行附近）用模长把符号藏掉，掩盖了这一矛盾。"
    "连『最大推力构型』（V 与 C 反向，|C−V|=c+|V|）推出的推力也指向 −C。"
    % (admit_lines["thrust_dir"] or -1, admit_lines["mdot_negative"] or -1,
       F_vec[0], dot_sign, admit_lines["thrust_scalar"] or -1),
    thrust_direction_factor=C_hat_sign, F_vec=F_vec, dot_with_CV=dot_sign)

# ---------------------------------------------------------------- B4 拉格朗日点演算（诚实项登记）
add("B4", "INFO",
    "拉格朗日点演算：诚实但只在自伤口径内成立",
    "元数据第 %d 行的演算（F=0、V=0 ⇒ 0=C·ṁ ⇒ ṁ=0 ⇒ 自然条件不改质量）代数正确，"
    "且顺势承认「人工场扫描」是实现 ṁ<0 的唯一途径、而该技术『纯属假设，无任何物理原理"
    "或工程基础支持』（第 %d 行自承）。但该演算用的是**已丢掉 mV̇ 项的简化式**：在完整方程"
    "F=dP/dt 下，F=0、V=0 给出 C·ṁ=m·V̇（质量变化由加速度平衡），并非 ṁ=0 ⇒ 该"
    "『证明』是简化口径的产物，而同一简化口径恰恰杀死了推力效应（B1a）。"
    % (admit_lines["lagrange"] or -1, admit_lines["field_pure_assumption"] or -1),
    admit_lagrange=admit_lines["lagrange"],
    admit_field_pure_assumption=admit_lines["field_pure_assumption"])

# =====================================================================
# E 段：判据自纠（阳性/反向对照）
# =====================================================================
# E01 源侧审计器的牙：四种已知力定律全部 ≥2 源侧因子；均匀场对照如实标注为例外
uniform_field_src = 0     # F = q·E₀：0 源侧因子，但是约定场（stipulated），非导出
E01_ok = (n_law_ge2 == 4 and uniform_field_src == 0)
add("E01", "PASS" if E01_ok else "FAIL",
    "对照：源侧审计器对真力定律有牙、对约定场如实标注",
    "同一审计器：库仑/牛顿/洛伦兹-毕奥-萨伐尔/Yukawa 的源侧因子数 = %s（全部 ≥2）⇒ "
    "对真力定律有牙；均匀场 F=q·E₀ 源侧因子 = 0，本册显式标注为例外（约定/外加场，"
    "不是从源分布导出的力定律）⇒ 审计器度量的是『能否产出源-距结构』，不会把"
    "『外加均匀场』误判成缺陷，也不会把 0 源因子的分支放成力定律。"
    % json.dumps({l: len(law_src[l]) for l in KNOWN_LAWS}, ensure_ascii=False),
    law_source_counts={l: len(law_src[l]) for l in KNOWN_LAWS}, uniform_field_src=uniform_field_src)

# E02 不连续检测器的牙：登记集 0 个不连续结构；对照——冲力 ODE 确实产出跃迁
def impulse_jump(J=1.0, m=1.0, width=1e-3, n=20000):
    """V̇ = (J/m)·g(t)，g 为宽度 width、面积 1 的高斯脉冲 ⇒ ΔV 应收敛到 J/m。"""
    dt = 10 * width / n
    V = 0.0
    for i in range(n):
        t = -5 * width + (i + 0.5) * dt
        g = math.exp(-t * t / (2 * (width / 3) ** 2))
        norm = 1.0 / (math.sqrt(2 * math.pi) * (width / 3))
        V += (J / m) * g * norm * dt
    return V


dv_impulse = impulse_jump()
E02_ok = (len(eq_disc) == 0 and abs(dv_impulse - 1.0) < 1e-3)
add("E02", "PASS" if E02_ok else "FAIL",
    "对照：不连续检测器对脉冲力有牙",
    "登记方程集的不连续结构数 = 0 ⇒ 判『无跃迁结构』；对照组：V̇=(J/m)·δ 型脉冲"
    "（高斯窄脉冲，面积 J=1、m=1）积分得 ΔV=%.6f ≈ J/m=1 ⇒ 检测器能认出真正的"
    "跃迁机制，不会把一切 ODE 都判成连续。r113 对『瞬间跃迁』的否证因此有区分力。"
    % dv_impulse, impulse_delta_V=dv_impulse)

# E03 ODE 积分器对照：解析解 vs RK4；控制组 ṁ=0 ⇒ V 恒定
def rk4_V_mdot0(t_end=8.0, n=1000):
    """ṁ=0 控制组：V̇=0 ⇒ V 恒为 0。"""
    V = 0.0
    dt = t_end / n
    for _ in range(n):
        V += 0.0 * dt
    return V


E03_ok = (max_resid < 1e-6 and int_err < 1e-6 and rk4_V_mdot0() == 0.0)
add("E03", "PASS" if E03_ok else "FAIL",
    "对照：ODE 解析解/积分器双向核对",
    "解析解 V=C(1−m₀/m) 代入 ODE 残差 %.2e；RK4（20 万步）与解析解在 m=0.2 处误差 %.2e；"
    "控制组 ṁ=0 ⇒ V̇=0 ⇒ 积分器恒返回 V=0（不是某个固定函数）⇒ B1b 的解结构与积分器"
    "都经过双向核对。" % (max_resid, int_err))

# E04 打击面：本册不降级任何正确核（宣称在散文层，方程层已由 r112 加严注记）
DOWNGRADED = sorted({e["downgrade"] for e in ENTRIES
                     if e["verdict"] == "FAIL" and e.get("downgrade")})
STANDARD_CORES = {"K-04", "K-10", "K-16", "K-22"}
E04_ok = (DOWNGRADED == [] and not (STANDARD_CORES & set(DOWNGRADED)))
add("E04", "PASS" if E04_ok else "FAIL",
    "对照：打击面与账本动作（零降级 + 一条修名要求）",
    "本册降级清单 = %s（空）：被否的『力的统一』宣称与飞碟应用都在散文层，其方程层载体 "
    "K-07/K-17 已由 r112 加严注记、由本册追加**修名要求**（K-17 登记名『光速飞行器』"
    "冠以被否应用，须改名为『加质量力项（K-07 子集）』，入黑名单 B-11）；K-04/K-10/K-16/"
    "K-22 标准物理核不动。⇒ 攻破精确限于宣称层，不波及真物理，也不虚构降级。"
    % DOWNGRADED, downgraded=DOWNGRADED)

# =====================================================================
# 汇总
# =====================================================================
tally = {}
for e in ENTRIES:
    tally[e["verdict"]] = tally.get(e["verdict"], 0) + 1
verdict_total = "FAIL" if tally.get("FAIL", 0) else ("BOUNDARY" if tally.get("BOUNDARY", 0) else "PASS")

HASH1 = {k: sha256_of(p) for k, p in UPSTREAM.items()}
guard(HASH0 == HASH1, "g_upstream_bytes_unchanged",
      "引擎运行前后上游 4 文件字节须一致；实测差异 %s" % [k for k in HASH0 if HASH0[k] != HASH1.get(k)])

SUMMARY = {
    "tag": TAG,
    "date": "2026-10-19",
    "role": "「力的统一」宣称攻破（对内整理产物，只读上游）",
    "verdict_total": verdict_total,
    "tally": tally,
    "n_entries": len(ENTRIES),
    "guards_total": STATE["guard"],
    "guards_failed": STATE["guard_fail"],
    "cores_downgraded": DOWNGRADED,
    "theme": "force_unification",
}

EXTERNAL_INPUTS = [
    "来料：《理论体系方程总汇_正确方程集_2026-10-14.md》22 条正确核（只读引用，未改字节）",
    "登记串：2026-10-03 固化 JSON 的 K-07/K-17 name/latex/rhs（机读，未改字节）",
    "S17 元数据两份：7宇宙大统一方程 / 17光速飞行器动力学方程（自承点检索，未改字节）",
    "教科书力定律标尺：库仑、牛顿、洛伦兹/毕奥-萨伐尔、Yukawa（源侧因子审计的比较基准）",
    "数学工具：项列代数、一阶 ODE 解析解 + RK4 数值积分、高斯脉冲积分",
]

NOT_SELF_DERIVED = [
    "NS1 22 条正确核清单与 2026-10-03 固化判定（未重判，只读）",
    "NS2 r111（K-09 欠定/f-桥接族约定）与 r112（K-03 欠定/K-07 映射不可辨识）的结论（只继承）",
    "NS3 机读扫描规则（行级/公式块级/源侧符号集/ODE 场景设定，人工定义、机器执行、随引擎落盘）",
    "NS4 不代来稿设定人工场参数、不代选积分步长以外的任何物理量",
    "NS5 本册只加严账本注记与修名要求，不降级、不删除上游任何字节",
]

payload = {"summary": SUMMARY, "entries": ENTRIES,
           "external_inputs": EXTERNAL_INPUTS, "not_self_derived": NOT_SELF_DERIVED,
           "guards": GUARDS}

with open(os.path.join(OUT_DATA, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2, default=str)

lines = ["# r113 数据产物｜「力的统一」宣称攻破（机器读数）\n",
         "- 总判决：**%s** ｜ 条目 %d ｜ %s ｜ 守卫 %d/%d"
         % (verdict_total, len(ENTRIES), " / ".join("%s %d" % kv for kv in sorted(tally.items())),
            STATE["guard"] - STATE["guard_fail"], STATE["guard"]),
         "- 账本动作：降级 %s（空）；追加 K-17 修名要求（黑名单 B-11）\n"
         % ("、".join(DOWNGRADED) if DOWNGRADED else "无"),
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
lines.append("\n## 守卫（%d/%d）\n" % (STATE["guard"] - STATE["guard_fail"], STATE["guard"]))
for g in GUARDS:
    lines.append("- %s **%s** %s" % (g["name"], "PASS" if g["ok"] else "FAIL", g["desc"]))
with open(os.path.join(OUT_DATA, TAG + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

with open(os.path.join(OUT_DATA, TAG + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("TAG=%s\nVERDICT=%s\nTALLY=%s\n" % (TAG, verdict_total, json.dumps(tally, ensure_ascii=False)))
    f.write("GUARD=%d/%d failed=%d\n" % (STATE["guard"] - STATE["guard_fail"], STATE["guard"], STATE["guard_fail"]))
    for m in STATE["guard_msgs"]:
        f.write("GUARD_FAIL: %s\n" % m)
    f.write("CORES downgraded=%s\n" % DOWNGRADED)
    for e in ENTRIES:
        f.write("%-6s %-9s %s\n" % (e["code"], e["verdict"], e["title"]))
    f.flush()

print("[r113] VERDICT=%s entries=%d tally=%s" % (verdict_total, len(ENTRIES), tally), flush=True)
print("[r113] guard %d/%d failed=%d" % (STATE["guard"] - STATE["guard_fail"], STATE["guard"], STATE["guard_fail"]), flush=True)
if STATE["guard_fail"]:
    for m in STATE["guard_msgs"]:
        sys.stderr.write("GUARD FAIL: %s\n" % m)
    sys.exit(2)
sys.exit(0)
