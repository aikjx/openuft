# ROOT V135 · 统一场论候选与地月可复算精算工程

**版本**：2026-11-23 ；**研究状态**：数学与程序验证完成有限范围，**未证明四力统一，未发现新引力**。

## 1. 一键复算（Windows / Linux / macOS，Python 3.9+）

在 ZIP 解压后的目录中执行：

```sh
python run_all.py
```

Windows 可以双击 `run_windows.bat`；Linux 使用 `sh run_linux.sh`。无需第三方 Python 包，无需网络、密钥或管理员权限。

此命令将运行 **59 项自动测试**，再重建所有 CSV、JSON、SVG 结果。若测试失败，则退出非零状态。

## 2. 核心结论

- 恒速空间螺旋的几何恒等式 \(\kappa^2+\tau^2=\omega^2\) 可以证明，但不是四力的独立推导。
- 已知的重力与标准模型可以共同写在作用量 \(S\) 中，但将作用量相加不等于证明微观统一。
- 若存在额外的普适 Yukawa 力，其有限分层球源的势、加速度、距离、方向规律可以严格计算。
- 延续 V132 的**假设参数** \(\alpha=1/3\) 与 \(\lambda=124.6\) km 时，示意分层地表候选额外比例地球 **0.62804%**、月球 **3.29459%**。
- 赤道参考重力初步对比出现 **约 0.05846 m/s²** 的候选模型与 NASA 参考值差异。这是需要优先审查的矛盾，不是一个新发现。
- 对假设第五力做了近圆轨道进动计算：地球 400 km 示例约 **0.04557 rad/圈**，是理论预测，未拟合轨道观测。
- 月球质量 \(\mu_{Moon}/G\) 是 JPL 与 CODATA 常数换算的复算，并没有从 ROOT 螺旋独立推导出月球质量。

## 3. 文件结构

```text
ROOT_V135_Unified_Field_Research/
├── README.md                  操作、成果与范围
├── run_all.py                 测试 + 重新生成全部数据
├── run_windows.bat            Windows 双击
├── run_linux.sh               Linux 一键复算
├── src/
│   ├── physics.py             物理函数与解析积分
│   ├── analysis.py            独立数值结果与可视化生成
│   └── audit.py               科学声明防误判门禁
├── tests/
│   └── test_physics.py        55 项单元/反例/数值交叉验证
├── docs/
│   ├── THEORY_ZH.md           中文核心理论、详细公式与警告
│   ├── derivations.tex        可独立编译的 LaTeX 推导
│   ├── VALIDATION_MATRIX.md   测试通过与未完成清单
│   ├── SOURCES.md             NASA/JPL/NIST/EGM/GRAIL 等来源
│   └── NEXT_EXPERIMENT.md     V136 实验验收路线
├── results/
│   ├── earth_moon_altitudes.csv
│   ├── earth_vectors.csv
│   ├── interior_profiles.csv
│   ├── candidate_near_circular_precession.csv
│   ├── density_sensitivity.csv
│   ├── benchmark_earth_equator.csv
│   ├── quadrature_convergence.csv
│   ├── claims_audit.json        科学证据门禁（明确未证明）
│   ├── summary.json
│   ├── run_stdout.txt
│   ├── tests_stderr.txt
│   └── SHA256SUMS.txt         压缩前各文件 SHA256
└── figures/
    ├── yukawa_altitude.svg
    └── yukawa_near_earth_moon.svg
```

## 4. 数据标签

`MODEL_PREDICTION_NOT_OBSERVATION`：预设候选模型计算，不是探测器观测。  
`ILLUSTRATIVE_DENSITY_NOT_PREM_GRAIL`：演示密度剖分，不是 PREM/GRAIL 模型。  
`NOT_PROVEN`：四力统一仍未证明。

## 5. 与 V131、V132 的关系

- 保留 V132 使用的地球示意五层结构和 \(\alpha=1/3,\lambda=124.6\) km 参数作为明确受审假设。
- 修复部分验证工作的可追溯性：新增从分层势精确求导、两种独立积分算法、均匀球闭式解、假设敏感性、月球对照和参数可辨识测试。
- 旧版的示意残差不可当作实测数据。此次输出所有候选项均作明确标注。

## 6. 物理单位约束

**理论只用 \(c=1\)，保留 \(\hbar\)、\(G\) 为独立有量纲常数；计算输入/输出采用观测资料所用的 SI 单位，不改变理论单位约定。**

详见 `docs/THEORY_ZH.md`、`docs/VALIDATION_MATRIX.md` 和 `docs/SOURCES.md`。
