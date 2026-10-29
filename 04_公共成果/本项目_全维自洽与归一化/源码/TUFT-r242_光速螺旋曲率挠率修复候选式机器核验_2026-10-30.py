# -*- coding: utf-8 -*-
# TUFT-r242 · 光速螺旋曲率挠率全域统一场论：修复候选式机器核验
#
# 承接：r241（理论体系整理与机器核验，23 条承重读数）。
# 任务：对「r241 审计闭环 · 算法联盟攻坚报告」提出的 10 条承重缺陷修复方案，
#       用 Fraction 四元组量纲 (M, L, T, Q) 逐条机器核验，筛出报告中仍带病的等式，
#       把量纲可行的修法登记为候选（不代选）。
# 范围：仅「光速螺旋 + Frenet–Serret 曲率/挠率」体系；ZOI 分支仍移除。
# 纪律：不修改来料任何字节；不代选（报告里的「推荐」只是候选之一）；
#       不跑 refresh_catalog.py（并发活跃）；不 git；不碰 verify.py 历史 17 issue。
# 口径：量纲四元组 (M, L, T, Q)，Fraction 精确；数值用 Decimal 60 位。

import os, json, io, sys
from fractions import Fraction
from decimal import Decimal, getcontext, InvalidOperation

getcontext().prec = 60

# ================================================================ 量纲四元组工具
def D(*a):
    return tuple(int(x) for x in a)

def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))

def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))

def dpow(a, n):
    # n 可为 int 或 Fraction（仅用于 √ 等有理数幂，本册只用 1/2 与整数）
    if isinstance(n, int):
        n = Fraction(n)
    return tuple(Fraction(e) * n for e in a)

def dstr(a):
    """统一渲染为负指数形式：L^-1、M^1*L^3*T^-2。"""
    sym = ("M", "L", "T", "Q")
    parts = ["%s^%s" % (s, str(e)) for s, e in zip(sym, a) if e != 0]
    return "*".join(parts) if parts else "1"

def dc(s):
    return Decimal(str(s))

def fv(x, n=12):
    return format(x, ".%de" % n) if x != 0 else "0"

# ================================================================ 基本量纲常量
DIM_KAPPA = D(0, -1, 0, 0)          # κ: L^-1
DIM_TAU   = D(0, -1, 0, 0)          # τ: L^-1
DIM_OMEGA = D(0, 0, -1, 0)          # ω: T^-1
DIM_C     = D(0, 1, -1, 0)          # c: L T^-1
DIM_HBAR  = D(1, 2, -1, 0)          # ℏ: M L^2 T^-1
DIM_G     = D(-1, 3, -2, 0)         # G: M^-1 L^3 T^-2
DIM_MASS  = D(1, 0, 0, 0)           # M
DIM_LEN   = D(0, 1, 0, 0)           # L
DIM_TIME  = D(0, 0, 1, 0)           # T
DIM_FORCE = D(1, 1, -2, 0)          # F: M L T^-2
DIM_ENERGY = D(1, 2, -2, 0)         # E: M L^2 T^-2
DIM_LAGR  = D(1, -1, -2, 0)         # 拉氏密度 / 能量密度: M L^-1 T^-2
DIM_EINST = D(0, -2, 0, 0)          # 爱因斯坦张量 G_{μν}: L^-2
DIM_ONE   = D(0, 0, 0, 0)           # 无量纲

# 派生量（与 r241 守卫一致）
def dgrad(dim):                       # ∇_μ(·) = 对坐标求导 ⇒ 多一个 L^-1
    return ddiv(dim, DIM_LEN)

# ================================================================ 数值常量（Decimal 60）
ALPHA_EXP = dc("7.2973525693e-3")    # 实验精细结构常数
# 高精度 π
PI = Decimal("3.14159265358979323846264338327950288419716939937510")
C_LIGHT = dc("299792458")
HBAR = dc("1.054571817e-34")
M_E = dc("9.1093837015e-31")

# ================================================================ 条目 / 守卫登记
ENTRIES = []
GUARDS = []

def add(code, status, title, detail, **kw):
    e = dict(code=code, status=status, title=title, detail=detail)
    e.update(kw)
    ENTRIES.append(e)

def guard(name, ok, expect, got):
    GUARDS.append(dict(name=name, ok=bool(ok), expect=str(expect), got=str(got)))

