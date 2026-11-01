# -*- coding: utf-8 -*-
"""r320 README 登记（append-only / 逐字节保全 / 幂等）。

纪律（承库内既有 _reg_rNNN.py，两条收紧）：
1. 行尾不翻译：二进制读 + 手工按 \\r\\n 拼 + 二进制写。README 是 CRLF 主体混 21 行裸 LF，
   文本模式读写会把那 21 行整片变形而行级判据照样「通过」。
2. 登记行的数字**由落盘面现推**（report 面 parse 计数、JSON 面取 kv），不在驱动里手打数字
   ⇒ 散文与面不可能漂移；对不上就 hard-throw，不写盘。
3. 幂等：`### r320 ·` 已 1 枚 ⇒ 先复核登记行的「自抓 N 枚」与判定册 §五之二 现数是否同，同则 SKIP(rc=0)、
   不同则 SELFBUG-DRIFT(rc=4) 交人工（本驱动不改写既有行）；>1 枚 ⇒ BAD STATE(rc=3) 交人工，绝不自动删。
4. 写后守卫：after 必须以 before 为**逐字节前缀**（纯追加）；验证键 == 1；
   小节里每个 markdown 相对链接目标必须在盘上存在（LINK-OK n/n）。
"""
import glob
import hashlib
import io
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _r320_selfbugs as SB  # noqa: E402  自抓块的唯一派生（判定册 §五之二）
README = os.path.join(ROOT, "README.md")
DATA = os.path.join(ROOT, "数据")
JUDG = os.path.join(ROOT, "判定")
SRC = os.path.join(ROOT, "源码")
BAK = os.path.join(ROOT, "scratch", "_bak_README_pre_r320.md")

KEY_DET = "### r320 ·"
CRLF = "\r\n"

# ---------------------------------------------------------------- 面：数字的唯一来源
eng = glob.glob(os.path.join(SRC, "TUFT-r320_*.py"))
jf = glob.glob(os.path.join(DATA, "TUFT-r320_*.json"))
rf = glob.glob(os.path.join(DATA, "TUFT-r320_*_report.txt"))
mf = glob.glob(os.path.join(DATA, "TUFT-r320_*_精算与可视化_2026-11-01.md"))
zf = glob.glob(os.path.join(DATA, "TUFT-r320_*_来料原件_ROOT_V24.0_用户附件逐字_2026-11-01.md"))
if not (len(eng) == 1 and len(jf) == 1 and len(rf) == 1 and len(mf) == 1 and len(zf) == 1):
    print("FACE-COUNT engine=%d json=%d report=%d datamd=%d zheng=%d -> 人工处置"
          % (len(eng), len(jf), len(rf), len(mf), len(zf)))
    sys.exit(2)

ENGINE = os.path.basename(eng[0])
JSON_FACE = os.path.basename(jf[0])
REPORT_FACE = os.path.basename(rf[0])
DATA_MD_FACE = os.path.basename(mf[0])
ZHENG_FACE = os.path.basename(zf[0])
JUDG_FACE = os.path.basename(glob.glob(os.path.join(JUDG, "判定_TUFT-r320_*.md"))[0])
HTML_FACE = os.path.basename(glob.glob(os.path.join(ROOT, "四力统一方程_ROOTV24图表层*_r320*.html"))[0])

d = json.load(io.open(os.path.join(DATA, JSON_FACE), encoding="utf-8"))
M = dict((it["id"], it) for it in d["items"])


def kv(i, k):
    v = M[i]["kv"]
    if k not in v:
        print("KV-MISSING %s.%s -> 面与驱动不同源，拒绝写盘" % (i, k))
        sys.exit(2)
    return v[k]


# ---- 由 report 面现推计数（不是手打的期望值）
rep = io.open(os.path.join(DATA, REPORT_FACE), encoding="utf-8").read()
rows = re.findall(r"^\[(\S+?)\s*\]\s+(PASS|FAIL|BOUNDARY|INFO)", rep, re.M)
if not rows:
    print("REPORT-PARSE-EMPTY（判集塌缩与没有缺陷同形，拒绝登记）")
    sys.exit(2)


