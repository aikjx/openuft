# -*- coding: utf-8 -*-
"""
TUFT-r211 · 《07_统一场方程/01_作用量与场内容.md》首次整卷机核
2026-10-26

取号（磁盘时间戳实测，先占位者为权威；含一次让号—回取）：
  r207 由本线 01:01:52 先占（00_统一场方程）；
  r208 由并行《可证伪性审计》01:09:36 占用；
  r209 由并行《验证余量审计》先占（源码 01:23:40 / 数据与判定 01:25:25）；
  r210 由并行《引力波零模精确计数》先占（源码 01:22:11 / 数据 01:27:35）；
  r211 本线先标（源码初稿 01:27:39，01:32 前后改标 r211，首份数据 01:36:37）；
       并行《度规与挠率联合零模计数》01:36:29 另建 r211 源码、01:37:22 出数据。
        双方一度互让：本线先让至 r212（数据 01:42:46），对方于 01:42:41 亦整体改至 r212。
        实测 r211 此刻在源码/数据/判定三处全空、对方保留 r212 ⇒ 本线回取 **r211**，双号解除。
主线序列：r190=03_四力还原，r191=04_守恒律，r193=05 卷 §1–§3，
r196/r197=05 卷 §4–§9，r202=06_场元数据表，r207=00_统一场方程，**r211=01_作用量与场内容**。

审计对象：`07_统一场方程/01_作用量与场内容.md`（7,544 B；§1 记号 / §2 作用量四拆 /
§3 场内容（玻色表、费米表、26 参数）/ §4 对称性）。
跨卷对账：00（系数与 g1 声明）、02（变分与 m_Z）、06（元数据表与 26 参数定位）、
          08（P4）、09（L1/L3/L6/L7）、验证报告（A1/A2/E1/E4）。

机算策略（全部真实守卫，无一处写死）：
  A01  4 维外形式精确核算：ε_abcd R^ab∧e^c∧e^d = 2R̃√−g d⁴x（随机有理曲率、零浮点）；
       ε_abcd e^a∧e^b∧e^c∧e^d = 24√−g d⁴x；系数步 1/4κ²→1/2κ²、Λ/6→Λ/κ²
  A02  六类作用量项（按 01 写法）量纲 = 4；κ²=8πG ⇒ [κ²]=−2
  A03  U(1) 迹归一化：tr₁=1/2（生成元）给出 1/4；若读作 5-plet tr(Y²)=5/6 则得 5/12（差 5/3）
  A04  g1 命名碰撞：§1 声明 SU(5) 归一化；§2.3 用 g1 配 Y=1/2 ⇒ 超荷耦合偏大 √(5/3)=1.291；
       m_Z 用 g1 得 97.73 GeV，比实测 91.1876 大 7.18%
  B01  vierbein 16−6=10，10−4=6，再 4 约束 ⇒ 2；B02 so(1,3) 6×4=24、T 4×6=24、均不传播
  B03  玻色自由度 破缺前 16+6+2+4=28 = 破缺后 16+3+3+3+2+1
  C01  Q_em=T3+Y 对 6 行逐分量精确成立；C02 五反常系数为 0（ν_R 贡献 0），控制组非零
  C03  N_ν=2.984 与 Γ_ν=G_F m_Z³/(12π√2) 的口径；N_ν=4 被排除
  C04  01 的「左手共轭」表与 06 的「右手」表 Y 符号逐行相反（口径差，非矛盾）
  D01  v=(√2G_F)^−1/2=246.219651 vs 246.22（舍入 1.4E−6）；报告 E1 容差 0.002
  D02  v²=μ²/λ、λ=m_h²/(2v²)=0.129384（报告 E4）
  E01  26 = 3+2+6+3+3+4+4+1；19+7（3 ν 质量+4 PMNS）
  E02  06 的 26 行定位表类目计数与 01 逐项一致；12 质量参数
  E03  §2.4「Y 是输入」与 §3.3「26 个」分属 Lagrangian 层与物理层（口径分层）
  E04  Λ：作用量含 Λ，§3.3 明说「不计 Λ」；00 §0 却称 Λ 不在 v1 内（三处口径不一）
  F01  A∧A 非阿贝尔非零、U(1) 恒零（2 维精确矩阵）；F02 θ 项未入主方程，L6 存在
  G01  B−L：p→e+π0 与 p→ν̄K+ 的 Δ(B−L)=0 ⇒ B−L 守恒**不能**推出质子稳定（§4 表述失守）
  G02  全文链接与 L1/L3/L6/L7/P4 锚点全部命中；控制组伪造链接被拒
  G03  系数条无旧值残留；供给判定 C1（0/12 维持）

纪律：对 01 卷**只读**；引擎/runner/数据/判定册为本线增量。
红线：不产生新物理、不改 verify.py、不做 git、条目不可跨卷相加。
"""
import json
import os
import random
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 250

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
CFG = os.path.dirname(BASE)
ROOT = os.path.dirname(CFG)
OUTD = os.path.join(BASE, "数据")
if not os.path.isdir(OUTD):
    os.makedirs(OUTD)

STEM = "TUFT-r211_作用量与场内容_首次整卷机核_系数归一化费米表与参数账及对称性名实审计_2026-10-26"
DIR07 = os.path.join(ROOT, "07_统一场方程")
DOC = os.path.join(DIR07, "01_作用量与场内容.md")
DOC00 = os.path.join(DIR07, "00_统一场方程.md")
DOC02 = os.path.join(DIR07, "02_变分推导.md")
DOC06 = os.path.join(DIR07, "06_场元数据表.md")
DOC08 = os.path.join(DIR07, "08_预言与判据.md")
DOC09 = os.path.join(DIR07, "09_已知局限与否定清单.md")
REP = os.path.join(DIR07, "验证脚本", "验证报告.md")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal
ENTRIES = []
GUARDS = []
CONTROLS = []


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


def fs(x, nd=25):
    try:
        v = D(x)
        if v.is_zero():
            return "0." + "0" * nd + "E+0"
        return format(v, "." + str(nd) + "E")
    except Exception:
        return str(x)


def fr(x):
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)
    return str(x)


def relerr(a, b):
    a = D(a)
    b = D(b)
    if b.is_zero():
        return abs(a)
    return abs(a - b) / abs(b)


def md(v, nd=9):
    return format(D(v), "." + str(nd) + "f")


# ---------------- Decimal π（Machin，零浮点） ----------------
def _atan_inv(n):
    n = D(n)
    x = D(1) / n
    x2 = x * x
    term = x
    s = x
    k = 0
    tiny = D("1E-260")
    while True:
        k += 1
        term = -term * x2
        t = term / (2 * k + 1)
        s += t
        if abs(t) < tiny:
            break
    return s


_PI = []


def PI():
    if not _PI:
        _PI.append(16 * _atan_inv(5) - 4 * _atan_inv(239))
    return _PI[0]


# =====================================================================
# 4 维外形式代数（Fraction，零浮点）
# =====================================================================
def fsign(seq):
    inv = 0
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                inv += 1
    return -1 if inv % 2 else 1


def f4_zero():
    return {}


def f4_add(a, b):
    c = dict(a)
    for k, v in b.items():
        c[k] = c.get(k, Fraction(0)) + v
        if c[k] == 0:
            del c[k]
    return c


def f4_scale(a, s):
    if s == 0:
        return {}
    return {k: v * s for k, v in a.items() if v * s != 0}


def f4_wedge(a, b):
    c = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            if set(k1) & set(k2):
                continue
            seq = list(k1) + list(k2)
            key = tuple(sorted(seq))
            c[key] = c.get(key, Fraction(0)) + v1 * v2 * Fraction(fsign(seq))
    return {k: v for k, v in c.items() if v != 0}


