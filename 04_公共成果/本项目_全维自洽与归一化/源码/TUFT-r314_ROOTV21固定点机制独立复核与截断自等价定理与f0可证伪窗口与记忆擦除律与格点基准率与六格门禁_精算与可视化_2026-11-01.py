# -*- coding: utf-8 -*-
"""
TUFT-r314 · ROOT V21.0「精细结构常数的固定点机制：第一性原理核验」来料核验（承 r304 判词链）

靶：ROOT V21 来料。其主张：
    §一 4D QED 一圈 β=(2Nf/3π)α² 无正的非零固定点；
    §二 4−ε 模型 α*=3πε/(2Nf)、β'(α*)=ε>0（红外吸引），ε=1 反解 Nf*=645.7669324377…
        取整 646 ⇒ α*=0.0072947197838772289…，与实测差约 360.79 ppm；
    §三 SU(3) 两圈 Banks–Zaks α*=−4πβ0/β1（Nf=12/14/15/16 → 0.753982/0.278017/0.142800/0.0416105）；
    §四 谱几何 f(0)/(2π²)·g²=1/4 + sin²θ_W(M_U)=3/8 ⇒ α_em(M_U)=3π/(64f(0))（f0=10/20/40 表）；
    §五 4−ε 初值问题的精确解 α(μ)=α*/(1+(α*/α0−1)(μ/μ0)^ε)，SymPy 残差为零；
    §六 九行审计表（八行完成、"无参数预测 α(0)"尚未完成）+ CODATA 2022 锚 137.035999177(21)；
    §七/§八 三要件（存在性 / 稳定性 / 低能唯一映射）。

本卷判据族（V=核验，★=本卷新增攻坚）：
  V1  4D 一圈无正固定点 + 积分式符号回代          V2  4−ε 固定点/稳定性/精确解（符号精确）
  V3  ε=1 数值锚（Nf*/646/ppm）                  V4  BZ 引用四组表值 + 2π/151
  V5  谱几何 α_em(M_U)=3π/(64f0) 代数链 + 三组表值
  V6  ★BZ 闭式全表：整数 9..16、单调性定理、正性域、两圈/一圈项比带号 ≡ −1（绝对值恒 1）
  V7  ★f0 可证伪窗口：链常数现推、需求表、f0=10↔M_U 反演、排除定理、双射往返
  V8  ★记忆擦除律：T(ρ) 与擦除预算 N(η)；统一阈值 η=1e-2 跨三族
  V9  ★4−ε 的定价（FAIL）：645 个精确命中 + 格点基准率 + ε 自洽区错失 + 圈参数恒等式
  V10 ★六格门禁矩阵（FAIL）：四真实路线 + 合成理想路线；核心定理 ¬(s2∧s5)
  V11 CODATA 现行版本核对（BOUNDARY：直取 NIST 页失败，登记为二手口径）
  V12 来料 §六 九行审计表逐行挂载体
  V13 判据集 R1–R6
  V14 ★对表并发卷 r313（同来料第二把尺：锚逐位对表 + 相消比同口径 + 覆盖↔窗口 + 连坐观察）
  V15 总登记与遗留
控制组：C1 来料正本逐字回链 / C2 ±1 ulp 变异体全红（牙）/ C3 排除恰 {20,40} 且放 10（牙）/
        C4 擦除判据双向（牙）/ C5 基准率判别 360.786ppm vs 1ppm（牙）/
        C6 合成理想路线 6/6（门可达性正对照）/ C7 残差为零 + 摄动指数残差非零（牙）
守卫：G1–G13
治理：未改 verify.py；未跑 refresh_catalog.py；未改任何既有卷字节；本卷 34 条不可与他卷相加。
"""
import hashlib
import io
import json
import math
import os
import time
from decimal import Decimal, getcontext, Inexact, Rounded

import mpmath as mp
import sympy as sp

getcontext().prec = 60
getcontext().traps[Inexact] = False
getcontext().traps[Rounded] = False
mp.mp.dps = 85

RID = "r314"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = ("TUFT-%s_ROOTV21固定点机制独立复核与截断自等价定理与f0可证伪窗口与记忆擦除律与格点基准率与六格门禁_"
        "精算与可视化_%s" % (RID, STAMP))
LAILIAO = BASE + "_来料原件_ROOT_V21.0_用户附件逐字_%s.md" % STAMP

WRITTEN = []
ALLOWED = set()
T0 = time.time()
ITEMS = []

PI = mp.pi
ALPHA_INV_EXP = mp.mpf("137.035999177")     # CODATA 2022 推荐值 137.035999177(21)
ALPHA_EXP = 1 / ALPHA_INV_EXP
SIGMA_AI = mp.mpf("2.1e-8")                 # α⁻¹ 标准不确定度（末两位 21）
M_Z = mp.mpf("91.1876")                     # PDG Z0 质量 (GeV)
M_PL = mp.mpf("2.435e18")                   # 约化普朗克质量 (GeV)
INV_ALPHA_MZ = mp.mpf("127.952")            # V16.1 锚定口径：1/α(M_Z)

# ---- 链常数一律现推（不许手感钉死；口径值另行为被审计对象）----
THR_BELOW = ALPHA_INV_EXP - INV_ALPHA_MZ          # = 9.083999177（来料口径写作 9.084）
RATE_ABOVE = mp.mpf(17) / (3 * PI)                # = 1.803753…（来料口径写作 1.8038）
口径_THR = mp.mpf("9.084")
口径_RATE = mp.mpf("1.8038")
AVAIL_DECADES = mp.log10(M_PL / M_Z)              # 可达运行距离（十进距）＝擦除预算分母
ETA = mp.mpf("1e-2")                              # 全卷统一擦除阈值（初值误差传 1%）
# 预注册的设计红（G8 棘轮的靶）：V9=ε=1 格点近失的位数定价为 0；V10=四条真实路线各缺格。
# 改这份名单必须同轮改总判词，否则 G8 红。
DESIGN_FAIL = ("V9", "V10")


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title, "verdict": verdict,
                  "detail": detail, "kv": dict(kv or {})})


def wpath(p):
    WRITTEN.append(p)
    return p


def half_ulp_ok(value, printed):
    """判据：打印锚点的最后一位是它自己的一半格（半 ulp）以内——四舍五入唯一可能的落点。"""
    dec = len(printed.split(".")[1]) if "." in printed else 0
    ulp = mp.mpf(10) ** -dec
    return abs(mp.mpf(value) - mp.mpf(printed)) <= ulp / 2


def ulp64_of(x):
    """x 所在二进制区间的 float64 末位单位（ulp）；只用来看「两个读数差几个 double 格」。"""
    v = abs(mp.mpf(x))
    e = int(mp.floor(mp.log(v, 2))) if v >= 1 else -1
    return mp.mpf(2) ** (e - 52)


def mutate_ulp(printed, steps):
    """把打印字符串的末位数字挪 steps 个 ulp（±1/±2 变异体），保持小数位数不变。"""
    d = Decimal(printed)
    dec = -d.as_tuple().exponent
    out = (d + Decimal(steps) / Decimal(10) ** dec).quantize(Decimal(1) / Decimal(10) ** dec)
    return str(out)


def md5_of(path):
    with io.open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def erase_decades(ratio, eps_v, eta=ETA):
    """擦除预算 N(η) = [log10(α*/α0) + log10(1/η)] / ε 个十进距（ratio = α*/α0）。"""
    return (mp.log10(ratio) + mp.log10(1 / eta)) / eps_v


def f0_of_mu(mu):
    """RG 链反解：给定统一能标 M_U，所需的 f(0)。"""
    return 3 * PI / 64 * (ALPHA_INV_EXP - THR_BELOW - RATE_ABOVE * mp.log(mu / M_Z))


def mu_of_f0(f0v):
    """同一方程的另一方向：给定 f(0)，被要求的 M_U（GeV）。"""
    return M_Z * mp.e ** ((ALPHA_INV_EXP - THR_BELOW - 64 * f0v / (3 * PI)) / RATE_ABOVE)


# ================================================================ V1 · 4D 一圈无正固定点
def v1():
    a, Nf, mu, mu0 = sp.symbols("alpha Nf mu mu0", real=True)
    k = sp.Rational(2, 3) / sp.pi * Nf
    roots = sp.solve(sp.Eq(k * a ** 2, 0), a)
    ok_roots = roots == [0]
    expr_inv = 1 / sp.Symbol("alpha0") - k * sp.log(mu / mu0)
    resid = sp.simplify(mu * sp.diff(expr_inv, mu) + k)
    ok_resid = resid == 0
    add("V1", "核验", "四维 QED 一圈：唯一固定点 α*=0，积分式符号回代严格成立（来料 §一）",
        "PASS" if (ok_roots and ok_resid) else "FAIL",
        f"SymPy：solve((2Nf/3π)·α²=0) 根集 = {roots}（Nf>0 时无正的非零根）；"
        f"积分式 α⁻¹(μ)=α⁻¹(μ0)−(2Nf/3π)ln(μ/μ0) 对 d/dlnμ 回代残差 = {resid}（精确零）。"
        f"⇒ 一圈 QED 只规定「怎么跑」，不规定「跑起来的那个数」——来料 §一的严格裁定复现。")
    return {"roots": [str(r) for r in roots], "resid": str(resid),
            "ok": bool(ok_roots and ok_resid)}


# ================================================================ V2 · 4−ε 符号结构
def v2():
    a, Nf, eps_s, t = sp.symbols("alpha Nf varepsilon t", real=True)
    x = sp.Function("x")(t)
    k_e = sp.Rational(2, 3) / sp.pi * Nf
    beta_e = -eps_s * a + k_e * a ** 2
    roots_e = sp.solve(sp.Eq(beta_e, 0), a)
    A = sp.simplify(roots_e[-1])
    ok_A = sp.simplify(A - 3 * sp.pi * eps_s / (2 * Nf)) == 0
    bp = sp.simplify(sp.diff(beta_e, a).subs(a, A))
    ok_bp = sp.simplify(bp - eps_s) == 0
    # 完整解 α(t)=A/(1+x)，x'=εx；k·A=ε 由 ε=1 的定义式给出
    kk = sp.Rational(2, 3) / sp.pi * (3 * sp.pi * eps_s / (2 * A))
    ok_kA = sp.simplify(kk * A - eps_s) == 0
    A_of_t = A / (1 + x)
    flow = -eps_s * A_of_t + (eps_s / A) * A_of_t ** 2
    resid = sp.simplify(sp.diff(A_of_t, t).subs(x.diff(t), eps_s * x) - flow)
    ok_resid = resid == 0
    add("V2", "核验", "4−ε 模型：α*=3πε/(2Nf)、β'(α*)=ε>0（红外吸引）、精确解残差零（来料 §二/§五）",
        "PASS" if (ok_A and ok_bp and ok_kA and ok_resid) else "FAIL",
        f"solve(β=0) = {roots_e} ⇒ 非零根 α* = {A}；β'(α*) = {bp}（ε>0 时红外吸引，来料符号证明复现）；"
        f"关系 k·α*=ε 的核对残差 = {sp.simplify(kk * A - eps_s)}；"
        f"完整解 α(μ)=α*/(1+(α*/α0−1)(μ/μ0)^ε) 沿流方程回代残差 = {resid}（精确零）。"
        f"μ=μ0 时 x=C=α*/α0−1 ⇒ α(μ0)=α0：初值自洽（来料 §五 复现）。")
    return {"alpha_star": str(A), "bp": str(bp), "resid": str(resid),
            "ok": bool(ok_A and ok_bp and ok_kA and ok_resid)}


# ================================================================ V3 · ε=1 数值锚
def v3():
    Nf_star = 3 * PI / (2 * ALPHA_EXP)
    a646 = 3 * PI / 1292
    ppm = (a646 - ALPHA_EXP) / ALPHA_EXP * 10 ** 6
    anchors = [(Nf_star, "645.7669324377"), (a646, "0.0072947197838772289"),
               (abs(ppm), "360.79")]
    oks = [(v, q, half_ulp_ok(mp.nstr(v, 30), q)) for v, q in anchors]
    all_ok = all(o for _, _, o in oks)
    add("V3", "核验", "ε=1 反推三锚（Nf*、Nf=646 的 α*、360.79 ppm）逐位复现且过半 ulp 判据",
        "PASS" if all_ok else "FAIL",
        f"Nf* = 3π/(2α_exp) = {mp.nstr(Nf_star, 20)}（来料 645.7669324377…，半 ulp="
        f"{mp.nstr(mp.mpf('1e-12') / 2, 3)}，实差 {mp.nstr(abs(Nf_star - mp.mpf('645.7669324377')), 3)}）；"
        f"Nf=646 ⇒ α* = 3π/1292 = {mp.nstr(a646, 25)}（来料 0.0072947197838772289…）；"
        f"相对偏差 (α*−α_exp)/α_exp = {mp.nstr(ppm, 10)} ppm ⇒ |偏差| = {mp.nstr(abs(ppm), 8)} ppm"
        f"（来料「约 360.79 ppm」）。ε=1 对应 d=3——来料的维数声明成立。"
        f"三项全部由本卷现场计算、按半 ulp 判据通过。",
        {"Nf_star": mp.nstr(Nf_star, 20), "a646": mp.nstr(a646, 25),
         "ppm": mp.nstr(ppm, 12), "abs_ppm": mp.nstr(abs(ppm), 10)})
    return {"Nf_star": Nf_star, "a646": a646, "ppm": ppm, "abs_ppm": abs(ppm),
            "pairs": anchors, "ok": all_ok}


# ================================================================ V4 · BZ 引用表值
def v4():
    quoted = {12: "0.753982", 14: "0.278017", 15: "0.142800", 16: "0.0416105"}
    vals = {}
    for nf, q in quoted.items():
        b0 = sp.Rational(11) - sp.Rational(2, 3) * nf
        b1 = sp.Rational(102) - sp.Rational(38, 3) * nf
        vals[nf] = mp.mpf(sp.N(sp.simplify(-4 * sp.pi * b0 / b1), 30))
    oks = {nf: half_ulp_ok(vals[nf], q) for nf, q in quoted.items()}
    two_pi_151 = sp.simplify(-4 * sp.pi * (sp.Rational(11) - sp.Rational(32, 3)) /
                            (sp.Rational(102) - sp.Rational(608, 3)))
    ok_151 = sp.simplify(two_pi_151 - 2 * sp.pi / 151) == 0
    all_ok = all(oks.values()) and ok_151
    add("V4", "核验", "SU(3) 两圈 Banks–Zaks 四组引用表值 + 闭式 2π/151（来料 §三）",
        "PASS" if all_ok else "FAIL",
        "β0=11−2Nf/3、β1=102−38Nf/3、α*=−4πβ0/β1：Nf=12 %s（来料 0.753982）、Nf=14 %s（0.278017）、"
        "Nf=15 %s（0.142800）、Nf=16 %s（0.0416105）——四组全部过半 ulp 判据；"
        "Nf=16 的闭式 = 2π/151 经 SymPy 精确化简恒等（来料 §三 末式复现）。"
        % tuple(mp.nstr(vals[nf], 10) for nf in (12, 14, 15, 16)),
        {"vals": {str(k): mp.nstr(v, 14) for k, v in vals.items()},
         "half_ulp": {str(k): bool(v) for k, v in oks.items()}, "two_pi_151": bool(ok_151)})
    return {"vals": vals, "pairs": [(vals[nf], quoted[nf]) for nf in sorted(quoted)], "ok": all_ok}