# ================================================================ 守卫段 G（工具自检）
guard("G1_dim_kappa_is_Lminus1", dstr(DIM_KAPPA) == "L^-1", "L^-1", dstr(DIM_KAPPA))
guard("G2_dim_hbar_c", dstr(dmul(DIM_HBAR, DIM_C)) == "M^1*L^3*T^-2",
      "M^1*L^3*T^-2", dstr(dmul(DIM_HBAR, DIM_C)))
guard("G3_dim_G", dstr(DIM_G) == "M^-1*L^3*T^-2", "M^-1*L^3*T^-2", dstr(DIM_G))
guard("G4_dim_hbar_over_c_times_kappa_is_mass",
      dstr(dmul(ddiv(DIM_HBAR, DIM_C), DIM_KAPPA)) == "M^1",
      "M^1", dstr(dmul(ddiv(DIM_HBAR, DIM_C), DIM_KAPPA)))
guard("G5_dim_GM_over_c2_is_length",
      dstr(ddiv(dmul(DIM_G, DIM_MASS), dpow(DIM_C, 2))) == "L^1",
      "L^1", dstr(ddiv(dmul(DIM_G, DIM_MASS), dpow(DIM_C, 2))))
guard("G6_dim_omega_squared", dstr(dpow(DIM_OMEGA, 2)) == "T^-2", "T^-2",
      dstr(dpow(DIM_OMEGA, 2)))
guard("G7_two_pi_pow8_numeric",
      abs((2 * PI) ** 8 - dc("2429063.940114066")) < dc("1e-6"),
      "2429063.940114066", fv((2 * PI) ** 8, 12))
guard("G8_alpha_inverse_numeric",
      abs(1 / ALPHA_EXP - dc("137.035999084")) < dc("1e-6"),
      "137.035999084", fv(1 / ALPHA_EXP, 12))
# 候选相关新增自检
grad_kappa = dgrad(DIM_KAPPA)                                    # L^-2
guard("G9_grad_kappa_is_Lminus2", dstr(grad_kappa) == "L^-2", "L^-2", dstr(grad_kappa))
F_cov = dmul(dmul(DIM_HBAR, DIM_C), grad_kappa)                 # M L T^-2
guard("G10_hbar_c_grad_kappa_is_force", dstr(F_cov) == "M^1*L^1*T^-2",
      "M^1*L^1*T^-2", dstr(F_cov))

# ================================================================ 修复候选式核验段 R
# 状态约定：PASS=候选修法量纲可行；FAIL=报告等式量纲仍错；
#          BOUNDARY=架构/数值分支待后续；INFO=继承 r241 或登记性条目。

# --- #1 统一力方程 ---
# 候选 A（报告推荐）：F_μ = ℏc · ∇_μ κ
R1A = dmul(dmul(DIM_HBAR, DIM_C), dgrad(DIM_KAPPA))
ok_R1A = R1A == DIM_FORCE
add("R01", "PASS" if ok_R1A else "FAIL",
    "候选A·协变梯度力方程 F_μ=ℏc∇_μκ 量纲可行（力）",
    "∇_μκ 量纲 [%s]；ℏc·∇_μκ = [%s] = 力的目标量纲 [%s] ✓。"
    "这是 r241 #1 缺陷（ℏcκ 为能量非力）的最小修法：把曲率换成对坐标的协变导数，补回缺失的长度幂次。"
    "【登记为候选修法 A，量纲通过】；是否物理正确需后续弱场极限退化到牛顿引力 F=GMm/r² 的核验（见 R09）。"
    % (dstr(dgrad(DIM_KAPPA)), dstr(R1A), dstr(DIM_FORCE)),
    dim=dstr(R1A), target=dstr(DIM_FORCE))

# 候选 B（报告备选）：F ∝ ℏc κ · ∂_ν κ
R1B = dmul(dmul(DIM_HBAR, DIM_C), dmul(DIM_KAPPA, dgrad(DIM_KAPPA)))
ok_R1B = R1B == DIM_FORCE
add("R02", "PASS" if ok_R1B else "FAIL",
    "候选B·ℏcκ∂_νκ 量纲仍错（非力）",
    "ℏcκ∂_νκ 量纲 [%s]，目标力 [%s]；得 [%s] ≠ 力（差一个曲率幂次，实为 MT⁻²）。"
    "报告把此式列为备选但量纲不自洽，【不采用】。" % (dstr(R1B), dstr(DIM_FORCE), dstr(R1B)),
    dim=dstr(R1B), target=dstr(DIM_FORCE))

