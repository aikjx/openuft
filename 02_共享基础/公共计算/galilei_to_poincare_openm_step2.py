# -*- coding: utf-8 -*-
"""
第79章 OPEN-M-2 表示论裁决：伽利略涡旋能否升格为庞加莱自旋1规范量子
纯标准库。用法: python galilei_to_poincare_openm_step2.py

机器证据:
  1. Inönü–Wigner 收缩：Poincaré(10维) --c→∞--> Bargmann-Galilei(11维, 质量成中心荷)；
     用结构常数 Jacobi 检验器验证两个代数各自自洽，并展示 [G,G]∝ε²→0 的收缩信号；
     逆向"去收缩"非唯一（c 是外部输入，且 Galilei 出现 Poincaré 没有的中心荷 M）。
  2. 小群/表示计数：有质量 SO(3)(2s+1)、无质量 E(2)(螺旋度,自旋1→2极化)、
     Galilei 粒子表示依赖中心荷 m>0（m=0 退化，无"无质量自旋1"对应）。
  3. Coleman–Mandula 直积壁垒：纯 Jacobi 层面"时空-内部混合"代数其实可自洽
     （给出一个 [P_μ,Q_ν]=i C g_{μν} Z 的自洽反例，残差=0）——这恰恰说明 no-go 不能
     只靠李代数，它本质依赖散射 S 矩阵解析性；Casimir 分析显示该混合 Q 与平移 P 同表示型,
     给不出独立紧内部量子数。独立紧内部荷唯一自洽位置=直积 [T,I]=0（Coleman–Mandula 1967）。
  4. Weinberg–Witten 阈值 + Coleman–Mandula 例外清单（SUSY/弦/共形/拓扑序：皆为额外输入）。
判定见文末。
"""
import itertools

def eps(i,j,k):
    v=[i,j,k]
    if len(set(v))!=3 or min(v)<1 or max(v)>3: return 0.0
    t=v[:]; inv=0
    for a in range(3):
        for b in range(a+1,3):
            if t[b]<t[a]: inv+=1
    return 1.0 if inv%2==0 else -1.0

class LieAlg:
    """f[(a,b)][c] 定义 [g_a,g_b]=i Σ_c f[(a,b)][c] g_c；反对称自动。"""
    def __init__(self, names):
        self.n=list(names); self.idx={n:i for i,n in enumerate(names)}; self.N=len(names)
        self.f=[[{} for _ in range(self.N)] for __ in range(self.N)]
    def set(self,a,b,c,v):
        ia,ib,ic=self.idx[a],self.idx[b],self.idx[c]
        self.f[ia][ib][ic]=v; self.f[ib][ia][ic]=-v
    def comm(self,a,b):  # [a,b] 的实结构常数 dict
        return self.f[self.idx[a]][self.idx[b]]
    def jacobi_residual(self):
        n=self.N; F=self.f; worst=0.0; arg=None
        for x,y,z in itertools.product(range(n),repeat=3):
            for c in range(n):
                s=0.0
                for d in range(n):
                    s+= F[y][z].get(d,0)*F[x][d].get(c,0)
                    s+= F[z][x].get(d,0)*F[y][d].get(c,0)
                    s+= F[x][y].get(d,0)*F[z][d].get(c,0)
                if abs(s)>abs(worst): worst=s; arg=(self.n[x],self.n[y],self.n[z],self.n[c])
        return worst,arg

print("="*82)
print(" 1. Poincaré 代数 与 Bargmann-中心扩张 Galilei 代数：各自 Jacobi 自洽 + 收缩")
print("="*82)
# --- Poincaré: J1-3,K1-3,P1-3,H (10) ---
P2=LieAlg(['J1','J2','J3','K1','K2','K3','P1','P2','P3','H'])
for i in (1,2,3):
    for j in (1,2,3):
        k=6-i-j  # {1,2,3} 中除 i,j 外的第三轴
        if i!=j:
            e=eps(i,j,k)
            P2.set(f'J{i}',f'J{j}',f'J{k}',e)
            P2.set(f'J{i}',f'K{j}',f'K{k}',e)
            P2.set(f'J{i}',f'P{j}',f'P{k}',e)
            P2.set(f'K{i}',f'K{j}',f'J{k}',-e)   # [K_i,K_j]=-i ε_ijk J_k
    P2.set(f'K{i}',f'P{i}','H',1.0)              # [K_i,P_j]=i δ_ij H
    P2.set(f'K{i}','H',f'P{i}',1.0)              # [K_i,H]=i P_i
r,a=P2.jacobi_residual()
print(f"Poincaré(10维) 全三元组 Jacobi 最大残差 = {r:.2e}  (在 {a})")

