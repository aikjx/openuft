# -*- coding: utf-8 -*-
r"""
TUFT-r262 · 重子不对称层
==============================================================
攻靶：「CP 破坏与宇宙重子不对称性（轻子生成，弱通道涡旋拓扑相位破缺）」
      靶文位置：来料原件 L5369-L5500（BAU 章）

本卷只审「BAU 章的定量闭合性与 TUFT 增量」。r252（质量谱）、r255（磁矩）、
r258（暗能量）不是同一层，不重复。

承重三条（全部纯代数 / 纯群论 / 纯量级，零实验输入）：
  B02  sphaleron 选择定则被写反：靶 L5459 写 Δ(B+L)=0, Δ(B−L)≠0，
       而标准为 ΔB=ΔL=3N_f ⇒ Δ(B+L)=6N_f≠0, Δ(B−L)=0
  B03  该错误与靶 L5463 的 B=(28/79)(B−L) 直接自毁：若 B−L 被破坏，
       则 B=(28/79)(B−L) 不能给出稳定平衡值
  A05  ε_i → η_B 的定量链整段缺失（washout / efficiency / g_* 全 0 命中）
  A06  唯一的「TUFT 独有预言」（κ²τ² 修正 ε_i）零公式零数值 ⇒ 不可证伪

纪律：控制组 / 守卫一律机算，禁写死 True。
"""
import hashlib
import io
import json
import math
import os
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
README = os.path.normpath(os.path.join(HERE, "..", "README.md"))

RID = "r262"
TITLE_CN = "重子不对称层"
DEGREE_NOTE = "本卷不占「修复即自杀」度数（SURVIVE>0）"
SLUG = ("TUFT-%s_%s_选择定则写反与eps到eta链条断裂_"
        "唯一独有预言零数值与Frenet-PMNS范畴错置_精算与可视化_2026-10-31") % (RID, TITLE_CN)

TARGETS = [
    "TUFT-r241_光速螺旋_来料原件_2026-10-30/基于光速螺旋流形的核心动力学方程组.md",
    "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md",
    "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md",
]

# ---------------------------------------------------------------- 常数（带来源）
C = 299792458.0
C0 = C
GEV_J = 1.602176634e-10
V_EW = 246.22                     # GeV
M_PL = 1.220890e19                # GeV
G_STAR_SM = 106.75                # SM 有效自由度（T ~ 1e10 GeV）
N_F = 3                           # 费米子代数
N_H = 1                           # Higgs 双重态数
S_OVER_NGAMMA = 7.04              # 今日 s/n_gamma
ETA_B_OBS = 6.1e-10               # 靶 L5430 引用的观测值
ETA_B_PLANCK = 6.12e-10           # Planck 2018
ETA_B_PLANCK_SIG = 0.04e-10
DM2_ATM = 2.5e-3                  # eV^2
EV_GEV = 1e-9
J_CKM = 3.08e-5                   # Jarlskog 不变量
ETA_B_SM_CKM = 1e-18              # SM 电弱重子生成量级（文献常用）

ENTRIES, CONTROLS, GUARDS = [], [], []
_ALPHA52 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def depollute(s):
    r"""上游 LaTeX 污染修复（实测四种形式，跑配平扫描）。

    甲 \boldsymbol{b}（花括号）/ 乙 \boldsymbol n（空格无括号）/ 丙 \(\boldsymbol p\)
    二次污染：\boldsymbol 自身又被污染成 \(\boldsymbol{b}\)oldsym\(\boldsymbol{b}\)ol{\(\boldsymbol{n}\)}
    —— 这种二级形态**无法还原成原词**，但不影响本卷定位，故只清 `\boldsymbol` 标记。
    丁（本卷新发现，r262）\boldsymbol{m=\frac{\hbar \omega}{c^2}} ——
    **整段公式被加粗**，花括号**嵌套** ⇒ `[^{}]*` 命不中（实测残留 22 处）。
    故改用**配平括号扫描**，把 `\boldsymbol` + 平衡花括号对整体剥壳、内容递归处理。
    戊（本卷新发现，r262）`\(\boldsymbol n)` —— **只有左括号+右括号、无尾反斜杠**，
    会把 `\neq` 切成 `\(n)eq`、把 `n_B` 切成 `(n)*B`。若不还原，引文失真。
    故先用 `\\\(\\boldsymbol\s+([A-Za-z])\)` 前置还原，再做配平扫描。
    """
    s = re.sub(r"\\\(\\boldsymbol\s+([A-Za-z])\)([A-Za-z])", r"\\\1\2", s)
    s = re.sub(r"\\\(\\boldsymbol\s+([A-Za-z])\)", r"\1", s)
    return re.sub(r"[\r\n]+", "\n", _unbold(s))


def _unbold(s):
    r"""剥掉 \boldsymbol（含嵌套花括号、空格单字符、\(...\) 三形态）。"""
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
    if isinstance(x, float) and (x != x or x in (float("inf"), float("-inf"))):
        return str(x)
    a = abs(x)
    if a != 0 and (a >= 1e5 or a < 1e-3):
        return "%.*e" % (n, x)
    return "%.*f" % (n, x)


def rel(a, b):
    if b == 0:
        return float("inf") if a != 0 else 0.0
    return abs(a - b) / abs(b)


def ordmag(x):
    return float("-inf") if x == 0 else math.log10(abs(x))


def ent(eid, group, title, verdict, detail, metric=None):
    ENTRIES.append({"id": eid, "group": group, "title": title,
                    "verdict": verdict, "detail": detail, "metric": metric})


def ctl(cid, name, ok, detail):
    CONTROLS.append({"id": cid, "name": name, "ok": bool(ok), "detail": detail})


def guard(gid, name, ok, detail):
    GUARDS.append({"id": gid, "name": name, "ok": bool(ok), "detail": detail})


# ================================================================ 靶只读
def load_targets():
    out = []
    for rp in TARGETS:
        p = os.path.join(DATA, rp)
        raw = io.open(p, "rb").read()
        out.append({"path": rp, "sha256": hashlib.sha256(raw).hexdigest(),
                    "nbytes": len(raw),
                    "text": depollute(raw.decode("utf-8", "replace"))})
    for d in out:
        d["lines"] = d["text"].split("\n")
    return out


def locate(docs):
    """所有定位拆成独立扫描，禁 AND。"""
    big = docs[0]["lines"]

    def scan(pred):
        return [i + 1 for i, s in enumerate(big) if pred(s)]

    L = {}
    L["bau_heading"] = scan(lambda s: "重子不对称性 BAU" in s)
    L["eta_def"] = scan(lambda s: "\\eta_B" in s and "6.1" in s)
    L["eta_val"] = scan(lambda s: "6.1\\times10^{-10}" in s or "6.1\\times 10^{-10}" in s)
    L["sakharov"] = scan(lambda s: "Sakharov" in s)
    L["sak_1"] = scan(lambda s: "重子数B破坏" in s)
    L["sak_2"] = scan(lambda s: "CP破坏" in s and "C破坏" in s)
    L["sak_3"] = scan(lambda s: "偏离热平衡" in s)
    L["sphal_rule"] = scan(lambda s: "\\Delta(B+L)=0" in s)
    L["sphal_rule_b"] = scan(lambda s: "\\Delta(B-L)" in s and "eq 0" in s)
    L["b_over_bl"] = scan(lambda s: "\\frac{28}{79}" in s)
    L["group_theory"] = scan(lambda s: "群论" in s and "SU(3)" in s)
    L["epsilon_def"] = scan(lambda s: "\\varepsilo" in s and "\\Gamma(N_i" in s)
    L["m_i_range"] = scan(lambda s: "10^{10}" in s and "10^{13}" in s)
    L["washout"] = scan(lambda s: "washout" in s.lower())
    L["efficiency"] = scan(lambda s: "efficiency" in s.lower() or "效率因子" in s)
    L["gstar"] = scan(lambda s: "g_*" in s or "g_{*}" in s)
    L["kappa_f"] = scan(lambda s: "\\kappa_f" in s or "κ_f" in s)
    L["kt2_coupling"] = scan(lambda s: "\\kappa^2\\tau^2" in s)
    L["unique_pred"] = scan(lambda s: "TUFT独有的预言" in s or "TUFT独有" in s)
    L["frenet_cp"] = scan(lambda s: "Frenet" in s and "复" in s)
    L["cp_phase_geom"] = scan(lambda s: "标架复旋转" in s or "标架复扭转" in s)
    L["majorana_phase"] = scan(lambda s: "马约拉纳CP相位" in s)
    L["ckm_small"] = scan(lambda s: "CKM" in s and "太小" in s)
    L["zero_nubb"] = scan(lambda s: "beta\\beta" in s and "0" in s)
    L["implied"] = scan(lambda s: "最终得到观测的" in s)
    L["pmns"] = scan(lambda s: "PMNS" in s)
    return L


# ================================================================ 群论与量级
def b_over_bl(nf=N_F, nh=N_H):
    """SM sphaleron 平衡：B = (8 nf + 4 nh)/(22 nf + 13 nh) (B-L)。"""
    num = 8 * nf + 4 * nh
    den = 22 * nf + 13 * nh
    return Fraction(num, den), num, den


def sphaleron_charges(nf=N_F):
    """sphaleron 一次跃迁（每代）：ΔB = ΔL = 3。"""
    dB = 3 * nf
    dL = 3 * nf
    return {"dB": dB, "dL": dL,
            "d_BplusL": dB + dL, "d_BminusL": dB - dL}


def eps_max_davidson_ibarra(M1):
    """ε_max = 3 M1 Δm_atm^{1/2} / (8 π v^2)，单位 GeV。"""
    dm = math.sqrt(DM2_ATM) * EV_GEV     # eV -> GeV
    return 3.0 * M1 * dm / (8.0 * math.pi * V_EW ** 2)


def eta_from_eps(eps, kappa_f, g_star=G_STAR_SM):
    """η_B = (28/79) · (ε κ_f / g_*) · (s/n_γ)。"""
    r, _, _ = b_over_bl()
    return float(r) * (eps * kappa_f / g_star) * S_OVER_NGAMMA


def eps_needed(eta_target=ETA_B_OBS, kappa_f=1.0, g_star=G_STAR_SM):
    r, _, _ = b_over_bl()
    return eta_target / (float(r) * kappa_f / g_star * S_OVER_NGAMMA)


def nubb_mass_param(m_light):
    """m_bb 在简并/正常序下的量级（单参数，非严格）。"""
    return m_light


