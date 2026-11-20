#!/usr/bin/env python3
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
d=root/'spec';d.mkdir(exist_ok=True)
stages=['DEFINE','DIMENSION','BASELINE','CALIBRATE','RANDOMIZE','BLIND','ACQUIRE','VETO','INFER','REPLICATE','RELEASE']
common={'schema':'ROOT-GCL/2.0','physics_state':'TEST PROPOSAL, NOT VALIDATED IN REAL HARDWARE','units':'SI',
 'data_label':'SYNTHETIC until signed hardware evidence is provided','stages':stages,
 'controls':['source movement','sham movement','sensor reversal','temperature','tilt','stray magnetic field','cable force','mass/geometry metrology'],
 'error_model':{'correlated_noise':'covariance required','long_term_drift':'measure with interleaved null','multiple_trials':'pre-register'},
 'decision_rules':['do not interpret p alone as physical discovery','require independent physics sensor and blinded hardware replication',
  'no fifth-force claim from J2-only Q deviation','no G prediction from Z=Gc/2']}
experiments=[
 ('01_multidistance_mass','移动源质量—多距离双传感器','Newton+J2+systematics, then pre-registered Yukawa',
  {'source_mass_kg':100,'source_radius_m':.04,'distances_m':[.15,.19,.24,.30,.39,.51,.65,.84,1.08,1.38,1.8],
   'source_motion':'A/B/sham randomized','detector':'double gradiometer OR torsion balance'},
  ['source position m','gravitational signal m/s2','tilt rad','temperature K','B field T','time ISO8601']),
 ('02_composition_factorization','同质量不同组成的源荷判别','one separable mediator, exact eta forward model',
  {'source_compositions':'blind A,B,C','test_pairs':'at least 3 independent material pairs',
   'same_mass_and_outer_geometry':True,'mass_metrology':'independent of tested gravity amplitude'},
  ['source code blind','test material pair code','eta dimensionless','covariance index','force baseline']),
 ('03_angular_j2_control','多方位多高度排除已知非球形假阳性','Newton J2/J4+multipoles vs spherical Yukawa',
  {'latitude_or_colatitude':'multiple','radii':'at least 3','model_angle_convention':'colatitude theta to spin axis',
   'centrifugal_effect':'must model separately'},
  ['r m','theta rad','radial g m/s2','angular g m/s2','J2/J4 fitted','source orientation']),
 ('04_electromagnetic_null','电磁储能变化与真实引力零实验','Einstein-Maxwell vs hypothesized extra coupling',
  {'magnetic_field_T':'safe, hardware-limited','EM_state':'off/on/reversed/sham','total_system_energy':'tracked',
   'shielding':'independent mechanical and EM readouts'},
  ['B vector T','E vector V/m','device electrical power W','strain','vibration','gravitational channel']),
]
for file,title,hyp,inputs,cols in experiments:
    doc={'id':'ROOT-V86-'+file,'title':title,'hypothesis':hyp,'design':inputs,
         'required_raw_columns':cols,'safety':{'high_field':'requires risk approval','moving_mass':'mechanical stop and lockout',
          'human_review':'mandatory before physical instrument operation'},**common}
    (d/f'{file}.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding='utf8')
(d/'schema_notes.md').write_text('''# ROOT-GCL/2.0 实验语言说明\n\n4 份协议是科研实验设计草案，不是连接真实设备的控制脚本。所有行为由设备工程师另行验收；不可自动驱动危险高场/重物。\n\n**状态机** DEFINE→DIMENSION→BASELINE→CALIBRATE→RANDOMIZE→BLIND→ACQUIRE→VETO→INFER→REPLICATE→RELEASE。\n\n`required_raw_columns` 是必需元数据字段示例；严格机器约束还应由实验室专属 JSON Schema、仪器驱动、时间同步及质量控制方案实现。本包对协议基本结构做自动校验，不能认证仪器可靠性。\n''',encoding='utf8')
print('Built',len(experiments),'protocols')
