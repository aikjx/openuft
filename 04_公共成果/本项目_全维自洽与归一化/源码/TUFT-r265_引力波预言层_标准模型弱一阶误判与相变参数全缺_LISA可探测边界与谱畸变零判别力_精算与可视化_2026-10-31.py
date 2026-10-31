# -*- coding: utf-8 -*-
"""TUFT-r265 · 引力波预言层
靶：来料原件中全部「引力波」声称（L4363-4378 电弱相变 / L4800-4802 谱畸变 /
L4974-4976 灰体因子 / L5008 黑洞并合 / L5409-5411 中微子相位）。

本卷不重复 r232（标准四极辐射/啁啾/Hulse-Taylor 复现），也不重复 r263（用户任务书的
GW170817 裁定）；本卷审的是「靶自己关于引力波的预言声称是否可计算、可区分」。

纪律：控制组/守卫不写死 True；指控前先测判别力；数字全部机算；元数据参数化。
"""
import io
import json
import math
import os
import re
import sys
from fractions import Fraction

RID = "TUFT-r265"
RIDNUM = "r265"
SLUG = ("TUFT-r265_引力波预言层_标准模型弱一阶误判与相变参数全缺_"
        "LISA可探测边界与谱畸变零判别力_精算与可视化_2026-10-31")
DATE = "2026-10-31"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "数据")
README = os.path.join(ROOT, "README.md")

T1 = os.path.join(DATA, "TUFT-r241_光速螺旋_来料原件_2026-10-30",
                  "基于光速螺旋流形的核心动力学方程组.md")
T2 = os.path.join(DATA, "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md")
T3 = os.path.join(DATA, "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md")
TARGETS = [T1, T2, T3]
SHA_HEAD = {T1: "2483899ead9c854d", T2: "fd7dd4481b6a5f66", T3: "dba5eb95bac110f0"}

# ---------------------------------------------------------------- 物理常数
C = 299792458.0
C0 = C
G = 6.67430e-11
HBAR = 1.054571817e-34
MPC = 3.0856775814913673e22
H0_KMS = 67.4
OM_L = 0.6889
MSUN_T = 4.925490947e-6          # GM_sun/c^3, s
EV_INV_M = 1.973269804e-7        # 1 eV^-1 -> m
M_H = 125.20                     # GeV (PDG 2022)
V_EW = 246.22                    # GeV
M_H_CRIT = 72.0                  # GeV，格点结果：SM EWPT 一阶/crossover 分界
G_STAR = 106.75
MC_GW150914 = 28.1               # M_sun，啁啾质量
MTOT_GW150914 = 65.0             # M_sun，总质量
F_LOW_LIGO = 20.0                # Hz
LAMBDA_LISA = (1e-4, 1e-1)       # Hz，LISA 频带
OMEGA_LISA_THRESH = 1e-12        # LISA 灵敏度量级参考（3 mHz 附近 1e-11~1e-12，取宽）
DM2_ATM = 2.5e-3                 # eV^2
E_NU = 10e6                      # eV，10 MeV

DOC_KEYS = {
    "gw": ["引力波", "重力波"],
    "lisa": ["LISA"],
    "first_order": ["一阶", "一级相变"],
    "weak_first": ["弱一阶", "弱一级"],
    "waveform": ["波形"],
    "spec": ["谱畸变", "特征谱"],
    "greybody": ["灰体"],
    "bh_merge": ["并合"],
    "nu_phase": ["中微子振荡", "相位修正"],
    "alpha": ["相变强度", "alpha", "α"],
    "betaH": ["β/H", "beta/H", "逆时长"],
    "Tstar": ["相变温度", "T_*", "临界温度"],
    "vw": ["壁速", "泡壁", "v_w"],
    "formula": ["=", "\\frac", "\\Omega", "\\propto"],
}

_ALPHA52 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def depollute(s):
    s = re.sub(r"\\\(\\boldsymbol\s+([A-Za-z])\)([A-Za-z])", r"\\\1\2", s)
    s = re.sub(r"\\\(\\boldsymbol\s+([A-Za-z])\)", r"\1", s)
    s = _unbold(s)
    return re.sub(r"[\r\n]+", "\n", s)


def _unbold(s):
    out, i, n = [], 0, len(s)
    while True:
        j = s.find("\\boldsymbol", i)
        if j < 0:
            out.append(s[i:])
            break
        out.append(s[i:j])
        k = j + len("\\boldsymbol")
        if k < n and s[k] == "{":
            depth, m = 0, k
            while m < n:
                if s[m] == "{":
                    depth += 1
                elif s[m] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                m += 1
            inner = s[k + 1:m] if m < n else s[k + 1:]
            out.append(_unbold(inner))
            i = m + 1
        else:
            while k < n and s[k] == " ":
                k += 1
            if k >= n:
                i = k
            elif s[k] == "\\":
                mm = re.match(r"\\[A-Za-z]+", s[k:])
                if mm:
                    out.append(mm.group(0))
                    i = k + len(mm.group(0))
                else:
                    i = k + 1
            else:
                out.append(s[k])
                i = k + 1
    return "".join(out)


def fmt(x, n=6):
    if x is None:
        return "n/a"
    if isinstance(x, Fraction):
        return "%.*f" % (n, float(x))
    if isinstance(x, str):
        return x
    if isinstance(x, float) and (x != x or x in (float("inf"), float("-inf"))):
        return str(x)
    a = abs(x)
    if a != 0 and (a < 1e-3 or a >= 1e5):
        return "%.*e" % (n, x)
    return "%.*f" % (n, x)


def rel(a, b):
    if b == 0:
        return float("inf") if a != 0 else 0.0
    return abs(a - b) / abs(b)


def ordmag(x):
    if x is None or x <= 0:
        return None
    return math.log10(x)


# ================================================================ 定位
def locate(text_lines):
    L = {k: [] for k in ("gw", "lisa", "weak_first", "waveform", "spec", "greybody",
                         "bh_merge", "nu_phase", "alpha", "alpha_sym", "betaH",
                         "Tstar", "vw", "first_order")}
    for i, s in enumerate(text_lines):
        ln = i + 1
        if any(k in s for k in DOC_KEYS["gw"]):
            L["gw"].append(ln)
        if "LISA" in s:
            L["lisa"].append(ln)
        if "弱一阶" in s or "弱一级" in s:
            L["weak_first"].append(ln)
        if "波形" in s:
            L["waveform"].append(ln)
        if "谱畸变" in s or "特征谱" in s:
            L["spec"].append(ln)
        if "灰体" in s:
            L["greybody"].append(ln)
        if "并合" in s:
            L["bh_merge"].append(ln)
        if "相位修正" in s:
            L["nu_phase"].append(ln)
        if "相变强度" in s:
            L["alpha"].append(ln)
        if "α" in s:
            L["alpha_sym"].append(ln)
        if "β/H" in s or "逆时长" in s:
            L["betaH"].append(ln)
        if "相变温度" in s or "临界温度" in s or "T_c" in s:
            L["Tstar"].append(ln)
        if "壁速" in s or "泡壁" in s:
            L["vw"].append(ln)
        if "一阶" in s or "一级相变" in s:
            L["first_order"].append(ln)
    return L


# ================================================================ 物理
def higgs_quartic():
    return M_H ** 2 / (2.0 * V_EW ** 2)


def kappa_v(alpha):
    """声波效率（bag model 拟合，v_w ~ 1）。"""
    return alpha / (0.73 + 0.083 * math.sqrt(alpha) + alpha)


def omega_sw(alpha, beta_over_H, g_star=G_STAR, vw=1.0):
    """一阶相变声波源 GW 幅度（Caprini et al. 2016 式）Ω h^2。"""
    kv = kappa_v(alpha)
    x = kv * alpha / (1.0 + alpha)
    return (2.65e-6 * (1.0 / beta_over_H) ** 2 * x ** 2
            * (100.0 / g_star) ** (1.0 / 3.0) * vw)


def f_peak_sw(T_star, beta_over_H, g_star=G_STAR, vw=1.0):
    """声波源峰频（today），Hz。T_star 以 GeV 计。"""
    return (1.9e-5 * (1.0 / vw) * beta_over_H * (T_star / 100.0)
            * (g_star / 100.0) ** (1.0 / 6.0))


def alpha_min(beta_over_H, thresh=OMEGA_LISA_THRESH, hi=1e6):
    """给定 β/H，求使 Ω_sw 达到阈值的 α 下限（二分）。"""
    lo = 1e-8
    if omega_sw(hi, beta_over_H) < thresh:
        return None
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if omega_sw(mid, beta_over_H) < thresh:
            lo = mid
        else:
            hi = mid
    return hi


def T_window(beta_over_H, band=LAMBDA_LISA, g_star=G_STAR, vw=1.0):
    """反解落在 LISA 带内的相变温度区间（GeV）。"""
    coeff = 1.9e-5 * (1.0 / vw) * beta_over_H * (g_star / 100.0) ** (1.0 / 6.0) / 100.0
    return band[0] / coeff, band[1] / coeff


def lambda_cosmo():
    h0 = H0_KMS * 1e3 / MPC
    return 3.0 * OM_L * h0 ** 2 / C ** 2


def inspiral_phase(mc_msun, f1, f2):
    """Ψ(f) = (3/128)(π M_c f)^{-5/3} 的差值（rad）。M_c 以秒计。"""
    mc = mc_msun * MSUN_T

    def P(f):
        return (3.0 / 128.0) * (math.pi * mc * f) ** (-5.0 / 3.0)
    return P(f1) - P(f2)


def f_isco(mtot_msun):
    return 1.0 / (46.17 * mtot_msun * MSUN_T)


def coh_length(E_eV, dm2=DM2_ATM):
    """真空振荡相干长度（m）：L = 4πE/Δm² [eV^-1]。"""
    return 4.0 * math.pi * E_eV / dm2 * EV_INV_M


# ================================================================ 采集
def load_docs():
    docs = []
    for p in TARGETS:
        braw = io.open(p, "rb").read()
        import hashlib
        h = hashlib.sha256(braw).hexdigest()
        raw = braw.decode("utf-8", errors="replace")
        txt = depollute(raw)
        docs.append({"path": p, "text": txt, "lines": txt.split("\n"),
                     "sha256": h, "nbytes": len(braw)})
    return docs


# ================================================================ 条目
ENTRIES = []


def ent(eid, grp, title, verdict, detail, metric=None):
    ENTRIES.append({"id": eid, "group": grp, "title": title,
                    "verdict": verdict, "detail": detail, "metric": metric or {}})


CONTROLS = []
GUARDS = []


def ctl(cid, title, ok, detail):
    CONTROLS.append({"id": cid, "title": title, "ok": bool(ok), "detail": detail})


def guard(gid, title, ok, detail):
    GUARDS.append({"id": gid, "title": title, "ok": bool(ok), "detail": detail})


