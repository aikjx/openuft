# -*- coding: utf-8 -*-
"""README 登记 r261：动态锚点 + 文末增量章节。用法：python _readme_add_r261.py [stage]"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\a10\aikjx\code\my_lib\openuft"
RP = "04_公共成果/本项目_全维自洽与归一化/README.md"
P = os.path.join(REPO, RP.replace("/", os.sep))
STAGE = len(sys.argv) > 1 and sys.argv[1] == "stage"

B = ("TUFT-r261_全维分析审计_alpha等于玻尔速度比与螺旋映射_"
     "数字复现与标准螺旋恒等式对拍与本源恒等式自动满足_双运动区分定理_"
     "精算与可视化_2026-10-31")

L_SRC = (
    "│   ├── " + B + ".py  # 新增（**r261 · 2026-10-31**）："
    "**全维分析审计（★新层）——靶为用户《全维分析整理好：α=v_Bohr/c 与螺旋映射》"
    "（逐字留档），审计形态=数字复现+恒等式对拍+定理化锐化+诚实项照登+提升定价**"
    "（条目 **15**：PASS 11 / BOUNDARY 1 / INFO 3，**零 FAIL**；**控制组 6/6**、**守卫 6/6**、退出码 0）。"
    "★数字复现 **8/8 全对**：α=e²/(4πε₀ℏc) rel 6.1e-10（Decimal 独立 3.6e-16）、"
    "v_Bohr=2,187,691.26 m/s（0.7297% c）、θ 机算 0.418111°（靶 0.41813° 差 4.6e-5 属靶舍入层，如实注记）、"
    "v_z/c=0.99997337、κ=α²/R 与 τ=α√(1−α²)/R 与标准圆柱螺旋恒等式（r58 库）逐项一致、"
    "α=r_C/a₀ 恒等式成立（r_C=3.8616e-13 m、a₀=5.2918e-11 m）。"
    "★新增机器定理二条：①**本源恒等式自动满足**——映射 ω=v_⊥/R=αc/R ⇒ ω²=c²(κ²+τ²) "
    "对任意 (α,R) 恒成立（三点机检残差 <1e-12），映射与本库承重恒等式（r241/r257）自动相容；"
    "②**双运动区分定理**——玻尔电子（v=αc、θ=90°、κ=1/a₀=1.890e10 m⁻¹）≠ c-螺旋"
    "（v=c、θ=0.418°、κ=α²/a₀=1.006e6 m⁻¹），曲率差 **1/α²=18778.9 倍**（靶自flag 锐化为定理）。"
    "★τ/κ=√(1−α²)/α=137.032——映射把 α 编码为『挠率/曲率比』（可登记签名数）。"
    "★诚实项三项照登（v_⊥/c=α 是新增假设非 Maxwell 推导 / 玻尔电子≠光子内部 / "
    "需独立推导+可判别实验）——与 r257 反定理**同向相容**（映射方向 α→几何，不触判别力 0 bit 红线）。"
    "★提升定价（BOUNDARY）：映射当前对光子可观测无新增耦合（重参数化）⇒ 判别力待补，"
    "τ/κ=137 签名与多体系长度比检验为可行方向。"
    "开发期自抓 5 处（append 双参第四现 / verdict 括号第四现 / B3 标题未格式化 / A4 少参 / "
    "WS_SHA 未定义+位置错 / G4 白名单漏本来料留档）——全部由守卫先行抓出后修复，未带病落盘。"
)

L_VD = (
    "├── 判定_" + B + ".md  # 新增（**r261 · 2026-10-31**）：全维分析审计判定册 —— "
    "§判词 · §判决分组（A 数字复现 / B 螺旋映射审计 / C 双运动区分 / D 衔接与定价 / E 全对率）· "
    "§★性质界定四条（验证通过轮非放水——8 项独立机算+负控制；零 FAIL 不是放水；"
    "与 r257 反定理同向；提升定价）· §治理（判定册落 `判定/`）。"
)

L_INC = (
    "- **r261（2026-10-31）· 全维分析审计（★新层）**：靶 = 用户《α=v_Bohr/c 与螺旋映射》"
    "（逐字留档）。条目 15（PASS 11 / BOUNDARY 1 / INFO 3，零 FAIL），控制组 6/6，守卫 6/6，rc=0；"
    "源码 [`TUFT-r261_…py`](源码/" + B + ".py)；"
    "判定册 [`判定_TUFT-r261_…md`](判定/判定_" + B + ".md)；"
    "来料留档 [`…_来料原件_用户分析逐字_2026-10-31.md`](数据/TUFT-r261_全维分析审计_alpha等于玻尔速度比与螺旋映射_来料原件_用户分析逐字_2026-10-31.md)。"
    "★数字复现 **8/8 全对**；★新增定理：**本源恒等式自动满足**（ω²=c²(κ²+τ²) 对任意 α,R）"
    "与**双运动区分**（玻尔电子 vs c-螺旋，曲率差 18778.9 倍）；τ/κ=137.032 签名数；"
    "诚实项三项照登，与 r257 反定理同向相容；提升定价=判别力待补（BOUNDARY）。"
)

L_SEC = """

