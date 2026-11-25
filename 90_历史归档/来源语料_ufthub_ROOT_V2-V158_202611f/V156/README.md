# ROOT V156：光速流、平衡与束缚的可复算研究

## 结论边界
本包是数学审计、简化模型数值计算及公开常数基准对照，不是四力统一证明，也不是实验数据反演。只设 c=1；hbar、G 保留。代码中 C=299792458 仅用于 SI 输出转换。V155 历史包原样附入。

## 1. 求导：光速流的不变质量
度规 (-,+,+,+)。p_a=E_a(1,n_a)，|n_a|=1。M²=-P·P=2 sum_{a<b} E_a E_b (1-n_a·n_b)。两束等能流在夹角 0,90,180 度时 M/E=0,sqrt(2),2。此不变质量并不意味着束缚。对自由粒子 p 为真实四动量；对相互作用的子系统必须计入完整场和束缚应力的能量动量。

## 2. 证明：无迹应力的扩张障碍
对平直时空的完整、对称、守恒 T，有限 E 和有限 I=integral r² T00 d³x，假设加权边界项消失。积分分部得 I'=2 integral x_i T0i，I''=2 integral Tii。无迹 T 给出 sum Tii=T00，因此 I(t)=I(0)+I'(0)t+Et²。正能量时不能永远局域；周期/静态亦不可能。此证明不适用于曲率强烈、外加边界、非无迹相互作用或能量/二阶矩不有限的情形。并非否定一切电磁或引力束缚。自由光速流 Monte Carlo 采用 4096 个位置各放两条反向等能射线，共 8192，按解析自由流轨迹计算，非 Maxwell PDE 模拟。

## 3. 候选束缚：球对称集体坐标
V(R)=A/R+S R²+B R³。取 A>0，S,B>=0 且至少一个正。A 量纲 ML，S 为 M/L²，B 为 M/L³。V'=-A/R²+2SR+3BR²；乘 R² 后的零点函数单调增且由负转正，所以唯一 R*>0。V''(R*)=6S+12BR*>0。若仅 S>0，R*=(A/2S)^(1/3)；仅 B>0，R*=(A/3B)^(1/4)。无束缚 V 单调下降。对于绝热辐射 E_rad=A/R，P_rad=E_rad/(3 volume)；表面项 S=4πσ，体积项 B=(4π/3)ρ_vac。平衡是 P_rad=2σ/R+ρ_vac。该模型的系数来自假设，不是由螺旋推导。未检验形变、泄漏、材料微观结构或量子稳定性。

## 4. 数值仿真
归一化 L0、E0 均任意；不是设置 hbar 或 G=1。选三组 (A,S,B)=(3,0,1),(2,1,0),(5,1,1)，均故意使 R*=1；三种初始半径 0.7、1.2、1.5 倍 R*，初始径向动量 0。采用演示 Hamiltonian H=sqrt(m0²+p²)-m0+V(R)，m0=V(R*) 是附加惯性假设；Rdot=p/sqrt(m0²+p²)，pdot=-V'。DOP853、RK45 独立求解同一方程，检查守恒与一致性。它是单自由度模型，不是完整场论、也不证明真实粒子。小振荡频率 sqrt(V''/m0)。

## 5. 平行、垂直、发散与方向
稳态 n=(rhat+b zhat×rhat)/sqrt(1+b² sin²θ)，rho=sqrt(1+b² sin²θ)/r²（归一化总通量），J=rho n，Pi=rho n⊗n。赤道 f=-div Pi=(b²,-b,0)/(r³ sqrt(1+b²))，用中心差分验证 7 种 b、4 种 r。径向 b=0 时 f=0（源外自由流）；b≠0 时反作用径向向外，切向符号随 b 反号，f 的 r^-3 不是引力加速度的 r^-2。稳态纯径向正能量流若全空间无限延伸，其能量积分发散；吸收者的普通辐射压力沿出射方向，不是吸引力。这里的反作用需另一个系统维持流场，未推导真实物质耦合。

## 6. 与引力的连接（已知 GR）
弱场静态线性化 Einstein 方程给出 ∇²Φ=4πG(T00+ΣTii)。对完整静态孤立系统且边界项消失，Laue 条件 ∫Tij=0，故领先阶远场质量为总能量 E（忽略高阶自引力）。本模型的积分空间应力迹：辐射 +E_rad，张力膜 -2E_surface，真空 -3E_volume。平衡条件恰好令其和为零；活性质量 2E_rad-E_surface-2E_volume=E_total。若忽略束缚应力会错误地算出辐射为双倍质量。这个结论使用 GR，未由 ROOT 独立导出 G 或 Einstein 方程。
地球、月球使用 JPL DE440 GM 与平均半径近似，计算 g、潮汐特征值 (2,-1,-1)GM/r³、圆轨道速度周期及紧致度 2GM/(r c_SI²)。在 SI 下 GM/G 得到质量是反演，不是从微观运动预测。有限差分复核潮汐张量。不包含 J2、质量异常、潮汐外源、实际卫星观测和协方差。

## 7. 验证与未完成事项
- 9 个 unittest 测试方法（内含 181 个角度子案例、28 个通量组合、9 个振荡场景、5 个符号恒等式等；不是独立物理实验）。
- MICROSCOPE 2022 的 Ti/Pt 等效原理检验达到 10^-15 量级；任何新耦合需预测材料差异后才能对照，不直接排除所有 ROOT 模型。
- 四力统一、规范群、粒子谱、G/hbar/alpha 的独立推导、完整 3D 束缚 PDE 和真实观测拟合尚未完成。

## 8. 复算
Python 3.10+，安装 requirements.txt，运行 python run_all.py。results/ 存 CSV、JSON 和测试日志；figures/ 为生成图。验证静态文件：python verify.py。Windows/Linux 脚本提供，实际仅 Linux 测试。运行会覆盖 results/ 和 figures/，它们不纳入静态源码哈希（原始归档仍由 ZIP CRC 保护）。

## 参考资料
- Giulini, Laue's Theorem Revisited, https://arxiv.org/abs/1808.09320
- JPL Astrodynamic Parameters, https://ssd.jpl.nasa.gov/astro_par.html
- JPL satellite physical parameters, https://ssd.jpl.nasa.gov/sats/phys_par/
- NIST CODATA 2022, https://www.nist.gov/publications/codata-recommended-values-fundamental-physical-constants-2022
- MICROSCOPE 2022, https://doi.org/10.1103/PhysRevLett.129.121102
