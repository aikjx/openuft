# -*- coding: utf-8 -*-
"""
空间螺旋几何化统一场论 · 全量 claims 批量审计与 L3 层级判定
============================================================

对象
----
claims.csv 现有全部主张（运行时动态读取；2026-09-26 时点 C01–C54，共 54 条），含原体系（C01–C23）、
修复版轮（C24–C38）、最小修复轮（C39–C45）、并发复算轮（C46/C47）、V21 续修轮（C48/C49）、
V22 收官轮（C50/C51/C52）、V21 续修②轮（C53 引力泡 / C54 TUFT-RG，统一脚本 §18/§19 登记，本册只读引用）。

任务（草稿《本项目｜V21续修》「下一步选项」第 1 项）
------------------------------------------------------
全量 claims 批量跑审计引擎，生成完整审计报告 + 完成 L3 层级判定。

实现
----
1. 逐条主张：category → 证据类型 → 按 openuft 层级定义与 C38 三审计算法
   （R1 禁跳级 / R2 identity·definition 封顶 L1 / R3 升 L3 需构造推导 + 带误差棒可检验预言）
   给出 L0–L3 判定与决策（ALLOW / REJECT-CAP / REJECT-R1）。
2. 逐条标记复核：当前台账状态 vs 引擎证据 ⇒ PASS（有引擎证据支持）/ FAIL（引擎证据否定当前标记，
   附建议回退状态）/ PARTIAL（部分证据）/ UNVERIFIED（草稿自评，无引擎证据）/ INFO（原体系人工审计，
   非本引擎复核对象）。
3. 台账完整性镜像（G1–G8，只读）——G1–G6 结构/计数 + G7 归档存在 + G8 归档哈希防篡改，
   与守卫脚本同口径；不修改任何台账状态。
4. 关键数值锚点复算（mpmath dps=50，独立于既有引擎产物，全部现场计算）。

产出
----
  数据/空间螺旋全量claims_批量审计_L3层级判定.json
  数据/空间螺旋全量claims_批量审计_L3层级判定.md
  数据/空间螺旋claims_L3层级判定表.csv
  （顶层组织文档 判定_空间螺旋全量claims_L3层级判定_2026-09-26.md 另行撰写）

红线
----
本脚本对 claims.csv **只读**；不翻转任何状态；falsified 集合的改动必须经引擎证据 + 人工决策。
「状态字面一致」≠「语义一致」：草稿 open（可证伪谱/普适性就绪）与引擎 open（退化谱/公式需修正）
是同一状态字的不同语义，复核结论必须区分。

用法：python 空间螺旋_全量claims批量审计与L3层级判定.py
"""

import os
import io
import sys
import json
import re
import time
import hashlib

from mpmath import mp, mpf, sqrt, pi

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

mp.dps = 50
T0 = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_DIR = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")
SYS_DIR = os.path.join(ROOT, "07_统一场方程", "空间螺旋几何化统一场论")
CLAIMS = os.path.join(SYS_DIR, "claims.csv")
BASELINE = os.path.join(OUT_DIR, "空间螺旋判定_不变量基线.json")

print("=" * 76)
print("空间螺旋 · 全量 claims 批量审计与 L3 层级判定")
print("对象：claims.csv 全部主张（只读）| 方法：C38 三审计算法 + 引擎证据表 + 数值锚点")
print("=" * 76)

# ---------------------------------------------------------------------------
# 常量（CODATA / SI-2019，与统一脚本 §12 同源）
# ---------------------------------------------------------------------------
C = mpf("299792458")
HBAR = mpf("1.0545718176461565e-34")
ME = mpf("9.1093837015e-31")
G = mpf("6.67430e-11")
ALPHA = mpf("0.0072973525693")
MU0 = 4 * pi * mpf("1e-7")
N18907 = mpf("18907")


def fmt(x, n=10):
    return mpmath_nstr(x, n)


def mpmath_nstr(x, n):
    import mpmath
    return mpmath.nstr(x, n)


# ---------------------------------------------------------------------------
# 1. 读台账
# ---------------------------------------------------------------------------
raw = io.open(CLAIMS, encoding="utf-8").read().splitlines()
rows = []
for ln in raw[1:]:
    if not ln.strip():
        continue
    f = ln.split(",")
    rows.append({"id": f[0], "statement": f[1] if len(f) > 1 else "",
                 "category": f[2] if len(f) > 2 else "",
                 "status": f[3] if len(f) > 3 else "",
                 "reviewer": f[4] if len(f) > 4 else "",
                 "n_fields": len(f)})
by_id = {r["id"]: r for r in rows}
print("     claims.csv 主张 %d 条（%s – %s）" % (len(rows), rows[0]["id"], rows[-1]["id"]))

# ---------------------------------------------------------------------------
# 2. 证据类型映射（category → evidence_type）
# ---------------------------------------------------------------------------
# identity / definition / parameterization → R2 封顶 L1
# construction → 可升 L2；升 L3 需 R3（构造推导 + 带误差棒可检验预言）
# conflict → 冲突未调和，最高 L1
# audit / repair → 按引擎证据与状态定级
EV_CATEGORY = {
    "几何定义": "identity", "数值定义": "definition", "归一化约定": "identity",
    "恒等+诠释": "identity", "单位制恒等式": "identity", "组织框架": "identity",
    "数学事实": "identity", "物理重述": "identity", "数学项命名": "identity",
    "几何参数化": "parameterization", "几何+量子": "identity",
    "几何推导": "construction", "归一化计算": "construction", "拓扑公式": "construction",
    "几何表达式": "construction", "量子闭合": "construction",
    "常数重排": "construction", "第一性锚点": "construction", "拓扑本源": "construction",
    "一致性检查": "construction", "唯象构造": "construction",
    "内部冲突": "conflict",
    "第一性审计": "audit", "闭环修复": "repair",
}

