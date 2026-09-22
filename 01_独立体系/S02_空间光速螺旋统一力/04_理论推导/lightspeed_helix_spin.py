# -*- coding: utf-8 -*-
"""§12 光速螺旋 · 光子自旋角动量（SAM）与 τ 的规范性质分析。

分三部分（严格边界，遵循 ROOT 红线：不粉饰、不外推）：

[A] 圆偏振（θ=0，标准自由真空 EM）自旋角动量：严格
    SAM 密度  S = (ε0/(2ω)) Im(E* × E)，能量密度 <u>
    每光子自旋 SAM_per_photon = |S| / N ，N = <u>/(ℏω)  → 应得 ℏ（螺旋度 σ=±1）

[B] 一般横向椭圆偏振：螺旋度 σ = 2 Im(E_x* E_y)/(|E_x|²+|E_y|²) ∈ [-1,1]
    圆偏振 σ=±1（自旋最大），线偏振 σ=0（无自旋）；SAM = σ ℏ/光子

[C] §12 斜场标架 (e1,e2,e3) 的规范分析：关键诚实结论
    显式标架：
      e1(s) = (cos Ks, sin Ks, 0)
      e2(s) = (-sin Ks cosθ, cos Ks cosθ, sinθ)
      e3(s) = (-sin Ks sinθ, cos Ks sinθ, -cosθ)
    数值检验：
      (1) 正交归一；
      (2) 实际导数结构 de1/ds=κe2+τe3, de2/ds=-κe1, de3/ds=-τe1
          （注意：并非 §12 声称的三对角 Frenet-Serret 形式）；
      (3) 该标架是左手系（e1×e2 = -e3），Darboux 向量 ω_D = τ e2 - κ e3；
      (4) 【核心】e1 与 θ 无关 → (e2,e3) 仅是绕 e1 旋转 θ 角的辅助标架；
          因此 κ=Kcosθ、τ=Ksinθ 的拆分是【规范/标架选择】，非物理可观测量；
          不变量只有 |ω_D| = K（且 ω_D ≡ K ẑ 与 θ 无关）与 κ²+τ² = K²。

结论：自由真空情形下 τ 与自旋无对应关系（物理场 e1 恒为圆偏振，SAM=σℏ 与 θ 无关）；
      τ 要成为物理量必须让场带上纵向分量（结构光/紧聚焦/近场），超出自由真空 EM。
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


# ---------- 复数向量工具 ----------
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def conj(v):
    return (v[0].conjugate(), v[1].conjugate(), v[2].conjugate())


def im(v):
    return (v[0].imag, v[1].imag, v[2].imag)


def norm2(v):
    return sum(abs(x) ** 2 for x in v)


def dot(a, b):
    return sum(a[i] * b[i] for i in range(3))


def vmag(v):
    return math.sqrt(sum(x * x for x in v))


def vsub(a, b):
    return tuple(a[i] - b[i] for i in range(3))


def vscale(a, k):
    return tuple(x * k for x in a)


def spin_density(Ec, w):
    """单色场规范无关自旋角动量密度 S = (ε0/(2ω)) Im(E* × E)。"""
    return vscale(im(cross(conj(Ec), Ec)), eps0 / (2.0 * w))


def energy_density(Ec, Bc):
    """时间平均能量密度 <u> = (ε0/4)|Ec|² + (1/(4μ0))|Bc|²。"""
    return eps0 / 4.0 * norm2(Ec) + 1.0 / (4.0 * mu0) * norm2(Bc)


def helicity(Ec):
    """横向场螺旋度 σ = 2 Im(E_x* E_y)/(|E_x|²+|E_y|²) ∈ [-1,1]。"""
    denom = abs(Ec[0]) ** 2 + abs(Ec[1]) ** 2
    if denom == 0:
        return 0.0
    return 2.0 * (Ec[0].conjugate() * Ec[1]).imag / denom


# ---------- §12 斜场标架 ----------
def frame(u, theta):
    """u = K s（无量纲），返回 (e1,e2,e3)。"""
    ct, st = math.cos(theta), math.sin(theta)
    cu, su = math.cos(u), math.sin(u)
    e1 = (cu, su, 0.0)
    e2 = (-su * ct, cu * ct, st)
    e3 = (-su * st, cu * st, -ct)
    return e1, e2, e3


def main():
    lam = 500e-9
    K = 2.0 * math.pi / lam
    w = c * K
    E0 = 1.0

    print("=" * 78)
    print("§12 光子自旋角动量（SAM）与 τ 的规范性质")
    print("=" * 78)
    print(f"λ={lam:.3e} m, K={K:.6e} m⁻¹, ω={w:.6e} rad/s")

    # ================= [A] 圆偏振 SAM =================
    print("\n" + "-" * 78)
    print("[A] 圆偏振（θ=0，标准自由真空 EM）：每光子自旋")
    print("-" * 78)
    Ec = (E0 + 0j, 1j * E0, 0j)                      # E ∝ x̂ + i ŷ
    Bc = vscale(cross((0, 0, 1), Ec), 1.0 / c)       # B = ẑ × E / c
    S = spin_density(Ec, w)
    u = energy_density(Ec, Bc)
    N = u / (hbar * w)                                # 光子数密度
    sam_per_photon = vmag(S) / N
    print(f"  自旋密度 S = ({S[0]:.4e}, {S[1]:.4e}, {S[2]:.6e})  → 纯轴向 ẑ")
    print(f"  能量密度 <u> = {u:.6e}")
    print(f"  光子数密度 N = <u>/(ℏω) = {N:.6e} m⁻³")
    print(f"  每光子自旋 |S|/N = {sam_per_photon:.6e} J·s"
          f"  = {sam_per_photon/hbar:.6f} ℏ")
    print(f"  自旋/能量比 |S|/<u> = {vmag(S)/u:.6e}  (理论 1/ω = {1/w:.6e})")
    print(f"  >>> 圆偏振每光子自旋 = ℏ（螺旋度 σ=+1），严格成立 ✅")

    # ================= [B] 一般椭圆偏振 =================
    print("\n" + "-" * 78)
    print("[B] 一般横向椭圆偏振：螺旋度 σ 与自旋 σℏ")
    print("-" * 78)
    print(f"  {'χ':>8}  {'偏振态':<10} {'σ=sin2χ':>10} {'σ(数值)':>10} {'自旋/ℏ':>10}")
    for chi_deg, label in [(0, "线偏振"), (15, "椭圆"), (30, "椭圆"),
                           (45, "圆偏振"), (60, "椭圆"), (90, "线偏振")]:
        chi = math.radians(chi_deg)
        Ec2 = (E0 * math.cos(chi) + 0j, 1j * E0 * math.sin(chi), 0j)
        Bc2 = vscale(cross((0, 0, 1), Ec2), 1.0 / c)
        S2 = spin_density(Ec2, w)
        u2 = energy_density(Ec2, Bc2)
        sig = helicity(Ec2)
        per = vmag(S2) / (u2 / (hbar * w)) / hbar
        print(f"  {chi_deg:>6}°  {label:<10} {math.sin(2*chi):>10.4f} "
              f"{sig:>10.4f} {per:>10.4f}")
    print("  >>> σ ∈ [-1,1]；圆偏振 σ=±1（自旋最大 ℏ），线偏振 σ=0（无自旋）✅")

    # ================= [C] §12 斜场标架规范分析 =================
    print("\n" + "-" * 78)
    print("[C] §12 斜场标架规范分析（κ=Kcosθ, τ=Ksinθ 是否为物理量？）")
    print("-" * 78)
    thetas = [0.0, math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2]
    h = 1e-6
    u0 = 0.37  # 无量纲采样点 K s

    print(f"\n  (1) 正交归一性与手性")
    for th in thetas:
        e1, e2, e3 = frame(u0, th)
        o12 = dot(e1, e2); o13 = dot(e1, e3); o23 = dot(e2, e3)
        n1 = vmag(e1); n2 = vmag(e2); n3 = vmag(e3)
        cr = cross(e1, e2)
        handed = "左手系(e1×e2=-e3)" if vmag(vsub(cr, e3)) > vmag(vsub(cr, vscale(e3, -1))) else "右手系"
        print(f"    θ={math.degrees(th):5.1f}°  |e|={n1:.6f},{n2:.6f},{n3:.6f}  "
              f"点积={o12:+.1e},{o13:+.1e},{o23:+.1e}  {handed}")

    print(f"\n  (2) 实际导数结构（数值微分，u=Ks）")
    print(f"    {'θ':>7} {'de1/du-(κ/K)e2-(τ/K)e3':>26} {'de2/du+(κ/K)e1':>18} {'de3/du+(τ/K)e1':>18}")
    for th in thetas:
        e1a, e2a, e3a = frame(u0 - h, th)
        e1b, e2b, e3b = frame(u0 + h, th)
        d1 = vscale(vsub(e1b, e1a), 1 / (2 * h))
        d2 = vscale(vsub(e2b, e2a), 1 / (2 * h))
        d3 = vscale(vsub(e3b, e3a), 1 / (2 * h))
        e1, e2, e3 = frame(u0, th)
        kk, tt = math.cos(th), math.sin(th)      # κ/K, τ/K
        pred1 = (kk * e2[0] + tt * e3[0], kk * e2[1] + tt * e3[1], kk * e2[2] + tt * e3[2])
        r1 = vmag(vsub(d1, pred1))
        r2 = vmag((d2[0] + kk * e1[0], d2[1] + kk * e1[1], d2[2] + kk * e1[2]))
        r3 = vmag((d3[0] + tt * e1[0], d3[1] + tt * e1[1], d3[2] + tt * e1[2]))
        print(f"    {math.degrees(th):5.1f}° {r1:>26.3e} {r2:>18.3e} {r3:>18.3e}")
    print("    >>> 残差 ~1e-11（有限差分截断精度）⇒ 实际结构为")
    print("        de1/ds = κe2 + τe3 ,  de2/ds = -κe1 ,  de3/ds = -τe1")
    print("        （并非 §12 声称的三对角 Frenet-Serret：de1/ds=κe2, de2/ds=-κe1+τe3）")

    print(f"\n  (3) Darboux 向量（左手系约定 ω_D = τe2 - κe3）与不变量")
    print(f"    {'θ':>7} {'ω_D/K':>28} {'|ω_D|/K':>10} {'κ²+τ² / K²':>12}")
    for th in thetas:
        e1, e2, e3 = frame(u0, th)
        kk, tt = math.cos(th), math.sin(th)
        wD = (tt * e2[0] - kk * e3[0], tt * e2[1] - kk * e3[1], tt * e2[2] - kk * e3[2])
        print(f"    {math.degrees(th):5.1f}° ({wD[0]:+.3e},{wD[1]:+.3e},{wD[2]:+.6f})"
              f" {vmag(wD):>10.6f} {kk*kk+tt*tt:>12.6f}")
    print("    >>> ω_D ≡ (0,0,1)·K = K ẑ：与 θ 无关（规范不变量）")
    print("        不变量：|ω_D| = K ，κ² + τ² = K²")

    print(f"\n  (4) 【核心】e1（物理场方向）是否依赖 θ？")
    for th in thetas:
        e1, e2, e3 = frame(u0, th)
        print(f"    θ={math.degrees(th):5.1f}°  e1 = ({e1[0]:+.6f}, {e1[1]:+.6f}, {e1[2]:+.6f})")
    print("    >>> e1 与 θ 完全无关！(e2,e3) 只是绕 e1 旋转 θ 角的辅助标架。")
    print("        故 κ=Kcosθ、τ=Ksinθ 的【拆分是规范/标架选择】，不是物理观测量；")
    print("        物理场恒为圆偏振 ⇒ SAM = σℏ 与 θ 无关 ⇒ τ 与自旋无对应关系。")

    # ================= [D] §12.3 正规 3D 螺旋标架 T(z) 的场与自旋 =================
    print("\n" + "-" * 78)
    print("[D] §12.3 正规 3D 螺旋 (T,N,B)：场方向 T(z) 的自旋（关键检验）")
    print("-" * 78)
    print("    §12.3 取 V(z)=(A cos Kz, A sin Kz, Bz)，场方向 = 切向")
    print("      T(z) = (-cosθ sin Kz, cosθ cos Kz, sinθ)")
    print("    ⇒ 横向旋转部分振幅 cosθ（圆偏振）+ 纵向【常量/直流】分量 sinθ")
    print(f"\n    {'θ':>7} {'|E|²/E₀²':>10} {'|S|/(ε₀E₀²/ω)':>16} "
          f"{'u_prop/(ε₀E₀²)':>15} {'自旋/光子(ℏ)':>14}")
    for th in thetas:
        ct, st = math.cos(th), math.sin(th)
        # 单色（传播）部分：横向圆偏振，振幅 cosθ
        Ec3 = (1j * ct * E0, ct * E0, 0j)
        Bc3 = vscale(cross((0, 0, 1), Ec3), 1.0 / c)
        S3 = spin_density(Ec3, w)
        u3 = energy_density(Ec3, Bc3)          # 传播部分能量密度
        # 总场模方（含直流纵向分量）：cos²θ(sin²+cos²) + sin²θ = 1
        Etot2 = ct * ct + st * st
        N3 = u3 / (hbar * w)
        per3 = vmag(S3) / N3 / hbar if N3 > 0 else float('nan')
        print(f"    {math.degrees(th):5.1f}° {Etot2:>10.6f} "
              f"{vmag(S3)/(eps0*E0*E0/w):>16.6f} {u3/(eps0*E0*E0):>15.6f} {per3:>14.6f}")
    print("    >>> 自旋密度 |S| ∝ cos²θ，传播能量 u_prop ∝ cos²θ，二者同比缩放；")
    print("        每光子自旋恒 = ℏ（与 θ 无关）。纵向 sinθ 为常量直流分量，")
    print("        不携带传播能量、不携带自旋 ⇒ 不是光子自由度。")

    # ================= 结论 =================
    print("\n" + "=" * 78)
    print("结论（诚实边界）")
    print("=" * 78)
    print("  ✅ 严格成立：圆偏振每光子自旋 = ℏ（螺旋度 σ=±1），沿传播轴 ẑ；")
    print("     一般椭圆偏振 SAM = σℏ，σ = 2Im(E_x*E_y)/(|E_x|²+|E_y|²) ∈ [-1,1]。")
    print("     自旋方向 = Darboux 向量方向 ω_D/|ω_D| = ẑ，且 |ω_D| = K = ω/c。")
    print("  ⚠️ 规范性质：草案斜标架 (e1,e2,e3) 的 κ/τ 拆分依赖辅助标架绕 e1 的")
    print("     转角 θ，属规范自由度（e1 与 θ 无关）；仅 |ω_D|=K 与 κ²+τ²=K² 为不变量。")
    print("  ⚠️ §12.3 正规螺旋：场方向 T(z) = 圆偏振(振幅 cosθ) + 纵向常量直流 sinθ；")
    print("     自旋密度与传播能量同按 cos²θ 缩放，每光子自旋仍恒为 ℏ；直流分量")
    print("     既不携带传播能量也不携带自旋。")
    print("  ❌ 诚实否定：两种读法下 τ 均不对应自旋自由度；『τ ↔ 自旋投影』不成立。")
    print("     光子自旋由横向圆旋转决定 = σℏ（σ=±1），由 K=ω/c 与螺旋度支配，与 τ 无关。")
    print("  📌 使 τ 物理化的必要条件：场须含纵向分量（结构光/紧聚焦/倏逝波），")
    print("     此时出现横向自旋（transverse spin），但超出自由真空 EM，需另行构造+实验。")
    print("=" * 78)


if __name__ == "__main__":
    main()