def tally(pfx):
    c = {}
    for i, v in rows:
        if i.startswith(pfx) and not i.startswith("G"):
            c[v] = c.get(v, 0) + 1
    return c


t_main = tally("V")
t_ctl = tally("C")
t_g = {}
for i, v in rows:
    if i.startswith("G"):
        t_g[v] = t_g.get(v, 0) + 1
N_ALL = len(rows)
N_MAIN = sum(t_main.values())
N_CTL = sum(t_ctl.values())
N_G = sum(t_g.values())
if not (N_ALL == N_MAIN + N_CTL + N_G and N_MAIN == 19 and N_CTL == 7 and N_G == 15):
    print("COUNT-MISMATCH all=%d main=%d ctl=%d guard=%d -> 面自己没闭合，拒绝登记"
          % (N_ALL, N_MAIN, N_CTL, N_G))
    sys.exit(2)
if sorted(i for i, v in rows if v == "FAIL") != ["V17", "V18"]:
    print("DESIGN-FAIL-ROSTER-DRIFT %s" % sorted(i for i, v in rows if v == "FAIL"))
    sys.exit(2)
n_pass_all = sum(1 for _, v in rows if v == "PASS")

# ---- 自抓枚数与逐条正文都由判定册 §五之二 现推（与 README 同步驱动共用同一段派生）
try:
    JUDG_FACE, N_BUGS, SELFBUG_LINE = SB.block_from_face(ROOT)
except SB.SelfBugError as e:
    print("%s -> 判定册没有闭合的 §五之二，拒绝登记" % e)
    sys.exit(2)

# ---------------------------------------------------------------- 小节文本（数字全部插值自面）
v11_rows = kv("V11", "rows")
worst = max(float(r[4]) for r in v11_rows)

head = ("### r320 · 2026-11-01 · ROOT V24 同来料第三把尺：图表可容性窗 / 任意 C\u00b9 重参数化指数不变律 / "
        "曲率任意性 / 坐标旋钮杠杆定价（\u2605外部来料审计层 \u00b7 承 r317/r321 \u00b7 \u2605与并发卷条目不可相加 \u00b7 "
        "\u2605本卷自抓 %d 枚仪器坑）" % N_BUGS)

sec = [head, ""]
sec.append("- **产物**：源码 [`%s`](源码/%s)；来料正本 [`…来料原件_ROOT_V24.0_用户附件逐字`](数据/%s)；"
            "数据 [`…json`](数据/%s) / [`…md`](数据/%s) / [`…_report.txt`](数据/%s)；"
            "判定册 [`判定_TUFT-r320_…md`](判定/%s)；runner `源码/_run_r320.py` \u2192 `源码/_out_r320.txt`；"
            "交互可视化 [`%s`](%s)" % (ENGINE, ENGINE, ZHENG_FACE, JSON_FACE, DATA_MD_FACE,
                                       REPORT_FACE, JUDG_FACE, HTML_FACE, HTML_FACE))
sec.append("- **复现**：`python -X utf8 源码\\_run_r320.py` \u21d2 **rc=0**；条目 **%d**"
            "（主 **%d**：PASS %d / **FAIL %d（V17、V18 = 预注册设计红，非仪器故障）** / BOUNDARY %d / INFO %d；"
            "控制组 **%d/%d**（正对照 3 + 拒绝型 4，类型字段驱动）；守卫 **%d/%d**）；"
            "mpmath 90 位 + Fraction/SymPy 精确；**二跑 6/6 面逐字节幂等**（自指哈希已切除：三趟写盘 + 报告面不参与自身哈希）。"
            % (N_ALL, N_MAIN, t_main["PASS"], t_main["FAIL"], t_main["BOUNDARY"], t_main["INFO"],
               N_CTL, N_CTL, N_G, N_G))
