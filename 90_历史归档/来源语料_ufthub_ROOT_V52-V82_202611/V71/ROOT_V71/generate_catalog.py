from pathlib import Path
import csv
P=Path(__file__).resolve().parent
# Each entry: category | statement | equation | status | preconditions | verification
rows=[]
def add(category,entries):
    for name,formula,status,conditions,test in entries:
        rows.append({'编号':f'E{len(rows)+1:03d}','领域':category,'方程名称':name,'方程LaTeX':formula,'证据状态':status,'前提与边界':conditions,'验证方式':test})
C='既有定律';D='条件推导';H='候选假设';O='开放问题'
add('空间螺旋与运动学',[
('圆柱螺旋轨迹',r'\\mathbf r=(R\\cos\\omega t,R\\sin\\omega t,ut)',D,'欧氏三空间固定R,u,ω','解析求导'),
('速度',r'\\mathbf v=(-R\\omega\\sin\\omega t,R\\omega\\cos\\omega t,u)',D,'恒定R,u,ω','数值差分'),
('总速度',r'v^2=(R\\omega)^2+u^2',D,'欧氏三维','单元测试'),
('ROOT光速约束',r'(R\\omega)^2+u^2=c^2',H,'不可直接用于有质量粒子的惯性世界线','相对论约束检查'),
('螺旋角',r'R\\omega=c\\cos\\lambda,\\ u=c\\sin\\lambda',D,'预设v=c','恒等代入'),
('加速度',r'\\mathbf a=(-R\\omega^2\\cos\\omega t,-R\\omega^2\\sin\\omega t,0)',D,'圆柱螺旋','解析求导'),
('加速度模',r'|\\mathbf a|=R\\omega^2',D,'恒定ω','单元测试'),
('曲率',r'\\kappa=R\\omega^2/v^2',D,'v不为0','交叉积'),
('挠率',r'\\tau=u\\omega/v^2',D,'v不为0','三重积'),
('曲率挠率比',r'\\tau/\\kappa=u/(R\\omega)',D,'κ非零','代数'),
('曲率挠率反演',r'R=\\kappa/(\\kappa^2+\\tau^2)',D,'κ正且螺旋非退化','代数'),
('角速度反演',r'|\\omega|=v\\sqrt{\\kappa^2+\\tau^2}',D,'非退化','单元测试'),
('Frenet正交',r'\\mathbf T\\cdot\\mathbf N=\\mathbf T\\cdot\\mathbf B=\\mathbf N\\cdot\\mathbf B=0',D,'光滑曲线非零曲率','数学证明'),
('运动分解',r'\\mathbf a=\\dot v\\mathbf T+v^2\\kappa\\mathbf N',C,'Frenet框架','数学证明'),
('Lorentz间隔',r'ds^2=-c^2dt^2+d\\mathbf x^2',C,'平直时空和(-+++)','Lorentz不变量'),
('惯性本征时',r'd\\tau=dt\\sqrt{1-v^2/c^2}',C,'有质量粒子平直惯性系','极限测试'),
])
add('物质、引力与天体',[
('应力能量张量',r'T_{\\mu\\nu}=-2(\\sqrt{-g})^{-1}\\delta S_m/\\delta g^{\\mu\\nu}',C,'微分同胚不变物质作用量','变分'),
('Einstein场方程',r'G_{\\mu\\nu}+\\Lambda g_{\\mu\\nu}=8\\pi G T_{\\mu\\nu}/c^4',C,'广义相对论','弱场极限'),
('Einstein-Hilbert作用量',r'S_g=c^3/(16\\pi G)\\int d^4x\\sqrt{-g}(R-2\\Lambda)',C,'x0=ct且d4x单位m4','量纲审计'),
('Bianchi恒等式',r'\\nabla^\\mu G_{\\mu\\nu}=0',C,'Levi-Civita联络','协变守恒'),
('能动守恒',r'\\nabla^\\mu T_{\\mu\\nu}=0',C,'总物质能动张量且场方程成立','守恒检验'),
('Poisson方程',r'\\nabla^2\\Phi=4\\pi G\\rho',C,'牛顿弱场非相对论','解析极限'),
('球对称包围质量',r'M(r)=4\\pi\\int_0^r\\rho(s)s^2ds',C,'球对称','质量积分'),
('牛顿重力',r'\\mathbf g=-GM(r)\\hat\\mathbf r/r^2',C,'球对称','Gauss通量'),
('表面引力',r'g_s=4\\pi G\\bar\\rho R/3',C,'球对称','数值计算'),
('潮汐径向',r'\\partial_r g_r=2GM/r^3',C,'真空点源径向分量导数','差分'),
('潮汐横向',r'\\partial_\\perp g_\\perp=-GM/r^3',C,'点源线性潮汐','迹为0'),
('弱场红移',r'\\Delta\\nu/\\nu\\simeq\\Delta\\Phi/c^2',C,'静态弱场','数值计算'),
('稳定高度红移',r'\\Delta\\nu/\\nu=GMh/[c^2R(R+h)]',D,'点源静态弱场','高精度极限'),
('地球J2势',r'\\Phi=-GM/r[1-J_2(a/r)^2P_2(\\sin\\phi)]',C,'轴对称J2近似','势梯度比较'),
('旋转系加速度',r'\\mathbf a_{rot}=\\mathbf a_I-2\\Omega\\times\\mathbf v_{rot}-\\Omega\\times(\\Omega\\times\\mathbf r)-\\dot\\Omega\\times\\mathbf r',C,'旋转参考系','分量核算'),
('轨道圆频率',r'\\Omega_{orb}=\\sqrt{GM/r^3}',C,'牛顿圆轨道','离心条件'),
('Schwarzschild半径',r'r_s=2GM/c^2',C,'非旋转无电荷GR','尺度比较'),
('Schwarzschild ISCO',r'r_{ISCO}=6GM/c^2=3r_s',C,'Schwarzschild时空类时轨道','GR测地线'),
('Kretschmann标量',r'K=48G^2M^2/(c^4r^6)',C,'Schwarzschild外部真空','几何不变量'),
])
add('电磁与规范场',[
('电场Gauss定律',r'\\nabla\\cdot\\mathbf E=\\rho_e/\\epsilon_0',C,'Maxwell经典','散度'),
('磁场Gauss定律',r'\\nabla\\cdot\\mathbf B=0',C,'Maxwell经典','散度'),
('Faraday感应',r'\\nabla\\times\\mathbf E=-\\partial_t\\mathbf B',C,'Maxwell经典','旋度'),
('Ampere-Maxwell',r'\\nabla\\times\\mathbf B=\\mu_0\\mathbf J+\\mu_0\\epsilon_0\\partial_t\\mathbf E',C,'Maxwell经典','旋度'),
('洛伦兹力',r'\\mathbf F=q(\\mathbf E+\\mathbf v\\times\\mathbf B)',C,'点电荷经典模型','符号反例'),
('磁力正交速度',r'\\mathbf v\\cdot(\\mathbf v\\times\\mathbf B)=0',C,'叉乘','恒等验证'),
('场强张量',r'F_{\\mu\\nu}=\\partial_\\mu A_\\nu-\\partial_\\nu A_\\mu',C,'U1','规范不变性'),
('电磁作用量',r'S_{EM}=-\\frac14\\int\\sqrt{-g}F_{\\mu\\nu}F^{\\mu\\nu}\\ d^4x',C,'自然单位规范归一','变分'),
('杨米尔斯场强',r'F^a_{\\mu\\nu}=\\partial_\\mu A^a_\\nu-\\partial_\\nu A^a_\\mu+g f^a{}_{bc}A^b_\\mu A^c_\\nu',C,'规范群和表象预先指定','Jacobi恒等式'),
('杨米尔斯方程',r'D_\\mu F^{a\\mu\\nu}=J^{a\\nu}',C,'规范归一已约定','变分'),
('标准模型群',r'G_{SM}=SU(3)_C\\times SU(2)_L\\times U(1)_Y',C,'经验上成功的规范结构','异常抵消'),
('电荷生成元',r'Q=T_3+Y',C,'SM超荷约定','谱检查'),
('Higgs机制',r'm_W=g v/2',C,'树级标准模型','质量关系'),
('U1立方异常',r'\\sum_f n_f Y_f^3=0',C,'SM单代左手Weyl谱','精确分数'),
('混合重力U1异常',r'\\sum_f n_f Y_f=0',C,'SM单代左手Weyl谱','精确分数'),
('SU2-U1异常',r'3Y_{Q_L}+Y_{L_L}=0',C,'SM单代','精确分数'),
('SU3-U1异常',r'2Y_{Q_L}+Y_{u^c}+Y_{d^c}=0',C,'SM单代','精确分数'),
('Witten异常条件',r'N_{SU(2)\\,doublet}\\equiv0\\ (\\mathrm{mod}\\ 2)',C,'SU2左手双重态','计数'),
])
add('耦合运行与高能',[
('一圈RG方程',r'd\\alpha_i^{-1}/d\\ln\\mu=-b_i/(2\\pi)',C,'1-loop MSbar与阈值忽略','数值差分'),
('一圈解',r'\\alpha_i^{-1}(\\mu)=\\alpha_i^{-1}(M_Z)-(b_i/2\\pi)\\ln(\\mu/M_Z)',C,'1-loop与固定粒子谱','交点计算'),
('标准模型beta',r'(b_1,b_2,b_3)=(41/10,-19/6,-7)',C,'SU5归一和SM谱','已知RG'),
('GUT归一',r'\\alpha_1=5\\alpha_Y/3',C,'SU5习惯','输入审计'),
('三个统一条件',r'\\alpha_1(\\mu_U)=\\alpha_2(\\mu_U)=\\alpha_3(\\mu_U)',H,'需要具体高能动力学','一圈交点对比'),
('Planck质量定义',r'm_P=\\sqrt{\\hbar c/G}',C,'定义使用已测G','反向拟合标注'),
('G的量纲',r'[G]=L^3M^{-1}T^{-2}',C,'SI','线性方程'),
('纯chbar无法构造G',r'\\nexists(a,b):[c^a\\hbar^b]=[G]',D,'不含额外尺度','线性代数'),
('加入独立质量尺度',r'G=\\gamma\\hbar c/M_*^2',H,'M*与γ必须另行预测','辨识性'),
('诱导引力单圈主项',r'1/G_{ind}\\sim N(1-6\\xi)\\Lambda_{UV}^2/(12\\pi)',D,'自然单位实标量固有时间截止/无裸项','热核'),
('引力裸加诱导',r'1/G_{eff}=1/G_{bare}+1/G_{ind}',D,'匹配约定与阈值依赖','参数退化'),
('一圈热核首项',r'a_1=(1/6-\\xi)R',C,'标量Laplace-type算符','热核展开'),
('KK五维一形式',r'dy+kA_\\mu dx^\\mu',D,'圆形额外维度','纤维规范不变性'),
('KK五维度规',r'ds_5^2=g_{\\mu\\nu}dx^\\mu dx^\\nu+\\varphi^2(dy+kA_\\mu dx^\\mu)^2',D,'额外维度+独立标量','坐标变换'),
('低能EFT扩展',r'\\mathcal L=\\mathcal L_{SM}+\\sum_d C_d\\mathcal O_d/\\Lambda^{d-4}',C,'有效场论与对称性','幂次计数'),
])
add('有限程新力与分层源',[
('点源Yukawa势',r'V_Y=-G\\alpha m_1m_2e^{-r/\\lambda}/r',H,'额外假设的线性媒介场','点源极限'),
('点源力比例',r'\\Delta F/F_N=\\alpha(1+r/\\lambda)e^{-r/\\lambda}',D,'点源','径向微分'),
('均匀球形状因子',r'\\mathcal F(x)=3(x\\cosh x-\\sinh x)/x^3',D,'均匀球和线性Yukawa','体积积分'),
('均匀球外势',r'\\Phi_Y=-G\\alpha M\\mathcal F(R/\\lambda)e^{-r/\\lambda}/r',D,'r>=R,测试点','积分'),
('均匀球外力比',r'\\Delta g/g_N=\\alpha\\mathcal F(R/\\lambda)(1+r/\\lambda)e^{-r/\\lambda}',D,'均匀球/r>=R','有限差分'),
('稳定表面因子',r'e^{-x}\\mathcal F(x)=3[(x-1)+(x+1)e^{-2x}]/(2x^3)',D,'x>0','代数恒等式'),
('短程表面极限',r'(\\Delta g/g_N)_{h=0}\\sim3\\alpha\\lambda/(2R)',D,'均匀球,lambda<<R,点测试物体','渐近数值'),
('分层源Yukawa因子',r'\\mathcal F_\\rho=(4\\pi/M)\\int_0^R\\rho(s)s^2\\sinh(s/\\lambda)/(s/\\lambda)\\,ds',D,'球对称线性作用','独立积分'),
('带电荷分层因子',r'\\mathcal F_{\\rho q}=(4\\pi/M)\\int_0^R\\rho(s)q(s)s^2\\sinh(s/\\lambda)/(s/\\lambda)\\,ds',H,'q(s)由具体新微观理论决定','合成源扫描'),
('分层外力比',r'\\Delta g/g_N=\\alpha q_t\\mathcal F_{\\rho q}(1+r/\\lambda)e^{-r/\\lambda}',D,'球对称线性Yukawa与测试质点','解析vs数值'),
('小x形状展开',r'\\mathcal F(x)=1+x^2/10+x^4/280+O(x^6)',D,'x<<1','Taylor'),
('两球有限尺寸',r'F_Y/F_N=\\alpha\\mathcal F(R_1/\\lambda)\\mathcal F(R_2/\\lambda)(1+r/\\lambda)e^{-r/\\lambda}',D,'两不重叠均匀球','体积积分'),
('表面短程衰减',r'\\Delta g(h)\\propto e^{-h/\\lambda}(1+(R+h)/\\lambda)',D,'球外同一源','比值测试'),
('环境屏蔽候选',r'\\Box\\phi=V_{,\\phi}+\\beta\\rho/M_*',H,'需明确V,边界与耦合','非线性场数值解未做'),
('优选方向候选',r'\\delta y=A\\cos(\\omega_\\oplus t+\\varphi)',H,'Lorentz破缺须自洽并受约束','恒星日锁相'),
])
add('推断与证伪',[
('Eotvos参数',r'\\eta=2(a_A-a_B)/(a_A+a_B)',C,'同一源同一惯性设置','单位测试'),
('线性特征模型',r'\\mathbf y=X\\boldsymbol\\theta+\\epsilon',D,'局部线性化/明确合成','矩阵秩'),
('结构可辨识',r'\\operatorname{rank}(X)=n_\\theta',D,'线性参数','SVD'),
('Fisher信息',r'\\mathcal I=X^T\\Sigma^{-1}X',C,'高斯误差/已知协方差','数值条件数'),
('最小二乘',r'\\hat\\theta=(X^T\\Sigma^{-1}X)^{-1}X^T\\Sigma^{-1}y',D,'满秩与已知Sigma','合成恢复'),
('参数协方差',r'\\operatorname{Cov}(\\hat\\theta)=(X^T\\Sigma^{-1}X)^{-1}',D,'线性高斯模型','蒙特卡洛'),
('盲法零假设',r'H_0: \\alpha=0',D,'在试验设计之前预登记','零假设测试'),
('基本引力常数判断',r'\\mu=GM\\quad\\Rightarrow\\quad G,M\\text{退化}',D,'只有轨道动力学和GM','雅可比秩'),
('分层牛顿不可辨识',r'g_A(r)=g_B(r),\\ r>=R,\\ M_A=M_B',C,'球对称相同总质量','构造反例'),
('新力分层可辨识',r'\\mathcal F_{\\rho_A}\\ne\\mathcal F_{\\rho_B}',D,'同质量不同径向分层,有限lambda','数值积分'),
('实验挑战',r'|\\eta_{Ti,Pt}|\\lesssim10^{-15}',C,'MICROSCOPE的约束尺度非统一限值','文献交叉'),
('GW传播条件',r'|v_{GW}/c-1|\\ll1',C,'多信使引力波事件','观测约束'),
])
with (P/'data'/'ROOT_V71_全部核心方程目录.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows([{**r,'方程LaTeX':r['方程LaTeX'].replace('\\\\','\\')} for r in rows])
print('equations:',len(rows))
