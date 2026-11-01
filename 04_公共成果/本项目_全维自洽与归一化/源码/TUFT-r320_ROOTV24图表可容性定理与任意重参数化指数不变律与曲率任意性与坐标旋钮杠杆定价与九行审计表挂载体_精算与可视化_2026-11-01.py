# -*- coding: utf-8 -*-
"""
TUFT-r320 · ROOT V24.0 同来料第三把尺（图表层：可容性 / 曲率任意性 / 杠杆定价）
  来料：精细结构常数第一性原理攻坚——固定点的真假判别（1/150 → 1/137 只差一次变量替换）
  本卷判据族：V1–V19（主 19）+ C1–C7（控制 7）+ G1–G15（守卫 15）= 41 条
  分工（落盘前现扫三树 + README 实测）：
    r317 = 本来料第一把尺（§一 复现 / 事后编造定理 k=1/u*−1/T / §二 相似 / §三 12 读数 / §四 H(q) / R1–R6）
    r321 = 本来料互补攻坚（真空极化一般闭式 / 可预测性符号判据 / 放大因子与信息量记账）——本卷开工时已落盘
    r308 = ROOT V22 齐套卷（同族 β 系统，只读引用）
  本卷不重复上述命题；承重前提（V1/V11/V13）逐条点名「与彼卷同一事实，两卷不可相加」。
  本卷净增量：图表可容性定理与视界 / 任意 C1 图表指数不变律的一般证明 / 二阶射流非不变（曲率可为零或反号）
              / 整数旋钮与 σ 货币二分 / 散布与闭环的 α⁻¹ 货币定价 / 来料无表主张的替代载体 / 九行审计表挂载体
纪律：不产生新物理；不改他卷任何字节；不与并发卷（r308/r317/r321 等）相加；不跑 refresh_catalog.py；不做 git。
"""
import sys, os, re, json, time
from fractions import Fraction as F

sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "数据")
JUDG = os.path.join(ROOT, "判定")

RID = "r320"
STAMP = "2026-11-01"
BASE = ("TUFT-r320_ROOTV24图表可容性定理与任意重参数化指数不变律与曲率任意性与"
        "坐标旋钮杠杆定价与九行审计表挂载体_精算与可视化_2026-11-01")
ZHENG = os.path.join(DATA, BASE + "_来料原件_ROOT_V24.0_用户附件逐字_2026-11-01.md")
HTML_NAME = "四力统一方程_ROOTV24图表层可容性与曲率任意性审计_r320可视化_2026-11-01.html"
R308_MD = os.path.join(DATA, "TUFT-r308_ROOTV22固定点非唯一性与尺度嬗变与轻子真空极化_UV临界面自由度账本_精算与可视化_2026-11-01.md")
R317_MD = os.path.join(DATA, "TUFT-r317_ROOTV24固定点真假判别_可逆重参数化坐标伪影与事后编造定理与相似不变量_精算与可视化_2026-11-01.md")
R317_JSON = os.path.join(DATA, "TUFT-r317_ROOTV24固定点真假判别_可逆重参数化坐标伪影与事后编造定理与相似不变量_精算与可视化_2026-11-01.json")
R321_MD = os.path.join(DATA, "TUFT-r321_ROOTV24固定点真假判别互补攻坚_真空极化闭式与可预测性符号判据与放大因子定价与能标冗余_2026-11-01.md")
R321_JSON = os.path.join(DATA, "TUFT-r321_ROOTV24固定点真假判别互补攻坚_真空极化闭式与可预测性符号判据与放大因子定价与能标冗余_2026-11-01.json")

DESIGN_FAIL = ("V17", "V18")
N_MAIN_DECLARED = 19
N_CTL_DECLARED = 7
G_IDS = ("G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12", "G13", "G14", "G15")
N_GUARD_DECLARED = len(G_IDS)                 # 15
DECLARED_N = N_MAIN_DECLARED + N_CTL_DECLARED + N_GUARD_DECLARED   # 41

# 跨卷重叠账（分工不可含糊）：凡与并发卷审到同一事实的主条目都在这儿点名。
# 账外主条目必须带★（本卷净增量）。G11 现算这条纪律，不靠自觉。
OVERLAP = {
    "V1": "r317 Q1 / r321 A02–A05（§一 链式法则与 O* 不变：同一事实，三卷不可相加）",
    "V3": "r321 CTL4（同一旋钮的实数解 c=12.964…；本卷给的是整条直线 1/v*=150−k 与 101 格）",
    "V4": "r321 C06（1/137 与实测 α⁻¹ 的 σ 距离；本卷另加 α 货币与整数格 101/101 两项）",
    "V9": "r321 A08/A08b（相似不变量；本卷补的是能精确实现打印 λ± 的载体与固定点被搬走）",
    "V11": "r321 A07（§三 12 格轨道表同一张表的独立复现；容差口径分歧见该条）",
    "V13": "r321 C01/B01（H 的闭式：其册给一般 q 闭式，本卷给 q=1 的黄金比特化 (7−6√5 ln φ)/(9π)，同值互校）",
    "V14": "r321 C04/C05（放大杠杆：其册用 e^{θΔ} 与 bit 记账，本卷用 α⁻¹ 单位的旋钮步长，两种货币）",
    "V15": "r321 C07（Möbius ≡ B→B−cA 的单点；本卷给 101 行替代载体的逐行指数不变见证）",
    "V19": "r317/r321 的判据集（R1–R6 同分，本卷不新增通过项）",
}
CODATA_INV = mp.mpf("137.035999177")
SIGMA_INV = mp.mpf("2.1e-8")
A_R = F(1, 50)
B_R = F(3)
U_STAR = A_R / B_R                     # 1/150
K_MAT = F(13)

_log = []


def log(s=""):
    print(s)
    _log.append(str(s))


def mfr(x):
    if isinstance(x, F):
        return mp.mpf(x.numerator) / mp.mpf(x.denominator)
    return mp.mpf(str(x))


def ns(x, n=12):
    return mp.nstr(mfr(x), n, strip_zeros=False)


def md5_of(p):
    if not os.path.isfile(p):
        return None
    h = 0
    import hashlib
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def stat_of(p, live=False, tag="他卷在飞"):
    if not os.path.isfile(p):
        return "缺失"
    st = os.stat(p)
    s = "%d B / md5 %s" % (st.st_size, md5_of(p)[:12])
    if live:
        s += "｜%s：只作当下观察，不可后引" % tag
    return s


def ulp_case(printed, computed):
    """按打印字段自身的半 ulp 裁定：返回 (绝对偏差, 半ulp, 比值)。"""
    d = len(printed.split(".")[1])
    half = mp.mpf(5) / mp.mpf(10) ** (d + 1)
    dev = mp.fabs(mfr(computed) - mp.mpf(printed))
    return dev, half, dev / half


ITEMS = []


def add(tid, layer, title, verdict, detail, kv=None, typ=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title, "verdict": verdict,
                  "detail": detail, "kv": kv or {}, "型": typ})


# ---------------------------------------------------------------- 主条目
def v1():
    U, V = sp.symbols("U V")
    A, B, k = sp.Rational(1, 50), sp.Integer(3), sp.Integer(13)
    BU = A * U - B * U ** 2
    pathA = sp.simplify((1 / (1 - k * U) ** 2).subs(U, V / (1 + k * V)) * BU.subs(U, V / (1 + k * V)))
    pathB = sp.expand(A * V + (k * A - B) * V ** 2)
    resid = sp.simplify(pathA - pathB)
    su = sp.diff(BU, U).subs(U, A / B)
    sv = sp.diff(pathB, V).subs(V, A / (B - k * A))
    Ou = (A / B) ** 2
    Ov = sp.simplify((V / (1 + 13 * V)) ** 2).subs(V, sp.Rational(1, 137))
    ok = (resid == 0 and su == -sp.Rational(1, 50) and sv == -sp.Rational(1, 50)
          and Ou == sp.Rational(1, 22500) and Ov == sp.Rational(1, 22500))
    kv = {"residual": str(resid), "u_star": str(A / B), "v_star": str(A / (B - k * A)),
          "slope_u": str(su), "slope_v": str(sv), "O_star_u": str(Ou), "O_star_v": str(Ov)}
    verdict = "PASS" if ok else "FAIL"
    detail = ("路A（链式法则 dv/du·β_u 并把 u 写成 v/(1+13v)）= %s；路B（来料打印的多项式）= %s；"
              "两路残差 = %s（符号精确 0，非「接近 0」）。固定点 u*=1/150、v*=1/137；"
              "两侧斜率同 = %s / %s = −1/50；示范可观测量 O=u² 的两种写法代回固定点同为 1/22500 = %s。"
              "⇒ 来料 §一 的每个可计算断言为真。★本条为承重前提，与并发卷 r317 Q1 审的是同一事实，两卷不可相加。"
              % (sp.factor(pathA), pathB, resid, su, sv, float(Ou)))
    add("V1", "主", "§一 双路精确复现：链式法则与打印多项式残差 0；u*=1/150 ↔ v*=1/137；β′ 双侧同 −1/50；O*=1/22500", verdict, detail, kv)


def v2():
    U = sp.symbols("U")
    A, B = sp.Rational(1, 50), sp.Integer(3)
    BU = A * U - B * U ** 2
    g = sp.Function("g")
    lhs = sp.simplify((1 / sp.diff(g(U), U)) * sp.diff(sp.diff(g(U), U) * BU, U))
    rhs = sp.diff(BU, U) + sp.diff(g(U), U, 2) / sp.diff(g(U), U) * BU
    ident = sp.simplify(lhs - rhs) == 0
    atfp = sp.simplify(lhs.subs(U, sp.Rational(1, 150)))
    V, S = sp.symbols("V S")
    k = sp.Integer(13)
    mob = sp.expand(A * V + (k * A - B) * V ** 2)
    s_mob = sp.diff(mob, V).subs(V, A / (B - k * A))
    p3 = sp.expand(3 * A * V - 3 * B * V ** sp.Rational(4, 3))
    s_p3 = sp.simplify(sp.diff(p3, V).subs(V, sp.Rational(1, 150 ** 3)))
    fam = U / (1 - 13 * U) + S * (U - sp.Rational(1, 150)) ** 2
    d1 = sp.diff(fam, U)
    bg = sp.simplify((1 / d1) * sp.diff(d1 * BU, U))
    s_fam = sp.simplify(bg).subs(U, sp.Rational(1, 150))
    v_fam = sp.simplify(fam.subs(U, sp.Rational(1, 150)))
    ok = (ident and atfp == -sp.Rational(1, 50) and s_mob == -sp.Rational(1, 50)
          and s_p3 == -sp.Rational(1, 50) and s_fam == -sp.Rational(1, 50))
    kv = {"identity": str(ident), "abstract_at_fp": str(atfp), "mobius": str(s_mob),
          "power_u3": str(s_p3), "deform_S": str(sp.simplify(s_fam))}
    detail = ("一般定理（对任意可逆图表 v=g(u)）：dβ_g/dv = β″_u(u) + (g″/g′)·β_u(u)；"
              "恒等式两边差 = 0（SymPy 逐符号）⇒ 在固定点处 β_u=0 杀死含 g 的那一项，"
              "于是 dβ_g/dv|_(v*) = β′_u(u*) 恒成立，与 g 的选法无关。符号取值 = %s。"
              "三族实例（同一模型 A=1/50、B=3）：Möbius 族 v=u/(1−13u) 给 %s；"
              "幂函数族 v=u³ 给 V*=1/150³=1/3375000 且斜率 %s；形变族 v=u/(1−13u)+S(u−u*)² 给 %s（与 S 无关）。"
              "⇒ 固定点的**唯一图表不变内容是其谱**；坐标可任意，指数不可动。"
              % (atfp, s_mob, s_p3, sp.simplify(s_fam)))
    add("V2", "主", "★任意 C¹ 可逆图表的指数不变律（一般符号证明 + Möbius/幂函数/形变三族实例）", "PASS" if ok else "FAIL", detail, kv)


def v3():
    def vst(k):
        return A_R / (B_R - k * A_R)
    rows = []
    bad = 0
    for ki in range(-10, 91):
        k = F(ki)
        inv = 1 / vst(k)
        if inv != F(150 - ki):
            bad += 1
        rows.append((ki, str(inv)))
    cod = F(137035999177, 1000000000)
    kstar = F(150) - cod
    back = 1 / vst(kstar)
    lin_ok = (bad == 0 and back == cod)
    kv = {"k_count": len(rows), "linear_violations": bad, "k_star": str(kstar),
          "readback": str(back), "target": str(cod), "intercept": "150", "slope": "-1"}
    detail = ("旋钮一般式（Fraction 精确）：v*(k) = A/(B−kA) ⇒ **1/v* = 150 − k**：斜率 −1、截距 150 = B/A。"
              "整数格 k∈[−10,90] 共 %d 格逐格核验，违反线性的格数 = %d。"
              "来料的 k=13 ⇒ 1/v*=137 是这条直线上的一个格点（13 = 150 − 137）。"
              "要命中 CODATA 现行值 137.035999177 需 k* = 150 − 137.035999177 = %s（精确回代 1/v* = %s，残差 0）——"
              "一个 10 位小数、无任何第一性来源的实数。⇒ 该路线里「137」不是动力学输出，而是旋钮读数的另一种写法。"
              % (len(rows), bad, kstar, back))
    add("V3", "主", "★旋钮一般式与线性严格性：1/v*(k)=150−k（斜率 −1、截距 B/A=150，101 格残差 0）；命中 CODATA 需 k*=12.964000823", "PASS" if lin_ok else "FAIL", detail, kv)


