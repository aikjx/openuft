# -*- coding: utf-8 -*-
"""r358 README 登记（现行格式：源码树 + 判定列表 两处；compact 行与 detail 节已于 23:14:59
被并行会话整体移除，本脚本只做**加法登记**，不代修他人缺口）。

纪律：①锚点含本卷 RID；②先判存在再分流（幂等 SKIP）；③验证键带位置前缀；④最终守卫 = diff 零删除。
"""
import io
import os
import shutil
import sys

RID = "r358"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
BAK = os.path.join(ROOT, "scratch", "_bak_README_pre_%s.md" % RID)

STEM = ("TUFT-r358_整性集的精确结构_陪集只需n加一个值判定_"
        "周期等于分母最小公倍数_窗口法不可靠_精算与可视化_2026-11-01")
HTML = "四力统一方程_整性集精确结构_r358可视化_2026-11-01.html"

ANCH_SRC = "│   ├── TUFT-r346_"
ANCH_JUD = "├── 判定_TUFT-r346_"

KEY_SRC = "│   ├── TUFT-r358_"
KEY_JUD = "├── 判定_TUFT-r358_"

LINE_SRC = (
    "│   ├── " + STEM + ".py  # 新增（**r358 · 2026-11-01**）：**整性集的精确结构：陪集只需 n+1 个值判定 / "
    "周期等于分母最小公倍数 / 窗口法不可靠（★攻 `X-R339-2` 非陪集机制 + `X-R346-2` 额外点判据，并压 `X-R346-1` 周期界）**"
    "（主条目 **25**：PASS 25 / FAIL 0 / INFO 0；**控制组 13/13**、**守卫 19/19**、退出码 0）。"
    "★**取号**：r355/r356 已被并行会话占（r356 仅源码、无判定册＝热号），r357 紧邻热区 ⇒ 取冷号 **r358**，"
    "先写 `_probe_r358.py` 占位再动大文件，零改他人字节。"
    "★★★**方法换挡（本卷真正的增量在方法）**：不再在网格上数点，先用 **Vandermonde** 把陪集上的多项式整个算出来 —— "
    "`P(c+m) = Σ_i b_i(c) C(m,i)`、`b_i(c) = Σ_{j≥i} a_j C(c, j−i)`；再**整数化** `β_i = D·b_i ∈ Z`（`D = lcm_i den b_i`）⇒ "
    "**`Q_c(m) ∈ Z ⟺ f(m) = Σ β_i C(m,i) ≡ 0 (mod D)`**，纯整数、快一个量级、且**可判定**。"
    "★★★**定理 E′（本卷最实用）**：`c+Z ⊆ S ⟺ P(c), P(c+1), …, P(c+n) ∈ Z` —— **只需 n+1 个值**就能判定整个陪集"
    "（证：`b_i = Δ^i Q(0)` 只用 `Q(0..i) ⊆ Q(0..n)`）；`A02` **304/304** 一致；`n+1` **不可减**（`C(m,n)/2` 反例 `A06` **4/4**）。"
    "★★★**定理 G（压 `X-R346-1`）**：最小周期 **可证 `N | D·n!`**（Taylor + `C(D·n!, i) ∈ D·Z`），"
    "实测 **`N = D`**（`B02` **11/11**，全在对角线上）⇒ 界由 r346 的 `(M^n n!)²` 压到 `D·n! ≤ M^n (n!)²`，"
    "实测最大压缩 **14 117 880 倍**（`B04`）。★`N = D` 是**实测未证**，另开 `X-R358-1`；`N | M^n` 早已被 `(5,2)` 的 `N=64 > M^n=32` 否证。"
    "★★★**定理 F（结构封口）**：每个部分陪集在一个周期内**恰 1 个整点**（`C01` **11/11**）⇒ "
    "**`S = Z ∪（每个陪集至多一条、公差 = D(c) 的等差级数）`**。"
    "★**r339 的「非陪集」由此机制化**：`(3,2)` 上 `D=4`、解 `m ≡ 2 (mod 4)` ⇒ 见证点 `−11/2, −3/2, 5/2` 差值 4 就是 `D`；"
    "「非陪集」= 「`Z` 与一条公差 4 的 AP 之并」—— 两个不同模数拼在一起，`u−v+w` 必然失败（`C06` 逐点核对通过）。"
    "★★**否证一个诱惑**：固定窗口法在原理上不可靠 —— UND 区 `D` 最大 **35 831 808**（`B06` **92** 个），"
    "11 个部分陪集里 **6** 个 `D > 12`（`D03`）；r339 只看到 `(5,2)` 的 1 个孤立点正是此效应。"
    "★**精确普查**：396 个陪集 = **FULL 70 / PARTIAL 11 / EMPTY 223 / UND 92**；"
    "`n ≥ 2` 时额外点只来自 `M ∈ {2,3}`（`B05`，238 个陪集违反 **0**），`n=1` 例外（`S=(1/d)Z` 使所有 `M | d` 整段）。"
    "★★**第二次功劳归还**：`A05` 定理 E 在 **299** 个随机整值多项式上也 100% 成立、`C03` 「单剩余类」在 **265** 个随机样本上也 100% 成立"
    " ⇒ 两条都是**多项式的初等事实**，**不得当判据用**（判别力 0），只能当结构陈述。"
    "★**不推翻 r339/r346 任何读数**：`D01` 30 组 Newton 与 r346 JSON 逐项字符串相等差异 **0**；`D02` 周期读数 **11/11** 一致；"
    "引擎主校验 `χ == h⁰` **480** 个 (组,k) 失配 **0**。"
    "★**定价** 2⁶=64 ⇒ 可行 **24** / 匹配 **1** / 钉住 **1** 位（`S6` 窗口法可靠被否证）/ 翻转 **0** ⇒ **不占度，候选 37，链止 r264:36**。"
    "★**自审四处（本卷踩出）**：①`C03` 判据实参写成 `True`（**假判据**，r346 是 `guard(...,True,...)`，**第二卷**同族）；"
    "②`E01` 期望值**是猜的**（猜 24 而真值 32）⇒ 改由**约束语法手算**（2⁵ − 2³）取期望；"
    "③**约束太弱 ⇒ 定价退化**（首跑 32 个可行、**0 位被钉住**）⇒ 补第 4 条约束 `S6=0`；"
    "④**分类器算法错**（用 gap 的 gcd 当最小周期，多条 AP 时会低估；`C(m,2)/2` 的 gcd 是 1 而真周期 4）⇒ 改最小正平移法并配构造自检。"
    "**家族自伤第六卷 `r327→r331→r335→r339→r346→r358`，落点仍在「守错门」。下轮从 r359 起。**"
)

