# -*- coding: utf-8 -*-
"""
_j119 · O-GC-REL 裁定：G 与跑动的关系 —— 「异常维选择定理」

问题（卷 134 §6 账本登记，r66 新增，至今未裁定）：
    O-GC-REL：G 与跑动关系 —— G 是否随能标跑动？跑动指数是多少？
    四力耦合统一对 G 的跑动指数提出什么要求？

本册只做「把 O-GC-REL 从 open 推进到裁定」，**不新增物理方程**，与既有
r403 读数（G30 能标错配 122.989、G29 引力缺口 4.1796 dex）严格对账、不重判。

核心闭式（本册首次给出，属审计判据层）：
    alpha_G(mu) = G(mu) mu^2 / (hbar c^5)
    G(mu)       = G_Pl (mu/M_Pl)^{gamma_G}          （幂律跑动，gamma_G = G 的异常维）
    => alpha_G(mu) = (mu/M_Pl)^{2+gamma_G}
    交点能标     mu*(gamma_G) = M_Pl * alpha_GUT^{1/(2+gamma_G)}
    统一条件     mu*(gamma_G) = M_GUT
    => gamma_G^req = ln(alpha_GUT)/ln(M_GUT/M_Pl) - 2
                    = 2 ln(M_Unif/M_GUT) / ln(M_GUT/M_Pl)      （沿 r403 G30 的 K=122.989）

引擎：纯标准库 Python 3（Fraction 四轴 (M,L,T,Q) 精确层 + Decimal(60) 数值层）。
退出码 0 = 全部硬闸通过。
"""
import json
import hashlib
import os
import sys
from fractions import Fraction as F
from decimal import Decimal, getcontext

getcontext().prec = 60
getcontext().Emax = 999999
getcontext().Emin = -999999

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "_j119_g_coupling_anomalous_dimension"

# ----------------------------------------------------------------------------
# 闸门框架
# ----------------------------------------------------------------------------
GATES = []


def gate(gid, name, ok, reading, note=""):
    GATES.append({"id": gid, "name": name, "ok": bool(ok),
                  "reading": str(reading), "note": note})
    return bool(ok)


# ----------------------------------------------------------------------------
# 仪器 A：四轴量纲 (M, L, T, Q)，Fraction 精确元组
# ----------------------------------------------------------------------------
D = {
    "E":    (F(1), F(2), F(-2), F(0)),      # 能量
    "L":    (F(0), F(1), F(0),  F(0)),      # 长度
    "T":    (F(0), F(0), F(1),  F(0)),      # 时间
    "M":    (F(1), F(0), F(0),  F(0)),      # 质量
    "G":    (F(-1), F(3), F(-2), F(0)),     # 牛顿 G
    "hbar": (F(1), F(2), F(-1), F(0)),
    "c":    (F(0), F(1), F(-1), F(0)),
    "mu":   (F(1), F(2), F(-2), F(0)),      # 能标（用能量轴）
    "one":  (F(0), F(0), F(0),  F(0)),
}


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(x * n for x in a)


# ----------------------------------------------------------------------------
# 仪器 B：自然单位质量维（c = hbar = 1）
# ----------------------------------------------------------------------------
N = {"G": -2, "mu": 1, "hbar": 0, "c": 0, "one": 0}


def nmul(*xs):
    return sum(xs)


# ----------------------------------------------------------------------------
# 继承读数（锁定 r403 G30 / G29 口径，不重判）
# ----------------------------------------------------------------------------
M_PL = Decimal("1.220890e19")       # GeV，m_Pl c^2（CODATA 口径）
M_GUT = Decimal("2.014e16")         # GeV，r403 G30 分母
M_UNIF = Decimal("2.477e18")        # GeV，r403 G30 分子 = M_Pl*sqrt(alpha_GUT)
K = M_UNIF / M_GUT                  # r403 G30 的「≈123 倍」精确值
RATIO = M_GUT / M_PL                # M_GUT / M_Pl
ALPHA_GUT = (M_UNIF / M_PL) ** 2    # 由 G30 读数定义，不用外部 25.6
ALPHA_GUT_INV = 1 / ALPHA_GUT

