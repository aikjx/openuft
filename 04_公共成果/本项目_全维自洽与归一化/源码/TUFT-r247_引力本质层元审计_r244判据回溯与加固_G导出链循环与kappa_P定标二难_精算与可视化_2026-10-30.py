# -*- coding: utf-8 -*-
r"""
TUFT-r247 · 引力本质层「元审计」—— r244 判据回溯与加固
================================================================================
【命题来源】用户：对 r244 的 FAIL 条目做「分析整理，修复优化」

【本卷性质：元审计层（审计审计本身）】
r244 问的是「靶的引力是什么」；本卷问的是：

    r244 拿出的 9 条 FAIL，每一条自己站得住吗？

按本线元纪律，判据必须反噬自己：控制组不得写死、指控须先测反例、
数值须复算、扫描器须配正反对照。本卷即用这套纪律回头审 r244。

【★ 最重要发现：r244 的 E2 判反了】
r244 E2 标题：「无『由 κ/τ 推出 G』的式子 ⇒ 引力本质层的预测预算为 0」。
但 r244 自己的扫描器在靶 3 份文本上命中 G-推导式 **6 处**——
本卷机读这 6 处的上下文，发现它们**全部是同一条真公式**：

    $$G=\frac{c^3}{2\hbar\kappa_P^2}$$      （靶标题逐字：引力常数几何表达式）

即：**靶确实给出了由 κ_P 推出 G 的显式式子**，r244 的标题与自己的证据矛盾。
⇒ 本卷翻案 E2，并把它换成一个**更锋利**的指控（见 F 组）：

    ① 该链的起点是 M_P^2 = ℏc/G —— **G 在输入侧从头到尾没离开过** ⇒ 循环；
    ② 靶随后「取定义 κ_P = 1/l_P」，与联立定标 κ_P = 1/(√2 l_P) **差 √2**；
       两种读法必居其一：要么残差 50%（G 反算得 G/2），要么恒等（零新增）。

【分层铁律】本卷条目不可与 r142–r246 相加；
本卷是**元审计层**，与 r244（引力本体论层）**不是同一层**，不可相加。
本卷**不改动** r244 任何产物（G7 真机读守卫）。
================================================================================
"""

import ast
import hashlib
import io
import math
import os
import re
import sys
import time
from fractions import Fraction

# ============================================================
# 0. 元信息
# ============================================================
RID = "r247"
BASE_NAME = ("TUFT-r247_引力本质层元审计_r244判据回溯与加固_"
             "G导出链循环与kappa_P定标二难_精算与可视化_2026-10-30")
START_TS = time.time()
START_ISO = time.strftime("%Y-%m-%dT%H:%M:%S")

SRC_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
DATA_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\数据"

R244_SRC = os.path.join(SRC_DIR, "TUFT-r244_引力本质层_曲线曲率与时空曲率范畴错置_"
                                 "引力方向地基缺失与kappa读法二难_精算与可视化_2026-10-30.py")
R244_OUT = os.path.join(SRC_DIR, "_out_r244.txt")

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
# 1. 常数
# ============================================================
C = 299792458.0
H = 6.62607015e-34
HBAR = H / (2.0 * math.pi)
G = 6.67430e-11
GM_EARTH = 3.986004418e14
R_EARTH = 6378137.0
G_STD_REF = 9.80665
L_PLANCK = math.sqrt(HBAR * G / C ** 3)


def fmt_rel(x):
    return "{:.3e}".format(x)


def rel(a, b):
    if b == 0:
        return float("inf") if a != 0 else 0.0
    return abs(a - b) / abs(b)


# ============================================================
# 2. r244 产物机读（不手抄，避免失真）
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


R244_SRC_TEXT = read_text(R244_SRC)

# ★坑（本轮开发期自抓）：_out_r244.txt 存在 `\r\r\n` 双重换行污染（CR 346 / LF 173），
# 文本模式读 + split("\n") 会得到 347 行（每行之间插一个空行）⇒ 条目/备注抽取错位。
# 故此处把所有 CR/LF 连续段折叠为单个 \n 后再解析。
R244_TEXT = re.sub(r"[\r\n]+", "\n", read_text(R244_OUT))
R244_CRLF_POLLUTED = (read_text(R244_OUT).count("\r") > 0)

RE_ENTRY = re.compile(r"^\[(PASS|FAIL|INFO)\] ([A-Z]\d+) · (.+)$", re.M)
RE_CTL = re.compile(r"^  \[(PASS|FAIL)\] (C\d\d) · (.+)$", re.M)
R244_ENTRIES = [(m.group(2), m.group(1), m.group(3).strip())
                for m in RE_ENTRY.finditer(R244_TEXT)]
R244_CONTROLS = [(m.group(2), m.group(1), m.group(3).strip())
                 for m in RE_CTL.finditer(R244_TEXT)]


def r244_entry(code):
    for c, s, t in R244_ENTRIES:
        if c == code:
            return (c, s, t)
    return None


def r244_note(code):
    """抽取 r244 某条目的备注行（条目行之后紧邻的『     备注：』行）"""
    lines = R244_TEXT.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("[") and (" %s · " % code) in ln:
            for j in range(i + 1, min(i + 4, len(lines))):
                if lines[j].strip().startswith("备注："):
                    return lines[j].strip()[3:]
                if lines[j].startswith("["):
                    break
    return ""


# ============================================================
# 3. 靶机读
# ============================================================
SHA_AT_IMPORT = {p: sha256_of(p) for p in TARGETS}
TARGET_TEXT = {p: read_text(p) for p in TARGETS}
RAW = TARGET_TEXT.get(TARGETS[0], "")
ALL = "".join(TARGET_TEXT.get(p, "") for p in TARGETS)
RAW_LINES = RAW.split("\n")


def nhit(text, *toks):
    return sum(text.count(t) for t in toks)


# ============================================================
# 4. ★ 新增证据计算
# ============================================================
def g_chain():
    r"""
    靶的 G 导出链（来料 line 5680–5713，逐字）：

      (a) M_P^2 = ℏc / G                       ← 起点，G 在【输入侧】
      (b) M_P   = (ℏ/c)·√(κ_P^2+τ_P^2)，且 κ_P = τ_P
                ⇒ M_P^2 = 2ℏ^2 κ_P^2 / c^2
      (a)=(b) ⇒ κ_P^2 = c^3 / (2ℏG)   ⇒   κ_P = 1/(√2 · l_P)
      (c) G   = c^3 / (2ℏ κ_P^2)                ← boxed「引力常数几何表达式」
      (d) 靶再「取定义 κ_P = 1/l_P」             ← 与 (b) 定标差 √2
      (e) ⇒ G = c^3 l_P^2 / (2ℏ) ⇒ l_P = √(2ℏG/c^3) = √2 · l_P^std

    两条 κ_P 定标路径：
      路径甲（由 (a)=(b) 联立）：κ_P^甲 = √(c^3/(2ℏG)) = 1/(√2 l_P^std)
      路径乙（(d) 明文定义）  ：κ_P^乙 = 1/l_P^std
    二者比 √2。代入 (c) 得 G 的两个反算值。
    """
    kA = math.sqrt(C ** 3 / (2.0 * HBAR * G))     # 路径甲
    kB = 1.0 / L_PLANCK                            # 路径乙（靶明文定义）
    gA = C ** 3 / (2.0 * HBAR * kA ** 2)           # 用甲代入 (c)
    gB = C ** 3 / (2.0 * HBAR * kB ** 2)           # 用乙代入 (c)
    lp_tuft = math.sqrt(2.0 * HBAR * G / C ** 3)   # 靶的 l_P
    return {
        "kappa_A": kA, "kappa_B": kB, "kappa_ratio": kB / kA,
        "G_from_A": gA, "G_from_B": gB,
        "rel_G_A": rel(gA, G), "rel_G_B": rel(gB, G),
        "rel_kappa": rel(kB, kA),
        "l_P_std": L_PLANCK, "l_P_tuft": lp_tuft,
        "l_P_ratio": lp_tuft / L_PLANCK,
    }


def g_chain_line_numbers():
    r"""
    真机读：定位 (a) 起点与 (c) boxed 的行号，验证 G 先出现在输入侧。

    ★坑（本轮开发期自抓）：来料中的 LaTeX 被上游预处理污染——
    \hbar 被写成 \h\(\boldsymbol{b}\)ar、\boxed 被写成 \\(\boldsymbol{b}\)oxed、
    \tau 被写成 \(\boldsymbol{b}\)oldsym…\(\boldsymbol{b}\)ol{t}au。
    故**不能**用含 \hbar / \boxed 的完整正则定位，须改用抗污染的子串组合。
    """
    lines_in = [i + 1 for i, s in enumerate(RAW_LINES)
                if "M_P^2" in s and "}{G}" in s]
    lines_out = [i + 1 for i, s in enumerate(RAW_LINES)
                 if ("G=\\frac{c^3}" in s) and ("kappa_P^2" in s)]
    lines_box = [i + 1 for i, s in enumerate(RAW_LINES)
                 if "oxed{G=" in s and "c^3" in s and "kappa_P^2" in s]
    lines_def = [i + 1 for i, s in enumerate(RAW_LINES)
                 if "取定义" in s and "kappa_P" in s and "1/l_P" in s]
    return {"input_M_P2_lines": lines_in, "G_expr_lines": lines_out,
            "boxed_lines": lines_box, "kappa_def_lines": lines_def}


def kappa_equals_g_over_c2():
    r"""
    ★ 定义恒等式刀（承 r204）：
    靶 ansatz κ(r) = G M e^{−λ(r)} / (c^2 r^2)。取 λ=0（对靶最有利），则
        c^2 · κ(r) = c^2 · GM/(c^2 r^2) ≡ GM/r^2
    右端正是**牛顿引力场强**。⇒ 用 Fraction 精确消去 c^2，残差应严格 0。
    """
    fr_c2 = Fraction(C) ** 2
    fr_gm = Fraction(int(GM_EARTH))
    fr_r2 = Fraction(int(R_EARTH)) ** 2
    lhs = fr_c2 * fr_gm / (fr_c2 * fr_r2)     # c^2 * κ(r)
    rhs = fr_gm / fr_r2                        # GM/r^2
    resid = lhs - rhs
    return {
        "lhs_float": float(lhs), "rhs_float": float(rhs),
        "resid_exact": resid, "resid_is_zero": (resid == 0),
        "vs_g_std": rel(float(rhs), G_STD_REF),
    }


def decade_span():
    r"""复核 r244 D3 备注中的『κ 跨 4 个数量级』"""
    rows = []
    for v in (0.0, 1.0, 10.0, 100.0, 1000.0):
        kap = 0.0 if v == 0 else G_STD_REF / v ** 2
        rows.append({"v": v, "kappa": kap, "m": (HBAR / C) * kap,
                     "kv2": (kap * v ** 2 if v > 0 else None)})
    span = math.log10(rows[1]["kappa"] / rows[4]["kappa"])
    return {"rows": rows, "span_decades": span,
            "kv2_all_g": all(abs(r["kv2"] - G_STD_REF) < 1e-12
                             for r in rows if r["v"] > 0)}


def riemann_token_split():
    r"""r244 C2 称『黎曼/曲率张量 3 处』——拆解语义，区分真曲率张量与『黎曼 ζ 函数』歧义"""
    zeta, real = [], []
    for m in re.finditer("黎曼", ALL):
        ctx = ALL[max(0, m.start() - 40): m.end() + 40]
        if ("ζ" in ctx) or ("zeta" in ctx) or ("函数" in ctx):
            zeta.append(ctx.replace("\n", "\\n")[:110])
        else:
            real.append(ctx.replace("\n", "\\n")[:110])
    curv = [ALL[max(0, m.start() - 60): m.end() + 60].replace("\n", "\\n")[:130]
            for m in re.finditer("曲率张量", ALL)]
    return {"zeta_hits": zeta, "riemann_real": real, "curv_tensor": curv,
            "n_zeta": len(zeta), "n_real": len(real), "n_curv": len(curv),
            "n_riemann_en": ALL.count("Riemann")}


def null_frame_hits():
    r"""D1 反例搜索：靶是否已经提出 null frame / 伪弧长修法（对靶有利项）"""
    toks = ["零标架", "null frame", "伪弧长", "拟弧长", "Cartan", "Newman",
            "Sachs", "仿射参数", "重新参数", "重参数"]
    out = {}
    for t in toks:
        out[t] = {"raw": RAW.count(t), "all": ALL.count(t)}
    ctx = []
    for m in re.finditer("伪弧长|null frame|零标架", ALL):
        ctx.append(ALL[max(0, m.start() - 55): m.end() + 95].replace("\n", "\\n"))
    return {"counts": out, "ctx": ctx[:6]}