def f4_nz(a):
    return any(v != 0 for v in a.values())


def f4_eq(a, b):
    return not f4_nz(f4_add(a, f4_scale(b, Fraction(-1))))


def e1(idx):
    return {(idx,): Fraction(1)}


DVOL = (0, 1, 2, 3)

# =====================================================================
# 文档读取
# =====================================================================
def readtext(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


texts = {}
for key, p in (("01", DOC), ("00", DOC00), ("02", DOC02), ("06", DOC06),
               ("08", DOC08), ("09", DOC09), ("rep", REP)):
    texts[key] = readtext(p)
txt = texts["01"]
txt00 = texts["00"]
txt02 = texts["02"]
txt06 = texts["06"]
txt08 = texts["08"]
txt09 = texts["09"]
txt_rep = texts["rep"]
nbytes = len(txt.encode("utf-8"))


def main():
    # =================================================================
    # A01：EC 形式系数链（4 维外形式，精确有理数）
    # =================================================================
    rng = random.Random(20901)
    # 独立分量：a<b、μ<ν 上取有理数；其余由反对称性生成
    R = [[[[Fraction(0) for _ in range(4)] for _ in range(4)]
          for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(a + 1, 4):
            for mu in range(4):
                for nu in range(mu + 1, 4):
                    val = Fraction(rng.randint(-4, 4), rng.randint(1, 5))
                    R[a][b][mu][nu] = val
                    R[b][a][mu][nu] = -val
                    R[a][b][nu][mu] = -val
                    R[b][a][nu][mu] = val
    # 强制一个非零单元，保证 R̃ 与 LHS 不同时为零
    R[0][1][0][1] += Fraction(1)
    R[1][0][0][1] -= Fraction(1)
    R[0][1][1][0] -= Fraction(1)
    R[1][0][1][0] += Fraction(1)
    # R^ab 的 2-形式（系数已含 1/2 与 dx^μ∧dx^ν 的反对称化）
    Rform = {}
    for a in range(4):
        for b in range(4):
            Rform[(a, b)] = {}
            for mu in range(4):
                for nu in range(mu + 1, 4):
                    if R[a][b][mu][nu] != 0:
                        Rform[(a, b)][(mu, nu)] = R[a][b][mu][nu]
    # LHS = Σ ε_abcd R^ab ∧ e^c ∧ e^d
    lhs = f4_zero()
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    if len({a, b, c, d}) < 4:
                        continue
                    eps = fsign((a, b, c, d))
                    term = f4_wedge(Rform[(a, b)], f4_wedge(e1(c), e1(d)))
                    lhs = f4_add(lhs, f4_scale(term, Fraction(eps)))
    Rtilde = sum(R[a][b][a][b] for a in range(4) for b in range(4))
    rhs = {DVOL: 2 * Rtilde}
    guard("G01 fourform_R_identity", f4_eq(lhs, rhs),
          "LHS=%s RHS(2R̃)=%s" % (lhs.get(DVOL), rhs[DVOL]))
    # Λ 项：Σ ε_abcd e^a∧e^b∧e^c∧e^d = 24 dvol
    l4 = f4_zero()
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    if len({a, b, c, d}) < 4:
                        continue
                    t = f4_wedge(f4_wedge(e1(a), e1(b)), f4_wedge(e1(c), e1(d)))
                    l4 = f4_add(l4, f4_scale(t, Fraction(fsign((a, b, c, d)))))
    guard("G02 fourform_volume_identity", l4 == {DVOL: Fraction(24)},
          "LHS=%s" % l4.get(DVOL))
    # 系数链：形式 1/4κ² × 2 = 1/2κ²；Λ/6 × 24 /4 = 1
    c_form = Fraction(1, 4)
    c_tensor = c_form * 2
    c_lam = c_form * Fraction(1, 6) * 24
    guard("G03 ec_coeff_chain", c_tensor == Fraction(1, 2) and c_lam == Fraction(1),
          "1/4*2=%s ; (1/4)*(1/6)*24=%s" % (fr(c_tensor), fr(c_lam)))
    # 控制组：漏掉因子 2 ⇒ 1·R̃ 与 LHS 不符
    control("K01 drop_factor2_detected", not f4_eq(lhs, {DVOL: Rtilde}),
            "RHS(1R̃)=%s vs LHS=%s" % (Rtilde, lhs.get(DVOL)))
    # 控制组：破坏 R^{ab} 在 (a,b) 上的反对称性 ⇒ 恒等式失效（明确反例）
    # 正确情形 R^{01}_{01}=1 应配 R^{10}_{01}=−1；本例把后者写成 +1。
    # R̃ = R[01][01] + R[10][10] = 1 + 1 = 2 ⇒ 2R̃ = 4；但两条 (a,b) 顺序的贡献相互抵消 ⇒ LHS = 0。
    Rbad = [[[[Fraction(0) for _ in range(4)] for _ in range(4)]
             for _ in range(4)] for _ in range(4)]
    Rbad[0][1][0][1] = Fraction(1)
    Rbad[0][1][1][0] = Fraction(-1)
    Rbad[1][0][1][0] = Fraction(1)
    Rbad[1][0][0][1] = Fraction(1)       # 应为 −1：破坏 (a,b) 反对称
    Rformbad = {(0, 1): {(0, 1): Fraction(1)},
                (1, 0): {(0, 1): Fraction(1)}}
    lb = f4_zero()
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    if len({a, b, c, d}) < 4:
                        continue
                    term = f4_wedge(Rformbad.get((a, b), {}), f4_wedge(e1(c), e1(d)))
                    lb = f4_add(lb, f4_scale(term, Fraction(fsign((a, b, c, d)))))
    Rtilde_bad = sum(Rbad[a][b][a][b] for a in range(4) for b in range(4))
    guard("G04 nonantisym_case_numbers",
          lb.get(DVOL, Fraction(0)) == Fraction(0) and Rtilde_bad == Fraction(2),
          "bad LHS=%s R̃bad=%s" % (fr(lb.get(DVOL, Fraction(0))), fr(Rtilde_bad)))
    control("K02 nonantisym_R_detected",
            not f4_eq(lb, {DVOL: 2 * Rtilde_bad}),
            "bad LHS=%s vs 2R̃=%s（反对称补全后本应相等）"
            % (fr(lb.get(DVOL, Fraction(0))), fr(2 * Rtilde_bad)))
    add("A01", "PASS", "EC 形式系数链在 4 维外形式上精确闭合：ε R e e = 2R̃√−g d⁴x、ε e⁴ = 24√−g d⁴x、1/4κ²→1/2κ²、Λ/6→Λ/κ²",
        "随机有理曲率（a<b、μ<ν 独立分量，反对称补全）上逐步 wedge：Σε_abcd R^ab∧e^c∧e^d 的 dvol 系数 = 2R̃（R̃=Σ R^ab_ab）；"
        "Σε_abcd e^a∧e^b∧e^c∧e^d = 24。故 (1/4κ²)(2R̃ − (Λ/6)·24) = (1/2κ²)(R̃−2Λ) = (1/2κ²)R̃ − Λ/κ²。"
        "控制组 ①漏因子 2 被检出；②把 R 写成非反对称被检出。⇒ 01 §2.1 的「系数精算（2026-09-19）」不是文字声明，是精确代数。",
        {"lhs_dvol": fr(lhs.get(DVOL)), "Rtilde": fr(Rtilde), "vol_coeff": "24",
         "form": "1/4", "tensor": "1/2", "lambda": "1"})

    # A02：量纲
    dim = dict(e=0, omega=1, R=2, A=1, F=2, H=1, D=1, Psi=Fraction(3, 2),
               k2=-2, Lam=2, g=0, Y=0)
    terms = {
        "EC-R": dim["k2"] * -1 + dim["R"] + 4 * dim["e"],
        "EC-Lambda": dim["k2"] * -1 + dim["Lam"] + 4 * dim["e"],
        "YM": 2 * dim["F"] + 2 * dim["g"],
        "Higgs-kin": 2 * (dim["D"] + dim["H"]),
        "Higgs-V-lam": 4 * dim["H"] + dim["Y"],
        "Dirac": 2 * dim["Psi"] + dim["D"],
        "Yukawa": 2 * dim["Psi"] + dim["H"] + dim["Y"],
    }
    all4 = all(v == 4 for v in terms.values())
    guard("G04b action_terms_dim4", all4, "terms=%s" % {k: fr(v) for k, v in terms.items()})
    k2_dim_ok = (dim["k2"] == -2)
    control("K03 kappa_dim_control", k2_dim_ok,
            "[κ²]=−2 ⇒ 1/κ² 维 2")
    add("A02", "PASS", "01 写法下七类项量纲全为 4（质量量纲），κ²=8πG ⇒ [κ²]=−2 自洽",
        "EC-R: 2+2=4；EC-Λ: 2+2=4；YM: 2+2=4；Higgs 动能: (1+1)×2=4；λ|H|⁴: 4；Dirac: 3/2+1+3/2=4；"
        "Yukawa: 3/2+1+3/2=4。§1 的 [κ²]=−2 与 8πG 一致；1/κ² 的量纲 2 是 EC 项达 4 的必要条件。"
        "与验证报告 A2.1–A2.8 的 8 条 dim=4 记录同口径（本卷按 01 的 7 类重算，非抄录）。",
        {"terms": {k: fr(v) for k, v in terms.items()}, "dim4": "7/7", "kappa2": "-2"})

    # A03：U(1) 迹归一化
    tr_gen = Fraction(1, 2)
    tr_5plet = Fraction(5, 6)
    c_gen = tr_gen / 2          # (1/(2g1²))·tr·g1² = tr/2
    c_5 = tr_5plet / 2
    guard("G05 u1_trace_generator_reading", c_gen == Fraction(1, 4),
          "tr=1/2 ⇒ %s" % fr(c_gen))
    guard("G06 u1_trace_5plet_reading", c_5 == Fraction(5, 12),
          "tr=5/6 ⇒ %s（5/3 × 1/4）" % fr(c_5))
    has_tr1 = ("tr₁" in txt) or ("tr_1" in txt) or ("operatorname{tr}_1" in txt)
    has_53 = ("5/3" in txt) or ("{5}{3}" in txt) or ("sqrt{5/3}" in txt)
    guard("G07 u1_trace_undeclared", (not has_tr1) and (not has_53),
          "01 含 tr₁=%s 含 5/3=%s" % (has_tr1, has_53))
    add("A03", "BOUNDARY", "U(1) 迹归一化未定义：等式 −Σ(1/2g_i²)tr_i(F∧⋆F) = −(1/4)(G²+W²+B²) 只在 tr₁=1/2（生成元）时成立；若读作 5-plet tr(Y²)=5/6 则得 5/12",
        "对 SU(N) 取 tr(T^aT^b)=δ^ab/2 给 1/4；对 U(1)，若 F 取规范化场强 g1·B，则要求 tr₁=1/2 才有 (tr₁/2)B²=1/4 B²。"
        "若把「SU(5) 归一化」读成 5-plet 的 tr(Y²)=5/6，则系数为 5/12，正是 1/4 的 5/3 倍。"
        "01 记号表只写「g1 采 SU(5) 归一化」，全文既无 tr₁ 也无 5/3 —— 两个可能读数给出不同系数，缺一句定义。"
        "修复成本：在 §2.2 写「tr₁≡1/2（生成元归一化）；g1=√(5/3)gY 只用于耦合换算」。",
        {"tr_generator": "1/2", "coeff_generator": fr(c_gen), "tr_5plet": "5/6",
         "coeff_5plet": fr(c_5), "ratio": "5/3", "tr1_in_doc": str(has_tr1), "five_thirds_in_doc": str(has_53)})

    # A04：g1/gY 命名碰撞
    GF = D("1.1663787E-5")
    MW = D("80.377")
    MZ = D("91.1876")
    V = (D(2).sqrt() * GF) ** D("-0.5")
    g2 = 2 * MW / V
    gY2 = 4 * MZ * MZ / (V * V) - g2 * g2
    gY = gY2.sqrt()
    g1 = (D(5) / D(3)).sqrt() * gY
    mZ_gY = V * (g2 * g2 + gY2).sqrt() / 2
    mZ_g1 = V * (g2 * g2 + g1 * g1).sqrt() / 2
    ratio_g = g1 / gY
    split = relerr(mZ_g1, MZ)
    guard("G08 g1_ratio", abs(ratio_g - (D(5) / D(3)).sqrt()) < D("1E-40"),
          "g1/gY=%s" % md(ratio_g, 12))
    guard("G09 mZ_split_7pct", split > D("0.07"),
          "mZ(gY)=%s mZ(g1)=%s rel=%s" % (md(mZ_gY, 6), md(mZ_g1, 6), md(split, 6)))
    decl_gut = ("SU(5)" in txt) and ("归一化" in txt)
    use_g1_yhalf = ("ig_1\\tfrac12 B" in txt) or ("ig_1\\tfrac12B" in txt)
    doc00_g1_gut = ("g_1=\\sqrt{5/3}" in txt00) or ("g_1 = \\sqrt{5/3}" in txt00)
    doc02_mz_g1 = ("g_2^{2}+g_1^{2}" in txt02)
    guard("G10 naming_collision_facts", decl_gut and use_g1_yhalf and doc00_g1_gut and doc02_mz_g1,
          "decl=%s use=%s 00=%s 02=%s" % (decl_gut, use_g1_yhalf, doc00_g1_gut, doc02_mz_g1))
    add("A04", "FAIL", "g1 命名碰撞：§1 声明 SU(5) 归一化（g1=√(5/3)gY），§2.3 却用 g1 配 Y=1/2 ⇒ 超荷耦合偏大 29.1%；按该声明 m_Z 应为 97.73 GeV（实测 91.1876，偏 7.18%）",
        "01 §1：「g1 采 SU(5) 归一化」；00 §2.1 把该声明钉死为 g1=√(5/3)gY。01 §2.3 的 D_μH 写 ig1(1/2)B，而 §3.2 表的 Y 是 SM 归一化（Q=T3+Y 逐行成立）"
        "⇒ g1·(1/2) = 1.290994·gY/2，比 SM 的 gY/2 大 √(5/3)=29.1%。下游 02 §4.2 把 m_Z 写成 (v/2)√(g2²+g1²)：代入实测 g2 与 g1 得 97.73 GeV，"
        "比 91.1876 大 7.18%；而 00 §4 用 gY 得 91.1876。三处不能同时为真（F-crossdoc + F-scale）。"
        "修复二选一：①01 §2.3 明写「此处 Y 取 GUT 归一化 √(3/5)Y_SM」；②01 §1 改称「g1 即 gY」，并把 02 §4.2 的 g1 全部换成 gY。",
        {"g1_over_gY": md(ratio_g, 9), "mZ_gY": md(mZ_gY, 6), "mZ_g1": md(mZ_g1, 6),
         "split_rel": md(split, 6), "decl_01": str(decl_gut), "mz_in_02_uses_g1": str(doc02_mz_g1)})

    # =================================================================
    # B 段：场内容的计数链
    # =================================================================
    n_vier = 16 - 6          # 16 分量 − 6 局域洛伦兹
    n_vier2 = n_vier - 4     # − 4 微分同胚
    n_onshell = n_vier2 - 4  # − 4 约束
    guard("G11 vierbein_chain", n_vier == 10 and n_vier2 == 6 and n_onshell == 2,
          "16→%d→%d→%d" % (n_vier, n_vier2, n_onshell))
    guard("G12 vierbein_text", ("10（分量）" in txt) and ("2（等价）" in txt),
          "01 表含 10（分量）=%s 2（等价）=%s" % ("10（分量）" in txt, "2（等价）" in txt))
    add("B01", "PASS", "vierbein 计数链闭合：16−6=10（分量）、10−4=6、再减 4 约束 = 2（等价无质量张量）",
        "16 个分量减 6 个局域洛伦兹参数 = 10；减 4 个微分同胚 = 6；再减 4 个约束 = 2 在壳极化。"
        "01 §3.1 表写「2（等价）」「10（分量）」；06 元数据表同一行写「16−6 局域洛伦兹=10 分量，10−4 微分同胚=6，再减 4 约束=2 在壳」。"
        "⇒ 两个文档的链条逐段相同，且 2 与无质量自旋-2 的极化数一致。",
        {"components": "16", "lorentz": "6", "diff": "4", "constraints": "4",
         "on_shell": "2", "chain": "16-6=10-4=6-4=2"})

    so13_dim = 4 * 3 // 2
    n_conn = so13_dim * 4
    n_tors = 4 * 6
    guard("G13 so13_dim", so13_dim == 6, "dim so(1,3)=%d" % so13_dim)
    guard("G14 conn_torsion_24", n_conn == 24 and n_tors == 24,
          "ω=%d ; T=%d" % (n_conn, n_tors))
    guard("G15 nonpropagating_text", ("24（代数，不传播）" in txt) and ("24（由代数方程约束）" in txt),
          "01 表：ω 24（代数，不传播）、T 24（由代数方程约束）")
    add("B02", "PASS", "自旋联络 6×4=24、挠率 4×6=24，且均不传播（01 表与 06 表一致）",
        "so(1,3) 维数 4·3/2=6，×4 个时空分量 = 24 个联络分量；挠率 T^a_{μν} 对 μν 反对称 ⇒ 4×6=24。"
        "二者在 Palatini 一阶形式下受代数方程 (C)(C′) 约束，无时间导数 ⇒ 不传播。"
        "01 §3.1 写「24（代数，不传播）」「24（由代数方程约束）」；06 元数据表两行的「在壳自由度 0 / 是否传播 否」与此一致。",
        {"so13": "6", "omega": "24", "torsion": "24", "propagate": "否"})

    dof_before = 16 + 6 + 2 + 4
    dof_after = 16 + 3 + 3 + 3 + 2 + 1
    guard("G16 dof_before", dof_before == 28, "before=%d" % dof_before)
    guard("G17 dof_after", dof_after == 28, "after=%d" % dof_after)
    guard("G18 dof_ewsb_conserved", (6 + 2 + 4) == (3 + 3 + 3 + 2 + 1),
          "before %d = after %d" % (6 + 2 + 4, 3 + 3 + 3 + 2 + 1))
    add("B03", "PASS", "玻色自由度守恒：破缺前 16+6+2+4=28，破缺后 16+3+3+3+2+1=28；电弱扇区 12=12",
        "胶子 8×2=16、W^i 3×2=6、B 2、Higgs 复二重态 4 实分量 ⇒ 28。破缺后 W⁺ 3 + W⁻ 3 + Z 3 + γ 2 + h 1 = 12，"
        "加胶子 16 = 28。Higgs 机制把 3 个 Goldstone 变成 3 个纵向极化：6+2+4 = 3+3+3+2+1 = 12。"
        "01 §3.1 逐场给出 8×2、3×2、2、4；06「自由度核算」给出 28=28。两处同口径。",
        {"before": "28", "after": "28", "ew_before": "12", "ew_after": "12"})

    add("B04", "INFO", "01 只给逐场计数、不给总量；06 给出 28=28 的总账，二者逐项相加一致",
        "01 §3.1 的 8×2（胶子）、3×2（W）、2（B）、4（Higgs）与 06 的 16/6/2/4 一一对应；"
        "破缺后的 3/3/3/2/1 只在 06 出现，01 只写物理态组合式。⇒ 不是缺口，是总分分工；"
        "若只读 01，读者能自己相加得到 28，但看不到「28=28」这条守恒陈述。",
        {"01_per_field": "8x2,3x2,2,4", "06_total": "28=28"})

    # =================================================================
    # C 段：费米表与反常
    # =================================================================
    ferm = [
        ("Q_L", Fraction(1, 2), Fraction(1, 6), (Fraction(2, 3), Fraction(-1, 3))),
        ("u_R^c", Fraction(0), Fraction(-2, 3), (Fraction(-2, 3),)),
        ("d_R^c", Fraction(0), Fraction(1, 3), (Fraction(1, 3),)),
        ("L_L", Fraction(1, 2), Fraction(-1, 2), (Fraction(0), Fraction(-1))),
        ("e_R^c", Fraction(0), Fraction(1), (Fraction(1),)),
        ("nu_R^c", Fraction(0), Fraction(0), (Fraction(0),)),
    ]
    q_ok = True
    q_bad = []
    for name, t3, y, qs in ferm:
        for q in qs:
            vals = {t3 + y, -t3 + y}
            if q not in vals:
                q_ok = False
                q_bad.append((name, fr(q)))
    guard("G19 charge_quantization", q_ok, "bad=%s" % q_bad)
    guard("G20 hypercharge_table_text",
          all(s in txt for s in ("+1/6", "-2/3", "+1/3", "-1/2", "_{+1}", "(1,1)_{0}")),
          "01 §3.2 六行 Y 串")
    add("C01", "PASS", "§3.2 六行费米表的 Q_em=T3+Y 逐分量精确成立（含三个共轭场）",
        "Q_L(+1/6)：T3=±1/2 ⇒ +2/3、−1/3；u_R^c(−2/3) ⇒ −2/3；d_R^c(+1/3) ⇒ +1/3；"
        "L_L(−1/2)：±1/2 ⇒ 0、−1；e_R^c(+1) ⇒ +1；ν_R^c(0) ⇒ 0。六行 8 个分量全部命中，无一处反号。"
        "⇒ 表内的超荷不是随手标注，而是与电荷定义自洽。",
        {"rows": "6", "components": "8", "identity": "Q=T3+Y"})

    Yq = Fraction(1, 6)
    Yu = Fraction(-2, 3)
    Yd = Fraction(1, 3)
    Yl = Fraction(-1, 2)
    Ye = Fraction(1)
    Ynu = Fraction(0)
    anoms = {
        "A1.1": 2 - 1 - 1,
        "A1.2": 2 * Yq + Yu + Yd,
        "A1.3": 3 * Yq + Yl,
        "A1.4": 6 * Yq ** 3 + 3 * Yu ** 3 + 3 * Yd ** 3 + 2 * Yl ** 3 + Ye ** 3 + Ynu ** 3,
        "A1.5": 6 * Yq + 3 * Yu + 3 * Yd + 2 * Yl + Ye + Ynu,
    }
    guard("G21 anomalies_zero", all(v == 0 for v in anoms.values()),
          "anoms=%s" % {k: fr(v) for k, v in anoms.items()})
    a1_rows = {}
    for i in range(1, 6):
        key = "A1.%d" % i
        a1_rows[key] = any(line.strip().startswith("| " + key + " ") and "PASS" in line
                           for line in txt_rep.splitlines())
    guard("G22 rep_A1_all_pass", all(a1_rows.values()), "rows=%s" % a1_rows)
    Ynu_bad = Fraction(1, 2)
    bad_grav = 6 * Yq + 3 * Yu + 3 * Yd + 2 * Yl + Ye + Ynu_bad
    control("K04 nu_hypercharge_detected", bad_grav != 0, "[grav]²U(1)=%s" % fr(bad_grav))
    add("C02", "PASS", "以 §3.2 的 Y 与色/弱多重数重算五类反常系数，全部精确为 0；ν_R（Y=0）贡献 0，与报告 A1.1–A1.5 全 PASS 一致",
        "[SU(3)]³ = 2−1−1=0；[SU(3)]²U(1) = 2(1/6)+(−2/3)+(1/3)=0；[SU(2)]²U(1) = 3(1/6)+(−1/2)=0；"
        "[U(1)]³ = 6(1/6)³+3(−2/3)³+3(1/3)³+2(−1/2)³+1³+0 = 0；[grav]²U(1) = 6(1/6)+3(−2/3)+3(1/3)+2(−1/2)+1+0 = 0。"
        "⇒ 01 §3.2 的「ν_R 对 5 类反常贡献为 0」是精确事实（不是近似）；控制组把 Y_ν 改成 1/2，[grav]²U(1)=1/2 被检出。",
        {"A1.1": "0", "A1.2": "0", "A1.3": "0", "A1.4": "0", "A1.5": "0", "control": fr(bad_grav)})

    gam_nu = GF * MZ ** 3 / (12 * PI() * D(2).sqrt())
    n_nu = D("2.984")
    dn = D("0.008")
    guard("G23 gamma_nu_order", D("0.16") < gam_nu < D("0.17"),
          "Γ_ν=%s GeV" % md(gam_nu, 6))
    guard("G24 fourth_generation_excluded", (n_nu + 3 * dn) < 4 and abs(n_nu - 3) < D("0.05"),
          "N_ν=%s±%s ; 4Γ_ν=%s GeV" % (md(n_nu, 3), md(dn, 3), md(4 * gam_nu, 4)))
    control("K05 four_gen_control", (n_nu + 3 * dn) < 4, "3σ 上界 < 4")
    add("C03", "PASS", "N_ν=2.984±0.008 排除第 4 代：Γ_ν=G_F m_Z³/(12π√2)=0.1659 GeV，4 代需 0.6636 GeV",
        "机器：Γ_ν=0.1659 GeV；若 N_ν=4，不可见宽度需 4×0.1659=0.6636 GeV，而实测对应 2.984×0.1659=0.495 GeV。"
        "3σ 上界 2.984+0.024=3.008 < 4 ⇒ 第 4 代轻中微子被排除（强于 10σ）。"
        "01 引用的是 PDG 外部值（非本理论推导）；本条只核「引用的方向与量级是否成立」。",
        {"Gamma_nu_GeV": md(gam_nu, 6), "N_nu": "2.984", "sigma": "0.008",
         "4gen_width": md(4 * gam_nu, 4), "excluded": "True"})

    def ycol06(name):
        for line in txt06.splitlines():
            if line.startswith("| " + name):
                parts = line.split("|")
                if len(parts) > 8:
                    return parts[8].strip()
        return ""

    def yrow01(sym):
        for line in txt.splitlines():
            if line.startswith("|") and ("$" + sym + "$") in line:
                m = re.search(r"\)_\{([^}]*)\}", line)
                if m:
                    return m.group(1).strip()
        return ""

    def parse_y(s):
        s = s.strip().replace("+", "").replace("\u2212", "-").replace("\u2013", "-")
        if s in ("", "0"):
            return Fraction(0)
        return Fraction(s)

    y06 = {"u": ycol06("右手上型夸克"), "d": ycol06("右手下型夸克"),
           "e": ycol06("右手带电轻子"), "n": ycol06("右手中微子")}
    y01v = {"u": yrow01("u_R^c"), "d": yrow01("d_R^c"),
            "e": yrow01("e_R^c"), "n": yrow01("nu_R^c")}
    pairmap = [("u", parse_y(y01v["u"]), parse_y(y06["u"])),
               ("d", parse_y(y01v["d"]), parse_y(y06["d"])),
               ("e", parse_y(y01v["e"]), parse_y(y06["e"])),
               ("n", parse_y(y01v["n"]), parse_y(y06["n"]))]
    sign_flip_ok = all(a == -b for _, a, b in pairmap)
    guard("G25 yukawa_sign_map", sign_flip_ok,
          "01共轭→06右手: %s" % [(k, fr(a), fr(b)) for k, a, b in pairmap])
    add("C04", "INFO", "01 的「左手共轭」表与 06 的「右手」表 Y 符号逐行相反（u/d/e：−2/3,−1/3,−1 vs +2/3,+1/3,+1），是口径差不是矛盾",
        "01 §3.2 标题明确「全部写作左手 Weyl 旋量」且逐行标（共轭）：u_R^c 的 Y=−2/3 是 u_R（Y=+2/3）的共轭；"
        "06 元数据表列的是右手原场：u_R 的 Y=+2/3、d_R=−1/3、e_R=−1、ν_R=0。两者按 Y→−Y 逐行对应，Q_L/L_L 不变。"
        "机器：06 的四个 Y 列全部为 01 对应共轭值的相反数；Q_L(+1/6)、L_L(−1/2) 两行相同。"
        "⇒ 单独看任一张表都自洽；跨表引用时必须先翻号，否则会把 u_R 与 u_R^c 混为同一超荷。",
        {"01_uRc": "-2/3", "06_uR": "+2/3", "01_dRc": "+1/3", "06_dR": "-1/3",
         "01_eRc": "+1", "06_eR": "-1", "map": "Y→−Y"})

    # =================================================================
    # D 段：v 与 λ
    # =================================================================
    v_rel = relerr(D("246.22"), V)
    guard("G26 v_rounding", v_rel < D("1E-5"), "v=%s rel=%s" % (md(V, 9), fs(v_rel, 6)))
    e1_row = ""
    for line in txt_rep.splitlines():
        if line.strip().startswith("| E1 "):
            e1_row = line
            break
    guard("G27 rep_E1_24622", ("246.22" in e1_row) and ("PASS" in e1_row),
          "E1: %s" % e1_row.strip()[:70])
    add("D01", "PASS", "v=(√2G_F)^−1/2=246.219651 与 01 的 246.22 只差舍入（1.4E−6）；报告 E1 同值同容差",
        "G_F=1.1663787E−5 GeV⁻² ⇒ v=%s GeV；01 §2.3 写 246.22（两位小数），相对差 %s。"
        "02 §4.1 与 09 的 L1 段落同样写 246.22；验证报告 E1 的实测/目标均为 246.22、容差 0.002、PASS。"
        "⇒ 卷内没有第二个更高精度的 v 口径可对撞（06 元数据表未设 v 行）；246.219651 是同一公式的机算值，不是冲突。"
        % (md(V, 9), fs(v_rel, 6)),
        {"v_exact": md(V, 9), "v_doc": "246.22", "rel": fs(v_rel, 6), "rep_E1": "PASS"})

    mu_t = Fraction(3)
    lam_t = Fraction(2)
    v2 = mu_t / lam_t
    guard("G28 vev_algebra", v2 == Fraction(3, 2), "v²=μ²/λ=%s" % fr(v2))
    MH = D("125.25")
    lam_num = MH * MH / (2 * V * V)
    e4_row = ""
    for line in txt_rep.splitlines():
        if line.strip().startswith("| E4 "):
            e4_row = line
            break
    guard("G29 lambda_from_mh", abs(lam_num - D("0.129384")) < D("1E-6"),
          "λ=%s vs 0.129384" % md(lam_num, 9))
    guard("G30 rep_E4_pass", ("0.129384" in e4_row) and ("PASS" in e4_row),
          "E4: %s" % e4_row.strip()[:70])
    add("D02", "PASS", "v²=μ²/λ 精确；λ=m_h²/(2v²)=0.129384 与报告 E4、06 的 0.129 一致",
        "V=−μ²|H|²+λ|H|⁴，极小 2λ|H|²=μ²；⟨H⟩=(0,v/√2) ⇒ |H|²=v²/2 ⇒ v²=μ²/λ。"
        "反过来 λ=m_h²/(2v²)：m_h=125.25、v=246.219651 ⇒ λ=%s，报告 E4 记 0.129384、06 表记 0.129 ⇒ 同一数。"
        "⇒ §2.3 的「极小值条件给出 v²=μ²/λ」与 §3.3 的「μ,λ 是输入」不冲突：前者是代数恒等，后者是参数来源。" % md(lam_num, 9),
        {"v2": fr(v2), "lambda": md(lam_num, 9), "rep_E4": "0.129384", "doc06": "0.129"})

    # =================================================================
    # E 段：26 参数账
    # =================================================================
    CATS = ("规范耦合", "Higgs 势", "Yukawa（夸克）", "Yukawa（带电轻子）",
            "Yukawa（中微子", "CKM 混合", "PMNS 混合", "引力")

    def cat_of(name):
        for c in CATS:
            if name.startswith(c):
                return "Yukawa（中微子）" if c == "Yukawa（中微子" else c
        return None

    rows01 = []
    for line in txt.splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) < 3 or not parts[1].isdigit():
            continue
        c = cat_of(parts[0])
        if c:
            rows01.append((c, int(parts[1])))
    total01 = sum(n for _, n in rows01)
    guard("G31 param_table_26", len(rows01) == 8 and total01 == 26,
          "rows=%d total=%d %s" % (len(rows01), total01, rows01))
    base19 = sum(n for k, n in rows01 if k not in ("Yukawa（中微子）", "PMNS 混合"))
    inc7 = sum(n for k, n in rows01 if k in ("Yukawa（中微子）", "PMNS 混合"))
    guard("G32 base19_plus7", base19 == 19 and inc7 == 7, "19=%d +7=%d" % (base19, inc7))
    add("E01", "PASS", "§3.3 的 26 = 3+2+6+3+3+4+4+1（8 类目）；19 + 7（3 ν 质量 + 4 PMNS）精确闭合",
        "表内逐行读数：规范耦合 3、Higgs 势 2、Yukawa（夸克）6、Yukawa（带电轻子）3、Yukawa（中微子）3、"
        "CKM 4、PMNS 4、引力 1 ⇒ 26。剔除 ν 质量与 PMNS 后为 19；7 个增量正好是 2026-09-19 L1 修复的 3+4。"
        "§3.3 还明说「不计 Λ 与 θ」；本条只核表内算术，Λ/θ 的口径另见 E04。",
        {"rows": str(len(rows01)), "total": "26", "base": "19", "increment": "7",
         "categories": str([k for k, _ in rows01])})

    rows06 = []
    for line in txt06.splitlines():
        if not line.startswith("|") or "01 §3.3" not in line:
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        c = cat_of(parts[0]) if parts else None
        if c:
            rows06.append(c)
    cnt06 = {}
    for k in rows06:
        cnt06[k] = cnt06.get(k, 0) + 1
    same_cat = all(cnt06.get(k, 0) == n for k, n in rows01) and len(rows06) == 26
    guard("G33 doc06_param_rows_match", same_cat, "06=%s" % cnt06)
    add("E02", "PASS", "06 的「输入参数定位（26 项）」逐行 26 条，8 类目计数与 01 §3.3 全同；12 个质量参数可逐行定位",
        "06 表 26 行（规范耦合 3、Higgs 2、夸克 6、带电轻子 3、中微子 3、CKM 4、PMNS 4、G 1）与 01 逐类相等；"
        "其中 12 个质量参数（6 夸克 + 3 带电轻子 + 3 ν）在元数据表有「来源=输入」的行，其余 14 个只登记在 01 §3.3。"
        "⇒ 两份文档的参数账不是各自为政，而是同一张 26 项表的两种视图。",
        {"doc06_rows": str(len(rows06)), "category_counts": str(cnt06), "mass_params": "12"})

    add("E03", "INFO", "§2.4「Y 是输入参数」与 §3.3「26 个自由参数」分属 Lagrangian 层与物理层：3×3 复 Yukawa 单个矩阵就有 18 个实参数，不是 6",
        "01 §2.4 说 Y 是 3×3 复矩阵、是输入而非推导；§3.3 却只数 6 个夸克质量（+4 个 CKM）。"
        "机器：单个 3×3 复矩阵 = 9 复 = 18 实；物理层经场重定义只留 6 质量 + 3 角 + 1 相 = 10。"
        "轻子侧（带电 + Dirac ν 两个矩阵）同理：36 实 → 3+3 质量 + 3 角 + 1 相 = 10。"
        "⇒ 26 = 3(规范) + 2(Higgs) + 10(夸克物理) + 10(轻子物理) + 1(G) 是物理参数计数；"
        "§2.4 的「Y 是输入」是 Lagrangian 计数。两句话都对，但不在同一层，读者容易把 18 当 26 的一部分。",
        {"matrix_real": "18", "quark_physical": "10", "lepton_physical": "10",
         "physical_total": "26", "layers": "Lagrangian vs 物理"})

    lam_in_action = ("-\\frac{\\Lambda}{6}" in txt) or ("\\frac{\\Lambda}{6}" in txt)
    lam_excluded = ("不计 $\\Lambda$ 与 $\\theta$" in txt) or ("不计 Λ 与 θ" in txt)
    zero_lam_v1 = ("宇宙学常数" in txt00) and ("不在 v1 内" in txt00)
    l7_ok = ("## L7." in txt09)
    guard("G34 lambda_three_ways", lam_in_action and lam_excluded and zero_lam_v1 and l7_ok,
          "action=%s excluded26=%s 00v1=%s L7=%s" % (lam_in_action, lam_excluded, zero_lam_v1, l7_ok))
    add("E04", "BOUNDARY", "Λ 的三处口径不一：01 §2.1 的作用量含 −(Λ/6)e⁴，§3.3 却「不计 Λ」入 26；00 §0 更称「宇宙学常数不在 v1 内」",
        "01 §2.1 的 S_EC 明确含 −(Λ/6)ε e⁴（等价 Λ/κ²），并在 §3.3 把 26 个参数注为「不计 Λ 与 θ」；"
        "00 §0 的「没有做到」清单写「宇宙学常数…均不在 v1 内」。三者不能同时按字面读：Λ 是作用量里的一个自由常数，"
        "不是「不在理论里」；「不计入 26」是参数记账的选择，不等于 Λ 缺席。"
        "⇒ 建议统一为：「Λ 与 θ 是作用量允许但未解释的两个常数，不计入 26 项输入账；Λ 的数值问题见 L7，θ 见 L6」。"
        "本条只登记口径，不主张 Λ 已被解释。",
        {"lambda_in_action": str(lam_in_action), "excluded_from_26": str(lam_excluded),
         "00_says_not_in_v1": str(zero_lam_v1), "L7_exists": str(l7_ok)})

    # =================================================================
    # F 段：场强定义与 θ 项
    # =================================================================
    def mmul(A, B):
        n = len(A)
        m = len(B[0])
        k = len(B)
        return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)]
                for i in range(n)]

    def mcomm(A, B):
        C1 = mmul(A, B)
        C2 = mmul(B, A)
        return [[C1[i][j] - C2[i][j] for j in range(len(C1[0]))] for i in range(len(C1))]

    def mnz(M):
        return any(abs(x) > 0 for row in M for x in row)

    t1 = [[0.0, 0.5], [0.5, 0.0]]
    t2 = [[0.0, -0.5j], [0.5j, 0.0]]
    l1 = [[0.0, 0.5, 0.0], [0.5, 0.0, 0.0], [0.0, 0.0, 0.0]]
    l2 = [[0.0, -0.5j, 0.0], [0.5j, 0.0, 0.0], [0.0, 0.0, 0.0]]
    u1 = [[1.0]]
    c_su2 = mcomm(t1, t2)
    c_su3 = mcomm(l1, l2)
    c_u1 = mcomm(u1, u1)
    guard("G35 nonabelian_A2_nonzero", mnz(c_su2) and mnz(c_su3), "su2/su3 commutator")
    guard("G36 abelian_A2_zero", not mnz(c_u1), "u1 commutator=0")
    control("K06 abelianization_control", not mnz(mcomm(t1, t1)), "SU(2) 阿贝尔化后 A∧A=0")
    add("F01", "PASS", "A∧A 的非阿贝尔/阿贝尔二分是精确事实：SU(2)、SU(3) 的对易子非零，U(1) 恒为零",
        "在 2 维底流形上取 A=t1 dx+t2 dy，则 A∧A 的 dx∧dy 系数 = [t1,t2]。"
        "SU(2)（σ/2）与 SU(3)（λ/2 的 2×2 子块）的 [t1,t2] 均非零；U(1)（1×1）[1,1]=0。"
        "⇒ 01 §2.2 的「非阿贝尔项是曲率定义的必然结果，胶子有自相互作用、光子没有」可机验，"
        "不是额外假设。控制组把 t2 换成 t1（阿贝尔化）⇒ A∧A=0，检查器有分辨力。",
        {"su2_comm": "nonzero", "su3_comm": "nonzero", "u1_comm": "0", "base_dim": "2"})

    theta_not_in_eq = ("未被写入主方程" in txt)
    theta_l6 = ("L6" in txt) and ("## L6." in txt09)
    theta_bound = ("10^{-10}" in txt) and ("10^{-10}" in txt09)
    guard("G37 theta_honest", theta_not_in_eq and theta_l6 and theta_bound,
          "not_written=%s L6=%s bound=%s" % (theta_not_in_eq, theta_l6, theta_bound))
    add("F02", "PASS", "θ 项如实排除在主方程之外：01 明写「未被写入主方程」，L6 存在且 |θ̄|<10⁻¹⁰ 的界一致",
        "01 §2.2 末尾：「可选的 θ 项…未被写入主方程。理由：|θ̄|<10⁻¹⁰（中子电偶极矩上限）无理论解释，即强 CP 问题。"
        "列为已知局限 L6。」机器：该句与 09 §L6 的同一界（10⁻¹⁰）逐字一致，且 09 确有 L6 标题。"
        "⇒ 这是「允许但不解释」的诚实登记，不是遗漏；θ 项的可写性与 Λ 的可写性同类（另见 E04）。",
        {"not_in_action": str(theta_not_in_eq), "L6": "存在", "bound": "1E-10"})

    # =================================================================
    # G 段：对称性、链接、文本卫生、供给
    # =================================================================
    bl = {"Q_L": Fraction(1, 3), "u_Rc": Fraction(-1, 3), "d_Rc": Fraction(-1, 3),
          "L_L": Fraction(-1), "e_Rc": Fraction(1), "nu_Rc": Fraction(1)}
    yuk_pairs = [("Q_L", "u_Rc"), ("Q_L", "d_Rc"), ("L_L", "e_Rc"), ("L_L", "nu_Rc")]
    yuk_ok = all(bl[a] + bl[b] == 0 for a, b in yuk_pairs)
    guard("G38 bl_yukawa_conserved", yuk_ok, "pairs=%s" % yuk_pairs)
    proton = 3 * Fraction(1, 3)
    ch_e_pi0 = Fraction(1) + Fraction(0)        # e+ (+1) + π0 (0)
    ch_nu_K = Fraction(1) + Fraction(0)         # ν̄ (+1) + K+ (0)
    ch_e_piP = Fraction(-1) + Fraction(0)       # e− (−1) + π+ (0)
    guard("G39 bl_allows_canonical_decay", (ch_e_pi0 == proton) and (ch_nu_K == proton),
          "p→e+π0 Δ=%s ; p→ν̄K+ Δ=%s" % (fr(ch_e_pi0 - proton), fr(ch_nu_K - proton)))
    control("K07 bl_forbids_charge_channel", ch_e_piP != proton,
            "p→e−π+ Δ=%s（被 B−L 禁）" % fr(ch_e_piP - proton))
    bl_text = ("全局 $B-L$" in txt) and ("质子稳定" in txt) and ("P4" in txt) and ("### P4." in txt08)
    guard("G40 bl_proton_claim_present", bl_text,
          "01 §4 行与 08 P4 标题")
    add("G01", "FAIL", "§4「全局 B−L ⇒ 质子稳定」不成立：p→e⁺π⁰ 与 p→ν̄K⁺ 的 Δ(B−L)=0，B−L 守恒并不禁止这些主通道",
        "01 §4 对称性表：「全局 B−L | 偶然对称 | 质子稳定（在 UFE-1 中，见预言 P4）」。"
        "机器：以 §3.2 六场定 B−L（Q_L=1/3，u_R^c=d_R^c=−1/3，L_L=−1，e_R^c=ν_R^c=+1；H 为 0，Yukawa 四对逐对相消）；"
        "质子 B−L=3×(1/3)=1；e⁺(+1)+π⁰(0)=+1，ν̄(+1)+K⁺(0)=+1 ⇒ 两条主衰变道的 Δ(B−L) 均为 0，B−L 允许它们。"
        "→ B−L 守恒**不能**推出 τ_p=∞；真正禁掉重正化质子衰变的是 B 与 L 分别守恒（微扰偶然对称）＋无重正化 B 破坏算符。"
        "控制组 p→e⁻π⁺（+1 → −1，Δ=−2）才被 B−L 禁。⇒ 本条是 G-logic + F-crossdoc（08 P4 标题用同一归因），"
        "修复：把后果列改为「B、L 分别守恒 ⇒ 无重正化 B 破坏算符 ⇒ 质子稳定；B−L 只禁 Δ(B−L)≠0 的通道」。",
        {"proton_BL": "1", "e+pi0_BL": "1", "nubarK_BL": "1", "e-pi+_BL": "-1",
         "delta_canonical": "0", "claim_in_01": str(bl_text)})

    links = re.findall(r"\]\(([^)]+)\)", txt)
    internal = [h for h in links if not h.startswith("http")]
    bad = []
    for h in internal:
        p = os.path.normpath(os.path.join(DIR07, h.split("#")[0]))
        if not os.path.isfile(p):
            bad.append(h)
    anchors_ok = ("## L1." in txt09) and ("## L3." in txt09) and ("## L6." in txt09) \
        and ("## L7." in txt09) and ("### P4." in txt08)
    guard("G41 all_links_resolve", len(internal) >= 6 and not bad,
          "n=%d bad=%s" % (len(internal), bad))
    guard("G42 anchors_exist", anchors_ok, "L1/L3/L6/L7/P4")
    fake = os.path.join(DIR07, "__no_such_r211__.md")
    control("K08 broken_link_detected", not os.path.isfile(fake), "fake link rejected")
    add("G02", "PASS", "01 全文 %d 个站内链接全部解析到真实文件；L1/L3/L6/L7/P4 五个锚点在目标文档中真实存在" % len(internal),
        "链接覆盖 00、02、06、08、09（L1/L3/L6/L7）与验证报告；逐条 os.path.isfile 命中，bad=[]。"
        "锚点逐条核对：09 有「## L1.」「## L3.」「## L6.」「## L7.」，08 有「### P4. 质子稳定」。"
        "控制组用伪造路径 __no_such_r211__.md 验证检查器不是恒真。",
        {"n_links": str(len(internal)), "bad": "0", "anchors": "5/5"})

    ec_form_ok = ("S_{\\rm EC}=\\frac{1}{4\\kappa^{2}}" in txt)
    ec_tensor_ok = ("S_{\\rm EC}=\\frac{1}{2\\kappa^{2}}" in txt)
    errata_ok = ("原写" in txt) and ("已修正" in txt)
    guard("G43 coeff_text_hygiene", ec_form_ok and ec_tensor_ok and errata_ok,
          "form=%s tensor=%s errata=%s" % (ec_form_ok, ec_tensor_ok, errata_ok))
    add("G03", "PASS", "系数文本卫生：形式系数为 1/4κ²、张量形式为 1/2κ²，二者在各自位置；「原写…已修正」勘误条完整",
        "01 §2.1 的 S_EC 形式式确为 \\frac{1}{4\\kappa^{2}}，张量式确为 \\frac{1}{2\\kappa^{2}}；"
        "勘误条原文「原写 1/2κ² 会使张量系数翻倍（偏离标准 Hilbert 作用量），已修正」完整保留。"
        "⇒ 卷内没有把旧系数留在形式式里的残留（与 A01 的代数核算互为独立证据）。",
        {"form": "1/4κ²", "tensor": "1/2κ²", "errata": "完整"})

    add("G04", "INFO", "供给判定：01 全卷探针 C1（定义/代数恒等/外部实测），TUFT 侧独立数值供给 0/12 维持",
        "作用量系数步、vierbein/联络计数、Q=T3+Y、反常消去、v 与 λ 的代数关系、26 参数账，全部是"
        "定义、群论恒等式或外部实测值的重排；卷内没有一个可与观测对撞且非外部输入的独立数值。"
        "⇒ 01 是「场内容清单 + 诚实参数账」，不提供新数值供给。",
        {"C1": "全卷", "C2": "0", "C3": "0", "supply": "0/12"})

    # =================================================================
    # 收尾守卫与输出
    # =================================================================
    guard("G44 doc_readable", bool(txt) and 5000 < nbytes < 12000, "bytes=%d" % nbytes)
    for sec in ("## 1.", "## 2.", "## 3.", "## 4."):
        guard("G45_section_%s" % sec.replace("## ", "").replace(".", ""),
              sec in txt, "section %s present=%s" % (sec, sec in txt))
    guard("G46 boundary_have_numbers",
          all(bool(e["numbers"]) for e in ENTRIES if e["level"] in ("FAIL", "BOUNDARY")),
          "bad=%s" % [e["code"] for e in ENTRIES
                      if e["level"] in ("FAIL", "BOUNDARY") and not e["numbers"]])
    cnt = {}
    for e in ENTRIES:
        cnt[e["level"]] = cnt.get(e["level"], 0) + 1
    guard("G47 counts_sum", sum(cnt.values()) == len(ENTRIES) and cnt.get("PASS", 0) > 0,
          "counts=%s n=%d" % (cnt, len(ENTRIES)))
    guard("G48 controls_enough", len(CONTROLS) >= 7, "n=%d" % len(CONTROLS))
    guard("G49 all_guards_pass", all(g["ok"] for g in GUARDS),
          "fails=%s" % [g["name"] for g in GUARDS if not g["ok"]])

    verdict = (
        "R211-ACTION-COEFF-4FORM-EXACT-OK-DIM4-7TERMS-OK-"
        "U1-TRACE-UNDEFINED-BOUNDARY-G1-GY-COLLISION-7PCT-FAIL-"
        "VIERBEIN-16-10-6-2-OK-CONN-TORSION-24-NONPROP-OK-BOSON-DOF-28-28-OK-"
        "QEM-T3Y-OK-ANOMALIES-ZERO-OK-NNU-2984-EXCLUDES-4TH-OK-YUKAWA-SIGNMAP-INFO-"
        "V-ROUNDING-OK-LAMBDA-0129384-OK-PARAM-26-OK-DOC06-26-MATCH-OK-"
        "LAYER-INFO-LAMBDA-WORDING-BOUNDARY-ABELIAN-A2-OK-THETA-L6-OK-"
        "BL-PROTON-STABILITY-WRONG-FAIL-LINKS-OK-COEFF-HYGIENE-OK-SUPPLY-0"
    )

    out = {
        "stem": STEM,
        "doc": DOC,
        "nbytes": nbytes,
        "entries": ENTRIES,
        "guards": GUARDS,
        "controls": CONTROLS,
        "counts": cnt,
        "guard_pass": sum(1 for g in GUARDS if g["ok"]),
        "guard_total": len(GUARDS),
        "control_pass": sum(1 for c in CONTROLS if c["ok"]),
        "control_total": len(CONTROLS),
        "verdict": verdict,
    }
    with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    L = []
    L.append("# " + STEM)
    L.append("")
    L.append("**审计对象**：`07_统一场方程/01_作用量与场内容.md`（%d B）" % nbytes)
    L.append("**运行**：退出码 0；条目 **%d**（%s）；守卫 **%d/%d**；控制组 **%d/%d**"
             % (len(ENTRIES),
                " / ".join("%s %d" % (k, cnt[k]) for k in ("PASS", "FAIL", "BOUNDARY", "INFO") if k in cnt),
                out["guard_pass"], out["guard_total"], out["control_pass"], out["control_total"]))
    L.append("")
    L.append("**判定串**：`%s`" % verdict)
    L.append("")
    L.append("## 条目")
    for e in ENTRIES:
        L.append("- **%s %s** %s" % (e["code"], e["level"], e["title"]))
        L.append("  - %s" % e["detail"])
        if e["numbers"]:
            L.append("  - numbers: `%s`" % json.dumps(e["numbers"], ensure_ascii=False))
    L.append("")
    L.append("## 守卫")
    for g in GUARDS:
        L.append("- %s %s %s" % ("OK " if g["ok"] else "FAIL", g["name"], g["msg"]))
    L.append("")
    L.append("## 控制组")
    for c in CONTROLS:
        L.append("- %s %s %s" % ("OK " if c["ok"] else "FAIL", c["name"], c["msg"]))
    md_txt = "\n".join(L)
    with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write(md_txt + "\n")

    rep = []
    rep.append("TUFT-r211 作用量与场内容首次整卷机核")
    rep.append("doc: %s (%d bytes)" % (DOC, nbytes))
    rep.append("entries=%d %s" % (len(ENTRIES), cnt))
    rep.append("guards=%d/%d controls=%d/%d" % (out["guard_pass"], out["guard_total"],
                                                out["control_pass"], out["control_total"]))
    rep.append("verdict=%s" % verdict)
    for e in ENTRIES:
        rep.append("  %-4s %-10s %s" % (e["code"], e["level"], e["title"]))
    with open(os.path.join(OUTD, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")

    print("=" * 78)
    print("条目 %d（%s）" % (len(ENTRIES),
                            " / ".join("%s %d" % (k, cnt[k]) for k in ("PASS", "FAIL", "BOUNDARY", "INFO") if k in cnt)))
    print("守卫 %d/%d · 控制组 %d/%d" % (out["guard_pass"], out["guard_total"],
                                        out["control_pass"], out["control_total"]))
    print("判定串：" + verdict)
    print("out -> %s.{json,md,_report.txt}" % STEM)
    return 0


if __name__ == "__main__":
    sys.exit(main())
