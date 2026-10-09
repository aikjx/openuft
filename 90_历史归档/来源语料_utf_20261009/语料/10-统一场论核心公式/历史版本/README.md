# 统一场论核心公式系统

## 项目简介

统一场论核心公式系统是一个用于计算和验证张祥前统一场论核心公式的Python实现。该系统提供了完整的公式计算、一致性验证、性能基准测试等功能，支持17个核心公式的计算和分析。

## 项目结构

```
├── code/                  # 核心代码目录
│   ├── core_algorithm.py           # 核心算法模块
│   ├── 公式规格数据库.json          # 公式规格数据库
│   ├── 统一场论系统入口.py           # 系统入口脚本
│   ├── test_core_algorithm.py       # 核心算法测试
│   ├── dimension_analysis_data.py   # 量纲分析数据
│   ├── dimension_verification.py    # 量纲验证
│   ├── dimension_verification_fixed.py # 修复版量纲验证
│   ├── visualization_generator.py   # 可视化生成器
│   ├── update_visualization_paths.py # 更新可视化路径
│   ├── helix_3d.png                 # 三维螺旋图
│   ├── helix_3d_fixed.png           # 修复版三维螺旋图
│   └── bak/                         # 备份目录
├── 公式验证/              # 公式验证目录
│   ├── 验证结果/                    # 验证结果
│   ├── README.md                    # 验证说明
│   ├── unified_field_theory_verification.py # 统一场论验证脚本
│   └── 统一场论20个核心公式完整验证脚本.py # 完整验证脚本
├── 公式验证论文/          # 公式验证论文目录
└── README.md             # 项目说明
```

## 核心功能

1. **公式计算**：支持17个统一场论核心公式的计算
2. **一致性验证**：验证公式之间的一致性关系
3. **性能基准测试**：测试各公式的计算性能
4. **可视化生成**：生成公式的可视化结果
5. **量纲分析**：分析公式的量纲一致性

## 已实现公式

1. **01**: 时空同一化方程
2. **02**: 三维螺旋时空方程
3. **03**: 质量定义方程
4. **04**: 引力场定义方程
5. **05**: 动量方程
6. **06**: 运动动量方程
7. **07**: 宇宙大统一方程（力方程）
8. **08**: 空间波动方程
9. **09**: 电荷定义方程
10. **10**: 电场定义方程
11. **11**: 磁场定义方程
12. **12**: 变化引力场产生电磁场
13. **13**: 磁矢势方程
14. **14**: 变化引力场产生电场
15. **15**: 变化磁场产生引力场和电场
16. **16**: 能量方程
17. **17**: 光速飞行器动力学方程

## 系统使用

### 命令行接口

```bash
# 查看系统信息
python code/统一场论系统入口.py --mode info

# 计算所有核心算法
python code/统一场论系统入口.py --mode calculate --verbose

# 验证核心算法一致性
python code/统一场论系统入口.py --mode verify --verbose

# 运行性能基准测试
python code/统一场论系统入口.py --mode benchmark --iterations 100 --verbose

# 保存计算结果到文件
python code/统一场论系统入口.py --mode calculate --output results.json
```

### 编程接口

```python
from code.core_algorithm import FormulaCalculator

# 初始化公式计算器
calculator = FormulaCalculator('code/公式规格数据库.json')

# 计算单个公式
result = calculator.calculate_formula('01', {'t': 1, 'C': [1, 0, 0]})

# 计算所有公式
all_results = calculator.calculate_all_formulas()
```

## 测试

运行测试脚本验证系统功能：

```bash
python code/test_core_algorithm.py
```

测试结果将显示所有公式的计算状态、一致性验证结果和性能基准测试结果。

## 依赖项

- Python 3.7+
- NumPy

## 系统版本

当前版本：3.1

## 功能特性

- ✅ 完整实现17个统一场论核心公式
- ✅ 公式一致性验证
- ✅ 性能基准测试
- ✅ 详细的日志记录
- ✅ 命令行接口
- ✅ 编程接口
- ✅ 测试覆盖
- ✅ 量纲分析
- ✅ 可视化支持

## 使用示例

### 计算时空同一化方程

```bash
python code/统一场论系统入口.py --mode calculate --parameters '{"t": 1, "C": [1, 0, 0]}' --verbose
```

### 验证公式一致性

```bash
python code/统一场论系统入口.py --mode verify --verbose
```

### 运行性能测试

```bash
python code/统一场论系统入口.py --mode benchmark --iterations 1000 --verbose
```

## 注意事项

1. 本系统仅用于学术研究和教育目的
2. 所有公式计算结果仅供参考，实际应用请结合物理实验验证
3. 系统支持自定义参数，可根据具体需求调整计算参数
4. 如有问题，请查看日志文件 `code/uft_system.log` 获取详细信息

## 许可证

本项目采用MIT许可证，详见LICENSE文件。