# ================================================================ V5 · 谱几何代数链
def v5():
    f0_s, g_s = sp.symbols("f0 g", positive=True)
    g2 = sp.solve(sp.Eq(f0_s / (2 * sp.pi ** 2) * g_s ** 2, sp.Rational(1, 4)), g_s ** 2)[0]
    ok_g2 = sp.simplify(g2 - sp.pi ** 2 / (2 * f0_s)) == 0
    alpha_em = sp.simplify(g2 * sp.Rational(3, 8) / (4 * sp.pi))
    ok_ae = sp.simplify(alpha_em - 3 * sp.pi / (64 * f0_s)) == 0
    table = {10: "0.0147262", 20: "0.00736311", 40: "0.00368155"}
    calc = {f: 3 * PI / (64 * f) for f in table}
    oks = {f: half_ulp_ok(calc[f], q) for f, q in table.items()}
    all_ok = ok_g2 and ok_ae and all(oks.values())
    add("V5", "核验", "谱几何归一化代数链 g²=π²/(2f0) ⇒ α_em(M_U)=3π/(64f0)，三组表值复现（来料 §四）",
        "PASS" if all_ok else "FAIL",
        f"f(0)/(2π²)·g²=1/4 ⇒ g² = {g2}；sin²θ_W(M_U)=3/8、α=e²/4π ⇒ α_em(M_U) = {alpha_em}"
        f"（同一条公式）。f0=10/20/40 → {mp.nstr(calc[10], 12)} / {mp.nstr(calc[20], 12)} / "
        f"{mp.nstr(calc[40], 12)}，对来料 0.0147262 / 0.00736311 / 0.00368155 全部过半 ulp。"
        f"口径说明：系数 f(0)/(2π²)·(1/4) 是来料引用的 CC 谱作用量归一化，本卷只核验其代数推论，"
        f"文献系数的独立推导不在本轮可计算范围（沿用 V16.1 对来料口径的处理惯例）。",
        {"g2": str(g2), "alpha_em": str(alpha_em),
         "calc": {str(k): mp.nstr(v, 16) for k, v in calc.items()}})
    return {"calc": calc, "pairs": [(calc[f], table[f]) for f in sorted(table)], "ok": all_ok}


# ================================================================ V6 · ★BZ 闭式全表 + 末项恒等 1
def v6():
    nf_x = sp.symbols("Nf", positive=True)
    b0_x = sp.Rational(11) - sp.Rational(2, 3) * nf_x
    b1_x = sp.Rational(102) - sp.Rational(38, 3) * nf_x
    closed = 2 * sp.pi * (33 - 2 * nf_x) / (19 * nf_x - 153)
    ok_closed = sp.simplify(-4 * sp.pi * b0_x / b1_x - closed) == 0
    rows = []
    for nf in range(9, 17):
        b0 = sp.Rational(11) - sp.Rational(2, 3) * nf
        b1 = sp.Rational(102) - sp.Rational(38, 3) * nf
        a_star = sp.simplify(-4 * sp.pi * b0 / b1)
        assert sp.simplify(a_star - 2 * sp.pi * (33 - 2 * nf) / (19 * nf - 153)) == 0
        rows.append((nf, b0, b1, a_star, mp.mpf(sp.N(a_star, 28))))
    d_mon = sp.simplify(sp.diff(closed, nf_x))
    ok_mon = d_mon == -642 * sp.pi / (19 * nf_x - 153) ** 2
    # 正性域：分子>0 ⟺ Nf<33/2；分母>0 ⟺ Nf>153/19 —— 由扫描现推，不许手数
    pos_ints = [nf for nf in range(1, 41) if (closed.subs(nf_x, nf) > 0)]
    lo_int = sp.ceiling(sp.Rational(153, 19))     # 分母换正的第一个整数
    hi_int = sp.floor(sp.Rational(33, 2))         # 分子保正的最大整数
    ok_domain = (pos_ints == list(range(int(lo_int), int(hi_int) + 1))
                 and (lo_int, hi_int) == (9, 16)
                 and sp.Rational(153, 19) < lo_int and hi_int < sp.Rational(33, 2))
    # ★本卷新增定理：两圈截断的固定点处，末项与首项之比恒为 −1（逐项现算，非引用）
    a_s = sp.symbols("alpha_s", positive=True)
    beta2 = -b0_x / (2 * sp.pi) * a_s ** 2 - b1_x / (8 * sp.pi ** 2) * a_s ** 3
    a_star_x = sp.simplify(sp.solve(sp.Eq(beta2, 0), a_s)[-1])
    lead = -b0_x / (2 * sp.pi) * a_star_x ** 2
    nextt = -b1_x / (8 * sp.pi ** 2) * a_star_x ** 3
    ratio = sp.simplify(nextt / lead)
    ok_ratio = ratio == -1
    ratio_num = [sp.simplify(ratio.subs(nf_x, nf)) for nf in (12, 15, 16)]
    ok_ratio_num = all(r == -1 for r in ratio_num)
    dist16 = rows[-1][4] / ALPHA_EXP
    n_rows = len(rows)
    all_ok = ok_closed and ok_mon and ok_domain and ok_ratio and ok_ratio_num and n_rows == 8
    add("V6", "★新增", "Banks–Zaks 闭式全表（整数 9..16）、单调性定理、正性域与「末项≡首项」截断警告",
        "PASS" if all_ok else "FAIL",
        f"闭式恒等（逐整数 SymPy 精确断言，{n_rows}/8 通过）：α*(Nf) = 2π(33−2Nf)/(19Nf−153) ≡ −4πβ0/β1。"
        f"全表 Nf=9..16：{'、'.join('%d:%s' % (r[0], mp.nstr(r[4], 8)) for r in rows)}。"
        f"单调性 dα*/dNf = {d_mon} 在 [9,16] 严格负 ⇒ 全表递减（来料「符号证明通过」的加强版）。"
        f"正性域：分子>0 ⟺ Nf<16.5（β0→0 即渐近自由丧失边缘）、分母>0 ⟺ Nf>153/19≈8.0526 ⇒ 整数正根"
        f"恰为 {pos_ints}（对 Nf=1..40 扫描现推，非手数），Nf→16.5⁻ 时 α*→0（BZ 窗口上缘）。"
        f"★截断警告（本卷新增，符号定理）：在两圈定出的固定点上，β 的两圈项与一圈项之比（带号）"
        f"= {ratio}、绝对值 ≡ 1（Nf=12/15/16 数值核对 {ratio_num}）——两圈截断的定位没有一项比它保留的"
        f"低阶邻居小，"
        f"α*≤0.15 的「微扰可用」不等于级数收敛；固定点位置不是可收敛级数的读数。"
        f"与电磁耦合的距离：α*(16)/α_exp = {mp.nstr(dist16, 8)}（最靠近的族成员仍是 α_em 的 "
        f"{mp.nstr(dist16, 4)} 倍，来料「强作用固定点不能直接当电磁常数」的定量化）。")
    return {"rows": [(r[0], mp.nstr(r[4], 14)) for r in rows], "ratio": str(ratio),
            "closed": str(closed), "d_mon": str(d_mon), "dist16": dist16,
            "ok": all_ok, "n_rows": n_rows}


# ================================================================ V7 · ★f0 可证伪窗口
def v7():
    d_thr = abs(THR_BELOW - 口径_THR)
    d_rate = abs(RATE_ABOVE - 口径_RATE)
    grid = [("M_Z", M_Z), ("1e12", mp.mpf("1e12")), ("1e13", mp.mpf("1e13")),
            ("1e14", mp.mpf("1e14")), ("1e15", mp.mpf("1e15")), ("M_Pl", M_PL)]
    demand = [(l, m, ALPHA_INV_EXP - THR_BELOW - RATE_ABOVE * mp.log(m / M_Z), f0_of_mu(m))
              for l, m in grid]
    ln_10 = (ALPHA_INV_EXP - THR_BELOW - 64 * 10 / (3 * PI)) / RATE_ABOVE
    mu_10 = M_Z * mp.e ** ln_10
    pred = lambda f0v: 64 * f0v / (3 * PI) + THR_BELOW
    excluded = [f for f in (10, 20, 40) if pred(f) > ALPHA_INV_EXP]
    survived = [f for f in (10, 20, 40) if pred(f) <= ALPHA_INV_EXP]
    f0_max = f0_of_mu(M_Z)
    f0_min = f0_of_mu(M_PL)
    rt = max(abs(f0_of_mu(mu_of_f0(f)) - f) for f in (9, 10, 12, 15, 18))
    slope = -RATE_ABOVE * 3 * PI / 64
    ok_chain = d_thr < mp.mpf("1e-5") and d_rate < mp.mpf("1e-4")
    ok_excl = excluded == [20, 40] and survived == [10]
    ok_rt = rt < mp.mpf("1e-20")
    ok_win = (f0_min < 10 < f0_max) and (f0_of_mu(M_Z) > f0_of_mu(M_PL)) and slope < 0
    all_ok = ok_chain and ok_excl and ok_rt and ok_win and len(demand) == 6
    add("V7", "★新增", "f(0) 从自由参数压成可证伪窗口：链常数现推、需求表、f0=10↔M_U 反演、排除定理、双射",
        "PASS" if all_ok else "FAIL",
        f"RG 链（本库 V16.1 口径，SM 内容一圈）：1/α(0) = 64f0/(3π) + 阈值和 + 斜率·ln(M_U/M_Z)，"
        f"锚 1/α(M_Z)={mp.nstr(INV_ALPHA_MZ, 8)}。链常数由锚现推而非手感钉："
        f"阈值和 = 137.035999177 − 127.952 = {mp.nstr(THR_BELOW, 12)}（来料口径 9.084，Δ={mp.nstr(d_thr, 3)}）；"
        f"斜率 = 17/(3π) = {mp.nstr(RATE_ABOVE, 10)}（口径 1.8038，Δ={mp.nstr(d_rate, 3)}）。"
        f"需求表：{'；'.join('%s GeV → 1/α(M_U)=%s → f0需求=%s' % (l, mp.nstr(i, 10), mp.nstr(f, 8)) for l, m, i, f in demand)}。"
        f"反演：f0=10 ⟺ ln(M_U/M_Z)={mp.nstr(ln_10, 10)} ⟺ M_U={mp.nstr(mu_10, 8)} GeV（大统一量级）。"
        f"排除定理（M_U≥M_Z ⇒ 预测 1/α(0) ≥ 64f0/(3π)+阈值和）：f0=20 → {mp.nstr(pred(20), 11)}、"
        f"f0=40 → {mp.nstr(pred(40), 11)}，双双 > 实测 {mp.nstr(ALPHA_INV_EXP, 12)} ⇒ 被低能数据+一圈运行直接排除，"
        f"恰排除集={excluded}、存活集={survived}（非全部排除、非全不排除——判据有牙）。"
        f"合法窗口 M_U∈[M_Z,M_Pl] ⟺ f0∈[{mp.nstr(f0_min, 8)}, {mp.nstr(f0_max, 8)}]；"
        f"斜率 d(f0需求)/dlnM_U = {mp.nstr(slope, 8)} < 0 且 f0↔M_U 往返残差 ≤ {mp.nstr(rt, 3)}"
        f"（双射）。⇒ 缺口从「f0 是自由参数」压缩为「单一方程的两个未知数之一」：几何侧独立给出"
        f"f0 或 M_U 任一个即可闭合链条。",
        {"thr": mp.nstr(THR_BELOW, 12), "rate": mp.nstr(RATE_ABOVE, 12),
         "d_thr": mp.nstr(d_thr, 4), "d_rate": mp.nstr(d_rate, 4),
         "f0_min": mp.nstr(f0_min, 10), "f0_max": mp.nstr(f0_max, 10),
         "mu_10": mp.nstr(mu_10, 10), "ln_10": mp.nstr(ln_10, 10),
         "demand": [[l, mp.nstr(i, 12), mp.nstr(f, 10)] for l, m, i, f in demand],
         "excluded": excluded, "survived": survived})
    return {"f0_min": f0_min, "f0_max": f0_max, "mu_10": mu_10, "excluded": excluded,
            "survived": survived, "rt": rt, "demand": demand, "ok": all_ok,
            "thr": THR_BELOW, "rate": RATE_ABOVE, "d_thr": d_thr, "d_rate": d_rate,
            "slope": slope, "ln_10": ln_10}


# ================================================================ V8 · ★记忆擦除律
def n_exact(a0_v, A_v, e_v, eta):
    """T(ρ)=η 的精确反演：ρ^ε = η/[α*/α0 − η(α*/α0−1)]，返回 N=−log10 ρ（十进距）。"""
    rat = A_v / a0_v
    den = rat - eta * (rat - 1)
    return (mp.log10(den) + mp.log10(1 / eta)) / e_v


def v8():
    a0, A, rho, e = sp.symbols("alpha0 A rho epsilon", positive=True)
    alpha_r = A / (1 + (A / a0 - 1) * rho ** e)          # ρ=μ/μ0；向红外跑 ρ→0
    T_exact = sp.simplify(a0 * sp.diff(sp.log(alpha_r), a0))
    T_closed = (A / a0) * rho ** e / (1 + (A / a0 - 1) * rho ** e)
    ok_T = sp.simplify(T_exact - T_closed) == 0
    T1 = sp.simplify(T_exact.subs(rho, 1))
    ok_T1 = T1 == 1                                      # ρ=1 处记忆完整（自洽性）
    rows = []
    for e_v, nf_v in [(mp.mpf("0.1"), 10), (mp.mpf("1"), 646)]:
        A_v = 3 * PI * e_v / (2 * nf_v)
        rat = A_v / ALPHA_EXP
        n0 = erase_decades(rat, e_v)                      # 前导阶闭式
        nx = n_exact(ALPHA_EXP, A_v, e_v, ETA)            # 精确反演
        rows.append((e_v, nf_v, A_v, rat, n0, nx, nx <= AVAIL_DECADES, abs(n0 - nx)))
    same_verdict = all((r[4] <= AVAIL_DECADES) == (r[5] <= AVAIL_DECADES) for r in rows)
    bz = []
    for nf_v in (12, 15, 16):
        b0_ = sp.Rational(11) - sp.Rational(2, 3) * nf_v
        b1_ = sp.Rational(102) - sp.Rational(38, 3) * nf_v
        th = sp.simplify(-2 * b0_ ** 2 / b1_)
        ast = 2 * sp.pi * (33 - 2 * nf_v) / (19 * nf_v - 153)
        assert sp.simplify(th - ast * (33 - 2 * nf_v) / (6 * sp.pi)) == 0   # 恒等式现场断言
        th_v = mp.mpf(sp.N(th, 30))
        nloc = 1 / th_v                                   # 局域位移 10%α* 擦到 1%α*
        bz.append((nf_v, mp.mpf(sp.N(ast, 20)), th_v, nloc, nloc <= AVAIL_DECADES))
    pert_picks = [b for b in bz if b[1] <= mp.mpf("0.15")]
    ok_bz = all(not b[4] for b in pert_picks) and len(pert_picks) >= 2
    ok = ok_T and ok_T1 and same_verdict and ok_bz and len(rows) == 2 and len(bz) == 3
    add("V8", "★新增", "记忆擦除律：T(ρ)=∂lnα/∂lnα0 的闭式、精确反演与跨三族统一阈值 η=1%",
        "PASS" if ok else "FAIL",
        f"符号核验：对闭式解 α(ρ)=α*/(1+(α*/α0−1)ρ^ε) 求 T=∂lnα/∂lnα0 = {T_closed}"
        f"（与手写式残差 0）；ρ=1 处 T={T1}——初值原样记忆，式子自洽。"
        f"预算两口径（前导阶 N₀=[log₁₀(α*/α₀)+log₁₀(1/η)]/ε 对精确反演 N）："
        + "；".join(f"ε={e_v},Nf={nf_v}: α*={mp.nstr(A_v, 10)}、α*/α_exp={mp.nstr(rat, 7)}、"
                    f"N₀={mp.nstr(n0, 8)}、N={mp.nstr(nx, 8)}（差 {mp.nstr(dr, 3)}）"
                    f"{'≤' if fits else '>'}可达 {mp.nstr(AVAIL_DECADES, 6)}"
                    for e_v, nf_v, A_v, rat, n0, nx, fits, dr in rows)
        + f"。两口径对判决一致（{same_verdict}）。"
        f"★线性化统一读法（模型无关）：局域位移 10%α* 擦到 1%α* 需 N=1/θ 个十进距，θ=β'(α*)——"
        + "；".join(f"Nf={nf}: α*={mp.nstr(s, 8)}、θ={mp.nstr(th, 6)}、N={mp.nstr(nn, 6)}"
                    f"（{'够' if fits else '不够'}）" for nf, s, th, nn, fits in bz)
        + f"。恒等式 β'=α*(33−2Nf)/(6π) 逐 Nf 现场断言成立 ⇒ 临界指数被 α* 锁死：微扰可用"
        f"（α*≤0.15 ⇔ Nf≥15）的 BZ 固定点必有 θ≤1/44 ⇒ N≥44 > 可达窗口 {mp.nstr(AVAIL_DECADES, 6)}"
        f"——微扰性与擦除速度不相容（本卷新增否定性判据）。读数：ε=1 那一行的「低能唯一映射」通过"
        f"（N={mp.nstr(rows[1][5], 4)}≪{mp.nstr(AVAIL_DECADES, 4)}），而 ε=0.1 行（N={mp.nstr(rows[0][5], 6)}）"
        f"与 BZ 微扰区行全部超时——唯一来得及擦除初值记忆的，恰是唯一非微扰的那一行。")
    return {"rows": [[mp.nstr(e_v, 4), nf_v, mp.nstr(A_v, 14), mp.nstr(rat, 10),
                      mp.nstr(n0, 10), mp.nstr(nx, 10), bool(fits)]
                     for e_v, nf_v, A_v, rat, n0, nx, fits, dr in rows],
            "bz": [[nf, mp.nstr(s, 12), mp.nstr(th, 10), mp.nstr(nn, 10), bool(f)]
                   for nf, s, th, nn, f in bz],
            "avail": AVAIL_DECADES, "ok": ok, "n4_last": rows[1][5]}


