#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML5动画预览生成器
HTML5 Animation Preview Generator

生成HTML5立体角积分动画的预览图和使用说明
Author: Web Visualization Master
Date: 2025-09-16
"""

import os
import webbrowser
from pathlib import Path

def create_preview_page():
    """创建预览页面"""
    
    preview_html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML5几何因子可视化 - 预览与说明</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .demo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 40px;
            margin-bottom: 50px;
        }
        
        .demo-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .demo-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        .demo-card h3 {
            font-size: 1.8em;
            margin-bottom: 15px;
            color: #feca57;
        }
        
        .demo-card p {
            margin-bottom: 20px;
            opacity: 0.9;
        }
        
        .features {
            list-style: none;
            margin: 20px 0;
        }
        
        .features li {
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
        }
        
        .features li:before {
            content: "✨";
            position: absolute;
            left: 0;
        }
        
        .launch-btn {
            display: inline-block;
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            color: white;
            text-decoration: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .launch-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }
        
        .tech-specs {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            padding: 30px;
            margin: 40px 0;
        }
        
        .tech-specs h3 {
            color: #51cf66;
            margin-bottom: 20px;
        }
        
        .spec-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .spec-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #51cf66;
        }
        
        .warning-box {
            background: rgba(255, 107, 107, 0.2);
            border: 2px solid #ff6b6b;
            border-radius: 15px;
            padding: 25px;
            margin: 30px 0;
        }
        
        .warning-box h4 {
            color: #ff6b6b;
            margin-bottom: 15px;
        }
        
        .math-preview {
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            border-radius: 15px;
            padding: 25px;
            margin: 30px 0;
        }
        
        .math-preview h4 {
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }
    </style>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
            }
        };
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌌 HTML5几何因子可视化</h1>
            <p>使用最先进的WebGL技术展示立体角积分与几何因子推导过程</p>
        </div>
        
        <div class="demo-grid">
            <div class="demo-card">
                <h3>🎯 基础版 - 立体角积分动画</h3>
                <p>交互式3D可视化，展示立体角积分的完整推导过程</p>
                <ul class="features">
                    <li>实时3D球对称场可视化</li>
                    <li>交互式积分参数控制</li>
                    <li>数学公式同步高亮</li>
                    <li>鼠标拖拽旋转视角</li>
                    <li>动态场线和投影效果</li>
                </ul>
                <a href="HTML5立体角积分动画.html" class="launch-btn" target="_blank">🚀 启动基础版</a>
            </div>
            
            <div class="demo-card">
                <h3>⚡ 高级版 - WebGL物理模拟</h3>
                <p>高性能WebGL渲染，包含粒子系统和实时物理模拟</p>
                <ul class="features">
                    <li>高性能粒子系统（1000+粒子）</li>
                    <li>实时数值积分计算</li>
                    <li>多层次场强可视化</li>
                    <li>性能监控和统计</li>
                    <li>高级光照和材质效果</li>
                    <li>全屏模式支持</li>
                </ul>
                <a href="WebGL高级几何因子可视化.html" class="launch-btn" target="_blank">⚡ 启动高级版</a>
            </div>
        </div>
        
        <div class="tech-specs">
            <h3>🔧 技术规格</h3>
            <div class="spec-grid">
                <div class="spec-item">
                    <strong>渲染引擎:</strong><br>
                    Three.js + WebGL 2.0
                </div>
                <div class="spec-item">
                    <strong>数学渲染:</strong><br>
                    MathJax 3.0
                </div>
                <div class="spec-item">
                    <strong>性能监控:</strong><br>
                    Stats.js + 自定义指标
                </div>
                <div class="spec-item">
                    <strong>兼容性:</strong><br>
                    现代浏览器 (Chrome 80+, Firefox 75+)
                </div>
                <div class="spec-item">
                    <strong>交互控制:</strong><br>
                    鼠标 + 键盘 + 触摸屏
                </div>
                <div class="spec-item">
                    <strong>响应式设计:</strong><br>
                    支持各种屏幕尺寸
                </div>
            </div>
        </div>
        
        <div class="math-preview">
            <h4>📐 数学推导预览</h4>
            <p>动画展示以下关键数学步骤：</p>
            
            <p><strong>步骤1：</strong> 立体角积分设置</p>
            $$\\int \\sin\\theta \\, d\\Omega = \\int_0^{2\\pi} d\\phi \\int_0^{\\pi} \\sin\\theta (\\sin\\theta \\, d\\theta)$$
            
            <p><strong>步骤2：</strong> 分离变量积分</p>
            $$= 2\\pi \\int_0^{\\pi} \\sin^2\\theta \\, d\\theta$$
            
            <p><strong>步骤3：</strong> 计算结果</p>
            $$= 2\\pi \\cdot \\frac{\\pi}{2} = \\pi^2$$
            
            <p><strong>步骤4：</strong> 几何因子推导</p>
            $$\\text{几何因子} = \\frac{\\pi^2}{2\\pi} \\cdot \\frac{4\\pi}{\\pi^2} = 2$$
        </div>
        
        <div class="warning-box">
            <h4>⚠️ 重要说明</h4>
            <p>这个可视化展示了原文档中的几何因子推导过程，但需要注意：</p>
            <ul>
                <li>积分结果 π² 具有特定的物理量纲和意义</li>
                <li>将其转换为无量纲几何因子2的过程存在概念问题</li>
                <li>标准物理学中的几何因子通常有更严格的理论基础</li>
                <li>建议将此作为教学演示，而非严格的物理推导</li>
            </ul>
        </div>
        
        <div class="tech-specs">
            <h3>🎮 使用说明</h3>
            <div class="spec-grid">
                <div class="spec-item">
                    <strong>鼠标控制:</strong><br>
                    • 拖拽旋转视角<br>
                    • 滚轮缩放<br>
                    • 点击UI控制
                </div>
                <div class="spec-item">
                    <strong>键盘快捷键:</strong><br>
                    • 空格键：播放/暂停<br>
                    • R键：重置<br>
                    • F键：全屏切换
                </div>
                <div class="spec-item">
                    <strong>参数调节:</strong><br>
                    • 积分上限控制<br>
                    • 精度调节<br>
                    • 可视化选项
                </div>
                <div class="spec-item">
                    <strong>实时反馈:</strong><br>
                    • 数值积分结果<br>
                    • 误差分析<br>
                    • 性能监控
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>🌟 使用最新的Web技术创建，为物理教学和研究提供直观的可视化工具</p>
            <p>💡 建议使用Chrome或Firefox浏览器以获得最佳体验</p>
        </div>
    </div>
    
    <script>
        // 等待MathJax加载完成
        window.addEventListener('load', () => {
            setTimeout(() => {
                if (window.MathJax) {
                    MathJax.typesetPromise().then(() => {
                        console.log('数学公式渲染完成');
                    });
                }
            }, 1000);
        });
        
        // 添加一些交互效果
        document.querySelectorAll('.demo-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.background = 'rgba(255, 255, 255, 0.15)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.background = 'rgba(255, 255, 255, 0.1)';
            });
        });
    </script>
</body>
</html>
    """
    
    # 保存预览页面
    preview_path = Path("utf/引力光速统一方程/code/HTML5动画预览.html")
    with open(preview_path, 'w', encoding='utf-8') as f:
        f.write(preview_html)
    
    return preview_path

