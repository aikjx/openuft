# J115 地球两极重力与垂直原理（机读）

- 体积：卷 136 · 第 93 轮 · J115 · 2026-11-13
- 判决：PASS
- 硬闸：98/98
- 记分板：0/6 不变；本册关闭 OPEN 0 条

## 直接回答

- 两极**不是**更轻，而是更重：γ_pole − γ_equator = 5185.96 mGal（+0.5302%）。
- 分项账（相对 GM/a²）：极 +6603.55(1/r²) − 3225.41(J2) = +3378.15 mGal；
  赤道 +1591.18(J2) − 3391.57(离心) = −1800.39 mGal；差 +5178.53 mGal（J2 截断），
  精确闭式读数 +5185.96 mGal。
- 物理拆法：纯引力差 1794.39 mGal（+0.182%）+ 赤道离心 3391.57 mGal = 5185.96 mGal。
- 所以「两极更轻」的直觉来源是 1/r²（+6604 mGal），但被 J2 在极点扣掉 3225 mGal；
  赤道被离心扣掉 3392 mGal，因此净差仍是两极更重。

## 关键读数

- gamma_equator: 9.7803253359
- gamma_pole: 9.8321849378
- pole_minus_equator_m_s2: 0.051859601900
- pole_minus_equator_mGal: 5185.960190
- relative_gap_percent: 0.530244139
- gamma_45_deg: 9.806197769344
- gamma_45_deg_grs80: 9.806199202496
- somigliana_k: 0.001931852646396240
- flattening: 0.003352810664747481
- polar_radius_m: 6356752.314245
- eccentricity_squared: 0.006694379990141317
- g_reference_sphere: 9.798285479187
- ledger_mGal:
  - pole_1_over_r2: 6603.5513
  - pole_J2: -3225.4052
  - equator_J2: 1591.1828
  - equator_centrifugal: -3391.5706
  - J2_only_difference: 5178.5339
  - exact_difference: 5185.9602
  - truncation: 7.4263
- pure_gravity_pole_over_equator_percent: 0.18208
- centrifugal_m_s2: 0.033915705977
- centrifugal_mGal: 3391.5706
- pure_gravity_gap_mGal: 1794.3896
- max_latitude_reduction_arcmin: 11.545458
- phi_star_deg: 45.096212151
- surface_speed_m_s: 465.101085
- surface_speed_over_c: 1.551410E-06
- light_speed_helix_radius_m: 4.111187E+12
- light_speed_helix_radius_AU: 27.481585
- light_speed_helix_over_R: 6.445748E+05
- required_omega_rad_s: 47.003139
- required_omega_rev_s: 7.480782
- required_centrifugal_m_s2: 1.409119E+10
- required_centrifugal_over_g: 1.440769E+09
- kappa_equator: 1.578423E-07
- kappa_pole: 1.562599E-07
- curvature_route_overshoot_factor: 3.8388
- pendulum_freq_gain_ppm: 2647.7155
- pendulum_period_ratio: 0.997359276387
- free_air_gradient_mGal_per_m: 0.310357
- latitude_gradient_mGal_per_arcmin: 1.508526
- dgamma_domega: -930.202170
- one_percent_omega_effect_mGal: -67.8314
- pendulum_5_vs_49_min_per_day: 2.1367
- scoreboards:
  - one_equation: 0/6
  - validated: 0
  - four_force_gut: 0
  - unique_C3: L_EW
  - open_items: 8
  - l4_open: 18
  - closed_by_this_volume: 0

## 垂直原理：证了什么、没证什么

- 已证（精确）：轴上切向重力恒零、离心恒零、铅垂线与自转轴重合；两极大地纬度=地心纬度。
- 最大纬度差 11.545458 arcmin（在 tanφ=a/b 处）。
- 未证：三力在任意时刻/任意地点两两垂直；ROOT-3F 已判为条件性运动学恒等式。

## 两条通道的否证

