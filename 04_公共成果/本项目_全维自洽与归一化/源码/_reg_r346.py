# -*- coding: utf-8 -*-
"""r346 README 登记（现行格式：源码树 + 判定列表 两处；compact 行与 detail 节已被并行会话整体移除，
本脚本只做**加法登记**，不代修他人缺口）。

纪律：①锚点含本卷 RID；②先判存在再分流（幂等 SKIP）；③验证键带位置前缀；④最终守卫 = diff 零删除。
"""
import io
import os
import shutil
import sys

RID = "r346"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
BAK = os.path.join(ROOT, "scratch", "_bak_README_pre_%s.md" % RID)

STEM = ("TUFT-r346_整数Newton系数是三行初等事实而非几何定理_"
        "分母整除首项定理与判词下调_精算与可视化_2026-11-01")
HTML = "四力统一方程_整数Newton系数_r346可视化_2026-11-01.html"

ANCH_SRC = "│   ├── TUFT-r339_"
ANCH_JUD = "├── 判定_TUFT-r339_"

KEY_SRC = "│   ├── TUFT-r346_"
KEY_JUD = "├── 判定_TUFT-r346_"

LINE_SRC = (
    "│   ├── " + STEM + ".py  # 新增（**r346 · 2026-11-01**）：**整数 Newton 系数是三行初等事实而非几何定理"
    "（★攻 `X-R339-1`：r339 定理 B「`a_j` 全整」的一般证明）**"
    "（主条目 **25**：PASS 25 / FAIL 0 / INFO 0；**控制组 13/13**、**守卫 19/19**、退出码 0）。"
    "★**取号**：扫号见 r340–r344 全被占、r345 为热号 ⇒ 取冷号 **r346**，大文件动手前先写 `_probe_r346.py` 占位，零改他人字节。"
    "★★★**主结论（判词 `...DEMOTED-FROM-A-THEOREM-TO-A-DEFINITION-TAUTOLOGY`）**："
    "`X-R339-1` 的答案**不是**「几何定理的一般证明」，而是「**这根本不是几何定理**」—— "
    "**引理 L（三行，无几何）**：`a_j = Δ^j P(0) = Σ_i (−1)^{j−i} C(j,i) P(i)` 是**整数组合** ⇒ `P(Z) ⊆ Z` 时 `a_j ∈ Z`；"
    "套到 `χ` 上只需一句话（**`χ` 是欧拉示性数**）⇒ **r339「定理 B」从定理降级为定义恒等式**。"
    "★★**两条承重件都不承重**：`a_j ∈ Z` 是「整数组合仍是整数」；`Z ⊆ S` 是 `S` 的定义。故其 30/30 不是发现，是**引擎自检**。"
    "★★**判别力 0**：72 组（n=1..6, d=1..12）全部通过（`A04`）⇒ 一个 100% 通过的谓词**不得当判据用**。"
    "★★**但它是 bug 探测器**：故意算错 td 两种（少一个 `T` / `td_cpn` 写成逐元素幂）⇒ 非整 **27/30** 与 **29/30**（`A05`）；"
    "却**漏掉 3 组与 1 组**（`A06`）⇒ **必要非充分**，r339 的 30/30 只能证明「没犯某些错」。"
    "★★★**定理 C（本卷唯一不平凡产出，且无假设）**：`k = r/M` 最简、`P(k) ∈ Z` ⇒ **`M | a_n`**。"
    "四行证明：乘 `M^n n!`、取模 `M`、`N_j(r) ≡ r^j (mod M)` 消掉 `j<n` 全部项、只剩 `a_n r^n`，`gcd(r,M)=1` 收尾；"
    "**连 `a_j ∈ Z` 都不需要**。推论：超曲面上 `a_n = d`（`CTL11` 72 组违例 0）⇒ **`S ⊆ (1/d)Z`**；"
    "`n=1` 时等号成立（`B04` **24/24**）；`M=d` 仅 **13/72** 可达 ⇒ `n ≥ 2` 只是**上界**不是等号（`B05`）。"
    "分母谱只能是 `d` 的因子，`B06` 越界 **0**。"
    "★★★**定理 D（把 r339 的「非陪集」从混沌改写成结构）**：每个陪集 `c+Z` 上整性**周期**，"
    "`b_i = Σ_{j≥i} a_j C(c,j−i)`（**396 陪集失配 0**）、`M^n n! b_i ∈ Z`（**1782 项非整 0**）⇒ 周期界 `(M^n n!)^2`（**81/81 合法**）⇒ "
    "**`S` 是有限个等差级数之并** ⇒ 并集上仿射封闭 `u−v+w` 必然失败，**这就是 r339 看到「非陪集」的原因**。"
    "实测周期 ∈ {1,2,4,16,32,64}；`(5,2)` 的 **N=64 > M^n=32** ⇒ **`N | M^n` 已被否证**（新开 `X-R346-1`）。"
    "★★**跨卷口径（不推翻 r339 任何读数）**：`G11` 与 r339 落盘 JSON 的 30 组 Newton **逐项字符串相等，差异 0**；"
    "`D04` 重跑 r339 的 `χ==h⁰` 主校验 **448/448 失配 0**，但**重贴标签**为「引擎正确性校验」而非「超曲面有特殊算术」。"
    "★**定价** 2⁶=64 ⇒ 可行 **3** / 匹配 **1** / **被钉住 4 位**、未钉住 2 位（`S1,S2` 只能联合判定）/ 翻转钉住位后 **0** ⇒ **不占度，候选 37，链止 r264:36**。"
    "★**自审三处（本卷踩出，家族自伤第五次 r327→r331→r335→r339→r346，落点从「算错对象」移到「守错门」）**："
    "①**假守卫** —— `G04/G09/G17` 首跑写成 `guard(..., True, ...)`，正是本库明令禁止的写死 ⇒ 全部改真判据，并新增 **`G19` 结构性防线**（`ctl/guard` 的 `ok` 顶层不得是常量）；"
    "②**守卫自命中** —— `G12/G13` 用 `src.count(\"random\")` 把自己的字符串字面量数进去 ⇒ 改 **AST 层**查 `Import`/浮点 `Constant`；"
    "③**期望值是猜的** —— `C06` 期望 `7,1,1` 而实测 `7,0,1` ⇒ 改两条独立路径交叉（直接扫描 vs 陪集枚举），期望取自另一条。"
    "**下轮从 r347 起（并行链极活跃：取号前必扫三树 + README 两树；大文件动手前先写 `_probe_rN.py` 占位）。**"
)

