# ROOT V90｜统一场论攻坚科研 ZIP（2026-11-18）

**立即可复现的科研工程包**。承接用户上传的 ROOT V86—V89 研究记录，进一步完成量子双质量四分支模型的严格数学推导、Yukawa 新力长程极限、可辨识性、误差分析和离线交互实验室。

> **研究诚信**：本包完成的是数学/程序/合成模拟攻坚，**不是四力统一已解决**，也不是第五力或引力子被实测。所有数据标为 THEORY / SYNTHETIC。

## 目录导览

| 文件/目录 | 用途 |
|---|---|
| `research/ROOT_V90_研究总论.md` | 多章节科研总论、结果与科学裁定 |
| `research/证明_四分支核与Yukawa高阶消零.md` | 完整数学证明与边界 |
| `research/方法矩阵.csv` | 多路线、必要条件与失败条件 |
| `research/实验协议_量子双体及控制.md` | 可证伪实验设计 |
| `research/来源与局限.md` | 2025—2026 文献与来源范围 |
| `src/root_v90.py` | SI 几何、势核、相位、数值与可辨识性计算 |
| `src/symbolic_audit.py` | SymPy 代数恒等式 |
| `src/simulate.py` | 121 个参数扫描、90 位核算与合成数据 |
| `tests/test_root_v90.py` | 可单独复现的 Python 单元测试 |
| `web/index.html` | 可离线双击运行的互动理论实验室 |
| `web/browser_smoke.py` | 可选 Chromium UI 烟测 |
| `results/` | 理论数据、合成零假设、验收与 UI 截图 |
| `figures/` | 数值理论曲线图 |
| `archive/V89_uploaded_context.txt` | 本次实际上传的历史会话文本 |
| `CHECKSUMS.sha256` | ZIP 内文件完整性校验（不含该文件自身） |

## Windows 一键

解压后双击 `RUN_WINDOWS.bat`，或者在命令行运行：

```bash
python -m pip install -r requirements.txt
python run_all.py
```

## Linux / macOS

```bash
python3 -m pip install -r requirements.txt
python3 run_all.py
```

必要模块：numpy / sympy / matplotlib / mpmath；Python 3.10+。所有输入数据和程序都在 ZIP 内；安装依赖需要软件包源，安装完成后主计算无需网络。只检查数学或回归测试时运行：

```bash
python -m unittest discover -s tests -v
python src/symbolic_audit.py
```

## 可操作界面

双击 `web/index.html`，独立浏览器即可离线操作。如果设备允许，可以运行可选的 `python web/browser_smoke.py`（需额外安装 Playwright，且 Chromium 的路径须适配环境）。浏览器测试只证明 UI 运行，不构成物理验证。

## 关键发现

四分支核 $F[f]$ 是相互作用二阶径向导数的积分，故消去常数与线性势项。Yukawa 与牛顿四分支核的差异在长程极限中首现于 $\lambda^{-3}$。仅靠测量相同的 $1/r$ 形状无法拆分 Newton 与 Coulomb 幅度；使用电荷反转需要可展开、带符号的相位，而不是 concurrence。

## 最终状态

- 已实现：数学定理、对应数值核、参数扫描、合成零假设模拟、视觉实验室、可复现测试。
- 未实现：真实量子双体实验、独立从根本作用量求 G、四力规范大统一、UV 完备量子引力、可实测量子引力圈修正。
- 与 V89 的“历史归档”的关系：用户只上传了 V89 会话文本，未在本次任务中提供早期 ZIP 的二进制；**本包没有虚构或替换未取得的 V86—V89 源文件**。
