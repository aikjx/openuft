# -*- coding: utf-8 -*-
"""TUFT V9.5 第十一章 参数内生攻破尝试：候选几何约束逐项检验
目的：系统检验「单粒子螺旋几何 + 静态 Proca」能否内生锁定 alpha*=7.2973525693e-3（B02 攻破尝试，7.2 主线 3）。
口径：每项约束给出唯一解并与 alpha* 比较；空约束/自动成立亦如实报告；不引入数字命理学。"""
import math, json, os

OUT = os.path.dirname(os.path.abspath(__file__))
alpha_star = 7.2973525693e-3

def deca(x):  # 距 alpha* 的对数数量级差距
    return abs(math.log10(x/alpha_star)) if x > 0 else float("inf")

rows = []
def rec(cid, cond, note):
    rows.append((cid, cond, note))
    print(f"[{'PASS' if cond else 'FAIL'}] {cid}: {note}")

# A1: 单值性 e^{i∮κ ds}=1；∮κ ds = 2π/√(1+α²)
rec("A1 曲率单值性 ∮κ ds=2πn", False,
    f"∮κ ds=2π/√(1+α²)；e^{{i∮κ ds}}=1 → α=0（α*={alpha_star:.3e}，距 {deca(0.0):.0f} 数量级）")
# A2: e^{i∮τ ds}=1；∮τ ds = 2πα/√(1+α²)
rec("A2 挠率单值性 ∮τ ds=2πn", False,
    f"∮τ ds=2πα/√(1+α²)；解集 {{0}}∪{{发散}}，不含 α*")
# A3: e^{i∮(κ+iτ)ds} 模长
rec("A3 复相位单值性", False,
    f"|e^{{i∮(κ+iτ)ds}}|=e^{{−2πα/√(1+α²)}}≠1，非纯相位，不构成单值条件")
# A4: 玻尔-索末菲
rec("A4 玻尔-索末菲 ∮p·dq", True,
    "≡2πħ：是 2.4 母恒等式的积分形式，对任意 α 成立——空约束")
# A5: 螺旋角动量
rec("A5 螺旋角动量 L_z=ħ/(1+α²)=ħ/2", False,
    f"解得 α=1（距 α* 约 {deca(1.0):.1f} 数量级；且未计入轴向角动量贡献，为朴素候选）")
# A6: b 与经典电子半径
rec("A6 b 与经典电子半径 r_e", True,
    "r_e=αλ 由 α 定义，b=αλ/√(1+α²)≈r_e 是恒等式（循环），空约束")
# A7: 场相位缠绕
rec("A7 场相位周期缠绕 ∮dφ", True,
    "φ=arctan α 为常数，每圈缠绕数 ≡0，空约束")

# A8: 扫描景观——每个约束的全局极小点（对数网格 α∈[1e-6,1]）
scan = []
a = 1e-6
while a <= 1.0:
    scan.append(a)
    a *= 10.0**0.02
def res_A1(x): return abs(1.0/math.sqrt(1.0+x*x) - 1.0)
def res_A2(x): return abs(x/math.sqrt(1.0+x*x) - round(x/math.sqrt(1.0+x*x)))
def res_A5(x): return abs(1.0/(1.0+x*x) - 0.5)
best = {"A1": (min(scan, key=res_A1), min(res_A1(x) for x in scan)),
        "A2": (min(scan, key=res_A2), min(res_A2(x) for x in scan)),
        "A5": (min(scan, key=res_A5), min(res_A5(x) for x in scan))}
for k, (xm, rmin) in best.items():
    print(f"    [scan] {k} 全局极小点 α≈{xm:.3e}（残差 {rmin:.2e}），距 α* {deca(xm):.1f} 个数量级")
rec("A8 α 扫描景观：无约束选中 α*", all(deca(v[0]) > 1.0 for v in best.values()),
    "最近约束解距 α* 均 ≥ 1.1 个数量级（α=0 或 α=1）")

