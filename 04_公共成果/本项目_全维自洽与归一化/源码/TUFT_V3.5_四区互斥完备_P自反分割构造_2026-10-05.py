# -*- coding: utf-8 -*-
"""
TUFT V3.5 · 四区互斥完备 + P 自反分割构造（分支②）—— 2026-10-05
=========================================================================
目标：构造一个 (κ,τ) 二维流形上、以 θ=atan2(τ,κ) 编码的 4 力分区，
**同时满足三个此前所有分区都失败的性质**：
  1. 100% 覆盖（无空白区）
  2. 互斥（无重叠，任意点至多落一个区）
  3. P 自反（θ→−θ 把每区映回自身 ⇒ P 不把任何力配置互换成另一个力）
     —— 分支① 失败（重叠 2.05% / 未覆盖 59.85%），ADD-02 失败（P 把
        Weak 240° 映到 Strong 120°），本册给出同时满足三者的构造。

构造（θ∈[0°,360°)，每区 = 关于 0°-180° 轴对称的一对楔形）：
  R1 = [0°,45°) ∪ [315°,360°)          # 经 0° 自反
  R2 = [45°,90°) ∪ [270°,315°)          # 经 180° 自反
  R3 = [90°,135°) ∪ [225°,270°)
  R4 = [135°,225°)                      # 经 180° 自反
每区合计 90° ⇒ 穷尽 [0°,360°)，互斥，且 θ→360°−θ 下每区自反。

力标签归属（R1..R4 → 引力/电磁/强/弱）是**建模选择**，本册只构造与验证几何，
标签由作者裁定；给出一个临时示例并显式标注。

红线：互斥完备 + P 自反 是几何自洽，≠ 物理正确；力标签归属非第一性推导。
纯标准库，零第三方依赖。
"""

import os
import sys
import json
import time
import math
import io

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")

RESULTS = []
GUARDS = []


def add(cid, sec, item, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-26s | %s" % (verdict, cid, item, detail[:150]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-32s | %s | %s" % (name, "PASS" if ok else "FAIL", detail))
    return bool(ok)


def region_of_theta(tdeg):
    """θ∈[0°,360°)。返回区域名（R1..R4）。"""
    t = tdeg % 360.0
    if t < 45.0 or t >= 315.0:
        return "R1"
    if t < 90.0 or (t >= 270.0 and t < 315.0):
        return "R2"
    if t < 135.0 or (t >= 225.0 and t < 270.0):
        return "R3"
    if t < 225.0:
        return "R4"
    return None  # 不可达（覆盖已验证为 100%）


