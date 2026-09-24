# -*- coding: utf-8 -*-
"""§12 光速螺旋（Light-Speed Helix）重构：场标架演化 + 数值验证（纯 Python，输出 SVG + 校验）。

核心修复：旧 S02 把 Frenet 标架绑到“粒子沿空间螺旋轨迹”，弧长速率 c 分解出轴向 u<c，
        与真空光速实验冲突。新模型：场/自旋标架沿轴向以 c 传播；标架曲线是
        “场矢量方向曲线”（在几何空间），不是质点轨迹；横向分量是相位旋转而非
        质点横向速度。轴向速度恒为 c，无几何冲突。

诚实边界（ROOT 红线，不粉饰）：
  1) 圆偏振（τ=0）即标准电磁圆偏振电场矢量旋转，物理上完全成立。
  2) 斜场标架（τ≠0，κ²+τ²=K²）要求场矢量方向曲线为 3D 螺旋、含纵向分量；
     自由真空平面波无纵向电场（∇·E=0），故 τ≠0 情形对应结构光/波导/近场，
     非自由空间光；其可观测挠率效应仍需实验验证。
  3) 本重构在数学骨架（κ²+τ²=K²、|ω_D|=K）上与旧 S02 完全一致，仅替换物理解释；
     不提供新的独立实验证据。

注意：原稿 Par2/§12 草案所写 e1=(cos Ks, sin Ks, 0) 为平面曲线（Frenet 挠率=0），
      且“e3=ẑ 常数 + τ≠0”几何上不能共存（副法向必随螺旋旋转）。本脚本采用
      修正后的 3D 螺旋方向曲线 V(z)=(A cos Kz, A sin Kz, B z)（A=cosθ/K, B=sinθ），
      其 Frenet 标架给出 κ=K cosθ, τ=K sinθ, Darboux ω_D=K ẑ，轴向 z 即弧长、传播速率 c。
"""
import math
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

c = 299792458.0


# ==================================================================
# 修正后的斜场标架：场矢量方向曲线 = 单位速率 3D 螺旋
#   V(z) = (A cos Kz, A sin Kz, B z),  A = cosθ/K, B = sinθ
#   A²K² + B² = cos²θ + sin²θ = 1  →  z 为弧长（轴向坐标即传播弧长，速率 c）
# ==================================================================
def helix_frame(z, theta, K):
    A = math.cos(theta) / K
    B = math.sin(theta)
    cK = math.cos(K * z)
    sK = math.sin(K * z)
    # 切线 T = V'/|V'| （|V'|=1）
    T = (-A * K * sK, A * K * cK, B)          # = (-cosθ sinKz, cosθ cosKz, sinθ)
    # 主法 N = T'/|T'|  (|T'| = A K² = K cosθ)
    N = (-cK, -sK, 0.0)
    # 副法 B = T × N
    Bv = (T[1] * N[2] - T[2] * N[1],
          T[2] * N[0] - T[0] * N[2],
          T[0] * N[1] - T[1] * N[0])
    kappa = K * math.cos(theta)
    tau = K * math.sin(theta)
    return T, N, Bv, kappa, tau


# ==================================================================
# 原稿草案的“字面框架”（用于演示其不一致）：e1 平面、e2/e3 倾斜旋转
# ==================================================================
def user_frame(z, theta, K):
    cK = math.cos(K * z)
    sK = math.sin(K * z)
    e1 = (cK, sK, 0.0)
    e2 = (-sK * math.cos(theta), cK * math.cos(theta), math.sin(theta))
    e3 = (-sK * math.sin(theta), cK * math.sin(theta), -math.cos(theta))
    return e1, e2, e3


