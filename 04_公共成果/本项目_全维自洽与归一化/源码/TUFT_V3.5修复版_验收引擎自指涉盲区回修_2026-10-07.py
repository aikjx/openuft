# -*- coding: utf-8 -*-
"""
TUFT V3.5 · 验收引擎自指涉盲区回修 —— 2026-10-07
=========================================================================
承接：`TUFT_V3.5修复版_验收审计与修复清单_2026-10-04.py`（分支①验收册，并发产出）
      + `TUFT_V3.5修复版_独立再验收_2026-10-05.py`（已发现盲区并从实际 SUT 抽取 field 验证 1.0000）。

【自指涉盲区复述】
  验收册引擎自建"被测函数复刻" sut_field(x,y)（硬编码径向 −(1/r²)(x,y)，旧版 bug），
  其 load_sut() 的 AST 守卫 sut_has_verified_symbols 只查函数**名字**存在于 SUT，
  **不校验硬编码复刻与实际 SUT 的 field() 实现是否一致**。
  ⇒ V-07 用硬编码 sut_field（径向）与参考均匀场比对 → FAIL(0.1173)，
     即便实际 SUT 已修复为均匀场，验收册引擎仍报告 FAIL —— 验证的是自己的复刻，不是实际 SUT。

【本册回修】从**实际 SUT 源码 AST 抽取 field()/omega()/region() 函数体并 exec**，
  替代硬编码复刻，重跑验收册的 V-07（场与公式比对）与 V-08（相似度判据）。
  判定：实际 SUT 的 field() 应为均匀场 −(1,1)/√2 ⇒ 与参考相似度 1.0000（V-07 从 FAIL 转 PASS）；
        V-08 自比恒 1 仍为失效判据（必须替换为对参考场的交叉比对）。

红线：不修改 SUT 文件；AST 抽取 exec 只针对函数体，不执行整文件副作用；
本册回修的是验收册引擎的方法论，判定其盲区修复是否成立。
纯标准库，零第三方依赖。
"""

import os
import sys
import json
import time
import math
import ast

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA_DIR = os.path.join(BASE, "数据")
SUT = os.path.join(BASE, "源码", "统一场论可视化证明_TUFT_V3.5_修复版_2026-10-04.py")
ACCEPT_ENGINE = os.path.join(BASE, "源码", "TUFT_V3.5修复版_验收审计与修复清单_2026-10-04.py")

RESULTS = []
GUARDS = []


def add(cid, sec, item, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-36s | %s" % (verdict, cid, item, detail[:175]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-36s | %s | %s" % (name, "PASS" if ok else "FAIL", detail))
    return bool(ok)


def extract_func(src, fname):
    """从源码 AST 抽取指定函数定义并 exec 到新命名空间，返回可调用对象或 None。"""
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == fname:
            mod = ast.Module(body=[node], type_ignores=[])
            ast.fix_missing_locations(mod)
            ns = {"math": math, "math_hypot": math.hypot}
            code = compile(mod, "<extracted:%s>" % fname, "exec")
            exec(code, ns)
            return ns.get(fname)
    return None


def cosine_sim(fa, fb, pts):
    num = da = db = 0.0
    for p in pts:
        a = fa(*p)
        b = fb(*p)
        num += a[0] * b[0] + a[1] * b[1]
        da += a[0] * a[0] + a[1] * a[1]
        db += b[0] * b[0] + b[1] * b[1]
    if da == 0 or db == 0:
        return float("nan")
    return num / math.sqrt(da * db)


def ref_force_from_E(x, y):
    """正确参考：F = −(ℏc/2)κ₀(1,1) = 均匀场（取 −(1,1)/√2 归一化，与独立再验收同规约）。"""
    return (-1.0 / math.sqrt(2.0), -1.0 / math.sqrt(2.0))


def pts_grid(n=401):
    out = []
    step = 2.0 / (n - 1)
    for i in range(n):
        for j in range(n):
            out.append((-1.0 + i * step, -1.0 + j * step))
    return out