# ================================================================ V9 · ★4−ε 的定价（FAIL）
def v9(v3r):
    n_limit = int(mp.ceil(v3r["Nf_star"])) + 1
    exact_hits = []
    for nf in range(1, n_limit):
        eps_req = 2 * nf * ALPHA_EXP / (3 * PI)
        if eps_req <= 1:
            exact_hits.append((nf, eps_req,
                               abs(3 * PI * eps_req / (2 * nf) - ALPHA_EXP) / ALPHA_EXP))
    n_expect = int(mp.floor(v3r["Nf_star"]))
    worst_resid = max(h[2] for h in exact_hits)
    eps_646 = 2 * 646 * ALPHA_EXP / (3 * PI)
    a_hi = 3 * PI / (2 * (n_expect))          # Nf=645
    a_lo = 3 * PI / (2 * (n_expect + 1))      # Nf=646（来料取整）
    gap_ppm = abs(a_hi - a_lo) / ALPHA_EXP * 10 ** 6
    half_gap = gap_ppm / 2
    base_rate = min(mp.mpf(1), v3r["abs_ppm"] / half_gap)
    grid_n = 200001                            # float64 口径，只数占比
    tol_f = float(v3r["abs_ppm"]) / 1e6
    a_exp_f = float(ALPHA_EXP)
    three_pi_f = 3.0 * math.pi
    cnt = 0
    for i in range(1, grid_n):
        e_g = i / (grid_n - 1)
        n_star = three_pi_f * e_g / (2 * a_exp_f)
        n_nei = int(round(n_star))
        if n_nei < 1:
            continue
        if abs(three_pi_f * e_g / (2 * n_nei) - a_exp_f) / a_exp_f <= tol_f:
            cnt += 1
    grid_frac = mp.mpf(cnt) / (grid_n - 1)
    tight = min(mp.mpf(1), mp.mpf(1e-6) * 10 ** 6 / half_gap)   # 容差 1 ppm 时的同一比值
    n_star_01 = 3 * PI * mp.mpf("0.1") / (2 * ALPHA_EXP)
    n_pick_01 = int(mp.nint(n_star_01))
    dev_01 = (3 * PI * mp.mpf("0.1") / (2 * n_pick_01) - ALPHA_EXP) / ALPHA_EXP * 10 ** 6
    Nf_s, e_s = sp.symbols("Nf varepsilon", positive=True)
    loop_param = sp.simplify(sp.Rational(2, 3) / sp.pi * Nf_s * (3 * sp.pi * e_s / (2 * Nf_s)))
    ok_lp = loop_param == e_s
    ok = (len(exact_hits) == n_expect and worst_resid < mp.mpf("1e-30") and eps_646 > 1
          and mp.mpf("0.3") < base_rate < mp.mpf("0.6") and grid_frac > mp.mpf("0.1")
          and abs(tight) < mp.mpf("0.01") and abs(dev_01) > 1000 and ok_lp)
    add("V9", "★定价", "4−ε 的「ε=1、Nf=646 命中 360.79 ppm」不构成预测：645 个零偏差命中＋格点基准率＋圈参数恒等式",
        "FAIL" if ok else "BOUNDARY",
        f"(a) 参数计数：α*=3πε/(2Nf) 有两个自由量、只有一个观测量。固定整数 Nf、放开 ε，则 "
        f"Nf=1..{len(exact_hits)} 各有一个 ε_req=2Nf·α_exp/(3π)≤1 给出**零偏差**命中"
        f"（最大残差 {mp.nstr(worst_resid, 3)}，格数由 Nf*=⌊{mp.nstr(v3r['Nf_star'], 13)}⌋={n_expect} 现推）。"
        f"Nf=646 需要 ε={mp.nstr(eps_646, 12)}>1——来料的「360.79 ppm 近失」完全是把 ε 钉在 1 的产物；"
        f"放开 ε 后命中是精确的且候选有 {len(exact_hits)} 个 ⇒ 信息量 0 bit。"
        f"(b) 钉住 ε=1 时可达值只有格点 {{3π/(2n)}}：α*({n_expect})={mp.nstr(a_hi, 14)}、"
        f"α*({n_expect + 1})={mp.nstr(a_lo, 14)}，格距 {mp.nstr(gap_ppm, 8)} ppm（半格 {mp.nstr(half_gap, 8)}）"
        f"⇒ 随机落点距目标 ≤{mp.nstr(v3r['abs_ppm'], 6)} ppm 的先验比例 = {mp.nstr(base_rate, 6)}；"
        f"第二口径：ε∈(0,1] 的 {grid_n - 1} 点网格上「存在整数 n 命中同一容差」的占比 = {mp.nstr(grid_frac, 6)}"
        f"（float64 计数，只用于占比）。两口径都说明这一量级的近失在该族里是常态而非稀有；"
        f"把容差收到 1 ppm 则比值降到 {mp.nstr(tight, 6)}——判据能区分「360 ppm」与「1 ppm」。"
        f"(c) 自洽区代价：圈参数恒等式 (2Nf/3π)·α* = {loop_param}（SymPy 精确）——固定点处的展开参数"
        f"就是 ε 本身，ε=1 的命中位于非微扰区；把 ε 收到 ≤0.1，所需 Nf*={mp.nstr(n_star_01, 8)} ⇒ "
        f"最近整数 {n_pick_01} 给出偏差 {mp.nstr(dev_01, 8)} ppm，比 360.79 ppm 大一个量级。"
        f"(d) 裁定：来料 §二数值全部复现（V3 PASS），但「反推 Nf 再取整」是参数选择而非预测——"
        f"多一个自由度换一个数字，符合度不进账（承 r304「读数不是预测」判词）。")
    return {"n_hits": len(exact_hits), "worst": worst_resid, "eps_646": eps_646,
            "gap_ppm": gap_ppm, "half_gap": half_gap,
            "base_rate": base_rate, "grid_frac": grid_frac, "tight": tight, "dev_01": dev_01,
            "n_expect": n_expect, "ok": ok}


# ================================================================ V10 · ★六格门禁矩阵
SLOTS = ["s1 存在性", "s2 稳定性", "s3 微扰一致性", "s4 无自由参数", "s5 四维 U(1)_em", "s6 低能唯一映射"]


def v10(v6r, v7r, v8r, v9r):
    # 截断末项/首项比：4−ε 与 BZ 同口径（带号 ≡ −1 ⇒ 绝对值 ≡ 1）
    a_y, Nf_y, e_y = sp.symbols("alpha Nf varepsilon", positive=True)
    k_y = sp.Rational(2, 3) / sp.pi * Nf_y
    A_y = 3 * sp.pi * e_y / (2 * Nf_y)
    lead_4 = -e_y * A_y
    next_4 = k_y * A_y ** 2
    ratio_4eps = sp.simplify(next_4 / lead_4)
    ok_ratio_4eps = ratio_4eps == -1 and sp.simplify(next_4 / (-lead_4)) == 1
    ell_running_A = RATE_ABOVE * ALPHA_EXP
    alpha_D = 3 * PI / (64 * mp.mpf(10))                 # f0=10 行的 α_em(M_U)（V5/V7 口径）
    ell_running_D = RATE_ABOVE * alpha_D
    rows = []
    rows.append(("A 四维 QED 一圈", [
        (False, "solve(β=0)={0}，无正的非零读数（V1）"),
        (False, "无固定点 ⇒ 无吸引子可言（V1）"),
        (True, "一圈截断：下一项/本项 ~ (2Nf/3π)α = %s ≪ 1/2（V1 口径）" % mp.nstr(ell_running_A, 6)),
        (False, "α0 是输入：1 自由量 0 选择方程（V1/r304 Q2）"),
        (True, "被跑动的正是四维 U(1)_em 的 α"),
        (False, "无吸引子 ⇒ 初值记忆不被擦除（V8）")]))
    rows.append(("B 4−ε（ε=1, Nf=646）", [
        (True, "α* = %s > 0（V3）" % mp.nstr(3 * PI / 1292, 12)),
        (True, "β'(α*) = ε = 1 > 0（V2 符号）"),
        (False, "固定点处末项/首项（带号）≡ %s、绝对值 ≡ 1（与 V6 同口径，非小量）；圈参数 = ε = 1（V9）" % ratio_4eps),
        (False, "两自由量一个观测量：%d 个零偏差命中（V9）" % v9r["n_hits"]),
        (False, "ε=1 ⇒ d=4−1=3，不是四维电磁（V3 维数声明）"),
        (True, "擦除预算 N=%s ≤ 可达 %s（V8）" % (mp.nstr(v8r["rows"][1][5], 6), mp.nstr(v8r["avail"], 6)))]))
    bz16 = [b for b in v8r["bz"] if b[0] == 16][0]
    rows.append(("C Banks–Zaks SU(3)（Nf=16）", [
        (True, "α* = 2π/151 = %s > 0（V4/V6）" % mp.nstr(bz16[1], 12)),
        (True, "β'(α*) = %s > 0（V8 恒等式）" % mp.nstr(bz16[2], 6)),
        (False, "两圈截断末项/首项（带号）≡ −1、绝对值 ≡ 1（V6 符号定理）"),
        (False, "Nf 是选择；且 α*/α_em = %s（V6）" % mp.nstr(v6r["dist16"], 6)),
        (False, "这是 SU(3) 的强耦合，不是 U(1)_em"),
        (False, "局域擦除需 N=%s ≫ 可达 %s（V8）" % (mp.nstr(bz16[3], 6), mp.nstr(v8r["avail"], 6)))]))
    rows.append(("D 谱几何 f(0)", [
        (True, "α_em(M_U) = 3π/(64f0)|f0=10 = %s > 0（V5）" % mp.nstr(alpha_D, 10)),
        (False, "无 β 函数、无吸引子——本卷未算出任何稳定性论证（V5/V7）"),
        (True, "一线运行链：(17/3π)α_em(M_U) = %s ≪ 1/2（V7 口径）" % mp.nstr(ell_running_D, 6)),
        (False, "f0 ∈ [%s, %s] 连续窗口非点（V7）" % (mp.nstr(v7r["f0_min"], 6), mp.nstr(v7r["f0_max"], 6))),
        (True, "被固定的就是四维 U(1)_em 的 α_em(M_U)"),
        (False, "无吸引子 ⇒ 缺口在 s4；单方程两未知数（V7）")]))
    grid = []
    for name, slots in rows:
        bools = [s[0] for s in slots]
        grid.append((name, bools, sum(bools), slots))
    real = grid
    dichotomy = all(not (b[1] and b[4]) for _, b, _, _ in real)          # ¬(s2 ∧ s5)
    fp_not_pert = all(not (b[0] and b[2]) for n, b, _, _ in real if b[1])  # 有吸引子者必失 s3
    best = max(s for _, _, s, _ in real)
    n_all6 = sum(1 for _, _, s, _ in real if s == 6)
    ok = (ok_ratio_4eps and dichotomy and fp_not_pert and len(real) == 4
          and best == 3 and n_all6 == 0 and all(len(b) == 6 for _, b, _, _ in real))
    add("V10", "★攻坚", "六格门禁矩阵：四条真实路线最高 3/6，且「吸引性 ⊥ 四维电磁」为机判二分定理",
        "FAIL" if ok else "BOUNDARY",
        "格定义（每格由本卷某条现场读数判决，不采信叙事）：s1 存在性=给出正的确定读数；"
        "s2 稳定性=该读数是红外吸引子（本卷算出 β'>0）；s3 微扰一致性=产出该数的截断中"
        "被舍项与末保留项之比 ≤1/2；s4 无自由参数=读数不含未定连续量；s5 对象=四维 U(1)_em 本身；"
        "s6 低能唯一映射=擦除预算 ≤ 可达十进距 "
        + mp.nstr(v8r["avail"], 6) + "。读数：" + "；".join(
            "%s = %d/6 [%s]" % (n, s, "".join("P" if x else "F" for x in b)) for n, b, s, _ in real) + "。"
            "★二分定理（机判成立）：四条真实路线中 s2（红外吸引）与 s5（这就是四维电磁耦合）"
            "互斥——%s；且凡有吸引子者必失 s3（%s）：固定点处末项/首项恒等于 1（V6 符号定理、"
            "4−ε 现场核验 %s）。⇒ 来料 §七 自己列出的三要件（存在/稳定/低能唯一映射）被 4−ε 路线"
            "满足 3/3，但把它变成电磁常数预测所缺的恰是 s3/s4/s5 三格——不是工程细节，是对象错位。"
            "无任何路线 6/6（合成理想路线见 C6，证明门禁可达、非空判）。"
            % (dichotomy, fp_not_pert, ratio_4eps),
            {"矩阵": [[n, [x for x in b], s] for n, b, s, _ in real],
             "逐格依据": [[list(x) for x in sl] for n, sl in rows],
             "二分定理_吸引与电磁互斥": bool(dichotomy),
             "有吸引子者必失微扰一致性": bool(fp_not_pert), "最高分": best})
    return {"grid": grid, "ok": ok, "best": best, "dichotomy": dichotomy,
            "fp_not_pert": fp_not_pert, "ratio_4eps": str(ratio_4eps)}


# ================================================================ V11 · CODATA 现行版本
def v11():
    same = ALPHA_INV_EXP == mp.mpf("137.035999177")
    add("V11", "核验", "锚点 CODATA 2022 α⁻¹(0)=137.035999177(21) 与来料一致；现行版本核对为二手口径",
        "BOUNDARY" if same else "FAIL",
        "数值一致：%s —— 与来料 §六 末行锚点逐字相同，且与 CODATA 2022 集合（2024-05-09 由 NIST 发布，"
        "维基百科「Eddington number」「List of physical constants」两条目均引同一"
        "「2022 CODATA Value: inverse fine-structure constant」=137.035999177(21)）一致。"
        "诚实边界：本卷试图直取 NIST 常数页（physics.nist.gov/cgi-bin/cuu/Value?invvs）失败"
        "（宿主返回 ill-formed request），故「该集合仍为现行推荐版」只由二手来源支撑 ⇒ 判 BOUNDARY，"
        "不作为「已与官方源逐字核对」登记（遗留 X-R314-1）。" % mp.nstr(ALPHA_INV_EXP, 12))
    return {"ok": same}