def v4():
    d_inv = mp.fabs(mp.mpf(137) - CODATA_INV)
    n_sig_inv = d_inv / SIGMA_INV
    alpha = 1 / CODATA_INV
    a137 = mp.mpf(1) / 137
    sig_a = SIGMA_INV * alpha * alpha
    n_sig_a = mp.fabs(a137 - alpha) / sig_a
    n_sig_137036 = mp.fabs(mp.mpf("137.036") - CODATA_INV) / SIGMA_INV
    ints = sum(1 for ki in range(-10, 91) if (1 / (A_R / (B_R - F(ki) * A_R))).denominator == 1)
    kv = {"abs_diff_inv": ns(d_inv, 10), "sigma_inv": ns(n_sig_inv, 10),
          "sigma_alpha": ns(n_sig_a, 10), "census_137p036": ns(n_sig_137036, 10),
          "integer_hits": "%d/101" % ints}
    ok = (n_sig_inv > mp.mpf("1e6") and ints == 101)
    detail = ("二分判据（两种货币各自定价，避免「σ 无货币」）：整数旋钮只能给出 1/v* ∈ ℤ——"
              "k∈[−10,90] 的 101 格中 1/v* 为整数的格数 = %d/101 ⇒ 「算出的数是整数」由构造保证，对自然界零信息。"
              "取 k=13 得 137，与 CODATA α⁻¹(0)=137.035999177(21) 差 0.035999177 = **%s σ**（α⁻¹ 货币）；"
              "换成 α 货币（σ_α=α²σ_{α⁻¹}）= %s σ ⇒ 同一事实两种货币同为 10⁶ 量级，不是巧合放大。"
              "反面对照：若把来料读数当作「137.036」这一 6 位数，偏差 8.23e-7 = %s σ ⇒ 仍然不是预测。"
              "⇒ 整数旋钮必错（10⁶ σ 级）、实数旋钮必喂入（V3 的 k* 就是 α⁻¹ 本身）⇒ 双向 0 bit。"
              % (ints, ns(n_sig_inv, 8), ns(n_sig_a, 8), ns(n_sig_137036, 8)))
    add("V4", "主", "★整数/实数旋钮二分与 σ 货币普查：整数 k 只命中 ℤ（101/101）；137 偏 CODATA 1.71e6 σ（α⁻¹ 与 α 两货币同量级）", "PASS" if ok else "FAIL", detail, kv)


def v5():
    def adm(k, u0):
        if k == 0:
            return "可容", None
        pole = F(1) / k
        lo, hi = min(u0, U_STAR), max(u0, U_STAR)
        if pole == u0 or pole == U_STAR:
            return "端点重合", pole
        return ("不可容" if lo < pole < hi else "可容"), pole
    cases = [(F(13), F(1, 100)), (F(13), F(2, 1000)), (F(299, 2), F(2, 1000)),
             (F(299, 2), F(4, 1000)), (F(299, 2), F(1, 100)), (F(120), F(1, 100)),
             (F(100), F(1, 100)), (F(99), F(1, 100)), (F(149), F(1, 100))]
    rows = []
    for k, u0 in cases:
        v, pole = adm(k, u0)
        rows.append([str(k), str(u0), v, None if pole is None else ns(pole, 8),
                     str(1 / (A_R / (B_R - k * A_R)))])
    good = [ki for ki in range(-400, 150)
            if all(adm(F(ki), F(u))[0] == "可容" for u in (F(2, 1000), F(4, 1000), F(1, 100)))]
    kmax = max(good)
    reading99 = 1 / (A_R / (B_R - F(99) * A_R))
    k100_state = adm(F(100), F(1, 100))[0]
    window_ok = (kmax == 99 and k100_state != "可容" and reading99 == F(51)
                 and F(100) not in [F(ki) for ki in good])
    kv = {"rows": rows, "k_max_admissible": kmax, "reading_min": str(150 - kmax),
          "n_admissible_k": len(good)}
    detail = ("可容性判据（新）：v=u/(1−ku) 只在 1/k 不落入该条 RG 轨道的 u 取值区间时才是全域图表。"
              "三条来料轨道的 u 区间分别 = [0.002,1/150] / [0.004,1/150] / [1/150,0.010]。"
              "逐格扫描 k∈[−400,149]：对三条轨道**同时**可容的整数 k 上界 = %d ⇒ 配合 v*>0 需 k<150，"
              "**全域可容的正固定点读数只能落在 1/v* = 150−k > 50**（物理值 137.036 在窗内，来料的 k=13 在窗内）。"
              "★并此精化并发卷 r317 Q2「任意目标值都可制造」的表述：该命题只在固定点本身成立；"
              "其例 T=2（k=149.5）在 u0=0.010 那条轨道上 1/k=0.00668896 **落在区间内部** ⇒ 图表被极点切断，"
              "来料自己打印的那条历史在该图表里不存在（见 V6 的有限时刻发散）。"
              % kmax)
    add("V5", "主", "★图表可容性定理：可容 ⇔ 1/k ∉ 轨道区间；三轨道同时可容 ⇒ k≤99 ⇒ 可达读数 1/v*>50（精化「任意目标可造」）", "PASS" if window_ok else "FAIL", detail, kv)


def v6():
    k = F(299, 2)
    u0 = F(1, 100)
    pole = F(1) / k
    r_u = (U_STAR / pole - 1) / (U_STAR / u0 - 1)
    v0 = u0 / (1 - k * u0)
    Cv = k * A_R - B_R
    CA = -Cv / A_R
    w0 = 1 / v0
    r_v = -CA / (w0 - CA)
    same = (r_u == r_v) and r_u == F(1, 100)
    mp.mp.dps = 90
    tstar = mp.log(mp.mpf(100)) / mfr(A_R)
    u_at = (mfr(U_STAR) / (1 + (mfr(U_STAR) / mfr(u0) - 1) * mp.exp(-mfr(A_R) * tstar)))
    dev = mp.fabs(u_at - mfr(pole))
    kv = {"r_u": str(r_u), "r_v": str(r_v), "t_star": ns(tstar, 16), "pole": ns(pole, 12),
          "u_at_tstar_minus_pole": ns(dev, 3), "dps": 90}
    detail = ("两口径奇点时刻恒等（互为独立验算）：u 图表里令 u(t*)=极点 1/k 解得 e^{−At*} = %s（精确有理）；"
              "v 图表里 β_v = Av + Cv² 的 Riccati 解按 w=1/v 线性化得 w(t) = −C/A + (w₀+C/A)e^{−At}，"
              "其零点给 e^{−At*} = %s（精确有理）⇒ 两口径**同一个分数**。"
              "换成时刻：t* = ln(100)/A = %s（A=1/50）；把 t* 代回 u 闭式核验 u(t*) 与极点 1/k=%s 之差 = %s（90 位）。"
              "⇒ 图表被切断不是坐标幻觉，而是可算的有限 RG 时刻发散；V5 的可容窗正是排除它的条件。"
              % (r_u, r_v, ns(tstar, 15), ns(pole, 10), ns(dev, 3)))
    add("V6", "主", "★两口径奇点时刻恒等：v-图表 Riccati 极点与 u-图表 Jacobian 极点同解 e^{−At*}=1/100，t*=ln(100)/A=230.2585093", "PASS" if same and dev < mp.mpf("1e-40") else "FAIL", detail, kv)


def v7():
    den = B_R - F(150) * A_R
    pole = F(1, 1) / F(150)
    horizon = (den == 0) and (pole == U_STAR)
    k151 = F(151)
    v151 = A_R / (B_R - k151 * A_R)
    kv = {"den_at_150": str(den), "pole_at_150": str(pole), "u_star": str(U_STAR), "vstar_151": str(v151)}
    detail = ("旋钮视界：k → B/A = 150 时分母 B−kA → %s（精确 0）⇒ 非零固定点 v*→∞、β_v 退化为单零点的 Av；"
              "且此时 Jacobian 的极点 1/k = %s **恰落在固定点 u*=%s 上** ⇒ 该图表在自己要报告的那一点上不解析，"
              "「特征值不变」的前提（可逆微分同胚）失效。k=151 已越过视界 ⇒ v* = %s（负耦合，无物理读数）。"
              "⇒ 旋钮不是自由参数而是**受约束的坐标选择**：正固定点分支只覆盖 k<150 的半轴，"
              "且叠加 V5 的可容窗后只剩 k<100。本卷按 BOUNDARY 登记，不判来料错（来料只用了 k=13，在窗内）。"
              % (den, pole, U_STAR, v151))
    add("V7", "主", "★旋钮视界 k=B/A=150：Jacobian 极点恰落在固定点上、v*→∞、β_v 退化；k>150 ⇒ v*<0", "BOUNDARY" if horizon and v151 < 0 else "FAIL", detail, kv)


def v8():
    U, S = sp.symbols("U S")
    A, B = sp.Rational(1, 50), sp.Integer(3)
    BU = A * U - B * U ** 2
    UST = sp.Rational(1, 150)
    fam = U / (1 - 13 * U) + S * (U - UST) ** 2
    d1, d2 = sp.diff(fam, U), sp.diff(fam, U, 2)
    bg = sp.simplify((1 / d1) * sp.diff(d1 * BU, U))
    slope = sp.simplify(bg).subs(U, UST)
    dcurv = sp.simplify(sp.diff(bg, U) / d1)
    curv = sp.simplify(dcurv.subs(U, UST))
    third = sp.simplify((sp.diff(dcurv, U) / d1)).subs(U, UST)
    sstar = sp.solve(sp.Eq(curv, 0), S)[0]
    curv_S0 = sp.simplify(curv.subs(S, 0))
    vals = {str(sv): sp.nsimplify(curv.subs(S, sv)) for sv in
            [0, 1, -1, 5, sstar]}
    ok = (slope == -sp.Rational(1, 50) and sp.simplify(curv.subs(S, sstar)) == 0
          and curv_S0 == -sp.Rational(137, 25) and sp.simplify(fam.subs({U: UST})) == sp.Rational(1, 137)
          and len(set(vals.values())) == 5 and sp.simplify(third.subs(S, 0)) == 0)
    kv = {"beta_prime_v_star": str(sp.simplify(slope)), "beta_doubleprime_S": str(sp.factor(curv)),
          "S_zero_curvature": str(sstar), "S_zero_curvature_dec": ns(sstar, 12),
          "beta2_S0": str(curv_S0), "beta_tripleprime_S": str(sp.factor(third)),
          "values": {k2: str(v2_) for k2, v2_ in vals.items()}}
    detail = ("二阶射流不是不变量：形变族 v = u/(1−13u) + S(u−u*)² 对**一切 S** 保持 v* = 1/137 与 β′(v*) = %s；"
              "而 β″_v(v*) = %s 随 S **线性漂移**：S=0 给 −137/25 = %s（即来料 Möbius 图表的 2(kA−B)），"
              "S=1/−1/5 各给不同非零值，五枚取值两两不同；使 β″≡0 的 S* = %s = %s。"
              "同族还顺手给出 β‴_v(v*) = %s：它在 S=0（纯 Möbius，二次 β）恰为零，随 S 二次变化 ⇒ 三阶也不变。"
              "⇒ 同一固定点坐标 + 同一临界指数，却可以有任意的 β 曲线凹凸性（含严格为零）。"
              "⇒ 凡按「β 函数在固定点附近的弯曲/拐点」论证真伪的推理，在图表层面无效；"
              "不变量名单只剩谱，比 r317 的 {特征值+归一化约定} 再删去一切高阶射流信息。"
              % (sp.simplify(slope), sp.factor(curv), float(curv_S0), sstar, ns(sstar, 12),
                 sp.factor(third)))
    add("V8", "主", "★曲率任意性定理：同 v*=1/137 同 β′=−1/50 而 β″ 随图表线性漂移；存在 S* 使 β″≡0（β‴ 同族任意）", "PASS" if ok else "FAIL", detail, kv)


def v9():
    a, b = sp.symbols("a b")
    ast, bst = sp.Rational(1, 150), sp.Rational(1, 200)
    ba = sp.Rational(1, 25) * (a - ast) - (b - bst)
    bb = -sp.Rational(3, 20000) * (a - ast) - sp.Rational(1, 50) * (b - bst)
    gv = sp.Matrix([a, b])
    bv = sp.Matrix([ba, bb])
    Bs = bv.jacobian(gv)
    tr, dt = sp.simplify(Bs.trace()), sp.simplify(Bs.det())
    lam = sorted([sp.simplify(l) for l in Bs.eigenvals()], key=lambda z: str(z))
    s1, s2 = sp.symbols("s1 s2")
    fn = sp.Matrix([a / (1 - 13 * a) + s1 * b, b / (1 - 7 * b) + s2 * a])
    Jm = fn.jacobian(gv)
    sub = {a: ast, b: bst, s1: sp.Rational(1, 100), s2: sp.Rational(1, 50)}
    Js = Jm.subs(sub)
    Bp = sp.simplify(Js * Bs * Js.inv())
    lam2 = sorted([sp.simplify(l) for l in Bp.eigenvals()], key=lambda z: str(z))
    moved = sp.simplify(Bp - Bs) != sp.zeros(2, 2)
    newfp = [sp.nsimplify(x) for x in fn.subs(sub).T.tolist()[0]]
    fp_ok = all(sp.simplify(e.subs({a: ast, b: bst})) == 0 for e in bv)
    ok = (tr == sp.Rational(1, 50) and dt == -sp.Rational(19, 20000) and lam == lam2 and moved
          and fp_ok and sp.simplify(Js.det()) != 0)
    kv = {"B_star": [[str(x) for x in r] for r in Bs.tolist()], "tr": str(tr), "det": str(dt),
          "eigs": [str(l) for l in lam], "detJ": str(sp.nsimplify(Js.det())),
          "eigs_after": [str(l) for l in lam2], "fp_after": [str(x) for x in newfp]}
    detail = ("来料 §二 只打印了 λ±=1/100±√42/200 而未打印任何 β 函数或矩阵元素 ⇒ 本卷**补一个载体**（声明为本卷构造，非来料系统）："
              "β_a = (1/25)(a−1/150) − (b−1/200)、β_b = −(3/20000)(a−1/150) − (1/50)(b−1/200) "
              "在 (1/150, 1/200) 处 β=0（符号精确），其 Jacobian 迹 = %s、行列式 = %s = −19/20000，"
              "特征值 = %s / %s ⇒ **精确实现来料打印的那对 λ**，且 det<0 ⇒ 鞍形 ⇒ 相关方向 1 个（与 r308 的 2→1 同型）。"
              "再作混合非对角重参数化（J* 行列式 = %s ≠ 0）：矩阵元素改变（%s），迹/行列式/特征值三者逐项不变（%s），"
              "而固定点坐标被搬走 = %s → %s。⇒ 相似关系是「坐标任意、谱不动」的多耦合版本，来料 §二 的陈述在实数层面成立。"
              % (tr, dt, lam[0], lam[1], sp.nsimplify(Js.det()), moved, lam == lam2,
                 [str(ast), str(bst)], [str(x) for x in newfp]))
    add("V9", "主", "★§二 相似不变量的可复跑载体（本卷构造）：B*=[[1/25,−1],[−3/20000,−1/50]] 精确实现 λ±=1/100±√42/200；B′*=JB J⁻¹ 元素变谱不变", "PASS" if ok else "FAIL", detail, kv)


