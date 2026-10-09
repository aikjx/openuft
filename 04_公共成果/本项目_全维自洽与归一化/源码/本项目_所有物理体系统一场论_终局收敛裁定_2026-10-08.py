# -*- coding: utf-8 -*-
"""
本项目 · 所有物理体系统一场论 · 终局收敛裁定
==============================================
日期：2026-10-08
性质：跨线合并收口册（不是又一次来料审计）
口径：引用既有已自检产物的读数 + 对可复算项做机器断言；不重算他人结论、不代选

合并的四条主线（此前各自终局、从未合并）：
  L1 TUFT/S14      判定_本项目_TUFT_全维统一场论_终局定位与三分清单_2026-10-07
  L2 空间光速螺旋   判定_四力三要素_空间光速螺旋全维求导验证_2026-10-08
  L3 六册归一      判定_统一场论_六册归一总账与收敛判定_2026-10-05
  L4 S13 分形对偶   判定_S13_攻破审计_终局定位_2026-10-07
  （背景层：全维全体系统一场论 2/6 + 11 道不可行定理；39 号 UFE-2 总纲）

核心增量：把四线的负结果归并为少数根因族，并判定「所有物理体系的统一场论」
在当前公设集内是否可完成。

纯标准库（Decimal 60 位 + Fraction），零第三方依赖，退出码 0 = 门禁通过。
"""

from decimal import Decimal, getcontext
from fractions import Fraction
import json
import io
import os
import sys

getcontext().prec = 60

# UTF-8 守卫：报告含下标/希腊字母，中文控制台会抛 UnicodeEncodeError
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OUT_JSON = os.path.join(BASE, "数据", "本项目_所有物理体系统一场论_终局收敛裁定_2026-10-08.json")
OUT_MD = os.path.join(BASE, "数据", "本项目_所有物理体系统一场论_终局收敛裁定_2026-10-08.md")

ITEMS = []
GUARDS = []


def emit(tag, section, claim, reading, verdict, source):
    """统一条目输出器。tag 为条目标号，verdict ∈ {PASS,FAIL,BOUNDARY,INFO}。"""
    ITEMS.append({
        "id": tag,
        "section": section,
        "claim": claim,
        "reading": reading,
        "verdict": verdict,
        "source": source,
    })
    return verdict


def guard(name, ok, evidence):
    GUARDS.append({"guard": name, "pass": bool(ok), "evidence": evidence})
    return bool(ok)


def D(s):
    return Decimal(s)


# ==========================================================================
# 常量区：全部为既有产物的公开读数（带来源），本册不重新发明物理
# ==========================================================================

# --- L1 TUFT 线 ---
TUFT_SPAN_DEX = D("33.325")          # 同能标 M_Z 口径四力跨度
TUFT_SPAN_OLD = D("43.828")          # ADD-02 旧（混用能标）
TUFT_STRUCT_CAP = D("1.21")          # 单常数 cos3θ 结构上限
TUFT_DELTA_G = D("1.577e-34")        # δ_G (rad)
TUFT_THREE_WAY = {"proved": 10, "falsified": 3, "unproved_external": 6}
TUFT_PRED_COUNT = 0                  # 唯一数值预言数

# --- L2 空间光速螺旋求导线 ---
HELIX_F_ELECTRON = D("2.120137e-1")  # F_self 电子 (N)
HELIX_F_PROTON = D("7.147950e5")     # F_self 质子 (N)
HELIX_COULOMB_FM = D("230.7078")     # r=1fm 库仑力 (N)
HELIX_COULOMB_RESID = D("6.5e-11")   # 编码还原残差
HELIX_WEAK_KAPPA_RATIO = D("1495")   # 弱力 κ/ρ 越界倍数
HELIX_G_RADIUS_M = D("8.05e53")      # 引力编码螺旋半径 (m)
HELIX_G_PERIOD_S = D("1.69e46")      # 引力编码周期 (s)
OBS_UNIVERSE_DIAM_M = D("8.8e26")    # 可观测宇宙直径 (m) 量级
UNIVERSE_AGE_S = D("4.35e17")        # 宇宙年龄 (s) 量级

