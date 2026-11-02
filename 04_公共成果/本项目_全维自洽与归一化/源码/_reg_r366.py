# -*- coding: utf-8 -*-
"""r366 README 登记（现行格式：源码树 + 判定列表 两处；compact 行与 detail 节已于
2026-11-01 23:14:59 被并行会话整体移除，本脚本只做**加法登记**，不代修他人缺口）。

纪律：①锚点含本卷 RID；②先判存在再分流（幂等 SKIP）；③验证键带位置前缀；④最终守卫 = diff 零删除。
"""
import io
import os
import shutil
import sys

RID = "r366"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
BAK = os.path.join(ROOT, "scratch", "_bak_README_pre_%s.md" % RID)

STEM = ("TUFT-r366_整值多项式通有性审计_整性判别力恒零_牛顿系数被td钉死"
        "_陪集周期紧界N等于D_精算与可视化_2026-11-02")
HTML = "四力统一方程_整值多项式通有性审计_r366可视化_2026-11-02.html"

ANCH_SRC = "│   ├── TUFT-r358_"
ANCH_JUD = "├── 判定_TUFT-r358_"

KEY_SRC = "│   ├── TUFT-r366_"
KEY_JUD = "├── 判定_TUFT-r366_"

LINE_SRC = (
    "│   ├── " + STEM + ".py  # 新增（**r366 · 2026-11-02**）：**整值多项式通有性审计：整性判别力恒零 / "
    "牛顿系数被 td 钉死 / 陪集周期紧界（★攻 `X-R358-1` 周期紧界 + `X-R358-2` `D(c)` 闭式，并回答「什么才有判别力」）**"
    "（主条目 **25**：PASS 25 / FAIL 0 / INFO 0；**控制组 15/15**、**守卫 19/19**、退出码 0）。"
    "★**取号**：r359/r361–r364 为空但邻居未收口，r360/r365/r368 已被占且四件套齐全 ⇒ "
    "取**被两卷包夹**的冷号 **r366**，先写 `_probe_r366.py` 占位再动大文件，零改他人字节。"
    "★★★**定理 H（本卷最硬产出）**：`X_d ⊂ CP^{n+1}` 的 χ 的牛顿系数有**完全闭式** "
    "**`a_m = C(n+1,m) − C(n+1−d, n+1−m)`**（广义二项式）⇒ `(a_0..a_n)` 由 `(n,d)` **两个参数完全钉死，零自由度**；"
    "而一般整值多项式有 **`n+1` 个自由整数参数** ⇒ 几何类是 `Int(Z)` 中的**零测真子集**。"
    "★★★**证明只要三行且不需要 td**：Koszul `0 → O(k−d) → O(k) → O_X(k) → 0` + χ 加性 + `Δ^m C(x+k,N)|₀ = C(x,N−m)`"
    " ⇒ **r339/r346/r358 绕 Todd 类算 χ 的路径是充分不必要的**；且第 2 步**不需要消灭定理** ⇒ "
    "定理 H 对 **CY 与一般型同样成立**（非 Fano 24 组，占 47.1%，失配 0）。"
    "★★★**判别力翻转（本卷核心）**：同一批 **16000** 个随机整值多项式上 —— "
    "r346 引理 L **16000/16000**、r358 定理 E **16000/16000** ⇒ **判别力恒为 0**；"
    "而**定理 H 命中 0/16000** ⇒ **判别力 ≈1**。这是三代主线（r331→…→r358）**第一次拿到非判别力零**的判据。"
    "★敏感性：几何 `a` 扰动一位后存活 **4/126**，且 4 次**全部是族内移动**（`(n,d=n)` 与 `(n,d=n+1)` 只差末位），**族外漏网 0**。"
    "★★**三条独立路径两两对拍 51 组 × 3 对，失配 0**：A（td 级数/Bernoulli/Stirling）vs C（Koszul 计数）vs H（闭式），互不共享中间量。"
    "★CY 自检：`d=n+2` 时 `a_0 = χ(O_X) = 1+(−1)^n` ⇒ 椭圆曲线 **0**、K3 **2**、五次三维 CY **0**、四次曲线 **−2**，全中。"
    "★★**`X-R358-2` 已答（素因子部分）**：140 个陪集上 **`D(c)` 的素因子集合 ⊆ `c` 的分母 `q` 的素因子集合，违例 0**"
    " ⇒ r358 见到 `D` 爆到 **3.6e7** 是 **c 的算术**，不是几何的复杂性；精确幂次转入 `X-R366-4`。"
    "★★**`X-R358-1` 归约**：140 个陪集分流 **EMPTY 78 / FULL 58 / PARTIAL 4**（部分占 2.9%，与 r358 的 11/396≈2.8% 一致）；"
    "PARTIAL 上 `N = D` **4/4**（合计 15/15），且 `|S| = H/D = n!`、`N = H/|S|` ⇒ "
    "**`N = D` 等价于「解集在 `Z/H` 上是一条轨道」** —— 后者未独立证明 ⇒ **只说归约，不说证明**。"
    "★**不推翻 r339/r346/r358 任何读数**：`D01` χ(k) 逐点对拍 **170** 点失配 0、`D02` r346 定理 C 51 组违例 0、"
    "`D03` r358 定理 E′ 70 陪集分歧 0、`D04` r358 非陪集机制重述（`(3,2)`：`D=4`、`N=4`、`|S|=6`）。"
    "★**定价** 2⁵=32 ⇒ 可行 **12** / 钉住 **1** 位（`S1` 由 K7 钉住）/ 自由 4 位翻转均可 ⇒ **不占度，候选 37，链止 r264:36**。"
    "★**自审六处（本卷踩出）**：①`CTL12` 的 `ok` **写死 `True`**（明知故犯，本库**第三卷**同族）⇒ G19 抓出；"
    "②`B05` 期望值**是猜的**（猜 ≤1 而真值 4）⇒ 改由解析路径 `closedH(n,d+1)−closedH(n,d)=C(n−d,n−m)` 独立算出；"
    "③**定价约束太弱 ⇒ 0 位被钉住**（与 r358 同族）⇒ 补 K7「本卷至少产出一个结论」；"
    "④`CTL4` 用 `isinstance(x,int)` 判 **`Fraction` 恒假** ⇒ 改 `F(x).denominator == 1`；"
    "⑤`CTL15` **扰动改错地方**：`BERN[2]=1/6` 经 `/2!` 后仍是 `1/12` ⇒ 负对照恒绿（漏网 **51/51**）⇒ 改 `1/3` 后失配 **44/51**；"
    "⑥解集周期**未做环形回绕**（探查 3 的 bug，`N=None`）⇒ 加 `C06` 成对对照（环形 4 vs 非环形 None）。"
    "**家族自伤第七卷 `r327→r331→r335→r339→r346→r358→r366`，落点仍在「守错门」。下轮从 r367 起。**"
)

