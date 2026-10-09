# TUFT-MATH-PROOF-ADD-01 复Omega场渲染与全域审计报告（分支 2）

- 引擎：源码/TUFT-MATH-PROOF-ADD-01_复Omega场渲染与全域审计_2026-10-05.py
- 日期：2026-10-05
- 读数：7 guard —— PASS 7 / FAIL 0（退出码 0）

| PASS | b4_cos3theta_identity | max|rect - cos(3theta)| = 2.22e-16（机器精度） |
| PASS | angular_only_radial_degenerate | Omega(1,0.8)=(-0.0516,-0.0000) vs Omega(2,1.6)=(-0.0516,-0.0000)（径向不变） |
| PASS | magnitude_continuous_boundary | |Omega|(210°两侧) = 5.101e-17 / 3.537e-10（连续） |
| PASS | phase_discontinuity_N6 | phi(210°⁻)=0.0000, phi(210°⁺)=-0.2500, 跳变=-0.2500（幅度=phi0/2） |
| PASS | three_lobe_partition | |Omega|(240°)=0.1179, |Omega|(0°)=0.1179, |Omega|(120°)=0.1179（三正瓣均非零） |
| PASS | dimensionless | Omega = lambda*cos3theta*exp(i phi)，lambda 无量纲耦合 ⇒ 无量纲 |
| PASS | vector_field_azimuthal | d|Omega|/dr(沿射线) = 1.73e-15（径向梯度~0 ⇒ 流场纯方位角） |

### 渲染要点

1. **Omega 是纯角度场**（径向退化）：幅值 |Omega|=lambda|cos3theta| 沿每条射线恒定，
   与半径无关 ⇒ 渲染用极坐标玫瑰图（|cos3theta| 三瓣）最忠实。
2. **幅值三正瓣**：EM(0°±30)、Strong(120°±30)、Weak(240°±30)，边界为 cos3theta
   零点（30/90/150/210/270/330°）；负瓣区为 G。
3. **N6 相位不连续**：相位在弱域[210°,270°]内线性变化，跨 210°/270° 边界跳变 phi0/2
   （幅值连续但相位不连续）——与 ADD-01「相位连续✔」矛盾。
4. **矢量场 F=-grad|Omega| 纯方位角**：因幅值与半径无关，流场无径向分量，仅沿角向
   在三瓣内环流。