### r261 · 2026-10-31 · 全维分析审计：α = v_Bohr/c 与螺旋映射（★新层 · ★验证通过轮）

- **产物**：源码 [`TUFT-r261_…py`](源码/__B__.py) / [`…html`](源码/__B__.html)；数据 [`…json`](数据/__B__.json) / [`…md`](数据/__B__.md) / [`…_report.txt`](数据/__B___report.txt)；判定册 [`判定_TUFT-r261_…md`](判定/判定___B__.md)；来料留档 [`数据/TUFT-r261_…_来料原件_用户分析逐字_2026-10-31.md`](数据/TUFT-r261_全维分析审计_alpha等于玻尔速度比与螺旋映射_来料原件_用户分析逐字_2026-10-31.md)；runner `源码/_run_r261.py` → `源码/_out_r261.txt`
- **复现**：`python -X utf8 源码\\TUFT-r261_…py` ⇒ **rc=0**，条目 **15**（**PASS 11 / BOUNDARY 1 / INFO 3，零 FAIL**），**控制组 6/6**，**守卫 6/6**。开发期自抓 5 处（详见源码树条目注文），全部由守卫先行抓出后修复重跑，未带病落盘。
- **结论一句话**：**靶分析 8 项数字/恒等式复现 8/8 全对（α、v_Bohr、玻尔推导、θ、v_z/c、κ·τ 两式、r_C/a₀），并新增两条机器定理（本源恒等式自动满足 + 双运动区分）；诚实声明三项照登；与 r257 反定理同向相容；提升为定律的定价 = 判别力待补（BOUNDARY，τ/κ=137 签名与多体系长度比检验为可行方向）。**
- **与既往轮的对照**：本靶是全维分析的正确范例（数字零崩坏 + 假设/范畴/验证路径三处诚实自flag），与 r245（差 6.9e4 倍）/r246（NameError）/r248-r251（量纲断裂/反号/定义恒等式）形成方法学对照。
- **取号**：2026-10-31 实测三树最大占用 **r260** ⇒ 取 **r261**（G4 机读复核，白名单含本卷来料留档）。**下轮从 r262 复查起**。
- **治理**：靶 = 用户消息逐字留档（无文件附件）；未改 `verify.py`；未跑 `refresh_catalog.py`；git 由收口提交统一处理（分域暂存）；**本卷条目不可与 r142–r260 相加**。
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
    io.open(os.path.join(REPO, "_tmp_readme_r261_stage.md"), "w",
            encoding="utf-8").write(out)
    print("STAGE 版构建：锚 src=r%d vd=r%d inc=r%d；行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
else:
    io.open(P, "w", encoding="utf-8").write(out)
    print("README r261 登记：锚 src=r%d vd=r%d inc=r%d；总行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
