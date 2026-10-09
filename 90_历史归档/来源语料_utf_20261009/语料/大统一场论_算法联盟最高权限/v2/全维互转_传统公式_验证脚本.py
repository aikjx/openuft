"""
全维互转验证 · 螺旋框架量 ↔ 传统公式
算法联盟 ROOT 最高权限 · 零模糊 · 不拟合

目标: 逐一验证本框架的几何量 (v总=c / 频率ω / 曲率κ / 挠率τ / 半径R)
      能否与传统物理公式精确互转。每种量用两条路线计算, 校验机器零。

框架核心量 (电子):
  R   = 螺旋半径 = 约化康普顿波长 λ̄_C = ℏ/(m_e c)
  ω   = 频率    = c/R
  ρ   = 横向半径 = R/√(1+α²)
  b   = 螺距     = α·ρ
  κ   = 曲率    = ρ/R²
  τ   = 挠率    = b/R²
  v_⊥ = ωρ, v_∥ = ωb,  v总 = c   (光速分解)
"""
from mpmath import mp, mpf, sqrt, pi
mp.dps = 60

# ── 输入 (CODATA 2022) ──
c     = mpf('299792458')
hbar  = mpf('1.0545718176461565e-34')
me    = mpf('9.1093837015e-31')
e     = mpf('1.602176634e-19')
alpha = mpf('7.2973525693e-3')
eps0  = mpf('8.8541878128e-12')

# ── 框架导出量 ──
R   = hbar/(me*c)                 # 螺旋半径 = λ̄_C
w   = c/R                         # 频率
rho = R/sqrt(1+alpha**2)          # 横向半径
b   = alpha*rho                   # 螺距
kap = rho/R**2                    # 曲率
tau = b/R**2                      # 挠率
v_perp = w*rho                    # 横向速度
v_par  = w*b                      # 纵向速度

print("="*80)
print("全维互转验证 · 螺旋框架量 ↔ 传统公式")
print("="*80)
print(f"  电子: m_e={mp.nstr(me,6)} kg, α={mp.nstr(alpha,6)}, e={mp.nstr(e,6)} C")
print(f"  框架: R={mp.nstr(R,6)} m, ω={mp.nstr(w,6)} rad/s")
print(f"        ρ={mp.nstr(rho,6)} m, b={mp.nstr(b,6)} m")
print(f"        κ={mp.nstr(kap,6)} m⁻¹, τ={mp.nstr(tau,6)} m⁻¹")

def relerr(a, b):
    return abs(1 - a/b)

def show(name, fw, trad, note=""):
    er = relerr(fw, trad)
    lvl = 'S(机器零)' if er < mpf('1e-20') else ('A(<0.1%)' if er < mpf('1e-3') else '✗')
    print(f"  {name:<28} 框架={mp.nstr(fw,8):>14} 传统={mp.nstr(trad,8):>14} 误差{mp.nstr(er,3):>8} {lvl}  {note}")

print("\n" + "="*80)
print("【一】速度全维: v_⊥² + v_∥² = c²  (光速分解 ↔ |v|=c)")
print("="*80)
show("v_⊥²+v_∥²=c²", v_perp**2+v_par**2, c**2)
show("v_⊥=ωρ (圆周速度)", v_perp, w*rho)
show("v_∥=ωb (前进速度)", v_par, w*b)
print("  → 传统 |v|=c 在本框架中分解为横向圆周 ωρ + 纵向推进 ωb, 二者正交合成总光速。")

print("\n" + "="*80)
print("【二】频率 ↔ 能量/质量/动量 (普朗克 ↔ 爱因斯坦 ↔ 德布罗意)")
print("="*80)
E_fw = hbar*w                  # E = ℏω
E_tr = me*c**2                 # E = mc²
show("E=ℏω ↔ E=mc²", E_fw, E_tr, "E=ℏω=mc²")
m_fw = hbar*w/c**2             # m = ℏω/c²
show("m=ℏω/c² ↔ m_e", m_fw, me, "质量=频率")
p_fw = hbar*w/c                # p = ℏω/c
p_tr = me*c                    # p = mc
show("p=ℏω/c ↔ p=mc", p_fw, p_tr, "动量")
lamb = (2*mp.pi*hbar)/p_fw   # 德布罗意 λ = h/p
show("λ=h/p ↔ 2πR (螺旋周长)", lamb, 2*mp.pi*R, "德布罗意波长=螺旋周长")
lc = hbar/(me*c)               # 约化康普顿波长
show("λ̄_C=ℏ/(mc) ↔ R", lc, R, "约化康普顿波长=螺旋半径")

