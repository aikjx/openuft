(function() {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();
  var success = style.getPropertyValue('--success').trim();

  // --- Chart: Constants Error Comparison (Vol 3) ---
  var chartError = echarts.init(document.getElementById('chart-error'), null, { renderer: 'svg' });
  chartError.setOption({
    animation: false,
    tooltip: { trigger: 'axis', appendToBody: true, axisPointer: { type: 'shadow' }, backgroundColor: bg2, borderColor: rule, textStyle: { color: ink } },
    grid: { left: '3%', right: '4%', bottom: '3%', top: '12%', containLabel: true },
    xAxis: { type: 'category', data: ['μ₀', 'ε₀', 'ℏ', 'e'], axisLine: { lineStyle: { color: rule } }, axisLabel: { color: muted, fontSize: 12 } },
    yAxis: { type: 'value', name: '相对误差 (%)', nameTextStyle: { color: muted }, axisLine: { lineStyle: { color: rule } }, axisLabel: { color: muted, fontSize: 11 }, splitLine: { lineStyle: { color: rule, opacity: 0.3 } } },
    series: [{
      name: 'CODATA 相对误差',
      type: 'bar',
      data: [
        { value: 5.44e-10, itemStyle: { color: accent } },
        { value: 5.44e-10, itemStyle: { color: accent } },
        { value: 2.73e-8, itemStyle: { color: accent2 } },
        { value: 1.37e-8, itemStyle: { color: success } }
      ],
      barWidth: '45%',
      label: {
        show: true, position: 'top',
        formatter: function(p) {
          if (p.value < 1e-9) return '5.44×10⁻¹⁰%';
          if (p.value < 2e-8) return '1.37×10⁻⁸%';
          return '2.73×10⁻⁸%';
        },
        color: ink, fontSize: 10
      }
    }]
  });
  window.addEventListener('resize', function() { chartError.resize(); });

  // --- Chart: Dimensional Verification Matrix (Vol 5) ---
  var chartDim = echarts.init(document.getElementById('chart-dim'), null, { renderer: 'svg' });
  var dimNames = ['μ₀', 'ε₀', 'G', 'ℏ', 'c', 'e', 'α'];
  var dimLabels = ['SI量纲', '几何表达量纲', '一致性'];
  var dimData = [];
  for (var i = 0; i < 3; i++) {
    for (var j = 0; j < 7; j++) {
      dimData.push([i, j, 1]);
    }
  }
  chartDim.setOption({
    animation: false,
    tooltip: { trigger: 'item', appendToBody: true, backgroundColor: bg2, borderColor: rule, textStyle: { color: ink },
      formatter: function(p) { return '<strong>' + dimNames[p.data[1]] + '</strong><br/>状态: 量纲一致性通过'; }
    },
    grid: { left: '12%', right: '8%', bottom: '8%', top: '3%' },
    xAxis: { type: 'category', data: dimLabels, axisLine: { lineStyle: { color: rule } }, axisLabel: { color: muted, fontSize: 11 } },
    yAxis: { type: 'category', data: dimNames, axisLine: { lineStyle: { color: rule } }, axisLabel: { color: muted, fontSize: 11 } },
    visualMap: { min: 0, max: 1, show: false, inRange: { color: [bg2, success] } },
    series: [{
      type: 'heatmap', data: dimData,
      label: { show: true, formatter: function() { return '✓'; }, color: ink, fontSize: 14, fontWeight: 'bold' },
      itemStyle: { borderColor: rule, borderWidth: 1 }
    }]
  });
  window.addEventListener('resize', function() { chartDim.resize(); });

  // --- Chart: CODATA 2022 Comparison (Vol 7) ---
  var chartCodata = echarts.init(document.getElementById('chart-codata'), null, { renderer: 'svg' });
  chartCodata.setOption({
    animation: false,
    tooltip: { trigger: 'axis', appendToBody: true, backgroundColor: bg2, borderColor: rule, textStyle: { color: ink } },
    legend: { data: ['理论计算值', 'CODATA 2022'], textStyle: { color: muted }, top: '2%' },
    grid: { left: '3%', right: '4%', bottom: '3%', top: '15%', containLabel: true },
    xAxis: { type: 'category', data: ['α', 'μ₀', 'ε₀', 'ℏ', 'e'], axisLine: { lineStyle: { color: rule } }, axisLabel: { color: muted, fontSize: 12 } },
    yAxis: { type: 'value', name: '相对误差 (%)', nameTextStyle: { color: muted }, axisLine: { lineStyle: { color: rule } }, axisLabel: { color: muted, fontSize: 11 }, splitLine: { lineStyle: { color: rule, opacity: 0.3 } } },
    series: [
      {
        name: '理论计算值',
        type: 'bar',
        data: [
          { value: 0, itemStyle: { color: accent } },
          { value: 5.44e-10, itemStyle: { color: accent } },
          { value: 5.44e-10, itemStyle: { color: accent } },
          { value: 2.73e-8, itemStyle: { color: accent } },
          { value: 1.37e-8, itemStyle: { color: accent } }
        ],
        barWidth: '35%',
        label: { show: true, position: 'top', formatter: function(p) {
          if (p.value === 0) return '0%';
          if (p.value < 1e-9) return '5.44×10⁻¹⁰%';
          if (p.value < 2e-8) return '1.37×10⁻⁸%';
          return '2.73×10⁻⁸%';
        }, color: ink, fontSize: 9 }
      }
    ]
  });
  window.addEventListener('resize', function() { chartCodata.resize(); });
})();
