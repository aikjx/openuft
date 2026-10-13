# -*- coding: utf-8 -*-
"""
§20_verify.py — 质量-耦合数值开环检验 + 图谱生成
S02 空间光速螺旋统一力 · 算法联盟
V1  α/α_w vs sin²θ_W（巧合 or 精确关系）
V2  m_W/m_Z vs cos θ_W（SM 树级）
V3  Veltman ρ 参数
V4  引力缺席 GUT 汇合 α_G(M_GUT)
V5  S02 频率阶梯比值（身份重述检验）
V6  SUSY-GUT 一循环预言 sin²θ_W(m_Z)（3/8 边界 + 双阈值跑动）
"""
import json, math, os

hbar = 1.054571817e-34
c    = 2.99792458e8
G    = 6.67430e-11
eV   = 1.602176634e-19
GeV  = 1e9 * eV
MeV  = 1e6 * eV

# 输入（与 §19 同套）
mW      = 80.369 * GeV
mZ      = 91.1876 * GeV
mpi     = 134.9768 * MeV
me      = 0.51099895 * MeV
alpha   = 1.0 / 137.035999084
alpha_w = 1.0 / 29.0
sin2W   = 0.23122
cos2W   = 1.0 - sin2W
alpha_mZ = 1.0 / 127.925
MGUT        = 1.604e16 * GeV      # §19 几何中心（统一能标代表值）
MGUT_cross  = 9.782e15 * GeV      # §19: SUSY α1=α2 交叉能标（V6 边界用）
aG_inv_at_cross = 25.5059         # §19: 交叉处 α1⁻¹=α2⁻¹
MSUSY   = 1e3 * GeV

print("=" * 70)
print("§20 质量-耦合数值开环 · 检验报告")
print("=" * 70)

# ---- V1: α/α_w ----
sw_cand = alpha / alpha_w
dev1 = (sin2W - sw_cand) / sin2W * 100.0
print("\n[V1] α/α_w vs sin²θ_W:")
print("  α/α_w = %.5f   sin²θ_W = %.5f   偏差 = %+.2f%%" % (sw_cand, sin2W, dev1))

# ---- V2: m_W/m_Z = cosθ_W ----
r_mass = mW / mZ
cosW = math.sqrt(cos2W)
dev2 = (r_mass - cosW) / cosW * 100.0
print("\n[V2] m_W/m_Z vs cosθ_W:")
print("  m_W/m_Z = %.5f   cosθ_W = %.5f   偏差 = %+.3f%%" % (r_mass, cosW, dev2))

# ---- V3: ρ ----
rho = r_mass**2 / cos2W
print("\n[V3] Veltman ρ 参数:")
print("  ρ = m_W²/(m_Z²cos²θ_W) = %.5f   (SM: 1.0004±0.0010)" % rho)

# ---- V4: 引力缺席 ----
MP_kg  = math.sqrt(hbar * c / G)
MP_GeV = MP_kg * c**2 / eV / 1e9
r_GUT  = MGUT / (MP_GeV * GeV)
aG_MGUT = r_GUT**2
aGUT    = 1.0 / aG_inv_at_cross
dec4 = math.log10(aG_MGUT / aGUT)
print("\n[V4] 引力缺席 GUT:")
print("  M_P = %.4e GeV   M_GUT/M_P = %.4e" % (MP_GeV, r_GUT))
print("  α_G(M_GUT) = %.3e   α_GUT = %.5f   相差 %.2f 个数量级" % (aG_MGUT, aGUT, -dec4))

# ---- V5: 频率阶梯比值 ----
wW  = mW  / hbar; wpi = mpi / hbar; we = me / hbar
wGUT = MGUT / hbar
print("\n[V5] S02 频率阶梯比值（≡ 质量比）:")
print("  ω_W/ω_π = %.1f   ω_W/ω_e = %.3e   ω_GUT/ω_W = %.3e   ω_GUT/ω_π = %.3e"
      % (wW/wpi, wW/we, wGUT/wW, wGUT/wpi))

# ---- V6: SUSY-GUT 预言 sin²θ_W ----
a2_inv_mZ = 1.0 / (alpha_mZ / sin2W)                 # = 29.5788
# 跑动: 从交叉点(M_GUT) 向下, 1 TeV 以上 MSSM b2=1, 以下 SM b2=-19/6
a2_inv_1TeV = aG_inv_at_cross + (1.0/(2.0*math.pi)) * math.log(MGUT_cross/MSUSY)
a2_inv_mZ_pred = a2_inv_1TeV + (-19.0/6.0/(2.0*math.pi)) * math.log(MSUSY/mZ)
sin2W_pred = alpha_mZ * a2_inv_mZ_pred
dev6 = (sin2W_pred - sin2W) / sin2W * 100.0
print("\n[V6] SUSY-GUT 一循环预言 sin²θ_W(m_Z) (3/8 边界, 双阈值):")
print("  α₂⁻¹(m_Z)预言 = %.4f   sin²θ_W预言 = %.4f   偏差 = %+.2f%% (文献两循环+阈值≈0.231)"
      % (a2_inv_mZ_pred, sin2W_pred, dev6))

