#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一场论知识图谱化 —— 把 v8-v18 + 虚拟宇宙模拟器/可视化 整理为机器可读知识图谱

产物（统一场论_知识图谱.*）：
  .json    节点(类型)+关系边(类型) + 统计
  .graphml 供外部图工具（Gephi/NetworkX）打开
  .md      人类可读总结（含诚实边界簇）
  figures/fig_knowledge_graph.png  可视化（分层力导布局，按类型/关系着色）
诚信：仅刻画框架 v8-v18 已证内容与显式诚实边界，不粉饰。
"""
from __future__ import annotations
import sys, os, json, math
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

# ----------------------- 节点 -----------------------
# (id, label_en(绘图), zh(文档), type)
NODES = [
    # 版本链
    ("v8.1",   "v8.1 refute-old",        "v8.1 证伪旧四力简并机制",   "version"),
    ("v9",     "v9 dual-eq",             "v9 对偶场方程重构",         "version"),
    ("v10",    "v10 Proca 4-force",      "v10 四力统一场方程(Proca)", "version"),
    ("v11",    "v11 deriv-chain",        "v11 全域求导证明链",        "version"),
    ("v12",    "v12 running/non-Abel",   "v12 跑动耦合·非阿贝尔",     "version"),
    ("v13",    "v13 weak-chiral/spec",   "v13 弱手征·双环·质量谱",    "version"),
    ("v14",    "v14 PN/grav-wave",       "v14 后牛顿·引力波检验",     "version"),
    ("v15",    "v15 kappa-Phi fix G",    "v15 κ-Φ桥接固定 G",         "version"),
    ("v16A07", "v16 A07 geo-action",     "v16 A07 螺旋世界几何作用量","version"),
    ("v17",    "v17 topo-QN/3-gen",      "v17 拓扑量子数·物质谱·代结构","version"),
    ("v18",    "v18 FRW cosmology",      "v18 宇宙本源 FRW宇宙学",    "version"),
    ("v19",    "v19 TEGT",               "v19 拓扑涌现规范论(TEGT)",  "version"),
    ("v20",    "v20 SU(2)_k gens",       "v20 拓扑代际与SU(2)_k",      "version"),
    ("v21",    "v21 braid matrices",      "v21 辫表示构造与验证",       "version"),
    ("v22",    "v22 SU(2)_k S,T",         "v22 SU(2)_k模表示与S矩阵",   "version"),
    ("v23",    "v23 mass hier bound",     "v23 代质量层级拓扑量化",     "version"),
    ("v24",    "v24 sigma1 explicit",     "v24 B₃ Jones表示收口",        "version"),
    ("v25",    "v25 vis graph",           "v25 交互式知识图谱",          "version"),
    ("v26",    "v26 cross-check",         "v26 全维精算复核与新发现",    "version"),
    ("v27",    "v27 jones-sigma2",        "v27 完整Jones表示σ₂闭合",     "version"),
    ("v28",    "v28 jones-sigma2-gen",     "v28 通用Jones表示σ₂闭合",     "version"),
    ("v29",    "v29 golden-ratio-origin",  "v29 黄金比φ拓扑起源",         "version"),
    ("v30",    "v30 mass-attack",          "v30 代质量层级正面攻击",      "version"),
    ("v31",    "v31 QG/Lambda topo",       "v31 量子引力与宇宙学常数(拓扑层)", "version"),
    ("v32",    "v32 Lambda residue",        "v32 宇宙学常数残差(拓扑层归零与局域层抵消)", "version"),
    ("v33",    "v33 alpha pitch",             "v33 精细结构常数α(螺距比量化)", "version"),
    ("v34",    "v34 closure ledger",        "v34 全链诚实边界收口报告", "version"),
    ("v35",    "v35 anchor-conditioned attack", "v35 双锚约束下SM群结构与代层级推导", "version"),
    ("sim",    "virtual-universe sim",   "虚拟宇宙模拟器",            "tool"),
    ("viz",    "visualization",          "虚拟宇宙可视化",            "tool"),
    ("graph",  "knowledge-graph",        "知识图谱可视化",            "tool"),
    # 概念/定律
    ("old_unified", "OLD unified (refuted)", "旧四力简并机制(已证伪)", "concept"),
    ("dual_eq",    "dual field eq",      "对偶场方程",                "concept"),
    ("unify_law",  "Proca/Yukawa law",   "统一力律 Proca/Yukawa",     "concept"),
    ("gravity",    "gravity",            "引力",                     "concept"),
    ("em",         "EM",                 "电磁",                     "concept"),
    ("weak",       "weak force",         "弱力",                     "concept"),
    ("strong_res", "strong(residual)",   "强(剩余)力",               "concept"),
    ("deriv_chain","global deriv chain", "全域求导链",               "concept"),
    ("running",    "running coupling",   "跑动耦合 α",               "concept"),
    ("nonabel",    "non-Abelian color",  "非阿贝尔色因子",           "concept"),
    ("weak_chiral","weak chiral/2-loop", "弱手征·双环",              "concept"),
    ("mass_spec",  "mass spectrum",      "质量谱",                   "concept"),
    ("pn_gw",      "PN + grav wave",     "后牛顿·引力波(γ=1)",       "concept"),
    ("kappaphi",   "kappa-Phi bridge",   "κ-Φ桥接",                  "concept"),
    ("G_const",    "Newton G",           "牛顿常量 G",               "constant"),
    ("helical",    "helical worldline",  "螺旋世界线 spiral",        "concept"),
    ("action_A07", "geo action A07",     "几何作用量 A07(EH bootstrap)","concept"),
    ("topo_qn",    "topological QN",     "拓扑量子数",               "concept"),
    ("charge_q",   "charge q=(k/3)e",    "电荷量子化 q=(k/3)e",      "concept"),
    ("gens",       "3 generations",      "代结构(3代)",              "concept"),
    ("gauge_grp",  "SU(3)xSU(2)xU(1)",   "规范群结构",               "concept"),
    ("friedmann",  "Friedmann eq",       "Friedmann 方程",           "concept"),
    ("scale_a",    "scale factor a(t)",  "尺度因子 a(t)",            "concept"),
    ("hubble",     "Hubble flow",        "哈勃流 v=H·r",             "concept"),
    ("rho_m",      "matter rho~a^-3",    "物质密度 ρ∝a⁻³",           "concept"),
    ("rho_r",      "radiation rho~a^-4", "辐射密度 ρ∝a⁻⁴",           "concept"),
    ("lambda",     "Lambda Λ",           "宇宙学常数 Λ",             "constant"),
    # 开放/诚实边界
    ("alpha_open",   "alpha (not 1st-princ)", "耦合常数α(未第一性推导)", "open"),
    ("confinement",  "QCD confinement",       "QCD 色禁闭线性项",          "open"),
    ("dm_infl",      "DM/inflation/nu-mass",  "暗物质·暴胀·中微子质量",    "open"),
    ("sing_qg",      "singularity/QG",        "奇点·量子引力",            "open"),
    ("lambda_num",   "Lambda value (open)",   "Λ 数值(几何开放)",         "open"),
    ("mass_hier",    "mass hierarchy(open)",  "质量层级(拓扑Yukawa开放)",  "open"),
    ("n137_claim",   "N=137 alpha claim",      "旧『N=137 推导α』伪推导",   "open"),
]

# ----------------------- 关系边 -----------------------
# (source, target, relation, category)
# category: proof(蓝) / unify(绿) / refute(红) / partial(橙) / open(灰虚线)
EDGES = [
    ("v8.1", "old_unified", "refutes", "refute"),
    ("v9", "dual_eq", "reconstructs", "proof"),
    ("v10", "unify_law", "derives", "unify"),
    ("unify_law", "gravity", "manifests_as", "unify"),
    ("unify_law", "em", "manifests_as", "unify"),
    ("unify_law", "weak", "manifests_as", "unify"),
    ("unify_law", "strong_res", "manifests_as", "unify"),
    ("v11", "v10", "proves", "proof"),
    ("v11", "deriv_chain", "establishes", "proof"),
    ("v12", "v11", "extends", "proof"),
    ("v12", "running", "introduces", "proof"),
    ("v12", "nonabel", "introduces", "proof"),
    ("v13", "v12", "extends", "proof"),
    ("v13", "weak_chiral", "derives", "proof"),
    ("v13", "mass_spec", "derives", "proof"),
    ("v14", "v13", "validates", "proof"),
    ("v14", "pn_gw", "verifies", "proof"),
    ("v15", "kappaphi", "uses", "proof"),
    ("v15", "G_const", "fixes", "proof"),
    ("v15", "v11", "depends_on", "proof"),
    ("v15", "v14", "converges_to", "proof"),
    ("v16A07", "helical", "uses", "proof"),
    ("v16A07", "action_A07", "produces", "proof"),
    ("action_A07", "unify_law", "bootstraps", "proof"),
    ("v16A07", "action_A07", "partial_close", "partial"),
    ("v17", "v16A07", "depends_on", "proof"),
    ("v17", "topo_qn", "derives", "proof"),
    ("topo_qn", "charge_q", "gives", "proof"),
    ("topo_qn", "gens", "gives", "proof"),
    ("topo_qn", "gauge_grp", "gives", "proof"),
    ("v17", "gauge_grp", "partial_close", "partial"),
    ("v18", "v10", "depends_on", "proof"),
    ("v18", "v14", "depends_on", "proof"),
    ("v18", "v15", "depends_on", "proof"),
    ("v18", "friedmann", "derives", "proof"),
    ("v18", "scale_a", "derives", "proof"),
    ("v18", "hubble", "derives", "proof"),
    ("v18", "rho_m", "derives", "proof"),
    ("v18", "rho_r", "derives", "proof"),
    ("v18", "lambda", "derives", "proof"),
    ("v18", "lambda_num", "partial_close", "partial"),
    ("v18", "sing_qg", "open", "open"),
    ("v19", "v16A07", "depends_on", "proof"),
    ("v19", "v17", "depends_on", "proof"),
    ("v19", "gauge_grp", "emerges", "proof"),
    ("v19", "gens", "emerges", "proof"),
    ("v19", "charge_q", "reuses", "proof"),
    ("v19", "lambda_num", "proposes_source", "partial"),
    ("mass_hier", "v19", "open_boundary", "open"),
    ("mass_hier", "v13", "open_boundary", "open"),
    ("v20", "v19", "depends_on", "proof"),
    ("v20", "gauge_grp", "emerges", "proof"),
    ("v20", "gens", "closes", "partial"),
    ("v16A07", "v20", "determines", "proof"),
    ("v21", "v19", "constructs", "proof"),
    ("v21", "v20", "constructs", "proof"),
    ("v21", "gauge_grp", "realizes", "proof"),
    ("v21", "v17", "realizes", "proof"),
    ("v22", "v19", "realizes", "proof"),
    ("v22", "v20", "realizes", "proof"),
    ("v22", "v21", "constructs", "proof"),
    ("v22", "gauge_grp", "realizes", "proof"),
    ("v23", "v17", "quantifies", "honest"),
    ("v23", "v19", "quantifies", "honest"),
    ("v23", "v20", "quantifies", "honest"),
    ("v23", "v22", "uses", "honest"),
    ("v23", "mass_hier", "bounds", "honest"),
    ("v24", "v21", "constructs", "proof"),
    ("v24", "v22", "constructs", "proof"),
    ("v24", "gauge_grp", "realizes", "proof"),
    ("v25", "graph", "visualizes", "engineering"),
    ("v26", "v24", "refines", "honest"),
    ("v26", "v22", "cross_checks", "honest"),
    ("v26", "mass_hier", "cross_checks", "honest"),
    ("v27", "v24", "completes", "new"),
    ("v27", "v22", "uses_S", "new"),
    ("v28", "v27", "generalizes", "new"),
    ("v28", "v24", "corrects_convention", "new"),
    ("v28", "v22", "uses_S", "new"),
    ("v29", "v26", "explains_observation", "new"),
    ("v29", "v28", "uses_general_k", "new"),
    ("v29", "v23", "honest_gap_unchanged", "new"),
    ("v30", "v23", "narrows_boundary", "honest"),
    ("v30", "v29", "uses_spectrum_lead", "new"),
    ("v30", "mass_hier", "excludes_topological", "honest"),
    ("v31", "v22", "uses_verlinde_counting", "new"),
    ("v31", "lambda", "structurally_evades_catastrophe", "partial"),
    ("v31", "lambda_num", "narrows_to_1e-122_residue", "honest"),
    ("v31", "v18", "extends_cosmology_layer", "partial"),
    ("v31", "v20", "clarifies_k2_scope", "partial"),
    ("v31", "v15", "reuses_kappa_phi_bridge", "proof"),
    ("v31", "sing_qg", "honest_boundary_unchanged", "honest"),
    ("v32", "v31", "continues_Q04_open", "new"),
    ("v32", "lambda", "lambda_is_weyl_boundary_const", "partial"),
    ("v32", "lambda_num", "cannot_derive_1e-106_residue", "honest"),
    ("v32", "v15", "reuses_kappa_phi_weyl_frame", "proof"),
    ("v32", "v18", "extends_cosmology_boundary", "partial"),
    ("v33", "v32", "parallel_boundary_anchor", "new"),
    ("v33", "v15", "audits_alpha_anchor_via_kappa_phi", "honest"),
    ("v33", "alpha_open", "alpha_is_pitch_ratio_underived", "partial"),
    ("v33", "n137_claim", "refutes_circular_derivation", "refute"),
    ("v33", "v28", "topo_invariants_too_small", "open"),
    ("v34", "v33", "summarizes_open_items", "new"),
    ("v34", "alpha_open", "confirms_anchor_underived", "honest"),
    ("v34", "lambda_num", "confirms_anchor_underived", "honest"),
    ("v35", "v34", "attacks_under_v34_anchors", "new"),
    ("v35", "v30", "deepens_generation_hierarchy_open", "honest"),
    ("v35", "v29", "uses_phi_SU2_3_dimension", "proof"),
    ("v35", "alpha_open", "anchor_input_not_deriving_group", "honest"),
    ("v35", "lambda_num", "anchor_input_not_deriving_hierarchy", "honest"),


    ("sim", "v10", "depends_on", "proof"),
    ("sim", "v18", "depends_on", "proof"),
    ("sim", "gravity", "reproduces", "proof"),
    ("sim", "em", "reproduces", "proof"),
    ("sim", "weak", "reproduces", "proof"),
    ("sim", "strong_res", "reproduces", "proof"),
    ("sim", "charge_q", "reproduces", "proof"),
    ("sim", "hubble", "reproduces", "proof"),
    ("sim", "scale_a", "reproduces", "proof"),
    ("sim", "sing_qg", "cannot_reproduce", "open"),
    ("sim", "lambda_num", "cannot_reproduce", "open"),
    ("sim", "confinement", "cannot_reproduce", "open"),
    ("sim", "alpha_open", "cannot_reproduce", "open"),
    ("sim", "dm_infl", "cannot_reproduce", "open"),
    ("viz", "sim", "depends_on", "proof"),
    ("viz", "unify_law", "visualizes", "proof"),
    ("viz", "friedmann", "visualizes", "proof"),
    ("viz", "charge_q", "visualizes", "proof"),
    ("viz", "sim", "visualizes", "proof"),
    # 诚实边界附着
    ("alpha_open", "v12", "open_boundary", "open"),
    ("confinement", "v10", "open_boundary", "open"),
    ("confinement", "v12", "open_boundary", "open"),
    ("dm_infl", "v18", "open_boundary", "open"),
    ("sing_qg", "v18", "open_boundary", "open"),
    ("lambda_num", "v18", "open_boundary", "open"),
]

TYPE_COLOR = {"version": "#4C72B0", "concept": "#55A868", "constant": "#DD8452",
              "tool": "#C44E52", "open": "#CCB974"}
CAT_COLOR = {"proof": "#4C72B0", "unify": "#55A868", "refute": "#C44E52",
             "partial": "#DD8452", "open": "#999999",
             "new": "#8172B2", "honest": "#937860"}
CAT_LINESTYLE = {"proof": "-", "unify": "-", "refute": "-", "partial": "--", "open": ":",
                 "new": "-.", "honest": (0, (5, 2))}

def build():
    G = nx.DiGraph()
    for nid, lab, zh, typ in NODES:
        G.add_node(nid, label=lab, zh=zh, type=typ)
    for s, t, rel, cat in EDGES:
        G.add_edge(s, t, relation=rel, category=cat)
    return G

def export_json(G, path):
    nodes = [{"id": n, "label": d["label"], "zh": d["zh"], "type": d["type"]}
             for n, d in G.nodes(data=True)]
    edges = [{"source": u, "target": v, "relation": d["relation"], "category": d["category"]}
             for u, v, d in G.edges(data=True)]
    by_type, by_rel, by_cat = {}, {}, {}
    for _, d in G.nodes(data=True):
        by_type[d["type"]] = by_type.get(d["type"], 0) + 1
    for _, _, d in G.edges(data=True):
        by_rel[d["relation"]] = by_rel.get(d["relation"], 0) + 1
        by_cat[d["category"]] = by_cat.get(d["category"], 0) + 1
    obj = {"graph_name": "统一场论知识图谱 v8-v18", "framework": "v8.1->v18 + 虚拟宇宙模拟器/可视化",
           "honest_note": "仅刻画已证内容与显式诚实边界；FAIL/部分闭合=自评标注非 bug",
           "stats": {"n_nodes": G.number_of_nodes(), "n_edges": G.number_of_edges(),
                     "by_type": by_type, "by_relation": by_rel, "by_category": by_cat},
           "nodes": nodes, "edges": edges}
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(obj, fp, ensure_ascii=False, indent=2)
    return obj

def export_graphml(G, path):
    H = nx.DiGraph()
    for n, d in G.nodes(data=True):
        H.add_node(n, label=d["label"], zh=d["zh"], type=d["type"])
    for u, v, d in G.edges(data=True):
        H.add_edge(u, v, relation=d["relation"], category=d["category"])
    try:
        nx.write_graphml(H, path)
        return True
    except Exception as e:
        print("  [warn] graphml 写出失败:", e); return False

def draw(G, path):
    pos = nx.spring_layout(G, k=1.6, iterations=300, seed=42, weight=None)
    fig, ax = plt.subplots(figsize=(16, 12))
    # 边
    for cat in ["proof", "unify", "refute", "partial", "open", "new", "honest"]:
        es = [(u, v) for u, v, d in G.edges(data=True) if d["category"] == cat]
        if not es: continue
        nx.draw_networkx_edges(G, pos, edgelist=es, ax=ax,
                               edge_color=CAT_COLOR[cat], style=CAT_LINESTYLE[cat],
                               alpha=0.55, arrows=True, arrowsize=10, node_size=900)
    # 节点
    for typ, col in TYPE_COLOR.items():
        ns = [n for n, d in G.nodes(data=True) if d["type"] == typ]
        if not ns: continue
        sz = [600 + 380 * G.degree(n) for n in ns]
        nx.draw_networkx_nodes(G, pos, nodelist=ns, ax=ax, node_color=col,
                               node_size=sz, edgecolors="white", linewidths=1.2)
    labels = {n: d["label"] for n, d in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=7.5, font_color="black")
    # 图例
    type_handles = [mpatches.Patch(color=c, label=t) for t, c in TYPE_COLOR.items()]
    cat_handles = [mpatches.Patch(color=CAT_COLOR[c],
                   label=f"{c} ({'solid' if CAT_LINESTYLE[c]=='-' else 'dashed/dotted'})")
                   for c in CAT_COLOR]
    ax.legend(handles=type_handles + cat_handles, loc="lower left", fontsize=8, framealpha=0.9)
    ax.set_title("Unified Field Theory Knowledge Graph (v8.1 -> v18 + virtual universe)",
                 fontsize=14)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=130); plt.close(fig)

def write_md(G, obj, path):
    L = []
    L.append("# 统一场论知识图谱 (v8.1 → v18 + 虚拟宇宙模拟器/可视化)\n")
    L.append(f"- 节点数 {obj['stats']['n_nodes']}，边数 {obj['stats']['n_edges']}")
    L.append(f"- 类型分布: {obj['stats']['by_type']}")
    L.append(f"- 关系类别分布: {obj['stats']['by_category']}\n")
    L.append("## 节点（按类型）")
    for typ in ["version", "tool", "concept", "constant", "open"]:
        L.append(f"\n### {typ}")
        for n, d in G.nodes(data=True):
            if d["type"] == typ:
                deg = G.degree(n)
                L.append(f"- `{n}` — {d['zh']}（度 {deg}）")
    L.append("\n## 关系边（按类别）")
    for cat in ["proof", "unify", "refute", "partial", "open", "new", "honest"]:
        L.append(f"\n### {cat}")
        for u, v, d in G.edges(data=True):
            if d["category"] == cat:
                L.append(f"- {G.nodes[u]['zh']} --{d['relation']}--> {G.nodes[v]['zh']}")
    L.append("\n## 诚实边界簇（open）")
    L.append("- 以下为框架显式标注的『未能第一性推导/未能还原』项，非 bug：")
    for n, d in G.nodes(data=True):
        if d["type"] == "open":
            outs = [G.nodes[v]['zh'] for _, v, dd in G.out_edges(n, data=True) if dd['relation']=='open_boundary']
            L.append(f"  - {d['zh']} → 边界附着: {outs if outs else '（v18 本源/模拟器诚实开放）'}")
    L.append("\n## 红线")
    L.append("- 图谱仅刻画 v8-v18 已证内容与显式诚实边界；不粉饰、不声称 100% 还原真实宇宙。")
    with open(path, "w", encoding="utf-8") as fp:
        fp.write("\n".join(L))

def main():
    print("=" * 70); print("统一场论知识图谱化"); print("=" * 70)
    G = build()
    jp = os.path.join(HERE, "统一场论_知识图谱.json")
    mp = os.path.join(HERE, "统一场论_知识图谱.md")
    gp = os.path.join(HERE, "统一场论_知识图谱.graphml")
    fp = os.path.join(FIGDIR, "fig_knowledge_graph.png")
    obj = export_json(G, jp)
    ok_gml = export_graphml(G, gp)
    draw(G, fp)
    write_md(G, obj, mp)
    print(f"  节点 {obj['stats']['n_nodes']}  边 {obj['stats']['n_edges']}")
    print(f"  类型 {obj['stats']['by_type']}")
    print(f"  关系类别 {obj['stats']['by_category']}")
    print(f"  [产物] {os.path.relpath(jp, HERE)}")
    print(f"  [产物] {os.path.relpath(mp, HERE)}")
    print(f"  [产物] {os.path.relpath(gp, HERE) if ok_gml else '(graphml 跳过)'}")
    print(f"  [图片] {os.path.relpath(fp, HERE)}")

if __name__ == "__main__":
    main()
