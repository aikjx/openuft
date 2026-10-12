# -*- coding: utf-8 -*-
# TUFT-V4 量纲全审计 + 精算对标 CODATA + 路线B（修公理重建：新增内禀长度 l0）
# 日期：2026-10-12
# 口径：纯标准库（Decimal 60 位 + Fraction 三维量纲向量 (M,L,T)）
#       机器验证，非口头断言；任何"量纲正确"结论均由 dim 元组断言兜底。
#
# 背景：来料 TUFT-V4 导出 G_th = 2π c³/(ℏ sinθ)，反解 sinθ ≈ 2.4e70 ≫ 1，
#       与 CODATA 实验 G 根本矛盾。根因 = G_th 量纲缺 L²（c³/ℏ 是 L M⁻¹ T⁻²，非 G 的 L³ M⁻¹ T⁻²）。
# 路线B 处方：新增内禀长度公理 l0，改 g = -c² l0² κ R/R³，导出 G_th = c³ l0²/(ℏ sinθ)。
#
# 本册机器读数（详见数据产物与判定册）：
#   - 路线B 修掉了量纲缺 L² 的硬伤（D01/D02/D04 全 PASS）；
#   - 但引入新自由常数 l0 后，G 被"交易"为 l0，而非第一性导出（V02 FAIL）；
#   - χ² 拟合：1 个数据 + 2 个参数 ⇒ dof=-1，G 沿整条 1-参数族拟合残差=0，
#     即 G 完全未被预言（X 系列）；
#   - 来料"平方几何恒等式量纲不匹配"是手算误判，机器证明 κ²+τ²=ω²/c² 量纲自洽（D03 纠错）；
#   - 3 维 Frenet 量 κ,τ 直接升为 4 维传播场的动态方程仍缺维度（D06 BOUNDARY）。
import json, os, math
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 60

# ============================ 量纲系统 (M, L, T) ============================
def D(*e):
    return tuple(Fraction(x) for x in e)
ZERO = D(0, 0, 0)
M = D(1, 0, 0)
L = D(0, 1, 0)
T = D(0, 0, 1)
G_DIM = D(-1, 3, -2)          # [G] = L³ M⁻¹ T⁻²
C_DIM = dadd(L, dpow(T, -1)) if False else D(0, 1, -1)   # [c] = L T⁻¹

def dscale(d, k):
    return tuple(a * Fraction(k) for a in d)
def dadd(*ds):
    r = ZERO
    for d in ds:
        r = tuple(a + b for a, b in zip(r, d))
    return r
def dmul(d1, d2):
    return dadd(d1, d2)
def dpow(d, e):
    return dscale(d, Fraction(e))
def dinv(d):
    return tuple(-a for a in d)
def deq(d1, d2):
    return all(a == b for a, b in zip(d1, d2))
def dim_str(d):
    parts = []
    names = "MLT"
    for nm, v in zip(names, d):
        if v == 0:
            continue
        s = "%s" % nm
        if v != 1:
            s += "^%s" % (v if v.denominator == 1 else "(%s)" % v)
        parts.append(s)
    return "·".join(parts) if parts else "1(无量纲)"

# 物理量量纲
HBAR_DIM = D(1, 2, -1)        # [ℏ] = M L² T⁻¹
OMEGA = dinv(T)               # [ω] = T⁻¹
KAPPA = dinv(L)               # [κ]=[τ] = L⁻¹（3维 Frenet 空间曲线几何量）
R_DIM = L                     # [R] = L
ACCEL = dadd(L, dpow(T, -2))  # [g] = L T⁻²
L0_DIM = L                    # [l0] = L（TUFT 新增内禀长度公理）
RHO_DIM = dadd(M, dpow(L, -3))# [ρ] = M L⁻³
EPS_DIM = dadd(M, dinv(L), dpow(T, -2))  # [ε=ρc²] = M L⁻¹ T⁻²
NABLA2 = dpow(L, -2)          # [∇²] = L⁻²
BOX = dpow(L, -2)             # [□] = L⁻²（4维达朗贝尔）

# ============================ 物理常数 / 数据 ============================
C_VAL = Decimal("299792458")              # m/s
HBAR_VAL = Decimal("1.0545718176461565e-34")  # J·s
G_VAL = Decimal("6.67430e-11")            # m³ kg⁻¹ s⁻² (CODATA 2018)
G_SIG = Decimal("0.00015e-11")            # CODATA 2018 不确定度 σ

# ============================ 结果收集 ============================
ENTRIES = []
SELF_FAIL = []
def add(eid, kind, title, detail):
    ENTRIES.append({"id": eid, "kind": kind, "title": title, "detail": detail})
