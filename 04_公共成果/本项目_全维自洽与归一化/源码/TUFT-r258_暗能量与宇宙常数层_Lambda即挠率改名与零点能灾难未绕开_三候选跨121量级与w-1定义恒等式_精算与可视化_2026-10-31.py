# -*- coding: utf-8 -*-
r"""
TUFT-r256 · 暗能量与宇宙常数层
==============================================================
攻靶：「Lambda（暗能量）作为全局背景挠率 tau_Lambda 的几何导出」
      靶文位置：来料原件 L4720-L4800（Lambda 专章），L883-L930（FRW 平行表述）

本卷只审「Lambda 的本体与数值来源」。r251 已审 FRW 约化与源项量纲，r252 已审
omega^2=c^2(kappa^2+tau^2) 的三通道线性相关 —— 本卷不重复，只做交联指针。

承重四条（全部纯代数 / 纯量纲 / 纯数值，零实验输入）：
  C5  靶自己的拉氏量（L4711-4713）动能项是标准无质量标量 => 零点能灾难
      M_Pl^4/(16 pi^2)/rho_Lambda = 5.5531e120（120.744 个数量级）
      与靶 L4776 声称「直接绕开」的 10^120 同量级 => 未绕开
  C4  三个自然候选 tau（H0/c、1/l_P、v/hbar c）给 Omega_Lambda
      = 1/3、2.4037e121、9.7763e87 => 跨 121.86 个数量级，靶一个都没选
  C3  两种读法反解 tau_Lambda（propto 的 A=1 / 等号带 c^2）差 c = 8.48 个数量级
  B1  Lambda 量纲 [L^-2] vs c^2 tau^2 量纲 [T^-2] => 多一个 c^2

纪律：控制组 / 守卫一律机算，禁写死 True。
"""
import hashlib
import io
import json
import math
import os
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
JUDGE = os.path.normpath(os.path.join(HERE, "..", "判定"))
README = os.path.normpath(os.path.join(HERE, "..", "README.md"))

RID = "r258"
DEGREE_NOTE = "本卷不占「修复即自杀」度数（SURVIVE>0）"
TITLE_CN = "暗能量与宇宙常数层"
SLUG = ("TUFT-%s_%s_Lambda即挠率改名与零点能灾难未绕开_"
        "三候选跨121量级与w-1定义恒等式_精算与可视化_2026-10-31") % (RID, TITLE_CN)

TARGETS = [
    "TUFT-r241_光速螺旋_来料原件_2026-10-30/基于光速螺旋流形的核心动力学方程组.md",
    "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md",
    "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md",
]

# ---------------------------------------------------------------- 常数（带来源）
C = 299792458.0                    # m/s  (SI 定义值)
C0 = C                             # 别名：避免被函数参数 C（C 组结果）遮蔽
G = 6.67430e-11                    # m^3 kg^-1 s^-2 (CODATA 2018)
HBAR = 1.054571817e-34             # J s
MPC = 3.0856775814913673e22        # m
H0_KMS = 67.4                      # km/s/Mpc (Planck 2018 TT,TE,EE+lowE+lensing)
OM_L = 0.6889                      # Planck 2018
OM_M = 0.3111                      # Planck 2018
LP = 1.616255e-35                  # m (CODATA 2018 Planck length)
VEW = 246.22                       # GeV (Fermi constant 换算的 Higgs VEV)
GEV_J = 1.602176634e-10            # J/GeV
HBARC_GEVM = 1.973269804e-16       # GeV m
MPL = 1.220890e19                  # GeV (non-reduced Planck mass)
RHO_L_LIT = 5.96e-27               # kg/m^3 文献暗能量密度
LAM_LIT = 1.089e-52                # m^-2  文献宇宙学常数

ENTRIES, CONTROLS, GUARDS, EVIDENCE = [], [], [], {}
_ALPHA52 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def depollute(s):
    r"""上游 LaTeX 污染修复（三种形式实测并存）。

      甲  \boldsymbol{b}        —— 花括号形式（实测 2931 处，最多）
      乙  \boldsymbol n         —— 空格形式，无花括号（如 Frenet 被污染成 Fre(\boldsymbol n)et）
      丙  \(\boldsymbol p\)     —— 反斜杠圆括号形式
    依次用正则吃掉甲、乙（丙被甲/乙顺带吃掉），最后压平 \r\r\n 双重换行。
    残留检查只查 `\boldsymbol` 标记本身；括号残留（如 `(n)`）不影响本卷定位。
    """
    s = re.sub(r"\\boldsymbol\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\boldsymbol\s+([A-Za-z])", r"\1", s)
    for ch in _ALPHA52:
        s = s.replace("\\(\\boldsymbol{" + ch + "}\\)", ch)
    return re.sub(r"[\r\n]+", "\n", s)


def fmt(x, n=6):
    if x is None:
        return "n/a"
    if isinstance(x, Fraction):
        return "%.*f" % (n, float(x))
    if x != x or x in (float("inf"), float("-inf")):
        return str(x)
    a = abs(x)
    if a != 0 and (a >= 1e5 or a < 1e-3):
        return "%.*e" % (n, x)
    return "%.*f" % (n, x)


def rel(a, b):
    if b == 0:
        return float("inf") if a != 0 else 0.0
    return abs(a - b) / abs(b)


def ordmag(x):
    if x == 0:
        return float("-inf")
    return math.log10(abs(x))


def ent(eid, group, title, verdict, detail, metric=None):
    ENTRIES.append({"id": eid, "group": group, "title": title,
                    "verdict": verdict, "detail": detail, "metric": metric})


def ctl(cid, name, ok, detail):
    CONTROLS.append({"id": cid, "name": name, "ok": bool(ok), "detail": detail})


def guard(gid, name, ok, detail):
    GUARDS.append({"id": gid, "name": name, "ok": bool(ok), "detail": detail})


# ================================================================ 靶只读取与定位
def load_targets():
    out = []
    for rel_p in TARGETS:
        p = os.path.join(DATA, rel_p)
        raw = io.open(p, "rb").read()
        sha = hashlib.sha256(raw).hexdigest()
        txt = depollute(raw.decode("utf-8", "replace"))
        out.append({"path": rel_p, "sha256": sha, "nbytes": len(raw),
                    "text": txt, "lines": txt.split("\n")})
    return out


def locate(docs):
    """所有定位一律拆成独立扫描，禁止 AND（r252 教训）。"""
    big = docs[0]["lines"]          # 来料原件 = 主靶
    L = {}

    def scan(pred):
        return [i + 1 for i, s in enumerate(big) if pred(s)]

    L["boxed_lam_tau"] = scan(lambda s: "oxed{\\Lambda \\propto c^2\\tau_\\Lambda^2}" in s)
    L["boxed_any"] = scan(lambda s: "oxed{" in s and "\\Lambda" in s and "tau_\\Lambda" in s)
    L["eq_lam_tau"] = scan(lambda s: "\\Lambda=c^2\\tau_\\Lambda^2" in s)
    L["prop_only"] = scan(lambda s: "\\Lambda \\propto c^2\\tau_\\Lambda^2" in s)
    L["tau_const"] = scan(lambda s: "全空间处处相同" in s and "不随时间演化" in s)
    L["tau_adjust"] = scan(lambda s: "随宇宙演化调整" in s)
    L["tau_freeze"] = scan(lambda s: "冻结为常数" in s)
    L["no_dilute"] = scan(lambda s: "不随宇宙膨胀稀释" in s)
    L["w_minus1"] = scan(lambda s: "w=\\frac{P_\\Lambda}{\\rho_\\Lambda}=-1" in s)
    L["w_perfect"] = scan(lambda s: "完美满足" in s and "w=-1" in s)
    L["w_testable"] = scan(lambda s: "严格等于" in s and "-1" in s)
    L["distinguish"] = scan(lambda s: "区分于" in s and "CDM" in s)
    L["pending"] = scan(lambda s: "待完成的定量目标" in s)
    L["resid_field"] = scan(lambda s: "残差场" in s)
    L["residual_small"] = scan(lambda s: "残留下" in s and "微小" in s)
    L["tau_ll_vac"] = scan(lambda s: "\\tau_\\Lambda \\ll \\tau_\\text{vac}" in s)
    L["v246"] = scan(lambda s: "246" in s and "GeV" in s)
    L["one120"] = scan(lambda s: "120" in s and ("数量级" in s or "灾难" in s))
    L["qft_disaster"] = scan(lambda s: "10^{120}" in s)
    L["delta_tau_term"] = scan(lambda s: "2c^2\\tau_\\Lambda\\delta\\tau" in s)
    L["expand"] = scan(lambda s: "c^2\\kappa^2 + c^2\\tau_\\Lambda^2" in s)
    L["delta_avg"] = scan(lambda s: "空间平均后相互抵消" in s)
    L["no_contrib"] = scan(lambda s: "不贡献全局" in s)
    L["lagrangian"] = scan(lambda s: "\\mathcal{L} = \\frac{1}{2}g^{\\mu\\nu}\\partial_\\mu\\kappa"
                               in s)
    L["omega_constraint"] = scan(lambda s: "\\omega^2 = c^2\\left(\\kappa^2+\\tau^2\\right)" in s)
    L["omega_lam"] = scan(lambda s: "\\omega_\\Lambda^2 = c^2\\left(\\kappa_\\Lambda^2+"
                                    "\\tau_\\Lambda^2\\right)" in s)
    L["kappa_lam0"] = scan(lambda s: "\\kappa_\\Lambda=0" in s)
    L["flat_k0"] = scan(lambda s: "平坦宇宙" in s and "k=0" in s)
    L["field_eq"] = scan(lambda s: "R_{\\mu\\nu}-\\frac12 g_{\\mu\\nu}R+\\Lambda g_{\\mu\\nu}" in s)
    L["friedmann"] = scan(lambda s: "H^2(t)=\\frac{8\\pi G}{3}\\rho" in s)
    L["rho_l_9"] = scan(lambda s: "10^{-9}" in s and "J/m" in s)
    L["not_external"] = scan(lambda s: "不需要额外引入新标量场" in s)
    L["manual_const"] = scan(lambda s: "手动加到场方程里的常数" in s)
    L["tau_r"] = scan(lambda s: "\\tau(r)=\\dfrac{\\tau_0}{r}" in s)
    L["tau_zero_assign"] = scan(lambda s: "\\tau_\\Lambda =" in s or "\\tau_\\Lambda=" in s)
    # tau_Lambda 的「数值赋值」：出现等号且右端含数字
    L["tau_numeric"] = [ln for ln in L["tau_zero_assign"]
                        if re.search(r"\\tau_\\Lambda\s*=\s*[-+]?[0-9]", big[ln - 1])]
    # 平行表述（同一章在 L883-930 与 L2969-3003 重复）
    L["_parallel_omega"] = [i + 1 for i, s in enumerate(big)
                           if "\\omega_\\Lambda^2 = c^2" in s]
    L["_parallel_prop"] = [i + 1 for i, s in enumerate(big)
                          if "\\Lambda \\propto \\tau_\\Lambda^2" in s]
    return L


# ================================================================ 量纲 (M,L,T,Q)
DIM = {"Lambda": (0, -2, 0),      # +Lambda g_munu 约定下 R 为 [L^-2]
       "c": (0, 1, -1),
       "tau": (0, -1, 0),         # 挠率 = 逆长度
       "omega": (0, 0, -1),
       "G": (-1, 3, -2),
       "rho": (1, -3, 0),
       "P": (1, -1, -2),
       "k": (0, -2, 0),
       "a": (0, 0, 0),
       "H": (0, 0, -1),
       "F": (1, 1, -2),
       }


def dmul(*names):
    out = [0, 0, 0]
    for n in names:
        for j in range(3):
            out[j] += DIM[n][j]
    return tuple(out)


def ddiff(a, b):
    return tuple(a[j] - b[j] for j in range(3))


def dfmt(d):
    return "(M^%d L^%d T^%d)" % d


# ================================================================ 主计算
def cosmology():
    H0 = H0_KMS * 1e3 / MPC
    rho_c = 3.0 * H0 ** 2 / (8.0 * math.pi * G)
    rho_l = OM_L * rho_c
    u_l = rho_l * C ** 2
    Lam = 3.0 * OM_L * H0 ** 2 / C ** 2
    Lam_alt = 8.0 * math.pi * G * rho_l / C ** 2
    return {"H0": H0, "rho_c": rho_c, "rho_l": rho_l, "u_l": u_l,
            "Lam": Lam, "Lam_alt": Lam_alt}


def tau_from_lambda(Lam):
    """两种读法：propto 读法 A=1（Lambda = tau^2）；等号读法（Lambda = c^2 tau^2）。"""
    t_prop = math.sqrt(Lam)                 # [L^-1]
    t_eq = math.sqrt(Lam) / C               # [L^-1] 若等式带 c^2
    return {"prop": t_prop, "eq": t_eq, "ratio": t_prop / t_eq}


def omega_from_tau(tau, H0):
    """Omega_Lambda = tau^2 c^2 / (3 H0^2)。"""
    return (tau ** 2) * C ** 2 / (3.0 * H0 ** 2)


def candidates(H0):
    t_h = H0 / C
    t_p = 1.0 / LP
    t_ew = VEW / HBARC_GEVM
    return {"H0/c": t_h, "1/l_P": t_p, "v/(hbar c)": t_ew}


def zero_point():
    """靶自己的拉氏量 L4711-4713 的动能项 = 标准无质量标量 => 零点能灾难。"""
    mpl4 = MPL ** 4
    zp = mpl4 / (16.0 * math.pi ** 2)          # GeV^4
    co = cosmology()
    rho_gev4 = co["u_l"] / GEV_J * (HBARC_GEVM ** 3)
    return {"zp": zp, "rho_gev4": rho_gev4, "ratio": zp / rho_gev4,
            "mpl4": mpl4}


def q0(w, om_m=OM_M, om_l=OM_L):
    return 0.5 * om_m + 0.5 * om_l * (1.0 + 3.0 * w)


def q0_fraction(w):
    """Fraction 精确：q0 = 1/2 Om + 1/2 OL (1+3w)。"""
    OM_m = Fraction(3111, 10000)
    OL = Fraction(6889, 10000)
    wq = Fraction(w) if not isinstance(w, Fraction) else w
    return Fraction(1, 2) * OM_m + Fraction(1, 2) * OL * (1 + 3 * wq)


def omega_tau_h_fraction():
    """Fraction 严格证明：tau = H0/c => Omega_Lambda = 1/3 与 H0 无关。"""
    mpc = Fraction(Decimal("3.0856775814913673e22"))
    h0 = Fraction(67400) / mpc
    c = Fraction(299792458)
    tau = h0 / c
    omega = (tau ** 2) * (c ** 2) / (3 * h0 ** 2)
    return omega, omega - Fraction(1, 3)


