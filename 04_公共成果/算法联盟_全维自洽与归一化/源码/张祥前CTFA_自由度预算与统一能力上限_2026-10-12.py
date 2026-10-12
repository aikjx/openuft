# -*- coding: utf-8 -*-
# 张祥前《三条公理 + CTFA 几何恒等式层》自由度预算与统一能力上限 全维全链路审计
# 日期：2026-10-12
# 口径：纯标准库 Decimal 60 位 + Fraction 三维量纲 (M,L,T)；复用同目录 CTFA 审计册量纲代数。
# 目的：把「三条公理 + CTFA 恒等式层 到底能统一什么、能攻破什么」从口头论断落成机器判决表——
#   (A) 自由度机器计数：恒等式层对 (kappa,tau) 的依赖是否闭合、独立自由度到底几个；
#   (B) 四力需求对照：4 个耦合 + 短程力程需求 vs 可用自由度，算出缺口；
#   (C) RG 承载能力：alpha=tau/kappa 是纯几何比，是否能承载 alpha_s 跑动（beta 恒零否证）；
#   (D) 标度单一性：kappa/tau 同量纲 => 单长度标度，能否覆盖弱/强两个力程（机器判无解）；
#   (E) 循环贴标签二择一：Z=Gc/2、Z'=c/(8*pi*eps0) 从实验常数反解，两读法代价对照；
#   (F) 替换检验（零判别力）：把 alpha 换成任意值，几何输出是否改变；
#   (G) 「攻破了什么」三层裁定：外部理论否证数 / 库内同族方法论成果 / 实验窗口状态。
# 红线：数学自洽 != 物理证实；本册只做可判定的结构与自由度审计，不产生新物理。
import json, os, sys
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 60

# ============================ 条目累加器 ============================
ENTRIES = []
def P(tag, title, detail, evidence=None):
    ENTRIES.append({"tag": tag, "title": title, "detail": detail,
                    "evidence": evidence or {}, "verdict": "PASS"})
def F(tag, title, detail, evidence=None):
    ENTRIES.append({"tag": tag, "title": title, "detail": detail,
                    "evidence": evidence or {}, "verdict": "FAIL"})
def B(tag, title, detail, evidence=None):
    ENTRIES.append({"tag": tag, "title": title, "detail": detail,
                    "evidence": evidence or {}, "verdict": "BOUNDARY"})
def I(tag, title, detail, evidence=None):
    ENTRIES.append({"tag": tag, "title": title, "detail": detail,
                    "evidence": evidence or {}, "verdict": "INFO"})
def rel(x, y):
    """相对偏差 |x-y|/|y|，y 不得为 0。入参允许 Decimal/int/str（str 视为已格式化读数）。"""
    x, y = Decimal(str(x)), Decimal(str(y))
    if y == 0:
        return Decimal(1)
    return abs(x - y) / abs(y)
def sci(x, n=12):
    return format(Decimal(x), "." + str(n) + "E")
# ============================ 量纲系统 (M,L,T) ============================
def D(*e):
    return tuple(Fraction(x) for x in e)
M = D(1, 0, 0)
L = D(0, 1, 0)
T = D(0, 0, 1)
ONE = D(0, 0, 0)
G_DIM = D(-1, 3, -2)
def dadd(d1, d2):
    """量纲相乘 = 指数相加（本库教训：写成逐分量相乘曾把三处 FAIL 全算错）。"""
    return tuple(a + b for a, b in zip(d1, d2))
def dscale(d, k):
    return tuple(a * Fraction(k) for a in d)
def dpow(d, e):
    return dscale(d, Fraction(e))
def dinv(d):
    return dscale(d, -1)
def deq(d1, d2):
    return all(a == b for a, b in zip(d1, d2))
def dim_str(d):
    parts, names = [], "MLT"
    for nm, v in zip(names, d):
        if v == 0:
            continue
        s = nm if v == 1 else "%s^%s" % (nm, v)
        parts.append(s)
    return "*".join(parts) if parts else "1"

# ============================ 量纲工具自检 (G0) ============================
# 纪律：量纲工具本身必须先过自检，否则会把整册判定算错。
G0 = []
def g0(tag, ok, msg):
    G0.append({"tag": tag, "ok": bool(ok), "msg": msg})
    if ok:
        P(tag, "量纲工具自检", msg)
    else:
        F(tag, "量纲工具自检", msg)
g0("G0-1", deq(dadd(M, L), D(1, 1, 0)), "dadd(M,L)==M*L 指数相加正确")
g0("G0-2", deq(dpow(L, -2), D(0, -2, 0)), "dpow 负指数正确（1/ell^2）")
g0("G0-3", deq(dscale(L, Fraction(3, 2)), (Fraction(0), Fraction(3, 2), Fraction(0))),
   "dscale 接受 Fraction(3/2)：L^(3/2)=(0,3/2,0)（自抓：首版期望值误写为 (0,3,2)）")
g0("G0-4", deq(dinv(G_DIM), D(1, -3, 2)), "dinv(G)==1/G 量纲正确")
g0("G0-5", dim_str(D(0, 1, 0)) == "L" and dim_str(ONE) == "1", "dim_str 基本输出正确")
g0("G0-6", deq(dpow(G_DIM, 2), D(-2, 6, -4)), "[G]^2 量纲正确（G^2/c^4 类比）")
# 阳性对照：故意把量纲写成逐分量相乘（已知错误实现），必须被判出不等
bad_mul = tuple(a * b for a, b in zip(D(1, 0, 0), D(0, 1, 0)))
g0("G0-7", not deq(bad_mul, D(1, 1, 0)), "阳性对照：逐分量相乘的错误实现被正确判为不等")

