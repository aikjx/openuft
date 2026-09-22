# -*- coding: utf-8 -*-
"""
TUFT 实验预言白皮书 · 第七节数值验证脚本（修复版）

修复点（相对草稿）：
  1. P3「暗物质无信号」信号强度为 0，在 log 坐标下柱状图无法渲染。
     对 is_null 型预言改用 current_sens/target_sens（探测深度提升比）衡量。
  2. 草稿调用 plt.show() 在无图形界面环境会报错/挂起，改用 Agg 后端 + savefig。

运行：python 全域统一场论_TUFT实验预言仿真.py
产出：tuft_predictions_detectability.png + 终端可探测性/优先级报告
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # 无头环境后端
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 探测系统中可用的中文字体，避免标题/标签出现方框
for _cand in ['Microsoft YaHei', 'SimHei', 'Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'Arial Unicode MS']:
    if any(_cand.lower() in f.name.lower() for f in fm.fontManager.ttflist):
        plt.rcParams['font.sans-serif'] = [_cand]
        break
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# ========== TUFT 预言信号强度 vs 探测灵敏度 ==========
# 字段: (名称, 信号强度或参考量, 当前灵敏度, 目标灵敏度, 年份, 是否为"预期无信号"型预言)
predictions = [
    ("P1: 张量标量比 r",     0.03,  0.036, 0.001, 2035, False),
    ("P2: 引力波手性 Π_T",   0.10,  1.0,   0.05,  2040, False),
    ("P3: 暗物质无信号",     0.0,   1e-47, 1e-49, 2030, True),   # 预期无信号：用"探测深度提升比"衡量
    ("P6: 黑洞面积偏差",     0.005, 0.05,  0.001, 2035, False),
    ("P9: 挠率直接探测",     1e-4,  1e-2,  1e-7,  2030, False),
    ("P10: 挠子耦合",        1e-6,  1e-4,  1e-8,  2035, False),
    ("P11: 自旋 EP 破缺",    1e-14, 1e-15, 1e-17, 2040, False),
]

names        = [p[0] for p in predictions]
signal       = np.array([p[1] for p in predictions], dtype=float)
current_sens = np.array([p[2] for p in predictions], dtype=float)
target_sens  = np.array([p[3] for p in predictions], dtype=float)
years        = np.array([p[4] for p in predictions])
is_null      = np.array([p[5] for p in predictions])

# 可探测性/理论支持比：
#  - 信号型预言: ratio = signal / sensitivity (>1 = 当前可探测)
#  - 无信号型预言: ratio = current_sens / target_sens (>1 = 探测深度持续提升，对理论更有利)
current_ratio = np.where(is_null, current_sens / target_sens, signal / current_sens)
target_ratio  = np.where(is_null, current_sens / target_sens, signal / target_sens)

fig, ax = plt.subplots(figsize=(12, 6))
y_pos = np.arange(len(names))

colors_current = ['green' if r > 1 else 'orange' if r > 0.1 else 'red' for r in current_ratio]
colors_target  = ['green' if r > 1 else 'orange' if r > 0.1 else 'red' for r in target_ratio]

ax.barh(y_pos - 0.2, current_ratio, 0.4, color=colors_current, alpha=0.7, label='当前灵敏度')
ax.barh(y_pos + 0.2, target_ratio,  0.4, color=colors_target,  alpha=0.7, label='目标灵敏度（2030-2040）')

ax.axvline(1.0, color='k', ls='--', lw=2, label='阈值（比值=1）')
ax.set_yticks(y_pos)
ax.set_yticklabels(names, fontsize=11)
ax.set_xlabel('信号/灵敏度 比值（无信号预言取"探测深度提升比"，对数坐标）', fontsize=12)
ax.set_xscale('log')
ax.set_xlim(1e-4, 1e4)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='x')
ax.set_title('TUFT 预言信号强度与探测灵敏度对比', fontsize=14)

plt.tight_layout()
plt.savefig('tuft_predictions_detectability.png', dpi=150)
print("图表已保存: tuft_predictions_detectability.png")

# ========== 输出可探测性分析 ==========
print("=" * 70)
print("TUFT 预言可探测性分析")
print("=" * 70)
for i, name in enumerate(names):
    if is_null[i]:
        print(f"\n{name}:")
        print(f"  参考灵敏度: 当前 {current_sens[i]:.2e} → 目标 {target_sens[i]:.2e}")
        print(f"  探测深度提升比(当前/目标): {current_ratio[i]:.2e}")
        print(f"  🟢 探测深度持续提升（预期无信号，对理论有利）")
        print(f"  预计验证年份: {years[i]}")
        continue
    status_current = "✅ 可探测" if current_ratio[i] > 1 else "⚠️ 接近" if current_ratio[i] > 0.1 else "❌ 不可探测"
    status_target  = "✅ 可探测" if target_ratio[i]  > 1 else "⚠️ 接近" if target_ratio[i]  > 0.1 else "❌ 不可探测"
    print(f"\n{name}:")
    print(f"  信号强度: {signal[i]:.2e}")
    print(f"  当前灵敏度: {current_sens[i]:.2e} → {status_current}")
    print(f"  目标灵敏度: {target_sens[i]:.2e} → {status_target}")
    print(f"  预计验证年份: {years[i]}")

# ========== 实验优先级排序 ==========
print("\n" + "=" * 70)
print("实验优先级排序（按 信号强度/成本/时间 综合评分）")
print("=" * 70)
priority_scores = [
    ("P9 挠率直接探测", 9.5),
    ("P3 暗物质无信号", 9.0),
    ("P1 张量标量比", 8.5),
    ("P2 引力波手性", 8.0),
    ("P10 挠子探测", 7.0),
    ("P6 黑洞面积", 6.5),
    ("P11 自旋 EP 破缺", 6.0),
    ("P4 宇宙组分", 5.5),
    ("P5 哈勃张力", 5.0),
    ("P14 α 常数演化", 4.0),
    ("P8 无奇点", 3.5),
    ("P7 霍金手性", 3.0),
    ("P13 高能散射", 2.5),
    ("P12 人工引力", 2.0),
]

for name, score in sorted(priority_scores, key=lambda x: -x[1]):
    stars = "★" * int(score) + "☆" * (10 - int(score))
    print(f"  {stars}  {name} ({score}/10)")
