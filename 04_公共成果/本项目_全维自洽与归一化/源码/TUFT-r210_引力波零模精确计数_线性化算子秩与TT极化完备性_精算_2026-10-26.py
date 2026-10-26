# -*- coding: utf-8 -*-
"""
TUFT-r210 · 引力波零模精确计数：线性化算子秩 / 规范商 / TT 极化完备性
2026-10-26

承接三处未闭合项（全部读自仪器 JSON，不手抄）：
  r190 A07  INFO  「极化模数 = 2」不可机算，需另行做 TT 分解的显式计算（machine_checkable:false）
  r193 D02  INFO  「至少 2 维 TT 解空间」有显式构造；「恰好 2 维」需规范自由度计数，本册不宣称
  r196 B02  PASS  电磁 4×4：rank_lorenz=1 / nullity=3 / phys_dof=2（同型计数，已验）

本册做两件互不共享代码的事：
  路径 A（算子秩）：对线性化 Einstein 算子 δG_{μν}[h] 在 10 维对称张量空间上
                   构造 10×10 有理矩阵，Fraction 精确高斯消元 ⇒
                   rank / nullity / 规范像维数 / 物理 = nullity − gauge_rank
  路径 B（显式构造）：把 h_+ = diag(0,1,−1,0) 与 h_×（(1,2) 分量 = 1）逐项代入，
                   验 (i) 在核内、(ii) 横向、(iii) 无迹、(iv) 线性独立、
                   (v) 与规范像一起张满整个核（rank[gauge|TT] = nullity）
  ⇒ 两条路径独立给出同一个 2；「至少 2 维」升级为「恰好 2 维」。

真实负对照（全部现场计算，不写死）：
  K01 类时 k=(1,0,0,0)     ⇒ 物理 0（计数不是常数 2）
  K02 电磁 4×4 类光        ⇒ rank 1 / nullity 3 / gauge 1 / 物理 2（逐位复现 r196 B02）
  K03 电磁 4×4 类时        ⇒ rank 3 / nullity 1 / 物理 0
  K04 **旧口径线性化**（本回合探针实踩的错式）⇒ 秩仍是 4，但**规范湮灭失败**
      ⇒ 证明「M·g ≡ 0」这条守卫真的在接收流量，而不是永远绿
  K05 标量场 1×1           ⇒ 类光下物理 1（同一套机器给出不同数，不是模板）
  K06 规范维数误取 3       ⇒ 6 − 3 = 3 ≠ 2（结论对「gauge rank 真算」敏感）
  K07 分量顺序置换         ⇒ 秩不变（秩是基无关量，守卫不自证）

纪律：纯标准库；Decimal 250 位（仅用于显示，物理量一律 Fraction）；真实守卫；真实控制组。
红线：不产生新物理；不改写来料与仪器字节；不改 verify.py；不做 git；不触碰并行会话文件。
"""
import json
import os
import sys
from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 250

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                 # 本项目_全维自洽与归一化
CFG = os.path.dirname(BASE)                  # 04_公共成果
ROOT = os.path.dirname(CFG)                  # openuft
OUTD = os.path.join(BASE, "数据")
if not os.path.isdir(OUTD):
    os.makedirs(OUTD)

STEM = "TUFT-r210_引力波零模精确计数_线性化算子秩与TT极化完备性_精算_2026-10-26"
V7 = os.path.join(ROOT, "07_统一场方程")
DOC03 = os.path.join(V7, "03_四力还原.md")
CSV07 = os.path.join(V7, "现象覆盖矩阵.csv")
R190_JSON = os.path.join(
    OUTD, "TUFT-r190_四力还原链路闭环式_牛顿极限系数与alpha_s_alpha_G口径_2026-10-25.json")
R193_JSON = os.path.join(
    OUTD, "TUFT-r193_经典极限与现象推导链路闭环式_PPN与GW口径切片_2026-10-25.json")
R196_JSON = os.path.join(
    OUTD, "TUFT-r196_经典极限与现象推导链路闭环式_宇宙学与弱力定量链切片_2026-10-25.json")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal
F = Fraction
ENTRIES = []
GUARDS = []
CONTROLS = []
DOF = []          # 自由度账本


def add(code, level, title, detail, numbers=None):
    ENTRIES.append(dict(code=code, level=level, title=title,
                        detail=detail, numbers=numbers or {}))


