# 53 · 涡量量子化 ∮v·dl=h/m：Onsager-Feynman 自洽（质荷同源深化 #3）

> 承接：[50_磁通普适](50_f普适化与磁通普适量子化_质荷同源深化_2026-10-10.md)、[51_AB相位](51_磁通量子化与AB相位自洽_质荷同源深化_2026-10-10.md)
> 日期：2026-10-10 · 复算仪器：[o1_vorticity_quantization.py](验证脚本/o1_vorticity_quantization.py)
> 分级：✅ 代数推论 + 与实验事实（Onsager-Feynman）自洽 + 🟡 同构非等同。L3 计数仍 0。

---

## 0. 一句话结论

50 号磁通普适量子化 $\Phi_i=\Phi_0=h/2e$ 直接推论出**速度场涡量量子化**：
$$
\oint \vec v\cdot d\vec l=\frac{\Phi_0}{f_i}=\frac{h/2e}{m_i/2e}=\frac{h}{m_i}.
$$
这与**超流氦 Onsager-Feynman 量子化涡旋** $\oint\vec v\cdot d\vec l=n\,h/m$（标准实验事实，1949 年已测）**同构自洽**。数值验证：电子 $7.27\times10^{-4}$、氦⁴ $9.97\times10^{-8}$ m²/s。质荷同源线再获一个与实验事实自洽的结果。

---

## 一、50 号推论：∮v·dl=h/m_i

50 号：$\Phi_i=f_i\cdot2\pi\hbar/m_i=\Phi_0=h/2e$（磁通普适）。由 $\Phi=f\oint\vec v\cdot d\vec l$：
$$
\oint\vec v\cdot d\vec l=\frac{\Phi_0}{f_i}=\frac{h/2e}{m_i/2e}=\frac{h}{m_i}.
$$
**m_i 消去后，涡量量子化普适**——速度场环量=h/m_i。

---

## 二、Onsager-Feynman 对照（超流氦，标准实验事实）

超流氦⁴ 量子化涡旋（Onsager 1949 / Feynman 1955，已实验确认）：
$$
\oint\vec v\cdot d\vec l=n\,\frac{h}{m_{\mathrm{He^4}}},\qquad n=1,2,\dots
$$
基态 $n=1$：$\oint\vec v\cdot d\vec l=h/m_{\mathrm{He^4}}=9.97\times10^{-8}$ m²/s。

**TUFT 涡量量子化 $h/m_i$ 与 Onsager-Feynman 同构**——标准超流涡旋量子化是实验事实，TUFT 侧给出同一形式（普适量子化 $h/m$）。

---

## 三、数值验证（`o1_vorticity_quantization.py`）

| 粒子 | $\oint\vec v\cdot d\vec l=h/m_i$ (m²/s) |
|---|---|
| 电子 | $7.27\times10^{-4}$ |
| μ子 | $3.52\times10^{-6}$ |
| 氦⁴ | $9.97\times10^{-8}$（与 Onsager-Feynman 基态一致）|

---

## 四、电荷量子化关联

1. **每个磁通量子 Φ₀（50 号）⇔ 一个涡量量子 $\oint\vec v\cdot d\vec l=h/m_i$**；
2. **2e 整相位（51 号）**：电荷量子化单位 $e$ 关联磁通量子；
3. **涡量量子化是电荷-磁通量子化的动力学实现**——质荷同源深化：磁通量子化（Φ₀）、相位自洽（AB）、涡量量子化（h/m）三链闭合，均与标准量子力学/超流实验事实自洽。

---

## 五、诚实边界

- **代数推论严格**（✅）：$\oint\vec v\cdot d\vec l=h/m_i$ 是 50 号直接推论；Onsager-Feynman 是实验事实——**自洽，不新增矛盾**；
- 依赖 $f_i=m_i/2e$ + $\omega\rho^2=\hbar/m_i$（🟡，50 号）；
- **同构非等同（🟡）**：超流氦涡旋是中性超流；TUFT 用于带电粒子，对应关系为形式同构而非同一物理系统；
- 电荷量子化的拓扑微观机制未独立导出（🟡，52 号 P1）；
- **L3 仍 0**；未动 claims.csv。

---

## 六、结论与下一步

**本轮净增**：① 涡量量子化 $\oint\vec v\cdot d\vec l=h/m_i$（50 号推论）；② 与超流氦 Onsager-Feynman 量子化涡旋同构自洽（标准实验事实）；③ 磁通（Φ₀）-相位（AB）-涡量（h/m）三链闭合，质荷同源深化完成闭环。

**下一步**：质荷同源线三链（50/51/53）与实验事实自洽已充分。可：① 连通正典（52 号 P1：新增 C 条目登记"磁通普适-涡量量子化-AB 自洽"）；② 攻电荷量子化拓扑机制（为何 e 整数倍）；③ 转 P2 纵波 B=0 实验方案。

---

[验证脚本目录](验证脚本/README.md) · [50 磁通普适](50_f普适化与磁通普适量子化_质荷同源深化_2026-10-10.md) · [51 AB相位](51_磁通量子化与AB相位自洽_质荷同源深化_2026-10-10.md) · [本体系归档首页](README.md)
