# -*- coding: utf-8 -*-
"""r330 README 注册（detail-only 追加，零删除）。"""
import io, os, datetime

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(BASE, "README.md")
RID = "r330"

SRC = "TUFT-r330_口径审计_六自由电荷vs反常自由一维与N自由的真实性_精算与可视化_2026-11-01.py"
DATA = "TUFT-r330_口径审计_六自由电荷vs反常自由一维与N自由的真实性_精算与可视化_2026-11-01"
JUD = "判定_TUFT-r330_口径审计_六自由电荷vs反常自由一维与N自由的真实性_2026-11-01.md"
HTML = "四力统一方程_反常自由口径审计与N自由真实性可视化_2026-11-01.html"

with io.open(README, "r", encoding="utf-8") as f:
    old = f.read()

if "TUFT-r330_" in old:
    print("SKIP: README 已含 r330")
    raise SystemExit(0)

block = """### r330 · 2026-11-01 · 口径审计 · 六自由电荷 vs 反常自由一维超荷（★攻 r306/r318/r322 自身口径 · 判词下调 · 承 r305/r307/r309/r318/r322 判词链 · 判词链第 10 层）

- **产物**：源码 [`%s`](源码/%s)；数据 [`…json`](数据/%s.json) / [`…md`](数据/%s.md) / [`…_report.txt`](数据/%s_report.txt)；判定册 [`%s`](判定/%s)；runner `源码/_run_r330.py` → `源码/_out_r330.txt`；交互可视化 [`%s`](%s)
- **复现**：`python -X utf8 源码\\_run_r330.py` ⇒ **rc=0**，条目 **27**（主 **10**：**PASS 7 / INFO 3**，FAIL 0），**控制组 6/6**，**守卫 11/11**，纯整数行列式因子 + Fraction 精确，秒级完成；HTML 几何体检 **GEOMETRY-OK**（680×400，29 图元）+ 负对照（回填 `width:0` ⇒ 精确报「rect(fill=#f0fff4) 宽度为 0 ⇒ 不可见」、rc=1）。
- **本卷攻自己**：r306/r318/r322 的 `A=diag(d_i)` 是 **6 维自由电荷**（=任意电荷、**破反常自由**）。但 r305 Thm S（r309 Thm S 加固）证：反常自由下荷空间严格 **1 维且就是 span(Y)**，即 `X_i = Y_i·M`（单通量），不是 6 个独立自由度。⇒ 必须机检「N 自由」是否只是电荷模型自由度的假象。
- **核心读数（全部机算）**：① m=6（r318 模型）N=3 可解 **16/64**，其中**非平凡 15**；② m=1（反常自由）N=3 可解 **1/64**，唯一解 `g=全1`、`t=(M,Ytw)=(0,3)`，**非平凡解 = 0**；③ r318 的 `X=(0,1,1,0,3,3)` **不平行于 Y**（`Y_ν=0` 而 `X_ν=3`）⇒ 其构造破反常自由；④ 用 m=6 的 `g0=(1,0,0,1,0,0)` 反解出 `X_i=(0,1,1,0,3,3)`，与 r318 **独立吻合**；⑤ 笨办法（直接枚举整数 Ytw/M，不经行列式判据）对 128 实例与行列式判决**全一致**（G4），避免 r309 式「同源回验抓不到同源错误」。
- **新定理（P9，比 r306/r318 更硬的机制定位）**：要「纯通量给出每代一份」，须 `d_i·Y_i ≡ 常数`。候选 `Y^eq_i = 1/d_i` 的四条反常 = **(1/2, 1/2, 6, 5/2) 全非零 ⇒ 破反常自由**；反之反常自由强制 `d_i·Y_i ∝ (1,−2,1,−1,1,0)`，**含负项（位 1: u^c=−2、位 3: L=−1）与零项（位 5: ν^c=0）** ⇒ 恒非常数。⇒ **挡住「通量给三代」的不是通量自由度不足，而是超荷非均匀性**；且「等指标超荷」与「反常自由」**互斥**。
- **判词**：**EQUAL-INDEX-UNDER-ANOMALY-FREEDOM-IMPOSSIBLE / N-FREE-IS-ANOMALY-VIOLATING-ARTIFACT** —— r318 `NO-GO-DOWNGRADED-TO-FREE`、r322 `NO-GO-NOT-RESURRECTED` **均在 m=6（破反常自由）模型内成立**；反常自由最小 SM 下 N=3 非平凡解 = 0，只剩全向复制（=注入 3）。净结论回到与 r305/r307/r309 一致：**本框架不预言 3**，「N 自由」是电荷模型自由度的假象。遗留 `X-R330-1`（m≥2 额外反常自由 U(1) 下 N=3 是否重可达）/ `X-R330-2`（表示数 5 vs 6 的差异，r302 用 5、r296/r306 用 6）/ `X-R322-1` / `X-R318-1`。
- **自伤登记（G11 机器门禁）**：首版两条负对照（「把 `d_iY_i` 第 5 位 1→2」「给 ν^c 非零超荷」）**读数都是 1，与基线完全相同 = 恒绿**。根因：「全 1 复制解」在 `M=0` 下条件退化为 `g_i·Ytw=N`，**对超荷取值完全盲**。⇒ 已换三档能真移动的负对照（`d_i` 全 4 → 非平凡 **0**；`d_i` 全 3 → **63**；等指标超荷 → **63**，基线 **15**），并加门禁：任一档读数等于基线即 FAIL。**恒绿的负对照比没有更危险。**
- **取号**：落盘前实测 r319–r326 全被并行链占，且 `_probe_r327.py`（14:13）显示另一会话正在探 r327 ⇒ 主动避开热区，取 **r330**（r328/r329 留空，src 树跳号正常）。**治理**：未改 verify.py；未跑 refresh_catalog.py；未改任何既有卷字节（G9 逐路径核验仅写本卷产物）；README 仅追加大本条目（按 r310+ 现行 detail-only 惯例）。**下轮从 r331 复查起（并行链极活跃，取号前必扫三树 + README detail）。**
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
n_detail = sum(1 for ln in new_lines if ln.startswith("### r330 ·"))
n_src = sum(1 for ln in new_lines if "TUFT-r330_" in ln)
print("BAK:", os.path.basename(bak))
print("prefix_preserved(零删除):", prefix_ok)
print("detail anchors '### r330 ·':", n_detail)
print("lines with TUFT-r330_:", n_src)
print("RESULT:", "PASS" if (prefix_ok and n_detail == 1) else "FAIL")
