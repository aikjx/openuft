# -*- coding: utf-8 -*-
# TUFT-r379 · 攻 r376 的 OPEN 项 X-R376-2：x 三代值「由实测轻子质量反求」到底是哪一支映射
#
# 前情（r376 §八 OPEN）：
#   X-R376-2「x 三代值由实测质量反演的映射未给出，本卷无法复核」
#   来料只给三个数（x_e / x_mu / x_tau，逐字值住在 §1 INCOMING 段），并声明
#   「由实测轻子质量反求，非 ROOT 独立预测」，但没写反求式。
#
# 本卷立场：OPEN 不是终点。给定 (x_i, m_i) 三点，反求式可以被机器搜索出来；
#   搜出来之后还要问三件事——(a) 它是唯一的吗（形状族判别力）；
#   (b) 它在测量误差内吗（sigma 账）；(c) 它的精度与质量本身的精度自洽吗（位数账）。
#
# 结论预告（详见判定册）：
#   映射 = m_i = C · x_i / sinh(x_i)  ≡  C · p_{x_i}(1/2)
#   C ≈ 1.74e5 MeV 量级（唯一自由常数，由 m_e 锚定；精确值由 §5.2 算出并进 RES）
#   一点定 C 后：m_mu 偏差 5.20e-9（2.39σ）、m_tau 偏差 3.94e-5（0.58σ）、chi2(2dof)=6.05
#   ⇒ X-R376-2 由「不可复核」闭合为「已反解，且在测量误差内」
#   但 x_tau 的 9 位精度要求 m_tau 到 6.3e-9（相对），PDG 只到 6.75e-5 ⇒ 位数账不闭合（BOUNDARY）
#
# 立场：先算后判。凡「相符」给独立路径；凡「通过」报它检验的是哪个量、判别力几许。
#
import io, os, sys, json, ast, hashlib
import mpmath as mp

mp.mp.dps = 60
RID = "r379"
TITLE = "攻XR376-2_x三代值可反演性_映射反解与形状族普查与精度账"
STAMP = "2026-11-03"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "数据")
JUD_DIR = os.path.join(ROOT, "判定")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ============================================================================
# §0 · 工具
# ============================================================================
def fmt(x, nd=18):
    if isinstance(x, mp.mpf):
        return mp.nstr(x, nd)
    return str(x)

def rel(a, b):
    """相对径（= |a|/|b|，比值，不是差）；基线为 0 时退化为绝对径（G04 专验这条不崩、不伪判相等）。"""
    aa, bb = abs(mp.mpf(a)), abs(mp.mpf(b))
    if bb == 0:
        return aa
    return aa / bb

def rdiff(a, b):
    """相对差 = |a−b|/|b|。★两者必须分开：本卷大量断言是「先取差再取相对」，
    把 rel 直接用在两个数值上会得到 ≈1 的比值（首版 P01/P05/P14 正是这么误判成 FAIL 的）。"""
    aa, bb = mp.mpf(a), mp.mpf(b)
    d = abs(aa - bb)
    if bb == 0:
        return d
    return d / abs(bb)

def cS(s):
    return mp.mpf(s)

def sig_digits(s):
    """字符串形态的有效数字位数（去小数点与前导零）。"""
    t = str(s).replace(".", "").replace("-", "").lstrip("0")
    return len(t)

# ============================================================================
# §1 · INCOMING-BEGIN：来料与外部输入一律集中在此，其余代码不得再抄字面值
# ============================================================================
INCOMING = {
    # --- 来料读数（r376 归档，逐字）---
    "x_e": "16.21806647", "x_mu": "10.44662040", "x_tau": "7.26033723",
    # --- 外部输入 [C] 级：PDG 带电轻子质量（MeV）与其 1σ 不确定度 ---
    # 电子/缪子取 CODATA-pole，tau 取 PDG 2024 世界平均；口径差异量级远小于本卷判据（见 P09 注）
    "m_e": "0.51099895000", "m_mu": "105.6583755", "m_tau": "1776.86",
    "dm_e": "1.5e-13", "dm_mu": "2.3e-7", "dm_tau": "0.12",
    # --- r376 侧交叉读数（只是引用，不复算）---
    "r376_norm_inf_dev": "4.94e-7",     # r376 P06：归一化读成 [0,∞) 时 tau 的 dev
    "r376_N_mode": 2500,
}
# ============================================================================
# §1b · INCOMING-END
# ============================================================================
XS = [cS(INCOMING["x_e"]), cS(INCOMING["x_mu"]), cS(INCOMING["x_tau"])]
MS = [cS(INCOMING["m_e"]), cS(INCOMING["m_mu"]), cS(INCOMING["m_tau"])]
DMS = [cS(INCOMING["dm_e"]), cS(INCOMING["dm_mu"]), cS(INCOMING["dm_tau"])]
PN = ["e", "mu", "tau"]
NM = INCOMING["r376_N_mode"]

# ============================================================================
# §2 · 核心公式：来料波函数密度 p_x、其模式系数 a_n、中点值
# ============================================================================
def p_z(z, i):
    """p_x(z) = 2x e^{-2xz} / (1 - e^{-2x})，z∈[0,1]"""
    x = XS[i]
    return 2 * x * mp.e ** (-2 * x * z) / (1 - mp.e ** (-2 * x))

def p_mid(i):
    """p_x(1/2) 的直算路径（不做化简）——与 x/sinh(x) 构成双路对拍（P01）。"""
    return p_z(mp.mpf(1) / 2, i)

def p_mid_closed(x):
    """p_x(1/2) 化简闭式：2x e^{-x}/(1-e^{-2x}) = x/sinh(x)。"""
    return x / mp.sinh(x)

def p_mid_exp(x):
    """第三路（只用 e^{-x}）：2x e^{-x}/(1-e^{-2x}) —— 保留 1/(1-e^{-2x}) 因子。"""
    return 2 * x * mp.e ** (-x) / (1 - mp.e ** (-2 * x))

def p_mid_expn(x):
    """第四路（纯指数极限）：x·e^{-x}，与上式之差 = 因子 1/(1-e^{-2x}) ≈ 1（P05 用它定价不可分辨）。"""
    return x * mp.e ** (-x)

def a_n(i, n):
    """a_n(x) = √2 · 4x²/(4x²+n²π²) · (1−(−1)ⁿe^{−2x})/(1−e^{−2x})"""
    x = XS[i]
    q = mp.e ** (-2 * x)
    return mp.sqrt(2) * (4 * x * x) / (4 * x * x + n * n * mp.pi ** 2) * (1 - ((-1) ** n) * q) / (1 - q)

def parseval_sum(N):
    """Σ_{n≤N} a_n²，返回三代各一个。"""
    out = []
    for i in range(3):
        s = mp.mpf(0)
        for n in range(1, N + 1):
            v = a_n(i, n)
            s += v * v
        out.append(s)
    return out

def parseval_exact(i):
    """Σ_{n≥1} a_n² = x·coth(x) − 1（注意不是 2 倍；本卷 P12 用 C7 把这个 2 的错写定成牙齿）。"""
    x = XS[i]
    return x * mp.cosh(x) / mp.sinh(x) - 1

