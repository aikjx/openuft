# -*- coding: utf-8 -*-
"""README 幂等登记脚本 · TUFT-r289
纪律：
  1) 锚点串必须含本卷 RID（禁用通用前缀，防整条覆盖他人记录）
  2) 先判「本卷条目是否已存在」再分流（存在=跳过，不存在=插入），不混为一步
  3) 写后从磁盘读回，逐处清点 = 1
  4) 备份只在首次创建、不覆盖
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
README = os.path.join(ROOT, "README.md")
SCRATCH = os.path.join(ROOT, "_scratch")
BACKUP = os.path.join(SCRATCH, "_README_before_r289_reg.md")

RID = "r289"
PY_NAME = ("TUFT-r289_KK电荷质量排除定理审计_二参数唯一解快子与真空能10的117次方灾难"
           "_精算与可视化_2026-10-31.py")
MD_NAME = ("TUFT-r289_KK电荷质量排除定理审计_二参数唯一解快子与真空能10的117次方灾难"
           "_2026-10-31.md")
JSON_NAME = MD_NAME.replace(".md", ".json")
JUD_NAME = ("判定_TUFT-r289_KK电荷质量排除定理审计_二参数唯一解快子与真空能10的117次方灾难"
            "_2026-10-31.md")

SRC_LINE = (
    "│   ├── " + PY_NAME + "  # 新增（**r289 · 2026-10-31**）："
    "**审计《ROOT V13.0》五维 KK 电荷—质量同源排除定理（★外部来料审计层）**——"
    "来料 §一–§八 的全部算术与代数**逐项命中**（表 10 行 / 势 3 行 / 恒等式 1 条 / QED 系数 1 条；"
    "最大相对偏差 **5.7e-6**，仅来自 ħ 末位口径）。条目 **49**（PASS 41 / FAIL 0 / INFO 6 / BOUNDARY 2）、"
    "**控制组 8/8**、**守卫 9/9**、rc=0。"
    "★★★**三处增量（来料均未做）**：①**唯一解是快子而非超定无解**——模型实为 **2 无量纲参数对 2 观测**，"
    "反解 m5^2/m_e^2=**−1.0414e42**（虚质量），且 |m5^2|/(1/R)^2=**1−9.6e−43**"
    "（与 KK 能隙几乎精确相等，不是微调而是精确反向）；②**真空能量级**——来料只登记 V(x*)<0 未给量级，"
    "本卷补 a 取 Casimir 标度 M_P^4 ⇒ |V_min|/ρ_Λ=**9.74e116**（SM 自由度数 ~100 时约 1e119），"
    "与 r258 的 10^120.74 **同构异源**；③**10000 组随机测试零判别力**——该不等式即 m5^2≥0 的改写，"
    "本卷复现 0/10000 违反并补负对照（m5^2<0 支 **10000/10000 全违反**）证其牙齿。"
    "★★**结构判词**：控制组 CTL2 证明**任意单尺度玩具** α=k·l_P^2/R^2 必得 α/(4α_g)=k ⇒ 该「排除定理」是"
    "**单尺度方案的普遍不可能性**，非 KK 特性（适用范围比来料自述更广、也因此更不稀奇）；"
    "CTL3 给出逃逸路径（两尺度 R_α=23.41 l_P、R_m=2.389e22 l_P 可同时匹配）= §八 自述方向 = "
    "RS/ADD + flux compactification 标准组合 ⇒ **ROOT 在此收敛到教科书**。"
    "★三项「可保留成果」独立信息量 **0 bit**（1940s KK 已知 + 计数必然）。"
    "★对靶有利照登：三表 10 行全对、势解析全对、β=2/(3π) 对单费米子正确、主动登记「唯一数值预测未完成」。"
    "★定价 4 槽 2^4=16：严格 SURVIVE **0** / 宽松 **1** / SUICIDE 8 / EMPTY 7 ⇒ **SURVIVE>0 ⇒ 不占度数链**"
    "（候选 37 度，链仍止 r264:36）。"
    "★开发期自抓 2 处（B02 期望值 4.858e-8→4.8574e-8 被 2e-5 容差抓出；A13 容差 1e-45 误设，"
    "实测 6.8e-19 为 1e-3 量级两项相减的 Decimal 抵消地板，已改 1e-15 并注明）。"
)

JUD_LINE = (
    "├── " + JUD_NAME + "  # 新增（**r289 · 2026-10-31**）：ROOT V13.0 五维 KK 排除定理判定册 —— "
    "§判决主文（算术全对 / 定理成立 / 新物理增量 0）· §承重三增量（快子唯一解 / 9.74e116 真空能 / "
    "随机测试无判别力）· §来料做对的五项照登 · §未做三层 · §结构判词（单尺度普遍不可能性 · "
    "三项成果 0 bit · 收敛到教科书）· §控制组 8/8 与定价 16 组合（严格 0 / 宽松 1 ⇒ 不占度）· "
    "§来源体检（favicon 占位引用 + PDG 非官方域名带 utm_source，NO-VERIFY，不影响判决）· "
    "§诚实边界 B1–B5 · §与 r243/r258/r264/r284/r287 关系 · 终判 **SURVIVE_MATH__FAIL_NOVELTY**"
)

DATA_LINE = (
    "    ├── " + JSON_NAME.replace(".json", ".json / .md / _report.txt") +
    "  # 新增（**r289 · 2026-10-31**）ROOT V13.0 审计机读产物：49 条目逐条 expected/actual/verdict/note、"
    "8 控制组（CTL2 单尺度必然性 / CTL3 两尺度逃逸 / CTL7 表值容差牙齿 / CTL8 真空能阈值非恒真）、"
    "9 守卫、4 槽定价 16 组合；来料原件逐字另存 "
    "`…_来料原件_ROOT_V13.0_用户附件逐字_2026-10-31.md`"
)

COMPACT_LINE = (
    "- **r289（2026-10-31）· ROOT V13.0 五维 KK 电荷—质量排除定理审计（★外部来料审计层）**："
    "条目 **49**（PASS 41 / FAIL 0 / INFO 6 / BOUNDARY 2）、控制组 **8/8**、守卫 **9/9**、rc=0。"
    "★★★三增量：①**唯一解是快子**（m5^2/m_e^2=−1.0414e42，|m5^2|/(1/R)^2=1−9.6e−43，非微调而是精确反向）；"
    "②**真空能 9.74e116 ρ_Λ**（来料只给「为负」，补量级后与 r258 的 10^120.74 同构异源）；"
    "③**10000 组随机测试零判别力**（负对照 10000/10000 全违反）。"
    "★★CTL2 证明**任意单尺度玩具**同样给出 α∝α_g ⇒ 排除是**单尺度普遍不可能性**，非 KK 特性；"
    "CTL3 两尺度可逃逸 = §八 自述方向 = RS/ADD 标准方案。★三项「可保留成果」独立信息量 **0 bit**。"
    "★定价严格 0 / 宽松 1 ⇒ **不占度数链**（候选 37 度）。"
    "取号：三树实测 r287 已占、r289 空；**下轮从 r289 复查起**。"
)

DETAIL_BLOCK = """### r289 · 2026-10-31 · ROOT V13.0 五维 KK 电荷—质量排除定理审计（★外部来料审计层）

