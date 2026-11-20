from pathlib import Path
import csv, json
ROOT=Path(__file__).resolve().parents[1]
ORIG=ROOT/'ledger'/'V94_original_205.csv'
with open(ORIG,encoding='utf-8-sig',newline='') as f: old=list(csv.DictReader(f))
new=[
('H01','是否存在紧支撑静磁场可准确维持指定轨道？','CONDITIONAL_MATH','给出 C∞ 矢势、闭环上 Lorentz 方程及紧支撑证明'),
('H02','嵌入闭合曲线的管状投影是否唯一？','CONDITIONAL_MATH','验证闭合曲线存在正管状半径；独立计算具体形状的安全半径'),
('H03','沿轨道的最低范数磁场能否显式计算？','CONDITIONAL_MATH','证明 B0 与切向量正交且受力精确'),
('H04','磁场是否满足无磁单极子方程？','CONDITIONAL_MATH','从 B=curl A 推出 divB=0；有限差分独立核验'),
('H05','外部电流是否守恒？','CONDITIONAL_MATH','J=curl B/mu0 且 divJ=0'),
('H06','总磁场能量是否有限？','CONDITIONAL_MATH','给出紧支撑和 U_B 积分；独立网格收敛'),
('H07','磁能量薄管极限是什么？','CONDITIONAL_MATH','推导 U_B/eps² 极限系数，并与数值积分比对'),
('H08','是否存在无电流的非零紧支撑静磁场？','CLOSED_MATH_NO_GO','用调和场积分证明零场定理'),
('H09','有无普适正的最低场能量？','CONDITIONAL_MATH','在不约束电流密度时证明反例：eps→0 使 U_B→0'),
('H10','局域化的电流密度代价是多少？','CONDITIONAL_MODEL','计算 J(ρ) 并检验典型 1/eps 尺度'),
('H11','电子在给定静场中能否严格形成目标闭环？','CONDITIONAL_NUMERIC','ODE 积分周期闭合、守恒速度；与解析曲线交叉核验'),
('H12','闭合轨道是否线性稳定？','OPEN','真实返回映射或 KAM/正常双曲性审计；不从闭合推稳定'),
('H13','小扰动是否会逃出磁管？','CONDITIONAL_NUMERIC','计算指定初始偏差的完整轨道并量化偏离'),
('H14','辐射会否破坏精确周期运动？','CONDITIONAL_PHYSICS','Lienard 能量损失与自洽反作用计算'),
('H15','场源是否能由有限线圈或材料实现？','OPEN_ENGINEERING','给出可装配电流分布、热损耗和磁场误差'),
('H16','测试粒子能否避免与外部电流源干涉？','OPEN_ENGINEERING','给出真空通道与源电流空间分离方案'),
('H17','静态局域外场能否形成无耗散吸引子？','NO_GO_IDEAL','Hamilton 系统相空间保体积，排除全维渐近吸引'),
('H18','是否存在完整自洽 Maxwell–物质场解？','OPEN','同时演化粒子辐射、自场、电流源反作用与支撑结构'),
('H19','光子能否在真空中沿静磁场形成闭环？','NO_GO_STANDARD','标准 Maxwell 光传播不受静磁场 Lorentz 力牵引'),
('H20','打结磁场线是否等于粒子的打结轨迹？','CLOSED_CONCEPT','分清场线拓扑、能流、荷电粒子轨迹'),
('H21','螺旋是否能独立导出 G、强弱耦合和电荷？','OPEN','无循环推导数值及规范结构，提出排他预测'),
('H22','协变描述如何消除参考系依赖？','OPEN','将场源、作用量和可观测量写成四维协变形式'),
('H23','是否能获得有统计功效的独立实验判据？','OPEN_EXPERIMENT','仪器噪声、磁扰、带电体辐射和对照与真实数据'),
('H24','有限能量构造能否独立复现？','ENGINEERING_TEST','源代码、维度测试、精度检查、解压执行、哈希'),
]
assert len(old)==205 and len(new)==24
with open(ROOT/'ledger'/'V95_NEW_24.csv','w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['id','issue','status_or_current_result','acceptance_criterion','source_version'])
 for row in new:w.writerow([*row,'V95'])
rows=old+[dict(zip(['id','issue','status_or_current_result','acceptance_criterion','source_version'],[*row,'V95'])) for row in new]
with open(ROOT/'ledger'/'ALL_229_ISSUES.csv','w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['id','issue','status_or_current_result','acceptance_criterion','source_version'])
 w.writeheader();w.writerows(rows)
(ROOT/'ledger'/'ALL_229_ISSUES.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('V94:',len(old),'new:',len(new),'total:',len(rows))