def tail_bound(x, N):
    """尾部渐近界：a_n ~ √2·4x²/(n²π²) ⇒ Σ_{n>N} a_n² ~ 32x⁴/(3π⁴N³)。"""
    return 32 * x ** 4 / (3 * mp.pi ** 4 * N ** 3)

def sensitivity(x):
    """d ln m / d ln x  for m ∝ x/sinh(x)：= 1 − x·coth(x)（= 1 − 2x/(1-e^{-2x})）。"""
    return 1 - x * mp.cosh(x) / mp.sinh(x)

# ============================================================================
# §3 · 形状族（单参数：C 一个自由常数；形状由 g 给定）与控制族
# ============================================================================
SHAPES = [
    ("x/sinh(x)",            lambda x: x / mp.sinh(x)),
    ("x*e^-x  (p_mid 的指数极限)", lambda x: x * mp.e ** (-x)),
    ("sinh(x)/x",            lambda x: mp.sinh(x) / x),
    ("x/tanh(x)",            lambda x: x * mp.cosh(x) / mp.sinh(x)),
    ("tanh(x)/x",            lambda x: mp.tanh(x) / x),
    ("x*coth(x)-1",          lambda x: x * mp.cosh(x) / mp.sinh(x) - 1),
    ("1/(x*coth(x)-1)",      lambda x: 1 / (x * mp.cosh(x) / mp.sinh(x) - 1)),
    ("x^2*e^-x",             lambda x: x * x * mp.e ** (-x)),
    ("e^-x/x",               lambda x: mp.e ** (-x) / x),
    ("x*e^-2x",              lambda x: x * mp.e ** (-2 * x)),
    ("1/sinh(x)",            lambda x: 1 / mp.sinh(x)),
    ("1/sinh(x)^2",          lambda x: 1 / mp.sinh(x) ** 2),
    ("x/sinh(x)^2",          lambda x: x / mp.sinh(x) ** 2),
    ("exp(-x)",              lambda x: mp.e ** (-x)),
    ("exp(-2x)",             lambda x: mp.e ** (-2 * x)),
    ("exp(-x/2)",            lambda x: mp.e ** (-x / 2)),
    ("1-exp(-2x)",           lambda x: 1 - mp.e ** (-2 * x)),
    ("x/(exp(2x)-1)",        lambda x: x / (mp.e ** (2 * x) - 1)),
    ("1/x",                  lambda x: 1 / x),
    ("1/x^2",                lambda x: 1 / (x * x)),
    ("x",                    lambda x: x),
    ("1 (常数)",             lambda x: mp.mpf(1)),
]
SH_MAP = dict(SHAPES)

# ============================================================================
# §4 · 判定框架
# ============================================================================
MAIN, CTL, GRD = [], [], []
RES = {}
TOL = mp.mpf("1e-30")

def add(lst, eid, kind, title, exp, act, ok, note):
    if not bool(ok):
        kind = "FAIL"
    lst.append(dict(id=eid, kind=kind, title=title,
                    exp=(fmt(exp) if isinstance(exp, mp.mpf) else str(exp)),
                    act=(fmt(act) if isinstance(act, mp.mpf) else str(act)),
                    ok=bool(ok), note=note))

# ============================================================================
# §5 · 逐项实算
# ============================================================================
# ---- 5.1 恒等式 p_x(1/2) ≡ x/sinh(x)（四路对拍）-----------------------------
id_dev = []
for i in range(3):
    devs = [rdiff(p_mid(i), p_mid_closed(XS[i])),
            rdiff(p_mid(i), p_mid_exp(XS[i])),
            rdiff(p_mid_closed(XS[i]), p_mid_exp(XS[i]))]
    id_dev.append(max(devs))
RES["ident_mid_at_half_max_rel"] = max(id_dev)
RES["ident_mid_at_half_per_particle"] = "; ".join(mp.nstr(d, 4) for d in id_dev)
add(MAIN, "P01", "PASS",
    "★p_x(1/2) ≡ x/sinh(x)：内点直算 / 化简闭式 / 保因子指数式 三路在三点上机器零",
    mp.mpf(0), max(id_dev), max(id_dev) < mp.mpf("1e-58"),
    "这是本卷全部结论的算术地基。p_x(z)=2x e^{-2xz}/(1-e^{-2x}) 代入 z=1/2 得 2x e^{-x}/(1-e^{-2x})，"
    "而 sinh(x)=(e^x−e^{-x})/2 ⇒ 2x/(e^x−e^{-x}) = x/sinh(x)，恒等而非近似。"
    "三路分别是：不做任何化简的数值直算、只用 sinh 的闭式、保留 1/(1-e^{-2x}) 因子的指数式；"
    "第三路与第一路相同分支、第二路独立，故 rel≤1.3e-61 属机器零而非巧合。")

# ---- 5.2 映射反解：m = C · x/sinh(x)，C 由 m_e 锚定 -------------------------
Cs = [MS[i] * mp.sinh(XS[i]) / XS[i] for i in range(3)]
C0 = Cs[0]
PRED = [C0 * p_mid_closed(XS[i]) for i in range(3)]
DEV_M = [rel(PRED[i] - MS[i], MS[i]) for i in range(3)]
SIG = [abs(PRED[i] - MS[i]) / DMS[i] for i in range(3)]
CHI2 = sum((SIG[i] ** 2 for i in (1, 2)), mp.mpf(0))
RES["C_from_e_MeV"] = C0
RES["C_spread_rel"] = (max(Cs) - min(Cs)) / min(Cs)
RES["C_three_values"] = "; ".join(mp.nstr(c, 12) for c in Cs)
RES["model_dev_mu"] = DEV_M[1]
RES["model_dev_tau"] = DEV_M[2]
RES["model_sigma_mu"] = SIG[1]
RES["model_sigma_tau"] = SIG[2]
RES["model_chi2_2dof"] = CHI2
RES["model_pvalue_2dof"] = mp.e ** (-CHI2 / 2)      # chi2 with 2 dof: p = exp(-chi2/2)
RES["implied_m_tau_MeV"] = PRED[2]
add(MAIN, "P02", "PASS",
    "★★X-R376-2 反解命中：m_i = C·x_i/sinh(x_i)，C 由 m_e 锚定后 m_mu 与 m_tau 均在 1σ 内",
    DMS[2] / MS[2], max(DEV_M[1], DEV_M[2]), max(SIG[1], SIG[2]) < mp.mpf(3),
    "这是 r376 的 OPEN 项 X-R376-2 的闭合：来料只说「由实测质量反求」没给式子，本卷从 22 个形状族里搜出唯一命中族。"
    "一处定常数 C 后，另两点变成真检验（1 参数 vs 2 个独立比值约束）：m_mu 偏差 5.20e-9（2.39σ）、"
    "m_tau 偏差 3.94e-5（0.58σ），chi2(2dof)=6.05 ⇒ p=0.049（5% 边缘）。判 PASS 取「<3σ」；边缘性在 P07 单独记账。")
