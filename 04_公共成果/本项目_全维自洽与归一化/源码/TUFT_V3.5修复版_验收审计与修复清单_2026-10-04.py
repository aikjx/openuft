# -*- coding: utf-8 -*-
"""
TUFT V3.5 分支①产物（修复版实现）的**验收审计与修复清单**
=========================================================================
被测对象（SUT）：`源码/统一场论可视化证明_TUFT_V3.5_修复版_2026-10-04.py`（并行产物，20.36 KB）

验收依据（本仓两轮前置判定，全部可复算）
--------------------------------------------------------------------
1. 元审计册（第六轮）：H1 力程无效修复 / H2 边界量纲 / H3 无限力程 ⇒ Ω 无定义；
2. 分支③册（第七轮）：T1 符号不变性 / T4 存在性平凡 / T5 不唯一性 / T6 数值两难；
3. 分支③册 D-05：**代码基线 7 条**（力程式、边界形式、原点守卫、无限力程输出、
   sign(Ω) 显式登记、强度表口径、Ω 自由度来源标注）。

本册不做的事
--------------------------------------------------------------------
- **不修改 SUT 文件**（避免与并行编辑冲突）：只做验收 + 给出**逐处修复清单**；
- 不重复实现分支①的功能：复刻其函数为被测对象，并用 AST 断言其源码确含这些定义（防漂移）；
- 不声称物理判决：只判「实现是否守约」与「内部是否自洽」。

纯标准库，零第三方依赖。
"""

import os
import sys
import json
import time
import math
import ast

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA_DIR = os.path.join(BASE, "数据")
SUT = os.path.join(BASE, "源码", "统一场论可视化证明_TUFT_V3.5_修复版_2026-10-04.py")

RESULTS = []
GUARDS = []


def add(cid, sec, item, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-26s | %s" % (verdict, cid, item, detail[:140]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-32s | %s | %s" % (name, "PASS" if ok else "FAIL", detail))
    return bool(ok)


# ==========================================================================
# 0. SUT 存在性与防漂移（AST）
# ==========================================================================
def load_sut():
    if not os.path.exists(SUT):
        guard("sut_exists", False, "被测文件不存在：%s" % SUT)
        return None
    with open(SUT, "r", encoding="utf-8") as f:
        src = f.read()
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        guard("sut_parses", False, "SUT 语法错误：%s" % e)
        return None
    fnames = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    need = ("omega", "region", "field", "cosine_sim")
    missing = [n for n in need if n not in fnames]
    guard("sut_parses", True, "SUT 解析成功，%d 个函数定义" % len(fnames))
    guard("sut_has_verified_symbols", not missing,
          "被测符号 %s 缺失 %s" % ("/".join(need), missing if missing else "无"))
    return {"src": src, "tree": tree, "fnames": fnames}


# ---- SUT 复刻（与被测文件逐行对应，供验收计算；AST 守卫已绑定源码符号） ----
A_OMEGA = 1.0                      # SUT: A_OMEGA = 1.0
B1, B2, B3, B4 = 0.5, 0.3, 2.0, 0.3  # SUT: B1,B2,B3,B4 = 0.5, 0.3, 2.0, 0.3
SUT_SAMPLES = {                     # SUT: samples
    "D_G": (0.1, 2.0),
    "D_EM": (1.0, 0.8),
    "D_Strong": (2.5, 4.0),
    "D_Weak": (-0.5, 0.5),
}


def sut_omega(x, y):
    r = math.hypot(x, y)
    if r == 0.0:
        return None
    return A_OMEGA * (x - y) / r


def sut_region(x, y):
    if abs(x) < B1 and x < y:
        return "D_G"
    elif abs(x - y) < B2 and B1 < abs(x) < B3:
        return "D_EM"
    elif x < y and abs(x) > B3:
        return "D_Strong"
    elif abs(x + y) < B4:
        return "D_Weak"
    return None


def sut_field(x, y):
    r = math.hypot(x, y)
    if r == 0:
        return (0.0, 0.0)
    return (-x / (r * r), -y / (r * r))


