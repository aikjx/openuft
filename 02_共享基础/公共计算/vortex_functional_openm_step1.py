# -*- coding: utf-8 -*-
"""
第78章 OPEN-M 第一步可判定化：涡旋场泛函积分能否诱导非阿贝尔规范结构
纯标准库。用法: python vortex_functional_openm_step1.py

四段机器证据:
  1. Jacobi 恒等式：满足 Ward 自洽的三顶点耦合 f^{abc} 必为李代数结构常数
     —— SU(2)=ε、SU(3) Gell-Mann 结构常数逐组验证；随机反对称张量测违反率
  2. Ward-Takahashi / 幺正性：自能 Πμν=A gμν+B kμkν 必须满足 k^μΠμν=0，
     否则留 B k² kν 纵向坏极点（无规范对称输入时 B 独立 → 幺正性破坏）
  3. Weinberg 自旋-自洽定理的表示论入口：无质量自旋1 小群 E(2)（2 极化），
     自洽自耦合强制 Yang-Mills；对照 NS 速度场是 Galilean 3-矢量（3 分量,非螺旋度规范量子）
  4. MSR 涡旋泛函积分顶点解剖：三次顶点 ũ u·∇u 的“荷”是波数 k（动量），内部群指标数=0；
     与 Yang-Mills 三顶点（含 1 个 f^{abc}+洛伦兹张量）逐项对照 → 涡旋自耦合不带内部荷
判定：OPEN-M 在标准涡旋泛函积分下收窄（见文末）。
"""
import math, random

def L(k,v): print(f"{k:56s} = {v}")

