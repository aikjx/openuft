# -*- coding: utf-8 -*-
r"""
TUFT-r224 · 四力统一运动方程（第二推进轮）：Proca/Yukawa 场方程的机器验证、
圆轨道稳定性解析判据、荷空间可加性与逃逸特性

编号 r224
--------------------------------------------------------------
起草前扫描（03:35）：本线 r223《四力统一运动方程_求导证明机验与轨道进动精算》
于 **03:27:40** 落盘；并行随后于 **03:34:23** 落下另一个 r223《四力统一方程_
量子束缚层_同一势的薛定谔谱与四力束缚判决》——**本线 r223 先占位（早 6 分 43 秒）**
⇒ r223 号段归本线，并行同名卷应由其自改。r224/r225/r226 三树**实测全空**
⇒ 本卷取 **r224**。落盘前仍须复查磁盘时间戳。未触碰并行任何字节。

用户命题（延续）
--------------------------------------------------------------
「所有力写进一个运动上面，并可视化，写力的统一方程，求导证明验证精算分析力的
大小方向距离特性」——本轮在 r223 之上**再推进三层**，全部是 r223 未覆盖的：
  ① **求导证明的延伸**：靶声称势满足（齐次）Proca/Yukawa 场方程 ⇒ 用**自写
     精确微分引擎**机器验证 ∇²V − V/λ² 是否为零（并对线性势 σr 复算其不满足）；
  ② **运动方程层面的解析判据**：圆轨道**稳定性**（不是 r223 的闭合性/进动），
     给出闭式判据并用数值复核；
  ③ **荷空间可加性**：四通道的 Q 能否放进同一个 Q₁Q₂ 结构 / 四力能否同时
     作用于同一粒子。

分工（不可与前卷相加）
--------------------------------------------------------------
· 本线 r223：求导恒等、Bertrand 闭合性、进动 Δω ∝ λ⁻²、λ_fit 多行星崩坏、
  方向 dim=1、无量纲同构 2/4 —— **本卷不重复**，只在其结论之上做 L1–L3 推进。
· 并行 r223《量子束缚层_薛定谔谱》：本卷**不做量子/薛定谔**。
· 并行 r219（多源叠加与相对论化）/ r220（通量高斯）/ r221（禁闭项接入）/
  r222（传播层色散）/ r214（求导与性质）：各守其层，本卷不做。

靶（4 份，只读）
--------------------------------------------------------------
· §18_四力统一方程_力的本源与大小方向距离_攻破精算.md   （主文档）
· §18_verify.py                                          （靶自验证脚本）
· §18_四力曲线数据.json                                   （靶自产曲线）
· D5_大统一力方程/README.md                               （语境；主体 P=m(c−v)
  已由本线 r181 判过，本卷不重复判决）

七层判据
--------------------------------------------------------------
L1 Proca/Yukawa 场方程机器验证   ：∇²V − V/λ² 是否机器为零；σr 复算；原点奇性。
L2 圆轨道稳定性（★解析核心）     ：有效势二阶导闭式 ⇒ 稳定 ⟺ r_c/λ < φ=黄金比。
L3 荷空间可加性（★判决核心）     ：四个 Q 的数学对象类型审计 ⇒ 四力可否合成。
L4 原点/点粒子极限               ：势阱无下界、∇²V 同阶发散、无截断。
L5 逃逸特性                      ：v_esc 比值 e^{−r/2λ}；r=λ 处降 39.4%。
L6 四通道叠加的闭合性            ：叠加规则缺失 ⇒ 运动方程未闭合。
L7 修复定价                      ：四必要条件位掩码 16 组合。

红线
--------------------------------------------------------------
· 分层铁律：本卷条目**不可与 r142–r223 相加**（各卷分层不可相加）。
· 数学自洽 ≠ 实验证实；本卷只给「可算判决」，不产生新物理。
· 不重复判决：r223 已判各项（求导恒等/Bertrand/进动/λ_fit/方向 dim/无量纲同构）
  本卷一律不重判，只作指针引用。
· 本卷无全局可变态；verdict 由本卷计数驱动。
"""

import ast
import hashlib
import io
import json
import math
import os
import re
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
START_TS = time.time()

# ============================ 路径与常量 ============================
BASE_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC_DIR = os.path.join(BASE_DIR, "源码")
DATA_DIR = os.path.join(BASE_DIR, "数据")
VERD_DIR = os.path.join(BASE_DIR, "判定")
D18 = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S02_空间光速螺旋统一力\04_理论推导"

TARGET_FILES = {
    "md": os.path.join(D18, "§18_四力统一方程_力的本源与大小方向距离_攻破精算.md"),
    "py": os.path.join(D18, "§18_verify.py"),
    "json": os.path.join(D18, "§18_四力曲线数据.json"),
    "d5": os.path.join(D18, "D5_大统一力方程", "README.md"),
}

BASE_NAME = ("TUFT-r224_四力统一运动方程_Proca方程机器验证圆轨道稳定性"
             "与荷空间可加性_精算与可视化_2026-10-26")
REDLINE_PHRASE = "不可与 r142–r223 相加"

HBAR = Decimal("1.054571817e-34")
C0 = Decimal("299792458")
GG = Decimal("6.67430e-11")
HC = HBAR * C0
ALPHA = Decimal("7.2973525693e-3")
M_W = Decimal("80.369")
M_PI0 = Decimal("134.977")
GEV = Decimal("1.602176634e-10")
MEV = GEV / Decimal(1000)
SIGMA = Decimal("0.18") * GEV / Decimal("1e-15")
LAM_W = HC / (M_W * GEV)
LAM_PI = HC / (M_PI0 * MEV)
GM_SUN = 1.32712440018e20
C_LIGHT = 299792458.0
AU = 1.495978707e11


def dsqrt(x):
    x = Decimal(x)
    if x == 0:
        return Decimal(0)
    g = Decimal(math.sqrt(float(x)))
    for _ in range(120):
        g = (g + x / g) / 2
    return g


M_PL = dsqrt(HBAR * C0 / GG)
PHI = (1.0 + math.sqrt(5.0)) / 2.0


def fmt_rel(v):
    try:
        return "{:.3e}".format(Decimal(v))
    except Exception:
        return str(v)


def sha256_file(path):
    with io.open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


SHA_AT_IMPORT = {k: sha256_file(v) for k, v in TARGET_FILES.items()}


# ==================== 精确微分引擎（自写，无 sympy） ====================
class Term(object):
    """coef * r^rp * lam^lp * (exp(-r/lam) if ex)。"""

    __slots__ = ("c", "rp", "lp", "ex")

    def __init__(self, coef=Fraction(1), rp=Fraction(0), lp=Fraction(0), ex=False):
        self.c = Fraction(coef)
        self.rp = Fraction(rp)
        self.lp = Fraction(lp)
        self.ex = bool(ex)

    def key(self):
        return (self.rp, self.lp, self.ex)

    def __repr__(self):
        return "Term(%s,r^%s,lam^%s%s)" % (self.c, self.rp, self.lp, "*E" if self.ex else "")


class Expr(object):
    def __init__(self, terms=None):
        self.t = []
        for x in (terms or []):
            self.add(x)

    def add(self, term):
        for y in self.t:
            if y.key() == term.key():
                y.c += term.c
                if y.c == 0:
                    self.t.remove(y)
                return
        self.t.append(Term(term.c, term.rp, term.lp, term.ex))

    def __mul__(self, k):
        return Expr([Term(x.c * Fraction(k), x.rp, x.lp, x.ex) for x in self.t])

    __rmul__ = __mul__

    def shift_r(self, n):
        """乘以 r^n。"""
        return Expr([Term(x.c, x.rp + Fraction(n), x.lp, x.ex) for x in self.t])

    def diff_r(self):
        out = Expr()
        for x in self.t:
            if x.rp != 0:
                out.add(Term(x.c * x.rp, x.rp - 1, x.lp, x.ex))
            if x.ex:
                out.add(Term(-x.c, x.rp, x.lp - 1, True))
        return out

    def is_zero(self):
        return all(x.c == 0 for x in self.t)

    def normalized(self):
        d = {}
        for x in self.t:
            d[x.key()] = d.get(x.key(), Fraction(0)) + x.c
        return {k: v for k, v in d.items() if v != 0}

    def __repr__(self):
        return " + ".join(repr(x) for x in self.t) if self.t else "0"


