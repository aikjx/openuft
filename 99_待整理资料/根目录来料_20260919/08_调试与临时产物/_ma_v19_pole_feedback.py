# -*- coding: utf-8 -*-
"""
MainAgent v19 独立解析骨架（预审 / GR 门，非联盟产出，不分配最终 E 编号）
目标：在严格面积势 v18 几何（反射核，核->外垒龟坐标 L=6.9694M，往返 Δt=2L=13.9389M）
      下，用复频域腔反馈解析求 modified-QNM 复极点，量化表观频率/阻尼移动。
不做：垒顶 WKB 当定量、手设 epsilon 冒充结论、真实 PSD（绝对 SNR 依赖 epsilon，OPEN）。

物理（时间约定 e^{-i w t}，Schwarzschild QNM w = w_r - i w_i, w_i>0）：
  GR 孤立 l=2 n0 极点  w0 = 0.3736716844 - 0.0889623157 i   （权威，qnm/Leaver 13 位）
  反射核把到达核的波全反射（Neumann |r_core|=1），外垒把一部分透出（泄漏）、一部分反射回腔。
  波在 [核, 外垒] 空腔内每往返一次乘复因子 g（|g|=rho<1, arg g=phi）。
  自洽（极点）条件：  g * exp(i w Δt) = 1
   => 阻尼： |w_i| = -ln(rho)/Δt = ln(1/rho)/Δt        （rho->1 无阻尼实梳齿；rho->0 宽阻尼）
   => 频率梳齿： w_r,n = (2π n - phi)/Δt                （Fabry-Perot 等间隔腔模）

关键澄清（防自欺）：
  * 单个 QNM + 单个“同指数”延迟副本，在无限时长纯线性叠加下只是【改变复留数】，复极点不动。
  * 极点真正移动来自【闭合腔的多次往返反馈】（回声串几何级数），即上式；不是单次叠加。
  * rho（腔的净往返振幅保留）是 OPEN 量：核 |r|=1 已知，但“单独外垒”的反射率不能直接用
    v18 的 |R_GR|^2=.531（那是外垒+吸收视界的【净】反射，含视界吸收通道，不是两侧真空的
    无耗散互易势垒）。严格 rho 需 v19 做【外垒双侧出射散射 IVP】。故本脚本给 rho 扫描，
    rho=.73 仅作“若与 v18 净反射同量级”的量级插图，非定量。
"""
import numpy as np

# ---------- 权威几何 / QNM（几何单位 G=c=M=1）----------
DT = 13.9389            # 核->外垒往返龟坐标 2L（v18 严格，质量无关）
L = DT/2
w_r0, w_i0 = 0.3736716844, 0.0889623157
tau_d0 = 1.0/w_i0       # GR 主环 e-fold = 11.241 M

print("="*78)
print("MainAgent v19 pole-feedback analytic skeleton (Δt=2L=%.4f M, GR w0=%.6f-%.6fi)"%(DT,w_r0,w_i0))
print("GR e-fold tau_d0=%.3f M ;  Δt/tau_d0=%.3f"%(tau_d0, DT/tau_d0))
print("="*78)

def poles(rho, phi):
    """腔反馈极点族：返回 (阻尼|w_i|, 选最接近 GR 主频的梳齿 w_r_app, 相邻梳齿间隔)。"""
    wi = -np.log(rho)/DT
    spacing = 2*np.pi/DT
    # w_r,n=(2πn-phi)/Δt，取最接近 w_r0 的整数 n
    n_star = int(round((w_r0*DT + phi)/(2*np.pi)))
    wr = (2*np.pi*n_star - phi)/DT
    return wi, wr, spacing, n_star

print("\n[A] 极点条件  g e^{i w Δt}=1 ：|w_i|=-lnρ/Δt ,  w_r,n=(2πn-arg g)/Δt")
print("-"*78)
print("%6s %10s %10s %10s %10s %10s %12s"%("rho","|w_i|app","tau_app(M)","tau/tau0","w_r_app","δw_r/w_r0","finesse"))
for rho in [0.30,0.50,0.685,0.729,0.80,0.90,0.95]:
    wi, wr, sp, n = poles(rho, 0.0)
    tau = 1.0/wi
    print("%6.3f %10.4f %10.2f %10.2f %10.4f %+10.1f%% %12.1f"%(
        rho, wi, tau, tau/tau_d0, wr, 100*(wr-w_r0)/w_r0,
        np.pi*np.sqrt(rho)/(1-rho)))

print("\n[B] 梳齿间隔 2π/Δt = %.4f M^-1 （与主频 %.4f 同量级 => 腔反馈显著重排频谱，"%(2*np.pi/DT,w_r0)+
      "\n    不是小扰动；与‘回波埋入主环、非干净晚期峰’一致）")

print("\n[C] 相位 arg g 扫描（rho=.729 量级插图；phi=核反射相位+外垒反射相位，Neumann 核=0/π）")
print("    显式：rho=.729 仅当外垒反射与 v18 净反射同量级才成立，精确 rho OPEN（双侧出射 IVP）")
print("-"*78)
rho=0.729
for phi_deg in [0,45,90,135,180,225,270,315]:
    phi=np.radians(phi_deg)
    wi,wr,sp,n=poles(rho,phi)
    print("  arg g=%3d° : |w_i|app=%.4f (tau=%.1fM, %.2f× GR)  w_r_app=%.4f  δw_r/w0=%+.1f%%"%(
        phi_deg, wi, 1/wi, (1/wi)/tau_d0, wr, 100*(wr-w_r0)/w_r0))

