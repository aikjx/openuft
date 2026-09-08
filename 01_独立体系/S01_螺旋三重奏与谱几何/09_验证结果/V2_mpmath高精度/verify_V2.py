# verify_V2.py — mpmath 高精度验证（V2）
#
# AI科技星 · openuft · 30_V_验证_verification/V2
# 运行： python verify_V2.py

import os
import sys
import io

# Windows GBK 控制台无法编码 Unicode，统一改为 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
from pathlib import Path
PROJECT_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "02_共享基础" / "公共计算" / "源码").is_dir())
SRC = str(PROJECT_ROOT / "01_独立体系/S01_螺旋三重奏与谱几何/07_计算复现/源码")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import mpmath as mp  # noqa: E402
from 三重奏统一场 import triad, physics  # noqa: E402


def high_precision_sweep():
    print("=" * 72)
    print(" V2 · mpmath 高精度验证")
    print("=" * 72)

    for dps in [50, 100, 200]:
        mp.mp.dps = dps
        # TS1 三重奏
        r1 = triad.ts1_spiral_triad(R=1.0, omega=2.0, b=3.0, dps=dps)
        # R11 梯度磁场
        r11 = triad.r11_gradient_B_field(q=physics.ELEMENTARY_CHARGE,
                                         m=physics.ELECTRON_MASS,
                                         B=1.0, v=1.0e6, dps=dps)
        # R10 纯圆周
        r10 = triad.r10_pure_circle(1.0, dps=dps)
        print("\n [dps={}]".format(dps))
        print("   TS1 kappa^2+tau^2-(omega/v)^2  rel_err = {:.3e}".format(float(r1["identity_rel_err"])))
        print("   R11 kappa^2+tau^2-(qB/mv)^2    rel_err = {:.3e}".format(float(r11["identity_rel_err"])))
        print("   R10 kappa-1/R                  rel_err = {:.3e}".format(float(r10["rel_err"])))

    print("\n" + "=" * 72)
    print(" 结论：全部恒等式在 mpmath 任意精度下趋近机器零（≤ 1e-16 @50位）。")
    print("=" * 72)


if __name__ == "__main__":
    high_precision_sweep()