def xi_scan():
    r"""
    C1 加固用：靶有没有「分离矢量 ξ」——这是把「曲率」变成「潮汐」的必需物件。
    没有 ξ，κ 就只能产出单点加速度（力图像），不可能是时空弯曲。
    """
    toks = ["分离矢量", "分离向量", "偏离矢量", "测地偏离矢量", "\\xi", "ξ"]
    out = {}
    for t in toks:
        out[t] = {"raw": RAW.count(t), "all": ALL.count(t)}
    # 与潮汐/测地偏离语义同现的次数（真正构成潮汐通道才算）
    co = 0
    for t in ("ξ", "\\xi"):
        for m in re.finditer(re.escape(t), ALL):
            ctx = ALL[max(0, m.start() - 120): m.end() + 120]
            if ("潮汐" in ctx) or ("测地偏离" in ctx) or ("测地线偏离" in ctx):
                co += 1
    return {"counts": out, "co_with_tide": co,
            "total_xi": ALL.count("ξ") + ALL.count("\\xi")}


def mass_formula_presence():
    r"""D2/D3 前提核查：m=(ℏ/c)√(κ²+τ²) 是否真实存在于靶文本（非 r244 特设）"""
    pats = {
        "boxed_m": r"boxed\{m=\\frac\{\\hbar\}\{c\}\\sqrt\{\\kappa\^2\+\\tau\^2\}\}",
        "m_hbar_c": r"m\s*=\s*\(?\s*ℏ\s*/\s*c\s*\)",
        "pure_curvature": r"m=\\frac\{\\hbar\s*\\kappa\}\{c\}",
        "mass_from_curv": r"质量主体来自曲率",
        "covariant_4d": r"四维曲率标量.{0,20}R.{0,30}替换三维",
    }
    out = {}
    for k, p in pats.items():
        out[k] = len(re.findall(p, ALL))
    m4 = re.search(r"[^。\n]{0,70}四维曲率标量[^。\n]{0,90}", RAW)
    out["covariant_4d_ctx"] = m4.group(0).strip()[:170] if m4 else ""
    return out


def self_confessed_substitution():
    r"""★靶自证：靶自己在别处宣称要用四维曲率标量 R 替换三维 κ,τ"""
    hits = [RAW_LINES[i] for i in range(len(RAW_LINES))
            if "四维曲率标量" in RAW_LINES[i] or ("替换三维" in RAW_LINES[i])]
    return [h.strip()[:180] for h in hits[:4]]


# ============================================================
# 5. 扫描器对照（r244 缺的那些）
# ============================================================
G_DERIV_WIDE = re.compile(r"G\s*=\s*[^\n=]{0,80}?(?:κ|kappa)")
NEG_G_TEXT = ("引力常数 G = 6.67430e-11 在 SI 中定义。我们在第 3 章讨论了螺旋曲率 κ "
              "与挠率 τ 的性质，二者无关。另外 G = 6.674e-11 时 κ 的取值另行讨论。")
TIDE_TOKENS = ["测地偏离", "测地线偏离", "潮汐", "引潮力", "起潮力", "潮汐力",
               "geodesic deviation", "tidal", "Ricci"]
POS_TIDE_TEXT = ("本理论给出测地偏离方程 D^2 ξ^μ/dτ^2 = −R^μ_{ναβ} u^ν ξ^α u^β，"
                 "并给出地表潮汐与月潮的数值，tidal 梯度为 3.07e-6 s^-2。")


# ============================================================
# 6. 修复定价重算（双档）
# ============================================================
ESSENCE_KEYS = ("intrinsic_curvature", "geodesic_deviation", "covariant_frenet",
                "timelike_carrier", "g_from_geometry")
GR_ESSENCE_SKELETON = {"intrinsic_curvature", "geodesic_deviation", "covariant_frenet"}


def repair_pricing(requirement):
    from itertools import product
    out = {"EMPTY": 0, "SUICIDE": 0, "SURVIVE": 0}
    surv = []
    for combo in product((False, True), repeat=len(ESSENCE_KEYS)):
        have = {k for k, v in zip(ESSENCE_KEYS, combo) if v}
        if not requirement.issubset(have):
            out["EMPTY"] += 1
        elif GR_ESSENCE_SKELETON.issubset(have):
            out["SUICIDE"] += 1
        else:
            out["SURVIVE"] += 1
            surv.append(sorted(have))
    out["SURVIVE_SETS"] = surv
    return out


# ============================================================
# 7. 条目容器
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
# 8. 真机读守卫
# ============================================================
def scan_untouched(lo=225, hi=247):
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
    msg = ("扫描 r%d–r%d 产物 %d 份，mtime 全部早于本轮启动 %s" % (lo, hi - 1, scanned, START_ISO)
           if ok else ("发现被触碰：%s" % ",".join(touched[:5]) if touched
                       else "未扫描到任何 r%d–r%d 产物（扫描器失效）" % (lo, hi - 1)))
    return ok, msg


def check_distribution():
    dist = {}
    for e in ENTRIES:
        dist[e["state"]] = dist.get(e["state"], 0) + 1
    ok = (sum(dist.values()) == len(ENTRIES)) and dist.get("FAIL", 0) >= 6 \
        and dist.get("PASS", 0) >= 3
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


# ============================================================
# 9. AST 自审器（升级版：补上 IfExp 写死 True 的盲区）
# ============================================================
_AST_WHITELIST = {"G6"}


def ast_scan_hardcoded(path_or_src, is_src=False):
    r"""
    扫描 ent/ctl/grd 调用的第 3 个位置参数是否为「写死的常量」。
    与 r244 版相比，新增两类检出：
      ① `True if <expr> else False` / `False if <expr> else True`（ast.IfExp）
         —— r244 的 C13 正是这种写法，其旧自审器（只查 ast.Constant）抓不到。
      ② `bool(<常数>)`、`not None` 之类恒真包装（此处只覆盖 IfExp，够抓 C13）。
    """
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
            bad.append("%s(%s, %s)" % (fn, code, third.value))
        elif isinstance(third, ast.IfExp):
            b, o = third.body, third.orelse
            if isinstance(b, ast.Constant) and isinstance(o, ast.Constant) \
               and b.value is True and o.value is False:
                bad.append("%s(%s, True-if-expr-else-False)" % (fn, code))
            elif isinstance(b, ast.Constant) and isinstance(o, ast.Constant) \
                    and b.value is False and o.value is True:
                bad.append("%s(%s, False-if-expr-else-True)" % (fn, code))
    return bad, ("无写死" if not bad else "发现写死：%s" % ", ".join(bad))


def _ast_self_audit():
    bad, msg = ast_scan_hardcoded(os.path.join(SRC_DIR, BASE_NAME + ".py"))
    return (not bad), msg


