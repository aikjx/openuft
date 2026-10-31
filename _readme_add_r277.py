# -*- coding: utf-8 -*-
"""README 登记 r277：动态锚点 + 文末增量章节。用法：python _readme_add_r277.py [stage]"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\a10\aikjx\code\my_lib\openuft"
RP = "04_公共成果/本项目_全维自洽与归一化/README.md"
P = os.path.join(REPO, RP.replace("/", os.sep))
STAGE = len(sys.argv) > 1 and sys.argv[1] == "stage"

B = ("TUFT-r277_常数本源普查_量纲代数三分类与无量纲约化K等于5_"
     "单位重标定不变性机器演示_精算与可视化_2026-10-31")

L_SRC = (
    "│   ├── " + B + ".py  # 新增（**r277 · 2026-10-31**）："
    "**常数本源普查（★新层 · 自驱轮）——回应『全维物理的常数，物理的本质本源』："
    "库常数块 13 成员全表机器三分类**（条目 **8**：PASS 5 / FAIL 1 / BOUNDARY 1 / INFO 1；"
    "**控制组 6/6**、**守卫 6/6**、退出码 0）。"
    "★三分类：**定义精确层** c（SI-1983）/h（2019）⇒ ℏ=h/2π 精确/e（2019）——位级机检、"
    "库值仅显示截断（rel 6.1e-10）；**测量·无量纲本源数层** α/G/g_e/g_p/质量；"
    "**派生层** ε₀=e²/(4παℏc)/μ_B=eℏ/2m_e/μ_N=eℏ/2m_p/a₀/r_C=α·a₀/ħc——"
    "六项数值命中（rel 3e-10~2e-9，ħ 截断层主导）。"
    "★**无量纲约化计数定理（B2）：全库计算最终依赖 K=5 个独立本源数 "
    "{α, g_p, m_e/m_μ, m_e/m_p, m_d/m_p}**（g_e−2=α/π+0.15% 高阶，α-可导层）——"
    "本源数清单第一次被机器钉死；grep 资产普查（B1）：G 用于 170 个引擎（引力链）、"
    "MP 用于 6 个——**写卷时预设『MP 零使用』被普查自身推翻、如实登记**"
    "（预设让位机检的示范条目）。"
    "★**本卷核心判定（C1 FAIL，解放性）**：单位重标定机器演示 5 组随机 (λM,λL,λT,λI)——"
    "全部量纲ful数值连续可变、α 与全部比值严格不变（CODATA 自洽层 6.1e-10）⇒ "
    "**本源不在常数数值里（数值=单位约定），而在无量纲关系结构里**"
    "（α=v_Bohr/c=r_C/a₀、K₁/K₂=β、μd/μH 比、g_e−2=α/π+高阶——r261/r271/r276 承接）——"
    "『从几何推出常数数值』在量纲层即被解除，候选动力学的合格线被精确化："
    "预测 K=5 本源数间的关系结构且通过三体系 VP 义务；本源问题=L6 作用量供给（五线互证承接）；"
    "L10 净盈余 0 bit 不变（C2 BOUNDARY）。"
    "★局限登记：(M,L,T) 量纲机不覆盖电流维 I（QE/ε₀/μ_B/μ_N 以数值关系层补偿）；"
    "m_d/m_p=1.99900=2×0.99950（中子/质子比未单列——下一普查扩展）。"
    "开发期自抓 7 处（**μ_N/ħc 派生 MeV→kg 换算错用 u、m→fm 漏 ×1e15——rel=1.0 直接暴露**/"
    "m_e-m_p 比同源换算错/CTL 阈值被截断层污染 ×3/CTL4 dstr 序期望错/B1 预设被普查推翻/"
    "EXPECT_DIST 条目数——全部由守卫链抓出后修复重跑全绿），未带病落盘。"
)

L_VD = (
    "├── 判定_" + B + ".md  # 新增（**r277 · 2026-10-31**）：常数本源普查判定册 —— "
    "§判词 · §判决分组（A 普查与派生链 / B grep 资产与 K=5 / C 重标定演示与关系结构）· "
    "§★性质界定四条（C1 是解放性判定——『预测常数数值』不可能任务被卸下，"
    "合格线=复现 K=5 关系结构+三体系 VP 义务；K=5 清单可证伪；关系网资产观；I 维局限）· "
    "§治理（判定册落 `判定/`）。"
)

L_INC = (
    "- **r277（2026-10-31）· 常数本源普查（★新层 · 自驱轮）**：回应『全维物理的常数，"
    "物理的本质本源』。条目 8（PASS 5 / FAIL 1 / BOUNDARY 1 / INFO 1），控制组 6/6，守卫 6/6，rc=0；"
    "源码 [`TUFT-r277_…py`](源码/" + B + ".py)；"
    "判定册 [`判定_TUFT-r277_…md`](判定/判定_" + B + ".md)。"
    "★常数块 13 成员三分类（定义精确/测量/派生）+ α-派生链六项命中 + grep 资产普查；"
    "★**K=5 独立无量纲输入计数定理** {α, g_p, m_e/m_μ, m_e/m_p, m_d/m_p}；"
    "★**单位重标定机器演示：本源不在常数数值里、在无量纲关系结构里**（C1 FAIL 解放性判定）——"
    "本源问题=L6 作用量供给；L10 保持 0 bit。取号实测最大 r276 ⇒ r277。"
)

L_SEC = """

