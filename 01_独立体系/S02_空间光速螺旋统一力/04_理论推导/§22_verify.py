# -*- coding: utf-8 -*-
"""
§22_verify.py — β 能标公设审计：普朗克锁定三通道 + 收束判定
S02 空间光速螺旋统一力 · 算法联盟
V1  H≡β 术语统一 (pitch=2πH=2πβ)
V2  通道 A: 普朗克锁定动态剖面在宏观尺度的扭转量级
V3  通道 B: ECSK 背景挠率 Lorentz 破坏参数量级 vs SME 上限
V4  通道 C: §17 有效质量公式 at ρ=ℓ_P vs 光子质量上限
V5  判定矩阵 → 图谱/JSON
"""
import json, math, os

hbar = 1.054571817e-34
c = 2.99792458e8
lP = 1.616255e-35
mP_kg = math.sqrt(hbar * c / 6.67430e-11)      # 普朗克质量 (kg)
mP_GeV = 1.2209e19                              # 普朗克质量 (GeV)
mgamma_kg = 1e-54                               # 光子质量实验上限 (kg)
SME_GeV = 1e-43                                 # SME 双折射强约束参数上限 (文献量级, GeV)

print("=" * 70)
print("§22 β 能标公设审计 · 普朗克锁定三通道 + 收束判定")
print("=" * 70)

# ---- V1: H ≡ β ----
print("\n[V1] H≡β 术语统一:")
print("  螺旋线: z = H φ  (每弧度上升 H);  缺陷线: z' = z + β φ  (每弧度扭转 β)")
print("  pitch = 2πH = 2πβ  ⇒  H ≡ β;  Burgers b = 2πH ẑ = 2πβ ẑ")
print("  → S02 自 §17 即含扭转密度 (=H); β 能标问题 = H 能标问题")

# ---- V2: 通道 A ----
print("\n[V2] 通道 A: 普朗克锁定动态剖面 (H(ρ)=ρ²/ℓ_P):")
H1 = 1.0**2 / lP
gapA = math.log10(H1 / 1.0)
print("  H(1 m) = %.3e m  (每弧度扭转米数)" % H1)
print("  差距(相对宏观几何合理值 ~1 m) = %.1f 个数量级 → 几何荒谬" % gapA)

# ---- V3: 通道 B ----
print("\n[V3] 通道 B: ECSK 背景挠率 Lorentz 破坏:")
gapB = math.log10(mP_GeV / SME_GeV)
print("  |T|公设 ~ M_P = %.4e GeV   vs   SME 上限 ~ %.0e GeV (文献量级)" % (mP_GeV, SME_GeV))
print("  差距 = %.1f 个数量级 → Lorentz 破坏灾难" % gapB)

# ---- V4: 通道 C ----
print("\n[V4] 通道 C: 普朗克尺度有效质量 (§17 公式 m_eff=ℏ/(cρ)):")
m_eff = hbar / (c * lP)
gapC = math.log10(m_eff / mgamma_kg)
print("  m_eff(ℓ_P) = %.3e kg   vs   光子质量上限 %.0e kg" % (m_eff, mgamma_kg))
print("  差距 = %.1f 个数量级 → 质量灾难" % gapC)

# ---- V5: 判定矩阵 ----
print("\n[V5] 判定矩阵:")
matrix = [
    ("通道 A 动态剖面", H1, "宏观扭转 ~1 m", gapA),
    ("通道 B ECSK 耦合", mP_GeV, "SME ~1e-43 GeV", gapB),
    ("通道 C 有效质量", m_eff, "上限 1e-54 kg", gapC),
]
for name, val, lim, gap in matrix:
    print("  %-16s 公设=%.3e  vs  %-18s 差距=%5.1f 数量级 → %s"
          % (name, val, lim, gap, "❌ 证伪" if gap > 20 else "✅ 自洽"))

