#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论可视化生成器
Unified Field Theory Visualization Generator

基于公式规格数据库生成统一场论公式的可视化页面
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class FormulaSpec:
    """公式规格定义"""
    id: str
    name: str
    formula_latex: str
    formula_unicode: str
    description: str
    icon: str
    category: str
    difficulty: int  # 1-5
    physics_concepts: List[str]
    math_concepts: List[str]
    visualization_type: str
    parameters: List[Dict[str, Any]]
    dependencies: List[str]
    applications: List[str]

class AdvancedVisualizationGenerator:
    """先进可视化生成器"""
    
    def __init__(self, formula_db_path: str):
        """初始化可视化生成器
        
        Args:
            formula_db_path: 公式规格数据库路径
        """
        self.formula_db = self._load_formula_db(formula_db_path)
        self.templates = self._load_templates()
        self.standards = self._load_standards()
        self.formulas = [FormulaSpec(**f) for f in self.formula_db['formulas']]
    
    def _load_formula_db(self, formula_db_path: str) -> Dict[str, Any]:
        """加载公式规格数据库
        
        Args:
            formula_db_path: 公式规格数据库路径
            
        Returns:
            公式规格数据库
        """
        with open(formula_db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_templates(self) -> Dict[str, str]:
        """加载可视化模板
        
        Returns:
            可视化模板字典
        """
        return {
            "base": "",  # 基础模板，后续填充
            "spacetime": self._get_spacetime_template(),
            "field": self._get_field_template(), 
            "particle": self._get_particle_template(),
            "wave": self._get_wave_template(),
            "energy": self._get_energy_template()
        }
    
    def _load_standards(self) -> Dict[str, Any]:
        """加载规范标准
        
        Returns:
            规范标准字典
        """
        return {
            "colors": {
                "spacetime": "#667eea",
                "mass": "#ff6b6b",
                "field": "#4ecdc4",
                "energy": "#feca57",
                "particle": "#ff9ff3"
            },
            "physics_units": {
                "length": "m",
                "time": "s", 
                "mass": "kg",
                "charge": "C",
                "field": "N/C"
            },
            "math_precision": 6,
            "animation_fps": 60
        }
    
    def _get_spacetime_template(self) -> str:
        """获取时空类可视化模板
        
        Returns:
            时空类可视化模板
        """
        return """<!-- 时空类可视化模板 -->
<div class="formula-card spacetime">
    <h3>{icon} {name}</h3>
    <div class="formula">
        <span class="latex">{formula_latex}</span>
        <span class="unicode">{formula_unicode}</span>
    </div>
    <p class="description">{description}</p>
    <div class="visualization">
        <!-- 时空可视化内容 -->
        <div class="3d-visualization" data-type="{visualization_type}" data-id="{id}"></div>
    </div>
    <div class="concepts">
        <h4>物理概念</h4>
        <ul class="physics-concepts">
            {physics_concepts}
        </ul>
        <h4>数学概念</h4>
        <ul class="math-concepts">
            {math_concepts}
        </ul>
    </div>
    <div class="applications">
        <h4>应用领域</h4>
        <ul>
            {applications}
        </ul>
    </div>
</div>"""
    
    def _get_field_template(self) -> str:
        """获取场类可视化模板
        
        Returns:
            场类可视化模板
        """
        return """<!-- 场类可视化模板 -->
<div class="formula-card field">
    <h3>{icon} {name}</h3>
    <div class="formula">
        <span class="latex">{formula_latex}</span>
        <span class="unicode">{formula_unicode}</span>
    </div>
    <p class="description">{description}</p>
    <div class="visualization">
        <!-- 场可视化内容 -->
        <div class="field-visualization" data-type="{visualization_type}" data-id="{id}"></div>
    </div>
    <div class="concepts">
        <h4>物理概念</h4>
        <ul class="physics-concepts">
            {physics_concepts}
        </ul>
        <h4>数学概念</h4>
        <ul class="math-concepts">
            {math_concepts}
        </ul>
    </div>
    <div class="applications">
        <h4>应用领域</h4>
        <ul>
            {applications}
        </ul>
    </div>
</div>"""
    
    def _get_particle_template(self) -> str:
        """获取粒子类可视化模板
        
        Returns:
            粒子类可视化模板
        """
        return """<!-- 粒子类可视化模板 -->
<div class="formula-card particle">
    <h3>{icon} {name}</h3>
    <div class="formula">
        <span class="latex">{formula_latex}</span>
        <span class="unicode">{formula_unicode}</span>
    </div>
    <p class="description">{description}</p>
    <div class="visualization">
        <!-- 粒子可视化内容 -->
        <div class="particle-visualization" data-type="{visualization_type}" data-id="{id}"></div>
    </div>
    <div class="concepts">
        <h4>物理概念</h4>
        <ul class="physics-concepts">
            {physics_concepts}
        </ul>
        <h4>数学概念</h4>
        <ul class="math-concepts">
            {math_concepts}
        </ul>
    </div>
    <div class="applications">
        <h4>应用领域</h4>
        <ul>
            {applications}
        </ul>
    </div>
</div>"""
    
    def _get_wave_template(self) -> str:
        """获取波动类可视化模板
        
        Returns:
            波动类可视化模板
        """
        return """<!-- 波动类可视化模板 -->
<div class="formula-card wave">
    <h3>{icon} {name}</h3>
    <div class="formula">
        <span class="latex">{formula_latex}</span>
        <span class="unicode">{formula_unicode}</span>
    </div>
    <p class="description">{description}</p>
    <div class="visualization">
        <!-- 波动可视化内容 -->
        <div class="wave-visualization" data-type="{visualization_type}" data-id="{id}"></div>
    </div>
    <div class="concepts">
        <h4>物理概念</h4>
        <ul class="physics-concepts">
            {physics_concepts}
        </ul>
        <h4>数学概念</h4>
        <ul class="math-concepts">
            {math_concepts}
        </ul>
    </div>
    <div class="applications">
        <h4>应用领域</h4>
        <ul>
            {applications}
        </ul>
    </div>
</div>"""
    
    def _get_energy_template(self) -> str:
        """获取能量类可视化模板
        
        Returns:
            能量类可视化模板
        """
        return """<!-- 能量类可视化模板 -->
<div class="formula-card energy">
    <h3>{icon} {name}</h3>
    <div class="formula">
        <span class="latex">{formula_latex}</span>
        <span class="unicode">{formula_unicode}</span>
    </div>
    <p class="description">{description}</p>
    <div class="visualization">
        <!-- 能量可视化内容 -->
        <div class="energy-visualization" data-type="{visualization_type}" data-id="{id}"></div>
    </div>
    <div class="concepts">
        <h4>物理概念</h4>
        <ul class="physics-concepts">
            {physics_concepts}
        </ul>
        <h4>数学概念</h4>
        <ul class="math-concepts">
            {math_concepts}
        </ul>
    </div>
    <div class="applications">
        <h4>应用领域</h4>
        <ul>
            {applications}
        </ul>
    </div>
</div>"""
    
    def generate_visualization(self, output_path: str = "visualization.html") -> None:
        """生成可视化页面
        
        Args:
            output_path: 输出文件路径
        """
        # 生成HTML内容
        html_content = self._generate_html()
        
        # 保存到文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 可视化页面已生成: {output_path}")
    
    def _generate_html(self) -> str:
        """生成HTML内容
        
        Returns:
            HTML内容
        """
        # 生成公式卡片
        formula_cards = []
        for formula in self.formulas:
            template = self.templates.get(formula.category, self.templates['spacetime'])
            
            # 格式化物理概念
            physics_concepts = "".join([f"<li>{concept}</li>" for concept in formula.physics_concepts])
            
            # 格式化数学概念
            math_concepts = "".join([f"<li>{concept}</li>" for concept in formula.math_concepts])
            
            # 格式化应用领域
            applications = "".join([f"<li>{app}</li>" for app in formula.applications])
            
            # 填充模板
            card = template.format(
                id=formula.id,
                name=formula.name,
                icon=formula.icon,
                formula_latex=formula.formula_latex,
                formula_unicode=formula.formula_unicode,
                description=formula.description,
                visualization_type=formula.visualization_type,
                physics_concepts=physics_concepts,
                math_concepts=math_concepts,
                applications=applications
            )
            
            formula_cards.append(card)
        
        # 生成完整HTML
        html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>统一场论核心公式可视化</title>
    <!-- KaTeX支持 -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/contrib/auto-render.min.js"></script>
    <!-- Three.js支持 -->
    <script src="https://cdn.jsdelivr.net/npm/three@0.154.0/build/three.min.js"></script>
    <style>
        /* 基础样式 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        h1 {
            text-align: center;
            color: white;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        /* 公式卡片样式 */
        .formula-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }

        .formula-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .formula-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        }

        /* 分类颜色 */
        .formula-card.spacetime {
            border-left: 5px solid #667eea;
        }

        .formula-card.field {
            border-left: 5px solid #4ecdc4;
        }

        .formula-card.particle {
            border-left: 5px solid #ff9ff3;
        }

        .formula-card.wave {
            border-left: 5px solid #feca57;
        }

        .formula-card.energy {
            border-left: 5px solid #ff6b6b;
        }

        .formula-card h3 {
            margin-bottom: 15px;
            color: #333;
            font-size: 1.3em;
        }

        .formula {
            margin-bottom: 15px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
        }

        .formula .latex {
            display: block;
            font-size: 1.2em;
            margin-bottom: 5px;
        }

        .formula .unicode {
            display: block;
            font-size: 1.1em;
            color: #666;
        }

        .description {
            margin-bottom: 15px;
            color: #666;
            line-height: 1.5;
        }

        .visualization {
            height: 200px;
            background: #f0f0f0;
            border-radius: 8px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
            font-style: italic;
        }

        .3d-visualization,
        .field-visualization,
        .particle-visualization,
        .wave-visualization,
        .energy-visualization {
            width: 100%;
            height: 100%;
        }

        .concepts {
            margin-bottom: 15px;
        }

        .concepts h4 {
            margin-bottom: 10px;
            color: #555;
            font-size: 1em;
        }

        .concepts ul {
            list-style-type: disc;
            margin-left: 20px;
            color: #666;
        }

        .concepts li {
            margin-bottom: 5px;
        }

        .applications {
            margin-top: 15px;
        }

        .applications h4 {
            margin-bottom: 10px;
            color: #555;
            font-size: 1em;
        }

        .applications ul {
            list-style-type: circle;
            margin-left: 20px;
            color: #666;
        }

        .applications li {
            margin-bottom: 5px;
        }

        /* 响应式设计 */
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }

            h1 {
                font-size: 2em;
            }

            .formula-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>统一场论核心公式可视化</h1>

        <div class="formula-grid">
            __FORMULA_CARDS__
        </div>
    </div>

    <script>
        // 渲染KaTeX公式
        document.addEventListener("DOMContentLoaded", function() {
            renderMathInElement(document.body, {
                delimiters: [
                    {left: "$", right: "$", display: false},
                    {left: "$$", right: "$$", display: true}
                ]
            });

            // 初始化可视化
            initVisualizations();
        });

        function initVisualizations() {
            // 初始化3D可视化
            const visualizationElements = document.querySelectorAll('[data-type]');
            visualizationElements.forEach(element => {
                const type = element.dataset.type;
                const id = element.dataset.id;

                // 根据类型初始化不同的可视化
                switch(type) {
                    case '3d_vector_field':
                        init3DVectorField(element, id);
                        break;
                    case '3d_helix_trajectory':
                        init3DHelixTrajectory(element, id);
                        break;
                    case 'solid_angle_density':
                        initSolidAngleDensity(element, id);
                        break;
                    case 'gravity_field_lines':
                        initGravityFieldLines(element, id);
                        break;
                    case 'electric_field_lines':
                        initElectricFieldLines(element, id);
                        break;
                    case 'magnetic_field_lines':
                        initMagneticFieldLines(element, id);
                        break;
                    case 'wave_visualization':
                        initWaveVisualization(element, id);
                        break;
                    case 'energy_visualization':
                        initEnergyVisualization(element, id);
                        break;
                    default:
                        element.innerHTML = '<p>可视化类型未实现: ' + type + '</p>';
                }
            });
        }

        function init3DVectorField(element, id) {
            element.innerHTML = '<p>3D矢量场可视化 - 公式ID: ' + id + '</p>';
        }

        function init3DHelixTrajectory(element, id) {
            element.innerHTML = '<p>3D螺旋轨迹可视化 - 公式ID: ' + id + '</p>';
        }

        function initSolidAngleDensity(element, id) {
            element.innerHTML = '<p>立体角密度可视化 - 公式ID: ' + id + '</p>';
        }

        function initGravityFieldLines(element, id) {
            element.innerHTML = '<p>引力场线可视化 - 公式ID: ' + id + '</p>';
        }

        function initElectricFieldLines(element, id) {
            element.innerHTML = '<p>电场线可视化 - 公式ID: ' + id + '</p>';
        }

        function initMagneticFieldLines(element, id) {
            element.innerHTML = '<p>磁场线可视化 - 公式ID: ' + id + '</p>';
        }

        function initWaveVisualization(element, id) {
            element.innerHTML = '<p>波动可视化 - 公式ID: ' + id + '</p>';
        }

        function initEnergyVisualization(element, id) {
            element.innerHTML = '<p>能量可视化 - 公式ID: ' + id + '</p>';
        }
    </script>
</body>
</html>'''
        
        return html_template.replace("__FORMULA_CARDS__", "".join(formula_cards))

# 主函数
if __name__ == "__main__":
    # 获取当前目录下的公式规格数据库路径
    formula_db_path = os.path.join(os.path.dirname(__file__), "公式规格数据库.json")
    
    # 创建可视化生成器
    generator = AdvancedVisualizationGenerator(formula_db_path)
    
    # 生成可视化页面
    generator.generate_visualization("统一场论核心公式可视化.html")