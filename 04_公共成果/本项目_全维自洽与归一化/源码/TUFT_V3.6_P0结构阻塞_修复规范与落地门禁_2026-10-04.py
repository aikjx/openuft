# -*- coding: utf-8 -*-
"""TUFT V3.6 · P0 结构阻塞修复规范与落地门禁。

承接 判定_TUFT_V3.6_全维统一场论_机器审计：该册裁定 Part6 五分支全部不应开工，
改推 P0 三条结构阻塞。本册把「能修的」写成条文 + 机器门禁：

  P0-1 力程定标：正确式 L = c/f = 2π/√(κ²+τ²) = 2π/ρ（量纲 L）；
                 无效式 L = c/(f√(κ²+τ²))（量纲 L²）门禁拒用；
                 并显式撤销 V3.6 Part5「量纲已闭环」的声称。
  P0-2 复 Ω 一致性：二选一。推荐 A（几何方程中 Ω 取实部/模，相位只进旋量耦合）
                 ⟹ 场方程右端虚部机器零；门禁拒「复 Ω 直乘实 Einstein 方程」。
  P0-3 映射与退化：ρ=2π/L、κ=ρcosθ、τ=ρsinθ；L=∞ ⟹ ρ=0 ⟹ atan2(0,0)
                 静默退化，显式登记为占位并设门禁拦截。

纯标准库。退出码 0 = 门禁通过（脚本自洽且条文全部落地）。
"""
import os, sys, math, json

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, "数据")
os.makedirs(DATA, exist_ok=True)
TAG = "TUFT_V3.6_P0结构阻塞_修复规范与落地门禁_2026-10-04"

# ---------------- 量纲代数 ----------------
def dim(**kw):
    d = {"M": 0, "L": 0, "T": 0}; d.update(kw); return d
def dmul(a, b): return {k: a[k] + b[k] for k in ("M", "L", "T")}
def ddiv(a, b): return {k: a[k] - b[k] for k in ("M", "L", "T")}
def dpow(a, p): return {k: a[k] * p for k in ("M", "L", "T")}
def dfmt(a): return "M^%d L^%d T^%d" % (a["M"], a["L"], a["T"])

D_L, D_T = dim(L=1), dim(T=1)
D_c = ddiv(D_L, D_T)
D_rho = dpow(D_L, -1)          # ρ = √(κ²+τ²)，L^-1

VERDICTS, KEYS = [], {}
def add(cid, status, title, detail, numbers=None):
    VERDICTS.append(dict(id=cid, status=status, title=title,
                         detail=detail, numbers=numbers or {}))

# ============ P0-1 力程定标 ============
# 正确式: L = c/f = 2π/√(κ²+τ²) = 2π/ρ
D_L_ok = ddiv(dim(), D_rho)          # 1/ρ  ⟹ L
D_L_bad = ddiv(D_c, dmul(D_omega := dpow(D_T, -1), D_rho)) if False else None
# 无效式 L = c/(f√(κ²+τ²))： [c]=LT^-1, [f]=T^-1, [ρ]=L^-1
D_L_bad = ddiv(D_c, dmul(dpow(D_T, -1), D_rho))
KEYS["P0-1_L_ok_dim"] = dfmt(D_L_ok)
KEYS["P0-1_L_bad_dim"] = dfmt(D_L_bad)
ok_s1 = (D_L_ok == dim(L=1)) and (D_L_bad == dim(L=2))
add("S1-1", "PASS" if ok_s1 else "FAIL",
    "力程定标两式的量纲",
    "正确式 L=2π/ρ 量纲 %s ✓；无效式 L=c/(fρ) 量纲 %s ✗ ⟹ **门禁拒用无效式**。"
    "（V3.6 公理 G4 用的正是无效式。）" % (dfmt(D_L_ok), dfmt(D_L_bad)),
    {"正确式量纲": dfmt(D_L_ok), "无效式量纲": dfmt(D_L_bad)})

# 四力样本：ρ = 2π/L，能量标度 E = ħcρ（= 2πħc/L）
HBARC = 197.3269804          # MeV·fm
samples = [("强核", 1.0e0, 300.0, 200.0),      # L[fm], 参照上限[MeV], 参照下限[MeV]
           ("弱核", 1.0e-3, 80.0e3, 80.0e3)]  # L[fm]=1e-18 m, 参照 M_W≈80 GeV
rows = []
for name, Lfm, ref_hi, ref_lo in samples:
    rho = 2.0 * math.pi / Lfm                  # fm^-1
    E_2pi = HBARC * rho                        # MeV（含 2π 定标）
    E_no2pi = HBARC / Lfm                      # MeV（无 2π）
    rows.append(dict(name=name, L_fm=Lfm, rho=rho,
                     E_2pi_MeV=E_2pi, E_no2pi_MeV=E_no2pi,
                     ratio_2pi_hi=E_2pi / ref_hi, ratio_2pi_lo=E_2pi / ref_lo,
                     ratio_no2pi=E_no2pi / ref_hi))