def create_readme():
    """创建README说明文件"""
    
    readme_content = """# HTML5几何因子可视化项目

## 🌟 项目概述

这是一个使用最先进的HTML5和WebGL技术创建的交互式3D可视化项目，用于展示立体角积分与几何因子推导的完整过程。

## 📁 文件结构

```
utf/引力光速统一方程/code/
├── HTML5立体角积分动画.html          # 基础版交互式动画
├── WebGL高级几何因子可视化.html       # 高级版物理模拟
├── HTML5动画预览.html                # 预览和说明页面
├── HTML5动画预览生成器.py            # 预览页面生成脚本
└── README.md                        # 本说明文件
```

## 🚀 功能特性

### 基础版功能
- ✨ 实时3D球对称场可视化
- 🎮 交互式积分参数控制
- 📐 数学公式同步高亮显示
- 🖱️ 鼠标拖拽旋转视角
- 🌊 动态场线和投影效果
- 📊 积分进度实时监控

### 高级版功能
- ⚡ 高性能粒子系统（1000+粒子）
- 🔢 实时数值积分计算
- 🌈 多层次场强可视化
- 📈 性能监控和统计
- 💎 高级光照和材质效果
- 🖥️ 全屏模式支持
- ⌨️ 键盘快捷键控制

## 🎯 使用方法

### 快速开始
1. 打开 `HTML5动画预览.html` 查看项目概览
2. 选择基础版或高级版启动相应的可视化
3. 使用鼠标拖拽旋转3D视角
4. 调节控制面板中的参数观察效果

### 控制说明
- **鼠标操作**：
  - 拖拽：旋转3D视角
  - 滚轮：缩放视图
  - 点击：UI控制

- **键盘快捷键**：
  - `空格键`：播放/暂停动画
  - `R键`：重置到初始状态
  - `F键`：切换全屏模式

### 参数调节
- **积分控制**：调节θ和φ的积分上限
- **精度设置**：控制数值积分的计算精度
- **可视化选项**：开关各种视觉元素
- **动画参数**：调节旋转速度和场强显示

## 📐 数学原理

项目可视化展示以下数学推导过程：

1. **立体角积分设置**：
   ∫ sin θ dΩ = ∫₀²π dφ ∫₀π sin θ (sin θ dθ)

2. **分离变量积分**：
   = 2π ∫₀π sin²θ dθ

3. **积分计算**：
   = 2π · π/2 = π²

4. **几何因子推导**：
   几何因子 = (π²/2π) · (4π/π²) = 2

## ⚠️ 重要说明

这个可视化展示了原文档中的几何因子推导过程，但需要注意：

- 积分结果 π² 具有特定的物理量纲和意义
- 将其转换为无量纲几何因子2的过程存在概念问题
- 标准物理学中的几何因子通常有更严格的理论基础
- 建议将此作为教学演示，而非严格的物理推导

## 🔧 技术规格

- **渲染引擎**：Three.js + WebGL 2.0
- **数学渲染**：MathJax 3.0
- **性能监控**：Stats.js + 自定义指标
- **兼容性**：现代浏览器 (Chrome 80+, Firefox 75+)
- **响应式设计**：支持各种屏幕尺寸

## 🌐 浏览器兼容性

| 浏览器 | 最低版本 | 推荐版本 | 状态 |
|--------|----------|----------|------|
| Chrome | 80+ | 90+ | ✅ 完全支持 |
| Firefox | 75+ | 85+ | ✅ 完全支持 |
| Safari | 13+ | 14+ | ⚠️ 部分功能 |
| Edge | 80+ | 90+ | ✅ 完全支持 |

## 🎨 自定义和扩展

项目采用模块化设计，可以轻松扩展：

- 添加新的可视化效果
- 修改数学公式和推导步骤
- 调整UI界面和交互方式
- 集成其他物理模拟

## 📝 更新日志

### v1.0.0 (2025-09-16)
- ✨ 初始版本发布
- 🎯 基础版交互式动画
- ⚡ 高级版WebGL物理模拟
- 📐 完整的数学推导可视化
- 🎮 丰富的交互控制功能

## 🤝 贡献指南

欢迎提交问题报告和功能建议！

## 📄 许可证

本项目仅用于教育和研究目的。

## 🙏 致谢

感谢以下开源项目的支持：
- Three.js - 3D图形库
- MathJax - 数学公式渲染
- Stats.js - 性能监控

---

💡 **提示**：建议使用Chrome或Firefox浏览器以获得最佳体验！
"""
    
    readme_path = Path("utf/引力光速统一方程/code/README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    return readme_path

def main():
    """主函数"""
    print("🚀 正在生成HTML5动画预览和说明文档...")
    
    # 创建预览页面
    preview_path = create_preview_page()
    print(f"✅ 预览页面已生成: {preview_path}")
    
    # 创建README
    readme_path = create_readme()
    print(f"✅ README文档已生成: {readme_path}")
    
    print("\n🌟 HTML5几何因子可视化项目已完成！")
    print("\n📁 生成的文件：")
    print(f"   • {preview_path}")
    print(f"   • {readme_path}")
    print("   • HTML5立体角积分动画.html")
    print("   • WebGL高级几何因子可视化.html")
    
    print("\n🎯 使用说明：")
    print("1. 打开 HTML5动画预览.html 查看项目概览")
    print("2. 选择基础版或高级版启动相应的可视化")
    print("3. 使用鼠标和键盘进行交互控制")
    
    print("\n💡 技术特点：")
    print("• 使用Three.js + WebGL 2.0进行高性能3D渲染")
    print("• MathJax 3.0实现数学公式的完美显示")
    print("• 实时粒子系统和物理模拟")
    print("• 响应式设计，支持各种设备")
    print("• 丰富的交互控制和参数调节")
    
    # 询问是否打开预览
    try:
        open_preview = input("\n🌐 是否在浏览器中打开预览页面？(y/n): ").lower().strip()
        if open_preview == 'y':
            webbrowser.open(str(preview_path.absolute()))
            print("🚀 预览页面已在浏览器中打开！")
    except KeyboardInterrupt:
        print("\n👋 再见！")

if __name__ == "__main__":
    main()