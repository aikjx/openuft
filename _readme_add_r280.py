# -*- coding: utf-8 -*-
"""README 登记 r280：动态锚点 + 文末增量章节。用法：python _readme_add_r280.py [stage]"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\a10\aikjx\code\my_lib\openuft"
RP = "04_公共成果/本项目_全维自洽与归一化/README.md"
P = os.path.join(REPO, RP.replace("/", os.sep))
STAGE = len(sys.argv) > 1 and sys.argv[1] == "stage"

B = ("TUFT-r280_方法全谱总攻与VP标度函数曲线_"
     "十方法族普查与九点x全谱与Z普适性机检_"
     "精算与可视化_2026-10-31")

L_SRC = (
    "│   ├── " + B + ".py  # 新增（**r280 · 2026-10-31**）："
    "**方法全谱总攻与 VP 标度函数曲线（★新层 · 自驱轮）——『所有方法试试』的直接执行**"
    "（条目 **8**：PASS 5 / FAIL 1 / BOUNDARY 1 / INFO 1；**控制组 6/6**、**守卫 6/6**、退出码 0）。"
    "★**方法全谱普查（A1）**：10 方法族逐一机器状态——几何选择✗关闭（四线指纹）、"
    "变分/能量极小✗二次类关闭（r271-A6）、RG/UV 固定点✗关闭（r250）、"
    "人择选择→不可机检登记、numerology→红线禁止（§6.2）、实验拟合→禁止（靶自flag 同款）、"
    "弦景/群论唯一性/信息论→0 供给、宇宙学早期固定→开放无机制（LHAASO 登记）——"
    "**可机检族全部关闭 ⇒ 方法空间内 L6（协变作用量供给）确认为唯一入口**（封账级结论）。"
    "★**VP 标度函数 Φ(x) 九点数值曲线（B1）**：x=a/λ_e∈{0.01…137} 跨 4 量级"
    "（Φ 从 0.0805 单调降至 2.4e-6——压抑区 1/a³ 标度、非接触平台、深非接触区），"
    "窗口=min(6λ_e,10a)=积分器支撑域、小 s 端 u_max 自适应扩展至 12（r275/276 的 s≥0.28 不受影响）——"
    "**L8 兼容义务从 3 测点升级为连续曲线（C1 FAIL）：任何候选动力学的 VP 机制必须逐点重现**。"
    "★曲线×实物互证（B2）：eH=26.92 MHz（r276 26.8865，rel 1.1e-3）、μH=205.33 meV"
    "（204.9839，rel 1.7e-3）、μd=227.72 meV（227.6076，rel 4.8e-4）。"
    "★**μHe 第四测点（B3，Z=2, x=0.341）**：机算 Δ(2P−2S)=1665.76 meV——"
    "**库内预测值（实测锚下一轮核实）**；Z 归一 Φ_μHe=0.04915 vs 曲线 0.04913"
    "（rel 4.1e-4）——**Φ 的 Z-普适性机检成立**（Z 依赖全在 prefactor (Zα)）——"
    "一条曲线同时覆盖质量维与电荷维。L10 保持 0 bit（C2）；判别资产升级为函数曲线。"
    "★取号事件（治理档）：首扫 r277⇒取 r278 落盘；并行抢 r278（四力统一方程卷）⇒让号 r279；"
    "并行续抢 r279（覆盖本卷 runner——竞态追尾实锤）⇒**二次让号改取 r280**"
    "（移动靶下跳号+快速落盘破局；G4 机读复核非本卷 *r280*=0）。"
    "开发期自抓 4 处（B3 标题占位符错位/B2 eH 换算 ×241.799 差 1000×——meV→MHz 应 ×241799/"
    "CTL1 归一化窗口设计错（2S 第二瓣在 6λ 窗外——改专用 30a 窗口）/**取号注记长串匹配×2 次"
    "失败改行级替换**）——全部由守卫链/运行报错抓出后修复重跑全绿，未带病落盘。"
)

L_VD = (
    "├── 判定_" + B + ".md  # 新增（**r280 · 2026-10-31**）：方法全谱总攻判定册 —— "
    "§判词 · §判决分组（A 方法普查/三体系 x 坐标 / B Φ 曲线+互证+Z-普适 / C 义务终形+L10）· "
    "§★性质界定四条（方法普查是诚实执行——试过的有指纹、试不了的登记、不许试的亮红线；"
    "Φ 曲线把 L8 义务函数化——判别力从 3 bit 级跃升函数级；Z-普适=维度压缩；L10 纪律）· "
    "§治理（判定册落 `判定/`）。"
)

L_INC = (
    "- **r280（2026-10-31）· 方法全谱总攻与 VP 标度函数曲线（★新层 · 自驱轮）**："
    "『所有方法试试』的直接执行。条目 8（PASS 5 / FAIL 1 / BOUNDARY 1 / INFO 1），"
    "控制组 6/6，守卫 6/6，rc=0；"
    "源码 [`TUFT-r280_…py`](源码/" + B + ".py)；"
    "判定册 [`判定_TUFT-r280_…md`](判定/判定_" + B + ".md)。"
    "★十方法族普查封账：可机检族全关闭 ⇒ L6 唯一入口；"
    "★**VP 标度函数 Φ(x) 九点曲线**（x 跨 4 量级）+ 三体系互证 + **μHe 第四测点（Z=2）"
    "Z-普适性机检**——L8 义务升级为连续曲线；L10 保持 0 bit。"
    "取号事件：r278/r279 双重竞态 ⇒ 二次让号 r280（治理档）。下轮从 r281 复查起。"
)

L_SEC = """

