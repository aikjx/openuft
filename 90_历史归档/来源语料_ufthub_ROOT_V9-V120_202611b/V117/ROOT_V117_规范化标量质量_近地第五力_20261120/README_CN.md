# ROOT V117｜统一场论 · 标量质量 / 近地第五力全链路科研包

**科研定位：** 重点检查 ROOT V116“给单实标量增加质量能否修复长程引力冲突”的独立动力学来源；不将数学正确、模型可算与自然界已证实混淆。

## 本轮实际修复

1. 不再把“标量质量”当作不受约束的额外自由数，而是从唯一指定的 Jordan 作用量 `F=ξφ²` 和 `V_J=λ₄(φ²−v²)²/4` 推导标准化质量。
2. 从完整的 Weyl 变换给出精确 `χ`、Einstein 势能 `U_E` 和普遍物质耦合 `A(χ)`。
3. 固定 V116 的 Newton 归一化，得到 λ₄=1 时第五力作用程约 124.6 km，强度约 1/3。
4. 在地球半径远大于作用程时，不再错误使用点质量源；加入均匀球与 `ρ∝1/r` 的解析球体外场及安全数值计算。
5. 明确“绝对 G 的实验归一化吸收近距离常数增强”的区别；真正可测的是不同距离的曲线形状。
6. 执行 SymPy 独立证明、65位 mpmath 源积分验证、自动参数扫描、Chrome 交互与历史回归。

## 一键复算

进入本目录，安装依赖：

```bash
python -m pip install -r requirements.txt
python run_all.py
python -m unittest discover -s tests -p 'test_v117.py' -v
```

`run_all.py` 重新计算 `results/V117_NUMERICAL_RESULTS.json` 并生成四张独立理论图。浏览器页直接打开 `web/index.html`（无须互联网、数据库或外部服务器）。

浏览器自动测试是可选工具，需要 Chromium/Playwright：

```bash
python -m pip install playwright
python tests/browser_smoke.py
```

测试不会覆盖归档截图，只有手动运行 `python tests/browser_smoke.py --capture` 时才会写入新截图。

## 结构

- `research/01_ROOT_V117_完整科研总论.md`：全部推导、数值、适用假设和外部参考
- `research/02_六项定理_反例_复算.md`：六项模型内定理、反例
- `research/03_396项OPEN_关键验收.md`：历史根本未解项目和下一版可证伪路线
- `src/model.py`：稳定、无溢出的第五力、球体解析解
- `tests/test_v117.py`：59项 Python/SymPy/高精度独立测试
- `figures/`：四张科研图 + 浏览器实测截图
- `archive/ROOT_V116_original.zip`：V116 原始历史包，包含前代归档
- `ledger/V117_ALL_396_PRESERVED.csv`：原样保留 V116 的396项台账
- `CHECKSUMS.sha256`、`MANIFEST.json`：下载前后可验证来源的文件清单

## 不得过度解释

- `v=0.087827...GeV` 是固定五味单圈 QCD 的数学示范尺度，将其认作独立实标量真空期望值尚未证明。
- ξ 从**实验 G 校准**得到；本包没有推导出 G。
- 地球两种球模型均不是现实地球密度，也未进行真实观测似然拟合，不能宣称第五力已发现或已排除。
- V117 **没有**导出 SU(3)×SU(2)×U(1)、三代粒子质量谱或量子引力 UV 完备性。

版本日期：2026-11-20。