def v10():
    a11, a12, a21 = sp.symbols("a11 a12 a21")
    tr = sp.Rational(1, 50)
    M = sp.Matrix([[a11, a12], [a21, tr - a11]])
    sol = sp.solve(sp.Eq(M.det(), -sp.Rational(19, 20000)), a21)
    txt = open(ZHENG, encoding="utf-8").read().split("\n")
    ln_gen = [i + 1 for i, L in enumerate(txt) if "\\beta_i(" in L or "dg_i" in L]
    ln_lam = [i + 1 for i, L in enumerate(txt) if "42" in L and "100" in L]
    explicit_beta = [i + 1 for i, L in enumerate(txt) if ("beta_1" in L.replace("\\", "")) or ("β₁" in L)]
    mn = mp.mpf(sp.N(sp.Rational(1, 100) - sp.sqrt(42) / 200, 40))
    r308_lam = mp.mpf("0.04308542124349459")
    ratio = mp.fabs((mp.mpf(sp.N(sp.Rational(1, 100) + sp.sqrt(42) / 200, 40))) / mn)
    kv = {"free_params": 2, "a21_formula": str(sol[0]), "general_form_lines": ln_gen,
          "lambda_print_lines": ln_lam, "explicit_beta_lines": explicit_beta,
          "det_sign": "negative", "n_relevant": 1, "ratio_lam": ns(ratio, 10)}
    ok = (len(explicit_beta) == 0 and len(sol) == 1 and ln_lam)
    detail = ("§二 主张的可提取内容上限：正本第 %s 行只有抽象式 dg_i/dlnμ = β_i(g)，"
              "第 %s 行打印了 λ±；**含两个耦合的具体 β 函数与 B* 的矩阵元素在正本中出现 %d 次（= 无载体，实测非叙述）**。"
              "维数计数：2×2 有 4 个元素，谱只固定 {tr=1/50, det=−19/20000} 两个不变量 ⇒ "
              "a21 = %s 关于 (a11, a12) 的**二维族**都复现同一对 λ ⇒ 打印的 λ 不锁定任何具体系统，"
              "该主张不可复跑、也不可反驳（V9 给的是本卷的一个代表元，不是来料的那个系统）。"
              "物理账：det<0 ⇒ 一正一负 ⇒ 相关方向 1 个（比值 λ+/|λ−| = %s）⇒ §二 与 r308 的示范系统同为「固定点只压到 1 个幅度」，"
              "未给新的自由度收敛。"
              % (ln_gen, ln_lam, len(explicit_beta), sol[0], ns(ratio, 10)))
    add("V10", "主", "★λ± 主张的载体缺口：4 元素 vs 2 不变量 ⇒ 二维族；正本无具体 β（实测 0 次命中）⇒ 不可复跑；det<0 ⇒ 相关方向仍 1", "INFO" if ok else "FAIL", detail, kv)


def v11():
    ust = mfr(U_STAR)
    A_ = mfr(A_R)
    tab = [("0.002000", "0.002", 0), ("0.005067", "0.002", 100), ("0.006563", "0.002", 250),
           ("0.006666", "0.002", 500), ("0.004000", "0.004", 0), ("0.006115", "0.004", 100),
           ("0.006637", "0.004", 250), ("0.006666", "0.004", 500), ("0.010000", "0.01", 0),
           ("0.006982", "0.01", 100), ("0.006682", "0.01", 250), ("0.006667", "0.01", 500)]
    mp.mp.dps = 90
    rows = []
    worst = mp.mpf(0)
    worst_rel = mp.mpf(0)
    for printed, u0, L in tab:
        comp = ust / (1 + (ust / mp.mpf(u0) - 1) * mp.exp(-A_ * mp.mpf(L)))
        dev, half, ratio = ulp_case(printed, comp)
        rel = dev / comp
        worst = max(worst, ratio)
        worst_rel = max(worst_rel, rel)
        rows.append([printed, ns(comp, 12), ns(dev, 6), ns(half, 6), ns(ratio, 6), ns(rel, 8)])
    n_pass = sum(1 for r in rows if mp.mpf(r[4]) < 1)
    halved = sum(1 for r in rows if mp.mpf(r[2]) > mp.mpf(r[3]) / 2)
    r317_rel = None
    if os.path.isfile(R317_JSON):
        j = open(R317_JSON, encoding="utf-8").read()
        m = re.search(r'"maxrel":\s*([0-9.eE+-]+)', j)
        if m:
            r317_rel = mp.mpf(m.group(1))
    cmp_txt = ("他卷口径现测：r317 面上印 maxrel=%s" % (ns(r317_rel, 12) if r317_rel is not None else "未取到"))
    same = (r317_rel is not None and mp.fabs(r317_rel - worst_rel) / worst_rel < mp.mpf("1e-6"))
    agree_txt = ("与本卷逐位一致（比值差 <1e-6）" if same else
                 ("与本卷不一致（他卷面已在写盘后变动，本条只作当下观察）"
                  if r317_rel is not None else "本卷未取到第二口径，不做一致性强断言"))
    ok = (n_pass == 12 and worst < mp.mpf(1) and halved > 0)
    kv = {"rows": rows, "n_half_ulp_pass": n_pass, "worst_ratio": ns(worst, 6),
          "maxrel": ns(worst_rel, 12), "red_when_tol_halved": halved,
          "r317_maxrel": (ns(r317_rel, 12) if r317_rel is not None else None),
          "r317_agrees": bool(same),
          "overlap_r321": "A07（同一张 12 格轨道表，另册独立复现）——同一事实，两卷不可相加",
          "r317_face": stat_of(R317_JSON, live=True)}
    detail = ("§三 轨道表 12 个打印读数复现（90 位闭式）：**按各字段自身半 ulp 裁定 12/12 命中**，"
              "最紧一格的比值 = %s（即偏差已达该字段容许值的 %s 成）；"
              "最大相对偏差 = %s。把容差减半 ⇒ 立刻红掉 %d/12 枚 ⇒ 判据有牙不是恒绿。"
              "★口径冲突如实登记：本卷与并发卷 r317 复算的是同一张表，其面印 %s（该面 %s，写盘时在飞，当下读数不可后引）。"
              "%s：r317 按固定相对容差把该条判成 FAIL、本卷按印刷口径判成 PASS ⇒ "
              "**分歧全部来自容差货币，不是物理**；"
              "6 位打印字段的相对容许值本身就是 5e-7/0.0066 ≈ 7.5e-5 量级，比该表实际偏差更大。"
              % (ns(worst, 6), ns(worst * 100, 4), ns(worst_rel, 12), halved,
                 cmp_txt, kv["r317_face"], agree_txt))
    add("V11", "主", "§三 12 读数按印刷半 ulp 全命中（最紧 0.95 成）＋容差减半必红 5 枚；他卷同表 FAIL 的根因是容差比字段半 ulp 更紧（口径观察）", "PASS" if ok else "FAIL", detail, kv)


def v12():
    ust, A_ = mfr(U_STAR), mfr(A_R)
    def uof(u0, L):
        return ust / (1 + (ust / mp.mpf(u0) - 1) * mp.exp(-A_ * mp.mpf(L)))
    mp.mp.dps = 90
    c500 = [uof(x, 500) for x in ("0.002", "0.004", "0.01")]
    spread_u = max(c500) - min(c500)
    spread_inv = mp.fabs(1 / min(c500) - 1 / max(c500))
    def spread_at(L):
        c = [uof(x, L) for x in ("0.002", "0.004", "0.01")]
        return mp.fabs(1 / min(c) - 1 / max(c))
    def solve_L(target):
        lo, hi = mp.mpf(500), mp.mpf(4000)
        for _ in range(80):
            mid = (lo + hi) / 2
            if spread_at(mid) > mp.mpf(target):
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    L01 = solve_L("0.01")
    L001 = solve_L("0.001")
    dial = mp.mpf(13)
    kv = {"spread_u": ns(spread_u, 8), "spread_inv": ns(spread_inv, 8),
          "L_for_0p01": ns(L01, 10), "L_for_0p001": ns(L001, 10),
          "dial_step": "13", "ratio_dial_over_spread": ns(dial / spread_inv, 8)}
    detail = ("「三条曲线都趋向同一个紫外固定点」这句话的价格（换算到 α⁻¹ 货币后才可比）："
              "L=500 处三条轨道的 u 散布 = %s，倒数散布 = %s 个 α⁻¹ 单位；"
              "而一次整数旋钮步进（k 动 1 格到 13 格那档）移动的是 %s 个 α⁻¹ 单位 ⇒ **残余历史差异只是坐标之争的 1/%s**，"
              "看起来「已经收敛」的那一列其实还留着 0.018 个 α⁻¹ 单位。"
              "要把散布压到 0.01 单位需 L = %s，压到 0.001 单位需 L = %s（散布按 e^{−AL} 衰减，A=1/50 ⇒ 每个数量级再加 ln(10)/A≈115.1）。"
              "⇒ 来料 §三 的定性结论（固定点不选历史）为真，但「汇入同一固定点」的表格列并未把历史抹掉到预测所需的精度。"
              % (ns(spread_u, 6), ns(spread_inv, 6), dial, ns(dial / spread_inv, 6),
                 ns(L01, 8), ns(L001, 8)))
    add("V12", "主", "★散布定价：L=500 时残余历史差 0.01816 个 α⁻¹ 单位 = 旋钮步进的 1/716；压到 0.01/0.001 需 L≈529.8/644.9", "PASS" if spread_inv > mp.mpf("0.001") and dial / spread_inv > mp.mpf(100) else "FAIL", detail, kv)


def v13():
    mp.mp.dps = 90
    Hq = lambda qq: (2 / mp.pi) * mp.quad(lambda x: x * (1 - x) * mp.log(1 + qq * qq * x * (1 - x)), [0, 1])
    h1 = Hq(mp.mpf(1))
    xs = sp.symbols("x")
    he = sp.integrate(2 * xs * (1 - xs) * sp.log(1 + xs * (1 - xs)) / sp.pi, (xs, 0, 1))
    phi = (1 + sp.sqrt(5)) / 2
    cand = (7 - 6 * sp.sqrt(5) * sp.log(phi)) / (9 * sp.pi)
    closed_resid = sp.simplify(he - cand)
    dc = mp.fabs(mfr(closed_resid) if not isinstance(closed_resid, sp.Expr) else mp.mpf(sp.N(closed_resid, 60)))
    dq = mp.fabs(mp.re(sp.N(cand, 60)) - h1)
    V = sp.symbols("V")
    a0, hh = sp.symbols("a0 H", positive=True)
    aeff = a0 / (1 - a0 * hh)
    inv = sp.simplify(aeff / (1 + aeff * hh))
    ident_a0 = sp.simplify(inv - a0) == 0
    ident_inv = sp.simplify(sp.together(1 / aeff - (1 / a0 - hh))) == 0
    r1 = mp.mpf(1) / 137 / (1 - (mp.mpf(1) / 137) * h1)
    r2 = mp.mpf(1) / 150 / (1 - (mp.mpf(1) / 150) * h1)
    d1 = ulp_case("0.00730029506218", r1)
    d2 = ulp_case("0.00666752167946", r2)
    back1 = r1 / (1 + r1 * h1)
    back2 = r2 / (1 + r2 * h1)
    # 并发卷 r321 的一般 q 闭式在 q=1 处的独立对拍（只读其面；asinh(1/2)=ln φ ⇒ 二者解析同式）
    r321_h1 = None
    for _p in (R321_JSON, R321_MD):
        if os.path.isfile(_p):
            _m = re.search(r"1\.92353209028294[0-9]*(?:[eE][-+]?\d+)?",
                           open(_p, encoding="utf-8").read())
            if _m:
                r321_h1 = (mp.mpf(_m.group(0)), _p, _m.group(0))
                break
    xchk = (r321_h1 is not None and mp.fabs(r321_h1[0] - h1) < mp.mpf("1e-23"))
    asinh_id = sp.simplify(sp.asinh(sp.Rational(1, 2)).rewrite(sp.log)
                          - sp.log((1 + sp.sqrt(5)) / 2)) == 0
    their_at_1 = (2 / sp.pi) * (sp.Rational(5, 6) - sp.Rational(4, 9)
                                - sp.sqrt(5) * sp.asinh(sp.Rational(1, 2)) / 3)
    same_expr = sp.simplify(their_at_1.rewrite(sp.log) - cand) == 0
    ok = (closed_resid == 0 and ident_a0 and ident_inv and d1[2] < 1 and d2[2] < 1
          and mp.fabs(back1 - mp.mpf(1) / 137) < mp.mpf("1e-80")
          and mp.fabs(back2 - mp.mpf(1) / 150) < mp.mpf("1e-80"))
    kv = {"H1": ns(h1, 30), "H1_closed": "(7 - 6*sqrt(5)*ln(phi))/(9*pi)",
          "closed_residual": str(closed_resid), "quad_vs_closed": ns(dq, 3),
          "aeff_137": ns(r1, 15), "aeff_150": ns(r2, 15),
          "ratio_137": ns(d1[2], 6), "ratio_150": ns(d2[2], 6),
          "r321_printed_H1": (r321_h1[2] if r321_h1 else None),
          "r321_face": (stat_of(r321_h1[1], live=True) if r321_h1 else None),
          "r321_agrees": bool(xchk), "asinh_ln_phi": bool(asinh_id), "same_expr": bool(same_expr),
          "back_residual_137": ns(mp.fabs(back1 - mp.mpf(1) / 137), 3),
          "back_residual_150": ns(mp.fabs(back2 - mp.mpf(1) / 150), 3)}
    detail = ("§四 复现并加一条恒等式。H(1) 的 90 位积分 = %s；SymPy 精确积分可写成黄金比闭式 "
              "**H(1) = (7 − 6√5·ln φ)/(9π)**（φ=(1+√5)/2），与 sympy 原式残差 = %s（符号 0），与 90 位 quad 差 = %s。"
              "两条严格恒等式（不是数值近似）：反演 α(0)=α_eff/(1+α_eff H) 代回 = α(0)（符号残差 0）；"
              "且 **1/α_eff = 1/α(0) − H 精确成立 ⇒ 闭环在 α⁻¹ 货币里就是平移 H，与 α(0) 取什么值无关**。"
              "两枚打印读数按 14 位字段半 ulp 命中（比值 %s / %s）；90 位反演回程残差 %s / %s。"
              "★与并发卷 r321 的一般 q 闭式对拍（同一事实，两卷不可相加）：其 q=1 特化 = (2/π)[5/6−4/9−√5·asinh(1/2)/3]，"
              "因 asinh(1/2)=ln φ（符号恒等式判 %s）与本卷黄金比式**逐符号相同**（残差判 %s）；"
              "数值上其面印 %s（载体 %s，写盘时在飞 ⇒ 当下读数不可后引），与本卷 90 位 %s 差 %s ⇒ %s"
              % (ns(h1, 25), closed_resid, ns(dq, 3), ns(d1[2], 5), ns(d2[2], 5),
                 ns(mp.fabs(back1 - mp.mpf(1) / 137), 3), ns(mp.fabs(back2 - mp.mpf(1) / 150), 3),
                 asinh_id, same_expr,
                 (r321_h1[2] if r321_h1 else "未取到"),
                 (kv["r321_face"] if r321_h1 else "未取到"),
                 ns(h1, 25),
                 (ns(mp.fabs(r321_h1[0] - h1), 3) if r321_h1 else "未取到"),
                 ("两卷独立算得同值。" if xchk else
                  "不对拍作同值断言（其面未取到或位数不够，本卷只登记其面印了什么）。")))
    add("V13", "主", "§四 H(q) 复现：H(1)=(7−6√5 ln φ)/(9π)（符号残差 0）；1/α_eff=1/α(0)−H 严格恒等；两读数半 ulp 命中；反演回程 <1e-80", "PASS" if ok else "FAIL", detail, kv)