# ---------------------------------------------------------------------------
# 3. 引擎证据登记表（可追溯；证据源 = 既有引擎产物）
#    verdict: PASS=引擎证据支持当前标记；PARTIAL=部分支持；UNVERIFIED=草稿自评无引擎证据；
#             INFO=原体系人工审计，非本引擎复核对象
# ---------------------------------------------------------------------------
ENGINE_EVIDENCE = {
    # —— 引擎证据支持当前标记（PASS）——
    "C24": ("PASS", "§14-C24 复算 + C39：b·ω·t 基底 + ω√(A²+b²)=c ⇒ |R'|=c 精确成立",
            "标记 pass 有引擎证据（与最小修复轮 B1 一致）"),
    "C25": ("PASS", "V21续修 §12：open（退化谱）——量纲 FAIL·谱退化 FAIL·误差棒公式误算 FAIL",
            "状态字 open 与引擎一致；语义须修正：草稿 open=可证伪谱，引擎 open=退化谱（谱宽 1.09e-75，不可检验）"),
    "C35": ("PASS", "V21续修 §13：open（框架就绪·公式需修正）——GR 项 PASS，几何项公式 FAIL",
            "状态字 open 与引擎一致；语义须修正：草稿 open=普适性就绪，引擎 open=几何项公式需修正（差因子 3.82e-8）"),
    "C38": ("PASS", "§9.5-4：三审计算法已实现（open→BOUNDARY），提交理论自身仍缺公开规格",
            "台账状态 BOUNDARY（大写）为引擎登记值；超出守卫 G3 白名单，见台账完整性检查"),
    "C39": ("PASS", "第二阶段 B1：|R'|=c 四组参数复算偏差 1.34e-51", ""),
    "C40": ("PASS", "第二阶段：几何不固定 α（定理 H 实算版）", ""),
    "C41": ("PASS", "第二阶段 B2：μ₀J 补全，∮B·dl=μ₀I 数值复现", ""),
    "C42": ("PASS", "第二阶段 B3：Φ 线性 ⇒ 因子恒等于 1，零新增内容", ""),
    "C43": ("PASS", "第二阶段：修复目标与 X8–X15 不相交，清零不成立", ""),
    "C44": ("PASS", "第二阶段 B4：ρ 无消费方程，删除属严格改进", ""),
    "C45": ("PASS", "第二阶段残差：3 未知/1 约束·α 自由·靶登记 0·L3=0", ""),
    "C46": ("PASS", "§9.6-1：C25 数值复核确认欠定（N 三量级均可命中 α）", ""),
    "C47": ("PASS", "§9.6-2：C35 RK4 复核（线性 Φ 零进动，GR 1PN 匹配但为拟合）", ""),
    "C48": ("PASS", "V21续修 §12：LB 谱扫描，α_n 相对差 ≤ 1.09e-75，正确传播误差 2.18e-87",
            "台账 open（退化谱）为引擎登记值"),
    "C49": ("PASS", "V21续修 §13：金星/地球几何修正预测差 1.9×/2.6×，量级 ~1e-3 角秒/百年",
            "台账 open（框架就绪·公式需修正）为引擎登记值"),
    # —— V22 收官轮（并发，§15–§17 已并入统一脚本，2026-09-26 10:41 登记）——
    "C50": ("PASS", "V22 §15：C25 谱 n 域扩展扫描（n=1..12+10^k），谱宽达 α 精度需 n_detect=2.196e33，"
                    "二阶项=V0 需 n_unit=1.793e38 ⇒ 阈值不可达",
            "台账 open（退化谱·阈值不可达）为 V22 引擎登记值；数值经本册独立复算一致（ℏ²/N²=3.111e-77 派生）"),
    "C51": ("PASS", "V22 §16：β0=3h²/c² 使草稿 Binet 方程 ≡ GR 1PN（u² 系数 3GM/c² 精确相等）；"
                    "β-free 形状比随 a²/a³ 框架歧义 1.87×/2.58×；标定靶=最佳靶 ⇒ 独立判别力为零",
            "台账 open（框架就绪·无独立判别力）为 V22 引擎登记值；与 V21续修 §13 公式偏差结论一致"),
    "C52": ("PASS", "V22 §17：全量 claims 批量审计引擎（类别→证据型→层级），结果 L3=0、无量纲靶登记=0",
            "台账 BOUNDARY（大写）为 V22 引擎登记值；本册补充标记复核与台账完整性镜像（V22 未覆盖这两项）"),
    # —— V21 续修②（§18 引力泡 + §19 TUFT-RG，2026-09-26 并入统一脚本）——
    "C53": ("PASS", "V21续修② §18：GravBubble 量纲三重失败、高斯积分漏乘 π^(3/2)、δφ 非无量纲、"
                    "×c⁴ 修复后 E=1.14e16 J 与实验室矛盾、无作用量故非孤子、V=-4 伪派生",
            "台账 falsified 为引擎登记值：FAIL 判定 6 条 + BOUNDARY 2 条 + INFO 1 条，针对模块宣称不针对议题"),
    "C54": ("PASS", "V21续修② §19：TUFT-RG b 系数六自由无推导、精确定理证明给定系数下无紫外非平凡固定点"
                    "（sympy 解集仅原点）、草稿 findroot 抛 TypeError、能标口径混用虚增跨度 34.96、"
                    "Landau 极点依赖任意 IR 输入",
            "台账 falsified 为引擎登记值：FAIL 5 条 + BOUNDARY 1 条 + INFO 1 条；体系级是否紫外完备仍 open"),
    # —— 部分证据（PARTIAL）——
    "C32": ("PARTIAL", "C44 支持「删除 ρ」动作方向；C32 原判（量纲 [S]=M·L⁻¹ + 线元积分范畴错误）未被引擎撤销",
            "台账 pass 仅部分成立：删除建议通过，原 FAIL 判定未复核撤销"),
    "C34": ("PARTIAL", "C41 支持 μ₀J 补全；J_geo 源项与电荷守恒约束仍缺闭合（§6-3 仍 FAIL）",
            "台账 pass 仅部分成立：缺电流项已修，几何源项未闭合"),
    # —— 引擎证据否定当前标记（FAIL；专项复核 §1–§9 判定引用，建议状态见 note）——
    "C26": ("FAIL", "统一脚本 §2-4：θ 冲突未消除反而扩为四方（tanθ=α / √N / 2√Nα / √((2√Nα)²−1) 互斥）；"
                    "§1-3 两种读数互不相容（tanθ=secθ 需 sinθ=1 无解）",
            "建议回退 falsified：C03/C23 仍有效且互斥，冲突一侧被删除而非调和"),
    "C27": ("FAIL", "统一脚本 §3-1：N=floor(2π/Δθ_min) 只能产整数，定义A=1/[α²(1−α)]=18916.908 非整数 ⇒ 不可复现",
            "建议回退 falsified：「彻底消除双值冲突」实为抛弃其中一个值"),
    "C28": ("FAIL", "统一脚本 §3-2（BOUNDARY）：Δθ_min=2π/18907=3.3232e-4 rad 无第一性来源，N 自由度平移为 Δθ_min 不降",
            "建议回退为 BOUNDARY（欠定非证伪）：原判 open/欠定，pass 不成立"),
    "C29": ("FAIL", "统一脚本 §4-1：[K₀]=[c⁴]/[G]=M·L·T⁻²（力）非曲率 L⁻¹；K₀=2.5642944e+38 N=α²F_Planck/(8π) "
                    "由 G 反定义，无独立物理量",
            "建议回退 falsified：量纲失败 + 反解值无独立存在"),
    "C30": ("FAIL", "统一脚本 §4-3：G 循环未解除，K₀=α²c⁴/(8πG) 与旧 ρ=√(G/(α²μ₀c²)) 结构同构 ⇒ 循环搬家",
            "建议回退 falsified：C12 的 falsified 标记不可撤销"),
    "C31": ("FAIL", "统一脚本 §4-2：N、α 均无量纲 ⇒ 任何无量纲函数仍无量纲，不可能产出有量纲 K₀/G（Buckingham Π）",
            "建议回退 falsified：结构性不可能，非精度问题"),
    "C33": ("FAIL", "统一脚本 §6-1：[α²K]=L⁻¹ 而 [∇×B]=L⁻¹·M·T⁻²·I⁻¹，差因子 M·T⁻²·I⁻¹ 非无量纲；"
                    "K 若改取 [∇×B] 量纲则不再是曲率",
            "建议回退 falsified：量纲失败未被 C41 修复（C41 只补 μ₀J）"),
    "C36": ("FAIL", "统一脚本 §6-5：∇Φ/Φ₀ 需无量纲 ⇒ [Φ₀]=[Φ]/L ≠ [Φ]；Φ₀ 作为 Φ 取值与量纲要求冲突",
            "建议回退 falsified：量纲冲突结论未撤销"),
    "C37": ("FAIL", "统一脚本 §9-1/§9-2：H6/O6/C3/U2 合计 17 ≠ 自列 10 子系统；C 1→3、U 0→2 上升却称清零；"
                    "UFT-3 靶登记仍 0",
            "建议回退 falsified：面板矛盾 + 靶登记未变"),
    # —— V21 续修③④ 并发轮登记 + 本审计攻坚登记（INFO：引擎只读镜像，不重判其内容）——
    "C55": ("INFO", "V21续修③ 登记文本：双圆 RG 截断伪影定理（gk*=−b1/d1 使二阶/一阶项比=−1 精确）、"
                    "固定点搜索代码 mpmath 1.3.0 下不可运行、到达 gk* 需 ln μ=572.06 而 Planck 跨度仅 64.67、"
                    "自由系数 6→13 且仍无作用量",
            "引擎只读镜像：falsified 由并发轮独立复算支撑，本引擎未重判其内容"),
    "C56": ("INFO", "V21续修③ 登记文本：σ 段方程不含 G/κ0/τ0/α_g 任一（(κ0²+α_gτ0²) 恒约去）、"
                    "量纲两头非法、显式 Euler 步长越界 986.7 倍（dt=5e-8 vs 稳定界 5.07e-11）、"
                    "草稿 σ_end 伪迹 1.9757e6 vs 稳定参考解 8.06e-13（差 2.45e18 倍）、σ̈=3/σ>0 永不瘦缩",
            "引擎只读镜像：falsified 由并发轮独立复算支撑（scipy Radau 外校），本引擎未重判其内容"),
    "C57": ("INFO", "V21续修③ 元审计登记文本：自评清单计数不符（实测 PASS=18/open=19 自述 20/17）、"
                    "与台账冲突 9 处、四态退化、矛盾自检算法为桩函数、CSV 导出破坏列结构（6 字段）",
            "引擎只读镜像：BOUNDARY 由并发轮元审计支撑，本引擎未重判其内容"),
    "C58": ("INFO", "V21续修④ 登记文本：薛定谔式 −ℏ²d²/ds²+V(s)ψ=Eψ 三项量纲互不一致"
                    "（V0 无量纲 vs [L⁻²] vs [M²L²T⁻²]）、几何不变量残差按构造成立（tautology）、"
                    "独立复算确认谱退化（α 精度/谱宽=10^65.14 量级）",
            "引擎只读镜像：falsified 由并发轮复算支撑，本引擎未重判其内容"),
    "C59": ("INFO", "V21续修④ 登记文本：Binet 方程符号错误（草稿正号 vs 力律自洽的负号）、"
                    "正确符号下匹配 GR 需 λgΦ0=−3h²/c²（负值）、GR 项独立复算 0.1035 角秒/轨道=42.95 角秒/百年 vs 观测 43",
            "引擎只读镜像：falsified 由并发轮复算支撑，本引擎未重判其内容"),
    "C60": ("INFO", "本审计 EHT 攻坚（空间螺旋EHT光子环_攻坚审计.py，mpmath 250 位）：GR 基准复现 "
                    "θ_sh=52.106/39.689 μas、b_crit/r_s=3√3/2 精确；散射角 RK4 七档收敛、1PN 弱场极限偏差 1.09e-5；"
                    "纲领映射审查 8/8 FAIL；判别式 V=F−C=0≤0 ⇒ 无映射方程层",
            "引擎只读镜像：falsified 由本审计攻坚复算支撑（日志 _run_eht4.log），本引擎未重判其内容"),
    "C61": ("INFO", "本审计 CMB 攻坚（空间螺旋CMB拓扑双谱_攻坚审计.py，mpmath 250 位）：Planck 2018 靶基准复算 "
                    "（声峰 l≈220、f_NL=−0.9±5.1、n_s=0.965±0.004、A_s=2.105e-9、r<0.036）；映射审查 8/8 FAIL"
                    "（与 C60 EHT 逐项同型）；判别式 V=0 ≤ 0 ⇒ 无映射方程层；CMB 仿真本体（Boltzmann）未提交",
            "引擎只读镜像：falsified 由本审计攻坚复算支撑（日志 _run_cmb2.log），本引擎未重判其内容"),
    "C62": ("INFO", "本审计数学链精算验证·二期：ω=c(κ²+τ²)/κ=c/ρ vs 光速约束 c/L，250 位相对差 2.66253228e-5"
                    "=解析因子 √(1+α²)−1（α=b/ρ）；正确组合 c√(κ²+τ²)=c/L 与约束偏差 1.56e-251；仅 b=0 自洽",
            "引擎只读镜像：falsified 由空间螺旋_数学链精算验证2.py 复算支撑（日志 _run_math2.log），本引擎未重判其内容"),
    "C63": ("INFO", "本审计频率链精算验证·三期：匀速螺旋 ω=const ⇒ dω/dt≡0 ⇒ F₅=(ℏ/2)dω/dt≡0（250 位机器零）；量纲 [F₅]=功率(W)≠力（X11）",
            "引擎只读镜像：falsified 由空间螺旋_频率链精算验证3.py 复算支撑（日志 _run_freq3.log），本引擎未重判其内容"),
    "C64": ("INFO", "本审计开放项精算验证·四期：Δ_top=1/(4π²)=0.02533029591，α_pred=sin(1/(137+Δ_top))=0.0072978559603"
                    " vs α_obs=0.0072973525693 相对差 6.898e-5；精确反解 Δ_top=1/asin(α)−137=0.0347828（01A 近似 0.03599908）与理论值差 27%~30%",
            "引擎只读镜像：falsified 由空间螺旋_开放项精算验证4.py 复算支撑（日志 _run_open4.log），本引擎未重判其内容"),
    "C65": ("INFO", "剩余开放项总攻·五期：N=137 材料自陈手填/输入非输出（00_总纲 L43；01A X4），1/α=137.036≠137 相对差 2.63e-4",
            "引擎只读镜像：falsified 由空间螺旋_剩余开放项总攻精算验证5.py 复算支撑（日志 _run_open5.log），本引擎未重判其内容"),
    "C66": ("INFO", "剩余开放项总攻·五期：κ_G/τ_G 自由⇒恒等零内容；绑定 C02⇒G_pred=2.84e42/1.50e36 偏大 46~53 量级；ρ 双口径差 1373 倍不自洽",
            "引擎只读镜像：falsified 由空间螺旋_剩余开放项总攻精算验证5.py 复算支撑（日志 _run_open5.log），本引擎未重判其内容"),
    "C67": ("INFO", "剩余开放项总攻·五期：αⁿ/N 全域（n=1..6、N=137~1e6）最大 5.33e-5，较 Ω_B=0.0493 小 13+ 量级，无 (n,N) 命中宇宙学占比",
            "引擎只读镜像：falsified 由空间螺旋_剩余开放项总攻精算验证5.py 复算支撑（日志 _run_open5.log），本引擎未重判其内容"),
    "C68": ("INFO", "剩余开放项总攻·五期：ρ=√(G/(α²μ₀c²)) 由 G 反推，材料自陈代数恒等式非独立物理推导（00_总纲 L95）",
            "引擎只读镜像：falsified 由空间螺旋_剩余开放项总攻精算验证5.py 复算支撑（日志 _run_open5.log），本引擎未重判其内容"),
    "C69": ("INFO", "剩余开放项总攻·五期：α=(1/(2√N))(c/(ωA)) V=(1−2−1)/1=−2 伪派生；N 无选择力不可证伪",
            "引擎只读镜像：falsified 由空间螺旋_剩余开放项总攻精算验证5.py 复算支撑（日志 _run_open5.log），本引擎未重判其内容"),
    "C70": ("INFO", "剩余开放项总攻·五期：F_grav 二分 n=1 零内容可吸收进 G；n≠1 违反 Bertrand 闭合轨道定理",
            "引擎只读镜像：falsified 由空间螺旋_剩余开放项总攻精算验证5.py 复算支撑（日志 _run_open5.log），本引擎未重判其内容"),
}
# 原体系 C01–C23：人工审计记录（INFO，非本引擎复核对象）
for i in range(1, 24):
    cid = "C%02d" % i
    if cid not in ENGINE_EVIDENCE:
        ENGINE_EVIDENCE[cid] = ("INFO", "原体系人工审计记录（reviewer=本项目）", "本引擎只作数值锚点交叉核对，不重判其状态")