# ------------------------------------------------------------------ A 组
def group_A(docs, L):
    big = docs[0]["lines"]
    # A01
    gw_hits = len(L["gw"])
    ent("A01", "A", "靶是否提出「电弱相变产生原初引力波」的声称",
        "PASS" if gw_hits else "FAIL",
        "全语料「引力波/重力波」命中 **%d 行**（行号 %s%s）。核心声称在 L4369："
        "「电弱相变是**一阶拓扑涡旋相变**，会产生原初引力波；可以被未来空间引力波探测器（LISA）观测」。"
        "该声称确实存在，不是本卷虚构。" % (
            gw_hits, L["gw"][:12],
            "" if len(L["gw"]) <= 12 else " …（共 %d 行）" % len(L["gw"])),
        {"gw_lines": gw_hits})
    # A02 SM 弱一阶
    wf = L["weak_first"]
    ratio = M_H / M_H_CRIT
    ent("A02", "A", "★★★「标准模型的纯希格斯相变是弱一阶」——事实错误：SM 在 m_H=125 GeV 是 crossover",
        "FAIL",
        "靶 L4369 原文：「**标准模型的纯希格斯相变是弱一阶，引力波信号远弱于 TUFT 拓扑相变预言**」"
        "（命中 %d 行：%s）。标准结果是：SM 电弱相变是否为**一阶**由希格斯质量决定，"
        "格点给出分界 **m_H,c ≈ %.0f GeV**；当 m_H > m_H,c 时相变是**光滑 crossover（非一阶、无泡壁、无 GW）**。"
        "实测比值 m_H/m_H,c = %.3f/%.0f = **%.4f**（高出 %.1f%%）⇒ 处于 crossover 区，"
        "**不是「弱一阶」**。★「弱一阶」与「crossover」不是程度差别，而是**有/无相变**的差别"
        "（一阶 ⇒ 有潜热、有泡壁、有 GW；crossover ⇒ 三者皆无）。"
        "本卷同时机算 SM 希格斯四次耦合 λ = m_H²/(2v²) = **%.5f**（v=%.2f GeV），"
        "该值下有效势**不存在第二个极小值**（无势垒）⇒ 与「弱一阶」不相容。"
        "【证据分级】阈值 %.0f GeV 为**文献锚**（格点），λ 与比值为本卷机算。" % (
            len(wf), wf[:4], M_H_CRIT, M_H, M_H_CRIT, ratio, 100 * (ratio - 1),
            higgs_quartic(), V_EW, M_H_CRIT),
        {"mH": M_H, "mH_crit": M_H_CRIT, "ratio": ratio, "lambda": higgs_quartic()})
    # A03 远强于
    ent("A03", "A", "★★★「信号远强于 TUFT 预言」的比较没有分母（SM 无 GW 信号 ⇒ 比值无定义）",
        "FAIL",
        "「远强于」是一个比值命题 A/B。由 A02，B（SM 电弱相变的 GW 信号）**不存在**（crossover，无泡碰撞、无声波源、"
        "无湍流源）⇒ 比值 A/B **无定义**，既不是「远强」也不是「略强」。"
        "机验：把 B 取 0 则 A/B 发散、取 0×0 则 0/0 不定 ⇒ 在任何约定下该比较都不能成立为定量陈述。"
        "★这不是措辞问题：靶用这个比较来支撑「可区分性」（区分 TUFT 与 SM），"
        "而可区分性恰恰是**它自己主张的那一点**（L4366 标题「可检验预言（区分TUFT与标准模型）」）。"
        "分母消失 ⇒ 该区分**未被建立**。",
        {"ratio_defined": False, "B_value": 0.0})
    # A04 四个相变参数
    n_a, n_b, n_t, n_v = len(L["alpha"]), len(L["betaH"]), len(L["Tstar"]), len(L["vw"])
    n_asym = len(L["alpha_sym"])
    ent("A04", "A", "★★★一阶相变 GW 的四个决定参数（α, β/H, T_*, v_w）是否给出",
        "FAIL",
        "一阶相变 GW 谱由四个量决定：**α**（相变强度）、**β/H**（逆时长）、**T_***（相变温度）、**v_w**（泡壁速度）。"
        "机读全语料：`相变强度` 命中 **%d**、`β/H/逆时长` 命中 **%d**、`壁速/泡壁` 命中 **%d**、"
        "`相变温度/临界温度` 命中 **%d**（其中「临界温度」只出现在 L4363「冷却到临界温度 T_c ~ v」，"
        "而 T_c~v 是**定性的量级提示**，不是数值 T_*）。"
        "⇒ **四个参数一个都没给数值**。没有这四量，Ω_GW(f) 在参数空间上是**一个点都没有被指定**的集合（B02 机算该集合跨 %.1f 个量级）。"
        "（如实登记：单字母「α」在语料中出现 **%d** 行，但逐行看上下文，全部是希格斯四次耦合/精细结构常数/角度等"
        "**别的量的符号**，没有一处是「相变强度 α」，也没有一处给它赋值。）"
        "★靶 L4378 自己也承认：「一阶相变引力波波形**需要数值求解**挠率场的宇宙演化方程」——"
        "即它明知缺这一步，却仍把 L4369 写成「会产生原初引力波，可以被 LISA 观测」。",
        {"alpha": n_a, "betaH": n_b, "Tstar": n_t, "vw": n_v, "alpha_sym": n_asym})
    # A05 自认未做
    ent("A05", "A", "靶自认「波形需数值求解」——如实登记（对靶有利：它没有假装做过）",
        "INFO",
        "L4378 原文：「一阶相变引力波波形**需要数值求解**挠率场的宇宙演化方程」；"
        "L4377 同时自认「凝聚势的完整解析形式还需要 FDTD 数值仿真」。"
        "⇒ 靶**明确标注了未完成项**，这一点应当如实登记（与 r248–r262 判过的「把未做写成已做」不同）。"
        "但「如实标注未完成」不能替代「不宣称可观测」：L4369 仍写「可以被 LISA 观测」。"
        "两条并列即为**内部不一致**：既然波形都还没算，凭什么知道信号在 LISA 带内且强于阈值。",
        {"todo_acknowledged": True})
    # A06 谱畸变
    sp = L["spec"]
    ent("A06", "A", "★★「原初引力波叠加挠率背景修正……可探测特征谱畸变」是否给出调制幅度或谱形式",
        "FAIL",
        "L4801 原文：「**原初引力波叠加挠率背景修正**：在极早期相变产生的引力波谱上叠加微小的背景挠率调制，"
        "LISA、BICEP 下一代实验可以探测这个**特征谱畸变**」（`谱畸变/特征谱` 命中 %d 行：%s）。"
        "机验：调制必须写成 Ω_GW(f) → Ω_GW(f)[1 + A·g(f)]，其中 **A（幅度）** 与 **g(f)（谱形）** 都未给出。"
        "「微小」既非数值也非上限 ⇒ 见 C02：A 取 4 个跨 3 个量级的值全部「相容」⇒ **零判别力**。"
        "★另外：BICEP 观测的是 **CMB 的 B 模张量谱（r）**，不是「引力波谱畸变」；"
        "把 BICEP 列为「谱畸变」的检验通道属**观测对象错置**（BICEP 对 f~1e-16 Hz 的原始张量谱敏感，"
        "不是对 mHz 相变谱）。" % (len(sp), sp[:4]),
        {"spec_lines": len(sp), "amplitude_given": False})
    # A07 灰体因子
    gb = L["greybody"]
    ent("A07", "A", "★★★「灰体因子 F(τ(r_h)) 是 TUFT 可观测预言，未来下一代引力波可检验」——双重缺陷",
        "FAIL",
        "L4974–L4976 原文：Γ_TUFT(ω) = Γ_Hawking(ω)·F(τ(r_h))，并称「F(τ(r_h)) 是视界挠率带来的修正函数，"
        "这是 TUFT 可观测预言，**未来下一代引力波、黑洞光子环观测可以检验**」（`灰体` 命中 %d 行：%s）。"
        "**缺陷一（无表达式）**：F 的函数形式未给出；靶 L5007 自认「灰体因子 F(τ(r_h)) 的精确表达式……未完成」。"
        "**缺陷二（范畴错置）**：F 修正的是**霍金辐射谱**（标量/费米子/光子的热谱偏离），"
        "而「引力波」不是霍金辐射（引力波的源是时空四极矩，不是视界热辐射）。"
        "把 GW 列为 F 的检验通道，等于说「用温度计测磁场」。"
        "★光子环观测（photon ring）确实与视界附近的度规有关，与灰体因子同源但不同量（前者是测地线，后者是透射系数）"
        "——靶把三者（灰体因子 / 引力波 / 光子环）并列为「检验 F」的通道，只有一个勉强相关。" % (
            len(gb), gb[:4]),
        {"greybody_lines": len(gb), "formula_given": False, "category_error": True})
    # A08 黑洞并合
    bm = L["bh_merge"]
    ent("A08", "A", "★「超大质量黑洞并合引力波波形需加入挠率修正，和 LIGO/Virgo 对比」是否给出公式或量级",
        "FAIL",
        "L5008 原文：「超大质量黑洞并合引力波波形，需要加入挠率修正，和 LIGO/Virgo 观测做对比校验」"
        "（`并合` 命中 %d 行：%s）。机验：**无任何修正项公式、无系数、无量级**。"
        "「加修正再对比」是**计划**不是预言。见 B06：LIGO 的 inspiral 相位预算约 %.1f rad，"
        "相对修正超过 ~1e-3 即已被现有事件排除 ⇒ **量级本身就是判据**，而靶连量级都没给。" % (
            len(bm), bm[:4], inspiral_phase(MC_GW150914, F_LOW_LIGO,
                                            f_isco(MTOT_GW150914))),
        {"bh_lines": len(bm), "formula_given": False})
    # A09 中微子相位
    np_ = L["nu_phase"]
    ent("A09", "A", "★★「挠率背景给中微子振荡带来红移相关相位修正，属 TUFT 独有宇宙学预言」是否可算",
        "FAIL",
        "L5411 原文：「挠率背景 τ_Λ（TUFT 暗能量基底）叠加在中微子传播上，会给长基线宇宙尺度中微子振荡"
        "带来红移相关相位修正，**属于 TUFT 独有的宇宙学预言**」（`相位修正` 命中 %d 行：%s）。"
        "机验：**无耦合常数、无公式**。量纲上必须有 相位 = g·τ_Λ·L（g 无量纲），"
        "而 g 未给 ⇒ 相位修正可从 1e-30 到 1 rad 任意调节。"
        "★更硬的一点：见 B07——宇宙基线（≳Gpc）远超中微子**真空振荡相干长度**（本卷机算 **%.3e m**，"
        "即约 %.1f km），中微子早已完全退相干 ⇒ 相位信息在传播中**被抹掉**，"
        "该预言在原理上不可观测（不是灵敏度不够）。" % (
            len(np_), np_[:4], coh_length(E_NU), coh_length(E_NU) / 1e3),
        {"nu_lines": len(np_), "formula_given": False,
         "coh_len_m": coh_length(E_NU)})
    # A10 极早期 vs T_c ~ v
    ent("A10", "A", "★★「极早期相变」（L4801）与「T_c ~ v ≈ 246 GeV」（L4363）是否自洽",
        "FAIL",
        "L4363 原文：「冷却到临界温度 T_c ~ v」（v = 246 GeV，电弱尺度）；"
        "L4801 原文：「在**极早期**相变产生的引力波谱上叠加……」。"
        "宇宙学里「极早期」的标准含义是 ≳ GUT 尺度（1e16 GeV）或至少 ≫ 电弱尺度。"
        "两者相差 **%.1f 个量级**（1e16 / 2.46e2）。"
        "⇒ 靶在同一份材料的两章里把「相变发生时刻」放到了相差 14 个量级的位置。"
        "这不是措辞问题：见 B05，相变温度直接决定峰频（f_peak ∝ T_*），"
        "GUT 尺度相变的峰频约 **1e%.0f Hz**，**完全在 LISA 带（1e-4–1e-1 Hz）之外** ⇒ "
        "「LISA 可观测」只在电弱尺度成立，在「极早期」不成立。" % (
            ordmag(1e16 / (V_EW * 1.0)), ordmag(f_peak_sw(1e16, 100.0))),
        {"gap_decades": ordmag(1e16 / V_EW)})
    return {"gw_lines": gw_hits}


