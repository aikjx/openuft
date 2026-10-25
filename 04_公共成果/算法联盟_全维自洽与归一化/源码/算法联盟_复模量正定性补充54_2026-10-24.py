# -*- coding: utf-8 -*-
"""
算法联盟 · 统一场论攻破 · 第54期补充：负区定位与物理可及性
================================================================================
日期   : 2026-10-24
目的   : 54期发现复模量存在 Δ_mod<0 区域。本补充定位负区在模空间的分布,
         判断其是否落在物理允许的基本域(T-duality fundamental domain)内,
         并评估其对 52/53期"均匀分谱不能闭合"结论的修正幅度。
引擎   : mpmath dps=30
"""
import json
import mpmath as mp
mp.mp.dps = 30
mpp = mp.mpf
pi = mp.pi
results = {"meta":{"date":"2026-10-24","engine":"mpmath dps=30","basis":"54期补充:负区定位"}}

def eta(tau, N=400):
    q = mp.exp(2j*pi*tau)
    prod = mpp('1'); qn = q
    for _ in range(N):
        prod *= 1 - qn; qn *= q
    return q**(mpp('1')/24)*prod

def dmod(T, U):
    return -4*mp.log(abs(eta(T))) - 4*mp.log(abs(eta(U)))

print("="*72)
print("(1) T-duality 基本域: |τ|≥1, |Re τ|≤1/2. 检验负区是否在基本域内")
# 负区样本: (-0.5,0.1), (-0.4,0.05) 等 → |τ|=sqrt(0.25+0.01)=0.5099 <1 ⇒ 在基本域外!
# 基本域要求 |T|≥1. 所以 T2=0.1, T1=-0.5 → |T|=0.51 <1 ⇒ 非基本域代表点
samples = [((-0.5,0.1),(-0.5,0.1)), ((-0.4,0.05),(-0.4,0.05)), ((-0.5,0.3),(-0.5,0.3)), ((-0.5,0.5),(-0.5,0.5))]
for (t1,t2),(u1,u2) in samples:
    Tmag = mp.sqrt(t1*t1+t2*t2); Umag = mp.sqrt(u1*u1+u2*u2)
    d = dmod(t1+1j*t2, u1+1j*u2)
    in_fund = Tmag>=1 and Umag>=1 and abs(t1)<=0.5 and abs(u1)<=0.5
    print("    T=(%s,%s)|T|=%.3f, U=(%s,%s)|U|=%.3f, Δ_mod=%.4f, 基本域内=%s"
          % (t1,t2,float(Tmag),u1,u2,float(Umag),float(d),in_fund))
    results.setdefault("neg_samples",[]).append({
        "T":(t1,t2),"U":(u1,u2),"|T|":mp.nstr(Tmag,3),"|U|":mp.nstr(Umag,3),
        "dmod":mp.nstr(d,4),"in_fundamental":in_fund})

print("\n"+"="*72)
print("(2) 扫描基本域内(|τ|≥1, |Reτ|≤1/2) 的复模量, 检验是否有负值")
neg_fund=0; tot_fund=0; min_fund=mpp('1e30'); minat_fund=None
T1s = [mpp('-0.5'),mpp('-0.3'),mpp('0'),mpp('0.3'),mpp('0.5')]
T2s = [mpp('0.9'),mpp('1'),mpp('1.2'),mpp('1.5'),mpp('2'),mpp('3'),mpp('5')]
for T1 in T1s:
    for U1 in T1s:
        for T2 in T2s:
            # 基本域: |T|=sqrt(T1²+T2²)≥1
            Tmag = mp.sqrt(T1*T1+T2*T2)
            if Tmag < 1: continue
            d = dmod(T1+1j*T2, U1+1j*T2)
            tot_fund+=1
            if d<min_fund: min_fund=d; minat_fund=(float(T1),float(T2),float(U1))
            if d<0: neg_fund+=1
print("    基本域内扫描: 总%d, 负%d, 最小%.4f @%s" % (tot_fund, neg_fund, float(min_fund), tuple(round(x,2) for x in minat_fund)))
results["fund_scan"] = {"total":tot_fund,"neg":neg_fund,"min":mp.nstr(min_fund,4),"min_at":list(minat_fund)}

print("\n"+"="*72)
print("(3) 关键判定: 负区是否物理可达?")
print("    54期找到的负区全部位于 |T|<1 (T2~0.1) → 在 T-duality 基本域外")
print("    基本域内(|T|≥1)扫描: 负%d/%d" % (neg_fund, tot_fund))
if neg_fund>0:
    verdict = ("基本域内也存在 Δ_mod<0 区域 → 52期'均匀分谱恒不能闭合'需修正为 "
               "'模量相关阈值可提供负差分, 均匀分谱在基本域内部分模量点可闭合'")
else:
    verdict = ("基本域内无负区: 54期发现的负区全在 |T|<1 (非物理基本域), "
               "52/53期结论对物理允许模量空间成立 → 均匀分谱不能闭合缺口仍结构性成立")
print("    → " + verdict)
results["verdict"] = verdict

with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\算法联盟_复模量正定性精算54_补充_2026-10-24.json","w",encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\njson 已写入：算法联盟_复模量正定性精算54_补充_2026-10-24.json")
