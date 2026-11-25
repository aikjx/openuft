# ROOT V142 — 从螺旋旋转到真实光子传播的最小判据

**研究状态：数学建模与符号/数值程序验证，未证明四力统一。**

## 本轮实际结果

- 非交换三维旋转标架的完整 Maurer–Cartan 曲率严格为零。
- 同一标架的投影几何曲率可非零，但并不能独立保证 Maxwell 动力学。
- 修复 V140 圆偏振电磁波的磁场方向错误，并用两个 Maxwell 旋度方程精确交叉检查。
- 从规范约束给出 Maxwell 两个与 Proca 三个物理偏振自由度。
- 证明标量对复合场在常量背景周围不具备普通的二次传播作用量。
- 严格仅采用 `c=1`，不将 `hbar`、`G` 无量纲化。

## 一键运行

Python >= 3.10；需要 `numpy`, `sympy`；绘图可选 `matplotlib`。

```bash
python -m pip install -r requirements.txt
python run_all.py
python create_figure.py
```

Windows 双击 `run_windows.bat`；Linux/macOS 使用 `sh run_linux.sh`。

`run_all.py` 输出 `results/tests.log`, `results/summary.json`, `results/symbolic_results.json`。

详细计算说明：`docs/DERIVATION_ZH.md`，LaTeX：`docs/ROOT_V142.tex`。图示：`figures/polarization_helix.png`。

`legacy/ROOT_V141_Helix_Dynamics_Complete.zip` 为上一版归档，用于追溯，不代表已对旧版全部测试重跑。

## 科学边界

目前不存在能够从这套特定螺旋运动学独立导出引力、电磁力、弱相互作用、强相互作用、所有耦合常数和粒子质量的完整证明；本轮严格的数学结果不能代替实验验证。后续应给出独立动力学、正则约束分析、对称性和真正区别于现有理论的观测预测。