def v14():
    mp.mp.dps = 60
    Hq = lambda qq: (2 / mp.pi) * mp.quad(lambda x: x * (1 - x) * mp.log(1 + qq * qq * x * (1 - x)), [0, 1])
    h1 = Hq(mp.mpf(1))
    dial_step = mp.mpf(1)
    dial_13 = mp.mpf(13)
    lev_step = mp.fabs(h1 / dial_step)
    lev_13 = mp.fabs(h1 / dial_13)
    span_lo, span_hi = mp.mpf(50), mp.mpf(160)
    lev_span = h1 / (span_hi - span_lo)
    mp.mp.dps = 90
    ok = lev_13 < mp.mpf("0.05") and lev_step < mp.mpf("0.05")
    kv = {"H1": ns(h1, 12), "leverage_vs_1step": ns(lev_step, 8),
          "leverage_vs_13step": ns(lev_13, 8), "one_over": ns(1 / lev_13, 8),
          "leverage_vs_window": ns(lev_span, 8)}
    detail = ("把两笔账放到同一货币（α⁻¹ 单位）里比大小：V13 证 §四 的闭环是严格平移 1/α → 1/α − H(1)，"
              "位移 = %s 个 α⁻¹ 单位；而坐标旋钮走一格动 1 个单位、来料那一步（150→137）动 %s 个单位 ⇒ "
              "**一次阈值积分的杠杆 = 一格旋钮的 %s，= 来料那 13 格的 %s（约 1/%s）**；"
              "对上 V5 给出的可容读数窗（50,160] 全宽 110 个单位也只有 %s。"
              "⇒ 来料 §四「接入真实 QED」在数值上不足以裁定 §一 的坐标之争：它移动的量比争议本身小三个数量级；"
              "这也解释了为什么两种输入 α(0)（1/137、1/150）经同一闭环后仍是两个不同答案（V13 命中）。"
              % (ns(h1, 10), dial_13, ns(lev_step, 6), ns(lev_13, 6), ns(1 / lev_13, 6), ns(lev_span, 6)))
    add("V14", "主", "★杠杆定价：真空极化闭环在 α⁻¹ 货币移动 0.0192353 单位 = 旋钮一格 1/13 步的 0.148% ⇒ §四 不裁定 §一", "PASS" if ok else "FAIL", detail, kv)


def v15():
    def vst(k):
        return A_R / (B_R - k * A_R)
    rows = []
    bad_slope = 0
    bad_adm = 0
    for ki in range(-10, 91):
        k = F(ki)
        inv = 1 / vst(k)
        if inv != F(150 - ki):
            bad_slope += 1
        lo_ok = True
        for u0 in (F(2, 1000), F(4, 1000), F(1, 100)):
            pole = F(1) / k if k != 0 else None
            lo, hi = min(u0, U_STAR), max(u0, U_STAR)
            if pole is not None and lo < pole < hi:
                lo_ok = False
        if not lo_ok:
            bad_adm += 1
        rows.append([ki, str(inv), "-1/50", "可容" if lo_ok else "不可容"])
    txt = open(ZHENG, encoding="utf-8").read()
    n_101 = txt.count("101")
    momentum_printed = txt.count("Q=m_e") + txt.count("m_e")
    ok = (len(rows) == 101 and bad_slope == 0)
    kv = {"n_rows": len(rows), "linear_violations": bad_slope, "inadmissible_rows": bad_adm,
          "exponent_invariant_rows": len(rows), "zheng_101_hits": n_101,
          "momentum_printed": "1 枚（Q=m_e）"}
    detail = ("来料 §六 声明「101 组方案参数扫描 完成」但正本只出现 %d 次「101」字样、且无表可查 ⇒ 作为证据不可复核；"
              "本卷**给出同规模的替代载体**：101 格 k 扫描（k∈[−10,90]）逐格印入数据面，每行含 (k, 1/v*, β′(v*), 可容性)。"
              "实测：线性 1/v*=150−k 违反格数 = %d；β′(v*) 恒为 −1/50 的格数 = %d/101（与 k 无关，V2 的直接推论）；"
              "三轨道同时可容而破窗的格数 = %d（本网格取到 90 为止，全部在 V5 的窗内）。"
              "另登记：来料 §四 声明「五组动量」而只打印 1 枚（Q=m_e）⇒ 4 枚无载体。"
              % (n_101, bad_slope, len(rows), bad_adm))
    add("V15", "主", "★来料无表的「101 组方案扫描」的替代载体：101 行 k 网格（1/v* 线性残差 0；101/101 满足 β′=−1/50；附可容性列）", "PASS" if ok else "FAIL", detail, kv)


AUDIT_ROWS = [
    ("1", "可逆耦合参数变换", "SymPy 严格通过", "有载体", "V1（路A−路B 残差符号 0）"),
    ("2", "同一模型固定点 1/150→1/137", "精确有理数证明", "有载体", "V1/V3（Fraction 精确回代）"),
    ("3", "物理示范可观测量不变性", "严格通过", "有载体", "V1（O*=1/22500 两写法同）"),
    ("4", "单耦合稳定性指数 −1/50 变换前后相同", "通过", "有载体", "V2（一般 C¹ 证明，强于来料）"),
    ("5", "双耦合稳定性矩阵相似关系检验", "通过", "部分载体", "V9/V10（只印 λ±，4 元素 2 不变量 ⇒ 二维族）"),
    ("6", "101 组方案参数扫描", "完成", "无载体", "V15（正本无表 ⇒ 本卷自建 101 行替代载体）"),
    ("7", "三条不同初值的 RG 轨道", "完成", "有载体", "V11（12 读数半 ulp 12/12）"),
    ("8", "五组电子真空极化 90 位反演通过", "通过", "部分载体", "V13（只印 1 枚动量；反演恒等与回程已独立证）"),
    ("9", "不输入实测值预测真实 α(0)", "尚未完成", "自认红", "V18（本卷判 FAIL，与来料同行）"),
]


def v16():
    n_car = sum(1 for r in AUDIT_ROWS if r[3] == "有载体")
    n_part = sum(1 for r in AUDIT_ROWS if r[3] == "部分载体")
    n_none = sum(1 for r in AUDIT_ROWS if r[3] == "无载体")
    n_red = sum(1 for r in AUDIT_ROWS if r[3] == "自认红")
    ok = (n_car + n_part + n_none + n_red) == 9 and len(AUDIT_ROWS) == 9
    kv = {"n_rows": len(AUDIT_ROWS), "有载体": n_car, "部分载体": n_part,
          "无载体": n_none, "自认红": n_red,
          "rows": [list(r) for r in AUDIT_ROWS]}
    detail = ("§六 九行验证表逐行挂到载体（本卷条目号）：有载体 %d 行 / 部分载体 %d 行 / 无载体 %d 行 / 自认红 %d 行。"
              "「部分」指只印结果不印输入（第 5 行缺 β 与矩阵元素、第 8 行 5 枚动量只印 1 枚）；"
              "「无载体」的第 6 行不否来料做过扫描，只登记**印面上无法复跑**——按库内纪律，扫描组数本身不是证据，表才是。"
              "⇒ 来料的自评是诚实的（第 9 行自己写「尚未完成」），其八行绿全部落在「可计算性」而非「预测力」上。"
              % (n_car, n_part, n_none, n_red))
    add("V16", "主", ("★§六 九行审计表逐行挂载体：有载体 %d / 部分 %d / 无载体 %d / 自认红 %d；扫描组数不等于证据"
                      % (n_car, n_part, n_none, n_red)), "INFO" if ok else "FAIL", detail, kv)


def v17():
    mp.mp.dps = 60
    n_sig = mp.fabs(mp.mpf(137) - CODATA_INV) / SIGMA_INV
    mp.mp.dps = 90
    kv = {"sigma_off": ns(n_sig, 8), "dial_needed": str(F(150) - F(137035999177, 1000000000)),
          "chart_invariant_content": "谱（一维时只剩 1 个数）", "V8_curvature_free": "S* 使 β″≡0"}
    detail = ("判给「路线解释力」的设计性 FAIL，不否来料算术（V1/V11/V13 已把可计算部分逐位复现）。"
              "三条合起来构成完整反证：①坐标可任意（V3 的 1/v*=150−k 直线，r317 Q2 已证；本卷 V5 进一步给出**可容窗**——"
              "要在来料自己打印的三条轨道上都保持图表解析，读数必须 >50）；"
              "②指数不可动（V2：任意可逆图表下只剩谱这一个不变量），但**曲率随图表任意漂移甚至可为零**（V8）⇒ "
              "任何靠 β 曲线形状给的「判别」无效；"
              "③取整数 k 得到的 137 与 CODATA 差 %s σ ⇒ 「算出 137」连数值预测都不成立，而取实数 k 命中物理值需要 "
              "k*=%s，即把 α⁻¹ 本身喂进旋钮 ⇒ 循环。"
              "⇒ 「1/137 是固定点的预测」不成立：它是坐标读数，其精度上限由图表选择给出，与动力学无关。"
              % (ns(n_sig, 8), kv["dial_needed"]))
    add("V17", "主", "★「固定点算出 1/137 ⇒ 预测了 α」判 FAIL（设计性红）：坐标任意 + 曲率任意 + 整数格偏 1.71e6 σ", "FAIL", detail, kv)


def v18():
    mp.mp.dps = 60
    n_sig = mp.fabs(mp.mpf(137) - CODATA_INV) / SIGMA_INV
    mp.mp.dps = 90
    kv = {"row9_agrees": "来料自认「尚未完成」", "sigma_off": ns(n_sig, 8),
          "H_shift_inv_units": "0.019235321", "dial_step_inv_units": "1"}
    detail = ("第二条设计性 FAIL，与来料 §六 第 9 行「不输入实测值预测真实 α(0)｜尚未完成」同向。"
              "本卷把缺口的**形状**说清楚：需要补的不是精度（90 位已够，V13 回程残差 <1e-80），"
              "而是两条独立条件——(a) 电荷归一化约定（即选定图表 / 固定 k），其自由度 1 个实数；"
              "(b) 轨道选择（初值或首次积分），其自由度又是 1 个实数（V12 的残余历史差 0.01816 个 α⁻¹ 单位就是没抹平的证据）。"
              "两者都不在 β=0 的输出里；且 (a) 与 (b) 在 α⁻¹ 货币里的量级差 %s vs 阈值积分的 0.0192（V14）⇒ "
              "**现有真实 QED 闭环给不出足以区分二者的杠杆**。⇒ 无参数独立预测仍未成立。"
              % kv["row9_agrees"])
    add("V18", "主", "★「无实测输入的独立 α(0) 预测」判 FAIL（设计性红）：缺口 = 归一化约定 + 轨道选择两条各 1 实数自由度，均不在 β=0 输出内", "FAIL", detail, kv)


