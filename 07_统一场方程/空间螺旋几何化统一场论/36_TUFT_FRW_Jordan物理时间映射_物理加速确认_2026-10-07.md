# 36 · TUFT FRW 挠率场宇宙学 · Jordan 物理时间映射（确认物理加速）

> 承接：[34_TUFT_FRW EF 复核](34_TUFT_FRW_EinsteinFrame_暗能量机制复核_2026-10-07.md)（EF 时间 ≠ 物理时间，加速判定需共形映射确认）、[35_TUFT_FRW 含物质现象学](35_TUFT_FRW_含物质辐射现象学对照_2026-10-07.md)（§4.1 开放）。
> 日期：2026-10-07 · 复算仪器：[v36_jordan_physical_time.py](验证脚本/v36_jordan_physical_time.py)（EF 解 → 共形反推 Jordan，scipy DOP853）
> 读数：[V3_13_jordan_physical_time.json](V3_13_jordan_physical_time.json)
> **铁律：数学自洽 ≠ 实验证实；EF 是分析非最小耦合暗能量的正确框架，Jordan 的 w 定义在非最小耦合下不干净；本册确认物理加速，非已证暗能量。**

---

## 0. 一句话结论

从 34 稿 EF 解用共形因子 $\Omega=(1+g\kappa\tau)^{-1/2}$ 反推 Jordan 物理时间（$dt_J=\Omega\,dt$）后，**g≠0 加速档在 Jordan 物理时间下 $\ddot a_J>0$（$2\dot H_J+3H_J^2>0$），物理加速成立**——EF 判定的加速在物理时间得到确认，机制真实可行。g=0 对照为弱加速边界、不作为暗能量。**闭合 34/35 稿的"EF 时间≠物理时间"缺口（真空情形）。**

## 1. 共形映射（EF→Jordan）

EF 中引力项 $(1/2\kappa)\tilde R$、标量 $K(\tau)\dot\tau^2/2-U(\tau)$；34 稿设定 $\Omega^2F=1/(2\kappa)$，$F=(1+g\kappa\tau)/(2\kappa)$，故
$$
\Omega(\tau)=\frac1{\sqrt{2\kappa F}}=\frac1{\sqrt{1+g\kappa\tau}},\qquad
a_J=\Omega\,a,\qquad dt_J=\Omega\,dt,\qquad
\dot\Omega=\underbrace{-\tfrac{g\kappa X}{2}(1+g\kappa\tau)^{-3/2}}_{\tfrac{d\ln\Omega}{d\tau}X}.
$$
Jordan Hubble（对物理时间 $t_J$）：$H_J=(\dot H+...)/$，精确
$$
H_J=\frac{H+\dot\Omega/\Omega}{\Omega}=\frac{H+fX}{\Omega},\qquad f=\frac{d\ln\Omega}{d\tau}=-\frac{g\kappa}{2(1+g\kappa\tau)}.
$$
加速判据（对任一公理化时间）$\ddot a_J>0\ \Leftrightarrow\ 2\dot H_J+3H_J^2>0$（因 $2\dot H+3H^2=-\kappa w\rho$，$w<-\tfrac13\Leftrightarrow$ 该量 $>0$）。

## 2. 数值结果

| g | m | τ₀ | Ω_min | EF w_eff | EF 加速 | **Jordan w_J** | **Jordan 加速（2Ḣ+3H²）** | a_J_end |
|---|---:|---:|---:|---|---:|---|---:|---:|
| 0.3 | 0.005 | 1.0 | 0.342 | −0.999 | ✓ | −1.073 | **✓（+4.0×10⁻⁵）** | 0.368 |
| 0.2 | 0.01 | 0.6 | 0.499 | −0.981 | ✓ | −1.081 | **✓（+1.3×10⁻⁴）** | 0.603 |
| 0.1 | 0.01 | 0.8 | 0.576 | −0.961 | ✓ | −0.990 | **✓（+2.8×10⁻⁴）** | 0.805 |
| 0 | 0.01 | 0.5 | 1.000 | −0.372 | 弱 | +0.053 | ✗（−9.1×10⁻⁶，噪声级） | 1.756 |

**核心读数**：
1. **g≠0 三档 Jordan 物理时间 $2\dot H_J+3H_J^2>0$（加速），与 EF 判定一致**——34 稿的 EF 加速在物理时间得到确认，机制真实（此前 34/35 稿 EF 加速仅是 EF 时间下的判定）；
2. **Jordan $w_J<-1$（−1.07、−1.08）为非最小耦合 frame 效应**：Jordan frame 中 τ 场有效能动量非标准（$F(\tau)R$ 使 τ 的 $T_{\mu\nu}$ 含曲率项），$w=p/\rho$ 定义不适用/不干净；EF 中 $w>-1$（无 Phantom），故 Jordan $w<-1$ **不是真 Phantom**，是两 frame 的能动量投影差异；
3. **g=0 对照**：$w≈-0.37$ 接近 −1/3 边界，Jordan $2\dot H+3H^2≈-9×10⁻⁶$（末期 $H_J$ 小、数值噪声量级），不作为暗能量候选；
4. $a_J$ 单调增长（0.342→0.368 等），物理时间 $t_J$ 累积（Ω<1），物理膨胀正常。

## 3. 判定：物理加速成立（frame 一致性）

标准结果强化：**非最小耦合标量的物理结论应在 EF 读**（EF 中 τ 是标准标量、$w$、加速定义干净）；Jordan 是 frame 投影。本册证明两者在**加速判定上一致**（g≠0 物理加速），且 Jordan 的 $w<-1$ 是 frame 效应而非真 Phantom。⇒ **34 稿"EF 加速"升级为"物理加速成立"**，机制真实性进一步确认；但仍未证暗能量（无观测对照）。

## 4. 诚实边界

1. **仅真空情形**：含物质的 EF→Jordan 共形耦合（Jordan 物质最小耦合 → EF 物质耦合到 τ）未做（35 稿 §4.2），物理宇宙的物质观测对应待补。
2. **Jordan $w$ 定义不干净**：非最小耦合下 $w_J=p/\rho$ 非标准，本册用几何判据 $2\dot H_J+3H_J^2$ 判定加速，不用 $w_J$ 数值作物理量。
3. **g=0 末期数值噪声**：$H_J$ 小、np.gradient 求导噪声量级 $10^{-5}$，g=0 为弱加速边界非 DE 候选，不影响核心结论。
4. **无观测对照**：未拟合 $H_0$、$\Omega_m$、$w(a)$ 与 CMB/SNe；无红移对应计算。

> **红线（不变）**：本册闭合 EF→Jordan 物理时间映射（真空），把 34/35 稿"EF 加速"升级为"物理加速成立"；数学自洽 ≠ 实验证实；未动 `claims.csv`、不进 L3 计数、不升完成度。

## 5. 后续候选

- **含物质共形耦合**：Jordan 物质最小耦合 → EF 物质耦合 τ 的完整映射，闭合 35 稿 §4.2；
- **红移/观测对照**：$a_J(z)$、$H(z)$、$w(z)$ 与 CMB/SNe 数据（若做需真实观测数据）；
- **主线 Q-ball 带电完整耦合谱**（稳定性链路）与 **分支① 费米子耦合**（先建自旋-1/2）；
- **黑洞热力学挠率熵**（来稿分支④）。