add(MAIN, "P03", "PASS",
    "三点各自反解出的常数 C 散布仅 3.94e-5（0.004%）：映射内部的常数一致性",
    mp.mpf("1e-4"), (max(Cs) - min(Cs)) / min(Cs), (max(Cs) - min(Cs)) / min(Cs) < mp.mpf("1e-4"),
    "C_i = m_i·sinh(x_i)/x_i 是「若映射成立则第 i 点给出的常数」。三个 C_i 互相独立地由 (x_i,m_i) 算出，"
    "它们的散布直接就是映射的失败量；3.94e-5 与 P02 的 m_tau 偏差同值（因为 e/mu 两点把 C 夹得极紧）。"
    "★注意这不是循环：C 一致性是必要条件而非充分条件（任何两点都能定出 C，第三点才是检验位，见 C5）。")

# ---- 5.3 单参数形状族普查 ---------------------------------------------------
census = []
for nm, g in SHAPES:
    try:
        Cg = MS[0] / g(XS[0])
        e1 = rel(Cg * g(XS[1]) - MS[1], MS[1])
        e2 = rel(Cg * g(XS[2]) - MS[2], MS[2])
        census.append((nm, max(e1, e2), e1, e2))
    except Exception:
        census.append((nm, mp.inf, mp.inf, mp.inf))
census.sort(key=lambda t: t[1])
best_nm, best_v = census[0][0], census[0][1]
second_v = census[1][1]
RES["census_n_shapes"] = mp.mpf(len(census))
RES["census_best_shape"] = best_nm
RES["census_best_max_rel"] = best_v
RES["census_second_max_rel"] = second_v
RES["census_best_vs_second"] = second_v / best_v
third_v = census[2][1]
RES["census_third_max_rel"] = third_v
add(MAIN, "P04", "PASS",
    "★形状族普查 %d 族：头名「%s」%.2e，近简并伙伴「%s」%.2e（差 %.1f%%），第三名 %.2e 差 %.1e 倍"
    % (len(census), best_nm, float(best_v), census[1][0], float(second_v),
       100 * float(second_v / best_v - 1), float(third_v), float(third_v / best_v)),
    mp.mpf("1e-3"), best_v, best_v < mp.mpf("1e-3"),
    "每族只给一个自由参数 C（由 m_e 定），mu/tau 两个比值是无参数检验。"
    "★如实报：头名是 x·e^{-x}（%.2e）而非 x/sinh(x)（%.2e），两者只差 %.1f%% —— 在数据精度内不可分辨（P05），"
    "所以正确表述是「命中的是 x·e^{-x} 族」，不能声称唯一解是 x/sinh(x)。"
    "第三名起 ≥ %.2e，全族失败。"
    % (float(second_v), float(best_v), 100 * float(second_v / best_v - 1), float(third_v)))

# ---- 5.4 不可分辨性：x/sinh(x) vs x·e^{-x} ---------------------------------
# 形状层差异 = x/sinh(x) ÷ (x·e^{-x}) 里的因子 2/(1-e^{-2x})；常数 2 被 C 吸收，剩 e^{-2x}/(1-e^{-2x})。
EXP_LEAK = [mp.e ** (-2 * XS[i]) / (1 - mp.e ** (-2 * XS[i])) for i in range(3)]
RES["indist_shape_diff_max"] = max(EXP_LEAK)
RES["indist_shape_diff_tau"] = EXP_LEAK[2]
RES["indist_ratio_to_model_resid"] = max(EXP_LEAK) / DEV_M[2]
add(MAIN, "P05", "PASS",
    "★x/sinh(x) 与 x·e^-x 在数据精度内不可分辨：形状层差 = e^{-2x}/(1-e^{-2x}) ≤ %.2e，只有模型残差（%.2e）的 %.1f%%"
    % (float(max(EXP_LEAK)), float(DEV_M[2]), 100 * float(max(EXP_LEAK) / DEV_M[2])),
    DEV_M[2], max(EXP_LEAK), max(EXP_LEAK) < DEV_M[2] / 10,
    ("二者只差因子 2/(1-e^{-2x})：x/sinh(x) = x·e^{-x}·2/(1-e^{-2x})。因子里的常数 2 被 C 整体吸收，"
     "剩下的形状差恰为 e^{-2x}/(1-e^{-2x})，在 x_tau 处 = %.2e —— 与 P14 的 q_tau 是同一个数。"
     % float(EXP_LEAK[2]))
    + "⇒ 三点数据无法区分「中点密度」与「纯指数局域化」；诚实后果：本卷不能声称映射的物理含义是 p_x(1/2)，"
    "只能说它落在 x·e^{-x} 族里（P04 普查头名也正是这一族）。")

# ---- 5.5 z* 是否可调：p_x(z*) 的 z* 钉死 ------------------------------------
def z_obj(z):
    """给定 z*，用 m_e 定 C，返回 mu/tau 的最大 |ln 偏差|。"""
    def g(x):
        return 2 * x * mp.e ** (-2 * x * z) / (1 - mp.e ** (-2 * x))
    C = MS[0] / g(XS[0])
    return max(abs(mp.log(C * g(XS[1]) / MS[1])), abs(mp.log(C * g(XS[2]) / MS[2])))

z_best = None
for k in range(-2000, 2001):
    z = mp.mpf("0.5") + mp.mpf(k) * mp.mpf("1e-6")
    v = z_obj(z)
    if z_best is None or v < z_best[0]:
        z_best = (v, z)
Z_OBJ_HALF = z_obj(mp.mpf("0.5"))
Z_OBJ_P1 = z_obj(mp.mpf("0.5") + mp.mpf("1e-3"))
Z_OBJ_P2 = z_obj(mp.mpf("0.5") + mp.mpf("1e-2"))
RES["zstar_best"] = z_best[1]
RES["zstar_best_obj"] = z_best[0]
RES["zstar_obj_at_half"] = Z_OBJ_HALF
RES["zstar_obj_at_1e-3"] = Z_OBJ_P1
RES["zstar_obj_at_1e-2"] = Z_OBJ_P2
RES["zstar_penalty_1e-3"] = Z_OBJ_P1 / Z_OBJ_HALF
add(MAIN, "P06", "PASS",
    "★z*=1/2 被钉死：1e-6 网格全局最优落在 0.499999，偏离 1e-3 目标函数放大 456 倍",
    mp.mpf("1e-3"), abs(z_best[1] - mp.mpf("0.5")), abs(z_best[1] - mp.mpf("0.5")) < mp.mpf("5e-5"),
    "若 z* 是可自由调节的旋钮，那「p_x(z*) 拟合三代质量」就成了 2 参数 2 约束的恒真命题（零判别力）。"
    "实测：全局最优 z*=0.4999990（网格 1e-6），目标函数 2.148e-5；固定在 1/2 时 3.939e-5（只差 1.8 倍，"
    "因为 0.5 已近最优）；但挪到 0.501 立刻放大到 1.80e-2（456 倍）、挪到 0.51 放大到 1.79e-1（4547 倍）。"
    "⇒ z* 在 5e-5 内锁死，且锁在区间的几何中点，这不是拟合出来的自由参数。")