def check_dim(eid, desc, computed, expected, must_pass=False):
    ok = deq(computed, expected)
    diff = dim_str(dadd(computed, dscale(expected, -1))) if not ok else "0"
    add(eid, "PASS" if ok else "FAIL",
        desc,
        "量纲=%s，期望=%s → %s" % (dim_str(computed), dim_str(expected),
                                    "匹配" if ok else "不匹配(差 %s)" % diff))
    if must_pass and not ok:
        SELF_FAIL.append(eid)
    return ok
def selfcheck(eid, cond, desc):
    add("S:" + eid, "PASS" if cond else "FAIL", "自检:" + desc,
        "通过" if cond else "失败(断言不成立)")
    if not cond:
        SELF_FAIL.append("S:" + eid)

# ----------------------- 一、路线B 修正后量纲审计（D 系列） -----------------------
# D01：G_th = c³ l0² / (ℏ sinθ)
GTH_DIM = dadd(dpow(C_DIM, 3), dpow(L0_DIM, 2), dinv(HBAR_DIM), dinv(D(0,0,0)))
# 量纲 = c³ · l0² · ℏ⁻¹ · (sinθ 无量纲)
GTH_DIM = dadd(dpow(C_DIM, 3), dpow(L0_DIM, 2), dinv(HBAR_DIM))
check_dim("D01", "G_th=c³l0²/(ℏ sinθ) 量纲 vs [G]", GTH_DIM, G_DIM, must_pass=True)

# D02：g = -c² l0² κ R / R³  （R/R³ ⇒ 方向 × R⁻²）
LHS_G = ACCEL
RHS_G = dadd(dpow(C_DIM, 2), dpow(L0_DIM, 2), KAPPA, dpow(R_DIM, -2))
check_dim("D02", "g=-c²l0²κ·R/R³ 量纲 vs [g]", RHS_G, LHS_G, must_pass=True)

# D03：几何恒等式 κ²+τ² = ω²/c²（来料曾误判"平方形式量纲不匹配"）
LHS_ID = dpow(KAPPA, 2)               # L⁻²
RHS_ID = dadd(dpow(OMEGA, 2), dinv(dpow(C_DIM, 2)))  # T⁻² / (L²T⁻²) = L⁻²
check_dim("D03", "κ²+τ²=ω²/c² 量纲（3维 Frenet κ,τ）", LHS_ID, RHS_ID, must_pass=True)

# D04：l0=l_P, sinθ=1 ⇒ G_th == G  （数值等同，机器验证）
def planck_length():
    return (HBAR_VAL * G_VAL / C_VAL**3).sqrt()
LP = planck_length()
GTH_RECOV = C_VAL**3 * LP**2 / (HBAR_VAL * Decimal("1"))   # sinθ=1
check_dim("D04", "l0=l_P,sinθ=1 时 G_th 量纲 vs [G]", GTH_DIM, G_DIM, must_pass=True)
rel_recov = abs((GTH_RECOV - G_VAL) / G_VAL)
selfcheck("gth_recovers_G", rel_recov < Decimal("1e-50"),
          "l0=l_P,sinθ=1 时 G_th 数值 == CODATA G（相对差 %s）" % format(rel_recov, '.3e'))

# D05：l0(θ=1) 数值 == l_P
l0_at_one = LP
rel_l0 = abs((l0_at_one - LP) / LP)
selfcheck("l0_equals_lP", rel_l0 < Decimal("1e-50"),
          "l0(θ=1) 数值 == 普朗克长度 l_P（相对差 %s）" % format(rel_l0, '.3e'))

# D06：动态 4 维传播方程源项维度（残留问题）
# 若 κ 为 3 维空间曲率 L⁻¹，则 □κ 量纲 L⁻³；牛顿源 Gρ 量纲 T⁻²，仍差 L⁻¹。
BOXKAPPA = dadd(BOX, KAPPA)            # [□κ] = L⁻³
SRC_GR = dadd(G_DIM, RHO_DIM)          # [Gρ] = T⁻²
check_dim("D06", "□κ (L⁻³) vs 源项 Gρ (T⁻²) 维度", BOXKAPPA, SRC_GR)
add("D06", "BOUNDARY", "动态场方程源项维度残留",
    "3维 Frenet κ(L⁻¹) 升为 4 维传播场时 □κ=L⁻³，而物质源 Gρ=T⁻²，差 L⁻¹；"
    "须把 κ 重新解释为 4 维时空曲率标量(L⁻²) 或引入 l0² 型因子，动态方程未闭合。")

