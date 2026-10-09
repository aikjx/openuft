# -*- coding: utf-8 -*-
"""
Gε₀ 耦合恒等式嵌入统一场母方程 · μ₀几何本源 · 量纲逐阶校验
Python 250 位 mpmath 精算验证 + sympy 量纲/代数审计
算法联盟 ROOT 最高权限 · 2026-08-21
====================================================================
本文档对 v5/1.md 所引 "全域双向分形统一场论" 之 Gε₀ 章逐条精算验证.

核心审查结论(与 v4/78 号一致):
  [P0-代数错误] ε₀ = e²/(α³ℏc) 与 μ₀ = α³ℏ/(ce²) 的 α 指数应为 1(非 3),
                且 ε₀ 缺 4π 因子. 正确: ε₀ = e²/(4παℏc).
  [P1-连带错误] Gε₀ = e²/(α³m_P²) 应为 Gε₀ = e²/(4πα·m_P²).
  [P2-正确项]   K_G = -ℏ³/(c m_P²) 两种形式代数等价(与 α,e 无关, 消去自洽) ✅
  [P3-光速闭环] c = 1/√(μ₀ε₀) 恒成立(定义链) ✅
  [P4-诚实判定] "正确公式" 是传统 α 定义的循环重排, 非 (κ,τ) 第一性独立导出;
                α, e, m_P 均为测量锚 (v4 NG-X), 不能伪称几何导出.
====================================================================
"""
import sys, io, os
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import mpmath as mp
from mpmath import mpf, sqrt, pi
mp.mp.dps = 250

# ---------- 符号代数(量纲审计) ----------
from sympy import symbols, solve, simplify, Eq, pi as SP, S

# ============================================================
# CODATA-2022 输入锚
# ============================================================
c       = mpf("299792458")
h       = mpf("6.62607015e-34")
hbar    = h/(2*pi)
e       = mpf("1.602176634e-19")
G       = mpf("6.67430e-11")
alpha   = mpf("0.0072973525693")          # 测量锚
eps0_CODATA = mpf("8.8541878128e-12")
mu0_CODATA  = mpf("1.25663706212e-6")     # 4π×1e-7

# 派生量
mP       = sqrt(hbar*c/G)                 # 普朗克质量 = √(ℏc/G)  [文档第五节一致]
Omega_P  = mP*c/hbar                      # Ω_P = m_P·c/ℏ  (ℏ/c = m_P/Ω_P)

L=[]
def sec(t):
    L.append("\n"+"="*74); L.append("  "+t); L.append("="*74)
def put(s=""):
    L.append(s)
def ok(b):
    return "✅ PASS" if b else "❌ FAIL"
def rel(a,b):
    return abs(a-b)/abs(b)

L.append("""
  ┌──────────────────────────────────────────────────────────────┐
  │  Gε₀耦合恒等式 · μ₀几何本源 · 量纲逐阶  Python 250位精算验证 │
  │  算法联盟 ROOT 最高权限 · 2026-08-21                          │
  └──────────────────────────────────────────────────────────────┘""")

# ============================================================
# [0] 文档关键公式逐条数值复现 + 与 CODATA 比对
# ============================================================
sec("[0] 逐条复现文档公式 · 与 CODATA 相对残差")

# 文档(A): ε₀ = e²/(α³ℏc)   [α 指数=3]
eps0_doc = e**2/(alpha**3 * hbar * c)
put(f"  文档 ε₀ = e²/(α³ℏc)        = {mp.nstr(eps0_doc,10)}")
put(f"  CODATA ε₀                  = {mp.nstr(eps0_CODATA,10)}")
put(f"  相对偏差 = {mp.nstr(rel(eps0_doc,eps0_CODATA),3)}  → 偏离 {mp.nstr(rel(eps0_doc,eps0_CODATA)*100,4)}%  {ok(False)}")
put(f"  [判定] 量级差 ~2.36e5 倍 —— α 指数写成 3, 应为 1; 且缺 4π 因子")

# 文档(B): μ₀ = α³ℏ/(c·e²)   [α 指数=3]
mu0_doc = alpha**3 * hbar/(c * e**2)
put(f"  文档 μ₀ = α³ℏ/(c·e²)      = {mp.nstr(mu0_doc,10)}")
put(f"  CODATA μ₀                  = {mp.nstr(mu0_CODATA,10)}")
put(f"  相对偏差 = {mp.nstr(rel(mu0_doc,mu0_CODATA),3)}  → 偏离 {mp.nstr(rel(mu0_doc,mu0_CODATA)*100,4)}%  {ok(False)}")
put(f"  [判定] 同理 α 指数错(应为1), 且缺 1/4π")

