# -*- coding: utf-8 -*-
"""
运动电荷引力场公式 (V2) 量纲审计与数值量级实证
算法联盟 · 公式层实证

复算对象:
  utf/10-统一场论核心公式/公式验证论文/圆周运动正电荷产生的引力场方程/
      verify_circular_motion_gravity_field.py  (V2 方程 A = -q/(4*pi*eps0*c^2*r)*(rhat x (rhat x a_q)))

目的:
  1. 用标准量纲 (M,L,T,I) 独立复算 V2 公式量纲, 对照作者自验证脚本的结论
  2. 数值量级量化: 把代码产出(量纲 N/C)经电子荷质比转为加速度后, 与真实牛顿引力场对比
  3. 给出"最小修正因子"分析

说明: 本脚本不依赖第三方库(仅 numpy 做数值), 纯标准库即可复算符号部分.
"""
import numpy as np

BASE = ['M', 'L', 'T', 'I']  # 质量, 长度, 时间, 电流


def mk(d):
    return {k: d.get(k, 0) for k in BASE}


def mul(a, b):
    return mk({k: a[k] + b[k] for k in BASE})


def div(a, b):
    return mk({k: a[k] - b[k] for k in BASE})


def power(a, n):
    return mk({k: a[k] * n for k in BASE})


def fmt(d):
    parts = []
    for k in BASE:
        e = d[k]
        if e != 0:
            parts.append(k if e == 1 else (k + str(e)))
    return "·".join(parts) if parts else "1 (无量纲)"


# ---- 基本量纲 ----
q   = mk({'T': 1, 'I': 1})              # 电荷: 库仑 C = A·s
eps0 = mk({'M': -1, 'L': -3, 'T': 4, 'I': 2})   # 真空介电常数: F/m = C^2·s^2/(kg·m^3); C=A*s => [M^-1 L^-3 T^4 I^2]
c   = mk({'L': 1, 'T': -1})             # 光速
r   = mk({'L': 1})                      # 距离
a_q = mk({'L': 1, 'T': -2})             # 加速度
m   = mk({'M': 1})                      # 质量
G   = mk({'M': -1, 'L': 3, 'T': -2})   # 引力常数: [M^-1 L^3 T^-2]

# 对照基准
N_over_C = div(mk({'M': 1, 'L': 1, 'T': -2}), mk({'I': 1, 'T': 1}))  # N/C = (kg·m/s^2)/C
accel    = mk({'L': 1, 'T': -2})        # m/s^2


