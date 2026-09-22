# -*- coding: utf-8 -*-
"""S02 全维精算：Frenet 标架演化 + 误差传播分析（纯 Python，输出双 SVG + 数值 demo）。

前置公设（S02 体系）：
  - 弧长速率恒为 c：  c^2 = u^2 + (R*Omega)^2
  - 映射公设：        Omega = omega = 2*pi*c/lambda
  - 圆柱螺旋：        r(s) = (R cos(Omega/c s), R sin(Omega/c s), (u/c) s)

红线：全部推导仅验证 S02 几何体系自洽；不证明光子真实空间轨迹；
      S02 字面空间螺旋模型轴向速度 u<c，与真空轴向光速实测冲突。

输出：
  frenet_evol.svg   : 标架演化矢量图（螺旋中心线 + 多弧长位置 t/n/b 正交箭头）
  error_heatmap.svg : 挠率相对误差热力图 sigma_tau/tau vs (R/R_max, lambda)
"""
import math

c = 299792458.0


# ==================================================================
# 几何：Frenet 标架与 Darboux 转动向量
# ==================================================================
def frenet_frame(s, R, lam):
    Omega = 2.0 * math.pi * c / lam
    u = math.sqrt(c ** 2 - (R * Omega) ** 2)
    kappa = R * Omega ** 2 / (c ** 2)
    tau = u * Omega / (c ** 2)
    theta = Omega / c * s
    t = (-R * Omega / c * math.sin(theta),
         R * Omega / c * math.cos(theta),
         u / c)
    n = (-math.cos(theta),
         -math.sin(theta),
         0.0)
    b = (u / c * math.sin(theta),
         -u / c * math.cos(theta),
         R * Omega / c)
    # Darboux 向量： omega_D = tau * t + kappa * b
    om = (tau * t[0] + kappa * b[0],
          tau * t[1] + kappa * b[1],
          tau * t[2] + kappa * b[2])
    return t, n, b, om, kappa, tau


# ==================================================================
# 误差传播：kappa, tau, kappa^2+tau^2 对 (R, lambda) 测量误差的传导
# ==================================================================
def error_kappa_tau(R, lam, sigma_R, sigma_lam):
    kappa = 4.0 * math.pi ** 2 * R / (lam ** 2)
    xi = 2.0 * math.pi * R / lam
    sq = math.sqrt(1.0 - xi ** 2)
    tau = (2.0 * math.pi / lam) * sq
    dk_dR = kappa / R
    dk_dlam = -2.0 * kappa / lam
    # 正确 dtau_dR（量纲 m^-2）： tau=(2pi/lam)*sqrt(1-xi^2), xi=2pi*R/lam
    #   = -8*pi^3*R/(lam^3*sqrt(1-xi^2)) = -kappa*xi/(R*sqrt(1-xi^2))
    # 注：论文 §2.2 旧写 dtau_dR=-kappa/sqrt(1-xi^2) 量纲错误（缺 xi/R 因子），已订正。
    dtau_dR = -kappa * xi / (R * sq)
    dtau_dlam = -tau / lam + (2.0 * math.pi * xi ** 2) / (lam ** 2 * sq)
    sig_kap = math.sqrt((dk_dR * sigma_R) ** 2 + (dk_dlam * sigma_lam) ** 2)
    sig_tau = math.sqrt((dtau_dR * sigma_R) ** 2 + (dtau_dlam * sigma_lam) ** 2)
    # kappa^2 + tau^2 = (2pi/lambda)^2  ->  d/dR = 0,  d/dlambda = -8*pi^2/lambda^3
    sig_k2t2 = abs(-8.0 * math.pi ** 2 / (lam ** 3)) * sigma_lam
    return kappa, tau, sig_kap, sig_tau, sig_k2t2


# ==================================================================
# SVG 基础工具
# ==================================================================
def make_svg(width, height):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
             f'viewBox="0 0 {width} {height}">']
    parts.append('<style>'
                 '.axis{stroke:#333;stroke-width:1}'
                 '.grid{stroke:#ddd;stroke-width:1}'
                 '.line{fill:none;stroke-width:2.5}'
                 'text{font-family:Arial;font-size:13px}'
                 '.ttl{font-size:15px;font-weight:bold;fill:#39d0ff}'
                 '.axlbl{fill:#555}'
                 '</style>')
    return parts


