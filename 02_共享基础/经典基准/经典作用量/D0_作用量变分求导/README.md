# D0 · 作用量变分求导（核心方法论）

> 方法①：从公理到方程。所有方程都是某个作用量 S 的 Euler-Lagrange 变分方程。

## 统一变分原理

| 理论 | 作用量 S | 变分 δS=0 → 方程 |
|---|---|---|
| 标量场 | ∫d⁴x [½(∂φ)² − ½m²φ²] | (□+m²)φ=0  (Klein-Gordon) |
| 电磁/Maxwell | −¼∫F² | ∂_μ F^{μν}=J^ν |
| Yang-Mills | −¼∫Tr(F²) | D_μ F^{μν}=J^ν |
| Einstein-Hilbert | ∫d⁴x √−g (R−2Λ)/(16πG) | G_{μν}+Λg_{μν}=8πG T_{μν} |
| 大统一力（张祥前） | P=m(c−v) | dP/dt=F |

## 全维度求导链（核心）

```
公理 v≡c（光速螺旋）
   ↓ 几何：世界线 r(t)，Frenet 框架 (T,N,B)
   ↓ 曲率 κ、挠率 τ
   ↓ 三重奏恒等式 κ²+τ²=(ω/v)²          ← TS1（Sympy 符号差=0）
   ↓ 全维推广 Σκᵢ²=−tr(A²)/(2v²)        ← R9
   ↓ 梯度磁场精确 κ²+τ²=(qB/mv)²        ← R11
   ↓ 电磁波 E=cB，c=1/√(ε₀μ₀)           ← TS3
   ↓ 力分解 F_e/F_m=c/v                  ← D5
```

## 运行

```powershell
cd openuft/70_source_code
python -m 三重奏统一场.verify
# 或直接复算 D0 变分求导：
python 10_D_求导_derivation/D0_作用量变分求导/D0_作用量变分求导.py
```

见同目录 `D0_作用量变分求导.py`，复算 KG / Maxwell / Einstein-Hilbert 变分结构。

— AI科技星 · openuft · D0
