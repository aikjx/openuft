#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZUFT统一场论核心公式项目结构创建器
Unified Field Theory Core Formulas Project Structure Creator

自动创建17个核心公式的完整项目结构
Author: Unified Field Theory Visualization Team
Date: 2025-09-16
"""

import os
from pathlib import Path

# 17个核心公式的详细信息
FORMULAS = [
    {
        "id": "01",
        "name": "时空同一化方程",
        "formula": r"\vec{r}(t) = \vec{C}t = x\vec{i} + y\vec{j} + z\vec{k}",
        "description": "揭示时间与空间的统一关系，时间是空间位移的度量",
        "icon": "🌌"
    },
    {
        "id": "02", 
        "name": "三维螺旋时空方程",
        "formula": r"\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}",
        "description": "描述空间中螺旋运动的轨迹，圆周运动与直线运动的叠加",
        "icon": "🌀"
    },
    {
        "id": "03",
        "name": "质量定义方程", 
        "formula": r"m = k \cdot \frac{dn}{d\Omega}",
        "description": "质量是空间位移矢量条数密度的几何化度量",
        "icon": "⚖️"
    },
    {
        "id": "04",
        "name": "引力场定义方程",
        "formula": r"\vec{A} = -Gk\frac{\Delta n}{\Delta s}\frac{\vec{r}}{r}",
        "description": "引力场是空间几何属性的梯度表现",
        "icon": "🌍"
    },
    {
        "id": "05",
        "name": "静止动量方程",
        "formula": r"\vec{p}_0 = m_0\vec{C}_0",
        "description": "静止状态下的动量定义",
        "icon": "⚡"
    },
    {
        "id": "06",
        "name": "运动动量方程",
        "formula": r"\vec{P} = m(\vec{C} - \vec{V})",
        "description": "运动状态下的动量表达",
        "icon": "🚀"
    },
    {
        "id": "07",
        "name": "宇宙大统一方程",
        "formula": r"F = \frac{d\vec{P}}{dt} = \vec{C}\frac{dm}{dt} - \vec{V}\frac{dm}{dt} + m\frac{d\vec{C}}{dt} - m\frac{d\vec{V}}{dt}",
        "description": "统一的力学方程，描述宇宙中所有力的本质",
        "icon": "🌟"
    },
    {
        "id": "08",
        "name": "空间波动方程",
        "formula": r"\frac{\partial^2 L}{\partial x^2} + \frac{\partial^2 L}{\partial y^2} + \frac{\partial^2 L}{\partial z^2} = \frac{1}{c^2} \frac{\partial^2 L}{\partial t^2}",
        "description": "描述空间的波动性质",
        "icon": "🌊"
    },
    {
        "id": "09",
        "name": "电荷定义方程",
        "formula": r"q = k'k\frac{1}{\Omega^2}\frac{d\Omega}{dt}",
        "description": "电荷的几何化定义",
        "icon": "⚡"
    },
    {
        "id": "10",
        "name": "电场定义方程",
        "formula": r"\vec{E} = -\frac{kk'}{4\pi\epsilon_0\Omega^2}\frac{d\Omega}{dt}\frac{\vec{r}}{r^3}",
        "description": "电场的统一场论表达",
        "icon": "🔌"
    },
    {
        "id": "11",
        "name": "磁场定义方程",
        "formula": r"\vec{B} = \frac{\mu_0 \gamma k k'}{4 \pi \Omega^2} \frac{d \Omega}{d t} \frac{[(x-v t) \vec{i}+y \vec{j}+z \vec{k}]}{[\gamma^2(x-v t)^2+y^2+z^2]^{3/2}}",
        "description": "磁场的统一场论表达",
        "icon": "🧲"
    },
    {
        "id": "12",
        "name": "变化引力场产生电磁场",
        "formula": r"\frac{\partial^2\vec{A}}{\partial t^2} = \frac{\vec{V}}{f}(\nabla \cdot \vec{E}) - \frac{C^2}{f}(\nabla \times \vec{B})",
        "description": "引力场变化产生电磁场的机制",
        "icon": "🔄"
    },
    {
        "id": "13",
        "name": "磁矢势方程",
        "formula": r"\vec{\nabla} \times \vec{A} = \frac{\vec{B}}{f}",
        "description": "磁矢势与磁场的关系",
        "icon": "🎯"
    },
    {
        "id": "14",
        "name": "变化引力场产生电场",
        "formula": r"\vec{E} = -f\frac{d\vec{A}}{dt}",
        "description": "引力场变化产生电场",
        "icon": "⚡"
    },
    {
        "id": "15",
        "name": "变化磁场产生引力场和电场",
        "formula": r"\frac{d\vec{B}}{dt} = \frac{-\vec{A} \times \vec{E}}{c^2} - \frac{\vec{V}}{c^2} \times \frac{d\vec{E}}{dt}",
        "description": "磁场变化产生引力场和电场",
        "icon": "🔀"
    },
    {
        "id": "16",
        "name": "统一场论能量方程",
        "formula": r"e = m_0 c^2 = mc^2\sqrt{1 - \frac{v^2}{c^2}}",
        "description": "能量的统一场论表达",
        "icon": "💫"
    },
    {
        "id": "17",
        "name": "光速飞行器动力学方程",
        "formula": r"\vec{F} = (\vec{C} - \vec{V})\frac{dm}{dt}",
        "description": "光速飞行器的动力学原理",
        "icon": "🛸"
    },
    {
        "id": "18",
        "name": "空间波动通解",
        "formula": r"L(r,t) = f(t-r/c) + g(t+r/c)",
        "description": "空间波动方程的通解",
        "icon": "〰️"
    },
    {
        "id": "19",
        "name": "引力光速统一方程",
        "formula": r"Z = \frac{Gc}{2}",
        "description": "引力常数与光速的统一关系",
        "icon": "🌌"
    }
]

def create_formula_folder(formula_info):
    """为单个公式创建完整的文件夹结构"""
    folder_name = f"{formula_info['id']}-{formula_info['name']}"
    folder_path = Path(f"utf/统一场论核心公式/{folder_name}")
    
    # 创建主文件夹
    folder_path.mkdir(parents=True, exist_ok=True)
    
    # 创建子文件夹
    (folder_path / "assets").mkdir(exist_ok=True)
    (folder_path / "examples").mkdir(exist_ok=True)
    
    # 创建README.md
    readme_content = f"""# {formula_info['icon']} {formula_info['name']}

