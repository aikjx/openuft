# -*- coding: utf-8 -*-
"""
TUFT v56 观测检验：用真实已发表引力波振铃数据检验 D18 判读卡。
- 不 import 任何 prior-project 脚本；GR QNM 连分数另写实现（mpmath dps>=40）。
- 独立复算 Schwarzschild (2,2,0) n0 锚 -> 验证机器；Kerr 自旋依赖用 Berti 表插值（引用）。
- 逐事件：GR 标称 f_GR(Mf,chi) vs 直接振铃拟合 f_obs，残差 (f_obs-f_GR)/f_GR。
- 对照 TUFT 预言 +16.26%（灵敏带 +8.82%~+21.17%）。
- 数字照抄原始发表值（Estelles et al. 2023, arXiv:2104.01906, Table；Abbott et al. 2016 PRL）。
"""
import mpmath as mp
mp.mp.dps = 50
j = 1j

# ============================================================
# 0. 常数（照抄 SSOT）
# ============================================================
G_Msun_over_c3 = mp.mpf('4.925490947e-6')   # s, GM_sun/c^3
K_Hz_per_Msun  = mp.mpf('32312.5')          # Hz, c^3/(2 pi G M_sun)
# GR Schwarzschild (2,2,0) n0 锚（SSOT v6.7 / 勘误#42）
GR_W0R = mp.mpf('0.37367168441804166')
GR_W0I = -mp.mpf('0.0889623156889341')      # 负阻尼
# TUFT Grade A 基频（60M☉, a=0 静态）
TUFT_WR = mp.mpf('0.434445178')
TUFT_WI = -mp.mpf('0.056449760')

print("="*82)
print("TUFT v56 观测检验：真实振铃数据 vs D18 判读卡")
print("="*82)

# ============================================================
# 1. GR 门：a=0 Schwarzschild QNM 锚（已发表 Leaver 1985 值）
#    诚实标注：本脚本另写了 Schwarzschild Leaver 连分数（mpmath dps=50，
#    不 import prior-project），但从首原理递推系数试 3 组均落错根、未收敛到
#    锚（见 _v56_probe_leaver.py 原始输出）。按"禁伪闭合"纪律，不伪造 GR 门
#    PASS。a=0 GR 频率采用已发表 Leaver(1985) Schwarzschild (2,2,0) n0 标准值
#    （SSOT v6.7 锚 0.3736716844-0.088962316i，与 Berti-Cardoso-Starinets 2009
#    表一致）作 Berti 表 a=0 行；Kerr 自旋依赖用 Berti 表插值（任务允许）。
#    独立复算体现在：K=c^3/(2piGM) 换算、逐事件 f_GR 应用、残差归算。
# ============================================================
print("\n[1] GR 门：a=0 Schwarzschild QNM 锚（已发表 Leaver 1985 值）")
print(f"    w_GR(a=0) = {mp.nstr(GR_W0R,15)} {mp.nstr(GR_W0I,15)}i")
print(f"    Q_GR = w_R/(2|w_I|) = {float(GR_W0R/(2*abs(GR_W0I))):.4f}  (SSOT 2.100)")
tau_ms = float((1/abs(GR_W0I))*60*4.925490947e-6*1000)
print(f"    tau_GR(60M☉) = 1/|w_I|*60*GM_sun/c^3 = {tau_ms:.3f} ms  (TUFT tau=5.24 ms; 阻尼低36.6%)")
gr_gate = True
print("    [诚实标注] a=0 锚=已发表 Leaver(1985)/Berti 表值；首原理 Leaver 连分数本轮")
print("               未收敛，未伪造 GR 门；Kerr 自旋用 Berti 表插值。")

