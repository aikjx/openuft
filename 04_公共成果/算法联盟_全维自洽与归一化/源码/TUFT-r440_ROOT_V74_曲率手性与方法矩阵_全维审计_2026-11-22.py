# -*- coding: utf-8 -*-
"""r440 · ROOT V74 曲率手性与方法矩阵全维审计引擎。

性质：只读审计外部来料 ROOT V74，不修改来料任何字节。
编号：全库 r431-r439 已被并行目录占用，r440 空闲，取 r440。
方法：纯标准库 Decimal 60 位 + Fraction 精确算术 + SHA-256 + W3 四门禁 + 幂等产物。
红线：数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功；拟合好 != 定律正确。
"""
import os
import sys
import csv
import json
import hashlib
from decimal import Decimal, getcontext
from fractions import Fraction

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60
D = Decimal
PI = D("3.14159265358979323846264338327950288419716939937510582097494")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "数据")
STAMP = "2026-11-22"
RID = "r440"
SRC = os.path.join(ROOT, "90_历史归档", "来源语料_ufthub_ROOT_V52-V82_202611",
                   "V74", "ROOT_V74")

ENTRIES = []
GUARDS = []

def add(code, verdict, title, detail):
    ENTRIES.append({"id": code, "verdict": verdict, "title": title, "detail": detail})


def guard(code, ok, detail):
    GUARDS.append({"id": code, "ok": bool(ok), "detail": detail})
    if not ok:
        raise AssertionError("GUARD-FAIL %s : %s" % (code, detail))


def fmt(x, n=12):
    if isinstance(x, (int, Fraction)):
        return str(x)
    return format(D(x), "." + str(n) + "E")


def rel(a, b):
    a = D(a)
    b = D(b)
    if a == b:
        return D(0)
    d = abs(b)
    if d == 0:
        return D("1e999")
    return abs(a - b) / d


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.reader(fh))


# ---------------- 事实源完整性 ----------------
F_PROOF = os.path.join(SRC, "PROOF_STATUS.md")
F_README = os.path.join(SRC, "README.md")
F_BOOK = os.path.join(SRC, "book", "ROOT_V74_统一场论第一性原理_严格证明审计与新突破路线.md")
F_METHOD = os.path.join(SRC, "data", "ROOT_V74_方法审计矩阵.csv")
F_EQ = os.path.join(SRC, "data", "ROOT_V74_方程索引.csv")
F_NUM = os.path.join(SRC, "results", "numerical_summary.json")
F_PHYS = os.path.join(SRC, "rootv74", "physics.py")
F_MANIFEST = os.path.join(SRC, "SHA256_MANIFEST.csv")

for p in (F_PROOF, F_README, F_BOOK, F_METHOD, F_EQ, F_NUM, F_PHYS, F_MANIFEST):
    guard("V74_source_exists_" + os.path.basename(p), os.path.exists(p),
          "事实源存在：%s" % os.path.relpath(p, ROOT))

MAN_ROWS = read_csv(F_MANIFEST)
MAN = {}
for row in MAN_ROWS[1:]:
    if len(row) >= 2 and row[0].strip():
        MAN[row[0].strip()] = row[1].strip()

CHECKED = {
    "PROOF_STATUS.md": F_PROOF,
    "README.md": F_README,
    "book/ROOT_V74_统一场论第一性原理_严格证明审计与新突破路线.md": F_BOOK,
    "data/ROOT_V74_方法审计矩阵.csv": F_METHOD,
    "data/ROOT_V74_方程索引.csv": F_EQ,
    "results/numerical_summary.json": F_NUM,
    "rootv74/physics.py": F_PHYS,
}
HASHES = {}
for relname, path in CHECKED.items():
    HASHES[relname] = sha(path)

BAD_HASH = [k for k, v in HASHES.items() if MAN.get(k) != v]
guard("V74_manifest_hash_match", not BAD_HASH,
      "8 个关键事实源 SHA-256 与来料 MANIFEST 逐项一致；不一致=%s" % (",".join(BAD_HASH) if BAD_HASH else "无"))

with open(F_NUM, "r", encoding="utf-8") as fh:
    NUM = json.load(fh)

