# ROOT V112｜引力—电磁—高维统一完整科研审计

**定位**：独立数学验证 + 已知场论的交叉尺度一致性 + 高维候选模型的精确反例。
**重要**：不是“已解决大统一”，不能从复算的 G 定义或重命名的作用量声称无参数预测出 G。

## 一键运行

```bash
python -m pip install -r requirements.txt
python run_all.py
python -m unittest discover -s tests -v
```

从项目根目录运行。`run_all.py` 会生成 `results/V112_RESULTS.json` 和四幅图。`web/index.html` 为无需服务器的离线计算器。

## 内容

- `research/01_完整科研总论.md`：十种引力研究路线及四个严格核心推导
- `research/02_数学证明_五维标量_荷质比_RN.md`：逐式核算
- `research/03_396项OPEN_攻坚验收矩阵.md`：保留五个终极 OPEN 和证据标准
- `src/physics.py`：SI 基准，RN、荷质尺度、量纲、Kaluza–Klein 标量一致性
- `tests/test_v112.py`：47 项测试，含 8 项 SymPy 检查
- `ledger/V112_ALL_396_PRESERVED.csv`：未更改的 V111 396 项历史台账
- `archive/ROOT_V111_original.zip`：原版科研包，便于独立回溯

## 关键结论

1. 定义 ξ=|Q|/(M√(4πε₀G))，牛顿-库仑力强比（绝对值）=ξ₁ξ₂；RN 事件视界需要 ξ≤1。
2. 电子 ξ≈2.041×10²¹；把电子当作普通经典 RN 黑洞的解释不成立。
3. Kerr–Newman 自旋与电荷联合极值边界进一步排除电子作为简单经典黑洞的模型。
4. 五维真空 Kaluza–Klein **若同时要求标量 φ 恒定**，普通非零 FμνFμν 静电/磁场与完整标量方程不相容。
4. 四维 Maxwell 应力张量 Tμμ=0，但可有 Rμν≠0；仅研究 R 的模型可能漏掉引力。
5. c 与 ℏ 无法靠幂次得到 G 的 SI 量纲；加入质量标度可写 G=ℏc/M²，但 M 必须独立预测，否则循环。
6. 现有强场引力波、EP、Cassini 证据限制新模型的偏离。

## 最终状态

已完成：条件性数学论证、独立数值计算、代码及归档测试。
**OPEN**：统一强弱电磁与引力的独立 UV 完备动力学、G 的无循环计算、三代粒子谱、独立新预言与真实实验验证。

研究日期：2026-11-20
