# ROOT V96｜外部有限截面电流与无源通道中的弱聚焦内外闭环

**性质**：数学推导 + 已知 Maxwell–Lorentz 物理模型 + 数值验证 + 反例审计。**不是完整统一场论，不是实际建成的实验装置。**

## 本轮与 V95 的实际区别

- V95：紧支撑逆向构造，目标轨道可以精确实现，但源电流可能贯穿粒子通道，小扰动不稳定。
- V96：明确的外部双线圈，离粒子轨道 8.434 mm，通道 `J=0`；已知弱聚焦机制令小扰动在径向/轴向振荡。
- 几何内外闭环：真正的径向往复来自 Maxwell–Lorentz 方程，而不是预设参数曲线。一般为准周期，特殊线性共振可五圈相位重合，但全非线性仍不必精确闭合。

## 文件

`research/` 含科学总论、15 条定理/反例；`src/coil_model.py` 为连续电流截面求积与 relativistic ODE；`src/generate_results.py` 为100圈积分、频率拟合、返回矩阵及散度/旋度验证；`src/symbolic_audit.py` 为符号和 SI 量纲检查；`tests/` 为测试；`results/` 和 `plots/` 全部标 `THEORY`；`ledger/ALL_253_ISSUES.csv` 延续 V95 的 229 项并追加24项；`archive/ROOT_V95_original.zip` 为 V95 的原始历史交付，保留未修改的科研来源。

## 一键复现

Python 3.10+，建议隔离虚拟环境：

```bash
python -m pip install -r requirements.txt
python verify_checksums.py       # 检验原始归档；必须在重新生成前运行
python run_all.py                # 符号审计、自动测试、数值和文档台账核验
```

Windows：`RUN_WINDOWS.bat`。 Linux/macOS：`sh RUN_LINUX_MAC.sh`。

**精度注意：** 源截面有限，但数值求积通过若干理想圆环核实现。有限个环核的场自能不能当作真实连续线圈的有限能量；本轮有限自能证明针对平滑有限截面的**连续分布**。数值模型仅对不与导体相交的粒子区域做高精度计算。

**工程注意：** 约 656 A/线圈、5.18×10^8 A/m² 峰值电流密度，以及理想铜约 493 W 热耗估计说明现阶段不是现成安全可制造装置；未进行电磁兼容、冷却、绝缘和人员安全设计。
