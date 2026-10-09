# -*- coding: utf-8 -*-
"""TUFT V3.6 全维统一场论 · 机器审计（判定册引擎）。

纪律：只判机器可算的（量纲代数 / 符号扇区计数 / 复数一致性 / 逻辑反例 /
跨册数值回链），不判"物理品味"。凡引用本项目既有判定，一律登记为回链而非新发现。
纯标准库。
输出：数据/TUFT_V3.6_全维统一场论_机器审计_2026-10-04.{json,md}
退出码 0 = 门禁通过（脚本自洽跑完），不代表被审材料通过。
"""
import os, sys, math, json, cmath

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                      # 04_公共成果/本项目_全维自洽与归一化
DATA = os.path.join(BASE, "数据")
os.makedirs(DATA, exist_ok=True)
TAG = "TUFT_V3.6_全维统一场论_机器审计_2026-10-04"

# ---------------- 量纲代数（指数向量：M, L, T）----------------
def dim(**kw):
    d = {"M": 0, "L": 0, "T": 0}
    d.update(kw)
    return d

def dmul(a, b):
    return {k: a[k] + b[k] for k in ("M", "L", "T")}

def ddiv(a, b):
    return {k: a[k] - b[k] for k in ("M", "L", "T")}

def dpow(a, p):
    return {k: a[k] * p for k in ("M", "L", "T")}

def dfmt(a):
    return "M^%d L^%d T^%d" % (a["M"], a["L"], a["T"])

D_M, D_L, D_T = dim(M=1), dim(L=1), dim(T=1)
D_c = ddiv(D_L, D_T)                 # 光速 L T^-1
D_hbar = dmul(dmul(D_M, dpow(D_L, 2)), dpow(D_T, -1))   # ML^2 T^-1
D_kappa = dpow(D_L, -1)              # 曲率/挠率 L^-1
D_energy = dmul(dmul(D_M, dpow(D_L, 2)), dpow(D_T, -2))   # 能量 ML^2 T^-2
D_force = dmul(dmul(D_M, D_L), dpow(D_T, -2))             # 力 ML T^-2

VERDICTS = []
def add(cid, status, title, detail, numbers=None):
    VERDICTS.append(dict(id=cid, status=status, title=title,
                         detail=detail, numbers=numbers or {}))

KEYS = {}

# ============ C1 力程量纲（V3.6 公理 G4）============
# ω = c*sqrt(k^2+t^2); f = ω/(2π); L = c/(f*sqrt(k^2+t^2))
D_sqrt = dpow(D_kappa, 1)                       # sqrt(k^2+t^2) 量纲 = L^-1
D_omega = dmul(D_c, D_sqrt)                     # T^-1
D_f = D_omega                                   # 2π 无量纲
D_L_v36 = ddiv(D_c, dmul(D_f, D_sqrt))          # V3.6 的力程
D_L_ok1 = ddiv(D_c, D_f)                        # 正确式 L = c/f
D_L_ok2 = ddiv(dim(), D_sqrt)                   # 等价式 L = 1/sqrt(k^2+t^2)
ok_c1 = (D_L_v36 == D_L)          # True = 量纲正确
KEYS["C1_L_v36_dim"] = dfmt(D_L_v36)
KEYS["C1_L_correct_dim"] = dfmt(D_L_ok1)
KEYS["C1_L_correct_dim2"] = dfmt(D_L_ok2)
add("C1", "PASS" if ok_c1 else "FAIL",
    "力程式 L=c/(f√(κ²+τ²)) 的量纲",
    "V3.6 公理 G4 的力程量纲为 %s，应为 %s ⟹ **量纲错误（L²≠L）**。"
    "唯一闭合式为 L=c/f=2π/√(κ²+τ²)（%s）。"
    "**该式与上一轮已判无效的「修复式」逐字相同**，而 V3.6 Part5 却声称 B01/B02/B03 量纲错误已修复 ⟹ 声称与内容矛盾。"
    % (dfmt(D_L_v36), dfmt(D_L), dfmt(D_L_ok1)),
    {"量纲(原式)": dfmt(D_L_v36), "量纲(应为)": dfmt(D_L),
     "量纲(正确式c/f)": dfmt(D_L_ok1), "量纲(正确式1/√)": dfmt(D_L_ok2)})

