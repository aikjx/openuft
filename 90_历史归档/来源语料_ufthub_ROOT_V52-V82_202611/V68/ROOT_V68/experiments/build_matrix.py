from pathlib import Path
import csv,json
root=Path(__file__).resolve().parents[1]
rows=[
('G-01','从 c, ħ, λ 构造 G','THEOREM-NO-GO','量纲矛盾，缺少独立尺度','dimensional_obstruction','不代表一般物理理论永远不能预测 G'),
('G-02','从螺旋 R 独立决定普朗克长度','OPEN','R 为自由参数，未给出稳定真空','helix','需新动力学产生 R'),
('G-03','Einstein-Hilbert 系数的微观来源','CONDITIONAL','指定正则化热核有曲率项','induced_inv_g','额外项/方案依赖'),
('G-04','诱导 G 无尺度拟合','OPEN','N ξ m ell Gbare 均有退化','reverse_fitted_length','新增可观测约束和参数定义'),
('G-05','热核质量阈值','DERIVED','积分表示与级数/连分式一致','heat_kernel_f','仅为指定一圈模型'),
('G-06','G 输入误差传播','OPEN','G 的实测不确定度需纳入','G_OBS','须先有独立模型预测'),
('G-07','诱导宇宙学常数','OPEN','UV 真空能项未被消去','none','需完整重整化/机制'),
('G-08','普适自由落体','OPEN','新增物质荷必须满足等效原理','eotvos_eta','真实材料/源荷未知'),
('G-09','GR 弱场 Newton 极限','KNOWN','已知 GR 而非 ROOT 独立推导','archived V67','不能重新标为原创'),
('G-10','背景场与反作用','OPEN','需全耦合守恒解','none','不能只固定背景'),
('G-11','标量张量 F(χ)>0','PARTIAL','条件模型需正重力动能','symbolic_checks','还需全谱稳定性'),
('G-12','引力波速度','CONSTRAINT','GW170817 约 10^-15','literature','需从特定作用量计算波速'),
('SYM-01','三维螺旋曲率/挠率','DERIVED','参数曲线求导已证明','helix','不是空间本体已被观测'),
('SYM-02','螺旋反演退化','DERIVED','κ=0 情形不可反演','helix_inverse','仅非退化条件成立'),
('SYM-03','轨迹唯一决定电力方向','DISPROVED','q 与 -q 反例','charge-sign argument','必须显式加入荷'),
('SYM-04','空间三力普遍正交','DISPROVED','一般洛伦兹/重力力不互相正交','archived V67','仅特殊构型成立'),
('SYM-05','由局部 5D 圆纤维得到 U(1)','DERIVED','一形式规范变化','kk_one_form_component','无法自动推出 SU3、SU2'),
('SYM-06','SU3xSU2xU1 从 ROOT 产生','OPEN','目前直接输入 SM 群','none','需新几何与表示'),
('SYM-07','手征表示从 ROOT 产生','OPEN','颜色/超荷/代数无法由 κτ 决定','none','构造完整谱和异常抵消'),
('SYM-08','标准模型一代异常抵消','KNOWN-VERIFIED','四个局域条件用有理数复算','anomaly_coefficients','验证给定谱非生成谱'),
('SYM-09','SU2 全局双重态奇偶','KNOWN-VERIFIED','3+1=4 双重态','anomaly_coefficients','新增双重态需重检'),
('SYM-10','不完整谱的异常反例','VERIFIED','只留 Q 出现非零异常','test_incomplete_spectrum_anomalous','是判别条件非发现'),
('SYM-11','SM 一圈耦合三线汇合','DISPROVED-IN-TOY','三个交点不同','pair_intersections','含新粒子的 GUT 仍有可能'),
('SYM-12','新粒子阈值修正','OPEN','没有指定新粒子质量谱','none','需可计算 beta/matching'),
('SYM-13','三代质量混合','OPEN','没有 Yukawa 纹理及动力学','none','拟合与预测分离'),
('SYM-14','核力由径向/切向/轴向导出','OPEN','缺颜色荷与非阿贝尔规范','none','不能将相互作用误作三维向量'),
('SYM-15','候选标量 U1 规范不变','DERIVED','F 的梯度变换抵消','symbolic_checks','仅 Abelian 扇区'),
('Q-01','候选额外标量 Euler-Lagrange','DERIVED','局部有限自由度独立符号导数','symbolic_checks','不等于场的全部量子一致性'),
('Q-02','Hilbert 作用量度规变分','KNOWN','标准既有 GR 结果','book 9','不表示新 GR 起源'),
('Q-03','规范 BRST/局域量子一致性','OPEN','本模型未给出完整量子构造','none','必要且尚未证明'),
('Q-04','全局规范异常','PARTIAL','SM 已知谱通过，未知新谱未检查','anomaly_coefficients','不能推广到所有 ROOT 场'),
('Q-05','负范数/鬼态排除','OPEN','需要完整二次涨落与约束','none','局部能量符号不足'),
('Q-06','微因果/Lorentz 协变','OPEN','螺旋示意没有生成 Lorentz 协变动力学','none','需要严格算符或特征分析'),
('Q-07','散射幺正与光学定理','OPEN','尚无完整散射计算','none','实验与数学待补'),
('Q-08','UV 完整量子引力','OPEN','仅有效作用量，不是 UV 完成','none','需更深理论'),
('Q-09','第五力 Yukawa 径向求导','DERIVED','解析力与数值函数一致','yukawa_acc_factor','物理荷均为假设'),
('Q-10','MICROSCOPE 条件性约束','CONSTRAINT','差分自由落体无显著违背','eotvos_eta','不直接约束普适第五力'),
('Q-11','Cassini gamma 约束','CONSTRAINT','PPN gamma 与 GR 一致','brans_dicke_gamma','只对具体模型可映射'),
('Q-12','ROOT 原创新效应检测','OPEN','没有独立新实验确认','none','不得宣布发现'),
('Q-13','数值一致性 vs 物理真实性','DISTINCTION','75+ 数学测试仅证明实现','test_core','不可作为统一证明'),
('Q-14','实验预注册与盲测','OPEN','尚无冻结参数的实验计划','none','需真实研究合作'),
]
p=root/'data/V68_逐项证明缺口与修复矩阵.csv'
with p.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['ID','研究命题','状态','证据或失败原因','验证函数或文档','下一步义务']);w.writerows(rows)
from collections import Counter
report={'total':len(rows),'counts':dict(Counter(r[2] for r in rows)),'note':'statuses describe specific claims, not overall theory success'}
(root/'results/repair_matrix_counts.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(report)