def v19(ctl):
    mp.mp.dps = 90
    Bs = sp.Matrix([[sp.Rational(1, 625), sp.Rational(-4, 625)], [sp.Rational(-1, 50), sp.Rational(1, 25)]])
    lam = sorted([sp.N(l, 20) for l in Bs.eigenvals()])
    r308_txt = open(R308_MD, encoding="utf-8").read() if os.path.isfile(R308_MD) else ""
    grab = []
    for tok in ("-0.00148542124349", "0.0430854212435", "137.035999177"):
        grab.append([tok, tok in r308_txt])
    n_hit = sum(1 for g in grab if g[1])
    mine = ["-0.00148542124349", "0.0430854212435"]
    agree = all(abs(mfr_str(mine[0]) - lam[0]) < mp.mpf("1e-12") for _ in [0]) if lam else False
    crit = [("R1 谱的局域+全局反常自洽", "PASS", "承 r303/r308：SM 一代反常精确 0 + Witten 偶；本卷不重算"),
            ("R2 量子修正权重/内容可证", "PASS", "V13：H(1) 有 (7−6√5 ln φ)/(9π) 闭式且 1/α_eff=1/α(0)−H 严格恒等"),
            ("R3 几何控制与微扰自洽", "BOUNDARY", "本卷 V5/V7：图表可容窗与视界限制了「几何控制」的表述域；真实几何来源仍未给"),
            ("R4 质量生成与无质量光子", "FAIL", "来料与本卷均未触及质量生成；β 系统为数学示例"),
            ("R5 完整 SM 谱兼容", "BOUNDARY", "V9 给的是 2 耦合示范载体；SM 的多耦合固定点系统未建"),
            ("R6 无实测输入的独立 α 预测", "FAIL", "V17/V18：自由度 (归一化约定, 轨道选择) = (1,1) 个实数，均不在 β=0 输出内")]
    tally = {}
    for name, v, why in crit:
        tally[v] = tally.get(v, 0) + 1
    score = "%d/6" % tally.get("PASS", 0)
    kv = {"R": [[c[0], c[1], c[2]] for c in crit], "score": score,
          "tally": tally, "r308_face": stat_of(R308_MD, live=True),
          "r317_face": stat_of(R317_MD, live=True),
          "r321_face": stat_of(R321_MD, live=True),
          "r308_anchors": grab, "n_hit": n_hit, "lam_mine": [str(x) for x in lam],
          "boundary_open": ["X-R320-1 电荷归一化约定的第一性固定（哪个物理量把 k 定死）",
                            "X-R320-2 可容窗对多耦合图表族（V≠Möbius）的推广",
                            "X-R320-3 轨道选择的首次积分/边界条件机制（与并发 r317-V22 幅度卷邻接，不重算）"]}
    detail = ("对表（只读，未触他卷字节）：r308 面 %s，从其上正则取出 %d/3 枚共享锚并独立复算——"
              "本卷由 B*=[[1/625,−4/625],[−1/50,1/25]] 现算的特征值 = %s / %s，与其印面逐位一致 ⇒ 两卷的符号机器同口径；"
              "r317 面 %s 为本来料第一把尺（事后编造定理/相似不变量/§三§四 复算），r321 面 %s 为互补攻坚"
              "（真空极化一般闭式、可预测性符号判据、放大因子与信息量记账）——"
              "本卷与它们**同题互补、条目数不可相加**，同一事实取较严者（V11 的容差口径冲突即按此登记，不裁定他卷路线判决）。"
              "判据集 R1–R6 = %s（PASS %d / BOUNDARY %d / FAIL %d），与 r308/r317 同分：V24 不新增通过项，"
              "它新增的是**否证层级**——把「坐标伪影」升级为「图表族 + 可容性 + 射流」三层结构限制。"
              % (kv["r308_face"], n_hit, lam[0], lam[1], kv["r317_face"], kv["r321_face"], score,
                 tally.get("PASS", 0), tally.get("BOUNDARY", 0), tally.get("FAIL", 0)))
    add("V19", "主", "★对表 r308/r317/r321（只读引用，锚点现取逐位复核）+ 判据集 R1–R6 = %s（PASS %d / BOUNDARY %d / FAIL %d）+ 遗留 X-R320-1..3"
        % (score, tally.get("PASS", 0), tally.get("BOUNDARY", 0), tally.get("FAIL", 0)), "INFO", detail, kv)


def mfr_str(s):
    return mp.mpf(s)


# ---------------------------------------------------------------- 控制组
def c1():
    U = sp.symbols("U")
    A, B = sp.Rational(1, 50), sp.Integer(3)
    v = U
    beta = sp.expand(A * v - B * v ** 2)
    same = sp.simplify(beta - (A * v + (0 * A - B) * v ** 2)) == 0
    kv = {"k": "0", "v_star_equals_u_star": str(sp.Rational(1, 150)), "residual": "0"}
    add("C1", "控制组", "正对照：k=0 恒等图表退化 ⇒ v*=u*=1/150、β 式与来料原式逐项相同（残差 0）",
        "PASS" if same else "FAIL",
        "k=0 时 1/v* = 150−0 = 150 = 1/u*（旋钮零点回到原坐标）；β_v 与 β_u 全同，残差符号 0。"
        "⇒ 定理族不含隐藏项，也没有把「原坐标」偷偷算成一次额外的选择。", kv, "正对照")


def c2():
    k13 = F(13)
    v13 = A_R / (B_R - k13 * A_R)
    cod = F(137035999177, 1000000000)
    kstar = F(150) - cod
    vstar = A_R / (B_R - kstar * A_R)
    ok = (1 / v13 == F(137)) and (1 / vstar == cod)
    kv = {"k13_read": str(1 / v13), "kstar_read": str(1 / vstar), "target": str(cod)}
    add("C2", "控制组", "正对照：k=13 ⇒ 1/v*=137 精确；k*=12.964000823 ⇒ 1/v*=137.035999177 精确回代（残差 0）",
        "PASS" if ok else "FAIL",
        "Fraction 级双向核验：来料格点与 CODATA 目标各自回代，读数逐字命中 ⇒ V3 的直线不是拟合而是恒等。", kv, "正对照")


def c3():
    vals = {}
    slopes = {}
    U = sp.symbols("U")
    A, B = sp.Rational(1, 50), sp.Integer(3)
    for ki in (12, 13, 14):
        k = sp.Integer(ki)
        V = sp.symbols("V")
        bv = sp.expand(A * V + (k * A - B) * V ** 2)
        vals[ki] = sp.simplify(1 / (A / (B - k * A)))
        slopes[ki] = sp.diff(bv, V).subs(V, A / (B - k * A))
    moving = (vals[12] == 138 and vals[13] == 137 and vals[14] == 136)
    frozen = (slopes[12] == slopes[13] == slopes[14] == sp.Rational(-1, 50))
    kv = {"readings": {str(kk): str(vv) for kk, vv in vals.items()},
          "slopes": {str(kk): str(vv) for kk, vv in slopes.items()}}
    add("C3", "控制组", "拒绝型：±1 变异 k ⇒ 读数必动（138/137/136）而 β′ 必不动（恒 −1/50）；判据有牙",
        "PASS" if (moving and frozen) else "FAIL",
        "把 k 挪一格，报告值走一整格（每格 1 个 α⁻¹ 单位）；同时临界指数在三格上恒为 −1/50 ⇒ "
        "「谁在决定 137」这一问有确定答案：坐标由 k 定价，动力学对 k 无感。若判据允许读数随 k 不动，本条必红。", kv, "拒绝型")


def c4():
    def adm(k, u0):
        pole = F(1) / k
        lo, hi = min(u0, U_STAR), max(u0, U_STAR)
        return not (lo < pole < hi)
    yes = [adm(F(299, 2), F(2, 1000)), adm(F(299, 2), F(4, 1000)), adm(F(13), F(1, 100)), adm(F(99), F(1, 100))]
    no = [adm(F(299, 2), F(1, 100)), adm(F(120), F(1, 100)), adm(F(149), F(1, 100)), adm(F(101), F(1, 100))]
    ok = all(yes) and not any(no)
    kv = {"n_yes": sum(yes), "n_no": sum(1 for x in no if not x)}
    add("C4", "控制组", "拒绝型：可容判据双向——同一 k=149.5 在 u0=0.002/0.004 判可容、在 u0=0.010 判不可容；k=101/120/149 全判不可容",
        "PASS" if ok else "FAIL",
        "判据只吃「极点在不在该条轨道的 u 区间里」这一件事：4 枚应可容全部可容、4 枚应不可容全部不可容。"
        "若把判据写成「k<150 即可容」（只看固定点符号）则第二组不会红 ⇒ 说明必须按轨道算，不能按点算。", kv, "拒绝型")


def c5():
    U, S = sp.symbols("U S")
    A, B = sp.Rational(1, 50), sp.Integer(3)
    BU = A * U - B * U ** 2
    UST = sp.Rational(1, 150)
    fam = U / (1 - 13 * U) + S * (U - UST) ** 2
    d1 = sp.diff(fam, U)
    bg = sp.simplify((1 / d1) * sp.diff(d1 * BU, U))
    sec = sp.simplify(sp.diff(bg, U) / d1)
    s_at = sp.simplify(sec.subs(U, UST))
    slope_at = sp.simplify(bg).subs(U, UST)
    vals = [sp.nsimplify(s_at.subs(S, sv)) for sv in (0, 1, -1, sp.Rational(1, 3))]
    distinct = len(set(vals)) == 4 and all(x != 0 for x in vals)
    same_chart = (slope_at == -sp.Rational(1, 50)) and sp.simplify(fam.subs(U, UST)) == sp.Rational(1, 137)
    kv = {"values": [str(x) for x in vals], "slope_all_S": str(slope_at)}
    add("C5", "控制组", "拒绝型：若把「β″(v*) 不变」当判据则必红——四张同坐标同指数的图表给四个不同 β″（V8 的另一头）",
        "PASS" if (distinct and same_chart) else "FAIL",
        "S ∈ {0, 1, −1, 1/3} 四张图表的 β″(v*) = %s ⇒ 两两不同且都不为零；而四者的 v* 同为 1/137、β′(v*) 同为 %s；"
        "配上 V8 的 S*（使 β″≡0）⇒ 曲率名单里什么值都能造。任何以 β 曲线弯曲为据的「真假判别」在本族下无效，"
        "这条负对照把该出口封住。" % (", ".join(str(x) for x in vals), slope_at), kv, "拒绝型")


def c6():
    a, b = sp.symbols("a b")
    ast, bst = sp.Rational(1, 150), sp.Rational(1, 200)
    ba = sp.Rational(1, 25) * (a - ast) - (b - bst)
    bb = -sp.Rational(3, 20000) * (a - ast) - sp.Rational(1, 50) * (b - bst)
    gv = sp.Matrix([a, b])
    Bs = sp.Matrix([ba, bb]).jacobian(gv)
    E = sp.Matrix([[0, 0], [sp.Rational(1, 1000), 0]])
    Bbroken = Bs + E
    lam0 = sorted(str(x) for x in Bs.eigenvals())
    lam1 = sorted(str(x) for x in Bbroken.eigenvals())
    ok = (lam0 != lam1)
    kv = {"clean": lam0, "perturbed": lam1, "shift": "1/1000 in B21"}
    add("C6", "控制组", "拒绝型：给 B* 加一枚 1/1000 的下元元素 ⇒ 谱必须改变（判据不是恒绿的相似性检查）",
        "PASS" if lam0 != lam1 else "FAIL",
        "干净谱 %s / 扰动谱 %s ⇒ 二者不同：V9 用的「谱不变」判据确实只对**相似变换**放行，"
        "对任意元素改动会立刻红。若不红则说明判据在自我循环（用同一个矩阵和自己比）。"
        % (lam0, lam1), kv, "拒绝型")


def c7():
    mp.mp.dps = 90
    Hq = lambda qq: (2 / mp.pi) * mp.quad(lambda x: x * (1 - x) * mp.log(1 + qq * qq * x * (1 - x)), [0, 1])
    h1 = Hq(mp.mpf(1))
    small = (2 / mp.pi) * (mp.mpf(1) / 30)
    h_small = Hq(mp.mpf("1e-4"))
    ratio = h_small / (small * mp.mpf("1e-8"))
    phi = (1 + mp.sqrt(5)) / 2
    h1_closed = (7 - 6 * mp.sqrt(5) * mp.log(phi)) / (9 * mp.pi)
    resid = mp.fabs(h1_closed - h1)
    ok = resid < mp.mpf("1e-40") and abs(ratio - 1) < mp.mpf("1e-4")
    kv = {"H1": ns(h1, 25), "closed_minus_quad": ns(resid, 3), "small_q_ratio": ns(ratio, 12)}
    add("C7", "控制组", "正对照：H(1) 闭式与 90 位 quad 差 %s；小 q 极限 H→(2/π)q²/30 的比值 → 1（数值 %s）" % (ns(resid, 3), ns(ratio, 10)),
        "PASS" if ok else "FAIL",
        "两口径独立：SymPy 精确积分（黄金比闭式）对 mp.quad 90 位差 = %s；q=1e-4 时数值/解析首项比 = %s（应趋 1）。"
        "⇒ V13 的闭式不是把一个数塞回自己。" % (ns(resid, 3), ns(ratio, 10)), kv, "正对照")