data = {"V1": {"H_equiv_beta": True, "pitch": "2πH=2πβ"},
        "V2": {"H_1m_m": H1, "gap_orders": round(gapA, 1)},
        "V3": {"T_GeV": mP_GeV, "SME_GeV": SME_GeV, "gap_orders": round(gapB, 1)},
        "V4": {"meff_kg": m_eff, "mgamma_kg": mgamma_kg, "gap_orders": round(gapC, 1)},
        "V5": {"channels": [n for n, _, _, _ in matrix],
               "gaps": [round(g, 1) for _, _, _, g in matrix]}}
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "§22_收束检验数据.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("\n数据已写入: §22_收束检验数据.json")

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>S02 普朗克锁定候选的排除因子</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0;}
  body{font-family:"Microsoft YaHei","PingFang SC",sans-serif;background:#f5f6f8;color:#1f2937;line-height:1.6;padding:20px;}
  .wrap{max-width:1080px;margin:0 auto;}
  header{background:linear-gradient(135deg,#0f172a,#1e3a5f);color:#fff;border-radius:14px;padding:22px 28px;margin-bottom:16px;}
  header h1{font-size:21px;}
  header .sub{font-size:13px;color:#cbd5e1;margin-top:8px;}
  .chartbox{background:#fff;border-radius:12px;padding:14px 16px;margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,.06);}
  #chart{width:100%;height:480px;}
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
  <h1>S02 普朗克锁定候选的排除因子（数量级）</h1>
  <div class="sub">S02 空间光速螺旋统一力 · §22 · 数据：§22_verify.py 实跑；Y 轴对数；柱顶数字 = 公设值与实验/几何上限的数量级差距</div>
</header>

<div class="chartbox">
  <div id="chart"></div>
  <p class="note">三个物理化通道（动态剖面 / ECSK 耦合 / 有效质量）的普朗克锁定公设分别被几何合理性、SME Lorentz 破坏上限（~10⁻⁴³ GeV）与光子质量上限（10⁻⁵⁴ kg）排除 35 / 62 / 46 个数量级。唯一自洽的选项是"不耦合的纯几何缺陷线"——自洽但零内容。</p>
</div>

<div class="chartbox">
  <h3 style="font-size:16px;margin-bottom:10px;">§22 收束判定</h3>
  <table>
    <tr><th>出路</th><th>审计链（§17–§22）</th><th>终审</th></tr>
    <tr><td>① 四力机制</td><td>§18 形式化 → §19 数值统一失败 → §20 质量预言失败 → §21 可观测性压制 → §22 锁定不自洽</td><td class="no">关闭</td></tr>
    <tr><td>② 几何语言</td><td>§17 坐标改写自洽 · §21 扭转映射 · §22 H≡β 术语统一</td><td class="ok">保留（组织性语言）</td></tr>
    <tr><td>③ 预言理论</td><td>§20 身份重述 → §21 无 β 来源 → §22 锁定不自洽</td><td class="no">关闭</td></tr>
  </table>
  <p class="note">收束判词：普朗克锁定不存在自洽实现——要么与实验矛盾，要么零内容。S02 作为组织性语言成立、作为预言机制不成立，是 §17 以来六节审计的一致终点。</p>
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
        return p.name + String.fromCharCode(10) + '公设值超出上限 ' + p.value + ' 个数量级';
      } },
    title: { text: '普朗克锁定候选的排除因子（数量级差距）', left: 'center', top: 6 },
    legend: { top: 30 },
    grid: { left: 70, right: 30, top: 66, bottom: 70, containLabel: true },
    xAxis: { type: 'category',
      data: ['动态剖面(宏观扭转)', 'ECSK 耦合(Lorentz 破坏)', '有效质量(光子质量)'],
      axisLabel: { interval: 0, width: 160, overflow: 'break', fontSize: 11 } },
    yAxis: { type: 'value', name: '数量级差距', min: 0, max: 70 },
    series: [{
      name: '排除因子', type: 'bar',
      data: [35, 62, 46],
      label: { show: true, position: 'top', fontSize: 12, formatter: function(p){ return p.value + ' 数量级'; } }
    }]
  };
  chart.setOption(option);
  window.addEventListener('resize', function(){ chart.resize(); });
})();
</script>
</body>
</html>
"""

html_path = os.path.join(HERE, "§22_普朗克锁定排除因子图谱.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
print("图谱已生成: %s" % html_path)

print("\n判定: 通道 A/B/C 全部证伪 (35/62/46); 通道 D (不耦合) 自洽零内容 → S02 物理化路线收束关闭")
