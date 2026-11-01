# -*- coding: utf-8 -*-
"""r318 README 注册（detail-only 追加，零删除）。
严格：备份一次；前缀逐行不变（new[:len(old)]==old）；### r318 · 恰 1 条。
"""
import io, os, datetime

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(BASE, "README.md")
RID = "r318"

SRC = "TUFT-r318_XR301攻防_合法几何源与三代可实现性_Ngen自由与不可预测性_精算与可视化_2026-11-01.py"
DATA = "TUFT-r318_XR301攻防_合法几何源与三代可实现性_Ngen自由与不可预测性_精算与可视化_2026-11-01"
JUD = "判定_TUFT-r318_XR301攻防_合法几何源与三代可实现性_Ngen自由与不可预测性_2026-11-01.md"
HTML = "四力统一方程_XR301合法几何源与Ngen自由可视化_2026-11-01.html"

with io.open(README, "r", encoding="utf-8") as f:
    old = f.read()

if "TUFT-r318_" in old:
    print("SKIP: README 已含 r318")
    raise SystemExit(0)

block = """### r318 · 2026-11-01 · X-R301-1 攻防 · 合法几何源下的代数可实现性与可预测性（N_gen 自由 · 三代非结构性禁止）（★攻 r306 唯一单点否证入口 · 承 r296/r306/r307/r309 判词链 · 判词链第 8 层）

- **产物**：源码 [`%s`](源码/%s)；数据 [`…json`](数据/%s.json) / [`…md`](数据/%s.md) / [`…_report.txt`](数据/%s_report.txt)；判定册 [`%s`](判定/%s)；runner `源码/_run_r318.py` → `源码/_out_r318.txt`；交互可视化 [`%s`](%s)
- **复现**：`python -X utf8 源码\\_run_r318.py` ⇒ **rc=1**（仅 P7 判据集设计性 FAIL），条目 **22**（主 **8**：**PASS 4 / FAIL 1 / INFO 3**），**控制组 4/4**，**守卫 10/10**，纯整数行列式因子 + Fraction 精确，耗时约 9 s。
- **核心发现**：沿用 r296/r306 规范 FCSRE 通量模型（A=diag(d_i)，6 独立电荷自由度）+ **单个 0/1 轨道扭转** ⇒ **N_gen=3 代数可达**：单扭转穷举 64 个中 **16 个可解**（全部满足 g₀=1 且 g₃=1，因 d=6、d=2 不整除 3）；显式构造 g=(1,0,0,1,0,0)、Y=3、X=(0,1,1,0,3,3) ⇒ **A·t=3·𝟙 逐行精确**；且 **N=1..12 全部可构造**（Y=N 显式拨入）⇒ **N_gen 完全自由**。
- **判词**：**NO-GO-DOWNGRADED-TO-FREE** —— r306 的 `NO-GO-STABLE`（三代结构性不可能）在「合法源 = 自由通量 + 0/1 扭转」口径下**过强**；三代**不被结构禁止**，但**亦不可预测**（每个解都把 N 作为扭转份数 Y 拨入，Y 是几何/拓扑输入）。三代问题从「被结构性禁止」降级为「未被机制选中」，与 r307「3 是拓扑输入、N_gen≤π0」独立一致。**r298→…→r317→r318 判词链：第 8 层 = 把「三代不可能」改写为「三代未选中」。** 遗留 X-R318-1（能否让 Y 被动力学/拓扑自然固定为 3——「预言 3」的真关口）/ X-R318-2（多扭转列在受约束模式 k₂≡k₃ 下是否仍实现 3）/ X-R296-3、X-R296-1（承 r306，仍 OPEN）。
- **取号**：落盘前实测 **r308–r317 已被并行会话占满**（r308=ROOT V22、r309=指标形式定理、r310–r316 齐套、r317=ROOT V24），**r318/r319/r320 三号全空** ⇒ 取 **r318**（源码先落占号）。**建模自纠（如实登记）**：初版把通量误建为**单列** d（得「仅全 1 扭转」，与 r296 规范 diag 模型不符，控制组 C1/C2 FAIL 当场暴露）⇒ 改用规范 diag 重算，单扭转可解数由 1 更正为 **16**、控制组 4/4；另 JS 一处多余 `}` 致几何体检 `missing )`，已修并复检 GEOMETRY-OK。**治理**：未改 verify.py；未跑 refresh_catalog.py；未改任何既有卷字节（G9 逐路径核验仅写本卷产物）；旧 TAG 重复件已隔离至 scratch/；README 仅追加大本条目（按 r310–r317 现行 detail-only 惯例，不回溯补 src 树/compact）。**下轮从 r321 复查起（并行链极活跃，取号前必扫三树 + README detail）。**
""" % (SRC, SRC, DATA, DATA, DATA, JUD, JUD, HTML, HTML)

# 备份一次
bak = os.path.join(BASE, "README.bak_%s_%s.md" % (RID, datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
if not os.path.exists(bak):
    with io.open(bak, "w", encoding="utf-8") as f:
        f.write(old)

sep = "" if old.endswith("\n\n") else ("\n" if old.endswith("\n") else "\n\n")
new = old + sep + block + "\n"

with io.open(README, "w", encoding="utf-8") as f:
    f.write(new)

# 校验
old_lines = old.splitlines()
new_lines = new.splitlines()
prefix_ok = new_lines[:len(old_lines)] == old_lines
n_detail = sum(1 for ln in new_lines if ln.startswith("### r318 ·"))
n_src = sum(1 for ln in new_lines if "TUFT-r318_" in ln)
print("BAK:", os.path.basename(bak))
print("prefix_preserved(零删除):", prefix_ok)
print("detail anchors '### r318 ·':", n_detail)
print("lines with TUFT-r318_:", n_src)
print("RESULT:", "PASS" if (prefix_ok and n_detail == 1) else "FAIL")