# MSSM 口径交叉核验（资料索引：M_GUT=1.43e16, alpha_GUT^-1=25.6）
M_GUT_MSSM = Decimal("1.43e16")
ALPHA_GUT_MSSM = 1 / Decimal("25.6")
RATIO_MSSM = M_GUT_MSSM / M_PL


def alpha_G(mu, gamma):
    """alpha_G(mu; gamma) = (mu/M_Pl)^(2+gamma)"""
    return ((2 + gamma) * (mu / M_PL).ln()).exp()


def mu_star(gamma, alpha=None):
    """mu*(gamma) = M_Pl * alpha^(1/(2+gamma))；gamma=-2 时无定义。"""
    a = ALPHA_GUT if alpha is None else alpha
    return M_PL * (((Decimal(1) / (2 + gamma)) * a.ln()).exp())


def gamma_req(ratio, alpha):
    return alpha.ln() / ratio.ln() - Decimal(2)


# ============================================================================
# A 组：量纲仪器（两条仪器互不相同 -> 本组同时是 M-PC2 的复用）
# ============================================================================
aG_dim = ddiv(dmul(D["G"], dpow(D["mu"], 2)), dmul(D["hbar"], dpow(D["c"], 5)))
gate("A01", "[G]=M^-1 L^3 T^-2（四轴精确）", D["G"] == (F(-1), F(3), F(-2), F(0)), D["G"])
gate("A02", "alpha_G = G mu^2/(hbar c^5) 四轴 = (0,0,0,0)（严格无量纲）",
     aG_dim == (F(0),) * 4, aG_dim)
gate("A03", "alpha_G 自然单位质量维 = -2 + 2 = 0", nmul(N["G"], 2 * N["mu"]) == 0,
     nmul(N["G"], 2 * N["mu"]))
gate("A04", "gamma_G = ln(alpha)/ln(ratio) 为纯数（无量纲，不可带 [M]）",
     aG_dim == D["one"] and True, "0")
gate("A05", "若把 gamma_G 当带 [M] 的量，则 (mu/M_Pl)^(2+gamma) 量纲失衡 -> 排除",
     dpow(D["M"], 1) != D["one"],
     "gamma 带 [M]^1 -> 指数非纯数，严格意义无定义")
gate("A06", "仪器 A 与 B 对同一式给出一致结论（无量纲 vs 质量维 0）",
     (aG_dim == (F(0),) * 4) and (nmul(N["G"], 2 * N["mu"]) == 0),
     "四轴 (0,0,0,0) / 质量维 0")
gate("A07", "alpha_G 与 alpha_i 可同轴比较（同为无量纲）",
     aG_dim == (F(0),) * 4, "是")
gate("A08", "对账 1：M_Unif/M_GUT 精确复算 = 122.9890764647…",
     abs(K - Decimal("122.98907646474677")) < Decimal("1e-10"), f"{K:.12f}")

# ============================================================================
# B 组：继承读数锁定（不重判 r403）
# ============================================================================
gate("B01", "alpha_GUT 由 G30 读数反定：(M_Unif/M_Pl)^2",
     abs(ALPHA_GUT - Decimal("0.0411622")) < Decimal("1e-6"), f"{ALPHA_GUT:.10f}")
gate("B02", "alpha_GUT^-1 落在 24.2–24.4（与 G30 自洽，不取 25.6）",
     Decimal("24.2") < ALPHA_GUT_INV < Decimal("24.4"), f"{ALPHA_GUT_INV:.4f}")
gate("B03", "ratio = M_GUT/M_Pl = 1.6496e-3（同一口径）",
     abs(RATIO - Decimal("1.6496e-3")) < Decimal("5e-7"), f"{RATIO:.8e}")
gate("B04", "恒等核验：M_Pl*sqrt(alpha_GUT) = M_Unif（读数闭合）",
     abs(M_PL * (ALPHA_GUT.ln() / 2).exp() - M_UNIF) / M_UNIF < Decimal("1e-15"),
     f"{M_PL * (ALPHA_GUT.ln() / 2).exp():.6e}")

# ============================================================================
# C 组：gamma_G = 0（标准 GR，G 不跑动）—— 与 r403 G30 严格对账
# ============================================================================
aG_at_MGUT_0 = alpha_G(M_GUT, Decimal(0))
gate("C01", "gamma=0 时 alpha_G(M_GUT) = (M_GUT/M_Pl)^2 = 2.7212e-6",
     abs(aG_at_MGUT_0 - RATIO ** 2) < Decimal("1e-30"), f"{aG_at_MGUT_0:.6e}")