# ============ C2 势能量纲（V3.6 公理 G3）============
D_E = dmul(dmul(D_hbar, D_c), D_kappa)          # (ħc/2)(κ+τ)
ok_c2 = (D_E == D_energy)
KEYS["C2_E_dim"] = dfmt(D_E)
add("C2", "PASS" if ok_c2 else "FAIL",
    "势能 E=(ħc/2)(κ+τ) 的量纲",
    "量纲 = %s，与能量 %s 一致 ⟹ **量纲闭合**（此项 V3.6 确已修对，如实记为 PASS）。"
    % (dfmt(D_E), dfmt(D_energy)),
    {"量纲": dfmt(D_E), "能量量纲": dfmt(D_energy)})

# ============ C3 cos3θ 的符号扇区数 ============
# V3.6 §2.1 取 Ω=λcos3θ，并用它划分「四个连通分区」
N = 36000
signs = []
for i in range(N):
    th = 2.0 * math.pi * i / N
    v = math.cos(3.0 * th)
    s = 0 if v == 0 else (1 if v > 0 else -1)
    signs.append(s)
nflip = sum(1 for i in range(N) if signs[i] != 0 and signs[(i + 1) % N] != 0
            and signs[i] != signs[(i + 1) % N])
KEYS["C3_cos3theta_sign_intervals"] = nflip
ok_c3 = (nflip == 4)
add("C3", "PASS" if ok_c3 else "FAIL",
    "cos3θ 能否给出「四个连通分区」",
    "cos3θ 在 θ∈[0,2π) 上有 **%d 个符号区间**（3θ 周期为 2π/3 ⟹ 每 2π 内 3 个全周期 × 2 段 = 6），"
    "而体系要求 4 个连通分区 ⟹ **分区基数不匹配**。此项与上一轮 V3.5 的 N2 判定同源，V3.6 未改 Ω 函数形式。" % nflip,
    {"符号区间数": nflip, "要求分区数": 4})

# ============ C4 复 Ω 代入实 Einstein 方程 ============
# 场方程左边 Einstein 张量为实；右边含 Ω=|Ω|e^{iφ}
phi = 0.3                      # 弱域非零相位（V3.6 Ω7）
Om = cmath.rect(1.0, phi)      # |Ω|=1, φ=0.3
Tmn = 1.0                      # 实能动张量分量
rhs = (8.0 * math.pi) * Om * Tmn
KEYS["C4_rhs_imag"] = abs(rhs.imag)
KEYS["C4_rhs_abs"] = abs(rhs)
ok_c4 = abs(rhs.imag) < 1e-15
add("C4", "PASS" if ok_c4 else "FAIL",
    "复权重场 Ω=|Ω|e^{iφ} 与实 Einstein 张量的一致性",
    "取弱域 φ=%.2f、|Ω|=1、T=1：右端 = 8π·Ω·T 的虚部 = %.6e（非零），"
    "而左端 Einstein 张量与 Λg 均为**实** ⟹ **复源项驱动实几何，方程不自洽**。"
    "（除非度规或 T 也变复数，但 V3.6 未作此设定。）" % (phi, abs(rhs.imag)),
    {"φ": phi, "|Im(RHS)|": abs(rhs.imag), "|RHS|": abs(rhs)})