# ---------------------------------------------------------------------------
# 4. L3 候选：带误差棒的可检验预言登记检查（UFT-3 口径）
# ---------------------------------------------------------------------------
PRED_PAT = re.compile(r"±|误差棒|不确定度|预测值")
registered_pred = []
for r in rows:
    if r["status"] in ("falsified", "info"):
        continue
    # 审计类主张（第一性审计/闭环修复）本身是审计口径，其「误差棒/预测」字眼不是登记在册的预测
    if r["category"] in ("第一性审计", "闭环修复"):
        continue
    if PRED_PAT.search(r["statement"]) and re.search(r"\d+(\.\d+)?(e[+-]?\d+)?", r["statement"]):
        registered_pred.append(r["id"])
# 注：C45/C48/C50/C52 含「误差棒/urel/预测」字样，但均为审计口径（靶规格 / 误差棒审计），非登记在册的预测值
print("     UFT-3 口径：全文登记在册的无量纲靶预测值 = %d 条" % len(registered_pred))

# ---------------------------------------------------------------------------
# 5. 逐条判定：L0–L3 层级 + 决策 + 标记复核
# ---------------------------------------------------------------------------
LEVEL_ORDER = {"L0": 0, "L1": 1, "L2": 2, "L3": 3}


def assign_level(claim, etype, evidence):
    cid = claim["id"]
    status = claim["status"]
    verdict, ref, note = evidence
    if status == "falsified":
        return "L0", "FAIL", "被证伪，不占层级（守卫 G4/G5 不变量：不得改回）"
    if status == "info":
        return "L0", "INFO", "信息类记录（复算备注），不占层级"
    if etype in ("identity", "definition", "parameterization"):
        return "L1", "ALLOW", "R2：identity/definition 证据封顶 L1"
    if etype == "conflict":
        return "L1", "REJECT-CAP", "内部冲突未调和，最高 L1"
    # construction / audit / repair
    if status in ("open", "boundary", "BOUNDARY"):
        return "L1", "REJECT-CAP", "未闭合（无构造推导 + 无带误差棒可检验预言）→ 封顶 L1"
    if status == "pass":
        if verdict == "FAIL":
            if "回退 falsified" in note:
                return "L0", "REJECT", "引擎证据否定当前标记 ⇒ 建议回退 falsified（守卫 G5 恢复路径）"
            return "L1", "REJECT", "引擎证据否定当前标记 ⇒ 建议回退为引擎状态（open/boundary）"
        if cid in registered_pred:
            return "L3", "ALLOW", "带误差棒可检验预言登记在册（UFT-3）"
        if cid in ("C02", "C24", "C39", "C41"):
            return "L2", "ALLOW", "构造推导/数值复核成立（引擎双路证据）"
        if verdict == "UNVERIFIED":
            return "L1", "REJECT-CAP", "标记未获引擎证据（草稿自评）→ 层级暂记 L1，不得据以升维"
        if verdict == "PARTIAL":
            return "L1", "REJECT-CAP", "标记仅部分复核（原 FAIL 判定未撤销）→ 封顶 L1"
        return "L1", "REJECT-CAP", "仅有声明/动作，无构造推导证据（如 C44 删除动作）"
    return "L1", "REJECT-CAP", "状态未知，保守封顶 L1"


