#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v25 交互式知识图谱（vis-network HTML）—— 把 TEGT 全链与开放项可视化

读取 知识图谱.py 生成的 统一场论_知识图谱.json（节点/边/开放项），
输出一个自包含的交互式 HTML（vis-network），支持：
  · 拖拽/缩放/悬停查看节点与边的语义（layer/kind/verdict）
  · 高亮开放项（mass_hier / lambda_problem / singularity 等红色节点）
  · 按版本分时着色（v8.1..v24 一条演进链）

这是『全维自动完成』的最后一公里：把全链的『已闭合 / 部分闭合 / 诚实开放』以可交互形式呈现，
便于敏感性分析（点击开放项查看其上游依赖与下游影响）。
"""
from __future__ import annotations
import sys, os, json
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "统一场论_知识图谱.json")
OUT = os.path.join(HERE, "统一场论_交互式知识图谱.html")

def main():
    with open(SRC, "r", encoding="utf-8") as fp:
        G = json.load(fp)
    nodes = G.get("nodes", [])
    edges = G.get("edges", [])
    # 版本着色
    def vcolor(vid):
        try:
            num = int(str(vid).lstrip("v"))
        except Exception:
            return "#888"
        import colorsys
        h = (num % 24) / 24.0
        r, g, b = colorsys.hsv_to_rgb(h, 0.55, 0.85)
        return "#%02x%02x%02x" % (int(r*255), int(g*255), int(b*255))
    # 开放项判定（红色高亮）
    open_ids = set()
    for n in nodes:
        if n.get("kind") in ("honest", "open") or "open" in str(n.get("id", "")).lower():
            open_ids.add(n["id"])
    # 也把 mass_hier 等显式标红
    for n in nodes:
        i = str(n.get("id", "")).lower()
        if any(k in i for k in ("mass", "hier", "lambda", "singul", "qcd", "alpha", "dark", "inflat", "neutr")):
            open_ids.add(n["id"])
    nodes_js = []
    for n in nodes:
        nid = n["id"]
        is_open = nid in open_ids
        color = "#e74c3c" if is_open else vcolor(nid)
        title = f"id={nid}\\nkind={n.get('kind','')}\\nlayer={n.get('layer','')}"
        nodes_js.append("{%s}" % ", ".join([
            "id: %s" % json.dumps(nid),
            "label: %s" % json.dumps(n.get("label", nid)),
            "color: { background: %s, border: %s }" % (json.dumps(color), json.dumps("#333" if is_open else "#555")),
            "title: %s" % json.dumps(title),
            "font: { color: %s }" % json.dumps("#000" if not is_open else "#fff"),
        ]))
    edges_js = []
    for e in edges:
        edges_js.append("{%s}" % ", ".join([
            "from: %s" % json.dumps(e["source"]),
            "to: %s" % json.dumps(e["target"]),
            "label: %s" % json.dumps(e.get("relation", "")),
            "arrows: 'to'",
            "color: { color: %s }" % json.dumps("#bbb"),
            "font: { size: 10, color: '#666' }",
        ]))
    html = """<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>统一场论 TEGT 交互式知识图谱</title>
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>body{font-family:system-ui,'Microsoft YaHei',sans-serif;margin:0;background:#fafafa}
#header{padding:10px 16px;background:#fff;border-bottom:1px solid #ddd}
#net{width:100vw;height:calc(100vh - 64px)}
.legend{font-size:12px;color:#555;margin-left:12px}
.red{color:#e74c3c;font-weight:bold}</style></head>
<body>
<div id="header"><b>统一场论 TEGT 交互式知识图谱（v8.1 → v29）</b>
<span class="legend"> 节点颜色=版本演进； <span class="red">红色=诚实开放项（mass_hier / Λ / 奇点 / QCD / α / 暗物质…）</span>；拖拽/缩放/悬停查看细节。</span></div>
<div id="net"></div>
<script>
const nodes = new vis.DataSet([NODES]);
const edges = new vis.DataSet([EDGES]);
const container = document.getElementById('net');
const data = { nodes, edges };
const options = {
  layout: { improvedLayout: true },
  physics: { stabilization: true, barnesHut: { gravitationalConstant: -8000, springLength: 120 } },
  interaction: { hover: true, tooltipDelay: 80, navigationButtons: true, keyboard: true },
  edges: { smooth: { enabled: true, type: 'cubicBezier', roundness: 0.4 } }
};
new vis.Network(container, data, options);
</script></body></html>"""
    html = html.replace("[NODES]", ",\n".join(nodes_js)).replace("[EDGES]", ",\n".join(edges_js))
    with open(OUT, "w", encoding="utf-8") as fp:
        fp.write(html)
    # 主链聚合用 JSON 摘要
    summ = dict(suite="统一场论 v25 · 交互式知识图谱（vis-network）", date="2026-09-05",
                new_system="自包含 vis-network HTML，节点版本着色、开放项标红、可拖拽/缩放/悬停",
                total=len(nodes), edges=len(edges), open_items=sorted(open_ids),
                results=[dict(id="v25_html", name="交互式知识图谱 HTML 生成", layer="可视化", kind="工程",
                               verdict="PASS", sym="vis-network", num=f"{len(nodes)} nodes / {len(edges)} edges",
                               note="全链 v8.1→v24 与开放项的可交互呈现，便于敏感性分析。")])
    with open(os.path.join(HERE, "v25_交互式知识图谱_核验结果.json"), "w", encoding="utf-8") as fp:
        json.dump(summ, fp, ensure_ascii=False, indent=2)
    print(f"节点数={len(nodes)} 边数={len(edges)} 开放项标红={len(open_ids)}")
    print(f"交互式知识图谱已写入: {os.path.basename(OUT)}")
    print(f"  开放项 id: {sorted(open_ids)}")

if __name__ == "__main__":
    main()
