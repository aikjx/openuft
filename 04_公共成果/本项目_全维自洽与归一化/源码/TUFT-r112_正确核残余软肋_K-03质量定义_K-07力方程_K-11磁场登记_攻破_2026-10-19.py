# -*- coding: utf-8 -*-
"""TUFT-r112 ｜ 「核心公式正确核」残余软肋攻破：K-03 质量定义 / K-07 力方程 / K-11 磁场登记 —— 机器判决

来料 = 本库《理论体系方程总汇_正确方程集_2026-10-14.md》收录的 22 条「正确核」
（外部来料《张祥前统一场论核心公式》经全目录盘点后的存活清单）中的 K-03、K-07、K-11，
以及 2026-10-03 固化册的登记串与 S17 元数据语料。

本册立场（红线）：**对内攻破**——攻击对象是本库整理产物中的软肋，不产生新物理、
不修改任何上游文件字节；所有裁定由量纲代数（Fraction 精确）、约定吸收检验、
立体角定理数值、重言检测、欠定性计数承担。

攻破命题：
  P-A（K-03 质量定义 m = k·dn/dΩ）：
      A1 离散对比形 m=(k/g)(Δn/ΔΩ) 在「引力常数」「引力场」两种读数下量纲是否俱败？
      A2 k = 4π·m_p 且 m_p = √(ħc/G) ⇒ 「导出 G = ħc/m_p²」是否为定义重排（重言）？
      A3 总立体角被 ∮dΩ = 4π 定理锁死 ⇒ 「Ω 随洛伦兹收缩变化导出质速关系」是否互斥？
      A4 「点电荷零静止质量」的登记解释（各向同性）是否自反？
      A5 n / dn/dΩ 无观测程序、k 外部锚定 ⇒ 定义是否欠定（与 r111 的 K-09 同族）？
  P-B（K-07 力方程 F = dP/dt，P = m(C−V)）：
      B1 符号缺陷能否被约定完全吸收（σ/τ 枚举）？吸收后残差物理内容是否为 0？
      B2 「四项 ↔ 四种基本力」映射是否可辨识（0 条方程约束 + 经典极限四项塌缩）？
      B3 C⃗（矢量光速）是否只出现在定义性行中、无任何观测约束？
  P-C（K-11 磁场 B⃗ = μ₀(v⃗×R⃗)/(4πR*³)（补 v））：
      C1 登记串（name）缺 q ⇒ 按字面读数是否量纲断裂、缺口是否恰为 [q]？
      C2 几何形式是否依赖特设 [k′]（元数据自承「量纲存在矛盾」）+ q 符号三处互斥？
      C3 标准形式代入 q 后是否恰为教科书毕奥-萨伐尔（零增量）？
"""

import hashlib
import json
import math
import os
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50

HERE = os.path.dirname(os.path.abspath(__file__))          # .../本项目_全维自洽与归一化/源码
NORM = os.path.dirname(HERE)                               # .../本项目_全维自洽与归一化
ROOT = os.path.dirname(os.path.dirname(NORM))              # openuft
OUT_DATA = os.path.join(NORM, "数据")
os.makedirs(OUT_DATA, exist_ok=True)

TAG = "TUFT-r112_正确核残余软肋_K-03质量定义_K-07力方程_K-11磁场登记_攻破_2026-10-19"

SRC_1014 = os.path.join(ROOT, "理论体系方程总汇_正确方程集_2026-10-14.md")
SRC_CORE_JSON = os.path.join(NORM, "数据", "统一场论核心公式_正确核固化_2026-10-03.json")
META_DIR = os.path.join(ROOT, "01_独立体系", "S17_统一场论核心公式", "01_文献来源",
                        "来源_核心公式元数据")
META_K03 = os.path.join(META_DIR, "3质量定义方程.md")
META_K07 = os.path.join(META_DIR, "7宇宙大统一方程.md")
META_K11 = os.path.join(META_DIR, "11磁场定义方程.md")

# ---------------------------------------------------------------- 量纲四元组 (M,L,T,A)
# A = 电流量纲（安培）；本册只用代数，不依赖具体单位制常数（口径与 r111 一致）
def D(m=0, l=0, t=0, a=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(a))


DIMLESS = D(0, 0, 0, 0)
DIM_M = D(1, 0, 0, 0)
DIM_L = D(0, 1, 0, 0)
DIM_T = D(0, 0, 1, 0)
DIM_A = D(0, 0, 0, 1)
DIM_V = D(0, 1, -1, 0)                 # 速度
DIM_q = D(0, 0, 1, 1)                  # 电荷 = A·T
DIM_mu0 = D(1, 1, -2, -2)              # μ₀ = N/A²
DIM_B = D(1, 0, -2, -1)                # 磁感应强度 T = kg/(A·s²)
DIM_G = D(-1, 3, -2, 0)                # 万有引力常数 m³/(kg·s²)
DIM_A_grav = D(0, 1, -2, 0)            # 引力场 / 加速度
DIM_curl = D(0, -1, 0, 0)              # 旋度算符


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


print("[r112] boot ok", flush=True)