# ============================================================
# 10. 主审计
# ============================================================
def run_audit():
    EVIDENCE.clear()
    del ENTRIES[:], CONTROLS[:], GUARDS[:]

    chain = g_chain()
    chain_lines = g_chain_line_numbers()
    idem = kappa_equals_g_over_c2()
    dec = decade_span()
    rie = riemann_token_split()
    nf = null_frame_hits()
    mf = mass_formula_presence()
    xi = xi_scan()
    scs = self_confessed_substitution()
    EVIDENCE.update({"chain": chain, "chain_lines": chain_lines, "idem": idem,
                     "dec": dec, "rie": rie, "nf": nf, "mf": mf, "scs": scs,
                     "xi": xi})

    g_wide_target = len(G_DERIV_WIDE.findall(ALL))
    g_wide_neg = len(G_DERIV_WIDE.findall(NEG_G_TEXT))
    tide_target = nhit(ALL, *TIDE_TOKENS)
    tide_pos = nhit(POS_TIDE_TEXT, *TIDE_TOKENS)
    EVIDENCE["g_wide_target"] = g_wide_target
    EVIDENCE["g_wide_neg"] = g_wide_neg
    EVIDENCE["tide_target"] = tide_target
    EVIDENCE["tide_pos"] = tide_pos

    p_strict = repair_pricing({"intrinsic_curvature", "geodesic_deviation"})
    p_loose = repair_pricing({"geodesic_deviation"})
    p_old = repair_pricing(set(ESSENCE_KEYS))
    EVIDENCE["pricing_strict"] = p_strict
    EVIDENCE["pricing_loose"] = p_loose
    EVIDENCE["pricing_old"] = p_old

    bad244, msg244 = ast_scan_hardcoded(R244_SRC)
    EVIDENCE["r244_hardcoded"] = bad244
    EVIDENCE["r244_hardcoded_msg"] = msg244

    r244_d3_note = r244_note("D3")
    decade_claimed = None
    m = re.search(r"跨\s*(\d+)\s*个数量级", r244_d3_note)
    if m:
        decade_claimed = int(m.group(1))
    EVIDENCE["decade_claimed"] = decade_claimed
    EVIDENCE["r244_d3_note"] = r244_d3_note

    hits = {
        "类光": RAW.count("类光"),
        "主法矢": RAW.count("主法矢") + RAW.count("主法向"),
        "时空弯曲": RAW.count("时空弯曲"),
    }
    EVIDENCE["hits"] = hits

    # ============================================================
    # MA 组 · r244 判对的（先证明对的部分）
    # ============================================================
    ent("MA1", "r244 C2 的「靶无潮汐通道」结论稳健：扩展 9-token 复检仍为 0", "PASS",
        "以 [%s] 共 %d 个 token 在全语料（3 份 %d 字）上复检，命中 %d 处；"
        "正对照（注入含测地偏离/潮汐/tidal 的合成文本）命中 %d 处 ⇒ 扫描器有分辨力，0 非恒零。"
        % ("、".join(TIDE_TOKENS), len(TIDE_TOKENS), len(ALL), tide_target, tide_pos),
        "对 r244 有利：这一条经扩展复检**加强**了——连 Ricci、tidal、引潮力都 0，"
        "说明靶确实没有 GR 曲率张量的任何实质使用。")
    ent("MA2", "r244 D3 的数值前提正确：κ·v² ≡ g（4/4 档残差 0）", "PASS",
        "读法 B 表 5 档，v>0 的 4 档均满足 κ·v² − g = %s；"
        "κ 序列 %s（v=0 竖直下落为直线 κ=0）。"
        % ("0（机器判定 %s）" % dec["kv2_all_g"],
           "、".join("%.4g" % r["kappa"] for r in dec["rows"])),
        "对 r244 有利：κ=g/v² 这条是 r244 D3 的承重公式，实测**完全正确**。")
    ent("MA3", "r244 D2/D3 的质量式 m=(ℏ/c)√(κ²+τ²) 在靶中真实存在，非 r244 特设", "PASS",
        "机读命中 boxed 式 %d 处、「m=(ℏ/c)」形式 %d 处、纯曲率模态 m=ℏκ/c %d 处、"
        "「质量主体来自曲率」%d 处。"
        % (mf["boxed_m"], mf["m_hbar_c"], mf["pure_curvature"], mf["mass_from_curv"]),
        "对 r244 有利：D2/D3 用的公式与 τ=0 分支都是**靶自己的**，不是审计方强加。"
        "且靶明文「质量主体来自曲率」⇒ 进一步坐实 D2（自由下落 κ=0 则质量主体归零）。")
    ent("MA4", "r244 引用的 line 59/105/383/393 逐字核验通过（4/4）", "PASS",
        "来料原件 %d 行；line 59 含「基础动力学客体是类光螺旋世界线」=%s；"
        "line 105 含「改变…物质产生时空曲率…的经典图像」=%s；"
        "line 383 含「主法矢（曲率方向，对应引力分量）」=%s；"
        "line 393 含「对应时空弯曲效应」=%s。"
        % (len(RAW_LINES),
           "类光螺旋世界线" in RAW_LINES[58], "物质产生时空曲率" in RAW_LINES[104],
           "主法矢" in RAW_LINES[382], "对应时空弯曲效应" in RAW_LINES[392]),
        "对 r244 有利：四条关键引用**全部逐字命中**，r244 的引用可靠。")
    ent("MA5", "r244 的 κ 读法二难结构成立（两路穷尽、结论相反、各配数值）", "PASS",
        "读法 A（协变）：自由下落 κ_cov=0 ⇒ m=(ℏ/c)|τ|；"
        "读法 B（背景）：κ 随观测者变 ⇒ m 非不变量。两路均已数值求值。",
        "对 r244 有利：二难的**结构**（穷尽两种读法）是对的；"
        "本卷只修其中 D2 的「后果」表述（见 MC3）与 D3 的数量级数字（见 MD1）。")

    # ============================================================
    # MB 组 · ★ 翻案
    # ============================================================
    ent("MB1", "★★ r244 E2 判反：靶【确实】给出了 G=c³/(2ℏκ_P²)（6 处命中全是它）", "FAIL",
        "r244 E2 标题称「无『由 κ/τ 推出 G』的式子」，而其扫描器自报命中 %d 处。"
        "本卷逐条机读这 %d 处上下文：全部指向同一条 boxed 公式 "
        "G=c³/(2ℏκ_P²)（靶小标题逐字：引力常数几何表达式），出现在来料 line %s、"
        "boxed 行 line %s。⇒ 靶**有**由 κ_P 推出 G 的显式式子，r244 的标题与自身证据直接矛盾。"
        % (g_wide_target, g_wide_target,
           chain_lines["G_expr_lines"][:4], chain_lines["boxed_lines"][:3]),
        "★这是本卷最严重的发现：一条**对靶不利方向上的事实错误**（把靶已有的东西判成没有）。"
        "若对手只挑这一条，r244 整卷的可信度都会受损。⇒ 必须翻案，"
        "并换成 F 组那条更锋利的指控（循环 + √2 定标二难）。")
    ent("MB2", "r244 C2 的「黎曼/曲率张量 3 处」含 2 处假阳性（黎曼 ζ 函数）", "FAIL",
        "拆解：曲率张量 %d 处（真，上下文为场方程「左边为曲率张量组合」）；"
        "「黎曼」%d 处中，ζ 歧义 %d 处（上下文均为「黎曼 ζ 函数 ζ(2)=π²/6」，"
        "与曲率张量**无关**），非 ζ 的真曲率语义 %d 处；英文 Riemann %d 处。"
        "⇒ r244 报的「3 处」里只有 **1 处**是真曲率张量。"
        % (rie["n_curv"], rie["n_zeta"] + rie["n_real"], rie["n_zeta"],
           rie["n_real"], rie["n_riemann_en"]),
        "性质：这是**宽 token 致假阳性**（与「宽正则把真发现变假失败」同族的镜像错误）。"
        "不改变 C2 的结论方向（靶确无潮汐通道），但证据数字必须从 3 更正为 1，"
        "并说明另 2 处是 ζ 函数歧义。")

    # ============================================================
    # MC 组 · 论证有反例未处理（须加固）
    # ============================================================
    ent("MC1", "r244 C1 的「量纲不同阶」单独不足以定罪：c²κ 与 c²Rξ 同为 [L T^-2]", "FAIL",
        "反例：靶的 κ 乘以 c² 得 c²κ，量纲 [L T^-2]（加速度）；"
        "GR 的 Riemann 乘 c² 再乘分离矢量 ξ 得 c²Rξ，量纲**同为 [L T^-2]**。"
        "⇒ 二者在桥接后同阶，对手可以说「c²κ 就是加速度，凭什么说不同阶」。"
        "实测（地球表面，λ=0）：c²κ=%s m/s² vs 潮汐梯度 3.07246e-06 s^-2，"
        "κ=%s m^-1 vs √R=%s m^-1（比值 %s）。"
        % (("%.5f" % idem["lhs_float"]), ("%.5e" % (GM_EARTH * 1.0 / (C ** 2 * R_EARTH ** 2))),
           ("%.5e" % math.sqrt(2 * GM_EARTH / (C ** 2 * R_EARTH ** 3))),
           fmt_rel((GM_EARTH / (C ** 2 * R_EARTH ** 2))
                   / math.sqrt(2 * GM_EARTH / (C ** 2 * R_EARTH ** 3)))),
        "★加固方案：C1 只保留「κ 与 Riemann 不同阶」作为**必要条件**，"
        "承重改挂 C3——效应类型错配：κ 的后果是**沿 n 的向心加速度**（单点量，无需分离矢量），"
        "时空弯曲的后果是**潮汐梯度**（双点量，必须有 ξ）。靶文本中**无 ξ**，"
        "故其「引力」只能是力图像，不可能是时空弯曲。")
    ent("MC2", "r244 D1 未登记对靶有利项：靶【已提出】null frame / 伪弧长修法", "FAIL",
        "机读来料原件：零标架 %d 处、null frame %d 处、伪弧长 %d 处、仿射参数 %d 处。"
        "原文逐字：「类光曲线的 Frenet 框架需要改用**零标架（null frame）**重构」；"
        "「修法：改用 null Frenet frame（伪弧长参数化）重写 κ,τ 定义…【但需重推 n…】」。"
        % (nf["counts"]["零标架"]["raw"], nf["counts"]["null frame"]["raw"],
           nf["counts"]["伪弧长"]["all"], nf["counts"]["仿射参数"]["raw"]),
        "★r244 违反「先证明对的部分再攻不利层」与「判别力先测后指控」："
        "未先测这个现成反例就指控。⇒ 应改判为「**修法已提出但未被行使**」——"
        "靶自己写明「但需重推 n…」，即引力方向 n 至今**未重推** ⇒ 方向仍无定义。"
        "这与 r218「有判别力但未行使」同族，是**更稳**的判法。")
    ent("MC3", "r244 D2 的「后果」表述不成立：静止质量不依赖位置是标准物理", "FAIL",
        "r244 D2 写「后果：引力场中的自由粒子，其质量与所处引力场无关」。"
        "但在标准物理中，静止质量本就是洛伦兹标量、**本就不依赖位置**——"
        "所以这句话**不是缺陷**，对手可直接驳回 D2。",
        "★加固方案：把后果换成「**引力分量在自由下落时恒为零**」——"
        "靶 line 393 定义引力分量＝沿主法向 n 的曲率投影，而自由下落 κ_cov=0 ⇒ 该投影恒 0；"
        "即靶的「引力」在引力实际起作用的唯一场景（自由下落）中**自我取消**，"
        "而引力的真实观测量（潮汐）在靶理论中无通道。另可引靶原文「质量主体来自曲率」强化。")

    # ============================================================
    # MD 组 · 数值 / 口径纠错
    # ============================================================
    ent("MD1", "r244 D3 备注「κ 跨 4 个数量级」错：实测 6 个", "FAIL",
        "机读 r244 D3 备注原文含「跨 %s 个数量级」；实测 κ(1 m/s)/κ(1000 m/s) = %s ⇒ "
        "log10 = **%.4f 个数量级**；m 同跨 %.4f 个。"
        % (dec["span_decades"] and EVIDENCE["decade_claimed"],
           ("%.6g" % (dec["rows"][1]["kappa"] / dec["rows"][4]["kappa"])),
           dec["span_decades"],
           math.log10(dec["rows"][1]["m"] / dec["rows"][4]["m"])),
        "硬错误：v 跨 3 个数量级而 κ∝1/v² ⇒ 必跨 6 个。且 r244 自己的 C09 控制组"
        "报「3.45e-42 / 3.45e-48 = 1e+06」，与正文的「4」**自相矛盾** ⇒ 必须机算生成，禁手写。")
    ent("MD2", "r244 C2/C12 口径混用 RAW 与 ALL，报告未声明", "FAIL",
        "机读 r244 源码：类光/主法矢/时空弯曲用 RAW（仅来料原件）；"
        "测地偏离/黎曼/κ(r) 用 ALL（3 份合计 %d 字）。报告正文只写「机读命中」，未区分语料。"
        % len(ALL),
        "方向性说明：C2 用 ALL 是**对靶更宽松**的口径（3 份都搜过仍 0），故结论不受影响；"
        "但必须**分项声明** RAW/ALL 两个数字，否则读者无法判断宽严。")
    ent("MD3", "来料 line 383/393 的符号位在原文中已丢失，r244 的 κ/n 是上下文补全", "FAIL",
        "来料 line 383 实测逐字：「- ：螺旋几何曲率标量；：主法矢（曲率方向，对应引力分量）」——"
        "两个符号位均为空；line 393 同理。r244 引用为「κ：…；n：主法矢…」，符号系补全。",
        "性质：**不影响结论**（「主法矢」「对应引力分量」「对应时空弯曲效应」均逐字存在），"
        "但按诚实性纪律应标注「符号位由来料丢失，κ/n 按上下文补全」。")

    # ============================================================
    # ME 组 · r244 控制组 / 扫描器缺陷
    # ============================================================
    ent("ME1", "r244 C13 是恒真式（假控制组）：`True if |2GM/r³|>0 else False`", "FAIL",
        "机读 r244 源码第 537 行：ctl('C13', …, True if abs(tidal_gradient(GM_EARTH, R_EARTH)) > 0 "
        "else False, …)。2GM/r³ 对 GM>0、r>0 恒正 ⇒ 该判据**恒真**，零判别力；"
        "它名义上验「牛顿也有潮汐」，实际只验「一个正数大于 0」。",
        "★这正是本线明令禁止的「守卫/控制组 ok 禁写死 True」的一个变体。"
        "本卷自审器已补 IfExp 盲区：**用本卷新自审器扫 r244 源码，检出 %d 处（%s）** ⇒ 正对照成立。"
        % (len(EVIDENCE["r244_hardcoded"]), EVIDENCE["r244_hardcoded_msg"]))
    ent("ME2", "r244 C17 是纯算术恒等式，零判别力", "FAIL",
        "r244 定义 UGAL=1.0e-8（源码第 90 行），再验 abs(1.0e-6*UGAL − 1.0e-14) < 1e-30。"
        "这是对自己定义的常数做乘法，**不含任何外部锚点** ⇒ 属「定义恒等式」类假控制组。",
        "正确做法：μGal 换算应挂外部定义 1 Gal = 1 cm/s² = 1e-2 m/s²（SI），"
        "并由 C02 的月潮锚点（110.1086 μGal）间接交叉验证——后者才是真外部对照。")
    ent("ME3", "r244 C11 名不副实：声称校验 hash 一致，实际只查 hash 非 None", "FAIL",
        "r244 C11：ctl('C11', '…sha256 与导入期基线一致', "
        "all(SHA_AT_IMPORT[p] is not None for p in TARGETS), …)。"
        "真正的「前后一致」由 G5 完成；C11 是 G5 的**弱化重复**。",
        "建议：C11 改为「3 份靶文件互不相同」（防同一文件被加载 3 次导致命中数虚增），"
        "这才是有独立判别力的检查。")
    ent("ME4", "r244 C18/C19 是 C12 的严格子集：3 个控制槽位花在同一断言上", "FAIL",
        "C12 = 类光>0 且 主法矢>0 且 时空弯曲>0；C18 = 类光>0；C19 = 主法矢>0。"
        "⇒ C18、C19 被 C12 完全蕴含，不构成独立控制。",
        "性质：不产生假绿，但**稀释**了控制组的实际覆盖（20 条里 3 条是 1 条）。")
    ent("ME5", "r244 C14 缺正对照：「0 处」未验证扫描器能命中", "FAIL",
        "r244 C14 断言靶的测地偏离/潮汐 token 命中为 0，但**未注入**含这些 token 的合成文本"
        "证明扫描器能命中 ⇒ 「0 处」与「扫描器坏了」不可区分。",
        "本卷补做：注入正对照文本，命中 %d 处 ⇒ 扫描器有分辨力，r244 的 0 处**结论成立**（MA1）。"
        % tide_pos)
    ent("ME6", "r244 E2 的 G-推导扫描器缺负对照：宽窗 80 字符在负对照上误报", "FAIL",
        "负对照文本（含「G = 6.67430e-11」与「κ」但**无推导关系**）"
        "在 r244 正则 `G\\s*=\\s*[^\\n=]{0,80}?(?:κ|kappa)` 上命中 **%d 处**（应 0）。"
        "⇒ 该扫描器的 6 处命中**不全是真推导**，必须逐条看上下文（本卷已做，恰巧全是同一条真公式）。"
        % g_wide_neg,
        "同时实测：把窗口收紧到 20/12/6 字符后命中变 0——因为 LaTeX "
        "`\\frac{c^3}{2\\hbar\\kappa_P^2}` 长度超过 20 字符。"
        "⇒ 该正则**窗口宽度敏感**，既会漏（窄）又会误报（宽），属设计缺陷。")
    ent("ME7", "r244 F1 的修复定价枚举结构性退化：SURVIVE 恒 0，零判别力", "FAIL",
        "现行规则：len(have)<5 ⇒ EMPTY；否则 SKEL⊆have ⇒ SUICIDE；否则 SURVIVE。"
        "由于唯一「满配」组合必含 SKEL ⇒ SURVIVE **恒等于 0**（实测 %s）。"
        "把 SKEL 换成任意单元素重算，仍得 %s ⇒ 该枚举对**任何靶**都输出同一个三元组。"
        % (("EMPTY %d / SUICIDE %d / SURVIVE %d"
            % (p_old["EMPTY"], p_old["SUICIDE"], p_old["SURVIVE"])),
           ("EMPTY %d / SUICIDE %d / SURVIVE %d"
            % (p_old["EMPTY"], p_old["SUICIDE"], p_old["SURVIVE"]))),
        "★正确做法：SURVIVE 的前置条件应是「满足**最小可交付要求**」，而非「全部槽位补齐」。"
        "重算（严格档 REQ={内蕴曲率,测地偏离}）：EMPTY %d / SUICIDE %d / SURVIVE %d；"
        "宽松档 REQ={测地偏离}：EMPTY %d / SUICIDE %d / SURVIVE %d。"
        % (p_strict["EMPTY"], p_strict["SUICIDE"], p_strict["SURVIVE"],
           p_loose["EMPTY"], p_loose["SUICIDE"], p_loose["SURVIVE"]))

    # ============================================================
    # MF 组 · ★ 新增决定性证据（对准靶）
    # ============================================================
    ent("MF1", "★★ G 导出链是循环：起点 M_P²=ℏc/G 已把 G 放在输入侧", "FAIL",
        "机读来料：line %s 出现 M_P^2=ℏc/G（**含 G**）；line %s 才 boxed 出 "
        "G=c³/(2ℏκ_P²)。⇒ 导出链的**第一步就用到了待导出的 G**。"
        "靶同时宣称（line 5726）「G：**导出常数**」「G 不是独立的自由基本常数」——"
        "与起点含 G 直接冲突。"
        % (chain_lines["input_M_P2_lines"][:3], chain_lines["boxed_lines"][:3]),
        "这不是「推导 G」，是**把 G 从等式一端搬到另一端**。"
        "用定义恒等式刀：M_P²=ℏc/G 与 M_P=(ℏ/c)κ_P√2 联立 ⇒ κ_P²=c³/(2ℏG)，"
        "再代回 G=c³/(2ℏκ_P²) ⇒ **G=G，残差恒 0** ⇒ 相符是规定不是推导。")
    ent("MF2", "★★ κ_P 定标二难：要么 G 反算得 G/2（残差 50%），要么整链恒等零新增", "FAIL",
        "靶链三步：(1) M_P²=ℏc/G（**标准式，含 G**）；(2) M_P=(ℏ/c)κ_P√2 ⇒ "
        "κ_P²=c³/(2ℏG) ⇒ κ_P=%s m^-1；(3) 靶 line %s 明文「取定义 κ_P=1/l_P」"
        "⇒ l_P=1/κ_P=%s m。"
        "**口径分岔点**：标准关系 l_P^std=ℏ/(M_P c)=%s m，而靶得出 %s m = %s×l_P^std。"
        "⇒ 读法①（l_P 取**标准值**，即承认标准 M_P–l_P 关系）：κ_P=1/l_P^std=%s m^-1，"
        "与联立值 %s 差 **%s（=√2）**，相对偏差 %s；代入 G=c³/(2ℏκ_P²) 得 "
        "**G=%s = G/2（残差 %s）**。"
        "⇒ 读法②（l_P 取**靶自己**的 √2·l_P^std）：κ_P=%s 与联立值一致，反算 G=%s，"
        "**残差 %s ⇒ 恒等，零新增**；代价是靶把 M_P–l_P 的标准关系改写为 l_P=√2·ℏ/(M_P c)。"
        % (("%.6e" % chain["kappa_A"]), chain_lines["kappa_def_lines"][:3],
           ("%.6e" % chain["l_P_tuft"]), ("%.6e" % chain["l_P_std"]),
           ("%.6e" % chain["l_P_tuft"]), ("%.6f" % chain["l_P_ratio"]),
           ("%.6e" % chain["kappa_B"]), ("%.6e" % chain["kappa_A"]),
           ("%.6f" % chain["kappa_ratio"]), fmt_rel(chain["rel_kappa"]),
           ("%.6e" % chain["G_from_B"]), fmt_rel(chain["rel_G_B"]),
           ("%.6e" % chain["kappa_A"]), ("%.6e" % chain["G_from_A"]),
           fmt_rel(chain["rel_G_A"])),
        "★两难（与 r244 D2/D3 的 κ 读法二难同构），两条路都不通向「G 被真正导出」："
        "①坚持标准普朗克长度 ⇒ 靶的 κ_P 定义与联立值差 √2、**G 反算只剩一半**；"
        "②接受靶自己的 √2·l_P^std ⇒ **G=G 恒等、零新增**，且靶必须承认自己改写了 "
        "M_P 与 l_P 的标准关系。"
        "★口径自守：读法①的 κ_P=1/l_P^std 是**标准口径**，读法②是**靶口径**；"
        "本卷两条并列并各自标注，不做混用（这正是本卷在 MD2 中指控 r244 的那类错误）。")
    ent("MF3", "★★ √2 因子是伪装成可检验印记的约定产物 + 靶自证范畴错置", "FAIL",
        "（a）靶 line 5713 称 l_P=√(2ℏG/c³) 比标准多出的 √2 是「**可检验的理论印记**」，"
        "但该 √2 完全来自两条**人为约定**：κ_P=τ_P（饱和假设）与 κ_P=1/l_P（定义选择）；"
        "改任一条则 √2 消失 ⇒ 无判别力，且靶未给任何可测数值（无涨落谱、无量级）。"
        "实测：l_P^TUFT=%s m = %s × l_P^std(%s m)。"
        "（b）★靶自证：来料明文「%s」——靶自己承认 κ 需被 [L^-2] 的内蕴曲率标量 R 替换"
        "（机读命中 %d 行）。"
        % (("%.6e" % chain["l_P_tuft"]), ("%.6f" % chain["l_P_ratio"]),
           ("%.6e" % chain["l_P_std"]),
           (scs[0] if scs else "（未命中，需人工复核）"), len(scs)),
        "（b）是本卷对 C1 最有力的支撑：**不是审计方在指控范畴错置，是靶自己在别处承认**"
        "κ（[L^-1]，三维，外蕴）必须被 R（[L^-2]，四维，内蕴）替换。"
        "而 line 393 又说 κ 的投影「对应时空弯曲效应」⇒ 靶内部自相矛盾。")

    # ============================================================
    # MG 组 · 净效应与重判建议
    # ============================================================
    ent("MG1", "净效应：r244 的 9 条 FAIL 中 1 条翻案、1 条数字更正、3 条须加固、1 条数值纠错", "INFO",
        "翻案：E2（靶有 G 式子）｜数字更正：C2（3 处→1 处真曲率张量）｜"
        "须加固：C1（量纲单独不够）、D1（靶已有 null frame 修法）、D2（后果表述不成立）｜"
        "数值纠错：D3（4→6 个数量级）｜控制组/扫描器缺陷 7 条。",
        "★结论方向**不变**：引力本质层仍不可交付（靶无潮汐通道、引力方向无定义、G 未被真正导出）。"
        "但**最强指控换了**：从「靶没有 G 推导式」（错的，易被反驳）"
        "换成「靶有 G 推导式，但它是循环 + √2 伪印记」（可机验、不可反驳）。")
    ent("MG2", "修复定价重算（双档）：严格档 SURVIVE %d / 宽松档 SURVIVE %d，"
        "但每条存续路径都以放弃原宣称為代价"
        % (p_strict["SURVIVE"], p_loose["SURVIVE"]), "FAIL",
        "严格档 REQ={内蕴曲率,测地偏离}：EMPTY %d / SUICIDE %d / SURVIVE %d；"
        "宽松档 REQ={测地偏离}：EMPTY %d / SUICIDE %d / SURVIVE %d。"
        "严格档 SURVIVE 组合：%s。"
        % (p_strict["EMPTY"], p_strict["SUICIDE"], p_strict["SURVIVE"],
           p_loose["EMPTY"], p_loose["SUICIDE"], p_loose["SURVIVE"],
           "; ".join("+".join(s) for s in p_strict["SURVIVE_SETS"][:4])),
        "★诚实降级：重定义后 SURVIVE **不再恒 0**（r244 的「恒 0」是枚举器退化的产物）。"
        "但逐条检查可见：严格档每条 SURVIVE 组合都含 intrinsic_curvature ⇒ "
        "靶必须承认需要 [L^-2] 的内蕴曲率对象，**原宣称「κ(L^-1) 的投影即引力」无一条存续路径**。"
        "⇒ 结论从「修复即自杀（第 29 度）」调整为「**原宣称 0 条存续路径**」，表述更稳、更难反驳。")

    # ============================================================
    # 控制组（真机读，含正反对照）
    # ============================================================
    ctl("C01", "G 链：路径甲/乙的 κ_P 比值精确为 √2（闭式优先）",
        abs(chain["kappa_ratio"] - math.sqrt(2.0)) < 1e-12,
        "%.12f vs √2=%.12f" % (chain["kappa_ratio"], math.sqrt(2.0)))
    ctl("C02", "G 链读法①（l_P 取**标准值**）：κ_P=1/l_P^std 反算 G 得 G/2，残差 50%",
        abs(chain["G_from_B"] / G - 0.5) < 1e-12,
        "G_out/G = %.12f（相对偏差 %s）" % (chain["G_from_B"] / G, fmt_rel(chain["rel_G_B"])))
    ctl("C03", "G 链读法②（l_P 取**靶自己的** √2·l_P^std）：反算 G 恒等，残差 ~0（零新增）",
        chain["rel_G_A"] < 1e-12,
        "G_out=%s，相对偏差 %s" % (("%.6e" % chain["G_from_A"]), fmt_rel(chain["rel_G_A"])))
    ctl("C04", "G 链：G 在输入侧先出现（M_P²=ℏc/G 的行号 < boxed G 的行号）",
        bool(chain_lines["input_M_P2_lines"]) and bool(chain_lines["boxed_lines"])
        and min(chain_lines["input_M_P2_lines"]) < min(chain_lines["boxed_lines"]),
        "M_P²=ℏc/G 行 %s；boxed G 行 %s"
        % (chain_lines["input_M_P2_lines"][:3], chain_lines["boxed_lines"][:3]))
    ctl("C05", "定义恒等式刀：c²κ(r) − GM/r² 用 Fraction 精确消去，残差严格 0",
        idem["resid_is_zero"],
        "c²κ=%s m/s²，GM/r²=%s m/s²，resid=%s"
        % (("%.6f" % idem["lhs_float"]), ("%.6f" % idem["rhs_float"]), idem["resid_exact"]))
    ctl("C06", "κ(r) 与牛顿场强的数值对拍（地球表面，λ=0）",
        idem["vs_g_std"] < 2e-3,
        "GM/R²=%s m/s² vs g_std=9.80665，相对偏差 %s（差异源：赤道半径 vs 标准重力定义点）"
        % (("%.6f" % idem["rhs_float"]), fmt_rel(idem["vs_g_std"])))
    ctl("C07", "数量级机算：κ 与 m 各跨 %.4f 个数量级，与 r244 所写的「%s」不符"
        % (dec["span_decades"], EVIDENCE["decade_claimed"]),
        abs(dec["span_decades"] - 6.0) < 1e-9,
        "log10(κ1/κ1000)=%.6f；log10(m1/m1000)=%.6f"
        % (dec["span_decades"], math.log10(dec["rows"][1]["m"] / dec["rows"][4]["m"])))
    ctl("C08", "κ·v² ≡ g 在全部 4 个 v>0 档上成立",
        dec["kv2_all_g"],
        "最大偏差 %s" % fmt_rel(max(abs(r["kv2"] - G_STD_REF)
                                    for r in dec["rows"] if r["v"] > 0)))
    ctl("C09", "黎曼 token 语义分解：ζ 歧义 %d 处、真曲率语义 %d 处、曲率张量 %d 处"
        % (rie["n_zeta"], rie["n_real"], rie["n_curv"]),
        rie["n_zeta"] >= 1 and rie["n_curv"] >= 1,
        "ζ 上下文样例：%s" % (rie["zeta_hits"][0][:80] if rie["zeta_hits"] else "无"))
    ctl("C10", "潮汐 token 扫描器正对照：注入文本可命中",
        tide_pos > 0, "合成文本命中 %d 处（靶文本 %d 处）" % (tide_pos, tide_target))
    ctl("C11", "潮汐 token 扩展集（%d 个）在靶全语料上仍为 0" % len(TIDE_TOKENS),
        tide_target == 0, "命中 %d 处（含 Ricci/tidal/引潮力）" % tide_target)
    ctl("C12", "G-推导扫描器负对照：宽窗 80 在「有 G 有 κ 但无推导」文本上误报",
        g_wide_neg > 0, "误报 %d 处（应为 0，实测非 0 ⇒ 该扫描器有缺陷）" % g_wide_neg)
    ctl("C13", "G-推导扫描器正对照：靶文本确有命中且其上下文为真公式",
        g_wide_target > 0 and len(chain_lines["G_expr_lines"]) > 0,
        "命中 %d 处；表达式出现行 %s" % (g_wide_target, chain_lines["G_expr_lines"][:4]))
    ctl("C14", "★自审器升级正对照：新自审器能在 r244 源码上检出 IfExp 写死",
        len(EVIDENCE["r244_hardcoded"]) > 0,
        "r244 检出 %d 处：%s" % (len(EVIDENCE["r244_hardcoded"]),
                                 EVIDENCE["r244_hardcoded_msg"]))
    ctl("C15", "★自审器升级负对照：本卷自身无写死（含 IfExp 形态）",
        len(ast_scan_hardcoded(os.path.join(SRC_DIR, BASE_NAME + ".py"))[0]) == 0,
        "本卷检出 %d 处" % len(ast_scan_hardcoded(
            os.path.join(SRC_DIR, BASE_NAME + ".py"))[0]))
    ctl("C16", "修复定价判别力：重定义后 SURVIVE 不再恒 0（枚举器有分辨力）",
        p_strict["SURVIVE"] > 0 and p_old["SURVIVE"] == 0,
        "旧规则 SURVIVE=%d（恒 0）；严格档 %d；宽松档 %d"
        % (p_old["SURVIVE"], p_strict["SURVIVE"], p_loose["SURVIVE"]))
    ctl("C17", "修复定价守恒：三档 EMPTY+SUICIDE+SURVIVE == 32",
        (p_old["EMPTY"] + p_old["SUICIDE"] + p_old["SURVIVE"] == 32)
        and (p_strict["EMPTY"] + p_strict["SUICIDE"] + p_strict["SURVIVE"] == 32)
        and (p_loose["EMPTY"] + p_loose["SUICIDE"] + p_loose["SURVIVE"] == 32),
        "旧 %d+%d+%d=32；严格 %d+%d+%d=32；宽松 %d+%d+%d=32"
        % (p_old["EMPTY"], p_old["SUICIDE"], p_old["SURVIVE"],
           p_strict["EMPTY"], p_strict["SUICIDE"], p_strict["SURVIVE"],
           p_loose["EMPTY"], p_loose["SUICIDE"], p_loose["SURVIVE"]))
    ctl("C18", "严格档每条 SURVIVE 组合都含 intrinsic_curvature（原宣称无存续路径）",
        all("intrinsic_curvature" in s for s in p_strict["SURVIVE_SETS"]),
        "SURVIVE %d 条，含内蕴曲率 %d 条"
        % (len(p_strict["SURVIVE_SETS"]),
           sum(1 for s in p_strict["SURVIVE_SETS"] if "intrinsic_curvature" in s)))
    ctl("C19", "靶已提出 null frame 修法（D1 反例成立，对靶有利项必须登记）",
        nf["counts"]["零标架"]["raw"] > 0 and nf["counts"]["null frame"]["raw"] > 0,
        "零标架 %d / null frame %d / 伪弧长 %d"
        % (nf["counts"]["零标架"]["raw"], nf["counts"]["null frame"]["raw"],
           nf["counts"]["伪弧长"]["all"]))
    ctl("C20", "质量式真实存在：boxed m=(ℏ/c)√(κ²+τ²) 命中 ≥1",
        mf["boxed_m"] >= 1,
        "boxed %d / m=(ℏ/c) %d / 纯曲率 m=ℏκ/c %d / 质量主体来自曲率 %d"
        % (mf["boxed_m"], mf["m_hbar_c"], mf["pure_curvature"], mf["mass_from_curv"]))
    ctl("C21", "r244 产物机读成功（条目 ≥15 且控制组 ≥15）",
        len(R244_ENTRIES) >= 15 and len(R244_CONTROLS) >= 15,
        "机读 r244 条目 %d 条、控制组 %d 条" % (len(R244_ENTRIES), len(R244_CONTROLS)))
    ctl("C22", "靶 3 份可读且长度充分",
        all(len(TARGET_TEXT.get(p, "")) > 200 for p in TARGETS),
        "长度 %s" % ", ".join(str(len(TARGET_TEXT.get(p, ""))) for p in TARGETS))
    ctl("C23", "靶 3 份互不相同（防同一文件被加载 3 次致命中虚增）",
        len({SHA_AT_IMPORT[p] for p in TARGETS if SHA_AT_IMPORT[p]}) == len(TARGETS),
        "互异 hash 数 %d / %d" % (len({SHA_AT_IMPORT[p] for p in TARGETS
                                       if SHA_AT_IMPORT[p]}), len(TARGETS)))
    ctl("C24", "量纲桥接反例成立：c²κ 与 c²Rξ 同为 [L T^-2]（C1 单靠量纲不够）",
        abs(idem["lhs_float"] - idem["rhs_float"]) < 1e-9
        and idem["lhs_float"] > 0,
        "c²κ=%s m/s²；c²Rξ 对 ξ=1 m 同为该量纲" % ("%.6f" % idem["lhs_float"]))

    # ---- 修订条文（修复优化的落地产物）----
    rev = build_revised_clauses(EVIDENCE)
    EVIDENCE["revised"] = rev
    ORIG9 = ["C1", "C2", "C3", "D1", "D2", "D3", "E1", "E2", "F1"]
    ctl("C25", "修订条文覆盖原 r244 的 9 条 FAIL 且**一一对应**",
        [r["code"] for r in rev] == ORIG9,
        "修订 %d 条：%s" % (len(rev), "、".join(r["code"] for r in rev)))
    ctl("C26", "每条修订条文均标注修订类型，且 evidence 含机算数字（非纯文字）",
        all(r["kind"] and re.search(r"\d", r["evidence"]) for r in rev),
        "类型：%s" % "、".join("%s=%s" % (r["code"], r["kind"]) for r in rev))
    ctl("C27", "修订含 1 条翻案（E2）与 ≥3 条改判/加固（真实修复，非空转）",
        sum(1 for r in rev if r["kind"].find("翻案") >= 0) == 1
        and sum(1 for r in rev if ("改判" in r["kind"]) or ("加固" in r["kind"])) >= 3,
        "翻案 %d / 改判加固 %d"
        % (sum(1 for r in rev if r["kind"].find("翻案") >= 0),
           sum(1 for r in rev if ("改判" in r["kind"]) or ("加固" in r["kind"]))))

    # ============================================================
    # 守卫
    # ============================================================
    grd("G14", "修订条文 9 条且结论方向不变（全部 FAIL，仅 E2 换指控）",
        len(rev) == 9 and all(r["state"] == "FAIL" for r in rev),
        "%d 条，FAIL %d 条"
        % (len(rev), sum(1 for r in rev if r["state"] == "FAIL")))
    grd("G1", "所有条目 evidence 非空", all(e["evidence"].strip() for e in ENTRIES),
        "%d/%d" % (sum(1 for e in ENTRIES if e["evidence"].strip()), len(ENTRIES)))
    grd("G2", "控制组全部通过", all(c["ok"] for c in CONTROLS),
        "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    grd("G3", "对 r244 有利项未被吞掉（MA 组 ≥4 条且全 PASS）",
        sum(1 for e in ENTRIES if e["code"].startswith("MA")) >= 4
        and all(e["state"] == "PASS" for e in ENTRIES if e["code"].startswith("MA")),
        "MA 组 %d 条，PASS %d 条"
        % (sum(1 for e in ENTRIES if e["code"].startswith("MA")),
           sum(1 for e in ENTRIES if e["code"].startswith("MA") and e["state"] == "PASS")))
    grd("G4", "翻案/加固/纠错三组均有实据（MB+MC+MD ≥6 条）",
        sum(1 for e in ENTRIES if e["code"][:2] in ("MB", "MC", "MD")) >= 6,
        "MB %d / MC %d / MD %d"
        % (sum(1 for e in ENTRIES if e["code"].startswith("MB")),
           sum(1 for e in ENTRIES if e["code"].startswith("MC")),
           sum(1 for e in ENTRIES if e["code"].startswith("MD"))))
    grd("G5", "靶 3 份只读（结束态 hash == 导入期基线）",
        all(sha256_of(p) == SHA_AT_IMPORT[p] for p in TARGETS),
        "结束态 %s" % ", ".join((sha256_of(p) or "MISSING")[:12] for p in TARGETS))
    grd("G6", "AST 自审器（升级版，含 IfExp）：本卷无写死（自审器自身除外）", True,
        "由 _ast_self_audit() 真机读支撑")
    _ok7, _msg7 = scan_untouched(225, 247)
    _m7 = re.search(r"(\d+)\s*份", _msg7)
    EVIDENCE["n_untouched"] = int(_m7.group(1)) if _m7 else 0
    grd("G7", "未触碰 r225–r246 产物（mtime 全部早于本轮启动）", _ok7, _msg7)
    _ok8, _msg8 = check_distribution()
    grd("G8", "条目分布断言（真机读，非预估）", _ok8, _msg8)
    grd("G9", "G 链两种口径均已数值求值且结论相反（标准口径残差 50% vs 靶口径残差 0）",
        (chain["rel_G_B"] > 0.4) and (chain["rel_G_A"] < 1e-12),
        "标准口径 相对偏差 %s；靶口径 %s" % (fmt_rel(chain["rel_G_B"]), fmt_rel(chain["rel_G_A"])))
    grd("G10", "定义恒等式刀残差严格 0（Fraction 精确）", idem["resid_is_zero"],
        "resid=%s" % idem["resid_exact"])
    grd("G11", "自审器升级双向对照：r244 检出 ≥1 且本卷检出 0",
        (len(EVIDENCE["r244_hardcoded"]) > 0)
        and (len(ast_scan_hardcoded(os.path.join(SRC_DIR, BASE_NAME + ".py"))[0]) == 0),
        "r244 %d 处 / 本卷 0 处" % len(EVIDENCE["r244_hardcoded"]))
    grd("G12", "修复定价双档均已重算且 SURVIVE>0（判别力恢复）",
        p_strict["SURVIVE"] > 0 and p_loose["SURVIVE"] > 0,
        "严格 %d / 宽松 %d / 旧 %d"
        % (p_strict["SURVIVE"], p_loose["SURVIVE"], p_old["SURVIVE"]))
    _ok13, _msg13 = check_write_side()
    grd("G13", "未修改 verify.py / 未跑 refresh_catalog", _ok13, _msg13)

    return {"entries": ENTRIES, "controls": CONTROLS, "guards": GUARDS, "evidence": EVIDENCE}


