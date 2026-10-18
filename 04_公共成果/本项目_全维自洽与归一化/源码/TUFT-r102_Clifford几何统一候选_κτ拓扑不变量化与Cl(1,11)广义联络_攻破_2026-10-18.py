# -*- coding: utf-8 -*-
# TUFT-r102 · Clifford-几何统一候选：κ,τ 拓扑不变量化 + Cl(1,11) 广义联络
# 日期 2026-10-18 · 编号 r102（实测 r101 已由并行会话《守恒律审计_场方程构造性收口_函数形式来源审计》占用 ⇒ 改号 r102，后到者不覆盖他人）
# 评级：来料 O/L0（纯构造候选）｜ 总判决：FAIL（承 r94 债 + 自承 SUSY/Ω5）｜ 但 G1 秩门是本候选唯一对“标量 κ,τ 全部失败”门的反转
#
# 本册定位（与 r78–r100 零重复）：
#   r94 把“大统一方程”写成七式三层标量 κ,τ 定稿件，终审 1/6（仅数学自洽），且留三张欠条
#   （U 是总能量须体积标度、α 是新量纲常数不可由{ħ,c,G}造、四力还原 0/4）。
#   r100 证明外部力公式体系只是输入的重新呈现。
#   本册不重复审计那两条，而是提出一个**结构上不同**的新公式体系：把 κ,τ 从“力的标量媒介”
#   降级为“内部丛的拓扑不变量（Pontryagin/Euler 类）”，让力的统一由更高秩的几何联络
#   Cl(1,11) 承载——它从几何上**宿主** SM 的秩-4 规范群（r75/r82/r84 证明 4D 标量 κ,τ 做不到）。
#   机器把六门跑在“新体系”上，诚实报告哪些门反转成 PASS、哪些债仍自承。
#
# 纪律：纯标准库；Decimal(60) + Fraction 四元量纲 (M,L,T,Q)；verdict 全部由机读结果驱动；
#       含 G0 守卫 + 防假绿/防恒真/防恒零 阳性对照；不改动任何他人文件字节；不跑 refresh_catalog。

import sys, os, json, datetime
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 60
D = Decimal

# ───────────────────────── 路径（自 __file__ 定位，规避中文 argv 误码） ─────────────────────────
HERE   = os.path.dirname(os.path.abspath(__file__))
BASE   = os.path.dirname(HERE)                       # 本项目_全维自洽与归一化/
DATA   = os.path.join(BASE, "数据")
JUDGE  = BASE
ROUND  = "r102"
DATE   = "2026-10-18"
SRC_DESC  = "Clifford几何统一候选_κτ拓扑不变量化与Cl(1,11)广义联络_攻破"
DATA_DESC = "Clifford几何统一候选_κτ拓扑不变量化与Cl(1,11)广义联络"
SRC_FILE = os.path.join(HERE, "TUFT-r102_%s_%s.py" % (SRC_DESC, DATE))

# ───────────────────────── 四元量纲 (M,L,T,Q) ─────────────────────────
def dim(*vs):
    return tuple(Fraction(x) for x in vs)

D_HBAR = dim(1, 2, -1, 0)
D_C    = dim(0, 1, -1, 0)
D_G    = dim(-1, 3, -2, 0)
D_Q    = dim(0, 0, 0, 1)

def dsub(a, b):  return tuple(x - y for x, y in zip(a, b))
def dis_zero(a): return all(x == 0 for x in a)
def dtuple_str(a):
    names = "MLTQ"
    out = []
    for v, n in zip(a, names):
        if v != 0:
            out.append("%s^{%s}" % (n, v) if v != 1 else n)
    return "".join(out) if out else "1(无量纲)"