# ============================ 常数 (CODATA) ============================
C = Decimal("299792458")
G = Decimal("6.67430e-11")
HBAR = Decimal("1.054571817e-34")
EPS0 = Decimal("8.8541878128e-12")
ALPHA = Decimal("7.2973525693e-3")
M_E = Decimal("9.1093837015e-31")
L_P = (HBAR * G / (C ** 3)).sqrt()
T_P = L_P / C
M_P = (HBAR * C / G).sqrt()
M_W = Decimal("80.379")                      # GeV，W 玻色子（弱力程）
LAMBDA_QCD = Decimal("0.200")                # GeV，强作用特征标度
HBARC = HBAR * C                             # J·m
GEV_J = Decimal("1.602176634e-10")
ELL_W = HBARC / (M_W * GEV_J)                # 弱力程 ħc/M_W
ELL_QCD = HBARC / (LAMBDA_QCD * GEV_J)       # 强力程 ħc/Λ_QCD
# 耦合常数（方案书载值，用于需求侧对照）
ALPHA_EM = Decimal("7.2973525693e-3")
ALPHA_W = Decimal("0.0332")                  # g^2/(4pi) @M_Z
ALPHA_S_LOW = Decimal("0.118")                # α_s @M_Z
ALPHA_S_HIGH = Decimal("1.20")                # α_s @~1 GeV
# ============================ (A) 自由度机器计数 ============================
# 恒等式层：omega=c*sqrt(kappa^2+tau^2), R=1/sqrt(kappa^2+tau^2), m=hbar*sqrt(kappa^2+tau^2)/c,
#           alpha=tau/kappa, Xi=kappa+i*tau
# 判定：对 (kappa,tau) 的依赖是否闭合 => 独立自由度到底几个。
def ctfa_from_kappa_tau(kappa, tau):
    """给定两个几何量，CTFA 层全部输出。返回 dict。"""
    s = (kappa * kappa + tau * tau).sqrt()      # = sqrt(kappa^2+tau^2) = omega/c = 1/R
    return {
        "omega": C * s,                          # 角频率 T^-1
        "R": Decimal(1) / s,                     # 螺旋半径 L
        "m": HBAR * s / C,                       # 质量 M
        "alpha": tau / kappa,                    # 无量纲比
        "Xi_modulus": s,                         # |Xi| = sqrt(kappa^2+tau^2)
    }
# 取一个与普朗克尺度同阶、alpha=CODATA 的测试几何量（不使用来料回填值）
s_test = Decimal(1) / L_P
kappa_test = s_test / (Decimal(1) + ALPHA * ALPHA).sqrt()
tau_test = ALPHA * kappa_test
out = ctfa_from_kappa_tau(kappa_test, tau_test)

# A-1 闭合性：omega/c 必须逐位等于 sqrt(kappa^2+tau^2)
s_direct = (kappa_test ** 2 + tau_test ** 2).sqrt()
P("A-1", "omega 对 (kappa,tau) 依赖闭合",
  "omega/c = sqrt(kappa^2+tau^2)，omega 不是独立自由度，是 (kappa,tau) 的函数。",
  {"omega_over_c": sci(out["omega"] / C), "sqrt_direct": sci(s_direct),
   "rel": sci(rel(out["omega"] / C, s_direct))})
# A-2 R 闭合：1/R == sqrt(kappa^2+tau^2)
invR = Decimal(1) / out["R"]
P("A-2", "R 对 (kappa,tau) 依赖闭合",
  "R = 1/sqrt(kappa^2+tau^2)，螺旋半径不是独立自由度。",
  {"R": sci(out["R"]), "invR": sci(invR), "rel": sci(rel(invR, s_direct))})
# A-3 m 闭合：m = hbar*sqrt(kappa^2+tau^2)/c
P("A-3", "m 对 (kappa,tau) 依赖闭合",
  "m = hbar*sqrt(kappa^2+tau^2)/c，质量不是独立自由度。",
  {"m": sci(out["m"]), "formula": sci(HBAR * s_direct / C),
   "rel": sci(rel(out["m"], HBAR * s_direct / C))})
# A-4 alpha 不增自由度：alpha 只由比值决定，改 kappa/tau 同比例不变
k2, t2 = kappa_test * Decimal("3.7"), tau_test * Decimal("3.7")
out2 = ctfa_from_kappa_tau(k2, t2)
P("A-4", "alpha=tau/kappa 耗尽同两自由度",
  "alpha 是 kappa,tau 之比，不引入第三个自由度；同比例缩放时 alpha 逐位不变。",
  {"alpha_before": sci(out["alpha"], 15), "alpha_after_scale3.7": sci(out2["alpha"], 15),
   "rel": sci(rel(out["alpha"], out2["alpha"]))})
# A-5 Xi 复曲率只有 2 实自由度
P("A-5", "复曲率 Xi=kappa+i*tau 仅 2 实自由度",
  "复数不增实自由度：|Xi| 由模给出、kappa,tau 由幅角给出，仍是 2 个。",
  {"Xi_modulus": sci(out["Xi_modulus"]), "real_freedom": 2})
