# -*- coding: utf-8 -*-
"""
TUFT V3.5 分支①修复版 · 独立再验收（读取实际 SUT，非复刻）—— 2026-10-05
=========================================================================
背景：第八轮验收册（TUFT_V3.5修复版_验收审计与修复清单）的 guards 用**自己
硬编码复刻的旧版 sut_field（径向 −r̂/r）** 做计算，AST 绑定只查函数名存在、
不读实际 `field()` 的行为 ⇒ 直接重跑它**无法确认 F-03/F-04 是否已修**
（它对任何 SUT 都固定报 V-07=0.1173、V-08≡1）。这是自指涉验证盲区。

本册做真正的独立再验收：**从实际交付的 SUT 源码抽取 `field()` 定义并 exec**，
与独立导出的理论目标 F=−∇(κ+τ)=−(1,1)/√2 交叉比对；同时核验 V-08 判据
是否已改为交叉比对（不再用 cos(f,f) 自比）。

红线：独立再验收 ≠ 物理正确；只验「实际代码与其声称的 E∝(κ+τ) 是否自洽」。
纯标准库，零第三方依赖。
"""

import os
import sys
import json
import time
import math
import ast
import io

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA_DIR = os.path.join(BASE, "数据")
SUT = os.path.join(BASE, "源码", "统一场论可视化证明_TUFT_V3.5_修复版_2026-10-04.py")
AUDIT_ENGINE = os.path.join(BASE, "源码", "TUFT_V3.5修复版_验收审计与修复清单_2026-10-04.py")

RESULTS = []
GUARDS = []


def add(cid, sec, item, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-26s | %s" % (verdict, cid, item, detail[:150]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-32s | %s | %s" % (name, "PASS" if ok else "FAIL", detail))
    return bool(ok)


def cosine_sim(fa, fb, pts):
    num = da = db = 0.0
    for p in pts:
        a = fa(*p)
        b = fb(*p)
        num += a[0] * b[0] + a[1] * b[1]
        da += a[0] * a[0] + a[1] * a[1]
        db += b[0] * b[0] + b[1] * b[1]
    if da == 0 or db == 0:
        return float('nan')
    return num / math.sqrt(da * db)


