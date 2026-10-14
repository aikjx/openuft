# -*- coding: utf-8 -*-
"""V9.26 束缚谱定量化配图：Bargmann 上限 + Derrick 数值终判（双面板）"""
import json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

for fp in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyhbd.ttc"]:
    try:
        font_manager.fontManager.addfont(fp)
        break
    except Exception:
        pass
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

d = json.load(open(r"D:\a10\aikjx\code\my_lib\tuft_v107_binding_count_audit_results.json", encoding="utf-8"))
fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.6))

# ---- A：Bargmann 上限 ----
ax = axes[0]
names = ["氘核 OPE\n(pi0 交换)", "弱力 W\n交换", "氢原子\n(库仑)", "引力\n(质子对)"]
caps = [0.0058, 9.9e-5, float("inf"), float("inf")]
disp = [0.0058, 9.9e-5, 1e4, 1e4]  # 对数显示：inf 用 1e4 占位
cols = ["#d62728", "#d62728", "#1f77b4", "#1f77b4"]
bars = ax.bar(range(4), [math.log10(x) for x in disp], color=cols, alpha=0.85)
ax.axhline(0, color="#333333", ls=":", lw=1.2)
ax.text(3.45, 0.06, "N_0 = 1（一个束缚态阈值）", ha="right", fontsize=9, color="#333333")
labels = ["N0<=0.0058\n严格零束缚态", "N0<=9.9e-5\n零束缚态", "积分发散\n无限量子谱", "积分发散\n无限经典层级"]
for b, lab in zip(bars, labels):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.12, lab, ha="center", fontsize=8.5)
ax.set_xticks(range(4)); ax.set_xticklabels(names, fontsize=9)
ax.set_ylabel("log10(Bargmann 上限 N_0)")
ax.set_title("A 组：Bargmann 严格上限 N_0 <= 2*kappa_tilde\n氘核双通道互证：上限 0.0058 < 1（变分+不等式）", fontsize=10.5)
ax.grid(alpha=0.3, axis="y")

# ---- B：Derrick 尺度扫描 ----
ax = axes[1]
r = d["B_derrick_numerical"]["derrick_scan_lambda32"]
alphas = [s["alpha"] for s in r["scale_transform"]]
Es = [s["E(alpha)"] for s in r["scale_transform"]]
ax.plot(alphas, Es, "o-", lw=2, color="#2ca02c", label="E(alpha)=EK/alpha+EP/alpha^3 (lambda=32)")
ax.axhline(0, color="#333333", ls=":", lw=1.2)
ax.annotate("alpha->0: E -> -inf\n（能量无下界）", xy=(0.2, -2036), xytext=(0.55, -1500),
            arrowprops=dict(arrowstyle="->", color="#333333"), fontsize=9)
ax.annotate("无驻点：dE/dA 在 [0.5,2] 全为正\n(+774 -> +2.1)", xy=(2.0, -0.15), xytext=(1.35, -1100),
            arrowprops=dict(arrowstyle="->", color="#333333"), fontsize=9)
ax.set_xlabel("alpha（尺度参数）")
ax.set_ylabel("E(alpha)")
ax.set_title("B 组：Derrick 数值终判——非线性自耦合 Proca 无稳定孤子\n(4.7 修复方案 2 关闭，禁闭只剩外源=输入)", fontsize=10.5)
ax.legend(loc="upper right", fontsize=8.5)
ax.grid(alpha=0.3)

fig.suptitle("V9.26 束缚谱定量化与非线性路线终判：Bargmann 上限 / Derrick 数值检验", fontsize=13, y=1.0)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(r"D:\a10\aikjx\code\my_lib\tuft_v107_binding_count_plots.png", dpi=140)
print("saved ok")