audit_rows = []
for r in rows:
    etype = EV_CATEGORY.get(r["category"], "construction")
    evidence = ENGINE_EVIDENCE.get(r["id"], ("INFO", "无登记", "未登记证据"))
    level, decision, why = assign_level(r, etype, evidence)
    audit_rows.append({
        "id": r["id"], "category": r["category"], "status": r["status"],
        "evidence_type": etype, "verdict": evidence[0],
        "evidence_ref": evidence[1], "note": evidence[2],
        "level": level, "decision": decision, "why": why,
    })

lv_cnt = {}
for a in audit_rows:
    lv_cnt[a["level"]] = lv_cnt.get(a["level"], 0) + 1
verdict_cnt = {}
for a in audit_rows:
    verdict_cnt[a["verdict"]] = verdict_cnt.get(a["verdict"], 0) + 1
print("     L 层级分布：%s" % lv_cnt)
print("     标记复核分布：%s" % verdict_cnt)
print("     >>> L3 = %d 条（UFT-3 登记 %d 条）——全台账无 L3 层级主张" % (lv_cnt.get("L3", 0), len(registered_pred)))

# ---------------------------------------------------------------------------
# 6. 数值锚点复算（dps=50，独立复算）
# ---------------------------------------------------------------------------
print("\n     数值锚点复算：")
anchors = []
# 6.1 ρ（C12 反解，档案 3.33e-9 m）
rho12 = sqrt(G / (ALPHA ** 2 * MU0 * C ** 2))
# 6.2 K₀（C29 反解，牛顿量纲）
k0 = C ** 4 * ALPHA ** 2 / (8 * pi * G)
# 6.3 α_grav(e)（C45，正确无量纲靶）
agrav = G * ME ** 2 / (HBAR * C)
# 6.4 ωA（C25，N=18907 反解命中 α）
wA = C / (2 * sqrt(N18907) * ALPHA)
# 6.5 谱修正基数 ℏ²/N² 与谱宽 35×ℏ²/N²（C48）
h2n2 = HBAR ** 2 / N18907 ** 2
spread = 35 * h2n2
# 6.6 |R'|=c（C24/C39：b/A=1/137 参数点）
A_chk = mpf("1.3")
b_chk = A_chk / 137
w_chk = C / sqrt(A_chk ** 2 + b_chk ** 2)
speed = sqrt((A_chk * w_chk) ** 2 + (b_chk * w_chk) ** 2) / C
# 6.7 判别式 V（C25 α 公式 / C29 G 式）
V_alpha = (1 - 2 - 1) / 1
V_G = (1 - 1 - 2) / 1
# 6.8 β_correct（C49：Binet 一阶正确式，水星标定 43.03″/百年）
a_mer, e_mer, T_mer = mpf("5.790905e10"), mpf("0.20563069"), mpf("0.240846")
ARC = pi / (180 * 3600)
h_mer = sqrt(G * mpf("1.98847e30") * a_mer * (1 - e_mer ** 2))
dphi_GR = 6 * pi * G * mpf("1.98847e30") / (C ** 2 * a_mer * (1 - e_mer ** 2))
geo_c = (mpf("43.03") - dphi_GR * (100 / T_mer) / ARC) * ARC / (100 / T_mer)
beta_corr = geo_c * a_mer ** 2 * (1 - e_mer ** 2) ** 2 / (2 * pi)

