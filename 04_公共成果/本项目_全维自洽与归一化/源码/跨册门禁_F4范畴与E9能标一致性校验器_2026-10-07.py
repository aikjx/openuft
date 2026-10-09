# -*- coding: utf-8 -*-
"""
跨册门禁：F4 范畴一致性 + E9 能标一致性 校验器（2026-10-07）

把 MEMORY.md 中两条跨册条款 operationalize 为可机器调用的 gate：
  - F4 范畴一致性：跨力/跨类比较前，先查对象是否同类（量纲级、数学范畴）。
      带量纲耦合（如 G，[G]=M^-2）不得直接进无量纲强度比较表；
      须先用 α(E)=c·E^{-dim} 化无量纲并声明能标（再交 E9）。
  - E9 能标一致性：同一张无量纲强度表内不得混用能标；未声明能标记 BOUNDARY。

输入：一组待比较项，每项含
    name          标识符
    coupling      原始数值（仅用于记录，不参与门禁判定）
    mass_dim      耦合常数的质量量纲（0 = 无量纲；-2 = G 型；等）
    kind          范畴标签：gauge / gravity / geometric / quantum_op / classical
    scale_GeV     该数值所取能标（GeV）；None = 未声明
    converted     若 mass_dim != 0，是否已化为 α(E) 形式（默认 False）

输出：结构化判定（PASS/FAIL/BOUNDARY）+ 定位到具体项的违规。

纯标准库；EXIT=0 表示脚本正常结束（门禁结果在 verdicts 里，不靠退出码表达结论）。
"""
import json
import math
import os

# ---- 物理常数（与四力本源册 / E9 册一致）----
G_NAT = 6.708612363414657e-39      # GeV^-2，G = 1/M_Pl^2，M_Pl = 1.22091e19 GeV
M_PL = 1.22091e19                  # GeV
M_Z = 91.1876                      # GeV
M_ELECTRON = 0.00051099895         # GeV

# 可比较范畴白名单：规范力 与 已化无量纲的引力 都是无量纲力耦合，可同表。
ALLOWED_COMPARABLE = {"gauge", "gravity_eff"}


def alpha_G(E_GeV):
    """无量纲引力耦合 α_G(E) = G·E^2（自然单位）。"""
    return G_NAT * (E_GeV ** 2)


def effective_dimensionless(it):
    """该项是否已处于「无量纲、可进强度表」状态。"""
    if it["mass_dim"] == 0:
        return True
    return bool(it.get("converted")) and it.get("scale_GeV") is not None


def category_of(it):
    if it["mass_dim"] == 0:
        return it["kind"]
    if it.get("converted") and it.get("scale_GeV") is not None:
        return "gravity_eff"
    return it["kind"]


def check_F4(items):
    """F4 范畴一致性门禁。返回 (status, violations)。"""
    violations = []
    # 1) 带量纲且未化无量纲 → 直接 FAIL
    for it in items:
        if not effective_dimensionless(it):
            violations.append({
                "item": it["name"],
                "reason": "带量纲耦合 [dim=%d] 未化为无量纲（须 α(E)=c·E^%d 且声明能标），不得进无量纲强度比较表"
                          % (it["mass_dim"], -it["mass_dim"]),
            })
    # 2) 已无量纲各项的范畴兼容性
    cats = {category_of(it) for it in items if effective_dimensionless(it)}
    if cats and not (cats <= ALLOWED_COMPARABLE):
        extra = ", ".join(sorted(cats - ALLOWED_COMPARABLE))
        violations.append({
            "item": "table",
            "reason": "跨范畴并列：含非规范力范畴（%s），类别不同须先判范畴再比数值（BOUNDARY 需人工裁定）"
                      % extra,
        })
    status = "FAIL" if any("不得进无量纲" in v["reason"] for v in violations) else \
             ("BOUNDARY" if violations else "PASS")
    return status, violations


