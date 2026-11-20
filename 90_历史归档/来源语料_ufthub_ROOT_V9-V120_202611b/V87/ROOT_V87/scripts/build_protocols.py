from pathlib import Path
import csv,json
root=Path(__file__).resolve().parent.parent
mat=[]
def add(k,topic,procedure,control,pass_condition,status,limitation):mat.append([len(mat)+1,k,topic,procedure,control,pass_condition,status,limitation])
add('theory','GR action variation','derive Einstein equations','boundary and stress tensor conventions','coefficient 8πG/c⁴','E','G not predicted')
add('theory','Newton limit','expand full metric to first order','include spatial h_ij','Poisson 4πGρ','C','weak static pressureless')
add('theory','geodesic reduction','derive Gamma^i_00','coordinate x0=ct','Newton -grad Φ','C','nonrel weak')
add('theory','Klein Gordon to Schr','factor out exp(-imc²t/hbar)','keep ∂tt and estimate its size','Schr when ∂tt negligible','C','spin zero')
add('theory','Dirac curved spacetime','form tetrad and spin connection','spin degrees and spin-curvature','correct nonrel Pauli limit','C','not fully calculated here')
add('theory','uniform gravity transformation','direct symbolic wave substitution','test arbitrary free plane wave','exact residual zero','E','no tidal')
add('theory','invariant observable','phase vs g and redshift','hold branches stationary','same DeltaPhi in leading order','C','control laser/trap')
add('theory','G M identifiability','derivatives wrt G M','no independent M','Jacobian determinant zero','E','new scale can lift')
add('theory','Schwarzschild redshift','use exact static formula','outside horizon','weak limit matches DeltaPhi/c²','E','no free-fall observer comparison')
add('theory','Schwarzschild curvature','compute K','vacuum exterior','r^-6 scaling','E','not Kerr')
add('theory','Schr Newton gaussian','Poisson Gaussian potential','self-energy factor 1/2','normalization, virial, extremum','C','not a fundamental particle prediction')
add('theory','quantum EFT','measure epsilon_Q','check low-energy regime','epsilon_Q << 1','C','no UV proof')
add('theory','Wheeler DeWitt canonical','constraint algebra and physical Hilbert space','clock problem, anomalies','consistent continuum and measurements','O','not solved here')
add('theory','loop quantum gravity','spin-network semiclassical limit','Lorentz, dynamics, matter','GR+QFT predictions','O','not solved here')
add('theory','string gravity','worldsheet / effective action','compactification and spectra','predict known particle constants','O','not solved here')
add('theory','asymptotic safety','nonperturbative RG fixed point','regulator truncation and spectra','robust UV limit','O','not solved here')
add('theory','holography','quantum boundary and emergent geometry','match actual 4D and SM','unique experimental prediction','O','not solved here')
add('theory','stochastic gravity','noise kernel stress correlations','conservation, renormalization','consistent low-energy fluctuation estimate','C','not full quantum gravity')
add('theory','induced/emergent gravity','integrate quantum matter loops','cutoff independent predictability','recover correct G without fitted scale','H','open mechanism')
add('experiment','atom/neutron quantum phase','source mass on/off randomized','laser phase and vibration','observed differential phase agrees with pre-registered null','E/C','no experiment run in ZIP')
add('experiment','classical gravity source mass','move independently weighed mass','real geometry, mass calibration','g predicted to uncertainties','E/C','hardware not connected')
add('experiment','quantum/clock triangle','compare DeltaPhi from three modalities','Doppler, special redshift, electromagnetic','joint residual consistent','C','small clock signal')
add('experiment','finite-size source correction','integrate actual mass distribution','sensor/source geometry measured','matches independent quadrature','C','point source only demonstration')
add('experiment','randomization and sham','blind code source/sham actuation','operator blindness','difference follows source mass not actuator','C','synthetic only')
add('experiment','source geometry scaling','multiple source distances','J2/gradient/multipole model','fits predicted geometry','C','SNR may be low')
add('experiment','composition Eötvös','different species in same gravity','independent WEP controls','limits within MICROSCOPE','E','specific scenario not all G theories')
add('experiment','gravitational quantum entanglement','two body branches, nonlocal invariant χ','EM/casimir/environment excluded','state witness and locality audit','H','not definitive without model assumptions')
add('experiment','decoherence test','coherence contrast across time','thermal, collision, magnetic','residual after known channels excluded','H','no hardware')
add('experiment','quantum-clock relativistic correction','height arrays and exact redshift','proper time / GR vs Newton','PN correction resolved within uncertainty','C','lab precision constraints')
add('experiment','G measurement independence','gravimeter and mass balance','do not infer M using same G','full rank independent calibration','C','GM degeneracy remains if no new input')
add('statistics','correlated noise GLS','fit with measured covariance','drift and common-mode','calibrated coverage','C','requires real noise data')
add('statistics','blind pre-registration','freeze cuts and signals','random seeds and sham controls','no after-the-fact tuning','C','plan only')
add('statistics','model falsifiability','predict distinct signal for competing theories','finite range and source composition','pre-defined likelihood and power','C','no experimental limits computed')
add('engineering','units and numerical precision','SI and dimensional asserts','expm1/log1p clock redshift','stable small shifts','E','double precision still finite')
add('engineering','source mass safety','enclosed motion and rated supports','moving mass limit switches','safe-state and E-stop','C','no device driver')
add('engineering','laser/magnetic safety','non-ionizing laser/em fields','independent review and lockouts','no hazard in simulation','C','physical hardware safety not certified')
add('engineering','data provenance','tag THEORY vs SYNTHETIC vs OBSERVED','prohibit faux observed labels','every file unambiguous','E','only synthetic here')
add('engineering','version and hash integrity','manifest, zip audit','independent extract/test','all files hashed','E','tests finite scope')
add('engineering','independent replication','new team, sensors, code','blind raw data sharing','same result within uncertainty','O','not achieved yet')

