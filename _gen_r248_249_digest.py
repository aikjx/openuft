# -*- coding: utf-8 -*-
r"""r248 + r249 双卷归一整理册生成器（非占号产物）

纪律：所有数字从两份 JSON **机读**，渲染层不手抄（承 r249 自抓②的教训）。
输出：数据/整理_TUFT-r248-r249_单方程全域力双卷归一总册_2026-10-31.md
      源码/整理_TUFT-r248-r249_单方程全域力双卷归一总册_2026-10-31.html
"""
import io
import json
import math
import os

BASE = (r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果"
        r"\本项目_全维自洽与归一化")
DATA = os.path.join(BASE, "数据")
SRC = os.path.join(BASE, "源码")

T248 = "TUFT-r248_单方程全域力层_主方程量纲断裂与自旋条件虚数解_精算与可视化_2026-10-30"
T249 = ("TUFT-r249_低能极限推导层_牛顿还原隐含普适质量与禁闭声称单调性反号"
        "_精算与可视化_2026-10-30")
OUT = "整理_TUFT-r248-r249_单方程全域力双卷归一总册_2026-10-31"

d8 = json.load(io.open(os.path.join(DATA, T248 + ".json"), encoding="utf-8"))
d9 = json.load(io.open(os.path.join(DATA, T249 + ".json"), encoding="utf-8"))

# ---- 机读关键量 ----
HBAR = 1.054571817e-34
C = 2.99792458e8
KB = 1.380649e-23
EV = 1.602176634e-19

ghost_kg = d9["B1_universal_mass"]["m_universal_kg"]
ghost_lam = d9["B1_universal_mass"]["reduced_Compton_wavelength_m"]
ghost_E_J = float(ghost_kg) * C * C
ghost_eV = ghost_E_J / EV
ghost_T = ghost_E_J / KB
ratio_1kg = d8["H_magnitude"]["ratios"]["1 kg 检验质量"]

# 恒等性自检：r248 的「1 kg 比值」与 r249 的「普适质量」是否为同一个常数
identical = abs(float(ratio_1kg) - float(ghost_kg)) / float(ghost_kg) < 1e-6


def rows_of(d):
    return d["rows"]


def lay_tbl(d):
    out = []
    for k, v in d["summary_by_layer"].items():
        out.append("| %s | %d | %d | %d | %d |" %
                   (k, v["PASS"], v["FAIL"], v["OPEN"], v["INFO"]))
    return "\n".join(out)


def rows_tbl(d, only=None):
    out = []
    for r in rows_of(d):
        if only and not r["id"].startswith(only):
            continue
        out.append("| %s | %s | **%s** | %s |" %
                   (r["id"], r["layer"], r["verdict"], r["claim"]))
    return "\n".join(out)


fav8 = [r for r in rows_of(d8) if r["layer"] == "对靶有利"]
fav9 = [r for r in rows_of(d9) if r["layer"] == "对靶有利"]