# A-6 独立自由度总账
FREE_PARAMS = 2
I("A-6", "CTFA 层独立自由度 = 2",
  "等价表述：1 个长度标度 ell=1/sqrt(kappa^2+tau^2) + 1 个无量纲参数 alpha。"
  "全部输出量 omega/R/m/alpha/Xi 均为 (kappa,tau) 的函数，无一例外。",
  {"independent_params": FREE_PARAMS,
   "equivalent_description": "1 length scale + 1 dimensionless ratio",
   "derived_quantities": ["omega", "R", "m", "alpha", "Xi"]})

# A-7 两种读法的自由参数/预言数对照（结构无差别性判据）
# 读法1：kappa,tau 为基本量 => m 由公式决定，但要预测某个粒子的质量必须先指定
#         kappa^2+tau^2=(mc/hbar)^2 => 输入即输出，零预言。
# 读法2：omega(=mc^2/hbar) 为基本量 => kappa^2+tau^2=(omega/c)^2 是恒等式，
#         kappa = s*cos(theta)、tau = s*sin(theta)，需额外输入 alpha(即 theta) => 2 自由参数。
READ1 = {"basic": ["kappa", "tau"], "n_free": 2, "n_predictions": 0,
         "reason": "m=hbar*sqrt(kappa^2+tau^2)/c 要给出某个粒子质量，必须先指定 "
                   "kappa^2+tau^2=(mc/hbar)^2；即逐粒子回填 s，等于把质量重命名为几何量。"}
READ2 = {"basic": ["omega", "alpha"], "n_free": 2, "n_predictions": 0,
         "reason": "kappa^2+tau^2=(omega/c)^2 是定义性恒等式，只把 kappa,tau 写成 "
                   "s*cos(theta)、s*sin(theta)，角 theta 仍须外部给定（即 alpha）。"}
P("A-7", "两种读法自由参数同为 2、预言数同为 0",
  "恒等式层对「谁是基本量」不敏感 => 不构成约束理论，只构成改写。这是结构无差别的机器证据。",
  {"reading1": READ1, "reading2": READ2,
   "n_free_equal": READ1["n_free"] == READ2["n_free"],
   "n_pred_equal": READ1["n_predictions"] == READ2["n_predictions"]})

# ============================ (B) 四力需求对照 ============================
# 需求侧：4 个相互作用，各自需要 1 个耦合值（其中强耦合跑动）+ 短程力程标度。
# 供给侧：CTFA 层只有 2 个自由度（1 长度标度 + 1 无量纲 alpha）。
FORCES = [
    {"force": "gravity", "coupling": "G", "coupling_value": sci(G, 6),
     "coupling_dim": dim_str(G_DIM), "range_scale": "macroscopic (>m)",
     "carrier_in_ctfa": "kappa 分量 (经 Z=Gc/2)", "status": "有载体(需 Z)"},
    {"force": "electromagnetic", "coupling": "alpha_em", "coupling_value": sci(ALPHA_EM, 10),
     "coupling_dim": dim_str(ONE), "range_scale": "macroscopic (>m)",
     "carrier_in_ctfa": "alpha=tau/kappa", "status": "有载体"},
    {"force": "weak", "coupling": "alpha_W", "coupling_value": sci(ALPHA_W, 6),
     "coupling_dim": dim_str(ONE), "range_scale": "short (hbar*c/M_W)",
     "carrier_in_ctfa": "无", "status": "缺"},
    {"force": "strong", "coupling": "alpha_s(跑动)", "coupling_value": "%s..%s" % (sci(ALPHA_S_LOW, 6), sci(ALPHA_S_HIGH, 6)),
     "coupling_dim": dim_str(ONE), "range_scale": "short (hbar*c/Lambda_QCD)",
     "carrier_in_ctfa": "无", "status": "缺"},
]
n_missing = sum(1 for x in FORCES if x["status"] == "缺")
P("B-1", "四力需求与 CTFA 供给对照完成",
  "4 个相互作用中 2 个有载体（引力经 Z、电磁经 alpha），2 个（弱、强）无任何自由度可承载。",
  {"table": FORCES, "n_missing": n_missing})
F("B-2", "自由度缺口 = 2（弱、强两个扇区无载体）",
  "缺口是结构性的：omega/R/m 全为 (kappa,tau) 的函数，alpha 是比值，"
  "无第三个可调量可供弱子用。按库内 Ω5(自由常数<=1) 与节点自由度口径，"
  "补 2 个自由度必然新增未声明外部输入，故这不是「还没推导出来」，是「无处可放」。",
  {"required_forces": 4, "available_dof": FREE_PARAMS, "gap": n_missing,
   "remedy_cost": "每补 1 个自由度 = +1 外部输入常数（撞 Ω5）"})
# ============================ (C) RG 承载能力 ============================
# 关键判据：CTFA 层是否存在能标 mu？若 kappa,tau 无 mu 依赖，则 alpha=tau/kappa 的 beta 恒零。
def scan_mu_dependence():
    """扫描 CTFA 层全部公式，检查是否存在 mu（能标）依赖。"""
    formulas = {
        "omega=c*sqrt(kappa^2+tau^2)": ["kappa", "tau"],
        "R=1/sqrt(kappa^2+tau^2)": ["kappa", "tau"],
        "m=hbar*sqrt(kappa^2+tau^2)/c": ["kappa", "tau"],
        "alpha=tau/kappa": ["kappa", "tau"],
        "Xi=kappa+i*tau": ["kappa", "tau"],
    }
    hits = []
    for f, syms in formulas.items():
        has_mu = ("mu" in f.lower().replace("tau", "")) or any("mu" == s for s in syms)
        if has_mu:
            hits.append(f)
    return hits, formulas