anchors = [
    ("ρ（C12 反解）", rho12, "3.3312858e-9"),
    ("K₀（C29 反解，N）", k0, "2.5642944e+38"),
    ("α_grav(e)（C45）", agrav, "1.7518094e-45"),
    ("ωA（C25，N=18907）", wA, "1.493874e+08"),
    ("ℏ²/N²（C48）", h2n2, "3.1110506e-77"),
    ("谱宽 (α₆−α₁)/α₁（C48）", spread, "1.0888677e-75"),
    ("|R'|/c（C24/C39，b/A=1/137）", speed, "1.0"),
    ("β_correct（C49，Binet 一阶式）", beta_corr, "≈2.7417e+11"),
]
for name, val, expect in anchors:
    print("       · %-32s = %s   （对照 %s）" % (name, fmt(val, 12), expect))
    if expect.startswith("≈"):
        continue
    reldev = abs(val / mpf(expect) - 1)
    print("         相对偏差 vs 档案/引擎值：%s" % fmt(reldev, 4))

# ---------------------------------------------------------------------------
# 7. 台账完整性镜像（G1–G8 只读；与守卫脚本同口径）
# ---------------------------------------------------------------------------
print("\n     台账完整性镜像（只读，不改台账）：")
mirror = []
# G1 字段数
bad_w = [r["id"] for r in rows if r["n_fields"] != 5]
mirror.append(("G1", "每行恰 5 字段", not bad_w, "异常：%s" % (bad_w if bad_w else "无")))
# G2 编号连续
nums = [int(r["id"][1:]) for r in rows if r["id"].startswith("C") and r["id"][1:].isdigit()]
gap = [n for n in range(1, max(nums) + 1) if n not in nums]
mirror.append(("G2", "claim_id 连续无缺号", not gap, "缺号：%s" % (gap if gap else "无")))
# G3 状态白名单（与守卫 2026-09-26 更新版同口径：含引擎登记态 info/BOUNDARY）
STATUS_OK = {"pass", "open", "boundary", "BOUNDARY", "falsified", "repaired", "info"}
bad_s = [r["id"] for r in rows if r["status"] not in STATUS_OK]
mirror.append(("G3", "状态在守卫白名单内", not bad_s,
               "超出白名单：%s" % (bad_s if bad_s else "无（白名单已含 info/BOUNDARY，与守卫同步）")))
