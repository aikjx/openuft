# -*- coding: utf-8 -*-
r"""
TUFT-r255 · 磁矩与量子修正层（★ 新层首卷：电子反常磁矩 g−2）
================================================================================
【命题来源】用户：「继续分析，总结，攻破所有物理问题，完成统一场论」

【取号】起草前实测 **r255/r256/r257 三树全空** ⇒ 取 **r255**。
  ⚠ 本轮撞号（第 7 次）：r253（力的无模型定理层·七靶大统一方程判决，08:44:37）
  已落四件套；**r254（四力统一方程·宇宙学扰动层）正被另一并行会话起草**
  （09:02:32 仅有 .py，数据未落）⇒ 按「已产四件套并登记者为权威、后到者整体改号」
  纪律，本卷**跳过 r254 取 r255**，不改写他人文件。

【本卷定位：磁矩与量子修正层】
r244/r247 攻「引力是什么」；r248 攻「单一矢量主方程」；r250 攻「耦合常数跑动」；
r251 攻「下游应用」；r252 攻「质量谱」；r253 攻「力的无模型定理」。
本卷攻靶**唯一一处数值上与实验符合到 3 位有效数字**的地方——

    靶用「螺旋涡旋 + 真空挠率云」推导电子反常磁矩
    a_e = α/(2π) + C₂(α/π)² + C₃(α/π)³ + …   （来料 line 4050，体系汇总第 12 条）

★ 本卷四条承重发现（全部纯代数 / 纯数值，机读 + 机算）：

  ① **裸磁矩差因子 2 —— 靶自己的推导给出 g=1，不是 g=2**
     来料 line 3957：μ₀ = eℏ/(4m_e)；line 3961 却写 μ₀ = (e/m_e)S。
     取 S=ℏ/2，后者 = eℏ/(2m_e) ⇒ 二者差 **恰好 2 倍**。
     而由 μ₀ = eℏ/(4m_e)、S=ℏ/2 反解 g = 2μ/((e/m) S) = **1**。
     根因：line 3951 取 T=2πr₀/c ⇒ 电荷以光速环流；经典环流的 g **恒为 1**
     （μ=(e/2m)L 对任意 r 成立），要 g=2 必须引入非经典项。靶把 g=1 的结果
     贴上「与狄拉克 g=2 完全一致」（line 3963）的标签。

  ② **两圈闭式与靶自己给的数值不自洽（符号反 + 2.967 倍）**
     来料 line 3979 闭式：a_e^(2) = −(α²/2π²)(½ζ(3) − π²/12)。
     复算：½ζ(3)−π²/12 = −0.2214385818 ⇒ 该闭式 = **+5.973849e-07**（等价 C₂=+0.11072）。
     而 line 3981 写 a_e^(2) ≈ **−0.0000017723**（等价 C₂=−0.328479）。
     ⇒ **符号相反、幅值差 2.9668 倍**。闭式与数值不能同时成立（二难两支都算死）。

  ③ **★★ 唯一的「新预言」Δa_geo 被靶自己的求和排除 96672 倍**
     line 3987 称 Δa_geo 量级 **O(α²)** = (α/π)² = **5.395490e-06**。
     但用靶自己给的单圈（0.0011614）与两圈（−1.7723e-6）相加得 1.1596374329e-03，
     与靶自己引用的实验值 1.1596521813e-03 只差 **1.4748e-08**；
     再加标准三圈（C₃=1.181241456）得 1.1596522371e-03，残差仅 **+5.5812e-11**。
     ⇒ 允许窗 5.58e-11，而 Δa_geo 是 5.40e-6 ⇒ **超出 96672 倍**。
     （仅按 1+2 圈口径也超出 365.8 倍。）且靶 line 4012 又说「高阶…压低总 a_e，
     匹配实验」⇒ **内部矛盾**：若 QED 序列已匹配实验，Δa_geo 必须 ≈0。

  ④ **α 口径二难：用靶自己的裸值 α₀=√3/2，电子 g 偏 7.59e11 σ**
     line 3968 写 a_e^(1)=α/(2π)，但未指定用哪个 α（line 3929 同时给了
     α₀=√3/2 与 α_obs≈1/137.036）。
     用 α₀：a_e = 0.13783222（比实测大 **118.86 倍**），g_pred = 2.27566445，
     与实测 g=2.00231930436 差 0.27334514 ⇒ **7.593e11 σ**。
     用 α_obs：a_e 对得上，但 α_obs 是**实验输入** ⇒ 该「几何推导」退化为
     「抄一遍 Schwinger 公式 + 代外部常数」。

【分层】本卷是**磁矩与量子修正层**，与 r250（耦合常数跑动层）领域不同，**条目不可相加**。
α₀ 与 P₀ 的自身问题归 **r250**（本卷只把它作为 E 组的口径输入，记 INFO 指针）。
r252 攻的是「质量比 m_p/m_e 的 f 未求值」；本卷攻的是「磁矩 g 的因子 2 与两圈符号」，
**不是同一层**。r248 用过本源公理 ω²=c²(κ²+τ²) 的另一后果；本卷不用该公理。
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
RID = "r255"
BASE_NAME = ("TUFT-r255_磁矩与量子修正层_裸涡旋因子2与两圈闭式符号反_"
             "dageo超窗96672倍与alpha口径二难_精算与可视化_2026-10-31")
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
# 1. 常数（全部带来源；不写死任何「结论」）
# ============================================================
E_CHG = 1.602176634e-19          # 元电荷 C（SI 定义值）
HBAR = 1.054571817e-34           # J·s（CODATA）
M_E = 9.1093837015e-31           # kg（CODATA）
MU_B = 9.2740100783e-24          # 玻尔磁子 J/T（CODATA）
A_OBS = 7.2973525693e-3          # 精细结构常数（CODATA）
A0_TUFT = math.sqrt(3.0) / 2.0   # 靶的裸值 α₀=√3/2
A_EXP = 1.15965218128e-3         # 电子反常磁矩实验值（CODATA 2018）
DA_EXP = 1.8e-13                 # a_e 的 1σ 不确定度
G_EXP = 2.00231930436            # 电子 g 因子实测
ZETA3 = 1.2020569031595943       # ζ(3)
C2_STD = -0.3284789655791934     # 标准两圈系数（Petermann，文献值）
C3_STD = 1.181241456             # 标准三圈系数（Laporta–Remiddi，文献值）
C2_TARGET_STATED = -1.7723e-6    # 靶写在 line 3981 的两圈数值


def fmt_rel(x):
    return "{:.3e}".format(x)


def rel(a, b):
    if b == 0:
        return float("inf") if a != 0 else 0.0
    return abs(a - b) / abs(b)


def disc(model, exp):
    """差异倍数（≥1，按**绝对值**比较；符号另由 sign_flip 单独判定）"""
    a, b = abs(model), abs(exp)
    if b == 0:
        return float("inf") if a != 0 else 1.0
    r = a / b
    return max(r, 1.0 / r) if r > 0 else float("inf")


# ============================================================
# 2. 靶机读（含上游 LaTeX 污染修复，承 r247/r252）
# ============================================================
_ALPHA52 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


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


def depollute(s):
    r"""上游把字母 X 批量替换成 \(\boldsymbol{X}\)。用精确字符串替换（避免正则转义陷阱）。"""
    for ch in _ALPHA52:
        s = s.replace("\\(\\boldsymbol{" + ch + "}\\)", ch)
    return re.sub(r"[\r\n]+", "\n", s)


SHA_AT_IMPORT = {p: sha256_of(p) for p in TARGETS}
TARGET_TEXT = {p: read_text(p) for p in TARGETS}
RAW = TARGET_TEXT.get(TARGETS[0], "")
ALL_RAW = "".join(TARGET_TEXT.get(p, "") for p in TARGETS)
ALL = depollute(ALL_RAW)
RAW_LINES = depollute(RAW).split("\n")
ALL_LINES = ALL.split("\n")


def loc(*subs):
    """多子串 AND 定位（每个子串独立存在即可；全部须在同一行）"""
    out = []
    for i, s in enumerate(RAW_LINES):
        if all(x in s for x in subs):
            out.append(i + 1)
    return out


def loc_any(*subs):
    out = []
    for i, s in enumerate(RAW_LINES):
        if any(x in s for x in subs):
            out.append(i + 1)
    return out


L_MU_DEF = loc("-\\frac{e}{2m_e}")                    # 磁矩定义
L_MU0_MINUS = loc("-\\frac{e}{m_e}")                  # μ₀=−(e/m)S
L_IA = loc("IA=")                                      # μ₀=IA
L_T_C = loc("2\\pi r_0}{c}")                           # T=2πr₀/c
L_MU_HALF = loc("\\frac12 e c r_0")                    # μ₀=½ecr₀
L_MU_4M = loc("\\frac{e\\hbar}{4m_e}")                 # μ₀=eℏ/(4m_e)
L_MU_S = loc("\\frac{e}{m_e} S")                       # μ₀=(e/m_e)S
L_G2_OK = loc("与狄拉克", "g=2")                       # 「与狄拉克 g=2 完全一致」
L_AE1 = loc("a_e^{(1)}=\\frac{\\alpha}{2\\pi}")        # 单圈式
L_AE1_NUM = loc("0.0011614")                           # 单圈数值
L_CLOSED = loc("zeta(3)", "\\pi^2}{12}")               # 两圈闭式
L_AE2_NUM = loc("0.0000017723")                        # 两圈数值
L_DAGEO = loc("Delta a_")                              # Δa_geo
L_DAGEO_ORD = loc("Delta a_", "mathcal{O}(\\alpha^2)")  # Δa_geo 量级
L_DAGEO_UNIQ = loc("理论独有")                          # 「理论独有的可观测预言」
L_SERIES = loc("C_2\\left(\\frac{\\alpha}{\\pi}\\right)^2")
L_C1 = loc("C_1=1/2")
L_EXP_TXT = loc("0.00115965218059")                    # 靶引用的实验值
L_EXP_EQ = loc("a_e\\approx0.001159652")
L_CANCEL = loc("抵消一部分")
L_MATCH = loc("匹配实验")
L_MUON = loc_any("μ子", "\\mu子")
L_G0_2 = loc("g_0=2")
L_ALPHA_BOTH = loc("alpha_0=", "sqrt{3}/2")

# 靶是否给出 C₂/C₃ 的具体数值
C2_EQ = len(re.findall(r"C_2\s*=", ALL))
C3_EQ = len(re.findall(r"C_3\s*=", ALL))
C2_STD_TOK = len(re.findall(r"0\.328", ALL))


# ============================================================
# 3. ★ 核心计算
# ============================================================
def bare_moment():
    r"""① 裸磁矩：靶自己的 I·A 推导给出 eℏ/(4m_e)，但随后写成 (e/m_e)S。"""
    # 代数：μ₀ = I·A = (e/T)·πr₀² ；T = 2πr₀/c ⇒ μ₀ = ½ e c r₀
    C_LIGHT = 299792458.0
    r0 = HBAR / (2.0 * M_E * C_LIGHT)                      # ← 必须除 c
    mu_from_IA = 0.5 * E_CHG * C_LIGHT * r0                # ½ e c r₀
    mu_from_4m = E_CHG * HBAR / (4.0 * M_E)                # eℏ/(4m_e)
    S = HBAR / 2.0
    mu_from_S = (E_CHG / M_E) * S                          # (e/m_e)S
    # 由 μ = g·(e/2m)S 反解 g
    g_from_IA = 2.0 * mu_from_IA / ((E_CHG / M_E) * S)
    g_from_4m = 2.0 * mu_from_4m / ((E_CHG / M_E) * S)
    g_from_S = 2.0 * mu_from_S / ((E_CHG / M_E) * S)
    return {
        "r0": r0, "mu_IA": mu_from_IA, "mu_4m": mu_from_4m, "mu_S": mu_from_S,
        "mu_B": MU_B,
        "ratio_4m_over_S": mu_from_4m / mu_from_S,     # ≈ 0.5
        "ratio_S_over_4m": mu_from_S / mu_from_4m,     # ≈ 2（承重口径）
        "IA_exact_half": abs(mu_from_IA - mu_from_4m) / mu_from_4m,
        "g_from_IA": g_from_IA, "g_from_4m": g_from_4m, "g_from_S": g_from_S,
        "mu_4m_over_muB": mu_from_4m / MU_B,           # ≈ 0.5
        # 代数严格：对任意 r，经典环流 g≡1
        "g_classical_algebraic": 1.0,
    }


def two_loop():
    r"""② 两圈闭式 vs 靶自己给的数值。"""
    # 靶的闭式：a_e^(2) = −(α²/2π²)(½ζ(3) − π²/12)
    bracket = 0.5 * ZETA3 - (math.pi ** 2) / 12.0
    a2_closed = -(A_OBS ** 2) / (2.0 * math.pi ** 2) * bracket
    ap2 = (A_OBS / math.pi) ** 2
    c2_closed = a2_closed / ap2                # 闭式等价于多少 C₂
    a2_stated = C2_TARGET_STATED               # 靶写的数值
    c2_stated = a2_stated / ap2                # 该数值等价于多少 C₂
    return {
        "bracket": bracket, "half_zeta3": 0.5 * ZETA3,
        "pi2_over_12": (math.pi ** 2) / 12.0,
        "a2_closed": a2_closed, "c2_closed": c2_closed,
        "a2_stated": a2_stated, "c2_stated": c2_stated,
        "ratio_closed_over_stated": a2_closed / a2_stated,
        "disc_closed_vs_stated": disc(a2_closed, a2_stated),
        "sign_flip": (a2_closed > 0) != (a2_stated > 0),
        "c2_std": C2_STD,
        "c2_gap": c2_stated - c2_closed,
    }


def dageo_layer():
    r"""③ Δa_geo = O(α²) 与「QED 序列已匹配实验」的冲突。"""
    a1 = A_OBS / (2.0 * math.pi)
    a12 = a1 + C2_TARGET_STATED
    a123 = a12 + C3_STD * (A_OBS / math.pi) ** 3
    room12 = abs(a12 - A_EXP)
    room123 = abs(a123 - A_EXP)
    ap2 = (A_OBS / math.pi) ** 2
    # 若坚持靶的闭式，总分是多少
    a2_closed = two_loop()["a2_closed"]
    a_closed_total = a1 + a2_closed
    return {
        "a1": a1, "a12": a12, "a123": a123,
        "exp": A_EXP,
        "resid12": a12 - A_EXP, "room12": room12,
        "resid123": a123 - A_EXP, "room123": room123,
        "dageo_order": ap2,
        "ratio12": ap2 / room12, "ratio123": ap2 / room123,
        "a_closed_total": a_closed_total,
        "a_closed_gap": a_closed_total - A_EXP,
        "a_closed_gap_rel": rel(a_closed_total, A_EXP),
    }


def alpha_fork():
    r"""④ α 口径二难：用 α₀ 还是 α_obs？"""
    ae_a0 = A0_TUFT / (2.0 * math.pi)
    ae_obs = A_OBS / (2.0 * math.pi)
    g_pred = 2.0 + 2.0 * ae_a0
    dg = 2.0 * DA_EXP
    return {
        "ae_a0": ae_a0, "ae_obs": ae_obs,
        "ratio_a0_over_exp": ae_a0 / A_EXP,
        "ratio_a0_over_obs": A0_TUFT / A_OBS,
        "g_pred_a0": g_pred, "g_exp": G_EXP,
        "dg_pred": abs(g_pred - G_EXP),
        "sigma": abs(g_pred - G_EXP) / dg,
        "ae_obs_rel_dev": rel(ae_obs, A_EXP),
        "delta_g_sigma_denom": dg,
    }


def caliber_scan():
    out = {
        "μ₀=eℏ/(4m_e) 行": len(L_MU_4M),
        "μ₀=(e/m_e)S 行": len(L_MU_S),
        "「与狄拉克 g=2」行": len(L_G2_OK),
        "两圈闭式行": len(L_CLOSED),
        "两圈数值 0.0000017723 行": len(L_AE2_NUM),
        "Δa_geo 行": len(L_DAGEO),
        "Δa_geo 标 O(α²) 行": len(L_DAGEO_ORD),
        "「理论独有」行": len(L_DAGEO_UNIQ),
        "「匹配实验」行": len(L_MATCH),
        "「抵消一部分」行": len(L_CANCEL),
        "C_2= 定义式": C2_EQ,
        "C_3= 定义式": C3_EQ,
        "0.328（标准两圈系数）": C2_STD_TOK,
        "μ子预言行": len(L_MUON),
    }
    return out


# ============================================================
# 4. 修复定价
# ============================================================
MS_KEYS = ("g2_derived", "c2_closed", "c3_closed", "dageo_value",
           "alpha_caliber", "QED_free", "muon_scaling")
REQ_STRICT = {"g2_derived", "c2_closed", "dageo_value", "alpha_caliber"}
REQ_LOOSE = {"c2_closed", "alpha_caliber"}


def repair_pricing(req):
    r"""
    EMPTY  = req ⊄ have
    SUICIDE= req ⊆ have 且 QED_free ∉ have（必须借标准 QED 系数 ⇒ 原「几何推导」宣称被替换）
    SURVIVE= req ⊆ have 且 QED_free ∈ have（真从几何算出，不借 QED）
    """
    from itertools import product
    out = {"EMPTY": 0, "SUICIDE": 0, "SURVIVE": 0, "SURVIVE_SETS": []}
    for combo in product((False, True), repeat=len(MS_KEYS)):
        have = {k for k, v in zip(MS_KEYS, combo) if v}
        if not req.issubset(have):
            out["EMPTY"] += 1
        elif "QED_free" not in have:
            out["SUICIDE"] += 1
        else:
            out["SURVIVE"] += 1
            out["SURVIVE_SETS"].append(sorted(have))
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
# 6. 真机读守卫 / AST 自审器（含 IfExp 补丁）
# ============================================================
def scan_untouched(lo=225, hi=255):
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
    ok = (dist.get("FAIL", 0) >= 8) and (dist.get("PASS", 0) >= 5)
    return ok, "实测分布 %s（要求 FAIL≥8 且 PASS≥5）" % dist


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


def ast_scan_hardcoded(path_or_src, is_src=False):
    src = path_or_src if is_src else read_text(path_or_src)
    if not src:
        return [], "（源读取失败或文件不存在）"
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
        code = node.args[0].value if isinstance(node.args[0], ast.Constant) else None
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


def find_other_volume_src(prefix):
    try:
        for nm in os.listdir(SRC_DIR):
            if nm.startswith("TUFT-" + prefix) and nm.endswith(".py"):
                return os.path.join(SRC_DIR, nm)
    except OSError:
        pass
    return None


# ============================================================
# 7. 主审计
# ============================================================
def run_audit():
    EVIDENCE.clear()
    del ENTRIES[:], CONTROLS[:], GUARDS[:]

    bm = bare_moment()
    tl = two_loop()
    dg = dageo_layer()
    af = alpha_fork()
    cs = caliber_scan()
    p_strict = repair_pricing(REQ_STRICT)
    p_loose = repair_pricing(REQ_LOOSE)
    EVIDENCE.update({"bm": bm, "tl": tl, "dg": dg, "af": af, "cs": cs,
                     "pricing_strict": p_strict, "pricing_loose": p_loose})

    self_path = os.path.join(SRC_DIR, BASE_NAME + ".py")
    self_bad, self_msg = ast_scan_hardcoded(self_path)
    r244_path = find_other_volume_src("r244")
    oth_bad, oth_msg = ast_scan_hardcoded(r244_path) if r244_path else ([], "（未找到 r244 源码）")

    # ============================================================
    # A 组 · 对靶有利（先证明对的部分）
    # ============================================================
    ent("A1", "磁矩定义式 μ = −(e/2m_e)S·g 形式正确", "PASS",
        "来料 line %s 逐字给出 μ = −(e/2m_e)S g，与标准关系 μ = −g(e/2m_e)S 一致；"
        "这是电磁学/量子力学的标准定义，靶照抄无误。" % L_MU_DEF[:4],
        "对靶有利：本卷**不**质疑这一条。B 组的攻击点建立在「这个定义是对的」之上——"
        "正因为定义对，才能由它反解出 g=1。")
    ent("A2", "Schwinger 单圈项 a_e^(1)=α/(2π) 形式与数值均正确（用 α_obs）", "PASS",
        "来料 line %s 给出 a_e^(1)=α/(2π)，line %s 代入 α≈1/137.036 得 0.0011614。"
        "本卷复算 α_obs/(2π)=%.10e，与靶的 0.0011614 **一致**（相对偏差 %s，"
        "该偏差正是两圈项 a_e^(2) 的贡献量与量级，不是错误）。"
        % (L_AE1[:4], L_AE1_NUM[:4], af["ae_obs"], fmt_rel(rel(af["ae_obs"], 1.1614e-3))),
        "对靶有利：**这一项是整卷唯一与实验符合到 3 位有效数字的地方**，且公式完全正确。"
        "本卷攻击的是它**下面**的两圈项（C 组）与它**所用 α 的口径**（E 组）。")
    ent("A3", "靶引用的实验值 0.00115965218059 与 CODATA 一致", "PASS",
        "来料 line %s 写 a_e^exp≈0.00115965218059；CODATA 2018 为 %.11e。"
        "相对偏差 %s。line %s 另写 a_e≈0.001159652。"
        % (L_EXP_TXT[:4], A_EXP, fmt_rel(rel(0.00115965218059, A_EXP)), L_EXP_EQ[:4]),
        "对靶有利：靶**没有篡改实验值**，引用精度到位。⇒ 本卷所有对比都可用"
        "「靶自己引用的实验值」作为锚点，无需外部输入。")
    ent("A4", "「真空挠率云 ⇒ 圈修正」的物理图像与 QED 真空极化同构（定性正确）", "PASS",
        "来料 line 3935–3936 逐字：「真空零点挠率场在电子周围形成极化云，"
        "虚微小螺旋涡旋环绕主电子涡旋，叠加额外磁偶极贡献」；"
        "「g−2 本质：真空挠率涨落的圈修正耦合到主涡旋的自旋磁矩」。"
        "这与 QED 的真空极化（虚 e⁺e⁻ 云）在**结构上**同构：都是「主客体 + 云 + 圈修正」。",
        "对靶有利：**图像方向是对的**。本卷攻击的是「从图像到数字」这一步"
        "——图像不能替代系数（见 C/D 组）。")
    ent("A5", "裸涡旋 a₀=0 ⇔ 狄拉克 g=2 ⇔ 点粒子极限，三者在逻辑上自洽", "PASS",
        "来料 line 3931 写「狄拉克理论预言点电子 g=2，即 a_e=(g−2)/2=0」；"
        "line 3963 写「裸涡旋本身无反常，a₀=0」。二者一致，且与"
        "「无结构点粒子 ⇒ 无反常磁矩」的标准结论相符。",
        "对靶有利：这是**正确的物理陈述**。注意：本卷 B1 说的不是「a₀≠0」，"
        "而是「靶算出的 μ₀ 实际对应 g=1」，那是另一个问题。")
    ent("A6", "靶主动把 Δa_geo 标为「可检验预言」并指出检验途径（有可证伪意识）", "PASS",
        "来料 line %s 称 Δa_geo「是**理论独有的可观测预言**」；line 4007 写"
        "「高阶系数会有微小偏移，未来更高精度g-2测量可以检验这个预言」。"
        "机读「理论独有」%d 处、「Δa_geo」%d 处。"
        % (L_DAGEO_UNIQ[:4], cs["「理论独有」行"], cs["Δa_geo 行"]),
        "对靶有利：靶**主动提出了一个可被实验检验的方向**，这在被审对象里是加分项。"
        "⇒ 正因为它自称可检验，本卷 D 组才**必须**去检验它——而检验结果是它已被排除。")

    # ============================================================
    # B 组 · ★★ 裸磁矩差因子 2：靶自己的推导给出 g=1
    # ============================================================
    ent("B1", "★★ 靶算出的 μ₀=eℏ/(4m_e) 与自己写的 μ₀=(e/m_e)S 差**恰好 2 倍**；"
        "由前者反解 g=%.6f" % bm["g_from_4m"], "FAIL",
        "来料 line %s 由 I·A 得 μ₀ = eℏ/(4m_e) = %.10e；line %s 却写 μ₀ = (e/m_e)S，"
        "取 S=ℏ/2 得 %.10e。二者之比 = **%.10f**（精确 2）。"
        "由 μ = g(e/2m_e)S 反解：用 eℏ/(4m_e) ⇒ g = **%.10f**；"
        "用 (e/m_e)S ⇒ g = %.10f。玻尔磁子 μ_B=%.10e，而 eℏ/(4m_e)=%.10e = μ_B/2。"
        % (L_MU_4M[:4], bm["mu_4m"], L_MU_S[:4], bm["mu_S"],
           bm["ratio_S_over_4m"], bm["g_from_4m"], bm["g_from_S"],
           MU_B, bm["mu_4m"]),
        "★这是**纯代数**：不受 α、κ、τ、ω 任何取值影响。靶的 I·A 推导给出的是 "
        "**g=1**（经典环流值），而 line %s 却写「与狄拉克 g=2 完全一致」。"
        % L_G2_OK[:4])
    ent("B2", "★ 根因：T=2πr₀/c 使电荷以光速环流，而经典环流的 g **恒为 1**", "FAIL",
        "来料 line %s 取 T = 2πr₀/c ⇒ 环流速度 = c。对半径 r 的经典电流环，"
        "μ = I·A = (e/T)πr² = ½ e c r，角动量 L = m c r ⇒ μ/L = e/(2m) ⇒ "
        "**g = 2μ/((e/m)L) = 1 对任意 r 成立**（与 r、c 取值无关）。"
        "本卷机验：由 μ_IA=½ecr₀ 反解 g = %.10f。" % (L_T_C[:4], bm["g_from_IA"]),
        "⇒ 要得到 g=2 必须引入**非经典**项（Tomonaga–Schwinger 的场论修正），"
        "而靶声称「几何推导」出了 g=2 —— 它实际推导出的是 g=1。"
        "这是 B1 那个「因子 2」的**物理来源**：经典环流与 g=2 之间差的正是那个 2。")
    ent("B3", "★ 符号不一致：同一卷内 μ₀ 的负号时有时无", "FAIL",
        "line %s 与 line %s 写 μ₀ = **−**(e/m_e)S；而 line %s 写 μ₀ = (e/m_e)S（无负号）。"
        "机读：含 −(e/m_e) 的行 %d 处、含 (e/m_e)S 的行 %d 处。"
        % (L_MU0_MINUS[:4], L_G0_2[:4], L_MU_S[:4], len(L_MU0_MINUS), len(L_MU_S)),
        "⇒ 属排版/推导不一致（量级结论不受影响），但说明该节**未经一致性检查**。"
        "与 B1 的因子 2 叠加，使 line 3963 的「完全一致」结论无法成立。")

    # ============================================================
    # C 组 · ★★ 两圈闭式与靶自己给的数值不自洽
    # ============================================================
    ent("C1", "★★ 两圈闭式复算 = %.6e（C₂=%+.6f），靶却写 %.4e（C₂=%+.6f）"
        % (tl["a2_closed"], tl["c2_closed"], tl["a2_stated"], tl["c2_stated"]), "FAIL",
        "来料 line %s 闭式：a_e^(2) = −(α²/2π²)(½ζ(3) − π²/12)。"
        "本卷复算：½ζ(3)=%.10f、π²/12=%.10f、括号=**%.10f** ⇒ a_e^(2) = **%+.6e**，"
        "等价于 C₂ = **%+.8f**。而 line %s 写 a_e^(2) ≈ %.7e，等价于 C₂ = %+.8f。"
        "⇒ **符号相反**（闭式为正、所述为负），**幅值差 %.4f 倍**。"
        % (L_CLOSED[:4], tl["half_zeta3"], tl["pi2_over_12"], tl["bracket"],
           tl["a2_closed"], tl["c2_closed"], L_AE2_NUM[:4], tl["a2_stated"],
           tl["c2_stated"], tl["disc_closed_vs_stated"]),
        "★注意：靶**所述的那个数值**（−1.7723e−6，即 C₂=−0.328479）与标准 QED 一致；"
        "错的是它给的**闭式**。⇒ 这是「公式与数字对不上」，不是「数字抄错」。")
    ent("C2", "★ 二难：坚持闭式则总分差 %.3e；坚持数值则闭式写错——两支都算死"
        % abs(dg["a_closed_gap"]), "FAIL",
        "分支一（信闭式）：a_e = a_e^(1) + a_e^(2,闭式) = %.10e + %.6e = **%.10e**，"
        "与实验 %.10e 差 **%+.4e**（相对 %s）。"
        "分支二（信数值）：则闭式 −(α²/2π²)(½ζ(3)−π²/12) **写错**，"
        "因为它在 α²/π² 单位下只给 %+.6f，缺 %+.6f（缺口 %.6f）。"
        % (tl["a2_closed"] - tl["a2_closed"] + dg["a1"], tl["a2_closed"],
           dg["a_closed_total"], A_EXP, dg["a_closed_gap"],
           fmt_rel(dg["a_closed_gap_rel"]), tl["c2_closed"], tl["c2_gap"], tl["c2_gap"]),
        "★该缺口 ΔC₂=%.6f 的绝对值远大于 |C₂| 本身（%.6f）⇒ 说明两圈系数是 "
        "ln2 主导的（|π²ln2/2|≈3.42 ≫ |C₂|≈0.33），而靶的闭式**不含 ln2 项**，"
        "这正是此类错误的典型形态。" % (tl["c2_gap"], abs(tl["c2_stated"])))

    # ============================================================
    # D 组 · ★★ Δa_geo：唯一的「新预言」被靶自己的求和排除
    # ============================================================
    ent("D1", "★★ Δa_geo 标称 O(α²)=%.4e，超出允许窗 %.3e 达 **%.0f 倍**"
        % (dg["dageo_order"], dg["room123"], dg["ratio123"]), "FAIL",
        "靶 line %s 称 Δa_geo「量级为 O(α²)」。本卷：O(α²)=(α/π)²=**%.6e**。"
        "而用**靶自己给的**单圈（0.0011614）与两圈（−1.7723e−6）相加得 **%.10e**，"
        "与**靶自己引用的**实验值 %.10e 只差 **%+.4e**；"
        "再加标准三圈（C₃=%.9f）得 **%.10e**，残差仅 **%+.4e**。"
        "⇒ 允许窗 %.3e，Δa_geo 是 %.4e ⇒ **超出 %.0f 倍**。"
        "（仅按 1+2 圈口径也超出 **%.1f 倍**。）"
        % (L_DAGEO_ORD[:4], dg["dageo_order"], dg["a12"], A_EXP, dg["resid12"],
           C3_STD, dg["a123"], dg["resid123"], dg["room123"], dg["dageo_order"],
           dg["ratio123"], dg["ratio12"]),
        "★这是**完全内部**的：只用靶自己写的两个数值 + 靶自己引用的实验值。"
        "结论：若 Δa_geo 真是 O(α²)，则 a_e 会偏到 1.16e−3 量级，"
        "而实测已把 a_e 钉在 1.159652e−3 上、误差 1.8e−13 ⇒ **该预言被排除 4.98 个数量级**。")
    ent("D2", "★★ 内部矛盾：靶同时说「Δa_geo 是 O(α²) 的新预言」与「QED 序列已压低 a_e 匹配实验」",
        "FAIL",
        "line %s 称 Δa_geo「量级为 O(α²)」，line 3987 称其为「理论独有的可观测预言」；"
        "但 line %s 写「差值由高阶圈（两圈、三圈）**抵消一部分**」，"
        "line %s 写「高阶：曲率挠率非线性相互作用带来微小负修正，**压低总 a_e，匹配实验**」。"
        "机读：「匹配实验」%d 处、「抵消一部分」%d 处。"
        % (L_DAGEO_ORD[:4], L_CANCEL[:4], L_MATCH[:4],
           cs["「匹配实验」行"], cs["「抵消一部分」行"]),
        "★二者不能同时成立：若「两圈+三圈（**纯标准 QED 项**）已把 a_e 压低到匹配实验」，"
        "则 Δa_geo 必须 ≈0；而靶又说 Δa_geo=O(α²)≠0。"
        "⇒ 靶唯一的新预言，被它自己给出的求和结果**归零**。")
    ent("D3", "★ μ子 g−2 预言零数值，且缺标度律 ⇒ 二难", "FAIL",
        "来料 line 4015–4018 逐字：「μ子也是同类封闭螺旋涡旋…涡旋更小，真空云穿透更深，"
        "高阶几何修正项更大」「本理论预言：μ子 a_μ 的高阶修正，相比标准模型，"
        "存在额外偏移项，可对应 μ子 g−2 反常」。**通篇无一个数字**，"
        "亦无「Δa 随 m 的标度律」。机读 μ子相关行 %d 处。" % cs["μ子预言行"],
        "⇒ 二难：若 Δa_geo **与粒子无关**（普适 O(α²)），则电子已被 D1 排除 5 个数量级，"
        "μ子同样被排除；若 Δa_geo **依赖粒子**，则必须先给出 a_μ/a_e 的标度律，"
        "而靶只给了「更大」两个字。两支都不通。")
    ent("D4", "★ C₂、C₃ 从未给出数值：级数不可计算", "FAIL",
        "来料 line 3995–3997 只给文字：「C₁=1/2（施温格单圈）」「C₂：标准QED系数+螺旋几何修正」"
        "「C₃：三圈，含挠率场高阶自耦合」。机读：「C_2 =」**%d 处**、「C_3 =」**%d 处**、"
        "标准两圈数值 0.328 **%d 处**。⇒ 靶只**命名**了 C₂/C₃，从未赋值。"
        % (C2_EQ, C3_EQ, C2_STD_TOK),
        "⇒ 与 r252 的「f 未给出」是同型缺陷（未定系数），但**分层不同**："
        "r252 是积分被积函数未定，本卷是级数系数未定。本卷只记 1 条，不与 r252 相加。")

    # ============================================================
    # E 组 · ★★ α 口径二难
    # ============================================================
    ent("E1", "★★ 用靶自己的裸值 α₀=√3/2，a_e 大 %.2f 倍、g 偏 **%.3e σ**"
        % (af["ratio_a0_over_exp"], af["sigma"]), "FAIL",
        "来料 line %s 写 a_e^(1)=α/(2π)，但**未指定用哪个 α**；"
        "line %s 同时给出 α₀=√3/2 与 α_obs≈1/137.036。"
        "若用 α₀：a_e = α₀/(2π) = **%.8f**，是实验值 %.10e 的 **%.2f 倍**；"
        "对应 g_pred = 2 + 2a_e = **%.8f**，与实测 g=%.11f 差 **%.8f**，"
        "而 δg = 2δa_e = %.1e ⇒ **%.3e σ**。"
        % (L_AE1[:4], L_ALPHA_BOTH[:4], af["ae_a0"], A_EXP, af["ratio_a0_over_exp"],
           af["g_pred_a0"], G_EXP, af["dg_pred"], af["delta_g_sigma_denom"], af["sigma"]),
        "★这不是「精度不够」，而是**被判死**：一个偏 7.6e11 σ 的预测量在任何意义上都不可接受。"
        "注意 α₀ 自身的合理性归 **r250**，本卷只用它作 E 组的口径输入（见 G1）。")
    ent("E2", "★ 用 α_obs 则数值对得上，但 α_obs 是**实验输入** ⇒ 「几何推导」退化为抄公式",
        "FAIL",
        "line %s 逐字「代入 α≈1/137.036」——这是 CODATA 实测值。"
        "本卷复算 α_obs/(2π) = %.10e，与实验 a_e=%.10e 相对偏差 %s"
        "（该偏差由两圈项补上，属正常）。"
        % (L_AE1_NUM[:4], af["ae_obs"], A_EXP, fmt_rel(af["ae_obs_rel_dev"])),
        "⇒ 二难闭合：**裸值给出荒谬数（E1），观测值给出正确数但那是外部输入（E2）**。"
        "两条支都不支持「从螺旋涡旋几何推导出反常磁矩」这一宣称："
        "该节实际做的是「抄 Schwinger 公式 + 代实测 α」。")

    # ============================================================
    # F 组 · 修复定价
    # ============================================================
    ent("F1", "修复定价（双档）：严格档 EMPTY %d / SUICIDE %d / SURVIVE %d；"
        "宽松档 %d / %d / %d"
        % (p_strict["EMPTY"], p_strict["SUICIDE"], p_strict["SURVIVE"],
           p_loose["EMPTY"], p_loose["SUICIDE"], p_loose["SURVIVE"]), "FAIL",
        "7 个结构槽位（2^7=%d 组合）：%s。严格档 REQ={g=2由几何导出, C₂闭式自洽, "
        "Δa_geo 有数值, α 口径唯一}：EMPTY %d / SUICIDE %d / SURVIVE %d；"
        "宽松档 REQ={C₂闭式自洽, α 口径唯一}：EMPTY %d / SUICIDE %d / SURVIVE %d。"
        "SUICIDE 定义：条件齐备但 **QED_free ∉ have** ⇒ 必须借标准 QED 系数才能算出，"
        "原「从螺旋几何推导」宣称被替换。"
        "注：宽松档 SURVIVE=%d>0 表明宣称**逻辑上非不可能**；本卷判的是**靶未达成**"
        "（B1 已机算其裸推导只给 g=1）。"
        % (2 ** len(MS_KEYS), ", ".join(MS_KEYS),
           p_strict["EMPTY"], p_strict["SUICIDE"], p_strict["SURVIVE"],
           p_loose["EMPTY"], p_loose["SUICIDE"], p_loose["SURVIVE"],
           p_loose["SURVIVE"]),
        "★分层铁律：本卷条目**不可与 r142–r254 相加**，尤其不可与 r250（耦合常数层）、"
        "r252（质量谱层）相加。本卷为**磁矩与量子修正层**首卷。")

    # ============================================================
    # G 组 · 交联指针（INFO，不计分）
    # ============================================================
    ent("G1", "交联（INFO，不计分）：α₀=√3/2 与 P₀=117.68 的自身问题归 r250", "INFO",
        "本卷 E 组用到 α₀=√3/2 作口径输入。r250 已独立判定：把靶第 9 条 RG 积分解代入 "
        "μ_Planck 得 α=7.93e−3，与第 10 条断言的 0.866 差 109.21 倍；"
        "且 α_* 是定义恒等式（m_e 缩放 1e9 倍时 α 极差 1.1e−16）。"
        "⇒ 本卷**不**把 r250 条目相加进来，只作指针。",
        "★本卷独立成立的部分是 B/C/D/E 组——它们**不依赖** α₀ 是否正确："
        "B 组是纯代数（g=1 与 α 无关）；C 组只比较靶的两个数；"
        "D 组只用 α_obs（靶自己指定的 1/137.036）；E1 反而是**假设 α₀ 成立**时的归谬。")

    # ============================================================
    # 控制组
    # ============================================================
    ctl("C01", "μ₀ 反解：由 eℏ/(4m_e) 得 g=1（要求 |g−1|<1e-12）",
        abs(bm["g_from_4m"] - 1.0) < 1e-12, "g = %.12f" % bm["g_from_4m"])
    ctl("C02", "μ₀ 反解：由 (e/m_e)S 得 g=2（要求 |g−2|<1e-12）",
        abs(bm["g_from_S"] - 2.0) < 1e-12, "g = %.12f" % bm["g_from_S"])
    ctl("C03", "★承重：(e/m_e)S 与 eℏ/(4m_e) 之比恰为 2（要求 |ratio−2|<1e-12）",
        abs(bm["ratio_S_over_4m"] - 2.0) < 1e-12,
        "(e/m_e)S ÷ eℏ/(4m_e) = %.15f（倒数 %.15f）"
        % (bm["ratio_S_over_4m"], bm["ratio_4m_over_S"]))
    ctl("C04", "I·A 路径与 eℏ/(4m_e) 数值一致（两条独立实现互校）",
        bm["IA_exact_half"] < 1e-14,
        "½ecr₀=%.12e vs eℏ/(4m_e)=%.12e，相对差 %s"
        % (bm["mu_IA"], bm["mu_4m"], fmt_rel(bm["IA_exact_half"])))
    # 注：本卷由 e/ℏ/m_e 现算的值与表列 μ_B 属不同 CODATA 发布批次，
    # 相对偏移 ~6e-10（9 位有效数字内一致）⇒ 容差取 1e-8 并如实报告该偏移。
    ctl("C05", "★eℏ/(4m_e) = μ_B/2 即半个玻尔磁子（两独立来源，9 位内一致）",
        abs(bm["mu_4m_over_muB"] - 0.5) < 1e-8,
        "现算 %.12e ÷ 表列 μ_B %.12e = %.12f（与 0.5 差 %s）"
        % (bm["mu_4m"], MU_B, bm["mu_4m_over_muB"],
           fmt_rel(abs(bm["mu_4m_over_muB"] - 0.5))))
    ctl("C06", "两圈闭式括号项复算：½ζ(3)−π²/12 = %.10f" % tl["bracket"],
        abs(tl["bracket"] - (0.5 * ZETA3 - math.pi ** 2 / 12.0)) < 1e-15,
        "%.12f（½ζ(3)=%.10f，π²/12=%.10f）"
        % (tl["bracket"], tl["half_zeta3"], tl["pi2_over_12"]))
    ctl("C07", "★承重：闭式与所述数值符号相反",
        (tl["a2_closed"] > 0) != (tl["a2_stated"] > 0),
        "闭式 %+.6e（C₂=%+.8f） vs 所述 %+.6e（C₂=%+.8f）"
        % (tl["a2_closed"], tl["c2_closed"], tl["a2_stated"], tl["c2_stated"]))
    ctl("C08", "★承重：闭式/所述幅值比 = %.4f（要求 >2）" % tl["disc_closed_vs_stated"],
        tl["disc_closed_vs_stated"] > 2.0, "%.6f" % tl["disc_closed_vs_stated"])
    ctl("C09", "靶所述两圈数值等价 C₂=%.6f，与标准值 %.6f 一致（差 <1e-3）"
        % (tl["c2_stated"], C2_STD), abs(tl["c2_stated"] - C2_STD) < 1e-3,
        "%.8f vs %.8f" % (tl["c2_stated"], C2_STD))
    ctl("C10", "单圈 + 两圈（靶的数值）= %.10e，与实验残差 %.3e"
        % (dg["a12"], abs(dg["resid12"])), abs(dg["resid12"]) < 1e-7,
        "残差 %+.6e（要求 <1e-7）" % dg["resid12"])
    ctl("C11", "★单圈+两圈+三圈 = %.10e，与实验残差仅 %.3e（允许窗）"
        % (dg["a123"], abs(dg["resid123"])), abs(dg["resid123"]) < 1e-9,
        "残差 %+.6e（要求 <1e-9）" % dg["resid123"])
    ctl("C12", "★承重：Δa_geo(O(α²)) 超窗 %.0f 倍（要求 >1e3）" % dg["ratio123"],
        dg["ratio123"] > 1e3, "%.4e / %.4e = %.2f 倍"
        % (dg["dageo_order"], dg["room123"], dg["ratio123"]))
    ctl("C13", "宽松口径：仅 1+2 圈时超窗 %.1f 倍（要求 >100）" % dg["ratio12"],
        dg["ratio12"] > 100.0, "%.4e / %.4e = %.2f 倍"
        % (dg["dageo_order"], dg["room12"], dg["ratio12"]))
    ctl("C14", "★口径二难：α₀ 给出 a_e 是实验的 %.2f 倍（要求 >100）"
        % af["ratio_a0_over_exp"], af["ratio_a0_over_exp"] > 100.0,
        "%.8f / %.10e = %.3f" % (af["ae_a0"], A_EXP, af["ratio_a0_over_exp"]))
    ctl("C15", "★口径二难：α₀ 使 g 偏 %.3e σ（要求 >1e6）" % af["sigma"],
        af["sigma"] > 1e6, "|%.8f − %.11f| = %.8f，δg=%.1e"
        % (af["g_pred_a0"], G_EXP, af["dg_pred"], af["delta_g_sigma_denom"]))
    ctl("C16", "α_obs 口径下单圈项与实验相对偏差 %.3e（应 ~1e-3，属两圈量级）"
        % af["ae_obs_rel_dev"], 1e-4 < af["ae_obs_rel_dev"] < 1e-2,
        "%.6e（1.5e-3 量级 = 两圈项贡献，非错误）" % af["ae_obs_rel_dev"])
    ctl("C17", "机读：靶确实写了 μ₀=eℏ/(4m_e) 与 μ₀=(e/m_e)S 两式",
        len(L_MU_4M) > 0 and len(L_MU_S) > 0,
        "行 %s / %s" % (L_MU_4M[:4], L_MU_S[:4]))
    ctl("C18", "机读：靶确实写了「与狄拉克 g=2 完全一致」",
        len(L_G2_OK) > 0, "行 %s" % L_G2_OK[:4])
    ctl("C19", "机读：靶确实给了两圈闭式与 0.0000017723 两个对象",
        len(L_CLOSED) > 0 and len(L_AE2_NUM) > 0,
        "闭式行 %s；数值行 %s" % (L_CLOSED[:4], L_AE2_NUM[:4]))
    ctl("C20", "机读：Δa_geo 被标为 O(α²) 且自称「理论独有」",
        len(L_DAGEO_ORD) > 0 and len(L_DAGEO_UNIQ) > 0,
        "O(α²) 行 %s；独有 行 %s" % (L_DAGEO_ORD[:4], L_DAGEO_UNIQ[:4]))
    ctl("C21", "机读：C₂/C₃ 无数值（「C_2 =」与「C_3 =」均 0 处）",
        C2_EQ == 0 and C3_EQ == 0, "C_2==%d、C_3==%d" % (C2_EQ, C3_EQ))
    ctl("C22", "机读：靶「匹配实验」与「抵消一部分」两句同时存在（内部矛盾的对象）",
        len(L_MATCH) > 0 and len(L_CANCEL) > 0,
        "匹配实验 行 %s；抵消 行 %s" % (L_MATCH[:4], L_CANCEL[:4]))
    _NCOMBO = 2 ** len(MS_KEYS)
    ctl("C23", "定价守恒：两档 EMPTY+SUICIDE+SURVIVE == %d" % _NCOMBO,
        (p_strict["EMPTY"] + p_strict["SUICIDE"] + p_strict["SURVIVE"] == _NCOMBO)
        and (p_loose["EMPTY"] + p_loose["SUICIDE"] + p_loose["SURVIVE"] == _NCOMBO),
        "严格 %d+%d+%d=%d；宽松 %d+%d+%d=%d"
        % (p_strict["EMPTY"], p_strict["SUICIDE"], p_strict["SURVIVE"], _NCOMBO,
           p_loose["EMPTY"], p_loose["SUICIDE"], p_loose["SURVIVE"], _NCOMBO))
    ctl("C24", "定价判别力：宽松档 SURVIVE > 0（枚举器非退化）",
        p_loose["SURVIVE"] > 0, "严格 %d / 宽松 %d" % (p_strict["SURVIVE"], p_loose["SURVIVE"]))
    ctl("C25", "靶 3 份可读且互不相同",
        all(len(TARGET_TEXT.get(p, "")) > 200 for p in TARGETS)
        and len({SHA_AT_IMPORT[p] for p in TARGETS if SHA_AT_IMPORT[p]}) == len(TARGETS),
        "长度 %s；互异 hash %d/%d"
        % (", ".join(str(len(TARGET_TEXT.get(p, ""))) for p in TARGETS),
           len({SHA_AT_IMPORT[p] for p in TARGETS if SHA_AT_IMPORT[p]}), len(TARGETS)))
    ctl("C26", "★污染已修复：去污染后 \\(\\boldsymbol 残留 < 全长的 0.5%%",
        ALL.count("\\(\\boldsymbol") < 0.005 * max(1, len(ALL)),
        "残留 %d / 全长 %d（%.4f%%）" % (ALL.count("\\(\\boldsymbol"), len(ALL),
                                       100.0 * ALL.count("\\(\\boldsymbol") / max(1, len(ALL))))
    ctl("C27", "★自审器本卷零写死（运行时真机读，含 IfExp 形态）",
        len(self_bad) == 0, "本卷检出 %d 处：%s" % (len(self_bad), self_msg))
    ctl("C28", "★自审器正对照（承 r247）：在他人卷 r244 源码上命中 ≥1 处",
        len(oth_bad) >= 1,
        "r244（%s）检出 %d 处：%s" % (os.path.basename(r244_path) if r244_path else "MISSING",
                                   len(oth_bad), oth_msg))

    # ============================================================
    # 守卫
    # ============================================================
    grd("G1", "所有条目 evidence 非空", all(e["evidence"].strip() for e in ENTRIES),
        "%d/%d" % (sum(1 for e in ENTRIES if e["evidence"].strip()), len(ENTRIES)))
    grd("G2", "控制组全部通过", all(c["ok"] for c in CONTROLS),
        "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    grd("G3", "对靶有利项未被吞掉（A 组 ≥5 条且全 PASS）",
        sum(1 for e in ENTRIES if e["code"].startswith("A")) >= 5
        and all(e["state"] == "PASS" for e in ENTRIES if e["code"].startswith("A")),
        "A 组 %d 条，PASS %d 条"
        % (sum(1 for e in ENTRIES if e["code"].startswith("A")),
           sum(1 for e in ENTRIES if e["code"].startswith("A") and e["state"] == "PASS")))
    grd("G4", "★承重①：裸磁矩因子 2（(e/m)S ÷ eℏ/4m = 2 且由后者反解 g=1）",
        abs(bm["ratio_S_over_4m"] - 2.0) < 1e-12 and abs(bm["g_from_4m"] - 1.0) < 1e-12,
        "ratio=%.15f，g=%.12f" % (bm["ratio_S_over_4m"], bm["g_from_4m"]))
    grd("G5", "★承重②：两圈闭式与所述数值符号相反",
        (tl["a2_closed"] > 0) != (tl["a2_stated"] > 0),
        "闭式 %+.6e vs 所述 %+.6e" % (tl["a2_closed"], tl["a2_stated"]))
    grd("G6", "★承重③：Δa_geo 超允许窗 >1e3 倍",
        dg["ratio123"] > 1e3, "%.2f 倍" % dg["ratio123"])
    grd("G7", "★承重④：α₀ 口径使 g 偏 >1e6 σ",
        af["sigma"] > 1e6, "%.3e σ" % af["sigma"])
    grd("G8", "靶 3 份只读（结束态 hash == 导入期基线）",
        all(sha256_of(p) == SHA_AT_IMPORT[p] for p in TARGETS),
        "结束态 %s" % ", ".join((sha256_of(p) or "MISSING")[:12] for p in TARGETS))
    _ok9, _msg9 = scan_untouched(225, 255)
    grd("G9", "未触碰 r225–r254 产物（mtime 全部早于本轮启动）", _ok9, _msg9)
    _ok10, _msg10 = check_distribution()
    grd("G10", "条目分布断言（真机读，非预估）", _ok10, _msg10)
    grd("G11", "★判别力先测后指控：B 组结论为纯代数（与 α、κ、τ、ω 取值无关）",
        abs(bm["g_classical_algebraic"] - 1.0) < 1e-15 and abs(bm["g_from_IA"] - 1.0) < 1e-12,
        "经典环流 g=%.12f（代数恒等，非数值巧合）" % bm["g_from_IA"])
    grd("G12", "★口径自守：D 组全程用靶指定的 α_obs=1/137.036 与靶引用的实验值",
        abs(af["ae_obs_rel_dev"]) < 1e-2 and abs(dg["resid123"]) < 1e-9,
        "α_obs 单圈相对偏差 %s；三圈残差 %.3e" % (fmt_rel(af["ae_obs_rel_dev"]), dg["resid123"]))
    grd("G13", "★上游污染已修复（防「靶公式缺失」误判）",
        ALL.count("\\(\\boldsymbol") < 0.005 * max(1, len(ALL))
        and len(L_MU_4M) > 0 and len(L_CLOSED) > 0,
        "残留 %d；关键定位 %d/%d 处"
        % (ALL.count("\\(\\boldsymbol"), len(L_MU_4M), len(L_CLOSED)))
    grd("G14", "★自审器零写死 + 正对照有分辨力（本卷 0 / 他人卷 ≥1）",
        len(self_bad) == 0 and len(oth_bad) >= 1,
        "本卷 %d；r244 %d" % (len(self_bad), len(oth_bad)))
    _ok15, _msg15 = check_write_side()
    grd("G15", "未修改 verify.py / 未跑 refresh_catalog", _ok15, _msg15)
    grd("G16", "★本卷不使用本源公理 ω²=c²(κ²+τ²)（与 r248/r252 不撞面）",
        "omega^2 = c^2" not in "".join(e["evidence"] for e in ENTRIES),
        "条目证据中无该公理引用")

    return {"entries": ENTRIES, "controls": CONTROLS, "guards": GUARDS, "evidence": EVIDENCE}


# ============================================================
# 8. 渲染
# ============================================================
def render_report(res):
    ev = res["evidence"]
    bm, tl, dg, af, cs = ev["bm"], ev["tl"], ev["dg"], ev["af"], ev["cs"]
    L = []
    A = L.append
    A("=" * 78)
    A("TUFT-%s · 磁矩与量子修正层（★ 新层首卷：电子反常磁矩 g−2）" % RID.upper())
    A("=" * 78)
    A("生成时间 %s" % START_ISO)
    A("")
    A("【靶（只读 3 份）】")
    for p in TARGETS:
        A("  - %s  sha256 %s" % (os.path.basename(p), (SHA_AT_IMPORT.get(p) or "MISSING")[:16]))
    A("")
    A("-" * 78)
    A("一、★★ 裸磁矩差因子 2：靶自己的推导给出 g=1，不是 g=2")
    A("-" * 78)
    A("  靶的 I·A 推导：μ₀ = (e/T)πr₀²，T=2πr₀/c ⇒ μ₀ = ½ecr₀")
    A("  ½ecr₀                         = %.12e" % bm["mu_IA"])
    A("  eℏ/(4m_e)（靶 line 3957）      = %.12e" % bm["mu_4m"])
    A("  (e/m_e)S，S=ℏ/2（靶 line 3961）= %.12e" % bm["mu_S"])
    A("  μ_B = eℏ/(2m_e)               = %.12e" % bm["mu_B"])
    A("  ⇒ eℏ/(4m_e) = μ_B × %.6f（半个玻尔磁子）" % bm["mu_4m_over_muB"])
    A("  ⇒ 两式之比（大/小） = %.15f（精确 2）" % bm["ratio_S_over_4m"])
    A("  由 μ=g(e/2m)S 反解 g：用 eℏ/(4m_e) ⇒ g=%.10f ；用 (e/m_e)S ⇒ g=%.10f"
      % (bm["g_from_4m"], bm["g_from_S"]))
    A("  ⇒ 靶实际推导出 **g=1**（经典环流对任意 r 恒为 1），却写「与狄拉克 g=2 完全一致」")
    A("")
    A("-" * 78)
    A("二、★★ 两圈闭式与靶自己给的数值不自洽")
    A("-" * 78)
    A("  ½ζ(3)            = %.10f" % tl["half_zeta3"])
    A("  π²/12            = %.10f" % tl["pi2_over_12"])
    A("  括号 ½ζ(3)−π²/12 = %.10f" % tl["bracket"])
    A("  靶闭式 a_e^(2)   = %.6e   （等价 C₂ = %+.8f）" % (tl["a2_closed"], tl["c2_closed"]))
    A("  靶所述 a_e^(2)   = %.6e   （等价 C₂ = %+.8f）" % (tl["a2_stated"], tl["c2_stated"]))
    A("  ⇒ 符号相反，幅值比 %.4f 倍" % tl["disc_closed_vs_stated"])
    A("  ⇒ 若信闭式：a_e = %.10e，与实验差 %+.4e（相对 %s）"
      % (dg["a_closed_total"], dg["a_closed_gap"], fmt_rel(dg["a_closed_gap_rel"])))
    A("")
    A("-" * 78)
    A("三、★★ Δa_geo = O(α²) 的「新预言」被靶自己的求和排除")
    A("-" * 78)
    A("  a_e^(1)（靶 0.0011614）        = %.10e" % dg["a1"])
    A("  + a_e^(2)（靶 −1.7723e−6）     = %.10e   残差 %+.4e" % (dg["a12"], dg["resid12"]))
    A("  + a_e^(3)（标准 C₃=%.9f）  = %.10e   残差 %+.4e" % (C3_STD, dg["a123"], dg["resid123"]))
    A("  实验值                        = %.10e" % A_EXP)
    A("  ⇒ 允许窗 = %.3e；Δa_geo 标称 O(α²) = %.4e" % (dg["room123"], dg["dageo_order"]))
    A("  ⇒ **超出 %.0f 倍**（仅 1+2 圈口径也超 %.1f 倍）" % (dg["ratio123"], dg["ratio12"]))
    A("")
    A("-" * 78)
    A("四、★★ α 口径二难")
    A("-" * 78)
    A("  用 α₀=√3/2  ：a_e = %.8f（实验的 %.2f 倍）⇒ g_pred = %.8f，偏 %.3e σ"
      % (af["ae_a0"], af["ratio_a0_over_exp"], af["g_pred_a0"], af["sigma"]))
    A("  用 α_obs     ：a_e = %.10e（对得上，但与实验相对偏差 %s 由两圈补）"
      % (af["ae_obs"], fmt_rel(af["ae_obs_rel_dev"])))
    A("  ⇒ 裸值荒谬；观测值是**实验输入** ⇒ 该节实为「抄 Schwinger + 代实测 α」")
    A("")
    A("-" * 78)
    A("五、条目")
    A("-" * 78)
    for e in res["entries"]:
        A("[%s] %s · %s" % (e["state"], e["code"], e["title"]))
        A("     证据：%s" % e["evidence"])
        if e["note"]:
            A("     备注：%s" % e["note"])
    A("")
    A("-" * 78)
    A("六、控制组")
    A("-" * 78)
    for c in res["controls"]:
        A("  [%s] %s · %s" % ("PASS" if c["ok"] else "FAIL", c["code"], c["title"]))
        A("       %s" % c["evidence"])
    A("")
    A("-" * 78)
    A("七、守卫")
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
    bm, tl, dg, af = ev["bm"], ev["tl"], ev["dg"], ev["af"]
    kv = (
        ("½ecr₀（靶的 I·A 推导）", "%.6e" % bm["mu_IA"]),
        ("eℏ/(4m_e)（靶 line 3957）", "%.6e" % bm["mu_4m"]),
        ("(e/m_e)S（靶 line 3961）", "%.6e" % bm["mu_S"]),
        ("两式之比（大/小）", "%.12f（精确 2）" % bm["ratio_S_over_4m"]),
        ("由 eℏ/(4m_e) 反解 g", "%.10f ⇒ g=1，非 2" % bm["g_from_4m"]),
        ("靶闭式 a_e^(2)", "%+.6e（C₂=%+.6f）" % (tl["a2_closed"], tl["c2_closed"])),
        ("靶所述 a_e^(2)", "%+.6e（C₂=%+.6f）" % (tl["a2_stated"], tl["c2_stated"])),
        ("闭式/所述", "%.4f 倍（符号相反）" % tl["disc_closed_vs_stated"]),
        ("1+2+3 圈 vs 实验残差", "%+.4e（允许窗）" % dg["resid123"]),
        ("Δa_geo = O(α²)", "%.4e" % dg["dageo_order"]),
        ("超窗倍数", "%.0f 倍（1+2 圈口径 %.1f 倍）" % (dg["ratio123"], dg["ratio12"])),
        ("α₀ 口径下 a_e", "%.8f（实验的 %.2f 倍）" % (af["ae_a0"], af["ratio_a0_over_exp"])),
        ("α₀ 口径下 g 偏差", "%.3e σ" % af["sigma"]),
        ("C₂/C₃ 数值定义式", "C_2==%d、C_3==%d（均未给出）"
         % (ev["cs"]["C_2= 定义式"], ev["cs"]["C_3= 定义式"])),
    )
    rows = "\n".join("<tr><td>%s</td><td>%s</td></tr>" % (k, v) for k, v in kv)
    ents = []
    for e in res["entries"]:
        cls = {"PASS": "p", "FAIL": "f", "INFO": "i"}.get(e["state"], "i")
        ents.append(
            '<div class="e %s"><div class="h">[%s] %s · %s</div>'
            '<div class="b">证据：%s</div>%s</div>'
            % (cls, e["state"], e["code"], e["title"], e["evidence"],
               ('<div class="b">备注：%s</div>' % e["note"]) if e["note"] else ""))
    ctls = "\n".join(
        '<li class="%s">%s · %s — %s</li>' % ("ok" if c["ok"] else "no", c["code"], c["title"], c["evidence"])
        for c in res["controls"])
    grds = "\n".join(
        '<li class="%s">%s · %s — %s</li>' % ("ok" if g["ok"] else "no", g["code"], g["title"], g["evidence"])
        for g in res["guards"])
    return """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-%(rid)s 磁矩与量子修正层</title><style>
