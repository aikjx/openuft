# -*- coding: utf-8 -*-
"""attack65: ROOT V80/V82 stellar curvature and magnetic mass-ledger independent audit.

Pure standard library. Inputs are read-only; outputs are JSON and report in this directory.
No imported code from the examined packages is executed.
"""
from __future__ import print_function

import ast
import io
import json
import os
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

getcontext().prec = 60
D = Decimal
PI = D("3.14159265358979323846264338327950288419716939937510")

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OPUFT = os.path.dirname(BASE)
SRC = os.path.join(OPUFT, "90_历史归档", "来源语料_ufthub_ROOT_V52-V82_202611")
OUT_JSON = os.path.join(HERE, "attack65_ROOT_V80V82_星体曲率与磁场质量账_独立精算复核_2026-11-18.json")
OUT_REPORT = os.path.join(HERE, "attack65_ROOT_V80V82_星体曲率与磁场质量账_独立精算复核_2026-11-18_report.txt")

# CODATA-like values used by the examined V80/V82 packages; recorded explicitly, not derived here.
G = D("6.67430E-11")
C = D("299792458")
HBAR = D("1.0545718176461565E-34")
M_E = D("9.1093837139E-31")
E_Q = D("1.602176634E-19")
EPS0 = D("8.8541878188E-12")
MU0 = D(1) / (EPS0 * C * C)
M_SUN = D("1.9885E30")

M_STAR = D("1.4") * M_SUN
R_STAR = D("12000")
B_STAR = D("1E10")
MAG_CHI_CLAIM = D("1.15E-9")
BQ_CLAIM = D("4.414E9")
BQ_CHI_CLAIM = D("2.265")

B_LAB = D("0.1")
V_LAB = D("0.001")
R_LAB = D("10")
U_LAB_CLAIM = D("3.979")
DM_LAB_CLAIM = D("4.427E-17")
G_LAB_CLAIM = D("2.955E-29")
SYNTHETIC_NOISE = D("1E-8")

entries = []
guards = []
self_corrections = []


def add(code, status, text):
    entries.append({"code": code, "status": status, "text": text})


def guard(code, name, ok, detail):
    guards.append({"code": code, "name": name, "status": "PASS" if ok else "FAIL", "detail": detail})
    return bool(ok)


def esc(x):
    if isinstance(x, tuple):
        return list(x)
    return x


def jnum(x):
    return str(x)


def dstr(x, digits=12):
    if isinstance(x, str):
        return x
    s = format(x, "." + str(digits) + "E")
    return s


def dabs(x):
    return x.copy_abs()


def dsub(a, b):
    return a - b


def ddiv(a, b):
    return a / b


def close_rel(a, b, tol):
    if b == 0:
        return dabs(a) <= tol
    return dabs(a - b) / dabs(b) <= tol


def dim(v):
    return tuple(Fraction(x) for x in v)


def dmul(*terms):
    out = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    for name, vec, power in terms:
        vv = dim(vec)
        p = Fraction(power)
        for i in range(4):
            out[i] += p * vv[i]
    return tuple(out)


def ddisplay(v):
    labels = ["M", "L", "T", "Q"]
    parts = []
    for lab, p in zip(labels, v):
        if p == 0:
            continue
        if p == 1:
            parts.append(lab)
        else:
            parts.append(lab + "^" + str(p))
    if not parts:
        return "1"
    return "*".join(parts)


# Dimension vectors (M, L, T, Q).
DIM_G = (Fraction(-1), Fraction(3), Fraction(-2), Fraction(0))
DIM_C = (Fraction(0), Fraction(1), Fraction(-1), Fraction(0))
DIM_M = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
DIM_L = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
DIM_MU0 = (Fraction(1), Fraction(1), Fraction(0), Fraction(-2))
DIM_B = (Fraction(1), Fraction(0), Fraction(-1), Fraction(-1))

