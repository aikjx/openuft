# -*- coding: utf-8 -*-
# 0·1·∞ 统一场论 · 核心结构突破推导（MainAgent 亲自精算验证）
import math

a = 0.0072973525693          # 精细结构常数
hbar = 1.054571817e-34       # J·s
c = 299792458.0              # m/s
G = 6.67430e-11              # CODATA
mp = 1.67262192369e-27       # 质子质量
me = 9.1093837015e-31        # 电子质量

print('=' * 70)
print('推导 1：tau = alpha * kappa，四大力场并非独立')
print('=' * 70)
print('kappa(r) = 1/[rho(r)(1+a^2)]')
print('tau(r)   = a/[rho(r)(1+a^2)] = a * kappa(r)')
print('=> grad(tau) = a * grad(kappa)：曲率梯度与挠率梯度同方向、固定比例')
print()
print('统一力场代入：')
print('F_n = -hbar*c/(1+a^2) * (a^-n*grad(kappa) + a^n*grad(tau))')
print('    = -hbar*c/(1+a^2) * (a^-n + a^(n+1)) * grad(kappa)')
print()
print('--- 四大力系数 C_n = (a^-n + a^(n+1))/(1+a^2) ---')
C = {}
for n in [-2, -1, 0, 1]:
    C[n] = (a**-n + a**(n+1)) / (1 + a**2)
    print('  n={0:+d} : C_n = {1:.6e}'.format(n, C[n]))
print()
print('结论A：C(-2)=C(+1)，C(-1)=C(0) —— 四力实际只有 2 组系数！')
print('       引力与强力、电磁与弱力在数学上完全同构，')
print('       "四大力由单一拓扑数 n 切换"在数值上不成立。')

print()
print('=' * 70)
print('推导 2：力不依赖源质量（致命）')
print('=' * 70)
print('grad(kappa) = -(1+a^2)^-1 * grad(rho)/rho^2')
print('F_n = -C_n/(1+a^2) * grad(rho)/rho^2')
print('=> F_n 中没有任何质量参数 m1、m2')
print('   牛顿引力 F = -G*m1*m2/r^2 要求 F ∝ m1*m2')
print('   库仑力   F = k_e*q1*q2/r^2 要求 F ∝ q1*q2')
print('=> 该框架的力是纯几何场，不感知源质量/电荷，')
print('   即使 rho(r) 形状完全正确，也只能给出与源无关的 1/r^2 场，')
print('   不可能还原牛顿引力或库仑定律的定量形式。')

print()
print('=' * 70)
print('尝试多种 rho(r) 候选：能否给出 1/r^2 空间形式（纯Python数值梯度）')
print('=' * 70)

def probe(name, rho_func, rs):
    eps = 1e-6
    row = []
    for r in rs:
        d = (rho_func(r+eps) - rho_func(r-eps))/(2*eps)
        row.append(d/rho_func(r)**2 * r**2)  # 若=常数，则空间形式为 1/r^2
    print('  ' + name.ljust(24) + ' r^2*grad(rho)/rho^2 = ' + str(['{0:.4f}'.format(x) for x in row]))

rs = [1.0, 2.0, 4.0, 8.0]
print('候选 1：rho = r          （应→常数，即 1/r^2）')
probe('rho=r', lambda r: r, rs)
print('候选 2：rho = r^2        （应→线性，即 1/r^3）')
probe('rho=r^2', lambda r: r**2, rs)
print('候选 3：rho = sqrt(r^2+1)（远场→1/r^2）')
probe('rho=sqrt(r^2+1)', lambda r: (r**2+1)**0.5, rs)
print('候选 4：rho = 1 + r      （近场截止，非1/r^2）')
probe('rho=1+r', lambda r: 1+r, rs)
print('=> 只有 rho(r) ∝ r（或远场近似）能给出 1/r^2 空间形式')

print()
print('=' * 70)
print('定量验证：即使 rho=r，能否匹配不同质量的引力？')
print('=' * 70)
C_g = C[-2]  # n=-2 系数
for name, m in [('质子-质子', mp), ('电子-电子', me)]:
    rho0 = C_g/((1+a**2)*G*m*m)
    print('  ' + name + ': 需要 rho0 = {0:.3e} m'.format(rho0))
print('  => rho0 必须随源质量 m^2 反比变化；但 rho0 是单一常数，')
print('     不可能同时满足不同质量组合 => 无法还原牛顿引力 F ∝ m1*m2')

print()
print('=' * 70)
print('修复路径评估（所有方法试）')
print('=' * 70)
print('路径1 [已证伪] 固定 rho(r) 形状：力不含源质量 => 无法还原牛顿/库仑')
print('路径2 [已证伪] 调整 n 权重：n 只缩放同一场，且四力塌缩为两组系数')
print('路径3 [已证伪] 令 alpha 为常数：tau=const*kappa，n 切换无物理内容')
print('路径4 [待突破] 令 alpha 依赖(源)质量/位置 alpha(r,m)：tau!=const*kappa，')
print('               n 切换才可能有物理意义；但 alpha 成为动力学场，')
print('               需新增动力学方程与实验约束')
print('路径5 [待突破] 引入几何源荷：rho(r) 由源质量决定，把质量编码进几何，')
print('               需给出确定性规则并检验')
print('路径6 [待突破] 把 n 与粒子/质量绑定：需给出 n(m) 确定规则，避免无穷参数')

print()
print('=' * 70)
print('精算验证：统一势能还原检查')
print('=' * 70)
print('Phi_n = hbar*c*(a^-n + a^(n+1))/((1+a^2)^2 * rho(r))')
print('=> 势能也只是 rho(r) 的标量倍数，不含源质量/电荷，同样无法还原')
