# 验证张祥前引力光速统一方程的计算准确性

# 物理常数
c = 299792458  # 光速，单位：m/s
G_CODATA = 6.67430e-11  # CODATA 2018引力常数，单位：m^3·kg^-1·s^-2

# 根据论文中的公式Z = G·c/2计算Z的理论值
Z_theory = G_CODATA * c / 2
print(f"根据Z = G·c/2计算的Z理论值: Z = {Z_theory}")

# 论文中给出的Z精确值
Z_paper = 0.010004524012147
print(f"论文中给出的Z精确值: Z = {Z_paper}")

# 验证两个Z值是否相等
if abs(Z_theory - Z_paper) < 1e-15:
    print("结论：论文中给出的Z精确值与通过G·c/2计算得到的值完全一致")
else:
    print(f"警告：两个Z值存在差异，差值为: {abs(Z_theory - Z_paper)}")

# 反向验证：使用Z_paper计算G，验证是否等于CODATA值
G_calculated = 2 * Z_paper / c
print(f"/n使用Z_paper计算的G值: G = {G_calculated}")
print(f"CODATA 2018的G值: G = {G_CODATA}")

# 计算相对误差
relative_error = abs(G_calculated - G_CODATA) / G_CODATA * 100
print(f"相对误差: {relative_error}%")

# 验证近似值Z=0.01的误差
Z_approx = 0.01
g_approx = 2 * Z_approx / c
approx_error = abs(g_approx - G_CODATA) / G_CODATA * 100
print(f"/n使用近似值Z=0.01计算的G值: G = {g_approx}")
print(f"近似值的相对误差: {approx_error}%")

# 关键发现分析
print("/n关键发现：")
print("1. 论文中给出的Z精确值(0.010004524012147)恰好等于G_CODATA·c/2的计算结果")
print("2. 这意味着Z的数值是从已知的G和c值推导出来的，而非独立测量或通过其他物理原理计算得到")
print("3. 因此，用Z值反过来验证G值本质上是一个代数恒等变换，不构成独立的实验验证")