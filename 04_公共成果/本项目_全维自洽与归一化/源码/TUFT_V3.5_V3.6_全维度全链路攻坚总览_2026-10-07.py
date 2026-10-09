# -*- coding: utf-8 -*-
"""
TUFT V3.5/V3.6 · 全维度全链路攻坚总览引擎 —— 2026-10-07
=========================================================================
扫描数据目录全部 TUFT 攻坚册 json，抽取 verdict 计数 / 自检 / 核心结论，
按攻坚链阶段归类，输出全链路状态矩阵（供总览整理册引用，回链不重算）。

阶段归类（文件名关键词 → 攻坚链阶段）：
  SRCAUDIT   溯源审计（四力三要素/终极正确性/核心公式/修复方案元审计）
  MARKER     记号层（可视化证明修复版/修复方案攻破）
  PARAM      参量层（Ω公理/O-FIELD/开放项/角度分区/修复规范）
  PHYS       物理层（C_L_C_R/β衰变/手征）
  IDENT      可识别性（可识别性解阻/δA/三条出路/自由度/跨链归一/七册）
  WALK4      走④链（走④落地/延伸/记账重做/φ0根因/候选S_T/收束）
  ACCEPT     验收修复链（修复版_验收/独立再验收/盲区回修/回修版）
  MCMCP      MCMC/预言（MATH-PROOF-ADD MCMC/预言版）
  CONCUR     并发（V3.6/GAQ/OPEN-MAP/ESCAPE/v_eq_c）
  EARLY      早期背景（空间螺旋）

红线：本引擎只扫描/归并现有 json 的已登记读数，不重算任何一册；
数据 json 结构不一（字段名差异），读取容错；缺失字段记 NULL。
纯标准库，零第三方依赖。
"""

import os
import sys
import json
import time
import glob

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA_DIR = os.path.join(BASE, "数据")

RESULTS = []
GUARDS = []


def add(cid, sec, item, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-34s | %s" % (verdict, cid, item, detail[:170]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-34s | %s | %s" % (name, "PASS" if ok else "FAIL", detail))
    return bool(ok)


def classify(fname):
    if fname.startswith("空间螺旋"):
        return "EARLY", "早期背景（空间螺旋体系）"
    if fname.startswith("GAQ_UFT_V18") or fname.startswith("TUFT_V3.6") or "OPEN-MAP" in fname \
       or "ESCAPE-AUDIT" in fname or fname.startswith("v_eq_c"):
        return "CONCUR", "并发·审计/动力学"
    if "走④" in fname or "候选S_T" in fname or "记账重做" in fname or "φ0零信息" in fname:
        return "WALK4", "走④链（公设放宽→收束）"
    if "验收" in fname or "盲区回修" in fname or "回修版" in fname:
        return "ACCEPT", "验收修复链"
    if "MCMC" in fname or "预言版" in fname:
        return "MCMCP", "MCMC/预言攻坚"
    if "可识别性" in fname or "δA" in fname or "三条出路" in fname or "自由度预算" in fname \
       or "并发产物审阅" in fname or "三链归一" in fname or "七册" in fname:
        return "IDENT", "可识别性/跨册归一"
    if "C_L_C_R" in fname or "β衰变" in fname or "手征" in fname:
        return "PHYS", "物理层（手征/β）"
    if "Ω公理" in fname or "O-FIELD" in fname or "开放项" in fname or "修复规范" in fname \
       or "W6W1" in fname or "闵氏" in fname or "里程碑" in fname or "Bishop" in fname:
        return "PARAM", "参量层（Ω/分区/场构型）"
    if "可视化证明_TUFT_V3.5_修复版" in fname or "修复方案_求导" in fname or "修复方案_全维" in fname:
        return "MARKER", "记号层（量纲/修复）"
    if "可视化证明_四力" in fname or "终极正确性" in fname or "四力统一方程" in fname \
       or "核心公式" in fname or "可视化" in fname:
        return "SRCAUDIT", "溯源审计"
    return "OTHER", "其他"


