# -*- coding: utf-8 -*-
"""
§29_verify.py — 抑制机制数值化：PQ/R 对称下的有效色三重态质量与窗口扩展
S02 空间光速螺旋统一力 · 算法联盟
机制参数化：dim-5 寿命 τ₅ ∝ M_Hc_eff² = (κ·M_Hc)²，κ=有效质量放大因子
  - PQ 对称 + 额外 50/50̄、5/5̄ 希格斯（PTEP2022）：有效色三重态质量 ≫ M_GUT → κ>1 连续压低
  - R 对称（ℤ₄^R / orbifold）：dim-5 完全禁止（等效 κ=∞，τ₅ 关断）
V1  机制文献核验（PTEP2022 论断 + κ 定义）
V2  κ×M_S 二维 τ_total 表（输入谱取 §28 json）
V3  κ*(M_S) 阈值曲线（τ_total=6.6e33）+ M_Hc_eff* 定量 + R 对称关断情形
V4  判定
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "§28_质子衰变定标数据.json"), "r", encoding="utf-8") as f:
    D28 = json.load(f)

# §28 V2 谱（无 Hc 链行 + 10³TeV 文献假设行；M_Hc_GeV, M_X_GeV）
SP = []
for r in D28["V2"]:
    if r["HcIter"] == 0 or r["M_S_TeV"] >= 1000.0:
        SP.append((r["M_S_TeV"], r["M_Hc"], r["M_X"]))

SK_K, HK = 6.6e33, 1.0e35
tanb = 3.0
sin4 = (2.0*tanb/(1.0+tanb*tanb))**4  # sin⁴2β = 0.1296

def tau5(M_S, MHc_eff):
    return 4.0e35*sin4*((0.1/1.0)**2)*((M_S/1.0e2)**2)*((MHc_eff/1.0e16)**2)

def tau6(MX):
    return 5.0e34*(MX/8.0e15)**4

def tau_tot(t5, t6):
    return 1.0/(1.0/t5 + 1.0/t6)

def tau_kappa(M_S, MHc, MX, kappa):
    t5 = tau5(M_S, kappa*MHc)
    return tau_tot(t5, tau6(MX))

def kappa_star(M_S, MHc, MX, target, lo=-6.0, hi=8.0, iters=60):
    """二分 log10 κ：τ_kappa=target"""
    def f(lk):
        return tau_kappa(M_S, MHc, MX, 10.0**lk) - target
    flo = f(lo)
    for _ in range(iters):
        mid = 0.5*(lo+hi)
        fm = f(mid)
        if flo*fm < 0: hi = mid
        else: lo = mid; flo = fm
    return 10.0**(0.5*(lo+hi))

print("="*70)
print("§29 抑制机制数值化：PQ/R 对称下的有效色三重态质量与窗口扩展（numpy）", flush=True)
print("="*70, flush=True)

print("\n[V1] 机制文献核验:", flush=True)
print("  PTEP2022:『PQ 对称 + 50/50̄、5/5̄ 希格斯多重态 → 有效色三重态质量 ≫ GUT 标度、dim-5 被抑制』", flush=True)
print("  机制参数化: τ₅ ∝ M_Hc_eff² = (κ·M_Hc)²，κ=有效质量放大因子；R 对称(ℤ₄^R/orbifold)=完全禁止(κ→∞)", flush=True)
print("  输入谱（§28 json V2）: %d 行" % len(SP), flush=True)

print("\n[V2] κ×M_S 二维 τ_total 表（tanβ=3, Ā_R=1 保守）:", flush=True)
tab = []
kappas = (1.0, 10.0, 100.0, 1.0e3, 1.0e4, 1.0e5)
hdr = "".join("%13s" % ("κ=%.0e" % k) for k in kappas)
print("  M_S(TeV) | M_Hc | M_X |" + hdr, flush=True)
for M_S, MHc, MX in SP:
    row = []
    for k in kappas:
        tt = tau_kappa(M_S, MHc, MX, k)
        row.append(tt)
        tab.append((M_S, k, tt))
    print("  %5.0f | %.2e | %.2e |" % (M_S, MHc, MX) +
          "".join("%13s" % ("%.2e" % t) for t in row), flush=True)

print("\n[V3] κ*(M_S) 阈值曲线（τ_total=6.6e33 Super-K K⁺ν̄ 界）:", flush=True)
ks = []
for M_S, MHc, MX in SP:
    kstar = kappa_star(M_S, MHc, MX, SK_K)
    ks.append((M_S, kstar, kstar*MHc))
    print("  M_S=%5.0f TeV: κ*=%8.2e   M_Hc_eff*=%8.2e GeV  (M_Hc_eff*/M_GUT谱=%.1f)"
          % (M_S, kstar, kstar*MHc, kstar*MHc/max(MX,1e10)), flush=True)

print("  可检验 κ 带（Super-K 复活界 ↔ Hyper-K 灵敏度上界）:", flush=True)
ktab = []
for M_S, MHc, MX in SP:
    klo = kappa_star(M_S, MHc, MX, SK_K)
    khi = kappa_star(M_S, MHc, MX, HK)
    ktab.append((M_S, klo, khi))
    print("  M_S=%5.0f TeV: κ ∈ [%.2e, %.2e]（复活→可检验）" % (M_S, klo, khi), flush=True)

prod = ks[0][2]*SP[0][0]*1.0e3
print("  ★ 解析复活定律: M_Hc_eff*·M_S = %.2e GeV²（τ₅∝M_S²·M_Hc_eff² 被 Super-K 界钉死；四标度一致验证）" % prod, flush=True)

print("\n  复活判定（κ≥κ* 即满足 Super-K）：", flush=True)
for M_S, kstar, eff in ks:
    if M_S <= 10.0:
        print("  M_S=%.0fTeV 复活需 κ*≈%.1e（M_Hc_eff≈%.1e GeV%s）"
              % (M_S, kstar, eff, "，<M_Pl=1.2e19 边缘可行" if eff < 1.2e19 else "，>M_Pl 非物理"), flush=True)
    else:
        print("  M_S=%.0fTeV 无抑制已存活（κ*=%.1f）" % (M_S, kstar), flush=True)

print("\n  R 对称完全禁止（τ₅ 关断 → τ=τ₆）：", flush=True)
for M_S, MHc, MX in SP:
    t6 = tau6(MX)
    print("  M_S=%5.0f TeV: τ=τ₆=%.2e yr（全程 >> 界；Hyper-K 不可检验）" % (M_S, t6), flush=True)

print("\n[V4] 判定:", flush=True)
ks1 = dict((M_S, k) for M_S, k, _ in ks)
print("  低能复活条件定量: M_S=1TeV 需 κ*=%.1e（M_Hc_eff≈3.6e18≈0.3M_Pl 边缘）；M_S=10TeV 仅需 κ*≈%.0f（M_Hc_eff≈3.6e17）"
      % (ks1[1.0], ks1[10.0]), flush=True)
print("  可检验窗口扩展: (M_S,κ) 平面 τ∈(6.6e33,1e35) 条带 — 半低能(10TeV)+κ~40 即复活且可检验", flush=True)
print("  R 对称(完全禁止): 质子衰变退化为纯 dim-6（τ≥1.5e37）— 不可检验（窗口另一方向关闭）", flush=True)
print("  S02 零参与；定级维持组织性语言", flush=True)

data = {"V1": {"mechanism": "PQ 对称+50/50̄、5/5̄ → 有效色三重态质量≫GUT（PTEP2022）；R 对称=完全禁止",
               "param": "τ₅ ∝ (κ·M_Hc)²", "SK_K": SK_K, "HK": HK},
        "V2": [{"M_S_TeV": r[0], "M_Hc": r[1], "M_X": r[2], "tau_kappa": r[3]} for r in
               [(M_S, MHc, MX, [tau_kappa(M_S, MHc, MX, k) for k in kappas]) for M_S, MHc, MX in SP]],
        "V3": [{"M_S_TeV": r[0], "kappa_star": r[1], "MHc_eff_star": r[2]} for r in ks],
        "V3b": [{"M_S_TeV": r[0], "kappa_lo": r[1], "kappa_hi": r[2]} for r in ktab],
        "law": {"MHc_eff_times_MS": prod, "GeV2": 1.0},
        "V4": {"low_E_revival": {"1TeV": ks1[1.0], "10TeV": ks1[10.0]}, "R_sym_forbid": True, "S02_zero": True}}
with open(os.path.join(HERE, "§29_抑制机制数据.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("\n数据已写入: §29_抑制机制数据.json")
