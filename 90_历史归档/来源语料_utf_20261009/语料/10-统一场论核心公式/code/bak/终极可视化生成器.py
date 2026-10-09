#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
张祥前统一场论核心公式 - 终极可视化生成器
创建最高质量的HTML5 + WebGL + MathJax可视化系统
达到国际顶级论文标准
"""

import json
import os
import math
from pathlib import Path

class UnifiedFieldVisualizationGenerator:
    def __init__(self):
        self.base_path = Path("utf/统一场论核心公式")
        self.load_formula_database()
        
    def load_formula_database(self):
        """加载公式数据库"""
        with open(self.base_path / "公式规格数据库.json", 'r', encoding='utf-8') as f:
            self.database = json.load(f)
    
    def generate_all_visualizations(self):
        """生成所有19个公式的高质量可视化"""
        print("🚀 开始生成张祥前统一场论核心公式可视化系统...")
        
        for formula in self.database['formulas']:
            print(f"📐 正在生成: {formula['id']}-{formula['name']}")
            self.generate_formula_visualization(formula)
            
        self.generate_master_index()
        print("✅ 所有可视化生成完成！")
    
    def generate_formula_visualization(self, formula):
        """为单个公式生成完整的可视化"""
        folder_name = f"{formula['id']}-{formula['name']}"
        folder_path = self.base_path / folder_name
        
        # 确保文件夹存在
        folder_path.mkdir(exist_ok=True)
        
        # 生成高质量HTML可视化
        html_content = self.create_advanced_html(formula)
        with open(folder_path / "visualization.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        # 生成理论文档
        theory_content = self.create_theory_document(formula)
        with open(folder_path / "theory.md", 'w', encoding='utf-8') as f:
            f.write(theory_content)
            
        # 生成README
        readme_content = self.create_readme(formula)
        with open(folder_path / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def create_advanced_html(self, formula):
        """创建高级HTML5可视化"""
        
        # 根据公式类型选择可视化模板
        visualization_code = self.get_visualization_code(formula)
        
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{formula['name']} - 张祥前统一场论可视化</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            overflow: hidden; color: white; height: 100vh;
        }}
        
        #canvas {{ 
            display: block; cursor: grab; width: 100%; height: 100%;
            background: radial-gradient(circle at center, #1a1a2e 0%, #0c0c0c 100%);
        }}
        
        .ui-panel {{
            position: absolute; background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px; padding: 20px; 
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
            transition: all 0.3s ease;
        }}
        
        .ui-panel:hover {{ transform: translateY(-2px); }}
        
        #info-panel {{ 
            top: 20px; left: 20px; width: 420px; max-height: 80vh; overflow-y: auto;
        }}
        
        #controls-panel {{ 
            top: 20px; right: 20px; width: 320px;
        }}
        
        #math-panel {{
            bottom: 20px; left: 20px; width: 500px;
        }}
        
        .panel-title {{
            font-size: 1.4em; font-weight: bold; margin-bottom: 15px;
            background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
            background-clip: text; -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
            text-shadow: none;
        }}
        
        .formula-display {{
            background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px;
            margin: 10px 0; border-left: 4px solid #667eea;
        }}
        
        .parameter-control {{
            margin: 10px 0; display: flex; align-items: center; gap: 10px;
        }}
        
        .parameter-control label {{
            min-width: 80px; font-size: 0.9em; color: #ccc;
        }}
        
        .parameter-control input[type="range"] {{
            flex: 1; height: 6px; border-radius: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            outline: none; -webkit-appearance: none;
        }}
        
        .parameter-control input[type="range"]::-webkit-slider-thumb {{
            -webkit-appearance: none; width: 18px; height: 18px;
            border-radius: 50%; background: #fff; cursor: pointer;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        }}
        
        .parameter-value {{
            min-width: 60px; text-align: right; font-family: monospace;
            background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 4px;
        }}
        
        .control-button {{
            background: linear-gradient(45deg, #667eea, #764ba2); color: white; 
            border: none; padding: 12px 24px; border-radius: 25px; 
            cursor: pointer; margin: 5px; font-size: 0.9em;
            transition: all 0.3s ease; font-weight: 500;
        }}
        
        .control-button:hover {{ 
            transform: translateY(-2px); 
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }}
        
        .control-button:active {{ transform: translateY(0); }}
        
        .stats-display {{
            background: rgba(255, 255, 255, 0.05); padding: 10px; 
            border-radius: 8px; margin: 10px 0; font-family: monospace;
            font-size: 0.85em; line-height: 1.4;
        }}
        
        .physics-insight {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 1px solid rgba(102, 126, 234, 0.3); padding: 15px; 
            border-radius: 10px; margin: 15px 0;
        }}
        
        .physics-insight h4 {{
            color: #667eea; margin-bottom: 8px; font-size: 1.1em;
        }}
        
        .loading-screen {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(135deg, #0c0c0c, #1a1a2e);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            z-index: 1000; transition: opacity 0.5s ease;
        }}
        
        .loading-spinner {{
            width: 60px; height: 60px; border: 4px solid rgba(255,255,255,0.1);
            border-top: 4px solid #667eea; border-radius: 50%;
            animation: spin 1s linear infinite; margin-bottom: 20px;
        }}
        
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        
        .fade-out {{ opacity: 0; pointer-events: none; }}
        
        /* 响应式设计 */
        @media (max-width: 768px) {{
            .ui-panel {{ width: calc(100% - 40px) !important; }}
            #controls-panel {{ top: auto; bottom: 20px; right: 20px; }}
            #math-panel {{ display: none; }}
        }}
    </style>
    
    <!-- 外部库 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        window.MathJax = {{
            tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] }},
            svg: {{ fontCache: 'global' }}
        }};
    </script>
</head>
<body>
    <!-- 加载屏幕 -->
    <div id="loadingScreen" class="loading-screen">
        <div class="loading-spinner"></div>
        <h2>正在加载 {formula['name']} 可视化...</h2>
        <p>张祥前统一场论 - 高级3D可视化系统</p>
    </div>
    
    <!-- 主画布 -->
    <canvas id="canvas"></canvas>
    
    <!-- 信息面板 -->
    <div id="info-panel" class="ui-panel">
        <div class="panel-title">{formula['icon']} {formula['name']}</div>
        
        <div class="formula-display">
            <strong>LaTeX公式：</strong><br>
            $${formula['formula_latex']}$$
        </div>
        
        <div class="formula-display">
            <strong>Unicode表示：</strong><br>
            <code>{formula['formula_unicode']}</code>
        </div>
        
        <p><strong>物理描述：</strong><br>{formula['description']}</p>
        
        <div class="physics-insight">
            <h4>🔬 物理洞察</h4>
            <p>该公式揭示了{', '.join(formula['physics_concepts'])}的深层关系。</p>
        </div>
        
        <div class="physics-insight">
            <h4>📊 数学工具</h4>
            <p>涉及{', '.join(formula['math_concepts'])}等数学概念。</p>
        </div>
        
        <div class="stats-display" id="statsDisplay">
            <strong>实时统计：</strong><br>
            帧率: <span id="fps">60</span> FPS<br>
            渲染对象: <span id="objectCount">0</span><br>
            计算精度: <span id="precision">高精度</span>
        </div>
    </div>
    
    <!-- 控制面板 -->
    <div id="controls-panel" class="ui-panel">
        <div class="panel-title">🎮 交互控制</div>
        
        <div style="text-align: center; margin-bottom: 15px;">
            <button class="control-button" onclick="toggleAnimation()">
                <span id="playPauseIcon">▶️</span> <span id="playPauseText">开始</span>
            </button>
            <button class="control-button" onclick="resetVisualization()">🔄 重置</button>
            <button class="control-button" onclick="toggleFullscreen()">🔍 全屏</button>
        </div>
        
        <!-- 动态参数控制 -->
        <div id="parameterControls">
            {self.generate_parameter_controls(formula)}
        </div>
        
        <div class="physics-insight">
            <h4>💡 操作提示</h4>
            <p>• 鼠标拖拽旋转视角<br>
            • 滚轮缩放场景<br>
            • 调节参数观察变化<br>
            • 点击重置恢复初始状态</p>
        </div>
    </div>
    
    <!-- 数学面板 -->
    <div id="math-panel" class="ui-panel">
        <div class="panel-title">📐 数学分析</div>
        <div id="mathAnalysis">
            <div class="formula-display">
                <strong>实时计算结果：</strong><br>
                <span id="calculationResult">计算中...</span>
            </div>
        </div>
    </div>

    <script>
        {visualization_code}
    </script>
</body>
</html>"""
        
        return html_template
    
    def generate_parameter_controls(self, formula):
        """生成参数控制HTML"""
        controls_html = ""
        
        for param in formula.get('parameters', []):
            param_name = param['name']
            param_type = param['type']
            default_val = param['default']
            param_range = param.get('range', [0, 1])
            
            if param_type == 'float':
                controls_html += f"""
                <div class="parameter-control">
                    <label>{param_name}:</label>
                    <input type="range" id="{param_name}" 
                           min="{param_range[0]}" max="{param_range[1]}" 
                           step="0.01" value="{default_val}"
                           oninput="updateParameter('{param_name}', this.value)">
                    <span class="parameter-value" id="{param_name}Value">{default_val}</span>
                </div>"""
            elif param_type == 'vector3':
                for i, axis in enumerate(['x', 'y', 'z']):
                    controls_html += f"""
                    <div class="parameter-control">
                        <label>{param_name}.{axis}:</label>
                        <input type="range" id="{param_name}_{axis}" 
                               min="{param_range[0]}" max="{param_range[1]}" 
                               step="0.01" value="{default_val[i]}"
                               oninput="updateVectorParameter('{param_name}', '{axis}', this.value)">
                        <span class="parameter-value" id="{param_name}_{axis}Value">{default_val[i]}</span>
                    </div>"""
        
        return controls_html
    
    def get_visualization_code(self, formula):
        """根据公式类型生成对应的可视化代码"""
        
        # 基础JavaScript框架
        base_code = f"""
        // 全局变量
        let scene, camera, renderer, controls;
        let animationId, isAnimating = false;
        let visualizationObjects = {{}};
        let parameters = {{}};
        let startTime = Date.now();
        
        // 初始化参数
        function initializeParameters() {{
            {self.generate_parameter_initialization(formula)}
        }}
        
        // 场景初始化
        function initScene() {{
            // 创建场景
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0a0a0a);
            scene.fog = new THREE.Fog(0x0a0a0a, 50, 200);
            
            // 创建相机
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(15, 15, 15);
            
            // 创建渲染器
            renderer = new THREE.WebGLRenderer({{ 
                canvas: document.getElementById('canvas'), 
                antialias: true,
                alpha: true
            }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            renderer.outputEncoding = THREE.sRGBEncoding;
            renderer.toneMapping = THREE.ACESFilmicToneMapping;
            renderer.toneMappingExposure = 1.2;
            
            // 创建控制器
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.maxDistance = 100;
            controls.minDistance = 5;
            
            // 添加光照系统
            setupLighting();
            
            // 创建坐标系
            createCoordinateSystem();
            
            // 创建特定可视化内容
            {self.get_specific_visualization(formula)}
            
            // 初始化参数
            initializeParameters();
            
            // 开始动画循环
            animate();
            
            // 隐藏加载屏幕
            setTimeout(() => {{
                document.getElementById('loadingScreen').classList.add('fade-out');
            }}, 1000);
        }}
        
        // 光照设置
        function setupLighting() {{
            // 环境光
            const ambientLight = new THREE.AmbientLight(0x404080, 0.3);
            scene.add(ambientLight);
            
            // 主光源
            const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
            directionalLight.position.set(20, 20, 10);
            directionalLight.castShadow = true;
            directionalLight.shadow.mapSize.width = 2048;
            directionalLight.shadow.mapSize.height = 2048;
            directionalLight.shadow.camera.near = 0.5;
            directionalLight.shadow.camera.far = 100;
            directionalLight.shadow.camera.left = -50;
            directionalLight.shadow.camera.right = 50;
            directionalLight.shadow.camera.top = 50;
            directionalLight.shadow.camera.bottom = -50;
            scene.add(directionalLight);
            
            // 补充光源
            const pointLight = new THREE.PointLight(0x667eea, 0.5, 100);
            pointLight.position.set(-10, 10, -10);
            scene.add(pointLight);
            
            const pointLight2 = new THREE.PointLight(0x764ba2, 0.5, 100);
            pointLight2.position.set(10, -10, 10);
            scene.add(pointLight2);
        }}
        
        // 创建坐标系
        function createCoordinateSystem() {{
            // 坐标轴
            const axesHelper = new THREE.AxesHelper(10);
            scene.add(axesHelper);
            
            // 网格
            const gridHelper = new THREE.GridHelper(20, 20, 0x444444, 0x222222);
            scene.add(gridHelper);
            
            // 坐标标签
            createAxisLabels();
        }}
        
        // 创建坐标轴标签
        function createAxisLabels() {{
            const loader = new THREE.FontLoader();
            // 这里可以添加文字标签，但为了简化，我们使用基础几何体标记
            
            // X轴标记
            const xGeometry = new THREE.SphereGeometry(0.2);
            const xMaterial = new THREE.MeshBasicMaterial({{ color: 0xff0000 }});
            const xMarker = new THREE.Mesh(xGeometry, xMaterial);
            xMarker.position.set(10, 0, 0);
            scene.add(xMarker);
            
            // Y轴标记
            const yGeometry = new THREE.SphereGeometry(0.2);
            const yMaterial = new THREE.MeshBasicMaterial({{ color: 0x00ff00 }});
            const yMarker = new THREE.Mesh(yGeometry, yMaterial);
            yMarker.position.set(0, 10, 0);
            scene.add(yMarker);
            
            // Z轴标记
            const zGeometry = new THREE.SphereGeometry(0.2);
            const zMaterial = new THREE.MeshBasicMaterial({{ color: 0x0000ff }});
            const zMarker = new THREE.Mesh(zGeometry, zMaterial);
            zMarker.position.set(0, 0, 10);
            scene.add(zMarker);
        }}
        
        // 主动画循环
        function animate() {{
            animationId = requestAnimationFrame(animate);
            
            const currentTime = (Date.now() - startTime) / 1000;
            
            if (isAnimating) {{
                updateVisualization(currentTime);
            }}
            
            // 更新控制器
            controls.update();
            
            // 更新统计信息
            updateStats();
            
            // 渲染场景
            renderer.render(scene, camera);
        }}
        
        // 更新可视化
        function updateVisualization(time) {{
            {self.get_animation_code(formula)}
        }}
        
        // 更新统计信息
        function updateStats() {{
            const fps = Math.round(1000 / (performance.now() - (window.lastFrameTime || performance.now())));
            window.lastFrameTime = performance.now();
            
            document.getElementById('fps').textContent = fps;
            document.getElementById('objectCount').textContent = scene.children.length;
        }}
        
        // 参数更新函数
        function updateParameter(name, value) {{
            parameters[name] = parseFloat(value);
            document.getElementById(name + 'Value').textContent = parseFloat(value).toFixed(2);
            updateVisualizationParameters();
        }}
        
        function updateVectorParameter(name, axis, value) {{
            if (!parameters[name]) parameters[name] = {{x: 0, y: 0, z: 0}};
            parameters[name][axis] = parseFloat(value);
            document.getElementById(name + '_' + axis + 'Value').textContent = parseFloat(value).toFixed(2);
            updateVisualizationParameters();
        }}
        
        // 更新可视化参数
        function updateVisualizationParameters() {{
            {self.get_parameter_update_code(formula)}
        }}
        
        // 控制函数
        function toggleAnimation() {{
            isAnimating = !isAnimating;
            const icon = document.getElementById('playPauseIcon');
            const text = document.getElementById('playPauseText');
            
            if (isAnimating) {{
                icon.textContent = '⏸️';
                text.textContent = '暂停';
            }} else {{
                icon.textContent = '▶️';
                text.textContent = '开始';
            }}
        }}
        
        function resetVisualization() {{
            startTime = Date.now();
            initializeParameters();
            // 重置所有参数控制器
            {self.get_reset_code(formula)}
        }}
        
        function toggleFullscreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen();
            }} else {{
                document.exitFullscreen();
            }}
        }}
        
        // 窗口大小调整
        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
        
        // 页面加载完成后初始化
        window.addEventListener('load', () => {{
            initScene();
        }});
        """
        
        return base_code
    
    def generate_parameter_initialization(self, formula):
        """生成参数初始化代码"""
        init_code = ""
        for param in formula.get('parameters', []):
            if param['type'] == 'float':
                init_code += f"parameters['{param['name']}'] = {param['default']};\n            "
            elif param['type'] == 'vector3':
                init_code += f"parameters['{param['name']}'] = {{x: {param['default'][0]}, y: {param['default'][1]}, z: {param['default'][2]}}};\n            "
        return init_code
    
    def get_specific_visualization(self, formula):
        """根据公式类型生成特定的可视化代码"""
        
        visualization_map = {
            "01": self.get_spacetime_unification_viz(),
            "02": self.get_helix_spacetime_viz(),
            "03": self.get_mass_definition_viz(),
            "04": self.get_gravity_field_viz(),
            "05": self.get_rest_momentum_viz(),
            "06": self.get_motion_momentum_viz(),
            "07": self.get_unified_force_viz(),
            "08": self.get_space_wave_viz(),
            "09": self.get_charge_definition_viz(),
            "10": self.get_electric_field_viz(),
            "11": self.get_magnetic_field_viz(),
            "12": self.get_gravity_em_coupling_viz(),
            "13": self.get_vector_potential_viz(),
            "14": self.get_gravity_to_electric_viz(),
            "15": self.get_magnetic_to_gravity_viz(),
            "16": self.get_energy_mass_viz(),
            "17": self.get_lightspeed_propulsion_viz(),
            "18": self.get_wave_solution_viz(),
            "19": self.get_constant_unification_viz()
        }
        
        return visualization_map.get(formula['id'], self.get_default_viz())
    
    def get_spacetime_unification_viz(self):
        """时空同一化方程可视化"""
        return """
            // 创建时空网格
            const spaceTimeGrid = new THREE.Group();
            
            // 创建空间网格线
            for (let i = -10; i <= 10; i++) {
                for (let j = -10; j <= 10; j++) {
                    const geometry = new THREE.BufferGeometry();
                    const positions = new Float32Array([
                        i, -10, j,
                        i, 10, j
                    ]);
                    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
                    
                    const material = new THREE.LineBasicMaterial({ 
                        color: 0x667eea, 
                        opacity: 0.3, 
                        transparent: true 
                    });
                    const line = new THREE.Line(geometry, material);
                    spaceTimeGrid.add(line);
                }
            }
            
            scene.add(spaceTimeGrid);
            visualizationObjects.spaceTimeGrid = spaceTimeGrid;
            
            // 创建光速矢量
            const arrowGeometry = new THREE.ConeGeometry(0.5, 2, 8);
            const arrowMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff, emissive: 0x333333 });
            const lightSpeedArrow = new THREE.Mesh(arrowGeometry, arrowMaterial);
            lightSpeedArrow.position.set(0, 0, 0);
            scene.add(lightSpeedArrow);
            visualizationObjects.lightSpeedArrow = lightSpeedArrow;
            
            // 创建轨迹线
            const trajectoryGeometry = new THREE.BufferGeometry();
            const trajectoryMaterial = new THREE.LineBasicMaterial({ 
                color: 0xff6b6b, 
                linewidth: 3 
            });
            const trajectoryLine = new THREE.Line(trajectoryGeometry, trajectoryMaterial);
            scene.add(trajectoryLine);
            visualizationObjects.trajectoryLine = trajectoryLine;
            
            // 轨迹点数组
            visualizationObjects.trajectoryPoints = [];
        """
    
    def get_helix_spacetime_viz(self):
        """三维螺旋时空方程可视化"""
        return """
            // 创建螺旋轨迹
            const helixPoints = [];
            for (let t = 0; t <= 20; t += 0.1) {
                const r = 5;
                const omega = 1;
                const h = 2;
                const x = r * Math.cos(omega * t);
                const y = r * Math.sin(omega * t);
                const z = h * t;
                helixPoints.push(new THREE.Vector3(x, y, z));
            }
            
            const helixGeometry = new THREE.BufferGeometry().setFromPoints(helixPoints);
            const helixMaterial = new THREE.LineBasicMaterial({ 
                color: 0x667eea, 
                linewidth: 3 
            });
            const helixCurve = new THREE.Line(helixGeometry, helixMaterial);
            scene.add(helixCurve);
            visualizationObjects.helixCurve = helixCurve;
            
            // 创建运动粒子
            const particleGeometry = new THREE.SphereGeometry(0.3);
            const particleMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xff6b6b, 
                emissive: 0x330000 
            });
            const particle = new THREE.Mesh(particleGeometry, particleMaterial);
            scene.add(particle);
            visualizationObjects.particle = particle;
            
            // 创建投影
            const projectionXY = new THREE.Group();
            const projectionXZ = new THREE.Group();
            const projectionYZ = new THREE.Group();
            
            scene.add(projectionXY);
            scene.add(projectionXZ);
            scene.add(projectionYZ);
            
            visualizationObjects.projectionXY = projectionXY;
            visualizationObjects.projectionXZ = projectionXZ;
            visualizationObjects.projectionYZ = projectionYZ;
        """
    
    def get_mass_definition_viz(self):
        """质量定义方程可视化"""
        return """
            // 创建立体角可视化
            const sphereGeometry = new THREE.SphereGeometry(8, 32, 16);
            const sphereMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x667eea, 
                transparent: true, 
                opacity: 0.3,
                wireframe: true
            });
            const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
            scene.add(sphere);
            visualizationObjects.sphere = sphere;
            
            // 创建矢量条数可视化
            const vectorGroup = new THREE.Group();
            
            for (let i = 0; i < 100; i++) {
                const phi = Math.random() * Math.PI * 2;
                const theta = Math.random() * Math.PI;
                
                const x = 8 * Math.sin(theta) * Math.cos(phi);
                const y = 8 * Math.sin(theta) * Math.sin(phi);
                const z = 8 * Math.cos(theta);
                
                const arrowGeometry = new THREE.ConeGeometry(0.1, 0.5, 6);
                const arrowMaterial = new THREE.MeshPhongMaterial({ color: 0xff6b6b });
                const arrow = new THREE.Mesh(arrowGeometry, arrowMaterial);
                
                arrow.position.set(x, y, z);
                arrow.lookAt(0, 0, 0);
                
                vectorGroup.add(arrow);
            }
            
            scene.add(vectorGroup);
            visualizationObjects.vectorGroup = vectorGroup;
            
            // 创建密度热图
            const densityGeometry = new THREE.SphereGeometry(7.5, 64, 32);
            const densityMaterial = new THREE.ShaderMaterial({
                uniforms: {
                    time: { value: 0 },
                    density: { value: 1.0 }
                },
                vertexShader: `
                    varying vec3 vPosition;
                    void main() {
                        vPosition = position;
                        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                    }
                `,
                fragmentShader: `
                    uniform float time;
                    uniform float density;
                    varying vec3 vPosition;
                    
                    void main() {
                        float r = length(vPosition);
                        float theta = acos(vPosition.z / r);
                        float phi = atan(vPosition.y, vPosition.x);
                        
                        float densityValue = sin(theta * 3.0) * cos(phi * 2.0) * density;
                        vec3 color = mix(vec3(0.0, 0.0, 1.0), vec3(1.0, 0.0, 0.0), densityValue * 0.5 + 0.5);
                        
                        gl_FragColor = vec4(color, 0.6);
                    }
                `,
                transparent: true
            });
            
            const densitySphere = new THREE.Mesh(densityGeometry, densityMaterial);
            scene.add(densitySphere);
            visualizationObjects.densitySphere = densitySphere;
        """
    
    def get_default_viz(self):
        """默认可视化模板"""
        return """
            // 创建基础几何体
            const geometry = new THREE.TorusKnotGeometry(3, 1, 100, 16);
            const material = new THREE.MeshPhongMaterial({ 
                color: 0x667eea,
                shininess: 100
            });
            const mesh = new THREE.Mesh(geometry, material);
            scene.add(mesh);
            visualizationObjects.mainObject = mesh;
            
            // 创建粒子系统
            const particleCount = 1000;
            const particleGeometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particleCount * 3);
            const colors = new Float32Array(particleCount * 3);
            
            for (let i = 0; i < particleCount; i++) {
                positions[i * 3] = (Math.random() - 0.5) * 20;
                positions[i * 3 + 1] = (Math.random() - 0.5) * 20;
                positions[i * 3 + 2] = (Math.random() - 0.5) * 20;
                
                colors[i * 3] = Math.random();
                colors[i * 3 + 1] = Math.random();
                colors[i * 3 + 2] = Math.random();
            }
            
            particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            particleGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
            
            const particleMaterial = new THREE.PointsMaterial({ 
                size: 0.1, 
                vertexColors: true,
                transparent: true,
                opacity: 0.8
            });
            
            const particles = new THREE.Points(particleGeometry, particleMaterial);
            scene.add(particles);
            visualizationObjects.particles = particles;
        """
    
    def get_animation_code(self, formula):
        """生成动画代码"""
        animation_map = {
            "01": """
                // 时空同一化动画
                if (visualizationObjects.lightSpeedArrow) {
                    const C = parameters.C || {x: 1, y: 0, z: 0};
                    const t = parameters.t || time;
                    
                    // 更新光速矢量方向
                    visualizationObjects.lightSpeedArrow.lookAt(C.x, C.y, C.z);
                    
                    // 更新位置
                    const position = new THREE.Vector3(C.x * t, C.y * t, C.z * t);
                    visualizationObjects.lightSpeedArrow.position.copy(position);
                    
                    // 更新轨迹
                    visualizationObjects.trajectoryPoints.push(position.clone());
                    if (visualizationObjects.trajectoryPoints.length > 100) {
                        visualizationObjects.trajectoryPoints.shift();
                    }
                    
                    const trajectoryGeometry = new THREE.BufferGeometry().setFromPoints(visualizationObjects.trajectoryPoints);
                    visualizationObjects.trajectoryLine.geometry.dispose();
                    visualizationObjects.trajectoryLine.geometry = trajectoryGeometry;
                }
            """,
            "02": """
                // 螺旋时空动画
                if (visualizationObjects.particle) {
                    const r = parameters.r || 5;
                    const omega = parameters.omega || 1;
                    const h = parameters.h || 2;
                    
                    const x = r * Math.cos(omega * time);
                    const y = r * Math.sin(omega * time);
                    const z = h * time;
                    
                    visualizationObjects.particle.position.set(x, y, z);
                    
                    // 更新螺旋轨迹
                    const helixPoints = [];
                    for (let t = 0; t <= time + 5; t += 0.1) {
                        const hx = r * Math.cos(omega * t);
                        const hy = r * Math.sin(omega * t);
                        const hz = h * t;
                        helixPoints.push(new THREE.Vector3(hx, hy, hz));
                    }
                    
                    const newGeometry = new THREE.BufferGeometry().setFromPoints(helixPoints);
                    visualizationObjects.helixCurve.geometry.dispose();
                    visualizationObjects.helixCurve.geometry = newGeometry;
                }
            """
        }
        
        return animation_map.get(formula['id'], """
            // 默认动画
            if (visualizationObjects.mainObject) {
                visualizationObjects.mainObject.rotation.x = time * 0.5;
                visualizationObjects.mainObject.rotation.y = time * 0.3;
            }
            
            if (visualizationObjects.particles) {
                visualizationObjects.particles.rotation.y = time * 0.1;
            }
        """)
    
    def get_parameter_update_code(self, formula):
        """生成参数更新代码"""
        return """
            // 更新可视化参数
            // 这里可以根据具体公式添加参数更新逻辑
        """
    
    def get_reset_code(self, formula):
        """生成重置代码"""
        reset_code = ""
        for param in formula.get('parameters', []):
            if param['type'] == 'float':
                reset_code += f"""
                document.getElementById('{param['name']}').value = {param['default']};
                document.getElementById('{param['name']}Value').textContent = '{param['default']}';
                parameters['{param['name']}'] = {param['default']};
                """
            elif param['type'] == 'vector3':
                for i, axis in enumerate(['x', 'y', 'z']):
                    reset_code += f"""
                    document.getElementById('{param['name']}_{axis}').value = {param['default'][i]};
                    document.getElementById('{param['name']}_{axis}Value').textContent = '{param['default'][i]}';
                    """
        return reset_code
    
    def create_theory_document(self, formula):
        """创建理论文档"""
        return f"""# {formula['name']} - 理论分析

## 公式表达

**LaTeX格式：**
```latex
{formula['formula_latex']}
```

**Unicode表示：**
```
{formula['formula_unicode']}
```

## 物理意义

{formula['description']}

## 核心概念

### 物理概念
{chr(10).join([f"- {concept}" for concept in formula['physics_concepts']])}

### 数学工具
{chr(10).join([f"- {concept}" for concept in formula['math_concepts']])}

## 应用领域

{chr(10).join([f"- {app}" for app in formula['applications']])}

## 可视化说明

该公式的可视化采用了{formula['visualization_type']}技术，通过3D交互式界面展示公式的几何和物理含义。

### 参数说明

{chr(10).join([f"- **{param['name']}**: {param['type']}类型，默认值{param['default']}" for param in formula.get('parameters', [])])}

## 理论背景

张祥前统一场论认为，{formula['description']}这一观点为理解宇宙的统一本质提供了新的视角。

## 数学推导

[此处可以添加详细的数学推导过程]

## 实验验证

[此处可以添加相关的实验验证方法和结果]

## 参考文献

1. 张祥前. 统一场论. 
2. [其他相关文献]
"""
    
    def create_readme(self, formula):
        """创建README文档"""
        return f"""# {formula['icon']} {formula['name']}

> {formula['description']}

## 🚀 快速开始

直接打开 `visualization.html` 即可体验交互式3D可视化。

## 📐 公式信息

- **公式编号**: {formula['id']}
- **难度等级**: {formula['difficulty']}/5
- **分类**: {formula['category']}

## 🎮 交互功能

- 🖱️ 鼠标拖拽旋转视角
- 🔍 滚轮缩放场景  
- 🎛️ 实时调节参数
- ▶️ 播放/暂停动画
- 🔄 重置到初始状态

## 📊 技术特性

- **渲染引擎**: WebGL + Three.js
- **数学渲染**: MathJax 3.0
- **响应式设计**: 支持移动设备
- **高性能**: 60fps流畅动画

## 🔬 物理洞察

{formula['description']}

该公式在张祥前统一场论中占据重要地位，揭示了{', '.join(formula['physics_concepts'])}之间的深层联系。

## 📚 相关文档

- [theory.md](theory.md) - 详细理论分析
- [../项目总览.md](../项目总览.md) - 项目整体介绍

## 🌟 特色功能

- 实时3D可视化
- 参数动态调节
- 数学公式同步显示
- 物理概念直观展示

---

*张祥前统一场论可视化项目 - 探索宇宙的统一本质*
"""
    
    def generate_master_index(self):
        """生成主索引页面"""
        # 这里可以更新主索引页面，添加更多功能
        pass