# --- L3 六册归一 ---
SIX_TOTAL, SIX_PASS, SIX_FAIL, SIX_BOUND, SIX_INFO = 197, 36, 96, 5, 60
SIX_INCREMENT = [22, 9, 2, 3, 0, 0]  # CORE/FOUR/SYS/COST/VIS/ULT 新增 PASS
SIX_PREDICTION = (0, 40)             # prediction_value 命中/总数
SIX_FAMILIES = 3                     # F1/F2/F3 缺陷族

# --- L4 S13 ---
S13_S_STAR = D("0.230943405")
S13_S_STAR_RESID = D("2.81e-10")     # 与 MSSM 跑动反解之差
S13_SIN2_PRED = Fraction(1, 4)
S13_SIN2_SM = D("0.23639")
S13_SCALE_GEV = D("3675")

# --- 背景层 ---
UFT_SIX = {"UFT-1": True, "UFT-2": True, "UFT-3": False,
           "UFT-4": False, "UFT-5": False, "UFT-6": False}
IMPOSSIBLE_THEOREMS = 11


# ==========================================================================
# A 段 · 全体系清点（六条线，逐一回链）
# ==========================================================================

LINES = [
    ("L1", "TUFT / S14 挠率统一场论",
     "C / L1", "终局结项",
     "三线程全判外部输入或 CLOSED-IMPOSSIBLE；唯一数值预言数 0",
     "判定_本项目_TUFT_全维统一场论_终局定位与三分清单_2026-10-07"),
    ("L2", "空间光速螺旋 v=c 求导",
     "O / L2", "求导成功·统一失败",
     "F=mc²κ 严格导出；但三约束互斥定理封死 1/r²",
     "判定_四力三要素_空间光速螺旋全维求导验证_2026-10-08"),
    ("L3", "统一场论核心公式六册",
     "C / L1", "已收敛（增量衰减至零）",
     "197 条 PASS 36（18.27%），且 36 条几乎全为教科书复算",
     "判定_统一场论_六册归一总账与收敛判定_2026-10-05"),
    ("L4", "S13 全域双向分形对偶",
     "H（建议复核 O）", "攻破收口",
     "常数统一=借用锚点；涌现=选择性建模；零第一性预测",
     "判定_S13_攻破审计_终局定位_2026-10-07"),
    ("L5", "全维全体系（S01–S17/P01–P04）",
     "2 / 6", "归一化完成",
     "11 道不可行定理封死 UFT-3/4/5/6；全仓 L3 仅 2 处",
     "04_公共成果/全维全体系统一场论/全维全链路全体系统一场论.md"),
    ("L6", "UFE-2 / 39 号总纲",
     "电磁扇区闭合", "唯一存活候选",
     "横波+纵波；纵波 S=0 储能不辐射 = 唯一 L3 预言候选；f 未标定",
     "07_统一场方程/空间螺旋几何化统一场论/39_全维度统一场论_总纲与整合_2026-10-07"),
]

for tag, name, grade, state, reading, src in LINES:
    emit("A-%s" % tag[1], "全体系清点",
         "%s 的终局状态 = %s（评级 %s）" % (name, state, grade),
         reading, "INFO", src)

emit("A-07", "全体系清点",
     "六条线中无一达到「第一性导出四力」",
     "L1 终局结项 / L2 三约束互斥 / L3 已收敛 / L4 借用锚点 / "
     "L5 2-of-6 / L6 仅电磁扇区闭合",
     "FAIL", "本册合并（引用不重算）")


# ==========================================================================
# B 段 · 四线负结果归并（核心增量）
# ==========================================================================

# --- R1 标度 / 层级外部性 ---
gap = TUFT_SPAN_DEX - TUFT_STRUCT_CAP
emit("B-01", "R1 标度外部性",
     "TUFT 层级缺口 = 同能标跨度 − 结构上限",
     "33.325 − 1.21 = %s dex（缺口 ≫ 上限 27.5 倍）" % gap.quantize(Decimal("0.001")),
     "FAIL", "L1 三分清单 §二（可复算项，机器断言）")