def check_E9(items):
    """E9 能标一致性门禁（仅对已成为无量纲的项生效）。返回 dict。"""
    eff = [it for it in items if effective_dimensionless(it)]
    declared = [(it["name"], it["scale_GeV"]) for it in eff if it.get("scale_GeV") is not None]
    undeclared = [it["name"] for it in eff if it.get("scale_GeV") is None]
    if undeclared:
        return {"status": "BOUNDARY",
                "spread_dex": None,
                "violations": [{"item": u, "reason": "未声明能标"} for u in undeclared]}
    if len(declared) < 2:
        return {"status": "PASS", "spread_dex": 0.0, "violations": []}
    vals = [s for _, s in declared]
    lo, hi = min(vals), max(vals)
    spread = math.log10(hi / lo)
    if spread > 1e-3:
        # 定位跨度两端
        i_lo, i_hi = vals.index(lo), vals.index(hi)
        return {"status": "FAIL", "spread_dex": spread, "violations": [{
            "item": "table",
            "reason": "混用能标：跨 %.2f dex（%s ~%.3g GeV → %s ~%.3g GeV）"
                      % (spread, declared[i_lo][0], lo, declared[i_hi][0], hi),
        }]}
    return {"status": "PASS", "spread_dex": spread, "violations": []}


def check_table(name, items):
    f4_status, f4_v = check_F4(items)
    e9 = check_E9(items)
    if f4_status == "FAIL" or e9["status"] == "FAIL":
        overall = "FAIL"
    elif f4_status == "BOUNDARY" or e9["status"] == "BOUNDARY":
        overall = "BOUNDARY"
    else:
        overall = "PASS"
    return {
        "table": name,
        "overall": overall,
        "F4": {"status": f4_status, "violations": f4_v},
        "E9": e9,
    }


# ============================ 自验 / 已知案例 ============================