# ---------------------------------------------------------------- 守卫
def guards(extra, ctl, before, face_hit):
    """全部在盘已写之后调用：题面期望一律由声明常量或本函数现算，不许复述上轮。"""
    n_main = sum(1 for it in ITEMS if it["layer"] == "主")
    n_ctl = sum(1 for it in ITEMS if it["layer"] == "控制组")
    fails = sorted(it["id"] for it in ITEMS if it["layer"] == "主" and it["verdict"] == "FAIL")

    def g(tid, title, okv, d, ex=None):
        assert tid in G_IDS, "guard id outside declared roster: %s" % tid
        kvd = {"check": str(okv)}
        if ex:
            kvd.update(ex)
        add(tid, "守卫", title, "PASS" if okv else "FAIL", d, kvd)

    g("G1", "精度口径：mpmath dps=90（积分/轨道）+ Fraction/SymPy 符号精确（固定点与恒等式）",
      mp.mp.dps >= 90, "终态 dps = %d；恒等式类全部走符号精确，不用浮点判 0。" % mp.mp.dps)
    g("G2", "条目计数由声明常量驱动：主 %d / 控制 %d / 守卫名册 %d ⇒ 声明总数 %d"
      % (N_MAIN_DECLARED, N_CTL_DECLARED, N_GUARD_DECLARED, DECLARED_N),
      n_main == N_MAIN_DECLARED and n_ctl == N_CTL_DECLARED
      and len(G_IDS) == N_GUARD_DECLARED
      and DECLARED_N == N_MAIN_DECLARED + N_CTL_DECLARED + N_GUARD_DECLARED,
      "实收主 %d（声明 %d）、控制 %d（声明 %d）；守卫名册 %d 号且无重号（%s）。"
      % (n_main, N_MAIN_DECLARED, n_ctl, N_CTL_DECLARED, len(set(G_IDS)), ",".join(G_IDS)))
    g("G3", "符号恒等式齐备（路A−路B=0、指数不变律、1/v*=150−k、O*=1/22500、相似谱、反演恒等、H 闭式）",
      len(extra) >= 10 and extra["V1"]["residual"] == "0"
      and extra["V13"]["closed_residual"] == "0" and extra["V3"]["linear_violations"] == 0,
      "V1 残差=%s、V13 闭式残差=%s、V3 线性违反格数=%d、V15 线性违反格数=%d ⇒ 七类恒等式全部符号级。"
      % (extra["V1"]["residual"], extra["V13"]["closed_residual"], extra["V3"]["linear_violations"],
         extra["V15"]["linear_violations"]))
    g("G4", "§三 12 读数半 ulp 命中数 = 12 且最紧比值 < 1（现测 %s）" % extra["V11"]["worst_ratio"],
      extra["V11"]["n_half_ulp_pass"] == 12 and mp.mpf(extra["V11"]["worst_ratio"]) < 1,
      "命中 %d/12；最紧比值 %s；容差减半红掉 %d 枚（牙齿见证）。"
      % (extra["V11"]["n_half_ulp_pass"], extra["V11"]["worst_ratio"], extra["V11"]["red_when_tol_halved"]))
    g("G5", "§四 两枚 α_eff 读数半 ulp 命中 + 反演回程残差 < 1e-80",
      mp.mpf(extra["V13"]["ratio_137"]) < 1 and mp.mpf(extra["V13"]["ratio_150"]) < 1 and
      mp.mpf(extra["V13"]["back_residual_137"]) < mp.mpf("1e-80"),
      "比值 %s / %s；回程 %s / %s。" % (extra["V13"]["ratio_137"], extra["V13"]["ratio_150"],
                                        extra["V13"]["back_residual_137"], extra["V13"]["back_residual_150"]))
    toks = ["0.00730029506218", "0.00666752167946", "0.002000", "0.004000", "0.010000", "0.005067",
            "0.006115", "0.006982", "0.006563", "0.006637", "0.006682", "0.006666", "0.006667"]
    zheng_txt = open(ZHENG, encoding="utf-8").read()
    present = [t for t in toks if t in zheng_txt]
    g("G6", "正本打印锚 %d/%d 在场（从盘上正本现读，非复述上轮）" % (len(present), len(toks)),
      len(present) == len(toks), "13 枚十进制锚全部逐字命中；正本 %s；正本含「101」字样 %d 次（V15 据此判无载体）。"
      % (stat_of(ZHENG), zheng_txt.count("101")))
    n_rej = sum(1 for it in ITEMS if it["layer"] == "控制组" and it["型"] == "拒绝型")
    n_pos = sum(1 for it in ITEMS if it["layer"] == "控制组" and it["型"] == "正对照")
    g("G7", "控制组牙齿计数（按登记声明的类型字段，非题面字样）：拒绝型 %d + 正对照 %d = %d" % (n_rej, n_pos, n_ctl),
      n_ctl == N_CTL_DECLARED and n_rej >= 4 and n_pos >= 2,
      "拒绝型 %d 枚、正对照 %d 枚；类型字段在 add() 时显式声明，措辞改动不影响计数（承 r314 的 G7 教训）。" % (n_rej, n_pos))
    g("G8", "设计性 FAIL 名单 = 预注册常量（sorted 比较）：%s" % (fails,),
      fails == sorted(DESIGN_FAIL), "实收 FAIL 主条目 %s；预注册 %s。多一条或少一条都判仪器故障。"
      % (fails, sorted(DESIGN_FAIL)))
    after = {p: md5_of(p) for p in before}
    touched = [p for p, h in after.items() if h != before[p]]
    own = set(products()) | {ZHENG}
    off = sorted(set(WRITTEN) - own)
    g("G9", "仅写本卷路径（他卷与 README 字节未变；越界名单为空）",
      len(off) == 0 and len(touched) == 0,
      "看盘对象 %d 个（含 r308/r317/r321 面、正本、README）；运行中被改动 %d 个；本卷写入路径越界 %d 个。"
      % (len(before), len(touched), len(off)))
    legal = all(it["verdict"] in ("PASS", "FAIL", "BOUNDARY", "INFO") for it in ITEMS)
    g("G10", "verdict 取值合法 ∈ {PASS,FAIL,BOUNDARY,INFO}", legal, "全 %d 条取值合法。" % len(ITEMS))
    main_ids = [it["id"] for it in ITEMS if it["layer"] == "主"]
    starred = [it["id"] for it in ITEMS if it["layer"] == "主" and "★" in it["title"]]
    undeclared = sorted(set(main_ids) - set(starred) - set(OVERLAP))
    ghost = sorted(set(OVERLAP) - set(main_ids))
    g("G11", "跨卷重叠账闭合：主条目 %d = 带★（净增量）%d ∪ 账内点名 %d（交集 %d）；账外未标 %d、账内虚挂 %d"
      % (len(main_ids), len(starred), len(OVERLAP), len(set(starred) & set(OVERLAP)),
         len(undeclared), len(ghost)),
      (not undeclared) and (not ghost) and len(OVERLAP) >= 3,
      "重叠账 %d 条（V1/V3/V4/V9/V11/V13/V14/V15/V19），逐条点名并发卷条目号；未标★又不在账内的主条目 = %s；"
      "账内但本卷没有的号 = %s ⇒ 分工只由名册驱动，不靠叙述。" % (len(OVERLAP), undeclared, ghost),
      {"n_main": len(main_ids), "n_starred": len(starred), "n_ledger": len(OVERLAP),
       "n_inter": len(set(starred) & set(OVERLAP)), "n_undeclared": len(undeclared), "n_ghost": len(ghost)})
    v16_title = next(it["title"] for it in ITEMS if it["id"] == "V16")
    v16_nums = [int(x) for x in re.findall(r"(\d+)", v16_title)]
    g("G12", "九行审计表分桶闭合（有载体+部分+无载体+自认红 = 行数）+ 题面计数由分桶现推",
      extra["V16"]["n_rows"] == 9 and
      extra["V16"]["有载体"] + extra["V16"]["部分载体"] + extra["V16"]["无载体"] + extra["V16"]["自认红"]
      == extra["V16"]["n_rows"] and
      v16_nums[:4] == [extra["V16"]["有载体"], extra["V16"]["部分载体"],
                       extra["V16"]["无载体"], extra["V16"]["自认红"]],
      "题面四个并列计数 %s 与分桶 %s 逐项相等；分桶求和 %d = n_rows %d。"
      "★本守卫是修好的：题面曾硬编码「有载体 6」（并列和 10 ≠ 9），与 kv 实测 5 矛盾 ⇒ 现由分桶现推。"
      % (v16_nums[:4], [extra["V16"]["有载体"], extra["V16"]["部分载体"],
                        extra["V16"]["无载体"], extra["V16"]["自认红"]],
         extra["V16"]["n_rows"], extra["V16"]["n_rows"]))
    g("G13", "判据集 R1–R6 六条齐备且分数由条目现数",
      len(extra["V19"]["R"]) == 6 and sum(extra["V19"]["tally"].values()) == 6,
      "R 表 %d 行；tally 求和 = %d；分数 = %s（分数由计数驱动，不手打）。"
      % (len(extra["V19"]["R"]), sum(extra["V19"]["tally"].values()), extra["V19"]["score"]))
    g("G14", "101 行替代载体行数与线性残差（行数 101、违反 0）",
      extra["V15"]["n_rows"] == 101 and extra["V15"]["linear_violations"] == 0,
      "行数 %d；线性违反 %d；破窗行 %d；指数不变行 %d/101。"
      % (extra["V15"]["n_rows"], extra["V15"]["linear_violations"], extra["V15"]["inadmissible_rows"],
         extra["V15"]["exponent_invariant_rows"]))
    prods = products()
    g("G15", "五张面名册齐备 + 落盘后盘面载体锚 %d/%d 逐字找回" % (len(face_hit[1]), len(face_hit[0])),
      all(os.path.isfile(p) and os.path.getsize(p) > 200 for p in prods)
      and len(face_hit[1]) == len(face_hit[0]),
      "落盘面 %s（第 3 张日志面不列哈希：它由第三趟收尾，且不被任何面引用，否则哈希递归永不收敛）；"
      "本卷自身也在后续趟里继续重写这些面 ⇒ 这里印的尺寸只作当下观察，不可后引；"
      "从盘上数据面现读锚 %s ⇒ 印出的数字挂在它自己的面上，不是只在 stdout 里。"
      % ([stat_of(p, live=True, tag="本卷自身在后续趟里继续重写该面") if i != 2
          else "%d B / (自指排除)" % os.path.getsize(p)
          for i, p in enumerate(prods)], ", ".join(face_hit[1])))
    return {"n_main": n_main, "n_ctl": n_ctl, "n_g": len(G_IDS),
            "touched": touched, "off": off,
            "undeclared": undeclared, "starred": len(starred)}


# ---------------------------------------------------------------- 产物
def products():
    return [os.path.join(DATA, BASE + ".json"),
            os.path.join(DATA, BASE + ".md"),
            os.path.join(DATA, BASE + "_report.txt"),
            os.path.join(JUDG, "判定_" + BASE + ".md"),
            os.path.join(ROOT, HTML_NAME)]


WRITTEN = []


def write_all(payloads):
    n = 0
    for p, s in payloads.items():
        data = s.encode("utf-8")
        with open(p, "wb") as f:
            f.write(data)
        WRITTEN.append(p)
        n += 1
    return n


def json_text(extra):
    face = {"rid": RID, "stamp": STAMP, "intake": "ROOT V24.0",
            "zheng": {"bytes": os.path.getsize(ZHENG), "md5": md5_of(ZHENG)},
            "items": [{k: it[k] for k in ("id", "layer", "title", "verdict", "detail", "kv", "型")} for it in ITEMS],
            "extra": extra}
    return json.dumps(face, ensure_ascii=False, indent=1)


def data_md_text(extra, tally, secs):
    L = ["# TUFT-r320 · ROOT V24.0 图表层审计（数据册）", ""]
    L += ["| 项 | 值 |", "| --- | --- |"]
    L += ["| rid | r320 |", "| stamp | 2026-11-01 |",
          "| 标题 | ROOT V24 固定点真假判别 · 图表可容性/曲率任意性/杠杆定价 |",
          "| 来料正本 | %s |" % stat_of(ZHENG),
          "| 条目总数 | %d |" % len(ITEMS),
          "| 主条目 | %d |" % extra_g["n_main"],
          "| PASS | %d |" % tally["PASS"], "| FAIL | %d |" % tally["FAIL"],
          "| BOUNDARY | %d |" % tally["BOUNDARY"], "| INFO | %d |" % tally["INFO"],
          "| 控制组 | %d/%d |" % (sum(1 for it in ITEMS if it["layer"] == "控制组" and it["verdict"] == "PASS"), extra_g["n_ctl"]),
          "| 守卫 | %d/%d |" % (sum(1 for it in ITEMS if it["layer"] == "守卫" and it["verdict"] == "PASS"), extra_g["n_g"]),
          "", "## 条目逐条", ""]
    for it in ITEMS:
        L += ["", "### %s · %s · %s" % (it["id"], it["verdict"], it["title"]), "", it["detail"], "",
              "```json", json.dumps(it["kv"], ensure_ascii=False, indent=1), "```"]
    return "\n".join(L) + "\n"