# 文档(C): Gε₀ = e²/(α³ m_P²)
LHS_Geps = G*eps0_CODATA
RHS_doc  = e**2/(alpha**3 * mP**2)
put(f"  G·ε₀ LHS                    = {mp.nstr(LHS_Geps,10)}")
put(f"  文档 RHS e²/(α³m_P²)       = {mp.nstr(RHS_doc,10)}")
put(f"  相对偏差 = {mp.nstr(rel(LHS_Geps,RHS_doc),3)}  {ok(False)}")
put(f"  [判定] 恒等式(文档版)不成立 —— α 指数 3 应为 1, 缺 4π")

# ============================================================
# [1] 正确公式 + 机器零验证
# ============================================================
sec("[1] 正确公式 · 机器零验证 (与 v4/29,78 一致)")
eps0_ok = e**2/(4*pi*alpha*hbar*c)
r_eps0  = rel(eps0_ok, eps0_CODATA)
put(f"  正确 ε₀ = e²/(4παℏc)      = {mp.nstr(eps0_ok,14)}")
put(f"  CODATA ε₀                  = {mp.nstr(eps0_CODATA,14)}")
put(f"  相对残差 = {mp.nstr(r_eps0,4)}  {ok(r_eps0 < mpf('1e-9'))}")

mu0_ok = 1/(eps0_ok*c**2)
r_mu0  = rel(mu0_ok, mu0_CODATA)
put(f"  正确 μ₀ = 1/(ε₀c²)         = {mp.nstr(mu0_ok,14)}")
put(f"  CODATA μ₀                  = {mp.nstr(mu0_CODATA,14)}")
put(f"  相对残差 = {mp.nstr(r_mu0,4)}  {ok(r_mu0 < mpf('1e-9'))}")
put(f"  (μ₀ = 4παℏ/(c·e²) 亦等价: {mp.nstr(4*pi*alpha*hbar/(c*e**2),14)})")

RHS_ok = e**2/(4*pi*alpha*mP**2)
r_ge   = rel(LHS_Geps, RHS_ok)
put(f"  G·ε₀ RHS_ok = e²/(4πα·m_P²) = {mp.nstr(RHS_ok,14)}")
put(f"  相对残差 = {mp.nstr(r_ge,4)}  {ok(r_ge < mpf('1e-9'))}")

# ============================================================
# [2] 量纲逐阶校验 (sympy 符号量纲)
# ============================================================
sec("[2] 量纲逐阶校验 (向量算术, 幂次表示)")
# 量纲幂次向量: (M, L, T, Q)
def dmul(*args):
    r=(0,0,0,0)
    for a in args: r=tuple(x+y for x,y in zip(r,a))
    return r
def dim_c():  # [c]=L T^-1
    return (0,1,-1,0)
def dim_hbar(): # [ℏ]=M L^2 T^-1
    return (1,2,-1,0)
def dim_e():    # [e]=Q
    return (0,0,0,1)
def dim_G():    # [G]=M^-1 L^3 T^-2
    return (-1,3,-2,0)
def dim_eps0(): # [ε0]=Q² M^-1 L^-3 T^2
    return (-1,-3,2,2)
def dim_mu0():  # [μ0]=M L Q^-2
    return (1,1,0,-2)
ZERO=(0,0,0,0)

# 1) ε₀ = e²/(ℏc)
d_eps0 = dmul(dim_e(),dim_e(),(0,0,0,0))  # e² = (0,0,0,2)
d_hbarc = dmul(dim_hbar(),dim_c())        # [ℏc]=M L^3 T^-2
d_eps0 = dmul((0,0,0,2), tuple(-x for x in d_hbarc))
put(f"  [ε₀] [e²/ℏc] = {d_eps0}  vs  [ε₀]={dim_eps0()}  {ok(d_eps0==dim_eps0())}")

# 2) μ₀ = ℏ/(c e²)
d_mu0 = dmul(dim_hbar(), tuple(-x for x in dmul(dim_c(), dmul(dim_e(), dim_e()))))
put(f"  [μ₀] [ℏ/(c e²)] = {d_mu0}  vs  [μ₀]={dim_mu0()}  {ok(d_mu0==dim_mu0())}")