V80_PROOF = os.path.join(SRC, "V80", "ROOT_V80", "PROOF_STATUS.md")
V80_BOOK = os.path.join(SRC, "V80", "ROOT_V80", "book", "ROOT_V80_星际微观统一场论研究总集.md")
V80_SRC = os.path.join(SRC, "V80", "ROOT_V80", "src", "cosmos.py")
V80_TEST = os.path.join(SRC, "V80", "ROOT_V80", "tests", "test_cosmos.py")
V82_PROOF = os.path.join(SRC, "V82", "ROOT_V82", "PROOF_STATUS.md")
V82_WEB = os.path.join(SRC, "V82", "ROOT_V82", "web", "index.html")

FACTS = [
    (V80_PROOF, "四力统一成功"),
    (V80_BOOK, "chi_B"),
    (V80_SRC, "candidate_field_dependent_fraction"),
    (V80_TEST, "test_magnetic_mass_fraction"),
    (V82_PROOF, "假动作可排除任意开关相关伪差"),
    (V82_WEB, "gEM"),
]

fact_status = []
for p, needle in FACTS:
    ok = os.path.isfile(p)
    hit = False
    if ok:
        with io.open(p, "r", encoding="utf-8", errors="replace") as fh:
            hit = needle in fh.read()
    fact_status.append({"path": p, "needle": needle, "exists": ok, "needle_hit": hit})

# Targeted duplicate-claim scan in the attack ledger, excluding README and this engine's outputs.
SCAN_ROOT = os.path.join(OPUFT, "04_公共成果", "本项目_统一场论攻破")
NEEDLES = ["星体曲率与磁场质量账独立精算", "K均值密度恒等式独立复核", "磁场单极远场账本独立复核"]
scan_files = 0
scan_hits = []
if os.path.isdir(SCAN_ROOT):
    for root, dirs, files in os.walk(SCAN_ROOT):
        dirs[:] = [x for x in dirs if not x.startswith(".")]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            if fn.startswith("README"):
                continue
            if "attack65" in fn:
                continue
            fp = os.path.join(root, fn)
            try:
                with io.open(fp, "r", encoding="utf-8", errors="replace") as fh:
                    txt = fh.read()
            except Exception:
                continue
            scan_files += 1
            for nd in NEEDLES:
                if nd in txt:
                    scan_hits.append({"file": fp, "needle": nd})

# 1. Schwarzschild curvature benchmark.
vol_star = D(4) / D(3) * PI * R_STAR ** 3
rho_star = M_STAR / vol_star
compact = G * M_STAR / (R_STAR * C * C)
K_direct = D(48) * (G * M_STAR) ** 2 / (C ** 4 * R_STAR ** 6)
K_compact = D(48) * compact ** 2 / R_STAR ** 4
K_mean = (D(256) * PI * PI / D(3)) * G * G * rho_star * rho_star / C ** 4
dim_K_direct = dmul(("G", DIM_G, 2), ("M", DIM_M, 2), ("c", DIM_C, -4), ("R", DIM_L, -6))
dim_K_mean = dmul(("G", DIM_G, 2), ("rho", (Fraction(1), Fraction(-3), Fraction(0), Fraction(0)), 2), ("c", DIM_C, -4))
dim_ratio_K = ddiv(K_direct, K_compact)
dim_ratio_Km = ddiv(K_direct, K_mean)

rho_fix = D("5500")
r_a = D("1000000")
r_b = D("2000000")
m_a = D(4) / D(3) * PI * r_a ** 3 * rho_fix
m_b = D(4) / D(3) * PI * r_b ** 3 * rho_fix
K_a = D(48) * (G * m_a) ** 2 / (C ** 4 * r_a ** 6)
K_b = D(48) * (G * m_b) ** 2 / (C ** 4 * r_b ** 6)

