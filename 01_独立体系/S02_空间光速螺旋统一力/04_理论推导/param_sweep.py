# -*- coding: utf-8 -*-
"""S02 全维精算：固定波长 λ，扫描螺旋半径 R（13 个离散采样点）。
公设：Ω = ω, ω = 2πc/λ；S02 弧长速率 c: c² = u² + (RΩ)²。
三重奏：κ² + τ² = (Ω/c)² = K²,  K = 2π/λ。
输出：数值精算表 + 双面板 SVG（Panel A: u/c,κ/K,τ/K vs x；Panel B: (κ/K,τ/K) 单位四分之一圆）。
"""
import math

c = 299792458.0
lam = 500e-9
omega = 2 * math.pi * c / lam
K = 2 * math.pi / lam
R_max = c / omega          # 最大 R：u -> 0 处 = λ/(2π)

samples = 12               # 13 个点 (x = 0, 1/12, ..., 1)
data = []
for i in range(samples + 1):
    x = i / samples
    R = x * R_max
    u = math.sqrt(c**2 - (R * omega)**2)
    u_over_c = u / c
    kappa = (R * omega**2) / (c**2)
    tau = (u * omega) / (c**2)
    k2t2 = kappa**2 + tau**2
    rel_err = abs(k2t2 - K**2) / (K**2)
    data.append({"x": x, "R_nm": R * 1e9, "uc": u_over_c,
                 "kappa": kappa, "tau": tau, "k2t2": k2t2, "rel": rel_err})

print(f"lam={lam*1e9:.2f} nm  omega={omega:.4e} rad/s  K=2pi/lam={K:.4e} m^-1  R_max={R_max*1e9:.4f} nm")
print(f"{'x':>4} {'R(nm)':>8} {'u/c':>10} {'kappa(m^-1)':>12} {'tau(m^-1)':>12} {'k^2+t^2':>14} {'rel_err':>10}")
print("-" * 78)
for r in data:
    print(f"{r['x']:.2f} {r['R_nm']:8.3f} {r['uc']:10.6f} {r['kappa']:12.4e} {r['tau']:12.4e} {r['k2t2']:14.4e} {r['rel']:10.2e}")

# ---------- 双面板 SVG ----------
W, H, m = 900, 500, 60
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
svg.append('<style> .axis{stroke:#333;stroke-width:1} .line{fill:none;stroke-width:2.5} '
           '.pt{r:3.5} text{font-family:Arial;font-size:13px} '
           '.ttl{font-size:15px;font-weight:bold;fill:#39d0ff} </style>')

# Panel A
Ax0, Ay0, Ax1, Ay1 = m, m, m + 420, H - m
svg.append(f'<line class="axis" x1="{Ax0}" y1="{Ay1}" x2="{Ax1}" y2="{Ay1}"/>')
svg.append(f'<line class="axis" x1="{Ax0}" y1="{Ay0}" x2="{Ax0}" y2="{Ay1}"/>')
svg.append(f'<text class="ttl" x="{Ax0}" y="{Ay0-15}">Panel A: u/c, κ/K, τ/K  vs  x=R/R_max</text>')
svg.append(f'<text x="{(Ax0+Ax1)/2}" y="{Ay1+22}" text-anchor="middle">x = R/R_max</text>')
svg.append(f'<text x="{Ax0-34}" y="{(Ay0+Ay1)/2}" text-anchor="middle" '
           f'transform="rotate(-90 {Ax0-34} {(Ay0+Ay1)/2})">Normalized value</text>')

def toA(x, y):
    return Ax0 + (Ax1 - Ax0) * x, Ay1 - (Ay1 - Ay0) * y

curves = [("uc", "#2266cc", lambda r: r["uc"]),
          ("kk", "#cc2222", lambda r: r["kappa"] / K),
          ("tt", "#22aa22", lambda r: r["tau"] / K)]
for _, color, expr in curves:
    pts = [f"{toA(r['x'], expr(r))[0]:.1f},{toA(r['x'], expr(r))[1]:.1f}" for r in data]
    svg.append(f'<polyline class="line" stroke="{color}" points="{" ".join(pts)}"/>')
    for r in data:
        sx, sy = toA(r["x"], expr(r))
        svg.append(f'<circle class="pt" fill="{color}" cx="{sx:.1f}" cy="{sy:.1f}"/>')

lx, ly = Ax0 + 20, Ay0 + 30
for color, lab in [("#2266cc", "u/c"), ("#cc2222", "κ/K"), ("#22aa22", "τ/K")]:
    svg.append(f'<line class="line" stroke="{color}" x1="{lx}" y1="{ly}" x2="{lx+25}" y2="{ly}"/>')
    svg.append(f'<text x="{lx+30}" y="{ly+4}">{lab}</text>')
    ly += 22

# Panel B: (κ/K, τ/K) 单位四分之一圆
Bx0, By0, Bx1, By1 = Ax1 + 40, m, W - m, H - m
svg.append(f'<line class="axis" x1="{Bx0}" y1="{By1}" x2="{Bx1}" y2="{By1}"/>')
svg.append(f'<line class="axis" x1="{Bx0}" y1="{By0}" x2="{Bx0}" y2="{By1}"/>')
svg.append(f'<text class="ttl" x="{Bx0}" y="{By0-15}">Panel B: (κ/K, τ/K) 参数曲线（单位四分之一圆）</text>')
svg.append(f'<text x="{(Bx0+Bx1)/2}" y="{By1+22}" text-anchor="middle">κ/K</text>')
svg.append(f'<text x="{Bx0-34}" y="{(By0+By1)/2}" text-anchor="middle" '
           f'transform="rotate(-90 {Bx0-34} {(By0+By1)/2})">τ/K</text>')

def toB(k, t):
    return Bx0 + (Bx1 - Bx0) * k, By1 - (By1 - By0) * t

pts = [f"{toB(r['kappa']/K, r['tau']/K)[0]:.1f},{toB(r['kappa']/K, r['tau']/K)[1]:.1f}" for r in data]
svg.append(f'<polyline class="line" stroke="#8822bb" points="{" ".join(pts)}"/>')
for r in data:
    sx, sy = toB(r["kappa"] / K, r["tau"] / K)
    svg.append(f'<circle class="pt" fill="#8822bb" cx="{sx:.1f}" cy="{sy:.1f}"/>')

svg.append('</svg>')
with open("param_sweep.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("\n[OK] 已生成 param_sweep.svg（双面板，13 采样点）")
