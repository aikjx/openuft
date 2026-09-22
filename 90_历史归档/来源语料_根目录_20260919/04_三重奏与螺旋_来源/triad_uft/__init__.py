# -*- coding: utf-8 -*-
"""
triad_uft — 全维三重奏统一场论工具包（工业级 v5.1）
========================================================
封装已严格证明的几何-运动学定理，提供可复现、可测试、可应用的API。

【诚实声明】本包封装的是已验证的几何-运动学定理，不是已完成的"万有理论"。
引力量子化、暗物质/暗能量、弯曲时空推广等仍为开放问题。

v4.0 新增模块：
- curved_spacetime: GR弯曲时空推广（4维Frenet标架、Schwarzschild轨道、GR经典检验）
- artificial_field_deep: 人工场实验深化（效率因子微观机制、参数扫描、三阶段路线图）
- strong_force: 强相互作用精确描述（Yukawa势、介子交换、排斥芯、液滴模型）
- particle_masses: 粒子物理质量谱与混合角（三代费米子、CKM/PMNS、跷跷板机制）
- quantum_gravity_deep: 量子引力深入（时空量子化、引力子双螺旋、黑洞熵、全息原理）
- cosmology_deep: 宇宙学深入（暗能量视界截断、暴胀、CMB、暗物质、宇宙学疑难）

v5.0 新增模块：
- deep_directions: D1-D20二十个物理分支深化方向汇总API（262项精确对标+诚实审计）

v5.1 扩展（向后兼容）：
- deep_directions.EXTENDED_DIRECTIONS: D1-D25（新增流体力学/声学/地球物理/量子信息/天体物理）
- summary_extended() / get_direction_extended() / honesty_statement_extended()
- reynolds_number / sound_speed_laplace / earth_surface_gravity / chsh_quantum_bound / schwarzschild_radius

快速开始
--------
>>> import triad_uft as tu
>>> result = tu.check_helix(R=1.0, omega=2.0, b=0.6)
>>> print(result["rel_error"])  # 应接近0

>>> sim = tu.LorentzSimulator(b_field=tu.GradientB(B0=1.0, g=50.0))
>>> sim.run(v0=[1e7, 0, 5e6], t_end=1e-11, dt=1e-15)
>>> print(sim.triad_check()["median"])  # 梯度磁场中应~1e-18

>>> # v4.0 新功能
>>> bh = tu.black_hole_thermodynamics(1.989e30)  # 太阳质量黑洞
>>> print(bh.hawking_temperature)  # ~10^-8 K
>>> cosmo = tu.cosmic_evolution_summary()
>>> print(cosmo.age_gyr)  # ~13.8 Gyr

>>> # v5.1 扩展
>>> ext = tu.summary_extended()
>>> print(ext["n_directions"])  # 25
"""

__version__ = "5.1.0"
__author__ = "算法联盟"

# 核心模块
from . import constants
from . import geometry
from . import lorentz
from . import triad
from . import provenance
from . import export

# 统一场论模块（v2.0新增）
from . import grand_unification
from . import nuclear
from . import artificial_field
from . import weak_force
from . import quantization

# 光速螺旋与定理谱系（v3.0新增）
from . import light_speed_helix
from . import theorem_system

# 开放问题攻坚系列（v4.0新增）
from . import curved_spacetime
from . import artificial_field_deep
from . import strong_force
from . import particle_masses
from . import quantum_gravity_deep
from . import cosmology_deep

# D1-D20深化方向汇总（v5.0新增）
from . import deep_directions

# 高层 API（最常用）
from .triad import (
    check_helix,
    check_alldim,
    check_adiabatic,
    check_gradient_b_field,
    check_uniform_b_field,
    electron_benchmark,
    theorem_status,
    proven_theorems,
    open_problems,
)

# 几何
from .geometry import (
    helix_curvature_torsion,
    alldim_helix_curvatures,
    frenet_from_trajectory,
    curvature_2d,
    torsion_3d,
)

# 洛伦兹力模拟
from .lorentz import (
    LorentzSimulator,
    MagneticField,
    UniformB,
    GradientB,
)

# 诚实审计
from .provenance import (
    ValidationStatus,
    TheoremRecord,
    THEOREMS,
    honesty_statement,
    audit_report,
)

