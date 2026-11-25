# ROOT V140｜光速螺旋·内部正交·复合规范场动力学精算

**本项目是可复算数学研究工程，不是已经证实的统一场论。**

## 关键结论

1. 理想光速螺旋满足 κ²+τ²=ω²（仅 c=1）。
2. 两对内部方向变量产生 F=dq₁∧dp₁+dq₂∧dp₂，自动有 dF=0。
3. 从 Maxwell 型作用量变分后，只能获得 J·dq_a=J·dp_a=0。当四个内部梯度独立时，才推出 J=0。
4. **严格反例**：B=(cos 2z,sin 2z,0)、E=0 满足全部内部标量方程，且应力能量守恒，但 J=(0,2cos 2z,2sin 2z,0)≠0，不符合无源 Maxwell。这说明仅靠运动正交和守恒不够。
5. **正例**：圆偏振无源平面波的电磁场方向旋转，但传播路径是直线，不要求光子实际走螺旋轨迹。
6. 目前不能从本模型独立推出强弱规范群、精细结构常数、G 或完整引力理论。

## 环境

- Python 3.10+；唯一第三方运行依赖：`sympy>=1.12`。
- 可选生成可视化：`numpy`、`matplotlib`。
- 无需联网、无需管理员权限、无需服务器。

## 一键运行

Windows 双击 `run_windows.bat`，Linux/macOS 执行 `./run_linux.sh`；或：

```bash
python -m pip install "sympy>=1.12"
python run_all.py
```

## 验证结果

参见 `results/test_run.log`（程序真实执行后生成），`results/symbolic_results.json`，`results/wave_sample.csv`。
中文详细推导 `docs/DERIVATION_zh.md`；TeX 文件 `docs/ROOT_V140.tex`。
`legacy/` 中保留 V139 ZIP，不用旧版本冒充本轮验证。

## 物理底线

- 严格采用 c=1；**不**设 ℏ=1 或 G=1。
- 一切“通过”只表示列明的数学和程序测试通过。
- 不把理论拟合或示意密度模型称为独立实验证据。
