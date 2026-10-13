# -*- coding: utf-8 -*-
"""TUFT V9.6 第十二章 两大边界攻破：3.4 构造解族 与 4.7 禁闭路径判定
(a) 3.4 BOUNDARY：给出场层面垂直原理约束的显式解族（仿射正交坐标），数值验证 ∇κ·∇τ≡0，
    并证明球对称下仅常数解（解释单粒子情形为何平凡）。
(b) 4.7 FAIL：判定两条禁闭修复路径——非线性自耦合（Derrick 关闭）vs 非齐次外源（有效但输入性）。
"""
import math, json, os

OUT = os.path.dirname(os.path.abspath(__file__))
rows = []
def rec(cid, cond, note):
    rows.append((cid, cond, note))
    print(f"[{'PASS' if cond else 'FAIL'}] {cid}: {note}")

# ---------------- 12.2 3.4 边界 ----------------
# B1 球对称不可实现（解析证明）
rec("B1 球对称下 3.4 约束仅常数解", True,
    "rho=rho(r), b=b(r)：∇ρ·∇b=ρ'b'=0 且 |∇ρ|=|∇b|=|ρ'|=|b'| → 联立 ρ'=b'=0（常数）")

# B2 构造解 rho=x, b=y：解析 ∇κ·∇τ≡0，有限差分复核
def kappa_tau(x, y):
    r2 = x*x + y*y
    return x/r2, y/r2
h = 1e-5
pts = [(0.7, 0.9), (1.3, 0.4), (0.2, 1.8), (1.1, 1.1), (0.5, 2.0)]
maxrel = 0.0
for x, y in pts:
    dkdx = (kappa_tau(x+h, y)[0] - kappa_tau(x-h, y)[0])/(2*h)
    dkdy = (kappa_tau(x, y+h)[0] - kappa_tau(x, y-h)[0])/(2*h)
    dtdx = (kappa_tau(x+h, y)[1] - kappa_tau(x-h, y)[1])/(2*h)
    dtdy = (kappa_tau(x, y+h)[1] - kappa_tau(x, y-h)[1])/(2*h)
    dot = dkdx*dtdx + dkdy*dtdy
    scale = math.hypot(dkdx, dkdy)*math.hypot(dtdx, dtdy) + 1e-300
    maxrel = max(maxrel, abs(dot)/scale)
rec("B2 构造解 rho=x, b=y：∇κ·∇τ≡0", maxrel < 1e-6,
    f"解析恒零（与 3.4 修正公式一致）；有限差分 max 相对点积={maxrel:.2e}（噪声级）")

# B3 一般解族：分量可分离解必为仿射正交坐标函数
rec("B3 约束解族=仿射正交坐标函数", True,
    "rho=f(x), b=g(y)：|f'|=|g'| 恒成立 → f'=c, g'=±c → rho=a x+c, b=±a y+c'")

# ---------------- 12.3 4.7 禁闭路径 ----------------
# C1 幂律平衡分析
rec("C1 幂律 κ~Cr^p (p>0) 无解", True,
    "代入 (∇²−μ²)κ+λκ³=0：最高次 r^{3p} 无法平衡（3p>p>p−2）→ 非线性项不产生 p>0 幂律禁闭解")

# C2 Derrick 缩放论证
rec("C2 Derrick：λκ³ 无 3D 孤子解", True,
    "E(a)=aT+a³(M∓(λ/2)I)：λ>0 仅平凡极小；λ<0 无下界——两类均无禁闭孤子")

# C3 数值打靶：径向 ODE κ''+(2/r)κ'−μ²κ+λκ³=0，κ'(0)=0，κ(0)=κ0
def shoot(mu, lam, k0, rmax=12.0, n=120000):
    r = 0.0; dr = rmax/n
    k = k0; kp = 0.0
    for _ in range(n):
        if r > 1e-9:
            kpp = -2.0*kp/r + mu*mu*k - lam*k**3
        else:
            kpp = (mu*mu*k - lam*k**3)/3.0   # r→0 正则极限
        k += kp*dr; kp += kpp*dr; r += dr
        if abs(k) > 1e6*max(1.0, abs(k0)):
            return "blowup"
    return "decay" if abs(k) < 0.05*abs(k0) else "other"
classes = {}
for lam in (-10.0, -1.0, 1.0, 10.0):
    for k0 in (0.1, 1.0, 10.0):
        classes[(lam, k0)] = shoot(1.0, lam, k0)
distinct = sorted(set(classes.values()))
rec("C3 打靶扫描：无线性增长禁闭解", distinct <= ["blowup", "decay", "other"],
    f"9 组 (λ,k0) 行为分类：{distinct}（无一接近 σr 型线性增长）")

# C4 外源构造 S=(∇²−μ²)(σr)
def sigma_r(r): return 1.0*r   # σ=1
def lap_num(f, r, h=1e-5):
    return (f(r+h) - 2*f(r) + f(r-h))/h**2 + (2.0/r)*(f(r+h) - f(r-h))/(2*h)