### r280 · 2026-10-31 · 方法全谱总攻与 VP 标度函数曲线（★新层 · 自驱轮）

- **产物**：源码 [`TUFT-r280_…py`](源码/__B__.py) / [`…html`](源码/__B__.html)；数据 [`…json`](数据/__B__.json) / [`…md`](数据/__B__.md) / [`…_report.txt`](数据/__B___report.txt)；判定册 [`判定_TUFT-r280_…md`](判定/判定___B__.md)；runner `源码/_run_r280.py` → `源码/_out_r280.txt`
- **复现**：`python -X utf8 源码\\TUFT-r280_…py` ⇒ **rc=0**，条目 **8**（**PASS 5 / FAIL 1 / BOUNDARY 1 / INFO 1**），**控制组 6/6**，**守卫 6/6**。开发期自抓 4 处，全部修复后重跑全绿。
- **结论一句话**：**『所有方法试试』执行完毕：十方法族普查封账——可机检族（几何/变分二次类/RG 固定点）全部关闭、不可机检与零供给族登记、禁止族红线 ⇒ L6（协变作用量供给）确认为唯一入口；VP 标度函数 Φ(x) 九点曲线（x 跨 4 量级）+ μHe Z-普适性机检把 L8 兼容义务从 3 测点升级为连续曲线——判别资产函数化，L10 保持 0 bit。**
- **取号事件（治理档）**：首扫 r277 ⇒ r278 落盘；并行抢 r278 ⇒ 让号 r279；并行续抢 r279（覆盖本卷 runner）⇒ 二次让号 r280。移动靶治理：跳号+快速落盘。**下轮从 r281 复查起（并行链活跃，取号前必扫）**。
- **与前置卷的关系**：方法族状态挂 r257-D1/r269-B1/r271-B1/r277-C1（几何）、r271-A6（变分）、r250（RG）、r263-C1（LHAASO）；Φ 曲线承接 r275/r276 积分器与三体系锚。
- **治理**：自驱轮无来料；五份前置判定册在盘（G1 指纹）；未改 `verify.py`；未跑 `refresh_catalog.py`；git 由收口提交统一处理（分域暂存）；**本卷条目不可与 r142–r279 相加**。
""".replace("__B__", B).replace("___B__", B)

if STAGE:
    head = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + RP],
                          stdout=subprocess.PIPE).stdout.decode("utf-8")
    lines = head.split("\n")
else:
    lines = io.open(P, "r", encoding="utf-8").read().split("\n")


def max_anchored(pattern):
    best, bl = -1, -1
    for i, s in enumerate(lines):
        m = re.search(pattern, s)
        if m:
            n = int(m.group(1))
            if n > best:
                best, bl = n, i
    return best, bl


n_src, i_src = max_anchored(r"│   ├── TUFT-r(\d+)")
n_vd, i_vd = max_anchored(r"^├── 判定_TUFT-r(\d+)")
n_inc, i_inc = max_anchored(r"^- \*\*r(\d+)（")

ins = []
if i_src >= 0:
    ins.append((i_src + 1, L_SRC))
if i_vd >= 0:
    ins.append((i_vd + 1, L_VD))
if i_inc >= 0:
    ins.append((i_inc + 1, L_INC))
ins.sort(key=lambda x: -x[0])
for idx, text in ins:
    lines.insert(idx, text)
lines.append(L_SEC)

out = "\n".join(lines)
if STAGE:
    io.open(os.path.join(REPO, "_tmp_readme_r280_stage.md"), "w",
            encoding="utf-8").write(out)
    print("STAGE 版构建：锚 src=r%d vd=r%d inc=r%d；行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
else:
    io.open(P, "w", encoding="utf-8").write(out)
    print("README r280 登记：锚 src=r%d vd=r%d inc=r%d；总行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
