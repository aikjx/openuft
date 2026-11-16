# -*- coding: utf-8 -*-
"""独立复算：外星文明科技公式合集 + em_field_energy_3d.html
所有数值用 Decimal 高精度，不复用文档登记值作为输入（除明确标注的来料常数）。"""
from decimal import Decimal as D, getcontext
import json
getcontext().prec = 50

def q(x): return D(str(x))

R = {}
def rec(key, doc, calc, unit, note):
    try:
        dev = (D(str(calc)) - D(str(doc))) / abs(D(str(doc))) if D(str(doc)) != 0 else None
    except Exception:
        dev = None
    R[key] = dict(doc=doc, calc=str(calc), unit=unit,
                  rel_dev=str(dev) if dev is not None else None, note=note)

# ---------- 0. 基本常数（SI 2019 定义值，来自 HTML 源码） ----------
EPS0 = q('8.8541878128e-12')
MU0  = q('1.25663706212e-6')
C0   = q('299792458')
# 校验 c = 1/sqrt(eps0*mu0)
c_from_const = (D(1)/(EPS0*MU0)).sqrt()
rec('c_check', 299792458, c_from_const, 'm/s', '由 eps0、mu0 反推光速，验证常数自洽')
# 常数乘积恒等式 eps0*mu0*c^2 = 1
R['eps0_mu0_c2'] = str(EPS0*MU0*C0*C0)

# ---------- 1. HTML 真空平面波能量密度 ----------
E0 = q('1e6')                 # V/m
B0 = E0/C0                    # 真空平面波 B0 = E0/c
ue = D('0.5')*EPS0*E0*E0      # 电场能量密度
ub = D('0.5')*B0*B0/MU0       # 磁场能量密度
u_tot = ue+ub
rec('HTML_vB0_mT', '3.34', B0*q(1000), 'mT', 'B0=E0/c')
rec('HTML_UE', '4.43', ue, 'J/m^3', '0.5 eps0 E0^2')
rec('HTML_UB', '4.43', ub, 'J/m^3', '0.5 B0^2/mu0')
rec('HTML_U_total', '8.85', u_tot, 'J/m^3', 'UE+UB')
# 恒等式 UE==UB ?  (解析：0.5 eps0 E^2 与 0.5 (E/c)^2/mu0 = 0.5 E^2 eps0，恒等)
R['HTML_UE_eq_UB_rel_dev'] = str(abs(ue-ub)/ue)
# 解析恒等：ub/ue = 1/(eps0*mu0*c^2)。常数表值使 eps0*mu0*c^2=0.99999999999996（SI2019 独立测量值）
# 用物理容差 1e-9 判定为恒等式
R['HTML_UE_eq_UB_identity'] = (abs(ue-ub)/ue < q('1e-9'))

# ---------- 2. 文档：“电磁场能量转化实质能量”实验 ----------
Edoc = q('1e4')      # V/m
f = q('1e6')         # Hz
A = q('1')           # m^2
eta = q('0.9')
u_doc = D('0.5')*q('8.854e-12')*Edoc*Edoc
rec('doc_u_Jm3', '4.427e-4', u_doc, 'J/m^3', '用文档登记 eps0=8.854e-12')
Pin = u_doc*A*f
rec('doc_Pin_W', '442.7', Pin, 'W(量纲存疑)', 'u*A*f；量纲为 J/m，见报告')
Pout = eta*Pin
rec('doc_Pout_W', '398.43', Pout, 'W', 'eta*Pin')
# 效率 90% 与 eta 相符 —— 是否同义反复
R['doc_efficiency_tautology'] = str(Pout/Pin)