# ==================================================================
# Frenet-Serret 数值校验（解析标架 vs 有限差分 d/ds）
# ==================================================================
def check_fs(K, theta, z_list, h=1e-10):
    maxr = 0.0
    for z in z_list:
        T, N, B, kap, tau = helix_frame(z, theta, K)
        Tp, Np, Bp, _, _ = helix_frame(z + h, theta, K)
        Tm, Nm, Bm, _, _ = helix_frame(z - h, theta, K)
        dT = tuple((Tp[i] - Tm[i]) / (2 * h) for i in range(3))
        dN = tuple((Np[i] - Nm[i]) / (2 * h) for i in range(3))
        dB = tuple((Bp[i] - Bm[i]) / (2 * h) for i in range(3))
        r1 = math.sqrt(sum((dT[i] - kap * N[i]) ** 2 for i in range(3)))
        rhsN = tuple(-kap * T[i] + tau * B[i] for i in range(3))
        r2 = math.sqrt(sum((dN[i] - rhsN[i]) ** 2 for i in range(3)))
        rhsB = tuple(-tau * N[i] for i in range(3))
        r3 = math.sqrt(sum((dB[i] - rhsB[i]) ** 2 for i in range(3)))
        maxr = max(maxr, r1, r2, r3)
    return maxr


def check_fs_scaled(K, theta, u_list, h_u=1e-5):
    """F-S 校验（无量纲版）：在 u=K·s 上中心差分，d/ds = K·d/du。

    为何需要：米制 s 上 K≈1.26e7 ⇒ 三阶导 ~K³≈2e21，中心差分截断误差
    ~h²·K³/6；取 h=1e-10 时已达 |res|≈3.3，相对 κ≈1.26e7 约 2.6e-7
    （旧注释误标为 ~1e-8）。    改用无量纲参数后导数 O(1)，相对残差 ~4e-10（较米制版改善约 600×）。
    """
    maxr = 0.0
    k = K / (2.0 * h_u)
    for u in u_list:
        T, N, B, kap, tau = helix_frame(u / K, theta, K)
        Tp, Np, Bp, _, _ = helix_frame((u + h_u) / K, theta, K)
        Tm, Nm, Bm, _, _ = helix_frame((u - h_u) / K, theta, K)
        dT = tuple(k * (Tp[i] - Tm[i]) for i in range(3))
        dN = tuple(k * (Np[i] - Nm[i]) for i in range(3))
        dB = tuple(k * (Bp[i] - Bm[i]) for i in range(3))
        r1 = math.sqrt(sum((dT[i] - kap * N[i]) ** 2 for i in range(3)))
        r2 = math.sqrt(sum((dN[i] - (-kap * T[i] + tau * B[i])) ** 2 for i in range(3)))
        r3 = math.sqrt(sum((dB[i] - (-tau * N[i])) ** 2 for i in range(3)))
        maxr = max(maxr, r1, r2, r3)
    return maxr


def check_invariant(K, theta):
    kap = K * math.cos(theta)
    tau = K * math.sin(theta)
    return abs(kap ** 2 + tau ** 2 - K ** 2) / K ** 2


def check_darboux(K, theta, z_list):
    maxr = 0.0
    for z in z_list:
        T, N, B, kap, tau = helix_frame(z, theta, K)
        wD = (tau * T[0] + kap * B[0],
              tau * T[1] + kap * B[1],
              tau * T[2] + kap * B[2])
        # 期望 ω_D = K ẑ
        r = math.sqrt((wD[0] - 0.0) ** 2 + (wD[1] - 0.0) ** 2 + (wD[2] - K) ** 2)
        maxr = max(maxr, r)
    return maxr


def check_user_frame(K, theta, z_list, h=1e-10):
    """演示原稿字面框架：e1 为平面曲线 → Frenet 挠率=0；
    其“扭转系数” <e1',e3>=K sinθ 是移动标架的 twist(Bishop)，不是 Frenet 挠率。"""
    def e1(z):
        return user_frame(z, theta, K)[0]

    # e1 恒在 xy 平面（z 分量恒 0）⇒ 平面曲线 ⇒ Frenet 挠率=0
    max_e1z = max(abs(e1(z)[2]) for z in z_list)

    # 计算字面框架的 twist 系数 b = <e1', e3>
    z = 0.0
    ep = e1(z + h); em = e1(z - h)
    T = tuple((ep[i] - em[i]) / (2 * h) for i in range(3))
    e3 = user_frame(z, theta, K)[2]
    twist = T[0] * e3[0] + T[1] * e3[1] + T[2] * e3[2]
    return max_e1z, twist