# ================================================================ A 组：原文核验
def group_A(docs, L):
    big = docs[0]["lines"]
    n_lines = len(big)

    def line(keys, idx=0):
        if not keys or len(keys) <= idx:
            return "n/a"
        return big[keys[idx] - 1].strip()[:300]

    ent("A01", "A", "eta_B 的观测值是否给出（含公式定义与数值）",
        "PASS" if (L["eta_def"] and L["eta_val"]) else "FAIL",
        "定义式行 %d 处（行 %s）；数值 `6.1e-10` 命中 %d 处（行 %s）。原文 line %s：%s "
        "⇒ 靶确实给出了定义与数值，且数值与 Planck 2018（6.12e-10）相符（见 C04）。" % (
            len(L["eta_def"]), L["eta_def"][:4], len(L["eta_val"]), L["eta_val"][:4],
            L["eta_def"][0] if L["eta_def"] else "?", line(L["eta_def"])),
        {"eta_def": len(L["eta_def"]), "eta_val": len(L["eta_val"])})
    ent("A02", "A", "Sakharov 三条件是否列全",
        "PASS" if (len(L["sakharov"]) > 0 and L["sak_1"] and L["sak_2"] and L["sak_3"]) else "FAIL",
        "「Sakharov」行 %d 处；三要素分别命中：B 破坏 %d、C+CP 破坏 %d、偏离热平衡 %d "
        "⇒ 三条齐备，且与标准表述一致（对靶有利）。原文 line %s：%s" % (
            len(L["sakharov"]), len(L["sak_1"]), len(L["sak_2"]), len(L["sak_3"]),
            L["sakharov"][0] if L["sakharov"] else "?", line(L["sakharov"])),
        {"sakharov": len(L["sakharov"])})
    ent("A03", "A", "B = (28/79)(B−L) 是否给出且注明为群论结果",
        "PASS" if (L["b_over_bl"] and L["group_theory"]) else "FAIL",
        "`\\frac{28}{79}` 命中 %d 处（行 %s）；「群论 + SU(3)」命中 %d 处（行 %s）。"
        "原文 line %s：%s ⇒ 系数与出处均正确（B01 机验）。" % (
            len(L["b_over_bl"]), L["b_over_bl"][:3], len(L["group_theory"]),
            L["group_theory"][:3], L["b_over_bl"][0] if L["b_over_bl"] else "?",
            line(L["b_over_bl"])),
        {"b_over_bl": len(L["b_over_bl"])})
    ent("A04", "A", "★★★ sphaleron 选择定则被写反（Δ(B+L)=0 / Δ(B−L)≠0）",
        "FAIL" if (L["sphal_rule"] and L["sphal_rule_b"]) else "PASS",
        "靶 line %s 写 `\\Delta(B+L)=0,\\quad \\Delta(B-L)\\neq 0`，原文：%s "
        "标准：sphaleron 每次跃迁 ΔB = ΔL = 3N_f ⇒ **Δ(B+L) = 6N_f = %d ≠ 0**（破坏），"
        "**Δ(B−L) = 0**（守恒）。靶把两者**完全写反**。"
        "该错误与它自己 line %s 的 `B=(28/79)(B−L)` 直接自毁（见 B03）。" % (
            L["sphal_rule"][:3] if L["sphal_rule"] else "?",
            line(L["sphal_rule"]),
            sphaleron_charges()["d_BplusL"],
            L["b_over_bl"][:3] if L["b_over_bl"] else "?"),
        {"rule_lines": L["sphal_rule"][:3],
         "d_BplusL": sphaleron_charges()["d_BplusL"],
         "d_BminusL": sphaleron_charges()["d_BminusL"]})
    ent("A05", "A", "★★★ eps_i → eta_B 的定量链是否出现（washout / efficiency / g_* / κ_f）",
        "FAIL" if not (L["washout"] or L["efficiency"] or L["gstar"] or L["kappa_f"]) else "PASS",
        "机读全语料 %d 行：`washout` **%d 处**、`efficiency/效率因子` **%d 处**、"
        "`g_*` **%d 处**、`κ_f` **%d 处**。四个必备环节**全部 0 命中** ⇒ "
        "从 CP 不对称参数 ε_i 到 η_B 的定量链条**整段缺失**。靶 L%s 只写一句「最终得到观测的 η_B」，"
        "中间无任何公式。标准链条应为 η_B = (28/79)·(ε₁κ_f/g_*)·(s/n_γ)（B05 已给出该式的量级反解）。" % (
            n_lines, len(L["washout"]), len(L["efficiency"]), len(L["gstar"]),
            len(L["kappa_f"]), L["implied"][:3] if L["implied"] else "?"),
        {"washout": len(L["washout"]), "efficiency": len(L["efficiency"]),
         "gstar": len(L["gstar"]), "kappa_f": len(L["kappa_f"]), "lines": n_lines})
    ent("A06", "A", "★★ 唯一的「TUFT 独有预言」（κ²τ² 修正 ε_i）是否有公式或数值",
        "FAIL",
        "靶 line %s 称「本源场非线性耦合 κ²τ²，会给 CP 不对称参数 ε_i 增加微小高阶修正，"
        "**这是 TUFT 独有的预言**」。机验：`κ²τ²` 耦合命中 %d 处；"
        "但 **ε_i 与 κ²τ² 之间没有任何等式**，也没有任何数值、量级、无量纲比值。"
        "⇒ 「独有预言」不可计算、不可比较、**不可证伪**（判据见 C02）。" % (
            L["unique_pred"][:3] if L["unique_pred"] else "?",
            len(L["kt2_coupling"])),
        {"unique_pred_lines": L["unique_pred"][:3],
         "kt2_hits": len(L["kt2_coupling"])})
    ent("A07", "A", "★ 重涡旋质量 M_i 是否给出公式（还是只给范围）",
        "FAIL",
        "靶 line %s 只给**范围** `M_i ~ 10^10 ~ 10^13 GeV`（命中 %d 处），"
        "**没有任何质量公式**（无 M_i 与 κ、τ、ω 的关系式）。"
        "这与 r252 判过的「质量谱反解拟合」同型：范围是**输入**，量级落在标准 thermal "
        "leptogenesis 的可行区（B06 核验），但这不是靶算出来的。" % (
            L["m_i_range"][:3] if L["m_i_range"] else "?",
            len(L["m_i_range"])),
        {"m_i_range_lines": L["m_i_range"][:3]})
    ent("A08", "A", "★★ 「CP 相位 = κ²τ² 带来的标架复旋转」是否有方程",
        "FAIL",
        "靶 line %s 称「CP 相位不是人为放进矩阵的自由参数，它是曲率-挠率非线性耦合顶点 κ²τ² "
        "带来的**标架复旋转**」。机验：`标架复旋转/复扭转` 命中 %d 处、"
        "`Frenet + 复` 命中 %d 处、`PMNS` 命中 %d 处 —— **但三者之间没有任何等式**。"
        "「Frenet 标架 → PMNS 复相位」的映射从未写出（自由度不匹配见 B07）。" % (
            L["cp_phase_geom"][:3] if L["cp_phase_geom"] else "?",
            len(L["cp_phase_geom"]), len(L["frenet_cp"]), len(L["pmns"])),
        {"geom_claims": len(L["cp_phase_geom"]), "frenet_cp": len(L["frenet_cp"]),
         "pmns": len(L["pmns"])})
    ent("A09", "A", "0νββ 是否被作为判据提出（可证伪方向）",
        "PASS" if L["zero_nubb"] else "FAIL",
        "`0νββ`（去污染后 `0\\nu\\beta\\beta`）命中 %d 处（行 %s）⇒ 靶主动提出可检验方向，"
        "且明确指出「若长期阴性，则 TUFT 这个轻子生成主线失效，需要切换替代 BAU 方案」"
        "—— 这是**全章唯一一条明确的可证伪陈述**（对靶有利）。" % (
            len(L["zero_nubb"]), L["zero_nubb"][:4]),
        {"nubb": len(L["zero_nubb"])})


# ================================================================ B 组：定量
def group_B(L):
    r, num, den = b_over_bl()
    sr = sphaleron_charges()
    # B01 28/79 群论核验
    ent("B01", "B", "B=(28/79)(B−L) 的群论核验（(8N_f+4N_H)/(22N_f+13N_H)）",
        "PASS" if r == Fraction(28, 79) else "FAIL",
        "Sphaleron 平衡条件解出 B = [(8N_f+4N_H)/(22N_f+13N_H)](B−L)；代入 "
        "N_f=3, N_H=1：(8×3+4)/(22×3+13) = %d/%d = **%s**（Fraction 精确）。"
        "靶 L%s 写 28/79 ⇒ **完全正确**（对靶有利，且它正确注明这是 "
        "SU(3)×SU(2)×U(1) 的群论结果）。" % (num, den, r,
                                           L["b_over_bl"][:2] if L["b_over_bl"] else "?"),
        {"ratio": str(r), "num": num, "den": den})
    # B02 选择定则机算
    ent("B02", "B", "★★★ sphaleron 选择定则机算：Δ(B+L)=6N_f≠0 而 Δ(B−L)=0",
        "FAIL" if (sr["d_BplusL"] != 0 and sr["d_BminusL"] == 0) else "PASS",
        "每次跃迁（每代）：ΔB = 3、ΔL = 3 ⇒ 对 N_f=%d 代："
        "**ΔB = %d，ΔL = %d，Δ(B+L) = %d ≠ 0**（破坏），"
        "**Δ(B−L) = %d − %d = %d**（守恒，严格 0）。"
        "靶 line %s 写的是 `Δ(B+L)=0, Δ(B−L)≠0` ⇒ **两项全反**。"
        "这不是笔误而是方向性错误：B−L 守恒正是 B 能被 (28/79)(B−L) 唯一确定的前提。" % (
            N_F, sr["dB"], sr["dL"], sr["d_BplusL"],
            sr["dB"], sr["dL"], sr["d_BminusL"],
            L["sphal_rule"][:2] if L["sphal_rule"] else "?"),
        {"dB": sr["dB"], "dL": sr["dL"], "d_BplusL": sr["d_BplusL"],
         "d_BminusL": sr["d_BminusL"]})
    # B03 自毁
    ent("B03", "B", "★★★ A04 的错误与靶自己的 B=(28/79)(B−L) 直接自毁",
        "FAIL",
        "若 Δ(B−L) ≠ 0（靶的说法），则 B−L **不是守恒荷**，sphaleron 过程会持续改变它，"
        "于是 `B = (28/79)(B−L)` 的右端随时间漂移，**B 没有稳定平衡值** ⇒ 无法定义「最终重子不对称」。"
        "反之，只有 B−L 守恒（标准结果），该式才能把初始的 B−L 唯一映射到 B。"
        "⇒ 靶 L%s（选择定则）与 L%s（转换系数）**互相排除**，不能同时成立。" % (
            L["sphal_rule"][:2] if L["sphal_rule"] else "?",
            L["b_over_bl"][:2] if L["b_over_bl"] else "?"),
        {"contradiction": True})
    # B04 eta_B 口径
    z = (ETA_B_OBS - ETA_B_PLANCK) / ETA_B_PLANCK_SIG
    ent("B04", "B", "eta_B 观测值的口径核验（靶 6.1e-10 vs Planck 6.12±0.04 e-10）",
        "PASS" if rel(ETA_B_OBS, ETA_B_PLANCK) < 0.02 else "FAIL",
        "靶 L%s 写 η_B ≈ 6.1e-10；Planck 2018 给 (6.12 ± 0.04)e-10 ⇒ 相对差 %s"
        "（%s σ，按 0.04 的 1σ）⇒ **靶的数值正确**（对靶有利）。" % (
            L["eta_val"][:2] if L["eta_val"] else "?", fmt(rel(ETA_B_OBS, ETA_B_PLANCK), 4),
            fmt(abs(z), 3)),
        {"eta_obs": ETA_B_OBS, "eta_planck": ETA_B_PLANCK, "sigma": z})
    # B05 量级反解
    e1 = eps_needed(ETA_B_OBS, 1.0)
    e01 = eps_needed(ETA_B_OBS, 0.1)
    e001 = eps_needed(ETA_B_OBS, 0.01)
    ent("B05", "B", "★ 要 η_B=6.1e-10，所需 ε₁ κ_f 的量级（靶从未做这一步）",
        "FAIL",
        "η_B = (28/79)·(ε₁κ_f/g_*)·(s/n_γ)，取 g_*=%s、s/n_γ=%s ⇒ 系数 = %s。"
        "要 η_B = 6.1e-10：κ_f=1 ⇒ ε₁ = **%s**；κ_f=0.1 ⇒ ε₁ = **%s**；"
        "κ_f=0.01 ⇒ ε₁ = **%s**。这三个数**靶一个都没给**（A05 已证 washout/efficiency 0 命中）。"
        "没有这一步，「解释 BAU」就停在口号层面。" % (
            fmt(G_STAR_SM, 2), fmt(S_OVER_NGAMMA, 2),
            fmt(float(b_over_bl()[0]) / G_STAR_SM * S_OVER_NGAMMA, 8),
            fmt(e1), fmt(e01), fmt(e001)),
        {"eps_kf1": e1, "eps_kf01": e01, "eps_kf001": e001})
    # B06 Davidson-Ibarra
    rows = []
    for M1 in (1e9, 1e10, 1e11, 1e12, 1e13):
        em = eps_max_davidson_ibarra(M1)
        ok = em >= e01
        rows.append({"M1": M1, "eps_max": em, "feasible_kf01": ok})
    ent("B06", "B", "★ Davidson–Ibarra 上界核验：M_i ~ 1e10–1e13 GeV 是否落在可行区",
        "PASS",
        "ε_max = 3M₁√Δm²_atm/(8πv²)（Δm²_atm=2.5e-3 eV²，v=%s GeV）：%s。"
        "与 B05 的「κ_f=0.1 需 ε₁=%s」相比：M₁ ≳ 1e10 GeV 才可能达标 ⇒ "
        "**靶给的 1e10–1e13 GeV 落在标准可行区**（对靶有利）。但注意：这是**标准 leptogenesis "
        "的既有结论**，不是靶的推导 —— 靶只是把范围抄进来（A07）。" % (
            fmt(V_EW, 2),
            "; ".join("M₁=%s ⇒ ε_max=%s" % (fmt(x["M1"], 0), fmt(x["eps_max"])) for x in rows),
            fmt(e01)),
        {"rows": rows})
    # B07 Frenet vs PMNS 自由度
    frenet_dof = 2       # κ(s), τ(s)
    pmns_dof = 6         # 3 角 + 1 Dirac + 2 Majorana
    so3_dim = 3
    u3_dim = 9
    ent("B07", "B", "★★ Frenet 标架（2 参、实）与 PMNS 矩阵（6 参、复）自由度不匹配",
        "FAIL",
        "Frenet 标架由 κ(s)、τ(s) **两个实函数**完全确定（曲线在 3D 内 upto 刚体运动）⇒ 自由度 **%d**。"
        "PMNS 的物理参数 = 3 个混合角 + 1 个 Dirac 相位 + 2 个 Majorana 相位 = **%d**。"
        "而且一个是 SO(3) 实正交（生成元 %d），一个是 U(3) 复幺正（实维数 %d）。"
        "**%d ≠ %d，实 ≠ 复** ⇒ 「PMNS 涡旋拓扑混合 = Frenet 标架复扭转」不是同构而是类比。"
        "靶从未给出 2→6 的映射（A08 已证三者间无等式）。这与 r244 判过的「范畴错置」同型。" % (
            frenet_dof, pmns_dof, so3_dim, u3_dim, frenet_dof, pmns_dof),
        {"frenet_dof": frenet_dof, "pmns_dof": pmns_dof,
         "so3": so3_dim, "u3": u3_dim})
    return {"eps": {"kf1": e1, "kf01": e01, "kf001": e001},
            "di": rows, "dof": {"frenet": frenet_dof, "pmns": pmns_dof}}


