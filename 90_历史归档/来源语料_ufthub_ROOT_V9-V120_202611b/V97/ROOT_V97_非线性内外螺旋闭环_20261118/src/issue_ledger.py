from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
original=ROOT/'ledger'/'V96_ALL_253_ISSUES.csv'
with original.open(encoding='utf-8-sig',newline='') as f:
 rows=list(csv.DictReader(f))
items=[
 ('J01','双向线性共振的完整算术分类','PROVEN_MATH','严格证明有理频率等价于正整数勾股三元组'),
 ('J02','最少需要几个主轨道周期','PROVEN_MATH','证明正且非零双频率的最小公分母为5'),
 ('J03','勾股分类是否表明自然力统一','NOT_IMPLIED','区分整数共振与物理相互作用起源'),
 ('J04','线性5圈共振在有限振幅是否闭合','COUNTEREXAMPLE_NUMERIC','幅度扫描显示非零返回残差'),
 ('J05','固定参考半径下非线性频率漂移','MODEL_NUMERIC','用磁场ODE及频率拟合定量验证'),
 ('J06','非圆形平面周期轨道的存在条件','CONDITIONAL_THEOREM','建立守恒量、有效势、连续性与旋角穿越的条件定理'),
 ('J07','5圈4振荡的非线性数值射击','MODEL_NUMERIC','两端异号、求根、全状态返回和独立核验'),
 ('J08','以不同截面求积阶数求闭环半径','MODEL_NUMERIC','至少4阶源求积并记录残余偏差'),
 ('J09','高精度ODE返回残差与源模型误差','LIMITATION_EXPLICIT','绝不可把ODE残差当绝对实验精度'),
 ('J10','保守磁场中的粒子总能量','ESTABLISHED_BASELINE','数值检查总速率与v·(v×B)=0'),
 ('J11','轴对称场的正则角动量','ESTABLISHED_BASELINE','独立磁通积分守恒检查'),
 ('J12','完整径向一自由度相位积分','CONDITIONAL_THEOREM','独立求转折点并积分旋角，与ODE对照'),
 ('J13','是否真正得到三维非平凡结轨道','OPEN_3D_TOPOLOGY','求出z非零的定常或周期轨道并做拓扑审计'),
 ('J14','三维非线性同振闭合','OPEN_SHOOTING','完整三维返回映射、连续族和稳定性'),
 ('J15','闭合轨道的非线性长期稳定','OPEN_LONG_TERM','KAM、共振岛、Poincare截面与长时随机扰动'),
 ('J16','粒子实际辐射反作用','OPEN_RADIATION','耦合Landau-Lifshitz近似并明确适用性'),
 ('J17','外部电源弥补损耗的能量账','OPEN_ENGINEERING','给出RF补偿、电场相位和热负载方案'),
 ('J18','完整导体自场和电源耦合','OPEN_COIL_SOURCES','考虑温度、电阻变化、场源反作用和机械力'),
 ('J19','空间闭合的Lorentz协变定义','OPEN_COVARIANCE','建立观测者相关回归及四维操作性表述'),
 ('J20','内部以c运动与物质实际速度的区分','OPEN_INTERNAL_DOF','提供独立协变内部自由度及可观测耦合'),
 ('J21','重力G是否由几何频率独立决定','OPEN_G','不得从含G定义中循环计算G'),
 ('J22','强弱电磁引力的统一作用量','OPEN_UNIFICATION','规范群、手征性、异常抵消、GR与SM极限'),
 ('J23','新理论实验上可排他的预测','OPEN_FALSIFIABILITY','先验定量预测，误差预算，真实观测可证伪'),
 ('J24','科研软件与来源独立验收','MODEL_VERIFIED','代码单测、符号、数值重算、哈希和离线网页验证')]
for id_,name,status,criterion in items:
 rows.append(dict(id=id_,issue=name,status_or_current_result=status,acceptance_criterion=criterion,source_version='V97'))
assert len(rows)==277,len(rows)
with (ROOT/'ledger'/'ALL_277_ISSUES.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(ROOT/'ledger'/'ALL_277_ISSUES.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Legacy=253, new={len(items)}, all={len(rows)}')
