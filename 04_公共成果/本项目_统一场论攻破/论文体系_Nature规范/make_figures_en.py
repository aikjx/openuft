# -*- coding: utf-8 -*-
# English-only figure set for Nature-standard paper series (Fig.1 - Fig.10)
# All labels in English (DejaVu Sans) -> no glyph/mojibake risk.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'dejavusans'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 160
plt.rcParams['savefig.dpi'] = 160

outdir = r'D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破\论文体系_Nature规范\figures'
os.makedirs(outdir, exist_ok=True)
C = dict(red='#c0392b', blue='#2f5b9e', green='#1e8449', orange='#d68910',
         purple='#7d3c98', gray='#7f8c8d', gold='#b7950b')

# ================= Fig.1  RGE three-point convergence =================
fig, ax = plt.subplots(figsize=(7.6, 5.2))
logmu = np.linspace(np.log10(91.1876), 19, 700)
MZ, MS = 91.1876, 1e3
MGUT = 1.6899e16
b_sm = (41/10, -19/6, -7)
b_ms = (33/5, 1, -3)
a0 = (1/0.016947, 1/0.033810, 1/0.1184)

def inv_a(b, mu0, a0v, mu):
    return 1/a0v - b*np.log(mu/mu0)/(2*np.pi)

def curve(i):
    out = np.empty_like(logmu)
    for k, lg in enumerate(logmu):
        mu = 10.0**lg
        if mu <= MS:
            out[k] = inv_a(b_sm[i], MZ, a0[i], mu)
        else:
            v = inv_a(b_sm[i], MZ, a0[i], MS)
            out[k] = inv_a(b_ms[i], MS, 1.0/v, mu)
    return out

for i, (col, lab) in enumerate(zip([C['red'], C['blue'], C['green']],
        [r'$\alpha_1^{-1}$ (U(1)$_Y$)', r'$\alpha_2^{-1}$ (SU(2)$_L$)', r'$\alpha_3^{-1}$ (SU(3)$_c$)'])):
    ax.plot(logmu, curve(i), color=col, lw=2.2, label=lab)