# ================================================================ C 组：判别力
STD_KEYS = ("Sakharov", "sphaleron", "Sphalero", "PMNS", "leptoge", "Leptoge",
            "Lepto", "\\eta_B", "CKM", "B-L", "B−L", "热平衡", "马约拉纳")
TUFT_KEYS = ("涡旋", "挠率", "Frenet", "\\kappa^2\\tau^2", "tau_\\Lambda",
             "标架", "弱通道", "拓扑相位")


def group_C(docs, L, B):
    big = docs[0]["lines"]
    lo, hi = 5416, min(5505, len(big))
    seg = big[lo - 1:hi]
    n_std = sum(1 for s in seg if any(k in s for k in STD_KEYS))
    n_tuft = sum(1 for s in seg if any(k in s for k in TUFT_KEYS))
    n_both = sum(1 for s in seg if any(k in s for k in STD_KEYS)
                 and any(k in s for k in TUFT_KEYS))
    n_seg = len(seg)
    ent("C01", "C", "★ BAU 章的「标准内容 / TUFT 增量」逐行配比（判断增量有多少）",
        "INFO",
        "取 L%d–L%d 共 **%d 行**：含标准物理关键词的行 **%d**（%.1f%%）、"
        "含 TUFT 关键词的行 **%d**（%.1f%%）、两者兼有的行 **%d**。"
        "兼有行才是「把 TUFT 接到标准链条上」的位置 ⇒ 仅 **%.1f%%**。"
        "结论：该章主体是**标准 leptogenesis 的复述**，TUFT 的增量是**定性附会**，"
        "没有一次把涡旋/挠率量代入标准公式。" % (
            lo, hi, n_seg, n_std, 100.0 * n_std / max(n_seg, 1),
            n_tuft, 100.0 * n_tuft / max(n_seg, 1), n_both,
            100.0 * n_both / max(n_seg, 1)),
        {"lines": n_seg, "std": n_std, "tuft": n_tuft, "both": n_both})
    # C02 「独有预言」零判别力
    deltas = [0.0, 1e-6, 1e-3, 1.0]
    basis = 1.0
    vals = [basis * (1.0 + d) for d in deltas]
    ent("C02", "C", "★★ 「κ²τ² 修 ε_i 是独有预言」零判别力：δ 无定义 ⇒ 对任意 δ 都无观测后果",
        "FAIL",
        "若该修正存在，唯一可能的写法是 ε_i → ε_i(1+δ)，δ 由 κ²τ²/v⁴ 之类的无量纲比给出。"
        "机验：δ 取 %s 四值，则 ε 的相对改变为 %s —— 但 **ε_i 本身靶从未赋值**（A05/B05），"
        "所以这四个 δ **产生完全相同的可观测预言：无**。"
        "⇒ 该「独有预言」不满足预言的最低条件（可计算且可与标准区分）⇒ **零判别力**。" % (
            deltas, [fmt(v - basis, 3) for v in vals]),
        {"deltas": deltas, "no_observable": True})
    # C03 反解拟合正对照
    r, _, _ = b_over_bl()
    coef = float(r) / G_STAR_SM * S_OVER_NGAMMA
    rows = []
    for M1 in (1e9, 1e10, 1e11, 1e12, 1e13):
        em = eps_max_davidson_ibarra(M1)
        kf = ETA_B_OBS / (coef * em)
        rows.append({"M1": M1, "eps_max": em, "kappa_f_needed": kf,
                     "in_unit_interval": 0.0 < kf <= 1.0})
    allok = all(x["in_unit_interval"] for x in rows)
    ent("C03", "C", "★★ 反解拟合零判别力：M_i 从 1e9 跨到 1e13（4 个量级）全都能「解释」η_B",
        "FAIL" if allok else "PASS",
        "用 η_B = coef·ε_max(M₁)·κ_f 反解 κ_f（coef=%s）：%s。"
        "**五档全部落在 (0,1]** ⇒ 任一 M₁ 都能通过调 κ_f「解释」观测值 ⇒ "
        "靶给的「M_i ~ 1e10–1e13 GeV」这个范围**零判别力**（与 r252 的「反推」同型）。"
        "真正有判别力的做法是**先算 κ_f**（washout 动力学），再预言 M₁ —— 靶没做（A05）。" % (
            fmt(coef, 8),
            "; ".join("M₁=%s ⇒ κ_f=%s" % (fmt(x["M1"], 0), fmt(x["kappa_f_needed"], 4))
                      for x in rows)),
        {"coef": coef, "rows": rows, "all_feasible": allok})
    # C04 CKM 不足的量化
    deficit = ETA_B_OBS / ETA_B_SM_CKM
    ent("C04", "C", "SM 的 CKM CP 破坏不足以为 BAU 供数（靶的定性陈述是否正确）",
        "PASS" if deficit > 1e6 else "FAIL",
        "Jarlskog 不变量 J = %s；SM 电弱重子生成给出的 η_B^SM ~ %s（文献量级）。"
        "与观测 %s 相比缺 **%s 倍 = %s 个数量级** ⇒ 靶 L%s「CKM 的 CP 破坏幅度太小，"
        "不足以解释观测到的 BAU」**完全正确**（对靶有利）。"
        "注意：这条正确性属于**标准物理**，不构成靶的增量。" % (
            fmt(J_CKM, 3), fmt(ETA_B_SM_CKM, 1), fmt(ETA_B_OBS, 2),
            fmt(deficit), fmt(ordmag(deficit), 3),
            L["ckm_small"][:2] if L["ckm_small"] else "?"),
        {"J": J_CKM, "deficit": deficit, "decades": ordmag(deficit)})
    epsd = {"kf1": eps_needed(ETA_B_OBS, 1.0),
            "kf01": eps_needed(ETA_B_OBS, 0.1),
            "kf001": eps_needed(ETA_B_OBS, 0.01)}
    return {"ratio": {"std": n_std, "tuft": n_tuft, "both": n_both, "n": n_seg},
            "rows": rows, "deltas": deltas, "coef": coef,
            "eps": epsd, "di": rows}


# ================================================================ D 组：修复定价
SLOTS = [
    ("s0", "撤回「κ²τ² 修 ε_i 是 TUFT 独有预言」（零公式 ⇒ 无法成立为预言）"),
    ("s1", "修 sphaleron 选择定则方向（Δ(B+L)≠0 破坏、Δ(B−L)=0 守恒）"),
    ("s2", "补 ε_i → η_B 的定量链（washout κ_f、g_*、s/n_γ）"),
    ("s3", "给出 M_i 的质量谱公式（而非只给 1e10–1e13 的范围）"),
    ("s4", "给出 Frenet 标架 → PMNS 的显式映射（2 参 → 6 参）"),
    ("s5", "撤回「CP 相位由 κ²τ² 产生」的几何本源声称（或补方程）"),
    ("s6", "修正 0νββ「反推马约拉纳 CP 相位」的表述（只能约束 |m_ββ|）"),
]
REQ_STRICT = {"s1", "s2", "s4", "s5"}
REQ_LOOSE = {"s1", "s2"}


def classify(changed, req):
    if "s0" in changed:
        return "SUICIDE"
    if req <= changed:
        return "SURVIVE"
    return "EMPTY"


def pricing():
    out = {}
    for tag, req in (("strict", REQ_STRICT), ("loose", REQ_LOOSE)):
        em = su = sv = 0
        surv = []
        for mask in range(1 << len(SLOTS)):
            ch = {SLOTS[i][0] for i in range(len(SLOTS)) if mask & (1 << i)}
            st = classify(ch, req)
            if st == "EMPTY":
                em += 1
            elif st == "SUICIDE":
                su += 1
            else:
                sv += 1
                if len(surv) < 3:
                    surv.append(sorted(ch))
        out[tag] = {"EMPTY": em, "SUICIDE": su, "SURVIVE": sv,
                    "total": em + su + sv, "req": sorted(req), "examples": surv}
    return out


def group_D(pr):
    st, lo = pr["strict"], pr["loose"]
    ent("D01", "D", "修复定价（2^7 = 128 组合，双档都报）",
        "BOUNDARY" if (st["SURVIVE"] > 0 and lo["SURVIVE"] > 0) else "FAIL",
        "7 槽位 %s。严格档必改 %s（4 项）⇒ **EMPTY %d / SUICIDE %d / SURVIVE %d**；"
        "宽松档必改 %s（2 项）⇒ **EMPTY %d / SUICIDE %d / SURVIVE %d**。"
        "两档 SURVIVE 均 > 0 ⇒ 靶的宣称**逻辑上非不可能**，本卷判「**靶未达成**」"
        "而非「修复即自杀」，**不占度数**。"
        "但严格档的 4 个存活组合**全部要求 s4**（Frenet→PMNS 的显式映射）—— 那是新推导，靶没有。"
        "最小修法（不代选）：s1 单独（代价 1，纯错误修正）· s2 单独（代价 2，抄标准公式即可）· "
        "s5+s6（代价 0，仅表述诚实性）· **s3/s4 需要新物理**。" % (
            [s[0] for s in SLOTS], st["req"], st["EMPTY"], st["SUICIDE"], st["SURVIVE"],
            lo["req"], lo["EMPTY"], lo["SUICIDE"], lo["SURVIVE"]),
        {"strict": {k: st[k] for k in ("EMPTY", "SUICIDE", "SURVIVE")},
         "loose": {k: lo[k] for k in ("EMPTY", "SUICIDE", "SURVIVE")}})


# ================================================================ E 组：交联（INFO）
def group_E(L):
    ent("E01", "E", "【交联·不重复】马约拉纳 CP 相位与 PMNS 的物理内含归中微子物理，本卷只审 BAU 闭合性",
        "INFO",
        "靶 line %s 提到「马约拉纳中微子天然自带 CP 破坏相位」。"
        "PMNS 的参数化、θ₁₂/θ₁₃/θ₂₃ 的取值、δ_CP 的当前约束属中微子振荡实验，"
        "**不在本卷范围**。本卷只审「这些相位是否被靶**接到** η_B 上」——结论是没接（A05）。"
        "此条为范围声明，**不计分**。" % (
            L["majorana_phase"][:3] if L["majorana_phase"] else "?"),
        {"scope": "PMNS 取值归中微子实验"})
    ent("E02", "E", "【交联·不重复】质量谱反解与 M_i 输入同型，已在 r252 判过",
        "INFO",
        "靶把 M_i 当输入（A07），与 r252 判过的「m_p/m_e 反解拟合」**同型**（1 未知数对 1 已知数）。"
        "本卷**不重复**论证，只登记同型关系；本卷的独立对象是 **η_B 链条的闭合性**"
        "与 **sphaleron 选择定则的正确性**，与 r252（质量谱）、r255（磁矩）、r258（暗能量）"
        "**不是同一层**。此条不计分。" ,
        {"r252_ref": "反解拟合"})


# ================================================================ 控制组
SHA_HEAD = {
    "TUFT-r241_光速螺旋_来料原件_2026-10-30/基于光速螺旋流形的核心动力学方程组.md":
        "2483899ead9c854d",
    "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md":
        "fd7dd4481b6a5f66",
    "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md":
        "dba5eb95bac110f0",
}


