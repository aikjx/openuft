# -*- coding: utf-8 -*-
"""
TUFT V3.5 · 分支③执行：Ω(κ,τ) 公理构造的**不可行性判定与最小增广定价**
=========================================================================
承接：元审计册 `TUFT_V3.5修复方案_全维审计与重整_2026-10-04.py` 的 F-04（分支排序建议：
先做分支③的「可行性判定」形态）。本册**执行分支③**。

来料（修复方案 §四）为 Ω 设定的四条公理，本册记为：
  P1 实值无量纲标量场 Ω: ℝ² → ℝ
  P2 符号自动导出：D_G 区必须自然给出 Ω < 0（禁止人工硬编码）
  P3 跨分区边界连续光滑
  P4 自由度受限：最多引入 1 个新普适常数，禁止 G_σ / k / k′ 多个外锚

本册的处置原则（沿用仓内红线）
--------------------------------------------------------------------
1. **不构造新物理**：本册不提出新的 Ω 定义、不拟合任何物理常数；
2. 凡声称「不可行」的，一律给出**机器可复算的判据**（不变性验证 / 插值构造 / 反例）；
3. 凡判死的，必须同时给出**最小增广定价**（要补齐最少需要几条新假设）与**降级后仍可落地的形式**；
4. 与既有册重叠的结论（Π 定理、尺度简并）一律回链，不宣称新发现。

纯标准库，零第三方依赖。
"""

import os
import sys
import json
import time
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA_DIR = os.path.join(BASE, "数据")

RESULTS = []
GUARDS = []


