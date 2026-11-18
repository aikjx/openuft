"""Generate reproducible numerical experiments (standard library outputs + optional matplotlib charts)."""
from __future__ import annotations
import csv,json,math,sys,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from planetary import *

DATA=ROOT/'data';RESULTS=ROOT/'results'
DATA.mkdir(exist_ok=True);RESULTS.mkdir(exist_ok=True)

def csv_write(path,headers,rows):
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(rows)

def main():
    bodies=load_bodies();rows=[]
    for b in bodies.values():
        p=surface_stats(b)
        rows.append([b.name,b.key,b.classification, b.mass_kg,b.mean_radius_m,p['mean_density_kg_m3'],
                    p['g_spherical_m_s2'],p['v_escape_m_s'],p['v_circular_m_s'],
                    p['v_equatorial_rotation_m_s'],p['centrifugal_equator_m_s2'],
                    p['compactness_rs_over_R'],b.observed_g_approx,
                    100*(p['g_spherical_m_s2']/b.observed_g_approx-1),b.composition_label])
    csv_write(DATA/'01_tian_ti_dui_bi.csv', ['天体','key','分类','质量kg','平均半径m','平均密度kg_m3',
        '球对称g_m_s2','逃逸速度m_s','近表面圆轨道速度m_s','表面自转线速度m_s','赤道离心加速度m_s2',
        '紧致度2GM_c2R','NASA参考g_m_s2','模型与参考差_pct_仅示意_非同位置','组成定性备注'],rows)

    er=[]
    for lat in range(0,91,5):
        r=earth_surface_field(lat)
        er.append([lat,r['r_m'],r['g_gravity_m_s2'],r['g_effective_m_s2'],
            r['gravity_radial_m_s2'],r['effective_radial_m_s2']])
    csv_write(DATA/'02_diqiu_weidu_J2_zizhuan.csv',['地理纬度_deg','距中心_m','地心万有引力模长_m_s2',
            '地固系有效重力模长_m_s2','径向引力分量_m_s2','径向有效重力分量_m_s2'],er)

    layered=earth_toy_layers();R=layered.radius;dense=[]
    for i in range(201):
        r=R*1.5*i/200
        dense.append([r/1000,r/R,layered.density_at(r),layered.enclosed_mass(r),layered.accel(r),
                     uniform_sphere_accel(layered.mass,layered.radius,r)])
    csv_write(DATA/'03_diqiu_fenceng_neibu_yinli.csv',
             ['半径_km','r_over_R','分层密度_kg_m3','包围质量_kg','分层引力_m_s2','同质量均匀球引力_m_s2'],dense)

    orb=[]
    moon=bodies['Moon'];sun=bodies['Sun']
    for h in [0.,1.,10.,100.,1e3,1e5,4e5,7.10e5,1e6,3.58e7]:
        r=EARTH_R= bodies['Earth'].mean_radius_m+h
        g=bodies['Earth'].mu/r**2
        v=math.sqrt(bodies['Earth'].mu/r)
        tide_sun=norm(tidal_relative_accel(sun.mu,(AU,0.,0.),(1000.,0.,0.)))
        tide_moon=norm(tidal_relative_accel(moon.mu,(384400e3,0.,0.),(1000.,0.,0.)))
        orb.append([h,g,v,g*1/C**2,tide_sun,tide_moon])
    csv_write(DATA/'04_haiba_yunxing_chaoxi.csv',
              ['高度_m','球对称引力加速度_m_s2','圆轨道速度_m_s','高差1米钟频比近似','太阳径向潮汐差_1km_m_s2','月球径向潮汐差_1km_m_s2'],orb)

    sc=[]
    for material in ['Ti','Pt','Fe','O','H','He']:
        sc.append([material,Z_A[material][0],Z_A[material][1],z_over_a(material)])
    csv_write(DATA/'05_element_charge_toy.csv',['元素','质子数Z','原子质量A','模型Z_over_A_不是物理已证荷'],sc)
    # Fifth force scan, test both potentials at a source/test-body separation and a selectable force range.
    yrows=[]
    for k in range(-18,-10):
        alpha=10**k
        for ratio in [.01,.1,1.,10.,100.]:
            lam=ratio*bodies['Earth'].mean_radius_m
            eta=eotvos_yukawa(bodies['Earth'].mean_radius_m,lam,alpha)
            yrows.append([alpha,ratio,eta,7e-15,abs(eta)<7e-15])
    csv_write(DATA/'06_yukawa_zu_cheng_yanzheng.csv',
              ['alpha_假设','lambda_over_RE','模型_Eotvos_Ti_Pt','仅示意_95pct粗界','模型低于粗界'],yrows)

    # Scenario matrix that is important not to mistake for a phenomenological "proof".
    scenarios=[
      ('地球地表不同纬度','已知','椭球 J2 自转','不需要变量G','J2位势梯度与地固系动力学','地面重力与GNSS'),
      ('地球内部密度不同','已知/模型','球壳密度/包围质量','仅外部球对称点不变','积分4πρr²dr','地震、密度重力反演'),
      ('不同半径但同密度','严格数学','g=4πGρR/3','引力不同不代表G不同','缩放R和ρ','天体质量半径'),
      ('不同元素同质量结构','条件数学','常规引力质量能量普适','常规牛顿引力与元素标签无关','固定M和密度形状','MICROSCOPE'),
      ('同地球不同材料自由落体','强约束','对比Ti和Pt','约10^-15水平无显著违背','η双差','MICROSCOPE'),
      ('组成依赖第五力','假设','Yukawa Q_A Q_B','可能违反弱等效原理','η(alpha,lambda)','扭秤/卫星'),
      ('地球自转','已知','离心+J2/扁率','有效重力随纬度变化','旋转坐标非惯性','地固系重力'),
      ('试验台匀速平移','已知','相对位置不变/局部Lorentz变换','无绝对速度项','平移不变量','参考系比较'),
      ('公转导致太阳潮汐','已知','外部天体势的梯度差','相对运动/轨道几何影响测量','潮汐张量','潮汐/卫星'),
      ('地球旋转框架拖曳','已知弱场GR','旋转源角动量J','与地球自转有关但非变量G','Lense–Thirring近似','陀螺/测地卫星'),
      ('微观原子实验放在地球上','已知','势差红移/潮汐/实验系统误差','局部引力通常已计入或可忽略','gΔh/c²','光钟与原子实验'),
      ('自由落体卫星实验','已知','轨道g不为零，支持重力自由落体','微重力不等于无引力','g(h)与加速度计','MICROSCOPE'),
      ('强磁场贡献引力','已知GR','EM能动张量引力源','量级通常极小','u_B=B²/(2μ0)','场源应力'),
      ('太阳等离子体压强','已知GR+恒星结构','压强/能密度/温度影响结构','不能仅靠平均密度','Tμν + EOS','恒星结构模型'),
      ('超强场黑洞','已知+未解决','需完整GR/量子理论','牛顿与J2不适用','史瓦西/Kerr几何','引力波/黑洞阴影'),
      ('星系整体空间运动','已知变换','相对运动与测地线','不存在已证实的绝对空间风','协变变换','多参考系数据'),
      ('宇宙空间膨胀','已知宇宙学','FLRW度规与Hubble扩张','不等于局域光速螺旋介质流动','爱因斯坦-弗里德曼方程','宇宙学观测'),
      ('微观螺旋速度c','ROOT假说','有质量粒子整体世界线不可以c','内部模态需要洛伦兹协变动力学','场变量/无负范数','微观散射'),
      ('螺旋三方向对应三力','已被反例推翻普遍性','电荷反号导致力反向','几何分量不能替代荷','qE 与- qE','电磁'),
      ('从不同星体反推G','不可辨识','多数天体质量由GM推算','不能证明G变化或独立G来源','G→kG,M→M/k','独立惯性质量'),
      ('诱导引力产生G','依赖假设','热核截止/场谱/裸项退化','不能独立得到常数','1/G_ind(N,xi,ell)','有效场论'),
      ('三规范群来自空间角度','未证明','颜色/手征/规范结构缺失','SU3×SU2×U1须独立导出','异常抵消/RGE','粒子物理'),
      ('不同星体上的精密光钟','预期效应','引力势差+运动学红移','须按同一时间参考进行比较','dτ/dt弱场','光钟/导航'),
      ('元素影响密度与半径','已知','状态方程/凝聚态/核反应','间接而不是新基本力','EOS与能量守恒','高压物态'),
      ('极端密度压力影响光传播','已知GR','度规与曲率','有限近似需量化','null测地线','透镜/时间延迟'),
      ('星体非球形局部异常','已知','高阶球谐或局部质量','均值模型不可代替测量','EGM2008/空间测量','卫星重力'),
      ('星体磁场场线变化','已知','Maxwell/磁流体动力学','磁场不是新的引力常数','IGRF14/其他星体模型','磁力仪'),
      ('四力联合作用量','已知加候选','GR+SM+新增场','直接相加不是统一起源','协变/异常/重整化','粒子实验'),
      ('地球的自转能量','已知GR','能量和动量影响Tμν','并非简单G(ω)','相对论应力张量','框架拖曳'),
      ('暗物质与暗能量','开放','需独立场/宇宙学模型','不可预设螺旋解释','Lagrangian+观测','CMB/星系旋转'),
    ]
    csv_write(DATA/'07_quan_chang_jing_shen_cha.csv',
              ['情况','证明状态','物理变量','关键纠错','方程或算法','需要的观测'],scenarios)

    micro_alt=710e3;micro_g=bodies['Earth'].mu/(bodies['Earth'].mean_radius_m+micro_alt)**2
    moon_tide_km=norm(tidal_relative_accel(moon.mu,(384400e3,0,0),(1000.,0,0)))
    sun_tide_km=norm(tidal_relative_accel(sun.mu,(AU,0,0),(1000.,0,0)))
    # Real numerical orbit integration to quantify the role of trajectory, not "absolute space motion".
    r0=bodies['Earth'].mean_radius_m+400e3;mu=bodies['Earth'].mu
    v0=math.sqrt(mu/r0);T=2*math.pi*math.sqrt(r0**3/mu)
    pos=(r0,0.,0.);vel=(0.,v0,0.);E0=orbital_energy_per_mass(pos,vel,mu)
    orbit=[];maxE=0.;maxR=0.
    N=2400;step=T/N
    for j in range(N+1):
        e=orbital_energy_per_mass(pos,vel,mu)
        maxE=max(maxE,abs(e/E0-1));maxR=max(maxR,abs(norm(pos)/r0-1))
        if j%12==0:orbit.append([j*step,*pos,*vel,e/E0])
        if j<N:pos,vel=kepler_verlet_step(pos,vel,mu,step)
    csv_write(DATA/'08_earth_400km_symplectic_orbit.csv',
              ['time_s','x_m','y_m','z_m','vx_m_s','vy_m_s','vz_m_s','specific_energy_over_initial'],orbit)
    orbit_summary={'altitude_m':400e3,'period_s':T,'circular_speed_m_s':v0,
                   'integrator':'velocity Verlet, Newtonian central two-body (not ephemeris)',
                   'steps':N,'max_abs_relative_energy_error':maxE,'max_rel_radial_drift':maxR,
                   'closing_position_error_fraction':norm(sub(pos,(r0,0,0)))/r0}
    summary={
        'version':'ROOT V69',
        'scientific_status':'NO independent G prediction; NO four-force unification proof; conditional astrophysical models only',
        'source_data':'NASA NSSDC, JPL, IERS, MICROSCOPE publication; see sources/',
        'earth_g_equator_effective':earth_surface_field(0)['g_effective_m_s2'],
        'earth_g_pole_effective':earth_surface_field(90)['g_effective_m_s2'],
        'earth_g_lat45_effective':earth_surface_field(45)['g_effective_m_s2'],
        'microscope_orbit_height_m':micro_alt,
        'earth_g_at_710km_m_s2':micro_g,
        'microscope_freefall_proper_accel_ideal_m_s2':0.,
        'microscope_note':'orbit remains strongly gravitational; satellite drag-free follows geodesic. g!=accelerometer proper acceleration.',
        'earth_layered_mass_kg':layered.mass,
        'earth_layered_central_pressure_toy_Pa':layered.hydrostatic_pressure(),
        'earth_mean_density':bodies['Earth'].density,
        'earth_spherical_surface_g':surface_stats(bodies['Earth'])['g_spherical_m_s2'],
        'Ti_ZA':z_over_a('Ti'),'Pt_ZA':z_over_a('Pt'),
        'microscope_eta_combined_1sigma':math.sqrt(2.3**2+1.5**2)*1e-15,
        'toy_eta_95_upper_approx':7e-15,
        'toy_alpha_bound_long_range_approx':alpha_bound_toy(7e-15),
        'toy_bound_disclaimer':'ignores actual Ti/Pt alloy details, Earth composition charge, instrument parameter covariances, finite range and analysis systematics; NOT published bound',
        'atomic_electron_potential_diff_1m_eV':gravitational_energy_eV(9.1093837139e-31,1),
        'atomic_electron_potential_diff_Bohr_eV':gravitational_energy_eV(9.1093837139e-31,5.29177210903e-11),
        'clock_fraction_1m':gravitational_redshift_fraction(9.81,1),
        'earth_weak_frame_dragging_equator_rad_s':norm(lense_thirring_precession(bodies['Earth'],(bodies['Earth'].mean_radius_m,0,0))),
        'solar_tide_relative_1km_m_s2':sun_tide_km,
        'moon_tide_relative_1km_m_s2':moon_tide_km,
        'Earth_B_energy_density_example_T_60uT_Jm3':source_energy_density_from_field(B=60e-6),
        'GM_scaling_symmetry':'G->kG,M->M/k leaves Newtonian orbital GM invariant',
        'scenario_count':len(scenarios),'body_count':len(bodies), 'orbit_integration_400km':orbit_summary,
    }
    (RESULTS/'numerical_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')

    # Additional plots are OPTIONAL dependency; CSV always generated
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.ticker import ScalarFormatter
        plt.figure(figsize=(10,5));keys=[b.key for b in bodies.values()]
        values=[surface_stats(b)['g_spherical_m_s2'] for b in bodies.values()]
        plt.bar(keys,values);plt.yscale('log');plt.ylabel('Monopole g at mean radius (m/s²)')
        plt.title('Planetary gravities; rounded NASA/JPL input')
        plt.xticks(rotation=30);plt.tight_layout();plt.savefig(RESULTS/'planetary_gravities.png',dpi=145);plt.close()

        plt.figure(figsize=(10,5))
        plt.plot([r[0] for r in dense],[r[4] for r in dense],label='Layered, spherical toy')
        plt.plot([r[0] for r in dense],[r[5] for r in dense],label='Uniform density, same total mass')
        plt.axvline(R/1000,linestyle='--',alpha=.5,label='Nominal surface')
        plt.xlabel('Radius from center (km)');plt.ylabel('g(r), m/s²')
        plt.legend();plt.title('Inside Earth: identical external g, different interior g');plt.tight_layout()
        plt.savefig(RESULTS/'earth_interior_gravity.png',dpi=145);plt.close()

        plt.figure(figsize=(10,5))
        plt.plot([r[0] for r in er],[r[2] for r in er],label='Earth gravity (J2)')
        plt.plot([r[0] for r in er],[r[3] for r in er],label='Earth effective gravity (rotation)')
        plt.xlabel('Geodetic latitude (deg)');plt.ylabel('Acceleration m/s²')
        plt.title('Earth J2 + ellipsoid + centrifugal, approximate');plt.legend();plt.tight_layout()
        plt.savefig(RESULTS/'earth_latitude_g.png',dpi=145);plt.close()

        plt.figure(figsize=(7,7))
        plt.plot([x[1]/1000 for x in orbit],[x[2]/1000 for x in orbit],lw=1.8)
        plt.gca().set_aspect('equal','box');plt.title('400 km circular orbit, velocity Verlet')
        plt.xlabel('x (km)');plt.ylabel('y (km)');plt.tight_layout();plt.savefig(RESULTS/'earth_orbit_integration.png',dpi=145);plt.close()

        plt.figure(figsize=(10,5))
        for ratio in [.1,1.,10.,100.]:
            xs=[r[0] for r in yrows if r[1]==ratio]
            ys=[abs(r[2]) for r in yrows if r[1]==ratio]
            plt.loglog(xs,ys,label=f'lambda/R={ratio:g}')
        plt.axhline(7e-15,color='gray',linestyle='--',label='illustrative coarse bound; NOT fit')
        plt.xlabel('alpha (hypothetical)');plt.ylabel('|Eotvos Ti-Pt| toy')
        plt.title('Composition-dependent Yukawa model — illustrative ONLY')
        plt.legend();plt.tight_layout();plt.savefig(RESULTS/'composition_ep_toy.png',dpi=145);plt.close()
    except ImportError:
        summary['charts']='not generated; matplotlib not installed'
        (RESULTS/'numerical_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
