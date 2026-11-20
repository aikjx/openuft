# ROOT V115｜量子迹异常、尺度嬗变与引力尺度科研总集

日期：2026-11-20。**不是“已经攻破四力统一”，而是对 ROOT V114 五个根本 OPEN 的有证据攻坚。**

## 一、核验后的核心结论

- 经典四维 Maxwell 应力—能量张量零迹，不代表量子 QED/QCD 也总是零迹。严格的规范场量子迹异常算符系数是 β(g)/(2g)，QCD 还有显式夸克质量项。
- 固定有效味数 \(n_f=5\) 的单圈 QCD 量纲嬗变尺度：\(\Lambda_5^{(1)}=0.0878270801455\) GeV。这是**演示用 RG 积分常数**，不是质子质量，更不是单圈预测禁闭的证明。
- 取 PDG 2025 \(\alpha_s(M_Z)=0.1180\pm0.0009\) 的输入，且假定仅有 \(\phi\) 的真空尺度 \(v=\Lambda_5^{(1)}\) 生成引力，简单诱导引力需要 \(\zeta=7.688761955\times10^{38}\) 才能匹配实测 EH 系数。此参数值**用实测 G 反算**，没有预测 G。
- 对质子与其他强子，真实质量来自量子 QCD 总能动张量的非微扰矩阵元；不能直接将单圈 β 系数当作质子质量分解百分比。
- ROOT 的四力统一、\(G\) 无循环预测、量子引力 UV 完备及独有实验信号仍然 OPEN。

## 二、完整内容

- `research/01_ROOT_V115_完整科研总论.md`：协变能动张量、QED/QCD 迹异常、量纲嬗变、诱导引力条件性排除、强子质量、五大 OPEN。
- `research/02_严格证明_迹异常_RG_引力标度.md`：七项可审查证明与失败条件。
- `research/03_五大OPEN_实验与证明义务.md`：科学状态和下一步。
- `src/v115.py`：可复算数学和单位换算。
- `run_all.py`：五张独立理论计算图、250 点 RG 结果、5000 组合成输入误差采样。
- `tests/test_v115.py`：115 项 Python/SymPy 数值及符号断言。
- `tests/browser_smoke.py`：12 项实际 Chromium E2E 检查。
- `web/index.html`：可离线打开，调节 \(\alpha_s\)、固定有效味数、\(\zeta\)、\(v\)。
- `ledger/V115_ALL_396_PRESERVED.csv`：与 V114 历史 396 项台账逐字节相同。
- `archive/ROOT_V114_original.zip`：完整上一轮科研包，便于交叉回归。
- `MANIFEST.json`、`CHECKSUMS.sha256`：交付完整性核验。

## 三、一键复现

在 ZIP 解压出来的 `ROOT_V115_量子迹异常_尺度嬗变_引力耦合_20261120` 目录运行：

```bash
python -m pip install -r requirements.txt
python run_all.py
python -m pytest tests/test_v115.py -q
python tests/browser_smoke.py
```

浏览器检查额外要求 Playwright Python 包及 Chromium（例如 `pip install playwright`）。浏览器工具默认**不覆盖已存档的截图**；需要重建时使用 `python tests/browser_smoke.py --capture`。

源代码不访问网络，不要求 GPU。

## 四、科学与工程验收边界

- PASS 只证明模型内部的算法和数学关系与已知理论一致，不表示真实自然界存在此候选统一理论。
- 系数比不是可观测的强/电实验比率；强子、核子质量需要非微扰矩阵元与重整化协议。
- 如果额外标量未稳定，实验 \(G_N\) 包含标量介导的测力修正，不可直接把 EH 系数等同实验 \(G_N\)。
- `figures/06_actual_browser.png` 为浏览器交互留档，渲染像素不保证跨浏览器版本位级相同。科研 JSON 用精确重复复算验收。
- 396 项历史任务原始状态未修改，新成果不冒充解决那些已存在的 OPEN。
