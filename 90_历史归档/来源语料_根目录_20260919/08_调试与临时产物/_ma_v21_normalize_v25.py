# -*- coding: utf-8 -*-
"""
MainAgent v21 审计 -> 企业级三件套归一化 v2.5（权威工作区根目录）
====================================================================
背景：子代理未经 MainAgent 审计自升 v2.3/v2.4、equation_range=E1-E446，
改主册/台账/书稿；归档作业曾把三件套移入 openuft/.../02_TUFT_来源（已复制回根目录）。
本脚本：
  - JSON：v2.4 -> MainAgent v2.5；作废 v2.3/v2.4 SSOT；E443-E446 重判为方法学/公设；
          D18 单一 MainAgent 注记；backlog 顶部换 MainAgent v21 PRIORITY；
          新增 main_agent_v21_audit（含勘误#27）；json.load 校验。
  - MD  ：标题/版本 -> v2.5；顶部插 MainAgent v2.5 重审定级通告；§9 加勘误 #27。
  - HTML：干净 v2.2 -> v2.5；banner + ④‑12 面板 + 勘误27 + stat/title/footer/配套。
所有替换逐锚 assert 唯一；CRLF 保留。
"""
import io, json, os

BASE = r"D:\a10\aikjx\code\my_lib"
PJ = os.path.join(BASE, "TUFT_归一化台账_v1.0.json")
PM = os.path.join(BASE, "TUFT_企业级归一化主册_v1.0.md")
PH = os.path.join(BASE, "TUFT_企业级归一化全维架构图_E1-E336.html")

# ============================================================ JSON
with io.open(PJ, "r", encoding="utf-8") as f:
    d = json.load(f)

assert d["version"] == "v2.4", d["version"]  # 仅在污染版上运行一次

ERR27 = ("#27 (v21 MainAgent audit): (1) Cook-Zalutskas asymptotic-weight spectrum was externally "
 "reported as 'method verified / new hard GR gate 4.2e-10', but its own convergence table is a "
 "NON-convergent single point: error already ~5e-10 at N=30, stays/rises N=40/50 (4.4->5.0e-10) "
 "and BLOWS UP at N=60 (1.5e-5 / 5.8e-6); it is not spectral exponential convergence and is NOT "
 "accepted as a new GR gate. The R2 'GR 15-16 digit' result (mpmath dps=45, N=100/200/400/1000) is "
 "in substance the Leaver s=-2 three-term recurrence reproduced ON SCHWARZSCHILD = the existing "
 "gate E436-E438 (MainAgent 2.1e-11), NOT a new independent method gate. (2) The coalition raised "
 "the normalization to v2.3/v2.4 and equation_range to E1-E446 and rewrote the master/ledger/book "
 "without MainAgent audit; those unsupervised v2.3/v2.4 SSOT states are VOID, superseded by MainAgent "
 "v2.5. E443-E446 keep their IDs but are RECLASSIFIED as methodological-negative / counterfactual-"
 "postulate records; NONE is a newly established positive TUFT theorem. MainAgent independent "
 "_ma_v21_pole.py / _ma_v21_diag(1-3).py additionally show: wavefunction two-branch Wronskian+Muller "
 "shooting runs away (|W|=2.3e3), Riccati-findroot has movable poles and is ill-posed as an integral "
 "matcher, naive finite-domain Chebyshev QEP plateaus at ~6e-3 and jumps to 4.5e-2 (a=2.5). "
 "modified-QNM pole stays OPEN (6th consecutive round); the only trusted GR complex-QNM gate remains "
 "Leaver E436-E438 (2.1e-11); correct route = a TRUE compactified LINEAR generalized-eigenvalue "
 "spectrum with BOTH horizon-Frobenius and infinity-outgoing weights built in (small N must converge "
 "monotonically >=1e-8), or multi-segment Frobenius; pass GR >=8 digits first.")

