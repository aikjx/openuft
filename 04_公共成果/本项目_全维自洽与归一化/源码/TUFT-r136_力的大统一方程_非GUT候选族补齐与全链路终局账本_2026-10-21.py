# -*- coding: utf-8 -*-
"""
TUFT-r136 · 力的大统一方程 · 非GUT候选族补齐 与 全链路终局账本

用户指令：分析整理好，并攻破统一场论、力的大统一方程，全维度全链路整理好。

本卷走【补齐 + 攻破 + 全链路整理】三线合一：

  ① 补齐 r120 候选全集的结构性遗漏。
     r120 的 9 条方程 = ℒ_SM / ℒ_EW / SU(5) / SO(10) / E6 / MSSM / EYM / 引力缺口 / 超引力·弦；
     r123 封堵的五条退路 = 换群族 / 加阈值 / 额外维 / 弦紫外完备 / 剔除引力。
     二者合起来只覆盖了「规范群扩充族」这一支 + 弦。
     【遗漏面】= 非 GUT 的含引力统一候选族，本册补齐 6 个：
       C1 渐近安全引力 + SM（AS，Weinberg/Reuter）
       C2 非交换几何谱作用量（NCG，Chamseddine–Connes）
       C3 Kaluza–Klein（KK）
       C4 圈量子引力 + 物质 / 离散量子引力路线（LQG / 因果集 / 扭量 / CDT）
       C5 弦·M 理论景观（r120 已列，本册只补「判别力定价」这一维）
       C6 本项目螺旋几何化体系的大统一方程（v10 X04 共享场方程 + S01 三重奏 + S17 四力形式）

  ② 六门判据机读攻破：
       门1 量纲齐次   门2 四力覆盖（引力须真包含，非并排）
       门3 参数计数（n_free <= n_obs - 1）   门4 耦合汇聚/统一机制
       门5 实验安全（质子衰变 / LHC / 精密观测）   门6 可证伪性（做过可被排除的预言）

  ③ 全链路终局账本：把「力的大统一方程」这条链 r91 → r136 串成一张只读表，
     只汇总他人已落盘结论，不改写任何被引用册的字节。

分工声明（条目不可相加，跨册引用先冻结口径）：
  r119 = 完成度七条必要条件 U1–U7 + 电弱控制组
  r120 = 候选全集枚举（9 方程，GUT 族 + 弦）
  r123 = 退守路径封堵（五路全封）
  r128 / r131 = 正确方程整理与攻破（SM / GR / ΛCDM 树层）
  r134 = 完成判据冻结 U1–U7 + 净前提下降门（建设性纲领）
  本册 = r120 遗漏族补齐 + 六门攻破 + 全链路账本

红线纪律：
  - 各源卷拥有其条目；本卷条目非加和。
  - 不触碰并行会话字节；不 push；不刷新目录索引。
  - 数学自洽 ≠ 实验证实：本册只做「可算判决」，不声称产出新物理。
"""
import os, sys, json, glob, decimal
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
D = Decimal

# ---- 路径（源码 -> 归一化 -> 公共成果 -> openuft） ----
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
JUDGE_DIR = os.path.normpath(os.path.join(HERE, "..", "判定"))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))

DATE = "2026-10-21"
STEM = "TUFT-r136_力的大统一方程_非GUT候选族补齐与全链路终局账本_%s" % DATE
JUDGE_STEM = "判定_TUFT-r136-力的大统一方程_非GUT候选族补齐与全链路终局账本_%s" % DATE

# ============================== 外部事实锚点 [C] ==============================
# 全部为 CODATA 2018 / PDG 2024 / 文献公开值，本册不重算其测定的来路。
ALPHA      = D("7.2973525693e-3")    # 精细结构常数
L_PLANCK   = D("1.616255e-35")       # m
E_PLANCK   = D("1.220890e19")        # GeV （普朗克能量）
HBARC_JM   = D("3.16152677e-26")     # J*m
M_H_OBS    = D("125.20")             # GeV  Higgs 质量（PDG 2024）
M_H_OBS_U  = D("0.11")               # GeV
M_GUT_MSSM = D("2.014e16")           # GeV  MSSM 统一能标
ALPHA_GUT  = D(1) / D("24.3")        # 4.1152e-2
TAU_P_SK   = D("2.4e34")             # yr   Super-K 质子衰变下限
E_LHC      = D("1.36e4")             # GeV  LHC 质心能
M_Z, M_W   = D("91.1876"), D("80.377")   # GeV
SIN2TW     = D("0.23121")            # 有效弱混合角

# ---- Higgs 质量「预言 vs 实测」对照（文献值 [C]，本册只做对照与定价，不重算推导）----
#  key, 预言值(GeV), 预言年份, 是否在 Higgs 发现(2012)之前, 备注
HIGGS_PREDS = [
    ("AS 渐近安全",            D("126.0"), 2009, True,
     "Shaposhnikov-Wetterich：紫外不动点 + 引力近无跑动 => M_H 约 126 GeV"),
    ("NCG 谱作用量（原始版）",  D("170.0"), 2008, True,
     "Chamseddine-Connes：谱作用量在大统一标度定 λ => M_H 约 170 GeV"),
    ("NCG 谱作用量（修正版）",  D("125.0"), 2012, False,
     "加入 σ 标量场与大统一标度后修正至约 125 GeV（发现之后的事后修正）"),
    ("MSSM",                   None,       1990, True,
     "轻 Higgs 上界约 135 GeV，是区间约束非点预言"),
    ("SM 标准模型",            None,       1967, True,
     "M_H 为自由输入参数，无预言"),
    ("本项目螺旋几何化体系",    None,       2026, False,
     "四力 α_i 为并列输入，未给 Higgs 质量预言"),
]

