# -*- coding: utf-8 -*-
"""
第76章 OPEN-7 正面攻关：非微扰尺度自发生成（维度转化 / QCD 质量间隙）能否解锁 UFT-3
纯标准库，机器精度。用法: python dimensional_transmutation_open7.py

内容:
  1. 1圈 beta 函数积分 -> RG 不变量 Lambda = mu*exp(-2pi/(b0 alpha_s(mu)))，多点数值验证 mu dLambda/dmu = 0
  2. 夸克阈值分段跑动 (nf=6/5/4/3) -> Lambda^(3,4,5)，对照 PDG 2圈匹配值
  3. 质量间隙与强子质量: m_hadron/Λ 为动力学锁定的纯数（格点 QCD 可从 g3 单独算出）
  4. 三棵尺度树 (L_P / v / Λ_QCD) -> 温度/密度/硬度/电导/声速 等宏观量的尺度归属
  5. 统一旋钮总账: SM 19 个自由参数分类 + UFT-1..6 对账（维度转化是否把 nullity 打到 0）
所有外部权威值 (PDG/CODATA) 在输出中显式标注 [PDG]/[CODATA]，1圈自算值标注 [1loop]。
"""
import math

def L(k, v):
    print(f"{k:52s} = {v}")

# ---------- 常数（CODATA2018/PDG，与 unification_ladder.py 口径一致）----------
hbar = 1.054571817e-34      # J s
c    = 2.99792458e8        # m/s
e    = 1.602176634e-19     # C
kB   = 1.380649e-23        # J/K
eps0 = 8.8541878128e-12
G    = 6.67430e-11         # SI
Ggev = 6.70883e-39         # GeV^-2
alpha = 7.2973525693e-3
m_e  = 9.1093837015e-31    # kg
m_e_gev = 0.51099895e-3    # GeV
m_p_kg = 1.67262192369e-27
m_p  = 0.938272088         # GeV
MZ   = 91.1876
alphas_MZ = 0.1179         # [PDG] 2022 world average
mt, mb, mc = 172.76, 4.18, 1.27  # GeV 阈值
v_h = 246.22
GF = 1.1663787e-5
GEV_J = 1.602176634e-10    # 1 GeV in J
GEV_M = hbar*c/GEV_J       # 1 GeV^-1 in m

def b0(nf):  # 1圈 QCD beta: mu dg/dmu = -b0 g^3/(16pi^2)
    return 11.0 - 2.0*nf/3.0

def inv_as_run(ainv0, mu0, mu, nf):
    # d(alpha_s^-1)/d ln mu = b0/2pi
    return ainv0 + (b0(nf)/(2*math.pi))*math.log(mu/mu0)

def Lambda_of(mu, as_mu, nf):
    return mu*math.exp(-2*math.pi/(b0(nf)*as_mu))

print("="*78)
print(" 1. RG 不变量推导与多点验证：Λ = μ·exp[-2π/(b₀ α_s(μ))]，μ dΛ/dμ = 0")
print("="*78)
# 固定约定 nf=5（不跨阈值），从 MZ 出发跑 1 圈，在多个 μ 用"跑动后的 α_s"重算 Λ
print(" [约定 nf=5, b0=23/3=%.5f；α_s(MZ)=%.4f]" % (b0(5), alphas_MZ))
ainv_MZ = 1/alphas_MZ
Lam_ref = Lambda_of(MZ, alphas_MZ, 5)
for mu in [MZ, 10.0, 160.0, 1000.0, 10000.0]:
    ainv = inv_as_run(ainv_MZ, MZ, mu, 5)
    a = 1/ainv
    lam = Lambda_of(mu, a, 5)
    L(f"μ={mu:8.2f} GeV  α_s(μ)={a:.5f}  Λ(μ)", f"{lam:.6e} GeV")
L("最大相对散布 max|Λ-Λref|/Λref", f"{max(abs(Lambda_of(mu,1/inv_as_run(ainv_MZ,MZ,mu,5),5)-Lam_ref)/Lam_ref for mu in[MZ,10,160,1000,10000]):.2e}  (1圈解析恒等=0)")
L("Λ^(5) [1loop 裸值]", f"{Lam_ref*1000:.1f} MeV")

print()
print("="*78)
print(" 2. 夸克阈值分段跑动（连续匹配）+ 对照 PDG")
print("="*78)
# MZ -> mb : nf=5 ; mb -> mc : nf=4 ; mc 以下 : nf=3，α_s 连续
a5 = alphas_MZ
a4 = 1/inv_as_run(1/a5, MZ, mb, 5)
a3 = 1/inv_as_run(1/a4, mb, mc, 4)
L("α_s(m_b) 连续匹配", f"{a4:.4f}")
L("α_s(m_c) 连续匹配", f"{a3:.4f}")
lam5 = Lambda_of(mb, a4, 5)   # 用 nf5 区段表达的 Λ5（在 mb 处算）
lam4 = Lambda_of(mc, a3, 4)   # Λ4
lam3 = Lambda_of(mc, a3, 3)   # Λ3
L("Λ^(5) [1loop 分段]", f"{lam5*1000:.1f} MeV")
L("Λ^(4) [1loop 分段]", f"{lam4*1000:.1f} MeV")
L("Λ^(3) [1loop 分段]", f"{lam3*1000:.1f} MeV")
L("Λ^(5) [PDG 2圈+退耦匹配]", "213 ± 9 MeV   [PDG2022]")
print(" 说明：1圈+连续匹配系统性偏低（缺2圈项与退耦阶跃）；2圈匹配给出 0.213 GeV。")
LAM = 0.213  # 后续统一采用 PDG Λ5