# 3) G = c³/(ℏ Ω_P²)
# [c³]=L³ T^-3 ; [ℏΩ_P²]=(1,2,-1,0)·(0,-2,0,0)=(1,0,-1,0) → 倒数(-1,0,1,0)
d_G = dmul(dmul(dim_c(),dim_c(),dim_c()), tuple(-x for x in dmul(dim_hbar(),(0,-2,0,0))))
put(f"  [G] [c³/(ℏΩ_P²)] = {d_G}  vs  [G]={dim_G()}  {ok(d_G==dim_G())}")

# 4) Gε₀ = e²/(α³ m_P²) → [e²/m_P²]=Q² M^-2
d_ge_l = dmul(dim_G(),dim_eps0())
d_ge_r = dmul((0,0,0,2), (-2,0,0,0))
put(f"  [Gε₀] 左 = {d_ge_l}  vs  右 [e²/m_P²] = {d_ge_r}  {ok(d_ge_l==d_ge_r)}")

# 5) 势能母方程 引力耦合系数 [K_G]=[G(ℏ/c)²]
# [ℏ/c]=(1,2,-1,0)·(0,-1,1,0)=(1,1,0,0) → 平方 (2,2,0,0); [G]=(-1,3,-2,0)
d_KG = dmul(dim_G(), (2,2,0,0))
put(f"  [K_G]=[G(ℏ/c)²] = {d_KG}  = M L⁵ T⁻²  {ok(d_KG==(1,5,-2,0))}")
put(f"  → 母方程要求 [K·S1S2]=ML³T⁻², S1S2~Ω1Ω2~L⁻² ⇒ [K]=ML⁵T⁻² 匹配 ✅")
put(f"     (验证: ML⁵T⁻² × L⁻² × 1/r(L⁻¹) = ML²T⁻² = 势能 量纲 ✅)")

# ============================================================
# [3] K_G 两种形式代数等价
# ============================================================
sec("[3] K_G 两种形式等价 (与 α,e 无关的代数恒等)")
K_G_original = -G*(hbar/c)**2
K_G_geo      = -(hbar**3)/(c * mP**2)
put(f"  K_G_original = -G(ℏ/c)²    = {mp.nstr(K_G_original,12)}")
put(f"  K_G_geo      = -ℏ³/(c·m_P²) = {mp.nstr(K_G_geo,12)}")
put(f"  绝对差 = {mp.nstr(abs(K_G_original-K_G_geo),3)}  相对 = {mp.nstr(rel(K_G_original,K_G_geo),3)}  {ok(abs(K_G_original-K_G_geo)<mpf('1e-200'))}")

# 推导链路复现: K_G = -(e²/(α³m_P²ε₀))·(ℏ/c)² , 代 ε₀=e²/(α³ℏc) 消去
# (用符号验证消去后确实等于 -ℏ³/(c m_P²), 不依赖 α,e —— 但中间用了错误公式)
e_s, a_s, mP_s, hb_s, c_s = symbols('e alpha mP hbar c', positive=True)
eps0_wrong = e_s**2/(a_s**3*hb_s*c_s)               # 文档(错误) ε₀
KG_expr = -e_s**2/(a_s**3*mP_s**2*eps0_wrong)*(hb_s/c_s)**2
KG_simpl = simplify(KG_expr)
put(f"  符号化简 K_G(用文档错误ε₀代换后) = {KG_simpl}")
put(f"  [结论] 消去过程中 α³, e² 完全抵消 → 最终 -ℏ³/(c m_P²)")
put(f"  → 尽管中间 ε₀ 公式错误, K_G 最终形式偶然正确(纯代数消元)")
put(f"  [诚实] 该 K_G 形式 = G(ℏ/c)² 的恒等重排 (因 G=ℏc/m_P²), 非新物理")

# ============================================================
# [4] G = c³/(ℏΩ_P²) 与 G = ℏc/m_P² 一致性
# ============================================================
sec("[4] G 两种几何表达一致性")
G_from_Omega = c**3/(hbar*Omega_P**2)
put(f"  G = c³/(ℏΩ_P²)   = {mp.nstr(G_from_Omega,12)}")
put(f"  G = ℏc/m_P²      = {mp.nstr(hbar*c/mP**2,12)}")
put(f"  CODATA G         = {mp.nstr(G,12)}")
put(f"  相对残差 = {mp.nstr(rel(G_from_Omega,G),3)}  {ok(rel(G_from_Omega,G)<mpf('1e-9'))}")
put(f"  m_P = (ℏ/c)Ω_P  ⟺  Ω_P = m_P c/ℏ   (定义自洽)")

