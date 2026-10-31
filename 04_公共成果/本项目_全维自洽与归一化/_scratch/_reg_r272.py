# -*- coding: utf-8 -*-
"""幂等注册 r272 到 README 四处（源码树/判定册树/增量章compact/增量章full）。
插入锚点：r270 对应四行的紧后。保留原文件换行符（CRLF/LF 自动探测）。
"""
import io, shutil, sys, os

BASE = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化"
README = os.path.join(BASE, "README.md")
BACKUP = os.path.join(BASE, "_scratch", "_README_before_r272_reg.md")

S = "LW推迟势数值验证层_标准电动力学独立复算与衰减律辐射功率kappa平方及v等c奇点_精算与可视化_2026-10-31"

src_line = ("│   ├── TUFT-r272_%s.py  # 新增（**r272 · 2026-10-31**）：**LW 推迟势数值验证层（V9.6 / 第十二章 12.10）**"
            "—— 从标准 Liénard-Wiechert 公式第一性独立重算，不调用靶书脚本；审计靶书四项数值声称 "
            "[A]衰减律 [B]推迟功率=Liénard [C]P∝κ² [D]v=c 奇点。条目 7（PASS 7 / FAIL 0），**控制组 3/3**、**守卫 6/6**、rc=0。"
            "★承重：四声称全高保真复现（P=0.3306255 vs Liénard 0.3306222，相对 9.84e-6；斜率 −2/−1 机器精度；"
            "P∝κ² 斜率 1.00001；v=c 时 (1−n·β)→0 ⇒ LW 奇异）。★结构判词：『LW 验证』= 标准电动力学的忠实重算，非 TUFT 专属预言；"
            "靶书自承「v=c 本源场元不能作 LW 源」，LW 对标仅适用亚光速复合体世界线 ⇒ 基本 v=c 源被排除。"
            "★修复定价 2^4=16：SURVIVE 16 / SUICIDE 0 ⇒ **SURVIVE>0 ⇒ 不占度数**；候选 37 度但不计。") % S

jud_line = ("├── 判定_TUFT-r272_%s.md  # 新增（**r272 · 2026-10-31**）：LW 推迟势数值验证层判定册 —— "
            "§结论 · §逐条判定表（7 声称全 PASS）· §控制组 3/3（含负对照证判别力）· §守卫 6/6 · "
            "§结构判词（标准 EM 忠实重算 / v=c 奇点 no-go / 判别性 0）· §定价（SURVIVE>0，不占度）。") % S

cpt_line = ("- **r272（2026-10-31）· LW 推迟势数值验证层：标准电动力学独立复算、衰减律 −2/−1、推迟功率=Liénard、"
            "P∝κ²、v=c 奇点（★新层 · 由 r271 改号）**：审计第十二章 V9.6.1 四项数值声称。条目 7（PASS 7 / FAIL 0），"
            "控制组 3/3，守卫 6/6，rc=0；源码 [`TUFT-r272_…py`](源码/TUFT-r272_%s.py)；"
            "判定册 [`…md`](数据/判定_TUFT-r272_%s.md)；"
            "数据 [`…json`](数据/TUFT-r272_%s.json) / [`…_report.txt`](数据/TUFT-r272_%s_report.txt)。"
            "★★**四声称全高保真复现**（P=0.3306255 vs Liénard 0.3306222，相对 9.84e-6；衰减律斜率 −2.000000000/−1.000000000 机器精度；"
            "P∝κ² 斜率 1.00001；v=c 时 min(1−n·β)=0 ⇒ LW 分母 (1−n·β)³ 奇异）。"
            "★★**结构判词：『LW 验证』= 标准经典电动力学的忠实重算，非 TUFT 专属预言**——靶书自承「v=c 本源场元不能直接作 LW 源」，"
            "LW 对标仅适用于亚光速复合体世界线，基本 v=c 源被排除在 LW 描述之外 ⇒ 判别性 0（与 r266 Yukawa 模板重包装同构）。"
            "★修复定价 2^4=16：SURVIVE 16 / SUICIDE 0 ⇒ **SURVIVE>0 ⇒ 不占度数**；候选 37 度但不计。") % (S, S, S, S)