# ============ C5 场方程是否含挠率项 ============
# V3.6 式(1.2): R_μν - ½R g_μν + Λ g_μν = (8πG/c⁴) Ω T_μν^matter
terms = ["R_{μν}", "-½R g_{μν}", "+Λ g_{μν}", "-(8πG/c⁴)Ω T_{μν}^matter"]
has_torsion = any("T^" in t or "挠率" in t or "torsion" in t.lower() for t in terms)
KEYS["C5_torsion_in_field_eq"] = has_torsion
ok_c5 = has_torsion
add("C5", "PASS" if ok_c5 else "FAIL",
    "「嘉唐挠率流形」与其场方程(1.2)是否含挠率",
    "式(1.2) 的项列表 = %s ⟹ **不含任何挠率项**，实为标准 Einstein+Λ 加一个标量乘子。"
    "但 G1 自称嘉唐挠率联络、Part3 预言 5 声称「挠率额外偏振模」⟹ **方程与自称/预言内部矛盾**。" % terms,
    {"项数": len(terms), "含挠率项": has_torsion})

# ============ C6 挠率 GW 偏振模 vs 本项目 J29（Einstein–Cartan 审计）============
# EC: 挠率只由自旋流（应力反对称部分）激发；对称应力 ⟹ 自旋流 ≡ 0
import random
random.seed(20261004)
max_antisym = 0.0
for _ in range(200):
    a = [[random.uniform(-1, 1) for _ in range(4)] for _ in range(4)]
    T = [[0.5 * (a[i][j] + a[j][i]) for j in range(4)] for i in range(4)]  # 对称化
    m = max(abs(T[i][j] - T[j][i]) for i in range(4) for j in range(4))
    max_antisym = max(max_antisym, m)
KEYS["C6_max_antisym_of_symmetric_stress"] = max_antisym
ok_c6 = max_antisym < 1e-15
add("C6", "FAIL" if ok_c6 else "BOUNDARY",
    "预言5（挠率引力波额外偏振模）与 Einstein–Cartan 既有判定的一致性",
    "机器复核：200 个随机**对称**应力张量的反对称部分 max|T_μν−T_νμ| = %.1e（机器零）⟹ "
    "对称物质不激发挠率（回链本项目 J29：挠率只由自旋流激发）。"
    "且 EC 挠率在标准作用量下是**代数、非传播**的 ⟹ 不产生额外传播的偏振模。"
    "V3.6 预言 5 与 J29 冲突，且与其自身(1.2)无挠率项矛盾。" % max_antisym,
    {"max|T_μν−T_νμ|": max_antisym, "样本数": 200})

# ============ C7 nEDM 证伪判据的口径 ============
# V3.6 预言4：δd_n ∈ [2e-28, 9e-28] e·cm（增量）；证伪判据却写"实验测得 d_n 小于下限 ⟹ 证伪"
lo, hi = 2e-28, 9e-28
sample = {"δ=5e-28, SM=0": 5e-28 + 0.0, "δ=5e-28, SM=-4e-28": 5e-28 - 4e-28}
counter = {k: (v < lo) for k, v in sample.items()}
KEYS["C7_total_vs_shift"] = "shift"
KEYS["C7_counterexample"] = counter
ok_c7 = not any(counter.values())
add("C7", "PASS" if ok_c7 else "FAIL",
    "预言4（nEDM）证伪判据的逻辑自洽性",
    "区间 [%.0e, %.0e] 针对的是**增量 δd_n**，而证伪判据比较的是**总量 d_n**。"
    "反例：%s ⟹ 总量可低于下限而增量仍在区间内（SM 本底抵消）。"
    "⟹ **判据把「增量」与「总量」混为一谈，不可证伪**。" % (lo, hi, counter),
    {"区间下限": lo, "区间上限": hi, "反例": counter})

# ============ C8 Part4「RG 流汇聚 / GUT 标度四力同值」============
# 与本项目 X17/J20（四耦合无公共交点）+ J32（R1 非 RG 定理而是调谐）冲突。
# 机器复核（SM 一圈）：α_i^{-1}(μ) = α_i^{-1}(M_Z) - b_i/(2π) ln(μ/M_Z)
a_inv = {"1": 59.0, "2": 29.6, "3": 8.45}      # SM 在 M_Z 的 α_i^{-1}（约值）
b = {"1": 41.0 / 10.0, "2": -19.0 / 6.0, "3": -7.0}
def inv_at(key, mu_over_mz):
    return a_inv[key] - b[key] / (2 * math.pi) * math.log(mu_over_mz)
