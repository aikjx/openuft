# ROOT V134｜非阿贝尔内部几何与统一场论审计

这是一份可离线运行的**理论数学审计**资料，承接 ROOT V133 内部相位世界线模型。

- 单位：**只有 `c=1`**；`ℏ`、`G`、`ε₀` 没有设为 1。
- 可得结论：一维内部复相位表示障碍；非阿贝尔场强；纯局部标架联络的零曲率；Wilson 回路；Wong 内部荷；一代标准模型异常条件。
- 不可得结论：从空间螺旋直接预测 `α`、粒子质量、`G`、`ℏ`；发现第五力；完成四种相互作用的统一。

## 文件目录

```text
ROOT_V134/
├── README.md
├── reports/
│   ├── ROOT_V134_统一场论非阿贝尔几何与量子一致性_科研报告.md
│   └── ROOT_V134_最核心方程与不可突破的数学边界.md
├── src/
│   ├── root_v134.py
│   ├── property_audit.py
│   └── make_figures.py
├── tests/test_root_v134.py
├── results/
│   ├── tests.log
│   ├── numeric_results.json
│   ├── color_precession.csv
│   ├── random_property_audit.json
│   └── random_property_audit.log
├── figures/ (3 张数学图)
├── previous/ROOT_V133_原始归档.zip
├── run_verification.sh
├── run_verification.ps1
└── manifest.sha256
```

## 环境

Python 3.10+；依赖 `numpy`, `scipy`, `matplotlib`。测试仅依赖 `numpy`/`scipy`。

```bash
python -m pip install numpy scipy matplotlib
python -m unittest discover -s tests -v
python src/root_v134.py
python src/property_audit.py
python src/make_figures.py
```

或直接运行 Linux `bash run_verification.sh` / Windows PowerShell `./run_verification.ps1`。

**本轮实际已运行：45 项单元测试；1000 组随机样本、每样本 5 类数学性质，共 5000 次数值性质检查；3 张数学图。** 通过不代表通过物理实验。

## 科研证据等级

- **MATH**：在定义明确的规范场模型中，解析恒等式可严格证明。
- **NUMERIC**：有限精度浮点计算独立复核解析式与误差。
- **MODEL**：引入新的内部维度、群表示和规范耦合属于额外假设。
- **EXPERIMENT**：未获取粒子、天文或引力的新实测数据；物理新发现未成立。

## 归档真实性

本 ZIP 包含 V133 原始归档，保留此前研究链。归档不等于旧版全部自动测试在本轮重新运行；本轮只报告实际运行的 V134 测试与性质检查。
