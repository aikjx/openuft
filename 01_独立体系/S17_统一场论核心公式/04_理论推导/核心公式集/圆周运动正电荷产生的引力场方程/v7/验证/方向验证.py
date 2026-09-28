# 方向关系和几何结构验证
import numpy as np

def verify_direction_relations():
    """验证方向关系和几何结构"""
    print("=== 方向关系和几何结构验证 ===")
    
    # 定义单位矢量
    r_hat = np.array([1, 0, 0])    # 径向单位矢量
    theta_hat = np.array([0, 1, 0])  # 横向单位矢量
    phi_hat = np.array([0, 0, 1])    # 角向单位矢量
    
    print("\n单位矢量定义:")
    print("径向单位矢量 (r_hat):", r_hat)
    print("横向单位矢量 (theta_hat):", theta_hat)
    print("角向单位矢量 (phi_hat):", phi_hat)
    
    # 1. 验证叉乘方向关系
    print("\n1. 叉乘方向验证:")
    # 引力场 A 沿横向 (theta_hat 方向)
    A = theta_hat
    print("引力场 A 方向:", A)
    
    # 计算 A × r_hat
    A_cross_r = np.cross(A, r_hat)
    print("A × r_hat 方向:", A_cross_r)
    
    # 验证结果是否沿 phi_hat 方向
    if np.array_equal(A_cross_r, -phi_hat):
        print("✓ 叉乘方向正确: A × r_hat 沿 -phi_hat 方向")
    else:
        print("✗ 叉乘方向错误")
    
    # 2. 验证场的横向性
    print("\n2. 场的横向性验证:")
    # 计算 A 与 r_hat 的点积
    dot_product = np.dot(A, r_hat)
    print(f"A · r_hat = {dot_product}")
    
    if np.isclose(dot_product, 0):
        print("✓ 引力场 A 是横向场 (垂直于径向)")
    else:
        print("✗ 引力场 A 不是横向场")
    
    # 3. 验证"三力垂直"结构
    print("\n3. 三力垂直结构验证:")
    # 径向电场 E_r 沿 r_hat 方向
    E_r = r_hat
    # 引力场 A 沿 theta_hat 方向
    # 横向磁场 B_theta 沿 -phi_hat 方向
    B_theta = -phi_hat
    
    # 验证两两垂直
    dot_EA = np.dot(E_r, A)
    dot_EB = np.dot(E_r, B_theta)
    dot_AB = np.dot(A, B_theta)
    
    print(f"E_r · A = {dot_EA}")
    print(f"E_r · B_theta = {dot_EB}")
    print(f"A · B_theta = {dot_AB}")
    
    if np.isclose(dot_EA, 0) and np.isclose(dot_EB, 0) and np.isclose(dot_AB, 0):
        print("✓ 三力垂直结构验证通过")
    else:
        print("✗ 三力垂直结构验证失败")
    
    # 4. 验证几何正交性
    print("\n4. 几何正交性验证:")
    # 验证单位矢量构成正交系
    dot_rtheta = np.dot(r_hat, theta_hat)
    dot_rphi = np.dot(r_hat, phi_hat)
    dot_thetaphi = np.dot(theta_hat, phi_hat)
    
    print(f"r_hat · theta_hat = {dot_rtheta}")
    print(f"r_hat · phi_hat = {dot_rphi}")
    print(f"theta_hat · phi_hat = {dot_thetaphi}")
    
    if np.isclose(dot_rtheta, 0) and np.isclose(dot_rphi, 0) and np.isclose(dot_thetaphi, 0):
        print("✓ 几何正交性验证通过")
    else:
        print("✗ 几何正交性验证失败")
    
    # 5. 验证右手定则
    print("\n5. 右手定则验证:")
    # 右手四指从 A 指向 r_hat，拇指应指向 B_theta
    # 计算右手定则方向
    right_hand_direction = np.cross(A, r_hat)
    print(f"右手定则方向: {right_hand_direction}")
    print(f"B_theta 方向: {B_theta}")
    
    if np.array_equal(right_hand_direction, B_theta):
        print("✓ 右手定则验证通过")
    else:
        print("✗ 右手定则验证失败")

if __name__ == "__main__":
    verify_direction_relations()