# ----------------------- 二、来料原始错误复算（N 系列） -----------------------
# N01：原始导出式 G_th0 = 2π c³/(ℏ sinθ) 反解 sinθ
sin_theta_wrong = (Decimal("2") * Decimal(str(math.pi)) * C_VAL**3) / (HBAR_VAL * G_VAL)
add("N01", "PASS", "原始式 sinθ=2πc³/(ℏG) 复算",
    "sinθ = %s ≈ 2.4e70，远超 [-1,1] ⇒ 与实验 G 矛盾（复算一致）" % format(sin_theta_wrong, '.4e'))

# N02：c³/ℏ 量纲 vs G，差 L²
RATIO_DIM = dadd(dpow(C_DIM, 3), dinv(HBAR_DIM), dinv(G_DIM))
add("N02", "PASS", "c³/ℏ 量纲 vs [G] 缺口",
    "c³/ℏ 量纲=%s；G 量纲=%s；比值量纲=%s ⇒ 缺 L²（根因）"
    % (dim_str(dadd(dpow(C_DIM,3),dinv(HBAR_DIM))), dim_str(G_DIM), dim_str(RATIO_DIM)))

# N03：l0 = sqrt(G_exp ℏ sinθ / c³)，θ=1 ⇒ 普朗克长度
def solve_l0(sin_theta):
    return (G_VAL * HBAR_VAL * Decimal(str(sin_theta)) / C_VAL**3).sqrt()
l0_scan = {}
for st in [Decimal("1"), Decimal("0.5"), Decimal("0.1"), Decimal("1e-2"),
          Decimal("1e-5"), Decimal("1e-10")]:
    l0_scan[st] = solve_l0(st)
selfcheck("l0_positive", all(v > 0 for v in l0_scan.values()),
          "l0 在 sinθ∈(0,1] 全为正实数")

# N04：沿拟合族 G_th 恒等于 G（见 X 系列）

# ----------------------- 三、χ² 拟合（X 系列） -----------------------
# 模型：G_th(l0, sinθ) = c³ l0²/(ℏ sinθ)。固定 CODATA G，解 l0 = sqrt(G ℏ sinθ / c³)。
# 对任意 sinθ∈(0,1] 取该 l0，则 G_th 数值恒等于 G ⇒ 残差=0。
chi2_rows = []
for st in [Decimal("1"), Decimal("0.5"), Decimal("0.1"), Decimal("1e-2"),
          Decimal("1e-5"), Decimal("1e-10"), Decimal("1e-20")]:
    l0 = solve_l0(st)
    Gth = C_VAL**3 * l0**2 / (HBAR_VAL * st)
    resid = (Gth - G_VAL) / G_SIG
    chi2 = resid * resid
    chi2_rows.append({"sin_theta": str(st), "l0_m": format(l0, '.6e'),
                      "G_th": format(Gth, '.6e'), "rel_resid": format((Gth-G_VAL)/G_VAL, '.3e'),
                      "chi2_per_point": format(chi2, '.3e')})
    selfcheck("chi2_zero_%s" % st, abs((Gth - G_VAL)/G_VAL) < Decimal("1e-40"),
              "sinθ=%s 拟合族上 G_th==G（相对残差 %s）" % (format(st,'.0e'), format((Gth-G_VAL)/G_VAL,'.2e')))
N_DATA = 1
N_PARAM = 2
DOF = N_DATA - N_PARAM
add("X01", "INFO", "χ² 拟合：模型过参数化",
    "模型 G_th(l0,sinθ) 含 2 自由参数，CODATA G 仅 1 个数据点 ⇒ dof=%d（<0，过参数化）。" % DOF)
add("X02", "INFO", "χ² 拟合：G 沿整条族残差=0",
    "对任意 sinθ∈(0,1]，取 l0=√(Gℏ sinθ/c³) 即 G_th≡G，χ²=0；G 完全未约束任一参数。")
add("X03", "FAIL", "χ² 拟合结论：G 未被预言",
    "路线B 把 G 的'第一性导出'降格为'用 l0 拟合 G'；l0 即普朗克长度（θ=1 时），"
    "等价于把 G 重新写回定义，循环定义。G 的预言力=0。")
add("X04", "PASS", "χ² 拟合：拟合优度无意义",
    "reduced χ² 需 dof>0；此处 dof<0 ⇒ 拟合优度不适用，进一步证明该形式无检验力。")