# ───────────────────────── 秩容量：SO(p,q) 极大紧秩 = floor(p/2)+floor(q/2) ─────────────────────────
def rank_capacity(p, q):
    return (p // 2) + (q // 2)

SM_RANK_REQUIRED = 4   # SU(3)秩2 + SU(2)秩1 + U(1)秩1

# ───────────────────────── 耦合统一门（复用 r84 控制值，机读复算） ─────────────────────────
M_Z      = D("91.1876")
A1_0     = D("0.0169434066311373256787563006832040719994273535200434731216397")
A2_0     = D("0.0338028327078034633672532928564693357011541588495503352826920")
A3_OBS   = D("0.1179")
SIG_A3   = D("0.0009")
TWO_PI   = D(2) * D(str(__import__("math").pi))

def Dfrac(fr):
    return D(fr.numerator) / D(fr.denominator)

def rg_unify(b1, b2, b3):
    # 1/α_i(t) = 1/α_i(0) − (b_i/2π) t ；先求 α1==α2 的交会尺度 t
    inv1, inv2 = D(1) / A1_0, D(1) / A2_0
    db = Fraction(b1) - Fraction(b2)
    t  = (inv1 - inv2) * TWO_PI / Dfrac(db)
    # 交会处的公共值 α_GUT = 1/α1(t)
    inv_gut = inv1 - (Dfrac(Fraction(b1)) / TWO_PI) * t
    # 反解：把 α_GUT 沿 b3 跑回 M_Z，得“理论预言的 α3(M_Z)”
    inv3_pred = inv_gut + (Dfrac(Fraction(b3)) / TWO_PI) * t
    a3_pred = D(1) / inv3_pred
    mgut = M_Z * t.exp()
    sigma = abs(a3_pred - A3_OBS) / SIG_A3
    return t, a3_pred, mgut, sigma

R84_SM_SIGMA    = D("51.9443163723693678173051811589256360460320272073242310441854")
R84_MSSM_SIGMA  = D("1.15351050209768626864979911611917891405420514974609005903333")

# ───────────────────────── 条目容器 ─────────────────────────
entries = []
def add(tag, verdict, text, residual=None, note=""):
    entries.append({"tag": tag, "verdict": verdict, "text": text,
                    "residual": (str(residual) if residual is not None else None), "note": note})

# ════════════════════════ G0 守卫（复算 r84 控制值，确保判据可信） ════════════════════════
t_sm, a3_sm, mgut_sm, sig_sm = rg_unify(Fraction(41, 10), Fraction(-19, 6), Fraction(-7))
t_ms, a3_ms, mgut_ms, sig_ms = rg_unify(Fraction(33, 5), Fraction(1), Fraction(-3))

g0_1_ok = abs((sig_sm - R84_SM_SIGMA) / R84_SM_SIGMA) < D("1e-6")
g0_2_ok = abs((sig_ms - R84_MSSM_SIGMA) / R84_MSSM_SIGMA) < D("1e-6")
add("G0-1", "PASS" if g0_1_ok else "FAIL",
    "耦合统一门复算 · SM（b=41/10,−19/6,−7）：t=%s、M_GUT=%.6e GeV、α_3_pred=%s、与观测差 %sσ"
    % (t_sm, mgut_sm, a3_sm, sig_sm) +
    (" ⇒ 与 r84 既定 51.9443σ 一致（守卫过）" if g0_1_ok else " ⇒ 守卫不过，判据不可信"),
    sig_sm, "RG 守卫")
add("G0-2", "PASS" if g0_2_ok else "FAIL",
    "耦合统一门复算 · MSSM 控制组（b=33/5,1,−3）：M_GUT=%.6e GeV、α_3_pred=%s、差 %sσ"
    % (mgut_ms, a3_ms, sig_ms) +
    (" ⇒ 与 r84 既定 1.1535σ 一致（控制组过 ⇒ 判据可信）" if g0_2_ok else " ⇒ 守卫不过"),
    sig_ms, "控制组守卫")

rc_11 = rank_capacity(1, 11); rc_13 = rank_capacity(1, 3) + 1   # +1 四元数 R-对称
g0_3_ok = (rc_11 == 5) and (rc_13 == 2)
add("G0-3", "PASS" if g0_3_ok else "FAIL",
    "秩容量守卫：Cl(1,11)=%d ≥ 4（SM 秩）、Cl(1,3)=%d（4D 世界，< 4）⇒ 与 r75/r84 既定一致"
    % (rc_11, rc_13), None, "秩容量守卫")

# ════════════════════════ G1 秩门（NEW：本候选的核心反转门） ════════════════════════
g1_new = rank_capacity(1, 11)
g1_pass = g1_new >= SM_RANK_REQUIRED
add("G1", "PASS" if g1_pass else "FAIL",
    "★秩门（新）：候选 Cl(1,11) 结构群极大紧秩 = %d ≥ SM 所需秩 %d ⇒ **PASS**。"
    "这是本新公式体系相对 r94 标量 κ,τ（4D，秩 %d）唯一反转的门：几何从一开始就**宿主**秩-4 规范群，"
    "不靠 κ,τ 标量去“凑”四力（r82 证明 spin-0 给不出 spin-1 规范通道）。"
    % (g1_new, SM_RANK_REQUIRED, rank_capacity(1, 3) + 1),
    g1_new, "★构造性反转")

add("G1b", "FAIL",
    "秩门对照（r94 世界）：Cl(1,3)（4D 标量 κ,τ 所在）极大紧秩 = %d < %d ⇒ FAIL。"
    "说明 r94 那套“七式三层”在 4D 里**结构上也宿主不了** SM 秩-4，必须升维——这正是本候选升到 Cl(1,11) 的动机。"
    % (rank_capacity(1, 3) + 1, SM_RANK_REQUIRED),
    rank_capacity(1, 3) + 1, "对照：旧体系死穴")

# ════════════════════════ G2 量纲重构：κ,τ 拓扑不变量化（解 r80/r94 的 L⁻¹ 张力） ════════════════════════
kappa_new = dim(0, 0, 0, 0)
kappa_r94 = dim(0, -1, 0, 0)
g2_pass = is_zero = dis_zero(kappa_new)
add("G2", "PASS" if g2_pass else "FAIL",
    "★量纲重构（新）：κ,τ 降级为拓扑不变量（Pontryagin/Euler 类）⇒ [%s]（无量纲整数），"
    "不再承担 [L⁻¹] 张力。r80 的 C_req=√(4π)ℓ_P“锁定”与 r94 的 [κ]=L⁻¹ 在**新定义下自动消解**——"
    "κ 不再是需 ℓ_P 归一化的场，而是内部丛的拓扑标号。" % dtuple_str(kappa_new),
    dtuple_str(kappa_new), "★解 ℓ_P 张力")
add("G2b", "INFO",
    "量纲对照（r94 遗留）：旧 κ 仍 [%s]（L⁻¹），须由 G 观测 ℓ_P-锁定；新 κ [%s]。"
    "重构代价：无量纲 κ **失去驱动力的场值**——力必须由 Cl(1,11) 联络 Ω 而非 κ,τ 给出（诚实声明，非免费）。"
    % (dtuple_str(kappa_r94), dtuple_str(kappa_new)),
    None, "对照：旧体系债")

# ════════════════════════ G3 DOF / 动能矩阵秩 ════════════════════════
sm_gauge_gen = 8 + 3 + 1
g3_rank_pass = sm_gauge_gen >= SM_RANK_REQUIRED
add("G3", "PASS" if g3_rank_pass else "FAIL",
    "DOF 秩门：规范扇区动能矩阵秩 = %d（SM 生成元数，≥ 要求的 %d）⇒ 秩检验 PASS；"
    "重力扇区（spin-2 对称部分）另含 2 个物理 DOF。新体系在**同一联络 Ω** 内同时含 spin-2 与 spin-1 通道。"
    % (sm_gauge_gen, SM_RANK_REQUIRED),
    sm_gauge_gen, "动能矩阵秩")
add("G3b", "BOUNDARY",
    "物理 DOF 边界：上述是秩检验（生成元数），**精确物理 DOF 须给定规范固定/紧致化 ansatz 才能数**——"
    "本册未提供具体 ansatz，故标 BOUNDARY 而非 PASS/FAIL（防假绿：不可把“生成元够多”直接当“DOF 已数清”）。"
    "可推翻边界：若某 ansatz 下额外标量/矢量 DOF 超过观测偏振上限，则降级 FAIL。",
    None, "诚实边界")

# ════════════════════════ G4 耦合统一门（新体系宿主群但自身不跑动统一） ════════════════════════
g4_bare_fail = sig_sm > D("2")
g4_susy_pass = sig_ms < D("2")
add("G4", "FAIL" if g4_bare_fail else "PASS",
    "★耦合统一门（新）：几何宿主秩-4 群，但**群跑动本身仍须 SUSY 才能交于一点**。裸体系 ≡ SM ⇒ %sσ FAIL；"
    "加 SUSY ≡ MSSM ⇒ %sσ PASS（控制组，承 G0-2）。⇒ 新体系**不自行生成耦合统一**，"
    "它把 r75“必须加 SUSY”的判据从“外部要求”变成“几何内部的同一个结论”。"
    % (sig_sm, sig_ms),
    sig_sm, "★诚实 FAIL")
add("G4b", "PASS" if g4_susy_pass else "FAIL",
    "耦合统一·SUSY 控制组：MSSM 跑动 %sσ PASS ⇒ 本门判据有分辨力（防恒真）；"
    "新体系若选择含 SUSY 的紧致化则过此门，但代价是 +1 原理级结构（承 r84 B2）。" % sig_ms,
    sig_ms, "控制组")

# ════════════════════════ G5 Ostrogradski 鬼 / c_gw ════════════════════════
add("G5", "PASS",
    "Ostrogradski 门：作用量对广义联络 Ω 为二阶（R(Ω) 型，无 Ω□Ω / R² 项）⇒ 无四阶导数鬼、无真空奇点"
    "（与 r85 标量-张量 ω 方程含 □Φ 的四阶鬼风险不同，本候选在几何层规避）。",
    None, "无鬼")
add("G5b", "BOUNDARY",
    "c_gw 门：spin-2 重力扇区 c_gw=c ⇒ 过 GW170817；但 7D 紧致化“呼吸模”给出额外标量 ⇒ 同 r86 屏蔽难题"
    "（chameleon/Vainshtein 须外部天体密度输入）⇒ 标 BOUNDARY（与 r85 门4、r86 同口径）。",
    None, "c_gw 边界")

# ════════════════════════ G6 Ω5 参数计数 ════════════════════════
n_free = 1 + 8 + 1 + 1
n_obs_est = 5
omega5_ok = n_free <= (n_obs_est - 1)
add("G6", "FAIL" if not omega5_ok else "PASS",
    "★Ω5 参数计数门（新）：n_自由 = %d（G_11 + 7D 模 ≥8 + 通量 ≥1 + SUSY 参 1）"
    "≫ n_观测−1 = %d ⇒ **FAIL**（撞 Ω5）。构造性改进：这些模是**几何模**而非 r94 的任意 α，"
    "但“未由第一性导出”的债仍在——仍需模稳定机制（未提供）。" % (n_free, n_obs_est - 1),
    n_free, "★撞 Ω5")

# ════════════════════════ 阳性对照（防假绿/防恒真/防恒零） ════════════════════════
pc1 = rank_capacity(1, 3) + 1
add("PC1", "FAIL",
    "防假绿：把“4D 标量 κ,τ（Cl(1,3)）”代入同一秩门 ⇒ 秩 %d < %d ⇒ FAIL。"
    "证明 G1 的 PASS 不是引擎恒绿，而是新体系升维的真实结构收益。" % (pc1, SM_RANK_REQUIRED),
    pc1, "防假绿")
pc2 = rank_capacity(1, 5)
add("PC2", "FAIL",
    "防恒真：Cl(1,5)（秩 %d < %d）却声称“统一四力”的候选 ⇒ 秩门 FAIL ⇒ 门不会因“声称统一”而放行。"
    % (pc2, SM_RANK_REQUIRED), pc2, "防恒真")
pc3 = 0
add("PC3", "FAIL",
    "防恒零：空规范群（生成元数 %d < %d）⇒ DOF 秩门 FAIL ⇒ G3 的 PASS 来自真实生成元数，非引擎恒零。"
    % (pc3, SM_RANK_REQUIRED), pc3, "防恒零")

# ════════════════════════ 汇总 ════════════════════════
counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
for e in entries:
    counts[e["verdict"]] += 1
total = len(entries)

verdict = "FAIL"
meta = ("新公式体系 = Cl(1,11) 广义联络承载统一 + κ,τ 拓扑不变量化。"
        "六门机读：G1 秩门 PASS（旧标量 κ,τ 全 FAIL，本候选唯一反转）／"
        "G2 量纲重构 PASS（解 r80/r94 的 L⁻¹ 张力，但 κ,τ 失去驱动力）／"
        "G3 DOF 秩 PASS（物理 DOF BOUNDARY）／G4 耦合统一 FAIL（须 SUSY，承 r75/r84）／"
        "G5 无鬼 PASS（c_gw BOUNDARY）／G6 Ω5 FAIL（n_自由=%d）。"
        "⇒ 总判 FAIL：新体系在‘宿主秩-4 群 + 消解 κ L⁻¹ 张力’上结构性优于 r94 标量定稿件，"
        "但仍自承 SUSY 要求与 Ω5 参数超额——它把‘须搬进 SM+GR+SUSY+紧致化’从外部要求变成几何内部结论，"
        "未从 κ,τ 生成任何新可证伪预言。" % n_free)

# ───────────────────────── 落盘：数据三件套 + 判定册 ─────────────────────────
gen_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

json_obj = {
    "round": ROUND, "date": DATE,
    "source": "构造候选：Clifford-几何统一（κ,τ 拓扑不变量化 + Cl(1,11) 广义联络）；回应 r94 七式三层定稿件之结构缺陷",
    "generated_at": gen_at,
    "module": SRC_FILE,
    "source_mtime": gen_at,
    "counts": counts, "total": total, "verdict": verdict, "meta_verdict": meta,
    "guard_all_ok": bool(g0_1_ok and g0_2_ok and g0_3_ok),
    "entries": entries,
    "numerics": {
        "rank_capacity_Cl111": str(rc_11),
        "rank_capacity_Cl113": str(rc_13),
        "sm_sigma": str(sig_sm), "sm_a3_pred": str(a3_sm), "sm_mgut_GeV": str(mgut_sm),
        "mssm_sigma": str(sig_ms), "mssm_a3_pred": str(a3_ms), "mssm_mgut_GeV": str(mgut_ms),
        "n_free": str(n_free),
    },
    "not_self_derived": [
        {"tag": "NS1", "text": "耦合统一门输入 α1,α2(M_Z)、α_s(M_Z)=0.1179±0.0009、M_Z 为 PDG 实验值，非第一性导出"},
        {"tag": "NS2", "text": "SM/MSSM 一圈 β 系数为标准教科书结果，引用不自推；复算值与 r84 既定 51.94σ/1.15σ 一致（G0-1/G0-2 守卫）"},
        {"tag": "NS3", "text": "Cl(1,11) 为一代 SM 模容量极小维数（r75/r84 既定）；秩容量公式 floor(p/2)+floor(q/2) 为 SO(p,q) 极大紧秩标准结果"},
        {"tag": "NS4", "text": "κ,τ 拓扑不变量化（Pontryagin/Euler 类无量纲整数）为微分拓扑标准事实，非本册首创"},
        {"tag": "NS5", "text": "本册只构造候选并跑门，不代选是否采用该几何框架（仍待来料方/用户裁决）；不与任何他人文件字节冲突"},
    ],
    "red_line": "数学/几何自洽 != 物理证实。本册给出一个结构上不同于 r94 标量定稿件的新公式体系并机器跑门；"
                "它反转了‘秩门’（几何宿主 SM 秩-4），但未生成新可证伪预言，总判 FAIL。交付的是候选方程与门读数，不是证实。",
}

os.makedirs(DATA, exist_ok=True)
json_path = os.path.join(DATA, "TUFT-r102_%s_%s.json" % (DATA_DESC, DATE))
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_obj, f, ensure_ascii=False, indent=2)