audit = {
    "round": "v21",
    "normalization_mainagent": "v2.5",
    "supersedes_unsupervised": ["v2.3", "v2.4"],
    "erratum": "#27",
    "scientific_verdict": "modified-QNM pole OPEN for the 6th consecutive round; no TUFT root reported by any route; no new positive TUFT theorem.",
    "only_trusted_gr_gate": "Leaver s=-2 three-term continued fraction E436-E438, MainAgent independent 2.1e-11 (0.373671684-0.088962316i)",
    "mainagent_independent_scripts": ["_ma_v21_pole.py", "_ma_v21_diag.py", "_ma_v21_diag2.py", "_ma_v21_diag3.py", "TUFT_v21_极点方法独立预审_打靶与朴素谱双否.md"],
    "reclassification": {
        "E443": "METHODOLOGICAL-NEGATIVE (open/limited): Leaver-type rational 3-term recurrence does not carry to TUFT as written (potential has e^{+-2/rho} essential singularity as rho->0); finite-box Robin/CAP spectral self-gate FAIL (5th wall). Scope limited: physical domain rho>=rho_h=0.61; rules out single-segment rational recurrence / transparent box only, NOT a principle impossibility.",
        "E444": "COUNTERFACTUAL POSTULATE (conditional only): virtual flat outgoing waveguide with core V=0 gives |r_b|^2@.3737=0.3250, epsilon=(1-|r_b|^2)^2=0.4557; NOT the true TUFT cavity value (E442: no interior flat zone), delta_omega UNMEASURED; observability conditional/critical.",
        "E445": "METHODOLOGICAL-NEGATIVE: R1 envelope-reduction global spectrum GR gate FAIL (6th wall); gate had tested only that findroot did not throw (root values ~1 digit / n1 absurd / box-dependent / pseudo-eigenvalue 0.2797-0.2234 hijack); positive residue = O(1/s^2) outgoing Robin correction direction (corrected converges vs bare saturation 8.8e-4), residual floor ~1e-6.",
        "E446": "METHODOLOGICAL-NEGATIVE + OLD-GATE REPRODUCTION: the reported GR 15-digit gate is the Leaver recurrence on Schwarzschild (=E436-E438, not new); TUFT side hits structural wall (factorization e^{-2/rho} cannot remove kinetic term omega^2 e^{4/rho} P; zero Frobenius radius at rho=0; at rho_h radius ~0.81 reaches only rho~1.42, not infinity; coefficients ~1e105 blow up)."
    },
    "cook_gate_4p2e_verdict": "NOT ACCEPTED as a new GR gate: |dw| = 4.4e-10 (N30) -> 4.7e-10 (N40) -> 5.0e-10 (N50) plateau -> 1.5e-5/5.8e-6 (N60); non-monotonic plateau+blowup, not spectral convergence.",
    "naive_spectral_plateau": "finite-domain Chebyshev QEP nearest lower-half mode: N500 |d|=7.0e-3 -> N650 6.0e-3 plateau; mapping a=2.5 jumps to 4.5e-2 (pseudo-mode); insufficient to resolve a ~1e-2 pole shift.",
    "next_route": "true Cook-Zalutskas-style compactified LINEAR generalized eigenproblem with horizon Frobenius AND infinity outgoing factors absorbed into the weight (small N, monotonic >=1e-8 GR), or multi-segment Frobenius+Wronskian; hard GR self-gate >=8 digits before any TUFT root; forbid one-way interior IVP (E442), single-exp echo fit (#25), single-ended complex shooting (#18/#19).",
    "erratum_27_text": ERR27
}

d["version"] = "v2.5"
d["latest_round"] = "v21_ma_audit"
d["equation_range"] = "E1-E446"
d["date"] = "2026-09-19"
d["last_updated"] = "2026-09-19 MainAgent v2.5 re-audit (supersedes unsupervised v2.3/v2.4)"
d["superseded_unsupervised_versions"] = ["v2.3", "v2.4"]
d["main_agent_v21_audit"] = audit

d["four_state_counts_approx"] = {
    "strict": 35, "conditional": 61, "definition": 18, "open": 27,
    "note": ("E1-E442 authoritative counts. E443/E445/E446 = methodological-negative, E444 = "
             "counterfactual-postulate (MainAgent v2.5 reclassification); none is promoted to a new "
             "TUFT theorem, so they are NOT added to strict/conditional theorem counts.")
}