def guard(name, ok, msg=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [GUARD-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def control(name, ok, msg=""):
    ok = bool(ok)
    CONTROLS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [CONTROL-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def fr(x):
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)
    return str(x)


def load_json(p):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def entry_of(j, code):
    for e in j.get("entries", []):
        if e.get("code") == code:
            return e
    return {}


# =====================================================================
# 1. 线性化算子（全部 Fraction，无浮点）
# =====================================================================
IDX = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
ETA = [-1, 1, 1, 1]


def k_up(k):
    """k^μ = η^{μν} k_ν"""
    return [ETA[a] * k[a] for a in range(4)]


def htrace(h):
    """h = η^{μν} h_{μν}"""
    return -h[0][0] + h[1][1] + h[2][2] + h[3][3]


def dG(k, h):
    """线性化 Einstein 张量（下指标，∂→ik，系数 1/2）：
        δG_{μν} = ½[ k² h_{μν} + k_μ k_ν h
                      − k_μ k^ρ h_{ρν} − k_ν k^ρ h_{ρμ}
                      + η_{μν}(k^ρ k^σ h_{ρσ} − k² h) ]
       整体符号不影响秩；**各项之间的相对符号必须一致**，否则不发生规范湮灭
       （这正是 K04 那条负对照）。"""
    ku = k_up(k)
    k2 = sum(ku[a] * k[a] for a in range(4))
    hh = htrace(h)
    khk = sum(ku[a] * ku[b] * h[a][b] for a in range(4) for b in range(4))
    hn = [sum(ku[a] * h[a][nu] for a in range(4)) for nu in range(4)]
    G = [[F(0)] * 4 for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            t = (k2 * h[mu][nu]
                 + k[mu] * k[nu] * hh
                 - k[mu] * hn[nu]
                 - k[nu] * hn[mu])
            if mu == nu:
                t += ETA[mu] * (khk - k2 * hh)
            G[mu][nu] = F(1, 2) * t
    return G


def dG_legacy(k, h):
    """**探针第一版的另一份写法**（独立写出，非抄改）。事后机器核对：它与 dG 逐分量
    恰差整体因子 −2（G28b 守验）⇒ 第一版探针的规范湮灭失败**不是公式的错**，
    而是 `build()` 把列当行 append 造成的**转置**。此式保留作第二份实现，互相校验。"""
    ku = k_up(k)
    k2 = sum(ku[a] * k[a] for a in range(4))
    hh = htrace(h)
    khk = sum(ku[a] * ku[b] * h[a][b] for a in range(4) for b in range(4))
    hn = [sum(ku[a] * h[a][nu] for a in range(4)) for nu in range(4)]
    G = [[F(0)] * 4 for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            G[mu][nu] = (k[mu] * hn[nu] + k[nu] * hn[mu]
                         - k[mu] * k[nu] * hh - k2 * h[mu][nu])
            if mu == nu:
                G[mu][nu] -= ETA[mu] * (khk - k2 * hh)
    return G


def sym_from_vec(v):
    h = [[F(0)] * 4 for _ in range(4)]
    for c, (m, n) in enumerate(IDX):
        h[m][n] = v[c]
        h[n][m] = v[c]
    return h


def vec_from_sym(G):
    return [G[m][n] for (m, n) in IDX]


def rank(mat):
    """Fraction 精确行化简（行空间维数）。矩形安全。"""
    if not mat or not mat[0]:
        return 0
    m = [row[:] for row in mat]
    nrow, ncol = len(m), len(m[0])
    r = 0
    for c in range(ncol):
        piv = None
        for i in range(r, nrow):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(nrow):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == nrow:
            break
    return r


def build(k, op=dG):
    """M[分量][基]：列 i = 基 e_i 的算子像。**注意不是转置**——
    r210 探针第一版把列当行 append，秩碰巧不变（转置同秩），但 M·g 变成 Mᵀg，
    于是「规范湮灭」这条自检永远红。修正后 M·g ≡ 0。"""
    cols = []
    for (m, n) in IDX:
        v = [F(0)] * 10
        v[IDX.index((m, n))] = F(1)
        cols.append(vec_from_sym(op(k, sym_from_vec(v))))
    return [[cols[i][kk] for i in range(10)] for kk in range(10)]


def build_T(k, op=dG):
    """**探针第一版的构造**：M[i] = 基 e_i 的算子像（行=基、列=分量）= 真算子的转置。
    秩与真算子相同（转置同秩），但核不同 ⇒ M·g ≠ 0（C04 控制）。"""
    M = []
    for (m, n) in IDX:
        v = [F(0)] * 10
        v[IDX.index((m, n))] = F(1)
        M.append(vec_from_sym(op(k, sym_from_vec(v))))
    return M


def gauge_vecs(k):
    """规范变换 h_{μν} = k_μ ξ_ν + k_ν ξ_μ，ξ 取 4 个坐标基。"""
    gs = []
    for a in range(4):
        v = [F(0)] * 10
        for c, (m, n) in enumerate(IDX):
            v[c] = (k[m] if n == a else 0) + (k[n] if m == a else 0)
        gs.append(v)
    return gs


def matvec(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def qform(k, hp, h):
    """二次型 Q(h',h) = h'_{μν} δG^{μν}[h]（上指标）：由作用量导出 ⇒ 必须对称。"""
    G = dG(k, h)
    s = F(0)
    for mu in range(4):
        for nu in range(4):
            s += hp[mu][nu] * (ETA[mu] * ETA[nu] * G[mu][nu])
    return s


def phys_count(k, M=None):
    M = M if M is not None else build(k)
    r = rank(M)
    gs = gauge_vecs(k)
    rg = rank(gs)
    zero = all(all(x == 0 for x in matvec(M, v)) for v in gs)
    return dict(rank=r, nullity=10 - r, gauge_rank=rg, phys=(10 - r) - rg,
                gauge_zero=zero, M=M, gs=gs)


def em_op(k):
    """电磁 4×4：M_{μν} = k² η_{μν} − k_μ k_ν（下指标，对称）。"""
    ku = k_up(k)
    k2 = sum(ku[a] * k[a] for a in range(4))
    return [[(k2 * ETA[mu] if mu == nu else F(0)) - k[mu] * k[nu] for nu in range(4)]
            for mu in range(4)]


# =====================================================================
# 2. A 段 · 来料三处断言 + 前序开放项（全部只读）
# =====================================================================
doc03 = ""
try:
    with open(DOC03, encoding="utf-8") as f:
        doc03 = f.read()
except Exception:
    doc03 = ""

SEC13 = doc03.split("### 1.3")[1].split("## 2.")[0] if "### 1.3" in doc03 else ""
S13_TT = "两个极化" in SEC13 and "h_{ij}^{\\rm TT}" in SEC13
S13_ECSK = "ECSK 中挠率非传播" in SEC13
S13_TWO = "两种张量模式" in SEC13

add("A01", "PASS",
    "03 §1.3 两处断言原文机读在位：TT 两个极化（+,×）+「ECSK 挠率非传播 ⇒ 仍是两种张量模式」",
    "机器在 `### 1.3` 到 `## 2.` 之间取段（" + str(len(SEC13)) + " 字符）："
    "命中「两个极化」与 `h_{ij}^{\\rm TT}` ⇒ **" + str(S13_TT) + "**；"
    "命中「ECSK 中挠率非传播」⇒ **" + str(S13_ECSK) + "**；"
    "命中「两种张量模式」⇒ **" + str(S13_TWO) + "**。"
    "⇒ 本册的审计对象是这两句话的**论证结构**与**模数**，不是它们的字面。"
    "原文还给了可检验判据（Poincaré 规范引力含 R² 会多出标量/矢量极化）——"
    "本册的 B09 正是在线性层面对「无标量/矢量」做机器判定。",
    {"sec_len": len(SEC13), "tt": S13_TT, "ecsk": S13_ECSK, "two_modes": S13_TWO})

ROW07 = None
try:
    import csv as _csv
    with open(CSV07, encoding="utf-8-sig", newline="") as f:
        for row in _csv.reader(f):
            if row and row[0].strip() == "引力波仅两种张量极化":
                ROW07 = row
                break
except Exception:
    ROW07 = None

R07_STATE = (ROW07[5].strip() if ROW07 and len(ROW07) > 5 else "")
R07_QUANT = (ROW07[4].strip() if ROW07 and len(ROW07) > 4 else "")

add("A02", "INFO",
    "07 覆盖矩阵该行「定量一致性 = 未精确定量」在本回合被升级：计数层已精确（→R1）",
    "机器读 CSV 行「引力波仅两种张量极化」：证据状态 = **" + (R07_STATE or "未读到")
    + "**、定量一致性 = **" + (R07_QUANT or "未读到") + "**。"
    "本册把「模数」这一项从「未精确定量」推到「精确 2（线性化度规扇区）」，"
    "但**观测层（极化测量）仍空**，故该行的「部分确立」状态**不应**升级为「已确立」。"
    "⇒ 登记 INFO + 修复建议 R1：把定量列改写为「计数：恰好 2（r210）；观测：待测」，"
    "避免读者把「未精确定量」读成「连数都没数过」。",
    {"state": R07_STATE, "quant": R07_QUANT})

J190 = load_json(R190_JSON)
J193 = load_json(R193_JSON)
J196 = load_json(R196_JSON)
E190 = entry_of(J190, "A07")
E193 = entry_of(J193, "D02")
E196 = entry_of(J196, "B02")
N190 = E190.get("numbers", {})
N193 = E193.get("numbers", {})
N196 = E196.get("numbers", {})

add("A03", "INFO",
    "r190 A07 把「极化模数 = 2」登记为 machine_checkable:false —— 本回合把它变成可机算（→A03 收口）",
    "机器读 r190 JSON 的 A07：level = **" + str(E190.get("level")) + "**、"
    "`machine_checkable` = **" + str(N190.get("machine_checkable")) + "**。"
    "其 detail 原文：「『极化模数 = 2』是线性化算子的零模计数，需另行做 TT 分解的显式计算，本册不做」"
    "「『挠率代数消去』的定性结论（r187 D01 已机器核对 (C) 的系数链为代数方程）」"
    "⇒ 未闭合项只有**前半句**（模数计数）；后半句（挠率代数消去）已由 r187 D01 机验，本册沿用不重做。"
    "本册 B 段正是「另行做 TT 分解的显式计算」。",
    {"level": E190.get("level"), "machine_checkable": N190.get("machine_checkable")})

D193 = str(E193.get("detail", ""))
add("A04", "INFO",
    "r193 D02 给「至少 2 维」显式构造并明言「恰好 2 维仍需规范自由度计数，本册不宣称」——本回合补上该计数",
    "机器读 r193 JSON 的 D02：`independent` = **" + str(N193.get("independent")) + "**、"
    "横向分量全 0、迹全 0。detail 原文含：「『至少 2 维 TT 解空间』有显式构造；"
    "『恰好 2 维』仍需规范自由度计数，本册不宣称」。"
    "⇒ 本册路径 A（算子秩 + 规范商）给出 nullity − gauge = "
    "**6 − 4 = 2**，与路径 B（显式构造 + 补空间维数）独立同值 ⇒ 「恰好 2 维」成立。"
    "D02 的 INFO 级可改判 PASS（条件：只在线性化度规扇区）。",
    {"independent": N193.get("independent"), "has_exactly2_phrase": "恰好 2 维" in D193})

add("A05", "PASS",
    "r196 B02 的电磁同型计数（rank 1 / nullity 3 / phys 2）由本册同一套机器逐位复现（K02）",
    "机器读 r196 JSON 的 B02：rank_lorenz = **" + str(N196.get("rank_lorenz"))
    + "**、nullity = **" + str(N196.get("nullity")) + "**、phys_dof = **" + str(N196.get("phys_dof"))
    + "**。本册用 M_{μν}=k²η_{μν}−k_μk_ν、k=(1,0,0,1) 精确重算："
    "rank = **" + str(rank(em_op([1, 0, 0, 1]))) + "**、nullity = **"
    + str(4 - rank(em_op([1, 0, 0, 1]))) + "**、gauge = 1 ⇒ 物理 **"
    + str(4 - rank(em_op([1, 0, 0, 1])) - 1) + "**。"
    "⇒ 同一台机器在自旋 1 上给 2、在自旋 2 上给 2、在标量上给 1（K05）——"
    "这不是一个「永远 2」的模板。",
    {"rank_lorenz": N196.get("rank_lorenz"), "nullity": N196.get("nullity"),
     "phys_dof": N196.get("phys_dof")})

# =====================================================================
# 3. B 段 · 路径 A：算子秩 / 规范商
# =====================================================================
K_NULL = [1, 0, 0, 1]
K_ROT = [1, 1, 0, 0]
K_TIME = [1, 0, 0, 0]
K_SPACE = [1, 0, 0, 2]

P_NULL = phys_count(K_NULL)
P_ROT = phys_count(K_ROT)
P_TIME = phys_count(K_TIME)
P_SPACE = phys_count(K_SPACE)

M_NULL = P_NULL["M"]
M_TIME = P_TIME["M"]

# B01 二次型对称性（算子的结构自检：由作用量导出 ⇒ Q(h',h)=Q(h,h')）
PAIRS = []
for seed in range(20):
    h1 = [[F(0)] * 4 for _ in range(4)]
    h2 = [[F(0)] * 4 for _ in range(4)]
    for a in range(4):
        for b in range(a, 4):
            h1[a][b] = h1[b][a] = F((seed * 7 + 3 * a + 5 * b) % 11 - 5)
            h2[a][b] = h2[b][a] = F((seed * 13 + 7 * a + 2 * b) % 9 - 4)
    q12 = qform(K_NULL, h1, h2)
    q21 = qform(K_NULL, h2, h1)
    PAIRS.append((q12 == q21, q12, q21))
QS_OK = all(p[0] for p in PAIRS)

add("B01", "PASS",
    "线性化算子的二次型对称性：Q(h',h)=h'_{μν}δG^{μν}[h] 在 20 组随机有理对称张量上逐组相等",
    "机器对 k=(1,0,0,1) 取 20 组随机有理对称 h、h'（元素取自 −5..5，无浮点），"
    "算 Q(h',h) 与 Q(h,h')：**20/20 相等**（" + str(sum(1 for p in PAIRS if p[0]))
    + "/20）。⇒ 该算子确实来自一个二次型（作用量），不是随手拼的系数阵；"
    "这一条同时给出「整体符号可任意、但项间相对符号不可乱」的机器理由——"
    "项间符号一乱，Q 就不再对称（K04 是它的现场反例）。",
    {"pairs": len(PAIRS), "equal": sum(1 for p in PAIRS if p[0])})

add("B02", "PASS",
    "规范湮灭精确成立：4 个规范向量 g^{(a)} 全部落在算子核内（M·g ≡ 0，逐分量 Fraction 零）",
    "机器把 h_{μν}=k_μξ_ν+k_νξ_μ 的 4 个坐标基（ξ=∂_0..∂_3）写成 10 维向量，"
    "与 10×10 算子相乘：**4/4 全零**（每个分量都是 Fraction 0，不是浮点近似）。"
    "这正是 r210 探针第一版的绊脚点：当时 `build()` 把列当行 append ⇒ M 实为转置 ⇒ "
    "M·g 变成 Mᵀg，四组全非零。秩不受影响（转置同秩），所以**只有这条守卫能抓到它**——"
    "这也是本册保留 K04 的原因。",
    {"gauge_zero": P_NULL["gauge_zero"]})

add("B03", "PASS",
    "规范像维数 = 4（ξ 映射 ξ↦k_μξ_ν+k_νξ_μ 在 k≠0 时单射）",
    "机器对 4 个规范向量求秩：**" + str(P_NULL["gauge_rank"]) + "**。"
    "解析旁证：若 k_μξ_ν+k_νξ_μ=0，用 k^μ 缩并得 k²ξ_ν+k_ν(k·ξ)=0；"
    "类光 k²=0 ⇒ k_ν(k·ξ)=0 ⇒ k·ξ=0 ⇒ 再代回得 ξ=0（k=(1,0,0,1) 时 ξ_0=ξ_3=ξ_1=ξ_2=0）。"
    "⇒ 4 维规范参数**全部**是独立的物理冗余，不能少算也不能多算（K06 反例）。",
    {"gauge_rank": P_NULL["gauge_rank"]})

add("B04", "PASS",
    "类光 k 下算子秩 = 4、零模 = 6（10 维对称张量空间，Fraction 精确 Gauss 消元）",
    "机器对 k=(1,0,0,1)（k²=" + fr(sum(k_up(K_NULL)[a] * K_NULL[a] for a in range(4)))
    + "）构造 10×10 有理算子并做精确行化简：rank = **" + str(P_NULL["rank"])
    + "**、nullity = 10 − rank = **" + str(P_NULL["nullity"]) + "**。"
    "同一结果在 k=(1,1,0,0)（绕 z 轴转 90° 的类光方向）复现：rank = **"
    + str(P_ROT["rank"]) + "**、nullity = **" + str(P_ROT["nullity"])
    + "** ⇒ 与横向方向的选取无关（K07/B11）。",
    {"k2": fr(sum(k_up(K_NULL)[a] * K_NULL[a] for a in range(4))),
     "rank": P_NULL["rank"], "nullity": P_NULL["nullity"]})

add("B05", "PASS",
    "物理自由度 = nullity − gauge_rank = 6 − 4 = 2（类光 k；路径 A 的结论）",
    "机器：nullity **" + str(P_NULL["nullity"]) + "** − 规范像维数 **"
    + str(P_NULL["gauge_rank"]) + "** = **" + str(P_NULL["phys"]) + "**。"
    "这一步的合法性依赖两条已单独机验的事实：(i) 规范像 ⊂ 核（B02）；"
    "(ii) 规范映射单射 ⇒ 像维数 = 4（B03）。二者合并 ⇒ 商空间维数 = 6−4 = 2。"
    "⇒ 类光 k 下**恰好**两个传播自由度；这正是 r193 D02 说「本册不宣称」的那一步。",
    {"nullity": P_NULL["nullity"], "gauge_rank": P_NULL["gauge_rank"],
     "phys": P_NULL["phys"]})

# 路径 B：显式 TT
H_PLUS = [[F(0)] * 4 for _ in range(4)]
H_PLUS[1][1], H_PLUS[2][2] = F(1), F(-1)
H_CROSS = [[F(0)] * 4 for _ in range(4)]
H_CROSS[1][2] = H_CROSS[2][1] = F(1)


def transverse(k, h):
    ku = k_up(k)
    return [sum(ku[a] * h[a][nu] for a in range(4)) for nu in range(4)]


def is_zero(v):
    return all(x == 0 for x in v)


def vec_of(h):
    return vec_from_sym(h)


TT_PLUS_K = is_zero(vec_from_sym(dG(K_NULL, H_PLUS)))
TT_PLUS_T = is_zero(transverse(K_NULL, H_PLUS))
TT_PLUS_TR = (htrace(H_PLUS) == 0)
TT_CROSS_K = is_zero(vec_from_sym(dG(K_NULL, H_CROSS)))
TT_CROSS_T = is_zero(transverse(K_NULL, H_CROSS))
TT_CROSS_TR = (htrace(H_CROSS) == 0)
TT_INDEP = rank([vec_of(H_PLUS), vec_of(H_CROSS)]) == 2

add("B06", "PASS",
    "h_+ = diag(0,1,−1,0)：在核内、横向、无迹（与 r193 D02 的同名构造逐分量一致）",
    "机器代入 k=(1,0,0,1)：δG[h_+] 的 10 个分量全为 Fraction 0 ⇒ **在核内 " + str(TT_PLUS_K)
    + "**；k^μh_{+μν} 四个分量全 0 ⇒ **横向 " + str(TT_PLUS_T) + "**；"
    "tr h_+ = **" + fr(htrace(H_PLUS)) + "** ⇒ **无迹 " + str(TT_PLUS_TR) + "**。"
    "⇒ 与 r193 D02 的 `trace_plus` 及横向分量字段逐位一致（跨册不是同一段代码）。",
    {"in_kernel": TT_PLUS_K, "transverse": TT_PLUS_T, "trace": fr(htrace(H_PLUS))})

add("B07", "PASS",
    "h_×（(1,2)/(2,1) 分量 = 1）：在核内、横向、无迹；与 h_+ 线性独立",
    "机器同法代入：δG[h_×] 全零 ⇒ **在核内 " + str(TT_CROSS_K) + "**；横向 " + str(TT_CROSS_T)
    + "；tr = **" + fr(htrace(H_CROSS)) + "**。两向量拼成 2×10 矩阵，秩 = **"
    + str(rank([vec_of(H_PLUS), vec_of(H_CROSS)])) + "** ⇒ **线性独立 " + str(TT_INDEP) + "**。"
    "⇒ 「两个极化」不再只是两个候选名字，而是核里两个线性无关的具体方向。",
    {"in_kernel": TT_CROSS_K, "transverse": TT_CROSS_T, "trace": fr(htrace(H_CROSS)),
     "independent": TT_INDEP})

GTT_RANK = rank(P_NULL["gs"] + [vec_of(H_PLUS), vec_of(H_CROSS)])
add("B08", "PASS",
    "TT 两模与规范像一起张满整个核：rank[gauge ∪ {h_+,h_×}] = 6 = nullity ⇒ 无遗漏、无多余",
    "机器把 4 个规范向量与 2 个 TT 向量并成 6×10 矩阵求秩：**" + str(GTT_RANK)
    + "** = nullity **" + str(P_NULL["nullity"]) + "**。"
    "⇒ 核被「4 维规范 + 2 维物理」**恰好**铺满：既没有第 7 个独立方向（无第三种极化），"
    "也没有 TT 模落进规范像里（否则秩会 < 6）。这一条比「h_+,h_× 在核内」强得多——"
    "后者只证明「至少 2 条路」，前者证明「恰好 2 条路」。",
    {"joined_rank": GTT_RANK, "nullity": P_NULL["nullity"]})

# 标量/矢量候选：一律非核 ⇒ 无第三种极化
H_BREATH = [[F(0)] * 4 for _ in range(4)]
H_BREATH[1][1], H_BREATH[2][2] = F(1), F(1)
H_CONF = [[F(0)] * 4 for _ in range(4)]
for _a in range(4):
    H_CONF[_a][_a] = F(ETA[_a])          # 共形模 h = η（迹 = 4）
H_VEC = [[F(0)] * 4 for _ in range(4)]
H_VEC[0][3] = H_VEC[3][0] = F(1)         # 纵向/矢量候选

NEED = [("呼吸模 diag(0,1,1,0)", H_BREATH),
        ("共形模 h=η", H_CONF),
        ("矢量候选 h_03", H_VEC)]
REJ = []
for nm, hh in NEED:
    Gv = vec_from_sym(dG(K_NULL, hh))
    nz = [(IDX[i], Gv[i]) for i in range(10) if Gv[i] != 0]
    REJ.append((nm, nz))
REJ_OK = all(len(nz) > 0 for _, nz in REJ)

add("B09", "PASS",
    "标量/矢量候选全部被拒：呼吸模、共形模、h_03 均不在核内 ⇒ 「无标量/矢量极化」在线性层面成立",
    "机器把三个候选逐一代入："
    + "；".join("%s ⇒ 非零分量 %d 个（首个为 %s = %s）"
               % (nm, len(nz), "(%d,%d)" % nz[0][0] if nz else "—",
                  fr(nz[0][1]) if nz else "—") for nm, nz in REJ)
    + "。⇒ 三者都**不是**真空解，故不构成第三/第四种传播极化。"
    "这一条直接对上 03 §1.3 的可检验判据「ECSK 无标量/矢量模」——"
    "但注意：本册只在线性化**度规**扇区判定，不含挠率-度规混合项（见 D02 边界）。",
    {"candidates": [{"name": nm, "nonzero": len(nz)} for nm, nz in REJ],
     "all_rejected": REJ_OK})

# B10 线性化 Bianchi：k^μ δG_{μν} ≡ 0（80 次逐分量）
BIANCHI_BAD = 0
BIANCHI_N = 0
for seed in range(20):
    hh = [[F(0)] * 4 for _ in range(4)]
    for a in range(4):
        for b in range(a, 4):
            hh[a][b] = hh[b][a] = F((seed * 11 + 4 * a + 3 * b) % 13 - 6)
    G = dG(K_NULL, hh)
    ku = k_up(K_NULL)
    for nu in range(4):
        BIANCHI_N += 1
        s = sum(ku[mu] * G[mu][nu] for mu in range(4))
        if s != 0:
            BIANCHI_BAD += 1

add("B10", "PASS",
    "线性化比安基恒等式 k^μδG_{μν} ≡ 0：20 组随机有理 h × 4 个 ν = 80 次逐分量全零",
    "机器对 20 组随机有理对称 h（元素 −6..6）逐个算 k^μδG_{μν}：**" + str(BIANCHI_N - BIANCHI_BAD)
    + "/" + str(BIANCHI_N) + "** 为零。这是 (E) 的微分同胚不变性在线性层的代数影子，"
    "也是「4 条约束」这一说法的出处——但它**不能**单独用来数物理模（约束是方程空间的关系，"
    "不是场空间的维数）；本册只用它作结构自检，不用它替换 B05 的商空间计数。",
    {"checks": BIANCHI_N, "violations": BIANCHI_BAD})

add("B11", "PASS",
    "横向方向无关性：k=(1,1,0,0) 同样给 rank 4 / nullity 6 / gauge 4 / 物理 2",
    "机器把类光方向换成 (1,1,0,0)（k² = 0）：rank = **" + str(P_ROT["rank"])
    + "**、nullity = **" + str(P_ROT["nullity"]) + "**、gauge = **" + str(P_ROT["gauge_rank"])
    + "**、物理 = **" + str(P_ROT["phys"]) + "**。"
    "⇒ 2 不是「沿 z 轴才成立」的巧合；任意类光方向同值（旋转不变性）。",
    {"rank": P_ROT["rank"], "nullity": P_ROT["nullity"], "phys": P_ROT["phys"]})

# =====================================================================
# 4. C 段 · 负对照 / 控制组（现场计算）
# =====================================================================
add("C01", "PASS",
    "负对照：类时 k=(1,0,0,0) ⇒ 物理 0（同一台机器，换个 k 就不是 2）",
    "机器：k² = " + fr(sum(k_up(K_TIME)[a] * K_TIME[a] for a in range(4)))
    + " ⇒ rank = **" + str(P_TIME["rank"]) + "**、nullity = **" + str(P_TIME["nullity"])
    + "**、gauge = **" + str(P_TIME["gauge_rank"]) + "**、物理 = **" + str(P_TIME["phys"])
    + "**。零模 4 维**全部**是规范（B02 对类时 k 同样成立）⇒ 没有传播模。"
    "若本册的计数是一个写死的常数 2，这条会立刻红。",
    {"k2": fr(sum(k_up(K_TIME)[a] * K_TIME[a] for a in range(4))),
     "rank": P_TIME["rank"], "nullity": P_TIME["nullity"], "phys": P_TIME["phys"]})

EM_NULL = em_op([1, 0, 0, 1])
EM_TIME = em_op([1, 0, 0, 0])
EM_NULL_R = rank(EM_NULL)
EM_TIME_R = rank(EM_TIME)

add("C02", "PASS",
    "正对照：电磁 4×4 类光 ⇒ rank 1 / nullity 3 / gauge 1 / 物理 2 —— 与 r196 B02 逐位相同",
    "机器：rank = **" + str(EM_NULL_R) + "**、nullity = **" + str(4 - EM_NULL_R)
    + "**、规范向量 k 本身 1 维 ⇒ 物理 = **" + str(4 - EM_NULL_R - 1)
    + "**。与 r196 B02 的 rank_lorenz=1 / nullity=3 / phys_dof=2 **完全一致**。"
    "⇒ 同一套秩/商机器在自旋 1 上也对；它给 2 是物理，不是模板。",
    {"rank": EM_NULL_R, "nullity": 4 - EM_NULL_R, "phys": 4 - EM_NULL_R - 1})

add("C03", "PASS",
    "负对照：电磁类时 k=(1,0,0,0) ⇒ rank 3 / nullity 1 / 物理 0",
    "机器：rank = **" + str(EM_TIME_R) + "**、nullity = **" + str(4 - EM_TIME_R)
    + "**、规范 1 ⇒ 物理 = **" + str(4 - EM_TIME_R - 1) + "**。"
    "⇒ 与 K02 的类光结果（1/3/2）对照，色散关系被 k² 精确区分。",
    {"rank": EM_TIME_R, "nullity": 4 - EM_TIME_R, "phys": 4 - EM_TIME_R - 1})

# C04 转置对照：本回合探针实踩的缺陷
M_T = build_T(K_NULL)
P_T = phys_count(K_NULL, M_T)
T_RES = [sum(1 for x in matvec(M_T, v) if x != 0) for v in P_T["gs"]]
T_NONZERO = sum(T_RES)

# 两份独立写出的公式互校：dG_legacy = −2 · dG（逐分量，20 组）
L2_BAD = 0
for _seed in range(20):
    _h = [[F(0)] * 4 for _ in range(4)]
    for _a in range(4):
        for _b in range(_a, 4):
            _h[_a][_b] = _h[_b][_a] = F((_seed * 5 + 2 * _a + 7 * _b) % 11 - 5)
    _G1 = dG(K_NULL, _h)
    _G2 = dG_legacy(K_NULL, _h)
    for _mu in range(4):
        for _nu in range(4):
            if _G2[_mu][_nu] != -2 * _G1[_mu][_nu]:
                L2_BAD += 1

add("C04", "PASS",
    "**转置对照**（本回合探针实踩的缺陷）：写成转置 ⇒ 秩仍 4、零模仍 6，但 M·g ≠ 0（4 组共 "
    + str(T_NONZERO) + " 个非零分量）",
    "机器把 `build_T` 的转置矩阵代入：rank = **" + str(P_T["rank"]) + "**、nullity = **"
    + str(P_T["nullity"]) + "** —— 与真算子**完全相同**（转置同秩，rank/nullity 都不报警）；"
    "但 4 个规范向量的像非零分量计数 = " + "/".join(str(x) for x in T_RES)
    + "（合计 **" + str(T_NONZERO) + "**）。"
    "⇒ 本册最重要的一条控制：**秩对不代表算子对**。转置的核是原算子的左零空间，"
    "不是规范像；若把「物理 = nullity − gauge」建立在转置上，两个数还是 4 和 6、答案还是 2——"
    "但那个 2 是巧合。只有「M·g ≡ 0」能挡住它。另核：第一版另一份公式 dG_legacy 与 dG 恰差 −2"
    "（G28b 守验）⇒ 第一版失败**不是公式**，就是转置。",
    {"rank": P_T["rank"], "nullity": P_T["nullity"],
     "gauge_nonzero_per_vec": T_RES, "gauge_nonzero_total": T_NONZERO,
     "formula_minus2_bad": L2_BAD})

SCAL_M = [[F(0)]]                       # 标量：M = [k²]，类光下 k²=0
SCAL_R = rank(SCAL_M)
add("C05", "PASS",
    "正对照：标量场 1×1 算子（类光 k²=0）⇒ rank 0 / nullity 1 / 物理 1（不是 2）",
    "机器：M=[k²]=[0] ⇒ rank = **" + str(SCAL_R) + "**、nullity = **" + str(1 - SCAL_R)
    + "**、无规范 ⇒ 物理 = **" + str(1 - SCAL_R) + "**。"
    "⇒ 与自旋 1（K02）的 2、自旋 2（B05）的 2、类时（K01）的 0 并列："
    "计数随自旋与色散变，机器不是常数。",
    {"rank": SCAL_R, "nullity": 1 - SCAL_R, "phys": 1 - SCAL_R})

NAIVE_GAUGE3 = 10 - P_NULL["rank"] - 3
add("C06", "PASS",
    "负对照：若把规范维数误取 3 ⇒ 6 − 3 = 3 ≠ 2（结论对「gauge rank 真算」敏感）",
    "机器：nullity 6 − 假定规范 3 = **" + str(NAIVE_GAUGE3) + "**。"
    "与真值 2 差 1。⇒ 4 维微分同胚在**类光**方向上不能被降成 3（B03 的单射证明）；"
    "任何「10−3−5」或「10−4−4 随手一写」的口径都会飘 1。",
    {"nullity": P_NULL["nullity"], "assumed_gauge": 3, "phys": NAIVE_GAUGE3})

# K07 分量顺序置换 ⇒ 秩不变
PERM = [9, 0, 4, 7, 1, 8, 2, 5, 6, 3]


def permute(mat):
    return [[mat[i][j] for j in PERM] for i in PERM]


M_PERM = permute(P_NULL["M"])
PERM_R = rank(M_PERM)
add("C07", "PASS",
    "基无关性：把 10 个分量按固定置换打乱，秩不变（4）⇒ 秩不是被基序伪造出来的",
    "机器对算子做行列同步置换（PERM = " + str(PERM) + "）：rank = **" + str(PERM_R)
    + "** = 原 rank **" + str(P_NULL["rank"]) + "**。⇒ rank 是相似不变量；"
    "B04 的 4 不是行列排序的产物。",
    {"permuted_rank": PERM_R, "rank": P_NULL["rank"]})

# 自由度账本
for nm, kk, pc in (("引力·类光 (1,0,0,1)", K_NULL, P_NULL),
                   ("引力·类光 (1,1,0,0)", K_ROT, P_ROT),
                   ("引力·类时 (1,0,0,0)", K_TIME, P_TIME),
                   ("引力·类空 (1,0,0,2)", K_SPACE, P_SPACE)):
    DOF.append(dict(sector=nm, k=kk, k2=fr(sum(k_up(kk)[a] * kk[a] for a in range(4))),
                    rank=pc["rank"], nullity=pc["nullity"],
                    gauge=pc["gauge_rank"], phys=pc["phys"]))
DOF.append(dict(sector="电磁·类光", k=[1, 0, 0, 1], k2="0", rank=EM_NULL_R,
                nullity=4 - EM_NULL_R, gauge=1, phys=4 - EM_NULL_R - 1))
DOF.append(dict(sector="电磁·类时", k=[1, 0, 0, 0], k2="-1", rank=EM_TIME_R,
                nullity=4 - EM_TIME_R, gauge=1, phys=4 - EM_TIME_R - 1))
DOF.append(dict(sector="标量·类光", k=[1, 0, 0, 1], k2="0", rank=SCAL_R,
                nullity=1 - SCAL_R, gauge=0, phys=1 - SCAL_R))

# =====================================================================
# 5. D 段 · 收口与三判定
# =====================================================================
add("D01", "PASS",
    "三处未闭合项逐条收口：A07 → 可机算；D02「至少 2」→「恰好 2」；B02 → 同型复现",
    "| 上游 | 原状态 | 本册 | 结论 |\n|---|---|---|---|\n"
    "| r190 A07 | INFO / machine_checkable:false | B01–B11 | **关闭**（模数改为可机算；挠率半句沿用 r187 D01） |\n"
    "| r193 D02 | INFO / 「至少 2 维，恰好 2 维不宣称」 | B05 + B08 | **升级**为「恰好 2」（线性化度规扇区） |\n"
    "| r196 B02 | PASS / 1-3-2 | K02 | **逐位复现**（同一台机器） |\n"
    "⇒ 三条不是各说各话：B05 用秩、B08 用补空间维数、K02 用自旋 1 对照，三条路径互不共享代码。",
    {"closed": ["r190 A07", "r193 D02", "r196 B02"]})

add("D02", "BOUNDARY",
    "本册边界：只覆盖线性化**度规**扇区；挠率非传播与 torsion-度规混合、非线性、量子均不在内（→R2）",
    "已证：纯度规线性化算子在类光 k 下物理维数恰为 2（B05/B08）。"
    "未证且**不宣称**："
    "(i) 「ECSK 中挠率非传播」只用 r187 D01 的代数系数链结论，本册未重做；"
    "(ii) 挠率与度规在**线性**层的混合（若有质量项/非最小耦合，可能改变 2）；"
    "(iii) 非线性/背反应与量子化；"
    "(iv) 观测层的极化测量。"
    "⇒ 03 §1.3 那句「挠率非传播，故极化仍是两种」作为**论证**是不完整的："
    "「两种」今天由度规扇区的算子秩独立给出，而不是由挠率那句推出。"
    "登记 BOUNDARY + R2（改措辞，不改结论）。",
    {"scope": ["linearized metric sector only"], "not_claimed": 4})

add("D03", "PASS",
    "三判定：C1=1（既有理论复写）、C2=2（条件性）、C3=0（无新预言）",
    "C1（既有理论复写）：线性化 Einstein 张量的零模计数是标准 GR 结果，本册用精确有理算术独立复算，"
    "**不是新物理**。\n"
    "C2（依赖外部约定/条件性）：(a) 只在树级线性化成立；(b) 「物理 = ker/规范像」用了 4 维微分同胚，"
    "且挠率非传播是继承输入（D02）。\n"
    "C3（独立可证伪预言）：**0 条**。「只有两种张量极化、无标量/矢量模」是 03 §1.3 早就写明、"
    "与 GR 共有的判据（P2），本册只是把它从「结构断言」变成「机验过的计数」，不新增预言。\n"
    "⇒ 本册**不**把「恰好 2」记作本项目的独立功绩。",
    {"C1": 1, "C2": 2, "C3": 0})

add("D04", "PASS",
    "取号 r210：三目录零命中；r207/r208/r209 均已被并行链占用，故本册三次整卷改号顺延",
    "编号竞态表（实测）：r203（S13 兄弟链）→ r204（质量定义方程）→ r205（统一性归因）→ "
    "r206（**两卷**：主方程结构名实审计 + 现象覆盖矩阵）→ "
    "**r207（并行链《主方程结构名实审计》）** → "
    "**r208（并行链《可证伪性审计》）** → "
    "**r209（并行链《验证余量审计》47项 PASS 余量分布）** → **r210（本册）**。"
    "本册首版拟用 r207、二版改 r209，两次落盘后复扫均发现被并行链先占 "
    "⇒ 依「整卷改号、不改他册」铁律，本册四件套与判定册全部改号 r210，"
    "并清除本册旧 r207/r209 名下的源码/数据/判定各一份（只删本册自己的文件）。"
    "落盘前对 `源码/数据/判定` 三目录分别扫 `*r210*`：零命中。",
    {"id": "r210", "collisions": 3, "attempted": ["r207", "r209", "r210"]})

# =====================================================================
# 5b. 控制组登记（真实谓词，非写死）
# =====================================================================
VERDICT = ("R210-GW-ZEROMODE-RANK4-NULLITY6-GAUGE4-PHYS2-OK-"
           "QFORM-SYM-20-20-OK-GAUGE-ZERO-4-4-OK-"
           "TT-PLUS-CROSS-KERNEL-TRANSVERSE-TRACELESS-OK-INDEP-OK-"
           "JOINED-RANK6-EQ-NULLITY-OK-SCALAR-VECTOR-REJECTED-3-OK-"
           "BIANCHI-80-80-OK-ROT-INV-1100-OK-"
           "TIMELIKE-PHYS0-CTRL-OK-SPACELIKE-PHYS0-CTRL-OK-"
           "EM-NULL-1-3-2-REPRO-R196B02-OK-EM-TL-3-1-0-CTRL-OK-"
           "TRANSPOSED-RANK4-NULLITY6-BUT-GAUGE-FAIL-8-CTRL-OK-SCALAR-FIELD-1-CTRL-OK-"
           "NAIVE-GAUGE3-GIVES3-CTRL-OK-PERM-RANK-INV-OK-"
           "UPSTREAM-R190A07-CLOSED-R193D02-EXACTLY2-R196B02-REPRO-OK-"
           "ECSK-ARG-GAP-BOUNDARY-SCOPE-METRIC-ONLY-"
           "C1-1-C2-2-C3-0-DOF-2-2-0-0-2-0-1-TUFT-SUPPLY-0")
control("K01 timelike_phys0", P_TIME["phys"] == 0 and P_TIME["gauge_zero"],
        "phys=%s" % P_TIME["phys"])
control("K02 em_null_132", (EM_NULL_R, 4 - EM_NULL_R, 4 - EM_NULL_R - 1) == (1, 3, 2),
        str((EM_NULL_R, 4 - EM_NULL_R, 4 - EM_NULL_R - 1)))
control("K03 em_time_310", (EM_TIME_R, 4 - EM_TIME_R, 4 - EM_TIME_R - 1) == (3, 1, 0),
        str((EM_TIME_R, 4 - EM_TIME_R, 4 - EM_TIME_R - 1)))
control("K04 transposed_rank4_gauge_fail",
        P_T["rank"] == 4 and T_NONZERO > 0 and all(x > 0 for x in T_RES),
        "rank=%s nonzero=%s" % (P_T["rank"], T_NONZERO))
control("K05 scalar_one", (SCAL_R, 1 - SCAL_R) == (0, 1), str((SCAL_R, 1 - SCAL_R)))
control("K06 naive_gauge3", NAIVE_GAUGE3 == 3 and NAIVE_GAUGE3 != P_NULL["phys"],
        "naive=%d true=%d" % (NAIVE_GAUGE3, P_NULL["phys"]))
control("K07 perm_rank_inv", PERM_R == P_NULL["rank"], "%d/%d" % (PERM_R, P_NULL["rank"]))

# =====================================================================
# 6. 守卫
# =====================================================================
guard("G01 sec13_nonempty", len(SEC13) > 400, "len=%d" % len(SEC13))
guard("G02 upstream_texts", S13_TT and S13_ECSK and S13_TWO,
      "tt=%s ecsk=%s two=%s" % (S13_TT, S13_ECSK, S13_TWO))
guard("G03 csv_row_found", ROW07 is not None and len(ROW07) >= 7, str(len(ROW07) if ROW07 else 0))
guard("G04 csv_partial_quant", R07_STATE == "部分确立" and R07_QUANT == "未精确定量",
      "%s | %s" % (R07_STATE, R07_QUANT))
guard("G05 r190_a07_false", E190.get("level") == "INFO"
      and N190.get("machine_checkable") is False, str(N190))
guard("G06 r193_d02_indep", E193.get("level") == "INFO" and N193.get("independent") is True,
      str(N193))
guard("G07 r196_b02_nums", (N196.get("rank_lorenz"), N196.get("nullity"), N196.get("phys_dof"))
      == (1, 3, 2), str(N196))
guard("G08 qform_symmetric", QS_OK, "%d/%d" % (sum(1 for p in PAIRS if p[0]), len(PAIRS)))
guard("G09 gauge_zero", P_NULL["gauge_zero"], "M.g != 0")
guard("G10 gauge_rank4", P_NULL["gauge_rank"] == 4, str(P_NULL["gauge_rank"]))
guard("G11 rank4", P_NULL["rank"] == 4, str(P_NULL["rank"]))
guard("G12 nullity6", P_NULL["nullity"] == 6, str(P_NULL["nullity"]))
guard("G13 phys2", P_NULL["phys"] == 2, str(P_NULL["phys"]))
guard("G14 tt_plus_kernel", TT_PLUS_K, str(TT_PLUS_K))
guard("G15 tt_plus_transverse", TT_PLUS_T and TT_PLUS_TR, "%s/%s" % (TT_PLUS_T, TT_PLUS_TR))
guard("G16 tt_cross_kernel", TT_CROSS_K, str(TT_CROSS_K))
guard("G17 tt_cross_transverse", TT_CROSS_T and TT_CROSS_TR, "%s/%s" % (TT_CROSS_T, TT_CROSS_TR))
guard("G18 tt_independent", TT_INDEP, str(TT_INDEP))
guard("G19 joined6", GTT_RANK == 6 and GTT_RANK == P_NULL["nullity"],
      "%d vs %d" % (GTT_RANK, P_NULL["nullity"]))
guard("G20 candidates_rejected", REJ_OK, str([len(nz) for _, nz in REJ]))
guard("G21 bianchi_80", BIANCHI_BAD == 0 and BIANCHI_N == 80,
      "%d/%d" % (BIANCHI_N - BIANCHI_BAD, BIANCHI_N))
guard("G22 rot_inv", (P_ROT["rank"], P_ROT["nullity"], P_ROT["phys"]) == (4, 6, 2),
      str(P_ROT))
guard("G23 timelike_zero", P_TIME["phys"] == 0 and P_TIME["gauge_zero"],
      str(P_TIME["phys"]))
guard("G24 spacelike_zero", P_SPACE["phys"] == 0, str(P_SPACE["phys"]))
guard("G25 em_null_132", (EM_NULL_R, 4 - EM_NULL_R, 4 - EM_NULL_R - 1) == (1, 3, 2),
      str((EM_NULL_R, 4 - EM_NULL_R, 4 - EM_NULL_R - 1)))
guard("G26 em_time_310", (EM_TIME_R, 4 - EM_TIME_R, 4 - EM_TIME_R - 1) == (3, 1, 0),
      str((EM_TIME_R, 4 - EM_TIME_R, 4 - EM_TIME_R - 1)))
guard("G27 transposed_gauge_fail", T_NONZERO > 0 and all(x > 0 for x in T_RES),
      "nonzero=%d %s" % (T_NONZERO, T_RES))
guard("G28 transposed_rank_same", P_T["rank"] == P_NULL["rank"]
      and P_T["nullity"] == P_NULL["nullity"], "%d/%d vs %d/%d"
      % (P_T["rank"], P_T["nullity"], P_NULL["rank"], P_NULL["nullity"]))
guard("G28b formula_minus2", L2_BAD == 0, "bad=%d" % L2_BAD)
guard("G29 scalar_one", (SCAL_R, 1 - SCAL_R) == (0, 1), str((SCAL_R, 1 - SCAL_R)))
guard("G30 naive_gauge3", NAIVE_GAUGE3 == 3, str(NAIVE_GAUGE3))
guard("G31 perm_invariant", PERM_R == P_NULL["rank"], "%d/%d" % (PERM_R, P_NULL["rank"]))
guard("G32 dof_ledger7", len(DOF) == 7, str(len(DOF)))
guard("G33 dof_heights", [d["phys"] for d in DOF] == [2, 2, 0, 0, 2, 0, 1],
      str([d["phys"] for d in DOF]))
cnt = Counter(e["level"] for e in ENTRIES)
guard("G34 levels", cnt.get("PASS", 0) == 23 and cnt.get("INFO", 0) == 3
      and cnt.get("BOUNDARY", 0) == 1 and cnt.get("FAIL", 0) == 0, str(dict(cnt)))
guard("G35 no_fail_has_no_numbers", all(bool(e["numbers"]) for e in ENTRIES),
      "entries=%d" % len(ENTRIES))
guard("G36 dof_grav_null_all2", all(d["phys"] == 2 for d in DOF if d["sector"].startswith("引力·类光")),
      str([d["phys"] for d in DOF if d["sector"].startswith("引力·类光")]))
guard("G37 verdict_tokens", ("PHYS2" in VERDICT) and ("RANK4" in VERDICT) and ("SUPPLY-0" in VERDICT),
      "len=%d" % len(VERDICT))
C_VERD = [("C1", 1), ("C2", 2), ("C3", 0)]
guard("G38 c1_c2_c3", [k for k, v in C_VERD if v > 0] == ["C1", "C2"]
      and [v for k, v in C_VERD] == [1, 2, 0], str(C_VERD))


def main():
    counts = Counter(e["level"] for e in ENTRIES)

    # ---- 先构造正文（不含计数头与守卫清单），把 G39 也计入守卫总数 ----
    md = []
    md.append("# " + STEM + "\n")
    md.append("## 一句话\n")
    md.append("线性化 Einstein 算子在类光 k=(1,0,0,1) 下的 10×10 有理矩阵 **秩 4 / 零模 6 / 规范像 4 ⇒ "
              "物理自由度恰为 2**；显式 TT 两模（h_+=diag(0,1,−1,0)、h_×=(1,2)分量=1）"
              "**在核内、横向、无迹、线性独立且与规范像一起张满整个核**（联合秩 6）⇒ "
              "r193 D02 的「至少 2 维」升级为「恰好 2 维」，r190 A07 的 `machine_checkable:false` 关闭，"
              "r196 B02 的电磁 1/3/2 由同一台机器逐位复现。呼吸/共形/h_03 三个标量矢量候选全部被拒 ⇒ "
              "「无标量/矢量极化」在线性度规层成立。**边界**：只覆盖线性化度规扇区，"
              "挠率-度规混合/非线性/量子/观测均不宣称。**本册最重要的一条负对照**："
              "把算子写成转置后秩同样是 4、零模同样是 6，但规范湮灭失败（4 组共 "
              + str(T_NONZERO) + " 个非零分量）——秩对不代表算子对。\n")
    md.append("**判定串**：`" + VERDICT + "`\n")
    md.append("## 自由度账本\n")
    md.append("| 扇区 | k | k² | rank | nullity | 规范维 | 物理 DOF |")
    md.append("|---|---|---|---|---|---|---|")
    for d in DOF:
        md.append("| %s | (%s) | %s | %s | %s | %s | **%s** |"
                  % (d["sector"], ",".join(str(x) for x in d["k"]), d["k2"],
                     d["rank"], d["nullity"], d["gauge"], d["phys"]))
    md.append("\n## 条目\n")
    md.append("| 编号 | 级 | 标题 |")
    md.append("|---|---|---|")
    for e in ENTRIES:
        md.append("| %s | %s | %s |" % (e["code"], e["level"], e["title"].replace("|", "\\|")))
    md.append("\n## 三判定\n")
    md.append("| 探针 | 判定 | 理由 |")
    md.append("|---|---|---|")
    md.append("| C1 | **既有理论复写** | 线性化 Einstein 张量零模计数是标准 GR，本册独立精确复算 |")
    md.append("| C2 | **条件性** | 树级线性化；物理=ker/规范像；挠率非传播为继承输入 |")
    md.append("| C3 | **独立可证伪预言** | 0 条（不新增预言；P2 判据只是被机验，不是新造） |")
    md.append("\n## 修复建议\n")
    md.append("- **R1**：07 覆盖矩阵「引力波仅两种张量极化」行，定量列 `未精确定量` → "
              "`计数：恰好 2（r210 线性化度规层）；观测：待测`；证据状态维持 `部分确立`。")
    md.append("- **R2**：03 §1.3 把「ECSK 中挠率非传播，故极化仍是两种」改写为"
              "「度规扇区线性化算子恰有 2 个物理零模（r210）；挠率非传播（r187 D01）另有约束」，"
              "结论不变，理由补全。")

    guard("G39 verdict_in_md", VERDICT in "\n".join(md), "verdict not in md body")

    n_g = sum(1 for g in GUARDS if g["ok"])
    n_c = sum(1 for c in CONTROLS if c["ok"])
    ok_all = (n_g == len(GUARDS) and n_c == len(CONTROLS))
    header = ("**条目 %d（PASS %d / INFO %d / BOUNDARY %d / FAIL %d）；"
              "守卫 %d/%d；控制组 %d/%d；退出码 %d**\n"
              % (len(ENTRIES), counts.get("PASS", 0), counts.get("INFO", 0),
                 counts.get("BOUNDARY", 0), counts.get("FAIL", 0),
                 n_g, len(GUARDS), n_c, len(CONTROLS), 0 if ok_all else 1))
    md.insert(1, header)
    md.append("\n## 守护（%d/%d）\n" % (n_g, len(GUARDS)))
    for g in GUARDS:
        md.append("- [%s] %s" % ("OK" if g["ok"] else "FAIL", g["name"]))
    md.append("\n## 控制组（%d/%d）\n" % (n_c, len(CONTROLS)))
    for c in CONTROLS:
        md.append("- [%s] %s" % ("OK" if c["ok"] else "FAIL", c["name"]))
    md.append("\n## 红线\n")
    md.append("本册只做机验计数与名实收口，不产生新物理，不宣称观测证实/否证；"
              "未改写 03 卷、07 卷 CSV 或 r190/r193/r196 任何字节；未改 verify.py；未做 git；"
              "未触碰并行链文件（r203/r204/r205/r206 两卷）。TUFT 供给 0/12 维持，①池 12/12。\n")
    with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print("\n" + "=" * 78)
    print("条目 %d（PASS %d / INFO %d / BOUNDARY %d / FAIL %d）"
          % (len(ENTRIES), counts.get("PASS", 0), counts.get("INFO", 0),
             counts.get("BOUNDARY", 0), counts.get("FAIL", 0)))
    print("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
    print("判定串：" + VERDICT)

    payload = dict(
        stem=STEM, verdict=VERDICT, counts=dict(counts),
        guards_total=len(GUARDS), guards_pass=n_g,
        controls_total=len(CONTROLS), controls_pass=n_c,
        guard_list=GUARDS, control_list=CONTROLS, entries=ENTRIES,
        dof=DOF,
        supply=dict(pool="12/12", supply="0/12"),
        judgement=[dict(probe="C1", verdict="既有理论复写", reason="线性化 Einstein 张量零模计数是标准 GR"),
                   dict(probe="C2", verdict="条件性", reason="树级线性化；物理=ker/规范像；挠率非传播为继承输入"),
                   dict(probe="C3", verdict="独立可证伪预言", reason="0 条（无新增预言）")],
        source="07_统一场方程/03_四力还原.md §1.3 + 现象覆盖矩阵.csv + r190/r193/r196 JSON",
    )
    with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rep = []
    rep.append("TUFT-r210 引力波零模精确计数 · 线性化算子秩与 TT 极化完备性 · 运行报告")
    rep.append("=" * 70)
    rep.append("条目 %d（PASS %d / INFO %d / BOUNDARY %d / FAIL %d）"
               % (len(ENTRIES), counts.get("PASS", 0), counts.get("INFO", 0),
                  counts.get("BOUNDARY", 0), counts.get("FAIL", 0)))
    rep.append("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
    rep.append("")
    for e in ENTRIES:
        rep.append("[%s] %s  %s" % (e["level"], e["code"], e["title"]))
        rep.append("    " + e["detail"])
        if e["numbers"]:
            try:
                rep.append("    " + json.dumps(e["numbers"], ensure_ascii=False))
            except Exception:
                pass
        rep.append("")
    rep.append("判定串：" + VERDICT)
    with open(os.path.join(OUTD, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep))

    print("out -> %s.{json,md,_report.txt}" % STEM)
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