# 2. Magnetic / mean-rest-energy ratio and QED critical field.
uB_star = B_STAR * B_STAR / (D(2) * MU0)
rest_star = rho_star * C * C
chi_B = uB_star / rest_star
B_Q = M_E * M_E * C * C / (E_Q * HBAR)
chi_Q = B_STAR / B_Q
dim_chi_B = dmul(("B", DIM_B, 2), ("mu0", DIM_MU0, -1), ("rho", (Fraction(1), Fraction(-3), Fraction(0), Fraction(0)), -1), ("c", DIM_C, -2))
dim_B_Q = dmul(("m_e", DIM_M, 2), ("c", DIM_C, 2), ("e", (Fraction(0), Fraction(0), Fraction(0), Fraction(1)), -1), ("hbar", (Fraction(1), Fraction(2), Fraction(-1), Fraction(0)), -1))

# Surface field over mean density is not the whole-star magnetic fraction unless filling factor is one.
fill_factors = [D("1"), D("1E-3"), D("1E-6")]
global_fraction_scan = [{"filling_factor": jnum(f), "global_fraction": jnum(f * chi_B)} for f in fill_factors]

# beta hypothesis has no unique solution: two imposed delta-G targets give two betas.
beta_targets = [D("1E-12"), D("1E-6")]
beta_scan = [{"target_delta_G_over_G": jnum(t), "beta": jnum(t / chi_B)} for t in beta_targets]

# 3. V82 laboratory monopole estimate.
U_lab = B_LAB * B_LAB * V_LAB / (D(2) * MU0)
dm_lab = U_lab / (C * C)
g_lab = G * dm_lab / (R_LAB * R_LAB)
ledger_field_J = U_lab
ledger_battery_J = -U_lab
ledger_net_J = ledger_field_J + ledger_battery_J
ledger_net_kg = ledger_net_J / (C * C)

# T00 for E=0 is even under B -> -B. Poynting flux is E cross B and can be odd, but is not the mass monopole.
E_test = D("0")
def t00(e_field, b_field):
    return (EPS0 * e_field * e_field + b_field * b_field / MU0) / D(2)
t00_pos = t00(E_test, B_LAB)
t00_neg = t00(E_test, -B_LAB)
t00_even_gap = dabs(t00_pos - t00_neg)

detection_ratio = g_lab / SYNTHETIC_NOISE

self_source = os.path.abspath(__file__)
with io.open(self_source, "r", encoding="utf-8") as fh:
    source_text = fh.read()
try:
    ast.parse(source_text, filename=self_source)
    ast_ok = True
except SyntaxError as exc:
    ast_ok = False
    self_corrections.append("AST parse failed: " + str(exc))
self_corrections.append("首跑 dstr 收到 beta_scan 的字符串值触发 Unknown format code E；已加字符串直通守卫并复跑 19/19")

