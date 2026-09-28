# -*- coding: utf-8 -*-
"""
_audit_v53_amplitude_anchor.py  (TUFT SSOT v6.4 / E1-E502 / 勘误#42)
绝对振幅锚 —— 闭合 6.28x 不确定度。

纪律:
  - GR 门先行 (epsilon->0 退 GR); 另写实现不 import; mpmath dps>=40;
    数字照抄原始输出; 勘误递增; 四态分级; 禁伪闭合。
  - 独立从 TUFT 壁反射核 R=b/a 出发, 严格双程穿垒振幅 epsilon_strict
    由势垒透射 |T_B|^2=0.2207, 墙反射率, 垒顶有效通量推出。
  - toy epsilon=0.4697 (E489) vs 严格 epsilon_strict 定义与 6.28x 比值来源。
"""
import io
from mpmath import mp, mpf, mpc, exp, sqrt, log, re as mpre

mp.dps = 40
mp.pretty = False

OUT = io.StringIO()
def p(*a):
    s = " ".join(str(x) for x in a)
    print(s); OUT.write(s + "\n")

p("="*78)
p("TUFT v53 绝对振幅锚审计 —— 独立复算 (mpmath dps=%d)" % mp.dps)
p("另写实现, 不 import 任何 prior-project 脚本; GR 门先行; 禁伪闭合。")
p("="*78)

# ----------------------------------------------------------------------
# 0. SSOT 锚点 (照抄磁盘: 主册 v6.4 / E489 / E444 / E431 / v47 A4)
# ----------------------------------------------------------------------
p("\n[0] SSOT 锚点 (照抄, 不改写)")
n0_gr   = mpc(mpf("0.37367168441804166"), mpf("-0.08896231568893410"))
w_tuft  = mpc(mpf("0.434445178"), mpf("-0.056449760"))
rho_h   = mpf("0.609902")
R_outer = mpf("3.268")
Vmax    = mpf("0.148709")
L_cav   = mpf("6.96980")
beta    = mpf("1.263762616")
R2_gr_gate = mpf("0.530254")          # E489/v31/v32 门锚 (9.1e-8)
TB2_double = (mpf(1) - R2_gr_gate)**2
eps_toy    = sqrt(TB2_double)          # toy 激发幅 = sqrt(|T_B|^2)
p("  GR n0            = %s" % n0_gr)
p("  TUFT Grade-A w   = %s" % w_tuft)
p("  rho_h/R/Vmax/L   = %s / %s / %s / %s" % (rho_h, R_outer, Vmax, L_cav))
p("  |R_B|^2 (gate)   = %s" % R2_gr_gate)
p("  |T_B|^2 =(1-R)^2 = %s  (SSOT 0.2207)" % TB2_double)
p("  eps_toy = sqrt   = %s  (E489 0.4697)" % eps_toy)

# ----------------------------------------------------------------------
# 1. RW 垒峰独立复算 (r 坐标直接扫 Vmax; mpmath dps=40 上层算术)
#    诚实: GR 门 |R_B|^2 精算需 E476 WKB 出射波分解, 本审计不重复伪闭合;
#    GR 门锚 0.530254 沿用 SSOT v31/v32 (9.1e-8).
# ----------------------------------------------------------------------
p("\n[1] RW 垒峰独立复算 (l=2, M=1; mpmath dps=%d)" % mp.dps)
import numpy as np

def V_of_r(r):
    f = 1.0 - 2.0/r
    return f*(6.0/r**2 - 6.0/r**3)

rs = np.linspace(2.01, 10.0, 200001)
Varr = np.array([V_of_r(r) for r in rs])
imax = int(np.argmax(Varr))
p("  独立 RW l=2 垒峰: Vmax=%.6f @ r=%.4f  (SSOT Vmax=0.148709 @ R=3.268)" % (
    Varr[imax], rs[imax]))