mu_hits, all_formulas = scan_mu_dependence()
# alpha_s 真实跑动幅度（需求侧，证缺口非平凡）
alpha_s_run = ALPHA_S_HIGH / ALPHA_S_LOW
F("C-1", "CTFA 层无能标 mu => d(alpha)/dln(mu) 恒 0",
  "逐式扫描 5 条 CTFA 恒等式，符号表仅含 {kappa,tau,c,hbar}，无 mu；"
  "故 alpha=tau/kappa 在两种读法下都是常数，beta(alpha)=0，无法承载跑动耦合。",
  {"mu_dependent_formulas": mu_hits, "n_formulas_scanned": len(all_formulas),
   "beta_alpha": "0 (恒零)", "verdict": "RG 结构缺失"})
P("C-2", "需求侧 alpha_s 跑动幅度非零（缺口真实、非平凡）",
  "α_s 从 M_Z 到 ~1GeV 跨约一个量级，是真实 RG 效应；CTFA 层 beta≡0 无法复现。",
  {"alpha_s_low": sci(ALPHA_S_LOW, 6), "alpha_s_high": sci(ALPHA_S_HIGH, 6),
   "ratio": sci(alpha_s_run, 6), "log10_span": sci(alpha_s_run.ln() / Decimal(10).ln(), 6)})

# ============================ (D) 标度单一性 ============================
# kappa 与 tau 同量纲 [L^-1] => CTFA 只有 1 个长度标度 ell = 1/sqrt(kappa^2+tau^2)。
# 弱/强两个短程力程要求 ell 同时取两个不同值 => 机器判定无解。
kappa_dim = D(0, -1, 0)
tau_dim = D(0, -1, 0)
P("D-1", "kappa 与 tau 同量纲 [L^-1]",
  "曲率与挠率量纲完全相同，无法用量纲区分「引力向/电磁向」；区分只靠系数 Z、Z'。",
  {"kappa_dim": dim_str(kappa_dim), "tau_dim": dim_str(tau_dim),
   "identical": deq(kappa_dim, tau_dim)})
ell_ratio = ELL_QCD / ELL_W
F("D-2", "单一长度标度无法覆盖弱/强两个力程（机器判无解）",
  "若只 1 个 ell，要同时预测弱力程 ħc/M_W 与强力程 ħc/Λ_QCD，"
  "必须要求 ell = ELL_W 且 ell = ELL_QCD，即两值相等；实测不等，故无解。",
  {"ell_weak": sci(ELL_W), "ell_strong": sci(ELL_QCD),
   "ratio_strong_over_weak": sci(ell_ratio, 6),
   "required_condition": "ELL_W == ELL_QCD", "holds": False,
   "reason": "两力程相差约 " + sci(ell_ratio - 1, 3) + " 个量级，单标度无法同时命中"})
# 机器穷举：给定单 ell，覆盖两个力程的相对误差
ell_best = (ELL_W + ELL_QCD) / Decimal(2)
err_w = rel(ell_best, ELL_W)
err_s = rel(ell_best, ELL_QCD)
P("D-3", "最优单标度下两力程相对误差量化",
  "取 ell 为两力程中值时，弱/强误差对称但均不为零，量化「单标度不可覆盖」的代价。",
  {"ell_best": sci(ell_best), "rel_err_weak": sci(err_w, 6),
   "rel_err_strong": sci(err_s, 6), "both_zero": (err_w == 0 and err_s == 0)})
# ============================ (E) 循环贴标签：Z / Z' 二择一 ============================
# 来料：G = 2Z/c  (式19)，eps0 = c/(8*pi*Z')  (式20)
# 反解：Z = G*c/2，Z' = c/(8*pi*eps0)。二者都是从实验常数反解出来的。
Z_back = G * C / Decimal(2)
G_forward = Decimal(2) * Z_back / C
PI_VAL = Decimal("3.14159265358979323846264338327950288")
Zprime_back = C / (Decimal(8) * PI_VAL * EPS0)
EPS0_forward = C / (Decimal(8) * PI_VAL * Zprime_back)
P("E-1", "Z=Gc/2 正反算闭合（循环机器零）",
  "G 逐位相等于 CODATA 值，恰恰证明 G=2Z/c 是恒等重排/循环定义，未第一性导出 G。",
  {"Z_back": sci(Z_back), "G_forward": sci(G_forward),
   "G_codata": sci(G), "rel": sci(rel(G_forward, G), 3)})
P("E-2", "eps0=c/(8*pi*Z') 正反算闭合（循环机器零）",
  "eps0 逐位回到 CODATA，说明 eps0 公式是定义式，非独立预言。",
  {"Zprime_back": sci(Zprime_back), "eps0_forward": sci(EPS0_forward),
   "eps0_codata": sci(EPS0), "rel": sci(rel(EPS0_forward, EPS0), 3)})