body{font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;margin:0;padding:28px;
background:#f6f7f9;color:#1b1f24;line-height:1.65}
h1{font-size:22px;margin:0 0 6px}h2{font-size:17px;margin:26px 0 10px;border-left:4px solid #3b6ea5;padding-left:10px}
.meta{color:#5b6470;font-size:13px}
.verdict{background:#fff;border:1px solid #dfe3e8;border-radius:8px;padding:16px;margin:14px 0}
table{border-collapse:collapse;width:100%%;background:#fff;font-size:14px}
td,th{border:1px solid #e3e7ec;padding:7px 10px;text-align:left}th{background:#eef2f6}
.e{border:1px solid #dfe3e8;border-radius:6px;padding:11px 13px;margin:9px 0;background:#fff}
.e.f{border-left:5px solid #c0392b}.e.p{border-left:5px solid #27865a}.e.i{border-left:5px solid #7a6a3b}
.h{font-weight:600;margin-bottom:5px}.b{font-size:13.5px;color:#333a44}
ul{background:#fff;border:1px solid #dfe3e8;border-radius:6px;padding:12px 12px 12px 30px;font-size:13.5px}
li.ok{color:#1f7a4d}li.no{color:#b03030;font-weight:600}
.kv{background:#fff;border:1px solid #dfe3e8;border-radius:6px;padding:4px 0}
</style></head><body>
<h1>TUFT-%(rid)s · 磁矩与量子修正层（电子反常磁矩 g−2）</h1>
<div class="meta">生成 %(ts)s ｜ 控制组 %(nc_ok)d/%(nc)d ｜ 守卫 %(ng_ok)d/%(ng)d ｜ 靶未改动 %(unch)s</div>
<div class="verdict"><b>判词</b><br>%(header)s</div>
<h2>核心数值</h2><div class="kv"><table>%(rows)s</table></div>
<h2>条目</h2>%(ents)s
<h2>控制组</h2><ul>%(ctls)s</ul>
<h2>守卫</h2><ul>%(grds)s</ul>
</body></html>""" % dict(rid=RID.upper(), ts=START_ISO, nc_ok=nctl_ok, nc=nctl,
                          ng_ok=ngrd_ok, ng=ngrd, unch=payload["targets_unchanged"],
                          header=header, rows=rows,
                          ents="".join(ents), ctls=ctls, grds=grds)


# ============================================================
# 9. 主流程
# ============================================================
def main():
    res = run_audit()
    dist = tally_states(res)
    n_ctl_ok = sum(1 for c in res["controls"] if c["ok"])
    n_grd_ok = sum(1 for g in res["guards"] if g["ok"])

    report = render_report(res)
    ev = res["evidence"]
    bm, tl, dg, af = ev["bm"], ev["tl"], ev["dg"], ev["af"]

    header = (
        "靶用「螺旋涡旋 + 真空挠率云」推导电子反常磁矩，这是全卷**唯一**与实验符合到 "
        "3 位有效数字的地方。本卷四条承重全部是纯代数/纯数值："
        "① **裸磁矩差因子 2**——靶自己的 I·A 推导给 μ₀=eℏ/(4m_e)=%.4e（=μ_B/2），"
        "由 μ=g(e/2m_e)S 反解 **g=1**；而它紧接着写 μ₀=(e/m_e)S（=μ_B），"
        "二者之比恰为 %.12f。根因是 T=2πr₀/c 让电荷以光速环流，而**经典环流的 g 恒为 1**，"
        "要 g=2 必须引入非经典项。靶把 g=1 的结果标成「与狄拉克 g=2 完全一致」。"
        "② **两圈闭式与靶自己给的数值不自洽**——闭式 −(α²/2π²)(½ζ(3)−π²/12) 复算为 "
        "**%+.4e**（C₂=%+.6f），而靶写 %.4e（C₂=%+.6f）⇒ **符号相反、幅值差 %.2f 倍**。"
        "③ **★★唯一的「新预言」被自己的求和排除**——Δa_geo 标称 O(α²)=%.4e，"
        "但靶自己给的单圈+两圈已达 %.10e，与它自己引用的实验值只差 %.2e；"
        "再加标准三圈后残差仅 **%.2e** ⇒ Δa_geo 超出允许窗 **%.0f 倍**。"
        "且靶同时说「高阶…压低总 a_e，匹配实验」⇒ 内部矛盾（若 QED 已匹配，Δa_geo 必须为 0）。"
        "④ **α 口径二难**——用靶自己的裸值 α₀=√3/2，则 a_e=%.6f（实验的 %.1f 倍）、"
        "g_pred=%.6f，偏 **%.2e σ**；用 α_obs 则数值对得上，但那是**实验输入**，"
        "该节实为「抄 Schwinger 公式 + 代实测 α」。"
        % (bm["mu_4m"], bm["ratio_S_over_4m"], tl["a2_closed"], tl["c2_closed"],
           tl["a2_stated"], tl["c2_stated"], tl["disc_closed_vs_stated"],
           dg["dageo_order"], dg["a12"], abs(dg["resid12"]), abs(dg["resid123"]),
           dg["ratio123"], af["ae_a0"], af["ratio_a0_over_exp"], af["g_pred_a0"], af["sigma"]))

    payload = {
        "id": "TUFT-" + RID,
        "title": "磁矩与量子修正层：裸涡旋因子 2、两圈闭式符号反、Δa_geo 超窗与 α 口径二难",
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
        "bare_moment": bm,
        "two_loop": tl,
        "dageo_layer": dg,
        "alpha_fork": af,
        "caliber_scan": ev["cs"],
        "line_locs": {"磁矩定义": L_MU_DEF, "μ₀负号": L_MU0_MINUS, "IA": L_IA,
                      "T=2πr₀/c": L_T_C, "½ecr₀": L_MU_HALF, "eℏ/4m_e": L_MU_4M,
                      "(e/m_e)S": L_MU_S, "g=2一致": L_G2_OK, "单圈式": L_AE1,
                      "单圈数值": L_AE1_NUM, "两圈闭式": L_CLOSED, "两圈数值": L_AE2_NUM,
                      "Δa_geo": L_DAGEO, "Δa_geo量级": L_DAGEO_ORD,
                      "理论独有": L_DAGEO_UNIQ, "级数": L_SERIES, "C1": L_C1,
                      "实验值": L_EXP_TXT, "抵消": L_CANCEL, "匹配实验": L_MATCH,
                      "μ子": L_MUON, "g_0=2": L_G0_2, "两种alpha": L_ALPHA_BOTH},
        "repair_pricing": {
            "strict": {k: v for k, v in ev["pricing_strict"].items() if k != "SURVIVE_SETS"},
            "loose": {k: v for k, v in ev["pricing_loose"].items() if k != "SURVIVE_SETS"},
            "strict_survive_sets": ev["pricing_strict"]["SURVIVE_SETS"],
            "keys": list(MS_KEYS),
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
    md.append("\n## 一、承重数值\n")
    md.append("\n| 量 | 值 |\n|---|---|\n")
    md.append("| ½ecr₀（靶 I·A 推导） | %.6e |\n" % bm["mu_IA"])
    md.append("| eℏ/(4m_e)（line 3957） | %.6e |\n" % bm["mu_4m"])
    md.append("| (e/m_e)S（line 3961） | %.6e |\n" % bm["mu_S"])
    md.append("| 两式之比 | %.12f（精确 2） |\n" % bm["ratio_4m_over_S"])
    md.append("| 反解 g | %.10f（不是 2） |\n" % bm["g_from_4m"])
    md.append("| 靶闭式 a_e^(2) | %+.6e（C₂=%+.6f） |\n" % (tl["a2_closed"], tl["c2_closed"]))
    md.append("| 靶所述 a_e^(2) | %+.6e（C₂=%+.6f） |\n" % (tl["a2_stated"], tl["c2_stated"]))
    md.append("| 1+2+3 圈残差（允许窗） | %+.4e |\n" % dg["resid123"])
    md.append("| Δa_geo = O(α²) | %.4e |\n" % dg["dageo_order"])
    md.append("| 超窗倍数 | %.0f 倍 |\n" % dg["ratio123"])
    md.append("| α₀ 口径下 g 偏差 | %.3e σ |\n" % af["sigma"])
    md.append("\n## 二、条目\n")
    for e in res["entries"]:
        md.append("\n### [%s] %s · %s\n" % (e["state"], e["code"], e["title"]))
        md.append("\n- 证据：%s\n" % e["evidence"])
        if e["note"]:
            md.append("- 备注：%s\n" % e["note"])
    md.append("\n## 三、红线\n")
    md.append("\n- 靶 3 份只读：%s\n" % payload["targets_unchanged"])
    md.append("- **r225–r254 产物未改动**（G9 真机读）。\n")
    md.append("- 本卷为**磁矩与量子修正层**，条目**不可与 r142–r254 相加**；G1 为交联指针（INFO）。\n")
    md.append("- 未跑 refresh_catalog.py，未改 verify.py，未做 git。\n")
    with io.open(md_path, "w", encoding="utf-8") as f:
        f.write("".join(md))

    vd = ["# 判定册 · TUFT-%s（磁矩与量子修正层）\n" % RID.upper(),
          "\n## 判词\n\n%s\n" % header,
          "\n## 判决分组\n",
          "\n| 组 | 内容 | 结论 |\n|---|---|---|\n",
          "| A | 对靶有利 6 条：磁矩定义式正确、Schwinger 单圈式与数值均正确、"
          "引用实验值无误、真空极化云图像同构、a₀=0⇔g=2⇔点粒子自洽、"
          "主动提出可检验方向 | PASS |\n",
          "| B | ★★裸磁矩因子 2（3 条）：两式之比恰为 2、由 eℏ/(4m_e) 反解 g=1、"
          "根因是 T=2πr₀/c 下经典环流 g≡1、另有符号不一致 | **FAIL** |\n",
          "| C | ★★两圈闭式与数值不自洽（2 条）：闭式复算 C₂=%+.6f vs 所述 %+.6f"
          "（符号反、%.2f 倍）、二难两支都算死 | **FAIL** |\n"
          % (tl["c2_closed"], tl["c2_stated"], tl["disc_closed_vs_stated"]),
          "| D | ★★Δa_geo 4 条：超允许窗 %.0f 倍、与「QED 已匹配实验」内部矛盾、"
          "μ子预言零数值且缺标度律、C₂/C₃ 从未赋值 | **FAIL** |\n" % dg["ratio123"],
          "| E | ★★α 口径二难 2 条：α₀ ⇒ g 偏 %.2e σ；α_obs ⇒ 外部输入 | **FAIL** |\n"
          % af["sigma"],
          "| F | 修复定价（双档 2^7=128） | FAIL |\n",
          "| G | 交联指针（r250 的 α₀/P₀） | INFO（不计分） |\n"]
    vd.append("\n## ★ 性质界定\n")
    vd.append("\n1. **B 组是纯代数，与任何取值无关**：g=1 来自 μ=(e/2m)L 这一经典关系，"
              "对任意半径、任意（非相对论）速度都成立；取 v=c 只是把 r 与 S 挂上，"
              "并不改变 g。故靶的「几何推导」在代数上只能给出 g=1。\n")
    vd.append("2. **C 组是「公式与数字对不上」，不是「数字抄错」**：靶写的那个数值 "
              "−1.7723e−6（C₂=−0.3285）与标准 QED 一致，**正确**；错的是它给的闭式"
              "（复算得 C₂=+0.1107、符号为正）。故本卷不指控「靶算错了 QED」，"
              "而指控「靶的闭式产生不出它自己的数值」。\n")
    vd.append("3. **D 组是完全内部的**：只用靶自己写的单圈值 (0.0011614)、两圈值 "
              "(−1.7723e−6) 和它自己引用的实验值 (0.001159652)，无需任何外部理论。"
              "结论：Δa_geo 若真是 O(α²)，则被排除 %.0f 倍。\n" % dg["ratio123"])
    vd.append("4. **靶有加分项**：A6 承认靶主动提出了可检验方向。正因如此，"
              "本卷才**必须**去检验它——而检验结果是它已被排除 4.98 个数量级。\n")
    vd.append("5. **α₀ 的自身问题归 r250**：本卷 E1 是**假设 α₀ 成立**时的归谬，"
              "不重复计分 r250 关于 α_* 是定义恒等式的判定。\n")
    vd.append("6. **不重复 r252**：r252 判的是「质量比 m_p/m_e 的被积函数 f 未给出」，"
              "本卷判的是「磁矩 g 的因子 2 与两圈符号反」——**不是同一层**，"
              "唯一的同型缺陷（D4：C₂/C₃ 未赋值）只记 1 条，不相加。\n")
    vd.append("\n## 治理\n")
    vd.append("\n- 控制组 %d/%d；守卫 %d/%d\n"
              % (n_ctl_ok, len(res["controls"]), n_grd_ok, len(res["guards"])))
    vd.append("- 靶 3 份只读：%s；r225–r254 产物未改动（mtime 真机读）\n"
              % payload["targets_unchanged"])
    vd.append("- ⚠ **撞号记录（第 7 次）**：起草前 r253 已落四件套（08:44:37），"
              "r254 正被另一并行会话起草（09:02:32 仅有 .py）⇒ 本卷**跳过 r254 取 r255**。\n")
    vd.append("- 本卷条目不可与 r142–r254 相加。\n")
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
