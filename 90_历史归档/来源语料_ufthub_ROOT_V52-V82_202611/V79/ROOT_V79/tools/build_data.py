"""Generate reproducible calculation tables and plots from reviewed formulas."""
import csv, json, math, pathlib
from datetime import date
from src import core as c
P=pathlib.Path(__file__).resolve().parents[1]
D=P/'data'; R=P/'results'; D.mkdir(exist_ok=True); R.mkdir(exist_ok=True)

EQ=[
('基础','E','c','c=299792458 m/s','SI exact by definition'),
('基础','E','G','G=6.67430(15)e-11 m3/kg/s2','2022 CODATA measured input'),
('基础','E','epsilon mu','mu0*epsilon0*c²=1','SI vacuum Maxwell'),
('运动学','E','螺旋位置','r=(R cos wt,R sin wt,u t)','parametrized curve'),
('运动学','E','螺旋速度','v²=(Rw)²+u²','geometry'),
('运动学','C','光速约束','(Rw)²+u²=c²','ROOT assumption, not observed'),
('运动学','C','螺旋曲率','kappa=cos²(lambda)/R','under speed c'),
('运动学','C','螺旋挠率','tau=sin(lambda)cos(lambda)/R','under speed c'),
('GR','E','EH作用量','S_g=c³/(16piG)*integral sqrt(-g) R d4x with x0=ct','GR action'),
('GR','E','Einstein方程','G_munu=(8piG/c4) T_munu','GR covariant field equation'),
('GR','E','应力定义','T_munu=-2/sqrt(-g)*delta S_m/delta g^{munu}','metric variation'),
('GR','E','协变守恒','nabla_mu T^{munu}=0','whole closed source'),
('GR','E','量子半经典','G_munu=(8piG/c4)<T_munu^ren>','conditional semiclassical'),
('EM','E','电磁场强','F_munu=partial_mu A_nu-partial_nu A_mu','U1 gauge'),
('EM','E','Bianchi恒等式','nabla_mu tildeF^{munu}=0','no magnetic monopoles'),
('EM','E','Maxwell电流方程','nabla_mu F^{munu}=J^nu','natural units convention'),
('EM','E','电场磁场能量密度','u=epsilon0*E²/2+B²/(2mu0)','vacuum SI'),
('EM','E','坡印亭向量','S=(E cross B)/mu0','energy flux'),
('EM','E','EM tensor T00','T00=u','local inertial frame'),
('EM','E','EM tensor T0i','T0i=S_i/c','x0=ct'),
('EM','E','EM tensor Tij','Tij=u deltaij-epsilon0 EiEj-BiBj/mu0','minus Maxwell stress'),
('EM','E','零迹','-T00+sum_i Tii=0','classical Maxwell 4D'),
('EM','E','标量一','I1=E²-c² B²','Lorentz invariant SI'),
('EM','E','标量二','I2=E dot B','pseudoscalar SI'),
('EM','E','平面波条件','|E|=c|B|, E perpendicular B','vacuum plane wave'),
('EM','E','平面波反例','I1=I2=0, T00=epsilon0E²>0','invariants not energy'),
('EM','E','磁反转能量','u(E,B)=u(E,-B)','fixed E'),
('EM','E','电磁应力B反转','Tij(E,B)=Tij(E,-B)','E fixed, spatial Tij'),
('EM','E','能流反转','S(E,-B)=-S(E,B)','for general crossed fields'),
('EM','E','手性密度反转','I2(E,-B)=-I2(E,B)','fixed E'),
('EM','E','磁能体积','U_B=B² V/(2mu0)','ideal uniform region'),
('EM','E','球体体积','V=4pi a³/3','sphere'),
('EM','C','B时间模型','B(t)=B0 cos(omega t)','quasistatic imposed profile'),
('EM','C','B磁能频谱','u_B=B0²/(4mu0)*(1+cos2omega t)','squared field'),
('EM','C','法拉第场','E_phi=-rho dotB/2','uniform axial B quasistatic'),
('EM','C','法拉第球能','U_E=epsilon0 pi a5 dotB²/15','sphere integration'),
('EM','C','平均能比','<U_E>/<U_B>=(omega a/c)²/10','quasistatic sphere'),
('EM','C','有效性参数','eta=omega a/c','must be <<1'),
('源账本','E','闭合总能守恒','dE_total/dt=0','no external flux/work'),
('源账本','E','净增质量当量','DeltaM=DeltaE_total/c²','closed rest system'),
('源账本','C','远场附加重力','Delta g~G DeltaE_total/(c²D²)','far static monopole'),
('源账本','C','远场多极引力波','hTTij=2G/(c4D)*ddotQTTij','weak slow farzone'),
('源账本','C','四极量级','h~2G(4pi f)² DeltaU a²/(c6D)','uncontrolled shape factor'),
('轴子','H','轴子光子作用','L_int=-(g_ag/4)a F tildeF','new coupling hypothetical'),
('轴子','C','拓扑项直接应力','delta_g integral a F wedge F=0','independent a,A'),
('轴子','C','轴子场方程','Box a-Vprime=(g_ag/4)FtildeF','given action'),
('轴子','C','修正Maxwell','nabla_mu(F^{munu}+g_ag a tildeF^{munu})=Jnu','given action'),
('轴子','H','玩具模态','a_ddot+2Gamma a_dot+omega_a²a=s0 cos omega t','phenomenology not sourced full PDE'),
('轴子','C','玩具模态振幅','A=s0/sqrt((omega_a²-omega²)²+4Gamma²omega²)','linear oscillator'),
('轴子','C','模态相位','delta=atan2(2Gamma omega,omega_a²-omega²)','linear oscillator'),
('轴子','H','平方曲率耦合','F(a)=F0+xi a²','hypothetical'),
('轴子','C','背景一次谐波','A1=2xi a0 A','given quadratic coupling'),
('轴子','C','二次谐波','A2=xi A²/2','given quadratic coupling'),
('轴子','C','零背景选择规则','a0=0 implies A1=0','given quadratic coupling'),
('常数','E','ROOT重参数化','Z=Gc/2 -> G=2Z/c','definition not prediction'),
('常数','E','引力长度','rg=GM/c²','definition'),
('常数','E','普朗克长度','lP=sqrt(hbar G/c³)','definition'),
('常数','E','电子无量纲引力','alphaG=G me²/(hbar c)','depends on G'),
('常数','R','从c,hbar独立G','no dimensional solution G=c^a hbar^b','dimensional no-go for chosen input'),
('量子','E','双光子不变质量','M² c4=2E1E2(1-cos theta)','free photon pair'),
('量子','E','共线光子质量','theta=0 => M=0','ideal photons'),
('量子','E','反向光子质量','theta=pi, E1=E2=E => M=2E/c²','photon pair rest frame'),
('实验','H','B奇信号','signal(B)=-signal(-B)','not automatically gravity'),
('实验','C','频谱2f判据','squared field -> DC+2f','not unique to gravity'),
('实验','C','频谱1f判据','E dot B drive at f','not unique to axion'),
('实验','E','真空GR试验','T_EM=0 in vacuum yet curvature can be nonzero','Schwarzschild exterior'),
]

