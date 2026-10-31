# -*- coding: utf-8 -*-
"""README 登记 r263：动态锚点 + 文末增量章节。用法：python _readme_add_r263.py [stage]"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\a10\aikjx\code\my_lib\openuft"
RP = "04_公共成果/本项目_全维自洽与归一化/README.md"
P = os.path.join(REPO, RP.replace("/", os.sep))
STAGE = len(sys.argv) > 1 and sys.argv[1] == "stage"

B = ("TUFT-r263_攻坚任务书审计_可证伪预言与GW170817裁定_"
     "R等于αλ除2π复现与轴向延迟逐位对拍与literal-helix排除因子6.3e10_"
     "精算与可视化_2026-10-31")

L_SRC = (
    "│   ├── " + B + ".py  # 新增（**r263 · 2026-10-31**）："
    "**攻坚任务书审计（★新层）——靶为用户附件《ROOT 统一场论·下一阶段核心攻坚任务》"
    "（五大 P0 + 可证伪预言 + 障碍分析，逐字留档）**"
    "（条目 **13**：PASS 6 / FAIL 1 / BOUNDARY 2 / INFO 4；**控制组 6/6**、**守卫 6/6**、退出码 0）。"
    "★数字复现逐位命中：**R=αλ/2π=0.638775 nm**（550 nm 算例）、**u=0.999973374c**、"
    "**额外光程 26.627 μm/m、轴向延迟 88.817 fs/m**——文档算术层零缺陷（连续第三轮验证通过）；"
    "本源恒等式 ω_h²=c²(κ²+τ²) 在全参数化（R,ω_h,θ 无一自由）下第四次自动满足；"
    "κ/√(κ²+τ²)=sinθ 恒等式三点机检（文档障碍一前半正确）。"
    "★**GW170817 实验裁定（本卷核心）**：literal-helix 版本（光子独享实体螺旋轨迹）⇒ "
    "轴向延迟 26.6 μm/m 在 40 Mpc 上累积 **1.10e11 s ≈ 3474 年** vs 观测同源延迟 **1.74 s** "
    "⇒ **排除因子 6.3e10**——「光子独享实体螺旋」被实验数据排除；"
    "「万物同螺旋」退化为坐标重定义、「场结构」不可判别（文档 P0-1 自flag）——"
    "三条出路两条不可判别、一条被排除；**B1 是全库第一个被实验数据裁定的可证伪预言**（P0-可证伪 兑现）。"
    "★文档三处自flag 全部确认：结构光 2015 是束结构效应非 ROOT 证据 ✓、"
    "α_measured→构造螺旋 ≠ ROOT→α（与 r257-D1/r261-D1 三线互证）✓、"
    "障碍一『几何不选 α』= r257-D1 独立重证（κ/√(κ²+τ²)=sinθ 任意 θ 机检）✓；"
    "LHAASO 不直接排除（u 与 λ 无关无色散）但谐振腔 1e-18 仍需通过（登记）。"
    "★五大 P0 ↔ 全库映射：P0-α→J32 0/7、P0-作用量→r229 供给 0、P0-协变→r214-234、"
    "P0-可证伪→本卷 B1、P0-光子本体→开放；「什么才算真正攻破」表 ↔ r235 验收口径逐档一致。"
    "开发期自抓 4 处（verdict 括号第五现+append 双参第五现同轮预修 / CTL2 阈值漏四阶项 / "
    "CTL4 期望串顺序 / G1 token 错配 1057→LHAASO）——全部由守卫先行抓出后修复，未带病落盘。"
)

L_VD = (
    "├── 判定_" + B + ".md  # 新增（**r263 · 2026-10-31**）：攻坚任务书审计判定册 —— "
    "§判词 · §判决分组（A 全数字复现 / B GW170817 裁定 / C 结构光与 LHAASO / D 方向批判与 P0 映射 / "
    "E 攻破表）· §★性质界定四条（B1 排除是条件化的；复现逐位；障碍一三线互证；"
    "B1 是全库第一个被实验裁定的可证伪预言——可证伪性双向性）· §治理（判定册落 `判定/`）。"
)

L_INC = (
    "- **r263（2026-10-31）· 攻坚任务书审计（★新层）**：靶 = 用户附件《ROOT 统一场论·下一阶段核心攻坚任务》"
    "（逐字留档）。条目 13（PASS 6 / FAIL 1 / BOUNDARY 2 / INFO 4），控制组 6/6，守卫 6/6，rc=0；"
    "源码 [`TUFT-r263_…py`](源码/" + B + ".py)；"
    "判定册 [`判定_TUFT-r263_…md`](判定/判定_" + B + ".md)；"
    "来料留档 [`…_来料原件_用户附件逐字_2026-10-31.md`](数据/TUFT-r263_攻坚任务书审计_可证伪预言与GW170817裁定_来料原件_用户附件逐字_2026-10-31.md)。"
    "★数字复现逐位命中（R=0.638775 nm / 88.817 fs / 26.627 μm）；"
    "★**GW170817 裁定：literal-helix 排除因子 6.3e10（3474 年 vs 1.74 s）**——"
    "全库第一个被实验数据裁定的可证伪预言；障碍一三线互证；五大 P0 映射到全库边界地图。"
)

L_SEC = """

