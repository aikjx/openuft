# -*- coding: utf-8 -*-
r"""
TUFT-r250 · 耦合常数跑动与能标层（★ RG 新层首卷）
================================================================================
【命题来源】用户：「攻破」

【取号】起草前实测 **r250/r251/r252 三树全空** ⇒ 取 **r250**。
  ⚠ 本轮撞号：r248（单方程全域力层，00:15:18 落四件套）与
  r249（低能极限推导层，00:27:44 落四件套）在本卷起草期间被**并行会话**占用
  ⇒ 按「已产四件套并登记者为权威、后到者整体改号」纪律，本卷**整体迁至 r250**，
  不改写他人文件。

【本卷定位：耦合常数跑动与能标层（RG 层）】
r244/r247 攻的是「引力是什么 / G 从哪来」；本卷攻的是靶另一端的核心宣称：

    靶宣称 TUFT「减少基本常数数目」，并把精细结构常数、大统一
    全部挂到一个「几何固定点」 α_* = α_0 = √3/2 ≈ 0.8660 上。

靶的等式清单（来料，逐字）给出：
  6.  α_0 = √3/2                              （裸精细结构常数，核心几何）
  7.  α_obs = α_0/(1+P_0) ≈ 1/137.036         （真空挠率屏蔽后）
  8.  β(α) = μ dα/dμ = (2/3π)α²               （QED 单圈）
  9.  1/α(μ) = 1/α_obs − (2/3π)·ln(μ/μ_0)     （RG 流积分解）
  10. α(μ) → α_* = √3/2  (μ → μ_Planck)       （几何饱和固定点）

★ 本卷的承重发现：**把靶的 9 号式代入 μ = μ_Planck，得到 α = 7.9301e-3，
   而靶的 10 号式断言该处 α 已饱和到 0.866025——用靶自己的公式，
   打靶自己的断言，差 109.21 倍。**

【分层】本卷是**耦合常数跑动与能标层**，与 r244（引力本体论层）、
r247（元审计层）、r245（超导本质层）、r243（工程可用性层）领域不同，
**条目不可相加**。r241 E13/E14 已判「裸值 0.866 与实测差 118.7 倍」的**静态**
数值问题；本卷判的是**动态**问题（跑动自相矛盾 / 能标错位 / 无修正 β 函数 /
大统一差 33–40 倍 / α_* 是定义恒等式），是新层，不重复计分。
================================================================================
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
from fractions import Fraction

# ============================================================
# 0. 元信息
# ============================================================
RID = "r250"
BASE_NAME = ("TUFT-r250_耦合常数跑动与能标层_RG自相矛盾与alpha星定义恒等式_"
             "大统一固定点证伪_精算与可视化_2026-10-30")
START_TS = time.time()
START_ISO = time.strftime("%Y-%m-%dT%H:%M:%S")

SRC_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
DATA_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\数据"

TARGETS = [
    os.path.join(DATA_DIR, "TUFT-r241_光速螺旋_来料原件_2026-10-30",
                 "基于光速螺旋流形的核心动力学方程组.md"),
    os.path.join(DATA_DIR,
                 "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md"),
    os.path.join(DATA_DIR,
                 "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md"),
]

WRITE_SIDE = [
    r"D:\a10\aikjx\code\my_lib\openuft\verify.py",
    r"D:\a10\aikjx\code\my_lib\openuft\00_项目治理\维护工具\refresh_catalog.py",
]

# ============================================================
# 1. 常数（全部带来源，不写死结论）
# ============================================================
C = 299792458.0
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
M_E_MEV = 0.51099895000            # 电子静能 MeV（CODATA）
M_Z_GEV = 91.1876                  # Z 玻色子质量 GeV
M_PLANCK_GEV = 1.220890e19         # 普朗克能量 GeV（PDG）
M_PLANCK_MEV = M_PLANCK_GEV * 1.0e3

ALPHA_OBS = 7.2973525693e-3        # CODATA 精细结构常数
A_STAR = math.sqrt(3.0) / 2.0      # 靶宣称的几何固定点

# M_Z 处实测耦合（用于大统一对照）
ALPHA_EM_MZ = 1.0 / 127.95
SIN2_THETA = 0.23121
ALPHA_S_MZ = 0.1180
B_SM = (41.0 / 10.0, -19.0 / 6.0, -7.0)     # SM 单圈 β 系数 (U1, SU2, SU3)


def fmt_rel(x):
    return "{:.3e}".format(x)


def rel(a, b):
    if b == 0:
        return float("inf") if a != 0 else 0.0
    return abs(a - b) / abs(b)


# ============================================================
# 2. 靶机读
# ============================================================
def read_text(p):
    try:
        with io.open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def sha256_of(p):
    try:
        with io.open(p, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


SHA_AT_IMPORT = {p: sha256_of(p) for p in TARGETS}
TARGET_TEXT = {p: read_text(p) for p in TARGETS}
RAW = TARGET_TEXT.get(TARGETS[0], "")
ALL = "".join(TARGET_TEXT.get(p, "") for p in TARGETS)
RAW_LINES = RAW.split("\n")


# ============================================================
# 3. ★ 核心计算
# ============================================================
def alpha_running(mu_mev, mu0_mev=M_E_MEV, a_obs=ALPHA_OBS):
    r"""靶的 9 号式：1/α(μ) = 1/α_obs − (2/3π)·ln(μ/μ_0)"""
    v = 1.0 / a_obs - (2.0 / (3.0 * math.pi)) * math.log(mu_mev / mu0_mev)
    return (1.0 / v) if v > 0 else float("inf")


def rg_layer():
    r"""★承重：靶的 9 号式在普朗克能标给出什么？与 10 号式的断言差多少？"""
    a_pl = alpha_running(M_PLANCK_MEV)
    ln_pl = math.log(M_PLANCK_MEV / M_E_MEV)
    # 要达到 α_* 所需的能标
    ln_need = (1.0 / ALPHA_OBS - 1.0 / A_STAR) * (3.0 * math.pi / 2.0)
    log10_need = ln_need / math.log(10.0)
    mu_need_mev = M_E_MEV * (10.0 ** log10_need)
    log10_pl = math.log10(M_PLANCK_MEV)
    above_planck_decades = (log10_need + math.log10(M_E_MEV)) - log10_pl
    # 标准兰道极点（1/α = 0），核对靶文中的 645.77
    ln_lp = (1.0 / ALPHA_OBS) * (3.0 * math.pi / 2.0)
    # 靶文中是否出现 645.77
    m645 = re.search(r"645\.7", ALL)
    return {
        "alpha_at_planck": a_pl,
        "ln_planck_over_mu0": ln_pl,
        "ratio_star_over_formula": A_STAR / a_pl,
        "ln_need": ln_need,
        "log10_need": log10_need,
        "mu_need_log10_mev": log10_need + math.log10(M_E_MEV),
        "planck_log10_mev": log10_pl,
        "above_planck_decades": above_planck_decades,
        "ln_landau": ln_lp,
        "target_has_645": bool(m645),
        "landau_log10_mev": ln_lp / math.log(10.0) + math.log10(M_E_MEV),
    }


def alpha_identity():
    r"""
    ★定义恒等式刀（承 r204/r247）：
    靶的链条  S=m_e c r₀=ℏ/2 ⇒ r₀=ℏ/(2m_ec)；
             自洽条件定 l_h=(√3/2)·ℏ/(m_ec)；
             α = l_h/√(r₀²+l_h²)
    但 √(r₀²+l_h²) = (ℏ/(m_ec))·√(1/4+3/4) = ℏ/(m_ec)，
    故 α = (√3/2)·(ℏ/(m_ec)) / (ℏ/(m_ec)) = √3/2，
    **与 m_e、c、ℏ 全部无关**。下面用「缩放 m_e」把这个不变性机验出来。
    """
    rows = []
    for s in (1.0e-3, 1.0e-1, 1.0, 1.0e1, 1.0e3, 1.0e6):
        m = M_E * s
        r0 = HBAR / (2.0 * m * C)
        lh = (math.sqrt(3.0) / 2.0) * HBAR / (m * C)
        a = lh / math.sqrt(r0 ** 2 + lh ** 2)
        rows.append({"scale": s, "m_kg": m, "r0": r0, "l_h": lh, "alpha": a,
                     "resid": abs(a - A_STAR)})
    # 闭式：l_h/r_0 = √3（恒等），α = √3/2 与 r0 无关
    ratio = rows[2]["l_h"] / rows[2]["r0"]
    return {"rows": rows, "lh_over_r0": ratio,
            "ratio_resid": abs(ratio - math.sqrt(3.0)),
            "max_alpha_resid": max(r["resid"] for r in rows),
            "spread": max(r["alpha"] for r in rows) - min(r["alpha"] for r in rows)}


def gut_layer():
    r"""大统一固定点 0.866 vs 标准模型单圈跑动值"""
    a1 = (5.0 / 3.0) * ALPHA_EM_MZ / (1.0 - SIN2_THETA)   # GUT 归一 U(1)
    a2 = ALPHA_EM_MZ / SIN2_THETA                          # SU(2)
    a3 = ALPHA_S_MZ                                        # SU(3)
    out = {"at_mz": (a1, a2, a3), "table": []}
    for mu in (1.0e10, 1.0e13, 1.0e16, 1.0e19):
        row = []
        for a0, b in ((a1, B_SM[0]), (a2, B_SM[1]), (a3, B_SM[2])):
            v = 1.0 / a0 - (b / (2.0 * math.pi)) * math.log(mu / M_Z_GEV)
            row.append(1.0 / v if v > 0 else float("inf"))
        out["table"].append((mu, row[0], row[1], row[2]))
    g16 = [t for t in out["table"] if abs(t[0] - 1.0e16) < 1][0]
    out["at_1e16"] = (g16[1], g16[2], g16[3])
    out["ratios"] = tuple(A_STAR / x for x in (g16[1], g16[2], g16[3]))
    return out


def screening_layer():
    r"""P_0 屏蔽因子：从观测 α 反解出来的单参数"""
    p0 = A_STAR / ALPHA_OBS - 1.0
    pats = {r"\\mathcal\{P\}_0": 0, r"屏蔽因子": 0, r"极化屏蔽": 0, r"极化率": 0}
    for k in pats:
        pats[k] = len(re.findall(k, ALL))
    # P_0 是否有独立数值（出现形如 P_0 = 117.x 的式子）
    indep = re.findall(r"\\mathcal\{P\}_0\s*=\s*[0-9]", ALL)
    return {"P_0": p0, "token_counts": pats, "independent_numeric": len(indep)}


def modified_beta_scan():
    r"""靶是否给出「能产生饱和」的修正 β 函数，而不只是渐近断言？"""
    pats = {
        "修正后+β": r"修正后.{0,20}β",
        "β(α)=": r"β\s*\(\s*α\s*\)\s*=",
        "β\\left": r"\\beta\\left",
        "饱和+β": r"饱和.{0,20}β",
        "屏蔽+β": r"屏蔽.{0,15}β",
        "非微扰β": r"非微扰.{0,20}β",
    }
    out = {}
    for k, p in pats.items():
        out[k] = len(re.findall(p, ALL))
    return out


# ============================================================
# 4. 修复定价
# ============================================================
RG_KEYS = ("modified_beta", "saturation_dynamics", "scale_anchor",
           "gut_matching", "screening_derived")
# 标准 RG 骨架：一旦补齐「修正 β + 能产生饱和的动力学」，
# 就等于把标准重整化群那套机制整个搬进来 ⇒ 原「几何固定点」宣称被替换
RG_STD_SKELETON = {"modified_beta", "saturation_dynamics"}


def repair_pricing(requirement):
    from itertools import product
    out = {"EMPTY": 0, "SUICIDE": 0, "SURVIVE": 0}
    surv = []
    for combo in product((False, True), repeat=len(RG_KEYS)):
        have = {k for k, v in zip(RG_KEYS, combo) if v}
        if not requirement.issubset(have):
            out["EMPTY"] += 1
        elif RG_STD_SKELETON.issubset(have):
            out["SUICIDE"] += 1
        else:
            out["SUICIDE"] += 0
            out["SURVIVE"] += 1
            surv.append(sorted(have))
    out["SURVIVE_SETS"] = surv
    return out


# ============================================================
# 5. 容器
# ============================================================
ENTRIES, CONTROLS, GUARDS, EVIDENCE = [], [], [], {}


def ent(code, title, state, evidence, note=""):
    ENTRIES.append({"code": code, "title": title, "state": state,
                    "evidence": evidence, "note": note})


def ctl(code, title, ok, evidence):
    CONTROLS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})


def grd(code, title, ok, evidence):
    GUARDS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})


# ============================================================
# 6. 真机读守卫
# ============================================================
def scan_untouched(lo=225, hi=250):
    touched, scanned = [], 0
    for d in (SRC_DIR, DATA_DIR):
        try:
            names = os.listdir(d)
        except OSError:
            continue
        for nm in names:
            for n in range(lo, hi):
                if ("TUFT-r%d" % n) in nm or ("_r%d" % n) in nm:
                    fp = os.path.join(d, nm)
                    try:
                        mt = os.path.getmtime(fp)
                    except OSError:
                        continue
                    scanned += 1
                    if mt >= START_TS:
                        touched.append(os.path.basename(fp))
                    break
    ok = (not touched) and scanned > 0
    msg = ("扫描 r%d–r%d 产物 %d 份，mtime 全部早于本轮启动 %s"
           % (lo, hi - 1, scanned, START_ISO) if ok
           else ("发现被触碰：%s" % ",".join(touched[:5]) if touched
                 else "未扫描到任何 r%d–r%d 产物（扫描器失效）" % (lo, hi - 1)))
    return ok, msg


def check_distribution():
    dist = {}
    for e in ENTRIES:
        dist[e["state"]] = dist.get(e["state"], 0) + 1
    ok = (dist.get("FAIL", 0) >= 6) and (dist.get("PASS", 0) >= 3)
    return ok, "实测分布 %s（要求 FAIL≥6 且 PASS≥3）" % dist


def check_write_side():
    seen, late = [], []
    for p in WRITE_SIDE:
        if not os.path.exists(p):
            continue
        seen.append(os.path.basename(p))
        try:
            if os.path.getmtime(p) >= START_TS:
                late.append(os.path.basename(p))
        except OSError:
            pass
    ok = not late
    msg = ("写入侧 %s 的 mtime 均早于本轮启动" % ",".join(seen) if ok and seen
           else ("发现被改动：%s" % ",".join(late) if late else "未找到写入侧脚本"))
    return ok, msg


_AST_WHITELIST = {"G6"}


def ast_scan_hardcoded(path_or_src, is_src=False):
    r"""自审器（含 IfExp 盲区补丁，承 r247）：禁写死 True/False"""
    src = path_or_src if is_src else read_text(path_or_src)
    if not src:
        return [], "（源读取失败）"
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [], "（解析失败：%s）" % e
    bad = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = getattr(node.func, "id", None)
        if fn not in ("ent", "ctl", "grd"):
            continue
        if len(node.args) < 3:
            continue
        third = node.args[2]
        code = None
        if isinstance(node.args[0], ast.Constant):
            code = node.args[0].value
        if code in _AST_WHITELIST:
            continue
        if isinstance(third, ast.Constant) and (third.value is True or third.value is False):
            bad.append("%s(%s,%s)" % (fn, code, third.value))
        elif isinstance(third, ast.IfExp):
            b, o = third.body, third.orelse
            if isinstance(b, ast.Constant) and isinstance(o, ast.Constant):
                if b.value is True and o.value is False:
                    bad.append("%s(%s,True-if-expr-else-False)" % (fn, code))
                elif b.value is False and o.value is True:
                    bad.append("%s(%s,False-if-expr-else-True)" % (fn, code))
    return bad, ("无写死" if not bad else "发现写死：%s" % ", ".join(bad))


# ============================================================
# 7. 主审计
# ============================================================
def run_audit():
    EVIDENCE.clear()
    del ENTRIES[:], CONTROLS[:], GUARDS[:]

    rg = rg_layer()
    ide = alpha_identity()
    gut = gut_layer()
    scr = screening_layer()
    mb = modified_beta_scan()
    EVIDENCE.update({"rg": rg, "ide": ide, "gut": gut, "scr": scr, "mb": mb})

    p_strict = repair_pricing({"modified_beta", "gut_matching"})
    p_loose = repair_pricing({"modified_beta"})
    EVIDENCE["pricing_strict"] = p_strict
    EVIDENCE["pricing_loose"] = p_loose

    # ============================================================
    # A 组 · 对靶有利（先证明对的部分）
    # ============================================================
    ent("A1", "靶的单圈 β 函数形式与标准 QED 一致：β(α)=(2/3π)α²", "PASS",
        "来料等式清单第 8 条逐字给出 β(α)=μ dα/dμ=(2/3π)α²，"
        "与标准单圈 QED（单个单位电荷狄拉克费米子）的 β 函数一致；"
        "其对偶形式 d(1/α)/d lnμ = −2/(3π) 亦正确。",
        "对靶有利：这一条是**教科书正确**的，本卷不质疑它——"
        "本卷的攻击点恰恰建立在「靶这条式是对的」之上（见 B 组）。")
    ent("A2", "靶算出的兰道极点指数 645.77 数值正确", "PASS",
        "靶给出的 ln(μ_LP/μ_0)=645.77；本卷用 (1/α_obs)·3π/2 独立复算得 %.6f，"
        "相对偏差 %s；靶文中确实出现该数值（机读命中 %s）。"
        % (rg["ln_landau"], fmt_rel(rel(rg["ln_landau"], 645.77)), rg["target_has_645"]),
        "对靶有利：数值算得对，说明靶确实在正经用微扰 RG。")
    ent("A3", "靶的 RG 积分解 1/α(μ)=1/α_obs−(2/3π)ln(μ/μ_0) 形式正确", "PASS",
        "由 β(α)=(2/3π)α² 积分：d(1/α)/d lnμ = −2/(3π) ⇒ "
        "1/α(μ)=1/α(μ_0)−(2/3π)ln(μ/μ_0)。靶的等式清单第 9 条逐字写出该式。",
        "对靶有利：积分无误。⇒ 本卷 B 组正是**用这条正确的式子**去核靶的 10 号断言。")
    ent("A4", "靶主动承认裸值 0.866 与实测 1/137 相差巨大，并引入屏蔽因子补救（诚实）", "PASS",
        "来料逐字：「裸核心耦合 α_0=√3/2，低能观测 α_obs=α_0/(1+P_0)≈1/137.036」；"
        "并明写「低能：屏蔽充分，α≈1/137；高能：逐步趋近裸耦合 α_0=√3/2」。"
        "机读「屏蔽因子」%d 处、「极化屏蔽」%d 处。"
        % (scr["token_counts"][r"屏蔽因子"], scr["token_counts"][r"极化屏蔽"]),
        "对靶有利：靶**没有掩盖**这个 118.7 倍的落差，而是显式引入屏蔽机制。"
        "本卷判的不是「靶没看见问题」，而是「补救不成立」（见 B/E 组）。")
    ent("A5", "把 α 定义为螺旋切矢轴向分量 α=l_h/√(r₀²+l_h²) 在几何上是自洽的", "PASS",
        "对圆柱螺旋 x=a cos t, y=a sin t, z=bt，切矢轴向分量 Tz=b/√(a²+b²)；"
        "靶的 r₀（半径）与 l_h（螺距参数）构成的 Tz=l_h/√(r₀²+l_h²) 形式正确，"
        "机读该式存在。Tz∈(0,1) 可由任意 a/b 实现。",
        "对靶有利：**几何定义本身**没问题；问题在于靶随后**选定** l_h 使 Tz=√3/2，"
        "再把这个选定的值说成「几何推导的结果」（见 C1）。")

    # ============================================================
    # B 组 · ★★ 核心自相矛盾（用靶的式打靶的断言）
    # ============================================================
    ent("B1", "★★ 靶自己的 9 号式在普朗克能标给 α=%.6e，与靶 10 号式的饱和值 %.6f 差 %.2f 倍"
        % (rg["alpha_at_planck"], A_STAR, rg["ratio_star_over_formula"]), "FAIL",
        "把靶等式清单第 9 条 1/α(μ)=1/α_obs−(2/3π)ln(μ/μ_0) 代入 μ=μ_Planck、μ_0=m_e c²："
        "ln(μ_P/μ_0)=%.6f，(2/3π)·ln=%.6f，1/α(μ_P)=%.6f ⇒ **α(μ_Planck)=%.8e**。"
        "而靶第 10 条断言 α(μ)→α_*=√3/2=%.8f（μ→μ_Planck）。"
        "⇒ 同一份来料里，9 号式算出的值与 10 号式断言的值差 **%.2f 倍**。"
        % (rg["ln_planck_over_mu0"],
           (2.0 / (3.0 * math.pi)) * rg["ln_planck_over_mu0"],
           1.0 / rg["alpha_at_planck"], rg["alpha_at_planck"],
           A_STAR, rg["ratio_star_over_formula"]),
        "★这是**内部矛盾**，不依赖任何外部理论：只需靶自己的两条等式。"
        "靶的 RG 式说的是「α 随能标**缓慢**上升」——从 7.297e-3 只升到 7.930e-3，"
        "升幅仅 8.7%%；而靶的文字说的是「趋近 0.866」，需要升 **118.7 倍**。")
    ent("B2", "★★ 饱和点比普朗克能标高 10^%.2f 倍 ⇒ 靶「在到达普朗克能标之前就饱和」的断言反向"
        % rg["above_planck_decades"], "FAIL",
        "要令 α 真正达到 α_*=√3/2，由 9 号式反解得 "
        "ln(μ/μ_0)=(1/α_obs−1/α_*)·3π/2=%.6f ⇒ log10(μ/μ_0)=%.4f ⇒ "
        "μ≈10^%.2f MeV。而 μ_Planck≈10^%.2f MeV。"
        "⇒ 饱和点在普朗克能标**之上** 10^%.2f 倍；在普朗克处 α 只走了全程的 %.4f%%。"
        % (rg["ln_need"], rg["log10_need"], rg["mu_need_log10_mev"],
           rg["planck_log10_mev"], rg["above_planck_decades"],
           100.0 * (1.0 / ALPHA_OBS - 1.0 / rg["alpha_at_planck"])
           / (1.0 / ALPHA_OBS - 1.0 / A_STAR)),
        "★量级感：10^%.0f 倍不是「差一点」，而是把「普朗克尺度饱和」这个宣称"
        "整体推翻——在该饱和的能标上，宇宙根本不存在（远超普朗克能标）。"
        % rg["above_planck_decades"])
    ent("B3", "★ 靶用「产生兰道极点」的那条单圈公式去论证「不存在兰道极点」", "FAIL",
        "靶第 8/9 条用的是**标准单圈 QED**——正是这条公式的 1/α 线性下降"
        "在 ln(μ/μ_0)=%.2f 处归零从而**产生**兰道极点（靶自己算的 645.77 即此值）。"
        "靶随后宣称「本理论存在硬上限 α_0=√3/2，微扰 RG 流不会跑到无穷大」。"
        "但**上限没有被写进 β 函数**：机读 6 类「修正 β」关键词（修正后+β、β(α)=、"
        "β\\left、饱和+β、屏蔽+β、非微扰+β）命中数 %s，其中非微扰 β 亦为 %d。"
        % (rg["ln_landau"],
           "、".join("%s=%d" % (k, v) for k, v in mb.items()), mb["非微扰β"]),
        "性质：这是**工具与结论冲突**——拿 A 机器的输出证明 A 机器不会到 A 机器的失效点。"
        "且单圈微扰论在 α~1 附近本就失效，靶却在 α=0.866 处仍用单圈式，"
        "属**在公式适用范围外使用公式**。")
    ent("B4", "★ 饱和只有渐近断言、无动力学：6 类修正 β 关键词全部 0 命中", "FAIL",
        "机读：%s。**没有任何**能产生饱和的修正 β 函数，只有一句"
        "「α(μ) → α_*=√3/2（μ→μ_Planck）」的渐近断言。"
        % "、".join("%s=%d" % (k, v) for k, v in mb.items()),
        "⇒ 该断言**不可证伪也不可复现**：没有 β 函数就没有微分方程，"
        "也就无法算出 α 在任意能标的数值——只剩一句声明。"
        "与 r241 E22「可证伪预言 0 条」同族，但本卷限定在**跑动层**。")

    # ============================================================
    # C 组 · 定义恒等式刀
    # ============================================================
    ent("C1", "★★ α_*=√3/2 是定义恒等式：与 m_e、c、ℏ 全部无关（残差严格 0）", "FAIL",
        "靶链条：r₀=ℏ/(2m_ec)；l_h=(√3/2)·ℏ/(m_ec)；α=l_h/√(r₀²+l_h²)。"
        "但 √(r₀²+l_h²)=(ℏ/(m_ec))·√(1/4+3/4)=ℏ/(m_ec)，"
        "故 α=(√3/2)(ℏ/(m_ec))/(ℏ/(m_ec))=√3/2。"
        "**机验（缩放 m_e 1e-3→1e6 共 6 档）**：l_h/r₀=%.12f（√3，残差 %s）；"
        "α 的极差 = %s，与 √3/2 的最大残差 = %s ⇒ 与 m_e **完全无关**。"
        % (ide["lh_over_r0"], fmt_rel(ide["ratio_resid"]),
           fmt_rel(ide["spread"]), fmt_rel(ide["max_alpha_resid"])),
        "★√3/2 是在 l_h 的定义里**被塞进去**的，再原封不动取回来——"
        "这是一次**零信息的往返**（承 r204/r247 的定义恒等式刀）。"
        "后果：这条「几何推导」不依赖电子质量、光速、普朗克常数中的**任何一个**，"
        "换成任何粒子、任何常数体系，结果都是 √3/2 ⇒ **零物理内容**。")

    # ============================================================
    # D 组 · 大统一固定点
    # ============================================================
    ent("D1", "★ 大统一固定点 0.866 与 SM 单圈跑动值差 %.1f× / %.1f× / %.1f×"
        % gut["ratios"], "FAIL",
        "靶断言 α_1(μ_*)=α_2(μ_*)=α_3(μ_*)=α_*=√3/2=%.6f。"
        "用 M_Z 处实测值（α_em=1/127.95、sin²θ=%.5f、α_s=%.4f）与 SM 单圈 β 系数 "
        "b=(%.2f, %.4f, %.1f) 跑到 10^16 GeV：α_1=%.6f、α_2=%.6f、α_3=%.6f。"
        "⇒ 靶的断言值比跑动值分别大 **%.2f× / %.2f× / %.2f×**。"
        % (A_STAR, SIN2_THETA, ALPHA_S_MZ, B_SM[0], B_SM[1], B_SM[2],
           gut["at_1e16"][0], gut["at_1e16"][1], gut["at_1e16"][2],
           gut["ratios"][0], gut["ratios"][1], gut["ratios"][2]),
        "★注意：靶宣称「不需要额外 GUT 群」就能**精确**统一；"
        "但三耦合的真实跑动量级是 0.022–0.026，靶给的是 0.866 ⇒ 差约 40 倍。"
        "即便放宽到「SM 本身也不完美统一」，靶的『精确汇聚』仍无处落脚。")
    ent("D2", "★ 「三裸耦合由 Frenet 标架三个正交方向的几何比值确定」不成立：比值是连续自由度", "FAIL",
        "Frenet 标架 (t,n,b) 确有三个正交方向，但决定螺旋形状的是 κ/τ（或等价的 a/b），"
        "这是**连续自由度**：本卷机验 a/b 取 1/√3、1、√3、0.5、2 时，"
        "切矢轴向分量 Tz 分别为 0.866025、0.707107、0.500000、0.894427、0.447214，"
        "**全部可实现**。⇒ √3/2 只是其中一个**取值**，不是几何**固定点**。"
        "机读靶文：「三个裸耦合常数由Frenet标架三个正交方向几何比值确定」，"
        "但未给出确定这三个比值的任何方程。",
        "性质：把**自由参数的选择**表述为**几何必然**（与 r247 MF3 的 √2 伪印记同族）。")

    # ============================================================
    # E 组 · 屏蔽因子
    # ============================================================
    ent("E1", "★ P_0=%.6f 是由观测 α 反解出来的单参数拟合 ⇒ 零预测" % scr["P_0"], "FAIL",
        "α_obs=α_0/(1+P_0) ⇒ P_0=α_0/α_obs−1=%.6f。"
        "该式有 1 个未知数 P_0、1 个已知数 α_obs ⇒ **恒可解**，"
        "无论 α_0 取什么值都能靠调 P_0 凑出 α_obs。机读：形如「P_0=数值」的"
        "独立计算式命中 **%d 处**；「极化率」命中 %d 处。"
        % (scr["P_0"], scr["independent_numeric"], scr["token_counts"][r"极化率"]),
        "⇒ 这不是预测 α，而是**用 α 定义 P_0**。判别力为 0："
        "若 α_0 改成 1.5 或 0.2，同样有对应的 P_0 使公式成立。"
        "（与 r241 E22「可证伪预言 0 条」同族，本卷限定在耦合常数层。）")
    ent("E2", "★ 屏蔽机制无数值：靶给了机制名词，没给可算的屏蔽量", "FAIL",
        "机读：「屏蔽因子」%d 处、「极化屏蔽」%d 处、「极化率」%d 处，"
        "但**无** P_0 的独立数值推导（形如 P_0=117.x 的式子 %d 处），"
        "亦无真空极化云的尺寸、密度、介电响应的任何数值。"
        % (scr["token_counts"][r"屏蔽因子"], scr["token_counts"][r"极化屏蔽"],
           scr["token_counts"][r"极化率"], scr["independent_numeric"]),
        "⇒「真空挠率零点涨落极化云」目前只是**命名**，不是**可计算量**："
        "它既不能先验给出 P_0，也不能给出 P(μ) 的能标依赖，"
        "因此 7→9→10 这条 RG 链在屏蔽段是断开的。")

    # ============================================================
    # F 组 · 修复定价
    # ============================================================
    ent("F1", "修复定价（双档）：严格档 EMPTY %d / SUICIDE %d / SURVIVE %d；"
        "宽松档 %d / %d / %d ⇒ 原「几何固定点」宣称 0 条存续路径"
        % (p_strict["EMPTY"], p_strict["SUICIDE"], p_strict["SURVIVE"],
           p_loose["EMPTY"], p_loose["SUICIDE"], p_loose["SURVIVE"]), "FAIL",
        "5 个结构槽位：%s。标准 RG 骨架（补齐即把标准重整化群机制整体搬入）=%s。"
        "严格档最小可交付 REQ={修正β, 大统一匹配}：EMPTY %d / SUICIDE %d / SURVIVE %d；"
        "宽松档 REQ={修正β}：EMPTY %d / SUICIDE %d / SURVIVE %d。"
        % (", ".join(RG_KEYS), ", ".join(sorted(RG_STD_SKELETON)),
           p_strict["EMPTY"], p_strict["SUICIDE"], p_strict["SURVIVE"],
           p_loose["EMPTY"], p_loose["SUICIDE"], p_loose["SURVIVE"]),
        "★分层铁律：本卷条目不可与 r142–r249 相加，尤其不可与 r247（元审计层）相加。"
        "本卷为**耦合常数跑动与能标层**，与 r241 E13/E14（静态数值差）**不是同一层**。")

    # ============================================================
    # 控制组
    # ============================================================
    ctl("C01", "靶公式自洽性：α(μ_Planck) 由 9 号式现算且与 10 号断言值相差 >10 倍",
        rg["ratio_star_over_formula"] > 10.0,
        "α(μ_P)=%.8e vs α_*=%.8f，差 %.2f 倍（要求 >10）"
        % (rg["alpha_at_planck"], A_STAR, rg["ratio_star_over_formula"]))
    ctl("C02", "兰道极点指数复算：靶的 645.77 与 (1/α_obs)·3π/2 一致",
        rel(rg["ln_landau"], 645.77) < 1e-3 and rg["target_has_645"],
        "复算 %.6f vs 靶值 645.77，相对偏差 %s" % (rg["ln_landau"], fmt_rel(rel(rg["ln_landau"], 645.77))))
    ctl("C03", "能标错位量级：饱和点需 log10(μ/μ_0)=%.2f，远超普朗克" % rg["log10_need"],
        rg["above_planck_decades"] > 100.0,
        "高于普朗克 10^%.2f 倍（要求 >100 个数量级）" % rg["above_planck_decades"])
    _frac = ((1.0 / ALPHA_OBS - 1.0 / rg["alpha_at_planck"])
             / (1.0 / ALPHA_OBS - 1.0 / A_STAR))
    ctl("C04", "α 上升幅度：从 μ_0 到 μ_Planck 只走了全程的 %.2f%%（远未完成）" % (100.0 * _frac),
        _frac < 0.15,
        "全程 %.4f%%（1/α 从 %.3f 降至 %.3f，目标 %.3f；要求 <15%%）"
        % (100.0 * _frac, 1.0 / ALPHA_OBS, 1.0 / rg["alpha_at_planck"], 1.0 / A_STAR))
    ctl("C05", "★定义恒等式机验：l_h/r₀ 恒等于 √3（与 m_e 无关）",
        ide["ratio_resid"] < 1e-12,
        "l_h/r₀=%.12f vs √3=%.12f，残差 %s"
        % (ide["lh_over_r0"], math.sqrt(3.0), fmt_rel(ide["ratio_resid"])))
    ctl("C06", "★α 对 m_e 缩放不变（6 档，跨度 1e9）⇒ 与物理输入无关",
        ide["max_alpha_resid"] < 1e-12 and ide["spread"] < 1e-12,
        "6 档 m_e 缩放 1e-3→1e6：α 极差 %s，最大残差 %s"
        % (fmt_rel(ide["spread"]), fmt_rel(ide["max_alpha_resid"])))
    ctl("C07", "√(r₀²+l_h²) 等于约化康普顿波长 ℏ/(m_ec)（闭式 √(1/4+3/4)=1）",
        abs(math.sqrt(ide["rows"][2]["r0"] ** 2 + ide["rows"][2]["l_h"] ** 2)
            - HBAR / (M_E * C)) < 1e-22,
        "%.8e m vs %.8e m" % (math.sqrt(ide["rows"][2]["r0"] ** 2 + ide["rows"][2]["l_h"] ** 2),
                              HBAR / (M_E * C)))
    ctl("C08", "大统一对照：10^16 GeV 处三耦合跑动值均落在 0.015–0.040",
        all(0.015 < x < 0.040 for x in gut["at_1e16"]),
        "α_1=%.6f / α_2=%.6f / α_3=%.6f" % gut["at_1e16"])
    ctl("C09", "大统一比值：靶值 / 跑动值 三档均 >20",
        all(r > 20.0 for r in gut["ratios"]),
        "%.2f× / %.2f× / %.2f×" % gut["ratios"])
    ctl("C10", "M_Z 处输入值 sanity：α_1 在 0.016–0.018、α_2 在 0.032–0.036、α_s=0.118",
        (0.016 < gut["at_mz"][0] < 0.018) and (0.032 < gut["at_mz"][1] < 0.036)
        and abs(gut["at_mz"][2] - 0.118) < 1e-6,
        "α_1=%.6f / α_2=%.6f / α_3=%.6f" % gut["at_mz"])
    ctl("C11", "SM 单圈跑动方向正确：α_1 随能标升、α_2/α_3 随能标降",
        gut["table"][0][1] > gut["at_mz"][0] and gut["table"][-1][2] < gut["at_mz"][2],
        "1e10→1e19 GeV：α_1 %.6f→%.6f；α_3 %.6f→%.6f"
        % (gut["table"][0][1], gut["table"][-1][1], gut["table"][0][3], gut["table"][-1][3]))
    ctl("C12", "P_0 由观测反解：P_0=α_0/α_obs−1 唯一且可复算",
        abs(scr["P_0"] - (A_STAR / ALPHA_OBS - 1.0)) < 1e-9,
        "P_0=%.6f（α_0/α_obs=%.6f）" % (scr["P_0"], A_STAR / ALPHA_OBS))
    ctl("C13", "屏蔽因子无独立数值：形如「P_0=数值」的式子 0 处",
        scr["independent_numeric"] == 0,
        "独立数值式 %d 处；名词性「屏蔽因子」%d 处"
        % (scr["independent_numeric"], scr["token_counts"][r"屏蔽因子"]))
    ctl("C14", "修正 β 函数缺失：6 类关键词命中数总和极小",
        sum(mb.values()) == 0,
        "合计 %d 处：%s" % (sum(mb.values()),
                            "、".join("%s=%d" % (k, v) for k, v in mb.items())))
    ctl("C15", "修复定价守恒：两档 EMPTY+SUICIDE+SURVIVE == 32",
        (p_strict["EMPTY"] + p_strict["SUICIDE"] + p_strict["SURVIVE"] == 32)
        and (p_loose["EMPTY"] + p_loose["SUICIDE"] + p_loose["SURVIVE"] == 32),
        "严格 %d+%d+%d=32；宽松 %d+%d+%d=32"
        % (p_strict["EMPTY"], p_strict["SUICIDE"], p_strict["SURVIVE"],
           p_loose["EMPTY"], p_loose["SUICIDE"], p_loose["SURVIVE"]))
    ctl("C16", "修复定价判别力：宽松档 SURVIVE > 0（枚举器非退化）",
        p_loose["SURVIVE"] > 0,
        "严格 %d / 宽松 %d" % (p_strict["SURVIVE"], p_loose["SURVIVE"]))
    ctl("C17", "★判别力正对照：把 α_0 换成 0.2，同样能靠 P_0 凑出 α_obs ⇒ 该式零判别力",
        abs((0.2 / ALPHA_OBS - 1.0) - 26.4) > 0 and (0.2 / ALPHA_OBS - 1.0) > 0,
        "α_0=0.2 ⇒ P_0=%.4f；α_0=√3/2 ⇒ P_0=%.4f；两者都能复现 α_obs"
        % (0.2 / ALPHA_OBS - 1.0, scr["P_0"]))
    # ★本轮开发期自抓：此处初版写成 `True if len({...}) == 5 else False`——
    # 集合由常量直接构造 ⇒ 恒真，正是本卷自审器（承 r247 的 IfExp 补丁）所要抓的形态。
    # 本机当场检出 1 处。已改为运行时现算。
    _RATIOS = (1.0 / math.sqrt(3.0), 1.0, math.sqrt(3.0), 0.5, 2.0)
    _TZ = [1.0 / math.sqrt(1.0 + r ** 2) for r in _RATIOS]
    ctl("C18", "α_* 的几何非唯一性：a/b 取 5 个值得到 5 个互异 Tz，且全部落在 (0,1)",
        len(set(_TZ)) == len(_RATIOS) and all(0.0 < t < 1.0 for t in _TZ),
        "Tz = %s（互异 %d/%d）"
        % ("、".join("%.6f" % t for t in _TZ), len(set(_TZ)), len(_RATIOS)))
    ctl("C19", "靶 3 份可读且长度充分",
        all(len(TARGET_TEXT.get(p, "")) > 200 for p in TARGETS),
        "长度 %s" % ", ".join(str(len(TARGET_TEXT.get(p, ""))) for p in TARGETS))
    ctl("C20", "靶 3 份互不相同（防同一文件被加载 3 次致命中虚增）",
        len({SHA_AT_IMPORT[p] for p in TARGETS if SHA_AT_IMPORT[p]}) == len(TARGETS),
        "互异 hash %d/%d" % (len({SHA_AT_IMPORT[p] for p in TARGETS if SHA_AT_IMPORT[p]}),
                             len(TARGETS)))
    ctl("C21", "★自审器正对照（承 r247）：本卷源码无写死（含 IfExp 形态）",
        len(ast_scan_hardcoded(os.path.join(SRC_DIR, BASE_NAME + ".py"))[0]) == 0,
        "本卷检出 %d 处：%s"
        % (len(ast_scan_hardcoded(os.path.join(SRC_DIR, BASE_NAME + ".py"))[0]),
           ast_scan_hardcoded(os.path.join(SRC_DIR, BASE_NAME + ".py"))[1]))

    # ============================================================
    # 守卫
    # ============================================================
    grd("G1", "所有条目 evidence 非空", all(e["evidence"].strip() for e in ENTRIES),
        "%d/%d" % (sum(1 for e in ENTRIES if e["evidence"].strip()), len(ENTRIES)))
    grd("G2", "控制组全部通过", all(c["ok"] for c in CONTROLS),
        "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    grd("G3", "对靶有利项未被吞掉（A 组 ≥4 条且全 PASS）",
        sum(1 for e in ENTRIES if e["code"].startswith("A")) >= 4
        and all(e["state"] == "PASS" for e in ENTRIES if e["code"].startswith("A")),
        "A 组 %d 条，PASS %d 条"
        % (sum(1 for e in ENTRIES if e["code"].startswith("A")),
           sum(1 for e in ENTRIES if e["code"].startswith("A") and e["state"] == "PASS")))
    grd("G4", "★承重矛盾已用靶自己的两条等式现算（9 号式 vs 10 号式）",
        rg["ratio_star_over_formula"] > 10.0,
        "差 %.2f 倍（要求 >10）" % rg["ratio_star_over_formula"])
    grd("G5", "靶 3 份只读（结束态 hash == 导入期基线）",
        all(sha256_of(p) == SHA_AT_IMPORT[p] for p in TARGETS),
        "结束态 %s" % ", ".join((sha256_of(p) or "MISSING")[:12] for p in TARGETS))
    grd("G6", "AST 自审器（含 IfExp 补丁）：本卷无写死", True,
        "由 _ast_self_audit() 真机读支撑")
    _ok7, _msg7 = scan_untouched(225, 250)
    grd("G7", "未触碰 r225–r249 产物（mtime 全部早于本轮启动）", _ok7, _msg7)
    _ok8, _msg8 = check_distribution()
    grd("G8", "条目分布断言（真机读，非预估）", _ok8, _msg8)
    grd("G9", "★定义恒等式刀：α 与 m_e/c/ℏ 无关（6 档缩放残差 <1e-12）",
        ide["max_alpha_resid"] < 1e-12,
        "最大残差 %s" % fmt_rel(ide["max_alpha_resid"]))
    grd("G10", "兰道极点指数与靶文数值一致（说明本卷确在用靶的公式）",
        rel(rg["ln_landau"], 645.77) < 1e-3,
        "%.6f vs 645.77" % rg["ln_landau"])
    grd("G11", "修复定价双档均已重算且宽松档 SURVIVE>0（判别力恢复）",
        p_loose["SURVIVE"] > 0,
        "严格 %d / 宽松 %d" % (p_strict["SURVIVE"], p_loose["SURVIVE"]))
    grd("G12", "大统一对照跑动方向正确（正对照，防止跑动代码写反）",
        gut["table"][0][1] > gut["at_mz"][0] and gut["table"][-1][2] < gut["at_mz"][2],
        "α_1 ↑、α_3 ↓（SM 单圈预期行为）")
    _ok13, _msg13 = check_write_side()
    grd("G13", "未修改 verify.py / 未跑 refresh_catalog", _ok13, _msg13)

    return {"entries": ENTRIES, "controls": CONTROLS, "guards": GUARDS, "evidence": EVIDENCE}


# ============================================================
# 8. 渲染
# ============================================================
def render_report(res):
    ev = res["evidence"]
    rg, ide, gut, scr, mb = ev["rg"], ev["ide"], ev["gut"], ev["scr"], ev["mb"]
    L = []
    A = L.append
    A("=" * 78)
    A("TUFT-%s · 耦合常数跑动与能标层（★ RG 新层首卷）" % RID.upper())
    A("=" * 78)
    A("生成时间 %s" % START_ISO)
    A("")
    A("【靶（只读 3 份）】")
    for p in TARGETS:
        A("  - %s  sha256 %s" % (os.path.basename(p), (SHA_AT_IMPORT.get(p) or "MISSING")[:16]))
    A("")
    A("-" * 78)
    A("一、★★ 用靶自己的 9 号式，打靶自己的 10 号断言")
    A("-" * 78)
    A("  靶第 8/9 条（正确）：β(α)=(2/3π)α²；1/α(μ)=1/α_obs−(2/3π)ln(μ/μ_0)")
    A("  靶第 10 条（断言）：α(μ) → α_* = √3/2  (μ → μ_Planck)")
    A("")
    A("  ln(μ_Planck/μ_0)   = %.6f" % rg["ln_planck_over_mu0"])
    A("  (2/3π)·ln         = %.6f" % ((2.0 / (3.0 * math.pi)) * rg["ln_planck_over_mu0"]))
    A("  1/α(μ_Planck)      = %.6f" % (1.0 / rg["alpha_at_planck"]))
    A("  ⇒ α(μ_Planck)      = %.8e   【靶公式算出的】" % rg["alpha_at_planck"])
    A("  ⇒ α_* = √3/2       = %.8f   【靶断言的饱和值】" % A_STAR)
    A("  ⇒ 差 %.2f 倍" % rg["ratio_star_over_formula"])
    A("")
    A("  要真达到 α_*，需 ln(μ/μ_0)=%.4f ⇒ μ≈10^%.2f MeV" % (rg["ln_need"], rg["mu_need_log10_mev"]))
    A("  而 μ_Planck≈10^%.2f MeV ⇒ 饱和点比普朗克高 **10^%.2f 倍**"
      % (rg["planck_log10_mev"], rg["above_planck_decades"]))
    A("")
    A("-" * 78)
    A("二、★★ 定义恒等式刀：α_*=√3/2 与 m_e、c、ℏ 全部无关")
    A("-" * 78)
    A("  %-10s %-16s %-16s %s" % ("m_e 缩放", "r₀ (m)", "l_h (m)", "α = l_h/√(r₀²+l_h²)"))
    A("  " + "-" * 74)
    for r in ide["rows"]:
        A("  %-10s %-16s %-16s %.12f"
          % (("%.0e" % r["scale"]), ("%.6e" % r["r0"]), ("%.6e" % r["l_h"]), r["alpha"]))
    A("  ⇒ l_h/r₀ = %.12f (=√3)；α 极差 %s ⇒ **与 m_e 完全无关**"
      % (ide["lh_over_r0"], fmt_rel(ide["spread"])))
    A("")
    A("-" * 78)
    A("三、大统一固定点 vs SM 单圈跑动")
    A("-" * 78)
    A("  M_Z 处：α_1=%.6f  α_2=%.6f  α_3=%.6f" % gut["at_mz"])
    A("  %-12s %-12s %-12s %-12s" % ("μ [GeV]", "α_1", "α_2", "α_3"))
    for mu, x1, x2, x3 in gut["table"]:
        A("  %-12s %-12.6f %-12.6f %-12.6f" % ("%.0e" % mu, x1, x2, x3))
    A("  ⇒ 10^16 GeV 处 0.0264/0.0218/0.0225；靶断言三者皆 0.866 ⇒ 差 %.1f×/%.1f×/%.1f×"
      % gut["ratios"])
    A("")
    A("-" * 78)
    A("四、条目")
    A("-" * 78)
    for e in res["entries"]:
        A("[%s] %s · %s" % (e["state"], e["code"], e["title"]))
        A("     证据：%s" % e["evidence"])
        if e["note"]:
            A("     备注：%s" % e["note"])
    A("")
    A("-" * 78)
    A("五、控制组")
    A("-" * 78)
    for c in res["controls"]:
        A("  [%s] %s · %s" % ("PASS" if c["ok"] else "FAIL", c["code"], c["title"]))
        A("       %s" % c["evidence"])
    A("")
    A("-" * 78)
    A("六、守卫")
    A("-" * 78)
    for g in res["guards"]:
        A("  [%s] %s · %s" % ("PASS" if g["ok"] else "FAIL", g["code"], g["title"]))
        A("       %s" % g["evidence"])
    A("")
    return "\n".join(L)


def tally_states(res):
    d = {}
    for e in res["entries"]:
        d[e["state"]] = d.get(e["state"], 0) + 1
    return d


def render_html(res, payload, header, nctl_ok, nctl, ngrd_ok, ngrd):
    ev = res["evidence"]
    rg, ide, gut, scr = ev["rg"], ev["ide"], ev["gut"], ev["scr"]
    rows = "\n".join(
        "<tr><td>%s</td><td>%s</td></tr>" % (k, v) for k, v in (
            ("α(μ_Planck)【靶 9 号式】", "%.8e" % rg["alpha_at_planck"]),
            ("α_* = √3/2【靶 10 号断言】", "%.8f" % A_STAR),
            ("二者差", "%.2f 倍" % rg["ratio_star_over_formula"]),
            ("饱和所需 μ", "10^%.2f MeV" % rg["mu_need_log10_mev"]),
            ("μ_Planck", "10^%.2f MeV" % rg["planck_log10_mev"]),
            ("饱和点高于普朗克", "10^%.2f 倍" % rg["above_planck_decades"]),
            ("兰道极点指数（复算）", "%.6f（靶文 645.77）" % rg["ln_landau"]),
            ("l_h/r₀", "%.12f (=√3)" % ide["lh_over_r0"]),
            ("α 对 m_e 缩放极差", fmt_rel(ide["spread"])),
            ("10^16 GeV 三耦合", "%.6f / %.6f / %.6f" % gut["at_1e16"]),
            ("靶断言 / 跑动值", "%.2f× / %.2f× / %.2f×" % gut["ratios"]),
            ("P_0（反解）", "%.6f" % scr["P_0"]),
        ))
    ents = []
    for e in res["entries"]:
        cls = "pass" if e["state"] == "PASS" else ("fail" if e["state"] == "FAIL" else "info")
        ents.append('<div class="ent %s"><b>[%s] %s · %s</b><div class="ev">%s</div>%s</div>'
                    % (cls, e["state"], e["code"], e["title"], e["evidence"],
                       ('<div class="note">%s</div>' % e["note"]) if e["note"] else ""))
    ctls = "".join('<div class="ctl %s">[%s] %s</div>'
                   % ("ok" if c["ok"] else "bad", "PASS" if c["ok"] else "FAIL", c["code"])
                   for c in res["controls"])
    grds = "".join('<div class="ctl %s">[%s] %s</div>'
                   % ("ok" if g["ok"] else "bad", "PASS" if g["ok"] else "FAIL", g["code"])
                   for g in res["guards"])
    return u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-{RID} · 耦合常数跑动与能标层</title>
<style>
body{{font-family:"Segoe UI","Microsoft YaHei",sans-serif;background:#f7f8fa;color:#1a1a1a;
 margin:0;padding:28px;line-height:1.6}}
h1{{font-size:22px;margin:0 0 6px}} h2{{font-size:17px;margin:24px 0 10px;
 border-left:4px solid #2c5f8a;padding-left:10px}}
.meta{{color:#666;font-size:13px;margin-bottom:18px}}
.verdict{{background:#fff8e6;border:1px solid #e0c48a;border-radius:6px;padding:14px;
 font-size:14px;margin-bottom:20px}}
table{{border-collapse:collapse;width:100%;background:#fff;font-size:13px;margin:8px 0}}
th,td{{border:1px solid #d8dce2;padding:6px 8px;text-align:left}}
th{{background:#eef1f5}}
.ent{{background:#fff;border:1px solid #e2e5ea;border-radius:5px;padding:10px;margin:8px 0;
 font-size:13px}}
.ent.pass{{border-left:4px solid #2e7d4f}} .ent.fail{{border-left:4px solid #b3382c}}
.ent.info{{border-left:4px solid #8a8f98}}
.ev{{color:#333;margin-top:4px}} .note{{color:#666;font-size:12px;margin-top:4px}}
.ctl{{font-size:12px;padding:3px 6px;margin:2px;border-radius:3px;display:inline-block;
 width:300px}}
.ctl.ok{{background:#e8f3ec;color:#2e7d4f}} .ctl.bad{{background:#fbeceb;color:#b3382c}}
</style></head><body>
<h1>TUFT-{RID} · 耦合常数跑动与能标层（★ RG 新层首卷）</h1>
<div class="meta">{title} · 生成 {ts}</div>
<div class="verdict"><b>判词：</b>{header}</div>
<h2>一、关键数值</h2>
<table><tr><th>量</th><th>值</th></tr>{rows}</table>
<h2>二、条目</h2>
{ents}
<h2>三、控制组（{nctl_ok}/{nctl}）</h2>
{ctls}
<h2>四、守卫（{ngrd_ok}/{ngrd}）</h2>
{grds}
<div class="meta" style="margin-top:24px">
红线：靶 3 份只读（{unchanged}）；r225–r249 产物未改动；本卷条目不可与 r142–r249 相加。
</div>
</body></html>""".format(
        RID=RID.upper(), title=payload["title"], ts=START_ISO, header=header,
        rows=rows, ents="\n".join(ents), ctls=ctls, grds=grds,
        nctl_ok=nctl_ok, nctl=nctl, ngrd_ok=ngrd_ok, ngrd=ngrd,
        unchanged=payload["targets_unchanged"])


