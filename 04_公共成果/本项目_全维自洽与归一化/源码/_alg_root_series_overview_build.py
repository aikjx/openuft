# -*- coding: utf-8 -*-
"""全维整理总览生成器：从六册 JSON 机读判词/门数，生成总览 HTML（避免手抄漂移）。"""
import os
import glob
import json
from datetime import date

ROOT = glob.glob(os.path.join("openuft", "**", "_ALG_rootv77_Gc_relation_audit_recompute_2026-11-18.json"),
                 recursive=True)
assert len(ROOT) == 1, ROOT
DATA = os.path.dirname(ROOT[0])
MAIN = os.path.dirname(DATA)
OUT = os.path.join(MAIN, "算法联盟_ROOT系列六册全维整理总览_2026-11-18.html")

SPECS = [
    {
        "file": "_ALG_rootv83_gravity_audit_recompute_2026-11-18.json",
        "tag": "V83",
        "name": "双传感器引力调制与电磁零实验",
        "focus": "奇偶对称性判别力",
        "negative": "奇偶对称性对任意偶中心力恒等 → 对识别引力模型判别力 = 0",
        "positive": "倾斜共模可翻转诊断（odd=2gθ，even 相消）",
        "external": "冷原子测 G（Nature 2014）一手补齐",
        "md": "算法联盟_ROOTV83双传感器引力调制可算审计_2026-11-18.md",
        "html": "算法联盟_ROOTV83双传感器引力调制可算审计_可视化_2026-11-18.html",
    },
    {
        "file": "_ALG_rootv79_frequency_audit_recompute_2026-11-18.json",
        "tag": "V79",
        "name": "变化电磁场的频率选择规律",
        "focus": "2f 谐波判别力",
        "negative": "B² 的 2f 是三角恒等式（27/27 残差 0）→ 判别力 = 0",
        "positive": "频率筛选只在模型层；需实测 f/2f 双分量才生效",
        "external": "Tajmar 2024 稳态零结果 → 约束域错位，非对时变主张判负",
        "md": "算法联盟_ROOTV79变化电磁场频率选择可算审计_2026-11-18.md",
        "html": "算法联盟_ROOTV79变化电磁场频率选择可算审计_可视化_2026-11-18.html",
    },
    {
        "file": "_ALG_rootv77_Gc_relation_audit_recompute_2026-11-18.json",
        "tag": "V77",
        "name": "万有引力常数 G 与光速 c 的关系",
        "focus": "定义重排识别",
        "negative": "五个 G 关系式全是定义重排（5/5）→ 仅凭 c 推不出 G",
        "positive": "错误 G 反例 flip：电子 44.8、质子 38.2、普朗克质量 0 数量级",
        "external": "CODATA 2022（NIST SP 961）一手补齐；不制造假阳性错误",
        "md": "算法联盟_ROOTV77_G与c关系可算审计_2026-11-18.md",
        "html": "算法联盟_ROOTV77_G与c关系可算审计_可视化_2026-11-18.html",
    },
    {
        "file": "_ALG_rootcore_Gorigin_audit_recompute_2026-11-18.json",
        "tag": "CORE",
        "name": "ROOT 核心问题：G 从哪来 / 四力为何未统一",
        "focus": "量纲唯一性 + 证明链断点",
        "negative": "G=C c³ℓ²/ħ 量纲唯一但参数不灭（ℓ_P 循环 / 其余偏离 39–49 dex）",
        "positive": "证明链断点定位第 4 步；四力状态 4/4 与一手及 r403 一致",
        "external": "CERN W/Z + LEP 精密检验；Donoghue 1994 GR-EFT；CODATA G",
        "md": "算法联盟_ROOT核心问题_G来源与四力统一可算审计_2026-11-18.md",
        "html": "算法联盟_ROOT核心问题_G来源与四力统一可算审计_可视化_2026-11-18.html",
    },
    {
        "file": "_ALG_rootv88_planetary_G_audit_recompute_2026-11-18.json",
        "tag": "V88",
        "name": "每个星球的基本 G 是否不同",
        "focus": "μ=GM 不可辨识 + 恒等式",
        "negative": "g 两式定义恒等（4/4）→ 表面引力差异不需不同 G（判别力 0）",
        "positive": "μ 简并 flip：G×k/M÷k 同一 μ；须独立 M 才解出 G",
        "external": "MICROSCOPE η 精确匹配 PRL 2022；只约束 WEP 组成依赖，不覆盖行星环境",
        "md": "算法联盟_每星球G是否不同可算审计_2026-11-18.md",
        "html": "算法联盟_每星球G是否不同可算审计_可视化_2026-11-18.html",
    },
    {
        "file": "_ALG_rootv85_dual_invariant_audit_recompute_2026-11-18.json",
        "tag": "V85",
        "name": "G 来源、星球差异与双不变量（Q / rank D）",
        "focus": "形状恒等式 + 秩判据",
        "negative": "Q 对 GM 幅度零判别力：看不见各星球常数 G 差异；"
                    "Q 偏离可来自多极矩；纯系统误差也满足 rank≤1",
        "positive": "Q=1 ⇔ 幂律 n=2（两路 ≤1.2E-16）；单媒介 9 子式精确全零，"
                    "两媒介 flip 到 0.4162",
        "external": "MICROSCOPE 2022（沿用 V88，不相加）+ RMP 81,61 的 Yukawa/ISL 综述；"
                    "两项精算示例均为人为模型存在性复现，非实测",
        "md": "算法联盟_ROOTV85双不变量可算审计_2026-11-18.md",
        "html": "算法联盟_ROOTV85双不变量可算审计_可视化_2026-11-18.html",
    },
]

