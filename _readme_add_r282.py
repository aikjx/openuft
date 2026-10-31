# -*- coding: utf-8 -*-
"""README 登记 r282：动态锚点 + 文末增量章节。用法：python _readme_add_r282.py [stage]"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\a10\aikjx\code\my_lib\openuft"
RP = "04_公共成果/本项目_全维自洽与归一化/README.md"
P = os.path.join(REPO, RP.replace("/", os.sep))
STAGE = len(sys.argv) > 1 and sys.argv[1] == "stage"

B = ("TUFT-r282_Φ曲线双端解析锚定与四体系闭合_"
     "接触极限解析链与Φ无穷等于α平方除20_精算与可视化_2026-10-31")

L_SRC = (
    "│   ├── " + B + ".py  # 新增（**r282 · 2026-10-31**）："
    "**Φ(x) 双端解析锚定与四体系闭合（★新层 · 自驱轮）——把 r280 曲线两端用解析极限钉死**"
    "（条目 **8**：PASS 5 / FAIL 1 / BOUNDARY 1 / INFO 1；**控制组 6/6**、**守卫 6/6**、退出码 0）。"
    "★**大 x 端解析链（A1/A2）**：∫₁^∞√(t²−1)/t⁴ dt=1/3、∫₁^∞√(t²−1)/(2t⁶) dt=1/15 ⇒ "
    "**∫₀^∞ sF(s)ds=2/5**（数值 3000 点收敛命中）⇒ **Δ_contact=α⁵m_ec²/(30π)"
    "（vs eH r276 值 rel 0.9%——平坦近似+2P 修正层）⇒ Φ∞=α²/20=2.6626e-6"
    "（m_ec²·λ_e=ħc 完全消去——本库第一个纯解析精确的标度函数锚）**；"
    "曲线大 x 点 Φ(137)/Φ∞=0.90 逼近中、Φ(10)/Φ∞=165 vs 1/x² 律 169（dev 2.3%✓）、"
    "Φ(2)/Φ∞=2723 vs 4230（dev 36% 高阶层如实登记）。"
    "★小 x 端对数层（A3）：Φ(0.01)/Φ(0.1)=1.069 ⇒ ln-ln 斜率 0.029（近平台缓升）——左端闭合。"
    "★四体系闭合表（B1）：eH(x=137.04)/μH(0.737)/μd(0.700)/μHe(0.341) 全部落曲线——"
    "μHe=1665.76 meV 为 r280 登记预测（实测锚 web 两轮未获——持续开放）。"
    "★K=5+1 普查扩展（B2，r277 遗留清账）：m_n/m_p=1.001378 核结构层登记"
    "（经 m_d=m_p+m_n−2.224 MeV 进入 μd 链）——普查边界推进至核物理门口。"
    "★**L8 义务终形（C1 FAIL 承接）：双端解析锚定+四体系锚+Z-普适的连续曲线——四重约束下"
    "固定比值候选的机制缺位量化到函数级**；L10 保持 0 bit（C2）。"
    "★取号事件（治理档）：首扫 r280⇒取 r281 落盘；并行又抢 r281（四力统一方程·红移漂移卷）——"
    "**第三次让号改取 r282**（竞态治理惯例沿用 r268/r280；G4 机读复核非本卷 *r282*=0）。"
    "开发期自抓 3 处（A3 标题裸占位符/∫sF 网格欠收敛 2-3%——3000 点收敛解决/CTL1 evidence "
    "网格不一致）——全部由守卫链/运行报错抓出后修复重跑全绿，未带病落盘。"
)

L_VD = (
    "├── 判定_" + B + ".md  # 新增（**r282 · 2026-10-31**）：Φ 曲线双端解析锚定判定册 —— "
    "§判词 · §判决分组（A 解析链/大 x 锚/小 x 层 / B 四体系表+K=5+1 / C 义务终形+L10）· "
    "§★性质界定四条（Φ∞=α²/20 是本库第一个纯解析精确标度锚；双端锚定的认识论意义——"
    "带解析边界条件的连续函数；μHe 预测仍开放；K=5+1 边界推进）· §治理（判定册落 `判定/`）。"
)

L_INC = (
    "- **r282（2026-10-31）· Φ 曲线双端解析锚定与四体系闭合（★新层 · 自驱轮）**："
    "条目 8（PASS 5 / FAIL 1 / BOUNDARY 1 / INFO 1），控制组 6/6，守卫 6/6，rc=0；"
    "源码 [`TUFT-r282_…py`](源码/" + B + ".py)；"
    "判定册 [`判定_TUFT-r282_…md`](判定/判定_" + B + ".md)。"
    "★∫sF=2/5 解析机检 + Δ_contact=α⁵m_ec²/(30π)（rel 0.9%）+ **Φ∞=α²/20 纯解析锚**；"
    "大 x 1/x² 律命中、小 x 对数层 0.029——曲线双端闭合；四体系闭合表（μHe 预测待锚）；"
    "K=5+1（m_n/m_p 核结构层）。L8 义务终形：四重约束连续曲线。"
    "取号事件：第三次让号（并行抢 r281）⇒ r282。下轮从 r283 复查起。"
)

L_SEC = """

### r282 · 2026-10-31 · Φ(x) 双端解析锚定与四体系闭合（★新层 · 自驱轮）

- **产物**：源码 [`TUFT-r282_…py`](源码/__B__.py) / [`…html`](源码/__B__.html)；数据 [`…json`](数据/__B__.json) / [`…md`](数据/__B__.md) / [`…_report.txt`](数据/__B___report.txt)；判定册 [`判定_TUFT-r282_…md`](判定/判定___B__.md)；runner `源码/_run_r282.py` → `源码/_out_r282.txt`
- **复现**：`python -X utf8 源码\\TUFT-r282_…py` ⇒ **rc=0**，条目 **8**（**PASS 5 / FAIL 1 / BOUNDARY 1 / INFO 1**），**控制组 6/6**，**守卫 6/6**。开发期自抓 3 处，全部修复后重跑全绿。
- **结论一句话**：**VP 标度函数曲线双端解析闭合：大 x 端 Φ∞=α²/20（∫sF=2/5 解析链，纯解析精确锚）+ 小 x 端对数层 0.029 + 中段四体系锚（eH/μH/μd/μHe）+ Z-普适——L8 兼容义务达到终形（四重约束连续函数）；K=5+1 普查扩展清账 r277 遗留；L10 保持 0 bit。**
- **与 r280 的关系**：r280 建立九点数值曲线；本卷补双端解析极限（Φ∞=α²/20 精确锚 + 对数层）并扩展 K=5+1——曲线从『数值样本』升级为『带解析边界条件的函数』。
- **取号事件（治理档）**：并行又抢 r281 ⇒ **第三次让号 r282**（惯例沿用 r268/r280）。**下轮从 r283 复查起（并行链活跃，取号前必扫）**。
- **治理**：自驱轮无来料；五份前置判定册在盘（G1 指纹）；未改 `verify.py`；未跑 `refresh_catalog.py`；git 由收口提交统一处理（分域暂存）；**本卷条目不可与 r142–r281 相加**。
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
    io.open(os.path.join(REPO, "_tmp_readme_r282_stage.md"), "w",
            encoding="utf-8").write(out)
    print("STAGE 版构建：锚 src=r%d vd=r%d inc=r%d；行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
else:
    io.open(P, "w", encoding="utf-8").write(out)
    print("README r282 登记：锚 src=r%d vd=r%d inc=r%d；总行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