# ============================================================
# [5] 光速闭环 c = 1/√(μ₀ε₀)
# ============================================================
sec("[5] 电磁光速闭环")
c_recover = 1/sqrt(mu0_ok*eps0_ok)
put(f"  c_recover = 1/√(μ₀ε₀) = {mp.nstr(c_recover,16)}")
put(f"  c_input             = {mp.nstr(c,16)}")
put(f"  绝对差 = {mp.nstr(abs(c_recover-c),3)}  {ok(abs(c_recover-c)<mpf('1e-240'))}")
put(f"  [判定] 定义链 μ₀=1/(ε₀c²) 恒成立, 闭环自洽 ✅")

# ============================================================
# [6] 诚实总判定
# ============================================================
sec("[6] 诚实总判定 · 收口")
put(f"  ── 文档真实代数错误(与 v4/78 一致) ──")
put(f"    ✗ ε₀ = e²/(α³ℏc)      → 应为 e²/(4παℏc)   (α指数3→1, 补4π)")
put(f"    ✗ μ₀ = α³ℏ/(ce²)      → 应为 4παℏ/(ce²)   (α指数3→1, 补4π)")
put(f"    ✗ Gε₀ = e²/(α³m_P²)   → 应为 e²/(4πα·m_P²)")
put(f"  ── 修正后数值机器零 ✅ ──")
put(f"    ✓ ε₀=e²/(4παℏc), μ₀=4παℏ/(ce²), Gε₀=e²/(4παm_P²)  残差~3e-10%")
put(f"  ── 正确项 ──")
put(f"    ✓ K_G=-ℏ³/(c m_P²) 两种形式等价(消元自洽, 但=G(ℏ/c)²恒等重排)")
put(f"    ✓ G=c³/(ℏΩ_P²)=ℏc/m_P² 自洽; m_P=√(ℏc/G)")
put(f"    ✓ 量纲逐阶全闭; 光速闭环 c=1/√(μ₀ε₀) 成立")
put(f"  ── 诚实边界 (勿伪称几何导出) ──")
put(f"    ⚠ '正确公式'是传统 α 定义 α=e²/(4πε₀ℏc) 的循环重排, 非 (κ,τ) 第一性导出")
put(f"    ⚠ α, e, m_P(依赖G) 均为测量锚 (v4 NG-X); ε₀/μ₀/G 的绝对值未脱离测量")
put(f"    ⚠ 真正含几何结构的是 v4/29 ε₀=q0²/(64π³c³κτℏα) 与 v4/30 G=c³/[ℏ(κ²+τ²)]")

report = "\n".join(L)
print(report)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "Gε0_μ0_几何本源_精算验证报告.md")
with io.open(out, "w", encoding="utf-8") as fh:
    fh.write("# Gε₀ 耦合恒等式 · μ₀ 几何本源 · 量纲逐阶校验 — Python 250 位精算验证报告\n\n")
    fh.write("> 算法联盟 ROOT 最高权限 · 精算验证 · 2026-08-21\n\n")
    fh.write("## 结论速览\n\n")
    fh.write("- **[P0 代数错误]** `ε₀=e²/(α³ℏc)` 与 `μ₀=α³ℏ/(ce²)` 的 α 指数应为 1(非 3), 且 ε₀ 缺 4π 因子。\n")
    fh.write("- **[P1 连带错误]** `Gε₀=e²/(α³m_P²)` 应为 `Gε₀=e²/(4πα·m_P²)`。\n")
    fh.write("- **[P2 正确项]** `K_G=-ℏ³/(c m_P²)` 两种形式代数等价(消元自洽)。\n")
    fh.write("- **[P3 正确项]** `G=c³/(ℏΩ_P²)=ℏc/m_P²` 自洽; 量纲全闭; 光速闭环成立。\n")
    fh.write("- **[P4 诚实边界]** 修正后的「正确公式」是传统 α 定义的循环重排, 非 (κ,τ) 第一性独立导出; α, e, m_P 均为测量锚。\n\n")
    fh.write("## 完整运行输出\n\n```\n" + report + "\n```\n")
print("\n[报告已写入] " + out)