### r263 · 2026-10-31 · 攻坚任务书审计：可证伪预言与 GW170817 裁定（★新层 · 全库第一个被实验裁定的可证伪预言）

- **产物**：源码 [`TUFT-r263_…py`](源码/__B__.py) / [`…html`](源码/__B__.html)；数据 [`…json`](数据/__B__.json) / [`…md`](数据/__B__.md) / [`…_report.txt`](数据/__B___report.txt)；判定册 [`判定_TUFT-r263_…md`](判定/判定___B__.md)；来料留档 [`数据/TUFT-r263_…_来料原件_用户附件逐字_2026-10-31.md`](数据/TUFT-r263_攻坚任务书审计_可证伪预言与GW170817裁定_来料原件_用户附件逐字_2026-10-31.md)；runner `源码/_run_r263.py` → `源码/_out_r263.txt`
- **复现**：`python -X utf8 源码\\TUFT-r263_…py` ⇒ **rc=0**，条目 **13**（**PASS 6 / FAIL 1 / BOUNDARY 2 / INFO 4**），**控制组 6/6**，**守卫 6/6**。开发期自抓 4 处（详见源码树条目注文），全部由守卫先行抓出后修复重跑，未带病落盘。
- **结论一句话**：**靶文档的算术层零缺陷（R/u/延迟逐位复现），其可证伪预言（literal-helix 轴向延迟）被 GW170817 以排除因子 6.3e10 裁定——「光子独享实体螺旋」出局的实验数据一致性账目完成；文档的障碍分析与攻坚路线与本库边界地图逐档对齐（三线互证）。**
- **与 r257/r261 的关系**：同一命题链的三次推进——r257 定理化（结构层）、r261 验证通过（α=v/c 分析）、r263 可证伪预言裁定（literal-helix 排除）——P0-可证伪从「尚未完成」到「第一个预言被裁定」。
- **取号**：2026-10-31 实测三树最大占用 **r262** ⇒ 取 **r263**（G4 机读复核，白名单含本卷来料留档）。**下轮从 r264 复查起**。
- **治理**：靶 = 用户附件逐字留档（sha256=44b738f1…）；未改 `verify.py`；未跑 `refresh_catalog.py`；git 由收口提交统一处理（分域暂存）；**本卷条目不可与 r142–r262 相加**。
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
    io.open(os.path.join(REPO, "_tmp_readme_r263_stage.md"), "w",
            encoding="utf-8").write(out)
    print("STAGE 版构建：锚 src=r%d vd=r%d inc=r%d；行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
else:
    io.open(P, "w", encoding="utf-8").write(out)
    print("README r263 登记：锚 src=r%d vd=r%d inc=r%d；总行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