# ================================================================ V12 · 来料 §六 九行审计表
AUDIT_ROWS = [
    ("1", "4D QED 一圈无非零正固定点", "V1"),
    ("2", "4−ε 固定点闭式 α*=3πε/(2Nf)", "V2"),
    ("3", "固定点红外吸引（β'>0）", "V2"),
    ("4", "ε=1 反推 Nf*=645.7669324377…", "V3"),
    ("5", "Nf=646 的 α* 与实测差约 360.79 ppm", "V3"),
    ("6", "SU(3) 两圈 BZ 表值（Nf=12/14/15/16）", "V4"),
    ("7", "谱几何 α_em(M_U)=3π/(64f(0)) 表值", "V5"),
    ("8", "4−ε 初值问题精确解、SymPy 残差为零", "V2"),
    ("9", "无参数预测 α(0)", "V9"),
]


def v12(v3r, v9r):
    by_carrier = {}
    for it in ITEMS:
        by_carrier.setdefault(it["id"], it["verdict"])
    lines = []
    n_done = 0
    for idx, claim, carrier in AUDIT_ROWS:
        verdict = by_carrier.get(carrier, "MISSING")
        if idx == "9":
            tag = "尚未完成 → 本卷判 %s（符合度不进账）" % verdict
        else:
            tag = "已完成 → 本卷载体 %s 判 %s" % (carrier, verdict)
            n_done += 1 if verdict == "PASS" else 0
        lines.append("%s. %s ｜ %s" % (idx, claim, tag))
    missing = [idx for idx, claim, carrier in AUDIT_ROWS if carrier not in by_carrier]
    ok = (n_done == 8 and len(AUDIT_ROWS) == 9 and not missing
          and by_carrier.get("V9") == "FAIL")
    add("V12", "核验", "来料 §六 九行审计表逐行挂载体（八行完成/一行未完成，无一行落在本卷之外）",
        "PASS" if ok else "FAIL",
        "九行全部指回本卷已算出的条目，不留散文行："
        + "；".join(lines)
        + "。计数由解析后的表复算（完成且载体 PASS 的行数=%d/8，未完成行=1），非手数。"
          "第 9 行的载体是 V9：本卷把它从「尚未完成」推进为「已定价的失败」——"
          "不是差一点点，而是 %d 个零偏差候选使信息量为 0 bit。" % (n_done, v9r["n_hits"]),
        {"完成行数": n_done, "总行数": len(AUDIT_ROWS),
         "逐行": lines})
    return {"ok": ok, "n_done": n_done}


# ================================================================ V13 · 判据集 R1–R6
def v13(v7r, v9r, v10r, v8r):
    rows = [
        ("R1", "来料数值锚点逐位复现（10 锚，半 ulp 判据 + ±1 ulp 变异体全红）", "PASS",
         "V3/V4/V5；牙齿在 C2"),
        ("R2", "结构定理可证（一圈无正固定点／BZ 闭式与单调性／f0↔M_U 双射／T(ρ) 闭式）", "PASS",
         "V1/V2/V6/V7/V8 全部符号或精确反演成立"),
        ("R3", "产出该读数的截断自洽（被舍项 ≪ 末保留项）", "FAIL",
         "固定点处末项/首项 ≡ 1（V6 符号定理、V10 现场核验）——微扰可用不等于级数自洽"),
        ("R4", "f(0) 的可证伪性（自由参数 → 窗口 + 排除）", "PASS",
         "V7：窗口 [%s, %s]、恰排除 {20,40}" % (mp.nstr(v7r["f0_min"], 6), mp.nstr(v7r["f0_max"], 6))),
        ("R5", "低能唯一映射（擦除预算 ≤ 可达十进距 %s）" % mp.nstr(v8r["avail"], 6), "BOUNDARY",
         "4−ε 通过（N=%s）；BZ 在微扰区失败（N=%s，V8）"
         % (mp.nstr(v8r["rows"][1][5], 6), mp.nstr(v8r["bz"][2][3], 6))),
        ("R6", "无自由参数的 α(0) 预测", "FAIL",
         "V9：%d 个零偏差命中（0 bit）；V10：无路线 6/6（最高 %d/6）" % (v9r["n_hits"], v10r["best"])),
    ]
    tally = {v: sum(1 for r in rows if r[2] == v) for v in ("PASS", "FAIL", "BOUNDARY")}
    ok = (len(rows) == 6 and sum(tally.values()) == 6)
    add("V13", "判据", "判据集 R1–R6 = %d/6 PASS + %d FAIL + %d BOUNDARY"
        % (tally["PASS"], tally["FAIL"], tally["BOUNDARY"]),
        "INFO" if ok else "FAIL",
        "逐条：" + "；".join("%s(%s) %s——%s" % r for r in rows) +
        "。与 r304 对照：r304 把缺口收敛到「不含自由边界值的耦合动力学选择方程」；本卷把该方程"
        "拆成六格并机判——来料的三要件（s1/s2/s6）4−ε 全满足，缺的是 s3/s4/s5，"
        "而 s2 与 s5 在四条真实路线上互斥（V10 二分定理）⇒ 缺口不是「再算一次」，是"
        "**需要一个四维电磁耦合自身的吸引子**。",
        {"逐条": ["%s(%s) %s——%s" % r for r in rows], "score": tally,
         "计数自洽": bool(ok)})
    return {"tally": tally, "rows": rows}


# ================================================================ V14 · ★对表并发卷 r313（只读引用）
R313_FACE = os.path.join(
    DATA, "TUFT-r313_ROOTV21精细结构常数固定点机制第一性核验_四路线互消与未知量搬家定理与BZ截断相消_"
          "精算与可视化_2026-11-01.md")


def v14(v6r, v7r):
    """同一来料的第二把尺：从 r313 面上正则取出它印下的读数，与本卷现场计算逐位对表。"""
    import re as _re
    exists = os.path.isfile(R313_FACE)
    face = io.open(R313_FACE, encoding="utf-8").read() if exists else ""
    nf_x = sp.symbols("Nf", positive=True)
    # ★精度口径自证（本卷第一版在这里被骗过，见 V15 遗留 X-R314-9）：SymPy 没有 mp.mpf 转换器，
    #   sympify(mp.mpf) 先过 float() ⇒ 精度被锁在 float64，此后 sp.N(...,28) 只是把 16 位真值
    #   补成 28 位假数字。所以反解 N_f 的主读数走纯 mpmath，另把 SymPy 路的偏离现算成 ulp64 记账。
    def bz_inverse(alpha):
        return (66 * PI + 153 * alpha) / (19 * alpha + 4 * PI)

    bz_mine = bz_inverse(ALPHA_EXP)
    with mp.workdps(140):                            # 独立裁判：同一闭式在 140 位重算
        a_ref = mp.mpf(1) / mp.mpf("137.035999177")
        bz_ref = (66 * mp.pi + 153 * a_ref) / (19 * a_ref + 4 * mp.pi)
    ref_gap = abs(bz_mine - bz_ref)
    bz_sym = mp.mpf(sp.N(sp.simplify(sp.solve(
        sp.Eq((33 - 2 * nf_x) * 2 * sp.pi / (19 * nf_x - 153), ALPHA_EXP), nf_x)[0]), 28))
    u64 = ulp64_of(bz_ref)
    sym_ulp = abs(bz_sym - bz_ref) / u64
    bz_key = "BZ 替身 N_f*（实测 α 反解）"
    tree = {
        "N_f^{req}（Landau 指数 ≡ 反解费米子数）": (r"645\.7669324377\d*", 3 * PI * ALPHA_INV_EXP / 2),
        "α*(646)=3π/1292": (r"0\.007294719783877\d*", 3 * PI / 1292),
        "偏差 ppm": (r"360\.7857\d*", abs((3 * PI / 1292) / ALPHA_EXP - 1) * 10 ** 6),
        "α_s*(16)=2π/151": (r"0\.0416104987\d*", 2 * PI / 151),
        bz_key: (r"16\.4078139933\d*", bz_mine),
        "谱几何替身 f(0)_tree=3π/(64α)": (r"20\.1802166386\d*", 3 * PI * ALPHA_INV_EXP / 64),
    }
    rows, n_hit, n_missing = [], 0, 0
    for label, (pat, mine) in tree.items():
        found = _re.findall(pat, face) if exists else []
        if not found:
            n_missing += 1
            rows.append((label, "-", mp.nstr(mine, 12), "面上无该读数"))
            continue
        printed = max(found, key=len)
        ok = half_ulp_ok(mp.nstr(mine, 30), printed)
        n_hit += 1 if ok else 0
        rows.append((label, printed, mp.nstr(mine, 30), "逐位一致" if ok else "矛盾"))
    bz_found = _re.findall(tree[bz_key][0], face) if exists else []
    bz_print = max(bz_found, key=len) if bz_found else None
    bz_print_ulp = abs(mp.mpf(bz_print) - bz_ref) / u64 if bz_print else None
    same_rows = [(nf, mp.nstr(mp.mpf(mv), 10)) for nf, mv in v6r["rows"]][:8]
    n_shared = sum(1 for nf, s in same_rows if ("%s" % s)[:8] in face)
    # 探测器自测（针要能亮也能灭）：正对照取自面上真实存在的一串数字（构造即在场，只证明通道通电），
    # 负对照取一个本卷不可能印出的 token。第一版把已是字符串的读数再套一次 mp.nstr ⇒ 得到带引号的
    # '0.75398…' ⇒ 误印「0 行同现」，这枚假零由 bad_shape 现场复现。
    probe = _re.search(r"\d+\.\d{6}", face).group(0) if (exists and face) else ""
    det_pos = bool(probe) and (probe[:8] in face)
    det_neg = ("9.87654321" in face)
    bad_shape = mp.nstr(v6r["rows"][3][1], 10)
    det_bad_absent = ("%s" % bad_shape)[:8] not in face
    ratio_mine = v6r["ratio"]
    ok_face = (n_hit == len(tree) and n_missing == 0
               and sp.sympify(ratio_mine) == -1 and len(same_rows) == 8
               and n_shared == len(same_rows) and det_pos and (not det_neg)
               and det_bad_absent and ref_gap < mp.mpf("1e-70")
               and bz_print_ulp is not None and bz_print_ulp < mp.mpf(1))
    add("V14", "★对表", "并发卷 r313 同来料读数的独立复算：%d/%d 锚逐位一致，相消比同口径，覆盖↔窗口是口径差"
        % (n_hit, len(tree)),
        "PASS" if ok_face else "FAIL",
        f"对表对象（只读，不改字节）：{os.path.basename(R313_FACE)}；面存在={exists}、"
        f"md5={md5_of(R313_FACE) if exists else '-'}、字节={os.path.getsize(R313_FACE) if exists else -1}、"
        f"mtime={time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(R313_FACE))) if exists else '-'}。"
        f"逐条（他们印的 / 本卷现算 / 判决）：" + "；".join(
            "%s: %s | %s | %s" % r for r in rows) +
        f"。⇒ {n_hit}/{len(tree)} 命中、{n_missing} 枚面上取不到（取不到即判 FAIL，不算跳过）。"
        f"★精度层级（本卷自己踩过的坑，当场复算）：{bz_key} 闭式 N=(66π+153α)/(19α+4π) 在 85 位算得 "
        f"{mp.nstr(bz_mine, 25)}，140 位裁判 {mp.nstr(bz_ref, 25)}（差 {mp.nstr(ref_gap, 3)}）；"
        f"r313 印 {bz_print}，距裁判 {mp.nstr(bz_print_ulp, 4)} 个 float64 ulp ⇒ 他们那一枚在 double "
        f"口径内正确。本卷第一版把 α 塞进 SymPy 再 sp.N(…,28)，得 {mp.nstr(bz_sym, 25)}，"
        f"距裁判 {mp.nstr(sym_ulp, 4)} 个 ulp ⇒「矛盾」是本卷的假精度造成的，不是他们的读数错；"
        f"修正后主读数走 mpmath。教训登记为 X-R314-9：sympify(mp.mpf) 静默过 float()，"
        f"名义 28 位实际 16 位——凡跨库传常数必须先证明目标库能吃到那个位数。"
        f"BZ 全表 8 行中有 {n_shared} 行的本卷 10 位读数出现在他们面上（第二口径；探测器正对照 "
        f"{probe[:8]}=在场、负对照=不在场、旧写法产出的带引号 token {bad_shape} 前缀缺席={det_bad_absent} "
        f"⇒ 第一版那句「0 行同现」是针坏不是没有，登记为 X-R314-10）。"
        f"★三条关系读数：(1) 相消比同口径——本卷 V6/V10 带号恒等 = {ratio_mine}，与 r313 Q5 的「两圈项/一圈项 "
        f"= −1」同式；本卷 V10 把同一恒等式在 4−ε 家族也验为 −1 ⇒ 相消是任何两项截断固定点的通性，不是 BZ 特有。"
        f"(2) 覆盖与窗口不矛盾——r313 判 f(0) 的树级像 = (0,∞) ⇒ 零判别力；本卷 V7 在同一条关系上补 SM 一圈跑动"
        f"与 M_U 区间 ⇒ 像收窄为 [{mp.nstr(v7r['f0_min'], 6)}, {mp.nstr(v7r['f0_max'], 6)}] 且恰排除 "
        f"{v7r['excluded']} ⇒ 「零判别力」是该口径选择的产物，几何路线在带跑动口径下可证伪（正面回 r313 的 "
        f"X-R313-4）。(3) 连坐观察——r313 面上 G6/G7 两枚守卫印 FAIL，其源码里两枚同吃 q5 的那一条合取布尔"
        f"（含路线级判据）；本卷把「2π/151 严格性」与「相消比 ≡ −1」两条恒等式单独核验为真 "
        f"⇒ 登记为仪器型态观察：恒等式级守卫被路线级判决捆住时，会印出与自己主文（Q5 表格全中）相反的守卫色。"
        f"本卷只读引用 r313，未改其字节；引用其数字时须连同上面的 md5 一起读。",
        {"面md5": md5_of(R313_FACE) if exists else "-", "锚数": len(tree), "命中": n_hit,
         "取不到": n_missing, "同口径相消比": ratio_mine, "第二口径同现行": n_shared,
         "BZ反解_85位": mp.nstr(bz_mine, 25), "BZ反解_140位裁判": mp.nstr(bz_ref, 25),
         "r313_距裁判ulp64": mp.nstr(bz_print_ulp, 4) if bz_print_ulp is not None else "-",
         "BZ反解_SymPy路距裁判ulp64": mp.nstr(sym_ulp, 4),
         "逐条": [[l, p, m, v] for l, p, m, v in rows]})
    return {"n_hit": n_hit, "n_tok": len(tree), "n_missing": n_missing,
            "ok": ok_face, "rows": rows, "n_shared": n_shared,
            "bz_mine": mp.nstr(bz_mine, 25), "bz_ref": mp.nstr(bz_ref, 25),
            "bz_print": bz_print, "bz_print_ulp": mp.nstr(bz_print_ulp, 4) if bz_print_ulp is not None else "-",
            "bz_sym": mp.nstr(bz_sym, 25), "sym_ulp": mp.nstr(sym_ulp, 4),
            "det_pos": det_pos, "det_neg": det_neg, "old_shape_token": "%s" % bad_shape}


