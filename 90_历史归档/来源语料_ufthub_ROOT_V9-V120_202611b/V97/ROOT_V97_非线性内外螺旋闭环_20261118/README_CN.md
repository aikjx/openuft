# ROOT V97｜从双频弱聚焦到非线性内外周期轨道

日期：2026-11-18。**性质：可复现理论计算和软件审计；未发现新物理定律，未完成统一场论。**

## 本轮进展

1. 严格证明：弱聚焦双向线性频率 `νr²+νz²=1` 同步有理共振等价于正整数勾股三元组；最短是 `4:3:5` 的五圈。
2. 在 V96 的有限截面双线圈、无电流通道下，不预设平面轨道形状，直接由 Maxwell–Lorentz 动力学求解非线性径向呼吸。
3. 对径向振幅 30 μm，通过射击调节参考半径，得到四个径向周期/五次方位旋转的**平面非圆形数值周期轨道**；参考半径约 `5.153022597 mm`。
4. 两种独立计算路线复查：完整 6 维轨迹积分 + 平面正则角动量/径向有效势积分。对源截面求积从 13 到 49 阶检查收敛，明确源误差大于 ODE 返回残差。
5. 维持科学限制：并未获得三维结轨道、辐射反作用自洽稳定性、四力共同作用量或独立预测 G。

## 目录

- `research/ROOT_V97_完整科研总论.md`：推导、数值精算、误差、局限性和文献。
- `research/严格定理与反例.md`：条件性定理、反例和证明状态。
- `ledger/ALL_277_ISSUES.csv` 与 `.json`：V96 的 253 项 + 新增24项；开放项保留。
- `src/coil_model.py`：来自 V96 的有限截面外线圈数值核，带来源注释。
- `src/v97_core.py`：勾股分类、轨道积分、非线性射击、磁通独立复算。
- `src/generate_results.py`：数值扫描和图片生成。
- `src/finalize_results.py`：源截面求积收敛补充与目录校正。
- `src/symbolic_audit.py`：20项符号和 SI 检验。
- `src/build_web.py`：把理论轨道数据生成离线浏览器可视化。
- `results/`：数值数据（`THEORY`）、日志、独立精度报告。
- `plots/`：理论轨道、振幅漂移、半径修正、浏览器截图。
- `tests/`：新增37项 Python 自动测试。
- `web/index.html`：离线动画和数值信息面板；不依赖在线资源。
- `archive/ROOT_V96_original.zip`：完整原始 V96 历史科研包，保留旧版数据证据。

## 安装与运行

Python 3.10+：

```bash
python -m pip install -r requirements.txt
python verify_checksums.py
python run_all.py
```

完整从头生成所有数值、图表和离线页面：

```bash
python run_all.py --regenerate
```

可选：执行原始 V96 ZIP 中的历史单测：

```bash
python run_all.py --historical
```

可选：已有 Chromium 和 Playwright 时运行网页实际检查：

```bash
python web/browser_smoke.py
```

`--regenerate` 会修改结果文件，因此原 ZIP 的 SHA-256 固定快照校验在再生成后自然不再全部匹配；先验证快照，再进行再生成。`run_all.py` 默认验证当前文件内数值数据并运行本轮测试，不强制重做耗时的参数扫描。

## 验收方法和物理限制

- Python 37项新增测试；SymPy/SI 20项；可选 V96 历史36项；实际 Chromium 8项。
- ODE 返回位置残差约 `1.58e-13 m`，仅代表指定离散磁场模型的求解器精度。
- 21阶与49阶截面求积算出的参考闭环半径差约 `3.63e-10 m`，表明源建模误差更大。
- 所有量化结果仅是 THEORETICAL_MODEL，不是实测观测；不能把磁场逆设计或周期轨道识别为“量子引力发现”。
- 螺旋三维挠率、光子传播、强弱规范相互作用与 GR 都没有从本模型自动导出。