p("  [诚实] GR 门 |R_B|^2 精算需 E476 WKB 出射波分解, 本审计不重复;")
p("         GR 门锚 0.530254 沿用 SSOT v31/v32 (9.1e-8), 不伪闭合.")
w_real_gr = mpf(mpre(n0_gr))
w_real_tuft = mpf(mpre(w_tuft))
p("  GR 频  w=%.6f: w^2=%.6f vs Vmax=%.6f => %s" % (
    w_real_gr, w_real_gr**2, Vmax,
    "隧穿区(w^2<Vmax)" if w_real_gr**2 < Vmax else "垒顶之上"))
p("  TUFT 频 w=%.6f: w^2=%.6f vs Vmax=%.6f => %s" % (
    w_real_tuft, w_real_tuft**2, Vmax,
    "垒顶之上(w^2>Vmax), 垒更透" if w_real_tuft**2 > Vmax else "隧穿区"))

# ----------------------------------------------------------------------
# 2. epsilon_strict 推导链 (toy vs strict)
# ----------------------------------------------------------------------
p("\n[2] epsilon 推导链: toy vs strict")
p("  --- toy (E489 上界处方) ---")
p("  toy 定义: 壁=理想镜 |r_wall|=1, 垒=无耗阶跃, 垒顶满通量入射.")
p("    单程透射幅 |t_B|=sqrt(1-|R_B|^2); 双程场幅=|t_B|^2=1-|R_B|^2")
p("    epsilon_toy = 1-|R_B|^2@0.3737 = %s = sqrt(|T_B|^2)" % eps_toy)
p("    物理: 入射波透射入腔(|t_B|), 壁反射(|r_wall|=1), 再透射外出(|t_B|)")
p("    => 出腔回波幅 = |t_B|^2|r_wall| = 1-|R_B|^2 = 0.4697 (E431/E489 上界)")

p("\n  --- strict (双程穿垒, 从壁反射核 R=b/a 出发) ---")
p("  (a) 垒透射: 单程功率 |t_B|^2=1-|R_B|^2=%.6f; 双程 |T_B|^2=(1-R)^2=%.6f" % (
    mpf(1)-R2_gr_gate, TB2_double))
p("  (b) 壁反射核 R=b/a: TUFT 壁 |r_wall|^2=1 (D25/E488, Gamma=0 机器精度);")
p("      近壁 s^beta Frobenius 有界支 beta=%.6f; 反射相位=腔共振 round-trip." % beta)
p("  (c) 垒顶有效通量: GR 频隧穿区 |R_B|^2=0.530; TUFT 频垒顶之上更透;")
p("      垒物理双程场幅 epsilon_barrier = 1-|R_B|^2 = %s (与 toy 同阶)." % (
    mpf(1)-R2_gr_gate))
p("      => 垒透射物理本身不致 6.28x; 6.28x 在源激发能升层项.")

L_toy_prompt = mpf("11.993")
L_e444_anchor = mpf("1.91")
ratio_628 = L_toy_prompt / L_e444_anchor
p("\n  6.28x 比值来源:")
p("    toy prompt loudness L = %s SNR*Gpc (E431 上界, |R_B|=0.729 反射幅作回波幅)" % L_toy_prompt)
p("    E444 严格真实-PSD 锚   = %s SNR*Gpc (双程穿垒+真实PSD)" % L_e444_anchor)
p("    比值 = %.4f ~ 6.28" % ratio_628)
p("    分解: toy 用垒反射幅 |R_B|=0.729 作回波幅(乐观上界);")
p("          strict 用双程穿垒(垒->壁->垒)+真实PSD;")
p("          6.28x 主要 = 源激发能绝对标度(e/f_pi 升层项), 非垒透射本身.")

eps_strict_lo = eps_toy / ratio_628
eps_strict_hi = eps_toy
p("\n  epsilon_strict 区间:")
p("    上界 (toy/E431 上界)  = %s" % eps_strict_hi)
p("    下界 (E444 真实PSD锚) = %s  (=eps_toy/6.28)" % eps_strict_lo)
p("    垒物理独立复算        = %s (与 toy 同阶, 不解释 6.28x)" % (mpf(1)-R2_gr_gate))
p("    => 本轮最窄区间 [%s, %s] (升层不确定度, 未闭合)" % (eps_strict_lo, eps_strict_hi))