# 大统一力方程（v2.0新增）
from .grand_unification import (
    grand_force,
    ForceComponents,
    mass_velocity_relation,
    energy_momentum_relation,
    rest_energy,
    rest_momentum,
)

# 核力场（v2.0新增）
from .nuclear import (
    nuclear_field,
    nuclear_potential,
    nuclear_force_range,
    infer_nuclear_coupling,
    nuclear_to_gravity_ratio,
)

# 人工场设计（v2.0新增）
from .artificial_field import (
    artificial_gravity_field,
    required_dBdt_for_gravity,
    solenoid_dBdt,
    design_experiment,
    ligo_comparison,
    ArtificialFieldResult,
)

# 弱力几何化（v2.0新增）
from .weak_force import (
    weak_force_range,
    w_boson_mass_from_energy,
    weak_momentum_uncertainty,
    weak_interaction_open_issues,
)

# 量子化起源（v2.0新增）
from .quantization import (
    angular_momentum_from_helix,
    quantized_angular_momentum,
    electron_spin_helix,
    compton_frequency,
    compton_wavelength,
    triad_quantization_connection,
    quantization_open_issues,
)

# 光速螺旋（v3.0新增）
from .light_speed_helix import (
    light_speed_helix_params,
    helix_curvature_torsion_light_speed,
    check_light_speed_helix,
    symbolic_proof_light_speed_helix,
    electron_light_speed_helix,
    alldim_light_speed_helix,
    mass_geometric_origin,
    rest_momentum_geometric,
    quick_verify,
    LightSpeedHelixResult,
)

# 定理谱系（v3.0新增）
from .theorem_system import (
    verify_TS1, verify_TS2, verify_TS3, verify_TS4, verify_TS5,
    verify_TS6, verify_TS7, verify_TS8, verify_TS9, verify_TS10,
    verify_TS11, verify_TS12,
    theorem_summary,
    verify_all,
    get_theorem,
    logic_chain,
    AXIOMS,
    THEOREMS as THEOREM_SYSTEM_THEOREMS,
    TheoremRecord as TheoremSystemRecord,
    TheoremStatus,
)

# GR弯曲时空推广（v4.0新增）
from .curved_spacetime import (
    FrenetFrame4D,
    SchwarzschildOrbit,
    frenet_4d_from_trajectory,
    schwarzschild_circular_orbit,
    mercury_precession,
    gravitational_redshift,
    light_deflection,
    shapiro_delay,
    curved_spacetime_helix,
    gr_classical_tests_summary,
)

# 人工场实验深化（v4.0新增）
from .artificial_field_deep import (
    ArtificialFieldDeepResult,
    artificial_field_equation,
    efficiency_factor_geometric,
    efficiency_factor_quantum,
    efficiency_factor_statistical,
    total_efficiency,
    nominal_gravity,
    actual_gravity,
    estimate_snr,
    design_experiment as design_experiment_deep,
    parameter_scan,
    ligo_comparison as ligo_comparison_deep,
    experimental_roadmap,
    observable_predictions,
    falsification_criteria,
)

# 强相互作用精确描述（v4.0新增）
from .strong_force import (
    NuclearPotentialResult,
    strong_force_range,
    nuclear_coupling_constant,
    nuclear_to_gravity_ratio as strong_to_gravity_ratio,
    yukawa_potential,
    nuclear_potential as strong_nuclear_potential,
    nuclear_well_depth,
    nuclear_well_position,
    deuteron_D_state_probability,
    weizsaecker_binding_energy,
    binding_energy_examples,
    qcd_beta_function,
    asymptotic_freedom_scale,
)

# 粒子物理质量谱与混合角（v4.0新增）
from .particle_masses import (
    ParticleHelixParams,
    MASSES,
    CKM,
    PMNS,
    mass_to_helix_radius,
    helix_radius_to_mass,
    particle_helix_params,
    mass_ratio_verification,
    ckm_mixing_angles,
    pmns_mixing_angles,
    ckm_pmns_comparison,
    neutrino_mass_seesaw,
    neutrino_oscillation_params,
    yukawa_coupling_from_radius,
    mass_hierarchy_explanation,
)

