# -*- coding: utf-8 -*-
"""
TUFT 跨册缺陷族检查 + 汇编数字一致性校验（可复跑）
==================================================
目的（整理/优化）：
  1) 判定总表：按 tuft_总索引.py 同一口径解析全部 *_report.txt 的 PASS/FAIL/BOUNDARY/INFO；
  2) 缺陷族矩阵：用可解释的正则族模式统计"同一病根"在哪些分册复发（文本命中数，启发式）；
  3) 一致性校验：把 tuft_全景总报告.md / tuft_全书_交付版.md 中写死的累计数字
     与自动扫描结果对比，检出"手工数字漂移"。
红线：数学自洽 != 物理实验证实。缺陷族命中数为**文本启发式计数**，不等于判定条数。
"""
from __future__ import print_function

import os
import re
import sys
import glob
import json

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_MD = os.path.join(HERE, "tuft_跨册缺陷族.md")
OUT_JSON = os.path.join(HERE, "tuft_跨册缺陷族.json")

# 缺陷族定义：族名 -> (正则, 判读说明)
FAMILIES = [
    ("量纲非法", r"量纲(非法|不符|错误|错|=[^,，。]*)", "公式量纲不合法或与目标量不符"),
    ("αKTΩ/c² 缺陷族", r"(α\s*K\s*T[\^A-Za-z0-9]*\s*Ω|alpha K T Omega|αKTΩ|m_q\s*=|m\s*=\s*α)", "以 αKTΩ/c² 充当质量/能量密度"),
    ("无构造/仅命名", r"(未给|无|缺).{0,6}(构造|映射|方程)|只有命名|命名而非|重新命名|重命名为|属命名", "只有命名/类比，没有构造或方程"),
    ("外部注入", r"(外部注入|外部输入|注入)", "关键结构（如 SU(3)、v、V0）由外部给定"),
    ("挠率无动力学", r"(挠率动能|T\^2 项|T² 项|不含挠率|无挠率势|代数约束)", "作用量缺挠率动能项 ⇒ 真空挠率为零"),
    ("代码与文字不符", r"(与(代码|实跑|数值解|仿真).{0,8}不符|代码与文字|实跑.{0,10}不符|从未调用|SyntaxError|domain error)", "代码实跑与文字声明不一致"),
    ("能标错配", r"(能标错配|相差.{0,8}个数量级|差 12 个数量级|数量级差)", "跨阶段能标量级不相容"),
    ("IR 当 UV / 尺度混淆", r"(尺度混淆|把 IR|IR 实测|UV 几何|循环(论证)?)", "把红外测量值当作紫外几何定值"),
    ("自由度审计", r"(自由参数|参数内生|自由度审计|完全相消|可调尺度)", "可调自由度与观测量不匹配"),
    ("可证伪性缺失", r"(不可证伪|无可证伪|无(公式)?定量|无可计算|无任何定量)", "缺少可判决的定量预言"),
    ("拓扑/整性误用", r"(半整数|环绕数|缠绕数|Lk\s*=|Hopf)", "整数不变量被当作半整数或反之"),
    ("饱和/截断类", r"(K_sat|曲率饱和|无下界|普朗克截断)", "以饱和/截断替代真正的机制构造"),
]

