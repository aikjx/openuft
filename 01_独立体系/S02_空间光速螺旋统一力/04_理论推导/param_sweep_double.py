# -*- coding: utf-8 -*-
"""S02 全维精算：双分支参数扫描（纯 Python，输出双 SVG + 数值表）。

前置公设（S02 体系）：
  - 弧长速率恒为 c：  c^2 = u^2 + (R*Omega)^2
  - 映射公设（分支A）： Omega = omega = 2*pi*c/lambda
  - 三重奏恒等式恒成立： kappa^2 + tau^2 = (Omega/c)^2

分支A：多波长扫描（可见光 400~700 nm），固定归一化半径 x = R/R_max。
        kappa, tau, K 全部反比于波长 lambda；kappa/tau 比值不随波长变。
分支B：固定螺距 h 参数化，扫描螺旋半径 R（0~250 nm，h=500 nm）。
        u = c / sqrt(1 + (2*pi*R/h)^2)，Omega = 2*pi*u/h；
        kappa^2 + tau^2 = Omega^2/c^2 仍恒成立，但不再是常数（随 R 增大单调递减）。

红线：仅验证 S02 几何体系自洽；不证明光子真实空间轨迹；
      S02 字面空间螺旋模型轴向速度 u<c，与真空轴向光速实测冲突。

输出：
  param_sweep_A.svg : 多波长扫描（分支A）
  param_sweep_B.svg : 固定螺距扫描（分支B）
"""
import math

# 物理常数（直接字面值，不使用变量占位）
c = 299792458.0


# --------------------------
# 分支A：多波长扫描，固定归一化半径 x
# --------------------------
def branch_A():
    x_list = [0.25, 0.75]
    lam_nm_list = [400, 460, 500, 580, 640, 700]
    out = []
    for lam_nm in lam_nm_list:
        lam = lam_nm * 1e-9
        K = 2.0 * math.pi / lam
        row = {"lam_nm": lam_nm, "K": K}
        for x in x_list:
            kap = x * K
            tau = math.sqrt(1.0 - x * x) * K
            row["kap_x" + str(x)] = kap
            row["tau_x" + str(x)] = tau
        out.append(row)
    return out


# --------------------------
# 分支B：固定螺距 h，扫描 R
# --------------------------
def branch_B(h_nm=500):
    h = h_nm * 1e-9
    R_nm_list = [0, 50, 100, 150, 200, 250]
    out = []
    for R_nm in R_nm_list:
        R = R_nm * 1e-9
        term = (2.0 * math.pi * R / h) ** 2
        u = c / math.sqrt(1.0 + term)
        Omega = 2.0 * math.pi * u / h
        kap = R * Omega * Omega / (c * c)
        tau = u * Omega / (c * c)
        k2t2 = kap * kap + tau * tau
        row = {
            "R_nm": R_nm,
            "u_over_c": u / c,
            "Omega": Omega,
            "kap": kap,
            "tau": tau,
            "k2t2": k2t2,
        }
        out.append(row)
    return out


# 运行计算
resA = branch_A()
resB = branch_B()

# ------------------------------------------------------------------
# 数值表（论文附录）
# ------------------------------------------------------------------
print("==== 分支A：多波长扫描（固定 x） ====")
print(f"{'lambda(nm)':>10} {'K(m^-1)':>14} {'kappa(x=0.25)':>16} {'tau(x=0.25)':>15} "
      f"{'kappa(x=0.75)':>16} {'tau(x=0.75)':>15}")
for r in resA:
    print(f"{r['lam_nm']:>10} {r['K']:14.4e} {r['kap_x0.25']:16.4e} {r['tau_x0.25']:15.4e} "
          f"{r['kap_x0.75']:16.4e} {r['tau_x0.75']:15.4e}")

print("\n==== 分支B：固定螺距 h=500nm，扫描 R ====")
print(f"{'R(nm)':>8} {'u/c':>10} {'Omega(rad/s)':>16} {'kappa(m^-1)':>14} "
      f"{'tau(m^-1)':>14} {'k^2+t^2(m^-2)':>16}")
for r in resB:
    print(f"{r['R_nm']:>8} {r['u_over_c']:10.4f} {r['Omega']:16.4e} {r['kap']:14.4e} "
          f"{r['tau']:14.4e} {r['k2t2']:16.4e}")


# ==================================================================
# SVG 绘图工具
# ==================================================================
def make_svg(width, height):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
             f'viewBox="0 0 {width} {height}">']
    parts.append('<style>'
                 '.axis{stroke:#333;stroke-width:1}'
                 '.grid{stroke:#ddd;stroke-width:1}'
                 '.line{fill:none;stroke-width:2.5}'
                 '.pt{r:3.5}'
                 'text{font-family:Arial;font-size:13px}'
                 '.ttl{font-size:15px;font-weight:bold;fill:#39d0ff}'
                 '.axlbl{fill:#555}'
                 '</style>')
    return parts