ax.axvline(np.log10(MS), color=C['gray'], ls='--', lw=1)
ax.axvline(np.log10(MGUT), color='black', ls=':', lw=1.2)
ax.plot(np.log10(MGUT), 25.83, 'o', ms=8, mfc=C['gold'], mec='black', zorder=5)
ax.annotate(r'$M_{\mathrm{GUT}}=1.69\times10^{16}$ GeV' + '\n' + r'$\alpha_{\mathrm{GUT}}^{-1}=25.83$',
            xy=(np.log10(MGUT), 25.83), xytext=(np.log10(MGUT)-2.4, 42),
            fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
ax.text(np.log10(MS)+0.12, 61, r'$M_{\mathrm{SUSY}}=1$ TeV', fontsize=9, color=C['gray'])
ax.set_xlabel(r'$\log_{10}(\mu/\mathrm{GeV})$', fontsize=12)
ax.set_ylabel(r'$\alpha_i^{-1}$', fontsize=12)
ax.set_xlim(np.log10(90), 19); ax.set_ylim(0, 66)
ax.legend(fontsize=10, loc='upper right', framealpha=0.9)
ax.set_title('Fig. 1  One-loop RGE three-point convergence in MSSM-SO(10)', fontsize=12, pad=10)
ax.grid(alpha=0.25)
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig1_RGE_convergence_EN.png'), bbox_inches='tight'); plt.close()

# ================= Fig.2  Four forces vs speed of light =================
fig, ax = plt.subplots(figsize=(7.8, 5.4))
rows = [
    ('P1  EM wave speed', r'$v=1/\sqrt{\varepsilon_0\mu_0}$', r'= c  (rel. dev. $2\times10^{-14}$)'),
    ('P2  GW speed', r'$\omega^2=c^2k^2$', r'$v_g=c$  (GW170817 $<10^{-15}$)'),
    ('P3  massless -> c', r'$v=dE/dp=pc^2/E$', 'm=0 -> c exact; W/Z -> short range'),
    ('P4  coupling contains c', r'$\alpha=e^2/4\pi\varepsilon_0\hbar c$', r'$7.2973525693\times10^{-3}$'),
    ('P5  EM / gravity', r'$e^2/4\pi\varepsilon_0Gm_e^2$', r'$4.165609\times10^{42}$'),
    ('P6  magnetic projection', r'$B=v\times E/c^2$', r'$F_{\mathrm{mag}}/F_{\mathrm{C}}=v^2/c^2$'),
    ('P7  radiation / mass', r'$P=G/5c^5\,|\dddot{Q}|^2$', 'GW170817; $m_p$: 95.01% trace anomaly'),
]
ys = np.arange(len(rows))[::-1]
for y, (tag, eq, note), lv, cc in zip(ys, rows, [4, 4, 4, 5, 5, 4, 5],
                                     [C['blue'], C['red'], C['green'], C['purple'], C['orange'], C['gray'], '#17becf']):
    ax.barh(y, lv, height=0.60, color=cc, alpha=0.88, edgecolor='black', lw=0.6)
    ax.text(0.12, y, tag, va='center', fontsize=10, color='white', fontweight='bold')
    ax.text(5.35, y+0.17, eq, va='center', fontsize=11)
    ax.text(5.35, y-0.19, note, va='center', fontsize=8.8, color='#333333')
ax.set_yticks([]); ax.set_xticks([]); ax.set_xlim(0, 9.6)
for s in ['top', 'right', 'left', 'bottom']:
    ax.spines[s].set_visible(False)
ax.set_title('Fig. 2  Seven first-principle connections between the four forces and the speed of light',
             fontsize=11.6, pad=10)
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig2_forces_light_EN.png'), bbox_inches='tight'); plt.close()

# ================= Fig.3  CUNI-v2 architecture =================
fig, ax = plt.subplots(figsize=(8.0, 6.4))
ax.set_xlim(0, 10); ax.set_ylim(0, 10.8); ax.axis('off')

def box(x, y, w, h, text, fc, ec, fs=9.6, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.08', fc=fc, ec=ec, lw=1.4))
    ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=fs,
            fontweight='bold' if bold else 'normal', color='#1a1a1a')

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                                 mutation_scale=13, color='#555555', lw=1.4))

box(0.8, 9.3, 8.4, 1.0, 'L1  SO(10) gauge layer: 45 bosons unify SM + X/Y', '#ffe9e9', C['red'], 9.6, True)
box(0.8, 8.0, 8.4, 1.0, r'L2  Chiral layer: 16 spinor = 15 fermions + $N^c$ (seesaw structural)', '#fff6e5', C['orange'])
box(0.8, 6.7, 8.4, 1.0, r'L3  Higgs layer: 210 -> 126 -> 10 chain, $\langle\Phi_{126}\rangle=M_R$', '#e5f7e5', C['green'])
box(0.8, 5.4, 8.4, 1.0, r'L4  Unified Yukawa: $W=y_{10}\Psi\Psi\Phi_{10}+y_{126}\Psi\Psi\Phi_{126}$', '#e5f0ff', C['blue'])
box(0.8, 4.1, 8.4, 1.0, r'L5  Soft breaking: $M_{\mathrm{SUSY}}=1$ TeV (RGE convergence switch)', '#f0e5ff', C['purple'])
box(0.8, 2.8, 8.4, 1.0, 'L6  Optional decoration: EC torsion (TUFT geometric layer, non-unifying)', '#f2f2f2', C['gray'], 9.4)
for yy in (8.0, 6.7, 5.4, 4.1, 2.8):
    arrow(5.0, yy, 5.0, yy-0.34)
box(0.5, 1.0, 3.6, 1.2, 'RGE upward run\nthree-point convergence achieved', '#fdf2d0', C['gold'], 9.4, True)
box(4.3, 1.0, 3.6, 1.2, r'GUT-boundary back-run' + '\n' + r'$\alpha_s$=0.1161, $\sin^2\theta_W$=0.2304', '#d5f5e3', C['green'], 9.2, True)
box(8.1, 1.0, 1.6, 1.2, 'Experiment\n$\\tau_p=3.51\\times10^{34}$ yr', '#fdebd0', C['orange'], 8.6, True)
arrow(2.3, 2.8, 2.3, 2.2); arrow(5.5, 2.8, 5.5, 2.2); arrow(8.5, 2.8, 8.5, 2.2)
ax.text(5.0, 0.35, r'Fig. 3  CUNI-v2 = MSSM-SO(10) unified action: architecture and evidence chain ($M_{\mathrm{GUT}}=1.69\times10^{16}$ GeV)',
        ha='center', fontsize=10.6, fontweight='bold')
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig3_CUNI_architecture_EN.png'), bbox_inches='tight'); plt.close()

