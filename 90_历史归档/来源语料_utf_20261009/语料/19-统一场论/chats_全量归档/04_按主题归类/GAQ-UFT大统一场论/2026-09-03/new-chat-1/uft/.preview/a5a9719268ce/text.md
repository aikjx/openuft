<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>全维统一场论 · 知识图谱</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:#F4F3EE; font-family:'Roboto','PingFang SC','Segoe UI',Arial,sans-serif; color:#1A1B1C; padding:16px; }
  .wrap { max-width:1080px; margin:0 auto; }
  h1 { font-size:20px; font-weight:600; margin:8px 0 4px; }
  .sub { font-size:13px; color:#6B7280; margin-bottom:12px; line-height:1.6; }
  #chart { width:100%; height:620px; background:#FFFFFF; border-radius:14px; border:1px solid #E4E3DD; }
  .legend-note { font-size:12px; color:#6B7280; margin-top:8px; line-height:1.7; }
  .legend-note b { color:#1A1B1C; }
  .fallback { display:none; padding:20px; background:#fff; border-radius:14px; border:1px solid #E4E3DD; font-size:13px; line-height:1.8; }
  .fallback h3 { margin-bottom:8px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>全维统一场论 · 全维度知识图谱</h1>
  <div class="sub">从对称性公理 → 规范群/时空结构 → 场方程 → Noether 守恒 → 实验验证/证伪 的完整关系网。节点按类型着色，连线为"生成/嵌入/约化/证伪"等关系；可拖拽、缩放、点击节点查看详情。</div>
  <div id="chart"></div>
  <div class="legend-note">
    <b>节点类型：</b>对称性原理（蓝）｜群/时空结构（紫）｜方程/机制（绿）｜守恒律（橙）｜实验/验证（青）<br>
    <b>验证状态：</b>✅ 已验证（L0–L4）｜⚠️ 理论自洽·部分模型被证伪（L5）｜❌ 未验证/未探测（L6–L8）。
    本图为文档《全维统一场论·全维度修订版》第 5 节三元组知识图谱的可视化。
  </div>
  <div class="fallback" id="fb">
    <h3>图表加载失败（CDN 不可用）</h3>
    无法加载 ECharts 库，以下为图谱的结构化文本等价物：<br>
    · 微分同胚不变性 →(Noether) Einstein 方程 →(Bianchi) ∇T=0 ✅<br>
    · 局域规范不变性 →(Noether 第二定理) Yang-Mills 方程 →(Bianchi) D J=0 ✅<br>
    · SU(2)_L×U(1)_Y →(Higgs 自发破缺) U(1)_em，m_W/m_Z=cosθ_W ✅<br>
    · SU(3)×SU(2)×U(1) →(嵌入) SU(5)；MSSM 下 RG 近精确汇合于 M_GUT≈1.3e16 GeV ⚠️<br>
    · 最小非超对称 SU(5) →(被 Super-K 证伪，τ_p>2.4e34yr) ❌<br>
    · SO(10) →(预言) 右手中微子 + 跷跷板 → m_ν≈0.1eV ⚠️<br>
    · 5 维纯引力 →(KK 约化) 4 维引力 + U(1) 规范场 + dilaton 标量场 ❌<br>
    · 局域超对称 →(包含) Rarita-Schwinger/引力微子 ❌<br>
    · 10 维超弦 →(Calabi-Yau 紧致化) 4 维超引力有效场论 ❌<br>
    · Ashtekar 变量 →(正则量子化) 圈量子引力（面积谱 8πγℓ_P²√(j(j+1))）❌<br>
    · 耦合量纲 [g²]=4-D → 只有 D=4 可重整；Lovelock 定理 → D>4 时 GR 非唯一（全维度约束）
  </div>
</div>
<script>
(function(){
  try {
    if (typeof echarts === 'undefined') { throw new Error('no echarts'); }
    var dom = document.getElementById('chart');
    if (!dom) { throw new Error('no dom'); }
    var chart = echarts.init(dom);

    var cats = [
      { name: '对称性原理', itemStyle: { color: '#9BBBF4' } },
      { name: '群/时空结构', itemStyle: { color: '#C9A7E8' } },
      { name: '方程/机制', itemStyle: { color: '#94D8C3' } },
      { name: '守恒律', itemStyle: { color: '#F4B393' } },
      { name: '实验/验证', itemStyle: { color: '#8BC8EA' } }
    ];

    var nodes = [
      // 对称性原理 (cat 0)
      { id: 'Diff', name: '微分同胚\n不变性', category: 0, symbolSize: 26 },
      { id: 'Gauge', name: '局域规范\n不变性', category: 0, symbolSize: 26 },
      { id: 'GlobalU1', name: '全局 U(1)', category: 0, symbolSize: 22 },
      { id: 'SUSYsym', name: '局域超对称', category: 0, symbolSize: 22 },
      { id: 'RGsym', name: '重整化\n不变性', category: 0, symbolSize: 22 },
      // 群/时空结构 (cat 1)
      { id: 'SM', name: 'SU(3)×SU(2)\n×U(1)', category: 1, symbolSize: 30 },
      { id: 'EW', name: 'SU(2)_L\n×U(1)_Y', category: 1, symbolSize: 26 },
      { id: 'U1', name: 'U(1)_em', category: 1, symbolSize: 24 },
      { id: 'SU5', name: 'SU(5)', category: 1, symbolSize: 26 },
      { id: 'minSU5', name: '最小非超对称\nSU(5)', category: 1, symbolSize: 24 },
      { id: 'SO10', name: 'SO(10)', category: 1, symbolSize: 26 },
      { id: 'MSSM', name: 'MSSM-GUT', category: 1, symbolSize: 26 },
      { id: 'KK5', name: '5 维纯引力', category: 1, symbolSize: 26 },
      { id: 'String', name: '10 维超弦', category: 1, symbolSize: 26 },
      { id: 'LQG', name: '圈量子引力', category: 1, symbolSize: 26 },
      { id: 'Ashtekar', name: 'Ashtekar\n变量', category: 1, symbolSize: 22 },
      // 方程/机制 (cat 2)
      { id: 'Einstein', name: 'Einstein 方程', category: 2, symbolSize: 30 },
      { id: 'YM', name: 'Yang-Mills\n方程', category: 2, symbolSize: 28 },
      { id: 'Dirac', name: 'Dirac 方程', category: 2, symbolSize: 24 },
      { id: 'KG', name: 'Higgs/KG\n方程', category: 2, symbolSize: 24 },
      { id: 'Higgs', name: 'Higgs 机制', category: 2, symbolSize: 26 },
      { id: 'KK', name: 'KK 约化\n(4D引力+U1+dilaton)', category: 2, symbolSize: 26 },
      { id: 'Seesaw', name: '跷跷板机制', category: 2, symbolSize: 24 },
      { id: 'RS', name: 'Rarita-Schwinger\n(引力微子)', category: 2, symbolSize: 24 },
      { id: 'Area', name: '面积算符谱', category: 2, symbolSize: 22 },
      { id: 'MPl', name: 'M_Pl²=2πR·M_5³', category: 2, symbolSize: 22 },
      { id: 'Ddim', name: '[g²]=4-D\n只有 D=4 可重整', category: 2, symbolSize: 24 },
      { id: 'Lovelock', name: 'Lovelock 定理\n(D>4 GR非唯一)', category: 2, symbolSize: 24 },
      // 守恒律 (cat 3)
      { id: 'divT', name: '∇T^{μν}=0\n能量动量守恒', category: 3, symbolSize: 22 },
      { id: 'divJ', name: 'D_μ J^{aμ}=0', category: 3, symbolSize: 22 },
      { id: 'Q', name: '电荷守恒', category: 3, symbolSize: 20 },
      // 实验/验证 (cat 4)
      { id: 'SK', name: 'Super-K\n质子衰变', category: 4, symbolSize: 26 },
      { id: 'EW1979', name: '电弱统一 1979\nm_W/m_Z=cosθ_W', category: 4, symbolSize: 26 },
      { id: 'GW', name: 'GW170817\n引力波-光速差', category: 4, symbolSize: 24 },
      { id: 'Grav', name: '亚毫米引力\n实验', category: 4, symbolSize: 24 },
      { id: 'MGUT', name: 'M_GUT≈1.3e16 GeV\nα_GUT^{-1}≈26', category: 4, symbolSize: 26 },
      { id: 'SKbound', name: 'τ_p>2.4e34 年', category: 4, symbolSize: 22 }
    ];

    var links = [
      { source: 'Diff', target: 'Einstein', label: 'Noether 生成' },
      { source: 'Diff', target: 'divT', label: '守恒' },
      { source: 'Gauge', target: 'YM', label: 'Noether 第二定理' },
      { source: 'Gauge', target: 'divJ', label: '协变守恒' },
      { source: 'GlobalU1', target: 'Q', label: '守恒' },
      { source: 'GlobalU1', target: 'Dirac', label: '作用量对称' },
      { source: 'EW', target: 'U1', label: '自发破缺' },
      { source: 'Higgs', target: 'U1', label: '给出质量' },
      { source: 'EW', target: 'Higgs', label: '包含' },
      { source: 'SM', target: 'SU5', label: '嵌入' },
      { source: 'SM', target: 'SO10', label: '嵌入' },
      { source: 'SO10', target: 'SU5', label: '含子群' },
      { source: 'minSU5', target: 'SU5', label: '特例' },
      { source: 'SO10', target: 'Seesaw', label: '预言右手中微子' },
      { source: 'KK5', target: 'KK', label: 'KK 约化' },
      { source: 'KK', target: 'MPl', label: '量纲关系' },
      { source: 'SUSYsym', target: 'RS', label: '必含' },
      { source: 'String', target: 'KK', label: 'Calabi-Yau 紧致化' },
      { source: 'Ashtekar', target: 'LQG', label: '正则量子化' },
      { source: 'LQG', target: 'Area', label: '离散面积谱' },
      { source: 'RGsym', target: 'MGUT', label: 'RG 流动汇合' },
      { source: 'MSSM', target: 'MGUT', label: '近精确汇合' },
      { source: 'SM', target: 'MGUT', label: 'SM 不汇合(9-13%)' },
      { source: 'SK', target: 'minSU5', label: '证伪' },
      { source: 'SK', target: 'SKbound', label: '给出上限' },
      { source: 'EW', target: 'EW1979', label: '验证' },
      { source: 'Einstein', target: 'GW', label: '验证' },
      { source: 'KK', target: 'Grav', label: '约束 M_5>3.6e8 GeV' },
      { source: 'Ddim', target: 'Lovelock', label: '全维度约束' },
      { source: 'Ddim', target: 'KK', label: '维度条件' }
    ];

    var data = nodes.map(function(n){
      var tooltip = n.name.replace(/\n/g, '');
      var extra = {
        Diff: '✅ 已验证 | 附录 V1/V2',
        Gauge: '✅ 已验证 | 附录 V3/V4',
        Einstein: '✅ L0 | Bianchi→∇T=0',
        YM: '✅ L1/L3 | U(1)与SU(2)符号验证',
        Dirac: '✅ L2 | 手征结构',
        KG: '✅ L2/L4 | E-L=0',
        Higgs: '✅ L4 | v=246.22 GeV',
        EW: '✅ L4 | 1979 诺贝尔奖',
        U1: '✅ L4 | 剩余对称',
        SM: '✅ L0-L3 | 已验证',
        SU5: '⚠️ L5 | 理论自洽未验证',
        minSU5: '❌ L5 | 被 SK 证伪(两重原因)',
        SO10: '⚠️ L5 | 最自洽候选',
        MSSM: '⚠️ L5 | 依赖未发现的超伴子',
        KK: '❌ L7 | 符号验证成立但无实验',
        KK5: '❌ L7 | 推测',
        String: '❌ L8 | 数学自洽',
        LQG: '❌ L8 | 与弦论不兼容',
        Area: '❌ L8 | 附录 N7: j=1/2→5.17ℓ_P²',
        Seesaw: '⚠️ L5 | m_ν≈0.1eV, 附录 N5',
        RS: '❌ L6 | 未探测到',
        SK: '❌ L5 | τ_p>2.4e34yr (PRD102)',
        MGUT: '⚠️ L5 | 单圈基准值, 附录 N3',
        divT: '✅ | Noether 第一/第二定理',
        divJ: '✅ | Noether 协变守恒',
        Q: '✅ | 全局 U(1)',
        EW1979: '✅ | 唯一被实验证实的统一',
        GW: '✅ | 速度差 ~10⁻¹⁵',
        Grav: '✅ | R<0.1mm 约束',
        MPl: '❌ L7 | 量纲锚点',
        Ddim: '✅ | [g²]=4-D 第一性原理',
        Lovelock: '✅ | D>4 GR 非唯一',
        SKbound: '❌ | 实验事实',
        SUSYsym: '❌ L6 | 未验证',
        RGsym: '✅ | 重整化群',
        GlobalU1: '✅ | 对称性',
        Ashtekar: '❌ L8 | 推测'
      };
      return {
        id: n.id, name: n.name, category: n.category, symbolSize: n.symbolSize,
        tooltip: { formatter: function(){ return '<b>' + tooltip + '</b><br>' + (extra[n.id] || ''); } }
      };
    });

    var linkData = links.map(function(l){
      return { source: l.source, target: l.target, label: { show: false }, lineStyle: { width: 1.2, opacity: 0.55 } };
    });

    chart.setOption({
      backgroundColor: 'transparent',
      title: { text: '', left: 'center' },
      tooltip: {
        trigger: 'item', triggerOn: 'click', renderMode: 'richText', confine: true,
        textStyle: { fontSize: 12, lineHeight: 18 }, padding: [8, 10]
      },
      legend: [{
        data: cats.map(function(c){ return c.name; }),
        top: 8, left: 'center', itemWidth: 14, itemHeight: 10,
        textStyle: { color: '#1A1B1C', fontSize: 12 }
      }],
      animationDuration: 800,
      animationDurationUpdate: 800,
      series: [{
        type: 'graph', layout: 'force', roam: true, draggable: true,
        top: 52, left: 8, right: 8, bottom: 8,
        data: data,
        links: linkData,
        categories: cats,
        focusNodeAdjacency: true,
        force: { repulsion: 520, edgeLength: [70, 150], gravity: 0.08 },
        label: { show: true, position: 'bottom', fontSize: 10, color: '#1A1B1C', lineHeight: 13 },
        lineStyle: { color: 'source', curveness: 0.06, opacity: 0.5 },
        emphasis: { focus: 'adjacency', lineStyle: { width: 3 } },
        edgeLabel: { show: false }
      }]
    });

    // 点击节点显示标签说明（揭示信息增量）
    chart.on('click', function(params){
      if (params.dataType === 'node') {
        var idx = params.dataIndex;
        var extra = {
          Diff: '对称性原理：时空中每个"重标号"都不改变物理 → Noether 给出能量-动量守恒。',
          Gauge: '对称性原理：每个点独立旋转相位 → Noether 第二定理给出 YM 场方程。',
          Einstein: '场方程：G_μν+Λg_μν=κ²T_μν。附录 V1/V2 已验证变分推导与 Friedmann 还原。',
          YM: '场方程：D_μF^{aμν}=J^{aν}。附录 V3(电磁)、V4(SU(2)) 已符号验证。',
          Dirac: '场方程：(iγ^μD_μ-m)ψ=0。附录 V5 由 E-L 直接给出。',
          KG: '场方程：D²Φ+V′(Φ)=0。附录 V6 验证 + Noether 守恒。',
          Higgs: '机制：μ²<0 → v=(√2G_F)^{-1/2}=246.22 GeV。',
          EW: '电弱统一：SU(2)×U(1)→U(1)_em，1979 年诺贝尔奖，唯一被证实的大统一。',
          U1: '破缺后剩余对称：电磁 U(1)。',
          SM: '标准模型：SU(3)×SU(2)×U(1)，L0-L3 全部已验证。',
          SU5: '大统一群：装入 15 个费米子一代；理论自洽但未验证。',
          minSU5: '被排除：①耦合不汇合(偏差9-13%)；②τ_p<2.4e34yr 被 SK 毙掉。',
          SO10: '16 维旋量 = 5̄⊕10⊕1，天然含右手中微子。',
          MSSM: '加入超对称后耦合近精确汇合(偏离<2%)，最强间接证据。',
          KK: '5维纯引力 = 4维引力+U(1)+dilaton。恒等式 R5=R4-(φ/4)F²+½(∂φ)²/φ²-(1/φ)□φ 已符号验证。',
          KK5: 'KK 起点：5 维纯 Einstein-Hilbert 作用量。',
          String: '10 维超弦，Calabi-Yau 紧致化 → 4 维有效理论；α′→0 还原超引力。',
          LQG: '背景无关量子几何；面积谱离散化；与弦论互不兼容。',
          Area: 'Â=8πγℓ_P²√(j(j+1))，γ=0.2375；j=1/2 → 5.17ℓ_P²。',
          Seesaw: 'm_ν=m_D²/M_R：100²/10¹⁴ GeV = 0.1 eV，与大气中微子同量级。',
          RS: '自旋 3/2 超伴子，LHC 未发现。',
          SK: 'Super-Kamiokande：盯质子数十年，零候选事件。',
          MGUT: 'MSSM 汇合点：M_SUSY=1TeV → M_GUT=1.43e16 GeV，α^{-1}=25.6。',
          divT: '微分同胚不变性的 Noether 后果：能量-动量自动守恒。',
          divJ: '局域规范不变性的 Noether 后果：流协变守恒。',
          Q: '全局 U(1) 的 Noether 荷。',
          EW1979: 'm_W/m_Z=cosθ_W=0.8768，v=246.22 GeV（附录 N2）。',
          GW: '引力波与光速差 ~10⁻¹⁵（FIX-10 口径澄清）。',
          Grav: '亚毫米引力实验：R≤0.1mm → M_5≥3.6e8 GeV（FIX-14）。',
          MPl: 'M_Pl²=2πR·M_5³：若 M_5=1TeV，R≈31AU 被排除。',
          Ddim: '全维度约束：[g²]=4-D，只有 D=4 可重整（FIX-2）。',
          Lovelock: '全维度约束：D>4 时 GR 非唯一，需 Gauss-Bonnet 等项（FIX-4）。',
          SKbound: '实验事实：τ(p→e⁺π⁰)>2.4e34 年 @90%C.L.（PRD 102,112011）。',
          SUSYsym: '局域超对称：玻色子-费米子配对，解决层级问题；未验证。',
          RGsym: '重整化群：耦合随能标流动。',
          GlobalU1: '全局相位对称 → 电荷守恒。',
          Ashtekar: 'LQG 的相空间变量 (A,E)。'
        };
        if (extra[n.id]) { chart.setOption({ graphic: [{ type: 'text', left: 'center', top: 26, style: { text: '', fontSize: 12, fill: '#333' } }] }); }
      }
    });

    window.addEventListener('resize', function(){ chart.resize(); });
  } catch (e) {
    document.getElementById('fb').style.display = 'block';
    document.getElementById('chart').style.display = 'none';
  }
})();
</script>
</body>
</html>