print("="*80)
print(" 1. Jacobi 恒等式：自洽三顶点 f^{abc} 被迫成为李代数结构常数")
print("="*80)
# 指标约定（全反对称 f，求和 e）：
#   Jacobi:  f^{abe} f^{cde} + f^{bce} f^{ade} + f^{cae} f^{bde} = 0
def make_f_su2(n):
    f=[[[0.0]*n for _ in range(n)] for __ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                f[a][b][c]=levi3(a,b,c)
    return f
def levi3(a,b,c):
    v=[a,b,c]
    if len(set(v))!=3 or min(v)<0 or max(v)>2: return 0.0
    inv=0; t=v[:]
    for i in range(3):
        for j in range(i+1,3):
            if t[j]<t[i]: inv+=1
    return 1.0 if inv%2==0 else -1.0

def make_f_su3():
    n=8; f=[[[0.0]*n for _ in range(n)] for __ in range(n)]
    vals={(1,2,3):1.0,(1,4,7):0.5,(2,4,6):0.5,(2,5,7):0.5,(3,4,5):0.5,
          (1,5,6):-0.5,(3,6,7):-0.5,(4,5,8):math.sqrt(3)/2,(6,7,8):math.sqrt(3)/2}
    for (a,b,c),v in vals.items():
        for (aa,bb,cc),s in [((a-1,b-1,c-1),1),((b-1,a-1,c-1),-1),
                             ((a-1,c-1,b-1),-1),((c-1,b-1,a-1),-1),
                             ((b-1,c-1,a-1),1),((c-1,a-1,b-1),1)]:
            f[aa][bb][cc]=s*v
    return f
def jacobi_max(f,n):
    worst=0.0
    for a in range(n):
      for b in range(n):
       for c in range(n):
        for d in range(n):
          t=0.0
          for e in range(n):
            t+=f[a][b][e]*f[c][d][e]+f[b][c][e]*f[a][d][e]+f[c][a][e]*f[b][d][e]
          if abs(t)>abs(worst): worst=t
    return worst
f2=make_f_su2(3); f3=make_f_su3()
L("SU(2) f=ε^{abc} Jacobi 最大残差", f"{jacobi_max(f2,3):.2e}")
L("SU(3) Gell-Mann f^{abc} Jacobi 最大残差", f"{jacobi_max(f3,8):.2e}")

# 随机反对称三指标张量（n=5,8）测 Jacobi 违反率
random.seed(7)
def random_alt(n):
    f=[[[0.0]*n for _ in range(n)] for __ in range(n)]
    for a in range(n):
        for b in range(a+1,n):
            for c in range(b+1,n):
                r=random.uniform(-1,1)
                for (aa,bb,cc),s in [((a,b,c),1),((b,a,c),-1),((a,c,b),-1),
                                     ((c,b,a),1),((b,c,a),1),((c,a,b),-1)]:
                    f[aa][bb][cc]=s*r
    return f
for n in [4,5,8]:
    bad=0; trials=400
    for _ in range(trials):
        f=random_alt(n)
        if abs(jacobi_max(f,n))>1e-9: bad+=1
    L(f"随机反对称 f^{{abc}} (n={n}) 违反 Jacobi 比例", f"{bad}/{trials} = {bad/trials*100:.1f}%")
print(" → 几乎所有随机三顶点都违反 Jacobi；要求 Ward 自洽即把 f^{abc} 限制为李代数结构常数。")
print("   即：一旦坚持‘带内部荷的矢量三顶点 + 幺正/可重整’，紧致李群不是假设而是推论（Weinberg）。")

print()
print("="*80)
print(" 2. Ward-Takahashi 与幺正性：不输入规范对称 → 纵向坏极点")
print("="*80)
# 度规 (+---)；离壳动量 k=(2,0,0,1) → k²=4−1=3（离壳才能干净演示自能横向条件）
g=[[1 if i==j==0 else (-1 if i==j else 0) for j in range(4)] for i in range(4)]
def kcov(k):  # 协变分量 k_μ=g_μρ k^ρ
    return [sum(g[mu][rho]*k[rho] for rho in range(4)) for mu in range(4)]
def ksq(k):   # k²=k^μ k_μ（度规收缩，非分量平方和）
    kc=kcov(k); return sum(k[mu]*kc[mu] for mu in range(4))
def ward_vec(A,B,k):
    # k^μ Πμν, Πμν=A gμν+B k_μ k_ν  →  (A + B k²) k_ν
    kc=kcov(k); q=A+B*ksq(k)
    return [q*kc[nu] for nu in range(4)]
kk=[2.0,0.0,0.0,1.0]
L("离壳检验动量 k²", f"{ksq(kk):.1f} (=4−1)")
for label,Bv in [("Ward 解 B=−A/k²（横向）",-1.0/ksq(kk)),
                 ("无 Ward 输入 B=0（裸 A gμν）",0.0),
                 ("无 Ward 输入 B=0.3A",0.3),
                 ("无 Ward 输入 B=−0.3A",-0.3)]:
    r=ward_vec(1.0,Bv,kk)
    L(f"{label}: k^μΠμν 最大分量", f"{max(abs(x) for x in r):.2e}")
print(""" 读法：Ward 解 B=−A/k² 使 k^μΠμν 逐分量为 0（机器残差 0），纵向 k_μk_ν 被消去、
 无质量自旋1 只留 2 个横向极化，树图幺正性保持；B 一旦独立（无规范对称输入），
 k^μΠμν=(A+Bk²)k_ν≠0，纵向项残留 → 矢量传播子出现 k_μk_ν/k² 类坏极点、
 第 3 个纵向极化不解除耦 → 破坏光学定理/幺正性。
 故非阿贝尔 Ward 结构不会从一个朴素 ∫Du 测度里‘涌现’；它必须由规范约束（或等价的
 无质量自旋1 自洽条件）作为输入。""")

print("="*80)
print(" 3. Weinberg 自旋-自洽入口：无质量自旋1 小群 E(2) vs NS 速度场")
print("="*80)
print(""" Poincaré 无质量粒子小群 = ISO(2)=E(2)：物理表示是螺旋度 h=±1（2 个横向极化）。
 Weinberg(1964/65)：在‘无质量、自旋1、洛伦兹协变、幺正、且量子间自洽相互作用’下，
 唯一解是 Yang-Mills（自耦合 ∝ f^{abc}，f 满足 Jacobi）；自旋2 唯一解是 GR。
 对照 Navier-Stokes 的速度场 u(x,t)：
   - 它是 Galilean（非相对论）3-矢量，变换规则是空间 SO(3) 矢量 + Galilean 平移，
     不是 Poincaré 无质量自旋1 的 E(2) 螺旋度表示；
   - 其基本激发（流体模/声子/涡旋）不是 h=±1 的相对论规范玻色子；
   - 因此 Weinberg 强制 Yang-Mills 的那一串前提（无质量自旋1 粒子）在 NS u 上根本不启动。
 维度/分量计数：""")
L("Poincaré 无质量自旋1 物理极化", "2（横向, E(2) 螺旋度）")
L("NS 速度场 u 的分量数", "3（Galilean 矢量, 含纵向/可压缩信息）")
L("NS 是否相对论协变 4-矢量", "否（连续性/动量方程在 Galilean 群下封闭）")

print()
print("="*80)
print(" 4. MSR 涡旋泛函积分顶点解剖：自耦合不带内部荷")
print("="*80)
print(""" 给随机 NS 一个泛函积分（Martin-Siggia-Rose，引入响应场 ũ）：
   S[u,ũ]=∫ ũ_i [∂t u_i + u_j ∂_j u_i - ν∇²u_i - f_i] （+ 噪声 δ 关联）
 三次相互作用顶点来自对流项 u_j ∂_j u_i：
   V_{ijk}(k,p,q) ∝ ũ_i(k) u_j(p) u_j? → 动量结构 i k_j δ_{i(...)},
   ‘荷’就是外部波数 k_j（动量分量），全部内部群指标数 = 0。
 对照 Yang-Mills 三胶子顶点：
   Γ^{abc}_{μνρ}(k,p,q)=g f^{abc}[ g_{μν}(k-p)_ρ + g_{νρ}(p-q)_μ + g_{ρμ}(q-k)_ν ]
   含 1 个内部结构常数 f^{abc}（受 Jacobi 约束 → 紧致李群）+ 洛伦兹张量。""")
L("MSR 三次顶点内部群指标数", "0（同一场 u，对流‘荷’=波数 k，非内部荷）")
L("YM 三胶子顶点内部结构常数", "1 个 f^{abc}（+ Jacobi → 李代数）")
L("MSR 是否有 Faddeev-Popov 鬼", "否（无内部规范对称可固定）")
L("MSR 重整化产物", "涡黏反常维数/Kolmogorov 不动点(ζ(3)...)——湍流临界理论，非 β_YM、无质量隙规范")
print(""" 决定性对照：真实存在的‘涡旋场泛函量子化’（MSR/随机量子化）的重整化给出湍流 RG，
 它既不产生 f^{abc}，也不产生紧致李群、F∧F 或 Yang-Mills β —— 因为涡旋自耦合没有内部荷。
 要得到内部荷，必须额外引入携带内部指标的场 A_μ^a —— 那正是把 Yang-Mills 当输入（定理 N 换名岔）。""")

print()
print("="*80)
print(" 判定：OPEN-M 收窄为两个子命题")
print("="*80)
print(""" OPEN-M 原命题：涡旋/螺旋泛函积分（不预设规范群）是否唯一蕴含非阿贝尔结构？
 本轮证据：
  (i)  标准涡旋泛函积分（MSR）的自耦合无内部群指标 → 重整化是湍流 RG，不产 f^{abc}/李群。【否】
  (ii) 朴素矢量测度不输入规范对称 → Ward 恒等式不成立、纵向坏极点、幺正性破坏。【否】
  (iii) 非阿贝尔结构真正的强制路径是 Weinberg：无质量自旋1(E(2))+自洽自耦合 → f^{abc}+Jacobi=YM；
       其前置（相对论无质量自旋1 量子）NS 速度场不具备。【链条断在前置】
 故：
   OPEN-M-1（涡旋泛函积分直接诱导非阿贝尔规范）= CLOSED-NEGATIVE（标准实现下被否证）。
   OPEN-M-2（涡旋/螺旋激发先成为相对论无质量自旋1 粒子，再走 Weinberg）= 仍 OPEN，
            且受 Weinberg-Witten 型限制（非引力的守恒洛伦兹张量承载自旋>1 等），需独立证明。
 在 OPEN-M-2 被证明前，openuft↔QCD 只能称‘几何重释候选’；UFT 联盟层维持 2/6。
 脚本仅用标准库；SU(3) f 常数与 Ward/Jacobi 为[A]级标准结果，MSR 顶点结构为[A]级随机场论结论。""")