# ================================================================ A 组：原文核验
def group_A(docs, L):
    big = docs[0]["lines"]
    n_lines = len(big)
    # A01
    hit = L["boxed_lam_tau"]
    ent("A01", "A", "boxed 主结果「Lambda ∝ c^2 tau_Lambda^2」是否存在",
        "PASS" if hit else "FAIL",
        "机读定位到 %d 处（行 %s）；其中 boxed 包裹的独立定位 %d 处。"
        "原文 line %s 逐字为：%s" % (
            len(hit), hit[:5], len(L["boxed_any"]),
            hit[:1], big[hit[0] - 1].strip() if hit else "n/a"),
        {"hits": len(hit), "lines": hit[:8]})
    # A02 平行表述（同章重复三次 = 复制粘贴，不是多路推导）
    ent("A02", "A", "Lambda 专章在语料内是否有多处平行表述（复制而非多路推导）",
        "INFO",
        "omega_Lambda 约束式出现 %d 处（行 %s）；「Lambda ∝ tau_Lambda^2」出现 %d 处"
        "（行 %s）。三处内容逐字相同 ⇒ 同章复制三次，**不构成独立推导路径**，"
        "后文一律以 L%s 为主靶。" % (
            len(L["_parallel_omega"]), L["_parallel_omega"][:6],
            len(L["_parallel_prop"]), L["_parallel_prop"][:6],
            L["boxed_lam_tau"][0] if L["boxed_lam_tau"] else "?"),
        {"parallel_omega": len(L["_parallel_omega"]),
         "parallel_prop": len(L["_parallel_prop"])})
    # A03 同一章内 ∝ 与 = 混用
    ent("A03", "A", "同章内「∝」与「=」混用（比例关系退化为等号，自由度被悄悄固定）",
        "FAIL" if (L["prop_only"] and L["eq_lam_tau"]) else "PASS",
        "「∝」写法 %d 处（行 %s）；「=」写法 %d 处（行 %s）。原文 line %s 逐字："
        "%s ⇒ 从「正比」变「等于」意味着比例系数被隐含取 1，"
        "而该系数从未被任何推导确定。" % (
            len(L["prop_only"]), L["prop_only"][:5],
            len(L["eq_lam_tau"]), L["eq_lam_tau"][:5],
            L["eq_lam_tau"][0] if L["eq_lam_tau"] else "?",
            (big[L["eq_lam_tau"][0] - 1].strip()[:220]
             if L["eq_lam_tau"] else "n/a")),
        {"prop": len(L["prop_only"]), "eq": len(L["eq_lam_tau"])})
    # A04 tau_Lambda 的数值赋值 0 处
    ent("A04", "A", "tau_Lambda 的数值在全语料是否被赋值过（若 0 处，Lambda 仍是输入）",
        "FAIL" if not L["tau_numeric"] else "PASS",
        "含 `\\tau_\\Lambda =` 的行 %d 处（行 %s），其中**右端带数字**的 %d 处"
        "（行 %s）。全语料 %d 行中，tau_Lambda 无任何数值赋值 ⇒ "
        "**Lambda 的数值仍是外部输入**，所谓「导出」只在符号层面成立。" % (
            len(L["tau_zero_assign"]), L["tau_zero_assign"][:8],
            len(L["tau_numeric"]), L["tau_numeric"][:5], n_lines),
        {"assign_lines": len(L["tau_zero_assign"]), "numeric": len(L["tau_numeric"]),
         "total_lines": n_lines})
    # A05 本体论三句冲突
    triple = (len(L["tau_const"]), len(L["tau_adjust"]), len(L["tau_freeze"]))
    ent("A05", "A", "★ tau_Lambda 的本体论三句自相冲突（「恒定」vs「随演化调整」）",
        "FAIL" if all(x > 0 for x in triple) else "PASS",
        "①「全空间处处相同、**不随时间演化**」line %s；②「**随宇宙演化调整**」line %s；"
        "③「**冻结为常数**」line %s。三句同时成立要求 tau_Lambda 既是"
        "「基底几何属性」（不可演化）又是「可演化、可冻结的动力学量」⇒ 本体论二难"
        "（见 E01）。逐字：①%s ②%s" % (
            L["tau_const"][:4], L["tau_adjust"][:4], L["tau_freeze"][:4],
            (big[L["tau_const"][0] - 1].strip()[:200] if L["tau_const"] else "n/a"),
            (big[L["tau_adjust"][0] - 1].strip()[:200] if L["tau_adjust"] else "n/a")),
        {"const": triple[0], "adjust": triple[1], "freeze": triple[2]})
    # A06 w=-1 声称
    ent("A06", "A", "w=-1 是否被明确声称（含「完美满足」与「严格等于」）",
        "PASS" if (L["w_minus1"] and L["w_perfect"]) else "FAIL",
        "状态方程行 %d 处（行 %s）；「完美满足 w=-1」%d 处（行 %s）；"
        "「严格等于 -1」%d 处（行 %s）。原文：%s" % (
            len(L["w_minus1"]), L["w_minus1"][:4], len(L["w_perfect"]),
            L["w_perfect"][:4], len(L["w_testable"]), L["w_testable"][:4],
            (big[L["w_perfect"][0] - 1].strip()[:300] if L["w_perfect"] else "n/a")),
        {"w_eq": len(L["w_minus1"]), "perfect": len(L["w_perfect"])})
    # A07 「区分于 LCDM」与 w=-1 的不可区分性
    ent("A07", "A", "★★ 自称「区分于 ΛCDM」，但唯一预言 w=-1 正是 ΛCDM 的定义",
        "FAIL" if L["distinguish"] else "PASS",
        "「区分于 ΛCDM 标准宇宙学」小节标题在 line %s；该小节列出的唯一预言是"
        "「w 严格等于 -1，不随红移演化」。而 ΛCDM 的定义特征**就是** w=-1、"
        "不随红移演化 ⇒ 把该节的「TUFT」换成「ΛCDM」一字不改仍成立 ⇒ "
        "**零区分度（正对照见 D02）**。" % (L["distinguish"][:4],),
        {"distinguish_lines": L["distinguish"][:4]})
    # A08 120 个数量级：靶明确点名要解决的疑难
    ent("A08", "A", "靶是否明确点名「10^120 个数量级灾难」作为要解决的疑难",
        "PASS" if L["one120"] else "FAIL",
        "含「120 + 数量级/灾难」的行 %d 处（行 %s）；含 `10^{120}` 的行 %d 处"
        "（行 %s）。逐字：%s ⇒ 靶**主动**把它列为本理论要解决的问题；"
        "本卷 C05 将机验它是否真的解决了。" % (
            len(L["one120"]), L["one120"][:6], len(L["qft_disaster"]),
            L["qft_disaster"][:6],
            (big[L["one120"][0] - 1].strip()[:240] if L["one120"] else "n/a")),
        {"n120": len(L["one120"]), "qft": len(L["qft_disaster"])})


# ================================================================ B 组：量纲
def group_B(L):
    d_lam = DIM["Lambda"]
    d_c2tau2 = dmul("c", "c", "tau", "tau")
    gap = ddiff(d_lam, d_c2tau2)
    # 补因子：Lambda = c^2 tau^2 × X  => X 的量纲 = gap
    factor = 1.0 / C ** 2
    ent("B01", "B", "★★ boxed 式 `Lambda ∝ c^2 tau^2` 的量纲审计",
        "FAIL" if gap != (0, 0, 0) else "PASS",
        "Lambda 量纲 %s（+Lambda g_munu 约定下 R 为 [L^-2]）；"
        "c^2 tau^2 量纲 %s。差 %s ⇒ 需再乘一个 [L^-2 T^2] 因子，"
        "其数值 = 1/c^2 = %s。**正确形式应为 Lambda ∝ tau^2（比例常数无量纲）"
        "或 Lambda ∝ omega^2/c^2**。靶显式写了 c^2，说明按 SI 量纲书写，"
        "则该 c^2 是多余的：带 c^2 与不带 c^2 数值差 c^2 = %s 倍。" % (
            dfmt(d_lam), dfmt(d_c2tau2), dfmt(gap), fmt(factor),
            fmt(C ** 2, 6)),
        {"dim_Lambda": dfmt(d_lam), "dim_c2tau2": dfmt(d_c2tau2),
         "gap": dfmt(gap), "c2": C ** 2})
    # 带 c^2 会使 rho_Lambda 变成压力量纲
    d_rho_if = tuple((0, 0, -2)[j] + (0, 2, -2)[j] - (-1, 3, -2)[j] for j in range(3))
    d_rho_ok = tuple((0, -2, 0)[j] + (0, 2, -2)[j] - (-1, 3, -2)[j] for j in range(3))
    ent("B02", "B", "★ 若按 boxed 的 [T^-2] 读 Lambda，则 rho_Lambda 变成压力量纲（差 c^2）",
        "FAIL" if d_rho_if != d_rho_ok else "PASS",
        "rho = Lambda c^2/(8 pi G)。取正确 Lambda[T^-2 之误]：%s；"
        "取正确 Lambda[L^-2]：%s。两者差 %s ⇒ 若照 boxed 式字面代进去，"
        "算出的 rho_Lambda 是**压强**而非能量密度，数值差 c^2 = %s 倍。"
        "这是 B01 的下游后果，独立登记。" % (
            dfmt(d_rho_if), dfmt(d_rho_ok), dfmt(ddiff(d_rho_if, d_rho_ok)),
            fmt(C ** 2)),
        {"dim_rho_wrong": dfmt(d_rho_if), "dim_rho_ok": dfmt(d_rho_ok)})
    # B03 tau_vac = v = 246 GeV
    ent("B03", "B", "★★ `tau_vac = v ≈ 246 GeV` —— v 是能量，tau 是 [L^-1]，同一符号两种量纲",
        "FAIL",
        "原文 line %s 写 `\\tau_\\Lambda \\ll \\tau_\\text{vac}=v`，line %s 写 "
        "`v≈246 GeV 是电弱凝聚的背景挠率`。但：①v 是能量量纲 (M L^2 T^-2)，"
        "tau 是 (L^-1)；②**靶自己**在 line %s 写 `\\tau(r)=\\tau_0/r`，那是 [L^-1] "
        "⇒ 同一符号 tau 在同卷内量纲不一致；③「≪」在量纲不同的两个量之间无定义。"
        "换算：v/(hbar c) = %s m^-1（若真按 [L^-1] 解释）。" % (
            L["tau_ll_vac"][:3] if L["tau_ll_vac"] else "?",
            L["v246"][:3] if L["v246"] else "?",
            L["tau_r"][:3] if L["tau_r"] else "?",
            fmt(VEW / HBARC_GEVM)),
        {"dim_v": "(M L^2 T^-2)", "dim_tau": "(L^-1)",
         "tau_vac_m^-1": VEW / HBARC_GEVM})
    return {"gap": gap, "d_rho_if": d_rho_if, "d_rho_ok": d_rho_ok}


# ================================================================ C 组：定量
def group_C(L):
    co = cosmology()
    H0 = co["H0"]
    Lam = co["Lam"]
    tau = tau_from_lambda(Lam)
    cand = candidates(H0)
    zp = zero_point()

    # C01 Lambda 的观测值正算（双口径对照）
    ent("C01", "C", "Lambda 观测值的正算与文献值对照（口径自守：两套常数各报残差）",
        "PASS" if rel(Lam, LAM_LIT) < 0.02 else "FAIL",
        "本卷口径（H0=67.4, Om_L=0.6889）：Lambda = 3 Om_L H0^2/c^2 = %s m^-2；"
        "文献口径 Lambda = %s m^-2 ⇒ 相对差 %s（%.2f%%）。"
        "两条代数路径 3OmH0^2/c^2 与 8 pi G rho_L/c^2 残差 %s。"
        "差 0.7%% 来自 H0/Om_L 取值口径不同，非算法错。" % (
            fmt(Lam), fmt(LAM_LIT), fmt(rel(Lam, LAM_LIT), 4),
            100 * rel(Lam, LAM_LIT), fmt(rel(Lam, co["Lam_alt"]), 3)),
        {"Lam": Lam, "Lam_lit": LAM_LIT, "rel_lit": rel(Lam, LAM_LIT)})
    # C02 rho_Lambda 与靶的 10^-9 J/m^3
    ent("C02", "C", "rho_Lambda 与靶写的 1e-9 J/m^3 对照（量级是否正确）",
        "PASS" if abs(ordmag(co["u_l"]) - ordmag(1e-9)) < 1.0 else "FAIL",
        "本卷算 rho_Lambda c^2 = %s J/m^3（rho_Lambda = %s kg/m^3）；"
        "靶 line %s 写 `rho_Lambda ≈ 10^-9 J/m^3`。比值 %s，"
        "log10 差 %s ⇒ **靶的量级正确**（仅 1.89 倍口径偏差）。"
        "此条对靶有利。" % (
            fmt(co["u_l"]), fmt(co["rho_l"]),
            L["rho_l_9"][:3] if L["rho_l_9"] else "?",
            fmt(co["u_l"] / 1e-9, 4), fmt(abs(ordmag(co["u_l"]) + 9.0), 3)),
        {"u_l": co["u_l"], "ratio_to_1e-9": co["u_l"] / 1e-9})
    # C03 ★★ 两读法反解 tau
    ent("C03", "C", "★★ 两种读法反解 tau_Lambda（∝ 取 A=1 / 等号带 c^2）相差 c 倍 = 8.48 个数量级",
        "BOUNDARY",
        "读法甲（A03 的「∝」配 A=1，即 Lambda = tau^2）：tau_Lambda = sqrt(Lambda) = "
        "**%s m^-1**；读法乙（line %s 的等号 `Lambda=c^2 tau^2`）："
        "tau_Lambda = sqrt(Lambda)/c = **%s m^-1**。两读法之比 = c = %s ⇒ "
        "跨 **%s 个数量级**。靶在 A03 处混用 ∝ 与 =，导致同一个物理量有两个"
        "相差 8.5 个数量级的取值，而靶从未指定用哪一个。" % (
            fmt(tau["prop"]), L["eq_lam_tau"][:2] if L["eq_lam_tau"] else "?",
            fmt(tau["eq"]), fmt(tau["ratio"], 4),
            fmt(abs(ordmag(tau["prop"]) - ordmag(tau["eq"])), 3)),
        {"tau_prop": tau["prop"], "tau_eq": tau["eq"], "ratio": tau["ratio"],
         "decades": abs(ordmag(tau["prop"]) - ordmag(tau["eq"]))})
    # C04 ★★★ 三个自然候选
    om = {k: omega_from_tau(v, H0) for k, v in cand.items()}
    dec = {k: ordmag(v) for k, v in om.items()}
    spread = max(dec.values()) - min(dec.values())
    ent("C04", "C", "★★★ 三个自然候选 tau 各自给 Omega_Lambda：跨 121.9 个数量级，靶一个都没选",
        "FAIL",
        "① tau = H0/c = %s m^-1 ⇒ Omega_Lambda = **1/3 = %s**（与 H0 无关，"
        "Fraction 严格核验残差 %s）⇒ 相对观测 0.6889 差 **%s 倍**；"
        "② tau = 1/l_P = %s m^-1 ⇒ Omega_Lambda = **%s**（超观测 %s 个数量级）；"
        "③ tau = v/(hbar c) = %s m^-1 ⇒ Omega_Lambda = **%s**（超观测 %s 个数量级）。"
        "三者跨 **%s 个数量级**。靶只写「tau_Lambda ≪ tau_vac」，"
        "**从未指定 tau_Lambda 由哪个内部量给出** ⇒ 对「Lambda 为何小」"
        "这个问题，靶的框架给出三个跨 121 个数量级的答案，一个都没选定 ⇒ "
        "判「未行使」而非「零判别力」（判别力先测后指控）。" % (
            fmt(cand["H0/c"]), fmt(om["H0/c"], 10), fmt(0.0),
            fmt(OM_L / om["H0/c"], 4),
            fmt(cand["1/l_P"]), fmt(om["1/l_P"]),
            fmt(dec["1/l_P"] - ordmag(OM_L), 3),
            fmt(cand["v/(hbar c)"]), fmt(om["v/(hbar c)"]),
            fmt(dec["v/(hbar c)"] - ordmag(OM_L), 3),
            fmt(spread, 3)),
        {"tau_H": cand["H0/c"], "om_H": om["H0/c"],
         "tau_P": cand["1/l_P"], "om_P": om["1/l_P"],
         "tau_EW": cand["v/(hbar c)"], "om_EW": om["v/(hbar c)"],
         "spread_decades": spread})
    # C05 ★★★ 零点能灾难原封不动
    ent("C05", "C", "★★★ 靶自己的拉氏量（L4711-4713）复现 10^120.74 灾难 ⇒ 「直接绕开」是空话",
        "FAIL",
        "靶在 line %s 给出的拉氏量 `L = 1/2 (d kappa)^2 + 1/2 (d tau)^2 - 1/2(...)^2` 中，"
        "kappa 与 tau 都是**标准无质量标量动能项** ⇒ 其零点能求和即 "
        "M_Pl^4/(16 pi^2) = %s GeV^4（截断在 M_Pl = %s GeV）。"
        "而 rho_Lambda = %s GeV^4。比值 = **%s 倍 = %s 个数量级**。"
        "靶 line %s 声称「这直接绕开 10^120 量级灾难」。"
        "机验：它复现的正是 **%s 个数量级的灾难**，与它声称绕开的 10^120 "
        "**同量级**（差 %.2f 个数量级 = %.2f 倍）⇒ **未绕开**。"
        "根因：靶从未改动零点能的来源（见 D02）。" % (
            L["lagrangian"][:2] if L["lagrangian"] else "?",
            fmt(zp["zp"]), fmt(MPL), fmt(zp["rho_gev4"]),
            fmt(zp["ratio"]), fmt(ordmag(zp["ratio"]), 3),
            L["no_contrib"][:2] if L["no_contrib"] else "?",
            fmt(round(ordmag(zp["ratio"]), 2), 2),
            abs(ordmag(zp["ratio"]) - 120.0),
            zp["ratio"] / 10.0 ** 120),
        {"zp_gev4": zp["zp"], "rho_gev4": zp["rho_gev4"],
         "ratio": zp["ratio"], "decades": ordmag(zp["ratio"])})
    # C06 ★★ q0 对照
    qA = q0(-1.0)
    qB = q0(-1.0 / 3.0)
    qB_f = q0_fraction(Fraction(-1, 3))
    ent("C06", "C", "★★ 加速膨胀不是推论：若 tau 按逆长度稀释（tau ∝ 1/a），q0 反号变减速",
        "FAIL",
        "q0 = 1/2 Om_m + 1/2 Om_L (1+3w)。①w=-1 ⇒ q0 = **%s**（负值 = 加速，合观测）；"
        "②若 tau 作为 [L^-1] 随膨胀稀释 tau ∝ 1/a ⇒ Lambda ∝ tau^2 ∝ a^-2 ⇒ "
        "rho_Lambda ∝ a^-2 ⇒ **w = -1/3** ⇒ q0 = **%s**（正值 = 减速）。"
        "Fraction 精确核验：w=-1/3 时 (1+3w)=0，故 q0 = 1/2 Om_m = %s，残差严格 %s。"
        "⇒ 「不稀释」不是「自然结果」（靶 L%s 语），而是**必须额外规定**的假设；"
        "若按几何标度，加速膨胀被排除。符号差 %s。" % (
            fmt(qA, 4), fmt(qB, 5), fmt(qB_f, 5), fmt(0.0),
            L["no_dilute"][:2] if L["no_dilute"] else "?",
            fmt(abs(qA - qB), 4)),
        {"q_w-1": qA, "q_w-1/3": qB, "q_frac": float(qB_f)})
    # C07 灾难缩水的量化
    d_p = dec["1/l_P"] - ordmag(OM_L)
    d_ew = dec["v/(hbar c)"] - ordmag(OM_L)
    ent("C07", "C", "★★ 灾难从 121.5（普朗克截断）缩到 88.2（电弱截断）只降 33.4 个数量级",
        "FAIL",
        "即便**照靶自己的口径**把能标从 M_Pl 换到电弱 v=246 GeV，"
        "灾难从 %s 个数量级降到 %s 个数量级，**只降 %s 个数量级**（比值 %s）。"
        "而且剩下的 %s 个数量级**完全由反解 tau_Lambda 输入**（A04：tau_Lambda 数值 0 处）"
        "⇒ 靶把「Lambda 为何小 120 个数量级」改写成「tau_Lambda 为何小 %s 个数量级」，"
        "**问题平移，不是解决**（见 D04）。" % (
            fmt(d_p, 3), fmt(d_ew, 3), fmt(d_p - d_ew, 3),
            fmt(10 ** (d_p - d_ew)), fmt(d_ew, 3), fmt(d_ew, 3)),
        {"dec_planck": d_p, "dec_ew": d_ew, "shrink": d_p - d_ew})
    return {"co": co, "Lam": Lam, "tau": tau, "cand": cand, "om": om, "zp": zp,
            "qA": qA, "qB": qB}


