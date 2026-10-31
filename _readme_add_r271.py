# -*- coding: utf-8 -*-
"""README 登记 r271：动态锚点 + 文末增量章节。用法：python _readme_add_r271.py [stage]"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\a10\aikjx\code\my_lib\openuft"
RP = "04_公共成果/本项目_全维自洽与归一化/README.md"
P = os.path.join(REPO, RP.replace("/", os.sep))
STAGE = len(sys.argv) > 1 and sys.argv[1] == "stage"

B = ("TUFT-r271_时空曲率比攻坚_K1除K2等于beta洛伦兹不变_"
     "时空不变量复现与2000组boost机检与三维候选剪枝定理_"
     "精算与可视化_2026-10-31")

L_SRC = (
    "│   ├── " + B + ".py  # 新增（**r271 · 2026-10-31**）："
    "**时空曲率比攻坚审计（★新层）——靶为用户附件《ROOT V7.0·精细结构常数与螺旋曲率挠率攻坚》"
    "（逐字留档；四份靶中最硬的一份）**"
    "（条目 **12**：PASS 8 / FAIL 1 / BOUNDARY 1 / INFO 2；**控制组 6/6**、**守卫 6/6**、退出码 0）。"
    "★own 重做文档全部机器检验并命中：半经典消元 v=K/L ⇒ v/c=Zα/n（力平衡残差 ~1e-16）；"
    "时空曲率 K₁=γ²β²/r、K₂=γ²β/r 数值复现（K₁ rel ~1e-7、K₂ rel ~1e-7，CODATA 2022 层；"
    "r_model=a₀/γ 定义反推命中）；**K₁/K₂=β=v/c 恒等（与 r 无关，r→10r 比值 rel 1.2e-16）**；"
    "三维观察者公式 κ_3D/|τ_3D|=β/(γ_Bβ_B)（U/c=0.6→0.009729803 ✓，rel 4.3e-8）"
    "+ 观察者系投影曲线数值级联微分独立对拍（rel 3.6e-7）；"
    "**2000 组随机 boost 洛伦兹不变性 own 实验**（β_U∈0.05–0.95 方向均匀："
    "max K₁ rel 9.2e-8、K₂ rel 6.0e-5——浮点非线性放大层，远小于 10⁻³ 物理判别层）；"
    "二次能量否定定理机检（dE/dθ=(ω²/c²)(A−B)sin2θ：A≠B 内区 0 穿越即无内驻点、"
    "A=B 全简并——文档『受限二次能量无法自行决定 θ=arctanα』成立）；"
    "经典辐射 P=4.6695e-8 W（靶 4.66929e-8，rel 5.3e-5）、时标 4.668e-11 s。"
    "★**三维候选剪枝定理（本卷定理化，B1 FAIL）**：三维 κ/|τ| 随观察者速度连续漂移"
    "（β_B 扫描 0.2→0.03575…0.95→0.00240；β_B=1/√2 平凡穿越 α）⇒ r269 六候选"
    "（全部三维读法）**非洛伦兹不变、非普适**——r269 多元性问题的第一把物理剃刀："
    "候选必须重构在时空不变量层；剪枝后边界（B2）：不变量层候选仍 ∞ 路（K₁/K₃ 等高阶组合）——"
    "层升级非终点；α 仍是输入非输出（B4，五线互证：r257-D1/r261-D1/r263-C2/r269-B1/本卷）。"
    "★文档自评『条件性证明已完成；普适 α 第一性预测开放』与本库判定链一致；"
    "核验表 8 通过 ↔ A1–A6 对齐、2 未完成 ↔ r229 供给 0 + J32 0/7；"
    "辅助螺旋读法（ct 纵轴时空表示非真实轨迹）= 四靶中第一次把候选从本体承诺降为表示选择——"
    "与 r263-B2 场结构读法相容且更严格（不变量化）。"
    "开发期自抓 2 处（G1 token 千分位格式 2,187,691.262 / A5 证据『机器精度层』表述与实测 "
    "6e-5 不符如实改写为非线性放大归因）——修复后重跑全绿，未带病落盘。"
)

L_VD = (
    "├── 判定_" + B + ".md  # 新增（**r271 · 2026-10-31**）：时空曲率比攻坚审计判定册 —— "
    "§判词 · §判决分组（A 复现 6 条 / B 剪枝定理与边界 / C 独立重验与治理）· "
    "§★性质界定四条（剪枝是 r269 后实质推进；剪枝≠闭合；own 重验纪律；"
    "辅助螺旋读法的治理意义=本体承诺降为表示选择）· §治理（判定册落 `判定/`）。"
)

L_INC = (
    "- **r271（2026-10-31）· 时空曲率比攻坚审计（★新层）**：靶 = 用户附件《ROOT V7.0》"
    "（逐字留档）。条目 12（PASS 8 / FAIL 1 / BOUNDARY 1 / INFO 2），控制组 6/6，守卫 6/6，rc=0；"
    "源码 [`TUFT-r271_…py`](源码/" + B + ".py)；"
    "判定册 [`判定_TUFT-r271_…md`](判定/判定_" + B + ".md)；"
    "来料留档 [`…_来料原件_用户附件逐字_2026-10-31.md`](数据/TUFT-r271_时空曲率比攻坚_K1除K2等于beta洛伦兹不变_三维候选剪枝定理与二次能量否定_来料原件_用户附件逐字_2026-10-31.md)。"
    "★K₁/K₂=β 洛伦兹不变复现 + 2000 组 boost own 机检；"
    "★**三维候选剪枝定理**：三维候选全部非洛伦兹不变（r269 多元性第一把物理剃刀），"
    "候选重构于时空不变量层但仍 ∞ 路（层升级非终点）；五线互证（α 仍输入）；"
    "二次能量否定定理机检。取号实测最大 r270 ⇒ r271。"
)

L_SEC = """

