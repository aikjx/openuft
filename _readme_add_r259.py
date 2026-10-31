# -*- coding: utf-8 -*-
"""README 登记 r259：动态锚点（树上现行最大号行之后插入）+ 文末增量章节
用法：python _readme_add_r259.py [stage]"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\a10\aikjx\code\my_lib\openuft"
RP = "04_公共成果/本项目_全维自洽与归一化/README.md"
P = os.path.join(REPO, RP.replace("/", os.sep))
STAGE = len(sys.argv) > 1 and sys.argv[1] == "stage"

B = ("TUFT-r259_同一运动动力学层_辐射与自旋自旋的c幂阶梯定理_"
     "拉莫尔与四极与21cm超精细现算_Darwin首阶与二十四格穷举_"
     "精算与可视化_2026-10-31")

L_SRC = (
    "│   ├── " + B + ".py  # 新增（**r259 · 2026-10-31**）："
    "**同一运动动力学层（★新层）——r257 静态谱定理化的时间依赖面延伸**"
    "（条目 **14**：PASS 7 / FAIL 2 / BOUNDARY 1 / INFO 4；**控制组 6/6**、**守卫 6/6**、退出码 0）。"
    "★c-幂阶梯定理（量纲机导）：**P ∝ c^{−(2s+1)}——s=1 Larmor c⁻³、s=2 四极 c⁻⁵，c 幂次由自旋唯一决定**"
    "（P=[ML²T⁻³] 对 (C,a,c) 枚举解出；阶梯机检 c→2c ⇒ P/8 rel 0.00e+00）。"
    "★三大现算：Larmor P=5.708e-24 W（电子 a=1e15）；**Hulse-Taylor 全参数现算 "
    "Ṗ_b=−2.4020e-12 vs 观测 −2.4056e-12（rel 0.148%，M_c=1.2307 M☉）**——c⁻⁵ 的 s=2 档被双星脉冲星钉在 0.1%；"
    "**21cm 氢超精细费米接触全 CODATA 现算 1422.81 MHz vs 实测 1420.405751（rel 1.69e-3，残余=QED 修正登记）**"
    "——与磁力 (v/c)² 同一磁相互作用的自旋-自旋投影。Darwin/Breit 首阶 (v/c)² 与磁投影同源。"
    "★四层同源：静态 Yukawa → 速度投影 → 辐射 → 自旋-自旋，共用一个格林函数与一个 c，无额外公设。"
    "★二十四格穷举：形状 3.5 · 方向 4 · 距离 4 · 大小 0 · 辐射 2 · 自旋-自旋 1 ⇒ "
    "**可测格 3/3 全绿**；弱/强的经典辐射为**范畴错位**（W/Z 衰变是粒子过程、胶子禁闭）如实登记。"
    "★反定理延伸：辐射 P∝g⁴、超精细 ΔE∝g_e g_p——大小层在动力学层同样 0 供给"
    "（同一运动统一动力学的『形』不统一『率』）。"
    "开发期自抓 5 处（append 双参笔误 / verdict 括号错配第三现 / c→C 大小写 / CTL1 阈值恰卡 >1.0 / "
    "M_c kg-M☉ 单位标签）——全部由守卫先行抓出后修复，未带病落盘。"
)

L_VD = (
    "├── 判定_" + B + ".md  # 新增（**r259 · 2026-10-31**）：同一运动动力学层判定册 —— "
    "§判词 · §判决分组（A 命题延续 / B 动力学三大现算 / C 二十四格 / D 反定理延伸 / E 开放通道 / F 完成度）· "
    "§★性质界定四条（r257 延伸非新命题；现算输入分层诚实；D2 是范畴登记不是攻击；"
    "c-阶梯量纲机导不依赖实验）· §治理（判定册落 `判定/`）。"
)

L_INC = (
    "- **r259（2026-10-31）· 同一运动动力学层（★新层）**：r257 的时间依赖面延伸。"
    "条目 14（PASS 7 / FAIL 2 / BOUNDARY 1 / INFO 4），控制组 6/6，守卫 6/6，rc=0；"
    "源码 [`TUFT-r259_…py`](源码/" + B + ".py)；"
    "判定册 [`判定_TUFT-r259_…md`](判定/判定_" + B + ".md)；数据 [`…json`](数据/" + B + ".json)。"
    "★**c-幂阶梯定理 P∝c^{−(2s+1)}**（s=1 Larmor c⁻³ / s=2 四极 c⁻⁵，阶梯机检精确 /8）；"
    "**Hulse-Taylor 现算 rel 0.148%**、**21cm 现算 1422.81 vs 1420.405751 MHz（rel 1.69e-3）**；"
    "**二十四格：可测格 3/3 全绿**（辐射 2 + 自旋-自旋 1），弱/强经典辐射范畴错位登记；"
    "反定理延伸：动力学层大小同样 0 供给。"
)

L_SEC = """

