#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
145_全维度Python审核验证.py
算法联盟 ROOT 最高权限 · 批量审核所有Python脚本
检测: 语法错误 / 导入错误 / 运行时错误 / 逻辑错误
"""
import subprocess
import sys
import os
import glob
import time

# 脚本目录
script_dir = r"d:\a10\aikjx\code\my_lib\utf\大统一场论_算法联盟最高权限\v2"

# 获取所有py文件
py_files = sorted(glob.glob(os.path.join(script_dir, "*.py")))

print("="*90)
print(f"算法联盟 ROOT · 全维度Python脚本审核")
print(f"脚本总数: {len(py_files)}")
print("="*90)

results = {
    "pass": [],
    "fail": [],
    "timeout": [],
}

for i, filepath in enumerate(py_files):
    filename = os.path.basename(filepath)
    # 跳过本脚本
    if "145_" in filename:
        continue

    print(f"\n[{i+1}/{len(py_files)}] 审核: {filename}")

    try:
        # 设置UTF-8编码和60秒超时
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        result = subprocess.run(
            [sys.executable, filename],
            cwd=script_dir,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode == 0:
            # 检查输出中是否有错误标记
            stdout = result.stdout or ""
            stderr = result.stderr or ""
            combined = stdout + stderr

            # 检查常见错误标记
            has_error = any(marker in combined for marker in [
                "Traceback", "Error", "ERROR", "✗", "NameError",
                "TypeError", "ValueError", "AttributeError",
                "ImportError", "ModuleNotFoundError"
            ])

            # 检查输出中的 ✓ 和 ✗ 计数
            pass_count = combined.count("✓")
            fail_count = combined.count("✗")

            if has_error and fail_count > 0:
                # 提取错误行
                error_lines = [l for l in combined.split('\n')
                              if 'Error' in l or 'Traceback' in l or '✗' in l]
                error_summary = error_lines[0][:80] if error_lines else "有错误标记"
                results["fail"].append((filename, error_summary))
                print(f"  ✗ 失败: {error_summary}")
            else:
                results["pass"].append((filename, pass_count))
                print(f"  ✓ 通过 (验证项: {pass_count})")

        else:
            # 非零退出码
            stderr = result.stderr or ""
            # 提取关键错误信息
            error_lines = [l for l in stderr.split('\n') if l.strip()]
            error_summary = error_lines[-1][:80] if error_lines else f"exit code {result.returncode}"
            results["fail"].append((filename, error_summary))
            print(f"  ✗ 失败 (exit {result.returncode}): {error_summary}")

    except subprocess.TimeoutExpired:
        results["timeout"].append((filename, "超时(>60s)"))
        print(f"  ⏱ 超时")
    except Exception as e:
        results["fail"].append((filename, str(e)[:80]))
        print(f"  ✗ 异常: {str(e)[:80]}")

# ===== 汇总报告 =====
print("\n" + "="*90)
print("全维度审核汇总报告")
print("="*90)

total = len(results["pass"]) + len(results["fail"]) + len(results["timeout"])
print(f"\n  总脚本数: {total}")
print(f"  ✓ 通过:   {len(results['pass'])}")
print(f"  ✗ 失败:   {len(results['fail'])}")
print(f"  ⏱ 超时:   {len(results['timeout'])}")
print(f"  通过率:   {len(results['pass'])/total*100:.1f}%")

if results["fail"]:
    print(f"\n  {'─'*80}")
    print(f"  失败脚本清单:")
    print(f"  {'─'*80}")
    for filename, error in results["fail"]:
        print(f"    {filename}")
        print(f"      → {error}")

if results["timeout"]:
    print(f"\n  {'─'*80}")
    print(f"  超时脚本清单:")
    print(f"  {'─'*80}")
    for filename, error in results["timeout"]:
        print(f"    {filename}")
        print(f"      → {error}")

# 通过脚本统计
if results["pass"]:
    total_passes = sum(p[1] for p in results["pass"])
    print(f"\n  {'─'*80}")
    print(f"  通过脚本验证项总计: {total_passes} 个✓")
    print(f"  {'─'*80}")

print(f"\n{'='*90}")
print("算法联盟 ROOT · 全维度Python脚本审核完成")
print("="*90)