def _get(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and k in d and d[k] is not None:
            return d[k]
    return default


def load_counts(d):
    c = _get(d, "计数", "counts", "verdict_counts")
    if isinstance(c, dict):
        return {str(k): int(v) for k, v in c.items() if str(v).lstrip("-").isdigit()}
    return {}


def load_selfcheck(d):
    sc = _get(d, "自检", "selfcheck", "guards")
    if isinstance(sc, dict):
        return {"total": _get(sc, "总数", "total", default=None),
                "pass": _get(sc, "通过", "passed", "ok", default=None)}
    return {"total": None, "pass": None}


def main():
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*.json")))
    relevant = [f for f in files if any(k in os.path.basename(f) for k in
                ("TUFT", "统一场论", "GAQ", "空间螺旋", "v_eq_c", "本项目_TUFT"))]

    per_stage = {}
    entries = []
    n_read = 0
    for f in relevant:
        name = os.path.basename(f)[:-5]
        try:
            with open(f, "r", encoding="utf-8") as fh:
                d = json.load(fh)
        except Exception as e:
            entries.append({"册": name, "阶段": "ERR", "读": "FAIL", "note": "json读取失败 %s" % e})
            continue
        n_read += 1
        stage, stage_note = classify(name)
        cnt = load_counts(d)
        total = cnt.get("总计", _get(d, "总计", "total", default=None))
        tot = sum(cnt.get(k, 0) for k in ("PASS", "FAIL", "BOUNDARY", "INFO",
                                          "MISMATCH", "CORRECTED")) or total or None
        sc = load_selfcheck(d)
        core = _get(d, "核心结论", "结论", "一句话结论", "核心", default=None)
        if core and isinstance(core, str) and len(core) > 220:
            core = core[:220] + "…"
        entries.append({"册": name, "阶段": stage, "阶段说明": stage_note,
                        "PASS": cnt.get("PASS"), "FAIL": cnt.get("FAIL"),
                        "BOUNDARY": cnt.get("BOUNDARY"), "INFO": cnt.get("INFO"),
                        "MISMATCH": cnt.get("MISMATCH"), "CORRECTED": cnt.get("CORRECTED"),
                        "总计": tot, "自检通过": sc["pass"], "自检总数": sc["total"],
                        "核心结论": core})
        per_stage.setdefault(stage, []).append(name)

    stages_order = ["SRCAUDIT", "MARKER", "PARAM", "PHYS", "IDENT", "WALK4",
                    "ACCEPT", "MCMCP", "CONCUR", "EARLY", "OTHER"]
    stage_desc = {"SRCAUDIT": "溯源审计", "MARKER": "记号层", "PARAM": "参量层",
                  "PHYS": "物理层", "IDENT": "可识别性", "WALK4": "走④链",
                  "ACCEPT": "验收修复链", "MCMCP": "MCMC/预言", "CONCUR": "并发审计",
                  "EARLY": "早期背景", "OTHER": "其他"}

    add("A-01", "扫描", "TUFT 相关 json 册", "PASS",
        "扫描数据目录 %d 个 json，命中 TUFT/统一场论/GAQ/空间螺旋 相关 %d 个，成功读取 %d 个"
        % (len(files), len(relevant), n_read))
    guard("scanned", n_read >= 50, "读取 TUFT 相关册 %d 个" % n_read)

    # 每阶段计数
    stage_summary = []
    for st in stages_order:
        if st in per_stage:
            stage_summary.append({"阶段": st, "阶段说明": stage_desc.get(st, st),
                                  "册数": len(per_stage[st])})
    add("B-01", "归并", "阶段归类", "PASS",
        "阶段册数：%s" % " / ".join("%s=%d" % (stage_desc.get(s["阶段"], s["阶段"]), s["册数"]) for s in stage_summary))
    guard("classified", len(per_stage) >= 6, "按阶段归类 %d 类" % len(per_stage))

    # =====================================================================
    # 汇总
    # =====================================================================
    payload = {
        "册": "TUFT_V3.5_V3.6_全维度全链路攻坚总览引擎",
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "扫描": {"总json": len(files), "相关": len(relevant), "成功读取": n_read},
        "阶段": stage_summary,
        "条目明细": entries,
        "红线": "只扫描/归并现有 json 已登记读数，不重算；字段缺失记 NULL",
    }
    base = os.path.join(DATA_DIR, "TUFT_V3.5_V3.6_全维度全链路攻坚总览_2026-10-07")
    with open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    md = ["# TUFT V3.5/V3.6 · 全维度全链路攻坚总览（机器扫描）", "",
          "- 生成时间：%s" % payload["生成时间"],
          "- 扫描 %d json，命中 %d 相关，成功读取 %d" % (len(files), len(relevant), n_read),
          "", "## 阶段册数", "", "| 阶段 | 说明 | 册数 |", "|---|---|---|"]
    for s in stage_summary:
        md.append("| %s | %s | %d |" % (s["阶段"], s["阶段说明"], s["册数"]))
    md += ["", "## 册明细（verdict 计数）", "",
           "| 阶段 | 册 | PASS | FAIL | BOUND | INFO | MIS | CORR | 总计 | 自检 | 核心结论 |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for e in entries:
        md.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s/%s | %s |" % (
            e["阶段"], e["册"], e["PASS"], e["FAIL"], e["BOUNDARY"], e["INFO"],
            e["MISMATCH"], e["CORRECTED"], e["总计"], e["自检通过"], e["自检总数"],
            (e["核心结论"] or "")[:60]))
    md.append("")
    with open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))

    print("-" * 74)
    print("扫描 %d json，TUFT 相关 %d，成功读取 %d" % (len(files), len(relevant), n_read))
    print("阶段册数：" + " / ".join("%s=%d" % (stage_desc.get(s["阶段"], s["阶段"]), s["册数"]) for s in stage_summary))
    print("产物：%s.json / .md" % base)
    if n_read < 50:
        print("WARN: 读取册数偏少")
    return 0


if __name__ == "__main__":
    sys.exit(main())