### r259 · 2026-10-31 · 同一运动动力学层：辐射与自旋-自旋的 c-幂阶梯定理（★新层 · r257 动力学延伸）

- **产物**：源码 [`TUFT-r259_…py`](源码/__B__.py) / [`…html`](源码/__B__.html)；数据 [`…json`](数据/__B__.json) / [`…md`](数据/__B__.md) / [`…_report.txt`](数据/__B___report.txt)；判定册 [`判定_TUFT-r259_…md`](判定/判定___B__.md)；runner `源码/_run_r259.py` → `源码/_out_r259.txt`
- **复现**：`python -X utf8 源码\\TUFT-r259_…py` ⇒ **rc=0**，条目 **14**（**PASS 7 / FAIL 2 / BOUNDARY 1 / INFO 4**），**控制组 6/6**，**守卫 6/6**。开发期自抓 5 处（详见源码树条目注文），全部由守卫/控制组先行抓出后修复重跑，未带病落盘。
- **结论一句话**：**c-幂阶梯定理（P∝c^{−(2s+1)}）把『同一个运动』从静态谱推进到辐射与自旋-自旋——Larmor 精确机检（/8 rel 0）、Hulse-Taylor 现算 0.148%、21cm 现算 1.69e-3，可测格 3/3 全绿；弱/强经典辐射为范畴错位；大小层反定理原样成立。**
- **与 r257 的关系**：同一命题、同一公设集（P1–P4），新增的只是时间依赖面——四个动力学面（静态/速度/辐射/自旋-自旋）共用一个格林函数与一个 c（B5 条目），无额外公设。
- **取号**：2026-10-31 实测三树最大占用 **r258** ⇒ 取 **r259**（G4 机读复核）；登记动态锚点随树上现行最大号。**下轮从 r260 复查起**。
- **治理**：本卷无外来靶文件（靶 = r257 命题的动力学层延伸）；未改 `verify.py`；未跑 `refresh_catalog.py`；git 由收口提交统一处理（分域暂存）；**本卷条目不可与 r142–r258 相加**。
- **收尾巡检（verify.py，2026-10-31）**：FAIL 402 项，分层归因——368 项来自并行线（源码/_scratch_dead/ 快照迁移）；34 项为开工前历史遗留（目录命名 x1、r243-r245 判定册断链 x6、attack 断链 x16、r258 数据断链等）；**r259 相关 = 0**（本卷判定册按惯例落 判定/、链接自洽、无来料原件）。本轮自产临时件（README 分域暂存副本）已清理。未改 verify.py；未跑 refresh_catalog.py。
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
    io.open(os.path.join(REPO, "_tmp_readme_r259_stage.md"), "w",
            encoding="utf-8").write(out)
    print("STAGE 版构建：锚 src=r%d vd=r%d inc=r%d；行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
else:
    io.open(P, "w", encoding="utf-8").write(out)
    print("README r259 登记：锚 src=r%d vd=r%d inc=r%d；总行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