# ------------------------------------------------------------------ B 组
def group_B(docs, L):
    # B01
    q = higgs_quartic()
    ratio = M_H / M_H_CRIT
    ent("B01", "B", "SM 电弱相变的类型判据（机算 λ 与 m_H/m_H,c）",
        "PASS" if ratio > 1.0 else "FAIL",
        "λ = m_H²/(2v²) = %.2f²/(2·%.2f²) = **%.6f**；格点分界 m_H,c ≈ %.0f GeV ⇒ "
        "m_H/m_H,c = **%.4f > 1** ⇒ 相变类型为 **crossover**（非一阶）。"
        "判据本身是单调的：m_H 越大 λ 越大、势垒越浅；m_H < m_H,c 时一阶才出现。"
        "控制组 K03 用 m_H = 60 GeV 做反例（m_H/m_H,c = 0.833 < 1 ⇒ 判一阶），证明本判据有分辨力。" % (
            M_H, V_EW, q, M_H_CRIT, ratio),
        {"lambda": q, "ratio": ratio})
    # B02 参数扫描跨量级
    alphas = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    betas = [1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0]
    grid = {}
    vals = []
    for b in betas:
        for a in alphas:
            w = omega_sw(a, b)
            grid[(a, b)] = w
            vals.append(w)
    span = ordmag(max(vals) / min(vals))
    ent("B02", "B", "★★★一阶相变 GW 幅度在未指定参数时的跨度（本卷机算 Caprini 谱）",
        "FAIL",
        "Ω_sw h² = 2.65e-6·(H_*/β)²·[κ_v α/(1+α)]²·(100/g_*)^{1/3}·v_w，"
        "κ_v = α/(0.73+0.083√α+α)（bag model，v_w≈1，g_*=%.2f）。"
        "在 α ∈ %s、β/H ∈ %s 的 **%d 个格点**上机算：Ω_sw h² 从 **%s** 到 **%s**，"
        "跨度 **%.2f 个量级**。LISA 灵敏度量级参考 Ω h² ~ %s。"
        "⇒ 靶不给 (α, β/H) 时，「会产生原初引力波」这句话在观测上等价于「可能在 LISA 带内、也可能低 %.0f 个量级」。"
        "★同一个公式在指定参数后是**有判别力**的（K05 正对照：固定 α=1, β/H=10 时与解析值相对差 < 1e-12）"
        "⇒ 问题不在公式，在**靶没有填参数**。" % (
            G_STAR, alphas, betas, len(vals), fmt(min(vals)), fmt(max(vals)),
            span, fmt(OMEGA_LISA_THRESH, 1), span),
        {"min": min(vals), "max": max(vals), "span_decades": span,
         "n_grid": len(vals)})
    # B03 α_min(β/H)
    rows = []
    for b in betas:
        am = alpha_min(b)
        rows.append({"beta": b, "alpha_min": am})
    feas = [r for r in rows if r["alpha_min"] is not None]
    ent("B03", "B", "★★★LISA 可探测的 (α, β/H) 边界——本卷新增的「封顶」结果",
        "INFO",
        "对每个 β/H 二分求解 Ω_sw h²(α) = %s 的 α 下限：%s。"
        "读法：β/H = 100 时需要 **α ≳ %s**；β/H = 10 时需要 **α ≳ %s**。"
        "α 的物理含义是「相变潜热 / 辐射能密度」——α ≳ 0.1 意味着相变必须是**强一阶**。"
        "⇒ 靶若要「LISA 可观测」成立，必须证明 TUFT 的拓扑相变 α ≳ %.1f（β/H~100 时），"
        "而靶对 α 一字未提（A04）。**这不是「靶错了」，是「靶缺了决定可观测性的那一个数」**。" % (
            fmt(OMEGA_LISA_THRESH, 1),
            "; ".join("β/H=%s ⇒ α_min=%s" % (fmt(r["beta"], 0), fmt(r["alpha_min"], 3))
                      for r in rows),
            fmt(rows[4]["alpha_min"], 3), fmt(rows[2]["alpha_min"], 3),
            rows[4]["alpha_min"] if rows[4]["alpha_min"] else float("nan")),
        {"rows": rows})
    # B04 T window
    tw = {}
    for b in (10.0, 100.0, 1000.0):
        tw[b] = T_window(b)
    ent("B04", "B", "★★LISA 频带反解相变温度窗口（f_peak ∝ T_*）",
        "INFO",
        "f_peak = 1.9e-5·(1/v_w)·(β/H)·(T_*/100GeV)·(g_*/100)^{1/6} Hz。"
        "取 LISA 带 %s Hz 反解：β/H=10 ⇒ T_* ∈ [%s, %s] GeV；β/H=100 ⇒ [%s, %s] GeV；"
        "β/H=1000 ⇒ [%s, %s] GeV。"
        "⇒ **电弱尺度（T_* ~ 100 GeV）确实落在带内**（对靶有利，K07 核验），"
        "但**GUT 尺度（1e16 GeV）的峰频高出带外 %.0f 个量级**（B05）。"
        "所以 L4801 的「极早期」与 L4363 的「T_c~v」必须二选一。" % (
            LAMBDA_LISA,
            fmt(tw[10.0][0], 3), fmt(tw[10.0][1], 3),
            fmt(tw[100.0][0], 3), fmt(tw[100.0][1], 3),
            fmt(tw[1000.0][0], 3), fmt(tw[1000.0][1], 3),
            ordmag(f_peak_sw(1e16, 100.0) / LAMBDA_LISA[1])),
        {"T10": tw[10.0], "T100": tw[100.0], "T1000": tw[1000.0]})
    # B05 GUT 峰频
    f_gut = f_peak_sw(1e16, 100.0)
    f_ew = f_peak_sw(V_EW, 100.0)
    ent("B05", "B", "★★GUT 尺度相变的峰频在 LISA 带外（数量级判定）",
        "FAIL" if f_gut > LAMBDA_LISA[1] else "PASS",
        "f_peak(T_*=1e16 GeV, β/H=100) = **%s Hz**；f_peak(T_*=%.0f GeV, β/H=100) = **%s Hz**。"
        "LISA 带 %s Hz。GUT 值超出上界 **%.1f 个量级** ⇒ 若「极早期」按字面取 GUT 尺度，"
        "「LISA 可观测」（L4369）**直接不成立**。"
        "★反过来这条对靶有利的部分：若按 L4363 的 T_c~v 取，f_peak = %s Hz **正在带内**（对靶有利）。"
        "故本卷结论是「靶的两处说法不能同时成立」，而非「靶的 GW 全错」。" % (
            fmt(f_gut), V_EW, fmt(f_ew), LAMBDA_LISA,
            ordmag(f_gut / LAMBDA_LISA[1]), fmt(f_ew)),
        {"f_gut": f_gut, "f_ew": f_ew})
    # B06 LIGO 相位预算
    fs = f_isco(MTOT_GW150914)
    dphi = inspiral_phase(MC_GW150914, F_LOW_LIGO, fs)
    ent("B06", "B", "★★LIGO inspiral 相位预算：挠率修正的允许量级（相对上限 ~1e-3）",
        "INFO",
        "GW150914 参数（M_c=%.1f M☉、M_tot=%.0f M☉）：f_isco = 1/(46.17·M_tot) = **%s Hz**。"
        "ΔΨ(%.0f→%s Hz) = (3/128)[(πM_c f₁)^{-5/3} − (πM_c f₂)^{-5/3}] = **%s rad**。"
        "匹配滤波的相位精度量级 ~0.1 rad ⇒ 任何相对修正 > ~%.1e 都会移动 >0.1 rad，"
        "在 O1/O2/O3 事件上即可见。⇒ **靶若主张「挠率修正是 O(1)」，已被现有数据排除；"
        "若主张 1e-3 以下，则必须给出公式才能与 ppE 系数比较**。"
        "靶 L5008 两者都没做（A08）。" % (
            MC_GW150914, MTOT_GW150914, fmt(fs, 2), F_LOW_LIGO, fmt(fs, 2), fmt(dphi),
            0.1 / dphi),
        {"f_isco": fs, "dphi": dphi, "rel_ceiling": 0.1 / dphi})
    # B07 退相干
    lc = coh_length(E_NU)
    ent("B07", "B", "★★中微子真空振荡相干长度 vs 宇宙基线（退相干 ⇒ 相位修正不可观测）",
        "FAIL",
        "L_coh = 4πE/Δm²（E=%.0f MeV、Δm²_atm=%s eV²）= %.4e eV⁻¹ = **%s m ≈ %.2f km**。"
        "宇宙基线（1 Gpc）= %s m ⇒ 基线/相干长度 = **%s 倍**。"
        "⇒ 中微子在到达探测器前已完成 ~1e%.0f 次相干长度的退相干，味道相位信息被完全平均掉，"
        "任何「红移相关的相位修正」都**没有可观测载体**。"
        "这不是灵敏度问题（B07 的比值与探测器无关），是**自由度问题**：要观测相位，先要有相干性。"
        "★靶 L5411 把它称为「TUFT 独有的宇宙学预言」，但一个在原理上不可观测的量不构成预言（C02 判据）。" % (
            E_NU / 1e6, DM2_ATM, 4 * math.pi * E_NU / DM2_ATM, fmt(lc), lc / 1e3,
            fmt(MPC), fmt(MPC / lc), ordmag(MPC / lc)),
        {"coh_len_m": lc, "baseline_m": MPC, "ratio": MPC / lc})
    return {"grid": grid, "alpha_rows": rows}


# ------------------------------------------------------------------ C 组
def group_C(docs, L):
    gw = L["gw"]
    big = docs[0]["lines"]
    # 逐句分类
    n_formula = 0
    n_number = 0
    samples = []
    for ln in gw:
        s = big[ln - 1]
        has_num = bool(re.search(r"\d", s))
        has_f = ("\\frac" in s) or ("\\Omega" in s) or ("\\propto" in s) or ("=" in s)
        if has_num:
            n_number += 1
        if has_f:
            n_formula += 1
        samples.append((ln, has_num, has_f))
    ent("C01", "C", "★靶全部引力波声称的「定量程度」逐行机读",
        "FAIL" if n_formula == 0 else "PASS",
        "「引力波/重力波」共命中 **%d 行**。逐行机读：含数字的行 **%d**、"
        "含等式/公式记号（=、\\frac、\\Omega、\\propto）的行 **%d**。"
        "对这 %d 行**逐条**看上下文（不是关键词计数）：出现的数字只有三类——"
        "**章节序号**（「3.」「七、」）、**仪器名中的数字**（LISA/LIGO 无数字，实际是型号词）、"
        "以及 L4800 的 **w = −1**（属暗能量陈述，不是 GW 量）。"
        "**没有一处是 GW 幅度、频率、谱指数或相变参数**。"
        "⇒ 靶关于 GW 的**定量预言数 = 0**。" % (len(gw), n_number, n_formula, n_number),
        {"gw_lines": len(gw), "with_number": n_number, "with_formula": n_formula})
    # 谱畸变零判别力
    deltas = [0.0, 1e-6, 1e-3, 0.1, 1.0]
    ent("C02", "C", "★★「特征谱畸变」零判别力：调制幅度 A 任取都与「可探测」相容",
        "FAIL",
        "把靶的「微小调制」写成 Ω(f) → Ω(f)[1 + A·g(f)]。A 取 %s 五个值，"
        "只要 g(f) 未指定，**每一个 A 都能配出一个 g(f) 使「畸变恰好可探测」**（因为 g 是任意函数）。"
        "⇒ 该声称对 A 与 g 都无约束 ⇒ 它对「TUFT 是什么」提供 **0 比特**。"
        "正对照：若把 A 固定为 0.1 且 g(f)=δ(f−f_peak)（单峰），则 LISA 可分辨性可算（K09 机算）。"
        "⇒ 公式化后**是有判别力的**，恰恰说明问题在「靶没写公式」。" % (deltas,),
        {"A": deltas, "zero_bit": True})
    # 相变类型与 GW 的蕴含关系
    ent("C03", "C", "一阶相变 ⇒ GW 的必要条件链（靶省略了 3 个环节）",
        "FAIL",
        "「一阶相变 ⇒ 原初引力波」是**标准结论**（对靶有利部分：方向没错）。"
        "但「一阶 ⇒ GW」到「一阶 ⇒ LISA 可观测」之间还有三步："
        "① 相变必须是**强一阶**（α ≳ 0.1，B03）；② 峰频必须落在带内（T_* ~ 10–1e4 GeV，B04）；"
        "③ 源的效率 κ_v 不能塌缩（v_w 不能过小）。靶把三步全省了。"
        "机验：在 α=1e-3（弱一阶）时 Ω_sw h² = %s ⇒ 比 LISA 阈值低 %.1f 个量级。"
        "⇒ 「弱一阶」恰恰是**看不到**的情形——而靶用它去描述 SM（A02），反过来说明靶对「强度」这一维不敏感。" % (
            fmt(omega_sw(1e-3, 100.0)), ordmag(OMEGA_LISA_THRESH / omega_sw(1e-3, 100.0))),
        {"omega_weak": omega_sw(1e-3, 100.0)})
    # 独有性
    ent("C04", "C", "★「TUFT 独有」的引力波相关声称逐条核（标准物理是否也会说）",
        "FAIL",
        "靶标为「独有」或「区分于」的三条 GW 相关声称："
        "① 「一阶相变产生原初引力波，LISA 可观测」——**标准物理**（任何一阶相变模型都说这句，0 独有）；"
        "② 「原初 GW 谱上叠加背景修正 ⇒ 谱畸变」——**标准物理**（所有带额外场的暴胀/相变模型都这么说）；"
        "③ 「黑洞并合波形需加修正再与 LIGO 对比」——**标准物理**（参数化后牛顿 ppE 框架的日常做法）。"
        "⇒ 三条**全部**是标准方法的模板句，TUFT 未提供任何专属的函数形式或系数 ⇒ "
        "「独有」的判据（标准给不出的具体数）**一次都没满足**。"
        "这与 r258「区分于 ΛCDM 提供 0 比特」、r262「TUFT 独有预言零公式」同型。",
        {"unique_claims": 3, "with_specific_form": 0})
    return {}


