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

> 治理待办：§17–§36 各节攻破产物（精算 md / verify.py / 数据 json / 图谱 html）尚未登记进本目录树，属在途登记债，由各节负责人按本节格式补登。