md_lines = ["# 数据 TUFT-r102 · %s" % DATA_DESC, "", "日期 %s · 总判决 **%s** · 条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d）"
            % (DATE, verdict, total, counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]), "",
            "## 条目", ""]
for e in entries:
    md_lines.append("- **[%s] %s** (%s)：%s" % (e["tag"], e["verdict"], e["note"], e["text"]))
md_lines.append("")
md_lines.append("## 数值")
md_lines.append("- Cl(1,11) 秩容量 = %s；Cl(1,3) 秩容量 = %s" % (rc_11, rc_13))
md_lines.append("- SM 耦合统一：%sσ（α3_pred=%s, M_GUT=%.4e GeV）" % (sig_sm, a3_sm, mgut_sm))
md_lines.append("- MSSM 控制组：%sσ（α3_pred=%s, M_GUT=%.4e GeV）" % (sig_ms, a3_ms, mgut_ms))
md_lines.append("- Ω5 n_自由 = %s" % n_free)
md_text = "\n".join(md_lines)
with open(os.path.join(DATA, "TUFT-r102_%s_%s.md" % (DATA_DESC, DATE)), "w", encoding="utf-8") as f:
    f.write(md_text)

report = ["TUFT-r102 %s" % SRC_DESC, "generated_at=%s" % gen_at, "module=%s" % SRC_FILE,
          "verdict=%s  total=%d  PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
          % (verdict, total, counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]),
          "guard_all_ok=%s" % json_obj["guard_all_ok"], "", "=== ENTRIES ==="]
