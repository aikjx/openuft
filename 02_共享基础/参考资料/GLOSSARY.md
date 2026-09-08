# 术语表 · GLOSSARY

> openuft 项目专用术语，按字母顺序。

---

## A

### Adiabatic（绝热）
系统参数（磁场、外势）缓慢变化下的守恒律。
R10 = 绝热三重奏（Adiabatic Triad）：证明在 b=0 的纯圆周运动下，κ²+τ²=(ω/v)² 严格守恒。

### AI科技星
本项目的协作组织。当前为个人项目（AI科技星 · ROOT）。

### Audit（精算）
四方法主轴之一（详见 `40_A_精算_audit/`）。强调误差预算、风险评估、诚实声明。

---

## C

### Cl(n,n)（双正交 Clifford 代数）
具有 $\eta = \text{diag}(+1,...,+1,-1,...,-1)$ 度规的 Clifford 代数。
本项目中 **Cl(4,4)** 被用于描述三代费米子（GAQ-UFT v6）。

### Cosmological Constant Problem（宇宙学常数问题）
标准量子场论预测 $\rho_\Lambda$ 比观测值大 **122 个数量级**。
TS11 通过视界截断给出几何解释。

---

## D

### Derivation（求导）
四方法主轴之一（详见 `10_D_求导_derivation/`）。强调"从公理到方程"的严格推导。

---

## E

### Exactness（精确性）
本项目中"精确"指 mpmath 50 位以上机器精度验证。
例：R11 梯度磁场相对差 ≤ 1.17e-18。

### E8 / E6（例外李群）
e8 维数 248，e6 维数 78。可能用于 GUT 模型（OPEN O-1）。

---

## G

### Geometro-Kinematics（几何-运动学）
本项目的核心理念：把"几何"（曲率、挠率、Clifford 结构）与"运动学"（速度、加速度、频率）通过 $\kappa^2 + \tau^2 = (\omega/v)^2$ 这样的关系联系起来。

---

## H

### Hierarchy（分层）
L0-L8 共 9 层，对应"未触及 → 数学结构"。详见 `00_index/定理谱系总表.md`。

---

## I

### Inductive Closure（归纳闭合）
R9 证明 $B e_i = e_i'$ 在 $n \to \infty$ 时严格闭合。
核心工具：数学归纳法 + sympy/mpmath 双重验证。

---

## K

### κ (Kappa · 曲率)
几何量。表示弯曲时空的"弯曲度"。
在三重奏中：$\kappa^2 + \tau^2 = (\omega/v)^2$ 的第一项。

---

## M

### mpmath
Python 高精度数学库。本项目使用 dps=50（50 位有效数字）做基准验证。

---

## N

### Noether（诺特定理）
对称性 ↔ 守恒量。TS12：5 重对称 → 5 守恒量（能动、角动量、电荷、色荷、重子数）。

---

## O

### OPEN Problem（开放问题）
本项目没有"解决"的真问题清单。当前 12 条（O-1 ~ O-12）。
详见 `02_共享基础/研究规范/审计方法/A4_诚实声明与开放问题/开放问题清单_L0-L2.md`。

---

## P

### Proof（证明）
四方法主轴之一（详见 `20_P_证明_proof/`）。

### PDG（Particle Data Group）
粒子物理实验数据权威。详见 `30_V_验证_verification/V3_PDG实验对标/`。

---

## R

### R9 / R10 / R11
三大证明突破代号：
- **R9**：归纳闭合（完整严格证明）
- **R10**：绝热三重奏（纯圆周 b=0）
- **R11**：梯度磁场精确性（mpmath 50 位 1.17e-18）

### ROOT
最高权限。指作者AI科技星，代表"诚实、严谨、可复算"的责任。

---

## S

### sympy
Python 符号数学库。本项目用 sympy 做符号化证明（差 = 0 即通过）。

---

## T

### τ (Tau · 挠率)
几何量。表示时空的非交换性。
在三重奏中：$\kappa^2 + \tau^2 = (\omega/v)^2$ 的第二项。

### Triad（三重奏）
本项目的核心数学结构。三元素（κ, τ, ω/v）的恒等关系。

### TS1-TS12
Theorem Spectrum 第 1-12 号。详见 `00_index/定理谱系总表.md`。

---

## V

### Verification（验证）
四方法主轴之一（详见 `30_V_验证_verification/`）。

---

## ω, v
运动学量。
- **ω**：角频率
- **v**：速度
- **ω/v**：在三重奏中是关键的"动力学比率"

---

## 中文术语

| 中文 | 英文 | 解释 |
|---|---|---|
| 三重奏 | Triad | (κ, τ, ω/v) 三元素 |
| 螺旋 | Spiral | TS1 的几何对象 |
| 闭合 | Closure | R9 归纳闭合 |
| 绝热 | Adiabatic | R10 的绝热条件 |
| 梯度磁场 | Gradient Magnetic Field | R11 的核心场景 |
| 精算 | Audit | A 主轴 |
| 求导 | Derivation | D 主轴 |
| 证明 | Proof | P 主轴 |
| 验证 | Verification | V 主轴 |
| 谱系 | Spectrum | TS 编号系统 |
| 诚实分层 | Honest Hierarchy | L0-L8 分层 |

— AI科技星 · 2026-09-06