# ==================================================================
# SVG 绘图
# ==================================================================
def make_svg(w, h):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">',
            '<style>'
            '.axis{stroke:#333;stroke-width:1}'
            '.line{fill:none;stroke-width:2.2}'
            'text{font-family:Arial;font-size:13px}'
            '.ttl{font-size:15px;font-weight:bold;fill:#39d0ff}'
            '.axlbl{fill:#555}'
            '</style>']


def arrow(svg, p0, p1, color, head=10):
    svg.append(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" '
               f'stroke="{color}" stroke-width="2.2"/>')
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    if L < 1e-6:
        return
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    bx, by = p1[0] - head * ux, p1[1] - head * uy
    w1x, w1y = bx + head * 0.6 * px, by + head * 0.6 * py
    w2x, w2y = bx - head * 0.6 * px, by - head * 0.6 * py
    svg.append(f'<polygon points="{p1[0]:.1f},{p1[1]:.1f} {w1x:.1f},{w1y:.1f} {w2x:.1f},{w2y:.1f}" '
               f'fill="{color}"/>')


def build_svg(K, lam):
    W, H = 760, 560
    svg = make_svg(W, H)
    # 投影：传播方向 z 向上；xy 旋转水平展开，带轻微深度倾斜
    scale = 90.0
    vscale = 26.0
    az = 0.6

    def proj(x, y, z):
        ca, sa = math.cos(az), math.sin(az)
        x1 = x * ca - y * sa
        y1 = x * sa + y * ca
        return (x1 * scale, -z * vscale + y1 * scale * 0.45)

    # ---- Panel A：圆偏振（θ=0）场标架演化 ----
    ax0, ay0 = 200.0, 470.0   # 面板 A 原点（屏幕）
    panelA_title = "Panel A：圆偏振 τ=0（标准 EM，无冲突）"

    def panelA_proj(x, y, z):
        sx, sy = proj(x, y, z)
        return (ax0 + sx, ay0 + sy)

    # 螺旋方向曲线（平面圆，z 仅作传播轴标记，故绘于各高度）
    zs = [0.0, 1.0e-6, 2.0e-6, 3.0e-6, 4.0e-6]
    # 轴向 ẑ 轴
    svg.append(f'<line class="axis" x1="{ax0:.1f}" y1="{ay0:.1f}" x2="{ax0:.1f}" y2="{ay0 - 4*vscale:.1f}"/>')
    svg.append(f'<text class="axlbl" x="{ax0+6:.1f}" y="{ay0 - 4*vscale:.1f}">z (传播, 速率 c)</text>')
    triad_len = 0.9
    for zi, z in enumerate(zs):
        T, N, B, kap, tau = helix_frame(z, 0.0, K)
        base = (0.0, 0.0, z)
        bscr = panelA_proj(*base)
        # 场矢量方向 = -N (圆偏振电场方向)
        field = (-N[0] * triad_len, -N[1] * triad_len, -N[2] * triad_len)
        tip = (base[0] + field[0], base[1] + field[1], base[2] + field[2])
        arrow(svg, bscr, panelA_proj(*tip), "#22aa22")   # 场矢量（绿）
        # 副法向 ẑ（蓝）
        btip = (base[0] + B[0] * triad_len, base[1] + B[1] * triad_len, base[2] + B[2] * triad_len)
        arrow(svg, bscr, panelA_proj(*btip), "#2266cc")
    svg.append(f'<text class="ttl" x="{ax0-120:.1f}" y="{ay0+30:.1f}">{panelA_title}</text>')
    svg.append(f'<text class="axlbl" x="{ax0-120:.1f}" y="{ay0+50:.1f}">'
               f'κ=K={K:.3e}, τ=0, ω_D=K ẑ；电场矢量绕 ẑ 旋转，轴向严格 c</text>')

    # ---- Panel B：斜场标架（θ=π/4）3D 螺旋方向曲线 ----
    bx0, by0 = 560.0, 470.0
    panelB_title = "Panel B：斜场标架 θ=π/4（κ²+τ²=K²）"

    def panelB_proj(x, y, z):
        sx, sy = proj(x, y, z)
        return (bx0 + sx, by0 + sy)

    theta = math.pi / 4
    A = math.cos(theta) / K
    B = math.sin(theta)
    # 螺旋方向曲线 V(z)
    helix_pts = []
    Nz = 200
    zmax = 4.0e-6
    for i in range(Nz + 1):
        z = zmax * i / Nz
        V = (A * math.cos(K * z), A * math.sin(K * z), B * z)
        helix_pts.append(panelB_proj(*V))
    hp = ["%.1f,%.1f" % p for p in helix_pts]
    svg.append(f'<polyline class="line" stroke="#888" stroke-width="1.5" points="{" ".join(hp)}"/>')
    # 轴向 ẑ
    svg.append(f'<line class="axis" x1="{bx0:.1f}" y1="{by0:.1f}" x2="{bx0:.1f}" y2="{by0 - B*zmax*vscale:.1f}"/>')
    svg.append(f'<text class="axlbl" x="{bx0+6:.1f}" y="{by0 - B*zmax*vscale:.1f}">z (传播, 速率 c)</text>')
    # 标架箭头
    zs2 = [0.0, 1.0e-6, 2.0e-6, 3.0e-6, 4.0e-6]
    for z in zs2:
        T, N, Bv, kap, tau = helix_frame(z, theta, K)
        base = (A * math.cos(K * z), A * math.sin(K * z), B * z)
        bscr = panelB_proj(*base)
        for vec, col in [(T, "#cc2222"), (N, "#22aa22"), (Bv, "#2266cc")]:
            tip = (base[0] + vec[0] * triad_len, base[1] + vec[1] * triad_len, base[2] + vec[2] * triad_len)
            arrow(svg, bscr, panelB_proj(*tip), col)
    svg.append(f'<text class="ttl" x="{bx0-110:.1f}" y="{by0+30:.1f}">{panelB_title}</text>')
    svg.append(f'<text class="axlbl" x="{bx0-110:.1f}" y="{by0+50:.1f}">'
               f'κ=K cosθ, τ=K sinθ；ω_D=K ẑ（传播轴），副法向 B 随螺旋旋转</text>')

    # 图例
    lx, ly = 20.0, 30.0
    for col, lab in [("#cc2222", "T 切向(场方向)"), ("#22aa22", "N 主法向"), ("#2266cc", "B 副法向")]:
        svg.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+25}" y2="{ly}" stroke="{col}" stroke-width="2.2"/>')
        svg.append(f'<text x="{lx+32}" y="{ly+4}">{lab}</text>')
        ly += 22
    svg.append('</svg>')
    return "\n".join(svg)