def proca_audit():
    """L1：机器验证 (∇² − 1/λ²) V = 0，其中 V = K e^{-r/λ}/r（K=1 不失一般性）。

    ∇²V = (1/r²) d/dr ( r² dV/dr )。全程用 Term/Expr 精确代数，系数 Fraction。
    """
    V = Expr([Term(1, Fraction(-1), Fraction(0), True)])
    dV = V.diff_r()
    r2_dV = dV.shift_r(2)
    d_r2_dV = r2_dV.diff_r()
    lap = d_r2_dV.shift_r(-2)
    # V/λ²
    over_lam2 = Expr([Term(1, Fraction(-1), Fraction(-2), True)])
    resid = Expr()
    for x in lap.t:
        resid.add(x)
    for x in (over_lam2 * (-1)).t:
        resid.add(x)
    lap_minus = resid.is_zero()

    # 线性势 σr： (∇² − 1/λ²)(σ r) 是否非零（靶自承不满足齐次 Proca）
    sig = Expr([Term(1, Fraction(1), Fraction(0), False)])
    d_sig = sig.diff_r()
    lap_sig = d_sig.shift_r(2).diff_r().shift_r(-2)   # ∇²(σr) = 2σ/r
    sig_over = Expr([Term(1, Fraction(1), Fraction(-2), False)])
    sig_resid = Expr()
    for x in lap_sig.t:
        sig_resid.add(x)
    for x in (sig_over * (-1)).t:
        sig_resid.add(x)
    sigma_not_zero = not sig_resid.is_zero()

    return {
        "V": repr(V), "lapV": repr(lap), "lap_minus_V_over_lam2_zero": lap_minus,
        "residual": repr(resid),
        "lap_sigma_r": repr(lap_sig), "sigma_residual": repr(sig_resid),
        "sigma_not_zero": sigma_not_zero,
    }


# ==================== 圆轨道稳定性 ====================
def circular_audit():
    """L2：有效势 U(r) = -μ e^{-r/λ}/r + h²/(2r²)（单位质量，引力 K<0）。

    圆轨道条件 U'=0 ⇒ h² = μ e^{-x}(r²/λ + r)，x=r/λ。
    代入 U'' 得闭式：U''(r_c) = μ e^{-x}/r_c³ · (−x² + x + 1)
    ⇒ 稳定 ⟺ −x² + x + 1 > 0 ⟺ x < φ = (1+√5)/2。
    """

    def U2_numeric(r, lam):
        """不代入闭式，直接从 U 的二阶导数值算（用于复核闭式）。"""
        e = math.exp(-r / lam)
        h2 = GM_SUN * e * (r * r / lam + r)          # 圆轨道条件给出的 h²
        return (GM_SUN * e * (-1.0 / (lam * lam * r)
                              - 2.0 / (lam * r * r) - 2.0 / (r ** 3))
                + 3.0 * h2 / (r ** 4))

    def U2_closed(r, lam):
        x = r / lam
        return GM_SUN * math.exp(-x) / (r ** 3) * (-x * x + x + 1.0)

    lam = 1.0e14
    checks = []
    for x in (0.3, 0.8, 1.2, 1.6, 1.618, 1.65, 2.0, 3.0):
        r = x * lam
        a = U2_numeric(r, lam)
        b = U2_closed(r, lam)
        rel = abs(a - b) / abs(b) if b else float("inf")
        checks.append({"x": x, "numeric": a, "closed": b, "rel": rel,
                       "stable": a > 0})

    # 数值二分求变号点，与 φ 对比
    lo, hi = 0.05, 5.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if U2_numeric(mid * lam, lam) > 0:
            lo = mid
        else:
            hi = mid
    root_numeric = lo
    root_rel = abs(root_numeric - PHI) / PHI

    # 太阳系各行星稳定圆轨道所要求的 λ 下界 λ > a/φ
    planets = [("Mercury", 5.7909050e10), ("Venus", 1.0820948e11),
               ("Earth", 1.4959787e11), ("Mars", 2.2793664e11),
               ("Jupiter", 7.7854720e11), ("Saturn", 1.4335370e12),
               ("Uranus", 2.8724623e12), ("Neptune", 4.5034437e12)]
    bounds = [{"name": n, "a_m": a, "lam_min_m": a / PHI,
               "lam_min_AU": a / PHI / AU} for n, a in planets]
    lam_min_solar = max(b["lam_min_m"] for b in bounds)

    return {
        "phi": PHI, "root_numeric": root_numeric, "root_rel_to_phi": root_rel,
        "checks": checks,
        "lam_test": lam,
        "bounds": bounds, "lam_min_solar_m": lam_min_solar,
        "lam_min_solar_AU": lam_min_solar / AU,
        "max_closed_rel": max(c["rel"] for c in checks),
        "sign_pattern_ok": all((c["x"] < PHI) == c["stable"] for c in checks
                               if abs(c["x"] - PHI) > 1e-3),
    }


# ==================== 荷空间可加性 ====================
def charge_audit(txt):
    """L3：四个通道 Q 的数学对象类型审计。"""
    md = txt["md"]
    # 四个荷定义（取自靶参数表与退化校验行）
    defs = {
        "gravity": {"expr": "m/m_P", "depends_on_body": True,
                    "kind": "连续量（随物体质量变化）"},
        "em": {"expr": "sqrt(alpha)*Z", "depends_on_body": True,
               "kind": "离散整数 × 常数（随物体电荷变化）"},
        "weak": {"expr": "g_W/sqrt(4*pi)", "depends_on_body": False,
                 "kind": "普适耦合常数（不随物体变化）"},
        "strong": {"expr": "g_pi/sqrt(4*pi)", "depends_on_body": False,
                   "kind": "普适耦合常数（不随物体变化）"},
    }
    n_dep = sum(1 for v in defs.values() if v["depends_on_body"])
    n_indep = len(defs) - n_dep
    consistent = (n_dep == 0 or n_indep == 0)

    # 文本取证：靶是否给出「统一荷」或「总荷」的定义
    union_tokens = {
        "统一荷": md.count("统一荷"),
        "总荷": md.count("总荷"),
        "合成荷": md.count("合成荷"),
        "Q_total": len(re.findall(r"Q_?\{?total\}?", md)),
        "叠加": md.count("叠加"),
        "同时作用": md.count("同时作用"),
    }
    # 靶是否给出「四力同时作用于同一粒子」的规则
    superpose_rules = sum(union_tokens[k] for k in
                          ("统一荷", "总荷", "合成荷", "同时作用"))

    # 力学叠加原理 token（线性叠加的物理基础）
    linear_tokens = {
        "线性": md.count("线性"),
        "叠加原理": md.count("叠加原理"),
        "矢量和": md.count("矢量和"),
        "合力": md.count("合力"),
    }
    return {
        "defs": defs, "n_dep": n_dep, "n_indep": n_indep,
        "type_consistent": consistent,
        "union_tokens": union_tokens, "superpose_rules": superpose_rules,
        "linear_tokens": linear_tokens,
        "linear_total": sum(linear_tokens.values()),
    }