def banner(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


banner("一、量纲审计 (符号推导)")
c2 = power(c, 2)
denom = mul(mul(eps0, c2), r)          # eps0 * c^2 * r
factor = div(q, denom)                 # q / (eps0 * c^2 * r)
print("q / (eps0 c^2 r) 量纲 =", fmt(factor))
field = mul(factor, a_q)               # 再乘 a_q
print("(q/(eps0 c^2 r)) · a_q 量纲 =", fmt(field))
print("电场强度 N/C    量纲 =", fmt(N_over_C))
print("加速度 m/s^2    量纲 =", fmt(accel))

ident_to_NC = (field == N_over_C)
ident_to_acc = (field == accel)
print("=> 与 N/C 量纲完全一致? ", ident_to_NC)
print("=> 与 m/s^2 量纲一致?    ", ident_to_acc)
assert ident_to_NC, "独立复算: 量纲应等于 N/C"
assert not ident_to_acc, "独立复算: 量纲不应等于 m/s^2"

# 作者原脚本(第51-58行)中间推导的维度代数瑕疵复核:
#   分母 = (C^2*s^2/(kg*m^3)) * (m^2/s^2) * m
#        = C^2*s^2*m^2*m / (kg*m^3*s^2)
#        = C^2 * m^(2+1-3) * (s^2/s^2) / kg
#        = C^2 / kg                       <-- 长度维 m^3 与 m^3 恰好完全相消!
#   代入 C = A*s  => 分母 = A^2*s^2 / kg  (无量纲 L)
#   作者第53-54行却写成 "A^2*s^2/(kg*m)", 多保留了一个 m
#   => 第57行最终写出 kg*m^2/(A*s^3) = [M L^2 T^-3 I^-1], 比正确 N/C = kg*m/(A*s^3) = [M L T^-3 I^-1] 多一个 L
#   但作者在第58-59行正确判断:"实际量纲应为 m/s^2, 这里存在问题 => 量纲可能不一致"
print("\n[对照] 作者自验证脚本(第51-58行)推导瑕疵复核:")
print("   分母真实量纲 (eps0 c^2 r) =", fmt(mul(mul(eps0, c2), r)), "  (长度维已完全相消, 应为 [M^-1 T^2 I^2])")
print("   作者手写分母量纲          = A^2*s^2/(kg*m)  (多保留一个 m, 错误)")
print("   作者最终手写量纲          = kg*m^2/(A*s^3) =", fmt(mk({'M':1,'L':2,'T':-3,'I':-1})), " (比正确 N/C 多一个 L)")
print("   正确量纲 N/C              =", fmt(N_over_C), " = kg*m/(A*s^3)")
print("   => 作者结论'量纲不一致'正确; 但其中间推导约分失误(多算一个 m), 正确量纲是 N/C 而非其手写的 kg*m^2/(A*s^3)")


banner("二、数值量级实证 (标准物理常数)")
e = 1.602176634e-19       # 元电荷 C
EPS0 = 8.8541878128e-12   # F/m
CC = 2.99792458e8         # m/s
GE = 6.67430e-11          # m^3/(kg·s^2)
ME = 9.1093837015e-31     # 电子质量 kg
PI = np.pi

# 代码实现的核心系数(无 q/m 因子):
#   factor = -q / (4*pi*eps0*c^2*r)
#   A_v2   = factor * cross2            (cross2 在横向时量级 = a_q)
# 量纲: A_v2 实为电场 E (N/C)
def E_v2(qval, r_m, a_val):
    return abs(qval) / (4 * PI * EPS0 * CC ** 2 * r_m) * abs(a_val)


def scenario(r_m, a_val, label):
    E = E_v2(e, r_m, a_val)            # N/C (代码产出的真实量纲)
    a_from_E = (e / ME) * E            # 经检验电子荷质比 (e/m_e) 转为加速度 m/s^2
    g_real = GE * ME / r_m ** 2        # 同一运动电子作为质量源产生的真实牛顿引力场 m/s^2
    ratio = a_from_E / g_real
    print(f"\n场景 [{label}]  r={r_m:g} m, a_q={a_val:g} m/s^2")
    print(f"  代码产出 E_v2        = {E:.3e} N/C   (代码误标为 m/s^2 的'引力场')")
    print(f"  转电子加速度 a_from_E= {a_from_E:.3e} m/s^2  (乘 e/m_e 后量级)")
    print(f"  真实牛顿引力 g_real  = {g_real:.3e} m/s^2  (运动电子为质量源)")
    print(f"  比值 a_from_E/g_real = {ratio:.3e}  (~{np.log10(ratio):.1f} 个数量级)")


scenario(1.0, 1.0, "单位场景(代码默认测试量级)")
scenario(5.29177210903e-11, 9.0e22, "原子尺度(玻尔半径, 电子圆周向心加速度)")
scenario(0.01, 100.0, "介观场景")


banner("三、最小修正因子分析")
print("被审公式量纲 = N/C (电场). 要得到加速度 m/s^2, 须消去电流维 I.")
print("最小修正: 在 E_v2 上乘检验粒子的荷质比 (q_test / m_test):")
print("   A_correct = (q_test / m_test) * E_v2   => 量纲 (N/C)*(C/kg) = N/kg = m/s^2")
print("但这意味着'场'依赖检验电荷而非检验质量 —— 与'引力场对一切质量给 g'的")
print("物理语义冲突. 故该公式机制上仍是电场(依赖电荷), 并非真正的引力场.")

banner("四、结论 (诚实归属)")
print("1. 正确性: 独立复算确认 V2 公式量纲 = N/C, 不是代码 ylabel 宣称的 m/s^2. 数学成立.")
print("2. 非完全原创: 作者自验证脚本第58-59行已先标注'量纲可能不一致';")
print("   本实证贡献 = 标准量纲独立复算(纠正其推导瑕疵, 给出精确 N/C) + 数值量级量化 + 最小修正分析.")
print("3. 红线: 数学自洽不等于物理证实; 本审计仅证'代码公式量纲错配 + 推导文档粉饰',")
print("   不评价张祥前统一场论整体.")
print("\nDONE.")
