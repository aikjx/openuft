import numpy as np
import time
from typing import Dict, List, Tuple, Optional, Union

# 性能监控装饰器
def performance_monitor(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.6f} 秒")
        return result
    return wrapper

# 可选依赖
try:
    from numba import jit
except ImportError:
    def jit(func=None, **kwargs):
        if func:
            return func
        return lambda f: f

try:
    import cupy as cp
except ImportError:
    cp = None

try:
    import jax
    import jax.numpy as jnp
except ImportError:
    jax = None
    jnp = None

try:
    import torch
except ImportError:
    torch = None

try:
    import tensorflow as tf
except ImportError:
    tf = None

try:
    from autograd import grad
except ImportError:
    grad = None

try:
    import mpmath
except ImportError:
    mpmath = None

class ParticlePhysics:
    """粒子物理模块"""
    
    def __init__(self):
        """初始化粒子物理参数"""
        # 物理常数
        self.G = 6.67430e-11  # 引力常数
        self.c = 299792458  # 光速
        self.hbar = 1.054571817e-34  # 约化普朗克常数
        self.k_B = 1.380649e-23  # 玻尔兹曼常数
        self.Avogadro = 6.02214076e23  # 阿伏伽德罗常数
        self.m_e = 9.1093837015e-31  # 电子质量
        self.m_p = 1.67262192369e-27  # 质子质量
        self.q_e = 1.602176634e-19  # 电子电荷
        self.epsilon_0 = 8.8541878128e-12  # 真空介电常数
        self.mu_0 = 1.25663706212e-6  # 真空磁导率
        
        # 粒子物理参数
        self.alpha = 1/137.035999084  # 精细结构常数
        self.G_F = 1.1663787e-5  # 费米常数 (GeV^-2)
        self.g_s = 0.118  # 强相互作用耦合常数
        
        # 粒子质量 (eV/c²)
        self.m_e_eV = 0.511e6  # 电子
        self.m_mu_eV = 105.6583755e6  # μ子
        self.m_tau_eV = 1776.86e6  # τ子
        self.m_nu_e_eV = 0.0001  # 电子中微子
        self.m_nu_mu_eV = 0.001  # μ子中微子
        self.m_nu_tau_eV = 0.01  # τ子中微子
        self.m_u_eV = 2.3e6  # 上夸克
        self.m_d_eV = 4.8e6  # 下夸克
        self.m_s_eV = 95e6  # 奇异夸克
        self.m_c_eV = 1.275e9  # 粲夸克
        self.m_b_eV = 4.18e9  # 底夸克
        self.m_t_eV = 173.0e9  # 顶夸克
        self.m_W_eV = 80.379e9  # W玻色子
        self.m_Z_eV = 91.1876e9  # Z玻色子
        self.m_H_eV = 125.18e9  # 希格斯玻色子
        self.m_gluon_eV = 0  # 胶子
        
        # 统一场论参数
        self.Z = self.G * self.c**2  # 引力光速统一常数
        self.r_k = 1.23e-15  # 核力场半径
        
    @performance_monitor
    def calculate_particle_decay_rate(self, particle: str, energy: float) -> float:
        """
        计算粒子衰变率
        
        参数:
            particle: 粒子名称
            energy: 能量 (GeV)
            
        返回:
            衰变率 (s^-1)
        """
        # 不同粒子的衰变率
        if particle == 'muon':
            # μ子衰变率
            decay_rate = (self.G_F**2 * self.m_mu_eV**5) / (192 * np.pi**3 * (self.hbar * self.c)**6)
        elif particle == 'tau':
            # τ子衰变率
            decay_rate = (self.G_F**2 * self.m_tau_eV**5) / (192 * np.pi**3 * (self.hbar * self.c)**6)
        elif particle == 'W':
            # W玻色子衰变率
            decay_rate = (self.G_F * self.m_W_eV**3) / (6 * np.sqrt(2) * np.pi)
        elif particle == 'Z':
            # Z玻色子衰变率
            decay_rate = (self.G_F * self.m_Z_eV**3) / (12 * np.sqrt(2) * np.pi)
        elif particle == 'Higgs':
            # 希格斯玻色子衰变率
            decay_rate = 1.28e-24  # 约1.28e-24 s^-1
        else:
            decay_rate = 0
        
        # 能量修正
        decay_rate *= (energy / (self.m_mu_eV / 1e9))**2
        
        return decay_rate
    
    @performance_monitor
    def calculate_neutrino_oscillation(self, distance: float, energy: float, mixing_angle: float) -> float:
        """
        计算中微子振荡概率
        
        参数:
            distance: 距离 (km)
            energy: 中微子能量 (GeV)
            mixing_angle: 混合角 (弧度)
            
        返回:
            振荡概率
        """
        # 中微子质量平方差
        delta_m2 = 2.5e-3  # eV² (太阳中微子)
        
        # 振荡概率
        probability = np.sin(2 * mixing_angle)**2 * np.sin(1.27 * delta_m2 * distance / energy)**2
        
        return probability
    
    @performance_monitor
    def calculate_strong_force(self, distance: float) -> float:
        """
        计算强相互作用力
        
        参数:
            distance: 距离 (m)
            
        返回:
            强相互作用力 (N)
        """
        # 强相互作用势 (线性势)
        k = 1e5  # N/m (弦张力)
        V = k * distance
        
        # 力
        force = -np.gradient(np.array([V]))[0]
        
        return abs(force)
    
    @performance_monitor
    def calculate_weak_force(self, distance: float, energy: float) -> float:
        """
        计算弱相互作用力
        
        参数:
            distance: 距离 (m)
            energy: 能量 (GeV)
            
        返回:
            弱相互作用力 (N)
        """
        # 弱相互作用势 (短程)
        m_W = self.m_W_eV / (self.c**2 * 1e9)  # W玻色子质量 (kg)
        lambda_w = self.hbar / (m_W * self.c)  # 弱相互作用范围
        
        # 力
        force = (self.G_F * energy**2) / (distance**2) * np.exp(-distance / lambda_w)
        
        return force
    
    @performance_monitor
    def simulate_particle_collision(self, particle1: str, particle2: str, energy: float) -> Dict[str, any]:
        """
        模拟粒子碰撞
        
        参数:
            particle1: 粒子1名称
            particle2: 粒子2名称
            energy: 质心能量 (GeV)
            
        返回:
            碰撞结果
        """
        # 碰撞截面
        if particle1 == 'electron' and particle2 == 'electron':
            # e-e 弹性散射截面
            cross_section = (4 * np.pi * self.alpha**2) / (s * np.sin(theta/2)**4)
            where s = energy**2
            theta = np.pi/2  # 平均散射角
        elif particle1 == 'proton' and particle2 == 'proton':
            # pp 非弹性散射截面
            cross_section = 100e-30 * (1 + np.log(energy)**2)  # 简化公式
        else:
            cross_section = 1e-30
        
        # 产生的粒子
        products = []
        if energy > 100:
            products.extend(['quark', 'antiquark', 'gluon'])
        if energy > 200:
            products.extend(['W', 'Z'])
        if energy > 1000:
            products.append('Higgs')
        
        return {
            'cross_section': cross_section,
            'products': products,
            'energy': energy,
            'particle1': particle1,
            'particle2': particle2
        }
    
    @performance_monitor
    def calculate_particle_mass(self, quark_contents: List[str]) -> float:
        """
        计算强子质量
        
        参数:
            quark_contents: 夸克组成
            
        返回:
            强子质量 (GeV/c²)
        """
        # 夸克质量字典
        quark_masses = {
            'u': self.m_u_eV / 1e9,
            'd': self.m_d_eV / 1e9,
            's': self.m_s_eV / 1e9,
            'c': self.m_c_eV / 1e9,
            'b': self.m_b_eV / 1e9,
            't': self.m_t_eV / 1e9
        }
        
        # 计算总质量
        total_mass = 0
        for quark in quark_contents:
            if quark in quark_masses:
                total_mass += quark_masses[quark]
        
        # 结合能修正
        binding_energy = 0.3  # GeV
        total_mass += binding_energy
        
        return total_mass
    
    @performance_monitor
    def calculate_nuclear_binding_energy(self, mass_number: int, atomic_number: int) -> float:
        """
        计算核结合能
        
        参数:
            mass_number: 质量数
            atomic_number: 原子序数
            
        返回:
            结合能 (MeV)
        """
        # 液滴模型
        a_v = 15.75  # 体积项系数
        a_s = 17.8  # 表面项系数
        a_c = 0.711  # 库仑项系数
        a_a = 23.7  # 不对称项系数
        a_p = 11.18  # 对项系数
        
        # 结合能公式
        B = a_v * mass_number - a_s * mass_number**(2/3) - \
            a_c * atomic_number**2 / mass_number**(1/3) - \
            a_a * (mass_number - 2 * atomic_number)**2 / mass_number
        
        # 对项
        if mass_number % 2 == 0 and atomic_number % 2 == 0:
            B += a_p / mass_number**(1/2)
        elif mass_number % 2 == 1:
            B += 0
        else:
            B -= a_p / mass_number**(1/2)
        
        return B
    
    @performance_monitor
    def calculate_particle_spin(self, particle: str) -> float:
        """
        计算粒子自旋
        
        参数:
            particle: 粒子名称
            
        返回:
            自旋
        """
        # 粒子自旋字典
        spin_dict = {
            'electron': 1/2,
            'muon': 1/2,
            'tau': 1/2,
            'neutrino': 1/2,
            'proton': 1/2,
            'neutron': 1/2,
            'quark': 1/2,
            'photon': 1,
            'W': 1,
            'Z': 1,
            'gluon': 1,
            'Higgs': 0,
            'pion': 0,
            'kaon': 0,
            'rho': 1,
            'omega': 1,
            'eta': 0
        }
        
        return spin_dict.get(particle, 0)
    
    @performance_monitor
    def calculate_particle_lifetime(self, particle: str) -> float:
        """
        计算粒子寿命
        
        参数:
            particle: 粒子名称
            
        返回:
            寿命 (s)
        """
        # 粒子寿命字典 (s)
        lifetime_dict = {
            'electron': 1e28,  # 稳定
            'proton': 1e34,  # 稳定
            'neutron': 881.5,  # 自由中子
            'muon': 2.197e-6,
            'tau': 2.906e-13,
            'pion': 2.6033e-8,
            'kaon': 1.238e-8,
            'rho': 4.42e-24,
            'omega': 0.84e-23,
            'eta': 5.1e-19,
            'lambda': 2.632e-10,
            'sigma': 0.8e-10,
            'xi': 2.9e-10,
            'omega': 0.82e-10,
            'W': 2.08e-25,
            'Z': 2.65e-25,
            'Higgs': 1.56e-22
        }
        
        return lifetime_dict.get(particle, 0)
    
    @performance_monitor
    def calculate_cp_violation(self, particle: str) -> float:
        """
        计算CP破坏参数
        
        参数:
            particle: 粒子名称
            
        返回:
            CP破坏参数
        """
        # CP破坏参数
        if particle == 'kaon':
            # K meson CP破坏
            epsilon = 2.228e-3
            return epsilon
        elif particle == 'B meson':
            # B meson CP破坏
            sin2beta = 0.679
            return sin2beta
        elif particle == 'neutrino':
            # 中微子CP破坏
            delta_cp = np.pi/2  # 假设值
            return delta_cp
        else:
            return 0
    
    @performance_monitor
    def simulate_cosmic_rays(self, energy: float, altitude: float) -> Dict[str, any]:
        """
        模拟宇宙线
        
        参数:
            energy: 宇宙线能量 (GeV)
            altitude: 海拔高度 (km)
            
        返回:
            宇宙线相互作用参数
        """
        # 大气深度
        atmospheric_depth = 1030 * np.exp(-altitude / 8.5)  # g/cm²
        
        # 相互作用概率
        interaction_probability = 1 - np.exp(-atmospheric_depth / 80)
        
        # 次级粒子数量
        n_secondary = 10 * np.log10(energy / 10)
        
        return {
            'atmospheric_depth': atmospheric_depth,
            'interaction_probability': interaction_probability,
            'secondary_particles': n_secondary,
            'energy': energy,
            'altitude': altitude
        }
    
    @performance_monitor
    def calculate_particle_interaction_cross_section(self, particle1: str, particle2: str, energy: float) -> float:
        """
        计算粒子相互作用截面
        
        参数:
            particle1: 粒子1名称
            particle2: 粒子2名称
            energy: 能量 (GeV)
            
        返回:
            截面 (m²)
        """
        # 不同相互作用的截面
        if particle1 == 'electron' and particle2 == 'electron':
            # e-e 散射截面
            cross_section = (4 * np.pi * self.alpha**2) / (energy**2)
        elif particle1 == 'proton' and particle2 == 'proton':
            # pp 散射截面
            cross_section = 100e-30 * (1 + np.log(energy)**2)
        elif particle1 == 'neutron' and particle2 == 'nucleus':
            # 中子-核散射截面
            cross_section = 1e-28
        else:
            cross_section = 1e-30
        
        # 转换为平方米
        cross_section_m2 = cross_section * 1e-32  # GeV^-2 → m²
        
        return cross_section_m2
    
    @performance_monitor
    def calculate_particle_antiparticle_annihilation(self, particle: str, energy: float) -> Dict[str, any]:
        """
        计算粒子-反粒子湮灭
        
        参数:
            particle: 粒子名称
            energy: 能量 (GeV)
            
        返回:
            湮灭参数
        """
        # 湮灭截面
        if particle == 'electron':
            # e+e- 湮灭
            cross_section = (4 * np.pi * self.alpha**2) / (3 * energy**2)
            products = ['photon', 'photon']
        elif particle == 'proton':
            # p-pbar 湮灭
            cross_section = 1e-28
            products = ['mesons', 'baryons']
        elif particle == 'quark':
            # q-qbar 湮灭
            cross_section = 1e-29
            products = ['gluons', 'bosons']
        else:
            cross_section = 0
            products = []
        
        return {
            'cross_section': cross_section,
            'products': products,
            'energy': energy,
            'particle': particle
        }

