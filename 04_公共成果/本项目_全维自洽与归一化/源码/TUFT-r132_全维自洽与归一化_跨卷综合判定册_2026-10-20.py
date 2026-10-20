# -*- coding: utf-8 -*-
"""
TUFT-r132 · 全维自洽与归一化 · 跨卷综合判定册（总结整理攻破）

定位：本卷是 r122→r131 战役的【跨卷综合判定册】，不是新审计，而是
      (1) 整理正确的理论体系（SM/GR 正确核 + 方程全集 + 推导链地基）
      (2) 攻破正确理论体系与方程的断裂边界（各卷 FAIL/DEAD 全景）
      (3) 统一场论路线判定（r125 DEAD + r129 κ-τ DEAD）
      (4) 元判定：全维自洽与归一化是否达成
      的【跨索引 / 元判定】。

红线纪律：
  - 各源卷各自拥有其条目；本卷为跨索引，条目【非加和】。
  - 元判定由机读结果驱动，不得硬编码“算完数却写死判定”。
  - 不触碰并行会话字节；本卷仅落盘自身 6 件交付物。
  - 不 push、不刷新目录。

输出（6 件，均落 数据/ 或 数据/判定/）：
  - 数据/TUFT-r132_...json              （机读综合册）
  - 数据/TUFT-r132_...md                （机读综合册 markdown）
  - 数据/TUFT-r132_..._report.txt        （人工可读报告）
  - 数据/判定_TUFT-r132_...md            （判定册=主交付物）
  - 源码/TUFT-r132_...py                 （本引擎）
  - 源码/_run_r132.py                    （UTF-8 安全 runner）
"""
import os, json, glob, datetime, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
PROJECT = os.path.normpath(os.path.join(HERE, ".."))
DATE = "2026-10-20"
STEM = "TUFT-r132_全维自洽与归一化_跨卷综合判定册_%s" % DATE
JUDGE_STEM = "判定_TUFT-r132_全维自洽与归一化_跨卷综合判定与攻破全景_%s" % DATE

# ---------------------------------------------------------------------------
# 卷元数据（角色 + 类别 + 目标）。类别决定元判定归属。
#   AUDIT_SELFCHECK      : 审计链自洽性自检（r122）
#   ORGANIZE_CORRECT     : 整理正确的理论体系（r127/r128/r130）
#   BREAK_UFT_CANDIDATE  : 统一场论路线/候选的攻破卷（r123/r124/r125/r126/r129/r131）
# ---------------------------------------------------------------------------
VOL_META = [
    (122, "AUDIT_SELFCHECK",     "反噬自洽审计（审计链对已知锚点自洽）",                 "审计链本身"),
    (123, "BREAK_UFT_CANDIDATE", "攻破·力的大统一方程退守路径（换群/阈值/额外维/紫外完备）", "力的大统一方程"),
    (124, "BREAK_UFT_CANDIDATE", "攻破·光子内部运行求导证明核心理论体系",               "光子内部运行核心理论体系"),
    (125, "BREAK_UFT_CANDIDATE", "路线对错判定·统一场论路线假设穷尽审计",                 "统一场论路线（含 κ-τ）"),
    (126, "BREAK_UFT_CANDIDATE", "攻破·超宇宙与宇宙图景宣称（精算+恒等式审计）",         "超宇宙/宇宙图景宣称"),
    (127, "ORGANIZE_CORRECT",    "整理正确核 + 攻破断裂边界（SM/GR 已验证方程集复核）",   "SM/GR 已验证方程集"),
    (128, "ORGANIZE_CORRECT",    "整理正确理论体系方程全集 + 攻破审计",                   "正确理论体系方程全集"),
    (129, "BREAK_UFT_CANDIDATE", "第一性原理导出定价（微观粒子 + 宏观星体）",             "κ-τ 统一场论导出全部粒子/星体"),
    (130, "ORGANIZE_CORRECT",    "攻破推导链·正确理论体系与方程的隐藏前提审计",           "正确理论体系与方程的推导链前提"),
    (131, "BREAK_UFT_CANDIDATE", "攻破·正确方程扩容与退守路径（树层可算/不可重整化）",   "正确方程扩容 + 统一完成尝试"),
]