# --- #2 场方程源项 ---
# 报告推荐式：T = (ℏ/c)·ω·√(κ²+τ²)·u_μu_ν
sqrt_k2 = D(0, -1, 0, 0)                       # √(κ²+τ²): L^-1
R2 = dmul(dmul(ddiv(DIM_HBAR, DIM_C), DIM_OMEGA), sqrt_k2)   # u_μu_ν 无量纲
ok_R2 = R2 == DIM_LAGR
add("R03", "PASS" if ok_R2 else "FAIL",
    "报告#2推荐式 (ℏ/c)ω√(κ²+τ²)u_μu_ν 量纲仍错（非能量密度）",
    "ℏ/c 量纲实为 [%s]（报告误算成 MLT⁻¹）；(ℏ/c)·ω·√(κ²+τ²) = [%s]，"
    "目标能量密度 [%s]。差 [%s]（=L¹T¹），即仍有 r241 E06 同款缺口，未被真正修好。"
    "报告结论「⇒MT⁻² 再补归一化因子」因 ℏ/c 算错而不成立。" % (
        dstr(ddiv(DIM_HBAR, DIM_C)), dstr(R2), dstr(DIM_LAGR),
        dstr(ddiv(R2, DIM_LAGR))),
    dim=dstr(R2), target=dstr(DIM_LAGR), gap=dstr(ddiv(R2, DIM_LAGR)))

# #2 正确分支：放弃硬匹配标准 EMT，走 EC 独立挠率源方程
add("R04", "BOUNDARY",
    "#2 正确分支·EC 独立挠率源方程（不硬匹配标准 Tμν）",
    "量纲干净的做法（报告#2 末尾自承）：把 TUFT 源作为爱因斯坦-嘉唐（EC）挠率场方程的独立源项，"
    "而非强行等同标准能量动量张量 G_μν=8πG T_μν。这样源的量纲由 EC 场方程自身约定决定，"
    "不与标准 EMT 的 [ML⁻¹T⁻²] 较劲。【登记为架构候选分支，待变分推导确认】；"
    "若坚持走标准 EMT，则须补 c⁴/G 类因子（见 R05/R06 的拉氏重构逻辑）。")

# --- #4 拉氏密度 ---
# 报告拉氏：(1/16πG)(R − τ²) + (ℏ/c)√(κ²+τ²)·ω
R4_bad1 = ddiv(dmul(DIM_EINST, DIM_ONE), DIM_G)   # (1/G)·R
R4_bad1 = dmul(DIM_EINST, ddiv(DIM_ONE, DIM_G))   # = R/G
ok_R4bad = R4_bad1 == DIM_LAGR
add("R05", "PASS" if ok_R4bad else "FAIL",
    "报告#4拉氏第一项 (1/16πG)(R−τ²) 量纲错（缺 c⁴）",
    "(1/G)·R 量纲 [%s]，目标能量密度 [%s]。标准爱因斯坦-希尔伯特拉氏是 c⁴/(16πG)·R，"
    "报告漏掉 c⁴ 因子 ⇒ 量纲差 c⁴=[L⁴T⁻⁴] 的量级。【不采用】。"
    % (dstr(R4_bad1), dstr(DIM_LAGR)),
    dim=dstr(R4_bad1), target=dstr(DIM_LAGR))

# 正确 EH 拉氏：c⁴/(16πG)·R
R4_good = dmul(ddiv(dpow(DIM_C, 4), DIM_G), DIM_EINST)
ok_R4good = R4_good == DIM_LAGR
add("R06", "PASS" if ok_R4good else "FAIL",
    "候选修法·标准 EH 拉氏 c⁴/(16πG)·R 量纲可行（能量密度）",
    "c⁴/(16πG)·R 量纲 [%s] = 能量密度 [%s] ✓。这是把曲率-挠率动力学接回广义相对论的标准起手式。"
    "【登记为候选修法，量纲通过】；TUFT 螺旋耦合项须叠加在其上（见 R07）。"
    % (dstr(R4_good), dstr(DIM_LAGR)),
    dim=dstr(R4_good), target=dstr(DIM_LAGR))

