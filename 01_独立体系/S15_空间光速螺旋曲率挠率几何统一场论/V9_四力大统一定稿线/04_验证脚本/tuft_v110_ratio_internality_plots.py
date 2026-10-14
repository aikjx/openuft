# -*- coding: utf-8 -*-
# V9.32 组合比值内生集完备性审计配图（三面板）
import json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

fp = r"C:\Windows\Fonts\msyh.ttc"
font_manager.fontManager.addfont(fp)
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

R = json.load(open(r"D:\a10\aikjx\code\my_lib\tuft_v110_ratio_internality_audit_results.json", encoding="utf-8"))
fig, axes = plt.subplots(1, 3, figsize=(15, 5.2))

# 面板 A：本源参数外输来源
ax = axes[0]
labels = ["q_G", "q_EM", "q_W", "q_pi", "lambda_W", "lambda_pi", "s"]
vals = [1, 1, 1, 1, 1, 1, 0]  # 1=含外输常数, 0=结构性内生
cols = ["#d62728" if v else "#2ca02c" for v in vals]
bars = ax.bar(labels, [1]*7, color=cols, width=0.55)
ax.set_ylim(0, 1.3)
ax.set_yticks([0, 1]); ax.set_yticklabels(["内生", "外输"])
ax.set_title("A 组：本源参数外输来源\n5/6 含外输常数（仅 s 符号内生）")
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, 1.08, "外输" if v else "内生", ha="center", fontsize=9)
ax.grid(axis="y", alpha=0.25)

# 面板 B：6 对力强比（log10）
ax = axes[1]
pairs = R["B"]["pair_ratios"]
names = [p["pair"] for p in pairs]
logs = [math.log10(p["ratio"]) for p in pairs]
ax.barh(names, logs, color="#1f77b4", height=0.5)
ax.set_xlabel("log10(力强比)")
ax.set_title("B 组：两两力强比全矩阵\n全部=荷比平方，含至少一个外输常数")
for i, l in enumerate(logs):
    ax.text(l + (0.1 if l >= 0 else -0.5), i, "%.2g" % pairs[i]["ratio"], va="center", fontsize=8)
ax.grid(axis="x", alpha=0.25)

# 面板 C：内生/外输判定（比值族）
ax = axes[2]
cats = ["力强比\n(6 对)", "几何比值\n(alpha/m)", "严格内生\n比值集"]
vals2 = [6, 5, 0]
bars = ax.bar(cats, vals2, color=["#ff7f0e", "#ff7f0e", "#d62728"], width=0.5)
ax.set_ylabel("条目数")
ax.set_title("C/D 组：完备性判定\n严格内生比值集 = 空集")
for b, v in zip(bars, vals2):
    ax.text(b.get_x()+b.get_width()/2, v+0.1, str(v), ha="center", fontsize=11)
ax.set_ylim(0, 7.5)
ax.text(0.5, 7.0, "全部含外输常数\n(alpha/G/G_F/f/m/hbar/c)", ha="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", fc="#fee", ec="#f88", alpha=0.9))
ax.grid(axis="y", alpha=0.25)

fig.suptitle("V9.32 组合比值内生集完备性审计：严格内生比值集=空集，B03 最终形态=常数全集+方向结构+q 结构剩余自由度", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(r"D:\a10\aikjx\code\my_lib\tuft_v110_ratio_internality_plots.png", dpi=130)
print("plot saved")