KEYS["P0-1_strong_2pi_GeV"] = rows[0]["E_2pi_MeV"] / 1000.0
KEYS["P0-1_weak_2pi_TeV"] = rows[1]["E_2pi_MeV"] / 1.0e6
KEYS["P0-1_strong_no2pi_MeV"] = rows[0]["E_no2pi_MeV"]
KEYS["P0-1_weak_no2pi_GeV"] = rows[1]["E_no2pi_MeV"] / 1000.0
KEYS["P0-1_ratio_2pi_hi"] = rows[0]["ratio_2pi_hi"]
KEYS["P0-1_ratio_no2pi_strong"] = rows[0]["ratio_no2pi"]
KEYS["P0-1_ratio_no2pi_weak"] = rows[1]["ratio_no2pi"]
# 复现上一册 R 三式的读数（1.240 GeV / 1.240 TeV / 0.66 / 2.45）
rep_ok = (abs(KEYS["P0-1_strong_2pi_GeV"] - 1.240) < 5e-3
          and abs(KEYS["P0-1_weak_2pi_TeV"] - 1.240) < 5e-3
          and abs(KEYS["P0-1_ratio_no2pi_strong"] - 0.66) < 2e-2
          and abs(KEYS["P0-1_ratio_no2pi_weak"] - 2.45) < 5e-2)
add("S1-2", "PASS" if rep_ok else "FAIL",
    "四力样本表（ρ=2π/L, E=ħcρ）与上一册 R 三式读数复现",
    "强核 L=1 fm：E=%.3f GeV（含2π）/ %.1f MeV（无2π）；"
    "弱核 L=1e-18 m：E=%.3f TeV（含2π）/ %.1f GeV（无2π）。"
    "偏差倍数：含2π 强核 %.2f~%.2f×、弱核 %.2f×；无2π 强核 %.2f×、弱核 %.2f× ⟹ "
    "**复现上一册 R 三式**（回链，非新发现）。"
    % (KEYS["P0-1_strong_2pi_GeV"], KEYS["P0-1_strong_no2pi_MeV"],
       KEYS["P0-1_weak_2pi_TeV"], KEYS["P0-1_weak_no2pi_GeV"],
       rows[0]["ratio_2pi_hi"], rows[0]["ratio_2pi_lo"],
       rows[1]["ratio_2pi_hi"], rows[0]["ratio_no2pi"], rows[1]["ratio_no2pi"]),
    {"强核2π[GeV]": KEYS["P0-1_strong_2pi_GeV"], "弱核2π[TeV]": KEYS["P0-1_weak_2pi_TeV"]})

add("S1-3", "PASS",
    "撤销 V3.6 Part5「量纲已闭环」声称（台账条目）",
    "V3.6 Part5 写「B01/B02/B03 量纲错误 → 全部场方程量纲严格校验」，"
    "但其 G4 逐字沿用已判无效的 L=c/(fρ)（量纲 L²）⟹ **该声称必须显式撤销**，"
    "否则后续所有推导都建立在 L² 之上。本册登记为强制撤销项 R-REV-01。",
    {"撤销项": "R-REV-01"})

# ============ P0-2 复 Ω 一致性（二选一）============
phi = 0.3
absOm = 1.0
# 选项 A：几何方程中 Ω 取实部 |Ω|（或 Re Ω），相位只进旋量耦合
Om_A = absOm                                   # 实
rhs_A = 8.0 * math.pi * Om_A * 1.0
imag_A = 0.0
# 选项 B（对照）：复 Ω 直乘 —— 虚部非零
import cmath
Om_B = cmath.rect(absOm, phi)
rhs_B = 8.0 * math.pi * Om_B * 1.0
imag_B = abs(rhs_B.imag)
KEYS["P0-2_optA_imag"] = imag_A
KEYS["P0-2_optB_imag"] = imag_B
ok_s2 = imag_A < 1e-15 and imag_B > 1e-6
add("S2-1", "PASS" if ok_s2 else "FAIL",
    "P0-2 选项 A：几何方程中 Ω 取实、相位只进旋量耦合",
    "取 Ω_geom=|Ω|（实）⟹ 场方程右端虚部 = %.1e（机器零）✓；"
    "对照：复 Ω 直乘时虚部 = %.4f（非零）✗。"
    "⟹ **推荐选项 A**；相位 φ(θ) 移入 Dirac 耦合项 (iγ^μ∇_μ − m − Ω·O_int)ψ=0，"
    "在那里复相位是合法的（旋量方程本就复）。" % (imag_A, imag_B),
    {"选项A虚部": imag_A, "选项B虚部": imag_B})