# D18: replace coalition v2.3/v2.4 notes by a single MainAgent note
p = d["predictions"]["D18"]
p.pop("v20_closure_note", None)
p.pop("v21_closure_note", None)
p["main_agent_v25_note"] = ("MainAgent v2.5 (erratum#27): sigma_abs=0 remains a theoretical reflection-core "
    "prediction (not yet observed); ringdown modified-QNM pole is OPEN for the 6th consecutive round "
    "(R1 envelope spectrum 6th-wall FAIL; R2 structural wall; Cook 4.2e-10 non-convergent, not accepted; "
    "the only trusted GR gate is Leaver E436-E438 2.1e-11). E444 r_b=0.325/epsilon=0.456 is a "
    "counterfactual virtual-waveguide POSTULATE with delta_omega unmeasured -> observability "
    "conditional/critical only. Unsupervised coalition v2.3/v2.4 notes voided.")

# backlog: drop coalition v2.3/v2.4 closures, insert one MainAgent priority
d["open_backlog"] = [b for b in d["open_backlog"]
                     if not (isinstance(b, str) and (b.startswith("v2.3 CLOSURE") or b.startswith("v2.4 CLOSURE")))]
priority = ("v2.5 MAIN-AGENT PRIORITY (v21 audit, erratum#27, E443-E446 reclassified): modified-QNM pole OPEN "
  "6th round. Trusted GR gate = Leaver E436-E438 only. Build a TRUE compactified LINEAR generalized "
  "eigenproblem absorbing BOTH horizon Frobenius and infinity outgoing into the weight (small N must "
  "converge monotonically to GR 0.373671684-0.088962316i >=1e-8; reject any plateau/blow-up like the "
  "Cook 4.2e-10 N30-plateau/N60-blowup), or multi-segment Frobenius (core to rho~1.42 + barrier + far "
  "outgoing) matched by Wronskians; only then swap inner boundary to TUFT Neumann reflection core and "
  "demand stability vs N/domain/near-wall offset <1e-6. Forbidden repeats: one-way interior IVP for r_b "
  "(E442 non-isolable), single-exp echo fit (#25), single-ended complex shooting (#18/#19), naive finite "
  "box Chebyshev QEP (6e-3 plateau), Riccati-findroot integral matching (movable poles). E444 virtual "
  "waveguide is counterfactual only. Page/Hawking thermal spectrum (specular wall f=0 zero-flux "
  "tension)/baryogenesis/quantum-measurement(Born rule) remain OPEN.")
d["open_backlog"].insert(0, priority)

# tag coalition raw keys as reclassified (kept for traceability)
for k in ("v20_two_subtask_key_results", "v21_two_spectrum_key_results"):
    if k in d and isinstance(d[k], dict):
        d[k]["main_agent_status"] = "RECORDED FOR TRACEABILITY; RECLASSIFIED/VOIDED as SSOT by MainAgent v2.5 (see main_agent_v21_audit)"

with io.open(PJ, "w", encoding="utf-8", newline="\n") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
with io.open(PJ, "r", encoding="utf-8") as f:
    chk = json.load(f)
assert chk["version"] == "v2.5" and chk["equation_range"] == "E1-E446"
assert "main_agent_v21_audit" in chk and "v21_closure_note" not in chk["predictions"]["D18"]
print("JSON OK v2.5 / v21_ma_audit / E1-E446; backlog =", len(chk["open_backlog"]),
      "; v2.3/v2.4 closures removed =", not any(b.startswith(("v2.3 CLOSURE", "v2.4 CLOSURE")) for b in chk["open_backlog"]))

# ============================================================ MD
with io.open(PM, "r", encoding="utf-8", newline="") as f:
    raw = f.read()
NL = "\r\n" if "\r\n" in raw else "\n"

def rep(s, old, new, key):
    c = s.count(old)
    assert c == 1, "MD ANCHOR[%s] count=%d" % (key, c)
    return s.replace(old, new)