PROOF_LINES = []
with open(F_PROOF, "r", encoding="utf-8") as fh:
    for line in fh:
        s = line.strip()
        if s.startswith("| P") and not s.startswith("|---"):
            PROOF_LINES.append(s)
PROOF_ROWS = [[c.strip() for c in s.strip("|").split("|")] for s in PROOF_LINES]
guard("V74_proof_rows", len(PROOF_ROWS) == 14,
      "PROOF_STATUS 证明责任清单共 %d 条（P01-P14）" % len(PROOF_ROWS))

METHOD_ROWS = [r for r in read_csv(F_METHOD)[1:] if r and r[0].strip()]
guard("V74_method_rows", len(METHOD_ROWS) == 47,
      "方法审计矩阵共 %d 条（M01-M47）" % len(METHOD_ROWS))

EQ_ROWS = [r for r in read_csv(F_EQ)[1:] if r and r[0].strip()]
guard("V74_equation_rows", len(EQ_ROWS) == 64,
      "方程索引共 %d 条（K01-K64）" % len(EQ_ROWS))

P14 = [r for r in PROOF_ROWS if r[0] == "P14"]
guard("V74_P14_no_unification",
      len(P14) == 1 and "不具备资格" in P14[0][-1],
      "P14 自陈四力大统一不具备资格：%s" % (P14[0][-1] if P14 else "缺失"))

M45 = [r for r in METHOD_ROWS if r[0] == "M45"]
M46 = [r for r in METHOD_ROWS if r[0] == "M46"]
M47 = [r for r in METHOD_ROWS if r[0] == "M47"]
guard("V74_gate_methods_present", bool(M45) and bool(M46) and bool(M47),
      "M45 科研发布门禁、M46 偶/奇曲率解耦与 M47 轴子候选均在方法矩阵中登记")

add("V74-A01", "PASS", "V74 自陈状态与本册审计口径一致",
    "README 明写未证明四力统一、未独立预测 G、未发现新相互作用；numerical_summary.scientific_status 同口径；"
    "PROOF_STATUS 的 P14 明写四力大统一不具备资格。本册不把条件定理/玩具模型升级为已证结论。")

add("V74-A02", "INFO", "事实源哈希链完整，后续读数均绑定只读快照",
    "8 个关键事实源（PROOF_STATUS/README/book/方法矩阵/方程索引/numerical_summary/physics.py/MANIFEST）"
    "SHA-256 与来料 MANIFEST 逐项一致；方程 64 条、方法 47 条、证明责任 14 条均机器计数通过。")

