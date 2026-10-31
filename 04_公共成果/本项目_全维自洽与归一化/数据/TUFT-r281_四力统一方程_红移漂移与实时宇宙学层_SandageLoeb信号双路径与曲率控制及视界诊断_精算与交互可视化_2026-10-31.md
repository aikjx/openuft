# TUFT-r281 · 数据册（引擎自动生成）
- 判决串：`R281-REDSHIFT-DRIFT-DUAL-PATH-OK-ZERO-AND-Q0-SLOPE-OK-SIGN-FLIP-ZCROSS-OK-DV-CM-S-DECADE-OK-R278-HZ-CROSS-OK-MILNE-ZERO-DRIFT-CONTROL-OK-EDS-ALGEBRA-OK-DSITTER-OK-DT-CONVERGENCE-OK-SPECTRAL-RESOLUTION-BOUNDARY-WZ-CURVATURE-PRIOR-BOUNDARY-VERDICT-STANDARD-REALTIME-COSMOLOGY-NO-NEW-THEORY`
- 条目：10（PASS 6 / FAIL 0 / BOUNDARY 2 / INFO 2）· 守卫 6/6 · 控制组 4/4

## 条目
- **H01 INFO** 判定：红移漂移 = 标准 ΛCDM 的实时宇宙学复现，不是新理论——dz/dt0=(1+z)H0−H(z) 是 Sandage(1962)/Loeb(1998) 的纯几何预言；本卷只做机器复现与判别力验证
- **H02 PASS** 漂移双路径互印——闭式 vs 沿光锥数值微分：6 点 max rel=1.335e-05；z=1 时 drift=+14.391×10⁻¹²/yr
- **H03 PASS** z=0 零点与斜率 −q0——drift(0)=0；z→0 斜率=0.526867 vs −q0=0.526867（rel 6.856e-07）（q0=-0.526867<0 ⇒ 近处正漂移）
- **H04 PASS** 符号翻转红移 z_cross——z_cross=1.913290（(1+z)=E(z)）；下方正、上方负——ΛCDM 特有；EdS 恒负、Milne 恒零（见控制组）
- **H05 PASS** 十年漂移速度 Δv 量级——Δv(z=1)=+2.157、Δv(z=4)=-5.525、Δv(z=5)=-7.925 cm/s ⇒ 与 Sandage–Loeb 的 cm/s/decade 量级一致
- **H06 PASS** 与 r278 的 D_H→H(z) 跨卷互印——用 r278 的 D_H(z=1,2,3) 反推 H(z)，与本卷同一 E(z) 的 max rel=9.345e-07
- **H07 PASS** 曲率判别力：Milne 精确零漂移——Ωk=1 ⇒ E=1+z ⇒ 漂移恒零（控制组 C1，max|drift|/H0 < 1e−14）；⇒ 漂移是真实可判别的曲率/暗能量探针，不是恒等式
- **H08 BOUNDARY** 实测需 10⁻⁹ 级 Δz 高分辨率光谱——Δz(10 yr) ~ 10⁻⁹–10⁻¹⁰，需 ELT/CODEX 级（~cm/s 速度精度、20–30 年基线）；当前任何巡天未达 ⇒ 本卷只做理论预言与自洽验证
- **H09 BOUNDARY** w(z) 演化与 Ωk 先验不在本卷——CPL w(z)=w0+wa z/(1+z) 的漂移曲线（含 w 导数项）需外部 SN Ia/BAO 数据；弯曲宇宙仅作控制组，主结果固定平坦 ΛCDM
- **H10 INFO** 判决：观测量层下一级增量，统一仍无新物理——背景(r237)+扰动(r254)+声学(r256)+视界(r260)+非线性(r274)+距离(r278)+实时漂移(本卷) 全部是已知物理；r229/r267 的新颖性与完成度判定不变

## 守卫
- **G1 OK** 漂移双路径互印（闭式 vs 沿光锥数值微分）——6 个红移点 max rel=1.335e-05（阈值 1e−4；数值路径步长 1000 yr）
- **G2 OK** z=0 零点与斜率 = −q0——drift(0)=0；斜率 0.526867 vs −q0=0.526867，rel=6.856e-07
- **G3 OK** 符号翻转红移 z_cross（ΛCDM 特有）——z_cross=1.913290、残差 0.000e+00；下方为正、上方为负 ⇒ q0<0 的真实翻转
- **G4 OK** Δv 量级落在 Sandage–Loeb cm/s/decade——|Δv(z=4)|=5.52 cm/s ∈ [3,12]；|Δv(z=5)|=7.93 cm/s ∈ [3,15]
- **G5 OK** r278 的 D_H 反推 H(z) 互印——3 个红移点 max rel=9.345e-07（阈值 1e−3；r278 D_H 四舍五入到 0.01 Mpc）
- **G6 OK** 交互 HTML 生成且自含——已生成 D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\四力统一方程_红移漂移与实时宇宙学层可视化_2026-10-31.html（27661 B），零外部 URL、JSON 已铸入

## 控制组
- **C1 OK** Milne 空宇宙精确零漂移（曲率判别力）——Ωm=0,ΩΛ=0,Ωr=0,Ωk=1 ⇒ E=1+z ⇒ (1+z)−E≡0；5 点 max|drift|/H0=0.000e+00
- **C2 OK** EdS 漂移代数恒等（(1+z)−(1+z)^{3/2} = −(1+z)(√(1+z)−1)）——4 点 max rel=6.587e-16（机器零）
- **C3 OK** de Sitter 漂移 = H0 z 恒等——4 点 max rel=0.000e+00
- **C4 OK** 数值微分步长收敛（500/1000/2000 yr）——z=2 时三个步长的漂移 max rel=7.486e-06（阈值 1e−3）