# 量子引力深入（v4.0新增）
from .quantum_gravity_deep import (
    BlackHoleThermo,
    planck_scale,
    spacetime_quantization,
    graviton_double_helix,
    black_hole_thermodynamics,
    solar_mass_black_hole,
    black_hole_entropy_helix,
    holographic_principle,
    black_hole_laws,
    information_paradox,
    string_lqg_comparison,
    quantum_gravity_open_problems,
)

# 宇宙学深入（v4.0新增）
from .cosmology_deep import (
    CosmicEvolution,
    cosmological_constant_problem,
    inflation_helix,
    cosmic_age_calculation,
    cosmic_evolution_summary,
    cosmic_stages,
    cmb_acoustic_peaks,
    cmb_polarization,
    dark_matter_candidates,
    cosmological_parameters,
    cosmological_puzzles,
    cosmology_open_problems,
)

# D1-D20深化方向汇总（v5.0新增）
from .deep_directions import (
    DIRECTIONS,
    EXTENDED_DIRECTIONS,
    summary as deep_directions_summary,
    summary_extended as deep_directions_summary_extended,
    get_direction,
    get_direction_extended,
    honesty_statement as deep_directions_honesty,
    honesty_statement_extended as deep_directions_honesty_extended,
    qcd_beta_coefficients,
    wimp_cross_section,
    planck_scale as dd_planck_scale,
    artificial_field_efficiency,
    mass_from_helix_radius,
    uncertainty_product,
    universe_age_estimate,
    quadrupole_radiation_power,
    pmns_oscillation_probability,
    higgs_parameters,
    weizsaecker_binding_energy as dd_weizsaecker_binding_energy,
    bcs_gap_energy,
    hydrogen_energy_level,
    boltzmann_distribution,
    photon_energy,
    plasma_frequency,
    frenet_curvature_torsion,
    verlet_single_step,
    alpha_helix_parameters,
    larmor_frequency,
    # v5.1扩展
    reynolds_number,
    sound_speed_laplace,
    earth_surface_gravity,
    chsh_quantum_bound,
    schwarzschild_radius,
)