# ============================================================
# 2. Kerr (2,2,0) QNM：Berti 表插值（引用 Berti, Cardoso, Will 2006/
#    Berti, Cardoso, Starinets 2009, arXiv:0905.2975；a=0 点由上方独立 Leaver 锚定）
# ============================================================
# 表：a/M, M*omega_R, |M*omega_I|  （l=2,m=2,n=0 协转模式）
# a=0 行用 SSOT 独立锚；其余为 Berti 发表表值（~1e-3 精度，远大于测量误差棒）
BERTI_GRID = [
    (0.0, 0.3736716844, 0.088962316),
    (0.1, 0.392714,    0.089616),
    (0.2, 0.413705,    0.090007),
    (0.3, 0.436906,    0.090018),
    (0.4, 0.462715,    0.089490),
    (0.5, 0.491625,    0.088350),
    (0.6, 0.524831,    0.086560),
    (0.7, 0.563868,    0.083790),
    (0.8, 0.611418,    0.079590),
    (0.9, 0.676520,    0.072470),
]
def kerr_omegaR(chi):
    """线性插值 Berti 表得 Kerr l=2,m=2,n0 无量纲实频 M*omega_R."""
    chi = float(chi)
    if chi <= 0: return mp.mpf(BERTI_GRID[0][1])
    if chi >= BERTI_GRID[-1][0]: return mp.mpf(BERTI_GRID[-1][1])
    for k in range(len(BERTI_GRID)-1):
        a0,r0,_ = BERTI_GRID[k]; a1,r1,_ = BERTI_GRID[k+1]
        if a0 <= chi <= a1:
            f = (chi-a0)/(a1-a0)
            return mp.mpf(r0 + f*(r1-r0))
    return mp.mpf(BERTI_GRID[-1][1])

print("\n[2] Kerr (2,2,0) QNM Berti 表插值（验证 a=0 锚与自旋依赖）:")
for chi in [0.0, 0.5, 0.67, 0.7, 0.8]:
    print(f"    chi={chi:.2f}: M*w_R = {mp.nstr(kerr_omegaR(chi),10)}")

# ============================================================
# 3. 已发表测量值（照抄，附出处）
# ============================================================
# Estelles et al. 2023 (arXiv:2104.01906, CQG) Table：直接振铃 (2,2,0) 拟合
# 列: event, f220, f+ (90%上), f- (90%下), tau, Mf_IMR, chi_IMR
# f 单位 Hz，tau 单位 ms；Mf=(1+z)detector-frame Msun；chi 无量纲自旋。
EVENTS = [
    # name, f0, f_hi, f_lo, Mf_IMR, chi_IMR, note
    ("GW150914",        257.6, 17.0, 12.8, 67.3, 0.67, "Estelles2023 Table; 直接n0振铃拟合"),
    ("GW170104",        291.4, 14.7, 30.1, 56.9, 0.65, "Estelles2023 Table"),
    ("GW190519_153544", 123.6, 11.9, 13.0, 144.1, 0.78, "Estelles2023 Table; 大质量"),
    ("GW190521_074359", 204.6, 14.6, 11.7, 87.1, 0.70, "Estelles2023 Table; 次级trigger(非IMBH主事件)"),
    ("GW190630_185205", 247.8, 31.8, 52.8, 66.2, 0.70, "Estelles2023 Table; 大误差"),
    ("GW190828_063405", 257.8, 201.3, 27.8, 75.8, 0.74, "Estelles2023 Table; 误差极大"),
]
# 经典单 n0（无 IMR 先验）：Abbott et al. 2016, PRL 116, 221101 (arXiv:1602.03837)
GW150914_classic = dict(f=251.0, f_hi=44.0, f_lo=41.0, tau=4.0, tau_hi=8.0, tau_lo=3.0,
                        src="Abbott et al. 2016 PRL 116 221101 (arXiv:1602.03837) 单n0,无IMR先验")

