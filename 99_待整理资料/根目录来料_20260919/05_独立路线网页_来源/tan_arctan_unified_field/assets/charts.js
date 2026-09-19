(function() {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();

  // --- Chart: tan function ---
  var chartTan = echarts.init(document.getElementById('chart-tan'), null, { renderer: 'svg' });
  var tanData = [];
  for (var i = -89; i <= 89; i += 0.5) {
    var rad = i * Math.PI / 180;
    tanData.push([i, Math.tan(rad)]);
  }
  chartTan.setOption({
    animation: false,
    tooltip: { trigger: 'axis', appendToBody: true },
    grid: { left: '10%', right: '5%', top: '10%', bottom: '15%' },
    xAxis: {
      type: 'value',
      name: '角度 θ (°)',
      nameLocation: 'middle',
      nameGap: 30,
      min: -90,
      max: 90,
      axisLine: { lineStyle: { color: muted } },
      axisLabel: { color: muted },
      splitLine: { lineStyle: { color: rule } }
    },
    yAxis: {
      type: 'value',
      name: 'tan(θ)',
      nameLocation: 'middle',
      nameGap: 40,
      min: -10,
      max: 10,
      axisLine: { lineStyle: { color: muted } },
      axisLabel: { color: muted },
      splitLine: { lineStyle: { color: rule } }
    },
    series: [{
      type: 'line',
      data: tanData,
      smooth: false,
      lineStyle: { color: accent, width: 2 },
      itemStyle: { color: accent },
      showSymbol: false
    }],
    markLine: {
      silent: true,
      lineStyle: { color: muted, type: 'dashed' },
      data: [
        { xAxis: -90 },
        { xAxis: 90 },
        { yAxis: 0 }
      ]
    }
  });
  window.addEventListener('resize', function() { chartTan.resize(); });

  // --- Chart: arctan function ---
  var chartArctan = echarts.init(document.getElementById('chart-arctan'), null, { renderer: 'svg' });
  var arctanData = [];
  for (var x = -100; x <= 100; x += 0.5) {
    arctanData.push([x, Math.atan(x) * 180 / Math.PI]);
  }
  chartArctan.setOption({
    animation: false,
    tooltip: { trigger: 'axis', appendToBody: true },
    grid: { left: '10%', right: '5%', top: '10%', bottom: '15%' },
    xAxis: {
      type: 'value',
      name: '坡度 x',
      nameLocation: 'middle',
      nameGap: 30,
      min: -100,
      max: 100,
      axisLine: { lineStyle: { color: muted } },
      axisLabel: { color: muted },
      splitLine: { lineStyle: { color: rule } }
    },
    yAxis: {
      type: 'value',
      name: 'arctan(x) (°)',
      nameLocation: 'middle',
      nameGap: 50,
      min: -90,
      max: 90,
      axisLine: { lineStyle: { color: muted } },
      axisLabel: { color: muted },
      splitLine: { lineStyle: { color: rule } }
    },
    series: [{
      type: 'line',
      data: arctanData,
      smooth: false,
      lineStyle: { color: accent2, width: 2 },
      itemStyle: { color: accent2 },
      showSymbol: false
    }],
    markLine: {
      silent: true,
      lineStyle: { color: muted, type: 'dashed' },
      data: [
        { yAxis: -90 },
        { yAxis: 90 },
        { yAxis: 0 }
      ]
    }
  });
  window.addEventListener('resize', function() { chartArctan.resize(); });
})();
