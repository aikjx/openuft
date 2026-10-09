# 计算Z=0.01近似值时的误差

# 已知值
Z_approx = 0.01  # 近似值
Z_exact = 0.010004524012147  # 精确值（公式10-9）
c = 299792458  # m/s（光速）
G_codata_2018 = 6.67430e-11  # m^3 * kg^-1 * s^-2（CODATA 2018推荐值）

# --- 计算Z近似值的误差 ---#
absolute_error_Z = abs(Z_exact - Z_approx)
relative_error_Z = (absolute_error_Z / Z_exact) * 100

print("Z值的误差计算：")
print(f"精确值Z_exact = {Z_exact}")
print(f"近似值Z_approx = {Z_approx}")
print(f"Z的绝对误差 = {absolute_error_Z:.15f}")
print(f"Z的相对误差 = {relative_error_Z:.6f}%\n")

# --- 计算使用Z近似值时G的误差 ---#
G_approx = (2 * Z_approx) / c  # 使用近似值计算G
G_exact = (2 * Z_exact) / c    # 使用精确值计算G

absolute_error_G = abs(G_exact - G_approx)
relative_error_G = (absolute_error_G / G_exact) * 100

# 与CODATA值的比较
absolute_error_G_codata = abs(G_codata_2018 - G_approx)
relative_error_G_codata = (absolute_error_G_codata / G_codata_2018) * 100

print("使用Z近似值时G的误差计算：")
print(f"使用精确值计算的G = {G_exact:.12e} m^3 kg^-1 s^-2")
print(f"使用近似值计算的G = {G_approx:.12e} m^3 kg^-1 s^-2")
print(f"G与精确值的绝对误差 = {absolute_error_G:.12e} m^3 kg^-1 s^-2")
print(f"G与精确值的相对误差 = {relative_error_G:.6f}%")
print(f"CODATA 2018推荐的G = {G_codata_2018:.12e} m^3 kg^-1 s^-2")
print(f"G与CODATA值的绝对误差 = {absolute_error_G_codata:.12e} m^3 kg^-1 s^-2")
print(f"G与CODATA值的相对误差 = {relative_error_G_codata:.6f}%")




# 定义绝对误差和 G_CODATA 的值
absolute_error = 3.01809603695900848846571050e-14
g_codata = 6.67430e-11

# 计算相对误差
relative_error = (absolute_error / g_codata) * 100

# 打印结果
print(f"计算相对误差: ({absolute_error}/{g_codata})×100%")
print(f"相对误差 = {relative_error}%")