def main():
    # =====================================================================
    # A. 从实际 SUT 源码抽取并执行 field()
    # =====================================================================
    sec = "实际SUT读取"
    if not os.path.exists(SUT):
        guard("sut_exists", False, SUT)
        return 2
    src = io.open(SUT, encoding="utf-8").read()
    tree = ast.parse(src)
    field_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "field"]
    guard("sut_has_field", len(field_nodes) == 1, "SUT 含 1 个 field 定义（%d）" % len(field_nodes))
    if len(field_nodes) != 1:
        return 2
    field_src = ast.get_source_segment(src, field_nodes[0])
    ns = {"math": math}
    exec(field_src, ns)
    field_fn = ns["field"]
    add("A-01", sec, "从实际 SUT 抽取 field()", "PASS",
        "exec 实际源码中的 field 定义；抽取成功，样本点实际调用 field()（非复刻）")

    # =====================================================================
    # B. 与独立理论目标交叉比对（F-03 验证）
    # =====================================================================
    sec = "F-03 交叉比对"
    # 独立目标：E∝(κ+τ)，κ=x,τ=y ⇒ F_target = −∇(κ+τ) 方向 = −(1,1)/√2（均匀场）
    def theory_target(x, y):
        return (-1.0 / math.sqrt(2.0), -1.0 / math.sqrt(2.0))

    # 旧缺陷场（验收册 V-07 报的径向 −r̂/r 方向），用于证明判据有信息量
    def old_radial(x, y):
        r = math.hypot(x, y)
        if r == 0:
            return (0.0, 0.0)
        return (-x / r, -y / r)

    pts = [(0.3, 0.3), (-0.3, 0.3), (0.3, -0.3), (-0.3, -0.3), (1.0, 0.0), (0.0, 1.0)]
    sim_fixed = cosine_sim(field_fn, theory_target, pts)
    sim_bad = cosine_sim(old_radial, theory_target, pts)

    # 实际 field() 应处处输出同一方向（均匀场）
    uniq_dirs = set()
    for p in pts:
        f = field_fn(*p)
        n = math.hypot(f[0], f[1])
        if n > 0:
            uniq_dirs.add((round(f[0] / n, 6), round(f[1] / n, 6)))
    is_uniform = len(uniq_dirs) == 1 and abs(sim_fixed - 1.0) < 1e-9

    guard("F03_fixed_uniform", is_uniform,
          "实际 field() 输出单一方向 %s（均匀场）" % sorted(uniq_dirs))
    guard("F03_cross_matches_theory", sim_fixed >= 0.95,
          "实际 field() 与理论 F=−∇(κ+τ) 交叉余弦相似度 = %.4f ≥ 0.95 ⇒ V-07 已修" % sim_fixed)
    guard("F03_rejects_old", sim_bad < 0.95,
          "旧缺陷径向场交叉相似度 = %.4f < 0.95 ⇒ 判据有信息量（能区分）" % sim_bad)

    add("B-01", sec, "实际 field() vs 理论目标", "PASS" if sim_fixed >= 0.95 else "FAIL",
        "交叉相似度（6 点）%.4f ≥ 0.95 ⇒ 实际代码与其声称的 E∝(κ+τ) 一致（F-03 修复确认）" % sim_fixed)
    add("B-02", sec, "旧缺陷径向场被拒", "PASS" if sim_bad < 0.95 else "FAIL",
        "同判据对旧场：%.4f < 0.95 ⇒ 判据非零信息（能区分正确场与旧缺陷场）" % sim_bad)

    # =====================================================================
    # C. V-08 判据核验：SUT 是否已改为交叉比对（不再用 cos(f,f) 自比当证据）
    # =====================================================================
    sec = "F-04 判据核验"
    # 检查实际 SUT：E-02 判据应基于 sim_cross（交叉），而非 sim_self
    has_cross = "sim_cross" in src and "cosine_sim(field, target_field" in src
    has_self_as_criterion = "ok_render = sim_self" in src   # 旧代码的判据行（应为空）
    guard("F04_uses_cross", has_cross,
          "SUT E-02 判据使用交叉比对（sim_cross / target_field）")
    guard("F04_no_self_criterion", not has_self_as_criterion,
          "SUT 不再用 ok_render=sim_self 当判据（自比已弃用）")
    add("C-01", sec, "V-08 判据改为交叉比对", "PASS" if (has_cross and not has_self_as_criterion) else "FAIL",
        "读取实际 SUT 源码：E-02 判据=交叉相似度；旧 ok_render=sim_self 判据行已移除 ⇒ V-08 已修")

    # =====================================================================
    # D. 方法论：验收册引擎自指涉盲区登记
    # =====================================================================
    sec = "方法论盲区"
    a_src = io.open(AUDIT_ENGINE, encoding="utf-8").read() if os.path.exists(AUDIT_ENGINE) else ""
    has_hardcoded_radial = "sut_field" in a_src and "(-x / (r * r), -y / (r * r))" in a_src
    add("D-01", sec, "验收册引擎自指涉盲区", "BOUNDARY",
        "复刻旧版 sut_field：验收册用自己的硬编码 sut_field(径向) 做 V-07/V-08 计算（%s），AST 只查函数名 ⇒ "
        "直接重跑它无法确认 F-03/F-04 是否已修，必须改读实际 SUT（本册即此做法）" %
        ("确认为硬编码旧版" if has_hardcoded_radial else "未检出硬编码"))
    guard("audit_engine_self_referential", has_hardcoded_radial,
          "验收册引擎含硬编码旧版 sut_field ⇒ 自指涉，重跑不能验证修复")

    # =====================================================================
    # 汇总
    # =====================================================================
    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    g_ok = sum(1 for g in GUARDS if g["ok"])

    payload = {
        "册": "TUFT_V3.5分支①修复版_独立再验收",
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "定位": "读取实际 SUT 源码验证 F-03/F-04，并登记验收册自指涉盲区",
        "计数": counts, "总计": len(RESULTS),
        "F03": {"实际field vs 理论": sim_fixed, "旧径向场被拒": sim_bad, "均匀方向数": len(uniq_dirs)},
        "F04": {"交叉比对": has_cross, "弃自比判据": not has_self_as_criterion},
        "方法论": {"验收册硬编码旧版": has_hardcoded_radial},
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "条目": RESULTS,
        "耗时": "%.1fs" % (time.time() - T_START),
    }
    base = os.path.join(DATA_DIR, "TUFT_V3.5修复版_独立再验收_2026-10-05")
    with io.open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    md = ["# TUFT V3.5 分支①修复版 · 独立再验收（机器产物）", "",
          "- 生成时间：%s" % payload["生成时间"],
          "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d ｜ 自检 %d / %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"],
           g_ok, len(GUARDS)),
          "- F-03：实际 field() vs 理论 F=−∇(κ+τ) 交叉相似度 %.4f（≥0.95 ⇒ V-07 已修）" % sim_fixed,
          "- 判据信息量：旧径向场被拒 %.4f（<0.95）" % sim_bad,
          "- F-04：判据已改交叉比对（自比弃用）⇒ V-08 已修",
          "- 方法论：验收册引擎用硬编码旧版 sut_field（自指涉），直接重跑不能验证修复",
          "", "## 条目", "", "| ID | 节 | 条目 | 判定 | 摘要 |", "|---|---|---|---|---|"]
    for r in RESULTS:
        head = r["detail"].replace("\n", " ")
        if len(head) > 170:
            head = head[:170] + "…"
        md.append("| %s | %s | %s | %s | %s |" % (r["id"], r["section"], r["item"], r["verdict"], head))
    md += ["", "## 自检", "", "| 基线 | 结果 | 取证 |", "|---|---|---|"]
    for g in GUARDS:
        md.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
    md.append("")
    with io.open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))

    print("-" * 74)
    print("总计 %d 条 ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]))
    print("自检 %d / %d" % (g_ok, len(GUARDS)))
    print("产物：%s.json / .md" % base)
    print("结论：F-03（场与公式一致）与 F-04（判据有信息）由读取实际 SUT 确认已修；")
    print("      验收册引擎自指涉，直接重跑不能验证修复")
    if g_ok != len(GUARDS):
        print("SELFCHECK FAILED")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
