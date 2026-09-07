# 全部实际目录逐项分析

生成日期：2026-09-07。[主论证与最优性评估](DIRECTORY_DESIGN_REVIEW.md) · [生成器](tools/audit_directories.py) · [机器可读清单](directory_audit.json)。

## 实测范围

扫描 openuft 下全部实际目录，包括 .github、模板、历史专题与迁移目录；不展开 ZIP 内部虚拟路径。根目录不计入目录数量，根文件职责见主文。

- 实际目录：262；已分析：262；未归类：0。
- 当前文件：393。
- 递归文件名集合仅为 README.md 的目录：167；这是占位倾向指标，不代表正文无研究内容。

目录的递归文件数包含子目录，不能逐行相加求总数。职责与边界由显式规则逐项匹配，不根据文件数量推断科学成熟度。

## 模型登记现状

| 模型 | 公设条数 | 公设版本 | 命题记录行 | 数据记录行 | 模型内 Python 文件 |
|---|---:|---|---:|---:|---:|
| h01_space_motion | 0 | 未填写 | 0 | 0 | 2 |
| h02_space_compression | 0 | 未填写 | 0 | 0 | 0 |
| h03_matter_driven | 0 | 未填写 | 0 | 0 | 0 |
| h04_geometry_action | 0 | 未填写 | 0 | 0 | 1 |
| h05_gauge_symmetry | 0 | 未填写 | 0 | 0 | 0 |
| h06_quantum_emergence | 0 | 未填写 | 0 | 0 | 0 |

模型内 Python 文件数不包括共享引擎；零条登记不说明不存在散落正文，只说明尚未录入这些登记表。

## 逐目录结论


### .github

| 目录 | 直接/递归文件 | 职责 | 保留理由 | 边界与风险 | 判断 |
|---|---:|---|---|---|---|
| [.github](../.github/) | 1/4 | 协作平台配置 | 平台固定路径要求 | 不属于理论模块；现有模板不意味着有 CI | 保留 |
| [.github/ISSUE_TEMPLATE](../.github/ISSUE_TEMPLATE/) | 3/3 | 问题反馈模板 | 规范外部输入 | 不能取代正式证据登记 | 保留 |

### 00_governance

| 目录 | 直接/递归文件 | 职责 | 保留理由 | 边界与风险 | 判断 |
|---|---:|---|---|---|---|
| [00_governance](./) | 12/20 | 全局治理 | 规则与研究内容职责分离 | 避免将治理文档当科学认证 | 保留 |
| [00_governance/catalog](catalog/) | 6/6 | 生成索引与历史总表 | 提供全局查找视图 | 目录索引不构成理论归属审查 | 保留 |
| [00_governance/tools](tools/) | 2/2 | 目录维护工具 | 生成视图可重复更新 | 应有覆盖检查，不能静默遗漏新目录 | 保留 |

### 01_models