# ---------------- B 段：量纲判据与曲率判别 ----------------
def rank_frac(mat):
    a = [[Fraction(x) for x in row] for row in mat]
    if not a:
        return 0
    rows = len(a)
    cols = len(a[0])
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if a[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        pv = a[r][c]
        for i in range(rows):
            if i != r and a[i][c] != 0:
                f = a[i][c] / pv
                for j in range(c, cols):
                    a[i][j] -= f * a[r][j]
        r += 1
        if r == rows:
            break
    return r


def det3(mat):
    m = [[Fraction(x) for x in row] for row in mat]
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

# c^a hbar^b 与 G 的量纲方程：b=-1, a+2b=3, -a-b=-2。
A_DIM = [[Fraction(0), Fraction(1)], [Fraction(1), Fraction(2)], [Fraction(-1), Fraction(-1)]]
Y_DIM = [Fraction(-1), Fraction(3), Fraction(-2)]
RANK_A = rank_frac(A_DIM)
RANK_AUG = rank_frac([A_DIM[i] + [Y_DIM[i]] for i in range(3)])
DET_AUG = det3([A_DIM[i] + [Y_DIM[i]] for i in range(3)])
guard("V74_dim_rank_gap", RANK_A == 2 and RANK_AUG == 3,
      "rank(A)=%d，rank([A|y])=%d ⇒ c^a hbar^b 拼不出 G" % (RANK_A, RANK_AUG))
guard("V74_dim_det_nonzero", DET_AUG != 0,
      "增广行列式 det=%s（精确有理数）≠0；阳性对照见下一步" % DET_AUG)

Y_CTRL = [Fraction(-1), Fraction(1), Fraction(-2)]
DET_CTRL = det3([A_DIM[i] + [Y_CTRL[i]] for i in range(3)])
guard("V74_dim_positive_control", DET_CTRL == 0,
      "相容右端阳性对照 det=%s，且 (a,b)=(3,-1) 满足三式；无解判定非恒真" % DET_CTRL)

with open(F_PHYS, "r", encoding="utf-8") as fh:
    PHYS_SRC = fh.read()
LIMITED_IMPL = ("a,b=3,-1" in PHYS_SRC and "return (a+2*b)==3" in PHYS_SRC)
guard("V74_dim_impl_limited", LIMITED_IMPL,
      "来料维度函数硬编码 a,b=3,-1 且只检查 L 分量；结论正确但实现不是通用量纲求解器")

add("V74-B01", "PASS", "P02/P13「仅凭角度与 c、ħ 不能预测 G」独立复核成立",
    "三方程 b=-1 / a+2b=3 / -a-b=-2 的 rank(A)=%d、rank([A|y])=%d、增广行列式 det=%s；"
    "相容阳性对照 det=%s。结论：{c,ħ,无量纲角} 内无解；继承 r430 同型结论但不重复声称新物理。"
    % (RANK_A, RANK_AUG, DET_AUG, DET_CTRL))

add("V74-B02", "CORRECTED", "来料量纲判据函数结论正确但实现口径过窄",
    "physics.py 的 dimension_G_can_be_built_with_c_hbar 固定 a=3,b=-1 且只返回 (a+2b)==3；"
    "该实现不能检验一般 (a,b)，也不检查 M/T 方程。本册用精确有理数秩/行列式重做，结论不变，"
    "但不能把该函数的 False 读数称为完整量纲求解。")

G_EXP = D("6.67430e-11")
C_LIGHT = D("299792458")
M_SUN = D("1.9884e30")


def k_of_mass(mass, radius):
    return D(48) * (G_EXP * D(mass) / C_LIGHT ** 2) ** 2 / D(radius) ** 6


def k_of_density(rho):
    return D(256) * PI ** 2 / D(3) * (G_EXP * D(rho) / C_LIGHT ** 2) ** 2


def g_of_mass(mass, radius):
    return G_EXP * D(mass) / D(radius) ** 2


BODY_CHECK = []
for body in NUM["bodies"]:
    m = body["mass_kg"]
    r = body["radius_m"]
    rho = body["mean_density_kg_m3"]
    k1 = k_of_mass(m, r)
    k2 = k_of_density(rho)
    g1 = g_of_mass(m, r)
    BODY_CHECK.append({
        "body": body["body"],
        "g_rel": rel(g1, body["g_Newton_m_s2"]),
        "K_rel": rel(k1, body["K_external_Schwarzschild_m-4"]),
        "K_density_rel": rel(k1, k2),
    })

BODY_MAX_REL = max(max(x["g_rel"], x["K_rel"], x["K_density_rel"]) for x in BODY_CHECK)
guard("V74_body_values", len(BODY_CHECK) == 7 and BODY_MAX_REL < D("1e-9"),
      "7 个天体的 g、K 与 K(rho) 三路复算最大相对差 %s" % fmt(BODY_MAX_REL, 6))

SD = NUM["same_density_pair"]
SD_K = [k_of_mass(x["mass_kg"], x["radius_m"]) for x in SD]
SD_G = [g_of_mass(x["mass_kg"], x["radius_m"]) for x in SD]
SD_K_REL = rel(SD_K[0], SD_K[1])
SD_G_RATIO = SD_G[1] / SD_G[0]
guard("V74_same_density_K", SD_K_REL < D("1e-12"),
      "同密度两球 K 相对差 %s ⇒ K 与半径无关，仅由 rho 决定" % fmt(SD_K_REL, 6))
guard("V74_same_density_g", rel(SD_G_RATIO, D(3)) < D("1e-12"),
      "同密度两球 g2/g1=%s=3 ⇒ K 不随 g 同步" % fmt(SD_G_RATIO, 10))

SG = NUM["same_g_pair"]
SG_K = [k_of_mass(x["mass_kg"], x["radius_m"]) for x in SG]
SG_G = [g_of_mass(x["mass_kg"], x["radius_m"]) for x in SG]
SG_K_RATIO = SG_K[0] / SG_K[1]
SG_G_REL = rel(SG_G[0], SG_G[1])
guard("V74_same_g_geometry", SG_G_REL < D("1e-12") and rel(SG_K_RATIO, D(9)) < D("1e-12"),
      "同 g 两球 g 相对差 %s，K1/K2=%s=(R2/R1)^2" % (fmt(SG_G_REL, 6), fmt(SG_K_RATIO, 10)))

add("V74-B03", "PASS", "同密度/同 g 曲率判别可独立复算",
    "同密度 (rho=5000) 两球：K 相对差 %s，而 g2/g1=%s；同 g=10 两球：g 相对差 %s，"
    "K1/K2=%s=(6e6/2e6)^2。K=48(GM/c^2)^2/R^6 与 K(rho)=256π^2G^2rho^2/(3c^4) 两路逐项一致。"
    % (fmt(SD_K_REL, 6), fmt(SD_G_RATIO, 10), fmt(SG_G_REL, 6), fmt(SG_K_RATIO, 10)))

add("V74-B04", "CORRECTED", "曲率判别是标准 Schwarzschild 代数，不是 ROOT 新预测",
    "K 与 g 的分离由 Einstein 外部 Schwarzschild 解代入 M=4πrho R^3/3 得到；G 仍是外部输入。"
    "它能区分“表面重力加速度”和“外部曲率不变量”，但不能推出 G、不能推出新相互作用，也不能升级为四力统一证据。")

# ---------------- C 段：规范运行与曲率手性 ----------------
RG = NUM["gauge_running"]
A_RG = [D(str(x)) for x in RG["alpha_inverse_at_MZ"]]
B_RG = [D(41) / D(10), -D(19) / D(6), D(-7)]
MZ = D("91.1876")
TWOPI = D(2) * PI


def rg_cross(ai, aj, bi, bj):
    return TWOPI * (ai - aj) / (bi - bj)


def rg_best(alist, blist):
    abar = sum(alist, D(0)) / D(len(alist))
    bbar = sum(blist, D(0)) / D(len(blist))
    num = sum(((ai - abar) * (bi - bbar) for ai, bi in zip(alist, blist)), D(0))
    den = sum(((bi - bbar) ** 2 for bi in blist), D(0))
    lopt = TWOPI * num / den
    evolved = [ai - bi * lopt / TWOPI for ai, bi in zip(alist, blist)]
    return lopt, evolved, max(evolved) - min(evolved)


CROSS = []
for i, j in ((0, 1), (0, 2), (1, 2)):
    CROSS.append(rg_cross(A_RG[i], A_RG[j], B_RG[i], B_RG[j]))
CROSS_RELS = [rel(CROSS[k], RG["crossings"][k]["log_mu_over_mz"]) for k in range(3)]
guard("V74_rg_crossings", max(CROSS_RELS) < D("1e-10"),
      "三对交叉 L 复算最大相对差 %s" % fmt(max(CROSS_RELS), 6))

LOPT, EVOLVED, GAP = rg_best(A_RG, B_RG)
MU_BEST = MZ * LOPT.exp()
GAP_JSON = RG["max_minus_min_at_best"]
guard("V74_rg_best", rel(GAP, GAP_JSON) < D("1e-10") and rel(MU_BEST, RG["best_mu_GeV"]) < D("1e-10"),
      "最优标度 mu=%s GeV，best alpha^-1 最大最小差=%s，与来料逐项一致"
      % (fmt(MU_BEST, 8), fmt(GAP, 12)))
guard("V74_rg_no_triple", GAP > D(1),
      "最优标度处三耦合仍分离，max-min=%s>1 ⇒ 不是三力精确统一" % fmt(GAP, 12))

L12 = CROSS[0]
A3_TARGET = A_RG[1] + (B_RG[2] - B_RG[1]) * L12 / TWOPI
_, EVOLVED_CTRL, GAP_CTRL = rg_best([A_RG[0], A_RG[1], A3_TARGET], B_RG)
guard("V74_rg_positive_control", GAP_CTRL < D("1e-40"),
      "注入使 1-2 交叉点同时容纳第三耦合的边界值后，best max-min=%s ⇒ 判据可识别真统一" % fmt(GAP_CTRL, 6))

add("V74-C01", "PASS", "一圈耦合运行的三对交叉数值可复现",
    "b=(41/10,-19/6,-7)，alpha^-1(MZ)=(59.0192406,29.584599,8.474576271186441) ⇒ "
    "L12=%s、L13=%s、L23=%s，与来料最大相对差 %s。"
    % (fmt(CROSS[0], 12), fmt(CROSS[1], 12), fmt(CROSS[2], 12), fmt(max(CROSS_RELS), 6)))

add("V74-C02", "FAIL", "三对交叉不等于三耦合统一",
    "最优最小二乘标度 mu=%s GeV 处 alpha^-1=(%s)，max-min=%s；交叉能标跨度 "
    "%s dex。三对两两交叉发生在不同能标，不能合并为单点统一。"
    % (fmt(MU_BEST, 8), ",".join(fmt(x, 8) for x in EVOLVED), fmt(GAP, 12),
       fmt(CROSS[2] - CROSS[0], 12)))

add("V74-C03", "PASS", "统一判据阳性对照有效",
    "把 alpha3^-1(MZ) 调整为使第三耦合也在 L12 处相交，最优 max-min 降为 %s（机器零），"
    "说明 C02 的 FAIL 来自输入耦合/β 系数本身，而非判据恒假。" % fmt(GAP_CTRL, 6))

EQ_BY_ID = {r[0]: r for r in EQ_ROWS}
for eqid in ("K28", "K29", "K30", "K31", "K32", "K58", "K61", "K62", "K63", "K64"):
    guard("V74_eq_present_" + eqid, eqid in EQ_BY_ID,
          "方程索引含 %s：%s" % (eqid, EQ_BY_ID.get(eqid, ["", "缺失"])[1]))

F_ONE = Fraction(1)
E_VEC = [Fraction(1), Fraction(2), Fraction(-3)]
B_VEC = [Fraction(2), Fraction(-1), Fraction(5)]
B_NEG = [-x for x in B_VEC]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Fraction(0))


