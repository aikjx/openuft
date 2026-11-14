#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZUFT统一场论核心公式 - 超级可视化生成器
为19个核心公式分别创建独立的高质量HTML5可视化系统
达到国际顶级论文标准
"""

import os
import json
from pathlib import Path

class SuperVisualizationGenerator:
    def __init__(self):
        self.base_path = Path("utf/统一场论核心公式")
        self.formulas = self.load_formulas()
        
    def load_formulas(self):
        """加载所有公式信息"""
        return [
            {
                "id": "01", "name": "时空同一化方程", "icon": "🌌",
                "formula_latex": r"r⃗(t)=C⃗t=xi⃗+yj⃗+zk⃗",
                "formula_unicode": "r⃗(t)=C⃗t=xi⃗+yj⃗+zk⃗",
                "description": "描述时空的统一性，空间位置矢量与时间的线性关系",
                "physics_concepts": ["时空统一", "光速不变", "相对论"],
                "math_concepts": ["矢量代数", "线性变换", "三维几何"],
                "parameters": [
                    {"name": "speed", "type": "float", "default": 1.0, "range": [0.1, 3.0]},
                    {"name": "direction", "type": "vector3", "default": [1, 0, 0], "range": [-2, 2]}
                ]
            },
            {
                "id": "02", "name": "三维螺旋时空方程", "icon": "🌀",
                "formula_latex": r"r⃗(t) = r\cos\omega t \cdot i⃗ + r\sin\omega t \cdot j⃗ + ht \cdot k⃗",
                "formula_unicode": "r⃗(t) = r cos ωt·i⃗ + r sin ωt·j⃗ + ht·k⃗",
                "description": "描述螺旋形时空轨迹，结合圆周运动和直线运动",
                "physics_concepts": ["螺旋运动", "角频率", "时空几何"],
                "math_concepts": ["参数方程", "三角函数", "螺旋线"],
                "parameters": [
                    {"name": "radius", "type": "float", "default": 5.0, "range": [1.0, 10.0]},
                    {"name": "omega", "type": "float", "default": 1.0, "range": [0.1, 3.0]},
                    {"name": "height", "type": "float", "default": 2.0, "range": [0.5, 5.0]}
                ]
            }
        ]
    
    def generate_all_visualizations(self):
        """生成所有19个公式的可视化"""
        print("🚀 开始生成ZUFT统一场论核心公式可视化系统...")
        
        # 创建完整的公式列表
        all_formulas = self.create_complete_formula_list()
        
        for formula in all_formulas:
            print(f"📐 正在生成: {formula['id']}-{formula['name']}")
            self.generate_single_visualization(formula)
            
        print("✅ 所有可视化生成完成！")
    
    def create_complete_formula_list(self):
        """创建完整的19个公式列表"""
        formulas = [
            {
                "id": "01", "name": "时空同一化方程", "icon": "🌌",
                "formula_latex": r"\vec{r}(t)=\vec{C}t=x\vec{i}+y\vec{j}+z\vec{k}",
                "description": "描述时空的统一性，空间位置矢量与时间的线性关系"
            },
            {
                "id": "02", "name": "三维螺旋时空方程", "icon": "🌀", 
                "formula_latex": r"\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}",
                "description": "描述螺旋形时空轨迹，结合圆周运动和直线运动"
            }
        ]
        # 继续添加其他17个公式
        formulas.extend([
            {
                "id": "03", "name": "质量定义方程", "icon": "⚖️",
                "formula_latex": r"m = k \cdot \frac{dn}{d\Omega}",
                "description": "通过立体角中的矢量条数密度定义质量"
            },
            {
                "id": "04", "name": "引力场定义方程", "icon": "🌍",
                "formula_latex": r"\overrightarrow{A}=-Gk\frac{\Delta n}{\Delta s}\frac{\overrightarrow{r}}{r}",
                "description": "定义引力场强度与空间矢量条数梯度的关系"
            },
            {
                "id": "05", "name": "静止动量方程", "icon": "⚡",
                "formula_latex": r"\overrightarrow{p}_{0}=m_{0}\overrightarrow{C}_{0}",
                "description": "静止物体的动量定义"
            },
            {
                "id": "06", "name": "运动动量方程", "icon": "🚀",
                "formula_latex": r"\overrightarrow{P}=m(\overrightarrow{C}-\overrightarrow{V})",
                "description": "运动物体的动量修正公式"
            },
            {
                "id": "07", "name": "宇宙大统一方程", "icon": "🌌",
                "formula_latex": r"F = \frac{d\vec{P}}{dt} = \vec{C}\frac{dm}{dt} - \vec{V}\frac{dm}{dt} + m\frac{d\vec{C}}{dt} - m\frac{d\vec{V}}{dt}",
                "description": "统一描述宇宙中所有力的基本方程"
            },
            {
                "id": "08", "name": "空间波动方程", "icon": "〰️",
                "formula_latex": r"\frac{\partial^2 L}{\partial x^2} + \frac{\partial^2 L}{\partial y^2} + \frac{\partial^2 L}{\partial z^2} = \frac{1}{c^2} \frac{\partial^2 L}{\partial t^2}",
                "description": "描述空间中波动现象的基本方程"
            },
            {
                "id": "09", "name": "电荷定义方程", "icon": "⚡",
                "formula_latex": r"q=k^{\prime}k\frac{1}{\Omega^{2}}\frac{d\Omega}{dt}",
                "description": "通过立体角变化率定义电荷"
            },
            {
                "id": "10", "name": "电场定义方程", "icon": "🔌",
                "formula_latex": r"\vec{E}=-\frac{kk^{\prime}}{4\pi\epsilon_0\Omega^2}\frac{d\Omega}{dt}\frac{\vec{r}}{r^3}",
                "description": "电场强度与立体角变化的关系"
            },
            {
                "id": "11", "name": "磁场定义方程", "icon": "🧲",
                "formula_latex": r"\vec{B}=\frac{\mu_{0} \gamma k k^{\prime}}{4 \pi \Omega^{2}} \frac{d \Omega}{d t} \frac{[(x-v t) \vec{i}+y \vec{j}+z \vec{k}]}{\left[\gamma^{2}(x-v t)^{2}+y^{2}+z^{2}\right]^{\frac{3}{2}}}",
                "description": "磁场与运动电荷的相对论性关系"
            },
            {
                "id": "12", "name": "变化引力场产生电磁场", "icon": "🔄",
                "formula_latex": r"\frac{\partial^{2}\overline{A}}{\partial t^{2}}=\frac{\overline{V}}{f}\left(\overline{\nabla}\cdot\overline{E}\right)-\frac{C^{2}}{f}\left(\overline{\nabla}\times\overline{B}\right)",
                "description": "变化的引力场如何产生电磁场"
            },
            {
                "id": "13", "name": "磁矢势方程", "icon": "🌀",
                "formula_latex": r"\vec{\nabla} \times \vec{A} = \frac{\vec{B}}{f}",
                "description": "磁矢势与磁场的关系"
            },
            {
                "id": "14", "name": "变化引力场产生电场", "icon": "⚡",
                "formula_latex": r"\vec{E}=-f\frac{d\vec{A}}{dt}",
                "description": "变化的引力场产生电场的机制"
            },
            {
                "id": "15", "name": "变化磁场产生引力场和电场", "icon": "🔄",
                "formula_latex": r"\frac{d\overrightarrow{B}}{dt}=\frac{-\overrightarrow{A}\times\overrightarrow{E}}{c^2}-\frac{\overrightarrow{V}}{c^{2}}\times\frac{d\overrightarrow{E}}{dt}",
                "description": "变化磁场产生引力场和电场的耦合关系"
            },
            {
                "id": "16", "name": "统一场论能量方程", "icon": "💫",
                "formula_latex": r"e = m_0 c^2 = mc^2\sqrt{1 - \frac{v^2}{c^2}}",
                "description": "能量与质量的统一关系"
            },
            {
                "id": "17", "name": "光速飞行器动力学方程", "icon": "🛸",
                "formula_latex": r"\vec{F} = (\vec{C} - \vec{V})\frac{dm}{dt}",
                "description": "光速飞行器的推进动力学原理"
            },
            {
                "id": "18", "name": "空间波动通解", "icon": "〰️",
                "formula_latex": r"L(r,t) = f(t-r/c) + g(t+r/c)",
                "description": "空间波动方程的通解形式"
            },
            {
                "id": "19", "name": "引力光速统一方程", "icon": "🌟",
                "formula_latex": r"Z = \frac{Gc}{2}",
                "description": "引力常数与光速的统一关系"
            }
        ])
        
        return formulas
    
    def generate_single_visualization(self, formula):
        """为单个公式生成完整的可视化"""
        folder_name = f"{formula['id']}-{formula['name']}"
        folder_path = self.base_path / folder_name
        
        # 确保文件夹存在
        folder_path.mkdir(exist_ok=True)
        
        # 生成HTML可视化
        html_content = self.create_html_visualization(formula)
        with open(folder_path / "visualization.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ 已生成: {folder_name}/visualization.html")
    
    def create_html_visualization(self, formula):
        """创建HTML可视化代码"""
        
        # 根据公式ID选择特定的可视化代码
        viz_code = self.get_visualization_code(formula['id'])
        
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{formula['name']} - ZUFT统一场论可视化</title>
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
        
        .panel-title {{
            font-size: 1.4em; font-weight: bold; margin-bottom: 15px;
            background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
            background-clip: text; -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
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
        
        .physics-insight {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 1px solid rgba(102, 126, 234, 0.3); padding: 15px; 
            border-radius: 10px; margin: 15px 0;
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
    </style>
    
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
    <div id="loadingScreen" class="loading-screen">
        <div class="loading-spinner"></div>
        <h2>正在加载 {formula['name']} 可视化...</h2>
        <p>ZUFT统一场论 - 高级3D可视化系统</p>
    </div>
    
    <canvas id="canvas"></canvas>
    
    <div id="info-panel" class="ui-panel">
        <div class="panel-title">{formula['icon']} {formula['name']}</div>
        
        <div class="formula-display">
            <strong>LaTeX公式：</strong><br>
            ${formula['formula_latex']}$
        </div>
        
        <p><strong>物理描述：</strong><br>{formula['description']}</p>
        
        <div class="physics-insight">
            <h4>🔬 物理意义</h4>
            <p>该公式是ZUFT统一场论的核心组成部分，揭示了宇宙基本规律的深层结构。</p>
        </div>
    </div>
    
    <div id="controls-panel" class="ui-panel">
        <div class="panel-title">🎮 交互控制</div>
        
        <div style="text-align: center; margin-bottom: 15px;">
            <button class="control-button" onclick="toggleAnimation()">
                <span id="playPauseIcon">▶️</span> <span id="playPauseText">开始</span>
            </button>
            <button class="control-button" onclick="resetVisualization()">🔄 重置</button>
            <button class="control-button" onclick="toggleFullscreen()">🔍 全屏</button>
        </div>
        
        <div class="physics-insight">
            <h4>💡 操作提示</h4>
            <p>• 鼠标拖拽旋转视角<br>
            • 滚轮缩放场景<br>
            • 点击按钮控制动画<br>
            • 观察公式的几何表现</p>
        </div>
    </div>

    <script>
        {viz_code}
    </script>
</body>
</html>"""
        
        return html_template    

    def get_visualization_code(self, formula_id):
        """根据公式ID返回对应的可视化JavaScript代码"""
        
        base_code = """
        // 全局变量
        let scene, camera, renderer, controls;
        let animationId, isAnimating = false;
        let visualizationObjects = {};
        let startTime = Date.now();
        
        // 场景初始化
        function initScene() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0a0a0a);
            scene.fog = new THREE.Fog(0x0a0a0a, 50, 200);
            
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(15, 15, 15);
            
            renderer = new THREE.WebGLRenderer({ 
                canvas: document.getElementById('canvas'), 
                antialias: true,
                alpha: true
            });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            
            setupLighting();
            createCoordinateSystem();
        """
        
        # 根据公式ID添加特定的可视化代码
        specific_code = self.get_specific_visualization_code(formula_id)
        
        animation_code = """
            animate();
            
            setTimeout(() => {
                document.getElementById('loadingScreen').classList.add('fade-out');
            }, 1000);
        }
        
        function setupLighting() {
            const ambientLight = new THREE.AmbientLight(0x404080, 0.3);
            scene.add(ambientLight);
            
            const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
            directionalLight.position.set(20, 20, 10);
            directionalLight.castShadow = true;
            scene.add(directionalLight);
            
            const pointLight = new THREE.PointLight(0x667eea, 0.5, 100);
            pointLight.position.set(-10, 10, -10);
            scene.add(pointLight);
        }
        
        function createCoordinateSystem() {
            const axesHelper = new THREE.AxesHelper(10);
            scene.add(axesHelper);
            
            const gridHelper = new THREE.GridHelper(20, 20, 0x444444, 0x222222);
            scene.add(gridHelper);
        }
        
        function animate() {
            animationId = requestAnimationFrame(animate);
            
            const currentTime = (Date.now() - startTime) / 1000;
            
            if (isAnimating) {
                updateVisualization(currentTime);
            }
            
            controls.update();
            renderer.render(scene, camera);
        }
        
        function updateVisualization(time) {
            // 更新可视化对象
            for (let key in visualizationObjects) {
                const obj = visualizationObjects[key];
                if (obj && obj.rotation) {
                    obj.rotation.y += 0.01;
                }
            }
        }
        
        function toggleAnimation() {
            isAnimating = !isAnimating;
            const icon = document.getElementById('playPauseIcon');
            const text = document.getElementById('playPauseText');
            
            if (isAnimating) {
                icon.textContent = '⏸️';
                text.textContent = '暂停';
            } else {
                icon.textContent = '▶️';
                text.textContent = '开始';
            }
        }
        
        function resetVisualization() {
            startTime = Date.now();
            camera.position.set(15, 15, 15);
            controls.reset();
        }
        
        function toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        }
        
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
        
        window.addEventListener('load', () => {
            initScene();
        });
        """
        
        return base_code + specific_code + animation_code
    
    def get_specific_visualization_code(self, formula_id):
        """为每个公式生成特定的可视化代码"""
        
        visualizations = {
            "01": """
            // 时空同一化方程可视化
            const spaceTimeGrid = new THREE.Group();
            
            // 创建时空网格
            for (let i = -10; i <= 10; i += 2) {
                for (let j = -10; j <= 10; j += 2) {
                    const geometry = new THREE.BufferGeometry();
                    const positions = new Float32Array([
                        i, -10, j, i, 10, j
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
            const arrowMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xffffff, 
                emissive: 0x333333 
            });
            const lightSpeedArrow = new THREE.Mesh(arrowGeometry, arrowMaterial);
            scene.add(lightSpeedArrow);
            visualizationObjects.lightSpeedArrow = lightSpeedArrow;
            
            // 创建轨迹粒子
            const particleGeometry = new THREE.SphereGeometry(0.3);
            const particleMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xff6b6b, 
                emissive: 0x330000 
            });
            const particle = new THREE.Mesh(particleGeometry, particleMaterial);
            scene.add(particle);
            visualizationObjects.particle = particle;
            """,
            
            "02": """
            // 三维螺旋时空方程可视化
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
            
            // 更新粒子位置的函数
            function updateVisualization(time) {
                const r = 5;
                const omega = 1;
                const h = 2;
                const t = time;
                
                if (visualizationObjects.particle) {
                    visualizationObjects.particle.position.set(
                        r * Math.cos(omega * t),
                        r * Math.sin(omega * t),
                        h * t % 40 - 20
                    );
                }
            }
            """,
            
            "03": """
            // 质量定义方程可视化 - 立体角和矢量条数
            const sphereGeometry = new THREE.SphereGeometry(8, 32, 16);
            const sphereMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x667eea, 
                transparent: true, 
                opacity: 0.2,
                wireframe: true
            });
            const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
            scene.add(sphere);
            visualizationObjects.sphere = sphere;
            
            // 创建矢量条
            const vectorGroup = new THREE.Group();
            for (let i = 0; i < 200; i++) {
                const phi = Math.random() * Math.PI * 2;
                const theta = Math.random() * Math.PI;
                
                const x = 8 * Math.sin(theta) * Math.cos(phi);
                const y = 8 * Math.sin(theta) * Math.sin(phi);
                const z = 8 * Math.cos(theta);
                
                const arrowGeometry = new THREE.ConeGeometry(0.1, 0.8, 6);
                const arrowMaterial = new THREE.MeshPhongMaterial({ 
                    color: new THREE.Color().setHSL(Math.random(), 0.7, 0.6) 
                });
                const arrow = new THREE.Mesh(arrowGeometry, arrowMaterial);
                
                arrow.position.set(x, y, z);
                arrow.lookAt(0, 0, 0);
                
                vectorGroup.add(arrow);
            }
            scene.add(vectorGroup);
            visualizationObjects.vectorGroup = vectorGroup;
            """,
            
            "04": """
            // 引力场定义方程可视化
            const fieldGroup = new THREE.Group();
            
            // 创建引力场线
            for (let i = 0; i < 50; i++) {
                const angle = (i / 50) * Math.PI * 2;
                const fieldLinePoints = [];
                
                for (let r = 2; r <= 15; r += 0.5) {
                    const x = r * Math.cos(angle);
                    const y = 0;
                    const z = r * Math.sin(angle);
                    fieldLinePoints.push(new THREE.Vector3(x, y, z));
                }
                
                const fieldLineGeometry = new THREE.BufferGeometry().setFromPoints(fieldLinePoints);
                const fieldLineMaterial = new THREE.LineBasicMaterial({ 
                    color: 0x00ff88,
                    opacity: 0.6,
                    transparent: true
                });
                const fieldLine = new THREE.Line(fieldLineGeometry, fieldLineMaterial);
                fieldGroup.add(fieldLine);
            }
            scene.add(fieldGroup);
            visualizationObjects.fieldGroup = fieldGroup;
            
            // 中心质量
            const massGeometry = new THREE.SphereGeometry(1);
            const massMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xffaa00,
                emissive: 0x442200
            });
            const centralMass = new THREE.Mesh(massGeometry, massMaterial);
            scene.add(centralMass);
            visualizationObjects.centralMass = centralMass;
            """
        }
        
        # 为其他公式提供默认可视化
        default_viz = """
        // 默认可视化 - 创建美丽的几何体
        const geometry = new THREE.TorusKnotGeometry(3, 1, 100, 16);
        const material = new THREE.MeshPhongMaterial({ 
            color: 0x667eea,
            shininess: 100
        });
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);
        visualizationObjects.mainObject = mesh;
        
        // 粒子系统
        const particleCount = 1000;
        const particleGeometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);
        
        for (let i = 0; i < particleCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 50;
            positions[i * 3 + 1] = (Math.random() - 0.5) * 50;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 50;
            
            colors[i * 3] = Math.random();
            colors[i * 3 + 1] = Math.random();
            colors[i * 3 + 2] = Math.random();
        }
        
        particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        particleGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        
        const particleMaterial = new THREE.PointsMaterial({ 
            size: 0.5, 
            vertexColors: true,
            transparent: true,
            opacity: 0.8
        });
        const particles = new THREE.Points(particleGeometry, particleMaterial);
        scene.add(particles);
        visualizationObjects.particles = particles;
        """
        
        return visualizations.get(formula_id, default_viz)

if __name__ == "__main__":
    generator = SuperVisualizationGenerator()
    generator.generate_all_visualizations()