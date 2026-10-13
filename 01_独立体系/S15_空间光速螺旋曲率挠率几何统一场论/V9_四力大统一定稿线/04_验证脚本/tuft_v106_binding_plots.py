# -*- coding: utf-8 -*-
"""V9.24 束缚态与结构形成审计配图（四面板）"""
import json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 中文字体（msyh.ttc 回退）
for fp in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyhbd.ttc"]:
    try:
        font_manager.fontManager.addfont(fp)
        break
    except Exception:
        pass
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

d = json.load(open(r"D:\a10\aikjx\code\my_lib\tuft_v106_binding_audit_results.json", encoding="utf-8"))
fig, axes = plt.subplots(2, 2, figsize=(13.5, 10))

# ---- A：库仑变分能 ----
ax = axes[0, 0]
aa = [i / 100 for i in range(20, 250, 2)]
Ea = [0.5 * a * a - a for a in aa]
ax.plot(aa, Ea, lw=2, color="#1f77b4", label="E_var(alpha)=alpha^2/2 - alpha (hartree)")
ax.axhline(-0.5, color="#d62728", ls="--", lw=1.5,
           label="E_1 精确 = -0.5 hartree = -13.6057 eV")
ax.plot([1.0], [-0.5], "o", ms=8, color="#d62728", zorder=5)
ax.annotate("alpha=1: 试函数=精确基态\n偏差 1e-6 (PASS)",
            xy=(1.0, -0.5), xytext=(0.55, -0.85),
            arrowprops=dict(arrowstyle="->", color="#333333"))
ax.set_xlabel("alpha")
ax.set_ylabel("E_var (hartree)")
ax.set_title("A 组：库仑极限复现氢原子基态")
ax.legend(loc="upper right", fontsize=8)
ax.grid(alpha=0.3)

# ---- B：汤川临界耦合 ----
ax = axes[0, 1]
kt = [b["kappa_tilde"] for b in d["B_yukawa"]["B_scan"]]
Em = [b["E_var_min"] for b in d["B_yukawa"]["B_scan"]]
ax.plot(kt, Em, "o-", lw=2, color="#2ca02c", label="E_var,min(kappa_tilde)")
ax.axhline(0, color="#333333", ls=":", lw=1)
ax.axvline(1.0, color="#d62728", ls="--", lw=1.5,
           label="kappa_tilde_c >= 1.0 (变分下界)")
ax.fill_between([0.4, 1.0], [-50], [5], color="#d62728", alpha=0.08,
                label="零束缚区 (kappa_tilde<1.0)")
ax.annotate("kappa_tilde=1.5 起有束缚\n(E_var,min<0)", xy=(1.5, -0.177),
            xytext=(3.2, -3.5), arrowprops=dict(arrowstyle="->", color="#333333"))
ax.set_xlabel("kappa_tilde = 2*mu*lambda*q^2/(hbar*c)")
ax.set_ylabel("E_var,min")
ax.set_title("B 组：汤川势临界耦合（有限束缚态）")
ax.legend(loc="lower right", fontsize=8)
ax.grid(alpha=0.3)

# ---- C：结构层级 ----
ax = axes[1, 0]
names = ["引力\nlambda=inf", "电磁\nlambda=inf", "剩余强力\nlambda_pi=1.46 fm", "弱力\nlambda_W=2.5e-3 fm"]
nb = ["无限层级\n(星系->原子)", "无限量子谱\n(E_n=-13.6/n^2)", "有限核素表\n(模板层零束缚)", "零束缚\n(无结构)"]
vals = [1e12, 1e6, 1.0, 1e-6]
cols = ["#ff7f0e", "#1f77b4", "#2ca02c", "#d62728"]
bars = ax.bar(range(4), [math.log10(v) for v in vals], color=cols, alpha=0.85)
ax.set_xticks(range(4))
ax.set_xticklabels(names, fontsize=8)
ax.set_ylabel("log10(束缚态数标度)")
ax.set_title("C 组：结构层级从力程谱涌现")
for b, n in zip(bars, nb):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.25, n,
            ha="center", fontsize=8.5)

# ---- D：氘核 no-go ----
ax = axes[1, 1]
D = d["D_deuteron"]
ax.axvspan(0, 1.0, color="#d62728", alpha=0.10, label="零束缚区 (kappa_tilde<1.0)")
ax.axvline(1.0, color="#d62728", ls="--", lw=1.5, label="kappa_tilde_c = 1.0")
ax.axvline(D["kappa_ope"], color="#1f77b4", lw=3, label="kappa_tilde_OPE = 0.0029")
ax.axvline(D["kappa_eff_deuteron"], color="#2ca02c", lw=3,
           label="kappa_tilde_eff = 1.38 (氘核深度要求)")
ax.annotate("耦合差 ~480 倍\n(no-go)", xy=(math.sqrt(D["kappa_ope"] * D["kappa_eff_deuteron"]), 0.5),
            xytext=(3.0, 0.55), arrowprops=dict(arrowstyle="->", color="#333333"), fontsize=9)
ax.text(0.003, 0.42, "OPE 零束缚态\n模板内氘核不存在", fontsize=8.5, color="#1f77b4")
ax.set_xscale("log")
ax.set_xlim(1e-3, 1e2)
ax.set_ylim(0, 1)
ax.set_xlabel("kappa_tilde")
ax.set_yticks([])
ax.set_title("D 组：氘核 no-go（方向缺失的动力学后果）")
ax.legend(loc="upper left", fontsize=8)
ax.grid(alpha=0.3, axis="x")

fig.suptitle("V9.24 束缚态与结构形成审计：库仑复现 / 汤川临界 / 结构层级 / 氘核 no-go",
             fontsize=13, y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.97])
fig.savefig(r"D:\a10\aikjx\code\my_lib\tuft_v106_binding_plots.png", dpi=140)
print("saved ok")