| 目录 | 直接/递归文件 | 职责 | 保留理由 | 边界与风险 | 判断 |
|---|---:|---|---|---|---|
| [01_models](../01_models/) | 1/276 | 研究路线主轴 | 优先按前提追踪论证 | 六路线并不互斥或穷尽 | 保留 |
| [01_models/_template](../01_models/_template/) | 4/37 | 新增路线模板 | 保证新路线拥有同一职责集合 | 模板不是第七条理论；空字段必须按实际填写 | 保留 |
| [01_models/_template/00_project](../01_models/_template/00_project/) | 2/2 | 立项计划与决策 | 问题、范围和退出条件需要稳定入口 | 计划不得作为结果；负责人和里程碑需要实际填写 | 保留 |
| [01_models/_template/01_literature](../01_models/_template/01_literature/) | 1/1 | 模型文献与基准 | 区分借用知识与本模型新主张 | 共同书目引用共享层，不复制多份主记录 | 保留 |
| [01_models/_template/02_assumptions](../01_models/_template/02_assumptions/) | 1/1 | 本体与公设 | 后续结论须有显式前提 | 模型名称不能代替公设、版本与适用域 | 保留；内容待完善 |
| [01_models/_template/03_formalism](../01_models/_template/03_formalism/) | 1/1 | 数学形式与定义 | 统一符号、单位和边界约定 | 定义与物理假设分别标记 | 保留 |
| [01_models/_template/04_derivations](../01_models/_template/04_derivations/) | 1/1 | 方程推导 | 保存从前提到方程的演算链 | 推导成功不等于理论一致或观测成立 | 保留 |
| [01_models/_template/05_consistency](../01_models/_template/05_consistency/) | 1/1 | 条件性证明与一致性 | 分别审查守恒、稳定性、已知极限等 | 数值例子不替代一般证明 | 保留 |
| [01_models/_template/06_predictions](../01_models/_template/06_predictions/) | 1/1 | 可测量预测 | 先规定可区分量和检验标准 | 拟合已有数据与独立预测不得混淆 | 保留 |
| [01_models/_template/07_computation](../01_models/_template/07_computation/) | 1/7 | 计算实现与复现 | 统一管理代码、配置、测试和执行 | 输出结论需链接验证层；模板不等于可运行环境 | 保留 |
| [01_models/_template/07_computation/configs](../01_models/_template/07_computation/configs/) | 1/1 | 参数与算法配置 | 输入与输出分离有利于复现 | 记录单位、版本及默认值 | 保留 |
| [01_models/_template/07_computation/notebooks](../01_models/_template/07_computation/notebooks/) | 1/1 | 交互探索 | 保留研究过程及演示 | 正式结果须能从干净状态顺序复算 | 按工作量使用 |
| [01_models/_template/07_computation/runs](../01_models/_template/07_computation/runs/) | 2/2 | 逐次运行记录 | 执行命令、环境及失败状态可追踪 | run_template.json 不是已完成运行 | 保留 |
| [01_models/_template/07_computation/src](../01_models/_template/07_computation/src/) | 1/1 | 模型专属源码 | 主实现集中，避免阶段间重复算法 | 历史阶段入口可以保留，但依赖要显式 | 保留 |
| [01_models/_template/07_computation/tests](../01_models/_template/07_computation/tests/) | 1/1 | 自动断言与回归 | 实现正确性需要独立检查入口 | 测试通过不代表理论正确 | 保留；当前多为模板 |
| [01_models/_template/08_data](../01_models/_template/08_data/) | 2/5 | 数据来源与处理链 | 数据身份独立于代码与论文 | 只读是约定，尚未由权限强制 | 保留 |
| [01_models/_template/08_data/external](../01_models/_template/08_data/external/) | 1/1 | 外部来源与获取元数据 | 明确来源、许可、版本及获取方式 | 若存原件必须确定唯一主位置，避免与 raw 冲突 | 边界需执行约束 |
| [01_models/_template/08_data/processed](../01_models/_template/08_data/processed/) | 1/1 | 派生数据 | 处理过程与原件分离 | 须链接输入 data_id 和生成 run_id | 保留 |
| [01_models/_template/08_data/raw](../01_models/_template/08_data/raw/) | 1/1 | 原始数据主副本 | 保留输入原貌 | 不要与 external 重复保管同一主副本 | 保留 |
| [01_models/_template/09_validation](../01_models/_template/09_validation/) | 1/1 | 实现验证与观测检验 | 对照预测、数据和基准 | 应标注检验类型，不能把内部恒等式当外部验证 | 保留 |
| [01_models/_template/10_uncertainty](../01_models/_template/10_uncertainty/) | 1/1 | 误差预算与稳健性 | 有效数字不能代替不确定度 | 必须进入预测和检验设计，不只用于论文末尾 | 保留 |
| [01_models/_template/11_falsification](../01_models/_template/11_falsification/) | 1/1 | 反例与负结果 | 失败记录需要不受最终叙述影响的位置 | 链接同一主结果，避免复制不利数据 | 保留 |
| [01_models/_template/12_conclusions](../01_models/_template/12_conclusions/) | 1/1 | 证据约束下的结论 | 把数学、数值、观测与未验证主张分开 | 必须追溯公设与证据版本 | 保留 |
| [01_models/_template/13_publications](../01_models/_template/13_publications/) | 1/4 | 模型论文材料 | 叙述、图表和补充材料有出版职责 | 跨模型综述放公共出版层 | 保留 |
| [01_models/_template/13_publications/figures](../01_models/_template/13_publications/figures/) | 1/1 | 图表与生成来源 | 出版图可追踪到运行 | 不要手工复制后失去版本关系 | 保留 |
| [01_models/_template/13_publications/manuscript](../01_models/_template/13_publications/manuscript/) | 1/1 | 正文与参考文献 | 面向出版读者组织叙述 | 结论证据仍保留在研究阶段 | 保留 |
| [01_models/_template/13_publications/supplement](../01_models/_template/13_publications/supplement/) | 1/1 | 补充材料 | 提供读者所需复现说明 | 不复制完整数据仓库 | 保留 |
| [01_models/_template/14_review](../01_models/_template/14_review/) | 2/2 | 评审与独立复现 | 保存意见、回复和独立检查过程 | 自评不等于外部认可；允许贯穿所有阶段 | 保留 |
| [01_models/_template/15_releases](../01_models/_template/15_releases/) | 2/2 | 冻结版本与发布清单 | 引用和复现需要确定版本 | 发布不自动代表同行评审通过 | 保留 |
| [01_models/_template/90_archive](../01_models/_template/90_archive/) | 1/1 | 模型内历史 | 保留替代关系与停止原因 | 模型稳定入口不删除；跨模型历史进入根归档 | 保留 |
| [01_models/h01_space_motion](../01_models/h01_space_motion/) | 4/51 | 空间运行与螺旋运动路线容器 | 同一前提下研究材料形成稳定主路径 | 公设版本尚待完善；交叉关系见主文第 5 节 | 保留；边界待科学定义 |
| [01_models/h01_space_motion/00_project](../01_models/h01_space_motion/00_project/) | 2/2 | 立项计划与决策 | 问题、范围和退出条件需要稳定入口 | 计划不得作为结果；负责人和里程碑需要实际填写 | 保留 |
| [01_models/h01_space_motion/01_literature](../01_models/h01_space_motion/01_literature/) | 1/1 | 模型文献与基准 | 区分借用知识与本模型新主张 | 共同书目引用共享层，不复制多份主记录 | 保留 |
| [01_models/h01_space_motion/02_assumptions](../01_models/h01_space_motion/02_assumptions/) | 1/1 | 本体与公设 | 后续结论须有显式前提 | 模型名称不能代替公设、版本与适用域 | 保留；内容待完善 |
| [01_models/h01_space_motion/03_formalism](../01_models/h01_space_motion/03_formalism/) | 1/1 | 数学形式与定义 | 统一符号、单位和边界约定 | 定义与物理假设分别标记 | 保留 |
| [01_models/h01_space_motion/04_derivations](../01_models/h01_space_motion/04_derivations/) | 1/3 | 方程推导 | 保存从前提到方程的演算链 | 推导成功不等于理论一致或观测成立 | 保留 |
| [01_models/h01_space_motion/04_derivations/D5_大统一力方程](../01_models/h01_space_motion/04_derivations/D5_大统一力方程/) | 2/2 | 保留 H01 的既有力方程推导与复算入口 | 沿用已有专题分组减少迁移破坏 | 命名与历史证明标签未重新审定；不必推广为全部模型必建目录 | 保留历史专题 |
| [01_models/h01_space_motion/05_consistency](../01_models/h01_space_motion/05_consistency/) | 1/11 | 条件性证明与一致性 | 分别审查守恒、稳定性、已知极限等 | 数值例子不替代一般证明 | 保留 |
| [01_models/h01_space_motion/05_consistency/P1_螺旋三重奏_TS1](../01_models/h01_space_motion/05_consistency/P1_螺旋三重奏_TS1/) | 2/2 | 保留三重奏命题相关历史论证 | 沿用已有专题分组减少迁移破坏 | 命名与历史证明标签未重新审定；不必推广为全部模型必建目录 | 保留历史专题 |
| [01_models/h01_space_motion/05_consistency/P3_归纳闭合_R9](../01_models/h01_space_motion/05_consistency/P3_归纳闭合_R9/) | 4/4 | 保留归纳闭合的条件与证明过程 | 沿用已有专题分组减少迁移破坏 | 命名与历史证明标签未重新审定；不必推广为全部模型必建目录 | 保留历史专题 |
| [01_models/h01_space_motion/05_consistency/P4_绝热三重奏_R10](../01_models/h01_space_motion/05_consistency/P4_绝热三重奏_R10/) | 2/2 | 保留绝热与特殊极限研究 | 沿用已有专题分组减少迁移破坏 | 命名与历史证明标签未重新审定；不必推广为全部模型必建目录 | 保留历史专题 |
| [01_models/h01_space_motion/05_consistency/P5_梯度磁场精确性_R11](../01_models/h01_space_motion/05_consistency/P5_梯度磁场精确性_R11/) | 1/1 | 保留梯度磁场命题专题入口 | 沿用已有专题分组减少迁移破坏 | 命名与历史证明标签未重新审定；不必推广为全部模型必建目录 | 保留历史专题 |
| [01_models/h01_space_motion/05_consistency/P6_谱理论框架_R7R8](../01_models/h01_space_motion/05_consistency/P6_谱理论框架_R7R8/) | 1/1 | 保留谱理论专题证明资料 | 沿用已有专题分组减少迁移破坏 | 命名与历史证明标签未重新审定；不必推广为全部模型必建目录 | 保留历史专题 |
| [01_models/h01_space_motion/06_predictions](../01_models/h01_space_motion/06_predictions/) | 1/1 | 可测量预测 | 先规定可区分量和检验标准 | 拟合已有数据与独立预测不得混淆 | 保留 |
| [01_models/h01_space_motion/07_computation](../01_models/h01_space_motion/07_computation/) | 1/7 | 计算实现与复现 | 统一管理代码、配置、测试和执行 | 输出结论需链接验证层；模板不等于可运行环境 | 保留 |
| [01_models/h01_space_motion/07_computation/configs](../01_models/h01_space_motion/07_computation/configs/) | 1/1 | 参数与算法配置 | 输入与输出分离有利于复现 | 记录单位、版本及默认值 | 保留 |
| [01_models/h01_space_motion/07_computation/notebooks](../01_models/h01_space_motion/07_computation/notebooks/) | 1/1 | 交互探索 | 保留研究过程及演示 | 正式结果须能从干净状态顺序复算 | 按工作量使用 |
| [01_models/h01_space_motion/07_computation/runs](../01_models/h01_space_motion/07_computation/runs/) | 2/2 | 逐次运行记录 | 执行命令、环境及失败状态可追踪 | run_template.json 不是已完成运行 | 保留 |
| [01_models/h01_space_motion/07_computation/src](../01_models/h01_space_motion/07_computation/src/) | 1/1 | 模型专属源码 | 主实现集中，避免阶段间重复算法 | 历史阶段入口可以保留，但依赖要显式 | 保留 |
| [01_models/h01_space_motion/07_computation/tests](../01_models/h01_space_motion/07_computation/tests/) | 1/1 | 自动断言与回归 | 实现正确性需要独立检查入口 | 测试通过不代表理论正确 | 保留；当前多为模板 |
| [01_models/h01_space_motion/08_data](../01_models/h01_space_motion/08_data/) | 2/5 | 数据来源与处理链 | 数据身份独立于代码与论文 | 只读是约定，尚未由权限强制 | 保留 |
| [01_models/h01_space_motion/08_data/external](../01_models/h01_space_motion/08_data/external/) | 1/1 | 外部来源与获取元数据 | 明确来源、许可、版本及获取方式 | 若存原件必须确定唯一主位置，避免与 raw 冲突 | 边界需执行约束 |
| [01_models/h01_space_motion/08_data/processed](../01_models/h01_space_motion/08_data/processed/) | 1/1 | 派生数据 | 处理过程与原件分离 | 须链接输入 data_id 和生成 run_id | 保留 |
| [01_models/h01_space_motion/08_data/raw](../01_models/h01_space_motion/08_data/raw/) | 1/1 | 原始数据主副本 | 保留输入原貌 | 不要与 external 重复保管同一主副本 | 保留 |
| [01_models/h01_space_motion/09_validation](../01_models/h01_space_motion/09_validation/) | 1/3 | 实现验证与观测检验 | 对照预测、数据和基准 | 应标注检验类型，不能把内部恒等式当外部验证 | 保留 |
| [01_models/h01_space_motion/09_validation/V2_mpmath高精度](../01_models/h01_space_motion/09_validation/V2_mpmath高精度/) | 2/2 | 保留多精度数值复算入口 | 沿用已有专题分组减少迁移破坏 | 命名与历史证明标签未重新审定；不必推广为全部模型必建目录 | 保留历史专题 |
| [01_models/h01_space_motion/10_uncertainty](../01_models/h01_space_motion/10_uncertainty/) | 1/1 | 误差预算与稳健性 | 有效数字不能代替不确定度 | 必须进入预测和检验设计，不只用于论文末尾 | 保留 |
| [01_models/h01_space_motion/11_falsification](../01_models/h01_space_motion/11_falsification/) | 1/1 | 反例与负结果 | 失败记录需要不受最终叙述影响的位置 | 链接同一主结果，避免复制不利数据 | 保留 |
| [01_models/h01_space_motion/12_conclusions](../01_models/h01_space_motion/12_conclusions/) | 1/1 | 证据约束下的结论 | 把数学、数值、观测与未验证主张分开 | 必须追溯公设与证据版本 | 保留 |
| [01_models/h01_space_motion/13_publications](../01_models/h01_space_motion/13_publications/) | 1/4 | 模型论文材料 | 叙述、图表和补充材料有出版职责 | 跨模型综述放公共出版层 | 保留 |
| [01_models/h01_space_motion/13_publications/figures](../01_models/h01_space_motion/13_publications/figures/) | 1/1 | 图表与生成来源 | 出版图可追踪到运行 | 不要手工复制后失去版本关系 | 保留 |
| [01_models/h01_space_motion/13_publications/manuscript](../01_models/h01_space_motion/13_publications/manuscript/) | 1/1 | 正文与参考文献 | 面向出版读者组织叙述 | 结论证据仍保留在研究阶段 | 保留 |
| [01_models/h01_space_motion/13_publications/supplement](../01_models/h01_space_motion/13_publications/supplement/) | 1/1 | 补充材料 | 提供读者所需复现说明 | 不复制完整数据仓库 | 保留 |
| [01_models/h01_space_motion/14_review](../01_models/h01_space_motion/14_review/) | 2/2 | 评审与独立复现 | 保存意见、回复和独立检查过程 | 自评不等于外部认可；允许贯穿所有阶段 | 保留 |
| [01_models/h01_space_motion/15_releases](../01_models/h01_space_motion/15_releases/) | 2/2 | 冻结版本与发布清单 | 引用和复现需要确定版本 | 发布不自动代表同行评审通过 | 保留 |
| [01_models/h01_space_motion/90_archive](../01_models/h01_space_motion/90_archive/) | 1/1 | 模型内历史 | 保留替代关系与停止原因 | 模型稳定入口不删除；跨模型历史进入根归档 | 保留 |
| [01_models/h02_space_compression](../01_models/h02_space_compression/) | 4/37 | 空间压缩与密度梯度路线容器 | 同一前提下研究材料形成稳定主路径 | 公设版本尚待完善；交叉关系见主文第 5 节 | 保留；边界待科学定义 |
| [01_models/h02_space_compression/00_project](../01_models/h02_space_compression/00_project/) | 2/2 | 立项计划与决策 | 问题、范围和退出条件需要稳定入口 | 计划不得作为结果；负责人和里程碑需要实际填写 | 保留 |
| [01_models/h02_space_compression/01_literature](../01_models/h02_space_compression/01_literature/) | 1/1 | 模型文献与基准 | 区分借用知识与本模型新主张 | 共同书目引用共享层，不复制多份主记录 | 保留 |
| [01_models/h02_space_compression/02_assumptions](../01_models/h02_space_compression/02_assumptions/) | 1/1 | 本体与公设 | 后续结论须有显式前提 | 模型名称不能代替公设、版本与适用域 | 保留；内容待完善 |
| [01_models/h02_space_compression/03_formalism](../01_models/h02_space_compression/03_formalism/) | 1/1 | 数学形式与定义 | 统一符号、单位和边界约定 | 定义与物理假设分别标记 | 保留 |
| [01_models/h02_space_compression/04_derivations](../01_models/h02_space_compression/04_derivations/) | 1/1 | 方程推导 | 保存从前提到方程的演算链 | 推导成功不等于理论一致或观测成立 | 保留 |
| [01_models/h02_space_compression/05_consistency](../01_models/h02_space_compression/05_consistency/) | 1/1 | 条件性证明与一致性 | 分别审查守恒、稳定性、已知极限等 | 数值例子不替代一般证明 | 保留 |
| [01_models/h02_space_compression/06_predictions](../01_models/h02_space_compression/06_predictions/) | 1/1 | 可测量预测 | 先规定可区分量和检验标准 | 拟合已有数据与独立预测不得混淆 | 保留 |
| [01_models/h02_space_compression/07_computation](../01_models/h02_space_compression/07_computation/) | 1/7 | 计算实现与复现 | 统一管理代码、配置、测试和执行 | 输出结论需链接验证层；模板不等于可运行环境 | 保留 |
| [01_models/h02_space_compression/07_computation/configs](../01_models/h02_space_compression/07_computation/configs/) | 1/1 | 参数与算法配置 | 输入与输出分离有利于复现 | 记录单位、版本及默认值 | 保留 |
| [01_models/h02_space_compression/07_computation/notebooks](../01_models/h02_space_compression/07_computation/notebooks/) | 1/1 | 交互探索 | 保留研究过程及演示 | 正式结果须能从干净状态顺序复算 | 按工作量使用 |
| [01_models/h02_space_compression/07_computation/runs](../01_models/h02_space_compression/07_computation/runs/) | 2/2 | 逐次运行记录 | 执行命令、环境及失败状态可追踪 | run_template.json 不是已完成运行 | 保留 |
| [01_models/h02_space_compression/07_computation/src](../01_models/h02_space_compression/07_computation/src/) | 1/1 | 模型专属源码 | 主实现集中，避免阶段间重复算法 | 历史阶段入口可以保留，但依赖要显式 | 保留 |
| [01_models/h02_space_compression/07_computation/tests](../01_models/h02_space_compression/07_computation/tests/) | 1/1 | 自动断言与回归 | 实现正确性需要独立检查入口 | 测试通过不代表理论正确 | 保留；当前多为模板 |
| [01_models/h02_space_compression/08_data](../01_models/h02_space_compression/08_data/) | 2/5 | 数据来源与处理链 | 数据身份独立于代码与论文 | 只读是约定，尚未由权限强制 | 保留 |
| [01_models/h02_space_compression/08_data/external](../01_models/h02_space_compression/08_data/external/) | 1/1 | 外部来源与获取元数据 | 明确来源、许可、版本及获取方式 | 若存原件必须确定唯一主位置，避免与 raw 冲突 | 边界需执行约束 |
| [01_models/h02_space_compression/08_data/processed](../01_models/h02_space_compression/08_data/processed/) | 1/1 | 派生数据 | 处理过程与原件分离 | 须链接输入 data_id 和生成 run_id | 保留 |
| [01_models/h02_space_compression/08_data/raw](../01_models/h02_space_compression/08_data/raw/) | 1/1 | 原始数据主副本 | 保留输入原貌 | 不要与 external 重复保管同一主副本 | 保留 |
| [01_models/h02_space_compression/09_validation](../01_models/h02_space_compression/09_validation/) | 1/1 | 实现验证与观测检验 | 对照预测、数据和基准 | 应标注检验类型，不能把内部恒等式当外部验证 | 保留 |
| [01_models/h02_space_compression/10_uncertainty](../01_models/h02_space_compression/10_uncertainty/) | 1/1 | 误差预算与稳健性 | 有效数字不能代替不确定度 | 必须进入预测和检验设计，不只用于论文末尾 | 保留 |
| [01_models/h02_space_compression/11_falsification](../01_models/h02_space_compression/11_falsification/) | 1/1 | 反例与负结果 | 失败记录需要不受最终叙述影响的位置 | 链接同一主结果，避免复制不利数据 | 保留 |
| [01_models/h02_space_compression/12_conclusions](../01_models/h02_space_compression/12_conclusions/) | 1/1 | 证据约束下的结论 | 把数学、数值、观测与未验证主张分开 | 必须追溯公设与证据版本 | 保留 |
| [01_models/h02_space_compression/13_publications](../01_models/h02_space_compression/13_publications/) | 1/4 | 模型论文材料 | 叙述、图表和补充材料有出版职责 | 跨模型综述放公共出版层 | 保留 |
| [01_models/h02_space_compression/13_publications/figures](../01_models/h02_space_compression/13_publications/figures/) | 1/1 | 图表与生成来源 | 出版图可追踪到运行 | 不要手工复制后失去版本关系 | 保留 |
| [01_models/h02_space_compression/13_publications/manuscript](../01_models/h02_space_compression/13_publications/manuscript/) | 1/1 | 正文与参考文献 | 面向出版读者组织叙述 | 结论证据仍保留在研究阶段 | 保留 |
| [01_models/h02_space_compression/13_publications/supplement](../01_models/h02_space_compression/13_publications/supplement/) | 1/1 | 补充材料 | 提供读者所需复现说明 | 不复制完整数据仓库 | 保留 |
| [01_models/h02_space_compression/14_review](../01_models/h02_space_compression/14_review/) | 2/2 | 评审与独立复现 | 保存意见、回复和独立检查过程 | 自评不等于外部认可；允许贯穿所有阶段 | 保留 |
| [01_models/h02_space_compression/15_releases](../01_models/h02_space_compression/15_releases/) | 2/2 | 冻结版本与发布清单 | 引用和复现需要确定版本 | 发布不自动代表同行评审通过 | 保留 |
| [01_models/h02_space_compression/90_archive](../01_models/h02_space_compression/90_archive/) | 1/1 | 模型内历史 | 保留替代关系与停止原因 | 模型稳定入口不删除；跨模型历史进入根归档 | 保留 |
| [01_models/h03_matter_driven](../01_models/h03_matter_driven/) | 4/37 | 物体驱动与源场耦合路线容器 | 同一前提下研究材料形成稳定主路径 | 公设版本尚待完善；交叉关系见主文第 5 节 | 保留；边界待科学定义 |
| [01_models/h03_matter_driven/00_project](../01_models/h03_matter_driven/00_project/) | 2/2 | 立项计划与决策 | 问题、范围和退出条件需要稳定入口 | 计划不得作为结果；负责人和里程碑需要实际填写 | 保留 |
| [01_models/h03_matter_driven/01_literature](../01_models/h03_matter_driven/01_literature/) | 1/1 | 模型文献与基准 | 区分借用知识与本模型新主张 | 共同书目引用共享层，不复制多份主记录 | 保留 |
| [01_models/h03_matter_driven/02_assumptions](../01_models/h03_matter_driven/02_assumptions/) | 1/1 | 本体与公设 | 后续结论须有显式前提 | 模型名称不能代替公设、版本与适用域 | 保留；内容待完善 |
| [01_models/h03_matter_driven/03_formalism](../01_models/h03_matter_driven/03_formalism/) | 1/1 | 数学形式与定义 | 统一符号、单位和边界约定 | 定义与物理假设分别标记 | 保留 |
| [01_models/h03_matter_driven/04_derivations](../01_models/h03_matter_driven/04_derivations/) | 1/1 | 方程推导 | 保存从前提到方程的演算链 | 推导成功不等于理论一致或观测成立 | 保留 |
| [01_models/h03_matter_driven/05_consistency](../01_models/h03_matter_driven/05_consistency/) | 1/1 | 条件性证明与一致性 | 分别审查守恒、稳定性、已知极限等 | 数值例子不替代一般证明 | 保留 |
| [01_models/h03_matter_driven/06_predictions](../01_models/h03_matter_driven/06_predictions/) | 1/1 | 可测量预测 | 先规定可区分量和检验标准 | 拟合已有数据与独立预测不得混淆 | 保留 |
| [01_models/h03_matter_driven/07_computation](../01_models/h03_matter_driven/07_computation/) | 1/7 | 计算实现与复现 | 统一管理代码、配置、测试和执行 | 输出结论需链接验证层；模板不等于可运行环境 | 保留 |
| [01_models/h03_matter_driven/07_computation/configs](../01_models/h03_matter_driven/07_computation/configs/) | 1/1 | 参数与算法配置 | 输入与输出分离有利于复现 | 记录单位、版本及默认值 | 保留 |
| [01_models/h03_matter_driven/07_computation/notebooks](../01_models/h03_matter_driven/07_computation/notebooks/) | 1/1 | 交互探索 | 保留研究过程及演示 | 正式结果须能从干净状态顺序复算 | 按工作量使用 |
| [01_models/h03_matter_driven/07_computation/runs](../01_models/h03_matter_driven/07_computation/runs/) | 2/2 | 逐次运行记录 | 执行命令、环境及失败状态可追踪 | run_template.json 不是已完成运行 | 保留 |
| [01_models/h03_matter_driven/07_computation/src](../01_models/h03_matter_driven/07_computation/src/) | 1/1 | 模型专属源码 | 主实现集中，避免阶段间重复算法 | 历史阶段入口可以保留，但依赖要显式 | 保留 |
| [01_models/h03_matter_driven/07_computation/tests](../01_models/h03_matter_driven/07_computation/tests/) | 1/1 | 自动断言与回归 | 实现正确性需要独立检查入口 | 测试通过不代表理论正确 | 保留；当前多为模板 |
| [01_models/h03_matter_driven/08_data](../01_models/h03_matter_driven/08_data/) | 2/5 | 数据来源与处理链 | 数据身份独立于代码与论文 | 只读是约定，尚未由权限强制 | 保留 |
| [01_models/h03_matter_driven/08_data/external](../01_models/h03_matter_driven/08_data/external/) | 1/1 | 外部来源与获取元数据 | 明确来源、许可、版本及获取方式 | 若存原件必须确定唯一主位置，避免与 raw 冲突 | 边界需执行约束 |
| [01_models/h03_matter_driven/08_data/processed](../01_models/h03_matter_driven/08_data/processed/) | 1/1 | 派生数据 | 处理过程与原件分离 | 须链接输入 data_id 和生成 run_id | 保留 |
| [01_models/h03_matter_driven/08_data/raw](../01_models/h03_matter_driven/08_data/raw/) | 1/1 | 原始数据主副本 | 保留输入原貌 | 不要与 external 重复保管同一主副本 | 保留 |
| [01_models/h03_matter_driven/09_validation](../01_models/h03_matter_driven/09_validation/) | 1/1 | 实现验证与观测检验 | 对照预测、数据和基准 | 应标注检验类型，不能把内部恒等式当外部验证 | 保留 |
| [01_models/h03_matter_driven/10_uncertainty](../01_models/h03_matter_driven/10_uncertainty/) | 1/1 | 误差预算与稳健性 | 有效数字不能代替不确定度 | 必须进入预测和检验设计，不只用于论文末尾 | 保留 |
| [01_models/h03_matter_driven/11_falsification](../01_models/h03_matter_driven/11_falsification/) | 1/1 | 反例与负结果 | 失败记录需要不受最终叙述影响的位置 | 链接同一主结果，避免复制不利数据 | 保留 |
| [01_models/h03_matter_driven/12_conclusions](../01_models/h03_matter_driven/12_conclusions/) | 1/1 | 证据约束下的结论 | 把数学、数值、观测与未验证主张分开 | 必须追溯公设与证据版本 | 保留 |
| [01_models/h03_matter_driven/13_publications](../01_models/h03_matter_driven/13_publications/) | 1/4 | 模型论文材料 | 叙述、图表和补充材料有出版职责 | 跨模型综述放公共出版层 | 保留 |
| [01_models/h03_matter_driven/13_publications/figures](../01_models/h03_matter_driven/13_publications/figures/) | 1/1 | 图表与生成来源 | 出版图可追踪到运行 | 不要手工复制后失去版本关系 | 保留 |
| [01_models/h03_matter_driven/13_publications/manuscript](../01_models/h03_matter_driven/13_publications/manuscript/) | 1/1 | 正文与参考文献 | 面向出版读者组织叙述 | 结论证据仍保留在研究阶段 | 保留 |
| [01_models/h03_matter_driven/13_publications/supplement](../01_models/h03_matter_driven/13_publications/supplement/) | 1/1 | 补充材料 | 提供读者所需复现说明 | 不复制完整数据仓库 | 保留 |
| [01_models/h03_matter_driven/14_review](../01_models/h03_matter_driven/14_review/) | 2/2 | 评审与独立复现 | 保存意见、回复和独立检查过程 | 自评不等于外部认可；允许贯穿所有阶段 | 保留 |
| [01_models/h03_matter_driven/15_releases](../01_models/h03_matter_driven/15_releases/) | 2/2 | 冻结版本与发布清单 | 引用和复现需要确定版本 | 发布不自动代表同行评审通过 | 保留 |
| [01_models/h03_matter_driven/90_archive](../01_models/h03_matter_driven/90_archive/) | 1/1 | 模型内历史 | 保留替代关系与停止原因 | 模型稳定入口不删除；跨模型历史进入根归档 | 保留 |
| [01_models/h04_geometry_action](../01_models/h04_geometry_action/) | 4/39 | 几何与作用量路线容器 | 同一前提下研究材料形成稳定主路径 | 公设版本尚待完善；交叉关系见主文第 5 节 | 保留；边界待科学定义 |
| [01_models/h04_geometry_action/00_project](../01_models/h04_geometry_action/00_project/) | 2/2 | 立项计划与决策 | 问题、范围和退出条件需要稳定入口 | 计划不得作为结果；负责人和里程碑需要实际填写 | 保留 |
| [01_models/h04_geometry_action/01_literature](../01_models/h04_geometry_action/01_literature/) | 1/1 | 模型文献与基准 | 区分借用知识与本模型新主张 | 共同书目引用共享层，不复制多份主记录 | 保留 |
| [01_models/h04_geometry_action/02_assumptions](../01_models/h04_geometry_action/02_assumptions/) | 1/1 | 本体与公设 | 后续结论须有显式前提 | 模型名称不能代替公设、版本与适用域 | 保留；内容待完善 |
| [01_models/h04_geometry_action/03_formalism](../01_models/h04_geometry_action/03_formalism/) | 1/1 | 数学形式与定义 | 统一符号、单位和边界约定 | 定义与物理假设分别标记 | 保留 |
| [01_models/h04_geometry_action/04_derivations](../01_models/h04_geometry_action/04_derivations/) | 1/3 | 方程推导 | 保存从前提到方程的演算链 | 推导成功不等于理论一致或观测成立 | 保留 |
| [01_models/h04_geometry_action/04_derivations/D0_作用量变分求导](../01_models/h04_geometry_action/04_derivations/D0_作用量变分求导/) | 2/2 | 保留 H04 的既有作用量推导与复算入口 | 沿用已有专题分组减少迁移破坏 | 命名与历史证明标签未重新审定；不必推广为全部模型必建目录 | 保留历史专题 |
| [01_models/h04_geometry_action/05_consistency](../01_models/h04_geometry_action/05_consistency/) | 1/1 | 条件性证明与一致性 | 分别审查守恒、稳定性、已知极限等 | 数值例子不替代一般证明 | 保留 |
| [01_models/h04_geometry_action/06_predictions](../01_models/h04_geometry_action/06_predictions/) | 1/1 | 可测量预测 | 先规定可区分量和检验标准 | 拟合已有数据与独立预测不得混淆 | 保留 |
| [01_models/h04_geometry_action/07_computation](../01_models/h04_geometry_action/07_computation/) | 1/7 | 计算实现与复现 | 统一管理代码、配置、测试和执行 | 输出结论需链接验证层；模板不等于可运行环境 | 保留 |
| [01_models/h04_geometry_action/07_computation/configs](../01_models/h04_geometry_action/07_computation/configs/) | 1/1 | 参数与算法配置 | 输入与输出分离有利于复现 | 记录单位、版本及默认值 | 保留 |
| [01_models/h04_geometry_action/07_computation/notebooks](../01_models/h04_geometry_action/07_computation/notebooks/) | 1/1 | 交互探索 | 保留研究过程及演示 | 正式结果须能从干净状态顺序复算 | 按工作量使用 |
| [01_models/h04_geometry_action/07_computation/runs](../01_models/h04_geometry_action/07_computation/runs/) | 2/2 | 逐次运行记录 | 执行命令、环境及失败状态可追踪 | run_template.json 不是已完成运行 | 保留 |
| [01_models/h04_geometry_action/07_computation/src](../01_models/h04_geometry_action/07_computation/src/) | 1/1 | 模型专属源码 | 主实现集中，避免阶段间重复算法 | 历史阶段入口可以保留，但依赖要显式 | 保留 |
| [01_models/h04_geometry_action/07_computation/tests](../01_models/h04_geometry_action/07_computation/tests/) | 1/1 | 自动断言与回归 | 实现正确性需要独立检查入口 | 测试通过不代表理论正确 | 保留；当前多为模板 |
| [01_models/h04_geometry_action/08_data](../01_models/h04_geometry_action/08_data/) | 2/5 | 数据来源与处理链 | 数据身份独立于代码与论文 | 只读是约定，尚未由权限强制 | 保留 |
| [01_models/h04_geometry_action/08_data/external](../01_models/h04_geometry_action/08_data/external/) | 1/1 | 外部来源与获取元数据 | 明确来源、许可、版本及获取方式 | 若存原件必须确定唯一主位置，避免与 raw 冲突 | 边界需执行约束 |
| [01_models/h04_geometry_action/08_data/processed](../01_models/h04_geometry_action/08_data/processed/) | 1/1 | 派生数据 | 处理过程与原件分离 | 须链接输入 data_id 和生成 run_id | 保留 |
| [01_models/h04_geometry_action/08_data/raw](../01_models/h04_geometry_action/08_data/raw/) | 1/1 | 原始数据主副本 | 保留输入原貌 | 不要与 external 重复保管同一主副本 | 保留 |
| [01_models/h04_geometry_action/09_validation](../01_models/h04_geometry_action/09_validation/) | 1/1 | 实现验证与观测检验 | 对照预测、数据和基准 | 应标注检验类型，不能把内部恒等式当外部验证 | 保留 |
| [01_models/h04_geometry_action/10_uncertainty](../01_models/h04_geometry_action/10_uncertainty/) | 1/1 | 误差预算与稳健性 | 有效数字不能代替不确定度 | 必须进入预测和检验设计，不只用于论文末尾 | 保留 |
| [01_models/h04_geometry_action/11_falsification](../01_models/h04_geometry_action/11_falsification/) | 1/1 | 反例与负结果 | 失败记录需要不受最终叙述影响的位置 | 链接同一主结果，避免复制不利数据 | 保留 |
| [01_models/h04_geometry_action/12_conclusions](../01_models/h04_geometry_action/12_conclusions/) | 1/1 | 证据约束下的结论 | 把数学、数值、观测与未验证主张分开 | 必须追溯公设与证据版本 | 保留 |
| [01_models/h04_geometry_action/13_publications](../01_models/h04_geometry_action/13_publications/) | 1/4 | 模型论文材料 | 叙述、图表和补充材料有出版职责 | 跨模型综述放公共出版层 | 保留 |
| [01_models/h04_geometry_action/13_publications/figures](../01_models/h04_geometry_action/13_publications/figures/) | 1/1 | 图表与生成来源 | 出版图可追踪到运行 | 不要手工复制后失去版本关系 | 保留 |
| [01_models/h04_geometry_action/13_publications/manuscript](../01_models/h04_geometry_action/13_publications/manuscript/) | 1/1 | 正文与参考文献 | 面向出版读者组织叙述 | 结论证据仍保留在研究阶段 | 保留 |
| [01_models/h04_geometry_action/13_publications/supplement](../01_models/h04_geometry_action/13_publications/supplement/) | 1/1 | 补充材料 | 提供读者所需复现说明 | 不复制完整数据仓库 | 保留 |
| [01_models/h04_geometry_action/14_review](../01_models/h04_geometry_action/14_review/) | 2/2 | 评审与独立复现 | 保存意见、回复和独立检查过程 | 自评不等于外部认可；允许贯穿所有阶段 | 保留 |
| [01_models/h04_geometry_action/15_releases](../01_models/h04_geometry_action/15_releases/) | 2/2 | 冻结版本与发布清单 | 引用和复现需要确定版本 | 发布不自动代表同行评审通过 | 保留 |
| [01_models/h04_geometry_action/90_archive](../01_models/h04_geometry_action/90_archive/) | 1/1 | 模型内历史 | 保留替代关系与停止原因 | 模型稳定入口不删除；跨模型历史进入根归档 | 保留 |
| [01_models/h05_gauge_symmetry](../01_models/h05_gauge_symmetry/) | 4/37 | 规范对称与相互作用路线容器 | 同一前提下研究材料形成稳定主路径 | 公设版本尚待完善；交叉关系见主文第 5 节 | 保留；边界待科学定义 |
| [01_models/h05_gauge_symmetry/00_project](../01_models/h05_gauge_symmetry/00_project/) | 2/2 | 立项计划与决策 | 问题、范围和退出条件需要稳定入口 | 计划不得作为结果；负责人和里程碑需要实际填写 | 保留 |
| [01_models/h05_gauge_symmetry/01_literature](../01_models/h05_gauge_symmetry/01_literature/) | 1/1 | 模型文献与基准 | 区分借用知识与本模型新主张 | 共同书目引用共享层，不复制多份主记录 | 保留 |
| [01_models/h05_gauge_symmetry/02_assumptions](../01_models/h05_gauge_symmetry/02_assumptions/) | 1/1 | 本体与公设 | 后续结论须有显式前提 | 模型名称不能代替公设、版本与适用域 | 保留；内容待完善 |
| [01_models/h05_gauge_symmetry/03_formalism](../01_models/h05_gauge_symmetry/03_formalism/) | 1/1 | 数学形式与定义 | 统一符号、单位和边界约定 | 定义与物理假设分别标记 | 保留 |
| [01_models/h05_gauge_symmetry/04_derivations](../01_models/h05_gauge_symmetry/04_derivations/) | 1/1 | 方程推导 | 保存从前提到方程的演算链 | 推导成功不等于理论一致或观测成立 | 保留 |
| [01_models/h05_gauge_symmetry/05_consistency](../01_models/h05_gauge_symmetry/05_consistency/) | 1/1 | 条件性证明与一致性 | 分别审查守恒、稳定性、已知极限等 | 数值例子不替代一般证明 | 保留 |
| [01_models/h05_gauge_symmetry/06_predictions](../01_models/h05_gauge_symmetry/06_predictions/) | 1/1 | 可测量预测 | 先规定可区分量和检验标准 | 拟合已有数据与独立预测不得混淆 | 保留 |
| [01_models/h05_gauge_symmetry/07_computation](../01_models/h05_gauge_symmetry/07_computation/) | 1/7 | 计算实现与复现 | 统一管理代码、配置、测试和执行 | 输出结论需链接验证层；模板不等于可运行环境 | 保留 |
| [01_models/h05_gauge_symmetry/07_computation/configs](../01_models/h05_gauge_symmetry/07_computation/configs/) | 1/1 | 参数与算法配置 | 输入与输出分离有利于复现 | 记录单位、版本及默认值 | 保留 |
| [01_models/h05_gauge_symmetry/07_computation/notebooks](../01_models/h05_gauge_symmetry/07_computation/notebooks/) | 1/1 | 交互探索 | 保留研究过程及演示 | 正式结果须能从干净状态顺序复算 | 按工作量使用 |
| [01_models/h05_gauge_symmetry/07_computation/runs](../01_models/h05_gauge_symmetry/07_computation/runs/) | 2/2 | 逐次运行记录 | 执行命令、环境及失败状态可追踪 | run_template.json 不是已完成运行 | 保留 |
| [01_models/h05_gauge_symmetry/07_computation/src](../01_models/h05_gauge_symmetry/07_computation/src/) | 1/1 | 模型专属源码 | 主实现集中，避免阶段间重复算法 | 历史阶段入口可以保留，但依赖要显式 | 保留 |
| [01_models/h05_gauge_symmetry/07_computation/tests](../01_models/h05_gauge_symmetry/07_computation/tests/) | 1/1 | 自动断言与回归 | 实现正确性需要独立检查入口 | 测试通过不代表理论正确 | 保留；当前多为模板 |
| [01_models/h05_gauge_symmetry/08_data](../01_models/h05_gauge_symmetry/08_data/) | 2/5 | 数据来源与处理链 | 数据身份独立于代码与论文 | 只读是约定，尚未由权限强制 | 保留 |
| [01_models/h05_gauge_symmetry/08_data/external](../01_models/h05_gauge_symmetry/08_data/external/) | 1/1 | 外部来源与获取元数据 | 明确来源、许可、版本及获取方式 | 若存原件必须确定唯一主位置，避免与 raw 冲突 | 边界需执行约束 |
| [01_models/h05_gauge_symmetry/08_data/processed](../01_models/h05_gauge_symmetry/08_data/processed/) | 1/1 | 派生数据 | 处理过程与原件分离 | 须链接输入 data_id 和生成 run_id | 保留 |
| [01_models/h05_gauge_symmetry/08_data/raw](../01_models/h05_gauge_symmetry/08_data/raw/) | 1/1 | 原始数据主副本 | 保留输入原貌 | 不要与 external 重复保管同一主副本 | 保留 |
| [01_models/h05_gauge_symmetry/09_validation](../01_models/h05_gauge_symmetry/09_validation/) | 1/1 | 实现验证与观测检验 | 对照预测、数据和基准 | 应标注检验类型，不能把内部恒等式当外部验证 | 保留 |
| [01_models/h05_gauge_symmetry/10_uncertainty](../01_models/h05_gauge_symmetry/10_uncertainty/) | 1/1 | 误差预算与稳健性 | 有效数字不能代替不确定度 | 必须进入预测和检验设计，不只用于论文末尾 | 保留 |
| [01_models/h05_gauge_symmetry/11_falsification](../01_models/h05_gauge_symmetry/11_falsification/) | 1/1 | 反例与负结果 | 失败记录需要不受最终叙述影响的位置 | 链接同一主结果，避免复制不利数据 | 保留 |
| [01_models/h05_gauge_symmetry/12_conclusions](../01_models/h05_gauge_symmetry/12_conclusions/) | 1/1 | 证据约束下的结论 | 把数学、数值、观测与未验证主张分开 | 必须追溯公设与证据版本 | 保留 |
| [01_models/h05_gauge_symmetry/13_publications](../01_models/h05_gauge_symmetry/13_publications/) | 1/4 | 模型论文材料 | 叙述、图表和补充材料有出版职责 | 跨模型综述放公共出版层 | 保留 |
| [01_models/h05_gauge_symmetry/13_publications/figures](../01_models/h05_gauge_symmetry/13_publications/figures/) | 1/1 | 图表与生成来源 | 出版图可追踪到运行 | 不要手工复制后失去版本关系 | 保留 |
| [01_models/h05_gauge_symmetry/13_publications/manuscript](../01_models/h05_gauge_symmetry/13_publications/manuscript/) | 1/1 | 正文与参考文献 | 面向出版读者组织叙述 | 结论证据仍保留在研究阶段 | 保留 |
| [01_models/h05_gauge_symmetry/13_publications/supplement](../01_models/h05_gauge_symmetry/13_publications/supplement/) | 1/1 | 补充材料 | 提供读者所需复现说明 | 不复制完整数据仓库 | 保留 |
| [01_models/h05_gauge_symmetry/14_review](../01_models/h05_gauge_symmetry/14_review/) | 2/2 | 评审与独立复现 | 保存意见、回复和独立检查过程 | 自评不等于外部认可；允许贯穿所有阶段 | 保留 |
| [01_models/h05_gauge_symmetry/15_releases](../01_models/h05_gauge_symmetry/15_releases/) | 2/2 | 冻结版本与发布清单 | 引用和复现需要确定版本 | 发布不自动代表同行评审通过 | 保留 |
| [01_models/h05_gauge_symmetry/90_archive](../01_models/h05_gauge_symmetry/90_archive/) | 1/1 | 模型内历史 | 保留替代关系与停止原因 | 模型稳定入口不删除；跨模型历史进入根归档 | 保留 |
| [01_models/h06_quantum_emergence](../01_models/h06_quantum_emergence/) | 4/37 | 量子结构与涌现路线容器 | 同一前提下研究材料形成稳定主路径 | 公设版本尚待完善；交叉关系见主文第 5 节 | 保留；边界待科学定义 |
| [01_models/h06_quantum_emergence/00_project](../01_models/h06_quantum_emergence/00_project/) | 2/2 | 立项计划与决策 | 问题、范围和退出条件需要稳定入口 | 计划不得作为结果；负责人和里程碑需要实际填写 | 保留 |
| [01_models/h06_quantum_emergence/01_literature](../01_models/h06_quantum_emergence/01_literature/) | 1/1 | 模型文献与基准 | 区分借用知识与本模型新主张 | 共同书目引用共享层，不复制多份主记录 | 保留 |
| [01_models/h06_quantum_emergence/02_assumptions](../01_models/h06_quantum_emergence/02_assumptions/) | 1/1 | 本体与公设 | 后续结论须有显式前提 | 模型名称不能代替公设、版本与适用域 | 保留；内容待完善 |
| [01_models/h06_quantum_emergence/03_formalism](../01_models/h06_quantum_emergence/03_formalism/) | 1/1 | 数学形式与定义 | 统一符号、单位和边界约定 | 定义与物理假设分别标记 | 保留 |
| [01_models/h06_quantum_emergence/04_derivations](../01_models/h06_quantum_emergence/04_derivations/) | 1/1 | 方程推导 | 保存从前提到方程的演算链 | 推导成功不等于理论一致或观测成立 | 保留 |
| [01_models/h06_quantum_emergence/05_consistency](../01_models/h06_quantum_emergence/05_consistency/) | 1/1 | 条件性证明与一致性 | 分别审查守恒、稳定性、已知极限等 | 数值例子不替代一般证明 | 保留 |
| [01_models/h06_quantum_emergence/06_predictions](../01_models/h06_quantum_emergence/06_predictions/) | 1/1 | 可测量预测 | 先规定可区分量和检验标准 | 拟合已有数据与独立预测不得混淆 | 保留 |
| [01_models/h06_quantum_emergence/07_computation](../01_models/h06_quantum_emergence/07_computation/) | 1/7 | 计算实现与复现 | 统一管理代码、配置、测试和执行 | 输出结论需链接验证层；模板不等于可运行环境 | 保留 |
| [01_models/h06_quantum_emergence/07_computation/configs](../01_models/h06_quantum_emergence/07_computation/configs/) | 1/1 | 参数与算法配置 | 输入与输出分离有利于复现 | 记录单位、版本及默认值 | 保留 |
| [01_models/h06_quantum_emergence/07_computation/notebooks](../01_models/h06_quantum_emergence/07_computation/notebooks/) | 1/1 | 交互探索 | 保留研究过程及演示 | 正式结果须能从干净状态顺序复算 | 按工作量使用 |
| [01_models/h06_quantum_emergence/07_computation/runs](../01_models/h06_quantum_emergence/07_computation/runs/) | 2/2 | 逐次运行记录 | 执行命令、环境及失败状态可追踪 | run_template.json 不是已完成运行 | 保留 |
| [01_models/h06_quantum_emergence/07_computation/src](../01_models/h06_quantum_emergence/07_computation/src/) | 1/1 | 模型专属源码 | 主实现集中，避免阶段间重复算法 | 历史阶段入口可以保留，但依赖要显式 | 保留 |
| [01_models/h06_quantum_emergence/07_computation/tests](../01_models/h06_quantum_emergence/07_computation/tests/) | 1/1 | 自动断言与回归 | 实现正确性需要独立检查入口 | 测试通过不代表理论正确 | 保留；当前多为模板 |
| [01_models/h06_quantum_emergence/08_data](../01_models/h06_quantum_emergence/08_data/) | 2/5 | 数据来源与处理链 | 数据身份独立于代码与论文 | 只读是约定，尚未由权限强制 | 保留 |
| [01_models/h06_quantum_emergence/08_data/external](../01_models/h06_quantum_emergence/08_data/external/) | 1/1 | 外部来源与获取元数据 | 明确来源、许可、版本及获取方式 | 若存原件必须确定唯一主位置，避免与 raw 冲突 | 边界需执行约束 |
| [01_models/h06_quantum_emergence/08_data/processed](../01_models/h06_quantum_emergence/08_data/processed/) | 1/1 | 派生数据 | 处理过程与原件分离 | 须链接输入 data_id 和生成 run_id | 保留 |
| [01_models/h06_quantum_emergence/08_data/raw](../01_models/h06_quantum_emergence/08_data/raw/) | 1/1 | 原始数据主副本 | 保留输入原貌 | 不要与 external 重复保管同一主副本 | 保留 |
| [01_models/h06_quantum_emergence/09_validation](../01_models/h06_quantum_emergence/09_validation/) | 1/1 | 实现验证与观测检验 | 对照预测、数据和基准 | 应标注检验类型，不能把内部恒等式当外部验证 | 保留 |
| [01_models/h06_quantum_emergence/10_uncertainty](../01_models/h06_quantum_emergence/10_uncertainty/) | 1/1 | 误差预算与稳健性 | 有效数字不能代替不确定度 | 必须进入预测和检验设计，不只用于论文末尾 | 保留 |
| [01_models/h06_quantum_emergence/11_falsification](../01_models/h06_quantum_emergence/11_falsification/) | 1/1 | 反例与负结果 | 失败记录需要不受最终叙述影响的位置 | 链接同一主结果，避免复制不利数据 | 保留 |
| [01_models/h06_quantum_emergence/12_conclusions](../01_models/h06_quantum_emergence/12_conclusions/) | 1/1 | 证据约束下的结论 | 把数学、数值、观测与未验证主张分开 | 必须追溯公设与证据版本 | 保留 |
| [01_models/h06_quantum_emergence/13_publications](../01_models/h06_quantum_emergence/13_publications/) | 1/4 | 模型论文材料 | 叙述、图表和补充材料有出版职责 | 跨模型综述放公共出版层 | 保留 |
| [01_models/h06_quantum_emergence/13_publications/figures](../01_models/h06_quantum_emergence/13_publications/figures/) | 1/1 | 图表与生成来源 | 出版图可追踪到运行 | 不要手工复制后失去版本关系 | 保留 |
| [01_models/h06_quantum_emergence/13_publications/manuscript](../01_models/h06_quantum_emergence/13_publications/manuscript/) | 1/1 | 正文与参考文献 | 面向出版读者组织叙述 | 结论证据仍保留在研究阶段 | 保留 |
| [01_models/h06_quantum_emergence/13_publications/supplement](../01_models/h06_quantum_emergence/13_publications/supplement/) | 1/1 | 补充材料 | 提供读者所需复现说明 | 不复制完整数据仓库 | 保留 |
| [01_models/h06_quantum_emergence/14_review](../01_models/h06_quantum_emergence/14_review/) | 2/2 | 评审与独立复现 | 保存意见、回复和独立检查过程 | 自评不等于外部认可；允许贯穿所有阶段 | 保留 |
| [01_models/h06_quantum_emergence/15_releases](../01_models/h06_quantum_emergence/15_releases/) | 2/2 | 冻结版本与发布清单 | 引用和复现需要确定版本 | 发布不自动代表同行评审通过 | 保留 |
| [01_models/h06_quantum_emergence/90_archive](../01_models/h06_quantum_emergence/90_archive/) | 1/1 | 模型内历史 | 保留替代关系与停止原因 | 模型稳定入口不删除；跨模型历史进入根归档 | 保留 |