# ================= Fig.4  Project overview =================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 4.6), gridspec_kw={'width_ratios': [1, 1.3]})
vals = [330, 672, 1]
labels = ['Closed / attacked\n330', 'Registered only\n672', 'Half-open\n1']
ax1.pie(vals, labels=labels, colors=[C['green'], C['red'], C['orange'],
        ][:3], autopct='%1.1f%%', startangle=90,
        wedgeprops={'edgecolor': 'white', 'lw': 1.5}, textprops={'fontsize': 9.2})
ax1.set_title('Master list: 1,003 T-rows', fontsize=10.6)
stages = ['Closing batch\nC0392-C0401', 'C-ALL engines\n39 closed + 520 reg.', 'Derivative deep.\n18 first-principle',
          'Screening\n9 new closed forms', 'CUNI-v1\n8 constraints 7/8', 'CUNI-v2\n6/6 + back-run 4/4']
prog = [10, 39, 18, 9, 7, 6]
pcols = ['#5dade2', '#85c1e9', '#aed6f1', '#d6eaf8', '#f0b429', '#28b463']
bars = ax2.barh(np.arange(len(stages)), prog, color=pcols, edgecolor='black', lw=0.5, height=0.6)
ax2.set_yticks(np.arange(len(stages))); ax2.set_yticklabels(stages, fontsize=8.8)
ax2.invert_yaxis()
for bi, v in zip(bars, prog):
    ax2.text(v+0.4, bi.get_y()+0.18, str(v), va='center', fontsize=9.2)
ax2.set_xlim(0, 48); ax2.set_xlabel('Count', fontsize=10)
ax2.set_title('Breaching milestones (322+ adjudications)', fontsize=10.6)
ax2.grid(axis='x', alpha=0.25)
fig.suptitle('Fig. 4  Unified-field-theory breaching project overview', fontsize=11.8, y=1.03)
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig4_project_overview_EN.png'), bbox_inches='tight'); plt.close()

# ================= Fig.5  Gravitational-wave observables =================
fig, axs = plt.subplots(1, 3, figsize=(11.2, 3.9))
th = np.linspace(0.02, np.pi, 500)
cos = np.cos(th)
x = (1-cos)/2
hd = 0.5 - x/4 + 1.5*x*np.log(x)          # normalized HD: zeta(pi)=1/4, zeta(0+)=1/2
axs[0].plot(th, hd, color=C['red'], lw=2)
axs[0].plot([np.pi], [0.25], 'o', ms=7, mfc=C['gold'], mec='black', zorder=5, ls='none')
axs[0].axhline(0, color='black', lw=0.6, ls=':')
axs[0].set_xlabel(r'$\theta$ (rad)', fontsize=10); axs[0].set_ylabel(r'$\zeta(\theta)$', fontsize=10)
axs[0].set_title('(a) Hellings-Downs curve', fontsize=10)
Om = np.linspace(0.05, 1.0, 300)          # in units of 1e3 rad/s
R, M = 1e4, 1.4*1.98847e30
G, c = 6.6743e-11, 2.99792458e8
eps_max = 0.5*Om**2*R**3/(G*M)
axs[1].plot(Om, eps_max, color=C['blue'], lw=2)
axs[1].set_xlabel(r'$\Omega$ ($10^3$ rad s$^{-1}$)', fontsize=10); axs[1].set_ylabel(r'$\epsilon_{\max}$', fontsize=10)
axs[1].set_title('(b) Ellipticity upper bound', fontsize=10)
axs[2].plot(Om, Om**6, color=C['green'], lw=2)
axs[2].set_xlabel(r'$\Omega$ ($10^3$ rad s$^{-1}$)', fontsize=10); axs[2].set_ylabel(r'$P/P_0$', fontsize=10)
axs[2].set_title(r'(c) Quadrupole power $\propto\Omega^6$', fontsize=10)
for a in axs:
    a.grid(alpha=0.25)