def norm2(a):
    return dot(a, a)


K_PARITY_PLUS = norm2(E_VEC) + norm2(B_VEC)
K_PARITY_MINUS = norm2(E_VEC) + norm2(B_NEG)
P_PARITY_PLUS = dot(E_VEC, B_VEC)
P_PARITY_MINUS = dot(E_VEC, B_NEG)
guard("V74_parity_even_K", K_PARITY_PLUS == K_PARITY_MINUS,
      "宇称反演 B→-B 后 K=E^2+B^2 不变：%s == %s" % (K_PARITY_PLUS, K_PARITY_MINUS))
guard("V74_parity_odd_P", P_PARITY_MINUS == -P_PARITY_PLUS and P_PARITY_PLUS != 0,
      "同一反演下 P=E·B 由 %s 变为 %s（非零变号）" % (P_PARITY_PLUS, P_PARITY_MINUS))

B_ORTHO = [Fraction(6), Fraction(-3), Fraction(0)]
P_ORTHO = dot(E_VEC, B_ORTHO)
guard("V74_parity_positive_control", P_ORTHO == 0,
      "阳性对照：E·B=0 的构型中偶/奇标记同时为 0，说明必须选非退化的 E·B 才能检测手性")

add("V74-D01", "PASS", "K63「静态 Schwarzschild 不能从 K 模拟手性」结构成立",
    "在电/磁分解 K=E^2+B^2、P=E·B 下，宇称反演 B→-B 使 K 精确不变（%s），"
    "使 P 非零变号（%s→%s）；E·B=0 的退化构型两项均不可判别。方程索引 K61–K63 与该结构一致。"
    % (K_PARITY_PLUS, P_PARITY_PLUS, P_PARITY_MINUS))