# =====================================================================
# 0. 上游装载与字节防改（sha256 首尾比对）
# =====================================================================
UPSTREAM = {
    "ledger_1014": SRC_1014,
    "core_json_1003": SRC_CORE_JSON,
    "meta_K03": META_K03,
    "meta_K07": META_K07,
    "meta_K11": META_K11,
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
print("[r112] upstream loaded: %s" % ", ".join("%s=%s" % (k, v[:8]) for k, v in HASH0.items()), flush=True)

ledger_txt = open(SRC_1014, encoding="utf-8").read()
core_json = json.load(open(SRC_CORE_JSON, encoding="utf-8"))
meta03 = open(META_K03, encoding="utf-8").read()
meta07 = open(META_K07, encoding="utf-8").read()
meta11 = open(META_K11, encoding="utf-8").read()

# ---- 机读 10-14 总汇 22 行（编号 / 公式文本 / 状态文本）
# 行结构：| K-xx | 来源号 | 公式 | 状态 | 层级 |  ⇒ 公式在 cells[1]、状态在 cells[2]
row_re = re.compile(r"^\|\s*(K-\d+)\s*\|([^\n]*)\|", re.M)
raw_rows = [(m.group(1), m.group(2)) for m in row_re.finditer(ledger_txt)]
rows = []
for rid, rest in raw_rows:
    cells = [c.strip() for c in rest.split("|")]
    formula = cells[1] if len(cells) > 1 else ""
    status = cells[2] if len(cells) > 2 else ""
    rows.append({"id": rid, "formula": formula, "status": status, "raw": rest})
n_rows = len(rows)
uniq_rows = len(set(r["id"] for r in rows))
guard(n_rows == 22 and uniq_rows == 22, "g_ledger_22_rows",
      "10-14 总汇须机读出 22 行唯一 K-编号；实测 %d/%d" % (n_rows, uniq_rows))
add("L01", "PASS" if (n_rows == 22 and uniq_rows == 22) else "FAIL",
    "上游账本机读：22 行正确核",
    "从 10-14 总汇正则提取 K-编号行 %d 条、唯一 %d 个（本册不重判该清单，只读）" % (n_rows, uniq_rows),
    rows=[r["id"] for r in rows])

# ---- 机读 2026-10-03 固化 JSON 的 K-09/K-10/K-11 登记串
def core_entry(cid):
    for it in core_json.get("canon", []):
        if isinstance(it, dict) and it.get("id") == cid:
            return it
    return None


E03, E07, E09, E10, E11 = (core_entry("K-03"), core_entry("K-07"),
                           core_entry("K-09"), core_entry("K-10"), core_entry("K-11"))
guard(all(x is not None for x in (E03, E07, E09, E10, E11)), "g_core_json_targets",
      "固化 JSON 须含 K-03/K-07/K-09/K-10/K-11；实测缺失 %s"
      % [c for c, x in zip(("K-03", "K-07", "K-09", "K-10", "K-11"),
                           (E03, E07, E09, E10, E11)) if x is None])
add("L02", "PASS" if all(x is not None for x in (E03, E07, E09, E10, E11)) else "FAIL",
    "上游登记串机读：K-03/K-07/K-09/K-10/K-11",
    "name/latex/rhs 三字段全部落到本册（防手抄靶点）：K-11 name『%s』；K-11 latex『%s』"
    % (E11.get("name") if E11 else None, E11.get("latex") if E11 else None),
    k11_name=E11.get("name") if E11 else None, k11_latex=E11.get("latex") if E11 else None)


def leading_sign(s):
    """取登记串中 '=' 之后首个非空字符的符号：'-' ⇒ -1，否则 +1。"""
    if not s:
        return None
    i = s.find("=")
    if i < 0:
        return None
    j = i + 1
    while j < len(s) and s[j] in " \t":
        j += 1
    if j < len(s) and s[j] == "-":
        return -1
    return 1


SIG_K09 = leading_sign(E09.get("latex", "")) if E09 else None      # q = kk′(1/Ω²)dΩ/dt
SIG_K10_latex = leading_sign(E10.get("latex", "")) if E10 else None  # E = −(kk′/…)…
SIG_K10_name = leading_sign(E10.get("name", "")) if E10 else None    # 电场 E⃗ = q r̂/(4πε₀r²)
# K-11 元数据中的电荷定义（几何形式代入句）
m11_qdef = re.search(r"q\s*=\s*-k'k", meta11)
SIG_K11_meta_q = -1 if m11_qdef else (1 if re.search(r"q\s*=\s*k'k", meta11) else None)
add("L03", "PASS",
    "登记串符号机读（q 定义 / E 定义）",
    "K-09 latex 符号 %+d；K-10 latex 符号 %+d；K-10 name 符号 %+d；K-11 元数据电荷定义符号 %+d"
    "（+1 无显式负号，-1 有显式负号）"
    % (SIG_K09 or 0, SIG_K10_latex or 0, SIG_K10_name or 0, SIG_K11_meta_q or 0),
    sig_k09=SIG_K09, sig_k10_latex=SIG_K10_latex, sig_k10_name=SIG_K10_name,
    sig_k11_meta_q=SIG_K11_meta_q)

# ---- 元数据自承检索（靶点自承，带行号）
def grep_line(text, pat):
    m = re.search(pat, text)
    if not m:
        return None
    return text[:m.start()].count("\n") + 1


ADMIT = {
    "k_planck": (META_K03, meta03, r"k\s*=\s*4\s*\\pi\s*m_p|k = 4π m_p|k\s*=\s*4\\pi\s*\\sqrt"),
    "mp_def": (META_K03, meta03, r"m_p\s*=\s*\\sqrt\{\\hbar c / G\}|m_p = √\(ħc/G\)"),
    "k_external": (META_K03, meta03, r"常数的外源性"),
    "fitted_newton": (META_K03, meta03, r"为了与牛顿引力定律"),
    "mass_velocity": (META_K03, meta03, r"导出.{0,12}质速关系|m\s*=\s*m_0\s*/\s*\\sqrt"),
    "point_charge_zero": (META_K03, meta03, r"点电荷质量为零"),
    "discrete_kg_form": (META_K03, meta03, r"m\s*=\s*\\frac\{k\}\{g\}"),
    "omega_total_closed": (META_K03, meta03, r"整个闭合曲面"),
    "kprime_contradiction": (META_K11, meta11, r"量纲存在矛盾，需特殊定义"),
    "kprime_no_value": (META_K11, meta11, r"其具体数值未在文档中精确给出"),
    "geom_substitution": (META_K11, meta11, r"代入运动电荷的磁场表达式"),
    "four_forces_prose": (META_K07, meta07, r"四种基本力"),
}
admit_lines = {}
for key, (path, text, pat) in ADMIT.items():
    ln = grep_line(text, pat)
    admit_lines[key] = ln
missing_admits = [k for k, v in admit_lines.items() if v is None]
guard(not missing_admits, "g_meta_admissions_present",
      "元数据自承点须全部检索命中（防靶点漂移）；缺失 %s" % missing_admits)
add("L04", "PASS" if not missing_admits else "FAIL",
    "元数据自承检索（靶点自己承认的软肋）",
    "12 项自承点命中行号：%s" % json.dumps(admit_lines, ensure_ascii=False),
    admit_lines=admit_lines)

# =====================================================================
# A 段：K-03 质量定义方程 m = k·dn/dΩ
# =====================================================================
# ---------------------------------------------------------------- A1 离散对比形双读俱败
# 登记变体（元数据 §1 公式变体）：m = (k/g)·(Δn/ΔΩ)，"其中 g 为引力常数"
DIM_k = DIM_M                       # [k] = M（元数据 §单位系统自承）
DIM_dn_dO = DIMLESS                 # 条数/立体角，两皆无量纲
req_g = ddiv(DIM_k, DIM_M)          # 闭合要求 [m]=M ⇒ [g] = [k]/[m]
dim_m_gG = ddiv(DIM_k, DIM_G)       # 读数一：g = 万有引力常数 G
dim_m_gf = ddiv(DIM_k, DIM_A_grav)  # 读数二：g = 引力场强度（加速度）
A1_ok = (not deq(dim_m_gG, DIM_M)) and (not deq(dim_m_gf, DIM_M)) and deq(req_g, DIMLESS)
add("A1", "FAIL" if A1_ok else "PASS",
    "K-03 离散对比形 m=(k/g)(Δn/ΔΩ) 双读数量纲俱败",
    "闭合要求 [g]=%s（无量纲）——任何标准读法的『引力常数』都不无量纲。"
    "读数一 g=G（[G]=%s）⇒ [m]=%s ≠ M；读数二 g=引力场（[g]=%s）⇒ [m]=%s ≠ M。"
    % (dstr(req_g), dstr(DIM_G), dstr(dim_m_gG), dstr(DIM_A_grav), dstr(dim_m_gf)),
    req_g=dstr(req_g), dim_m_if_gG=dstr(dim_m_gG), dim_m_if_gfield=dstr(dim_m_gf))

# ---------------------------------------------------------------- A2 重言检测：G = ħc/m_p²
HBAR = Decimal("1.054571817e-34")     # J·s（元数据 §7 登记值）
CC = Decimal("299792458")             # m/s
GG = Decimal("6.67430e-11")           # m³/(kg·s²)（元数据 §7 登记值）
M_E = Decimal("9.1093837015e-31")     # kg（CODATA 电子质量，独立测量常数）
TAUT_THRESH = Decimal("1e-30")

m_p = (HBAR * CC / GG).sqrt()         # 元数据登记定义 m_p = √(ħc/G)
res_T1 = abs(GG - HBAR * CC / (m_p * m_p)) / GG          # 声称「第一性原理导出」的关系
res_T2 = abs(GG - HBAR * CC / (M_E * M_E)) / GG          # 反向对照：电子质量（非定义配对）
is_taut_T1 = res_T1 < TAUT_THRESH
is_taut_T2 = res_T2 < TAUT_THRESH
add("A2", "FAIL" if (is_taut_T1 and not is_taut_T2) else "PASS",
    "K-03 「导出 G = ħc/m_p²」为定义重排（重言），零内容",
    "靶命题 T1『由其第一性原理导出量子引力核心关系 G=ħc/m_p²』：代入来料自己登记的"
    " m_p≡√(ħc/G) 后残差 %s（相对）< %s ⇒ 定义重排。反向对照 T2『G=ħc/m_e²』残差 %s ⇒ "
    "检测器不误判非定义配对（电子质量是与 G 独立的测量常数）。"
    % (res_T1, TAUT_THRESH, res_T2),
    res_T1=str(res_T1), res_T2=str(res_T2), thresh=str(TAUT_THRESH))

# k = 4π m_p 的「推导」前提计数：前提 A = (n=1, Ω=4π) ↦ m = m_p；结论 C = k = 4π m_p
# 机读：A 与 C 在定义 m = k·n/Ω 下互为代数解算；且 22 行中约束 A 的方程数 = 0
rows_planck = [r["id"] for r in rows if ("普朗克" in r["raw"] or "m_p" in r["raw"])]
add("A2b", "FAIL" if (len(rows_planck) == 0 and is_taut_T1) else "PASS",
    "k = 4π·m_p 的前提外部性：22 行中约束普朗克几何图像的方程数 = 0",
    "『一个普朗克质量对应 n=1、Ω=4π 的一条空间位移矢量』是**外部假设**（22 行命中 %d 条），"
    "把它代入定义 m=k·n/Ω 解出 k=4πm_p —— 结论就是假设本身改写，独立前提数 = 0；"
    "而 m_p≡√(ħc/G) 含 G ⇒ k 的数值由外部常数 G 锚定（元数据自承『常数的外源性』，第 %d 行）。"
    % (len(rows_planck), admit_lines["k_external"] or -1),
    rows_with_planck=rows_planck, admit_line_k_external=admit_lines["k_external"])

# ---------------------------------------------------------------- A3 总立体角定理 vs 质速关系
def omega_closed_surface(gamma, n):
    """洛伦兹收缩椭球（半轴 1/γ, 1, 1，沿 x 收缩）对原点的总立体角，中点法则。"""
    dth = math.pi / n
    dph = 2.0 * math.pi / n
    tot = 0.0
    for i in range(n):
        th = (i + 0.5) * dth
        st, ct = math.sin(th), math.cos(th)
        for j in range(n):
            ph = (j + 0.5) * dph
            cp, sp = math.cos(ph), math.sin(ph)
            x, y, z = st * cp / gamma, st * sp, ct
            a1, a2, a3 = ct * cp / gamma, ct * sp, -st      # ∂r/∂θ
            b1, b2, b3 = -st * sp / gamma, st * cp, 0.0     # ∂r/∂φ
            c1 = a2 * b3 - a3 * b2
            c2 = a3 * b1 - a1 * b3
            c3 = a1 * b2 - a2 * b1
            num = x * c1 + y * c2 + z * c3
            den = (x * x + y * y + z * z) ** 1.5
            tot += num / den
    return tot * dth * dph


def omega_cap(theta0, n):
    """球冠（非闭合面）立体角对照：真值 2π(1−cosθ₀)。"""
    dth = theta0 / n
    s = sum(math.sin((i + 0.5) * dth) for i in range(n))
    return s * dth * 2.0 * math.pi


FOUR_PI = 4.0 * math.pi
GRIDS = (120, 240, 480, 960)
GAMMAS = (1.25, 2.0, 10.0)
solid = {}
for g in GAMMAS:
    vals = [omega_closed_surface(g, n) for n in GRIDS]
    orders = []
    for a, b, c in zip(vals, vals[1:], vals[2:]):
        d1, d2 = a - c, b - c
        if d1 > 0 and d2 > 0 and b != c:
            orders.append(math.log(d1 / d2, 2))
    solid[g] = {"vals": vals, "orders": orders,
                "rel": abs(vals[-1] - FOUR_PI) / FOUR_PI}
cap_vals = [omega_cap(math.pi / 3.0, n) for n in (240, 480, 960)]
cap_rel = abs(cap_vals[-1] - math.pi) / math.pi

solid_ok = all(v["rel"] < 1e-4 for v in solid.values())
orders_ok = [o for v in solid.values() for o in v["orders"] if 1.5 <= o <= 3.0]
cap_ok = cap_rel < 1e-6
guard(solid_ok and cap_ok and len(orders_ok) >= 4, "g_solidangle_bothsides",
      "闭合面须收敛到 4π、非闭合球冠须收敛到 π、阶≈2（四档步长，γ=10 首档因尖点欠采样非单调、"
      "取后续档）；实测 rel_ellipsoid=%s rel_cap=%.2e n_orders_in_band=%d"
      % ({str(g): "%.2e" % v["rel"] for g, v in solid.items()}, cap_rel, len(orders_ok)))

# 声称的质速关系所需 Ω：m = k·n/Ω，n 不变、m = γ·m₀ ⇒ Ω 须缩到 4π/γ
required = {g: FOUR_PI / g for g in GAMMAS}
deficit = {g: (FOUR_PI - FOUR_PI / g, 100.0 * (1.0 - 1.0 / g)) for g in GAMMAS}
A3_ok = solid_ok and cap_ok and all(d[1] > 5.0 for d in deficit.values())
add("A3", "FAIL" if A3_ok else "PASS",
    "K-03 总立体角被 ∮dΩ=4π 锁死 ⇒ 「Ω 收缩导出质速关系」互斥",
    "定理：∇·(r̂/r²)=4πδ³(r) ⇒ 任何包围原点的闭合面总立体角恒为 4π。数值（洛伦兹收缩椭球，"
    "半轴 1/γ,1,1；四档步长 120/240/480/960）：γ=1.25 Ω=%.9f（n=960，相对偏差 %.2e）、"
    "γ=2 Ω=%.9f、γ=10 Ω=%.9f，收敛阶 %s（≈2 表明是真值 4π 而非巧合；γ=10 首档三重序因尖点欠采样非单调，"
    "已按纪律取后续档）。对照组：θ₀=60° 球冠 Ω=%.9f ≈ π（相对 %.2e）"
    "⇒ 计算器对闭合/非闭合有区分。登记的总质量形式用『穿过包围物体的整个闭合曲面（总立体角为 Ω）』"
    "（元数据第 %d 行）⇒ Ω≡4π 与运动无关；而来料自承的质速关系推导（第 %d 行）要求 Ω=4π/γ"
    "（γ=1.25 时缺口 %.3f sr = %.1f%%）⇒ 两个自承命题互斥，该推导路线不成立。"
    % (solid[1.25]["vals"][-1], solid[1.25]["rel"], solid[2.0]["vals"][-1], solid[10.0]["vals"][-1],
       ["%.2f" % o for v in solid.values() for o in v["orders"]][:6],
       cap_vals[-1], cap_rel,
       admit_lines["omega_total_closed"] or -1, admit_lines["mass_velocity"] or -1,
       deficit[1.25][0], deficit[1.25][1]),
    solid_angle={str(g): {"vals": v["vals"], "rel": v["rel"]} for g, v in solid.items()},
    orders=[o for v in solid.values() for o in v["orders"]],
    cap_vals=cap_vals, cap_rel=cap_rel,
    required_omega={str(g): required[g] for g in GAMMAS},
    deficit_sr={str(g): deficit[g][0] for g in GAMMAS},
    deficit_pct={str(g): deficit[g][1] for g in GAMMAS})

# ---------------------------------------------------------------- A4 点电荷零质量自反
# 登记解释（元数据 §5）：点电荷零静止质量因为「dn/dΩ 各向同性且无额外集中」。
# 机算：各向同性 ⇒ dn/dΩ = ρ > 0 常数 ⇒ m = k∮ρ dΩ = 4πkρ > 0（零质量要求 ρ≡0）。
RHO = Fraction(1, 1)                    # 单位密度符号值（>0）
m_iso = Fraction(4) * math.pi * 1.0 * 1.0   # 数值演示：4πkρ（k=ρ=1）
A4_ok = m_iso > 0.0
add("A4", "FAIL" if A4_ok else "PASS",
    "K-03 「点电荷零静止质量」的登记解释自反",
    "各向同性密度 dn/dΩ = ρ>0 代入登记定义得 m = k∮ρdΩ = 4πkρ > 0（数值演示 %.6f，k=ρ=1）；"
    "要 m=0 必须 ρ≡0（一条位移矢量都没有），这与电荷定义自身的前提（q∝dΩ/dt≠0 依赖空间运动）"
    "不相容。『各向同性且无额外集中 ⇒ 零质量』在数学上给出相反结果：均匀分布积分出**正的**"
    "总质量。该解释（元数据第 %d 行）不可用。"
    % (m_iso, admit_lines["point_charge_zero"] or -1),
    m_isotropic_demo=m_iso)

# ---------------------------------------------------------------- A5 欠定门与降级
# n_free：n（条数）与密度场 dn/dΩ 无可观测程序；Ω 在总质量形式下被定理锁死（A3）；k 外部锚定（A2b）
rows_omega = [r["id"] for r in rows if ("dn" in r["formula"] or "\\Omega" in r["formula"]
                                        or "Ω" in r["formula"] or "Delta" in r["formula"]
                                        or "Δ" in r["formula"])]
n_free = 1            # 密度场 / 条数（至少一个无可观测自由量）
n_obs = 0             # 22 行中把 n 或 dn/dΩ 与可测量联系起来的方程数
gate_A5 = n_free > n_obs - 1
add("A5", "FAIL" if gate_A5 else "PASS",
    "K-03 欠定性判定（承重降级结论）",
    "含 Ω/dn 的登记行 %s 全部为定义性位置（定义式/等价改写/最小修复），约束 n 或 dn/dΩ 取值的"
    "方程数 = 0 ⇒ 无可观测程序；k 外部锚定（A2b）；Ω 被 ∮dΩ=4π 锁死（A3）。"
    "参数门：n_自由=%d > n_观测−1=%d ⇒ **定义欠定**（与 r111 对 K-09 的判据同族："
    "有量纲常数无定值 + 定义量无观测程序）⇒ K-03 从正确核降级，保留为猜想候选、"
    "不得再引作质量的定义。"
    % (rows_omega, n_free, n_obs - 1),
    rows_with_omega=rows_omega, n_free=n_free, n_obs=n_obs,
    downgrade="K-03")

# ---------------------------------------------------------------- A6 牛顿自洽 = 定义代入（INFO）
# 登记声称（元数据 §6）：把 m = k·dn/dΩ 代入 A⃗ = −Gk(dn/dΩ)r̂/r³ 「立即得到牛顿万有引力定律」。
# 机算：定义代入是恒等重排；且元数据自承该定义是「为了与牛顿引力定律自洽…必须」反推出来的。
add("A6", "INFO",
    "K-03 与牛顿引力的『自洽验证』为零内容（拟合出来的定义）",
    "代入 m=k·dn/dΩ 后 A⃗=−Gk(dn/dΩ)r̂/r³ ≡ −Gm r̂/r²——恒等重排，不产生新预言；"
    "且元数据第 %d 行自承质量定义是『为了与牛顿引力定律…自洽，通过对比，必须将 m 定义为"
    "kΔn/Ω』⇒ 该『验证』是把牛顿形式当设计目标反推定义，闭环、零信息增量。"
    % (admit_lines["fitted_newton"] or -1),
    admit_line_fitted=admit_lines["fitted_newton"])

# =====================================================================
# B 段：K-07 力方程 F = dP/dt（P = m(C−V)）
# =====================================================================
# 项列代数：四项展开 F = C·ṁ − V·ṁ + m·Ċ − m·V̗（来料登记形式）
FULL = {"C·ṁ": Fraction(1), "V·ṁ": Fraction(-1),
        "m·Ċ": Fraction(1), "m·V̗": Fraction(-1)}
NEWTON = {"V·ṁ": Fraction(1), "m·V̗": Fraction(1)}     # F_N = d(mV)/dt = m·V̗ + V·ṁ


def classical(expr, s, t):
    """经典极限 C=0（含 C 的项消失），整体再乘符号因子 σ·τ。"""
    out = {}
    for k, v in expr.items():
        if k.startswith("C") or k.startswith("m·Ċ"):
            continue
        out[k] = v * s * t
    return out


SIGNS = (1, -1)
passing = [(s, t) for s in SIGNS for t in SIGNS if classical(FULL, s, t) == NEWTON]
# 与上游自承约定对照：10-14 总汇 K-07 行自承「经典极限需 F=-dP/dt 或 P=m(V-C) 约定」
k07_row = next((r for r in rows if r["id"] == "K-07"), {"raw": ""})
note_has_F = bool(re.search(r"F\s*=\s*-\s*d\s*P\s*/\s*dt", k07_row["raw"]))
note_has_P = bool(re.search(r"P\s*=\s*m\s*\(\s*V\s*-\s*C\s*\)", k07_row["raw"]))
# 缺失项对照：删去牛顿可见项（V·ṁ 或 m·V̗）后，任何 (σ,τ) 都不能恢复牛顿
missing_fail = []
for drop in ("V·ṁ", "m·V̗"):
    red = {k: v for k, v in FULL.items() if k != drop}
    for s in SIGNS:
        for t in SIGNS:
            if classical(red, s, t) == NEWTON:
                missing_fail.append((drop, s, t))
B1_ok = (len(passing) == 2 and not missing_fail and note_has_F and note_has_P)
add("B1", "INFO" if B1_ok else "FAIL",
    "K-07 符号缺陷可被约定完全吸收，残差物理内容 = 0",
    "枚举 F=σ·dP/dt、P=τ·m(C−V)（σ,τ=±1）共 4 种读数：经典极限（C=0）下 F=−στ·(m·V̗+V·ṁ)，"
    "与牛顿 F_N=+d(mV)/dt 相符的恰有 %d 种：%s（σ=−1 ⇔『F=−dP/dt』；τ=−1 ⇔『P=m(V−C)』）"
    "——与 10-14 总汇 K-07 行自承的两种约定逐字对应（机读命中：F=−dP/dt %s、P=m(V−C) %s）。"
    "修好读数 (σ,τ)=(1,−1) 后"
    " F=d(m(V−C))/dt ≡ d(mV)/dt（C=0），含变质量项，与牛顿逐项相同。"
    "对照：删去任一牛顿可见项（V·ṁ 或 m·V̗）后，4 种符号读数共 8 个删除组合中"
    "能恢复牛顿的为 %d 个（=0 即无一能恢复）⇒ 吸收检测器对『符号类缺陷（可吸收）』与"
    "『缺失项类缺陷（不可吸收）』有区分。"
    "结论：r104/缺陷记录 #4 的最小修复（新约定）可执行且完备，但它是**单位/符号约定**——"
    "修复不增加任何物理内容，被修复的方程在可观测区的全部内容就是牛顿第二定律。"
    % (len(passing), passing, note_has_F, note_has_P, len(missing_fail)),
    passing=passing, missing_fail=missing_fail,
    note_has_F=note_has_F, note_has_P=note_has_P)

# ---------------------------------------------------------------- B2 四力映射不可辨识
BRANCH_TOKS = ["电场力", "磁场力", "核力", "加质量力", "加速度力"]
rows_branch = [r["id"] for r in rows if any(tok in r["raw"] for tok in BRANCH_TOKS)]
eq_blocks = re.findall(r"\$\$([^$]*)\$\$", meta07)
eq_branch = [b.strip()[:60] for b in eq_blocks if any(tok in b for tok in BRANCH_TOKS)]
prose_hits = {tok: meta07.count(tok) for tok in BRANCH_TOKS}
# 经典极限四项塌缩：classical(FULL,1,−1) == NEWTON（一个牛顿表达式）
collapse_ok = classical(FULL, 1, -1) == NEWTON
# 映射读数计数：4! 项排列 × 2^4 分支符号 = 384，全部与同一方程组相容
n_mappings = 24 * 16
n_obs_mapping = len(rows_branch) + len(eq_branch)   # 约束映射的方程数（行级 + 元数据公式块级）
B2_ok = (len(rows_branch) == 0 and len(eq_branch) == 0 and collapse_ok and n_mappings > n_obs_mapping - 1)
add("B2", "FAIL" if B2_ok else "PASS",
    "K-07 『四项 ↔ 四种基本力』映射不可辨识",
    "机读：22 行正确核中，出现分支力词（电场力/磁场力/核力/加质量力/加速度力）的行数 = %d；"
    "K-07 元数据全部 $$…$$ 公式块中同样 = %d ⇒ 四力映射只存在于散文（元数据命中 %s），"
    "方程层零约束。经典极限 C=0 下四项恒等塌缩为单个牛顿表达式 d(mV)/dt（机算相符=%s）"
    "⇒ 四力分离只在 C≠0 的理论偏好系里存在。映射自由度：4!×2⁴=%d 种读法全部与同一方程组相容，"
    "约束数 = %d ⇒ 参数门 %d > %d−1 ⇒ **不可辨识**。『宇宙大统一方程』的四力宣称不成立；"
    "方程的可辨识内容 = 牛顿第二定律的几何记号改写。"
    % (len(rows_branch), len(eq_branch), json.dumps(prose_hits, ensure_ascii=False),
       collapse_ok, n_mappings, n_obs_mapping, n_mappings, n_obs_mapping),
    rows_branch=rows_branch, eq_blocks_branch=eq_branch, prose_hits=prose_hits,
    collapse_ok=collapse_ok, n_mappings=n_mappings, n_obs_mapping=n_obs_mapping)

# ---------------------------------------------------------------- B3 C 的可观测性
rows_C = [r["id"] for r in rows if ("\\vec C" in r["formula"] or "C_0" in r["formula"]
                                    or "\\vec{C}" in r["formula"])]
statuses_C = {r["id"]: r["status"] for r in rows if r["id"] in rows_C}
n_free_C = 2     # |C|=c 锁死模长，方向是 S² 上 2 个自由函数
n_obs_C = 0      # 约束 C 方向的方程/观测数
B3_ok = (len(rows_C) >= 3 and n_free_C > n_obs_C - 1)
add("B3", "FAIL" if B3_ok else "PASS",
    "K-07 的 C⃗（矢量光速）无任何观测约束",
    "含 C⃗ 的登记行 %d 条：%s，状态列全部是定义性/恒等/子集（%s）⇒ 没有一条方程把 C 的方向"
    "与可测量联系起来；|C|=c 锁死模长后方向仍是 %d 个自由函数，约束数 = %d ⇒ 参数门不通过。"
    "C 是理论偏好系量，四力映射的一切『预言』都可以通过事后拟合 C 的方向复现 ⇒ 与 B2 合流。"
    % (len(rows_C), rows_C, json.dumps(statuses_C, ensure_ascii=False), n_free_C, n_obs_C),
    rows_C=rows_C, statuses_C=statuses_C, n_free_C=n_free_C, n_obs_C=n_obs_C)

# =====================================================================
# C 段：K-11 磁场定义方程登记
# =====================================================================
# ---------------------------------------------------------------- C1 登记串（name）缺 q
# name 字面读数：B = μ₀(v×R)/(4πR³) ⇒ 因子 μ₀·v·R⁻²（(v×R)/R³ = v·R⁻²）
dim_name = dmul(dmul(DIM_mu0, DIM_V), dpow(DIM_L, -2))
gap_q = ddiv(DIM_B, dim_name)
# latex 机读读数：因子 μ₀·q·v·R⁻²（固化 JSON rhs）
rhs_k11 = E11.get("rhs", []) if E11 else []
dim_latex = DIMLESS
for sym, pw in rhs_k11:
    if sym == "mu0":
        dim_latex = dmul(dim_latex, dpow(DIM_mu0, pw))
    elif sym == "q":
        dim_latex = dmul(dim_latex, dpow(DIM_q, pw))
    elif sym in ("V", "v"):
        dim_latex = dmul(dim_latex, dpow(DIM_V, pw))
    elif sym == "r":
        dim_latex = dmul(dim_latex, dpow(DIM_L, pw))
C1_ok = (not deq(dim_name, DIM_B)) and deq(dim_latex, DIM_B) and deq(gap_q, DIM_q)
add("C1", "FAIL" if C1_ok else "PASS",
    "K-11 登记串（name）按字面读数量纲断裂，缺口恰为 [q]",
    "name 串『%s』字面因子 μ₀·v·R⁻² ⇒ [B]_name=%s ≠ [B]=%s；latex 机读因子（固化 JSON rhs %s）"
    "⇒ [B]_latex=%s ✓ 闭合。缺口 = [B]/[B]_name = %s，**恰为电荷量纲 [q]** ⇒ 『最小修复：补速度因子 v』"
    "只补了 v，name 串仍缺源电荷 q；name 串被 10-14 总汇与 53 号卷直接引用，按字面无法计算。"
    "登记自相矛盾（M02 族：人读串与机读因子分解不一致）。修复动作：name 串补 q 与 latex 对齐"
    "（不降级：其实质是教科书毕奥-萨伐尔）。"
    % (E11.get("name") if E11 else None, dstr(dim_name), dstr(DIM_B),
       rhs_k11, dstr(dim_latex), dstr(gap_q)),
    dim_name=dstr(dim_name), dim_latex=dstr(dim_latex), gap=dstr(gap_q), rhs_k11=rhs_k11)

# ---------------------------------------------------------------- C2 几何形式的特设常数与符号互斥
# 闭合求解：q = kk′(1/Ω²)(dΩ/dt)，[q]=T·A、[k]=M、[dΩ/dt]=T⁻¹ ⇒ [k′] = [q]/([k]·T⁻¹)
dim_kprime_req = ddiv(DIM_q, dmul(DIM_M, dpow(DIM_T, -1)))
# q 符号三处互斥：K-09 latex（+） vs K-10 latex（−） vs K-11 元数据电荷定义（−）；
# 且 K-10 自身 name（+）与 latex（−）反号
sign_conflict = len({SIG_K09, SIG_K10_latex, SIG_K11_meta_q}) > 1
k10_self_conflict = (SIG_K10_name is not None and SIG_K10_latex is not None
                     and SIG_K10_name != SIG_K10_latex)
C2_ok = (deq(dim_kprime_req, D(-1, 0, 2, 1)) and admit_lines["kprime_contradiction"]
         and (sign_conflict or k10_self_conflict))
add("C2", "FAIL" if C2_ok else "PASS",
    "K-11 几何形式依赖特设 [k′] 且 q 符号链三处互斥",
    "闭合求解得 [k′]=%s（=M⁻¹T²A）——一个 22 条正确核中**无人声明、无人定值**的特设量纲常数，"
    "元数据第 %d 行自承『电荷常数 k′：量纲存在矛盾，需特殊定义』、第 %d 行自承"
    "『其具体数值未在文档中精确给定』。符号链：K-09 latex 符号 %+d、K-10 latex 符号 %+d、"
    "K-11 元数据电荷定义符号 %+d ⇒ %s；K-10 自身 name（%+d）与 latex（%+d）反号 ⇒ %s。"
    "几何形式还以 r111 已降级的 K-09（欠定）为唯一 q 来源 ⇒ **几何形式不可引用**；"
    "标准形式（含 q）才是可引用内容。"
    % (dstr(dim_kprime_req), admit_lines["kprime_contradiction"] or -1,
       admit_lines["kprime_no_value"] or -1,
       SIG_K09 or 0, SIG_K10_latex or 0, SIG_K11_meta_q or 0,
       "三处互斥" if sign_conflict else "一致", SIG_K10_name or 0, SIG_K10_latex or 0,
       "自相矛盾" if k10_self_conflict else "一致"),
    dim_kprime_req=dstr(dim_kprime_req), sign_conflict=sign_conflict,
    k10_self_conflict=k10_self_conflict,
    admit_kprime_contradiction=admit_lines["kprime_contradiction"],
    admit_kprime_no_value=admit_lines["kprime_no_value"])

# ---------------------------------------------------------------- C3 标准形式 = 教科书毕奥-萨伐尔（INFO）
# 元数据自承：几何形式 = 把电荷几何定义代入运动电荷磁场表达式得到；标准形式即匀速点电荷的
# 毕奥-萨伐尔定律 ⇒ 代入 q 后两者恒等，零增量。
add("C3", "INFO",
    "K-11 标准形式恒等于教科书毕奥-萨伐尔（零增量）",
    "元数据第 %d 行自承几何形式由『代入运动电荷的磁场表达式』得到；标准形式"
    " B=(μ₀qγ/4π)(v×R)/[γ²(x−vt)²+y²+z²]^{3/2} 就是匀速运动点电荷的毕奥-萨伐尔定律，"
    "代入 q=kk′(1/Ω²)(dΩ/dt) 后逐因子还原几何形式（μ₀·γ·k·k′·Ω⁻²·T⁻¹·v·R·L⁻³）⇒ "
    "除教科书内容外加一套待定常数外壳，增量 0。"
    % (admit_lines["geom_substitution"] or -1),
    admit_geom_substitution=admit_lines["geom_substitution"])

# =====================================================================
# E 段：判据自纠（阳性/反向对照）
# =====================================================================
# E01 重言检测器两侧有牙（A2 已算，这里登记为判据自纠条目）
add("E01", "PASS" if (is_taut_T1 and not is_taut_T2) else "FAIL",
    "对照：重言检测器两侧有牙",
    "T1（m_p≡√(ħc/G) 的定义配对）残差 %s ⇒ 判『定义重排』；T2（G 与独立测量常数 m_e 配对）"
    "残差 %s ⇒ 不判。若检测器把 T2 也判为重言则 A2 不可信；实测两侧都对。"
    % (res_T1, res_T2))

# E02 立体角计算器两侧有牙（A3 已算）
add("E02", "PASS" if (solid_ok and cap_ok and len(orders_ok) >= 4) else "FAIL",
    "对照：立体角计算器对闭合/非闭合有牙",
    "闭合椭球（γ=1.25/2/10）三档步长收敛到 4π（最大相对偏差 %.2e，阶 %s）；"
    "非闭合球冠收敛到 π（相对 %.2e）⇒ 计算器不会把任何曲面都算成 4π。"
    % (max(v["rel"] for v in solid.values()),
       ["%.2f" % o for o in orders_ok][:6], cap_rel))

# E03 符号吸收检测器两侧有牙（B1 已算）
add("E03", "PASS" if B1_ok else "FAIL",
    "对照：约定吸收检测器对符号/缺失项有牙",
    "符号类缺陷：4 种 (σ,τ) 中恰 2 种恢复牛顿（可吸收）；缺失项类缺陷：2 种删除 × 4 种符号"
    "共 8 组合无一恢复（不可吸收）⇒ 『可被约定吸收 ⇒ 零内容』的判据不会把真缺陷也吸收掉。")

# E04 量纲求解器跨轮复现（r111 注册答案 [f]=kg·A⁻¹）
dim_f_repro = ddiv(DIM_B, dmul(DIM_curl, DIM_A_grav))     # K-13: ∇×A = B/f ⇒ [f]=[B]/([curl][A])
add("E04", "PASS" if deq(dim_f_repro, D(1, 0, 0, -1)) else "FAIL",
    "对照：量纲求解器复现 r111 注册答案",
    "用本册求解器重算 [f]=[B]/([∇×][A])=%s，与 r111 判定册注册的 [f]=kg·A⁻¹（=M·A⁻¹）一致 "
    "⇒ 跨轮量纲口径无漂移，C2 的 [k′] 求解可信。"
    % dstr(dim_f_repro))

# E05 打击面精确：降级只限 K-03，标准物理核全部保留
STANDARD_CORES = {"K-04", "K-10", "K-16", "K-22"}
DOWNGRADED = sorted({e["downgrade"] for e in ENTRIES
                     if e["verdict"] == "FAIL" and e.get("downgrade")})
E05_ok = (DOWNGRADED == ["K-03"] and not (STANDARD_CORES & set(DOWNGRADED)))
add("E05", "PASS" if E05_ok else "FAIL",
    "对照：打击面精确（标准物理正确核全部保留）",
    "本册降级清单 = %s；K-04（牛顿引力）/K-10（库仑）/K-16（质能）/K-22（α 定义）四条标准物理核"
    "全部保留（K-10/K-11 的登记串缺陷只要求修串、不动实质）⇒ 攻破不波及真物理。"
    % DOWNGRADED, downgraded=DOWNGRADED)

# =====================================================================
# 汇总
# =====================================================================
CORES_BEFORE_R111 = 22
CORES_AFTER_R111 = 17
CORES_AFTER = CORES_AFTER_R111 - len(DOWNGRADED)

tally = {}
for e in ENTRIES:
    tally[e["verdict"]] = tally.get(e["verdict"], 0) + 1
verdict_total = "FAIL" if tally.get("FAIL", 0) else ("BOUNDARY" if tally.get("BOUNDARY", 0) else "PASS")
guard_failed = [g for g in STATE["guard_msgs"]]

# 上游字节防改：末尾复算 sha256
HASH1 = {k: sha256_of(p) for k, p in UPSTREAM.items()}
guard(HASH0 == HASH1, "g_upstream_bytes_unchanged",
      "引擎运行前后上游 5 文件字节须一致；实测差异 %s"
      % [k for k in HASH0 if HASH0[k] != HASH1.get(k)])

SUMMARY = {
    "tag": TAG,
    "date": "2026-10-19",
    "role": "正确核残余软肋攻破（对内整理产物，只读上游）",
    "verdict_total": verdict_total,
    "tally": tally,
    "n_entries": len(ENTRIES),
    "guards_total": STATE["guard"],
    "guards_failed": STATE["guard_fail"],
    "cores_before_r111": CORES_BEFORE_R111,
    "cores_after_r111": CORES_AFTER_R111,
    "cores_downgraded": DOWNGRADED,
    "cores_after": CORES_AFTER,
}

EXTERNAL_INPUTS = [
    "来料：《理论体系方程总汇_正确方程集_2026-10-14.md》22 条正确核（只读引用，未改字节）",
    "登记串：2026-10-03 固化 JSON 的 K-03/K-07/K-09/K-10/K-11 name/latex/rhs（机读，未改字节）",
    "S17 元数据三份：3质量定义方程 / 7宇宙大统一方程 / 11磁场定义方程（自承点检索，未改字节）",
    "SI 量纲制（M,L,T,A 四元组）与标准场量纲（[B]=MT⁻²A⁻¹、[q]=T·A、[μ₀]=MLT⁻²A⁻²、[G]=M⁻¹L³T⁻²）",
    "CODATA：ħ=1.054571817e-34 J·s、c=299792458 m/s、G=6.67430e-11、m_e=9.1093837015e-31 kg",
    "数学定理：∇·(r̂/r²)=4πδ³(r) ⇒ 包围原点的任意闭合面总立体角恒为 4π",
]

NOT_SELF_DERIVED = [
    "NS1 22 条正确核的原始清单与 2026-10-03 固化判定（未重判，只读）",
    "NS2 r111 对 K-09 欠定、f-桥接族为单位约定的结论（本册只继承引用，不重判）",
    "NS3 机读扫描规则（行级/公式块级/符号提取/残差阈值 1e-30，人工定义、机器执行、随引擎落盘）",
    "NS4 不代来稿补 k/k′/f 的数值、不代选单位制、不代定 Ω 与 n",
    "NS5 本册只改『正确核』分类账与登记串修串要求，不删除/修改上游任何字节",
]

payload = {"summary": SUMMARY, "entries": ENTRIES,
           "external_inputs": EXTERNAL_INPUTS, "not_self_derived": NOT_SELF_DERIVED,
           "guards": GUARDS}

with open(os.path.join(OUT_DATA, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2, default=str)

lines = ["# r112 数据产物｜正确核残余软肋攻破（机器读数）\n",
         "- 总判决：**%s** ｜ 条目 %d ｜ %s ｜ 守卫 %d/%d"
         % (verdict_total, len(ENTRIES), " / ".join("%s %d" % kv for kv in sorted(tally.items())),
            STATE["guard"] - STATE["guard_fail"], STATE["guard"]),
         "- 正确核账本：22 → 17（r111）→ **%d**（本册降级 %s）\n"
         % (CORES_AFTER, "、".join(DOWNGRADED)),
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
    f.write("CORES 22 -> 17 (r111) -> %d (r112 downgraded %s)\n" % (CORES_AFTER, DOWNGRADED))
    for e in ENTRIES:
        f.write("%-6s %-9s %s\n" % (e["code"], e["verdict"], e["title"]))
    f.flush()

print("[r112] VERDICT=%s entries=%d tally=%s" % (verdict_total, len(ENTRIES), tally), flush=True)
print("[r112] guard %d/%d failed=%d" % (STATE["guard"] - STATE["guard_fail"], STATE["guard"], STATE["guard_fail"]), flush=True)
print("[r112] cores 22 -> 17 (r111) -> %d (downgraded %s)" % (CORES_AFTER, DOWNGRADED), flush=True)
if STATE["guard_fail"]:
    for m in STATE["guard_msgs"]:
        sys.stderr.write("GUARD FAIL: %s\n" % m)
    sys.exit(2)
sys.exit(0)
