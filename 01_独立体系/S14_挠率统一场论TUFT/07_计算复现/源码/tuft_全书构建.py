# -*- coding: utf-8 -*-
"""
TUFT 全书交付版 · 生成器（可复跑）
==================================
优化点：**取消手工维护的重复数字**。
  - 结构表与累计判定：从 `tuft_总索引.md`（自动扫描）读取；
  - 跨册缺陷族：从 `tuft_跨册缺陷族.json` 读取；
  - 叙事部分（各册判词 / 正面成果 / 解冻条件 / 未完成章节）：内置为数据表，随脚本版本化。
产物：`tuft_全书_交付版.md`
红线：数学自洽 != 物理实验证实。
"""
from __future__ import print_function

import os
import re
import sys
import json

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_全书_交付版.md")
INDEX = os.path.join(HERE, "tuft_总索引.md")
FAM = os.path.join(HERE, "tuft_跨册缺陷族.json")

# ---------- 叙事数据（随脚本版本化，不含手工累计数字）----------
VERDICTS = [
    ("续篇（自旋统计/泡利/手性）", "自旋 1/2 与泡利原理在框架内闭环",
     "`m=αKTΩ/c²` 量纲非法、`γ₅ ∝ T̂` 类型错误 → 已修订"),
    ("闭环相位 = π", "`ψ(2π)=−ψ`、`ψ(4π)=+ψ` 为 SU(2)/SO(3) 双覆盖的表示论事实",
     "闭环莫比乌斯 `Lk=−0.4999≈−1/2` 数值成立；原稿\"外部旋转=莫比乌斯绕行\"、曲线不闭合等问题已修订"),
    ("色挠率 SU(3)", "**本册不成立**",
     "SU(3) 外部注入；线性弦势被证否（实跑 `V~r^1.94`）；`α_s(K_sat)=0.118≠0`；`b0` 反号（`−0.0796` vs `+0.7162`）"),
    ("三路线 A/B/C（分析）", "三条路线均无可保留的超越 GR/SM 的独立预言", "B 给出可被排除的定量命题 `ξ_max≈0.049`"),
    ("四力统一主丛框架", "**不成立**",
     "结构群是**直积**（18 维）非单群；\"3:1 维度比 → sin²θ_W\" 差 **8.12%**；"
     "SM 三耦合在 `1e16 GeV` 处 **21.0% 分散**；统一作用量 = EH+YM+Dirac 逐字照搬；19 个自由参数无一被几何替代"),
    ("黑洞热力学 / 信息悖论", "**不成立**；正面：`T_H=ħc√K(r_h)/(4πk_B)` 与标准式**代数恒等**（偏差 `2.15e-16`）",
     "`K_sat` 对天体黑洞低 **77 个数量级**；代码复现：视界 `K` **跳变 1.582 倍**、内部 `max K=0.6258 K_sat`、"
     "`minimize` 从未调用；`T_H=ħc/(8πGM)` 量纲 **[M]**；`M=(1/c²)∫αKTΩ` 量纲 `L⁻²T²`；真空挠率与作用量矛盾"),
    ("宇宙暴胀 / CMB", "**不成立**",
     "势能 `V=V0Ω(1−Ω)` 为凹函数且 `Ω∉[0,1]` 时**无下界**（`H²<0`，实跑 `math domain error`）；"
     "滚动方向反（`Ω→0`，越界 `−0.0002`）；`N≈60`（实为 `0.2247κ`，`κ=1 → 0.22`）与 `n_s≈0.965`（需 `κ=474.4` vs `267.1`）**互斥**；"
     "`F_T` 量纲非法且数值 `=1+1.06e-103`；`Π_T` 手性能标差 **12 个数量级**；代码 `SyntaxError`+`domain error`"),
    ("挠率探测（R5）/ 挠率产生（R6）", "工程与机制前置均未满足",
     "数值层 `S_tot` 偏低 12 倍；可行性差 `10²⁸`；阶段 0 判定见 R6 报告"),
    ("O-SCALE 锚定 / 全维闭环归一化", "提供与其他体系对接的统一第一性坐标",
     "归一化评级见 `tuft_第一性归一化总览.md`（H/O/C/U）"),
]