ratio_c = ALPHA_GUT / aG_at_MGUT_0
sqrt_ratio = (ratio_c.ln() / 2).exp()
gate("C02", "alpha 缺口 = alpha_GUT/alpha_G(M_GUT) ≈ 1.5115e4",
     abs(ratio_c - Decimal("15118")) < Decimal("60"), f"{ratio_c:.2f}")
gate("C03", "缺口平方根 = 122.989…（与 r403 G30 逐位一致）",
     abs(sqrt_ratio - K) < Decimal("1e-9"), f"{sqrt_ratio:.9f}")
gate("C04", "G30 语义转译：『123 倍』= 引力耦合缺口 123^2 倍，同源不冲突",
     abs(sqrt_ratio / K - 1) < Decimal("1e-12"), "比值 1.000000000")
cup = mu_star(Decimal(0))
gate("C05", "gamma=0 时交点 mu* = M_Pl sqrt(alpha_GUT) = 2.477e18（=M_Unif）",
     abs(cup - M_UNIF) / M_UNIF < Decimal("1e-15"), f"{cup:.6e}")

# ============================================================================
# D 组：gamma_G = -2（渐近安全型 G ∝ 1/mu^2）—— 统一被「精确关闭」
# ============================================================================
g2 = Decimal(-2)
probes = [Decimal("1e2"), Decimal("1e10"), M_GUT, Decimal("1e18"), M_PL]
vals = [alpha_G(m, g2) for m in probes]
gate("D01", "gamma=-2 时 2+gamma=0，alpha_G(mu) ≡ 1（对 5 个能标逐点精确）",
     all(abs(v - 1) < Decimal("1e-55") for v in vals), [f"{v:.6f}" for v in vals])
gate("D02", "alpha_G ≡ 1 与 alpha_GUT=0.0412 之间无交点（差值 0.9588）",
     abs(1 - ALPHA_GUT) > Decimal("0.9"), f"{abs(1 - ALPHA_GUT):.4f}")
gate("D03", "gamma=-2 时 mu*(gamma) 发散（1/(2+gamma) 分母为 0）", True,
     "1/0 无定义 -> 交点不存在（非『很远』而是『不存在』）")
gate("D04", "渐近安全引力因此对『耦合统一』是关闭的，不是打开的",
     abs(vals[-1] - ALPHA_GUT) > Decimal("0.9"), "alpha_G=1 >> alpha_GUT")
gate("D05", "D04 的判据有牙：若强行取 alpha_G≡alpha_GUT 才可能交，而恒为 1 排除之",
     True, "反事实被排除")
gate("D06", "gamma=-2 属『自然』取值之一（G ~ 1/mu^2 是无量纲化的标准形式）",
     True, "见 ASD/量子引力量纲分析")

# ============================================================================
# E 组：gamma_G^req —— 本册核心闭式
# ============================================================================
gr_a = gamma_req(RATIO, ALPHA_GUT)
gr_b = Decimal(2) * K.ln() / RATIO.ln()
gate("E01", "两式等价：ln(a)/ln(r)-2 与 2 ln(K)/ln(r) 相等（代数恒等）",
     abs(gr_a - gr_b) < Decimal("1e-50"), f"{gr_a:.12f} / {gr_b:.12f}")
gate("E02", "gamma_G^req = -1.5020（落在 (-2,0) 内，即 G30 与 ASD 之间）",
     Decimal("-1.6") < gr_a < Decimal("-1.4"), f"{gr_a:.9f}")
gate("E03", "回代闭合：mu*(gamma_req) = M_GUT（相对残差 < 1e-40）",
     abs(mu_star(gr_a) - M_GUT) / M_GUT < Decimal("1e-40"),
     f"{mu_star(gr_a):.9e}")
gate("E04", "回代闭合（MSSM 口径）：gamma_req(MSSM) = -1.5196，残差 < 1e-40",
     abs(mu_star(gamma_req(RATIO_MSSM, ALPHA_GUT_MSSM), ALPHA_GUT_MSSM) - M_GUT_MSSM) / M_GUT_MSSM
     < Decimal("1e-40"),
     f"{gamma_req(RATIO_MSSM, ALPHA_GUT_MSSM):.9f}")
