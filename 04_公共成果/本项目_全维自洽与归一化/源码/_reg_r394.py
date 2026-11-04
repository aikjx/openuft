# -*- coding: utf-8 -*-
"""r394 入 README：双锚点各行插一条。幂等；核验 = 删掉插入行后与备份逐字节相等。"""
import io
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RM = os.path.join(ROOT, "README.md")
BAK = os.path.join(ROOT, "scratch", "_README_bak_r394.md")

TAG_S = ("TUFT-r394_审计ROOTV61_中心化子46与34个残余生成元_单个十维Higgs论证无效但结论对_"
         "Schur锁死二重态三重态简并_六代计数与半整数出口_Jarlskog恒等式精确复核_精算_2026-11-04.py")
TAG_M = ("判定_TUFT-r394_审计ROOTV61_中心化子46与34个残余生成元_单个十维Higgs论证无效但结论对_"
         "Schur锁死二重态三重态简并_六代计数与半整数出口_Jarlskog恒等式精确复核_精算_2026-11-04.md")

ANCHOR_S = "│   ├── TUFT-r392_攻X-R391-1_三代与反常互斥定理"
ANCHOR_M = "├── 判定_TUFT-r392_攻X-R391-1_三代与反常互斥定理"

LINE_S = ("│   ├── " + TAG_S +
          "  # 新增（**r394 · 2026-11-04**）：审计 ROOT V61（四力大统一的真空稳定性与粒子谱审查）"
          "（主册 13：PASS 10 / INFO 2 / FAIL 1；控制组 3；守卫 14/14；合计 30；"
          "`FINAL = GATES-PASS-WITH-1-NEGATIVE`）："
          "① **中心化子 46（`A1`/`A2`）**：66 个显式生成元逐个算 `[T,E_ab]`，三档读数 `T=0 -> 66` / "
          "`T_F=E_{11,12} -> 46` / 一般 Cartan -> `6` **互不相同**（判别力自证）；分解账 `66 = 45+1+10+10`、"
          "`46-12 = 34 = 33+1` 三处加法独立闭合（`G06`）；负对照 `E_{1,12}` 确被排除（`G07`）；"
          "② **V61 §二 的论证无效（`A3`，本卷唯一真判负）**：`so(4)+so(4) < so(8)` 是显式 12 维子代数且对换位封闭 "
          "⇒ 「28 > 12」对「SM < 稳定子」**零判别力** —— **结论对、理由错**；"
          "③ **正确判据是单态计数（`A4`）**：`10 = 5+5bar`，维数和 10、超荷和 0、**单态数 0** ⇒ SM 不稳定化 10 里"
          "**任何**非零矢量（比维数比较更强）；稳定子复算 `36`（单矢量）/ `28`（两独立实矢量，`A5`）；"
          "④ **Schur 锁死（`A6`，核心新刀）**：与整个 `so(10)` 交换的对称 10x10 算子只有 **1 维**（路径集与全 45 个生成元同读数）"
          "⇒ `m_H = m_T` 是**定理**不是模型选择；负对照 `so(8)` 在 `R^10 = 8+1+1` 上给 **4 维**（`K2`）；"
          "⑤ **六代与半整数出口（`A7`/`A8`）**：`N=3 -> 16_{+1} 3 个 + 16bar_{-1} 3 个 = 6`、净手征 6、`Sum s Q^2 = 0`；"
          "改成 `q=(3/2,-3/2)` 给 `n=3` 且 `Sum s Q^2` 仍 0 ⇒ 「6」是**整数性**的后果不是反常；与 r392 的 `n = 2 q+` 同一读数（**不新增证据**）；"
          "⑥ **势与 Δ 四行（`A9`/`A10`）**：`H` 方向 `V''=4=8 lam v^2`、`T` 方向 `V''=2/3=2 Delta`（解析式与 5 点精确 Vandermonde 双路径）；"
          "`m_T^2 = Delta` 还是 `2 Delta` 取决归一化（复场/实分量差因子 2）⇒ 记 INFO 不指控；"
          "⑦ **Jarlskog 精确复核（`A11`）**：`U = D*R`（Gauss 有理相位 x **Cayley 变换**给的一般有理正交阵），"
          "`Im tr = 691103452755937080287232000/631817884405930548876667` 与 `6 J ProdProd` **逐位相等**，命中 `+6`，零容差；"
          "实纹理退化档 `J=0 且 Im tr=0`（`K3` 显式标注）；`|J|/J_CKM = 653.1` ⇒ 不是预言；"
          "⑧ **26/26 可判性分类（`A13`）**：8 行里可判 **4** / 半可判 1 / 不可判或未证明 3 ⇒ 「26/26」不能当 26 条独立证据；"
          "⑨ **自伤七条**：E01 `stabilizer_dim` 行列反、E02 只约束一个矢量（`36/36`）、"
          "**E03 单轴旋转致 `J≡0` 恒等式退化成 `0=0`**（改 Cayley + 三条门禁）、E04 判据过严、E05 显示层、"
          "**E06 `n_half` 一名两用致关键表 `n=1` 而 A8 正文 `n=3`**（改后缀 + 新增 `G14` 漂移守卫）、"
          "**E07 几何行成装饰变量致负对照失效**（改用 `f5Y1` + 断言每个 `fN_Y1` 至少被引用一次）；"
          "⑩ 可视化六图 `GEOMETRY-OK`，两条负对照各打不同图（fig4 越界 1、fig5 越界 1，其余图 0）。独有预言 **0**；不占度（度数链维持 36）。")