def arrow(svg, p0, p1, color, head=11):
    svg.append(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" '
               f'stroke="{color}" stroke-width="2.5"/>')
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    if L < 1e-6:
        return
    ux, uy = dx / L, dy / L
    px, py = -uy, ux  # 垂直
    bx, by = p1[0] - head * ux, p1[1] - head * uy
    w1x, w1y = bx + head * 0.6 * px, by + head * 0.6 * py
    w2x, w2y = bx - head * 0.6 * px, by - head * 0.6 * py
    svg.append(f'<polygon points="{p1[0]:.1f},{p1[1]:.1f} {w1x:.1f},{w1y:.1f} {w2x:.1f},{w2y:.1f}" '
               f'fill="{color}"/>')


# ==================================================================
# 图11-1：Frenet 标架演化矢量图（3D 正交投影，示意 z 轴压缩）
# ==================================================================
def build_frenet_svg():
    lam = 500e-9
    R = 20e-9
    Omega = 2.0 * math.pi * c / lam
    u = math.sqrt(c ** 2 - (R * Omega) ** 2)
    R_max = lam / (2.0 * math.pi)
    s_cycle = lam  # 一个螺旋周期的弧长
    s_max = 2.0 * s_cycle  # 画 2 圈

    R_scene = 70.0           # 场景尺度：螺旋半径像素
    scale = R_scene / R     # 米 -> 像素
    z_squash = 0.16         # 轴向示意压缩（非等比，仅绘图用）
    az, el = 0.95, 0.5

    def proj0(x, y, z):
        ca, sa = math.cos(az), math.sin(az)
        ce, se = math.cos(el), math.sin(el)
        x1 = x * ca - y * sa
        y1 = x * sa + y * ca
        x2 = x1
        y2 = y1 * ce - z * se
        z2 = y1 * se + z * ce
        return scale * x2, -scale * z2 * z_squash

    # 螺旋中心线采样
    helix_pts = []
    Ns = 400
    for i in range(Ns + 1):
        s = s_max * i / Ns
        theta = Omega / c * s
        x = R * math.cos(theta)
        y = R * math.sin(theta)
        z = (u / c) * s
        helix_pts.append((x, y, z))

    # 标架采样弧长位置
    s_samples = [0.0, 0.25e-6, 0.5e-6, 0.75e-6, 1.0e-6]
    arrow_px = 55.0
    arrow_m = arrow_px / scale

    # 收集所有需投影的 3D 点以自动适配视图框
    raw = []
    for (x, y, z) in helix_pts:
        raw.append(proj0(x, y, z))
    frame_defs = []  # (base3d, [ (vec3d, color), ... ])
    for s in s_samples:
        t, n, b, om, kap, tau = frenet_frame(s, R, lam)
        theta = Omega / c * s
        base = (R * math.cos(theta), R * math.sin(theta), (u / c) * s)
        vecs = [("t", t, "#cc2222"), ("n", n, "#22aa22"), ("b", b, "#2266cc")]
        for (_, v, col) in vecs:
            tip = (base[0] + v[0] * arrow_m,
                   base[1] + v[1] * arrow_m,
                   base[2] + v[2] * arrow_m)
            raw.append(proj0(*base))
            raw.append(proj0(*tip))
        frame_defs.append((base, vecs))

    xs = [p[0] for p in raw]
    ys = [p[1] for p in raw]
    margin = 50.0
    minx, maxx = min(xs) - margin, max(xs) + margin
    miny, maxy = min(ys) - margin, max(ys) + margin
    W = maxx - minx
    H = maxy - miny

    def P(x, y, z):
        sx, sy = proj0(x, y, z)
        return (sx - minx, sy - miny)

    svg = make_svg(W, H)
    # 中心线
    hp = ["%.1f,%.1f" % P(*pt) for pt in helix_pts]
    svg.append(f'<polyline class="line" stroke="#888" stroke-width="1.5" points="{" ".join(hp)}"/>')

    # 标架箭头
    for (base, vecs) in frame_defs:
        for (_, v, col) in vecs:
            tip = (base[0] + v[0] * arrow_m,
                   base[1] + v[1] * arrow_m,
                   base[2] + v[2] * arrow_m)
            arrow(svg, P(*base), P(*tip), col)

    # 图例
    lx, ly = 20.0, 30.0
    for col, lab in [("#cc2222", "t 切向"), ("#22aa22", "n 主法向"), ("#2266cc", "b 副法向")]:
        svg.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+25}" y2="{ly}" stroke="{col}" stroke-width="2.5"/>')
        svg.append(f'<text x="{lx+32}" y="{ly+4}">{lab}</text>')
        ly += 22
    svg.append(f'<text class="ttl" x="{lx}" y="{H-20}">图11-1 Frenet 标架演化 '
               f'(lambda=500nm, R=20nm, z 轴示意压缩)</text>')
    svg.append('</svg>')
    return "\n".join(svg)


