# -*- coding: utf-8 -*-
"""r336 README 注册（detail-only 追加，零删除）。"""
import io, os, datetime

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(BASE, "README.md")
RID = "r336"

SRC = "TUFT-r336_族数唯一性定理_反常自由荷空间实为2维_单扭转唯一纯复制_双扭转反例_精算与可视化_2026-11-01.py"
DATA = "TUFT-r336_族数唯一性定理_反常自由荷空间实为2维_单扭转唯一纯复制_双扭转反例_精算与可视化_2026-11-01"
JUD = "判定_TUFT-r336_族数唯一性定理_反常自由荷空间实为2维_单扭转唯一纯复制_双扭转反例_2026-11-01.md"
HTML = "四力统一方程_族数唯一性与反常自由荷空间维数可视化_2026-11-01.html"

with io.open(README, "r", encoding="utf-8") as f:
    old = f.read()

if "TUFT-r336_" in old:
    print("SKIP: README 已含 r336")
    raise SystemExit(0)

block = """### r336 · 2026-11-01 · 族数唯一性定理 · 反常自由荷空间实为 2 维、单扭转下唯一纯复制（★攻 r309 荷空间维数与 r330 判词范围 · 判词链第 11 层）

- **产物**：源码 [`%s`](源码/%s)；数据 [`…json`](数据/%s.json) / [`…md`](数据/%s.md) / [`…_report.txt`](数据/%s_report.txt)；判定册 [`%s`](判定/%s)；runner `源码/_run_r336.py` → `源码/_out_r336.txt`；交互可视化 [`%s`](%s)
- **复现**：`python -X utf8 源码\\_run_r336.py` ⇒ **rc=0**，条目 **28**（主 **11**：**PASS 9 / INFO 2**，FAIL 0），**控制组 6/6**，**守卫 11/11**，全 Fraction 精确；HTML 几何体检 **GEOMETRY-OK**（680×340，26 图元）+ 负对照（回填 `width:0` ⇒ 精确报「rect(fill=#fff) 宽度为 0 ⇒ 不可见」、rc=1）。
- **本卷攻两处自身前提**：① r309 Thm S「反常自由荷空间**恰好 1 维 = span(Y)**」；② r330「**N 自由是破反常自由的假象**」。
- **结果 1（荷空间维数，两次修正）**：把四条反常改写到 `y_i = d_i q_i`，前三条**线性**、RREF 秩 3 ⇒ 零空间 **3 维**；三次条件在其上**精确分解** `F = (b+c)·Q/12`（2197 点零失配；负对照：分母改 11 ⇒ 1944 点失配）⇒ 解集 = **一个平面 ∪ 一个二次曲面**，至少 **2 维**。显式反例 `u=(0,−1,1,0,0,0)`、`v=(0,0,0,0,1,−1)` 均反常自由且 **∉ span(Y)**。再加 Yukawa：表面两条相容条件，但 μ 项把二者合成 `2X₀+X₁+X₂=0`，**恰是 [SU3]²Y 那条** ⇒ 只加一条独立条件 ⇒ **6 表示下仍是 2 维（Y 与 B−L 并存，rank{Y,B−L}=2）**。而至 **5 表示（无 ν^c）** 时 Yukawa 只剩三条 ⇒ 秩 4 ⇒ **恰好 1 维 = span(Y)**。⇒ **「1 维」的真身是「5 表示 + Yukawa」**，这解开了本库长期记着的「r302 用 5 / r296,r306 用 6」不一致（**`X-R330-2` 关闭**）。
- **结果 2（定理）**：设 `n_i = y_i + k_i·T = N`，`k∈{0,1}^6`。对 i 求和并用**引力反常 `Σy_i=0`** ⇒ **`T·K = 6N`**（K=Σk∈{0..6}）⇒ **`y_i = N − k_i·T` 被 k 唯一确定**，可解性退化为「逐模式查四条反常」。K∈{1,2,3,6}：K=3 ⇒ `y∈{N,−N}`，`[SU3]²Y = y₀+y₁+y₂` 取值 {±3N,±N} ≠ 0；K=2 ⇒ `y∈{N,−2N}`，`[SU2]²Y = y₀+y₃` 取值 {2N,−N,−4N} ≠ 0；K=1 ⇒ 同理排除；K=6 ⇒ `y≡0` ⇒ **纯复制**。机检 **N=1..12 非平凡存活恒为 0**（总存活恒为 1）⇒ **单扭转列下等指标解唯一是纯复制**，与表示数、Yukawa、m 全无关。
- **结果 3（反例，下调 r330 判词）**：放宽到**两条扭转列** `n_i = y_i + k¹_iT₁ + k²_iT₂`：N=3 时真双列（T₁≠T₂）反常自由解 **12** 组；**更强的是在 Yukawa 全合规（q∝Y）下**仍有真通量解 —— 显式 **M=3, T₁=6, T₂=3, k¹=(0,1,0,1,0,0), k²=(0,1,0,0,0,1)** ⇒ `n=(3,3,3,3,3,3)`。⇒ **承重前提不是「反常自由」，而是「扭转自由度只有一个群元」**；r330 的 `N-FREE-IS-ANOMALY-VIOLATING-ARTIFACT` **降级为单扭转口径下的定理**。r307 的 `k_R∈{0,1}` 只是 **per-element**，不排除多群元/多模叠加后 `k^eff>1`。
- **判词**：**SINGLE-TWIST-UNIQUENESS-THEOREM / TWIST-COLUMN-COUNT-IS-THE-LOAD-BEARING-PREMISE**。净结论不变：**框架不预言 3**，3 只能作为扭转量子 T、列数 t、模式 k 的输入；判据集 **R1–R12 = 0/12**。遗留 `X-R336-1`（扭转自由度能否真有两个独立群元 —— **本卷唯一可翻盘处**）/ `X-R336-2`（5 表示下重算）/ `X-R330-1`（改判为「加扭转列」问题）/ `X-R322-1` / `X-R318-1`。
- **取号**：并行链已落 r331（族数整性定理）并正在做 r333（仅见来料原件）⇒ 取 **r336**（r334/r335 留空，src 树跳号正常）。**治理**：未改 verify.py；未跑 refresh_catalog.py；未改任何既有卷字节（G9 逐路径核验）；README 仅追加大本条目。**下轮从 r337 复查起（并行链极活跃，取号前必扫三树 + README detail）。**
""" % (SRC, SRC, DATA, DATA, DATA, JUD, JUD, HTML, HTML)

bak = os.path.join(BASE, "README.bak_%s_%s.md" % (RID, datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
if not os.path.exists(bak):
    with io.open(bak, "w", encoding="utf-8") as f:
        f.write(old)

sep = "" if old.endswith("\n\n") else ("\n" if old.endswith("\n") else "\n\n")
new = old + sep + block + "\n"

with io.open(README, "w", encoding="utf-8") as f:
    f.write(new)

old_lines = old.splitlines()
new_lines = new.splitlines()
prefix_ok = new_lines[:len(old_lines)] == old_lines
n_detail = sum(1 for ln in new_lines if ln.startswith("### r336 ·"))
n_src = sum(1 for ln in new_lines if "TUFT-r336_" in ln)
print("BAK:", os.path.basename(bak))
print("prefix_preserved(零删除):", prefix_ok)
print("detail anchors '### r336 ·':", n_detail)
print("lines with TUFT-r336_:", n_src)
print("RESULT:", "PASS" if (prefix_ok and n_detail == 1) else "FAIL")
