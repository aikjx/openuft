# 数值方法 · NUMERICAL METHODS

> openuft 项目使用的所有数值工具详解。

---

## 1. 符号化证明 · sympy

### 用途
"差 = 0"型严格证明。例如：
```
κ² + τ² - (ω/v)² = 0
```
通过 sympy 的 `simplify()` 在符号层面验证。

### 标准模板
```python
import sympy as sp

t = sp.symbols('t', real=True)
r = sp.Matrix([sp.cos(t), sp.sin(t), 0.3*t])
v = r.diff(t).norm()**2
# ... 完整公式见 verify_xxx.py

LHS = ...
RHS = ...
diff = sp.simplify(LHS - RHS)
assert diff == 0, f"DIFF = {diff}"
print("✅ TS1 符号证明通过")
```

### 注意
- 必须使用实数 (`real=True`) 符号
- 必须包含时间维度
- 必须避免 `simplify()` 跨层歧义（必要时用 `trigsimp()` 或 `radsimp()`）

---

## 2. 高精度验证 · mpmath

### 用途
"差 ≤ ε"型机验证。例如：50 位有效数字下差 ≤ 1.17e-18。

### 标准模板
```python
from mpmath import mp, mpf, sqrt, cos, sin, pi

mp.dps = 50  # 50 位有效数字

t = mpf('1.23456789')
v = sqrt(cos(t)**2 + sin(t)**2)  # 应该 = 1

assert abs(v - 1) < mpf('1e-45')
print("✅ mpmath 50 位验证通过")
```

### 高精度等级

| dps | 位数 | 用途 |
|---|---|---|
| 15 | IEEE 单精度 | 快速原型 |
| 20 | IEEE 扩展 | 实验数据 |
| 50 | 基准 | TS 验证 |
| 100 | 高精度 | 关键数值 |
| 250 | 极限 | 异常值检测 |
| 1000+ | 研究级 | 特殊应用 |

---

## 3. 实验数据对标 · PDG/LIGO/Planck

### PDG 数据下载
- URL：https://pdg.lbl.gov/
- 关键数据：m_e, m_μ, m_τ, M_W, M_Z, m_H, sin²θ_W, α, α_s, ...
- 精度：1e-10 (电子质量) 到 1% (top quark 质量)

### LIGO 数据
- URL：https://www.ligo.caltech.edu/page/detection-companion-papers
- 关键事件：GW150914, GW170817, GW190521
- 提取：δc/c < 1e-15

### Planck 2018
- URL：https://www.cosmos.esa.int/web/planck/
- 关键数据：H_0 = 67.4 ± 0.5 km/s/Mpc, Ω_b, Ω_c, Ω_Λ
- 精度：0.06% (宇宙学参数)

---

## 4. 误差预算 · 蒙特卡洛

### 标准方法
```python
import numpy as np

# 参数采样（N=10000）
N = 10000
samples = np.random.normal(loc=1.0, scale=0.01, size=N)  # mean=1, std=1%
pre = 1.0 * samples  # 预言值缩放

# VaR / TVaR
VaR_95 = np.percentile(pre, 5)
TVaR_95 = pre[pre <= VaR_95].mean()
```

### Chi-平方检验
```python
from scipy.stats import chi2

expected = ...
observed = ...
chi2_stat = ((observed - expected)**2 / expected).sum()
ndf = len(observed) - 1
p_value = 1 - chi2.cdf(chi2_stat, ndf)
```

---

## 5. 验证脚本组合用法

```bash
# 1. 符号证明
python 源码/三重奏统一场/verify/verify_sympy.py

# 2. 高精度
python 源码/三重奏统一场/verify/verify_mpmath.py --dps=50

# 3. 实验对标
python 源码/三重奏统一场/verify/verify_pdg.py
python 源码/三重奏统一场/verify/verify_ligo.py
python 源码/三重奏统一场/verify/verify_planck.py

# 4. 综合验证（项目根目录）
python verify.py
```

---

## 6. 性能优化技巧

| 场景 | 技巧 |
|---|---|
| sympy 慢 | 启用 `cache`，避免 `simplify()` 跨调用 |
| mpmath 慢 | 用 `mp.dps` 梯度：从 20 → 50 → 250 验证 |
| 大数组 | `numpy.einsum` 替代显式循环 |
| 蒙特卡洛 | 用 `numpy.random.Generator` (PCG64)，避免 `np.random.normal` |
| I/O 密集 | 多进程 `multiprocessing.Pool` |

---

— AI科技星 · 2026-09-06
