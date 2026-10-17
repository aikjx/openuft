# 来料全文：HST 论文框架（PAPER_FRAMEWORK）

> 来源：用户来料（2026-10-17）。本文件为**正本留档**。英文原文一字未改。
> 内容：三篇候选论文标题、目标期刊表、Paper I（基础）章节大纲与摘要。
> 机器复核见：`判定_TUFT-r96-HST螺旋空间理论体系_全维审计_2026-10-17.md` G 段。

---

# Helical Space Theory (HST): Paper Framework

## Suggested Title Options

1. **"Electromagnetic Wave Propagation in Helical Coordinates: Dispersion, Chiral Splitting, and Effective Mass"**
2. **"Helical Space Theory: A Coordinate Framework for Chiral Wave Propagation and Zero-Energy Modes"**
3. **"Wave Equations in Helical Geometry: Exact Solutions, Topological Modes, and Experimental Signatures"**

## Target Journals

| Journal | Impact | Fit |
|---|---|---|
| Physical Review D | 5.0 | Field theory + gravitation |
| Classical and Quantum Gravity | 3.6 | Geometric framework |
| Annals of Physics | 2.2 | Comprehensive treatment |
| Journal of Mathematical Physics | 1.4 | Mathematical rigor |
| Physics Letters B | 4.4 | Concise letter format |

---

## Paper I: Foundation Paper (Classical + Quantum)

### Title: "Electromagnetic Wave Propagation in Helical Coordinates"

### Abstract (~200 words)

We introduce a helical coordinate system $(t, \rho, \chi, \zeta)$ for Minkowski spacetime, defined by $\varphi = \chi + \beta\zeta$ where $\beta$ is the helical twist rate. We derive the complete metric, prove that the Ricci tensor vanishes identically ($R_{\mu\nu}=0$), and establish that the helical transformation is a valid reparameterization of flat spacetime. We solve the scalar and vector wave equations exactly, finding that modes decompose into Bessel functions with a modified dispersion relation $\omega = c|k - \beta m|$. This leads to three key predictions: (1) chiral frequency splitting $\Delta\omega = 2c\beta$ between co-rotating and counter-rotating modes, (2) effective photon mass generation $m_{\text{eff}} \neq 0$ for modes with nonzero angular momentum, and (3) zero-energy modes at $k = \beta m$ with topological character. We verify all predictions numerically using FDTD simulations and derive experimental bounds from CMB polarization ($\beta < 6 \times 10^{-29}$ m$^{-1}$). We discuss connections to Kaluza-Klein theory, string theory $B$-fields, and the Standard Model Extension.

### Section Outline

**1. Introduction** (2 pages)
- Motivation: helical structures in nature (DNA, chiral crystals, OAM beams)
- Prior work: helical waveguides, twisted fibers, chiral media
- This work: systematic coordinate framework from first principles

**2. Helical Geometry** (3 pages)
- 2.1 Coordinate transformation and metric
- 2.2 Christoffel symbols (5 independent nonzero)
- 2.3 Curvature: proof that $R_{\mu\nu} = 0$
- 2.4 Volume element and causal structure

**3. Geodesics and Particle Motion** (3 pages)
- 3.1 Conserved quantities: $E$, $\ell$, $P$
- 3.2 Null geodesics: complete classification (6 cases)
- 3.3 Laboratory frame velocities
- 3.4 Frenet-Serret correspondence

**4. Wave Equations** (4 pages)
- 4.1 Scalar wave equation → Bessel equation
- 4.2 Dispersion relation $\omega = c|k - \beta m|$
- 4.3 Maxwell equations in helical coordinates
- 4.4 Polarization and gauge conditions

**5. Quantum Field Theory** (3 pages)
- 5.1 Canonical quantization
- 5.2 Effective mass generation
- 5.3 Chiral splitting $\Delta\omega = 2c\beta$
- 5.4 Zero-energy modes and topology

**6. Dirac Equation and Fermions** (2 pages)
- 6.1 Tetrad and spin connection
- 6.2 Modified Dirac equation
- 6.3 Spin-helix coupling

**7. Connections to Known Theories** (3 pages)
- 7.1 Kaluza-Klein: helical compactification
- 7.2 String theory: NS-NS $B$-field correspondence
- 7.3 SME: Carroll-Field-Jackiw coefficient
- 7.4 Axion electrodynamics

**8. Experimental Constraints** (2 pages)
- 8.1 CMB polarization bound
- 8.2 Laboratory tests
- 8.3 Proposed experiments

**9. Discussion and Conclusions** (1 page)

**Appendices:**
- A: Christoffel symbols derivation
- B: Ricci tensor calculation
- C: Numerical verification details

### Key Equations (for figures)

