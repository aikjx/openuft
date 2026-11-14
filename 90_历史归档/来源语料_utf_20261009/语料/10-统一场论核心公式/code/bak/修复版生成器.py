#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZUFT统一场论核心公式 - 修复版可视化生成器
创建最高质量的HTML5 + WebGL + MathJax可视化系统
"""

import json
import os
from pathlib import Path

class UnifiedFieldVisualizationGenerator:
    def __init__(self):
        self.base_path = Path(".")
        
    def generate_single_formula(self, formula_id, formula_name):
        """生成单个公式的高质量可视化"""
        print(f"📐 正在生成: {formula_id}-{formula_name}")
        
        folder_name = f"{formula_id}-{formula_name}"
        folder_path = self.base_path / folder_name
        
        # 确保文件夹存在
        folder_path.mkdir(exist_ok=True)
        
        # 生成高质量HTML可视化
        html_content = self.create_advanced_html(formula_id, formula_name)
        with open(folder_path / "visualization.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ 完成: {formula_id}-{formula_name}")
    
    def create_advanced_html(self, formula_id, formula_name):
        """创建高级HTML5可视化"""
        
        # 获取公式信息
        formula_info = self.get_formula_info(formula_id)
        
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{formula_name} - ZUFT统一场论可视化</title>
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
            text-shadow: none;
        }}
        
        .formula-display {{
            background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px;
            margin: 10px 0; border-left: 4px solid #667eea;
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
        <h2>正在加载 {formula_name} 可视化...</h2>
        <p>ZUFT统一场论 - 高级3D可视化系统</p>
    </div>
    
    <!-- 主画布 -->
    <canvas id="canvas"></canvas>
    
    <!-- 信息面板 -->
    <div id="info-panel" class="ui-panel">
        <div class="panel-title">{formula_info['icon']} {formula_name}</div>
        
        <div class="formula-display">
            <strong>LaTeX公式：</strong><br>
            $${formula_info['latex']}$$
        </div>
        
        <div class="formula-display">
            <strong>Unicode表示：</strong><br>
            <code>{formula_info['unicode']}</code>
        </div>
        
        <p><strong>物理描述：</strong><br>{formula_info['description']}</p>
        
        <div class="physics-insight">
            <h4>🔬 物理洞察</h4>
            <p>{formula_info['insight']}</p>
        </div>
        
        <div class="physics-insight">
            <h4>🌌 宇宙意义</h4>
            <p>{formula_info['cosmic_meaning']}</p>
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
        
        <div class="physics-insight">
            <h4>💡 操作提示</h4>
            <p>• 鼠标拖拽旋转视角<br>
            • 滚轮缩放场景<br>
            • 观察公式的几何本质<br>
            • 感受宇宙的统一美学</p>
        </div>
    </div>

    <script>
        {self.get_visualization_code(formula_id)}
    </script>
</body>
</html>"""
        
        return html_template
    
    def get_formula_info(self, formula_id):
        """获取公式信息"""
        formulas = {
            "01": {
                "icon": "🌌",
                "latex": "\\vec{r}(t) = \\vec{C}t = x\\vec{i} + y\\vec{j} + z\\vec{k}",
                "unicode": "r⃗(t) = C⃗t = xi⃗ + yj⃗ + zk⃗",
                "description": "揭示时间与空间的统一关系，时间是空间位移的度量",
                "insight": "该公式颠覆了传统时空观，认为空间本身在以光速运动，时间只是这种运动的度量。",
                "cosmic_meaning": "这是理解宇宙本质的第一步，空间不是静态容器，而是动态的存在。"
            },
            "02": {
                "icon": "🌀",
                "latex": "\\vec{r}(t) = r\\cos\\omega t \\cdot \\vec{i} + r\\sin\\omega t \\cdot \\vec{j} + ht \\cdot \\vec{k}",
                "unicode": "r⃗(t) = r cos ωt · i⃗ + r sin ωt · j⃗ + ht · k⃗",
                "description": "描述空间中螺旋运动的轨迹，圆周运动与直线运动的叠加",
                "insight": "螺旋运动是宇宙中最基本的运动形式，从电子轨道到星系结构都体现这一规律。",
                "cosmic_meaning": "揭示了宇宙中旋转与直线运动的统一，是理解自旋和磁场的几何基础。"
            },
            "03": {
                "icon": "⚖️",
                "latex": "m = k \\cdot \\frac{dn}{d\\Omega}",
                "unicode": "m = k · dn/dΩ",
                "description": "质量是空间位移矢量条数密度的几何化度量",
                "insight": "质量不再是物质的内在属性，而是空间几何扭曲程度的度量。",
                "cosmic_meaning": "这一定义将质量几何化，为理解引力的本质提供了全新视角。"
            },
            "04": {
                "icon": "🌍",
                "latex": "\\vec{A} = -Gk\\frac{\\Delta n}{\\Delta s}\\frac{\\vec{r}}{r}",
                "unicode": "A⃗ = -Gk(Δn/Δs)(r⃗/r)",
                "description": "引力场是空间几何属性的梯度表现",
                "insight": "引力不是力，而是空间几何的自然表现，物体沿着空间的几何结构运动。",
                "cosmic_meaning": "统一了牛顿引力和爱因斯坦广义相对论，提供了更深层的几何理解。"
            },
            "05": {
                "icon": "⚡",
                "latex": "\\vec{p_0} = m_0\\vec{C_0}",
                "unicode": "p⃗₀ = m₀C⃗₀",
                "description": "静止状态下的动量定义",
                "insight": "即使在静止状态，物体也具有动量，这是空间本身运动的体现。",
                "cosmic_meaning": "揭示了静止的相对性，所有物体都参与空间的光速运动。"
            },
            "06": {
                "icon": "🚀",
                "latex": "\\vec{P} = m(\\vec{C} - \\vec{V})",
                "unicode": "P⃗ = m(C⃗ - V⃗)",
                "description": "运动状态下的动量表达",
                "insight": "动量是物体相对于空间本底运动的度量，体现了绝对运动与相对运动的关系。",
                "cosmic_meaning": "为理解惯性和动量守恒提供了新的几何解释。"
            },
            "07": {
                "icon": "🌟",
                "latex": "\\vec{F} = \\frac{d\\vec{P}}{dt} = \\vec{C}\\frac{dm}{dt} - \\vec{V}\\frac{dm}{dt} + m\\frac{d\\vec{C}}{dt} - m\\frac{d\\vec{V}}{dt}",
                "unicode": "F⃗ = dP⃗/dt = C⃗(dm/dt) - V⃗(dm/dt) + m(dC⃗/dt) - m(dV⃗/dt)",
                "description": "统一的力学方程，描述宇宙中所有力的本质",
                "insight": "四种基本力统一在一个方程中：电磁力、强核力、弱核力和引力都是这个方程的不同体现。",
                "cosmic_meaning": "这是物理学的圣杯——大统一理论的数学表达，揭示了宇宙力的统一本质。"
            },
            "08": {
                "icon": "🌊",
                "latex": "\\nabla^2 L = \\frac{1}{c^2}\\frac{\\partial^2 L}{\\partial t^2}",
                "unicode": "∇²L = (1/c²)(∂²L/∂t²)",
                "description": "描述空间的波动性质",
                "insight": "空间本身可以波动，这为引力波的存在提供了更本质的解释。",
                "cosmic_meaning": "揭示了时空的动态本质，空间不是静态背景，而是可以传播波动的介质。"
            },
            "09": {
                "icon": "⚡",
                "latex": "q = k'k\\frac{1}{\\Omega^2}\\frac{d\\Omega}{dt}",
                "unicode": "q = k'k(1/Ω²)(dΩ/dt)",
                "description": "电荷的几何化定义",
                "insight": "电荷是立体角快速变化的产物，将电荷现象几何化。",
                "cosmic_meaning": "统一了电荷与几何，为理解电磁现象的本质提供了新视角。"
            },
            "10": {
                "icon": "🔌",
                "latex": "\\vec{E} = -\\frac{kk'}{4\\pi\\varepsilon_0\\Omega^2}\\frac{d\\Omega}{dt}\\frac{\\vec{r}}{r^3}",
                "unicode": "E⃗ = -[kk'/(4πε₀Ω²)](dΩ/dt)(r⃗/r³)",
                "description": "电场的统一场论表达",
                "insight": "电场是立体角变化在空间中的表现，与传统库仑定律形式一致但物理含义更深。",
                "cosmic_meaning": "将电场现象追溯到几何本源，体现了电磁现象的几何本质。"
            },
            "11": {
                "icon": "🧲",
                "latex": "\\vec{B} = \\frac{\\mu_0}{4\\pi}\\frac{q\\vec{v} \\times \\vec{r}}{r^3}",
                "unicode": "B⃗ = (μ₀/4π)[q(v⃗ × r⃗)/r³]",
                "description": "磁场的统一场论表达",
                "insight": "磁场是运动电荷（几何化电荷）在空间中产生的旋转效应。",
                "cosmic_meaning": "揭示了磁现象的几何本质，磁场是空间旋转的表现。"
            },
            "12": {
                "icon": "🔄",
                "latex": "\\frac{\\partial^2\\vec{A}}{\\partial t^2} = \\frac{\\vec{V}}{f}(\\nabla \\cdot \\vec{E}) - \\frac{C^2}{f}(\\nabla \\times \\vec{B})",
                "unicode": "∂²A⃗/∂t² = (V⃗/f)(∇·E⃗) - (C²/f)(∇×B⃗)",
                "description": "引力场变化产生电磁场的机制",
                "insight": "引力场的变化可以产生电磁场，这是场统一的直接体现。",
                "cosmic_meaning": "预言了引力与电磁的相互转化，为统一场理论提供了实验验证途径。"
            },
            "13": {
                "icon": "🎯",
                "latex": "\\nabla \\times \\vec{A} = \\frac{\\vec{B}}{f}",
                "unicode": "∇×A⃗ = B⃗/f",
                "description": "磁矢势与磁场的关系",
                "insight": "引力场的旋度直接关联磁场，体现了引力与磁场的内在联系。",
                "cosmic_meaning": "建立了引力场与磁场的桥梁，是场统一的重要环节。"
            },
            "14": {
                "icon": "⚡",
                "latex": "\\vec{E} = -f\\frac{d\\vec{A}}{dt}",
                "unicode": "E⃗ = -f(dA⃗/dt)",
                "description": "引力场变化产生电场",
                "insight": "变化的引力场直接产生电场，这是电磁感应的引力版本。",
                "cosmic_meaning": "预言了引力波探测的新方法，通过电场变化探测引力波。"
            },
            "15": {
                "icon": "🔀",
                "latex": "\\frac{d\\vec{B}}{dt} = -\\frac{\\vec{A} \\times \\vec{E}}{c^2} - \\nabla \\times \\vec{E}",
                "unicode": "dB⃗/dt = -(A⃗×E⃗)/c² - ∇×E⃗",
                "description": "磁场变化产生引力场和电场",
                "insight": "磁场变化不仅产生电场，还产生引力场，这是场相互作用的完整描述。",
                "cosmic_meaning": "揭示了电磁场与引力场的双向耦合，为反重力技术提供理论基础。"
            },
            "16": {
                "icon": "💫",
                "latex": "E = m_0c^2 = mc^2\\sqrt{1-\\frac{v^2}{c^2}}",
                "unicode": "E = m₀c² = mc²√(1-v²/c²)",
                "description": "能量的统一场论表达",
                "insight": "能量是空间光速运动的剧烈程度，质能关系有了新的几何含义。",
                "cosmic_meaning": "将爱因斯坦质能公式纳入统一场论框架，能量成为几何现象。"
            },
            "17": {
                "icon": "🛸",
                "latex": "\\vec{F} = (\\vec{C} - \\vec{V})\\frac{dm}{dt}",
                "unicode": "F⃗ = (C⃗ - V⃗)(dm/dt)",
                "description": "光速飞行器的动力学原理",
                "insight": "通过改变物体质量可以产生巨大推力，这是实现光速飞行的理论基础。",
                "cosmic_meaning": "为星际旅行和反重力技术提供了理论指导，开启了新的推进时代。"
            },
            "18": {
                "icon": "〰️",
                "latex": "L(\\vec{r},t) = f(t-\\frac{r}{c}) + g(t+\\frac{r}{c})",
                "unicode": "L(r⃗,t) = f(t-r/c) + g(t+r/c)",
                "description": "空间波动方程的通解",
                "insight": "空间波动的解包含前进波和后退波，描述了信息在空间中的传播。",
                "cosmic_meaning": "为理解引力波、电磁波等各种波动现象提供了统一的数学框架。"
            },
            "19": {
                "icon": "🌌",
                "latex": "Z = \\frac{G \\cdot c}{2}",
                "unicode": "Z = G·c/2",
                "description": "引力常数与光速的统一关系",
                "insight": "引力常数G与光速c存在深层的数学关系，这可能是验证理论的关键。",
                "cosmic_meaning": "揭示了宇宙基本常数的内在联系，为理解宇宙的数学结构提供了线索。"
            }
        }
        
        return formulas.get(formula_id, formulas["01"])
    
    def get_visualization_code(self, formula_id):
        """根据公式ID生成对应的可视化代码"""
        
        base_code = """
        // 全局变量
        let scene, camera, renderer, controls;
        let animationId, isAnimating = false;
        let visualizationObjects = {};
        let startTime = Date.now();
        
        // 场景初始化
        function initScene() {
            // 创建场景
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0a0a0a);
            scene.fog = new THREE.Fog(0x0a0a0a, 50, 200);
            
            // 创建相机
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(15, 15, 15);
            
            // 创建渲染器
            renderer = new THREE.WebGLRenderer({ 
                canvas: document.getElementById('canvas'), 
                antialias: true,
                alpha: true
            });
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
            """ + self.get_specific_visualization(formula_id) + """
            
            // 开始动画循环
            animate();
            
            // 隐藏加载屏幕
            setTimeout(() => {
                document.getElementById('loadingScreen').classList.add('fade-out');
            }, 1000);
        }
        
        // 光照设置
        function setupLighting() {
            // 环境光
            const ambientLight = new THREE.AmbientLight(0x404080, 0.3);
            scene.add(ambientLight);
            
            // 主光源
            const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
            directionalLight.position.set(20, 20, 10);
            directionalLight.castShadow = true;
            directionalLight.shadow.mapSize.width = 2048;
            directionalLight.shadow.mapSize.height = 2048;
            scene.add(directionalLight);
            
            // 补充光源
            const pointLight = new THREE.PointLight(0x667eea, 0.5, 100);
            pointLight.position.set(-10, 10, -10);
            scene.add(pointLight);
            
            const pointLight2 = new THREE.PointLight(0x764ba2, 0.5, 100);
            pointLight2.position.set(10, -10, 10);
            scene.add(pointLight2);
        }
        
        // 创建坐标系
        function createCoordinateSystem() {
            // 坐标轴
            const axesHelper = new THREE.AxesHelper(10);
            scene.add(axesHelper);
            
            // 网格
            const gridHelper = new THREE.GridHelper(20, 20, 0x444444, 0x222222);
            scene.add(gridHelper);
        }
        
        // 主动画循环
        function animate() {
            animationId = requestAnimationFrame(animate);
            
            const currentTime = (Date.now() - startTime) / 1000;
            
            if (isAnimating) {
                updateVisualization(currentTime);
            }
            
            // 更新控制器
            controls.update();
            
            // 渲染场景
            renderer.render(scene, camera);
        }
        
        // 更新可视化
        function updateVisualization(time) {
            """ + self.get_animation_code(formula_id) + """
        }
        
        // 控制函数
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
        }
        
        function toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        }
        
        // 窗口大小调整
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
        
        // 页面加载完成后初始化
        window.addEventListener('load', () => {
            initScene();
        });
        """
        
        return base_code
    
    def get_specific_visualization(self, formula_id):
        """根据公式ID生成特定的可视化代码"""
        
        visualizations = {
            "01": """
            // 时空同一化方程可视化
            // 创建时空网格
            const spaceTimeGrid = new THREE.Group();
            
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
            
            // 创建轨迹线
            visualizationObjects.trajectoryPoints = [];
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
            """,
            
            "07": """
            // 宇宙大统一方程可视化
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
            """
        }
        
        return visualizations.get(formula_id, """
            // 默认可视化
            const geometry = new THREE.TorusKnotGeometry(3, 1, 100, 16);
            const material = new THREE.MeshPhongMaterial({ 
                color: 0x667eea,
                shininess: 100
            });
            const mesh = new THREE.Mesh(geometry, material);
            scene.add(mesh);
            visualizationObjects.mainObject = mesh;
        """)
    
    def get_animation_code(self, formula_id):
        """生成动画代码"""
        
        animations = {
            "01": """
            // 时空同一化动画
            if (visualizationObjects.lightSpeedArrow) {
                const position = new THREE.Vector3(
                    Math.cos(time) * 5,
                    Math.sin(time) * 5,
                    time * 2
                );
                visualizationObjects.lightSpeedArrow.position.copy(position);
                visualizationObjects.lightSpeedArrow.lookAt(position.x * 2, position.y * 2, position.z + 5);
                
                // 更新轨迹
                visualizationObjects.trajectoryPoints.push(position.clone());
                if (visualizationObjects.trajectoryPoints.length > 100) {
                    visualizationObjects.trajectoryPoints.shift();
                }
            }
            """,
            
            "02": """
            // 螺旋时空动画
            if (visualizationObjects.particle) {
                const r = 5;
                const omega = 1;
                const h = 2;
                
                const x = r * Math.cos(omega * time);
                const y = r * Math.sin(omega * time);
                const z = h * time;
                
                visualizationObjects.particle.position.set(x, y, z);
            }
            """,
            
            "07": """
            // 大统一方程动画
            if (visualizationObjects.forceGroup) {
                visualizationObjects.forceGroup.rotation.y = time * 0.2;
                
                // 各个力的独立运动
                visualizationObjects.forceGroup.children.forEach((force, index) => {
                    force.rotation.x = time * (0.5 + index * 0.1);
                    force.rotation.z = time * (0.3 + index * 0.05);
                });
            }
            """
        }
        
        return animations.get(formula_id, """
            // 默认动画
            if (visualizationObjects.mainObject) {
                visualizationObjects.mainObject.rotation.x = time * 0.5;
                visualizationObjects.mainObject.rotation.y = time * 0.3;
            }
        """)