# ---- 图谱 + JSON ----
data = {"V1": {"alpha_div_alpha_w": sw_cand, "sin2W": sin2W, "dev_pct": dev1},
        "V2": {"mW_over_mZ": r_mass, "cosW": cosW, "dev_pct": dev2},
        "V3": {"rho": rho},
        "V4": {"MP_GeV": MP_GeV, "MGUT_over_MP": r_GUT, "aG_MGUT": aG_MGUT, "aGUT": aGUT},
        "V5": {"wW_wpi": wW/wpi, "wW_we": wW/we, "wGUT_wW": wGUT/wW, "wGUT_wpi": wGUT/wpi},
        "V6": {"sin2W_pred": sin2W_pred, "dev_pct": dev6}}
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "§20_开环检验数据.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("\n数据已写入: §20_开环检验数据.json")

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Weinberg 角候选来源对比 · 质量-耦合数值开环图谱</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0;}
  body{font-family:"Microsoft YaHei","PingFang SC",sans-serif;background:#f5f6f8;color:#1f2937;line-height:1.6;padding:20px;}
  .wrap{max-width:1080px;margin:0 auto;}
  header{background:linear-gradient(135deg,#0f172a,#1e3a5f);color:#fff;border-radius:14px;padding:22px 28px;margin-bottom:16px;}
  header h1{font-size:21px;}
  header .sub{font-size:13px;color:#cbd5e1;margin-top:8px;}
  .chartbox{background:#fff;border-radius:12px;padding:14px 16px;margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,.06);}
  #chart{width:100%;height:520px;}
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
  <h1>Weinberg 角候选来源对比（sin²θ_W）</h1>
  <div class="sub">S02 空间光速螺旋统一力 · §20 · 数据：§20_verify.py 实跑（α=1/137.035999084、α_w=1/29、sin²θ_W(m_Z)=0.23122、m_W=80.369 GeV、m_Z=91.1876 GeV）</div>
</header>

<div class="chartbox">
  <div id="chart"></div>
  <p class="note">红线 = 实验测量 sin²θ_W(m_Z)=0.23122。α/α_w=0.2116 偏差 +8.5%（量级巧合、非精确关系）；SUSY-GUT 一循环+双阈值预言 0.2272（偏差 −1.7%）；文献两循环+阈值修正约 0.231（~1% 吻合）→ Weinberg 角的真正来源是 GUT 边界条件+跑动，不是 S02 数值巧合。</p>
</div>

<div class="chartbox">
  <h3 style="font-size:16px;margin-bottom:10px;">§20 开环检验汇总</h3>
  <table>
    <tr><th>编号</th><th>检验项</th><th>结果</th><th>判定</th></tr>
    <tr><td>V2</td><td>m_W/m_Z vs cosθ_W</td><td>0.88135 vs 0.87679（+0.52%）</td><td class="ok">树级成立至 0.5%（辐射修正）</td></tr>
    <tr><td>V3</td><td>ρ = m_W²/(m_Z²cos²θ_W)</td><td>1.01043（SM: 1.0004±0.001）</td><td class="ok">W 质量张力量化（开环）</td></tr>
    <tr><td>V4</td><td>α_G(M_GUT) vs α_GUT</td><td>1.73×10⁻⁶ vs 0.0392</td><td class="ok">引力缺席 GUT（差 4.4 数量级）</td></tr>
    <tr><td>V5</td><td>S02 频率阶梯比值</td><td>595.4 / 1.573×10⁵ / 1.996×10¹⁴ / 1.189×10¹⁷</td><td class="no">≡ 质量比（身份重述，无预言）</td></tr>
  </table>
  <p class="note">结论：S02 的 ω↔m 公设是组织语言而非预言机制；质量数值仍由 Higgs 自发破缺+辐射修正+GUT 边界供给。</p>
</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"
        onerror="document.getElementById('chart').innerHTML='<p style=\\'padding:24px\\'>ECharts 加载失败（离线环境），请参照上方表格。</p>';"></script>
<script>
(function(){
  var el = document.getElementById('chart');
  if(!el || typeof echarts === 'undefined'){ return; }
  var chart = echarts.init(el);
  var option = {
    tooltip: { trigger: 'axis', triggerOn: 'mousemove|click', renderMode: 'richText', confine: true,
      formatter: function(params){
        if(!params || !params.length){ return ''; }
        var p = params[0];
        return p.name + String.fromCharCode(10) + 'sin²θ_W = ' + Number(p.value).toFixed(5);
      } },
    title: { text: 'sin²θ_W 候选来源对比', left: 'center', top: 6 },
    legend: { top: 30 },
    grid: { left: 70, right: 30, top: 66, bottom: 70 },
    xAxis: { type: 'category', data: ['α/α_w（S02 巧合）', 'SUSY-GUT 一循环预言', '实验测量（m_Z）', 'SUSY-GUT 两循环+阈值（文献）'],
      axisLabel: { interval: 0, width: 130, overflow: 'break', fontSize: 11 } },
    yAxis: { type: 'value', name: 'sin²θ_W', min: 0.20, max: 0.24 },
    series: [{
      name: 'sin²θ_W', type: 'bar',
      data: [0.21163, 0.22716, 0.23122, 0.23150],
      label: { show: true, position: 'top', fontSize: 11, formatter: function(p){ return Number(p.value).toFixed(4); } },
      markLine: { symbol: 'none', silent: true, label: { fontSize: 11, formatter: '实验 0.23122', position: 'insideEndTop' },
        data: [{ yAxis: 0.23122 }] }
    }]
  };
  chart.setOption(option);
  window.addEventListener('resize', function(){ chart.resize(); });
})();
</script>
</body>
</html>
"""

html_path = os.path.join(HERE, "§20_Weinberg角与质量比值_开环检验图谱.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
print("图谱已生成: %s" % html_path)

print("\n判定汇总: V1 巧合(+8.5%证伪为精确关系) / V2 树级+0.52% / V3 ρ=1.0104开环 / V4 引力缺席4.4量级 / V5 身份重述 / V6 GUT预言-1.7%(文献≈0.231)")
