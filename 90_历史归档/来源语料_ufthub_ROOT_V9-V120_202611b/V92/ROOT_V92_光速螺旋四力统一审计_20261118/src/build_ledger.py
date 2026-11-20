"""Preserve all 115 V91 tasks, append V92 helix relevance without falsifying their status."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'archive'/'ROOT_V91_原始归档.zip'
LEGACY=ROOT/'ledger'/'ROOT_V91_115_issues_original.csv'

HELIX_TASKS=[
('H01','速度定义','三维速度v与四速度U的不同','已由SR运动学明确区分','采用四维协变变量','数学定义已澄清'),
('H02','螺旋运动学','推导 κ,τ,ω,v 闭环','在常螺旋假设下严格成立','非螺旋路径需用Frenet一般理论','闭合定理已验证'),
('H03','光速公设','全部有质量粒子实际三速度=c','与狭义相对论冲突','若指内部自由度必须重新定义','原朴素公设被反例否定'),
('H04','无质量传播','光子自由传播是否空间螺旋','平直无外力情况下自由光子为空间直线','提供外场或修改动力学的可检验模型','纯自由光子螺旋模型被反例否定'),
('H05','坐标变换','三维挠率是否Lorentz不变','轴向boost可以将tau变0','用世界线协变不变量代替','原命题已否定'),
('H06','力学映射','是否由κ,τ,ω唯一决定所有力','沿直线电场加速有F非零但κ=0','至少引入切向加速度和场变量','简单映射被否定'),
('H07','电磁映射','均匀B的回旋角频率','ω=|q|B/(γm) 已验证','明确B,q,m与场方程输入','条件关系已验证'),
('H08','电场加速','切向F=γ³m dv/dt','静电直线反例','完整Liénard/辐射反作用需另算','模型基准已验证'),
('H09','强相互作用','螺旋能否推出SU(3)色荷与禁闭','无已知推导','构造非阿贝尔规范作用量和量子化','开放'),
('H10','弱相互作用','能否推出手征/中微子/衰变','经典曲线无法替代场论振幅','引入自旋or量子场与粒子表示','开放'),
('H11','引力','空间曲率与四维Riemann区分','量纲与定义不同','世界线测地偏离与场方程','概念区分已验证，动力学开放'),
('H12','维度审计','仅c,κ,τ,ω推导G','无质量维度，严格不可能','引入独立质量尺度和无量纲耦合','不可能性证明完成'),
('H13','新增尺度','c,ħ,κ构造G','可写c³/(ħκ²)但κ独立未定义','独立确定κ，避免Planck长度循环','维度形式已验证，物理开放'),
('H14','量纲碰撞','F与曲率的维度匹配','F=γmv²κ需给定m','独立动力学决定m及作用力','量纲检查完成'),
('H15','曲率场区别','Frenet/规范联络/时空几何','同名curvature非同一物理张量','给出纤维丛联络与表示映射','概念区分完成'),
('H16','Lorentz协变','基本螺旋是否选定优选系','尚无协变模型','构造内部自由度世界线作用量','开放'),
('H17','高阶动力学','曲率平方世界线作用量稳定性','高阶导数易引入额外模态','Dirac约束及谱稳定性检查','开放'),
('H18','参数辨识','几何无法唯一反演B,q/m','不同质荷比场强可给同一螺旋','独立电荷/质量/场校准','反例完成'),
('H19','频率概念','轨道ω与量子相位E/ħ的关系','含义不同，不能默认相等','给出可测相干频率和定标','概念区分完成'),
('H20','粒子质量','r=ħ/mc是否自证m','经常只是康普顿长度换元','预言独立质量与粒子谱','开放'),
('H21','自旋统计','螺旋能否推出1/2自旋','经典轨迹无自旋统计定理','建立Lorentz群表示与费米量子化','开放'),
('H22','保守与耗散','加速电荷辐射如何处理','单理想洛伦兹模型忽略辐射','加入辐射反作用及量子跃迁','开放'),
('H23','光速一致性','光速分解与gamma关系','正定三维运动不等于Minkowski规范','将内部自由度独立于速度','原混淆已否定'),
('H24','模型极限','牛顿/Maxwell/Einstein/SM','仅有螺旋恒等式不保证四者','独立求出作用量及四极限','开放'),
('H25','实验可证伪','B扫描和boost可检验数值','现有磁力学无新预言','提出新参数或新残差并与精密数据比对','开放'),
('H26','内部几何','隐藏螺旋转相不等于轨迹','需要指定内部态空间及变换','构造能产生独立相位的最小模型','开放'),
('H27','能量守恒','设v=c时有质量粒子能量','SR下gamma发散','内部自由度需重定义哈密顿量','简单版本被否定'),
('H28','弱场强场','新螺旋频率能否退化开普勒','旧R^-1/2版本失败','完整场方程及稳定轨道分析','旧候选被反例否定'),
('H29','新观测量','螺旋几何可否预测不同于SM/GR','当前无独立可测预言','预注册差异参数和系统误差','开放'),
('H30','算法复现','代数/数值/独立积分交叉','本轮已建立','扩充真实实验约束输入','软件原型验收'),
('H31','常数来源','规范耦合常数G和弱强常数','纯几何不提供可算数值','动力学与重整化的独立预测','开放'),
('H32','量子引力','是否自动包含时空量子化','曲线运动方程不等于场量子化','构造量子几何并验证','开放'),
]


def status_for(row):
 i=row['id'];p=i[0]
 if i in ('A04','A05','A07','A08','A09','A10','A11'):
  return ('CONTRADICTION_REPAIRED_BY_REJECTION','几何/物理断言已有反例，原结论不可保留；并非更广泛理论已解决')
 if i in ('A01','A02','A03'):
  return ('NON_PREDICTIVE_IDENTITY','换元、康普顿关系或量纲约束不能自证物理新定律')
 if p=='B':return ('OPEN_DYNAMICS','需要独立协变作用量；几何恒等式不构成动力学')
 if p=='C':return ('OPEN_GAUGE','强弱电磁须保留量子场和规范表示')
 if p=='D':return ('OPEN_QUANTUM_GRAVITY','经典螺旋不等于量子引力的证明')
 if p=='E':return ('CONDITIONAL_MODEL','可做数值和辨识性审计，不能替代实验')
 if p=='F':return ('REQUIRES_EXPERIMENT','需要真实标定、排误与独立测量')
 if p=='G':return ('ENGINEERING_CONTINUATION','科研工程可持续改进，不等于基本物理成立')
 return ('OPEN','原状态不变，仍需研究')


def build():
 if not LEGACY.exists():
  import zipfile
  with zipfile.ZipFile(SOURCE) as z:
   matches=[a for a in z.namelist() if a.endswith('/ledger/ROOT_V91_115_issues.csv') or a=='ledger/ROOT_V91_115_issues.csv']
   if not matches: raise FileNotFoundError('V91 ledger inside its archive not found')
   LEGACY.write_bytes(z.read(matches[0]))
 with LEGACY.open(encoding='utf-8-sig') as f: old=list(csv.DictReader(f))
 assert len(old)==115,(len(old),'V91 ledger expected 115')
 detailed=[]
 for x in old:
  status,reason=status_for(x)
  detailed.append({**x,'v92_helix_audit_state':status,'v92_assessment':reason,
                   'v92_completion_means':'Do not change legacy status without independent theoretical or experimental validation'})
 with (ROOT/'ledger'/'V91_115逐项螺旋关联审计.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(detailed[0]));w.writeheader();w.writerows(detailed)
 with (ROOT/'ledger'/'V92_新增32项专门任务.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f); w.writerow(['id','topic','question','diagnosis','next_test','status'])
  w.writerows(HELIX_TASKS)
 (ROOT/'ledger'/'FULL_TRACKER_147.json').write_text(json.dumps({'v91_baseline_count':115,'v92_new_questions_count':32,'total':147,'legacy':detailed,'new':[
 dict(zip(('id','topic','question','diagnosis','next_test','status'),r)) for r in HELIX_TASKS]},ensure_ascii=False,indent=2),encoding='utf-8')
 return {'legacy':len(old),'new':len(HELIX_TASKS),'total':len(old)+len(HELIX_TASKS),'counts_by_v92_state':{k:sum(x['v92_helix_audit_state']==k for x in detailed) for k in sorted({x['v92_helix_audit_state'] for x in detailed})}}

if __name__=='__main__':print(json.dumps(build(),ensure_ascii=False,indent=2))