1. **Metric:** $ds^2 = -c^2dt^2 + d\rho^2 + \rho^2d\chi^2 + 2\beta\rho^2d\chi d\zeta + (1+\beta^2\rho^2)d\zeta^2$

2. **Dispersion:** $\omega = c|k - \beta m|$

3. **Chiral Splitting:** $\Delta\omega = 2c\beta$

4. **Effective Mass:** $m_{\text{eff}}^2 c^4 = -2\hbar c^2\beta m p_z + \hbar^2 c^2(\beta^2 m^2 + K^2)$

5. **Zero Mode:** $\Phi_{\text{zero}} = A\rho^{|m|}e^{im\varphi}$

---

## Paper II: Cosmological Applications

### Title: "Helical Cosmology: Phase Transitions, Dark Energy, and CMB Signatures"

### Key Sections

1. $\beta$ as a dynamical field
2. Helical phase transition and Kibble mechanism
3. Gravitational wave signature
4. Dark energy from $\beta$ potential
5. CMB polarization predictions

---

## Paper III: Experimental Proposal

### Title: "Proposed Measurement of Chiral Frequency Splitting in Orbital Angular Momentum Beams"

### Key Sections

1. Experimental design (OAM interferometer)
2. Sensitivity analysis
3. Noise budget
4. Expected signal for $\beta$ values
5. Systematic error analysis

---

## Numerical Verification Summary

All predictions verified computationally:

| Test | Method | Result | Error |
|---|---|---|---|
| $R_{\mu\nu} = 0$ | Direct computation | PASS | $< 10^{-15}$ |
| $\omega = c\|k-\beta m\|$ | FDTD + FFT | PASS | $< 5\%$ |
| $\Delta\omega = 2c\beta$ | Analytical | PASS | $< 10^{-10}$ |
| Zero mode | FDTD | PASS | $< 10\%$ |
| Bessel radial | Analytical | PASS | exact |
| $m_{\text{eff}}$ | Analytical | PASS | exact |
| Geodesic $\|v\| = c$ | ODE integration | PASS | $< 10^{-6}$ |
| Conservation laws | ODE integration | PASS | $< 10^{-10}$ |

### Code Repository Structure

```
hst_verification/
├── helical_wave_sim.py    # Main verification code
├── fig1_dispersion.png    # Dispersion relation plots
├── fig2_fdtd_verification.png  # FDTD results
├── fig3_chiral_splitting.png   # Chiral splitting
├── fig4_bessel_modes.png      # Radial modes
├── fig5_effective_mass.png    # Effective mass
└── fig6_geodesics.png         # Geodesic orbits
```

---

## Theorem Chain Summary

```
Axiom 1 (Helical structure) + Axiom 2 (Co-moving simplicity)
    │
    ├── Theorem 1.1: det(g) independent of β
    ├── Theorem 1.2: R_μν = 0 (flatness)
    └── Theorem 1.3: 5 independent Christoffel symbols
         │
         ├── Theorem 2.1: V_eff = ℓ²/(2ρ²)
         ├── Theorem 3.1: ω = c|k - βm|
         ├── Theorem 4.1: Δω = 2cβ (chiral splitting)
         ├── Theorem 4.2: m_eff formula
         ├── Theorem 5.1: ΔE_spin = 2ℏcβ
         ├── Theorem 10.1: P, CP violation
         ├── Theorem 11.1: Zero mode ρ^|m| e^{imφ}
         ├── Theorem 13.1: String B-field correspondence
         ├── Theorem 15.1: KK helical compactification
         ├── Theorem 15.3: Axion electrodynamics
         └── Theorem 15.4: SME CFJ coefficient
              │
              └── Experimental bound: β < 6×10⁻²⁹ m⁻¹
```

---

## Key Novel Contributions

1. **First complete derivation** of the helical metric's geometric properties (Christoffel, Ricci, Einstein tensors) with proof of flatness
2. **Exact solution** of Maxwell equations in helical coordinates
3. **Discovery** of chiral frequency splitting as a universal constant $\Delta\omega = 2c\beta$
4. **Identification** of zero-energy modes with topological character
5. **Systematic mapping** to KK theory, string theory, SME, and axion electrodynamics
6. **Comprehensive experimental constraints** from CMB to laboratory scales
7. **Numerical verification** of all key predictions via FDTD simulation

---

## Timeline Estimate

| Phase | Duration | Milestone |
|---|---|---|
| Paper I draft | 4 weeks | Complete manuscript |
| Peer feedback | 2 weeks | Internal review |
| Revisions | 2 weeks | Final draft |
| Submission | 1 week | To Phys. Rev. D |
| Paper II | 8 weeks | Follow-up |
| Paper III | 12 weeks | Experimental proposal |

---

*Framework prepared for Helical Space Theory (HST) project.*
*Last updated: 2026-10-13*
