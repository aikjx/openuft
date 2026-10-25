# -*- coding: utf-8 -*-
"""
算法联盟 · 统一场论攻破 · 第56期：攻破"θ=2 截断无关"的越界 —— 临界指数数值的截断依赖
================================================================================
日期   : 2026-10-24
对标   : 权威定本 §8(引力UV渐近安全, 称 θ=2 截断无关)、§12 UV-精算(g_* 截断无关严格证明)
引擎   : mpmath dps=40

攻破对象: OpenUFT §8 断言 β_g=2g-Bg²/(2π) 下 g_*=4π/B、θ=2 "坐标/截断无关",
          并把 θ=2 表述为普适临界指数。本卷用文献标准 FRG β 函数检验:
          (1) 玩具模型内 θ=2 是否真满足场重定义不变(数值+解析);
          (2) 进入真实 EH/R² 截断(文献 β 函数)后 θ 是否仍=2;
          (3) 判定"θ=2 截断无关"是普适物理还是单截断特例 → 推进/降级 UV-精算项。
"""
import json
import mpmath as mp
mp.mp.dps = 40
mpp = mp.mpf
pi = mp.pi
results = {"meta":{"date":"2026-10-24","engine":"mpmath dps=40","basis":"§8/§12 UV-精算"}}

print("="*72)
print("(1) 玩具模型 β_g=2g-Bg²/(2π): g_*=4π/B, θ=2 —— 严格检验场重定义不变性")
B = mpp('10')
# g_* = 4π/B
gst = 4*pi/B
# β'(g)=2-2·B·g/(2π)=2-B·g/π; θ=-β'(g_*)
theta = -(2 - B*gst/pi)
print("    g_*=4π/%.0f=%s, θ=-β'(g_*)=%s (解析应=2)" % (B, mp.nstr(gst,6), mp.nstr(theta,6)))
results["toy"] = {"B":str(B),"gstar":mp.nstr(gst,8),"theta":mp.nstr(theta,8)}
# 场重定义: g̃=F(g)=g+ag²  (任意 a), 检验 β̃'(g̃*) 与 θ 不变
for a in [mpp('0.7'), mpp('-0.3'), mpp('2.0')]:
    # F(g)=g+a·g², 反函数 g=g̃(g̃) 数值解
    F = lambda g: g + a*g*g
    # 求 g̃* = F(g*)
    gst_tilde = F(gst)
    # β 在 g̃ 空间: β̃(g̃)=F'(g)·β(g); 在不动点 θ=-β̃'(g̃*) 应=F''关系下仍=-β'(g*)=2
    # 数值: 对 g 微扰 dg, g̃=F(g), β̃(g̃)=F'(g)β(g), dβ̃/dg̃ = (d/dg̃)(F'β)
    eps = mpp('1e-6')
    g1 = gst; g2 = gst + eps
    Fp1 = 1 + 2*a*g1; Fp2 = 1 + 2*a*g2
    # β(g)=2g-Bg²/(2π)
    b1 = 2*g1 - B*g1*g1/(2*pi); b2 = 2*g2 - B*g2*g2/(2*pi)
    # β̃=F'·β; dβ̃/dg̃ = (β̃2-β̃1)/(F2-F1)
    bt1 = Fp1*b1; bt2 = Fp2*b2
    Ft1 = g1 + a*g1*g1; Ft2 = g2 + a*g2*g2
    dbeta_dgt = (bt2-bt1)/(Ft2-Ft1)
    theta_t = -dbeta_dgt
    print("    a=%.1f: g̃*=%s, θ(重定义后)=%s (不变性应=2)" % (float(a), mp.nstr(gst_tilde,6), mp.nstr(theta_t,6)))
    results.setdefault("reparam",{})[str(a)] = {"gtilde":mp.nstr(gst_tilde,8),"theta_tilde":mp.nstr(theta_t,8)}

print("\n"+"="*72)
print("(2) 进入文献真实截断后 θ 是否仍=2")
print("    (2a) Essential RG 单耦合 β_η(1-loop, d=4):")
print("         β_η = 2η + (1/3)((d-3)d-36)η² + (d-3)(d(d(d+19)-566)+1200)/(30(d-2))·η³")
# d=4: 2η + (1/3)(4-36)η² + (1)(4(4(23)-566)+1200)/(30·2)·η³
#     = 2η - (32/3)η² - (11.6)η³
d = mpp('4')
a2 = mpp('1')/3*((d-3)*d-36)          # -32/3
a3 = (d-3)*(d*(d*(d+19)-566)+1200)/(30*(d-2))  # -11.6
beta_eta = lambda e: 2*e + a2*e*e + a3*e*e*e
# 求不动点 η*: β=0, η≠0
e0 = mpp('0.1')
for _ in range(200):
    be = beta_eta(e0)
    bde = 2 + 2*a2*e0 + 3*a3*e0*e0
    e0 = e0 - be/bde
eta_st = e0
bpd = 2 + 2*a2*eta_st + 3*a3*eta_st*eta_st
theta_e = -bpd
print("    η*=%s, θ=-β'=%.6f  (文献 2411.00938: η*=0.16, θ=2.296)" % (mp.nstr(eta_st,6), float(theta_e)))
print("    ⇒ 玩具模型 θ=2 ≠ essential RG θ=%.6f" % float(theta_e))
results["essentialRG"] = {"eta_star":mp.nstr(eta_st,8),"theta":mp.nstr(theta_e,8)}

print("\n    (2b) Einstein-Hilbert 双耦合截断(文献 Acta Phys. Pol. B 40:3439):")
print("         NGFP G*=0.7012, Λ*=0.1715, θ=1.689±2.486i (优化 cutoff)")
print("    (2c) R² 高阶截断: NGFP 仍存在, θ 数值变化 (hep-th/0607128, 0511260)")
print("    ⇒ 跨截断/方案 θ 从 2(玩具) → 2.296(essential) → 1.689±2.486i(EH) 变化")
results["truncations"] = {
    "toy":"theta=2 (β_g=2g-Bg²/2π, 单耦合, 截断无关仅限此模型)",
    "essentialRG":"theta=2.296 (单耦合 essential, 1-loop)",
    "EH_two_coupling":"theta=1.689±2.486i (G*=0.7012, Λ*=0.1715)",
    "R2_higher":"NGFP存, θ变 (hep-th/0607128)"
}

print("\n"+"="*72)
print("(3) 判定")
verdict = ("'θ=2 截断无关'是玩具模型(β_g=2g-Bg²/2π 单耦合截断)的特例, 不是普适物理: "
           "玩具模型内 θ=2 确实满足场重定义不变(数值验证通过, 任意 a 下 θ 保持 2), "
           "但进入文献真实截断后 θ 依赖截断/方案(essential RG θ=2.296, EH 双耦合 θ=1.689±2.486i, "
           "R² 高阶 θ 变)。权威定本 §8 'θ=2 截断无关'存在越界: "
           "严格成立的仅是'同一截断内临界指数对场重定义不变'(普适), 数值 2 是单截断特例。"
           "⇒ UV-精算项(g_* 截断无关严格证明)维持开放, 且需降级: g_* 与 θ 的数值均非截断无关, "
           "仅 θ 的重参数化不变性为普适性质。'θ=2'不得表述为普适临界指数, 降为单截断结果。")
print("    → " + verdict)
results["verdict"] = verdict

with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\算法联盟_theta2截断依赖精算56_2026-10-24.json","w",encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\njson 已写入：算法联盟_theta2截断依赖精算56_2026-10-24.json")