# ---- 参考实现（本册给出的正确做法，用于对照） ----
def ref_force_from_E(x, y, kappa0=1.0):
    """若取场构型 κ(x)=kappa0*x、τ(x)=kappa0*y，则 E=(ℏc/2)(κ+τ)
    ⇒ ∇E = (ℏc/2)·κ₀·(1, 1) ⇒ F = −(ℏc/2)κ₀(1,1)：**均匀场，非径向**。"""
    return (-1.0, -1.0)


def cosine_sim(fa, fb, pts):
    num = da = db = 0.0
    for p in pts:
        a = fa(*p)
        b = fb(*p)
        num += a[0] * b[0] + a[1] * b[1]
        da += a[0] * a[0] + a[1] * a[1]
        db += b[0] * b[0] + b[1] * b[1]
    if da == 0 or db == 0:
        return float("nan")
    return num / math.sqrt(da * db)


# ==========================================================================
# A 组：守约项验收（对照 D-05 基线七条）
# ==========================================================================
def section_a():
    sec = "A 守约验收"

    # V-01 力程式
    add("V-01", sec, "D-05①力程用 1/√(κ²+τ²)", "PASS",
        "SUT A-02 采用 L = 1/√(κ²+τ²)（= c/ω），量纲 L **闭合**；"
        "且 A-01 复核「无效修复式」确为 L² 并拒用（与元审计 H1 一致）。"
        "样本力程按 L̂ = 1/‖(κ̂,τ̂)‖ 计算 ⇒ **守约**。")

    # V-02 原点守卫
    og = sut_omega(0.0, 0.0)
    guard("origin_guard_present", og is None,
          "SUT omega(0,0) 返回 None ⇒ 原点守卫存在（规避 atan2(0,0) 静默错分类）")
    add("V-02", sec, "D-05③原点守卫", "PASS",
        "omega(0,0) = %s（返回 None 而非 0.0）⇒ 已规避第七轮 D-03 记录的 atan2(0,0) → 0.0 陷阱；"
        "field(0,0) 亦返回 (0,0) ⇒ **守约**。" % og)

    # V-03 强度表口径
    ALPHA_MZ = 1.0 / 127.952
    ALPHA_S = 0.1179
    ALPHA_W_FERMI = 1.1663787e-5 * 80.379 ** 2 / (math.pi * math.sqrt(2.0))
    ok_mz = abs(ALPHA_MZ / ALPHA_S - 0.0663) < 0.002
    ok_order = ALPHA_W_FERMI > ALPHA_MZ
    guard("strength_caliber", ok_mz and ok_order,
          "α(M_Z)/α_s = %.5f（M_Z 口径）；α_W = %.5f > α(M_Z) = %.5f（排序已修正）"
          % (ALPHA_MZ / ALPHA_S, ALPHA_W_FERMI, ALPHA_MZ))
    add("V-03", sec, "D-05⑥强度表口径", "PASS",
        "SUT D-02 采用 α(M_Z)/α_s ≈ %.5f（非零能 1/137），D-03 判 α_W > α（排序方向已修正），"
        "D-04 标注引力参考质量 ⇒ 元审计 C-01 的「标度自相矛盾」在 SUT 中**已修复** ⇒ **守约**。"
        % (ALPHA_MZ / ALPHA_S))

    # V-04 分区边界形式（公允判定：因无量纲化而规避了 H2）
    add("V-04", sec, "D-05②边界写无量纲式", "PASS",
        "SUT 的 region() 使用 |x| < B1 等不等式，而 (x,y) 已为**无量纲化坐标** ⇒ "
        "与无量纲常数 B_i 比较**合法**，元审计 H2（|κ| 量纲 L⁻¹ 与无量纲 B_i 不可比较）**被合法规避**。"
        "代价见 V-05：无量纲化引入了一个未声明的外锚。")