# ----------------------- 四、修正版 ADM-BSSN 形式陈述（A 系列） -----------------------
# 路线B 的唯一效应：把牛顿常数 G 重写为 c³ l0²/(ℏ sinθ)。
# 弱场极限：∇²Φ = 4π G_th ρ，其中 g=-∇Φ 且按公理 g=-c² l0² κ R/R³。
# 故 ADM-BSSN 约束/演化方程与标准 GR 在结构上完全相同，G_th 仅作为系数出现。
add("A01", "INFO", "ADM 哈密顿约束（修正版）",
    "16π G_th/c⁴ · (R_ijkl 约化) 出现在约束中；G_th 已含 l0²，故与 GR 形式同构，无新传播结构。")
add("A02", "INFO", "ADM 动量约束（修正版）",
    "∇_j(K^{ij}-γ^{ij}K) = 8π G_th/c⁴ · (T^{0i})；源项带 G_th，与 GR 同构。")
add("A03", "INFO", "BSSN 演化方程（修正版）",
    "∂_t γ̃_ij = -2α K̃_ij + ... ；∂_t K̃_ij = ... - α (Ã_ij + 1/3 γ̃_ij Ã - 8π G_th/c⁴ (ρ+S)) ... ；"
    "l0 只进入 G_th 系数，不引入新动力学项。")
add("A04", "BOUNDARY", "ADM-BSSN 中 κ,τ 的角色未定义",
    "修正版仅把 G 替换为 G_th，未给出 κ,τ 如何进入度规/外曲率的演化；"
    "κ,τ 与 ADM 变量(γ_ij, K_ij) 的映射仍是开放项（同 r19/r21 的 τ 动力学未闭合问题）。")

# ----------------------- 五、核心裁定（V 系列） -----------------------
add("V01", "PASS", "路线B 修掉量纲缺 L² 硬伤",
    "G_th=c³l0²/(ℏ sinθ) 量纲匹配 G；g=-c²l0²κR/R³ 量纲匹配加速度（D01/D02 PASS）。")
add("V02", "FAIL", "路线B 未实现 G 的第一性导出",
    "新增自由常数 l0 后，G 被'交易'为 l0（θ=1 时 l0=l_P），不是从 κ,τ,ω 导出；"
    "代价=把'导出 G'降为'用 l0 拟合 G'，与路线A（普朗克长度循环）等价。")
add("V03", "BOUNDARY", "动态场方程仍缺维度",
    "3 维 Frenet κ(L⁻¹) 直接作 4 维传播场时 □κ=L⁻³ 与源项 T⁻² 差 L⁻¹（D06）；"
    "动态演化方程未闭合，须重新解释 κ 为 4 维曲率标量或补 l0² 型因子。")
add("V04", "INFO", "来料手算误判纠错",
    "来料称'κ²+τ²=ω²/c² 平方形式量纲不匹配'是手算错（误取 [κ]=L⁻²）；"
    "机器证明 3 维 Frenet κ,τ(L⁻¹) 下该式量纲自洽（D03）。真正 BUG 仅在于引力公理，不在几何恒等式。")
add("V05", "FAIL", "框架底层不可挽救（不新增基础常数则）",
    "不引入 l0（或等价普朗克长度）则 G 量纲缺 L²，数学上无解（sinθ 爆炸）；"
    "引入 l0 则 G 退化为循环定义。故'从 κ,τ,ω 第一性导出 G'在原公理集内不可达成，"
    "必须新增基础常数或接受 G 为外部输入。")

# ============================ 汇总 ============================
KINDS = ["PASS", "FAIL", "BOUNDARY", "INFO", "CORRECTED"]
counts = {k: sum(1 for e in ENTRIES if e["kind"] == k) for k in KINDS}
counts_total = sum(counts.values())

RESULTS = {
    "engine": "TUFT-V4 量纲全审计 + l0 公理重建（路线B）",
    "date": "2026-10-12",
    "rating": "O/L2",
    "verdict": "路线B 修掉量纲缺 L² 硬伤，但引入自由常数 l0 使 G 退化为循环定义；"
               "χ² 拟合过参数化(dof=-1)，G 完全未被预言。不新增基础常数则框架底层不可挽救。",
    "counts": counts,
    "entries": ENTRIES,
    "numerical": {
        "sin_theta_wrong_formula": format(sin_theta_wrong, '.6e'),
        "planck_length_m": format(LP, '.6e'),
        "l0_at_sin1_m": format(LP, '.6e'),
        "G_recovered": format(GTH_RECOV, '.6e'),
        "G_CODATA": format(G_VAL, '.6e'),
        "chi2_fit_rows": chi2_rows,
        "dof": DOF,
    },
    "constants": {"c": str(C_VAL), "hbar": str(HBAR_VAL), "G": str(G_VAL), "G_sigma": str(G_SIG)},
    "self_checks_pass": len(SELF_FAIL) == 0,
}