POSITIVES = [
    "`ψ(2π)=−ψ`、`ψ(4π)=+ψ`（SU(2) 双覆盖）与闭合莫比乌斯 `Lk≈−1/2`（数值 PASS）",
    "高斯环绕数为**整数**（Hopf 链实算 `−1.0000`）——纠正\"半整数环绕数\"的误用",
    "霍金温度合法几何形式 `T_H = ħc√K(r_h)/(4πk_B)`（与标准式代数恒等，偏差 `2e-16`）",
    "`A/4l_P²` 与黑洞四定律、GSL 相消（`dS_BH=dS_rad`）：标准结果，可作一致性锚",
    "标准模型费米子表 `Q=T₃+Y` 九项全对 + 五类反常 **Fraction 精确为零**（继承性质）",
    "慢滚公式骨架（`ε,η,n_s,N,r=16ε`）与 BICEP/Keck 上限的对照方法（可用）",
    "**判决过程本身**：可被实验排除的定量命题（如 `ξ_max≈0.049`）比\"看起来自洽\"更有价值",
]

THAW = [
    "**群选择原理**：为什么是 `U(1)×SU(2)×SU(3)`（而非把 SM 结构当天降）",
    "**挠率动力学**：作用量补 `T²` 动能项与独立耦合常数（否则真空挠率恒为零）",
    "**映射构造**：挠率分量 → 规范耦合；曲率 `K` → 能标 `Q²` 的显式映射",
    "**量纲门禁**：所有公式先过量纲检查（`αKTΩ/c²`、`F_T`、`T_H` 三处已翻车）",
    "**正则归一**：标量场写 `½M_P²(∂Ω)²`（或 `φ=M_PΩ`），否则 N 与 n_s 的\"吻合\"只是 κ 选取的假象",
    "**可判决量**：至少一个与 GR/SM 有别的定量预言（Page 曲线、TB/EB 谱、正则黑洞 `f(r)`、`ξ_max`）",
    "**代码-文字一致**：脚本须实跑并与文字逐条对齐（本书已把\"代码复现\"列为独立审查环节）",
]

PENDING = [
    ("数学公理化（微分几何/主丛严格化）", "并行推进中",
     "可把 `T^{λ,A}_{μν}`、直积丛、`F=dA+A∧A` 写严格，但**补不上**\"群选择原理\"这个物理缺环"),
    ("人工引力场工程", "**未做**",
     "前置：挠率动力学 + `ξ` 由作用量变分固定（B 路线判 `ξ~O(1)` 越界 ⇒ 要么 `ξ≪1`）"),
    ("地面挠率探测", "已审计（R5）", "数值层 `S_tot` 偏低 12 倍、可行性差 `10²⁸` ⇒ 判定与修复见 R5 文档"),
    ("跨体系归一化", "已做", "H/O/C/U 坐标，可与 openuft 其他体系对接"),
    ("与 openuft 主库对接", "已完成登记", "`S14_torsion_unified_field_tuft`（kind=`candidate_theory`，健康度 **C**）；`verify.py` → **PASS**"),
]


def parse_index(path):
    """从 tuft_总索引.md 读取每份报告判定与合计。"""
    text = open(path, encoding="utf-8").read() if os.path.isfile(path) else ""
    rows = re.findall(r"\|\s*([^|]+?_report\.txt)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", text)
    total = re.search(r"\|\s*\*\*合计\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*", text)
    return rows, (tuple(int(x) for x in total.groups()) if total else None)


def parse_families(path):
    if not os.path.isfile(path):
        return {}, {}
    data = json.load(open(path, encoding="utf-8"))
    fams = data.get("families", {})
    ranked = sorted(fams.items(), key=lambda kv: -kv[1]["total"])
    return fams, ranked