### 02_shared

| 目录 | 直接/递归文件 | 职责 | 保留理由 | 边界与风险 | 判断 |
|---|---:|---|---|---|---|
| [02_shared](../02_shared/) | 1/27 | 共享研究资产 | 复用时保留单一主位置 | 共享不等于不含假设 | 保留 |
| [02_shared/computation](../02_shared/computation/) | 1/8 | 共享计算工具 | H01/H04 已有共同依赖 | 缺少完整环境发布契约 | 保留并补工程约束 |
| [02_shared/computation/src](../02_shared/computation/src/) | 0/7 | 共享源码根 | 为 Python 包提供一致导入根 | 当前靠入口定位；将来可评估正式打包 | 保留 |
| [02_shared/computation/src/triad_uft](../02_shared/computation/src/triad_uft/) | 7/7 | 历史复算实现 | 多个入口调用同一实现 | 历史 STRICT/VERIFIED 标签未获本次科学认证 | 保留并审查假设 |
| [02_shared/protocols](../02_shared/protocols/) | 5/10 | 共同研究方法 | 方法约定集中维护 | 旧阶段名及历史证据分层需统一解释 | 保留；需语义修订 |
| [02_shared/protocols/audit_methodology](../02_shared/protocols/audit_methodology/) | 1/5 | 历史审计方法材料 | 保留误差与开放问题的已有来源 | 方法文档含历史主张，不自动成为中立协议 | 有条件保留 |
| [02_shared/protocols/audit_methodology/A1_误差预算](../02_shared/protocols/audit_methodology/A1_误差预算/) | 1/1 | 误差预算历史资料；数值精度与模型误差必须区分 | 保留原有方法与审计资料的出处 | 不能作为当前证据等级的自动认证 | 有条件保留；需语义审查 |
| [02_shared/protocols/audit_methodology/A4_诚实声明OpenProblems](../02_shared/protocols/audit_methodology/A4_诚实声明OpenProblems/) | 1/1 | 开放问题历史清单；结论需链接模型当前版本 | 保留原有方法与审计资料的出处 | 不能作为当前证据等级的自动认证 | 有条件保留；需语义审查 |
| [02_shared/protocols/audit_methodology/A5_分层标注Hierarchy](../02_shared/protocols/audit_methodology/A5_分层标注Hierarchy/) | 1/1 | 历史层级体系；需与当前证据类型建立明确映射 | 保留原有方法与审计资料的出处 | 不能作为当前证据等级的自动认证 | 有条件保留；需语义审查 |
| [02_shared/protocols/audit_methodology/A6_AI科技星认证](../02_shared/protocols/audit_methodology/A6_AI科技星认证/) | 1/1 | 历史自评记录；目录名称不证明外部认证 | 保留原有方法与审计资料的出处 | 不能作为当前证据等级的自动认证 | 有条件保留；需语义审查 |
| [02_shared/references](../02_shared/references/) | 8/8 | 数学、文献与术语 | 统一公共背景与引用入口 | 原始来源与内部总结应明确区分 | 保留 |

