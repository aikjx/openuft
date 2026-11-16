# -*- coding: utf-8 -*-
"""方向自审与攻击面重定向 · 可翻转判据机核（纯标准库）。

本文件刻意不是「第 27 册判定册」：
- 不设自设公理集，不产 GATES-PASS 自盖章，不做 NO-HARDCODE-OK / VERDICT-MACHINE 自证守卫；
- 判据取外部实验读数（允许单侧下界），来源给一手 URL 供外部核查；
- 结论必须随外部读数改变，机读演示三个翻转态；
- 不占 RID、不入 README、不回写任何既有产物。
"""
import os
import glob
import json
import re
import collections
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
D = Decimal
LN10 = D(10).ln()

HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
MAIN = os.path.dirname(DATA)
OUT_JSON = os.path.join(DATA, "_ALG_redirect_falsifiable_recompute_2026-11-16.json")
OUT_MD = os.path.join(MAIN, "算法联盟_方向自审与攻击面重定向_2026-11-16.md")


def sci(x, d=8):
    v = D(str(x))
    if v == 0:
        return "0"
    return format(v, "." + str(d) + "E")


def dex(x):
    return D(str(x)).ln() / LN10


def frac_str(x):
    return str(Fraction(str(x)))


# ---------------------------------------------------------------- 一、自审
def row_text(r):
    if isinstance(r, dict):
        return " ".join(str(r.get(k, "")) for k in ("name", "note", "act", "exp"))
    return str(r)


def collect_rows(d):
    """历史册字段名不统一：rows / gates / segments / checks 都曾用作判据行。"""
    out = []
    for v in d.values():
        if not isinstance(v, list):
            continue
        for x in v:
            if isinstance(x, dict) and any(k in x for k in ("name", "note", "ok", "kind")):
                out.append(row_text(x))
    return out


def self_audit():
    led = json.load(open(HITS[0], encoding="utf-8"))["ledger"]
    ids = [x["id"] for x in led]
    zero_sigma = [x["id"] for x in led
                  if str(x.get("sigma", "0")) in ("0", "0.0", "")]
    books, reports = [], []
    for root, dirs, fs in os.walk(MAIN):
        dirs[:] = [d for d in dirs if d not in ("_scratch", "__pycache__")]
        for f in fs:
            p = os.path.join(root, f)
            if not f.startswith("_ALG_"):
                continue
            if f.endswith(".json") and "verify" not in f and "来料" not in f:
                try:
                    d = json.load(open(p, encoding="utf-8"))
                except Exception:
                    continue
                if "final" in d:
                    books.append((p, d))
            elif f.endswith(".txt") and "report" in f.lower():
                reports.append((p, open(p, encoding="utf-8", errors="ignore").read()))

    blobs = {os.path.basename(p): json.dumps(d, ensure_ascii=False) for p, d in books}
    blobs.update({os.path.basename(p): t for p, t in reports})
    gate_text = "\n".join(t for p, d in books for t in collect_rows(d))

    def count(pat, text):
        return len(pat.findall(text))

    unused = []
    for aid in ids:
        pat = re.compile(r"(?<![A-Z0-9])" + re.escape(aid) + r"(?![0-9])")
        if count(pat, gate_text) == 0:
            unused.append(aid)

    p11_pat = re.compile(r"P11|tau_p|2\.4\s*[eE]\s*34|质子衰变|proton\s*decay", re.I)
    p11_files = sorted(k for k, t in blobs.items() if p11_pat.search(t))
    p11_gates = [t for p, d in books for t in collect_rows(d) if p11_pat.search(t)]
    p11_books = sorted({os.path.basename(p) for p, d in books
                        if any(p11_pat.search(t) for t in collect_rows(d))})

    finals = [str(d.get("final", "")) for _, d in books]
    suffix = collections.Counter(f.split("--")[-1] for f in finals)
    fail_sum = sum(int(d.get("counts", {}).get("FAIL", 0) or 0) for _, d in books)
    # 口径：只看 final 后缀，不看册名前缀。
    # 并行会话有册名含 BREAKTHROUGH-LOCATION，但后缀仍是 GATES-PASS，属误报来源。
    positive = [f for f in finals if not f.split("--")[-1].startswith("GATES-PASS")]

    return {
        "n_books": len(books),
        "n_reports": len(reports),
        "n_anchors": len(ids),
        "anchors_never_in_judgement_rows": unused,
        "anchors_never_in_judgement_rows_count": len(unused),
        "zero_sigma_anchor_count": len(zero_sigma),
        "zero_sigma_anchors": zero_sigma,
        "p11_mentioned_files": len(p11_files),
        "p11_judgement_rows": len(p11_gates),
        "p11_books": p11_books,
        "final_suffix_distribution": dict(suffix),
        "counts_fail_sum": fail_sum,
        "positive_final_count": len(positive),
        "conclusion_ever_changed": len(positive) > 0,
        "note_on_positive": "按 final 后缀判定；册名含 BREAKTHROUGH-LOCATION 不算判正",
    }