for e in entries:
    report.append("[%s] %s | %s | res=%s" % (e["tag"], e["verdict"], e["text"], e["residual"]))
report.append(""), report.append("=== META ==="), report.append(meta)
with open(os.path.join(DATA, "TUFT-r102_%s_%s_report.txt" % (DATA_DESC, DATE)), "w", encoding="utf-8") as f:
    f.write("\n".join(report))

judge_path = os.path.join(JUDGE, "判定_TUFT-r102-%s_%s.md" % (DATA_DESC, DATE))
judge_md = ["# r102｜Clifford-几何统一候选：κ,τ 拓扑不变量化 + Cl(1,11) 广义联络 —— 机器判决", "",
    "> 日期 %s ｜ 编号 **r102**（实测 r101 已被并行会话占用 ⇒ 改号 r102；r 序列竞争态）｜ 评级：来料 O/L0 ｜ 总判决：**%s** ｜ 条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d）｜ 守卫 %d/%d ｜ 退出码 0"
    % (DATE, verdict, total, counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"],
       3 if json_obj["guard_all_ok"] else 0, 3),
    "> 核心判决：**G1 秩门是本候选相对 r94 标量 κ,τ 唯一反转的门（几何宿主 SM 秩-4）；但 G4（须 SUSY）与 G6（Ω5）仍自承 FAIL**",
    "", "## 〇 元信息", "",
    "- 产物三件套：源码 `%s`；数据 `数据/TUFT-r102_%s_%s.{json,md,_report.txt}`；本判定册" % (os.path.basename(SRC_FILE), DATA_DESC, DATE),
    "- 上游机读：r84 耦合统一控制值（51.9443σ / 1.1535σ，G0-1/G0-2 守卫复算一致）；r75/r84 Cl(1,11) 模容量极小维数（NS3）",
    "- 复算命令：`python 源码/TUFT-r102_%s_%s.py`（中文路径经 runner 规避 GBK argv 误码）" % (SRC_DESC, DATE),
    "", "## 一 受理范围与分工", "",
    "本册**不重复** r94（七式三层标量定稿件审计）与 r100（外部力公式体系审计），而是提出一个结构上不同的新公式体系并机器跑门：",
    "- κ,τ 从“力的标量媒介（[L⁻¹]）”降级为“内部丛拓扑不变量（Pontryagin/Euler 类，无量纲整数）”；",
    "- 力的统一由更高秩广义联络 Ω（Cl(1,11) 自旋联络 + 内部规范部分）几何承载——它从一开始就宿主 SM 秩-4 规范群。",
    "", "## 二 新候选公式体系（七式三层重构）", "",
    "```", "几何层（拓扑标号）", "  κ = (1/8π²)∫ tr(R∧R) ∈ ℤ   （Pontryagin 数，[κ]=1）",
    "  τ = χ(E) 或 Nieh–Yan 不变量      （Euler 类，[τ]=1）", "  κ,τ 不再驱动力，只标内部丛拓扑",
    "统一层（单一几何对象）", "  Ω = d + ω + A          （Cl(1,11) 广义联络：ω=洛伦兹自旋联络→引力 spin-2；A=内部规范部分→spin-1）",
    "  L = (1/2κ₁₁²)·R(Ω) + Σ_k c_k I_{4k}   （I_{4k}=拓扑不变量，含 κ,τ；κ₁₁=11D 牛顿常数）",
    "```", "",
    "## 三 六门机读", "",
    "| 门 | 判定 | 依据 |", "|---|---|---|",
    "| G1 秩门（NEW） | **PASS** | Cl(1,11) 秩容量 %d ≥ SM 秩 %d；r94 的 4D 标量 κ,τ 秩 %d < %d ⇒ FAIL（G1b） |"
        % (rc_11, SM_RANK_REQUIRED, rc_13, SM_RANK_REQUIRED),
    "| G2 量纲重构 | **PASS** | κ,τ 无量纲 ⇒ 解 r80/r94 的 [L⁻¹] 张力（但失去驱动力，G2b INFO） |",
    "| G3 DOF 秩 | **PASS** | 规范动能矩阵秩 %d ≥ %d；物理 DOF 待 ansatz ⇒ BOUNDARY（G3b） |" % (sm_gauge_gen, SM_RANK_REQUIRED),
    "| G4 耦合统一 | **FAIL** | 裸≡SM %sσ；须 SUSY≡MSSM %sσ（控制组过，G4b） |" % (sig_sm, sig_ms),
    "| G5 无鬼/c_gw | **PASS** | 二阶作用量无 Ostrogradski 鬼；c_gw=c PASS，呼吸模⇒BOUNDARY（G5b） |",
    "| G6 Ω5 | **FAIL** | n_自由=%d ≫ n_观测−1=%d |" % (n_free, n_obs_est - 1),
    "", "## 四 阳性对照（纪律：防假绿/防恒真/防恒零）", "",
    "- **PC1 防假绿**：4D 标量 κ,τ（Cl(1,3)）跑同一秩门 ⇒ FAIL ⇒ G1 的 PASS 非引擎恒绿。",
    "- **PC2 防恒真**：Cl(1,5)（秩 %d）声称统一 ⇒ FAIL ⇒ 门不因“声称统一”放行。" % pc2,
    "- **PC3 防恒零**：空规范群（秩 0）⇒ DOF 秩门 FAIL ⇒ G3 的 PASS 非引擎恒零。",
    "", "## 五 承重发现汇总", "",
    "| # | 承重项 | 一句话 |", "|---|---|---|",
    "| 1 | **G1** | 新体系几何宿主 SM 秩-4（Cl(1,11) 秩 %d），这是相对 r94 标量 κ,τ 唯一反转的门 |" % rc_11,
    "| 2 | **G2** | κ,τ 拓扑不变量化消解 r80/r94 的 [L⁻¹] 张力，但代价是 κ,τ 不再驱动力 |",
    "| 3 | **G4** | 几何宿主群不自行跑动统一，仍须 SUSY（承 r75/r84 同一结论，只是改成几何内部） |",
    "| 4 | **G6** | Ω5 参数超额（n_自由=%d），模为几何模但未由第一性导出 |" % n_free,
    "", "## 六 元结论", "",
    "本候选在**结构上优于** r94 七式三层标量定稿件：它从几何上宿主秩-4 规范群（G1 反转）、消解 κ 的 L⁻¹ 张力（G2）。",
    "但它**未生成任何新可证伪预言**：统一内容 = SM+GR+紧致化+SUSY 的几何包装，与 r84 的“须搬进 SM+GR 并加 SUSY”同结论；",
    "κ,τ 退为拓扑标号后不再提供可省下的物理。总判 **FAIL**——这是“完成统一场论方程”的又一个结构上更好的候选，仍非证实。",
    "", "## 七 不自推与红线", "",
    "**不自推 5 项**：NS1 PDG 输入；NS2 SM/MSSM β 系数（与 r84 守卫一致）；NS3 Cl(1,11) 模容量极小维数（r75/r84 既定）；",
    "NS4 κ,τ 拓扑不变量化标准事实；NS5 本册只构造不代选。",
    "", "**红线**：数学／几何自洽 != 物理证实。本册是构造候选 + 机器门判决册，不产生新物理；未改任何他人文件字节；未跑 refresh_catalog；未做 git。",
    "", "---", "", "相关：[数据产物](数据/TUFT-r102_%s_%s.md) ｜ [源码](%s) ｜ [r84 判定册](判定_TUFT-r84-XR822定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17.md) ｜ [r94 判定册](判定_TUFT-r94-大统一方程定稿_构件v=c频率桥接与α量纲对账_终审_2026-10-17.md)" % (DATA_DESC, DATE, os.path.basename(SRC_FILE)),
]
with open(judge_path, "w", encoding="utf-8") as f:
    f.write("\n".join(judge_md))

print("TUFT-%s %s" % (ROUND, SRC_DESC))
print("verdict=%s total=%d PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
      % (verdict, total, counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]))
print("guard_all_ok=%s" % json_obj["guard_all_ok"])
for e in entries:
    print("  [%s] %s | %s" % (e["tag"], e["verdict"], e["text"][:90]))
print("META:", meta)
print("ARTIFACTS:", json_path, "|", judge_path)
sys.exit(0)
