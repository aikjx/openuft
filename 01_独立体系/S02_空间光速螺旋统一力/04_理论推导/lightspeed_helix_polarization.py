# -*- coding: utf-8 -*-
"""§12 光速螺旋 · 一般横向偏振态的微分几何与自旋（框架优化）。

背景（§12.10 结论）：τ≠0 分支在自由真空 EM 中无物理对应物——
  草案斜标架的 κ/τ 拆分是标架规范；正规 3D 螺旋 T(z) 的纵向分量是常量直流。
本脚本给出【自由真空中真实存在】的推广，使微分几何工具仍有用：

  一般横向偏振（椭圆偏振）的场方向曲线 = 平面椭圆
      r(z) = (1/K)(a cos Kz, b sin Kz, 0)
  ⇒ 曲线【平面】⇒ Frenet 挠率 τ ≡ 0（严格，非近似）
  ⇒ 曲率 κ(φ) = K·ab/(a²sin²φ + b²cos²φ)^{3/2}  随位置变化
  ⇒ 转动切线定理：∮κ ds = 2π，故 ⟨κ⟩ = 2π/L（L 为椭圆周长）
     圆偏振 a=b=1 时退化为 κ ≡ K（常数），L = 2π/K，⟨κ⟩ = K ✓
  ⇒ 螺旋度 σ = 2ab/(a²+b²)，每光子自旋 SAM = σ ℏ

诚实结论：恒等式 κ²+τ²=K² 仅为【圆偏振】特例；一般偏振下 τ=0 但 κ 非常数，
          κ²+τ² ≠ 常数。正确的推广不变量是 ⟨κ⟩·L = 2π。

ROOT 红线：以上均为标准自由真空 EM + 平面曲线微分几何，不作越界宣称。
"""
import math
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

c = 299792458.0
mu0 = 4e-7 * math.pi
eps0 = 1.0 / (mu0 * c * c)
hbar = 1.054571817e-34


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def conj(v):
    return (x.conjugate() for x in v)


def im(v):
    return (x.imag for x in v)


def norm2(v):
    return sum(abs(x) ** 2 for x in v)


def vmag(v):
    return math.sqrt(sum(x * x for x in v))


def vscale(v, k):
    return tuple(x * k for x in v)


def spin_density(Ec, w):
    """单色场自旋密度 S = (ε0/(2ω)) Im(E* × E)。"""
    Ec = tuple(Ec)
    return vscale(tuple(im(cross(tuple(conj(Ec)), Ec))), eps0 / (2.0 * w))


def energy_density(Ec, Bc):
    return eps0 / 4.0 * norm2(Ec) + 1.0 / (4.0 * mu0) * norm2(Bc)


def curvature_ellipse(a, b, K, phi):
    """椭圆 r(φ)=(1/K)(a cos φ, b sin φ, 0) 的曲率（解析）。"""
    denom = (a * a * math.sin(phi) ** 2 + b * b * math.cos(phi) ** 2) ** 1.5
    return K * a * b / denom


def arc_speed(a, b, phi):
    """|dr/dφ|（含 1/K 因子已约去，用无量纲周长 P 定义）。"""
    return math.sqrt(a * a * math.sin(phi) ** 2 + b * b * math.cos(phi) ** 2)


def simpson(f, lo, hi, n):
    """复合 Simpson 积分（n 为偶数）。"""
    if n % 2:
        n += 1
    h = (hi - lo) / n
    s = f(lo) + f(hi)
    for i in range(1, n):
        s += f(lo + i * h) * (4 if i % 2 else 2)
    return s * h / 3.0


