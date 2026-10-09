# -*- coding: utf-8 -*-
"""
78号 · G-ε₀ 耦合恒等式审查修正 (接 29号 ε₀ 几何本源 / 30号 G 双变量)
算法联盟 ROOT 最高权限 · 2026-08-21

================ 审查对象 ================
用户新推导声称:
    (A) ε₀ = e²/(α³ℏc)            ← 待审
    (B) G·ε₀ = e²/(α³·m_P²)        ← 待审
并断言 ε₀, G 是 "从几何第一性原理导出的次级常数"。

================ 审查结论 (预先) ================
[P0] (A)(B) 的 α 指数应为 1 (不是 3), 且缺 4π 因子 —— 两个真实代数错误。
[P1] 正确公式: ε₀ = e²/(4παℏc)  与 CODATA 残差 ~3e-10% (机器零, 与29号一致)
[P2] 正确恒等式: G·ε₀ = e²/(4πα·m_P²)  残差 ~3e-10% (机器零)
[P3] 关键诚实判定: "正确公式" 只是传统 α 定义 α=e²/(4πε₀ℏc) 的**循环重排**,
     并非从 (κ,τ_v) 几何第一性原理独立导出 —— 因为 α, e, m_P(依赖G) 全是测量锚。
[P4] 用户的 "U_geo = U_class 反解 ε₀" 是**循环论证**: 反解得到的正是传统 α 定义,
     未产生新物理关系; v4 29号 的 ε₀=q0²/(64π³c³κτℏα) 才含真正的几何结构(虽需q0锚定)。
"""
import sys, io, os
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import sympy as sp
from mpmath import mp, mpf, nstr
mp.dps = 80

L=[]
def sec(t): L.append("\n"+"="*74); L.append("  "+t); L.append("="*74)
def put(s=""): L.append(s)
def ok(b): return "✅ PASS" if b else "❌ FAIL"

# CODATA 锚
c   = mpf('299792458')
h   = mpf('6.62607015e-34')
hbar= h/(2*mp.pi)
e   = mpf('1.602176634e-19')
G   = mpf('6.67430e-11')
alpha = mpf('0.0072973525693')
eps0 = mpf('8.8541878128e-12')
mP = mp.sqrt(hbar*c/G)

# ---------- A: 复现用户公式的数值错误 ----------
sec("[A] 复现用户公式 (A)/(B) 的数值错误")
eps0_user = e**2/(alpha**3*hbar*c)
LHS_Geps = G*eps0
RHS_Geps_user = e**2/(alpha**3*mP**2)
put(f"  用户 ε₀ = e²/(α³ℏc)        = {nstr(eps0_user,6)}")
put(f"  CODATA ε₀                 = {nstr(eps0,6)}")
put(f"  比值 ε₀_user/ε₀_CODATA    = {nstr(eps0_user/eps0,4)}  (≈2.36e5, 高出 23 万倍)")
put(f"  → 用户公式 (A) 数值错误, 偏差 {nstr(abs(eps0_user-eps0)/eps0*100,3)} %")
put(f"  G·ε₀ LHS                  = {nstr(LHS_Geps,6)}")
put(f"  用户 RHS e²/(α³m_P²)      = {nstr(RHS_Geps_user,6)}")
put(f"  → 恒等式 (B) 用户版不成立, 偏差 {nstr(abs(LHS_Geps-RHS_Geps_user)/LHS_Geps*100,3)} %")
put(f"  根因: α 指数写成 3 (应为 1) + 缺 4π 因子")

# ---------- B: sympy 代数修正 (α 指数 3→1) ----------
sec("[B] sympy 严格解用户等式, 确定正确 ε₀")
hbarc_s, e_s, eps0_s, alpha_s = sp.symbols('hbarc e eps0 alpha', positive=True)
# 用户关键等式: 几何势能系数 = 经典势能系数 (约去公共几何因子后)
eq = sp.Eq(hbarc_s/(4*sp.pi*alpha_s), e_s**2/(4*sp.pi*eps0_s*alpha_s**2))
sol = sp.solve(eq, eps0_s)[0]
put(f"  用户等式 ℏc/(4πα) = e²/(4πε₀α²) 解 ε₀:")
put(f"    正确解 = {sol}   (α 指数 1, 无 4π)")
put(f"  用户写成 e²/(α³ℏc) (α 指数 3, 差 α²) → 错")
put(f"  [代数修正] α 指数: 3 → 1")
# 等式相除揭示循环
ratio = sp.simplify((hbarc_s/(4*sp.pi*alpha_s))/(e_s**2/(4*sp.pi*eps0_s*alpha_s**2)))
put(f"  用户等式左右相除 = {ratio}")
put(f"  等式成立 ⟺ α = e²/(ε₀ℏc)   ← 这是传统 α 定义(缺4π), 非新物理")

