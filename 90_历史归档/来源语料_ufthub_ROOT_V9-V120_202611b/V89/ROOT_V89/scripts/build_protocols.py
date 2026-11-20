import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
protocols={
'bmv_mass_phase':{
 'hypothesis':'在排除电磁干扰后，同一冻结路径双量子质量模型出现受引力参数控制的非局部相位',
 'physics':'Delta=(GmAmBt/hbar)*F1(d,sA,sB)',
 'controls':['质量与距离独立计量','净电荷和表面电势约束','磁场反转','装置假动作','盲化实验','复用完整量子态层析'],
 'observables':['Delta_rad','entanglement_witness','state_tomography','decoherence_budget'],
 'failure_conditions':['电荷项不能排除','未测量混合态纠缠','后选择偏差','作用路径模型与实际不符']},
'coulomb_null':{
 'hypothesis':'检查 $1/r$ 势中引力与残余静电的精确退化',
 'physics':'Delta=(t/hbar)*(GmAmB-k_eqAqB)*F1',
 'controls':['独立电荷检出','电荷符号/大小可控时扫描','不同材料与屏蔽','环境电场测量'],
 'observables':['phase_vs_charge','phase_vs_distance','charge_sensor_output'],
 'failure_conditions':['用距离拟合宣称已分开 G 与 Coulomb','混淆浮点等效电荷与可实现净电荷']},
'eft_null_diagnostic':{
 'hypothesis':'三距离消去 1/r 和 1/r^2 形状，只检查计算可辨识性',
 'physics':'w=(a1 cross a2); residual=w dot Delta',
 'controls':['90 位高精度','形状列秩','全部高阶电磁项','真实相位测量噪声','禁止把浮点残差当物理信号'],
 'observables':['null_residual_analytic','null_residual_float','roundoff_ratio'],
 'failure_conditions':['常规数值圆整假阳性','高阶经典效应混淆','量子圈相位远小于噪声']},
'classical_mediator_audit':{
 'hypothesis':'比较受限 LOCC 经典通信、含物质 QFT 经典背景、量子媒介的具体预测',
 'physics':'rho_LOCC=sum_z p(z)*rhoA(z) tensor rhoB(z)',
 'controls':['明确局域性定义','明确经典场自由度','物质传播与绑定态条件','非局域作用是否预设','统一测量与后选择'],
 'observables':['negativity','local_noise','retarded_correlations'],
 'failure_conditions':['用单一经典模型推及所有经典引力','把纠缠自动归结引力子存在']},
'cross_scale_G_source':{
 'hypothesis':'检查 G=2Z/c、GM、Planck 长度等重参数化是否独立预测 G',
 'physics':'G=2Z/c; G=c^3*lP^2/hbar; mu=GM',
 'controls':['不使用实测 G 的独立输入','量纲审计','不同天体独立质量','不确定度传播'],
 'observables':['G_predicted','observed_minus_predicted','source_of_each_parameter'],
 'failure_conditions':['Z 或 lP 是从实测 G 算回','仅以 GM 判定 G 在星球变化']}
}
for name,obj in protocols.items():
 obj={'schema':'ROOT-GCL/3.0','protocol_id':name,'simulation_only':True,'hardware_connected':False,
      'mandatory_result_labels':['THEORETICAL','SYNTHETIC','NOT_OBSERVED'],
      'safety':['不直接执行高电压、高磁场或悬浮装置操作','真实仪器必须经过独立实验室安全审查'],
      'interpretation':'此协议是设计与审计规范，不表示实验已完成',**obj}
 (R/'protocols'/f'{name}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
print('protocols',len(protocols))
