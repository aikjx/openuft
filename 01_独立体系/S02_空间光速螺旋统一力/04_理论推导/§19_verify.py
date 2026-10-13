# -*- coding: utf-8 -*-
"""
§19_verify.py — 四力数值统一：耦合常数一循环跑动验证 + 图谱生成
S02 空间光速螺旋统一力 · 算法联盟
校验项:
  V1  最小 SM 三线两两交叉能标 (不共点 -> 不统一)
  V2  SUSY-SM 三线交叉能标簇 (共点 -> 统一) 与 M_GUT
  V3  α_GUT^-1 数值
  V4  质量-频率阶梯 ω_c = m c^2/hbar, λ = hbar/(m c)
  V5  曲线数据 -> JSON + §19 图谱 HTML
"""
import json, math, os

# ---- 常数 ----
hbar  = 1.054571817e-34
c     = 2.99792458e8
hc    = hbar * c
eV    = 1.602176634e-19
GeV   = 1e9 * eV
MeV   = 1e6 * eV

# ---- 输入 (m_Z, MS-bar, PDG 2024) ----
mZ     = 91.1876 * GeV          # 91.1876 GeV
alpha_mZ  = 1.0 / 127.925
sin2W    = 0.23122
alpha_s  = 0.1184
cos2W    = 1.0 - sin2W

a1_mZ = (5.0/3.0) * alpha_mZ / cos2W    # GUT 归一化
a2_mZ = alpha_mZ / sin2W
a3_mZ = alpha_s
inv = lambda a: 1.0/a

# ---- β 系数 ----
b_SM   = (41.0/10.0, -19.0/6.0, -7.0)        # 最小 SM
b_SUSY = (33.0/5.0, 1.0, -3.0)               # MSSM
MSUSY  = 1e3 * GeV                          # 超对称阈值 1 TeV

def inv_alpha_SM(i, mu):
    """最小 SM: α_i^-1(mu) = α_i^-1(mZ) - b_i/(2π) ln(mu/mZ)"""
    return inv((a1_mZ, a2_mZ, a3_mZ)[i]) - (b_SM[i]/(2.0*math.pi)) * math.log(mu/mZ)

def inv_alpha_SUSY(i, mu):
    """SUSY: mZ..MSUSY 用 SM β, MSUSY 以上用 MSSM β"""
    if mu <= MSUSY:
        return inv_alpha_SM(i, mu)
    base = inv_alpha_SM(i, MSUSY)
    return base - (b_SUSY[i]/(2.0*math.pi)) * math.log(mu/MSUSY)

def crossing(f_i, f_j, mu_lo, mu_hi):
    """二分法求 f_i(mu)=f_j(mu) 的 mu"""
    lo, hi = mu_lo, mu_hi
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        d = (f_i(mid) - f_j(mid)) * (f_i(lo) - f_j(lo))
        if d <= 0: hi = mid
        else:      lo = mid
    return math.sqrt(lo*hi)

print("=" * 70)
print("§19 四力数值统一 · 一循环耦合跑动验证报告")
print("=" * 70)
print("输入: α(mZ)=1/127.925  sin²θW=0.23122  αs(mZ)=0.1184  (mZ=91.1876 GeV)")
print("m_Z 处: α1^-1=%.4f  α2^-1=%.4f  α3^-1=%.4f"
      % (inv(a1_mZ), inv(a2_mZ), inv(a3_mZ)))

# ---- V1: 最小 SM 交叉 ----
print("\n[V1] 最小 SM (b=(41/10,-19/6,-7)):")
c12 = crossing(lambda m: inv_alpha_SM(0,m), lambda m: inv_alpha_SM(1,m), mZ, 1e17)
c13 = crossing(lambda m: inv_alpha_SM(0,m), lambda m: inv_alpha_SM(2,m), mZ, 1e17)
c23 = crossing(lambda m: inv_alpha_SM(1,m), lambda m: inv_alpha_SM(2,m), mZ, 1e17)
print("  α1=α2 @ %.3e GeV" % (c12/GeV))
print("  α1=α3 @ %.3e GeV" % (c13/GeV))
print("  α2=α3 @ %.3e GeV" % (c23/GeV))
spread_sm = math.log10(c23/c12)
print("  交叉簇跨度 = %.2f 个数量级  (>=2 即判不共点)" % spread_sm)