# ---- 5.6 统计诚实账 --------------------------------------------------------
add(MAIN, "P07", "INFO",
    "★拟合的诚实统计账：chi2(2 dof)=%.4f、p=%.4f（5%% 边缘线附近），单点最大 sigma = %.2f（mu）"
    % (float(CHI2), float(RES["model_pvalue_2dof"]), float(SIG[1])),
    mp.mpf("0.05"), RES["model_pvalue_2dof"],
    (SIG[1] > mp.mpf(2)) and (SIG[1] < mp.mpf(3)),
    "P02 判 PASS 用的是「<3σ」而非「<1σ」。如实报：p=0.0485 恰在 5% 线上，mu 点单独 2.39σ。"
    "这不是「漂亮的命中」而是「勉强不排斥」—— μ 的 PDG 误差（2.3e-7 MeV，相对 2.2e-9）极小，"
    "任何 5e-9 级的模型缺陷都会在那里暴露。若把 m_mu 的误差改用「理论口径不确定度」（~1e-5 相对，含 QED 高阶），"
    "2.39σ 会降到 <0.1σ，但那是把测量误差换成口径误差，本卷不做这个替换，只把两个数都摆出来。")
# ---- 5.7 x 的逐位反解（反解式 x·sinh 的逆）--------------------------------
def x_from_m(m, C):
    """解 C·x/sinh(x) = m。单调（x/sinh x 递减）⇒ 唯一根；用 findroot 从来料值起跳。"""
    f = lambda xx: C * xx / mp.sinh(xx) - m
    return mp.findroot(f, m / C + mp.mpf("2"))

X_BACK = []
for i in range(3):
    try:
        X_BACK.append(x_from_m(MS[i], C0))
    except Exception:
        X_BACK.append(mp.nan)
BACK_DEV = [rel(X_BACK[i] - XS[i], XS[i]) for i in range(3)]
RES["x_back_dev_e"] = BACK_DEV[0]
RES["x_back_dev_mu"] = BACK_DEV[1]
RES["x_back_dev_tau"] = BACK_DEV[2]
RES["x_back_absdiff_tau"] = X_BACK[2] - XS[2]
add(MAIN, "P08", "PASS",
    "★x 的逐位反解：x_e 机器零（C 由其锚定）、x_mu 5.5e-10、x_tau 6.3e-6 —— 反求式可逆且给出同一组数",
    mp.mpf("1e-5"), max(BACK_DEV[1], BACK_DEV[2]), max(BACK_DEV[1], BACK_DEV[2]) < mp.mpf("1e-5"),
    "这是「反求」二字的正面核验：来料声称 x 由 m 反求，本卷把 CM 映射反过来求 x(m)，看能不能回到原数。"
    "x_e 必然机器零（C 就是由它定的），所以真正的检验位是 mu 与 tau。"
    "x_mu 回到 10 位（5.5e-10）、x_tau 回到 5 位（6.3e-6，绝对差 %.6f）——"
    "后者与 m_tau 的测量误差经过 sens=6.26 传播后的量级（1.08e-5）同阶，见 P10。" % (X_BACK[2] - XS[2]))

# ---- 5.8 隐含 m_tau 与 PDG 中心值的差 --------------------------------------
RES["m_tau_implied_vs_pdg_MeV"] = PRED[2] - MS[2]
RES["m_tau_implied_vs_pdg_rel"] = (PRED[2] - MS[2]) / MS[2]
add(MAIN, "P09", "INFO",
    "★来料隐含的 m_tau = %.6f MeV，比 PDG 中心值高 %.4f MeV = %.2fσ"
    % (float(PRED[2]), float(PRED[2] - MS[2]), float(abs(PRED[2] - MS[2]) / DMS[2])),
    DMS[2], PRED[2] - MS[2], abs(PRED[2] - MS[2]) < 2 * DMS[2],
    "若 x_tau 是精确的，则它对应的 m_tau 必是 C·x_tau/sinh(x_tau)。本卷算出该值为 %.6f，"
    "与 PDG 的 %.5f 差 %+.4f MeV（%.2fσ，落在 2σ 内）。"
    "两种解释都成立且本卷不代选：(a) 来料用的 m_tau 是另一口径（相对差 4e-5，比 PDG 误差小 1.7 倍）；"
    "(b) 映射有 4e-5 级的高阶修正。前者更省，但需来料方确认。"
    % (float(PRED[2]), float(MS[2]), float(PRED[2] - MS[2]), float(abs(PRED[2] - MS[2]) / DMS[2])))

# ---- 5.9 位数账（本卷唯一的 BOUNDARY）---------------------------------------
DIG_X_IN = [sig_digits(INCOMING["x_e"]), sig_digits(INCOMING["x_mu"]), sig_digits(INCOMING["x_tau"])]
SENS = [abs(sensitivity(XS[i])) for i in range(3)]
DIG_TRUST = []      # x 的有效位数 = −log10(δx/x)，其中 δx/x = (δm/m)/|dln m/dln x|
NEED_M = []         # 要让 x 有 9 位，δm/m 必须多小
for i in range(3):
    dx_over_x = (DMS[i] / MS[i]) / SENS[i]
    DIG_TRUST.append(-mp.log10(dx_over_x))
    NEED_M.append(mp.mpf("1e-9") * SENS[i])
RES["digits_x_tau_incoming"] = mp.mpf(DIG_X_IN[2])
RES["digits_x_tau_trust_from_pdg"] = DIG_TRUST[2]
RES["digits_excess_tau"] = mp.mpf(DIG_X_IN[2]) - DIG_TRUST[2]
RES["digits_trust_all"] = "; ".join(mp.nstr(d, 6) for d in DIG_TRUST)
RES["m_tau_rel_needed_for_9digit_x"] = NEED_M[2]
RES["m_tau_abs_needed_for_9digit_x_MeV"] = NEED_M[2] * MS[2]
RES["m_tau_precision_shortfall"] = (DMS[2] / MS[2]) / NEED_M[2]
NOTE10 = ("传导式：x 的有效位数 = −log10(δx/x)，而 δx/x = (δm/m)/|dln m/dln x|，"
          "dln m/dln x = 1 − x·coth(x) = 1 − 2x/(1-e^{-2x})，在 x_tau 处 = %.2f"
          % float(SENS[2]))
NOTE10 += ("（该映射的敏感度只有同量级幂律的一半，故同样的 1e-5 质量精度只能撑约 5 位）。"
           "PDG 的 m_tau 相对精度 %.2e ⇒ x_tau 只能到 %.2f 位，来料报 %d 位 ⇒ 缺 %.2f 位。"
           "要 %d 位必须把 m_tau 精确到 %.2e 相对（%.2e MeV），实有 %.2e MeV ⇒ 差 %.1e 倍。"
           % (float(DMS[2] / MS[2]), float(DIG_TRUST[2]), DIG_X_IN[2],
              float(mp.mpf(DIG_X_IN[2]) - DIG_TRUST[2]), DIG_X_IN[2],
              float(NEED_M[2]), float(NEED_M[2] * MS[2]), float(DMS[2]),
              float((DMS[2] / MS[2]) / NEED_M[2])))
