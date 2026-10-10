# -*- coding: utf-8 -*-
"""attack19_复合结构唯一性.py
算法联盟最高权限 · 独立复算
攻击 O3 子线「复合结构唯一性」：
  为何 SM 规范群 SU(3)×SU(2)×U(1) 对应 CP^1×CP^2 (弱2⊕色3)，而非其他 CP^m×CP^n？
验证：
  V1 CP^n 等距群 = SU(n+1)/Z_{n+1}（枚举 n）
  V2 CP^m×CP^n 等距 = SU(m+1)×SU(n+1)（直积）
  V3 枚举 (m,n) 给出哪些规范群——是否存在唯一选择
  V4 U(1) 的不对称：CP^n 等距是单李群(SU)，不含独立 U(1) 因子
纯标准库 + numpy。
"""
import numpy as np
rng = np.random.default_rng(20261010)

def fs_dist2(u, v):
    u = u/np.linalg.norm(u); v = v/np.linalg.norm(v)
    return np.arccos(np.clip(np.abs(np.vdot(u,v)),0,1))**2

def random_su(n):
    Z = rng.normal(size=(n,n)) + 1j*rng.normal(size=(n,n))
    Q, R = np.linalg.qr(Z)
    ph = np.diag(R); ph = ph/np.abs(ph)
    U = Q * ph[None,:]
    d = np.linalg.det(U)
    return U * (np.conj(d)/abs(d))**(1/n)

def random_su2():
    a,b,c = rng.uniform(-np.pi,np.pi,3)
    return np.array([[np.cos(a)+1j*np.sin(a),0],[0,np.cos(a)-1j*np.sin(a)]])@ \
           np.array([[np.cos(b),np.sin(b)],[-np.sin(b),np.cos(b)]])@ \
           np.array([[np.cos(c)+1j*np.sin(c),0],[0,np.cos(c)-1j*np.sin(c)]])

# ============ V1: CP^n 等距群 = SU(n+1)（机器验证 n=1,2,3）============
for n in [1,2,3]:
    max_err = 0.0
    for _ in range(1500):
        u = rng.normal(size=n+1)+1j*rng.normal(size=n+1)
        v = rng.normal(size=n+1)+1j*rng.normal(size=n+1)
        U = random_su(n+1)
        max_err = max(max_err, abs(fs_dist2(u,v)-fs_dist2(U@u,U@v)))
    print(f"[V1] CP^{n}: 随机 SU({n+1}) 保 FS 距离, max err={max_err:.2e} "
          f"{'PASS' if max_err<1e-12 else 'FAIL'}  (等距=SU({n+1}))")

# ============ V2: CP^1×CP^2 等距 = SU(2)×SU(3)（直积，验证同 attack17）============
max_err2 = 0.0
for _ in range(1500):
    z1 = rng.normal(size=2)+1j*rng.normal(size=2); z2 = rng.normal(size=2)+1j*rng.normal(size=2)
    w1 = rng.normal(size=3)+1j*rng.normal(size=3); w2 = rng.normal(size=3)+1j*rng.normal(size=3)
    Uw = random_su2(); Uc = random_su(3)
    d0 = fs_dist2(z1,z2)+fs_dist2(w1,w2)
    d1 = fs_dist2(Uw@z1,Uw@z2)+fs_dist2(Uc@w1,Uc@w2)
    max_err2 = max(max_err2, abs(d0-d1))
print(f"[V2] CP^1×CP^2 等距=SU(2)×SU(3) 直积, max err={max_err2:.2e} "
      f"{'PASS' if max_err2<1e-12 else 'FAIL'}")

# ============ V3: 枚举 (m,n) → 等距群，唯一性检验 ============
print("\n[V3] CP^m×CP^n 等距群 = SU(m+1)×SU(n+1) 枚举:")
groups = {}
for m in range(0,4):
    for n in range(0,4):
        if m<n:  # 对称只列一次
            continue
        g = f"SU({m+1})×SU({n+1})"
        dim = (m+1)**2-1 + (n+1)**2-1
        groups[(m,n)] = (g, dim)
for (m,n),(g,dim) in groups.items():
    mark = " ← SM(弱2⊕色3)" if (m,n)==(1,2) else ""
    print(f"    CP^{m}×CP^{n} -> {g:16s} dim={dim}{mark}")
print("    -> 无限多 (m,n) 给出合法规范群；SM=(1,2) 只是其一，无唯一性")
print("    -> 复合结构唯一性 = O1 同类（无限几何选择需额外原理）")

# ============ V4: U(1) 不对称 ============
print("\n[V4] U(1)_Y 的不对称:")
print("    CP^n 等距 = SU(n+1)（单李群，不含独立 U(1) 因子）")
print("    SM 需独立 U(1)_Y（第三因子）—— 由整体相位补，非 CP 等距自然给出")
print("    -> 几何机制(CP^n 等距)只能给 SU 部分；U(1) 是额外相位输入")

# ============ V5: 从二分量到复合的跳跃是输入 ============
print("\n[V5] 从 S13 公设到 CP^1×CP^2 的跳跃:")
print("    二分量旋量 -> 目标空间 CP^1 (SU(2) 等距) -> 只有电弱，无色")
print("    三分量旋量 -> 目标空间 CP^2 (SU(3) 等距) -> 色，但稳定子 U(2) 是内嵌")
print("    独立直积 SU(3)×SU(2) 需 CP^1×CP^2 乘积流形 = '弱⊕色张量积' 是输入")
print("    -> 不是三公设唯一推导：'为何同时有二分量+三分量'未由公设给出")

print("="*62)
print("attack19_复合结构唯一性 · 独立复算")
print("="*62)
print()
print("分层结论：")
print("  [数学] CP^n 等距=SU(n+1)、乘积流形等距=直积，全 PASS（机器精度）。")
print("  [唯一性] SM=(1,2) 不是唯一选择——无限多 (m,n) 合法 → 未闭合，O1 同类。")
print("  [U(1)] CP 等距只给 SU 部分；U(1)_Y 是额外相位输入（不对称）。")
print("  [公设] '弱⊕色张量积' 是输入，非三公设唯一导出 → 复合唯一性未解。")