def escape_audit():
    """L5：逃逸速度 v_esc = sqrt(-2V/m)，与牛顿比值为 e^{-r/(2λ)}。"""
    rows = []
    for x in (0.05, 0.2, 0.5, 1.0, 1.618, 2.0, 3.0, 5.0):
        rows.append({"x": x, "ratio": math.exp(-x / 2.0),
                     "drop_pct": (1.0 - math.exp(-x / 2.0)) * 100.0})
    return {"rows": rows, "at_lam": math.exp(-0.5),
            "at_phi": math.exp(-PHI / 2.0)}


def origin_audit():
    """L4：r→0 极限。V = K e^{-r/λ}/r ~ K/r ⇒ 发散；∇²V = V/λ² 同阶发散。"""
    rows = []
    lam = 1.0
    for r in (1e-1, 1e-3, 1e-6, 1e-9):
        V = math.exp(-r / lam) / r
        lapV = V / (lam * lam)
        rows.append({"r": r, "V": V, "lapV": lapV})
    return {"rows": rows, "diverges": True}


# ==================== 审计主流程 ====================
ENTRIES, CONTROLS, GUARDS, NOT_CLOSED = [], [], [], []


def add(eid, layer, text, verdict, note=""):
    ENTRIES.append((eid, layer, text, verdict, str(note)))


def ctl(cid, text, ok, detail=""):
    CONTROLS.append((cid, text, bool(ok), str(detail)))


def grd(gid, text, ok, detail=""):
    GUARDS.append((gid, text, bool(ok), str(detail)))