# ---------------------------------------------------------------- 二、来料勘误
REPO_P11 = {
    "value": "2.4e34", "sigma": "0", "unit": "yr", "kind": "measured-bound",
    "source_as_registered": "Super-K 2024（arXiv:2410.19045）/ GAQ-UFT V50",
}
EXT_P11 = {
    "value": "2.4e34", "unit": "yr", "confidence": "90% CL",
    "source": "Super-Kamiokande Collaboration, arXiv:2010.16098, "
              "Phys. Rev. D 103 (2021) 012008; 450 kton-yr exposure",
    "url": "https://arxiv.org/abs/2010.16098",
    "kind": "experiment",
}
ERRATUM = {
    "registered_source_actual_title": "How fast can protons decay? "
                                      "(Davoudiasl & Denton, arXiv:2410.19045, 2024/2025)",
    "registered_source_actual_kind": "hep-ph theory paper; reports no p -> e+ pi0 lifetime limit",
    "correct_primary_source": EXT_P11["source"],
    "action": "登记勘误，不回写来料总表原件（避免破坏 43 册两路机拼与快照不变量）",
}

# ---------------------------------------------------------------- 三、可翻转判据
TAU_BOUND = D("2.4e34")          # 外部实验下界 yr
TAU_PRED = D("4.589e31")         # 仓库既有最小 SU(5) 估计，非本轮独立复算
TAU_PRED_SOURCE = "R1 _ALG_all_directions_recompute_2026-11-09.json :: B-SU5-PROTON"
HYPERK_BOUND = D("1e35")         # Hyper-K 10 年预期灵敏度（公开一手转述）
WEAK_BOUND = D("1e31")           # 假想弱下界，仅用于翻转演示


def gate(tau_bound):
    """单侧下界判据：tau_pred < tau_bound ⇒ EXCLUDED；否则 SURVIVES（非证实）。

    与旧链不同：这里没有 p_free=0、没有双侧 sigma、没有 obs_type 过滤。
    """
    excluded = TAU_PRED < tau_bound
    factor = tau_bound / TAU_PRED if TAU_PRED != 0 else None
    return {
        "tau_bound_yr": sci(tau_bound),
        "tau_pred_yr": sci(TAU_PRED),
        "state": "EXCLUDED" if excluded else "SURVIVES",
        "exclusion_factor": sci(factor) if factor else None,
        "exclusion_dex": sci(dex(factor), 6) if factor and factor > 0 else None,
        "M_X_uplift_needed": sci(factor ** (D(1) / D(4)), 6) if excluded else None,
        "alpha_GUT_reduction_needed": sci(factor.sqrt(), 6) if excluded else None,
    }


