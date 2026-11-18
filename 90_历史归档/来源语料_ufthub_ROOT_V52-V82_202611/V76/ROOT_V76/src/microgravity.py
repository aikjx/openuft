"""ROOT V76: reproducible established-physics calculations (not a unified-field discovery).
SI units, signature (-,+,+,+). No optional dependencies.
Reference: CODATA 2022 values for G, vacuum permittivity, elementary charge.
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Sequence

C = 299_792_458.0  # exact SI
G = 6.67430e-11  # CODATA 2022, measured not derived
EPS0 = 8.8541878188e-12  # CODATA 2022; uncertainty in last digits
MU0 = 1.0 / (EPS0 * C*C)
E_CHARGE = 1.602176634e-19  # exact SI
H = 6.62607015e-34  # exact SI
HBAR = H/(2*math.pi)
MEV = 1e6 * E_CHARGE
DEUTERON_BINDING_MEV = 2.22456640  # CODATA 2022 approximate
EARTH_G = 9.80665  # standard gravitational acceleration (conventional value)

Vector = tuple[float, float, float]

def vec(values: Sequence[float]) -> Vector:
    if len(values) != 3: raise ValueError('three Cartesian components required')
    return tuple(float(x) for x in values)  # type: ignore

def plus(a: Vector,b: Vector) -> Vector: return (a[0]+b[0],a[1]+b[1],a[2]+b[2])
def minus(a: Vector,b: Vector) -> Vector: return (a[0]-b[0],a[1]-b[1],a[2]-b[2])
def scale(a: Vector,x: float) -> Vector: return (a[0]*x,a[1]*x,a[2]*x)
def dot(a: Vector,b: Vector) -> float: return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def cross(a: Vector,b: Vector) -> Vector:
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm2(a: Vector) -> float: return dot(a,a)
def norm(a: Vector) -> float: return math.sqrt(norm2(a))

@dataclass(frozen=True)
class EMT:
    """3+1 electromagnetic tensor components: T00=u; T0i=S_i/c; Tij=-Maxwell stress.
    Units for all entries: J/m^3 in local orthonormal inertial frame.
    """
    energy_density: float
    momentum_energy: Vector
    spatial: tuple[Vector, Vector, Vector]

    def trace(self) -> float:
        return -self.energy_density+sum(self.spatial[i][i] for i in range(3))

    def active_density(self) -> float:
        """(T00+sum Tii)/c²: local stationary linearized GR combination,
        not a universal isolated field-only mass formula."""
        return (self.energy_density + sum(self.spatial[i][i] for i in range(3))) / C**2


def em_energy_density(E: Vector,B: Vector) -> float:
    return 0.5*(EPS0*norm2(E)+norm2(B)/MU0)

def em_energy_flux(E: Vector,B: Vector) -> Vector:
    return scale(cross(E,B), 1.0/MU0)

def em_tensor(E: Vector,B: Vector) -> EMT:
    u=em_energy_density(E,B)
    rows=[]
    for i in range(3):
        rows.append(tuple((u if i==j else 0.0)-EPS0*E[i]*E[j]-B[i]*B[j]/MU0 for j in range(3)))
    return EMT(u,scale(em_energy_flux(E,B),1/C),tuple(rows))  # type: ignore[arg-type]

def em_cross_energy(E1: Vector,B1: Vector,E2: Vector,B2: Vector) -> float:
    return EPS0*dot(E1,E2)+dot(B1,B2)/MU0

def em_superposition_identity(E1: Vector,B1: Vector,E2: Vector,B2: Vector):
    u1=em_energy_density(E1,B1);u2=em_energy_density(E2,B2)
    cross_term=em_cross_energy(E1,B1,E2,B2)
    total=em_energy_density(plus(E1,E2),plus(B1,B2))
    return {'u1':u1,'u2':u2,'cross':cross_term,'sum':u1+u2+cross_term,'total':total}

def plane_wave_fields(e_amplitude: float, phase: float, axis: int=0):
    """Plane vacuum wave propagating +z, E along x, B along y."""
    e=e_amplitude*math.cos(phase)
    if axis == 0: return (e,0.,0.),(0.,e/C,0.)
    raise ValueError('only +z/+x E configuration in this demonstration')

def em_invariants(E: Vector,B: Vector):
    # F_munu F^munu = 2(B²-E²/c²) in common SI tensor convention
    return {'B2_minus_E2_over_c2':norm2(B)-norm2(E)/C**2,'E_dot_B':dot(E,B)}

def gravitating_equivalent_mass(added_joules: float) -> float:
    return added_joules/(C*C)

def spherical_monopole_delta_g(added_energy_joules:float, distance_m:float)->float:
    if distance_m<=0: raise ValueError('distance_m must be positive')
    return G*gravitating_equivalent_mass(added_energy_joules)/(distance_m**2)

def sphere_field_energy(B_tesla:float,radius_m:float)->float:
    if radius_m<0: raise ValueError('negative sphere radius')
    return 4*math.pi*radius_m**3/3 * em_energy_density((0,0,0),(0,0,B_tesla))

def thermal_energy(mass_kg:float,heat_capacity_J_kg_K:float,delta_temp_K:float)->float:
    return mass_kg*heat_capacity_J_kg_K*delta_temp_K

def nuclear_binding_mass_defect(binding_MeV:float=DEUTERON_BINDING_MEV)->float:
    return binding_MeV*MEV/(C*C)

def redshift_fraction(delta_height_m:float,g:float=EARTH_G)->float:
    return g*delta_height_m/(C*C)

def relativistic_energy(mass_kg:float,v_m_s:float)->float:
    if mass_kg<0 or not (-C < v_m_s < C): raise ValueError('mass>=0 and |v|<c')
    return mass_kg*C*C/math.sqrt(1-(v_m_s/C)**2)

def relativistic_kinetic_energy(mass_kg:float,v_m_s:float)->float:
    if mass_kg<0 or not (-C < v_m_s < C): raise ValueError('mass>=0 and |v|<c')
    beta2=(v_m_s/C)**2
    return mass_kg*C*C * (1/math.sqrt(1-beta2)-1)

def system_invariant_mass(total_energy_j:float,total_momentum:Vector)->float:
    """M=sqrt((E/c²)^2-|p|²/c²); errors on spacelike total four-momentum."""
    if total_energy_j<0: raise ValueError('negative total energy')
    arg=(total_energy_j/C**2)**2-norm2(total_momentum)/C**2
    scale_ref=max((total_energy_j/C**2)**2,1e-120)
    if arg < -1e-12*scale_ref: raise ValueError('nonphysical spacelike total 4-momentum')
    return math.sqrt(max(0,arg))

def two_photon_invariant_mass(E1_j:float,E2_j:float,angle_rad:float)->float:
    if E1_j<0 or E2_j<0: raise ValueError('negative photon energy')
    return math.sqrt(max(0.,2*E1_j*E2_j*(1-math.cos(angle_rad))))/(C*C)

def quantum_two_level_energy(E1:float,E2:float,coupling:float,theta:float,phase:float)->float:
    """Illustrative Hermitian 2×2 Hamiltonian H=[[E1,v],[v,E2]].
    State amplitudes [cos theta, exp(i phase)sin theta]. Energy unit set by inputs."""
    return E1*math.cos(theta)**2+E2*math.sin(theta)**2+2*coupling*math.sin(theta)*math.cos(theta)*math.cos(phase)

def quantum_two_level_eigenvalues(E1:float,E2:float,coupling:float):
    m=(E1+E2)/2; s=math.hypot((E1-E2)/2,coupling)
    return m-s,m+s

@dataclass(frozen=True)
class Ledger:
    """Energy accounting for ONE closed system. Each field energy counted once."""
    battery:float
    field:float
    thermal:float
    mechanical:float
    radiation_still_inside:float=0.
    def total(self): return self.battery+self.field+self.thermal+self.mechanical+self.radiation_still_inside
    def transfer_to_field(self,energy_j:float):
        if energy_j>self.battery: raise ValueError('not enough battery energy')
        return Ledger(self.battery-energy_j,self.field+energy_j,self.thermal,self.mechanical,self.radiation_still_inside)
    def transfer_to_heat(self,energy_j:float):
        if energy_j>self.field: raise ValueError('not enough field energy')
        return Ledger(self.battery,self.field-energy_j,self.thermal+energy_j,self.mechanical,self.radiation_still_inside)
    def emission(self,energy_j:float):
        if energy_j>self.radiation_still_inside: raise ValueError('insufficient internal radiation')
        return Ledger(self.battery,self.field,self.thermal,self.mechanical,self.radiation_still_inside-energy_j)

def helix(speed:float,radius:float,omega:float,pitch_speed:float):
    """Minkowski helical spatial trajectory velocity decomposition: kinematics only."""
    if radius<=0: raise ValueError('radius>0')
    v=math.hypot(radius*omega,pitch_speed)
    if speed<=0 or not math.isclose(v,speed,rel_tol=1e-10): raise ValueError('specified speed mismatch')
    return {'speed':v,'curvature':radius*omega**2/v**2,'torsion':pitch_speed*omega/v**2,'acceleration':radius*omega**2}

def identifiability_one_observation(g_effective:float,mass:float,radius:float):
    """Only GM measured; G and M cannot both be independently recovered."""
    if radius<=0: raise ValueError('radius>0')
    return {'mu':g_effective*radius*radius,'fitted_G_if_mass_known':g_effective*radius*radius/mass}

def source_taxonomy():
    return [
      ('电子/轻子静能','fermion','已知','物质场 T_{μν}，勿重复加入测得的原子质量'),
      ('夸克静质量','QCD','已知','作为强子总能量的一个分解项，重整化方案依赖'),
      ('胶子场动能','QCD','已知','QCD 完整能动张量的一部分'),
      ('QCD 迹反常','QCD','已知','强子质量分解涉及重整化；非额外可重复加的质量'),
      ('强子束缚能','QCD','已知','结合系统的总质量由完整本征能量决定'),
      ('核结合能','Nuclear','已知','质量亏损 ΔM=E_bind/c²'),
      ('弱相互作用衰变','Weak','已知','能量从初态到终态与辐射转移'),
      ('Higgs 真空期望值','Higgs','已知/开放','粒子质量耦合已知，真空能引力与宇宙学常数仍开放'),
      ('原子电子能级','Atomic','已知','跃迁能量与封闭系统质量差'),
      ('分子化学键','Chemical','已知','化学结合能影响总质量'),
      ('固体晶格振动','Condensed','已知','声子能量贡献热能；定义账本分区'),
      ('热运动','Thermal','已知','内能增加质量，压强应力进入 T'),
      ('电场储能','EM','已知','ε₀ E²/2'),
      ('磁场储能','EM','已知','B²/(2μ₀)'),
      ('电磁波','EM','已知','辐射能量与动量；两标量不变量可同时为零'),
      ('电磁场交叉项','EM','已知','ε₀E₁·E₂+B₁·B₂/μ₀'),
      ('磁致伸缩','Engineering','系统误差','设备形变可以伪装成重力读数'),
      ('热应力','Engineering','系统误差','压力和支持结构需要计入完整封闭系统'),
      ('电源内部能量','Engineering','已知','向磁场转移储能不改变封闭系统总能量'),
      ('机械旋转动能','Motion','已知','角动量/惯性/应力，不等同于额外基本力'),
      ('整体平动','Motion','已知','坐标系能量变化，封闭系统不变质量不变'),
      ('天体自转/公转','Astro','已知','源动量与框架拖曳；需区分非惯性效应'),
      ('潮汐与局部曲率','GR','已知','物体尺度上的梯度和相对加速度'),
      ('量子态叠加','Quantum','已知/条件','计算 <T> 或 Hamiltonian，不把相干当额外质量'),
      ('量子纠缠','Quantum','已知/开放','相关性本身不是可随意追加的质量'),
      ('真空涨落','Quantum','未解决','重整化后 <T> 与宇宙学常数问题'),
      ('自旋/磁矩','Spin','已知/假设','标准耦合可算；超出 GR 的独立引力仍待证据'),
      ('空间螺旋基元','ROOT hypothesis','未证实','需定义可协变场变量/作用量/实测证伪'),
      ('候选第五力','New Physics','未证实','必须考虑粒子荷、短程源形状及组成依赖'),
      ('规范异常','QFT','已知','自洽性条件，不能从几何轨迹独立产生粒子谱'),
      ('引力常数 G 来源','Gravity','未解决','不能反向标定自由长度冒充无参数预测')]
