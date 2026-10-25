# -*- coding: utf-8 -*-
"""
算法联盟 · 统一场论攻破 · 第66期：主线A DEFN 层电弱参数"定义闭合"审计 + sin²θ_W 口径核验
================================================================================
日期   : 2026-10-25
对标   : 主线A §3.1 电弱参数(31号线)/本源矩阵 DEFN 行 vs PDG 2024 电弱参数
引擎   : mpmath dps=40
攻破点 : 主线A 将电弱参数(v,G_F,g,sin²θ_W)标为 DEFN"定义闭合"。
         ① 这些量数值全部来自实验测定(G_F 由 μ 衰变寿命、m_W 由对撞机)，
            非几何/公理首原，也非纯"定义闭合"——严格说它们是"定义式 + 实验输入";
         ② sin²θ_W(on-shell)=0.22320268 vs PDG on-shell s²_W=0.22339(10)，
            偏差 ~0.084%(≈1.9σ)——口径/数值需核验。
方法   : (1) 复算 v=(√2G_F)^(-1/2)、G_F=1/(√2v²)、g=2m_W/v 定义闭合性;
         (2) 核验 sin²θ_W on-shell vs PDG (0.22339) 与 MS-bar (0.23122);
         (3) 判定 DEFN"定义闭合"是否越界(是否实为实验输入)。
"""
import json
import mpmath as mp
mp.mp.dps = 40
mpp = mp.mpf
pi = mp.pi
sqrt2 = mp.sqrt(2)
results = {"meta":{"date":"2026-10-25","engine":"mpmath dps=40","basis":"主线A §3.1 vs PDG 2024 电弱参数"}}

print("="*72)
print("一、电弱参数定义闭合复算")
GF = mpp('1.1663787e-5')   # PDG 实验输入(μ 衰变)
v = 1/mp.sqrt(sqrt2*GF)    # v=(√2G_F)^(-1/2)
GF_back = 1/(sqrt2*v**2)   # G_F=1/(√2v²)
mW = mpp('80.369')          # PDG m_W (GeV)
g = 2*mW/v                  # g=2m_W/v
print("  G_F (实验输入)     = %.6e GeV⁻²" % float(GF))
print("  v=(√2G_F)^(-1/2)   = %.8f GeV" % float(v))
print("  G_F=1/(√2v²)       = %.6e GeV⁻² (残差 %e)" % (float(GF_back), float(abs(GF_back-GF))))
print("  g=2m_W/v (m_W=%.3f GeV) = %.8f" % (float(mW), float(g)))
results["ew_defn"]={"GF_exp":mp.nstr(GF,7),"v":mp.nstr(v,9),"GF_reback_dev":mp.nstr(abs(GF_back-GF),4),
  "mW":mp.nstr(mW,6),"g_2mW_over_v":mp.nstr(g,9)}

print("\n"+"="*72)
print("二、sin²θ_W 口径核验 vs PDG 2024")
sw2_main = mpp('0.22320268')     # 主线A on-shell
sw2_pdg_onshell = mpp('0.22339') # PDG on-shell s²_W (0.22339±0.00010)
sw2_pdg_msbar = mpp('0.23122')   # PDG MS-bar s²_Z (0.23122±0.00004)
dev_os = abs(sw2_main-sw2_pdg_onshell)/sw2_pdg_onshell
dev_ms = abs(sw2_main-sw2_pdg_msbar)/sw2_pdg_msbar
print("  主线A on-shell 0.22320268 vs PDG on-shell 0.22339: 偏差 %.4f%% (≈%.1fσ, σ=0.00010)" % (float(dev_os*100), float(abs(sw2_main-sw2_pdg_onshell)/0.00010)))
print("  主线A on-shell 0.22320268 vs PDG MS-bar 0.23122:  偏差 %.4f%%" % (float(dev_ms*100)))
print("  ⇒ 主线A 数值接近 PDG on-shell 但差 %.1fσ; 且 on-shell 定义下该值依赖 m_W/m_Z, 非独立预言" % (float(abs(sw2_main-sw2_pdg_onshell)/0.00010)))
results["sin2thetaW"]={"mainA_onshell":mp.nstr(sw2_main,9),"pdg_onshell":mp.nstr(sw2_pdg_onshell,8),"pdg_msbar":mp.nstr(sw2_pdg_msbar,8),
  "dev_onshell_sigma":float(abs(sw2_main-sw2_pdg_onshell)/0.00010),"dev_onshell_pct":float(dev_os*100)}

print("\n"+"="*72)
print("三、DEFN'定义闭合'判定")
print("  ① v=(√2G_F)^(-1/2) 是定义式(由 G_F 定义 v), 但 G_F 数值来自 μ 衰变实验测定——非几何/公理首原;")
print("  ② g=2m_W/v 依赖实验 m_W; sin²θ_W 依赖实验 m_W,m_Z —— 均为'定义式 + 实验输入';")
print("  ③ 主线A 称 DEFN'闭合只证明口径自洽, 不构成统一证据'——此口径本身诚实;")
print("  但 '定义闭合' 实为 '实验输入锁定'(G_F/v/g/m_W 皆实验测定), 非可首原导出的闭合。")
results["defn_assess"]={"formulas":"定义式(v↔G_F, g=2mW/v, s2W 依赖 mW,mZ)","input_source":"全部实验测定(G_F μ衰变, mW/mZ 对撞机)",
  "closure_type":"实验输入锁定, 非几何首原闭合","mainA_dishonest_label":"'定义闭合'过强→实为实验输入锁定(DEFN→FIELD/实验输入)"}

print("\n"+"="*72)
print("四、判定: 主线A DEFN 层电弱参数层级")
verdict = ("主线A 将电弱参数标为 DEFN'定义闭合'**表述过强、有越界成分**: ",
    "① v/G_F/g/sin²θ_W 数值全部来自实验测定(μ 衰变 G_F、对撞机 m_W/m_Z), 非几何/公理首原; ",
    "② 它们只是'定义式相互锁定'(v↔G_F), 但锁定的是实验输入而非首原——严格层级应为 FIELD/实验输入, 非纯 DEFN; ",
    "③ sin²θ_W(on-shell)=0.22320268 vs PDG on-shell 0.22339(10), 偏差 ≈1.9σ(0.084%), 数值口径需修正; ",
    "④ 正确降级: DEFN'定义闭合'→ FIELD/有效(实验输入锁定, 口径自洽但非独立预言); sin²θ_W 数值标注 PDG 口径偏差。",
    "注: 主线A §3 文首'不构成统一证据'诚实红线保留——此审计是层级精确化, 非推翻。")
for v in verdict: print("    → " + v)
results["verdict"]="".join(verdict)

with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\算法联盟_主线A_DEFN电弱参数审计66_2026-10-25.json","w",encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\njson 已写入：算法联盟_主线A_DEFN电弱参数审计66_2026-10-25.json")