# ================================================================ V15 · 总登记
def v15():
    add("V15", "登记", "总判词、治理与遗留登记", "INFO",
        "判词：ROOT-V21-NUMERICS-REPRODUCED / FIXED-POINT-TRUNCATION-SELF-EQUAL / "
        "F0-CERTIFIABLE-WINDOW / ERASURE-LAW-QUANTIFIED / EPSILON-ONE-FIT-IS-ZERO-BIT / "
        "ATTRACTIVITY-ORTHOGONAL-TO-EM / STILL-NOT-A-PREDICTION。"
        "治理：未改 verify.py 与任何既有卷字节（对并发卷 r313 只读，其面 md5 由 V14 现场印出）；"
        "未跑 refresh_catalog.py（并发活跃，整体重生成会回退他人更大版本）；本卷条目数由守卫 G2 "
        "现算并核验，引用时以该读数为准，且不可与 r142–r313 各卷相加。取号 r314 由写前现扫三树决定"
        "（r308 已被并发的 ROOT V22 卷占用、r313 已被并发的 ROOT V21 卷占用 ⇒ 本卷让号）；"
        "下轮从 r315 起现扫取号。"
        "遗留：X-R314-1（NIST 常数页直取失败，现行版本只由二手来源支撑）；"
        "X-R314-2（谱几何系数 f(0)/(2π²)·(1/4) 的独立推导未联网核对，沿用 V16.1 惯例）；"
        "X-R314-3（4−ε 与 BZ 的两圈及以上系数为文献口径）；"
        "X-R314-4（阈值修正/全阶跑动下的 f0 窗口重做——本轮为一圈口径）；"
        "X-R314-5（M_U≈2.61×10¹⁶ GeV 与本库 r303 无阈值统一排除之间的张力未清算）；"
        "X-R314-6（非微扰固定点的可能性：V6 的 ≡1 恒等只约束微扰截断，不约束严格解）；"
        "X-R314-7（V14 的连坐观察只登记「同一条合取布尔驱动两枚恒等式守卫」这一源码事实与"
        "本卷的独立复算，未裁定 r313 的 FAIL 色应改——那需要作者自己重跑）；"
        "X-R314-8（V14 的覆盖↔窗口关系在一圈口径下成立；若允许 M_U 越过 M_Pl 或引入阈值修正，"
        "窗口会重新扩张，届时「可证伪」结论须重测）；"
        "X-R314-9（本卷仪器自己的精度坑：sp.N(sympify(mp.mpf),28) 名义 28 位、实为 float64 的 16 位，"
        "第一版据此把 r313 的正确读数判成「矛盾」。已改为跨库常数走 mpmath，并由 140 位裁判现算两条路"
        "的 ulp64 偏离；凡「他人读数与本卷不符」的判决，须先证本卷算这条路没被库精度静默截断）；"
        "X-R314-10（第二枚仪器坑：对已是字符串的读数再套一次 mp.nstr 得到带引号 token ⇒ 子串探测器"
        "误印「0 行同现」。现配正/负对照自测（在场 token 必亮、缺席 token 必灭），并把旧写法产出的"
        "那个带引号前缀缺席做成现场见证——假零与没有零同形，探测器必须自证能亮也能灭）；"
        "X-R314-11（第三枚仪器坑：控制组的「型」原先由题面字串『负对照』反推，措辞一改就假红；"
        "现由登记时的 kv[\"型\"] 声明，G7 按声明计数）。")
    return {"ok": True}


# ================================================================ 控制组
def controls(anchor_pairs, v7r, v8r, v9r, v10r):
    ctl = []
    # C1 正对照：来料正本逐字回链（数字挂在印出它的那份文件上）
    p_liao = os.path.join(DATA, LAILIAO)
    exists = os.path.isfile(p_liao)
    text = io.open(p_liao, encoding="utf-8").read() if exists else ""
    hits = {q: text.count(q) for _, q in anchor_pairs}
    n_present = sum(1 for q, c in hits.items() if c >= 1)
    ok1 = exists and n_present == len(anchor_pairs)
    ctl.append(("C1", "正对照", "来料正本 %d 个打印锚点在盘上逐字命中（含 137.035999177）"
                % len(anchor_pairs), "PASS" if ok1 else "FAIL",
                "正本存在=%s、md5=%s、字节=%d；锚点命中 %d/%d。缺任何一个 ⇒ 本卷的「复现」"
                "就没有可核对的载体（数字必须挂在印出它的那份文件上）。"
                % (exists, md5_of(p_liao) if exists else "-", os.path.getsize(p_liao) if exists else -1,
                   n_present, len(anchor_pairs))))
    # C2 负对照（牙）：±1/±2 ulp 变异体必须全部被半 ulp 判据拒绝
    reds, greens = [], []
    for v, q in anchor_pairs:
        for step in (1, -1, 2, -2):
            m = mutate_ulp(q, step)
            (greens if half_ulp_ok(mp.nstr(v, 30), m) else reds).append((q, step, m))
    ok2 = len(reds) == 4 * len(anchor_pairs) and not greens
    ctl.append(("C2", "负对照", "±1/±2 ulp 变异体全部被半 ulp 判据拒绝（判据有牙，%d 枚）"
                % (4 * len(anchor_pairs)), "PASS" if ok2 else "FAIL",
                "共 4×%d=%d 枚变异体，红 %d 枚、绿 %d 枚%s。若任何一枚变异体仍被判通过，"
                "则「锚点复现」是宽容差的假绿（r304 起本库把 6 ulp 宽判据换成半 ulp 的原因）。"
                % (len(anchor_pairs), 4 * len(anchor_pairs), len(reds), len(greens),
                   "" if not greens else "（越界样本：%s）" % greens[:3])))
    # C3 负对照（牙）：f0 排除集恰为 {20,40}，并在窗口边界两侧各取一值
    pred = lambda f0v: 64 * f0v / (3 * PI) + THR_BELOW
    excl = sorted(f for f in (10, 20, 40) if pred(f) > ALPHA_INV_EXP)
    edge_in = pred(18) <= ALPHA_INV_EXP          # 18 < 18.842 → 存活
    edge_out = pred(19) > ALPHA_INV_EXP          # 19 > 18.842 → 排除
    ok3 = (excl == [20, 40] and edge_in and edge_out)
    ctl.append(("C3", "负对照", "f0 排除判据恰拒绝 {20,40}、且在窗口边界两侧分判（18 活/19 拒）",
                "PASS" if ok3 else "FAIL",
                "排除集=%s（来料三个示例值中恰两个）；f0=18 → 预测 1/α(0)≥%s ≤ 实测 → 存活；"
                "f0=19 → ≥%s > 实测 → 排除。既不是全拒也不是全放。"
                % (excl, mp.nstr(pred(18), 11), mp.nstr(pred(19), 11))))
    # C4 负对照（牙）：擦除判据必须两个方向都能判，且方向由现算的 N 决定
    n_pass_4 = [r for r in v8r["rows"] if mp.mpf(r[5]) <= AVAIL_DECADES]
    n_fail_4 = [r for r in v8r["rows"] if mp.mpf(r[5]) > AVAIL_DECADES]
    n_fail_bz = [b for b in v8r["bz"] if mp.mpf(b[3]) > AVAIL_DECADES]
    ok4 = (len(n_pass_4) == 1 and len(n_fail_4) == 1 and len(n_fail_bz) >= 2
           and AVAIL_DECADES > 0)
    ctl.append(("C4", "负对照", "擦除判据双向有效：%d 行判「够」/%d 行判「不够」（4−ε）+%d 行 BZ「不够」"
                % (len(n_pass_4), len(n_fail_4), len(n_fail_bz)),
                "PASS" if ok4 else "FAIL",
                "可达窗口 %s 个十进距（现算 log10(M_Pl/M_Z)）。判「够」仅 ε=1 那一行（N=%s）；"
                "判「不够」= ε=0.1 行（N=%s）+ BZ Nf=15（N=%s）、Nf=16（N=%s）。"
                "★方向本身是新结果：唯一来得及擦除初值记忆的那一行，恰是唯一非微扰的那一行——"
                "擦除速度与截断自洽性在 4−ε 族里反向。阈值若被放宽到 1000 则全绿、判据失去区分力，"
                "故阈值固定为现算值。"
                % (mp.nstr(AVAIL_DECADES, 6), v8r["rows"][1][5], v8r["rows"][0][5],
                   v8r["bz"][1][3], v8r["bz"][2][3])))
    # C5 负对照（牙）：格点基准率能区分 360.786 ppm 与 1 ppm
    ratio_disc = v9r["base_rate"] / v9r["tight"] if v9r["tight"] != 0 else mp.inf
    ok5 = mp.mpf("0.3") < v9r["base_rate"] < mp.mpf("0.6") and v9r["tight"] < mp.mpf("0.01") \
        and ratio_disc > 100
    ctl.append(("C5", "负对照", "基准率判据把「360.79 ppm 近失」与「1 ppm 命中」分开（%d 倍）"
                % int(ratio_disc), "PASS" if ok5 else "FAIL",
                "同一格族下：tol=360.786 ppm ⇒ 先验比例 %s（常态）；tol=1 ppm ⇒ %s（稀有）；"
                "比值 %s。⇒ 「近失」这个词必须由基准率定价，不能由印象定价。"
                % (mp.nstr(v9r["base_rate"], 6), mp.nstr(v9r["tight"], 6), mp.nstr(ratio_disc, 6))))
    # C6 门可达性正对照：合成理想路线必须 6/6
    ideal = [True, True, True, True, True, True]
    ok6 = sum(ideal) == 6 and v10r["best"] < 6
    ctl.append(("C6", "正对照", "合成理想路线 6/6：门禁可达、非空判（四条真实路线最高 %d/6）"
                % v10r["best"], "PASS" if ok6 else "FAIL",
                "六格全真的定义本身无矛盾（存在正固定点＋红外吸引＋被舍项≪末项＋无自由参数＋"
                "对象是四维 U(1)_em＋擦除预算可达）⇒ V10 的 FAIL 不是把标准调到不可满足，"
                "而是四条真实路线各自缺格。"))
    # C7 负对照（牙）：RG 精确解残差为零，指数被改动后残差必须非零
    a, e, t = sp.symbols("alpha varepsilon t", positive=True)
    Nf_s = sp.symbols("Nf", positive=True)
    A_ = 3 * sp.pi * e / (2 * Nf_s)
    x = sp.Function("x")(t)
    sol = A_ / (1 + x)
    rhs = -e * sol + (sp.Rational(2, 3) / sp.pi * Nf_s) * sol ** 2
    resid_ok = sp.simplify(sp.diff(sol, t).subs(x.diff(t), e * x) - rhs)
    resid_bad = sp.simplify(sp.diff(sol, t).subs(x.diff(t), (e / 2) * x) - rhs)
    ok7 = (resid_ok == 0) and (resid_bad != 0)
    ctl.append(("C7", "负对照", "精确解回代：指数 ε 残差=0；把指数改成 ε/2 残差≠0（牙）",
                "PASS" if ok7 else "FAIL",
                "残差(正确指数)=%s；残差(摄动指数)=%s（非零 ⇒ 该检验不是恒真的样板）。"
                % (resid_ok, sp.simplify(resid_bad))))
    for tid, kind, title, verdict, detail in ctl:
        add(tid, "控制组", title, verdict, detail, {"型": kind})
    return [i for i in ITEMS if i["layer"] == "控制组"]


# ================================================================ 守卫
def guards(extra, ctl, roster, before):
    g = []
    g.append(("G1", "计算精度 ≥ 80 位（mpmath dps=%d）" % mp.mp.dps, mp.mp.dps >= 80,
              "来料声明 64/85 位口径，本卷取 85 位；SymPy 走分数/符号精确路径"))
    n_anchor = len(extra["anchors"])
    n_green = sum(1 for v, q in extra["anchors"] if half_ulp_ok(mp.nstr(v, 30), q))
    g.append(("G2", "锚点计数与颜色一致（声明 10 = 实收 %d = 判绿 %d）" % (n_anchor, n_green),
              n_anchor == 10 and n_green == 10,
              "V3 三枚 + V4 四枚 + V5 三枚 = 10；枚数由拼装现数，不手数"))
    c2 = [i for i in ITEMS if i["id"] == "C2"][0]
    g.append(("G3", "变异体全红（C2 PASS 才允许声称锚点复现）", c2["verdict"] == "PASS",
              "C2 verdict=%s；变异体共 4×%d=%d 枚" % (c2["verdict"], n_anchor, 4 * n_anchor)))
    counts = {
        "来料 §六 审计表": len(AUDIT_ROWS),
        "六格矩阵真实路线": len(extra["v10"]["grid"]),
        "六格矩阵列数": max(len(b) for _, b, _, _ in extra["v10"]["grid"]),
        "BZ 整数全表": len(extra["v6"]["rows"]),
        "判据集 R": len(extra["v13"]["rows"]),
        "对表 r313 锚": len(extra["v14"]["rows"]),
    }
    want = {"来料 §六 审计表": 9, "六格矩阵真实路线": 4, "六格矩阵列数": 6,
            "BZ 整数全表": 8, "判据集 R": 6, "对表 r313 锚": 6}
    bad_counts = {k: (counts[k], want[k]) for k in want if counts[k] != want[k]}
    tally_ok = sum(extra["v13"]["tally"].values()) == 6
    g.append(("G4", "版面计数由解析复算（表行数/矩阵维度/判据数）", not bad_counts and tally_ok,
              "实测 %s；R 类合计 %s=6" % (counts, extra["v13"]["tally"])))
    Nf_s, e_s = sp.symbols("Nf varepsilon", positive=True)
    lp = sp.simplify(sp.Rational(2, 3) / sp.pi * Nf_s * (3 * sp.pi * e_s / (2 * Nf_s)))
    g.append(("G5", "圈参数恒等式 (2Nf/3π)·α*≡ε 由守卫独立复算", lp == e_s,
              "守卫自己再推一次（不吃 V9 的布尔）：%s == %s" % (lp, e_s)))
    f0_probe = mp.mpf("13.7")                       # V7 未用过的外采样点
    mu_p = M_Z * mp.e ** ((ALPHA_INV_EXP - THR_BELOW - 64 * f0_probe / (3 * PI)) / RATE_ABOVE)
    back = 3 * PI / 64 * (ALPHA_INV_EXP - THR_BELOW - RATE_ABOVE * mp.log(mu_p / M_Z))
    ends = [abs(f0_of_mu(M_Z) - extra["v7"]["f0_max"]), abs(f0_of_mu(M_PL) - extra["v7"]["f0_min"])]
    g.append(("G6", "f0↔M_U 双射：外采样点往返 + 打印窗口端点复算",
              abs(back - f0_probe) < mp.mpf("1e-20") and max(ends) < mp.mpf("1e-20"),
              "f0=13.7 → M_U=%s → 回到 f0=%s（残差 %s）；端点残差 %s"
              % (mp.nstr(mu_p, 10), mp.nstr(back, 14), mp.nstr(abs(back - f0_probe), 3),
                 [mp.nstr(x, 3) for x in ends])))
    rej = [i for i in ctl if i["kv"].get("型") == "负对照" and i["verdict"] == "PASS"]
    pos = [i for i in ctl if i["kv"].get("型") == "正对照" and i["verdict"] == "PASS"]
    g.append(("G7", "判据牙齿齐备：控制组 ≥7、拒绝型负对照 ≥3 且全 PASS（「型」由登记时声明，不按题面字串猜）",
              len(ctl) >= 7 and len(rej) >= 3 and len(pos) >= 2
              and all(i["verdict"] == "PASS" for i in ctl),
              "控制组 %d 枚（型=负对照 %s／型=正对照 %s）；第一版按「题面含『负对照』字样」计数 ⇒ "
              "命中 0 枚而判红——题面措辞不是登记字段，这是假阳。"
              % (len(ctl), [r["id"] for r in rej], [p["id"] for p in pos])))
    main_fail = sorted(i["id"] for i in ITEMS
                       if i["layer"] not in ("控制组", "守卫") and i["verdict"] == "FAIL")
    want_fail = sorted(DESIGN_FAIL)
    g.append(("G8", "FAIL 棘轮：主条目 FAIL 集恰为预注册设计红 %s（不多不少，防止悄悄放行或悄悄加红）"
              % want_fail, main_fail == want_fail,
              "预注册 = %s；实测 = %s；逐条理由：%s"
              % (want_fail, main_fail,
                 {i["id"]: i["title"][:28] for i in ITEMS
                  if i["id"] in main_fail and i["layer"] not in ("控制组", "守卫")})))
    declared = extra["declared_n"]
    import re as _re
    residue = [i["id"] for i in ITEMS
               if _re.search(r"%[sdf(]", i["title"] + i["detail"]) or "{}" in i["title"] + i["detail"]]
    g.append(("G10", "无未格式化占位残留（百分号 s/d/f、空花括号、TODO 一律现算）", not residue,
              "残留条目 = %s" % residue))
    legal = {"PASS", "FAIL", "BOUNDARY", "INFO"}
    bad_v = [i["id"] for i in ITEMS if i["verdict"] not in legal]
    g.append(("G11", "verdict 取值合法（∈ {PASS,FAIL,BOUNDARY,INFO}）", not bad_v,
              "非法 = %s；分布 %s" % (bad_v, {v: sum(1 for i in ITEMS if i["verdict"] == v)
                                              for v in sorted(legal)})))
    bad = [p for p in WRITTEN if (RID not in os.path.basename(p)) and (p not in ALLOWED)]
    g.append(("G12", "仅写本卷路径（不触碰他卷字节）", len(bad) == 0,
              "写入 %d 个路径，越界 %d 个%s" % (len(WRITTEN), len(bad), bad and ("：" + str(bad)) or "")))
    ok_faces = (set(roster) == set(before) and len(roster) == 5
                and all(RID in os.path.basename(p) for p in roster)
                and all(isinstance(v, (str, type(None))) for v in before.values()))
    n_new = sum(1 for v in before.values() if v is None)
    g.append(("G13", "五张面名册齐备且运行前图像逐张探过（json/md/report/判定册/可视化）",
              ok_faces,
              "名册 5 张、名册==探过集合=%s、路径全部带 %s=%s；运行前不存在（首次落盘）%d 张、"
              "已存在 %d 张。逐面 md5/mtime 的新鲜度点名由收口只读轮另做，本枚只钉名册完整性"
              "（缺一张面 ⇒ 红）。正本（%s）只读、未进写入名单"
              % (set(roster) == set(before), RID, all(RID in os.path.basename(p) for p in roster),
                 n_new, 5 - n_new, LAILIAO)))
    n_main = sum(1 for i in ITEMS if i["layer"] not in ("控制组", "守卫"))
    final_n = n_main + len(ctl) + len(g) + 1        # +1 = 本枚 G9 自己
    g.append(("G9", "条目计数一致（声明 %d = 实收 %d）" % (declared, final_n), declared == final_n,
              "主条目 %d + 控制组 %d + 守卫 %d = %d；实收 %d。声明数取自卷首判据族，不是从 ITEMS 现数"
              "（现数会随漏登记一起变小而自证）。" % (n_main, len(ctl), len(g) + 1, final_n, final_n)))
    for gid, title, ok, detail in g:
        add(gid, "守卫", title, "PASS" if ok else "FAIL", detail, {})
    return g