## 📐 公式表达

$${formula_info['formula']}$$

## 🎯 物理意义

{formula_info['description']}

### 核心概念
- **基本定义**：[待补充具体概念]
- **物理意义**：[待补充物理解释]
- **应用范围**：[待补充应用领域]

### 物理解释
1. **参数说明**：[待补充各参数的物理意义]
2. **数学结构**：[待补充数学形式的分析]
3. **物理图像**：[待补充直观的物理图像]

## 🔬 理论背景

### 历史发展
- **传统理论**：[待补充传统理论观点]
- **统一场论**：[待补充统一场论的创新]
- **突破意义**：[待补充理论突破的意义]

### 数学基础
1. **数学工具**：[待补充所需数学工具]
2. **推导过程**：[待补充推导步骤]
3. **数学性质**：[待补充数学性质分析]

## 🎮 可视化特色

### 交互功能
- **参数控制**：实时调节公式参数
- **多视角观察**：从不同角度理解公式
- **动态演示**：展示公式的动态特性
- **数值计算**：实时计算和显示结果

### 视觉效果
- **3D可视化**：立体展示物理过程
- **动画效果**：流畅的动态演示
- **交互界面**：直观的用户界面
- **数学渲染**：精美的公式显示

## 📊 教育价值

### 学习目标
1. 理解公式的物理意义
2. 掌握相关的数学概念
3. 认识理论的创新之处
4. 培养物理直觉和数学思维

### 适用对象
- 物理学专业学生
- 理论物理研究者
- 对统一场论感兴趣的学习者
- 科普教育工作者

## 🔗 与其他公式的关系

- **前置公式**：[待补充前置依赖]
- **后续公式**：[待补充后续发展]
- **关联公式**：[待补充相关公式]

## 🚀 技术实现

- **前端技术**：HTML5 + CSS3 + JavaScript
- **3D渲染**：Three.js + WebGL
- **数学渲染**：MathJax
- **交互控制**：响应式设计

## 📚 参考资料

- ZUFT统一场论相关文献
- 相关物理学教材
- 数学物理方法参考书

---

*本文档是ZUFT统一场论核心公式可视化项目的一部分*
"""
    
    with open(folder_path / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # 创建theory.md
    theory_content = f"""# {formula_info['icon']} {formula_info['name']} - 理论背景

## 🔬 理论基础

### 统一场论框架
{formula_info['name']}是ZUFT统一场论体系中的重要组成部分，它在整个理论框架中起到[具体作用]的关键作用。

### 数学推导
[待补充详细的数学推导过程]

### 物理解释
[待补充深入的物理解释]

## 📖 历史发展

### 传统理论的局限
[待补充传统理论的问题]

### 统一场论的创新
[待补充统一场论的突破]

## 🔍 深入分析

### 数学性质
[待补充数学性质分析]

### 物理含义
[待补充物理含义解析]

### 实验验证
[待补充实验验证方法]

## 🌟 创新意义

### 理论突破
[待补充理论突破点]

### 应用前景
[待补充应用前景]

---