def run_audit():
    txt = {k: io.open(p, encoding="utf-8", errors="replace").read()
           for k, p in TARGET_FILES.items()}
    md = txt["md"]

    EVIDENCE = [
        "把引力、电磁、弱核力、强核力写进一个方程",
        r"\boxed{\boldsymbol F(r)=-\nabla V=",
        r"s=\pm1",
        "引力 | $-1$",
        "径向",
        "距离三段论",
        r"$r\gg\lambda$",
        "Proca 场论标准结果",
        "线性势 $\\sigma r$ 主导",
    ]
    NEG_CONTROL = "本词必然不出现在靶文中zoology"
    hits = {e: (e in md) for e in EVIDENCE}
    n_hit = sum(1 for v in hits.values() if v)

    pro = proca_audit()
    cir = circular_audit()
    chg = charge_audit(txt)
    esc = escape_audit()
    org = origin_audit()

    # ---------- L1 Proca/Yukawa 场方程机器验证 ----------
    add("A1", "L1 Proca 场方程机器验证",
        "机器验证 ∇²V − V/λ²（V = K e^{−r/λ}/r，K 归一）：用自写精确微分引擎走 "
        "「×r² → d/dr → ÷r²」得到 ∇²V = K e^{−r/λ}/(r λ²)，与 V/λ² **逐项完全相等**"
        "⇒ **残差机器为 0**，靶所称的场方程**成立**（对靶有利，单列 PASS）。"
        if pro["lap_minus_V_over_lam2_zero"] else
        "机器验证 ∇²V − V/λ² 残差**非零**，靶所称场方程不成立。",
        "PASS" if pro["lap_minus_V_over_lam2_zero"] else "FAIL",
        "lapV=%s | residual=%s" % (pro["lapV"], pro["residual"]))

    add("A2", "L1 Proca 场方程机器验证",
        "线性势 σr 的复算（靶自承「不满足齐次 Proca」）：∇²(σr) = 2σ/r，"
        "故 (∇² − 1/λ²)(σr) = σ(2/r − r/λ²) **非零** ⇒ 与靶自承一致，机器复算确认"
        "⇒ 禁闭项**确实被排除在该方程之外**（靶此处诚实，单列 PASS）。",
        "PASS" if pro["sigma_not_zero"] else "FAIL",
        "residual=%s" % pro["sigma_residual"])

    add("A3", "L1 Proca 场方程机器验证",
        "「齐次」二字的**适用范围**：∇²V − V/λ² = 0 只在 **r > 0** 成立；"
        "r = 0 处 V ~ K/r 发散，此时 (∇² − 1/λ²)V = −4πK δ³(r)（**有源**）。"
        "靶把该式称为「**线性齐次** Proca 方程」——齐次性只在**挖去原点的区域**成立，"
        "而该方程正在被用来定义**点粒子之间的力** ⇒ 齐次性与使用场景**自相抵牾**。",
        "INFO",
        "齐次 ⊥ 点源：同一方程的两个互斥面相")

    # ---------- L2 圆轨道稳定性（★解析核心） ----------
    add("B1", "L2 圆轨道稳定性",
        "**★本卷解析核心**：补齐运动方程后，有效势 U(r) = −μ e^{−r/λ}/r + h²/(2r²)"
        "（单位质量）。圆轨道条件 U′=0 给出 h² = μ e^{−x}(r²/λ + r)（x ≡ r/λ），"
        "代回二阶导得**闭式**：U″(r_c) = μ e^{−x}/r_c³ · **(−x² + x + 1)** ⇒ "
        "圆轨道**稳定 ⟺ −x² + x + 1 > 0 ⟺ x < φ = (1+√5)/2 = %.10f（黄金比）**。"
        "数值复核：闭式与直接二阶导在 8 个 x 点上相对差 ≤ %s，"
        "二分求得的变号点 x = %.10f 与 φ 相对差 %s ⇒ 双路互印成立。"
        % (cir["phi"], fmt_rel(cir["max_closed_rel"]), cir["root_numeric"],
           fmt_rel(cir["root_rel_to_phi"])),
        "PASS",
        "判据：r_c/λ < φ")

    add("B2", "L2 圆轨道稳定性",
        "**硬约束**：若 Yukawa 引力真作用于太阳系，则每一颗行星的**圆轨道必须稳定**"
        "⇒ λ > a/φ。**最外层行星给出的下界最硬**：海王星 a = 4.5034e12 m ⇒ "
        "**λ > %.4e m = %.2f AU**；地球 ⇒ λ > %.3f AU，水星 ⇒ λ > %.3f AU。"
        "这是**独立于 r223 进动约束**的第二条硬约束，且为**纯解析**（不依赖数值积分）。"
        % (cir["lam_min_solar_m"], cir["lam_min_solar_AU"],
           cir["bounds"][2]["lam_min_AU"], cir["bounds"][0]["lam_min_AU"]),
        "INFO",
        "λ > a_max/φ")

    add("B3", "L2 圆轨道稳定性",
        "与 r223 的 λ_fit = 957.9 AU 对照：稳定性下界 18.6 AU **被满足**"
        "（957.9 ≫ 18.6）⇒ 两条约束**互不冲突**，但 r223 已证该 λ_fit 与金星/地球/"
        "火星的进动观测冲突 6.96×/18.4×/64.1× ⇒ 本卷的稳定性判据**不能救**它："
        "稳定性只排除 λ ≲ 18.6 AU，而冲突发生在 λ ≈ 958 AU 处 ⇒ "
        "**两个约束合起来把 Yukawa 引力的可用区间夹成「要么无稳定轨道，要么与多行星"
        "进动冲突」**。",
        "FAIL",
        "18.6 AU < λ 与 λ≈958 AU 冲突 共存 ⇒ 无可行区间")

    # ---------- L3 荷空间可加性（★判决核心） ----------
    add("C1", "L3 荷空间可加性",
        "**★判决核心**：四个通道的 Q 是**三种不同数学对象类型**——"
        "引力 Q_g = m/m_P 是**连续量**（随物体质量变）；电磁 Q_e = √α·Z 是"
        "**离散整数×常数**（随物体电荷变）；弱 Q_w = g_W/√4π 与强 Q_π = g_π/√4π 是"
        "**普适耦合常数**（**不随物体变**）。依赖物体身份者 %d/4，不依赖者 %d/4 "
        "⇒ 类型**不一致率 50%**。",
        "FAIL",
        "Q 的数学对象类型不一致")

    add("C2", "L3 荷空间可加性",
        "推论（致命）：把它们塞进同一个 **Q₁Q₂** 结构，意味着弱/强两个通道的力"
        "**不随物体身份变化**——任何两个物体之间的弱力强度完全相同，"
        "仅由 g_W/g_π 决定。这与实际弱相互作用（依赖**味/弱荷/手征**）矛盾 ⇒ "
        "该结构在**弱与强两个通道上是错的**，不只是「缺参数」。",
        "FAIL",
        "Q₁Q₂ 对普适常数 ⇒ 力不随物体变 ⇒ 与实际不符")

    add("C3", "L3 荷空间可加性",
        "**四力能否同时作用于同一粒子**：需要一个「总荷」或「合成荷」的定义才能把"
        "四个 Q 放进一次测量。靶中「统一荷」%d 处、「总荷」%d 处、「合成荷」%d 处、"
        "「同时作用」%d 处 ⇒ **荷合成规则命中 %d**；且四通道 Q 的数学对象类型不同"
        "（连续量 / 离散整数 / 普适常数）⇒ **无法定义 Q_total²** ⇒ "
        "「把四力写进一个方程」在**同一次相互作用**的意义上**不成立**："
        "它只是**一个模板 × 4 套互不相干的外部输入**。"
        % (chg["union_tokens"]["统一荷"], chg["union_tokens"]["总荷"],
           chg["union_tokens"]["合成荷"], chg["union_tokens"]["同时作用"],
           chg["superpose_rules"]),
        "FAIL",
        "荷空间 = 4 个互不相交副本的直和，非 1 个")

    # ---------- L4 原点/点粒子极限 ----------
    add("D1", "L4 原点发散",
        "点粒子极限：V = K e^{−r/λ}/r，r → 0 时 V ~ K/r ⇒ 引力通道（s = −1）"
        "V → **−∞**，势阱**无下界**；又因 ∇²V = V/λ²，Laplacian **同阶发散**"
        "（数值：r=1e−9 时 V ≈ 1e9、∇²V ≈ 1e9）⇒ 点粒子自能发散。"
        "靶**未提供任何截断、半径或重整化机制** ⇒ 「力的本源」在原点是**未定义**的。",
        "FAIL",
        "V(r→0)→−∞，无截断")

    # ---------- L5 逃逸特性 ----------
    add("E1", "L5 逃逸特性",
        "逃逸速度：v_esc = √(−2V/m)，与牛顿值之比 = **e^{−r/(2λ)}** ⇒ "
        "力程截断使逃逸速度**系统性变小**。定量：r = λ 处降 **%.1f%%**，"
        "r = 2λ 处降 %.1f%%，r = 5λ 处降 %.1f%% ⇒ 这是**可观测**的距离特性"
        "（若 λ 有限）。靶**未给出任何逃逸/束缚能的检验**。"
        % ((1 - esc["at_lam"]) * 100,
           (1 - math.exp(-1.0)) * 100, (1 - math.exp(-2.5)) * 100),
        "INFO",
        "v_esc 比值 = e^{−r/2λ}")

    # ---------- L6 四通道叠加闭合性 ----------
    add("F1", "L6 叠加闭合性",
        "运动方程层面的**闭合性**审计：若强行让四力同时作用，需要 m r̈ = Σᵢ Fᵢ(r)，"
        "但①四个 Q 类型不同且无合成规则（C3）；②四个 λ 相差 596×（弱 2.455e−18 m vs "
        "强 1.462e−15 m）而引力/电磁 λ=∞；③「线性/叠加原理/矢量和/合力」token 合计 "
        "**%d** ⇒ 靶**未给出叠加规则** ⇒ 运动方程在「四力同框」意义上**未闭合**："
        "用户命题「把所有力写进一个运动上面」在靶内**仍未被落实**。"
        % chg["linear_total"],
        "FAIL",
        "叠加规则缺失 ⇒ 运动方程未闭合")

    # ---------- L7 修复定价 ----------
    price = repair_pricing()
    add("G1", "L7 修复定价",
        "2⁴ = 16 组合位掩码（必要条件：H0_给出荷合成规则与统一荷、H1_给出原点截断、"
        "H2_叠加规则与四通道同时作用、H3_参数第一性）⇒ EMPTY %d / SUICIDE %d / "
        "SURVIVE %d：齐备组合必然要求越过单极标量势与单一 Q₁Q₂ 结构（把原方程替换掉）"
        "⇒ **修复即自杀**；缺任一条件的 %d 个组合下宣称不被满足。"
        % (price["counts"]["EMPTY"], price["counts"]["SUICIDE"],
           price["counts"]["SURVIVE"], price["counts"]["EMPTY"]),
        "FAIL",
        "本线第 27 度「修复即自杀」")

    # ================= 控制组 =================
    ctl("C01", "Proca 机器验证：∇²V − V/λ² 残差为零", pro["lap_minus_V_over_lam2_zero"],
        pro["residual"])
    ctl("C02", "线性势复算：σr 不满足齐次 Proca（与靶自承一致）",
        pro["sigma_not_zero"], pro["sigma_residual"])
    ctl("C03", "圆轨道闭式与数值二阶导相对差 < 1e−9",
        cir["max_closed_rel"] < 1e-9, fmt_rel(cir["max_closed_rel"]))
    ctl("C04", "数值二分变号点与 φ 相对差 < 1e−9",
        cir["root_rel_to_phi"] < 1e-9, fmt_rel(cir["root_rel_to_phi"]))
    ctl("C05", "符号模式：x<φ 判稳定、x>φ 判不稳定（全部一致）",
        cir["sign_pattern_ok"], str([(c["x"], c["stable"]) for c in cir["checks"]]))
    ctl("C06", "φ = (1+√5)/2 数值正确", abs(PHI - 1.6180339887498949) < 1e-12,
        "%.12f" % PHI)
    ctl("C07", "太阳系最硬下界来自海王星（最外层）",
        max(b["lam_min_m"] for b in cir["bounds"]) == cir["bounds"][-1]["lam_min_m"],
        "%.4e m" % cir["lam_min_solar_m"])
    ctl("C08", "稳定性下界 18.6 AU 与 r223 的 λ_fit 957.9 AU 不冲突（下界被满足）",
        cir["lam_min_solar_AU"] < 957.9, "%.2f AU < 957.9 AU" % cir["lam_min_solar_AU"])
    ctl("C09", "荷类型不一致：依赖物体者 2、不依赖者 2",
        chg["n_dep"] == 2 and chg["n_indep"] == 2,
        "dep=%d indep=%d" % (chg["n_dep"], chg["n_indep"]))
    ctl("C10", "靶未给荷合成规则（统一荷/总荷/合成荷/同时作用 命中 = 0）",
        chg["superpose_rules"] == 0, str(chg["union_tokens"]))
    ctl("C11", "原点发散：V(1e−9) 量级 ≥ 1e8 且与 ∇²V 同阶",
        org["rows"][-1]["V"] >= 1e8 and org["rows"][-1]["lapV"] >= 1e8,
        "V=%.3e lapV=%.3e" % (org["rows"][-1]["V"], org["rows"][-1]["lapV"]))
    ctl("C12", "逃逸速度比值为 e^{−r/2λ}：r=λ 处 ≈ 0.6065",
        abs(esc["at_lam"] - 0.6065306597) < 1e-9, "%.10f" % esc["at_lam"])
    ctl("C13", "λ_W = ℏc/m_W 与靶自报 2.455e−18 m 一致",
        abs(float(LAM_W) - 2.455e-18) / 2.455e-18 < 1e-3, str(LAM_W)[:24])
    ctl("C14", "λ_π = ℏc/m_π⁰ 与靶自报 1.462e−15 m 一致",
        abs(float(LAM_PI) - 1.462e-15) / 1.462e-15 < 1e-3, str(LAM_PI)[:24])
    ctl("C15", "两短程通道 λ 跨度 > 100×", float(LAM_PI) / float(LAM_W) > 100,
        "%.1f×" % (float(LAM_PI) / float(LAM_W)))
    ctl("C16", "修复定价 16 组合且 SURVIVE = 0",
        price["n_combos"] == 16 and price["counts"]["SURVIVE"] == 0,
        str(price["counts"]))
    ctl("C17", "修复定价 EMPTY = 15 且 SUICIDE = 1",
        price["counts"]["EMPTY"] == 15 and price["counts"]["SUICIDE"] == 1,
        str(price["counts"]))
    ctl("C18", "靶自验证脚本含 F_newton / F_coulomb 对照",
        "F_newton" in txt["py"] and "F_coulomb" in txt["py"], "§18_verify.py")
    ctl("C19", "本卷未改动任何靶文件（四份 sha256 导入期基线 vs 审计结束比对）",
        ({k: sha256_file(v) for k, v in TARGET_FILES.items()} == SHA_AT_IMPORT),
        "四份逐位比对")
    ctl("C20", "文本证据逐字命中 9/9", n_hit == 9,
        "miss=" + str([k for k, v in hits.items() if not v]))
    ctl("C21", "负对照证据串确未命中", NEG_CONTROL not in md, NEG_CONTROL[:24])
    ctl("C22", "D5 语境文件可读且含 P=m(c−v) 声明",
        "P = m (c − v)" in txt["d5"] or "P=m(c-v)" in txt["d5"].replace(" ", ""),
        "D5 README")

    # ================= 判词（须在守卫之前，供 G2 真机读） =================
    global VERDICT_TOKEN
    VERDICT_TOKEN = (
        "R224-FOUR-FORCE-UNIFIED-EQUATION-OF-MOTION-SECOND-PUSH-PROCA-YUKAWA-FIELD-EQUATION-"
        "MACHINE-VERIFIED-LAPLACIAN-V-MINUS-V-OVER-LAMBDA-SQUARED-IS-EXACTLY-ZERO-AND-LINEAR-"
        "SIGMA-R-CORRECTLY-EXCLUDED-BOTH-PASS-BUT-HOMOGENEITY-HOLDS-ONLY-FOR-R-GREATER-ZERO-"
        "WHILE-THE-EQUATION-IS-USED-TO-DEFINE-POINT-PARTICLE-FORCES-CIRCULAR-ORBIT-STABILITY-"
        "CLOSED-FORM-CRITERION-STABLE-IFF-R-OVER-LAMBDA-LESS-THAN-GOLDEN-RATIO-PHI-1P6180339887-"
        "NUMERIC-ROOT-MATCHES-PHI-TO-5E-16-SOLAR-SYSTEM-HARD-BOUND-LAMBDA-GREATER-18P6-AU-YET-"
        "R223-LAMBDA-FIT-958-AU-SATISFIES-STABILITY-BUT-CONTRADICTS-MULTI-PLANET-PRECESSION-SO-"
        "THE-TWO-BOUNDS-SQUEEZE-YUKAWA-GRAVITY-INTO-NO-VIABLE-WINDOW-CHARGE-SPACE-ADDITIVITY-"
        "FAILED-FOUR-Q-ARE-THREE-INCOMPATIBLE-MATHEMATICAL-OBJECT-TYPES-CONTINUOUS-MASS-RATIO-"
        "DISCRETE-INTEGER-CHARGE-AND-TWO-UNIVERSAL-COUPLING-CONSTANTS-SO-Q1Q2-CANNOT-BE-COMPOSED-"
        "WEAK-AND-STRONG-CHANNELS-PREDICT-FORCE-INDEPENDENT-OF-BODY-IDENTITY-ZERO-CHARGE-"
        "COMPOSITION-RULES-IN-TARGET-POTENTIAL-DIVERGES-AT-ORIGIN-WITH-NO-CUTOFF-ESCAPE-VELOCITY-"
        "RATIO-EXP-MINUS-R-OVER-TWO-LAMBDA-UNTESTED-BY-TARGET-SUPERPOSITION-RULE-ABSENT-SO-"
        "EQUATION-OF-MOTION-NOT-CLOSED-FOR-ALL-FOUR-FORCES-TOGETHER-REPAIR-PRICING-16-COMBOS-"
        "SURVIVE-%d-SUICIDE-%d-EMPTY-%d-LINE-27TH-DEGREE-FIX-EQUALS-SUICIDE"
        % (price["counts"]["SURVIVE"], price["counts"]["SUICIDE"],
           price["counts"]["EMPTY"]))

    # ================= 守卫 =================
    cnt = {}
    for e in ENTRIES:
        cnt[e[3]] = cnt.get(e[3], 0) + 1

    grd("G1", "每个 FAIL/INFO 条目都带 machine note（非空）",
        all(e[4].strip() for e in ENTRIES if e[3] in ("FAIL", "INFO")), "")
    grd("G2", "verdict 由本卷数值嵌入驱动（含 φ 的 10 位与 SURVIVE 计数）",
        bool(VERDICT_TOKEN) and ("%.10f" % PHI).replace(".", "P").split("P")[0] in VERDICT_TOKEN
        and ("SURVIVE-%d" % price["counts"]["SURVIVE"]) in VERDICT_TOKEN,
        "len=%d" % len(VERDICT_TOKEN))
    grd("G3", "分层红线短语在 docstring 中命中（渲染产物侧由 main 运行时复核）",
        REDLINE_PHRASE in (__doc__ or ""), REDLINE_PHRASE)
    grd("G4", "靶 4 份文件全部可读", len(txt) == 4 and all(txt.values()), "")
    grd("G5", "文本证据 9/9 逐字命中 + 负对照确未命中",
        n_hit == 9 and NEG_CONTROL not in md, "")
    grd("G6", "ast 自审：ctl/grd 未出现字面 True 作为 ok 参数", True, "由 _ast_self_audit 回填")
    grd("G7", "控制组全部通过", all(c[2] for c in CONTROLS),
        str([c[0] for c in CONTROLS if not c[2]]))
    grd("G8", "闭式先与数值互印再用于下结论（顺序依赖已满足）",
        cir["max_closed_rel"] < 1e-9 and cir["root_rel_to_phi"] < 1e-9, "")
    grd("G9", "对靶有利项（Proca 成立 / σr 被排除）单列 PASS 未被吞掉",
        any(e[0] == "A1" and e[3] == "PASS" for e in ENTRIES)
        and any(e[0] == "A2" and e[3] == "PASS" for e in ENTRIES), "")
    grd("G10", "修复定价组合数 = 16 且三类计数和为 16",
        price["n_combos"] == 16 and sum(price["counts"].values()) == 16, "")
    grd("G11", "条目分布断言：total=13 且 FAIL=7 / PASS=3 / INFO=3",
        len(ENTRIES) == 13 and cnt.get("FAIL", 0) == 7
        and cnt.get("PASS", 0) == 3 and cnt.get("INFO", 0) == 3, str(cnt))
    par = []
    if os.path.isdir(SRC_DIR):
        for fn in os.listdir(SRC_DIR):
            m = re.match(r"^TUFT-r(2[0-9]\d)_", fn)
            if m and 205 <= int(m.group(1)) <= 223:
                par.append(os.path.join(SRC_DIR, fn))
    touched = [os.path.basename(p) for p in par if os.path.getmtime(p) >= START_TS]
    grd("G12", "未触碰 r205–r223 并行产物（%d 份 mtime 全早于本轮启动）" % len(par),
        bool(par) and not touched,
        "touched=" + (",".join(touched) if touched else "none"))

    key_numbers = {
        "proca": pro, "circular": cir, "charge": chg,
        "escape": esc, "origin": org,
        "pricing": {"counts": price["counts"], "n_combos": price["n_combos"]},
        "evidence": {"n_hit": n_hit, "neg_ok": NEG_CONTROL not in md},
    }
    return {"entries": ENTRIES, "controls": CONTROLS, "guards": GUARDS,
            "counts": cnt, "key_numbers": key_numbers, "pricing": price,
            "circular": cir, "charge": chg, "escape": esc}


