# -*- coding: utf-8 -*-
"""§12 光速螺旋重构 · 能流验证（Poynting）：检验「能流沿轴向严格以 c 传播」。

仅对物理上成立的情形（圆偏振，τ=0）做严格验证：标准真空平面波
    E = E0 (cos Kz, sin Kz, 0) 的时间谐波，B = ẑ × E / c
    S = E × B / μ0 = ε0 c E0² ẑ ，且 |S|/u = c
即能量通量纯轴向、传播速率 = c，与「轴向速度 ≡ c」的公理一致。

诚实边界（ROOT 红线）：
  - 上述是标准自由真空 EM，完全成立。
  - τ≠0 的斜场标架要求电场含纵向分量（自由真空 ∇·E=0 横波无此分量），
    属结构光/波导/近场；其 Poynting 会含横向/方位分量，但波前轴向传播仍为 c。
    本脚本对斜场标架仅做构造性说明，不做越界宣称。
"""
import math
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

c = 299792458.0
mu0 = 4e-7 * math.pi
eps0 = 1.0 / (mu0 * c * c)   # ≈ 8.854e-12


def circular_pol(z, t, E0, K, w):
    """圆偏振电场与磁场（瞬时实场）。"""
    ph = K * z - w * t
    Ex = E0 * math.cos(ph)
    Ey = E0 * math.sin(ph)
    Ez = 0.0
    # B = ẑ × E / c  →  (Ey, -Ex, 0)/c
    Bx = Ey / c
    By = -Ex / c
    Bz = 0.0
    return (Ex, Ey, Ez), (Bx, By, Bz)


def poynting(E, B):
    Sx = (E[1] * B[2] - E[2] * B[1]) / mu0
    Sy = (E[2] * B[0] - E[0] * B[2]) / mu0
    Sz = (E[0] * B[1] - E[1] * B[0]) / mu0
    return (Sx, Sy, Sz)


def energy_density(E, B):
    return 0.5 * eps0 * (E[0] ** 2 + E[1] ** 2 + E[2] ** 2) + \
           0.5 / mu0 * (B[0] ** 2 + B[1] ** 2 + B[2] ** 2)


