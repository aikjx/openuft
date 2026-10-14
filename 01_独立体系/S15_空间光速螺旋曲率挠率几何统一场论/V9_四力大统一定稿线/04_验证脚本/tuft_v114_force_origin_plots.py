# -*- coding: utf-8 -*-
# V9.39 力的本源推导链配图（三面板）：A 推导链 / B F=-dE/dr 数值互证 / C 判定
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

# A：本源链条
ax = axes[0]
ax.axis("off")
steps = ["1 螺旋公设 r(t)=(rho cos, rho sin, b)", "2 Frenet: kappa=rho/(rho2+b2), tau=b/(rho2+b2)",
         "3 绑定: kappa2+tau2=(omega/c)2", "4 复场 Xi=kappa+i*tau (BOUNDARY)",
         "5 Proca: (grad2-mu2)phi=0 -> Yukawa", "6 能量: E=s*hbar*c*q1q2*e^(-r/L)/r",
         "7 力: F=-dE/dr (PASS, dev~1e-11)"]
y = 0.92
for i, s in enumerate(steps):
    col = "#2ca02c" if i in (0, 1, 2, 4, 5, 6) else "#ff7f0e"
    ax.text(0.05, y, s, fontsize=9.5, color=col, transform=ax.transAxes)
    y -= 0.13
ax.set_title("A 组：本源链条七环\n全部可验算（①-③ L1 PASS、④ BOUNDARY、⑤-⑦ PASS）")

# B：F=-dE/dr vs 单方程（log-log 双曲线+数值点）
ax = axes[1]
r = [10**(x/100.0) for x in range(-300, 301)]
alpha = 0.0072973525693
q_pi, lam_pi = 0.0204, HBARC/134.9768
def F_closed(q1, q2, lam, rr):
    if lam is None:
        return HBARC*q1*q2/(rr*rr)
    return HBARC*q1*q2*(1/rr+1/lam)*math.exp(-rr/lam)/(rr*rr)
def F_grad(q1, q2, lam, rr):
    dr = 1e-6*max(rr, 1e-6)
    E = lambda x: HBARC*q1*q2*math.exp(-x/lam)/x if lam else HBARC*q1*q2/x
    return -(E(rr+dr)-E(rr-dr))/(2*dr)
ax.loglog(r, [F_closed(1.0, alpha, None, x) for x in r], "b-", lw=2, label="电磁 1/r2 (单方程=梯度)")
ax.loglog(r, [F_closed(q_pi, q_pi, lam_pi, x) for x in r], "r--", lw=2, label="强力 Yukawa (单方程=梯度)")
rs = [0.1, 1.0, 10.0]
for x0 in rs:
    ax.plot(x0, F_grad(1.0, alpha, None, x0), "k^", ms=7)
    ax.plot(x0, F_grad(q_pi, q_pi, lam_pi, x0), "ks", ms=7)
ax.set_xlabel("距离 r (fm)")
ax.set_ylabel("|F| (MeV/fm)")
ax.set_title("B 组：F=-dE/dr 数值 vs V9.34 单方程\n相对偏差 ~1e-11（差分精度）")
ax.legend(fontsize=8)
ax.grid(alpha=0.3, which="both")

# C：判定
ax = axes[2]
cats = ["本源定位\n(场能量梯度)", "推导链\n(七环)", "新预言\n(TUFT)"]
vals = [1, 1, 0]
bars = ax.bar(cats, vals, color=["#2ca02c", "#2ca02c", "#7f7f7f"], width=0.5)
ax.set_ylim(-0.2, 1.4); ax.set_yticks([0, 1]); ax.set_yticklabels(["0/FAIL", "PASS"])
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v+0.06, "PASS" if v else "0", ha="center", fontsize=10)
ax.set_title("C/D 组：判定\n力的本源=场能量梯度（Noether 推论）\n代价：参数表外输(B03)/BOUNDARY/新预言 0")

fig.suptitle("V9.39 力的本源动力学推导：Proca -> 能量-动量 -> F=-dE/dr（偏差 ~1e-11）", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(r"D:\a10\aikjx\code\my_lib\tuft_v114_force_origin_plots.png", dpi=130)
print("plot saved")