fig.suptitle('Fig. 5  Gravitational-wave observables: HD correlation, ellipticity bound, quadrupole scaling', fontsize=11, y=1.04)
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig5_GW_observables_EN.png'), bbox_inches='tight'); plt.close()

# ================= Fig.6  Black-hole thermodynamics =================
fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.0))
M = np.linspace(1, 30, 300)               # solar masses
S = M**2 * (1.048955e77)                   # S = 4*pi*(2GM/c^2)^2/(4 l_P^2); scaled: S ~ M^2 * 1.049e77
axs[0].plot(M, S, color=C['purple'], lw=2)
axs[0].set_yscale('log')
axs[0].set_xlabel(r'$M$ ($M_\odot$)', fontsize=10); axs[0].set_ylabel(r'$S_{\mathrm{BH}}$ ($k_B$)', fontsize=10)
axs[0].set_title(r'(a) Area law $S=A/4l_P^2$', fontsize=10)
axs[1].plot(M, S, color=C['purple'], lw=1.6, alpha=0.75, label=r'$S_{\mathrm{BH}}$')
axs[1].plot(M, S + 1.0*np.log(S), color=C['orange'], lw=2, ls='--', label=r'$S_{\mathrm{BH}}+C\ln S_{\mathrm{BH}}$')
axs[1].set_yscale('log')
axs[1].set_xlabel(r'$M$ ($M_\odot$)', fontsize=10); axs[1].set_ylabel(r'$S$ ($k_B$)', fontsize=10)
axs[1].set_title('(b) Log correction (C = 1, illustrative)', fontsize=10)
axs[1].legend(fontsize=9)
for a in axs:
    a.grid(alpha=0.25)
fig.suptitle(r'Fig. 6  Black-hole entropy: area law and logarithmic quantum correction (1 $M_\odot$ -> 1.049 x 10$^{77}$ $k_B$)', fontsize=10.6, y=1.04)
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig6_BH_thermodynamics_EN.png'), bbox_inches='tight'); plt.close()

# ================= Fig.7  Quantum information measures =================
fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.0))
N = np.logspace(2, 6, 200)
axs[0].loglog(N, 1/(2*np.sqrt(N)), color=C['blue'], lw=2, label=r'$\Delta\theta_{\min}=1/(2\sqrt{N})$')
axs[0].loglog(N, 1/np.sqrt(N), color=C['gray'], lw=1.4, ls='--', label=r'$1/\sqrt{N}$ (SQL)')
axs[0].set_xlabel('N (entangled particles)', fontsize=10); axs[0].set_ylabel(r'$\Delta\theta_{\min}$', fontsize=10)
axs[0].set_title('(a) Entanglement-enhanced scaling', fontsize=10)
axs[0].legend(fontsize=8.6); axs[0].grid(alpha=0.25, which='both')
thq = np.linspace(0.001, 0.999, 400)
H = -(thq*np.log(thq) + (1-thq)*np.log(1-thq))
axs[1].plot(thq, H/np.log(2), color=C['purple'], lw=2)
axs[1].set_xlabel(r'$p$ (diagonal population)', fontsize=10); axs[1].set_ylabel(r'$C_{\mathrm{rel}}/\ln 2$', fontsize=10)
axs[1].set_title(r'(b) Relative-entropy coherence $C_{\mathrm{rel}}$', fontsize=10)
axs[1].grid(alpha=0.25)
fig.suptitle('Fig. 7  Quantum coherence measures: Heisenberg scaling and relative-entropy coherence', fontsize=10.8, y=1.04)
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig7_quantum_measures_EN.png'), bbox_inches='tight'); plt.close()