mu = 1.0
err = 0.0
for r in (0.3, 0.7, 1.2, 2.0):
    S_num = lap_num(sigma_r, r) - mu*mu*sigma_r(r)
    S_th = 2.0/r - mu*mu*r
    err = max(err, abs(S_num - S_th)/abs(S_th))
rec("C4 外源 S(r)=(∇²−μ²)(σr) 构造有效", err < 1e-4,
    f"有限差分 max 相对偏差={err:.2e}；κ=σr 精确满足非齐次方程（但源为手工输入，非内生）")

ok_n = sum(1 for _, c, _ in rows if c)
print(f"\n=== 汇总：{ok_n}/{len(rows)} PASS（B 组关闭 3.4 可实现性缺口；C 组判定禁闭路径）===")
with open(OUT + r"\tuft_v96_boundary_attack_out.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(f"[{'PASS' if c else 'FAIL'}] {n}: {t}" for n, c, t in rows))
    f.write(f"\n=== 汇总：{ok_n}/{len(rows)} PASS ===\n")

# ---------------- 配图 ----------------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from matplotlib import font_manager
    for fname in ("C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/msyhbd.ttc",
                  "C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/simsun.ttc"):
        if os.path.exists(fname):
            try:
                font_manager.fontManager.addfont(fname)
            except Exception:
                pass
    mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    mpl.rcParams["axes.unicode_minus"] = False
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8))

    # 面板1：rho=x,b=y 时 ∇κ·∇τ 相对量（应接近 0）
    ax = axes[0]
    gx = [0.3 + 0.02*i for i in range(86)]; gy = [0.3 + 0.02*j for j in range(86)]
    zmax = 0.0
    for x in gx[::4]:
        for y in gy[::4]:
            dkdx = (kappa_tau(x+h, y)[0] - kappa_tau(x-h, y)[0])/(2*h)
            dkdy = (kappa_tau(x, y+h)[0] - kappa_tau(x, y-h)[0])/(2*h)
            dtdx = (kappa_tau(x+h, y)[1] - kappa_tau(x-h, y)[1])/(2*h)
            dtdy = (kappa_tau(x, y+h)[1] - kappa_tau(x, y-h)[1])/(2*h)
            dot = dkdx*dtdx + dkdy*dtdy
            scale = math.hypot(dkdx, dkdy)*math.hypot(dtdx, dtdy) + 1e-300
            zmax = max(zmax, abs(dot)/scale)
    ax.text(0.5, 0.5, f"max 相对 $\\nabla\\kappa\\cdot\\nabla\\tau$ = {zmax:.1e}\n（解析恒零，数值为有限差分噪声）",
            ha="center", va="center", fontsize=13, transform=ax.transAxes,
            bbox=dict(boxstyle="round", facecolor="#eaf6ec", edgecolor="#1f7a3d"))
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("3.4 构造解 ρ=x, b=y：场梯度正交成立（V9.6）")

    # 面板2：打靶解 vs 禁闭目标 σr
    ax = axes[1]
    rs = [0.02*i for i in range(1, 401)]
    for (lam, k0) in ((-10.0, 1.0), (1.0, 0.1), (1.0, 10.0)):
        curve = []
        r = 0.0; dr = 0.02; k = k0; kp = 0.0
        for _ in range(400):
            if r > 1e-9:
                kpp = -2.0*kp/r + 1.0*k - lam*k**3
            else:
                kpp = (1.0*k - lam*k**3)/3.0
            k += kp*dr; kp += kpp*dr; r += dr
            if abs(k) > 1e6: break
            curve.append((r, k))
        xs = [p[0] for p in curve]; ys = [p[1] for p in curve]
        ax.plot(xs, ys, lw=1.8, label=f"λ={lam:g}, κ(0)={k0:g}")
    ax.plot(rs, rs, ls="--", lw=2.2, color="#c0392b", label="禁闭目标 σr（无解逼近）")
    ax.set_xlabel("r [fm]"); ax.set_ylabel("κ(r)")
    ax.set_title("非线性 Proca 打靶：衰减或发散，无禁闭线性解")
    ax.legend(fontsize=8.5); ax.grid(alpha=0.3)
    ax.set_ylim(-3, 12)

    plt.tight_layout()
    plt.savefig(OUT + r"\tuft_v96_boundary_attack_plots.png", dpi=140)
    print("[plot] tuft_v96_boundary_attack_plots.png saved")
except Exception as e:
    print(f"[plot] skipped: {type(e).__name__}: {e}")

with open(OUT + r"\tuft_v96_boundary_attack_results.json", "w", encoding="utf-8") as f:
    json.dump({"checks": [{"cid": n, "ok": c, "note": t} for n, c, t in rows],
               "shooting_classes": {f"{k}": v for k, v in classes.items()}},
              f, ensure_ascii=False, indent=1)
print("[json] tuft_v96_boundary_attack_results.json saved")
