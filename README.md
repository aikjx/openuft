# openuft · 多假设统一场论研究（全维度 · 全链路）

通过**不同理论体系（假设 / 体系）**分别建模、推导、分析、验证、精算，在跨体系比较中逐步筛选、收敛出真正的统一场论。
每个体系自成一条**全链路**研究线：假设 → 定义 → 求导(D) → 证明(P) → 预测 → 验证(V) → 精算(A) → 证伪 → 结论。
研究目标不等于已达成结论；凡未经验证的内容一律标注「推测 / 未验证」。

作者：AI 科技星（AI Tech Star） · 研究组织：AI 科技星实验室（Algorithm Alliance）

## 目录总览（两大层）

### 第一层 · 主分类轴 = 假设体系（`01_hypotheses`）
统一场论按「产生场的机制 / 世界观」分为 6 条独立研究线，每条自带全链路：

| 体系 | 编号 | 核心问题 |
|---|---|---|
| 空间运行与螺旋运动 | h01 | 空间运动 / 速度场 / 螺旋结构能否产生可观测场？ |
| 空间压缩与密度梯度 | h02 | 空间压缩量如何定义、测量，并与质量 / 引力 / 场方程联系？ |
| 物体驱动与源场耦合 | h03 | 物体运动及源分布如何驱动场，场又如何反作用于物体？ |
| 几何与作用量 | h04 | 给定几何结构与作用量，能否一致导出动力学与已知极限？ |
| 规范对称与相互作用 | h05 | 规范群、对称破缺、耦合能否形成一致的统一描述？ |
| 量子结构与涌现 | h06 | 量子自由度 / 微观结构如何产生时空与有效相互作用？ |

新增体系：复制 `01_hypotheses/_template/` 为 `h07_xxx/`，并登记于 `01_hypotheses/README.md`。

### 第二层 · 跨体系公共层

| 目录 | 职责 |
|---|---|
| [00_index](00_index/README.md) | 全量资料索引、定理谱系、总报告 |
| [02_comparison](02_comparison/README.md) | 跨体系比较矩阵（竞争 / 交叉 / 收敛 / 淘汰） |
| [03_research_protocol](03_research_protocol/README.md) | 研究协议 + 共享审计方法论（误差预算 / 蒙特卡洛 / 诚实分层 L0–L8） |
| [04_synthesis](04_synthesis/README.md) | 综合各体系结论 → 统一候选 |
| [50_physics_domains](50_physics_domains/README.md) | 跨物理领域对照（引力 / 电磁 / 弱 / 强 / 宇宙学 / 粒子谱） |
| [60_application](60_application/README.md) | 工程与应用探索 |
| [70_source_code](70_source_code/README.md) | 代码与复现工具 |
| [80_visualization](80_visualization/README.md) | 可视化产物 |
| [90_paper_论文](90_paper_论文/README.md) | 论文与报告 |
| [95_history_archive](95_history_archive/README.md) | 历史版本归档 |
| [99_inbox_future](99_inbox_future/README.md) | 待研究问题 inbox |
| [docs](docs/README.md) | 共享数学、文献、术语资料 |

## 全链路工作流（每条体系内部）

```
假设(00) → 定义(01) → 求导(02,D) → 证明(03,P) → 预测(04)
        → 验证(05,V) → 精算(06,A) → 证伪(07) → 结论(08)
```

- **求导 D**：从公理 / 作用量变分导出方程（方法论见 `03_research_protocol/method_D_求导.md`）
- **证明 P**：严格代数 / 数值证明（方法论见 `03_research_protocol/method_P_证明.md`）
- **验证 V**：实验 / 数值对照（方法论见 `03_research_protocol/method_V_验证.md`）
- **精算 A**：误差预算、蒙特卡洛、证伪标准、诚实分层（方法论见 `03_research_protocol/audit_methodology/`）

## 阅读顺序

1. 在 [理论路线](01_hypotheses/README.md) 选择体系，沿 00 → 08 阅读全链路。
2. 按 [研究协议](03_research_protocol/README.md) 建立可追溯记录。
3. 在 [比较矩阵](02_comparison/README.md) 对照预测与证据，观察竞争 / 收敛。
4. 在 [综合区](04_synthesis/README.md) 登记候选、冲突与缺口。

既有文件通过 [全量分类索引](00_index/material_catalog.md) 访问。[迁移说明](MIGRATION_GUIDE.md) 记录本次布局调整。
