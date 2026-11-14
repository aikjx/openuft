import re

# 读取文件
with open('第40章：四种力的统一.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义要删除的旧内容
old_content = '''#### 与四种力的对应关系

宇宙大统一方程通过不同的条件简化,可以对应不同的基本力：

|| 力的类型 | 简化条件 | 对应项 | 物理机制 |
||---------|---------|-------|---------|
|| **引力** | $\frac{dm}{dt} = 0$, $\frac{d\vec{c}}{dt} = 0$ | $-m\frac{d\vec{v}}{dt}$ | 质量不变时,物体在弯曲空间中运动产生加速度 |
|| **电磁力** | $\frac{dm}{dt} = 0$, $\frac{d\vec{c}}{dt} \neq 0$ | $m\frac{d\vec{c}}{dt} - m\frac{d\vec{v}}{dt}$ | 电荷运动导致局部光速变化,产生电磁效应 |
|| **核力** | $\frac{dm}{dt} \neq 0$, $\frac{d\vec{c}}{dt} \neq 0$ | $\vec{c}\frac{dm}{dt} - \vec{v}\frac{dm}{dt} + m\frac{d\vec{c}}{dt}$ | 短距离内质量剧烈变化,光速也发生局部变化 |
|| **弱力** | $\frac{dm}{dt} \neq 0$, $\frac{d\vec{v}}{dt} \approx 0$ | $\vec{c}\frac{dm}{dt} - \vec{v}\frac{dm}{dt}$ | 粒子衰变时质量变化,不涉及显著运动变化 |

#### 推导过程'''

# 定义新内容
new_content = '''#### 力的统一：一个方程四项展开

宇宙大统一方程的展开形式为：

$$\vec{F} = \frac{d\vec{P}}{dt} = \underbrace{\frac{dm}{dt}(\vec{c} - \vec{v})}_{\text{核力与部分电磁力}} + \underbrace{m\frac{d\vec{c}}{dt}}_{\text{引力与惯性力}} - \underbrace{m\frac{d\vec{v}}{dt}}_{\text{电磁力的另一部分}}$$

**四项物理意义**：

1. **$\frac{dm}{dt}(\vec{c} - \vec{v})$：质量变化产生的力**
   - 对应：核力与部分电磁力
   - 物理机制：质量变化时，光速与物体速度的差值产生力
   - 作用尺度：原子核尺度（核力）、原子尺度（部分电磁力）

2. **$m\frac{d\vec{c}}{dt}$：空间光速方向变化产生的力**
   - 对应：引力与惯性力
   - 物理机制：光速矢量的方向变化产生力
   - 作用尺度：宏观尺度（引力）、所有尺度（惯性力）

3. **$-m\frac{d\vec{v}}{dt}$：物体加速度相关的力**
   - 对应：电磁力的另一部分
   - 物理机制：物体速度变化产生电磁效应
   - 作用尺度：原子尺度

**震撼的统一**：

> **一个方程，四项展开，统一了引力、电磁力、核力与惯性力。**
> 
> 相比之下，标准模型需要61种基本粒子，超弦理论需要十维时空——这里的简洁令人震撼。

#### 推导过程'''

# 执行替换
content = content.replace(old_content, new_content)

# 写回文件
with open('第40章：四种力的统一.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('修改成功完成！')