LINE_JUD = (
    "├── 判定_TUFT-r366_" + STEM[len("TUFT-r366_"):] + ".md  # 新增（**r366 · 2026-11-02**）："
    "整值多项式通有性审计判定册（攻 `X-R358-1` + `X-R358-2`，回答「什么才有判别力」）—— "
    "§判决主文（**八段判词 ↔ 命题逐句对应表**，每段挂承重条目）· "
    "§为什么值得单独立册（r346/r358 连续两次「功劳归还」后必须回答：这条线上还有没有能判别几何的东西）· "
    "§定理 H（闭式 `a_m = C(n+1,m) − C(n+1−d, n+1−m)`；三行证明只需 Koszul + χ 加性；**td 是充分不必要**）· "
    "§判别力（引理 L / 定理 E 在 `Int(Z)` 上 **100%** ⇒ 判别力 0；定理 H **0/16000** ⇒ ≈1；敏感性 4/126 且全为族内移动）· "
    "§`X-R358-2` 与 `X-R358-1`（`D(c)` 素因子 ⊆ `c` 分母素因子，140 组 0 违例；`N=D` 归约为「解集单轨道」，**未证**）· "
    "§与既有卷的关系（`D01` 170 点失配 0 / `D02` 51 组违例 0 / `D03` 70 陪集分歧 0 / `D04` 机制重述；**只改路径不改读数**）· "
    "§控制组 15/15（含 **2 条扰动型双读数**：CTL14 上标错位 48/51 失配**漏网 3**、CTL15 错算 td 44/51 失配**漏网 7**"
    " ⇒ 主校验是**必要非充分**的 bug 探测器）· "
    "§判据与方法（沉淀六条：**先闭式再取样** / **判别力必须两侧都测** / **源码级检查一律走 AST** / "
    "**「值相等」≠同义反复** / **负对照扰动要落在敏感方向** / **空全部分三类必须分流**）· "
    "§定价（32 ⇒ 可行 12、钉住 S1、自由 4 位）· §自审六处 · "
    "§诚实边界（定理 H 只证「给不出别的」没证「所以必须给这个」，与 r327 同型；判别力只在随机整值多项式这一个对照类上测过）· "
    "§遗留 OPEN（`X-R366-1` 完全交与加权超曲面 / `X-R366-2` 单轨道的独立证明 / `X-R366-3` 用定理 H 反审框架 / `X-R366-4` `D(c)` 精确幂次）· §最终一句。"
)