def writecsv(path,head,rows):
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f); writer.writerow(head);writer.writerows(rows)
writecsv(D/'equation_catalog.csv',['id','domain','proof_status','name','equation','scope'],[(f'V79-{i:03}',*eq) for i,eq in enumerate(EQ,1)])
METHODS=[
('变分原理','检查完整模型应力与耦合','作用量定义并包含物质支撑','未给出闭合作用量','条件严格'),
('静态EM应力','计算T00、Tij','E、B精确测量','只用场强标量代替T','已确立'),
('平面波反例','排除标量为零即无引力','E=cB且垂直','把两个场不变量误当成T','已确立'),
('Lorentz提升','检查两个电磁不变量','速度小于c','参照系依赖误判','已确立'),
('场能二次谐波','提取B²的2f分量','B近似余弦','线圈源未计入','条件严格'),
('法拉第耦合','计算感生E能量','准静态均匀B观测区','高频超出ωa/c<<1','条件严格'),
('数值独立积分','验证体积系数','球对称观测区域','网格精度不足','数值'),
('全装置能量账本','排除内部转换增重','能量闭合','漏掉电源/支撑/热/辐射','已确立'),
('远场多极计算','辨别总质量与空间分布','已知全源T且远辐射区','在10米套辐射远场公式','条件严格'),
('伪标量拓扑','求直接度规应力','最小aFtildeF','误认拓扑项为直接引力源','已知理论'),
('伪标量动力学','求axion传播','独立场与模型参数','仅E·B不能决定a','候选'),
('奇偶分离','分辨EM偶和E.B奇','固定平行E/B实验','串扰也会奇','已知筛选'),
('频谱锁相','分别测f和2f','线性接收器已校准','非线性电子学伪差','试验设计'),
('零背景对称性','检验a0=0下f项是否消失','二次曲率耦合','别的项产生f','候选'),
('非零背景','尝试检验1f信号','背景可独立测量','a0从G回填','候选'),
('等能不同储存','比电池/电容/磁体','完整质量/应力匹配','质量多极不同','试验设计'),
('假负载','分离加热/电源振动','匹配电学耗散','假负载控制不充分','试验设计'),
('磁屏蔽','分离漏磁','机械结构保持等价','屏蔽改变重量和热','试验设计'),
('真空扭秤','缩小气流与浮力','高真空高灵敏','静电漏磁背景','已用实验方法'),
('原子干涉仪','量子自由落体测量','环境噪声受控','磁能级相位偏差','试验设计'),
('光钟','重力红移与变化场','避免电磁Stark/Zeeman移频','频移非引力','试验设计'),
('重复盲测','排除偶然/分析偏差','预注册阈值','试验结果选择性报告','试验设计'),
('外部零结果','对照2024稳场实验','匹配其测试配置','理论无上界/未约束','实证约束'),
('CODATA对比','输入常数并传播不确定度','G以实验值输入','回填冒充预测','已知理论'),
('维度筛选','检验只用c,hbar','不额外引入尺度','忘记质量量纲','严格否定'),
('规范异常','独立检查强弱群谱','完整量子场模型','仅凭空间曲线无手征谱','开放'),
('重整化群','从UV生成动态能标','独立固定边界条件','靠实验G标定UV','开放'),
('新物理严格胜出','冻结参数并预测盲测','实验独立复现','模拟不能代替观测','开放'),
]
writecsv(D/'method_matrix.csv',['id','method','goal','assumption','failure_or_confusion','status'],[(f'M-{i:02}',*x) for i,x in enumerate(METHODS,1)])