# 便捷函数
@performance_monitor
def calculate_particle_decay_rate(particle: str, energy: float) -> float:
    """计算粒子衰变率"""
    pp = ParticlePhysics()
    return pp.calculate_particle_decay_rate(particle, energy)

@performance_monitor
def calculate_neutrino_oscillation(distance: float, energy: float, mixing_angle: float) -> float:
    """计算中微子振荡概率"""
    pp = ParticlePhysics()
    return pp.calculate_neutrino_oscillation(distance, energy, mixing_angle)

@performance_monitor
def calculate_strong_force(distance: float) -> float:
    """计算强相互作用力"""
    pp = ParticlePhysics()
    return pp.calculate_strong_force(distance)

@performance_monitor
def calculate_nuclear_binding_energy(mass_number: int, atomic_number: int) -> float:
    """计算核结合能"""
    pp = ParticlePhysics()
    return pp.calculate_nuclear_binding_energy(mass_number, atomic_number)

if __name__ == "__main__":
    # 测试代码
    pp = ParticlePhysics()
    
    # 测试粒子衰变率计算
    decay_rate = pp.calculate_particle_decay_rate('muon', 1)
    print(f"μ子衰变率: {decay_rate:.2e} s^-1")
    
    # 测试中微子振荡计算
    distance = 1000  # km
    energy = 1  # GeV
    mixing_angle = np.pi/4  # 45度
    oscillation_prob = pp.calculate_neutrino_oscillation(distance, energy, mixing_angle)
    print(f"中微子振荡概率: {oscillation_prob:.3f}")
    
    # 测试强相互作用力计算
    distance = 1e-15  # 1 fm
    strong_force = pp.calculate_strong_force(distance)
    print(f"强相互作用力: {strong_force:.2e} N")
    
    # 测试核结合能计算
    binding_energy = pp.calculate_nuclear_binding_energy(56, 26)  # Fe-56
    print(f"Fe-56结合能: {binding_energy:.2f} MeV")
    print(f"Fe-56比结合能: {binding_energy/56:.3f} MeV/nucleon")
    
    # 测试粒子质量计算
    proton_mass = pp.calculate_particle_mass(['u', 'u', 'd'])
    print(f"质子质量: {proton_mass:.3f} GeV/c²")
    
    neutron_mass = pp.calculate_particle_mass(['u', 'd', 'd'])
    print(f"中子质量: {neutron_mass:.3f} GeV/c²")
    
    print("粒子物理模块测试完成!")