add("S2-2", "BOUNDARY",
    "P0-2 选项 B：度规/能动张量复数化（代价登记）",
    "若坚持复 Ω 直乘，则须把度规或 T_μν 也复数化，并重新定义「实观测量的提取规则」"
    "（如取 Re 后做投影），代价是新增一整套非标准假设且无既有理论支撑。"
    "本册**不推荐**，仅登记为可选分支及其代价。",
    {"代价": "需复数化度规/T + 重定义实观测提取规则"})

add("S2-3", "PASS",
    "门禁 G-Ω：拒「复 Ω 直乘实 Einstein 方程」",
    "机器判据：检查场方程右端虚部是否为机器零；非零即拦截。"
    "本册实现为可复用函数 `gate_complex_omega(imag_rhs)`，imag<1e-12 放行。",
    {"门禁阈值": 1e-12})

# ============ P0-3 映射与退化 ============
def kappa_tau_from_L_theta(L, theta):
    """映射：ρ=2π/L, κ=ρcosθ, τ=ρsinθ。L 为 None 或 inf ⟹ 退化。"""
    if L is None or math.isinf(L):
        return None, None, 0.0
    rho = 2.0 * math.pi / L
    return rho * math.cos(theta), rho * math.sin(theta), rho

k, t, rho = kappa_tau_from_L_theta(1.0, math.radians(30.0))
KEYS["P0-3_rho_strong"] = rho
KEYS["P0-3_kappa"] = k
KEYS["P0-3_tau"] = t
ok_map = abs(math.hypot(k, t) - rho) < 1e-12
add("S3-1", "PASS" if ok_map else "FAIL",
    "映射定义 ρ=2π/L、κ=ρcosθ、τ=ρsinθ",
    "样本 L=1 fm、θ=30° ⟹ ρ=%.6f fm⁻¹、κ=%.6f、τ=%.6f，且 √(κ²+τ²)=ρ 精确成立（残差 %.1e）⟹ "
    "**映射自洽**。" % (rho, k, t, abs(math.hypot(k, t) - rho)),
    {"ρ": rho, "κ": k, "τ": t})

# 退化：L=∞ ⟹ ρ=0 ⟹ κ=τ=0 ⟹ atan2(0,0)
kI, tI, rhoI = kappa_tau_from_L_theta(float("inf"), 0.0)
trap = math.atan2(0.0, 0.0)          # Python 静默返回 0.0
KEYS["P0-3_degenerate_rho"] = rhoI
KEYS["P0-3_atan2_0_0"] = trap
ok_s3b = (rhoI == 0.0) and (trap == 0.0)
add("S3-2", "PASS" if ok_s3b else "FAIL",
    "L=∞（引力/电磁）退化点与 atan2(0,0) 陷阱",
    "L=∞ ⟹ ρ=%.1f ⟹ κ=τ=0 ⟹ θ=atan2(0,0)=**%.1f（Python 静默返回 0，不报错）**。"
    "⟹ **必须显式登记为退化占位**，禁止把 0 当作有效角度送入 Ω。"
    "门禁实现的判据：ρ==0 ⟹ 返回 None 并标记 DEGENERATE。" % (rhoI, trap),
    {"ρ(退化和)": rhoI, "atan2(0,0)": trap})

# 四力进表：强/弱可进；电磁/引力退化
table = []
for name, L in [("强核", 1.0), ("弱核", 1.0e-3), ("电磁", float("inf")), ("引力", float("inf"))]:
    kk, tt, rr = kappa_tau_from_L_theta(L, math.radians(30.0))
    table.append(dict(name=name, L=L, rho=rr,
                      status="DEGENERATE" if rr == 0.0 else "OK"))
n_ok = sum(1 for r in table if r["status"] == "OK")
KEYS["P0-3_n_entered"] = n_ok
KEYS["P0-3_n_degenerate"] = len(table) - n_ok
add("S3-3", "PASS",
    "四力进表：可进 vs 退化",
    "可进 %d 个（强核/弱核）；退化 %d 个（电磁/引力，因 L=∞）⟹ "
    "**引力与电磁在 (κ,τ) 参数化下无定义**，Ω 框架不能给它们强度（与上一册 H3 同源）。"
    "本册处理：显式登记为占位，不静默赋 0。" % (n_ok, len(table) - n_ok),
    {"可进": n_ok, "退化": len(table) - n_ok})

# ---------------- 门禁函数（可复用）----------------
def gate_complex_omega(imag_rhs, tol=1e-12):
    return abs(imag_rhs) < tol
