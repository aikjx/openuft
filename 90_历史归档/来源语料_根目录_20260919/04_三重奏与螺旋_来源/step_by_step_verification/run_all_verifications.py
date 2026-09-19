"""
================================================================================
主验证程序 - 运行所有分步验证
================================================================================
"""

import subprocess
import sys
from pathlib import Path

print("=" * 90)
print(" " * 25 + "UNIFIED FIELD THEORY - STEP BY STEP VERIFICATION")
print("=" * 90)

verification_dir = Path(__file__).parent

verification_files = [
    ("STEP 1-2: 螺旋运动公理和引力场方程", "step1_2_spiral_motion.py"),
    ("STEP 3-4: 电磁场定义和质量-电荷关系", "step3_4_em_and_mass_charge.py"),
    ("STEP 5-6: 高斯通量和核心联立方程", "step5_6_gaussian_flux.py"),
    ("STEP 7-8: 代数化简和最终公式", "step7_8_algebraic_simplification.py"),
]

for i, (title, filename) in enumerate(verification_files, 1):
    print(f"\n\n{'='*90}")
    print(f"运行验证: {title}")
    print(f"{'='*90}\n")

    file_path = verification_dir / filename

    if file_path.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(file_path)],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)

            if result.returncode != 0:
                print(f"\n⚠️  警告: {filename} 执行时出现错误 (code: {result.returncode})")

        except Exception as e:
            print(f"✗ 执行失败: {e}")
    else:
        print(f"✗ 文件不存在: {file_path}")

print("\n\n" + "=" * 90)
print("所有分步验证完成！")
print("=" * 90)