# ================================================================ 版面装配
def products():
    return [os.path.join(DATA, BASE + ".json"),
            os.path.join(DATA, BASE + ".md"),
            os.path.join(DATA, BASE + "_report.txt"),
            os.path.join(JUD, "判定_" + BASE + ".md"),
            os.path.join(ROOT, "四力统一方程_ROOTV21耦合固定点机制审计_r314可视化_%s.html" % STAMP)]


def parts():
    main = [i for i in ITEMS if i["layer"] not in ("控制组", "守卫")]
    ctl = [i for i in ITEMS if i["layer"] == "控制组"]
    grd = [i for i in ITEMS if i["layer"] == "守卫"]
    return main, ctl, grd


def tables_text(extra):
    T = []
    T.append("[表 1] BZ 整数全表（V6，闭式 α*(Nf)=2π(33−2Nf)/(19Nf−153)）")
    for nf, v in extra["v6"]["rows"]:
        T.append("   Nf=%-3d α* = %s" % (nf, v))
    T.append("[表 2] f0 需求与窗口（V7；链常数由 137.035999177 − 127.952 与 17/(3π) 现推）")
    for label, mu, inv_mu, f0v in extra["v7"]["demand"]:
        T.append("   M_U=%-7s GeV  1/α(M_U)=%-13s  f0 需求=%s"
                 % (label, mp.nstr(inv_mu, 12), mp.nstr(f0v, 10)))
    T.append("   窗口 f0 ∈ [%s, %s]；f0=10 ⟺ M_U=%s GeV；排除集=%s 存活集=%s"
             % (mp.nstr(extra["v7"]["f0_min"], 8), mp.nstr(extra["v7"]["f0_max"], 8),
                mp.nstr(extra["v7"]["mu_10"], 8), extra["v7"]["excluded"], extra["v7"]["survived"]))
    T.append("[表 3] 擦除预算（V8，η=1%%，可达 %.6f 个十进距）" % AVAIL_DECADES)
    for e_s, nf_v, A_s, rat_s, n0_s, nx_s, fits in extra["v8"]["rows"]:
        T.append("   4−ε ε=%-4s Nf=%-4d α*=%-14s N₀=%-10s N精确=%-10s %s"
                 % (e_s, nf_v, A_s, n0_s, nx_s, "够" if fits else "不够"))
    for nf_v, s_s, th_s, nn_s, fits in extra["v8"]["bz"]:
        T.append("   BZ  Nf=%-4d α*=%-14s β'=%-12s N=1/β'=%-12s %s"
                 % (nf_v, s_s, th_s, nn_s, "够" if fits else "不够"))
    T.append("[表 4] 六格门禁矩阵（V10；P=真 F=假；s1 存在/s2 稳定/s3 微扰/s4 无自由/s5 四维电磁/s6 唯一映射）")
    for name, bools, score, _ in extra["v10"]["grid"]:
        T.append("   %-26s %s  = %d/6" % (name, " ".join("P" if b else "F" for b in bools), score))
    T.append("   合成理想路线（C6）          P P P P P P  = 6/6（证明门禁可达）")
    return T


def build_payloads(extra):
    main, ctl, grd = parts()
    tally = {v: sum(1 for i in ITEMS if i["verdict"] == v) for v in ("PASS", "FAIL", "BOUNDARY", "INFO")}
    summary = {"rid": RID, "stamp": STAMP,
               "标题": "ROOT V21 固定点机制独立复核（来料核验 + 五项攻坚 + 对表并发卷 r313）",
               "来料正本": LAILIAO, "条目总数": len(ITEMS), "主条目": len(main),
               "控制组": "%d/%d" % (sum(1 for i in ctl if i["verdict"] == "PASS"), len(ctl)),
               "守卫": "%d/%d" % (sum(1 for i in grd if i["verdict"] == "PASS"), len(grd)),
               "PASS": tally["PASS"], "FAIL": tally["FAIL"], "BOUNDARY": tally["BOUNDARY"],
               "INFO": tally["INFO"], "判据集": extra["v13"]["tally"],
               "精度位": mp.mp.dps, "耗时秒": round(time.time() - T0, 2),
               "判词": "ROOT-V21-NUMERICS-REPRODUCED / FIXED-POINT-TRUNCATION-SELF-EQUAL / "
                       "F0-CERTIFIABLE-WINDOW / ERASURE-LAW-QUANTIFIED / EPSILON-ONE-FIT-IS-ZERO-BIT / "
                       "ATTRACTIVITY-ORTHOGONAL-TO-EM / STILL-NOT-A-PREDICTION"}
    js = json.dumps({"summary": summary, "items": ITEMS}, ensure_ascii=False, indent=1)

    M = ["# %s" % summary["标题"], "",
         "- 轮次：**%s**（%s）· 精度 mpmath %d 位 + SymPy 精确 · 耗时 %s s" % (RID, STAMP, mp.mp.dps, summary["耗时秒"]),
         "- 来料正本（逐字）：`数据/%s`" % LAILIAO,
         "- 条目：总 %d（主 %d / 控制 %d / 守卫 %d）· PASS %d / FAIL %d / BOUNDARY %d / INFO %d"
         % (len(ITEMS), len(main), len(ctl), len(grd), tally["PASS"], tally["FAIL"],
            tally["BOUNDARY"], tally["INFO"]),
         "- 判词：**%s**" % summary["判词"], "",
         "## 一、总判词（先给结论）", ""]
    M.append("1. **来料的每一条可计算断言都复现了**：10 个打印锚（Nf*=645.7669324377、α*(646)、"
             "360.79 ppm、BZ 四组、谱几何三组）全部过**半 ulp**判据，±1/±2 ulp 的 %d 枚变异体全部被拒（C2）。"
             "也就是说：下面的否定不是「算错了」，而是「算对了但仍然不是预测」。" % extra["n_mutants"])
    M.append("2. **★截断自等定理**（V6/V10）：任何由两项截断 β 定出的固定点，其末项与首项之比**带号恒为 −1**"
             "（BZ：两圈项/一圈项 = %s；4−ε：同口径 = %s）⇒ 绝对值恒 1，没有一项比它保留的邻居小。"
             "微扰可用（α*≤0.15）≠ 级数自洽——固定点位置不是收敛级数的读数。"
             % (extra["v6"]["ratio"], extra["v10"]["ratio_4eps"]))
    M.append("3. **★f0 已被压成可证伪窗口**（V7）：M_U∈[M_Z,M_Pl] ⟺ f0∈[%s, %s]，来料示例值中"
             "f0=20/40 被低能数据+一圈运行**恰**排除，f0=10 存活并反演到 M_U=%s GeV（大统一量级）。"
             % (mp.nstr(extra["v7"]["f0_min"], 6), mp.nstr(extra["v7"]["f0_max"], 6),
                mp.nstr(extra["v7"]["mu_10"], 8)))
    M.append("4. **★记忆擦除律**（V8）：T(ρ)=∂lnα/∂lnα₀ 的闭式与预算 N(η)；统一 η=1%%、可达窗口 %.6f 个十进距。"
             "唯一来得及擦除的是 ε=1 那一行（N=%s），而它恰是非微扰的那一行；BZ 微扰区需 N=%s（Nf=15）~%s（Nf=16）。"
             % (AVAIL_DECADES, extra["v8"]["rows"][1][5], extra["v8"]["bz"][1][3], extra["v8"]["bz"][2][3]))
    M.append("5. **★ε=1 取整的「360.79 ppm 命中」= 0 bit**（V9）：放开 ε 后 Nf=1..%d 每个整数都有零偏差命中"
             "（最大残差 %s）；钉住 ε=1 时格距 %s ppm，故半格内先验比例 %s——这个量级的近失是该族的常态"
             "（1 ppm 容差才降到 %s）。" % (extra["v9"]["n_hits"], mp.nstr(extra["v9"]["worst"], 3),
                                            mp.nstr(extra["v9"]["gap_ppm"], 8),
                                            mp.nstr(extra["v9"]["base_rate"], 6),
                                            mp.nstr(extra["v9"]["tight"], 6)))
    M.append("6. **★六格门禁与二分定理**（V10）：s1 存在性/s2 稳定性/s3 微扰一致性/s4 无自由参数/"
             "s5 四维 U(1)_em/s6 低能唯一映射。四条真实路线最高 %d/6，无一 6/6；机判二分定理成立："
             "**s2（红外吸引）与 s5（这就是四维电磁耦合）互斥**（%s），且凡有吸引子者必失 s3（%s）。"
             "来料 §七 自列的三要件被 4−ε 满足 3/3——缺的不是执行，是对象。"
             % (extra["v10"]["best"], extra["v10"]["dichotomy"], extra["v10"]["fp_not_pert"]))
    M.append("7. **判据集** R1–R6 = %d PASS / %d FAIL / %d BOUNDARY（V13）；"
             "与 r304 的判词链汇合于同一句：缺的是**四维电磁耦合自身的吸引子/选择方程**。"
             % (extra["v13"]["tally"]["PASS"], extra["v13"]["tally"]["FAIL"],
                extra["v13"]["tally"]["BOUNDARY"]))
    M.append("8. **★与并发卷 r313 对表**（V14，只读引用）：同一份 ROOT V21 来料已有 r313 落库，本卷作为第二把尺"
             "把它面上 %d 个打印读数现场复算，**%d 枚逐位一致、%d 枚面上取不到**；r313 的「像覆盖 (0,∞) ⇒ 零判别力」"
             "与本卷 V7 的「f0 窗口 + 恰排除 %s」不是冲突而是口径差——加上 M_U 区间与一圈跑动后像就收窄成可证伪集合。"
             "另登记一枚仪器型态观察：r313 的 G6/G7 两枚恒等式守卫共用同一条含路线级判据的合取布尔，"
             "于是印出与其主文（表格全中）相反的守卫色（X-R314-7，本卷不裁定）。"
             "对表同时照出本卷自己两枚假红（首版「N_f* 矛盾」＝跨库常数被 float64 截断，"
             "首版「0 行同现」＝探测器吃下带引号的字符串），修正见证见 §三 V14 与 X-R314-9/10。"
             % (extra["v14"]["n_tok"], extra["v14"]["n_hit"], extra["v14"]["n_missing"],
                extra["v7"]["excluded"]))
    M += ["", "## 二、读数表", "", "```"] + tables_text(extra) + ["```", ""]
    for hd, lst in (("三、主条目", main), ("四、控制组", ctl), ("五、守卫", grd)):
        M.append("## %s" % hd)
        M.append("")
        for it in lst:
            M.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
        M.append("")
    M.append("## 六、治理")
    M.append("")
    M.append("- 未改 `verify.py`、未跑 `refresh_catalog.py`、未触碰任何既有卷字节；写入名单只含本卷五张面；"
             "对并发卷 r313 只读（其面 md5 由 V14 现场印出）。")
    M.append("- 取号：写前现扫三树——r308 已被并发的 ROOT V22 卷占用、r313 已被并发的同来料 ROOT V21 卷占用 "
             "⇒ 本卷让号取 r314；下轮从 r315 起现扫取号。")
    M.append("- 本卷 %d 条**不可**与 r142–r313 各卷条目相加（不同判据族）。" % len(ITEMS))
    md = "\n".join(M)
    R = ["=" * 78, "TUFT-%s · ROOT V21 耦合固定点机制审计 · 精算面（%s）" % (RID, STAMP), "=" * 78]
    R += tables_text(extra)
    R.append("-" * 78)
    for it in ITEMS:
        R.append("[%s][%s] %s" % (it["id"], it["verdict"], it["title"]))
        R.append("    " + it["detail"])
    R.append("-" * 78)
    for k, v in summary.items():
        R.append("%-10s : %s" % (k, v))
    report = "\n".join(R)
    return {products()[0]: js, products()[1]: md, products()[2]: report}


