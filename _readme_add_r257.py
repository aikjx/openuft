# -*- coding: utf-8 -*-
"""README 登记 r257：动态锚点（树上现行最大号行之后插入）+ 文末增量章节
用法：python _readme_add_r257.py [stage]
  stage 模式 = 从 HEAD 版本出发构建「HEAD + 仅 r257 增量」的分域暂存内容（不写工作区，只写 _tmp 文件）"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\a10\aikjx\code\my_lib\openuft"
RP = "04_公共成果/本项目_全维自洽与归一化/README.md"
P = os.path.join(REPO, RP.replace("/", os.sep))
STAGE = len(sys.argv) > 1 and sys.argv[1] == "stage"

B = ("TUFT-r257_同一运动定理卷_单一运动公设求导统一力方程_"
     "传播子双路机导与符号定理与磁投影_耦合不可导反定理与十六格穷举矩阵_"
     "精算与可视化_2026-10-31")

L_SRC = (
    "│   ├── " + B + ".py  # 新增（**r257 · 2026-10-31**）："
    "**同一运动定理卷（★新层）——把用户命题「力的大统一是在同一个运动里面」公理化并定理化**"
    "（条目 **20**：PASS 12 / FAIL 2 / BOUNDARY 1 / INFO 5；**控制组 6/6**、**守卫 6/6**、退出码 0；"
    "方法全谱 10 道工序）。★公设集 P1–P4（单速 c / 单一传播子 / 三旋钮 (s,m,g) / ℏ）双路机器导出"
    "**统一力方程 V₁₂(r;s,m,g)=(−1)^(s+1)·g₁g₂·e^(−mr)/4πr**：路一 QFT KG 传播子三重校验"
    "（齐次残差 9.1e-05 / Gauss 通量 1.000000 / Fourier Richardson rel 8.8e-04）、"
    "路二 经典场方程 (∇²−m²)φ=−gδ³ 独立同式（通量 1.000000 + e^{+mr} 无界排除）——两路独立汇合同一闭式。"
    "★验证矩阵全现算：**GW170817 同速 1.74s/40Mpc ⇒ |Δv|/v ≤ 4.23e-16**（引力与光同一运动速度的最强实测）、"
    "符号定理 (−1)^(s+1) 三物理事实对拍、磁投影 (v/c)²、α=CODATA 全链条 rel 6.1e-10、"
    "g=m√(4πG) 识别精确还原牛顿（rel 0）、λ_W=2.4550e-18 m、λ_π=1.4138 fm。"
    "★反定理钉死边界：①定义恒等式陷阱机证——g=ℏ^a c^b κ^d ω^e m^f 量纲解族 (a,b) 自由，"
    "任取 (1,0)/(0,1) 两族都能反解出 g=1/137 ⇒ 同一运动几何对耦合值**判别力 0 bit**（r250 定理推广）；"
    "②SM 单圈三耦合最优标度 2.39e14 GeV 处 spread 8.6%（×1.09）『近交』但两两交点"
    " 1.0e13/2.4e14/9.7e16 GeV 相跨 3 个数量级 ⇒ 精确『同一耦合』机算排除。"
    "★十六格穷举：形状 3.5/4 · 方向 4/4 · 距离 4/4 · 大小 0/4 ⇒ **结构层 11.5/12 机验统一，"
    "大小层 0/4 开放**——「同一个运动」统一律（形状/方向/距离/速度）不统一常数（大小）。"
    "开发期自抓 8 处（verdict 括号错配复现 / 弱力程单位换算错 10 倍 / 经典路通量取点错 / "
    "cross() 漏乘 2π（修正后揭示『近交≠交汇』的更锋利真结果）/ C1·C2 格式串优先级与占位 / "
    "CTL1 阈值过严 / G1 校验方式 / λ_π 单位）——全部由守卫/控制组先行抓出后修复，未带病落盘。"
)

L_VD = (
    "├── 判定_" + B + ".md  # 新增（**r257 · 2026-10-31**）：同一运动定理卷判定册 —— "
    "§判词 · §判决分组（A 公设集 / B 双路求导 / C 逐力精算 / D 反定理 / E 十六格穷举 / F 完成度）· "
    "§★性质界定四条（对命题是「定理化」不是「背书」；双路推导独立；反定理一不依赖实验输入；"
    "GW170817 界为现算非引用）· §治理（判定册按 r241/r246 惯例落 `判定/`）。"
)

L_INC = (
    "- **r257（2026-10-31）· 同一运动定理卷（★新层）**：命题「力的大统一是在同一个运动里面」定理化。"
    "条目 20（PASS 12 / FAIL 2 / BOUNDARY 1 / INFO 5），控制组 6/6，守卫 6/6，rc=0；"
    "源码 [`TUFT-r257_…py`](源码/" + B + ".py)；"
    "判定册 [`判定_TUFT-r257_…md`](判定/判定_" + B + ".md)；数据 [`…json`](数据/" + B + ".json)。"
    "★单一运动公设集双路导出统一力方程 V=(−1)^(s+1)g₁g₂e^(−mr)/4πr；"
    "**十六格穷举：形状 3.5/4·方向 4/4·距离 4/4·大小 0/4 ⇒ 结构层 11.5/12 机验统一**；"
    "★GW170817 同速现算 4.23e-16；★反定理：判别力 0 bit + 单圈近交（8.6%）但交点相跨 3 数量级"
    " ⇒ 同一运动统一律不统一常数（J32 0/7 的结构性根源）。"
)

L_SEC = """