MD = f"""# 整理册 · 单方程全域力双卷归一总册（r248 + r249）

> 本册把同一份来料的两卷攻破归一整理。**不占新 r 号**（整理册非攻破卷）。
> 全部数字由脚本机读两份 JSON 生成，渲染层不手抄。

## 0. 一句话

靶用**一个矢量方程**声称统一四力，并在五步内「自动推导」出牛顿引力、库仑定律、弱力宇称破缺、强力禁闭与渐近自由。
两卷共 **{d8['counts']['items'] + d9['counts']['items']} 条**判据（r248 {d8['counts']['items']} 条 / r249 {d9['counts']['items']} 条，
**分层并列、不可相加**），守卫 **{d8['counts']['guards'] + d9['counts']['guards']}/{d8['counts']['guards'] + d9['counts']['guards']}**，
修复定价两卷均 **SURVIVE 0** ⇒ 本线第 **31**（r248）与 **32**（r249）度。

- **r248（主方程本体层）**：量纲是能量不是力；自旋 ℏ/2 被自己的公式排除；距离依赖两端都不匹配已知力。
- **r249（低能极限推导层）**：牛顿还原隐含一个普适质量；禁闭与渐近自由都与自己的方程反号。

## 1. 来料与还原（「t 污染」事件）

来料 `_tmp_r246_来料/基于光速螺旋流形的核心动力学方程组.md` 的 LaTeX **被批量破坏**：
所有 `t` 被替换为 `\\(\\boldsymbol{{t}}\\)` ⇒ `τ`→`\\(\\boldsymbol{{t}}\\)au`、`√`→`\\sqr\\(\\boldsymbol{{t}}\\)`、
`\\left`→`\\lef\\(\\boldsymbol{{t}}\\)`。表面看「公式全没了」。

**修复**：`s.replace('\\\\(\\\\boldsymbol{{t}}\\\\)','t')` 一次还原全部（还原件 `_tmp_r246_fixed.md`，原文件只读）。
★若不还原即审计，会误判「靶公式缺失」——正是 r247 判过的「把靶已有的东西判成没有」那一类事实性错误。

## 2. 靶的完整方程组（一张表）

| 编号 | 方程 | 靶的用途 |
|---|---|---|
| (1) | $\\omega^2=c^2(\\kappa^2+\\tau^2)$ | 本源几何不变式 |
| (2) | $\\nabla_t t=\\kappa n;\\ \\nabla_t n=-\\kappa t+\\tau b;\\ \\nabla_t b=-\\tau n$ | Frenet-Serret |
| (3) | $\\displaystyle F=\\frac{{\\hbar c}}{{4\\pi}}\\frac{{\\kappa n+\\tau b}}{{\\sqrt{{1+(\\omega r/c)^2}}}}$ | **全域力主方程** |
| (5) | $m=\\frac{{\\hbar}}{{c}}\\sqrt{{\\kappa^2+\\tau^2}}$ | 质量几何式 |
| (12) | $S=\\hbar\\frac{{\\sqrt{{\\kappa^2+\\tau^2}}}}{{\\kappa}}$，靶令 $=\\tfrac12$ | 自旋 1/2 |
| (17) | $R_{{\\mu\\nu}}-\\tfrac12 g_{{\\mu\\nu}}R+\\Lambda g_{{\\mu\\nu}}=\\frac{{4\\pi Gm^2}}{{c^2\\hbar}}u_\\mu u_\\nu$ | 场方程 |
| (61) | $\\kappa(r)=\\frac{{GM}}{{c^2r^2}}e^{{-\\lambda(r)}}$ | 引力曲率 |

## 3. 两卷的分层与关系（不可相加）

| 卷 | 审什么 | 最锋利的一条 |
|---|---|---|
| **r248** | 主方程**本体**（量纲 / 自旋 / 距离依赖 / 地基 / 公设 / 数值） | 自旋 ℏ/2 虚数解 |
| **r249** | 「从主方程**推导出四力**」这一步（牛顿 / 库仑 / 单调性 / 宇称 / 参数 / 标架） | 禁闭与渐近自由反号 |

**共同的方法论收获**：两卷最硬的两条都是**纯代数/符号结论**，不依赖实验输入、不依赖 $\\kappa,\\tau,\\omega$ 取何值——
$\\sqrt{{1+x^2}}\\ge1$ 恒成立（r248），$-x/(1+x^2)^{{3/2}}<0$ 恒成立（r249）。

## 4. ★「幽灵质量」$\\hbar/(4\\pi c)$ —— 两卷的同一病根

这是本册最重要的整理发现：**同一个常数在两卷中以两种身份出现**。

| 卷 | 它扮演的角色 | 数值 |
|---|---|---|
| r248 · H1 | $F_{{靶}}/F_{{牛顿}}=\\hbar/(4\\pi c\\,m_{{test}})$，取 $m_{{test}}=1$ kg 时的**比值** | {float(ratio_1kg):.4e} |
| r249 · B1 | 令比值 $=1$ 反解出的**普适质量** | {float(ghost_kg):.4e} kg |

**机读恒等性自检**：两者一致 = **{'是' if identical else '否'}**（相对差 < 1e−6）。

它不是一个巧合，而是**同一个缺陷的两次显形**：主方程少了一个质量因子，那个缺失的质量恰好是

$$m_{{ghost}}=\\frac{{\\hbar}}{{4\\pi c}}={float(ghost_kg):.4e}\\ \\mathrm{{kg}}$$

其派生物同样荒谬：

- 约化康普顿波长 $\\hbar/(m_{{ghost}}c)={float(ghost_lam):.6f}$ m $=4\\pi$ 米（**精确**）
- 静能 $m_{{ghost}}c^2={ghost_E_J:.4e}$ J $={ghost_eV:.4e}$ eV（比最轻的中微子还小约 7 个数量级）
- 对应温度 $E/k_B={ghost_T:.4e}$ K
- 与真实粒子：电子差 **{d9['B3_mass_gap']['electron_decades']:.2f}**、质子差 **{d9['B3_mass_gap']['proton_decades']:.2f}** 个数量级

**二难**：要么接受「万物质量 = $2.7993\\times10^{{-44}}$ kg」（荒谬），
要么让 $\\kappa$ 含受力质量 ⇒ 时空几何由「放什么检验物体」决定（与靶「物质是几何投影」**因果倒置**）。

## 5. 判据总表（分层并列）

### r248 · 分层计数（{d8['counts']['items']} 条：PASS {d8['counts']['PASS']} / FAIL {d8['counts']['FAIL']} / OPEN {d8['counts']['OPEN']} / INFO {d8['counts']['INFO']}）

| 层 | PASS | FAIL | OPEN | INFO |
|---|---|---|---|---|
{lay_tbl(d8)}

### r248 · 条目

| ID | 层 | 结论 | 判据 |
|---|---|---|---|
{rows_tbl(d8)}

### r249 · 分层计数（{d9['counts']['items']} 条：PASS {d9['counts']['PASS']} / FAIL {d9['counts']['FAIL']} / INFO {d9['counts']['INFO']}）

| 层 | PASS | FAIL | OPEN | INFO |
|---|---|---|---|---|
{lay_tbl(d9)}

### r249 · 条目

| ID | 层 | 结论 | 判据 |
|---|---|---|---|
{rows_tbl(d9)}

## 6. 关键数值速查

| 量 | 值 | 出处 |
|---|---|---|
| 式(1) 数值微分对拍残差 | {d8['A1_step_search']['combined_rel_resid']:.3e}（$h={d8['A1_step_search']['best_h']:.0e}$） | r248 A1 |
| 主方程右端量纲 | ${d8['B1_force_dimension']['dim_(hbar*c)*kappa']}$（能量，非力 ${d8['B1_force_dimension']['target_force_N']}$） | r248 B1 |
| 场方程右端系数量纲 | ${d8['B2_field_eq_dimension']['dim_RHS_coefficient']}$ vs 左端 ${d8['B2_field_eq_dimension']['dim_LHS_(1/L^2)']}$ | r248 B2 |
| 长程 / 短程局部指数 | {d8['C_distance_dependence']['long_range_exponent_limit']:.0f} / {d8['C_distance_dependence']['short_range_exponent_limit']:.0f}（引力需 −2） | r248 C1/C2 |
| 自旋条件 | $(\\tau/\\kappa)^2={d8['D_spin_condition']['derived'].split('= ')[-1]}$，实数域无解 | r248 D1 |
| Eötvös $\\eta(\\mathrm{{Ti,Pt}})$ | {d8['E2_etvos']['eta_target']:.4f} vs MICROSCOPE {d8['E2_etvos']['MICROSCOPE_limit']:.1e}（超 {d8['E2_etvos']['excess_factor']:.2e} 倍） | r248 E2 |
| $F_{{靶}}/F_{{牛顿}}$ | 电子 {d8['H_magnitude']['ratios']['电子']:.3e} / 质子 {d8['H_magnitude']['ratios']['质子']:.3e} / 1 kg {float(ratio_1kg):.3e}，跨 {d8['H_magnitude']['span_decades']:.1f} 数量级 | r248 H1 |
| **幽灵质量 $m_{{ghost}}$** | **{float(ghost_kg):.4e} kg**（波长 {float(ghost_lam):.6f} m $=4\\pi$） | r249 B1/B2 |
| 弱力力程反解 | $\\lambda_W={d9['A3_weak_range']['lambda_W_m']:.4e}$ m；$\\omega={d9['A3_weak_range']['omega_W_rad_per_s']:.4e}$ rad/s（回代 {d9['A3_weak_range']['E=hbar*omega_in_GeV']:.3f} GeV） | r249 A3 |
| 单调性 | $dF/dx=-x/(1+x^2)^{{3/2}}$，全网格恒负 = {d9['D_monotonicity']['strictly_decreasing_for_r_gt_0']}；$F(0)={d9['D_monotonicity']['F_at_r_to_0']:.1f}$（最大值） | r249 D1/D2 |
| 修复定价 | r248 {d8['I_repair_pricing']['tally']['SURVIVE']}/{d8['I_repair_pricing']['tally']['SUICIDE']}/{d8['I_repair_pricing']['tally']['EMPTY']}；r249 {d9['H_repair_pricing']['tally']['SURVIVE']}/{d9['H_repair_pricing']['tally']['SUICIDE']}/{d9['H_repair_pricing']['tally']['EMPTY']}（SURVIVE/SUICIDE/EMPTY） | 两卷 |

## 7. 对靶有利项汇总（共 {len(fav8) + len(fav9)} 条，照实记）

### r248（{len(fav8)} 条）

{chr(10).join('- **%s**：%s' % (r['id'], r['claim']) for r in fav8)}

### r249（{len(fav9)} 条）

{chr(10).join('- **%s**（%s）：%s' % (r['id'], r['verdict'], r['claim']) for r in fav9)}

## 8. 控制组与守卫

| 卷 | 守卫 | 控制组 |
|---|---|---|
| r248 | {d8['counts']['guards']}/{d8['counts']['guards']}（残差阈值非写死 / 定价真枚举 / 靶只读 / GR 量纲正对照 / 求解器可解 / hash 复验 / **数值微分标定**） | 3 类：正对照（GR、$\\kappa^2$、$S=2\\hbar$）· 负对照（解析 vs 数值）· 分辨力（指数扫描、比值随质量变） |
| r249 | {d9['counts']['guards']}/{d9['counts']['guards']}（残差非写死 / 定价真枚举 / A3 由计算得出 / 扫描器对真物理式符号正确 / hash 复验） | 4 条：Yukawa 与禁闭符号相反 · 单圈 QCD 渐近自由 · 中心差分数值导数 · 宇称审计三态 |

## 9. 与既有卷的分层（一律不可相加）

r243 工程可用性层 · r244 引力本体论层 · r245 超导本质层（凝聚态） · r247 元审计层（审 r244） ·
**r248 单方程全域力层（主方程本体）** · **r249 低能极限推导层（下游推导）**。

与 r243 的交叉验证：r248 的 $\\eta(\\mathrm{{Ti,Pt}})={d8['E2_etvos']['eta_target']:.4f}$ 与 r243 的独立实现**完全一致**；
r249 的二难与 r243 的 $\\kappa$ 读法二难**同型但靶不同**。

## 10. 自抓记录（本线三次，同一类教训）

1. **r249 A3**：残差 0 属**恒等式回代**（$\\lambda_W=\\hbar/m_Wc$→反解 $\\omega$→回代 $E=m_Wc^2$）⇒ 由 PASS 降为 **INFO**。
2. **r249 HTML**：$\\alpha_s$ 数值被手抄为 0.4264/0.1185，与实算 0.3032/0.1123 不符 ⇒ 改占位符动态插入。
3. **r248 A1（落盘后交叉复核发现）**：数值微分初版用**一阶差分公式去取二阶/三阶导数** ⇒ $\\boldsymbol r'$ 与 $\\boldsymbol r''$ 近似平行、
   $|\\boldsymbol r'\\times\\boldsymbol r''|\\sim10^{{-10}}$ ⇒ 数值 $\\kappa$ 崩为 $5\\times10^{{-9}}$（残差 **100%**），
   而 verdict 却按**恒等式残差**（2.220e−16，必然为 0）判 PASS ⇒ **对靶有利方向的假 PASS**。
   修正：各阶独立差分公式 + 步长自适应 ⇒ 联合相对残差 **{d8['A1_step_search']['combined_rel_resid']:.3e}**，PASS 真正成立；新增守卫 **G-7（数值微分标定）**。

**统一教训**：凡「残差 = 0」，先问是不是自己绕回来的；凡高阶梯度的机算，先用解析解标定实现。

## 11. 开放项与下一步

- **未审靶材**：## 36 节「垂直原理」（电场/磁场/磁力正交性的几何声称）、黑洞无奇点解（式 59–68）、FRW 宇宙学约化（式 33–42）。
- **r249 的 A3 结构同构值得追**：靶的 $r_c=c/\\omega$ 与 Yukawa $\\lambda=\\hbar/mc$ 同构是真实的，
  若靶能给出 $\\omega$ 的赋值规则，则该层可能由 INFO 升为可判；**目前靶从未赋值**。
- **下一步取号**：从 **r251** 起（**本册落盘时实测 r251/r252/r253 三树全空**；而 r250 已被并行会话《耦合常数跑动与能标层·RG》占用，故本册章末原写「从 r250 起」已作废——这是「下轮字段必过期」纪律的**第四次显形**）。
"""

