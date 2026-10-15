# -*- coding: utf-8 -*-
# V9.46 单方程×实验数据一致性矩阵配图（三面板）
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
fp = r"C:\Windows\Fonts\msyh.ttc"
font_manager.fontManager.addfont(fp)
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

fig, axes = plt.subplots(1, 3, figsize=(15, 5.2))

# A：一致性矩阵 10 行判定（绿=继承 PASS 红=FAIL）
ax = axes[0]
labels = ["库仑 1/r^2", "牛顿 1/r^2", "氢原子 E1", "GW 波速", "EHT 阴影",
          "g-2 电子", "形状因子", "氘核束缚", "Cornell 势", "mu 衰变"]
vals = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
colors = ["#2ca02c" if v else "#d62728" for v in vals]
ax.barh(range(len(labels)), [1]*len(labels), color=colors, edgecolor="k", linewidth=0.4)
for i, lab in enumerate(labels):
    ax.text(1.01, i, lab, va="center", fontsize=8.5)
ax.set_yticks([])
ax.set_xlim(0, 1.7)
ax.set_xticks([])
ax.text(0.5, -1.1, "继承 PASS=5（势形层，参数外输）  FAIL=5（TUFT 独有结构）",
        ha="center", fontsize=9, transform=ax.transAxes)
ax.set_title("A 组：一致性矩阵判定（10 项）\n一致=继承、不一致=独有")

# B：四力势形 log-log（继承性展示）
ax = axes[1]
r = [10**x for x in [0, 0.5, 1, 1.5, 2]]  # fm
alpha_hbarc = 1.4399645     # MeV*fm
newton_pp = 1.1654e-36      # MeV*fm
lam_pi = 1.4619             # fm
lam_W = 2.4550e-3           # fm
xs = [10**x for x in [math.log10(1e-2), math.log10(1e-1), math.log10(1), math.log10(1e1), math.log10(1e2)]]
for name, coeff, lam, col in [("库仑 1/r^2", alpha_hbarc, 1e12, "#2ca02c"),
                              ("牛顿 1/r^2", newton_pp, 1e12, "#1f77b4"),
                              ("汤川(pi) Yukawa", 0.0204*alpha_hbarc*1e0, lam_pi, "#ff7f0e"),
                              ("汤川(W)", alpha_hbarc*0.0651, lam_W, "#9467bd")]:
    yy = [coeff*(1/x + 1/lam)*math.exp(-x/lam)/x for x in xs]
    ax.loglog(xs, yy, "-o", ms=3, label=name, color=col)
ax.set_xlabel("r [fm]")
ax.set_ylabel("F(r) [MeV/fm]")
ax.set_title("B 组：单方程四力势形（继承性）\n同一方程+参数表实例（V9.34）")
ax.legend(fontsize=7.5)
ax.grid(alpha=0.3, which="both")

# C：结构定理三件套 + 判定
ax = axes[2]
ax.axis("off")
items = [
    ("方程封闭", "单方程封闭式 PASS（V9.34/36）", "#2ca02c"),
    ("无自由参数", "N_p=0，chi2 恒 0（V9.38）", "#2ca02c"),
    ("一致性=继承", "5 继承 PASS / 5 FAIL / 判别 0（本轮）", "#ff7f0e"),
]
y = 0.86
for name, desc, col in items:
    ax.text(0.06, y, name, fontsize=10.5, fontweight="bold", color=col, transform=ax.transAxes)
    ax.text(0.06, y-0.11, desc, fontsize=8.5, color="#333", transform=ax.transAxes)
    y -= 0.17
ax.annotate("", xy=(0.94, 0.42), xytext=(0.94, 0.72),
            arrowprops=dict(arrowstyle="->", lw=1.5), transform=ax.transAxes)
ax.text(0.5, 0.30, "新的一致需要新结构\n（V9.31 结构定理：已知几何结构族内不存在）",
        ha="center", fontsize=9, transform=ax.transAxes,
        bbox=dict(boxstyle="round,pad=0.3", fc="#fdd", ec="#d62728"))
ax.text(0.5, 0.10, "判别性预言=0 类维持；总账不变：实现 50% / 预言 20%",
        ha="center", fontsize=8.5, transform=ax.transAxes)
ax.set_title("C 组：一致性结构定理")

fig.suptitle("V9.46 单方程×实验数据一致性矩阵：势形层继承一致、判别性层零一致（第五十一章）", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(r"D:\a10\aikjx\code\my_lib\tuft_v123_exp_consistency_plots.png", dpi=130)
print("plot saved")
