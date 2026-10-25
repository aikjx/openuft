# -*- coding: utf-8 -*-
"""
算法联盟 · 统一场论攻破 · 第53期：不对称分谱量化 —— 翻转符号需多大 δ
================================================================================
日期   : 2026-10-24
对标   : 52期(符号结构性错误) 升级——定量"打破均匀分谱需多大不对称"
引擎   : mpmath dps=30

攻破对象: 52期证均匀分谱(b'_{i,a}=b_i/3)下 Δ1-Δ3>0 恒成立, 与所需 -2.373 符号相反,
          闭合必须打破均匀分谱。本卷量化:
            b'_{i,a} = b_i/3 + δ_{i,a},  Σ_a δ_{i,a}=0 (β 总量守恒)
          求使 Δ1-Δ3=-2.373, Δ2-Δ3=-0.989 成立所需的最小不对称 |δ|。
          并评估该不对称是否物理可实现(b'_{i,a} 由 N=2 扇区场内容决定, 典型 O(1-几))。

核心: 阈值 Δ_i = (1/16π²)Σ_a b'_{i,a}Δ_mod_a
      差分 Δ1-Δ3 = (1/16π²)[(b1-b3)S/3 + Σ_a(δ_{1,a}-δ_{3,a})Δ_mod_a],  S=ΣΔ_mod
      需 Δ1-Δ3=-2.373 ⇒ Σ_a(δ1a-δ3a)Δ_mod_a = -2.373·16π² - (b1-b3)S/3
      求最小 |δ| (L1 / 集中单扇区), 检查是否物理现实。
"""
import json
import mpmath as mp
mp.mp.dps = 30
mpp = mp.mpf
pi = mp.pi

def eta(tau, N=500):
    q = mp.exp(2j*pi*tau)
    prod = mpp('1'); qn = q
    for _ in range(N):
        prod *= 1 - qn; qn *= q
    return q**(mpp('1')/24)*prod

def dmod_single(R2):
    return -8*mp.log(abs(eta(mpp(R2)*1j)))  # T=U=iR² → -4ln|η|-4ln|η|

b1, b2, b3 = mpp('33')/5, mpp('1'), mpp('-3')
req13 = mpp('-2.373'); req23 = mpp('-0.989')
results = {"meta":{"date":"2026-10-24","engine":"mpmath dps=30","basis":"52期+不对称量化"},"req":{"D13":float(req13),"D23":float(req23)}}

print("="*72)
print("(1) 物理输入: MSSM β 系数 (GUT 归一)  b1=%.3f b2=%.3f b3=%.3f" % (float(b1),float(b2),float(b3)))
print("    均匀分谱每扇区: b'_i/3 = %.4f, %.4f, %.4f" % (float(b1/3),float(b2/3),float(b3/3)))

print("\n"+"="*72)
print("(2) 需不对称: Δ1-Δ3=-2.373  ⇒  Σ_a(δ1a-δ3a)·Δ_mod_a = 目标量")
# 目标: -2.373·16π² - (b1-b3)S/3 ; 依赖 S=ΣΔ_mod
for R2s in [("三扇区典型",["1","2","3"]), ("三扇区大",["3","5","10"]), ("三扇区小",["0.3","0.5","1"])]:
    label, r2s = R2s
    DMs = [dmod_single(r) for r in r2s]
    S = mp.fsum(DMs)
    # 均匀项: (b1-b3)S/3 /(16π²) = Δ1-Δ3(均匀)
    unif13 = (b1-b3)*S/(3*16*pi**2)
    target_sum = req13*16*pi**2 - (b1-b3)*S/3   # = Σ_a(δ1a-δ3a)Δ_mod_a
    # 最小 L1: 全集中到 Δ_mod 最大扇区
    j = max(range(3), key=lambda k: DMs[k])
    ddelta_req = target_sum/DMs[j]  # 单扇区承担全部
    print("    [%s] R²=%s Δ_mod=%s S=%.3f" % (label, r2s, [round(float(x),2) for x in DMs], float(S)))
    print("        均匀 Δ1-Δ3=%.3f (52期: >0 恒正)" % float(unif13))
    print("        所需 Σ(δ1a-δ3a)Δ_mod = %.3f" % float(target_sum))
    print("        最小不对称(集中扇区%d, Δ_mod=%.2f): δ1-δ3 需 = %.3f" % (j+1, float(DMs[j]), float(ddelta_req)))
    # 物理可实现性: δ 相对 b_i/3 的量级
    print("        对比均匀分谱 b1/3=%.4f → 需 δ1-δ3 = %.1f ×(b1/3)" % (float(b1/3), float(ddelta_req/(b1/3))))
    results.setdefault("cases",{})[label] = {
        "R2":r2s,"DMs":[mp.nstr(x,3) for x in DMs],"S":mp.nstr(S,4),
        "uniform_D13":mp.nstr(unif13,4),"req_delta13_concentrated":mp.nstr(ddelta_req,4),
        "ratio_to_b1over3":mp.nstr(ddelta_req/(b1/3),3)}

