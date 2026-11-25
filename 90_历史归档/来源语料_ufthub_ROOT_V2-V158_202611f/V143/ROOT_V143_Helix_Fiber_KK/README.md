# ROOT V143 — 光速螺旋与圆纤维几何的统一候选：数学审计

**交付性质：完整可运行数学研究包，不是四力统一证明。** 使用 `c=1`，始终保留 `ℏ` 和 `G` 的量纲。

## 完成的工作

1. 将原先三维光速螺旋推广为五维零间隔轨迹，严谨修正曲率/挠率与角频率恒等式。
2. 用既有 Kaluza–Klein 圆纤维度规从几何产生独立的 U(1) 规范连接与二次 Maxwell 场强作用量。
3. 在均匀磁场的非平凡例子中，**直接计算五维 5×5 度规的 Christoffel 符号及 Ricci 标量**，确认公式。
4. 从 Maxwell 场检验两个横向偏振，符号验证齐次与非齐次方程的真空解。
5. 从半径变分揭示纯五维真空理论不能一般性地冻结内部半径；否则需 `F²=0`。
6. 推导最简模式的 `α=4Gm²/ℏ`，并使用 CODATA 参考值发现不能将电子直接当成最简单的带电 KK 质量模态。
7. 完整 unittest、SymPy 符号检验、JSON/CSV、图表、LaTeX、Windows/Linux 一键运行。

## 一键运行

需要 Python 3.10+ 和 SymPy。

```bash
python -m pip install -r requirements.txt
python run_all.py
```

Windows 可运行 `run_windows.bat`，Linux/macOS 运行 `sh run_linux.sh`。

主文档：`docs/DERIVATION_ZH.md`。公式 LaTeX：`docs/ROOT_V143.tex`。
结果：`results/summary.json`, `results/symbolic.json`, `results/mass_coupling_scan.csv`, `results/tests.log`。
旧版归档：`legacy/ROOT_V142_Helix_Polarization_Complete.zip`。所有成果均为对给定数学模型的精确计算与测试，不含真实第五力观测拟合或已验证的新基本力。

## 已知不足（不可称“统一场论完成”）

- U(1) 是借助新增加的内部圆坐标和独立度规场得到的，**不是由原来的三方向正交与曲率/挠率唯一推出**。
- 无 SU(2)、SU(3)、手征费米子、正确的电子质量、电荷谱、耦合常数演化和量子引力完整理论。
- 固定半径的降维并非无条件的一致截断；需独立稳定化证明。
- 电子与最简 KK 模态的质量-电荷数值差距约 **42 个数量级**。
- 所有测试为代码/符号/数学性质验证，**不等于新理论已获实验证实**。