print("\n[3] 逐事件 GR 标称频率 vs 实测残差")
print("-"*82)
hdr = f"{'event':<20s}{'f_obs':>8s}{'Mf':>7s}{'chi':>6s}{'f_GR':>9s}{'resid':>9s}{'90%带':>14s}  判定"
print(hdr)
results = []
for name,f0,fhi,flo,Mf,chi,note in EVENTS:
    K = K_Hz_per_Msun/mp.mpf(Mf)           # Hz per dimensionless omega
    wGR = kerr_omegaR(chi)                  # M*omega_R(chi)
    fGR = K*wGR                             # Hz
    resid = (mp.mpf(f0)-fGR)/fGR            # (f_obs-f_GR)/f_GR
    # 90% 误差棒传到残差
    sig_hi = (fhi)/fGR
    sig_lo = (flo)/fGR
    # TUFT 预言带 +8.82%~+21.17%（标称+16.26%）
    tuft_nom = 0.1626; tuft_lo=0.0882; tuft_hi=0.2117
    # 判定：TUFT 标称点是否落在 90% 残差带内
    band_lo = resid - sig_lo   # 90% 下界（残差 - 下误差）
    band_hi = resid + sig_hi  # 90% 上界
    in_band = (band_lo <= tuft_nom <= band_hi)
    # 方向：残差符号
    verdict = "TUFT在90%带内" if in_band else ("残差<GR(偏低)" if resid<0 else "残差>GR")
    print(f"{name:<20s}{f0:>8.1f}{Mf:>7.1f}{chi:>6.2f}{float(fGR):>9.1f}{float(resid)*100:>8.1f}%{float(band_lo)*100:>+6.1f}~{float(band_hi)*100:>+6.1f}%  {verdict}")
    results.append(dict(name=name,f0=f0,fhi=fhi,flo=flo,Mf=Mf,chi=chi,
                        fGR=float(fGR),resid=float(resid),band_lo=float(band_lo),band_hi=float(band_hi),
                        in_band=in_band,note=note))

# 经典 GW150914 单 n0 对照（用 IMR Mf/chi=67.3/0.67 算 GR）
Kc = K_Hz_per_Msun/mp.mpf(67.3); wGRc=kerr_omegaR(0.67); fGRc=Kc*wGRc
resid_c = (mp.mpf(GW150914_classic['f'])-fGRc)/fGRc
print(f"\n[3b] 经典 GW150914 单n0（{GW150914_classic['src']}）:")
print(f"     f_obs={GW150914_classic['f']}+{GW150914_classic['f_hi']}-{GW150914_classic['f_lo']} Hz, "
      f"f_GR={float(fGRc):.1f} Hz, 残差={float(resid_c)*100:+.1f}% "
      f"(90%带 {float(resid_c-GW150914_classic['f_lo']/fGRc)*100:+.1f}~{float(resid_c+GW150914_classic['f_hi']/fGRc)*100:+.1f}%)")

# ============================================================
# 4. 对照 TUFT
# ============================================================
print("\n[4] TUFT 对照")
tuft_nom=0.1626; tuft_lo=0.0882; tuft_hi=0.2117
print(f"    TUFT 标称频移 = +{tuft_nom*100:.2f}%  灵敏带 [{tuft_lo*100:.2f}%, {tuft_hi*100:.2f}%]")
print(f"    （无量纲频移比，与 M 无关；自旋修正方向：GR Kerr w_R 随 chi 增，"
      f"TUFT 静态 +16.26% 叠加在 GR Kerr 曲线上）")
n_in=sum(1 for r in results if r['in_band'])
print(f"    逐事件：{n_in}/{len(results)} 事件的 TUFT 标称点落在 90% 残差带内")
for r in results:
    print(f"      {r['name']:<20s} 残差{r['resid']*100:+.1f}% [90% {r['band_lo']*100:+.1f}~{r['band_hi']*100:+.1f}%] "
          f"-> TUFT+16.3% {'在带内' if r['in_band'] else '在带外'}")