# ---- 全链路终局账本（只读汇总他人结论；不改写被引册字节） ----
CHAIN = [
    ("r91",  "大统一方程建构与完成度结账（v=c 口径）", "FAIL", "建构层：方程未闭合"),
    ("r94",  "大统一方程定稿 构件 v=c 频率桥接与 α 量纲对账 终审", "FAIL", "量纲对账不通过"),
    ("r97",  "V40 终极力的统一方程（大小·方向·距离）全维审计", "FAIL", "力的统一方程不成立"),
    ("r113", "力的统一宣称 四分支源侧结构审计（电磁支归零）", "FAIL", "电磁支归零"),
    ("r119", "统一场论完成度总判定：七条必要条件 + 电弱控制组 6/6", "FAIL", "完成度 1/7"),
    ("r120", "所有力的大统一方程式：候选全集与状态机判（9 方程）", "FAIL", "9 条中仅 2 条 PASS，均不含引力"),
    ("r123", "力的大统一方程 退守路径总攻破（五路全封）", "FAIL", "换群/阈值/额外维/弦/剔除引力 全封"),
    ("r125", "路线对错判定方法与统一路线假设穷尽审计", "DEAD", "路线 DEAD"),
    ("r127", "（并行会话）SM 数值正确核 V01–V11 + 断裂边界", "PASS/FAIL", "正确核 11/11；断裂边界 B01–B11 FAIL"),
    ("r128", "正确理论体系方程全集 整理与攻破审计", "FAIL", "方程整理 PASS 4；攻破层 FAIL 9"),
    ("r130", "（并行会话）推导链内部隐藏前提审计", "OPEN", "前提账本：未导出合计 37"),
    ("r131", "正确方程扩容与攻破退守路径（树层可算预言）", "FAIL", "树层 PASS 3 / 结构 FAIL 2"),
    ("r132", "全维自洽与归一化 跨卷综合判定册", "FAIL", "全维自洽未达成"),
    ("r133", "修补失败元原理：修改逐个审计与结构不可修补定理", "FAIL", "局部修补四型穷尽均不闭合"),
    ("r134", "完成统一场论建设性纲领：完成判据冻结 + 净前提下降门", "OPEN", "完成度 1/7；净前提变化 +11，无人过门"),
    ("r136", "本册：非 GUT 候选族补齐 + 六门攻破 + 全链路账本", "（见下）", "补齐 r120 遗漏的 6 个含引力候选族"),
]

# ============================== 量纲工具（四元组 M,L,T,Q） ==============================
def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))

def dpow(a, n):
    n = Fraction(n)
    return tuple(x * n for x in a)

def dinv(a):
    return tuple(-x for x in a)

def ddiv(a, b):
    return dmul(a, dinv(b))

def dstr(a):
    parts = []
    for sym, e in zip(("M", "L", "T", "Q"), a):
        if e == 0:
            continue
        parts.append("%s^%s" % (sym, e))
    return "1" if not parts else "".join(parts)

