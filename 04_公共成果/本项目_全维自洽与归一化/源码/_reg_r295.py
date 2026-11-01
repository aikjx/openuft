# -*- coding: utf-8 -*-
"""r295 README 幂等登记（四处：源码树 / 判定树 / compact 增量 / detail 增量节）

纪律（见 MEMORY.md）：
  * 幂等键必须带**位置前缀**，裸 "TUFT-rN_" 会误抓 detail 内多个链接
  * 先判存在再分流，两步不合并
  * 读-改-写单窗口；写后从磁盘读回逐处计数 = 1
  * diff 零删除守卫（delete + replace 行数必须为 0）；末行无尾换行属伪删除，需按内容复核
"""
import difflib
import io
import os
import sys

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(ROOT, "README.md")
BAK = os.path.join(ROOT, "_bak_README_pre_r295.md")

SRC_NAME = ("TUFT-r295_三代多重度的通量指标定理_"
            "半单Cartan零迹与U1比值阻碍及三条逃逸路线定价_精算与可视化_2026-11-01.py")
BASE_NAME = ("TUFT-r295_三代多重度的通量指标定理_"
             "半单Cartan零迹与U1比值阻碍及三条逃逸路线定价_2026-11-01")
JUD_NAME = ("判定_TUFT-r295_三代多重度的通量指标定理_"
            "半单Cartan零迹与U1比值阻碍及三条逃逸路线定价_2026-11-01.md")
HTML_NAME = "统一场论_三代多重度通量指标定理_可视化_2026-11-01.html"

SRC_LINE = (
    "│   ├── " + SRC_NAME + "  # 新增（**r295 · 2026-11-01**）："
    "**三代多重度的通量指标定理（★自审层 · 攻 r294 自留 OPEN X-R294-1）**"
    "（主条目 **43**：PASS 30 / FAIL 0 / INFO 13；**控制组 7/7**、**守卫 11/11**、退出码 0）。"
    "★**不引外部来料**——攻靶是本库上一卷 r294 的 `NO-GO-STRONG` 与它自己留的 OPEN。"
    "★★**Theorem A（半单零迹）**：任何半单李代数任何不可约表示，权重集在 Weyl 群下成对抵消 ⇒ "
    "`tr_R(H) = 0` ⇒ **沿 Cartan 子代数的通量给出零指标，非零指标必须由 U(1) 提供**；"
    "机检 SU(2)×3 / SU(3)×3 / SU(4)×1 / SU(5)×4 共 **11 个表示全部零向量（11/11）**；"
    "★**CTL7 负对照**：从 SU(5) 基本表示删去 1 个权 ⇒ 权重和立刻非零，证明该零是真检测而非构造空转。"
    "★★**Theorem B（U(1) 比值阻碍）**：SM 兼容通量只剩 Y 方向，`tr_R(Y) = (1, 2, −1, −1, −1)` ⇒ "
    "**多重度比恒为 1:2:1:1:1，与通量大小 M 无关** ⇒ **任何单一 U(1)_Y 通量都给不出等代数三代**；"
    "M=3 得 `(3, 6, −3, −3, −3)`（u_R 是别人 2 倍）；反解 `n_Q = n_u` 的线性式系数 `1−2 = −1 ≠ 0` ⇒ 唯一解 **M = 0**（零通量）；"
    "`Σ_R tr_R(Y) = 0` 与 SM 规范反常抵消一致（**未调参即命中的外部正对照**）。"
    "★★**Theorem C（换 U(1) 也不行）**：`aY + b(B−L)` 下令 `n_Q = n_u` 得 **b = a**，代入后 "
    "`(n_Q,n_u,n_d,n_L,n_e) = (3a,3a,0,−3a,−2a)` ⇒ **d_R 恒为 0** ⇒ 等代数要求 `3a = 0` ⇒ **a = b = 0**；"
    "**C05b**：d_R 沿纯 Y = **−1**、沿纯 B−L = **+1**，只在 b=a 方向相加为零 ⇒ **消掉 d_R 的代价正是失去 d_R**。"
    "★**一般性**：任何保持 G_SM 的 U(1) 必在 `Cartan(SU3)⊕Cartan(SU2)⊕Y` 内，前三个分量由 Theorem A 归零 ⇒ Theorem B 即全部情形。"
    "★**四条逃逸定价**：**E1 非交换通量** ⇒ SM 被显式破缺（通量是拓扑量、不可局域关闭）；"
    "**E2 平坦/'t Hooft** ⇒ 零曲率给零指标，Z_N 分数通量支**不判决**（记 OPEN X-R295-1）；"
    "**E3 CY3** ⇒ `|Δ|=|h¹¹−h²¹|=3` 的配对在 h¹¹∈[1,20]、h²¹∈[0,20] 内有 **35** 个 ⇒ 3 是**选择不是预言**；"
    "**E4 T⁶/Z₃** ⇒ 固定点 **3³ = 27**，可给 3 代。**E3/E4 均需 6 维额外空间，而 ROOT 设定是 2 维 ⇒ 换理论而非打补丁**。"
    "★**定价**：4 槽（保 SM / 等三代 / 无景观 / 只加 2 维）2^4=16 ⇒ **严格档 SURVIVE 0**、**宽松档 2**"
    "（`{S1,S3,S4}` 由 T² 满足但不给三代；`{S2,S3,S4}` 由 E1 满足但破缺 SM）⇒ 按纪律「宽松档 > 0 ⇒ 不占度」"
    "**不占度数链，候选 37 度，链仍止 r264:36**。"
    "★**与 r294 的定位**：其结论是「dim(R) | N_gen」（整数整除，可被非整数电荷/分数通量绕过）；本卷是「比值 1:2:1:1:1」"
    "（**不依赖量子化，绕不过去**）；且本卷证明 r294 的 `Q ∝ I` 前提**不必要** ⇒ **不否证 r294，而是加强它**，两卷不可相加。"
    "★**判定纪律（本卷自我约束）**：**只有真正算出数的条目才给 PASS/FAIL，纯陈述一律 INFO** —— "
    "初稿曾把 A 组 act 写成恒 0 造成 12 条假 PASS，已改为「权重和非零分量个数」实测，**13 条降级为 INFO**（PASS 30 条全部出自算术或枚举）。"
)