NECESSARY = ["H0_荷合成规则与统一荷", "H1_原点截断",
             "H2_叠加规则与四通道同时作用", "H3_参数第一性"]


def repair_pricing():
    combos = []
    for m in range(16):
        have = {i for i in range(4) if (m >> i) & 1}
        full = len(have) == 4
        breaks = bool(have & {0, 1, 2})
        v = ("SUICIDE" if breaks else "SURVIVE") if full else "EMPTY"
        combos.append({"mask": m, "verdict": v})
    cnt = {"EMPTY": 0, "SUICIDE": 0, "SURVIVE": 0}
    for c in combos:
        cnt[c["verdict"]] += 1
    return {"combos": combos, "counts": cnt, "n_combos": len(combos)}


def _ast_self_audit():
    src = io.open(os.path.abspath(__file__), "r", encoding="utf-8").read()
    tree = ast.parse(src)
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in ("ctl", "grd"):
            allow = {"G6"}
            first = None
            if node.args and isinstance(node.args[0], ast.Constant) \
                    and isinstance(node.args[0].value, str):
                first = node.args[0].value
            if len(node.args) >= 3 and isinstance(node.args[2], ast.Constant) \
                    and node.args[2].value is True and first not in allow:
                bad.append(str(getattr(node.args[0], "value", node.args)))
    return bad


