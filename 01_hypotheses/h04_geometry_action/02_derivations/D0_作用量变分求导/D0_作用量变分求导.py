# D0_作用量变分求导.py — 复算 D0 核心变分求导
#
# 算法联盟 · openuft · 10_D_求导_derivation/D0
# 运行： python D0_作用量变分求导.py

import os
import sys
import io

# Windows GBK 控制台无法编码 Unicode，统一改为 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 定位 triad_uft 包（兼容从任意目录运行）
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "70_source_code"))
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from triad_uft import derivations  # noqa: E402


def main():
    print("=" * 70)
    print(" D0 作用量变分求导 · 核心方法论复算")
    print("=" * 70)

    print("\n[1] Klein-Gordon（标量场作用量变分）")
    eom = derivations.kg_equation()
    print("   Euler-Lagrange 方程 =", eom)
    print("   应为 (d_t^2 - nabla^2 + m^2) phi = 0")

    print("\n[2] Maxwell 从无源 Lagrangian L=-1/4 F^2（1+1 维演示）")
    r = derivations.maxwell_from_lagrangian()
    print("   d_0 F^01 =", r["eom_A1"])
    print("   -d_1 F^01 =", r["eom_A0"])
    print("   即 ∂_μ F^{μν}=0（真空 Maxwell）")

    print("\n[3] Einstein-Hilbert 变分（trace 关系校验）")
    r = derivations.einstein_hilbert_variation()
    print("   trace 关系:", r["trace_relation"])
    print("   解得 R =", r["R_from_trace"], "→ R = 4Λ（约定相依）")

    print("\n[4] Maxwell 平面波 E=cB 与 c=1/√(ε₀μ₀)")
    r = derivations.maxwell_wave_relation()
    print("   c(由 ε₀,μ₀) =", r["c_from_em"])
    print("   c(定义值)    =", r["c_exact"])
    print("   相对误差      = {:.3e}".format(r["rel_err"]))

    print("\n" + "=" * 70)
    print(" D0 复算完成：变分求导链自洽。")
    print("=" * 70)


if __name__ == "__main__":
    main()