LINE_M = ("├── " + TAG_M +
          "  # 新增（**r394 · 2026-11-04**）：ROOT V61 审计判定册 —— "
          "§一 一句话判决（数字全对、结论全对，但有一条**论证**错、有一条「限制」只是「分母」的后果）· "
          "§二 六项主张 + 26/26 表的逐行裁定表 · §三 中心化子三档（66/46/6）与三处加法闭合 · "
          "§四 为什么「28 > 12」无效（`so(4)+so(4)` 是 `so(8)` 的 12 维子代数）+ 36/28 复算 · "
          "§五 单态计数判据（10 的四块分解 + 超荷和当正对照）· §六 Schur（1 维 vs 负对照 4 维）· "
          "§七 六代与半整数出口（两档 `Sum s Q^2` 都 0）· §八 Δ 四行 + 归一化口径账 · "
          "§九 Jarlskog 精确复核（两条不同源路径 + 排序约定 + 退化档）· §十 26/26 的可判性分类 · "
          "§十一 控制组 3 + 守卫 14 读数表 · §十二 自伤清单 E01–E07（含「负对照的尺子没接上」这一最静默型）· "
          "§十三 诚实边界五条 + 与前卷「不相加」声明 + 回链 · §十四 下一轮入口四条（产物真链接写盘实测："
          "源码 41,894 / JSON 17,505 / 报告 17,371 / HTML 13,954；本册 26,388 B、333 行、`bad_blocks=0`、`CRLF=0`）。")


def main():
    raw = open(RM, "rb").read()
    txt = raw.decode("utf-8")
    assert "\r\n" not in txt, "README 出现 CRLF，先归一"
    lines = txt.split("\n")

    if any(TAG_S in ln for ln in lines) and any(TAG_M in ln for ln in lines):
        print("SKIP 两处均已登记，+0 字节")
        return

    shutil.copy2(RM, BAK)
    print("BAK ->", BAK, os.path.getsize(BAK))

    # 自下而上插：先判定列表，后源码树
    def insert_after(anchor, newline, lines):
        idx = [i for i, ln in enumerate(lines) if ln.startswith(anchor)]
        assert len(idx) == 1, ("锚点命中 %d 次：" % len(idx), anchor)
        lines.insert(idx[0] + 1, newline)
        return idx[0] + 1

    i_m = insert_after(ANCHOR_M, LINE_M, lines)
    i_s = insert_after(ANCHOR_S, LINE_S, lines)
    print("插入行号（0 基）：判定 %d，源码 %d" % (i_m, i_s))

    out = "\n".join(lines)
    io.open(RM, "w", encoding="utf-8", newline="").write(out)
    print("README ->", len(out.encode("utf-8")), "B")

    # 核验：删掉两条插入行后必须与备份逐字节相等
    cur = io.open(RM, encoding="utf-8").read().split("\n")
    keep = [ln for ln in cur if not (ln.startswith("│   ├── " + TAG_S) or ln.startswith("├── " + TAG_M))]
    rebuilt = "\n".join(keep).encode("utf-8")
    bak = open(BAK, "rb").read()
    print("删插入行后 == 备份：", rebuilt == bak, "| 差值", len(rebuilt) - len(bak))
    assert rebuilt == bak, "核验失败，禁止写回"
    print("OK 零删除核验通过；新增", len(out.encode("utf-8")) - len(bak), "B")


main()