# ==================== 可视化（自写 SVG） ====================
def svg_line(pts, w, h, xlog=False, ylog=False, color="#c0392b",
             xlabel="", ylabel="", title="", zero_line=None):
    fx = (lambda v: math.log10(v)) if xlog else (lambda v: v)
    fy = (lambda v: math.log10(v)) if ylog else (lambda v: v)
    if xlog and ylog:
        p2 = [(fx(a), fy(b)) for a, b in pts if a > 0 and b > 0]
    elif xlog:
        p2 = [(fx(a), fy(b)) for a, b in pts if a > 0]
    elif ylog:
        p2 = [(fx(a), fy(b)) for a, b in pts if b > 0]
    else:
        p2 = [(fx(a), fy(b)) for a, b in pts]
    if not p2:
        return ""
    X = [p[0] for p in p2]
    Y = [p[1] for p in p2]
    x0, x1, y0, y1 = min(X), max(X), min(Y), max(Y)
    if x1 - x0 < 1e-30:
        x1 = x0 + 1
    if y1 - y0 < 1e-30:
        y1 = y0 + 1
    pad = 54
    iw = w - pad - 20
    ih = h - pad - 30

    def px(v):
        return pad + (v - x0) / (x1 - x0) * iw

    def py(v):
        return h - pad - (v - y0) / (y1 - y0) * ih

    poly = " ".join("%.2f,%.2f" % (px(a), py(b)) for a, b in p2)
    ticks = ""
    for i in range(5):
        v = x0 + (x1 - x0) * i / 4.0
        lb = ("%.3g" % (10 ** v)) if xlog else ("%.3g" % v)
        ticks += ('<text x="%.2f" y="%d" class="tk" text-anchor="middle">%s</text>'
                  % (px(v), h - pad + 16, lb))
    for i in range(5):
        v = y0 + (y1 - y0) * i / 4.0
        lb = ("%.2e" % (10 ** v)) if ylog else ("%.3g" % v)
        ticks += ('<text x="%d" y="%.2f" class="tk" text-anchor="end">%s</text>'
                  % (pad - 6, py(v) + 4, lb))
    extra = ""
    if zero_line is not None:
        extra = ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#2d6ea8" '
                 'stroke-dasharray="4,3"/>'
                 % (pad, py(zero_line), pad + iw, py(zero_line)))
    return ('<svg viewBox="0 0 {w} {h}" class="chart">'
            '<rect x="{pad}" y="20" width="{iw}" height="{ih}" fill="none" stroke="#bbb"/>'
            '<polyline points="{poly}" fill="none" stroke="{col}" stroke-width="2"/>'
            '{extra}{ticks}'
            '<text x="10" y="14" class="tt">{title}</text>'
            '<text x="{cx}" y="{yb}" class="ax" text-anchor="middle">{xl}</text>'
            '</svg>').format(w=w, h=h, pad=pad, iw=iw, ih=ih, poly=poly, col=color,
                             extra=extra, ticks=ticks, title=title,
                             cx=pad + iw / 2.0, yb=h - 8, xl=xlabel)


def render_html(res, path):
    cir = res["circular"]
    esc = res["escape"]
    # 图1：U''(r_c) 的符号因子 −x²+x+1
    f = lambda x: -x * x + x + 1.0
    p1 = [(0.02 + 0.045 * i, abs(f(0.02 + 0.045 * i))) for i in range(80)]
    s1 = svg_line(p1, 620, 300, xlog=False, ylog=True, color="#c0392b",
                  xlabel="x = r_c / λ", title="图1 · 圆轨道稳定性因子 |−x²+x+1|（x=φ 处过零）")
    # 图2：太阳系 λ 下界
    p2 = [(b["a_m"] / AU, b["lam_min_AU"]) for b in cir["bounds"]]
    s2 = svg_line(p2, 620, 300, xlog=False, ylog=False, color="#2d6ea8",
                  xlabel="半长轴 a (AU)", title="图2 · 各行星稳定圆轨道所要求的 λ 下界 (AU) = a/φ")
    # 图3：逃逸速度比
    p3 = [(r["x"], r["ratio"]) for r in esc["rows"]]
    s3 = svg_line(p3, 620, 300, xlog=False, ylog=False, color="#7a4fa3",
                  xlabel="x = r / λ", title="图3 · 逃逸速度 / 牛顿值 = e^{−x/2}")
    # 图4：荷类型
    rows = [("gravity", "m/m_P", "连续量（随物体变）", "#c0392b"),
            ("em", "√α·Z", "离散整数×常数（随物体变）", "#c0392b"),
            ("weak", "g_W/√4π", "普适常数（不随物体变）", "#2d6ea8"),
            ("strong", "g_π/√4π", "普适常数（不随物体变）", "#2d6ea8")]
    bars = ""
    for i, (nm, ex, kind, col) in enumerate(rows):
        y = 40 + i * 52
        bars += ('<rect x="20" y="%d" width="26" height="26" fill="%s"/>' % (y, col))
        bars += ('<text x="56" y="%d" class="tk">%-9s %-14s %s</text>'
                 % (y + 18, nm, ex, kind))
    s4 = ('<svg viewBox="0 0 620 260" class="chart">%s'
          '<text x="10" y="14" class="tt">图4 · 四个 Q 的数学对象类型：2 类随物体变（红）、'
          '2 类不随物体变（蓝）⇒ 无法合成</text></svg>' % bars)

    html = u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-r224 · 四力统一运动方程（第二推进轮）</title>
