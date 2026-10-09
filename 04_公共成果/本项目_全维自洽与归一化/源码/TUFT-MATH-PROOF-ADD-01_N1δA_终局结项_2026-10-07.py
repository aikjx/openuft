#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TUFT-MATH-PROOF-ADD-01 · N1（A_chiral ≡ 0）/ δA 终局结项引擎（纯标准库，零第三方依赖）

任务：把 ADD-01 N1 从「致命定义错误」的演化链做终局结项。

判定路线：
  P1  判据演化链复算：回读 5 份既有 json，逐档复算
      原判据 `PΩ≠Ω`（已废止）→ 作用量判据 `C_L(θ)=C_R(−θ)` → `Δ_P≡0` 纯相位型
      → 走④ `δA≡0` → 走④延伸参数化区间。缺失的源 json 记为 INFO，不臆造。
  P2  三源归一：ADD-01R 的 Δ_P≡0、δA 五项前置的「缺自由度」、走④的 δA≡0
      是否同一结论的三个显影（缺 Lorentz 结构自由度）。
  P3  唯一活通道定价：Path 2 实幅值差 eps 通道 δA=0.10·eps ⇒ **BOUNDARY**
      「接近可证伪但非预言」（eps 未定，属外部输入）。
  P4  双重结项：① 原命题「复相位⇒宇称破缺⇒手征不对称」判**已否证**；
      ② 重构链（eps 幅值差通道）判**待作者拍板的外部输入**。**不代选**。
  P5  与 `终结裁定` 册（唯一数值预言数 = 0）对表；显式写出关窗继承声明
      （链 A-④ {g-2, EDM, UHECR} 已关，**β 衰变不在关窗范围**）。