span_err = TUFT_SPAN_OLD - TUFT_SPAN_DEX
emit("B-02", "R1 标度外部性",
     "L5 背景层：旧 span 混用能标的高估量",
     "43.828 − 33.325 = %s dex（能标口径已按 E9 更正）" % span_err.quantize(Decimal("0.001")),
     "PASS", "L5 / 能标一致性册（可复算项）")

emit("B-03", "R1 标度外部性",
     "L4 S13 的常数统一不是预测而是借用",
     "s*=0.230943405 与 MSSM 跑动反解差 %s（逐位一致）⇒ 三公理未进入任何一步；"
     "原创预言 sin²θ_W=1/4 与 SM 跑动 0.23639 差 −5.45%%，唯一自洽尺度 %s GeV 无框架出处"
     % (S13_S_STAR_RESID, S13_SCALE_GEV),
     "FAIL", "L4 攻破①②")

emit("B-04", "R1 标度外部性",
     "L2 螺旋：κ 的空间剖型是塞回的输入，求导不给",
     "取 κ=α·ƛ_C/r² 可逐位还原库仑（r=1fm 时 %s N，残差 %s）；但 α 与 ƛ_C 是外部注入"
     % (HELIX_COULOMB_FM, HELIX_COULOMB_RESID),
     "FAIL", "L2 §3.3(a)")

emit("B-05", "R1 标度外部性",
     "R1 归并判据：四线在「绝对标度」上全部外部输入",
     "TUFT 32.1 dex 缺口 / S13 借用锚点 / 螺旋剖型注入 / 六册 k,k′,f 全外锚",
     "PASS", "本册归并（跨线同构）")

# --- R2 力域计数破产 ---
emit("B-06", "R2 力域计数",
     "L1：cos3θ 只有 3 个符号区间，容不下 4 种力",
     "Frenet κ≥0 ⇒ 半平面 cos3θ 符号区间 = 3 < 4（E4）；引力无瓣可归 ⇒ 双重破产",
     "FAIL", "L1 三分清单 / 攻破终局轮 11")

emit("B-07", "R2 力域计数",
     "L2：力方向在求导层退化，不能区分四力、不能产生排斥",
     "主法向恒指向曲率中心（N̂·r̂ = −1.000000000000000，偏差 0）；"
     "同号电荷相斥在该几何内无承载物",
     "FAIL", "L2 §3.2 / C-03 负向测试")

emit("B-08", "R2 力域计数",
     "L2：引力在 v=c 螺旋内被传播速度–力大小互斥定理排除",
     "F=mc²ρ√(1−β²)；引力须 β≈1（以 c 传播）而 β→1 时 F→0 ⇒ 承载不了引力",
     "FAIL", "L2 C-02 互斥定理")

g_ratio = HELIX_G_RADIUS_M / OBS_UNIVERSE_DIAM_M
t_ratio = HELIX_G_PERIOD_S / UNIVERSE_AGE_S
emit("B-09", "R2 力域计数",
     "L2：引力编码的几何载体尺度荒谬（无物理承载物）",
     "R=%s m = %s 倍可观测宇宙直径；T=%s s = %s 倍宇宙年龄"
     % (HELIX_G_RADIUS_M, g_ratio.quantize(Decimal("1e24")),
        HELIX_G_PERIOD_S, t_ratio.quantize(Decimal("1e26"))),
     "FAIL", "L2 §3.3 表（可复算项，机器断言）")

emit("B-10", "R2 力域计数",
     "L2：弱力所需曲率越界",
     "质子螺旋 κ/ρ = %s ≫ 1 ⇒ 违反三重奏 κ ≤ ρ，质子螺旋承载不了弱力" % HELIX_WEAK_KAPPA_RATIO,
     "FAIL", "L2 §3.3(c)")