def panel_frame(svg, x0, y0, x1, y1, title, xlabel, ylabel, y_unit_suffix=""):
    """绘制坐标轴 + 标题 + 轴标签，返回 (x0,y0,x1,y1)。"""
    svg.append(f'<line class="axis" x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}"/>')
    svg.append(f'<line class="axis" x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}"/>')
    svg.append(f'<text class="ttl" x="{x0}" y="{y0-15}">{title}</text>')
    svg.append(f'<text class="axlbl" x="{(x0+x1)/2}" y="{y1+22}" text-anchor="middle">{xlabel}</text>')
    svg.append(f'<text class="axlbl" x="{x0-40}" y="{(y0+y1)/2}" text-anchor="middle" '
               f'transform="rotate(-90 {x0-40} {(y0+y1)/2})">{ylabel}{y_unit_suffix}</text>')
    return (x0, y0, x1, y1)


def lin_map(xv, xmin, xmax, px0, px1):
    return px0 + (px1 - px0) * (xv - xmin) / (xmax - xmin)


def plot_curve(svg, pts, color):
    strs = [f"{sx:.1f},{sy:.1f}" for (sx, sy) in pts]
    svg.append(f'<polyline class="line" stroke="{color}" points="{" ".join(strs)}"/>')
    for (sx, sy) in pts:
        svg.append(f'<circle class="pt" fill="{color}" cx="{sx:.1f}" cy="{sy:.1f}"/>')


def legend(svg, lx, ly, items):
    for color, lab in items:
        svg.append(f'<line class="line" stroke="{color}" x1="{lx}" y1="{ly}" x2="{lx+25}" y2="{ly}"/>')
        svg.append(f'<text x="{lx+30}" y="{ly+4}">{lab}</text>')
        ly += 22


# ==================================================================
# 图10-1：分支A 多波长扫描
# ==================================================================
def build_figure_A():
    W, H, m = 900, 540, 70
    svg = make_svg(W, H)
    x0, y0, x1, y1 = panel_frame(
        svg, m, m, W - m, H - m,
        "图10-1 分支A：K, κ, τ 随波长 λ 的变化（固定归一化半径 x）",
        "波长 λ (nm)", "曲率/挠率/波数", " (×10⁶ m⁻¹)")

    lam_min, lam_max = 400.0, 700.0
    y_max = 16.0  # 单位 1e6 m^-1（K@400nm ≈ 15.7）

    # 网格线（y）
    for g in [0, 4, 8, 12, 16]:
        gy = y1 - (y1 - y0) * g / y_max
        svg.append(f'<line class="grid" x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}"/>')
        svg.append(f'<text class="axlbl" x="{x0-8}" y="{gy+4:.1f}" text-anchor="end">{g}</text>')
    # 网格线（x）
    for gl in [400, 500, 600, 700]:
        gx = lin_map(gl, lam_min, lam_max, x0, x1)
        svg.append(f'<line class="grid" x1="{gx:.1f}" y1="{y0}" x2="{gx:.1f}" y2="{y1}"/>')
        svg.append(f'<text class="axlbl" x="{gx:.1f}" y="{y1+18}" text-anchor="middle">{gl}</text>')

    def toP(lam_nm, val_unit):
        return (lin_map(lam_nm, lam_min, lam_max, x0, x1),
                y1 - (y1 - y0) * (val_unit / y_max))

    series = [
        ("K (x任意)", "#000000", lambda r: r["K"] / 1e6),
        ("κ (x=0.25)", "#cc2222", lambda r: r["kap_x0.25"] / 1e6),
        ("τ (x=0.25)", "#22aa22", lambda r: r["tau_x0.25"] / 1e6),
        ("κ (x=0.75)", "#2266cc", lambda r: r["kap_x0.75"] / 1e6),
        ("τ (x=0.75)", "#cc8800", lambda r: r["tau_x0.75"] / 1e6),
    ]
    for _, color, expr in series:
        pts = [toP(r['lam_nm'], expr(r)) for r in resA]
        plot_curve(svg, pts, color)

    legend(svg, x0 + 20, y0 + 30,
           [("#000000", "K = 2π/λ"),
            ("#cc2222", "κ (x=0.25)"),
            ("#22aa22", "τ (x=0.25)"),
            ("#2266cc", "κ (x=0.75)"),
            ("#cc8800", "τ (x=0.75)")])

    svg.append('</svg>')
    return "\n".join(svg)