# 分册标识：report 文件名 -> 册名
BOOKS = [
    ("tuft_续篇_全维求导精算_report.txt", "续篇（自旋/泡利/手性）"),
    ("tuft_相位pi_全维求导精算_report.txt", "闭环相位 π"),
    ("tuft_色挠率_SU3_report.txt", "色挠率 SU(3)"),
    ("tuft_三路线_ABC_report.txt", "三路线 A/B/C（分析）"),
    ("tuft_四力统一_report.txt", "四力统一主丛框架"),
    ("tuft_黑洞热力学_report.txt", "黑洞热力学 / 信息悖论"),
    ("tuft_暴胀CMB_report.txt", "宇宙暴胀 / CMB"),
    ("tuft_r5_report.txt", "挠率探测（R5）"),
    ("tuft_r6_report.txt", "挠率产生机制（R6）"),
    ("tuft_O_SCALE_锚定方案_report.txt", "O-SCALE 锚定方案"),
    ("tuft_引力波_挠率扰动_report.txt", "B：挠率引力波"),
    ("tuft_B_自屏蔽_数值求解_report.txt", "B：自屏蔽数值解"),
    ("tuft_B_根因溯源_report.txt", "B：根因溯源"),
    ("tuft_B_UV完成_report.txt", "B：UV 完成"),
    ("tuft_收口_修复优化_report.txt", "收口方案"),
    ("tuft_续篇_双结交换仿真_report.txt", "双结交换仿真（附）"),
]


def parse_counts(text):
    """与 tuft_总索引.py 同口径：优先汇总行，回退行内标记。"""
    counts = {}
    for m in re.finditer(r"(PASS|FAIL|BOUNDARY|INFO)\s*[=:]\s*(\d+)", text):
        counts[m.group(1)] = int(m.group(2))
    if counts:
        return counts
    c = {}
    for k in ("PASS", "FAIL", "BOUNDARY", "INFO"):
        c[k] = len(re.findall(r"\[\s*%s[^\]]*\]" % k, text))
    return c


def read_text(path):
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def side_docs(report_name):
    """把该册的 report.txt + 对应精算报告/修订版 md 合并作为族统计语料。"""
    stem = report_name.replace("_report.txt", "")
    parts = [read_text(os.path.join(HERE, report_name))]
    for cand in glob.glob(os.path.join(HERE, stem + "*.md")) + \
            glob.glob(os.path.join(HERE, stem.replace("_全维求导精算", "") + "*报告.md")):
        parts.append(read_text(cand))
    return "\n".join(parts)