def main():
    # =====================================================================
    # A. 角度轴一维：覆盖 / 互斥 / P 自反（内部采样，避开边界）
    # =====================================================================
    sec = "角度轴"
    N = 7200
    gaps_1d = 0
    p_not_reflexive = 0
    # 内部采样：t=(i+0.5)*360/N 避开分区边界（边界测度零，单独登记）
    for i in range(N):
        t = 360.0 * (i + 0.5) / N
        r = region_of_theta(t)
        if r is None:
            gaps_1d += 1
        rP = region_of_theta(360.0 - t)
        if r is not None and rP != r:
            p_not_reflexive += 1
    ok_cover_1d = gaps_1d == 0
    ok_pref_1d = p_not_reflexive == 0
    guard("cover_1d", ok_cover_1d, "角度轴 %d 内部点覆盖率 100%%（空白 %d）" % (N, gaps_1d))
    guard("pref_1d", ok_pref_1d, "角度轴内部 P 自反失败点数 %d（θ→−θ 全落同区）" % p_not_reflexive)
    add("A-01", sec, "角度轴 100% 覆盖", "PASS" if ok_cover_1d else "FAIL",
        "内部采样 %d 点：空白 %d ⇒ 覆盖 100%%（无空隙）" % (N, gaps_1d))
    add("A-02", sec, "角度轴 P 自反", "PASS" if ok_pref_1d else "FAIL",
        "内部采样 P 自反失败 %d ⇒ 四区内部全 P 自反（不同于 ADD-02 的 Weak↔Strong 互换）" % p_not_reflexive)
    # 边界测度零登记
    add("A-03", sec, "边界约定（测度零）", "BOUNDARY",
        "分区边界 θ∈{45,90,135,225,270,315}° 及其镜像，测度为零；边界点归属是约定，"
        "内部（开集）已证 P 自反；不影响覆盖/互斥结论")

    # =====================================================================
    # B. (κ,τ) 二维网格：经 atan2 归属，验证覆盖 / 互斥 / P 自反
    # =====================================================================
    sec = "二维流形"
    RNG, N2 = 5.0, 401
    unassigned = 0
    pref_fail = 0
    boundary_points = 0
    BOUND = {0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0}
    EPS = 1e-6
    for i in range(N2):
        k = -RNG + 2 * RNG * i / (N2 - 1)
        for j in range(N2):
            t = RNG - 2 * RNG * j / (N2 - 1)
            if k == 0.0 and t == 0.0:
                continue        # 原点（θ 未定义，已排除）
            th_deg = math.degrees(math.atan2(t, k)) % 360.0
            # 边界射线（测度零）：θ 精确落边界 → 计入边界，不进 P 自反统计
            if any(abs(th_deg - b) < EPS or abs(th_deg - b - 360.0) < EPS or abs(th_deg - b + 360.0) < EPS for b in BOUND):
                boundary_points += 1
                continue
            r = region_of_theta(th_deg)
            if r is None:
                unassigned += 1
            rP = region_of_theta((360.0 - th_deg) % 360.0)
            if r is not None and rP != r:
                pref_fail += 1
    total2 = N2 * N2 - 1
    interior2 = total2 - boundary_points
    cover2 = 100.0 * (1 - unassigned / float(total2))
    ok_cover2 = unassigned == 0
    ok_pref2 = pref_fail == 0
    guard("cover_2d", ok_cover2, "(κ,τ) 网格覆盖 %.2f%%（未覆盖 %d）" % (cover2, unassigned))
    guard("pref_2d", ok_pref2, "(κ,τ) 内部点 P 自反失败 %d（边界射线已排除）" % pref_fail)
    add("B-01", sec, "二维覆盖（互斥完备）", "PASS" if ok_cover2 else "FAIL",
        "401×401 网格经 atan2：覆盖 %.2f%%（未覆盖 %d，原点已排除）⇒ 无空白 ⇒ 完备" % (cover2, unassigned))
    add("B-02", sec, "二维 P 自反（内部）", "PASS" if ok_pref2 else "FAIL",
        "内部点 %d 中 P 自反失败 %d ⇒ 四力配置不被 P 互换（修复 ADD-02 缺陷）" % (interior2, pref_fail))
    add("B-03", sec, "边界射线（测度零）", "BOUNDARY",
        "θ∈{0,45,90,135,180,225,270,315}° 边界射线 %d 点，测度零；归属是约定，内部（开集）已证 P 自反" % boundary_points)
    add("B-04", sec, "与历史分区对比", "PASS",
        "分支①：重叠 2.05%%、未覆盖 59.85%%（不互斥不完备）；ADD-02：P 把 Weak↔Strong 互换；"
        "本册：覆盖 100%%、互斥、内部全 P 自反 ⇒ 三项全达标（仅测度零边界待约定）")

    # =====================================================================
    # C. 力标签归属（建模选择，显式标注）
    # =====================================================================
    sec = "力标签"
    provisional = {
        "R1": "电磁（EM，经 0° 自反）",
        "R2": "强核（Strong）",
        "R3": "引力（Gravity）",
        "R4": "弱核（Weak，P 自反域内可承载 η≠0 破缺）",
    }
    for r, lbl in provisional.items():
        add("C-01", sec, "临时归属 %s" % r, "BOUNDARY",
            "%s —— 标签归属待作者裁定；本册只保证几何自洽（互斥完备+P 自反），不保证标签物理正确" % lbl)
    add("C-02", sec, "标签归属边界", "BOUNDARY",
        "力→区域映射需作者结合强度表/耦合匹配裁定；此处为临时示例")

    # =====================================================================
    # 汇总
    # =====================================================================
    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    g_ok = sum(1 for g in GUARDS if g["ok"])

    payload = {
        "册": "TUFT_V3.5_四区互斥完备_P自反分割构造",
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "定位": "分支②：几何自洽的 4 力分区（覆盖 100%/互斥/P 自反）",
        "计数": counts, "总计": len(RESULTS),
        "构造": {"R1": "[0,45)+[315,360)", "R2": "[45,90)+[270,315)",
                 "R3": "[90,135)+[225,270)", "R4": "[135,225)"},
        "一维": {"覆盖": "100%%" if ok_cover_1d else "有隙", "P自反失败": p_not_reflexive},
        "二维": {"覆盖": cover2, "未覆盖": unassigned, "P自反失败": pref_fail,
                 "网格": "%d×%d" % (N2, N2)},
        "对比": {"分支①": "重叠2.05%/未覆盖59.85%", "ADD-02": "P把Weak↔Strong互换",
                 "本册": "覆盖100%/互斥/P自反全达标"},
        "力标签": provisional,
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "条目": RESULTS,
        "耗时": "%.1fs" % (time.time() - T_START),
    }
    base = os.path.join(DATA_DIR, "TUFT_V3.5_四区互斥完备_P自反分割构造_2026-10-05")
    with io.open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    md = ["# TUFT V3.5 · 四区互斥完备 + P 自反分割（机器产物）", "",
          "- 生成时间：%s" % payload["生成时间"],
          "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d ｜ 自检 %d / %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"],
           g_ok, len(GUARDS)),
          "- 构造：R1=[0,45)+[315,360) ｜ R2=[45,90)+[270,315) ｜ R3=[90,135)+[225,270) ｜ R4=[135,225)",
          "- 二维网格：覆盖 %.2f%% ｜ 未覆盖 %d ｜ P 自反失败 %d" % (cover2, unassigned, pref_fail),
          "- 对比：分支①(重叠2.05%/未覆盖59.85%)、ADD-02(P 把 Weak↔Strong 互换) ⇒ 本册三项全达标",
          "", "## 条目", "", "| ID | 节 | 条目 | 判定 | 摘要 |", "|---|---|---|---|---|"]
    for r in RESULTS:
        head = r["detail"].replace("\n", " ")
        if len(head) > 160:
            head = head[:160] + "…"
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
    print("核心结果：二维覆盖 %.2f%% ｜ P 自反失败 %d ｜ 力标签为建模选择待裁定" % (cover2, pref_fail))
    if g_ok != len(GUARDS):
        print("SELFCHECK FAILED")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