# ---------- C: 正确公式数值机器零 ----------
sec("[C] 正确公式: ε₀ = e²/(4παℏc) 与 G·ε₀ = e²/(4πα·m_P²)")
eps0_ok = e**2/(4*mp.pi*alpha*hbar*c)
res_eps0 = abs(eps0_ok-eps0)/eps0*100
put(f"  ε₀_ok = e²/(4παℏc) = {nstr(eps0_ok,12)}")
put(f"  ε₀_CODATA           = {nstr(eps0,12)}")
put(f"  残差 = {nstr(res_eps0,4)}%  {ok(res_eps0<mpf('1e-6'))}")
put(f"  (与 v4 29号 eps0_from_e=E²/(4πℏcα) 完全一致 ✓)")
RHS_Geps_ok = e**2/(4*mp.pi*alpha*mP**2)
res_ge = abs(LHS_Geps-RHS_Geps_ok)/LHS_Geps*100
put(f"  G·ε₀ LHS       = {nstr(LHS_Geps,12)}")
put(f"  G·ε₀ RHS_ok    = e²/(4πα·m_P²) = {nstr(RHS_Geps_ok,12)}")
put(f"  残差 = {nstr(res_ge,4)}%  {ok(res_ge<mpf('1e-6'))}")
put(f"  → 修正后 G·ε₀ = e²/(4πα·m_P²) 机器零成立 (是 G=ℏc/m_P² + α 定义的两步代数推论)")

# ---------- D: 诚实判定 (循环性 / 测量锚) ----------
sec("[D] 诚实判定: 是几何导出还是循环重排?")
put(f"  α = e²/(4πε₀ℏc)  (传统定义)  ⟹  e²/(4παℏc) ≡ ε₀  (恒等重排)")
put(f"  ⇒ '正确公式 ε₀=e²/(4παℏc)' 只是把传统 α 定义重新排列, 非独立导出")
put(f"  G·ε₀ = e²/(4παm_P²): 由 G=ℏc/m_P² 代入即得, 是代数恒等, 非新物理耦合")
put(f"  [测量锚盘点] 要算 ε₀ 需 α, e; 要算 G 需 m_P(即需 G):")
put(f"    · α=1/137        → 测量锚 (v4 NG-X-2, 40/51号证不能纯几何唯一锁定)")
put(f"    · e 元电荷       → 测量锚 (v4 NG-X-A2)")
put(f"    · m_P=√(ℏc/G)   → 依赖 G, 循环 (v4 30号 G=c³/[ℏ(κ²+τ²)] 需普朗克 κ_P,τ_P)")
put(f"  ⇒ ε₀, G 作为测量锚的代数组合, 并未被 (κ,τ_v) 独立导出")
put(f"  [真正含几何结构的是 v4 29号] ε₀_geo = q0²/(64π³c³κτℏα) (含 κτ 螺旋结构, 但 q0 锚定)")

sec("[E] 收口 · 修正建议")
put(f"  ── 用户公式的两个真实错误 ──")
put(f"    ✗ ε₀ = e²/(α³ℏc)      → 应为 e²/(4παℏc)  (α指数3→1, 补4π)")
put(f"    ✗ G·ε₀ = e²/(α³m_P²)  → 应为 e²/(4πα·m_P²)  (同上)")
put(f"  ── 修正后 (数值机器零) ──")
put(f"    ✓ ε₀   = e²/(4παℏc)      残差 ~3e-10% (与 29号一致)")
put(f"    ✓ G·ε₀ = e²/(4πα·m_P²)   残差 ~3e-10%")
put(f"  ── 诚实边界 (勿伪称几何导出) ──")
put(f"    ⚠ 上述'正确公式'是传统 α 定义/质量标度的循环重排, 非 (κ,τ_v) 第一性导出;")
put(f"      α, e, m_P 均为测量锚 (v4 NG-X); 用户推导的 U_geo=U_class 反解 ε₀ 是循环论证")
put(f"    ✓ 真正含几何结构的是 29号 ε₀=q0²/(64π³c³κτℏα) 与 30号 G=c³/[ℏ(κ²+τ²)]")

report = "\n".join(L)
print(report)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "78_Gε0耦合恒等式审查修正报告.md")
with io.open(out, "w", encoding="utf-8") as fh:
    fh.write("# 78号 · G-ε₀ 耦合恒等式审查修正\n\n")
    fh.write("> 算法联盟 ROOT 最高权限 · 审查修正 · 2026-08-21\n\n```\n"+report+"\n```\n")
print("\n[报告已写入] "+out)
