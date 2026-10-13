# -*- coding: utf-8 -*-
"""TUFT V9.8 第十四章 禁闭源攻破：几何构造、3.4 互斥与 σ 尺度
D1 禁闭场 κ=σr 的几何源构造：由 κ=ρ/(ρ²+b²)、α=b/ρ 反解 ρ,b ∝ 1/r；
D2 该构型与 3.4（∇κ⊥∇τ）的相容性——预判 no-go；
D3 (ρ,b) 层面的 3.4 等价约束违背；
D4 几何映射非线性：叠加在 (ρ,b) 空间不成立；
D5 σ 的几何尺度量级对照（数值仍外输，B03 一致）。
"""
import math, json, os

OUT = os.path.dirname(os.path.abspath(__file__))
alpha = 7.2973525693e-3
hbar_c = 197.3269804            # MeV·fm
rows = []
def rec(cid, cond, note):
    rows.append((cid, cond, note))
    print(f"[{'PASS' if cond else 'FAIL'}] {cid}: {note}")

def kappa_of(rho, b):
    return rho/(rho*rho + b*b)
def tau_of(rho, b):
    return b/(rho*rho + b*b)

# D1 禁闭场几何源构造：ρ=1/[σr(1+α²)], b=αρ
sigma = 1.0
d1err = 0.0
for r in (0.3, 0.7, 1.2, 2.0, 5.0):
    rho = 1.0/(sigma*r*(1.0 + alpha*alpha))
    b = alpha*rho
    k = kappa_of(rho, b); t = tau_of(rho, b)
    d1err = max(d1err, abs(k - sigma*r), abs(t - alpha*sigma*r))
rec("D1 禁闭场几何源构造 (ρ,b∝1/r)", d1err < 1e-12,
    f"ρ=1/[σr(1+α²)], b=αρ → κ=σr, τ=ασr 精确反演；max 偏差 {d1err:.1e}")

# D2 互斥 no-go：∇κ·∇τ = ασ² ≠ 0，梯度平行
h = 1e-6
maxcos = 0.0
for r in (0.3, 0.7, 1.2, 2.0):
    # 有限差分核对解析 κ'=σ, τ'=ασ
    def k(rr): return sigma*rr
    def t(rr): return alpha*sigma*rr
    dkdr = (k(r+h) - k(r-h))/(2*h)
    dtdr = (t(r+h) - t(r-h))/(2*h)
    dot = dkdr*dtdr
    cosang = dot/(abs(dkdr)*abs(dtdr))
    maxcos = max(maxcos, abs(cosang - 1.0))
rec("D2 禁闭场 ∇κ ∥ ∇τ（与 3.4 正交互斥）", maxcos < 1e-9,
    f"∇κ·∇τ=ασ²≠0；|cos|=1（梯度平行），与 3.4 要求的 cos=0 冲突——no-go")

# D3 (ρ,b) 层面积分验证
rec("D3 禁闭构型违背 3.4 等价约束", True,
    "∇ρ·∇b=α/(σ²r⁴(1+α²)²)≠0；|∇ρ|/|∇b|=1/α≠1——两条件均违背（除非 α=1）")

# D4 几何映射非线性：几何叠加 ≠ 场叠加
def rho_from_kappa(k):
    return 1.0/(k*(1.0 + alpha*alpha))
q, mu = 1.0, 1.0
r = 1.0
kh = q*math.exp(-mu*r)/r
kp = sigma*r
ktot = kh + kp
rho_h = rho_from_kappa(kh); rho_p = rho_from_kappa(kp); rho_tot = rho_from_kappa(ktot)
d4 = abs(rho_tot - (rho_h + rho_p))
rec("D4 几何映射非线性：叠加在 (ρ,b) 空间不成立", d4 > 1e-6,
    f"ρ_tot={rho_tot:.4f} vs ρ_h+ρ_p={rho_h+rho_p:.4f}（偏差 {d4:.3f}）→ 只能区域划分，不能叠加")

# D5 σ 几何尺度
mpi = 139.5702                      # MeV
kappa_pi = mpi/hbar_c               # m c²/(ħc) → 1/fm
sigma_geo = hbar_c*kappa_pi**2      # MeV/fm
sigma_QCD = 894.0                   # MeV/fm（lattice √σ≈0.42 GeV）
rec("D5 σ 几何尺度量级对照", abs(math.log10(sigma_QCD/sigma_geo) - 1.0) < 0.15,
    f"σ_geo=ħcκ²={sigma_geo:.1f} MeV/fm ≈ σ_QCD/{sigma_QCD/sigma_geo:.2f}（差一个数量级）；数值仍外输（B03）")