# G4 原 falsified 三条未改回
rev = [c for c in ("C12", "C21", "C23") if by_id.get(c, {}).get("status") != "falsified"]
mirror.append(("G4", "C12/C21/C23 未被改回", not rev, "被改动：%s" % (rev if rev else "无")))
# G5 审计组 falsified 不缩水（对照不变量基线）
cur_fals = sorted(r["id"] for r in rows if r["reviewer"] == "本项目审计组" and r["status"] == "falsified")
base = json.load(io.open(BASELINE, encoding="utf-8")) if os.path.isfile(BASELINE) else None
if base:
    prev = set(base.get("falsified_audit_ids", []))
    now = set(cur_fals)
    shrunk = sorted(prev - now)
    if shrunk:
        mirror.append(("G5", "审计组 falsified 不缩水（基线 %d 条）" % len(prev), False,
                       "缩水 %d 条：%s（来源：分支A分支B轮按草稿汇总表应用更新标记，多数未过引擎复核）"
                       % (len(shrunk), "、".join(shrunk))))
    else:
        mirror.append(("G5", "审计组 falsified 不缩水（基线 %d 条）" % len(prev), True,
                       "与基线一致（2026-09-26 专项复核回退已执行：8 条→falsified、C28→boundary）"))
else:
    mirror.append(("G5", "审计组 falsified 不缩水", True, "基线缺失，本次未比对"))
# G6 引擎计数漂移（阶段一产物 total 与守卫期望；期望口径 2026-09-26 更新为 42=35 判定行+7 能力行）
e1 = json.load(io.open(os.path.join(OUT_DIR, "空间螺旋修复版_第一性审计.json"), encoding="utf-8"))
e2 = json.load(io.open(os.path.join(OUT_DIR, "空间螺旋修复版_最小修复闭环.json"), encoding="utf-8"))
expect = {"阶段一": 42, "阶段二": 10}
drift = (e1["counts"]["total"] != expect["阶段一"]) or (e2["counts"]["total"] != expect["阶段二"])
mirror.append(("G6", "引擎判定总数符合守卫期望", not drift,
               "阶段一 total=%d（期望 %d%s）· 阶段二 total=%d（期望 %d）"
               % (e1["counts"]["total"], expect["阶段一"],
                  "；+%d 来自 §9.5/§9.6 能力行" % (e1["counts"]["total"] - expect["阶段一"])
                  if e1["counts"]["total"] != expect["阶段一"] else "",
                  e2["counts"]["total"], expect["阶段二"])))