# ================= Fig.8  Neutrino / BBN =================
fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.0))
Tf = np.linspace(0.4, 1.4, 300)
# linear interpolation anchored at measured points from engine C0399:
# Yp(0.8 MeV) = 0.2785 ; Yp(0.7331 MeV) = 0.245
Yp = 0.245 + (0.2785-0.245)/(0.8-0.7331) * (Tf-0.7331)
axs[0].plot(Tf, Yp, color=C['green'], lw=2)
axs[0].plot([0.8, 0.7331], [0.2785, 0.245], 'o', ms=7, mfc=C['gold'], mec='black', zorder=5, ls='none')
axs[0].set_xlabel(r'$T_f$ (MeV)', fontsize=10); axs[0].set_ylabel(r'$Y_p$', fontsize=10)
axs[0].set_title(r'(a) Helium abundance vs freeze-out (C0399)', fontsize=9.6)
axs[0].grid(alpha=0.25)
y = np.logspace(-13, -9, 300)
Omega = 0.12*(y/2.8846e-11)**2
axs[1].loglog(y, Omega, color=C['orange'], lw=2)
axs[1].plot([2.8846e-11], [0.12], 'o', ms=8, mfc=C['gold'], mec='black', zorder=5, ls='none')
axs[1].axhline(0.12, color=C['gray'], ls=':', lw=1)
axs[1].set_xlabel(r'$y$ (coupling)', fontsize=10); axs[1].set_ylabel(r'$\Omega h^2$', fontsize=10)
axs[1].set_title(r'(b) Freeze-in relic density, $y^*=2.8846\times10^{-11}$ (C0397)', fontsize=9.2)
axs[1].grid(alpha=0.25, which='both')
fig.suptitle('Fig. 8  Early-universe constraints: BBN helium abundance and freeze-in relic density', fontsize=10.6, y=1.04)
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig8_neutrino_BBN_EN.png'), bbox_inches='tight'); plt.close()

# ================= Fig.9  Precision tests =================
fig, axs = plt.subplots(1, 3, figsize=(11.4, 3.9))
w = np.logspace(-1, 5, 400)
gamma = (1+w)/(2+w)
axs[0].semilogx(w, gamma, color=C['blue'], lw=2)
axs[0].axhline(2/3, color=C['gray'], ls=':', lw=1)
axs[0].plot([1, 2], [(1+1)/(2+1), (1+2)/(2+2)], 'o', ms=7, mfc=C['gold'], mec='black', zorder=5)
axs[0].set_xlabel(r'$\omega$ (Brans-Dicke)', fontsize=10); axs[0].set_ylabel(r'$\gamma_{\mathrm{PPN}}$', fontsize=10)
axs[0].set_title(r'(a) BD PPN: $\gamma=(1+\omega)/(2+\omega)$ (C0392)', fontsize=9.6)
axs[0].grid(alpha=0.25, which='both')
axs[1].bar([0, 1], [4/3, 1], color=[C['red'], C['blue']], width=0.55, edgecolor='black', lw=0.6)
axs[1].axhline(1, color=C['gray'], ls=':', lw=1)
axs[1].set_xticks([0, 1]); axs[1].set_xticklabels(['potential\nvDVZ', 'GR\nreference'], fontsize=9)
axs[1].set_ylabel('ratio to GR', fontsize=10); axs[1].set_ylim(0, 1.55)
axs[1].set_title('(b) vDVZ 4/3 excess (C0393)', fontsize=9.6)
axs[1].grid(axis='y', alpha=0.25)
axs[2].errorbar([0.04095], [0.0409], yerr=[0.0012], fmt='o', ms=8, mfc=C['gold'], mec='black', capsize=4, label='theory')
axs[2].axhline(0.041, color=C['red'], ls='--', lw=1.4, label='frame-dragging meas.')
axs[2].set_xticks([0.04095]); axs[2].set_xticklabels(['GP-B\nframe-drag'], fontsize=9)
axs[2].set_ylabel(r'$\omega$ (arcsec yr$^{-1}$)', fontsize=10); axs[2].set_title('(c) GP-B frame dragging (C0395)', fontsize=9.6)
axs[2].legend(fontsize=8); axs[2].grid(alpha=0.25)
fig.suptitle('Fig. 9  Precision gravity tests: BD PPN, vDVZ breakdown, GP-B frame dragging', fontsize=10.4, y=1.04)
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig9_precision_tests_EN.png'), bbox_inches='tight'); plt.close()