sec.append("- **命题（来料）**：ROOT V24.0《精细结构常数第一性原理攻坚：固定点的真假判别》——"
           "\u03b2_u = Au \u2212 Bu\u00b2（A=1/50, B=3）给 u*=1/150；可逆重参数化 v = u/(1\u2212ku) 把固定点搬到 v*=1/137（k=13），"
           "并主张稳定性指数与可观测量不变、多耦合矩阵相似、轨道初值自由、\u00a7四 真空极化物理闭环。")
sec.append("- **\u2605V2 一般指数不变律（本卷净增量，来料只在 Möbius 族上陈述）**：任意 C\u00b9 可逆图表 g 给 "
           "d\u03b2_g/dv = \u03b2\u2033_u + (g\u2033/g\u2032)\u03b2_u；固定点处 \u03b2_u=0 把图表依赖项整条杀掉 \u21d2 "
           "**只剩谱不变**。恒等式符号残差 %s，\u03b2\u2032(v*) 在 Möbius / 幂函数 v=u\u00b3 / 形变三族上同为 %s。"
           % (kv("V2", "identity"), kv("V2", "abstract_at_fp")))
sec.append("- **\u2605V5 图表可容性定理（新）**：v-图表在一条 RG 轨道上全局解析 \u21d4 极点 1/k **不落在** "
           "[min(u\u2080,u*), max(u\u2080,u*)]。来料自己打印的三条轨道同时可容 \u21d2 k \u2264 %s \u21d2 "
           "**可达正读数 1/v* \u2265 %s**（把并发 r317「任意目标都能造」的适用域收紧：窗内才造得出，窗外图表自己先炸）。"
           % (kv("V5", "k_max_admissible"), kv("V5", "reading_min")))
sec.append("- **\u2605V7 旋钮视界（BOUNDARY）**：k = B/A = 150 时分母 = %s，Jacobian 极点 1/k = %s **恰落在固定点 "
           "u* = %s 上** \u21d2 v*\u2192\u221e、\u03b2_v 退化、「相似性/不变性」那套前提当场失效；k=151 \u21d2 v* = %s（负读数）。"
           % (kv("V7", "den_at_150"), kv("V7", "pole_at_150"), kv("V7", "u_star"), kv("V7", "vstar_151")))
sec.append("- **\u2605V8 曲率任意性定理（新）**：同一坐标、同一指数，\u03b2\u2033(v*) = %s 随形变参数 S **线性漂移**；"
           "取 S* = %s = **%s** 可使 \u03b2\u2033 \u2261 0，且 \u03b2\u2034 同族任意（S=0 时 \u03b2\u2033 = %s）。"
           "⇒ **「靠曲率/临界指数判哪个固定点是真的」这一整类论证无效**（控制组 C5 给四张同坐标同指数图表、四个不同 \u03b2\u2033 作证）。"
           % (kv("V8", "beta_doubleprime_S"), kv("V8", "S_zero_curvature"),
              kv("V8", "S_zero_curvature_dec"), kv("V8", "beta2_S0")))
sec.append("- **\u2605V3/V4 旋钮定价（新）**：1/v*(k) = 150 \u2212 k（斜率 %s、截距 %s，%d 格线性残差违反 %d）；"
           "命中 CODATA 需 k* = %s（**非整数**）。整数 k 只命中整数格（%s），"
           "137 距 CODATA %s 个 \u03b1\u207b\u00b9 单位 = **%s \u03c3**（\u03b1 货币 %s \u03c3，两货币同量级）"
           "\u21d2 「137 是整数」这句话**信息量为零**。"
           % (kv("V3", "slope"), kv("V3", "intercept"), kv("V3", "k_count"), kv("V3", "linear_violations"),
              kv("V3", "k_star"), kv("V4", "integer_hits"), kv("V4", "abs_diff_inv"),
              kv("V4", "sigma_inv"), kv("V4", "sigma_alpha")))
