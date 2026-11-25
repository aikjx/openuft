# ROOT V134 — 运行说明

**状态**：严格审查与示例，不是统一场论证成。2026-11-24。

1. Windows 命令行：进入本目录，运行 `python verify_v134.py`（Python 3.9+）。
2. Linux：`python3 verify_v134.py`。
3. 输出位于 `data/verification_results.json`、`data/kk_circle_spectrum.csv`、`data/monopole_flux_index.csv` 与 `data/vacuum_curvature_examples.csv`。
4. 双击 `交互审查面板.html` 可离线改变假设半径与量子通量数。
5. `核心公式.tex` 不依赖任何特殊 ROOT 宏；可复制到已有 LaTeX 文档。若编译，应使用完整的 LaTeX 文档环境与常见数学宏包。
6. `历史研究包/` 中的早期研究只作原始归档；其数学和外部引用不代表 V134 独立重新验证过。
7. `SHA256SUMS.txt` 中的哈希适用于目录内文件（不含哈希文件自身）。

仅使用 `c=1`；所有测试中 `HBARC_GEV_M` 为 **从 SI 转换物理结果** 的数值常数，不是理论推导中设定 `hbar=1` 或 `G=1`。所有可观测新效应尚无本模型独立预测。
