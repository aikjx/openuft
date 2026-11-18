# ROOT V76｜微观现象、能动张量累加与引力本源研究包

**版本**：2026-11-17 · **状态**：科研工程完成；四力统一及 G 无参数预测仍未证明。

## 核心科学结论

1. 微观现象形成引力源的正确计算对象是**总物质作用量对度规的变分**，得到完整 `T_{μν}`，含相互作用及支持应力；不能把所有力或束缚能随意相加。
2. 电磁场可矢量叠加；电磁能量是二次的，含 `ε₀ E₁·E₂+B₁·B₂/μ₀` 交叉项。
3. 交变电磁场已有 GR 引力效应，但不是 G 数值的独立解释；封闭电池与磁场之间的内部能量转移不改变装置总能量。
4. 核结合、QCD 质量、热能、光子能动量、量子相干都需要按完整系统的状态与边界计算；重复计数无效。
5. 空间光速螺旋的曲率挠率可严格求导，但目前没有由其无参数独立预测 `G`、标准模型规范群和粒子谱的新物理证明。

## 目录

```
ROOT_V76/
├── README.md / PROOF_STATUS.md / SOURCES.md / RELEASE_NOTES.md
├── book/ROOT_V76_微观现象融合引力本源与累加法_研究专著.md
├── src/microgravity.py                 # 零第三方依赖、SI 单位、测试版物理核心
├── tests/test_microgravity.py          # 75 项数学、数值和守恒测试
├── tools/
│   ├── generate_results.py             # CSV/JSON/PNG 批量生成
│   ├── build_catalogs.py               # 50条方程 + 30条方法
│   ├── symbolic_checks.py              # 8项可选 SymPy 独立核验
│   └── browser_smoke.py                # 16项 Chromium 离线交互检查
├── data/                               # 31类微观现象表、方程/方法目录、4组数据表
├── results/                            # PNG 图、浏览器截图、报告和数值摘要
├── web/index.html                      # 无网络依赖的五模块交互实验台
├── run_all.py / run_all.sh / RUN_ALL.bat
└── SHA256_MANIFEST.csv                 # 完整性校验
```

## 一键复算

**Windows**：双击 `RUN_ALL.bat`，需要 Python 3.10+（计算核心不依赖外部包）。

**Linux/macOS**：

```bash
sh run_all.sh
```

或手动：

```bash
python run_all.py --generate
python tools/symbolic_checks.py        # 可选 pip install sympy
python tools/browser_smoke.py          # 可选 pip install playwright，及 Chromium
```

图片绘制可选 `pip install matplotlib`；即使无 matplotlib，脚本仍输出 CSV 和 JSON。使用 `web/index.html` 时直接通过浏览器打开即可，无服务器、CDN 或网络。

## 验收语义

- **75/75 单元测试**：验证已给定物理模型的程序实现和限值。**不是**对新物理的实测验证。
- **8/8 符号检查**：用 SymPy 检查解析等式。
- **16/16 浏览器检查**：五页切换、滑块、交叉能、能量账本和量子参数测试；**Canvas2D**，不称为 WebGL3D。
- **ZIP 哈希与解压复运行**：检查打包工程可完整重现。

## 数值口径

- 常数采用 NIST CODATA 2022 (G 是实验测量的外部输入)。
- `1 m³, B=10 T` 计算理想均匀场能量 `~3.979×10⁷ J`、质量当量 `~4.427×10⁻¹⁰ kg`；**不能**直接当作真实磁体系统产生的可测额外引力。
- 半径1m球、10T、距中心2m的数值仅为对额外球形能量分布应用弱场远场引力单极的示意，忽略磁场边界和线圈、支架的质量/应力。
- 物理试验需由真实独立仪器开展。研究包不包含或伪造任何实验传感器数据。

## 研究结果、开放问题与归档

完整推导和失败条件见 `book/`，证明状态见 `PROOF_STATUS.md`。为方便追溯，`archive/` 保留 V75 电磁引力专项研究包作为历史材料，**不重复计为 V76 新测试数**。
