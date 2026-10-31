# -*- coding: utf-8 -*-
"""README 登记 r283：动态锚点 + 文末增量章节。用法：python _readme_add_r283.py [stage]"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\a10\aikjx\code\my_lib\openuft"
RP = "04_公共成果/本项目_全维自洽与归一化/README.md"
P = os.path.join(REPO, RP.replace("/", os.sep))
STAGE = len(sys.argv) > 1 and sys.argv[1] == "stage"

B = ("TUFT-r283_V10选择机制审计_拓扑闭合环面结四次能量条件级数_"
     "全库总结_精算与可视化_2026-10-31")

L_SRC = (
    "│   ├── " + B + ".py  # 新增（**r283 · 2026-10-31**）："
    "**V10 选择机制审计 + 全库总结（★新层）——靶 = 用户附件《ROOT V10.0：从『寻找 α 的公式』"
    "转向『寻找唯一选择机制』》（逐字留档；用户指令『总结所有，并 openuft 攻破』）**"
    "（条目 **11**：PASS 7 / FAIL 1 / BOUNDARY 1 / INFO 2；**控制组 6/6**、**守卫 6/6**、退出码 0）。"
    "★靶全部数字独立复算命中：①拓扑闭合链 2πpb=qL ⇒ κ/|τ|=2πpR/(|q|L)（rel 0，R/L 连续自由度"
    "确认）②绕数候选 262.70 ppm ✓ ③**条件级数 80 位复算：Ω=4π³+π²+π=137.03630377587843、"
    "α⁻¹_cand=137.03599917614199（vs CODATA 137.035999177 差 −8.580e-10=−0.04086σ，"
    "σ_eff=2.0999e-8=官方 u(α⁻¹)——与靶 137.035999176142 命中到第 15 位）**"
    "④三阶段 σ 阶梯：主项 14506σ（靶 14505）/首阶 25.9σ（靶 25.87）/完整 0.0409σ ✓"
    "⑤圆环面结 (2,3) 四组 Q_geom 数值积分复算（max rel 2.7e-5——同结型非唯一确认）"
    "⑥四次能量 (B−A)/C=2α²/(1+α²)=1.0649704e-4（rel 1.4e-9 命中）"
    "⑦磁单极 α_eα_m=n²/4 + 敏感度 1.65e-10→1.58σ（量级命中）。"
    "★**本卷核心判定（B1 FAIL）：五层缺口全部机器确认（拓扑连续自由度/离散族无理由/"
    "能量系数未导出/结型非唯一/匹配公设未证+敏感度）⇒ 唯一选择机制缺位终形——"
    "与 r257-D1/r269-B1/r271-B1/r277-C1/r280-A1 合流为六线互证（判别力 0 bit 第六种证明："
    "拓扑/能量新族关闭）**；Symmetry 路线定位（B2 BOUNDARY）：数值命中 0.04086σ ≠ 物理验证"
    "（匹配公设未证——与 numerology 的认识论距离只有一步，登记警惕）。"
    "★**全库总结（C1，用户指令『总结所有』）**：r246→r283 判定链闭合于 L6 唯一入口——"
    "审计形态学三型（攻破/验证通过/预测）、判别力六线互证、L1–L10 链路、K=5+1 常数本源、"
    "Φ 曲线双端解析锚定、μHe 预测待锚——『力的大统一是在同一个运动里面』的**结构层已机器化**"
    "（V₁₂ 统一式+Φ 曲线+恒等式库），**起源层（K=5+1 本源数为何取这些值）诚实开放**。"
    "开发期自抓 3 处（**Machin π atan 负项提前 break——π(80) 假值由 CTL1 交叉抓出**/"
    "级数 om_pow 初始化 Ω¹ 应 Ω³/**CTL1 误取 omega 当 π**——三处全部由守卫链/交叉校验抓出"
    "修复后 80 位复算闭环命中），未带病落盘。"
)

L_VD = (
    "├── 判定_" + B + ".md  # 新增（**r283 · 2026-10-31**）：V10 选择机制审计+全库总结判定册 —— "
    "§判词 · §判决分组（A 复现 7 条 / B 六线合流+Symmetry 定位 / C 全库总结+治理）· "
    "§★性质界定四条（B1 六线收官；Symmetry 定位——0.04086σ≠物理验证；全库总结；"
    "连续第四份全诚实靶）· §治理（判定册落 `判定/`）。"
)

L_INC = (
    "- **r283（2026-10-31）· V10 选择机制审计 + 全库总结（★新层）**：靶 = 用户附件"
    "《ROOT V10.0》（逐字留档）。条目 11（PASS 7 / FAIL 1 / BOUNDARY 1 / INFO 2），"
    "控制组 6/6，守卫 6/6，rc=0；"
    "源码 [`TUFT-r283_…py`](源码/" + B + ".py)；"
    "判定册 [`判定_TUFT-r283_…md`](判定/判定_" + B + ".md)；"
    "来料留档 [`…_来料原件_用户附件逐字_2026-10-31.md`](数据/TUFT-r283_V10选择机制审计_拓扑闭合环面结四次能量条件级数_全库总结_来料原件_用户附件逐字_2026-10-31.md)。"
    "★靶全部数字复算命中（80 位级数 α⁻¹=137.03599917614199、σ 阶梯 14506/25.9/0.0409、"
    "环面结四组、262.70 ppm、(B−A)/C、磁单极、敏感度 1.58σ）；"
    "★**六线互证收官：唯一选择机制缺位终形（五层缺口机器确认）**；"
    "★全库总结（r246→r283）：结构层机器化完成、起源层（L6）诚实开放、净盈余 0 bit。"
    "取号实测最大 r282 ⇒ r283。"
)

L_SEC = """