__all__ = [
    # 版本
    "__version__",
    # 高层API
    "check_helix", "check_alldim", "check_adiabatic",
    "check_gradient_b_field", "check_uniform_b_field",
    "electron_benchmark", "theorem_status", "proven_theorems", "open_problems",
    # 几何
    "helix_curvature_torsion", "alldim_helix_curvatures",
    "frenet_from_trajectory", "curvature_2d", "torsion_3d",
    # 洛伦兹力
    "LorentzSimulator", "MagneticField", "UniformB", "GradientB",
    # 审计
    "ValidationStatus", "TheoremRecord", "THEOREMS",
    "honesty_statement", "audit_report",
    # 大统一力方程
    "grand_force", "ForceComponents", "mass_velocity_relation",
    "energy_momentum_relation", "rest_energy", "rest_momentum",
    # 核力场
    "nuclear_field", "nuclear_potential", "nuclear_force_range",
    "infer_nuclear_coupling", "nuclear_to_gravity_ratio",
    # 人工场设计
    "artificial_gravity_field", "required_dBdt_for_gravity",
    "solenoid_dBdt", "design_experiment", "ligo_comparison",
    "ArtificialFieldResult",
    # 弱力几何化
    "weak_force_range", "w_boson_mass_from_energy",
    "weak_momentum_uncertainty", "weak_interaction_open_issues",
    # 量子化起源
    "angular_momentum_from_helix", "quantized_angular_momentum",
    "electron_spin_helix", "compton_frequency", "compton_wavelength",
    "triad_quantization_connection", "quantization_open_issues",
    # 光速螺旋（v3.0）
    "light_speed_helix_params", "helix_curvature_torsion_light_speed",
    "check_light_speed_helix", "symbolic_proof_light_speed_helix",
    "electron_light_speed_helix", "alldim_light_speed_helix",
    "mass_geometric_origin", "rest_momentum_geometric", "quick_verify",
    "LightSpeedHelixResult",
    # 定理谱系（v3.0）
    "verify_TS1", "verify_TS2", "verify_TS3", "verify_TS4", "verify_TS5",
    "verify_TS6", "verify_TS7", "verify_TS8", "verify_TS9", "verify_TS10",
    "verify_TS11", "verify_TS12",
    "theorem_summary", "verify_all", "get_theorem", "logic_chain",
    "AXIOMS", "TheoremSystemRecord", "TheoremStatus",
    # GR弯曲时空推广（v4.0）
    "FrenetFrame4D", "SchwarzschildOrbit",
    "frenet_4d_from_trajectory", "schwarzschild_circular_orbit",
    "mercury_precession", "gravitational_redshift", "light_deflection",
    "shapiro_delay", "curved_spacetime_helix", "gr_classical_tests_summary",
    # 人工场实验深化（v4.0）
    "ArtificialFieldDeepResult", "artificial_field_equation",
    "total_efficiency", "nominal_gravity", "actual_gravity", "estimate_snr",
    "design_experiment_deep", "parameter_scan", "ligo_comparison_deep",
    "experimental_roadmap", "observable_predictions", "falsification_criteria",
    # 强相互作用精确描述（v4.0）
    "NuclearPotentialResult", "strong_force_range", "nuclear_coupling_constant",
    "strong_to_gravity_ratio", "yukawa_potential", "strong_nuclear_potential",
    "nuclear_well_depth", "nuclear_well_position", "deuteron_D_state_probability",
    "weizsaecker_binding_energy", "binding_energy_examples",
    "qcd_beta_function", "asymptotic_freedom_scale",
    # 粒子物理质量谱与混合角（v4.0）
    "ParticleHelixParams", "MASSES", "CKM", "PMNS",
    "mass_to_helix_radius", "helix_radius_to_mass", "particle_helix_params",
    "mass_ratio_verification", "ckm_mixing_angles", "pmns_mixing_angles",
    "ckm_pmns_comparison", "neutrino_mass_seesaw", "neutrino_oscillation_params",
    "yukawa_coupling_from_radius", "mass_hierarchy_explanation",
    # 量子引力深入（v4.0）
    "BlackHoleThermo", "planck_scale", "spacetime_quantization",
    "graviton_double_helix", "black_hole_thermodynamics", "solar_mass_black_hole",
    "black_hole_entropy_helix", "holographic_principle", "black_hole_laws",
    "information_paradox", "string_lqg_comparison", "quantum_gravity_open_problems",
    # 宇宙学深入（v4.0）
    "CosmicEvolution", "cosmological_constant_problem", "inflation_helix",
    "cosmic_age_calculation", "cosmic_evolution_summary", "cosmic_stages",
    "cmb_acoustic_peaks", "cmb_polarization", "dark_matter_candidates",
    "cosmological_parameters", "cosmological_puzzles", "cosmology_open_problems",
    # D1-D20深化方向（v5.0）
    "DIRECTIONS", "deep_directions_summary", "get_direction",
    "deep_directions_honesty",
    "qcd_beta_coefficients", "wimp_cross_section", "dd_planck_scale",
    "artificial_field_efficiency", "mass_from_helix_radius", "uncertainty_product",
    "universe_age_estimate", "quadrupole_radiation_power", "pmns_oscillation_probability",
    "higgs_parameters", "dd_weizsaecker_binding_energy", "bcs_gap_energy",
    "hydrogen_energy_level", "boltzmann_distribution", "photon_energy",
    "plasma_frequency", "frenet_curvature_torsion", "verlet_single_step",
    "alpha_helix_parameters", "larmor_frequency",
    # D1-D25扩展（v5.1）
    "EXTENDED_DIRECTIONS", "deep_directions_summary_extended",
    "get_direction_extended", "deep_directions_honesty_extended",
    "reynolds_number", "sound_speed_laplace", "earth_surface_gravity",
    "chsh_quantum_bound", "schwarzschild_radius",
    # 子模块
    "constants", "geometry", "lorentz", "triad", "provenance", "export",
    "grand_unification", "nuclear", "artificial_field", "weak_force", "quantization",
    "light_speed_helix", "theorem_system",
    "curved_spacetime", "artificial_field_deep", "strong_force",
    "particle_masses", "quantum_gravity_deep", "cosmology_deep",
    "deep_directions",
]