print("\n" + "="*80)
print("【三】曲率/挠率 ↔ 固有力 / 向心力 (牛顿 ↔ 几何)")
print("="*80)
F_c1 = me*w**2*rho             # 向心力 mω²ρ
F_c2 = me*c**2*kap             # 固有力 mc²κ
show("mω²ρ ↔ mc²κ (向心力)", F_c1, F_c2, "ω²ρ=c²κ")
# 牛顿极限: 若向心力由引力/电磁提供
# 电子静能 = 螺旋动能
E_kin = 0.5*me*v_perp**2
show("0.5·m·v_⊥² (经典动能)", E_kin, 0.5*me*(w*rho)**2, "恒等")

print("\n" + "="*80)
print("【四】α ↔ 电荷 (几何螺距比 ↔ 元电荷)")
print("="*80)
alpha_from_tau_kap = tau/kap
show("α=τ/κ (几何)", alpha_from_tau_kap, alpha)
e_fw = sqrt(4*mp.pi*eps0*hbar*c*alpha)   # e=√(4πε₀ℏcα)
show("e=√(4πε₀ℏcα) ↔ e", e_fw, e, "电荷=几何导出")

print("\n" + "="*80)
print("【五】κ²+τ² ↔ 频率/半径 (曲率挠率全维 ↔ 波动)")
print("="*80)
show("κ²+τ²=(ω/c)²", kap**2+tau**2, (w/c)**2, "核心恒等")
show("κ²+τ²=1/R²", kap**2+tau**2, 1/R**2, "半径恒等")

print("\n" + "="*80)
print("【六】量子条件 / 作用量")
print("="*80)
S = me*c*R                     # 作用量 = 动量×半径
show("S=pc·R ↔ ℏ", S, hbar, "最小作用量=ℏ")
show("ω·R=c (定义)", w*R, c)

print("\n" + "="*80)
print("互转汇总")
print("="*80)
print("""
  框架量          传统公式               互转关系
  ────────────────────────────────────────────────────────
  v_⊥, v_∥        |v|=c              v_⊥²+v_∥²=c² (正交分解)
  ω (频率)        E=ℏω, E=mc²        m=ℏω/c², E=ℏω=mc²
  p (动量)        p=mc, p=h/λ        p=ℏω/c=ℏ/R
  R (螺旋半径)     λ̄_C=ℏ/(mc)         约化康普顿波长=螺旋半径
  λ=2πR          λ=h/p (德布罗意)    德布罗意波长=螺旋周长
  κ (曲率)        a_c=ω²ρ=向心力      mc²κ=mω²ρ (固有力)
  α=τ/κ          e (元电荷)          e=√(4πε₀ℏcα)
  κ²+τ²          Klein-Gordon        □ψ=(κ²+τ²)ψ
  作用量 S        S=∮p·dq=nℏ         单圈 S=pc·R=ℏ

  ★ 互转本质: 所有传统公式都是上述几何量的【同一种写法】。
     频率是枢纽: m=ℏω/c² 把"质量"翻译成"频率";
     R 是枢纽:  λ̄_C=ℏ/(mc)=R 把"波长"翻译成"螺旋半径";
     (ω,c,ℏ) 三者构成换算单位系, 传统公式在其下重写。
  ★ 诚实边界: 这些是【恒等/定义重排】(TAUT), 非独立预言;
     它们证明框架与标准公式【一致】(自洽), 不产生新可检验预言。
""")
print("算法联盟最高权限 · 全维互转验证完成")
