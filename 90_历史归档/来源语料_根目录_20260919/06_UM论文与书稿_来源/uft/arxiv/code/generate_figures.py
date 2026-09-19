\
"""Generate figures for the paper."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)

def helix_figure():
    """Fig 1: 3D helix structure."""
    theta = np.linspace(0, 6*np.pi, 500)
    kappa = 3.162e-4
    tau = 2.308e-6
    alpha = tau/kappa

    R = 3.162e3  # scaled for visibility
    ax_advance = alpha / kappa  # scaled

    x = R * np.cos(theta)
    y = R * np.sin(theta)
    z = ax_advance * theta / 1000  # scale down

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, 'b-', lw=1.5, label='Helix')
    ax.scatter([0], [0], [0], color='red', s=50, label='Axis')
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_title(f"Light Helix Structure\nR=1/kappa=3162m, alpha=tau/kappa=1/137")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "helix_geometry.pdf"), dpi=150)
    plt.savefig(os.path.join(OUT, "helix_geometry.png"), dpi=150)
    print("Saved helix_geometry.pdf")
    plt.close()

def coupling_figure():
    """Fig 2: Gauge coupling ratios comparison."""
    ratios = ["alpha_EM", "alpha_W", "alpha_S"]
    framework = [1/128, 4/128, 15/128]
    # Use alpha_exp for EM, alpha_W_exp, alpha_S_exp for others
    # E10 CRITICAL: use M_Z-scale INDEPENDENT values consistently.
    # alpha_EM(M_Z)=1/127.955, alpha_2(M_Z)=0.0338 (NOT 4*alpha_EM=0.03106, circular)
    # alpha_S(M_Z)=0.1179. All at M_Z scale for valid comparison.
    experiment = [1/127.955, 0.0338, 0.1179]
    # Normalize to same base
    exp_norm = [experiment[0], experiment[1], experiment[2]]
    # Normalize so alpha_EM = 1 in both
    f_norm = [f/experiment[0] for f in framework]
    e_norm = [1.0, experiment[1]/experiment[0], experiment[2]/experiment[0]]

    x = np.arange(len(ratios))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width/2, f_norm, width, label="Framework (15:4:1)", color="steelblue")
    ax.bar(x + width/2, e_norm, width, label="Experiment", color="coral")
    ax.set_ylabel("Normalized coupling")
    ax.set_title("Gauge Coupling Ratios: Framework vs Experiment")
    ax.set_xticks(x)
    ax.set_xticklabels(ratios)
    ax.legend()
    ax.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "coupling_ratios.pdf"), dpi=150)
    plt.savefig(os.path.join(OUT, "coupling_ratios.png"), dpi=150)
    print("Saved coupling_ratios.pdf")
    plt.close()

def forces_figure():
    """Fig 3: Four perpendicular modes."""
    fig, ax = plt.subplots(figsize=(6, 6))
    circle = plt.Circle((0, 0), 1, fill=False, color='gray', lw=2)
    ax.add_patch(circle)
    # Radial
    ax.annotate("", xy=(1.3, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="blue", lw=2))
    ax.text(1.4, 0, "EM\n(radial)", fontsize=9, va="center")
    # Tangential
    ax.annotate("", xy=(0.7, 0.7), xytext=(0.5, 0.5),
                arrowprops=dict(arrowstyle="->", color="red", lw=2))
    ax.text(0.9, 0.95, "Strong\n(tang.)", fontsize=9)
    # Chiral (arrow on circumference)
    ax.annotate("", xy=(0, 1.3), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="green", lw=2))
    ax.text(-0.2, 1.4, "Weak\n(chiral)", fontsize=9)
    # Axial (out of page)
    ax.text(0, 0, "+", fontsize=20, ha="center", va="center", color="purple")
    ax.text(-0.15, -0.15, "Gravity\n(axial)", fontsize=9)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Four Perpendicular Modes\n(Cross-section view)", fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "four_forces.pdf"), dpi=150)
    plt.savefig(os.path.join(OUT, "four_forces.png"), dpi=150)
    print("Saved four_forces.pdf")
    plt.close()

if __name__ == "__main__":
    print("Generating figures...")
    helix_figure()
    coupling_figure()
    forces_figure()
    print("All figures generated in figures/")