# ==================================================================
# 图11-2：挠率相对误差热力图  sigma_tau/tau  vs (R/R_max, lambda)
# ==================================================================
def heat_color(val):
    if not math.isfinite(val) or val <= 0:
        t = 1.0
    else:
        lv = math.log10(val)
        lo, hi = -3.0, 0.3
        t = (lv - lo) / (hi - lo)
        t = max(0.0, min(1.0, t))
    r = int(255 * t)
    b = int(255 * (1.0 - t))
    g = int(140 * (1.0 - abs(t - 0.5) * 2.0))
    return f"rgb({r},{g},{b})"


def build_heatmap_svg():
    sigma_R = 0.5e-9
    sigma_lam = 1e-9
    W, H, m = 760, 520, 70
    svg = make_svg(W, H)
    px0, py0, px1, py1 = m, m, W - m, H - m
    gx, gy = 60, 48  # 网格列、行数
    cw = (px1 - px0) / gx
    ch = (py1 - py0) / gy

    for i in range(gx):
        xfrac = (i + 0.5) / gx           # R/R_max ∈ (0,1)
        for j in range(gy):
            # y 轴：lambda 400..700，方向自下而上
            lam_nm = 400.0 + (700.0 - 400.0) * (1.0 - (j + 0.5) / gy)
            lam = lam_nm * 1e-9
            R_max = lam / (2.0 * math.pi)
            R = xfrac * R_max
            _, tau, _, sig_tau, _ = error_kappa_tau(R, lam, sigma_R, sigma_lam)
            rel = sig_tau / tau if tau > 0 else float("inf")
            col = heat_color(rel)
            x = px0 + i * cw
            y = py0 + j * ch
            svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" fill="{col}"/>')

    # 坐标轴
    svg.append(f'<line class="axis" x1="{px0}" y1="{py1}" x2="{px1}" y2="{py1}"/>')
    svg.append(f'<line class="axis" x1="{px0}" y1="{py0}" x2="{px0}" y2="{py1}"/>')
    svg.append(f'<text class="axlbl" x="{(px0+px1)/2}" y="{py1+22}" text-anchor="middle">归一化半径 R/R_max</text>')
    svg.append(f'<text class="axlbl" x="{px0-46}" y="{(py0+py1)/2}" text-anchor="middle" '
               f'transform="rotate(-90 {px0-46} {(py0+py1)/2})">波长 lambda (nm)</text>')
    for i in range(6):
        xf = i / 5.0
        x = px0 + xf * (px1 - px0)
        svg.append(f'<text class="axlbl" x="{x:.1f}" y="{py1+18}" text-anchor="middle">{xf:.1f}</text>')
    for j, ln in enumerate([400, 460, 520, 580, 640, 700]):
        y = py0 + (1.0 - (ln - 400) / 300.0) * (py1 - py0)
        svg.append(f'<text class="axlbl" x="{px0-8}" y="{y+4:.1f}" text-anchor="end">{ln}</text>')

    # 色标（相对误差，对数）
    cb_x, cb_y, cb_w, cb_h = px1 + 25, py0, 24, py1 - py0
    steps = 40
    for k in range(steps):
        t = k / (steps - 1)
        val = 10 ** (-3.0 + t * 3.3)
        col = heat_color(val)
        y = cb_y + (1.0 - t) * cb_h
        svg.append(f'<rect x="{cb_x:.1f}" y="{y:.1f}" width="{cb_w:.1f}" height="{cb_h/steps+1:.1f}" fill="{col}"/>')
    svg.append(f'<text class="axlbl" x="{cb_x+cb_w+4}" y="{cb_y+8}" font-size="11">10^0</text>')
    svg.append(f'<text class="axlbl" x="{cb_x+cb_w+4}" y="{cb_y+cb_h/2:.1f}" font-size="11">10^-1.5</text>')
    svg.append(f'<text class="axlbl" x="{cb_x+cb_w+4}" y="{cb_y+cb_h:.1f}" font-size="11">10^-3</text>')
    svg.append(f'<text class="ttl" x="{px0}" y="{py0-20}">图11-2 挠率相对误差 sigma_tau/tau 热力图 '
               f'(sigma_R=0.5nm, sigma_lambda=1nm)</text>')
    svg.append(f'<text class="axlbl" x="{px0}" y="{py1+40}" font-size="11">'
               f'右侧（R/R_max→1）tau→0，相对误差发散（已饱和红色）</text>')
    svg.append('</svg>')
    return "\n".join(svg)