### r283 · 2026-10-31 · V10 选择机制审计 + 全库总结（★新层）

- **产物**：源码 [`TUFT-r283_…py`](源码/__B__.py) / [`…html`](源码/__B__.html)；数据 [`…json`](数据/__B__.json) / [`…md`](数据/__B__.md) / [`…_report.txt`](数据/__B___report.txt)；判定册 [`判定_TUFT-r283_…md`](判定/判定___B__.md)；来料留档 [`数据/TUFT-r283_…_来料原件_用户附件逐字_2026-10-31.md`](数据/TUFT-r283_V10选择机制审计_拓扑闭合环面结四次能量条件级数_全库总结_来料原件_用户附件逐字_2026-10-31.md)；runner `源码/_run_r283.py` → `源码/_out_r283.txt`
- **复现**：`python -X utf8 源码\\TUFT-r283_…py` ⇒ **rc=0**，条目 **11**（**PASS 7 / FAIL 1 / BOUNDARY 1 / INFO 2**），**控制组 6/6**，**守卫 6/6**。开发期自抓 3 处（Machin π 负项 break/级数 Ω³ 初始化/CTL1 取值），全部由守卫链与交叉校验抓出修复，80 位复算闭环命中。
- **结论一句话**：**靶《V10》全部数字独立复算命中（80 位级数 α⁻¹=137.03599917614199、σ 阶梯 14506/25.9/0.0409σ、环面结四组、(B−A)/C、磁单极、敏感度 1.58σ）——五层缺口机器确认 ⇒ 唯一选择机制缺位终形（六线互证收官）；全库总结：r246→r283 判定链闭合于 L6 唯一入口——『力的大统一是在同一个运动里面』结构层机器化完成、起源层诚实开放、净盈余 0 bit。**
- **全库主线（总结）**：r246 攻破轮 → r257 同一运动定理 → r259 c-幂阶梯 → r261 验证通过 → r263 GW170817 裁定 → r269 候选多元性 → r271 时空不变量+剪枝 → r275 全链路 L1–L10 → r276 三体系 → r277 常数本源 K=5 → r280 方法全谱+Φ 曲线 → r282 双端解析锚定 → r283 六线合流+全库总结。
- **取号**：2026-10-31 实测三树最大占用 **r282** ⇒ 取 **r283**（G4 机读复核）。**下轮从 r284 复查起（并行链活跃，取号前必扫）**。
- **治理**：来料逐字留档（sha256=BA4E43DA…）；未改 `verify.py`；未跑 `refresh_catalog.py`；git 由收口提交统一处理（分域暂存）；**本卷条目不可与 r142–r282 相加**。
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
    io.open(os.path.join(REPO, "_tmp_readme_r283_stage.md"), "w",
            encoding="utf-8").write(out)
    print("STAGE 版构建：锚 src=r%d vd=r%d inc=r%d；行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
else:
    io.open(P, "w", encoding="utf-8").write(out)
    print("README r283 登记：锚 src=r%d vd=r%d inc=r%d；总行数 %d"
          % (n_src, n_vd, n_inc, len(lines)))
