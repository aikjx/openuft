# -*- coding: utf-8 -*-
"""54 · 全物理现象覆盖矩阵（2026-10-19）—— 域级槽位补全 + 机器统计引擎

职责（补充完成，不重判）：
  1. 机读继承：从 07_现象覆盖矩阵.md 提取现象行与统计自称值，抗漂移核对。
  2. 域级补全：把 31–52 卷（全物理系列）、62–65 号（螺旋几何化子卷）、
     r95–r111（攻破链）登记为覆盖槽位；每行的"产物规模"由文件存在性与
     JSON 键数机读，"覆盖性质/状态"为人工登记（随引擎落盘，声明为外部输入）。
  3. 机读统计：总行数、状态分布、域分布；生成 54 卷 md + csv + json + out.txt。

红线：新增行是"域级槽位登记"，不把任何未解决项改判为已确立；
本卷不产生新物理、不修改被引文件字节。
"""

import glob
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(DIR)
BASE_MD = os.path.join(DIR, "07_现象覆盖矩阵.md")
R_DATA = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")
SPIRAL = os.path.join(DIR, "空间螺旋几何化统一场论")

VOL_MD = os.path.join(DIR, "54_全物理现象覆盖矩阵_2026-10-19.md")
OUT_CSV = os.path.join(DIR, "现象覆盖矩阵_全物理_2026-10-19.csv")
OUT_JSON = os.path.join(DIR, "54_fullphysics_coverage_results.json")
OUT_TXT = os.path.join(DIR, "54_fullphysics_coverage_out.txt")

GUARDS = []
ENTRIES = []


def guard(cond, name, desc=""):
    GUARDS.append((name, bool(cond), desc))
    return bool(cond)


def add(code, verdict, title, detail, **extra):
    e = {"code": code, "verdict": verdict, "title": title, "detail": detail}
    e.update(extra)
    ENTRIES.append(e)


print("[54] boot ok", flush=True)

# ---------------------------------------------------------------- 1. 继承矩阵机读
if not os.path.isfile(BASE_MD):
    sys.stderr.write("BASE_MD NOT FOUND\n")
    sys.exit(3)

base_txt = open(BASE_MD, encoding="utf-8").read()
# 现象行：取"## 覆盖矩阵"与"## 统计"之间的表格行，剔除表头行
i0 = base_txt.find("## 覆盖矩阵")
i1 = base_txt.find("## 统计")
slice_txt = base_txt[i0:i1] if (i0 >= 0 and i1 > i0) else base_txt
table_lines = [ln for ln in slice_txt.splitlines() if ln.strip().startswith("|")]
data_lines = [ln for ln in table_lines if not ln.strip().startswith("| 现象")
              and not re.match(r"^\|\s*-{2,}", ln.strip())]
n_rows = len(data_lines)
m_stat_est = re.search(r"已确立（含已验证项）\s*\|\s*(\d+)", base_txt)
m_stat_par = re.search(r"部分确立\s*/\s*定性\s*\|\s*(\d+)", base_txt)
m_stat_unt = re.search(r"未检验（已推导）\s*\|\s*(\d+)", base_txt)
m_stat_uns = re.search(r"未解决\s*/\s*矛盾\s*/\s*不适用\s*\|\s*(\d+)", base_txt)
stat = (int(m_stat_est.group(1)) if m_stat_est else None,
        int(m_stat_par.group(1)) if m_stat_par else None,
        int(m_stat_unt.group(1)) if m_stat_unt else None,
        int(m_stat_uns.group(1)) if m_stat_uns else None)
sum_stat = sum(x for x in stat if x is not None)
guard(n_rows == 39 and stat == (24, 3, 2, 10) and sum_stat == 39,
      "g_base_matrix_39",
      "07 矩阵须为 39 行且统计 24/3/2/10；实测 行数=%d 统计=%s 合计=%d" % (n_rows, stat, sum_stat))