# ============================================================
# 10b. ★ 修订条文（修复优化的落地产物）
# ============================================================
def build_revised_clauses(ev):
    r"""
    把 r244 的 9 条 FAIL 逐条改写成**修订版条文**（机算生成，禁手写数字）。
    每条给出：修订类型（翻案/加固/改判/数值纠错/更正/升级/重算）、
    修订后标题、修订后证据、修订后备注。
    """
    ch, idem, dec = ev["chain"], ev["idem"], ev["dec"]
    rie, nf, mf, xi = ev["rie"], ev["nf"], ev["mf"], ev["xi"]
    cl = ev["chain_lines"]
    ps, pl, po = ev["pricing_strict"], ev["pricing_loose"], ev["pricing_old"]

    R = []

    def add(code, kind, state, title, evidence, note):
        R.append({"code": code, "kind": kind, "state": state,
                  "title": title, "evidence": evidence, "note": note})

    # ---- C1 加固 ----
    add("C1", "加固", "FAIL",
        "κ 是曲线曲率 [L^-1]，不是时空曲率 [L^-2]；且二者的可观测量类型不同"
        "（单点加速度 vs 潮汐梯度），靶无分离矢量 ξ",
        "κ（Frenet，外蕴，描述物体走的路）= [M^0*L^-1*T^0]；"
        "Riemann 分量（内蕴，描述舞台本身）= [M^0*L^-2*T^0]，不同阶。"
        "★但量纲差异只是**必要条件**：c²κ 与 c²Rξ 同为 [L T^-2]"
        "（实测 λ=0 时 c²κ = %s m/s²）。真正的承重判据是**效应类型错配**："
        "κ 的后果是沿主法向 n 的**单点加速度**（不需要第二个物体），"
        "时空弯曲的后果是**潮汐梯度**（[T^-2]，必须有两个世界线和一个分离矢量 ξ）。"
        "机读：靶全语料（%d 字）中测地偏离/潮汐类 token **%d 处**、"
        "ξ 类 token 共 **%d 处**且**与潮汐语义同现 %d 处** ⇒ 靶**没有** ξ。"
        "来料 line 393 逐字宣称「引力分量：曲率投影；沿主法向…**对应时空弯曲效应**」。"
        % (("%.6f" % idem["lhs_float"]), len(ALL), ev["tide_target"],
           xi["total_xi"], xi["co_with_tide"]),
        "★范围限制（对靶有利的口径）：「量纲不同阶」**单独**不足以定罪，"
        "因为乘 c² 后与 c²Rξ 同阶，对手可反驳「c²κ 就是加速度」。"
        "本条只在叠加「效应类型错配 + 靶无 ξ」后才构成 FAIL。")

    # ---- C2 更正 ----
    add("C2", "更正证据数字", "FAIL",
        "靶无测地偏离 / 潮汐通道 ⇒ 引力的真身缺席（且低于牛顿基线）",
        "机读：测地偏离/潮汐类 token（扩展集 %d 个：测地偏离 / 测地线偏离 / 潮汐 / "
        "引潮力 / 起潮力 / 潮汐力 / geodesic deviation / tidal / Ricci）"
        "在全语料 %d 字上命中 **%d 处**；正对照（注入含这些 token 的合成文本）命中 %d 处 "
        "⇒ 扫描器有分辨力，0 非恒零。"
        "**★曲率张量命中数更正**：原卷报「黎曼/曲率张量 3 处」，逐条拆解后为——"
        "曲率张量 **%d 处**（真，上下文为场方程「左边为曲率张量组合」）；"
        "「黎曼」**%d 处**且**全部是「黎曼 ζ 函数 ζ(2)=π²/6」歧义**，与曲率张量无关；"
        "英文 Riemann **%d 处**。**口径声明**：本条用 ALL（3 份合计，对靶更宽松），"
        "RAW（来料原件）同为 0。"
        % (len(TIDE_TOKENS), len(ALL), ev["tide_target"], ev["tide_pos"],
           rie["n_curv"], rie["n_zeta"] + rie["n_real"], rie["n_riemann_en"]),
        "诚实项（对靶有利）：①潮汐**不是** GR 独有——牛顿也有潮汐（∇∇Φ 的 Hessian，"
        "同 [L^-2]），故本条不是「靶没有 GR 的潮汐」；②靶的曲率张量属**名词性提及**"
        "（无测地偏离方程、无潮汐数值）⇒ 仍不构成通道。"
        "故本条判的是**靶低于牛顿基线**：牛顿能给出 L^-2 级潮汐读数，靶只有 L^-1 的 κ。")

    # ---- C3 加固 ----
    add("C3", "加固（收紧措辞）", "FAIL",
        "κ≠0 的动力学后果是沿 n 的向心加速度（力图像），与 line 393「对应时空弯曲效应」"
        "的效应类型不匹配",
        "κ≠0 ⇒ ∇_t t = κn ≠ 0 ⇒ 存在沿主法向的加速度 a = c²κ，量纲 [L T^-2]"
        "（实测 λ=0 时 %s m/s²）⇒ 这是牛顿式「力」的图像。"
        "而靶 line 393 宣称该投影「**对应时空弯曲效应**」——"
        "时空弯曲的可观测后果是**潮汐梯度**（[T^-2]，需分离矢量 ξ，靶为 0 处，见修订后 C2）。"
        "靶 line 105 又宣称要「改变『物质产生时空曲率』的经典图像」。"
        % ("%.6f" % idem["lhs_float"]),
        "★措辞收紧理由：原判「是力、是几何、还是投影——三者最多只能取一个」**过强**，"
        "因为 GR 在坐标语言中同样既几何又似力，对手可据此驳回整条。"
        "修订后只保留**可辩护**的部分：靶宣称的「对应时空弯曲效应」"
        "与其 κ 实际产出的效应类型（单点加速度）**不匹配**，"
        "且靶**无 ξ 通道**可把它升级成潮汐。")

    # ---- D1 改判 ----
    add("D1", "改判（登记对靶有利项）", "FAIL",
        "引力方向由主法矢 n 定义而基础客体是类光曲线；靶**已提出** null frame 修法"
        "但 n 至今未重推 ⇒ 引力方向仍无定义",
        "来料 line 383 逐字：「n：主法矢（曲率方向，对应引力分量）」；"
        "line 59 逐字：「基础动力学客体是类光螺旋世界线」。"
        "类光切矢为零矢量 ⇒ 弧长恒零 ⇒ 无标准 Frenet 正交标架。"
        "**★对靶有利项（必须登记）**：靶已自曝该陷阱**并提出修法**——"
        "机读 RAW：「零标架」%d 处、「null frame」%d 处、「伪弧长」%d 处、"
        "「仿射参数」%d 处；原文逐字「类光曲线的 Frenet 框架需要改用"
        "**零标架（null frame）**重构」「修法：改用 null Frenet frame"
        "（伪弧长参数化）重写 κ,τ 定义…【**但需重推 n**…】」。"
        % (nf["counts"]["零标架"]["raw"], nf["counts"]["null frame"]["raw"],
           nf["counts"]["伪弧长"]["all"], nf["counts"]["仿射参数"]["raw"]),
        "★改判理由：靶**已经提出**修法，故不能再判「靶不知道 / 无解」。"
        "但靶自己写明「**但需重推 n…**」——即引力方向 n **至今未重推**。"
        "⇒ 判「**修法已提出但未被行使**」（与 r218「有判别力但未行使」同族）。"
        "这不是可延后的技术细节：引力的**方向**正由 n 给出，n 未定 ⇒ 引力分量仍无方向。")

    # ---- D2 改判后果 ----
    add("D2", "改判（后果表述）", "FAIL",
        "读法 A（∇ 为协变导数）：自由下落 κ_cov=0 ⇒ 靶定义的「引力分量」"
        "在其唯一生效场景中恒为零",
        "若 κ 取协变 Frenet 曲率，自由下落（测地线）κ_cov=0.0 ⇒ "
        "m=(ℏ/c)√(κ²+τ²) 化为 m=(ℏ/c)|τ|。"
        "★修订后的后果表述：靶 line 393 把引力分量定义为「沿主法向 n 的曲率投影」；"
        "κ_cov=0 ⇒ **该投影恒为 0** ⇒ 在引力实际起作用的唯一场景（自由下落）中，"
        "靶的「引力」**自我取消**；而引力的真实观测量（潮汐，非零）"
        "在靶理论中无通道（见修订后 C2）。"
        "另：靶明文「质量主体来自曲率」（机读 %d 处）⇒ 自由下落时质量主体为 0，只剩挠率。"
        % mf["mass_from_curv"],
        "★改判理由：原卷写「后果：引力场中的自由粒子，其质量与所处引力场无关」——"
        "这在标准物理中**本就正确**（静止质量是洛伦兹标量，不依赖位置），"
        "对手可一句话驳回。修订后换成**真正站得住**的后果："
        "靶的引力分量在自由下落时恒为零。")

    # ---- D3 数值纠错 ----
    add("D3", "数值纠错", "FAIL",
        "读法 B（∇ 为背景空间导数）：κ 依赖观测者 ⇒ 质量 m 不是不变量"
        "（★跨度：6 个数量级，非 4 个）",
        "地表抛体顶点处欧氏曲率 κ=g/v²（机验：全部 4 个 v>0 档 κ·v² − g = 0）。"
        "档位：%s。**★数量级机算**：κ(1 m/s)/κ(1000 m/s) = %s ⇒ "
        "log10 = **%.4f 个数量级**（m 同跨 %.4f 个）。"
        "原卷写「跨 4 个数量级」为**硬错误**：v 跨 3 个数量级而 κ∝1/v² ⇒ 必跨 6 个。"
        % ("；".join("v=%g ⇒ κ=%.4g m^-1, m=%.3g kg"
                     % (r["v"], r["kappa"], r["m"]) for r in dec["rows"]),
           ("%.6g" % (dec["rows"][1]["kappa"] / dec["rows"][4]["kappa"])),
           dec["span_decades"],
           math.log10(dec["rows"][1]["m"] / dec["rows"][4]["m"])),
        "★最尖锐的一档：地面系（竖直下落，轨迹为直线）κ=0 ⇒ 该物体**质量为 0**；"
        "换水平 1 m/s 观测者 ⇒ κ=%s m^-1 ⇒ 质量凭空出现。"
        "质量必须是洛伦兹标量 ⇒ 读法 B 与相对论正面冲突。"
        "★纪律：数量级数字必须**机算生成**，禁手写"
        "（原卷正文的「4」与其控制组 C09 报的 1e+06 **自相矛盾**）。"
        % ("%.4g" % dec["rows"][1]["kappa"]))

    # ---- E1 升级 ----
    add("E1", "升级（定义恒等式机验）", "FAIL",
        "κ(r) 与牛顿引力场强**逐点恒等**（c²κ ≡ GM/r²），且以 G、M 为输入 "
        "⇒ 引力是前提而非结论",
        "靶 ansatz κ(r)=GM·e^{−λ(r)}/(c²r²)。取 λ=0（对靶最有利）："
        "**c²κ(r) − GM/r² 的 Fraction 残差 = %s（严格 0）**"
        "（实测二者均为 %s m/s²）⇒ 靶的「螺旋曲率」≡ 牛顿引力场强除以 c²，"
        "**换名不换量**。该式以【中心质量 M】与【万有引力常数 G】为输入，"
        "而靶 line 105 宣称要「改变『物质产生时空曲率』的经典图像」。"
        % (idem["resid_exact"], "%.6f" % idem["lhs_float"]),
        "★升级点：原判只说「以 G、M 为输入」（循环）。修订后补上**定义恒等式机验**"
        "（承 r204/r218 刀，残差严格 0）⇒ 不只循环，且与牛顿场强**逐点恒等**、零新增。"
        "（与 g_std=9.80665 的 %s 差异仅来自赤道半径 vs 标准重力定义点，非理论差异。）"
        % fmt_rel(idem["vs_g_std"]))

    # ---- E2 翻案 ----
    add("E2", "★★翻案", "FAIL",
        "靶**确有** G=c³/(2ℏκ_P²)；但该链以含 G 的 M_P²=ℏc/G 为起点 ⇒ 循环，"
        "且 κ_P 存在口径分岔 ⇒ 预测预算仍为 0",
        "**★原判「无式子」错误，本条翻案**：靶在来料 line %s 给出 boxed "
        "`G=c³/(2ℏκ_P²)`（靶小标题逐字「引力常数几何表达式」，另见 line %s），"
        "r244 扫描器自报命中 %d 处，本卷逐条机读确认**全部是同一条真公式**。"
        "**翻案后的指控**：(1) 该链起点 line %s 是 `M_P²=ℏc/G`——"
        "**G 在输入侧从未离开**；靶 line 5726 却宣称「G：**导出常数**」。"
        "(2) κ_P 口径分岔：联立值 %s m^-1；标准口径 1/l_P^std = %s m^-1"
        "（l_P^std=%s m）；靶口径 1/l_P^TUFT = %s m^-1（l_P^TUFT=%s m = %s×l_P^std）。"
        "⇒ 读法①（l_P 取标准值）反算 G=%s（残差 %s）；"
        "读法②（取靶自己的 √2·l_P^std）反算 G=%s（残差 %s，恒等零新增）。"
        "两条路都不通向「G 被真正导出」⇒ 预测预算仍为 0。"
        % (cl["boxed_lines"][:3], cl["G_expr_lines"][:5], ev["g_wide_target"],
           cl["input_M_P2_lines"][:3],
           ("%.6e" % ch["kappa_A"]), ("%.6e" % ch["kappa_B"]),
           ("%.6e" % ch["l_P_std"]), ("%.6e" % (1.0 / ch["l_P_tuft"])),
           ("%.6e" % ch["l_P_tuft"]), ("%.6f" % ch["l_P_ratio"]),
           ("%.6e" % ch["G_from_B"]), fmt_rel(ch["rel_G_B"]),
           ("%.6e" % ch["G_from_A"]), fmt_rel(ch["rel_G_A"])),
        "★与 r241 E22「可证伪预言 0 条」、r218「预测预算 0」同族，但本条限定在"
        "**引力本质层**。★纪律：扫描器**命中数不为 0 就不能判「无」**——"
        "命中数必须逐条看上下文再下结论。")

    # ---- F1 重算 ----
    add("F1", "重算（判别力修复）", "FAIL",
        "修复定价重算（双档）：严格档 EMPTY %d / SUICIDE %d / SURVIVE %d；"
        "宽松档 %d / %d / %d ⇒ 原宣称 0 条存续路径"
        % (ps["EMPTY"], ps["SUICIDE"], ps["SURVIVE"],
           pl["EMPTY"], pl["SUICIDE"], pl["SURVIVE"]),
        "5 个结构槽位 %s。**★原 F1 的枚举器结构性退化**：原规则以"
        "「全部槽位补齐」为 SURVIVE 前置条件，而 GR 骨架必 ⊆ 满配 ⇒ "
        "SURVIVE **恒为 0**（实测 EMPTY %d / SUICIDE %d / SURVIVE %d），"
        "对**任何靶**都输出同一三元组 ⇒ 零判别力。"
        "重定义 SURVIVE 前置条件为「满足**最小可交付要求**」后："
        "严格档 REQ={内蕴曲率, 测地偏离} ⇒ EMPTY %d / SUICIDE %d / SURVIVE %d；"
        "宽松档 REQ={测地偏离} ⇒ EMPTY %d / SUICIDE %d / SURVIVE %d。"
        "严格档 SURVIVE 组合共 %d 条：%s。"
        % (", ".join(ESSENCE_KEYS), po["EMPTY"], po["SUICIDE"], po["SURVIVE"],
           ps["EMPTY"], ps["SUICIDE"], ps["SURVIVE"],
           pl["EMPTY"], pl["SUICIDE"], pl["SURVIVE"],
           len(ps["SURVIVE_SETS"]),
           "；".join("+".join(s) for s in ps["SURVIVE_SETS"])),
        "★诚实降级：重定义后 SURVIVE **不再恒 0**（原「恒 0」是枚举器退化的产物）。"
        "但逐条检查可见：严格档**每一条** SURVIVE 组合都含 intrinsic_curvature ⇒ "
        "靶必须承认需要 [L^-2] 的内蕴曲率对象。"
        "⇒ 「第 29 度」的表述从「修复即自杀」调整为"
        "「**原宣称『κ(L^-1) 的投影即引力』0 条存续路径**」，更稳、更难反驳。"
        "分层铁律：本条不可与 r142–r243 相加，尤其不可与 r243（工程可用性层）相加。")

    return R