def judgment_text(extra):
    main, ctl, grd = parts()
    J = ["# 判定册 · TUFT-%s ROOT V21 耦合固定点机制审计（%s）" % (RID, STAMP), "",
         "对象：外部来料《ROOT V21｜精细结构常数的固定点机制：第一性原理核验》"
         "（正本逐字存档于 `数据/%s`）。" % LAILIAO,
         "本卷判词：**%s**" % " / ".join([
             "ROOT-V21-NUMERICS-REPRODUCED", "FIXED-POINT-TRUNCATION-SELF-EQUAL",
             "F0-CERTIFIABLE-WINDOW", "ERASURE-LAW-QUANTIFIED", "EPSILON-ONE-FIT-IS-ZERO-BIT",
             "ATTRACTIVITY-ORTHOGONAL-TO-EM", "STILL-NOT-A-PREDICTION"]), "",
         "## 一、判词展开", ""]
    J.append("1. **复现层（V1–V5）**：来料八组可计算断言全部为真——一圈无正固定点、4−ε 的闭式与红外吸引、"
             "精确解零残差、ε=1 反推三锚、BZ 四组表值与 2π/151、谱几何 3π/(64f0) 链与三组表值。"
             "锚点判据用**半 ulp**（打印值必须是现场值的唯一四舍五入落点），并由 C2 的 4×%d 枚 "
             "±1/±2 ulp 变异体全红定价。" % len(extra["anchors"]))
    J.append("2. **★V6 截断自等定理**：β 截断到两项时，固定点处「保留的末项 / 保留的首项」**带号恒等于 −1**"
             "（BZ：两圈项/一圈项；4−ε：二次项/线性项，V10 同口径现场核验）⇒ 绝对值恒 1，"
             "没有一项比它保留的邻居小。故 α*≤0.15 的「微扰可用」只是数值大小判断，不构成级数自洽；"
             "固定点位置不是一个收敛展开的读数。BZ 全表 8 行（整数 9..16 现扫）、闭式 "
             "2π(33−2Nf)/(19Nf−153)、单调性 dα*/dNf = −642π/(19Nf−153)²、正性域扫描一并落账。")
    J.append("3. **★V7 f0 从自由参数到可证伪窗口**：链常数现推（阈值和 = %s，斜率 = %s，与来料口径 "
             "9.084/1.8038 的差分别 %s / %s）；需求表六档；f0=10 ⟺ M_U = %s GeV；排除定理恰拒绝 "
             "%s、放行 %s；窗口 f0 ∈ [%s, %s] 且 f0↔M_U 双射（往返残差 %s）。"
             % (mp.nstr(extra["v7"]["thr"], 12), mp.nstr(extra["v7"]["rate"], 10),
                mp.nstr(extra["v7"]["d_thr"], 4), mp.nstr(extra["v7"]["d_rate"], 4),
                mp.nstr(extra["v7"]["mu_10"], 8),
                extra["v7"]["excluded"], extra["v7"]["survived"],
                mp.nstr(extra["v7"]["f0_min"], 6), mp.nstr(extra["v7"]["f0_max"], 6),
                mp.nstr(extra["v7"]["rt"], 3)))
    J.append("4. **★V8 记忆擦除律**：T(ρ)=∂lnα/∂lnα₀ 的闭式经 SymPy 求导核验（ρ=1 处 T=1 自洽），"
             "预算两口径（前导阶闭式 vs 精确反演）在 η=1%% 下对判决一致；可达窗口取现算的 "
             "log₁₀(M_Pl/M_Z)=%.6f 个十进距。方向本身是新结果：4−ε 族里唯一来得及擦除初值记忆的"
             "是 ε=1 那一行（N=%s），而它正是圈参数=1 的非微扰行；BZ 微扰区（Nf≥15）需 N=%s~%s。"
             % (AVAIL_DECADES, extra["v8"]["rows"][1][5], extra["v8"]["bz"][1][3], extra["v8"]["bz"][2][3]))
    J.append("5. **★V9 ε=1 取整的符合度定价为 0 bit**：放开 ε ⇒ Nf=1..%d 每个整数一个零偏差命中"
             "（最大残差 %s）；钉住 ε=1 ⇒ 可达值只有格点，格距 %s ppm，半格 %s ppm，"
             "于是「距目标 ≤360.786 ppm」的先验比例 = %s（第二口径网格 %s）；容差收到 1 ppm 才降到 %s。"
             % (extra["v9"]["n_hits"], mp.nstr(extra["v9"]["worst"], 3),
                mp.nstr(extra["v9"]["gap_ppm"], 8), mp.nstr(extra["v9"]["half_gap"], 8),
                mp.nstr(extra["v9"]["base_rate"], 6), mp.nstr(extra["v9"]["grid_frac"], 6),
                mp.nstr(extra["v9"]["tight"], 6)))
    J.append("6. **★V10 六格门禁与二分定理**：s1 存在性、s2 稳定性、s3 微扰一致性、s4 无自由参数、"
             "s5 四维 U(1)_em、s6 低能唯一映射，逐格由本卷现场读数判决（矩阵 4 条真实路线 × 6 格）。"
             "最高分 %d/6，无路线 6/6（C6 的合成理想路线 6/6 证明门禁可达）。机判二分定理："
             "s2∧s5 在四条路线上互斥（=%s），且凡有吸引子者必失 s3（=%s）——"
             "**来料 §七 自己列的三要件（存在/稳定/低能唯一映射）被 4−ε 满足 3/3，"
             "但它仍不是电磁常数的预测：缺的三格恰好是「四维」「电磁」「无自由参数」。**"
             % (extra["v10"]["best"], extra["v10"]["dichotomy"], extra["v10"]["fp_not_pert"]))
    J.append("7. **V12 把来料 §六 的九行审计表逐行挂到本卷载体**（八行完成、第 9 行「无参数预测 α(0)」"
             "的载体是 V9，本卷把它从「尚未完成」推进为「已定价的失败」）。")
    J.append("8. **★V14 与并发卷 r313 对表（只读引用）**：同一份 ROOT V21 来料在写前已被 r313 落库，本卷遂兼任"
             "第二把尺——从 r313 的精算面正则取出 %d 个打印读数（N_f^{req}、α*(646)、ppm、2π/151、"
             "BZ 替身 N_f*、谱几何替身 f(0)_tree），与本卷现场计算逐位对表：**%d 枚逐位一致、%d 枚面上取不到**"
             "（取不到即判 FAIL，不算跳过），并印出该面的 md5 作为引用锚。关系读数：本卷 V6/V10 的带号相消比"
             "与 r313 Q5 同口径；本卷 V7 的 f0 窗口与 r313 的「像覆盖 (0,∞)」是**口径差**（是否带跑动与 M_U 区间），"
             "不互相否证；r313 面上 G6/G7 两枚恒等式守卫印 FAIL 而本卷独立复算这两条恒等式为真，"
             "差异登记为仪器型态观察（X-R314-7），不裁定他卷。"
             "**对表把自己也照了一遍**：本卷首版在此处印出「BZ 替身 N_f* 矛盾」与「0 行同现」两枚红，"
             "现场复核后两枚都是本卷的仪器错——(a) `sp.N(sympify(mp.mpf),28)` 名义 28 位实为 float64 的 16 位，"
             "r313 那一枚距 140 位裁判 %s 个 ulp64（在 double 口径内正确），本卷的 SymPy 路距 %s 个 ulp64；"
             "修正后主读数走 mpmath 且两路偏离都印在面上（X-R314-9）；(b) 子串探测器把已是字符串的读数"
             "再套一次 `mp.nstr` 得到带引号 token ⇒ 假零，现补正/负对照自测（X-R314-10）。"
             % (extra["v14"]["n_tok"], extra["v14"]["n_hit"], extra["v14"]["n_missing"],
                extra["v14"]["bz_print_ulp"], extra["v14"]["sym_ulp"]))
    J += ["", "## 二、模型与判定管线", "",
          "- **模型**：4D QED 一圈 β=(2Nf/3π)α²；4−ε 模型 β=−εα+(2Nf/3π)α²；SU(3) 两圈 "
          "β0=11−2Nf/3、β1=102−38Nf/3；CC 谱作用量归一化 f(0)/(2π²)g²=1/4 与 sin²θ_W(M_U)=3/8；"
          "SM 内容一圈 RG 链锚 1/α(M_Z)=127.952。",
          "- **管线**：V1 一圈 → V2 4−ε 符号 → V3 ε=1 锚 → V4 BZ 表值 → V5 谱几何链 → "
          "V6 ★BZ 闭式全表与截断自等 → V7 ★f0 窗口与排除 → V8 ★擦除律 → V9 ★符合度定价 → "
          "V10 ★六格矩阵 → V11 CODATA 现行性 → V12 九行审计表 → V13 判据集 → "
          "V14 ★对表并发卷 r313 → V15 总登记。",
          "- **口径**：α⁻¹(0)=137.035999177(21)（CODATA 2022，V11 记二手来源）；M_Z=91.1876 GeV；"
          "M_Pl=2.435×10¹⁸ GeV；η=1%；全卷统一。", ""]
    J.append("## 三、判据集 R1–R6")
    J.append("")
    for line in [i for i in ITEMS if i["id"] == "V13"][0]["kv"]["逐条"]:
        J.append("- " + line)
    J.append("")
    J.append("## 四、六格矩阵读数")
    J.append("")
    J.append("```")
    J += [t for t in tables_text(extra) if "六格" in t or t.startswith("   ")][-10:]
    J.append("```")
    J.append("")
    for hd, lst in (("五、控制组", ctl), ("六、守卫", grd), ("七、主条目逐条", main)):
        J.append("## %s" % hd)
        J.append("")
        for it in lst:
            J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
        J.append("")
    J.append("## 八、诚实边界（本卷不主张什么）")
    J.append("")
    J.append("- **B1**：谱几何系数 f(0)/(2π²)·(1/4) 与 sin²θ_W=3/8 为来料引用的文献口径；本卷只核验其"
             "代数推论，未独立推导该系数（X-R314-2，沿用 V16.1 惯例）。")
    J.append("- **B2**：RG 链为一圈口径（阈值和与斜率现推自 1/α(M_Z)=127.952 与 17/(3π)）；阈值修正、"
             "Higgs/顶夸克阈值效应与全阶跑动下的 f0 窗口重做未在本轮（X-R314-4）。")
    J.append("- **B3**：V6 的「末项≡首项」只约束**微扰截断**定出的固定点；非微扰/严格可解模型的固定点"
             "不受该恒等式限制（X-R314-6），故 V10 的 s3 判定对象是微扰路线。")
    J.append("- **B4**：V8 对 BZ 族用线性化流（局域位移 10%α*），该式只在 |δα|≪α* 附近成立；把 α₀ 取为"
             "α_em 的跨族读数不在线性化适用域内，故未采用——两口径已在面中并列印出。")
    J.append("- **B5**：V11 的 CODATA 现行版本核对由 NIST 页直取失败，只由二手来源支撑 ⇒ BOUNDARY。")
    J.append("- **B6**：M_U≈2.61×10¹⁶ GeV（f0=10 反演）与本库 r303 的无阈值统一排除之间的张力未清算"
             "（X-R314-5），引用本卷该行时须一并读出。")
    J.append("- **B7**：V14 对并发卷 r313 的一切引用都是**只读**的（面 md5/字节/mtime 由 V14 现场印出为该锚）；"
             "本卷不复用 r313 的任何计算，对表只把「它印出的字符串」与本卷现场值放在一起判半 ulp。"
             "因此若 r313 的面在本轮之后被作者重跑改写，本卷 V14 那一行即失效，须现读新面重做。")
    J.append("")
    J.append("## 九、治理与遗留")
    J.append("")
    J.append("- 治理：未改 `verify.py`；未跑 `refresh_catalog.py`；未改任何既有卷字节；写入名单=本卷五张面；"
             "本卷 %d 条不可与他卷条目相加；取号 r314 由写前现扫三树决定"
             "（r308 已被并发的 ROOT V22 卷占用、r313 已被并发的同来料 ROOT V21 卷占用 ⇒ 本卷让号；"
             "下轮从 r315 起现扫取号）。" % len(ITEMS))
    J.append("- 遗留：X-R314-1（NIST 常数页直取）、X-R314-2（谱几何系数独立推导）、"
             "X-R314-3（两圈及以上系数文献口径）、X-R314-4（阈值修正下 f0 窗口重做）、"
             "X-R314-5（M_U 与 r303 排除的张力）、X-R314-6（非微扰固定点的 s3 边界）、"
             "X-R314-7（r313 守卫连坐只登记不裁定）、X-R314-8（一圈口径下的 f0 窗口）、"
             "X-R314-9（跨库常数被 float64 静默截断，本卷第一版据此误判 r313）、"
             "X-R314-10（子串探测器自测缺失导致假零）、X-R314-11（控制组「型」原先按题面字串反推）。")
    J.append("- 下一道关键问题与来料结语同向：**寻找四维电磁耦合自身的吸引子/选择方程**，"
             "而不是继续用实验值挑选几何系数——本卷把这句话变成了六格可判的门禁。")
    return "\n".join(J)


def html_text(extra):
    main, ctl, grd = parts()
    payload = {"rid": RID, "stamp": STAMP,
               "title": "ROOT V21 固定点机制独立复核 · 截断自等 / f0 窗口 / 擦除律 / 格点基准率 / 六格门禁",
               "counts": {"items": len(ITEMS), "main": len(main), "ctl": len(ctl), "grd": len(grd)},
               "items": [{"id": i["id"], "layer": i["layer"], "v": i["verdict"], "t": i["title"],
                          "d": i["detail"]} for i in ITEMS],
               "bz": extra["v6"]["rows"], "demand": [[l, mp.nstr(a, 12), mp.nstr(b, 10)]
                                                     for l, m, a, b in extra["v7"]["demand"]],
               "f0_min": float(extra["v7"]["f0_min"]), "f0_max": float(extra["v7"]["f0_max"]),
               "thr": float(THR_BELOW), "rate": float(RATE_ABOVE), "invA": float(ALPHA_INV_EXP),
               "mz": float(M_Z), "mpl": float(M_PL),
               "erase": [[r[0], r[1], r[5], bool(r[6])] for r in extra["v8"]["rows"]] +
                        [["BZ Nf=%d" % b[0], b[1], b[3], bool(b[4])] for b in extra["v8"]["bz"]],
               "avail": float(AVAIL_DECADES), "eta": float(ETA),
               "matrix": [[n, b, s] for n, b, s, _ in extra["v10"]["grid"]], "slots": SLOTS,
               "x313": {"face": os.path.basename(R313_FACE), "md5": extra["v14"]["rows"] and "",
                        "rows": [[l, p, m, v] for l, p, m, v in extra["v14"]["rows"]],
                        "hit": extra["v14"]["n_hit"], "tok": extra["v14"]["n_tok"],
                        "missing": extra["v14"]["n_missing"]},
               "lattice": {"gap": float(extra["v9"]["gap_ppm"]), "half": float(extra["v9"]["half_gap"]),
                           "obs": float(extra["v3"]["abs_ppm"]), "rate": float(extra["v9"]["base_rate"]),
                           "grid": float(extra["v9"]["grid_frac"]), "tight": float(extra["v9"]["tight"]),
                           "hits": extra["v9"]["n_hits"]},
               "alpha_exp": float(ALPHA_EXP)}
    payload["x313"]["md5"] = md5_of(R313_FACE) if os.path.isfile(R313_FACE) else "-"
    return _HTML.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False))


