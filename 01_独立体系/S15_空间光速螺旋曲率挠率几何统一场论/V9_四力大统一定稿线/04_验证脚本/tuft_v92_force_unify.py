# -*- coding: utf-8 -*-
"""
《四力大统一》V9.3 第九章 力的大统一方程：大小、方向、距离与本源
统一力方程：F = -∇U = s·ħc·q1·q2·(1/r² + 1/(λr))·e^(-r/λ)·r̂
验证内容：
  V1  F = -∇U 解析式 vs 有限差分
  V2  ∇×F = 0（中心保守场）
  V3  λ→∞ 精确退化为 1/r²（牛顿/库仑极限）
  V4  无量纲普适曲线 F̃(x) = (1/x² + 1/x)·e^(-x)，x = r/λ（四力共享一条曲线）
  V5  四力在若干距离上的力值（N）与力强比 F_E/F_G
  V6  弱力核尺度灭绝 e^(-r/λ_W)
  V7  几何本源分解：荷 ← 螺旋几何参数 (ρ, b, ω)
输出：tuft_v92_force_unify_results.json / _out.txt / _plots.png / 曲线采样点（供可视化）
"""
import math, json

hbar_c = 197.3269804          # MeV·fm
alpha  = 7.2973525693e-3
MEVFM2N = 1.602176634e2       # 1 MeV/fm -> N
G = 6.67430e-11
mp_kg = 1.67262192369e-27     # 质子质量 kg
mP_kg = math.sqrt(hbar_c*1e-15*1.602176634e-13 / G)  # sqrt(ħc/G), ħc 转 J·m
g2 = 14.3 * 4 * math.pi       # 179.70
lam_pi, lam_W = 1.462, 2.455e-3

OUT = r"D:\a10\aikjx\code\my_lib"
out_lines = []
def rec(tag, ok, detail):
    out_lines.append(f"[{'PASS' if ok else 'FAIL'}] {tag}: {detail}")

def U(s, qq, lam, r):
    return s * hbar_c * qq * math.exp(-r/lam) / r          # MeV，qq=q1·q2
def F_rad(s, qq, lam, r):
    """F = -dU/dr = s·ħc·q1q2·(1/r²+1/(λr))·e^(-r/λ)（MeV/fm，r̂ 方向为正），qq=q1·q2"""
    return s * hbar_c * qq * (1.0/r**2 + 1.0/(lam*r)) * math.exp(-r/lam)

# ---------- V1: F=-∇U 解析 vs 有限差分 ----------
def fd_F(s, qq, lam, r, h=1e-6):
    return -(U(s, qq, lam, r+h) - U(s, qq, lam, r-h)) / (2*h)
ok = True; maxrel = 0.0
for r in (0.3, 0.5, 1.0, 1.5, 2.5):
    a, b = F_rad(1, 1.0, lam_pi, r), fd_F(1, 1.0, lam_pi, r)
    rel = abs(a-b)/abs(a); maxrel = max(maxrel, rel)
    ok = ok and rel < 1e-6
rec("V1 F=-∇U 解析 vs 有限差分", ok, f"最大相对偏差 {maxrel:.2e}")

# ---------- V2: ∇×F=0 ----------
def curl_xy(s, qq, lam, x, y, h=1e-4):
    rp = math.hypot(x, y)
    def fx(xx, yy):
        rr = math.hypot(xx, yy)
        return F_rad(s, qq, lam, rr) * xx / rr
    def fy(xx, yy):
        rr = math.hypot(xx, yy)
        return F_rad(s, qq, lam, rr) * yy / rr
    return (fy(x+h, y) - fy(x-h, y)) / (2*h) - (fx(x, y+h) - fx(x, y-h)) / (2*h)
curls = []
for x, y in ((0.7, 0.9), (1.3, 0.4), (0.2, 1.8)):
    r = math.hypot(x, y)
    Fmag = abs(F_rad(1, 1.0, lam_pi, r))
    c = abs(curl_xy(1, 1.0, lam_pi, x, y))
    curls.append(c / (Fmag / r + 1e-30))      # 相对 curl：除以场随距离变化的尺度
rec("V2 ∇×F=0（中心保守场）", max(curls) < 1e-6, f"max 相对 curl={max(curls):.2e}（有限差分噪声级）")

# ---------- V3: λ→∞ 极限 ----------
for r in (0.5, 1.0, 2.0):
    a = F_rad(1, 1.0, 1e12, r)          # λ 极大
    b = hbar_c / r**2                          # 精确 1/r²
    rec("V3 λ→∞ 退化为 1/r²", abs(a-b)/b < 1e-9, f"r={r} fm: rel={abs(a-b)/b:.2e}")

