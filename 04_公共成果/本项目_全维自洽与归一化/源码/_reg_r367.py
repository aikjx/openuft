# -*- coding: utf-8 -*-
"""r367 README 登记（现行格式：源码树 + 判定列表 两处；只做**加法登记**，不代修他人缺口）。

纪律：①锚点含前卷 RID；②先判存在再分流（幂等 SKIP）；③验证键带位置前缀；④最终守卫 = diff 零删除。
"""
import io
import os
import shutil
import sys

RID = "r367"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
BAK = os.path.join(ROOT, "scratch", "_bak_README_pre_%s.md" % RID)

STEM = ("TUFT-r367_完全交与加权超曲面的牛顿系数闭式_陪集周期N等于D的反例搜索"
        "_与轨道数定理_精算与可视化_2026-11-03")
HTML = "四力统一方程_完全交牛顿系数闭式与额外点充要条件_r367可视化_2026-11-03.html"

ANCH_SRC = "│   ├── TUFT-r366_"
ANCH_JUD = "├── 判定_TUFT-r366_"

KEY_SRC = "│   ├── TUFT-r367_"
KEY_JUD = "├── 判定_判定_TUFT-r367_"

LINE_SRC = (
    "│   ├── " + STEM + ".py  # 新增（**r367 · 2026-11-03**）：**完全交的牛顿系数闭式 + 额外点的充要条件 + "
    "陪集周期的反例搜索（★攻 `X-R366-1` 完全交 / `X-R358-2` 额外点刻画 / `X-R366-2` `N = D` 反例搜索）**"
    "（主条目 **24**：PASS 24 / FAIL 0 / INFO 0；**控制组 11/11**、**守卫 20/20**、退出码 0）。"
    "★**取号**：r370/r374–r381 已被并行会话占且四件套齐全、r361/r378 为散件 ⇒ "
    "取**被 r365 与 r368 双向包夹**的冷号 **r367**，先写 `_probe_r367.py` 占位再动大文件，零改他人字节。"
    "★★★**定理 K（本卷最硬产出，`X-R366-1` 已答）**：完全交 `X_{d_1..d_r} ⊂ CP^N`（`n = N − r`）的牛顿系数有**完全闭式** "
    "**`a_m = Σ_{S⊆[r]} (−1)^{|S|} C(N − d_S, N − m)`**（`d_S = Σ_{i∈S} d_i`，广义二项式），"
    "`r = 1` 退化为 r366 定理 H ⇒ **r366 的「零自由度」从超曲面推广到任意余维**。"
    "★★★**证明仍只要三行且不需要 Todd 类**：Koszul 复形 + χ 加性 + `Δ^m C(x+k,N)|₀ = C(x,N−m)`；"
    "前两步**不需要消灭定理** ⇒ 定理 K 对 **CY 与一般型同样成立**。两路径（td 级数 / Koszul 闭式）对拍 **239 组失配 0**。"
    "★★★**定理 P（额外点的充要条件，`X-R358-2` 推进）**：`PARTIAL ⟺ (n 为奇数且 n ≥ 3) ∧ (d 为偶数) ∧ (c 为半整数)`；"
    "1088 个可算陪集（枚举 1200、`D > 6000` 跳过 112）**违例 0**；**充分性 30/30**、**必要性 0/1058**、"
    "**无盲区**（跳过组中满足三条件的 0 组）；两条负控分别拆掉一条（半整数但 d 奇 84 组 0、n 偶 460 组 0）。"
    "PARTIAL 的 `c` 既约分母集合 = `[2]`（**全是半整数**），与 r339 的三个孤证 `−11/2, −3/2, 5/2` 吻合；"
    "`D` 取值 `[2, 4, 32, 64]` 全为 2 的幂（与 r366 `C03` 一致）。"
    "`n = 1` 无 PARTIAL 由 r346 定理 C（`S = (1/d)Z`）解释，`D03` 实测 144 组 0。★**这是枚举证据，不是解析证明**（`X-R367-1` 保留）。"
    "★★**`X-R366-2` 广域反例搜索**：30 个 PARTIAL 陪集的**类数（轨道数）分布 `[(1,30)]`**，多类 **0**、周期恒为 `D` ⇒ `N = D`，"
    "**零反例**（含探查阶段 3144 组）。**零反例 ≠ 证明**，`CAP_D = 6000` 之外只排除了 PARTIAL 侧（`X-R367-4`）。"
    "★**对照构造 `C(m,2)/2`**：`β=[0,0,1]`、`D=2` ⇒ 解集 `{0,1,4,5}` 在 mod 4 下占**两个剩余类**、周期 **4 ≠ D**"
    " ⇒ 证明「类数恒 1」**不是通有性质**，`C01` 有判别力。机理差异（`C03`）：几何类 `β_n = D·a_n = D·d ≡ 0 (mod D)`"
    " ⇒ 模 `D` 后最高次项消失。★**方法换挡（快一个量级）**：整数化 `β_i = D·b_i` + **有限差分递推** "
    "`g_j(m+1) = g_j(m) + g_{j+1}(m)`（`g_{n+1} ≡ 0`，全程 `mod D`）⇒ 判整性的代价从 `O(D·n!)` 降到 `O(D)`；"
    "`CTL3` 与 Fraction 直算在 **224 点**不一致 **0**。★**不推翻 r339/r346/r358/r366 任何读数**："
    "`D01` 48 组失配 0 / `D02` 70 陪集分歧 0 / `D04` r339 三点 3/3 / `CTL11` r366 `C03` 1088 组违例 0。"
    "★**定价** 2⁵=32 ⇒ 可行 **10** / 钉住 **1** 位（`S0` 由 K6 钉住）/ 自由 4 位翻转均可 ⇒ **不占度，候选 37，链止 r264:36**。"
    "★**自审三处（本卷踩出）**：①**`GRID_A` 的 `r ≠ len(ds)`（家族自伤第八卷，落点仍是对象错位）** —— "
    "`r ≥ 4` 的分支沿用了三元组 ⇒ 网格记的 `r` 与 `len(ds)` 不等，`pathK(...)[n]` 取错下标；"
    "**诊断价值最高的一点：`A01` 两路径对拍在这批数据上是 0 失配**（两条路径内部错在同一方向），"
    "真正暴露它的是 `A05`（68 违例）与 `A06`（13 违例）—— 这两条的期望值来自**第三条独立路径**"
    " ⇒ 沉淀「凡对拍全绿的卷必须另有第三条路径的条目」；修法 `product(range(1,3), repeat=r)`（256 → 239 组）+ **新增 `G20` 常驻**；"
    "②**有限差分递推的更新顺序**：`g_j(m+1) = g_j(m) + g_{j+1}(m)` 要求右端取**旧值** ⇒ 循环必须 **j 递增**；"
    "j 递减会用已更新的 `g[j+1]`，而**在几何类上这个错法巧合地不出错**（4232 点 0 失配），"
    "只有换到 `C(m,2)/2` 才暴露（正确 `{0,1,4,5}` vs 错误 `{0,3,4,7}`）⇒ 印证「对照类必须换一个」；"
    "③探查 4 的 **9 条假违例**：判「`c` 为半整数」时用了循环变量 `q` 而非既约分母（`F(0,2)` 的既约分母是 **1**）"
    " ⇒ 改 `F(p,q).denominator` 后 1430 组 0 违例。★**新增守卫 `G20`（对象错位守卫）**："
    "`GRID_A` 每组必须满足 `len(ds) == r`，实测违例 0（分母 239）。"
    "**家族自伤第八卷 `r327→r331→r335→r339→r346→r358→r366→r367`，八卷落点全是「守错门」。下轮从 r368 起。**"
)

