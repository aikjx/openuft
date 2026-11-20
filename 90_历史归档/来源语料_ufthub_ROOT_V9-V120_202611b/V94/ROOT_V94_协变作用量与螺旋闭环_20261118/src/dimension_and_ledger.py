"""V94 independently rebuilt SI dimension audit and additive issue ledger."""
import csv, json, itertools, zipfile, io
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# exponents in kg, metre, second, ampere (M,L,T,I)
D={
 'm_kg':(1,0,0,0),'position_x':(0,1,0,0),'path_R':(0,1,0,0),'tube_a':(0,1,0,0),
 'time_t':(0,0,1,0),'path_phase_u':(0,0,0,0),'m_winding':(0,0,0,0),'n_winding':(0,0,0,0),
 'speed_c':(0,1,-1,0),'speed_v':(0,1,-1,0),'beta':(0,0,0,0),'gamma':(0,0,0,0),
 'acceleration':(0,1,-2,0),'jerk':(0,1,-3,0),'curvature':(0,-1,0,0),'torsion':(0,-1,0,0),
 'sigma_dr_du':(0,1,0,0),'udot':(0,0,-1,0),'omega':(0,0,-1,0),
 'momentum':(1,1,-1,0),'force':(1,1,-2,0),'action':(1,2,-1,0),'hbar':(1,2,-1,0),
 'energy':(1,2,-2,0),'radiated_power':(1,2,-3,0),'magnetic_B':(1,0,-2,-1),
 'magnetic_Bdot':(1,0,-3,-1),'magnetic_Bddot':(1,0,-4,-1),
 'electric_E':(1,1,-3,-1),'electric_potential_phi':(1,2,-3,-1),
 'vector_potential_A':(1,1,-2,-1),'charge_q':(0,0,1,1),'current_I':(0,0,0,1),
 'current_density_J':(0,-2,0,1),'charge_density':(0,-3,1,1),
 'epsilon0':(-1,-3,4,2),'mu0':(1,1,-2,-2),
 'electric_energy_density':(1,-1,-2,0),'magnetic_energy_density':(1,-1,-2,0),
 'four_accel_curvature':(0,-1,0,0),'rigid_term_K':(1,4,-2,0),'monodromy_matrix':(0,0,0,0),
 'floquet_multiplier':(0,0,0,0),'frequency_f':(0,0,-1,0),
 'G':(-1,3,-2,0),'planck_length':(0,1,0,0),'stress_energy':(1,-1,-2,0),
 'gradient_E':(1,0,-3,-1),'curl_B':(1,-1,-2,-1),
 'dadt':(0,1,-3,0),'field_flux':(1,2,-2,-1),'path_period':(0,0,1,0),
 'field_source_power_density':(1,-1,-3,0),'spin':(1,2,-1,0)
}

def add(*values):return tuple(sum(x) for x in zip(*values))
def neg(a):return tuple(-x for x in a)
def mul(a,n):return tuple(n*x for x in a)
def E(name,lhs,rhs,classification):return {'formula':name,'left':lhs,'right':rhs,'dimension_match':lhs==rhs,'classification':classification}

