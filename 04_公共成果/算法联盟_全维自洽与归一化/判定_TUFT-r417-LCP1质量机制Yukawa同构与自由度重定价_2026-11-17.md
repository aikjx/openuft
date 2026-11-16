# 判定册 · TUFT r417：LCP-1 质量机制 Yukawa 同构与自由度重定价（2026-11-17）

> 承接 r416：把“封装场给质量”与 SM Yukawa/Higgs 质量机制逐项对表，判定它是新机制还是改名。
> 引擎：`源码/TUFT-r417_LCP1质量机制Yukawa同构与自由度重定价_2026-11-17.py`；数据：`数据/TUFT-r417_LCP1质量机制Yukawa同构与自由度重定价_2026-11-17.{json,md,_report.txt}`
> verdict: `LCP1-MASS-MECHANISM--RENAMED-YUKAWA-WHEN-MAPPED--FREEDOM-UNCHANGED-OR-UNDERSTATED--NO-Y-OR-VEV-DERIVED--EW-GAUGE-SECTOR-MISSING--0OF6-UNCHANGED`

## §0 一句话裁定

**LCP-1 的质量式在标准归一化下与 SM Yukawa 同构；未映射时自由度少报，映射后novelty=0。它不是新的质量起源机制，也未恢复电弱规范扇区。**

## §1 映射表

| LCP-1 项 | SM 对应 | 条件 |
|---|---|---|
| `m_seal^2 = m0^2 + y^2 sigma0^2` | `m_f = y_f v_sm/sqrt(2)` | `m0=0`，`sigma0=v_sm/sqrt(2)` |
| `sigma` 四次势 | Higgs 四次势 | `lambda_h=lambda_L/4` |
| `y psi_bar psi sigma` | Yukawa 项 | 逐味 `y_f` 外给 |
| U(1) 无质量光子 | 未破缺 U(1)em | 未给 SU(2)xU(1) 电弱扇区 |

## §2 数值与机器读数

- `v_sm`=2.462196507941E+02 GeV；`sigma0`=1.741035847379E+02 GeV。
- 质量式映射相对残差=5.000000E-60；错归一化阴性对照=4.142136E-01。
- 四次势映射相对残差=0.000000E+06。
- 逐味反解：`y_e`=2.935028309550E-06，`y_mu`=6.068707640859E-04，`y_tau`=1.020576344062E-02。
- 质量比：`m_mu/m_e`=2.067682830E+02，`m_tau/m_e`=3.477228280E+03；单一 y 不能同时命中。

## §3 门禁表

| 门禁 | 状态 | 读数 |
|---|---|---|
| bare_mass_term | PART | SM 手征费米子要求 m0=0；若保留 m0 则须另给矢量样新费米子表示 |
| charge_quantization | PART | 电荷量子化是继承的 SM/U(1) 条件，LCP-1 未新增派生 |
| edm | PART | 实 y 给 d_e=0，与 SM CP 守恒 Yukawa 同型；不是新预言 |
| electroweak_gauge_sector | FAIL | LCP-1 仅列 U(1)em 无质量光子；未给 SU(2)_L x U(1)_Y 双重态、W/Z 质量与 Goldstone 混合 |
| freedom_accounting | FAIL | 改名支 novelty=0；新机制支基准 +4，拟合三轻子 +6，beta 函数另 +2 |
| g2 | NOT_PREDICTIVE | Yukawa 树级质量关系不含 g-2 一圈修正；旧 TUFT 偏差 74.96% 不变 |
| mass_formula_isomorphism | PASS | m0=0 且 sigma0=v_sm/sqrt2 时，LCP 质量式与 SM Yukawa 质量式逐项同构，相对残差 5.000000E-60 |
| mass_spectrum | FAIL | 单一 y 给三种轻子同质量；实测 m_mu/m_e=2.067682830E+02，m_tau/m_e=3.477228280E+03 |
| photon_identity | PART | 未破缺 U(1) 保 m_gamma=0；“封装光->光子”仍缺群论/拓扑映射 |
| potential_normalization | PASS | lambda_h=lambda_L/4 后实标量势逐点相等，相对残差 0.000000E+06 |
| running_couplings | OPEN | beta_y、beta_lambda 未给；r416 beta 门禁 OPEN 原样继承 |
| stability | PART | lambda_L>0 只对齐四次势稳定条件；未给 beta_lambda 与真空稳定性判据 |
| yukawa_derivation | FAIL | 逐味 y_e,y_mu,y_tau 只能由质量反解；反解比值残差 0.000000E+06/3.000000E-60，未减少参数 |

## §4 定理 RY（Renamed-Yukawa）

若候选只以“标量真空值 × 耦合”产生费米子质量，且未推导该真空值、耦合与规范表示，则它与 SM Yukawa 的可检验内容相同。新理论地位必须来自新派生，不能来自改名。

## §5 自由度与红线

改名支：y_f(3) + v_sm(1) + lambda_h(1)，beyond-SM=0，novelty=0。
新机制支：r416 基准 sigma/v/lambda/y=4；拟合三轻子需 y_e/y_mu/y_tau，累计 6；beta_y/beta_lambda 仍为 +2 个函数级自由度。

下一步机器交接：r418 —— 封装光能否在不引入电弱双重态的前提下生成 W/Z 质量并保持 m_gamma=0。

守卫：24/24；条目：18。

红线：0/6 未完成、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4 全部保持。

事实源 md5：
- `openuft_ROOT_V48_全维度攻破力评估.md` = 4a4738106f0acecc8dd48d55988fe928
- `openuft_TUFT_V32分支融合报告.md` = 16adebed7af5dba9695ffd0baacddd9b
- `判定_TUFT-r413-出路C可变函数与部门选择的可识别性攻破_2026-11-16.md` = 44b8cc0a50a75f2d5e00cb99ae06a30e
- `判定_TUFT-r415-全方法谱系封闭生成算子与演生规范首次机判_2026-11-16.md` = 5ca88f71e3a680f25d870842159cf403
- `判定_TUFT-r416-封装光LCP1实验门禁与最小方程判决_2026-11-17.md` = 94e7182e01846d76ea2f1d1edad0d6fc
- `算法联盟_一致性强制_从反常消去推出电荷量子化与中微子Dirac层级约束_v1.md` = 117bd5ea600f5a0236e6019f1a225193
- `算法联盟_物理UFT_可证伪清单_实验窗口总账_v1.md` = e4355054cbaf508ba143ae5f6cfadc6c