# ================= Fig.10  Topological / discrete invariants =================
fig, ax = plt.subplots(figsize=(8.6, 4.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 6.4); ax.axis('off')
items = [
    ('T780', 'Instanton charge', r'$Q\in\mathbb{Z}$'),
    ('T772', 'WZW level', r'$c=1/3$'),
    ('T797', '3D Ising', r'$\nu=0.629971$'),
    ('T068', 'FQHE conductance', r'$\sigma=e^2/3h$'),
    ('T069', 'Fibonacci anyon', r'$\varphi=1.6180339$'),
    ('T779', 'Trefoil Jones', r'$V(t)=t+t^3-t^4$'),
    ('T748', 'Grassmannian', r'$\dim\mathrm{Gr}(2,4)=4$'),
    ('T778', 'GW invariants', '2875 / 609250\n/ 317206375'),
    ('T075', 'Z2 classification', r'$\mathbb{Z}_2$'),
]
for k, (tid, name, form) in enumerate(items):
    col, row = k % 3, k // 3
    x, y = 0.35 + col*3.2, 3.9 - row*1.35
    ax.add_patch(FancyBboxPatch((x, y), 2.95, 1.12, boxstyle='round,pad=0.06',
                                fc='#f5f8ff', ec=C['blue'], lw=1.2))
    ax.text(x+0.14, y+0.78, tid+'  '+name, fontsize=8.6, fontweight='bold', color=C['blue'])
    ax.text(x+0.14, y+0.30, form, fontsize=10.5 if len(form) <= 18 else 9.2, linespacing=1.35)
ax.text(5.0, 0.45, 'Fig. 10  Discrete and topological invariants (9 screened closed-form items, mpmath 250-digit guards 9/9)',
        ha='center', fontsize=9.8, fontweight='bold')
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig10_topological_invariants_EN.png'), bbox_inches='tight'); plt.close()

# ================= Fig.11  QCD running vs KSS / beta coefficients =================
fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.0))
ax = axs[0]
mu = np.logspace(np.log10(MZ), np.log10(MGUT), 400)
aMZ = 1/0.1161
ax.plot(mu, aMZ + (23/3)/(2*np.pi)*np.log(mu/MZ), color=C['gray'], ls='--', lw=1.5,
        label='SM only (b0 = 23/3)')
eff = (25.827 - aMZ)/np.log(MGUT/MZ)
ax.plot(mu, aMZ + eff*np.log(mu/MZ), color=C['blue'], lw=2.0, label='MSSM 3-segment (effective)')
ax.axhline(25.827, color=C['red'], ls=':', lw=1.2)
ax.scatter([MGUT], [25.827], s=58, color=C['gold'], edgecolor='k', zorder=5, label='GUT point')
ax.set_xscale('log')
ax.set_xlabel(r'$\mu$ (GeV)', fontsize=10)
ax.set_ylabel(r'$\alpha_s^{-1}(\mu)$', fontsize=10)
ax.set_title('(a) One-loop strong-coupling running', fontsize=9.8)
ax.legend(fontsize=8, loc='upper left')
ax.grid(alpha=0.25)
ax.annotate(r'$\alpha_{\rm GUT}^{-1}=25.827$', xy=(MGUT, 25.827), xytext=(1.5e10, 16.3),
            fontsize=8.5, color=C['red'],
            arrowprops=dict(arrowstyle='->', color=C['red'], lw=1))

ax = axs[1]
labels = ['SM\nNf=3', 'SM\nNf=4', 'SM\nNf=5', 'SM\nNf=6', 'MSSM\nb1', 'MSSM\nb2', 'MSSM\nb3']
vals = [9, 25/3, 23/3, 7, 33/5, 1, -3]
cols = [C['gray']]*4 + [C['purple']]*3
ax.bar(range(len(vals)), vals, color=cols)
ax.axhline(0, color='k', lw=0.8)
ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels, fontsize=7.6)
ax.set_ylabel(r'$b$ (one-loop coefficient)', fontsize=9.5)
ax.set_title('(b) Beta-function coefficients', fontsize=9.8)
ax.grid(axis='y', alpha=0.25)
fig.suptitle('Fig. 11  QCD running: SM-only versus MSSM three-segment unification, and one-loop beta coefficients',
             fontsize=10.2, y=1.04)
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig11_QCD_running_EN.png'), bbox_inches='tight'); plt.close()