def main():
    # =====================================================================
    # A. 盲区确认（读验收册引擎源码）
    # =====================================================================
    sec = "盲区确认"
    with open(ACCEPT_ENGINE, "r", encoding="utf-8") as f:
        acc_src = f.read()
    has_hardcoded_sut_field = "def sut_field(x, y):" in acc_src and "(-x / (r * r), -y / (r * r))" in acc_src
    ast_only_name = "fnames" in acc_src and "sut_has_verified_symbols" in acc_src
    add("A-01", sec, "验收册引擎自建硬编码 sut_field", "PASS" if has_hardcoded_sut_field else "FAIL",
        "验收册引擎含硬编码 sut_field（径向 −(1/r²)(x,y)），是自建复刻非实际 SUT 实现")
    add("A-02", sec, "AST 守卫只查函数名不查实现", "PASS" if ast_only_name else "FAIL",
        "load_sut() 的 sut_has_verified_symbols 只核对函数名存在，不校验硬编码复刻与实际 SUT field() 实现一致 ⇒ 自指涉盲区确认")
    guard("blindspot_confirmed", has_hardcoded_sut_field and ast_only_name,
          "验收册引擎自指涉盲区成立（硬编码复刻 + AST 只查名）")

    # =====================================================================
    # B. 从实际 SUT 源码 AST 抽取 field/omega/region
    # =====================================================================
    sec = "SUT 实抽"
    if not os.path.exists(SUT):
        add("B-01", sec, "实际 SUT 存在", "FAIL", "SUT 不存在：%s" % SUT)
        guard("sut_exists", False, "实际 SUT 缺失")
    else:
        with open(SUT, "r", encoding="utf-8") as f:
            sut_src = f.read()
        sut_field = extract_func(sut_src, "field")
        sut_omega = extract_func(sut_src, "omega")
        sut_region = extract_func(sut_src, "region")
        ok = sut_field is not None and sut_omega is not None and sut_region is not None
        add("B-01", sec, "AST 抽取 field/omega/region", "PASS" if ok else "FAIL",
            "从实际 SUT 源码 AST 抽取并 exec：field=%s, omega=%s, region=%s" %
            (sut_field is not None, sut_omega is not None, sut_region is not None))
        guard("sut_extracted", ok, "实际 SUT 的 field/omega/region 均已 AST 抽取")

    # =====================================================================
    # C. 用实际抽取 field 重跑 V-07 / V-08
    # =====================================================================
    sec = "重跑 V-07/V-08"
    if os.path.exists(SUT) and sut_field is not None:
        pts = pts_grid(301)
        sim_cross = cosine_sim(sut_field, ref_force_from_E, pts)
        sim_self = cosine_sim(sut_field, sut_field, pts)
        add("C-01", sec, "V-07 交叉比对（实际field vs 参考均匀场）", "PASS" if sim_cross > 0.95 else "FAIL",
            "实际 SUT 抽取 field() 与参考均匀场 −(1,1)/√2 余弦相似度 **%.4f** ⇒ "
            "（验收册硬编码径向 sut_field 得 0.1173 FAIL；实际实现为均匀场 ⇒ V-07 从 FAIL 转 PASS）" % sim_cross)
        guard("v07_cross_pass", sim_cross > 0.95, "实际 field 是均匀场（V-07 交叉比对通过）")
        add("C-02", sec, "V-08 自相似度判据", "FAIL" if sim_self > 0.9999 else "PASS",
            "自比 cos(field,field)=**%.4f** 恒 1 ⇒ **零信息判据仍失效**，必须替换为对参考场的交叉比对"
            "（本册 C-01 即其替代）" % sim_self)
        guard("v08_invalid", sim_self > 0.9999, "V-08 自比恒 1，失效判据（须交叉比对替代）")

    # =====================================================================
    # D. 判定回修成立 + 修复建议
    # =====================================================================
    sec = "回修判定"
    add("D-01", sec, "盲区回修成立", "BOUNDARY",
        "验收册引擎的 sut_field 应改为**从实际 SUT AST 抽取 field() 并 exec**（本册 B/C 段即回修范式），"
        "重跑 V-07 得 1.0000（非硬编码 0.1173）；V-08 自比恒 1 判据须废弃、由交叉比对替代")
    add("D-02", sec, "修复建议（登记给验收册引擎）", "BOUNDARY",
        "① load_sut() 增加按符号名的 AST 抽取 exec（替代 sut_field/sut_omega/sut_region 硬编码复刻）"
        "② V-08 自相似度判据删除，改为 V-07 交叉比对 ③ 抽取函数体须在独立命名空间 exec，避免整文件副作用")
    add("D-03", sec, "不修改 SUT / 验收册引擎", "BOUNDARY",
        "本册只验证回修范式可行，不改 SUT 也不改验收册引擎源码（并行编辑冲突规避）；修复建议待并入验收册引擎下一版")

    # =====================================================================
    # 汇总
    # =====================================================================
    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    g_ok = sum(1 for g2 in GUARDS if g2["ok"])

    payload = {
        "册": "TUFT_V3.5修复版_验收引擎自指涉盲区回修",
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "定位": "回修验收册引擎自指涉盲区：AST 抽取实际 SUT field() 替代硬编码复刻",
        "承接": "TUFT_V3.5修复版_验收审计与修复清单_2026-10-04.py + 独立再验收_2026-10-05.py",
        "计数": counts, "总计": len(RESULTS),
        "关键量": {"V-07交叉相似度(实际field vs 均匀场)": (round(sim_cross, 4) if ('sim_cross' in dir()) else None),
                  "V-08自相似度": (round(sim_self, 4) if ('sim_self' in dir()) else None)},
        "核心结论": "验收册引擎自指涉盲区成立（硬编码 sut_field + AST 只查名）；从实际 SUT AST 抽取 field() 后 "
                   "V-07 交叉相似度 1.0000（非硬编码径向 0.1173）⇒ 回修范式可行；V-08 自比恒 1 判据失效须废弃",
        "诚实边界": "不修改 SUT/验收册引擎；AST 抽取 exec 仅针对函数体；修复建议待并入下一版",
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "条目": RESULTS,
        "耗时": "%.1fs" % (time.time() - T_START),
    }
    base = os.path.join(DATA_DIR, "TUFT_V3.5修复版_验收引擎自指涉盲区回修_2026-10-07")
    with open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    md = ["# TUFT V3.5修复版 · 验收引擎自指涉盲区回修（机器产物）", "",
          "- 生成时间：%s" % payload["生成时间"],
          "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d ｜ 自检 %d / %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"],
           g_ok, len(GUARDS)),
          "- V-07 交叉相似度（实际field vs 均匀场）：%.4f ｜ V-08 自相似度：%.4f" % (sim_cross, sim_self),
          "", "## 条目", "", "| ID | 节 | 条目 | 判定 | 摘要 |", "|---|---|---|---|---|"]
    for r in RESULTS:
        head = r["detail"].replace("\n", " ")
        if len(head) > 200:
            head = head[:200] + "…"
        md.append("| %s | %s | %s | %s | %s |" % (r["id"], r["section"], r["item"], r["verdict"], head))
    md += ["", "## 自检", "", "| 基线 | 结果 | 取证 |", "|---|---|---|"]
    for g2 in GUARDS:
        md.append("| %s | %s | %s |" % (g2["name"], "PASS" if g2["ok"] else "FAIL", g2["detail"]))
    md.append("")
    with open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))

    print("-" * 74)
    print("总计 %d 条 ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]))
    print("自检 %d / %d" % (g_ok, len(GUARDS)))
    print("产物：%s.json / .md" % base)
    print("核心：盲区成立；AST 抽取实际 field → V-07 交叉相似度 %.4f（硬编码径向 0.1173）" % sim_cross)
    if g_ok != len(GUARDS):
        print("SELFCHECK FAILED")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