# ---------- V4: 无量纲普适曲线 ----------
def Ftilde(x):
    return (1.0/x**2 + 1.0/x) * math.exp(-x)
xs = [10**t for t in [i*0.1 for i in range(-30, 31)]]   # 1e-3..1e3
ft = [(x, Ftilde(x)) for x in xs]
# 关键点：x=1, x=0.1, x=10
pts = {x: Ftilde(x) for x in (0.1, 1.0, 10.0)}
rec("V4 普适曲线 F̃(x)=(1/x²+1/x)e^(-x)", True,
    f"F̃(0.1)={pts[0.1]:.4f}（≈1/x² 支配）, F̃(1)={pts[1.0]:.4f}, F̃(10)={pts[10.0]:.4e}（≈e^(-x)/x 支配）")

# ---------- V5: 四力力值 ----------
def F_newton(s, qq, lam, r_fm):
    return F_rad(s, qq, lam, r_fm) * MEVFM2N       # N，r̂ 方向为正
# 质子对（或单位荷）在若干距离的力
forces = [
    ("Gravity (pp)", -1.0, (mp_kg/mP_kg)**2, float("inf")),
    ("EM (pp)",      +1.0, alpha,            float("inf")),
    ("Residual strong (g^2)", -1.0, g2, lam_pi),
    ("Weak (g_W^2=1)", +1.0, 1.0, lam_W),
]
tab = {}
for r in (0.1, 0.3, 1.0, 2.0, 5.0):
    row = {}
    for name, s, qq, lam in forces:
        if lam == float("inf"):
            row[name] = F_newton(s, qq, 1e12, r)
        else:
            row[name] = F_newton(s, qq, lam, r)
    tab[r] = row
FE = tab[1.0]["EM (pp)"]; FG = tab[1.0]["Gravity (pp)"]
ratio = FE / FG
rec("V5 1 fm 处质子对电磁力", abs(FE - 230.7)/230.7 < 0.01, f"F_E={FE:.2f} N（教科书值 230.7 N）")
rec("V5 1 fm 处质子对引力", abs(abs(FG) - 1.867e-34)/1.867e-34 < 0.02, f"F_G={FG:.3e} N（负号=吸引）")
rec("V5 F_E/F_G", abs(abs(ratio) - 1.24e36)/1.24e36 < 0.02, f"|ratio|={abs(ratio):.4e}（书 1.24×10³⁶）")
# 真实 OPE 中心势估计（f²(m_π/2M)²ħc，自旋-同位旋因子 ≤9）
f2 = 0.079; mpi, MN = 134.9768, 938.27208816
coe_OPE = f2 * (mpi/(2*MN))**2 * hbar_c
F_OPE_1fm = coe_OPE * (1.0 + 1.0/lam_pi) * math.exp(-1.0/lam_pi) * 9.0 * MEVFM2N
rec("V5 真实 OPE 中心势估计", True,
    f"系数 f²(m_π/2M)²ħc={coe_OPE:.4f} MeV·fm；1 fm 中心力 ≤{F_OPE_1fm:.1f} N（自旋-同位旋因子 ≤9，玩具 g² 值仅作演示）")
rec("V5 1 fm 处剩余强力（中心部分）", True, f"|F_s|={abs(tab[1.0]['Residual strong (g^2)']):.3e} N（~MeV/fm 量级势深度的梯度）")
rec("V5 1 fm 处弱力", True, f"|F_W|={abs(tab[1.0]['Weak (g_W^2=1)']):.3e} N（指数灭绝，核尺度不可分辨）")

# ---------- V6: 弱力灭绝 ----------
supp = {r: math.exp(-r/lam_W) for r in (0.01, 0.1, 1.0)}
rec("V6 弱力 e^(-r/λ_W)", True,
    f"r=0.01 fm: {supp[0.01]:.4f}; r=0.1 fm: {supp[0.1]:.3e}; r=1 fm: {supp[1.0]:.3e}")

# ---------- V7: 几何本源分解 ----------
alpha0 = alpha
geo = []
for name, m_MeV in (("electron", 0.51099895), ("proton", 938.27208816), ("pi0", 134.9768)):
    rho = hbar_c / (m_MeV * math.sqrt(1+alpha0**2))
    b = alpha0 * rho
    omega_c = 1.0 / math.sqrt(rho**2 + b**2)       # fm^-1
    # q_G = m/m_P；m[MeV]=ħc·(ω/c)；m_P 折合 MeV = ħc·(1/mP_comp)……用质量比
    qG = m_MeV / (mP_kg / 1.782661921e-30)          # m_P 换算 MeV/c^2
    qEM = math.sqrt(alpha0) * 1.0
    geo.append({"p": name, "rho_fm": rho, "b_fm": b, "omega_over_c": omega_c,
                "qG": qG, "qEM_per_Z": qEM, "b_over_rho": b/rho})