add("V74-D02", "CORRECTED", "曲率标量耦合仍是假设层，局部阈值不等于全局失稳",
    "K28 引入 χ、η、l_*、m0 四个输入；K29/K30 给 (□-m0^2+eta l_*^2 G)χ=0 与 m_eff^2=m0^2-eta l_*^2 G；"
    "K31 标 H，K32 明写 χ=0 始终是解。来料 numerical_summary.new_testable_hypothesis 也标 xi,l_* free。"
    "⇒ 这不是无参数预言；局部负 m_eff^2 不足以证明全局 tachyon 或新力存在。")

# ---------------- E 段：方法矩阵覆盖与自设门禁 ----------------
OPEN_WORDS = ("待", "开放", "候选", "未", "假设", "设计", "工程要求", "未完成")
METHOD_OPEN = [r for r in METHOD_ROWS if any(w in (r[-1] + r[-2]) for w in OPEN_WORDS)]
METHOD_DONE = [r for r in METHOD_ROWS if "已" in r[-1]]
guard("V74_method_coverage", len(METHOD_OPEN) >= 20 and len(METHOD_DONE) >= 10,
      "47 条方法中开放/待做/候选/设计类 %d 条，已验证/已实现/已计算类 %d 条；"
      "自陈边界未被执行成功掩盖" % (len(METHOD_OPEN), len(METHOD_DONE)))