JUD_LINE = (
    "├── " + JUD_NAME + "  # 新增（**r295 · 2026-11-01**）："
    "三代多重度通量指标定理判定册（★自审层）—— §判决主文（r294 的 no-go 成立且更强）· "
    "§Theorem A 为何是关键一步（前提变少、结论变强）· §Theorem B 的三种读法（谱型 / 反解 / 归一化不变量）· "
    "§Theorem C 换 U(1) 的失败点（消掉 d_R 的代价）· §四条逃逸的判决与定价 · §定价（严格 0 / 宽松 2 ⇒ 候选 37、链止 r264:36）· "
    "§本卷判定纪律（13 条降级 INFO 的自我约束）· §诚实边界 6 条 · §与既有卷关系（r294 / r292 / r293 / r267 / r264 / r270）· "
    "§遗留 OPEN（X-R295-1 分数通量谱型 / X-R295-2 多 U(1) 独立通量 / X-R295-3 CY3 上重写 α 公式）· §最终一句。"
)

COMPACT = (
    "- **r295（2026-11-01）· 三代多重度的通量指标定理：半单 Cartan 零迹、U(1) 比值阻碍与四条逃逸路线定价（★自审层 · 攻 r294 自留 OPEN X-R294-1）**："
    "**不引外部来料**，攻本库上一卷自己下的 `NO-GO-STRONG`。条目 **43**（PASS 30 / FAIL 0 / INFO 13），控制组 **7/7**，守卫 **11/11**，rc=0。"
    "★★**Theorem A**：半单代数任何不可约表示的权重和在 Weyl 群下成对抵消 ⇒ `tr_R(H)=0` ⇒ **非零指标必须由 U(1) 提供**；"
    "机检 11 个表示（SU2/SU3/SU4/SU5）全零，**CTL7 负对照**（删 1 权即非零）证明非空转。"
    "★★**Theorem B**：`tr_R(Y) = (1,2,−1,−1,−1)` ⇒ **多重度比恒 1:2:1:1:1，与 M 无关** ⇒ 任何单一 U(1)_Y 通量都给不出等代数三代；"
    "M=3 得 `(3,6,−3,−3,−3)`，反解 `n_Q=n_u` 唯一解 **M=0**。"
    "★★**Theorem C**：`aY+b(B−L)` 令 `n_Q=n_u` 得 **b=a**，代入后 **d_R 恒 0** ⇒ 等代数要求 **a=b=0**；**消掉 d_R 的代价正是失去 d_R**。"
    "★**逃逸**：E1 非交换（破缺 SM）/ E2 't Hooft（**不判决，OPEN**）/ E3 CY3（`|Δ|=3` 配对 **35** 个 ⇒ 3 是选择非预言）/ E4 T⁶/Z₃（固定点 **27**）；**E3/E4 均需 6 维，ROOT 只有 2 维 ⇒ 换理论**。"
    "★定价 2^4=16 ⇒ 严格 **0** / 宽松 **2** ⇒ **不占度，候选 37，链仍止 r264:36**。"
    "★与 r294：整除型 → **比值型**（不依赖量子化），且证明其 `Q∝I` 前提不必要 ⇒ **加强而非推翻**，两卷不可相加。"
    "★**新纪律**：只有算出数的条目才给 PASS，纯陈述一律 INFO（初稿 12 条假 PASS 已修，13 条降级）。"
    "**下轮从 r296 复查起（并行链活跃，取号前必扫）**。"
)