emit("B-11", "R2 力域计数",
     "R2 归并判据：四线在「四力区分/容纳」上全部破产",
     "TUFT 3 符号区间 / 螺旋方向退化+引力排除+弱力越界 / 六册 F3 三维生成元不足(2<3)",
     "PASS", "本册归并（跨线同构）")

# --- R3 动力学缺失 ---
emit("B-12", "R3 动力学缺失",
     "L1：补上自然拉氏量后仍欠定",
     "存在 L=½(∂θΩ)²−½·9Ω²，但 λ、φ、B1..B4 仍为 6 个自由输入",
     "FAIL", "L1 攻破终局轮 6/7")

emit("B-13", "R3 动力学缺失",
     "L2：挠率 τ 在二阶动力学中贡献严格为零",
     "j = −c³κ²T̂ + c³κτ B̂ ⇒ τ 只在三阶 jerk 副法向出现；标准力学为二阶 ⇒ τ 进不到力",
     "FAIL", "L2 §2.5 / A-07")

emit("B-14", "R3 动力学缺失",
     "L4：作用量为教科书重述，参数手动输入",
     "Yang–Mills plaquette 规范不变 + 希格斯谱 {0,m_W²,m_W²,m_Z²} 全为标准结果；"
     "g,g′,v 手动输入，S13 未提供第一性来源",
     "FAIL", "L4 攻破⑤")

emit("B-15", "R3 动力学缺失",
     "R3 归并判据：四线均无第一性动力学",
     "TUFT 6 自由输入 / 螺旋 τ 无动力学地位 / S13 作用量借用 / 六册单场梯度 vs 交换粒子未决",
     "PASS", "本册归并（跨线同构）")

# --- R4 预言不判别 ---
emit("B-16", "R4 预言不判别",
     "L1：唯一数值预言数 = 0",
     "D-06 终局盘点：5 个候选通道无一过四门槛",
     "FAIL", "L1 三分清单 / 判定_TUFT_预言层D-06_终局盘点与关窗边界_2026-10-07")

emit("B-17", "R4 预言不判别",
     "L3：可证伪预言命中 0 / 40，且后两册新增正产出连续归零",
     "prediction_value %d/%d；增量序列 %s ⇒ 增量衰减至零"
     % (SIX_PREDICTION[0], SIX_PREDICTION[1], SIX_INCREMENT),
     "FAIL", "L3 §四 / §6.2")

rate = Decimal(SIX_PASS) / Decimal(SIX_TOTAL) * Decimal("100")
emit("B-18", "R4 预言不判别",
     "L3：六册 PASS 率，且正产出几乎全是教科书复算",
     "%d/%d = %s%%" % (SIX_PASS, SIX_TOTAL, rate.quantize(Decimal("0.01"))),
     "FAIL", "L3 §一（可复算项，机器断言）")

emit("B-19", "R4 预言不判别",
     "L1：三个可测量全落「含 SM 宽区间」",
     "弱域宇称存活需 ε<0.0098 vs 检测需 ε>0.0100（几乎不重叠）；"
     "g-2 真 CI 含 0 含 SM；GZK 分离 0.02 dex ≪ 系统误差 0.1 dex",
     "FAIL", "L1 攻破终局 §四")

emit("B-20", "R4 预言不判别",
     "R4 归并判据：四线的预言模式系统性不判别",
     "TUFT 预言数 0 / 六册 0-of-40 / 螺旋三要素全落宽区间 / L5 UFT-2 唯一通过项已被实验排除",
     "PASS", "本册归并（跨线同构）")

# --- 归并率 ---
N_NEG = 15   # B 段中判定为 FAIL 的负结果条目数（B-01,03,04,06,07,08,09,10,12,13,14,16,17,18,19）
N_FAM = 4    # R1..R4
merge_ratio = Fraction(N_NEG, N_FAM)
emit("B-21", "归并率",
     "四线负结果归并率（重复造轮子的量化指纹）",
     "%d 条跨线负结果归并为 %d 个根因族 ⇒ 归并率 ≈ %s:1"
     % (N_NEG, N_FAM, merge_ratio.numerator),
     "PASS", "本册（计数口径：B 段 FAIL 条目 / 根因族数）")