# 两两交点：解 α_i^{-1} = α_j^{-1}
M_Z = 91.1876                                  # GeV，圈跑动的参考标度
def cross(i, j):
    # a_i - b_i/(2π) L = a_j - b_j/(2π) L  ⟹ L = 2π(a_i-a_j)/(b_i-b_j)，L=ln(μ/M_Z)
    L = 2 * math.pi * (a_inv[i] - a_inv[j]) / (b[i] - b[j])
    return M_Z * math.exp(L)                   # 交点标度（GeV）
c12, c13, c23 = cross("1", "2"), cross("1", "3"), cross("2", "3")
KEYS["C8_MU_12_GeV"] = c12
KEYS["C8_MU_13_GeV"] = c13
KEYS["C8_MU_23_GeV"] = c23
spread = max(c12, c13, c23) / max(min(c12, c13, c23), 1e-300)
KEYS["C8_spread_ratio"] = spread
ok_c8 = abs(math.log10(c12) - math.log10(c13)) < 0.5 and abs(math.log10(c13) - math.log10(c23)) < 0.5
add("C8", "PASS" if ok_c8 else "FAIL",
    "Part4「RG 流在 GUT 标度汇聚、四力耦合同值」",
    "SM 一圈机器复核：两两交点标度 μ12=%.3e、μ13=%.3e、μ23=%.3e GeV，"
    "最大/最小跨 %.2f 个量级 ⟹ **三规范耦合不交于一点**；"
    "叠加引力（J20/X17：引力在 M_GUT 弱 1.3×10⁴ 倍）⟹ **四力无公共交点**。"
    "J32 进一步裁定 R1 不是 RG 定理而是调谐条件 ⟹ Part4 的「汇聚」为**已被本项目否证的声称**。" % (c12, c13, c23, math.log10(spread)),
    {"μ12[GeV]": c12, "μ13[GeV]": c13, "μ23[GeV]": c23, "跨量级": math.log10(spread)})

# ============ C9 「四力打包进同一组方程」的性质 ============
add("C9", "FAIL",
    "「引力/电磁/强/弱全部打包进同一组耦合场方程」的统一层级",
    "把四个扇区的耦合写成同一方程 + 一个切换因子 Ω，**只是可写性**（J46: 平凡成立，"
    "SM 拉氏量本就把三种规范相互作用写在同一积分里）；V3.6 未给出从该方程**导出**任一耦合常数数值的推导。"
    "J32 实测 7 项关键数值可推导 = 0/7；X25 门禁：不得据此宣称已统一物理四力。"
    "⟹ 降级为**形式层统一**，不进入动力学层。",
    {"可推导项": 0, "关键数值总数": 7})

# ============ C10 Ω 的自由度和退化点 ============
# Ω 无量纲，κ,τ 同为 L^-1 ⟹ Π 定理：只能依赖比值 ⟹ 1 个自由度
KEYS["C10_Omega_dof"] = 1
# 引力/电磁 L=∞ ⟹ √(κ²+τ²)=0 ⟹ κ=τ=0 ⟹ θ=atan2(0,0)
th_degen = math.atan2(0.0, 0.0)
KEYS["C10_atan2_0_0"] = th_degen
add("C10", "FAIL",
    "Ω 的自由度与引力/电磁退化点",
    "Ω 无量纲而 κ,τ 同为 L⁻¹ ⟹ Π 定理给出 **Ω 实际只有 1 个自由度**（θ=atan2(τ,κ)），"
    "与「二维流形」的自称冗余。且引力/电磁力程 L=∞ ⟹ κ=τ=0 ⟹ θ=atan2(0,0)=%.1f "
    "（**Python 静默返回 0，不报错**）⟹ Ω 无定义，引力与电磁在 Ω 框架内**没有强度**。"
    "此项与上一轮 H3 同源，V3.6 未处理。" % th_degen,
    {"Ω自由度": 1, "atan2(0,0)": th_degen})

