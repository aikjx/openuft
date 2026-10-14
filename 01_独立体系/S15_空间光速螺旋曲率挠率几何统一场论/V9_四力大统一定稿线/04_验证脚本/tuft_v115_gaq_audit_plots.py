# -*- coding: utf-8 -*-
# V9.40 GAQ 审计配图（三面板）：A 公理三关 / B A2 量纲断裂 / C 72 条普查
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
fp = r"C:\Windows\Fonts\msyh.ttc"
font_manager.fontManager.addfont(fp)
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

hbar = 1.054571817e-34
c = 299792458.0
m_e = 9.1093837015e-31
lP = 1.616255e-35
omega_e = m_e*c*c/hbar
fig, axes = plt.subplots(1, 3, figsize=(15, 5.2))

# A：A1-A4 三关判定
ax = axes[0]
ax.axis("off")
rows = [
    ("A1  v=c（全域光速约束）", "PASS（=TUFT 公设一，继承）", "#2ca02c"),
    ("A2  kappa^2+tau^2=(w*lP/c)^2", "FAIL（量纲断裂：L^-2 vs 无量纲）", "#d62728"),
    ("A3  32 维流形", "OPEN（旋量维数 65536 vs SM ~60 无对齐）", "#ff7f0e"),
    ("A4  本源几何化（50 常数反向生成）", "FAIL/OPEN（与已证 B02/B03 冲突，无机制）", "#d62728"),
]
y = 0.9
for name, verdict, col in rows:
    ax.text(0.04, y, name, fontsize=10.5, fontweight="bold", color=col, transform=ax.transAxes)
    ax.text(0.04, y-0.09, verdict, fontsize=9.5, color="#333", transform=ax.transAxes)
    y -= 0.22
ax.set_title("A 组：GAQ 公理 A1–A4 三关判定\n（量纲+循环+断裂点，家族七）")

# B：A2 数值失配（log 柱）
ax = axes[1]
names = ["TUFT L1\n(w/c)^2", "GAQ A2\n(w*lP/c)^2"]
vals = [math.log10((omega_e/c)**2), math.log10((omega_e*lP/c)**2)]
bars = ax.bar(names, vals, color=["#2ca02c", "#d62728"], width=0.5)
ax.set_ylabel("log10 数值")
ax.set_title("B 组：A2 vs TUFT L1（电子）\n失配 69.6 个数量级；且 A2 侧无量纲")
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v+0.5, "%.1f" % v, ha="center", fontsize=10)
ax.text(0.5, 2, "量纲：L^-2 vs 无量纲 —— 断裂", ha="center", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", fc="#fdd", ec="#d62728"))

# C：72 条普查
ax = axes[2]
cats = ["P\n（已有 TUFT\n审计维持）", "O\n（OPEN/超\n可验证域）", "C\n（冲突/\n无法执行）"]
vals = [21, 37, 1]
bars = ax.bar(cats, vals, color=["#2ca02c", "#ff7f0e", "#7f7f7f"], width=0.5)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v+0.6, str(v), ha="center", fontsize=12, fontweight="bold")
ax.set_ylabel("攻击线条数")
ax.set_title("C 组：72 条攻击线普查\n无一条推翻 TUFT 判定；断裂点 4 处全 OPEN")

fig.suptitle("V9.40 GAQ-UFT V50 公理地基三关审计：A2 量纲断裂 69.6 量级，外部框架不能替代 TUFT", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(r"D:\a10\aikjx\code\my_lib\tuft_v115_gaq_audit_plots.png", dpi=130)
print("plot saved")