LINE_JUD = (
    "├── 判定_TUFT-r346_" + STEM[len("TUFT-r346_"):] + ".md  # 新增（**r346 · 2026-11-01**）："
    "整数 Newton 系数判定册（攻 `X-R339-1`，**答案是「这不是几何定理」，判词下调**）—— "
    "§判决主文（**七段判词 ↔ 七条命题逐句对应表**，每段挂读数）· §为什么值得单独立册"
    "（`X-R339-1` 问「一般证明」，答「一般证明只有三行且不需要几何」⇒ 追问「那这条定理说了什么」⇒ **两条承重件全不承重**）· "
    "§引理 L（`a_j = Δ^j P(0)` 是整数组合；**只靠 `χ` 是欧拉示性数**一步落地；三行、无几何）· "
    "§判别力 0 与 bug 探测器（`A04` 72/72 全绿 ⇒ 无判别力；`A05` 错算 td ⇒ 非整 27/30、29/30；`A06` 漏 3 组与 1 组 ⇒ **必要非充分**）· "
    "§定理 C（`M | a_n`，**无假设**、四行证明；推论 `S ⊆ (1/d)Z`；`n=1` 等号 24/24；`M=d` 仅 13/72 ⇒ `n≥2` 只是上界；分母谱只含 `d` 的因子）· "
    "§定理 D（陪集周期 + `b_i` 闭式 396 失配 0 / `M^n n! b_i` 1782 项非整 0 / 周期界 `(M^n n!)^2` 81/81）"
    "⇒ **`S` 是有限个等差级数之并**，把 r339 的「非陪集」从混沌改写成结构；`(5,2)` 的 N=64 > M^n=32 ⇒ `N|M^n` 否证）· "
    "§与 r339 的关系（`G11` 30 组逐项差异 0、`D04` 448/448 重跑但**重贴标签**；**不推翻任何读数，只改读法与信用归属**）· "
    "§判据与方法（沉淀三条：**假守卫三字母就能让门禁变装饰 ⇒ 结构性防线 `G19`** / **守卫不得读自己源码的字符串字面量，须 AST 层** / **期望值只能取自另一条独立路径**）· "
    "§定价（可行 3 / 匹配 1 / 钉住 4 位 / 翻转 0）· "
    "§自审三处（假守卫 / 守卫自命中 / 期望靠猜；**家族自伤第五卷**，落点已从「算错」移到「守错」）· "
    "§诚实边界（`X-R339-1` 只答了「是定义恒等式」未给更强的替身判据 / 定理 D 的周期界**不紧** / 未覆盖加权超曲面 / 全 Fraction）· "
    "§与既有卷的关系（r335→r339→r346 三代读数全复现；分层铁律不可相加）· "
    "§遗留 OPEN（`X-R346-1` 周期与 `M^n` 的确切关系 / `X-R339-2` / `X-R339-3` / `X-R336-1` / `X-R335-1` / `X-R331-1`）· §最终一句。"
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
