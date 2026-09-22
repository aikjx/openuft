# D5_大统一力方程.py — 复算空间光速螺旋统一力框架核心关系
#
# AI科技星 · openuft · 10_D_求导_derivation/D5
# 运行： python D5_大统一力方程.py

import os
import sys
import io

# Windows GBK 控制台无法编码 Unicode，统一改为 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
from pathlib import Path
PROJECT_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "02_共享基础" / "公共计算" / "源码").is_dir())
SRC = str(PROJECT_ROOT / "01_独立体系/S02_空间光速螺旋统一力/07_计算复现/源码")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import helix_force as derivations  # noqa: E402


def main():
    print("=" * 70)
    print(" D5 空间光速螺旋统一力方程· 核心关系复算")
    print("=" * 70)

    for vf in [0.1, 0.3, 0.6, 0.9]:
        r = derivations.helix_unified_force(v_frac=vf)
        print("\n v = {:.2f} c".format(vf))
        print("   力比 F_e/F_m = c/v  = {:.4f}".format(r["force_ratio_c_over_v"]))
        print("   由电磁 c = 1/√(ε₀μ₀) = {:.6e} m/s".format(r["c_from_em"]))
        print("   相对定义值误差          = {:.3e}".format(r["rel_err_c"]))

    print("\n" + "=" * 70)
    print(" 诚实边界：P=m(c-v), dP/dt=F 是几何-运动学力分解，")
    print(" 非实验新预言；统一场论（引力/量子化/暗物质）仍为 OPEN。")
    print("=" * 70)


if __name__ == "__main__":
    main()