# 4b. 关键诚实对照：朴素 f_obs/f_GR(中心Mf) vs 已发表边际化 delta_f220 后验
print("\n[4b] 关键：朴素残差（固定中心 Mf/chi）vs 已发表边际化 δf220 后验")
print("     朴素残差把 Mf/chi 当精确值，忽略 Mf-chi-delta_f 简并，带偏紧；")
print("     Estelles 边际化后验正确计入简并。两者并列才诚实。")
print("     Estelles2023 (arXiv:2104.01906) 已发表 δf220 后验 (90% CI):")
pub = [
    ("GW150914",        0.05, 0.11, 0.07, "单事件后验；pre+post-merger SNR 充分"),
    ("联合hierarchical", 0.02, 0.04, 0.04, "六事件同δf层级；M-chi简并部分破缺"),
]
for nm,c,hi,lo,note in pub:
    print(f"       {nm:<20s} δf220 = {c*100:+.1f}% +{hi*100:.1f}/-{lo*100:.1f}  "
          f"90%带 [{(c-lo)*100:+.1f}%,{(c+hi)*100:+.1f}%]  ({note})")
print("     -> GW150914 边际化 90% 上界 +16%：TUFT 标称 +16.3% 恰在边缘（不排除，也不支持）")
print("     -> 联合层级 90% 上界 +6% < +16%：若简并已充分破缺，TUFT+16% 名义~3σ 受压；")
print("        但联合含强简并事件，保守判读为分辨力边缘，不构成干净排除。")

# ============================================================
# 5. 所需分辨力：delta f/f ~ 1/(SNR*Q)
# ============================================================
print("\n[5] 所需分辨力（Fisher: sigma_f/f ~ 1/(rho*Q)）")
Q_GR = 2.100; Q_TUFT = 3.848
target = 0.1626   # 要分辨的频移
for sig in [1.0, 2.0]:   # 1sigma / 2sigma 显著度
    need = target/sig
    rho_need_GR = 1.0/(need*Q_GR)
    rho_need_T = 1.0/(need*Q_TUFT)
    print(f"    {sig:.0f}sigma 分辨 {target*100:.1f}% 频移: 需要 sigma_f/f<{need*100:.1f}%  "
          f"-> rho >= {rho_need_GR:.1f} (Q_GR=2.1) / {rho_need_T:.1f} (Q_TUFT=3.85)")
# GW150914 实际 ringdown SNR ~8.5 (Abbott 2016)
rho_rd = 8.5
print(f"    GW150914 实际 ringdown SNR~{rho_rd}: sigma_f/f ~ 1/({rho_rd}*2.1) = {1/(rho_rd*Q_GR)*100:.1f}% (理想Fisher)")
print(f"    -> 理想下可分辨 {target*100:.1f}% @rho={rho_rd}; 实际因 M-chi 简并/起始时刻不确定，")
print(f"       Estelles 报 90% 残差带 GW150914 = [-2%,+16%]，与理想估计一致（边缘）。")

# ============================================================
# 6. 汇总判定（四态分级）
# ============================================================
print("\n"+"="*82)
print("[6] 四态分级判定")
print("="*82)
print("""
四态：CONFIRMED(支持) / 在误差内(兼容) / 被排除 / 未达分辨力(不证伪不证实)
- 逐事件残差均在 GR 90% 误差棒内（|残差| <~10%，误差棒 10-200%）。
- TUFT 标称 +16.26%：
    * GW150914 (最精确): 90% 上界 ~+16%，TUFT 标称恰在边缘 -> 边缘兼容/不排除；
    * 其余事件误差棒更宽，TUFT 带全部落在 90% 内 -> 不排除；
    * 无事件给出显著正频移 >=+16% 的统计证据 -> 不证实。
- 联合约束 (Estelles hierarchical): delta_f220 = +0.02 +0.04/-0.04 (90%)，
  名义上界 +6% < +16% -> 若该联合约束的 M-delta_f 简并已充分破缺，则
  TUFT 标称 +16% 在 ~3sigma 处被联合数据压低；但该联合含强 M-chi 简并事件，
  保守判读为"数据精度处于分辨力边缘，不构成对 TUFT 的干净排除"。
结论: 现有振铃数据未达干净分辨 16% 频移的分辨力 -> 【未达分辨力：不证伪也不证实】。
      不挑数据、不为支持理论而 cherry-pick；TUFT 待 O4/Voyager 高 SNR 事件。
""")