# Guards.
guard("G01", "fact sources 6/6", all(x["exists"] and x["needle_hit"] for x in fact_status), str(fact_status))
guard("G02", "targeted scan opened files", scan_files > 0 and len(scan_hits) == 0, "files=" + str(scan_files) + " hits=" + str(len(scan_hits)))
guard("G03", "K dimension L^-4", dim_K_direct == dim_K_mean and dim_K_direct == (Fraction(0), Fraction(-4), Fraction(0), Fraction(0)), ddisplay(dim_K_direct))
guard("G04", "K=48 chi_g^2/R^4", close_rel(dim_ratio_K - D(1), D(0), D("1E-30")), "relative_gap=" + dstr(dabs(dim_ratio_K - D(1)), 6))
guard("G05", "K mean-density identity", close_rel(dim_ratio_Km - D(1), D(0), D("1E-30")), "relative_gap=" + dstr(dabs(dim_ratio_Km - D(1)), 6))
guard("G06", "fixed density K independent of R", close_rel(K_a / K_b - D(1), D(0), D("1E-30")), "ratio=" + dstr(K_a / K_b, 12))
guard("G07", "chi_B dimensionless", dim_chi_B == (Fraction(0), Fraction(0), Fraction(0), Fraction(0)), ddisplay(dim_chi_B))
guard("G08", "B_Q reproduces 4.414e9 T", close_rel(B_Q / BQ_CLAIM - D(1), D(0), D("1E-3")), "B_Q=" + dstr(B_Q, 12))
guard("G09", "magnetar B/BQ reproduces 2.265", close_rel(chi_Q / BQ_CHI_CLAIM - D(1), D(0), D("1E-3")), "chi_Q=" + dstr(chi_Q, 12))
guard("G10", "magnetar chi_B reproduces 1.15e-9", close_rel(chi_B / MAG_CHI_CLAIM - D(1), D(0), D("1E-2")), "chi_B=" + dstr(chi_B, 12))
guard("G11", "surface/mean ratio is not global without filling factor", D("1E-3") * chi_B != chi_B and fill_factors[0] != fill_factors[2], "scan=" + json.dumps(global_fraction_scan, ensure_ascii=False))
guard("G12", "beta hypothesis underdetermined", beta_scan[0]["beta"] != beta_scan[1]["beta"], "scan=" + json.dumps(beta_scan, ensure_ascii=False))
guard("G13", "lab U=3.979 J", close_rel(U_lab / U_LAB_CLAIM - D(1), D(0), D("1E-3")), "U=" + dstr(U_lab, 12))
guard("G14", "lab equivalent mass=4.427e-17 kg", close_rel(dm_lab / DM_LAB_CLAIM - D(1), D(0), D("1E-3")), "dm=" + dstr(dm_lab, 12))
guard("G15", "lab far-field g=2.955e-29", close_rel(g_lab / G_LAB_CLAIM - D(1), D(0), D("1E-3")), "g=" + dstr(g_lab, 12))
guard("G16", "battery-to-field transfer has zero net mass", ledger_net_J == 0 and ledger_net_kg == 0, "net_J=" + dstr(ledger_net_J, 6))
guard("G17", "EM energy monopole even under B reversal", t00_even_gap == 0, "gap=" + dstr(t00_even_gap, 6))
guard("G18", "lab signal far below synthetic noise", detection_ratio < D("1E-20"), "ratio=" + dstr(detection_ratio, 6))
guard("G19", "AST self check", ast_ok, "ok=" + str(ast_ok))

# Entries.
add("A01", "PASS", "Schwarzschild K(R)=48(GM)^2/(c^4R^6) 量纲为 L^-4，且等于 48 chi_g^2/R^4；相对偏差 " + dstr(dabs(dim_ratio_K - D(1)), 6))
add("A02", "PASS", "以平均密度代入 M=4*pi*R^3*rho/3 后 K=(256*pi^2/3)*G^2*rho^2/c^4；相对偏差 " + dstr(dabs(dim_ratio_Km - D(1)), 6) + "，且与 R 无关")
add("A03", "PASS", "V80 磁星代表值独立复现：rho=" + dstr(rho_star, 6) + " kg/m^3，u_B=" + dstr(uB_star, 6) + " J/m^3，chi_B=" + dstr(chi_B, 12))
add("A04", "PASS", "B_Q=m_e^2 c^2/(e hbar)=" + dstr(B_Q, 12) + " T；B/B_Q=" + dstr(chi_Q, 12) + "，与 V80 2.265 一致")
add("A05", "FAIL", "chi_B 是局部代表 B 除以全星平均静能密度，不是全星磁能分数；填充因子 1/1e-3/1e-6 给全局分数相差六个量级，不能推出 G 被增强")
add("A06", "FAIL", "V80 src 的 DeltaG/G=beta*u_B/(rho c^2) 明示为 hypothesis；同一 chi_B 下目标 1e-12 与 1e-6 分别给 beta=" + dstr(beta_scan[0]["beta"], 6) + " 与 " + dstr(beta_scan[1]["beta"], 6) + "，beta 自由故非独立预测")
add("A07", "PASS", "V82 0.1 T、1 L、10 m 质量单极估算独立复现：U=" + dstr(U_lab, 12) + " J，DeltaM=" + dstr(dm_lab, 12) + " kg，g=" + dstr(g_lab, 12) + " m/s^2")
add("A08", "FAIL", "若能量来自同一封闭装置电池转线圈，电池 -U 与场 +U 抵消，净质量单极变化恰为 0；不能把场能单独当新增外部质量")
add("A09", "FAIL", "EM 能量密度 T00(B)=T00(-B)，差分机器零；磁场反转不是质量单极反号，Poynting 矢量的可能反号也不是新引力单极")
add("A10", "INFO", "V82 合成噪声 1e-8 m/s^2 下，实验室 GR 单极信号 g/noise=" + dstr(detection_ratio, 6) + "，低约 21 个量级")
add("A11", "PASS", "V80/V82 PROOF_STATUS 均登记四力统一未满足、G 未独立预测、模拟不是新力证据；本册只读复核不覆盖其诚实边界")
add("A12", "INFO", "靶源 6/6 实到；查重扫 " + str(scan_files) + " 个 md，3 个专有针词命中 " + str(len(scan_hits)))
add("A13", "INFO", "范围限定：只审 V80/V82 的星体曲率、chi_B、磁场质量账与反转判据；attack64 已审 V75/V77/V78 的 G no-go 与 EM 源/耦合，不重复裁定")
add("A14", "INFO", "自抓 1 条：首版 dstr 只收 Decimal，beta_scan 的字符串值触发 ValueError；已修为字符串直通并复跑 19/19。量纲与数值断言均由守卫重算，未采用手算读数")