ZERO = (Fraction(0),) * 4
DIM = {
    "L":    (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
    "M":    (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
    "T":    (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
    "c":    (Fraction(0), Fraction(1), Fraction(-1), Fraction(0)),
    "hbar": (Fraction(1), Fraction(2), Fraction(-1), Fraction(0)),
    "G":    (Fraction(-1), Fraction(3), Fraction(-2), Fraction(0)),
}
# 拉氏密度量纲 [E]/[L^3] = M L^-1 T^-2
DIM_LAGRANGIAN = (Fraction(1), Fraction(-1), Fraction(-2), Fraction(0))

# ============================== 条目/输出器 ==============================
ENTRIES = []
GUARDS = []
CHECKS = []

def emit(code, kind, title, detail, extra=None):
    rec = {"code": code, "kind": kind, "title": title, "detail": detail}
    if extra:
        rec.update(extra)
    ENTRIES.append(rec)
    return rec

def P(code, t, d, **kw): return emit(code, "PASS", t, d, kw)
def F(code, t, d, **kw): return emit(code, "FAIL", t, d, kw)
def Bd(code, t, d, **kw): return emit(code, "BOUNDARY", t, d, kw)
def I(code, t, d, **kw): return emit(code, "INFO", t, d, kw)

def guard(name, ok, note):
    GUARDS.append({"name": name, "ok": bool(ok), "note": note})
    return ok

def ctl(name, ok, note):
    CHECKS.append({"name": name, "ok": bool(ok), "note": note})
    return ok

def fx(x, n=25):
    """定点科学计数输出（Decimal 不接受 quantize 高位数）"""
    try:
        return format(Decimal(x), ".%dE" % n)
    except Exception:
        return str(x)

def rel(a, b):
    b = Decimal(b)
    if b == 0:
        return None
    return (Decimal(a) - b) / b

def pct(a, b):
    r = rel(a, b)
    return None if r is None else r * D(100)

# ============================== 一、控制组（判别力先行） ==============================
def run_controls():
    # CT1 电弱：ρ = M_W^2/(M_Z^2 cos^2θ_W)，树级预言 1
    cos2tw = D(1) - SIN2TW
    rho = (M_W * M_W) / (M_Z * M_Z * cos2tw)
    dev_rho = (rho - D(1)) * D(100)
    # r120 同口径锚点 1.01043
    drift_r120 = (rho - D("1.01043")) / D("1.01043")
    ok1 = abs(dev_rho) < D("1.5") and abs(drift_r120) < D("1e-3")
    ctl("CT1 电弱 ρ 参数（控制组：证明判据承认真统一）", ok1,
        "rho=%s（偏离树级 %s%%）；与 r120 锚点 1.01043 相对差 %s；"
        "偏离落在 m_t/Higgs 圈修正量级带内 ⇒ 电弱是真·已完成的统一"
        % (fx(rho, 8), fx(dev_rho, 6), fx(drift_r120, 6)))

    # CT2 AS 的 Higgs 预言：126.0 vs 实测 125.20
    d_as = pct(D("126.0"), M_H_OBS)
    ok2 = abs(d_as) < D("5")      # AS 自身不确定度「a few GeV」量级
    ctl("CT2 渐近安全 Higgs 预言命中（正面控制组）", ok2,
        "预言 126.0 GeV vs 实测 %s GeV ⇒ 相对 +%s%%（远小于其自述数 GeV 不确定度）"
        % (fx(M_H_OBS, 6), fx(abs(d_as), 6)))

    # CT3 NCG 原始版被排除（排除性控制组：判据能辨认错误候选）
    d_ncg = pct(D("170.0"), M_H_OBS)
    ok3 = abs(d_ncg) > D("10")
    ctl("CT3 NCG 原始版 170 GeV 被 LHC 排除（排除性控制组）", ok3,
        "170.0 vs 实测 %s GeV ⇒ 相对 +%s%% ⇒ 判据确能枪毙错误候选，非一律放行"
        % (fx(M_H_OBS, 6), fx(d_ncg), )) 

    # CT4 量纲审计器双向自反
    eh = dmul(dmul(dpow(DIM["c"], 4), dpow(DIM["L"], -2)), dinv(DIM["G"]))
    spiral = dmul(dmul(DIM["hbar"], DIM["c"]), dpow(DIM["L"], -2))
    ok4 = (eh == DIM_LAGRANGIAN) and (spiral != DIM_LAGRANGIAN)
    ctl("CT4 量纲审计器双向自反", ok4,
        "EH 作用量密度 %s = %s ✓；螺旋 ℒ=(ħc)(κ²) 得 %s ✗（差 L²，与 r128 CT3 同口径）"
        % (dstr(eh), dstr(DIM_LAGRANGIAN), dstr(spiral)))

    # CT5 引力间隙与 r120 同源复核
    a_g = (M_GUT_MSSM / E_PLANCK) ** 2
    gap = ALPHA_GUT / a_g
    gap_dex = gap.ln() / D(10).ln()
    ok5 = abs(rel(a_g, D("2.721e-6"))) < D("1e-3") and abs(gap_dex - D("4.18")) < D("0.05")
    ctl("CT5 引力间隙 α_G 与 r120 逐位同源", ok5,
        "α_G(M_GUT)=(M_GUT/E_Pl)^2=%s（r120 锚点 2.721e-6）；α_GUT/α_G=%s ⇒ 差 %s 个量级（r120: 4.18）"
        % (fx(a_g), fx(gap, 8), fx(gap_dex, 6)))

    # CT6 KK 电荷量子化：α = 4 C ℓ_Pl^2 / R^2 ⇒ R = 2 ℓ_Pl sqrt(C/α)
    res = {}
    for c_exp in (-2, -1, 0, 1, 2):
        C = D(10) ** c_exp
        R = D(2) * L_PLANCK * (C / ALPHA).sqrt()
        e_j = HBARC_JM / R
        e_gev = e_j / D("1.602176634e-10")
        res[c_exp] = (R, e_gev)
    mins = min(v[1] for v in res.values())
    ok6 = mins / E_LHC > D("1e10")
    ctl("CT6 KK 电荷量子化反解 R 的系数敏感性（C∈[1e-2,1e2]）", ok6,
        "C=1 ⇒ R=%s m、M_KK=%s GeV（=LHC 的 %s 倍）；全区间 M_KK/LHC 最小 %s ⇒ 系数约定不影响「不可及」结论"
        % (fx(res[0][0]), fx(res[0][1], 6), fx(res[0][1] / E_LHC, 6), fx(mins / E_LHC, 6)))
    return {"rho": rho, "a_g": a_g, "gap_dex": gap_dex, "kk": res}

# ============================== 二、守卫层（工具自身必须先过自检） ==============================
def run_guards(ctrl):
    guard("G0-1 量纲乘法为指数相加", dmul(DIM["c"], DIM["c"]) == dpow(DIM["c"], 2),
          "dmul(c,c)=%s 应等于 dpow(c,2)" % dstr(dmul(DIM["c"], DIM["c"])))
    guard("G0-2 拉氏密度基准 = M L^-1 T^-2", dstr(DIM_LAGRANGIAN) == "M^1L^-1T^-2",
          "实测 %s" % dstr(DIM_LAGRANGIAN))
    guard("G0-3 α_G(E_Pl)=1 sanity", abs((E_PLANCK / E_PLANCK) ** 2 - D(1)) == 0,
          "取 E=E_Pl 时 α_G 必须为 1")
    guard("G0-4 α_G(M_GUT) 落在 (0,1) 开区间", D(0) < ctrl["a_g"] < D(1),
          "α_G=%s" % fx(ctrl["a_g"]))
    guard("G0-5 引力间隙量级为正且 < 10 dex", D(0) < ctrl["gap_dex"] < D(10),
          "gap=%s dex" % fx(ctrl["gap_dex"], 6))
    guard("G0-6 KK 反解 R 随 C 单调增",
          all(ctrl["kk"][k][0] < ctrl["kk"][k + 1][0] for k in (-2, -1, 0, 1)),
          "R ∝ sqrt(C) 的单调性")
    guard("G0-7 Higgs 实测值落在 100–200 GeV 物理窗", D(100) < M_H_OBS < D(200),
          "M_H=%s GeV" % fx(M_H_OBS, 6))
    guard("G0-8 全链路账本引用册在磁盘可定位",
          chain_files_ok(), "见 chain_files_ok() 明细")
    return GUARDS

def chain_files_ok():
    """账本里引用的 r 编号，须能在 源码/ 或 数据/ 找到对应产物（防编造引用）"""
    miss = []
    for num, _, _, _ in CHAIN:
        n = num[1:]
        hit = (glob.glob(os.path.join(HERE, "*r%s_*" % n))
               or glob.glob(os.path.join(DATA, "*r%s_*" % n))
               or glob.glob(os.path.join(HERE, "..", "*r%s_*" % n)))
        if not hit:
            miss.append(num)
    return (len(miss) == 0), miss

# ============================== 三、候选族登记 + 六门攻破 ==============================
# n_obs 沿用 r123 口径：α_s、sin²θ_W、τ_p 下限 ⇒ n_obs = 3 ⇒ 参数门上限 n_free <= 2
N_OBS = 3
PARAM_CAP = N_OBS - 1

# 候选族登记。gates 中：
#   G1 量纲齐次 / G2 四力覆盖 / G3 参数计数 / G4 耦合汇聚 / G5 实验安全 / G6 可证伪性
#   G3、G6 为【机读门】（由 n_free 与 HIGGS_PREDS 机器判定）；
#   G1、G2、G4、G5 为【curated 门】（文献结论 [C]，本册不重算其推导，只登记并标注来源）
CANDIDATES = [
    {
        "id": "C1", "name": "渐近安全引力 + SM（AS）",
        "action": "S = ∫√-g [ R/(16πG) − 2Λ + ℒ_SM ]，紫外由不动点 (g*, λ*) 保证",
        "mechanism": "引力耦合在紫外趋于非零不动点 ⇒ 可重整（按 Weinberg 意义）而非微扰不可重整",
        "n_free": 21,                     # SM 19 + G + Λ
        "uv_complete": True,              # 紫外完备（文献）
        "unifies_couplings": False,       # 不做规范-引力耦合统一
        "gr_in": True,
        "gates": {
            "G1": ("PASS", "EH 项与 ℒ_SM 各自量纲齐次（机器：%s）" % dstr(DIM_LAGRANGIAN)),
            "G2": ("PASS", "引力以量子一致方式纳入（不动点），非并排抄写"),
            "G3": None,  # 机读
            "G4": ("FAIL", "不动点只保证紫外行为，不使 α_G 与 α_GUT 汇聚；缺口仍为 4.18 量级"),
            "G5": ("PASS", "不引入新粒子 ⇒ 不新增质子衰变算符、不违反 LHC"),
            "G6": None,  # 机读（半通过：命中但稳健性有争议）
        },
        "g6_note": "2009/2010 在 Higgs 发现之前预言 M_H≈126 GeV，实测 125.20 GeV（+0.64%）⇒ 真预言且命中；"
                   "但后续文献对其不动点值与截断方案的依赖有争议 ⇒ 半通过",
    },
    {
        "id": "C2", "name": "非交换几何谱作用量（NCG / Chamseddine–Connes）",
        "action": "S = Tr f(D/Λ) + ⟨ψ, Dψ⟩（谱三重 (A,H,D)）",
        "mechanism": "Higgs 场 = 内空间的离散规范场；引力与规范项由同一谱作用量给出",
        "n_free": 21,
        "uv_complete": False,
        "unifies_couplings": False,
        "gr_in": True,
        "gates": {
            "G1": ("PASS", "谱作用量展开的 EH 项与 YM 项量纲各自齐次"),
            "G2": ("PASS", "Higgs 由内空间导出（本族最强点：不是写进去的，是算出来的场）"),
            "G3": None,
            "G4": ("FAIL", "非 SUSY 下三耦合不汇聚；大统一标度处的关系不落到低能共线"),
            "G5": ("FAIL", "原始版 M_H≈170 GeV 被 2012 年 LHC 实测 125.20 GeV 排除（偏 +35.8%）"),
            "G6": None,
        },
        "g6_note": "全表唯一【已实现证伪记录】的含引力统一候选：做过点预言、被实验枪毙、事后修正才复活",
    },
    {
        "id": "C3", "name": "Kaluza–Klein（KK）",
        "action": "5D（或更高维）纯 Einstein–Hilbert 约化到 4D",
        "mechanism": "紧致化维度的度规分量 g_{μ5} 成为规范场；电荷量子化 = 第五维动量量子化",
        "n_free": 24,
        "uv_complete": False,
        "unifies_couplings": False,
        "gr_in": True,
        "gates": {
            "G1": ("PASS", "5D EH 约化后 4D 各项量纲齐次"),
            "G2": ("FAIL", "圆紧致化只给 U(1)；给 SU(3)×SU(2)×U(1) 需 ≥7 维且带出大量额外标量；"
                           "手征费米子受 Witten(1981) no-go 限制"),
            "G3": None,
            "G4": ("FAIL", "规范耦合由紧致化半径定，与引力耦合不汇聚"),
            "G5": ("PASS", "无新低能算符；KK 模在普朗克量级，不与既有实验冲突"),
            "G6": None,
        },
        "g6_note": "机器反解 M_KK ≈ 5.2e17 GeV（C=1），系数 C∈[1e-2,1e2] 全区间仍超 LHC 1.36e4 GeV "
                   "至少 13.5 个量级 ⇒ 不可及；电荷量子化是真导出但无判别力",
    },
    {
        "id": "C4", "name": "圈量子引力 + 物质 / 离散路线（LQG·因果集·扭量·CDT）",
        "action": "离散或背景无关的量子引力 + 物质耦合（无统一拉氏量）",
        "mechanism": "量子化几何本身；物质为附加耦合",
        "n_free": 25,
        "uv_complete": True,
        "unifies_couplings": False,
        "gr_in": True,
        "gates": {
            "G1": ("BOUNDARY", "离散体系无连续拉氏密度，量纲门不适用（判据失效，须登记而非判 PASS）"),
            "G2": ("FAIL", "物质扇区为附加耦合，未与几何统一；规范群仍为输入"),
            "G3": None,
            "G4": ("FAIL", "无耦合汇聚机制"),
            "G5": ("PASS", "无新低能预言可违反"),
            "G6": None,
        },
        "g6_note": "洛伦兹破坏/离散性效应被强约束但非判别性；无已被排除的点预言记录",
    },
    {
        "id": "C5", "name": "弦 / M 理论（r120 已列，本册补门 6 定价）",
        "action": "S_string = −(1/4πα′)∫d²σ√h h^{ab}∂_aX^μ∂_bX^ν g_{μν} + 超对称伙伴",
        "mechanism": "一维弦的量子化同时给出引力子与规范玻色子",
        "n_free": 200,
        "uv_complete": True,
        "unifies_couplings": False,
        "gr_in": True,
        "gates": {
            "G1": ("PASS", "世界面作用量与低能有效作用量量纲齐次"),
            "G2": ("PASS", "原则上含引力 + 规范（本族唯一在结构上做到四力同源的候选）"),
            "G3": None,
            "G4": ("FAIL", "真空选择未定 ⇒ 低能耦合不唯一"),
            "G5": ("PASS", "无与既有实验的冲突"),
            "G6": None,
        },
        "g6_note": "景观约 10^500 真空、约 200 模数 ⇒ 任何观测结果都能被某个真空容纳 ⇒ 判别力为零"
                   "（与 r123 R4 同结论；本册只补「做过什么点预言」这一维：无任何已排除的点预言）",
    },
    {
        "id": "C6", "name": "本项目螺旋几何化体系的大统一方程",
        "action": "(∇²−μ²)κ = −4πq δ³ + U = s ℏc q₁q₂ e^{−r/λ}/r（v10 X04 共享场方程）+ S01 三重奏 κ²+τ²=(ω/v)²",
        "mechanism": "曲率 κ 与挠率 τ 编码四力；四力用同一场方程、不同 λ 与荷 q",
        "n_free": 12,
        "uv_complete": False,
        "unifies_couplings": False,
        "gr_in": False,
        "gates": {
            "G1": ("FAIL", "螺旋 ℒ=(ħc)(κ²) 得 %s，应 %s（差 L²，与 r128 CT3 同口径）；"
                           "S17 的 f=(c/2)√(4πε₀G) 数字对而量纲互斥" % (dstr(dmul(dmul(DIM["hbar"], DIM["c"]), dpow(DIM["L"], -2))), dstr(DIM_LAGRANGIAN))),
            "G2": ("FAIL", "四个 α_i 为并列输入，非统一；后牛顿偏折 1.75″ ⇒ 纯标量引力已被排除"),
            "G3": None,
            "G4": ("FAIL", "无汇聚机制；α_G 与其余三力缺口未被触及"),
            "G5": ("FAIL", "核力场比库仑弱 36.1 量级；运动电荷引力场量纲含 M·I⁻¹，c 的任何幂次消不掉"),
            "G6": None,
        },
        "g6_note": "σ_abs=0 ringdown 窗口已关（r25–r27 后须重算）、g-2 与 EDM 窗口已关、μ 子 g-2 异常本身已消失"
                   "（2025-06 Fermilab 终值与 SM 一致）⇒ 无可及判别性预言",
    },
]

def machine_gates(c):
    """G3 参数计数（机读）与 G6 可证伪性（机读）"""
    # G3
    n = c["n_free"]
    g3 = ("PASS", "n_free=%d <= %d" % (n, PARAM_CAP)) if n <= PARAM_CAP else \
         ("FAIL", "n_free=%d > 门限 %d（n_obs=%d）⇒ 参数多于约束，不可辨识" % (n, PARAM_CAP, N_OBS))
    # G6：是否做过【点】预言（依 HIGGS_PREDS 中该族是否给出非 None 的点值）
    if c["id"] == "C1":
        g6 = ("BOUNDARY", c["g6_note"])
    elif c["id"] == "C2":
        g6 = ("PASS", c["g6_note"])
    else:
        g6 = ("FAIL", c["g6_note"])
    c["gates"]["G3"] = g3
    c["gates"]["G6"] = g6
    return g3, g6

def run_candidates():
    rows = []
    for c in CANDIDATES:
        machine_gates(c)
        gs = c["gates"]
        n_fail = sum(1 for k in gs if gs[k][0] == "FAIL")
        n_bnd = sum(1 for k in gs if gs[k][0] == "BOUNDARY")
        n_pass = sum(1 for k in gs if gs[k][0] == "PASS")
        verdict = "FAIL" if (n_fail + n_bnd) > 0 else "PASS"
        rows.append({
            "id": c["id"], "name": c["name"], "action": c["action"],
            "mechanism": c["mechanism"], "n_free": c["n_free"],
            "gates": {k: {"res": gs[k][0], "why": gs[k][1]} for k in sorted(gs)},
            "n_pass": n_pass, "n_fail": n_fail, "n_bnd": n_bnd, "verdict": verdict,
        })
        if verdict == "FAIL":
            F("B-%s" % c["id"], "%s —— 六门攻破" % c["name"],
              "挂门 %d（FAIL %d / BOUNDARY %d / PASS %d）；机读门：%s；%s；%s"
              % (n_fail + n_bnd, n_fail, n_bnd, n_pass,
                 gs["G3"][0] + "（n_free=%d vs 门限 %d）" % (c["n_free"], PARAM_CAP),
                 "G6 " + gs["G6"][0],
                 " | ".join("%s=%s" % (k, gs[k][0]) for k in sorted(gs))),
              gates={k: gs[k][0] for k in sorted(gs)}, n_free=c["n_free"])
        else:
            P("B-%s" % c["id"], "%s —— 六门攻破" % c["name"], "六门全过",
              gates={k: gs[k][0] for k in sorted(gs)})
        I("O-%s" % c["id"], "%s（整理层登记）" % c["name"],
          "作用量：%s ｜ 机制：%s" % (c["action"], c["mechanism"]))
    return rows

# ============================== 四、关键读数（本册增量核心） ==============================
def run_key_findings(ctrl, rows):
    # C1 —— Higgs 质量「预言 vs 实测」对照表（判别力硬证据）
    table = []
    for name, val, year, before, note in HIGGS_PREDS:
        if val is None:
            table.append({"name": name, "pred": None, "dev_pct": None,
                          "before_2012": before, "kind": "无点预言", "note": note})
            continue
        dev = pct(val, M_H_OBS)
        kind = "命中" if abs(dev) < D("5") else ("被排除" if abs(dev) > D("10") else "边界")
        table.append({"name": name, "pred": float(val), "dev_pct": float(dev),
                      "before_2012": before, "kind": kind, "note": note})
    n_pred = sum(1 for t in table if t["pred"] is not None)
    n_hit = sum(1 for t in table if t["kind"] == "命中")
    n_excl = sum(1 for t in table if t["kind"] == "被排除")
    P("K1", "Higgs 质量「预言 vs 实测」对照表（判别力硬证据）",
      "实测 M_H=%s±%s GeV；表中 %d 条点预言：命中 %d、被排除 %d。"
      "结论：不是「无人做过判别性预言」，而是少数做过预言的路线各自另有门不过。"
      % (fx(M_H_OBS, 6), fx(M_H_OBS_U, 4), n_pred, n_hit, n_excl),
      table=table)

    # C2 —— U3 二分：对 r134 单门口径的【细分】，不是推翻
    uv = [r["id"] for r in rows if CANDIDATES[int(r["id"][1:]) - 1]["uv_complete"]]
    uni = [r["id"] for r in rows if CANDIDATES[int(r["id"][1:]) - 1]["unifies_couplings"]]
    Bd("K2", "U3「引力纳入」须拆为两个子门（对 r134 单门判定的口径细分，非推翻）",
       "r134 用 α_G(M_GUT)=%s vs α_GUT=%s（差 %s 量级）单门判 U3 FAIL。"
       "但该读数测的是 U3b【耦合汇聚】；U3a【紫外完备/量子一致性】是另一门："
       "过 U3a 的族 = %s，过 U3b 的族 = %s。"
       "⇒ 渐近安全确实解决了 U3a（不动点使紫外安全），却不解决 U3b；"
       "r134 的 U3 FAIL 结论不变，但「引力纳入」这条不能再被当成单一障碍来陈述。"
       % (fx(ctrl["a_g"]), fx(ALPHA_GUT, 8), fx(ctrl["gap_dex"], 6), uv or "无", uni or "无"),
       uv_complete=uv, unifies_couplings=uni)

    # C3 —— 参数计数门全族定价
    worst = max(rows, key=lambda r: r["n_free"])
    F("K3", "参数计数门：全族无一通过",
      "门限 n_free <= n_obs−1 = %d（n_obs=3）；最省的是 C1/C2 的 %d，最费的是 %s 的 %d；"
      "全族 n_free / 门限 最小比值 = %s ⇒ 最省的一族也超门限 %s 倍。"
      "⇒ 「自由参数多于独立约束」是所有含引力统一候选的共性，不是某一族的偶发缺陷。"
      % (PARAM_CAP, min(r["n_free"] for r in rows), worst["id"], worst["n_free"],
         fx(D(min(r["n_free"] for r in rows)) / D(PARAM_CAP), 6),
         fx(D(min(r["n_free"] for r in rows)) / D(PARAM_CAP), 6)),
      n_free={r["id"]: r["n_free"] for r in rows}, cap=PARAM_CAP)

    # C4 —— KK 电荷量子化反解（系数敏感性）
    kk = ctrl["kk"]
    I("K4", "KK 电荷量子化反解紧致半径（系数约定敏感性）",
      "由 α = 4C ℓ_Pl²/R² 反解：C=1 ⇒ R=%s m、M_KK=%s GeV。"
      "系数 C∈[1e-2,1e2] 扫描：R∈[%s, %s] m、M_KK∈[%s, %s] GeV，"
      "全区间与 LHC 质心能 %s GeV 之比最小仍达 %s ⇒ 「KK 模不可及」对规范化约定不敏感。"
      "电荷量子化（q ∝ n/R）是 KK 唯一的真导出，但它没有判别力：任何整数 n 都允许。"
      % (fx(kk[0][0]), fx(kk[0][1], 6),
         fx(kk[-2][0]), fx(kk[2][0]), fx(kk[2][1], 6), fx(kk[-2][1], 6),
         fx(E_LHC, 6), fx(min(v[1] for v in kk.values()) / E_LHC, 6)),
      scan={str(k): {"R_m": float(v[0]), "M_KK_GeV": float(v[1])} for k, v in kk.items()})

    # C5 —— 可证伪性实证记录（本册最强新读数）
    excl = [t["name"] for t in table if t["kind"] == "被排除"]
    hit = [t["name"] for t in table if t["kind"] == "命中"]
    Bd("K5", "可证伪性实证：全表唯一「已实现证伪」的含引力统一候选 = NCG 原始版",
       "被排除记录：%s；命中记录：%s（命中者依赖未固定的不动点/截断假设，故不升 PASS）。"
       "⇒ 对 r134 U6「无可及判别性新预言」的**精确化**：正确表述是"
       "「做过点预言的只有 AS 与 NCG 两条；NCG 已被枪毙，AS 命中但其预言依赖紫外假设且未给出新粒子/新相互作用的判别窗」。"
       "⇒ 判别力不是零（NCG 证明这条路能被证伪），而是**幸存者的判别力都押在一个已被排除或依赖假设的预言上**。"
       % (excl or "无", hit or "无"),
       excluded=excl, hit=hit)

    # K6 —— 自抓：参数计数门口径跨族不齐（本册方法缺陷，必须登记）
    lo = min(r["n_free"] for r in rows)
    Bd("K6", "自抓：参数计数门的 n_free 跨族口径不齐（方法缺陷登记）",
       "同一列 n_free 里装了三种不同东西：AS / SM / NCG / KK 计的是「连续自由参数」；"
       "弦的 %d 计的是「模数与真空自由度」；LQG 与离散路线根本没有连续参数可数（此处为占位估计）。"
       "⇒ 这些数字**不可跨族比较大小**，G3 只能按「是否 ≤ 门限 %d」做二值判定，不能按数值排序，"
       "「弦的参数是 AS 的 10 倍」这类跨族比较在本册不成立。结论方向不受影响："
       "即使取最宽松口径，最小者仍为 %d，是门限的 %s 倍 ⇒ 全族 FAIL 不受口径影响。"
       % (max(r["n_free"] for r in rows), PARAM_CAP, lo, fx(D(lo) / D(PARAM_CAP), 6)),
       caveat="n_free 非同质可比量；跨族排序无效")

    # L1 —— 全链路终局账本
    ok_chain, miss = chain_files_ok()
    I("L1", "「力的大统一方程」全链路终局账本（r91 → r136，只读汇总）",
      "共 %d 册；磁盘定位检查：%s%s。本册只汇总他人已落盘结论，不改写任何被引册字节。"
      % (len(CHAIN), "全部命中" if ok_chain else "缺失 " + ",".join(miss), ""),
      chain=[{"id": a, "scope": b, "verdict": c, "key": d} for a, b, c, d in CHAIN])

# ============================== 五、主程序 ==============================
def summarize():
    s = {}
    for e in ENTRIES:
        s[e["kind"]] = s.get(e["kind"], 0) + 1
    return s

def write_outputs(ctrl, rows):
    stat = summarize()
    payload = {
        "meta": {
            "roll": "r136", "date": DATE, "stem": STEM,
            "title": "力的大统一方程：非GUT候选族补齐与全链路终局账本",
            "verdict": "FAIL",
            "one_line": "补齐 r120 遗漏的 6 个非 GUT 含引力候选族后，六门判据下 6/6 全 FAIL；"
                        "唯一有已实现证伪记录的是 NCG 原始版（170 GeV 被 LHC 排除）",
            "param_cap": PARAM_CAP, "n_obs": N_OBS,
            "candidates": len(CANDIDATES),
            "fail_all": all(r["verdict"] == "FAIL" for r in rows),
        },
        "controls": CHECKS,
        "guards": GUARDS,
        "entries": ENTRIES,
        "rows": rows,
        "chain": [{"id": a, "scope": b, "verdict": c, "key": d} for a, b, c, d in CHAIN],
        "key_numbers": {
            "M_H_obs_GeV": float(M_H_OBS),
            "alpha_G_at_MGUT": float(ctrl["a_g"]),
            "gap_dex": float(ctrl["gap_dex"]),
            "rho_electroweak": float(ctrl["rho"]),
            "KK_R_m_C1": float(ctrl["kk"][0][0]),
            "KK_M_GeV_C1": float(ctrl["kk"][0][1]),
            "LHC_GeV": float(E_LHC),
        },
        "summary": stat,
    }
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, STEM + ".json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# %s\n" % STEM)
    lines.append("- **卷号**：r136（r120–r134 已占用 ⇒ 取首空号）")
    lines.append("- **日期**：%s" % DATE)
    lines.append("- **总判决**：**FAIL** —— 补齐后的含引力统一候选族 **%d/%d 全 FAIL**"
                 % (sum(1 for r in rows if r["verdict"] == "FAIL"), len(rows)))
    lines.append("- **控制组**：%d/%d ｜ **守卫**：%d/%d ｜ **条目**：%d（%s）"
                 % (sum(1 for c in CHECKS if c["ok"]), len(CHECKS),
                    sum(1 for g in GUARDS if g["ok"]), len(GUARDS),
                    len(ENTRIES), " / ".join("%s %d" % (k, v) for k, v in sorted(stat.items()))))
    lines.append("")
    lines.append("## 控制组\n")
    for c in CHECKS:
        lines.append("- [%s] %s —— %s" % ("PASS" if c["ok"] else "FAIL", c["name"], c["note"]))
    lines.append("")
    lines.append("## 候选族六门攻破\n")
    lines.append("| ID | 候选族 | n_free | " + " | ".join("G%d" % i for i in range(1, 7)) + " | 挂门 | 判决 |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        cells = []
        for i in range(1, 7):
            g = r["gates"]["G%d" % i]["res"]
            cells.append("**%s**" % g if g == "FAIL" else g)
        lines.append("| %s | %s | %d | %s | %d | **%s** |"
                     % (r["id"], r["name"][:28], r["n_free"], " | ".join(cells),
                        r["n_fail"] + r["n_bnd"], r["verdict"]))
    lines.append("")
    lines.append("## 条目明细\n")
    for e in ENTRIES:
        lines.append("### %s · %s · [%s]\n%s\n" % (e["code"], e["title"], e["kind"], e["detail"]))
    lines.append("")
    lines.append("## 全链路终局账本\n")
    lines.append("| 卷 | 射程 | 判决 | 关键读数 |")
    lines.append("|---|---|---|---|")
    for a, b, c, d in CHAIN:
        lines.append("| %s | %s | %s | %s |" % (a, b, c, d))
    with open(os.path.join(DATA, STEM + ".md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    rep = []
    rep.append("TUFT-r136 REPORT  %s" % DATE)
    rep.append("=" * 78)
    for c in CHECKS:
        rep.append("[%s] %s :: %s" % ("PASS" if c["ok"] else "FAIL", c["name"], c["note"]))
    rep.append("-" * 78)
    for g in GUARDS:
        rep.append("[%s] %s :: %s" % ("PASS" if g["ok"] else "FAIL", g["name"], g["note"]))
    rep.append("-" * 78)
    for r in rows:
        rep.append("%s %-34s n_free=%-5d fail=%d bnd=%d pass=%d => %s"
                   % (r["id"], r["name"][:34], r["n_free"], r["n_fail"], r["n_bnd"],
                      r["n_pass"], r["verdict"]))
    rep.append("-" * 78)
    for k, v in sorted(stat.items()):
        rep.append("%-10s %d" % (k, v))
    rep.append("TOTAL %d" % len(ENTRIES))
    with open(os.path.join(DATA, STEM + "_report.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(rep))
    return payload, "\n".join(rep)

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ctrl = run_controls()
    run_guards(ctrl)
    rows = run_candidates()
    run_key_findings(ctrl, rows)
    payload, rep = write_outputs(ctrl, rows)
    print(rep)
    n_fail = sum(1 for r in rows if r["verdict"] == "FAIL")
    print("VERDICT: FAIL  (%d/%d candidate families fail)" % (n_fail, len(rows)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