LINE_JUD = (
    "├── 判定_判定_" + STEM + ".md  # 新增（**r367 · 2026-11-03**）："
    "完全交闭式 + 额外点充要条件 + 陪集周期反例搜索判定册（攻 `X-R366-1` + `X-R358-2` + `X-R366-2`）—— "
    "§判决主文（**五段判词 ↔ 命题逐句对应表**，每段挂承重条目）· "
    "§为什么单独立册（r366 留下三个未决项，每项都卡在「不知道该找什么」）· "
    "§定理 K（闭式 `a_m = Σ_S (−1)^{|S|} C(N−d_S, N−m)`；三行证明只需 Koszul + χ 加性；**td 再次是充分不必要**；239 组对拍 0 失配）· "
    "§定理 P（额外点 ⟺ n 奇且 ≥3 · d 偶 · c 半整数；充分性 30/30、必要性 0/1058、无盲区 0/112；两条负控各拆一条；**枚举证据非证明**）· "
    "§反例搜索（30 个 PARTIAL 类数全 1、周期恒 D ⇒ N = D，**零反例不是证明**；CAP_D 之外 FULL/EMPTY 侧未搜）· "
    "§对照构造（`C(m,2)/2` 类数 2、周期 4 ≠ D ⇒ 「类数恒 1」有判别力；几何类独有 `β_n ≡ 0 (mod D)`）· "
    "§方法换挡（整数化 + 有限差分递推 O(D·n!)→O(D)；**递推必须 j 递增**，几何类上巧合不出错）· "
    "§与既有卷的关系（`D01` 48 组 0 / `D02` 70 陪集 0 / `D03` 144 组 0 / `D04` 3/3 / `CTL11` 1088 组 0；**只改路径不改读数**）· "
    "§控制组 11/11（含 **2 条双读数扰动对照**：CTL1 上标错位 237/239 失配**漏网 2**、CTL2 错算 td 132/239 失配**漏网 107**）· "
    "§守卫 20/20（**新增 `G20` 对象错位守卫**：`len(ds) == r`）· "
    "§定价（32 ⇒ 可行 10、钉住 S0、自由 4 位）· §自审三处 · "
    "§诚实边界（定理 K 已证、定理 P 未证、`N=D` 只到零反例；本卷不产新物理，供给仍 0）· "
    "§遗留 OPEN（`X-R367-1` 定理 P 的解析证明 / `X-R367-2` `D(c)` 精确幂次 / `X-R367-3` 加权完全交 / "
    "`X-R367-4` CAP_D 之外的反例搜索 / `X-R366-2` 单轨道独立证明 / `X-R366-3` 用定理 K 反审框架）· §最终一句。"
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

io.open(README, "w", encoding="utf-8", newline="\n").write(out)

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
