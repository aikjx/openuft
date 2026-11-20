from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
new=[
('V99-01','推导轴对称五圈闭环的自交对称性','CLOSED_CONDITIONAL_MATH','在明示的精确周期、双转折初态及单调方位假设下证明四个不同时间对'),
('V99-02','在 V98 连续 ODE 轨迹复核四个空间自交候选','NUMERIC_CROSSCHECK','13/17/21 阶源模型与独立积分容差均通过；不能取代区间存在证明'),
('V99-03','从含自交浸入曲线寻找无自交真实周期轨道','OPEN','自洽动力学获得无自交周期解，至少给出可验证数值根'),
('V99-04','固定能量和角动量的约化哈密顿量','CLOSED_MODEL_MATH','从有明确假设的相对论作用量推导并做量纲检查'),
('V99-05','固定 Pphi 的 Poincare 截面初值约束','NUMERIC_CROSSCHECK','独立磁通积分、半径求根和回归测试'),
('V99-06','考虑事件时间的变分返回映射','NUMERIC_CROSSCHECK','变分 ODE 与中心差分多步长比较'),
('V99-07','二维返回矩阵保面积性质','NUMERIC_CROSSCHECK','det 近 1 并给出截断与数值误差区间'),
('V99-08','退化 Floquet 乘子是否严格为 1','OPEN','区间线性化或多重精度认证迹及谱；给出参数区间'),
('V99-09','完整连续线圈源下周期解区间存在证明','OPEN','验证式 ODE + Krawczyk / interval Newton，处理对称零模'),
('V99-10','源截面积分严格余项上界','OPEN','通过解析界/区间 Gauss 求积证明连续源的收敛'),
('V99-11','有自交曲线不定义普通结类型','CLOSED_MATH','定义辨析与四组数值交点位置验证'),
('V99-12','近似多边形的 Fox knot determinant 诊断','NUMERIC_CROSSCHECK','三投影一致并使用标准 3_1、5_1 与 unknot 测试'),
('V99-13','扰动后无自交周期轨道及其结类型','OPEN','从实际动力学构造无自交周期解，区间检验拓扑不变量'),
('V99-14','辐射反作用长期能量闭合','OPEN_EXPERIMENT','纳入自洽反作用、供能、器件损耗和寿命估计'),
('V99-15','有限尺寸真实源及注入实验','OPEN_EXPERIMENT','制造误差、供电、热、真空、诊断和盲测'),
('V99-16','空间光速螺旋与 GR+SM 四力统一','OPEN_FOUNDATIONAL','独立协变作用量、量子一致性及新实验可证伪预测')]
with (ROOT/'inputs/V98_297_ISSUES.csv').open(encoding='utf-8-sig',newline='') as f:
 old=list(csv.DictReader(f))
 cols=list(old[0]);assert len(old)==297,len(old)
for n,title,state,criteria in new:
 old.append(dict(id=n,issue=title,status_or_current_result=state,acceptance_criterion=criteria,source_version='V99'))
with (ROOT/'ledger/ALL_313_ISSUES.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(old)
(ROOT/'ledger/V99_NEW_16_ISSUES.json').write_text(json.dumps([dict(id=n,title=title,status=state,acceptance=criteria) for n,title,state,criteria in new],ensure_ascii=False,indent=2),encoding='utf-8')
print('V99 ledger',len(old),'entries, appended',len(new))