print("\n[D] 无限时长 单 QNM + 单延迟同指数副本 => 仅留数改变（极点不动）验证")
wc=complex(w_r0,-w_i0)
for eps in [0.0,0.3,0.729,1.0]:
    C=1+eps*np.exp(1j*0)*np.exp(1j*wc*DT)   # z(t)=e^{i w0 t}(1+eps e^{i w0 Δt})
    print("  eps=%.3f : 合成因子 C=%.4f%+.4fi（与 t 无关的复常数 => 仍为单一指数 w0，无 δw）"%(
        eps,C.real,C.imag))
print("  => 单次叠加不改极点；δw/δ阻尼 只来自 [A] 的闭合多次往返反馈。")

print("\n[E] 自洽：rho=.729 -> finesse=%.1f（低 finesse，腔模可分辨但不尖锐），"%(np.pi*np.sqrt(rho)/(1-rho))+
      "与 v15 真实 TUFT 无高 Q 壁腔窄谱一致；v15 玩具高窄峰要求 rho≈1。")

print("\n[F] 模型适用边界（自我限定，防把极限公式当全区间）")
print("  [A] 的 g e^{iwΔt}=1 是【强反射/离散回声可分辨】的纯腔梳齿极限。")
print("  rho->0 时 |w_i|=-ln rho/Δt 发散 —— 这是极限失效信号，不是预言：")
print("  rho=0（核完全不反射＝视界）必须平滑回到 GR w0=.3737-.08896i，纯腔公式给不出。")
print("  -> 真实 TUFT：核 Neumann 全反射 |r_core|=1，但主频 .374 处外垒不是高反射镜")
print("     （v15 无高 Q 腔；v18 一次往返后主环振幅 e^{-w_i0 Δt}=e^-1.24=%.3f），"%(np.exp(-w_i0*DT))+
      "系统处在【中间耦合区】，非封闭腔也非视界，必须时域数值，不能用单一解析公式。")

print("\n[G] 弱反馈端锚（rho=0 必须回 GR 的另一端）")
print("  最小内插（一阶能量份额模型，非严格极点方程）：w_i_app ≈ w_i0 (1-R_E)，R_E∈[0,1]")
print("  R_E=0(核=视界)->w_i0=%.5f (tau=%.2fM, GR) ; R_E=1(全挡回)->0(无阻尼,封闭)"%(w_i0,tau_d0))
for RE in [0.0,0.25,0.5,0.75,1.0]:
    wia=w_i0*(1-RE)
    tau=np.inf if wia==0 else 1/wia
    ts="inf" if wia==0 else "%.1f"%tau
    print("    R_E=%.2f : |w_i|app=%.5f  tau=%sM (%.2f×GR)  一阶 δw_r≈0（回注先改留数）"%(
        RE,wia,ts,(tau/tau_d0) if wia>0 else np.inf))
print("  弱反馈端频率一阶不动（与[D]一致：反馈回注首阶只改复留数，δw_r 为二阶/相位效应）。")

print("\n[H] 统一极点方程（连接 GR w0 与封闭梳齿；需一个数值输入，留 v19 时域）")
print("  格林函数 G(w) ∝ 1/[D0(w) - a e^{i w Δt}]，D0(w0)=0 为 GR QNM 分母。")
print("  极点：D0(w)=a e^{i w Δt}；在 w0 邻域 δw=[a/D0'(w0)] e^{i w0 Δt} e^{i δw Δt}。")
print("  a=0(无反馈) -> δw=0 严格回 GR w0；|a|增大 -> 向 [A] 梳齿过渡。")
print("  D0'(w0)（GR 极点留数斜率）不能纯解析定，由 v19 时域模板注入/双侧出射 IVP 自然产出。")
print("  => v19 正确顺序：① 外垒【双侧出射】散射 IVP 定 r_b(w)（区别 v18 含视界的净 R）；")
print("     ② 得 g(w)=r_core r_b(w)（含相位）；③ 时域注入 l=m=2 QNM 初值直接读中间区 δw/δ阻尼；")
print("     ④ PSD matched-filter SNR 最后做，且绝对 SNR 依赖注入 ε(OPEN)，不依赖能否下载真实 PSD。")

print("\n[四态分级]")
print(" 严格(解析)：极点条件 g e^{iwΔt}=1 及 |w_i|、梳齿公式；[D] 单副本仅改留数；[F] 极限边界。")
print(" 条件定理：给定 rho,phi 下的强反馈腔模；给定 R_E 下的弱反馈一阶阻尼内插。")
print(" 框架(未数值)：统一方程 D0(w)=a e^{iwΔt}，D0'(w0) 待 v19。")
print(" OPEN：rho/R_E（外垒双侧出射反射率）；外垒相位 arg r_b(w)（单点 arg 可取，群延迟不可）；")
print("       g(w) 色散、even 通道、中间耦合区 δw 数值、注入 ε、PSD 下绝对 SNR。")
print(" 量级插图(非定量)：rho=.729 借 v18 净反射 .531，含视界吸收通道，不可直接等同无耗散外垒。")