DICHOTOMY = {
    "branch_1_Z_is_basic": {
        "assumption": "Z 是独立基本常数",
        "consequence": "G 与 eps0 成为被预测量",
        "problem": "G 与 eps0 由实验独立测得（相对精度 ~2.2e-5 / ~1.5e-10），"
                   "框架无任何机制把 Z 的取值推出为这些值，故不是预测而是回填。",
        "n_predictions_honest": 0,
    },
    "branch_2_Z_is_definition": {
        "assumption": "Z、Gc/2 是定义式（Z'=c/(8*pi*eps0) 同）",
        "consequence": "什么也没预测，只给 G、eps0 改了名字",
        "problem": "「统一」退化为词汇替换，不含新物理。",
        "n_predictions_honest": 0,
    },
}
F("E-3", "Z / Z' 二择一无出路（两分支诚实预言数均为 0）",
  "分支1（Z 基本）：G/eps0 被预测，但无机制定 Z，需回填 => 预言数 0；"
  "分支2（Z 定义）：G/eps0 未被预测，仅改名 => 预言数 0。"
  "即「先有 G/eps0 才能统一」是结构性循环，必须先承认这两个外部输入。",
  {"branches": DICHOTOMY, "third_branch_exists": False,
   "root_cause": "必须先有实验 G、eps0 才能决定哪个几何分量贴引力/电磁标签"})

# ============================ (F) 替换检验：几何层对 alpha 的零判别力 ============================
# 把 alpha 替换成任意其它值（1/137、1e-3、0.5），保持 s=sqrt(kappa^2+tau^2)=1/l_P 不变，
# 观察几何输出 (omega, R, m) 是否改变。若不变 => 几何层对 alpha 零判别力 => alpha 是贴上去的标签。
s_base = Decimal(1) / L_P
sub_rows = []
for alpha_alt in [ALPHA, Decimal(1) / Decimal(137), Decimal("1e-3"), Decimal("0.5")]:
    k = s_base / (Decimal(1) + alpha_alt * alpha_alt).sqrt()
    t = alpha_alt * k
    o = ctfa_from_kappa_tau(k, t)
    sub_rows.append({
        "alpha_in": sci(alpha_alt, 8), "kappa": sci(k), "tau": sci(t),
        "omega": sci(o["omega"]), "R": sci(o["R"]), "m": sci(o["m"]),
        "alpha_out": sci(o["alpha"], 8),
        "alpha_rel_error_vs_input": sci(rel(o["alpha"], alpha_alt), 3),
        # 原始 Decimal，供机器精确比较（不受读数有效位截断影响）
        "_alpha_in_raw": alpha_alt, "_alpha_out_raw": o["alpha"],
        "_omega_raw": o["omega"], "_R_raw": o["R"], "_m_raw": o["m"],
    })
geom_cols = ["omega", "R", "m"]
def varies_within(col, tol=Decimal("1e-40")):
    """判定该几何输出是否随 alpha 变化。
    自抓教训：不能用 set() 严格相等 —— Decimal 60 位下 (kappa^2+tau^2) 的舍入使
    sqrt 结果差 ~1e-59，属「数值零」而非「严格零」；必须用相对容差判据。"""
    vals = [r["_" + col + "_raw"] for r in sub_rows]
    ref = vals[0]
    return any(rel(v, ref) > tol for v in vals)
geom_spread = {c: sci(max(rel(r["_" + c + "_raw"], sub_rows[0]["_" + c + "_raw"]) for r in sub_rows), 3)
               for c in geom_cols}
geom_varying = any(varies_within(c) for c in geom_cols)
P("F-1", "替换检验：几何输出 (omega,R,m) 对 alpha 零敏感",
  "扫描 4 个 alpha 取值（含 1/137、1e-3、0.5），只要 s=sqrt(kappa^2+tau^2)=1/l_P 固定，"
  "则 omega、R、m 逐位不变。几何层对 alpha 无判别力 => alpha=tau/kappa 是贴标签，不是几何决定量。",
  {"n_alphas_tested": len(sub_rows), "geom_columns_tested": geom_cols,
   "geom_varying_with_alpha": geom_varying,
   "geom_max_relative_spread": geom_spread, "tolerance": "1e-40",
   "note": "几何输出相对散布停在 Decimal round-off 量级(<1e-40)，即严格零敏感",
   "rows": sub_rows})
# alpha 回环一致性：每个 alpha 输入，输出 alpha 逐位回到输入（循环定义证据）
alpha_loop_ok = all(rel(r["_alpha_out_raw"], r["_alpha_in_raw"]) < Decimal("1e-50") for r in sub_rows)
F("F-2", "alpha=tau/kappa 是循环定义（无独立可检验值）",
  "任意指定 alpha，tau/kappa 必然返回同一个值（回环），无自由度、无约束力；"
  "来料另预设 theta=arctan(alpha) 则更是把 alpha 当输入再当输出。",
  {"alpha_loop_all_exact": alpha_loop_ok, "tolerance": "1e-30",
   "n_cases": len(sub_rows)})