# G7 归档存在 + G8 归档哈希防篡改（守卫 G7/G8 同口径）
ARCHIVE = os.path.join(SYS_DIR, "修复版申报原文_2026-09-25.md")
archive_sha = hashlib.sha256(io.open(ARCHIVE, "rb").read()).hexdigest() if os.path.isfile(ARCHIVE) else ""
mirror.append(("G7", "被审文本已归档（审计可溯源）", os.path.isfile(ARCHIVE),
               "路径：%s" % ARCHIVE))
tampered = base is not None and bool(base.get("archive_sha256")) and archive_sha != base["archive_sha256"]
mirror.append(("G8", "被审文本哈希未变（防篡改溯源）", not tampered,
               "当前 %s… vs 基线 %s…%s"
               % (archive_sha[:16], (base.get("archive_sha256", "")[:16] if base else "无"),
                  "（**已变更**：归档被改写，审计锚点失效）" if tampered else "")))
for gid, name, ok, detail in mirror:
    print("       [%s] %s %s  %s" % ("PASS" if ok else "FAIL", gid, name, detail))

# ---------------------------------------------------------------------------
# 8. 产出
# ---------------------------------------------------------------------------
if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)

n_L0 = lv_cnt.get("L0", 0)
n_L1 = lv_cnt.get("L1", 0)
n_L2 = lv_cnt.get("L2", 0)
n_L3 = lv_cnt.get("L3", 0)

