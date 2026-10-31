# -*- coding: utf-8 -*-
r"""r254 README 四处登记：源码树 / 判定册树 / 增量章紧凑 / 增量章完整。
唯一扩展锚点（带 '# 新增（**r253 ...）' 后缀），命中须=1，否则中止。CRLF 保留。
"""
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
RD = os.path.join(HERE, "README.md")
BAK = os.path.join(HERE, "_README_before_r254_reg.md")
shutil.copy2(RD, BAK)

raw = open(RD, "rb").read()
crlf = b"\r\n" in raw
text = raw.decode("utf-8").replace("\r\n", "\n")
lines = text.split("\n")

# ---- 锚点（扩展，唯一）----
anchor_src = ("TUFT-r253_力的无模型定理层_通量守恒与传播子极点及自旋符号与软定理普适性_"
              "七靶大统一方程判决_精算与可视化_2026-10-31.py  # 新增（**r253 · 2026-10-31**）")
anchor_jud = ("判定_TUFT-r253_力的无模型定理层_通量守恒与传播子极点及自旋符号与软定理普适性_"
              "七靶大统一方程判决_精算与可视化_2026-10-31.md  # 新增（**r253 · 2026-10-31**）")
anchor_compact = "**r253（2026-10-31）· 无模型定理层："

R254 = "TUFT-r254_四力统一方程_宇宙学扰动层_线性增长因子BAO声视界与sigma8演化_精算与交互可视化_2026-10-31"

def insert_after(substr, new_lines, tag):
    idxs = [i for i, ln in enumerate(lines) if substr in ln]
    if len(idxs) != 1:
        raise SystemExit("ANCHOR FAIL [%s]: found %d" % (tag, len(idxs)))
    i = idxs[0]
    lines[i + 1:i + 1] = new_lines
    return i

# ---- 新行 ----
src_new = ("│   ├── " + R254 + ".py  # 新增（**r254 · 2026-10-31**；★**复现层**，"
           "非审计层、不进「修复即自杀」度数链）：**宇宙学扰动层 —— 复现标准 ΛCDM "
           "线性扰动骨架（线性增长 D(a) 双路径 / 增长率 f·γ / BAO 声视界 r_d / σ8(z) 演化）**"
           "（条目 **8**：PASS 4 / BOUNDARY 2 / INFO 2；**守卫 5/5**、控制组 2/2、退出码 0）。"
           "★承重：①双路径互印 rel=4.13e−12（RK4 vs 精确积分）②r_d=147.073 Mpc vs Planck 147.09"
           "（rel 1.17e−4）③σ8(z) 单调演化 0.811→0.256。★诚实边界：σ8(0) 是观测输入、"
           "CMB 峰位需 Boltzmann、本卷为教科书结果复现非新物理。")

jud_new = ("├── 判定_" + R254 + ".md  # 新增（**r254 · 2026-10-31**）：宇宙学扰动层判定册 —— "
           "§判词 · §判决分组（H 组 8 条 / G 守卫 5 / C 控制组 2）· §★性质界定"
           "（复现层非审计层 / σ8(0) 观测输入 / 与 r237 不可相加）· §治理"
           "（靶只读、不进自杀度数链）。承重：双路径互印 4.13e−12、r_d 锚 147.073 Mpc、"
           "σ8 演化单调；诚实项 σ8(0) 输入 / CMB 峰位在框架外 / 非新物理。")

compact_new = ("- **r254（2026-10-31）· 宇宙学扰动层：线性增长因子 D(a) / BAO 声视界 r_d / "
               "σ8(z) 演化（★复现层）**：承 r237 背景层进入扰动层，复现标准 ΛCDM 线性扰动骨架。"
               "条目 8（PASS 4 / BOUNDARY 2 / INFO 2），守卫 5/5，控制组 2/2，rc=0；源码 "
               "[`TUFT-r254_…py`](源码/" + R254 + ".py)；判定册 "
               "[`判定_TUFT-r254_…md`](判定/判定_" + R254 + ".md)；数据 "
               "[`…json`](数据/" + R254 + ".json) / [`…md`](数据/" + R254 + ".md) / "
               "[`…_report.txt`](数据/" + R254 + "_report.txt)；交互可视化 "
               "[`四力统一方程_宇宙学扰动层可视化_2026-10-31.html`]"
               "(四力统一方程_宇宙学扰动层可视化_2026-10-31.html)。"
               "★双路径互印 4.13e−12；r_d=147.073 Mpc vs Planck 147.09（rel 1.17e−4）；"
               "σ8(z) 单调 0.811→0.256。★诚实边界：σ8(0) 为观测输入；CMB 峰位/张量需 Boltzmann，"
               "不在本卷；本卷为教科书结果复现，非新物理，不进「修复即自杀」度数链。")