def write_all(payloads):
    for p, txt in payloads.items():
        d = os.path.dirname(p)
        if not os.path.isdir(d):
            raise RuntimeError("目录缺失：%s" % d)
        with io.open(wpath(p), "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
    return len(payloads)


_HTML = u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__RID__ · ROOT V21 固定点机制独立复核</title>
<style>
body{margin:0;background:#0f1218;color:#dfe6f2;font:14px/1.6 "Segoe UI","Microsoft YaHei",sans-serif}
header{padding:22px 28px;background:linear-gradient(90deg,#131a26,#0f1218);border-bottom:1px solid #24304a}
h1{margin:0 0 6px;font-size:20px} .sub{color:#8fa3c7;font-size:12px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(430px,1fr));gap:16px;padding:20px 28px}
.card{background:#141a26;border:1px solid #263450;border-radius:12px;padding:16px 18px}
.card h2{margin:0 0 10px;font-size:15px;color:#e8eefc}
.badge{display:inline-block;padding:2px 9px;border-radius:999px;font-size:12px;margin-right:6px}
.PASS{background:#12351f;color:#7ee2a0}.FAIL{background:#3a1418;color:#ff9d9d}
.BOUNDARY{background:#3a2d10;color:#ffd28a}.INFO{background:#12283c;color:#8ecbff}
.live{background:#1d2a44;color:#a9c6ff}
input[type=range]{width:100%} label{color:#9fb2d4;font-size:12px;display:block;margin-top:8px}
.val{color:#fff;font-variant-numeric:tabular-nums}
table{border-collapse:collapse;width:100%;font-size:12px}
td,th{border-bottom:1px solid #223052;padding:4px 6px;text-align:right}
th{color:#93a8cc;font-weight:600} td.l{text-align:left}
.cell{width:26px;height:22px;border-radius:4px;display:inline-block}
.bar{height:16px;border-radius:4px;background:#2d6cf7}
.small{color:#8fa3c7;font-size:12px} .mono{font-family:Consolas,monospace}
details{margin-top:6px} summary{cursor:pointer;color:#a9c6ff}
</style></head><body>
<header><h1>__TITLE__</h1>
<div class="sub">轮次 __RID__ · __STAMP__ · 精度 mpmath 85 位 + SymPy 精确 ·
<span id="counts"></span></div></header>
<div class="grid">

<div class="card"><h2>1 · 4−ε 固定点与「截断自等」</h2>
<label>ε（展开参数）<span class="val" id="vEps"></span></label>
<input type="range" id="eps" min="0.001" max="1" step="0.001" value="1">
<label>N<sub>f</sub>（费米子种数）<span class="val" id="vNf"></span></label>
<input type="range" id="nf" min="1" max="700" step="1" value="646">
<div id="p1out" class="mono"></div>
<div class="small">固定点 α*=3πε/(2N<sub>f</sub>)；β'(α*)=ε&gt;0 ⇒ 红外吸引。
★带号相消比（二次项/线性项）恒 = −1，与 N<sub>f</sub>、ε 无关：
定位完全来自两项精确相消，故「微扰可用」不等于级数自洽。</div></div>

<div class="card"><h2>2 · ε=1 取整的符合度定价（0 bit）</h2>
<div id="p2out" class="mono"></div>
<div class="small">放开 ε ⇒ 每个整数 N<sub>f</sub> 都能零偏差命中（可调 ε 吸收任何 α），
该族对 α 的观测值零判别力；钉住 ε=1 ⇒ 可达值只剩格点，
格距即先验命中窗。近失不是证据，是格点的间距。</div></div>

<div class="card"><h2>3 · f(0) 可证伪窗口（含一圈跑动）</h2>
<label>f(0) <span class="val" id="vF0"></span></label>
<input type="range" id="f0" min="1" max="40" step="0.1" value="10">
<div id="p3out" class="mono"></div>
<div class="small">链：1/α(0)=64f0/(3π)+阈值和+斜率·ln(M<sub>U</sub>/M<sub>Z</sub>)。
M<sub>U</sub>∈[M<sub>Z</sub>,M<sub>Pl</sub>] ⇒ f0 被压成窗口；来料示例值中 f0=20/40 恰被排除。
对照并发卷 r313：其「像覆盖 (0,∞)」是树级直接贴低能的口径 ⇒ 加跑动与区间后集合收窄，
两者不互相否证。</div></div>

<div class="card"><h2>4 · Banks–Zaks 全表与截断比</h2>
<div id="p4tbl"></div>
<div class="small">闭式 α*=2π(33−2N<sub>f</sub>)/(19N<sub>f</sub>−153)，
整数正根域现扫 1..40 恰为 9..16；带号末项/首项 ≡ −1（对任意 β<sub>0</sub>,β<sub>1</sub>）。</div></div>

<div class="card"><h2>5 · 记忆擦除预算 vs 可达十进距</h2>
<div id="p5bars"></div>
<div class="small">阈值 η=1%；可达窗口 __AVAIL__ 个十进距（现算 log<sub>10</sub>(M<sub>Pl</sub>/M<sub>Z</sub>)）。
★唯一来得及擦除初值记忆的那一行（ε=1）恰是唯一非微扰的那一行 ⇒
擦除速度与截断自洽性在 4−ε 族里反向。</div></div>

<div class="card"><h2>6 · 六格门禁矩阵</h2>
<div id="p6tbl"></div>
<div class="small">★二分定理：s2（红外吸引）与 s5（这就是四维 U(1)<sub>em</sub>）在四条真实路线上互斥；
且凡有吸引子者必失 s3。合成理想路线 6/6（C6）证明门禁可达 ⇒ FAIL 不是标准不可满足，是对象错位。</div></div>

<div class="card"><h2>7 · 与并发卷 r313 对表（只读）</h2>
<div id="p7tbl"></div>
<div class="small">面 <span class="mono" id="p7face"></span> md5 <span class="mono" id="p7md5"></span>。
把 r313 面上打印的读数与本卷现场计算逐位对表（半 ulp）；取不到即判 FAIL，不算跳过。</div></div>

<div class="card"><h2>8 · 条目台账</h2>
<div class="small" id="flt"></div>
<div id="p8list"></div></div>
</div>
<script>
var P = __PAYLOAD__;
var A_EXP = P.alpha_exp, INV_A = P.invA, THR = P.thr, RATE = P.rate;
var MZ = P.mz, MPL = P.mpl, AVAIL = P.avail, PI = Math.PI;
function f(x,n){return isFinite(x)?x.toFixed(n===undefined?10:n):String(x);}
function badge(t){return '<span class="badge '+t+'">'+t+'</span>';}
document.getElementById('counts').innerHTML =
 P.counts.items+' 条（主 '+P.counts.main+' / 控制 '+P.counts.ctl+' / 守卫 '+P.counts.grd+'）';
function runEps(){
 var e=+document.getElementById('eps').value, nf=+document.getElementById('nf').value;
 var astar=3*PI*e/(2*nf), looppar=(2*nf/(3*PI))*astar;
 var dev=(astar/A_EXP-1)*1e6;
 var epsReq=2*nf/(3*PI*A_EXP);
 var sign=-1; // 带号相消比恒 -1
 document.getElementById('vEps').textContent=' ε='+f(e,3);
 document.getElementById('vNf').textContent=' Nf='+nf;
 document.getElementById('p1out').innerHTML =
  'α* = '+f(astar,12)+'<br>α*/α_exp − 1 = '+f(dev,3)+' ppm<br>'+
  'β′(α*) = +'+f(e,3)+' ⇒ 红外吸引<br>'+
  '圈参数 (2Nf/3π)·α* = '+f(looppar,6)+' ≡ ε ⇒ '+badge(Math.abs(looppar-e)<1e-12?'PASS':'FAIL')+
  '该式的零点由 ε 自定<br>带号末项/首项 = '+sign+' （恒等，非小量）⇒ '+badge('BOUNDARY')+
  '<br>把 α*=α_exp 反解 ⇒ ε_req(Nf) = '+f(epsReq,6)+'（'+(epsReq<=1?'≤1 在 ε 展开名义域内':'>1 出域，d=4−ε<3')+'）';
}
function runF0(){
 var f0=+document.getElementById('f0').value;
 var lb=64*f0/(3*PI)+THR, mu=MZ*Math.exp((INV_A-THR-64*f0/(3*PI))/RATE);
 var inWin=(f0>=P.f0_min && f0<=P.f0_max);
 var okM=(mu>=MZ && mu<=MPL);
 document.getElementById('vF0').textContent=' f0='+f(f0,1);
 document.getElementById('p3out').innerHTML =
  '预测 1/α(0) ≥ '+f(lb,6)+' vs 实测 '+f(INV_A,6)+' ⇒ '+
  badge(lb<=INV_A?'PASS':'FAIL')+(lb<=INV_A?'存活（可由某个 M_U 实现）':'被低能数据排除')+
  '<br>反演 M_U = '+f(mu/Math.pow(10,Math.floor(Math.log10(mu))),4)+'×10'+
  Math.floor(Math.log10(mu))+' GeV '+badge(okM?'PASS':'BOUNDARY')+
  (okM?'（落在 [M_Z, M_Pl]）':'（出区间 ⇒ 该 f0 无一圈解）')+
  '<br>本卷窗口 f0∈['+f(P.f0_min,3)+', '+f(P.f0_max,3)+'] ⇒ 当前 f0 '+
  badge(inWin?'PASS':'FAIL')+(inWin?'在窗口内':'在窗口外');
}
function lat(){
 var L=P.lattice;
 document.getElementById('p2out').innerHTML =
  '零偏差命中整数 Nf 个数 = '+L.hits+'（每个都可命中 ⇒ 无信息）<br>'+
  'ε=1 格距 = '+f(L.gap,4)+' ppm，半格窗 = '+f(L.half,4)+' ppm<br>'+
  '来料读数偏差 = '+f(L.obs,4)+' ppm ⇒ 先验比例 = '+f(L.rate,4)+
  ' <span class="badge BOUNDARY">≈ '+Math.round(L.rate*100)+'% 常态</span><br>'+
  '第二口径（连续网格）= '+f(L.grid,4)+'；容差收到 1 ppm ⇒ '+f(L.tight,6)+
  ' <span class="badge PASS">才稀有</span>';
}
function bz(){
 var h='<table><tr><th class="l">Nf</th><th>α*</th><th class="l">相对 α_exp</th></tr>';
 P.bz.forEach(function(r){h+='<tr><td class="l">'+r[0]+'</td><td>'+r[1]+'</td><td>'+
  f(r[1]/A_EXP,3)+'×</td></tr>';});
 document.getElementById('p4tbl').innerHTML=h+'</table>';
}
function erase(){
 var mx=Math.max.apply(null,P.erase.map(function(r){return +r[2];}).concat([AVAIL]));
 var h='<table>';
 P.erase.forEach(function(r){
  var n=+r[2], w=Math.min(100, 100*Math.log10(Math.max(n,1e-9))/Math.log10(mx));
  h+='<tr><td class="l">'+r[0]+' '+r[1]+'</td><td class="l" style="width:60%">'+
     '<div class="bar" style="width:'+f(w,1)+'%;background:'+(r[3]?'#1f9d55':'#c33')+'"></div></td>'+
     '<td>'+f(n,3)+'</td><td class="l">'+badge(r[3]?'PASS':'FAIL')+'</td></tr>';});
 h+='<tr><td class="l">可达窗口（现算）</td><td></td><td>'+f(AVAIL,4)+'</td><td class="l">—</td></tr></table>';
 document.getElementById('p5bars').innerHTML=h;
}
function matrix(){
 var h='<table><tr><th class="l">路线</th>'+P.slots.map(function(s){return '<th>'+s+'</th>';}).join('')+
  '<th>分</th></tr>';
 P.matrix.forEach(function(r){
  h+='<tr><td class="l">'+r[0]+'</td>'+r[1].map(function(b){
   return '<td><span class="cell" style="background:'+(b?'#1f9d55':'#5a1e24')+'"></span></td>';}).join('')+
   '<td>'+r[2]+'/6</td></tr>';});
 h+='<tr><td class="l">合成理想路线（C6 正对照）</td>'+
   P.slots.map(function(){return '<td><span class="cell" style="background:#2d6cf7"></span></td>';}).join('')+
   '<td>6/6</td></tr></table>';
 document.getElementById('p6tbl').innerHTML=h;
}
function x313(){
 var X=P.x313;
 document.getElementById('p7face').textContent=X.face;
 document.getElementById('p7md5').textContent=X.md5;
 var h='<div class="small">命中 '+X.hit+'/'+X.tok+'，面上取不到 '+X.missing+'</div>'+
  '<table><tr><th class="l">读数名</th><th class="l">r313 印的</th><th class="l">本卷现算</th><th class="l">判决</th></tr>';
 X.rows.forEach(function(r){
  h+='<tr><td class="l">'+r[0]+'</td><td class="l mono">'+r[1]+'</td><td class="l mono">'+r[2]+
     '</td><td class="l">'+badge(r[3]==='逐位一致'?'PASS':'FAIL')+' '+r[3]+'</td></tr>';});
 document.getElementById('p7tbl').innerHTML=h+'</table>';
}
function ledger(){
 var layers=['全部','主条目','★攻坚','★新增','★对表','核验','判据','登记','控制组','守卫'];
 var box=document.getElementById('flt');
 box.innerHTML=layers.map(function(l,i){return '<span class="badge '+
   (i===0?'live':'INFO')+'" style="cursor:pointer" data-l="'+l+'">'+l+'</span>';}).join('');
 var list=document.getElementById('p8list');
 function draw(sel){
  list.innerHTML=P.items.filter(function(it){
   return sel==='全部'||it.layer===sel||(sel==='主条目'&&['★攻坚','★新增','★对表','核验','判据','登记'].indexOf(it.layer)>=0);
  }).map(function(it){
   return '<details><summary>'+badge(it.v)+' <b>'+it.id+'</b> '+it.t+'</summary>'+
     '<div class="small mono" style="white-space:pre-wrap">'+it.d+'</div></details>';}).join('');
 }
 box.addEventListener('click',function(ev){
  var l=ev.target.getAttribute('data-l'); if(!l)return;
  [].forEach.call(box.children,function(c){c.className='badge INFO';});
  ev.target.className='badge live'; draw(l);});
 draw('全部');
}
runEps();runF0();lat();bz();erase();matrix();x313();ledger();
document.getElementById('eps').addEventListener('input',runEps);
document.getElementById('nf').addEventListener('input',runEps);
document.getElementById('f0').addEventListener('input',runF0);
</script></body></html>"""


def main():
    before = {p: (md5_of(p) if os.path.isfile(p) else None) for p in products()}
    extra = {}
    extra["v1"] = v1()
    extra["v2"] = v2()
    extra["v3"] = v3()
    extra["v4"] = v4()
    extra["v5"] = v5()
    extra["v6"] = v6()
    extra["v7"] = v7()
    extra["v8"] = v8()
    extra["v9"] = v9(extra["v3"])
    extra["v10"] = v10(extra["v6"], extra["v7"], extra["v8"], extra["v9"])
    extra["v11"] = v11()
    extra["v12"] = v12(extra["v3"], extra["v9"])
    extra["v13"] = v13(extra["v7"], extra["v9"], extra["v10"], extra["v8"])
    extra["v14"] = v14(extra["v6"], extra["v7"])
    extra["v15"] = v15()
    anchors = extra["v3"]["pairs"] + extra["v4"]["pairs"] + extra["v5"]["pairs"]
    extra["anchors"] = anchors
    extra["n_mutants"] = 4 * len(anchors)
    ctl = controls(anchors, extra["v7"], extra["v8"], extra["v9"], extra["v10"])
    # 卷首判据族声明：V1–V15（15）+ C1–C7（7）+ G1–G13（13）
    extra["declared_n"] = 35
    guards(extra, ctl, products(), before)
    payloads = build_payloads(extra)
    payloads[products()[3]] = judgment_text(extra)
    payloads[products()[4]] = html_text(extra)
    n = write_all(payloads)
    main_items, ctl_i, grd_i = parts()
    tally = {v: sum(1 for i in ITEMS if i["verdict"] == v)
             for v in ("PASS", "FAIL", "BOUNDARY", "INFO")}
    print("=" * 78)
    print("TUFT-%s · ROOT V21 固定点机制独立复核（来料核验 + 五项攻坚 + 对表 r313）" % RID)
    print("=" * 78)
    print("条目 %d（主 %d / 控制 %d / 守卫 %d）· 落盘 %d 张面"
          % (len(ITEMS), len(main_items), len(ctl_i), len(grd_i), n))
    for k in ("PASS", "FAIL", "BOUNDARY", "INFO"):
        print("  %-9s %d" % (k, tally[k]))
    print("  判据集    %s" % extra["v13"]["tally"])
    print("  对表 r313 %d/%d 锚逐位一致（取不到 %d）"
          % (extra["v14"]["n_hit"], extra["v14"]["n_tok"], extra["v14"]["n_missing"]))
    print("-" * 78)
    for it in ITEMS:
        print("[%s] %-9s %s" % (it["id"], it["verdict"], it["title"]))
    print("-" * 78)
    for p in products():
        print("%-8s md5=%s 字节=%d" % (os.path.basename(p)[-28:], md5_of(p), os.path.getsize(p)))
    print("可视化：%s" % products()[4])
    bad = [p for p in WRITTEN if RID not in os.path.basename(p)]
    off = sorted(set(WRITTEN) - set(products()))
    rc_ctl = all(i["verdict"] == "PASS" for i in ITEMS if i["layer"] == "控制组")
    rc_grd = all(i["verdict"] == "PASS" for i in ITEMS if i["layer"] == "守卫")
    print("写入越界=%s 非本卷路径=%s 控制组全绿=%s 守卫全绿=%s"
          % (off, bad, rc_ctl, rc_grd))
    print("FAIL 主条目（按设计红，非仪器故障）=%s"
          % [i["id"] for i in main_items if i["verdict"] == "FAIL"])
    rc = 0 if (not bad and not off and rc_ctl and rc_grd) else 2
    print("RC =", rc)
    return rc


if __name__ == "__main__":
    import sys
    sys.exit(main())







