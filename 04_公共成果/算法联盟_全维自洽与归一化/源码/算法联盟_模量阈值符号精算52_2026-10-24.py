# -*- coding: utf-8 -*-
"""
算法联盟 · 统一场论攻破 · 第52期：模量阈值符号方向 —— 0.67 缺口纯模量阈值能否闭合
================================================================================
日期   : 2026-10-24
对标   : 50期(量级判定 O(1-2)) 关键盲区——只查量级未查符号
引擎   : mpmath dps=30

攻破对象: 50期判"缺口0.67量级可被模量阈值覆盖(三扇区累计~1.99 O(1-2))"。
本卷检验 50期未检查的 符号方向:
  闭合缺口需要 Δ1-Δ3 = -2.373 <0 (50期阶段A), Δ2-Δ3 = -0.989 <0
  即 α_3 阈值最正、α_1 最负。
  问: Z2xZ2 模量相关阈值 Δ_mod = -4ln|η(T)|-4ln|η(U)| 在均匀分谱(b'_{i,a}∝b_i)
      下能否给出负的 Δ_i 差分? 若 Δ_mod 恒正且 b_i 排序固定, 则符号固定 → 50期量级
      可覆盖但符号错误 → 纯模量阈值不能闭合缺口。

核心: (1) 数值检验 Δ_mod(T,U) 正定性 (2) 均匀分谱下 Δ_i-Δ_j 符号
      (3) 判定缺口闭合所需符号方向是否可达。
"""
import json
import mpmath as mp
mp.mp.dps = 30
mpp = mp.mpf
pi = mp.pi

def eta(tau, N=600):
    q = mp.exp(2j*pi*tau)
    prod = mpp('1'); qn = q
    for _ in range(N):
        prod *= 1 - qn; qn *= q
    return q**(mpp('1')/24)*prod

def dmod(T, U):
    """模量相关阈值 Δ_mod = -4ln|η(T)| -4ln|η(U)|"""
    return -4*mp.log(abs(eta(T))) - 4*mp.log(abs(eta(U)))

results = {"meta":{"date":"2026-10-24","engine":"mpmath dps=30","basis":"50期(量级)+符号检验"},"req":{"D13":-2.373,"D23":-0.989}}

print("="*72)
print("(1) Δ_mod(T,U) 正定性扫描 (T=U=iR², R² 大范围)")
R2s = ["0.05","0.1","0.3","0.5","1","2","3","5","10","20","50"]
signed = []
for R2 in R2s:
    d = dmod(mpp(R2)*1j, mpp(R2)*1j)
    signed.append((R2, float(d)))
    print("    R²=%-5s  Δ_mod=%.4f  %s" % (R2, float(d), "正" if d>0 else "负/零"))
pos = all(v>0 for _,v in signed)
print("    全部正: %s  (|η|<1 恒真 → -ln|η|>0 → Δ_mod>0 恒成立)" % pos)
results["pos_definite"] = {"all_positive":pos,"scan":{k:mp.nstr(v,4) for k,v in signed}}

print("\n"+"="*72)
print("(2) 正定性的结构原因: |η(τ)|<1 对 Im τ>0")
print("    η=q^{1/24}Π(1-q^n), |q|=e^{-2πImτ}<1 → |η|<1 → -ln|η|>0")
print("    ⇒ Δ_mod(T,U) = -4ln|η(T)|-4ln|η(U)| > 0 对任意物理模量恒成立")
print("    ⇒ 模量相关阈值对三个规范方向都是正的(各扇区 Δ_mod>0)")

