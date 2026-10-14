# -*- coding: utf-8 -*-
# V9.33 判别性预言空间穷举配图（三面板）
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

fp = r"C:\Windows\Fonts\msyh.ttc"
font_manager.fontManager.addfont(fp)
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

R = json.load(open(r"D:\a10\aikjx\code\my_lib\tuft_v111_predictive_closure_results.json", encoding="utf-8"))
fig, axes = plt.subplots(1, 3, figsize=(15, 5.2))

# 面板 A：预言空间 17 类 × 7 扇区
ax = axes[0]
sectors = R["A"]["sectors"]
names = list(sectors.keys())
counts = [len(v) for v in sectors.values()]
cols = plt.cm.tab10(range(len(names)))
bars = ax.bar(names, counts, color=cols, width=0.55)
ax.set_ylabel("预言类数")
ax.set_title("A 组：预言空间 P = 17 类 × 7 扇区\n（38 章全扫描登记）")
for b, c in zip(bars, counts):
    ax.text(b.get_x()+b.get_width()/2, c+0.1, str(c), ha="center", fontsize=10)
ax.set_ylim(0, 5.5)
ax.tick_params(axis="x", rotation=20)
ax.grid(axis="y", alpha=0.25)

# 面板 B：否决原因分布
ax = axes[1]
reasons = R["C"]["reason_breakdown"]
labels = list(reasons.keys())
vals = list(reasons.values())
bars = ax.bar(labels, vals, color=["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4"], width=0.5)
ax.set_ylabel("预言类数")
ax.set_title("B/C 组：否决原因分布（17 类全否决）\n判别性预言 = 0 类")
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v+0.1, str(v), ha="center", fontsize=11)
ax.set_ylim(0, 19)
ax.grid(axis="y", alpha=0.25)

# 面板 C：判别性计数 + 覆盖论证示意
ax = axes[2]
cats = ["可测断言\n(17 类)", "判别性\n预言", "覆盖缺口\n(超出 P)"]
vals2 = [17, 0, 0]
bars = ax.bar(cats, vals2, color=["#1f77b4", "#d62728", "#7f7f7f"], width=0.5)
for b, v in zip(bars, vals2):
    ax.text(b.get_x()+b.get_width()/2, v+0.3, str(v), ha="center", fontsize=11)
ax.set_ylim(0, 20)
ax.set_title("D 组：完备性闭合\n判别性=0 类（枚举证明）\n覆盖缺口=0（战役闭合）")
ax.text(0.5, 18.6, "17 类无一四元全 1\n(U,I,M,N) 判据矩阵", ha="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", fc="#efe", ec="#8b8", alpha=0.9))
ax.grid(axis="y", alpha=0.25)

fig.suptitle("V9.33 判别性预言空间穷举：判别性预言=0 类由清单法升级为四元判据枚举证明", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(r"D:\a10\aikjx\code\my_lib\tuft_v111_predictive_closure_plots.png", dpi=130)
print("plot saved")