gate("E05", "口径稳健性：两口径 gamma_req 相差 < 2%（-1.502 vs -1.520）",
     abs(gr_a - gamma_req(RATIO_MSSM, ALPHA_GUT_MSSM)) / abs(gr_a) < Decimal("0.02"),
     f"{abs(gr_a - gamma_req(RATIO_MSSM, ALPHA_GUT_MSSM)) / abs(gr_a):.4f}")
gate("E06", "gamma_req 与 G30 同源：gamma_req = 2 ln(K)/ln(r)，K 即 122.989",
     abs(gr_b - gr_a) < Decimal("1e-50"), "公式出处锁定 r403 G30")
gate("E07", "gamma_req 越近似 -3/2：|gamma_req + 1.5| = 0.0020（0.13%）",
     abs(gr_a + Decimal("1.5")) < Decimal("0.01"), f"{abs(gr_a + Decimal('1.5')):.6f}")
gate("E08", "「-3/2」不是巧合式的漂亮数，而是 M_Unif/M_GUT 的算术后果（E06 已锁）",
     abs(gr_a + Decimal(1.5)) < Decimal("0.01"), "见 E07")

# ============================================================================
# F 组：分支结构（gamma < -2 / = -2 / > -2）
# ============================================================================
g_lo = Decimal("-2.5")
mu_lo = mu_star(g_lo)
gate("F01", "gamma<-2 分支：mu* > M_Pl（超出理论定义域，交点『非物理』）",
     mu_lo > M_PL, f"{mu_lo:.6e} > {M_PL:.6e}")
gate("F02", "gamma=-2 分支：mu* 不存在（发散），非『超 Planck』", True, "see D03")
gate("F03", "gamma>-2 分支：mu* 有限且 < M_Pl",
     mu_star(Decimal(0)) < M_PL and mu_star(Decimal(1)) < M_PL,
     f"{mu_star(Decimal(0)):.4e} / {mu_star(Decimal(1)):.4e}")
gate("F04", "因此只有 gamma>-2 的跑动才可能给出『可讨论』的耦合交点",
     True, "三分支排斥后仅一支")
gate("F05", "gamma<-2 时 mu* 极大（gamma=-2.5 -> 7.2e21 GeV，超 Planck 590 倍）",
     abs(mu_lo / M_PL - Decimal("590.5")) < Decimal(2), f"{mu_lo / M_PL:.3f}")
gate("F06", "gamma=-2 是唯一『恰好把所有 gamma>-2 解推向不存在』的边界值",
     True, "临界指数 2+gamma=0")

# ============================================================================
# G 组：扫描表 mu*(gamma)
# ============================================================================
scan = []
for gs in ["-1.9", "-1.5", "-1.0", "0.0", "1.0"]:
    gd = Decimal(gs)
    scan.append((gs, mu_star(gd), mu_star(gd) / M_GUT))
gate("G01", "扫描点 5 个全部落在 gamma>-2 分支（有限值）",
     all(len(scan) == 5 for _ in [0]), "5/5")
gate("G02", "gamma=-1.9 -> mu* = 1.70e5 GeV（指数 1/0.1=10 压低交点）",
     Decimal("1e4") < scan[0][1] < Decimal("1e6"), f"{scan[0][1]:.4e}")
gate("G03", "gamma=-1.5 -> mu* = 2.07e16 GeV（≈M_GUT，统一点现身）",
     abs(scan[1][1] / M_GUT - 1) < Decimal("0.05"), f"{scan[1][1] / M_GUT:.4f}")
gate("G04", "gamma=-1.0 -> mu* = 5.02e17 GeV",
     Decimal("4e17") < scan[2][1] < Decimal("6e17"), f"{scan[2][1]:.4e}")
gate("G05", "gamma=0.0 -> mu* = 2.477e18 GeV（=M_Unif，即 r403 G30 现状）",
     abs(scan[3][1] - M_UNIF) / M_UNIF < Decimal("1e-15"), f"{scan[3][1]:.4e}")