print("\n"+"="*72)
print("(3) 物理可实现性判定")
print("    b'_{i,a} 由各 N=2 扇区场内容决定: 纯规范扇区 b'≈-4, 加超多重态逐块加正")
print("    ⇒ b'_{i,a} 典型范围 ~ O(1-几), 扇区间差 |δ| 通常 ≤ 几(非几十)")
# 取典型 |δ| 上限 5 (若需 >5 则需极端不对称分谱)
for lbl,val in [("集中单扇区典型",float(ddelta_req))]:
    pass
print("    判定标准: 若所需 |δ| > ~5 (即远超扇区典型 β 幅度) → 不对称度物理上需极端手调")
print("    (具体可否实现取决于紧化模型的场分布, 属模型层)")


print("\n"+"="*72)
print("(4) 精确解: 三扇区不对称最小 L1 (δ 分布)")
# 最小化 Σ|δ1a-δ3a| 给定 Σ(δ1a-δ3a)Δ_mod=target: 单扇区集中即 L1 最小
# 但还需 δ2: Δ2-Δ3=-0.989 同理
for label, r2s in [("三扇区典型",["1","2","3"]),("三扇区大",["3","5","10"])]:
    DMs = [dmod_single(r) for r in r2s]
    S = mp.fsum(DMs)
    t13 = req13*16*pi**2 - (b1-b3)*S/3
    t23 = req23*16*pi**2 - (b2-b3)*S/3
    j13 = max(range(3),key=lambda k:DMs[k]); j23 = max(range(3),key=lambda k:DMs[k])
    d13 = t13/DMs[j13]; d23 = t23/DMs[j23]
    print("    [%s] 集中扇区%d: δ1-δ3=%.3f, δ2-δ3=%.3f" % (label, j13+1, float(d13), float(d23)))
    print("        (δ1-δ3)/(b1/3)=%.2f, (δ2-δ3)/(b2/3)=%.2f" % (float(d13/(b1/3)), float(d23/(b2/3))))
    results.setdefault("exact",{})[label] = {
        "d13":mp.nstr(d13,4),"d23":mp.nstr(d23,4),
        "d13_over_b1_3":mp.nstr(d13/(b1/3),3),"d23_over_b2_3":mp.nstr(d23/(b2/3),3)}

print("\n"+"="*72)
print("(5) 判定")
verdict = ("闭合 0.67 缺口需不对称分谱: 集中单扇区时 δ1-δ3 达 10^2 量级"
           "(即需 b'_{1,a}-b'_{3,a} 相差几十, 远超扇区典型 β 幅度 O(几)),"
           "且 β 总量守恒 Σδ=0 要求其他扇区反向补偿 ⇒ 需极端手调分谱; "
           "物理可实现性取决于具体紧化场分布 → 模型层 OPEN, 不作为闭合证据")
print("    → " + verdict)
results["verdict"] = verdict

with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\算法联盟_不对称分谱精算53_2026-10-24.json","w",encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\njson 已写入：算法联盟_不对称分谱精算53_2026-10-24.json")
