import numpy as np

# 验证光速柱面螺旋运动的速度计算（式1）
def verify_spiral_velocity():
    # 定义参数
    r = 1.0  # 螺旋半径
    omega = 2.0  # 角频率
    h = 3.0  # 轴向速度
    c = np.sqrt(r**2 * omega**2 + h**2)  # 计算光速
    
    # 计算速度矢量的模
    def velocity_magnitude(t):
        # 位置矢量对时间的导数
        vx = -r * omega * np.sin(omega * t)
        vy = r * omega * np.cos(omega * t)
        vz = h
        return np.sqrt(vx**2 + vy**2 + vz**2)
    
    # 验证不同时间点的速度模是否等于c
    times = np.linspace(0, 2*np.pi/omega, 100)
    velocity_magnitudes = [velocity_magnitude(t) for t in times]
    
    # 检查所有时间点的速度模是否等于c（考虑浮点误差）
    max_error = max(abs(v - c) for v in velocity_magnitudes)
    
    print("=== 光速柱面螺旋运动速度验证 ===")
    print(f"螺旋半径 r = {r}")
    print(f"角频率 omega = {omega}")
    print(f"轴向速度 h = {h}")
    print(f"计算得到的光速 c = {c}")
    print(f"最大速度模误差: {max_error}")
    print(f"验证结果: {'通过' if max_error < 1e-10 else '失败'}")
    print()

if __name__ == "__main__":
    verify_spiral_velocity()