full_block = [
    "### r272 · 2026-10-31 · LW 推迟势数值验证层：标准电动力学独立复算、衰减律 −2/−1、推迟功率=Liénard、P∝κ²、v=c 奇点（★由 r271 改号）",
    "- **产物**：源码 [`TUFT-r272_…py`](源码/TUFT-r272_%s.py)；数据 [`…json`](数据/TUFT-r272_%s.json) / [`…_report.txt`](数据/TUFT-r272_%s_report.txt)；判定册 [`判定_…md`](数据/判定_TUFT-r272_%s.md)。" % (S, S, S, S),
    "- **复现**：`python -X utf8 源码/TUFT-r272_…py` ⇒ **rc=0**，条目 **7**（**PASS 7 / FAIL 0**），**控制组 3/3**，**守卫 6/6**。负对照（省略 γ⁴）相对偏差 49.6%% ⇒ 判据有真实分辨力。",
    "- **结论一句话**：靶书 Ch.12/V9.6.1 四项 LW 数值声称 [A]衰减律 [B]推迟功率=Liénard [C]P∝κ² [D]v=c 奇点 **全部被独立复算证实**，但这是标准经典电动力学的忠实重算，非 TUFT 专属预言；基本 v=c 源被 LW 奇点排除 ⇒ 判别性 0。",
    "- **取号**：起草时 r271 已被并行会话占用（《时空曲率比攻坚_K1除K2=β洛伦兹不变_三维候选剪枝定理与二次能量否定》来料原件 16:46 早于本卷 16:57）⇒ 整体迁 **r272**，未改动他卷任何字节。**下轮从 r273 复查起**。",
]

# ---- 幂等检查 ----
with io.open(README, "r", encoding="utf-8", newline="") as f:
    text0 = f.read()
if "TUFT-r272_%s" % S in text0:
    print("ALREADY REGISTERED — abort (idempotent).")
    sys.exit(0)

# 备份
shutil.copy2(README, BACKUP)

with io.open(README, "r", encoding="utf-8", newline="") as f:
    lines = f.readlines()

# 探测换行符
ending = "\r\n" if lines and lines[0].endswith("\r\n") else "\n"

def find_idx(prefix):
    for i, ln in enumerate(lines):
        if ln.startswith(prefix):
            return i
    raise RuntimeError("anchor not found: " + prefix)

src_i = find_idx("│   ├── TUFT-r270_可机检验收规范层")
jud_i = find_idx("├── 判定_TUFT-r270_可机检验收规范层")
cpt_i = find_idx("- **r270（")
full_i = find_idx("### r270 ·")

# 插入（从后往前，保持索引有效）
new = list(lines)
new.insert(full_i + 1, ending.join(full_block) + ending)
new.insert(cpt_i + 1, cpt_line + ending)
new.insert(jud_i + 1, jud_line + ending)
new.insert(src_i + 1, src_line + ending)

with io.open(README, "w", encoding="utf-8", newline="") as f:
    f.write("".join(new))

# ---- 验证 ----
with io.open(README, "r", encoding="utf-8", newline="") as f:
    text = f.read()
checks = {
    "src":  text.count("│   ├── TUFT-r272_%s" % S),
    "jud":  text.count("├── 判定_TUFT-r272_%s" % S),
    "cpt":  text.count("**r272（"),
    "ful":  text.count("### r272 ·"),
}
print("注册后四树计数:", checks)
deadlink = text.count("](判定/判定_TUFT-r272_")  # 死链模式应为 0
print("疑似死链计数(应为0):", deadlink)
print("BACKUP:", BACKUP)
