# -*- coding: utf-8 -*-
r"""
TUFT-r252 · 质量谱层（★ 新层首卷：m_p/m_e 与 m_n/m_e）
================================================================================
【命题来源】用户：「攻破」→「继续」

【取号】起草前实测 **r252/r253/r254 三树全空** ⇒ 取 **r252**。
  ⚠ 本轮撞号（第 6 次）：r251（下游物理应用层·垂直原理 FRW 与黑洞无奇点，
  08:09:31 落四件套）在本卷起草期间被**并行会话**占用
  ⇒ 按「已产四件套并登记者为权威、后到者整体改号」纪律，本卷**整体迁至 r252**，
  不改写他人文件。

【本卷定位：质量谱层】
r244/r247 攻「引力是什么 / G 从哪来」；r248 攻「单一矢量主方程」；
r250 攻「耦合常数跑动（RG）」。本卷攻靶**另一端的核心数值宣称**：

    靶声称从「三重螺旋涡旋拓扑」推出质子–电子质量比
    m_p/m_e = 3[1 + ∫_{μ_e}^{Λ_QCD} (dμ/μ) f(α_s,α)] ≈ 1836.15

★ 本卷三条承重发现（全部机读 + 机算，不依赖外部理论判真假）：

  ① **反解拟合**：来料 line 4156–4159 逐字写「实验比值 Ω_exp≈1836.15 →
     反推：1+𝒦=1836.15/3=612.05 ⇒ 𝒦≈611.05」。1 个未知数对 1 个已知数，
     恒可解 ⇒ 判别力 0（配正对照：Ω 换成 100/1000/1e6/π 同样「成功」）。

  ② **主结果未求值**：boxed 主结果（line 4179）**不含任何数值**，
     而后面的体系汇总表（line 4226）同一式子却写了 ≈1836.15。
     靶 line 4183 自认「目前还没有把 f(α_s,α) 解析封闭形式求出来」，
     line 4184 自认「需要后续格点数值仿真…才能得到高精度数值」。
     ⇒ 数值只能来自实验值回代。量化缺口：积分跨度仅 ln(Λ_QCD/μ_e)=5.9697 个
     e-fold，要攒出 𝒦=611.05 需 **f̄=102.36**，而靶自己给的全部耦合
     (α_s≈1、α_*≈0.866、α_obs≈0.0073) 都是 O(1)–O(10⁻²) ⇒ 缺口 **102×**。
     五个自然候选 f 全部对不上（差 1.34×–586×）。

  ③ **权重 3 的通道线性相关**：来料 line 4147 明列三个通道
     κ²、τ²、ω²/c²，并写 ω²/c²=κ²+τ²（本源公理 ω²=c²(κ²+τ²)）
     ⇒ 第三通道 = 前两通道之和 ⇒ 独立通道数 = 2 ≠ 3。
     二难：要么第三通道不独立（权重 3 无来源），
     要么它独立于公理（与本源公理冲突）。

  附：**中子质量换名**——𝒦_n−𝒦_p ≡ (m_n−m_p)/(3m_e) 是纯代数恒等式
     （Fraction 残差**严格 0**），靶却赋予「SU(2) 弱耦合微小扰动」的物理诠释
     ⇒ 定义恒等式刀（承 r204/r247）。

【分层】本卷是**质量谱层**，与 r244（引力本体论层）、r247（元审计层）、
r248（单方程全域力层）、r250（耦合常数跑动层）领域不同，**条目不可相加**。
靶 line 4162 借用 α_*=√3/2、line 4161 借用 α_s≈1，这两者在 **r250 已被判**，
本卷只作**交联指针（INFO）**，不重复计分。
本源公理 ω²=c²(κ²+τ²) 在 r248 已被用于另一攻击面（自旋 ℏ/2）；
本卷用的是它在**通道计数**上的后果——后果不同，只记 1 条，不相加。
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
RID = "r252"
BASE_NAME = ("TUFT-r252_质量谱层_mpme反解拟合与未定值积分_"
             "权重3通道线性相关与中子质量换名_精算与可视化_2026-10-31")
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
M_E_MEV = 0.51099895000        # 电子静能 MeV（CODATA 2018）
M_P_MEV = 938.27208816         # 质子静能 MeV（CODATA 2018）
M_N_MEV = 939.56542052         # 中子静能 MeV（CODATA 2018）

# 靶自己给的参数（来料 line 4161/4162）
LAMBDA_QCD_MEV = 200.0         # 靶：「Λ_QCD≈200 MeV」
ALPHA_S_QCD = 1.0              # 靶：「α_s(Λ_QCD)≈1」
A_STAR = math.sqrt(3.0) / 2.0  # 靶：「大统一固定点 α_*=√3/2≈0.866」
ALPHA_OBS = 7.2973525693e-3    # CODATA 精细结构常数
V_EW_MEV = 246220.0            # 电弱真空期望值 246.22 GeV（PDG）

OMEGA_EXP = M_P_MEV / M_E_MEV          # 1836.15267343
OMEGA_N_EXP = M_N_MEV / M_E_MEV        # 1838.68366172


def fmt_rel(x):
    return "{:.3e}".format(x)


def rel(a, b):
    if b == 0:
        return float("inf") if a != 0 else 0.0
    return abs(a - b) / abs(b)


def disc(model, exp):
    """差异倍数（≥1）：max(model/exp, exp/model)"""
    r = model / exp
    return max(r, 1.0 / r) if r > 0 else float("inf")


# ============================================================
# 2. 靶机读（含上游 LaTeX 污染修复，承 r247）
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
    r"""上游把字母 X 批量替换成 \(\boldsymbol{X}\)（t 最普遍，\hbar 里的 b 同理）。
    用精确字符串替换，避免正则转义陷阱。另折叠 \r\r\n 双重换行。"""
    for ch in _ALPHA52:
        s = s.replace("\\(\\boldsymbol{" + ch + "}\\)", ch)
    return re.sub(r"[\r\n]+", "\n", s)


SHA_AT_IMPORT = {p: sha256_of(p) for p in TARGETS}
TARGET_TEXT = {p: read_text(p) for p in TARGETS}
RAW = TARGET_TEXT.get(TARGETS[0], "")
ALL_RAW = "".join(TARGET_TEXT.get(p, "") for p in TARGETS)
# 去污染后的全文 / 行（供机读定位）
ALL = depollute(ALL_RAW)
RAW_LINES = depollute(RAW).split("\n")
ALL_LINES = ALL.split("\n")

# 抗污染子串定位（承 r247：含 \hbar/\boxed 的完整正则会命中 0）
BOXED_MPME = [i + 1 for i, s in enumerate(ALL_LINES)
              if "oxed{\\frac{m_p}{m_e}" in s]
BOXED_MPME_WITH_NUM = [ln for ln in BOXED_MPME if "1836" in ALL_LINES[ln - 1]]
BOXED_MPME_NO_NUM = [ln for ln in BOXED_MPME if "1836" not in ALL_LINES[ln - 1]]

# 注意：「反推：」独占一行，与含 1836 的式子不在同一行 ⇒ 不可 AND（否则命中 0）
L_REVERSE = [i + 1 for i, s in enumerate(RAW_LINES) if "反推" in s]
L_REVERSE_NUM = [i + 1 for i, s in enumerate(RAW_LINES) if "1836.15/3" in s]
L_MPME_ALL = [i + 1 for i, s in enumerate(ALL_LINES) if "\\frac{m_p}{m_e}" in s]
L_MPME_NUM = [ln for ln in L_MPME_ALL if "1836" in ALL_LINES[ln - 1]]
L_K611 = [i + 1 for i, s in enumerate(RAW_LINES)
          if re.search(r"611\.05", s) or re.search(r"611\b", s)]
L_OMEGA3 = [i + 1 for i, s in enumerate(RAW_LINES) if "\\Omega = 3" in s]
L_CHANNELS = [i + 1 for i, s in enumerate(RAW_LINES)
              if "kappa^2" in s and "tau^2" in s and "omega^2/c^2" in s]
L_FDEF = [i + 1 for i, s in enumerate(RAW_LINES) if "权重函数" in s]
L_NOF = [i + 1 for i, s in enumerate(RAW_LINES)
         if "没有把" in s and "解析封闭形式" in s]
L_LATTICE = [i + 1 for i, s in enumerate(RAW_LINES) if "格点数值仿真" in s]
L_GOT611 = [i + 1 for i, s in enumerate(RAW_LINES) if "得到" in s and "611" in s]
L_CAND = [i + 1 for i, s in enumerate(RAW_LINES) if "权重候选" in s]
L_HONEST1 = [i + 1 for i, s in enumerate(RAW_LINES) if "不能由纯初等几何恒等式" in s]
L_HONEST2 = [i + 1 for i, s in enumerate(RAW_LINES) if "模型构造" in s]
L_MUN = [i + 1 for i, s in enumerate(RAW_LINES) if "m_n}{m_e}" in s]
L_SU2 = [i + 1 for i, s in enumerate(RAW_LINES) if "SU(2)" in s and "m_n" in s]
L_EWSCALE = [i + 1 for i, s in enumerate(RAW_LINES) if "电弱标度" in s]
L_MUSCALE = [i + 1 for i, s in enumerate(RAW_LINES) if "电子标度" in s]


def count(pat, text=None):
    return len(re.findall(pat, text if text is not None else ALL))


# ============================================================
# 3. ★ 核心计算
# ============================================================
def reverse_fit(omegas):
    r"""① 反解拟合：Ω=3(1+𝒦) ⇒ 𝒦=Ω/3−1。1 未知数 1 已知数，恒可解。"""
    rows = []
    for o in omegas:
        k = o / 3.0 - 1.0
        back = 3.0 * (1.0 + k)
        rows.append({"omega": o, "K": k, "back": back,
                     "resid": abs(back - o)})
    return rows


def integral_layer():
    r"""② 积分层：靶给了上下限的两个互斥读法，各自需要多大的被积函数？"""
    ln_mue = math.log(LAMBDA_QCD_MEV / M_E_MEV)      # 读法 A：μ_e → Λ_QCD
    ln_ew = math.log(LAMBDA_QCD_MEV / V_EW_MEV)      # 读法 B：电弱标度 → Λ_QCD（靶写的顺序）
    ln_ew_rev = math.log(V_EW_MEV / LAMBDA_QCD_MEV)  # 读法 C：反向
    kp = OMEGA_EXP / 3.0 - 1.0
    return {
        "K_p": kp,
        "ln_mue": ln_mue,
        "ln_ew": ln_ew,
        "ln_ew_rev": ln_ew_rev,
        "fbar_mue": kp / ln_mue,
        "fbar_ew": kp / ln_ew,          # 负值！
        "fbar_ew_rev": kp / ln_ew_rev,
        "max_target_coupling": max(ALPHA_S_QCD, A_STAR, ALPHA_OBS),
        "gap_vs_target": (kp / ln_mue) / max(ALPHA_S_QCD, A_STAR, ALPHA_OBS),
    }


def f_candidates():
    r"""② 续：给 f 五个自然候选，实测 Ω 并与实验比。"""
    ln_mue = math.log(LAMBDA_QCD_MEV / M_E_MEV)
    cands = (
        ("f=1", 1.0),
        ("f=α_s(Λ_QCD)≈1（靶给）", ALPHA_S_QCD),
        ("f=α_*=√3/2（靶给）", A_STAR),
        ("f=1/α_obs", 1.0 / ALPHA_OBS),
        ("f=α_obs", ALPHA_OBS),
    )
    rows = []
    for nm, f in cands:
        k = f * ln_mue
        o = 3.0 * (1.0 + k)
        rows.append({"name": nm, "f": f, "K": k, "omega": o,
                     "disc": disc(o, OMEGA_EXP)})
    best = min(r["disc"] for r in rows)
    return {"rows": rows, "best_disc": best, "all_miss": best > 1.05}


def channel_layer():
    r"""③ 通道计数：κ², τ², ω²/c²，且 ω²/c²=κ²+τ² ⇒ 线性相关。"""
    # 取三个数值样例，验证 c3 == c1 + c2（由本源公理强制）
    rows = []
    for k2, t2 in ((1.0, 1.0), (2.0, 3.0), (0.5, 7.0)):
        c1, c2, c3 = k2, t2, k2 + t2
        rows.append({"k2": k2, "t2": t2, "c1": c1, "c2": c2, "c3": c3,
                     "resid": abs(c3 - (c1 + c2))})
    # 若为独立通道，权重应为 3；靶的分解给出独立数 2
    return {"rows": rows, "n_listed": 3, "n_independent": 2,
            "max_resid": max(r["resid"] for r in rows)}


def neutron_layer():
    r"""附：中子质量——𝒦_n−𝒦_p ≡ (m_n−m_p)/(3m_e) 是纯代数恒等式。"""
    fr_me = Fraction(str(M_E_MEV))
    fr_mp = Fraction(str(M_P_MEV))
    fr_mn = Fraction(str(M_N_MEV))
    kp_f = (fr_mp / fr_me) / 3 - 1
    kn_f = (fr_mn / fr_me) / 3 - 1
    diff_f = kn_f - kp_f
    rhs_f = (fr_mn - fr_mp) / (3 * fr_me)
    resid_exact = diff_f - rhs_f                      # 应严格 0
    kp = float(kp_f); kn = float(kn_f)
    ratio_lhs = float(diff_f) / kp                    # (𝒦_n−𝒦_p)/𝒦_p
    ratio_rhs = (M_N_MEV - M_P_MEV) / (M_P_MEV - 3.0 * M_E_MEV)
    return {
        "K_p": kp, "K_n": kn, "K_diff": float(diff_f),
        "rhs": float(rhs_f), "resid_exact_num": resid_exact.numerator,
        "resid_exact_den": resid_exact.denominator,
        "resid_is_zero": (resid_exact == 0),
        "ratio_lhs": ratio_lhs, "ratio_rhs": ratio_rhs,
        "ratio_resid": abs(ratio_lhs - ratio_rhs),
        "omega_n_calc": float(fr_mn / fr_me),
        "omega_n_target": 1838.68,
        "omega_n_resid": abs(float(fr_mn / fr_me) - 1838.68),
        "mn_mp_mev": M_N_MEV - M_P_MEV,
    }


def caliber_scan():
    r"""机读：靶到底给了哪些数值？缺口在哪？（防「凭印象指控」）"""
    pats = {
        "反推（明示）": r"反推",
        "611.05": r"611\.05",
        "611（含 611.05）": r"611",
        "权重候选": r"权重候选",
        "权重函数": r"权重函数",
        "电弱标度": r"电弱标度",
        "电子标度": r"电子标度",
        "Λ_QCD": r"Lambda_\{\\text\{QCD\}\}",
        "α_s": r"\\alpha_s",
        "f(" : r"f\\\(|f\\left",
        "SU(2)": r"SU\(2\)",
        "格点": r"格点",
    }
    out = {k: count(v) for k, v in pats.items()}
    # 靶是否给出所需被积函数量级 102 / 85 附近的数值
    out["102.36 或 102.35"] = count(r"102\.3")
    out["85.87 或 85.9"] = count(r"85\.8|85\.9")
    out["μ_e 的数值（0.511）"] = count(r"0\.511")
    out["0.51099895"] = count(r"0\.51099895")
    # f 的显式函数式（f = … 或 f(…) = …）
    out["f 的显式定义式"] = count(r"f\s*\(\s*\\alpha_s[^)]*\)\s*=")
    return out


# ============================================================
# 4. 修复定价
# ============================================================
MS_KEYS = ("f_closed_form", "fbar_source", "K_independent", "weight3_derived",
           "bounds_fixed", "QCD_free", "neutron_derived")
# fbar_source：被积函数量级 f̄≈102.36 有理论来源（正是 C3 实测的缺口）
REQ_STRICT = {"f_closed_form", "fbar_source", "K_independent",
              "weight3_derived", "bounds_fixed"}
REQ_LOOSE = {"f_closed_form", "fbar_source", "K_independent"}


def repair_pricing(req):
    r"""
    EMPTY  = req ⊄ have（条件不齐备 ⇒ 交付不出）
    SUICIDE= req ⊆ have 且 QCD_free ∉ have
             （必须引入 QCD/格点输入才能算出 𝒦 ⇒ 原「纯螺旋涡旋几何」宣称被替换）
    SURVIVE= req ⊆ have 且 QCD_free ∈ have（真从几何算出，不借 QCD）
    """
    from itertools import product
    out = {"EMPTY": 0, "SUICIDE": 0, "SURVIVE": 0, "SURVIVE_SETS": []}
    for combo in product((False, True), repeat=len(MS_KEYS)):
        have = {k for k, v in zip(MS_KEYS, combo) if v}
        if not req.issubset(have):
            out["EMPTY"] += 1
        elif "QCD_free" not in have:
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
# 6. 真机读守卫 / AST 自审器（含 IfExp 补丁，承 r247）
# ============================================================
def scan_untouched(lo=225, hi=252):
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
    ok = (dist.get("FAIL", 0) >= 8) and (dist.get("PASS", 0) >= 4)
    return ok, "实测分布 %s（要求 FAIL≥8 且 PASS≥4）" % dist


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
    r"""自审器：ent/ctl/grd 第三个参数禁写死 True/False；覆盖 IfExp 形态。"""
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
    """找他人卷源码做自审器正对照"""
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

    rf = reverse_fit((OMEGA_EXP, 100.0, 1000.0, 1.0e6, math.pi, 2.0))
    ig = integral_layer()
    fc = f_candidates()
    ch = channel_layer()
    nt = neutron_layer()
    cs = caliber_scan()
    p_strict = repair_pricing(REQ_STRICT)
    p_loose = repair_pricing(REQ_LOOSE)
    EVIDENCE.update({"rf": rf, "ig": ig, "fc": fc, "ch": ch,
                     "nt": nt, "cs": cs,
                     "pricing_strict": p_strict, "pricing_loose": p_loose})

    self_path = os.path.join(SRC_DIR, BASE_NAME + ".py")
    self_bad, self_msg = ast_scan_hardcoded(self_path)
    r244_path = find_other_volume_src("r244")
    oth_bad, oth_msg = ast_scan_hardcoded(r244_path) if r244_path else ([], "（未找到 r244 源码）")

    # ============================================================
    # A 组 · 对靶有利（先证明对的部分）
    # ============================================================
    ent("A1", "量纲层自洽：m_p/m_e 无量纲，𝒦 无量纲，∫dμ/μ 无量纲，f 无量纲", "PASS",
        "靶的 boxed 式 m_p/m_e=3[1+∫(dμ/μ)f(α_s,α)]：左端两个质量之比 [M]/[M]=1；"
        "𝒦 被明写为「无量纲因子」（来料 line 4155）；∫dμ/μ 的对数跨度无量纲；"
        "故 f 必须无量纲 ⇒ 四者一致。机读「无量纲因子」命中 %d 处。"
        % count(r"无量纲"),
        "对靶有利：本卷**不**在量纲层攻击——这一层是干净的。"
        "本卷的攻击点全部落在「数值从哪来」上（见 B–E 组）。")
    ent("A2", "主质量公式 m=(ℏ/c)√(κ²+τ²) 量纲 [M] 正确", "PASS",
        "[ℏ/c]=[M L²T⁻¹]/[L T⁻¹]=[M L]；[√(κ²+τ²)]=[L⁻¹] ⇒ [m]=[M]。"
        "来料 line 1132/2758 boxed 逐字给出式(5) m=(ℏ/c)√(κ²+τ²)。",
        "对靶有利：质量定义式量纲无误；本卷沿用 r248 的这一结论作基线，不重复计分。")
    ent("A3", "靶主动声明 1836.15267343 不能由几何恒等式得到，且属模型构造（诚实）", "PASS",
        "来料 line %s 逐字：「真实物理里 $m_p/m_e\\approx1836.15267343$，这个数值"
        "**不能由纯初等几何恒等式精确解析得到**，QCD束缚态质量主要来自胶子场的"
        "量子色动力学束缚能…并非简单整数/根号几何比值」；line %s：「下面是本TUFT框架下的"
        "**拓扑涡旋模型推导，属于理论模型构造，不是已经被实验证明的第一性精确解**」。"
        % (L_HONEST1[:4], L_HONEST2[:4]),
        "对靶有利：靶**没有把模型冒充精确解**，且正确指出了 QCD 束缚能才是质子质量主体。"
        "本卷判的不是「靶不诚实」，而是「即便按靶自己的降级声明，"
        "该式仍然产生不了任何数值」（见 B/C 组）。")
    ent("A4", "靶主动把权重 3 标为「候选」，未自称已证（诚实）", "PASS",
        "来料 line %s 逐字标题为「三重拓扑缠绕的几何权重**候选**：」，"
        "机读「权重候选」命中 %d 处。" % (L_CAND[:4], cs["权重候选"]),
        "对靶有利：靶用了「候选」这个限定词。⇒ 本卷 D 组判的是"
        "「候选**无法升级为结论**」，而不是「靶隐瞒了它是候选」。")
    ent("A5", "靶主动列出缺陷并承认需后续数值仿真（诚实）", "PASS",
        "来料 line %s 逐字：「❗ 缺陷：目前还**没有把 $f(\\alpha_s,\\alpha)$ 解析封闭形式"
        "求出来**」；line %s：「不能宣称这是严格第一性精确解析解…需要后续格点数值仿真"
        "（FDTD涡旋演化+MCMC参数扫描）来数值求解积分」。机读「格点」%d 处。"
        % (L_NOF[:4], L_LATTICE[:4], cs["格点"]),
        "对靶有利：这是**自我披露**。⇒ 本卷 B 组的「未求值」判定与靶的自述"
        "**方向一致**；本卷新增的是把它**量化**（需 f̄=%.2f、缺口 %.1f×）"
        "并指出汇总表仍写了 ≈1836.15（B2）。" % (ig["fbar_mue"], ig["gap_vs_target"]))
    ent("A6", "定性物理图像与格点 QCD 结论兼容", "PASS",
        "来料 line 4170–4171：「质子质量 ≠ 三个夸克组分质量之和」；"
        "「质子绝大部分质量 = 三重交缠螺旋涡旋场的禁闭场能…和格点QCD结论一致："
        "强子质量主要来自量子场能，不是希格斯组分质量」。"
        "这与标准强子物理（质子质量 ≈ 95%% 来自 QCD 场能）方向一致。",
        "对靶有利：**物理图像**是对的。本卷攻击的是「从图像到 1836.15 这个数」"
        "的那一步缺失，不是图像本身。")

    # ============================================================
    # B 组 · ★★ 反解拟合（零判别力）
    # ============================================================
    ent("B1", "★★ 靶逐字写「反推」：𝒦=Ω_exp/3−1=%.5f，1 未知数对 1 已知数 ⇒ 判别力 0"
        % rf[0]["K"], "FAIL",
        "来料 line %s 逐字：「> 实验比值 $\\Omega_\\text{exp}\\approx1836.15$ / "
        "> **反推**：/ > $$1+\\mathcal{K}=1836.15/3=612.05$$ / > $$\\mathcal{K}\\approx611.05$$」。"
        "（「反推」二字出现在 line %s，紧随其后 line %s 给出 1836.15/3=612.05。）"
        "本卷复算 𝒦=%.5f（回代 Ω=%.5f，残差 %s）。方程 Ω=3(1+𝒦) 有 1 个未知数、"
        "1 个已知数 ⇒ **对任意 Ω>3 恒有实数解 𝒦=Ω/3−1**。"
        % (L_REVERSE[:4], L_REVERSE[:4], L_REVERSE_NUM[:4],
           rf[0]["K"], rf[0]["back"], fmt_rel(rf[0]["resid"])),
        "★这不是「推导 𝒦」，是**用 Ω_exp 定义 𝒦**。与 r250 的 P_0=%.2f 同族"
        "（同一手法：1 未知数 + 1 已知数 = 零判别力）。" % (A_STAR / ALPHA_OBS - 1.0))
    ent("B2", "★ 正对照：把 Ω_exp 换成 100/1000/1e6/π/2，同一流程全部「成功」", "FAIL",
        "本卷机算：%s。**每一个**都能解出对应的 𝒦 并完美回代（残差均 < 1e-12）。"
        % "；".join("Ω=%.4g ⇒ 𝒦=%.4f" % (r["omega"], r["K"]) for r in rf[1:]),
        "⇒ 该流程**不排除任何 Ω 值**，因此不能用来「推出」1836.15。"
        "判别力为 0 的含义：若有一天实验值是 100 或 10000，这套流程同样「推」出来。")
    ent("B3", "★ 判别力未行使（非「零判别力」）：一旦 𝒦 被独立固定，式子立刻可证伪", "FAIL",
        "本卷给 f 一个最简单的独立取值 f=1（即被积函数常数 1），则 "
        "𝒦=ln(Λ_QCD/μ_e)=%.6f ⇒ Ω=3(1+𝒦)=%.4f，与实验值 %.5f 差 **%.2f 倍**。"
        % (ig["ln_mue"], 3.0 * (1.0 + ig["ln_mue"]), OMEGA_EXP,
           disc(3.0 * (1.0 + ig["ln_mue"]), OMEGA_EXP)),
        "★性质界定（承 r218 教训：**判别力先测后指控**）："
        "该式**有判别力**——𝒦 一旦被独立确定，立刻与实验冲突 88 倍。"
        "靶的问题不是「式子无法证伪」，而是**从未把 𝒦 独立定下来**（见 C 组）。")

    # ============================================================
    # C 组 · ★★ 主结果未求值（预测预算 0）
    # ============================================================
    ent("C1", "★★ boxed 主结果在推导处无数值、在汇总表有数值：同一式子两处不一致", "FAIL",
        "本卷机读全部 \\boxed{m_p/m_e=…} ——共 **%d 处**（行号 %s）；"
        "其中**含** 1836 数值的 %d 处（行 %s），**不含**数值的 %d 处（行 %s）。"
        "放宽到非 boxed 的同类式：含 \\frac{m_p}{m_e} 的式子共 **%d 处**（行 %s），"
        "其中含 1836 数值的 %d 处（行 %s）。"
        "⇒ 推导章（line 4179，位于「第四步：数值对比与诚实审计」标题下）的 boxed 式"
        "**只有积分、没有数值**；而体系汇总表（line 4226）的同一式子却写了 ≈1836.15。"
        % (len(BOXED_MPME), BOXED_MPME[:8], len(BOXED_MPME_WITH_NUM),
           BOXED_MPME_WITH_NUM[:8], len(BOXED_MPME_NO_NUM), BOXED_MPME_NO_NUM[:8],
           len(L_MPME_ALL), L_MPME_ALL[:8], len(L_MPME_NUM), L_MPME_NUM[:8]),
        "★这是**靶自己文本内部**的不一致：一处承认算不出来，一处已经给出数值。"
        "而 1836.15 的唯一来源就是 line 4175 的实验值 ⇒ **实验值 → 反解 𝒦 → 写回「模型」**。")
    ent("C2", "★★ 循环：靶先说积分「得到 𝒦≈611」，后说「还没求出 f」", "FAIL",
        "来料 line %s：「这个积分就是…最后得到 $\\mathcal{K}\\approx611$」；"
        "line %s：「目前还**没有把 $f(\\alpha_s,\\alpha)$ 解析封闭形式求出来**」。"
        "机读「611」共 %d 处，无一来自积分计算。 ⇒ 611 **不是积分算出来的**。"
        % (L_GOT611[:4], L_NOF[:4], cs["611（含 611.05）"]),
        "★内部矛盾：被积函数都还没有，积分值不可能已经「得到」。"
        "⇒ 611.05 的来源只能是 B1 的反解。")
    ent("C3", "★★ 被积函数量级缺口：需要 f̄=%.2f，而靶给的全部耦合最大才 %.3f ⇒ 缺口 %.0f 倍"
        % (ig["fbar_mue"], ig["max_target_coupling"], ig["gap_vs_target"]), "FAIL",
        "按靶自己给的参数：μ_e=m_e c²=%.8f MeV、Λ_QCD≈%g MeV（line 4161）⇒ "
        "对数跨度 ln(Λ_QCD/μ_e)=%.6f 个 e-fold。要攒出 𝒦=%.5f，"
        "被积函数**平均值**必须 f̄=𝒦/ln=%.4f。而靶给的三个耦合："
        "α_s(Λ_QCD)≈1、α_*=√3/2=%.4f、α_obs=%.4e，**全部 O(1)–O(10⁻²)**。"
        "机读：语料中 102.3 命中 %d 处、85.8/85.9 命中 %d 处、"
        "f 的显式定义式（形如 f(α_s,…)=…）命中 **%d 处**。"
        % (M_E_MEV, LAMBDA_QCD_MEV, ig["ln_mue"], ig["K_p"], ig["fbar_mue"],
           A_STAR, ALPHA_OBS, cs["102.36 或 102.35"], cs["85.87 或 85.9"],
           cs["f 的显式定义式"]),
        "★这是**量化**的：不是「f 未定义」这种定性说法，而是"
        "「即便 f 是常数，它也必须是 102.36，而靶的理论里没有任何 O(100) 的无量纲量」。")
    ent("C4", "★ 五个自然候选 f 全部对不上 1836.15（最接近也差 %.3f 倍）" % fc["best_disc"], "FAIL",
        "本卷机算（f 取常数、跨度 ln=%.4f）：%s。**无一命中**。"
        % (ig["ln_mue"],
           "；".join("%s ⇒ Ω=%.4f（差 %.2f×）" % (r["name"], r["omega"], r["disc"])
                     for r in fc["rows"])),
        "⇒ f 必须被**精细调谐**到 ≈%.2f 才可能对上，而该数值在语料中**不存在**（%d 处）。"
        "这正是「拟合」而非「推导」的操作特征：把一个自由度调到目标值。"
        % (ig["fbar_mue"], cs["102.36 或 102.35"]))
    ent("C5", "★ 积分下限自相矛盾：一处说「电子标度」、一处说「电弱标度」", "FAIL",
        "来料 line %s（积分定义处，line 4165 上下限 μ_e→μ_QCD）+ line %s 文字："
        "「从**电子标度**一直积分到QCD禁闭标度」；但 line %s 又写："
        "「由RG流从**电弱标度**积分到QCD禁闭标度累积产生」。"
        "二者相差 %.0f 倍（0.511 MeV vs 246220 MeV）。"
        % (L_MUSCALE[:4], L_MUSCALE[:4], L_EWSCALE[:4], V_EW_MEV / M_E_MEV),
        "★后果（机算）：若按「电弱标度→Λ_QCD」这个**靶写的上下限顺序**，"
        "ln(Λ_QCD/v)=%.4f 为**负** ⇒ 要得到 𝒦=+%.2f，被积函数必须 f̄=%.2f（**负值**），"
        "与「耦合权重函数」的正定性冲突；若把积分反过来读（Λ_QCD→电弱标度），"
        "ln=%.4f ⇒ 需 f̄=%.2f。三种读法给出 %.2f / %.2f / %.2f 三个**互不相同**的所需值，"
        "而靶**从未指定**下限的数值（机读 0.511 命中 %d 处）。"
        % (ig["ln_ew"], ig["K_p"], ig["fbar_ew"], ig["ln_ew_rev"], ig["fbar_ew_rev"],
           ig["fbar_mue"], ig["fbar_ew"], ig["fbar_ew_rev"], cs["μ_e 的数值（0.511）"]))

    # ============================================================
    # D 组 · ★★ 权重 3 的通道线性相关
    # ============================================================
    ent("D1", "★★ 三个通道线性相关：ω²/c²=κ²+τ² ⇒ 独立通道数 = 2，不是 3", "FAIL",
        "来料 line %s 明列三个通道「$$\\kappa^2,\\ \\tau^2,\\ \\omega^2/c^2=\\kappa^2+\\tau^2$$」，"
        "而本源公理（line 4193）为 ω²=c²(κ²+τ²) ⇒ **第三通道 ≡ 第一通道 + 第二通道**。"
        "本卷机验三组取值，残差最大 %s（严格 0）。"
        % (L_CHANNELS[:4], fmt_rel(ch["max_resid"])),
        "★若权重 3 来自「三个正交通道叠加」，则它数的是**列出**的对象数 3，"
        "而非**独立**的对象数 2 —— 而叠加只能对独立分量计数。"
        "⇒ 权重 3 与靶自己的通道分解不相容。")
    ent("D2", "★ 二难：第三通道要么不独立（权重 3 无来源），要么独立于公理（与本源公理冲突）", "FAIL",
        "分支一：承认 ω²/c²=κ²+τ²（本源公理）⇒ 第三通道是前两者之和 ⇒ 独立数 2 ⇒"
        "「三重」不成立、权重 3 无来源。分支二：坚持第三通道独立 ⇒ 必须放弃 "
        "ω²=c²(κ²+τ²)，而这正是靶整套体系的**第一公理**（line 4125 本源公理）。"
        "两条分支都通向失败。",
        "★注：本源公理 ω²=c²(κ²+τ²) 在 r248 已被用于**另一后果**（自旋 ℏ/2 被自己公式排除）。"
        "本卷用的是它在**通道计数**上的后果——后果不同，属本层，只记 1 条，**不与 r248 相加**。")
    ent("D3", "★ 权重 3 与靶自己的物理图像冲突：靶自认质子质量 ≠ 三夸克质量之和", "FAIL",
        "来料 line 4170 逐字：「质子质量 ≠ 三个夸克组分质量之和」；line 4149："
        "「三重涡旋的总场能，等于三个正交通道场能叠加，**加上交叉耦合能**」，"
        "交叉项来自 V∝(κ²+τ²−ω²/c²)² 展开的 κ²τ²。但若严格按该分解，"
        "总场能含 κ²+τ²+ω²/c²+κ²τ² = 2(κ²+τ²)+κ²τ²，**不是** 3(1+𝒦) 的形式。",
        "⇒ 从「三个通道 + 交叉耦合能」到「3(1+𝒦)」这一步**没有给出推导**；"
        "配合 A4（靶自称「候选」），该权重目前是**未证成的取值**。")

    # ============================================================
    # E 组 · ★ 中子质量换名（定义恒等式刀）
    # ============================================================
    ent("E1", "★★ 𝒦_n−𝒦_p ≡ (m_n−m_p)/(3m_e) 是纯代数恒等式（Fraction 残差**严格 0**）", "FAIL",
        "由 𝒦=m/(3m_e)−1：𝒦_n−𝒦_p=(m_n/m_e−m_p/m_e)/3=(m_n−m_p)/(3m_e)。"
        "本卷用 Fraction 精确有理数代入 m_e=%.8f、m_p=%.8f、m_n=%.8f MeV："
        "左端 %.8f，右端 %.8f，残差分子 %d ⇒ **严格 0**（非浮点近似）。"
        "同理 (𝒦_n−𝒦_p)/𝒦_p = %.6e ≡ (m_n−m_p)/(m_p−3m_e) = %.6e，残差 %s。"
        % (M_E_MEV, M_P_MEV, M_N_MEV, nt["K_diff"], nt["rhs"],
           nt["resid_exact_num"], nt["ratio_lhs"], nt["ratio_rhs"],
           fmt_rel(nt["ratio_resid"])),
        "★定义恒等式刀（承 r204/r247）：靶把这个**必然成立**的代数恒等式"
        "赋予物理诠释——line 4190 逐字：「$m_n-m_p\\approx1.293$ MeV 这个微小质量差，"
        "本理论解释为：**弱相互作用通道（n法向极化挠率）带来微小拓扑能差**，"
        "来自SU(2)弱耦合的微小扰动」。但恒等式对**任何**解释都成立，"
        "换成「电磁自能」「希格斯耦合」「随机数」也得到同一个数 ⇒ **零判别力、事后贴标签**。")
    ent("E2", "★ m_n/m_e=1838.68 也是实验值换名，𝒦_n 无独立计算", "FAIL",
        "本卷由 CODATA 直接算得 m_n/m_e=%.8f，靶写 1838.68（残差 %s）⇒ "
        "靶的数值就是实验值。对应 𝒦_n=%.5f，同样来自反解 Ω_n/3−1，"
        "语料中无 𝒦_n 的积分计算。机读「电弱标度」%d 处、「SU(2)」%d 处，"
        "但**无**任何把 SU(2) 耦合换算成 %.6e 这个差值的式子。"
        % (nt["omega_n_calc"], fmt_rel(nt["omega_n_resid"]), nt["K_n"],
           cs["电弱标度"], cs["SU(2)"], nt["ratio_lhs"]),
        "⇒ 靶对 m_n−m_p 的「解释」是**命名**不是**计算**："
        "它把一个已知的 1.293 MeV 改称「弱相互作用通道拓扑能差」，"
        "但没有给出任何能先验算出 1.293 的方程。")

    # ============================================================
    # F 组 · 交联指针（INFO，不重复计分）
    # ============================================================
    ent("F1", "交联（INFO，不计分）：本卷借用的 α_* 与 α_s 已在 r250 被判", "INFO",
        "来料 line 4161–4162 借用 α_s(Λ_QCD)≈1 与 α_*=√3/2 来估算 𝒦。"
        "r250 已独立判定：α_*=√3/2 是**定义恒等式**（m_e 缩放 1e-3→1e6 时 α 极差 %s），"
        "且用靶第 9 条算 μ_Planck 得 α=7.93e-3 与第 10 条断言的 0.866 差 109 倍。"
        "⇒ 本卷 C3/C4 用的 α_*=%.4f 只是**沿靶口径代入**，其自身问题归 r250。"
        % (fmt_rel(1.11e-16), A_STAR),
        "★分层铁律：本卷**不**把 r250 的条目相加进来，只作指针。"
        "本卷独立成立的部分是 B/C/D/E 组——它们**不依赖** α_* 是否正确"
        "（C3 的缺口 %.0f 倍在把 α_* 换成 1 或 α_obs 时只会更大）。" % ig["gap_vs_target"])

    # ============================================================
    # G 组 · 修复定价
    # ============================================================
    ent("G1", "修复定价（双档）：严格档 EMPTY %d / SUICIDE %d / SURVIVE %d；"
        "宽松档 %d / %d / %d ⇒ 原「从涡旋几何推出 m_p/m_e」宣称 %d 条不借 QCD 的存续路径"
        % (p_strict["EMPTY"], p_strict["SUICIDE"], p_strict["SURVIVE"],
           p_loose["EMPTY"], p_loose["SUICIDE"], p_loose["SURVIVE"],
           p_loose["SURVIVE"]), "FAIL",
        "7 个结构槽位（2^7=128 组合）：%s。严格档最小可交付 REQ={f 封闭形式, "
        "f̄ 量级有来源, 𝒦 独立计算, 权重3被导出, 上下限唯一确定}："
        "EMPTY %d / SUICIDE %d / SURVIVE %d；"
        "宽松档 REQ={f 封闭形式, f̄ 量级有来源, 𝒦 独立计算}：EMPTY %d / SUICIDE %d / SURVIVE %d。"
        "SUICIDE 定义：条件齐备但 **QCD_free ∉ have** ⇒ 必须引入 QCD/格点输入才能算出 𝒦，"
        "原「纯螺旋涡旋几何」宣称被替换。"
        "注：宽松档 SURVIVE=%d > 0 表明该宣称**逻辑上并非不可能**（若真能从涡旋几何"
        "给出 f̄≈%.1f 且不借 QCD 则成立）；本卷判的是**靶未达成**——"
        "C3 已实测该 f̄ 在靶理论中**无任何来源**（102.3 关键词 0 命中）。"
        % (", ".join(MS_KEYS), p_strict["EMPTY"], p_strict["SUICIDE"], p_strict["SURVIVE"],
           p_loose["EMPTY"], p_loose["SUICIDE"], p_loose["SURVIVE"],
           p_loose["SURVIVE"], ig["fbar_mue"]),
        "★分层铁律：本卷条目**不可与 r142–r251 相加**，尤其不可与 r250（RG 层）、"
        "r248（单方程全域力层）相加。本卷为**质量谱层**首卷。")

    # ============================================================
    # 控制组
    # ============================================================
    ctl("C01", "反解现算：𝒦=Ω_exp/3−1 与靶的 611.05 一致",
        abs(rf[0]["K"] - 611.05) < 0.01,
        "本卷 %.5f vs 靶 611.05（残差 %s）" % (rf[0]["K"], fmt_rel(rel(rf[0]["K"], 611.05))))
    ctl("C02", "回代闭合：3(1+𝒦) 复原 Ω_exp（残差 <1e-12）",
        rf[0]["resid"] < 1e-12, "残差 %s" % fmt_rel(rf[0]["resid"]))
    ctl("C03", "★正对照（零判别力）：5 个替代 Ω 全部能解出实数 𝒦 并完美回代",
        all(r["resid"] < 1e-12 for r in rf[1:]) and len(rf) == 6,
        "%s" % "；".join("Ω=%.4g→𝒦=%.4f" % (r["omega"], r["K"]) for r in rf[1:]))
    ctl("C04", "★判别力存在性（承 r218）：f=1 时 Ω=%.4f 与实验差 %.2f 倍 ⇒ 式子可证伪"
        % (3.0 * (1.0 + ig["ln_mue"]), disc(3.0 * (1.0 + ig["ln_mue"]), OMEGA_EXP)),
        disc(3.0 * (1.0 + ig["ln_mue"]), OMEGA_EXP) > 10.0,
        "差 %.2f 倍（要求 >10）" % disc(3.0 * (1.0 + ig["ln_mue"]), OMEGA_EXP))
    ctl("C05", "对数跨度：ln(Λ_QCD/μ_e)=%.6f 个 e-fold（量级 sanity：4–8）" % ig["ln_mue"],
        4.0 < ig["ln_mue"] < 8.0, "%.6f（200 MeV / %.8f MeV）" % (ig["ln_mue"], M_E_MEV))
    ctl("C06", "★被积函数缺口：需 f̄=%.4f，靶最大耦合 %.4f ⇒ 缺口 >50 倍"
        % (ig["fbar_mue"], ig["max_target_coupling"]),
        ig["gap_vs_target"] > 50.0, "缺口 %.2f 倍" % ig["gap_vs_target"])
    ctl("C07", "★读法 B 的符号：按「电弱标度→Λ_QCD」需 f̄ 为负（%.2f）" % ig["fbar_ew"],
        ig["fbar_ew"] < 0.0, "f̄=%.4f（ln=%.4f）" % (ig["fbar_ew"], ig["ln_ew"]))
    ctl("C08", "三种读法给出三个互不相同的所需 f̄（靶未指定下限数值）",
        len({round(ig["fbar_mue"], 4), round(ig["fbar_ew"], 4),
             round(ig["fbar_ew_rev"], 4)}) == 3,
        "%.4f / %.4f / %.4f" % (ig["fbar_mue"], ig["fbar_ew"], ig["fbar_ew_rev"]))
    ctl("C09", "五个自然候选 f 全部 miss（最接近仍差 >1.05 倍）",
        fc["all_miss"], "最接近 %.4f 倍：%s"
        % (fc["best_disc"], "；".join("%s→%.2f×" % (r["name"], r["disc"]) for r in fc["rows"])))
    ctl("C10", "★机读一致性：boxed 主结果既存在含数值版本，也存在不含数值版本",
        len(BOXED_MPME_WITH_NUM) > 0 and len(BOXED_MPME_NO_NUM) > 0,
        "含数值 %d 处（行 %s）；不含 %d 处（行 %s）"
        % (len(BOXED_MPME_WITH_NUM), BOXED_MPME_WITH_NUM[:6],
           len(BOXED_MPME_NO_NUM), BOXED_MPME_NO_NUM[:6]))
    ctl("C11", "通道线性相关：ω²/c²−(κ²+τ²) 在 3 组取值下残差严格 0",
        ch["max_resid"] == 0.0, "最大残差 %s（3 组）" % fmt_rel(ch["max_resid"]))
    ctl("C12", "通道计数：靶列出 %d 个，独立 %d 个 ⇒ 不一致"
        % (ch["n_listed"], ch["n_independent"]),
        ch["n_listed"] != ch["n_independent"], "%d vs %d" % (ch["n_listed"], ch["n_independent"]))
    ctl("C13", "★中子恒等式：Fraction 精确残差分子为 0（非浮点近似）",
        nt["resid_is_zero"], "残差 = %d/%d" % (nt["resid_exact_num"], nt["resid_exact_den"]))
    ctl("C14", "中子恒等式第二形式：(𝒦_n−𝒦_p)/𝒦_p 与 (m_n−m_p)/(m_p−3m_e) 一致",
        nt["ratio_resid"] < 1e-12,
        "%.9e vs %.9e（残差 %s）" % (nt["ratio_lhs"], nt["ratio_rhs"], fmt_rel(nt["ratio_resid"])))
    ctl("C15", "靶的中子比值 1838.68 与 CODATA 直算一致（说明它就是实验值）",
        nt["omega_n_resid"] < 0.01,
        "直算 %.8f vs 靶 1838.68（残差 %s）" % (nt["omega_n_calc"], fmt_rel(nt["omega_n_resid"])))
    ctl("C16", "机读缺口：102.3 与 85.8/85.9 在语料中命中数均为 0",
        cs["102.36 或 102.35"] == 0 and cs["85.87 或 85.9"] == 0,
        "102.3=%d；85.8/85.9=%d" % (cs["102.36 或 102.35"], cs["85.87 或 85.9"]))
    ctl("C17", "机读：f 的显式定义式（f(α_s,…)=…）命中 0 处",
        cs["f 的显式定义式"] == 0, "命中 %d 处" % cs["f 的显式定义式"])
    ctl("C18", "机读：靶未给出 μ_e 的数值（0.511 命中 0 处）",
        cs["μ_e 的数值（0.511）"] == 0, "命中 %d 处" % cs["μ_e 的数值（0.511）"])
    _NCOMBO = 2 ** len(MS_KEYS)
    ctl("C19", "定价守恒：两档 EMPTY+SUICIDE+SURVIVE == %d" % _NCOMBO,
        (p_strict["EMPTY"] + p_strict["SUICIDE"] + p_strict["SURVIVE"] == _NCOMBO)
        and (p_loose["EMPTY"] + p_loose["SUICIDE"] + p_loose["SURVIVE"] == _NCOMBO),
        "严格 %d+%d+%d=%d；宽松 %d+%d+%d=%d"
        % (p_strict["EMPTY"], p_strict["SUICIDE"], p_strict["SURVIVE"], _NCOMBO,
           p_loose["EMPTY"], p_loose["SUICIDE"], p_loose["SURVIVE"], _NCOMBO))
    ctl("C20", "定价判别力：宽松档 SURVIVE > 0（枚举器非退化）",
        p_loose["SURVIVE"] > 0, "严格 %d / 宽松 %d" % (p_strict["SURVIVE"], p_loose["SURVIVE"]))
    ctl("C21", "靶 3 份可读且长度充分",
        all(len(TARGET_TEXT.get(p, "")) > 200 for p in TARGETS),
        "长度 %s" % ", ".join(str(len(TARGET_TEXT.get(p, ""))) for p in TARGETS))
    ctl("C22", "靶 3 份互不相同（防同一文件被加载 3 次致命中虚增）",
        len({SHA_AT_IMPORT[p] for p in TARGETS if SHA_AT_IMPORT[p]}) == len(TARGETS),
        "互异 hash %d/%d" % (len({SHA_AT_IMPORT[p] for p in TARGETS if SHA_AT_IMPORT[p]}),
                             len(TARGETS)))
    ctl("C23", "★污染已修复：去污染后 \\(\\boldsymbol 残留 < 全长的 0.5%%",
        ALL.count("\\(\\boldsymbol") < 0.005 * max(1, len(ALL)),
        "残留 %d / 全长 %d（%.4f%%）" % (ALL.count("\\(\\boldsymbol"), len(ALL),
                                       100.0 * ALL.count("\\(\\boldsymbol") / max(1, len(ALL))))
    ctl("C24", "★自审器本卷零写死（运行时真机读，含 IfExp 形态）",
        len(self_bad) == 0, "本卷检出 %d 处：%s" % (len(self_bad), self_msg))
    ctl("C25", "★自审器正对照（承 r247）：在他人卷 r244 源码上命中 ≥1 处（证明有分辨力）",
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
    grd("G4", "★承重①：靶文本内出现「反推」且 𝒦 与 Ω_exp/3−1 一致",
        len(L_REVERSE) > 0 and len(L_REVERSE_NUM) > 0 and abs(rf[0]["K"] - 611.05) < 0.01,
        "「反推」行 %s；1836.15/3 行 %s；𝒦=%.5f"
        % (L_REVERSE[:4], L_REVERSE_NUM[:4], rf[0]["K"]))
    grd("G5", "★承重②：boxed 主结果两处不一致已被机读（含/不含数值均 >0）",
        len(BOXED_MPME_WITH_NUM) > 0 and len(BOXED_MPME_NO_NUM) > 0,
        "含 %d / 不含 %d" % (len(BOXED_MPME_WITH_NUM), len(BOXED_MPME_NO_NUM)))
    grd("G6", "★承重③：通道线性相关残差严格 0 且 3≠2 已机读",
        ch["max_resid"] == 0.0 and len(L_CHANNELS) > 0,
        "残差 %s；通道行 %s" % (fmt_rel(ch["max_resid"]), L_CHANNELS[:4]))
    grd("G7", "★承重④：中子恒等式 Fraction 残差严格 0",
        nt["resid_is_zero"], "残差分子 %d" % nt["resid_exact_num"])
    grd("G8", "靶 3 份只读（结束态 hash == 导入期基线）",
        all(sha256_of(p) == SHA_AT_IMPORT[p] for p in TARGETS),
        "结束态 %s" % ", ".join((sha256_of(p) or "MISSING")[:12] for p in TARGETS))
    _ok9, _msg9 = scan_untouched(225, 252)
    grd("G9", "未触碰 r225–r251 产物（mtime 全部早于本轮启动）", _ok9, _msg9)
    _ok10, _msg10 = check_distribution()
    grd("G10", "条目分布断言（真机读，非预估）", _ok10, _msg10)
    grd("G11", "★判别力先测后指控：B3 实测差 %.2f 倍 >10 ⇒ 判「未行使」而非「零判别力」"
        % disc(3.0 * (1.0 + ig["ln_mue"]), OMEGA_EXP),
        disc(3.0 * (1.0 + ig["ln_mue"]), OMEGA_EXP) > 10.0,
        "差 %.2f 倍" % disc(3.0 * (1.0 + ig["ln_mue"]), OMEGA_EXP))
    grd("G12", "★口径自守：C3/C4 全程用靶给的 Λ_QCD=200 MeV 与靶口径 α_*，另列标准对照",
        ig["gap_vs_target"] > 50.0,
        "靶口径下缺口 %.2f 倍（α_*=%.4f、α_s=%.1f）" % (ig["gap_vs_target"], A_STAR, ALPHA_S_QCD))
    grd("G13", "★上游污染已修复（防「靶公式缺失」误判）",
        ALL.count("\\(\\boldsymbol") < 0.005 * max(1, len(ALL))
        and len(BOXED_MPME) > 0,
        "残留 %d；boxed 主结果定位成功 %d 处" % (ALL.count("\\(\\boldsymbol"), len(BOXED_MPME)))
    grd("G14", "★自审器零写死 + 正对照有分辨力（本卷 0 / 他人卷 ≥1）",
        len(self_bad) == 0 and len(oth_bad) >= 1,
        "本卷 %d；r244 %d" % (len(self_bad), len(oth_bad)))
    _ok15, _msg15 = check_write_side()
    grd("G15", "未修改 verify.py / 未跑 refresh_catalog", _ok15, _msg15)

    return {"entries": ENTRIES, "controls": CONTROLS, "guards": GUARDS, "evidence": EVIDENCE}


# ============================================================
# 8. 渲染
# ============================================================
def render_report(res):
    ev = res["evidence"]
    ig, fc, rf, nt, cs = ev["ig"], ev["fc"], ev["rf"], ev["nt"], ev["cs"]
    L = []
    A = L.append
    A("=" * 78)
    A("TUFT-%s · 质量谱层（★ 新层首卷：m_p/m_e 与 m_n/m_e）" % RID.upper())
    A("=" * 78)
    A("生成时间 %s" % START_ISO)
    A("")
    A("【靶（只读 3 份）】")
    for p in TARGETS:
        A("  - %s  sha256 %s" % (os.path.basename(p), (SHA_AT_IMPORT.get(p) or "MISSING")[:16]))
    A("")
    A("-" * 78)
    A("一、★★ 反解拟合：靶逐字写「反推」")
    A("-" * 78)
    A("  来料 line 4156-4159：实验比值 Ω_exp≈1836.15 → 反推：1+𝒦=1836.15/3=612.05 ⇒ 𝒦≈611.05")
    A("  本卷复算 𝒦 = %.8f（回代 Ω=%.8f，残差 %s）" % (rf[0]["K"], rf[0]["back"], fmt_rel(rf[0]["resid"])))
    A("")
    A("  正对照（把 Ω_exp 换掉，流程照样「成功」）：")
    for r in rf[1:]:
        A("    Ω=%-12.6g  ⇒  𝒦=%-14.6f  回代残差 %s" % (r["omega"], r["K"], fmt_rel(r["resid"])))
    A("  ⇒ 1 未知数 1 已知数，不排除任何 Ω 值 ⇒ 判别力 0")
    A("")
    A("-" * 78)
    A("二、★★ 主结果未求值：需要 f̄=%.4f（靶给的耦合最大才 %.4f）" % (ig["fbar_mue"], ig["max_target_coupling"]))
    A("-" * 78)
    A("  μ_e = m_e c² = %.8f MeV；Λ_QCD ≈ %g MeV（靶给）" % (M_E_MEV, LAMBDA_QCD_MEV))
    A("  对数跨度 ln(Λ_QCD/μ_e) = %.6f 个 e-fold" % ig["ln_mue"])
    A("  要攒出 𝒦=%.5f ⇒ 被积函数平均值 f̄ = %.4f" % (ig["K_p"], ig["fbar_mue"]))
    A("  靶给的全部耦合：α_s≈%.1f、α_*=%.6f、α_obs=%.4e ⇒ 最大 %.4f" %
      (ALPHA_S_QCD, A_STAR, ALPHA_OBS, ig["max_target_coupling"]))
    A("  ⇒ 缺口 **%.2f 倍**" % ig["gap_vs_target"])
    A("")
    A("  五个自然候选 f（常数近似）：")
    A("  %-24s %-12s %-12s %-12s" % ("候选", "f", "Ω_model", "与 1836.15 差"))
    A("  " + "-" * 62)
    for r in fc["rows"]:
        A("  %-24s %-12.6g %-12.4f %-12.3f×" % (r["name"], r["f"], r["omega"], r["disc"]))
    A("  ⇒ 无一命中，最接近也差 %.3f 倍" % fc["best_disc"])
    A("")
    A("  下限二难（靶一处说电子标度、一处说电弱标度）：")
    A("    读法 A（μ_e→Λ_QCD）      ln=%+.6f ⇒ 需 f̄=%+.4f" % (ig["ln_mue"], ig["fbar_mue"]))
    A("    读法 B（电弱标度→Λ_QCD） ln=%+.6f ⇒ 需 f̄=%+.4f（负值！）" % (ig["ln_ew"], ig["fbar_ew"]))
    A("    读法 C（反向 Λ_QCD→EW）  ln=%+.6f ⇒ 需 f̄=%+.4f" % (ig["ln_ew_rev"], ig["fbar_ew_rev"]))
    A("")
    A("-" * 78)
    A("三、★★ 权重 3：三个通道线性相关（ω²/c² = κ²+τ²）")
    A("-" * 78)
    A("  %-10s %-10s %-12s %-12s %-12s %s" % ("κ²", "τ²", "c1=κ²", "c2=τ²", "c3=ω²/c²", "c3-(c1+c2)"))
    for r in ev["ch"]["rows"]:
        A("  %-10g %-10g %-12g %-12g %-12g %s" % (r["k2"], r["t2"], r["c1"], r["c2"], r["c3"], fmt_rel(r["resid"])))
    A("  ⇒ 靶列出 %d 个通道，独立只有 %d 个 ⇒ 权重 3 与自己的分解不相容"
      % (ev["ch"]["n_listed"], ev["ch"]["n_independent"]))
    A("")
    A("-" * 78)
    A("四、★★ 中子质量换名：Fraction 残差严格 0")
    A("-" * 78)
    A("  𝒦_p = %.8f；𝒦_n = %.8f；𝒦_n−𝒦_p = %.8f" % (nt["K_p"], nt["K_n"], nt["K_diff"]))
    A("  (m_n−m_p)/(3m_e)      = %.8f" % nt["rhs"])
    A("  Fraction 残差          = %d/%d（严格 0）" % (nt["resid_exact_num"], nt["resid_exact_den"]))
    A("  (𝒦_n−𝒦_p)/𝒦_p        = %.9e" % nt["ratio_lhs"])
    A("  (m_n−m_p)/(m_p−3m_e)  = %.9e" % nt["ratio_rhs"])
    A("  ⇒ 恒等式，任何「SU(2) 弱耦合扰动」的诠释都得到同一个数 ⇒ 零判别力")
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
    ig, fc, rf, nt = ev["ig"], ev["fc"], ev["rf"], ev["nt"]
    kv = (
        ("m_p/m_e（CODATA 直算）", "%.8f" % OMEGA_EXP),
        ("靶 boxed 值", "≈1836.15"),
        ("𝒦（由 Ω_exp 反推）", "%.8f" % rf[0]["K"]),
        ("ln(Λ_QCD/μ_e)", "%.6f 个 e-fold" % ig["ln_mue"]),
        ("所需被积函数 f̄", "%.4f" % ig["fbar_mue"]),
        ("靶给的最大耦合", "%.4f（α_s≈1）" % ig["max_target_coupling"]),
        ("缺口", "%.2f 倍" % ig["gap_vs_target"]),
        ("电弱读法所需 f̄", "%.4f（负值）" % ig["fbar_ew"]),
        ("f=1 时 Ω_model", "%.4f（差 %.2f 倍）" %
         (3.0 * (1.0 + ig["ln_mue"]), disc(3.0 * (1.0 + ig["ln_mue"]), OMEGA_EXP))),
        ("通道：列出 / 独立", "%d / %d" % (ev["ch"]["n_listed"], ev["ch"]["n_independent"])),
        ("𝒦_n−𝒦_p Fraction 残差", "%d/%d（严格 0）" % (nt["resid_exact_num"], nt["resid_exact_den"])),
        ("m_n/m_e 直算 vs 靶", "%.8f vs 1838.68" % nt["omega_n_calc"]),
    )
    rows = "\n".join("<tr><td>%s</td><td>%s</td></tr>" % (k, v) for k, v in kv)
    fc_rows = "\n".join(
        "<tr><td>%s</td><td>%.6g</td><td>%.4f</td><td>%.3f×</td></tr>"
        % (r["name"], r["f"], r["omega"], r["disc"]) for r in fc["rows"])
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
<title>TUFT-%(rid)s 质量谱层</title><style>
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
<h1>TUFT-%(rid)s · 质量谱层（m_p/m_e 与 m_n/m_e）</h1>
<div class="meta">生成 %(ts)s ｜ 控制组 %(nc_ok)d/%(nc)d ｜ 守卫 %(ng_ok)d/%(ng)d ｜ 靶未改动 %(unch)s</div>
<div class="verdict"><b>判词</b><br>%(header)s</div>
<h2>核心数值</h2><div class="kv"><table>%(rows)s</table></div>
<h2>五个自然候选被积函数 f</h2>
<table><tr><th>候选</th><th>f</th><th>Ω_model</th><th>与 1836.15 差</th></tr>%(fc_rows)s</table>
<h2>条目</h2>%(ents)s
<h2>控制组</h2><ul>%(ctls)s</ul>
<h2>守卫</h2><ul>%(grds)s</ul>
</body></html>""" % dict(rid=RID.upper(), ts=START_ISO, nc_ok=nctl_ok, nc=nctl,
                          ng_ok=ngrd_ok, ng=ngrd, unch=payload["targets_unchanged"],
                          header=header, rows=rows, fc_rows=fc_rows,
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
    ig, fc, rf, nt = ev["ig"], ev["fc"], ev["rf"], ev["nt"]

    header = (
        "靶声称从「三重螺旋涡旋拓扑」推出 m_p/m_e≈1836.15，但来料 line 4156–4159 "
        "**逐字写着「反推」**：𝒦=Ω_exp/3−1=%.2f——1 个未知数对 1 个已知数，"
        "对任意 Ω>3 恒可解（本卷把 Ω 换成 100/1000/1e6/π 同样全部「成功」）⇒ 判别力 0。"
        "更根本的是 boxed 主结果**未求值**：推导章（line 4179）的 boxed 式只有积分、没有数值，"
        "而体系汇总表（line 4226）同一式子却写了 ≈1836.15；靶 line 4183 自认"
        "「还没有把 f(α_s,α) 解析封闭形式求出来」。把它量化：积分跨度仅 "
        "ln(Λ_QCD/μ_e)=%.4f 个 e-fold，要攒出 𝒦=%.2f 需被积函数平均 **f̄=%.2f**，"
        "而靶自己给的全部耦合（α_s≈1、α_*=%.3f、α_obs=%.1e）最大才 %.2f ⇒ **缺口 %.0f 倍**；"
        "五个自然候选 f 全部对不上（最接近差 %.2f 倍）。"
        "另两条独立证据：(1) 权重 3 的通道**线性相关**——靶明列 κ²、τ²、ω²/c² 且 "
        "ω²/c²=κ²+τ² ⇒ 独立通道数是 2 不是 3，二难两支都死（要么权重无来源，"
        "要么与本源公理冲突）；(2) 中子质量是**换名**——𝒦_n−𝒦_p ≡ (m_n−m_p)/(3m_e) "
        "的 Fraction 残差**严格 0**，靶却赋予「SU(2) 弱耦合微小扰动」的诠释，"
        "而该恒等式对任何诠释都成立 ⇒ 零判别力。"
        % (rf[0]["K"], ig["ln_mue"], ig["K_p"], ig["fbar_mue"], A_STAR, ALPHA_OBS,
           ig["max_target_coupling"], ig["gap_vs_target"], fc["best_disc"]))

    payload = {
        "id": "TUFT-" + RID,
        "title": "质量谱层：m_p/m_e 反解拟合、未定值积分、权重 3 通道线性相关与中子质量换名",
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
        "reverse_fit": rf,
        "integral_layer": ig,
        "f_candidates": fc,
        "channel_layer": ev["ch"],
        "neutron_layer": {k: (str(v) if k in ("resid_exact_num", "resid_exact_den") else v)
                          for k, v in nt.items()},
        "caliber_scan": ev["cs"],
        "boxed_locs": {"all": BOXED_MPME, "with_num": BOXED_MPME_WITH_NUM,
                       "no_num": BOXED_MPME_NO_NUM},
        "line_locs": {"反推": L_REVERSE, "611": L_K611, "Ω=3": L_OMEGA3,
                      "三通道": L_CHANNELS, "权重函数": L_FDEF, "未求出f": L_NOF,
                      "格点仿真": L_LATTICE, "积分得611": L_GOT611, "权重候选": L_CAND,
                      "诚实1": L_HONEST1, "诚实2": L_HONEST2, "m_n/m_e": L_MUN,
                      "SU2": L_SU2, "电弱标度": L_EWSCALE, "电子标度": L_MUSCALE},
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
    md.append("\n## 一、承重：反解拟合 + 未求值积分\n")
    md.append("\n| 量 | 值 |\n|---|---|\n")
    md.append("| m_p/m_e（CODATA 直算） | %.8f |\n" % OMEGA_EXP)
    md.append("| 𝒦（由 Ω_exp 反推） | %.8f（靶写 611.05） |\n" % rf[0]["K"])
    md.append("| ln(Λ_QCD/μ_e) | %.6f 个 e-fold |\n" % ig["ln_mue"])
    md.append("| 所需被积函数 f̄ | %.4f |\n" % ig["fbar_mue"])
    md.append("| 靶给的最大耦合 | %.4f |\n" % ig["max_target_coupling"])
    md.append("| 缺口 | %.2f 倍 |\n" % ig["gap_vs_target"])
    md.append("| 电弱读法所需 f̄ | %.4f（负值） |\n" % ig["fbar_ew"])
    md.append("\n## 二、条目\n")
    for e in res["entries"]:
        md.append("\n### [%s] %s · %s\n" % (e["state"], e["code"], e["title"]))
        md.append("\n- 证据：%s\n" % e["evidence"])
        if e["note"]:
            md.append("- 备注：%s\n" % e["note"])
    md.append("\n## 三、红线\n")
    md.append("\n- 靶 3 份只读：%s\n" % payload["targets_unchanged"])
    md.append("- **r225–r251 产物未改动**（G9 真机读）。\n")
    md.append("- 本卷为**质量谱层**，条目**不可与 r142–r251 相加**；"
              "F1 为交联指针（INFO），不计分。\n")
    md.append("- 未跑 refresh_catalog.py，未改 verify.py，未做 git。\n")
    with io.open(md_path, "w", encoding="utf-8") as f:
        f.write("".join(md))

    vd = ["# 判定册 · TUFT-%s（质量谱层）\n" % RID.upper(),
          "\n## 判词\n\n%s\n" % header,
          "\n## 判决分组\n",
          "\n| 组 | 内容 | 结论 |\n|---|---|---|\n",
          "| A | 对靶有利 6 条：量纲层自洽、质量公式 [M] 正确、靶三次主动自我披露"
          "（不能由几何恒等式得到 / 权重自称候选 / 承认 f 未求出）、定性图像与格点 QCD 兼容 | PASS |\n",
          "| B | ★★反解拟合 3 条：逐字「反推」、正对照 5 个替代 Ω 全成功、"
          "判别力存在但未行使（f=1 ⇒ 差 %.0f 倍） | **FAIL** |\n"
          % disc(3.0 * (1.0 + ig["ln_mue"]), OMEGA_EXP),
          "| C | ★★未求值 5 条：boxed 两处不一致、循环（先说得到 611 后说 f 未求出）、"
          "需 f̄=%.1f（缺口 %.0f 倍）、5 个候选全 miss、下限二难 | **FAIL** |\n"
          % (ig["fbar_mue"], ig["gap_vs_target"]),
          "| D | ★★权重 3 的 3 条：通道线性相关（独立数 2≠3）、二难两支都死、"
          "与靶自认「质子质量≠三夸克之和」冲突 | **FAIL** |\n",
          "| E | ★中子质量换名 2 条：𝒦_n−𝒦_p 恒等式 Fraction 残差严格 0、"
          "m_n/m_e 是实验值换名 | FAIL |\n",
          "| F | 交联指针（r250 的 α_* / α_s） | INFO（不计分） |\n",
          "| G | 修复定价（双档） | FAIL |\n"]
    vd.append("\n## ★ 性质界定\n")
    vd.append("\n1. **不是外部证伪，是靶文本内部的不一致**：C1 只比较靶自己两处 boxed 式"
              "（line 4179 无数值 vs line 4226 有数值）；C2 只比较靶自己两句话"
              "（line 4168「得到 𝒦≈611」vs line 4183「还没求出 f」）。\n")
    vd.append("2. **靶是诚实的**：A3–A5 三条 PASS 明确承认靶**主动**声明了该式不是第一性精确解、"
              "权重只是候选、f 尚未求出。本卷判的不是「靶不诚实」，而是"
              "「即便按靶自己的降级声明，这个式子仍然产生不了任何数值」。\n")
    vd.append("3. **判别力先测后指控（承 r218）**：B3 实测 f=1 时 Ω=%.2f 与实验差 %.0f 倍 "
              "⇒ 该式**有判别力**。故本卷判「未行使」，**不**判「零判别力」。\n"
              % (3.0 * (1.0 + ig["ln_mue"]), disc(3.0 * (1.0 + ig["ln_mue"]), OMEGA_EXP)))
    vd.append("4. **量化缺口而非定性指责**：C3 给出「需 f̄=%.2f，靶最大耦合 %.2f，"
              "缺口 %.0f 倍」；C4 给出 5 个自然候选的具体偏差（%.2f×–%.0f×）。"
              "这是可复算的，不是印象。\n"
              % (ig["fbar_mue"], ig["max_target_coupling"], ig["gap_vs_target"],
                 fc["best_disc"], max(r["disc"] for r in fc["rows"])))
    vd.append("5. **口径自守**：C3/C4 全程使用**靶给的** Λ_QCD=200 MeV 与靶口径 α_*=√3/2；"
              "F1 明记 α_* 自身的问题归 **r250**，本卷不重复计分。\n")
    vd.append("6. **定义恒等式刀（承 r204/r247）**：E1 用 Fraction 精确有理数证明 "
              "𝒦_n−𝒦_p ≡ (m_n−m_p)/(3m_e)（残差分子 0），故靶的「SU(2) 弱耦合扰动」诠释"
              "是**事后贴标签**——换成任何诠释都得到同一个数。\n")
    vd.append("\n## 治理\n")
    vd.append("\n- 控制组 %d/%d；守卫 %d/%d\n"
              % (n_ctl_ok, len(res["controls"]), n_grd_ok, len(res["guards"])))
    vd.append("- 靶 3 份只读：%s；r225–r251 产物未改动（mtime 真机读）\n"
              % payload["targets_unchanged"])
    vd.append("- ⚠ **撞号记录（第 6 次）**：起草期间 r251（下游物理应用层·垂直原理 FRW 与"
              "黑洞无奇点，08:09:31）被并行会话占用 ⇒ 本卷整体迁至 **r252**。\n")
    vd.append("- 本卷条目不可与 r142–r251 相加。\n")
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