print()
print("="*78)
print(" 3. 质量间隙：无量纲 g₃ → 有量纲强子质量，系数被动力学锁定（非自由旋钮）")
print("="*78)
hadrons = [("质子 m_p", 0.938272), ("中子 m_n", 0.939565), ("ρ 介子", 0.775),
           ("核子-ρ 典型禁闭尺度 4πf_π", 4*math.pi*0.0922), ("π 介子(Goldstone)", 0.1350)]
for name, m in hadrons:
    L(f"{name:28s} /Λ_QCD", f"{m/LAM:6.3f}")
print(" → m_p/Λ=4.40、m_ρ/Λ=3.64：无量纲纯数，格点 QCD 只用 g3（+可忽略流夸克质量）")
print("   即在离散化后唯一尺度 a 由 g3 经同一维度转化锁定，从第一性算出，误差百分之几 [A/格点]。")
L("质子质量中 QCD（胶子+迹反常）占比", "≈99%  [与第71章 99.26% 同口径]")
L("π 介子为何远轻 (m_π²∝(m_u+m_d)Λ，手征 Goldstone)", f"m_π/Λ={0.135/LAM:.2f}  [A 手征微扰论]")
print(" 质量间隙解析存在性 = 克雷研究所千禧年问题（OPEN-7）；格点数值证据 [A]，解析证明 OPEN。")

print()
print("="*78)
print(" 4. 三棵尺度树 → 全部宏观物理量的尺度归属")
print("="*78)
# 树A：引力树
Lp = math.sqrt(hbar*G/c**3)
mP = 1/math.sqrt(Ggev)
mPr = mP/math.sqrt(8*math.pi)
print("[树G] 输入 {G, ħ, c}")
L("普朗克长度 L_P", f"{Lp:.3e} m")
L("普朗克质量 m_P", f"{mP:.3e} GeV；约化 {mPr:.2e} GeV")
# 树H：电弱树
print("[树H] 输入 {无量纲规范耦合 g,g',λ,Yukawa y_f + 一个维象参数 μ_H²}")
g2 = 2*math.sqrt(2)*m_p*0  # placeholder no-op
g = 0.653
gp = math.sqrt((4*math.pi*alpha)/(1-0.2231))  # 仅展示
lam4p = (125.1/v_h)**2/2
L("Higgs vev v", f"{v_h} GeV（来自维象 μ_H²=−(88.4 GeV)²，不是维度转化）")
L("m_W=gv/2", f"{g*v_h/2:.2f} GeV [PDG 80.38]")
L("λ (Higgs 自耦合)=(m_H/√2/v)²", f"{lam4p:.4f} [PDG mH=125.1]")
ye = math.sqrt(2)*m_e_gev/v_h
L("电子 Yukawa y_e=√2 m_e/v", f"{ye:.3e}（无量纲但来源未知）")
# 树Q：QCD树（唯一纯维度转化）
print("[树Q] 输入 {无量纲 g3} —— 唯一不含量纲输入的尺度树")
L("Λ_QCD = μ e^{-2π/(b0 α_s)}", f"{LAM*1000:.0f} MeV")
L("质子质量 m_p≈4.40 Λ", "0.938 GeV（普通物质 99% 质量）")

print()
print("--- 4.1 原子/化学尺度 = 树H(y_e 给 m_e) × 树EM(α)，绑树Q 的核质量 ---")
ke_e2 = e**2/(4*math.pi*eps0)                 # J m
a0 = hbar/(m_e*c*alpha)
Eh = hbar**2/(m_e*a0**2)                     # Hartree
re = ke_e2/(m_e*c**2)
lamC = hbar/(m_e*c)
L("Bohr 半径 a0=ħ/(m_e c α)", f"{a0:.4e} m  [5.29e-11]")
L("Hartree 能量 E_h=ħ²/(m_e a0²)", f"{Eh/e:.2f} eV  [27.21]")
L("经典电子半径 r_e", f"{re:.4e} m；r_e:λ̄C:a0 = α²:α:1 = {alpha**2:.3e}:{alpha:.3e}:1")
L("r_e/λ̄C 检验", f"{re/lamC:.6f}  (应=α={alpha:.6f})")

print("--- 4.2 密度（质量来自树Q，体积来自树EM）---")
rho_atom = m_p_kg/a0**3
L("原子数密度尺度 m_p/a0³", f"{rho_atom:.2e} kg/m³（实测量属 2e3–2e4，同尺度树，密堆系数 O(10⁻¹)）")