# ---- V2/V3: SUSY 交叉 ----
print("\n[V2] SUSY-SM (M_SUSY=1 TeV; 上方 b=(33/5,1,-3)):")
s12 = crossing(lambda m: inv_alpha_SUSY(0,m), lambda m: inv_alpha_SUSY(1,m), MSUSY, 1e19)
s13 = crossing(lambda m: inv_alpha_SUSY(0,m), lambda m: inv_alpha_SUSY(2,m), MSUSY, 1e19)
s23 = crossing(lambda m: inv_alpha_SUSY(1,m), lambda m: inv_alpha_SUSY(2,m), MSUSY, 1e19)
print("  α1=α2 @ %.3e GeV" % (s12/GeV))
print("  α1=α3 @ %.3e GeV" % (s13/GeV))
print("  α2=α3 @ %.3e GeV" % (s23/GeV))
spread_susy = math.log10(s23/s12)
print("  交叉簇跨度 = %.2f 个数量级" % spread_susy)
MGUT = math.sqrt(s12*s23)
ag_inv = [inv_alpha_SUSY(i, MGUT) for i in range(3)]
print("  M_GUT(几何中心) = %.3e GeV   α_GUT^-1 = %.3f / %.3f / %.3f"
      % (MGUT/GeV, ag_inv[0], ag_inv[1], ag_inv[2]))

# ---- V4: 质量-频率阶梯 ----
print("\n[V4] 质量-频率阶梯 (ω_c = m c²/ℏ, λ = ℏ/(m c)):")
ladder = [
    ("π⁰",  134.9768e6*eV,  2.05e23),
    ("e⁻",  0.51099895e6*eV, 7.76e20),
    ("W±",  80.369*GeV,     1.22e26),
    ("Z⁰",  91.1876*GeV,    1.39e26),
    ("M_GUT", 2e16*GeV,     3.0e40),
]
for name, Ec2, w_ref in ladder:
    w = Ec2 / hbar
    lam = hc / Ec2
    print("  %-6s  m=%.4e GeV/c²   λ=%.3e m   ω_c=%.3e s⁻¹  (参考 %.1e)"
          % (name, Ec2/GeV if Ec2 > 1e6*eV else Ec2/MeV/1000, lam, w, w_ref))
lam_gut = hc/(2e16*GeV)
print("  λ_GUT = %.3e m ≈ 10⁻³² m" % lam_gut)

# ---- V5: 曲线数据 + 图谱 ----
xs = [2.0 + i*0.05 for i in range(301)]        # log10(μ/GeV): 1e2..1e17
mus = [10.0**x for x in xs]
series = {k: [] for k in ("a1_SM","a2_SM","a3_SM","a1_SU","a2_SU","a3_SU")}
for mu in mus:
    for i, key in ((0,"a1_SM"),(1,"a2_SM"),(2,"a3_SM")):
        series[key].append(inv_alpha_SM(i, mu))
    for i, key in ((0,"a1_SU"),(1,"a2_SU"),(2,"a3_SU")):
        series[key].append(inv_alpha_SUSY(i, mu))

data = {"x_log10_mu_GeV": xs, "series": series,
        "MGUT_GeV": MGUT/GeV, "aGUT_inv": ag_inv}
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "§19_耦合跑动曲线数据.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
print("\n[V5] 曲线数据已写入: §19_耦合跑动曲线数据.json (%d 点)" % len(xs))

def js_arr(arr):
    return "[" + ",".join("%.4f" % v for v in arr) + "]"

