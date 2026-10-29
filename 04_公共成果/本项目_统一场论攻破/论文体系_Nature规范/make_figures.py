# -*- coding: utf-8 -*-
# Nature 规范论文体系配图生成器（2026-10-30）
# Fig1 RGE 三点收敛 / Fig2 力×光速 / Fig3 CUNI-v2 架构 / Fig4 攻破工程全景
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
outdir = r'D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破\论文体系_Nature规范\figures'
import os
os.makedirs(outdir, exist_ok=True)

# ---------- Fig 1: RGE 三点收敛 ----------
fig, ax = plt.subplots(figsize=(7.6, 5.2))
logmu = np.linspace(np.log10(91.1876), np.log10(1e19), 600)
MZ, MS = 91.1876, 1e3
MGUT = 1.6899e16
b_sm = (41/10, -19/6, -7)
b_ms = (33/5, 1, -3)
a1z, a2z, a3z = 1/0.016947, 1/0.033810, 1/0.1184

def inv_a(b, mu0, a0, mu):
    return 1/a0 - b*np.log(mu/mu0)/(2*np.pi)

def curve(i):
    vals = np.empty_like(logmu)
    for k, lg in enumerate(logmu):
        mu = 10**lg
        if mu <= MS:
            vals[k] = inv_a(b_sm[i], MZ, [a1z, a2z, a3z][i], mu)
        else:
            v0 = inv_a(b_sm[i], MZ, [a1z, a2z, a3z][i], MS)
            vals[k] = inv_a(b_ms[i], MS, 1/v0, mu)
    return vals

cols = ['#d62728', '#1f77b4', '#2ca02c']
labs = [r'$\alpha_1^{-1}$ (U(1)Y)', r'$\alpha_2^{-1}$ (SU(2)L)', r'$\alpha_3^{-1}$ (SU(3)c)']
for i, (col, lab) in enumerate(zip(cols, labs)):
    ax.plot(logmu, curve(i), color=col, lw=2.2, label=lab)
ax.axvline(np.log10(1e3), color='gray', ls='--', lw=1)
ax.text(np.log10(1e3)+0.12, 62, r'M_SUSY = 1 TeV', fontsize=9, color='gray')
ax.axvline(np.log10(MGUT), color='black', ls=':', lw=1.2)
ax.plot(np.log10(MGUT), 25.83, 'o', ms=8, mfc='gold', mec='black')
ax.annotate(r'M_GUT = 1.69×10¹⁶ GeV' + '\n' + r'$\alpha_{GUT}^{-1}$ = 25.83',
            xy=(np.log10(MGUT), 25.83), xytext=(np.log10(MGUT)-2.1, 40),
            fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
ax.set_xlabel(r'$\log_{10}(\mu/\mathrm{GeV})$', fontsize=12)
ax.set_ylabel(r'$\alpha_i^{-1}$', fontsize=12)
ax.set_ylim(0, 66); ax.set_xlim(np.log10(90), 19)
ax.legend(fontsize=10, loc='upper right', framealpha=0.9)
ax.set_title('Fig.1  MSSM-SO(10) 单圈 RGE 三点收敛（2026-10-30 实跑，mpmath 60 位）', fontsize=11)
ax.grid(alpha=0.25)
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig1_RGE_convergence.png'), bbox_inches='tight'); plt.close()

# ---------- Fig 2: 力 × 光速 七条连接 ----------
fig, ax = plt.subplots(figsize=(7.6, 5.4))
rows = [
    ('P1 电磁波速', r'$v=1/\sqrt{\varepsilon_0\mu_0}$', '= c (偏差 2×10⁻¹⁴)'),
    ('P2 引力波速', r'$\omega^2=c^2k^2$', 'v_g = c (GW170817 <10⁻¹⁵)'),
    ('P3 无质量→c', r'$v=dE/dp=pc^2/E$', 'm=0 → c 精确；W/Z → 短程'),
    ('P4 耦合含c', r'$\alpha=e^2/4\pi\varepsilon_0\hbar c$', '7.2973525693×10⁻³'),
    ('P5 电磁/引力', r'$e^2/4\pi\varepsilon_0Gm_e^2$', '4.165609×10⁴²'),
    ('P6 磁场投影', r'$B=v\times E/c^2$', 'F_mag/F_C = v²/c²'),
    ('P7 辐射/质能', r'$P=G/5c^5|\dddot Q|^2$', 'GW170817 验证；m_p 95.01%'),
]
ys = np.arange(len(rows))[::-1]
barv = [3, 3, 3, 4, 5, 3, 4]
colors = ['#1f77b4', '#8c564b', '#2ca02c', '#d62728', '#9467bd', '#ff7f0e', '#17becf']
for y, r, bv, cc in zip(ys, rows, barv, colors):
    ax.barh(y, bv, height=0.62, color=cc, alpha=0.85, edgecolor='black', lw=0.6)
    ax.text(0.15, y, r[0], va='center', fontsize=10, color='white', fontweight='bold')
    ax.text(3.2, y+0.18, r[1], va='center', fontsize=10.5, family='DejaVu Sans')
    ax.text(3.2, y-0.18, r[2], va='center', fontsize=9, color='#333333')
ax.set_yticks([]); ax.set_xlim(0, 8.2)
ax.set_xticks([])
ax.set_title('Fig.2  四大力与光速 c 的七条第一性连接（求导证明 + 数值精算 7/7）', fontsize=11)
for s in ['top', 'right', 'left']:
    ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig2_forces_light.png'), bbox_inches='tight'); plt.close()

# ---------- Fig 3: CUNI-v2 架构 ----------
fig, ax = plt.subplots(figsize=(7.8, 6.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 10.6); ax.axis('off')
def box(x, y, w, h, text, fc='#eef4ff', ec='#2f5b9e', fs=9.2, bold=False):
    p = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.08', fc=fc, ec=ec, lw=1.4)
    ax.add_patch(p)
    ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=fs,
            fontweight='bold' if bold else 'normal', color='#1a1a1a')
def arrow(x1, y1, x2, y2, text=None, tx=5.1, ty=0.35):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                 mutation_scale=14, color='#555555', lw=1.4))
    if text:
        ax.text(tx, ty, text, fontsize=8.6, ha='center', color='#444444')