- **产物**：源码 [`{py}`](源码/{py})；数据 [`…json`](数据/{js}) / [`…md`](数据/{md}) / [`…_report.txt`](数据/{rep})；判定册 [`{jud}`](判定/{jud})；来料原件 [`…_来料原件_ROOT_V13.0_用户附件逐字_2026-10-31.md`](数据/TUFT-r289_KK电荷质量排除定理审计_来料原件_ROOT_V13.0_用户附件逐字_2026-10-31.md)
- **复现**：`python -X utf8 源码\\{py}` ⇒ **rc=0**，条目 **49**（**PASS 41 / FAIL 0 / INFO 6 / BOUNDARY 2**），**控制组 8/8**，**守卫 9/9**。
- **结论一句话**：**来料的算术与代数全部正确（表 10 行、势 3 行、恒等式、QED 系数逐项命中，最大偏差 5.7e-6），但它证明的「排除」不是 KK 的特性，而是「耦合与质量共用同一尺度」的普遍后果——负结果成立，新物理增量 0 bit。**
- **三处增量（来料未做）**：①**唯一解是快子**——模型为 2 无量纲参数对 2 观测（非超定），反解 m5^2/m_e^2=−1.0414e42，|m5^2|/(1/R)^2=1−9.6e−43（快子质量平方与 KK 能隙几乎精确相等）⇒ 排除强度应升级为「真空不稳定」；②**真空能量级**——来料只登记 V(x*)<0，本卷补 |V_min|/ρ_Λ=9.74e116（a 取 M_P^4，单场最保守；SM 自由度数 ~100 时约 1e119），上翻至 Minkowski 需常数项 c0/a=1.1094e-6（B06），该常数本身即 Λ 问题；③**随机测试判别力**——10000 组「全过」是 m5^2≥0 的同义反复，负对照翻转符号后 10000/10000 全违反。
- **控制组（8/8，四条负对照）**：CTL2 单尺度玩具必得 α/(4α_g)=k ⇒ **排除是单尺度必然，非 KK 特性**；CTL3 两尺度（23.41 l_P / 2.389e22 l_P）可同时匹配 ⇒ 缺口仅在「同源」假设；CTL7 表值偏 0.34% 必 FAIL ⇒ 5e-6 容差有牙齿；CTL8 a 取 1e-110 M_P^4 时 B05 失守（9.7e6<1e100）⇒ 真空能判据非恒真。
- **定价**：4 槽（放弃同源 / 接受快子 / 上翻常数 / 给 x^-6 一个 5D 来源）2^4=16 ⇒ 严格 SURVIVE **0**（S3/S4 各引一个新自由参数，「无新参数」与「能匹配」互斥）、宽松 SURVIVE **1**、SUICIDE 8、EMPTY 7 ⇒ **不占度数链**（候选 37 度，链仍止 r264:36）。
- **与既有卷**：B05 与 **r258**（10^120.74）同构异源；B07 与 **r287** dof=0、**r284** ε*=6.261e-12 微调同构；A13/E01 与 **r264** 定义恒等式同构；C04 引 **r243** WEP η=1.2119（超 MICROSCOPE 1.2e14 倍）作 §四 moduli problem 的实验后果（名录指针，不重复计数）。
- **取号**：2026-10-31 23:3x 三树实测 **r287 已占**（V10 §七 可行性否证）、**r289 三树全空**（src/json/md/report 均 0、README 锚 0、判定锚 0）⇒ 取 **r289**。**下轮从 r289 复查起（并行链活跃，取号前必扫）**。
- **治理**：未改 `verify.py`；未跑 `refresh_catalog.py`；未改任何既有卷字节；git 由收口提交统一处理；**本卷 49 条不可与 r142–r287 相加**。
"""


def main():
    with open(README, "r", encoding="utf-8") as f:
        text = f.read()

    os.makedirs(SCRATCH, exist_ok=True)
    if not os.path.exists(BACKUP):
        with open(BACKUP, "w", encoding="utf-8") as f:
            f.write(text)
        print("[reg] backup created:", BACKUP)
    else:
        print("[reg] backup exists, not overwriting")

    lines = text.split("\n")
    report = []

    def find_line(pred, start=0):
        for i in range(start, len(lines)):
            if pred(lines[i]):
                return i
        return -1

    # 1) 源码树：含本卷 RID 的锚点（r287 行尾）
    if any(ln.startswith("│   ├── ") and PY_NAME in ln for ln in lines):
        report.append("src: already present, skip")
    else:
        i = find_line(lambda s: s.startswith("│   ├── TUFT-r287_"))
        if i < 0:
            report.append("src: ANCHOR NOT FOUND")
        else:
            lines.insert(i + 1, SRC_LINE)
            report.append("src: inserted after line %d" % (i + 1))

    # 2) 判定树：r287 判定行后
    if any(JUD_NAME in ln for ln in lines):
        report.append("jud: already present, skip")
    else:
        i = find_line(lambda s: s.startswith("├── 判定_TUFT-r287_"))
        if i < 0:
            report.append("jud: ANCHOR NOT FOUND")
        else:
            lines.insert(i + 1, JUD_LINE)
            report.append("jud: inserted after line %d" % (i + 1))

    # 3) 数据树：块内最后一个 `    ├── TUFT-r` 行后
    if any(ln.startswith("    ├── TUFT-r289") for ln in lines):
        report.append("data: already present, skip")
    else:
        i = find_line(lambda s: s.strip() == "└── 数据/")
        if i < 0:
            report.append("data: BLOCK NOT FOUND")
        else:
            last = -1
            for j in range(i + 1, len(lines)):
                if lines[j].startswith("    ├── TUFT-r"):
                    last = j
                if lines[j].startswith("## ") or lines[j].startswith("| ---"):
                    break
            if last < 0:
                lines.insert(i + 2, DATA_LINE)
                report.append("data: inserted at block head")
            else:
                lines.insert(last + 1, DATA_LINE)
                report.append("data: inserted after line %d" % (last + 1))

    # 4) compact 列表：r287 条后
    if any(ln.startswith("- **r289（2026-10-31）· ") for ln in lines):
        report.append("compact: already present, skip")
    else:
        i = find_line(lambda s: s.startswith("- **r287（2026-10-31）· "))
        if i < 0:
            report.append("compact: ANCHOR NOT FOUND")
        else:
            lines.insert(i + 1, COMPACT_LINE)
            report.append("compact: inserted after line %d" % (i + 1))

    # 5) 增量详节：文件尾追加
    if any(ln.startswith("### r289 · 2026-10-31 · ") for ln in lines):
        report.append("detail: already present, skip")
    else:
        body = DETAIL_BLOCK.format(py=PY_NAME, js=JSON_NAME, md=MD_NAME,
                                   rep=JSON_NAME.replace(".json", "_report.txt"),
                                   jud=JUD_NAME)
        lines.append("")
        lines.append(body)
        report.append("detail: appended at tail")

    new_text = "\n".join(lines)
    with open(README, "w", encoding="utf-8") as f:
        f.write(new_text)

    # ---- 读回验证（从磁盘）
    with open(README, "r", encoding="utf-8") as f:
        disk = f.read()
    dlines = disk.split("\n")
    checks = {
        "src": sum(1 for s in dlines if s.startswith("│   ├── ") and PY_NAME in s),
        "jud": sum(1 for s in dlines if s.startswith("├── 判定_TUFT-r289")),
        "data": sum(1 for s in dlines if s.startswith("    ├── TUFT-r289")),
        "compact": sum(1 for s in dlines if s.startswith("- **r289（2026-10-31）· ")),
        "detail": sum(1 for s in dlines if s.startswith("### r289 · 2026-10-31 · ")),
    }
    print("[reg] actions:")
    for r in report:
        print("   ", r)
    print("[reg] readback counts:", checks)

    # ---- diff 零删除
    with open(BACKUP, "r", encoding="utf-8") as f:
        old = f.read().split("\n")
    import difflib
    removed = [l for l in difflib.unified_diff(old, dlines, lineterm="", n=0)
               if l.startswith("-") and not l.startswith("---")]
    print("[reg] removed-lines =", len(removed))
    for l in removed[:5]:
        print("   DEL:", l[:100])

    ok = all(v == 1 for v in checks.values()) and len(removed) == 0
    print("[reg] RESULT:", "OK" if ok else "CHECK")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
