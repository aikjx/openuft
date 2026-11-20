"""Build a transparent 115-item research issue ledger, ROOT V91.
States: CLOSED_MATH (mathematical error diagnosed/repaired in specific model),
BASELINE (established result only), PROTOTYPE (implemented but unverified as physics),
OPEN (scientific question unresolved), EXPERIMENT (real data required).
"""
from __future__ import annotations
import csv,json
from pathlib import Path

ROWS = r'''
A01|G=2Z/c 循环定义|Z 若以 G 定义便无预测|引入独立的 Z 动力学方程，否则仅保留换元|不使用 G 作为独立 Z 的输入，仍能预言 G|CLOSED_MATH
A02|G=c²r/m 循环定义|r=GM/c² 时为同义改写|明确独立半径测量或撤回求 G 声称|r 的定义、标定独立于 G|CLOSED_MATH
A03|m=ħ/(cr) 质量预测|常是康普顿尺度定义|给出独立可计算的 r 及质量谱|不用已知 m 反算 r|CLOSED_MATH
A04|螺旋 vθ=c 与 vz 非零|真实正交速度合成超光速|采用 (Rω)²+p²=c² 或重定义非运动参数|各惯性系中不出现超光速粒子轨迹|CLOSED_MATH
A05|螺旋轴向与总速皆 c|横向非零时运动学冲突|区分相速度、群速度、坐标速度和内部相位|模型的能量动量满足相对论色散关系|CLOSED_MATH
A06|时间势的符号与精确性|Φ=-GM/r 时历史符号不一致|以度规和观察者定义 dτ，区分弱场/强场|恢复适当 Schwarzschild 与 PPN 极限|CLOSED_MATH
A07|强场 ω 与牛顿弱场|历史表达衰减 R^-1/2 非 R^-3/2|撤回同一轨道频率弱场退化声称|新表达在 R≫GM/c² 给出 sqrt(GM/R³)|CLOSED_MATH
A08|ISCO=r_g/2|与 Schwarzschild 外稳定轨道 3r_g 冲突|作为已排除假设标记，不作 GR 结果|若提出另类时空须给度规及稳定性比较|CLOSED_MATH
A09|精细结构 α 的 π 公式|候选数值与 CODATA 2022 差约 2.22 ppm|降级为被精密测量排除的精确关系|新公式误差纳入全部已知观测不确定度|CLOSED_MATH
A10|质子电子质量比算术|56π=175.929... 非 1836.15|纠正算术并撤回该质量比预测|由独立机制预测实测质量比|CLOSED_MATH
A11|Z+iZ′ 复数相加|Z 与 Z′ SI 量纲不同|定义物理一致归一化与作用量|两耦合先转换为同量纲再相加|CLOSED_MATH
A12|螺旋解释所有粒子|运动学本身不产生自旋统计和规范结构|给定洛伦兹协变场表示与量子化机制|导出粒子场方程与观测量|OPEN
B13|明确统一的层级|共同作用量不等于基础统一|列低能兼容/共同起源/UV 三门槛|所有宣传严格对应通过的门槛|PROTOTYPE
B14|时空基本自由度|几何与物理变量未独立公设|提出可操作相空间和约束|给出具体态空间、测量与对称变换|OPEN
B15|单一基本作用量|GR+SM 拼接已知但不揭示来源|推导新作用量及全部变分方程|无需预先逐项植入待统一的动力学|OPEN
B16|Lorentz 协变|特权绝对螺旋时间可破坏对称|证明全部可测量 Lorentz 变换规则|变换后事件概率一致|OPEN
B17|广义协变|坐标选择可能混入物理假设|在四维几何中使用协变作用量|不变可观测量保持相同|OPEN
B18|因果性与局域性|可能产生超光速传播或非局域耦合|求特征锥、传播子和局域因果条件|因果支持与实验证据相容|OPEN
B19|初值问题|未证明约束与演化良定|规范固定、超曲面分解与 PDE 良定性|合理初值存在唯一演化（模规范）|OPEN
B20|能量稳定性|候选新自由度可引幽灵或梯度不稳定|线性化频谱、约束与哈密顿量检查|物理自由度正范数且满足稳定条件|OPEN
B21|应力能量守恒|不能仅累加静态能量|从协变变分构造全部 Tμν|在运动方程上满足 ∇μTμν=0|OPEN
B22|牛顿极限|理论须恢复质量源与逆平方律|完整弱场低速展开|得到 ∇²Φ=4πGρ 和观测容差|BASELINE
B23|Maxwell 极限|新理论须恢复电磁动力学|取适当低能规范极限|正确的电磁传播、电荷守恒和极化|BASELINE
B24|Einstein 极限|不能忽略已验证 GR 效应|求后牛顿、强场及波动极限|满足 Solar System、双星、引力波等约束|BASELINE
B25|等效原理|新标量可能引入成分依赖|推导测试体作用量与耦合|给出 WEP/EEP 量并通过观测限制|OPEN
B26|引力自耦合|不能把引力能量当简单局域标量|展开非线性作用量至高阶|与自洽 Einstein 动力学相容|OPEN
B27|G 本源|G 无法仅从 c、ħ 量纲推出|寻找独立质量尺度/动力学机制|不以 G 定义输入常数仍预测其测量值|OPEN
B28|宇宙学常数与真空能|缺乏可接受的真空能解释|理论重整化与宇宙观测同时比较|给出定量且非循环的暗能量机制|OPEN
B29|奇点与高曲率|理论高能区可能失效|构造量子或非微扰扩展|获得受控曲率及可检验延拓|OPEN
B30|独立预测|额外参数可能仅重现已知事实|先验预注册新可测量|在既有观测之外给排他预测|OPEN
C31|四力作用形式起源|耦合本征结构不同|从同一机制推导全部相互作用算符|粒子散射幅与已知极限吻合|OPEN
C32|统一群或基本结构|简单规范大统一无法自动包括 GR|构造群表示和引力耦合|低能群与引力同时正确出现|OPEN
C33|SM 规范群来源|SU3×SU2×U1 是输入|推导对称破缺与群嵌入|精确得到低能规范因子|OPEN
C34|夸克轻子表示|无法任意指定电荷|推导手征表示及超荷|获得正确电荷与异常抵消|OPEN
C35|三代及味层级|缺乏理论解释|构建味对称、质量矩阵|预言三代、混合及质量谱|OPEN
C36|弱相互作用手征性|几何螺旋不足以产生 γ5 结构|给出左右手表示及耦合|正确恢复弱作用宇称破坏|OPEN
C37|Higgs 质量机制|需要解释电弱自发破缺|导出势函数与真空结构|正确预言 W/Z、Higgs 与 Yukawa|OPEN
C38|复合与基本质量|质子质量不等于单一 Higgs 项|包含 QCD 束缚与 Yukawa|正确计算轻子/强子质量|OPEN
C39|中微子质量|标准模型最简形式不能解释全部振荡|引入可检验的 Dirac/Majorana 等候选|满足振荡、宇宙学与双β约束|OPEN
C40|QCD 禁闭|仅有 1/r 核不能生成色禁闭|正确 SU3 非阿贝尔动力学及数值|在非微扰区域重现已知强子谱|BASELINE
C41|弱 CP 破坏|需复杂质量与混合|推导 CKM/PMNS 相位|符合精密味物理检验|OPEN
C42|强 CP 问题|为何 θ_QCD 极小未知|分析 axion 或其它模型|满足电偶极矩和粒子谱限制|OPEN
C43|电弱统一极限|单独 Maxwell 不够|恢复 SU2×U1 破缺后谱|预测光子及 W/Z 相互作用|BASELINE
C44|异常抵消|候选新粒子可能破坏量子一致性|完整三角异常与混合异常计算|每一异常组合为零|OPEN
C45|大统一能标与质子寿命|候选高能态受质子衰变约束|计算匹配/阈值/寿命|不违反实验下限且有可证伪预言|OPEN
C46|耦合跑动|耦合不简单常数|计算含阈值的 RG 流动|与能标依赖实验值相容|OPEN
C47|所有物质能量引力源|不能遗漏压力和应力|变分完整量子场及装置源项|完整 Tμν 账本与守恒一致|BASELINE
C48|不同星球是否改变 G|不同 GM 和 J2 易混淆|独立质量/多方向多材料校准|排除形状、质量与仪器假象|EXPERIMENT
C49|变化电磁场产生引力|已知 EM Tμν 是引力源|求源场耦合并计算装置场|有超出背景的可检验残差才称新效应|BASELINE
C50|全部自由参数起源|当前粒子参数来自实验|计数独立输入并建立推导|无循环预测参数及不确定度|OPEN
D51|时空量子自由度|尚未直接确认|构造量子几何态及观测|明确新实验签名|OPEN
D52|度规量子化|路径积分与算符定义有难题|定义约束、规范及物理态|可计算幺正且协变动力学|OPEN
D53|引力子实在性|弱场扰动量子不等于实测引力子|构造探测协议和背景排除|排他量子证据|EXPERIMENT
D54|自旋2与引力极化|候选不能凭词语指定自旋|线性化传播子、极化张量|恢复低能自旋2 与传播速率|BASELINE
D55|高能 UV 病态|常规 Einstein 微扰非可重整化|提出 UV 固定点/弦/其它受控定义|非微扰自由度和预测稳定|OPEN
D56|引力低能 EFT|EFT 可低能计算但非 UV 完备|从操作性观测量匹配有效算符|结果重定义与规范不变|BASELINE
D57|半经典重力边界|平均 T 不含全涨落|比较噪声、反馈、测量模型|预测并验证适用域|OPEN
D58|两体引力纠缠|模型内相位不等于实测|测量真实纠缠见证|控制 EM 与测量选择偏差|EXPERIMENT
D59|经典替代模型|不能对一切经典模型套用 LOCC 结论|明确局域性、媒介与关联|逐模型给差异或反例|OPEN
D60|传播延迟|冻结静态势忽略动态媒介|协变量子场传播及仪器时间窗|有限传播速度预测并与对照比较|OPEN
D61|退相干预算|理想纯态结果不等于器件表现|用环境谱密度建立噪声模型|预测实际可检测纠缠窗口|EXPERIMENT
D62|量子参考钟/测量|坐标时间非直接量测|定义相对钟、路径和探测器|完整可重复的操作量|OPEN
D63|黑洞量子信息|信息保持问题未解决|构造动力学并对照熵/信息|有清晰可推导的演化图景|OPEN
D64|引力波量子性|观测经典引力波不等于量子态|定义压缩/非经典见证|仪器可分辨与背景排除|EXPERIMENT
D65|引力 EFT 一圈效应|势项不能代替规范不变读数|计算完整散射/干涉观测|给匹配不变的误差预算|OPEN
D66|可测量子引力新预测|当前尺度一圈信号过小|寻找强于系统噪声的替代通道|排他且可复现实验信号|OPEN
E67|冻结路径近似|位置分支可能动态变化|加入波包与反冲的时间演化|近似误差量化并小于目标|OPEN
E68|四分支核推广|V90 只研究径向与点源|扩展非径向/动态/有限尺寸|独立积分和微分交叉校核|PROTOTYPE
E69|相位包裹|测到 sin 相位无法简单反演|建立相位扫描或层析|给连续带符号相位与置信区间|EXPERIMENT
E70|相位局域规约|局部 phase 改变非物理|仅使用局域不变量|数值结果不随局部相位变化|BASELINE
E71|Yukawa 参数约束|不能任意设 α=1|叠加公开实验 exclusion 曲线|候选参数未被既有数据排除|OPEN
E72|α 与 λ 长程退化|远距离可测组合近似 α/λ³|加入新形状和独立量测|Fisher 满秩且误差有限|PROTOTYPE
E73|Coulomb/Newton 核同形|仅距阵秩一|独立电荷诊断、符号反转和空装置|去掉偶电荷背景或独立校准|PROTOTYPE
E74|有限尺寸质量积分|球壳定理不能推广到新力|实测密度与非球形核卷积|与直接积分一致|OPEN
E75|组成依赖|新荷可能取决于材料|多材料双差和独立校准|组成项通过系统对照|EXPERIMENT
E76|完整 1PN 干涉读数|历史仅计算代表势项|求动力学、路径与钟完整贡献|坐标与场重定义不改变结果|OPEN
E77|规范不变 EFT 相位|单势函数可变|计算操作性探测器读数|不同规范下同一结果|OPEN
E78|相关噪声|独立噪声假设过于理想|建立非对角协方差与 GLS|不确定度正确覆盖|PROTOTYPE
E79|Fisher 参数辨识|固定 λ 满秩不意味着联合可辨识|联合未知数线性化并消 nuisance|最小 Fisher 特征值受控|PROTOTYPE
E80|长程条件数|FY-FN 随 λ^-3 消失|精确界及大范围形状扫描|给检测极限和失败条件|PROTOTYPE
E81|两距离牛顿消零|代数消零可放大噪声|用协方差优化零化权重|增益高于相应噪声损失|PROTOTYPE
E82|三距离高阶零化|高阶 EM 也被保留|引入多极/材料对照|目标项可与所有 nuisance 分开|OPEN
E83|profile likelihood 区间|非高斯退化不可简单对称拟合|模拟覆盖率与参数边界|有校准的置信区间|OPEN
E84|多理论模型选择|只拟合偏差易过拟合|零模型、新力、材料噪声同场比较|独立保留数据上验证|OPEN
E85|数值严重相消|先求 FY 再减 FN 会损精度|使用精确正积分或高精度核算|极长 λ 仍能计算非零差异|PROTOTYPE
E86|SYNTHETIC 与观测隔离|仿真不是发现|数据元信息与来源清单|无法将合成数据误标为实测|PROTOTYPE
F87|实验装置可制造性|理想量子质量位置叠加技术困难|逐器件明确尺寸和仪器|完成原型及独立验收|EXPERIMENT
F88|大质量空间叠加|需生成、保持两体非经典态|给路径选择与重合度测量|完整态准备与层析|EXPERIMENT
F89|相干寿命|环境导致相位损失|测量退相干速率与谱|超过最短互动窗口|EXPERIMENT
F90|纠缠见证|concurrence 非直接单量测|选择实验可测见证及门槛|排除经典可分离状态|EXPERIMENT
F91|残余净电荷|单电子可压倒弱引力|独立电荷诊断/主动放电|误差预算低于目标|EXPERIMENT
F92|表面斑块电势|电荷偶背景难去除|表面电势表征与材料交换|给系统上界|EXPERIMENT
F93|Casimir 与极化|复杂近场 EM|材料/间距扫描加模型|残差不与引力混淆|EXPERIMENT
F94|磁场和梯度|驱动和磁性导致伪差|反转、空路径、多探测器同步|磁残差低于目标|EXPERIMENT
F95|热与气体噪声|碰撞和热辐射退相干|真空/温度扫描|无源参数拟合后仍显著|EXPERIMENT
F96|机械振动|路径扰动产生相位|独立加速度传感器和盲试|振动伪差满足预算|EXPERIMENT
F97|质量密度校准|未知源质量与 G 退化|独立称重、几何扫描和层析|源项协方差可审计|EXPERIMENT
F98|独立 G 测量|单独 GM 不能解 G|独立校准质量和几何|无循环估计 G 与误差|EXPERIMENT
F99|等效原理|组成变化可能影响新力|不同材料多方向 Eötvös 实验|与 WEP 既有限制比较|EXPERIMENT
F100|GR 精密基准|理论易与既有观测冲突|GPS/水星/脉冲星/引力波联合检验|全数据集兼容|EXPERIMENT
F101|EM 场引力效应|标准 EM 能动张量已产生引力|建完整装置 Tμν|计算可辨识的 GR 基准差分|EXPERIMENT
F102|主动引力调制|移动质量不是改变 G|明确控制量与守恒账本|实测与 GR 预测定量一致或剩余异常|EXPERIMENT
F103|第三方真实复现|单团队研究不足|盲法/原始数据/独立实验室|可重复排他结论|EXPERIMENT
G104|统一符号字典|r、R、ω 等跨稿混用|建立单位、语境、域名录|每个符号有唯一局部定义|PROTOTYPE
G105|自动量纲检查|循环式可能掩盖量纲错误|SymPy 单位矩阵和 SI 检查|所有已保留公式通过|PROTOTYPE
G106|自动符号证明|手工推导可能遗漏条件|生成严格恒等式回归检查|符号等式成立且条件明确|PROTOTYPE
G107|边界反例搜索|只测良性参数会漏错|随机与解析极限反例|不通过的候选被自动标记|PROTOTYPE
G108|高精度数值体系|灾难性消去产生伪新物理|90位对照和稳定积分|满足指定相对/绝对误差界|PROTOTYPE
G109|已知物理基准库|不能无限衍生未经检验公式|建立 CODATA/GR/SM 回归|标明版本和来源|PROTOTYPE
G110|参数辨识审计|满秩判断可能依赖缩放|白化 Fisher 与 nuisance 消元|结构性零空间显式报告|PROTOTYPE
G111|观测证据档案|模拟被误当真实证据|来源 URI、许可和仪器元数据|每个数字可追溯|PROTOTYPE
G112|公式版本治理|历史错误重复出现|列出替代、废止和理由|从旧公式到新状态可追踪|PROTOTYPE
G113|统一理论路线比较|不能单一套路推翻全部替代理论|使用共同协变/谱/实验标准|模型间预测可复核|OPEN
G114|第三方独立复现|同一代码测同一实现不足|独立实现/操作流程与 SHA|异机复算一致|PROTOTYPE
G115|研究结论证据分级|不能把程序运行当物理证明|采用 E/C/H/R/O 与真实数据隔离|每份交付声明证据等级|PROTOTYPE
'''

