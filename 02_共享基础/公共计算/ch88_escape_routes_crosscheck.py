# -*- coding: utf-8 -*-
# 第88章 独立交叉检验：三条剩余出路（额外物质族 / see-saw阈值 / 输入误差棒）
# 纯标准库。被对账仪器（均 exit 0，不改）：
#   unification_probe.py / so10_thresholds.py(55门禁) / so10_errorbar_propagation.py(10门禁)
import math
print("="*78)
print("[A] 矢量型完整代为何对统一'盲'：完整不可约多重态的 Dynkin 指标三群简并")
# 一代手征 SM 费米子 15 Weyl，按 (T3重数和, T2重数和, (3/5)ΣY²) 计
# Q(3,2,1/6), u^c(3*,1,-2/3), d^c(3*,1,1/3), L(1,2,-1/2), e^c(1,1,1)
T3 = 0.5*2 + 0.5 + 0.5                      # Q 弱二重态含2个 SU3 基础
T2 = 0.5*3 + 0.5                           # Q 含3色 + L
sY2 = 3*2*(1/6)**2 + 3*(2/3)**2 + 3*(1/3)**2 + 2*(1/2)**2 + 1.0
T1 = (3/5)*sY2
print("  一代手征 ΣT (SU3,SU2,U1) = %.4f, %.4f, %.4f" % (T3,T2,T1))
assert abs(T3-2)<1e-12 and abs(T2-2)<1e-12 and abs(T1-2)<1e-12
# 矢量(Dirac)代=手征+镜像 两份 Weyl；b 的物质项每 Weyl (2/3)T
db = (2/3)*(2*2)
print("  一个完整矢量(15态Dirac)代 Δb_i = (2/3)·4 = %.4f  (三群相等)" % db)
print("  独立仪器 unification_probe.py '10 Dirac/代' = 16/3 = %.4f = 2×(8/3)，方向同为(1,1,1)" % (16/3))
print("  -> h_ij:=Δb_i-Δb_j = 0：加任意多完整代只平移三耦合、不改两两差 => 表示层 no-go")

print("="*78)
print("[B] 输入耦合误差棒能否把 R3221 情形 C 推进可见区（独立重算 z）")
sLnM = 0.1049018863          # errorbar 仪器：C 情形 σ(ln M_GUT)，仅来自 α_em/s2w/αs 测量误差
MC   = 2.2929062775069996e16
lims = {"P03现代格点":5.39e15, "SU5锚点":1.20e16, "so10最宽松(含√2)":1.69e16}
for name,L in lims.items():
    z = math.log(MC/L)/sLnM
    edge2 = MC*math.exp(-2*sLnM)
    print("  对 %-16s 需下移 z=%.2fσ ;  C 的 -2σ 下沿=%.3e (>上限? %s)"
          % (name,z,edge2,"是,仍不可见" if edge2>L else "否"))
zexc = math.log(MC/lims["so10最宽松(含√2)"])/sLnM
print("  即便最宽松口径也要 %.2fσ（单侧）；对现代口径 %.1fσ" % (zexc, math.log(MC/lims["P03现代格点"])/sLnM))
print("  对照仪器 E7：ln(τ_C/Super-K)/σlnτ = 6.34σ（C 已稳在 SK 之上）")
print("  强子/短程系统差 σ(lnτ)=2.35 只移动 τ 不移动 M_GUT，且现代格点方向使 τ 变长")

print("="*78)
print("[C] 最强单分量阈值杠杆（重解，非乘系数）能否够到 Hyper-K=1e35")
# so10_thresholds.py §7：在 10+45+126 全谱简并点(M_GUT=1.99e17,α^-1=9.20,τ=7.87e37)，
# 45_H(8,1,1)_0 上移5 e-fold：弹性 -0.6110 -> M=4.874e16, τ=6.491e35（全表最有利的一行）
M0,tau0 = 4.874e16, 6.491e35
print("  最有利单分量 45_H(8,1,1)_0 上移 5 e-fold(分裂~e^5=%.0f倍): τ=%.3e yr, 仍是 HK 的 %.2f 倍"
      % (math.exp(5),tau0,tau0/1e35))
# 还需把 M 再压多少：τ∝M^4
need_log = math.log10(M0) - math.log10((1e35/tau0)**0.25 * M0)   # 需要的额外 Δlog10 M
extra_efold = abs(need_log)/0.6110*5
print("  要到 τ=1e35 还需 Δlog10M=%.3f => 该色八重态标量再上移 ~%.1f e-fold（累计分裂 ~%.0f 倍）"
      % (abs(need_log),extra_efold,math.exp(5+extra_efold)))
print("  且该点 α_GUT^-1=9.20 已逼近强耦合；即同时付'单分量调谐分裂'+'失去微扰控制'两笔代价")

print("="*78)
print("[D] see-saw 必需的 126_H 与缺位 120_H 的阈值定价（读数自 55 门禁仪器，exit0 复跑）")
print("  完整多重态整块搬到 B-L：M_GUT 到 1e-12 不动（对合性把整块 Δb 吸成公共平移）")
print("   10+45 全谱: α^-1=39.92 τ=1.481e39 ; 再加126: α^-1=9.20 τ=7.867e37（都远超 HK）")
print("  120_H 整块: α^-1=-15.37（出微扰分支,τ无定义）；只留中性二重体: α^-1=-2.48 仍出分支")
print("  120_H 的 |B-L|=2 色单态 Q=±1 无中性 => 补它也给不出 B-L 破缺（替不了 126 的 Δ_R）")
print("="*78)
print("结论：额外完整代=表示层no-go；see-saw阈值不降价反近强耦合；输入误差棒2.9σ(最宽)/13.8σ(现代)")
print("      第85章列的三条剩余出路在独立仪器上一致被封；几何输入 0/5，UFT 维持 2/6。")