raw = rep(raw, "# TUFT 企业级归一化主册 v2.4", "# TUFT 企业级归一化主册 v2.5（MainAgent 重审定级）", "title")
raw = rep(raw, "（内部 version=v2.4）", "（内部 version=v2.5）", "version-inline")

banner = (
"> **★ v2.5 最新（MainAgent v21 独立审计，勘误 #27；作废子代理未经审计自升的 v2.3/v2.4）**："
"子代理 v21 两条谱路线（R1 包络约化全局谱、R2 本质奇点因子化）**均未报 TUFT 根，modified-QNM 极点连续第 6 轮 OPEN**。"
"MainAgent 复核裁定 **E443–E446 全部保留编号但降级为方法学否定/反事实公设记录，无一是新成立的 TUFT 正向定理**："
"E443＝单段有理递推/有限盒方法学否定（物理域 ρ≥0.61，非原理不可能）；E444＝反事实虚拟平坦波导公设（|r_b|²=.325/ε=.456，δω 未测，非真实腔值）；"
"E445＝R1 GR 门第 6 墙 FAIL（仅 O(1/s²) 出射 Robin 方向有效、残差 1e-6 地板）；E446＝R2 其 GR“15 位”实为重跑 **Leaver 旧门 E436–438（非新门）**、TUFT 侧撞本质奇点结构墙。"
"**Cook–Zalutskas 4.2e-10 不采纳（勘误 #27）**：落盘表 N=30 即 ~5e-10 平台、N=40/50 不降反微升、N=60 崩至 1.5e-5/5.8e-6，非谱指数收敛。"
"MainAgent 另独立证伪（`_ma_v21_pole.py`/`_ma_v21_diag1–3.py`）：波函数 Wronskian+Muller 打靶跑飞（|W|=2.3e3）、Riccati-findroot 可动极点不适定、朴素有限域 Chebyshev 谱卡 6e-3 平台且跳模 4.5e-2。"
"**唯一可信 GR 复 QNM 门＝Leaver E436–438（独立 2.1e-11）**；正路＝真内建视界 Frobenius＋无穷出射权的紧化【线性】广义特征值（小 N 须单调收敛≥1e-8）或多段 Frobenius，先过 GR ≥8 位。"
"权威口径：**version=v2.5 / latest_round=v21_ma_audit / E1–E446（443–446 方法学/公设级）/ 勘误 #27**；归档目录 openuft/…/02_TUFT_来源 内 v2.4 件为来料快照、非 SSOT。"
+ NL + NL)
raw = rep(raw, "> **v2.3 最新（v20 两数值子任务收口", banner + "> **v2.3 最新（v20 两数值子任务收口", "banner")

# §9 erratum #27 after the #26 row
lines = raw.split(NL)
idx26 = next(i for i, ln in enumerate(lines) if ln.startswith("| 26 |"))
e27 = ("| 27 | ① 对外称 Cook–Zalutskas 渐近权谱“方法验证成功/GR 门 4.2e-10 硬资产”；"
"② 子代理未经 MainAgent 审计自升归一化 v2.3/v2.4、equation_range→E1–E446、改主册/台账/书稿 | "
"MainAgent v21 独立审计：① cook 落盘收敛 N=30 即 ~5e-10 平台、N40/50 不降（4.4→5.0e-10）、N60 崩至 1.5e-5/5.8e-6，系非谱指数收敛单点，**不采纳为新 GR 门**；R2 所报 GR“15 位”(dps45) 本质＝Leaver s=−2 三项递推在 Schwarzschild 复现（旧门 E436–438，2.1e-11），非新方法硬资产。"
"② **作废子代理 v2.3/v2.4 SSOT**，MainAgent v2.5 重审定级：E443/E445/E446＝方法学否定（单段有理递推/有限盒/因子化；物理域 ρ≥0.61，非原理否定）、E444＝反事实虚拟波导公设（|r_b|²=.325/ε=.456、δω 未测），**无一是新成立 TUFT 正向定理**。"
"MainAgent `_ma_v21_pole/diag1–3` 另证 Wronskian 打靶跑飞（|W|=2.3e3）、Riccati-findroot 可动极点不适定、朴素有限域 Cheb QEP 6e-3 平台/a2.5 跳模 4.5e-2。modified-QNM 极点连续第 6 轮 OPEN；唯一可信 GR 门＝Leaver E436–438；正路＝真内建两端渐近权紧化线性谱/多段 Frobenius，先过 GR≥8 位 | v21（MainAgent） |")
lines.insert(idx26 + 1, e27)
raw = NL.join(lines)