SCOPE={'A':'历史公式审计','B':'基础作用量','C':'四力与标准模型','D':'量子引力','E':'数学与参数识别','F':'真实实验','G':'工程与科研验收'}
PRIORITY_TOP={'A01','A04','A06','A07','A08','A09','A10','A11','B14','B15','B16','B17','B20','B27','C33','C34','C36','C44','D55','D59','D60','E72','E73','E77','E79','F91','F97','G108'}

def build(root:Path):
    rows=[]
    for line in ROWS.strip().splitlines():
        fields=line.split('|')
        if len(fields)!=6:
            raise RuntimeError(f'Bad row: {line}')
        identifier,title,diagnosis,fix,acceptance,status=fields
        rows.append(dict(id=identifier,domain=SCOPE[identifier[0]],issue=title,
                         diagnosis=diagnosis,remedy_or_research_route=fix,
                         acceptance_criterion=acceptance,status=status,
                         priority='P0/P1' if identifier in PRIORITY_TOP else 'P2/P3',
                         evidence='ROOT V91 exact symbolic/numerical check' if status=='CLOSED_MATH'
                         else ('Established baseline in limited regime' if status=='BASELINE'
                         else 'Model/software only; no real experimental result')))
    if len(rows)!=115: raise AssertionError(f'expected 115 rows, got {len(rows)}')
    ids=[r['id'] for r in rows]
    expected=[f'{prefix}{n:02d}' for prefix,lo,hi in [('A',1,12),('B',13,30),('C',31,50),('D',51,66),('E',67,86),('F',87,103),('G',104,115)] for n in range(lo,hi+1)]
    if ids!=expected: raise AssertionError(f'ID missing/duplicate/out of order: {ids!=expected}')
    p=root/'ledger'
    p.mkdir(exist_ok=True,parents=True)
    (p/'ROOT_V91_115_issues.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    with (p/'ROOT_V91_115_issues.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    from collections import Counter
    stats=Counter(x['status'] for x in rows)
    (p/'STATUS_COUNTS.json').write_text(json.dumps({'total':len(rows),'statuses':dict(stats), 'meaning':{'CLOSED_MATH':'diagnosis / model-level mathematical correction; NOT unified physics','BASELINE':'established theory requirement, NOT new ROOT result','PROTOTYPE':'model/software implementation, not physical validation','OPEN':'fundamental theory still unresolved','EXPERIMENT':'needs real independent physical data'}},ensure_ascii=False,indent=2),encoding='utf-8')
    return dict(stats)
if __name__=='__main__':
    base=Path(__file__).resolve().parents[1]
    print(build(base))
