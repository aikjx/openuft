#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节优化脚本
用于统一场论书籍的批量优化
"""

import os
import re
from pathlib import Path

class ChapterOptimizer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.formulas = {
            # 公式1：时空同一化方程
            'time_space': r'\vec{r}(t) = \vec{c}t',
            # 公式2：三维螺旋时空方程
            'spiral_3d': r'\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}',
            # 公式3：质量定义方程
            'mass_def': r'm = k \dfrac{dn}{d\Omega}',
            # 公式4：引力场定义方程
            'gravity_field': r'\vec{A} = -Gk\dfrac{\Delta n}{\Delta s}\dfrac{\vec{r}}{r}',
            # 公式5：静止动量方程
            'static_momentum': r'\vec{p}_{0} = m_{0}\vec{c}_{0}',
            # 公式6：运动动量方程
            'dynamic_momentum': r'\vec{P} = m(\vec{c} - \vec{v})',
            # 公式7：宇宙大统一方程
            'unified_force': r'\vec{F} = \dfrac{d\vec{P}}{dt} = \vec{c}\dfrac{dm}{dt} - \vec{v}\dfrac{dm}{dt} + m\dfrac{d\vec{c}}{dt} - m\dfrac{d\vec{v}}{dt}',
            # 公式9：电荷定义方程
            'charge_def': r'q = k^{\prime}k\dfrac{1}{\Omega^{2}}\dfrac{d\Omega}{dt}',
            # 公式10：电场定义方程
            'electric_field': r'\vec{E} = -\dfrac{kk^{\prime}}{4\pi\varepsilon_0\Omega^2}\dfrac{d\Omega}{dt}\dfrac{\vec{r}}{r^3}',
            # 公式11：磁场定义方程
            'magnetic_field': r'\vec{B} = \dfrac{\mu_{0} \gamma k k^{\prime}}{4 \pi \Omega^{2}} \dfrac{d \Omega}{d t} \dfrac{[(x-v t) \vec{i}+y \vec{j}+z \vec{k}]}{\left[\gamma^{2}(x-v t)^{2}+y^{2}+z^{2}\right]^{3/2}}',
            # 公式16：能量方程
            'energy': r'E = m_0 c^2 = mc^2\sqrt{1 - \dfrac{v^2}{c^2}}',
            # 公式18：核力场定义方程
            'nuclear_field': r'\vec{D} = - G m \dfrac{ \vec{c} - 3 \dfrac{\vec{r}}{r} \dot{r} }{r^3}',
            # 公式19：引力光速统一方程
            'gravity_light': r'Z = \dfrac{Gc}{2}',
        }
        
        self.dimensions = {
            'force': '[MLT⁻²]',
            'energy': '[ML²T⁻²]',
            'momentum': '[MLT⁻¹]',
            'mass': '[M]',
            'length': '[L]',
            'time': '[T]',
            'charge': '[Q]',
            'acceleration': '[LT⁻²]',
            'field': '[LT⁻²]',
        }
    
    def optimize_formula(self, formula_text, dimension=None):
        """优化单个公式"""
        result = f'$${formula_text}$$'
        if dimension:
            result += f'\n\n其中量纲为：{dimension}'
        return result
    
    def add_formula_with_dimension(self, content, marker, formula, dimension, label):
        """添加带量纲的公式"""
        formula_block = f'\n\n{label}\n\n$$ {formula} $$\n\n量纲：{dimension}\n\n'
        return content.replace(marker, marker + formula_block)
    
    def format_existing_formula(self, content):
        """格式化现有公式"""
        # 替换纯文本公式为LaTeX格式
        patterns = [
            (r'F = G × (m₁ × m₂) / r²', r'$$F = \dfrac{G m_1 m_2}{r^2}$$'),
            (r'F = G \* (m1 \* m2) / r\^2', r'$$F = \dfrac{G m_1 m_2}{r^2}$$'),
            (r'E = mc\^2', r'$$E = mc^2$$'),
            (r'p = mv', r'$$p = mv$$'),
            (r'F = ma', r'$$F = ma$$'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def optimize_chapter(self, chapter_file, required_formulas=None):
        """优化单个章节"""
        print(f'正在优化：{chapter_file.name}')
        
        try:
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 格式化现有公式
            content = self.format_existing_formula(content)
            
            # 如果需要添加特定公式
            if required_formulas:
                for formula_name, formula_key, dimension, label in required_formulas:
                    if formula_key in self.formulas:
                        content = self.add_formula_with_dimension(
                            content,
                            label,
                            self.formulas[formula_key],
                            dimension,
                            f'**{label}**'
                        )
            
            # 写回文件
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f'✅ {chapter_file.name} 优化完成')
            return True
        except Exception as e:
            print(f'❌ {chapter_file.name} 优化失败：{str(e)}')
            return False

def main():
    base_path = r'D:\a10\aikjx\code\my_lib\utf\12-书籍\人人都能理解统一场论\V1'
    optimizer = ChapterOptimizer(base_path)
    
    # 定义需要优化的章节和所需公式
    chapters_to_optimize = {
        '第2章：空间的本质.md': [
            ('时空同一化方程', 'time_space', '[L]', '时空同一化方程'),
            ('三维螺旋时空方程', 'spiral_3d', '[L]', '三维螺旋时空方程'),
        ],
        '第11章：质量的本质.md': [
            ('质量定义方程', 'mass_def', '[M]', '质量定义方程'),
            ('静止动量方程', 'static_momentum', '[MLT⁻¹]', '静止动量方程'),
            ('运动动量方程', 'dynamic_momentum', '[MLT⁻¹]', '运动动量方程'),
            ('能量方程', 'energy', '[ML²T⁻²]', '能量方程'),
        ],
        '第12章：力的本质.md': [
            ('宇宙大统一方程', 'unified_force', '[MLT⁻²]', '宇宙大统一方程'),
            ('引力场定义方程', 'gravity_field', '[LT⁻²]', '引力场定义方程'),
            ('核力场定义方程', 'nuclear_field', '[LT⁻²]', '核力场定义方程'),
        ],
        '第13章：场的概念.md': [
            ('电荷定义方程', 'charge_def', '[Q]', '电荷定义方程'),
            ('电场定义方程', 'electric_field', '[MLT⁻³Q⁻¹]', '电场定义方程'),
            ('磁场定义方程', 'magnetic_field', '[MT⁻¹Q⁻¹]', '磁场定义方程'),
        ],
    }
    
    print('=== 开始批量优化 ===\n')
    
    success_count = 0
    fail_count = 0
    
    for chapter_name, formulas in chapters_to_optimize.items():
        chapter_file = Path(base_path) / chapter_name
        if chapter_file.exists():
            if optimizer.optimize_chapter(chapter_file, formulas):
                success_count += 1
            else:
                fail_count += 1
        else:
            print(f'⚠️ 文件不存在：{chapter_name}')
            fail_count += 1
    
    print(f'\n=== 优化完成 ===')
    print(f'成功：{success_count} 章')
    print(f'失败：{fail_count} 章')

if __name__ == '__main__':
    main()