with io.open(PM, "w", encoding="utf-8", newline="") as f:
    f.write(raw)
assert "主册 v2.5" in raw and "| 27 |" in raw and "勘误 #27" in raw
print("MD OK v2.5 + banner + erratum #27")

# ============================================================ HTML (clean v2.2 -> v2.5)
with io.open(PH, "r", encoding="utf-8", newline="") as f:
    h = f.read()

def hrep(s, old, new, key):
    c = s.count(old)
    assert c == 1, "HTML ANCHOR[%s] count=%d" % (key, c)
    return s.replace(old, new)

h = hrep(h, "（v1–v20）｜v2.2：Leaver GR 复QNM门 PASS 独立 1e-11",
         "（v1–v21）｜v2.5（MainAgent 重审定级，勘误#27）：v21 谱法连续6墙 OPEN、E443–446 方法学/公设级、Cook 4.2e-10 非收敛不采纳；历史 v2.2：Leaver GR 复QNM门 PASS 独立 1e-11", "title")

h = hrep(h, '<div class="n" style="color:var(--novel)">E1–E442</div>',
         '<div class="n" style="color:var(--novel)">E1–E446</div>', "stat-range")
h = hrep(h, '<div class="n">25</div><div class="l">勘误固化条',
         '<div class="n">27</div><div class="l">勘误固化条（#27 v21 MainAgent 重审定级/作废 v2.3-v2.4）', "stat-err")

banner_html = (
'<div class="note bad" style="margin:6px 0 14px"><b>★ v2.5 MainAgent 重审定级（勘误 #27，E443–E446）：</b>'
'子代理未经审计自升的 v2.3/v2.4 <b>作废</b>。E443–E446 保留编号但<b>降级为方法学否定/反事实公设记录，无一是新成立 TUFT 正向定理</b>。'
'R1 包络约化谱 GR 门第 6 墙 FAIL（O(1/s²) 出射 Robin 方向有效、残差 1e-6 地板）；R2 所报 GR“15 位”＝Leaver 旧门 E436–438 复现（非新硬资产），TUFT 侧 ω²e^{4/ρ}P 残留/Frobenius 半径 .81 够不到无穷远；'
'<b>Cook–Zalutskas 4.2e-10 系 N30 即达、N 增平台、N60 崩至 1e-5 的非收敛单点，不采纳</b>；E444 r_b=.325/ε=.456 为反事实虚拟波导公设（δω 未测）。'
'MainAgent 独立 _ma_v21_pole/diag1–3 另证 Wronskian 打靶跑飞、Riccati-findroot 不适定、朴素谱 6e-3 平台/跳模。'
'<b>modified-QNM 极点连续第 6 轮 OPEN；唯一可信 GR 复 QNM 门＝Leaver E436–438（独立 2.1e-11）；正路＝内建两端渐近权的紧化线性谱/多段 Frobenius（先过 GR≥8 位）。</b></div>')
h = hrep(h, '<div class="stats">', banner_html + '<div class="stats">', "banner")

h = hrep(h, "态 II 撤销，极点 OPEN</b>。</div>",
         "态 II 撤销，极点 OPEN</b>｜<b style=\"color:#ff7b72\">#27（v21 MainAgent）Cook 4.2e-10 系 N30 平台/N60 崩的非收敛单点不采纳、R2“15位”＝Leaver 旧门 E436–438；子代理自升 v2.3/v2.4 作废，E443–446 降方法学/公设；极点连续 6 轮 OPEN</b>。</div>", "errata27-excerpt")
h = hrep(h, "【勘误节选·现共 26 条·禁止回退】", "【勘误节选·现共 27 条·禁止回退】", "errata-count")