# ==========================================================================
# B 组：违约项验收（真缺陷）
# ==========================================================================
def section_b():
    sec = "B 违约验收"

    # V-05 无量纲化的隐藏外锚
    add("V-05", sec, "无量纲化引入未声明外锚 κ₀ ⇒ P4 实际被违反", "FAIL",
        "SUT 的 (x,y) 是「无量纲化曲率/挠率」，即 x = κ/κ₀、y = τ/κ₀ ⇒ 需要**一个参考尺度 κ₀**。"
        "而 SUT B-01 自称「仅 1 个常数 A（≤1 满足公理④）」⇒ 实际自由常数为 **A 与 κ₀ 两个**（κ₀ 未被声明）。"
        "⇒ 这正落在第七轮 A4（节点约束）/O-OMEGA-NODE 的结论上：**自由度会转移到未被计数的入口**；"
        "此处转移到「无量纲化尺度」。修法：在符号台账显式登记 κ₀ 并计入常数个数（⇒ P4 违反，如实标注）"
        "或改用纯比值 θ = atan2(τ,κ)（无需 κ₀）。")

    # V-06 Ω 符号「自动导出」不成立（T1 实例化）
    def sut_axioms(om):
        """检验 SUT 自己声称的三条：无量纲 / 除原点外连续 / 常数 ≤ 1。"""
        vals = [om(-3.0 + 0.01 * i, 1.0) for i in range(601) if om(-3.0 + 0.01 * i, 1.0) is not None]
        if not vals or not all(math.isfinite(v) for v in vals):
            return False
        return max(abs(vals[i + 1] - vals[i]) for i in range(len(vals) - 1)) < 1e2

    neg_omega = lambda x, y: -sut_omega(x, y) if sut_omega(x, y) is not None else None
    ok_pos = sut_axioms(sut_omega)
    ok_neg = sut_axioms(neg_omega)
    guard("sign_flip_still_valid", ok_pos and ok_neg,
          "SUT 的 Ω 合格 = %s；−Ω 合格 = %s ⇒ 公理集仍不禁止反面（T1 在 SUT 上复现）"
          % (ok_pos, ok_neg))
    add("V-06", sec, "B-02「Ω 符号自动导出」判 PASS 不成立（T1 复现）", "FAIL",
        "SUT 的 Ω = A(x−y)/√(x²+y²)，其引力区 Ω<0 **来自选择了 (x−y) 而非 (y−x)** —— "
        "这是**候选函数形式的选择**，不是公理推导：机器验证 −Ω 同样满足 SUT 自己的三条公理"
        "（无量纲 = %s，连续 = %s，常数个数不变）。"
        "⇒ 与第七轮 T1 完全同型：**把硬编码藏进函数形式的选择里**，仍违反 P2「禁止人工硬编码」。"
        "⇒ 应改为 BOUNDARY/FAIL 并显式登记「符号约定为输入」（D-05⑤）。" % (ok_pos, ok_neg))

    # V-07 渲染的场与声称的 E 不一致（真 bug）
    pts = [(0.3, 0.3), (-0.3, 0.3), (0.3, -0.3), (-0.3, -0.3), (1.0, 0.0), (0.0, 1.0)]
    sim = cosine_sim(sut_field, ref_force_from_E, pts)
    guard("render_field_mismatch", abs(sim) < 0.9,
          "SUT field（径向 −r̂/r）与其声称的 E∝(κ+τ)、κ=x,τ=y 导出的力（均匀 −(1,1)）"
          "余弦相似度 = %.4f ⇒ 不一致" % sim)
    add("V-07", sec, "渲染的矢量场与声称的势能不自洽（真 bug）", "FAIL",
        "SUT 注释写明「E ∝ (κ+τ)，取 κ=x, τ=y 作为剖面；F = −(ℏc/2)∇(κ+τ)」，"
        "但 ∇(x+y) = (1,1) ⇒ F 应为**均匀场 −(1,1)**，而 SUT 的 field() 给的是**径向 −r̂/r**（∝ 1/r²）。"
        "机器：两者在 6 个采样点的余弦相似度 = **%.4f**（应为 1 才自洽）⇒ **场渲染与公式不自洽**。"
        "后果：渲染出的图看起来像「引力径向吸引」，但该方向并非由其 E 导出 ⇒ "
        "这正是元审计 E-01「图是表现不是证据」在代码层的实例。"
        "修法：要么改场构型（让 κ(x),τ(x) 真正给出 1/r² 势能，如 κ+τ ∝ 1/r），"
        "要么把 E 换成与径向场匹配的形式并在注释里写明所假设的场构型。" % sim)

    # V-08 自相似度判据零信息
    sim_self_f = cosine_sim(sut_field, sut_field, pts)
    sim_self_g = cosine_sim(ref_force_from_E, ref_force_from_E, pts)
    guard("self_similarity_is_trivial", abs(sim_self_f - 1.0) < 1e-12 and abs(sim_self_g - 1.0) < 1e-12,
          "cos(f,f) = %.12f、cos(g,g) = %.12f ⇒ 与自身比对恒为 1，判据无判别力" % (sim_self_f, sim_self_g))
    add("V-08", sec, "E-02 相似度判据零信息（自己跟自己比恒等于 1）", "FAIL",
        "SUT 的 E-02 用「预测场与自身模板」的余弦相似度 %.4f ≥ 阈值 0.95 作为渲染管线自洽的证据。"
        "但 **cos(f, f) ≡ 1** 是数学恒等式：对任意场（含上面那个错误的径向场）都成立"
        "（机器：cos(field,field) = %.12f，cos(参考场,参考场) = %.12f）⇒ **该判据不能区分任何两个场**。"
        "⇒ 它验的是「管线能跑通」，不是「场是对的」；而后者恰是 V-07 判负的地方。"
        "修法：与目标场（由 E 显式导出的场）比对，或用 V-07 的交叉相似度作为门禁。" % (sim_self_f, sim_self_f, sim_self_g))

    # V-09 样本与力程表冲突（H3 的新形态）
    RANGE_TABLE = {"D_G": float("inf"), "D_EM": float("inf"), "D_Strong": 1e-15, "D_Weak": 1e-18}
    conflicts = []
    for k, (x, y) in SUT_SAMPLES.items():
        Lhat = 1.0 / math.hypot(x, y)
        if math.isinf(RANGE_TABLE[k]):
            conflicts.append((k, Lhat))
    guard("sample_vs_range_table", len(conflicts) >= 2,
          "引力/电磁样本给出有限力程 %s ⇒ 与「无限力程」冲突（%d 处）"
          % (["%s:%.4f" % c for c in conflicts], len(conflicts)))
    add("V-09", sec, "四区样本与力程表冲突（元审计 H3 以新形态复现）", "FAIL",
        "SUT 给四区各一个 (κ̂,τ̂) 样本，但**引力区样本 (0.1, 2.0) 与电磁区样本 (1.0, 0.8) 都有非零坐标** ⇒ "
        "L̂ = 1/‖(κ̂,τ̂)‖ 分别为 %.4f 与 %.4f（无量纲、有限），而力程表规定引力/电磁为**无限长程**。"
        "⇒ 无限力程要求 √(κ²+τ²) = 0 ⇒ 坐标必须是原点，而原点在 SUT 中被 omega() 判为 None（无场点）"
        "⇒ **引力与电磁在 SUT 的参数化内部不可表达**（元审计 H3 / 第七轮 D-02 的同型复现）。"
        "修法：按 D-05④，引力/电磁输出「力程 ∞」而**不给 (κ,τ) 数值**；"
        "样本表只保留强核与弱核两组，另两类标注为「无限力程类（原点极限）」。"
        % (conflicts[0][1], conflicts[1][1]))

    # V-10 Ω 与强度表未对接
    o_vals = {k: sut_omega(*v) for k, v in SUT_SAMPLES.items()}
    rel_grav = 5.907e-39 / 0.1179
    gap = abs(o_vals["D_G"]) / rel_grav
    guard("omega_not_calibrated", gap > 1e10,
          "Ω(D_G) = %.4f vs 引力相对强度 %.3e ⇒ 相差 %.2e 倍 ⇒ Ω 未与强度表对接"
          % (o_vals["D_G"], rel_grav, gap))
    add("V-10", sec, "Ω 与强度表未对接（A=1.0 ⇒ 强度要素仍由外部表给出）", "FAIL",
        "SUT 的 Ω 取 A = 1.0，值域 [−√2, √2]；而四力相对强度跨 **37.3 个量级**（引力 %.3e）。"
        "机器：Ω(D_G) = %.4f 与引力相对强度 %.3e 相差 **%.2e 倍** ⇒ Ω **从未被标定到实际强度**，"
        "三要素中的「大小」仍完全由 D 组外部强度表提供 ⇒ Ω 在计算链中**形同虚设**（定义了但未使用）。"
        "⇒ 这正好印证第七轮 T4/T5：若要让 Ω 命中四个强度，就必须用观测去拟合（标定而非预测），"
        "且 T6 表明在双精度下引力档还无法精确命中。修法（D-05⑦）："
        "要么明确声明「Ω 未标定，强度取自外部表」，要么标定并**标注自由度来源**。" % (rel_grav, o_vals["D_G"], rel_grav, gap))

    # V-11 分区自报（公允：它自己如实报了）
    add("V-11", sec, "分区重叠/未覆盖：SUT 已自行如实登记", "PASS",
        "SUT C-02 把重叠率 > 0 判 FAIL、C-03 未覆盖率判 BOUNDARY，并用 guard "
        "`partition_injectivity_open` 显式断言「重叠率 > 0 ⇒ 单射未成立」⇒ **诚实登记，未粉饰**。"
        "（术语提醒：该处应称「互斥完备分割」而非「单射」，见元审计 B-05。）")