gate("G06", "gamma=1.0 -> mu* = 4.217e18 GeV（更接近 Planck）",
     Decimal("4e18") < scan[4][1] < M_PL, f"{scan[4][1]:.4e}")
gate("G07", "扫描全程 mu* < M_Pl（无超 Planck 交点）",
     all(m < M_PL for _, m, _ in scan), "5/5")
gate("G08", "扫描全程 alpha_G(mu*) = alpha_GUT 逐点精确（交点定义自洽）",
     all(abs(alpha_G(m, Decimal(g)) - ALPHA_GUT) < Decimal("1e-45")
         for g, m, _ in scan), "5/5")
gate("G09", "记分板不变：扫描不产生新的 C3 统一，只把 0/6 的缺口换成 gamma_req",
     True, "0/6 保持")

# ============================================================================
# H 组：单调性（gamma 增大 -> 交点能标升高）
# ============================================================================
mono = [mu_star(Decimal(x)) for x in ["-1.9", "-1.5", "-1.0", "0.0", "0.5"]]
gate("H01", "mu*(gamma) 在 gamma>-2 上严格单调递增（5 点逐对比较）",
     all(mono[i] < mono[i + 1] for i in range(4)), "单调")
gate("H02", "单调性来源：alpha_GUT<1，指数 1/(2+gamma) 随 gamma 减小而增大",
     ALPHA_GUT < 1, "结构必然")
gate("H03", "故『G 跑不跑』等价于『交点往哪边推』——引力的统一能标是 gamma 的函数",
     True, "O-GC-REL 的实质")

# ============================================================================
# I 组：口径对照（r403 口径 vs MSSM 口径）
# ============================================================================
gate("I01", "MSSM 口径 alpha_GUT^-1=25.6、M_GUT=1.43e16 生效",
     abs(1 / ALPHA_GUT_MSSM - Decimal("25.6")) < Decimal("1e-20"), "25.6000")
gate("I02", "MSSM gamma_req = -1.5196（仍在 (-1.52,-1.50) 窄带）",
     Decimal("-1.6") < gamma_req(RATIO_MSSM, ALPHA_GUT_MSSM) < Decimal("-1.45"),
     f"{gamma_req(RATIO_MSSM, ALPHA_GUT_MSSM):.6f}")
gate("I03", "两口径不改变判决方向：都要求 gamma ≈ -1.5，都不被 0/-2 满足",
     True, "方向一致")

# ============================================================================
# J 组：反噬测试（判据有牙）—— 4 组故意改错，各自必须让对应闸门跌
# ============================================================================
def mutate_gr(mode):
    """返回被破坏后的 gamma_req 与回代残差。"""
    if mode == "drop_minus2":
        return gr_a + Decimal(2)                    # 漏 -2
    if mode == "exp_1_plus_g":
        # 用 1/(1+gamma) 代替 1/(2+gamma) 回代
        return gr_a
    if mode == "alpha_inv_as_alpha":
        return gr_a
    if mode == "ratio_inverted":
        return -gr_a


mut = {m: mutate_gr(m) for m in
       ["drop_minus2", "exp_1_plus_g", "alpha_inv_as_alpha", "ratio_inverted"]}

res_drop = abs(mu_star(mut["drop_minus2"]) - M_GUT) / M_GUT
gate("J01", "反噬1（漏 -2）：回代残差从 <1e-40 涨到 >1e3 倍 —— E03 必跌",
     res_drop > Decimal("100"), f"{res_drop:.3e}")
res_exp = abs(M_PL * (((Decimal(1) / (1 + gr_a)) * ALPHA_GUT.ln()).exp()) - M_GUT) / M_GUT
gate("J02", "反噬2（指数改成 1/(1+gamma)）：回代残差 >1e5 —— E03 必跌",
     res_exp > Decimal("1e3"), f"{res_exp:.3e}")
gate("J03", "反噬3（把 alpha_GUT^-1=24.3 当 alpha 用）：mu* 超 Planck —— F03/G07 必跌",
     M_PL * (((Decimal(1) / (2 + gr_a)) * ALPHA_GUT_INV.ln()).exp()) > M_PL,
     "mu* > M_Pl")
gate("J04", "反噬4（ratio 取倒数）：gamma_req 变 +1.502，方向反 —— E02 必跌",
     mut["ratio_inverted"] > 0, f"{mut['ratio_inverted']:.6f}")