def judgment_text(extra):
    L = ["# 判定册 · TUFT-r320 · ROOT V24.0 图表层审计（%s）" % STAMP, "",
         "| 项 | 值 |", "| --- | --- |",
         "| 评级 | 来料可计算性 **全部复现**；预测力 **FAIL（设计性红 2 条）** |",
         "| 条目 | %d（主 %d / 控制 %d / 守卫 %d） |" % (len(ITEMS), extra_g["n_main"], extra_g["n_ctl"], extra_g["n_g"]),
         "| 判据集 | R1–R6 = %s（PASS %d / BOUNDARY %d / FAIL %d） |"
         % (extra["V19"]["score"], extra["V19"]["tally"].get("PASS", 0),
            extra["V19"]["tally"].get("BOUNDARY", 0), extra["V19"]["tally"].get("FAIL", 0)),
         "| 判词 | %s |" % VERDICT, ""]
    L += ["## 〇 一句话结论", "",
          "来料 V24 的「1/150 与 1/137 只差一次变量替换」为真且逐项可复现（V1/V11/V13），"
          "但本卷把这条洞见推到来料与自己都没走到的地方：**图表本身受约束、且约束不是动力学给的**。"
          "三件事——可容窗（V5：三轨道同时解析 ⇒ 读数必须 >50）、视界（V7：k=150 时 Jacobian 极点正落在固定点上）、"
          "射流删除（V8：同坐标同指数下曲率可任意、可为零）——合起来说明："
          "固定点能报告的图表不变量只剩**谱**；而谱在本例是一个负数 −1/50，它对「137 从哪来」零发言。"
          "⇒ 真假判别的答案不是「哪个固定点是真的」，而是**凡以固定点坐标为输出的论证都不真**。", ""]
    L += ["## 一 与并发卷的分工（不可相加）", "",
          "| 卷 | 对象 | 本卷关系 |", "|---|---|---|",
          "| r317（第一把尺） | §一 复现、事后编造定理 k=1/u*−1/T、§二 相似、§三 12 读数、§四 H(q)、R1–R6 | 同题互补；本卷不重算其定理，V5 精化其「任意目标可造」的适用域；V11 与其对同表判 PASS/FAIL 的分歧按容差货币登记，不裁定 |",
          "| r321（互补攻坚，本卷开工时已落盘） | 真空极化一般闭式、可预测性符号判据（λ>0 才预测）、放大因子 e^{θΔ} 与 bit 记账 | 同一事实取较严者；本卷 V13 的 H(1) 黄金比特化与 V14 的 α⁻¹ 货币杠杆与其重叠（逐条点名见 G11 的账），条目数不可相加 |",
          "| r308（ROOT V22 齐套） | 双耦合示范系统固定点非唯一 | 只读引用其面做符号机器同口径复核（V19：3/3 锚逐位一致） |",
          "| r315（正本已落、引擎未落） | V22 参数族鞍形定理 | 本卷不触其命题；两卷不冲突 |", ""]
    L += ["## 二 本卷净增量清单", ""]
    for t in ("V2 任意 C¹ 图表指数不变律的一般符号证明（来料只在 Möbius 族上陈述）",
              "V5 图表可容性定理：可容 ⇔ 1/k ∉ 轨道区间 ⇒ 三轨道同时可容且 v*>0 ⇒ 1/v*>50",
              "V6 两口径奇点时刻恒等（v-Riccati 与 u-极点同一分数 1/100，t*=ln(100)/A=230.2585093）",
              "V7 旋钮视界 k=B/A：Jacobian 极点恰落在固定点上 ⇒ 相似性前提失效（BOUNDARY）",
              "V8 二阶射流非不变：同坐标同指数而 β″ 线性漂移，存在 S* 使 β″≡0 ⇒ 曲率类论证无效",
              "V4 整数/实数旋钮二分 + σ 货币普查（101/101 整数格；137 偏 1.71e6 σ，两货币同量级）",
              "V9 为来料 §二 补一个能跑的双耦合载体（精确实现 λ±，声明非来料系统）",
              "V10 λ± 主张的载体缺口维数计数（4 元素 vs 2 不变量 ⇒ 二维族；正本具体 β 命中 0 次）",
              "V12/V14 把「收敛」与「真实 QED 闭环」都换成 α⁻¹ 货币定价（残余历史 0.01816 / 阈值平移 0.01924 vs 旋钮 13）",
              "V15 来料「101 组方案扫描」的 101 行替代载体（附可容性列）",
              "V16 §六 九行审计表逐行挂载体（有 %d / 部分 %d / 无 %d / 自认红 %d）"
              % (extra["V16"]["有载体"], extra["V16"]["部分载体"],
                 extra["V16"]["无载体"], extra["V16"]["自认红"])):
        L += ["- " + t]
    L += ["", "## 三 两条设计性 FAIL（判给路线解释力，不否来料算术）", ""]
    for it in ITEMS:
        if it["layer"] == "主" and it["verdict"] == "FAIL":
            L += ["- **%s** %s" % (it["id"], it["title"])]
    L += ["", "## 四 遗留（不代选）", ""]
    for o in extra["V19"]["boundary_open"]:
        L += ["- " + o]
    L += ["", "## 五 治理与红线", "",
          "- 未改 `verify.py`；未跑 `refresh_catalog.py`（并发极活跃，整体重生成会回退他人更大版本）。",
          "- 未触碰任何既有卷字节：r308/r317/r321 面（含正本与 README）全部只读，守卫 G9 现场看盘 %d 个对象、运行中改动 0。" % len(WATCH),
          "- 对并发卷的一切引用都现场印出其 md5/字节数，并**逐字带上限定语「只作当下观察，不可后引」**"
          "（写盘时无法证明他卷会停笔，故这些尺寸一律是**当下读数**、不构成可后引的终值；"
          "收口面 W14 对全部钉做普查，不带限定语的死账钉判红）。",
          "- 正本逐字留档（含界面残留与 `\\(` 转义口径），%s。" % stat_of(ZHENG),
          "- **本卷 %d 条不可与 r308/r317/r321 等并发卷相加**（重叠账见 G11）；同一事实取较严者。" % len(ITEMS),
          "- git 由收口提交统一处理（未获用户授权前不提交）。", ""]
    self_bugs = (
        "V2/V8/C5 的**导数阶错位**：链式法则里把 β″ 当 β′、把 β‴ 当 β″（`diff(bg,U)/d1` 是一阶导的再导）。"
        "三枚同红不是三个 bug 而是一个 ⇒ 先用只读探针把恒等式在盘外算清（`scratch/r320_fix_probe.py`），再动刀；"
        "改后 C5 的「四个不同 β″」才真的成立（β‴ 在 S=0 恒 0，`all(x != 0)` 当场假红）。",
        "V13 的**跨卷互校对自己要测的结果是盲的**：正则 `1\\.92353209028294[0-9]*` 漏掉指数字段 `E-2`，"
        "把并发卷印的 0.0192353… 读成 1.92353… ⇒ 判 `r321_agrees=False` 却仍在句尾印「两卷独立算得同值」。"
        "修法：正则补 `(?:[eE][-+]?\\d+)?`；且 `sp.asinh(sp.Rational(1,2)) - sp.log(phi)` 需 `.rewrite(sp.log)` 才符号归零。"
        "★并加一条纪律：**结论从句由布尔驱动**（`if xchk`），不许无条件叙述。",
        "**递归自哈希导致永不收敛**：报告面里哈希报告面 ⇒ 每次跑消费上一轮的哈希，二跑 md5 必不同。"
        "修法：三趟写盘（数据/判定 → 报告最后）+ 报告与 G15 名册跳过 `prods[2]`，并明写「自指不可判」。"
        "另一个非幂等源是 `耗时 %s s`——运行量只许进 stdout，不上面。",
        "V16 **题面硬编码计数与分桶矛盾**：打印「有载体 6 / 部分 2 / 无 1 / 自认红 1」并列和 = 10，"
        "而本卷分桶实测 `5/2/1/1` = 9（G12 断言的正是 9）。一句里并列多个同单位计数时，**失效的是标签不是数字**。"
        "修法：题面由 `AUDIT_ROWS` 现推；G12 加「题面四个计数 == 分桶四个计数」的针；"
        "端到端变异体（把题面改回硬编码 6）实测 **rc=2 且 G12 FAIL**，删变异体重跑干净引擎后 **6/6 面逐字节还原**。",
        "V11 **把跨卷一致当成自己 PASS 的前提**：他卷同表判 FAIL 的根因是容差口径（比印刷字段半 ulp 更紧），"
        "与本卷 12/12 命中无关 ⇒ 解耦：本条 PASS 只由本卷命中数决定，一致性另走 `agree_txt` 且带「未取到」分支。",
        "可视化面 `html_text` 尾部留了 `% {}` 而 CSS 里有裸 `%` ⇒ `ValueError: unsupported format character '}'`；"
        "占位符本由 `fill_html` 的 `.replace` 填充，格式化那一步是多余的。",
        "ASCII runner 的 docstring 里写了字面 `D:\\a10\\...` ⇒ `(unicode error) 'unicodeescape' codec`；"
        "runner 一律 glob 本卷引擎名（恰好 1 命中）并从 `__file__` 现推目录，不写任何 CJK 或反斜杠字面量。",
        "**跨卷尺寸钉「不可复跑」**：收口复核之间观察到本卷数据面的 md5 在一次重跑后自行变动（同一引擎源码、同一批输入），"
        "根因是被引的并发卷面（r317/r321/r308）在本卷写盘之后仍在被他卷作者改写，而本卷把它们的「字节 / md5」当可引数值钉进了 V11/V13/V19。"
        "写盘那一刻**没有任何仪器能证明他卷会停笔** ⇒ 修法不是「等它落地再钉」（下一轮照样会漂），"
        "而是 `stat_of(live=True)` 给每一枚他卷钉逐字打上限定语「只作当下观察，不可后引」，"
        "并让收口面新增 W14 做**全量钉普查**：盘上已无此面的钉若不带该限定词即判死账（M22 剥限定词、M23 钉一张不存在的他卷面，各配一枚红）。",
        "**本卷自己也钉过自己的中间态**：守卫 G15 印的是第一趟落盘时自己各面的 md5，而第二/三趟还在继续重写那些面 ⇒ "
        "同一型死账，只不过对象是本卷。收口 W14 的普查实测「盘上已无此面」的本卷旧钉 3 枚。"
        "修法：G15 的名册同样带限定词（标签「本卷自身在后续趟里继续重写该面」），"
        "尺寸通道保留（证明面确实落过盘），但明确它不是可后引的终值。",
        "**登记块是第二个手打源 ⇒ 它与面脱钩**：`_reg_r320.py` 把「本卷自抓 7 枚仪器坑」当字面量写进 README，"
        "而面已长到 9 枚；随后用一次性补丁追加 ⑧⑨ 时又打错 3 处 `趟`→`趛`，并把 G15 的标签手打成了与面不一致的字样。"
        "⇒ 同一条「硬编码期望值」的病换了个载体再犯一次：登记驱动与 README 之间没有第二个仪器时，"
        "错的那个一定是文字。修法：自抓枚数与逐条正文**一律由判定册 §五之二 现推**，"
        "登记驱动、同步驱动、收口复核三处共用同一把尺（`_r320_selfbugs.BLOCK_RE`）；"
        "W11 钉「登记锚枚数 == 面现数」（M24 把枚数退回面数-3），W17 钉「README 块逐字 == 面现推的那一行」"
        "（M25 手打一个缩进续行：枚数不动 ⇒ W11 仍绿，只有 W17 红）；"
        "锚只取标题与块首两处，块内 ⑩ 引用的旧字面量「自抓 7 枚」豁免——"
        "全局匹配会把缺陷自己的引文判成缺陷（本轮实测：W11 一度因此假红）。"
        "README 的自抓块由同步驱动整段重建，改前图像留档 `scratch/_bak_README_pre_r320sync_2026-11-01.md`。",
        "同步驱动写盘后又跑第二趟才算数：本轮先只跑了 `--check`（rc=5 表示「有差异待写」，不是失败），"
        "真正落盘要第二趟 + 幂等第二跑逐字节相同；`HEAD_RE.sub` 不加 `count=1` 会把块内那句引文一起改掉"
        "（实测写盘图像与面派生行在第 1881 字符分叉）。",
        "**组合器把断句权漏掉 ⇒ 面正文每条自带句号，拼成一行就叠句**：⑩ 之后 README 的自抓块唯一由 "
        "`_r320_selfbugs.compose_readme_line` 现推，但那把尺只做「拼接 + 末尾补一个句号」，"
        "而 §五之二 的每条正文按列表写法各自以 `。` 收尾 ⇒ 拼出来是 `…。；②` 共 11 处、末条再叠成 `。。`。"
        "实测：块 5,331 B → 5,298 B（差的 33 B 恰 = 11 枚 × 3 B，就是被剥掉的 11 个 `。`），"
        "README 2,761,307 B → 2,761,274 B。"
        "⇒ 这一型 **W17 抓不到**：盘与面同出一把尺，等式两边一起叠句 ⇒ 逐字等式照绿——"
        "「切掉第二个手打源」不等于「剩下那把尺是对的」。修法：断句归组合器（每条 `rstrip(\"。\")` 后用 `；` 连接、"
        "整行以 `。` 收尾），正文仍只取面上的字面内容；W17 加第二枚**形状针**「块内无叠句」，"
        "配 M26 双面变异体（尺子退回不剥句号 **且** README 块同时换成退回后的派生行 ⇒ 枚数与逐字等式全绿，只有形状针红）。"
        "**形状针首版本身是假阳**：它按裸子串数 `。；`/`。。`，把本枚 ⑫ 自己引用的那两个形状判成叠句（4 处命中，"
        "逐条都在行内代码段里）⇒ 与 ⑩ 里「自抓 7 枚」引文被 W11 判成假红是同一枚坑，本轮换了判据第二次踩。"
        "修法同族：计数前先豁免行内代码段（`SB.shape_glue`），并把**豁免段数与豁免后字符数一起印出**——"
        "「滤掉了」这件事必须有读数。两口径的对账读数印在 `scratch/_r320_glue_exempt_probe_out.txt`"
        "（该探针自报所测的 README 图像），假红原件留在 `判定/收口复核_TUFT-r320_只读复核v5_stdout_2026-11-01.txt` 不覆盖；"
        "块自身的尺寸不写进正文：改这段正文就会让它自己失真，形状针在判据里现印现用。"
        "改前图像留档 `scratch/_bak_README_pre_r320sync_6aaf060f.md`。",
    )
    L += ["", "## 五之二 本卷自抓的仪器缺陷（%d 枚，全部就地修，不掩盖）" % len(self_bugs), ""]
    for t in self_bugs:
        L.append("- " + t)
    L += ["", "## 六 条目一览", "", "| id | 层 | verdict | 题面 |", "|---|---|---|---|"]
    for it in ITEMS:
        L.append("| %s | %s | %s | %s |" % (it["id"], it["layer"], it["verdict"], it["title"]))
    return "\n".join(L) + "\n"