def keys(txt):
    return [txt.count(KEY_SRC), txt.count(KEY_JUD)]


old = io.open(README, encoding="utf-8").read()
k0 = keys(old)
if all(c == 1 for c in k0):
    print("SKIP (already registered)  keys=%r" % (k0,))
    sys.exit(0)
if any(c != 0 for c in k0):
    print("PARTIAL / BAD STATE keys=%r -> 人工处置" % (k0,))
    sys.exit(3)

if not os.path.exists(BAK):
    os.makedirs(os.path.dirname(BAK), exist_ok=True)
    shutil.copy2(README, BAK)
    print("BACKUP -> scratch/_bak_README_pre_%s.md" % RID)

L = old.split("\n")


def find_one(anchor, name):
    hits = [i for i, l in enumerate(L) if l.startswith(anchor)]
    if len(hits) != 1:
        print("ANCHOR %s hit=%d" % (name, len(hits)))
        for i in hits:
            print("   %d %s" % (i, L[i][:70]))
        sys.exit(4)
    return hits[0]


i_src = find_one(ANCH_SRC, "src")
i_jud = find_one(ANCH_JUD, "jud")
print("anchors: src=%d jud=%d" % (i_src, i_jud))

M = list(L)
for pos, txt in sorted([(i_src, LINE_SRC), (i_jud, LINE_JUD)], key=lambda t: -t[0]):
    M.insert(pos + 1, txt)
out = "\n".join(M)

io.open(README, "w", encoding="utf-8").write(out)

chk = io.open(README, encoding="utf-8").read()
k1 = keys(chk)
print("post-keys src=%d jud=%d" % tuple(k1))
if not all(c == 1 for c in k1):
    print("REG-FAIL（验证键不是 1）")
    sys.exit(5)

old_l, new_l = old.split("\n"), chk.split("\n")
p = 0
for line in new_l:
    if p < len(old_l) and line == old_l[p]:
        p += 1
if p != len(old_l):
    print("DIFF-DELETION: 只对上 %d/%d 行 ⇒ 有旧行丢失" % (p, len(old_l)))
    sys.exit(6)
print("DIFF-ZERO-DELETION ok (%d/%d 旧行原位保留)" % (p, len(old_l)))
print("bytes %d -> %d (delta %+d)" % (len(old.encode("utf-8")), len(chk.encode("utf-8")),
                                      len(chk.encode("utf-8")) - len(old.encode("utf-8"))))
print("REG-OK %s" % RID)