# 主程序
if __name__ == "__main__":
    generator = UnifiedFieldVisualizationGenerator()
    generator.generate_all_visualizations()    
 
   def get_gravity_field_viz(self):
        """引力场定义方程可视化"""
        return """
            // 创建引力场线可视化
            const fieldLineGroup = new THREE.Group();
            
            // 创建中心质量
            const massGeometry = new THREE.SphereGeometry(1, 32, 16);
            const massMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xffd700, 
                emissive: 0x332200 
            });
            const centralMass = new THREE.Mesh(massGeometry, massMaterial);
            scene.add(centralMass);
            visualizationObjects.centralMass = centralMass;
            
            // 创建引力场线
            for (let i = 0; i < 20; i++) {
                const phi = (i / 20) * Math.PI * 2;
                const fieldLine = [];
                
                for (let r = 2; r <= 15; r += 0.5) {
                    const x = r * Math.cos(phi);
                    const y = 0;
                    const z = r * Math.sin(phi);
                    fieldLine.push(new THREE.Vector3(x, y, z));
                }
                
                const lineGeometry = new THREE.BufferGeometry().setFromPoints(fieldLine);
                const lineMaterial = new THREE.LineBasicMaterial({ 
                    color: 0x00ff88, 
                    opacity: 0.7, 
                    transparent: true 
                });
                const line = new THREE.Line(lineGeometry, lineMaterial);
                fieldLineGroup.add(line);
            }
            
            // 垂直方向的场线
            for (let i = 0; i < 10; i++) {
                const theta = (i / 10) * Math.PI;
                const fieldLine = [];
                
                for (let r = 2; r <= 15; r += 0.5) {
                    const x = r * Math.sin(theta);
                    const y = r * Math.cos(theta);
                    const z = 0;
                    fieldLine.push(new THREE.Vector3(x, y, z));
                }
                
                const lineGeometry = new THREE.BufferGeometry().setFromPoints(fieldLine);
                const lineMaterial = new THREE.LineBasicMaterial({ 
                    color: 0x00ff88, 
                    opacity: 0.7, 
                    transparent: true 
                });
                const line = new THREE.Line(lineGeometry, lineMaterial);
                fieldLineGroup.add(line);
            }
            
            scene.add(fieldLineGroup);
            visualizationObjects.fieldLineGroup = fieldLineGroup;
            
            // 创建场强度可视化
            const fieldStrengthGeometry = new THREE.SphereGeometry(12, 64, 32);
            const fieldStrengthMaterial = new THREE.ShaderMaterial({
                uniforms: {
                    time: { value: 0 },
                    G: { value: 6.67e-11 },
                    mass: { value: 1.0 }
                },
                vertexShader: `
                    varying vec3 vPosition;
                    varying float vDistance;
                    void main() {
                        vPosition = position;
                        vDistance = length(position);
                        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                    }
                `,
                fragmentShader: `
                    uniform float time;
                    uniform float G;
                    uniform float mass;
                    varying vec3 vPosition;
                    varying float vDistance;
                    
                    void main() {
                        float fieldStrength = G * mass / (vDistance * vDistance);
                        float intensity = fieldStrength * 1000.0;
                        
                        vec3 color = mix(
                            vec3(0.0, 0.0, 0.5), 
                            vec3(1.0, 0.5, 0.0), 
                            clamp(intensity, 0.0, 1.0)
                        );
                        
                        float alpha = 0.3 * (1.0 - vDistance / 12.0);
                        gl_FragColor = vec4(color, alpha);
                    }
                `,
                transparent: true,
                side: THREE.DoubleSide
            });
            
            const fieldStrengthSphere = new THREE.Mesh(fieldStrengthGeometry, fieldStrengthMaterial);
            scene.add(fieldStrengthSphere);
            visualizationObjects.fieldStrengthSphere = fieldStrengthSphere;
        """
    
    def get_unified_force_viz(self):
        """宇宙大统一方程可视化"""
        return """
            // 创建四种基本力的可视化
            const forceGroup = new THREE.Group();
            
            // 电磁力 - 蓝色螺旋
            const emGeometry = new THREE.TorusKnotGeometry(3, 0.5, 100, 16);
            const emMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x0088ff, 
                emissive: 0x001122 
            });
            const emForce = new THREE.Mesh(emGeometry, emMaterial);
            emForce.position.set(-6, 0, 0);
            forceGroup.add(emForce);
            
            // 强核力 - 红色立方体
            const strongGeometry = new THREE.BoxGeometry(2, 2, 2);
            const strongMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xff0044, 
                emissive: 0x220011 
            });
            const strongForce = new THREE.Mesh(strongGeometry, strongMaterial);
            strongForce.position.set(6, 0, 0);
            forceGroup.add(strongForce);
            
            // 弱核力 - 绿色八面体
            const weakGeometry = new THREE.OctahedronGeometry(1.5);
            const weakMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x00ff44, 
                emissive: 0x002211 
            });
            const weakForce = new THREE.Mesh(weakGeometry, weakMaterial);
            weakForce.position.set(0, 6, 0);
            forceGroup.add(weakForce);
            
            // 引力 - 金色球体
            const gravityGeometry = new THREE.SphereGeometry(1.5, 32, 16);
            const gravityMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xffd700, 
                emissive: 0x332200 
            });
            const gravityForce = new THREE.Mesh(gravityGeometry, gravityMaterial);
            gravityForce.position.set(0, -6, 0);
            forceGroup.add(gravityForce);
            
            scene.add(forceGroup);
            visualizationObjects.forceGroup = forceGroup;
            
            // 创建统一场效应
            const unifiedFieldGeometry = new THREE.SphereGeometry(10, 64, 32);
            const unifiedFieldMaterial = new THREE.ShaderMaterial({
                uniforms: {
                    time: { value: 0 },
                    dmdt: { value: 0.1 },
                    dCdt: { value: new THREE.Vector3(0.1, 0, 0) },
                    dVdt: { value: new THREE.Vector3(0.05, 0, 0) }
                },
                vertexShader: `
                    varying vec3 vPosition;
                    varying vec3 vNormal;
                    uniform float time;
                    
                    void main() {
                        vPosition = position;
                        vNormal = normal;
                        
                        vec3 newPosition = position + normal * sin(time + length(position)) * 0.2;
                        gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
                    }
                `,
                fragmentShader: `
                    uniform float time;
                    uniform float dmdt;
                    uniform vec3 dCdt;
                    uniform vec3 dVdt;
                    varying vec3 vPosition;
                    varying vec3 vNormal;
                    
                    void main() {
                        float r = length(vPosition);
                        float theta = acos(vPosition.z / r);
                        float phi = atan(vPosition.y, vPosition.x);
                        
                        // 四种力的贡献
                        float emContrib = sin(theta * 3.0 + time) * 0.25;
                        float strongContrib = cos(phi * 4.0 + time * 2.0) * 0.25;
                        float weakContrib = sin(theta * phi + time * 0.5) * 0.25;
                        float gravityContrib = cos(r * 0.5 + time) * 0.25;
                        
                        float totalForce = emContrib + strongContrib + weakContrib + gravityContrib;
                        
                        vec3 color = vec3(
                            0.5 + emContrib + strongContrib * 0.5,
                            0.5 + weakContrib + gravityContrib * 0.5,
                            0.5 + totalForce * 0.3
                        );
                        
                        float alpha = 0.4 + abs(totalForce) * 0.3;
                        gl_FragColor = vec4(color, alpha);
                    }
                `,
                transparent: true,
                side: THREE.DoubleSide
            });
            
            const unifiedField = new THREE.Mesh(unifiedFieldGeometry, unifiedFieldMaterial);
            scene.add(unifiedField);
            visualizationObjects.unifiedField = unifiedField;
            
            // 创建力矢量箭头
            const arrowGroup = new THREE.Group();
            
            for (let i = 0; i < 50; i++) {
                const arrowGeometry = new THREE.ConeGeometry(0.1, 0.5, 8);
                const arrowMaterial = new THREE.MeshPhongMaterial({ 
                    color: new THREE.Color().setHSL(Math.random(), 0.7, 0.6) 
                });
                const arrow = new THREE.Mesh(arrowGeometry, arrowMaterial);
                
                const phi = Math.random() * Math.PI * 2;
                const theta = Math.random() * Math.PI;
                const r = 8 + Math.random() * 4;
                
                arrow.position.set(
                    r * Math.sin(theta) * Math.cos(phi),
                    r * Math.sin(theta) * Math.sin(phi),
                    r * Math.cos(theta)
                );
                
                arrowGroup.add(arrow);
            }
            
            scene.add(arrowGroup);
            visualizationObjects.arrowGroup = arrowGroup;
        """
    
    def get_space_wave_viz(self):
        """空间波动方程可视化"""
        return """
            // 创建空间波动网格
            const waveGeometry = new THREE.PlaneGeometry(20, 20, 100, 100);
            const waveMaterial = new THREE.ShaderMaterial({
                uniforms: {
                    time: { value: 0 },
                    frequency: { value: 1.0 },
                    amplitude: { value: 1.0 },
                    c: { value: 1.0 }
                },
                vertexShader: `
                    uniform float time;
                    uniform float frequency;
                    uniform float amplitude;
                    uniform float c;
                    varying float vHeight;
                    varying vec3 vPosition;
                    
                    void main() {
                        vPosition = position;
                        float r = length(position.xy);
                        float wave = amplitude * sin(frequency * r - c * time);
                        
                        vec3 newPosition = position;
                        newPosition.z = wave;
                        vHeight = wave;
                        
                        gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
                    }
                `,
                fragmentShader: `
                    varying float vHeight;
                    varying vec3 vPosition;
                    
                    void main() {
                        float intensity = (vHeight + 1.0) * 0.5;
                        vec3 color = mix(
                            vec3(0.0, 0.2, 0.8),
                            vec3(1.0, 0.4, 0.0),
                            intensity
                        );
                        
                        gl_FragColor = vec4(color, 0.8);
                    }
                `,
                transparent: true,
                side: THREE.DoubleSide
            });
            
            const waveMesh = new THREE.Mesh(waveGeometry, waveMaterial);
            waveMesh.rotation.x = -Math.PI / 2;
            scene.add(waveMesh);
            visualizationObjects.waveMesh = waveMesh;
            
            // 创建波源
            const sourceGeometry = new THREE.SphereGeometry(0.5, 16, 8);
            const sourceMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xffffff, 
                emissive: 0x333333 
            });
            const waveSource = new THREE.Mesh(sourceGeometry, sourceMaterial);
            waveSource.position.set(0, 0.5, 0);
            scene.add(waveSource);
            visualizationObjects.waveSource = waveSource;
            
            // 创建波动粒子
            const particleCount = 200;
            const particleGeometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particleCount * 3);
            const velocities = new Float32Array(particleCount * 3);
            
            for (let i = 0; i < particleCount; i++) {
                positions[i * 3] = (Math.random() - 0.5) * 20;
                positions[i * 3 + 1] = Math.random() * 5;
                positions[i * 3 + 2] = (Math.random() - 0.5) * 20;
                
                velocities[i * 3] = (Math.random() - 0.5) * 0.1;
                velocities[i * 3 + 1] = (Math.random() - 0.5) * 0.1;
                velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.1;
            }
            
            particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            particleGeometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3));
            
            const particleMaterial = new THREE.PointsMaterial({ 
                color: 0x88ccff, 
                size: 0.1,
                transparent: true,
                opacity: 0.8
            });
            
            const waveParticles = new THREE.Points(particleGeometry, particleMaterial);
            scene.add(waveParticles);
            visualizationObjects.waveParticles = waveParticles;
        """
    
    def get_electric_field_viz(self):
        """电场定义方程可视化"""
        return """
            // 创建电荷
            const chargeGeometry = new THREE.SphereGeometry(0.8, 32, 16);
            const chargeMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xff4444, 
                emissive: 0x221111 
            });
            const charge = new THREE.Mesh(chargeGeometry, chargeMaterial);
            scene.add(charge);
            visualizationObjects.charge = charge;
            
            // 创建电场线
            const fieldLineGroup = new THREE.Group();
            
            for (let i = 0; i < 24; i++) {
                const phi = (i / 24) * Math.PI * 2;
                for (let j = 0; j < 12; j++) {
                    const theta = (j / 12) * Math.PI;
                    
                    const fieldLine = [];
                    for (let r = 1.5; r <= 12; r += 0.3) {
                        const x = r * Math.sin(theta) * Math.cos(phi);
                        const y = r * Math.sin(theta) * Math.sin(phi);
                        const z = r * Math.cos(theta);
                        fieldLine.push(new THREE.Vector3(x, y, z));
                    }
                    
                    const lineGeometry = new THREE.BufferGeometry().setFromPoints(fieldLine);
                    const lineMaterial = new THREE.LineBasicMaterial({ 
                        color: 0x4488ff, 
                        opacity: 0.6, 
                        transparent: true 
                    });
                    const line = new THREE.Line(lineGeometry, lineMaterial);
                    fieldLineGroup.add(line);
                }
            }
            
            scene.add(fieldLineGroup);
            visualizationObjects.electricFieldLines = fieldLineGroup;
            
            // 创建电场强度可视化
            const fieldGeometry = new THREE.SphereGeometry(10, 64, 32);
            const fieldMaterial = new THREE.ShaderMaterial({
                uniforms: {
                    time: { value: 0 },
                    charge: { value: 1.0 },
                    epsilon0: { value: 8.85e-12 }
                },
                vertexShader: `
                    varying vec3 vPosition;
                    varying float vDistance;
                    void main() {
                        vPosition = position;
                        vDistance = length(position);
                        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                    }
                `,
                fragmentShader: `
                    uniform float time;
                    uniform float charge;
                    uniform float epsilon0;
                    varying vec3 vPosition;
                    varying float vDistance;
                    
                    void main() {
                        float fieldStrength = abs(charge) / (4.0 * 3.14159 * epsilon0 * vDistance * vDistance);
                        float intensity = fieldStrength * 1e10;
                        
                        vec3 color = mix(
                            vec3(0.0, 0.0, 0.8),
                            vec3(1.0, 0.2, 0.2),
                            clamp(intensity, 0.0, 1.0)
                        );
                        
                        float alpha = 0.2 * (1.0 - vDistance / 10.0) * intensity;
                        gl_FragColor = vec4(color, alpha);
                    }
                `,
                transparent: true,
                side: THREE.DoubleSide
            });
            
            const electricField = new THREE.Mesh(fieldGeometry, fieldMaterial);
            scene.add(electricField);
            visualizationObjects.electricField = electricField;
            
            // 创建测试电荷
            const testChargeGeometry = new THREE.SphereGeometry(0.3, 16, 8);
            const testChargeMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x44ff44, 
                emissive: 0x112211 
            });
            const testCharge = new THREE.Mesh(testChargeGeometry, testChargeMaterial);
            testCharge.position.set(5, 0, 0);
            scene.add(testCharge);
            visualizationObjects.testCharge = testCharge;
            
            // 创建力矢量
            const forceArrowGeometry = new THREE.ConeGeometry(0.2, 1, 8);
            const forceArrowMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xffff44, 
                emissive: 0x222211 
            });
            const forceArrow = new THREE.Mesh(forceArrowGeometry, forceArrowMaterial);
            scene.add(forceArrow);
            visualizationObjects.forceArrow = forceArrow;
        """
    
    def get_magnetic_field_viz(self):
        """磁场定义方程可视化"""
        return """
            // 创建电流导线
            const wireGeometry = new THREE.CylinderGeometry(0.1, 0.1, 20, 16);
            const wireMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x888888, 
                emissive: 0x111111 
            });
            const wire = new THREE.Mesh(wireGeometry, wireMaterial);
            wire.rotation.z = Math.PI / 2;
            scene.add(wire);
            visualizationObjects.wire = wire;
            
            // 创建电流指示
            const currentGeometry = new THREE.ConeGeometry(0.2, 0.5, 8);
            const currentMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xff4444, 
                emissive: 0x221111 
            });
            const currentIndicator = new THREE.Mesh(currentGeometry, currentMaterial);
            currentIndicator.position.set(8, 0, 0);
            currentIndicator.rotation.z = -Math.PI / 2;
            scene.add(currentIndicator);
            visualizationObjects.currentIndicator = currentIndicator;
            
            // 创建磁场线（圆形）
            const magneticFieldGroup = new THREE.Group();
            
            for (let i = 1; i <= 8; i++) {
                const radius = i * 1.5;
                const circleGeometry = new THREE.RingGeometry(radius - 0.05, radius + 0.05, 64);
                const circleMaterial = new THREE.MeshBasicMaterial({ 
                    color: 0x00ff88, 
                    transparent: true, 
                    opacity: 0.7 
                });
                const circle = new THREE.Mesh(circleGeometry, circleMaterial);
                circle.rotation.x = Math.PI / 2;
                magneticFieldGroup.add(circle);
                
                // 添加方向指示箭头
                for (let j = 0; j < 8; j++) {
                    const angle = (j / 8) * Math.PI * 2;
                    const arrowGeometry = new THREE.ConeGeometry(0.1, 0.3, 6);
                    const arrowMaterial = new THREE.MeshPhongMaterial({ color: 0x00ff88 });
                    const arrow = new THREE.Mesh(arrowGeometry, arrowMaterial);
                    
                    arrow.position.set(
                        radius * Math.cos(angle),
                        0,
                        radius * Math.sin(angle)
                    );
                    arrow.rotation.y = angle + Math.PI / 2;
                    arrow.rotation.x = Math.PI / 2;
                    
                    magneticFieldGroup.add(arrow);
                }
            }
            
            scene.add(magneticFieldGroup);
            visualizationObjects.magneticFieldGroup = magneticFieldGroup;
            
            // 创建磁场强度可视化
            const magneticFieldGeometry = new THREE.CylinderGeometry(12, 12, 0.5, 64, 1, true);
            const magneticFieldMaterial = new THREE.ShaderMaterial({
                uniforms: {
                    time: { value: 0 },
                    current: { value: 1.0 },
                    mu0: { value: 4e-7 }
                },
                vertexShader: `
                    varying vec3 vPosition;
                    varying float vRadius;
                    void main() {
                        vPosition = position;
                        vRadius = length(position.xz);
                        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                    }
                `,
                fragmentShader: `
                    uniform float time;
                    uniform float current;
                    uniform float mu0;
                    varying vec3 vPosition;
                    varying float vRadius;
                    
                    void main() {
                        float fieldStrength = mu0 * current / (2.0 * 3.14159 * vRadius);
                        float intensity = fieldStrength * 1e6;
                        
                        vec3 color = mix(
                            vec3(0.0, 0.8, 0.2),
                            vec3(0.8, 1.0, 0.0),
                            clamp(intensity, 0.0, 1.0)
                        );
                        
                        float alpha = 0.3 * intensity;
                        gl_FragColor = vec4(color, alpha);
                    }
                `,
                transparent: true,
                side: THREE.DoubleSide
            });
            
            const magneticFieldMesh = new THREE.Mesh(magneticFieldGeometry, magneticFieldMaterial);
            scene.add(magneticFieldMesh);
            visualizationObjects.magneticFieldMesh = magneticFieldMesh;
            
            // 创建运动电荷
            const movingChargeGeometry = new THREE.SphereGeometry(0.3, 16, 8);
            const movingChargeMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x4444ff, 
                emissive: 0x111122 
            });
            const movingCharge = new THREE.Mesh(movingChargeGeometry, movingChargeMaterial);
            movingCharge.position.set(0, 3, 0);
            scene.add(movingCharge);
            visualizationObjects.movingCharge = movingCharge;
            
            // 创建洛伦兹力矢量
            const lorentzForceGeometry = new THREE.ConeGeometry(0.15, 0.8, 8);
            const lorentzForceMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xff44ff, 
                emissive: 0x221122 
            });
            const lorentzForce = new THREE.Mesh(lorentzForceGeometry, lorentzForceMaterial);
            scene.add(lorentzForce);
            visualizationObjects.lorentzForce = lorentzForce;
        """
    
    def get_lightspeed_propulsion_viz(self):
        """光速飞行器动力学方程可视化"""
        return """
            // 创建飞行器
            const spacecraftGeometry = new THREE.ConeGeometry(1, 3, 8);
            const spacecraftMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x888888, 
                emissive: 0x222222,
                shininess: 100
            });
            const spacecraft = new THREE.Mesh(spacecraftGeometry, spacecraftMaterial);
            spacecraft.rotation.x = Math.PI / 2;
            scene.add(spacecraft);
            visualizationObjects.spacecraft = spacecraft;
            
            // 创建推进系统
            const engineGeometry = new THREE.CylinderGeometry(0.5, 0.8, 1, 16);
            const engineMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xff4444, 
                emissive: 0x441111 
            });
            const engine = new THREE.Mesh(engineGeometry, engineMaterial);
            engine.position.set(0, 0, -2);
            engine.rotation.x = Math.PI / 2;
            spacecraft.add(engine);
            
            // 创建推进粒子流
            const thrustParticleCount = 500;
            const thrustGeometry = new THREE.BufferGeometry();
            const thrustPositions = new Float32Array(thrustParticleCount * 3);
            const thrustVelocities = new Float32Array(thrustParticleCount * 3);
            const thrustColors = new Float32Array(thrustParticleCount * 3);
            
            for (let i = 0; i < thrustParticleCount; i++) {
                thrustPositions[i * 3] = (Math.random() - 0.5) * 2;
                thrustPositions[i * 3 + 1] = (Math.random() - 0.5) * 2;
                thrustPositions[i * 3 + 2] = -2 - Math.random() * 10;
                
                thrustVelocities[i * 3] = (Math.random() - 0.5) * 0.2;
                thrustVelocities[i * 3 + 1] = (Math.random() - 0.5) * 0.2;
                thrustVelocities[i * 3 + 2] = -Math.random() * 2 - 1;
                
                const intensity = Math.random();
                thrustColors[i * 3] = 1.0;
                thrustColors[i * 3 + 1] = intensity * 0.5;
                thrustColors[i * 3 + 2] = intensity * 0.2;
            }
            
            thrustGeometry.setAttribute('position', new THREE.BufferAttribute(thrustPositions, 3));
            thrustGeometry.setAttribute('velocity', new THREE.BufferAttribute(thrustVelocities, 3));
            thrustGeometry.setAttribute('color', new THREE.BufferAttribute(thrustColors, 3));
            
            const thrustMaterial = new THREE.PointsMaterial({ 
                size: 0.2, 
                vertexColors: true,
                transparent: true,
                opacity: 0.8,
                blending: THREE.AdditiveBlending
            });
            
            const thrustParticles = new THREE.Points(thrustGeometry, thrustMaterial);
            scene.add(thrustParticles);
            visualizationObjects.thrustParticles = thrustParticles;
            
            // 创建质量变化可视化
            const massVisualizationGeometry = new THREE.SphereGeometry(2, 32, 16);
            const massVisualizationMaterial = new THREE.ShaderMaterial({
                uniforms: {
                    time: { value: 0 },
                    dmdt: { value: 0.1 },
                    C: { value: new THREE.Vector3(1, 0, 0) },
                    V: { value: new THREE.Vector3(0.5, 0, 0) }
                },
                vertexShader: `
                    uniform float time;
                    uniform float dmdt;
                    varying vec3 vPosition;
                    varying vec3 vNormal;
                    
                    void main() {
                        vPosition = position;
                        vNormal = normal;
                        
                        float pulsation = 1.0 + sin(time * 5.0) * dmdt * 0.5;
                        vec3 newPosition = position * pulsation;
                        
                        gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
                    }
                `,
                fragmentShader: `
                    uniform float time;
                    uniform float dmdt;
                    uniform vec3 C;
                    uniform vec3 V;
                    varying vec3 vPosition;
                    varying vec3 vNormal;
                    
                    void main() {
                        vec3 forceDirection = C - V;
                        float forceIntensity = length(forceDirection) * dmdt;
                        
                        vec3 color = mix(
                            vec3(0.2, 0.2, 0.8),
                            vec3(1.0, 0.8, 0.2),
                            forceIntensity
                        );
                        
                        float alpha = 0.3 + forceIntensity * 0.4;
                        gl_FragColor = vec4(color, alpha);
                    }
                `,
                transparent: true,
                side: THREE.DoubleSide
            });
            
            const massVisualization = new THREE.Mesh(massVisualizationGeometry, massVisualizationMaterial);
            scene.add(massVisualization);
            visualizationObjects.massVisualization = massVisualization;
            
            // 创建时空扭曲效应
            const spacetimeGeometry = new THREE.PlaneGeometry(30, 30, 50, 50);
            const spacetimeMaterial = new THREE.ShaderMaterial({
                uniforms: {
                    time: { value: 0 },
                    spacecraftPosition: { value: new THREE.Vector3(0, 0, 0) }
                },
                vertexShader: `
                    uniform float time;
                    uniform vec3 spacecraftPosition;
                    varying vec3 vPosition;
                    
                    void main() {
                        vPosition = position;
                        
                        float distance = length(position.xy - spacecraftPosition.xy);
                        float warp = exp(-distance * 0.1) * sin(time * 2.0) * 2.0;
                        
                        vec3 newPosition = position;
                        newPosition.z = warp;
                        
                        gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
                    }
                `,
                fragmentShader: `
                    varying vec3 vPosition;
                    
                    void main() {
                        float grid = abs(fract(vPosition.x * 0.1) - 0.5) + abs(fract(vPosition.y * 0.1) - 0.5);
                        vec3 color = mix(vec3(0.1, 0.1, 0.3), vec3(0.3, 0.3, 0.8), grid);
                        
                        gl_FragColor = vec4(color, 0.6);
                    }
                `,
                transparent: true,
                side: THREE.DoubleSide
            });
            
            const spacetimeMesh = new THREE.Mesh(spacetimeGeometry, spacetimeMaterial);
            spacetimeMesh.position.z = -5;
            spacetimeMesh.rotation.x = -Math.PI / 2;
            scene.add(spacetimeMesh);
            visualizationObjects.spacetimeMesh = spacetimeMesh;
            
            // 创建推力矢量
            const thrustVectorGeometry = new THREE.ConeGeometry(0.3, 2, 8);
            const thrustVectorMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x00ff00, 
                emissive: 0x002200 
            });
            const thrustVector = new THREE.Mesh(thrustVectorGeometry, thrustVectorMaterial);
            thrustVector.position.set(0, 2, 0);
            scene.add(thrustVector);
            visualizationObjects.thrustVector = thrustVector;
        """
    
    def get_constant_unification_viz(self):
        """引力光速统一方程可视化"""
        return """
            // 创建引力常数G的可视化
            const GGeometry = new THREE.SphereGeometry(3, 32, 16);
            const GMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xffd700, 
                emissive: 0x332200,
                transparent: true,
                opacity: 0.8
            });
            const GSphere = new THREE.Mesh(GGeometry, GMaterial);
            GSphere.position.set(-8, 0, 0);
            scene.add(GSphere);
            visualizationObjects.GSphere = GSphere;
            
            // 创建光速c的可视化
            const cGeometry = new THREE.SphereGeometry(3, 32, 16);
            const cMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xffffff, 
                emissive: 0x333333,
                transparent: true,
                opacity: 0.8
            });
            const cSphere = new THREE.Mesh(cGeometry, cMaterial);
            cSphere.position.set(8, 0, 0);
            scene.add(cSphere);
            visualizationObjects.cSphere = cSphere;
            
            // 创建统一常数Z的可视化
            const ZGeometry = new THREE.OctahedronGeometry(2);
            const ZMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x667eea, 
                emissive: 0x112244,
                transparent: true,
                opacity: 0.9
            });
            const ZOctahedron = new THREE.Mesh(ZGeometry, ZMaterial);
            ZOctahedron.position.set(0, 0, 0);
            scene.add(ZOctahedron);
            visualizationObjects.ZOctahedron = ZOctahedron;
            
            // 创建连接线
            const connectionGeometry1 = new THREE.BufferGeometry();
            const connectionPoints1 = [
                new THREE.Vector3(-8, 0, 0),
                new THREE.Vector3(0, 0, 0)
            ];
            connectionGeometry1.setFromPoints(connectionPoints1);
            const connectionMaterial1 = new THREE.LineBasicMaterial({ 
                color: 0xffd700, 
                linewidth: 3 
            });
            const connection1 = new THREE.Line(connectionGeometry1, connectionMaterial1);
            scene.add(connection1);
            
            const connectionGeometry2 = new THREE.BufferGeometry();
            const connectionPoints2 = [
                new THREE.Vector3(8, 0, 0),
                new THREE.Vector3(0, 0, 0)
            ];
            connectionGeometry2.setFromPoints(connectionPoints2);
            const connectionMaterial2 = new THREE.LineBasicMaterial({ 
                color: 0xffffff, 
                linewidth: 3 
            });
            const connection2 = new THREE.Line(connectionGeometry2, connectionMaterial2);
            scene.add(connection2);
            
            // 创建数值显示
            const textGeometry = new THREE.RingGeometry(0.5, 1, 16);
            const textMaterial = new THREE.MeshBasicMaterial({ 
                color: 0x88ccff, 
                transparent: true, 
                opacity: 0.7 
            });
            
            const GLabel = new THREE.Mesh(textGeometry, textMaterial);
            GLabel.position.set(-8, -4, 0);
            scene.add(GLabel);
            
            const cLabel = new THREE.Mesh(textGeometry, textMaterial);
            cLabel.position.set(8, -4, 0);
            scene.add(cLabel);
            
            const ZLabel = new THREE.Mesh(textGeometry, textMaterial);
            ZLabel.position.set(0, -4, 0);
            scene.add(ZLabel);
            
            // 创建统一场效应
            const unificationGeometry = new THREE.TorusGeometry(12, 1, 16, 100);
            const unificationMaterial = new THREE.ShaderMaterial({
                uniforms: {
                    time: { value: 0 },
                    G: { value: 6.67e-11 },
                    c: { value: 3e8 }
                },
                vertexShader: `
                    uniform float time;
                    varying vec3 vPosition;
                    varying vec3 vNormal;
                    
                    void main() {
                        vPosition = position;
                        vNormal = normal;
                        
                        vec3 newPosition = position + normal * sin(time + length(position) * 0.1) * 0.5;
                        gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
                    }
                `,
                fragmentShader: `
                    uniform float time;
                    uniform float G;
                    uniform float c;
                    varying vec3 vPosition;
                    varying vec3 vNormal;
                    
                    void main() {
                        float Z = G * c / 2.0;
                        float angle = atan(vPosition.y, vPosition.x);
                        
                        vec3 color = mix(
                            vec3(1.0, 0.8, 0.0),
                            vec3(1.0, 1.0, 1.0),
                            sin(angle * 3.0 + time) * 0.5 + 0.5
                        );
                        
                        float alpha = 0.6 + sin(time + length(vPosition) * 0.2) * 0.2;
                        gl_FragColor = vec4(color, alpha);
                    }
                `,
                transparent: true,
                side: THREE.DoubleSide
            });
            
            const unificationTorus = new THREE.Mesh(unificationGeometry, unificationMaterial);
            scene.add(unificationTorus);
            visualizationObjects.unificationTorus = unificationTorus;
            
            // 创建能量流
            const energyFlowGeometry = new THREE.BufferGeometry();
            const energyFlowPositions = new Float32Array(200 * 3);
            const energyFlowColors = new Float32Array(200 * 3);
            
            for (let i = 0; i < 200; i++) {
                const angle = (i / 200) * Math.PI * 4;
                const radius = 12 + Math.sin(angle * 3) * 2;
                
                energyFlowPositions[i * 3] = radius * Math.cos(angle);
                energyFlowPositions[i * 3 + 1] = radius * Math.sin(angle);
                energyFlowPositions[i * 3 + 2] = Math.sin(angle * 2) * 3;
                
                const intensity = (Math.sin(angle) + 1) * 0.5;
                energyFlowColors[i * 3] = 1.0;
                energyFlowColors[i * 3 + 1] = intensity;
                energyFlowColors[i * 3 + 2] = intensity * 0.5;
            }
            
            energyFlowGeometry.setAttribute('position', new THREE.BufferAttribute(energyFlowPositions, 3));
            energyFlowGeometry.setAttribute('color', new THREE.BufferAttribute(energyFlowColors, 3));
            
            const energyFlowMaterial = new THREE.PointsMaterial({ 
                size: 0.3, 
                vertexColors: true,
                transparent: true,
                opacity: 0.8,
                blending: THREE.AdditiveBlending
            });
            
            const energyFlow = new THREE.Points(energyFlowGeometry, energyFlowMaterial);
            scene.add(energyFlow);
            visualizationObjects.energyFlow = energyFlow;
        """