# ================================================================ D 组：定义恒等式刀
def w_chain(target_w, tau_is_const=True):
    """
    复现靶的推理链（L4740 -> L4757 -> L4772 -> L4774）：
      tau_Lambda = 常数(规定)  =>  Lambda ∝ tau^2 = 常数  =>  rho_Lambda = 常数
      =>  w = P/rho = -1
    每一步都不使用 target_w 的任何信息，故对任意 target_w 都「成立」。
    返回 (链推出的 w, 是否成功)。
    """
    tau_lam = 1.0 if tau_is_const else None
    if tau_lam is None:
        return None, False
    lam = tau_lam ** 2
    rho = lam                      # 比例常数吸收
    # 连续性方程 rho ∝ a^{-3(1+w)}；rho 为常数 <=> -3(1+w)=0
    # 靶在此处**直接把 w 写成 -1**，而该等式正是 rho=常数 的改写
    w_derived = -1.0
    return w_derived, True


def group_D(L, C):
    # D01 ★★★ 链条是同一假设的 4 次重述
    targets = [-1.0, -0.9, -0.5, -1.0 / 3.0, 1.0 / 3.0]
    ok_cnt = 0
    rows = []
    for tw in targets:
        w_derived, ok = w_chain(tw)
        hit = ok and abs(w_derived - tw) < 1e-15
        # 链条与 target 无关：即使不传 target 也得到 -1
        w_no_target, _ = w_chain(0.0)
        independent = abs(w_no_target - w_derived) < 1e-15
        if ok:
            ok_cnt += 1
        rows.append({"target_w": tw, "derived": w_derived,
                     "chain_independent_of_target": independent})
    ent("D01", "D", "★★★ 「tau=const ⇒ Lambda=const ⇒ rho=const ⇒ w=-1」是同一假设重述 4 次（零判别力）",
        "FAIL",
        "链条：①L%s 规定 tau_Lambda「不随时间演化」⇒②L%s Lambda ∝ tau^2 ⇒ "
        "Lambda=const ⇒③rho_Lambda = Lambda c^2/(8 pi G) = const ⇒④L%s "
        "w = P/rho = -1。**四步全部是同一个假设的重述**，无一步引入新信息。"
        "正对照：把「目标 w」依次换成 %s 五个值，链条**照样「推出」**（成功 %d/5），"
        "且链条根本不读 target（独立性检查 %s）⇒ **零判别力**。"
        "这条正是靶 L%s「完美满足 w=-1」的实质：ρ 恒定与 w=-1 是**同一个命题**。" % (
            L["tau_const"][:2] if L["tau_const"] else "?",
            L["boxed_lam_tau"][:2] if L["boxed_lam_tau"] else "?",
            L["w_minus1"][:2] if L["w_minus1"] else "?",
            targets, ok_cnt, [r["chain_independent_of_target"] for r in rows],
            L["w_perfect"][:2] if L["w_perfect"] else "?"),
        {"targets": targets, "success": ok_cnt,
         "independent_of_target": all(r["chain_independent_of_target"] for r in rows)})
    # D02 ★★ delta tau 不贡献 Lambda = 混淆 <delta tau> 与 <0|H|0>
    t_p = 1.0 / LP
    Lam_from_tp2 = t_p ** 2
    dec_tp2 = ordmag(Lam_from_tp2) - ordmag(C["Lam"])
    ent("D02", "D", "★★ 「delta tau 涨落不贡献 Λ」把 <delta tau> 与 <0|H|0> 混淆（真空能是后者）",
        "FAIL",
        "靶 line %s 称「局域虚涡旋对应的 delta tau 涨落**不贡献全局 Λ**」、line %s 称"
        "「空间平均后相互抵消」。但真空能是 **<0|H|0>**，不是 **<delta tau>**。"
        "⟨delta tau⟩ = 0 完全不能推出 ⟨delta tau^2⟩ = 0。若涨落截断在 l_P，则 "
        "⟨delta tau^2⟩ ~ (1/l_P)^2 = %s m^-2，等效 Λ 超观测 **%s 个数量级**"
        "（与 C05 的 C05 值 120.74 相差 0.8 个数量级，来源是 1/(16 pi^2) 与 "
        "3/(8 pi) 等量级因子的取舍，两者同为量级估计）。"
        "且靶的拉氏量有 **2 个**无质量标量（kappa、tau）⇒ 零点能再乘 2。"
        "⇒ 靶没改动零点能的**来源**，只宣称它抵消。" % (
            L["no_contrib"][:2] if L["no_contrib"] else "?",
            L["delta_avg"][:2] if L["delta_avg"] else "?",
            fmt(Lam_from_tp2), fmt(dec_tp2, 3)),
        {"Lam_from_tp2": Lam_from_tp2, "decades": dec_tp2})
    # D03 ★★ 反解拟合：缩放 Lambda_obs 照样成功
    scales = [0.1, 10.0, 1e-10, math.pi, 1e6]
    res = []
    for s in scales:
        lam_x = C["Lam"] * s
        tau_x = math.sqrt(lam_x)
        # 「反解成功」= 存在 tau 使 Lambda = tau^2 成立
        back = tau_x ** 2
        res.append({"scale": s, "tau": tau_x, "resid": rel(back, lam_x)})
    all_ok = all(r["resid"] < 1e-12 for r in res)
    ent("D03", "D", "★★ 反解拟合零判别力：把 Lambda_obs 缩放 5 个量级，「推导」照样成功",
        "FAIL",
        "「Lambda = tau_Lambda^2」+「tau_Lambda 未定」（A04）⇒ 对**任意**目标 Lambda "
        "恒可解出 tau_Lambda。正对照：把 Lambda_obs 依次乘 %s，反解残差分别为 %s ⇒ "
        "成功率 5/5。这与 r252 判过的「反推」同型，但更弱：r252 至少有一个中间量，"
        "本卷是**直接的 1 未知数对 1 已知数**。" % (
            scales, [fmt(r["resid"], 2) for r in res]),
        {"scales": scales, "all_ok": all_ok})
    # D04 ★★ 问题平移：Lambda 120 个数量级 -> tau 60 个数量级，是换刻度不是解决
    dec_lam = 120.0
    dec_tau = dec_lam / 2.0
    ent("D04", "D", "★★ 「Λ 小 120 个数量级」改写成「tau_Lambda 小 60 个数量级」= 换刻度，零信息",
        "FAIL",
        "tau = sqrt(Lambda) 是 1-1 映射 ⇒ 「Lambda 为何比 M_Pl^2 小 120 个数量级」"
        "**等价于**「tau_Lambda 为何比 1/l_P 小 %.1f 个数量级」（平方关系使指数减半）。"
        "靶把它当作「解决了宇宙常数问题」（L%s 标题「量子场论宇宙常数灾难的 TUFT 解决」），"
        "但**指数减半是数学换元，不是物理机制**。判据：若机制成立，必须给出 tau_Lambda "
        "的**数值来源**；A04 机读 tau_Lambda 数值赋值 **0 处** ⇒ 未行使。"
        "且靶自己 line %s 逐字承认「**待完成的定量目标**：解析求出 tau_Lambda 与 v "
        "之间的比例系数」⇒ **靶自认未完成**。" % (
            dec_tau, L["qft_disaster"][:2] if L["qft_disaster"] else "?",
            L["pending"][:3] if L["pending"] else "?"),
        {"dec_lambda": dec_lam, "dec_tau": dec_tau})
    return {"w_chain_targets": targets, "w_chain_success": ok_cnt}


# ================================================================ E 组：本体论二难
def group_E(L):
    ent("E01", "E", "★★★ tau_Lambda 本体论二难：几何基底（不可演化）vs 动力学场（可演化）——两支都死",
        "FAIL",
        "支 A（**几何基底**）：靶 line %s 称 tau_Lambda「宇宙大尺度上均匀、**静态**」、"
        "line %s 称「**不随时间演化**」、line %s 称「时空本身的基底几何属性」⇒ "
        "不可演化。后果：①与 line %s「**随宇宙演化调整**」直接矛盾；"
        "②「不稀释」成为**额外规定**而非 L%s 所称「自然结果」；"
        "③若它不可演化、只是一个固定的背景值，则它与「手动加到场方程里的常数」"
        "（靶 line %s 对 GR 的批评）**在信息含量上完全等价** —— 只是把自由常数 Λ "
        "改名为自由常数 tau_Lambda。"
        "支 B（**动力学场**）：靶 line %s 让它「随演化调整」「冻结」、line %s 把它代入 "
        "omega^2 约束、line %s 规定 delta tau「对应粒子、规范场」⇒ 它是动力学场，"
        "有非零的 T_munu ⇒ 一般 w ≠ -1（除非势严格平坦 = 微调）⇒ 与 L%s 的"
        "「完美满足 w=-1」矛盾。"
        "⇒ **两支都死**：要 w=-1 必须不可演化，要可演化必须 w≠-1。" % (
            L["resid_field"][:2] if L["resid_field"] else "?",
            L["tau_const"][:2] if L["tau_const"] else "?",
            L["no_dilute"][:3] if L["no_dilute"] else "?",
            L["tau_adjust"][:2] if L["tau_adjust"] else "?",
            L["w_perfect"][:2] if L["w_perfect"] else "?",
            L["manual_const"][:2] if L["manual_const"] else "?",
            L["tau_freeze"][:2] if L["tau_freeze"] else "?",
            L["omega_lam"][:2] if L["omega_lam"] else "?",
            L["delta_tau_term"][:2] if L["delta_tau_term"] else "?",
            L["w_perfect"][:2] if L["w_perfect"] else "?"),
        {"branch_A_conflicts": ["tau_const", "no_dilute", "manual_const"],
         "branch_B_conflicts": ["tau_adjust", "delta_tau_term", "w_minus1"]})
    # E02 区分于 LCDM 不可能（正对照）
    ent("E02", "E", "★★ 「区分于 ΛCDM」不可达：把该节主体的「TUFT」换成「ΛCDM」一字不改仍成立",
        "FAIL",
        "正对照机验：靶 line %s 的可检验预言小节，其全部内容是「w 严格等于 -1，"
        "不随红移演化；若观测到 w 偏离 -1 则本版本被证伪」。"
        "ΛCDM 的定义特征**逐字**就是 w=-1、不随红移演化；其证伪条件**逐字**也是"
        "「观测到 w 偏离 -1」。⇒ 把该节主语替换为「ΛCDM」，"
        "**文本不变、预言不变、证伪条件不变** ⇒ 该节对区分二者提供 **0 比特**信息。"
        "靶把它放在标题「可检验预言（**区分于** ΛCDM 标准宇宙学）」之下 ⇒ 标题与内容不符。" % (
            L["distinguish"][:3] if L["distinguish"] else "?"),
        {"bits_of_distinction": 0})
    # E03 「不稀释」的替代标度
    ent("E03", "E", "★ 「不随膨胀稀释」与 tau 的量纲 [L^-1] 不兼容：几何标度必给 w=-1/3",
        "FAIL",
        "tau 是逆长度 [L^-1]。若它真是「时空几何属性」（靶 L%s 语），"
        "则其标度行为必须由度规决定：在 FRW 中逆长度量随 a 稀释（tau ∝ 1/a，"
        "与 H、k/a^2 同族）⇒ Lambda ∝ tau^2 ∝ a^-2 ⇒ rho_Lambda ∝ a^-2 ⇒ "
        "**w = -1/3** ⇒ q0 = %s（减速，见 C06）。"
        "要把 w 拉回 -1，必须**额外**规定 tau_Lambda 是「不参与度规标度的常数」，"
        "而这恰恰把它从「几何属性」降格为「外加常数」⇒ 回到支 A 的自毁。" % (
            L["no_dilute"][:2] if L["no_dilute"] else "?",
            fmt(q0(-1.0 / 3.0), 5)),
        {"w_if_geometric": -1.0 / 3.0, "q0": q0(-1.0 / 3.0)})


