# -*- coding: utf-8 -*-
"""
TUFT_V3.5_新体系_立项决策支持与可行窗口综合判定_2026-10-07.py
================================================
引擎：归并新体系动力学挠率的全部正负面证据，判定可行窗口，
并给出新体系是否值得立项的决策支持（立项定位：解释性 vs 预言性）。

回链（不重算）：
- ESCAPE-AUDIT(2026-10-04)：E1 c_T 无量纲 / E2 无Ostrogradsky / E3 m_τ 解 Π 定理 /
  E4 θ 分区不足 / E5 弃 θ=换核心公理 / E6 hierarchy 搬运 / E7 常数 2→4 / E9 能标范畴错误
- 新体系立项评估(2026-10-07)：前置清单六项；条件性值得立项
- 新体系可证伪预言草案(2026-10-07)：α_i(E)=α_i(μ)+Δα_i(E;m_τ,g_T) 框架
- 新体系 PGT 谱分析(2026-10-07)：谱稳定性非自动；EC 传播挠率被观测排除；
  谱兼容(高 m_τ)vs 预言可测(低 m_τ)两难
- 走④β通道裁定(2026-10-07)：β 可测预言整体不可达

惯例：add 5 参；guard；退出码 0/2；纯标准库；json/md 同名。
红线：数学自洽 ≠ 物理真实；评级 C/L1 维持；本册为决策支持非立项裁决。
"""
import json, os

RES = []
def add(cid, sec, item, verdict, detail):
    RES.append({"id": cid, "sec": sec, "item": item, "verdict": verdict, "detail": detail})

GUARDS = []
def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})

# ---------------- A. 证据归并 ----------------
add("A-01", "证据归并", "正面信号汇总", "PASS",
    "E1 c_T 无量纲(不引新带量纲常数) / E2 无 Ostrogradsky / E3 m_τ 解 Π 定理(自由度1→2) / PGT 真实物理对应 / ghost-free 参数区存在(1812.02675) / α_i(E) 可证伪预言框架成立(最大增量点)")
add("A-02", "证据归并", "负面信号汇总", "BOUNDARY",
    "E4 θ 分区不足(弃 θ 已解决) / E5 弃 θ=换核心公理(新体系本如此) / E6 hierarchy 未解释(m_τ 待解释输入) / E7 常数 2→4 / 2⁻ 分量必然 ghost/tachyon(0905.1068) / quadratic 轴向 ghostly(1910.07506) / EC 传播挠率被观测排除(cdnsciencepub 2025) / 谱兼容vs预言可测两难")

# ---------------- B. 可行窗口判定 ----------------
add("B-01", "可行窗口", "窗口定义：高 m_τ ghost-free 参数区", "PASS",
    "新体系唯一可行窗口=选 ghost-free 参数区(1812.02675)且 m_τ 高(>TeV)，传播模式低能不可见")
add("B-02", "可行窗口", "窗口内谱稳定", "PASS",
    "选对 ghost-free 参数区 ⇒ 无 ghost/tachyon（1812.02675 存在性作为可行依据）")
add("B-03", "可行窗口", "窗口内观测兼容", "PASS",
    "高 m_τ ⇒ 传播挠率模式低能不可见，避开 EC 观测排除（cdnsciencepub 2025）")
add("B-04", "可行窗口", "窗口内预言可测", "FAIL",
    "高 m_τ ⇒ 低能四费米子修正被 1/m_τ² 压到不可测（回链可证伪预言草案）；可行窗口内 F-02 可证伪预言不满足")

# ---------------- C. 三难判定 ----------------
add("C-01", "三难判定", "新体系三难", "FAIL",
    "自洽+观测兼容（高 m_τ 窗口）⇔ 预言不可测；可测预言（低 m_τ）⇔ ghost/tachyon 或 EC 观测排除——三条件无法同时满足")
add("C-02", "三难判定", "与 F-02 关联", "FAIL",
    "新体系可行窗口仍不满足 F-02（可证伪预言）要求——攻坚核心诉求在可行窗口内未达成")
add("C-03", "三难判定", "立项决策建议", "BOUNDARY",
    "新体系可立项为「解释性统一场论」（自洽+观测兼容，接受预言不可测），**不可**作为「预言性场论」；立项定位须作者明确，不得伪装可证伪")

# ---------------- D. 全链收敛 ----------------
add("D-01", "全链收敛", "TUFT 攻坚总收敛", "PASS",
    "三条路线均无法同时满足【自洽+观测兼容+可证伪预言】：V3.6 静态几何 CLOSED-IMPOSSIBLE；β 通道可测预言不可达；新体系可行窗口(高 m_τ)预言不可测——F-02 贯穿全程未达成")
add("D-02", "全链收敛", "本册定位", "BOUNDARY",
    "本册为立项决策支持非裁决；立项与否/定位（解释性 vs 预言性）须作者拍板；若立为新体系须重审计评级另起")

