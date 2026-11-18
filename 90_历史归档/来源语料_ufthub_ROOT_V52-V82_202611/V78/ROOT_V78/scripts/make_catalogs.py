"""Create curated equation inventory and falsification matrix (not auto-generated fluff)."""
import csv
from pathlib import Path
root=Path(__file__).resolve().parents[1]
raw='''
SI-01|c=299792458 m/s|E|SI定义，数值本身依赖单位|不能推导G
SI-02|G=6.67430(15)e-11 SI|E|CODATA实验推荐，带不确定度|不能冒充理论预言
DIM-01|[G]=L^3 M^-1 T^-2|E|基本量纲|不是动力学
DIM-02|[c]=L T^-1|E|基本量纲|不是动力学
DIM-03|[hbar]=M L^2 T^-1|E|基本量纲|不是动力学
DIM-04|b=-1; a=5; a+b=2 (contradiction)|E|G=c^a hbar^b 的量纲矛盾|仅限制这一输入集合
DIM-05|G=gamma c^3 L^2/hbar|C|独立长度L及无量纲gamma|若L由G反算则循环
DIM-06|G=gamma2 hbar c/Mstar^2|C|独立质量Mstar|需独立gamma2
G-01|Z=Gc/2|E|定义Z|非独立预测
G-02|G=2Z/c|E|前一式的反演|不能当新基本定律
G-03|r_g=GM/c^2|E|引力长度定义|不能用其反推未知G
G-04|ellP=sqrt(hbar G/c^3)|E|普朗克长度定义|不是独立ellP观测
G-05|alpha_g(m)=Gm^2/(hbar c)|E|无量纲引力耦合|需控制m环境变化
G-06|r_g/lambda_bar_C=alpha_g(m)|E|lambda_bar_C=hbar/(mc)|未独立决定G
G-07|mu=GM|E|轨道动力学典型参数|无法分辨G和M
G-08|(G,M)->(sG,M/s)|E|mu不变的参数退化|需外部M测量
GR-01|Gmunu+Lambda gmunu=8pi G/c^4 Tmunu|E|爱因斯坦方程|G作为输入
GR-02|Tmunu=-2/sqrt(-g) dSm/dg^munu|E|选定应力能量约定|边界与场变量需一致
GR-03|nabla_mu T^munu_total=0|E|Bianchi恒等式/满足场方程|各分量未必单独守恒
GR-04|g(r)=GM/r^2|C|球外牛顿/弱场|内部密度与自转另计
EM-01|Fmunu=d_mu Anu-d_nu Amu|E|阿贝尔场强|不决定引力耦合
EM-02|nabla_mu F^munu=J^nu|E|自然单位Maxwell源方程|需要电流约定
EM-03|u_EM=eps0 E^2/2+B^2/(2mu0)|E|真空局部惯性系|设备能量需完整账本
EM-04|S=(E cross B)/mu0|E|Poynting矢量|非标量引力源
EM-05|sigma_ij=eps0(EiEj-dij E^2/2)+(BiBj-dij B^2/2)/mu0|E|Maxwell应力|不同Tij记号有符号差
EM-06|u(E1+E2)=u1+u2+eps0 E1.dot(E2)|E|局部真空电场叠加|边界能量不能忽略
EM-07|u(B1+B2)=u1+u2+B1.dot(B2)/mu0|E|局部真空磁场叠加|不是独立力的相加
EM-08|I1=E^2-c^2 B^2|E|与Lorentz不变量成比例|不能独自充当全部引力源
EM-09|I2=E.dot(B)|E|宇称奇不变量（比例）|不是能量密度
EM-10|plane wave: I1=I2=0; u>0|E|真空平面波|对仅I1或I2源模型的反例
EM-11|T_EM(E,+B)=T_EM(E,-B), E parallel B|C|理想反转且E,B大小/形状固定|真实设备机械态未必等同
EM-12|E.dot(+B)= -E.dot(-B), E parallel B|E|E固定、B翻转|不保证引力奇响应
EM-13|E_phi=-rho/2 dB/dt|C|准静态空间均匀轴磁场|有限装置近似
EM-14|<U_E>/<U_B>=(omega a/c)^2/10|C|均匀球域、周期平均|非全空间Maxwell精确解
SYS-01|Delta M=Delta E_external/c^2|E|隔离系统净能量变化|需完整系统边界
SYS-02|E_before=E_after|E|封闭系统无外部能量净交换|各能量通道可能变化
SYS-03|g_added~G Delta E/(c^2 r^2)|C|弱场远场单极估算|不能代表设备近场
SYS-04|M_gamma_pair=2E/c^2 for counterpropagating equal E|E|合系统质心系|单个光子质量为零
SYS-05|M_gamma_pair=0 for copropagating collinear photons|E|同向真空光子|数值需避免消差
GRX-01|f(phi)=Mstar^2+xi phi^2|H|玩具标量张量|不是G来源证明
GRX-02|G_tensor=1/(8pi f(phi))|C|自然单位，曲率系数|不等于实验室G_Cav
GRX-03|Box phi-mphi^2 phi+xi R phi-gphigamma F.Ftilde/4=0|C|候选作用量变分|新场存在未证实
GRX-04|nabla_mu(F^munu+gphigamma phi Ftilde^munu)=J^nu|C|候选作用量变分|需一致电流/规范约定
GRX-05|f Gmunu=Tmunu+nabla_mu nabla_nu f-gmunu Box f|C|候选作用量，省略Lambda|T需完整定义
GRX-06|f(phi0+d)-f(phi0-d)=4xi phi0 d|E|f是phi平方|phi0=0时奇响应为零
GRX-07|phi F.Ftilde is parity even for pseudoscalar phi|C|整体宇称变换|若背景破缺需另判
YUK-01|V=-GMm(1+alpha exp(-r/lambda))/r|H|假设性有限程相互作用|未观测本模型
YUK-02|F(x)=3(x cosh(x)-sinh(x))/x^3|C|均匀球外部Yukawa源|x大需稳定实现
YUK-03|Delta g/gN=alpha F(R/lambda)(1+r/lambda) exp(-r/lambda)|C|球外、弱场|点源近似可失效
LAB-01|eta=2(aA-aB)/(aA+aB)|E|组成依赖弱等效原理差异|背景需要独立估计
LAB-02|D=(y++-y+- - y-+ + y--)/4|E|二开关差分代数|同奇偶伪差不能消除
LAB-03|rank([1,x_i])=2 iff x_i varies|E|线性两参数设计矩阵|不能排除未知共同伪差
QFT-01|[Dmu,Dnu]=R_spin+sum g_i F_i|E|总协变导数形式|直和不等于物理大统一
QFT-02|SU(3)c x SU(2)L x U(1)Y|E|标准模型规范群|ROOT尚未独立推导
QFT-03|alpha_g=Gm^2/(hbar c) is operational dimensionless|E|指定m及单位约定|不代表G本源
'''
rows=[]
for line in raw.strip().splitlines():
    a=line.split('|')
    assert len(a)==5,(line,a)
    rows.append(a)