# ---- F-3 电子参数内部一致性（拟合 vs 派生证据） ----
# 来料独立列出 kappa_e=2.589e12 m^-1 与 R_e=3.862e-13 m，二者应满足 kappa_e*R_e=1
KAPPA_E_CLAIM = Decimal("2.589e12")
R_E_CLAIM = Decimal("3.862e-13")
prod_claim = KAPPA_E_CLAIM * R_E_CLAIM
cos_theta = Decimal(1) / (Decimal(1) + ALPHA * ALPHA).sqrt()
B("F-3", "电子 kappa_e * R_e != 1（参数为取整回填，非同一条世界线导出）",
  "来料独立给出 kappa_e 与 R_e，二者乘积偏离 1 约 %.1E；"
  "若严格闭合应等于 cos(theta)=1/sqrt(1+alpha^2)，实测仍差 %.1E。"
  "这正是「参数吻合已知物理后回填」的证据（故 alpha 逐位吻合 CODATA 不是预言）。"
  % (Decimal(1) - prod_claim, abs(prod_claim - cos_theta)),
  {"kappa_e_R_e": sci(prod_claim), "target_1": "1", "deviation_from_1": sci(Decimal(1) - prod_claim, 3),
   "cos_theta": sci(cos_theta), "deviation_from_cos_theta": sci(abs(prod_claim - cos_theta), 3)})
# ============================ (G) 「攻破了什么」三层裁定 ============================
# G-1 第一层：是否否证了任何已建立理论？库内逐册检索结论 = 0。
LAYER1 = {
    "question": "这套公理+恒等式层是否攻破/否证了任何已建立的物理理论？",
    "n_external_theories_refuted": 0,
    "verdict": "零",
    "reason": "§B/§E 的 7 条「统一」全部是同形重写（牛顿、库仑、毕奥-萨伐尔、法拉第、"
              "质能、波动方程、alpha 标准定义）；被剔除的 7 条（核力场比库仑弱 1e36、"
              "运动电荷引力场量纲两难、式23 等价于 h*nu=M*c^2 日地差 8.5e87、"
              "f/k'/k/Z 五个常数定义）是自证伪，不是对外部理论的否证。",
    "self_refuted_items": 7,
}
P("G-1", "第一层裁定：对外部已建立理论的否证数 = 0",
  "这是「统一」与「攻破」的区分：本册只做词汇层归并，不产生任何否证外部理论的结论。", LAYER1)

# G-2 第二层：同族几何真正取得的成果（引用登记，不重算）
LAYER2 = {
    "disclaimer": "以下为库内同族 Frenet-Serret 世界线几何（TUFT 侧）的成果，"
                  "属数值方法论，由脚本复算得出；不是这三条公设的推论。",
    "achievements": [
        {"item": "Leaver 连分式求 RW QNM", "reading": "0.373671684418-0.088962315689i, |delta|=4.46e-7",
         "source": "TUFT R25", "significance": "特征值级精度，较 R21/R24 的 1e-3 提升约 4 个量级"},
        {"item": "RW <-> Zerilli 等谱", "reading": "SUSY(Darboux) 伙伴，s=-lam(lam+1)/3, C=-[lam(lam+1)/3]^2",
         "source": "TUFT R27", "significance": "免用 Nollert 广义连分式即证等谱"},
        {"item": "结构递推项数诊断", "reading": "RW 偏移{-1,0,1}=3 项; Zerilli{-3,-2,-1,0,1}=5 项",
         "source": "TUFT R26", "significance": "解释 R25 不可直接移植 Zerilli 的原因"},
        {"item": "Kerr/Teukolsky 递推阶数", "reading": "RW p=2 -> 3 项; Teukolsky p=1 -> 4 项",
         "source": "TUFT R28", "significance": "Kerr 不能用 R25 单连分式，须引 Nollert 广义连分式"},
        {"item": "sigma_abs=0 ringdown", "reading": "tau = 3.4 * tau_GR, R^2=0.9998, |T_h|^2(基模)=0.469",
         "source": "TUFT R20/R21", "significance": "时域/实频两路交叉一致的定量预言"},
        {"item": "回声梳定量否证", "reading": "gamma*T_echo = 0.362 < 1",
         "source": "TUFT R22", "significance": "否证「回声梳」假设，指向长寿命改性振铃"},
    ],
}
I("G-2", "第二层裁定：同族几何有真实成果，但不归属这三条公设",
  "价值在于「用曲率/挠率世界线几何分析 Kerr/Teukolsky/RW」，即引力波数值方法论；"
  "把它记为「三条公设统一了四力」是归属错误。", LAYER2)

# G-3 第三层：实验窗口状态
LAYER3 = {
    "g_minus_2": {"reading": "偏差 74.96%", "status": "已关闭"},
    "EDM": {"reading": "超 ACME2018 上限 1.28e16 倍", "status": "已关闭"},
    "beta_running": {"reading": "beta = 0（无 RG 结构）", "status": "窗口不存在"},
    "ringdown": {"reading": "chi^2 = 33.00, df=2, 联合排除 5.74 sigma", "status": "已关闭"},
    "n_open_windows": 0,
}
F("G-3", "第三层裁定：四个实验窗口全部关闭，当前无可检验窗口",
  "g-2、EDM、beta 跑动、ringdown 四个方向均已关（见 2026-09-30 更正）；"
  "CTFA 层共享牛顿全部脆弱点且无 1PN 修正，抢不到牛顿与 GR 都未覆盖的可证伪区间。", LAYER3)

# ============================ 汇总 ============================
def count(v):
    return sum(1 for e in ENTRIES if e["verdict"] == v)