# ===================== Demo 运行 =====================
print("=== Frenet 标架演化 demo (lambda=500nm, R=20nm) ===")
lam = 500e-9
R = 20e-9
Omega = 2.0 * math.pi * c / lam
u = math.sqrt(c ** 2 - (R * Omega) ** 2)
R_max = lam / (2.0 * math.pi)
for s in [0.0, 0.25e-6, 0.5e-6, 0.75e-6, 1.0e-6]:
    t, n, b, om, kap, tau = frenet_frame(s, R, lam)
    om_mag = math.sqrt(om[0] ** 2 + om[1] ** 2 + om[2] ** 2)
    print(f"s={s:.2e} t={tuple(round(v,3) for v in t)} n={tuple(round(v,3) for v in n)} "
          f"b={tuple(round(v,3) for v in b)}")
    print(f"    |omega_D|={om_mag:.4e}  (应等于 Omega/c={Omega/c:.4e})  kappa={kap:.3e} tau={tau:.3e}")

print("\n=== Darboux 向量模长一致性校验（|omega_D| == K = Omega/c）===")
for xf in [0.0, 0.25, 0.5, 0.75, 0.99]:
    RR = xf * R_max
    _, _, _, om, _, _ = frenet_frame(0.0, RR, lam)
    om_mag = math.sqrt(om[0] ** 2 + om[1] ** 2 + om[2] ** 2)
    print(f"R/R_max={xf:.2f}  |omega_D|={om_mag:.4e}  K=Omega/c={Omega/c:.4e}  "
          f"rel_err={abs(om_mag-Omega/c)/(Omega/c):.2e}")

print("\n=== 误差传播 demo (lambda=500nm, R=20nm, sigma_R=0.5nm, sigma_lambda=1nm) ===")
sigma_R = 0.5e-9
sigma_lam = 1e-9
kap, tau, sig_kap, sig_tau, sig_k2t2 = error_kappa_tau(R, lam, sigma_R, sigma_lam)
print(f"kappa={kap:.3e}  sigma_kappa={sig_kap:.3e}  rel_err={sig_kap/kap:.2%}")
print(f"tau={tau:.3e}  sigma_tau={sig_tau:.3e}  rel_err={sig_tau/tau:.2%}")
print(f"sigma_(kappa^2+tau^2)={sig_k2t2:.3e}  (仅由 sigma_lambda 决定，与 R 无关)")
print(f"  相对误差公式校验: (sigma_kappa/kappa)=sqrt((sigma_R/R)^2+(2 sigma_lambda/lambda)^2)"
      f"={math.sqrt((sigma_R/R)**2+(2*sigma_lam/lam)**2):.2%}")

# 生成图件
svgA = build_frenet_svg()
svgB = build_heatmap_svg()
with open("frenet_evol.svg", "w", encoding="utf-8") as f:
    f.write(svgA)
with open("error_heatmap.svg", "w", encoding="utf-8") as f:
    f.write(svgB)
print("\n[OK] 已生成 frenet_evol.svg（Frenet 标架演化矢量图）")
print("[OK] 已生成 error_heatmap.svg（挠率相对误差热力图）")

print("\n红线重申：几何标架演化与误差传播仅完成 S02 体系数学自洽校验，不代表物理实在；"
      "S02 模型轴向速度推论与真空光速实测冲突。")