h = hrep(h, "《TUFT_归一化台账_v1.0.json》（内部 <b>v2.2 / latest_round=v20 / E1–E442</b>，json.load 校验 OK）",
         "《TUFT_归一化台账_v1.0.json》（内部 <b>v2.5 / latest_round=v21_ma_audit / E1–E446</b>，json.load 校验 OK；作废子代理 v2.3/v2.4）", "peitao")

panel = (
'<section style="margin:14px 0">'
'<h2>④‑12 v21：谱方法连续 6 墙 MainAgent 重审定级（E443–E446，勘误 #27）——无新 TUFT 根，极点连续 6 轮 OPEN'
'<span class="badge" style="color:#ff7b72;border-color:#ff7b72">v2.3/v2.4 作废 · 方法学/公设级</span></h2>'
'<div class="eq"><span class="id d">E443</span>Leaver/有理三项递推不可直接用于 TUFT（势 ρ→0 含 e^{±2/ρ} 本质奇点）；有限盒 Robin/CAP 谱第 5 墙。MainAgent 限定：物理域 ρ≥0.61，仅否“单段有理递推/透明盒”，<b>非原理否定</b> → 方法学否定（开放）。</div>'
'<div class="eq"><span class="id o">E444</span>虚拟平坦波导（核侧 V=0 公设）|r_b|²=.325/ε=.456，δω 未测 → <b>反事实公设·仅条件</b>，非 TUFT 真实腔值（E442 腔内无平坦区）。</div>'
'<div class="eq"><span class="id d">E445</span>R1 包络谱 GR 门 FAIL（第 6 墙）：根值仅 ~1 位/n1 实部荒谬/盒漂移/行列式条件数爆炸；O(1/s²) Robin 修正方向有效（corrected 收敛 vs bare 8.8e-4 饱和）但残差 1e-6 地板、被伪本征值 0.2797−.2234 劫持 → 方法学否定。</div>'
'<div class="eq"><span class="id d">E446</span>R2 因子化：GR“15 位”＝Leaver 旧门 E436–438 复现（非新门）；TUFT 动能项 ω²e^{4/ρ}P 残留、ρ_h Frobenius 半径 .81 仅延到 ρ≈1.42 够不到无穷远、系数 ~1e105 爆炸 → 结构墙/方法学否定。</div>'
'<div class="note bad"><b>Cook 4.2e-10 不采纳（勘误 #27）</b>：N30→50 平台 ~5e-10（4.4→5.0e-10）、N60 崩 1.5e-5，非谱指数收敛。MainAgent 独立：波函数 Wronskian 打靶 Muller 跑飞 |W|=2.3e3、Riccati-findroot 可动极点不适定、朴素有限域 Cheb QEP 6e-3 平台且 a=2.5 跳模 4.5e-2。<b>modified-QNM 仍 OPEN（连续 6 轮）</b>；正路＝真内建视界 Frobenius＋无穷出射权的紧化【线性】广义特征值（小 N 单调收敛≥1e-8）或多段 Frobenius，先过 GR ≥8 位。</div>'
'</section>')
h = hrep(h, "<footer>", panel + "<footer>", "panel")

h = hrep(h, "<footer>TUFT 企业级归一化 v2.2（含 v20）｜",
         "<footer>TUFT 企业级归一化 v2.5（MainAgent 重审定级；作废子代理未经审计的 v2.3/v2.4）｜<b>v21 谱方法审计（勘误#27，E443–E446）：R1 包络谱 GR 门第 6 墙 FAIL、R2“15位”＝Leaver E436–438 旧门复现非新门、Cook 4.2e-10 非收敛不采纳；两线均未报 TUFT 根，modified-QNM 连续 6 轮 OPEN（E443–446 全降方法学/反事实公设，无新 TUFT 定理）。</b>历史——TUFT 企业级归一化 v2.2（含 v20）｜", "footer")

with io.open(PH, "w", encoding="utf-8", newline="") as f:
    f.write(h)
assert ("v2.5" in h) and ("④‑12" in h) and ("勘误 #27" in h) and ("E1–E446" in h)
print("HTML OK v2.5 + banner + panel ④-12 + erratum #27")
print("ALL NORMALIZED v2.5")