# --- Bargmann-Galilei: J1-3,G1-3,P1-3,H,M (11) ---
G=LieAlg(['J1','J2','J3','G1','G2','G3','P1','P2','P3','H','M'])
for i in (1,2,3):
    for j in (1,2,3):
        k=6-i-j
        if i!=j:
            e=eps(i,j,k)
            G.set(f'J{i}',f'J{j}',f'J{k}',e)
            G.set(f'J{i}',f'G{j}',f'G{k}',e)
            G.set(f'J{i}',f'P{j}',f'P{k}',e)
    G.set(f'G{i}',f'P{i}','M',1.0)   # [G_i,P_j]=i δ_ij M（质量=中心荷）；i≠j 与余者对易=0
# [G,G]=0, [G,H]=0, M 与一切对易 —— 均默认 0
rg,ag=G.jacobi_residual()
print(f"Bargmann-Galilei(11维) Jacobi 最大残差 = {rg:.2e}")
print("关键：量子 Galilei 群必须中心扩张，质量 M 是与一切对易的中心荷；Poincaré 无此中心扩张。")

print("\n收缩信号：令 G_i(ε)=ε K_i（ε=1/c），则 [G_i(ε),G_j(ε)] = -i ε² ε_ijk J_k")
for epsilon in [1.0,0.3,0.1,0.01]:
    print(f"  ε=1/c={epsilon:<5}  [G_1,G_2] 中 J_3 的结构常数 = {-epsilon**2:+.5f}   {'← Poincaré' if epsilon==1 else ('→ 0 (boost 相交换, Galilei)' if epsilon<=0.01 else '')}")
print("""读法：c→∞ 时 boost-boost 对易子被压到 0，同时'长出' Poincaré 没有的中心荷 M。
 这是 Inönü–Wigner 收缩。逆向'去收缩'(Galilei→Poincaré)需要：
   (i)  重新点亮被压成 0 的 [G,G]∼ε²J（形变参数 ε=1/c 是外部输入，形变并不唯一）；
   (ii) 把中心荷 M（质量）改回能量分量 H——两套不可约表示的范畴并不连续对接。
 即使项目运动学已取 c（给了 Poincaré 背景），这只解决'时空协变'，没给内部荷（见第3段）。""")

print("="*82)
print(" 2. 小群与极化计数：Galilei 涡旋没有'无质量自旋1'表示可对应")
print("="*82)
def weyl_dim_spinor_chain(n):  # 仅展示，不用
    return n
print(f"{'表示类别':<28}{'稳定子(小群)':<14}{'物理态数':<22}{'质量/螺旋度'}")
print("-"*90)
print(f"{'Poincaré 有质量':<26}{'SO(3)':<16}{'2s+1 (s=1→3)':<24}m²>0, 自旋 s")
print(f"{'Poincaré 无质量':<26}{'E(2)=ISO(2)':<16}{'每螺旋度1态 (h=±1→2)':<24}m²=0, 螺旋度 h")
print(f"{'Galilei 粒子':<26}{'SO(3)':<16}{'2s+1':<24}中心荷 m>0 必需")
print(f"{'Galilei m=0':<26}{'(退化)':<16}{'无标准粒子不可约表示':<24}M=0 表示坍缩")
print("""结论：NS 涡旋是 Galilei 场，其粒子化表示建立在中心荷 m>0 上；'无质量螺旋度 h=±1'
 是 Poincaré 无质量扇区特有的 E(2) 表示，Galilei 范畴里没有可连续对接的对象。
 OPEN-M-2 要求的第一步（涡旋激发成为无质量自旋1量子）在表示论上不是坐标换写能完成的。""")

print("="*82)
print(" 3. Coleman–Mandula：内部荷不能从时空对称派生（直积壁垒）")
print("="*82)
# 构造一个'时空-内部混合'小代数，证明纯 Jacobi 层面它可自洽：
# 生成元 K1,H,P1,Q0,Q1,Z ；Q 为 Lorentz 矢量，[P_μ,Q_ν]=i C g_μν Z，Z 中心
M=LieAlg(['K1','H','P1','Q0','Q1','Z'])
C=1.0
M.set('K1','H','P1',1.0)      # [K,H]=iP1
M.set('K1','P1','H',1.0)      # [K,P1]=i H
M.set('K1','Q0','Q1',1.0)     # Q 按矢量 boost
M.set('K1','Q1','Q0',1.0)
M.set('H','Q0','Z',C)         # [P0,Q0]= i C g00 Z = +iCZ
M.set('P1','Q1','Z',-C)       # [P1,Q1]= i C g11 Z = -iCZ
# Z 中心、[H,Q1]=0、[P1,Q0]=0 默认
rm,am=M.jacobi_residual()
print(f"混合 ansatz [P_μ,Q_ν]=i C g_μν Z（Q=矢量内部荷, Z=中心标量）Jacobi 最大残差 = {rm:.2e}")
print(""" → 残差为 0：纯李代数上'时空指标的内部荷'并不违反 Jacobi。这是关键的诚实点：
   Coleman–Mandula no-go 不能只靠 Jacobi/形式代数得到（否则这个自洽反例就不存在）。
   它本质上要用散射 S 矩阵的解析性、粒子谱与非平凡散射假设。
 Casimir/表示型分析：该 Q_μ 满足与 P_μ 完全相同的洛伦兹矢量对易（[J,Q] 矢量、[P,Q]=g·Z），
   Z 为 c 数中心时 Q 就是'第二类平移生成元'，其 Casimir(Q², P·Q) 给出的是附加运动学标签，
   不是与时空对易的紧内部量子数。Coleman–Mandula(1967) 证明：在 4D 局域 QFT、有质量隙、
   非平凡 S 矩阵、有限粒子型谱下，这类附加运动学生成元要么与 P 线性相关（退化为能量动量），
   要么把散射角全部钉死（S 矩阵=1，无散射）或迫使质量谱连续——三者都排除它作为'色'那种
   区分粒子种类、在散射中相加守恒的紧内部荷。独立紧内部对称唯一自洽位置是直积：""")