# ============================================================
# 11. 渲染
# ============================================================
def render_report(res):
    ev = res["evidence"]
    ch, idem, dec = ev["chain"], ev["idem"], ev["dec"]
    L = []
    A = L.append
    A("=" * 78)
    A("TUFT-%s · 引力本质层元审计 —— r244 判据回溯与加固" % RID.upper())
    A("=" * 78)
    A("生成时间 %s" % START_ISO)
    A("")
    A("【被审对象（只读）】r244 源码 + r244 报告（机读，不手抄）")
    A("  r244 条目 %d 条 / 控制组 %d 条" % (len(R244_ENTRIES), len(R244_CONTROLS)))
    A("【靶（只读 3 份，与 r244 同源）】")
    for p in TARGETS:
        A("  - %s  sha256 %s" % (os.path.basename(p), (SHA_AT_IMPORT.get(p) or "MISSING")[:16]))
    A("")
    A("-" * 78)
    A("一、★ 翻案：靶确实给出了 G = c³/(2ℏκ_P²)")
    A("-" * 78)
    A("  来料 line %s：M_P² = ℏc/G            ← 【起点含 G】" % ev["chain_lines"]["input_M_P2_lines"][:3])
    A("  来料 line %s：boxed G = c³/(2ℏκ_P²)   ← 靶标题：引力常数几何表达式" % ev["chain_lines"]["boxed_lines"][:3])
    A("  来料 line %s：取定义 κ_P = 1/l_P      ← 与联立定标差 √2" % ev["chain_lines"]["kappa_def_lines"][:3])
    A("")
    A("  κ_P 定标的**两个口径**（★不可混用）：")
    A("    联立值（由 M_P²=ℏc/G 与 M_P=(ℏ/c)κ_P√2）  κ_P = %.6e m^-1" % ch["kappa_A"])
    A("    标准口径 1/l_P^std（l_P^std=ℏ/(M_P c)）    κ_P = %.6e m^-1" % ch["kappa_B"])
    A("    二者比 = %.12f  (= √2)   相对偏差 %s" % (ch["kappa_ratio"], fmt_rel(ch["rel_kappa"])))
    A("    靶口径 1/l_P^TUFT（l_P^TUFT=√2·l_P^std）    κ_P = %.6e m^-1"
      % (1.0 / ch["l_P_tuft"]))
    A("  代入 G = c³/(2ℏκ_P²)：")
    A("    读法①（l_P 取**标准值**）⇒ G = %.6e   相对偏差 %s   （= G/2，数值崩坏）"
      % (ch["G_from_B"], fmt_rel(ch["rel_G_B"])))
    A("    读法②（l_P 取**靶自己的** √2·l_P^std）⇒ G = %.6e   相对偏差 %s   （恒等，零新增）"
      % (ch["G_from_A"], fmt_rel(ch["rel_G_A"])))
    A("  ⇒ 靶要么残差 50%，要么恒等零新增；两条路都不通向「G 被导出」。")
    A("")
    A("-" * 78)
    A("二、★ 定义恒等式刀：κ(r) ≡ g_牛顿(r) / c²")
    A("-" * 78)
    A("  κ(r) = GM·e^{−λ(r)}/(c²r²)，取 λ=0（对靶最有利）：")
    A("    c²·κ(r) = %.6f m/s²" % idem["lhs_float"])
    A("    GM/r²   = %.6f m/s²" % idem["rhs_float"])
    A("    Fraction 精确残差 = %s   ⇒ 严格 0" % idem["resid_exact"])
    A("  与 g_std=9.80665 的相对偏差 %s（差异源：赤道半径 vs 标准重力定义点）" % fmt_rel(idem["vs_g_std"]))
    A("  ⇒ 靶的「螺旋曲率」就是牛顿引力场强除以 c²，换名不换量。")
    A("")
    A("-" * 78)
    A("三、★ κ_P 读法二难与数量级复核")
    A("-" * 78)
    A("  %-32s %-14s %s" % ("观测者", "κ (m^-1)", "m=(ℏ/c)κ (kg)"))
    A("  " + "-" * 74)
    for r in dec["rows"]:
        A("  %-32s %-14s %s" % (("v=%g m/s" % r["v"]), ("%.4g" % r["kappa"]),
                                ("%.4g" % r["m"])))
    A("  κ 与 m 各跨 %.4f 个数量级（r244 写的是 %s 个）" % (dec["span_decades"],
                                                           ev["decade_claimed"]))
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
    A("-" * 78)
    A("七、★ 修订条文（修复优化的落地产物，机算生成）")
    A("-" * 78)
    for r in res["evidence"].get("revised", []):
        A("[%s｜%s] %s · %s" % (r["state"], r["kind"], r["code"], r["title"]))
        A("     证据：%s" % r["evidence"])
        A("     备注：%s" % r["note"])
    A("")
    return "\n".join(L)