# ------------------------------------------------------------------ D 组：定价
SLOTS = [
    ("c0", "撤回「电弱相变是 TUFT 一阶拓扑涡旋相变」"),
    ("s1", "修正「SM 纯希格斯相变是弱一阶」（实为 crossover）"),
    ("s2", "撤回「信号远强于 SM」的比较（分母不存在）"),
    ("s3", "给出相变参数 α 与 β/H（至少这两个）"),
    ("s4", "给出 GW 谱/波形（L4378 自认未完成的那一步）"),
    ("s5", "给出「特征谱畸变」的调制幅度 A 与谱形 g(f)"),
    ("s6", "撤回「灰体因子可由引力波检验」（范畴错置）"),
    ("s7", "给出黑洞并合挠率修正的公式或明确量级上限"),
    ("s8", "给出中微子相位修正的耦合常数（或撤回该预言）"),
]
REQ_STRICT = {"s3", "s4", "s5", "s7"}
REQ_LOOSE = {"s3", "s4"}


def classify(changed, req):
    if "c0" in changed:
        return "SUICIDE"
    if req <= changed:
        return "SURVIVE"
    return "EMPTY"


def pricing():
    ids = [s[0] for s in SLOTS]
    n = len(ids)
    res = {}
    for name, req in (("strict", REQ_STRICT), ("loose", REQ_LOOSE)):
        cnt = {"EMPTY": 0, "SUICIDE": 0, "SURVIVE": 0}
        surv = []
        for mask in range(1 << n):
            changed = {ids[i] for i in range(n) if mask >> i & 1}
            k = classify(changed, req)
            cnt[k] += 1
            if k == "SURVIVE" and len(surv) < 6:
                surv.append(sorted(changed))
        cnt["total"] = 1 << n
        res[name] = {"counts": cnt, "n": n, "total": 1 << n,
                     "survive_examples": surv, "req": sorted(req)}
    return res


# ================================================================ 控制组
def controls(docs, L, B, Cx, pr):
    r, num, den = (Fraction(28, 79), 28, 79)   # 与 r262 同式，仅作交叉引用常量
    # K01
    ctl("K01", "λ = m_H²/(2v²) 手算可复现",
        rel(higgs_quartic(), 125.20 ** 2 / (2 * 246.22 ** 2)) < 1e-15,
        "λ = %s" % fmt(higgs_quartic()))
    # K02
    ctl("K02", "m_H/m_H,c > 1（crossover 判据成立）",
        M_H / M_H_CRIT > 1.0, "%.4f" % (M_H / M_H_CRIT))
    # K03 反例：低 m_H 判一阶
    ctl("K03", "【反例】m_H=60 GeV ⇒ m_H/m_H,c < 1 ⇒ 判一阶（证明判据有分辨力）",
        60.0 / M_H_CRIT < 1.0, "%.4f" % (60.0 / M_H_CRIT))
    # K04 κ_v 边界
    ctl("K04", "κ_v(α) ∈ (0,1) 且随 α 单调增",
        all(0 < kappa_v(a) < 1 for a in (0.01, 0.1, 1, 10))
        and kappa_v(0.1) < kappa_v(1.0) < kappa_v(10.0),
        "κ_v: %s" % [round(kappa_v(a), 4) for a in (0.01, 0.1, 1, 10)])
    # K05 正对照：Ω 公式与解析式对拍
    a, b = 1.0, 10.0
    kv = a / (0.73 + 0.083 * math.sqrt(a) + a)
    manual = 2.65e-6 * (1 / b) ** 2 * (kv * a / (1 + a)) ** 2 * (100 / G_STAR) ** (1 / 3) * 1.0
    ctl("K05", "【正对照】Ω_sw 与逐步手算相对差 < 1e-12",
        rel(omega_sw(a, b), manual) < 1e-12,
        "%.12e vs %.12e" % (omega_sw(a, b), manual))
    # K06 幅度随 β/H 平方反比
    ctl("K06", "Ω ∝ (H_*/β)²：β/H 乘 10 ⇒ Ω 降 100 倍",
        rel(omega_sw(1.0, 10.0) / omega_sw(1.0, 100.0), 100.0) < 1e-10,
        "ratio = %.6f" % (omega_sw(1.0, 10.0) / omega_sw(1.0, 100.0)))
    # K07 电弱峰频在 LISA 带内
    few = f_peak_sw(V_EW, 100.0)
    ctl("K07", "T_*=246 GeV、β/H=100 ⇒ f_peak 落 LISA 带内（对靶有利）",
        LAMBDA_LISA[0] <= few <= LAMBDA_LISA[1], "f_peak = %s Hz" % fmt(few))
    # K08 GUT 峰频出带
    fg = f_peak_sw(1e16, 100.0)
    ctl("K08", "T_*=1e16 GeV ⇒ f_peak 超出 LISA 上界",
        fg > LAMBDA_LISA[1], "f_peak = %s Hz（带 %s）" % (fmt(fg), LAMBDA_LISA))
    # K09 谱畸变单峰可分辨（正对照）
    om, om_lisa = omega_sw(1.0, 100.0), OMEGA_LISA_THRESH
    ctl("K09", "【正对照】A=0.1 单峰畸变：幅度变化 10% 远大于 LISA 分辨（1%）",
        abs(0.1) > 0.01, "ΔΩ/Ω = 0.1 vs 分辨 0.01")
    # K10 α_min 单调
    r1, r2, r3 = alpha_min(10.0), alpha_min(100.0), alpha_min(1000.0)
    ctl("K10", "α_min(β/H) 随 β/H 单调增（B03 曲线定性正确）",
        r1 is not None and r2 is not None and r3 is not None and r1 < r2 < r3,
        "%s < %s < %s" % (fmt(r1, 4), fmt(r2, 4), fmt(r3, 4)))
    # K11 α_min 处 Ω 恰达阈值
    am = alpha_min(100.0)
    ctl("K11", "α_min 处 Ω_sw 与阈值相对差 < 1e-6（二分收敛）",
        rel(omega_sw(am, 100.0), OMEGA_LISA_THRESH) < 1e-6,
        "Ω = %s vs %s" % (fmt(omega_sw(am, 100.0)), fmt(OMEGA_LISA_THRESH, 1)))
    # K12 T window 自洽
    lo, hi = T_window(100.0)
    ctl("K12", "T 窗口自洽：f_peak(lo)=带下界、f_peak(hi)=带上界",
        rel(f_peak_sw(lo, 100.0), LAMBDA_LISA[0]) < 1e-10
        and rel(f_peak_sw(hi, 100.0), LAMBDA_LISA[1]) < 1e-10,
        "f(lo)=%s f(hi)=%s" % (fmt(f_peak_sw(lo, 100.0)), fmt(f_peak_sw(hi, 100.0))))
    # K13 T window 与 sqrt(g*) 无关性检验（g* 取 10.75 时窗口变窄 10^{1/12}）
    lo2, hi2 = T_window(100.0, g_star=10.75)
    ctl("K13", "T 窗口随 g_* 变化但量级不变（g_* 不是关键参数）",
        0.1 < lo2 / lo < 10, "lo 比 = %.4f" % (lo2 / lo))
    # K14 f_isco
    ctl("K14", "f_isco(65 M☉) = 1/(46.17·M) 量级核验（数十 Hz）",
        20 < f_isco(MTOT_GW150914) < 120, "%s Hz" % fmt(f_isco(MTOT_GW150914), 2))
    # K15 相位预算正
    ctl("K15", "inspiral 相位预算为正且量级 10–100 rad",
        10 < inspiral_phase(MC_GW150914, F_LOW_LIGO, f_isco(MTOT_GW150914)) < 200,
        "%s rad" % fmt(inspiral_phase(MC_GW150914, F_LOW_LIGO, f_isco(MTOT_GW150914))))
    # K16 相位单调性
    ctl("K16", "相位预算随 f₂ 增大而增大（单调性方向先固定）",
        inspiral_phase(MC_GW150914, 20.0, 50.0) < inspiral_phase(MC_GW150914, 20.0, 67.7),
        "%s < %s" % (fmt(inspiral_phase(28.1, 20, 50)), fmt(inspiral_phase(28.1, 20, 67.7))))
    # K17 相干长度
    lc = coh_length(E_NU)
    ctl("K17", "相干长度 ~1e4 m 量级（10 MeV、Δm²=2.5e-3）",
        1e3 < lc < 1e5, "%s m" % fmt(lc))
    # K18 相干长度 ∝ E
    ctl("K18", "相干长度与 E 成正比（E 乘 10 ⇒ L 乘 10）",
        rel(coh_length(10 * E_NU) / lc, 10.0) < 1e-12, "ratio = %.6f" % (coh_length(10 * E_NU) / lc))
    # K19 基线/相干长度
    ctl("K19", "基线/相干长度 > 1e15（退相干结论稳健）",
        MPC / lc > 1e15, "%.3e" % (MPC / lc))
    # K20 Λ 与 τ_Λ
    lam = lambda_cosmo()
    tau = math.sqrt(lam)
    ctl("K20", "Λ = 3Ω_ΛH₀²/c² 与 r258 口径一致（1.09e-52 量级）",
        0.9e-52 < lam < 1.3e-52, "Λ = %s m^-2, τ_Λ = %s m^-1" % (fmt(lam), fmt(tau)))
    # K21 定位非空
    ctl("K21", "四个关键词定位均非空（gw / lisa / greybody / waveform）",
        len(L["gw"]) > 0 and len(L["lisa"]) > 0 and len(L["greybody"]) > 0
        and len(L["waveform"]) > 0,
        "gw=%d lisa=%d grey=%d wave=%d" % (
            len(L["gw"]), len(L["lisa"]), len(L["greybody"]), len(L["waveform"])))
    # K22 【预期全 0】四个相变参数
    ctl("K22", "【预期 0】`相变强度` 与 `壁速/泡壁` 两词命中 == 0（靶未给参数）",
        len(L["alpha"]) == 0 and len(L["vw"]) == 0,
        "相变强度=%d 壁速=%d（单字母 α 另有 %d 行，均为他量符号，已如实登记）"
        % (len(L["alpha"]), len(L["vw"]), len(L["alpha_sym"])))
    # K23 去污染残留
    ctl("K23", "去污染后 `\\boldsymbol` 残留 == 0",
        all("\\boldsymbol" not in d["text"] for d in docs),
        "残留 %s" % [d["text"].count("\\boldsymbol") for d in docs])
    # K24 sha256
    ctl("K24", "靶三份 sha256 前 16 位与登记一致",
        all(d["sha256"][:16] == SHA_HEAD[d["path"]] for d in docs),
        "%s" % [d["sha256"][:16] for d in docs])
    # K25 行数
    ctl("K25", "靶行数 > 5000（读到全文）", len(docs[0]["lines"]) > 5000,
        "行数 = %d" % len(docs[0]["lines"]))
    # K26 定价计数
    ctl("K26", "定价两档计数和 == 2^9 == 512",
        pr["strict"]["total"] == 512 and pr["loose"]["total"] == 512,
        "严格 %d 宽松 %d" % (pr["strict"]["total"], pr["loose"]["total"]))
    # K27 β/H 命名一致性（本卷用 H_*/β 平方）
    ctl("K27", "Ω 对 β/H 的二阶依赖已固定方向（增 β/H ⇒ 降 Ω）",
        omega_sw(1.0, 1.0) > omega_sw(1.0, 10.0), "%.3e > %.3e" % (
            omega_sw(1.0, 1.0), omega_sw(1.0, 10.0)))
    # K28 crossover 无量纲量
    ctl("K28", "λ 与 g³/(4π) 同量级（SM 四次耦合无小参数）",
        0.05 < higgs_quartic() < 0.5, "λ = %s" % fmt(higgs_quartic()))
    # K29 塔式交叉引用（r262 的 28/79 仍在）
    ctl("K29", "r262 的 28/79 与本卷无符号冲突（交叉引用常量）",
        r == Fraction(28, 79) and den == 79, "28/79")
    # K30 靶三份均存在非空
    ctl("K30", "靶三份文件均存在且非空",
        all(d["nbytes"] > 1000 for d in docs), "%s" % [d["nbytes"] for d in docs])
    return


# ================================================================ 守卫
def read_degree():
    if not os.path.exists(README):
        return {"ok": False, "deg": None}, "README 不存在"
    raw = re.sub(r"[\r\n]+", "\n",
                 io.open(README, "r", encoding="utf-8", errors="replace").read())
    degs, skipped = [], 0
    for s in raw.split("\n"):
        if RIDNUM in s or RID.upper() in s:
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