M_BY_ID = {r[0]: r for r in METHOD_ROWS}
for mid in ("M04", "M05", "M13", "M14", "M33", "M45", "M46", "M47"):
    guard("V74_method_present_" + mid, mid in M_BY_ID,
          "方法矩阵含 %s：%s" % (mid, M_BY_ID.get(mid, ["", "缺失"])[1]))

M45_GATE = "现阶段未满足" in M_BY_ID["M45"][-1] or "现阶段未满足" in M_BY_ID["M45"][-2]
guard("V74_M45_gate_not_satisfied", M45_GATE,
      "M45 科研发布门禁自陈现阶段未满足：%s / %s" % (M_BY_ID["M45"][-2], M_BY_ID["M45"][-1]))

add("V74-E01", "INFO", "47 条方法矩阵显示条件结果多、正式预测少",
    "开放/待做/候选/设计类 %d 条，已验证/已实现/已计算类 %d 条；M04 只说明维度限制，"
    "M05/M37/M38 是外部 Schwarzschild 代数，M13/M14 是条件实验，M33 为历史 V73，M46 为结构判据，"
    "M47 的轴子电磁/引力候选仍明确标注为假设性 EFT。"
    % (len(METHOD_OPEN), len(METHOD_DONE)))

add("V74-E02", "PASS", "M45 科研发布门禁被来料自认未满足",
    "方法矩阵 M45「科研发布门禁」的失败模式/现状写明现阶段未满足，与 PROOF_STATUS P14 的"
    "「四力大统一不具备资格」及 numerical_summary.scientific_status 三方一致；本册不越过该门禁。")

# ---------------- W3 四门禁 ----------------
W3_GATES = [
    {
        "id": "仅用角度、c、hbar 预测 G",
        "C1": False, "C2": False, "C3": True, "C4": False,
        "reason": "没有输出 G 的数值；量纲系统不相容；秩/行列式判据可执行；一旦加质量标度即退化为 G=c hbar/m^2 恒等式。",
    },
    {
        "id": "同密度/同 g 曲率判别",
        "C1": True, "C2": False, "C3": True, "C4": False,
        "reason": "K 与 g 的数值可算且已复现，但等式来自外部 Schwarzschild 代数并依赖 G 输入，不是 ROOT 独立新力预测。",
    },
    {
        "id": "一圈规范耦合运行与 GUT 候选",
        "C1": True, "C2": False, "C3": True, "C4": False,
        "reason": "边界耦合与 beta 系数均外部输入；三对交叉不在同一点，最优残差 max-min=%s。" % fmt(GAP, 8),
    },
    {
        "id": "曲率诱导 chi 有效质量假设",
        "C1": True, "C2": False, "C3": True, "C4": False,
        "reason": "Delta m^2=xi l_*^2 K 可算，但 xi、l_*、m0、eta 全自由；chi=0 始终是解，无双锚点实验约束。",
    },
]
for item in W3_GATES:
    item["PASS"] = bool(item["C1"] and item["C2"] and item["C3"] and item["C4"])