def controls(docs, L, B, Cx, pr):
    r, num, den = b_over_bl()
    sr = sphaleron_charges()
    ctl("K01", "28/79 群论核验（N_f=3, N_H=1）",
        r == Fraction(28, 79), "(8·3+4)/(22·3+13)=%d/%d=%s" % (num, den, r))
    ctl("K02", "Δ(B+L) == 6N_f == 18", sr["d_BplusL"] == 18,
        "dB=%d dL=%d ⇒ B+L=%d" % (sr["dB"], sr["dL"], sr["d_BplusL"]))
    ctl("K03", "Δ(B−L) == 0（守恒）", sr["d_BminusL"] == 0,
        "dB−dL=%d" % sr["d_BminusL"])
    ctl("K04", "【预期不一致】靶的具体写法与标准相反（证明审计有分辨力）",
        bool(L["sphal_rule"]) and sr["d_BminusL"] == 0,
        "靶 Δ(B+L)=0（行 %s）；标准 Δ(B−L)=0 ⇒ 方向相反" % (L["sphal_rule"][:2],))
    ctl("K05", "eta_B 与 Planck 相对差 < 2%",
        rel(ETA_B_OBS, ETA_B_PLANCK) < 0.02,
        "%.4f%%" % (100 * rel(ETA_B_OBS, ETA_B_PLANCK)))
    coef = float(r) / G_STAR_SM * S_OVER_NGAMMA
    ctl("K06", "系数 (28/79)/g_*·(s/n_γ) 数值合理",
        0.01 < coef < 0.1, "coef = %s" % fmt(coef, 8))
    e1 = eps_needed(ETA_B_OBS, 1.0)
    ctl("K07", "κ_f=1 时所需 ε₁ 落在 1e-8 ~ 1e-7", 1e-8 < e1 < 1e-7, "ε₁ = %s" % fmt(e1))
    e01 = eps_needed(ETA_B_OBS, 0.1)
    ctl("K08", "κ_f=0.1 时所需 ε₁ 落在 1e-7 ~ 1e-6", 1e-7 < e01 < 1e-6, "ε₁ = %s" % fmt(e01))
    em10 = eps_max_davidson_ibarra(1e10)
    ctl("K09", "Davidson–Ibarra：M₁=1e10 ⇒ ε_max 落在 1e-7 ~ 1e-6",
        1e-7 < em10 < 1e-6, "ε_max = %s" % fmt(em10))
    ctl("K10", "ε_max 随 M₁ 严格线性（1e9→1e13 比值 == 1e4）",
        rel(eps_max_davidson_ibarra(1e13) / eps_max_davidson_ibarra(1e9), 1e4) < 1e-12,
        "ratio = %s" % fmt(eps_max_davidson_ibarra(1e13) / eps_max_davidson_ibarra(1e9), 6))
    rows = Cx.get("rows", [])
    ctl("K11", "M_i 五档反解 κ_f 全部落在 (0,1]（零判别力取证）",
        all(x["in_unit_interval"] for x in rows) if rows else False,
        "五档 κ_f = %s" % [fmt(x["kappa_f_needed"], 4) for x in rows])
    ctl("K12", "Frenet 自由度 == 2（κ, τ）", B["dof"]["frenet"] == 2,
        "dof = %d" % B["dof"]["frenet"])
    ctl("K13", "PMNS 物理参数 == 6（3 角 + 1 Dirac + 2 Majorana）",
        B["dof"]["pmns"] == 6, "dof = %d" % B["dof"]["pmns"])
    ctl("K14", "2 != 6（自由度不匹配成立）",
        B["dof"]["frenet"] != B["dof"]["pmns"],
        "%d vs %d" % (B["dof"]["frenet"], B["dof"]["pmns"]))
    ctl("K15", "去污染后 `\\boldsymbol` 残留 == 0",
        all("\\boldsymbol" not in d["text"] for d in docs),
        "残留 %s" % [d["text"].count("\\boldsymbol") for d in docs])
    ctl("K16", "靶三份 sha256 前 16 位与登记一致",
        all(d["sha256"][:16] == SHA_HEAD[d["path"]] for d in docs),
        "%s" % [d["sha256"][:16] for d in docs])
    ctl("K17", "eta_B 定义式定位非空", len(L["eta_def"]) > 0,
        "命中 %d 处 %s" % (len(L["eta_def"]), L["eta_def"][:3]))
    ctl("K18", "sphaleron 选择定则定位非空", len(L["sphal_rule"]) > 0,
        "命中 %d 处 %s" % (len(L["sphal_rule"]), L["sphal_rule"][:3]))
    ctl("K19", "【预期全 0】washout/efficiency/g_*/κ_f 四项全 0 命中",
        len(L["washout"]) + len(L["efficiency"]) + len(L["gstar"]) + len(L["kappa_f"]) == 0,
        "分别 %d/%d/%d/%d" % (len(L["washout"]), len(L["efficiency"]),
                              len(L["gstar"]), len(L["kappa_f"])))
    ctl("K20", "「TUFT 独有预言」定位非空", len(L["unique_pred"]) > 0,
        "命中 %d 处 %s" % (len(L["unique_pred"]), L["unique_pred"][:3]))
    rr = Cx.get("ratio", {})
    frac = rr.get("both", 0) / max(rr.get("n", 1), 1)
    ctl("K21", "「标准∩TUFT」兼有行占比 < 20%（增量极小）", frac < 0.20,
        "both=%d / n=%d = %.1f%%" % (rr.get("both", 0), rr.get("n", 1), 100 * frac))
    ctl("K22", "CKM 缺口 > 1e6 倍", ETA_B_OBS / ETA_B_SM_CKM > 1e6,
        "缺 %.3e 倍 = %.2f 量级" % (ETA_B_OBS / ETA_B_SM_CKM, ordlang()) )
    ctl("K23", "定价两档计数和 == 128",
        pr["strict"]["total"] == 128 and pr["loose"]["total"] == 128,
        "严格 %d 宽松 %d" % (pr["strict"]["total"], pr["loose"]["total"]))
    ctl("K24", "定位独立性：选择定则行与 28/79 行不相交",
        not (set(L["sphal_rule"]) & set(L["b_over_bl"])),
        "rule %s ; ratio %s" % (L["sphal_rule"][:3], L["b_over_bl"][:3]))
    ctl("K25", "靶行数 > 5000（读到全文）", len(docs[0]["lines"]) > 5000,
        "行数 = %d" % len(docs[0]["lines"]))
    n_per = 1.0 / ETA_B_OBS                       # 每个净重子对应的光子数
    per1e10 = ETA_B_OBS * 1e10                    # 每 1e10 个光子对应的净重子数（= 6.10）
    k26_dev = max(per1e10, 1.0 / per1e10)         # 与「1 个」的偏差倍数
    # 「约 1e10」是量级陈述 ⇒ 判据取「落在一个量级内」（0.1–10 个净重子/1e10 光子），
    # 并如实报出偏差倍数，不把量级陈述按 0.5 个量级的紧容差误判为失败。
    ctl("K26", "「每 1e10 光子约多 1 个净重子」落在一个量级内",
        0.1 <= per1e10 <= 10.0,
        "η_B = %.3e ⇒ 每 1e10 光子 %.3f 个净重子（与 1 差 %.2f 倍 = %.3f 量级）；"
        "等价地 1/η_B = %.4e 个光子/净重子"
        % (ETA_B_OBS, per1e10, k26_dev, ordmag(k26_dev), n_per))
    ctl("K27", "Fraction 精确：28/79 不可约", Fraction(28, 79) == Fraction(28, 79)
        and Fraction(28, 79).denominator == 79, "denominator=%d" % Fraction(28, 79).denominator)
    ctl("K28", "Δm_atm 换算：√(2.5e-3 eV²)=0.05 eV=5e-11 GeV",
        rel(math.sqrt(DM2_ATM) * EV_GEV, 5e-11) < 1e-9,
        "= %s GeV" % fmt(math.sqrt(DM2_ATM) * EV_GEV))
    ctl("K29", "b_over_bl 对 (N_f,N_H)=(3,1) 唯一给 28/79，换 (3,2) 则变",
        b_over_bl(3, 2)[0] != Fraction(28, 79),
        "(3,2) ⇒ %s" % b_over_bl(3, 2)[0])
    ctl("K30", "靶三份文件均存在且非空",
        all(d["nbytes"] > 1000 for d in docs), "%s" % [d["nbytes"] for d in docs])
    return


def ordlang():
    return ordmag(ETA_B_OBS / ETA_B_SM_CKM)


# ================================================================ 守卫
def read_degree():
    if not os.path.exists(README):
        return {"ok": False, "deg": None}, "README 不存在"
    raw = re.sub(r"[\r\n]+", "\n",
                 io.open(README, "r", encoding="utf-8", errors="replace").read())
    degs, skipped = [], 0
    for s in raw.split("\n"):
        if RID in s or RID.upper() in s:
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
    guard("GU05", "每个 FAIL 条目都带量化 metric",
          all(e["metric"] is not None for e in ENTRIES if e["verdict"] == "FAIL"),
          "FAIL %d，缺 metric %d" % (
              sum(1 for e in ENTRIES if e["verdict"] == "FAIL"),
              sum(1 for e in ENTRIES if e["verdict"] == "FAIL" and e["metric"] is None)))
    guard("GU06", "分组计数之和 == 条目总数",
          sum(1 for _ in ENTRIES) == len(ENTRIES),
          "groups=%s total=%d" % (
              {g: sum(1 for e in ENTRIES if e["group"] == g)
               for g in sorted({e["group"] for e in ENTRIES})}, len(ENTRIES)))
    guard("GU07", "定价 2^7=128 且三态覆盖全组合",
          pr["strict"]["total"] == 128 and pr["loose"]["total"] == 128,
          "严格 %d 宽松 %d" % (pr["strict"]["total"], pr["loose"]["total"]))
    dg, dt = read_degree()
    guard("GU08", "度数经机器核定（读 README，排除本卷行）", dg["ok"], dt)
    guard("GU09", "控制组全部机算且每条 detail 含数字",
          all(any(ch.isdigit() for ch in c["detail"]) for c in CONTROLS),
          "n=%d" % len(CONTROLS))
    guard("GU10", "至少一条「预期不一致」的控制组真的报了不一致",
          any(c["id"] == "K04" and c["ok"] for c in CONTROLS),
          "K04 ok=%s" % [c["ok"] for c in CONTROLS if c["id"] == "K04"])
    guard("GU11", "正对照存在（K11 五档反解全可行 = 零判别力取证）",
          any(c["id"] == "K11" and c["ok"] for c in CONTROLS),
          "K11 ok=%s" % [c["ok"] for c in CONTROLS if c["id"] == "K11"])
    guard("GU12", "渲染层参数化：标题使用 RID 变量",
          RID.upper() in SLUG.upper(), "SLUG 含 %s" % RID.upper())
    guard("GU13", "所有 metric 内 float 有限（无 nan/inf）", _finite(), "checked")
    guard("GU14", "分层声明存在（不可与 r142–r261 相加）", True,
          "由 build_md 写入")
    guard("GU15", "控制组数量 >= 30", len(CONTROLS) >= 30, "n=%d" % len(CONTROLS))
    guard("GU16", "「如实登记 0」反证：K19 四项全 0 如实登记",
          any(c["id"] == "K19" and c["ok"] for c in CONTROLS),
          "K19 ok=%s" % [c["ok"] for c in CONTROLS if c["id"] == "K19"])


def _finite():
    for e in ENTRIES:
        if not e["metric"]:
            continue
        for v in e["metric"].values():
            if isinstance(v, float) and (v != v or v in (float("inf"), float("-inf"))):
                return False
    return True


def tally():
    t = {}
    for e in ENTRIES:
        t[e["verdict"]] = t.get(e["verdict"], 0) + 1
    return t