### 03_comparative

| 目录 | 直接/递归文件 | 职责 | 保留理由 | 边界与风险 | 判断 |
|---|---:|---|---|---|---|
| [03_comparative](../03_comparative/) | 2/6 | 跨模型分析 | 比较结论的范围超过单模型 | 必须冻结前提、数据与评价准则 | 保留 |
| [03_comparative/applications](../03_comparative/applications/) | 1/1 | 应用可行性探索 | 为公共应用方向提供入口 | 与比较不是同一职责；增长后再考虑独立 | 暂保留的折中 |
| [03_comparative/comparison](../03_comparative/comparison/) | 1/1 | 比较方案与结果 | 研究公平对照关系 | 总登记表在父层，具体报告放此 | 保留 |
| [03_comparative/physics_domains](../03_comparative/physics_domains/) | 1/1 | 按物理领域的次级视图 | 统一候选涉及多个物理主题 | 用链接组织，不再复制模型主文件 | 保留为视图 |
| [03_comparative/synthesis](../03_comparative/synthesis/) | 1/1 | 综合候选 | 组合前提须显式讨论兼容性 | 不能将各路线结论直接相加 | 保留 |

### 04_publications

| 目录 | 直接/递归文件 | 职责 | 保留理由 | 边界与风险 | 判断 |
|---|---:|---|---|---|---|
| [04_publications](../04_publications/) | 1/11 | 跨模型传播 | 综合叙述没有唯一单模型归属 | 明确区分历史报告、草稿和正式出版 | 保留 |
| [04_publications/legacy_reports](../04_publications/legacy_reports/) | 1/9 | 历史综合报告 | 暂不拆散未审查的理论系列 | 放在出版层不代表已发表或已验证 | 暂保留；归属待审 |
| [04_publications/legacy_reports/全维修订版v2](../04_publications/legacy_reports/全维修订版v2/) | 1/1 | 全维修订版v2历史作品系列 | 保留系列版本与上下文 | 理论归属、发表状态和科学结论均待审 | 暂保留历史分组 |
| [04_publications/legacy_reports/求导证明v3](../04_publications/legacy_reports/求导证明v3/) | 1/1 | 求导证明v3历史作品系列 | 保留系列版本与上下文 | 理论归属、发表状态和科学结论均待审 | 暂保留历史分组 |
| [04_publications/legacy_reports/终极报告系列](../04_publications/legacy_reports/终极报告系列/) | 5/5 | 终极报告系列历史作品系列 | 保留系列版本与上下文 | 理论归属、发表状态和科学结论均待审 | 暂保留历史分组 |
| [04_publications/legacy_reports/综述修订](../04_publications/legacy_reports/综述修订/) | 1/1 | 综述修订历史作品系列 | 保留系列版本与上下文 | 理论归属、发表状态和科学结论均待审 | 暂保留历史分组 |
| [04_publications/visualizations](../04_publications/visualizations/) | 1/1 | 公共可视化 | 支持跨模型解释 | 模型专属图回到模型论文层 | 保留 |

