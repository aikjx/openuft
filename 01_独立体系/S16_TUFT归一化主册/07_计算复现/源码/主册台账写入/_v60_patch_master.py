# -*- coding: utf-8 -*-
"""主册头部升 v7.1->v7.2：改标题 + 插入 v7.2 块（不动 v7.1 块及以下）。"""
import io
P = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\主册\TUFT_归一化主册_v1.0.md"
t = io.open(P, encoding="utf-8").read()
lines = t.split("\n")

assert "主册 v7.1" in lines[0], "title v7.1 not found"
lines[0] = lines[0].replace("主册 v7.1", "主册 v7.2", 1)
assert "E1–E509" in lines[0], "E1-E509 not in title"
lines[0] = lines[0].replace("E1–E509", "E1–E510")

v72 = """
> **★★ v7.2（v60 泛音 n=1 独立通道检验轮：基模 n0 被否后高阶模 n=1 是否还有意外——独立高斯似然，n1 频率残差 med=−5%±20%(GR 侧)，TUFT +16.26% 仅 1.06σ、不显著排除；阻尼未约束；n1 兼容 GR 但未达分辨力，无孤例、不复活理论，2026-09-26，append-only；数字照抄原始输出，三结局都照写，不夸大为第三重独立排除）**：先 Read 磁盘 SSOT（v7.1/E1–E509/勘误#42）及 v56 观测报告/v58/v59 似然脚本（作方法模板不 import）。磁盘起点 **v7.1/E1–E509/勘误#42**，本轮升 **v7.2/E1–E510/勘误#42 held（本轮无新勘误）**；物理四态 **35/61/18/27 冻结**。
>
> **① 方法（独立脚本 `_audit_v60_overtone_likelihood.py`，不 import v56/v57/v58/v59，纯标准库 math；Kerr (2,2,1) 表由 qnm 0.4.4 独立复算硬编码，a=0 锚 0.346710996879−0.273914875291i 与 SSOT 吻合 12 位；数字照抄 `_out.txt`）**：n1 频移 H0: δf=0(GR) vs H1: δf=+16.26%(TUFT v32 与 n0 同比例)；阻尼 H0: δτ=0 vs H1: δτ=+57.6%(τ比=1.576 同 n0)。
>
> **② 数据（唯一已发表 n1 直接测量=GW150914 单事件）**：Isi et al. 2019 PRL 123 111102（**arXiv:1905.00869**；任务括号 1909.06188 系误植已透明校正，不改 SSOT 数）无毛发检验：δf1=−0.05±0.20(68%=1σ=20%)；δτ1 未约束 [−6%,+100%]；无毛 vs 浮动 BF=1.75。Estelles2023(arXiv:2104.01906) 仅测 n0、泛音固定 GR；Capano2021(arXiv:2105.05238)=GW190521 (3,3,0) 非 n1。泛音探测本身不鲁棒：全边缘化后 BF 仅 2.3±0.1（PRD110 L041501/2024）。GR 归算：(68M☉,χ=0.63) f221^GR=233.3 Hz、τ221^GR=1.332 ms。
>
> **③ 合并结果**：n1 频率 med=−5%±20%，ΔlnL=−0.534、BF=0.586、**−2.32 dB**（弱偏 GR），H1=+16.26% 距 med=1.06σ；保守 1σ×1.5→−1.03 dB/0.71σ；最乐观 c_m 端 +8.82%→−0.90 dB/0.69σ。n1 阻尼（中心=无毛模 0%，σ=32.2%）：ΔlnL=−1.60、−6.94 dB、H1=+57.6% 距 1.79σ；×1.5→−3.09/1.19σ；最乐观 +47.5%→−4.72/1.48σ。
>
> **④ 三结局照写**：(1) n1 也排除？否（1.06σ/1.79σ 均不显著）；(2) n1 兼容 GR、偏离 TUFT？是——残差 med=−5%(GR 侧，距 GR 仅 0.25σ)，无正频移/长阻尼指向 TUFT，与 n0 同向，但分辨力不足不能独立排除；(3) n1 反贴近 TUFT(孤例)？否——med=−5% 而非 +16%。
>
> **⑤ 三通道总判定**：n0 频率 5.86σ + n0 阻尼 5.59σ 已干净否定 TUFT 复谱；n1 高阶模落在 GR 侧(−5%)但 1σ=20% 太宽、探测不鲁棒(BF~2.3)，**既不能独立排除 TUFT，也不构成复活证据，与 n0 无矛盾**。不据 n1 复活理论，也不据 n1 夸大为第三重独立排除。
>
> **⑥ E510（泛音 n=1 独立通道：唯一测量 GW150914 δf1=−5%±20% 落在 GR 侧，TUFT +16.26% 仅 1.06σ 不显著排除、阻尼未约束；兼容 GR/未达分辨力/无孤例/不复活）**：观测似然对照通道，**不闭合新物理 E 数进四态**；勘误 #42 held；四态 35/61/18/27 冻结。open_backlog 不变：TUFT 静态 11.6 位硬门 OPEN；旋转绝对值 1.62 无外部 Grade-A 锚；a≥0.2 慢转 O(a²)~3–4%；5 升层项 OPEN；观测侧 n0 复谱双通道已排除（待 O4/Voyager 高 ringdown-SNR 破 M–χ–overtone 简并复核 n1）。本轮交付：《TUFT_v60_泛音n1检验合并报告.md》、脚本 `_audit_v60_overtone_likelihood.py`/`_out.txt`；openuft 第66章 append §66.23。
"""

new = "\n".join(lines[:2]) + v72 + "\n".join(lines[2:])
io.open(P, "w", encoding="utf-8").write(new)

chk = io.open(P, encoding="utf-8").read()
print("title v7.2:", "主册 v7.2" in chk)
print("E1–E510 in title:", "E1–E510" in chk)
print("v7.2 block present:", "v7.2（v60 泛音" in chk)
print("v7.1 block retained:", "v7.1（v59 阻尼" in chk)
print("E510 count:", chk.count("E510"))
print("len() now:", len(chk))