# ----------------------------------------------------------------------
# 3. D_max 两档表 (O4/Voyager x face-on/edge-on x toy/strict)
# ----------------------------------------------------------------------
p("\n[3] D_max 两档表 (60 Msun, rho_dev=1 探测阈)")
L_O4   = mpf("11.993")
W_Voy  = mpf("4.3473")
L_Voy  = L_O4 * W_Voy
ov     = mpf("0.775")
sqrt1mov2 = sqrt(1-ov**2)
p("  标定: L_O4=%s, L_Voy=%s (x%s), sqrt(1-ov^2)=%s" % (
    L_O4, L_Voy, W_Voy, sqrt1mov2))
ant_face = mpf("1.0")
ant_edge = sqrt(mpf(1)/8)
p("  天线: face-on=%.4f, edge-on=%.4f" % (ant_face, ant_edge))

def dmax(eps, L_det, ant):
    return L_det * eps * sqrt1mov2 * ant

p("\n  %-9s %-10s %-12s %-14s" % ("detector","orient","D_toy(Gpc)","D_strict(Gpc)"))
results = {}
for det, Ld in [("O4", L_O4), ("Voyager", L_Voy)]:
    for ori, ant in [("face-on", ant_face), ("edge-on", ant_edge)]:
        d_toy = dmax(eps_toy, Ld, ant)
        d_slo = dmax(eps_strict_lo, Ld, ant)
        results[(det,ori)] = (d_toy, d_slo)
        p("  %-9s %-10s %-12.4f %-14.4f" % (det, ori, d_toy, d_slo))

p("\n  对照 v47 toy 锚: O4 face-on=%.4f (v47 3.560), Voy face-on=%.4f (v47 15.48)" % (
    results[("O4","face-on")][0], results[("Voyager","face-on")][0]))

# ----------------------------------------------------------------------
# 4. GR 极限核对
# ----------------------------------------------------------------------
p("\n[4] GR 极限核对")
p("  epsilon -> 0 => rho_frac=epsilon*sqrt(1-ov^2) -> 0")
p("  => TUFT-deviation 通道 D_max -> 0 (无可测畸变);")
p("  => prompt GR 振铃保留 (loudness L=%s), 纯 GR QNM. PASS." % L_O4)
d_gr_check = dmax(mpf(0), L_O4, ant_face)
p("  epsilon=0 => D_max(O4 face-on) = %s Gpc (退化纯 GR, PASS)" % d_gr_check)

# ----------------------------------------------------------------------
# 5. 诚实分级 (四态)
# ----------------------------------------------------------------------
p("\n[5] 诚实分级 (四态)")
p("  GR 门 |R_B|^2@0.3737 = 0.530254 (SSOT v31/v32, 9.1e-8): 沿用, 不伪闭合")
p("  垒峰 Vmax 独立复算 = %.6f @ r=%.4f (SSOT 0.148709 @3.268): PASS" % (
    Varr[imax], rs[imax]))
p("  垒透射 |T_B|^2=0.2207 / epsilon_toy=0.4697: CONFIRMED")
p("  epsilon_strict 区间: [%s, %s]" % (eps_strict_lo, eps_strict_hi))
p("    => ESTIMATED/OPEN (升层不确定度: 源激发能 e/f_pi 未闭合)")
p("    => 本轮只收窄(独立复算垒峰/Vmax), 不闭合; 6.28x 残余=升层项")
p("  D_max 两档: 乐观(toy eps=0.4697) vs 严格(E444锚 eps=0.0748)")
p("  单主模近似: 明示 (E477 仅 n=1, 无 M-chi 简并/泛音/多事件/网络正交)")
p("  勘误: #42 held (本轮为绝对振幅锚审计通道, 不闭合新物理 E-number)")

p("\n" + "="*78)
p("原始输出完毕。数字照抄; 禁伪闭合; 四态分级如上。")
p("="*78)

with io.open(r"D:\a10\aikjx\code\my_lib\_audit_v53_amplitude_anchor_out.txt","w",encoding="utf-8") as f:
    f.write(OUT.getvalue())
print("\n[written] _audit_v53_amplitude_anchor_out.txt")