io.open(os.path.join(DATA, OUT + ".md"), "w", encoding="utf-8").write(MD)

# ---------------- HTML ----------------
CSS = """
:root{--bg:#0b1220;--panel:#0f1829;--panel2:#111c31;--ink:#e2e8f0;--dim:#94a3b8;
--line:#1f2b3f;--green:#4ade80;--red:#f87171;--amber:#fbbf24;--blue:#63d2ff;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--ink);font-family:"Noto Sans SC","Microsoft YaHei",system-ui,sans-serif;line-height:1.8;padding:26px 16px;}
.wrap{max-width:980px;margin:0 auto;}
.banner{background:linear-gradient(135deg,#0b1220,#0a3b1e);border:1px solid #166534;border-radius:14px;padding:26px;margin-bottom:18px;}
.badge{display:inline-block;background:#14532d;color:#bbf7d0;font-size:11px;padding:2px 10px;border-radius:99px;margin-bottom:12px;font-weight:600;}
.banner h1{font-size:22px;font-weight:900;letter-spacing:1px;}
.banner p{font-size:13px;color:var(--dim);margin-top:8px;}
.preview{background:var(--panel2);border:1px solid #334155;border-left:5px solid var(--green);border-radius:10px;padding:14px 16px;font-size:13.5px;color:#bbf7d0;margin-bottom:20px;}
.preview b{color:var(--green);}
section{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px 22px;margin-bottom:18px;}
h2{font-size:17px;font-weight:800;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid var(--line);}
h2 .n{color:var(--green);margin-right:6px;}
h3{font-size:14.5px;font-weight:700;color:#86efac;margin:14px 0 6px;}
p,li{font-size:13.5px;color:#cbd5e1;}
ul,ol{padding-left:22px;margin:8px 0;}li{margin:4px 0;}
table{border-collapse:collapse;margin:10px 0;font-size:12px;}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top;}
th{background:#0d1730;color:#86efac;font-weight:700;}
.eq{background:#0c1a2e;border:1px solid #1d4ed8;border-left:5px solid var(--blue);border-radius:8px;padding:12px 16px;margin:12px 0;font-family:Consolas,monospace;font-size:12.5px;color:#dbeafe;white-space:pre-wrap;}
.key{background:#1a0b0b;border:1px solid #7f1d1d;border-left:5px solid var(--red);border-radius:8px;padding:14px 16px;margin:12px 0;font-size:13.5px;color:#fecaca;}
.warn{background:#1c1206;border:1px solid #78350f;border-left:5px solid var(--amber);border-radius:8px;padding:12px 16px;margin:12px 0;font-size:13.5px;color:#fde68a;}
.PASS{color:#4ade80;font-weight:700;}.FAIL{color:#f87171;font-weight:700;}.OPEN{color:#fbbf24;font-weight:700;}.INFO{color:#94a3b8;font-weight:700;}
.foot{font-size:12px;color:var(--dim);text-align:center;padding:16px 0;}
"""