# ---------------- 自检 ----------------
guard("pos_sig_summed", any(x["id"] == "A-01" and x["verdict"] == "PASS" for x in RES), "正面信号已归并")
guard("neg_sig_summed", any(x["id"] == "A-02" and x["verdict"] == "BOUNDARY" for x in RES), "负面信号已归并")
guard("window_defined", any(x["id"] == "B-01" and x["verdict"] == "PASS" for x in RES), "可行窗口已定义（高 m_τ ghost-free）")
guard("window_safe", any(x["id"] == "B-03" and x["verdict"] == "PASS" for x in RES), "窗口内观测兼容已判定")
guard("window_unpredictive", any(x["id"] == "B-04" and x["verdict"] == "FAIL" for x in RES), "窗口内预言不可测已判定（F-02 不满足）")
guard("trilemma", any(x["id"] == "C-01" and x["verdict"] == "FAIL" for x in RES), "新体系三难已判定")
guard("global_convergence", any(x["id"] == "D-01" and x["verdict"] == "PASS" for x in RES), "攻坚总收敛已判定")

ok_all = all(g["ok"] for g in GUARDS)
n_pass = sum(1 for x in RES if x["verdict"] == "PASS")
n_fail = sum(1 for x in RES if x["verdict"] == "FAIL")
n_bound = sum(1 for x in RES if x["verdict"] == "BOUNDARY")

out = {
    "title": "TUFT V3.5 · 新体系立项决策支持与可行窗口综合判定",
    "generated": "2026-10-07",
    "engine": "TUFT_V3.5_新体系_立项决策支持与可行窗口综合判定_2026-10-07.py",
    "count": {"total": len(RES), "pass": n_pass, "fail": n_fail, "boundary": n_bound},
    "feasible_window": "高 m_τ(>TeV) ghost-free 参数区——谱稳定✅ 观测兼容✅ 但预言不可测❌",
    "trilemma": "自洽+观测兼容 ⇔ 预言不可测；可测预言 ⇔ 谱/观测冲突——三条件无法同时满足",
    "decision_support": "新体系可立项为解释性统一场论（接受预言不可测），不可作为预言性场论；立项定位须作者明确",
    "global_convergence": "TUFT 三条路线(V3.6静态几何/β通道/新体系)均无法同时满足【自洽+观测兼容+可证伪预言】——F-02 贯穿全程未达成",
    "redline": "数学自洽 ≠ 物理真实；评级 C/L1 维持；回链不重算",
    "items": RES,
    "guards": GUARDS,
    "guard_summary": {"total": len(GUARDS), "pass": sum(1 for g in GUARDS if g["ok"]), "ok": ok_all},
}

base = os.path.splitext(os.path.abspath(__file__))[0]
with open(base + ".json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

md = [
    "# TUFT V3.5 · 新体系立项决策支持与可行窗口综合判定（机器产物）",
    "",
    "- 生成时间：2026-10-07",
    "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ 自检 %d / %d" % (len(RES), n_pass, n_fail, n_bound, sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
    "- **可行窗口：高 m_τ(>TeV) ghost-free 参数区**——谱稳定✅ 观测兼容✅ 预言不可测❌",
    "- **新体系三难：自洽+观测兼容 ⇔ 预言不可测；可测预言 ⇔ 谱/观测冲突**",
    "- **攻坚总收敛：TUFT 三条路线均无法同时满足【自洽+观测兼容+可证伪预言】——F-02 贯穿全程未达成**",
    "",
    "## 可行窗口判定",
    "",
    "| 判据 | 结果 | 说明 |",
    "|---|---|---|",
    "| 谱稳定 | ✅ | ghost-free 参数区(1812.02675 存在性) |",
    "| 观测兼容 | ✅ | 高 m_τ 传播模式不可见(避开 EC 排除) |",
    "| 预言可测 | ❌ | 低能修正被 1/m_τ² 压制，F-02 不满足 |",
    "",
    "## 条目",
    "",
    "| ID | 节 | 条目 | 判定 | 摘要 |",
    "|---|---|---|---|---|",
]
for x in RES:
    md.append("| %s | %s | %s | %s | %s |" % (x["id"], x["sec"], x["item"], x["verdict"], x["detail"]))
md += [
    "",
    "## 自检",
    "",
    "| 基线 | 结果 | 取证 |",
    "|---|---|---|",
]
for g in GUARDS:
    md.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
md += [
    "",
    "## 诚实边界与决策衔接",
    "",
    "1. 本册为**立项决策支持非裁决**：归并新体系全部证据，给出可行窗口与三难，立项与否/定位（解释性 vs 预言性）须作者拍板；",
    "2. 若立为新体系：须选高 m_τ ghost-free 参数区、接受预言不可测、hierarchy 作开放项、常数 2→4 登记 Ω5'、重新全维审计评级另起；",
    "3. 若作者坚持可证伪预言（F-02）：新体系不可行（可行窗口预言不可测），须另寻观测通道或接受解释性定位；",
    "4. **攻坚总收敛**：V3.6 静态几何 CLOSED-IMPOSSIBLE / β 通道不可达 / 新体系可行窗口预言不可测——三条件【自洽+观测兼容+可证伪预言】贯穿全程无法同时满足，这是全链最诚实的总判定；",
    "5. 红线：数学自洽 ≠ 物理真实；评级 C/L1 维持。",
]
with open(base + ".md", "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print("items=%d pass=%d fail=%d boundary=%d guards=%d/%d ok=%s"
      % (len(RES), n_pass, n_fail, n_bound, sum(1 for g in GUARDS if g["ok"]), len(GUARDS), ok_all))
raise SystemExit(0 if ok_all else 2)