js = (
    "var X=" + js_arr(xs) + ";\n"
    "var S1_SM=" + js_arr(series["a1_SM"]) + ";\n"
    "var S2_SM=" + js_arr(series["a2_SM"]) + ";\n"
    "var S3_SM=" + js_arr(series["a3_SM"]) + ";\n"
    "var S1_SU=" + js_arr(series["a1_SU"]) + ";\n"
    "var S2_SU=" + js_arr(series["a2_SU"]) + ";\n"
    "var S3_SU=" + js_arr(series["a3_SU"]) + ";\n"
    "var MGUT=" + ("%.4f" % (MGUT/GeV)) + ";"
)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>四力数值统一 · 耦合常数跑动与大统一能标图谱</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0;}
  body{font-family:"Microsoft YaHei","PingFang SC",sans-serif;background:#f5f6f8;color:#1f2937;line-height:1.6;padding:20px;}
  .wrap{max-width:1180px;margin:0 auto;}
  header{background:linear-gradient(135deg,#0f172a,#1e3a5f);color:#fff;border-radius:14px;padding:22px 28px;margin-bottom:16px;}
  header h1{font-size:22px;}
  header .eq{font-family:Consolas,"Courier New",monospace;font-size:15px;color:#fde68a;margin-top:10px;}
  header .sub{font-size:13px;color:#cbd5e1;margin-top:8px;}
  .chartbox{background:#fff;border-radius:12px;padding:14px 16px;margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,.06);}
  #chart{width:100%;height:560px;}
  table{width:100%;border-collapse:collapse;font-size:13.5px;}
  th,td{border:1px solid #e5e7eb;padding:6px 10px;text-align:left;}
  th{background:#f1f5f9;}
  .note{font-size:12.5px;color:#64748b;margin-top:10px;}
  .ok{color:#15803d;font-weight:600;} .no{color:#dc2626;font-weight:600;}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>四力数值统一 · 耦合常数跑动与大统一能标（一循环 RG）</h1>
  <div class="eq">αᵢ⁻¹(μ) = αᵢ⁻¹(m_Z) − (bᵢ/2π)·ln(μ/m_Z)，  b(SM)=(41/10,−19/6,−7)，  b(MSSM)=(33/5,1,−3)</div>
  <div class="sub">S02 空间光速螺旋统一力 · §19 · 数据来源：§19_verify.py 实跑（m_Z=91.1876 GeV，α=1/127.925，sin²θ_W=0.23122，α_s=0.1184；M_SUSY=1 TeV）</div>
</header>

<div class="chartbox">
  <div id="chart"></div>
  <p class="note">实线 = SUSY-SM（M_SUSY=1 TeV 以上换 MSSM β），虚线 = 最小 SM（全区间 SM β）。两条情景在 1 TeV 以下重合。SUSY 三线于 ~1.0–2.7×10¹⁶ GeV 交汇（α_GUT⁻¹≈25.5–25.9，虚线 M_GUT 标记）；最小 SM 三线两两交叉于 10¹³–10¹⁷ GeV 三个不同能标，不共点。</p>
</div>

<div class="chartbox">
  <h3 style="font-size:16px;margin-bottom:10px;">交叉能标表（§19_verify.py 输出）</h3>
  <table>
    <tr><th>情景</th><th>α₁=α₂</th><th>α₁=α₃</th><th>α₂=α₃</th><th>判定</th></tr>
    <tr><td>最小 SM</td><td>1.03×10¹³ GeV</td><td>2.44×10¹⁴ GeV</td><td>9.9×10¹⁶ GeV</td><td class="no">不共点（跨 ~4 个数量级）→ 不统一</td></tr>
    <tr><td>SUSY-SM</td><td>9.8×10¹⁵ GeV</td><td>1.48×10¹⁶ GeV</td><td>2.63×10¹⁶ GeV</td><td class="ok">共点簇（跨 &lt;0.5 数量级）→ M_GUT≈1.6×10¹⁶ GeV（文献常取≈2×10¹⁶）</td></tr>
  </table>
  <p class="note">α_GUT⁻¹ ≈ 25.5–25.9；与质子寿命下限 τ_p&gt;2.4×10³⁴ yr 相容（要求 M_GUT≳10¹⁵–10¹⁶ GeV）。SUSY 未发现、质子衰变/磁单极未观测：框架内成立、实验未证实。</p>
</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"
        onerror="document.getElementById('chart').innerHTML='<p style=\\'padding:24px\\'>ECharts 加载失败（离线环境），请参照上方交叉能标表。</p>';"></script>
<script>
__DATA__
(function(){
  var el = document.getElementById('chart');
  if(!el || typeof echarts === 'undefined'){ return; }
  var chart = echarts.init(el);
  var option = {
    tooltip: {
      trigger: 'axis', triggerOn: 'mousemove|click', renderMode: 'richText', confine: true,
      formatter: function(params){
        if(!params || !params.length){ return ''; }
        var x = params[0].value[0];
        var mu = Math.pow(10, x);
        var s = 'μ ≈ ' + Number(mu).toExponential(1) + ' GeV';
        for(var i=0;i<params.length;i++){
          var p = params[i];
          s += String.fromCharCode(10) + p.marker + p.seriesName + '：' + Number(p.value[1]).toFixed(2);
        }
        return s;
      }
    },
    legend: { top: 4, type: 'scroll', data: ['α₁⁻¹ SM','α₂⁻¹ SM','α₃⁻¹ SM','α₁⁻¹ SUSY','α₂⁻¹ SUSY','α₃⁻¹ SUSY'] },
    grid: { left: 70, right: 30, top: 50, bottom: 60 },
    xAxis: { type: 'value', name: 'log₁₀(μ/GeV)', nameLocation: 'middle', nameGap: 38, min: 2, max: 17,
      axisLabel: { formatter: function(v){ return v.toFixed(1); } } },
    yAxis: { type: 'value', name: 'αᵢ⁻¹', nameLocation: 'middle', nameGap: 42, min: 0, max: 60 },
    series: [
      { name: 'α₁⁻¹ SM', type: 'line', data: S1_SM.map(function(v,i){return [X[i],v];}), showSymbol: false,
        lineStyle: { width: 2, type: 'dashed' },
        markLine: { symbol: 'none', silent: true,
          label: { fontSize: 11, formatter: 'M_GUT≈2×10¹⁶ GeV', position: 'insideEndTop' },
          data: [{ xAxis: Math.log10(MGUT) }] } },
      { name: 'α₂⁻¹ SM', type: 'line', data: S2_SM.map(function(v,i){return [X[i],v];}), showSymbol: false,
        lineStyle: { width: 2, type: 'dashed' } },
      { name: 'α₃⁻¹ SM', type: 'line', data: S3_SM.map(function(v,i){return [X[i],v];}), showSymbol: false,
        lineStyle: { width: 2, type: 'dashed' } },
      { name: 'α₁⁻¹ SUSY', type: 'line', data: S1_SU.map(function(v,i){return [X[i],v];}), showSymbol: false, lineStyle: { width: 2 } },
      { name: 'α₂⁻¹ SUSY', type: 'line', data: S2_SU.map(function(v,i){return [X[i],v];}), showSymbol: false, lineStyle: { width: 2 } },
      { name: 'α₃⁻¹ SUSY', type: 'line', data: S3_SU.map(function(v,i){return [X[i],v];}), showSymbol: false, lineStyle: { width: 2 } }
    ]
  };
  chart.setOption(option);
  window.addEventListener('resize', function(){ chart.resize(); });
})();
</script>
</body>
</html>
"""

html_path = os.path.join(HERE, "§19_耦合跑动_大统一能标图谱.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html.replace("__DATA__", js))
print("图谱已生成: %s" % html_path)

print("\n判定: 最小 SM 不统一 (交叉簇跨 %.2f 数量级), SUSY-SM 统一成立 (跨 %.2f 数量级)。"
      % (spread_sm, spread_susy))