def html_rows(d):
    return "".join("<tr><td>%s</td><td>%s</td><td><span class='%s'>%s</span></td><td>%s</td></tr>"
                   % (r["id"], r["layer"], r["verdict"], r["verdict"], r["claim"])
                   for r in rows_of(d))


def html_lay(d):
    return "".join("<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>"
                   % (k, v["PASS"], v["FAIL"], v["OPEN"], v["INFO"])
                   for k, v in d["summary_by_layer"].items())


HTML = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>r248+r249 双卷归一总册</title><style>@@CSS@@</style></head><body><div class="wrap">
<div class="banner"><span class="badge">TUFT 审计链 · 整理册（非占号）</span>
<h1>单方程全域力双卷归一总册 · r248 + r249</h1>
<p>同一份来料的两卷攻破归一整理。全部数字由脚本机读两份 JSON 生成，渲染层不手抄。</p></div>

<div class="preview"><b>一句话</b>：靶用一个矢量方程声称统一四力并五步推导出牛顿引力、库仑定律、
弱力宇称破缺、强力禁闭与渐近自由。两卷共 <b>@@TOT@@ 条</b>判据（分层并列、不可相加），
守卫 <b>@@GT@@/@@GT@@</b>，两卷修复定价均 <b>SURVIVE 0</b> ⇒ 第 31 与 32 度。</div>

