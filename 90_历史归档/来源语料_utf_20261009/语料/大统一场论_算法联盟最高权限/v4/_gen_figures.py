# -*- coding: utf-8 -*-
"""R5 公式可视化：螺旋轨迹 / Xi unit circle / force hierarchy / dark matter.
算法联盟 ROOT 最高权限 · V4 融合版 · 47 R5 产物。
输出：v4/figures/（自动创建）。标题用英文以规避 CJK 字体缺失。
"""
import os, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

OUT = os.path.dirname(os.path.abspath(__file__)) + "/figures"
os.makedirs(OUT, exist_ok=True)
plt.rcParams["mathtext.fontset"] = "dejavusans"
plt.rcParams["font.family"] = "DejaVu Sans"

ALPHA = 1.0/137.035999084
RHO = 1.0/np.sqrt(1+ALPHA**2)
B = ALPHA*RHO
R = np.sqrt(RHO**2+B**2)

# ---------- Fig1: helix ----------
theta = np.linspace(0, 8*np.pi, 2000)
x = RHO*np.cos(theta); y = RHO*np.sin(theta); z = B*theta
fig = plt.figure(figsize=(6,5))
ax = fig.add_subplot(111, projection="3d")
ax.plot(x, y, z, lw=1.0, color="#1f77b4")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z axis (b theta)")
ax.set_title(r"Fig.1 Helical world-line  $r(\theta)=(\rho\cos\theta,\rho\sin\theta,b\theta)$")
ax.view_init(elev=20, azim=45)
fig.tight_layout(); fig.savefig(OUT+"/fig1_helix.png", dpi=130); plt.close(fig)

# ---------- Fig2: Xi unit circle ----------
fig, ax = plt.subplots(figsize=(5,5))
ax.add_patch(Circle((0,0),1, fill=False, color="gray", ls="--"))
ax.quiver(0,0, RHO, B, angles="xy", scale_units="xy", scale=1, color="#d62728",
          width=0.02, label=r"$\tilde\kappa+i\tilde\tau$ (electron)")
ax.scatter([RHO],[B], color="#d62728", zorder=5)
ax.scatter([1/np.sqrt(2)],[1/np.sqrt(2)], color="#2ca02c", zorder=5,
           label=r"Planck equal $\kappa=\tau=1/\sqrt{2}$")
ax.scatter([1.0],[0.0], color="#9467bd", zorder=5, label=r"dark matter pure-$\kappa$ ($\tilde\tau=0$)")
ax.set_xlim(0,1.1); ax.set_ylim(0,1.1)
ax.set_xlabel(r"$\tilde\kappa$"); ax.set_ylabel(r"$\tilde\tau$")
ax.set_title(r"Fig.2 Complex curvature field $\Xi=\kappa+i\tau$ unit circle")
ax.legend(fontsize=8, loc="lower right")
fig.tight_layout(); fig.savefig(OUT+"/fig2_xi_circle.png", dpi=130); plt.close(fig)

# ---------- Fig3: force hierarchy ----------
forces = ["Gravity G", "EM E", "Weak W", "Strong S"]
alpha_i = np.array([3.85e-45, 1/137.0, 1/137.0/4.0, 1.0])
fig, ax = plt.subplots(figsize=(6,4))
bars = ax.bar(forces, alpha_i, color=["#8c564b","#1f77b4","#ff7f0e","#2ca02c"])
ax.set_yscale("log")
ax.set_ylabel(r"relative coupling $\alpha_i$ ($\propto \hbar c/r^2$)")
ax.set_title("Fig.3 Four-force strength hierarchy (geometric)")
for b,v in zip(bars, alpha_i):
    ax.text(b.get_x()+b.get_width()/2, v*1.5, f"{v:.1e}", ha="center", fontsize=8)
fig.tight_layout(); fig.savefig(OUT+"/fig3_forces.png", dpi=130); plt.close(fig)

# ---------- Fig4: dark matter free-streaming ----------
m_DM = 1.68
m_vals = np.array([0.1, 0.5, 1.68, 5.0, 50.0])
lam = 1.0/m_vals
fig, ax = plt.subplots(figsize=(6,4))
ax.plot(m_vals, lam, "-o", color="#9467bd")
ax.axvline(m_DM, color="red", ls="--", lw=1, label=f"prediction m_DM={m_DM} GeV")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"dark matter mass $m_{\rm DM}$ [GeV]")
ax.set_ylabel(r"free-streaming scale $\lambda_{\rm fs}\sim 1/m$ [a.u.]")
ax.set_title("Fig.4 Dark matter free-streaming vs mass (pure-kappa phase)")
ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(OUT+"/fig4_darkmatter.png", dpi=130); plt.close(fig)

print("OK figures ->", OUT)
print(sorted(os.listdir(OUT)))