### 90_archive

| 目录 | 直接/递归文件 | 职责 | 保留理由 | 边界与风险 | 判断 |
|---|---:|---|---|---|---|
| [90_archive](../90_archive/) | 1/31 | 跨项目历史与迁移证据 | 保证演变可追溯 | 不参加当前研究成熟度判断 | 保留 |
| [90_archive/legacy](../90_archive/legacy/) | 6/24 | 历史研究系列 | 保留原有版本关系 | 历史标题和结论待审 | 保留 |
| [90_archive/legacy/GAQ_UFT_v1_几何原子](../90_archive/legacy/GAQ_UFT_v1_几何原子/) | 5/5 | GAQ_UFT_v1_几何原子历史版本 | 保存既有研究或布局演变 | 历史内容与旧链接不表示当前约定 | 保留归档 |
| [90_archive/legacy/GAQ_UFT_v3_三大新体系](../90_archive/legacy/GAQ_UFT_v3_三大新体系/) | 5/5 | GAQ_UFT_v3_三大新体系历史版本 | 保存既有研究或布局演变 | 历史内容与旧链接不表示当前约定 | 保留归档 |
| [90_archive/legacy/GAQ_UFT_v4_全维统一](../90_archive/legacy/GAQ_UFT_v4_全维统一/) | 1/1 | GAQ_UFT_v4_全维统一历史版本 | 保存既有研究或布局演变 | 历史内容与旧链接不表示当前约定 | 保留归档 |
| [90_archive/legacy/GAQ_UFT_v5_cħ几何化](../90_archive/legacy/GAQ_UFT_v5_cħ几何化/) | 1/1 | GAQ_UFT_v5_cħ几何化历史版本 | 保存既有研究或布局演变 | 历史内容与旧链接不表示当前约定 | 保留归档 |
| [90_archive/legacy/GAQ_UFT_v6_质量谱](../90_archive/legacy/GAQ_UFT_v6_质量谱/) | 1/1 | GAQ_UFT_v6_质量谱历史版本 | 保存既有研究或布局演变 | 历史内容与旧链接不表示当前约定 | 保留归档 |
| [90_archive/legacy/layout_before_20260907](../90_archive/legacy/layout_before_20260907/) | 5/5 | layout_before_20260907历史版本 | 保存既有研究或布局演变 | 历史内容与旧链接不表示当前约定 | 保留归档 |
| [90_archive/legacy_tools](../90_archive/legacy_tools/) | 2/2 | 废弃工具 | 保存旧操作逻辑供追溯 | 不得作为当前运行入口 | 保留只供查阅 |
| [90_archive/migrations](../90_archive/migrations/) | 0/4 | 迁移记录集合 | 结构变更需要恢复依据 | 不要把当前活跃研究放入这里 | 保留 |
| [90_archive/migrations/20260907_full_layout](../90_archive/migrations/20260907_full_layout/) | 4/4 | 本次迁移快照与映射 | 恢复 193 个迁移前文件字节 | 只代表该时间点；脚本不是可随时重跑的入口 | 保留 |