LINE_JUD = (
    "├── 判定_TUFT-r358_" + STEM[len("TUFT-r358_"):] + ".md  # 新增（**r358 · 2026-11-01**）："
    "整性集精确结构判定册（攻 `X-R339-2` + `X-R346-2`，压 `X-R346-1`）—— "
    "§判决主文（**七段判词 ↔ 七条命题逐句对应表**，每段挂读数）· §为什么值得单独立册"
    "（r339 只给现象、r346 只给一半结构，两者都还在**网格上数点**；本卷改用 Vandermonde 把陪集多项式**解析地算出来**）· "
    "§定理 E′/E（陪集判据：`n+1` 个值 / `b` 全整，双向；`n+1` **不可减**；**功劳在多项式不在几何**）· "
    "§定理 G（`N | D·n!` 已证、`N = D` 实测 **11/11**；界从 `(M^n n!)²` 压到 `D·n!`，最大压缩 **14 117 880** 倍；`N|M^n` 已否证）· "
    "§定理 F（一周期恰 1 点 ⇒ 一条 AP ⇒ `S = Z ∪ 每陪集至多一条`；分类器自检 `C(m,2)/2` 报 2 类；**判别力 0** 故降级为结构陈述）· "
    "§与 r339/r346 的关系（`D01` 30 组逐项差异 0、`D02` 周期 **11/11**、`C06` 见证点逐点核对、引擎主校验 480 失配 0；**只 sharpen 不推翻**）· "
    "§判据与方法（沉淀三条：**先 Vandermonde 再取样** / **最小周期不能用 gap 的 gcd 求** / **定价约束必须足以钉住至少一位**）· "
    "§定价（可行 24 / 匹配 1 / 钉住 1 位 / 翻转 0）· "
    "§自审四处（假判据 / 期望靠猜 / 约束太弱导致定价退化 / 分类器算法错）· "
    "§诚实边界（`N = D` 实测未证 / UND 92 个不当作空 / 单剩余类判别力 0 / 全 Fraction 与整数运算）· "
    "§遗留 OPEN（`X-R358-1` `N=D` 能否证 / `X-R358-2` `M∈{2,3}` 的机制 / `X-R358-3` 自然密度与族数 / `X-R339-3` / `X-R335-1` / `X-R331-1`）· §最终一句。"
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
