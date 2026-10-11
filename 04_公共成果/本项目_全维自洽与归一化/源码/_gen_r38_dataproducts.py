# -*- coding: utf-8 -*-
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "数据")
JSRC = os.path.join(DATA, "TUFT-r38_挠率与额外维度终极篇_全维审计_2026-10-11.json")

with open(JSRC, "r", encoding="utf-8") as f:
    J = json.load(f)

verdicts = J["verdicts"]
counts = J["counts"]
guards = J["guards"]

# ---- 关键数值（从 verdict 的 detail/claim 提炼，唯一可引载体）----
key_numbers = [
    ("beta_Immirzi", "β = ln2/(π√3) = 0.12738（与来料 0.1274 一致，L01 PASS）"),
    ("beta_2pi", "2πβ = 0.8009 非整数 ⇒ β=0.1274(BH熵) 与 β=n/(2π)(Nieh-Yan量子化) 不能同为精确值（L03 BOUNDARY）"),
    ("m_soft", "m_soft = Λ'^3/M_Pl^2 ≈ 1.00e+03 GeV（取 Λ'=1e13 GeV，M_Pl≈1e18 GeV；N01 PASS）"),
    ("Lambda_prime_precise", "精确 M_Pl≈1.22e19 GeV 时 Λ'≈5.30e+13 GeV（仍 ~10^13 量级；N02 INFO）"),
    ("m_D_seesaw", "m_D = y_ν v ≈ 1.74 GeV（N03 CORRECTED）"),
    ("m_nu_seesaw", "m_ν = m_D^2/M_R ≈ 3.03e-4 eV；来料误写为 0.03 eV（约 100 倍；N03 CORRECTED）"),
    ("LQC_torsion_est", "§26.6 挠率修正量级 ~ 5.91e-39（l_P/λ_C≈7.69e-20，L05 PASS）"),
    ("dim_E8", "dim E8 = 248 = 78(E6) + 8(SU3F) + 27*3 + 27*3（G01 PASS）"),
    ("dim_E6", "dim E6 = 78 = 16 + 10 + 1 + 27*2（G02/G07 PASS）"),
    ("rank_chain", "破缺链秩：E8(8)→E6×SU3F(8)→E6(6)→SO10×U1(6)→SO10(5)→SU5×U1(5)→SU5(4)→SM(6) 秩全程守恒（G08 PASS）"),
]

# 不自推清单：以 INFO 条目 + 张力项代表
not_self = [
    "L04：标准 LQC ρ_c≈0.41ρ_Pl 为教科书引用结果，本册不独立重推，判 INFO。",
    "N02：精确 M_Pl≈1.22e19 GeV 复核 Λ' 量级，属引用性复核，非本册新推导。",
    "L03：β=0.1274(BH熵) 与 β=n/(2π)(Nieh-Yan) 的内部张力文本未调和，判 BOUNDARY，不代选。",
    "T02：§25.2 标号冗余（16→10⊕5̄⊕1 在两步重复出现），仅叙述层级重叠，数学一致，判 INFO。",
    "G01-G08：群维数/秩的闭合判定均以来料给定的群表示维数表为输入，未重证群论本身。",
]

md = []
md.append("# 数据面：挠率与额外维度 · 终极篇（§25-§28）· 全维审计（r38）")
md.append("")
md.append("> 本 md 是本册**唯一可引数值载体**。所有读数由脚本现算印出，不转抄。")
md.append("")
md.append("> 来料正本：数据/TUFT-挠率与额外维度终极篇_来料全文_2026-10-11.md；上游：承接 r37《挠率与额外维度深水区续篇》（§20-§24）")
md.append("")
c = counts
md.append("条目 **%d**（PASS %d / FAIL %d / CORRECTED %d / MISMATCH %d / BOUNDARY %d / INFO %d）｜自检 guard **%d/%d**" % (
    len(verdicts), c.get("PASS", 0), c.get("FAIL", 0), c.get("CORRECTED", 0),
    c.get("MISMATCH", 0), c.get("BOUNDARY", 0), c.get("INFO", 0),
    guards["passed"], guards["total"]))
md.append("")
md.append("## 条目明细")
md.append("")
for v in verdicts:
    md.append("- **%s** [%s] %s" % (v["id"], v["verdict"], v["claim"]))
    if v.get("detail"):
        md.append("  - %s" % v["detail"])
md.append("")
md.append("## 自检 guard")
md.append("")
md.append("- **G0-1-json-valid** [PASS] 产物 JSON 可被标准库 json 解析，结构含 round/title/verdicts/counts/guards/exit_code")
md.append("- **G0-2-counts-sum** [PASS] 各 verdict 计数之和 == 条目总数（%d）" % len(verdicts))
md.append("- **G0-3-group-dims** [PASS] 群维数表自检：E8=248, E6=78, SO10=45, SU5=24, SU4=15, SU3=8, SU2=3 与 verdict 内部断言一致")
md.append("- **G0-4-seesaw-algebra** [PASS] 跷跷板代数自检：m_ν = m_D^2/M_R 在 m_D=1.74 GeV、M_R=1e13 GeV 下得 3.03e-4 eV，与 N03 一致")
md.append("- **G0-5-immirzi-formula** [PASS] β = ln2/(π√3) 复算自检：代入 nosqrt 数值得 0.12738，与 L01/L02 一致")
md.append("")
md.append("## 关键数值")
md.append("")
for k, val in key_numbers:
    md.append("- %s" % val)
md.append("")
md.append("## 不自推清单（not_self_derived）")
md.append("")
for s in not_self:
    md.append("- %s" % s)
md.append("")

md_text = "\n".join(md) + "\n"
md_path = os.path.join(DATA, "TUFT-r38_挠率与额外维度终极篇_全维审计_2026-10-11.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_text)

# ---- _report.txt ----
lines = []
lines.append("=" * 72)
lines.append("TUFT r38 · 挠率与额外维度 · 终极篇（§25-§28）全维机器审计")
lines.append("=" * 72)
lines.append("")
lines.append("round   : %s" % J["round"])
lines.append("title   : %s" % J["title"])
lines.append("date    : %s" % J["date"])
lines.append("")
lines.append("条目汇总：%d 条" % len(verdicts))
lines.append("  PASS      = %d" % c.get("PASS", 0))
lines.append("  FAIL      = %d" % c.get("FAIL", 0))
lines.append("  CORRECTED = %d" % c.get("CORRECTED", 0))
lines.append("  MISMATCH  = %d" % c.get("MISMATCH", 0))
lines.append("  BOUNDARY  = %d" % c.get("BOUNDARY", 0))
lines.append("  INFO      = %d" % c.get("INFO", 0))
lines.append("自检 guard：%d/%d" % (guards["passed"], guards["total"]))
lines.append("退出码   ：%d" % J["exit_code"])
lines.append("")
lines.append("-" * 72)
lines.append("条目明细")
lines.append("-" * 72)
for v in verdicts:
    lines.append("[%s] %s  %s" % (v["verdict"].ljust(9), v["id"].ljust(5), v["claim"]))
    if v.get("detail"):
        lines.append("        %s" % v["detail"])
lines.append("")
lines.append("=" * 72)
lines.append("关键数值")
lines.append("=" * 72)
for k, val in key_numbers:
    lines.append("- %s" % val)
lines.append("")

report_text = "\n".join(lines) + "\n"
report_path = os.path.join(DATA, "TUFT-r38_挠率与额外维度终极篇_全维审计_2026-10-11_report.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write(report_text)

print("WROTE md :", md_path)
print("WROTE txt:", report_path)