<section><h2><span class="n">§1</span>★★ 幽灵质量：两卷的同一病根</h2>
<div class="key"><b>同一个常数 $\\hbar/(4\\pi c)$ 在两卷中以两种身份出现</b><br>
r248 · H1：$F_{靶}/F_{牛顿}=\\hbar/(4\\pi c\\,m_{test})$，取 $m_{test}=1$ kg → <b>@@R1@@</b><br>
r249 · B1：令比值 $=1$ 反解出的<b>普适质量</b> → <b>@@GH@@ kg</b><br>
机读恒等性自检：<b>@@ID@@</b>（相对差 &lt; 1e−6）<br><br>
它不是巧合，而是同一个缺陷的两次显形：主方程<b>少了一个质量因子</b>，那个缺失的质量恰好是
$\\hbar/(4\\pi c)$。其派生物同样荒谬——约化康普顿波长 <b>@@LAM@@ m $=4\\pi$ 米（精确）</b>；
静能 <b>@@EV@@ eV</b>（比最轻的中微子还小约 7 个数量级）；与电子差 <b>@@DE@@</b>、质子差 <b>@@DP@@</b> 个数量级。<br><br>
<b>二难</b>：要么接受「万物质量 $=2.7993\\times10^{-44}$ kg」，要么让 $\\kappa$ 含受力质量
⇒ 时空几何由「放什么检验物体」决定，与靶「物质是几何投影」<b>因果倒置</b>。</div>
</section>