# ==================================================================
# 图10-2：分支B 固定螺距扫描（三面板：u/c, κ&τ, κ²+τ²）
# ==================================================================
def build_figure_B():
    W, H, m = 960, 560, 60
    svg = make_svg(W, H)
    pw = (W - 2 * m - 2 * 30) / 3.0  # 三面板宽
    gap = 30
    R_min, R_max = 0.0, 250.0

    # 面板布局参数
    panel_defs = []
    for i in range(3):
        px0 = m + i * (pw + gap)
        px1 = px0 + pw
        py0 = m
        py1 = H - m
        panel_defs.append((px0, py0, px1, py1))

    panels_spec = [
        ("图10-2a  u/c 随 R 变化", "R (nm)", "u/c", 0.0, 1.05, "uc"),
        ("图10-2b  κ, τ 随 R 变化", "R (nm)", "曲率/挠率", 0.0, 16.0, "kaptau"),
        ("图10-2c  κ²+τ² 随 R 变化", "R (nm)", "κ²+τ²", 0.0, 1.7, "k2t2"),
    ]
    for idx, (title, xlbl, ylbl, ymin, ymax, pkind) in enumerate(panels_spec):
        px0, py0, px1, py1 = panel_defs[idx]
        suffix = ""
        if pkind == "kaptau":
            suffix = " (×10⁶ m⁻¹)"
        elif pkind == "k2t2":
            suffix = " (×10¹⁴ m⁻²)"
        panel_frame(svg, px0, py0, px1, py1, title, xlbl, ylbl, suffix)

        # 网格线（y）
        yticks = [0.0, 0.25, 0.5, 0.75, 1.0] if pkind == "uc" else (
            [0.0, 4.0, 8.0, 12.0, 16.0] if pkind == "kaptau" else [0.0, 0.5, 1.0, 1.5])
        for g in yticks:
            gy = py1 - (py1 - py0) * g / ymax
            svg.append(f'<line class="grid" x1="{px0}" y1="{gy:.1f}" x2="{px1}" y2="{gy:.1f}"/>')
            lab = f"{g:.2f}" if pkind == "uc" else f"{g:.1f}"
            svg.append(f'<text class="axlbl" x="{px0-8}" y="{gy+4:.1f}" text-anchor="end">{lab}</text>')
        # 网格线（x）
        for gxv in [0, 100, 200, 250]:
            gx = lin_map(gxv, R_min, R_max, px0, px1)
            svg.append(f'<line class="grid" x1="{gx:.1f}" y1="{py0}" x2="{gx:.1f}" y2="{py1}"/>')
            svg.append(f'<text class="axlbl" x="{gx:.1f}" y="{py1+18}" text-anchor="middle">{gxv}</text>')

        def toP(R_nm, val):
            return (lin_map(R_nm, R_min, R_max, px0, px1),
                    py1 - (py1 - py0) * (val / ymax))

        if pkind == "uc":
            pts = [toP(r['R_nm'], r['u_over_c']) for r in resB]
            plot_curve(svg, pts, "#2266cc")
            legend(svg, px0 + 15, py0 + 25, [("#2266cc", "u/c")])
        elif pkind == "kaptau":
            pts_k = [toP(r['R_nm'], r['kap'] / 1e6) for r in resB]
            pts_t = [toP(r['R_nm'], r['tau'] / 1e6) for r in resB]
            plot_curve(svg, pts_k, "#cc2222")
            plot_curve(svg, pts_t, "#22aa22")
            legend(svg, px0 + 15, py0 + 25, [("#cc2222", "κ (×10⁶)"), ("#22aa22", "τ (×10⁶)")])
        else:  # k2t2
            pts = [toP(r['R_nm'], r['k2t2'] / 1e14) for r in resB]
            plot_curve(svg, pts, "#8822bb")
            legend(svg, px0 + 15, py0 + 25, [("#8822bb", "κ²+τ² (×10¹⁴)")])

    svg.append('</svg>')
    return "\n".join(svg)


figA = build_figure_A()
figB = build_figure_B()

with open("param_sweep_A.svg", "w", encoding="utf-8") as f:
    f.write(figA)
with open("param_sweep_B.svg", "w", encoding="utf-8") as f:
    f.write(figB)

print("\n[OK] 已生成 param_sweep_A.svg（分支A 多波长扫描）")
print("[OK] 已生成 param_sweep_B.svg（分支B 固定螺距扫描，三面板）")
print("\n红线重申：全部精算仅证明 S02 几何公理体系自洽，不代表物理实在；"
      "S02 字面空间螺旋模型轴向速度 u<c，与真空光速实测冲突。")
