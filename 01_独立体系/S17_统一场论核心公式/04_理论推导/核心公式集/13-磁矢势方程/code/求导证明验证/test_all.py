#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论磁矢势方程全面测试脚本

该脚本用于测试所有修复后的脚本，确保它们能正常运行，并生成全面的验证报告。
"""

import subprocess
import sys
import os

# 定义测试函数
def run_test(script_name, description):
    """运行指定的测试脚本并返回结果"""
    print(f"\n{'='*60}")
    print(f"测试: {description}")
    print(f"脚本: {script_name}")
    print(f"{'='*60}")
    
    try:
        # 改进：使用二进制模式运行，避免编码问题
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=False,  # 使用二进制模式
            check=True
        )
        
        # 尝试解码输出，先使用gbk（Windows默认），如果失败再使用utf-8
        try:
            stdout = result.stdout.decode('gbk')
            stderr = result.stderr.decode('gbk') if result.stderr else ''
        except UnicodeDecodeError:
            stdout = result.stdout.decode('utf-8', errors='ignore')
            stderr = result.stderr.decode('utf-8', errors='ignore') if result.stderr else ''
        
        print("✓ 测试通过")
        return True, stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ 测试失败，退出码: {e.returncode}")
        # 解码错误输出
        try:
            stderr = e.stderr.decode('gbk') if e.stderr else ''
        except UnicodeDecodeError:
            stderr = e.stderr.decode('utf-8', errors='ignore') if e.stderr else ''
        if stderr:
            print(f"错误输出: {stderr[:1000]}...")  # 只显示前1000字符
        return False, stderr
    except Exception as e:
        print(f"✗ 测试异常: {str(e)}")
        return False, str(e)

# 主测试函数
def main():
    """运行所有测试"""
    print("统一场论磁矢势方程全面测试")
    print("="*60)
    
    # 获取当前脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 定义测试列表，使用绝对路径
    tests = [
        (os.path.join(script_dir, "verify_magnetic_potential_equation.py"), "主验证脚本"),
        (os.path.join(script_dir, "verify_dimension_fix.py"), "量纲修复脚本"),
        (os.path.join(script_dir, "generate_visualizations.py"), "可视化图表生成脚本")
    ]
    
    # 运行所有测试
    results = []
    for script, desc in tests:
        success, output = run_test(script, desc)
        results.append((desc, success))
    
    # 生成测试报告
    print(f"\n{'='*60}")
    print("测试报告汇总")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for desc, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{desc}: {status}")
    
    print(f"\n总测试数: {total}")
    print(f"通过数: {passed}")
    print(f"失败数: {total - passed}")
    
    if passed == total:
        print(f"\n{'='*60}")
        print("🎉 所有测试通过！")
        print("磁矢势方程求导证明验证脚本已全面修复完成。")
        print(f"{'='*60}")
        return 0
    else:
        print(f"\n{'='*60}")
        print("⚠️  部分测试失败，请检查上述错误信息。")
        print(f"{'='*60}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