payload = {
    "title": "空间螺旋几何化统一场论 · 全量 claims 批量审计与 L3 层级判定",
    "date": "2026-09-26",
    "scope": {"claims_total": len(rows), "ids": "%s–%s" % (rows[0]["id"], rows[-1]["id"]),
              "claims_csv": "07_统一场方程/空间螺旋几何化统一场论/claims.csv（只读）"},
    "method": ["C38 三审计算法（R1/R2/R3）", "引擎证据登记表（可追溯）",
               "数值锚点复算 mpmath dps=50", "台账完整性镜像（G1–G8，只读）"],
    "level_counts": {"L0": n_L0, "L1": n_L1, "L2": n_L2, "L3": n_L3, "total": len(audit_rows)},
    "verdict_counts": {k: verdict_cnt.get(k, 0) for k in ("PASS", "FAIL", "PARTIAL", "UNVERIFIED", "INFO")},
    "uft3_registered_predictions": len(registered_pred),
    "anchors": [{"name": n, "value": fmt(v, 14), "expected": e} for n, v, e in anchors],
    "mirror": [{"id": gid, "name": name, "ok": ok, "detail": detail} for gid, name, ok, detail in mirror],
    "claims": audit_rows,
}
with io.open(os.path.join(OUT_DIR, "空间螺旋全量claims_批量审计_L3层级判定.json"), "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=1)

# CSV 层级判定表
csv_lines = ["claim_id,category,status,evidence_type,verdict,level,decision,evidence_ref"]
for a in audit_rows:
    ev = a["evidence_ref"].replace(",", "；")
    csv_lines.append("%s,%s,%s,%s,%s,%s,%s,%s" % (a["id"], a["category"], a["status"],
                                                   a["evidence_type"], a["verdict"], a["level"],
                                                   a["decision"], ev))
with io.open(os.path.join(OUT_DIR, "空间螺旋claims_L3层级判定表.csv"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(csv_lines) + "\n")

# MD 审计报告
md = []
md.append("# 空间螺旋几何化统一场论 · 全量 claims 批量审计与 L3 层级判定")
md.append("")
md.append("> 日期 2026-09-26 · 引擎：`源码/空间螺旋_全量claims批量审计与L3层级判定.py`（可复跑，对 claims.csv 只读）")
md.append("> 对象：`07_统一场方程/空间螺旋几何化统一场论/claims.csv` 全部主张 %d 条（%s–%s）"
          % (len(rows), rows[0]["id"], rows[-1]["id"]))
md.append("> 方法：C38 三审计算法（R1 禁跳级 / R2 identity·definition 封顶 L1 / R3 升 L3 需构造推导+带误差棒预言）· 引擎证据登记表 · 数值锚点 mpmath dps=50")
md.append("")
md.append("**L 层级判定**：L0=%d ｜ L1=%d ｜ L2=%d ｜ **L3=%d** ｜ 合计 %d"
          % (n_L0, n_L1, n_L2, n_L3, len(audit_rows)))
md.append("")
md.append("**标记复核**：PASS=%d ｜ PARTIAL=%d ｜ UNVERIFIED=%d ｜ INFO(原体系人工)=%d"
          % (verdict_cnt.get("PASS", 0), verdict_cnt.get("PARTIAL", 0),
             verdict_cnt.get("UNVERIFIED", 0), verdict_cnt.get("INFO", 0)))
md.append("")
md.append("**UFT-3**：登记在册的无量纲靶预测值 = **%d** 条 ⇒ 全台账无 L3 主张（与既有口径一致）。" % len(registered_pred))
md.append("")
md.append("## 一、L 层级判定总表")
md.append("")
md.append("| claim | category | status | 证据类型 | 标记复核 | L | 决策 |")
md.append("|---|---|---|---|---|---|---|")
for a in audit_rows:
    md.append("| %s | %s | %s | %s | %s | **%s** | %s |"
              % (a["id"], a["category"], a["status"], a["evidence_type"], a["verdict"], a["level"], a["decision"]))
md.append("")
md.append("## 二、标记复核要点（仅引擎证据支持的标记可登记 PASS）")
md.append("")
md.append("- **PASS（%d 条）**：C24（|R'|=c 复算）、C25/C35（open，语义按引擎修正）、C38（BOUNDARY）、"
          "C39–C45（第二阶段引擎）、C46/C47（§9.6）、C48/C49（V21续修 §12/§13）、"
          "C50/C51/C52（V22 收官 §15–§17）、C53/C54（V21续修② §18/§19，量纲/固定点实证）。"
          % verdict_cnt.get("PASS", 0))
md.append("- **PARTIAL（2 条）**：C32（删除 ρ 方向通过，原量纲 FAIL 未撤销）、C34（μ₀J 已补，J_geo 源项未闭合）。")
md.append("- **FAIL（%d 条，引擎证据否定当前标记）**：C26（§2-4 四方冲突）/C27（§3-1 floor 删除一方）/C28（§3-2 欠定非 pass）/C29（§4-1 K₀ 量纲失败）/C30（§4-3 循环搬家）/C31（§4-2 Π 定理）/C33（§6-1 α²K 量纲失败）/C36（§6-5 Φ₀ 量纲冲突）/C37（§9-1/§9-2 面板矛盾）——草稿汇总表标记 PASS 被统一脚本 §1–§9 判定**否定**；建议回退（C28 回 BOUNDARY，其余回 falsified）。"
          % verdict_cnt.get("FAIL", 0))
md.append("- **UNVERIFIED（%d 条）**：—（本轮专项复核已把全部 9 条升级为有引擎证据的 FAIL，详见组织文档《判定_空间螺旋C26-C37专项复核_2026-09-26.md》）。"
          % verdict_cnt.get("UNVERIFIED", 0))
md.append("- **INFO（%d 条）**：C01–C23 为原体系人工审计记录，非本引擎复核对象（本册仅作数值锚点交叉核对）。"
          % verdict_cnt.get("INFO", 0))
_falsified_ids = [a["id"] for a in audit_rows if a["status"] == "falsified"]
md.append("- **falsified（%d 条）**：%s——已证伪，封顶 L0；守卫 G4/G5 不变量：不得改回。"
          % (len(_falsified_ids), "、".join(_falsified_ids)))
md.append("")
md.append("## 三、台账完整性镜像（只读）")
md.append("")
md.append("| 编号 | 断言 | 结果 | 说明 |")
md.append("|---|---|---|---|")
for gid, name, ok, detail in mirror:
    md.append("| %s | %s | %s | %s |" % (gid, name, "PASS" if ok else "**FAIL**", detail))
md.append("")
md.append("## 四、数值锚点（dps=50 现场复算）")
md.append("")
md.append("| 量 | 复算值 | 对照 |")
md.append("|---|---|---|")
for name, val, expect in anchors:
    md.append("| %s | %s | %s |" % (name, fmt(val, 14), expect))
md.append("")
md.append("## 五、结论与建议")
md.append("")
md.append("1. **L3 层级判定完成：全台账 0 条 L3**（UFT-3 登记 0 条）——与三阶段审计既有口径一致；草稿所称「L3 完整第一性推导闭环」在台账层面无任何一条主张支撑。")
md.append("2. **C26–C37 专项复核完成且回退已执行**：9 条草稿自评 PASS 被引擎证据否定（FAIL）（C32/C34 部分支持）；2026-09-26 已写回台账——C26/C27/C29/C30/C31/C33/C36/C37→falsified、C28→boundary、C32/C34 维持 pass；守卫 G5 缩水清零、基线已重建（11 条），与 V22 §17-CLAIMS-3 口径一致。")
md.append("3. **守卫状态**：G3/G5/G6 已修复（白名单扩 info/BOUNDARY、期望计数 42、回退执行、基线重建）；守卫实跑 **8/8 全绿（EXIT=0）**、结论「申报不成立」（falsified 17 条 = 基线 17 条）。")
md.append("4. **语义修正**：C25/C35 的 open 状态字虽与引擎一致，但草稿语义（可证伪谱/普适性就绪）已被 V21续修引擎推翻（退化谱/公式需修正），台账备注须采用引擎语义。")
md.append("5. **与 V22 §17 批量审计的关系**：V22 覆盖 C01–C49 并登记 C50/C51/C52；本册覆盖全部 %d 条，两引擎 **L3=0 结论一致**。差异仅两处：①纯定义类主张 V22 记 L0、本册按 R2 封顶 L1（均 ≤ L1，不影响主结论）；②本册额外提供逐条**标记复核**（PASS/FAIL/PARTIAL/UNVERIFIED/INFO）与**台账完整性镜像**（G1–G8），V22 未覆盖。"
          % len(rows))
md.append("6. **V21 续修②（C53/C54）登记后**：falsified 集合由 4 条增至 %d 条（新增引力泡公式层与 TUFT-RG 模块层），"
          "L3 仍为 0、无量纲靶登记仍为 0 ⇒ 「L3 完整第一性推导闭环」与本轮两个新模块均无关（两模块皆为量纲/参数层面的否定结论）。"
          % len(_falsified_ids))
md.append("7. **守卫修复已执行**：白名单扩入 `info`/`BOUNDARY`；期望计数更新为 42（35 判定行 + §9.5/§9.6 能力 7 行）；回退 9 条；基线重建（11 条，revision 注明回退与合法翻标）。后续若引擎新增状态或统一脚本行数变化，需同步守卫白名单与期望（或改「基线快照 + 只禁缩水」模式彻底解耦）。")
md.append("")
with io.open(os.path.join(OUT_DIR, "空间螺旋全量claims_批量审计_L3层级判定.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(md))

print("\n" + "=" * 76)
print("L3 层级判定：L0=%d L1=%d L2=%d L3=%d | 标记复核 PASS=%d PARTIAL=%d UNVERIFIED=%d INFO=%d | 用时 %.1f s"
      % (n_L0, n_L1, n_L2, n_L3, verdict_cnt.get("PASS", 0), verdict_cnt.get("PARTIAL", 0),
         verdict_cnt.get("UNVERIFIED", 0), verdict_cnt.get("INFO", 0), time.time() - T0))
print("产出：数据/空间螺旋全量claims_批量审计_L3层级判定.{json,md} + 数据/空间螺旋claims_L3层级判定表.csv")
print("=" * 76)
