# -*- coding: utf-8 -*-
"""
验证张祥前常数Z的基本计算
基于引力光速统一方程 Z = (G * c) / 2
"""

# 已知常数
G_codata_2018 = 6.67430e-11  # m³·kg⁻¹·s⁻² (CODATA 2018推荐值)
c = 299792458                # m·s⁻¹ (光速)

# 按照公式 Z = (G * c) / 2 计算Z值
Z_calculated = (G_codata_2018 * c) / 2
Z_paper = 0.010004524012147  # 论文中给出的Z精确值

print("===== 张祥前常数Z的基本验证 =====")
print(f"使用CODATA 2018推荐值 G = {G_codata_2018} m³·kg⁻¹·s⁻²")
print(f"光速 c = {c} m·s⁻¹")
print(f"/n根据公式 Z = (G * c) / 2 计算:")
print(f"Z = ({G_codata_2018} * {c}) / 2 = {Z_calculated}")
print(f"/n论文中给出的Z精确值: Z = {Z_paper}")
print(f"两者差值为: {abs(Z_calculated - Z_paper)}")

# 验证是否完全一致
if abs(Z_calculated - Z_paper) < 1e-15:
    print("结论：论文中给出的Z精确值与通过G·c/2计算得到的值完全一致")
else:
    print("警告：两个Z值存在差异")