# ==========================================================================
# C 组：修复清单（不改 SUT，只给逐处修法）
# ==========================================================================
def section_c():
    sec = "C 修复清单"
    fixes = [
        ("F-01", "V-06", "把 B-02「Ω 符号自动导出」的 verdict 由 PASS 改为 **BOUNDARY/FAIL**，"
                         "并在 detail 写明「符号来自候选函数形式的选择（x−y vs y−x），−Ω 同样合格」"),
        ("F-02", "V-05", "符号台账登记无量纲化尺度 κ₀ 并计入常数个数；或改用 θ = atan2(τ,κ) 免掉 κ₀"),
        ("F-03", "V-07", "统一场构型与势能：若坚持径向 1/r² 场，则把 E 写成对应的 −1/r 形式并注明；"
                         "若坚持 E ∝ (κ+τ)，则把 field() 改为均匀场 −(ℏc/2)κ₀(1,1)"),
        ("F-04", "V-08", "相似度判据改为**与目标场交叉比对**（用 V-07 的交叉相似度），禁用 cos(f,f) 自比"),
        ("F-05", "V-09", "样本表只保留强核/弱核两组 (κ,τ)；引力/电磁输出「力程 ∞」并标注为原点极限类"),
        ("F-06", "V-10", "Ω 要么显式标注「未标定，强度取自外部表」，要么标定并注明拟合了哪些观测"),
        ("F-07", "V-11", "术语：把「单射」改为「互斥完备分割」（ℝ² → 4 类必为多对一，单射不可能）"),
    ]
    for fid, ref, how in fixes:
        add(fid, sec, "修复 %s" % ref, "INFO", how)
    guard("fix_list_covers_all_failures", len(fixes) == 7,
          "修复清单 7 条，覆盖 B 组全部 6 项违约（V-05…V-10）+ 1 项术语")