# ==================================================================
# 主报告
# ==================================================================
def main():
    lam = 500e-9
    K = 2.0 * math.pi / lam
    z_list = [0.0, 0.5e-6, 1.0e-6, 1.5e-6, 2.0e-6, 2.5e-6, 3.0e-6]

    print("=" * 78)
    print("§12 光速螺旋（Light-Speed Helix）重构验证")
    print("=" * 78)

    # 1) Frenet-Serret（修正后的 3D 螺旋方向曲线）
    u_list = [K * z for z in z_list]
    for name, th in [("圆偏振 θ=0", 0.0), ("斜场 θ=π/4", math.pi / 4), ("斜场 θ=π/3", math.pi / 3)]:
        res_old = check_fs(K, th, z_list)            # 米制差分（截断误差显著）
        res = check_fs_scaled(K, th, u_list)         # 无量纲差分
        kap = K * math.cos(th)
        print(f"[1] F-S 残差 ({name}) = {res:.3e}  相对 κ={kap:.3e} → {res/kap:.2e}（无量纲差分，标架满足 F-S）")
        print(f"    米制差分对照 |res|={res_old:.3e}（相对 {res_old/kap:.2e}，纯 h² 截断，非模型误差）")

    # 1b) 步长收敛性：证明残差确为 h² 截断（先降后升的 U 形：截断∝h²，舍入∝1/h）
    print("\n[1b] 步长收敛性（θ=π/4）：残差应随 h 减小按 h² 下降，过小则舍入主导回升")
    prev = None
    for h_u in [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
        r = check_fs_scaled(K, math.pi / 4, u_list, h_u=h_u)
        tag = "" if prev is None else f"   上一档/本档 = {prev/r:8.1f}"
        print(f"    h_u={h_u:.0e}  残差={r:.4e}{tag}")
        prev = r
    print("    >>> 下降段比值≈100（h 缩 10× ⇒ 残差降 100×）证明确为 O(h²) 截断；")
    print("        h_u=1e-6 回升为浮点舍入主导。最优 h_u≈1e-5（相对残差 ~4e-10）。")

    # 2) 不变量
    print("\n[2] 不变量 κ²+τ²=K²")
    for th in [0.0, math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2 - 1e-3]:
        rel = check_invariant(K, th)
        print(f"    θ={th:.3f}  rel_err={rel:.2e}   κ=K cosθ={K*math.cos(th):.3e}  τ=K sinθ={K*math.sin(th):.3e}")

    # 3) Darboux = K ẑ
    res = check_darboux(K, math.pi / 4, z_list)
    print(f"\n[3] Darboux |ω_D - K ẑ| 残差 (θ=π/4) = {res:.3e}  (ω_D 恒沿传播轴 ẑ)")

    # 4) 原稿字面框架不一致演示
    print("\n[4] 原稿草案字面框架 e1=(cos Ks,sin Ks,0) 演示")
    maxz, twist = check_user_frame(K, math.pi / 4, z_list)
    print(f"    e1 的 z 分量（恒为 0 ⇒ 平面曲线）max|e1_z| = {maxz:.2e}")
    print(f"    ⇒ Frenet 挠率 τ=0（平面），与所写 τ=K sinθ 矛盾")
    print(f"    e1' 在 e3 上的投影（移动标架 twist 系数）= {twist:.3e} = K sinθ={K*math.sin(math.pi/4):.3e}")
    print(f"    >>> 该 twist 是 Bishop 帧旋转系数，不是 Frenet 挠率；")
    print(f"        正确获得 τ≠0 须用 3D 螺旋方向曲线 V(z)=(A cos Kz,A sin Kz,B z)。")

    # 5) 与 §9 数值映射
    print("\n[5] 与 §9 参数扫描的映射（全部数值/误差表可直接复用）")
    print(f"    x = R/R_max = cosθ ;  κ = K·x ;  τ = K·√(1-x²) = K·sinθ")
    print(f"    θ=0 ↔ x=1 (R=R_max, 纯弯曲 τ=0) ;  θ=π/2 ↔ x=0 (R=0, 纯扭转 κ=0)")

    # 生成 SVG
    svg = build_svg(K, lam)
    with open("lightspeed_helix.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("\n[OK] 已生成 lightspeed_helix.svg（场标架演化：圆偏振 + 斜场 3D 螺旋）")

    print("\n" + "=" * 78)
    print("结论：光速螺旋重构在数学骨架（κ²+τ²=K²、|ω_D|=K）上与旧 S02 完全一致，")
    print("      仅把底层物理解释由“粒子空间轨迹”改为“场/自旋标架沿轴向以 c 传播”；")
    print("      轴向速度恒为 c，消除 u<c 冲突。τ≠0 情形需纵向场分量（非自由真空光），")
    print("      其可观测效应仍待实验验证（ROOT 红线）。")
    print("=" * 78)


if __name__ == "__main__":
    main()
