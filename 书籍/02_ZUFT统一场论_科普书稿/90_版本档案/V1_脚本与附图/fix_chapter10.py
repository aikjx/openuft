import re

# 读取文件
with open('第10章：空间的几何属性.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 定义要插入的新内容（在总结部分之后、思考问题之前）
new_content = '''
### 与统一场论核心理论的联系

统一场论中的"空间的几何化"是理解几何属性的关键：

1. **双层螺旋结构**：
   - 空间以光速作圆柱螺旋运动
   - 每一层贡献4π立体角
   - 双层结构形成8π的几何因子

2. **几何常数Z**：
   - Z = Gc/2：引力的几何基础
   - Z' = c/(8πε₀)：电磁的几何基础
   - Z被解释为"单位四维时空体积内空间位移条数的流量密度"

3. **空间的本质**：
   - 空间的几何属性不是抽象的数学概念
   - 而是空间螺旋运动的直接表现
   - 质量、电荷、力都是空间几何的派生量

**深刻启示**：

> **空间不是被动的背景舞台，而是以光速螺旋运动的动态实体。**
>
> 所有物理现象（引力、电磁、核力）都可以归结为空间几何的不同表现方式。

'''

# 找到"## 思考问题"的位置（大约在226行）
target_line = -1
for i, line in enumerate(lines):
    if '## 思考问题' in line:
        target_line = i
        break

if target_line != -1:
    # 在思考问题之前插入新内容
    lines.insert(target_line, new_content + '\n')
    # 写回文件
    with open('第10章：空间的几何属性.md', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f'✅ 修改成功完成！已在第{target_line}行之前添加与核心理论的联系。')
else:
    print('❌ 未找到"## 思考问题"行')
