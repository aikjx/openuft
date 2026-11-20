from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
E=[]
def add(topic,eq,status,scope,reason):E.append((f'V88-{len(E)+1:03}',topic,eq,status,scope,reason))
add('GR','G_μν+Λg_μν=8πG T_μν/c^4','E','Einstein gravity','coupling G is an input')
add('weak-field','g_00=-(1+2Φ/c²)+O(Φ²)','E','slow static weak field','gauge/coordinate convention specified')
add('weak-field','∇²Φ=4πGρ','E','slow weak field','00 Einstein limit')
add('Newton','Φ(r)=-GM/r','E','external spherical source','Newton solution')
add('Newton','U_12=-Gm1m2/r','E','weak gravity point masses','static interaction')
add('proper time','S=-mc²∫dτ','E','relativistic point particle','proper time action')
add('proper time','dτ/dt≈1+Φ/c²−v²/(2c²)','E','static weak field low v','leading expansion')
add('proper time','L≈−mc²+mv²/2−mΦ','E','leading nonrel limit','action expansion')
add('quantum bridge','H=mc²+p²/(2m)+mΦ','E','weak field low speed','Legendre transform')
add('quantum bridge','iħ∂tψ=[−ħ²∇²/(2m)+mΦ]ψ','E','scalar spinless, prescribed gravity','quantization of test matter, not spacetime')
add('two masses','|ψ0⟩=(|0⟩+|1⟩)_A(|0⟩+|1⟩)_B/2','E','assumed preparation','separable equal superpositions')
add('geometry','x_A(0/1)=∓s1/2','E','static branch coordinates','definition')
add('geometry','x_B(0/1)=d∓s2/2','E','static branch coordinates','definition')
add('geometry','r_ij=x_B(j)-x_A(i)>0','E','d>(s1+s2)/2','positive point-source separations')
add('two masses','H_int|ij⟩=−Gm1m2/r_ij |ij⟩','C','frozen path Newton Hamiltonian','not full quantum gravity dynamics')
add('phase','θ_ij=Gm1m2 t/(ħ r_ij)','E','frozen path','unitary branch phase')
add('phase','θ_ij=(Gm1m2/ħ)∫dt/r_ij(t)','C','prescribed moving paths','must include kinetic/control terms')
add('phase','|ψ(t)⟩=Σ_ij e^(iθij)|ij⟩/2','E','equal initial paths','four-amplitude state')
add('phase','Δ=θ00−θ01−θ10+θ11','E','two-basis branch','local phase invariant')
add('phase','Δ→Δ under θij→θij+ai+bj','E','local diagonal Z rotations','gauge cancellation')
add('phase','Δ=(Gm1m2t/ħ)[1/r00−1/r01−1/r10+1/r11]','E','Newton two-body model','exact for frozen paths')
add('phase','Δ_symmetric=(Gm²t/ħ)[2/d−1/(d+s)−1/(d−s)]','E','equal masses and equal branch splits','analytic simplification')
add('phase','Δ_symmetric=−2Gm²t s²/[ħd(d²−s²)]','E','same as above','algebraic identity')
add('phase','Δ≈−2Gm1m2t s1s2/(ħd³)','E','s1,s2 << d','Taylor leading term')
add('entanglement','C=2|det(A_ij)|','E','pure two-qubit state','pure concurrence formula')
add('entanglement','C=|sin(Δ/2)|','E','initial equal product state','analytic derivation')
add('entanglement','N_pure=C/2','E','pure 2x2','partial transpose eigenvalues')
add('entanglement','Δ=2πk ⇒ C=0','E','equal pure state','separable after interaction')
add('noise','ηi=exp(−γi t)','C','independent local Z dephasing','specified phenomenological channel')
add('noise','ρ_ij,kl=ρ_ij,kl^ideal η1^[i≠k] η2^[j≠l]','E','same Z-dephasing channel','CPTP product map')
add('noise','ρ^(T_B)_(ij,kl)=ρ_(il,kj)','E','two-qubit density matrix','definition of partial transpose')
add('noise','N=max(0,−Σ_{λk<0} λk(ρ^(T_B)))','E','two-qubit state','negativity definition')
add('noise','Trρ=1; ρ≥0; ρ=ρ†','E','density operator','necessary physical constraints')
add('noise','γ*≈0.0346059 s^-1','C','default parameters & local Z dephasing','numerical threshold not universal')
add('electrostatic','U_C=q1q2/(4πε0r)','E','vacuum point charges','Coulomb potential')
add('electrostatic','θ_C=−q1q2 t/(4πε0ħr)','E','static point charge model','quantum phase')
add('electrostatic','Δ_total∝[Gm1m2−q1q2/(4πε0)]','E','both 1/r potentials','geometric degeneracy')
add('electrostatic','q_eq=sqrt(4πε0Gm1m2)','E','equal-magnitude residual charges','equal Coulomb and Newton amplitude')
add('electrostatic','q_eq≈8.6175172×10^-25 C','C','m1=m2=10^-14 kg','model numeric')
add('identifiability','Δ_grav∝Gm1m2','E','fixed geometry and t','cannot identify G without mass priors')
add('identifiability','m1→am1;m2→m2/a ⇒ Δ unchanged','E','a>0','product degeneracy')
add('local classical','ρ_sep=Σk pk ρA,k⊗ρB,k','E','LOCC output with separable input','separable by construction')
add('local classical','LOCC(separable)⊂separable','E','strict LOCC assumptions','no local classical generation of entanglement')
add('local classical','N(ρ_sep)=0','E','two-qubit separable density matrix','PPT')
add('scales','ℓ_P²=ħG/c³','E','definition of Planck length','not independent G derivation')
add('scales','G=c³ℓ_P²/ħ','E','ℓP defined from G','algebraic inversion')
add('ROOT','Z=Gc/2','E','definition','not original prediction')
add('ROOT','G=2Z/c','E','Z defined by G','tautological unless Z independently derived')
add('quantum field','[h_ij(x),π^kl(y)]∼iħ δ(x−y)','H','specified canonical gauge-fixed quantum gravity','not derived/verified in V88; structural schematic')
add('beyond Newton','Δ_obs=Δ_Newton+Δ_field+Δ_systematics','C','specified full model','only meaningful if Δ_field predicted independently')
add('falsifiability','W=Tr(ρ W_hat)<0','C','valid entanglement witness with chosen sign convention','requires actual tomography or measurements')
add('future','P(data|M_quantum) vs P(data|M_classical)','C','fully specified models / likelihood','must declare nuisance priors')

