# ROOT V75｜变化电磁场产生引力的严格物理审计与数值科研包

## 先看结论

- **已证实的理论机制：** 在广义相对论中，静态和动态电磁场的能量、动量和应力都会通过 \(T_{\mu\nu}\) 参与引力场方程。
- **未证实的论断：** 电磁场“变化”是普通引力的唯一来源；\(\dot B\) 能无参数决定普适引力常数 \(G\)；由这一命题已经实现四力统一。
- **研究实现：** 完成 Einstein–Maxwell 标准理论分析、交变磁场感应能量推导、拟议标量–光子作用量的条件场方程、定量扫描与程序反例，附完整离线实验页面。

## 核心内容

```text
ROOT_V75/
├── README.md                          运行手册
├── PROOF_STATUS.md                   证明状态与科学界限
├── SOURCES.md                        研究来源与网址
├── book/
│   └── ROOT_V75_变化电磁场与引力起源_严格推导研究专著.md
├── src/
│   └── em_gravity.py                 纯标准库 SI 数值核心
├── tests/
│   └── test_em_gravity.py            41项数学和算法单元测试
├── tools/
│   ├── generate_results.py           生成CSV及PNG
│   ├── symbolic_checks.py            5组SymPy符号推导校核
│   ├── create_catalogs.py           50条方程、30项因素矩阵
│   └── browser_smoke.py             10项Chromium交互测试
├── data/
│   ├── ROOT_V75_核心方程与证明状态.csv
│   ├── ROOT_V75_多维影响因素与实验控制矩阵.csv
│   └── 参数扫描数据CSV
├── web/
│   └── index.html                    无需服务器/网络依赖的可交互网页
├── results/
│   ├── numerical_summary.json
│   ├── browser_smoke.json
│   ├── V75_交互网页实际截图.png
│   ├── 图1_磁场能量等效引力.png
│   ├── 图2_交变磁场能量.png
│   └── 图3_准静态近似有效范围.png
├── run_all.py                         一键复算检查
├── RUN_ALL.bat                        Windows启动
├── run_all.sh                         Linux/macOS启动
└── SHA256_MANIFEST.csv                文件校验清单
```

## 直接使用

1. 解压ZIP，进入 `ROOT_V75`。
2. 双击或用浏览器打开 `web/index.html`，拖动磁场、电场、半径、频率、相位，观察模型数值变化。
3. 运行 `python run_all.py`：执行不依赖外部包的41项单元测试。
4. 安装可选依赖 `pip install numpy matplotlib sympy`，再运行：

```bash
python tools/generate_results.py
python tools/symbolic_checks.py
```

5. 如果本机有 Playwright 与 Chromium，可运行 `python tools/browser_smoke.py`；某些组织环境禁用 `file://`，脚本使用 `page.set_content()` 本地加载，并不需要上传网页。

## 数值结果代表什么

磁场 10 T、球形区域半径 1 m，理想空间场能量约 \(1.6667\times10^8\) J；仅把它当作附加能量产生的球对称远场引力单极，在 r=2m 得到 \(3.094\times10^{-20}\) m/s²。这**不是**实际装置、完整 GR 解或实测的人工引力场。真实磁场支架、电流、热与能量源均不能忽略。

### 交变磁场的特别说明

纯粹设 \(B=B_0\cos\omega t\) 而 \(E=0\) 不符合 Maxwell-Faraday 定律。本包加入准静态感应电场 \(E_\theta=-r_\perp\dot B/2\)，并明确限制 \(\omega a/c\ll1\)。

### 三个不应该混淆的量

- **电磁场产生的引力场/曲率：** 现有 GR 中成立。
- **量测装置因为电磁激励出现的重力样信号：** 还需要排除直接电磁力、磁致伸缩、热、振动等干扰。
- **普适引力常数 G 的起源：** 本研究未独立证明。所有使用 G 的数值均有明确外部常数输入。

## 研究与实验诚信

代码测试是对数学模型的实现验证，不是对新物理的实验确证。理论候选中独立参数未被预测，无法宣告四力统一。所有来源和假设见 `SOURCES.md` 与专著。没有访问传感器，也没有虚构仪器数据。
