# ROOT V144｜统一场论研究攻坚包

**交付性质：运行测试通过的理论数学审计与数值反例工程。四力统一未被证明。**

本版是 V143 的后续，保存了 V143 全部原始 ZIP 供版本追溯。

## 本轮新增

- SU(3) (8 个)、SU(2) (3 个)、U(1) (1 个) 的显式矩阵、结构常数、Jacobi 恒等式测试。
- 在常数非对易方向场中验证非阿贝尔场强，在纯旋转标架中验证场强为零。
- 修正“规范生成元数量等于必须增加的维数”的错误直觉：对比 16D 直接群流形与 12D SU(3) 内流形研究路线。
- 对最简 5D Kaluza--Klein 带电态建立质量下界，定量证明电子质量与精细结构常数冲突约 `10^42`。
- 对紧致正曲率群流形的未扭曲 Dirac 零模给出 Lichnerowicz 不存在性证明。
- 37 项 Python `unittest` + 5 项 SymPy 独立符号恒等式校验，自动写出 JSON、CSV、测试日志。

## 运行

需要 Python 3.10+：

```bash
python -m pip install -r requirements.txt
python run_all.py
```

Windows 双击 `run_windows.bat`；Linux/macOS `sh run_linux.sh`。

## 文件

- `docs/DERIVATION_ZH.md`：完整中文推导、数值对照、已确立事实与尚未证明的命题。
- `docs/ROOT_V144.tex`：可编译的 LaTeX 数学论文草稿（英文，尚不构成可发表的原创突破证明）。
- `src/physics.py`：显式 Pauli/Gell-Mann 矩阵，KK 模型与群流形的计算代码。
- `src/symbolic_checks.py`：独立 SymPy 求导与恒等式检查。
- `tests/test_v144.py`：37 项有明确判据的自动化测试。
- `results/*.json`, `results/*.csv`, `results/tests.log`：每次运行可以重新生成。
- `figures/architecture.svg`：研究路线与障碍示意图。
- `legacy/ROOT_V143_Helix_Fiber_KK_Complete.zip`：上一版本的原始压缩包。
- `manifest.sha256`：归档内容的哈希校验列表。

## 严格结论

1. 几何能提供描述规范场的数学语言，但不能仅凭“光速螺旋 + 三方向垂直”独立推出全部相互作用。
2. 最小 KK 圆纤维的电子质量—电荷映射不成立；修改模型需显式说明新结构，重新求导和检验。
3. 正定双不变群度规上的未扭曲自旋零模存在严格障碍，但允许有扭曲背景的其他紧化思路。
4. 所有自动化通过仅意味着**给定的公式/程序一致**。本包没有实验发现新力、没有证明统一场论，也没有独立计算出 G、ℏ 或标准模型参数。

## 公开参考资料

- NIST CODATA 2022 常数：https://physics.nist.gov/cuu/Constants/
- Internal symmetries in Kaluza-Klein models (2023)：https://arxiv.org/abs/2306.01049
- Lichnerowicz spin Dirac 恒等式（MIT 讲义）：https://math.mit.edu/~rbm/Loops2024/Isaac1.pdf

**单位约定：仅 `c=1`；`ℏ` 和 `G` 保留为独立有量纲常数。** 脚本中出现的 `C_SI` 只是实测数值的 SI 单位换算。