def main():
    lam = 500e-9
    K = 2.0 * math.pi / lam
    w = c * K
    E0 = 1.0
    NPTS = 20000

    print("=" * 78)
    print("§12 一般横向偏振态：微分几何（τ≡0, κ 变分）与自旋 σℏ")
    print("=" * 78)
    print(f"λ={lam:.3e} m, K={K:.6e} m⁻¹, ω={w:.6e} rad/s")
    print("场方向曲线 r(φ) = (1/K)(a cos φ, b sin φ, 0)，φ = Kz")

    # ---------- [A] τ ≡ 0（平面曲线）----------
    print("\n" + "-" * 78)
    print("[A] 挠率 τ：场方向曲线为平面曲线 ⇒ τ ≡ 0（严格）")
    print("-" * 78)
    print("  验证：r', r'', r''' 的 z 分量恒为 0 ⇒ det(r',r'',r''') ≡ 0")
    for a, b in [(1.0, 1.0), (1.0, 0.6), (1.0, 0.2)]:
        maxdet = 0.0
        maxz = 0.0
        for i in range(0, 360, 15):
            phi = math.radians(i)
            rp = (-a * math.sin(phi), b * math.cos(phi), 0.0)
            rpp = (-a * math.cos(phi), -b * math.sin(phi), 0.0)
            rppp = (a * math.sin(phi), -b * math.cos(phi), 0.0)
            det = (rp[0] * (rpp[1] * rppp[2] - rpp[2] * rppp[1])
                   - rp[1] * (rpp[0] * rppp[2] - rpp[2] * rppp[0])
                   + rp[2] * (rpp[0] * rppp[1] - rpp[1] * rppp[0]))
            maxdet = max(maxdet, abs(det))
            maxz = max(maxz, abs(rp[2]), abs(rpp[2]), abs(rppp[2]))
        print(f"    (a,b)=({a:.1f},{b:.1f})  max|z 分量|={maxz:.1e}  max|det|={maxdet:.1e}"
              f"  ⇒ τ = det/|r'×r''|² = 0")
    print("    >>> 自由真空横波的场方向曲线【必为平面】⇒ τ ≡ 0，与 §12.10 一致。")

    # ---------- [B] κ 变分 + ⟨κ⟩·L = 2π ----------
    print("\n" + "-" * 78)
    print("[B] 曲率 κ(φ) 变分与转动切线定理 ∮κ ds = 2π")
    print("-" * 78)
    print(f"    {'a':>5} {'b':>5} {'κ_min/K':>10} {'κ_max/K':>10} "
          f"{'⟨κ⟩/K':>10} {'2π/(KL)':>10} {'∮κds/2π':>10}")
    for a, b in [(1.0, 1.0), (1.0, 0.8), (1.0, 0.6), (1.0, 0.4), (1.0, 0.2)]:
        # 数值：L（无量纲周长 P）与 ∮κ ds
        P = simpson(lambda p: arc_speed(a, b, p), 0.0, 2.0 * math.pi, NPTS)
        Ikappa = simpson(lambda p: curvature_ellipse(a, b, 1.0, p) * arc_speed(a, b, p),
                         0.0, 2.0 * math.pi, NPTS)
        kmin = min(curvature_ellipse(a, b, 1.0, math.radians(i)) for i in range(360))
        kmax = max(curvature_ellipse(a, b, 1.0, math.radians(i)) for i in range(360))
        kavg = Ikappa / P
        print(f"    {a:>5.1f} {b:>5.1f} {kmin:>10.5f} {kmax:>10.5f} "
              f"{kavg:>10.5f} {2*math.pi/P:>10.5f} {Ikappa/(2*math.pi):>10.6f}")
    print("    >>> ⟨κ⟩/K 与 2π/(KL) 完全吻合；∮κds/2π = 1.000000（转动切线定理）✅")
    print("        圆偏振 (a,b)=(1,1)：κ_min=κ_max=K（常数），退化为 κ²+τ²=K² 特例。")

    # ---------- [C] 螺旋度与自旋 ----------
    print("\n" + "-" * 78)
    print("[C] 螺旋度 σ = 2ab/(a²+b²) 与每光子自旋 SAM = σℏ")
    print("-" * 78)
    print(f"    {'a':>5} {'b':>5} {'σ=2ab/(a²+b²)':>16} {'SAM/ℏ(数值)':>14} {'偏振态':>10}")
    for a, b, label in [(1.0, 1.0, "圆偏振"), (1.0, 0.8, "椭圆"), (1.0, 0.6, "椭圆"),
                        (1.0, 0.4, "椭圆"), (1.0, 0.2, "近线偏振"), (1.0, 0.0, "线偏振")]:
        Ec = (a * E0 + 0j, 1j * b * E0, 0j)
        Bc = vscale(cross((0, 0, 1), Ec), 1.0 / c)
        S = spin_density(Ec, w)
        u = energy_density(Ec, Bc)
        sig = 2.0 * a * b / (a * a + b * b) if (a * a + b * b) > 0 else 0.0
        per = vmag(S) / (u / (hbar * w)) / hbar if u > 0 else 0.0
        print(f"    {a:>5.1f} {b:>5.1f} {sig:>16.6f} {per:>14.6f} {label:>10}")
    print("    >>> SAM = σℏ 与数值完全吻合；圆偏振 σ=1，线偏振 σ=0 ✅")

    # ---------- [D] 诚实结论 ----------
    print("\n" + "=" * 78)
    print("框架优化结论（诚实边界）")
    print("=" * 78)
    print("  1. 自由真空横波的场方向曲线【必为平面】⇒ τ ≡ 0；τ≠0 需要纵向结构，")
    print("     属结构光/紧聚焦/倏逝波，超出自由真空（与 §12.6、§12.10 一致）。")
    print("  2. 恒等式 κ²+τ²=K² 仅为【圆偏振】特例（κ 常数 =K）。一般椭圆偏振下")
    print("     τ=0 而 κ(φ) 非常数 ⇒ κ²+τ² 不是常数，原三重奏不变量不普适。")
    print("  3. 正确的推广不变量：⟨κ⟩·L = 2π（转动切线定理），圆偏振退化为 ⟨κ⟩=K。")
    print("  4. 自旋由偏振椭圆度决定：σ = 2ab/(a²+b²)，SAM = σℏ，与 τ 无关。")
    print("  5. 优化收益：以【一般偏振态】替代无物理对应物的 τ 分支后，微分几何")
    print("     工具（κ(s)、⟨κ⟩、周长 L）在真实自由空间光上重新可用。")
    print("=" * 78)


if __name__ == "__main__":
    main()
