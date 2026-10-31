# -*- coding: utf-8 -*-
"""README 登记 r269：动态锚点 + 文末增量章节。用法：python _readme_add_r269.py [stage]"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\a10\aikjx\code\my_lib\openuft"
RP = "04_公共成果/本项目_全维自洽与归一化/README.md"
P = os.path.join(REPO, RP.replace("/", os.sep))
STAGE = len(sys.argv) > 1 and sys.argv[1] == "stage"

B = ("TUFT-r269_候选比例多元性定理_tanθ与sinθ候选互斥_"
     "κ除τ推导机检与550nm四位复现与玻尔圆轨道τ等于零反例_六候选穷举_"
     "精算与可视化_2026-10-31")

L_SRC = (
    "│   ├── " + B + ".py  # 新增（**r269 · 2026-10-31**）："
    "**候选比例多元性定理（★新层）——靶为用户附件《α 作为螺旋曲率与挠率之比》"
    "（逐字留档；连续第三份全正确分析）**"
    "（条目 **12**：PASS 7 / FAIL 2 / INFO 3；**控制组 6/6**、**守卫 6/6**、退出码 0）。"
    "★数字复现 7/7 全对：κ/|τ|=R|ω|/|u|=v_⊥/|v_z| 恒等式机检（rel ~1e-16）、"
    "三比例表（tanθ/sinθ/cotθ）确认、tanθ 分支三位（θ=0.41810008°、v_⊥/c=0.0072971583、"
    "|u|/c=0.9999733754）、550 nm 四位（R=0.638758 nm、H=549.985356 nm、"
    "κ=83,362.54 m⁻¹、|τ|=11,423,669.13 m⁻¹）。"
    "★**候选多元性定理（本卷核心）**：r263 靶假设 sinθ=α、本靶假设 tanθ=α——"
    "两个都「数学上自洽」却互斥（sinθ=tanθ ⇒ θ=0 ⇒ α=0）；机器枚举 6 个可逆几何函数候选"
    "（sin/tan/cot/tan(θ/2)/sin²/tan(θ/2)=f/2）全部命中 1/137.036 且两两互斥"
    "（最小角距 >0）⇒ 候选无穷多、选择问题 **∞ 路**——r257-D1「判别力 0 bit」的"
    "**第三种独立证明（候选无穷性）**（r261-D1 映射方向、r263-C2 障碍一为前两线，四线互证）。"
    "★玻尔圆轨道反例机检：τ=0 ⇒ κ/|τ|=∞≠α——文档 §四 核心论点成立，"
    "杀死一切『v/c=α ⇒ κ/τ=α』滑移；诚实声明四项照登（连续第二轮全诚实靶）。"
    "★取号事件如实登记：首扫最大 r267 ⇒ 取 r268 落盘引擎（16:31:13），"
    "并行会话 16:31:15 亦落 r268 引擎（竞态窗口 2 s）——为守号位唯一性治理不变量，"
    "本卷**让号改取 r269**（改写时实测最大 r268；G4 机读复核非本卷 *r269*=0）。"
    "开发期自抓 5 处（verdict 括号第六现+append 双参第六现同轮预修 / B1 百分号优先级 / "
    "CTL5 百分号优先级 / **sin² 候选实现缺陷由 CTL3 控制组抓出**（sqrt(f²)=f 恒坍缩到 "
    "sinθ 候选）/ ent 括号修复引入即抓）——全部修复后重跑，未带病落盘。"
)

L_VD = (
    "├── 判定_" + B + ".md  # 新增（**r269 · 2026-10-31**）：候选比例多元性定理判定册 —— "
    "§判词 · §判决分组（A 复现 / B 多元性定理 / C 反例与诚实 / D 四线互证与正向通道 / E 汇总）· "
    "§★性质界定四条（FAIL 判『唯一候选』非靶分析；多元性是构造性证明；连续第四轮验证通过；"
    "正向通道=几何零供给唯一天窗）· §治理（判定册落 `判定/`）。"
)

L_INC = (
    "- **r269（2026-10-31）· 候选比例多元性定理（★新层）**：靶 = 用户附件《α 作为螺旋曲率与挠率之比》"
    "（逐字留档）。条目 12（PASS 7 / FAIL 2 / INFO 3），控制组 6/6，守卫 6/6，rc=0；"
    "源码 [`TUFT-r269_…py`](源码/" + B + ".py)；"
    "判定册 [`判定_TUFT-r269_…md`](判定/判定_" + B + ".md)；"
    "来料留档 [`…_来料原件_用户附件逐字_2026-10-31.md`](数据/TUFT-r269_候选比例多元性定理_tanθ与sinθ候选互斥_来料原件_用户附件逐字_2026-10-31.md)。"
    "★六候选穷举全自洽全互斥 ⇒ 选择问题 ∞ 路（r257-D1 判别力 0 bit 的候选无穷性证明，四线互证）；"
    "r263 sinθ 候选与本靶 tanθ 候选互斥实例化；玻尔 τ=0 反例机检；数字复现 7/7。"
    "取号事件：r268 竞态（窗口 2 s）⇒ 本卷让号 r269（守号位唯一性）。"
)

L_SEC = """