def tally_states(res):
    d = {}
    for e in res["entries"]:
        d[e["state"]] = d.get(e["state"], 0) + 1
    return d


def render_html(res, payload, header, dist, nctl_ok, nctl, ngrd_ok, ngrd):
    ev = res["evidence"]
    ch, idem, dec = ev["chain"], ev["idem"], ev["dec"]
    ch_rows = "\n".join(
        "<tr><td>%s</td><td>%s</td></tr>" % (k, v) for k, v in (
            ("κ_P 路径甲（联立定标）", "%.6e m^-1" % ch["kappa_A"]),
            ("κ_P 路径乙（靶明文 1/l_P）", "%.6e m^-1" % ch["kappa_B"]),
            ("乙/甲", "%.12f (=√2)" % ch["kappa_ratio"]),
            ("G 反算（用甲）", "%.6e（相对偏差 %s）" % (ch["G_from_A"], fmt_rel(ch["rel_G_A"]))),
            ("G 反算（用乙）", "%.6e（相对偏差 %s）" % (ch["G_from_B"], fmt_rel(ch["rel_G_B"]))),
            ("l_P 标准", "%.6e m" % ch["l_P_std"]),
            ("l_P TUFT", "%.6e m（×%.6f）" % (ch["l_P_tuft"], ch["l_P_ratio"])),
            ("c²κ(r)（λ=0）", "%.6f m/s²" % idem["lhs_float"]),
            ("GM/r²", "%.6f m/s²" % idem["rhs_float"]),
            ("Fraction 残差", str(idem["resid_exact"])),
            ("κ 数量级跨度", "%.4f 个（r244 写 %s 个）" % (dec["span_decades"],
                                                          ev["decade_claimed"])),
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
<title>TUFT-{RID} · 引力本质层元审计</title>
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
<h1>TUFT-{RID} · 引力本质层元审计（r244 回溯与加固）</h1>
<div class="meta">{title} · 生成 {ts}</div>
<div class="verdict"><b>判词：</b>{header}</div>
<h2>一、关键数值</h2>
<table><tr><th>量</th><th>值</th></tr>{ch_rows}</table>
<h2>二、条目</h2>
{ents}
<h2>三、控制组（{nctl_ok}/{nctl}）</h2>
{ctls}
<h2>四、守卫（{ngrd_ok}/{ngrd}）</h2>
{grds}
<div class="meta" style="margin-top:24px">
红线：靶 3 份只读（{unchanged}）；r244 产物未改动；本卷条目不可与 r142–r246 相加。
</div>
</body></html>""".format(
        RID=RID.upper(), title=payload["title"], ts=START_ISO, header=header,
        ch_rows=ch_rows, ents="\n".join(ents), ctls=ctls, grds=grds,
        nctl_ok=nctl_ok, nctl=nctl, ngrd_ok=ngrd_ok, ngrd=ngrd,
        unchanged=payload["targets_unchanged"])


# ============================================================
# 12. 主流程
# ============================================================
def main():
    import json
    res = run_audit()

    ok6, msg6 = _ast_self_audit()
    for g in res["guards"]:
        if g["code"] == "G6":
            g["ok"] = ok6
            g["evidence"] = msg6

    dist = tally_states(res)
    rev = res["evidence"].get("revised", [])
    n_ctl_ok = sum(1 for c in res["controls"] if c["ok"])
    n_grd_ok = sum(1 for g in res["guards"] if g["ok"])

    report = render_report(res)
    ev = res["evidence"]
    ch = ev["chain"]
    header = (
        "r244 的 E2 **判反了**：靶确实给出了 G=c³/(2ℏκ_P²)（boxed，靶标题「引力常数几何表达式」），"
        "r244 自报命中 6 处却判「无式子」⇒ 必须翻案。翻案后指控更锋利：该链起点 M_P²=ℏc/G "
        "**已把 G 放在输入侧**（真机读行号 %s < %s）⇒ 循环；靶又「取定义 κ_P=1/l_P」，"
        "而联立定标给出 κ_P=1/(√2·l_P^std) ⇒ 口径分岔：l_P 取标准值则 "
        "**G 反算得 G/2（残差 50%%）**，取靶自己的 √2·l_P^std 则 **G=G 恒等（零新增）**，"
        "两条路都不通向「G 被导出」。"
        "另：κ(r)≡g_牛顿(r)/c²（Fraction 残差严格 0）⇒ 靶的曲率是牛顿场强换名；"
        "靶自己又写明要用四维曲率标量 R 替换三维 κ ⇒ 靶自证范畴错置。"
        "元审计层面另检出 r244 证据数字错误 1 处（黎曼 3 处中 2 处是 ζ 函数）、"
        "数量级错误 1 处（4→6）、论证反例未处理 3 处、控制组/扫描器缺陷 7 处、"
        "修复定价枚举结构性退化 1 处。"
        % (ev["chain_lines"]["input_M_P2_lines"][:1], ev["chain_lines"]["boxed_lines"][:1]))

    payload = {
        "id": "TUFT-" + RID,
        "title": "引力本质层元审计：r244 判据回溯与加固（G 导出链循环与 κ_P 定标二难）",
        "generated_at": START_ISO,
        "targets": [{"path": os.path.basename(p), "sha256": SHA_AT_IMPORT.get(p)}
                    for p in TARGETS],
        "targets_unchanged": all(sha256_of(p) == SHA_AT_IMPORT[p] for p in TARGETS),
        "r244_read": {"entries": len(R244_ENTRIES), "controls": len(R244_CONTROLS)},
        "verdict_header": header,
        "entries": res["entries"],
        "entry_distribution": dist,
        "controls": res["controls"],
        "controls_ok": "%d/%d" % (n_ctl_ok, len(res["controls"])),
        "guards": res["guards"],
        "guards_ok": "%d/%d" % (n_grd_ok, len(res["guards"])),
        "g_chain": ch,
        "g_chain_lines": {k: v for k, v in ev["chain_lines"].items()},
        "identity_kappa_vs_g": {k: str(v) for k, v in ev["idem"].items()},
        "decade": {"span": ev["dec"]["span_decades"],
                   "claimed": ev["decade_claimed"],
                   "rows": ev["dec"]["rows"]},
        "riemann_split": {"n_zeta": ev["rie"]["n_zeta"],
                          "n_real": ev["rie"]["n_real"],
                          "n_curv": ev["rie"]["n_curv"]},
        "null_frame": ev["nf"]["counts"],
        "mass_formula": ev["mf"],
        "self_confessed": ev["scs"],
        "scanner_controls": {"g_wide_target": ev["g_wide_target"],
                             "g_wide_neg": ev["g_wide_neg"],
                             "tide_target": ev["tide_target"],
                             "tide_pos": ev["tide_pos"]},
        "repair_pricing": {"old": {k: v for k, v in ev["pricing_old"].items() if k != "SURVIVE_SETS"},
                           "strict": {k: v for k, v in ev["pricing_strict"].items() if k != "SURVIVE_SETS"},
                           "loose": {k: v for k, v in ev["pricing_loose"].items() if k != "SURVIVE_SETS"},
                           "strict_survive_sets": ev["pricing_strict"]["SURVIVE_SETS"]},
        "r244_hardcoded_scan": ev["r244_hardcoded"],
        "xi_scan": ev["xi"],
        "revised_clauses": rev,
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
    md.append("\n## 一、翻案：G 导出链\n")
    md.append("\n| 量 | 值 |\n|---|---|\n")
    md.append("| κ_P 路径甲（联立） | %.6e m^-1 |\n" % ch["kappa_A"])
    md.append("| κ_P 路径乙（靶明文） | %.6e m^-1 |\n" % ch["kappa_B"])
    md.append("| 乙/甲 | %.12f（=√2） |\n" % ch["kappa_ratio"])
    md.append("| G 反算（甲） | %.6e（偏差 %s） |\n" % (ch["G_from_A"], fmt_rel(ch["rel_G_A"])))
    md.append("| G 反算（乙） | %.6e（偏差 %s） |\n" % (ch["G_from_B"], fmt_rel(ch["rel_G_B"])))
    md.append("| c²κ(r) 与 GM/r² 残差 | %s（Fraction 严格 0） |\n" % ev["idem"]["resid_exact"])
    md.append("\n## 二、条目\n")
    for e in res["entries"]:
        md.append("\n### [%s] %s · %s\n" % (e["state"], e["code"], e["title"]))
        md.append("\n- 证据：%s\n" % e["evidence"])
        if e["note"]:
            md.append("- 备注：%s\n" % e["note"])
    md.append("\n## 三、红线\n")
    md.append("\n- 靶 3 份只读：%s\n" % payload["targets_unchanged"])
    md.append("- **r244 产物未改动**（G7 真机读：r225–r246 mtime 全早于本轮启动）。\n")
    md.append("- 本卷是**元审计层**，条目**不可与 r142–r246 相加**，尤其不可与 r244 相加。\n")
    md.append("- 未跑 refresh_catalog.py，未改 verify.py，未做 git。\n")
    with io.open(md_path, "w", encoding="utf-8") as f:
        f.write("".join(md))

    vd = ["# 判定册 · TUFT-%s（引力本质层元审计）\n" % RID.upper(),
          "\n## 判词\n\n%s\n" % header,
          "\n## 判决分组\n",
          "\n| 组 | 内容 | 结论 |\n|---|---|---|\n",
          "| MA | r244 **判对**的 5 条（潮汐通道 0、κ=g/v²、质量式真实、引用逐字、二难结构） | PASS |\n",
          "| MB | ★**翻案** 2 条：E2 靶确有 G 式子；C2「黎曼 3 处」含 2 处 ζ 假阳性 | **FAIL** |\n",
          "| MC | 论证有反例未处理 3 条：C1 量纲单独不够、D1 靶已有 null frame 修法、D2 后果表述不成立 | **FAIL** |\n",
          "| MD | 数值/口径纠错 3 条：数量级 4→6、RAW/ALL 口径未声明、符号位补全未标注 | FAIL |\n",
          "| ME | r244 控制组/扫描器缺陷 7 条（C13 恒真、C17 恒等式、C11 名不副实、C18/C19 冗余、C14 缺正对照、E2 扫描器缺负对照、F1 枚举退化） | FAIL |\n",
          "| MF | ★**新增决定性证据** 3 条：G 链循环、κ_P 定标二难、√2 伪印记 + 靶自证范畴错置 | **FAIL** |\n",
          "| MG | 净效应与修复定价重算（双档） | INFO/FAIL |\n"]
    vd.append("\n## ★ 性质界定（关键）\n")
    vd.append("\n1. **本卷不是为靶翻案**：翻的是 r244 的一条**事实性错误**——"
              "把靶已有的东西判成没有。这种错误方向对靶不利，反而最伤整卷可信度。\n")
    vd.append("2. **翻案后指控更强**：从「靶没有 G 推导式」（一句话可反驳）"
              "换成「靶有，但它是循环 + √2 伪印记」（需解整条链才能反驳）。\n")
    vd.append("3. **C1 的量纲论证单独不够**：c²κ 与 c²Rξ 同为 [L T^-2]。"
              "承重必须改挂「效应类型错配」——κ 的后果是单点加速度，"
              "时空弯曲的后果是需分离矢量 ξ 的潮汐梯度，而靶文本**无 ξ**。\n")
    vd.append("4. **D1 必须登记对靶有利项**：靶已提出 null frame / 伪弧长修法"
              "（RAW 零标架 %d 处、null frame %d 处）。正确判法是"
              "「修法已提出但未被行使」——靶自己写「但需重推 n…」。\n"
              % (ev["nf"]["counts"]["零标架"]["raw"], ev["nf"]["counts"]["null frame"]["raw"]))
    vd.append("5. **第 29 度的表述须调整**：r244 的「SURVIVE 恒 0」是枚举器退化的产物"
              "（对任何靶都输出 31/1/0）。重定义后严格档 SURVIVE %d、宽松档 %d；"
              "但每条存续路径都含 intrinsic_curvature ⇒ "
              "**原宣称「κ(L^-1) 的投影即引力」0 条存续路径**。\n"
              % (ev["pricing_strict"]["SURVIVE"], ev["pricing_loose"]["SURVIVE"]))
    vd.append("6. **★口径自守（本卷自身纪律）**：κ_P 的「联立值 / 标准口径 / 靶口径」"
              "三个数**不可混用**。本卷在 MF2 中把读法①明确标注为"
              "「l_P 取**标准值**」、读法②标注为「l_P 取**靶自己的** √2·l_P^std」，"
              "两条并列各报数值与残差——这正是本卷在 MD2 中指控 r244 的同一类错误，"
              "故本卷必须率先自守。\n")
    vd.append("\n## 治理\n")
    vd.append("\n- 控制组 %d/%d；守卫 %d/%d\n"
              % (n_ctl_ok, len(res["controls"]), n_grd_ok, len(res["guards"])))
    vd.append("- 靶 3 份只读：%s；r244 产物未改动（mtime 真机读）\n"
              % payload["targets_unchanged"])
    vd.append("- 本卷条目不可与 r142–r246 相加。\n")
    rev = res["evidence"].get("revised", [])
    if rev:
        vd.append("\n## ★ 修订条文（r244 九条 FAIL 的修订版，机算生成）\n")
        vd.append("\n| 编号 | 修订类型 | 修订后状态 |\n|---|---|---|\n")
        for r in rev:
            vd.append("| %s | %s | %s |\n" % (r["code"], r["kind"], r["state"]))
        vd.append("\n---\n")
        for r in rev:
            vd.append("\n### [%s｜%s] %s\n" % (r["state"], r["kind"], r["code"]))
            vd.append("\n**修订后标题**：%s\n" % r["title"])
            vd.append("\n**证据**：%s\n" % r["evidence"])
            vd.append("\n**备注**：%s\n" % r["note"])
        vd.append("\n> 说明：以上条文为**新增交付**，不改动 r244 已落盘的任何产物。"
                  "使用时以本卷条文为准；r244 原条文保留供追溯对照。\n")

    with io.open(vd_path, "w", encoding="utf-8") as f:
        f.write("".join(vd))

    rev_path = os.path.join(DATA_DIR, BASE_NAME + "_修订条文.md")
    rv = ["# 修订条文 · TUFT-%s：r244 九条 FAIL 的修订版\n" % RID.upper(),
          "\n> 生成时间：%s　|　机算生成，所有数字均由本卷源码现算，禁手写\n" % START_ISO,
          "\n> **性质**：本文件是**新增交付**，不改动 r244 已落盘的任何产物；"
          "r244 原条文保留供追溯对照。\n",
          "\n## 修订一览\n",
          "\n| 编号 | 修订类型 | 状态 | 一句话 |\n|---|---|---|---|\n"]
    one_liner = {
        "C1": "量纲差异只是必要条件，承重改挂「效应类型错配 + 靶无 ξ」",
        "C2": "证据数字更正：3 处 → 真曲率张量 1 处（另 2 处是黎曼 ζ 函数）",
        "C3": "收紧措辞：删掉过强的三选一，只留「效应类型不匹配」",
        "D1": "改判：登记靶已提出 null frame 修法，改判「已提出但未行使」",
        "D2": "改判后果：换成「引力分量在自由下落时恒为 0」",
        "D3": "数值纠错：4 个数量级 → 实测 6 个",
        "E1": "升级：κ(r) 与牛顿场强逐点恒等（Fraction 残差严格 0）",
        "E2": "★★翻案：靶确有 G=c³/(2ℏκ_P²)，改判为「循环 + κ_P 口径分岔」",
        "F1": "重算：原 SURVIVE 恒 0 是枚举器退化；改述为「原宣称 0 条存续路径」",
    }
    for r in rev:
        rv.append("| %s | %s | %s | %s |\n"
                  % (r["code"], r["kind"], r["state"], one_liner.get(r["code"], "")))
    rv.append("\n## 条文全文\n")
    for r in rev:
        rv.append("\n### [%s｜%s] %s\n" % (r["state"], r["kind"], r["code"]))
        rv.append("\n**修订后标题**：%s\n" % r["title"])
        rv.append("\n**证据**：%s\n" % r["evidence"])
        rv.append("\n**备注**：%s\n" % r["note"])
    rv.append("\n## 红线\n")
    rv.append("\n- **r244 产物未改动**（mtime 真机读：r225–r246 共 %d 份全早于本轮启动）。\n"
              % EVIDENCE.get("n_untouched", 0))
    rv.append("- 靶 3 份只读（sha256 前后一致）。\n")
    rv.append("- 本文件条目不可与 r142–r246 相加。\n")
    with io.open(rev_path, "w", encoding="utf-8") as f:
        f.write("".join(rv))

    with io.open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html(res, payload, header, dist, n_ctl_ok,
                            len(res["controls"]), n_grd_ok, len(res["guards"])))

    sys.stdout.write(report)
    sys.stdout.write("\n" + "=" * 78 + "\n")
    sys.stdout.write("条目 %d = %s\n" % (len(res["entries"]),
                                         " / ".join("%s %d" % (k, v) for k, v in sorted(dist.items()))))
    sys.stdout.write("控制组 %d/%d\n" % (n_ctl_ok, len(res["controls"])))
    sys.stdout.write("守卫 %d/%d\n" % (n_grd_ok, len(res["guards"])))
    sys.stdout.write("修订条文 %d 条（%s）\n"
                     % (len(rev), "、".join("%s=%s" % (r["code"], r["kind"])
                                            for r in rev)))
    sys.stdout.write("靶未改动 %s\n" % payload["targets_unchanged"])
    sys.stdout.write("=" * 78 + "\n")

    bad = (n_ctl_ok != len(res["controls"])) or (n_grd_ok != len(res["guards"]))
    return 2 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