# 全维统一度总账（等权口径）
layers = [
    ("形式层（统一势+统一力方程）", 4, 4, "PASS"),
    ("力程层（λ 谱连续过渡，λ 外输）", 4, 4, "PASS(输入)"),
    ("本源映射层（荷由几何表达）", 2, 4, "引力/电磁 PASS；强/弱玩具"),
    ("常数层（耦合常数内生）", 0, 4, "FAIL(B01-B03)"),
    ("量子层（量子化/规范结构）", 0, 4, "FAIL(4.7)"),
]
score = sum(u for n, u, t, s in layers); total = sum(t for n, u, t, s in layers)
rec("U1 全维统一度（等权口径）", True,
    f"{score}/{total} = {score/total*100:.0f}%：形式 100%、力程 100%、本源 50%、常数 0%、量子 0%")

ok_n = sum(1 for _, c, _ in rows if c)
print(f"\n=== 汇总：{ok_n}/{len(rows)} PASS（FAIL 均为『约束不存在/指向错误 α』的负结果）===")
with open(OUT + r"\tuft_v95_param_attack_out.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(f"[{'PASS' if c else 'FAIL'}] {n}: {t}" for n, c, t in rows))
    f.write(f"\n=== 汇总：{ok_n}/{len(rows)} PASS ===\n")

# 配图：统一度四层条形 + 约束解位置
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from matplotlib import font_manager
    for fname in ("C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/msyhbd.ttc",
                  "C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/simsun.ttc"):
        if os.path.exists(fname):
            try:
                font_manager.fontManager.addfont(fname)
            except Exception:
                pass
    mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    mpl.rcParams["axes.unicode_minus"] = False
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8))
    ax = axes[0]
    names = [n for n, u, t, s in layers]
    frac = [u/t*100 for n, u, t, s in layers]
    colors = ["#1f7a3d", "#1f7a3d", "#b8860b", "#c0392b", "#c0392b"]
    ax.barh(names[::-1], frac[::-1], color=colors[::-1])
    for i, v in enumerate(frac[::-1]):
        ax.text(v+2, i, f"{v:.0f}%", va="center", fontsize=10)
    ax.set_xlim(0, 118); ax.set_xlabel("统一度（等权口径，N/4）")
    ax.set_title("TUFT 全维统一度总账（V9.5）")
    ax.grid(axis="x", alpha=0.3)
    ax2 = axes[1]
    ax2.axvline(math.log10(alpha_star), color="#1f7a3d", lw=2.2, label="alpha*=7.297e-3（实验值）")
    for k, (xm, _) in best.items():
        ax2.axvline(math.log10(xm), color="#c0392b", ls="--", lw=1.5)
        ax2.text(math.log10(xm)+0.08, 0.8, k, color="#c0392b", fontsize=10)
    ax2.set_xlim(-7, 1); ax2.set_ylim(0, 1)
    ax2.set_xticks(range(-6, 2)); ax2.set_xticklabels([f"$10^{{{i}}}$" for i in range(-6, 2)])
    ax2.set_xlabel("α（对数）"); ax2.set_yticks([])
    ax2.set_title("候选约束解 vs α*（无约束选中实验值）")
    ax2.legend(fontsize=9, loc="lower left")
    plt.tight_layout()
    plt.savefig(OUT + r"\tuft_v95_param_attack_plots.png", dpi=140)
    print("[plot] tuft_v95_param_attack_plots.png saved")
except Exception as e:
    print(f"[plot] skipped: {type(e).__name__}: {e}")

with open(OUT + r"\tuft_v95_param_attack_results.json", "w", encoding="utf-8") as f:
    json.dump({"alpha_star": alpha_star,
               "checks": [{"cid": n, "ok": c, "note": t} for n, c, t in rows],
               "layers": [{"layer": n, "unified": u, "total": t, "status": s} for n, u, t, s in layers]},
              f, ensure_ascii=False, indent=1)
print("[json] tuft_v95_param_attack_results.json saved")
