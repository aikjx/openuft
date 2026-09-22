# D2 · Yang-Mills 作用量

## 作用量

$$S_{\rm YM} = -\frac{1}{4} \int d^4x \, F_{\mu\nu}^a F^{a\mu\nu}$$

场强：$F_{\mu\nu}^a = \partial_\mu A_\nu^a - \partial_\nu A_\mu^a + g f^{abc} A_\mu^b A_\nu^c$

- $A_\mu^a$：规范场（$a$ 为伴随表示指标）
- $f^{abc}$：结构常数
- $g$：规范耦合常数

## 场方程（变分 $\delta A_\mu^a$）

$$D_\mu F^{\mu\nu a} = J^{\nu a}$$

其中 $D_\mu = \partial_\mu + i g A_\mu^a T^a$ 为协变导数。

## 关键性质

- 规范不变：$A_\mu \to U A_\mu U^\dagger - \frac{i}{g} U \partial_\mu U^\dagger$
- 渐近自由：非阿贝尔规范场在高动量下耦合减弱（QCD）
- 禁闭：$SU(3)$ 色禁闭（数值证据，无解析证明）

## 与 openuft 体系对照

| 体系 | 恢复情况 |
|---|---|
| 07_统一场方程 (UFE-1) | UFE-1 含 $SU(3)_C \times SU(2)_L \times U(1)_Y$ YM 项 |
| S06_TCL拓扑手征锁定 | 规范群从拓扑涌现 |
| P03_规范对称统一候选 | 待建模，未冻结群 |
