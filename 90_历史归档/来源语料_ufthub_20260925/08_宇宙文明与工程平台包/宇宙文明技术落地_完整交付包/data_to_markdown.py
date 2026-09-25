#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将JSON数据转化为格式化Markdown数据表和分析
"""
import json
import os

DATA_DIR = "/home/user/.super_doubao/super-doubao-runtime/workspace/cosmic_civilization_book/data"
OUTPUT_DIR = "/home/user/.super_doubao/super-doubao-runtime/workspace/cosmic_civilization_book/chapters"

def load_data(filename):
    with open(os.path.join(DATA_DIR, filename), 'r') as f:
        return json.load(f)

def fmt_num(x, sig=6):
    """格式化数字为科学计数法或普通"""
    if x == 0:
        return "0"
    if abs(x) >= 1e6 or abs(x) < 1e-4:
        return f"{x:.{sig}e}"
    return f"{x:.{sig}g}"

def generate_table(data, columns, title, max_rows=200):
    """生成Markdown表格"""
    lines = []
    lines.append(f"### {title}")
    lines.append("")
    # 表头
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"]*len(columns)) + " |"
    lines.append(header)
    lines.append(separator)
    # 数据行 (采样，最多max_rows行)
    step = max(1, len(data) // max_rows)
    for i in range(0, len(data), step):
        row = data[i]
        values = []
        for col in columns:
            if col in row:
                values.append(fmt_num(row[col]))
            else:
                values.append("-")
        lines.append("| " + " | ".join(values) + " |")
    lines.append("")
    lines.append(f"*本表共 {len(data)} 条数据，以上为等间隔采样展示。*")
    lines.append("")
    return "\n".join(lines)

def generate_analysis(data, key_columns, title):
    """生成数据分析"""
    lines = []
    lines.append(f"### {title}")
    lines.append("")
    lines.append("**统计分析:**")
    lines.append("")
    for col in key_columns:
        values = [d[col] for d in data if col in d and isinstance(d[col], (int, float))]
        if values:
            vmin = min(values)
            vmax = max(values)
            vavg = sum(values)/len(values)
            lines.append(f"- **{col}**: 范围 [{fmt_num(vmin)}, {fmt_num(vmax)}], 平均值 {fmt_num(vavg)}")
    lines.append("")
    return "\n".join(lines)

# ============================================================
# 数据集1: 本体量子数n扫描
# ============================================================
print("生成数据集1 Markdown...")
data1 = load_data('01_n_scan.json')
md1 = []
md1.append("## 附录数据卷一：本体量子数 n 全维扫描")
md1.append("")
md1.append("本卷包含本体量子数 $n$ 从 $10^8$ 到 $10^{10}$ 的对数扫描数据，共1000个采样点。每个点计算对应的全域分形本征常数 $\delta_F=1/(2\\pi n)$、本体双曲角 $\beta=\mathrm{arcsinh}(\delta_F)$、万有引力常数理论值 $G_{\\text{theory}}$ 及其与CODATA 2022实验值的相对残差。")
md1.append("")
md1.append(generate_analysis(data1, ['n', 'delta_F', 'beta', 'G_theory', 'G_residual_pct'], "全局统计分析"))
md1.append(generate_table(data1, ['n', 'delta_F', 'beta', 'G_theory', 'G_residual_pct'], "本体量子数n扫描数据表 (采样100行)"))
with open(os.path.join(OUTPUT_DIR, 'data_volume_01_n_scan.md'), 'w') as f:
    f.write("\n".join(md1))

# ============================================================
# 数据集2: 动态分形维能量演化
# ============================================================
print("生成数据集2 Markdown...")
data2 = load_data('02_fractal_dimension_energy.json')
md2 = []
md2.append("## 附录数据卷二：动态分形维随能量尺度演化")
md2.append("")
md2.append("本卷包含动态分形维 $d_s=4-\sinh^2\\beta\\cdot\\kappa\\tau/c^2$ 随能量尺度从 $1\\,\\mathrm{eV}$ 到 $10^{19}\\,\\mathrm{GeV}$（普朗克尺度）的演化数据，共1000个能量采样点。数据展示了时空有效维数在高能下自动降维、消除紫外发散的核心机制。")
md2.append("")
md2.append(generate_analysis(data2, ['logE_eV', 'E_GeV', 'ratio', 'd_s'], "全局统计分析"))
md2.append(generate_table(data2, ['logE_eV', 'E_eV', 'E_GeV', 'ratio', 'd_s'], "动态分形维能量演化数据表 (采样100行)"))
with open(os.path.join(OUTPUT_DIR, 'data_volume_02_fractal_dim.md'), 'w') as f:
    f.write("\n".join(md2))

# ============================================================
# 数据集3: 引力-电磁互激效应
# ============================================================
print("生成数据集3 Markdown...")
data3 = load_data('03_gravity_em_coupling.json')
md3 = []
md3.append("## 附录数据卷三：引力-电磁互激效应全参数扫描")
md3.append("")
md3.append("本卷包含引力-电磁互激效应的二维参数扫描：磁场强度 $B$ 从 $1\\,\\mathrm{T}$ 到 $1000\\,\\mathrm{T}$，探测距离 $r$ 从 $0.01\\,\\mathrm{m}$ 到 $1\\,\\mathrm{m}$，共2500个参数组合。每个组合计算磁场能量、等效电磁质量、交叉耦合有效引力质量、引力扰动加速度及信噪比（假设探测器灵敏度 $10^{-20}\\,\\mathrm{m/s^2}$）。")
md3.append("")
md3.append(generate_analysis(data3, ['B_T', 'r_m', 'U_B_J', 'm_EM_kg', 'm_eff_kg', 'delta_g', 'SNR'], "全局统计分析"))
md3.append(generate_table(data3, ['B_T', 'r_m', 'U_B_J', 'm_EM_kg', 'm_eff_kg', 'delta_g', 'SNR'], "引力-电磁互激效应数据表 (采样150行)"))
with open(os.path.join(OUTPUT_DIR, 'data_volume_03_gravity_em.md'), 'w') as f:
    f.write("\n".join(md3))

# ============================================================
# 数据集4: 宇宙学红移演化
# ============================================================
print("生成数据集4 Markdown...")
data4 = load_data('04_cosmology_redshift.json')
md4 = []
md4.append("## 附录数据卷四：宇宙学参数红移演化")
md4.append("")
md4.append("本卷包含宇宙学参数随红移 $z$ 从 $0$ 到 $1100$（复合时期）的演化数据，共500个红移采样点。对比了标准$\\Lambda$CDM模型与本理论（含双曲修正项）的哈勃参数 $H(z)$，展示了哈勃张力的理论消解机制。")
md4.append("")
md4.append(generate_analysis(data4, ['z', 'H_z_lcdm', 'H_z_theory', 'correction', 'rho_m', 'rho_r', 'rho_L'], "全局统计分析"))
md4.append(generate_table(data4, ['z', 'a', 'H_z_lcdm', 'H_z_theory', 'correction', 'rho_m', 'rho_r', 'rho_L'], "宇宙学红移演化数据表 (采样100行)"))
with open(os.path.join(OUTPUT_DIR, 'data_volume_04_cosmology.md'), 'w') as f:
    f.write("\n".join(md4))

# ============================================================
# 数据集5: CKM参数扫描
# ============================================================
print("生成数据集5 Markdown...")
data5 = load_data('05_ckm_scan.json')
md5 = []
md5.append("## 附录数据卷五：CKM矩阵Wolfenstein参数扫描")
md5.append("")
md5.append("本卷包含CKM矩阵Wolfenstein参数 $(\lambda, A, \\bar{\\rho}, \\bar{\\eta})$ 的二维扫描：$\lambda$ 从 $0.220$ 到 $0.230$，$A$ 从 $0.78$ 到 $0.88$，共400个参数组合。每个组合计算CKM矩阵元 $V_{ud}, V_{us}, V_{ub}, V_{cs}, V_{cb}, V_{tb}$ 及第一行幺正性检验。")
md5.append("")
md5.append(generate_analysis(data5, ['lambda', 'A', 'Vud', 'Vus', 'Vub', 'Vcs', 'Vcb', 'Vtb', 'unitarity_row1'], "全局统计分析"))
md5.append(generate_table(data5, ['lambda', 'A', 'Vud', 'Vus', 'Vub', 'Vcs', 'Vcb', 'Vtb', 'unitarity_row1'], "CKM参数扫描数据表 (采样100行)"))
with open(os.path.join(OUTPUT_DIR, 'data_volume_05_ckm.md'), 'w') as f:
    f.write("\n".join(md5))

# ============================================================
# 数据集6: Koide关系扫描
# ============================================================
print("生成数据集6 Markdown...")
data6 = load_data('06_koide_scan.json')
md6 = []
md6.append("## 附录数据卷六：Koide质量关系参数扫描")
md6.append("")
md6.append("本卷包含三代轻子Koide质量关系的参数扫描：基准相位 $\\theta$ 从 $0.5$ 到 $0.9$ 弧度（约$28.6°$到$51.6°$），共100个采样点。每个点计算三代粒子质量 $m_1,m_2,m_3$、Koide比值 $Q=(m_1+m_2+m_3)/(\\sqrt{m_1}+\\sqrt{m_2}+\\sqrt{m_3})^2$ 及质量比。")
md6.append("")
md6.append(generate_analysis(data6, ['theta_deg', 'm1', 'm2', 'm3', 'koide_ratio', 'r12', 'r23'], "全局统计分析"))
md6.append(generate_table(data6, ['theta_rad', 'theta_deg', 'm1', 'm2', 'm3', 'koide_ratio', 'r12', 'r23'], "Koide关系扫描数据表 (全部100行)", max_rows=100))
with open(os.path.join(OUTPUT_DIR, 'data_volume_06_koide.md'), 'w') as f:
    f.write("\n".join(md6))

# ============================================================
# 数据集7: 引力推进器
# ============================================================
print("生成数据集7 Markdown...")
data7 = load_data('07_gravity_thruster.json')
md7 = []
md7.append("## 附录数据卷七：引力推进器技术参数扫描")
md7.append("")
md7.append("本卷包含基于引力-电磁互激效应的引力推进器技术参数扫描：功率从 $0.1\\,\\mathrm{MW}$ 到 $1000\\,\\mathrm{MW}$，频率从 $0.1\\,\\mathrm{GHz}$ 到 $100\\,\\mathrm{GHz}$，共1500个参数组合。每个组合计算电磁能量等效质量流、交叉耦合有效质量流、理论推力及推功比。")
md7.append("")
md7.append(generate_analysis(data7, ['power_MW', 'freq_GHz', 'mass_flow_kg_s', 'eff_mass_flow', 'thrust_N', 'thrust_per_power_N_W'], "全局统计分析"))
md7.append(generate_table(data7, ['power_MW', 'freq_GHz', 'mass_flow_kg_s', 'eff_mass_flow', 'thrust_N', 'thrust_per_power_N_W'], "引力推进器参数数据表 (采样150行)"))
with open(os.path.join(OUTPUT_DIR, 'data_volume_07_thruster.md'), 'w') as f:
    f.write("\n".join(md7))

# ============================================================
# 数据集8: 真空能提取
# ============================================================
print("生成数据集8 Markdown...")
data8 = load_data('08_vacuum_energy.json')
md8 = []
md8.append("## 附录数据卷八：真空能提取技术参数")
md8.append("")
md8.append("本卷包含基于分形余项真空能的提取技术参数扫描：提取体积从 $0.001\\,\\mathrm{m^3}$ 到 $1000\\,\\mathrm{m^3}$，提取效率从 $0.1\\%$ 到 $50\\%$，共1500个参数组合。每个组合计算真空总能量、可提取能量及功率（假设1秒提取周期）。")
md8.append("")
md8.append(generate_analysis(data8, ['volume_m3', 'efficiency', 'total_energy_J', 'extractable_J', 'power_W'], "全局统计分析"))
md8.append(generate_table(data8, ['volume_m3', 'efficiency', 'total_energy_J', 'extractable_J', 'power_W'], "真空能提取参数数据表 (采样150行)"))
with open(os.path.join(OUTPUT_DIR, 'data_volume_08_vacuum_energy.md'), 'w') as f:
    f.write("\n".join(md8))

# ============================================================
# 数据集9: 时空工程
# ============================================================
print("生成数据集9 Markdown...")
data9 = load_data('09_spacetime_engineering.json')
md9 = []
md9.append("## 附录数据卷九：时空曲率操控技术参数")
md9.append("")
md9.append("本卷包含时空工程（曲率操控）技术参数：集中能量从 $1\\,\\mathrm{J}$ 到 $10^{20}\\,\\mathrm{J}$，共50个能量采样点。每个点计算等效质量、Schwarzschild半径、时空曲率标量及度规扰动幅度。")
md9.append("")
md9.append(generate_analysis(data9, ['energy_J', 'mass_eq_kg', 'schwarzschild_radius_m', 'curvature_1_m2', 'metric_perturbation_h'], "全局统计分析"))
md9.append(generate_table(data9, ['energy_J', 'mass_eq_kg', 'schwarzschild_radius_m', 'curvature_1_m2', 'metric_perturbation_h'], "时空曲率操控参数数据表 (全部50行)", max_rows=50))
with open(os.path.join(OUTPUT_DIR, 'data_volume_09_spacetime.md'), 'w') as f:
    f.write("\n".join(md9))

# ============================================================
# 数据集10: 恒星工程
# ============================================================
print("生成数据集10 Markdown...")
data10 = load_data('10_stellar_engineering.json')
md10 = []
md10.append("## 附录数据卷十：恒星工程与戴森球参数")
md10.append("")
md10.append("本卷包含恒星工程（戴森球）技术参数：恒星质量从 $0.1$ 到 $100$ 太阳质量，共30个采样点。每个点计算恒星光度、半径、戴森球接收功率、可用功率（30%效率）及恒星主序寿命。")
md10.append("")
md10.append(generate_analysis(data10, ['star_mass_solar', 'luminosity_solar', 'radius_solar', 'dyson_power_W', 'usable_power_W', 'lifetime_years'], "全局统计分析"))
md10.append(generate_table(data10, ['star_mass_solar', 'luminosity_solar', 'radius_solar', 'dyson_power_W', 'usable_power_W', 'lifetime_s', 'lifetime_years'], "恒星工程参数数据表 (全部30行)", max_rows=30))
with open(os.path.join(OUTPUT_DIR, 'data_volume_10_stellar.md'), 'w') as f:
    f.write("\n".join(md10))

print("\n全部10个数据卷Markdown生成完成!")
print(f"输出目录: {OUTPUT_DIR}")