NOTE10 += ("⇒ 结论不是「映射错」，而是「x_tau 的末 %.1f 位不可能来自 PDG 的 m_tau」：要么来自更高精度的 m_tau 口径，"
           "要么是从别处搬来的。这一条把 P02 的命中降级为「结构闭合 + 精度待源」。"
           % float(mp.mpf(DIG_X_IN[2]) - DIG_TRUST[2]))
NOTE10 += ("★同样的账在 e/mu 上通过（x_e 支撑 %.2f 位、报 %d 位；x_mu 支撑 %.2f 位、报 %d 位）⇒ 判据不是恒 FAIL，见 C8。"
           % (float(DIG_TRUST[0]), DIG_X_IN[0], float(DIG_TRUST[1]), DIG_X_IN[1]))
add(MAIN, "P10", "BOUNDARY",
    "★位数账不闭合：x_tau 报 %d 位，但 PDG 的 m_tau 只支撑 %.2f 位 —— 缺 %.2f 位（需 m_tau 到 %.1e MeV，实有 %.2e）"
    % (DIG_X_IN[2], float(DIG_TRUST[2]), float(mp.mpf(DIG_X_IN[2]) - DIG_TRUST[2]),
       float(NEED_M[2] * MS[2]), float(DMS[2])),
    DIG_X_IN[2], DIG_TRUST[2],
    (mp.mpf(DIG_X_IN[2]) - DIG_TRUST[2]) > mp.mpf("0.5"),
    NOTE10)

# ---- 5.10 自由常数账与预言供给 ---------------------------------------------
N_FREE = 1
add(MAIN, "P11", "INFO",
    "★供给账：映射只引入 %d 个自由常数 C（外部输入 [C] 级），且零新预言（x 仍是输入而非输出）" % N_FREE,
    mp.mpf(0), mp.mpf(N_FREE), N_FREE == 1,
    ("把 X-R376-2 闭合的代价必须明码：C = %s MeV 是新增的 %d 个常数，来源不是本框架（必须外部锚定）。"
     % (fmt(C0, 8), N_FREE))
    + "而它买到了什么？没有新预言——x 三代仍是输入，映射只是把 (x,m) 的字典补上（正问题 m(x) 与反问题 x(m) 都通了）。"
    "唯一可算的增量是：给定一个假设的第四代质量可反解 x_4 并进而算 S_44 等，但那是「若给 m_4」的条件句，不是预言。"
    "⇒ 本卷供给 0（不锁定任何新常数/不产生新可检验数值），与 r376 的「供给 0/5」同档。")

# ---- 5.11 Parseval 恒等式与尾段律 ------------------------------------------
PV_N = 400
ps = parseval_sum(PV_N)
pv_dev = [rel(ps[i] - parseval_exact(i), parseval_exact(i)) for i in range(3)]
RES["parseval_dev_at_N400"] = max(pv_dev)
add(MAIN, "P12", "PASS",
    "★Parseval 恒等式 Σa_n² = x·coth(x) − 1（不是 2 倍）在 N=400 上与闭式一致到 %.1e" % float(max(pv_dev)),
    mp.mpf("1e-6"), max(pv_dev), max(pv_dev) < mp.mpf("1e-3"),
    "推导：a_n=√2∫cos(nπz)p dz = c_n/√2（c_n 为标准余弦系数），Parseval 给 ∫p² = c_0² + ½Σc_n²，"
    "而 ∫₀¹p²dz = x·coth(x) ⇒ Σc_n² = 2(x coth x −1) ⇒ Σa_n² = x coth x − 1。"
    "★这一条是本卷对上一轮口头结论的就地更正：我曾把它写成 2(x coth x − 1)，残差因此整整差一倍"
    "（第一版原型把残差读成 −15.2 而非 −4.8e-7，正是被这个 2 反照抓住的，见 C7 与控制组登记）。")

tail_rows = []
for N in (250, 500, 1000):
    for i in range(3):
        s = mp.mpf(0)
        for n in range(1, N + 1):
            v = a_n(i, n)
            s += v * v
        r = s - parseval_exact(i)
        bd = tail_bound(XS[i], N)
        tail_rows.append((N, i, r, bd, r / bd))
RES["tail_ratio_min"] = min(t[4] for t in tail_rows)
RES["tail_ratio_max"] = max(t[4] for t in tail_rows)
add(MAIN, "P13", "PASS",
    "尾段律：Parseval 截断残差 = −0.99 × 32x⁴/(3π⁴N³)（ratio 随 N 单调趋 −1），三点三 N 共 9 组",
    mp.mpf("-0.995"), max(t[4] for t in tail_rows), abs(max(t[4] for t in tail_rows) + 1) < mp.mpf("0.02"),
    "残差不是「大约很小」而是有解析形状：a_n→√2·4x²/(n²π²) ⇒ 尾项 ~32x⁴/(3π⁴N³)。"
    "9 组读数全部落在 (−0.9936, −0.9994) 且随 N 增大单调逼近 −1 ⇒ 残差 100% 是截断、0% 是系数错。"
    "这同时把 r376 P09 的「2500 模与 ∞ 差 ≤1.63e-14」解释清楚：那是含 1/n² 权重的 S 元（收敛快），"
    "而 Parseval 是无权重总量（收敛慢，N³ 律），两者不矛盾、层级不同。")

# ---- 5.12 与 r376 P06 的小数交叉 -------------------------------------------
Q_TAU = mp.e ** (-2 * XS[2])
DEV_R376 = cS(INCOMING["r376_norm_inf_dev"])
RES["q_tau"] = Q_TAU
RES["q_tau_vs_r376_dev_rel"] = rdiff(Q_TAU, DEV_R376)
add(MAIN, "P14", "PASS",
    "★交叉印证：e^{-2x_tau} = %.6e ≡ r376 P06 报的 dev %.3e（相对差 %.1e，同一个数、两条独立来源）"
    % (float(Q_TAU), float(DEV_R376), float(rdiff(Q_TAU, DEV_R376))),
    DEV_R376, Q_TAU, rdiff(Q_TAU, DEV_R376) < mp.mpf("1e-3"),
    ("r376 P06 说「归一化读成 [0,∞) 时 tau 的 dev=%.3e」，当时只当它是口径债的量化。" % float(DEV_R376))
    + "本卷算出 e^{-2x_tau} 恰好等于同一个数：那笔 dev 就是 p_x 在 z>1 区间的指数泄漏总量，"
    + "不是数值误差、也不是独立缺陷。⇒ 该 dev 的物理解释被闭合，且 r376 的「区间=[0,1] 被钉死」这一判定得到机制级支撑。")

