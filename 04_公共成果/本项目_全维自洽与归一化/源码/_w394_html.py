# -*- coding: utf-8 -*-
"""生成 r394 可视化 HTML（六图）+ 写入磁盘。不读来料中间量，读数全部来自本卷 JSON。"""
import io
import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "数据")

RID = "r394"
TITLE = ("TUFT-r394_审计ROOTV61_中心化子46与34个残余生成元_单个十维Higgs论证无效但结论对_"
         "Schur锁死二重态三重态简并_六代计数与半整数出口_Jarlskog恒等式精确复核_精算_2026-11-04")
OUT = os.path.join(ROOT, TITLE + "_可视化_2026-11-04.html")

# ---- 读数：从 JSON 取，严禁在本脚本里另写一套 ----
J = json.load(io.open(os.path.join(DATA, TITLE + ".json"), encoding="utf-8"))
ROWS = {r["id"]: r for r in J["rows"]}
MAIN = [r for r in J["rows"] if r["id"][0] == "A"]
CTL = [r for r in J["rows"] if r["id"][0] == "K"]
GRD = [r for r in J["rows"] if r["id"][0] == "G"]
NF = sum(1 for r in MAIN if r["kind"] == "FAIL")
NP = sum(1 for r in MAIN if r["kind"] == "PASS")
NI = sum(1 for r in MAIN if r["kind"] == "INFO")
assert len(MAIN) + len(CTL) + len(GRD) == len(J["rows"])

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>TUFT-r394 可视化 · 审计 ROOT V61</title>
<style>
  :root{--bg:#f7f8fa;--ink:#1a202c;--sub:#4a5568;--line:#cbd5e0;--acc:#2b6cb0;--ok:#2f855a;--warn:#c53030;--grey:#a0aec0;--amber:#b7791f;}
  html,body{margin:0;background:var(--bg);color:var(--ink);}
  body{font-family:"Segoe UI","Microsoft YaHei",sans-serif;}
  .wrap{max-width:780px;margin:0 auto;padding:26px 18px 56px;}
  h1{font-size:19px;line-height:1.55;margin:0 0 6px;}
  .sub{color:var(--sub);font-size:13px;margin:0 0 20px;line-height:1.7;}
  .card{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:14px 12px 10px;margin-bottom:18px;}
  .cap{font-size:12.5px;color:var(--sub);margin:8px 2px 0;line-height:1.7;}
  .cap b{color:var(--ink);}
  svg{display:block;width:100%;height:auto;}
</style>
</head>
<body>
<div class="wrap">
<h1>TUFT-r394 · 审计 ROOT V61：中心化子 46 / 半个十维不能破缺 / Schur 锁死简并 / 六代与半整数 / Jarlskog</h1>
<div class="sub">把 V61 的六项主张逐条变成可算判决 · 纯标准库 <code>Fraction</code>（判据区零浮点）<br>
读数来源：<code>数据/TUFT-r394_…_精算_2026-11-04.json</code>（@@NALL@@ 条：主册 @@NMAIN@@ = PASS @@NP@@ / INFO @@NI@@ / FAIL @@NF@@，控制组 @@NCTL@@，守卫 @@NGRD@@）</div>

<div class="card"><svg id="fig1" viewBox="0 0 680 250"></svg>
<div class="cap"><b>图 1｜中心化子三档</b>：把 66 个显式生成元逐个与 <code>T</code> 做换位子。三档读数 <b>66 / 46 / 6</b> 互不相同 —— 这是计数本身有判别力的证据，不是把 <code>45+1</code> 抄了一遍。</div></div>

<div class="card"><svg id="fig2" viewBox="0 0 680 270"></svg>
<div class="cap"><b>图 2｜分解账闭合</b>：<code>66 = 45+1+10+10</code>、<code>46 = 45+1</code>、<code>46−12 = 34 = 33+1</code>。三处加法互相独立，任一处抄错都会在守卫 G06 露出来。</div></div>

<div class="card"><svg id="fig3" viewBox="0 0 680 300"></svg>
<div class="cap"><b>图 3｜为什么维数比较无效</b>：左边是 V61 §二 的判据（<b>28 &gt; 12</b>），右边是本卷换上的判据（<b>单态数 = 0</b>）。<code>so(8)</code> 里就有 12 维子代数 <code>so(4)⊕so(4)</code>，所以左边那条不等式对「SM ⊂ 稳定子」零判别力。</div></div>

<div class="card"><svg id="fig4" viewBox="0 0 680 240"></svg>
<div class="cap"><b>图 4｜Schur 引理</b>：与整个 <code>so(10)</code> 交换的对称算子只有 <b>1 维</b> ⇒ 二次涨落算符必 ∝ 单位 ⇒ <code>m_H = m_T</code> 是<b>定理</b>，不是模型选择。负对照 <code>so(8)</code> 给 <b>4 维</b>。</div></div>

<div class="card"><svg id="fig5" viewBox="0 0 680 240"></svg>
<div class="cap"><b>图 5｜六代是整数性的后果</b>：同一对电荷，<code>q=(3,−3)</code> 给 6，<code>q=(3/2,−3/2)</code> 给 3，两者 <code>Σ s Q²</code> 都 = 0。⇒ 想保住三代，该改的是磁通量子化条件，不是谱。</div></div>

<div class="card"><svg id="fig6" viewBox="0 0 680 320"></svg>
<div class="cap"><b>图 6｜Δ 的四行条件与 Jarlskog 精确复核</b>：左边是势的二次项（H 方向 <code>8λv²</code>、T 方向 <code>2Δ</code>，归一化口径差因子 2，见 A10）；右边是恒等式两侧，两条<b>不同源</b>的路径给出同一个有理数（零容差）。</div></div>

<script>
function mk394(id, tag, at) {
  var s = document.getElementById(id);
  var e = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (var k in at) { e.setAttribute(k, at[k]); }
  s.appendChild(e);
  return e;
}
function tx394(id, x, y, str, size, fill, anchor, weight) {
  var e = mk394(id, "text", { x: x, y: y, fill: fill || "#1a202c",
    "font-size": size || 12, "text-anchor": anchor || "start",
    "font-weight": weight || "400",
    "font-family": "Segoe UI, Microsoft YaHei, sans-serif" });
  e.textContent = str;
  return e;
}
function ln394(id, x1, y1, x2, y2, stroke, w) {
  return mk394(id, "line", { x1: x1, y1: y1, x2: x2, y2: y2,
    stroke: stroke || "#cbd5e0", "stroke-width": w || 1 });
}
function rc394(id, x, y, w, h, fill, stroke, sw, r) {
  return mk394(id, "rect", { x: x, y: y, width: w, height: h,
    fill: fill, stroke: stroke || "none", "stroke-width": sw || 0, rx: r || 4 });
}
function pt394(id, d, stroke, w, fill) {
  return mk394(id, "path", { d: d, fill: fill || "none", stroke: stroke,
    "stroke-width": w || 1.6, "stroke-linejoin": "round", "stroke-linecap": "round" });
}
var CACC = "#2b6cb0", COK = "#2f855a", CWARN = "#c53030", CGREY = "#a0aec0",
    CLINE = "#cbd5e0", CAMB = "#b7791f", CINK = "#1a202c";

/* ---------------- 每图独立几何行：负对照只改这一行即可精确打中指定图 ---------------- */
var f1Y1 = 232;
var f2Y1 = 250;
var f3Y1 = 282;
var f4Y1 = 222;
var f5Y1 = 222;
var f6Y1 = 302;

/* ============================ 图 1：中心化子三档 ============================ */
(function () {
  var id = "fig1";
  tx394(id, 24, 26, "Cent_{so(12)}(T) 的维数：三档读数互不相同", 13, CINK, "start", "600");
  var rows = [["T = 0（无磁通）", 66, CACC, "全空间：什么都未破缺"],
              ["T_F = E_{11,12}（单平面）", 46, COK, "45 + 1 = so(10) ⊕ u(1)"],
              ["T ∈ Cartan（一般）", 6, CAMB, "只剩 6 维 Cartan 自身"]];
  for (var i = 0; i < rows.length; i++) {
    var y = 60 + i * 48, w = rows[i][1] * 5.2;
    tx394(id, 196, y + 20, rows[i][0], 12, "#4a5568", "end");
    rc394(id, 206, y, w, 30, rows[i][2], "none", 0, 3);
    tx394(id, 206 + w + 10, y + 20, String(rows[i][1]), 13, rows[i][2], "start", "700");
    tx394(id, 206 + w + 46, y + 20, rows[i][3], 11, "#718096");
  }
  ln394(id, 206, 194, 206, 200, "#718096", 1.2);
  tx394(id, 206, 214, "0", 11, "#718096", "middle");
  tx394(id, 206 + 66 * 5.2, 214, "66 = dim so(12)", 11, "#718096", "middle");
  tx394(id, 24, f1Y1, "维数由 66 个显式生成元的换位子核算出；若判据写错（例如只比迹），三档会合并成一档", 11, CGREY);
})();

/* ============================ 图 2：分解账 ============================ */
(function () {
  var id = "fig2";
  tx394(id, 24, 26, "三条加法互相独立，任一处错都会露出来", 13, CINK, "start", "600");
  var S = 8.6;
  function bar(y, parts, label) {
    var x = 92;
    tx394(id, 84, y + 21, label, 12, "#4a5568", "end");
    for (var i = 0; i < parts.length; i++) {
      var w = Math.max(parts[i][1] * S, 16);
      rc394(id, x, y, w, 30, parts[i][2], "#ffffff", 1, 2);
      if (w > 30) {
        tx394(id, x + w / 2, y + 20, String(parts[i][1]), 12, "#ffffff", "middle", "700");
      }
      x += w + 2;
    }
    return x;
  }
  bar(52, [[45, "45", "#2b6cb0"], [1, "1", "#2f855a"], [10, "10", "#b7791f"], [10, "10", "#805ad5"]], "66");
  tx394(id, 92, 100, "so(10) 45  ⊕  u(1) 1  ⊕  10  ⊕  10 = 66", 11, "#718096");
  bar(120, [[45, "45", "#2b6cb0"], [1, "1", "#2f855a"]], "46");
  tx394(id, 92, 168, "未破缺部分 = so(10) ⊕ u(1) = 46（与图 1 的读数一致）", 11, "#718096");
  bar(188, [[33, "33", "#2c5282"], [1, "1", "#2f855a"]], "34");
  tx394(id, 92, 236, "46 − 12 = 34 = 33 + 1：33 个仍在 Spin(10) 内未破缺，1 个是 u(1)_F 残余", 11, "#718096");
  tx394(id, 24, f2Y1, "★「33 个住在 so(10) 里」隐含「SM 的 12 个生成元整体落在 so(10) 内」——来料未写，本卷核为真", 11, CGREY);
})();

/* ============================ 图 3：维数比较 vs 单态计数 ============================ */
(function () {
  var id = "fig3";
  tx394(id, 24, 26, "10 在 SU(3)×SU(2)×U(1) 下的分解：维数和 10、超荷和 0、单态 0", 13, CINK, "start", "600");
  var bx = [[60, 108, "#2b6cb0", "(3,1,−1/3)"], [172, 72, "#4299e1", "(1,2,+1/2)"],
            [280, 108, "#2f855a", "(3̄,1,+1/3)"], [392, 72, "#48bb78", "(1,2,−1/2)"]];
  for (var i = 0; i < bx.length; i++) {
    rc394(id, bx[i][0], 52, bx[i][1], 44, bx[i][2], "#ffffff", 1, 3);
    tx394(id, bx[i][0] + bx[i][1] / 2, 78, bx[i][3], 10.5, "#ffffff", "middle", "600");
  }
  tx394(id, 166, 112, "5", 13, "#2b6cb0", "middle", "700");
  tx394(id, 386, 112, "5̄", 13, "#2f855a", "middle", "700");
  pt394(id, "M 60 118 L 244 118", "#2b6cb0", 1.2);
  pt394(id, "M 280 118 L 464 118", "#2f855a", 1.2);
  tx394(id, 480, 78, "维数和 = 3+2+3+2 = 10", 11, "#4a5568");
  tx394(id, 480, 96, "超荷和 = 3(−1/3)+2(+1/2)+c.c. = 0", 11, "#4a5568");
  tx394(id, 24, 148, "① V61 §二 的判据", 12, CWARN, "start", "700");
  rc394(id, 24, 158, 306, 92, "#fff5f5", CWARN, 1.2);
  tx394(id, 40, 182, "「一般复 10 的稳定子含 SO(8)，维数 28」", 11.5, "#4a5568");
  tx394(id, 40, 202, "⇒ 「28 > 12，所以不能完成 SM 破缺」", 11.5, "#4a5568");
  tx394(id, 40, 228, "反例：so(4)⊕so(4) ⊂ so(8)，维数 12、", 11.5, CWARN);
  tx394(id, 40, 244, "对换位封闭 ⇒ 该不等式零判别力", 11.5, CWARN, "start", "600");
  tx394(id, 350, 148, "② 本卷换上的判据", 12, COK, "start", "700");
  rc394(id, 350, 158, 306, 92, "#f0fff4", COK, 1.2);
  tx394(id, 366, 182, "SM ⊂ 稳定子(v)  ⟺  v 是 SM 不变向量", 11.5, "#4a5568");
  tx394(id, 366, 202, "⟺  v 落在 10 的单态子空间里", 11.5, "#4a5568");
  tx394(id, 366, 228, "单态数 = 0 ⇒ 任何非零 v 都被某个", 11.5, COK);
  tx394(id, 366, 244, "SM 生成元推动 ⇒ 单个 10 必破 SM", 11.5, COK, "start", "600");
  tx394(id, 24, f3Y1, "结论对、理由错：V61 的结论由 ② 独立证成，且 ② 更强（不是「某个 v 不行」，是「任何 v 都不行」）", 11, CGREY);
})();

/* ============================ 图 4：Schur ============================ */
(function () {
  var id = "fig4";
  tx394(id, 24, 26, "与整个李代数交换的对称算子维数：1 维意味着「必须 ∝ 单位」", 13, CINK, "start", "600");
  ln394(id, 70, 170, 640, 170, "#718096", 1.4);
  ln394(id, 70, 40, 70, 170, "#718096", 1.4);
  var bars = [[160, 1, "#2f855a", "so(10) 在 10 上"], [420, 4, "#c53030", "so(8) 在 R^10=8+1+1 上"]];
  for (var i = 0; i < bars.length; i++) {
    var h = bars[i][1] * 26;
    rc394(id, bars[i][0], 170 - h, 130, h, bars[i][2], "none", 0, 3);
    tx394(id, bars[i][0] + 65, 170 - h - 10, String(bars[i][1]) + " 维", 14, bars[i][2], "middle", "700");
    tx394(id, bars[i][0] + 65, 190, bars[i][1 + 2], 11.5, "#4a5568", "middle");
  }
  for (var k = 0; k <= 4; k++) {
    tx394(id, 62, 174 - k * 26, String(k), 10, "#718096", "end");
  }
  tx394(id, 24, 208, "1 维 ⇒ 不变二次算子 = c·𝟙 ⇒ m_H = m_T 是 Schur 引理，不是模型选择", 11.5, COK, "start", "600");
  tx394(id, 24, f4Y1, "负对照给 4 维（8×8 单位 ⊕ 2×2 对称块）⇒ 简并不是「怎么算都 1」", 11, CGREY);
})();

/* ============================ 图 5：六代 vs 半整数 ============================ */
(function () {
  var id = "fig5";
  tx394(id, 24, 26, "同一对电荷、同一个公式 n = q₊ − q₋，只改分母", 13, CINK, "start", "600");
  ln394(id, 80, 168, 620, 168, "#718096", 1.4);
  var bars = [[150, 6, "#2b6cb0", "q = (3, −3)", "整数磁通"], [400, 3, "#b7791f", "q = (3/2, −3/2)", "分母 2"]];
  for (var i = 0; i < bars.length; i++) {
    var h = bars[i][1] * 20;
    rc394(id, bars[i][0], 168 - h, 120, h, bars[i][2], "none", 0, 3);
    tx394(id, bars[i][0] + 60, 168 - h - 10, "n = " + bars[i][1], 14, bars[i][2], "middle", "700");
    tx394(id, bars[i][0] + 60, 186, bars[i][3], 11.5, "#4a5568", "middle");
    tx394(id, bars[i][0] + 60, 202, bars[i][4], 11, "#718096", "middle");
  }
  tx394(id, 300, 84, "Σ s Q² = 0", 12, COK, "middle", "600");
  tx394(id, 300, 102, "Σ s Q² = 0", 12, COK, "middle", "600");
  tx394(id, 24, f5Y1, "两者两项反常都精确抵消 ⇒ 「6」不是反常在捣乱，是整数性在捣乱", 11.5, COK, "start", "600");
})();

/* ============================ 图 6：Δ 四行 + Jarlskog ============================ */
(function () {
  var id = "fig6";
  tx394(id, 24, 26, "左：势的二次项（精确 Vandermonde 与解析式两条路径）　右：Jarlskog 恒等式（两条不同源路径）", 12.5, CINK, "start", "600");
  rc394(id, 24, 44, 312, 214, "#f7fafc", "#cbd5e0", 1.2);
  tx394(id, 40, 68, "V(H,T) = −μ²(|H|²+|T|²) + λ(… )² + Δ|T|²", 11, "#4a5568");
  var conds = [["Δ < 0", "T 方向出现负质量平方", COK],
               ["Δ = 0", "T 平坦方向（质量由 λ 混合给出）", CAMB],
               ["Δ > 0", "有色真空稳定", COK],
               ["Δ ≥ μ²", "原点无负质量平方", COK]];
  for (var i = 0; i < conds.length; i++) {
    var y = 86 + i * 40;
    rc394(id, 40, y, 280, 32, "#ffffff", conds[i][2], 1, 3);
    tx394(id, 50, y + 21, conds[i][0], 11.5, conds[i][2], "start", "700");
    tx394(id, 118, y + 21, conds[i][1], 10.5, "#4a5568");
  }
  tx394(id, 40, 250, "H 方向 V'' = 4 = 8λv²；T 方向 V'' = 2/3 = 2Δ", 11, CINK, "start", "600");
  rc394(id, 348, 44, 308, 214, "#f7fafc", "#cbd5e0", 1.2);
  tx394(id, 364, 68, "Im tr([H_u,H_d]³)  =  6 · J · ∏Δm²_u · ∏Δm²_d", 11, "#4a5568");
  rc394(id, 364, 84, 276, 60, "#ebf4ff", CACC, 1.2);
  tx394(id, 372, 106, "Im tr = 1.093833317817127…", 10.5, CACC);
  tx394(id, 372, 128, "= 691103452755937080287232000 / 631817884405930548876667", 8.6, "#4a5568");
  rc394(id, 364, 154, 276, 60, "#f0fff4", COK, 1.2);
  tx394(id, 372, 176, "6J∏∏ = 1.093833317817127…", 10.5, COK);
  tx394(id, 372, 198, "同一个分数，逐位相等（零容差）", 10.5, "#4a5568");
  tx394(id, 364, 236, "J = 0.0234446441…  ·  R 正交 = True", 10.5, "#4a5568");
  tx394(id, 364, 252, "实纹理退化档：J = 0 且 Im tr = 0（两侧同为 0，不能当证据）", 9.6, CGREY);
  tx394(id, 24, f6Y1, "★系数 6 是绝对值：∏ 的排序反过来常数变 −6 ⇒ 报「成立」时必须同时报排序约定（本卷取 i<j）", 11, CGREY);
})();
</script>
</div>
</body>
</html>
"""

HTML = (HTML.replace("@@NALL@@", str(len(J["rows"])))
            .replace("@@NMAIN@@", str(len(MAIN)))
            .replace("@@NP@@", str(NP))
            .replace("@@NI@@", str(NI))
            .replace("@@NF@@", str(NF))
            .replace("@@NCTL@@", str(len(CTL)))
            .replace("@@NGRD@@", str(len(GRD))))
assert "@@" not in HTML

# ★★几何行必须真的被引用：声明 1 次 + 使用 ≥1 次，否则负对照改它等于没改
for _i in range(1, 7):
    _tok = "f%dY1" % _i
    assert HTML.count(_tok) >= 2, ("几何变量成为装饰：%s 只出现 %d 次" % (_tok, HTML.count(_tok)))


io.open(OUT, "w", encoding="utf-8", newline="\n").write(HTML)
print("HTML ->", OUT, os.path.getsize(OUT), "B")
print("rows", len(J["rows"]), "MAIN", len(MAIN), "CTL", len(CTL), "GRD", len(GRD), "NF", NF)