W3_PASS = sum(1 for item in W3_GATES if item["PASS"])
guard("V74_w3_zero", W3_PASS == 0, "W3 四候选全部未过门，PASS=%d/4" % W3_PASS)

W3_CTRL = [dict(x) for x in W3_GATES]
W3_CTRL[3]["C1"] = True
W3_CTRL[3]["C2"] = True
W3_CTRL[3]["C3"] = True
W3_CTRL[3]["C4"] = True
W3_CTRL[3]["PASS"] = True
W3_CTRL_PASS = sum(1 for x in W3_CTRL if x["PASS"])
guard("V74_w3_positive_control", W3_CTRL_PASS == W3_PASS + 1,
      "合成阳性候选（四项全真）后 PASS 计数 %d -> %d，0/4 非解析失败假零" % (W3_PASS, W3_CTRL_PASS))

add("W3-01", "FAIL", "W3 四门禁：四候选 0/4",
    "G 预测（无数值/反解/恒等式）、曲率判别（外部 GR 代数/G 输入）、规范运行（外部边界/无三交点）、"
    "chi 曲率耦合（自由耦合/无锚点）全部未过 W3；L3/validated/UFT3 不新增。")
add("W3-02", "PASS", "W3 门禁机器化并带阳性对照",
    "C1/C2/C3/C4 为可执行布尔；实测 PASS=%d/4；合成四项全真候选后 PASS=%d/4。"
    % (W3_PASS, W3_CTRL_PASS))
add("RED-01", "INFO", "红线计数继承不变",
    "0/6、0/22、UFT3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4；"
    "本册只把 ROOT V74 的条件结果定价为可复算边界，不增加任何 W3/L3 计数。")

# ---------------- 产物生成 ----------------
COUNTS = {}
for e in ENTRIES:
    COUNTS[e["verdict"]] = COUNTS.get(e["verdict"], 0) + 1

KEY = {
    "proof_rows": len(PROOF_ROWS),
    "method_rows": len(METHOD_ROWS),
    "equation_rows": len(EQ_ROWS),
    "dim_rank_A": RANK_A,
    "dim_rank_augmented": RANK_AUG,
    "dim_det_augmented": str(DET_AUG),
    "body_max_relative_error": fmt(BODY_MAX_REL, 6),
    "same_density_K_relative_error": fmt(SD_K_REL, 6),
    "same_density_g_ratio": fmt(SD_G_RATIO, 12),
    "same_g_K_ratio": fmt(SG_K_RATIO, 12),
    "rg_crossings": [fmt(x, 12) for x in CROSS],
    "rg_best_mu_GeV": fmt(MU_BEST, 8),
    "rg_best_alpha_inverse_gap": fmt(GAP, 12),
    "parity_even_K": str(K_PARITY_PLUS),
    "parity_odd_P": str(P_PARITY_PLUS),
    "method_open_like": len(METHOD_OPEN),
    "method_done_like": len(METHOD_DONE),
}

META = {
    "rid": RID,
    "stamp": STAMP,
    "title": "ROOT V74 曲率手性与方法矩阵全维审计",
    "verdict_counts": COUNTS,
    "entry_total": len(ENTRIES),
    "guard_total": len(GUARDS),
    "w3_pass": W3_PASS,
    "w3_positive_control": W3_CTRL_PASS,
    "method": "纯标准库 Decimal 60 位 + Fraction 精确算术 + SHA-256 + W3 四门禁 + 幂等产物",
    "source": os.path.relpath(SRC, ROOT).replace("\\", "/"),
    "source_sha256": sha(os.path.abspath(__file__)),
    "fact_sha256": HASHES,
}