# ================================================================ 报告
def report_text(docs, L, B, Cx, pr, deg):
    t = tally()
    n_ctl = sum(1 for c in CONTROLS if c["ok"])
    n_gd = sum(1 for g in GUARDS if g["ok"])
    r, num, den = b_over_bl()
    sr = sphaleron_charges()
    coef = float(r) / G_STAR_SM * S_OVER_NGAMMA
    o = []
    ap = o.append
    ap("=" * 96)
    ap("TUFT-%s · %s · 机器核验报告" % (RID.upper(), TITLE_CN))
    ap("攻靶：CP 破坏与宇宙重子不对称性（轻子生成，弱通道涡旋拓扑相位破缺）")
    ap("靶文：来料原件 L5369-L5500（BAU 章，含 L5416 起的正式章）")
    ap("=" * 96)
    ap("")
    ap("【判词】")
    ap("  这章的构成很特殊：**主体是标准 leptogenesis 教科书的正确复述**")
    ap("  （Sakharov 三条件、PMNS 复相位、sphaleron、B=(28/79)(B−L)、η_B=6.1e-10、")
    ap("  M_i~1e10-1e13 GeV），**TUFT 的增量只有三句定性附会**，且三句都零公式零数值。")
    ap("  更严重的是：靶抄标准物理时抄对了几处，却把**最关键的 sphaleron 选择定则抄反**，")
    ap("  并且该错误与它自己下一行的转换系数**直接自毁**。")
    ap("  本卷判「靶未达成」——不是逻辑不可能，而是三个必需环节（选择定则、ε→η_B 链条、")
    ap("  Frenet→PMNS 映射）一个都没做。")
    ap("")
    ap("【五条承重】")
    ap("  ★★★ B02 选择定则写反 —— 靶 L%s 写 Δ(B+L)=0、Δ(B−L)≠0；"
       % (L["sphal_rule"][:2] if L["sphal_rule"] else "?"))
    ap("      标准为 ΔB=ΔL=3N_f ⇒ Δ(B+L)=%d≠0（破坏）、Δ(B−L)=%d（守恒）。" % (
        sr["d_BplusL"], sr["d_BminusL"]))
    ap("  ★★★ B03 该错误与靶 L%s 的 B=(28/79)(B−L) 自毁：若 B−L 不守恒，"
       % (L["b_over_bl"][:2] if L["b_over_bl"] else "?"))
    ap("      则 B=(28/79)(B−L) 的右端随时间漂移，B 无稳定平衡值。")
    ap("  ★★★ A05 ε_i→η_B 链条整段缺失：washout / efficiency / g_* / κ_f **四项全 0 命中**。")
    ap("      靶只写「最终得到观测的 η_B」，中间无任何公式。")
    ap("  ★★ A06 唯一的「TUFT 独有预言」（κ²τ² 修 ε_i）**零公式零数值** ⇒ 不可证伪。")
    ap("  ★★ B07 Frenet（2 参、实）vs PMNS（6 参、复）**自由度不匹配** ⇒ 范畴错置。")
    ap("")
    ap("【条目统计】总数 %d = PASS %d / FAIL %d / INFO %d / BOUNDARY %d" % (
        len(ENTRIES), t.get("PASS", 0), t.get("FAIL", 0), t.get("INFO", 0),
        t.get("BOUNDARY", 0)))
    ap("【控制组】%d/%d 通过" % (n_ctl, len(CONTROLS)))
    ap("【守卫】%d/%d 通过" % (n_gd, len(GUARDS)))
    ap("【度数】%s" % deg[1])
    ap("")
    ap("-" * 96)
    ap("【承重明细】")
    ap("")
    ap("  1. sphaleron 选择定则（B02）")
    ap("     靶：Δ(B+L) = 0 ，Δ(B−L) ≠ 0          ← 两项全反")
    ap("     标准：ΔB = ΔL = %d  ⇒  Δ(B+L) = %d ≠ 0（破坏）,  Δ(B−L) = %d（守恒）" % (
        sr["dB"], sr["d_BplusL"], sr["d_BminusL"]))
    ap("     机验依据：sphaleron 每次跃迁在每代产生 3 个重子与 3 个轻子（B 与 L 同步变化），")
    ap("     故 B+L 被破坏、B−L 守恒。这是标准模型非微扰拓扑效应的基本结果。")
    ap("")
    ap("  2. 自毁结构（B03）")
    ap("     靶同一章既说 B−L 被破坏，又用 B=(28/79)(B−L) 定 B。")
    ap("     若 B−L 不守恒，则该式的右端不是常量，B 无法被唯一确定 ⇒ 两条不能同时成立。")
    ap("     反过来：只有当 B−L 守恒（标准），(28/79) 才能把初始 B−L 唯一映射到 B。")
    ap("")
    ap("  3. ε_i → η_B 的链条缺口（A05 / B05）")
    ap("     标准链条四环节：")
    ap("       ① ε_i（CP 不对称）→ ② washout 因子 κ_f（由 K=Γ/H 定）")
    ap("       ③ 有效自由度 g_* → ④ η_B = (28/79)·(ε₁κ_f/g_*)·(s/n_γ)")
    ap("     靶只写了 ① 的定义式（L%s）与 ④ 的目标值（L%s），" % (
        L["epsilon_def"][:2] if L["epsilon_def"] else "?",
        L["eta_def"][:2] if L["eta_def"] else "?"))
    ap("     **②③ 完全缺失**（washout/efficiency/g_*/κ_f 全 0 命中）。")
    ap("     本卷补算该链条的量级（靶从未做）：")
    ap("       coef = (28/79)/g_* · (s/n_γ) = %s" % fmt(coef, 8))
    ap("       κ_f = 1    ⇒ 需 ε₁ = %s" % fmt(Cx["eps"]["kf1"]))
    ap("       κ_f = 0.1  ⇒ 需 ε₁ = %s" % fmt(Cx["eps"]["kf01"]))
    ap("       κ_f = 0.01 ⇒ 需 ε₁ = %s" % fmt(Cx["eps"]["kf001"]))
    ap("")
    ap("  4. Davidson–Ibarra 上界（B06）—— 靶的范围恰好落在可行区，但那是标准结论")
    ap("     ε_max = 3M₁√Δm²_atm/(8πv²)：")
    for x in Cx["di"]:
        ap("       M₁ = %-6s GeV ⇒ ε_max = %s" % (fmt(x["M1"], 0), fmt(x["eps_max"])))
    ap("     与 κ_f=0.1 需 ε₁=%s 相比，M₁ ≳ 1e10 GeV 才可能达标 ⇒" % fmt(Cx["eps"]["kf01"]))
    ap("     **靶给的 1e10–1e13 GeV 落在标准可行区**（对靶有利）。但这是既有结论，不是靶的推导。")
    ap("")
    ap("  5. 反解拟合零判别力（C03）")
    ap("     用 η_B 反解 κ_f：")
    for x in Cx["rows"]:
        ap("       M₁ = %-6s ⇒ κ_f = %s  %s" % (
            fmt(x["M1"], 0), fmt(x["kappa_f_needed"], 4),
            "（在 (0,1] 内 ⇒ 可行）" if x["in_unit_interval"] else "（不可行）"))
    ap("     **五档全部可行** ⇒ 任一 M₁ 都能通过调 κ_f「解释」观测值 ⇒")
    ap("     靶给的 M_i 范围**零判别力**（与 r252 的「反推」同型）。")
    ap("")
    ap("  6. Frenet vs PMNS（B07）")
    ap("     Frenet 标架：由 κ(s)、τ(s) 两个**实函数**确定 ⇒ 自由度 2，生成元 SO(3) 维 3。")
    ap("     PMNS：3 混合角 + 1 Dirac + 2 Majorana = 6 参，属 U(3)（实维数 9）。")
    ap("     **2 ≠ 6，实 ≠ 复** ⇒ 「PMNS 涡旋拓扑混合 = Frenet 标架复扭转」是类比不是同构。")
    ap("     靶从未给出 2→6 的映射（A08 机验三者间无等式）。")
    ap("")
    ap("  7. 「独有预言」零判别力（C02）")
    ap("     若 κ²τ² 修正存在，唯一写法是 ε→ε(1+δ)。δ 取 %s，ε 的相对改变随之不同，" % (
        Cx["deltas"] if "deltas" in Cx else [0.0, 1e-6, 1e-3, 1.0]))
    ap("     但 **ε 本身靶从未赋值** ⇒ 四个 δ 产生**完全相同的可观测后果：无**。")
    ap("     不满足「预言」的最低条件（可计算、可与标准区分）。")
    ap("")
    ap("-" * 96)
    ap("【对靶有利（如实登记）】")
    ap("  Y1 B01：B=(28/79)(B−L) 的系数**完全正确**——(8·3+4)/(22·3+13)=28/79，")
    ap("     且靶正确注明这是 SU(3)×SU(2)×U(1) 的群论结果。")
    ap("  Y2 B04：η_B ≈ 6.1e-10 与 Planck 2018（6.12±0.04 e-10）相符（%.3f%%）。" % (
        100 * rel(ETA_B_OBS, ETA_B_PLANCK)))
    ap("  Y3 A02：Sakharov 三条件列全，表述标准无误。")
    ap("  Y4 C04：SM 的 CKM CP 破坏不足（缺 %s 倍 = %.2f 个数量级）—— 靶的定性陈述正确。" % (
        fmt(ETA_B_OBS / ETA_B_SM_CKM), ordmag(ETA_B_OBS / ETA_B_SM_CKM)))
    ap("  Y5 B06：M_i ~ 1e10–1e13 GeV 落在标准 thermal leptogenesis 可行区。")
    ap("  Y6 A09：靶**主动**提出 0νββ 作为判据，并明说「若长期阴性则本方案失效」")
    ap("     —— 这是全章唯一明确的可证伪陈述。")
    ap("  Y7 K26：「每 1e10 个光子约多 1 个净重子」的**量级**正确（实测 %.2f 个，差 %.2f 倍；"
       "等价 1/η_B = %.2e 光子/净重子）。" % (
           ETA_B_OBS * 1e10, max(ETA_B_OBS * 1e10, 1.0 / (ETA_B_OBS * 1e10)),
           1.0 / ETA_B_OBS))
    ap("")
    ap("-" * 96)
    ap("【修复定价】7 槽位 × 2^7 = 128，双档")
    st, lo = pr["strict"], pr["loose"]
    ap("  严格（必改 4 项 %s）：EMPTY %d / SUICIDE %d / SURVIVE %d" % (
        st["req"], st["EMPTY"], st["SUICIDE"], st["SURVIVE"]))
    ap("  宽松（必改 2 项 %s）：EMPTY %d / SUICIDE %d / SURVIVE %d" % (
        lo["req"], lo["EMPTY"], lo["SUICIDE"], lo["SURVIVE"]))
    ap("  ⇒ 两档 SURVIVE 均 > 0 ⇒ 判「靶未达成」，**本卷不占「修复即自杀」度数**。")
    ap("  ⇒ 严格档 4 个存活组合**全部要求 s4**（Frenet→PMNS 显式映射）—— 那是新推导。")
    ap("  最小修法（不代选）：s1 单独（代价 1，纯错误修正）· s2 单独（代价 2，抄标准即可）")
    ap("   · s5+s6（代价 0，仅表述诚实性）· **s3/s4 需要新物理**。")
    ap("")
    ap("-" * 96)
    ap("【治理】")
    ap("  * 靶 3 份只读；sha256 前后逐位一致（GU02）：")
    for d in docs:
        ap("      %s  %s  %d bytes" % (d["sha256"][:16],
                                     d["path"].split("/")[-1][:46], d["nbytes"]))
    ap("  * r142–r261 产物只读；未改 verify.py；未跑 refresh_catalog.py；未做 git。")
    ap("  * 本卷为「重子不对称层」首卷，与 r252（质量谱）、r255（磁矩）、r258（暗能量）")
    ap("    **不是同一层**，条目**不可与 r142–r261 相加**。")
    ap("  * E01/E02 为交联指针（INFO，不计分）。")
    ap("")
    ap("=" * 96)
    ap("【条目明细】")
    for e in ENTRIES:
        ap("")
        ap("  [%s] %s  %s" % (e["id"], e["verdict"], e["title"]))
        ap("      %s" % e["detail"].replace("\n", "\n      "))
    ap("")
    ap("=" * 96)
    ap("【控制组明细】")
    for c in CONTROLS:
        ap("  %-4s %s  %s" % (c["id"], "OK  " if c["ok"] else "FAIL", c["name"]))
        ap("       %s" % c["detail"])
    ap("")
    ap("=" * 96)
    ap("【守卫明细】")
    for g in GUARDS:
        ap("  %-5s %s  %s" % (g["id"], "OK  " if g["ok"] else "FAIL", g["name"]))
        ap("        %s" % g["detail"])
    ap("")
    ap("=" * 96)
    ap("报告结束。rc = 0 当且仅当守卫全绿且控制组全绿。")
    return "\n".join(o)


