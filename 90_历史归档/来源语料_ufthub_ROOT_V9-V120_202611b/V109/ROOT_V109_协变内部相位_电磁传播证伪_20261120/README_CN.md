# ROOT V109｜内部相位、电磁传播与统一场论科研审计包

版本 2026-11-20；本包 **不是完整四力统一的证明**，也没有新的真实物理观测。历史 ROOT V108 完整科研 ZIP 存在 `archive/ROOT_V108_original.zip`，未覆盖旧文件。

## 本轮的实际成果

- 通过新增 `θ F\widetilde F` 的协变有效作用量推导修正 Maxwell 方程和赝标量方程。
- 证明常数 θ 时局域传播不修正；通过独立复数模式积分验证 WKB 旋光近似。
- 建立非绝热反例：端点差公式不是普遍精确式。
- 建立单测量 λ 与 Δθ 参数退化的精确秩论证。
- 对照 2026 年 ACT、PRD 观测，明确该效应已属于 axion-like 模型，不能当成 ROOT 独有发现。
- 从 V108 原样保留 396 个唯一问题及原始验收条件，新增 12 条专项路线并**单独存放**，不会擅自宣告旧目标已完成。

## 文件内容

- `research/01_ROOT_V109_科研总论.md`：全部主要结论、量纲、局限与公开文献。
- `research/02_严格数学证明与反例.md`：8 项定理/反例，注明前提。
- `research/03_实验可辨识性与公开文献.md`：如何从天文偏振转成有条件的实验检验。
- `research/04_五大OPEN的最短可审计路径.md`：从物理解释到真正统一的剩余验收路线。
- `src/axion_em.py`：两个 helicity 模式的 SciPy 复数积分，A 与 E 模式代理、绝热度和秩。
- `src/symbolic_audit.py`：10 项 SymPy 检查和自然单位量纲。
- `tests/test_v109.py`：反例、极限、对称、数值收敛、历史追溯测试。
- `results/*THEORY*` / `figures/*THEORY*`：明确标记为模型计算。
- `ledger/V108_ALL_396_AUDITED.csv`：原始审计表；`ledger/V109_ALL_396_PRESERVED.csv`：增加本轮参考列；`ledger/V109_NEW_WORKSTREAMS.csv`：12 条新增工作线。
- `web/index.html`：可离线调节内部相位、耦合、波数和时长，运行 RK4 模式积分；不连接外部网络。
- `figures/05_CHROMIUM_ACTUAL_SCREENSHOT.png`：实际 Chromium 验证时的界面截图。
- `CHECKSUMS.sha256`、`verify_integrity.py`、`VALIDATION_REPORT.md`：独立校验。

## 一键运行（无需联网）

Python 3.10+，建议：

```bash
python -m pip install -r requirements.txt
python run_all.py
python verify_integrity.py
```

在已安装 Chromium 与 playwright 的系统可以另执行 `python web/browser_smoke.py`。这一项是可选的真实浏览器测试，默认 Python requirements 不安装 Playwright，用户可单独安装它。若浏览器阻止 `file://`，测试程序改用将同一 HTML 内容直接加载浏览器，避免借助网络服务。自行浏览时可双击 `web/index.html`。

## 单位和证据说明

模型示例以 ħ=c=1 的自然单位和任意参考频率归一化；k、t、λ、θ 的数值是理论模拟参数，不得当作 GHz、秒或实际物理光子观测。文献耦合 g_{aγ} 具有 GeV⁻¹ 量纲，需要独立的 f 才能由 g=λ/f 进行比较。

**ROOT 仍未证明：四力共同起源、SM 规范群/粒子质量谱无参数产生、G 的独立数值、引力子的实验确认或新力的真实观测。**