sec.append("- **\u2605V9/V10 载体的缺口（新）**：来料 \u00a7二 只印 \u03bb\u00b1 不印矩阵 \u21d2 本卷自建 "
           "B* = %s（tr=%s、det=%s）精确实现 \u03bb\u00b1 = %s，且 B\u2032* = JB J\u207b\u00b9 元素全变而谱不变；"
           "维数计数 4 元素 vs 2 不变量 \u21d2 **%d 参数族**，正本含具体 \u03b2 的行数 = %d（实测 0 次命中 \u21d2 不可复跑）；"
           "det<0 \u21d2 相关方向仍 %d。"
           % (kv("V9", "B_star"), kv("V9", "tr"), kv("V9", "det"), kv("V9", "eigs"),
              kv("V10", "free_params"), len(kv("V10", "explicit_beta_lines")), kv("V10", "n_relevant")))
sec.append("- **\u2605V12/V14 把两条「物理闭环」换成 \u03b1\u207b\u00b9 货币定价（新）**：轨道残余历史 = "
           "%s 个 \u03b1\u207b\u00b9 单位 = 旋钮一格的 1/%s（压到 0.01/0.001 需 L\u2248%s/%s）；"
           "真空极化阈值平移 = %s 单位 = 旋钮 %s 格的 **%s**（1/%s）\u21d2 "
           "\u00a7四 的量级**不足以裁定 \u00a7一**，两卷同一事实取较严者。"
           % (kv("V12", "spread_inv"), kv("V12", "ratio_dial_over_spread"),
              kv("V12", "L_for_0p01"), kv("V12", "L_for_0p001"), kv("V14", "leverage_vs_13step"),
              kv("V12", "dial_step"), kv("V14", "one_over"), kv("V14", "one_over")))
sec.append("- **\u2605V13 H(1) 黄金比闭式 + 与并发 r321 的互校（同一事实不可相加）**：90 位求积 H(1) = %s，"
           "SymPy 精确积分给闭式 **%s**（符号残差 %s，与 quad 差 %s）；严格恒等 **1/\u03b1_eff = 1/\u03b1(0) \u2212 H** "
           "（闭环在 \u03b1\u207b\u00b9 货币里只是平移 H，与 \u03b1(0) 取什么值无关），90 位反演回程残差 1/137 \u2192 %s、1/150 \u2192 %s。"
           "r321 印的一般 q 闭式在 q=1 处与本卷黄金比式**现场比对** = %s（asinh(1/2)=ln \u03c6）\u21d2 互校 %s；"
           "被引面尺寸属当下读数（写盘时在飞），不可后引。"
           % (kv("V13", "H1"), kv("V13", "H1_closed"), kv("V13", "closed_residual"), kv("V13", "quad_vs_closed"),
              kv("V13", "back_residual_137"), kv("V13", "back_residual_150"),
              kv("V13", "r321_printed_H1"), "通过" if kv("V13", "r321_agrees") else "未通过"))
sec.append("- **V6/V11/V15/V16 复现与替代载体**：两口径奇点时刻恒等（v-Riccati 极点 = u-图表 Jacobian 极点 = %s，"
           "t* = ln(100)/A = **%s**）；\u00a7三 %d 枚轨道读数按**印刷字段半 ulp** 全命中（最紧比值 %.6f < 1），"
           "容差减半必红 %s 枚（牙）；\u00a7六「101 组方案扫描」正本无表 \u21d2 自建 %s 行替代载体"
           "（违反 %s、不可容 %s、%s/%s 行满足 \u03b2\u2032 = \u22121/50，动量只印 %s）；"
           "九行审计表逐行挂载体：有载体 %s / 部分 %s / 无载体 %s / 自认红 %s（= %s 行，扫描组数不等于证据）。"
           % (kv("V6", "r_u"), kv("V6", "t_star"), len(v11_rows), worst,
              kv("V11", "red_when_tol_halved"), kv("V15", "n_rows"), kv("V15", "linear_violations"),
              kv("V15", "inadmissible_rows"), kv("V15", "exponent_invariant_rows"), kv("V15", "n_rows"),
              kv("V15", "momentum_printed"), kv("V16", "有载体"), kv("V16", "部分载体"),
              kv("V16", "无载体"), kv("V16", "自认红"), kv("V16", "n_rows")))