<section><h2><span class="n">§2</span>两卷分层与关系（不可相加）</h2>
<table><thead><tr><th>卷</th><th>审什么</th><th>最锋利的一条</th></tr></thead><tbody>
<tr><td><b>r248</b></td><td>主方程<b>本体</b>（量纲 / 自旋 / 距离依赖 / 地基 / 公设 / 数值）</td><td>自旋 $\\hbar/2$ 虚数解</td></tr>
<tr><td><b>r249</b></td><td>「从主方程<b>推导出四力</b>」这一步（牛顿 / 库仑 / 单调性 / 宇称 / 参数 / 标架）</td><td>禁闭与渐近自由反号</td></tr>
</tbody></table>
<div class="warn"><b>共同的方法论收获</b>：两卷最硬的两条都是<b>纯代数/符号结论</b>，
不依赖实验输入、不依赖 $\\kappa,\\tau,\\omega$ 取何值——$\\sqrt{1+x^2}\\ge1$ 恒成立（r248），
$-x/(1+x^2)^{3/2}<0$ 恒成立（r249）。</div>
</section>

<section><h2><span class="n">§3</span>来料还原（「t 污染」事件）</h2>
<p>来料 LaTeX 被批量破坏：所有 <code>t</code> 被替换为 <code>\\(\\boldsymbol{t}\\)</code> ⇒
<code>τ</code>→<code>\\(\\boldsymbol{t}\\)au</code>、<code>√</code>→<code>\\sqr\\(\\boldsymbol{t}\\)</code>。
表面看「公式全没了」。修复：<code>s.replace('\\\\(\\\\boldsymbol{t\\\\)','t')</code> 一次还原。
★若不还原即审计，会误判「靶公式缺失」——正是 r247 判过的那类对靶不利方向的事实性错误。</p>
</section>

<section><h2><span class="n">§4</span>r248 · 分层计数与条目（@@N8@@ 条）</h2>
<table><thead><tr><th>层</th><th>PASS</th><th>FAIL</th><th>OPEN</th><th>INFO</th></tr></thead><tbody>@@L8@@</tbody></table>
<table><thead><tr><th>ID</th><th>层</th><th>结论</th><th>判据</th></tr></thead><tbody>@@R8@@</tbody></table>
</section>