with (root/'data'/'method_matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['id','domain','task','method','control','success_condition','status','limitation']);w.writerows(mat)

protocols={
 'quantum_phase_bridge':{
  'id':'ROOT-GCL3-QP-001','title':'量子相位—牛顿势差验证','type':'theory_and_synthetic_protocol',
  'observation_performed':False,'hypothesis':'Held-branch phase difference = -m ΔΦ T/ħ under stated approximations',
  'units':{'M':'kg','R':'m','h':'m','T':'s','phase':'rad','g':'m/s²'},
  'parameters':{'M_kg':100.,'R_m':.30,'h_m':.01,'T_s':1.,'particle_mass_kg':1.44316060e-25},
  'controls':['weigh source independently','sham actuator','laser and trap phase','repeat at multiple distances','finite-size density map','switch blind','recalibrate clock and vibrations'],
  'pass_if':'Observed residual after all registered corrections within joint uncertainty, using independent raw data',
  'no_claims':['no quantum gravity proof','no new G derivation','simulation not observed']},
 'gravity_phase_clock_triangle':{
  'id':'ROOT-GCL3-TRI-002','title':'经典加速度—量子相位—相对论钟差三角一致性','type':'conceptual_measured_future',
  'observation_performed':False,'hypothesis':'DeltaPhi from each modality agrees at shared order with known relativistic corrections',
  'units':{'acceleration':'m/s²','phase':'rad','frequency_ratio':'dimensionless','potential_difference':'m²/s²'},
  'parameters':{'M_kg':5.9722e24,'r_lower_m':6.371e6,'r_upper_m':6.371e6+1.0},
  'controls':['static clock GR expression','independent geodesy and geometry','source movement external','Doppler and tidal corrections','magnetic and temperature independence'],
  'pass_if':'Joint phase-acceleration-clock residual does not exceed theory+measurement covariance',
  'no_claims':['does not break GM degeneracy','no novel gravity observed here']},
 'schrodinger_newton_toy':{
  'id':'ROOT-GCL3-SN-003','title':'高斯波包半经典模型的数学一致性审计','type':'theory_only',
  'observation_performed':False,'hypothesis':'Gaussian variational energy follows kinetic plus half-counted Newton self-energy',
  'units':{'mass':'kg','gaussian_width':'m','energy':'J'},
  'parameters':{'mass_kg':1e-16},
  'controls':['mass normalization','Poisson gradient','independent dimensionless quadrature','energy minimization','quantum linearity limitations'],
  'pass_if':'Numerical and analytic normalized integrals and extremum agree',
  'no_claims':['not a confirmed single-particle nonlinear equation','not electron radius']},
 'bipartite_quantum_mediator':{
  'id':'ROOT-GCL3-ENT-004','title':'双量子源的相互作用相位与媒介识别','type':'hypothesis_protocol',
  'observation_performed':False,'hypothesis':'Four-path interaction can produce χ=θ00+θ11−θ01−θ10 in a coherent two-body model',
  'units':{'m1':'kg','m2':'kg','distance':'m','time':'s','chi':'rad'},
  'parameters':{'m1_kg':1e-12,'m2_kg':1e-12,'T_s':1.0},
  'controls':['electrostatic/Casimir forces','magnetic impurities','locality assumptions','matter-field loops','environment entanglement','phase unwrapping'],
  'pass_if':'Independent quantum-state witness with calibrated assumptions and no alternative interactions',
  'no_claims':['gravity quantization not unambiguous absent assumptions','no entanglement observed in this project']}}
for name,obj in protocols.items():
 (root/'protocols'/f'{name}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
print('methods',len(mat),'protocols',len(protocols))