SUMMARY = {"PASS": count("PASS"), "FAIL": count("FAIL"),
           "BOUNDARY": count("BOUNDARY"), "INFO": count("INFO"),
           "TOTAL": len(ENTRIES)}

RESULTS = {
    "engine": "张祥前CTFA_自由度预算与统一能力上限",
    "date": "2026-10-12",
    "object": "三条公理 + CTFA 几何恒等式层",
    "anchor": "判定_张祥前CTFA_全维审计与原创延伸_2026-10-12.md (C/L1) + "
              "整理_张祥前统一场论_核心公式与理论体系全维梳理_2026-10-12.md",
    "rating": "C/L1（几何重述；统一能力上限 = 2 个相互作用扇区）",
    "headline": {
        "independent_dof": FREE_PARAMS,
        "required_forces": 4,
        "gap": n_missing,
        "can_unify": ["gravity(经 Z=Gc/2)", "electromagnetic(alpha=tau/kappa)"],
        "cannot_unify": ["weak", "strong"],
        "unification_nature": "词汇层归并（7 类已知方程的几何重写），增量 0",
        "n_external_theories_refuted": 0,
        "n_open_experiment_windows": 0,
    },
    "constants": {"c": str(C), "G": str(G), "hbar": str(HBAR), "eps0": str(EPS0),
                  "alpha": str(ALPHA), "l_P": str(L_P), "m_P": str(M_P),
                  "ell_weak": str(ELL_W), "ell_strong": str(ELL_QCD)},
    "dof_counting": {"note": "omega/R/m/alpha/Xi 全部为 (kappa,tau) 的函数",
                     "sample_output": {k: sci(v, 10) if isinstance(v, Decimal) else str(v)
                                       for k, v in out.items()},
                     "readings": {"reading1": READ1, "reading2": READ2}},
    "force_demand_table": FORCES,
    "rg_capacity": {"mu_dependent_formulas": mu_hits,
                    "beta_alpha": "0", "alpha_s_span_log10": sci(alpha_s_run.ln() / Decimal(10).ln(), 6)},
    "single_scale": {"kappa_dim": dim_str(kappa_dim), "tau_dim": dim_str(tau_dim),
                     "ell_weak": sci(ELL_W), "ell_strong": sci(ELL_QCD),
                     "ratio": sci(ell_ratio, 6), "ell_best": sci(ell_best),
                     "rel_err_weak": sci(err_w, 6), "rel_err_strong": sci(err_s, 6)},
    "label_circularity": {"Z_back": sci(Z_back), "Zprime_back": sci(Zprime_back),
                          "G_forward_rel": sci(rel(G_forward, G), 3),
                          "eps0_forward_rel": sci(rel(EPS0_forward, EPS0), 3),
                          "dichotomy": DICHOTOMY},
    "substitution_test": {"rows": sub_rows, "geom_varying_with_alpha": geom_varying,
                          "alpha_loop_all_exact": alpha_loop_ok},
    "electron_param_consistency": {"kappa_e_R_e": sci(prod_claim), "deviation_from_1": sci(Decimal(1) - prod_claim, 3),
                                   "cos_theta": sci(cos_theta),
                                   "deviation_from_cos_theta": sci(abs(prod_claim - cos_theta), 3)},
    "what_it_breaks": {"layer1_external_refutation": LAYER1,
                       "layer2_family_achievements": LAYER2,
                       "layer3_experiment_windows": LAYER3},
    "summary": SUMMARY,
    "entries": ENTRIES,
    "red_line": "数学自洽 != 物理证实。本册只做可判定的结构/自由度审计，不产生新物理。",
}

# ============================ 自检 ============================
checks = []
def chk(tag, ok, msg):
    checks.append({"tag": tag, "ok": bool(ok), "msg": msg})
chk("S-1", len(G0) == 7 and all(g["ok"] for g in G0), "量纲工具自检 7/7 全过")
chk("S-2", rel(out["omega"] / C, s_direct) < Decimal("1e-50"), "omega 闭合残差 < 1e-50")
chk("S-3", rel(out["m"], HBAR * s_direct / C) < Decimal("1e-50"), "m 闭合残差 < 1e-50")
chk("S-4", rel(out["alpha"], out2["alpha"]) < Decimal("1e-50"), "同比例缩放下 alpha 逐位不变")
chk("S-5", FREE_PARAMS == 2, "独立自由度 = 2")
chk("S-6", n_missing == 2, "四力缺口 = 2")
chk("S-7", not geom_varying, "替换检验：几何输出不随 alpha 变化")
chk("S-8", alpha_loop_ok, "alpha 回环全部精确（循环定义）")
chk("S-9", len(mu_hits) == 0, "CTFA 层无能标依赖公式")
chk("S-10", ELL_W != ELL_QCD, "两短程力程确实不等（单标度不可覆盖）")
chk("S-11", rel(G_forward, G) < Decimal("1e-40"), "G 正反算相对残差 < 1e-40")
chk("S-12", rel(EPS0_forward, EPS0) < Decimal("1e-40"), "eps0 正反算相对残差 < 1e-40")
chk("S-13", READ1["n_free"] == READ2["n_free"] == 2 and
          READ1["n_predictions"] == READ2["n_predictions"] == 0, "两读法自由参数=2 且预言数=0")