SCANS=[]
for B in [0,0.01,.1,1,3,5,10,15,20]:
    s=c.Scenario(B,50,1,10).evaluate()
    SCANS.append((B,s['max_magnetic_J'],s['mean_equivalent_mass_kg'],s['net_energy_added_farfield_g_scale']))
writecsv(D/'magnetic_scan.csv',['B_T','U_B_max_J','mean_field_mass_kg','farfield_added_energy_g_mps2_if_net_added'],SCANS)

SCANF=[]
for f in [0,1,10,50,100,1e3,1e4,1e5,1e6,1e7,1e8]:
    scan=c.Scenario(10,f,1,10).evaluate()
    SCANF.append((f,scan['induced_ratio'],scan['omega_a_over_c'],scan['omega_a_over_c']<0.1))
writecsv(D/'frequency_quasistatic_scan.csv',['frequency_Hz','avg_E_over_B_energy','omega_a_over_c','illustrative_quasistatic_flag_eta_lt_0_1'],SCANF)

TIME=[]
s=c.Scenario().evaluate()
for i in range(257):
    phase=2*math.pi*i/256
    ub,ue=c.cycle_energy(10,50,1,phase)
    TIME.append((i/256,ub,ue,ub+ue,2*s['max_magnetic_J']-ub-ue,2*s['max_magnetic_J']))
writecsv(D/'time_energy_ledger.csv',['cycle_frac','magnetic_J','induced_E_J','region_EM_J','reserve_J_assumed','total_J'],TIME)