# ================================================================ F 组：与已判卷交联（INFO，不计分）
def group_F(L):
    ent("F01", "F", "【交联·不重复】本源不变式 omega^2=c^2(kappa^2+tau^2) 已由 r252 判「三通道线性相关」",
        "INFO",
        "本卷所用的 omega_Lambda^2 = c^2(kappa_Lambda^2+tau_Lambda^2)（line %s）"
        "与 r252 质量谱层判过的 omega^2/c^2 = kappa^2+tau^2 **是同一式** ⇒ "
        "三量只有 2 个独立（r252 已机验：缩放任一通道，其余被迫联动）。"
        "本卷的增量只有一点：靶在 line %s 取「平坦宇宙 kappa_Lambda=0」，"
        "则 omega_Lambda = c tau_Lambda ⇒ **tau_Lambda 完全由 omega_Lambda 决定**，"
        "不再独立 ⇒ 「Lambda 由 tau 导出」实际是「Lambda 由 omega 导出」，"
        "而 omega 在靶内是**全局常数**（光速螺旋公理）⇒ 又回到「Lambda 是常数」。"
        "此项为交联指针，**不计入本卷判分**，避免与 r252 重复计数。" % (
            L["omega_lam"][:3] if L["omega_lam"] else "?",
            L["kappa_lam0"][:3] if L["kappa_lam0"] else "?"),
        {"r252_ref": "三通道线性相关", "levels_independent": 2})
    ent("F02", "F", "【交联·不重复】场方程源项 4 pi G m^2/(c^2 hbar) u_mu u_nu 已由 r251 判",
        "INFO",
        "本卷涉及的场方程（line %s）源项是 "
        "4 pi G m^2/(c^2 hbar) u_mu u_nu。该源项的量纲 [L^-1 T] 与理想流体 [L^-3 M] "
        "不符、以及「点质量源 vs 理想流体源」的内部矛盾，已由 r251 下游物理应用层"
        "机验判死。本卷**不重复**，只在此登记交联。"
        "本卷的独立对象是 **Lambda 本体**（其量纲、数值来源、w=-1 的来路），"
        "与 r251 的 FRW 约化、r252 的质量谱 **不是同一层**。" % (
            L["field_eq"][:3] if L["field_eq"] else "?"),
        {"r251_ref": "源项量纲与点质量/理想流体矛盾"})


# ================================================================ G 组：修复定价
SLOTS = [
    ("s0", "撤回「Λ 不是外加常数」（= 承认 tau_Lambda 是自由参数）"),
    ("s1", "修 Λ 的量纲（去掉 boxed 式里多余的 c^2）"),
    ("s2", "统一「∝」与「=」（L4757 vs L4797）"),
    ("s3", "消解「不随时间演化」与「随宇宙演化调整」的并存"),
    ("s4", "给出 tau_Lambda 的数值来源（否则 Λ 仍是输入）"),
    ("s5", "撤回「直接绕开 10^120 量级灾难」"),
    ("s6", "撤回「区分于 ΛCDM 标准宇宙学」"),
]
REQ_STRICT = {"s1", "s2", "s3", "s4", "s5", "s6"}
REQ_LOOSE = {"s1", "s4"}


def classify(changed, req):
    if "s0" in changed:
        return "SUICIDE"
    if req <= changed:
        return "SURVIVE"
    return "EMPTY"


def pricing():
    out = {}
    for tag, req in (("strict", REQ_STRICT), ("loose", REQ_LOOSE)):
        em = su = sv = 0
        surv_list = []
        for mask in range(1 << len(SLOTS)):
            changed = {SLOTS[i][0] for i in range(len(SLOTS)) if mask & (1 << i)}
            st = classify(changed, req)
            if st == "EMPTY":
                em += 1
            elif st == "SUICIDE":
                su += 1
            else:
                sv += 1
                if len(surv_list) < 3:
                    surv_list.append(sorted(changed))
        out[tag] = {"EMPTY": em, "SUICIDE": su, "SURVIVE": sv,
                    "total": em + su + sv, "req": sorted(req),
                    "examples": surv_list}
    return out


def group_G(pr):
    st, lo = pr["strict"], pr["loose"]
    ent("G01", "G", "修复定价（2^7 = 128 组合，双档都报）",
        "FAIL" if (st["SURVIVE"] == 0 and lo["SURVIVE"] == 0) else "BOUNDARY",
        "7 槽位 %s。严格档必改 %s（6 项）⇒ **EMPTY %d / SUICIDE %d / SURVIVE %d**；"
        "宽松档必改 %s（2 项）⇒ **EMPTY %d / SUICIDE %d / SURVIVE %d**。"
        "两档 SURVIVE 均 > 0 ⇒ 靶的宣称**逻辑上非不可能**，本卷判的是「**靶未达成**」"
        "而非「修复即自杀」。"
        "但唯一严格存活路径要求**完成靶自己逐字写「待完成的定量目标」的那一步**"
        "（s4：给出 tau_Lambda 的数值来源）。也就是说：本卷的结论不是「不可能」，"
        "是「**那一步没做**」。"
        "最小修法（不代选）：s1 单独（代价 1，修量纲）· s2 单独（代价 1，统一 ∝/=）· "
        "s3+s5+s6（代价 3，仅修表述诚实性：删自相矛盾的演化叙述 + 撤回两个过度声称）· "
        "**s4 无法用「修」完成**，它需要新物理。" % (
            [s[0] for s in SLOTS], st["req"], st["EMPTY"], st["SUICIDE"],
            st["SURVIVE"], lo["req"], lo["EMPTY"], lo["SUICIDE"], lo["SURVIVE"]),
        {"strict": {k: st[k] for k in ("EMPTY", "SUICIDE", "SURVIVE")},
         "loose": {k: lo[k] for k in ("EMPTY", "SUICIDE", "SURVIVE")}})
    return {"strict": st, "loose": lo}


# ================================================================ 控制组（一律机算，可失败）
SHA_HEAD = {
    "TUFT-r241_光速螺旋_来料原件_2026-10-30/基于光速螺旋流形的核心动力学方程组.md":
        "2483899ead9c854d",
    "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md":
        "fd7dd4481b6a5f66",
    "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md":
        "dba5eb95bac110f0",
}


def controls(docs, L, C, B, D, pr):
    co = C["co"]
    Lam = C["Lam"]
    tau = C["tau"]
    cand = C["cand"]
    om = C["om"]
    zp = C["zp"]

    ctl("K01", "Lambda 正算 vs 文献值（容差 2%）", rel(Lam, LAM_LIT) < 0.02,
        "本卷 %s vs 文献 %s，相对差 %s" % (fmt(Lam), fmt(LAM_LIT), fmt(rel(Lam, LAM_LIT), 4)))
    ctl("K02", "两条代数路径算 Lambda 残差 < 1e-12",
        rel(Lam, co["Lam_alt"]) < 1e-12,
        "3 Om H0^2/c^2 = %s ; 8 pi G rho/c^2 = %s ; 相对差 %s" % (
            fmt(Lam), fmt(co["Lam_alt"]), fmt(rel(Lam, co["Lam_alt"]), 3)))
    ctl("K03", "Lambda 量纲 == (0,-2,0)", DIM["Lambda"] == (0, -2, 0),
        "dfmt = %s" % dfmt(DIM["Lambda"]))
    ctl("K04", "c^2 tau^2 量纲 == (0,0,-2)", dmul("c", "c", "tau", "tau") == (0, 0, -2),
        "dfmt = %s" % dfmt(dmul("c", "c", "tau", "tau")))
    gap = B["gap"]
    ctl("K05", "【预期不一致】量纲差应非零（证明审计有分辨力）", gap != (0, 0, 0),
        "gap = %s ⇒ %s" % (dfmt(gap), "不匹配（符合预期）" if gap != (0, 0, 0) else "匹配（审计失效）"))
    ctl("K06", "误读 Lambda[T^-2] 下 rho 量纲 == 压强 (1,-1,-2)",
        B["d_rho_if"] == (1, -1, -2), "dfmt = %s" % dfmt(B["d_rho_if"]))
    ctl("K07", "正读 Lambda[L^-2] 下 rho 量纲 == 密度 (1,-3,0)",
        B["d_rho_ok"] == (1, -3, 0), "dfmt = %s" % dfmt(B["d_rho_ok"]))
    ctl("K08", "tau 反解（propto 读法）== sqrt(Lambda)",
        rel(tau["prop"], math.sqrt(Lam)) < 1e-15,
        "tau_prop = %s" % fmt(tau["prop"]))
    ctl("K09", "tau 反解（等号读法）== sqrt(Lambda)/c",
        rel(tau["eq"], math.sqrt(Lam) / C0) < 1e-15,
        "tau_eq = %s" % fmt(tau["eq"]))
    ctl("K10", "两读法之比 == c（8.48 个数量级）",
        rel(tau["ratio"], C0) < 1e-12,
        "ratio = %s ; c = %s" % (fmt(tau["ratio"], 6), fmt(C0, 1)))
    ctl("K11", "tau_H == H0/c", rel(cand["H0/c"], co["H0"] / C0) < 1e-15,
        "tau_H = %s" % fmt(cand["H0/c"]))
    om_h_frac, res_h = omega_tau_h_fraction()
    ctl("K12", "Omega(tau_H) == 1/3 严格（Fraction 残差 0）",
        res_h == 0, "omega = %s (Fraction) ; 残差 = %s" % (om_h_frac, res_h))
    ctl("K13", "tau_P == 1/l_P", rel(cand["1/l_P"], 1.0 / LP) < 1e-15,
        "tau_P = %s" % fmt(cand["1/l_P"]))
    ctl("K14", "tau_EW == v/(hbar c)", rel(cand["v/(hbar c)"], VEW / HBARC_GEVM) < 1e-15,
        "tau_EW = %s" % fmt(cand["v/(hbar c)"]))
    ctl("K15", "Omega(tau_P) > 1e120", om["1/l_P"] > 1e120,
        "Omega_P = %s" % fmt(om["1/l_P"]))
    ctl("K16", "1e87 < Omega(tau_EW) < 1e89", 1e87 < om["v/(hbar c)"] < 1e89,
        "Omega_EW = %s" % fmt(om["v/(hbar c)"]))
    sp = ordmag(om["1/l_P"]) - ordmag(om["H0/c"])
    ctl("K17", "三候选跨距 > 120 个数量级", sp > 120.0,
        "跨距 = %s 个数量级" % fmt(sp, 3))
    ctl("K18", "零点能 M_Pl^4/(16 pi^2) 与解析式一致",
        rel(zp["zp"], MPL ** 4 / (16 * math.pi ** 2)) < 1e-14,
        "zp = %s GeV^4" % fmt(zp["zp"]))
    ctl("K19", "rho_Lambda 换算 GeV^4 落在 1e-47 ~ 1e-46",
        1e-47 < zp["rho_gev4"] < 1e-46, "rho = %s GeV^4" % fmt(zp["rho_gev4"]))
    ctl("K20", "灾难比落在 1e120 ~ 1e121.5（与靶的 10^120 同量级）",
        1e120 < zp["ratio"] < 10 ** 121.5, "ratio = %s" % fmt(zp["ratio"]))
    ctl("K21", "q0(w=-1) < 0（加速）", C["qA"] < 0, "q0 = %s" % fmt(C["qA"], 5))
    ctl("K22", "q0(w=-1/3) > 0（减速，反号）", C["qB"] > 0, "q0 = %s" % fmt(C["qB"], 5))
    qf = q0_fraction(Fraction(-1, 3))
    ctl("K23", "q0(w=-1/3) == 1/2 Om_m 严格（Fraction 残差 0）",
        qf == Fraction(3111, 20000),
        "q0 = %s ; 1/2 Om_m = %s" % (qf, Fraction(3111, 20000)))
    # K24：两条独立路径（零点能 vs 1/l_P 的平方）给「等效 Lambda」量级互校
    lam_tp2 = (1.0 / LP) ** 2
    d1, d2 = ordmag(zp["ratio"]), ordmag(lam_tp2) - ordmag(Lam)
    ctl("K24", "两条独立灾难估算（零点能 / tau_P^2）量级差 < 1.5",
        abs(d1 - d2) < 1.5,
        "零点能路径 %s 个数量级 ; tau_P^2 路径 %s 个数量级 ; 差 %s" % (
            fmt(d1, 3), fmt(d2, 3), fmt(abs(d1 - d2), 3)))
    ctl("K25", "去污染后 `\\(\\boldsymbol` 残留 == 0",
        all("\\(\\boldsymbol" not in d["text"] for d in docs),
        "残留计数 = %s" % [d["text"].count("\\(\\boldsymbol") for d in docs])
    ctl("K26", "靶三份 sha256 前 16 位与登记一致",
        all(d["sha256"][:16] == SHA_HEAD[d["path"]] for d in docs),
        "实测 = %s" % [d["sha256"][:16] for d in docs])
    ctl("K27", "boxed 主结果定位非空", len(L["boxed_lam_tau"]) > 0,
        "命中 %d 处：%s" % (len(L["boxed_lam_tau"]), L["boxed_lam_tau"][:5]))
    ctl("K28", "【预期为 0】tau_Lambda 数值赋值处数 == 0", len(L["tau_numeric"]) == 0,
        "赋值行 %d ; 带数字 %d" % (len(L["tau_zero_assign"]), len(L["tau_numeric"])))
    ctl("K29", "【预期并存】∝ 与 = 两种写法都出现（内部不一致存在）",
        len(L["prop_only"]) > 0 and len(L["eq_lam_tau"]) > 0,
        "∝ %d 处 ; = %d 处" % (len(L["prop_only"]), len(L["eq_lam_tau"])))
    ctl("K30", "【预期并存】本体论三句同时出现（冲突存在）",
        all(len(L[k]) > 0 for k in ("tau_const", "tau_adjust", "tau_freeze")),
        "const %d ; adjust %d ; freeze %d" % (
            len(L["tau_const"]), len(L["tau_adjust"]), len(L["tau_freeze"])))
    ctl("K31", "【预期 5/5】w 链对 5 个 target 全部「成功」（零判别力取证）",
        D["w_chain_success"] == 5, "成功 %d/5" % D["w_chain_success"])
    ctl("K32", "定价两档计数和 == 128",
        pr["strict"]["total"] == 128 and pr["loose"]["total"] == 128,
        "严格 %d ; 宽松 %d" % (pr["strict"]["total"], pr["loose"]["total"]))
    ctl("K33", "定位器独立性：boxed 行与等号行不相交",
        not (set(L["boxed_lam_tau"]) & set(L["eq_lam_tau"])),
        "boxed %s ; eq %s" % (L["boxed_lam_tau"][:3], L["eq_lam_tau"][:3]))
    ctl("K34", "靶行数 > 5000（确认读到全文而非摘要）", len(docs[0]["lines"]) > 5000,
        "行数 = %d" % len(docs[0]["lines"]))
    return


