# -*- coding: utf-8 -*-
"""README 登记 r276：动态锚点 + 文末增量章节。用法：python _readme_add_r276.py [stage]"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\a10\aikjx\code\my_lib\openuft"
RP = "04_公共成果/本项目_全维自洽与归一化/README.md"
P = os.path.join(REPO, RP.replace("/", os.sep))
STAGE = len(sys.argv) > 1 and sys.argv[1] == "stage"

B = ("TUFT-r276_多体系α链扩展_电子氢缪子氢缪子氘三体系Uehling数值机检_"
     "mr立方标度失效量化_精算与可视化_2026-10-31")

L_SRC = (
    "│   ├── " + B + ".py  # 新增（**r276 · 2026-10-31**）："
    "**多体系 α 链扩展（★新层 · 自驱轮）——承接 r275 L9/L8，同一套 Uehling 积分器"
    "打三个质量尺度**（条目 **8**：PASS 5 / FAIL 1 / BOUNDARY 1 / INFO 1；"
    "**控制组 6/6**、**守卫 6/6**、退出码 0）。"
    "★三体系全部命中：①电子氢 ⟨2P−2S⟩=26.887 MHz vs 文献『VP 使 2S 下移约 27 MHz』"
    "（ScienceDirect 核实）rel 4.2e-3——λ_e/a₀=7.3e-3 压抑区；"
    "②缪子氢 204.984 meV（r275 位级回归 rel 1.7e-7，仪器同一性）——a/λ_e=0.74 近壳区；"
    "③缪子氘 227.608 meV vs 点氘常数 230.4862 meV=228.7766+1.7096(TPE)"
    "（**Pohl et al. Science 353, 669 (2016) Eq.5/7/8 原文核实**）rel 1.2e-2；"
    "理论公式复算 ΔE(r_d)=202.8783 meV vs 实测 202.8785 meV（Eq.5，rel 1.1e-6）——"
    "μd 双锚（公式锚+数值锚）分离命中。"
    "★**m_r³ 标度定律失效量化（本卷核心）**：数值比 VP(μd)/VP(μH)=1.1104 vs "
    "naive (m_r^d/m_r^p)³=1.1685（**−5.0%**）且数值比 vs 文献点常数比 1.1187（rel 7.4e-3）——"
    "a_μd/λ_e=0.70、a_μH/λ_e=0.74 均在非接触区，VP 含非平庸 a/λ_e 依赖——"
    "**L8 兼容义务升级（C1 FAIL）：固定比值候选必须重现三条不同的 a/λ_e 依赖曲线"
    "（27 MHz 压抑区 / 205 meV / 229 meV 近壳区）而非单一 m_r³ 系数**（r250/r275 承接）；"
    "L10 盈余账本保持 0 bit（C2），本轮净增判别测点 3 个；μHe（Z 标度维）留下一测点。"
    "★锚值核实链：μd ← Pohl 2016 全文（fetch 原文）；eH ← ScienceDirect 综述（web）；"
    "μH ← r275（Antognini 2011，web）。"
    "开发期自抓 5 处（G1 token/B1 标题裸占位符+三元脏结构/CTL3 写死布尔/CTL4 换算校验值/"
    "EXPECT_DIST 与实际条目数不匹配——全部由守卫链抓出后修复重跑），未带病落盘。"
)

L_VD = (
    "├── 判定_" + B + ".md  # 新增（**r276 · 2026-10-31**）：多体系 α 链扩展判定册 —— "
    "§判词 · §判决分组（三体系数值/标度失效/L8 义务加重/L10 复述）· "
    "§★性质界定四条（标度失效是义务的具体化；μd 双锚分离；eH 压抑区命中——积分器动态"
    "范围 5 个量级；L10 不动纪律）· §治理（判定册落 `判定/`）。"
)

L_INC = (
    "- **r276（2026-10-31）· 多体系 α 链扩展（★新层 · 自驱轮）**：承接 r275 L9/L8。"
    "条目 8（PASS 5 / FAIL 1 / BOUNDARY 1 / INFO 1），控制组 6/6，守卫 6/6，rc=0；"
    "源码 [`TUFT-r276_…py`](源码/" + B + ".py)；"
    "判定册 [`判定_TUFT-r276_…md`](判定/判定_" + B + ".md)。"
    "★三体系 Uehling 数值全部命中：eH 26.887 MHz（rel 4.2e-3）/ μH 204.984 meV"
    "（位级回归）/ μd 227.608 meV vs 点氘常数 230.4862（Pohl 2016 Eq.5/7/8 原文核实）；"
    "★**m_r³ 标度失效 −5.0% 量化** ⇒ L8 义务升级为三体系非平庸 a/λ_e 依赖（C1 FAIL）；"
    "L10 保持 0 bit；μHe 留下一测点。取号实测（启动时）⇒ r276。"
)

L_SEC = """

### r276 · 2026-10-31 · 多体系 α 链扩展：eH/μH/μd 三体系 Uehling 数值机检（★新层 · 自驱轮）

- **产物**：源码 [`TUFT-r276_…py`](源码/__B__.py) / [`…html`](源码/__B__.html)；数据 [`…json`](数据/__B__.json) / [`…md`](数据/__B__.md) / [`…_report.txt`](数据/__B___report.txt)；判定册 [`判定_TUFT-r276_…md`](判定/判定___B__.md)；runner `源码/_run_r276.py` → `源码/_out_r276.txt`
- **复现**：`python -X utf8 源码\\TUFT-r276_…py` ⇒ **rc=0**，条目 **8**（**PASS 5 / FAIL 1 / BOUNDARY 1 / INFO 1**），**控制组 6/6**，**守卫 6/6**。开发期自抓 5 处，全部修复后重跑全绿。
- **结论一句话**：**同一 α、同一积分器、三个质量尺度（eH 27 MHz 压抑区 / μH 205 meV / μd 229 meV 近壳区）全部命中——多体系 α 链三体系机检完成；m_r³ 标度定律失效 −5.0% 量化 ⇒ L8 兼容义务升级为『重现三体系非平庸 a/λ_e 依赖』；L10 净盈余保持 0 bit，判别测点 +3。**
- **与 r275 的关系**：r275 建立 Uehling 积分器与单体系（μH）锚定；本卷同一仪器扩展到 eH/μd 并量化标度失效——L9 完成三体系化、L8 义务具体化、L10 复述。
- **取号**：2026-10-31 实测三树最大占用（启动时）⇒ 取 **r276**（G4 机读复核）。**下轮从 r277 复查起**。
- **治理**：自驱轮无来料；锚值 web/fetch 核实（μd：Pohl 2016 原文；eH：ScienceDirect；μH：r275）；未改 `verify.py`；未跑 `refresh_catalog.py`；git 由收口提交统一处理（分域暂存）；**本卷条目不可与 r142–r275 相加**。
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
    io.open(os.path.join(REPO, "_tmp_readme_r276_stage.md"), "w",
            encoding="utf-8").write(out)
    print("STAGE 版构建：锚 src=r%d vd=r%d inc=r%d；行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
else:
    io.open(P, "w", encoding="utf-8").write(out)
    print("README r276 登记：锚 src=r%d vd=r%d inc=r%d；总行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
