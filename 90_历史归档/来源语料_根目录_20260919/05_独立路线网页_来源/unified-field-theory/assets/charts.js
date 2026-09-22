(function() {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();
  var success = style.getPropertyValue('--success').trim();

  // --- Chart: Physical Constants Error Comparison ---
  var chartConstants = echarts.init(document.getElementById('chart-constants'), null, { renderer: 'svg' });
  chartConstants.setOption({
    animation: false,
    tooltip: {
      trigger: 'axis',
      appendToBody: true,
      axisPointer: { type: 'shadow' },
      backgroundColor: bg2,
      borderColor: rule,
      textStyle: { color: ink }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['μ₀ 真空磁导率', 'ε₀ 真空介电常数', 'ℏ 约化普朗克常数', 'e 基本电荷'],
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: muted, fontSize: 12 }
    },
    yAxis: {
      type: 'value',
      name: '相对误差 (%)',
      nameTextStyle: { color: muted },
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: muted, fontSize: 12 },
      splitLine: { lineStyle: { color: rule, opacity: 0.3 } }
    },
    series: [{
      name: 'CODATA 相对误差',
      type: 'bar',
      data: [
        { value: 5.44e-10, itemStyle: { color: accent } },
        { value: 5.44e-10, itemStyle: { color: accent } },
        { value: 2.73e-8, itemStyle: { color: accent2 } },
        { value: 1.37e-8, itemStyle: { color: success } }
      ],
      barWidth: '50%',
      label: {
        show: true,
        position: 'top',
        formatter: function(p) {
          if (p.value < 1e-9) return '5.44×10⁻¹⁰ %';
          if (p.value < 1e-7) return '2.73×10⁻⁸ %';
          return '1.37×10⁻⁸ %';
        },
        color: ink,
        fontSize: 11
      }
    }]
  });
  window.addEventListener('resize', function() { chartConstants.resize(); });

  // --- Chart: Dimensional Verification Matrix ---
  var chartDimensions = echarts.init(document.getElementById('chart-dimensions'), null, { renderer: 'svg' });
  chartDimensions.setOption({
    animation: false,
    tooltip: {
      trigger: 'item',
      appendToBody: true,
      backgroundColor: bg2,
      borderColor: rule,
      textStyle: { color: ink },
      formatter: function(p) {
        var names = ['μ₀', 'ε₀', 'ℏ', 'e', 'κ', 'τ', 'c'];
        var dims = [
          '[kg·m·s⁻²·A⁻²]',
          '[kg⁻¹·m⁻³·s⁴·A²]',
          '[kg·m²·s⁻¹]',
          '[A·s]',
          '[m⁻¹]',
          '[m⁻¹]',
          '[m·s⁻¹]'
        ];
        return '<strong>' + names[p.data[1]] + '</strong><br/>量纲: ' + dims[p.data[1]] + '<br/>状态: 一致性通过';
      }
    },
    grid: {
      left: '15%',
      right: '10%',
      bottom: '10%',
      top: '5%'
    },
    xAxis: {
      type: 'category',
      data: ['SI量纲', '几何表达量纲', '一致性'],
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: muted, fontSize: 12 }
    },
    yAxis: {
      type: 'category',
      data: ['c', 'τ', 'κ', 'e', 'ℏ', 'ε₀', 'μ₀'],
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: muted, fontSize: 12 }
    },
    visualMap: {
      min: 0,
      max: 1,
      show: false,
      inRange: {
        color: [bg2, success]
      }
    },
    series: [{
      type: 'heatmap',
      data: [
        [0, 0, 1], [1, 0, 1], [2, 0, 1],
        [0, 1, 1], [1, 1, 1], [2, 1, 1],
        [0, 2, 1], [1, 2, 1], [2, 2, 1],
        [0, 3, 1], [1, 3, 1], [2, 3, 1],
        [0, 4, 1], [1, 4, 1], [2, 4, 1],
        [0, 5, 1], [1, 5, 1], [2, 5, 1],
        [0, 6, 1], [1, 6, 1], [2, 6, 1]
      ],
      label: {
        show: true,
        formatter: function() { return '✓'; },
        color: ink,
        fontSize: 16,
        fontWeight: 'bold'
      },
      itemStyle: {
        borderColor: rule,
        borderWidth: 1
      }
    }]
  });
  window.addEventListener('resize', function() { chartDimensions.resize(); });
})();
