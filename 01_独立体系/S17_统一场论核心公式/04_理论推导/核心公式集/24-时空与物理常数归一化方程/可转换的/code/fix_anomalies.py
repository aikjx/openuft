#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
归一化方程异常公式修复脚本
自动修复所有异常公式的代数错误和量纲不闭合问题
"""

import os
import re

# 修复规则字典
FIX_RULES = {
    # 公式162: 缺少G²
    r'ω²Gh = h²ν/(r³c²)': 'ω²Gh = G²h²ν/(r³c²)',
    
    # 公式166: 缺少G²
    r'ω²Gν = hν²/(r³c²)': 'ω²Gν = G²hν²/(r³c²)',
    
    # 公式202: 量纲不闭合，删除该公式
    r'ω²GT²/(4π²) = 1': '',
    
    # 公式354: 表达冗余
    r'Gmc² = c⁴r/1': 'Gm = c²r',
    
    # 公式546: 约简错误
    r'φ = ω²r⁴/m · m = ω²r²': 'φ = ω²r³ = Gm = c²r',
    
    # 公式611: 代数错误
    r'ε₀ = e²G/(4πω²r³m²)': 'ε₀ = e²/(4πω²r³m)',
    
    # 公式62: 量子引力无量纲式
    r'G h ν/(c³ r² ω²) = 1': 'ω² r³ c²/(G h ν) = 1',
    
    # 公式67: 普朗克尺度无量纲式
    r'r³ c³/(G h T² ν) = 1/(4π²)': '4π² r³/(l_p² c T² ν) = 1',
    
    # 公式9: 质量表达式
    r'm = \(h³ ν³/(4π² G c⁶ T²)\)^\(1/3\)': 'm = h ν/c² = c² r/G = 4π² r³/(G T²)'
}

def fix_file(file_path):
    """修复文件中的异常公式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 应用修复规则
        original_content = content
        for pattern, replacement in FIX_RULES.items():
            content = re.sub(pattern, replacement, content)
        
        # 移除空行（如果删除了公式）
        content = re.sub(r'\n\s*\n', '\n\n', content)
        
        # 只在内容改变时写入
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ 修复了文件: {file_path}")
            return True
        else:
            print(f"✗ 未发现需要修复的内容: {file_path}")
            return False
    except Exception as e:
        print(f"✗ 修复文件时出错 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("=" * 80)
    print("归一化方程异常公式修复")
    print("=" * 80)
    print()
    
    # 修复目标文件
    # 使用绝对路径确保文件能够正确找到
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.join(script_dir, "..")
    
    # 需要修复的文件列表
    target_files = [
        "空间光速螺旋统一场论：全维度关联·转换·归一化·全验证体系.md",
        "归一化方程转换.md",
        "归一化方程转换2_优化.md",
        "归一化方程转换3.md",
        "归一化方程转换4.md",
        "归一化方程转换5.md",
        "归一化方程转换修正版.md"
    ]
    
    total_fixed = 0
    total_files = len(target_files)
    
    for file_name in target_files:
        target_file = os.path.join(parent_dir, file_name)
        
        if os.path.exists(target_file):
            print(f"开始修复文件: {file_name}")
            fixed = fix_file(target_file)
            if fixed:
                total_fixed += 1
        else:
            print(f"✗ 文件不存在: {file_name}")
        print()
    
    print("=" * 80)
    print("修复完成！")
    print(f"修复了 {total_fixed}/{total_files} 个文件")
    print()
    print("修复的问题:")
    for pattern, replacement in FIX_RULES.items():
        if replacement:
            print(f"  - {pattern} → {replacement}")
        else:
            print(f"  - 删除: {pattern}")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()