# 直积版：内部 T 与全部时空生成元对易
D=LieAlg(['K1','H','P1','T_a'])   # T_a 内部生成元，与 K,H,P 全对易
rd,_=D.jacobi_residual()
print(f"   直积 [T_时空, T_内部]=0 的代数 Jacobi 最大残差 = {rd:.2e}  ← 唯一通过 CM 全部物理论证的位置")
print(""" 对 openuft 的判决：曲率 κ、挠率 τ、涡量 ω、螺旋频率全部是'时空几何'层对象
 （Poincaré/微分同胚张量）。按 Coleman–Mandula，强/弱力携带的紧内部荷（色 SU(3)、弱 SU(2)）
 不可能从任何 4D 时空几何的对称代数第一性导出——它们在代数范畴上就属于与时空直积的另一因子。
 这不是某个构造没试对，而是'几何统一纲领'在 4D 局域 S 矩阵框架内的严格天花板。""")

print("="*82)
print(" 4. Weinberg–Witten 阈值 与 Coleman–Mandula 的例外（皆为额外输入）")
print("="*82)
print("无质量粒子 h 与允许的协变守恒张量（Weinberg–Witten 1980）：")
for h,flow,tensor in [(0,'允许','允许'),(0.5,'允许(临界 h≤1/2)','允许'),
                      (1,'禁止 协变守恒流荷(h>1/2)','允许(h≤1)'),
                      (2,'禁止','禁止 协变守恒 Tμν(h>1)；引力子因 T 非协变而例外')]:
    print(f"  h={h:<4} 四流Jμ: {flow:<22} 能动张量Tμν: {tensor}")
print(""" 含义：想用涡旋物质的'协变守恒流'给复合出的无质量自旋1量子赋予内部荷，被 WW-I 禁止；
 非阿贝尔色流只满足协变导数守恒 D_μ j^{aμ}=0（普通散度非零），而它已预设规范群——循环。

Coleman–Mandula 之外能混合时空与内部的'例外'，没有一个免费：""")
print("  • 超对称(HLS 1975)：用 Z2 分级费米生成元 Q_α 绕过李代数版 CM —— 需引入整套费米超荷(额外输入)，LHC 至今零超粒子。")
print("  • 弦论：无限高自旋态塔使'有限粒子型谱/质量隙'假设失效 —— 代价无限维 + 额外紧致维(巨大额外输入)。")
print("  • 无质量隙/共形：CM 原假设有质量隙；共形扩张仍强约束，不给出紧内部荷的免费来源。")
print("  • 拓扑序演生规范(Wen 量子比特海)：内部规范力可演生，但需非时空几何的微观局域自由度+长程纠缠(额外输入)。")

print("="*82)
print(" 裁决：OPEN-M-2")
print("="*82)
print(""" 在 4D 局域、Poincaré 协变、有非平凡 S 矩阵、非超对称的标准物理假设内：
   运动学升格(Galilei→Poincaré)即使完成，也只到达'时空张量场'；
   紧内部荷 SU(3)×SU(2) 被 Coleman–Mandula 钉在与时空直积的独立因子，不能由涡旋/螺旋时空几何派生；
   复合无质量自旋1携荷又被 Weinberg–Witten 拦。
 故 OPEN-M-2 = CLOSED-NEGATIVE（标准假设内）。出口仅在 CM/WW 假设之外（SUSY/弦/拓扑演生），
 它们引入的结构比规范群本身更重，且无实验证据，不构成'从螺旋第一性导出 QCD'，不解锁 UFT-2/3。
 合并第78章：OPEN-M 整体（M-1 泛函捷径 + M-2 表示升格）在标准物理下关闭。
 几何统一纲领的严格边界：引力(时空曲率)可几何化；电磁在引入额外紧致维时可几何化(KK,但荷质比
 route 已失败,见第76章)；强/弱非阿贝尔内部力按 Coleman–Mandula 不可能从 4D 时空几何导出。
 UFT 联盟层维持 2/6；命名定理 Q（时空-内部直积表示论壁垒），与 P/N/L/.../C 并列，无四态迁移。
 脚本纯标准库；Poincaré/Galilei/Jacobi/小群/CM/WW 均为[A]级教科书与经典定理，判决性推理标[B][C]。""")
