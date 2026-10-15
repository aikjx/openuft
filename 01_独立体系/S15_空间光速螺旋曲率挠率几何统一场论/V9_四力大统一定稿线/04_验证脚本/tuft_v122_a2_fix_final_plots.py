# -*- coding: utf-8 -*-
# V9.45 A2 修复最终化配图（三面板）：A 路径族唯一性 / B 三粒子恒等 / C 口径三表+判定
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
fp = r"C:\Windows\Fonts\msyh.ttc"
font_manager.fontManager.addfont(fp)
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

MEV_PER_SEC = 1.5192675e21
c = 2.99792458e8
lP_m = 1.616255e-35
lP_fm = lP_m*1e15
fig, axes = plt.subplots(1, 3, figsize=(15, 5.2))

# A：路径族唯一性（路径 A/B -> 式 1）
ax = axes[0]
ax.axis("off")
ax.text(0.5, 0.95, "等价修复路径族唯一性定理", ha="center", fontsize=12, fontweight="bold", transform=ax.transAxes)
items = [
    ("路径 A（并行线 46.2）", "kappa~=lP*kappa, tau~=lP*tau\nowega=c*sqrt(kappa^2+tau^2)", "#1f77b4"),
    ("路径 B（VM 线）", "(omega*lP/c)^2 * lP^-2 = (omega/c)^2", "#ff7f0e"),
    ("修复目标唯一", "kappa^2+tau^2=(omega/c)^2 = TUFT L1\n不存在第三条量纲自洽修复", "#2ca02c"),
]
y = 0.78
for name, desc, col in items:
    ax.text(0.08, y, name, fontsize=10.5, fontweight="bold", color=col, transform=ax.transAxes)
    ax.text(0.08, y-0.13, desc, fontsize=9, color="#333", transform=ax.transAxes, family="monospace")
    y -= 0.26
ax.text(0.5, 0.05, "殊途同归：修复 = 回归（非突破）", ha="center", fontsize=10, transform=ax.transAxes,
        bbox=dict(boxstyle="round,pad=0.3", fc="#efe", ec="#2ca02c"))
ax.set_title("A 组：路径族唯一性")

# B：三粒子 log10 柱（修复版 vs 原A2）
ax = axes[1]
parts = ["电子", "质子", "pi0"]
lhs = [math.log10((m*MEV_PER_SEC/c)**2) for m in [0.51099895, 938.27208816, 134.9768]]
orig = [math.log10((m*MEV_PER_SEC*lP_m/c)**2) for m in [0.51099895, 938.27208816, 134.9768]]
x = range(3)
w = 0.35
b1 = ax.bar([i-w/2 for i in x], lhs, w, label="修复版 (w/c)^2", color="#2ca02c")
b2 = ax.bar([i+w/2 for i in x], orig, w, label="原 A2 (w*lP/c)^2", color="#d62728")
for i in x:
    ax.text(i-w/2, lhs[i]+1, "%.1f" % lhs[i], ha="center", fontsize=9)
    ax.text(i+w/2, orig[i]+1, "%.1f" % orig[i], ha="center", fontsize=9)
ax.set_xticks(list(x)); ax.set_xticklabels(parts)
ax.set_ylabel("log10 数值")
ax.set_title("B 组：三粒子机器精度闭环\n修复版=原 A2*lP^-2（比值=1/lP^2=3.828e69 恒等）")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# C：口径三表 + 判定
ax = axes[2]
ax.axis("off")
rows = [
    ("D1（V9.40）", "69.58 跨量纲伪失配", "表述不精确，结论成立", "#ff7f0e"),
    ("D2（并行线）", "19.79 dex 真实质量失配\nm_GAQ/m_e=6.187e19", "正确口径", "#1f77b4"),
    ("D3（本波）", "相对残差 0.0", "修复闭合", "#2ca02c"),
]
y = 0.88
for name, val, judge, col in rows:
    ax.text(0.05, y, name, fontsize=10.5, fontweight="bold", color=col, transform=ax.transAxes)
    ax.text(0.05, y-0.12, val, fontsize=8.5, color="#333", transform=ax.transAxes)
    ax.text(0.7, y-0.02, judge, fontsize=9, color=col, transform=ax.transAxes)
    y -= 0.22
ax.text(0.5, 0.16, "B02/B03 之墙独立于 A2 版本（FAIL 维持）", ha="center", fontsize=9.5, transform=ax.transAxes,
        bbox=dict(boxstyle="round,pad=0.3", fc="#fdd", ec="#d62728"))
ax.text(0.5, 0.03, "总账不变：实现 50% / 预言 20%；判别性预言=0 类", ha="center", fontsize=9, transform=ax.transAxes)
ax.set_title("C 组：口径三表裁定与判定")

fig.suptitle("V9.45 A2 修复最终化：唯一量纲正确版 = TUFT L1；修复=回归非突破（第五十章）", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(r"D:\a10\aikjx\code\my_lib\tuft_v122_a2_fix_final_plots.png", dpi=130)
print("plot saved")