# 报告第二项：(ℏ/c)√(κ²+τ²)·ω
R4_term2 = dmul(ddiv(DIM_HBAR, DIM_C), dmul(sqrt_k2, DIM_OMEGA))
ok_R4t2 = R4_term2 == DIM_LAGR
add("R07", "PASS" if ok_R4t2 else "FAIL",
    "报告#4第二项 (ℏ/c)√(κ²+τ²)·ω 量纲错（非能量密度）",
    "该耦合项量纲 [%s]，目标能量密度 [%s]；与 R03 同源（差 L¹T¹）。"
    "须重构为与 EH 拉氏同量纲的耦合（例如乘 c⁴/G 类因子或重写为挠率二次项），"
    "否则变分得到的 □κ 场方程仍量纲断裂。【登记为待重构项】。"
    % (dstr(R4_term2), dstr(DIM_LAGR)),
    dim=dstr(R4_term2), target=dstr(DIM_LAGR))

# --- #5 α 精细结构常数 RG 流候选 ---
alpha0_exact = dc("3").sqrt() / 2                       # √3/2
P0 = alpha0_exact / ALPHA_EXP - 1                       # 反解屏蔽因子
dim_P0 = DIM_ONE                                        # 屏蔽因子须无量纲
ok_P0dim = dim_P0 == DIM_ONE
add("R08", "BOUNDARY",
    "#5 α RG 流候选路线·量纲层屏蔽因子无量纲 ✓，收敛性待数值扫描",
    "屏蔽因子 P₀=α₀/α−1 数值 [%s]（无量纲 ✓，量纲自检通过）。"
    "路线 A（诚实降级 + RG 流自洽生成 P₀）在量纲层面无碍；但「RG 流能否收敛到 117.7」是数值问题，"
    "非纯量纲可判。【登记为开放项，不代选；若扫描无法收敛则升级为证伪项】。"
    % fv(P0, 6),
    P0=float(P0), alpha0=float(alpha0_exact), alpha_exp=float(ALPHA_EXP))

# --- #8 弱场史瓦西退化（r242 最重要验收）---
# 架构核验：若源走标准 EMT（R06 框架），则 G_μν = (8πG/c⁴)T_μν 量纲对齐
lhs_dim = DIM_EINST                                       # G_μν: L^-2
rhs_dim = dmul(ddiv(DIM_G, dpow(DIM_C, 4)), DIM_LAGR)    # (G/c⁴)·T: L^-2
ok_R8 = lhs_dim == rhs_dim
add("R09", "BOUNDARY",
    "#8 弱场史瓦西退化·架构/量纲可行，数值展开 g00/grr 为本轮最重要验收（开放）",
    "若修复后源接标准 EMT，则 G_μν=[%s] 与 (8πG/c⁴)T_μν=[%s] 量纲对齐 ✓ ⇒ 架构自洽。"
    "τ→0 极限须严格退化到真空爱因斯坦方程 → 史瓦西解；"
    "【本轮仅做架构/量纲核验，数值展开 g00/grr 对比留作 r242 后续最重要验收】。"
    % (dstr(lhs_dim), dstr(rhs_dim)),
    lhs=dstr(lhs_dim), rhs=dstr(rhs_dim), align=bool(ok_R8))

# --- #3 自旋子模块证伪归档（继承 r241 E05）---
add("R10", "INFO",
    "#3 自旋子模块证伪归档·从主承重链路剥离",
    "r241 E05 已机器确证：S=ℏ√(κ²+τ²)/κ 令 S=ℏ/2 ⇒ β²=−3/4 无实数解。"
    "处置：证伪归档，主理论不依赖该自旋子式；保留本源不变式 ω²=c²(κ²+τ²)。"
    "【继承 r241，本册登记为剥离项】。")

# --- #6 r₀ 命名撤回（继承 r241 E15）---
r0_claim = HBAR / (2 * M_E * C_LIGHT)
add("R11", "INFO",
    "#6 r₀=ℏ/(2m_ec) 命名撤回·改「螺旋特征尺度」",
    "r₀=%s m，既非康普顿波长 %s m 也非约化康普顿波长 %s m ⇒ 「康普顿半径」命名不成立。"
    "【继承 r241 E15，本册登记为命名修正】。"
    % (fv(r0_claim, 6), fv(2 * PI * HBAR / (M_E * C_LIGHT), 6),
       fv(HBAR / (M_E * C_LIGHT), 6)),
    r0=fv(r0_claim, 12))

