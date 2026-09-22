# -*- coding: utf-8 -*-
"""
V1.7 · 统一跑动检验：sin²θ_W = 1/4 候选预言的跑动验证（SM/MSSM 单圈）
验证A: M_Z 处三规范耦合精确值（GUT 归一化 α₁⁻¹、α₂⁻¹、α₃⁻¹）
验证B: SM 单圈三线不汇聚（三线两两相交但不成一点——标准结论复现）
验证C: CP² 候选检验——sin²θ = 1/4 若在电弱尺度成立，与实验跑动值差多少？
验证D: MSSM 对照——α_EM+α_s 输入、预测 sin²θ(M_Z)（真预测，非恒等）
验证E: 判定与诚实边界（候选定位、框架待决项、OPEN）
"""
import numpy as np

# [UTF8-GUARD v1]
import sys as _sys_utf8
try:
    _sys_utf8.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PI = np.pi
aEM_inv = 127.916            # α_EM(M_Z)⁻¹（输入）
s2w_exp = 0.23122            # sin²θ_W(M_Z) 实验（MS-bar）
a3_inv = 1 / 0.1179          # α_s(M_Z)⁻¹（输入）
mZ = 91.1876                 # GeV
v_fw = 255.26                # 框架真空值（第25章，GeV）

c2w = 1 - s2w_exp
A1 = (3.0 / 5.0) * c2w * aEM_inv
A2 = s2w_exp * aEM_inv
A3 = a3_inv
print("=" * 66)
print("验证A | M_Z 处三规范耦合（GUT 归一化）")
print("=" * 66)
print(f"  α₁⁻¹ = (3/5)cos²θ·α_EM⁻¹ = {A1:.4f}    α₂⁻¹ = sin²θ·α_EM⁻¹ = {A2:.4f}    α₃⁻¹ = {A3:.4f}")
print(f"  复核 sin²θ = 3A₂/(3A₂+5A₁) = {3*A2/(3*A2+5*A1):.5f}（输入 {s2w_exp} ✓）")

# ---- SM 单圈 β（dα_i⁻¹/dlnμ = -b_i/2π）----
b1_sm, b2_sm, b3_sm = 41.0/10, -19.0/6, -7.0
print()
print("=" * 66)
print("验证B | SM 单圈：三线是否汇聚于一点")
print("=" * 66)
print(f"  SM β: b = ({b1_sm:+.2f}, {b2_sm:+.2f}, {b3_sm:+.2f})")
x12 = (A1 - A2) / (b1_sm - b2_sm)
M12 = mZ * np.exp(2*PI*x12)
A_at12 = A1 - b1_sm*x12
A3_at12 = A3 - b3_sm*x12
print(f"  α₁⁻¹=α₂⁻¹ 交点: M = {M12:.3e} GeV（α⁻¹ = {A_at12:.2f}），同点 α₃⁻¹ = {A3_at12:.2f}")
print(f"  → 三线不成一点（差距 {abs(A_at12-A3_at12)/A_at12*100:.1f}%）: SM 单圈无大统一 ✓（标准结论）")

print()
print("=" * 66)
print("验证C | CP² 候选（sin²θ = 1/4）跑动检验")
print("=" * 66)
x_v = np.log(v_fw / mZ) / (2*PI)
A1v, A2v = A1 - b1_sm*x_v, A2 - b2_sm*x_v
s2w_v = 3*A2v / (3*A2v + 5*A1v)
print(f"  实验值单圈跑动到 v={v_fw:.1f} GeV: sin²θ(v) = {s2w_v:.5f}")
print(f"  vs CP² 候选 1/4 = {1/4:.5f} → 差 {(s2w_v-0.25)/0.25*100:+.1f}%（电弱尺度，SM 单圈）")
r_target = 9.0/5.0
x_star = (A1 - r_target*A2) / (b1_sm - r_target*b2_sm)
M_star = mZ * np.exp(2*PI*x_star)
print(f"  sin²θ = 1/4 在 SM 单圈下唯一成立尺度: M = {M_star:.2f} GeV")
print(f"  → 该尺度既非 v 也非 ℓ_P⁻¹，无框架出处：候选需框架指定统一尺度，否则无预测")

print()
print("=" * 66)
print("验证D | MSSM 对照（α_EM+α_s 输入 → 预测 sin²θ(M_Z)，真预测）")
print("=" * 66)
b1_m, b2_m, b3_m = 33.0/5, 1.0, -3.0
x_unif = (A1 - A2) / (b1_m - b2_m)
M_unif = mZ * np.exp(2*PI*x_unif)
A_gut = A1 - b1_m*x_unif
A3_at = A3 - b3_m*x_unif
print(f"  MSSM β: b = ({b1_m:+.2f}, {b2_m:+.2f}, {b3_m:+.2f})")
print(f"  α₁⁻¹=α₂⁻¹ 统一点: M = {M_unif:.3e} GeV, α_GUT⁻¹ = {A_gut:.2f}（α_GUT ≈ 1/{A_gut:.1f}）")
print(f"  同点 α₃⁻¹ = {A3_at:.2f} → 三线汇聚差 {abs(A3_at-A_gut)/A_gut*100:.2f}%（单圈；两圈+阈值后 <1%）")
# 真预测：仅用 α_EM、α_s 输入，求 (L, sin²θ) 使 A₁(L)=A₂(L)=A₃(L)
s = np.sqrt(np.linspace(0.05, 0.4, 100000))
def A1_0(s2): return (3.0/5.0)*(1-s2)*aEM_inv
def A2_0(s2): return s2*aEM_inv
# A1=A3: L13 = (A1_0-A3)/(b1-b3)·2π；A2=A3: L23 = (A2_0-A3)/(b2-b3)·2π
L13 = (A1_0(s) - A3) / (b1_m - b3_m) * 2*PI
L23 = (A2_0(s) - A3) / (b2_m - b3_m) * 2*PI
i = np.argmin(np.abs(L13 - L23))
s2w_pred = s[i]
L_pred = L13[i]
M_pred = mZ*np.exp(L_pred)
print(f"  用 α_EM、α_s 输入预测 sin²θ(M_Z) = {s2w_pred:.5f} vs 实验 {s2w_exp:.5f}"
      f"（差 {(s2w_pred-s2w_exp)/s2w_exp*100:+.2f}%）")
print(f"  同时确定统一尺度 M = {M_pred:.3e} GeV、α_GUT⁻¹ = {A3 - b3_m*L_pred/(2*PI):.2f}")
print(f"  → MSSM 著名预测复现（对偶周期四 ↔ 超对称谱的候选对应之外部数值锚点；对照观察，非本框架推导）")

print()
print("=" * 66)
print("验证E | 判定与诚实边界")
print("=" * 66)
print("  ① CP² 候选 sin²θ = 1/4：电弱尺度检验差 5.4%（SM 单圈）；")
print("     唯一自洽尺度 M ≈ 3.7 TeV 无框架出处 → 候选未获跑动支持（负面结果如实记录）")
print("  ② MSSM 对照：单圈统一 M ≈ 2×10¹⁶ GeV、α_GUT ≈ 1/24；")
print("     α_EM+α_s 输入预测 sin²θ(M_Z) 差 0.1% 级——若框架对偶周期四对应超对称谱，此为外部数值锚点")
print("  ③ 框架待决：统一尺度的几何指定（v/ℓ_P⁻¹/新尺度）、超荷归一化来源（λ₈ 嵌入 vs GUT 归一化）")
print("  → 常数统一 0.2 → 0.25（验证路径落实、候选定位清晰；达成度未提升）")
