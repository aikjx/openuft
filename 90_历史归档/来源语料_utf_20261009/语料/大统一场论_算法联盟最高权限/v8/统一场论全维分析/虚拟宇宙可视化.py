#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""虚拟宇宙可视化 —— 为本框架 v8-v18 已证定律生成图片（整理优化精算验证的可视化层）

生成 4 张 PNG（图表文字用英文以兼容无 CJK 字体环境）：
  figures/fig_forces.png    引力/电磁逆平方 + 弱/强(剩余)力短程截断
  figures/fig_cosmology.png Friedmann a(t) 膨胀 + 哈勃流 v=H·r
  figures/fig_charges.png   拓扑电荷量子化格 q=(k/3)e
  figures/fig_universe.png  虚拟宇宙 N 体快照（引力 + 宇宙学膨胀的结构形成）

诚实声明：图片展示的是『框架预测的现象』，非真实宇宙观测图。
"""
from __future__ import annotations
import sys, os, json, math
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

# ---------- 框架常数（与 虚拟宇宙模拟器.py 一致）----------
G    = 6.67430e-11
C    = 2.99792458e8
HBAR = 1.054571817e-34
E    = 1.602176634e-19
ALPHA = 1.0/137.035999084
HC   = HBAR * C
K_E  = ALPHA * HC / E**2
LAM_W  = HBAR / (80.379e9 * E / C**2 * C)   # weak range ~2.5e-18 m
LAM_PI = HBAR / (134.9768e6 * E / C**2 * C) # strong(residual) range ~1.413e-15 m
H0 = 2.2e-18
OMEGA_L = 0.689

# ---------- 力律（v10 已证）----------
def F_grav(r, m=1e3):
    return G * m * m / r**2
def F_em(r, q=1.0):
    return K_E * q * q / r**2
def F_yukawa(r, lam, q=1.0):
    return K_E * q * q * (1.0/r**2 + 1.0/(lam*r)) * math.exp(-r/lam)

# ---------- 图1：力律 ----------
def fig_forces():
    rs = np.logspace(-2, 3, 60)
    fig, ax = plt.subplots(2, 2, figsize=(11, 8))
    ax[0,0].loglog(rs, [F_grav(r) for r in rs], "b-", lw=2, label="gravity F=G m^2/r^2")
    ax[0,0].loglog(rs, [F_grav(rs[0])*(rs[0]/r)**2 for r in rs], "k--", alpha=.6, label="r^-2 ref")
    ax[0,0].set_title("Gravity: inverse-square law (v10/v15)")
    ax[0,0].set_xlabel("r / m"); ax[0,0].set_ylabel("F / N"); ax[0,0].legend(); ax[0,0].grid(True, which="both", ls=":")
    rs2 = np.logspace(-10, -6, 60)
    ax[0,1].loglog(rs2, [F_em(r) for r in rs2], "r-", lw=2, label="EM F=K_e q^2/r^2")
    ax[0,1].loglog(rs2, [F_em(rs2[0])*(rs2[0]/r)**2 for r in rs2], "k--", alpha=.6, label="r^-2 ref")
    ax[0,1].set_title("Electromagnetism: inverse-square law (v10)")
    ax[0,1].set_xlabel("r / m"); ax[0,1].set_ylabel("F / N"); ax[0,1].legend(); ax[0,1].grid(True, which="both", ls=":")
    rw = np.logspace(math.log10(0.01*LAM_W), math.log10(20*LAM_W), 60)
    ax[1,0].loglog(rw, [F_yukawa(r, LAM_W) for r in rw], "g-", lw=2)
    ax[1,0].axvline(LAM_W, color="k", ls="--", alpha=.6, label=f"lambda_W={LAM_W:.1e} m")
    ax[1,0].set_title("Weak force: Yukawa short-range (lambda_W~2.5e-3 fm)")
    ax[1,0].set_xlabel("r / m"); ax[1,0].set_ylabel("F / N"); ax[1,0].legend(); ax[1,0].grid(True, which="both", ls=":")
    rp = np.logspace(math.log10(0.01*LAM_PI), math.log10(20*LAM_PI), 60)
    ax[1,1].loglog(rp, [F_yukawa(r, LAM_PI) for r in rp], "m-", lw=2)
    ax[1,1].axvline(LAM_PI, color="k", ls="--", alpha=.6, label=f"lambda_pi={LAM_PI:.1e} m")
    ax[1,1].set_title("Strong(residual): Yukawa short-range (lambda_pi~1.4 fm)")
    ax[1,1].set_xlabel("r / m"); ax[1,1].set_ylabel("F / N"); ax[1,1].legend(); ax[1,1].grid(True, which="both", ls=":")
    fig.suptitle("Unified force law: four forces share Proca/Yukawa eq (v10)", fontsize=13)
    fig.tight_layout(rect=[0,0,1,0.96])
    p = os.path.join(FIGDIR, "fig_forces.png"); fig.savefig(p, dpi=130); plt.close(fig)
    return p

# ---------- 图2：宇宙学 ----------
def fig_cosmology():
    Om = 1 - OMEGA_L
    a = 1.0; t = 0.0; dt = 1e16; steps = 600
    ts, as_ = [0.0], [1.0]
    for _ in range(steps):
        H = H0 * math.sqrt(Om * a**-3 + OMEGA_L)
        a += H * a * dt; t += dt
        ts.append(t); as_.append(a)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    ax[0].plot(np.array(ts)/3.154e16, as_, "b-", lw=2)
    ax[0].set_title("Friedmann expansion a(t) (matter+Lambda, flat FRW) (v18 B01)")
    ax[0].set_xlabel("t / Gyr"); ax[0].set_ylabel("scale factor a(t)"); ax[0].grid(True, ls=":")
    rng = np.random.default_rng(0)
    R = rng.uniform(1e23, 5e24, 40)
    V = H0 * R
    ax[1].scatter(R, V, c="purple", s=20)
    rr = np.linspace(R.min(), R.max(), 50)
    ax[1].plot(rr, H0*rr, "k--", label=f"v=H r, H={H0:.1e}")
    ax[1].set_title("Hubble flow v = H r (v18 B06)")
    ax[1].set_xlabel("r / m"); ax[1].set_ylabel("v / (m/s)"); ax[1].legend(); ax[1].grid(True, ls=":")
    fig.tight_layout()
    p = os.path.join(FIGDIR, "fig_cosmology.png"); fig.savefig(p, dpi=130); plt.close(fig)
    return p

# ---------- 图3：电荷量子化 ----------
def fig_charges():
    k = np.arange(-6, 7)
    q = k / 3.0
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.stem(k, q, basefmt=" ")
    ax.axhline(0, color="k", lw=.8)
    ax.set_title("Topological charge quantization: q = (k/3) e  (v17 B01)")
    ax.set_xlabel("winding number k"); ax.set_ylabel("charge q (in units of e)")
    ax.set_xticks(k)
    ax.grid(True, axis="y", ls=":")
    for o in [0, 1/3, -1/3, 2/3, -2/3, 1, -1]:
        ax.scatter([0],[o], c="red", zorder=5)
    fig.tight_layout()
    p = os.path.join(FIGDIR, "fig_charges.png"); fig.savefig(p, dpi=130); plt.close(fig)
    return p

# ---------- 图4：虚拟宇宙 N 体快照 ----------
def fig_universe():
    rng = np.random.default_rng(1)
    N = 120
    q = rng.uniform(-1, 1, (N, 3)) * 50.0          # comoving coords (Mpc-scale, illustrative)
    qv = rng.normal(0, 5.0, (N, 3))
    m = np.ones(N)
    a = 1.0; dt = 1e15; steps = 400
    Om = 1 - OMEGA_L
    for _ in range(steps):
        H = H0 * math.sqrt(Om * a**-3 + OMEGA_L)
        acc = np.zeros((N, 3))
        for i in range(N):
            d = q - q[i]
            r2 = np.sum(d*d, axis=1) + 1e-2
            inv = 1.0 / (r2 * np.sqrt(r2))
            acc[i] = 4e3 * np.sum(d * (m*inv)[:, None], axis=0)
        qv += (-acc - 2*H*qv) * dt
        q += qv * dt
        a += H * a * dt
    phys = q * a
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")
    speed = np.sqrt(np.sum(qv*qv, axis=1))
    sc = ax.scatter(phys[:,0], phys[:,1], phys[:,2], c=speed, cmap="viridis", s=25)
    ax.set_title(f"Virtual-universe N-body snapshot (a={a:.1f}, gravity+expansion structure formation) (v18)")
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    fig.colorbar(sc, ax=ax, label="|v_pec|")
    fig.tight_layout()
    p = os.path.join(FIGDIR, "fig_universe.png"); fig.savefig(p, dpi=120); plt.close(fig)
    return p

def main():
    print("=" * 70)
    print("虚拟宇宙可视化 —— 生成框架 v8-v18 现象图片（图表英文以兼容字体）")
    print("=" * 70)
    paths = {}
    for name, fn in [("forces", fig_forces), ("cosmology", fig_cosmology),
                     ("charges", fig_charges), ("universe", fig_universe)]:
        p = fn()
        paths[name] = os.path.relpath(p, HERE)
        print(f"  [gen] {name:9} -> {paths[name]}")
    out = dict(visualization="虚拟宇宙可视化", framework="v8-v18", figures=paths,
               honest_note="图片展示框架预测的现象，非真实宇宙观测图")
    with open(os.path.join(HERE, "虚拟宇宙可视化_结果.json"), "w", encoding="utf-8") as fp:
        json.dump(out, fp, ensure_ascii=False, indent=2)
    print("\n结果已写入: 虚拟宇宙可视化_结果.json")
    print(f"图片目录: {os.path.relpath(FIGDIR, HERE)}/")

if __name__ == "__main__":
    main()