print("--- 4.3 硬度/体积模量（纯树EM：静电能密度）---")
B_atom = Eh/a0**3
L("原子压力尺度 E_h/a0³", f"{B_atom:.2e} Pa")
L("实测金属体积模量", "(0.4–4)×10¹¹ Pa —— 同一尺度树乘成键/电子气 O(10⁻²) 因子")

print("--- 4.4 电导（量子尺度 e²/ħ + 树EM几何）---")
G0 = 2*e**2/(2*math.pi*hbar)  # 电导量子 2e²/h，h=2πħ
L("电导量子 G0=2e²/h", f"{G0:.4e} S  [7.748e-5]")
L("电导率尺度 G0/a0", f"{G0/a0:.2e} S/m；Cu 实测 5.96e7（平均自由程~40 nm≫a0，因子~40）")

print("--- 4.5 声速（EM 恢复力 + QCD 惯性）---")
A = 20.0
vs = alpha*c*math.sqrt(m_e/(A*m_p_kg))
L("v_s≈αc·√(m_e/(A m_p))", f"{vs:.2e} m/s（实测固体 2e3–6e3，同尺度树）")

print("--- 4.6 温度（k_B T 只是能量单位换算，非独立本源）---")
for nm, en in [("室温 300 K", 0.02585), ("化学键", 1.0), ("Hartree", Eh/e),
               ("太阳核心", 1.3e3), ("核结合/每核子", 1.0e6)]:
    L(f"{nm:16s} {en:g} eV", f"{en*11604.5:.3g} K")
print(" → 温度不是独立「力」：化学/硬度/电导树落 eV(树EM)，核温度落 MeV(树Q)，无独立温标树。")

print()
print("="*78)
print(" 5. 统一旋钮总账：维度转化能否把 nullity_dyn 打到 0？")
print("="*78)
L("Λ_QCD / v（强-电弱尺度比）", f"{LAM/v_h:.3e}  —— 无量纲但两树各自独立，无机制关联")
L("m_p / m_P（引力等级）", f"{m_p/(mP):.3e}  —— 19 个数量级，等级问题")
L("α_s(MZ) 本身", f"{alphas_MZ} —— 无量纲输入，维度转化不解释它")
print("""
 SM 19 个自由参数（不含中微子质量）维度转化审计：
   3 个规范耦合 g3,g2,g1 ............ 无量纲，未被任何机制派生（GUT 近交汇=[C]）
   1 个 Higgs 维象参数 μ_H² ......... 量纲！EW 尺度 v 的真实来源（CW 维度转化=[C]，SM 内不成立）
   1 个 λ ........................... 无量纲
   6 夸克 + 3 轻子 Yukawa ........... 无量纲，跨 10⁶（y_e=2.9e-6 ~ y_t≈1），无机制
   4 CKM + 1 θ_QCD ................. 无量纲（θ<1e-10 强 CP 问题）
 关键判定：
   QCD 扇区内部 nullity_scale = 0：g3 → Λ → 全部强子质量，O(1) 系数由动力学锁定、
                                    格点可算（不是自由旋钮）。这是全物理唯一已知的此类机制。
   全物理 nullity 仍 ≥ 4：跨树比值 {Λ/v, m_p/m_P, g3:g2:g1, Yukawa 谱} 无约束。
""")
print(" UFT-1..6 对账（第76章，加入维度转化机制后）")
uft = [("UFT-1 数学自洽", "✅", "RG/β 函数/QCD 重整化严格自洽 [A]"),
       ("UFT-2 四力统一", "❌", "维度转化只在 SU(3) 扇区内；不产出统一群/统一作用量"),
       ("UFT-3 常数派生", "❌", "强子/Λ 是 QCD 内的无量纲纯数（格点[A]），但非 openuft 公设派生，"
                              "且不锁定 α/G/Yukawa；跨树无量纲靶数=0"),
       ("UFT-4 观测复现", "❌/[A参照]", "是 QCD 本身复现强子谱，非 openuft 复现 SM"),
       ("UFT-5 可证伪预言", "✅", "强子谱/质量间隙分布可证伪（格点已验证到 %级）"),
       ("UFT-6 外部验证", "❌", "QCD 本身 reviewed；openuft 引入方式仍 unreviewed")]
for k, s, note in uft:
    print(f"  {k:14s} {s:9s} {note}")
print("""
 结论：维度转化是第68/69/70章+砖二封死几何路线后，唯一被物理实现的"形状→尺度"机制，
 它把"强子尺度从何而来/普通物质质量从何而来"解为无量纲耦合的红外产物；但它：
  (i) 是被 openuft 引入的重整化群动力学公设，无法由世界线螺旋几何导出（定理C/E/F/L）；
  (ii) 只统一 QCD 一棵树，Λ/v、引力、Yukawa 谱仍自由 —— UFT 联盟层维持 2/6。
 OPEN-7（质量间隙解析证明）、Coleman-Weinberg EW 尺度生成 [C]、GUT 三耦近交汇 [C]、
 量子引力给 m_P [C]，是把其余树也变成"无量纲输入→动力学锁定尺度"所需、但均未达成的四块砖。
""")