add("B01", "PASS" if (n_rows == 39 and stat == (24, 3, 2, 10)) else "FAIL",
    "继承矩阵机读：39 现象行 + 统计 24/3/2/10",
    "机读现象行 %d 条；统计自称 已确立 %s / 部分 %s / 未检验 %s / 未解决 %s ⇒ 合计 %d，与行数一致"
    % (n_rows, stat[0], stat[1], stat[2], stat[3], sum_stat),
    n_rows=n_rows, stat=stat)

# ---------------------------------------------------------------- 2. 域级补全（31–52 卷）
# status 语义（人工登记，外部输入账）：ESTABLISHED_STD=标准物理已确立但非 UFE-1 导出；
# OPEN_UFE1=UFE-1 明确未解决；AUDIT=卷级审计/攻破产物；ANCHOR=文献锚点+本库复算登记。
DOMAINS = [
    ("31", "第一性原理推导（量纲→判决）", "31_firstprinciples_calc.py", "AUDIT", "量纲审计方法论卷：把'推导'定义为可复算的判决链"),
    ("32", "宇宙本源核心方程体系", "32_essence_calc.py", "ANCHOR", "核心方程体系的锚点计算卷"),
    ("33", "宇宙本质本源定理", "33_essence_units_calc.py", "ANCHOR", "本质定理的量纲与锚点卷"),
    ("34", "五大量级问题", "34_orders_calc.py", "ANCHOR", "从 Planck 到宇宙学的量级谱锚点"),
    ("35", "量子基础与测量问题", "35_quantum_calc.py", "OPEN_UFE1", "UFE-1 未量子化 ⇒ 测量问题不在主方程覆盖内"),
    ("36", "暗物质候选全景", "36_darkmatter_calc.py", "OPEN_UFE1", "v1 场内容无暗物质候选（L8）；本卷只做候选普查"),
    ("37", "粒子质量谱全序", "37_massspectrum_calc.py", "OPEN_UFE1", "Yukawa/味参数为输入 ⇒ 质量谱非第一性导出"),
    ("38", "宇宙起源三谜", "38_cosmos_calc.py", "OPEN_UFE1", "暴胀/重子生成/暗能量起源均未解决"),
    ("39", "统一场论攻坚总终卷", "39_final_calc.py", "AUDIT", "攻坚路线总收卷"),
    ("40", "宇宙学张力全景", "40_tensions_calc.py", "OPEN_UFE1", "H₀ 5σ、S₈ 张力未解决（参数输入）"),
    ("41", "黑洞观测与量子判决", "41_blackhole_calc.py", "ESTABLISHED_STD", "r_s/霍金蒸发/QNM 锚点；GR 侧已确立"),
    ("42", "中子星与致密天体", "42_ns_calc.py", "ESTABLISHED_STD", "EOS/TOV 锚点；状态方程本身为输入"),
    ("43", "引力波频谱", "43_gwspectrum_calc.py", "ESTABLISHED_STD", "C4 GW150914 辐射能已复算；P1 仅两张量极化"),
    ("44", "中微子振荡", "44_nu_calc.py", "ESTABLISHED_STD", "ν_R 纳入后 Dirac 质量相容；质量谱/PMNS 为输入"),
    ("45", "拓扑与守恒", "45_topo_calc.py", "ANCHOR", "Hopf/缠绕数与守恒律锚点"),
    ("46", "CMB 物理", "46_cmb_calc.py", "ESTABLISHED_STD", "声学峰/功率谱锚点；Λ 数值未解"),
    ("47", "黑洞热力学", "47_bhth_calc.py", "ESTABLISHED_STD", "贝肯斯坦-霍金熵/温度锚点"),
    ("48", "V50 公理审计", "48_v50audit_calc.py", "AUDIT", "GAQ-UFT V50 公理层审计"),
    ("49", "V50 修复草案", "49_v50fix_calc.py", "AUDIT", "V50 修复草案卷（49A EC 拉氏量审计同族）"),
    ("50", "恒星能量与太阳", "50_sun_calc.py", "ESTABLISHED_STD", "pp 链/CNO 锚点；太阳中微子问题已由标准物理解"),
    ("51", "大爆炸核合成", "51_bbn_calc.py", "ESTABLISHED_STD", "D/H、He-4 丰度锚点"),
    ("52", "电弱统一与实验对照", "52_ew_calc.py", "ESTABLISHED_STD", "m_W/ρ/α_s 跑动已复算（V1/V2/V6）"),
]

