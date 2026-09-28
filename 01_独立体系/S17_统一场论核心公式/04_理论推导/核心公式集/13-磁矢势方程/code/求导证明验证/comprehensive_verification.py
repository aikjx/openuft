#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合验证脚本
运行所有磁矢势方程验证测试并生成详细报告
"""

import subprocess
import sys
import os
import datetime

def run_script(script_name, description):
    """
    运行验证脚本并返回结果
    """
    print(f"\n{'='*60}")
    print(f"运行: {description}")
    print(f"脚本: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(script_name)
        )
        
        if result.returncode == 0:
            print("✓ 执行成功")
            print(result.stdout)
            if result.stderr:
                print("警告信息:")
                print(result.stderr)
            return True, result.stdout, result.stderr
        else:
            print("✗ 执行失败")
            print("错误信息:")
            print(result.stderr)
            return False, result.stdout, result.stderr
    except Exception as e:
        print(f"✗ 执行异常: {str(e)}")
        return False, "", str(e)

def main():
    """
    主验证函数
    """
    print("磁矢势方程综合验证脚本")
    print("=" * 80)
    print(f"执行时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 脚本路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    scripts = [
        {
            'name': os.path.join(base_dir, 'verify_magnetic_potential_equation.py'),
            'description': '磁矢势方程验证'
        },
        {
            'name': os.path.join(base_dir, 'verify_theory_consistency.py'),
            'description': '理论一致性验证'
        },
        {
            'name': os.path.join(base_dir, 'verify_dimension_fix.py'),
            'description': '量纲修复验证'
        },
        {
            'name': os.path.join(base_dir, 'verify_magnetic_potential_equation.py'),
            'description': '磁矢势方程详细验证'
        },
        {
            'name': os.path.join(base_dir, 'verify_astrophysical_magnetic_fields.py'),
            'description': '天体磁场验证'
        }
    ]
    
    # 运行所有脚本
    results = []
    for script in scripts:
        success, stdout, stderr = run_script(script['name'], script['description'])
        results.append({
            'script': script['name'],
            'description': script['description'],
            'success': success,
            'stdout': stdout,
            'stderr': stderr
        })
    
    print("\n" + "=" * 80)
    print("综合验证报告")
    print("=" * 80)
    
    # 统计结果
    total = len(results)
    success_count = sum(1 for r in results if r['success'])
    failure_count = total - success_count
    
    print(f"总验证项: {total}")
    print(f"成功: {success_count}")
    print(f"失败: {failure_count}")
    print()
    
    # 详细结果
    for i, result in enumerate(results, 1):
        status = "✓" if result['success'] else "✗"
        print(f"{i}. {status} {result['description']}")
        if not result['success'] and result['stderr']:
            print(f"   错误: {result['stderr'][:200]}...")
        print()
    
    # 运行主要验证脚本
    print("\n" + "=" * 80)
    print("运行核心验证脚本")
    print("=" * 80)
    
    # 运行主验证脚本
    main_script = os.path.join(base_dir, 'verify_magnetic_potential_equation.py')
    if os.path.exists(main_script):
        success, stdout, stderr = run_script(main_script, '磁矢势方程核心验证')
        results.append({
            'script': main_script,
            'description': '磁矢势方程核心验证',
            'success': success,
            'stdout': stdout,
            'stderr': stderr
        })
    
    # 运行量纲验证
    dimension_script = os.path.join(base_dir, 'verify_dimension_fix.py')
    if os.path.exists(dimension_script):
        success, stdout, stderr = run_script(dimension_script, '量纲一致性验证')
        results.append({
            'script': dimension_script,
            'description': '量纲一致性验证',
            'success': success,
            'stdout': stdout,
            'stderr': stderr
        })
    
    # 生成最终报告
    print("\n" + "=" * 80)
    print("最终验证总结")
    print("=" * 80)
    
    total = len(results)
    success_count = sum(1 for r in results if r['success'])
    failure_count = total - success_count
    
    print(f"验证完成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总验证脚本: {total}")
    print(f"成功执行: {success_count}")
    print(f"执行失败: {failure_count}")
    print()
    
    if success_count == total:
        print("🎉 所有验证脚本执行成功！")
        print("磁矢势方程在多维分析中表现良好，理论框架自洽。")
    else:
        print("⚠️  部分验证脚本执行失败，需要进一步分析。")
    
    print("\n" + "=" * 80)
    print("验证建议")
    print("=" * 80)
    print("1. 检查失败脚本的错误信息，针对性修复问题")
    print("2. 确保所有依赖库已正确安装")
    print("3. 验证物理常数的取值是否正确")
    print("4. 考虑运行特定场景的详细测试，如：")
    print("   - 不同引力场配置的旋度计算")
    print("   - 非球对称引力场的磁场生成")
    print("   - 天体自转对磁场的影响")
    print("5. 与实验数据对比验证理论预测的准确性")

if __name__ == "__main__":
    main()