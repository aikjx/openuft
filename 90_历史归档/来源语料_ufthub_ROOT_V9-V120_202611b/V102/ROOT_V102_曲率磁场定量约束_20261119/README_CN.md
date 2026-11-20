# ROOT V102｜可复现科研包（中文使用手册）

本包内容：V100 历史理论轨道的独立曲率—横向磁场反演；闭合空间结的磁场必要下界；磁场平方积分与经典辐射等价式；轨道曲率波动与辐射 Cauchy 超额的精确关系。**全部为条件理论与数值模拟，未解决四力统一、量子引力或 G 的来源。**

## 环境
Python 3.10+。依赖 `numpy`、`scipy`、`sympy`、`matplotlib`、`pytest`。

## 一键运行
Windows：运行 `RUN_WINDOWS.bat`；Linux/Mac：`sh RUN_LINUX_MAC.sh`。
命令行：

```bash
python -m pip install -r requirements.txt
python run_all.py
```

其中 `run_all.py` 重建数值报告、CSV、两张理论图表，执行 9 项符号/量纲检查和 41 项 Python 测试。

## 数据来源
`data/V100_ORBIT_21Q_INPUT_THEORY.csv`：V100 21 阶线圈数值轨迹的 1201 个位置点，直接从 V101 保存的历史副本提取。`data/V100_RADIATION_INPUT_THEORY.json` 是历史理论辐射参考值。另有 `archive/ROOT_V101_original.zip` 保留原始科研包。**不是实验数据。**

## 结果目录
- `results/V102_SUMMARY_THEORY.json`：磁场、曲率、辐射、误差、证据等级。
- `results/V100_RECONSTRUCTED_B_PROFILE_THEORY.csv`：沿闭合轨道的曲率、所需横向磁场值。
- `results/BETA_SCAN_THEORY.csv`：不同速度的理论比较。
- `results/GEOMETRY_SAMPLING_CONVERGENCE_THEORY.csv`：不同采样密度误差审计。
- `results/INDEPENDENT_GEOMETRY_CONTROLS_THEORY.csv`：圆环、两种环面结、V100 轨道的对照。
- `figures/*.png`：理论图，不是实验照片。
- `ledger/ALL_357_ISSUES.csv`：继承 349 项并新增 8 项任务。

## 科学结论与限制
局部横向 B 与曲率的对应是已有 Lorentz 方程的严格推论；B 的平行分量、全局 Maxwell 源、连续场周期轨道的存在性、结类型、长期稳定性和辐射反馈都不能从单条几何轨迹推出。任何 4π 非平凡结下界在用于 V100 连续场轨道前必须先有严格嵌入与非平凡结证书。

## 复现安全
数据生成与测试完全离线，除安装依赖外不需网络。对 ZIP 做了 SHA-256 和独立解压复测（见 `VALIDATION_REPORT.md`）。