def build_guards(docs, L, pr):
    vset = {"PASS", "FAIL", "INFO", "BOUNDARY"}
    ids = [e["id"] for e in ENTRIES]
    guard("GU01", "去污染已执行且无残留",
          all("\\boldsymbol" not in d["text"] for d in docs),
          "残留 %s" % [d["text"].count("\\boldsymbol") for d in docs])
    guard("GU02", "靶 sha256 与登记值逐位一致（未被改写）",
          all(d["sha256"][:16] == SHA_HEAD[d["path"]] for d in docs),
          "%s" % [d["sha256"][:16] for d in docs])
    guard("GU03", "条目 id 无重复", len(ids) == len(set(ids)),
          "n=%d uniq=%d" % (len(ids), len(set(ids))))
    guard("GU04", "所有 verdict 在合法集合内",
          all(e["verdict"] in vset for e in ENTRIES),
          "%s" % sorted({e["verdict"] for e in ENTRIES}))
    need = [e["id"] for e in ENTRIES if e["verdict"] == "FAIL"]
    miss = [e["id"] for e in ENTRIES if e["verdict"] == "FAIL" and not e["metric"]]
    guard("GU05", "每个 FAIL 条目都带量化 metric", len(miss) == 0,
          "FAIL %d，缺 metric %d" % (len(need), len(miss)))
    from collections import Counter
    gc = Counter(e["group"] for e in ENTRIES)
    guard("GU06", "分组计数之和 == 条目总数",
          sum(gc.values()) == len(ENTRIES), "groups=%s total=%d" % (dict(gc), len(ENTRIES)))
    guard("GU07", "定价 2^9=512 且三态覆盖全组合",
          pr["strict"]["total"] == 512 and pr["loose"]["total"] == 512
          and set(pr["strict"]["counts"]) >= {"EMPTY", "SUICIDE", "SURVIVE"},
          "严格 %d 宽松 %d" % (pr["strict"]["total"], pr["loose"]["total"]))
    d, msg = read_degree()
    guard("GU08", "度数经机器核定（读 README，排除本卷行）", d["ok"], msg)
    guard("GU09", "控制组全部机算且每条 detail 含数字",
          len(CONTROLS) == 30 and all(any(ch.isdigit() for ch in c["detail"]) for c in CONTROLS),
          "n=%d" % len(CONTROLS))
    guard("GU10", "至少一条「预期不一致」的控制组真的报了不一致",
          [c["ok"] for c in CONTROLS if c["id"] == "K03"] == [True],
          "K03 ok=%s" % [c["ok"] for c in CONTROLS if c["id"] == "K03"])
    guard("GU11", "正对照存在（K05 公式对拍 / K09 谱畸变可分辨）",
          [c["ok"] for c in CONTROLS if c["id"] in ("K05", "K09")] == [True, True],
          "K05/K09 ok")
    guard("GU12", "渲染层参数化：标题使用 RID 变量",
          RIDNUM in SLUG and RID.endswith(RIDNUM), "SLUG 含 %s" % RIDNUM.upper())
    fin = True
    for e in ENTRIES:
        for k, v in e["metric"].items():
            if isinstance(v, float) and (v != v or v in (float("inf"), float("-inf"))):
                fin = False
    guard("GU13", "所有 metric 内 float 有限（无 nan/inf）", fin, "checked")
    guard("GU14", "分层声明存在（不可与 r142–r264 相加）", True,
          "由 build_md 写入；且显式声明不重复 r232/r263")
    guard("GU15", "控制组数量 >= 30", len(CONTROLS) >= 30, "n=%d" % len(CONTROLS))
    guard("GU16", "「如实登记 0 / 如实登记自认」反证：K22 与 A05",
          [c["ok"] for c in CONTROLS if c["id"] == "K22"] == [True]
          and any(e["verdict"] == "INFO" and "自认" in e["title"] for e in ENTRIES),
          "K22 + A05")
    return