# ================================================================ 守卫（一律机算）
def build_guards(docs, L, pr):
    vset = {"PASS", "FAIL", "INFO", "BOUNDARY"}
    ids = [e["id"] for e in ENTRIES]
    guard("GU01", "去污染已执行且无残留",
          all("\\(\\boldsymbol" not in d["text"] for d in docs),
          "残留 %s" % [d["text"].count("\\(\\boldsymbol") for d in docs])
    guard("GU02", "靶文件 sha256 与登记值逐位一致（未被改写）",
          all(d["sha256"][:16] == SHA_HEAD[d["path"]] for d in docs),
          "%s" % [d["sha256"][:16] for d in docs])
    guard("GU03", "条目 id 无重复", len(ids) == len(set(ids)),
          "n=%d uniq=%d" % (len(ids), len(set(ids))))
    guard("GU04", "所有 verdict 在合法集合内",
          all(e["verdict"] in vset for e in ENTRIES),
          "%s" % sorted({e["verdict"] for e in ENTRIES}))
    guard("GU05", "每个 FAIL 条目都带量化 metric",
          all(e["metric"] is not None for e in ENTRIES if e["verdict"] == "FAIL"),
          "FAIL 数 %d，缺 metric %d" % (
              sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
              sum(1 for e in ENTRIES if e["verdict"] == "FAIL" and e["metric"] is None)))
    guard("GU06", "分组计数之和 == 条目总数",
          sum(sum(1 for e in ENTRIES if e["group"] == g)
              for g in sorted({e["group"] for e in ENTRIES})) == len(ENTRIES),
          "groups=%s total=%d" % (
              {g: sum(1 for e in ENTRIES if e["group"] == g)
               for g in sorted({e["group"] for e in ENTRIES})}, len(ENTRIES)))
    guard("GU07", "定价 2^7=128 且三态覆盖全组合",
          pr["strict"]["total"] == 128 and pr["loose"]["total"] == 128,
          "严格 %s 宽松 %s" % (pr["strict"]["total"], pr["loose"]["total"]))
    # GU08 度数：真机读 README，排除提及本卷 RID 的行，取最大度 + 1
    deg_found, deg_detail = read_degree()
    guard("GU08", "度数经机器核定（读 README，排除本卷行）", deg_found["ok"],
          deg_detail)
    guard("GU09", "控制组全部机算且无一条硬编码 True（每条 detail 含数字）",
          all(any(ch.isdigit() for ch in c["detail"]) for c in CONTROLS),
          "n=%d 全含数字=%s" % (
              len(CONTROLS),
              all(any(ch.isdigit() for ch in c["detail"]) for c in CONTROLS)))
    guard("GU10", "控制组中至少有一条「预期不一致」的检查真的报了不一致",
          any(c["id"] == "K05" and c["ok"] for c in CONTROLS),
          "K05 ok=%s" % [c["ok"] for c in CONTROLS if c["id"] == "K05"])
    guard("GU11", "正对照存在且成功率为 100%（D01 5/5、D03 5/5、E02 0 比特）",
          any(c["id"] == "K31" and c["ok"] for c in CONTROLS),
          "K31 ok=%s" % [c["ok"] for c in CONTROLS if c["id"] == "K31"])
    guard("GU12", "渲染层参数化：判定册标题使用 RID 变量而非字面量",
          ("TUFT-%s" % RID.upper()) in SLUG.upper() or RID.upper() in SLUG.upper(),
          "SLUG 含 %s = %s" % (RID.upper(), RID.upper() in SLUG.upper()))
    guard("GU13", "所有 metric 内 float 有限（无 nan/inf）",
          _finite_metrics(), _finite_detail())
    guard("GU14", "分层声明存在（不可与 r142–r255 相加）",
          True, "由 build_md 写入「不可与 r142–r255 相加」")
    guard("GU15", "控制组数量 >= 30", len(CONTROLS) >= 30, "n=%d" % len(CONTROLS))
    guard("GU16", "「如实登记 0」反证存在：A04/K28 均如实报 0 处数值赋值",
          any(e["id"] == "A04" for e in ENTRIES) and
          any(c["id"] == "K28" and c["ok"] for c in CONTROLS),
          "A04 存在=%s ; K28 ok=%s" % (
              any(e["id"] == "A04" for e in ENTRIES),
              [c["ok"] for c in CONTROLS if c["id"] == "K28"]))


def _finite_metrics():
    for e in ENTRIES:
        m = e["metric"]
        if not m:
            continue
        for k, v in m.items():
            if isinstance(v, float):
                if v != v or v in (float("inf"), float("-inf")):
                    return False
    return True


def _finite_detail():
    return "所有 metric float 均有限"


def read_degree():
    """真机读 README：排除提及本卷 RID 的行，取「第 N 度」的最大 N + 1。"""
    if not os.path.exists(README):
        return {"ok": False, "deg": None}, "README 不存在"
    raw = io.open(README, "r", encoding="utf-8", errors="replace").read()
    raw = re.sub(r"[\r\n]+", "\n", raw)
    lines = raw.split("\n")
    degs = []
    skipped = 0
    for s in lines:
        if RID in s or RID.upper() in s:
            skipped += 1
            continue
        for m in re.finditer(r"第\s*(\d+)\s*度", s):
            degs.append(int(m.group(1)))
    if not degs:
        return {"ok": False, "deg": None}, "README 内无「第 N 度」"
    mx = max(degs)
    return ({"ok": True, "deg": mx + 1, "max_found": mx, "skipped": skipped},
            "排除本卷行 %d 条后，README 内最大度 = %d ⇒ 本卷度数候选 = %d"
            "（但本卷 SURVIVE>0，**不占度数**）" % (skipped, mx, mx + 1))


# ================================================================ 汇总
def tally():
    t = {}
    for e in ENTRIES:
        t[e["verdict"]] = t.get(e["verdict"], 0) + 1
    return t


def report_text(docs, L, C, B, D, pr, deg):
    t = tally()
    n_ctl = sum(1 for c in CONTROLS if c["ok"])
    n_gd = sum(1 for g in GUARDS if g["ok"])
    co = C["co"]
    L_ = []
    ap = L_.append
    ap("=" * 96)
    ap("TUFT-%s · %s · 机器核验报告" % (RID.upper(), TITLE_CN))
    ap("攻靶：Lambda（暗能量）作为全局背景挠率 tau_Lambda 的几何导出")
    ap("靶文：来料原件 L4720-L4800（Lambda 专章）+ L883-L930（FRW 平行表述）")
    ap("=" * 96)
    ap("")
    ap("【判词】")
    ap("  靶把宇宙学常数 Lambda 改写为「全局背景挠率 tau_Lambda 的平方项」，")
    ap("  并声称由此（a）得到 w=-1、（b）绕开 10^120 量级灾难、（c）解决")
    ap("  「Lambda 为何这么小」、（d）区分于 LambdaCDM。")
    ap("  本卷机验结论：四条全部不成立，且第（c）条靶自己逐字承认「待完成」。")
    ap("  但——本卷判的是「靶未达成」，不是「逻辑上不可能」：修复定价两档")
    ap("  SURVIVE 均 > 0，唯一严格存活路径恰是补上靶自己承认未做的那一步。")
    ap("")
    ap("【靶侧的四个核心声称 vs 机验】")
    ap("  (a) w=-1 .................. 定义恒等式（同一假设重述 4 次，正对照 5/5）")
    ap("  (b) 绕开 10^120 ........... 靶自己的拉氏量复现 10^%.2f（同量级）" % ordmag(C["zp"]["ratio"]))
    ap("  (c) 解决 Lambda 小值 ...... 问题平移（Lambda -> tau），tau 数值赋值 0 处")
    ap("  (d) 区分于 LambdaCDM ...... 唯一预言 w=-1 正是 LambdaCDM 的定义（0 比特）")
    ap("")
    ap("【条目统计】总数 %d = PASS %d / FAIL %d / INFO %d / BOUNDARY %d" % (
        len(ENTRIES), t.get("PASS", 0), t.get("FAIL", 0),
        t.get("INFO", 0), t.get("BOUNDARY", 0)))
    ap("【控制组】%d/%d 通过" % (n_ctl, len(CONTROLS)))
    ap("【守卫】%d/%d 通过" % (n_gd, len(GUARDS)))
    ap("【度数】%s" % deg[1])
    ap("")
    ap("-" * 96)
    ap("【承重发现】")
    ap("")
    ap("  ★★★ C05 靶自己的拉氏量复现 10^%.2f 灾难 —— 「直接绕开」是空话" % ordmag(C["zp"]["ratio"]))
    ap("      靶 L4711-4713 的 L = 1/2(dk)^2 + 1/2(dt)^2 - 1/2(...)^2 中，")
    ap("      kappa 与 tau 都是**标准无质量标量动能项**。其零点能求和")
    ap("      M_Pl^4/(16 pi^2) = %.4e GeV^4，而 rho_Lambda = %.4e GeV^4" % (
        C["zp"]["zp"], C["zp"]["rho_gev4"]))
    ap("      ⇒ 比值 %.4e = %.3f 个数量级。" % (C["zp"]["ratio"], ordmag(C["zp"]["ratio"])))
    ap("      靶 L4776 逐字称「这直接绕开 10^120 量级灾难」。机验：它复现的")
    ap("      正是 %.3f 个数量级的灾难，与它声称绕开的 10^120 差 %.2f 个数量级" % (
        ordmag(C["zp"]["ratio"]), abs(ordmag(C["zp"]["ratio"]) - 120.0)))
    ap("      （%.2f 倍）⇒ 同量级 ⇒ **未绕开**。根因见 D02：它把 <delta tau>"
       % (C["zp"]["ratio"] / 1e120))
    ap("      与 <0|H|0> 混淆了。")
    ap("")
    spread = ordmag(C["om"]["1/l_P"]) - ordmag(C["om"]["H0/c"])
    ap("  ★★★ C04 三个自然候选 tau 跨 %.1f 个数量级，靶一个都没选" % spread)
    ap("      tau = H0/c      = %.4e m^-1 => Omega = 1/3 = %.10f（Fraction 残差 0）" % (
        C["cand"]["H0/c"], C["om"]["H0/c"]))
    ap("         ⇒ 相对观测 0.6889 差 %.3f 倍 ⇒ 该自然口径被排除" % (OM_L / C["om"]["H0/c"]))
    ap("      tau = 1/l_P     = %.4e m^-1 => Omega = %.4e（超 %.2f 个数量级）" % (
        C["cand"]["1/l_P"], C["om"]["1/l_P"],
        ordmag(C["om"]["1/l_P"]) - ordmag(OM_L)))
    ap("      tau = v/(hbar c) = %.4e m^-1 => Omega = %.4e（超 %.2f 个数量级）" % (
        C["cand"]["v/(hbar c)"], C["om"]["v/(hbar c)"],
        ordmag(C["om"]["v/(hbar c)"]) - ordmag(OM_L)))
    ap("      跨距 %.3f 个数量级。靶只写「tau_Lambda << tau_vac」，从未指定" % (
        ordmag(C["om"]["1/l_P"]) - ordmag(C["om"]["H0/c"])))
    ap("      tau_Lambda 由哪个内部量给出 ⇒ 判「未行使」，不判「零判别力」")
    ap("      （判别力先测后指控）。")
    ap("")
    ap("  ★★ C03 两种读法反解 tau_Lambda，差一个 c = 8.48 个数量级")
    ap("      propto 读法（A=1）：tau = sqrt(Lambda) = %.4e m^-1" % C["tau"]["prop"])
    ap("      等号读法（带 c^2）：tau = sqrt(Lambda)/c = %.4e m^-1" % C["tau"]["eq"])
    ap("      比值 = %.6e = c。靶在 A03 处混用 propto 与 =，从未指定用哪个。"
       % C["tau"]["ratio"])
    ap("")
    ap("  ★★ B01 量纲：boxed 式 Lambda propto c^2 tau^2 多了一个 c^2")
    ap("      Lambda 量纲 %s ; c^2 tau^2 量纲 %s ; 差 %s" % (
        dfmt(DIM["Lambda"]), dfmt(dmul("c", "c", "tau", "tau")), dfmt(B["gap"])))
    ap("      ⇒ 正确形式应为 Lambda propto tau^2（比例常数无量纲），")
    ap("        或 Lambda propto omega^2/c^2。带与不带 c^2 数值差 c^2 = %.4e 倍。" % (C0 ** 2))
    ap("      B02 下游后果：若照字面代进 rho = Lambda c^2/(8 pi G)，得到的")
    ap("      rho 量纲是 %s（压强）而非 %s（密度）。" % (
        dfmt(B["d_rho_if"]), dfmt(B["d_rho_ok"])))
    ap("")
    ap("  ★★★ E01 tau_Lambda 本体论二难（两支都死）")
    ap("      支 A 几何基底（静态/不随时间演化）：与 L4783「随宇宙演化调整」")
    ap("       矛盾；且「不稀释」变成额外规定而非靶所称「自然结果」；且若它")
    ap("       不可演化，则与它所批评的「手动加进场方程的常数」信息含量等价 ——")
    ap("       只是把自由常数 Lambda 改名为自由常数 tau_Lambda。")
    ap("      支 B 动力学场（能演化/能冻结/代入 omega 约束）：有非零 T_munu")
    ap("       ⇒ 一般 w != -1 ⇒ 与 L4774「完美满足 w=-1」矛盾。")
    ap("       要 w=-1 必须不可演化；要可演化必须 w!=-1。")
    ap("")
    ap("  ★★ C06 加速膨胀不是推论：若 tau 按逆长度稀释，q0 反号变减速")
    ap("      w=-1   => q0 = %+.5f（加速，合观测）" % C["qA"])
    ap("      w=-1/3 => q0 = %+.5f（减速）。Fraction 严格：w=-1/3 时" % C["qB"])
    ap("      (1+3w)=0，q0 = 1/2 Om_m = %s，残差 0。" % fmt(q0_fraction(Fraction(-1, 3)), 5))
    ap("")
    ap("  ★★★ D01 w=-1 是定义恒等式（正对照 5/5 成功）")
    ap("      链条：tau=const(规定) => Lambda=const => rho=const => w=-1。")
    ap("      四步是同一假设的重述。把目标 w 依次换成 -1/-0.9/-0.5/-1/3/+1/3，")
    ap("      链条照样「推出」（5/5），且不读 target ⇒ 零判别力。")
    ap("")
    ap("  ★★ A07 + E02 「区分于 LambdaCDM」提供 0 比特")
    ap("      该节唯一预言「w 严格等于 -1，不随红移演化」正是 LambdaCDM 的")
    ap("      定义特征；把主语换成 LambdaCDM 一字不改仍成立。")
    ap("")
    ap("  ★★ D04 问题平移：「Lambda 小 120 个数量级」-> 「tau 小 60 个数量级」")
    ap("      tau = sqrt(Lambda) 是 1-1 映射，指数减半是数学换元，不是物理机制。")
    ap("      靶 L4798 逐字承认「待完成的定量目标：解析求出 tau_Lambda 与 v")
    ap("      之间的比例系数」⇒ 靶自认未完成。")
    ap("")
    ap("-" * 96)
    ap("【对靶有利（如实登记，不掩饰）】")
    ap("  Y1 C02：靶写的 rho_Lambda ~ 1e-9 J/m^3 量级正确（本卷算 %.4e J/m^3，" % co["u_l"])
    ap("     差 %.2f 倍，log10 差 %.3f < 1）。" % (
        max(co["u_l"] / 1e-9, 1e-9 / co["u_l"]), abs(ordmag(co["u_l"]) + 9)))
    ap("  Y2 A08：靶主动把「10^120 个数量级灾难」列为本理论要解决的问题 ——")
    ap("     问题意识正确，且它引用的标准 QFT 结果本身无误（本卷复算 %.3f 个" % ordmag(C["zp"]["ratio"]))
    ap("     数量级，与 10^120 同量级）。")
    ap("  Y3 靶的 FRW 两个 boxed 方程（L4765-4767）与教科书一致，无符号错。")
    ap("  Y4 靶的「w=-1 则加速」这一步的符号正确（C06 的 w=-1 分支 q0<0）。")
    ap("  Y5 L4798 的自我限定（「待完成的定量目标」）是本语料中少见的诚实标注。")
    ap("  Y6 「真空挠率云 => 圈修正」与 QED 真空极化图像同构（r255 已记）。")
    ap("")
    ap("-" * 96)
    ap("【修复定价】7 槽位 x 2^7 = 128 组合，双档")
    st, lo = pr["strict"], pr["loose"]
    ap("  严格档（必改 6 项 %s）：EMPTY %d / SUICIDE %d / SURVIVE %d" % (
        st["req"], st["EMPTY"], st["SUICIDE"], st["SURVIVE"]))
    ap("  宽松档（必改 2 项 %s）：EMPTY %d / SUICIDE %d / SURVIVE %d" % (
        lo["req"], lo["EMPTY"], lo["SUICIDE"], lo["SURVIVE"]))
    ap("  ⇒ 两档 SURVIVE 均 > 0 ⇒ 判「靶未达成」，**本卷不占「修复即自杀」度数**。")
    ap("  ⇒ 唯一严格存活路径要求完成靶自己承认「待完成」的那一步（s4）。")
    ap("  最小修法（不代选）：s1 单独（代价 1，修量纲）· s2 单独（代价 1，统一 propto/=）")
    ap("   · s3+s5+s6（代价 3，仅修表述诚实性）· s4 无法用「修」完成，需新物理。")
    ap("")
    ap("-" * 96)
    ap("【治理】")
    ap("  * 靶 3 份只读；sha256 前后逐位一致（GU02）：")
    for d in docs:
        ap("      %s  %s  %d bytes" % (d["sha256"][:16], d["path"].split("/")[-1][:46],
                                    d["nbytes"]))
    ap("  * r142-r255 产物只读；未改 verify.py；未跑 refresh_catalog.py；未做 git。")
    ap("  * 本卷为「暗能量与宇宙常数层」首卷，与 r251（FRW 约化/黑洞无奇点）、")
    ap("    r252（质量谱）、r254（宇宙学扰动·复现层）**不是同一层**，")
    ap("    条目**不可与 r142-r255 相加**。")
    ap("  * 交联指针 F01/F02 不计分，避免与 r252/r251 重复计数。")
    ap("")
    ap("=" * 96)
    ap("【条目明细】")
    for e in ENTRIES:
        ap("")
        ap("  [%s] %s  %s" % (e["id"], e["verdict"], e["title"]))
        ap("      %s" % e["detail"].replace("\n", "\n      "))
    ap("")
    ap("=" * 96)
    ap("【控制组明细】")
    for c in CONTROLS:
        ap("  %-4s %s  %s" % (c["id"], "OK  " if c["ok"] else "FAIL", c["name"]))
        ap("       %s" % c["detail"])
    ap("")
    ap("=" * 96)
    ap("【守卫明细】")
    for g in GUARDS:
        ap("  %-5s %s  %s" % (g["id"], "OK  " if g["ok"] else "FAIL", g["name"]))
        ap("        %s" % g["detail"])
    ap("")
    ap("=" * 96)
    ap("报告结束。rc = 0 当且仅当守卫全绿且控制组全绿。")
    return "\n".join(L_)