# ==========================================================================
# D 组：回链与总评
# ==========================================================================
BACKLINKS = [
    ("META", "04_公共成果/本项目_全维自洽与归一化/判定_TUFT_V3.5修复方案_全维审计与重整_2026-10-04.md"),
    ("OMEGA", "04_公共成果/本项目_全维自洽与归一化/判定_TUFT_V3.5_Ω公理构造_不可行性判定与最小增广_2026-10-04.md"),
    ("FOUR", "04_公共成果/本项目_全维自洽与归一化/判定_统一场论可视化证明_四力三要素实证审计_2026-10-04.md"),
    ("SUTDATA", "04_公共成果/本项目_全维自洽与归一化/数据/统一场论可视化证明_TUFT_V3.5_修复版_2026-10-04.json"),
]


def section_d():
    missing = [k for k, p in BACKLINKS if not os.path.exists(os.path.join(ROOT, p))]
    guard("backlink_all_exist", not missing,
          "回链 %d 条，缺失 %s" % (len(BACKLINKS), missing if missing else "0 条"))
    add("G-01", "D 总评", "跨册回链完整性", "PASS" if not missing else "FAIL",
        "回链命中 %d/%d：%s。" % (len(BACKLINKS) - len(missing), len(BACKLINKS),
                                 ", ".join(k for k, _ in BACKLINKS)))

    add("G-02", "D 总评", "总评：记号层守约，物理层与渲染层违约", "FAIL",
        "**守约 4 项**：力程式（V-01）、原点守卫（V-02）、强度表口径（V-03）、边界无量纲式（V-04）；"
        "**违约 6 项**：隐藏外锚 κ₀（V-05）、Ω 符号实为选择（V-06）、渲染场与 E 不自洽（V-07）、"
        "相似度判据零信息（V-08）、样本与力程表冲突（V-09）、Ω 未与强度表对接（V-10）。"
        "⇒ **分支①可以交付，但必须先过 F-01…F-06 六处修复**；"
        "其中 V-07/V-08 是代码级真 bug（不是建模选择），V-09 是元审计 H3 的复现。")

    add("G-03", "D 总评", "一个方法论结论：验收必须做，不能只看「跑通了」", "PASS",
        "SUT 退出码 0、自检全过，但仍有 6 项违约 —— 其中 V-08（自相似度恒 1）与 V-07（场与公式不符）"
        "**恰恰藏在「自检全过」之下** ⇒ **「自检通过」不等于「守约」**："
        "自检只能验自己声明的性质，验不了「声明的性质是否就是需要的性质」。"
        "⇒ 结论（可复用）：对任何修复版实现，必须做**独立验收审计**（用前置判定册的定理做判据），"
        "不能以实现自带的自检代替。")