def cross_round_readings():
    """把自审引用的跨册读数也机读进来，避免正文手抄数字。"""
    out = {}
    p9 = os.path.join(DATA, "_ALG_information_gate_recompute_2026-11-12.json")
    p26 = os.path.join(DATA, "_ALG_r26_fullscope_recompute_2026-11-15.json")
    if os.path.exists(p9):
        k = json.load(open(p9, encoding="utf-8"))["key_numbers"]
        out["r9"] = {"models_satisfying_target": k.get("models_satisfying_target"),
                     "mus": k.get("mus"),
                     "sat_after_dropping_each": k.get("sat_after_dropping_each")}
    if os.path.exists(p26):
        k = json.load(open(p26, encoding="utf-8"))["key_numbers"]
        out["r26"] = {"single_removal_changed": k.get("single_removal_changed"),
                      "break_books": k.get("break_books"),
                      "min_cover": k.get("min_cover")}
    return out


def pct(n, d):
    return format(D(n) * 100 / D(d), ".2f")


def render_md(o):
    a = o["self_audit"]
    g = o["flip_states"]
    cr = o["cross_round_readings"]
    r9 = cr.get("r9", {})
    r26 = cr.get("r26", {})
    L = []
    L.append("# 算法联盟 · 方向自审与攻击面重定向")
    L.append("")
    L.append("> 日期：2026-11-16 · **非判定册** · 不占 RID · 不入 README · 不回写任何既有产物")
    L.append("> 判词：`%s`" % o["verdict"])
    L.append("")
    L.append("## 0. 对两个问题的直接回答")
    L.append("")
    L.append("**「写这么多真的是正确的吗」**：内部一致性是对的——两路机拼、反噬、幂等、快照零漂移都真实可复核；"
             "但「正确」被严格限定在**自设判据内部**，不是关于物理实在的外部有效性。本次外部核查还查出 1 处确凿的来料出处错误（见第 3 节）。"
             "因此准确说法是：**计算无误，有效性未验证，且已发现至少一处输入错误**。")
    L.append("")
    L.append("**「方向是否错误」**：是。错在五处结构性偏斜（第 2 节），它们都不是算错，而是**问错了对象**。"
             "最硬的一条：自设的「双侧 sigma」门槛把 GUT 领域最锋利的单侧下界实验判负量挡在攻击面之外。")
    L.append("")
    L.append("**「重新攻破」**：不再按旧范式追加判定册（并行会话已有 R27／R28 与第 29／30 轮，本次快照已计入）。"
             "改为换战场——具体模型 × 外部一手读数 × 可翻转判据 × 外部裁决，"
             "并在第 7 节落地一个**结论会随实验读数改变**的机核，与前 %s 册恒定结论形成对照。" % a["n_books"])
    L.append("")
    L.append("## 1. 机读自审读数")
    L.append("")
    L.append("实时快照：判定册 `%s` 册、report `%s` 份、来料锚 `%s` 项。"
             "册数含并行会话新增册，按既有纪律不与本链相加。" % (
                 a["n_books"], a["n_reports"], a["n_anchors"]))
    L.append("")
    L.append("| 读数 | 值 | 含义 |")
    L.append("|---|---|---|")
    L.append("| 从未进入任何判据行的锚 | `%s` 项（%s%%） | 来料是清单，不是判据 |" % (
        a["anchors_never_in_judgement_rows_count"],
        pct(a["anchors_never_in_judgement_rows_count"], a["n_anchors"])))
    L.append("| `sigma=0` 的锚 | `%s` 项（%s%%） | 其中含质子衰变下界 P11 |" % (
        a["zero_sigma_anchor_count"], pct(a["zero_sigma_anchor_count"], a["n_anchors"])))
    L.append("| P11 出现文件数 | `%s` | 文本提及不等于承重 |" % a["p11_mentioned_files"])
    L.append("| P11 判据行数 | `%s`，分布在 `%s` 册 | 全部集中在 11-09～11-14 |" % (
        a["p11_judgement_rows"], len(a["p11_books"])))
    L.append("| `final` 后缀分布 | `%s` | 只有两种，都是 GATES-PASS |" % (
        str(a["final_suffix_distribution"])))
    L.append("| `counts.FAIL` 合计 | `%s` | 43 册几乎恒绿 |" % a["counts_fail_sum"])
    L.append("| 判正册数 / 结论曾改变 | `%s` / `%s` | 程序结构上不可翻转 |" % (
        a["positive_final_count"], "是" if a["conclusion_ever_changed"] else "否"))
    L.append("| R9 目标满足构型 / MUS | `%s` / `%s` | 证明的是自设公理集不相容 |" % (
        r9.get("models_satisfying_target"), r9.get("mus")))
    L.append("| R26 移除单册后读数变化 | `%s` 册 | 当时写成洞见，实为「不产生新信息」的诊断 |" % (
        r26.get("single_removal_changed")))
    L.append("")
    L.append("## 2. 五条结构性偏斜")
    L.append("")
    L.append("1. **任务替换**。原始诉求是「攻破统一场论、发现本源方程」；自第三轮起被改写为自设公理集 "
             "`C1∧C2∧C3∧C4` 的可认证性。R9 在 128 个真值指派上得满足构型 `%s`、MUS `%s`，"
             "去掉 A2／A3／A5／I1 各得 1 个满足构型——这证明的是**助手自己写的目标不相容**，"
             "不是「统一场论不可攻破」。此后三十余册都在同一改写框架内换判据，结论必然仍为 0。" % (
                 r9.get("models_satisfying_target"), r9.get("mus")))
    L.append("2. **判据自设、自证、自判**。判据由本链设计，机核由本链实现，执行、验证、宣告 PASS 也由本链完成，"
             "没有外部裁决者。`VERIFY 17/17`、`42/52 守卫`、`NO-HARDCODE-OK` 审的是「机核是否按自己写的规则跑」，"
             "不是「规则是否对应物理」。反噬只能证明判据没被绕过，不能证明判据问对了问题。")
    L.append("3. **输入门槛把最硬的判负量挡在门外**。46 锚全部被提及过，但 `%s` 项从未进入任何判据行；"
             "P11 在 R1 就承重过一次（最小 SU(5) `τ_p≈4.589e31 yr` 对 `2.4e34 yr`），"
             "随后 R4 引入 `obs_type == two-sided`、R20 写 `GM-P11-ONE-SIDED-BOUND` 判其「单侧下界、σ=0」，"
             "R21／R25 又反复强调 `sigma=0` 禁当误差棒。这条纪律在统计拟合语境下正确，"
             "但把**下界／上限型实验判负量整体踢出攻击面**——而 GUT 的核心判负量恰好全是下界型"
             "（质子衰变寿命、LHC 质量下限、电偶极矩上限）。" % a["anchors_never_in_judgement_rows_count"])
    L.append("4. **结论不可翻转**。%s 册 `final` 后缀只有 `%s` 与 `%s` 两种，判正册 `%s`。"
             "R26 机读测出「移除任一单册，BREAK 读数不变」，当时写成结构性洞见；"
             "换个角度看，这正是「整条链没有产生关于物理的新信息」的诊断书。" % (
                 a["n_books"], "GATES-PASS-WITH-0-NEGATIVE",
                 "GATES-PASS-WITH-1-NEGATIVE", a["positive_final_count"]))
    L.append("5. **已知结论被包装成发现**。SM 一圈不交汇、最小 SU(5) 被质子衰变排除，都是教科书级结论。"
             "R20 的 `χ²_min=5933.430263133` 与 R1 的 `τ_p` 判负是复述，不是新物理。"
             "二十余轮增加的是审计基础设施，不是物理内容。")
    L.append("")
    L.append("## 3. 一处确凿的来料错误：P11 出处")
    L.append("")
    L.append("来料总表登记 `P11 = 2.4e34 yr`，来源标为 `Super-K 2024（arXiv:2410.19045）`。外部核查结果：")
    L.append("")
    L.append("- `arXiv:2410.19045` 实为 Davoudiasl & Denton 的理论文章《How fast can protons decay?》"
             "（2024 提交、2025 修订），讨论质子寿命在时空上可能变化，**不报告任何 `p→e⁺π⁰` 实验下界**。")
    L.append("- `2.4e34 yr (90% CL)` 的一手出处是 Super-K `arXiv:2010.16098`（PRD 2021，`450 kton·yr` 曝光）；"
             "同文另给 `p→μ⁺π⁰ > 1.6e34 yr`。")
    L.append("- 数值两路一致（相对偏离 `%s`），**来源不一致**；内部同源两路机拼永远抓不到这类错误。" % (
        o["value_relative_deviation"]))
    L.append("- 处置：**登记勘误，不回写来料总表原件**。回写会让 43 册两路机拼与既有快照整体漂移，"
             "且不属于本次授权范围。建议后续由独立一轮统一修正来源字段并复跑受影响册。")
    L.append("")
    L.append("这一条本身就是第 2 节第 2 点最直接的证据：**只有外部裁决能抓到自证循环抓不到的错误**。")
    L.append("")
    L.append("## 4. 自审过程中我自己的五次误判")
    L.append("")
    L.append("整理过程中连续出现五次「用口径或格式制造读数」，逐一记录以免再犯：")
    L.append("")
    L.append("1. 初判「46 锚里没有质子衰变下界」——错，`P11` 一直在册，只是符号写作 `tau_p_lower`。")
    L.append("2. 再判「P11 从未被承重」——错，R1 的 `B-SU5-PROTON` 就用它判负；真实情况是「早期承重 `%s` 条判据行，后期弃用」。" % a["p11_judgement_rows"])
    L.append("3. 判据行收集器只扫 `rows/gates`，漏了早期册的 `segments`，一度把承重数报成 0——"
             "字段名不统一是同一类对象错位。")
    L.append("4. 正则把并行会话册名 `BREAKTHROUGH-LOCATION` 误当「判正」，一度报 `positive_final_count=1`——"
             "改为只看 `final` 后缀后归零。")
    L.append("5. 相对偏离为 0 时仍走科学计数格式化，吐出 `0.00000000E+8`（指数 8 会被误读成 1e8）——"
             "补零值分支后改为 `0`；这正是项目里「零值禁科学计数」那条既有纪律。")
    L.append("")
    L.append("五次都在**没有外部裁决**的情况下差点变成结论。这不是自谦，是可复核的过程记录，"
             "也是为什么新方向必须把裁决权交给外部读数。")
    L.append("")
    L.append("## 5. 保留与废弃")
    L.append("")
    L.append("**保留（工具是对的）**：红线（数学自洽 ≠ 实验证实、不宣称攻破）；异源两路机拼；"
             "反噬与正负双对照；幂等复跑与快照零漂移；精确 `Decimal/Fraction` 算术纪律；"
             "防重复计数；「未被满足 ≠ 不可满足」；「同源存档回验不是独立复算」。")
    L.append("")
    L.append("**废弃（用法错了）**：把自设公理集当作「攻破」的定义；`obs_type == two-sided` 硬门槛；"
             "`GATES-PASS-*` 自盖章；每轮六件套仪式；恒定 0 的结论形式；把整理册／覆盖度也算作证据。")
    L.append("")
    L.append("## 6. 重新攻破：换战场")
    L.append("")
    L.append("四条原则：**对象**必须是物理学界真实提出的具体模型，不是「能否攻破」这个元命题；"
             "**判据**必须取外部实验读数，单侧下界与上限同样有效；"
             "**结论**必须可被数据翻转，并明确写出翻转条件；"
             "**裁决**必须外部可核查，给一手 URL，不再自盖章。")
    L.append("")
    L.append("必须同时说清：**统一场论作为研究纲领不能被一次计算「攻破」，能被攻破的是具体模型**；"
             "最小 SU(5) 早在数十年前就被质子衰变下界排除，这不是本轮功劳。"
             "真正尚未关闭的战场是带阈值修正的 SO(10)、flipped SU(5)、"
             "以及高维算符被压制的 SUSY GUT，它们的判负窗口由下一代实验给出。")
    L.append("")
    L.append("## 7. 已落地的可翻转判据")
    L.append("")
    L.append("判据定义：`%s`" % o["gate_definition"])
    L.append("")
    L.append("`τ_pred = %s yr` 取自仓库 R1 既有估计（**非本轮独立复算**，4 位有效数字）。" % (
        g[0]["tau_pred_yr"]))
    L.append("")
    L.append("| 外部下界 | 判定 | 排除倍数 | 数量级 |")
    L.append("|---|---|---|---|")
    for s in g:
        L.append("| `%s yr` | %s | `%s` | `%s` |" % (
            s["tau_bound_yr"], s["state"], s["exclusion_factor"], s["exclusion_dex"]))
    L.append("")
    L.append("**翻转演示成立 = `%s`**：把下界从 `2.4e34` 换成假想弱下界 `1e31`，"
             "同一个 `τ_pred` 的判词由 `EXCLUDED` 变为 `SURVIVES`。"
             "这是 43 册里从未出现过的性质——结论随外部读数改变。" % o["flip_demonstration_works"])
    L.append("")
    L.append("标度律 `τ ~ M_X⁴ / α_GUT²` 给出的敏感性：要逃过当前排除线，`M_X` 需抬升 `%s` 倍，"
             "或 `α_GUT` 需降低 `%s` 倍。Hyper-K 十年预期把下界抬到 `1e35 yr`，"
             "即抬升 `%s` 倍、对应 `M_X` 下界抬升 `%s` 倍。" % (
                 g[0]["M_X_uplift_needed"], g[0]["alpha_GUT_reduction_needed"],
                 o["hyperk_bound_uplift_factor"], o["hyperk_M_X_uplift_factor"]))
    L.append("")
    L.append("**正信号翻转条件**：若实验观测到 `p→e⁺π⁰` 事例并给出有限寿命，判词由 `EXCLUDED` "
             "翻为 `POSITIVE-SIGNAL`；那将是大一统的强证据，而不是本册结论。"
             "判词不再恒定，是新方向与前 43 册的根本区别。")
    L.append("")
    L.append("## 8. 边界与红线")
    L.append("")
    for b in o["boundary"]:
        L.append("- %s" % b)
    L.append("")
    L.append("**红线**：%s" % o["red_line"])
    L.append("")
    L.append("## 9. 交付物与下一步")
    L.append("")
    L.append("本轮刻意只产 3 件，不产六件套：`算法联盟_方向自审与攻击面重定向_2026-11-16.md`（本文件）、"
             "`源码/_alg_redirect_falsifiable_recompute.py`、`数据/_ALG_redirect_falsifiable_recompute_2026-11-16.json`。")
    L.append("")
    L.append("下一步（按外部读数驱动，不再按册数驱动）：把单侧判据推广到 `p→μ⁺π⁰`、`p→K⁺ν̄`、"
             "LHC 质量下限与电偶极矩上限；每个具体模型给出明确翻转阈值；"
             "实验结果更新时重跑，让判词真的有机会改变。")
    L.append("")
    return "\n".join(L) + "\n"


