# ROOT V151 — 精算与复核报告

## 运行环境

- Python 3.13.5, NumPy 2.3.5, SymPy 1.14.0, Matplotlib 3.10.8。
- 所有计算均在本轮真实执行。无需互联网访问即可重跑。

## 实际执行

- `python -m unittest discover -s tests -v`: **74/74 通过**，详情 `results/unittest.log`。
- `python symbolic_audit.py`: **22/22 通过**，详情 `results/symbolic_audit.json`。
- `python generate_results.py`: **成功生成** 2 个 CSV、1 个数值 JSON、3 张 PNG；SymPy 额外存储 `results/symbolic_audit.json`。
- `chern_number_numeric(n_grid=60,σ=+1)`: **+2.000000...**（数值积分）。
- `chern_number_numeric(n_grid=60,σ=-1)`: **−2.000000...**（数值积分）。
- 解析值 `C_σ=2σ`，两种离散积分与结果一致。
- 两种极化的平面波 `∇·E=∇·B=0`，`∂tE−∇×B=0`，`∂tB+∇×E=0` 的符号残差为 0。
- `A_μ=∂_μψ` 的 `F=d²ψ=0` 符号核验通过。
- 任意单对 Euler 标量 `F=dq∧dp` 的 Pfaffian 恒等为 0。

## 测试与实验的区别

上述全是**数学、程序一致性或模拟参数测试**。没有通过真实粒子/地月实验验证 ROOT 的新物理机制；不保证模型的四力统一完备性。之前版本中 α、地月质量的实验参考值均不能作为从 ROOT 独立预测出的结果。

## 精度与不确定度

- 解析恒等式用 SymPy 核验，数值积分用 Gauss–Legendre 求积，有限差分测试采用明确误差容差。
- `α` 来自 NIST CODATA 2022，是观察参考值，**没有反向调参给本轮模型做“预测”**。
- 极点处球面偏振基底不能用单张光滑坐标图覆盖；代码用局部坐标和二图跃迁绕过该坐标奇性。
- 数值绘图仅供物理理解，不是独立实验数据。

## 可复现命令

```bash
python -m pip install -r requirements.txt
python run_all.py
python verify_manifest.py
```

## ZIP 可靠性

使用 ZIP CRC、文件哈希清单以及独立临时解压后运行 `run_all.py`、`verify_manifest.py` 进行验证（详细结果由当前构建脚本现场输出）。为避免不同 Matplotlib 版本引起 PNG 元数据或抗锯齿像素变化，`manifest.json` 只锁定静态源码、文档、脚本和历史原包，不锁定自动再生的 `results/` 与 `figures/`。