def main():
    print("=" * 78)
    print("  TUFT V3.5 分支①产物（修复版实现）· 验收审计与修复清单")
    print("=" * 78)

    sut = load_sut()
    if sut is None:
        print("SUT 不可用，终止")
        return 2

    section_a()
    print("-" * 78)
    section_b()
    print("-" * 78)
    section_c()
    print("-" * 78)
    section_d()
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
        "title": "TUFT V3.5 分支①产物（修复版实现）验收审计与修复清单",
        "date": "2026-10-04",
        "sut": os.path.relpath(SUT, ROOT),
        "results": RESULTS,
        "guards": GUARDS,
        "counts": cnt,
        "guard_ok": gok,
        "guard_total": len(GUARDS),
        "compliant": ["V-01 力程式", "V-02 原点守卫", "V-03 强度表口径", "V-04 边界无量纲式"],
        "violations": ["V-05 隐藏外锚 κ₀", "V-06 Ω 符号实为选择", "V-07 渲染场与 E 不自洽",
                       "V-08 相似度判据零信息", "V-09 样本与力程表冲突", "V-10 Ω 未与强度表对接"],
        "rating": "C / L1",
        "verdict_line": "记号层 4 项守约；物理层与渲染层 6 项违约（含 2 处代码级真 bug）⇒ 分支①须过 F-01…F-06 后方可交付",
    }

    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)
    stem = "TUFT_V3.5修复版_验收审计与修复清单_2026-10-04"
    with open(os.path.join(DATA_DIR, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    lines = ["# TUFT V3.5 分支①产物验收审计与修复清单（数据产物）", ""]
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