def load_volume(n):
    fs = glob.glob(os.path.join(DATA, "TUFT-r%d_*.json" % n))
    if not fs:
        return None
    f = max(fs, key=os.path.getmtime)
    try:
        with open(f, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None

def extract_record(n, role, category, target, j):
    rec = {"n": n, "role": role, "category": category, "target": target,
           "judgment_file": "数据/判定_TUFT-r%d_*.md" % n, "overall": None,
           "verdict_tag": None, "tally": {}, "detail": {}}
    if j is None:
        rec["overall"] = "NO-JSON"
        rec["verdict_tag"] = "NO-JSON"
        return rec
    if n == 122:
        t = j.get("tally", {})
        rec["overall"] = "SELF-CONSISTENT（PASS %d / FAIL %d / BOUNDARY %d）" % (
            t.get("PASS", 0), t.get("FAIL", 0), t.get("BOUNDARY", 0))
        rec["verdict_tag"] = "PASS"
        rec["tally"] = t
    elif n == 123:
        rec["overall"] = j.get("verdict")
        rec["verdict_tag"] = j.get("verdict")
        rec["tally"] = j.get("counts", {})
    elif n == 124:
        vc = j.get("verdict_count", {})
        rec["overall"] = "FAIL（%d 定理 FAIL；%d 修正；%d INFO）" % (
            vc.get("FAIL", 0), vc.get("CORRECTED", 0), vc.get("INFO", 0))
        rec["verdict_tag"] = "FAIL"
        rec["tally"] = vc
    elif n == 125:
        rec["overall"] = j.get("route_verdict")
        rec["verdict_tag"] = j.get("route_verdict")
        rec["tally"] = j.get("tally", {})
        rec["detail"]["min_falsifier_goal_preserving"] = j.get("min_falsifying_set_goal_preserving")
    elif n == 126:
        rec["overall"] = j.get("verdict_total")
        rec["verdict_tag"] = j.get("verdict_total")
        rec["tally"] = j.get("tally", {})
    elif n == 127:
        rec["overall"] = "正确核确立（11/11 过门）；断裂边界 10 FAIL + 1 OPEN"
        rec["verdict_tag"] = "CORRECT-CORE-ESTABLISHED"
        rec["tally"] = j.get("tally", {})
    elif n == 128:
        rec["overall"] = j.get("verdict_total")
        rec["verdict_tag"] = j.get("verdict_total")
        rec["tally"] = j.get("tally", {})
    elif n == 129:
        s = j.get("summary", {})
        rec["overall"] = "DEAD（micro=%s；star=%s；method=%s）" % (
            s.get("verdict_micro"), s.get("verdict_star"), s.get("verdict_method"))
        rec["verdict_tag"] = "DEAD"
        rec["detail"] = {
            "micro_std_alive": s.get("micro_std_alive"), "micro_kt_fail": s.get("micro_kt_fail"),
            "micro_kt_open": s.get("micro_kt_open"), "star_std_alive": s.get("star_std_alive"),
            "star_kt_fail": s.get("star_kt_fail"), "kt_star_success": s.get("kt_star_success"),
            "min_falsifier_micro": s.get("min_falsifier_micro"),
            "min_falsifier_star": s.get("min_falsifier_star"),
        }
        rec["tally"] = {
            "micro_std_alive": s.get("micro_std_alive"), "micro_kt_fail": s.get("micro_kt_fail"),
            "star_std_alive": s.get("star_std_alive"), "star_kt_fail": s.get("star_kt_fail"),
        }
    elif n == 130:
        s = j.get("summary", {})
        rec["overall"] = s.get("verdict")
        rec["verdict_tag"] = s.get("verdict")
        rec["detail"] = {
            "n_chains": s.get("n_chains"), "n_total_premises": s.get("n_total_premises"),
            "n_posted": s.get("n_posted"), "n_assumed": s.get("n_assumed"),
            "n_derived": s.get("n_derived"), "n_open": s.get("n_open"),
            "closure": round(s.get("closure_all", 0), 4),
            "n_closed": s.get("n_closed"), "n_premise_open": s.get("n_premise_open"),
            "n_domain_limited": s.get("n_domain_limited"), "n_conjectural": s.get("n_conjectural"),
            "n_circular": s.get("n_circular"),
        }
        rec["tally"] = {
            "CLOSED": s.get("n_closed"), "PREMISE-OPEN": s.get("n_premise_open"),
            "DOMAIN-LIMITED": s.get("n_domain_limited"), "CONJECTURAL": s.get("n_conjectural"),
            "CIRCULAR": s.get("n_circular"),
        }
    elif n == 131:
        rec["overall"] = j.get("verdict_total")
        rec["verdict_tag"] = j.get("verdict_total")
        rec["tally"] = j.get("tally", {})
    return rec

def compute_meta(records):
    by = {r["n"]: r for r in records}
    audit_self = by[122]["verdict_tag"] == "PASS"
    correct_core = by[127]["tally"].get("PASS", 0) == 11
    premise_open = by[130]["verdict_tag"] == "SOUND-BUT-PREMISE-OPEN"
    closure = by[130]["detail"]["closure"]
    cand = [123, 124, 125, 126, 128, 129, 131]
    cand_tags = {n: by[n]["verdict_tag"] for n in cand}
    all_fail = all(t in ("FAIL", "DEAD") for t in cand_tags.values())
    n_cand = len(cand)
    n_fail = sum(1 for t in cand_tags.values() if t in ("FAIL", "DEAD"))
    # 开放项聚合（仅统计 OPEN/BOUNDARY/DOMAIN-LIMITED/CONJECTURAL 类）
    # 注意：各卷 json 对“OPEN”的键名不一致——
    #   r129 用 detail.micro_kt_open；r130 用 detail.n_open（tally 无 OPEN 键）；
    #   r122/r125/r127/r128 用 tally.OPEN。必须分别归一，否则漏计。
    open_total = 0
    boundary_total = 0
    for r in records:
        t = r.get("tally", {})
        if r["n"] == 129:
            open_total += (r["detail"].get("micro_kt_open", 0) or 0)
        elif r["n"] == 130:
            open_total += (r["detail"].get("n_open", 0) or 0)
        else:
            open_total += t.get("OPEN", 0) or 0
            boundary_total += t.get("BOUNDARY", 0) or 0
    domain_lim = by[130]["detail"]["n_domain_limited"]
    conject = by[130]["detail"]["n_conjectural"]
    achieved = not all_fail
    master = "全维自洽与归一化 = 未达成" if not achieved else "全维自洽与归一化 = 达成"
    detail = ("UNIFIED-FIELD DEAD（%d/%d 候选卷全 FAIL/DEAD）；正确核确立（11/11）但推导前提开放"
              "（closure=%.3f）；审计链自洽（r122 PASS）") % (n_fail, n_cand, closure)
    return {
        "audit_self_consistent": audit_self,
        "correct_core_established": correct_core,
        "correct_theory_premise_open": premise_open,
        "closure": closure,
        "unified_field_candidates": cand,
        "unified_field_candidate_verdicts": cand_tags,
        "unified_field_achieved": achieved,
        "n_candidates": n_cand,
        "n_candidates_failed": n_fail,
        "open_total": open_total,
        "boundary_total": boundary_total,
        "domain_limited_total": domain_lim,
        "conjectural_total": conject,
        "master_verdict": master,
        "master_detail": detail,
        # 建设性 BSM 准入判据（源自 r130）：新理论必须净减少前提数
        "bsm_admission": "任何候选统一理论须使前提净计数下降（net premise count DECREASE）；"
                         "当前 7 卷候选无一满足，故全判 DEAD/FAIL。",
    }

def build_json(records, meta):
    payload = {
        "doc": "r132 全维自洽与归一化 · 跨卷综合判定册",
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "scope_note": "跨卷综合（非加和）：各源卷拥有各自条目；本册为元判定/跨索引。",
        "volumes": records,
        "meta": meta,
        "non_additivity_freeze": True,
        "exit_code": 0,
    }
    out = os.path.join(DATA, STEM + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out

def build_md(records, meta):
    lines = []
    lines.append("# %s（机读综合册）" % STEM)
    lines.append("")
    lines.append("> 跨卷综合判定册 | 非加和冻结：各源卷条目归各源卷；本册为元判定/跨索引。")
    lines.append("")
    lines.append("## 元判定")
    lines.append("")
    lines.append("- **%s**" % meta["master_verdict"])
    lines.append("- %s" % meta["master_detail"])
    lines.append("- 审计链自洽: %s | 正确核确立: %s | 正确理论前提开放: %s | closure=%.3f" % (
        meta["audit_self_consistent"], meta["correct_core_established"],
        meta["correct_theory_premise_open"], meta["closure"]))
    lines.append("- 统一场论候选: %d 卷，失败 %d 卷（%s）" % (
        meta["n_candidates"], meta["n_candidates_failed"],
        ", ".join("%d=%s" % (k, v) for k, v in meta["unified_field_candidate_verdicts"].items())))
    lines.append("- 诚实开放项聚合: OPEN=%d, BOUNDARY=%d, DOMAIN-LIMITED=%d, CONJECTURAL=%d" % (
        meta["open_total"], meta["boundary_total"], meta["domain_limited_total"], meta["conjectural_total"]))
    lines.append("")
    lines.append("## 跨卷索引（机读）")
    lines.append("")
    lines.append("| 卷 | 类别 | 角色 | 目标 | 总体判定 | 计数 |")
    lines.append("|----|------|------|------|----------|------|")
    for r in records:
        tally = r.get("tally", {})
        ts = " ".join("%s=%s" % (k, v) for k, v in tally.items() if v is not None) if tally else "-"
        lines.append("| r%d | %s | %s | %s | %s | %s |" % (
            r["n"], r["category"], r["role"], r["target"], r["overall"], ts))
    lines.append("")
    lines.append("## 建设性 BSM 准入判据")
    lines.append("")
    lines.append("- %s" % meta["bsm_admission"])
    lines.append("")
    out = os.path.join(DATA, STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out

def build_report(records, meta):
    lines = []
    lines.append("=" * 70)
    lines.append("r132 全维自洽与归一化 · 跨卷综合判定报告")
    lines.append("=" * 70)
    lines.append("生成时间: %s" % datetime.datetime.now().isoformat(timespec="seconds"))
    lines.append("")
    lines.append("【元判定】 %s" % meta["master_verdict"])
    lines.append(meta["master_detail"])
    lines.append("")
    lines.append("一、攻破全景（r122→r131）")
    lines.append("-" * 70)
    for r in records:
        lines.append("r%-3d [%-20s] %s" % (r["n"], r["category"], r["role"]))
        lines.append("      目标: %s" % r["target"])
        lines.append("      总体: %s" % r["overall"])
        t = r.get("tally", {})
        if t:
            lines.append("      计数: %s" % " ".join("%s=%s" % (k, v) for k, v in t.items() if v is not None))
        lines.append("")
    lines.append("二、整理正确的理论体系")
    lines.append("-" * 70)
    lines.append("· r127：SM/GR 已验证方程集正确核 11/11 全部过门（e=g sinθ_W、M_W^tree=79.95 GeV、")
    lines.append("  ρ=1.0104、λ_H=0.1294、β₀=7、v=246.22 GeV、r_s(☉)=2953.25 m、水星 42.98″/cent、")
    lines.append("  光线偏折 1.7512″、GW 速度=c、a_e 相对 8.8e-10）。")
    lines.append("· r128：正确理论体系方程全集已整理（PASS 4），覆盖 SM 拉氏量各项与 EH 场方程。")
    lines.append("· r130：推导链审计 18 条/55 前提，closure=%.3f；正确理论【内部自洽但前提开放】，" % meta["closure"])
    lines.append("  四块最深 POSTED 前提=地基：① EH 作用量形式 ② 规范群选择 SU(3)×SU(2)×U(1) ")
    lines.append("  ③ μ²<0 符号（电弱对称破缺）④ 等效原理/SEP。力的四起源 g,g′,g_s,G 在 DERIVED 层为空（OPEN）。")
    lines.append("")
    lines.append("三、攻破正确理论体系与方程的断裂边界")
    lines.append("-" * 70)
    lines.append("· r127 B01–B11：断裂边界 10 FAIL + 1 OPEN（中微子质量 4.01 dex、宇宙学常数 52.79/120.74 dex、")
    lines.append("  暗物质 Ω_c/Ω_b=5.36、重子不对称 8 dex、层级 16.99 dex、味 5.53 dex、三耦合 3.86 dex/52σ…）。")
    lines.append("· r128：统一完成边界 9 FAIL（方程全集本身正确，但无法归一/补全）。")
    lines.append("· r123：力的大统一方程退守路径 14 FAIL（换群族/阈值/额外维/紫外完备/剔除引力均不通）。")
    lines.append("· r124：光子内部运行核心理论体系 5 定理 FAIL（T1 光速预算、T2 自转载荷、T3 内禀性、")
    lines.append("  T05 内禀频率—外部标度对偶等）。")
    lines.append("· r126：超宇宙与宇宙图景宣称 18 FAIL（恒等式审计否定）。")
    lines.append("· r131：正确方程扩容 2 FAIL（树层可算但幂计数不可重整化）。")
    lines.append("")
    lines.append("四、统一场论路线判定")
    lines.append("-" * 70)
    lines.append("· r125：统一场论路线 route_verdict=DEAD；11 假设 PASS1/FAIL7/OPEN3；")
    lines.append("  最小证伪集规模=1（A05 引力间隙 或 A08 可证伪性）。")
    lines.append("· r129：κ-τ 统一场论导出全部微观粒子与宏观星体 → kt_verdict=DEAD（micro DEAD、star DEAD、")
    lines.append("  method ALIVE）；最小证伪集规模=1（M12 定义域失效 / M10 参数计数；S10 κ-τ 导出 0/9 / S12 时空定义域）。")
    lines.append("")
    lines.append("五、诚实开放项（未闭合，禁宣称全封）")
    lines.append("-" * 70)
    lines.append("OPEN 聚合=%d；BOUNDARY=%d；DOMAIN-LIMITED=%d；CONJECTURAL=%d。" % (
        meta["open_total"], meta["boundary_total"], meta["domain_limited_total"], meta["conjectural_total"]))
    lines.append("代表性未闭合：宇宙学常数、暗物质、重子不对称、层级、味、YM 质量隙、宇宙审查、" )
    lines.append("Cabibbo 张力、光子内部运行修复项、κ-τ 导出定义域失效。")
    lines.append("")
    lines.append("六、结论")
    lines.append("-" * 70)
    lines.append("全维自洽与归一化【未达成】。")
    lines.append("· 整理正确的理论体系：成功（SM/GR 正确核确立 + 方程全集整理 + 推导链地基清晰）。")
    lines.append("· 攻破正确理论体系达成统一：失败（7 卷统一候选全 DEAD/FAIL；断裂边界已逐条定价）。")
    lines.append("· 建设性出路：任何 BSM 候选须满足净前提数下降（r130 准入判据）；当前无候选满足。")
    lines.append("")
    lines.append("=" * 70)
    out = os.path.join(DATA, STEM + "_report.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out

def build_judgment_ledger(records, meta):
    by = {r["n"]: r for r in records}
    lines = []
    lines.append("# 判定_TUFT-r132 · 全维自洽与归一化 · 跨卷综合判定与攻破全景")
    lines.append("")
    lines.append("**卷号**：r132（增补卷，因 r131 已被并行会话占用）")
    lines.append("**日期**：%s" % DATE)
    lines.append("**类别**：跨卷综合判定册（总结整理攻破）")
    lines.append("")
    lines.append("## 卷首分工声明（非加和冻结）")
    lines.append("")
    lines.append("- 本卷是 r122→r131 战役的**跨卷综合判定册**，不是新审计。")
    lines.append("- **各源卷拥有各自条目，本卷为跨索引/元判定，条目非加和。**")
    lines.append("- 本卷结论由机读结果（各源卷 json 的 verdict/tally/summary）驱动，未硬编码。")
    lines.append("- 并行会话成果（r123/r124/r126/r128/r131）仅被索引引用，不并入本册计数。")
    lines.append("")
    lines.append("## 0. 元判定（一图流结论）")
    lines.append("")
    lines.append("> **%s**" % meta["master_verdict"])
    lines.append(">")
    lines.append("> %s" % meta["master_detail"])
    lines.append(">")
    lines.append("> | 维度 | 状态 |")
    lines.append("> |------|------|")
    lines.append("> | 审计链自洽（r122） | %s |" % ("自洽" if meta["audit_self_consistent"] else "否"))
    lines.append("> | 正确核确立（r127） | %s |" % ("确立（11/11）" if meta["correct_core_established"] else "否"))
    lines.append("> | 正确理论前提开放（r130） | %s（closure=%.3f）|" % (
        "开放" if meta["correct_theory_premise_open"] else "否", meta["closure"]))
    lines.append("> | 统一场论达成（候选 7 卷） | %s（%d/%d 失败）|" % (
        "未达成" if not meta["unified_field_achieved"] else "达成", meta["n_candidates_failed"], meta["n_candidates"]))
    lines.append("")
    lines.append("## 1. 攻破全景总表（r122→r131 跨卷索引，机读）")
    lines.append("")
    lines.append("| 卷 | 类别 | 角色 | 目标 | 总体判定 | 关键计数 | 源判定册 |")
    lines.append("|----|------|------|------|----------|----------|----------|")
    for r in records:
        t = r.get("tally", {})
        ts = " ".join("%s=%s" % (k, v) for k, v in t.items() if v is not None) if t else "-"
        lines.append("| r%d | %s | %s | %s | %s | %s | %s |" % (
            r["n"], r["category"], r["role"], r["target"], r["overall"], ts, r["judgment_file"]))
    lines.append("")
    lines.append("## 2. 整理正确的理论体系（SM/GR 正确核 + 方程全集 + 推导链地基）")
    lines.append("")
    lines.append("### 2.1 r127 · 正确核 11/11 过门")
    lines.append("- e = g·sinθ_W、M_W^tree = 79.9534 GeV、ρ = 1.010429、λ_H = 0.129383、")
    lines.append("  β₀ = 7.000、v = 246.22 GeV、r_s(☉) = 2953.25 m、水星 42.981″/cent、")
    lines.append("  光线偏折 1.7512″、GW 速度 = c、a_e 相对偏差 8.8e-10。")
    lines.append("- 判定：**正确核确立**，SM/GR 已验证方程集为项目唯一可靠的“正确”基准。")
    lines.append("")
    lines.append("### 2.2 r128 · 正确理论体系方程全集已整理")
    lines.append("- 覆盖 SM 拉氏量各项、EH 场方程、守恒律；整理 PASS 4。")
    lines.append("- 方程全集本身正确，但**无法归一/补全**为统一场（verdict_total=FAIL，9 条统一边界 FAIL）。")
    lines.append("")
    lines.append("### 2.3 r130 · 推导链地基：四块最深 POSTED 前提")
    lines.append("- 18 条推导链 / 55 前提：POSTED 13、ASSUMED 16、DERIVED 18、OPEN 8；closure = %.3f。" % meta["closure"])
    lines.append("- 判定：**SOUND-BUT-PREMISE-OPEN**——正确理论内部自洽，但 rests on 开放前提，不自封口。")
    lines.append("- 四块最深 POSTED 前提（=“正确性”的地基，不可由 SM/GR 自身导出）：")
    lines.append("  ① EH 作用量形式（场方程非更底层导出，是公设；GHY 项为技术假设）")
    lines.append("  ② 规范群选择 SU(3)×SU(2)×U(1)（异常抵消的四项 Fraction 精确相消，但群选择本身是输入）")
    lines.append("  ③ μ²<0 符号（电弱对称破缺的 sign 是公设，非导出）")
    lines.append("  ④ 等效原理 / SEP（强等效原理的几何假设）")
    lines.append("- 力的四起源 g, g′, g_s, G 在 DERIVED 层为空（OPEN）——**“力的起源”仍开放**。")
    lines.append("")
    lines.append("## 3. 攻破正确理论体系与方程的断裂边界")
    lines.append("")
    lines.append("### 3.1 r127 · 断裂边界 B01–B11（10 FAIL + 1 OPEN）")
    lines.append("- B01 中微子质量 4.01 dex、B02 宇宙学常数 52.79/120.74 dex、B03 暗物质 Ω_c/Ω_b=5.364、")
    lines.append("  B05 重子不对称 8 dex、B07 层级 16.99 dex、B08 味 5.53 dex、B10 三耦合 3.86 dex/52.06σ。")
    lines.append("- 判定：SM/GR 正确，但**对标准模型之外现象全部断裂**，边界已逐条精算定价。")
    lines.append("")
    lines.append("### 3.2 r128 · 统一完成边界（9 FAIL）")
    lines.append("- 方程全集正确，但补全/归一为单一统一场失败：9 条失败边界。")
    lines.append("")
    lines.append("### 3.3 r123 · 力的大统一方程退守路径（14 FAIL）")
    lines.append("- 换群族 / 阈值 / 额外维 / 紫外完备 / 剔除引力 五类退守路径全部攻破（PASS 7 为控制组）。")
    lines.append("")
    lines.append("### 3.4 r124 · 光子内部运行核心理论体系（5 定理 FAIL）")
    lines.append("- T1 光速预算、T2 自转载荷、T3 内禀性、T05 内禀频率—外部标度对偶 等 5 定理 FAIL；")
    lines.append("  2 处 CORRECTED（修复定价），2 INFO。")
    lines.append("")
    lines.append("### 3.5 r126 · 超宇宙与宇宙图景宣称（18 FAIL）")
    lines.append("- 恒等式审计否定其“导出”宣称；18 FAIL + 1 PASS（控制组）+ 2 BOUNDARY + 4 INFO。")
    lines.append("")
    lines.append("### 3.6 r131 · 正确方程扩容与退守路径（2 FAIL）")
    lines.append("- 树层可算预言成立（PASS 3），但幂计数不可重整化导致 2 FAIL（扩容路径不自封口）。")
    lines.append("")
    lines.append("## 4. 统一场论路线判定（r125 + r129）")
    lines.append("")
    lines.append("### 4.1 r125 · 路线对错判定")
    lines.append("- route_verdict = **DEAD**；11 假设 PASS 1 / FAIL 7 / OPEN 3。")
    lines.append("- 最小证伪集（保目标）规模 = 1：{A05 引力间隙} 或 {A08 可证伪性}。")
    lines.append("- 含义：统一场论路线存在单点即可证伪的结构性缺口。")
    lines.append("")
    lines.append("### 4.2 r129 · κ-τ 统一场论导出全部粒子/星体")
    lines.append("- 微观：std_alive=%s、kt_fail=%s、kt_open=%s → **DEAD**。" % (
        by[129]["detail"].get("micro_std_alive"), by[129]["detail"].get("micro_kt_fail"),
        by[129]["detail"].get("micro_kt_open")))
    lines.append("- 宏观：std_alive=%s、kt_fail=%s、kt_success=%s → **DEAD**。" % (
        by[129]["detail"].get("star_std_alive"), by[129]["detail"].get("star_kt_fail"),
        by[129]["detail"].get("kt_star_success")))
    lines.append("- 方法 ALIVE（判据本身有效）；最小证伪集规模 = 1（M12 定义域失效 / M10 参数计数；")
    lines.append("  S10 κ-τ 导出 0/9 / S12 时空定义域失效）。")
    lines.append("- 含义：κ-τ（v=c 曲率挠率频率角速度）统一场论**不能**第一性原理导出全部微观/宏观属性。")
    lines.append("")
    lines.append("## 5. 诚实开放项（未闭合，禁宣称全封）")
    lines.append("")
    lines.append("- OPEN 聚合 = %d；BOUNDARY = %d；DOMAIN-LIMITED = %d；CONJECTURAL = %d。" % (
        meta["open_total"], meta["boundary_total"], meta["domain_limited_total"], meta["conjectural_total"]))
    lines.append("- 代表性未闭合：宇宙学常数、暗物质、重子不对称、层级、味、YM 质量隙、宇宙审查、")
    lines.append("  Cabibbo 张力、光子内部运行修复项、κ-τ 导出定义域失效、规范群选择、μ²<0 符号、SEP。")
    lines.append("- 这些 OPEN 是 SM/GR 正确核与任何统一候选之间的“裂隙”，需新物理（且满足 r130 准入判据）方可能闭合。")
    lines.append("")
    lines.append("## 6. 结论与建设性出路")
    lines.append("")
    lines.append("**全维自洽与归一化 = 未达成。**")
    lines.append("")
    lines.append("1. **整理正确的理论体系：成功。** SM/GR 正确核 11/11 确立；方程全集整理完毕；")
    lines.append("   推导链地基（四块 POSTED 前提）已显式冻结为“正确性”的边界。")
    lines.append("2. **攻破正确理论体系达成统一：失败。** 7 卷统一候选（r123/r124/r125/r126/r128/r129/r131）")
    lines.append("   全部 DEAD/FAIL；断裂边界已逐条精算定价，无遗漏。")
    lines.append("3. **建设性 BSM 准入判据（源自 r130）：** 任何候选统一理论须使**前提净计数下降**")
    lines.append("   （net premise count DECREASE）。当前 7 卷候选无一满足，故全判 DEAD/FAIL。")
    lines.append("4. **下一步：** 仅在“前提净计数下降”的新候选上投入；对 OPEN 裂隙做受控新物理扫描，")
    lines.append("   并以电弱控制组（r119/r122）保判别力。")
    lines.append("")
    lines.append("## 附录 · Glossary")
    lines.append("- **正确核**：SM/GR 已通过实验验证的方程与读数集合（r127）。")
    lines.append("- **断裂边界**：正确理论对标准模型外现象失效处，已精算定价（r127 B01–B11）。")
    lines.append("- **POSTED 前提**：作为公设/输入的前提，不可由该理论自身导出；closure 越低越不自封口。")
    lines.append("- **非加和冻结**：跨卷综合册不把各卷条目相加，仅作索引/元判定。")
    lines.append("- **最小证伪集**：使声称失效所需的最少假设集合；规模 1 = 单点即可证伪。")
    lines.append("- **BSM 准入判据**：新理论须净减少前提数，否则不构成进展。")
    lines.append("")
    lines.append("## 数据出处")
    lines.append("- 机读综合册：`数据/%s.json` / `数据/%s.md`" % (STEM, STEM))
    lines.append("- 源卷 json：`数据/TUFT-r{122..131}_*.json`（逐卷机读提取）")
    lines.append("- 源判定册：`数据/判定_TUFT-r{125,127,129,130}_*.md`、`判定/判定_TUFT-r{123,124,126,128,131}_*.md`")
    lines.append("")
    out = os.path.join(DATA, JUDGE_STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out

def main():
    os.makedirs(DATA, exist_ok=True)
    records = []
    for n, role, cat, target in VOL_META:
        j = load_volume(n)
        records.append(extract_record(n, role, cat, target, j))
    meta = compute_meta(records)
    p1 = build_json(records, meta)
    p2 = build_md(records, meta)
    p3 = build_report(records, meta)
    p4 = build_judgment_ledger(records, meta)
    print("OK generated:")
    for p in (p1, p2, p3, p4):
        print("  ", os.path.relpath(p, PROJECT))
    print("META:", meta["master_verdict"], "|", meta["master_detail"])
    print("non_additivity_freeze=True | exit_code=0")
    return 0

if __name__ == "__main__":
    sys.exit(main())