- v=c：ωR/c = 1.551410E-06；光速螺旋半径 27.481585 AU = 6.445748E+05 R_E；强行地表 v=c 需 ω=47.003139 rad/s。
- κ/τ：子午线为平面曲线 τ≡0；螺旋字典退化为等曲率圆，对纬度零变化。

## 硬闸明细

- [PASS] A-anchor ROOT-3F verdict present + needle | 04_公共成果/本项目_全维自洽与归一化/整理_三力垂直原理_ROOT-3F条件性正交与保持判据_2026-11-02.md sha=f381fe236b085937
- [PASS] A-anchor J92 light-speed helix present + needle | 07_统一场方程/114_第73轮_光速螺旋与垂直原理检验_J92_图谱轴值零命中与节点正文11处前史记录_精确螺旋与两归一化_诱导扭率不同构b2_Z未定与三代未解释_2026-11-08.md sha=f56509ffdc7dcc63
- [PASS] A-anchor legacy IGF script present + needle | 03_跨体系研究/物理领域/地球物理/verify_geophysics_deep.py sha=22f82e51b5e118b9
- [PASS] A-anchor core formula table present | 07_统一场方程/openuft_49_1000_core_formulae.md sha=91de667ed16ef1d0
- [PASS] A05 novelty: core formula table has no normal-gravity entry | no Somigliana / no 9.78 / no 重力 in 1000-formula table
- [PASS] A06 J92 records the light-speed helix as already falsified | falsified flag + omega·rho condition at anchored bytes
- [PASS] P01 pole normal gravity exceeds equatorial (poles are heavier) | GP-GE = 0.051859601900 m/s^2 = 5185.960190 mGal
- [PASS] P02 the pole-equator gap reads 5185.96 mGal | 5185.96019 mGal
- [PASS] P03 relative size of the gap | 0.530244139 %
- [PASS] P04 the premise 'poles are lighter' is falsified: sign(GP-GE) = +1 | sign = +1, so the premise is FALSE
- [PASS] P05 the equatorial centrifugal term supplies 3391.6 mGal of the 5186.0 mGal gap | pure-gravity contrast 1794.3896 mGal + centrifugal 3391.5706 mGal = 5185.9602 mGal
- [PASS] P06 a spherical Earth with the same radius would differ by centrifugal only | sphere: equator lighter by 3391.5706 mGal
- [PASS] P-PC1 flipping the measured sign would break the invariant | detected
- [PASS] S01 gamma(0) reproduces the WGS84 equatorial value | 9.780325335900000000000000000000
- [PASS] S02 gamma(90) reproduces the WGS84 polar value | 9.832184937800000000000000000000
- [PASS] S03 gamma(45) reproduces the WGS84 closed-form reading | 9.806197769343780
- [PASS] S04 normal gravity is strictly increasing in latitude (1-degree grid) | 91 points, monotone
- [PASS] S05 dgamma/dphi vanishes at the equator | 0.0000000000
- [PASS] S06 dgamma/dphi vanishes at the pole | 0.0000000000
- [PASS] S07 analytic derivative matches central differences at five latitudes | max relative error 0.000000
- [PASS] S08 the grid minimum is the equator value and the maximum the pole value | min=gamma(0) max=gamma(90)
- [PASS] S09 no interior critical point: the derivative is strictly positive inside | min dgamma = 0.001801892185
- [PASS] S10 GRS80 and WGS84 differ at 45 deg only at the 1e-6 level | |GRS80-WGS84|(45) = 0.000001433152 m/s^2
- [PASS] S11 the legacy international gravity formula stays within 0.25 mGal | max |IGF-Somigliana| = 0.2108 mGal
- [PASS] S12 all 91 latitude values lie inside [gamma_eq, gamma_pole] | 91/91
- [PASS] S-PC1 swapping the two endpoint values breaks gamma(90) by 1400 mGal | detected
- [PASS] D01 reference sphere gravity GM/a^2 | 9.798285479187
- [PASS] D02 naive 1/r^2 at the polar radius GM/b^2 | 9.864320992254
- [PASS] D03 oblateness 1/r^2 term contributes +6603.6 mGal at the pole | 6603.551 mGal
- [PASS] D04 J2 subtracts 3225.4 mGal at the pole | -3225.405 mGal
- [PASS] D05 J2 adds 1591.2 mGal at the equator | 1591.183 mGal
- [PASS] D06 centrifugal subtracts 3391.6 mGal at the equator | -3391.571 mGal
- [PASS] D07 the three-term mGal ledger closes to 5178.5 mGal (J2-only truncation) | 5178.534 mGal
- [PASS] D08 truncation error of the J2-only ledger | exact - J2-only = 7.426 mGal (0.143 %)
- [PASS] D09 pure gravity (oblateness + J2) is still +0.18% at the pole | relative 0.1821 %
- [PASS] D10 Clairaut relation J2 ~ (2/3)f - (1/3)m holds to 1% | J2=1.082626680E-03 vs Clairaut=1.085278274E-03, m=3.449786507E-03
- [PASS] D-PC1 dropping the centrifugal term misses by 3391.6 mGal | detected
- [PASS] V01 tangential gravity on the axis is exactly zero for any r | g_theta(axis) = 0.0000000000
- [PASS] V02 centrifugal force on the axis is exactly zero | omega^2 r sin^2(0) = 0
- [PASS] V03 effective field on the axis is exactly axial | no theta-hat / phi-hat component
- [PASS] V04 geodetic minus geocentric latitude vanishes at the equator and in the polar limit | delta(0)=0.000000000000 ; delta(89.999)=1.176e-07 rad
- [PASS] V05 the maximum latitude reduction sits at tan(phi) = a/b | argmax 45.096212151 deg vs atan(a/b) 45.096212151 deg
- [PASS] V06 maximum reduction of latitude is 2 atan(a/b) - pi/2 = 11.545 arcmin | 11.5455 arcmin
- [PASS] V07 at 45 deg the reduction is 11.54 arcmin and strictly below the maximum | 11.5454 arcmin
- [PASS] V08 the polar surface normal is exactly the rotation axis | n(pole) = (0,0,1)
- [PASS] V09 the three-force configuration at the pole is degenerate (centrifugal = 0) | orthogonality there is trivial, not a dynamical law
- [PASS] V10 ROOT-3F already judged the general three-force claim conditional | verdict string + codim-3 argument anchored
- [PASS] V-PC1 off-axis perturbation grows linearly (not identically zero) | ratio(2e-6 / 1e-6) = 1.999999999996
- [PASS] X01 equatorial surface speed | 465.101085 m/s
- [PASS] X02 the surface is not light-speed: omega R / c | 1.551410e-06
- [PASS] X03 omega*rho=c defines rho_c = c/omega | 4.111187e+12 m
- [PASS] X04 the light-speed helix radius in AU | 27.4816 AU
- [PASS] X05 how many Earth radii fit in the light-speed radius | 6.4457e+05
- [PASS] X06 forcing v=c at the surface requires omega = c/R | 47.003139 rad/s = 7.4808 rev/s
- [PASS] X07 that required omega exceeds Earth's by 6.45e5 | 6.4457e+05
- [PASS] X08 the forced centrifugal term is 1.44e9 g | 1.4091e+10 m/s^2 = 1.4408e+09 g
- [PASS] X09 the two light-speed conditions are equivalent only at b = 0 | omega*sqrt(rho^2+b^2)=c gives omega*rho = c/sqrt(1+(b/rho)^2)
- [PASS] X10 no helix pitch can make the surface light-speed at Earth's omega | b/rho_c = 0.999999999999
- [PASS] X11 the v=c channel cannot generate 5186 mGal; it overshoots by 1e9 | acceleration ratio 1.441e+09
- [PASS] X-PC1 assuming rho_c = R is rejected | |c/omega - R| = 4.111e+12 m
- [PASS] K01 meridian curvature at the equator | 1.578423e-07 1/m
- [PASS] K02 meridian curvature at the pole | 1.562599e-07 1/m
- [PASS] K03 curvature ratio equator/pole | 1.010126259
- [PASS] K04 meridional radius of curvature at both ends | 6335439.327 m / 6399593.626 m
- [PASS] K05 gravity ratio pole/equator | 1.005302441
- [PASS] K06 a naive g ~ 1/R^2 curvature route overshoots by 3.84x | predicted +2.0355 %, observed +0.5302 %, factor 3.8388
- [PASS] K07 the terrestrial meridian is a planar closed curve: torsion identically zero | planar ellipse => tau = 0 exactly
- [PASS] K08 helix with tau=0 degenerates to a circle of constant curvature | tau=0 => b=0 => kappa=1/rho constant
- [PASS] K09 the kappa/tau dictionary is undefined on the meridian (tau=0) | kappa/tau diverges
- [PASS] K10 a 1-D helix cannot determine a field on the 2-D geoid surface | dim(curve)=1 < dim(surface)=2; the latitude profile is not supplied
- [PASS] K-PC1 an ellipse is not a helix: tau=0 while a pitched helix has tau>0 | ellipse tau=0; helix tau=b/(rho^2+b^2)>0 for b>0
- [PASS] W01 omega and the rounded sidereal day agree to 1e-7 | 2pi/T_sid = 7.292115855307e-05 rad/s vs defining 7.292115000e-05
- [PASS] W02 dgamma/domega at the equator | -930.202170 m/s per rad/s
- [PASS] W03 a 1% spin-up lowers equatorial gravity by 67.8 mGal | -67.831 mGal
- [PASS] W04 pendulum frequency is 2647.7 ppm higher at the pole | 2647.7155 ppm
- [PASS] W05 pendulum period is shorter at the pole | 0.997359276387
- [PASS] W06 free-air gradient at the pole is 0.3104 mGal/m | 3.103573e-06 s^-2 = 0.310357 mGal/m
- [PASS] W07 latitude gradient at 45 deg is 1.5085 mGal per arcminute | 1.508526 mGal/arcmin (= 90.512 mGal/deg)
- [PASS] W08 a 5-deg vs 49-deg pendulum comparison gives ~2.1 min/day | 2.1367 min/day
- [PASS] W09 dgamma/dGM at the equator | 2.462164e-14 s^2/m^2
- [PASS] W-PC1 centrifugal response is quadratic in omega, not linear | half omega => quarter centrifugal
- [PASS] B01 authoritative scoreboard is 0/6 | 0/6
- [PASS] B02 validated systems = 0 | validated=0
- [PASS] B03 correct four-force GUT equations = 0 | 0
- [PASS] B04 unique C3-level true unification is electroweak L_EW | L_EW (2 forces)
- [PASS] B05 ledger OPEN items stay at 8 | 8 OPEN
- [PASS] B06 L4 physics layer stays at 18 OPEN | 18 OPEN
- [PASS] B07 this volume closes zero OPEN items | closed=0
- [PASS] B08 classical geodesy is not UFT evidence | red line
- [PASS] B-PC1 a 6/6 scoreboard would be caught | detected
- [PASS] H01 the honest claim block passes its own validator | issues: none
- [PASS] H02 a corrupted claim block is caught on three counts | issues: 3
- [PASS] H03 the reproduction is a model-level replay, not measurement-level | stated in scope
- [PASS] H04 local gravity anomalies are outside the scope | EGM high-degree terms not used; anomalies ~±100 mGal not modelled
- [PASS] H05 verticality is proved only on the axis (axial symmetry), not globally | two non-theorems listed
- [PASS] H06 the kappa/tau no-go is a dimension/degeneracy argument | 1-D curve vs 2-D surface; tau=0 degeneration
- [PASS] H07 no new physics and no OPEN item closed | 0 new physics, 0 closed
- [PASS] H08 mathematical reproduction is not physical validation of UFT | red line

> Reproducing the normal gravity field is not unifying forces; an exact axial theorem is not a global dynamical law.