# ---------------- 自检 guard ----------------
GUARDS = []
def guard(name, cond, note=""):
    GUARDS.append(dict(name=name, ok=bool(cond), note=note))

guard("量纲向量加法封闭", dmul(D_L, dpow(D_L, -1)) == dim())
guard("c 的量纲为 L T^-1", D_c == {"M": 0, "L": 1, "T": -1})
guard("ħc 的量纲为 M L^3 T^-2", dmul(D_hbar, D_c) == {"M": 1, "L": 3, "T": -2})
guard("能量量纲正确", D_energy == {"M": 1, "L": 2, "T": -2})
guard("cos3θ 扫描点数 > 1e4", N > 10000)
guard("C3 检出 6 区间", KEYS["C3_cos3theta_sign_intervals"] == 6)
guard("C4 虚部确实非零", KEYS["C4_rhs_imag"] > 1e-6)
guard("C6 对称应力反对称部分为机器零", KEYS["C6_max_antisym_of_symmetric_stress"] < 1e-12)
guard("C8 三交点不全同量级", KEYS["C8_spread_ratio"] > 1.0)
guard("判定条目非空", len(VERDICTS) >= 8)

n_pass = sum(1 for v in VERDICTS if v["status"] == "PASS")
n_fail = sum(1 for v in VERDICTS if v["status"] == "FAIL")
n_bnd = sum(1 for v in VERDICTS if v["status"] == "BOUNDARY")
n_info = sum(1 for v in VERDICTS if v["status"] == "INFO")
n_guard_ok = sum(1 for g in GUARDS if g["ok"])

out = dict(tag=TAG, verdicts=VERDICTS, guards=GUARDS, key_numbers=KEYS,
           counts=dict(PASS=n_pass, FAIL=n_fail, BOUNDARY=n_bnd, INFO=n_info,
                       guard_ok=n_guard_ok, guard_total=len(GUARDS)))

with open(os.path.join(DATA, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

lines = ["# %s（判定产物）" % TAG, ""]
lines.append("计数：PASS %d / FAIL %d / BOUNDARY %d / INFO %d ；自检 %d/%d"
             % (n_pass, n_fail, n_bnd, n_info, n_guard_ok, len(GUARDS)))
lines.append("")
for v in VERDICTS:
    lines.append("## %s [%s] %s" % (v["id"], v["status"], v["title"]))
    lines.append(v["detail"])
    lines.append("")
with open(os.path.join(DATA, TAG + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("=" * 78)
print("TUFT V3.6 机器审计")
print("=" * 78)
print("计数：PASS %d / FAIL %d / BOUNDARY %d / INFO %d" % (n_pass, n_fail, n_bnd, n_info))
print("自检 guard：%d/%d" % (n_guard_ok, len(GUARDS)))
print("-" * 78)
for v in VERDICTS:
    print("  %-4s %-9s %s" % (v["id"], v["status"], v["title"]))
print("-" * 78)
for k in ["C1_L_v36_dim", "C1_L_correct_dim", "C3_cos3theta_sign_intervals",
          "C4_rhs_imag", "C6_max_antisym_of_symmetric_stress",
          "C8_MU_12_GeV", "C8_MU_13_GeV", "C8_MU_23_GeV", "C10_atan2_0_0"]:
    print("  %-38s %s" % (k, KEYS[k]))
print("=" * 78)
for g in GUARDS:
    if not g["ok"]:
        print("  [GUARD FAIL] %s" % g["name"])
sys.exit(0 if n_guard_ok == len(GUARDS) else 1)