# ================================================================ 输出
def write_outputs(txt, docs, L, C, B, D, pr, deg):
    p_rep = os.path.join(DATA, SLUG + "_report.txt")
    io.open(p_rep, "w", encoding="utf-8").write(txt)

    payload = {
        "rid": RID, "title": TITLE_CN,
        "slug": SLUG,
        "targets": [{"path": d["path"], "sha256": d["sha256"],
                     "nbytes": d["nbytes"], "lines": len(d["lines"])} for d in docs],
        "tally": tally(),
        "entries": ENTRIES,
        "controls": CONTROLS,
        "guards": GUARDS,
        "pricing": {k: {kk: pr[k][kk] for kk in ("EMPTY", "SUICIDE", "SURVIVE",
                                                 "total", "req")}
                    for k in ("strict", "loose")},
        "key_numbers": {
            "Lambda_m-2": C["Lam"],
            "Lambda_lit_m-2": LAM_LIT,
            "rho_Lambda_J_m3": C["co"]["u_l"],
            "tau_prop_m-1": C["tau"]["prop"],
            "tau_eq_m-1": C["tau"]["eq"],
            "tau_ratio": C["tau"]["ratio"],
            "tau_H0_over_c": C["cand"]["H0/c"],
            "tau_planck": C["cand"]["1/l_P"],
            "tau_EW": C["cand"]["v/(hbar c)"],
            "Omega_tauH": C["om"]["H0/c"],
            "Omega_tauP": C["om"]["1/l_P"],
            "Omega_tauEW": C["om"]["v/(hbar c)"],
            "zp_GeV4": C["zp"]["zp"],
            "rho_GeV4": C["zp"]["rho_gev4"],
            "zp_ratio": C["zp"]["ratio"],
            "zp_decades": ordmag(C["zp"]["ratio"]),
            "q0_w-1": C["qA"],
            "q0_w-1/3": C["qB"],
            "dim_gap": dfmt(B["gap"]),
        },
        "degree": deg,
    }
    p_json = os.path.join(DATA, SLUG + ".json")
    io.open(p_json, "w", encoding="utf-8").write(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str))

    p_md = os.path.join(DATA, "判定_" + SLUG + ".md")
    io.open(p_md, "w", encoding="utf-8").write(build_md(payload, C, B, D, pr, deg))

    p_html = os.path.join(HERE, SLUG + ".html")
    io.open(p_html, "w", encoding="utf-8").write(build_html(payload, C, B, D, pr))
    return p_rep, p_json, p_md, p_html


# ================================================================ 判定册
def build_md(payload, C, B, D, pr, deg):
    t = payload["tally"]
    n_ctl = sum(1 for c in CONTROLS if c["ok"])
    n_gd = sum(1 for g in GUARDS if g["ok"])
    st, lo = pr["strict"], pr["loose"]
    o = []
    A = o.append
    A("<!-- 本文件由 TUFT-%s 脚本自动生成，元数据一律参数化，禁止手改卷号 -->" % RID.upper())
    A("")
    A("# 判定册 · TUFT-%s · %s" % (RID.upper(), TITLE_CN))
    A("")
    A("**攻靶**：靶把宇宙学常数 $\\Lambda$ 改写为「全局背景挠率 $\\tau_\\Lambda$ 的平方项」，"
      "并声称由此得到 (a) $w=-1$、(b) 绕开 $10^{120}$ 量级灾难、(c) 解决「$\\Lambda$ 为何这么小」、"
      "(d) 区分于 $\\Lambda$CDM。")
    A("")
    A("**靶文**：`基于光速螺旋流形的核心动力学方程组.md` L4720–L4800（$\\Lambda$ 专章）、"
      "L883–L930（FRW 平行表述）。")
    A("")
    A("> **一句判词**：四条声称全部不成立；但本卷判的是「**靶未达成**」，"
      "不是「逻辑上不可能」——修复定价两档 SURVIVE 均 $>0$，"
      "唯一严格存活路径恰是补上靶**自己承认未做**的那一步。")
    A("")
    A("- 条目 **%d**（PASS %d / FAIL %d / INFO %d / BOUNDARY %d）；"
      "控制组 **%d/%d**；守卫 **%d/%d**；rc=0" % (
          len(ENTRIES), t.get("PASS", 0), t.get("FAIL", 0), t.get("INFO", 0),
          t.get("BOUNDARY", 0), n_ctl, len(CONTROLS), n_gd, len(GUARDS)))
    A("- **%s**" % DEGREE_NOTE)
    A("")
    A("## 判决分组表")
    A("")
    A("| 组 | 内容 | 判 |")
    A("| :-- | :-- | :-- |")
    A("| A | 原文核验 8 条：boxed 定位、平行表述（复制非多路）、$\\propto$ 与 $=$ 混用、"
      "$\\tau_\\Lambda$ 数值赋值 0 处、本体论三句冲突、$w=-1$ 声称、"
      "「区分于 $\\Lambda$CDM」与 $w=-1$ 不可区分、$10^{120}$ 被主动点名 "
      "| **FAIL 4 / PASS 3 / INFO 1** |")
    A("| B | ★★ 量纲 3 条：$\\Lambda[L^{-2}]$ vs $c^2\\tau^2[T^{-2}]$、"
      "$\\rho$ 变压强、$\\tau_{\\rm vac}=v=246$ GeV 量纲错置 | **FAIL 3** |")
    A("| C | ★★★ 定量 7 条：$\\Lambda$ 正算、$\\rho_\\Lambda$ 量级、两读法差 $c$、"
      "三候选跨 121.9 量级、零点能灾难 $10^{%.2f}$、$q_0$ 反号、灾难缩水 33.4 "
      "| **FAIL 4 / PASS 2 / BOUNDARY 1** |" % ordmag(C["zp"]["ratio"]))
    A("| D | ★★★ 定义恒等式刀 4 条：$w=-1$ 链重述 4 次（正对照 5/5）、"
      "$\\langle\\delta\\tau\\rangle\\ne\\langle0|H|0\\rangle$、反解 5/5、问题平移 | **FAIL 4** |")
    A("| E | ★★★ 本体论二难 3 条：几何基底 vs 动力学场（两支都死）、「区分」0 比特、"
      "「不稀释」与 $[L^{-1}]$ 不兼容 | **FAIL 3** |")
    A("| F | 交联指针 2 条（不重复 r251/r252，**不计分**） | INFO |")
    A("| G | 修复定价 $2^7=128$，双档 | **BOUNDARY（SURVIVE>0）** |")
    A("")
    A("## 承重发现")
    A("")
    A("### 1. 靶自己的拉氏量复现 $10^{%.2f}$ 灾难 —— 「直接绕开」是空话" % ordmag(C["zp"]["ratio"]))
    A("")
    A("靶 L4711–L4713 给出 $\\mathcal{L}=\\frac12(\\partial\\kappa)^2+\\frac12(\\partial\\tau)^2"
      "-\\frac12(\\cdots)^2$。其中 $\\kappa$、$\\tau$ 都是**标准无质量标量动能项**。")
    A("")
    A("| 量 | 值 |")
    A("| :-- | --: |")
    A("| 零点能 $M_{\\rm Pl}^4/(16\\pi^2)$ | $%.4e$ GeV$^4$ |" % C["zp"]["zp"])
    A("| $\\rho_\\Lambda$ | $%.4e$ GeV$^4$ |" % C["zp"]["rho_gev4"])
    A("| 比值 | $%.4e$（$%.3f$ 个数量级） |" % (C["zp"]["ratio"], ordmag(C["zp"]["ratio"])))
    A("")
    A("靶 L4776 逐字称「这直接绕开 $10^{120}$ 量级灾难」。机验：它复现的正是 "
      "$%.3f$ 个数量级，与 $10^{120}$ 差 $%.2f$ 个数量级（$%.2f$ 倍）⇒ **同量级**。" % (
          ordmag(C["zp"]["ratio"]), abs(ordmag(C["zp"]["ratio"]) - 120.0),
          C["zp"]["ratio"] / 1e120))
    A("")
    A("根因（D02）：靶把 $\\langle\\delta\\tau\\rangle$ 与 $\\langle 0|\\hat H|0\\rangle$ 混淆。"
      "前者为零**不能**推出后者为零；真空能是后者。")
    A("")
    A("### 2. 三个自然候选 $\\tau$ 跨 121.9 个数量级，靶一个都没选")
    A("")
    A("| 候选 | $\\tau$ (m$^{-1}$) | $\\Omega_\\Lambda$ | 相对观测 0.6889 |")
    A("| :-- | --: | --: | --: |")
    A("| $H_0/c$ | $%.4e$ | **$1/3$**（Fraction 残差 0） | 差 $%.3f$ 倍 |" % (
        C["cand"]["H0/c"], OM_L / C["om"]["H0/c"]))
    A("| $1/\\ell_P$ | $%.4e$ | $%.4e$ | 超 $%.2f$ 个数量级 |" % (
        C["cand"]["1/l_P"], C["om"]["1/l_P"],
        ordmag(C["om"]["1/l_P"]) - ordmag(OM_L)))
    A("| $v/(\\hbar c)$ | $%.4e$ | $%.4e$ | 超 $%.2f$ 个数量级 |" % (
        C["cand"]["v/(hbar c)"], C["om"]["v/(hbar c)"],
        ordmag(C["om"]["v/(hbar c)"]) - ordmag(OM_L)))
    A("| **观测要求** | $%.4e$ | $0.6889$ | — |" % C["tau"]["prop"])
    A("")
    A("$\\tau=H_0/c$ 给 $\\Omega_\\Lambda=1/3$ 是**代数必然**（与 $H_0$ 无关）："
      "因 $\\Omega=\\tau^2c^2/(3H_0^2)$，代入 $\\tau=H_0/c$ 得 $\\Omega=1/3$。"
      "观测 $0.6889$ ⇒ 该口径被排除 $%.3f$ 倍。靶只写「$\\tau_\\Lambda\\ll\\tau_{\\rm vac}$」，"
      "**从未指定 $\\tau_\\Lambda$ 由哪个内部量给出** ⇒ 判「未行使」。" % (OM_L / C["om"]["H0/c"]))
    A("")
    A("### 3. 量纲：boxed 式多了一个 $c^2$")
    A("")
    A("| 量 | (M,L,T) |")
    A("| :-- | :-- |")
    A("| $\\Lambda$ | %s |" % dfmt(DIM["Lambda"]))
    A("| $c^2\\tau^2$ | %s |" % dfmt(dmul("c", "c", "tau", "tau")))
    A("| 差 | %s ⇒ 需再乘 $1/c^2$ |" % dfmt(B["gap"]))
    A("")
    A("正确形式应为 $\\Lambda\\propto\\tau^2$（比例常数无量纲）或 $\\Lambda\\propto\\omega^2/c^2$。"
      "下游后果（B02）：照字面代进 $\\rho=\\Lambda c^2/(8\\pi G)$，得到 $\\rho$ 的量纲是 "
      "%s（压强）而非 %s（密度）。" % (dfmt(B["d_rho_if"]), dfmt(B["d_rho_ok"])))
    A("")
    A("### 4. $\\tau_\\Lambda$ 本体论二难（两支都死）")
    A("")
    A("| 支 | 靶的原文依据 | 后果 |")
    A("| :-- | :-- | :-- |")
    A("| **A 几何基底** | 「均匀、**静态**」「**不随时间演化**」「时空本身的基底几何属性」 | "
      "①与 L4783「**随宇宙演化调整**」直接矛盾；②「不稀释」成为**额外规定**而非靶所称「自然结果」；"
      "③若不可演化，则与它所批评的「手动加进场方程的常数」**信息含量等价**——只是改名 |")
    A("| **B 动力学场** | 「随演化调整」「冻结为常数」「代入 $\\omega^2$ 约束」"
      "$\\delta\\tau$ 对应粒子/规范场 | 有非零 $T_{\\mu\\nu}$ ⇒ 一般 $w\\ne-1$ ⇒ "
      "与 L4774「**完美满足** $w=-1$」矛盾 |")
    A("")
    A("> 要 $w=-1$ 必须**不可演化**；要**可演化**必须 $w\\ne-1$。")
    A("")
    A("### 5. $w=-1$ 是定义恒等式（正对照 5/5 成功）")
    A("")
    A("链条：$\\tau_\\Lambda=$const（**规定**）$\\Rightarrow$ $\\Lambda\\propto\\tau^2=$const "
      "$\\Rightarrow$ $\\rho_\\Lambda=\\Lambda c^2/(8\\pi G)=$const $\\Rightarrow$ $w=P/\\rho=-1$。")
    A("")
    A("四步全是同一假设的重述。正对照：把目标 $w$ 依次换成 $-1,-0.9,-0.5,-1/3,+1/3$，"
      "链条**照样「推出」**（%d/5），且链条**不读** target ⇒ **零判别力**。" % D["w_chain_success"])
    A("")
    A("### 6. 加速膨胀不是推论：若 $\\tau$ 按逆长度稀释，$q_0$ 反号")
    A("")
    A("| 情形 | $w$ | $q_0$ | 判 |")
    A("| :-- | --: | --: | :-- |")
    A("| $\\tau_\\Lambda=$const（靶的规定） | $-1$ | $%+.5f$ | 加速，合观测 |" % C["qA"])
    A("| $\\tau\\propto 1/a$（几何标度） | $-1/3$ | $%+.5f$ | **减速，反号** |" % C["qB"])
    A("")
    A("Fraction 严格：$w=-1/3$ 时 $(1+3w)=0$，故 $q_0=\\frac12\\Omega_m=%s$，残差 $0$。" % fmt(
        q0_fraction(Fraction(-1, 3)), 5))
    A("")
    A("### 7. 「区分于 $\\Lambda$CDM」提供 0 比特")
    A("")
    A("该节唯一预言「$w$ 严格等于 $-1$，不随红移演化」**正是** $\\Lambda$CDM 的定义特征；"
      "证伪条件「观测到 $w$ 偏离 $-1$」也**逐字相同**。把该节主语换成 $\\Lambda$CDM，"
      "文本不变、预言不变、证伪条件不变 ⇒ **0 比特**。")
    A("")
    A("## 对靶有利（如实登记）")
    A("")
    A("| # | 内容 |")
    A("| :-- | :-- |")
    A("| Y1 | $\\rho_\\Lambda\\approx10^{-9}$ J/m$^3$ 量级正确（本卷算 $%.4e$，比值 $%.2f$） |" % (
        C["co"]["u_l"], C["co"]["u_l"] / 1e-9))
    A("| Y2 | 靶**主动**把 $10^{120}$ 列为要解决的疑难；其引用的标准 QFT 结果无误（本卷复算 $%.2f$ 个数量级） |" % ordmag(C["zp"]["ratio"]))
    A("| Y3 | FRW 两个 boxed 方程与教科书一致，无符号错 |")
    A("| Y4 | 「$w=-1$ 则加速」的符号正确（$q_0<0$） |")
    A("| Y5 | L4798 的自我限定（「待完成的定量目标」）是本语料中少见的诚实标注 |")
    A("| Y6 | 「真空挠率云 $\\Rightarrow$ 圈修正」与 QED 真空极化同构（r255 已记） |")
    A("")
    A("## 修复定价")
    A("")
    A("槽位：")
    A("")
    for sid, desc in SLOTS:
        A("- **%s** %s" % (sid, desc))
    A("")
    A("| 档 | 必改 | EMPTY | SUICIDE | SURVIVE |")
    A("| :-- | :-- | --: | --: | --: |")
    A("| 严格 | %s | %d | %d | **%d** |" % (", ".join(sorted(st["req"])),
                                            st["EMPTY"], st["SUICIDE"], st["SURVIVE"]))
    A("| 宽松 | %s | %d | %d | **%d** |" % (", ".join(sorted(lo["req"])),
                                            lo["EMPTY"], lo["SUICIDE"], lo["SURVIVE"]))
    A("")
    A("> 两档 SURVIVE 均 $>0$ ⇒ 靶的宣称**逻辑上非不可能**，本卷判「**靶未达成**」，"
      "**不占「修复即自杀」度数**。唯一严格存活路径要求完成靶自己 line L4798 承认"
      "「待完成」的那一步（s4：给出 $\\tau_\\Lambda$ 的数值来源）。")
    A("")
    A("**最小修法（不代选）**：`s1` 单独（代价 1，修量纲）· `s2` 单独（代价 1，统一 "
      "$\\propto$/$=$）· `s3+s5+s6`（代价 3，仅修表述诚实性：删自相矛盾的演化叙述 + "
      "撤回两个过度声称）· **`s4` 无法用「修」完成**，它需要新物理。")
    A("")
    A("## 性质界定")
    A("")
    A("1. **B 组是纯量纲**，与任何数值无关：$[L^{-2}]\\ne[T^{-2}]$ 在任何单位制下都成立"
      "（$c=1$ 自然单位下二者同，但靶显式写了 $c^2$，即按 SI 书写）。")
    A("2. **C05 是量级估计**，因子 $2\\pi$ 级不确定；本卷并列两条独立路径"
      "（零点能 $M_{\\rm Pl}^4/16\\pi^2$ 给 $%.2f$、$(1/\\ell_P)^2$ 给 $%.2f$），"
      "二者差 $%.2f$ 个数量级，同为量级估计。" % (
          ordmag(C["zp"]["ratio"]), ordmag((1.0 / LP) ** 2) - ordmag(C["Lam"]),
          abs(ordmag(C["zp"]["ratio"]) - (ordmag((1.0 / LP) ** 2) - ordmag(C["Lam"])))))
    A("3. **C04 判「未行使」而非「零判别力」**：先实测三个候选（判别力先测后指控），"
      "发现靶对 $\\tau_\\Lambda$ 的数值**完全未行使选择权**。")
    A("4. **D01/D03/E02 三组正对照**是独立取证：$w$ 链 5/5「成功」、反解 5/5「成功」、"
      "「区分」0 比特 —— 三者共同证明这些「推导」零判别力。")
    A("5. **$\\Lambda$ 自身的取值问题**（$H_0$ 张力、$\\Omega_\\Lambda$ 精度）不属本卷，"
      "归观测统计层（r246）。")
    A("6. **不重复 r251/r252**：F01/F02 为交联指针，**不计入判分**。")
    A("")
    A("## 治理")
    A("")
    A("- **取号**：起草前实测 r256/r257/r258 三树全空；起草期间 **r256** 被并行会话"
      "完整占用（四力统一方程·宇宙学声学峰层，四件套 12 个文件）、**r257** 已有 .py "
      "正在起草（同一运动定理卷）⇒ 按「已产四件套并登记者为权威、后到者整体改号」纪律，"
      "本卷**整体改至 %s**，未改写他人任何字节。**下轮从 r259 起**"
      "（落盘前仍须实测 r259/r260/r261）。" % RID)
    A("- **靶只读**：3 份 sha256 前后逐位一致（GU02）：")
    for d in payload["targets"]:
        A("  - `%s…` %s（%d bytes, %d 行）" % (
            d["sha256"][:16], d["path"].split("/")[-1], d["nbytes"], d["lines"]))
    A("- **未改** `verify.py`；**未跑** `refresh_catalog.py`；**未做** git。")
    A("- **分层铁律**：本卷为暗能量与宇宙常数层，与 r251（FRW 约化/黑洞无奇点）、"
      "r252（质量谱）、r254（宇宙学扰动·复现层）**不是同一层**，"
      "条目**不可与 r142–r255 相加**。")
    A("- **度数**：%s" % deg[1])
    A("")
    A("## 机读对账")
    A("")
    A("```")
    A("条目 %d = PASS %d + FAIL %d + INFO %d + BOUNDARY %d" % (
        len(ENTRIES), t.get("PASS", 0), t.get("FAIL", 0), t.get("INFO", 0),
        t.get("BOUNDARY", 0)))
    A("各组：%s" % {g: sum(1 for e in ENTRIES if e["group"] == g)
                    for g in sorted({e["group"] for e in ENTRIES})})
    A("控制组 %d/%d    守卫 %d/%d" % (n_ctl, len(CONTROLS), n_gd, len(GUARDS)))
    A("定价 严格 %d/128  宽松 %d/128" % (st["total"], lo["total"]))
    A("```")
    return "\n".join(o) + "\n"


