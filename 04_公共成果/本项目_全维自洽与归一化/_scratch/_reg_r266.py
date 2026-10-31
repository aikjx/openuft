# -*- coding: utf-8 -*-
# 幂等注册 TUFT-r266 四处（源码树/判定树/compact/full），锚定 r265 行，保 CRLF。
# 纪律：已存在则不动；落盘后从磁盘读回核验四树计数各=1、死链=0、链接可解析。
import io, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(BASE, "README.md")
BAK = os.path.join(BASE, "_scratch", "_README_before_r266_reg.md")
SRC_N = "TUFT-r266_力的大统一方程层_数值复现与几何本源定义恒等式及Yukawa模板拆解_精算与可视化_2026-10-31"
SHORT = "力的大统一方程层"

# ---- 锚点（r265 四处条目，必须唯一） ----
ANCH = {
 "SRC": "│   ├── TUFT-r265_引力波预言层_标准模型弱一阶误判与相变参数全缺_LISA可探测边界与谱畸变零判别力_精算与可视化_2026-10-31.py",
 "JUD": "├── 判定_TUFT-r265_引力波预言层_标准模型弱一阶误判与相变参数全缺_LISA可探测边界与谱畸变零判别力_精算与可视化_2026-10-31.md",
 "CPT": "- **r265（2026-10-31）· 引力波预言层：SM 弱一阶误判 / 相变参数全缺 / LISA 可探测边界 / 谱畸变零判别力（★引力波预言层首卷）**：",
 "FUL": "- **取号（撞号第 10 次）**：落盘前实测 r263/r264 已被并行链占用，r265/r266/r267 三树为空 ⇒ 取 r265。**下轮从 r266 起**。",
}

# ---- r266 插入块（每行为独立字符串，写回时统一加 \r） ----
BLK = {
"SRC": [
 "│   ├── %s.py  # 新增（**r266 · 2026-10-31**）：**%s（V9.3 第九章）（★新层）**—— 审计 §9.1–9.8 全部数值声称。条目 10（PASS 10 / FAIL 0），**控制组 4/4**、**守卫 5/5**、rc=0。★承重：§9.4 F_E=230.71 N / F_G=−1.867e-34 N / 比值 1.2356e36 与独立 SI 库仑/牛顿重算一致；§9.3 强/弱力程 λ 即 π⁰/W 康普顿波长（标准）；§9.6 弱力灭绝 e^{-1/λ_W}=1.12e-177（书 1.25e-177，≈12%% 取整，量级一致）；§9.8 V1–V7 自检表全部可独立复现。★结构判词：『力的大统一』= Yukawa/Proca 模板重包装（力程 λ 即媒介子康普顿波长），非第一性原理推导；几何本源(V7)=定义恒等式（残差精确 0），与 r264「内生=0」一致；★**书诚实声明玩具耦合（g²=179.7、g_W²=1 仅方法演示）与常数层开放（自承 B01–B03）**。★修复定价 2^1=2：SURVIVE 2 / SUICIDE 0 ⇒ **SURVIVE>0 ⇒ 不占「修复即自杀」度数**；候选 37 度但不计。" % (SRC_N, SHORT),
],
"JUD": [
 "├── 判定_%s.md  # 新增（**r266 · 2026-10-31**）：%s判定册 —— §判词 · §逐条判定表（10 量化声明全 PASS）· §控制组 4/4 · §守卫 5/5 · §结构发现（Yukawa 模板重包装 / V7 定义恒等式 / 书诚实声明）· §对靶有利 2 条 · §定价（SURVIVE>0，不占度）。" % (SRC_N, SHORT),
],
"CPT": [
 "- **r266（2026-10-31）· %s：数值复现高保真 / Yukawa 模板重包装 / V7 几何本源定义恒等式 / 弱力灭绝~12%% 取整偏差（★新层）**：审计第九章 §9.1–9.8 全部数值声称（§9.3 四力还原表、§9.4 F_E/F_G/比值、§9.6 普适曲线与弱力灭绝、§9.8 V1–V7 自检表）。条目 10（PASS 10 / FAIL 0），控制组 4/4，守卫 5/5，rc=0；源码 [`TUFT-r266_…py`](源码/%s.py)；判定册 [`…md`](数据/判定_%s.md)；数据 [`…json`](数据/%s.json) / [`…_report.txt`](数据/%s_report.txt)。★★★**数值复现高保真**：§9.4 的 F_E=230.71 N / F_G=−1.867e-34 N / 比值 1.2356e36 与独立 SI 库仑/牛顿重算完全一致；§9.3 强/弱力程 λ 即 π⁰/W 康普顿波长（标准物理）。★★★**结构判词：『力的大统一』= Yukawa/Proca 模板重包装**——四力共用 F=s ħc q₁q₂(1/r²+1/(λr))e^{-r/λ}，力程差别仅由 λ（媒介子康普顿波长）决定，非第一性原理推导。★★**几何本源(V7)=定义恒等式**：q_G=m/m_P（m=ħω/c²）代入统一式即 F=G m₁m₂/r²，残差精确 0；与 r264「内生=0」一致，常数层仍外部输入（书自承 B01–B03）。★**书诚实声明玩具耦合**（g²=179.7、g_W²=1 仅方法演示，非真实耦合）与边界 ⇒ 非隐藏缺陷（对靶有利）。★**唯一诚实偏差**：弱力灭绝因子书值 1.25e-177 vs 精确 1.12e-177（≈12%% 取整），连带 T9 弱力玩具 1.6e-170 vs 1.44e-170（≈10%%）；量级与框架结论（指数灭绝~10^-177）一致，非结构错误。★修复定价 2^1=2：SURVIVE 2 / SUICIDE 0 ⇒ **SURVIVE>0 ⇒ 不占度数链**；候选 37 度但不计。" % (SHORT, SRC_N, SRC_N, SRC_N, SRC_N),
],
"FUL": [
 "### r266 · 2026-10-31 · %s：数值复现高保真、Yukawa 模板重包装、V7 几何本源定义恒等式、弱力灭绝~12%% 取整偏差（★新层）" % SHORT,
 "",
 "- **产物**：源码 [`TUFT-r266_…py`](源码/%s.py)；数据 [`…json`](数据/%s.json) / [`…_report.txt`](数据/%s_report.txt)；判定册 [`判定_…md`](数据/判定_%s.md)。（纯数值复现层，无交互可视化。）" % (SRC_N, SRC_N, SRC_N, SRC_N),
 "- **复现**：`python -X utf8 源码/%s.py` ⇒ **rc=0**，条目 **10**（**PASS 10 / FAIL 0**），**控制组 4/4**，**守卫 5/5**。" % SRC_N,
 "- **结论**：第九章「力的大统一方程」属数值复现层，靶全部数值声称与独立标准物理重算一致；结构判词为 Yukawa/Proca 模板重包装 + V7 几何本源定义恒等式（残差 0），与 r264「内生=0」呼应；书诚实声明玩具耦合与常数层开放。**SURVIVE>0 ⇒ 不占「修复即自杀」度数链**（候选 37 度不计）。",
 "- **取号**：落盘前实测 r266/r267/r268 三树为空（锚点串核验，非裸 `grep -cF` 误报）⇒ 取 r266。**下轮从 r267 起**（★落盘前必须再实测；度数须经 G13/GU08 机器核定）。",
],
}