domain_rows = []
n_missing = 0
for num, name, engine, status, note in DOMAINS:
    p_engine = os.path.join(DIR, engine)
    p_json = p_engine.replace("_calc.py", "_calc_results.json")
    p_html = None
    for h in glob.glob(os.path.join(DIR, num + "_*.html")):
        p_html = h
        break
    exists = os.path.isfile(p_engine)
    if not exists:
        n_missing += 1
    n_keys = None
    if os.path.isfile(p_json):
        try:
            d = json.load(open(p_json, encoding="utf-8"))
            n_keys = len(d) if isinstance(d, dict) else len(d)
        except Exception:
            n_keys = None
    domain_rows.append({"vol": num, "domain": name, "engine_exists": exists,
                        "html_exists": bool(p_html), "json_keys": n_keys,
                        "status": status, "note": note})

guard(n_missing == 0, "g_domain_engines_present",
      "31–52 卷引擎须全部在盘；实测缺失 %d 个" % n_missing)
add("B02", "PASS" if n_missing == 0 else "FAIL",
    "域级补全：31–52 全物理系列 22 卷引擎在盘性",
    "在盘 %d/22；HTML 卷在盘 %d/22；JSON 可读者 %d/22"
    % (sum(1 for r in domain_rows if r["engine_exists"]),
       sum(1 for r in domain_rows if r["html_exists"]),
       sum(1 for r in domain_rows if r["json_keys"] is not None)),
    rows=domain_rows)

# ---------------------------------------------------------------- 3. 螺旋线 + 攻破链登记
spiral_files = sorted(glob.glob(os.path.join(SPIRAL, "6[2-5]_*.md")))
spiral_rows = []
for p in spiral_files:
    t = open(p, encoding="utf-8").read()
    m = re.search(r"PASS\s*=?\s*(\d+)\s*/\s*FAIL\s*=?\s*(\d+)", t)
    verdict_guess = None
    if m:
        verdict_guess = "FAIL %s / PASS %s" % (m.group(2), m.group(1))
    spiral_rows.append({"file": os.path.basename(p), "tally": verdict_guess})
add("B03", "PASS" if spiral_rows else "FAIL",
    "螺旋几何化子卷（62–65 号）登记",
    "在盘 %d 卷：%s ⇒ 覆盖性质为 AUDIT（攻破链），不占'已确立'名额"
    % (len(spiral_rows), "；".join(r["file"].split("_")[0] for r in spiral_rows)),
    rows=spiral_rows)

r_files = sorted(glob.glob(os.path.join(R_DATA, "TUFT-r1*.json")))
add("B04", "PASS" if len(r_files) >= 13 else "FAIL",
    "攻破链（r100–r111）登记",
    "机读 %d 份数据文件 ⇒ 覆盖性质为 AUDIT；详见 53 卷合账（本卷只登记槽位，不重复计数）" % len(r_files),
    n_files=len(r_files))

# ---------------------------------------------------------------- 4. 统计
status_cnt = {}
for r in domain_rows:
    status_cnt[r["status"]] = status_cnt.get(r["status"], 0) + 1
total_rows = n_rows + len(domain_rows)
tally = {}
for e in ENTRIES:
    tally[e["verdict"]] = tally.get(e["verdict"], 0) + 1
verdict_total = "FAIL" if tally.get("FAIL", 0) else ("BOUNDARY" if tally.get("BOUNDARY", 0) else "PASS")
guard_failed = [g for g in GUARDS if not g[1]]