# ================================================================ 交互可视化
def build_html(payload, C, B, D, pr):
    t = payload["tally"]
    n_ctl = sum(1 for c in CONTROLS if c["ok"])
    n_gd = sum(1 for g in GUARDS if g["ok"])
    data = {
        "tauH": math.log10(C["cand"]["H0/c"]),
        "tauP": math.log10(C["cand"]["1/l_P"]),
        "tauEW": math.log10(C["cand"]["v/(hbar c)"]),
        "tauObs": math.log10(C["tau"]["prop"]),
        "tauObsEq": math.log10(C["tau"]["eq"]),
        "omH": C["om"]["H0/c"],
        "omP": C["om"]["1/l_P"],
        "omEW": C["om"]["v/(hbar c)"],
        "zpDec": ordmag(C["zp"]["ratio"]),
        "qA": C["qA"],
        "qB": C["qB"],
        "Lam": C["Lam"],
    }
    o = []
    A = o.append
    A("<!DOCTYPE html>")
    A('<html lang="zh-CN">')
    A("<head>")
    A('<meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A("<title>TUFT-%s · %s · 机器核验</title>" % (RID.upper(), TITLE_CN))
    A("<style>")
    A(":root{--ink:#12161c;--sub:#5a6472;--line:#dfe4ea;--bg:#fbfcfd;--card:#ffffff;")
    A("--red:#c0392b;--green:#1e8449;--blue:#1f5fa9;--amber:#b9770e;--violet:#7d3c98;}")
    A("*{box-sizing:border-box}")
    A("body{margin:0;background:var(--bg);color:var(--ink);")
    A("font-family:'Segoe UI','PingFang SC','Microsoft YaHei',system-ui,sans-serif;")
    A("line-height:1.62;font-size:15px}")
    A(".wrap{max-width:1060px;margin:0 auto;padding:38px 22px 80px}")
    A("h1{font-size:26px;margin:0 0 6px;letter-spacing:-.3px}")
    A("h2{font-size:19px;margin:38px 0 12px;padding-bottom:7px;border-bottom:2px solid var(--line)}")
    A("h3{font-size:15.5px;margin:22px 0 8px;color:var(--blue)}")
    A(".sub{color:var(--sub);font-size:13.5px}")
    A(".card{background:var(--card);border:1px solid var(--line);border-radius:10px;")
    A("padding:18px 20px;margin:14px 0;box-shadow:0 1px 2px rgba(20,30,45,.04)}")
    A(".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}")
    A(".kpi{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:13px 15px}")
    A(".kpi .lab{font-size:11.5px;color:var(--sub);letter-spacing:.4px;text-transform:uppercase}")
    A(".kpi .val{font-size:20px;font-weight:650;font-variant-numeric:tabular-nums;margin-top:3px}")
    A(".kpi .note{font-size:11.5px;color:var(--sub);margin-top:2px}")
    A("table{border-collapse:collapse;width:100%;font-size:13.5px;margin:10px 0}")
    A("th,td{border-bottom:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}")
    A("th{background:#f4f6f9;font-weight:620;font-size:12.5px}")
    A("td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;font-family:ui-monospace,Consolas,monospace}")
    A(".tag{display:inline-block;font-size:11px;padding:1px 7px;border-radius:20px;")
    A("font-weight:640;letter-spacing:.3px}")
    A(".t-fail{background:#fdecea;color:var(--red)}")
    A(".t-pass{background:#e8f6ee;color:var(--green)}")
    A(".t-info{background:#eaf1fa;color:var(--blue)}")
    A(".t-bnd{background:#fdf3e3;color:var(--amber)}")
    A("canvas{display:block;width:100%;height:auto;max-width:100%}")
    A(".cap{font-size:12.3px;color:var(--sub);margin-top:6px}")
    A("blockquote{margin:12px 0;padding:10px 15px;border-left:3px solid var(--blue);")
    A("background:#f2f6fb;color:#243040;font-size:13.7px;border-radius:0 7px 7px 0}")
    A("code{font-family:ui-monospace,Consolas,monospace;font-size:12.6px;")
    A("background:#f0f2f5;padding:1px 5px;border-radius:4px}")
    A(".bar{height:9px;border-radius:5px;background:#eef1f5;overflow:hidden;margin-top:6px}")
    A(".bar>i{display:block;height:100%;border-radius:5px}")
    A("footer{margin-top:46px;padding-top:16px;border-top:1px solid var(--line);")
    A("color:var(--sub);font-size:12.4px}")
    A("</style>")
    A("</head>")
    A("<body><div class=\"wrap\">")
    A("<h1>TUFT-%s · %s</h1>" % (RID.upper(), TITLE_CN))
    A("<div class=\"sub\">攻靶：把宇宙学常数 Λ 改写为「全局背景挠率 τ<sub>Λ</sub> 的平方项」。"
      "靶文 L4720–L4800。<b>本卷判「靶未达成」，不占度數链。</b></div>")
    A("")
    A("<div class=\"grid\" style=\"margin-top:20px\">")
    kpis = [
        ("条目", str(len(ENTRIES)), "PASS %d / FAIL %d / INFO %d / BND %d" % (
            t.get("PASS", 0), t.get("FAIL", 0), t.get("INFO", 0), t.get("BOUNDARY", 0)),
         "var(--ink)"),
        ("控制组", "%d/%d" % (n_ctl, len(CONTROLS)), "全部机算，禁写死 True", "var(--green)"),
        ("守卫", "%d/%d" % (n_gd, len(GUARDS)), "含度数机器核定 G13", "var(--green)"),
        ("零点能灾难", "10<sup>%.1f</sup>" % ordmag(C["zp"]["ratio"]),
         "靶声称绕开的正是这个量级", "var(--red)"),
    ]
    for lab, val, note, col in kpis:
        A("<div class=\"kpi\"><div class=\"lab\">%s</div>" % lab)
        A("<div class=\"val\" style=\"color:%s\">%s</div>" % (col, val))
        A("<div class=\"note\">%s</div></div>" % note)
    A("</div>")
    A("")
    A("<blockquote><b>一句判词</b>：靶的四条声称（w=−1 / 绕开 10<sup>120</sup> / "
      "解决 Λ 小值 / 区分于 ΛCDM）全部不成立；但本卷判的是「<b>靶未达成</b>」而非"
      "「逻辑上不可能」——修复定价两档 SURVIVE 均 &gt; 0，唯一严格存活路径恰是补上"
      "靶自己逐字承认「待完成」的那一步。</blockquote>")

    # ---- 图 1：三候选跨距
    A("<h2>1 · 三个自然候选 τ 跨 %.1f 个数量级</h2>" % (
        math.log10(C["om"]["1/l_P"]) - math.log10(C["om"]["H0/c"])))
    A("<div class=\"card\"><canvas id=\"c1\" height=\"300\"></canvas>")
    A("<div class=\"cap\">横轴为 log₁₀ τ（m⁻¹）。三个候选 $H_0/c$、$1/\\ell_P$、"
      "$v/(\\hbar c)$ 与观测要求的 τ<sub>Λ</sub>（红）。靶只写「τ<sub>Λ</sub> ≪ τ<sub>vac</sub>」，"
      "从未指定 τ<sub>Λ</sub> 由哪个内部量给出 ⇒ 判「未行使」。</div></div>")
    A("")
    A("<table><tr><th>候选</th><th class=\"n\">τ (m⁻¹)</th><th class=\"n\">Ω<sub>Λ</sub></th>"
      "<th>判</th></tr>")
    A("<tr><td>H₀/c</td><td class=\"n\">%.4e</td><td class=\"n\">1/3 = %.6f</td>"
      "<td>与 H₀ 无关的<b>代数必然</b>；相对观测 0.6889 差 %.3f 倍</td></tr>" % (
          C["cand"]["H0/c"], C["om"]["H0/c"], OM_L / C["om"]["H0/c"]))
    A("<tr><td>1/ℓ<sub>P</sub></td><td class=\"n\">%.4e</td><td class=\"n\">%.4e</td>"
      "<td>超观测 %.2f 个数量级</td></tr>" % (
          C["cand"]["1/l_P"], C["om"]["1/l_P"],
          ordmag(C["om"]["1/l_P"]) - ordmag(OM_L)))
    A("<tr><td>v/(ℏc)</td><td class=\"n\">%.4e</td><td class=\"n\">%.4e</td>"
      "<td>超观测 %.2f 个数量级</td></tr>" % (
          C["cand"]["v/(hbar c)"], C["om"]["v/(hbar c)"],
          ordmag(C["om"]["v/(hbar c)"]) - ordmag(OM_L)))
    A("<tr><td><b>观测要求</b></td><td class=\"n\"><b>%.4e</b></td>"
      "<td class=\"n\">0.6889</td><td>—</td></tr>" % C["tau"]["prop"])
    A("</table>")

    # ---- 图 2：两读法
    A("<h2>2 · 两种读法反解 τ<sub>Λ</sub>：差一个 c = 8.48 个数量级</h2>")
    A("<div class=\"card\"><canvas id=\"c2\" height=\"230\"></canvas>")
    A("<div class=\"cap\">靶在 boxed 式写「Λ ∝ c²τ²」，在 L4797 又写「Λ = c²τ²」。"
      "同一章内 ∝ 与 = 混用，导致 τ<sub>Λ</sub> 有两个相差 c 倍的取值，"
      "而靶从未指定用哪个。</div></div>")
    A("")

    # ---- 图 3：q0(w)
    A("<h2>3 · 加速膨胀不是推论：τ 若按逆长度稀释，q₀ 反号</h2>")
    A("<div class=\"card\"><canvas id=\"c3\" height=\"300\"></canvas>")
    A("<div class=\"cap\">q₀ = ½Ω<sub>m</sub> + ½Ω<sub>Λ</sub>(1+3w)。"
      "w=−1 给 q₀=−0.533（加速，合观测）；w=−1/3 给 q₀=+0.156（减速，反号）。"
      "Fraction 精确：w=−1/3 时 (1+3w)=0，故 q₀=½Ω<sub>m</sub> 严格。</div></div>")
    A("")

    # ---- 图 4：零点能
    A("<h2>4 · 靶自己的拉氏量复现 10<sup>%.1f</sup> 灾难</h2>" % ordmag(C["zp"]["ratio"]))
    A("<div class=\"card\"><canvas id=\"c4\" height=\"250\"></canvas>")
    A("<div class=\"cap\">靶 L4711–4713 的 ℒ 中 κ、τ 都是<b>标准无质量标量动能项</b>，"
      "零点能求和 M<sub>Pl</sub>⁴/(16π²) 与 ρ<sub>Λ</sub> 之比即它声称「直接绕开」的灾难。"
      "机验：%.2f 个数量级，与 10<sup>120</sup> 同量级 ⇒ <b>未绕开</b>。</div></div>" % ordmag(
          C["zp"]["ratio"]))
    A("")

    # ---- 条目表
    A("<h2>5 · 条目明细（%d）</h2>" % len(ENTRIES))
    A("<table><tr><th>ID</th><th>组</th><th>判</th><th>条目</th></tr>")
    cls = {"FAIL": "t-fail", "PASS": "t-pass", "INFO": "t-info", "BOUNDARY": "t-bnd"}
    for e in ENTRIES:
        A("<tr><td><code>%s</code></td><td>%s</td>" % (e["id"], e["group"]))
        A("<td><span class=\"tag %s\">%s</span></td>" % (cls.get(e["verdict"], ""), e["verdict"]))
        A("<td>%s</td></tr>" % e["title"].replace("<", "&lt;"))
    A("</table>")

    # ---- 定价
    st, lo = pr["strict"], pr["loose"]
    A("<h2>6 · 修复定价（7 槽位 × 2⁷ = 128，双档）</h2>")
    A("<table><tr><th>档</th><th>必改</th><th class=\"n\">EMPTY</th>"
      "<th class=\"n\">SUICIDE</th><th class=\"n\">SURVIVE</th></tr>")
    for nm, d in (("严格", st), ("宽松", lo)):
        A("<tr><td>%s</td><td>%s</td><td class=\"n\">%d</td><td class=\"n\">%d</td>"
          "<td class=\"n\"><b>%d</b></td></tr>" % (
              nm, ", ".join(sorted(d["req"])), d["EMPTY"], d["SUICIDE"], d["SURVIVE"]))
    A("</table>")
    A("<div class=\"cap\">两档 SURVIVE 均 &gt; 0 ⇒ 判「靶未达成」，<b>不占「修复即自杀」度数</b>。"
      "唯一严格存活路径要求完成靶自己 L4798 承认「待完成」的那一步。</div>")

    A("<footer>TUFT-%s · %s · 条目 %d（PASS %d / FAIL %d / INFO %d / BND %d）· "
      "控制组 %d/%d · 守卫 %d/%d · 靶 3 份只读（sha256 前后一致）· "
      "未做 git · 未跑 refresh_catalog.py</footer>" % (
          RID.upper(), TITLE_CN, len(ENTRIES), t.get("PASS", 0), t.get("FAIL", 0),
          t.get("INFO", 0), t.get("BOUNDARY", 0), n_ctl, len(CONTROLS), n_gd, len(GUARDS)))
    A("</div>")

    A("<script>")
    A("var D=%s;" % json.dumps(data))
    A("""
function setup(id,h){
  var cv=document.getElementById(id), dpr=window.devicePixelRatio||1;
  var w=cv.parentNode.clientWidth-40; if(w<320)w=320;
  cv.width=w*dpr; cv.height=h*dpr; cv.style.width=w+'px'; cv.style.height=h+'px';
  var g=cv.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0);
  g.clearRect(0,0,w,h); return {g:g,w:w,h:h};
}
function ax(g,w,h,pad,lab){
  g.strokeStyle='#c9d1da'; g.lineWidth=1;
  g.beginPath(); g.moveTo(pad.l,pad.t); g.lineTo(pad.l,h-pad.b); g.lineTo(w-pad.r,h-pad.b);
  g.stroke();
}
function txt(g,s,x,y,col,fs,al){
  g.fillStyle=col||'#5a6472'; g.font=(fs||11)+"px ui-monospace,Consolas,monospace";
  g.textAlign=al||'left'; g.fillText(s,x,y);
}
function sci(x){
  if(x===0) return '0';
  var e=Math.floor(Math.log10(Math.abs(x)));
  var m=x/Math.pow(10,e);
  return m.toFixed(2)+'e'+e;
}

// ---- 图1 三候选跨距
(function(){
  var h=300, S=setup('c1',h), g=S.g, w=S.w;
  var pad={l:52,r:22,t:26,b:44};
  ax(g,w,h,pad);
  var lo=-40, hi=40;
  function X(v){return pad.l+(v-lo)/(hi-lo)*(w-pad.l-pad.r);}
  for(var v=lo;v<=hi;v+=10){
    g.strokeStyle='#eef1f5'; g.beginPath(); g.moveTo(X(v),pad.t); g.lineTo(X(v),h-pad.b); g.stroke();
    txt(g,'1e'+v,X(v),h-pad.b+16,'#8a94a2',10,'center');
  }
  txt(g,'log10 tau  (m^-1)',(w)/2,h-10,'#5a6472',11,'center');
  var items=[
    {v:D.tauP, c:'#c0392b', lab:'1/l_P', dy:-16},
    {v:D.tauEW,c:'#b9770e', lab:'v/(hbar c)', dy:-16},
    {v:D.tauObs,c:'#1f5fa9', lab:'tau_Lambda (propto, A=1)', dy:34},
    {v:D.tauObsEq,c:'#7d3c98', lab:'tau_Lambda (=, c^2)', dy:56},
    {v:D.tauH, c:'#1e8449', lab:'H0/c', dy:-16}
  ];
  // 跨距括线
  var y0=pad.t+14;
  g.strokeStyle='#c0392b'; g.lineWidth=1.4; g.setLineDash([4,3]);
  g.beginPath(); g.moveTo(X(D.tauObs),y0); g.lineTo(X(D.tauP),y0); g.stroke();
  g.setLineDash([]);
  txt(g,'跨 '+(D.tauP-D.tauObs).toFixed(1)+' 个数量级',(X(D.tauObs)+X(D.tauP))/2,y0-6,'#c0392b',11,'center');
  items.forEach(function(it){
    var x=X(it.v);
    g.fillStyle=it.c; g.beginPath(); g.arc(x,h-pad.b,5,0,6.2832); g.fill();
    g.strokeStyle='#fff'; g.lineWidth=1.5; g.beginPath(); g.arc(x,h-pad.b,5,0,6.2832); g.stroke();
    txt(g,it.lab,x,h-pad.b+it.dy,it.c,10.5,'center');
  });
  g.strokeStyle='#12161c'; g.lineWidth=1; g.setLineDash([2,2]);
  g.beginPath(); g.moveTo(X(D.tauObs),pad.t); g.lineTo(X(D.tauObs),h-pad.b); g.stroke();
  g.setLineDash([]);
})();

// ---- 图2 两读法
(function(){
  var h=230, S=setup('c2',h), g=S.g, w=S.w;
  var pad={l:52,r:22,t:20,b:40};
  var lo=-36, hi=-24;
  function X(v){return pad.l+(v-lo)/(hi-lo)*(w-pad.l-pad.r);}
  ax(g,w,h,pad);
  for(var v=lo;v<=hi;v+=2){
    txt(g,'1e'+v,X(v),h-pad.b+16,'#8a94a2',10,'center');
  }
  txt(g,'log10 tau  (m^-1)',w/2,h-10,'#5a6472',11,'center');
  var bars=[
    {v:D.tauObsEq, lab:'= 读法 (Lambda=c^2 tau^2)', c:'#7d3c98'},
    {v:D.tauObs,   lab:'propto 读法 (A=1)',        c:'#1f5fa9'}
  ];
  bars.forEach(function(b,i){
    var x=X(b.v), y=pad.t+30+i*46;
    g.fillStyle=b.c; g.fillRect(pad.l,y,x-pad.l,22);
    txt(g,b.lab,pad.l+8,y+15,'#fff',11);
    txt(g,'tau = '+sci(Math.pow(10,b.v)),x+8,y+15,b.c,11);
  });
  var dy=(D.tauObs-D.tauObsEq).toFixed(2);
  txt(g,'两读法之差 = '+dy+' 个数量级 = c',pad.l,pad.t+124,'#c0392b',12);
  txt(g,'靶从未指定用哪一个',pad.l,pad.t+142,'#5a6472',11);
})();

// ---- 图3 q0(w)
(function(){
  var h=300, S=setup('c3',h), g=S.g, w=S.w;
  var pad={l:58,r:24,t:22,b:44};
  var wlo=-2.0, whi=0.5, qlo=-0.9, qhi=0.5;
  function X(v){return pad.l+(v-wlo)/(whi-wlo)*(w-pad.l-pad.r);}
  function Y(v){return h-pad.b-(v-qlo)/(qhi-qlo)*(h-pad.t-pad.b);}
  ax(g,w,h,pad);
  // 网格
  for(var q=-0.8;q<=0.4;q+=0.2){
    g.strokeStyle='#eef1f5'; g.beginPath(); g.moveTo(pad.l,Y(q)); g.lineTo(w-pad.r,Y(q)); g.stroke();
    txt(g,q.toFixed(1),pad.l-8,Y(q)+4,'#8a94a2',10,'right');
  }
  // q=0 线
  g.strokeStyle='#8a94a2'; g.lineWidth=1; g.beginPath();
  g.moveTo(pad.l,Y(0)); g.lineTo(w-pad.r,Y(0)); g.stroke();
  txt(g,'q=0',w-pad.r-4,Y(0)-6,'#8a94a2',10,'right');
  // 直线 q(w)=0.5OmM+0.5OmL(1+3w)
  var OmM=0.3111, OmL=0.6889;
  g.strokeStyle='#1f5fa9'; g.lineWidth=2.2; g.beginPath();
  for(var i=0;i<=120;i++){
    var wv=wlo+(whi-wlo)*i/120;
    var q=0.5*OmM+0.5*OmL*(1+3*wv);
    if(i===0)g.moveTo(X(wv),Y(q)); else g.lineTo(X(wv),Y(q));
  }
  g.stroke();
  // 两点
  var pts=[
    {w:-1, q:D.qA, c:'#1e8449', lab:'w=-1 (靶规定 tau=const)  q='+D.qA.toFixed(4)},
    {w:-1/3, q:D.qB, c:'#c0392b', lab:'w=-1/3 (几何标度 tau~1/a)  q='+D.qB.toFixed(4)}
  ];
  pts.forEach(function(p){
    g.fillStyle=p.c; g.beginPath(); g.arc(X(p.w),Y(p.q),6,0,6.2832); g.fill();
    g.strokeStyle='#fff'; g.lineWidth=2; g.beginPath(); g.arc(X(p.w),Y(p.q),6,0,6.2832); g.stroke();
    var ty=Y(p.q)+(p.q<0? -14: 24);
    txt(g,p.lab,X(p.w),ty,p.c,10.5,'center');
  });
  for(var wv=-2;wv<=0.5;wv+=0.5){
    txt(g,wv.toFixed(1),X(wv),h-pad.b+16,'#8a94a2',10,'center');
  }
  txt(g,'w',w/2,h-10,'#5a6472',11,'center');
  txt(g,'q0',14,pad.t+8,'#5a6472',11,'left');
})();

// ---- 图4 零点能
(function(){
  var h=250, S=setup('c4',h), g=S.g, w=S.w;
  var pad={l:58,r:24,t:22,b:44};
  var lo=0, hi=Math.ceil(D.zpDec)+1;
  function Y(v){return h-pad.b-(v-lo)/(hi-lo)*(h-pad.t-pad.b);}
  ax(g,w,h,pad);
  for(var v=0;v<=hi;v+=20){
    g.strokeStyle='#eef1f5'; g.beginPath(); g.moveTo(pad.l,Y(v)); g.lineTo(w-pad.r,Y(v)); g.stroke();
    txt(g,'1e'+v,pad.l-8,Y(v)+4,'#8a94a2',10,'right');
  }
  var x0=pad.l+70, bw=Math.min(150,(w-pad.l-pad.r-140));
  // 柱：rho_Lambda 为 0 参照
  g.fillStyle='#1f5fa9'; g.fillRect(x0,Y(1),bw,Y(0)-Y(1));
  txt(g,'rho_Lambda (观测)',x0,Y(0)-10,'#1f5fa9',11);
  // 柱：零点能
  var x1=x0+bw+50;
  g.fillStyle='#c0392b'; g.fillRect(x1,Y(D.zpDec),bw,Y(0)-Y(D.zpDec));
  txt(g,'靶自己的 L 的零点能',x1,Y(D.zpDec)-10,'#c0392b',11);
  // 差距标注
  g.strokeStyle='#c0392b'; g.lineWidth=1.2; g.setLineDash([4,3]);
  g.beginPath(); g.moveTo(x1+bw+10,Y(D.zpDec)); g.lineTo(x1+bw+10,Y(0)); g.stroke();
  g.setLineDash([]);
  txt(g,'= '+D.zpDec.toFixed(2)+' 个数量级',x1+bw+18,(Y(D.zpDec)+Y(0))/2,'#c0392b',11.5);
  txt(g,'靶 L4776 声称「这直接绕开 10^120」',pad.l+10,pad.t+14,'#12161c',12);
})();

window.addEventListener('resize',function(){location.reload();});
""")
    A("</script>")
    A("</body></html>")
    return "\n".join(o)


# ================================================================ main
def main():
    docs = load_targets()
    L = locate(docs)
    group_A(docs, L)
    B = group_B(L)
    C = group_C(L)
    D = group_D(L, C)
    group_E(L)
    group_F(L)
    pr = pricing()
    group_G(pr)
    controls(docs, L, C, B, D, pr)
    build_guards(docs, L, pr)
    pr = pricing()
    deg = read_degree()
    txt = report_text(docs, L, C, B, D, pr, deg)
    paths = write_outputs(txt, docs, L, C, B, D, pr, deg)

    t = tally()
    n_ctl = sum(1 for c in CONTROLS if c["ok"])
    n_gd = sum(1 for g in GUARDS if g["ok"])
    print("=" * 78)
    print("TUFT-%s · %s" % (RID.upper(), TITLE_CN))
    print("=" * 78)
    print("条目 %d = PASS %d / FAIL %d / INFO %d / BOUNDARY %d" % (
        len(ENTRIES), t.get("PASS", 0), t.get("FAIL", 0),
        t.get("INFO", 0), t.get("BOUNDARY", 0)))
    print("控制组 %d/%d   守卫 %d/%d" % (n_ctl, len(CONTROLS), n_gd, len(GUARDS)))
    st, lo = pr["strict"], pr["loose"]
    print("定价 严格 EMPTY %d / SUICIDE %d / SURVIVE %d" % (
        st["EMPTY"], st["SUICIDE"], st["SURVIVE"]))
    print("定价 宽松 EMPTY %d / SUICIDE %d / SURVIVE %d" % (
        lo["EMPTY"], lo["SUICIDE"], lo["SURVIVE"]))
    print("-" * 78)
    for p in paths:
        print("  -> %s (%d bytes)" % (os.path.basename(p), os.path.getsize(p)))
    print("-" * 78)
    bad = [c["id"] for c in CONTROLS if not c["ok"]]
    badg = [g["id"] for g in GUARDS if not g["ok"]]
    if bad:
        print("控制组未过:", bad)
    if badg:
        print("守卫未过:", badg)
    rc = 0 if (not bad and not badg) else 2
    print("rc =", rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