def main():
    rows, total = [], {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    missing = []
    for report, label in BOOKS:
        path = os.path.join(HERE, report)
        if not os.path.isfile(path):
            missing.append(report)
            continue
        text = read_text(path)
        c = parse_counts(text)
        rows.append((report, label, c))
        for k in total:
            total[k] += c.get(k, 0)

    # 缺陷族矩阵（文本启发式）
    fam_index = {name: {"total": 0, "books": {}} for name, _, _ in FAMILIES}
    for report, label, c in rows:
        corpus = side_docs(report)
        for name, pattern, _ in FAMILIES:
            n = len(re.findall(pattern, corpus))
            if n:
                fam_index[name]["total"] += n
                fam_index[name]["books"][label] = n

    md = []
    md.append("# TUFT 跨册缺陷族与汇编一致性（自动生成）\n")
    md.append("> 由 `tuft_跨册缺陷族检查.py` 生成（可复跑）。红线：数学自洽 != 物理实验证实。")
    md.append("> 缺陷族命中数是**文本启发式计数**（在同一病根的多册语料中检索族模式），不等于判定条数。\n")

    md.append("## 一、判定总表（与 `tuft_总索引.py` 同口径）\n")
    md.append("| 分册 | 报告 | PASS | FAIL | BOUNDARY | INFO |")
    md.append("|---|---|---|---|---|---|")
    for report, label, c in rows:
        md.append("| %s | `%s` | %d | %d | %d | %d |" % (
            label, report, c.get("PASS", 0), c.get("FAIL", 0),
            c.get("BOUNDARY", 0), c.get("INFO", 0)))
    md.append("| **合计（%d 册）** | — | **%d** | **%d** | **%d** | **%d** |" % (
        len(rows), total["PASS"], total["FAIL"], total["BOUNDARY"], total["INFO"]))
    md.append("")
    if missing:
        md.append("> 未找到的报告（跳过）：" + "、".join(missing) + "\n")

    md.append("## 二、缺陷族矩阵（族 × 分册 命中数）\n")
    labels = [label for _, label, _ in rows]
    md.append("| 缺陷族 | 命中合计 | 复现册数 | 分布 |")
    md.append("|---|---|---|---|")
    for name, _, meaning in sorted(FAMILIES, key=lambda x: -fam_index[x[0]]["total"]):
        books = fam_index[name]["books"]
        dist = "；".join("%s(%d)" % (b, n) for b, n in sorted(books.items(), key=lambda x: -x[1]))
        md.append("| **%s** | %d | %d | %s |" % (name, fam_index[name]["total"], len(books), dist or "—"))
    md.append("")
    md.append("| 缺陷族 | 判读 |")
    md.append("|---|---|")
    for name, _, meaning in FAMILIES:
        md.append("| %s | %s |" % (name, meaning))
    md.append("")

    # 一致性校验：以 tuft_总索引.md 的自动扫描合计为基准，比对其他汇编中写死的数字
    subset = "PASS %d · FAIL %d · BOUNDARY %d · INFO %d" % (
        total["PASS"], total["FAIL"], total["BOUNDARY"], total["INFO"])
    md.append("## 三、汇编数字一致性校验\n")
    md.append("本检查覆盖的 **%d 册子集**（上表）合计：%s。\n" % (len(rows), subset))
    md.append("基准 = `tuft_总索引.md` 的自动扫描合计（覆盖全部 `*_report.txt`）。\n")
    ref_text = read_text(os.path.join(HERE, "tuft_总索引.md"))
    ref = re.search(r"\|\s*\*\*合计\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*", ref_text)
    ref_tuple = tuple(int(x) for x in ref.groups()) if ref else None
    md.append("基准合计：**%s**\n" % ("/".join(str(x) for x in ref_tuple) if ref_tuple else "（未找到）"))
    md.append("| 文件 | 其中写明的累计数字 | 与基准 |")
    md.append("|---|---|---|")
    drift = 0
    for fname in ["tuft_全景总报告.md", "tuft_全书_交付版.md"]:
        text = read_text(os.path.join(HERE, fname))
        found = re.findall(r"PASS\s*(\d+)\s*[·\u00b7]?\s*FAIL\s*(\d+)\s*[·\u00b7]?\s*BOUNDARY\s*(\d+)\s*[·\u00b7]?\s*INFO\s*(\d+)", text)
        if not found:
            md.append("| `%s` | （未找到累计数字） | — |" % fname)
            continue
        ok = ref_tuple is not None and all(tuple(int(x) for x in f) == ref_tuple for f in found)
        if not ok:
            drift += 1
        md.append("| `%s` | %s | %s |" % (
            fname, " / ".join("P/F/B/I = " + "/".join(f) for f in found),
            "✅ 一致" if ok else "⚠️ 漂移"))
    md.append("")
    md.append("**结论**：%s" % (
        "两处汇编的累计数字与自动扫描基准一致 ✅" if drift == 0
        else "有 %d 处手工数字与自动扫描基准不一致 ⚠️（优化动作：用 `tuft_全书构建.py` 重新生成，勿手改数字）" % drift))

    open(OUT_MD, "w", encoding="utf-8").write("\n".join(md) + "\n")
    json.dump({"books": [{"report": r, "label": l, "counts": c} for r, l, c in rows],
               "total": total,
               "families": fam_index,
               "drift_files": drift},
              open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("已生成: " + OUT_MD)
    print("  覆盖 %d 册；子集合计 %s" % (len(rows), subset))
    print("  基准（总索引合计）: %s" % ("/".join(str(x) for x in ref_tuple) if ref_tuple else "N/A"))
    print("  缺陷族 Top5：")
    for name, _, _ in sorted(FAMILIES, key=lambda x: -fam_index[x[0]]["total"])[:5]:
        print("    %-16s 命中 %3d；复现 %d 册" % (
            name, fam_index[name]["total"], len(fam_index[name]["books"])))
    print("  汇编数字漂移文件数: %d" % drift)


if __name__ == "__main__":
    main()