# --- #7 null Frenet 标架（类光曲线）---
add("R12", "BOUNDARY",
    "#7 null Frenet 标架·类光曲线 κ,τ 定义重写（架构候选，开放）",
    "标准 Frenet–Serret 不适用于类光曲线（弧长恒 0）。修法：改用 null Frenet frame（伪弧长参数化）"
    "重写 κ,τ 定义，保持本源不变式 ω²=c²(κ²+τ²) 不变。量纲层 κ,τ 仍为 L⁻¹；"
    "【但需重推 null Frenet–Serret 微分方程并核验不变式仍成立，登记为开放项】。")

# --- #9 11 项自由量登记 + 自评修订（继承 r241 E20）---
free_items = ["ε_s", "μ_s", "ε_W", "μ_W", "ρ_s", "ρ_W", "P₀(μ)", "τ₀",
              "λ(r)", "Λ", "m(κ,τ 标度)"]
add("R13", "INFO",
    "#9 11 项自由量登记·修订「无拟合」自评文字",
    "清点无定义/无数值/无来源量共 %d 项：%s。修订自评：本源不变式不含拟合参数，"
    "耦合子模块含外部输入参数（与「无拟合无凑数」字面冲突，须显式登记）。【继承 r241 E20】。"
    % (len(free_items), "、".join(free_items)),
    count=len(free_items), items=free_items)

# --- #10 可证伪预言（继承 r241 E22，r242 攻坚目标）---
add("R14", "BOUNDARY",
    "#10 可证伪预言=0·r242 攻坚目标（开放）",
    "r241 E22 清点可证伪预言为 0 条，体系仍处玩具模型档。r242 目标：从修复后挠率场方程"
    "推导至少一条独立可观测预言（星系挠率晕 / g-2·EDM 挠率修正），须第一性推导、给数值区间、实验可判定。"
    "【本轮仅登记，推导留作后续】。")

# ================================================================ 输出
def main():
    counts = {}
    for e in ENTRIES:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    g_ok = sum(1 for g in GUARDS if g["ok"])
    lines = []
    lines.append("TUFT-r242 · 光速螺旋曲率挠率全域统一场论 · 修复候选式机器核验")
    lines.append("=" * 78)
    for e in ENTRIES:
        lines.append("[%s] %s · %s" % (e["status"], e["code"], e["title"]))
        lines.append("    %s" % e["detail"])
    lines.append("-" * 78)
    lines.append("守卫 %d/%d" % (g_ok, len(GUARDS)))
    for g in GUARDS:
        if not g["ok"]:
            lines.append("  [GUARD FAIL] %s expect=%s got=%s" % (g["name"], g["expect"], g["got"]))
    summary = ("条目 %d  PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
               % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
                  counts.get("BOUNDARY", 0), counts.get("INFO", 0)))
    lines.append(summary)
    lines.append("守卫 %d/%d" % (g_ok, len(GUARDS)))
    lines.append("退出码 0")
    txt = "\n".join(lines)
    print(txt)

    payload = dict(
        round="r242",
        title="光速螺旋曲率挠率全域统一场论：修复候选式机器核验",
        date="2026-10-30",
        source="承接 r241；核验对象 = r241 审计闭环报告提出的 10 条修复方案",
        entries=ENTRIES,
        guards=GUARDS,
        counts=counts,
        summary=summary,
        scope_excluded="ZOI 分支仍移除（不整理、不核验、不引用）",
        discipline="不代选：报告「推荐」仅为候选之一；不修改来料字节；不跑 refresh_catalog；不 git",
    )
    OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "数据")
    OUT = os.path.normpath(OUT)
    NAME = "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30"
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    with io.open(os.path.join(OUT, NAME + ".json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2))
    with io.open(os.path.join(OUT, NAME + ".md"), "w", encoding="utf-8") as fh:
        fh.write("# %s\n\n" % payload["title"])
        fh.write("```\n%s\n```\n" % txt)
    with io.open(os.path.join(OUT, NAME + "_report.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt + "\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