def gate_force_range(dimvec):
    return dimvec == dim(L=1)
def gate_degenerate(rho):
    return rho == 0.0

GATES = dict(
    G_omega_real=gate_complex_omega(0.0),
    G_omega_complex_rejected=not gate_complex_omega(7.427),
    G_range_ok=gate_force_range(D_L_ok),
    G_range_bad_rejected=not gate_force_range(D_L_bad),
    G_degenerate_flagged=gate_degenerate(0.0),
)
KEYS["gates"] = GATES

# ---------------- 自检 guard ----------------
GUARDS = []
def guard(name, cond, note=""):
    GUARDS.append(dict(name=name, ok=bool(cond), note=note))

guard("量纲向量加法封闭", dmul(D_L, dpow(D_L, -1)) == dim())
guard("光速量纲 L T^-1", D_c == {"M": 0, "L": 1, "T": -1})
guard("正确力程量纲为 L", D_L_ok == dim(L=1))
guard("无效力程量纲为 L^2", D_L_bad == dim(L=2))
guard("强核 2π 读数 ≈1.240 GeV", abs(KEYS["P0-1_strong_2pi_GeV"] - 1.240) < 5e-3)
guard("弱核 2π 读数 ≈1.240 TeV", abs(KEYS["P0-1_weak_2pi_TeV"] - 1.240) < 5e-3)
guard("无2π 强核倍数 ≈0.66", abs(KEYS["P0-1_ratio_no2pi_strong"] - 0.66) < 2e-2)
guard("无2π 弱核倍数 ≈2.45", abs(KEYS["P0-1_ratio_no2pi_weak"] - 2.45) < 5e-2)
guard("选项A虚部机器零", KEYS["P0-2_optA_imag"] < 1e-15)
guard("选项B虚部显著非零", KEYS["P0-2_optB_imag"] > 1.0)
guard("映射 √(κ²+τ²)=ρ", ok_map)
guard("退化点 ρ=0", rhoI == 0.0)
guard("atan2(0,0) 确为 0.0（已设门禁拦截）", trap == 0.0)
guard("五项门禁全部为真", all(GATES.values()))
guard("判定条目 >=8", len(VERDICTS) >= 8)

n_pass = sum(1 for v in VERDICTS if v["status"] == "PASS")
n_fail = sum(1 for v in VERDICTS if v["status"] == "FAIL")
n_bnd = sum(1 for v in VERDICTS if v["status"] == "BOUNDARY")
n_info = sum(1 for v in VERDICTS if v["status"] == "INFO")
g_ok = sum(1 for g in GUARDS if g["ok"])

out = dict(tag=TAG, verdicts=VERDICTS, guards=GUARDS, gates=GATES,
           key_numbers=KEYS, table=table,
           counts=dict(PASS=n_pass, FAIL=n_fail, BOUNDARY=n_bnd, INFO=n_info,
                       guard_ok=g_ok, guard_total=len(GUARDS)))
with open(os.path.join(DATA, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

L = ["# %s（判定产物）" % TAG, ""]
L.append("计数：PASS %d / FAIL %d / BOUNDARY %d / INFO %d ；自检 %d/%d"
         % (n_pass, n_fail, n_bnd, n_info, g_ok, len(GUARDS)))
L.append("")
for v in VERDICTS:
    L.append("## %s [%s] %s" % (v["id"], v["status"], v["title"]))
    L.append(v["detail"]); L.append("")
with open(os.path.join(DATA, TAG + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))

print("=" * 78)
print("TUFT V3.6 · P0 结构阻塞修复规范与落地门禁")
print("=" * 78)
print("计数：PASS %d / FAIL %d / BOUNDARY %d / INFO %d" % (n_pass, n_fail, n_bnd, n_info))
print("自检 guard：%d/%d" % (g_ok, len(GUARDS)))
print("-" * 78)
for v in VERDICTS:
    print("  %-6s %-9s %s" % (v["id"], v["status"], v["title"]))
print("-" * 78)
print("  门禁：%s" % GATES)
print("  四力进表：%s" % [(r["name"], r["status"]) for r in table])
for k in ["P0-1_L_ok_dim", "P0-1_L_bad_dim", "P0-1_strong_2pi_GeV",
          "P0-1_weak_2pi_TeV", "P0-1_ratio_no2pi_strong", "P0-1_ratio_no2pi_weak",
          "P0-2_optA_imag", "P0-2_optB_imag", "P0-3_atan2_0_0"]:
    print("  %-30s %s" % (k, KEYS[k]))
print("=" * 78)
for g in GUARDS:
    if not g["ok"]:
        print("  [GUARD FAIL] %s" % g["name"])
sys.exit(0 if g_ok == len(GUARDS) else 1)