# 主程序
if __name__ == "__main__":
    generator = UnifiedFieldVisualizationGenerator()
    
    # 生成所有19个公式的可视化
    formulas = [
        ("01", "时空同一化方程"),
        ("02", "三维螺旋时空方程"),
        ("03", "质量定义方程"),
        ("04", "引力场定义方程"),
        ("05", "静止动量方程"),
        ("06", "运动动量方程"),
        ("07", "宇宙大统一方程"),
        ("08", "空间波动方程"),
        ("09", "电荷定义方程"),
        ("10", "电场定义方程"),
        ("11", "磁场定义方程"),
        ("12", "变化引力场产生电磁场"),
        ("13", "磁矢势方程"),
        ("14", "变化引力场产生电场"),
        ("15", "变化磁场产生引力场和电场"),
        ("16", "统一场论能量方程"),
        ("17", "光速飞行器动力学方程"),
        ("18", "空间波动通解"),
        ("19", "引力光速统一方程")
    ]
    
    print("🚀 开始生成ZUFT统一场论核心公式可视化系统...")
    
    for formula_id, formula_name in formulas:
        generator.generate_single_formula(formula_id, formula_name)
    
    print("✅ 所有19个公式的可视化生成完成！")
    print("🌌 ZUFT统一场论可视化系统已就绪！")