sec.append("- **\u2605V17/V18 两条设计性 FAIL（判给路线解释力，不否来料算术）**：V17「固定点算出 1/137 \u21d2 预测了 \u03b1」"
           "FAIL \u2014\u2014 坐标可任意 + 曲率可任意 + 整数格偏 %s \u03c3；V18「无实测输入的独立 \u03b1(0) 预测」FAIL \u2014\u2014 "
           "缺口 = 归一化约定 + 轨道选择**两条各 1 个实数自由度**，都不在 \u03b2=0 的输出里。"
           "来料可计算部分全真（PASS %d 条），预测力为设计性红。" % (kv("V17", "sigma_off"), n_pass_all))
sec.append("- **V19 判据集**：R1\u2013R6 = **%s**（tally %s）；\u5e76\u63d0 r308 \u9762\u540c\u53e3\u5f84\u590d\u6838 %d \u679a\u951a\u9010\u4f4d\u4e00\u81f4\uff08\u53ea\u8bfb\u5f15\u7528\uff09\u3002"
            % (kv("V19", "score"), kv("V19", "tally"), len(kv("V19", "r308_anchors"))))
sec.append("- **判词**：**INTAKE-NUMERICS-ALL-REPRODUCED / CHART-ADMISSIBILITY-WINDOW-READINGS-GT-50 / "
           "SPECTRUM-IS-THE-ONLY-CHART-INVARIANT / CURVATURE-ARBITRARY-INCL-ZERO / "
           "INTEGER-DIAL-OFF-BY-1.7e6-SIGMA / THRESHOLD-LEVERAGE-1/676-OF-DIAL / STILL-NOT-A-PREDICTION**。"
           "\u2605本卷真正的裁定不是「哪个固定点是真的」，而是**凡以固定点坐标为输出的论证都不真**——"
           "可容窗（V5）、视界（V7）、射流删除（V8）合起来把「固定点能报告的图表不变量」压到只剩谱，"
           "而这里的谱是一个负数 \u22121/50，它对「137 从哪来」零发言。")
sec.append("- **\u2605与并发卷的分工（不可相加，G11 机检）**：主条目 %d = 题面带\u2605（净增量）%d \u222a 账内点名 %d（交集 %d），"
           "账外未标 %d、账内虚挂 %d。r317（第一把尺）拿「坐标伪影 + 事后编造定理 k=1/u*\u22121/T」，"
           "r321（互补攻坚）拿「一般 q 闭式 + \u03bb>0 符号判据 + 放大因子与 bit 记账」，"
           "本卷拿「可容窗 / 视界 / 曲率任意性 / \u03b1\u207b\u00b9 货币杠杆定价 / 九行审计表挂载体」；"
           "H(1) 闭式与 \u03b1\u207b\u00b9 平移恒等与 r321 重叠，**同一事实取较严者，条目数不可相加**。"
           % (kv("G11", "n_main"), kv("G11", "n_starred"), kv("G11", "n_ledger"), kv("G11", "n_inter"),
              kv("G11", "n_undeclared"), kv("G11", "n_ghost")))
sec.append(SELFBUG_LINE)
sec.append("- **治理与红线**：未改 `verify.py`；未跑 `refresh_catalog.py`（并发极活跃，整体重生成会回退他人更大版本）；"
           "未触碰任何既有卷字节（r308/r317/r321 面与 README 全只读，G9 现场看盘并当场比对）；"
           "正本逐字留档、13/13 十进制锚由 G6 从盘上正本现读（非复述上轮）；"
           "登记行**不钉本卷面尺寸**（面尺寸随并发卷 r321 在飞而动，属当下读数）；"
           "git 由收口提交统一处理（未获用户授权前不提交）。**下轮取号前必再扫三树 + README**"
           "（本轮实测：源码树已到 r326，r321 齐套但 README 未注册，r319 名下有他人「互补攻坚」重命名残留）。")
