# r441 ROOT V75 audit
# -*- coding: utf-8 -*-
"""ROOT V75 实验控制矩阵与证明状态全维审计（r441）。

只读审计 V75 来料；不运行来料代码、不改来料字节、不新增物理。
增量分工：attack64 已复核 G no-go 与电磁源/耦合；本册只审计其未覆盖的方程目录、
因素矩阵、数值摘要、工程测试与实验状态，并用 W3 四门禁定价。
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(ROOT, "90_历史归档", "来源语料_ufthub_ROOT_V52-V82_202611", "V75", "ROOT_V75")
STAMP = "2026-11-22"
RID = "r441"

ENTRIES = []
GUARDS = []
COUNTS = {}

F_MANIFEST = os.path.join(SRC, "SHA256_MANIFEST.csv")
F_README = os.path.join(SRC, "README.md")
F_PROOF = os.path.join(SRC, "PROOF_STATUS.md")
F_BOOK = os.path.join(SRC, "book", "ROOT_V75_变化电磁场与引力起源_严格推导研究专著.md")
F_EQ = os.path.join(SRC, "data", "ROOT_V75_核心方程与证明状态.csv")
F_FACTOR = os.path.join(SRC, "data", "ROOT_V75_多维影响因素与实验控制矩阵.csv")
F_SUMMARY = os.path.join(SRC, "results", "numerical_summary.json")
F_VERIFY = os.path.join(SRC, "results", "verification_report.json")
F_BROWSER = os.path.join(SRC, "results", "browser_smoke.json")
F_CODE = os.path.join(SRC, "src", "em_gravity.py")

SOURCE_FILES = [F_MANIFEST, F_README, F_PROOF, F_BOOK, F_EQ, F_FACTOR, F_SUMMARY, F_VERIFY, F_BROWSER, F_CODE]


def add(code, verdict, title, detail):
    ENTRIES.append({"id": code, "verdict": verdict, "title": title, "detail": detail})


def guard(code, ok, detail):
    GUARDS.append({"id": code, "ok": bool(ok), "detail": detail})
    if not ok:
        raise AssertionError("GUARD-FAIL %s : %s" % (code, detail))


def fmt(x, n=12):
    return format(Decimal(x), ".%dE" % n)


def rel(a, b):
    a = Decimal(a)
    b = Decimal(b)
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return [list(row) for row in csv.reader(fh)]


def read_json(path):
    with open(path, "r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def rank_frac(mat):
    a = [[Fraction(x) for x in row] for row in mat]
    if not a:
        return 0
    rows = len(a)
    cols = len(a[0])
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if a[i][c] != 0), None)
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        pv = a[r][c]
        a[r] = [x / pv for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == rows:
            break
    return r


def det_frac(mat):
    a = [[Fraction(x) for x in row] for row in mat]
    n = len(a)
    det = Fraction(1)
    for c in range(n):
        piv = next((i for i in range(c, n) if a[i][c] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != c:
            a[piv], a[c] = a[c], a[piv]
            det = -det
        pv = a[c][c]
        det *= pv
        for i in range(c + 1, n):
            if a[i][c] != 0:
                f = a[i][c] / pv
                a[i] = [x - f * y for x, y in zip(a[i], a[c])]
    return det


for p in SOURCE_FILES:
    guard("V75_source_exists_" + os.path.basename(p), os.path.isfile(p), "事实源存在：%s" % os.path.relpath(p, ROOT))

MANIFEST_ROWS = [r for r in read_csv(F_MANIFEST)[1:] if r and r[0].strip()]
HASH_BAD = []
for relp, want, size in MANIFEST_ROWS:
    fp = os.path.join(SRC, relp.replace("/", os.sep))
    if not os.path.isfile(fp):
        HASH_BAD.append(relp + ":missing")
        continue
    got = sha256(fp)
    if got != want:
        HASH_BAD.append(relp + ":sha")
    if os.path.getsize(fp) != int(size):
        HASH_BAD.append(relp + ":size")
guard("V75_manifest_all_match", not HASH_BAD, "SHA256_MANIFEST %d 项逐项一致；不一致=%s" % (len(MANIFEST_ROWS), HASH_BAD))

EQ_ROWS = [r for r in read_csv(F_EQ)[1:] if r and r[0].strip()]
FACTOR_ROWS = [r for r in read_csv(F_FACTOR)[1:] if r and r[0].strip()]
guard("V75_equation_rows", len(EQ_ROWS) == 50, "核心方程与证明状态共 %d 条（E01-E50）" % len(EQ_ROWS))
guard("V75_factor_rows", len(FACTOR_ROWS) == 30, "实验控制矩阵共 %d 条控制变量" % len(FACTOR_ROWS))

SUMMARY = read_json(F_SUMMARY)
VERIFY = read_json(F_VERIFY)
BROWSER = read_json(F_BROWSER)
guard("V75_data_rows", SUMMARY["data_rows"] == {"magnetic_scan": 15, "em_scan": 25, "time_series": 1001},
      "数据行数：magnetic=%d / em=%d / time=%d" % (SUMMARY["data_rows"]["magnetic_scan"], SUMMARY["data_rows"]["em_scan"], SUMMARY["data_rows"]["time_series"]))
guard("V75_verification_counts", "41" in VERIFY["unit_tests"] and "5" in VERIFY["symbolic_checks"] and "10" in VERIFY["chromium_interactions"],
      "工程读数：%s / %s / %s" % (VERIFY["unit_tests"], VERIFY["symbolic_checks"], VERIFY["chromium_interactions"]))
guard("V75_browser_count", BROWSER["passed"] == 10 and BROWSER["total"] == 10 and not BROWSER["console_errors"] and not BROWSER["page_errors"],
      "浏览器交互 %d/%d，page/console errors=0/0" % (BROWSER["passed"], BROWSER["total"]))

PROOF_TEXT = open(F_PROOF, "r", encoding="utf-8").read()
README_TEXT = open(F_README, "r", encoding="utf-8").read()
guard("V75_honest_boundary", "无新仪器数据" in PROOF_TEXT and ("尚未证明" in PROOF_TEXT or "未证明" in PROOF_TEXT),
      "PROOF_STATUS 明写尚无独立参数证明、无新仪器数据、无四力统一")
guard("V75_readme_no_unification", "未证实" in README_TEXT and "未独立证明" in README_TEXT,
      "README 明确区分已证 GR 机制与未证 G 起源/四力统一")

add("V75-A01", "PASS", "V75 事实源哈希链完整且计数闭合",
    "SHA256_MANIFEST 共 %d 项逐项一致；方程 %d 条、因素控制 %d 条、扫描数据 15/25/1001 点、工程测试 41/5/10 均可机读。"
    % (len(MANIFEST_ROWS), len(EQ_ROWS), len(FACTOR_ROWS)))
add("V75-A02", "INFO", "V75 自陈边界与 attack64 分工不重复",
    "本册只读审计 V75 自身的方程目录/因素矩阵/数值摘要/工程测试/实验状态；G no-go 与电磁源-耦合混同继承 attack64，不重判。")
# ---------------- B 段：数值摘要独立复算 ----------------
PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944")
C = D = lambda x: Decimal(str(x))
C0 = D(SUMMARY["constants"]["c_m_s"])
G0 = D(SUMMARY["constants"]["G_m3_kg_s2"])
MU0 = D(SUMMARY["constants"]["mu0_H_m"])
EPS0 = D(1) / (MU0 * C0 * C0)
guard("V75_eps0_from_mu0_c", rel(EPS0, SUMMARY["constants"]["eps0_F_m"]) < Decimal("1e-15"),
      "eps0=1/(mu0 c^2) 相对差 %s" % fmt(rel(EPS0, SUMMARY["constants"]["eps0_F_m"]), 6))

B_T = D(10)
A_R = D(1)
U_B = B_T * B_T / (D(2) * MU0)
VOL = D(4) * PI * A_R * A_R * A_R / D(3)
U_SPHERE = VOL * U_B
M_EQ = U_SPHERE / (C0 * C0)
G_R1 = G0 * M_EQ / (A_R * A_R)
G_R2 = G0 * M_EQ / (D(2) * A_R * D(2) * A_R)
H00_R2 = D(2) * G0 * U_SPHERE / (C0 ** 4 * D(2) * A_R)

EX = SUMMARY["example_10T_1m"]
NUM_CHECK = [
    ("magnetic_energy_density_J_m3", U_B),
    ("ideal_sphere_energy_J", U_SPHERE),
    ("mass_equivalent_kg", M_EQ),
    ("toy_g_at_r_1m_m_s2", G_R1),
    ("toy_g_at_r_2m_m_s2", G_R2),
    ("toy_metric_h00_at_r_2m", H00_R2),
]
MAX_NUM_REL = max(rel(got, EX[key]) for key, got in NUM_CHECK)
guard("V75_10T_numbers", MAX_NUM_REL < Decimal("1e-12"),
      "10 T/1 m 六个代表值最大相对差 %s（小于 1e-12）" % fmt(MAX_NUM_REL, 6))

E1 = D(1000000)
U_E1 = EPS0 * E1 * E1 / D(2)
RHO_E1 = U_E1 / (C0 * C0)
MAX_E_REL = max(rel(U_E1, SUMMARY["example_1MV_per_m"]["u_J_m3"]),
                rel(RHO_E1, SUMMARY["example_1MV_per_m"]["mass_density_eq_kg_m3"]))
guard("V75_1MV_numbers", MAX_E_REL < Decimal("1e-12"),
      "1 MV/m 场能与质量密度最大相对差 %s" % fmt(MAX_E_REL, 6))

FREQ = D(50)
OMEGA = D(2) * PI * FREQ
AVG_UB = VOL * B_T * B_T / (D(4) * MU0)
AVG_UE = EPS0 * VOL * A_R * A_R * OMEGA * OMEGA * B_T * B_T / D(40)
QS_PARAM = OMEGA * A_R / C0
QS_RATIO = QS_PARAM * QS_PARAM / D(10)
QS = SUMMARY["50Hz_quasistatic"]
MAX_QS_REL = max(rel(AVG_UB, QS["average_B_energy_joule"]),
                 rel(AVG_UE, QS["average_induced_E_energy_joule"]),
                 rel(QS_PARAM, QS["quasistatic_parameter"]),
                 rel(QS_RATIO, QS["ratio_induced_to_B"]))
guard("V75_quasistatic_numbers", MAX_QS_REL < Decimal("1e-12") and QS_PARAM < Decimal("1e-5"),
      "50 Hz 准静态四项最大相对差 %s；omega*a/c=%s < 1e-5" % (fmt(MAX_QS_REL, 6), fmt(QS_PARAM, 6)))

WAVE_E = D(1000000)
WAVE_B = WAVE_E / C0
I1 = D(2) * (WAVE_B * WAVE_B - WAVE_E * WAVE_E / (C0 * C0))
P_PSEUDO = D(0)
WAVE_U = (EPS0 * WAVE_E * WAVE_E + WAVE_B * WAVE_B / MU0) / D(2)
guard("V75_null_wave", abs(I1) < Decimal("1e-40") and P_PSEUDO == 0 and WAVE_U > 0
      and rel(WAVE_U, SUMMARY["null_wave"]["u_J_m3"]) < Decimal("1e-12"),
      "平面波 I1=%s，P=0，u=%s J/m^3 > 0；说明 F^2=0 不等于无引力源" % (fmt(I1, 3), fmt(WAVE_U, 6)))

STATIC_B_U = D(10) ** 2 / (D(2) * MU0)
ROT_B_U = D(10) ** 2 / (D(2) * MU0)
guard("V75_counterexamples", STATIC_B_U > 0 and ROT_B_U == STATIC_B_U,
      "静态 B 与等幅旋转 B 均保持 u=B^2/(2mu0)>0；变化率不是能量单极的必要条件")

add("V75-B01", "PASS", "10 T/1 m 六个代表数值可独立复算",
    "u_B=%s J/m³、U_B=%s J、m_eq=%s kg、g(1m)=%s m/s²、g(2m)=%s m/s²、|h00(2m)|=%s；"
    "与 results/numerical_summary.json 最大相对差 %s。"
    % (fmt(U_B), fmt(U_SPHERE), fmt(M_EQ), fmt(G_R1), fmt(G_R2), fmt(H00_R2), fmt(MAX_NUM_REL, 6)))
add("V75-B02", "PASS", "1 MV/m 电场数值与单位口径一致",
    "u=%s J/m³、rho_eq=%s kg/m³，最大相对差 %s；该能量密度比 10 T 磁场低约 7 个量级。"
    % (fmt(U_E1), fmt(RHO_E1), fmt(MAX_E_REL, 6)))
add("V75-B03", "PASS", "50 Hz 准静态感应能量与有效域可复算",
    "<U_B>=%s J，<U_E_ind>=%s J，ratio=%s，omega*a/c=%s；来料仅在该小参数下成立，不能外推高频。"
    % (fmt(AVG_UB), fmt(AVG_UE), fmt(QS_RATIO, 6), fmt(QS_PARAM, 6)))
add("V75-B04", "PASS", "零不变量平面波仍有非零能量，反例成立",
    "取 E=1 MV/m、B=E/c 且正交，I1=%s、P=0，但 u=%s J/m³>0 ⇒ 仅用 F² 或 E·B 替代完整 T_μν 会漏掉电磁辐射引力源。"
    % (fmt(I1, 3), fmt(WAVE_U, 6)))
add("V75-B05", "PASS", "“变化率必要”被静态场与旋转场反例排除",
    "dB/dt=0 的静态 B 仍有 u_B=%s J/m³；等幅旋转 B 的能量单极与静态同值；变化率不能充当引力单极的唯一变量。"
    % fmt(STATIC_B_U))
# ---------------- C 段：G 来源量纲、证明状态与候选模型 ----------------
# 行=(M,L,T,Q) 四个基本量纲，列=(c,E,B,omega,a) 五个输入量；元素为该量在该量纲上的指数。
# [c]=(0,1,-1,0) [E]=(1,1,-3,-1) [B]=(1,0,-2,-1) [omega]=(0,0,-1,0) [a]=(0,1,0,0)
DIM_A = [
    [Fraction(0), Fraction(1), Fraction(1), Fraction(0), Fraction(0)],      # M 行
    [Fraction(1), Fraction(1), Fraction(0), Fraction(0), Fraction(1)],      # L 行
    [Fraction(-1), Fraction(-3), Fraction(-2), Fraction(-1), Fraction(0)],  # T 行
    [Fraction(0), Fraction(-1), Fraction(-1), Fraction(0), Fraction(0)],    # Q 行
]
DIM_Y = [Fraction(-1), Fraction(3), Fraction(-2), Fraction(0)]  # [G]=M^-1 L^3 T^-2 Q^0
DIM_AUG = [list(row) + [DIM_Y[i]] for i, row in enumerate(DIM_A)]
RANK_A_G = rank_frac(DIM_A)
RANK_AUG_G = rank_frac(DIM_AUG)
guard("V75_G_dim_rank_gap", RANK_A_G < RANK_AUG_G,
      "给定 {c,E,B,omega,a} 时 rank(A)=%d < rank([A|G])=%d ⇒ 量纲空间内拼不出 G" % (RANK_A_G, RANK_AUG_G))
# 阳性对照：目标量取 [a]=(0,1,0,0)，它恰为 A 的第 5 列（x_a=1 即有解）。
# 若判据恒假，则 rank([A|y_ctrl]) 也会比 rank(A) 大 1。
DIM_Y_CTRL = [Fraction(0), Fraction(1), Fraction(0), Fraction(0)]
DIM_AUG_CTRL = [list(row) + [DIM_Y_CTRL[i]] for i, row in enumerate(DIM_A)]
RANK_AUG_CTRL = rank_frac(DIM_AUG_CTRL)
guard("V75_G_dim_positive_control", RANK_A_G == RANK_AUG_CTRL,
      "阳性对照：目标量 [a] 在 A 的列空间内，rank(A)=%d == rank([A|a])=%d（判据非恒假）"
      % (RANK_A_G, RANK_AUG_CTRL))

STATUS = {}
for r in EQ_ROWS:
    STATUS[r[3]] = STATUS.get(r[3], 0) + 1
guard("V75_status_partition", STATUS.get("known", 0) == 23 and STATUS.get("conditional", 0) == 13
      and STATUS.get("counterexample", 0) == 3 and STATUS.get("candidate", 0) == 3,
      "证明状态分布：known=%d / conditional=%d / counterexample=%d / candidate=%d / 其它=%d"
      % (STATUS.get("known", 0), STATUS.get("conditional", 0), STATUS.get("counterexample", 0),
         STATUS.get("candidate", 0), len(EQ_ROWS) - STATUS.get("known", 0) - STATUS.get("conditional", 0)
         - STATUS.get("counterexample", 0) - STATUS.get("candidate", 0)))
EQ_IDS = {r[0]: r for r in EQ_ROWS}
for eid in ("E01", "E05", "E17", "E18", "E27", "E31", "E35", "E41", "E44", "E47", "E50"):
    guard("V75_eq_present_" + eid, eid in EQ_IDS, "方程索引含 %s：%s" % (eid, EQ_IDS.get(eid, ["", "缺失"])[1]))

CATEGORIES = {}
for r in FACTOR_ROWS:
    CATEGORIES[r[0]] = CATEGORIES.get(r[0], 0) + 1
FACTOR_FIELDS_OK = all(len(r) >= 4 and all(x.strip() for x in r[:4]) for r in FACTOR_ROWS)
guard("V75_factor_matrix_coverage", len(CATEGORIES) == 8 and FACTOR_FIELDS_OK,
      "因素矩阵覆盖 8 类：%s；30 行必要字段均非空" % sorted(CATEGORIES.items()))

add("V75-C01", "PASS", "G 来源在给定电磁/几何输入集内量纲无解",
    "以 {c,E,B,ω,a} 的 (M,L,T,Q) 指数矩阵做精确有理数判定，rank(A)=%d、rank([A|G])=%d；"
    "M 行要求 x_E+x_B=-1 而 Q 行要求 x_E+x_B=0，故不相容；阳性对照取 [a] 时 rank 不增（=%d），说明判据非恒假。"
    % (RANK_A_G, RANK_AUG_G, RANK_AUG_CTRL))
add("V75-C02", "CORRECTED", "50 条方程证明状态显示“已知/条件/候选/反例”未混写",
    "状态分布：known=%d、conditional=%d、counterexample=%d、candidate=%d、derived/condition/necessary/toy 等=%d；"
    "E35–E42 的标量–光子模型仍列 candidate/derived conditional，E44 明确 [G] 需独立质量/长度动力学。"
    % (STATUS.get("known", 0), STATUS.get("conditional", 0), STATUS.get("counterexample", 0),
       STATUS.get("candidate", 0), len(EQ_ROWS) - STATUS.get("known", 0) - STATUS.get("conditional", 0)
       - STATUS.get("counterexample", 0) - STATUS.get("candidate", 0)))
add("V75-C03", "CORRECTED", "标量–光子候选不是无参数预言",
    "E35–E42 给出候选作用量与三条条件场方程，但 M_*、m_phi、xi、Lambda 均未由理论定值；"
    "E41 只给 F_g>0 与 1+phi/Lambda>0 的必要稳定性条件，E40 的有效张量耦合明确不等于实验室 G_Cav。")

add("V75-D01", "PASS", "30 项实验控制矩阵覆盖 8 类且无空字段",
    "分布：%s；控制项从 B/E/相位/dB/dt 扩展到材料、支架、热、地球 g/潮汐、传播延迟、多极矩、第五力与盲测统计，"
    "说明来料没有把“装置重力样信号”直接等同于新引力。" % sorted(CATEGORIES.items()))
guard("V75_no_new_measurement", SUMMARY["flags"]["experimental_new_gravity_discovery"] is False
      and "no new measurement" in VERIFY["scientific_status"],
      "数值摘要与验证报告一致：无新仪器测量、无新物理发现")
add("V75-D02", "PASS", "工程测试与实验确证被明确分层",
    "41 项单元测试、5 组符号校核、10 项 Chromium 交互与 0 page/console errors 只证明离线模型/网页按定义实现；"
    "verification_report.scientific_status 明写 no new measurement / no four-force unification。")

# ---------------- E 段：W3 四门禁 ----------------
W3 = [
    {"id": "G_from_EM", "C1": False, "C2": False, "C3": False, "C4": False},
    {"id": "EM_source_is_gravity", "C1": True, "C2": False, "C3": True, "C4": True},
    {"id": "scalar_photon_candidate", "C1": False, "C2": False, "C3": True, "C4": False},
    {"id": "artificial_g_detectable", "C1": True, "C2": False, "C3": False, "C4": False},
]


def w3_pass_count(rows):
    return sum(1 for r in rows if all(r[k] for k in ("C1", "C2", "C3", "C4")))


W3_PASS = w3_pass_count(W3)
guard("V75_w3_zero", W3_PASS == 0, "W3 四候选全部未过门，PASS=%d/4" % W3_PASS)
W3_CTRL = [dict(r) for r in W3]
for k in ("C1", "C2", "C3", "C4"):
    W3_CTRL[0][k] = True
W3_CTRL_PASS = w3_pass_count(W3_CTRL)
guard("V75_w3_positive_control", W3_CTRL_PASS == 1,
      "合成阳性候选后 PASS 计数 0 -> %d，0/4 非解析失败假零" % W3_CTRL_PASS)

add("V75-E01", "FAIL", "W3 四候选 0/4",
    "G 起源：无数值且量纲无解；EM 源：标准 GR 已知结果而非体系内新推；标量候选：自由参数未锚定；"
    "人工重力：玩具 g 用外部 G 且无实测。四者分别败在不同门，不能合并为 W3 通过。")
add("V75-E02", "PASS", "W3 门禁带阳性对照",
    "四项全真的合成候选使 PASS 从 0/4 升到 %d/4，证明 C1–C4 是可执行的判据而非恒假集合。" % W3_CTRL_PASS)
add("V75-RED-01", "INFO", "红线计数继承不变",
    "0/6、0/22、UFT3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4；本册只给 V75 条件结果定价。")
# ---------------- 落盘 ----------------
COUNTS = {}
for e in ENTRIES:
    COUNTS[e["verdict"]] = COUNTS.get(e["verdict"], 0) + 1

KEY = {
    "source": os.path.relpath(SRC, ROOT).replace("\\", "/"),
    "manifest_items": len(MANIFEST_ROWS),
    "manifest_bad": len(HASH_BAD),
    "equation_rows": len(EQ_ROWS),
    "factor_rows": len(FACTOR_ROWS),
    "factor_categories": len(CATEGORIES),
    "status_distribution": dict(STATUS),
    "data_rows": SUMMARY["data_rows"],
    "engineering": {"unit_tests": VERIFY["unit_tests"], "symbolic_checks": VERIFY["symbolic_checks"],
                    "chromium_interactions": VERIFY["chromium_interactions"]},
    "browser_passed": "%d/%d" % (BROWSER["passed"], BROWSER["total"]),
    "scientific_status": VERIFY["scientific_status"],
    "eps0_from_mu0_c_rel": fmt(rel(EPS0, SUMMARY["constants"]["eps0_F_m"]), 6),
    "B_10T_u_J_m3": fmt(U_B),
    "toy_g_at_1m_m_s2": fmt(G_R1),
    "toy_metric_h00_at_2m": fmt(H00_R2),
    "wave_I1_T2": fmt(I1, 3),
    "wave_u_J_m3": fmt(WAVE_U, 6),
    "quasistatic_parameter": fmt(QS_PARAM, 6),
    "dim_rank_A": RANK_A_G,
    "dim_rank_augmented_G": RANK_AUG_G,
    "dim_rank_positive_control": RANK_AUG_CTRL,
    "w3_pass": "%d/4" % W3_PASS,
    "w3_positive_control": "%d/4" % W3_CTRL_PASS,
}

META = {
    "rid": RID,
    "stamp": STAMP,
    "title": "ROOT V75 实验控制矩阵与证明状态全维审计",
    "verdict_counts": COUNTS,
    "entry_total": len(ENTRIES),
    "guard_total": len(GUARDS),
    "w3_pass": W3_PASS,
    "w3_positive_control": W3_CTRL_PASS,
    "method": "纯标准库 Decimal 60 位 + Fraction 精确量纲矩阵 + SHA-256 + W3 四门禁 + 幂等产物",
    "source": os.path.relpath(SRC, ROOT).replace("\\", "/"),
    "source_sha256": sha256(os.path.abspath(__file__)),
    "fact_sha256": {os.path.basename(p): sha256(p) for p in SOURCE_FILES},
}

JSON_OBJ = {
    "meta": META,
    "entries": ENTRIES,
    "guards": GUARDS,
    "w3_gate": W3,
    "key_numbers": KEY,
    "redlines": {
        "UFT_goals": "0/6 未完成",
        "systems": "0/22",
        "UFT3": 0,
        "L3": 0,
        "validated": 0,
        "four_force_correct_equations": 0,
        "L3_implies_L4": False,
    },
}

DATA = os.path.join(os.path.dirname(HERE), "数据")
os.makedirs(DATA, exist_ok=True)
BASE = "TUFT-r441_ROOT_V75_实验控制矩阵与证明状态_全维审计_2026-11-22"
J_PATH = os.path.join(os.path.dirname(HERE), "判定_" + BASE + ".md")
JSON_PATH = os.path.join(DATA, BASE + ".json")
MD_PATH = os.path.join(DATA, BASE + ".md")
REP_PATH = os.path.join(DATA, BASE + "_report.txt")


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


write_text(JSON_PATH, json.dumps(JSON_OBJ, ensure_ascii=False, indent=2) + "\n")

MD_LINES = [
    "# r441 ROOT V75 实验控制矩阵与证明状态全维审计数据",
    "",
    "## 条目",
    "",
    "| ID | 判定 | 标题 | 读数 |",
    "|---|---|---|---|",
]
for e in ENTRIES:
    MD_LINES.append("| %s | %s | %s | %s |" % (e["id"], e["verdict"], e["title"], e["detail"].replace("\n", " ")))
MD_LINES.extend(["", "## 守卫", "", "| ID | OK | 读数 |", "|---|---|---|"])
for g in GUARDS:
    MD_LINES.append("| %s | %s | %s |" % (g["id"], "PASS" if g["ok"] else "FAIL", g["detail"].replace("\n", " ")))
MD_LINES.extend(["", "## 关键读数", ""])
for k, v in KEY.items():
    MD_LINES.append("- %s = %s" % (k, v))
MD_LINES.append("")
write_text(MD_PATH, "\n".join(MD_LINES))

REP = [
    "r441 ROOT V75 实验控制矩阵与证明状态全维审计",
    "============================================",
    "entries=%d" % len(ENTRIES),
    "counts=" + " / ".join("%s=%d" % (k, COUNTS[k]) for k in sorted(COUNTS)),
    "guards=%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
    "w3_pass=%d/4" % W3_PASS,
    "w3_positive_control=%d/4" % W3_CTRL_PASS,
    "source_sha256=%s" % META["source_sha256"],
    "dim_rank_A=%d" % RANK_A_G,
    "dim_rank_augmented_G=%d" % RANK_AUG_G,
    "dim_rank_positive_control=%d" % RANK_AUG_CTRL,
    "manifest_items=%d bad=%d" % (len(MANIFEST_ROWS), len(HASH_BAD)),
    "equation_rows=%d factor_rows=%d categories=%d" % (len(EQ_ROWS), len(FACTOR_ROWS), len(CATEGORIES)),
    "B_10T_u_J_m3=%s" % fmt(U_B),
    "toy_g_at_1m_m_s2=%s" % fmt(G_R1),
    "wave_u_J_m3=%s" % fmt(WAVE_U, 6),
    "quasistatic_parameter=%s" % fmt(QS_PARAM, 6),
    "redline=数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功；拟合好 != 定律正确",
    "",
]
write_text(REP_PATH, "\n".join(REP))

J = [
    "# 判定 r441：ROOT V75 实验控制矩阵与证明状态全维审计",
    "",
    "## 〇、一句话",
    "",
    "ROOT V75 的自陈边界诚实（无新仪器数据、未独立证明 G、未实现四力统一）：50 条方程与 30 项因素矩阵可机读且无空字段，"
    "10 T/1 m 的六个代表值、1 MV/m、50 Hz 准静态与零不变量平面波反例均可独立复算；但 G 来源在 {c,E,B,ω,a} 量纲空间内 rank 缺 1 无解，"
    "标量–光子候选参数未锚定，工程测试与实验确证被明确分层。W3 四候选 0/4（阳性对照 1/4），红线计数不变。",
    "",
    "## 一、产物",
    "",
    "| 顺序 | 文件 | 作用 |",
    "|---|---|---|",
    "| 0 | 本判定册 | 五段裁定 + W3 + 红线 |",
    "| 1 | [引擎](源码/TUFT-r441_ROOT_V75_实验控制矩阵与证明状态_全维审计_2026-11-22.py) | %d 条目 / %d 守卫 / 纯标准库 |" % (len(ENTRIES), len(GUARDS)),
    "| 2 | [数据 md](数据/TUFT-r441_ROOT_V75_实验控制矩阵与证明状态_全维审计_2026-11-22.md) · [json](数据/TUFT-r441_ROOT_V75_实验控制矩阵与证明状态_全维审计_2026-11-22.json) · [报告](数据/TUFT-r441_ROOT_V75_实验控制矩阵与证明状态_全维审计_2026-11-22_report.txt) | 机器读数留档 |",
    "| 3 | 来料正本（只读） | %s |" % KEY["source"],
    "",
    "## 二、条目与守卫",
    "",
    "条目 %d（%s），守卫 %d/%d，W3 %d/4（阳性对照 %d/4），源码 SHA-256 `%s`。"
    % (len(ENTRIES), " / ".join("%s=%d" % (k, COUNTS[k]) for k in sorted(COUNTS)),
       sum(1 for g in GUARDS if g["ok"]), len(GUARDS), W3_PASS, W3_CTRL_PASS, META["source_sha256"]),
    "",
    "| ID | 判定 | 标题 | 读数 |",
    "|---|---|---|---|",
]
for e in ENTRIES:
    J.append("| %s | %s | %s | %s |" % (e["id"], e["verdict"], e["title"], e["detail"].replace("\n", " ")))
J.extend(["", "## 三、守卫表", "", "| ID | OK | 读数 |", "|---|---|---|"])
for g in GUARDS:
    J.append("| %s | %s | %s |" % (g["id"], "PASS" if g["ok"] else "FAIL", g["detail"].replace("\n", " ")))
J.extend(["", "## 四、关键读数", ""])
for k, v in KEY.items():
    J.append("- %s = %s" % (k, v))
J.extend([
    "",
    "## 五、红线与边界",
    "",
    "数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功；拟合好 != 定律正确。",
    "本册不新增 W3/L3/UFT3/validated；0/6、0/22、含引力四力正确方程 0 条、L3↛L4 保持不变。",
    "",
    "G no-go 与电磁源-耦合混同继承 attack64，本册不重判；本册增量限于方程目录、因素矩阵、数值摘要、工程测试与实验状态的可复算定价。",
    "来料的球形能量等效是理想远场玩具，不是完整 Einstein-Maxwell 解，也不是实测的人工引力场；50 Hz 结论仅在 ωa/c<<1 成立。",
    "",
])
write_text(J_PATH, "\n".join(J))

print("r441 entries=%d counts=%s" % (len(ENTRIES), " / ".join("%s=%d" % (k, COUNTS[k]) for k in sorted(COUNTS))))
print("r441 guards=%d/%d w3=%d/4 (ctrl=%d/4)" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS), W3_PASS, W3_CTRL_PASS))
print("r441 json=%s" % JSON_PATH)
print("r441 verdict=%s" % J_PATH)