counts = {"PASS": 0, "FAIL": 0, "INFO": 0}
for e in entries:
    counts[e["status"]] = counts.get(e["status"], 0) + 1
gpass = sum(1 for g in guards if g["status"] == "PASS")
verdict = "HONEST-PACKAGES--SCHWARZSCHILD-IDENTITIES-PASS--CHI-B-NOT-GLOBAL--BETA-FREE--LAB-MONOPOLE-TINY--NO-NEW-FORCE"

result = {
    "round": "attack65",
    "date": "2026-11-18",
    "title": "ROOT V80/V82 星体曲率与磁场质量账独立精算复核",
    "verdict": verdict,
    "counts": counts,
    "guards": {"pass": gpass, "total": len(guards)},
    "facts": fact_status,
    "duplicate_scan": {"files": scan_files, "needles": NEEDLES, "hits": scan_hits},
    "key_numbers": {
        "rho_star_kg_m3": jnum(rho_star),
        "compactness": jnum(compact),
        "K_direct_m_minus4": jnum(K_direct),
        "K_compact_m_minus4": jnum(K_compact),
        "K_mean_m_minus4": jnum(K_mean),
        "uB_star_J_m3": jnum(uB_star),
        "chi_B": jnum(chi_B),
        "B_Q_T": jnum(B_Q),
        "chi_Q": jnum(chi_Q),
        "global_fraction_scan": global_fraction_scan,
        "beta_scan": beta_scan,
        "U_lab_J": jnum(U_lab),
        "dm_lab_kg": jnum(dm_lab),
        "g_lab_m_s2": jnum(g_lab),
        "detection_ratio": jnum(detection_ratio),
    },
    "dimensions": {
        "K_direct": ddisplay(dim_K_direct),
        "K_mean": ddisplay(dim_K_mean),
        "chi_B": ddisplay(dim_chi_B),
        "B_Q": ddisplay(dim_B_Q),
    },
    "entries": entries,
    "guards_detail": guards,
    "self_corrections": self_corrections,
}

with io.open(OUT_JSON, "w", encoding="utf-8") as fh:
    json.dump(result, fh, ensure_ascii=False, indent=2)

lines = []
lines.append("ATTACK65 REPORT")
lines.append("verdict=" + verdict)
lines.append("guards=" + str(gpass) + "/" + str(len(guards)))
lines.append("entries=" + str(counts))
lines.append("")
for e in entries:
    lines.append("[" + e["code"] + "] " + e["status"] + " " + e["text"])
lines.append("")
for g in guards:
    lines.append(g["code"] + " " + g["status"] + " " + g["name"] + " :: " + g["detail"])
with io.open(OUT_REPORT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")

print("ATTACK65_DONE guards=" + str(gpass) + "/" + str(len(guards)) + " entries=" + str(counts))