SUMMARY = {
    "tag": "54_fullphysics_coverage",
    "date": "2026-10-19",
    "role": "全物理现象覆盖矩阵（域级槽位补全 + 统计，不重判）",
    "verdict_total": verdict_total,
    "tally": tally,
    "inherited_rows": n_rows,
    "inherited_stat": stat,
    "domain_rows": len(domain_rows),
    "domain_status_cnt": status_cnt,
    "total_rows": total_rows,
    "spiral_volumes": len(spiral_rows),
    "r_chain_files": len(r_files),
    "guards_total": len(GUARDS),
    "guards_failed": len(guard_failed),
}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({"summary": SUMMARY, "entries": ENTRIES,
               "guards": [{"name": g[0], "ok": g[1], "desc": g[2]} for g in GUARDS]},
              f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------- 5. 生成 54 卷
STATUS_LABEL = {
    "ESTABLISHED_STD": "域级登记（标准物理已确立，非 UFE-1 导出）",
    "OPEN_UFE1": "域级登记（UFE-1 明确未解决）",
    "AUDIT": "域级登记（卷级审计/攻破产物）",
    "ANCHOR": "域级登记（文献锚点 + 本库复算）",
}

vol = []
vol.append("# 54 · 全物理现象覆盖矩阵（2026-10-19）\n")
vol.append("> **openuft · 07_统一场方程 · 编号 54**｜在 07 矩阵（39 行）基础上补全至全物理域级槽位")
vol.append("> 引擎：`54_fullphysics_coverage_calc.py` → `54_fullphysics_coverage_results.json` + `_out.txt` + `现象覆盖矩阵_全物理_2026-10-19.csv`（守卫 %d/%d）"
           % (len(GUARDS) - len(guard_failed), len(GUARDS)))
vol.append("> 上游：[07_现象覆盖矩阵](07_现象覆盖矩阵.md)（39 行继承，只读）· [53 核心公式体系总册](53_核心公式体系总册_2026-10-19.md)（合账）· [31–52 全物理系列](.)\n")
vol.append("---\n")
vol.append("## 0. 本卷补什么\n")
vol.append("07 矩阵回答『已知现象有多少能从主方程推出来』（39 行）。本卷把覆盖面**补全到全物理域级**：")
vol.append("31–52 卷覆盖的 22 个物理学域 + 62–65 螺旋线 + r100–r111 攻破链，全部登记为覆盖槽位。")
vol.append("**新增行不改变任何未解决项的状态**——它们登记的是『该域在本库有卷级产物/锚点复算』，不是『该域已被统一场论解决』。\n")
vol.append("## 1. 继承矩阵（机读核对）\n")
vol.append("| 口径 | 机读值 | 自称值 | 守卫 |")
vol.append("|---|---|---|---|")
vol.append("| 现象行数 | %d | 39 | %s |" % (n_rows, "PASS" if n_rows == 39 else "FAIL"))
vol.append("| 统计 已确立/部分/未检验/未解决 | %s | 24/3/2/10 | %s |"
           % ("/".join(str(x) for x in stat), "PASS" if stat == (24, 3, 2, 10) else "FAIL"))
vol.append("\n## 2. 全物理域级覆盖表（22 域，机读产物规模）\n")
vol.append("| 卷 | 域 | 引擎在盘 | HTML 卷 | JSON 键数 | 覆盖性质 | 备注 |")
vol.append("|---|---|---|---|---|---|---|")
for r in domain_rows:
    vol.append("| %s | %s | %s | %s | %s | %s | %s |"
               % (r["vol"], r["domain"], "是" if r["engine_exists"] else "否",
                  "是" if r["html_exists"] else "否",
                  r["json_keys"] if r["json_keys"] is not None else "—",
                  STATUS_LABEL[r["status"]], r["note"]))
vol.append("\n### 2.1 域级状态分布（机读）\n")
vol.append("| 状态 | 域数 |")
vol.append("|---|---|")
for k in sorted(status_cnt):
    vol.append("| %s | %d |" % (STATUS_LABEL[k], status_cnt[k]))
vol.append("\n## 3. 螺旋线与攻破链槽位\n")
vol.append("| 槽位 | 在盘 | 覆盖性质 |")
vol.append("|---|---|---|")
for r in spiral_rows:
    vol.append("| %s | 是 | AUDIT（攻破链；%s） |" % (r["file"], r["tally"] or "计数见卷内"))
vol.append("| r100–r111 攻破链（%d 份数据） | 是 | AUDIT（合账见 53 卷） |" % len(r_files))
vol.append("\n## 4. 全覆盖总账（机读）\n")
vol.append("| 口径 | 行数 |")
vol.append("|---|---|")
vol.append("| 继承现象行（07 矩阵） | %d |" % n_rows)
vol.append("| 新增全物理域级行（31–52） | %d |" % len(domain_rows))
vol.append("| 螺旋线 + 攻破链槽位 | %d |" % (len(spiral_rows) + 1))
vol.append("| **合计登记行** | **%d** |" % total_rows)
vol.append("\n> 读数纪律：合计 %d 行中，标『已确立』的仍只有继承矩阵的 24 行；新增 22 域级行与攻破链槽位**不占已确立名额**。\n" % total_rows)
vol.append("## 5. 未解决项的全物理清单（随继承转录，防误读）\n")
vol.append("禁闭与质量隙 · 强子质量谱第一性 · 暗物质候选（v1 无） · 暗能量数值（10¹²⁰） · 宇宙加速的动力学来源 · 层级问题（1.3×10¹⁷） · 耦合统一（SM 单圈不统一；SO(10) 条件性且与 P4 互斥） · 物质–反物质不对称（差 ~10⁸） · 引力量子化（M_Pl 失效） · H₀ 张力（5σ） · μ子 g−2（4σ 级争议） · 质子衰变取舍（P4 vs SO(10) 链）。\n")
vol.append("## 6. 红线\n")
vol.append("本卷是覆盖面补全与统计册，不产生新物理、不把任何域改判为已解决、不修改被引文件字节；未跑 git。\n")

with open(VOL_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(vol))

# CSV
with open(OUT_CSV, "w", encoding="utf-8") as f:
    f.write("slot,domain_or_phenomenon,engine_present,html_present,json_keys,status,note\n")
    for r in domain_rows:
        f.write("%s,%s,%s,%s,%s,%s,%s\n"
                % (r["vol"], r["domain"].replace(",", "；"),
                   "Y" if r["engine_exists"] else "N", "Y" if r["html_exists"] else "N",
                   r["json_keys"] if r["json_keys"] is not None else "",
                   r["status"], r["note"].replace(",", "；")))
    for r in spiral_rows:
        f.write("spiral,%s,Y,Y,,AUDIT,%s\n" % (r["file"].replace(",", "；"), (r["tally"] or "").replace(",", " ")))
    f.write("r_chain,r100-r111,Y,Y,%d,AUDIT,合账见53卷\n" % len(r_files))

with open(OUT_TXT, "w", encoding="utf-8") as f:
    f.write("54 fullphysics coverage | verdict=%s | entries=%d | guards=%d/%d\n"
            % (verdict_total, len(ENTRIES), len(GUARDS) - len(guard_failed), len(GUARDS)))
    f.write("inherited rows=%d stat=%s\n" % (n_rows, stat))
    f.write("domain rows=%d status=%s\n" % (len(domain_rows), status_cnt))
    f.write("total slots=%d\n" % total_rows)
    for g in GUARDS:
        f.write("GUARD %-30s %s %s\n" % (g[0], "PASS" if g[1] else "FAIL", g[2]))
    f.flush()

print("[54] VERDICT=%s entries=%d guards=%d/%d total_slots=%d"
      % (verdict_total, len(ENTRIES), len(GUARDS) - len(guard_failed), len(GUARDS), total_rows), flush=True)
if guard_failed:
    for g in guard_failed:
        sys.stderr.write("GUARD FAIL: %s :: %s\n" % (g[0], g[2]))
    sys.exit(2)
sys.exit(0)