with (ROOT/'data'/'equation_catalog.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.writer(f);wr.writerow(['id','theme','equation_or_proposition','proof_status','assumptions','caveat']);wr.writerows(E)

methods=[
('作用量变分','E','GR Newton 低能极限','不可将 G 重新定义算成独立预测'),
('低速固有时展开','E','量子势 mΦ','限制 v≪c 及弱场'),
('Schrodinger 耦合','E','量子相位的来源','不能推导量子化引力场'),
('两体 Newton Hamiltonian','C','四路径条件相位','冻结路径近似'),
('四路径非局部相位','E','去除所有局部相位','不要与单分支相位混淆'),
('纯态 concurrence','E','精确理想纠缠','只有初始等幅独立两比特'),
('PPT 负性','E','混态纠缠复核','要求物理密度矩阵'),
('独立局部 Z 退相干','C','失去纠缠临界阈值','不是实验完整噪声'),
('连续退相干阈值扫描','C','判定 t 与 Γ 可行窗口','阈值依赖初态与结构'),
('质量标度检验','E','Δ∝m1m2','同时检查质量自主定标'),
('时间标度检验','E','Δ∝t','路径与控制场同样可能随 t 变化'),
('全尺度几何对比','E','Δ 几何 1/d 曲线','与 Coulomb 同形'),
('小分支 Taylor 展开','E','Δ∝s1s2/d^3','仅 s≪d'),
('路径零实验 s1=0','E','理想 Δ=0','控制引入的非引力效应应排除'),
('路径零实验 s2=0','E','理想 Δ=0','必须检查不同态制备'),
('短时间零实验','E','t=0 无新增纠缠','原本已纠缠初态应排除'),
('初态两体层析','C','排除预存纠缠','测量效率和 SPAM 偏差'),
('完整两体见证测量','C','不把相位当纠缠','需要可验证观测统计'),
('电荷比例等效审查','E','qeq 定量','残余电荷量子化的实际物理限制'),
('电荷反向与中和对照','C','电荷/引力分离','偶极、Casimir 干扰仍存在'),
('磁场梯度联合建模','C','非引力假阳性','需实际装置磁矩信息'),
('机械振动与热散射','C','退相干噪声','需实验谱密度'),
('有限尺寸校正','O','修复近距离点源发散','V88 未实现体积分'),
('路径动态运动','O','相位轨道积分','V88 仅冻结轨道'),
('LOCC 通道极限','E','严格局域经典信道不能造纠缠','不排除所有经典几何理论'),
('随机局部相位数值对照','E','可分态 N=0','一类具体 LOCC 模型'),
('非局域经典/混合机制','H','检验理论分辨率','模型必须完整具体'),
('非引力量子媒介排查','C','排除量子信息泄漏','实际屏蔽并非自动充分'),
('量子场对易结构检验','H','超越 Newton 相位','需要完整引力有效场论'),
('场迟滞/传播时延','H','试图区分动力学场','需数值相对论模型'),
('独立质量计量','C','解除 Gm1m2 退化','不得用 GM 自身反推'),
('钟差/相位/双体相关三角检验','H','跨测量原理联系','仍可能共享 G 输入'),
('控制实验预注册','C','避免后验筛选','现阶段无实测数据'),
('随机顺序与盲测','C','降低仪器伪差','不能单独消除同形系统误差'),
('参考文献竞争解释','E','2025-2026 已发表模型比较','不以单篇论文终结争论'),
('完整误差预算','O','计入制备、光学、温度、电磁','V88 数值只为理想示例'),
('大尺度太阳系与 EFE 对照','C','兼容性检查','当前弱场微观模拟不适用于黑洞强场'),
('ROOT 新微观作用量','O','从第一性理论推出 G','仍未完成'),
('标准模型与四力耦合统一','O','粒子谱、规范结构、G','仍未完成'),
('独立实验复验','O','真实量子引力证据','本次仅合成数据与代码'),
]
with (ROOT/'data'/'method_matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['id','approach','status','goal','failure_condition']);w.writerows([(f'V88-M{i:02}',*t) for i,t in enumerate(methods,1)])
(ROOT/'results'/'catalog_counts.json').write_text(json.dumps({'equations':len(E),'methods':len(methods)},indent=2),encoding='utf8')
print('catalog equations:',len(E),'methods:',len(methods))