### r271 · 2026-10-31 · 时空曲率比攻坚审计：K₁/K₂=β 洛伦兹不变与三维候选剪枝定理（★新层）

- **产物**：源码 [`TUFT-r271_…py`](源码/__B__.py) / [`…html`](源码/__B__.html)；数据 [`…json`](数据/__B__.json) / [`…md`](数据/__B__.md) / [`…_report.txt`](数据/__B___report.txt)；判定册 [`判定_TUFT-r271_…md`](判定/判定___B__.md)；来料留档 [`数据/TUFT-r271_…_来料原件_用户附件逐字_2026-10-31.md`](数据/TUFT-r271_时空曲率比攻坚_K1除K2等于beta洛伦兹不变_三维候选剪枝定理与二次能量否定_来料原件_用户附件逐字_2026-10-31.md)；runner `源码/_run_r271.py` → `源码/_out_r271.txt`
- **复现**：`python -X utf8 源码\\TUFT-r271_…py` ⇒ **rc=0**，条目 **12**（**PASS 8 / FAIL 1 / BOUNDARY 1 / INFO 2**），**控制组 6/6**，**守卫 6/6**。开发期自抓 2 处（G1 token 千分位 / A5 证据表述如实化），修复后重跑全绿。
- **结论一句话**：**靶把候选从三维几何升级到时空不变量（K₁/K₂=β 洛伦兹不变，own 2000 组 boost 机检通过）——本卷定理化「三维候选剪枝定理」：三维螺旋候选全部随观察者漂移、非普适（r269 多元性第一把物理剃刀），但不变量层候选仍 ∞ 路、α 仍是输入非输出（五线互证）——靶自评『条件性证明完成、第一性预测开放』与本库判定链完全一致。**
- **与 r257/r261/r263/r269 的关系**：判别力问题五线互证补全——r257-D1（量纲反解）、r261-D1（映射方向）、r263-C2（几何不选值）、r269-B1（候选无穷性）、本卷 B1（三维层剪枝）+B2（不变量层仍开放）。
- **取号**：2026-10-31 实测三树最大占用 **r270** ⇒ 取 **r271**（G4 机读复核）。**下轮从 r272 复查起**。
- **治理**：靶 = 用户附件逐字留档（sha256=180001AA…）；未改 `verify.py`；未跑 `refresh_catalog.py`；git 由收口提交统一处理（分域暂存）；**本卷条目不可与 r142–r270 相加**。
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
    io.open(os.path.join(REPO, "_tmp_readme_r271_stage.md"), "w",
            encoding="utf-8").write(out)
    print("STAGE 版构建：锚 src=r%d vd=r%d inc=r%d；行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
else:
    io.open(P, "w", encoding="utf-8").write(out)
    print("README r271 登记：锚 src=r%d vd=r%d inc=r%d；总行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