with (root/'data'/'equation_catalog.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['ID','equation','status','assumptions','limitation']);w.writerows(rows)

methods=[
('M01','量纲矩阵','c/hbar/角度','独立G不可能性','增加独立尺度','E'),
('M02','Z定义倒查','Z=Gc/2','参数循环','独立Z量子动力学','E'),
('M03','GM尺度变换','轨道mu','G-M不可分辨','外部质量标定','E'),
('M04','普朗克尺度','ellP','含G定义','不从G反算ellP','E'),
('M05','无量纲耦合','alpha_g','必须明确质量参照','比较不同物理尺度','E'),
('M06','热核诱导引力','场谱/截止','UV及裸项退化','独立UV完成','C'),
('M07','RG量纲嬗变','初始耦合/尺度','UV耦合仍输入','寻找无参数初始条件','C'),
('M08','Einstein-Maxwell','总能动张量','G仍预先输入','明确源/耦合界限','E'),
('M09','电磁波反例','I1=I2=0','不变量非完整源','用Tmunu','E'),
('M10','双电场角度','E1,E2,夹角','交叉能漏计','全场能与电源','E'),
('M11','双磁场角度','B1,B2','应力/交叉能漏计','完整Maxwell场','E'),
('M12','磁场反转零信号','E=0,±B','现实机械伪差','完整系统对照','C'),
('M13','平行E/B奇偶分离','Eparallel±B','电磁T偶，I2奇','测量独立新场耦合','C'),
('M14','伪标量曲率偶耦合','phi²R','phi0=0时无奇重力','检验背景phi0','C'),
('M15','轴子光子候选','phi F Ftilde','尚无实验引力信号','实验电磁边界','H'),
('M16','标量-张量候选','f(phi)R','需额外Mstar/xi','PPN+WEP测试','H'),
('M17','Maxwell诱导电场','B(t)','准静态近似不完整','真实线圈求解','C'),
('M18','封闭电池-磁场账本','电池/线圈/热','重复计数','外部输入同时计量','E'),
('M19','光子系统不变质量','共线/对向','数值消差','配对夹角稳定计算','E'),
('M20','Yukawa点源','alpha,lambda','短程时球体近似错误','稳定球形积分','H'),
('M21','行星密度分层','rho(r)','内部形状可能影响短程力','层积分多天体','C'),
('M22','材料差分','核结合能/电子比例','组成依赖伪差','空白和同材对照','H'),
('M23','微观加速重力','原子干涉','激光相位/电磁系统误差','双同位素/盲测','C'),
('M24','钟频高度差','gh/c²','势差不等于G变化','独立时钟标定','E'),
('M25','螺旋运动学','R,omega,u','不决定场动力学','作用量与规范群','E'),
('M26','光速约束','R²omega²+u²=c²','不能用于有质量质心轨迹','场模态解释','H'),
('M27','五维圆纤维','KK U(1)','不含SU3 SU2谱','完整紧化/手征场','C'),
('M28','规范异常','SM费米子表象','需独立得出表象','一代异常校核','E'),
('M29','规范耦合演化','beta函数','SM耦合不精确交汇','新谱阈值检验','E'),
('M30','总联络曲率','联络直和','形式相加非动态统一','唯一作用量及自由参','E'),
('M31','双反转','四状态数据','同反转伪差无法消除','随机化次序','C'),
('M32','跨环境设计矩阵','不同场/星体','固定环境参数退化','秩/条件数','E'),
('M33','强场曲率不变量','Kretschmann','需真实度规和参数','独立强场观测','E'),
('M34','散射与幺正性','新场传播子','高能增长/负范数','检查UV行为','H'),
('M35','等效原理','组成/自旋','MICROSCOPE约束强','预测eta并比较','E'),
('M36','跨机构独立复现','实验原始数据','单仪器伪差','公开协议与盲审','C'),
]
with (root/'data'/'method_matrix.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['ID','method','inputs','known_failure','next_requirement','status']);w.writerows(methods)
print(f'Catalogs: {len(rows)} equations, {len(methods)} methods')