def main():
    audit = self_audit()
    cross = cross_round_readings()
    value_match = REPO_P11["value"] == EXT_P11["value"]
    value_rel = (abs(D(REPO_P11["value"]) - D(EXT_P11["value"]))
                 / D(EXT_P11["value"]))
    source_match = ("2010.16098" in REPO_P11["source_as_registered"])
    base = gate(TAU_BOUND)
    hyperk = gate(HYPERK_BOUND)
    weak = gate(WEAK_BOUND)
    flip_states = [base, hyperk, weak]
    flip_works = len({s["state"] for s in flip_states}) > 1
    bound_uplift = HYPERK_BOUND / TAU_BOUND

    verdict = ("REDIRECT__BOOKS-%s__UNUSED-ANCHORS-%s__SRC-MISMATCH-%s__"
               "SU5-%s__FLIP-STATES-%s__CONSTANT-VERDICT-%s" % (
                   audit["n_books"], audit["anchors_never_in_judgement_rows_count"],
                   0 if source_match else 1, base["state"],
                   len({s["state"] for s in flip_states}),
                   0 if flip_works else 1))

    out = {
        "date": "2026-11-16",
        "title": "方向自审与攻击面重定向 · 可翻转判据（非判定册）",
        "kind": "direction-audit-and-falsifiable-gate",
        "verdict": verdict,
        "self_audit": audit,
        "cross_round_readings": cross,
        "erratum_P11": ERRATUM,
        "external_p11": EXT_P11,
        "repository_p11": REPO_P11,
        "value_match_two_path": bool(value_match),
        "value_relative_deviation": sci(value_rel, 8),
        "source_match_external_check": bool(source_match),
        "tau_pred_source": TAU_PRED_SOURCE,
        "tau_pred_is_independent_recompute": False,
        "gate_definition": "tau_pred < tau_bound -> EXCLUDED; else SURVIVES (not confirmed). "
                           "One-sided bounds accepted; no p_free axiom, no two-sided sigma filter.",
        "flip_states": flip_states,
        "flip_demonstration_works": bool(flip_works),
        "hyperk_bound_uplift_factor": sci(bound_uplift, 6),
        "hyperk_M_X_uplift_factor": sci(bound_uplift ** (D(1) / D(4)), 6),
        "positive_signal_flip_condition": "若实验观测到 p -> e+ pi0 事例并给出有限寿命，"
                                          "判词由 EXCLUDED 翻为 POSITIVE-SIGNAL；"
                                          "这是大一统的强证据，不是本册结论",
        "boundary": [
            "tau_pred 取仓库既有估计（4 位有效数字），非本轮独立复算；"
            "GUT 质子寿命理论不确定度约 2-3 个数量级（强子矩阵元、阈值修正、高维算符）。",
            "标度律 tau ~ M_X^4 / alpha_GUT^2 是量纲级估计，不是精确预言；"
            "排除结论对 2.72 个数量级的余量稳健，但对具体模型参数不稳健。",
            "最小 SU(5) 被质子衰变排除是教科书级已知结论，不是本轮新发现。",
            "「未被满足 != 不可满足」；存活不等于被证实。",
        ],
        "red_line": "数学自洽 != 实验证实；本轮不宣称攻破统一场论，"
                    "不宣称发现新方程或独立实验预言；四力统一未证。",
        "discipline": ["不占 RID", "不入 README", "不回写既有产物",
                       "不自设公理集", "不做自盖章守卫", "来源给一手 URL 供外部核查"],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as f:
        f.write(render_md(out))

    print("VERDICT =", verdict)
    print("\n[方向自审]")
    for k in ("n_books", "n_reports", "n_anchors",
              "anchors_never_in_judgement_rows_count", "zero_sigma_anchor_count",
              "p11_mentioned_files", "p11_judgement_rows", "counts_fail_sum",
              "positive_final_count", "conclusion_ever_changed"):
        print("  %-40s = %s" % (k, audit[k]))
    print("  final_suffix_distribution =", audit["final_suffix_distribution"])
    print("  p11_books =", audit["p11_books"])
    print("\n[来料勘误]")
    print("  value_match_two_path =", value_match)
    print("  source_match_external_check =", source_match)
    print("  登记来源实为 =", ERRATUM["registered_source_actual_title"])
    print("\n[可翻转判据]")
    for s in flip_states:
        print("  bound=%-12s state=%-9s factor=%-16s dex=%s" % (
            s["tau_bound_yr"], s["state"], s["exclusion_factor"], s["exclusion_dex"]))
    print("  flip_demonstration_works =", flip_works)
    print("  M_X 需抬升 =", base["M_X_uplift_needed"],
          " / alpha_GUT 需降低 =", base["alpha_GUT_reduction_needed"])
    print("  Hyper-K 下界抬升 =", sci(bound_uplift, 6), "倍")
    print("\nJSON =", OUT_JSON, os.path.getsize(OUT_JSON), "B")
    return out


if __name__ == "__main__":
    main()