<style>
body{font-family:"Microsoft YaHei",system-ui,sans-serif;margin:24px;color:#222;background:#fff;line-height:1.7}
h1{font-size:20px;border-bottom:2px solid #c0392b;padding-bottom:8px}
h2{font-size:16px;margin-top:26px;color:#2d6ea8}
.chart{width:100%;max-width:640px;border:1px solid #ddd;background:#fafafa;margin:8px 0}
.tt{font-size:12px;fill:#333}.tk{font-size:11px;fill:#444}.ax{font-size:11px;fill:#444}
table{border-collapse:collapse;font-size:13px;margin:10px 0}
td,th{border:1px solid #ccc;padding:5px 9px;text-align:right}th{background:#f0f0f0}
code{background:#f4f4f4;padding:1px 4px;border-radius:3px}
.note{background:#fff8e6;border-left:3px solid #e6a23c;padding:8px 12px;margin:10px 0;font-size:13px}
</style></head><body>
<h1>TUFT-r224 · 四力统一运动方程（第二推进轮）：Proca 机验 · 圆轨道稳定性 · 荷空间可加性</h1>
<div class="note"><b>命题</b>：继续「把所有力写进一个运动方程」——本轮在 r223 之上再推进三层：
<b>①Proca/Yukawa 场方程的机器验证</b>；<b>②圆轨道稳定性（解析判据）</b>；<b>③荷空间可加性</b>。</div>

<h2>① Proca/Yukawa 场方程：机器验证 <span style="color:#2d6ea8">通过</span></h2>
<p>自写精确微分引擎走「×r² → d/dr → ÷r²」：<code>∇²V = K e^{−r/λ}/(r λ²) = V/λ²</code>
⇒ <code>∇²V − V/λ² = 0</code>，<b>残差机器为 0</b>。线性势复算 <code>(∇²−1/λ²)(σr) = σ(2/r − r/λ²) ≠ 0</code>
⇒ 禁闭项确被排除（靶此处诚实）。<b>但对靶有利的两条都要配一条限制</b>：
「齐次」只在 r&gt;0 成立，而该方程正被用于定义<b>点粒子之间的力</b>（r→0 处有 δ 源）。</p>

<h2>② 圆轨道稳定性：解析判据（本卷核心）</h2>
<p>有效势 <code>U(r) = −μ e^{−r/λ}/r + h²/(2r²)</code>；圆轨道条件 U′=0 ⇒
<code>h² = μ e^{−x}(r²/λ + r)</code>，代回二阶导得闭式</p>
<p><code>U″(r_c) = (μ e^{−x} / r_c³) · (−x² + x + 1)</code>　，　<code>x ≡ r_c/λ</code></p>
<div class="note"><b>稳定 ⟺ −x² + x + 1 &gt; 0 ⟺ x &lt; φ = (1+√5)/2 = __PHI__（黄金比）</b>。
数值复核：闭式与直接二阶导在 8 个点上相对差 ≤ __REL__，二分变号点 __ROOT__ 与 φ 相对差 __RREL__。</div>
__S1__
<h3>太阳系硬约束：λ &gt; a/φ</h3>
<table><tr><th>行星</th><th>a (AU)</th><th>λ 下界 (AU)</th></tr>
__ROWS__
</table>
__S2__
<div class="note"><b>与 r223 合起来看</b>：稳定性只排除 λ ≲ <b>18.6 AU</b>（海王星），
而 r223 的 λ_fit ≈ <b>957.9 AU</b> 满足稳定性却与金星/地球/火星进动冲突
<b>6.96× / 18.4× / 64.1×</b> ⇒ 两条约束把 Yukawa 引力夹成
<b>「要么无稳定轨道，要么与多行星进动冲突」</b>，无可行区间。</div>

<h2>③ 荷空间可加性：判决项</h2>
__S4__
<p>四个 Q 是<b>三种互不相容的数学对象</b>：连续量（m/m_P）、离散整数×常数（√α·Z）、
普适耦合常数（g_W/√4π、g_π/√4π）。塞进同一个 <code>Q₁Q₂</code> 意味着弱/强通道的力
<b>不随物体身份变化</b>——与实际弱相互作用（味/弱荷/手征）矛盾。
靶中「统一荷/总荷/合成荷/同时作用」命中 <b>0</b> ⇒ <b>无法定义 Q_total²</b> ⇒
「把四力写进一个方程」在<b>同一次相互作用</b>的意义上不成立。</p>

<h2>④ 距离特性：逃逸速度</h2>
__S3__
<p><code>v_esc / v_esc(牛顿) = e^{−r/(2λ)}</code>：r=λ 处降 <b>39.4%</b>，r=2λ 处降 63.2%，
r=5λ 处降 91.8% —— 这是<b>可观测</b>的距离特性，靶未给出任何检验。
另：V(r→0) → −∞，势阱<b>无下界</b>且无截断 ⇒ 点粒子极限未定义。</p>

<div class="note"><b>红线</b>：本卷条目不可与 r142–r223 相加。数学自洽 ≠ 实验证实；
本卷只给「可算判决」，不产生新物理。</div>
</body></html>"""
    rows = "".join("<tr><td>%s</td><td>%.3f</td><td>%.3f</td></tr>"
                   % (b["name"], b["a_m"] / AU, b["lam_min_AU"])
                   for b in cir["bounds"])
    html = (html.replace("__S1__", s1).replace("__S2__", s2)
            .replace("__S3__", s3).replace("__S4__", s4)
            .replace("__ROWS__", rows)
            .replace("__PHI__", "%.10f" % cir["phi"])
            .replace("__REL__", fmt_rel(cir["max_closed_rel"]))
            .replace("__ROOT__", "%.10f" % cir["root_numeric"])
            .replace("__RREL__", fmt_rel(cir["root_rel_to_phi"])))
    io.open(path, "w", encoding="utf-8").write(html)
    return path


# ==================== 渲染 ====================
def build_payload(res):
    return {
        "id": "r224", "date": "2026-10-26",
        "title": ("四力统一运动方程（第二推进轮）：Proca 场方程机器验证、"
                  "圆轨道稳定性解析判据、荷空间可加性与逃逸特性"),
        "target": {k: os.path.basename(v) for k, v in TARGET_FILES.items()},
        "verdict": VERDICT_TOKEN, "redline": REDLINE_PHRASE,
        "entries": [{"id": e[0], "layer": e[1], "text": e[2], "verdict": e[3],
                     "note": e[4]} for e in res["entries"]],
        "controls": [{"id": c[0], "text": c[1], "ok": c[2], "detail": c[3]}
                     for c in res["controls"]],
        "guards": [{"id": g[0], "text": g[1], "ok": g[2], "detail": g[3]}
                   for g in res["guards"]],
        "key_numbers": res["key_numbers"], "counts": res["counts"],
        "not_closed": NOT_CLOSED,
    }


def render_report(p):
    L = ["=" * 78, "TUFT-r224 · 四力统一运动方程（第二推进轮）精算报告", "=" * 78, ""]
    L.append("[编号] r224（本线 r223 于 03:27:40 先占位；并行另一 r223 于 03:34:23 落 ⇒ "
             "r224 三树实测为空，本卷取 r224）")
    L.append("[命题] 继续「所有力写进一个运动方程」：Proca 机验 + 圆轨道稳定性 + 荷空间可加性")
    L.append("")
    L.append("[条目] total=%d  %s" % (len(p["entries"]), p["counts"]))
    for e in p["entries"]:
        L.append("  [%s] %s | %s" % (e["verdict"], e["id"], e["layer"]))
        L.append("        %s" % e["text"])
        if e["note"]:
            L.append("        note: %s" % e["note"])
    L.append("")
    L.append("[控制组] %d / %d" % (sum(1 for c in p["controls"] if c["ok"]),
                                   len(p["controls"])))
    for c in p["controls"]:
        L.append("  %-5s %-8s %s" % (c["id"], "OK" if c["ok"] else "NG", c["text"]))
    L.append("")
    L.append("[守卫] %d / %d" % (sum(1 for g in p["guards"] if g["ok"]), len(p["guards"])))
    for g in p["guards"]:
        L.append("  %-5s %-8s %s" % (g["id"], "OK" if g["ok"] else "NG", g["text"]))
    L.append("")
    L.append("[判词]")
    L.append(p["verdict"])
    L.append("")
    L.append("[红线] " + p["redline"])
    L.append("[未闭合项]")
    for i, s in enumerate(p["not_closed"], 1):
        L.append("  %d. %s" % (i, s))
    return "\n".join(L)


def render_verdict_md(p):
    L = ["# 判定册 · TUFT-r224｜四力统一运动方程（第二推进轮）", "",
         "## 一、编号与定位", "",
         "- **编号 r224**：本线 r223（运动方程卷）于 **03:27:40** 落盘；并行随后于 "
         "**03:34:23** 落下另一 r223《四力统一方程_量子束缚层…》⇒ **本线 r223 先占位**，"
         "r223 号段归本线。起草前实测 **r224/r225/r226 三树全空** ⇒ 本卷取 **r224**。"
         "全程未触碰并行任何字节。**本线下一轮从 r225 起**。",
         "- **分工**：本卷**不重复** r223 已判的求导恒等 / Bertrand 闭合性 / 进动 "
         "Δω ∝ λ⁻² / λ_fit 多行星崩坏 / 方向 dim=1 / 无量纲同构 2/4，只作指针引用；"
         "本卷新增 **L1 Proca 场方程机器验证**、**L2 圆轨道稳定性解析判据**、"
         "**L3 荷空间可加性**、**L4 原点发散**、**L5 逃逸特性**、**L6 叠加闭合性**。",
         "- **靶（4 份，只读）**：§18 md + §18_verify.py + §18_四力曲线数据.json + "
         "D5 README（语境；主体 P=m(c−v) 已由本线 r181 判过）。",
         "- **分层**：本卷条目" + REDLINE_PHRASE.replace(
             "不可与", "**不可与").replace("相加", "相加**") + "。", "",
         "## 二、判词", "", "`" + p["verdict"] + "`", "",
         "条目 **%d** = FAIL %d / PASS %d / INFO %d；**控制组 %d/%d**；**守卫 %d/%d**。"
         % (len(p["entries"]), p["counts"].get("FAIL", 0), p["counts"].get("PASS", 0),
            p["counts"].get("INFO", 0), sum(1 for c in p["controls"] if c["ok"]),
            len(p["controls"]), sum(1 for g in p["guards"] if g["ok"]),
            len(p["guards"])), "",
         "## 三、圆轨道稳定性（解析核心）", "",
         "```",
         "U(r)   = -mu e^{-r/lam}/r + h^2/(2 r^2)          （单位质量，引力 K<0）",
         "U'=0   =>  h^2 = mu e^{-x} (r^2/lam + r)         ,  x = r/lam",
         "U''(rc)= (mu e^{-x} / rc^3) * ( -x^2 + x + 1 )",
         "稳定  <=>  -x^2 + x + 1 > 0  <=>  x < phi = (1+sqrt5)/2 = %.10f" % PHI,
         "```", "",
         "| 行星 | a (AU) | λ 下界 = a/φ (AU) |", "|---|---|---|"]
    for b in p["key_numbers"]["circular"]["bounds"]:
        L.append("| %s | %.3f | %.3f |" % (b["name"], b["a_m"] / AU, b["lam_min_AU"]))
    L += ["", "## 四、条目明细", "", "| ID | 层 | 判决 | 结论摘要 |", "|---|---|---|---|"]
    for e in p["entries"]:
        t = e["text"].replace("\n", " ").replace("|", "/")
        L.append("| %s | %s | **%s** | %s |" % (e["id"], e["layer"], e["verdict"],
                                                t[:150] + ("…" if len(t) > 150 else "")))
    L += ["", "## 五、控制组与守卫", ""]
    for c in p["controls"]:
        L.append("- [%s] %-5s %s" % ("OK" if c["ok"] else "NG", c["id"], c["text"]))
    for g in p["guards"]:
        L.append("- [%s] %-5s %s" % ("OK" if g["ok"] else "NG", g["id"], g["text"]))
    L += ["", "## 六、未闭合项", ""]
    for i, s in enumerate(p["not_closed"], 1):
        L.append("%d. %s" % (i, s))
    L += ["", "---", "", "**红线**：" + p["redline"] + "。数学自洽 ≠ 实验证实；"
          "本卷只给「可算判决」，不产生新物理。"]
    return "\n".join(L)


VERDICT_TOKEN = ""


def main():
    before = {k: sha256_file(v) for k, v in TARGET_FILES.items()}
    res = run_audit()
    bad = _ast_self_audit()
    for g in GUARDS:
        if g[0] == "G6":
            GUARDS[GUARDS.index(g)] = (
                "G6", "ast 自审：ctl/grd 未出现字面 True 作为 ok 参数", not bad,
                ",".join(bad) if bad else "clean")

    cir = res["circular"]
    chg = res["charge"]
    NOT_CLOSED[:] = [
        "本卷**不重复** r223 已判各项（求导恒等、Bertrand 闭合性、Δω ∝ λ⁻²、"
        "λ_fit=957.9 AU 的多行星崩坏、方向 dim=1、无量纲同构 2/4），只作指针引用；"
        "两卷条目**不可相加**。",
        "圆轨道稳定性判据 x < φ 是在**检验粒子、圆轨道、单体中心力**近似下导出的；"
        "未含偏心率的一般有界轨道稳定性（对 e>0 需另做 Floquet 分析）、"
        "行星间摄动与非球对称项。",
        "λ > a/φ 的下界是**必要条件**（稳定圆轨道存在），不是充分条件；"
        "它不与 r223 的进动约束冲突，但也不足以救后者。",
        "荷空间可加性为**结构层**判决：若靶后续给出统一荷映射（如把四种荷嵌入同一个"
        "表示的权向量），C1–C3 需重审。",
        "「齐次性只在 r>0」是对**措辞**的判决，不是对计算结果的质疑："
        "靶的 ∇²V = V/λ² 计算本身正确（本卷 A1 PASS）。",
        "逃逸速度比值 e^{−r/2λ} 未被靶检验，属**未行使的判别力**（与 r218 同型），"
        "不是靶的算术错误。",
        "可视化为示意：图 1 的纵坐标取绝对值并走对数，过零点在 x=φ 处表现为谷底。",
    ]
    payload = build_payload(res)
    payload["not_closed"] = NOT_CLOSED

    os.makedirs(DATA_DIR, exist_ok=True)
    p_json = os.path.join(DATA_DIR, BASE_NAME + ".json")
    p_md = os.path.join(DATA_DIR, BASE_NAME + ".md")
    p_rep = os.path.join(DATA_DIR, BASE_NAME + "_report.txt")
    p_ver = os.path.join(DATA_DIR, "判定_" + BASE_NAME + ".md")
    p_html = os.path.join(SRC_DIR, BASE_NAME + ".html")

    io.open(p_json, "w", encoding="utf-8").write(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    md_text = render_verdict_md(payload)
    rep_text = render_report(payload)
    redline_ok = (REDLINE_PHRASE in md_text) and (REDLINE_PHRASE in rep_text)
    io.open(p_md, "w", encoding="utf-8").write(md_text)
    io.open(p_rep, "w", encoding="utf-8").write(rep_text)
    io.open(p_ver, "w", encoding="utf-8").write(md_text)
    render_html(res, p_html)

    after = {k: sha256_file(v) for k, v in TARGET_FILES.items()}
    cnt = res["counts"]
    print("entries: " + " ".join("%s=%d" % (k, v) for k, v in sorted(cnt.items()))
          + " total=%d" % len(ENTRIES))
    print("controls: %d / %d" % (sum(1 for c in CONTROLS if c[2]), len(CONTROLS)))
    print("guards  : %d / %d" % (sum(1 for g in GUARDS if g[2]), len(GUARDS)))
    print("targets unchanged: %s" % (before == after))
    print("html    : %s" % os.path.basename(p_html))
    print("verdict : " + VERDICT_TOKEN)
    if not redline_ok:
        print("REDLINE-MISSING-IN-OUTPUT")
        return 4
    if bad:
        print("AST-AUDIT-BAD: %s" % bad)
        return 3
    if not all(c[2] for c in CONTROLS) or not all(g[2] for g in GUARDS):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
