# -*- coding: utf-8 -*-
"""README 登记 r285：动态锚点 + 文末增量章节。用法：python _readme_add_r285.py [stage]"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\a10\aikjx\code\my_lib\openuft"
RP = "04_公共成果/本项目_全维自洽与归一化/README.md"
P = os.path.join(REPO, RP.replace("/", os.sep))
STAGE = len(sys.argv) > 1 and sys.argv[1] == "stage"

B = ("TUFT-r285_五测点预测与Φ曲线加密_"
     "μ三氦第五测点与十三点全谱与同位素标度机检_"
     "精算与可视化_2026-10-31")

L_SRC = (
    "│   ├── " + B + ".py  # 新增（**r285 · 2026-10-31**）："
    "**五测点预测与 Φ 曲线加密（★新层 · 自驱轮）——承接 r280/r282**"
    "（条目 **8**：PASS 4 / FAIL 1 / BOUNDARY 1 / INFO 2；**控制组 6/6**、**守卫 6/6**、退出码 0）。"
    "★Φ 曲线 9 点→**14 点**加密（x∈{0.01…137}，Φ 单调递减 0.0805→接触极限，CTL3 单调机检）——"
    "L8 义务曲线分辨率提升 55%。"
    "★**μ³He 第五测点预测（B3 前条 A2，Z=2, x=0.344）**：m_r=101.8274 MeV、a=132.778 fm、"
    "Δ(2P−2S)=**1641.88 meV（库内预测值，实测锚未发布——登记待锚）**；"
    "μHe 复算回归 1665.76 meV（rel 2.8e-6——r280 显示层舍入）；"
    "**Z-普适性双确认**：Φ_μ³He=0.04888 vs 曲线 0.04889（rel 7.6e-5）、"
    "Φ_μHe=0.04915 vs 0.04913（rel 4.1e-4）——两个 Z=2 体系同落 Z=1 曲线。"
    "★μHe/μ³He 同位素对（A3）：Δ 比值 %.4f vs naive m_r³ %.4f——非接触修正（新类判别靶："
    "同 Z 不同中子数的波函数微差）。"
    "★五测点汇总（A4）：eH 26.887 MHz / μH 204.98 / μd 227.61 / μHe 1665.76 / μ³He 1641.88"
    "（后二预测待锚）——**L8 义务终形（B1 FAIL 承接）：14 点曲线+五测点+同位素微差+Z-普适+"
    "双端解析锚——判别完备度达本库机器极限（C2 声明）**；L10 保持 0 bit（B2）。"
    "开发期自抓 2 处（A3 字面 % 未转义消耗格式参数/A2 标题裸占位符）+CTL2 阈值改显示层舍入"
    "（r280 值 %.2f）+EXPECT_DIST 条目数对齐——全部由守卫链/运行报错抓出修复重跑全绿，"
    "未带病落盘。"
)

L_VD = (
    "├── 判定_" + B + ".md  # 新增（**r285 · 2026-10-31**）：五测点预测与 Φ 曲线加密判定册 —— "
    "§判词 · §判决分组（A 加密/第五测点/同位素对/汇总 / B 义务终形+L10 / C 治理+完备度声明）· "
    "§★性质界定四条（同位素对是新类判别靶；预测登记在先纪律——git 时间戳；"
    "判别完备度声明——继续加密边际信息量低于实测锚到位；L10 纪律）· §治理。"
)

L_INC = (
    "- **r285（2026-10-31）· 五测点预测与 Φ 曲线加密（★新层 · 自驱轮）**："
    "条目 8（PASS 4 / FAIL 1 / BOUNDARY 1 / INFO 2），控制组 6/6，守卫 6/6，rc=0；"
    "源码 [`TUFT-r285_…py`](源码/" + B + ".py)；"
    "判定册 [`判定_TUFT-r285_…md`](判定/判定_" + B + ".md)。"
    "★Φ 曲线 14 点加密 + **μ³He 第五测点预测 1641.88 meV（待锚）** + μHe 回归 + "
    "**Z-普适双确认**（rel ≤4.1e-4）+ 同位素对标度机检；"
    "L8 义务终形：14 点+五测点+同位素微差+Z-普适+双端解析锚。L10 保持 0 bit。"
    "取号实测（启动时）⇒ r285。"
).replace("%.4f", "")

L_SEC = """

### r285 · 2026-10-31 · 五测点预测与 Φ 曲线加密（★新层 · 自驱轮）

- **产物**：源码 [`TUFT-r285_…py`](源码/__B__.py) / [`…html`](源码/__B__.html)；数据 [`…json`](数据/__B__.json) / [`…md`](数据/__B__.md) / [`…_report.txt`](数据/__B___report.txt)；判定册 [`判定_TUFT-r285_…md`](判定/判定___B__.md)；runner `源码/_run_r285.py` → `源码/_out_r285.txt`
- **复现**：`python -X utf8 源码\\TUFT-r285_…py` ⇒ **rc=0**，条目 **8**（**PASS 4 / FAIL 1 / BOUNDARY 1 / INFO 2**），**控制组 6/6**，**守卫 6/6**。开发期自抓 2 处+CTL2 舍入层阈值+条目数对齐，全部修复重跑全绿。
- **结论一句话**：**Φ 曲线 14 点加密完成；μ³He 第五测点预测 1641.88 meV（登记在先待锚）；μHe/μ³He Z-普适双确认（rel ≤4.1e-4）+ 同位素微差标度机检——L8 兼容义务达到本库机器极限的完备判别集（14 点+五测点+同位素微差+Z-普适+双端解析锚）；L10 保持 0 bit。**
- **与 r280/r282 的关系**：r280 九点曲线+μHe 预测 → r282 双端解析锚 → 本卷 14 点加密+μ³He 第五测点+同位素对——五轮递进（r275 积分器起）完成 L8 义务的机器极限形式。
- **取号**：2026-10-31 实测三树最大占用（启动时）⇒ 取 **r285**（G4 机读复核）。**下轮从 r286 复查起（并行链活跃，取号前必扫）**。
- **治理**：自驱轮无来料；五份前置判定册在盘（G1 指纹）；未改 `verify.py`；未跑 `refresh_catalog.py`；git 由收口提交统一处理（分域暂存）；**本卷条目不可与 r142–r284 相加**。
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
    io.open(os.path.join(REPO, "_tmp_readme_r285_stage.md"), "w",
            encoding="utf-8").write(out)
    print("STAGE 版构建：锚 src=r%d vd=r%d inc=r%d；行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
else:
    io.open(P, "w", encoding="utf-8").write(out)
    print("README r285 登记：锚 src=r%d vd=r%d inc=r%d；总行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