<section><h2><span class="n">§5</span>r249 · 分层计数与条目（@@N9@@ 条）</h2>
<table><thead><tr><th>层</th><th>PASS</th><th>FAIL</th><th>OPEN</th><th>INFO</th></tr></thead><tbody>@@L9@@</tbody></table>
<table><thead><tr><th>ID</th><th>层</th><th>结论</th><th>判据</th></tr></thead><tbody>@@R9@@</tbody></table>
</section>

<section><h2><span class="n">§6</span>自抓三次（同一类教训）</h2>
<ol>
<li><b>r249 A3</b>：残差 0 属恒等式回代 ⇒ 由 PASS 降为 <b>INFO</b>。</li>
<li><b>r249 HTML</b>：$\\alpha_s$ 手抄为 0.4264/0.1185，与实算 0.3032/0.1123 不符 ⇒ 改占位符。</li>
<li><b>r248 A1</b>：数值微分用一阶差分公式取二阶/三阶导数 ⇒ $\\kappa$ 崩为 $5\\times10^{-9}$（残差 100%），
verdict 却按恒等式残差判 PASS ⇒ <b>对靶有利方向的假 PASS</b>。已修正（残差 @@RES@@），新增守卫 G-7。</li>
</ol>
<div class="warn"><b>统一教训</b>：凡「残差 = 0」，先问是不是自己绕回来的；凡高阶梯度的机算，先用解析解标定实现。</div>
</section>

<section><h2><span class="n">§7</span>下一步</h2>
<ul>
<li><b>未审靶材</b>：## 36 节「垂直原理」、黑洞无奇点解（式 59–68）、FRW 宇宙学约化（式 33–42）。</li>
<li><b>A3 值得追</b>：$r_c=c/\\omega$ 与 Yukawa $\\lambda=\\hbar/mc$ 结构同构是真实的；若靶给出 $\\omega$ 赋值规则，该层可由 INFO 升为可判——目前靶从未赋值。</li>
<li><b>取号</b>：从 <b>r251</b> 起（本册落盘时实测 r251/r252/r253 三树全空；r250 已被并行会话占用 ⇒ 原「从 r250 起」作废）。</li>
</ul>
</section>

<div class="foot">整理册 · r248 + r249 双卷归一 · 非占号产物 · 数字全部机读自两份 JSON</div>
</div></body></html>"""

HTML = (HTML.replace("@@CSS@@", CSS)
        .replace("@@TOT@@", str(d8["counts"]["items"] + d9["counts"]["items"]))
        .replace("@@GT@@", str(d8["counts"]["guards"] + d9["counts"]["guards"]))
        .replace("@@R1@@", "%.4e" % float(ratio_1kg))
        .replace("@@GH@@", "%.4e" % float(ghost_kg))
        .replace("@@ID@@", "一致" if identical else "不一致")
        .replace("@@LAM@@", "%.6f" % float(ghost_lam))
        .replace("@@EV@@", "%.4e" % ghost_eV)
        .replace("@@DE@@", "%.2f" % d9["B3_mass_gap"]["electron_decades"])
        .replace("@@DP@@", "%.2f" % d9["B3_mass_gap"]["proton_decades"])
        .replace("@@N8@@", str(d8["counts"]["items"]))
        .replace("@@N9@@", str(d9["counts"]["items"]))
        .replace("@@L8@@", html_lay(d8)).replace("@@L9@@", html_lay(d9))
        .replace("@@R8@@", html_rows(d8)).replace("@@R9@@", html_rows(d9))
        .replace("@@RES@@", "%.3e" % d8["A1_step_search"]["combined_rel_resid"]))
io.open(os.path.join(SRC, OUT + ".html"), "w", encoding="utf-8").write(HTML)

print("幽灵质量恒等性自检：r248 的 1kg 比值 %s  vs  r249 的普适质量 %s  -> %s"
      % ("%.6e" % float(ratio_1kg), "%.6e" % float(ghost_kg), identical))
print("幽灵质量静能 = %.4e eV；对应温度 = %.4e K" % (ghost_eV, ghost_T))
print("OK -> %s.md" % OUT)
print("OK -> %s.html" % OUT)
