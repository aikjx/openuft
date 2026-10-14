# -*- coding: utf-8 -*-
# V9.36 合流配图（三面板）：A 单方程三要素 / B 四力力程曲线 / C SM 对照判定
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
fp = r"C:\Windows\Fonts\msyh.ttc"
font_manager.fontManager.addfont(fp)
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

HBARC = 197.3269804
fig, axes = plt.subplots(1, 3, figsize=(15, 5.2))

# A：单方程结构
ax = axes[0]
ax.axis("off")
ax.text(0.5, 0.84, "力的大统一方程（单方程封闭式）", ha="center", fontsize=13, fontweight="bold")
ax.text(0.5, 0.64, "F(r) = -hbar*c*(s1*s2*q1*q2)*[(1/r+1/L)*e^(-r/L)/r^2]*rhat",
        ha="center", fontsize=11, family="DejaVu Sans")
ax.text(0.5, 0.44, "|F| = hbar*c*|q1q2|*(1/r+1/L)*e^(-r/L)/r^2", ha="center", fontsize=10, family="DejaVu Sans")
ax.text(0.5, 0.32, "方向 rhat 径向（s 定吸斥）", ha="center", fontsize=10)
ax.text(0.5, 0.20, "距离 L = hbar/(mc)（m=0 长程、m>0 有限）", ha="center", fontsize=10)
ax.text(0.5, 0.05, "四力 = 同一方程 + 参数表实例", ha="center", fontsize=11, color="#b00")
ax.set_title("A 组：单方程封闭式\n三要素（大小/方向/距离）单方程导出")

# B：四力力程曲线 log-log
ax = axes[1]
r = [10**(x/100.0) for x in range(-300, 301)]
qG, qE, qW, qPi = 938.27208816/1.220890e22, math.sqrt(0.0072973525693), 0.065116, 0.0204
lamW, lamPi = HBARC/80377.0, HBARC/134.9768
def F(q1, q2, lam, rr):
    if lam is None:
        return HBARC*q1*q2/(rr*rr)
    return HBARC*q1*q2*(1/rr+1/lam)*math.exp(-rr/lam)/(rr*rr)
for qq, lam, lab, ls in [(qG, None, "引力 (1/r2)", "-"), (qE, None, "电磁 (1/r2)", "-"),
                          (qW, lamW, "弱力 (L=2.46e-3 fm)", "--"), (qPi, lamPi, "剩余强力 (L=1.46 fm)", "--")]:
    ax.loglog(r, [F(qq, qq, lam, x) for x in r], label=lab, lw=2, ls=ls)
ax.axvline(lamW, color="gray", ls=":", lw=1)
ax.axvline(lamPi, color="gray", ls=":", lw=1)
ax.set_xlabel("距离 r (fm)")
ax.set_ylabel("|F| (MeV/fm)")
ax.set_title("B 组：四力力程曲线（log-log）\n长程 1/r2 vs 指数衰减力程")
ax.legend(fontsize=8)
ax.grid(alpha=0.3, which="both")

# C：SM 对照判定
ax = axes[2]
cats = ["TUFT 单方程\nvs SM 势形层", "SM 内生层\n(TUFT 缺失)", "新预言\n(TUFT)"]
vals = [1, 0, 0]
bars = ax.bar(cats, vals, color=["#2ca02c", "#d62728", "#7f7f7f"], width=0.5)
ax.set_ylim(-0.2, 1.4); ax.set_yticks([0, 1]); ax.set_yticklabels(["FAIL/0", "PASS"])
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v+0.06, "PASS" if v else "FAIL/0", ha="center", fontsize=10)
ax.set_title("C 组：判定\nTUFT = SM 低能势形层子集（子集 PASS）\nSM 规范-旋量-Higgs 层全缺失（FAIL）")
ax.text(0.5, 1.28, "FE/FG=1.2356e36 偏差0 | SM 比值偏差0.02%", ha="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", fc="#efe", ec="#8b8"))

fig.suptitle("V9.36 单方程封闭式与 SM 对照合流：力的大统一方程=SM 低能势形层参数化投影", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(r"D:\a10\aikjx\code\my_lib\tuft_v112_113_merge_plots.png", dpi=130)
print("plot saved")
