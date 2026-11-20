from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
ORIGINAL=Path('/mnt/data/ROOT_V97_非线性内外螺旋闭环_20261118/ledger/ALL_277_ISSUES.csv')
# Self-contained fallback: recover V97 task table from retained original archive.
if not ORIGINAL.exists():
    import zipfile,io
    with zipfile.ZipFile(ROOT/'archive'/'ROOT_V97_original.zip') as z:
        names=[n for n in z.namelist() if n.endswith('ledger/ALL_277_ISSUES.csv')]
        if len(names)!=1: raise RuntimeError('Cannot identify original V97 ledger')
        legacy=list(csv.DictReader(io.StringIO(z.read(names[0]).decode('utf-8-sig'))))
else:
    with ORIGINAL.open(encoding='utf-8-sig',newline='') as f:
        legacy=list(csv.DictReader(f))
# Keep original rows, statuses and criteria unchanged.
new_tasks=[
('三维有限振幅 Maxwell 轨道数值射击','NUMERICAL_MODEL','全六维返回误差低于明确门槛，并用独立积分检查'),
('非零轴向振幅求根','NUMERICAL_MODEL','排除 z=0 平面伪解，给出稳健非零初值'),
('多截面求积收敛','NUMERICAL_MODEL','13/17/21及更高阶磁场源求积比较'),
('非事件固定时间积分交叉验证','NUMERICAL_MODEL','独立积分在相同返回时刻计算六维残差'),
('Boris与高阶ODE交叉验证','NUMERICAL_MODEL','至少三种时间步长证明二阶收敛'),
('轴对称正则角动量守恒','NUMERICAL_MODEL','计算磁通函数与p_phi漂移并审计求积误差'),
('粒子通道真空 Maxwell 方程','NUMERICAL_MODEL','数值核验散度及旋度并表现出网格收敛'),
('光速约束与四速度区别','ESTABLISHED_PHYSICS','明确v<c及U_mu U^mu=-c²的不同意义'),
('三维曲率挠率与局部受力','OPEN','对完整轨迹计算曲率/挠率并与场作用对应'),
('三维闭环曲线是否存在自交','OPEN','以可证实几何界与连续曲线分析排除/确认自交'),
('三维轨道结拓扑','OPEN','计算可靠Alexander/Jones多项式或其他完整拓扑判据'),
('周期轨道的数学存在性严格证明','OPEN','经区间算术/验证式积分为非线性定点证明'),
('五周期 Floquet 线性稳定性','OPEN','移除中性方向并用变分方程与高精度矩阵核查'),
('非线性长期稳定性','OPEN','KAM结构、岛链、扰动和共振区域研究'),
('经典辐射反作用','OPEN','纳入一致的LAD/LL近似与能量收支检查'),
('外部线圈材料及工程热设计','OPEN','电流、发热、功率、机械应力可制造性分析'),
('真实测量可观测量定义','OPEN','确定实验信号、误差预算与独立标定方式'),
('洛伦兹协变的内部螺旋自由度','OPEN','独立作用量与规范、因果、能量稳定性审查'),
('四力共同作用量与粒子谱','OPEN','恢复GR与标准模型且避免循环输入已知参数'),
('第一性原理独立预测G','OPEN','建立非循环、实验可证伪的独立参数预测')]
rows=[]
for r in legacy:
    rows.append({
      'id':r['id'],'issue':r['issue'],
      'status_or_current_result':r['status_or_current_result'],
      'acceptance_criterion':r['acceptance_criterion'],
      'source_version':r['source_version']})
for i,(name,status,criterion) in enumerate(new_tasks,1):
    rows.append({'id':f'V98-{i:02d}','issue':name,
      'status_or_current_result':status,
      'acceptance_criterion':criterion,'source_version':'V98'})
if len(legacy)!=277 or len(rows)!=297:raise ValueError(f'Expected 277+20, got {len(legacy)}+{len(new_tasks)}')
fields=list(rows[0].keys())
with (ROOT/'ledger'/'ALL_297_ISSUES.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
(ROOT/'ledger'/'ALL_297_ISSUES.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Ledger retained {len(legacy)} V97 issues and added {len(new_tasks)} V98 issues = {len(rows)} total')