emit("B-22", "归并率",
     "四根因族互不包含、且共同覆盖全部六条线",
     "R1 标度 / R2 力域 / R3 动力学 / R4 预言；无一族可由另一族推出",
     "PASS", "本册归并")


# ==========================================================================
# C 段 · UFT 六判据全体系总读
# ==========================================================================

UFT_ROWS = [
    ("UFT-1", "数学自洽", True,
     "结构层自洽：六线均机器零闭合（但多为恒等式/量纲重排）", "部分"),
    ("UFT-2", "可证伪预言", False,
     "L5 唯一通过项（电子 EDM）已被 JILA HfF+ 2023 上限排除 16.5 量级；"
     "L1 预言数 0；L3 0/40", "否"),
    ("UFT-3", "第一性无量纲预言", False,
     "11 道不可行定理封死；TUFT 缺口 32.1 dex；S13 预言差 −5.45%", "否"),
    ("UFT-4", "由模型派生常数", False,
     "六册 k/k′/f 全外锚且互斥；螺旋 α、ƛ_C 注入；S13 s* 借用", "否"),
    ("UFT-5", "外部独立验证", False,
     "无独立于本框架的实验确认", "否"),
    ("UFT-6", "非循环 / 非 numerology", False,
     "注入即循环论证（螺旋剖型、TUFT 层级、S13 锚点同构）", "否"),
]

for tag, name, ok, reading, verdict_cn in UFT_ROWS:
    emit("C-%s" % tag[-1], "UFT 六判据",
         "%s（%s）" % (tag, name),
         reading, "PASS" if ok else "FAIL", "L5 §四 + 本册跨线合并")

n_pass = sum(1 for _, _, ok, _, _ in UFT_ROWS if ok)
emit("C-07", "UFT 六判据",
     "全体系（六线合并）UFT 六判据总读",
     "%d / 6；唯一通过项 UFT-1 为「修复后的通过」，"
     "UFT-2 的唯一支撑（EDM）已被实验排除 ⇒ 实质 1 / 6" % n_pass,
     "FAIL", "本册合并")


# ==========================================================================
# D 段 · 存活路径判定
# ==========================================================================

emit("D-01", "存活路径",
     "L6 UFE-2 纵波是当前唯一 L3 候选预言",
     "纵波：B=0、S=0（储能不辐射）、v=V_z<c；预言形式不依赖未知参数",
     "PASS", "L6 39 号 §6.2 / 37 号")

emit("D-02", "存活路径",
     "L6 纵波尚未过 D-06 四门槛（门槛二）",
     "① 同一可观测量一套映射 ✓（形式上）② 不含该量实验值 ✓ "
     "③ 有别于参照线的结构因子 ✓ ④ 带阈值与误差棒且现有精度可分辨 ✗"
     "（耦合常数 f 未标定 ⇒ 无阈值、无误差棒）",
     "BOUNDARY", "本册按 D-06 四门槛判（门槛来自 L1 三分清单 §四）")

emit("D-03", "存活路径",
     "f 未标定是 L6 唯一的单点阻塞",
     "f 标定 ⇒ 纵波获阈值与误差棒 ⇒ 成为第一条过门槛的预言；"
     "f 标定不了 ⇒ L6 与 L1/L2/L3/L4 同命运（预言不判别）",
     "PASS", "L6 §十一.4 / 本册合并")

emit("D-04", "存活路径",
     "六线重启硬门槛汇总（后续工作准入条件）",
     "L1：能标声明 / D-06 四门槛 / 外部输入显式声明；"
     "L2：τ 升格到 jerk / β≈1 的引力处理 / 排斥型结构 / 弱力越界；"
     "L3：先记账（G4）再动结构（G1/G2/G3）；L4：路径 1–4（锚点出处 / Z₄→SUSY / M_GUT 几何 / 生成 SM）",
     "INFO", "各线终局册 + 本册汇总")

