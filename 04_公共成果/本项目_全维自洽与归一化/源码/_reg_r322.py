# -*- coding: utf-8 -*-
"""r322 README 注册（detail-only 追加，零删除）。"""
import io, os, datetime

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(BASE, "README.md")
RID = "r322"

SRC = "TUFT-r322_XR318-1审计_真几何扭转模式约束与NO-GO存活检验_精算与可视化_2026-11-01.py"
DATA = "TUFT-r322_XR318-1审计_真几何扭转模式约束与NO-GO存活检验_精算与可视化_2026-11-01"
JUD = "判定_TUFT-r322_XR318-1审计_真几何扭转模式约束与NO-GO存活检验_2026-11-01.md"
HTML = "四力统一方程_XR318-1真扭转约束与NOGO存活可视化_2026-11-01.html"

with io.open(README, "r", encoding="utf-8") as f:
    old = f.read()

if "TUFT-r322_" in old:
    print("SKIP: README 已含 r322")
    raise SystemExit(0)

block = """### r322 · 2026-11-01 · X-R318-1 审计 · 真几何扭转的模式约束与 r318 反例的存活检验（NO-GO 未被约束复活）（★攻 r318 薄弱点 · 承 r306/r307/r309/r318 判词链 · 判词链第 9 层）

- **产物**：源码 [`%s`](源码/%s)；数据 [`…json`](数据/%s.json) / [`…md`](数据/%s.md) / [`…_report.txt`](数据/%s_report.txt)；判定册 [`%s`](判定/%s)；runner `源码/_run_r322.py` → `源码/_out_r322.txt`；交互可视化 [`%s`](%s)
- **复现**：`python -X utf8 源码\\_run_r322.py` ⇒ **rc=0**，条目 **22**（主 **8**：**PASS 6 / INFO 2**，FAIL 0），**控制组 4/4**，**守卫 10/10**，纯整数行列式因子 + Fraction 精确，耗时约 14 s。
- **核心发现**：r318 的薄弱点 = P2 默认「任意 0/1 模式合法」。本卷施加**可证结构约束** `k_{u^c}=k_{d^c}`、`k_{e^c}=k_{ν^c}`（同中心荷 ⇒ 同 k；r307 Thm N + r309 Thm U）⇒ 约束集 = 2^4 = **16** 个；其中 N=3 可解 = **4**（`{g0=1,g3=1,g1=g2,g4=g5}`）；r318 显式构造 g=(1,0,0,1,0,0) 满足约束且 **A·t=3·𝟙 存活**；N=1..12 在约束下仍全可及（`g_for_N` 自动满足约束，因 d_{u^c}=d_{d^c}=3、d_{e^c}=d_{ν^c}=1）。
- **判词**：**NO-GO-NOT-RESURRECTED-BY-CONSTRAINT** —— 结构约束把 N=3 可解面由 16 缩到 4（非零），r318 反例存活，N 自由仍成立 ⇒ `NO-GO-DOWNGRADED-TO-FREE` 在真扭转结构约束下**不被动摇**；框架仍**不预言** 3（3 是扭转份数 Y 的拓扑输入）。**r298→…→r318→r322 判词链：第 9 层 = 用真扭转结构约束给 r318 反例做存活检验，结论「存活」。** 遗留 X-R322-1（给定具体轨道模型，其**全群元约束**能否排除那 4 个可解模式——复活 NO-GO 的唯一可能）/ X-R318-1（Y 能否被动力学/拓扑自然固定为 3）/ X-R296-3、X-R296-1。
- **取号**：落盘前实测 r319（齐套）/ r320（仅 src）/ r321（src+dat）已被并行占，**r322/r323/r324 全空** ⇒ 取 **r322**（源码先落占号）。**治理**：未改 verify.py；未跑 refresh_catalog.py；未改任何既有卷字节（G9 逐路径核验仅写本卷产物）；README 仅追加大本条目（按 r310–r318 现行 detail-only 惯例）。**下轮从 r324 复查起（并行链极活跃，取号前必扫三树 + README detail）。**
""" % (SRC, SRC, DATA, DATA, DATA, JUD, JUD, HTML, HTML)

bak = os.path.join(BASE, "README.bak_%s_%s.md" % (RID, datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
if not os.path.exists(bak):
    with io.open(bak, "w", encoding="utf-8") as f:
        f.write(old)

sep = "" if old.endswith("\n\n") else ("\n" if old.endswith("\n") else "\n\n")
new = old + sep + block + "\n"

with io.open(README, "w", encoding="utf-8") as f:
    f.write(new)

old_lines = old.splitlines()
new_lines = new.splitlines()
prefix_ok = new_lines[:len(old_lines)] == old_lines
n_detail = sum(1 for ln in new_lines if ln.startswith("### r322 ·"))
n_src = sum(1 for ln in new_lines if "TUFT-r322_" in ln)
print("BAK:", os.path.basename(bak))
print("prefix_preserved(零删除):", prefix_ok)
print("detail anchors '### r322 ·':", n_detail)
print("lines with TUFT-r322_:", n_src)
print("RESULT:", "PASS" if (prefix_ok and n_detail == 1) else "FAIL")