*详细的理论分析文档*
"""
    
    with open(folder_path / "theory.md", "w", encoding="utf-8") as f:
        f.write(theory_content)
    
    # 创建基础的visualization.html模板
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{formula_info['name']} - 交互式3D可视化</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden; color: white;
        }}
        #canvas {{ display: block; cursor: grab; }}
        .ui-panel {{
            position: absolute; background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px; padding: 20px; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
        }}
        #info-panel {{ top: 20px; left: 20px; width: 380px; }}
        #controls-panel {{ top: 20px; right: 20px; width: 300px; }}
        .panel-title {{
            font-size: 1.3em; font-weight: bold; margin-bottom: 15px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .button {{
            background: linear-gradient(45deg, #667eea, #764ba2); color: white; border: none;
            padding: 10px 20px; border-radius: 20px; cursor: pointer; margin: 5px;
            transition: all 0.3s ease;
        }}
        .button:hover {{ transform: translateY(-2px); }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
    <canvas id="canvas"></canvas>
    
    <div id="info-panel" class="ui-panel">
        <div class="panel-title">{formula_info['icon']} {formula_info['name']}</div>
        <p><strong>公式：</strong> ${formula_info['formula']}$</p>
        <p><strong>描述：</strong> {formula_info['description']}</p>
    </div>
    
    <div id="controls-panel" class="ui-panel">
        <div class="panel-title">🎮 控制面板</div>
        <button class="button" onclick="startVisualization()">▶️ 开始</button>
        <button class="button" onclick="pauseVisualization()">⏸️ 暂停</button>
        <button class="button" onclick="resetVisualization()">🔄 重置</button>
    </div>

    <script>
        let scene, camera, renderer;
        let animationId, isAnimating = false;
        
        function initScene() {{
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0a0a0a);
            
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(10, 10, 10);
            camera.lookAt(0, 0, 0);
            
            renderer = new THREE.WebGLRenderer({{ canvas: document.getElementById('canvas'), antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            
            // 添加基础光照
            const ambientLight = new THREE.AmbientLight(0x404080, 0.4);
            scene.add(ambientLight);
            const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
            directionalLight.position.set(10, 10, 5);
            scene.add(directionalLight);
            
            // 添加坐标轴
            const axesHelper = new THREE.AxesHelper(5);
            scene.add(axesHelper);
            
            // TODO: 添加具体的可视化内容
            
            animate();
        }}
        
        function animate() {{
            animationId = requestAnimationFrame(animate);
            
            if (isAnimating) {{
                // TODO: 添加动画逻辑
            }}
            
            renderer.render(scene, camera);
        }}
        
        function startVisualization() {{ isAnimating = true; }}
        function pauseVisualization() {{ isAnimating = false; }}
        function resetVisualization() {{ isAnimating = false; /* TODO: 重置逻辑 */ }}
        
        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
        
        window.addEventListener('load', () => {{
            initScene();
            if (window.MathJax) setTimeout(() => MathJax.typesetPromise(), 1000);
        }});
    </script>
</body>
</html>"""
    
    with open(folder_path / "visualization.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print(f"✅ 已创建: {folder_name}")

def create_index_html():
    """创建主索引页面"""
    index_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZUFT统一场论核心公式可视化</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white; padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 50px; }
        .header h1 { font-size: 3em; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .formula-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }
        .formula-card {
            background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
            border-radius: 15px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .formula-card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3); }
        .formula-title { font-size: 1.2em; font-weight: bold; margin-bottom: 10px; }
        .formula-description { font-size: 0.9em; opacity: 0.9; margin-bottom: 15px; }
        .formula-link {
            display: inline-block; background: linear-gradient(45deg, #ff6b6b, #feca57);
            color: white; text-decoration: none; padding: 8px 16px; border-radius: 20px;
            font-size: 0.9em; transition: all 0.3s ease;
        }
        .formula-link:hover { transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌌 ZUFT统一场论</h1>
            <h2>核心公式交互式可视化</h2>
            <p>探索宇宙的统一本质，理解时空、质量、引力的几何化描述</p>
        </div>
        
        <div class="formula-grid">"""
    
    for formula in FORMULAS:
        folder_name = f"{formula['id']}-{formula['name']}"
        index_content += f"""
            <div class="formula-card">
                <div class="formula-title">{formula['icon']} {formula['name']}</div>
                <div class="formula-description">{formula['description']}</div>
                <a href="{folder_name}/visualization.html" class="formula-link">🚀 启动可视化</a>
            </div>"""
    
    index_content += """
        </div>
    </div>
</body>
</html>"""
    
    with open("utf/统一场论核心公式/index.html", "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print("✅ 已创建主索引页面: index.html")

def main():
    """主函数"""
    print("🚀 开始创建ZUFT统一场论核心公式项目结构...")
    print(f"📊 总共需要创建 {len(FORMULAS)} 个公式的可视化")
    
    # 创建每个公式的文件夹
    for i, formula in enumerate(FORMULAS, 1):
        print(f"\n📁 创建第 {i}/{len(FORMULAS)} 个公式...")
        create_formula_folder(formula)
    
    # 创建主索引页面
    print("\n🏠 创建主索引页面...")
    create_index_html()
    
    print(f"\n🎉 项目结构创建完成！")
    print(f"📂 共创建了 {len(FORMULAS)} 个公式文件夹")
    print("🌐 可以通过 index.html 访问所有可视化")
    print("\n📋 下一步工作：")
    print("1. 完善每个公式的具体可视化实现")
    print("2. 添加详细的理论说明文档")
    print("3. 创建公式间的关联导航")
    print("4. 优化交互体验和视觉效果")

if __name__ == "__main__":
    main()