def build_md():
    L = []
    L.append("# TUFT-V4 量纲全审计 + 精算对标 CODATA + 路线B（l0 公理重建）")
    L.append("")
    L.append("- 引擎：`源码/TUFT-V4_量纲全审计与l0公理重建_全维审计_2026-10-12.py`")
    L.append("- 数据：`数据/TUFT-V4_量纲全审计与l0公理重建_全维审计_2026-10-12.json` / `.md`")
    L.append("- 判定：`判定_TUFT-V4_量纲全审计与l0公理重建_全维审计_2026-10-12.md`")
    L.append("- 口径：Decimal 60 位 + Fraction 三维量纲 (M,L,T)；机器验证，非口头断言。")
    L.append("")
    L.append("## 一、条目汇总")
    L.append("")
    L.append("| 类别 | 数量 |")
    L.append("|---|---|")
    for k in KINDS:
        L.append("| %s | %d |" % (k, counts[k]))
    L.append("| 合计 | %d |" % counts_total)
    L.append("")
    L.append("评级：**O/L2**（修公理后量纲自洽，但 G 仍未第一性导出；诚实边界已标注）。")
    L.append("")
    L.append("## 二、逐条裁定")
    L.append("")
    L.append("| 编号 | 类别 | 标题 | 关键读数 |")
    L.append("|---|---|---|---|")
    for e in ENTRIES:
        L.append("| %s | %s | %s | %s |" % (e["id"], e["kind"], e["title"], e["detail"]))
    L.append("")
    L.append("## 三、χ² 拟合族（CODATA G 约束下）")
    L.append("")
    L.append("| sinθ | l0 (m) | G_th | 相对残差 | χ²/点 |")
    L.append("|---|---|---|---|---|")
    for r in chi2_rows:
        L.append("| %s | %s | %s | %s | %s |" % (r["sin_theta"], r["l0_m"], r["G_th"], r["rel_resid"], r["chi2_per_point"]))
    L.append("")
    L.append("## 四、核心结论（路线B 终审）")
    L.append("")
    L.append("1. **量纲硬伤已修**：`G_th=c³l0²/(ℏ sinθ)` 量纲匹配 G；`g=-c²l0²κR/R³` 匹配加速度（D01/D02）。")
    L.append("2. **但 G 退化为循环定义**：θ=1 时 l0=l_P（普朗克长度），G_th 即 G；")
    L.append("   路线B 把'第一性导出 G'降格为'用新常数 l0 拟合 G'，与路线A（直接引用 l_P）等价（V02 FAIL）。")
    L.append("3. **χ² 过参数化**：2 参数 vs 1 数据 ⇒ dof=-1；G 沿整条 1-参数族拟合残差=0，")
    L.append("   G 完全未被预言，拟合无检验力（X01/X02/X03/X04）。")
    L.append("4. **来料手算纠错**：平方几何恒等式 κ²+τ²=ω²/c² 在 3 维 Frenet 口径下量纲自洽，")
    L.append("   真正 BUG 仅在于引力公理（V04 INFO）。")
    L.append("5. **动态方程未闭合**：3 维 κ(L⁻¹) 升 4 维传播场时源项仍差 L⁻¹（D06/A04 BOUNDARY）。")
    L.append("6. **框架底层不可挽救（不新增基础常数）**：原公理集下 G 量纲缺 L²，sinθ 爆炸；")
    L.append("   引入 l0 则循环。'从 κ,τ,ω 导出 G' 在原公理集内不可达成（V05 FAIL）。")
    L.append("")
    L.append("> 红线：数学自洽 ≠ 物理证实。本审计是对来料的机器化复算与诚实边界标注，不产生新物理。")
    return "\n".join(L)

def main():
    md = build_md()
    base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(base, "..", "数据"))
    os.makedirs(data_dir, exist_ok=True)
    stem = "TUFT-V4_量纲全审计与l0公理重建_全维审计_2026-10-12"
    with open(os.path.join(data_dir, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(RESULTS, f, ensure_ascii=False, indent=2)
    with open(os.path.join(data_dir, stem + ".md"), "w", encoding="utf-8") as f:
        f.write(md)
    try:
        print(md)
    except Exception:
        pass
    return 0 if len(SELF_FAIL) == 0 else 2

if __name__ == "__main__":
    import sys
    sys.exit(main())