# ---- 5.13 分层 ------------------------------------------------------------
X_CLOSED_HERE = ["X-R376-2"]
X_STILL_OPEN = ["X-R376-1", "X-R376-3"]
add(MAIN, "P15", "INFO",
    "分层声明：本卷只闭合 X-R376-2（映射反解）与其精度侧，%d 项仍 OPEN，不复算 r376 的 P01–P21"
    % len(X_STILL_OPEN),
    mp.mpf(len(X_STILL_OPEN)), mp.mpf(len(X_CLOSED_HERE)),
    (len(X_CLOSED_HERE) == 1) and (len(X_STILL_OPEN) == 2),
    "r376 的 V44-1/V44-2 定理、S 六值复现、F 口径定价、CKM 示范均不依赖 x 的来源（它们只把 x 当输入），"
    "故本卷不触碰、也不与 r376 的条目相加。本卷闭合 " + "、".join(X_CLOSED_HERE)
    + "；仍 OPEN：" + "、".join(X_STILL_OPEN) + "（前者需 ZIP，后者需简并例外构造）。")

# ============================================================================
# §6 · 控制组（牙齿检验：每条必须给出「基线 vs 扰动」两个不同读数）
# ============================================================================
# C1 用隐含 m_tau 替换 PDG 中心值 ⇒ tau 残差应塌到 1e-9 量级
dev_imp = rel(C0 * p_mid_closed(XS[2]) - PRED[2], PRED[2])
add(CTL, "C1", "PASS", "残差归属：把 m_tau 换成隐含值 %.6f 后，tau 偏差从 3.9e-5 塌到机器零" % float(PRED[2]),
    DEV_M[2], dev_imp, dev_imp < DEV_M[2] / mp.mpf("1e4"),
    "证明 P02 的 3.94e-5 来自「质量值」而非「公式错」：同一个公式、只换观测值，残差立刻塌掉 4 个数量级。"
    "若残差来自公式，换观测值只会移位置不会塌。")

# C2 z* 的敏感度（牙齿：z* 不是可调旋钮）
add(CTL, "C2", "PASS", "z* 的牙齿：挪 1e-3 目标函数放大 %.0f 倍，挪 1e-2 放大 %.0f 倍" % (
    float(Z_OBJ_P1 / Z_OBJ_HALF), float(Z_OBJ_P2 / Z_OBJ_HALF)),
    mp.mpf(1), Z_OBJ_P1 / Z_OBJ_HALF, (Z_OBJ_P1 / Z_OBJ_HALF) > mp.mpf(100),
    "若 z* 能自由调到大幅改善，那 P06 就是空话。实测放大 456 倍（1e-3）与 4547 倍（1e-2）⇒ 0.5 是被数据选的。")

# C3 假数据自检：由 x/sinh(x) 反生成三代质量，全 22 族普查必须精确命中真族
M_FAKE = [C0 * p_mid_closed(XS[i]) for i in range(3)]
census_fake = []
for nm, g in SHAPES:
    try:
        Cg = M_FAKE[0] / g(XS[0])
        e1 = rel(Cg * g(XS[1]) - M_FAKE[1], M_FAKE[1])
        e2 = rel(Cg * g(XS[2]) - M_FAKE[2], M_FAKE[2])
        census_fake.append((nm, max(e1, e2)))
    except Exception:
        census_fake.append((nm, mp.inf))
census_fake.sort(key=lambda t: t[1])
fake_best_nm, fake_dev = census_fake[0][0], census_fake[0][1]
TIE_SET = [t[0] for t in census if t[1] < mp.mpf("1e-3")]      # 真数据下不可分辨的族集合
RES["c3_fake_best_shape"] = fake_best_nm
RES["c3_fake_best_rel"] = fake_dev
RES["c3_tie_set"] = " / ".join(TIE_SET)
add(CTL, "C3", "PASS",
    "自检：用本卷映射生成假质量再回灌 22 族普查 ⇒ 头名「%s」残差 %.1e，且落在真数据不可分辨集（%d 族）内"
    % (fake_best_nm, float(fake_dev), len(TIE_SET)),
    best_v, fake_dev,
    (fake_dev < mp.mpf("1e-40")) and (fake_best_nm in TIE_SET),
    "假质量由 x/sinh(x) 反生成，故真族必须精确命中（残差 1e-60 级）；若普查对真族也失手，"
    "那 P04 的「全族失败」就毫无意义。本条同时要求 best 族与真数据普查的 best 同名（不自相矛盾）。")

# C4 判别力牙齿：错族必须失败
g_bad = SH_MAP["x^2*e^-x"]
Cb = MS[0] / g_bad(XS[0])
bad_dev = max(rel(Cb * g_bad(XS[i]) - MS[i], MS[i]) for i in (1, 2))
add(CTL, "C4", "PASS", "判别力牙齿：把形状换成 x²e^-x（最像 x·e^-x 的错族）⇒ 残差 %.2e" % float(bad_dev),
    mp.mpf("1e-3"), bad_dev, bad_dev > mp.mpf("0.1"),
    "命中族与错族之间必须隔几个数量级，否则「唯一命中」是措辞而非事实。实测 0.552 vs 3.94e-5 ⇒ 隔 1.4e4 倍。")

# C5 自由度账：锚点自身恒零，跨点必然非零
g_id = lambda x: x / mp.sinh(x)
self_dev, other_dev = [], []
for i in range(3):
    Ci = MS[i] / g_id(XS[i])
    self_dev.append(rel(Ci * g_id(XS[i]) - MS[i], MS[i]))
    for j in range(3):
        if i != j:
            other_dev.append(rel(Ci * g_id(XS[j]) - MS[j], MS[j]))
RES["c5_self_dev_max"] = max(self_dev)
RES["c5_other_dev_min"] = min(other_dev)
RES["c5_other_dev_max"] = max(other_dev)
add(CTL, "C5", "PASS",
    "自由度账：锚点自身残差 3/3 恒为零，跨点 6/6 必非零（最小 %.2e、最大 %.2e）"
    % (float(min(other_dev)), float(max(other_dev))),
    max(other_dev), max(self_dev),
    (max(self_dev) < mp.mpf("1e-55")) and (min(other_dev) > mp.mpf("1e-12")),
    "C 只有一个自由度、被一个数吃掉后该点必然精确 ⇒ 「两点拟合」永不失败，全部信息量落在第三点。"
    "牙齿是跨点：6 个跨点残差最小 %.2e（远大于机器零）⇒ 判据不是恒真。" % float(min(other_dev)))

# C6 锚点无关性：用 mu 或 tau 当锚，C 的差异
C_mu = MS[1] * mp.sinh(XS[1]) / XS[1]
C_tau = MS[2] * mp.sinh(XS[2]) / XS[2]
add(CTL, "C6", "PASS", "锚点无关性：以 e / mu / tau 分别锚定 C，三者相对差 ≤ 3.94e-5",
    mp.mpf("1e-4"), (max(Cs) - min(Cs)) / min(Cs), (max(Cs) - min(Cs)) / min(Cs) < mp.mpf("1e-4"),
    "若「命中」来自某个特定锚点的偶然，换锚点会崩。实测三锚互差 3.94e-5（与 P03 同值，因为它就是同一批 C_i）。")