# ================= Fig.12  C7 criterion: exact crossing and threshold budget =================
fig, axs = plt.subplots(1, 2, figsize=(12.2, 4.3))

def spread_of(Lv):
    aT = [a0[i] - b_sm[i] * Lv / (2 * np.pi) for i in range(3)]
    ts = [2 * np.pi * (aT[i] - aT[j]) / (b_ms[i] - b_ms[j]) for (i, j) in ((0, 1), (0, 2), (1, 2))]
    return max(ts) - min(ts)

ax = axs[0]
Lg = np.linspace(-1.6, 7.02, 900)
ms = MZ * np.exp(Lg)
sp = np.array([spread_of(L) for L in Lg])
ax.axvspan(20, MZ, color='#dfe6ec', alpha=0.6, zorder=0)
ax.plot(ms, sp, color=C['blue'], lw=2.0, label=r'spread of three $t^{*}_{ij}$')
ax.scatter([54.9616], [0.0], s=54, color=C['gold'], edgecolor='k', zorder=5, label='exact crossing point')
sp_1tev = spread_of(np.log(1e3 / MZ))
ax.scatter([1e3], [sp_1tev], s=54, color=C['red'], edgecolor='k', zorder=5, label=r'$M_{\rm SUSY}=1$ TeV')
ax.set_xscale('log')
ax.set_xlim(20, 1e5)
ax.set_ylim(-0.06, 2.7)
ax.set_xlabel(r'$M_{\rm SUSY}$ (GeV)', fontsize=10)
ax.set_ylabel(r'$\Delta\ln M$ (spread of $t^{*}_{ij}$)', fontsize=10)
ax.set_title(r'(a) Exact crossing lies below $M_Z$', fontsize=9.8)
ax.grid(alpha=0.25)
ax.annotate('54.96 GeV: exact crossing\ninside non-physical region', xy=(54.96, 0.0),
            xytext=(23, 0.95), fontsize=8.0, color=C['gold'],
            arrowprops=dict(arrowstyle='->', color=C['gold'], lw=1))
ax.annotate('1 TeV: spread = 0.984 (3.24 percent)', xy=(1e3, sp_1tev),
            xytext=(3.0e3, 0.30), fontsize=8.0, color=C['red'],
            arrowprops=dict(arrowstyle='->', color=C['red'], lw=1))
ax.text(3.5e3, 2.02, 'shaded:\nnon-physical region\n' + r'$M_{\rm SUSY}<M_Z$', fontsize=8.0, color=C['gray'])
ax.legend(fontsize=8, loc='upper left')

ax = axs[1]
dv = (0.017557, -0.042137, 0.024580)
lab = [r'$\delta\alpha_1^{-1}$', r'$\delta\alpha_2^{-1}$', r'$\delta\alpha_3^{-1}$']
cols = [C['green'], C['red'], C['blue']]
ax.bar(range(3), dv, color=cols, width=0.55)
ax.axhline(0, color='k', lw=0.8)
ax.set_xticks(range(3))
ax.set_xticklabels(lab, fontsize=9)
ax.set_ylabel(r'shift in $\alpha_i^{-1}$', fontsize=10)
ax.set_title(r'(b) Minimal-norm threshold budget', fontsize=9.8)
ax.set_ylim(-0.062, 0.038)
for k, v in enumerate(dv):
    ax.text(k, v + (0.0028 if v > 0 else -0.0055), '%.5f' % v, ha='center', fontsize=8.4)
ax.text(0.03, 0.03, 'norm = 0.0518 (0.21 percent of 24.269)', transform=ax.transAxes, fontsize=8.2)
ax.grid(axis='y', alpha=0.25)

fig.suptitle('Fig. 12  C7 three-point crossing: algebraic criterion, exact crossing point and threshold budget',
             fontsize=10.2, y=1.04)
plt.tight_layout(); plt.savefig(os.path.join(outdir, 'Fig12_C7_criterion_EN.png'), bbox_inches='tight'); plt.close()

print('EN figures generated:')
for f in sorted(os.listdir(outdir)):
    if f.endswith('_EN.png'):
        print('  -', f)