# ---- 读盘（保 CRLF） ----
if not os.path.exists(BAK):
    import shutil; shutil.copy(P, BAK)
lines = list(io.open(P, encoding="utf-8", newline=""))

# 幂等：若四处已存在则报错退出（不应发生）
for key, anchor in ANCH.items():
    if any(SRC_N in ln for ln in lines):
        sys.stderr.write("ALREADY REGISTERED: %s\n" % SRC_N); sys.exit(3)

for key, anchor in ANCH.items():
    hits = [i for i, ln in enumerate(lines) if ln.startswith(anchor)]
    if len(hits) != 1:
        sys.stderr.write("ANCHOR NOT UNIQUE / NOT FOUND: %s -> %d\n" % (key, len(hits))); sys.exit(2)
    idx = hits[0]
    block = BLK[key]
    for j, piece in enumerate(reversed(block)):
        lines.insert(idx + 1 + j, piece + "\r")   # 加 \r 与周围 CRLF 一致

# ---- 写回（\n 连接；每行列已有 \r ⇒ 全文件 \r\n） ----
io.open(P, "w", encoding="utf-8", newline="").write("\n".join(lines) + "\n")

# ---- 落盘后从磁盘读回核验 ----
import subprocess
def cnt(pat):
    out = subprocess.run(["grep","-cF",pat,P],capture_output=True,text=True).stdout.strip()
    return int(out) if out.isdigit() else 0
checks = {
 "SRC_TREE": ("│   ├── TUFT-r266_", 1),
 "JUD_TREE": ("├── 判定_TUFT-r266_", 1),
 "COMPACT":  ("**r266（2026-10-31）", 1),
 "FULL":     ("### r266 · 2026-10-31", 1),
 "DEADLINK": ("]](判定/判定_TUFT-r266".replace("]]", "]("), 0),
}
ok = True
for name,(pat,exp) in checks.items():
    c = cnt(pat)
    flag = "OK" if c==exp else "BAD"
    if c!=exp: ok=False
    print("%-10s pat=%r exp=%d got=%d %s" % (name, pat[:28], exp, c, flag))

# 链接可解析性
import re
txt = io.open(P, encoding="utf-8", newline="").read()
links = re.findall(r"\]\((数据/判定_%s\.md|源码/%s\.py|数据/%s\.json|数据/%s_report\.txt)\)" % (SRC_N,SRC_N,SRC_N,SRC_N), txt)
for rel in set(links):
    fp = os.path.join(BASE, rel)
    print("LINK %-60s %s" % (rel, "EXISTS" if os.path.exists(fp) else "MISSING"))

# CRLF 全量
cr = subprocess.run(["grep","-c",r"\r", P], capture_output=True, text=True).stdout.strip()
print("CRLF lines (grep -c '\\r'):", cr)
print("REGISTRATION", "SUCCESS" if ok else "FAILED")
sys.exit(0 if ok else 1)