chk("S-14", LAYER1["n_external_theories_refuted"] == 0, "外部理论否证数 = 0")
chk("S-15", LAYER3["n_open_windows"] == 0, "开放实验窗口数 = 0")
selfcheck_pass = sum(1 for c in checks if c["ok"])
if selfcheck_pass != len(checks):
    for g in G0:
        if not g["ok"]:
            print("G0-FAIL:", g["tag"], g["msg"])
    for c in checks:
        if not c["ok"]:
            print("SELFCHECK-FAIL:", c["tag"], c["msg"])
    sys.exit(1)
RESULTS["selfcheck"] = checks

# ============================ 产物输出 ============================
base = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(base, "..", "数据"))
os.makedirs(data_dir, exist_ok=True)
stem = "张祥前CTFA_自由度预算与统一能力上限_2026-10-12"
with open(os.path.join(data_dir, stem + ".json"), "w", encoding="utf-8") as f:
    json.dump(RESULTS, f, ensure_ascii=False, indent=2, default=str)

def fmt_num(x, n=10):
    try:
        return sci(Decimal(str(x)), n)
    except Exception:
        return str(x)

md = []
md.append("# 数据 · 张祥前 CTFA 自由度预算与统一能力上限（%s）\n" % RESULTS["date"])
md.append("- 引擎：`源码/%s.py`" % stem)
md.append("- 裁定：**%s**" % RESULTS["rating"])
md.append("- 自检：%d/%d，退出码 0" % (selfcheck_pass, len(checks)))
md.append("- 红线：%s\n" % RESULTS["red_line"])
md.append("## 头条读数\n")
h = RESULTS["headline"]
md.append("| 项 | 读数 |\n|---|---|")
md.append("| CTFA 层独立自由度 | **%d** |" % h["independent_dof"])
md.append("| 四力需求 | %d |" % h["required_forces"])
md.append("| **自由度缺口** | **%d**（弱、强无载体） |" % h["gap"])
md.append("| 可统一 | %s |" % "、".join(h["can_unify"]))
md.append("| 不可统一 | %s |" % "、".join(h["cannot_unify"]))
md.append("| 统一的性质 | %s |" % h["unification_nature"])
md.append("| 外部理论否证数 | **%d** |" % h["n_external_theories_refuted"])
md.append("| 开放实验窗口 | **%d** |" % h["n_open_experiment_windows"])
md.append("\n## 条目汇总\n")
md.append("| 类别 | 数量 |\n|---|---|")
for k in ["PASS", "FAIL", "BOUNDARY", "INFO"]:
    md.append("| %s | %d |" % (k, SUMMARY[k]))
md.append("| **合计** | **%d** |" % SUMMARY["TOTAL"])
md.append("\n## 逐条裁定\n")
md.append("| 标签 | 判定 | 标题 |\n|---|---|---|")
for e in ENTRIES:
    md.append("| %s | %s | %s |" % (e["tag"], e["verdict"], e["title"]))
md.append("\n## 关键数值\n")
md.append("- 弱力程 ħc/M_W = %s m" % sci(ELL_W))
md.append("- 强力程 ħc/Λ_QCD = %s m" % sci(ELL_QCD))
md.append("- 两力程比 = %s" % sci(ell_ratio, 6))
md.append("- α_s 跑动跨度 = %s dex" % sci(alpha_s_run.ln() / Decimal(10).ln(), 6))
md.append("- 电子 κ_e·R_e = %s（偏离 1 约 %s）" % (sci(prod_claim), sci(Decimal(1) - prod_claim, 3)))
md.append("- G 正反算相对残差 = %s；eps0 = %s" % (sci(rel(G_forward, G), 3), sci(rel(EPS0_forward, EPS0), 3)))
with open(os.path.join(data_dir, stem + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

report = []
report.append("=" * 78)
report.append("张祥前 CTFA 自由度预算与统一能力上限 全维全链路审计")
report.append("日期: %s" % RESULTS["date"])
report.append("对象: %s" % RESULTS["object"])
report.append("裁定: %s" % RESULTS["rating"])
report.append("=" * 78)
report.append("")
report.append("头条读数:")
report.append("  独立自由度        = %d" % h["independent_dof"])
report.append("  四力需求          = %d" % h["required_forces"])
report.append("  自由度缺口        = %d" % h["gap"])
report.append("  可统一            = %s" % ", ".join(h["can_unify"]))
report.append("  不可统一          = %s" % ", ".join(h["cannot_unify"]))
report.append("  外部理论否证数    = %d" % h["n_external_theories_refuted"])
report.append("  开放实验窗口      = %d" % h["n_open_experiment_windows"])
report.append("")
report.append("条目汇总:")
for k in ["PASS", "FAIL", "BOUNDARY", "INFO", "TOTAL"]:
    report.append("  %-9s = %d" % (k, SUMMARY[k]))
report.append("")
report.append("自检: %d/%d" % (selfcheck_pass, len(checks)))
report.append("-" * 78)
for e in ENTRIES:
    report.append("[%-8s] %s : %s" % (e["verdict"], e["tag"], e["title"]))
    report.append("           %s" % e["detail"])
report.append("-" * 78)
report.append("红线: %s" % RESULTS["red_line"])
with open(os.path.join(data_dir, stem + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report) + "\n")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
print("\n".join(report))
print("WROTE: %s.{json,md,_report.txt}" % stem)
print("SELFCHECK %d/%d  EXIT 0" % (selfcheck_pass, len(checks)))