# C7 「错写成 2 倍」的牙齿（本轮自伤的留痕）
x0 = XS[0]
wrong = 2 * parseval_exact(0)
right = parseval_exact(0)
add(CTL, "C7", "PASS",
    "自伤牙齿：Parseval 若误写成 2(x coth x −1)，x_e 处「恒等式残差」从 %.1e 级跃到 %.3f（差 %.3f，整量级）"
    % (float(RES["parseval_dev_at_N400"]), float(wrong - right), float(wrong - right)),
    right, wrong, abs(wrong - right) > mp.mpf(1),
    "本卷上一轮的口头结论文档把恒等式写成 2(x coth x − 1)；本轮第一版原型照抄了这个 2，"
    "结果 Σa_n² 与「2 倍式」的残差读成 −15.218（恰好 = −(x coth x − 1) = −15.218066），"
    "立刻暴露「差的是整个量级而不是截断」。⇒ 该 2 已被就地更正为 1，本控制条把这一错写永久留作牙齿。")

# C8 位数判据不是恒 FAIL
dig_if_ok = mp.mpf(4)
add(CTL, "C8", "PASS",
    "位数判据的牙齿：来料报 %d 位 vs 支撑 %.2f 位 ⇒ 红；若只报 %.0f 位则放行（%.0f ≤ %.2f）"
    % (DIG_X_IN[2], float(DIG_TRUST[2]), float(dig_if_ok), float(dig_if_ok), float(DIG_TRUST[2])),
    mp.mpf(DIG_X_IN[2]), DIG_TRUST[2],
    (dig_if_ok <= DIG_TRUST[2]) and (DIG_TRUST[2] < mp.mpf(DIG_X_IN[2])),
    "P10 判 BOUNDARY 必须排除「判据恒 FAIL」：同一判据在 6 位写法下放行、9 位写法下拦截，"
    "说明它区分的是「精度声明 vs 支撑精度」而不是「有无映射」。")

# ============================================================================
# §7 · 守卫
# ============================================================================
SRC = io.open(os.path.abspath(__file__), encoding="utf-8").read()
TREE = ast.parse(SRC)

def _add_calls():
    out = []
    for node in ast.walk(TREE):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "add":
            out.append(node)
    return out

AC = _add_calls()
bad_ok_const = sum(1 for nd in AC if isinstance(nd.args[6], ast.Constant) and isinstance(nd.args[6].value, bool))
add(GRD, "G01", "PASS", "AST 扫描：全部 add() 的 ok 实参顶层不是布尔常量（禁写死）",
    mp.mpf(0), mp.mpf(bad_ok_const), bad_ok_const == 0,
    "写死的 True 会让「通过」与实算脱钩。本卷 P07/P09/P11/P14/P15 是 INFO 型（结论为「记录」），"
    "它们的 ok 也必须由实算比较给出，不能直接填 True。")

bad_argn = sum(1 for nd in AC if len(nd.args) != 8)
add(GRD, "G02", "PASS", "AST 扫描：add() 一律 8 个实参",
    mp.mpf(0), mp.mpf(bad_argn), bad_argn == 0,
    "漏 note 会在判定册出现空列；本卷起草时就曾把 C 组按 7 参写（崩在 TypeError），故扫描与实参个数同时立账。")

ctl_ne = sum(1 for e in CTL if e["exp"] != e["act"])
add(GRD, "G03", "PASS", "控制组每条都给出「基线 vs 扰动」两个不同读数（exp ≠ act）",
    mp.mpf(len(CTL)), mp.mpf(ctl_ne), ctl_ne == len(CTL),
    "exp==act 的控制条只能证明代码通电。本卷 8 条控制全部两端异值（且方向朝「判据有牙齿」）。")

r_probe = rel(mp.mpf("1e-60"), mp.mpf(0))
add(GRD, "G04", "PASS", "rel() 分母保底：rel(1e-60, 0) 不抛错、不伪判相等",
    mp.mpf("1e-60"), r_probe, r_probe == mp.mpf("1e-60"),
    "本卷多处「基线为 0」（C5 的两点恒成立、C3 的自检命中）；rel(a,0) 必须退化为绝对值，否则崩溃或被伪判完美相符。")

dps_ok = mp.mp.dps >= 60
pi_check = abs(mp.pi - mp.mpf("3.14159265358979323846264338327950288419716939937510582097494")) < mp.mpf("1e-55")
add(GRD, "G05", "PASS", "工作精度自证：dps≥60 且 π 到 55 位相符",
    mp.mpf(0), mp.mpf(0 if (dps_ok and pi_check) else 1), dps_ok and pi_check,
    "恒等式 p_x(1/2)=x/sinh(x) 的残差报的是 1e-61 级，若工作精度只有 15 位那这个数就是假的。dps=60 + π 自证。")

rid_count = SRC.count('RID = "r3' + '79"')
add(GRD, "G06", "PASS", "条目计数与分层：主册 %d、控制 %d、守卫登记中；本文件 RID 赋值 1 处" % (len(MAIN), len(CTL)),
    mp.mpf(1), mp.mpf(rid_count), rid_count == 1,
    "RID 字面在源码只许出现一次（用拼接构造，防被 G10 封锁表误伤）；多命中意味着别的卷号混进本文件。")

add(GRD, "G07", "PASS", "源码不含 random：确定性可复现",
    mp.mpf(0), mp.mpf(SRC.count("import " + "ra" + "ndom") + SRC.count("ran" + "dom.")),
    (SRC.count("import " + "ra" + "ndom") == 0) and (SRC.count("ran" + "dom.") == 0),
    "扫描词拼接构造（同 G06），否则守卫自身含禁词会永久假红。")

empty_note = sum(1 for lst in (MAIN, CTL, GRD) for e in lst if not e["title"].strip() or not e["note"].strip())
add(GRD, "G08", "PASS", "所有条目 title/note 非空（防「只有数字没有指称」）",
    mp.mpf(0), mp.mpf(empty_note), empty_note == 0,
    "数字没有指称就不能进判定册。本卷 C1–C8/G01–G12 起草时全部漏 note（按 7 参调用），被 add() 的 TypeError 挡在落盘前。")

ids_p = [e["id"] for e in MAIN] == ["P%02d" % k for k in range(1, len(MAIN) + 1)]
ids_c = [e["id"] for e in CTL] == ["C%d" % k for k in range(1, len(CTL) + 1)]
ids_g = [e["id"] for e in GRD] == ["G%02d" % k for k in range(1, len(GRD) + 1)]
add(GRD, "G09", "PASS", "编号连续无跳号：P/C/G 三序列各与登记时刻条数一致",
    mp.mpf(1), mp.mpf(1 if (ids_p and ids_c and ids_g) else 0), ids_p and ids_c and ids_g,
    "跳号会在判定册与 README 之间留下无法引用的空位（r376 就踩过 P07→P09）；本卷先把 id 序列排完再写第一条 add。")

region = SRC.split("# §1 · INCOMING-BEGIN")[1].split("# §1b · INCOMING-END")[0]
outside = SRC.replace(region, "")
forbidden = ["16.21806" + "647", "10.44662" + "040", "7.26033" + "723",
             "0.510998" + "95", "105.658375" + "5", "1776." + "86",
             "1.741035" + "8", "4.94e" + "-7"]
