# -*- coding: utf-8 -*-
r"""r254 修正登记：只补回缺失的 源码树/判定册树/增量章紧凑 三处（完整块已由并行会话登记）。
唯一扩展锚点（带 '# 新增（**r253 ...）' 后缀），命中须=1，否则中止。CRLF 保留。
"""
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
RD = os.path.join(HERE, "README.md")
BAK = os.path.join(HERE, "_README_r254_three_only.md")
shutil.copy2(RD, BAK)

raw = open(RD, "rb").read()
crlf = b"\r\n" in raw
text = raw.decode("utf-8").replace("\r\n", "\n")
lines = text.split("\n")

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

i_src = insert_after(anchor_src, [src_new], "src")
i_jud = insert_after(anchor_jud, [jud_new], "jud")
i_cmp = insert_after(anchor_compact, [compact_new], "compact")

out = ("\r\n" if crlf else "\n").join(lines)
open(RD, "w", encoding="utf-8", newline="\n").write(out)

print("CRLF preserved:", crlf)
print("lines before/after:", len(text.split("\n")), "/", len(lines))
print("src after %d | jud after %d | compact after %d" % (i_src + 1, i_jud + 1, i_cmp + 1))
print("full-block count for r254 (应=1):", out.count("### r254 · 2026-10-31 · 四力统一方程·宇宙学扰动层"))
for key in ["TUFT-r254_四力统一方程_宇宙学扰动层_线性增长因子BAO声视界与sigma8演化_精算与交互可视化_2026-10-31.py",
            "判定_TUFT-r254_四力统一方程_宇宙学扰动层_线性增长因子BAO声视界与sigma8演化_精算与交互可视化_2026-10-31.md",
            "**r254（2026-10-31）· 宇宙学扰动层"]:
    print("  present:", key, "=>", key in out)