def main():
    rows, total = parse_index(INDEX)
    fams, ranked = parse_families(FAM)

    L = []
    L.append("# TUFT 全维统一场论 · 全书交付版（生成件）")
    L.append("")
    L.append("> **本文件由 `tuft_全书构建.py` 自动生成**：结构表与累计判定取自 `tuft_总索引.md`（自动扫描），")
    L.append("> 跨册缺陷族取自 `tuft_跨册缺陷族.json`；叙事部分（判词/成果/解冻条件）随脚本版本化。")
    L.append("> **判据优先**：每一条主张给出 `PASS / FAIL / BOUNDARY / INFO`，FAIL 必须附可复跑脚本与运行原始输出。")
    L.append("> **红线**：数学自洽 ≠ 物理实验证实；登记、可复跑、可证伪优先于\"看起来自洽\"。")
    L.append("")

    L.append("## 第一章 全书结构（自动表）")
    L.append("")
    L.append("| 报告 | PASS | FAIL | BOUNDARY | INFO |")
    L.append("|---|---|---|---|---|")
    for name, p, f, b, i in rows:
        L.append("| `%s` | %s | %s | %s | %s |" % (name.strip(), p, f, b, i))
    if total:
        L.append("| **合计（%d 份报告）** | **%d** | **%d** | **%d** | **%d** |"
                 % (len(rows), total[0], total[1], total[2], total[3]))
    L.append("")
    L.append("> 索引来源：`tuft_总索引.py`（`python tuft_总索引.py` 复跑）。编排总览：`tuft_全景总报告.md`。")
    L.append("")

    L.append("## 第二章 各册判词（一句话 + 关键数值）")
    L.append("")
    L.append("| 分册 | 判词 | 关键数值 / 修复 |")
    L.append("|---|---|---|")
    for book, verdict, detail in VERDICTS:
        L.append("| %s | %s | %s |" % (book, verdict, detail))
    L.append("")

    L.append("## 第三章 跨册缺陷族（自动统计）")
    L.append("")
    if ranked:
        L.append("> 命中数为**文本启发式计数**（同一病根在各册语料中的族模式检索），不等于判定条数。")
        L.append("")
        L.append("| 缺陷族 | 命中合计 | 复现册数 | 分布（Top） |")
        L.append("|---|---|---|---|")
        for name, info in ranked[:8]:
            dist = "；".join("%s(%d)" % (b, n) for b, n in
                             sorted(info["books"].items(), key=lambda x: -x[1])[:6])
            L.append("| **%s** | %d | %d | %s |" % (name, info["total"], len(info["books"]), dist or "—"))
        L.append("")
    L.append("**核心判读**：缺陷不是\"个别笔误\"，而是少数**结构性病根**在各分册反复复发：")
    L.append("")
    L.append("1. **量纲非法**（复现册数最多）——`αKTΩ/c²`、`F_T`、`T_H` 反复出现同一类错误；")
    L.append("2. **无构造/仅命名**——把\"重新命名\"当\"推导\"（挠率→规范场、曲率饱和→奇点移除、拓扑膜→信息守恒）；")
    L.append("3. **挠率无动力学**——作用量缺 `T²` 项 ⇒ 真空挠率为零 ⇒ 一切\"挠率结构/涨落\"无源（跨四册）；")
    L.append("4. **代码与文字不符**——实跑判决比文字声明更可信（黑洞 `K` 跳变 1.582 倍、暴胀 `domain error`）。")
    L.append("")

    L.append("## 第四章 正面成果（可保留清单）")
    L.append("")
    for k, item in enumerate(POSITIVES, 1):
        L.append("%d. %s" % (k, item))
    L.append("")

    L.append("## 第五章 全书统一解冻条件")
    L.append("")
    for item in THAW:
        L.append("- %s" % item)
    L.append("")

    L.append("## 第六章 未完成章节与下一步")
    L.append("")
    L.append("| 方向 | 状态 | 说明 |")
    L.append("|---|---|---|")
    for a, b, c in PENDING:
        L.append("| %s | %s | %s |" % (a, b, c))
    L.append("")

    L.append("## 第七章 复跑与文件索引")
    L.append("")
    L.append("```powershell")
    L.append("cd tuft")
    L.append("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe tuft_色挠率_SU3_全维求导精算.py")
    L.append("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe tuft_四力统一_全维求导精算.py")
    L.append("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe tuft_黑洞热力学_全维求导精算.py")
    L.append("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe tuft_暴胀CMB_全维求导精算.py")
    L.append("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe tuft_总索引.py")
    L.append("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe tuft_跨册缺陷族检查.py")
    L.append("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe tuft_全书构建.py")
    L.append("cd ../openuft")
    L.append("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe -B verify.py    # -> PASS")
    L.append("```")
    L.append("")
    L.append("- 编排总览：`tuft_全景总报告.md`；自动索引：`tuft_总索引.md`；缺陷族：`tuft_跨册缺陷族.md`")
    L.append("- 逐册：精算报告 + 诚实修订版 + 运行原始输出 `tuft_*_report.txt`")
    L.append("- 主库登记：`openuft/01_独立体系/S14_挠率统一场论TUFT/`（`claims.csv`、`postulates.md`、`11_证伪与反例/精算判定_FAIL汇总.md`）")
    L.append("")
    L.append("---")
    L.append("")
    L.append("*红线（全书结语）：**把\"不可证\"收敛为\"已判决\"，同样是成果。**")
    L.append("本书的价值不在于让 TUFT 成立，而在于让它**可被检查、可被证伪、可被安全引用**。*")

    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("已生成: " + OUT)
    print("  报告数 %d；合计 %s" % (len(rows), "/".join(str(x) for x in total) if total else "N/A"))
    print("  缺陷族条目 %d" % len(ranked))


if __name__ == "__main__":
    main()