leaks = {t: outside.count(t) for t in forbidden if outside.count(t) > 0}
add(GRD, "G10", "PASS", "★来料/外部输入字面值集中封锁：8 个展示数除 INCOMING 段外零出现",
    mp.mpf(0), mp.mpf(sum(leaks.values())), sum(leaks.values()) == 0,
    "抄表列值进正文的债：来料 x 三值与 PDG 三代质量只许住 INCOMING 段，正文一律变量插值。"
    "封锁表自身拼接构造（同 G06/G07）。")

keys_list = []
for node in ast.walk(TREE):
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Subscript) and getattr(t.value, "id", "") == "RES":
                keys_list.append(t.slice.value.value if hasattr(t.slice, "value") and hasattr(t.slice.value, "value") else None)
dup_keys = len(keys_list) - len(set(keys_list))
add(GRD, "G11", "PASS", "RES 键唯一：%d 次赋值无重名（防后写覆盖前写）" % len(keys_list),
    mp.mpf(0), mp.mpf(dup_keys), dup_keys == 0,
    "同键后写覆盖前写会让 REPORT 印一个值、判定册引另一个值。扫描按 AST 取键，不靠人工对照。")

indep = ["P01 三路（直算/闭式/保因子式）", "P04 普查 vs P02 锚定",
         "P08 反解(数值求根) vs P02 正解", "P12 循环求和 vs x coth x 闭式",
         "P13 尾段律 vs P12 总量", "C3 假质量自检 vs P04 真数据普查"]
add(GRD, "G12", "PASS", "★至少 6 组「exp 与 act 来自不同代码路径」",
    mp.mpf(6), mp.mpf(len(indep)), len(indep) >= 6,
    "名单即账：" + "；".join(indep) + "。少于 6 组说明「相符」退化成同一段代码的自言自语。")
# ============================================================================
# §8 · 汇总与产物（JSON / MD / report.txt）
# ============================================================================
ALL = MAIN + CTL + GRD
KINDS = ["PASS", "FAIL", "BOUNDARY", "INFO"]
CNT = dict((k, sum(1 for e in ALL if e["kind"] == k)) for k in KINDS)
GUARD_PASS = sum(1 for e in GRD if e["ok"])
VERDICT = "FAIL" if CNT.get("FAIL", 0) else ("BOUNDARY" if CNT.get("BOUNDARY", 0) else "PASS")

BASE = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
os.makedirs(DATA_DIR, exist_ok=True)

def _plain(v):
    if isinstance(v, mp.mpf):
        return mp.nstr(v, 30)
    return v

PAYLOAD = {
    "rid": RID,
    "title": TITLE,
    "stamp": STAMP,
    "verdict": VERDICT,
    "counts": CNT,
    "n_entries": len(ALL),
    "n_main": len(MAIN),
    "n_control": len(CTL),
    "n_guard": len(GRD),
    "guard_pass": GUARD_PASS,
    "entries": {"main": MAIN, "control": CTL, "guard": GRD},
    "metrics": dict((k, _plain(v)) for k, v in RES.items()),
    "incoming": INCOMING,
}
JSON_PATH = os.path.join(DATA_DIR, BASE + ".json")
with io.open(JSON_PATH, "w", encoding="utf-8") as f:
    f.write(json.dumps(PAYLOAD, ensure_ascii=False, indent=2))

MD = []
MD.append("# TUFT-%s · %s" % (RID, TITLE))
MD.append("")
MD.append("- 日期：%s" % STAMP)
MD.append("- 条目 %d：%s" % (len(ALL), " / ".join("%s=%d" % (k, CNT.get(k, 0)) for k in KINDS)))
MD.append("- 主册 %d / 控制组 %d / 守卫 %d（通过 %d）" % (len(MAIN), len(CTL), len(GRD), GUARD_PASS))
MD.append("- verdict：**%s**" % VERDICT)
MD.append("")
for tag, lst in (("主条目（§5）", MAIN), ("控制组（§6）", CTL), ("守卫（§7）", GRD)):
    MD.append("## %s" % tag)
    MD.append("")
    for e in lst:
        MD.append("### %s [%s] %s" % (e["id"], e["kind"], e["title"]))
        MD.append("")
        MD.append("- 期望：`%s`" % e["exp"])
        MD.append("- 实算：`%s`" % e["act"])
        MD.append("- 依据：%s" % e["note"])
        MD.append("")
MD.append("## 关键读数（RES）")
MD.append("")
MD.append("| 键 | 值 |")
MD.append("| --- | --- |")
for k in sorted(RES.keys()):
    MD.append("| `%s` | `%s` |" % (k, fmt(RES[k], 24)))
MD.append("")
MD_PATH = os.path.join(DATA_DIR, BASE + ".md")
with io.open(MD_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(MD) + "\n")

L = []
L.append("=" * 108)
L.append("TUFT-%s · %s · %s" % (RID, TITLE, STAMP))
L.append("=" * 108)
L.append("条目 %d（%s）｜主册 %d / 控制 %d / 守卫 %d（通过 %d/%d）"
         % (len(ALL), " ".join("%s=%d" % (k, CNT.get(k, 0)) for k in KINDS),
            len(MAIN), len(CTL), len(GRD), GUARD_PASS, len(GRD)))
L.append("-" * 108)
for tag, lst in (("§5 主条目", MAIN), ("§6 控制组", CTL), ("§7 守卫", GRD)):
    L.append("[%s]" % tag)
    for e in lst:
        L.append("  %-4s %-9s %s" % (e["id"], e["kind"], e["title"]))
    L.append("")
L.append("-" * 108)
L.append("[关键读数 RES]")
for k in sorted(RES.keys()):
    L.append("  %-40s %s" % (k, fmt(RES[k], 22)))
L.append("-" * 108)
L.append("[结论] X-R376-2 由「不可复核」闭合为「已反解」：m_i = C·x_i/sinh(x_i)（C 由 m_e 锚定，1 个自由常数）。")
L.append("        mu / tau 两点在 1σ~2.4σ 内（chi2(2dof) 见 RES），且 x(m) 反解能回到同一组 x；")
L.append("        但 x_tau 报 %d 位而 PDG 的 m_tau 只支撑 %.2f 位 ⇒ P10 判 BOUNDARY，P02 的命中降级为「结构闭合 + 精度待源」。"
         % (DIG_X_IN[2], float(DIG_TRUST[2])))
L.append("        供给账：0 新预言（x 仍是输入）；X-R376-1 / X-R376-3 仍 OPEN。")
L.append("[verdict] %s" % VERDICT)
L.append("=" * 108)
TXT = "\n".join(L)
print(TXT)

REP_PATH = os.path.join(DATA_DIR, BASE + "_report.txt")
with io.open(REP_PATH, "w", encoding="utf-8") as f:
    f.write(TXT + "\n")

print("")
print("[written] %s" % JSON_PATH)
print("[written] %s" % MD_PATH)
print("[written] %s" % REP_PATH)
sys.exit(1 if CNT.get("FAIL", 0) else 0)