### 99_inbox

| 目录 | 直接/递归文件 | 职责 | 保留理由 | 边界与风险 | 判断 |
|---|---:|---|---|---|---|
| [99_inbox](../99_inbox/) | 1/11 | 待审资料与研究问题 | 未知归属无需猜测 | 缺少负责人、期限和处置监测 | 保留并补管理 |
| [99_inbox/CMB_B模观测](../99_inbox/CMB_B模观测/) | 1/1 | CMB_B模观测待研究问题 | 为未立项主题保留入口 | 标题不代表成果；须指定模型归属、负责人和处置日期 | 暂保留；待审理 |
| [99_inbox/人工场实验验证](../99_inbox/人工场实验验证/) | 1/1 | 人工场实验验证待研究问题 | 为未立项主题保留入口 | 标题不代表成果；须指定模型归属、负责人和处置日期 | 暂保留；待审理 |
| [99_inbox/大统一完成](../99_inbox/大统一完成/) | 1/1 | 大统一完成待研究问题 | 为未立项主题保留入口 | 标题不代表成果；须指定模型归属、负责人和处置日期 | 暂保留；待审理 |
| [99_inbox/引力非重整化突破](../99_inbox/引力非重整化突破/) | 1/1 | 引力非重整化突破待研究问题 | 为未立项主题保留入口 | 标题不代表成果；须指定模型归属、负责人和处置日期 | 暂保留；待审理 |
| [99_inbox/弦论_LQG统一](../99_inbox/弦论_LQG统一/) | 1/1 | 弦论_LQG统一待研究问题 | 为未立项主题保留入口 | 标题不代表成果；须指定模型归属、负责人和处置日期 | 暂保留；待审理 |
| [99_inbox/弯曲时空三重奏](../99_inbox/弯曲时空三重奏/) | 1/1 | 弯曲时空三重奏待研究问题 | 为未立项主题保留入口 | 标题不代表成果；须指定模型归属、负责人和处置日期 | 暂保留；待审理 |
| [99_inbox/强相互作用精确化](../99_inbox/强相互作用精确化/) | 1/1 | 强相互作用精确化待研究问题 | 为未立项主题保留入口 | 标题不代表成果；须指定模型归属、负责人和处置日期 | 暂保留；待审理 |
| [99_inbox/暗物质直接探测](../99_inbox/暗物质直接探测/) | 1/1 | 暗物质直接探测待研究问题 | 为未立项主题保留入口 | 标题不代表成果；须指定模型归属、负责人和处置日期 | 暂保留；待审理 |
| [99_inbox/暗能量本质](../99_inbox/暗能量本质/) | 1/1 | 暗能量本质待研究问题 | 为未立项主题保留入口 | 标题不代表成果；须指定模型归属、负责人和处置日期 | 暂保留；待审理 |
| [99_inbox/黑洞信息悖论](../99_inbox/黑洞信息悖论/) | 1/1 | 黑洞信息悖论待研究问题 | 为未立项主题保留入口 | 标题不代表成果；须指定模型归属、负责人和处置日期 | 暂保留；待审理 |