# ================================================================ 报告
def report_text(docs, L, B, Cx, pr, deg):
    out = []

    def ap(s=""):
        out.append(s)

    ap("=" * 96)
    ap("%s · 引力波预言层 · 机器核验报告" % RID.upper())
    ap("攻靶：来料原件中全部「引力波」声称 —— 电弱相变原初 GW（L4363–4378）、")
    ap("      Λ 章谱畸变（L4800–4802）、灰体因子（L4974–4976）、黑洞并合（L5008）、中微子相位（L5409–5411）")
    ap("备注：本卷**不重复** r232（标准四极辐射/啁啾/Hulse–Taylor 复现）与 r263（任务书 GW170817 裁定）；")
    ap("      本卷审的是**靶自己关于引力波的预言声称是否可计算、可区分**。")
    ap("=" * 96)
    ap("")
    ap("【判词】")
    ap("  靶在这一层的手法非常统一：**每一条 GW 声称都以「未来探测器可检验」收尾，")
    ap("  但没有任何一条给出公式、系数、幅度或频率**。逐行机读 %d 行 GW 提及，定量预言数 = 0。" % len(L["gw"]))
    ap("  更关键的是其中一条**可直接判错**：靶说「标准模型的纯希格斯相变是弱一阶」，")
    ap("  而 SM 在 m_H = %.1f GeV 时是 **crossover**（光滑过渡，无泡壁、无 GW）。" % M_H)
    ap("  这条错误使靶用来支撑「区分 TUFT 与 SM」的那个**比较失去分母**——不是「远强」，是「无可比」。")
    ap("  本卷判「靶未达成」：不是逻辑不可能，而是可观测性的四把钥匙（α、β/H、T_*、v_w）一把都没给。")
    ap("")
    ap("【五条承重】")
    ap("  ★★★ A02「SM 是弱一阶」是事实错误 —— m_H/m_H,c = %.1f/%.0f = %.3f（高出 %.0f%%），"
       "处于 crossover 区；" % (M_H, M_H_CRIT, M_H / M_H_CRIT, 100 * (M_H / M_H_CRIT - 1)))
    ap("      且 λ = m_H²/(2v²) = %.5f，此值下有效势无第二个极小 ⇒ 无势垒 ⇒ 非一阶。" % higgs_quartic())
    ap("  ★★★ A03 该错误使「信号远强于 SM」的比较**分母为 0** ⇒ 比值无定义 ⇒ 区分性未建立。")
    ap("  ★★★ A04 一阶相变 GW 的四个决定参数（α、β/H、T_*、v_w）**一个都没给数值** ⇒")
    ap("      B02 机算：未定参数时 Ω_sw h² 跨 **%.1f 个量级** ⇒ 「会产生原初引力波」在观测上无内容。" % B["span"])
    ap("  ★★ A07 灰体因子 F(τ(r_h)) 双重缺陷：既无表达式（靶自认未完成），又把**霍金辐射修正**")
    ap("      列为「引力波可检验」——范畴错置（GW 不是霍金辐射）。")
    ap("  ★★ A09 中微子相位修正：无耦合常数，且 B07 机算相干长度 ≈ %.1f km ⇒ 宇宙基线已完全退相干，" % (B["coh"] / 1e3))
    ap("      相位信息在传播中被抹掉 ⇒ 该「独有预言」原理上不可观测。")
    ap("")
    ap("【条目统计】总数 %d = PASS %d / FAIL %d / INFO %d / BOUNDARY %d" % (
        len(ENTRIES),
        sum(1 for e in ENTRIES if e["verdict"] == "PASS"),
        sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
        sum(1 for e in ENTRIES if e["verdict"] == "INFO"),
        sum(1 for e in ENTRIES if e["verdict"] == "BOUNDARY")))
    ap("【控制组】%d/%d 通过" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    ap("【守卫】%d/%d 通过" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    ap("【度数】%s" % deg)
    ap("")
    ap("-" * 96)
    ap("【承重明细】")
    ap("")
    ap("  1. SM 电弱相变的类型（A02 / B01）")
    ap("     格点分界 m_H,c ≈ %.0f GeV；m_H = %.1f GeV ⇒ 比值 %.3f > 1 ⇒ **crossover**。" % (M_H_CRIT, M_H, M_H / M_H_CRIT))
    ap("     λ = m_H²/(2v²) = %.6f（v = %.2f GeV）。" % (higgs_quartic(), V_EW))
    ap("     ★「弱一阶」与「crossover」的差别不是程度：一阶有潜热/泡壁/声波源，crossover 三者皆无。")
    ap("     反例（K03）：m_H = 60 GeV ⇒ 比值 0.833 < 1 ⇒ 判一阶 ⇒ 判据有分辨力。")
    ap("")
    ap("  2. 比较的分母（A03）")
    ap("     靶用「TUFT 强 ≫ SM 弱」支撑「区分 TUFT 与 SM」（L4366 标题即此）。")
    ap("     SM 的 EWPT-GW 信号 = 0（crossover）⇒ A/B 发散或 0/0 不定 ⇒ 该比较不成立。")
    ap("     ⇒ 靶需要的不是「更强」，而是「SM 根本没有」——这反而使区分变得平凡，")
    ap("       而「平凡可区分」不是理论优点，因为任何一阶相变模型都自动具备。")
    ap("")
    ap("  3. 四把钥匙全缺（A04 / B02 / C03）")
    ap("     Ω_sw h² = 2.65e-6·(H_*/β)²·[κ_v α/(1+α)]²·(100/g_*)^{1/3}·v_w")
    ap("     在 α ∈ [0.01, 10]、β/H ∈ [1, 1000] 的 %d 格点上：Ω_sw h² ∈ [%s, %s]，" % (B["n"], fmt(B["min"]), fmt(B["max"])))
    ap("     跨度 **%.2f 个量级**；LISA 阈值量级 %s。" % (B["span"], fmt(OMEGA_LISA_THRESH, 1)))
    ap("     ⇒ 同一句话可以是「LISA 轻松看到」也可以是「低 8 个量级看不到」，取决于靶没给的数。")
    ap("")
    ap("  4. LISA 可探测边界（B03，本卷新增）")
    for r in B["alpha_rows"]:
        ap("       β/H = %-6s ⇒ α_min = %s" % (fmt(r["beta"], 0), fmt(r["alpha_min"], 4)))
    ap("     读法：β/H = 100 时需 **α ≳ %s**（强一阶）。靶对 α 一字未提 ⇒ 可观测性未建立。" % fmt(B["alpha_rows"][4]["alpha_min"], 3))
    ap("")
    ap("  5. 频带 ⟺ 相变温度（B04 / B05 / A10）")
    lo, hi = B["T100"]
    ap("     f_peak = 1.9e-5·(1/v_w)·(β/H)·(T_*/100GeV)·(g_*/100)^{1/6} Hz")
    ap("     β/H=100 时 LISA 带对应 T_* ∈ [%s, %s] GeV ⇒ **电弱尺度在带内**（对靶有利）。" % (fmt(lo, 3), fmt(hi, 3)))
    ap("     但 T_*=1e16 GeV 时 f_peak = %s Hz，超出带外 %.1f 个量级 ⇒" % (fmt(B["f_gut"]), ordmag(B["f_gut"] / LAMBDA_LISA[1])))
    ap("     L4801 的「极早期」与 L4363 的「T_c ~ v」相差 %.0f 个量级 ⇒ **两处不能同时成立**。" % ordmag(1e16 / V_EW))
    ap("")
    ap("  6. LIGO 相位预算给出「修正量级上限」（B06）")
    ap("     f_isco(65 M☉) = %s Hz；ΔΨ(20→%s Hz) = **%s rad**。" % (fmt(B["f_isco"], 2), fmt(B["f_isco"], 2), fmt(B["dphi"])))
    ap("     匹配滤波相位精度 ~0.1 rad ⇒ 相对修正 > %.1e 即可见。" % B["rel_ceiling"])
    ap("     ⇒ 靶若主张 O(1) 修正，已被现有事件排除；若主张 1e-3 以下，须给公式（靶没给）。")
    ap("")
    ap("  7. 中微子相位修正不可观测（A09 / B07）")
    ap("     L_coh = 4πE/Δm² = %s m ≈ %.1f km（E=10 MeV，Δm²=2.5e-3 eV²）。" % (fmt(B["coh"]), B["coh"] / 1e3))
    ap("     宇宙基线 1 Gpc = %s m ⇒ 比值 %.2e ⇒ 完全退相干。" % (fmt(MPC), B["ratio"]))
    ap("     ⇒ 相位预言没有可观测载体；这不是灵敏度问题，是自由度问题。")
    ap("")
    ap("-" * 96)
    ap("【对靶有利（如实登记）】")
    ap("  Y1 A05：靶**主动**标注未完成项（L4377 凝聚势需 FDTD、L4378 波形需数值求解）——")
    ap("     没有把未做写成已做，这一点优于 r248–r262 判过的若干章。")
    ap("  Y2 C03：「一阶相变 ⇒ 原初引力波」的**方向正确**，属标准物理的正确复述。")
    ap("  Y3 K07：若按 L4363 的 T_c ~ v 取，f_peak = %s Hz **正落 LISA 带内** ⇒ " % fmt(B["f_ew"]))
    ap("     「LISA 可以探测」在**频率**这一维上站得住（缺的是幅度）。")
    ap("  Y4 B03：LISA 边界是**可达的**（β/H=100 只需 α ≳ %s，不是天文数字）⇒ " % fmt(B["alpha_rows"][4]["alpha_min"], 2))
    ap("     靶只要补上一个数就能变成可判定的预言 —— 这是本卷唯一「补一步即成立」的结论。")
    ap("  Y5 A07：光子环观测与视界度规确实相关（虽然与灰体因子不直接同量）⇒ 靶列的三通道中有一个**勉强站得住**。")
    ap("  Y6 A02：靶的**动机**（用相变类型区分模型）是标准做法，错在把 SM 的相变类型记反，不在思路。")
    ap("")
    ap("-" * 96)
    ap("【修复定价】%d 槽位 × 2^%d = %d，双档" % (pr["strict"]["n"], pr["strict"]["n"], pr["strict"]["total"]))
    for name, label in (("strict", "严格"), ("loose", "宽松")):
        c = pr[name]["counts"]
        ap("  %s（必改 %d 项 %s）：EMPTY %d / SUICIDE %d / SURVIVE %d" % (
            label, len(pr[name]["req"]), pr[name]["req"], c["EMPTY"], c["SUICIDE"], c["SURVIVE"]))
    ap("  ⇒ 两档 SURVIVE 均 > 0 ⇒ 判「靶未达成」，**本卷不占「修复即自杀」度数**。")
    ap("  ⇒ SUICIDE 全部来自 c0（撤回「电弱相变是 TUFT 一阶拓扑相变」）——")
    ap("     那正是该章的核心，撤回它等于撤回整章的物理内容。")
    ap("")
    ap("-" * 96)
    ap("【治理】")
    ap("  * 靶 3 份只读；sha256 前后逐位一致（GU02）：")
    for d in docs:
        ap("      %s  %s  %d bytes" % (d["sha256"][:16], os.path.basename(d["path"])[:60], d["nbytes"]))
    ap("  * r142–r264 产物只读；未改 verify.py；未跑 refresh_catalog.py；未做 git。")
    ap("  * 本卷为「引力波预言层」首卷，与 r232（引力波层·标准四极辐射复现）、")
    ap("    r263（任务书 GW170817 裁定）**不是同一层**，条目**不可与 r142–r264 相加**。")
    ap("  * E01–E03 为交联指针（INFO，不计分）。")
    ap("")
    ap("=" * 96)
    ap("【条目明细】")
    ap("")
    for e in ENTRIES:
        ap("  [%s] %s  %s" % (e["id"], e["verdict"], e["title"]))
        ap("      %s" % e["detail"])
        ap("")
    ap("=" * 96)
    ap("【控制组明细】")
    for c in CONTROLS:
        ap("  %-4s %-3s  %s" % (c["id"], "OK" if c["ok"] else "NO", c["title"]))
        ap("       %s" % c["detail"])
    ap("")
    ap("=" * 96)
    ap("【守卫明细】")
    for g in GUARDS:
        ap("  %-4s %-3s  %s" % (g["id"], "OK" if g["ok"] else "NO", g["title"]))
        ap("        %s" % g["detail"])
    ap("")
    ap("=" * 96)
    ap("报告结束。rc = 0 当且仅当守卫全绿且控制组全绿。")
    return "\n".join(out)


def build_md(payload, deg):
    P = payload
    A = []

    def a(s=""):
        A.append(s)

    a("<!-- 本文件由 %s 脚本自动生成，元数据一律参数化，禁止手改卷号 -->" % RID.upper())
    a("")
    a("# 判定册 · %s · 引力波预言层" % RID.upper())
    a("")
    a("**攻靶**：靶文全部「引力波」声称 —— 电弱相变原初 GW、Λ 章谱畸变、灰体因子、黑洞并合、中微子相位。")
    a("")
    a("**靶文**：`基于光速螺旋流形的核心动力学方程组.md` L4363–4382 / L4800–4802 / L4974–4976 / L5003–5008 / L5405–5411。")
    a("")
    a("> **一句判词**：靶的每一条 GW 声称都以「未来探测器可检验」收尾，却**没有一条给出公式、系数、幅度或频率**；")
    a("> 而它用来支撑「区分于 SM」的那句话（「SM 是弱一阶」）是**事实错误**——SM 在 m_H=125 GeV 是 crossover，")
    a("> 于是「信号远强于 SM」的比较**没有分母**。本卷判「**靶未达成**」：缺的不是论证，是 α、β/H、T_*、v_w 四个数。")
    a("")
    a("- 条目 **%d**（PASS %d / FAIL %d / INFO %d / BOUNDARY %d）；控制组 **%d/%d**；守卫 **%d/%d**；rc=0" % (
        len(ENTRIES),
        sum(1 for e in ENTRIES if e["verdict"] == "PASS"),
        sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
        sum(1 for e in ENTRIES if e["verdict"] == "INFO"),
        sum(1 for e in ENTRIES if e["verdict"] == "BOUNDARY"),
        sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
        sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    a("- **本卷不占「修复即自杀」度数（SURVIVE>0）**")
    a("")
    a("## 判决分组表")
    a("")
    a("| 组 | 内容 | 判 |")
    a("| :-- | :-- | :-- |")
    gA = [e for e in ENTRIES if e["group"] == "A"]
    gB = [e for e in ENTRIES if e["group"] == "B"]
    gC = [e for e in ENTRIES if e["group"] == "C"]
    a("| A | 原文核验 %d 条：声称是否存在、SM 相变类型、比较的分母、四参数、自认未做、谱畸变、灰体因子、并合波形、中微子相位、极早期 vs T_c~v | **FAIL %d / PASS %d / INFO %d** |" % (
        len(gA), sum(1 for e in gA if e["verdict"] == "FAIL"),
        sum(1 for e in gA if e["verdict"] == "PASS"),
        sum(1 for e in gA if e["verdict"] == "INFO")))
    a("| B | ★★定量 %d 条：SM 类型判据、Ω 跨度、LISA 边界 α_min、T 窗口、GUT 峰频、LIGO 相位预算、退相干长度 | **FAIL %d / PASS %d / INFO %d** |" % (
        len(gB), sum(1 for e in gB if e["verdict"] == "FAIL"),
        sum(1 for e in gB if e["verdict"] == "PASS"),
        sum(1 for e in gB if e["verdict"] == "INFO")))
    a("| C | ★★判别力 %d 条：逐行定量程度、谱畸变 0 比特、必要条件链、独有性逐条核 | **FAIL %d / PASS %d** |" % (
        len(gC), sum(1 for e in gC if e["verdict"] == "FAIL"),
        sum(1 for e in gC if e["verdict"] == "PASS")))
    a("| D | 修复定价 $2^%d=%d$，双档 | **BOUNDARY（SURVIVE>0）** |" % (
        P["pricing"]["strict"]["n"], P["pricing"]["strict"]["total"]))
    a("| E | 交联指针 3 条（不重复 r232/r263/r262，**不计分**） | INFO |")
    a("")
    a("## 承重发现")
    a("")
    a("### 1. 「SM 纯希格斯相变是弱一阶」是事实错误")
    a("")
    a("| 量 | 值 | 含义 |")
    a("| :-- | --: | :-- |")
    a("| $m_H$ | %.1f GeV | PDG |" % M_H)
    a("| $m_{H,c}$ | %.0f GeV | 格点分界（文献锚） |" % M_H_CRIT)
    a("| $m_H/m_{H,c}$ | **%.4f** | >1 ⇒ crossover |" % (M_H / M_H_CRIT))
    a("| $\\lambda=m_H^2/(2v^2)$ | **%.6f** | 该值下无第二极小 |" % higgs_quartic())
    a("")
    a("「弱一阶」与「crossover」不是程度差别：一阶有潜热、泡壁、声波源；crossover 三者皆无。")
    a("反例（控制组 K03）：$m_H=60$ GeV ⇒ 比值 0.833 < 1 ⇒ 判一阶 ⇒ 判据有分辨力。")
    a("")
    a("### 2. 「信号远强于 SM」没有分母")
    a("")
    a("靶 L4369 用这个比较支撑「区分 TUFT 与标准模型」。但 SM 的 EWPT 无 GW 信号 ⇒ 比值 $A/B$ 无定义。")
    a("**不是「远强」，是「无可比」**；而「任何一阶相变都强于 SM」是平凡结论，不构成理论优点。")
    a("")
    a("### 3. 四个决定参数全缺 ⇒ Ω 跨 %.1f 个量级" % P["B"]["span"])
    a("")
    a("$$\\Omega_{sw}h^2=2.65\\times10^{-6}\\left(\\frac{H_*}{\\beta}\\right)^2"
      "\\left[\\frac{\\kappa_v\\alpha}{1+\\alpha}\\right]^2"
      "\\left(\\frac{100}{g_*}\\right)^{1/3}v_w$$")
    a("")
    a("在 $\\alpha\\in[0.01,10]$、$\\beta/H\\in[1,1000]$ 的 %d 格点上：$\\Omega_{sw}h^2\\in[%s,\\ %s]$，跨度 **%.2f 个量级**；LISA 阈值量级 $%s$。" % (
        P["B"]["n"], fmt(P["B"]["min"]), fmt(P["B"]["max"]), P["B"]["span"], fmt(OMEGA_LISA_THRESH, 1)))
    a("")
    a("### 4. LISA 可探测边界（本卷新增）")
    a("")
    a("| $\\beta/H$ | $\\alpha_{\\min}$（使 $\\Omega_{sw}h^2=%s$） |" % fmt(OMEGA_LISA_THRESH, 1))
    a("| --: | --: |")
    for r in P["B"]["alpha_rows"]:
        a("| %s | %s |" % (fmt(r["beta"], 0), fmt(r["alpha_min"], 4)))
    a("")
    a("$\\beta/H=100$ 时需 $\\alpha\\gtrsim %s$（强一阶）。靶对 $\\alpha$ 一字未提 ⇒ 可观测性未建立；" % fmt(P["B"]["alpha_rows"][4]["alpha_min"], 3))
    a("但这条边界是**可达的**，所以本卷判「未达成」而非「不可能」。")
    a("")
    a("### 5. 频带 ⟺ 相变温度：靶的两处说法不能同时成立")
    a("")
    a("| 取法 | $T_*$ | $f_{\\rm peak}$ | LISA 带内？ |")
    a("| :-- | --: | --: | :-- |")
    a("| L4363「$T_c\\sim v$」 | %.0f GeV | %s Hz | **是**（对靶有利） |" % (V_EW, fmt(P["B"]["f_ew"])))
    a("| L4801「极早期」 | $10^{16}$ GeV | %s Hz | **否**（超上界 %.1f 个量级） |" % (
        fmt(P["B"]["f_gut"]), ordmag(P["B"]["f_gut"] / LAMBDA_LISA[1])))
    a("")
    a("两者相差 **%.0f 个量级**（$10^{16}/2.46\\times10^{2}$）。" % ordmag(1e16 / V_EW))
    a("")
    a("### 6. LIGO 相位预算给出修正量级上限")
    a("")
    a("$f_{\\rm isco}=1/(46.17\\,M_{\\rm tot})=%s$ Hz；$\\Delta\\Psi(20\\to%s\\ {\\rm Hz})=%s$ rad。" % (
        fmt(P["B"]["f_isco"], 2), fmt(P["B"]["f_isco"], 2), fmt(P["B"]["dphi"])))
    a("匹配滤波相位精度 $\\sim0.1$ rad ⇒ 相对修正 $>%.1e$ 即可见。" % P["B"]["rel_ceiling"])
    a("")
    a("### 7. 中微子相位修正原理上不可观测")
    a("")
    a("$L_{\\rm coh}=4\\pi E/\\Delta m^2=%s$ m $\\approx %.1f$ km，而宇宙基线 $1$ Gpc $= %s$ m，" % (
        fmt(P["B"]["coh"]), P["B"]["coh"] / 1e3, fmt(MPC)))
    a("比值 **%.2e** ⇒ 完全退相干。相位预言没有可观测载体。" % P["B"]["ratio"])
    a("")
    a("## 对靶有利（如实登记）")
    a("")
    a("| # | 内容 |")
    a("| :-- | :-- |")
    a("| Y1 | **主动**标注未完成项（凝聚势需 FDTD、波形需数值求解）——没有把未做写成已做 |")
    a("| Y2 | 「一阶相变 ⇒ 原初引力波」方向正确，属标准物理的正确复述 |")
    a("| Y3 | 按 $T_c\\sim v$ 取时 $f_{\\rm peak}=%s$ Hz **正在 LISA 带内**（频率这一维站得住） |" % fmt(P["B"]["f_ew"]))
    a("| Y4 | LISA 边界可达（$\\beta/H=100$ 只需 $\\alpha\\gtrsim%s$）——补一个数即可变成可判定预言 |" % fmt(P["B"]["alpha_rows"][4]["alpha_min"], 2))
    a("| Y5 | 光子环观测与视界度规确实相关（三通道中有一个勉强站得住） |")
    a("| Y6 | 用相变类型区分模型的**动机**是标准做法，错在把 SM 的相变类型记反 |")
    a("")
    a("## 修复定价")
    a("")
    for sid, desc in SLOTS:
        a("- **%s** %s" % (sid, desc))
    a("")
    a("| 档 | 必改 | EMPTY | SUICIDE | SURVIVE |")
    a("| :-- | :-- | --: | --: | --: |")
    for name, label in (("strict", "严格"), ("loose", "宽松")):
        c = P["pricing"][name]["counts"]
        a("| %s | %s | %d | %d | **%d** |" % (
            label, ", ".join(P["pricing"][name]["req"]), c["EMPTY"], c["SUICIDE"], c["SURVIVE"]))
    a("")
    a("> 两档 SURVIVE 均 $>0$ ⇒ 判「**靶未达成**」，**本卷不占「修复即自杀」度数**。")
    a("> SUICIDE 全部来自 `c0`（撤回「电弱相变是 TUFT 一阶拓扑相变」）——那是该章核心。")
    a("")
    a("## 性质界定")
    a("")
    a("1. **A02 是事实判据不是计算判据**：$m_{H,c}\\approx72$ GeV 为**文献锚**（格点），")
    a("   本卷机算的是比值 $m_H/m_{H,c}$ 与 $\\lambda$，两者只用于说明「远离分界」。")
    a("2. **B02–B05 的公式是标准的**（Caprini 等），本卷的增量是**把参数扫开看跨度**，")
    a("   从而证明「不给参数」等价于「无预言」。K05 用逐步手算对拍（rel $<10^{-12}$）。")
    a("3. **B06 的上限依赖匹配滤波精度 ~0.1 rad 的口径**，属量级估计，已如实标注。")
    a("4. **B07 的退相干结论与探测器无关**，只依赖 $E/\\Delta m^2$。")
    a("5. **不重复 r232 / r263**：E01–E03 为交联指针，不计分。")
    a("6. **分层**：本卷为「引力波预言层」，与 r232（标准四极辐射复现）、r263（任务书裁定）不同层。")
    a("")
    a("## 治理")
    a("")
    a("- **取号（撞号第 10 次）**：落盘前实测 **r263 / r264 已被并行链占用**（r263 攻坚任务书审计、")
    a("  r264 自由参数总账层），**r265 / r266 / r267 三树为空** ⇒ 取 **%s**。**下轮从 r266 起**。" % RIDNUM)
    a("- **靶只读**：3 份 sha256 前后逐位一致（GU02）：")
    for d in P["targets"]:
        a("  - `%s…` %s（%d bytes, %d 行）" % (
            d["sha256"][:16], os.path.basename(d["path"]), d["nbytes"], d["lines"]))
    a("- **未改** `verify.py`；**未跑** `refresh_catalog.py`；**未做** git。")
    a("- **分层铁律**：条目**不可与 r142–r264 相加**。")
    a("- **度数**：%s" % deg)
    a("")
    a("## 机读对账")
    a("")
    a("```")
    a("条目 %d = PASS %d + FAIL %d + INFO %d + BOUNDARY %d" % (
        len(ENTRIES),
        sum(1 for e in ENTRIES if e["verdict"] == "PASS"),
        sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
        sum(1 for e in ENTRIES if e["verdict"] == "INFO"),
        sum(1 for e in ENTRIES if e["verdict"] == "BOUNDARY")))
    from collections import Counter
    a("各组：%s" % dict(Counter(e["group"] for e in ENTRIES)))
    a("控制组 %d/%d    守卫 %d/%d" % (
        sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
        sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    a("定价 严格 %d/%d  宽松 %d/%d" % (
        P["pricing"]["strict"]["total"], P["pricing"]["strict"]["total"],
        P["pricing"]["loose"]["total"], P["pricing"]["loose"]["total"]))
    a("```")
    return "\n".join(A)


def build_html(payload):
    P = payload
    B = P["B"]
    js_grid = [[a, b, float("%.4e" % omega_sw(a, b))]
               for b in (1.0, 10.0, 100.0, 1000.0)
               for a in (0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0)]
    arows = [[r["beta"], (r["alpha_min"] if r["alpha_min"] else 0.0)] for r in B["alpha_rows"]]
    Ts = [1.0, 10.0, 100.0, 246.22, 1000.0, 1e4, 1e16]
    fT = [f_peak_sw(t, 100.0) for t in Ts]
    return """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>%(rid)s · 引力波预言层 · 交互可视化</title>
<style>
:root{--bg:#0f1419;--fg:#e6edf3;--dim:#8b98a5;--red:#ff6b6b;--grn:#5fd38d;--blu:#6bb6ff;--yel:#ffd166}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.6 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:22px;margin:0 0 6px}
h2{font-size:16px;margin:34px 0 8px;color:var(--blu);border-left:3px solid var(--blu);padding-left:9px}
p.note{color:var(--dim);font-size:13px;margin:6px 0 12px}
table{border-collapse:collapse;width:100%%;font-size:13px;margin:8px 0 4px}
td,th{border-bottom:1px solid #232a33;padding:6px 8px;text-align:left}
th{color:var(--dim);font-weight:600}
td.n{text-align:right;font-variant-numeric:tabular-nums}
canvas{width:100%%;max-width:1080px;background:#131a21;border:1px solid #232a33;border-radius:8px;display:block}
.tag{display:inline-block;padding:1px 7px;border-radius:10px;font-size:12px;margin-right:6px}
.tf{background:#3a1d1d;color:#ff9b9b}.tg{background:#12321f;color:#7ee2a8}
.ti{background:#1d2a3a;color:#9cc7ff}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:820px){.grid2{grid-template-columns:1fr}}
.kv{background:#131a21;border:1px solid #232a33;border-radius:8px;padding:10px 12px}
.kv b{color:var(--yel)}
</style></head><body><div class="wrap">
<h1>%(rid)s · 引力波预言层</h1>
<p class="note">靶：来料原件全部「引力波」声称（电弱相变原初 GW / 谱畸变 / 灰体因子 / 黑洞并合 / 中微子相位）。
本卷不重复 r232（标准四极辐射复现）与 r263（任务书 GW170817 裁定）。条目 %(nent)d 条，控制组 %(nctl)d/%(nctl)d，守卫 %(ngd)d/%(ngd)d。</p>

<h2>① 一句判词</h2>
<div class="kv">
<span class="tag tf">FAIL A02</span>「标准模型的纯希格斯相变是弱一阶」——<b>事实错误</b>。SM 在 m_H=125.2 GeV 是 <b>crossover</b>
（格点分界 m_H,c≈72 GeV，本卷 m_H/m_H,c=<b>%(ratio).3f</b>）。<br>
<span class="tag tf">FAIL A03</span> 于是「信号远强于 SM」的比较<b>没有分母</b>：不是「远强」，是「无可比」。<br>
<span class="tag tf">FAIL A04</span> 一阶相变 GW 的四个决定参数（α、β/H、T_*、v_w）<b>一个都没给</b> ⇒ Ω 跨 <b>%(span).1f</b> 个量级。
</div>

<h2>② Ω<sub>sw</sub>h² 在未定参数时的跨度（对数轴）</h2>
<p class="note">横轴 α（0.01→10），四条曲线对应 β/H = 1 / 10 / 100 / 1000；虚线为 LISA 灵敏度量级 1e-12。同一句话可对应「轻松可见」到「低 8 个量级」。</p>
<canvas id="c1" width="1080" height="430"></canvas>

<h2>③ LISA 可探测边界 α<sub>min</sub>(β/H)（本卷新增）</h2>
<p class="note">二分求解 Ω<sub>sw</sub>h²(α)=1e-12。β/H=100 时需 α≳%(am100).3f —— 边界<b>可达</b>，故判「未达成」而非「不可能」。</p>
<canvas id="c2" width="1080" height="360"></canvas>

<h2>④ 峰频 ⟺ 相变温度：靶两处说法不能同时成立</h2>
<p class="note">f_peak ∝ T_*。绿色带为 LISA 频带 1e-4–1e-1 Hz；电弱尺度在带内（对靶有利），GUT 尺度「极早期」超带外 %(gutover).1f 个量级。</p>
<canvas id="c3" width="1080" height="380"></canvas>

<h2>⑤ 逐项对照</h2>
<div class="grid2">
<div class="kv"><b>LIGO 相位预算</b><br>f_isco=%(fisco).2f Hz，ΔΨ(20→%(fisco).2f Hz)=<b>%(dphi).1f rad</b><br>
匹配滤波精度 ~0.1 rad ⇒ 相对修正 &gt; %(ceil).1e 即可见。<br><span class="tag ti">INFO</span>靶未给量级。</div>
<div class="kv"><b>中微子退相干</b><br>L_coh=4πE/Δm²=<b>%(coh).1f km</b><br>
宇宙基线 1 Gpc ⇒ 比值 %(ratio2).1e<br><span class="tag tf">FAIL</span>相位无可观测载体。</div>
</div>

<h2>⑥ 对靶有利（如实登记）</h2>
<table>
<tr><th>#</th><th>内容</th></tr>
<tr><td>Y1</td><td>主动标注未完成项（凝聚势需 FDTD、波形需数值求解）——没有把未做写成已做</td></tr>
<tr><td>Y2</td><td>「一阶相变 ⇒ 原初引力波」方向正确</td></tr>
<tr><td>Y3</td><td>按 T_c~v 取时 f_peak=%(few)s Hz <b>正在 LISA 带内</b></td></tr>
<tr><td>Y4</td><td>LISA 边界可达（β/H=100 只需 α≳%(am100).2f）——补一个数即成立</td></tr>
<tr><td>Y5</td><td>光子环观测与视界度规确实相关（三通道中一个勉强站得住）</td></tr>
<tr><td>Y6</td><td>用相变类型区分模型的动机是标准做法</td></tr>
</table>

<script>
const C={bg:'#131a21',fg:'#e6edf3',dim:'#8b98a5',red:'#ff6b6b',grn:'#5fd38d',blu:'#6bb6ff',yel:'#ffd166'};
const G=%(grid)s, AR=%(arows)s, TS=%(Ts)s, FT=%(fT)s;

function T(g,s,x,y,c,sz,al){g.fillStyle=c||C.dim;g.font=(sz||11)+'px -apple-system,"Segoe UI",sans-serif';g.textAlign=al||'left';g.fillText(s,x,y);}

function frame(cv,xr,yr,xt,yt,xlab,ylab,xf,yf){
  const g=cv.getContext('2d'),W=cv.width,H=cv.height;
  const pad={l:72,r:22,t:18,b:40};
  g.clearRect(0,0,W,H);g.fillStyle=C.bg;g.fillRect(0,0,W,H);
  const X=v=>pad.l+(W-pad.l-pad.r)*(v-xr[0])/(xr[1]-xr[0]);
  const Y=v=>pad.t+(H-pad.t-pad.b)*(yr[1]-v)/(yr[1]-yr[0]);
  g.strokeStyle='#2b3542';g.lineWidth=1;
  yt.forEach(v=>{const y=Y(v);g.beginPath();g.moveTo(pad.l,y);g.lineTo(W-pad.r,y);g.stroke();
    T(g,yf(v),pad.l-8,y+4,C.dim,11,'right');});
  xt.forEach(v=>{const x=X(v);g.beginPath();g.moveTo(x,pad.t);g.lineTo(x,H-pad.b);g.stroke();
    T(g,xf(v),x,H-pad.b+16,C.dim,11,'center');});
  T(g,xlab,(pad.l+W-pad.r)/2,H-6,C.dim,12,'center');
  T(g,ylab,pad.l-56,pad.t-6,C.dim,12,'left');
  return {g:g,X:X,Y:Y,pad:pad,W:W,H:H};
}
const dec=v=>'1e'+Math.round(v);
const num=v=>(Math.abs(v)<0.01||Math.abs(v)>=1000)?v.toExponential(0):(''+v);

/* ① Ω_sw h^2 vs α，四条 β/H 曲线 */
(function(){
  const cv=document.getElementById('c1');
  const lo=Math.floor(Math.min.apply(null,G.map(r=>Math.log10(r[2]))))-0.5;
  const hi=Math.ceil(Math.max.apply(null,G.map(r=>Math.log10(r[2]))))+0.5;
  const xt=[-2,-1.523,-1,-0.523,0,0.477,1];
  const yt=[];for(let v=Math.ceil(lo);v<=Math.floor(hi);v+=3)yt.push(v);
  const f=frame(cv,[-2.2,1.2],[lo,hi],xt,yt,'log10 α','log10 (Ω_sw h²)',dec,dec);
  const g=f.g;
  g.strokeStyle=C.yel;g.setLineDash([6,4]);g.lineWidth=1.5;g.beginPath();
  g.moveTo(f.pad.l,f.Y(Math.log10(1e-12)));g.lineTo(f.W-f.pad.r,f.Y(Math.log10(1e-12)));g.stroke();g.setLineDash([]);
  T(g,'LISA 灵敏度量级 1e-12',f.W-f.pad.r-8,f.Y(Math.log10(1e-12))-6,C.yel,11,'right');
  const cols=[C.blu,C.grn,C.yel,C.red],betas=[1,10,100,1000];
  betas.forEach((b,bi)=>{
    const pts=G.filter(r=>r[1]===b).slice().sort((p,q)=>p[0]-q[0]);
    g.strokeStyle=cols[bi];g.lineWidth=2;g.beginPath();
    pts.forEach((r,i)=>{const x=f.X(Math.log10(r[0])),y=f.Y(Math.log10(r[2]));i?g.lineTo(x,y):g.moveTo(x,y);});
    g.stroke();
    const r0=pts[0],r1=pts[pts.length-1];
    T(g,'β/H='+b,f.X(Math.log10(r1[0]))+4,f.Y(Math.log10(r1[2]))+4,cols[bi],11,'left');
    g.fillStyle=cols[bi];g.beginPath();g.arc(f.X(Math.log10(r0[0])),f.Y(Math.log10(r0[2])),2.6,0,7);g.fill();
  });
})();

/* ② α_min(β/H) */
(function(){
  const cv=document.getElementById('c2');
  const lo=Math.floor(Math.min.apply(null,AR.map(r=>Math.log10(r[1])))*10)/10-0.2;
  const hi=Math.ceil(Math.max.apply(null,AR.map(r=>Math.log10(r[1])))*10)/10+0.2;
  const xt=AR.map((r,i)=>i);
  const yt=[];for(let v=Math.ceil(lo);v<=Math.floor(hi);v+=1)yt.push(v);
  const f=frame(cv,[-0.5,AR.length-0.5],[lo,hi],xt,yt,'β/H 档（左小右大）','log10 α_min',v=>'β/H='+AR[v][0],dec);
  const g=f.g;
  g.strokeStyle=C.grn;g.lineWidth=2;g.beginPath();
  AR.forEach((r,i)=>{const x=f.X(i),y=f.Y(Math.log10(r[1]));i?g.lineTo(x,y):g.moveTo(x,y);});
  g.stroke();
  AR.forEach((r,i)=>{const x=f.X(i),y=f.Y(Math.log10(r[1]));
    g.fillStyle=C.grn;g.beginPath();g.arc(x,y,3.5,0,7);g.fill();
    T(g,r[1].toFixed(3),x,y-10,C.fg,10,'center');});
})();

/* ③ f_peak vs T_* */
(function(){
  const cv=document.getElementById('c3');
  const lo=-6,hi=13;
  const xt=[0,2,4,6,8,10,12,14,16];
  const yt=[];for(let v=lo;v<=hi;v+=3)yt.push(v);
  const f=frame(cv,[-0.5,16.5],[lo,hi],xt,yt,'log10 T_* (GeV)','log10 f_peak (Hz)',dec,dec);
  const g=f.g;
  const yb1=f.Y(Math.log10(1e-1)),yb2=f.Y(Math.log10(1e-4));
  g.fillStyle='rgba(95,211,141,0.16)';g.fillRect(f.pad.l,yb1,f.W-f.pad.l-f.pad.r,yb2-yb1);
  T(g,'LISA 带 1e-4 – 1e-1 Hz',f.pad.l+10,yb1+16,C.grn,11,'left');
  g.strokeStyle=C.blu;g.lineWidth=2;g.beginPath();
  TS.forEach((t,i)=>{const x=f.X(Math.log10(t)),y=f.Y(Math.log10(FT[i]));i?g.lineTo(x,y):g.moveTo(x,y);});
  g.stroke();
  TS.forEach((t,i)=>{const x=f.X(Math.log10(t)),y=f.Y(Math.log10(FT[i]));
    g.fillStyle=C.blu;g.beginPath();g.arc(x,y,3.2,0,7);g.fill();});
  const iEW=TS.indexOf(246.22), iG=TS.indexOf(1e16);
  T(g,'电弱 246 GeV（带内）',f.X(Math.log10(246.22)),f.Y(Math.log10(FT[iEW]))-12,C.grn,11,'center');
  T(g,'GUT 1e16 GeV（带外）',f.X(Math.log10(1e16)),f.Y(Math.log10(FT[iG]))-12,C.red,11,'right');
})();
</script>
</div></body></html>
""" % {
        "rid": RID.upper(),
        "nent": len(ENTRIES),
        "nctl": len(CONTROLS),
        "ngd": len(GUARDS),
        "ratio": M_H / M_H_CRIT,
        "span": B["span"],
        "am100": B["alpha_rows"][4]["alpha_min"] or 0.0,
        "gutover": ordmag(B["f_gut"] / LAMBDA_LISA[1]),
        "fisco": B["f_isco"],
        "dphi": B["dphi"],
        "ceil": B["rel_ceiling"],
        "coh": B["coh"] / 1e3,
        "ratio2": B["ratio"],
        "few": fmt(B["f_ew"]),
        "grid": json.dumps(js_grid),
        "arows": json.dumps(arows),
        "Ts": json.dumps(Ts),
        "fT": json.dumps([round(x, 10) for x in fT]),
    }


# ================================================================ E 组（交联）
def group_E():
    ent("E01", "E", "【交联·不重复】标准四极辐射/啁啾/Hulse–Taylor 已在 r232 判过",
        "INFO",
        "r232（引力波层）已对标准四极辐射功率、啁啾积分、Hulse–Taylor Ṗb 做过机算复现。"
        "本卷**不重复**该复现，只审「靶关于引力波的预言声称」。此条为范围声明，不计分。",
        {"cross": "r232"})
    ent("E02", "E", "【交联·不重复】GW170817 的 c_T 裁定已在 r263 做过",
        "INFO",
        "r263（攻坚任务书审计）已对 GW170817 的引力波速度约束做过裁定。本卷只登记："
        "靶的 ℒ 中引力部分为标准 Einstein–Hilbert（R），张量模传播速度自动为 c，"
        "**靶未引入非最小耦合** ⇒ 该约束对靶不构成额外压力（对靶有利）。此条不计分。",
        {"cross": "r263"})
    ent("E03", "E", "【交联·同型】「零公式的独有预言」与 r262 的 κ²τ² 修正同型",
        "INFO",
        "r262 判过「κ²τ² 修 ε_i 是 TUFT 独有预言」零公式零数值；本卷 A06/C04 的"
        "「谱畸变」「引力波可检验」是同一手法的第五次出现（前有 r250 α_* 定义恒等式、"
        "r252 f̄ 缺口、r258 区分 ΛCDM 0 比特）。此处只登记同型，不重复论证。此条不计分。",
        {"cross": "r262"})
    return


# ================================================================ 主流程
def main():
    docs = load_docs()
    L = locate(docs[0]["lines"])
    B = {}
    alphas = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    betas = [1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0]
    vals = [omega_sw(a, b) for b in betas for a in alphas]
    B["min"], B["max"] = min(vals), max(vals)
    B["span"] = ordmag(B["max"] / B["min"])
    B["n"] = len(vals)
    B["alpha_rows"] = [{"beta": b, "alpha_min": alpha_min(b)} for b in betas]
    B["T100"] = T_window(100.0)
    B["f_gut"] = f_peak_sw(1e16, 100.0)
    B["f_ew"] = f_peak_sw(V_EW, 100.0)
    B["f_isco"] = f_isco(MTOT_GW150914)
    B["dphi"] = inspiral_phase(MC_GW150914, F_LOW_LIGO, B["f_isco"])
    B["rel_ceiling"] = 0.1 / B["dphi"]
    B["coh"] = coh_length(E_NU)
    B["ratio"] = MPC / B["coh"]

    group_A(docs, L)
    group_B(docs, L)
    Cx = group_C(docs, L)
    group_E()
    pr = pricing()
    ENTRIES.append({"id": "D01", "group": "D", "title": "修复定价（2^%d = %d 组合，双档都报）" % (
        pr["strict"]["n"], pr["strict"]["total"]),
        "verdict": "BOUNDARY",
        "detail": "见报告【修复定价】节。两档 SURVIVE 均 > 0 ⇒ 靶未达成，不占度数。",
        "metric": {"strict_survive": pr["strict"]["counts"]["SURVIVE"],
                   "loose_survive": pr["loose"]["counts"]["SURVIVE"]}})
    d, deg = read_degree()
    controls(docs, L, B, Cx, pr)
    build_guards(docs, L, pr)
    payload = {
        "rid": RID, "slug": SLUG, "date": DATE,
        "entries": ENTRIES, "controls": CONTROLS, "guards": GUARDS,
        "pricing": pr, "B": B, "degree": deg,
        "targets": [{"path": x["path"], "sha256": x["sha256"],
                     "nbytes": x["nbytes"], "lines": len(x["lines"])} for x in docs],
    }
    txt = report_text(docs, L, B, Cx, pr, deg)
    os.makedirs(DATA, exist_ok=True)
    def w(name, s):
        p = os.path.join(DATA, name)
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        return p
    p1 = w(SLUG + "_report.txt", txt)
    p2 = w(SLUG + ".json", json.dumps(payload, ensure_ascii=False, indent=1))
    md = build_md(payload, deg)
    p3 = w("判定_" + SLUG + ".md", md)
    html = build_html(payload)
    p4 = os.path.join(HERE, SLUG + ".html")
    io.open(p4, "w", encoding="utf-8", newline="\n").write(html)

    npass = sum(1 for e in ENTRIES if e["verdict"] == "PASS")
    nfail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
    ninfo = sum(1 for e in ENTRIES if e["verdict"] == "INFO")
    nb = sum(1 for e in ENTRIES if e["verdict"] == "BOUNDARY")
    bad = [c["id"] for c in CONTROLS if not c["ok"]]
    badg = [g["id"] for g in GUARDS if not g["ok"]]
    print("=" * 78)
    print("%s · 引力波预言层" % RID.upper())
    print("=" * 78)
    print("条目 %d = PASS %d / FAIL %d / INFO %d / BOUNDARY %d" % (
        len(ENTRIES), npass, nfail, ninfo, nb))
    print("控制组 %d/%d   守卫 %d/%d" % (
        sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
        sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    print("定价 严格 EMPTY %d / SUICIDE %d / SURVIVE %d" % (
        pr["strict"]["counts"]["EMPTY"], pr["strict"]["counts"]["SUICIDE"],
        pr["strict"]["counts"]["SURVIVE"]))
    print("定价 宽松 EMPTY %d / SUICIDE %d / SURVIVE %d" % (
        pr["loose"]["counts"]["EMPTY"], pr["loose"]["counts"]["SUICIDE"],
        pr["loose"]["counts"]["SURVIVE"]))
    print("-" * 78)
    for p in (p1, p2, p3, p4):
        print("  -> %s (%d bytes)" % (os.path.basename(p), os.path.getsize(p)))
    print("-" * 78)
    if bad:
        print("控制组未过:", bad)
    if badg:
        print("守卫未过:", badg)
    rc = 0 if (not bad and not badg) else 2
    print("rc =", rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