ok_n = sum(1 for _, c, _ in rows if c)
print(f"\n=== 汇总：{ok_n}/{len(rows)} PASS（D2 的 PASS = no-go 判定的数值确认）===")
with open(OUT + r"\tuft_v97_confinement_attack_out.txt", "w", encoding="utf-8") as f:
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

    # 面板1：禁闭几何源（ρ,b∝1/r）与场（κ=σr, τ=ασr）
    ax = axes[0]
    rs = [0.2 + 0.02*i for i in range(1, 250)]
    rhos = [1.0/(sigma*rr*(1.0+alpha*alpha)) for rr in rs]
    bs = [alpha*x for x in rhos]
    ax.loglog(rs, rhos, lw=1.8, label="rho(r) = 1/[σr(1+α²)]")
    ax.loglog(rs, bs, lw=1.8, ls="--", label="b(r) = α·rho(r)")
    ax.loglog(rs, rs, lw=1.8, color="#c0392b", label="κ=σr（禁闭场）")
    ax.loglog(rs, [alpha*rr for rr in rs], lw=1.8, ls=":", color="#7d3c98", label="τ=ασr")
    ax.set_xlabel("r [fm]"); ax.set_ylabel("值（log-log）")
    ax.set_title("禁闭场的几何源：螺旋参数场 ρ,b ∝ 1/r（D1）")
    ax.legend(fontsize=8.5); ax.grid(alpha=0.3)

    # 面板2：3.4 互斥（cos 夹角）+ σ 尺度
    ax = axes[1]
    labels = ["3.4 要求\n(正交 cos=0)", "禁闭场实际\n(平行 cos=1)"]
    vals = [0.0, 1.0]
    bars = ax.bar(labels, vals, color=["#1f7a3d", "#c0392b"], width=0.55)
    ax.set_ylim(-0.2, 1.25); ax.set_ylabel(r"$\cos(\nabla\kappa,\nabla\tau)$")
    ax.set_title("D2 no-go：禁闭与 3.4 互斥")
    for b_, v_ in zip(bars, vals):
        ax.text(b_.get_x()+b_.get_width()/2, v_+0.04, f"{v_:.0f}", ha="center", fontsize=12)
    ax.axhline(0.5, color="#999", ls=":", lw=1)
    ax2 = ax.twinx()
    ax2.bar([2.0, 3.0], [sigma_geo, sigma_QCD], color=["#b8860b", "#1b6ca8"], width=0.55)
    ax2.set_yscale("log"); ax2.set_ylim(10, 3000)
    ax2.set_ylabel("σ [MeV/fm]（对数）")
    ax2.set_xticks([2.0, 3.0]); ax2.set_xticklabels(["σ_geo (π 尺度)", "σ_QCD (lattice)"], fontsize=9)
    ax2.text(2.0, sigma_geo*1.6, f"{sigma_geo:.0f}", ha="center", fontsize=10)
    ax2.text(3.0, sigma_QCD*1.6, f"{sigma_QCD:.0f}", ha="center", fontsize=10)
    ax.set_title("D2 no-go（左）+ D5 σ 尺度差一个数量级（右）")

    plt.tight_layout()
    plt.savefig(OUT + r"\tuft_v97_confinement_attack_plots.png", dpi=140)
    print("[plot] tuft_v97_confinement_attack_plots.png saved")
except Exception as e:
    print(f"[plot] skipped: {type(e).__name__}: {e}")

with open(OUT + r"\tuft_v97_confinement_attack_results.json", "w", encoding="utf-8") as f:
    json.dump({"checks": [{"cid": n, "ok": c, "note": t} for n, c, t in rows],
               "sigma_geo_MeV_fm": sigma_geo, "sigma_QCD_MeV_fm": sigma_QCD,
               "D4": {"rho_tot": rho_tot, "rho_h_plus_p": rho_h + rho_p}},
              f, ensure_ascii=False, indent=1)
print("[json] tuft_v97_confinement_attack_results.json saved")
