# ROOT V139 · 光速螺旋 → 几何规范场：可复算研究包

**研究状态：螺旋/几何规范场的数学验证通过；四力统一尚未证明。**

- 单位：仅 `c=1`，保留 `ℏ`、`G` 的独立量纲。
- 完整中文推导：`docs/ROOT_V139_derivation_zh.md`
- 可编辑 LaTeX：`docs/ROOT_V139.tex`（不附带编译工具，直接编辑）
- Python 源码：`src/model.py`、`src/verify.py`、`src/symbolic.py`、`src/dimensions.py`
- 自动化测试：`tests/test_model.py`
- 数值 CSV + JSON：`results/`
- 图示：`figures/`
- 上版归档：`legacy/ROOT_V138_Helical_Geometry_Complete.zip`，包含更早各版本历史文件。

## 一键运行

Windows 双击 `run_windows.bat`；Linux/macOS 执行 `bash run_linux.sh`；通用命令：

```bash
python run_all.py
```

核心数值测试仅依赖 Python 标准库。若安装 SymPy 还运行解析证明检查：

```bash
python -m pip install sympy
python src/symbolic.py
```

所有工具均可离线运行；不会调用真实卫星接口，不会模拟为已进行实测拟合。

## 主要完成内容

1. 螺旋曲率、挠率和角速度的**双向重建**、三方向正交、非测地线判据。
2. 洛伦兹 boost 验证，区分轨迹几何角速度与量子波频率。
3. 内部 spinor 的 Berry U(1) 连接、曲率、Chern 数及定向场的时空拉回。
4. 证明单个方向场 Berry 形式必有 `F∧F=0`，无法覆盖 `E·B ≠ 0` 的通用电磁场。
5. 两个独立方向场相加可消除局部 Pfaffian 障碍，但尚未得到 Maxwell 方程。
6. 最小 U(1) Stückelberg 动力学例子，规范变换、场方程及带质量矢量的限制。
7. 审计并明确区分：数学恒等式、合成数值、待验证假设和已经被反例排除的强版本假设。

## 特别说明

V139 **没有**：从单一螺旋推导四种力、独立预测精细结构常数/引力常数、真实地月观测联合反演、量子一致性证明。早期 ROOT 候选第五力的显著额外地表引力仍存在实验一致性障碍。
