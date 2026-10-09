#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一场论交互式可视化工具

该脚本用于生成统一场论公式和模块的交互式可视化图表，
包括力导向图、热力图、散点图等多种可视化方式。
"""

import networkx as nx
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import datetime

class InteractiveVisualization:
    """统一场论交互式可视化类"""
    
    def __init__(self, formula_analyzer):
        """初始化可视化工具"""
        self.analyzer = formula_analyzer
        self.current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    def generate_force_directed_graph(self, output_file='interactive_force_graph.html'):
        """生成力导向交互式网络图"""
        G = self.analyzer.create_formula_module_graph()
        
        # 准备节点数据
        nodes = []
        for node in G.nodes():
            node_data = G.nodes[node]
            node_type = node_data['type']
            color = '#FF9999' if node_type == 'module' else '#99CCFF'
            size = 30 if node_type == 'module' else 20
            
            # 添加更多节点属性
            node_info = {
                'id': node,
                'label': node,
                'title': f"{node}\\n{node_data['name']}",
                'type': node_type,
                'size': size,
                'color': color,
                'name': node_data['name']
            }
            
            # 添加模块特有属性
            if node_type == 'module':
                node_info['formula'] = node_data.get('formula', '')
                node_info['meaning'] = node_data.get('meaning', '')
                node_info['dimension'] = node_data.get('dimension', '')
            
            # 添加公式特有属性
            if node_type == 'formula':
                node_info['formula'] = node_data.get('formula', '')
            
            nodes.append(node_info)
        
        # 准备边数据
        edges = []
        for u, v, data in G.edges(data=True):
            edges.append({
                'source': u,
                'target': v,
                'label': data.get('relation', '关联'),
                'width': 1.5,
                'color': '#666666'
            })
        
        # 创建HTML内容
        html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>统一场论公式-模块关系力导向图</title>
    <script src="https://cdn.jsdelivr.net/npm/vis-network@9.1.9/dist/vis-network.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/vis-network@9.1.9/dist/vis-network.min.css" rel="stylesheet" type="text/css" />
    <style>
        body {{
            font-family: 'SimHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        #network {{
            width: 100%;
            height: 800px;
            border: 1px solid #ddd;
            background-color: white;
            border-radius: 8px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .title {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .description {{
            font-size: 16px;
            color: #666;
        }}
        .controls {{
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .control-button {{
            padding: 8px 16px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: white;
            cursor: pointer;
            font-family: 'SimHei';
            font-size: 14px;
        }}
        .control-button:hover {{
            background-color: #f0f0f0;
        }}
        .control-button.active {{
            background-color: #4CAF50;
            color: white;
            border-color: #4CAF50;
        }}
        .legend {{
            display: flex;
            justify-content: center;
            margin-top: 20px;
            gap: 20px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
        }}
        .module-color {{
            background-color: #FF9999;
        }}
        .formula-color {{
            background-color: #99CCFF;
        }}
        .info-panel {{
            position: fixed;
            top: 20px;
            right: 20px;
            width: 300px;
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: none;
        }}
        .info-panel.active {{
            display: block;
        }}
        .info-title {{
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }}
        .info-item {{
            margin-bottom: 5px;
            font-size: 14px;
        }}
        .info-label {{
            font-weight: bold;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">统一场论公式-模块关系力导向图</div>
        <div class="description">交互式可视化公式与模块之间的关系网络</div>
    </div>
    
    <div class="controls">
        <button class="control-button" onclick="togglePhysics()">物理引擎: 开启</button>
        <button class="control-button" onclick="toggleLabels()">显示标签: 关闭</button>
        <button class="control-button" onclick="showModules()">只显示模块</button>
        <button class="control-button" onclick="showFormulas()">只显示公式</button>
        <button class="control-button" onclick="showAll()">显示全部</button>
        <button class="control-button" onclick="resetView()">重置视图</button>
    </div>
    
    <div id="network"></div>
    
    <div class="info-panel" id="infoPanel">
        <div class="info-title">节点信息</div>
        <div id="nodeInfo"></div>
    </div>
    
    <div class="legend">
        <div class="legend-item">
            <div class="legend-color module-color"></div>
            <span>模块节点</span>
        </div>
        <div class="legend-item">
            <div class="legend-color formula-color"></div>
            <span>公式节点</span>
        </div>
    </div>

    <script>
        // 节点数据
        var nodes = {json.dumps(nodes)};
        
        // 边数据
        var edges = {json.dumps(edges)};
        
        // 网络配置
        var container = document.getElementById('network');
        var data = {{
            nodes: nodes,
            edges: edges
        }};
        
        var options = {{
            nodes: {{
                font: {{
                    size: 12,
                    face: 'SimHei',
                    color: '#333'
                }},
                shape: 'circle',
                borderWidth: 2,
                shadow: {{
                    enabled: true,
                    size: 10,
                    x: 0,
                    y: 0,
                    color: 'rgba(0,0,0,0.2)'
                }}
            }},
            edges: {{
                font: {{
                    size: 10,
                    face: 'SimHei',
                    color: '#666'
                }},
                arrows: {{
                    to: {{
                        enabled: true,
                        scaleFactor: 0.5
                    }}
                }},
                smooth: {{
                    enabled: true,
                    type: 'dynamic',
                    forceDirection: 'none',
                    roundness: 0.5
                }},
                shadow: {{
                    enabled: false
                }}
            }},
            interaction: {{
                hover: true,
                zoomView: true,
                dragNodes: true,
                dragView: true,
                selectNodes: true,
                selectEdges: true,
                multiselect: true
            }},
            layout: {{
                hierarchical: {{
                    enabled: false,
                    direction: 'UD',
                    sortMethod: 'directed'
                }}
            }},
            physics: {{
                enabled: true,
                stabilization: {{
                    enabled: true,
                    iterations: 1000,
                    updateInterval: 100,
                    onlyDynamicEdges: false,
                    fit: true
                }},
                barnesHut: {{
                    gravitationalConstant: -2000,
                    centralGravity: 0.3,
                    springLength: 100,
                    springConstant: 0.04,
                    damping: 0.09,
                    avoidOverlap: 0.1
                }},
                maxVelocity: 50,
                minVelocity: 0.1,
                solver: 'barnesHut',
                timestep: 0.5,
                adaptiveTimestep: true
            }},
            groups: {{
                module: {{
                    color: '#FF9999',
                    shape: 'circle'
                }},
                formula: {{
                    color: '#99CCFF',
                    shape: 'circle'
                }}
            }}
        }};
        
        // 创建网络
        var network = new vis.Network(container, data, options);
        
        // 物理引擎状态
        var physicsEnabled = true;
        
        // 标签显示状态
        var labelsEnabled = false;
        
        // 点击事件
        network.on('click', function(params) {{
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                var node = nodes.find(n => n.id === nodeId);
                if (node) {{
                    showNodeInfo(node);
                }}
            }} else {{
                hideNodeInfo();
            }}
        }});
        
        // 显示节点信息
        function showNodeInfo(node) {{
            var infoPanel = document.getElementById('infoPanel');
            var nodeInfo = document.getElementById('nodeInfo');
            
            var infoHTML = '';
            infoHTML += '<div class="info-item"><span class="info-label">ID:</span> ' + node.id + '</div>';
            infoHTML += '<div class="info-item"><span class="info-label">名称:</span> ' + node.name + '</div>';
            infoHTML += '<div class="info-item"><span class="info-label">类型:</span> ' + (node.type === 'module' ? '模块' : '公式') + '</div>';
            
            if (node.formula) {{
                infoHTML += '<div class="info-item"><span class="info-label">公式:</span> ' + node.formula + '</div>';
            }}
            
            if (node.meaning) {{
                infoHTML += '<div class="info-item"><span class="info-label">意义:</span> ' + node.meaning + '</div>';
            }}
            
            if (node.dimension) {{
                infoHTML += '<div class="info-item"><span class="info-label">量纲:</span> ' + node.dimension + '</div>';
            }}
            
            nodeInfo.innerHTML = infoHTML;
            infoPanel.classList.add('active');
        }}
        
        // 隐藏节点信息
        function hideNodeInfo() {{
            var infoPanel = document.getElementById('infoPanel');
            infoPanel.classList.remove('active');
        }}
        
        // 切换物理引擎
        function togglePhysics() {{
            physicsEnabled = !physicsEnabled;
            network.setOptions({{
                physics: {{
                    enabled: physicsEnabled
                }}
            }});
            
            var button = document.querySelector('button[onclick="togglePhysics()"]');
            button.textContent = '物理引擎: ' + (physicsEnabled ? '开启' : '关闭');
            button.classList.toggle('active', physicsEnabled);
        }}
        
        // 切换标签显示
        function toggleLabels() {{
            labelsEnabled = !labelsEnabled;
            var labelType = labelsEnabled ? 'label' : 'id';
            
            network.setOptions({{
                nodes: {{
                    label: labelType
                }}
            }});
            
            var button = document.querySelector('button[onclick="toggleLabels()"]');
            button.textContent = '显示标签: ' + (labelsEnabled ? '开启' : '关闭');
            button.classList.toggle('active', labelsEnabled);
        }}
        
        // 只显示模块
        function showModules() {{
            var filteredNodes = nodes.filter(node => node.type === 'module');
            var filteredEdges = edges.filter(edge => {{
                var sourceNode = nodes.find(n => n.id === edge.source);
                var targetNode = nodes.find(n => n.id === edge.target);
                return sourceNode && targetNode && sourceNode.type === 'module' && targetNode.type === 'module';
            }});
            
            network.setData({{
                nodes: filteredNodes,
                edges: filteredEdges
            }});
        }}
        
        // 只显示公式
        function showFormulas() {{
            var filteredNodes = nodes.filter(node => node.type === 'formula');
            var filteredEdges = edges.filter(edge => {{
                var sourceNode = nodes.find(n => n.id === edge.source);
                var targetNode = nodes.find(n => n.id === edge.target);
                return sourceNode && targetNode && sourceNode.type === 'formula' && targetNode.type === 'formula';
            }});
            
            network.setData({{
                nodes: filteredNodes,
                edges: filteredEdges
            }});
        }}
        
        // 显示全部
        function showAll() {{
            network.setData({{
                nodes: nodes,
                edges: edges
            }});
        }}
        
        // 重置视图
        function resetView() {{
            network.fit();
        }}
        
        // 初始化
        network.once('stabilizationIterationsDone', function() {{
            network.setOptions({{
                physics: {{
                    enabled: true,
                    stabilization: {{
                        enabled: false
                    }}
                }}
            }});
        }});
    </script>
</body>
</html>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"力导向交互式网络图已保存到: {output_file}")
    
    def generate_heatmap(self, output_file='module_heatmap.html'):
        """生成模块使用热力图"""
        # 分析模块在公式中的使用情况
        usage_matrix = []
        module_ids = list(self.analyzer.modules.keys())
        formula_ids = list(self.analyzer.formulas.keys())
        
        for formula_id in formula_ids:
            formula_modules = self.analyzer.formulas[formula_id]['modules']
            row = []
            for module_id in module_ids:
                row.append(1 if module_id in formula_modules else 0)
            usage_matrix.append(row)
        
        # 创建热力图数据
        heatmap_data = []
        for i, formula_id in enumerate(formula_ids):
            for j, module_id in enumerate(module_ids):
                value = usage_matrix[i][j]
                if value > 0:
                    heatmap_data.append({
                        'formula': formula_id,
                        'module': module_id,
                        'value': value,
                        'formula_name': self.analyzer.formulas[formula_id]['name'],
                        'module_name': self.analyzer.modules[module_id]['name']
                    })
        
        # 创建HTML内容
        html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>统一场论模块使用热力图</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        body {{
            font-family: 'SimHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            width: 100%;
            height: 800px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .title {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .description {{
            font-size: 16px;
            color: #666;
        }}
        .chart-container {{
            width: 100%;
            height: 700px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">统一场论模块使用热力图</div>
        <div class="description">显示各公式对模块的使用情况</div>
    </div>
    
    <div class="container">
        <div id="heatmap" class="chart-container"></div>
    </div>

    <script>
        // 热力图数据
        var heatmapData = {json.dumps(heatmap_data)};
        
        // 模块和公式列表
        var modules = {json.dumps([self.analyzer.modules[mid]['name'] for mid in module_ids])};
        var formulas = {json.dumps([fid for fid in formula_ids])};
        var formulaNames = {json.dumps([self.analyzer.formulas[fid]['name'] for fid in formula_ids])};
        
        // 初始化图表
        var chart = echarts.init(document.getElementById('heatmap'));
        
        // 准备数据
        var data = [];
        for (var i = 0; i < heatmapData.length; i++) {{
            var item = heatmapData[i];
            var formulaIndex = formulas.indexOf(item.formula);
            var moduleIndex = modules.indexOf(item.module_name);
            data.push([moduleIndex, formulaIndex, item.value]);
        }}
        
        // 配置项
        var option = {{
            tooltip: {{
                position: 'top',
                formatter: function(params) {{
                    var data = params.data;
                    var moduleName = modules[data[0]];
                    var formulaName = formulaNames[data[1]];
                    var formulaId = formulas[data[1]];
                    return formulaId + ' (' + formulaName + ')<br/>' +
                           moduleName + '<br/>' +
                           '使用: ' + (data[2] ? '是' : '否');
                }}
            }},
            grid: {{
                height: '60%',
                top: '10%'
            }},
            xAxis: {{{{
                type: 'category',
                data: formulas,
                splitArea: {{{{
                    show: true
                }}}}
            }}},
            yAxis: {{{{
                type: 'category',
                data: modules,
                splitArea: {{{{
                    show: true
                }}}}
            }}},
            visualMap: {{{{
                min: 0,
                max: 1,
                calculable: true,
                orient: 'horizontal',
                left: 'center',
                bottom: '15%',
                inRange: {{{{
                    color: ['#e0f2ff', '#1890ff']
                }}}}
            }}},
            series: [{{
                name: '模块使用',
                type: 'heatmap',
                data: data,
                label: {{{{
                    show: true,
                    formatter: function(params) {{
                        return params.value[2];
                    }}
                }}},
                emphasis: {{{{
                    itemStyle: {{{{
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }}}}
                }}}
            }}]
        }};
        
        // 设置配置
        chart.setOption(option);
        
        // 响应式调整
        window.addEventListener('resize', function() {{
            chart.resize();
        }});
    </script>
</body>
</html>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"模块使用热力图已保存到: {output_file}")
    
    def generate_scatter_plot(self, output_file='module_scatter.html'):
        """生成模块相关性散点图"""
        # 计算模块相关性
        module_ids = list(self.analyzer.modules.keys())
        module_count = len(module_ids)
        
        # 计算模块共同出现次数
        cooccurrence = {}
        for formula_id, formula_info in self.analyzer.formulas.items():
            modules = formula_info['modules']
            if len(modules) >= 2:
                for i in range(len(modules)):
                    for j in range(i+1, len(modules)):
                        pair = tuple(sorted([modules[i], modules[j]]))
                        if pair not in cooccurrence:
                            cooccurrence[pair] = 0
                        cooccurrence[pair] += 1
        
        # 准备散点图数据
        scatter_data = []
        for pair, count in cooccurrence.items():
            module1, module2 = pair
            scatter_data.append({
                'module1': module1,
                'module2': module2,
                'count': count,
                'module1_name': self.analyzer.modules[module1]['name'],
                'module2_name': self.analyzer.modules[module2]['name']
            })
        
        # 创建HTML内容
        html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>统一场论模块相关性散点图</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        body {{
            font-family: 'SimHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            width: 100%;
            height: 800px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .title {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .description {{
            font-size: 16px;
            color: #666;
        }}
        .chart-container {{
            width: 100%;
            height: 700px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">统一场论模块相关性散点图</div>
        <div class="description">模块共同出现频率分析</div>
    </div>
    
    <div class="container">
        <div id="scatter" class="chart-container"></div>
    </div>

    <script>
        // 散点图数据
        var scatterData = {json.dumps(scatter_data)};
        
        // 初始化图表
        var chart = echarts.init(document.getElementById('scatter'));
        
        // 准备数据
        var data = scatterData.map(function(item) {{
            return [
                item.module1_name,
                item.module2_name,
                item.count,
                item.module1,
                item.module2
            ];
        }});
        
        // 配置项
        var option = {{
            tooltip: {{
                trigger: 'item',
                formatter: function(params) {{
                    var data = params.value;
                    return data[3] + ' (' + data[0] + ')<br/>' +
                           data[4] + ' (' + data[1] + ')<br/>' +
                           '共同出现次数: ' + data[2];
                }}
            }},
            xAxis: {{{{
                type: 'category',
                data: [...new Set(scatterData.map(item => item.module1_name))],
                axisLabel: {{{{
                    rotate: 45,
                    interval: 0
                }}}}
            }}},
            yAxis: {{{{
                type: 'category',
                data: [...new Set(scatterData.map(item => item.module2_name))]
            }}},
            series: [{{
                name: '模块相关性',
                type: 'scatter',
                symbolSize: function(data) {{
                    return data[2] * 10 + 10;
                }},
                data: data,
                itemStyle: {{{{
                    color: function(params) {{
                        var count = params.value[2];
                        if (count >= 5) return '#ff4d4f';
                        if (count >= 3) return '#faad14';
                        return '#52c41a';
                    }}
                }}}
            }}]
        }};
        
        // 设置配置
        chart.setOption(option);
        
        // 响应式调整
        window.addEventListener('resize', function() {{
            chart.resize();
        }});
    </script>
</body>
</html>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"模块相关性散点图已保存到: {output_file}")
    
    def generate_radar_chart(self, output_file='module_radar.html'):
        """生成模块中心性雷达图"""
        # 获取中心性数据
        centrality_df = self.analyzer.analyze_module_centrality()
        top_modules = centrality_df.head(8)
        
        # 准备雷达图数据
        indicators = [
            {{{{ name: '度中心性', max: 1 }}}},
            {{{{ name: '中介中心性', max: 1 }}}},
            {{{{ name: '接近中心性', max: 1 }}}},
            {{{{ name: '特征向量中心性', max: 1 }}}},
            {{{{ name: '使用次数', max: 15 }}}}
        ]
        
        series_data = []
        for idx, row in top_modules.iterrows():
            series_data.append({{{{
                value: [
                    row['degree'],
                    row['betweenness'],
                    row['closeness'],
                    row['eigenvector'],
                    row['使用次数']
                ],
                name: row['模块名称']
            }}}})
        
        # 创建HTML内容
        html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>统一场论模块中心性雷达图</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        body {{
            font-family: 'SimHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            width: 100%;
            height: 800px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .title {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .description {{
            font-size: 16px;
            color: #666;
        }}
        .chart-container {{
            width: 100%;
            height: 700px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">统一场论模块中心性雷达图</div>
        <div class="description">核心模块多维度中心性分析</div>
    </div>
    
    <div class="container">
        <div id="radar" class="chart-container"></div>
    </div>

    <script>
        // 初始化图表
        var chart = echarts.init(document.getElementById('radar'));
        
        // 配置项
        var option = {{{{
            tooltip: {{}},
            legend: {{{{
                data: {json.dumps([row['模块名称'] for idx, row in top_modules.iterrows()])},
                bottom: 0
            }}}},
            radar: {{{{
                indicator: {json.dumps(indicators)}
            }}}},
            series: [{{{{
                name: '模块中心性',
                type: 'radar',
                data: {json.dumps(series_data)}
            }}}}]
        }};
        
        // 设置配置
        chart.setOption(option);
        
        // 响应式调整
        window.addEventListener('resize', function() {{
            chart.resize();
        }});
    </script>
</body>
</html>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"模块中心性雷达图已保存到: {output_file}")
    
    def generate_dashboard(self, output_file='visualization_dashboard.html'):
        """生成综合可视化仪表盘"""
        # 创建仪表盘HTML
        html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>统一场论可视化仪表盘</title>
    <link href="https://cdn.jsdelivr.net/npm/antd@5.12.8/dist/reset.css" rel="stylesheet">
    <style>
        body {{
            font-family: 'SimHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f2f5;
        }}
        .dashboard {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .title {{
            font-size: 28px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .subtitle {{
            font-size: 16px;
            color: #666;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            grid-gap: 20px;
            margin-bottom: 20px;
        }}
        .full-width {{
            grid-column: 1 / -1;
        }}
        .card {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 20px;
        }}
        .card-title {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            border-bottom: 1px solid #f0f0f0;
            padding-bottom: 10px;
        }}
        .chart-container {{
            width: 100%;
            height: 400px;
        }}
        .large-chart {{
            height: 600px;
        }}
        .nav-menu {{
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
            background-color: white;
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .nav-item {{
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .nav-item:hover {{
            background-color: #f0f0f0;
        }}
        .nav-item.active {{
            background-color: #1890ff;
            color: white;
        }}
        .iframe-container {{
            width: 100%;
            height: 100%;
            border: none;
        }}
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <div class="title">统一场论可视化仪表盘</div>
            <div class="subtitle">综合分析与交互式可视化</div>
        </div>
        
        <div class="nav-menu">
            <div class="nav-item active" onclick="showTab('overview')">概览</div>
            <div class="nav-item" onclick="showTab('force-graph')">力导向图</div>
            <div class="nav-item" onclick="showTab('heatmap')">热力图</div>
            <div class="nav-item" onclick="showTab('scatter')">散点图</div>
            <div class="nav-item" onclick="showTab('radar')">雷达图</div>
        </div>
        
        <!-- 概览标签 -->
        <div class="tab-content active" id="overview">
            <div class="grid">
                <div class="card">
                    <div class="card-title">项目统计</div>
                    <div style="padding: 20px;">
                        <h3>基本信息</h3>
                        <ul>
                            <li>核心模块数量: {len(self.analyzer.modules)}</li>
                            <li>公式数量: {len(self.analyzer.formulas)}</li>
                            <li>分析日期: {self.current_date}</li>
                        </ul>
                        
                        <h3>核心模块</h3>
                        <ul>
                            {''.join([f'<li>{mid} {self.analyzer.modules[mid]["name"]} (使用次数: {self.analyzer.analyze_module_usage().loc[mid]["使用次数"]})</li>' for mid in self.analyzer.modules if self.analyzer.analyze_module_usage().loc[mid]["使用次数"] >= 3])}
                        </ul>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-title">快速导航</div>
                    <div style="padding: 20px;">
                        <h3>可视化资源</h3>
                        <ul>
                            <li><a href="interactive_force_graph.html" target="_blank">力导向交互式网络图</a></li>
                            <li><a href="module_heatmap.html" target="_blank">模块使用热力图</a></li>
                            <li><a href="module_scatter.html" target="_blank">模块相关性散点图</a></li>
                            <li><a href="module_radar.html" target="_blank">模块中心性雷达图</a></li>
                        </ul>
                        
                        <h3>分析报告</h3>
                        <ul>
                            <li><a href="formula_analysis_report.md" target="_blank">公式分析报告</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="card full-width">
                <div class="card-title">模块使用频率分布</div>
                <div class="chart-container" id="usageChart"></div>
            </div>
        </div>
        
        <!-- 力导向图标签 -->
        <div class="tab-content" id="force-graph">
            <div class="card full-width">
                <div class="card-title">力导向交互式网络图</div>
                <iframe class="iframe-container" src="interactive_force_graph.html"></iframe>
            </div>
        </div>
        
        <!-- 热力图标签 -->
        <div class="tab-content" id="heatmap">
            <div class="card full-width">
                <div class="card-title">模块使用热力图</div>
                <iframe class="iframe-container" src="module_heatmap.html"></iframe>
            </div>
        </div>
        
        <!-- 散点图标签 -->
        <div class="tab-content" id="scatter">
            <div class="card full-width">
                <div class="card-title">模块相关性散点图</div>
                <iframe class="iframe-container" src="module_scatter.html"></iframe>
            </div>
        </div>
        
        <!-- 雷达图标签 -->
        <div class="tab-content" id="radar">
            <div class="card full-width">
                <div class="card-title">模块中心性雷达图</div>
                <iframe class="iframe-container" src="module_radar.html"></iframe>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <script>
        // 显示标签
        function showTab(tabId) {
            // 隐藏所有标签
            var tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // 显示选中标签
            document.getElementById(tabId).classList.add('active');
            
            // 更新导航状态
            var navItems = document.querySelectorAll('.nav-item');
            navItems.forEach(item => {{
                item.classList.remove('active');
            }});
            event.target.classList.add('active');
        }
        
        // 初始化使用频率图表
        window.onload = function() {{
            var chart = echarts.init(document.getElementById('usageChart'));
            
            var moduleNames = {json.dumps([self.analyzer.modules[mid]['name'] for mid in self.analyzer.modules])};
            var usageCounts = {json.dumps([self.analyzer.analyze_module_usage().loc[mid]['使用次数'] for mid in self.analyzer.modules])};
            var moduleIds = {json.dumps([mid for mid in self.analyzer.modules])};
            
            var option = {{
                tooltip: {{
                    trigger: 'axis',
                    axisPointer: {{
                        type: 'shadow'
                    }},
                    formatter: function(params) {{
                        var data = params[0];
                        var index = data.dataIndex;
                        return moduleIds[index] + ' (' + moduleNames[index] + ')<br/>' +
                               '使用次数: ' + data.value;
                    }}
                }},
                grid: {{
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                }},
                xAxis: {{
                    type: 'value',
                    boundaryGap: [0, 0.01]
                }},
                yAxis: {{
                    type: 'category',
                    data: moduleNames,
                    axisLabel: {{
                        interval: 0,
                        rotate: 30
                    }}
                }},
                series: [{{
                    name: '使用次数',
                    type: 'bar',
                    data: usageCounts,
                    itemStyle: {{
                        color: function(params) {{
                            var count = params.value;
                            if (count >= 10) return '#ff4d4f';
                            if (count >= 5) return '#faad14';
                            return '#52c41a';
                        }}
                    }}
                }}]
            }};
            
            chart.setOption(option);
            
            window.addEventListener('resize', function() {{
                chart.resize();
            }});
        }};
    </script>
</body>
</html>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"综合可视化仪表盘已保存到: {output_file}")

if __name__ == "__main__":
    # 导入FormulaAnalysis类
    from formula_analysis_optimized import FormulaAnalysis
    
    # 创建分析实例
    analyzer = FormulaAnalysis()
    
    # 创建可视化实例
    visualizer = InteractiveVisualization(analyzer)
    
    # 生成各种可视化
    visualizer.generate_force_directed_graph()
    visualizer.generate_heatmap()
    visualizer.generate_scatter_plot()
    visualizer.generate_radar_chart()
    visualizer.generate_dashboard()
    
    print("\n可视化生成完成！")
    print("生成的文件：")
    print("1. interactive_force_graph.html - 力导向交互式网络图")
    print("2. module_heatmap.html - 模块使用热力图")
    print("3. module_scatter.html - 模块相关性散点图")
    print("4. module_radar.html - 模块中心性雷达图")
    print("5. visualization_dashboard.html - 综合可视化仪表盘")