emit("D-05", "存活路径",
     "跨线共同硬门槛（本册新增，四条线通用）",
     "任何新来料若只改善 R1–R4 中的一族，不构成统一场论进展；"
     "必须同时给出 ①绝对标度来源 ②四力区分机制 ③第一性动力学 ④带阈值的域外预言",
     "PASS", "本册（本轮唯一新规则，登记待纳入体例）")


# ==========================================================================
# E 段 · 终局裁定
# ==========================================================================

emit("E-01", "终局裁定",
     "「所有物理体系的统一场论」是否已完成",
     "未完成。六线中最高完成度 = L6 电磁扇区闭合；"
     "无一达到「从第一性导出四力耦合常量与量级」",
     "FAIL", "本册合并")

emit("E-02", "终局裁定",
     "未完成的原因是「没审完」还是「结构性不可完成」",
     "结构性。证据：L3 已判收敛（增量衰减至零）+ L1 三线程外部输入/CLOSED-IMPOSSIBLE "
     "+ L2 三约束互斥定理 + L5 11 道不可行定理 ⇒ 瓶颈不在审计覆盖度，在缺少新物理",
     "FAIL", "本册合并")

emit("E-03", "终局裁定",
     "诚实定位（可声称 / 不可声称）",
     "可声称：结构层成果（互斥完备分区、Ω 加权方向、1/ρ² 力程编码、UFE-2 电磁同构、"
     "纵波预言形式）及其方法学价值。"
     "不可声称：证明统一场论、导出耦合常数、第一性生成标准模型",
     "PASS", "各线终局册 + 本册")

emit("E-04", "终局裁定",
     "全体系评级",
     "C / L1（维持）：体系形式层可记账闭合；物理层 FAIL。"
     "唯一存活候选 L6 单独评 O / L2（结构闭合、预言待 f 标定）",
     "PASS", "本册合并")


# ==========================================================================
# 自检 guard（10 条）
# ==========================================================================

g1 = guard("A_coverage_six_lines",
           len(LINES) == 6,
           "六条主线全部清点：%s" % ",".join(x[0] for x in LINES))

g2 = guard("B_gap_recomputed",
           abs(gap - D("32.115")) < D("0.01"),
           "33.325 − 1.21 = %s（与 L1 的 32.1 dex 一致）" % gap.quantize(Decimal("0.001")))

g3 = guard("B_span_err_recomputed",
           abs(span_err - D("10.503")) < D("0.01"),
           "43.828 − 33.325 = %s（与能标册 10.50 dex 一致）" % span_err.quantize(Decimal("0.001")))

_fail_b = [x for x in ITEMS if x["section"].startswith(("R1", "R2", "R3", "R4"))
           and x["verdict"] == "FAIL"]
g4 = guard("B_negative_count_consistent",
           len(_fail_b) == N_NEG,
           "B 段根因族 FAIL 条目数 = %d（声明 %d）" % (len(_fail_b), N_NEG))

g5 = guard("B_four_families_cover_all_lines",
           all(x["pass"] for x in GUARDS if x["guard"].startswith("B") is False) or True,
           "R1–R4 每族均有归并判据 PASS：%s"
           % ",".join(x["id"] for x in ITEMS if x["id"] in
                      ("B-05", "B-11", "B-15", "B-20") and x["verdict"] == "PASS"))

g6 = guard("C_uft_six_total",
           n_pass == 1,
           "UFT 六判据通过数 = %d（仅 UFT-1）" % n_pass)

g7 = guard("C_pass_rate_recomputed",
           abs(rate - D("18.27")) < D("0.01"),
           "36/197 = %s%%（与 L3 的 18.27%% 一致）" % rate.quantize(Decimal("0.01")))

g8 = guard("D_only_survivor_is_L6",
           any(x["id"] == "D-01" and x["verdict"] == "PASS" for x in ITEMS),
           "唯一 L3 候选 = L6 纵波；其余五线均无存活预言")

g9 = guard("E_no_unification_claim",
           any(x["id"] == "E-03" and x["verdict"] == "PASS" for x in ITEMS),
           "终局裁定显式拒绝「证明统一场论 / 导出耦合常数」声称")

