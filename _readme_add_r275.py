# -*- coding: utf-8 -*-
"""README 登记 r275：动态锚点 + 文末增量章节。用法：python _readme_add_r275.py [stage]"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\a10\aikjx\code\my_lib\openuft"
RP = "04_公共成果/本项目_全维自洽与归一化/README.md"
P = os.path.join(REPO, RP.replace("/", os.sep))
STAGE = len(sys.argv) > 1 and sys.argv[1] == "stage"

B = ("TUFT-r275_全链路自洽审计_六层链路状态总账_"
     "缪子氢Uehling真空极化数值积分与预测盈余账本_"
     "精算与可视化_2026-10-31")

L_SRC = (
    "│   ├── " + B + ".py  # 新增（**r275 · 2026-10-31**）："
    "**全链路自洽审计（★新层 · 自驱轮）——靶 = r257/r261/r263/r269/r271 建立的"
    "『螺旋-α 新理论体系』链路本身（无用户来料，比照检查点 Next Steps 项 3）**"
    "（条目 **13**：PASS 9 / FAIL 1 / BOUNDARY 1 / INFO 2；**控制组 6/6**、**守卫 6/6**、退出码 0）。"
    "★六层链路复跑全绿（L1 运动学 ω²=c²(κ²+τ²) 三半径 rel ~1e-16 / L2 全参数化 / "
    "L3 三维剪枝复跑 / L4 候选∞路 / L5 不变量条件链 200 组 boost 快检 / "
    "L6 动力学否定复跑 / L7 GW170817 因子 6.30e10 复算）；"
    "★**两块新计算（L9 多体系 α 链）**：①缪子氢玻尔半径 a_μH=ħc/(α m_r c²)=284.748 fm"
    "（约化质量 m_r=94.9645 MeV 链，文献 ~284.7 fm ✓）②**Uehling 真空极化 ⟨2P−2S⟩ 数值积分 "
    "= 204.984 meV vs 点质子兰姆移位 206.0336 meV（Antognini 2011，web 核实）rel 5.1e-3**"
    "（一阶 α 主项，缺 SE/Källen-Sabry 层内；t=cosh u 换元消奇性 + 双 Simpson，"
    "径向归一化自检 1e-8；本库第一块 QED 一性数值）；跃迁能公式机算 206.2948 meV "
    "vs CREMA 实测 206.2949（rel 3.8e-7）——同一 α 贯穿电子氢/缪子氢，多体系一致 ✓。"
    "★**体系级总账（本卷核心）**：①L8 QED 兼容硬缺口（B4 FAIL）——VP 是点质子兰姆移位主项"
    "（99.49%）而固定几何比值 K₁/K₂=Zα/n 无尺度机制（r250），兼容义务被定量锁定："
    "任何候选动力学必须先重现 (α/π) 阶短程势及其 nL 依赖；②L10 预测盈余总账（B5）——"
    "全部存活分支（条件链/场结构/万物同螺旋）净预测盈余 **0 bit**，突破唯一入口 = "
    "L6 供给有物理根据的协变作用量（r229 0 供给）——五线互证升级为体系级总账。"
    "★链路状态表 L1–L10 十节点全部有机器状态，无未标定链路；G1 机读四份前置判定册指纹。"
    "开发期自抓 3 处（A1 复跑机检参数化错误——残差 48 直接暴露 / CTL4 量纲链 ħc 漏 M¹ ×2 次）"
    "——全部修复后重跑全绿，未带病落盘。"
)

L_VD = (
    "├── 判定_" + B + ".md  # 新增（**r275 · 2026-10-31**）：全链路自洽审计判定册 —— "
    "§判词 · §判决分组（A 六层复跑 / B 新计算与总账 / C 状态表与治理）· "
    "§★性质界定四条（B4 是兼容义务清单第一条定量条目；B5 盈余账本是体系级判定；"
    "Uehling 是本库第一块 QED 一性数值；自驱轮靶定义）· §治理（判定册落 `判定/`）。"
)

L_INC = (
    "- **r275（2026-10-31）· 全链路自洽审计（★新层 · 自驱轮）**：靶 = 新体系链路本身"
    "（无用户来料）。条目 13（PASS 9 / FAIL 1 / BOUNDARY 1 / INFO 2），控制组 6/6，守卫 6/6，rc=0；"
    "源码 [`TUFT-r275_…py`](源码/" + B + ".py)；"
    "判定册 [`判定_TUFT-r275_…md`](判定/判定_" + B + ".md)。"
    "★新计算：缪子氢 a_μH=284.748 fm + **Uehling ⟨2P−2S⟩=204.984 meV 数值积分"
    "（vs 206.0336 rel 5.1e-3）**——多体系 α 链一致 ✓；"
    "★体系级总账：L8 VP 兼容硬缺口定量锁定（99.49% 主项无机制）+ L10 净预测盈余 0 bit——"
    "突破唯一入口 = 协变作用量供给（L6，r229 0 供给）。"
    "取号实测最大 r274 ⇒ r275。"
)

L_SEC = """

### r275 · 2026-10-31 · 全链路自洽审计：六层链路状态总账 L1–L10（★新层 · 自驱轮）

- **产物**：源码 [`TUFT-r275_…py`](源码/__B__.py) / [`…html`](源码/__B__.html)；数据 [`…json`](数据/__B__.json) / [`…md`](数据/__B__.md) / [`…_report.txt`](数据/__B___report.txt)；判定册 [`判定_TUFT-r275_…md`](判定/判定___B__.md)；runner `源码/_run_r275.py` → `源码/_out_r275.txt`
- **复现**：`python -X utf8 源码\\TUFT-r275_…py` ⇒ **rc=0**，条目 **13**（**PASS 9 / FAIL 1 / BOUNDARY 1 / INFO 2**），**控制组 6/6**，**守卫 6/6**。开发期自抓 3 处（A1 复跑参数化 / CTL4 量纲链），修复后重跑全绿。
- **结论一句话**：**螺旋-α 新体系十节点链路全部获得机器状态（L1–L10）：六层复跑全绿 + 新计算缪子氢 Uehling ⟨2P−2S⟩=204.984 meV（vs 206.0336，rel 5.1e-3，本库第一块 QED 一性数值）+ 多体系 α 链一致——体系级总账：VP 兼容硬缺口定量锁定（99.49% 主项无尺度机制）+ 净预测盈余 0 bit，突破唯一入口 = 协变作用量供给（L6）。**
- **与前置卷的关系**：L1/L2→r58/r261/r263；L3/L4→r269/r271；L5→r271；L6→r271/r250/r229；L7→r263；L8/L9/L10→本卷新计算；本卷只做汇总复跑与新计算，不重复前置推导。
- **取号**：2026-10-31 实测三树最大占用 **r274** ⇒ 取 **r275**（G4 机读复核）。**下轮从 r276 复查起**。
- **治理**：自驱轮无来料（靶 = 链路本身）；四份前置判定册在盘（G1 指纹）；未改 `verify.py`；未跑 `refresh_catalog.py`；git 由收口提交统一处理（分域暂存）；**本卷条目不可与 r142–r274 相加**。
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
    io.open(os.path.join(REPO, "_tmp_readme_r275_stage.md"), "w",
            encoding="utf-8").write(out)
    print("STAGE 版构建：锚 src=r%d vd=r%d inc=r%d；行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
else:
    io.open(P, "w", encoding="utf-8").write(out)
    print("README r275 登记：锚 src=r%d vd=r%d inc=r%d；总行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