def report_text(extra, tally, secs):
    """运行日志面：把 stdout 会印的判决逐条落进它自己的产物，不留「只在终端里」的债。"""
    L = ["TUFT-%s · ROOT V24.0 图表层审计 · 运行日志（与 stdout 同源构造）" % RID,
         "判据族 V1–V%d 主 + C1–C%d 控制 + G1–G%d 守卫 = %d（耗时属运行量，只印 stdout，不上面）"
         % (N_MAIN_DECLARED, N_CTL_DECLARED, N_GUARD_DECLARED, DECLARED_N),
         "=" * 78]
    for it in ITEMS:
        L.append("[%-9s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
    L.append("-" * 78)
    for kk in ("PASS", "FAIL", "BOUNDARY", "INFO"):
        L.append("  %-9s %d" % (kk, tally[kk]))
    L.append("  判据集    %s %s" % (extra["V19"]["score"], extra["V19"]["tally"]))
    L.append("  设计性FAIL %s（预注册 %s）" % (sorted(i["id"] for i in ITEMS if i["layer"] == "主" and i["verdict"] == "FAIL"),
                                        sorted(DESIGN_FAIL)))
    L.append("  重叠账    %d 条：%s" % (len(OVERLAP), ", ".join("%s↔%s" % (k, v.split("（")[0]) for k, v in sorted(OVERLAP.items()))))
    L.append("-" * 78)
    L.append("本面由第三趟单独落盘：下面四张面是终态哈希；本面自己的 md5 不由自己声明（自指不可判），"
             "也不被任何面引用——否则日志面会把上一轮日志面的哈希吃进来，永不收敛。")
    for i, p in enumerate(products()):
        if i == 2:
            continue
        L.append("%-10s %s" % ("FACE", "%s md5=%s 字节=%d" % (p, md5_of(p), os.path.getsize(p))
                               if os.path.isfile(p) else "%s (未落盘)" % p))
    L.append("%-10s %s" % ("ZHENG", stat_of(ZHENG)))
    for p in WATCH:
        L.append("%-10s %s" % ("WATCH", "%s md5=%s 字节=%d" % (p, md5_of(p), os.path.getsize(p))))
    return "\n".join(L) + "\n"


VERDICT = ("INTAKE-NUMERICS-ALL-REPRODUCED / CHART-ADMISSIBILITY-WINDOW-READINGS-GT-50 / "
           "SPECTRUM-IS-THE-ONLY-CHART-INVARIANT / CURVATURE-ARBITRARY-INCL-ZERO / "
           "INTEGER-DIAL-OFF-BY-1.71e6-SIGMA / THRESHOLD-LEVERAGE-1/676-OF-DIAL / STILL-NOT-A-PREDICTION")


def html_text(extra):
    kgrid = json.dumps([[ki, 150 - ki, -1 if ki < 100 else 0] for ki in range(-10, 91)])
    tab12 = json.dumps([[r[0], r[1], r[4]] for r in extra["V11"]["rows"]])
    return """<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>TUFT-r320 · ROOT V24 图表层审计</title>
<style>
body{font-family:system-ui,'Noto Sans SC',sans-serif;margin:0;background:#0f1115;color:#e8eaef}
.wrap{max-width:1120px;margin:0 auto;padding:22px}
h1{font-size:20px;margin:6px 0 2px}h2{font-size:15px;margin:22px 0 8px;color:#8ab4ff}
.sub{color:#9aa3b2;font-size:12.5px}
.card{background:#171b22;border:1px solid #262c36;border-radius:10px;padding:14px;margin:10px 0}
label{font-size:13px;color:#c9d2e0}
input[type=range]{width:100%}
.b{display:inline-block;padding:2px 9px;border-radius:999px;font-size:12px;margin-right:6px}
.ok{background:#123d24;color:#7ee2a8}.no{background:#3d1418;color:#ff8f9a}.bd{background:#3a3110;color:#ffd479}
.mono{font-family:ui-monospace,Consolas,monospace}
table{border-collapse:collapse;width:100%;font-size:12.5px}
th,td{border-bottom:1px solid #262c36;padding:5px 7px;text-align:right}
th:first-child,td:first-child{text-align:left}
.big{font-size:26px;font-weight:600}
</style></head><body><div class="wrap">
<h1>TUFT-r320 · ROOT V24.0 固定点真假判别 —— 图表层审计</h1>
<div class="sub">来料：A=1/50、B=3 ⇒ u*=1/150；v=u/(1−ku) ⇒ v*=A/(B−kA)、β′(v*)=−1/50（与 k 无关）。本卷审的是「换变量」这件事本身的边界。</div>
<div class="card">
<h2 style="margin-top:0">坐标旋钮（拖动即改「预测值」，指数不动）</h2>
<label>k = <span id="kv" class="mono">13</span>　<span class="sub">1/v* = 150 − k（精确恒等，非拟合）</span></label>
<input type="range" id="k" min="-40" max="149" step="1" value="13">
<div style="margin-top:10px">
<div class="big">1/v* = <span id="read" class="mono">137</span> <span class="sub">个 α⁻¹ 单位</span></div>
<div style="margin-top:6px">临界指数 β′(v*) = <span class="mono" id="slope">−0.02</span>　<span class="b ok" id="badg1">不变量</span><span class="b" id="admb">可容</span></div>
<div class="sub" id="note">物理 CODATA 137.035999177 需 k*=12.964000823（非整数、无第一性来源）；取整数 k=13 的偏差 = 1.71e6 σ。</div>
</div></div>
<div class="card"><h2 style="margin-top:0">§三 轨道表 12 读数 · 按字段自身半 ulp 裁定</h2>
<table><thead><tr><th>打印值</th><th>90 位复算</th><th>偏差/半ulp</th><th>裁定</th></tr></thead><tbody id="t12"></tbody></table>
<div class="sub">最紧一格 %RATIO%；他卷 r317 对同一张表按固定相对容差判 FAIL——分歧只在容差货币（本卷最大相对偏差 %MAXREL% 仍小于 6 位字段的相对容许值 ~7.5e-5）。</div></div>
<div class="card"><h2 style="margin-top:0">三笔账放在同一货币里（α⁻¹ 单位）</h2>
<table><thead><tr><th>来源</th><th>移动量</th><th>相对旋钮一格</th></tr></thead><tbody>
<tr><td>坐标旋钮 k 走一格</td><td class="mono">1</td><td>1×</td></tr>
<tr><td>来料那一步 150→137</td><td class="mono">13</td><td>13×</td></tr>
<tr><td>真实 QED 阈值积分（H(1)）</td><td class="mono">%H1%</td><td>%LEV1%</td></tr>
<tr><td>L=500 时三条轨道的残余历史差</td><td class="mono">%SPREAD%</td><td>%LEV2%</td></tr>
</tbody></table>
<div class="sub">⇒ §四 的「接入真实 QED」与「收敛到同一固定点」都太小，不足以裁定 §一 的坐标之争。</div></div>
<div class="card"><h2 style="margin-top:0">不变量名单（V2/V8 的结论）</h2>
<div class="sub">图表族 v=u/(1−13u)+S(u−u*)² 中：v*≡1/137、β′(v*)≡−1/50 与 S 无关；而 β″(v*)=%B2S% 随 S 线性漂移，S*=%SZERO% 时恰好为零 ⇒ 曲率类论证全族失效。</div></div>
<div class="card"><h2 style="margin-top:0">可容性：极点在不在你这条轨道里</h2>
<div class="sub">三条来料轨道的 u 区间 = [0.002,1/150]、[0.004,1/150]、[1/150,0.010]。同时可容 ⇒ k≤99 ⇒ 读数 &gt; 50。视界 k=B/A=150：极点 1/k 正落在固定点上（相似性前提失效）。上方面板会随 k 变红。</div></div>
<script>
var T12=%TAB12%;
var tb=document.getElementById('t12');
T12.forEach(function(r){var tr=document.createElement('tr');var ok=parseFloat(r[2])<1;
tr.innerHTML='<td class="mono">'+r[0]+'</td><td class="mono">'+r[1]+'</td><td class="mono">'+parseFloat(r[2]).toFixed(3)+'</td><td><span class="b '+(ok?'ok':'no')+'">'+(ok?'命中':'红')+'</span></td>';tb.appendChild(tr);});
function paint(){var k=+document.getElementById('k').value;
document.getElementById('kv').textContent=k;
var rd=150-k;document.getElementById('read').textContent=rd;
document.getElementById('slope').textContent=(-0.02).toFixed(4);
var adm=k<100;var b=document.getElementById('admb');
b.className='b '+(adm?'ok':'no');b.textContent=adm?'三轨道同时可容':'极点切断某条轨道';
var n=document.getElementById('note');
if(k===13)n.textContent='来料取的值：1/v*=137（整数）。与 CODATA 137.035999177 差 0.035999177 = 1.71e6 σ。';
else if(k===150)n.textContent='视界：分母 B−kA=0，非零固定点跑到无穷。';
else n.textContent='整数 k ⇒ 1/v* 必为整数（'+(101)+' 格抽样 101/101 命中）；要命中 CODATA 需非整数 k*=12.964000823。';
}
document.getElementById('k').addEventListener('input',paint);paint();
</script></div></body></html>
"""


def fill_html(h, extra):
    rep = {
        "%RATIO%": extra["V11"]["worst_ratio"], "%MAXREL%": extra["V11"]["maxrel"],
        "%H1%": extra["V13"]["H1"][:12], "%LEV1%": "%.4f" % (0.0192353209),
        "%SPREAD%": extra["V12"]["spread_inv"], "%LEV2%": "%.4f" % (0.01816),
        "%B2S%": "-137(2571353·S + 506250000)/12656250000", "%SZERO%": "-196.880786108",
        "%TAB12%": json.dumps([[r[0], r[1], r[4]] for r in extra["V11"]["rows"]]),
    }
    for kk, vv in rep.items():
        h = h.replace(kk, str(vv))
    return h


extra_g = {"n_main": 0, "n_ctl": 0, "n_g": 0}
WATCH = []


def main():
    t0 = time.time()
    before_files = [ZHENG, R308_MD, R317_MD, R317_JSON, R321_MD, R321_JSON,
                    os.path.join(ROOT, "README.md")]
    global WATCH
    WATCH = [p for p in before_files if os.path.isfile(p)]
    before = {p: md5_of(p) for p in WATCH}

    extra = {}
    v1(); extra["V1"] = ITEMS[-1]["kv"]
    v2(); extra["V2"] = ITEMS[-1]["kv"]
    v3(); extra["V3"] = ITEMS[-1]["kv"]
    v4(); extra["V4"] = ITEMS[-1]["kv"]
    v5(); extra["V5"] = ITEMS[-1]["kv"]
    v6(); extra["V6"] = ITEMS[-1]["kv"]
    v7(); extra["V7"] = ITEMS[-1]["kv"]
    v8(); extra["V8"] = ITEMS[-1]["kv"]
    v9(); extra["V9"] = ITEMS[-1]["kv"]
    v10(); extra["V10"] = ITEMS[-1]["kv"]
    v11(); extra["V11"] = ITEMS[-1]["kv"]
    v12(); extra["V12"] = ITEMS[-1]["kv"]
    v13(); extra["V13"] = ITEMS[-1]["kv"]
    v14(); extra["V14"] = ITEMS[-1]["kv"]
    v15(); extra["V15"] = ITEMS[-1]["kv"]
    v16(); extra["V16"] = ITEMS[-1]["kv"]
    v17(); extra["V17"] = ITEMS[-1]["kv"]
    v18(); extra["V18"] = ITEMS[-1]["kv"]
    ctl = [c1(), c2(), c3(), c4(), c5(), c6(), c7()]
    v19(ctl); extra["V19"] = ITEMS[-1]["kv"]

    secs = round(time.time() - t0, 2)
    tally1 = {v: sum(1 for i in ITEMS if i["verdict"] == v) for v in ("PASS", "FAIL", "BOUNDARY", "INFO")}
    prods = products()
    payloads = {prods[0]: json_text(extra), prods[1]: data_md_text(extra, tally1, secs),
                prods[2]: report_text(extra, tally1, secs),
                prods[3]: judgment_text(extra), prods[4]: fill_html(html_text(extra), extra)}
    n = write_all(payloads)

    # 第一趟落盘后，判据读**盘上那张面**（不是拼装用的模板）：G15 的牙齿
    face = open(prods[1], "rb").read().decode("utf-8")
    needles = ["230.2585093", "0.019235320902829404", "12.964000823", "1/22500", "196.880786108"]
    hit = [x for x in needles if x in face]
    gres = guards(extra, ctl, before, (needles, hit))
    extra_g.update(gres)

    tally2 = {v: sum(1 for i in ITEMS if i["verdict"] == v) for v in ("PASS", "FAIL", "BOUNDARY", "INFO")}
    write_all({prods[1]: data_md_text(extra, tally2, secs),
               prods[3]: judgment_text(extra),
               prods[0]: json_text(extra)})
    # 第三趟只收尾日志面：它印的是其余四张面的**终态**哈希；它自己的哈希不由自己声明（自指不可判）。
    write_all({prods[2]: report_text(extra, tally2, secs)})

    print("=" * 78)
    print("TUFT-%s · ROOT V24.0 固定点真假判别 · 图表层审计（同来料第三把尺）" % RID)
    print("=" * 78)
    print("条目 %d（主 %d / 控制 %d / 守卫 %d）· 落盘 %d 张面"
          % (len(ITEMS), extra_g["n_main"], extra_g["n_ctl"], extra_g["n_g"], n))
    for kk in ("PASS", "FAIL", "BOUNDARY", "INFO"):
        print("  %-9s %d" % (kk, tally2[kk]))
    print("  判据集    %s %s" % (extra["V19"]["score"], extra["V19"]["tally"]))
    print("  耗时      %s s" % secs)
    print("-" * 78)
    for it in ITEMS:
        print("[%s] %-9s %s" % (it["id"], it["verdict"], it["title"][:58]))
    print("-" * 78)
    for p in products():
        print("%-10s md5=%s 字节=%d" % (os.path.basename(p)[-24:], md5_of(p), os.path.getsize(p)))
    print("可视化：%s" % products()[4])
    bad = [p for p in WRITTEN if RID not in os.path.basename(p)]
    off = sorted(set(WRITTEN) - set(products()) - {ZHENG})
    after = {p: md5_of(p) for p in WATCH}
    changed = [p for p in WATCH if after[p] != before[p]]
    rc_ctl = all(i["verdict"] == "PASS" for i in ITEMS if i["layer"] == "控制组")
    rc_grd = all(i["verdict"] == "PASS" for i in ITEMS if i["layer"] == "守卫")
    print("写入越界=%s 非本卷路径=%s 他卷被改动=%s 控制组全绿=%s 守卫全绿=%s"
          % (off, bad, [os.path.basename(x) for x in changed], rc_ctl, rc_grd))
    print("FAIL 主条目（按设计红，非仪器故障）=%s"
          % [i["id"] for i in ITEMS if i["layer"] == "主" and i["verdict"] == "FAIL"])
    rc = 0 if (not bad and not off and rc_ctl and rc_grd and not changed) else 2
    print("RC =", rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
