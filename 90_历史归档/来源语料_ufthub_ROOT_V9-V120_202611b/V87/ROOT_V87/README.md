# ROOT V87｜量子力学 × 牛顿 × 爱因斯坦低能统一研究科研包

**科学状态：有限条件下的严格理论衔接与可复现数值验证；没有证明完整量子引力、G 的本源和四力大统一。**

## 最有价值的结果

- **Einstein → Newton**：完整弱场度规的一阶 Einstein 方程恢复 `∇²Φ=4πGρ`；测地线恢复 `a=-∇Φ`。
- **Curved spacetime matter → QM**：Klein–Gordon 取 `e^{-imc²t/ħ}` 非相对论极限恢复 `iħψ_t=(-ħ²∇²/2m+mΦ)ψ`。在均匀场，具有精确加速坐标和相位变换。
- **三角跨理论校核**：理想保持分支的 `Δphase=-mΔΦT/ħ`，静止钟的 `z≈ΔΦ/c²`，经典加速度的 `g=-∇Φ`。必须控制路径、频移和电磁相位。
- **重要无解证明**：只利用同一个 Newtonian 源的 `g` 和 `Δphase`，仍只能测得 `GM`；对未知 `(G,M)` 的灵敏度 Jacobian 行列式为 0。
- **半经典自引力审计**：高斯波包 Poisson 势、质量归一化、独立自能积分、变分极小值；Schrödinger–Newton 作为**条件模型**，不是单粒子自引力基本定律。
- **量子引力判据**：低能 EFT 展开与双系统相位不变量可用于提出可检验假说，但纠缠并不在无额外假设时唯一判定量子几何。

## 目录

```
ROOT_V87/
  README.md, PROOF_STATUS.md, SOURCES.md, RELEASE_NOTES.md, HISTORY_V86.md
  book/ROOT_V87_量子力学_牛顿_爱因斯坦_极限统一与量子引力审计.md
  src/bridge.py                         # SI constants + physics core
  tests/test_bridge.py                  # numbered Python unittest tests
  tests/symbolic_checks.py             # analytic checks with SymPy
  scripts/generate_results.py          # reproducible theory/synthetic data and PNG plots
  scripts/build_catalog.py             # equation catalog creator
  scripts/build_protocols.py           # experiment protocols creator
  web/index.html                       # fully offline interactive scientific UI
  web/browser_smoke.py                 # Chromium functional tests
  data/*.csv                           # equation/method catalog and theory/synthetic curves
  protocols/*.json                     # scientific protocols, none used on equipment
  results/*.json, *.png                # test reports, plots and browser screenshot
  archive/ROOT_V86.zip                 # previous research archive for continuity
  run_all.py, RUN_WINDOWS.bat, RUN_LINUX.sh, requirements.txt
  SHA256_MANIFEST.csv, VERIFY_REPORT.json
```

## 安装和运行

Python 3.10+，联网安装依赖（首次安装时）：

```bash
python -m pip install -r requirements.txt
python run_all.py
```

也可以仅做独立检查：

```bash
python -m unittest discover -s tests -p 'test_*.py' -q
python tests/symbolic_checks.py
python scripts/generate_results.py
```

使用 `web/index.html` 在浏览器打开交互实验室，不需要联网或 Python。Windows 运行 `RUN_WINDOWS.bat`；Linux/macOS 使用 `bash RUN_LINUX.sh`。

在 Linux Chromium 环境可额外运行：`python web/browser_smoke.py`。它依赖 Playwright 的 Python 发行包与 Chromium 浏览器，**不会连接仪器或进行新物理测量**。

## 避免误解

1. 已测试的程序仅证明公式与代码在所述模型假设下相容。
2. 实验协议中的 hardware control 是未来实验设计，不附带任何仪器驱动。
3. `data/synthetic_source_switch.csv` **全部是程序模拟，非实际观测**。
4. 任何关于 Planck 长度/质量的数字**以实测 G 为输入**，不能反向作为 G 的独立预测。
5. 本包的可检验突破是**一致性、有限高度和不可辨识性条件**，不是已经攻破量子引力。
