# 04_理论推导

所属独立体系：[空间光速螺旋统一力](../README.md)。

逐步列出本体系前提、借用定理、近似和输出方程；不得循环论证。

[身份与基础前提](../system.json) · [来源](../sources.md) · [证据登记](../claims.csv)

现有条目：

- [D5_大统一力方程](D5_大统一力方程)
- 光速螺旋重构：`曲率挠率频率体系_全维精算论文.md` §12 全章（含 §12.3 数值精度订正、§12.5 作用域限定、§12.9 能流、§12.10 自旋与 τ 规范分析、§12.11 一般偏振态）
- 脚本：`lightspeed_helix.py`（场标架 F-S/不变量/Darboux，无量纲差分 + O(h²) 收敛证明）、`lightspeed_helix_poynting.py`、`lightspeed_helix_spin.py`、`lightspeed_helix_polarization.py`
- 图件：`lightspeed_helix.svg`、`lightspeed_helix_poynting.svg`

- §16 共振判据与非傍轴修正（**开放项①已关闭**）：[§16_9 攻破精算](§16_9_共振判据非傍轴修正_解析闭式_攻破精算.md)
  - 修正判据：κ²+τ²+2(|l|+1)/w₀²=k²，来自精确纵向波数 k_z=√(k²−k_⊥²) 与 LG₀ₗ 束腰横向本征值 k_⊥²=2(|l|+1)/w₀²；相对频移 (|l|+1)/(2k·z_R)，傍轴主判据 ω_D=k（S02-C0012）为其极限恢复。
  - 数值证据：傍轴 k_z=k 的 Helmholtz 残差 5e-4~1.5e-3，改用精确 k_z 后 ≤2e-16 ⇒ 傍轴近似即主判据的系统误差源。
  - 脚本：[resonance_nonparaxial_verify.py](resonance_nonparaxial_verify.py)（V1–V4 全 PASS，exit 0）；数据：[§16_非傍轴共振修正数据.json](§16_非傍轴共振修正数据.json)；待并入 claim 行：[_s16_9_claims_rows.csv](_s16_9_claims_rows.csv)（S02-C0116）
  - 关联：[§16_OAM 涡旋真空场耦合](§16_OAM涡旋真空场耦合TUFT螺旋测地线.md)、[sec16_7 四力审计脚本](sec16_7_fourforce_audit.py)

- §16.10 测试粒子近似自洽性（**开放项②条件闭合**）：[§16_10 攻破精算](§16_10_测试粒子近似自洽性_反作用判据_攻破精算.md)
  - 唯一无量纲反馈参数 ε_rad=τ₀ω=q²ω/(6πε₀mc³)，τ₀ 三路径（q²/(6πε₀mc³)、2r_e/(3c)、2αħ/(3mc²)）机器零一致（2.10e-16）；反馈对共振判据的偏移为二阶 −ε_rad²/4。
  - 失效阈值：ħω_c=205.554·mc²（=3/(2α)，与质量无关）、电子 E_S=1.3233e18 V/m（2.32e29 W/cm²，为现存最强激光 2.32e6 倍）⇒ 经典域内 ε~1e-8、偏移 ~1e-17，比 §16.9 非傍轴修正（强度加权平均口径）小 11–13 量级。
  - 诚实边界：真·自洽反馈（场被反散射/真空非线性）属 QED 域，登记为框架外开放项 O-S02-BACKREACTION-QED；中性粒子 q=0 时该通道反馈恒零。
  - 脚本：[resonance_backreaction_verify.py](resonance_backreaction_verify.py)（V1–V5 全 PASS，exit 0）；数据：[§16_测试粒子近似反作用判据数据.json](§16_测试粒子近似反作用判据数据.json)；待并入 claim 行：[_s16_10_claims_rows.csv](_s16_10_claims_rows.csv)（S02-C0117）
- §16.11 半整数拓扑荷 $l$ 的拓展（**开放项③已划定边界：排除**）：[§16_11 攻破精算](§16_11_半整数拓扑荷排除_涡旋单值性与自旋表示判据_攻破精算.md)
  - S02 自由空间真空 Maxwell 框架内半整数 $l$ 被排除：单值性 $e^{i2\pi l}=1\Rightarrow l\in\mathbb Z$；矢量场自旋 1 的 $2\pi$ 因子 $+1$ 与半整数相位 $-1$ 不匹配（恰与自旋 1/2 旋量匹配但非 Maxwell）；半整数 $l$ 尝试解在分支切割处生成等效线源（无源 Maxwell 不可容纳）。
  - 合法例外（向错 / 介质分数阶涡旋 / 旋量耦合）登记为框架外开放项 O-S02-FRACTIONAL-VORTEX；光子 OAM $l$ 整数（玻色单值 + 自旋 1 双重约束），总角动量 $j=l\oplus s$ 光子 $s=1$ 整数 ⇒ $j$ 整数。
  - 脚本：[fractional_topological_charge_verify.py](fractional_topological_charge_verify.py)（V1–V4 全 PASS，exit 0）；数据：[§16_半整数拓扑荷排除数据.json](§16_半整数拓扑荷排除数据.json)；待并入 claim 行：[_s16_11_claims_rows.csv](_s16_11_claims_rows.csv)（S02-C0118）

> 治理待办：§17–§36 各节攻破产物（精算 md / verify.py / 数据 json / 图谱 html）尚未登记进本目录树，属在途登记债，由各节负责人按本节格式补登。