full_block = [
    "",
    "### r254 · 2026-10-31 · 四力统一方程·宇宙学扰动层：线性增长因子 D(a) / BAO 声视界 r_d / σ8(z) 演化（★复现层首卷）",
    "",
    "- **产物**：源码 [`TUFT-r254_…py`](源码/" + R254 + ".py) / [`…html 模板`](源码/TUFT-r254_宇宙学扰动层交互可视化模板_2026-10-31.html)；数据 [`…json`](数据/" + R254 + ".json) / [`…md`](数据/" + R254 + ".md) / [`…_report.txt`](数据/" + R254 + "_report.txt)；判定册 [`判定_TUFT-r254_…md`](判定/判定_" + R254 + ".md)；交互可视化 [`四力统一方程_宇宙学扰动层可视化_2026-10-31.html`](四力统一方程_宇宙学扰动层可视化_2026-10-31.html)；runner `源码/_run_r254.py` → `源码/_out_r254.txt`",
    "- **复现**：`python -X utf8 源码\\_run_r254.py` ⇒ **rc=0**，条目 **8**（**PASS 4 / BOUNDARY 2 / INFO 2**），**守卫 5/5**，**控制组 2/2**。双路径互印 rel=4.13e−12；r_d=147.073 Mpc vs Planck 147.09（rel 1.17e−4）；σ8(z) 单调 0.811→0.256；f0=0.527、γ0=0.554。",
    "- **结论一句话**：宇宙学扰动层全部机器复现（增长双路 1e−3 内、r_d 锚 5% 内、σ8 演化单调）；σ8(0) 为观测输入、CMB 峰位需 Boltzmann——复现层，无新理论。",
    "- **与 r237 的分层（不可相加）**：r237 背景层（年龄/距离-红移/Λ 通道）、r254 扰动层（增长/BAO/σ8），二者均为 ΛCDM 复现的不同增量，与 r228–r234 力层、r248–r253 审计层均不同靶。",
    "- **取号**：起草前实测 **r254/r255/r256 三树全空**（r238–r253 已被并行链占用）；本轮无撞号。**下轮从 r255 起**（落盘前仍须复查时间戳）。",
    "- **治理**：Planck 2018 / Peebles 1980 / Eisenstein–Hu 1998 只读；对 r214–r253 及并行会话产物只读；未改 verify.py；未跑 refresh_catalog.py；未做 git；本卷条目**不可与 r237 及其他线相加**；**不进「修复即自杀」度数链**（PASS 型复现层）。",
]

i_src = insert_after(anchor_src, [src_new], "src")
i_jud = insert_after(anchor_jud, [jud_new], "jud")
i_cmp = insert_after(anchor_compact, [compact_new], "compact")
# 完整块追加到 EOF
lines.extend(full_block)

out = ("\r\n" if crlf else "\n").join(lines)
open(RD, "w", encoding="utf-8", newline="\n").write(out)

print("CRLF preserved:", crlf)
print("lines before/after:", len(text.split("\n")), "/", len(lines))
print("src insert after line %d | jud after %d | compact after %d"
      % (i_src + 1, i_jud + 1, i_cmp + 1))
for key in ["r254 · 2026-10-31 · 四力统一方程·宇宙学扰动层",
            "TUFT-r254_四力统一方程_宇宙学扰动层_线性增长因子BAO声视界与sigma8演化_精算与交互可视化_2026-10-31.py",
            "判定_TUFT-r254_四力统一方程_宇宙学扰动层_线性增长因子BAO声视界与sigma8演化_精算与交互可视化_2026-10-31.md",
            "**r254（2026-10-31）· 宇宙学扰动层"]:
    print("  present:", key, "=>", key in out)