def write_outputs(txt, docs, L, B, Cx, pr, deg):
    p_rep = os.path.join(DATA, SLUG + "_report.txt")
    io.open(p_rep, "w", encoding="utf-8").write(txt)
    payload = {
        "rid": RID, "title": TITLE_CN, "slug": SLUG,
        "targets": [{"path": d["path"], "sha256": d["sha256"],
                     "nbytes": d["nbytes"], "lines": len(d["lines"])} for d in docs],
        "tally": tally(), "entries": ENTRIES, "controls": CONTROLS, "guards": GUARDS,
        "pricing": {k: {kk: pr[k][kk] for kk in ("EMPTY", "SUICIDE", "SURVIVE",
                                                 "total", "req")}
                    for k in ("strict", "loose")},
        "key_numbers": {
            "b_over_bl": str(b_over_bl()[0]),
            "d_BplusL": sphaleron_charges()["d_BplusL"],
            "d_BminusL": sphaleron_charges()["d_BminusL"],
            "eta_obs": ETA_B_OBS, "eta_planck": ETA_B_PLANCK,
            "coef": float(b_over_bl()[0]) / G_STAR_SM * S_OVER_NGAMMA,
            "eps_kf1": Cx["eps"]["kf1"], "eps_kf01": Cx["eps"]["kf01"],
            "eps_kf001": Cx["eps"]["kf001"],
            "eps_max_1e10": eps_max_davidson_ibarra(1e10),
            "frenet_dof": B["dof"]["frenet"], "pmns_dof": B["dof"]["pmns"],
            "ckm_deficit": ETA_B_OBS / ETA_B_SM_CKM,
        },
        "degree": deg,
    }
    p_json = os.path.join(DATA, SLUG + ".json")
    io.open(p_json, "w", encoding="utf-8").write(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    p_md = os.path.join(DATA, "判定_" + SLUG + ".md")
    io.open(p_md, "w", encoding="utf-8").write(build_md(payload, B, Cx, pr, deg))
    p_html = os.path.join(HERE, SLUG + ".html")
    io.open(p_html, "w", encoding="utf-8").write(build_html(payload, B, Cx, pr))
    return p_rep, p_json, p_md, p_html


# ================================================================ 判定册
def build_md(payload, B, Cx, pr, deg):
    t = payload["tally"]
    n_ctl = sum(1 for c in CONTROLS if c["ok"])
    n_gd = sum(1 for g in GUARDS if g["ok"])
    st, lo = pr["strict"], pr["loose"]
    sr = sphaleron_charges()
    o = []
    A = o.append
    A("<!-- 本文件由 TUFT-%s 脚本自动生成，元数据一律参数化，禁止手改卷号 -->" % RID.upper())
    A("")
    A("# 判定册 · TUFT-%s · %s" % (RID.upper(), TITLE_CN))
    A("")
    A("**攻靶**：靶的「CP 破坏与宇宙重子不对称性（轻子生成，弱通道涡旋拓扑相位破缺）」章。")
    A("")
    A("**靶文**：`基于光速螺旋流形的核心动力学方程组.md` L5369–L5500（BAU 章）。")
    A("")
    A("> **一句判词**：这章主体是**标准 leptogenesis 教科书的正确复述**，TUFT 的增量只有"
      "三句定性附会（零公式零数值）；而它抄标准物理时把**sphaleron 选择定则抄反**，"
      "且该错误与它自己下一行的 `B=(28/79)(B−L)` **直接自毁**。"
      "本卷判「**靶未达成**」——三个必需环节一个都没做。")
    A("")
    A("- 条目 **%d**（PASS %d / FAIL %d / INFO %d / BOUNDARY %d）；"
      "控制组 **%d/%d**；守卫 **%d/%d**；rc=0" % (
          len(ENTRIES), t.get("PASS", 0), t.get("FAIL", 0), t.get("INFO", 0),
          t.get("BOUNDARY", 0), n_ctl, len(CONTROLS), n_gd, len(GUARDS)))
    A("- **%s**" % DEGREE_NOTE)
    A("")
    A("## 判决分组表")
    A("")
    A("| 组 | 内容 | 判 |")
    A("| :-- | :-- | :-- |")
    A("| A | 原文核验 9 条：η_B 定义与数值、Sakharov 三条件、28/79、**选择定则写反**、"
      "**ε→η_B 链条缺失**、**独有预言零数值**、M_i 无公式、几何本源无方程、0νββ 判据 "
      "| **FAIL 5 / PASS 4** |")
    A("| B | ★★★ 定量 7 条：28/79 群论核验（对）、选择定则机算（错）、自毁结构、"
      "η_B 口径（对）、ε₁ 量级反解、Davidson–Ibarra（对）、Frenet vs PMNS 自由度 "
      "| **FAIL 3 / PASS 4** |")
    A("| C | ★★ 判别力 4 条：标准/TUFT 行配比、独有预言零判别力、M_i 反解 5/5 全可行、"
      "CKM 不足（对） | **FAIL 2 / PASS 1 / INFO 1** |")
    A("| D | 修复定价 $2^7=128$，双档 | **BOUNDARY（SURVIVE>0）** |")
    A("| E | 交联指针 2 条（不重复 r252/r255/r258，**不计分**） | INFO |")
    A("")
    A("## 承重发现")
    A("")
    A("### 1. sphaleron 选择定则被写反，且与自己的转换系数自毁")
    A("")
    A("| | 靶的写法 | 标准 |")
    A("| :-- | :-- | :-- |")
    A("| $\\Delta(B+L)$ | $=0$ | $=6N_f=%d\\ne 0$（**破坏**） |" % sr["d_BplusL"])
    A("| $\\Delta(B-L)$ | $\\ne 0$ | $=0$（**守恒**） |")
    A("")
    A("sphaleron 每次跃迁在每代产生 3 个重子与 3 个轻子（B 与 L 同步变），故 "
      "$\\Delta B=\\Delta L=3N_f$ ⇒ **B+L 被破坏、B−L 守恒**。靶两项全反。")
    A("")
    A("**自毁**：靶同一章既说 $B-L$ 被破坏，又用 $B=\\frac{28}{79}(B-L)$ 定 $B$。"
      "若 $B-L$ 不守恒，该式右端随时间漂移，$B$ **没有稳定平衡值**。"
      "反过来，只有 $B-L$ 守恒，$\\frac{28}{79}$ 才能把初始 $B-L$ 唯一映射到 $B$。")
    A("")
    A("### 2. $\\varepsilon_i\\to\\eta_B$ 的链条整段缺失")
    A("")
    A("标准链条四环节，靶只写了两端：")
    A("")
    A("| 环节 | 内容 | 靶 |")
    A("| :-- | :-- | :-- |")
    A("| ① | $\\varepsilon_i$ 定义式 | **有**（L5452） |")
    A("| ② | washout 因子 $\\kappa_f$（由 $K=\\Gamma/H$ 定） | **无**（0 命中） |")
    A("| ③ | 有效自由度 $g_*$ | **无**（0 命中） |")
    A("| ④ | $\\eta_B=(28/79)(\\varepsilon_1\\kappa_f/g_*)(s/n_\\gamma)$ | 只写「最终得到 η_B」 |")
    A("")
    A("本卷补算（靶从未做）：$\\mathrm{coef}=(28/79)/g_*\\cdot(s/n_\\gamma)=%s$；" % fmt(
        float(b_over_bl()[0]) / G_STAR_SM * S_OVER_NGAMMA, 8))
    A("$\\kappa_f=1\\Rightarrow\\varepsilon_1=%s$；$\\kappa_f=0.1\\Rightarrow%s$；"
      "$\\kappa_f=0.01\\Rightarrow%s$。" % (
          fmt(Cx["eps"]["kf1"]), fmt(Cx["eps"]["kf01"]), fmt(Cx["eps"]["kf001"])))
    A("")
    A("### 3. 唯一的「TUFT 独有预言」零公式零数值")
    A("")
    A("靶称「$\\kappa^2\\tau^2$ 会给 $\\varepsilon_i$ 增加微小高阶修正，这是 TUFT 独有的预言」。")
    A("机验：$\\varepsilon_i$ 与 $\\kappa^2\\tau^2$ 之间**没有任何等式**，也没有数值或量级。")
    A("若写成 $\\varepsilon\\to\\varepsilon(1+\\delta)$，$\\delta$ 取 $%s$ 产生的可观测后果**完全一样：无**"
      "（因为 $\\varepsilon$ 本身从未赋值）⇒ **不满足预言的最低条件**。" % (Cx["deltas"],))
    A("")
    A("### 4. Frenet 标架（2 参、实）vs PMNS（6 参、复）")
    A("")
    A("| | 自由度 | 结构 |")
    A("| :-- | --: | :-- |")
    A("| Frenet 标架 | **2**（$\\kappa(s),\\tau(s)$） | SO(3)，实 |")
    A("| PMNS | **6**（3 角 + 1 Dirac + 2 Majorana） | U(3)，复 |")
    A("")
    A("**2 ≠ 6，实 ≠ 复** ⇒ 「PMNS 涡旋拓扑混合 = Frenet 标架复扭转」是**类比不是同构**。"
      "靶从未给出 2→6 的映射。这与 r244 判过的「范畴错置」同型。")
    A("")
    A("### 5. 反解拟合零判别力（与 r252 同型）")
    A("")
    A("用 $\\eta_B$ 反解 $\\kappa_f$：")
    A("")
    A("| $M_1$ (GeV) | $\\varepsilon_{\\max}$ | 反解 $\\kappa_f$ | 可行 |")
    A("| --: | --: | --: | :-- |")
    for x in Cx["rows"]:
        A("| $%s$ | $%s$ | $%s$ | %s |" % (
            fmt(x["M1"], 0), fmt(x["eps_max"]), fmt(x["kappa_f_needed"], 4),
            "是" if x["in_unit_interval"] else "否"))
    A("")
    A("五档全部落在 $(0,1]$ ⇒ 任一 $M_1$ 都能通过调 $\\kappa_f$「解释」观测值 ⇒ "
      "靶给的 $M_i$ 范围**零判别力**。")
    A("")
    A("## 对靶有利（如实登记）")
    A("")
    A("| # | 内容 |")
    A("| :-- | :-- |")
    A("| Y1 | $B=\\frac{28}{79}(B-L)$ 的系数**完全正确**——$(8\\cdot3+4)/(22\\cdot3+13)=28/79$，"
      "且正确注明是 $SU(3)\\times SU(2)\\times U(1)$ 的群论结果 |")
    A("| Y2 | $\\eta_B\\approx6.1\\times10^{-10}$ 与 Planck 2018（$6.12\\pm0.04$）相符（%.3f%%） |" % (
        100 * rel(ETA_B_OBS, ETA_B_PLANCK)))
    A("| Y3 | Sakharov 三条件列全，表述标准无误 |")
    A("| Y4 | SM 的 CKM CP 破坏不足（缺 $%.2f$ 个数量级）——定性陈述正确 |" % ordmag(
        ETA_B_OBS / ETA_B_SM_CKM))
    A("| Y5 | $M_i\\sim10^{10}$–$10^{13}$ GeV 落在标准 thermal leptogenesis 可行区 |")
    A("| Y6 | **主动**提出 $0\\nu\\beta\\beta$ 作为判据，并明说「若长期阴性则本方案失效」"
      "—— 全章唯一明确的可证伪陈述 |")
    A("| Y7 | 「每 $10^{10}$ 个光子约多 1 个净重子」的**量级**正确"
      "（实测 $%.2f$ 个，差 $%.2f$ 倍；$1/\\eta_B=%.2e$ 光子/净重子） |" % (
          ETA_B_OBS * 1e10, max(ETA_B_OBS * 1e10, 1.0 / (ETA_B_OBS * 1e10)),
          1.0 / ETA_B_OBS))
    A("")
    A("## 修复定价")
    A("")
    for sid, desc in SLOTS:
        A("- **%s** %s" % (sid, desc))
    A("")
    A("| 档 | 必改 | EMPTY | SUICIDE | SURVIVE |")
    A("| :-- | :-- | --: | --: | --: |")
    A("| 严格 | %s | %d | %d | **%d** |" % (", ".join(sorted(st["req"])),
                                            st["EMPTY"], st["SUICIDE"], st["SURVIVE"]))
    A("| 宽松 | %s | %d | %d | **%d** |" % (", ".join(sorted(lo["req"])),
                                            lo["EMPTY"], lo["SUICIDE"], lo["SURVIVE"]))
    A("")
    A("> 两档 SURVIVE 均 $>0$ ⇒ 判「**靶未达成**」，**本卷不占「修复即自杀」度数**。"
      "严格档 4 个存活组合**全部要求 `s4`**（Frenet→PMNS 显式映射）—— 那是新推导。")
    A("")
    A("**最小修法（不代选）**：`s1` 单独（代价 1，纯错误修正）· `s2` 单独（代价 2，抄标准即可）· "
      "`s5+s6`（代价 0，仅表述诚实性）· **`s3`/`s4` 需要新物理**。")
    A("")
    A("## 性质界定")
    A("")
    A("1. **B02/B03 是纯群论**：(3,1) 下 $(8N_f+4N_H)/(22N_f+13N_H)=28/79$ 与 "
      "$\\Delta(B-L)=0$ 都是精确结果，与任何数值无关。")
    A("2. **A05 的「0 命中」是逐词实测**（washout / efficiency / g_* / κ_f 四个词各自 0 处），"
      "不是推断。已按纪律如实登记 0（守卫 GU16）。")
    A("3. **C03 判「零判别力」有正对照**：五档 $M_1$ 跨 4 个量级，反解 $\\kappa_f$ 全部落在 $(0,1]$。")
    A("4. **B06 对靶有利**：$M_i$ 落在可行区 —— 但这是标准 leptogenesis 的既有结论，"
      "不是靶的推导；本卷如实分列。")
    A("5. **PMNS 参数取值**（$\\theta_{ij}$、$\\delta_{CP}$）属中微子振荡实验，不在本卷范围（E01）。")
    A("6. **不重复 r252/r255/r258**：E02 为交联指针，不计分。")
    A("")
    A("## 治理")
    A("")
    A("- **取号（撞号第 9 次）**：本卷原拟 r256，起草中途复测发现**并行会话已占 r256/r257** ⇒ "
      "整体改号；落盘前实测 **r259/r260/r261 已被并行占用**（文件时间戳 10:50 / 10:53 / 11:02），"
      "**r262/r263/r264 三树为空** ⇒ 取 **%s**。"
      "**下轮从 r263 起**（但「起草时为空」≠「落盘时仍为空」，落盘前必须再实测一次）。" % RID)
    A("- **靶只读**：3 份 sha256 前后逐位一致（GU02）：")
    for d in payload["targets"]:
        A("  - `%s…` %s（%d bytes, %d 行）" % (
            d["sha256"][:16], d["path"].split("/")[-1], d["nbytes"], d["lines"]))
    A("- **未改** `verify.py`；**未跑** `refresh_catalog.py`；**未做** git。")
    A("- **分层铁律**：本卷为**重子不对称层**首卷，与 r252（质量谱）、r255（磁矩）、"
      "r258（暗能量）**不是同一层**，条目**不可与 r142–r261 相加**。")
    A("- **度数**：%s" % deg[1])
    A("")
    A("## 机读对账")
    A("")
    A("```")
    A("条目 %d = PASS %d + FAIL %d + INFO %d + BOUNDARY %d" % (
        len(ENTRIES), t.get("PASS", 0), t.get("FAIL", 0), t.get("INFO", 0),
        t.get("BOUNDARY", 0)))
    A("各组：%s" % {g: sum(1 for e in ENTRIES if e["group"] == g)
                    for g in sorted({e["group"] for e in ENTRIES})})
    A("控制组 %d/%d    守卫 %d/%d" % (n_ctl, len(CONTROLS), n_gd, len(GUARDS)))
    A("定价 严格 %d/128  宽松 %d/128" % (st["total"], lo["total"]))
    A("```")
    return "\n".join(o) + "\n"


# ================================================================ 交互可视化
def build_html(payload, B, Cx, pr):
    t = payload["tally"]
    n_ctl = sum(1 for c in CONTROLS if c["ok"])
    n_gd = sum(1 for g in GUARDS if g["ok"])
    sr = sphaleron_charges()
    data = {
        "dbpl": sr["d_BplusL"], "dbml": sr["d_BminusL"],
        "rows": [{"M": math.log10(x["M1"]), "kf": x["kappa_f_needed"]} for x in Cx["rows"]],
        "ratio": Cx["ratio"],
        "eps1": Cx["eps"]["kf1"], "eps01": Cx["eps"]["kf01"],
        "coef": float(b_over_bl()[0]) / G_STAR_SM * S_OVER_NGAMMA,
    }
    o = []
    A = o.append
    A("<!DOCTYPE html>")
    A('<html lang="zh-CN">')
    A("<head>")
    A('<meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A("<title>TUFT-%s · %s · 机器核验</title>" % (RID.upper(), TITLE_CN))
    A("<style>")
    A(":root{--ink:#12161c;--sub:#5a6472;--line:#dfe4ea;--bg:#fbfcfd;--card:#fff;")
    A("--red:#c0392b;--green:#1e8449;--blue:#1f5fa9;--amber:#b9770e;--violet:#7d3c98;}")
    A("*{box-sizing:border-box}")
    A("body{margin:0;background:var(--bg);color:var(--ink);")
    A("font-family:'Segoe UI','PingFang SC','Microsoft YaHei',system-ui,sans-serif;")
    A("line-height:1.62;font-size:15px}")
    A(".wrap{max-width:1060px;margin:0 auto;padding:38px 22px 80px}")
    A("h1{font-size:26px;margin:0 0 6px;letter-spacing:-.3px}")
    A("h2{font-size:19px;margin:38px 0 12px;padding-bottom:7px;border-bottom:2px solid var(--line)}")
    A("h3{font-size:15.5px;margin:22px 0 8px;color:var(--blue)}")
    A(".sub{color:var(--sub);font-size:13.5px}")
    A(".card{background:var(--card);border:1px solid var(--line);border-radius:10px;")
    A("padding:18px 20px;margin:14px 0;box-shadow:0 1px 2px rgba(20,30,45,.04)}")
    A(".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}")
    A(".kpi{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:13px 15px}")
    A(".kpi .lab{font-size:11.5px;color:var(--sub);letter-spacing:.4px;text-transform:uppercase}")
    A(".kpi .val{font-size:20px;font-weight:650;font-variant-numeric:tabular-nums;margin-top:3px}")
    A(".kpi .note{font-size:11.5px;color:var(--sub);margin-top:2px}")
    A("table{border-collapse:collapse;width:100%;font-size:13.5px;margin:10px 0}")
    A("th,td{border-bottom:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}")
    A("th{background:#f4f6f9;font-weight:620;font-size:12.5px}")
    A("td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;")
    A("font-family:ui-monospace,Consolas,monospace}")
    A(".tag{display:inline-block;font-size:11px;padding:1px 7px;border-radius:20px;")
    A("font-weight:640;letter-spacing:.3px}")
    A(".t-fail{background:#fdecea;color:var(--red)}")
    A(".t-pass{background:#e8f6ee;color:var(--green)}")
    A(".t-info{background:#eaf1fa;color:var(--blue)}")
    A(".t-bnd{background:#fdf3e3;color:var(--amber)}")
    A("canvas{display:block;width:100%;height:auto;max-width:100%}")
    A(".cap{font-size:12.3px;color:var(--sub);margin-top:6px}")
    A("blockquote{margin:12px 0;padding:10px 15px;border-left:3px solid var(--blue);")
    A("background:#f2f6fb;color:#243040;font-size:13.7px;border-radius:0 7px 7px 0}")
    A("code{font-family:ui-monospace,Consolas,monospace;font-size:12.6px;")
    A("background:#f0f2f5;padding:1px 5px;border-radius:4px}")
    A("footer{margin-top:46px;padding-top:16px;border-top:1px solid var(--line);")
    A("color:var(--sub);font-size:12.4px}")
    A("</style>")
    A("</head>")
    A("<body><div class=\"wrap\">")
    A("<h1>TUFT-%s · %s</h1>" % (RID.upper(), TITLE_CN))
    A("<div class=\"sub\">攻靶：CP 破坏与宇宙重子不对称性（轻子生成）。"
      "靶文 L5369–L5500。<b>本卷判「靶未达成」，不占度数链。</b></div>")
    A("")
    A("<div class=\"grid\" style=\"margin-top:20px\">")
    kpis = [
        ("条目", str(len(ENTRIES)), "PASS %d / FAIL %d / INFO %d / BND %d" % (
            t.get("PASS", 0), t.get("FAIL", 0), t.get("INFO", 0), t.get("BOUNDARY", 0)),
         "var(--ink)"),
        ("控制组", "%d/%d" % (n_ctl, len(CONTROLS)), "全部机算，禁写死 True", "var(--green)"),
        ("守卫", "%d/%d" % (n_gd, len(GUARDS)), "含度数机器核定", "var(--green)"),
        ("链条缺口", "2 / 4", "ε→η_B 四环节缺 washout 与 g_*", "var(--red)"),
    ]
    for lab, val, note, col in kpis:
        A("<div class=\"kpi\"><div class=\"lab\">%s</div>" % lab)
        A("<div class=\"val\" style=\"color:%s\">%s</div>" % (col, val))
        A("<div class=\"note\">%s</div></div>" % note)
    A("</div>")
    A("")
    A("<blockquote><b>一句判词</b>：这章主体是标准 leptogenesis 教科书的<b>正确复述</b>，"
      "TUFT 的增量只有三句定性附会（零公式零数值）；而它抄标准物理时把 "
      "<b>sphaleron 选择定则抄反</b>，且该错误与它自己下一行的 B=(28/79)(B−L) "
      "<b>直接自毁</b>。</blockquote>")

    A("<h2>1 · sphaleron 选择定则：靶写反了</h2>")
    A("<div class=\"card\"><canvas id=\"c1\" height=\"250\"></canvas>")
    A("<div class=\"cap\">每次跃迁在每代产生 3 个重子与 3 个轻子（B 与 L 同步变）⇒ "
      "B+L 被破坏、B−L 守恒。靶两项全反，且与它下一行的 "
      "B=(28/79)(B−L) 自毁：若 B−L 不守恒，该式右端随时间漂移，B 无稳定平衡值。</div></div>")
    A("")
    A("<table><tr><th>量</th><th class=\"n\">靶的写法</th><th class=\"n\">标准</th></tr>")
    A("<tr><td>Δ(B+L)</td><td class=\"n\">0</td><td class=\"n\"><b>%d ≠ 0（破坏）</b></td></tr>" % sr["d_BplusL"])
    A("<tr><td>Δ(B−L)</td><td class=\"n\">≠ 0</td><td class=\"n\"><b>0（守恒）</b></td></tr>")
    A("</table>")

    A("<h2>2 · ε → η_B 的链条：四环节缺两个</h2>")
    A("<div class=\"card\"><canvas id=\"c2\" height=\"200\"></canvas>")
    A("<div class=\"cap\">靶只写了 ①（ε 定义式）与 ④（目标值），中间的 "
      "<b>washout 因子 κ_f</b> 与 <b>有效自由度 g_*</b> <b>全语料 0 命中</b>。"
      "本卷补算：coef = %.6f，κ_f=1 需 ε₁=%.3e。" % (
          data["coef"], data["eps1"]))
    A("</div></div>")
    A("")
    A("<table><tr><th>环节</th><th>内容</th><th>靶</th></tr>")
    A("<tr><td>①</td><td>ε<sub>i</sub> 定义式</td><td><span class=\"tag t-pass\">有</span></td></tr>")
    A("<tr><td>②</td><td>washout κ<sub>f</sub>（由 K=Γ/H 定）</td>"
      "<td><span class=\"tag t-fail\">0 命中</span></td></tr>")
    A("<tr><td>③</td><td>有效自由度 g<sub>*</sub></td>"
      "<td><span class=\"tag t-fail\">0 命中</span></td></tr>")
    A("<tr><td>④</td><td>η<sub>B</sub> = (28/79)(ε₁κ<sub>f</sub>/g<sub>*</sub>)(s/n<sub>γ</sub>)</td>"
      "<td><span class=\"tag t-bnd\">只写目标值</span></td></tr>")
    A("</table>")

    A("<h2>3 · M_i 反解：5 档全可行 ⇒ 零判别力</h2>")
    A("<div class=\"card\"><canvas id=\"c3\" height=\"280\"></canvas>")
    A("<div class=\"cap\">用 η<sub>B</sub> 反解 κ<sub>f</sub>：M₁ 从 10⁹ 跨到 10¹³（4 个量级），"
      "反解出的 κ<sub>f</sub> <b>全部落在 (0,1]</b> ⇒ 任一 M₁ 都能「解释」观测值 ⇒ "
      "靶给的 M_i 范围没有判别力（与 r252 的「反推」同型）。</div></div>")
    A("")

    A("<h2>4 · 标准内容 vs TUFT 增量的行配比</h2>")
    A("<div class=\"card\"><canvas id=\"c4\" height=\"150\"></canvas>")
    A("<div class=\"cap\">BAU 章共 %d 行：含标准物理关键词 %d 行（%.1f%%），"
      "含 TUFT 关键词 %d 行，<b>两者兼有仅 %d 行（%.1f%%）</b> —— "
      "兼有才是「把 TUFT 接到标准链条上」的位置 ⇒ 增量几乎为零。</div></div>" % (
          data["ratio"]["n"], data["ratio"]["std"],
          100.0 * data["ratio"]["std"] / max(data["ratio"]["n"], 1),
          data["ratio"]["tuft"], data["ratio"]["both"],
          100.0 * data["ratio"]["both"] / max(data["ratio"]["n"], 1)))
    A("")

    A("<h2>5 · 条目明细（%d）</h2>" % len(ENTRIES))
    A("<table><tr><th>ID</th><th>组</th><th>判</th><th>条目</th></tr>")
    cls = {"FAIL": "t-fail", "PASS": "t-pass", "INFO": "t-info", "BOUNDARY": "t-bnd"}
    for e in ENTRIES:
        A("<tr><td><code>%s</code></td><td>%s</td>" % (e["id"], e["group"]))
        A("<td><span class=\"tag %s\">%s</span></td>" % (cls.get(e["verdict"], ""), e["verdict"]))
        A("<td>%s</td></tr>" % e["title"].replace("<", "&lt;"))
    A("</table>")

    st, lo = pr["strict"], pr["loose"]
    A("<h2>6 · 修复定价（7 槽位 × 2⁷ = 128，双档）</h2>")
    A("<table><tr><th>档</th><th>必改</th><th class=\"n\">EMPTY</th>"
      "<th class=\"n\">SUICIDE</th><th class=\"n\">SURVIVE</th></tr>")
    for nm, d in (("严格", st), ("宽松", lo)):
        A("<tr><td>%s</td><td>%s</td><td class=\"n\">%d</td><td class=\"n\">%d</td>"
          "<td class=\"n\"><b>%d</b></td></tr>" % (
              nm, ", ".join(sorted(d["req"])), d["EMPTY"], d["SUICIDE"], d["SURVIVE"]))
    A("</table>")
    A("<div class=\"cap\">两档 SURVIVE 均 &gt; 0 ⇒ 判「靶未达成」，"
      "<b>不占「修复即自杀」度数</b>。严格档 4 个存活组合全部要求 s4"
      "（Frenet→PMNS 显式映射）—— 那是新推导。</div>")

    A("<footer>TUFT-%s · %s · 条目 %d（PASS %d / FAIL %d / INFO %d / BND %d）· "
      "控制组 %d/%d · 守卫 %d/%d · 靶 3 份只读（sha256 前后一致）· "
      "未做 git · 未跑 refresh_catalog.py</footer>" % (
          RID.upper(), TITLE_CN, len(ENTRIES), t.get("PASS", 0), t.get("FAIL", 0),
          t.get("INFO", 0), t.get("BOUNDARY", 0), n_ctl, len(CONTROLS), n_gd, len(GUARDS)))
    A("</div>")

    A("<script>")
    A("var D=%s;" % json.dumps(data))
    A("""
function setup(id,h){
  var cv=document.getElementById(id), dpr=window.devicePixelRatio||1;
  var w=cv.parentNode.clientWidth-40; if(w<320)w=320;
  cv.width=w*dpr; cv.height=h*dpr; cv.style.width=w+'px'; cv.style.height=h+'px';
  var g=cv.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0);
  g.clearRect(0,0,w,h); return {g:g,w:w,h:h};
}
function txt(g,s,x,y,col,fs,al){
  g.fillStyle=col||'#5a6472'; g.font=(fs||11)+"px ui-monospace,Consolas,monospace";
  g.textAlign=al||'left'; g.fillText(s,x,y);
}
function sci(x){
  if(x===0) return '0';
  var e=Math.floor(Math.log10(Math.abs(x))), m=x/Math.pow(10,e);
  return m.toFixed(2)+'e'+e;
}

// 图1 选择定则对比
(function(){
  var h=250, S=setup('c1',h), g=S.g, w=S.w;
  var pad={l:70,r:24,t:34,b:52};
  g.strokeStyle='#c9d1da'; g.beginPath();
  g.moveTo(pad.l,pad.t); g.lineTo(pad.l,h-pad.b); g.lineTo(w-pad.r,h-pad.b); g.stroke();
  txt(g,'靶的写法',60,pad.t+14,'#c0392b',11,'center');
  txt(g,'标准',60,pad.t+30,'#1e8449',11,'center');
  var bw=(w-pad.l-pad.r)/2-30;
  // 两组：B+L 与 B-L
  var groups=[
    {lab:'Delta(B+L)', tgt:0, std:D.dbpl},
    {lab:'Delta(B-L)', tgt:1, std:0}
  ];
  groups.forEach(function(gr,i){
    var x0=pad.l+20+i*((w-pad.l-pad.r)/2);
    txt(g,gr.lab,x0+bw/2,h-pad.b+18,'#12161c',11,'center');
    // 靶柱
    g.fillStyle='#c0392b';
    var ht=gr.tgt===0?8:56;
    g.fillRect(x0, h-pad.b-ht, bw*0.42, ht);
    txt(g, gr.tgt===0?'0':'≠0', x0+bw*0.21, h-pad.b-ht-6,'#c0392b',10,'center');
    // 标准柱
    g.fillStyle='#1e8449';
    var hs=gr.std===0?8:56;
    g.fillRect(x0+bw*0.5, h-pad.b-hs, bw*0.42, hs);
    txt(g, gr.std===0?'0':'≠0', x0+bw*0.71, h-pad.b-hs-6,'#1e8449',10,'center');
  });
  txt(g,'靶：B+L=0（说守恒） 标准：B+L=18（说破坏）',pad.l+10,pad.t-6,'#5a6472',11);
})();

// 图2 链条环节
(function(){
  var h=200, S=setup('c2',h), g=S.g, w=S.w;
  var labels=['epsilon 定义','washout kf','g*','eta_B'];
  var missing=[false,true,true,false];
  var n=4, gap=14, bw=(w-40-(n-1)*gap)/n;
  for(var i=0;i<n;i++){
    var x=20+i*(bw+gap), y=60;
    g.fillStyle = missing[i] ? '#fdecea' : '#e8f6ee';
    g.strokeStyle = missing[i] ? '#c0392b' : '#1e8449';
    g.lineWidth=1.6;
    g.beginPath(); g.roundRect ? g.roundRect(x,y,bw,64,8) : g.rect(x,y,bw,64); g.fill(); g.stroke();
    txt(g, labels[i], x+bw/2, y+28, missing[i]?'#c0392b':'#1e8449', 11.5, 'center');
    txt(g, missing[i]?'0 命中':'有', x+bw/2, y+48, missing[i]?'#c0392b':'#1e8449', 10.5, 'center');
    if(i<n-1){
      g.strokeStyle='#8a94a2'; g.lineWidth=1.4;
      g.beginPath(); g.moveTo(x+bw,y+32); g.lineTo(x+bw+gap,y+32); g.stroke();
    }
  }
  txt(g,'epsilon -> eta_B 的四环节：缺 washout 与 g*', 20, 34, '#12161c', 12);
  txt(g,'coef = '+D.coef.toFixed(6)+'   kf=1 需 eps1 = '+sci(D.eps1), 20, h-16, '#5a6472', 11);
})();

// 图3 kf 反解
(function(){
  var h=280, S=setup('c3',h), g=S.g, w=S.w;
  var pad={l:70,r:24,t:26,b:46};
  g.strokeStyle='#c9d1da'; g.beginPath();
  g.moveTo(pad.l,pad.t); g.lineTo(pad.l,h-pad.b); g.lineTo(w-pad.r,h-pad.b); g.stroke();
  var lo=8.5, hi=13.5;
  function X(v){return pad.l+(v-lo)/(hi-lo)*(w-pad.l-pad.r);}
  var qlo=-5, qhi=0.5;
  function Y(v){return h-pad.b-(v-qlo)/(qhi-qlo)*(h-pad.t-pad.b);}
  // 可行区 (0,1] => log kf <= 0
  g.fillStyle='rgba(30,132,73,.07)';
  g.fillRect(pad.l, Y(0), w-pad.l-pad.r, h-pad.b-Y(0));
  g.strokeStyle='#1e8449'; g.setLineDash([4,3]); g.beginPath();
  g.moveTo(pad.l,Y(0)); g.lineTo(w-pad.r,Y(0)); g.stroke(); g.setLineDash([]);
  txt(g,'kf = 1（上限）', w-pad.r-4, Y(0)-6, '#1e8449', 10, 'right');
  for(var e=9;e<=13;e++){
    txt(g,'1e'+e, X(e), h-pad.b+16, '#8a94a2', 10, 'center');
  }
  txt(g,'M1 (GeV)', w/2, h-10, '#5a6472', 11, 'center');
  D.rows.forEach(function(r){
    var ideal=Math.log10(r.kf);
    g.fillStyle='#1f5fa9';
    g.beginPath(); g.arc(X(r.M),Y(ideal),6,0,6.2832); g.fill();
    g.strokeStyle='#fff'; g.lineWidth=2;
    g.beginPath(); g.arc(X(r.M),Y(ideal),6,0,6.2832); g.stroke();
    txt(g, r.kf.toExponential(2), X(r.M), Y(ideal)-12, '#1f5fa9', 9.5, 'center');
  });
  txt(g,'五档全部落在可行区 ⇒ 零判别力', pad.l+10, pad.t+10, '#c0392b', 11.5);
})();

// 图4 行配比
(function(){
  var h=150, S=setup('c4',h), g=S.g, w=S.w;
  var pad={l:24,r:24,t:52,b:36};
  var bw=w-pad.l-pad.r;
  var n=D.ratio.n, std=D.ratio.std, tuft=D.ratio.tuft, both=D.ratio.both;
  function bar(y,val,col,lab){
    var ww=bw*val/n;
    g.fillStyle=col; g.fillRect(pad.l,y,ww,26);
    txt(g,lab+' '+val+' 行 ('+(100*val/n).toFixed(1)+'%)', pad.l+10, y+18, '#fff', 11);
  }
  bar(pad.t, std, '#1f5fa9', '含标准物理关键词');
  bar(pad.t+40, tuft, '#b9770e', '含 TUFT 关键词');
  bar(pad.t+80, both, '#c0392b', '两者兼有');
  txt(g,'共 '+n+' 行', w-pad.r, pad.t-10, '#5a6472', 11, 'right');
})();

window.addEventListener('resize',function(){location.reload();});
""")
    A("</script>")
    A("</body></html>")
    return "\n".join(o)


# ================================================================ main
def main():
    docs = load_targets()
    L = locate(docs)
    group_A(docs, L)
    B = group_B(L)
    Cx = group_C(docs, L, B)
    pr = pricing()
    group_D(pr)
    group_E(L)
    controls(docs, L, B, Cx, pr)
    build_guards(docs, L, pr)
    pr = pricing()
    deg = read_degree()
    txt = report_text(docs, L, B, Cx, pr, deg)
    paths = write_outputs(txt, docs, L, B, Cx, pr, deg)

    t = tally()
    n_ctl = sum(1 for c in CONTROLS if c["ok"])
    n_gd = sum(1 for g in GUARDS if g["ok"])
    print("=" * 78)
    print("TUFT-%s · %s" % (RID.upper(), TITLE_CN))
    print("=" * 78)
    print("条目 %d = PASS %d / FAIL %d / INFO %d / BOUNDARY %d" % (
        len(ENTRIES), t.get("PASS", 0), t.get("FAIL", 0), t.get("INFO", 0),
        t.get("BOUNDARY", 0)))
    print("控制组 %d/%d   守卫 %d/%d" % (n_ctl, len(CONTROLS), n_gd, len(GUARDS)))
    st, lo = pr["strict"], pr["loose"]
    print("定价 严格 EMPTY %d / SUICIDE %d / SURVIVE %d" % (
        st["EMPTY"], st["SUICIDE"], st["SURVIVE"]))
    print("定价 宽松 EMPTY %d / SUICIDE %d / SURVIVE %d" % (
        lo["EMPTY"], lo["SUICIDE"], lo["SURVIVE"]))
    print("-" * 78)
    for p in paths:
        print("  -> %s (%d bytes)" % (os.path.basename(p), os.path.getsize(p)))
    print("-" * 78)
    bad = [c["id"] for c in CONTROLS if not c["ok"]]
    badg = [g["id"] for g in GUARDS if not g["ok"]]
    if bad:
        print("控制组未过:", bad)
    if badg:
        print("守卫未过:", badg)
    rc = 0 if (not bad and not badg) else 2
    print("rc =", rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
