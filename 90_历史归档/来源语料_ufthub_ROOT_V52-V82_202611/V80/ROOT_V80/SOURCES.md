# 外部资料与证据等级（查询日期 2026-11-18）

| 类别 | 来源 | 数据/约束 | 使用限制 |
|---|---|---|---|
| 基础常数 | NIST CODATA 2022 https://physics.nist.gov/cuu/pdf/JPCRD2022CODATA.pdf | G=6.67430(15)e-11, c exact | G 是测得输入，非理论预测 |
| 行星质量/半径 | NASA https://nssdc.gsfc.nasa.gov/planetary/factsheet/ | 太阳系参考量 | 采用舍入参数，忽略椭球及局地变化 |
| 太阳/行星 GM | JPL https://ssd.jpl.nasa.gov/astro_par.html | 太阳 GM、水星运行数据 | 轨道仅约束 GM，和独立 G 不等价 |
| 微弱等效性 | MICROSCOPE https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.129.121102 | Ti/Pt η ~1e-15 无显著偏离 | 对具体模型需推导材料耦合 |
| 延迟/光传播 | Cassini https://www.nature.com/articles/nature01997 | γ-1=(2.1±2.3)e-5 | 单组 PPN 约束不是任意新模型的直接界限 |
| 双脉冲星 | PRX 11.041050 https://journals.aps.org/prx/abstract/10.1103/PhysRevX.11.041050 | GR 四极辐射 1.3e-4 at 95% | 指定时序模型与不确定度 |
| GW/电磁同源 | LVK https://ligo.org/science-summaries/GW170817GRB/ | 2017 事件延迟 1.7 秒 | 固有发射延迟须建模 |
| 2026 强场引力 | LVK https://ligo.org/science-summaries/o4b_tgr/ | 77 新高显著信号与旧样本组合 | 未在本包下载波形数据做统计推断 |
| 黑洞几何 | EHT https://eventhorizontelescope.org/publications/first-sagittarius-event-horizon-telescope-results-vi-testing-black-hole-metric | Sgr A* 环与时空测试 | 辐射转移和质量/距离模型依赖 |
| 磁星强场 QED | MNRAS https://academic.oup.com/mnras/article/539/4/3655/8123400 | 约 4.41e9 T 临界 QED 场 | 高场需要 QED/EOS 耦合，B 值为演示输入 |
| 2026 引力综述 | PDG https://pdg.lbl.gov/2026/reviews/astro-cosmo.html | 多通道检验框架 | 非原始数据集 |

**可靠性声明**：表中磁场示意值、白矮星/中子星质量半径是为模型教学而选择的对比参数，不是观测拟合。宇宙学、引力波/射电计时、EHT 与磁星的原始文件不随本包分发，故本项目仅能通过理论基准数值与已报告约束进行定性/条件审计。