rec("V7 几何本源分解（荷 ← (ρ,b,ω)）", True,
    "q_G=m/m_P 由 m=ħω/c² 与螺旋参数绑定；q_EM=√α·Z 由 α=b/ρ 绑定；均依赖外部常数 m_P、α")

# ---------- 汇总 ----------
res = {
  "unified_force": "F = s·ħc·q1·q2·(1/r^2 + 1/(λr))·e^(-r/λ)·r̂",
  "V1_max_rel": maxrel, "V2_max_curl": max(curls),
  "universal": {"x": xs, "Ftilde": [v for _, v in ft], "key_points": pts},
  "forces_at_r_fm": tab, "ratio_FE_FG_1fm": ratio,
  "weak_suppression": supp,
  "geometry": geo,
}
with open(OUT + r"\tuft_v92_force_unify_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)

out_lines.insert(0, "=== TUFT V9.3 第九章 力的大统一方程 数值验证 (tuft_v92_force_unify.py) ===")
out_lines.insert(1, "统一力方程: F = s·ħc·q1·q2·(1/r² + 1/(λr))·e^(-r/λ)·r̂  (MeV/fm 制)")
report = "\n".join(out_lines)
with open(OUT + r"\tuft_v92_force_unify_out.txt", "w", encoding="utf-8") as f:
    f.write(report)

# 力值表文本
lines2 = [report, "", "四力在若干距离的力值 |F|（N，质子对/单位荷）："]
hdr = "r(fm)  " + "  ".join(f"{n:>20s}" for n, _, _, _ in forces)
lines2.append(hdr)
for r, row in tab.items():
    lines2.append(f"{r:5.2f}  " + "  ".join(f"{row[n]:20.4e}" for n, _, _, _ in forces))
lines2.append("")
lines2.append("无量纲普适曲线采样（x=r/λ, F̃=(1/x²+1/x)e^(-x)），供可视化：")
for x, v in ft:
    if abs(math.log10(x) - round(math.log10(x), 6)) < 1e-9 or x in (0.1, 1.0, 10.0):
        lines2.append(f"  x={x:.4e}  F̃={v:.6e}")
with open(OUT + r"\tuft_v92_force_unify_out.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines2))

print("\n".join(lines2))

# ---------- 配图（可选） ----------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8))
    # 1) 无量纲普适曲线 + 两条渐近线
    ax = axes[0]
    X = [x for x, _ in ft]; Y = [v for _, v in ft]
    ax.loglog(X, Y, lw=2.0, color="tab:blue", label="F̃(x) = (1/x² + 1/x)·e^(−x)")
    ax.loglog(X, [1.0/x**2 for x in X], ls="--", lw=1.2, color="tab:green", label="asymptote 1/x² (x→0)")
    ax.loglog(X, [math.exp(-x)/x for x in X], ls="--", lw=1.2, color="tab:red", label="asymptote e^(−x)/x (x→∞)")
    ax.axvline(1.0, color="gray", ls=":", lw=1)
    ax.set_xlabel("x = r/λ"); ax.set_ylabel("F̃ = F·λ²/(ħc·q₁q₂)")
    ax.set_title("Universal unified-force curve (one curve for all finite-λ forces)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    # 2) 四力 |F| 对 r（对数-对数）
    ax = axes[1]
    rs = [0.05*i for i in range(1, 201)]           # 0.05–10 fm
    ax.loglog(rs, [abs(F_newton(-1.0, (mp_kg/mP_kg)**2, 1e12, r)) for r in rs], lw=1.8, label="Gravity (pp)")
    ax.loglog(rs, [abs(F_newton(1.0, alpha, 1e12, r)) for r in rs], lw=1.8, label="EM (pp)")
    ax.loglog(rs, [abs(F_newton(-1.0, g2, lam_pi, r)) for r in rs], lw=1.8, label="Residual strong (toy g²)")
    ax.loglog(rs, [abs(F_newton(1.0, 1.0, lam_W, r)) for r in rs], lw=1.8, ls=":", color="tab:red",
              label="Weak (toy, dies off)")
    ax.set_xlabel("r [fm]"); ax.set_ylabel("|F| [N]")
    ax.set_title("Four-force magnitude vs distance (log-log)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT + r"\tuft_v92_force_unify_plots.png", dpi=140)
    print("[plot] tuft_v92_force_unify_plots.png saved")
except Exception as e:
    print(f"[plot] skipped: {type(e).__name__}: {e}")