### r257 · 2026-10-31 · 同一运动定理卷：单一运动公设求导统一力方程（★新层 · ★方法全谱 10 道工序）

- **产物**：源码 [`TUFT-r257_…py`](源码/__B__.py) / [`…html`](源码/__B__.html)；数据 [`…json`](数据/__B__.json) / [`…md`](数据/__B__.md) / [`…_report.txt`](数据/__B___report.txt)；判定册 [`判定_TUFT-r257_…md`](判定/判定___B__.md)；runner `源码/_run_r257.py` → `源码/_out_r257.txt`
- **复现**：`python -X utf8 源码\\TUFT-r257_…py` ⇒ **rc=0**，条目 **20**（**PASS 12 / FAIL 2 / BOUNDARY 1 / INFO 5**），**控制组 6/6**，**守卫 6/6**。开发期自抓 8 处（详见源码树条目注文），全部由守卫/控制组先行抓出后修复重跑，未带病落盘。
- **结论一句话**：**「力的大统一是在同一个运动里面」在结构层成立并被定理化——单一运动公设集双路导出统一力方程，十六格中形状/方向/距离 11.5/12 格机验统一、GW170817 同速至 4.23e-16；但大小层 4 格零供给（判别力 0 bit 定理 + 单圈近交不交汇）——同一运动统一律，不统一常数。**
- **★应用户指令**：「用尽一切方法，一切逻辑，一切思维，一切假设，无穷新处理方式，求导证明验证精算出统一场论方程，力的大统一是在同一个运动里面」——本卷 10 道工序：命题入档 / 量纲机读 / 双路闭式推导 / 数值微分 / 振荡积分（Richardson 外推）/ Gauss 通量 / Decimal 50 位 / 符号表机检 / 十六格穷举矩阵 / 守卫链自审。
- **与并行链 r248–r256 的分层（不可相加）**：本卷只用 J51 已闭环的传播子形状层与全库已定判决，不使用 r248 已判死的主方程分支、r244 已判死的类光 Frenet 标架——同一运动命题在传播子层独立成立/独立定界（A4 条目如实登记）。
- **取号**：2026-10-31 实测三树最大占用 **r256** ⇒ 取 **r257**（G4 守卫「非本卷 *r257* = 0」机读复核）；登记时并行链已推进至 r258（动态锚点随树上现行最大号）。**下轮从 r259 复查起**。
- **治理**：本卷无外来靶文件（靶 = 用户命题 + 全库既有判决链，命题逐字入档 A1/G1）；未改 `verify.py`；未跑 `refresh_catalog.py`；git 由收口提交统一处理（分域暂存，并行登记行留工作区）；**本卷条目不可与 r142–r256 相加**。
- **收尾巡检（verify.py，2026-10-31）**：**FAIL 402 项**，分层归因——**368 项来自并行线**（源码/_scratch_dead/ 快照迁移：旧 README 快照以相对路径引用已移文件）；**34 项为开工前历史遗留**（目录命名 x1、r243-r245 判定册断链 x6、attack 断链 x16、r258 数据断链等）；**r257 相关 = 0**（本卷判定册按 r241/r246 惯例落 判定/、链接自洽；无来料原件）。未改 verify.py；未跑 refresh_catalog.py。
""".replace("__B__", B).replace("___B__", B)

if STAGE:
    head = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + RP],
                          stdout=subprocess.PIPE).stdout.decode("utf-8")
    lines = head.split("\n")
else:
    lines = io.open(P, "r", encoding="utf-8").read().split("\n")

# 动态锚点：三类行中现行最大 r 号
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
    io.open(os.path.join(REPO, "_tmp_readme_r257_stage.md"), "w",
            encoding="utf-8").write(out)
    print("STAGE 版构建：锚 src=r%d vd=r%d inc=r%d；行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
else:
    io.open(P, "w", encoding="utf-8").write(out)
    print("README r257 登记：锚 src=r%d vd=r%d inc=r%d；总行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