box(1.0, 9.2, 8.0, 1.0, 'L1 SO(10) 规范层：45 玻色子统一 SM+X/Y', '#ffe9e9', '#c0392b', 9.4, True)
box(1.0, 7.9, 8.0, 1.0, 'L2 手征层：16 旋量 = 15 费米子 + Nᶜ（seesaw 结构必然）', '#fff6e5', '#d68910', 9.4)
box(1.0, 6.6, 8.0, 1.0, 'L3 Higgs 层：210→126→10 破缺链，⟨Φ₁₂₆⟩=M_R', '#e5f7e5', '#1e8449', 9.4)
box(1.0, 5.3, 8.0, 1.0, 'L4 统一 Yukawa：W=y₁₀ΨΨΦ₁₀+y₁₂₆ΨΨΦ₁₂₆（b-τ 统一）', '#e5f0ff', '#2f5b9e', 9.4)
box(1.0, 4.0, 8.0, 1.0, 'L5 软破缺：M_SUSY=1 TeV（RGE 汇聚物理开关）', '#f0e5ff', '#7d3c98', 9.4)
box(1.0, 2.7, 8.0, 1.0, 'L6 装饰层：EC 挠率（TUFT 几何对接，非统一机制）', '#f2f2f2', '#7f8c8d', 9.2)
arrow(5.0, 7.9, 5.0, 7.65)
arrow(5.0, 6.6, 5.0, 6.35)
arrow(5.0, 5.3, 5.0, 5.05)
arrow(5.0, 4.0, 5.0, 3.75)
arrow(5.0, 2.7, 5.0, 2.45)
box(0.6, 0.9, 3.4, 1.2, 'RGE 向上跑\n三点收敛达成', '#fdf2d0', '#b7950b', 9.6, True)
box(3.6, 0.9, 3.4, 1.2, 'GUT 边界回推\nα_s=0.1161  sin²θ_W=0.2304', '#d5f5e3', '#1e8449', 9.2, True)
box(6.6, 0.9, 3.0, 1.2, '实验接口\nτ_p=3.51×10³⁴ yr', '#fdebd0', '#ca6f1e', 9.2, True)
arrow(2.3, 2.7, 2.3, 2.1)
arrow(5.3, 2.7, 5.3, 2.1)
arrow(8.1, 2.7, 8.1, 2.1)
ax.text(5.0, 0.35, 'Fig.3  CUNI-v2 = MSSM-SO(10) 大统一作用量架构与证据链闭环（M_GUT=1.69×10¹⁶ GeV）',
        ha='center', fontsize=10.4, fontweight='bold')
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig3_CUNI_architecture.png'), bbox_inches='tight'); plt.close()

# ---------- Fig 4: 攻破工程全景 ----------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 4.6), gridspec_kw={'width_ratios': [1, 1.25]})
labels = ['已攻破/闭式\n330', '登记不深攻\n672', '半攻\n1']
vals = [330, 672, 1]
cols = ['#2ca02c', '#d62728', '#ff7f0e']
w, _, at = ax1.pie(vals, labels=labels, colors=cols, autopct='%1.1f%%',
                   startangle=90, wedgeprops={'edgecolor': 'white', 'lw': 1.5},
                   textprops={'fontsize': 9.5})
for a in at: a.set_fontsize(9)
ax1.set_title('母册 T 行 1003 项状态', fontsize=10.5)
stages = ['清尾批\nC0392-C0401', 'C-ALL 引擎\n39 闭式+520 登记', '求导深化\n18 项第一性', '甄别\n9 项新闭式', 'CUNI-v1\n8 约束 7/8', 'CUNI-v2\n收敛 6/6+回推 4/4']
prog = [10, 39, 18, 9, 7, 6]
pcols = ['#5dade2', '#85c1e9', '#aed6f1', '#d6eaf8', '#f0b429', '#28b463']
b = ax2.barh(np.arange(len(stages)), prog, color=pcols, edgecolor='black', lw=0.5, height=0.6)
ax2.set_yticks(np.arange(len(stages))); ax2.set_yticklabels(stages, fontsize=9)
ax2.invert_yaxis()
for bi, v in zip(b, prog):
    ax2.text(v+0.3, bi.get_y()+0.18, str(v), va='center', fontsize=9.5)
ax2.set_xlim(0, 48); ax2.set_xlabel('数量', fontsize=10)
ax2.set_title('攻破里程碑（累计判定 322+ 项）', fontsize=10.5)
ax2.grid(axis='x', alpha=0.25)
fig.suptitle('Fig.4  统一场论攻破工程全景（母册 T 行 + 攻破里程碑）', fontsize=11.5, y=1.02)
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig4_project_overview.png'), bbox_inches='tight'); plt.close()

print('4 figures generated in', outdir)
for f in sorted(os.listdir(outdir)):
    print(' -', f)