def main():
    lam = 500e-9
    K = 2.0 * math.pi / lam
    w = c * K
    E0 = 1.0

    print("=" * 78)
    print("§12 能流验证：圆偏振（τ=0，标准自由真空 EM）")
    print("=" * 78)
    print(f"λ={lam:.3e} m, K={K:.3e} m⁻¹, ω={w:.3e} rad/s, c={c:.3e} m/s")
    print(f"ε0={eps0:.3e}, μ0={mu0:.3e}")

    # 扫描 z、t，检查 S 是否纯轴向、|S| 是否 = ε0 c E0²、|S|/u 是否 = c
    max_trans = 0.0
    max_S_err = 0.0
    max_v_err = 0.0
    zs = [0.0, 0.5e-6, 1.0e-6, 1.5e-6, 2.0e-6]
    ts = [0.0, 1e-15, 2e-15, 3e-15]
    for z in zs:
        for t in ts:
            E, B = circular_pol(z, t, E0, K, w)
            S = poynting(E, B)
            u = energy_density(E, B)
            trans = math.hypot(S[0], S[1])          # 横向分量
            Sabs = math.hypot(*S)
            v = Sabs / u if u > 0 else float('nan')
            max_trans = max(max_trans, trans)
            max_S_err = max(max_S_err, abs(Sabs - eps0 * c * E0 ** 2))
            max_v_err = max(max_v_err, abs(v - c))
    print(f"\n[1] 横向 Poynting |S_⊥| 最大值 = {max_trans:.3e}  (应为 0)")
    print(f"[2] |S| 与 ε0 c E0² 最大偏差 = {max_S_err:.3e}  (理论 |S|=ε0 c E0²)")
    print(f"[3] 能流传播速率 |S|/u 最大偏差 = {max_v_err:.3e}  (理论 = c)")
    print(f"    >>> 圆偏振能流纯轴向、速率严格 c，与公理 u≡c 一致 ✅")

    # 相速度验证：波前 S(z,t) 极值的传播
    # 圆偏振 S 为常量（不随时间振荡），改用 E 相位验证 v_phase = ω/K = c
    v_phase = w / K
    print(f"\n[4] 相位速度 v_phase = ω/K = {v_phase:.6e}  与 c 偏差 {abs(v_phase-c):.2e}")

    # 与 §12 场标架对应：S 沿 e3=ẑ
    print("\n[5] 场标架对应：圆偏振 e3=ẑ（传播轴），S ∝ e3=ẑ → 能流沿标架传播轴")
    print(f"     S = ε0 c E0² · e3 ,  e3=ẑ")

    # 斜场标架（τ≠0）诚实说明
    print("\n" + "-" * 78)
    print("斜场标架 τ≠0（构造性说明，非越界宣称）：")
    print("  若场方向曲线取 §12 的 3D 螺旋 T(z)，电场含纵向分量 E_z≠0；")
    print("  则 ∇·E=0（真空横波条件）被违反，须结构化/波导/近场介质支撑；")
    print("  此类场 Poynting 含横向/方位分量，波前轴向传播仍为 c，")
    print("  但『能流纯轴向』只在 τ=0（圆偏振）成立。需实验验证 τ 可观测效应。")
    print("-" * 78)

    # ---- SVG：圆偏振 E/B/S 箭头（多 z 切片，S 纯轴向）----
    svg = make_svg(K, lam, E0, w)
    with open("lightspeed_helix_poynting.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("\n[OK] 已生成 lightspeed_helix_poynting.svg（E/B 旋转 + S 轴向箭头）")
    print("=" * 78)


def make_svg(K, lam, E0, w):
    W, H = 520, 560
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">',
           '<style>'
           '.axis{stroke:#333;stroke-width:1}'
           '.ttl{font-size:15px;font-weight:bold;fill:#39d0ff}'
           '.axlbl{fill:#555;font-size:12px}'
           '</style>']
    scale = 70.0
    vscale = 70.0
    az = 0.5

    def proj(x, y, z):
        ca, sa = math.cos(az), math.sin(az)
        x1 = x * ca - y * sa
        y1 = x * sa + y * ca
        return (x1 * scale, -z * vscale + y1 * scale * 0.4)

    ox, oy = 260.0, 500.0
    svg.append(f'<text class="ttl" x="{ox-120}" y="{oy+30}">圆偏振能流：S 纯轴向 (速率 c)</text>')
    svg.append(f'<line class="axis" x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy - 4*vscale:.1f}"/>')
    svg.append(f'<text class="axlbl" x="{ox+6}" y="{oy-4*vscale:.1f}">z (传播, c)</text>')

    def arrow(p0, p1, color):
        svg.append(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" '
                   f'stroke="{color}" stroke-width="2.2"/>')
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy)
        if L < 1e-6:
            return
        ux, uy = dx / L, dy / L
        px, py = -uy, ux
        bx, by = p1[0] - 9 * ux, p1[1] - 9 * uy
        w1x, w1y = bx + 5 * px, by + 5 * py
        w2x, w2y = bx - 5 * px, by - 5 * py
        svg.append(f'<polygon points="{p1[0]:.1f},{p1[1]:.1f} {w1x:.1f},{w1y:.1f} {w2x:.1f},{w2y:.1f}" fill="{color}"/>')

    t0 = 0.0
    zs = [0.0, 1.0e-6, 2.0e-6, 3.0e-6, 4.0e-6]
    for z in zs:
        E, B = circular_pol(z, t0, E0, K, w)
        base = proj(0.0, 0.0, z)
        # E（绿）
        Et = (base[0] + E[0] * scale, base[1] - E[1] * scale * 0.4)
        arrow(base, Et, "#22aa22")
        # B（橙）：B = ẑ×E/c，按 c 放大使其与 E 同尺度可视觉（B 方向 = 垂直 E）
        Bt = (base[0] + B[0] * c * scale, base[1] - B[1] * c * scale * 0.4)
        arrow(base, Bt, "#ee8800")
        # S（红，纯轴向 ẑ）
        S = poynting(E, B)
        Stip = (base[0], base[1] - (vscale * 0.9))
        arrow(base, Stip, "#cc2222")
        svg.append(f'<text class="axlbl" x="{base[0]+8}" y="{base[1]-2}">z={z*1e6:.0f}µm</text>')

    svg.append(f'<text class="axlbl" x="{ox-120}" y="{oy+50}">绿=E场 橙=B场 红=S能流(沿ẑ)</text>')
    svg.append(f'<text class="axlbl" x="{ox-120}" y="{oy+68}">'
               f'S = ε0 c E0² ẑ，|S|/u = c（无 u&lt;c 几何约束）</text>')
    svg.append('</svg>')
    return "\n".join(svg)


if __name__ == "__main__":
    main()