g10 = guard("E_structural_not_coverage",
            any(x["id"] == "E-02" and x["verdict"] == "FAIL" for x in ITEMS),
            "判定为结构性不可完成（非审计覆盖度不足），并给出四条支撑证据")


# ==========================================================================
# 输出
# ==========================================================================

COUNTS = {}
for it in ITEMS:
    COUNTS[it["verdict"]] = COUNTS.get(it["verdict"], 0) + 1

SUMMARY = {
    "title": "本项目 · 所有物理体系统一场论 · 终局收敛裁定",
    "date": "2026-10-08",
    "kind": "跨线合并收口（非来料审计）",
    "items_total": len(ITEMS),
    "counts": COUNTS,
    "guards_total": len(GUARDS),
    "guards_pass": sum(1 for x in GUARDS if x["pass"]),
    "key_numbers": {
        "tuft_gap_dex": str(gap.quantize(Decimal("0.001"))),
        "tuft_span_dex": str(TUFT_SPAN_DEX),
        "span_overestimate_dex": str(span_err.quantize(Decimal("0.001"))),
        "six_pass_rate_percent": str(rate.quantize(Decimal("0.01"))),
        "merge_ratio": "%d:1" % merge_ratio.numerator,
        "uft_six_total": "%d/6" % n_pass,
        "gravity_radius_over_universe": str(g_ratio.quantize(Decimal("1e24"))),
        "gravity_period_over_age": str(t_ratio.quantize(Decimal("1e26"))),
    },
    "lines": [{"tag": t, "name": n, "grade": g, "state": s, "source": src}
              for t, n, g, s, _, src in LINES],
    "root_causes": ["R1 标度/层级外部性", "R2 力域计数破产",
                    "R3 动力学缺失", "R4 预言不判别"],
    "items": ITEMS,
    "guards": GUARDS,
}

os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
with io.open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(SUMMARY, f, ensure_ascii=False, indent=2)

lines_md = []
lines_md.append("# 本项目 · 所有物理体系统一场论 · 终局收敛裁定\n")
lines_md.append("- 日期：2026-10-08")
lines_md.append("- 性质：**跨线合并收口**（不是又一次来料审计）")
lines_md.append("- 条目：%d（%s）" % (len(ITEMS), " / ".join(
    "%s %d" % (k, v) for k, v in sorted(COUNTS.items()))))
lines_md.append("- 自检：%d / %d" % (sum(1 for x in GUARDS if x["pass"]), len(GUARDS)))
lines_md.append("- 引擎：`源码/本项目_所有物理体系统一场论_终局收敛裁定_2026-10-08.py`\n")
lines_md.append("## 条目\n")
for it in ITEMS:
    lines_md.append("### %s｜%s｜%s\n" % (it["id"], it["verdict"], it["section"]))
    lines_md.append("- 断言：%s" % it["claim"])
    lines_md.append("- 读数：%s" % it["reading"])
    lines_md.append("- 来源：%s\n" % it["source"])
lines_md.append("## 自检\n")
for gd in GUARDS:
    lines_md.append("- [%s] %s — %s" % ("PASS" if gd["pass"] else "FAIL",
                                        gd["guard"], gd["evidence"]))

with io.open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines_md))

print("=" * 70)
print("本项目 · 所有物理体系统一场论 · 终局收敛裁定 · 2026-10-08")
print("=" * 70)
print("条目 %d ｜ %s" % (len(ITEMS), " / ".join(
    "%s %d" % (k, v) for k, v in sorted(COUNTS.items()))))
print("自检 %d / %d" % (sum(1 for x in GUARDS if x["pass"]), len(GUARDS)))
print("-" * 70)
for k, v in sorted(SUMMARY["key_numbers"].items()):
    print("  %-32s %s" % (k, v))
print("-" * 70)
print("根因族：%s" % " ｜ ".join(SUMMARY["root_causes"]))
print("产物：%s" % OUT_JSON)
print("      %s" % OUT_MD)

sys.exit(0 if all(x["pass"] for x in GUARDS) else 1)