# ---------- 3. dB/dt 公式代数核验 ----------
# 文档：dB/dt = dV/dt*E/c^2 + V*(dE/dt)/c^2
# 文档“解得”：dB/dt = 0.5*(dV/dt + V*(dE/dt)/E)*E/c^2
# 展开后式 = 0.5*dV/dt*E/c^2 + 0.5*V*dE/dt/c^2 = 原式的一半
# 取符号变量 a=dV/dt, b=dE/dt, V,E,c^2 均符号：比较系数
# 原式系数 (1,1)，解得式系数 (0.5,0.5) => 相差 1/2
R['dBdt_algebra'] = dict(orig_coeff=[1,1], solved_coeff=['0.5','0.5'],
                         ratio='0.5', verdict='解得式 = 原式/2，除非原式为0，否则不成立')

# ---------- 4. 全息干涉公式 I=|O+R|^2 ----------
# 恒等式展开 I = |O|^2+|R|^2+2Re(O R*)
R['holography_identity'] = 'I=|O+R|^2 = |O|^2+|R|^2+2Re(O R*) — 标准全息干涉，恒等式展开正确'

# ---------- 5. 能量融合 E_total = a*E_EM+(1-a)*E_strong ----------
R['energy_fusion'] = '线性插值定义；alpha∈[0,1] 为自由参数，无新方程，属定义式'

# ---------- 6. 金字塔几何（太阳神翼）----------
# 底边 527m，高 336m，倾角 51°50'，占地 277729 m^2，体积 3110万 m^3
base=527; height=336
area = base*base
rec('pyramid_area_m2', 277729, area, 'm^2', '底面正方形')
# 体积 = 1/3 * 底面积 * 高
vol = D(1)/D(3)*D(area)*D(height)
rec('pyramid_volume_m3', 3.11e7, vol, 'm^3', 'V=1/3*S*h')
# 侧面倾角（面与底面夹角）：tan(theta)=h/(base/2)
import math
theta = math.degrees(math.atan(height/(base/2)))
# 转成度分
deg=int(theta); minute=(theta-deg)*60
rec('pyramid_incline_deg', 51+50/60, theta, 'deg', 'tan theta = h/(a/2)')

# ---------- 7. 仙烟成分求和 ----------
comp = [q('0.01'), q('0.02'), q('0.0045'), q('0.005'), q('0.003'), q('0.0001'), q('0.001')]
ctot = sum(comp)
rec('cigarette_Ctotal_g', '0.0436', ctot, 'g', '7 项相加')

# ---------- 8. 抗癌仙烟效果公式 ----------
rec('anti_cancer_health', '0.36', q('0.8')*q('0.30')+q('0.6')*q('0.20'), '无量纲', '加权和')
rec('anti_cancer_air', '0.09', q('0.9')*q('0.10'), '无量纲', '')
rec('anti_cancer_disease', '0.21', q('0.5')*q('0.30')+q('0.3')*q('0.20'), '无量纲', '')
rec('anti_cancer_effect', '0.009%', q('0.0001')*q('0.90')*100, '%', '0.01%*90%')

# ---------- 9. 核裂变质量亏损 ----------
u_kg = q('1.66053906660e-27')
dm = q('0.2')*u_kg
rec('fission_dm_kg', '3.3210781332e-28', dm, 'kg', '0.2 u')
dE = dm*C0*C0
rec('fission_dE_J_c_exact', '2.98897031988e-11', dE, 'J', '用精确 c')
# 文档用 c≈3e8
dE_approx = dm*q('3e8')*q('3e8')
rec('fission_dE_J_doc_c', '2.98897031988e-11', dE_approx, 'J', '文档用 c=3e8')
# 换算 MeV
MeV = q('1.602176634e-13')
rec('fission_MeV', '200', dE/MeV, 'MeV', '0.2u 裂变能')
# 1 u = 931.494 MeV 校验
R['u_to_MeV'] = str(q('0.2')*q('931.49410242'))

# ---------- 10. 等离子体加速 v=sqrt(2qEd/m), E=qEd ----------
# 代数恒等：代入 v^2=2qEd/m 到 0.5 m v^2 => qEd
R['plasma_identity'] = '0.5*m*(2*q*E*d/m) = q*E*d — 代入后恒等，非新结论'