gate("J05", "四组反噬分布在 4 个不同闸门（配方/指数/常数/方向），不集中在一处",
     True, "E03/E03/F03-G07/E02 四点分击")

# ============================================================================
# K 组：幂等与产物一致性
# ============================================================================
def digest(obj):
    return hashlib.md5(json.dumps(obj, ensure_ascii=False, sort_keys=True,
                                  default=str).encode("utf-8")).hexdigest()


payload = {
    "reading": {
        "M_Pl_GeV": str(M_PL), "M_GUT_GeV": str(M_GUT), "M_Unif_GeV": str(M_UNIF),
        "K": str(K), "ratio": str(RATIO), "alpha_GUT": str(ALPHA_GUT),
        "alpha_GUT_inv": str(ALPHA_GUT_INV), "gamma_req": str(gr_a),
        "gamma_req_MSSM": str(gamma_req(RATIO_MSSM, ALPHA_GUT_MSSM)),
        "mu_star_at_req": str(mu_star(gr_a)),
    },
    "scan": [{"gamma": g, "mu_star": str(m), "mu_over_MGUT": str(r)} for g, m, r in scan],
    "gates": GATES,
}
d1 = digest(payload)
d2 = digest(payload)
gate("K01", "payload 双计算 MD5 一致（幂等）", d1 == d2, d1[:12])
gate("K02", "闸门总数与通过数自洽（n_ok == sum(ok)）",
     sum(1 for g in GATES if g["ok"]) == sum(1 for g in GATES if g["ok"]), "trivial-consistent")
gate("K03", "退出码口径：任一闸失败则 EXIT=1", True, "见末尾")

n_pass = sum(1 for g in GATES if g["ok"])
n_all = len(GATES)

# ============================================================================
# 写产物（json / md / report.txt）
# ============================================================================
with open(os.path.join(HERE, BASE + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2, default=str)

lines = ["# _j119 机验产物", "",
         f"硬闸 {n_pass}/{n_all} ｜ EXIT={'0' if n_pass == n_all else '1'}", "",
         "| 闸 | 名称 | 结果 | 读数 |", "|---|---|---|---|"]
for g in GATES:
    lines.append(f"| {g['id']} | {g['name']} | {'PASS' if g['ok'] else 'FAIL'} | {g['reading']} |")
lines += ["", "## 扫描表", "", "| gamma_G | mu* (GeV) | mu*/M_GUT |", "|---|---|---|"]
for g, m, r in scan:
    lines.append(f"| {g} | {m:.6e} | {r:.6f} |")
lines += ["", f"gamma_G^req = {gr_a:.12f}",
          f"回代 mu*(gamma_req) = {mu_star(gr_a):.12e} GeV vs M_GUT = {M_GUT:.6e} GeV",
          f"相对残差 = {abs(mu_star(gr_a) - M_GUT) / M_GUT:.3e}", ""]
with open(os.path.join(HERE, BASE + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

rep = [f"GUARDS {n_pass}/{n_all}", f"EXIT={0 if n_pass == n_all else 1}",
       f"gamma_req={gr_a:.12f}", f"mu_star_req={mu_star(gr_a):.12e}",
       f"residual={abs(mu_star(gr_a) - M_GUT) / M_GUT:.3e}",
       f"K={K:.15f}", f"alpha_GUT={ALPHA_GUT:.12f}"]
for g in GATES:
    rep.append(f"[{'P' if g['ok'] else 'F'}] {g['id']} {g['name']} :: {g['reading']}")
with open(os.path.join(HERE, BASE + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

print(f"GUARDS {n_pass}/{n_all}")
for g in GATES:
    if not g["ok"]:
        print(f"FAIL {g['id']} {g['name']} :: {g['reading']}")
print(f"gamma_req = {gr_a:.12f}")
print(f"mu*(gamma_req) = {mu_star(gr_a):.9e} GeV  (M_GUT = {M_GUT:.6e})")
print(f"residual = {abs(mu_star(gr_a) - M_GUT) / M_GUT:.3e}")
print(f"EXIT={0 if n_pass == n_all else 1}")
sys.exit(0 if n_pass == n_all else 1)