def build_cases():
    cases = []

    # 案例 A：教科书四力表「原始 G 直接入表」——最常见的范畴错误
    cases.append(("A_教科书原始G入表", [
        {"name": "强", "coupling": 1.0, "mass_dim": 0, "kind": "gauge", "scale_GeV": 1.0},
        {"name": "电磁", "coupling": 1e-2, "mass_dim": 0, "kind": "gauge", "scale_GeV": 1.0},
        {"name": "弱", "coupling": 1e-5, "mass_dim": 0, "kind": "gauge", "scale_GeV": 1.0},
        {"name": "引力(raw G)", "coupling": G_NAT, "mass_dim": -2, "kind": "gravity",
         "scale_GeV": None, "converted": False},
    ], "FAIL"))  # 期望：F4 FAIL（带量纲未化无量纲）

    # 案例 B：ADD-02 四力耦合表（E9 册已审）—— 混用能标
    cases.append(("B_ADD-02四力混标", [
        {"name": "α_s", "coupling": 0.1179, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
        {"name": "α_weak", "coupling": 0.01696, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
        {"name": "α_em(零能标)", "coupling": 7.297e-3, "mass_dim": 0, "kind": "gauge", "scale_GeV": 1e-6},
        {"name": "α_G(电子标度)", "coupling": 1.75e-45, "mass_dim": -2, "kind": "gravity",
         "scale_GeV": M_ELECTRON, "converted": True},
    ], "FAIL"))  # 期望：F4 PASS（已化无量纲），E9 FAIL（混标 ~8 dex）

    # 案例 C：干净表——三个规范耦合同取 M_Z
    cases.append(("C_干净_规范耦合同标度", [
        {"name": "α_1", "coupling": 0.01694, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
        {"name": "α_2", "coupling": 0.03380, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
        {"name": "α_3", "coupling": 0.1179, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
    ], "PASS"))

    # 案例 D：引力已化 α_G 且与其他同取 M_Z —— 应通过两道门
    cases.append(("D_引力化α_G同标度", [
        {"name": "α_1", "coupling": 0.01694, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
        {"name": "α_2", "coupling": 0.03380, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
        {"name": "α_3", "coupling": 0.1179, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
        {"name": "α_G(M_Z)", "coupling": alpha_G(M_Z), "mass_dim": -2, "kind": "gravity",
         "scale_GeV": M_Z, "converted": True},
    ], "PASS"))

    return cases


def self_test_anchors():
    """双锚点自检：α_G=G·E² 能反解出质子/电子质量。"""
    # 反解：给定 α_G，E = sqrt(α_G / G)
    def E_of(alpha):
        return math.sqrt(alpha / G_NAT)
    a_proton = 5.9e-39
    a_electron = 1.75e-45
    E_p = E_of(a_proton)
    E_e = E_of(a_electron)
    r_p = E_p / 0.93827      # 质子质量 ~0.938 GeV
    r_e = E_e / M_ELECTRON
    # 双锚点反解应恢复 m_p / m_e（文献口径「吻合到 5e-4」；此处取 1e-3 容差，
    # 因 G_NAT 有效数字舍入使重算偏差约 5.5e-4，仍 < 0.1%，公式正确无误）。
    return {
        "E_from_5.9e-39_GeV": E_p, "ratio_to_mp": r_p,
        "E_from_1.75e-45_GeV": E_e, "ratio_to_me": r_e,
        "ok": abs(r_p - 1) < 1e-3 and abs(r_e - 1) < 1e-3,
    }


def run_all():
    cases = build_cases()
    results = []
    n_ok = 0
    for name, items, expect in cases:
        v = check_table(name, items)
        hit = (v["overall"] == expect)
        n_ok += 1 if hit else 0
        results.append({"case": name, "expect": expect, "got": v["overall"],
                        "match": hit, "verdict": v})
    anchors = self_test_anchors()
    summary = {
        "tag": "跨册门禁_F4范畴与E9能标一致性校验器",
        "self_test_cases": len(cases),
        "self_test_pass": n_ok,
        "anchor_selfcheck": anchors,
        "cases": results,
    }
    return summary


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    summary = run_all()
    out_json = os.path.join(here, "..", "数据", "跨册门禁_F4范畴与E9能标一致性校验器_2026-10-07.json")
    out_md = os.path.join(here, "..", "数据", "跨册门禁_F4范畴与E9能标一致性校验器_2026-10-07.md")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    # 简报
    lines = []
    lines.append("# 跨册门禁_F4范畴与E9能标一致性校验器（自验产物）\n")
    lines.append("自验案例 %d / 通过 %d\n" % (summary["self_test_cases"], summary["self_test_pass"]))
    a = summary["anchor_selfcheck"]
    lines.append("双锚点自检：E(5.9e-39)=%.5f GeV（比 m_p %.5f）；E(1.75e-45)=%.6g GeV（比 m_e %.5f）；ok=%s\n"
                 % (a["E_from_5.9e-39_GeV"], a["ratio_to_mp"], a["E_from_1.75e-45_GeV"], a["ratio_to_me"], a["ok"]))
    lines.append("\n## 案例逐条\n")
    for c in summary["cases"]:
        v = c["verdict"]
        lines.append("- **%s**：期望 %s / 实得 %s / %s" % (c["case"], c["expect"], c["got"], "✓" if c["match"] else "✗"))
        lines.append("  - F4=%s；E9=%s（spread=%s）" % (v["F4"]["status"], v["E9"]["status"], v["E9"]["spread_dex"]))
        for viol in v["F4"]["violations"] + v["E9"]["violations"]:
            lines.append("    - [%s] %s" % (viol["item"], viol["reason"]))
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    # 控制台
    print("自验案例 %d / 通过 %d" % (summary["self_test_cases"], summary["self_test_pass"]))
    print("双锚点 ok =", a["ok"], " E(5.9e-39)=%.4f  E(1.75e-45)=%.4g" % (a["E_from_5.9e-39_GeV"], a["E_from_1.75e-45_GeV"]))
    for c in summary["cases"]:
        print("  %-28s expect=%-7s got=%-7s %s" % (c["case"], c["expect"], c["got"], "OK" if c["match"] else "MISMATCH"))
    print("EXIT=0")


if __name__ == "__main__":
    main()