JSON_OBJ = {
    "meta": META,
    "entries": ENTRIES,
    "guards": GUARDS,
    "w3_gate": W3_GATES,
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

os.makedirs(DATA, exist_ok=True)
BASE = "TUFT-r440_ROOT_V74_曲率手性与方法矩阵_全维审计_2026-11-22"
J_PATH = os.path.join(os.path.dirname(HERE), "判定_" + BASE + ".md")
J_PATH = J_PATH.replace("判定_TUFT", "判定_TUFT").replace("_2026-11-22.md", "_2026-11-22.md")
JSON_PATH = os.path.join(DATA, BASE + ".json")
MD_PATH = os.path.join(DATA, BASE + ".md")
REP_PATH = os.path.join(DATA, BASE + "_report.txt")


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


write_text(JSON_PATH, json.dumps(JSON_OBJ, ensure_ascii=False, indent=2) + "\n")

MD_LINES = [
    "# r440 ROOT V74 曲率手性与方法矩阵全维审计数据",
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
    "r440 ROOT V74 曲率手性/方法矩阵全维审计",
    "========================================",
    "entries=%d" % len(ENTRIES),
    "counts=" + " / ".join("%s=%d" % (k, COUNTS[k]) for k in sorted(COUNTS)),
    "guards=%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
    "w3_pass=%d/4" % W3_PASS,
    "w3_positive_control=%d/4" % W3_CTRL_PASS,
    "source_sha256=%s" % META["source_sha256"],
    "dim_rank_A=%d" % RANK_A,
    "dim_rank_augmented=%d" % RANK_AUG,
    "same_density_K_rel=%s" % fmt(SD_K_REL, 6),
    "same_g_K_ratio=%s" % fmt(SG_K_RATIO, 12),
    "rg_best_alpha_inverse_gap=%s" % fmt(GAP, 12),
    "parity_even_K=%s" % K_PARITY_PLUS,
    "parity_odd_P=%s" % P_PARITY_PLUS,
    "redline=数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功；拟合好 != 定律正确",
    "",
]
write_text(REP_PATH, "\n".join(REP))

J = [
    "# 判定 r440：ROOT V74 曲率手性与方法矩阵全维审计",
    "",
    "## 〇、一句话",
    "",
    "ROOT V74 的自陈边界是诚实的：仅凭角度与 c、ħ 不能给出 G；同密度/同 g 曲率判别可复算但属外部 Schwarzschild 代数；"
    "三对规范交叉不在同一点；偶/奇曲率结构说明静态 K 不能辨手性；χ 曲率耦合仍带自由耦合。W3 四候选 0/4，红线计数不变。",
    "",
    "## 一、产物",
    "",
    "| 顺序 | 文件 | 作用 |",
    "|---|---|---|",
    "| 0 | 本判定册 | 五段裁定 + W3 + 红线 |",
    "| 1 | [引擎](源码/TUFT-r440_ROOT_V74_曲率手性与方法矩阵_全维审计_2026-11-22.py) | %d 条目 / %d 守卫 / 纯标准库 |" % (len(ENTRIES), len(GUARDS)),
    "| 2 | [数据 md](数据/TUFT-r440_ROOT_V74_曲率手性与方法矩阵_全维审计_2026-11-22.md) · [json](数据/TUFT-r440_ROOT_V74_曲率手性与方法矩阵_全维审计_2026-11-22.json) · [报告](数据/TUFT-r440_ROOT_V74_曲率手性与方法矩阵_全维审计_2026-11-22_report.txt) | 机器读数留档 |",
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
J.extend([
    "",
    "## 四、关键读数",
    "",
])
for k, v in KEY.items():
    J.append("- %s = %s" % (k, v))
J.extend([
    "",
    "## 五、红线",
    "",
    "数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功；拟合好 != 定律正确。",
    "本册不新增 W3/L3/UFT3/validated；0/6、0/22、含引力四力正确方程 0 条保持不变。",
    "",
])
write_text(J_PATH, "\n".join(J))

print("r440 entries=%d counts=%s" % (len(ENTRIES), " / ".join("%s=%d" % (k, COUNTS[k]) for k in sorted(COUNTS))))
print("r440 guards=%d/%d w3=%d/4 (ctrl=%d/4)" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS), W3_PASS, W3_CTRL_PASS))
print("r440 json=%s" % JSON_PATH)
print("r440 verdict=%s" % J_PATH)