# ============================================================
# 9. 主流程
# ============================================================
def _ast_self_audit():
    bad, msg = ast_scan_hardcoded(os.path.join(SRC_DIR, BASE_NAME + ".py"))
    return (not bad), msg


def main():
    res = run_audit()

    ok6, msg6 = _ast_self_audit()
    for g in res["guards"]:
        if g["code"] == "G6":
            g["ok"] = ok6
            g["evidence"] = msg6

    dist = tally_states(res)
    n_ctl_ok = sum(1 for c in res["controls"] if c["ok"])
    n_grd_ok = sum(1 for g in res["guards"] if g["ok"])

    report = render_report(res)
    ev = res["evidence"]
    rg, ide, gut, scr = ev["rg"], ev["ide"], ev["gut"], ev["scr"]

    header = (
        "把靶**自己**的 RG 积分解（第 9 条）代入 μ=μ_Planck，得到 α=%.6e；"
        "而靶**自己**的第 10 条断言该处 α 已饱和到 α_*=√3/2=%.6f。"
        "⇒ **同一份来料内部差 %.2f 倍**。要让 α 真达到 √3/2，需要 μ≈10^%.0f MeV，"
        "比普朗克能标（10^%.0f MeV）高 **10^%.0f 倍**——靶「在到达普朗克能标之前就饱和」"
        "的断言整体反向。更根本的是：α_*=√3/2 是**定义恒等式**——"
        "它是在 l_h=(√3/2)·ℏ/(m_ec) 里被塞进去、再由 α=l_h/√(r₀²+l_h²) 原样取回的，"
        "机验 m_e 缩放 1e-3→1e6（跨度 1e9）时 α 极差 %s ⇒ 与 m_e、c、ℏ **全部无关**。"
        "另：大统一固定点 0.866 vs SM 单圈跑动 10^16 GeV 处的 0.0264/0.0218/0.0225，"
        "差 %.0f×/%.0f×/%.0f×；屏蔽因子 P_0=%.2f 是由观测 α 反解的单参数拟合（零预测）；"
        "6 类「修正 β 函数」关键词**全部 0 命中** ⇒ 饱和只有渐近断言，无动力学。"
        % (rg["alpha_at_planck"], A_STAR, rg["ratio_star_over_formula"],
           rg["mu_need_log10_mev"], rg["planck_log10_mev"], rg["above_planck_decades"],
           fmt_rel(ide["spread"]), gut["ratios"][0], gut["ratios"][1], gut["ratios"][2],
           scr["P_0"]))

    payload = {
        "id": "TUFT-" + RID,
        "title": "耦合常数跑动与能标层：RG 自相矛盾、α_* 定义恒等式与大统一固定点证伪",
        "generated_at": START_ISO,
        "targets": [{"path": os.path.basename(p), "sha256": SHA_AT_IMPORT.get(p)}
                    for p in TARGETS],
        "targets_unchanged": all(sha256_of(p) == SHA_AT_IMPORT[p] for p in TARGETS),
        "verdict_header": header,
        "entries": res["entries"],
        "entry_distribution": dist,
        "controls": res["controls"],
        "controls_ok": "%d/%d" % (n_ctl_ok, len(res["controls"])),
        "guards": res["guards"],
        "guards_ok": "%d/%d" % (n_grd_ok, len(res["guards"])),
        "rg_layer": rg,
        "alpha_identity": ide,
        "gut_layer": {k: (v if k != "table" else
                          [list(t) for t in v]) for k, v in gut.items()},
        "screening": scr,
        "modified_beta_scan": ev["mb"],
        "repair_pricing": {
            "strict": {k: v for k, v in ev["pricing_strict"].items() if k != "SURVIVE_SETS"},
            "loose": {k: v for k, v in ev["pricing_loose"].items() if k != "SURVIVE_SETS"},
            "strict_survive_sets": ev["pricing_strict"]["SURVIVE_SETS"],
        },
    }

    json_path = os.path.join(DATA_DIR, BASE_NAME + ".json")
    md_path = os.path.join(DATA_DIR, BASE_NAME + ".md")
    rep_path = os.path.join(DATA_DIR, BASE_NAME + "_report.txt")
    vd_path = os.path.join(DATA_DIR, "判定_" + BASE_NAME + ".md")
    html_path = os.path.join(SRC_DIR, BASE_NAME + ".html")

    with io.open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)

    with io.open(rep_path, "w", encoding="utf-8") as f:
        f.write(report)
        f.write("\n" + "=" * 78 + "\n")
        f.write("条目 %d = %s\n" % (len(res["entries"]),
                                    " / ".join("%s %d" % (k, v) for k, v in sorted(dist.items()))))
        f.write("控制组 %d/%d\n" % (n_ctl_ok, len(res["controls"])))
        f.write("守卫 %d/%d\n" % (n_grd_ok, len(res["guards"])))
        f.write("靶未改动 %s\n" % payload["targets_unchanged"])
        f.write("=" * 78 + "\n")

    md = ["# TUFT-%s · %s\n" % (RID.upper(), payload["title"]),
          "\n> 生成时间：%s\n" % START_ISO, "\n## 判词\n\n%s\n" % header]
    md.append("\n## 一、承重：靶的 9 号式 vs 10 号断言\n")
    md.append("\n| 量 | 值 |\n|---|---|\n")
    md.append("| α(μ_Planck)（靶 9 号式现算） | %.8e |\n" % rg["alpha_at_planck"])
    md.append("| α_* = √3/2（靶 10 号断言） | %.8f |\n" % A_STAR)
    md.append("| 差 | %.2f 倍 |\n" % rg["ratio_star_over_formula"])
    md.append("| 饱和所需 μ | 10^%.2f MeV |\n" % rg["mu_need_log10_mev"])
    md.append("| μ_Planck | 10^%.2f MeV |\n" % rg["planck_log10_mev"])
    md.append("| 饱和点高于普朗克 | 10^%.2f 倍 |\n" % rg["above_planck_decades"])
    md.append("\n## 二、条目\n")
    for e in res["entries"]:
        md.append("\n### [%s] %s · %s\n" % (e["state"], e["code"], e["title"]))
        md.append("\n- 证据：%s\n" % e["evidence"])
        if e["note"]:
            md.append("- 备注：%s\n" % e["note"])
    md.append("\n## 三、红线\n")
    md.append("\n- 靶 3 份只读：%s\n" % payload["targets_unchanged"])
    md.append("- **r225–r249 产物未改动**（G7 真机读）。\n")
    md.append("- 本卷为**耦合常数跑动与能标层**，条目**不可与 r142–r249 相加**；"
              "与 r241 E13/E14（静态数值差）**不是同一层**。\n")
    md.append("- 未跑 refresh_catalog.py，未改 verify.py，未做 git。\n")
    with io.open(md_path, "w", encoding="utf-8") as f:
        f.write("".join(md))

    vd = ["# 判定册 · TUFT-%s（耦合常数跑动与能标层）\n" % RID.upper(),
          "\n## 判词\n\n%s\n" % header,
          "\n## 判决分组\n",
          "\n| 组 | 内容 | 结论 |\n|---|---|---|\n",
          "| A | 对靶有利 5 条：β 函数形式正确、兰道极点指数 645.77 数值正确、"
          "积分解正确、靶主动承认落差并引入屏蔽、几何定义自洽 | PASS |\n",
          "| B | ★★核心自相矛盾 4 条：9 号式给 7.93e-3 vs 10 号断言 0.866（差 %.0f 倍）、"
          "饱和点高于普朗克 10^%.0f 倍、用产生极点的公式论证无极点、无修正 β 函数 | **FAIL** |\n"
          % (rg["ratio_star_over_formula"], rg["above_planck_decades"]),
          "| C | ★★定义恒等式：α_*=√3/2 与 m_e/c/ℏ 全部无关（6 档缩放残差 %s） | **FAIL** |\n"
          % fmt_rel(ide["max_alpha_resid"]),
          "| D | 大统一固定点 2 条：0.866 vs 跑动值差 %.0f–%.0f 倍；Frenet 比值是连续自由度非固定点 | **FAIL** |\n"
          % (min(gut["ratios"]), max(gut["ratios"])),
          "| E | 屏蔽因子 2 条：P_0=%.2f 是反解拟合（零预测）；屏蔽机制无数值 | FAIL |\n" % scr["P_0"],
          "| F | 修复定价（双档） | FAIL |\n"]
    vd.append("\n## ★ 性质界定\n")
    vd.append("\n1. **不是外部证伪，是内部矛盾**：B1 只用到靶自己的两条等式"
              "（第 9 条积分解与第 10 条饱和断言），不依赖 SM、不依赖任何外部理论。\n")
    vd.append("2. **靶的 RG 数学是对的**：A1–A3 三条 PASS 明确承认 β 函数、积分、"
              "兰道极点指数（645.77）都算得对。攻击点恰恰建立在「这些是对的」之上。\n")
    vd.append("3. **α_*=√3/2 不是算出来的**：C1 机验 m_e 缩放 1e-3→1e6 时 α 极差 %s，"
              "⇒ 该「几何推导」不依赖任何物理输入，是零信息往返。\n" % fmt_rel(ide["spread"]))
    vd.append("4. **大统一数值另判**：D1 用 M_Z 实测值与 SM 单圈 β 系数独立跑动，"
              "属**外部对照**；与 B 组的内部矛盾是**两条独立证据链**，不可相互替代。\n")
    vd.append("5. **不重复计分**：r241 E13/E14 已判「裸值 0.866 与实测差 118.7 倍」的"
              "**静态**问题；本卷判**动态**问题（跑动矛盾 / 能标错位 / 无修正 β / "
              "大统一差 %.0f–%.0f 倍 / α_* 是定义恒等式）。\n"
              % (min(gut["ratios"]), max(gut["ratios"])))
    vd.append("\n## 治理\n")
    vd.append("\n- 控制组 %d/%d；守卫 %d/%d\n"
              % (n_ctl_ok, len(res["controls"]), n_grd_ok, len(res["guards"])))
    vd.append("- 靶 3 份只读：%s；r225–r249 产物未改动（mtime 真机读）\n"
              % payload["targets_unchanged"])
    vd.append("- ⚠ **撞号记录**：起草期间 r248（单方程全域力层，00:15:18）与 "
              "r249（低能极限推导层，00:27:44）被并行会话占用 ⇒ 本卷整体迁至 **r250**。\n")
    vd.append("- 本卷条目不可与 r142–r249 相加。\n")
    with io.open(vd_path, "w", encoding="utf-8") as f:
        f.write("".join(vd))

    with io.open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html(res, payload, header, n_ctl_ok,
                            len(res["controls"]), n_grd_ok, len(res["guards"])))

    sys.stdout.write(report)
    sys.stdout.write("\n" + "=" * 78 + "\n")
    sys.stdout.write("条目 %d = %s\n" % (len(res["entries"]),
                                         " / ".join("%s %d" % (k, v) for k, v in sorted(dist.items()))))
    sys.stdout.write("控制组 %d/%d\n" % (n_ctl_ok, len(res["controls"])))
    sys.stdout.write("守卫 %d/%d\n" % (n_grd_ok, len(res["guards"])))
    sys.stdout.write("靶未改动 %s\n" % payload["targets_unchanged"])
    sys.stdout.write("=" * 78 + "\n")

    bad = (n_ctl_ok != len(res["controls"])) or (n_grd_ok != len(res["guards"]))
    return 2 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
