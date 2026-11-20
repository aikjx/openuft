# ROOT V111｜Noether 守恒、引力变分与 Floquet 反例科研包

**研究日期：2026-11-20。状态：指定经典有效模型中的条件性数学证明和真实运行的数值测试；并未攻破四力统一。**

## 研究主线

1. 在 V110 有限模相位—电磁系统中独立推导正则 Noether 荷 `Q`，并严格证明有/无周期相位势时的守恒与破缺方程。
2. 联立总能量 `H` 推导内部相位速度、有限光场振幅的严格不等式；求解不同初始条件下的反馈，精确检查两个相互独立的守恒律。
3. 通过六个独立电磁场张量分量，证明 `theta F∧F` 相互作用对度规没有直接变分贡献；修复“出现电磁耦合便已独立生成引力 G”的错误推论。
4. 审计紧致相位 `theta~theta+2pi` 的曲率耦合：`theta^2 R` 不是全局单值的周期耦合，`cos(theta) R` 形式上允许，但无法消除独立的引力质量标度。
5. 提供一个**全部瞬时频率平方严格为正，但仍发生 Floquet 不稳定**的独立数值反例。
6. 完整保留 V110 的 396 项历史问题，原先未解决的四力统一、独立 G 与量子引力目标不被擅自标记为完成。

## 使用方法

```bash
python -m pip install -r requirements.txt
python run_all.py
python web/browser_smoke.py
python verify_integrity.py
```

打开 `web/index.html` 可以**离线**浏览三种有限模模型、守恒荷、能量与交互曲线，无需联网或部署。测试环境应具有 Chromium；可直接调用浏览器脚本完成 UI 验证。

## 文件结构

- `research/01_完整科研总论.md`：本轮完整推导、实算与科学边界。
- `research/02_严格证明_守恒荷_引力变分.md`：逐项数学证明与反例。
- `research/03_所有OPEN_证据层级与下一步.md`：继承 396 项问题，五大核心 OPEN 的硬验收条件。
- `results/`：CSV/JSON 原始再生成数据。
- `src/`：有限模动力学、符号审计、场的度规变分、Floquet 反例、科研图表/HTML 生成。
- `tests/`：可重复的自动测试。
- `figures/`：5 张数值理论图 + 1 张真实 Chromium 截图（截图不在自动复跑时覆盖）。
- `ledger/`：保留完整 396 行历史问题和每个原始状态。
- `archive/ROOT_V110_original.zip`：上一版本的完整原包。
- `CHECKSUMS.sha256`、`MANIFEST.json`：独立完整性核验。

## 科学结论摘要

- 无相位势 `Lambda4=0` 时 `Q=f² theta_dot -(lambda k/2)(Aplus² - Aminus²)` 严格守恒；有周期势时 `Qdot=-Lambda4 sin(theta)`。
- 任何闭合有限模模型，满足 `|Q-f² theta_dot|<=|lambda|H/k`。
- `theta F tilde F` 拓扑项**没有直接的度规变分应力张量**，不能单靠它导出 G；普通相位场、Maxwell 场的应力张量仍然存在。
- 瞬时刚度为正不保证 Floquet 稳定；Floquet 反例的最小刚度 0.888、周期矩阵迹约 -2.007737。
- 对标准模型与 Einstein 引力的统一来源，目前仍没有独立的证明或新的排他性实验预测。

**注意：** 有限维数截断中的量均按参考频率无量纲化。这些曲线不是测得的天体/粒子数据，不能代入 SI 物理量而没有明确的模式归一化、体积和单位换算。