def dimension_results():
    d=D
    cases=[
      E('B=gamma*m*(a cross v)/(q*v^2)',d['magnetic_B'],add(d['m_kg'],d['acceleration'],neg(d['charge_q']),neg(d['speed_v'])),'EXACT_ON_TRAJECTORY'),
      E('q(v cross B)=gamma*m*a',d['force'],add(d['charge_q'],d['speed_v'],d['magnetic_B']),'EXACT_ON_TRAJECTORY'),
      E('Bdot = dB/dt',d['magnetic_Bdot'],add(d['magnetic_B'],neg(d['time_t'])),'DEFINITION'),
      E('E=-1/2 Bdot cross (x-r)',d['electric_E'],add(d['magnetic_Bdot'],d['position_x']),'EXACT_INVERSE_FIELD'),
      E('vector_A=1/2 B cross (x-r)',d['vector_potential_A'],add(d['magnetic_B'],d['position_x']),'EXACT_INVERSE_FIELD'),
      E('phi=1/2 (B cross v) dot (x-r)',d['electric_potential_phi'],add(d['magnetic_B'],d['speed_v'],d['position_x']),'EXACT_INVERSE_FIELD'),
      E('J=epsilon0/2*(Bddot cross dx - Bdot cross v)',d['current_density_J'],add(d['epsilon0'],d['magnetic_Bddot'],d['position_x']),'EXACT_INVERSE_FIELD'),
      E('epsilon0 E^2 = energy density',d['electric_energy_density'],add(d['epsilon0'],mul(d['electric_E'],2)),'EXACT_SI'),
      E('B^2 / mu0 = energy density',d['magnetic_energy_density'],add(mul(d['magnetic_B'],2),neg(d['mu0'])),'EXACT_SI'),
      E('dB/dt = -curl E',d['magnetic_Bdot'],add(d['electric_E'],mul(d['position_x'],-1)),'EXACT_MAXWELL'),
      E('curl B = mu0 J + mu0 epsilon0 dE/dt',d['curl_B'],add(d['mu0'],d['current_density_J']),'EXACT_MAXWELL'),
      E('force = gamma*m*v^2*kappa',d['force'],add(d['m_kg'],mul(d['speed_v'],2),d['curvature']),'EXACT_MAGNITUDE'),
      E('dt/du = sigma/v',d['time_t'],add(d['sigma_dr_du'],neg(d['speed_v'])),'EXACT_GEOMETRY'),
      E('omega=m*du/dt',d['omega'],d['udot'],'EXACT_GEOMETRY'),
      E('gamma m a = q E',d['force'],add(d['charge_q'],d['electric_E']),'DIMENSION_CORRECT_NOT_ALWAYS_LAW'),
      E('loop work = force * length',d['energy'],add(d['force'],d['position_x']),'DIMENSION_ONLY'),
      E('time component boost drift=boost_velocity*period',d['position_x'],add(d['speed_v'],d['path_period']),'EXACT_RELATIVITY'),
      E('G=c^3/(hbar*kappa_*^2)',d['G'],add(mul(d['speed_c'],3),neg(d['hbar']),mul(d['curvature'],-2)),'DIMENSION_ONLY_NOT_DERIVATION'),
      E('rigid_term_K*kappa4^2 = energy',d['energy'],add(d['rigid_term_K'],mul(d['four_accel_curvature'],2)),'HYPOTHETICAL_NEW_COUPLING'),
      E('q flux / hbar is phase',d['path_phase_u'],add(d['charge_q'],d['field_flux'],neg(d['hbar'])),'EXACT_AB_PHASE'),
      E('B = kappa alone',d['magnetic_B'],d['curvature'],'INVALID_DIMENSIONS'),
      E('force = omega*kappa alone',d['force'],add(d['omega'],d['curvature']),'INVALID_DIMENSIONS'),
      E('G = c*kappa alone',d['G'],add(d['speed_c'],d['curvature']),'INVALID_DIMENSIONS'),
      E('torsion = angular velocity',d['torsion'],d['omega'],'INVALID_DIMENSIONS'),
      E('Efield = magnetic B',d['electric_E'],d['magnetic_B'],'INVALID_DIMENSIONS'),
      E('current density = charge density',d['current_density_J'],d['charge_density'],'INVALID_DIMENSIONS'),
      E('F = m*c^2',d['force'],add(d['m_kg'],mul(d['speed_c'],2)),'INVALID_DIMENSIONS'),
      E('power = F*v',d['radiated_power'],add(d['force'],d['speed_v']),'EXACT_DIMENSION'),
      E('hbar = action',d['hbar'],d['action'],'EXACT_DIMENSION'),
      E('spin = angular momentum',d['spin'],d['action'],'EXACT_DIMENSION'),
      E('eps0 mu0 = 1/c^2',add(d['epsilon0'],d['mu0']),mul(d['speed_c'],-2),'EXACT_SI'),
      E('Bdot = B/time',d['magnetic_Bdot'],add(d['magnetic_B'],neg(d['time_t'])),'EXACT'),
      E('monodromy eigenvalue dimensionless',d['floquet_multiplier'],d['monodromy_matrix'],'EXACT')
    ]
    out=ROOT/'results';out.mkdir(exist_ok=True)
    with (out/'V94_DIMENSION_BASE.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['quantity','kg_exponent','m_exponent','s_exponent','A_exponent'])
        w.writerows([[name,*exponents] for name,exponents in D.items()])
    with (out/'V94_DIMENSION_PAIRS.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['quantity_a','quantity_b','dimensional_equivalence'])
        w.writerows([[a,b,x==y] for (a,x),(b,y) in itertools.combinations(D.items(),2)])
    with (out/'V94_EQUATION_DIMENSIONS.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['equation','lhs','rhs','matched','classification'])
        for item in cases:w.writerow([item['formula'],item['left'],item['right'],item['dimension_match'],item['classification']])
    if any(x['dimension_match'] for x in cases if x['classification']=='INVALID_DIMENSIONS'):raise RuntimeError('invalid example unexpectedly matched')
    if any(not x['dimension_match'] for x in cases if x['classification']!='INVALID_DIMENSIONS'):raise RuntimeError('model formula dimension failure')
    return {'quantities':len(D),'pairs':len(D)*(len(D)-1)//2,'equations':len(cases),'mismatches':sum(not x['dimension_match'] for x in cases)}

NEW=[
('V94-001','从粒子作用量推导洛伦兹力','MODEL_DERIVED','明确 SR/EM 变分、作用域，禁止称四力统一'),
('V94-002','自由平直时空粒子能否自发形成非平凡空间闭环','NO_GO_PROVEN','无外场自由运动只能直线，给出反例例外条件'),
('V94-003','均匀静 B 能否产生非平凡环面结轨道','NO_GO_PROVEN','严格解析解及曲率/挠率变率冲突'),
('V94-004','任意光滑恒速曲线的逆向磁场存在性','MODEL_DERIVED','给出可验证 B(t) 和前提条件'),
('V94-005','逆向磁场是否支持 Maxwell 方程','MODEL_DERIVED','给出势、外部源电流，验证四条方程'),
('V94-006','逆向场是否具有有限总能量','OBSTRUCTION_FOUND','需要有限支撑、有限能量替代装置'),
('V94-007','外场源是否物理可制造','OPEN_ENGINEERING','明确电流、电压、装置尺寸及边界条件'),
('V94-008','理想 Maxwell 驱动与带电粒子自场一致性','OPEN_PHYSICS','包含真实源电荷与自场，不用外部试验粒子近似'),
('V94-009','带电粒子辐射反馈与能量供给','OPEN_PHYSICS','加入 ALD/LL 合理适用条件并检查守恒'),
('V94-010','三叶结闭环单圈积分精度','NUMERIC_VERIFIED','独立 ODE 前向积分和误差界'),
('V94-011','局部线性稳定性与 Floquet 乘子','NUMERIC_VERIFIED','扰动步长收敛，记录特征值与谱半径'),
('V94-012','全球非线性稳定性','OPEN_PHYSICS','长期积分及鲁棒噪声、边界和随机扰动'),
('V94-013','闭合空间轨迹是否 Lorentz 不变','NO_GO_PROVEN','比较相隔 T 的同位置事件的不同惯性系描述'),
('V94-014','真正时空闭合与闭合类时曲线','DISTINCTION_ESTABLISHED','区分时空事件闭合与空间周期运动'),
('V94-015','是否可让质量为零的自由粒子绕闭合结','OPEN_PHYSICS','明确传播介质/引力场/边界，禁止滥用质量粒子作用量'),
('V94-016','曲率挠率与 B 场必要关系','MODEL_DERIVED','明确 v、q/m 与方向，不能独立导出 q'),
('V94-017','场线结和粒子轨道结是否同一对象','DISTINCTION_ESTABLISHED','明确速度平行磁场时磁力为零'),
('V94-018','量纲对碰覆盖电磁势与源电流','NUMERIC_VERIFIED','基于 SI 基本维进行错误公式筛查'),
('V94-019','独立 85 位逆向场计算','NUMERIC_VERIFIED','使用独立坐标解析导数，比较双精度'),
('V94-020','螺旋几何能否确定基本电荷 q','OPEN_PHYSICS','必须不输入 q 再求出其值'),
('V94-021','螺旋几何能否独立预测 G','OPEN_PHYSICS','不得预先输入 G 定义一个曲率尺度'),
('V94-022','协变内部螺旋新自由度','OPEN_PHYSICS','构造无幽灵、Lorentz 协变的新作用量'),
('V94-023','新螺旋自由度与 SU3 SU2 U1 规范场','OPEN_PHYSICS','正确粒子表示、异常、强弱电磁作用'),
('V94-024','新自由度的 UV 完备性','OPEN_PHYSICS','幺正性、因果与高能一致性'),
('V94-025','新力与既有模型可区分预测','OPEN_EXPERIMENT','设计未被背景吸收的独立可观测量'),
('V94-026','准静态与动态源的能动张量一致性','OPEN_PHYSICS','检查完整场+源体+支撑设备应力能量守恒'),
('V94-027','闭环量子波函数与路径量子相位','OPEN_PHYSICS','规范不变量、边界条件、自旋和测量定义'),
('V94-028','ROOT 历史科研包逐代可复现','ENGINEERING_VERIFIED','历史 ZIP 回归、哈希和独立解压')]

def ledger():
    with zipfile.ZipFile(ROOT/'archive'/'ROOT_V93_original.zip') as z:
        matches=[name for name in z.namelist() if name.endswith('/ledger/ALL_177_FLAT.csv')]
        if len(matches)!=1:raise RuntimeError('V93 original ledger not found uniquely inside archive')
        raw=z.read(matches[0]).decode('utf-8-sig')
        rows=list(csv.DictReader(io.StringIO(raw)))
    assert len(rows)==177,len(rows)
    new=[dict(id=a,issue=b,status_or_current_result=c,acceptance_criterion=d,source_version='V94') for a,b,c,d in NEW]
    flat=rows+new
    assert len(flat)==205 and len({r['id'] for r in flat})==205
    out=ROOT/'ledger';out.mkdir(exist_ok=True)
    with (out/'ALL_205_ISSUES.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
    (out/'ALL_205_ISSUES.json').write_text(json.dumps(flat,ensure_ascii=False,indent=2))
    with (out/'V94_NEW_28.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(new)
    return {'carried_from_V93':len(rows),'new_V94':len(new),'total':len(flat)}

if __name__=='__main__':
    dim=dimension_results();issues=ledger()
    (ROOT/'results'/'DIMENSION_AND_LEDGER_SUMMARY.json').write_text(json.dumps({'dimensions':dim,'ledger':issues},ensure_ascii=False,indent=2))
    print('dimensions:',dim,'issue ledger:',issues)