books = []
for s in SPECS:
    p = os.path.join(DATA, s["file"])
    d = json.load(open(p, encoding="utf-8"))
    s["verdict"] = d["verdict"]
    s["gates"] = "%s/%s" % (d["n_gate_ok"], d["n_gate_total"])
    s["red"] = d["red_line"]
    books.append(s)

total_gates = sum(int(b["gates"].split("/")[0]) for b in books)
total_n = sum(int(b["gates"].split("/")[1]) for b in books)

rows = "\n".join(
    """    <tr>
      <td><b>%s</b><br><span class="src">%s</span></td>
      <td>%s</td>
      <td class="num">%s</td>
      <td><span class="negdot"></span>%s</td>
      <td><span class="posdot"></span>%s</td>
    </tr>""" % (b["tag"], b["name"], b["focus"], b["gates"], b["negative"], b["positive"])
    for b in books)

verdicts = "\n".join(
    """    <div class="vcard">
      <div class="vt">%s · %s</div>
      <div class="vcode">%s</div>
      <div class="vlink"><a href="%s">审计册</a> · <a href="%s">可视化</a></div>
    </div>""" % (b["tag"], b["name"].replace("&", "&amp;"), b["verdict"], b["md"], b["html"])
    for b in books)

ext_rows = "\n".join(
    """    <tr><td><b>%s</b></td><td>%s</td></tr>""" % (b["tag"], b["external"])
    for b in books)

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>算法联盟 · ROOT 系列六册全维整理总览 · 2026-11-18</title>
<style>
  :root{--bg:#f7f8fa;--panel:#fff;--ink:#1a2230;--sub:#5a6675;--line:#dfe3ea;
        --accent:#2540a6;--ok:#137a4b;--okbg:#e7f6ee;--neg:#a12a2a;--negbg:#fdecec;
        --warn:#8a5a00;--warnbg:#fff6e0;--code:#0f2d5c}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
       font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
       line-height:1.65;font-size:15px}
  .wrap{max-width:1120px;margin:0 auto;padding:34px 22px 70px}
  header{border-left:5px solid var(--accent);padding:6px 0 6px 18px;margin-bottom:26px}
  h1{font-size:26px;margin:0 0 6px}
  .meta{color:var(--sub);font-size:13px}
  section{background:var(--panel);border:1px solid var(--line);border-radius:12px;
          padding:20px 22px;margin-bottom:18px}
  h2{font-size:18px;margin:0 0 14px;color:var(--accent)}
  p{margin:8px 0}
  .stat{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:6px 0 2px}
  .scard{background:#fbfcfe;border:1px solid var(--line);border-radius:10px;padding:14px;text-align:center}
  .scard .n{font-size:23px;font-weight:700;color:var(--accent)}
  .scard .l{font-size:12px;color:var(--sub);margin-top:4px}
  table{width:100%;border-collapse:collapse;margin:10px 0;font-size:13.3px}
  th,td{border-bottom:1px solid var(--line);padding:9px 10px;text-align:left;vertical-align:top}
  th{background:#f3f5f9;color:var(--sub);font-weight:600}
  td.num{font-family:ui-monospace,Menlo,Consolas,monospace;color:var(--code);white-space:nowrap}
  .src{font-size:12px;color:var(--sub)}
  .src a{color:var(--accent)}
  .negdot,.posdot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}
  .negdot{background:#a12a2a}.posdot{background:#137a4b}
  .vgrid{display:grid;grid-template-columns:1fr;gap:10px}
  .vcard{background:#fbfcfe;border:1px solid var(--line);border-radius:9px;padding:12px 14px}
  .vt{font-size:13px;font-weight:600;margin-bottom:6px}
  .vcode{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.2px;color:var(--code);
         background:#eef1f7;padding:6px 8px;border-radius:5px;word-break:break-all}
  .vlink{font-size:12.5px;margin-top:7px}
  .vlink a{color:var(--accent);text-decoration:none}
  .flow{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:13px}
  .step{background:#eef1fb;border:1px solid #c9d4f5;color:var(--code);
        border-radius:8px;padding:7px 11px}
  .arrow{color:var(--sub)}
  .note{background:var(--warnbg);border-left:4px solid #d8a11a;padding:10px 14px;
        border-radius:6px;font-size:13.5px;color:#5a4200;margin:12px 0}
  .flip{background:var(--okbg);border-left:4px solid var(--ok);padding:10px 14px;
        border-radius:6px;font-size:13.5px;color:#0d5636;margin:12px 0}
  footer{color:var(--sub);font-size:12px;text-align:center;margin-top:24px}
  @media(max-width:820px){.stat{grid-template-columns:repeat(2,1fr)}}
</style>
</head>
<body>
<div class="wrap">

<header>
  <h1>算法联盟 · ROOT 系列六册全维整理总览</h1>
  <div class="meta">CORE / V77 / V79 / V83 / V85 / V88 · 2026-11-18 · 非判定册索引，不占 RID，不入 README，六册结论不相加</div>
</header>

<section>
  <h2>总览统计（机读自六册 JSON）</h2>
  <div class="stat">
    <div class="scard"><div class="n">__N_BOOKS__</div><div class="l">审计册（机读）</div></div>
    <div class="scard"><div class="n">__TOTAL_GATES__</div><div class="l">判据 ok / 总数</div></div>
    <div class="scard"><div class="n">0</div><div class="l">独立实验预言</div></div>
    <div class="scard"><div class="n">0</div><div class="l">宣称攻破统一场论</div></div>
  </div>
  <div class="flow" style="margin-top:14px">
    <span class="step">具体对象</span><span class="arrow">→</span>
    <span class="step">两路独立复算</span><span class="arrow">→</span>
    <span class="step">恒等式 / 定义重排识别</span><span class="arrow">→</span>
    <span class="step">可翻转判据 + 反例</span><span class="arrow">→</span>
    <span class="step">外部一手 URL 裁决</span><span class="arrow">→</span>
    <span class="step">红线边界</span>
  </div>
  <p class="src" style="margin-top:12px">统一范式：具体模型 × 外部一手读数 × 可翻转判据 × 外部裁决。六册共用，不产六件套、不自盖章。</p>
</section>

<section>
  <h2>六册对照：负读数与正读数</h2>
  <table>
    <tr><th>册 / 对象</th><th>判别焦点</th><th>判据</th><th>负读数（判别力 0 / 域错位）</th><th>正读数（可翻转 / 有效部分）</th></tr>
    __ROWS__
  </table>
</section>

<section>
  <h2>机读判词（取自各册 JSON，非手抄）</h2>
  <div class="vgrid">
__VERDICTS__
  </div>
</section>

<section>
  <h2>外部一手核查汇总</h2>
  <table>
    <tr><th>册</th><th>核查结论</th></tr>
    __EXTROWS__
  </table>
  <div class="note">六册来料均只附 favicon 图标链接（google favicon 服务），那不是论文或数据表来源。本系列一律补齐一手 DOI / URL 供外部核查——这是 11-16 方向自审后确立的纪律。</div>
</section>

<section>
  <h2>共享结论与未关闭边界</h2>
  <p><b>六册共同指向：</b>来料提供的是<b>前提明确的恒等式、定义重排与可复现工程</b>——数值与结构全部可独立复算，但恒等式与定义重排无论验证多少次，都不增加关于引力理论或 G 本源的信息量。六册各找到一个"零判别力/参数不灭"结构（奇偶对称性 / 2f 三角恒等式 / 五个 G 关系式 / g 两式恒等 / G=C c³ℓ²/ħ 量纲结构 / Q 对 GM 幅度盲），并各找到一个"可翻转但有限"的有效部分（倾斜诊断 / 模型层频率筛选 / 错误 G 反例 / μ 简并 / 证明链断点定位 / 秩判据两媒介 flip）。</p>
  <div class="flip"><b>未关闭的真正战场（按外部读数驱动，非按册数驱动）：</b>
    ① V83：高频域双传感器同时测 f/2f 奇偶信号 + 电磁零实验；
    ② V79：在受控电磁调制下测 δG/G 并给系统误差预算，让 G5 判词有机会翻转；
    ③ V77：零输入推导 Z / l_P / α_g 之一，且给可证伪读数，不再由实测 G 反向定义；<br>
    ④ V88：给独立质量信息打破 μ=GM 简并，并把 δ(ρ,T,B,组成) 升级为可推导可证伪函数，用地球—月球—太阳—木星—中子星联合观测寻找不可被质量分布解释的残差；<br>
    ⑤ CORE：点亮证明链第 4 步——找到不含 G 的微观作用量，独立确定 C_micro 与 ℓ_micro，使 G_predicted 落入可证伪区间；<br>
    ⑥ V85：多半径测 g(r) 并先扣多极矩/自转/相对论项，再报 Q 的误差棒；同时用独立材料与源荷标定区分「单媒介」与「共模系统误差」——否则 rank≤1 通过不携带模型信息。
    结果更新时重跑对应机核，让判词真的有机会改变。</div>
  <p><b>红线：</b>__RED__</p>
  <p class="src">纪律：非判定册 · 不占 RID · 不入 README · 不回写既有产物 · 两路机拼 · 反噬只动一个判据 · flip 演示 · 幂等复跑 · 来源给一手 URL · 不制造假阳性出处错误 · 门限数据驱动。</p>
</section>

<footer>
  算法联盟 · ROOT 系列六册全维整理总览 · 2026-11-18　|　判词/门数机读自六册 JSON　|　数学自洽 ≠ 实验证实
</footer>

</div>
</body>
</html>
"""

HTML = (HTML.replace("__N_BOOKS__", str(len(books)))
            .replace("__TOTAL_GATES__", "%s/%s" % (total_gates, total_n))
            .replace("__ROWS__", rows)
            .replace("__VERDICTS__", verdicts)
            .replace("__EXTROWS__", ext_rows)
            .replace("__RED__", books[0]["red"]))
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(HTML)
print("OUT =", OUT, os.path.getsize(OUT), "B", "gates", total_gates, "/", total_n)