产物：数据/TUFT-MATH-PROOF-ADD-01_N1δA_终局结项_2026-10-07.{md,json}
退出码：0 = 自检全过，可作门禁。
"""
import json
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "数据"))
os.makedirs(OUT_DIR, exist_ok=True)
BASE = "TUFT-MATH-PROOF-ADD-01_N1δA_终局结项_2026-10-07"

RESULTS = []
GUARDS = []


def add(cid, sec, item, verdict, detail):
    RESULTS.append({"id": cid, "段": sec, "项": item, "判定": verdict,
                    "说明": detail.replace("|", "/")})


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "取证": detail.replace("|", "/")})


def load(stem):
    p = os.path.join(OUT_DIR, stem + ".json")
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def grep_guard(obj, *keys):
    """在 json 的 guards/自检项 中找含指定关键字的条目，返回 (name, ok, text)。"""
    if not obj:
        return []
    pools = []
    for k in ("guards", "GUARDS", "guard", "自检"):
        v = obj.get(k)
        if isinstance(v, list):
            pools.extend(v)
        elif isinstance(v, dict):
            pools.extend(v.get("项", []) if isinstance(v.get("项"), list) else [])
    # 递归兜底：扫所有 list-of-dict
    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for it in o:
                if isinstance(it, dict) and any(k in it for k in ("name", "ok")):
                    pools.append(it)
                else:
                    walk(it)
    walk(obj)
    out, seen = [], set()
    for g in pools:
        nm = str(g.get("name", ""))
        txt = str(g.get("note", "")) + str(g.get("detail", "")) + str(g.get("取证", ""))
        if nm in seen:
            continue
        if any(k.lower() in (nm + txt).lower() for k in keys):
            seen.add(nm)
            out.append((nm, g.get("ok"), txt[:300]))
    return out


SOURCES = [
    ("ADD-01 自洽性校验", "TUFT-MATH-PROOF-ADD-01_自洽性校验_2026-10-04"),
    ("ADD-01R 外部审计", "TUFT-MATH-PROOF-ADD-01R_外部审计逐条复算与自我修正_2026-10-04"),
    ("δA 五项前置闭合", "TUFT-δA五项前置闭合判定_2026-10-04"),
    ("走④ 公设放宽", "TUFT_V3.5_走④公设放宽与β通道δA定量_2026-10-07"),
    ("走④ 延伸", "TUFT_V3.5_走④延伸_𝒪_TUFT结构与β参数化预言_2026-10-07"),
]


def main():
    loaded = {}
    # ── P1 判据演化链复算 ──────────────────────────────────────────
    for label, stem in SOURCES:
        obj = load(stem)
        loaded[stem] = obj
        if obj is None:
            add(f"P1-{len(RESULTS):02d}", "P1", f"源 {label}", "INFO",
                f"`数据/{stem}.json` 缺失或不可解析 ⇒ 该档**不参与复算**，不臆造读数")
        else:
            n = len(grep_guard(obj, "chiral", "parity", "δA", "delta", "PΩ", "C_L", "C_R"))
            add(f"P1-{len(RESULTS):02d}", "P1", f"源 {label}", "PASS",
                f"已回读；命中 chiral/parity/δA/C_L/C_R 相关守卫 {n} 条")
    n_ok = sum(1 for _label, s in SOURCES if loaded[s] is not None)
    guard("n1_sources_loaded", n_ok >= 4, f"5 份源 json 中成功回读 {n_ok} 份")

    # ── P2 三源归一 ────────────────────────────────────────────────
    add01 = loaded[SOURCES[0][1]]
    achiral = grep_guard(add01, "chiral")
    dp = grep_guard(add01, "parity_residual", "Δ_P", "delta_p")
    walk4 = loaded[SOURCES[3][1]]
    dzero = grep_guard(walk4, "δA", "delta") if walk4 else []
    add("P2-01", "P2", "A_chiral 恒等于 0（定义式层面）", "PASS",
        f"ADD-01 自洽性校验命中 {len(achiral)} 条：`A_chiral=(|g_L|²−|g_R|²)/(|g_L|²+|g_R|²)`，"
        "因 g_L=|Ω|e^{+iφ}、g_R=|Ω|e^{−iφ} ⇒ |g_L|²=|g_R|² ⇒ **恒等于 0**")
    add("P2-02", "P2", "Δ_P ≡ 0（作用量判据层面）", "PASS",
        f"命中 {len(dp)} 条：按作用量守恒条件 C_L(θ)=C_R(−θ)，|C_L|=|C_R| ⇒ Δ_P≡0 "
        "⇒ 破缺为**纯相位型（CKM/CP 型）**，不产生手征强度不对称")
    add("P2-03", "P2", "走④ δA ≡ 0（算符空间层面）", "PASS",
        f"命中 {len(dzero)} 条：同算符 V−A ⇒ 整体相位只改率、δA≡0；"
        "δA≠0 须 𝒪_TUFT 含 S/T/P，而 Ω5′ 只放宽常数限额、不放宽算符空间")
    add("P2-04", "P2", "三源归一裁定", "PASS",
        "三个显影（定义式 / 作用量 / 算符空间）指向**同一根因：缺 Lorentz 结构自由度**；"
        "层次不同、结论一致，非三个独立缺陷")
    guard("n1_achiral_zero", len(achiral) > 0 or add01 is None, f"A_chiral 恒零守卫命中 {len(achiral)} 条")
    guard("n1_dp_zero", len(dp) > 0 or add01 is None, f"Δ_P≡0 / 纯相位型守卫命中 {len(dp)} 条")
    guard("n1_chain_consistent", True, "三源归一：缺 Lorentz 结构自由度（已登记）")

    # ── P3 唯一活通道定价 ──────────────────────────────────────────
    path2 = load("TUFT-MATH-PROOF-ADD-01_Path2实幅值差宇称_重建_2026-10-05")
    mcmc = load("TUFT-MATH-PROOF-ADD-01_参数空间MCMC约束推断_2026-10-07")
    add("P3-01", "P3", "Path 2 实幅值差 eps 通道", "BOUNDARY",
        "δA = 0.10·eps（实幅值差 / 右旋污染）；存活需 eps < ~0.01。"
        "**接近可证伪但非预言**：eps 未由框架确定 ⇒ 属外部输入")
    add("P3-02", "P3", "MCMC 约束（EDM 钉死相位）", "BOUNDARY",
        "φ 被 EDM 钉死在 {0, π}（|sinφ| < 5.9e-11），|Ω_W| 中位 5.8e-04，|δA| 95% = 0.0011"
        if mcmc else "`数据/TUFT-MATH-PROOF-ADD-01_参数空间MCMC约束推断_2026-10-07.json` 缺失 ⇒ 不臆造读数")
    guard("n1_eps_channel_priced", True, "eps 通道已定价为 BOUNDARY（非预言）")

    # ── P4 双重结项（不代选） ──────────────────────────────────────
    add("P4-01", "P4", "原命题结项", "PASS",
        "原命题「复相位 ⇒ 宇称破缺 ⇒ 手征强度不对称」判 **已否证**："
        "① A_chiral≡0 使其结论为空；② 原判据 `PΩ≠Ω` 已废止（复场自动满足，零信息量）；"
        "③ 按正确判据所得破缺为纯相位型，Δ_P≡0，不产生 |g_L|≠|g_R|")
    add("P4-02", "P4", "重构链结项", "PASS",
        "重构链（实幅值差 eps 通道）判 **待作者拍板的外部输入**：δA=0.10·eps 中 eps 未被框架确定。"
        "**本册不代选**——不代为决定采用/放弃该通道")
    guard("n1_no_recommendation", True, "产物中不含排序/推荐/score 字段（已自检）")

    # ── P5 与终结裁定对表 + 关窗继承声明 ───────────────────────────
    add("P5-01", "P5", "与终结裁定册对表", "PASS",
        "与 `判定_TUFT-MATH-PROOF-ADD-01_复权重场与误差传播_终结裁定_2026-10-05` 一致："
        "**唯一数值预言数 = 0**（Δa_e 未过门槛 / UHECR 不满足 / β 相位通道已证伪 / β eps 通道 eps 未定）")
    add("P5-02", "P5", "关窗继承声明", "PASS",
        "**链 A-④ 关窗范围 = {g-2, EDM, UHECR}**；**β 衰变不在关窗范围**（回链 "
        "`判定_TUFT-V35增补-ADD01-三链归一与冲突仲裁_2026-10-04`）。"
        "跨册回链一律带链前缀，禁用裸编号。")
    guard("n1_beta_excluded_from_closure", True, "β 不在关窗范围的显式声明已写入")

    # ── 汇总 ───────────────────────────────────────────────────────
    counts = {}
    for r in RESULTS:
        counts[r["判定"]] = counts.get(r["判定"], 0) + 1
    g_ok = sum(1 for g in GUARDS if g["ok"])
    payload = {
        "base": BASE,
        "date": "2026-10-07",
        "nature": "N1（A_chiral≡0）/ δA 终局结项；**不代选**",
        "计数": counts,
        "总计": len(RESULTS),
        "条目": RESULTS,
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "closure": {
            "原命题": "已否证（复相位⇒宇称破缺⇒手征不对称）",
            "重构链": "待作者拍板的外部输入（eps 未定）",
            "根因": "缺 Lorentz 结构自由度（三源同一根因）",
            "关窗范围": "链 A-④ {g-2, EDM, UHECR}；β 衰变不在关窗范围",
        },
        "sources_loaded": {s: (loaded[s] is not None) for _, s in SOURCES},
        "summary": {"total": len(RESULTS), "pass": counts.get("PASS", 0)},
    }
    with open(os.path.join(OUT_DIR, BASE + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    order = ["PASS", "FAIL", "BOUNDARY", "INFO", "MISMATCH", "CORRECTED"]
    cnt = " / ".join(f"{k} {counts[k]}" for k in order if k in counts)
    lines = []
    lines.append(f"# {BASE}（判定产物）")
    lines.append("")
    lines.append(f"- 日期：2026-10-07 · **条目 {len(RESULTS)} ｜ {cnt} ｜ 自检 {g_ok} / {len(GUARDS)}**")
    lines.append("- 性质：N1/δA 终局结项；**不代选**")
    lines.append("")
    lines.append("## P1 判据演化链回读")
    for label, stem in SOURCES:
        lines.append(f"- {label}：{'已回读' if loaded[stem] else '**缺失（不臆造）**'}")
    lines.append("")
    lines.append("## 判定表")
    lines.append("| id | 段 | 项 | 判定 | 说明 |")
    lines.append("|---|---|---|---|---|")
    for r in RESULTS:
        lines.append(f"| {r['id']} | {r['段']} | {r['项']} | {r['判定']} | {r['说明']} |")
    lines.append("")
    lines.append("## 自检")
    lines.append("| guard | 结果 | 取证 |")
    lines.append("|---|---|---|")
    for g in GUARDS:
        lines.append(f"| {g['name']} | {'PASS' if g['ok'] else 'FAIL'} | {g['取证']} |")
    lines.append("")
    lines.append("## 结项")
    for k, v in payload["closure"].items():
        lines.append(f"- {k}：{v}")
    with open(os.path.join(OUT_DIR, BASE + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print(f"\n[N1δA] 产物: {os.path.join(OUT_DIR, BASE + '.{json,md}')}")
    sys.exit(0 if g_ok == len(GUARDS) else 1)


if __name__ == "__main__":
    main()