PAR=[]
E=(0,0,1e6)
for sg in [1,-1]:
    B=(0,0,sg*10.)
    d=c.parity_check(E,B)
    PAR.append((sg,c.energy_density(E,B),c.invariants_SI(E,B)[0],c.invariants_SI(E,B)[1],d['delta_tensor_max']))
writecsv(D/'field_parity.csv',['B_sign','energy_density_J_m3','I1','I2_EdotB','tensor_diff_under_B_flip'],PAR)

WALSH=[]
for a0 in [0,.1,1,2]:
    for A in [0,.25,.5,1,2]:
        a1,a2=c.quadratic_coupling_response(a0,A,1)
        WALSH.append((a0,A,a1,a2))
writecsv(D/'axion_toy_harmonics.csv',['a_background_toy','oscillation_amplitude_toy','f_coefficient_toy','2f_coefficient_toy'],WALSH)

s=c.Scenario().evaluate()
fourier=[c.fourier_amplitude([row[1] for row in TIME[:-1]],n) for n in range(5)]
summary={'version':'V79','status':'known_theory_plus_toy_hypothesis_not_new_physics',
 'constants':{'G_m3_kg_s2':c.G,'c_m_s':c.C,'epsilon0_F_m':c.EPS0,'mu0_H_m':c.MU0},
 'baseline':s,'baseline_freq_harmonics_magnetic_J':{str(i):{'cos':x,'sin':y} for i,(x,y) in enumerate(fourier)},
 'counts':{'equations':len(EQ),'methods':len(METHODS),'data_tables':5},
 'important_limitations':['G is imported as CODATA input','field volume is illustrative not physical coil','2f energy is not gravitational wave discovery','finite distance is not necessarily far-zone','axion oscillator is unconstrained toy model']}
(R/'numerical_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    def saveplot(name):plt.tight_layout();plt.savefig(R/name,dpi=150);plt.close()
    plt.figure(figsize=(8,4))
    plt.plot([r[0] for r in TIME],[r[1]/1e6 for r in TIME],label='Magnetic energy (MJ)')
    plt.plot([r[0] for r in TIME],[r[2]/1e-5 for r in TIME],label='Induced E energy (1e-5 J)')
    plt.xlabel('Drive cycles');plt.ylabel('Separate normalized units');plt.legend();saveplot('time_energy_harmonics.png')
    plt.figure(figsize=(8,4))
    plt.loglog([r[0] for r in SCANF if r[0]>0],[r[1] for r in SCANF if r[0]>0],marker='o')
    plt.axvline(.1*c.C/(2*math.pi),linestyle='--',label='eta=0.1 threshold for a=1m')
    plt.xlabel('Frequency (Hz)');plt.ylabel('Quasistatic average UE/UB');plt.legend();saveplot('induced_electric_ratio.png')
    x=[k/150 for k in range(1,400)]
    plt.figure(figsize=(8,4))
    for d in [.02,.1,.3]:
        arr=[abs(c.oscillator_response(q,1,d,1)[0]) for q in x]
        plt.plot(x,arr,label=f'damping={d} (toy)')
    plt.yscale('log');plt.xlabel('Drive frequency / oscillator frequency');plt.ylabel('Toy response amplitude');plt.legend();saveplot('toy_axion_resonance.png')
    plt.figure(figsize=(8,4))
    for a0 in [0,.3,1.0]:
        z=[c.quadratic_coupling_response(a0,A,1)[0] for A in x]
        plt.plot(x,z,label=f'background a0={a0}')
    plt.plot(x,[c.quadratic_coupling_response(0,A,1)[1] for A in x],linestyle='--',label='2f at a0=0')
    plt.xlabel('Amplitude A (toy)');plt.ylabel('Coupling harmonic coefficient');plt.legend();saveplot('parity_frequency_selection.png')
except ImportError:
    print('matplotlib not installed: generated CSV/JSON without PNG')
print(json.dumps({'equations':len(EQ),'methods':len(METHODS),'tables':5,'baseline':s},ensure_ascii=False,indent=2))