# ---------- 11. 核聚变 D-T 与 Li-6 ----------
rec('DT_Q_MeV', '17.6', q('3.5')+q('14.1'), 'MeV', '3.5+14.1')
rec('Li6_Q_MeV', '4.8', q('2.05')+q('2.75'), 'MeV', '2.05+2.75')
# 1 克 D-T 燃料能量估算 + 与石油当量比较
# 1 mol D-T (2.014+3.016=5.03 g) 含 Na 个反应，每反应 17.6 MeV
NA = q('6.02214076e23')
m_mol = q('5.03')  # g per mole of D-T pairs
per_gram_J = NA/m_mol*(q('17.6')*MeV)
R['DT_1g_J'] = str(per_gram_J)
# 1 吨石油 ≈ 4.1868e10 J (1 toe)
toe = q('4.1868e10')
tons_oil_per_g = per_gram_J/toe
R['DT_1g_tons_oil'] = str(tons_oil_per_g)
rec('DT_oil_claim', '8e4', tons_oil_per_g, '万吨石油/克', '文档称 8 万吨石油当量/克')

# ---------- 12. 氚增殖 / Q 值等 —— 目标值非实测 ----------
R['fusion_targets'] = 'Q>=5/10, Btor>=25T, tau_E>=1000s, dpa<=200 等均为工程目标/阈值，非实验测量结果'

# ---------- 13. 无线输电延迟 ----------
# GEO 到地表 ~3.6万公里，光速传播最短延迟
d_geo = q('3.6e7')  # m
t_light = d_geo/C0*1000  # ms
R['geo_light_delay_ms'] = str(t_light)
rec('wireless_delay_claim_ms', '1', t_light, 'ms', '3.6万公里光速单程下限')

# ---------- 14. 反物质 1 克湮灭 ----------
E_ann = q('0.002')*C0*C0  # 1g 反物质+1g 物质 = 2g
R['antimatter_1g_pair_J'] = str(E_ann)
# 1 GW 核电站年发电
E_nuc_yr = q('1e9')*(q('365.25')*q('24')*q('3600'))
R['nuclear_1GW_year_J'] = str(E_nuc_yr)
R['antimatter_equiv_years_1GW'] = str(E_ann/E_nuc_yr)
rec('antimatter_claim_years', '40', E_ann/E_nuc_yr, '年(1GW电站)', '文档称 1 克反物质≈核电站40年')

# ---------- 15. 强核力能量密度核对 ----------
R['strong_energy_density_claim'] = '10^15 J/cm^3 = 10^21 J/m^3；无一手出处，且与 QCD 标度自洽性未证'

# ---------- 16. 引力场/反重力公式量纲备注 ----------
R['gravity_formulas_dimension'] = {
 'eta_MG': 'tanh(dPhi_grav/Phi0)：引力势差/磁通量子，量纲不一致',
 'rho_grav': 'hbar*c/Lp^3 的量纲 = J/m^2，非能量密度 J/m^3（应为 Lp^4）',
 'F_GW': 'c^4/(16 pi G)*d(h^2)/dt 量纲 = N/s，非力 N',
 'g_eff': 'curl(B x v/c) 量纲 = T/m，与 m/s^2 不可相加',
 'rho_GEB': '(1+4GM rho_EM/c^4) 括号内量纲非 1，不可与 1 相加',
}

# ---------- 17. 无人机/飞船速度 claim ----------
rec('craft_speed_kms', '30000', q('30000'), 'km/s', '二代飞碟 3 万公里/秒 ≈ 0.1c（数量级核对）')
R['speed_fraction_c'] = str(q('30000')*1000/C0)

print(json.dumps(R, ensure_ascii=False, indent=2))
with open('C:/Users/mo/AppData/Local/Temp/ufo-audit-pdf/recompute.json','w',encoding='utf-8') as fh:
    json.dump(R, fh, ensure_ascii=False, indent=2)