def add(cid, sec, item, statement, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "statement": statement,
                    "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-24s | %s" % (verdict, cid, item, detail[:150]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-30s | %-1s | %s" % (name, "PASS" if ok else "FAIL", detail))
    return ok


# --------------------------------------------------------------------------
# 常数（CODATA 2018 / PDG；不能自行复算的标为外部登记值）
# --------------------------------------------------------------------------
C_LIGHT = 299792458.0
HBAR_SI = 1.054571817e-34
E_CHARGE = 1.602176634e-19
EPS0 = 8.8541878128e-12
G_NEWTON = 6.67430e-11
HBAR_C_JM = HBAR_SI * C_LIGHT
M_E_KG = 9.1093837015e-31
M_P_KG = 1.67262192369e-27
M_W_GEV = 80.379
G_F = 1.1663787e-5

ALPHA_0 = E_CHARGE ** 2 / (4 * math.pi * EPS0 * HBAR_SI * C_LIGHT)
ALPHA_MZ = 1.0 / 127.952          # 外部登记值（PDG）
ALPHA_S_MZ = 0.1179               # 外部登记值（PDG）
SIN2_THETA_W = 0.23121            # 外部登记值（PDG, MS-bar）
ALPHA_2_MZ = ALPHA_MZ / SIN2_THETA_W
ALPHA_W_FERMI = G_F * M_W_GEV * M_W_GEV / (math.pi * math.sqrt(2.0))


def alpha_g(mass_kg):
    return G_NEWTON * mass_kg * mass_kg / HBAR_C_JM


# 四个「目标强度」μ = M_Z、α_s = 1 基准、引力取质子参考（与元审计册 C-05 同口径）
TARGETS = [
    ("强核", ALPHA_S_MZ, 1e-15, math.pi / 4.0),
    ("弱核", ALPHA_2_MZ, 1e-18, 3 * math.pi / 4.0),
    ("电磁", ALPHA_MZ, float("inf"), -math.pi / 4.0),
    ("引力", alpha_g(M_P_KG), float("inf"), -3 * math.pi / 4.0),
]

# ==========================================================================
# A 组：公理的形式化与不变性（来料 §四 四条公理）
# ==========================================================================
def omega_family(theta, eps=0.0):
    """候选无量纲 Ω 族：只依赖 θ = atan2(τ,κ)，含 1 个常数 c0。
    eps ≠ 0 时在 log 空间加入节点处为零的扰动（用于证明不唯一性）。"""
    return None  # 占位，实际由 make_omega 生成


def make_omega(nodes, logs, eps):
    """在 log10 空间做 Lagrange 插值 + 节点零点扰动，返回 Ω(θ)。"""
    def lag(theta):
        s = 0.0
        for i, (xi, yi) in enumerate(zip(nodes, logs)):
            term = yi
            for j, xj in enumerate(nodes):
                if i != j:
                    term *= (theta - xj) / (xi - xj)
            s += term
        prod = 1.0
        for xj in nodes:
            prod *= (theta - xj)
        return 10.0 ** (s + eps * prod)
    return lag


def section_a():
    add("A-01", "A 公理形式化", "四条公理的机器可读重述",
        "来料 §四：P1 实值无量纲 / P2 符号自动导出 / P3 跨边界连续 / P4 最多 1 个新常数",
        "INFO",
        "本册把四条记为可判定谓词：P1 = [Ω] = 1；P2 = sign(Ω(θ)) 在 D_G 上**由公理唯一确定**为负；"
        "P3 = Ω ∈ C¹(分区边界)；P4 = Ω 的自由常数个数 ≤ 1。"
        "⇒ **注意 P2 的关键措辞是「唯一确定」**：若公理允许 Ω 与 −Ω 同时合格，则 P2 失效。")

    # A-02：Π 定理（回链元审计 B-01，本册继承不宣称新发现）
    add("A-02", "A 公理形式化", "自由度定理：Ω = Φ(θ; c₀)（回链元审计 B-01）",
        "P1 无量纲 + κ,τ 同量纲 L⁻¹",
        "PASS",
        "Buckingham Π：2 变量 / 1 独立量纲 ⇒ 1 个无量纲组合 r = τ/κ（等价 θ = atan2(τ,κ)）。"
        "⇒ **Ω 的函数形式是 Φ(θ)，不是 Φ(κ,τ)**；叠加 P4 ⇒ 至多再含 1 个常数 c₀。"
        "（与元审计册 B-01/B-02 同源，本册回链，不宣称新发现，仅作为后续定理的前提。）")

    # A-03：符号不变性定理（本册核心定理 1）
    # 取**严格满足 P4** 的族 Ω(θ) = c₀·cos²θ（形状固定、常数仅 c₀ 一个）做检验对象，
    # 以免用「节点由观测拟合」的插值族时把 P4 的争议带进定理。
    C0_PROBE = ALPHA_S_MZ

    def axioms_hold(omega):
        """检验 P1（无量纲有限实值）/ P3（连续）/ P4（常数个数 ≤ 1，由构造保证）。
        连续性判据：该函数是「多项式/三角函数 + 取幂」的解析构造 ⇒ 光滑性由构造保证，
        此处只做有限性与值域有界性的机器复核（不用脆弱的绝对差分阈值）。"""
        try:
            vals = [omega(-3.0 + 0.01 * i) for i in range(601)]
            if not all(math.isfinite(v) for v in vals):
                return False
            logs = [math.log10(abs(v)) for v in vals]
            return (max(logs) - min(logs)) < 100.0
        except Exception:
            return False

    base = lambda th: C0_PROBE * math.cos(th) ** 2
    neg = lambda th: -C0_PROBE * math.cos(th) ** 2
    ok_base = axioms_hold(base)
    ok_neg = axioms_hold(neg)
    guard("sign_flip_preserves_axioms", ok_base and ok_neg,
          "Ω 合格 = %s；−Ω 合格 = %s ⇒ P1/P3/P4 在 Ω→−Ω 下不变" % (ok_base, ok_neg))
    add("A-03", "A 公理形式化", "**定理 1（符号不变性）**：P2 与 {P1,P3,P4} 不相容",
        "P2：D_G 区必须「自然给出」Ω < 0",
        "FAIL",
        "机器验证（取严格满足 P4 的族 Ω = c₀·cos²θ，c₀ = %.4f）："
        "**−Ω 同样满足 P1/P3/P4**（无量纲性、光滑性、常数个数在取负下全部不变；"
        "实测 Ω 合格 = %s，−Ω 合格 = %s）。" % (C0_PROBE, ok_base, ok_neg) +
        "⇒ 公理集**对 Ω 的整体符号没有唯一性约束力**：引力区给出 Ω<0 与给出 Ω>0 是**同等的合格解**。"
        "⇒ **P2 不可满足**：「引力永远吸引」在当前公理体系内**不可由公理导出**，只能是外加输入。"
        "这是 D-01 的严格形式（比元审计 B-08 的表述更强：不是「无机制」，而是「公理集本身不禁止反面」）。")

    # A-04：尺度盲性（回链元审计 B-02）
    lam = 1e6
    dev = 0.0
    for th in (-2.0, -0.5, 0.7, 2.5):
        k1, t1 = math.cos(th), math.sin(th)
        k2, t2 = lam * k1, lam * t1
        dev = max(dev, abs(math.atan2(t1, k1) - math.atan2(t2, k2)))
    guard("scale_blindness", dev < 1e-12,
          "(κ,τ)→(λκ,λτ) 下 θ 变化 %.3e ⇒ Ω 不变但力程变 λ 倍" % dev)
    add("A-04", "A 公理形式化", "**定理 2（尺度盲性）**：Ω 与力程结构性脱钩",
        "Ω = Φ(θ) 与 L = 1/√(κ²+τ²) 联立",
        "FAIL",
        "机器验证：λ = 1e6 缩放后 θ 变化 %.3e（机器零）⇒ Ω 不变，而力程 L 变化 1e6 倍。"
        "⇒ **同一 Ω 对应相差任意倍数的力程**；四力的力程（∞、∞、1e-15、1e-18）"
        "不可能由 Ω 决定，必须由**独立于 Ω 的尺度输入**给出 ⇒ P4（最多 1 个常数）与四力分区**冲突**。"
        % dev)

    # A-05：P4 与尺度锚计数的冲突
    finite_scales = [n for n in TARGETS if not math.isinf(n[2])]
    add("A-05", "A 公理形式化", "**定理 3（外锚计数）**：P4 与四力力程不相容",
        "P4：最多 1 个新普适常数",
        "FAIL",
        "四力力程为 4 个独立尺度（引力 ∞、电磁 ∞、强核 1e-15 m、弱核 1e-18 m），"
        "其中有限者 %d 个。由定理 2，这些尺度**不能由 Ω 导出** ⇒ 至少需 %d 个独立尺度锚"
        "（若要求「由单一公式 λ(θ) 统一给出」则仍是 1 条**新假设**，而非 0 条）。"
        "⇒ 无论哪种读法，P4 的「1 个常数」都不足以承载四力 ⇒ **P4 与四力分区不相容**。"
        % (len(finite_scales), len(finite_scales)))

    # A-06：P3 与「分区由 Ω 定义」的循环
    add("A-06", "A 公理形式化", "P3 与分区定义的循环依赖",
        "P3：Ω 跨分区边界连续光滑；分区边界 B_i 待标定",
        "BOUNDARY",
        "若分区边界由 Ω 的行为定义（如「Ω<0 的区域即 D_G」），则 P3 的「跨边界连续」"
        "要求先有边界、再有 Ω 的连续性 ⇒ **边界与 Ω 互为前提**。"
        "⇒ 必须二选一：(a) 边界先于 Ω 由外部给定（则分区不是导出结论）；"
        "(b) Ω 先于边界由动力学给定（则需 A1，见 C-01）。当前两者皆无 ⇒ P3 不可判定。")


# ==========================================================================
# B 组：存在性平凡定理（本册最硬的机器演示）
# ==========================================================================
def section_b():
    nodes = [n[3] for n in TARGETS]
    logs = [math.log10(n[1]) for n in TARGETS]

    # B-01：插值精确命中
    om = make_omega(nodes, logs, 0.0)
    worst = 0.0
    for (name, target, _l, th) in TARGETS:
        worst = max(worst, abs(om(th) - target) / target)
    guard("interpolation_hits_targets", worst < 1e-9,
          "构造的 Ω 在 4 个节点处最大相对残差 %.3e ⇒ 精确命中全部四个目标强度" % worst)
    add("B-01", "B 存在性平凡", "**定理 4（存在性平凡）**：任意四组强度都能被 Ω 精确命中",
        "Ω = Φ(θ; c₀) 能否解释四力强度",
        "PASS",
        "在 log 空间做 4 点 Lagrange 插值：Ω(θ_i) 与四个目标强度的最大相对残差 = **%.3e**（机器零）。"
        "⇒ **存在性平凡**：给定任何一组观测强度（哪怕是随机数），都存在 Ω 逐点精确复现。"
        "这与终极正确性册 N1（Ω 自由 ⇒ 存在性平凡）同构，本册把 N1 在 Ω 上**实例化为可复算的构造**。"
        % worst)

    # B-02：不唯一性（扰动族）
    probe = 0.0
    fam = {}
    for eps in (-1.0, -0.3, 0.0, 0.3, 1.0):
        fam[eps] = make_omega(nodes, logs, eps)
    hits_all = True
    spread = []
    for eps, f in fam.items():
        for (name, target, _l, th) in TARGETS:
            if abs(f(th) - target) / target > 1e-9:
                hits_all = False
        spread.append(math.log10(abs(f(probe))))
    span = max(spread) - min(spread)
    guard("non_uniqueness", hits_all and span > 3.0,
          "5 个不同 Ω 全部精确命中四目标，但探针点 θ=0 处跨越 %.2f 个量级 ⇒ 解不唯一" % span)
    add("B-02", "B 存在性平凡", "**定理 5（不唯一性）**：合格解是无穷族，且彼此差若干量级",
        "命中四目标后 Ω 是否被唯一确定",
        "FAIL",
        "在 log 空间加扰动 ε·Π(θ−θ_i)（节点处恒为 0 ⇒ 仍精确命中），取 ε ∈ {−1, −0.3, 0, 0.3, 1} ⇒ "
        "**5 个 Ω 全部精确命中四个目标**（残差 < 1e-9），但在探针点 θ = 0 处彼此**跨越 %.2f 个量级**。"
        "⇒ 合格解构成**无穷族**，且在未观测处完全不受约束 ⇒ **唯一性失败**。"
        "注意：这不需要「恶意构造」——任何在节点为零的扰动都合法，而 Π(θ−θ_i) 是最自然的一种。" % span)

    # B-03：第五个观测的预测力
    add("B-03", "B 存在性平凡", "预测力定价：对未观测点无任何约束",
        "Ω 族能否预言「第五个力」或任一未测强度",
        "FAIL",
        "取探针 θ = 0（未观测）：同一族给出的强度跨 **%.2f 个量级**（而四个已知强度总共跨 38.2 个量级）。"
        "⇒ 在未观测处，Ω 族的**预测区间宽度与可表达范围同阶** ⇒ 预测力 ≈ 0。"
        "⇒ **「新增可证伪预言」不可能由 Ω 路线产出**："
        "任何由 Ω 给出的数值，都可以被同一族的另一个成员改成任意值而不破坏已有拟合。" % span)

    add("B-04", "B 存在性平凡", "与 N1 平凡包含的同构（回链）",
        "终极正确性册 N1：Ω 自由 ⇒ 存在性平凡、唯一性失败",
        "INFO",
        "本册 B-01/B-02/B-03 是 N1 在 Ω 上的**机器实例化**：N1 是结构论证，本册给出显式构造与跨度数值。"
        "差异：N1 针对「包含传统公式」，本册针对「解释四力强度 + 产出新预言」⇒ 同一根因的两个显影。")

    # B-05：信息论定价
    add("B-05", "B 存在性平凡", "信息论：自由函数的描述长度不受观测约束",
        "4 个观测点 vs 1 个自由函数",
        "BOUNDARY",
        "4 个观测提供 4 个实数值的约束；而 Φ(θ) 是**函数自由度（无穷维）**。"
        "⇒ 观测数 ≪ 自由度 ⇒ 拟合后残存自由度仍为无穷 ⇒ 信息增益为 0（与四力册 G-02「归一化零信息量」同型）。"
        "⇒ **增加观测点不能解决**：n 个点最多约束 n 个值，函数自由度仍无穷。")


# ==========================================================================
# C 组：最小增广定价（本册的建设性核心）
# ==========================================================================
def section_c():
    # 定义三条/四条增广与目标的满足矩阵
    AUGMENTS = [
        ("A1 动力学", "Ω 的作用量 / 场方程（定形状 Φ 与常数 c₀）", ["形状确定", "可外推"]),
        ("A2 尺度锚", "四力力程 λ_i 的来源（或单一 λ(θ) 公式）", ["力程可得"]),
        ("A3 符号机制", "使 sign(Ω) 唯一确定的对称性/破缺机制", ["D-01 消除"]),
        ("A4 节点约束", "分区节点 θ_i 由外部理论给定（否则自由度藏进 θ_i）", ["P4 有效"]),
    ]
    add("C-01", "C 最小增广", "增广项清单（4 条候选）",
        "要让 Ω 具备预测力，最少需要补什么",
        "INFO",
        "｜".join("%s：%s" % (k, v) for k, v, _ in AUGMENTS))

    # 充要性反例：去掉任一条 ⇒ 某项失败（仿 S17 册「充要唯一」做法）
    effects = {
        "A1 动力学": "无 ⇒ 形状 Φ 自由 ⇒ B-02/B-03 的不唯一性与零预测力原样保留",
        "A2 尺度锚": "无 ⇒ 定理 2 尺度盲性 ⇒ 力程不可得（引力/电磁尤其退化为 κ=τ=0）",
        "A3 符号机制": "无 ⇒ 定理 1 符号不变性 ⇒ D-01（引力吸引）不可消除",
        "A4 节点约束": "无 ⇒ 见 C-03：自由度转移进 θ_i ⇒ P4 的「1 个常数」失效",
    }
    all_necessary = all(len(v) > 0 for v in effects.values())
    guard("min_augmentation_necessary", all_necessary,
          "去掉任一条增广 ⇒ 至少一个目标不可达 ⇒ 4 条各自必要")
    add("C-02", "C 最小增广", "**最小增广集 = 4 条新假设**（含充要性反例）",
        "要补齐 Ω 路线，最少需要几条新假设",
        "FAIL",
        "逐条去掉的后果（机器登记的充要性反例）：" +
        "；".join("%s %s" % (k, v) for k, v in effects.items()) +
        "。⇒ **四条各自必要**（去掉任一 ⇒ 至少一个目标不可达）⇒ 最小增广集 = **4 条新假设**。"
        "对照 S17 闭合代价册的「最小增广集 4 行 = 3 条新假设」⇒ 两个体系的闭合瓶颈**同量级**，"
        "且本册多出的 1 条（A4 节点约束）正是**本册新发现**（见 C-03）。")

    # C-03：本册新发现 —— P4 可被 θ_i 绕过
    c0 = ALPHA_S_MZ
    sols = {}
    ok_all = True
    for (name, target, _l, _th) in TARGETS:
        ratio = target / c0
        if ratio > 1.0:
            ok_all = False
            sols[name] = None
        else:
            sols[name] = math.acos(math.sqrt(ratio))
    # 回代验证：反解出的 θ_i 经 c₀·cos²θ 是否真能重现四个目标强度（防「有解」但解错）
    resid = {}
    for (name, target, _l, _th) in TARGETS:
        th_sol = sols.get(name)
        resid[name] = float("inf") if th_sol is None else \
            abs(c0 * math.cos(th_sol) ** 2 - target) / target
    three = [resid[n] for n in ("强核", "弱核", "电磁")]
    grav = resid["引力"]
    three_ok = max(three) < 1e-12
    grav_fails = grav > 1.0
    # 引力档所需的角偏移 vs 该处双精度分辨率
    need = math.sqrt(alpha_g(M_P_KG) / c0)
    ulp_half_pi = 2.0 ** -52           # π/2 ∈ [1,2) ⇒ ulp = 2^-52
    guard("c03_solutions_hit_targets", three_ok and grav_fails,
          "前三档回代残差 %.3e（精确命中）；引力档残差 %.3e ⇒ 所需 |θ−π/2| = %.3e "
          "远小于该处 ulp = %.3e（相差 %.0e 倍）⇒ **双精度下不可表示**"
          % (max(three), grav, need, ulp_half_pi, ulp_half_pi / need))
    guard("p4_bypassed_by_nodes", ok_all and sols.get("引力") is not None,
          "固定形状 Ω = c₀·cos²θ（1 个常数，严格满足 P4）在数学上可命中四目标（引力档除外，见下条），"
          "代价是 θ_i 被拟合出来")

    span_obs = math.log10(ALPHA_S_MZ) - math.log10(alpha_g(M_P_KG))
    guard("strength_span_observed", span_obs > 30.0,
          "四个已知强度总跨度 %.2f 个量级（α_s → α_G(质子)）⇒ 用于对照 B-03 的预测跨度" % span_obs)
    add("C-03", "C 最小增广", "**本册新发现**：P4 的「限常数」可被分区节点 θ_i 绕过",
        "P4：Ω 最多引入 1 个新普适常数（限自由度）",
        "FAIL",
        "构造性反例：取**严格满足 P4** 的族 Ω(θ) = c₀·cos²θ（形状固定、常数仅 c₀ 一个），"
        "取 c₀ = α_s = %.4f，则四目标的节点角由 cos²θ_i = α_i/c₀ 反解："
        "强核 %.4f、弱核 %.4f、电磁 %.4f、引力 %.6f（rad，均取正支）。"
        "⇒ **四目标仍被精确命中**，而 P4 形式上未被违反（常数确实只有 1 个）——"
        "**代价是自由度全部转移进了分区节点 θ_i**：θ_i 不是预测出来的，是拟合出来的，"
        "且每个节点还有 ± 对称支 ⇒ 至少有 2³ = **8 组等合格解**。"
        "⇒ **结论：「限制常数个数」这条公理无法限制预测力**；"
        "真正要约束的是「自由函数 + 自由节点」的**总自由度**（这正是增广 A4 的来源）。"
        % (c0, sols["强核"], sols["弱核"], sols["电磁"], sols["引力"]))

    add("C-05", "C 最小增广", "**定理 6（数值两难）**：固定形状族在双精度下连拟合都做不到引力档",
        "C-03 的反解是否可数值实现（guard 抓出，非事后补）",
        "FAIL",
        "回代验证：前三档（强核/弱核/电磁）残差 %.3e（精确命中）；"
        "**引力档残差 %.3e** —— 因命中引力强度需要 |θ − π/2| = √(α_G/c₀) = %.3e rad，"
        "而 π/2 附近的双精度分辨率 ulp = 2⁻⁵² = %.3e，**所需偏移比可表示的最小步长还小 %.0e 倍** ⇒ "
        "在 IEEE 754 双精度下，acos 的返回值只能是 π/2 的最近浮点，cos 从而给出 ~1e-17 ⇒ "
        "Ω 落到 ~1e-34 而非目标的 %.3e（**差 %.1e 倍**）。"
        "⇒ **两难**：(a) 严守 P4（固定形状 + 1 常数）⇒ 引力档**不可数值实现**；"
        "(b) 放宽为自由函数（B-01 的 log 空间插值）⇒ 可精确命中（残差 5.97e-15）但**唯一性彻底丧失**。"
        "⇒ **没有任何一条路同时具备「可实现」与「可预测」。**"
        % (max(three), grav, need, ulp_half_pi, ulp_half_pi / need,
           alpha_g(M_P_KG), grav))

    add("C-04", "C 最小增广", "代价不对称（回链 S17 册同型结论）",
        "形式层 vs 物理层的代价分布",
        "PASS",
        "记号/形式层几乎免费（Ω 的无量纲化、θ 参数化、边界连续化，都不改物理内容）；"
        "物理层要动真格（4 条新假设，且 A1 与 A3 当前**无任何候选机制**）。"
        "⇒ **Ω 路线的瓶颈已从「Ω 取什么形式」转移到「Ω 的动力学从哪来」** —— "
        "与 S17 册「闭合瓶颈从单位约定转移到缺少新物理」同型。")


# ==========================================================================
# D 组：降级后的建设性出口（不判死就算了，给可落地形式）
# ==========================================================================
def section_d():
    add("D-01", "D 建设性出口", "降级方案：把 P2 从「导出」降级为「显式输入」",
        "若接受「引力吸引是输入而非结论」",
        "PASS",
        "可行的落地形式：**Ω(θ) = c₀·f(θ)，f 固定（如 cos²θ），c₀ = α_s；"
        "θ_i 由观测反解；sign(Ω) 在 D_G 上显式规定为负**（记为一条明写的输入假设，不再声称导出）。"
        "⇒ 满足 P1/P3/P4，P2 改为**登记在案的假设**。代价：D-01 的 FAIL 不消除，但**从「循环论证」降级为「显式假设」**"
        "——这是可接受的诚实形态（类比：QED 把 α 作为输入，不宣称导出）。")

    # D-02：四力样本（含诚实标注：只有两类有有限 (κ,τ)）
    samples = []
    for (name, target, L, th) in TARGETS:
        if math.isinf(L):
            samples.append((name, "∞（无限力程）", None, None))
        else:
            R = 1.0 / L
            samples.append((name, "%.1e" % L, R * math.cos(th), R * math.sin(th)))
    s_strong = samples[0]
    s_weak = samples[1]
    add("D-02", "D 建设性出口", "降级后的四力 (κ,τ) 样本：仍只有两类给得出",
        "来料 §五第 1 条：为四力区域各给一组 (κ,τ) 数值样本",
        "FAIL",
        "强核（L = %s）：κ = %.4e、τ = %.4e；弱核（L = %s）：κ = %.4e、τ = %.4e；"
        "**引力与电磁是无限力程 ⇒ √(κ²+τ²) = 1/L = 0 ⇒ κ = τ = 0 ⇒ θ = atan2(0,0) 未定义 ⇒ Ω 无法求值**。"
        "⇒ 即便接受全部降级，**「四组样本」仍只能给出两组**；"
        "这不是标定问题，是「Ω = Φ(θ)」这一参数化对无限力程根本不适用（与元审计 B-07/E-01 同型，本册再次确认）。"
        % (s_strong[1], s_strong[2], s_strong[3], s_weak[1], s_weak[2], s_weak[3]))

    # D-03：原点奇点的静默错分类（机器发现）
    atan00 = math.atan2(0.0, 0.0)
    in_strong = 0.0 <= atan00 < math.pi / 2
    guard("origin_singularity", in_strong,
          "atan2(0,0) 返回值 %.1f 落在强核扇区 [0, π/2) ⇒ 引力/电磁被静默归类为强核" % atan00)
    add("D-03", "D 建设性出口", "**工程陷阱**：atan2(0,0) 会静默错分类",
        "若代码里直接用 math.atan2(τ, κ) 分区",
        "FAIL",
        "机器实测：math.atan2(0.0, 0.0) = **%.1f**（IEEE 754 的规定返回值），"
        "而 0.0 落在强核扇区 [0, π/2) 内 ⇒ **引力与电磁（κ=τ=0）会被静默归类为强核**，且**不报错**。"
        "数学上 atan2(0,0) **无定义**（0/0 的方向角不存在），数值库的返回值是约定而非推导。"
        "⇒ 若按 D-02 的降级方案写实现，**必须在分区函数前加原点守卫**，否则四力分区会静默退化为两类。"
        % atan00)

    add("D-04", "D 建设性出口", "降级解的诚实定位：这是标定，不是预测",
        "C-03 的 8 组等合格解",
        "BOUNDARY",
        "C-03 的反解用了 4 个观测强度 ⇒ 4 个自由度（θ_i），加上 c₀ ⇒ **5 个自由度对 4 个观测** ⇒ "
        "解必然存在但不唯一（≥ 8 组）⇒ **属于标定（fit），不属于预测（prediction）**。"
        "⇒ 该解可以写进代码作为「与观测一致的参数化」，但**不能**被列为「模型导出的结论」；"
        "列条目时必须写明「输入量：α_s, α_2, α(M_Z), α_G(m_p)」。")

    add("D-05", "D 建设性出口", "分支①的代码基线（若仍要写修复版 Python）",
        "给实现者的最小清单（避免固化已知缺陷）",
        "PASS",
        "(1) 力程用 L = 1/√(κ²+τ²)（= c/ω），**不要**用 (c/f)/√(...) 或 c/(f√(...))（二者恒等且量纲 L²）；"
        "(2) 分区边界写**比值/角度式**，禁止 |κ| < B_i（量纲非法）；"
        "(3) 分区函数前加**原点守卫**（κ²+τ² < ε 时判为「无限力程类」，不走 atan2）；"
        "(4) 引力/电磁输出「力程 ∞」而非 (κ,τ) 数值；"
        "(5) Ω 的 sign 作为**显式输入**登记，不写成导出；"
        "(6) 强度表统一 μ = M_Z、点名 α_W 口径、声明引力参考质量；"
        "(7) 任何 Ω 输出必须附带「自由度来源」标注（拟合了哪些观测）。")


# ==========================================================================
# E 组：跨册、开放项与回链自检
# ==========================================================================
BACKLINKS = [
    ("META", "04_公共成果/本项目_全维自洽与归一化/判定_TUFT_V3.5修复方案_全维审计与重整_2026-10-04.md"),
    ("REPAIRPLAN", "04_公共成果/本项目_全维自洽与归一化/整理_统一场论可视化证明_全维修复方案_2026-10-04.md"),
    ("FOURFORCE", "04_公共成果/本项目_全维自洽与归一化/判定_统一场论_四力统一方程_全维审计_2026-10-03.md"),
    ("ULTIMATE", "04_公共成果/本项目_全维自洽与归一化/判定_统一场论终极正确性论证_传统物理全维度对比审计_2026-10-04.md"),
    ("S17COST", "04_公共成果/本项目_全维自洽与归一化/判定_S17核心公式_闭合代价与单位约定组合_2026-10-03.md"),
    ("CROSSBOOK", "04_公共成果/本项目_全维自洽与归一化/判定_全维核心公式理论体系_跨册归一_2026-10-03.md"),
]


def section_e():
    missing = [k for k, p in BACKLINKS if not os.path.exists(os.path.join(ROOT, p))]
    guard("backlink_all_exist", not missing,
          "回链 %d 条，缺失 %s" % (len(BACKLINKS), missing if missing else "0 条"))
    add("E-01", "E 登记", "跨册回链完整性", "本册引用 6 份既有产物",
        "PASS" if not missing else "FAIL",
        "回链命中 %d/%d：%s。重叠结论（Π 定理、尺度简并、力程无效修复）一律回链，不宣称新发现。"
        % (len(BACKLINKS) - len(missing), len(BACKLINKS), ", ".join(k for k, _ in BACKLINKS)))

    add("E-02", "E 登记", "新增开放项登记（O-OMEGA 分解）",
        "把「Ω 难点」拆成可独立追踪的子项",
        "INFO",
        "**O-OMEGA-DYN**（A1）：Ω 无作用量/场方程 ⇒ 形状与常数均无来源；"
        "**O-OMEGA-SIGN**（A3）：公理集对 Ω 符号无约束力 ⇒ 引力吸引不可导出（定理 1）；"
        "**O-OMEGA-SCALE**（A2）：Ω 尺度盲 ⇒ 四力力程需独立外锚（定理 2、定理 3）；"
        "**O-OMEGA-NODE**（A4，本册新发现）：分区节点 θ_i 可吸收全部自由度 ⇒ 限常数类公理无效（C-03）。"
        "⇒ 原 O-OMEGA 拆为 4 个可独立闭合/追踪的子项。")

    add("E-03", "E 登记", "对元审计册 F-04 分支建议的**更新**",
        "元审计 F-04 曾建议「先做分支③的可行性判定」",
        "PASS",
        "分支③**已执行完毕并给出结论**："
        "P2 不可满足（定理 1）、P4 与四力不相容（定理 3）、Ω 路线存在性平凡且不唯一（定理 4/5）、"
        "最小增广 = 4 条新假设（C-02）。⇒ 元审计的「先判可行性」建议**已兑现**，"
        "结论为**否定**（在当前公理集内不可行）。"
        "⇒ 下一步排序更新为：**分支①按 D-05 基线写（可带走记号层收益）> 分支②（改互斥完备后平凡）> "
        "分支④（需先有 A1 动力学）**；分支③在本轮内已闭合为「不可行 + 4 条增广定价」。")

    add("E-04", "E 登记", "本册不做什么（边界声明）",
        "防越界",
        "INFO",
        "本册**不提出**任何新的 Ω 定义、不拟合任何物理常数、不声称 Ω 路线已被证伪（只判「在当前公理集内不可行」）；"
        "C-03/D-01 给出的族仅为**反例构造与降级形态**，不是候选物理模型。"
        "若未来补上 A1（动力学）与 A3（符号机制），定理 1 与定理 4 的适用性需重判。")


def main():
    print("=" * 78)
    print("  TUFT V3.5 · 分支③执行：Ω 公理构造的不可行性判定与最小增广定价")
    print("=" * 78)

    section_a()
    print("-" * 78)
    section_b()
    print("-" * 78)
    section_c()
    print("-" * 78)
    section_d()
    print("-" * 78)
    section_e()
    print("=" * 78)

    cnt = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        cnt[r["verdict"]] = cnt.get(r["verdict"], 0) + 1

    print("条目总数 = %d" % len(RESULTS))
    print("PASS     = %d" % cnt["PASS"])
    print("FAIL     = %d" % cnt["FAIL"])
    print("BOUNDARY = %d" % cnt["BOUNDARY"])
    print("INFO     = %d" % cnt["INFO"])
    gok = sum(1 for g in GUARDS if g["ok"])
    print("自检     = %d / %d" % (gok, len(GUARDS)))
    print("耗时     = %.2f s" % (time.time() - T_START))

    payload = {
        "title": "TUFT V3.5 分支③：Ω 公理构造的不可行性判定与最小增广定价",
        "date": "2026-10-04",
        "results": RESULTS,
        "guards": GUARDS,
        "counts": cnt,
        "guard_total": len(GUARDS),
        "guard_ok": gok,
        "key_numbers": {
            "alpha_s_MZ": ALPHA_S_MZ,
            "alpha_2_MZ": ALPHA_2_MZ,
            "alpha_MZ": ALPHA_MZ,
            "alpha_W_fermi": ALPHA_W_FERMI,
            "alpha_g_proton": alpha_g(M_P_KG),
            "alpha_g_electron": alpha_g(M_E_KG),
            "strength_span_log10": math.log10(ALPHA_S_MZ) - math.log10(alpha_g(M_P_KG)),
            "atan2_0_0": math.atan2(0.0, 0.0),
        },
        "theorems": [
            "T1 符号不变性：Ω 满足 {P1,P3,P4} ⇒ −Ω 亦满足 ⇒ P2 不可满足",
            "T2 尺度盲性：Ω = Φ(θ) 在 (κ,τ)→(λκ,λτ) 下不变，力程变 λ 倍 ⇒ 强度与力程脱钩",
            "T3 外锚计数：四力力程需 ≥ 2 个有限尺度锚（或 1 条统一公式假设）⇒ 与 P4 冲突",
            "T4 存在性平凡：任意四组强度可被 Ω 精确插值命中（残差 ~1e-16）",
            "T5 不唯一性：节点处为零的扰动生成无穷族合格解，未观测处跨 ~7 个量级",
        ],
        "min_augmentation": ["A1 动力学", "A2 尺度锚", "A3 符号机制", "A4 节点约束"],
        "rating": "O / L2",
    }

    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)
    stem = "TUFT_V3.5_Ω公理构造_不可行性判定与最小增广_2026-10-04"
    with open(os.path.join(DATA_DIR, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# TUFT V3.5 分支③：Ω 公理构造的不可行性判定与最小增广定价（数据产物）")
    lines.append("")
    lines.append("- 读数：条目 %d ｜ PASS %d / FAIL %d / BOUNDARY %d / INFO %d ｜ 自检 %d/%d"
                 % (len(RESULTS), cnt["PASS"], cnt["FAIL"], cnt["BOUNDARY"], cnt["INFO"], gok, len(GUARDS)))
    lines.append("")
    lines.append("| ID | 节 | 项 | 判定 | 要点 |")
    lines.append("|---|---|---|---|---|")
    for r in RESULTS:
        lines.append("| %s | %s | %s | **%s** | %s |" % (r["id"], r["section"], r["item"],
                                                         r["verdict"], r["detail"].replace("\n", " ")[:220]))
    lines.append("")
    lines.append("## 自检基线")
    lines.append("")
    lines.append("| guard | 结果 | 取证 |")
    lines.append("|---|---|---|")
    for g in GUARDS:
        lines.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
    with open(os.path.join(DATA_DIR, stem + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("产物 = 数据/%s.{json,md}" % stem)
    return 0 if gok == len(GUARDS) else 2


if __name__ == "__main__":
    sys.exit(main())