### r269 · 2026-10-31 · 候选比例多元性定理：tanθ 与 sinθ 候选互斥（★新层 · r257-D1 判别力 0 bit 的候选无穷性证明）

- **产物**：源码 [`TUFT-r269_…py`](源码/__B__.py) / [`…html`](源码/__B__.html)；数据 [`…json`](数据/__B__.json) / [`…md`](数据/__B__.md) / [`…_report.txt`](数据/__B___report.txt)；判定册 [`判定_TUFT-r269_…md`](判定/判定___B__.md)；来料留档 [`数据/TUFT-r269_…_来料原件_用户附件逐字_2026-10-31.md`](数据/TUFT-r269_候选比例多元性定理_tanθ与sinθ候选互斥_来料原件_用户附件逐字_2026-10-31.md)；runner `源码/_run_r269.py` → `源码/_out_r269.txt`
- **复现**：`python -X utf8 源码\\TUFT-r269_…py` ⇒ **rc=0**，条目 **12**（**PASS 7 / FAIL 2 / INFO 3**），**控制组 6/6**，**守卫 6/6**。开发期自抓 5 处（含 CTL3 控制组抓出 sin² 候选实现缺陷），全部修复后重跑，未带病落盘。
- **结论一句话**：**靶分析 7/7 全对（连续第三份全正确分析）；但「α=κ/|τ|」与 r263 的「α=sinθ」两个都自洽却互斥——机器枚举 6 个可逆函数候选全部命中 1/137.036 且两两互斥 ⇒ 候选无穷多、几何候选族对 α 的选择问题是 ∞ 路（r257-D1 判别力 0 bit 的第三种独立证明）；玻尔圆轨道 τ=0 反例杀死一切『v/c=α ⇒ κ/τ=α』滑移——出路唯在独立 ROOT 动力学（正向通道登记，当前 0 供给）。**
- **取号事件（治理档）**：首扫最大 r267 ⇒ 取 r268 并落盘引擎（16:31:13）；并行会话 16:31:15 亦落 r268 引擎（竞态窗口 2 s）。为守「号位唯一」治理不变量，本卷让号改取 r269；r268 归并行会话卷（ROOT-V5.0 融合审计）。**下轮从 r270 复查起**。
- **与 r257/r261/r263 的关系**：判别力 0 bit 四线互证——r257-D1（量纲反解）、r261-D1（映射方向）、r263-C2（几何不选值）、本卷 B1（候选无穷性）。
- **治理**：靶 = 用户附件逐字留档（sha256=A63740CE…）；未改 `verify.py`；未跑 `refresh_catalog.py`；git 由收口提交统一处理（分域暂存）；**本卷条目不可与 r142–r268 相加**。
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
    io.open(os.path.join(REPO, "_tmp_readme_r269_stage.md"), "w",
            encoding="utf-8").write(out)
    print("STAGE 版构建：锚 src=r%d vd=r%d inc=r%d；行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
else:
    io.open(P, "w", encoding="utf-8").write(out)
    print("README r269 登记：锚 src=r%d vd=r%d inc=r%d；总行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