### r277 · 2026-10-31 · 常数本源普查：量纲代数三分类、无量纲约化 K=5（★新层 · 自驱轮）

- **产物**：源码 [`TUFT-r277_…py`](源码/__B__.py) / [`…html`](源码/__B__.html)；数据 [`…json`](数据/__B__.json) / [`…md`](数据/__B__.md) / [`…_report.txt`](数据/__B___report.txt)；判定册 [`判定_TUFT-r277_…md`](判定/判定___B__.md)；runner `源码/_run_r277.py` → `源码/_out_r277.txt`
- **复现**：`python -X utf8 源码\\TUFT-r277_…py` ⇒ **rc=0**，条目 **8**（**PASS 5 / FAIL 1 / BOUNDARY 1 / INFO 1**），**控制组 6/6**，**守卫 6/6**。开发期自抓 7 处（含 MeV→kg 换算级真缺陷由派生链 rel=1.0 直接暴露），全部修复后重跑全绿。
- **结论一句话**：**全库 13 常数三分类完成：定义精确（c/ℏ/e，数值=约定）、测量·无量纲本源数（α/g_p/g_e/质量）、派生（ε₀/μ_B/μ_N/a₀/r_C/ħc 六项命中）——全库计算最终依赖 K=5 个独立本源数 {α, g_p, m_e/m_μ, m_e/m_p, m_d/m_p}；单位重标定机器演示证明本源不在常数数值里而在无量纲关系结构里——『物理的本质本源』的库内诚实回答：结构可机器化、起源=L6 作用量供给开放、净盈余 0 bit。**
- **与前置卷的关系**：C1 = r257-D1 量纲反解第三证的常数版（Duff–Okun 论纲机器实现）；关系网清单承接 r261/r271/r276；本源问题承接 r275 L6/L10。
- **取号**：2026-10-31 实测三树最大占用 **r276** ⇒ 取 **r277**（G4 机读复核）。**下轮从 r278 复查起**。
- **治理**：自驱轮无来料；五份前置判定册在盘（G1 指纹）；未改 `verify.py`；未跑 `refresh_catalog.py`；git 由收口提交统一处理（分域暂存）；**本卷条目不可与 r142–r276 相加**。
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
    io.open(os.path.join(REPO, "_tmp_readme_r277_stage.md"), "w",
            encoding="utf-8").write(out)
    print("STAGE 版构建：锚 src=r%d vd=r%d inc=r%d；行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
else:
    io.open(P, "w", encoding="utf-8").write(out)
    print("README r277 登记：锚 src=r%d vd=r%d inc=r%d；总行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