DETAIL = (
    "\n\n### r295 · 2026-11-01 · 三代多重度的通量指标定理（★自审层 · 攻 r294 自留 OPEN）\n"
    "\n"
    "- **产物**：源码 [`TUFT-r295_…py`](源码/" + SRC_NAME + ")；"
    "数据 [`…json`](数据/" + BASE_NAME + ".json) / "
    "[`…md`](数据/" + BASE_NAME + ".md) / "
    "[`…_report.txt`](数据/" + BASE_NAME + "_report.txt)；"
    "判定册 [`判定_TUFT-r295_…md`](判定/" + JUD_NAME + ")；"
    "runner `源码/_run_r295.py` → `源码/_out_r295.txt`；"
    "交互可视化 [`统一场论_三代多重度通量指标定理_可视化_2026-11-01.html`](" + HTML_NAME + ")\n"
    "- **复现**：`python -X utf8 源码\\_run_r295.py` ⇒ **rc=0**，条目 **43**（**PASS 30 / FAIL 0 / INFO 13**），"
    "**控制组 7/7**，**守卫 11/11**。\n"
    "- **为什么先攻自己**：r294 判 ROOT V15 主线 `NO-GO-STRONG`，并留 OPEN `X-R294-1`（非阿贝尔/每分量独立通量能否救活 3 代）。"
    "**攻自己刚下的刀，优先级高于再去砍别人。** 本卷只做一件事：把 r294 的隐含前提摊开，看这个 no-go 有多硬。\n"
    "- **★Theorem A（半单 Cartan 零迹）**：r294 的 `index = q_R·dim(R)·M` 隐含前提是 **Q 在每个不可约表示上 ∝ 单位阵**。"
    "本卷发现该前提**不必要**：任何半单代数任何不可约表示，权集在 Weyl 群下不变、Weyl 反射把 w 送到 −w，每条轨道成对抵消 ⇒ "
    "`tr_R(H) = 0` ⇒ **沿 Cartan 子代数的通量指标恒为 0，非零指标必须由 U(1) 提供**。"
    "机检 **11 个表示全零**（SU(2) 基本/伴随/dim4、SU(3) 3/3̄/8、SU(4) 4、SU(5) 5/5̄/10/24）。"
    "★**CTL7 负对照**：从 SU(5) 基本表示**删去 1 个权**，权重和立刻非零 ⇒ **这个零是真算出来的，不是构造上写死的**。\n"
    "- **★Theorem B（U(1) 比值阻碍）**：SM 的 Cartan 子代数是 `Cartan(SU3)₂ ⊕ Cartan(SU2)₁ ⊕ Y`（rank 4），前三个分量由 Theorem A 归零 ⇒ 只剩 Y。"
    "`tr_R(Y) = (1, 2, −1, −1, −1)`（Q_L / u_R / d_R / L_L / e_R），且 `Σ_R tr_R(Y) = 0` "
    "**与 SM 一代规范反常抵消一致、未调参即命中**（外部正对照）。⇒ **多重度比恒为 1:2:1:1:1，与 M 无关**。"
    "M=3 时 `|n_R| = (3,6,3,3,3)`——u_R 拿 6 份；反解 `n_Q = n_u` 的线性式系数 `1−2 = −1 ≠ 0` ⇒ **唯一解 M = 0（零通量 = 无紧致化效应）**。"
    "★**归一化无关**（CTL3：Y→(7/3)Y 后比值仍为 2）⇒ 阻碍不依赖超荷定义约定。\n"
    "- **★Theorem C（换 U(1) 也不行）**：r294 档 B 设想过「用独立 U(1)_F 配整数电荷 q_R」。本卷用**物理的** B−L 做一般线性组合："
    "`aY + b(B−L)`，令 `n_Q = n_u` ⇒ 系数 `(−1, +1)` ⇒ **b = a**；代入后 `(3a, 3a, 0, −3a, −2a)` ⇒ **d_R 恒为 0** ⇒ "
    "要 `n_d = n_Q` 必须 `3a = 0` ⇒ **a = b = 0**。★**C05b 是关键机检**：d_R 沿纯 Y = **−1**、沿纯 B−L = **+1**，"
    "只在 b=a 方向上相加为零 ⇒ **消掉 d_R 的代价，恰恰就是失去 d_R**。"
    "★**一般性**：任何保持 G_SM 的 U(1) 必落在 `Cartan(SU3) ⊕ Cartan(SU2) ⊕ Y` 内，前三个由 Theorem A 归零 ⇒ **Theorem B 即全部情形**，不必再枚举。\n"
    "- **四条逃逸的判决**：**E1 非交换通量**（`[F,G_SM] ≠ 0` ⇒ SM 在紧致化尺度被显式破缺；通量是拓扑量、不可局域关闭）；"
    "**E2 平坦 / 't Hooft**（零曲率 ⇒ `∫tr_R F = 0` ⇒ 零模数 0；Z_N 分数通量支与 dim(R) 不成比例，**本卷不判决**，记 `X-R295-1`）；"
    "**E3 CY3**（代数 = `|χ|/2 = |h¹¹−h²¹|`，`|Δ|=3` 的配对在 h¹¹∈[1,20]、h²¹∈[0,20] 内有 **35** 个 ⇒ **3 是选择不是预言**）；"
    "**E4 T⁶/Z₃**（固定点 **3³ = 27**，配 Wilson 线可给 3 代）。"
    "★**两条致命代价**：E3/E4 **均需 6 维额外空间**，而 ROOT 自 V13 起设定是 **2 维**（R 为唯一紧致半径）⇒ **换一套理论，不是修补原方案**；"
    "且换过去之后 ROOT 的 α 公式、快子判据、真空能估计全部不再适用。\n"
    "- **定价**：4 槽（S1 保 SM / S2 等代数三代 / S3 无景观挑选 / S4 额外维 ≤ 2）2^4 = **16** 个子集全查 ⇒ "
    "**严格档 SURVIVE = 0**（无路线四槽全满足）、**宽松档 = 2**（`{S1,S3,S4}` 由 T² 满足但不给三代；`{S2,S3,S4}` 由 E1 满足但破缺 SM）⇒ "
    "按既有纪律「**宽松档 > 0 ⇒ 不占度**」⇒ **不占「修复即自杀」度数链，候选 37 度，链仍止 r264:36**。\n"
    "- **★与 r294 的定位（重要）**：r294 的结论形式是「`dim(R) | N_gen`」（**整数整除**，理论上可被非整数电荷或分数通量绕过）；"
    "本卷是「**多重度比 1:2:1:1:1**」（**连续量的比值**，不依赖任何量子化约定，绕不过去）。"
    "且本卷证明 r294 的 `Q ∝ I` 前提**不必要** ⇒ **不否证 r294，其 NO-GO 成立且被加强**；两卷是同一命题的两轮攻防，**不可相加**。\n"
    "- **★本卷判定纪律（自我约束，如实登记）**：**只有真正算出数的条目才给 PASS/FAIL，纯陈述一律 INFO**。"
    "初稿曾把 A 组的 `act` 写成恒 0，使 A01–A11 自动 PASS ——那是**假 PASS**（判据恒真、零判别力）；已改为「权重和的非零分量个数」实测，"
    "并补 **CTL7**（删一个权必须报非零）证明检测有牙齿。结果：**43 条中 13 条降级为 INFO**，PASS 30 条全部出自算术或枚举。"
    "（该纪律的直接来历是 r293 的「有命中 ≠ 无」「PASS ≠ 有内容」，本卷把它前移成**写作时**的约束。）\n"
    "- **诚实边界**：①**不否证 r294**，只补前提并把结论改写成比值形式，两卷不可相加；②**不关闭 CY3 / 轨形逃逸**，只给代价；"
    "③**E2 分数通量不判决**，是本卷唯一实质缺口（`X-R295-1`）；④Theorem A 机检覆盖 11 个表示，一般性由 Weyl 不变性论证给出；"
    "⑤结论限定「单一通量、单一 U(1) 方向」，多 U(1) 各自独立通量属新物理假设（`X-R295-2`）；⑥**本卷没有给出任何新预言**，它是一次减法。\n"
    "- **与既有卷**：**r294** 攻其 OPEN、结论加强而非推翻｜**r292** 其 P5「指标定理与三代冲突」被两次独立加强｜"
    "**r293** 沿用其「PASS ≠ 有内容」纪律并在写作阶段即执行｜**r267** CY3 上「3 是选择不是预言」与其「独有可证伪预言 = 0」同构｜"
    "**r264** 「可数内生数值 = 0」再次体现：三代数目在该框架内不是算出来的量｜"
    "**r270** 可为其验收规范补一条：**「紧致化方案必须报告多重度谱型（比值），而不只是代数」**。\n"
    "- **取号**：落盘前实测 r295 / r296 三树全空、README 四处锚点均为 0；r294 已于本批早前由并行会话落盘"
    "（`TUFT-r294_磁通手征谱三代不可实现定理…`，其取号行明记「r293 已被并行会话占用」）。取 **r295** 未抢未碰他人字节。"
    "**下轮从 r296 复查起（并行链活跃，取号前必扫）**。\n"
    "- **治理**：未改 `verify.py`；未跑 `refresh_catalog.py`；未改任何既有卷字节；git 由收口提交统一处理；"
    "**本卷 43 条不可与 r142–r294 相加**。\n"
)