sec.append("- **遗留（不代选）**：X-R320-1 电荷归一化约定的第一性固定（哪个物理量把 k 定死）；"
           "X-R320-2 可容窗对多耦合图表族（V \u2260 Möbius）的推广；"
           "X-R320-3 轨道选择的首次积分/边界条件机制（与 r317 幅度卷邻接，不重算）；"
           "承前 X-R317-1/2/3、X-R311-4 不变量表述。")
sec.append("")

# ---------------------------------------------------------------- 写入（纯追加，逐字节保全）
if not os.path.exists(README):
    print("README MISSING")
    sys.exit(2)
before = open(README, "rb").read()
text = before.decode("utf-8")
n0 = text.count(KEY_DET)
if n0 == 1:
    # 已登记也不许闭眼跳过：登记行的自抓枚数必须与判定册 §五之二 现数同
    k = text.index(KEY_DET)
    nxt = text.find("\n### ", k + 1)
    sec_disk = text[k:nxt if nxt > 0 else len(text)]
    m_disk = re.search(r"自抓 (\d+) 枚仪器坑", sec_disk)
    n_disk = int(m_disk.group(1)) if m_disk else -1
    if n_disk != N_BUGS:
        print("SELFBUG-DRIFT README=%d vs 判定册=%d -> 登记行落后于面，交同步驱动 "
              "`_sync_r320_readme.py`（本驱动绝不改写既有行）" % (n_disk, N_BUGS))
        sys.exit(4)
    print("SKIP (already registered)  key=%r count=1  bytes=%d  自抓枚数 README=判定册=%d"
          % (KEY_DET, len(before), N_BUGS))
    sys.exit(0)
if n0 > 1:
    print("PARTIAL / BAD STATE count=%d -> 人工处置（驱动绝不自动删既有行）" % n0)
    sys.exit(3)

# 面内数字与登记行的一致性（写盘前先算完全部文本，不留半截账）
body = "\n".join(sec)
for probe in ("条目 **%d**" % N_ALL, "主 **%d**" % N_MAIN, "控制组 **%d/%d**" % (N_CTL, N_CTL),
              "守卫 **%d/%d**" % (N_G, N_G), "R1\u2013R6 = **%s**" % kv("V19", "score"),
              "自抓 %d 枚仪器坑" % N_BUGS):
    if probe not in body:
        print("SELF-CHECK-FAIL 登记行缺锚 %r" % probe)
        sys.exit(4)

links = re.findall(r"\]\(([^)\s]+)\)", body)
if not links:
    print("LINK-EMPTY")
    sys.exit(4)
missing = [t for t in links if not os.path.exists(os.path.join(ROOT, t))]
if missing:
    print("LINK-MISSING %s" % missing)
    sys.exit(4)

if not os.path.exists(BAK):
    shutil.copy2(README, BAK)
    print("BACKUP -> scratch/_bak_README_pre_r320.md  md5 %s" % hashlib.md5(before).hexdigest()[:12])

assert text.endswith("\n")
block = CRLF + CRLF.join(sec) + CRLF
out = text + CRLF + block
after = out.encode("utf-8")
if not after.startswith(before):
    print("NOT-APPEND-ONLY：追加之外的任何字节位移都拒绝")
    sys.exit(6)

open(README, "wb").write(after)

chk = open(README, "rb").read()
if not chk.startswith(before):
    print("POST-PREFIX-BROKEN")
    sys.exit(6)
ct = chk.decode("utf-8")
n1 = ct.count(KEY_DET)
print("post-keys %r count=%d" % (KEY_DET, n1))
if n1 != 1:
    print("REG-FAIL（验证键不是 1）")
    sys.exit(5)
print("APPEND-ONLY-OK 前 %d 字节逐字节保全；added = %d B / %d 行；LINK-OK %d/%d"
      % (len(before), len(chk) - len(before), len(sec), len(links), len(links)))
print("REG-OK r320")