print("\n"+"="*72)
print("(3) 均匀分谱下 Δ_i 差分符号")
# 均匀分谱: b'_{i,a} = b_i/3 (三扇区平分 MSSM β), 阈值 Δ_i = Σ_a (b_i/3)/(16π²)·Δ_mod_a
b = {"b1":mpp('33')/5, "b2":mpp('1'), "b3":mpp('-3')}
# 三扇区取不同模量 → Δ_mod_a>0
# Δ_i = (b_i/3)/(16π²)·Σ_a Δ_mod_a = b_i/(48π²)·S,  S=Σ_a Δ_mod_a > 0
# ⇒ Δ_i ∝ b_i: Δ1-Δ3 = (b1-b3)/(48π²)·S > 0 (因 b1>b3)
# 但闭合需 Δ1-Δ3 = -2.373 < 0 → 符号相反!
for S_label,S in [("S=30(三扇区典型)",mpp('30')),("S=60(大模量)",mpp('60')),("S=6(小模量)",mpp('6'))]:
    d13 = (b["b1"]-b["b3"])*S/(48*pi**2)
    d23 = (b["b2"]-b["b3"])*S/(48*pi**2)
    print("    %s: Δ1-Δ3=%.3f, Δ2-Δ3=%.3f" % (S_label, float(d13), float(d23)))
    results.setdefault("even_split",{})[S_label] = {"D13":mp.nstr(d13,3),"D23":mp.nstr(d23,3)}
print("    均匀分谱 Δ1-Δ3>0 恒成立 (b1>b3), 但闭合需 <0 → 符号相反")

print("\n"+"="*72)
print("(4) 结论: 50期'量级可覆盖'的符号缺口")
need13 = mpp('-2.373'); need23 = mpp('-0.989')
# 均匀分谱最大可得 |Δ1-Δ3| 随 S 增长, 但方向错误
print("    闭合所需: Δ1-Δ3=%.3f (<0), Δ2-Δ3=%.3f (<0)" % (float(need13), float(need23)))
print("    均匀分谱给出: Δ1-Δ3>0, Δ2-Δ3>0 (恒正, 与需求相反)")
print("    ⇒ 纯模量相关阈值(均匀分谱) 符号错误, 不能闭合 0.67 缺口")
print("    ⇒ 若要有 Δ1-Δ3<0, 必须打破均匀分谱: 各扇区 b'_{i,a} 依赖 i 且差异大,")
print("      或引入负的常数/格点项(51期: 模型依赖的 (2,2) 格点求和)")
verdict = ("50期量级可覆盖成立, 但符号方向错误: 均匀分谱下模量相关阈值 Δ_mod>0 恒正, "
           "Δ1-Δ3=(b1-b3)S/48π²>0 与所需 -2.373 相反 → 纯模量阈值不能闭合缺口; "
           "需打破均匀分谱或引入模型依赖负项 → 模型层 OPEN")
results["verdict"] = verdict
print("    → " + verdict)

# (5) 量化: 要闭合需多不对称
print("\n"+"="*72)
print("(5) 量化解: 打破均匀分谱需多少不对称")
# 设 Δ_i = (1/16π²)[Σ_a b'_{i,a}Δ_mod_a]. 需 Δ1-Δ3<0 且 Δ2-Δ3<0.
# 取三扇区 Δ_mod 分别为 x,y,z (>0), 每扇区 b'_{i,a} 三方向取 b_i/3 的扰动
# 简化: 若扇区1只贡献 α3 阈值(Δ_mod1 集中到 b'_{3,1}), 扇区2/3 集中到 α1/α2
# 则 Δ1-Δ3 = [b'_{1,2}Δ_mod2 - b'_{3,1}Δ_mod1]/(16π²)... 具体模型依赖
print("    均匀分谱 Δ1-Δ3 = (b1-b3)S/(48π²) ≈ %.3f·S/π²" % float((b["b1"]-b["b3"])/(48)))
print("    要翻转符号需 Δ_mod 在不同方向配不同 b' (模型依赖, 非几何普适)")
results["quant"] = {"uniform_slope_per_Spisq": mp.nstr((b["b1"]-b["b3"])/48,4),
                    "need_flip_model_dep": True}

with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\算法联盟_模量阈值符号精算52_2026-10-24.json","w",encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\njson 已写入：算法联盟_模量阈值符号精算52_2026-10-24.json")