A_SRC = "│   ├── TUFT-r294_"
A_JUD = "├── 判定_TUFT-r294_"
A_CMP = "- **r294（2026-11-01）· 磁通手征谱"

K_SRC = "│   ├── TUFT-r295_"
K_JUD = "├── 判定_TUFT-r295_"
K_CMP = "- **r295（2026-11-01）"
K_DET = "### r295 · 2026-11-01"


def insert_after(text, anchor, payload):
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith(anchor):
            lines.insert(i + 1, payload)
            return "\n".join(lines), i + 2
    return None, -1


def main():
    old = io.open(README, encoding="utf-8").read()
    if not os.path.exists(BAK):
        with io.open(BAK, "w", encoding="utf-8") as f:
            f.write(old)
        print("[bak] 已创建:", BAK)
    else:
        print("[bak] 既有备份保留（不覆盖）")

    txt = old
    log = []
    for key, anchor, payload, name in [
        (K_SRC, A_SRC, SRC_LINE, "src"),
        (K_JUD, A_JUD, JUD_LINE, "jud"),
        (K_CMP, A_CMP, COMPACT, "cmp"),
    ]:
        if key in txt:
            log.append((name, "SKIP-已存在", -1))
            continue
        t, ln = insert_after(txt, anchor, payload)
        if t is None:
            print("FAIL 锚点未命中:", name, anchor)
            return 2
        txt = t
        log.append((name, "INSERT", ln))
        if name == "cmp":
            lines = txt.split("\n")
            j = ln - 1
            if j + 1 < len(lines) and lines[j + 1].strip() != "":
                lines.insert(j + 1, "")
                txt = "\n".join(lines)

    if K_DET in txt:
        log.append(("det", "SKIP-已存在", -1))
    else:
        if not txt.endswith("\n"):
            txt += "\n"
        txt += DETAIL
        log.append(("det", "APPEND", txt.count("\n")))

    if txt == old:
        print("[write] 无变化，不写盘")
    else:
        with io.open(README, "w", encoding="utf-8") as f:
            f.write(txt)
        print("[write] 已写盘")
    for k, a, ln in log:
        print("  %-4s %-14s line=%s" % (k, a, ln))

    new = io.open(README, encoding="utf-8").read()
    ok = True
    for name, key in [("源码树", K_SRC), ("判定树", K_JUD), ("compact", K_CMP), ("detail", K_DET)]:
        c = new.count(key)
        print("[verify] %-8s %-26s count=%d %s" % (name, key, c, "OK" if c == 1 else "BAD"))
        if c != 1:
            ok = False

    ol, nl = old.split("\n"), new.split("\n")
    sm = difflib.SequenceMatcher(None, ol, nl, autojunk=False)
    deleted, inserted = [], 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("delete", "replace"):
            deleted.extend(ol[i1:i2])
        if tag in ("insert", "replace"):
            inserted += (j2 - j1)
    print("[diff] 删除/替换行 = %d（须 0）；新增行 = %d" % (len(deleted), inserted))
    for ln in deleted:
        print("   - ", ln[:90])
    if deleted:
        # 末行无尾换行⇒追加后被补 \n，diff 记为 replace。按内容复核。
        last = ol[-1]
        same = new.count(last) == 1
        print("[diff] 末行内容在新文件中出现次数 = %d（=1 则仅补尾换行，内容零改动）" % new.count(last))
        if len(deleted) == 1 and deleted[0] == last and same:
            print("[diff] 判定：唯一「删除」为末行尾换行归一化，内容零改动 ⇒ 通过")
            deleted = []
    if deleted:
        ok = False

    print("[diff] 行数 %d → %d（+%d）" % (len(ol), len(nl), len(nl) - len(ol)))
    print("REG-%s" % ("OK" if ok else "FAIL"))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
