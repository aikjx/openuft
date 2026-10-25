# -*- coding: utf-8 -*-
"""
算法联盟 · 统一场论攻破 · 第63期：α*/G*=0.4773 【已证-几何】层级审计 —— 首原导出 vs 场内容/方案相关
================================================================================
日期   : 2026-10-25
对标   : 主线A总纲 §2.5(α*/G*=0.4773【已证-几何】DERIV) + 本源精算脚本L101 + 权威定本附录B(M3证伪)
引擎   : mpmath dps=40
攻破点 : 主线A把 α*/G*=0.4773 标为【已证-几何】DERIV("不动点线性关系，无自由参数")，
         但附录B M3证伪已明确"0.4773 系引力 β_G 跑动、方案相关——不能由 su(3) Casimir 首原"，
         且本源精算脚本只是硬编码 ratio_fp=0.4773 输入(L101注释"已首原导出"非推导)。
         需审计: 0.4773 的真正来源(不动点线性关系 α*/G*=-D1/D2)是否依赖场内容(D1/D2/β系数)，
         是否方案相关，是否被 M3 证伪牵连 → 判定 DERIV 层级是否越界残留、须降级。
方法   : (1) 复算 α*/G* = -D1/D2 来源(V3.4 β 系数 D1=0.5318, D2=-1.114);
         (2) 核对 D1/D2/C4 是否为场内容输入(非首原);
         (3) 对照附录B M3 证伪 → 判定层级。
"""
import json
import mpmath as mp
mp.mp.dps = 40
mpp = mp.mpf
results = {"meta":{"date":"2026-10-25","engine":"mpmath dps=40","basis":"主线A §2.5 / 附录B M3 / 本源精算脚本"}}

print("="*72)
print("一、0.4773 的来源复算: 不动点线性关系")
print("  V3.4 β 函数: β_α = D1·G + D2·α, 不动点要求 β_α=0")
D1 = mpp('0.5318'); D2 = mpp('-1.114')
ratio = -D1/D2
print("  α*/G* = -D1/D2 = %.3f/%.3f = %.6f  (V3.4 β 系数)" % (float(D1), float(abs(D2)), float(ratio)))
print("  主线A/本源精算脚本声称 0.4773; 复算 -D1/D2 = %.6f" % float(ratio))
results["ratio_compute"]={"D1":mp.nstr(D1,6),"D2":mp.nstr(D2,6),
  "ratio_minus_D1_over_D2":mp.nstr(ratio,7),"claimed":mp.nstr(mpp('0.4773'),7)}

print("\n"+"="*72)
print("二、支撑 D1/D2/C4 是否场内容输入(非首原)?")
print("  V3.4 RG流脚本: C1=0.12 C2=-0.35 C3=0.08 C4=0.0597; D1=0.5318 D2=-1.114; F1=1 F2=0 F3=-1")
print("  ⇒ 全部为**硬编码数值输入**(脚本 L7-9), 非由公理+几何第一性推导")
print("  ⇒ 0.4773 = -D1/D2 依赖 D1/D2(场内容), 非纯几何首原")
results["field_content"]={"beta_coeffs":"C1=0.12 C2=-0.35 C3=0.08 C4=0.0597; D1=0.5318 D2=-1.114",
  "input_or_derived":"ALL hard-coded inputs in TUFT_V3.4_RG流数值积分_2026-10-10.py L7-9",
  "ratio_depends_on_field_content":True}

print("\n"+"="*72)
print("三、对照附录B M3 证伪")
print("  权威定本附录B: 'C4=0.0597, 0.4773 非规范一圈 b0, 系引力 β_G 跑动、**方案相关**——"
      "不能由 su(3) Casimir 首原; YB 降为自洽重参数化'")
print("  ⇒ 0.4773 已被登记为方案相关、不能首原导出")
results["M3"]={"verdict":"0.4773 scheme-dependent, NOT first-principle from su(3) Casimir (附录B M3)",
  "ratio_scheme_dependent":True,"first_principle":False}

print("\n"+"="*72)
print("四、判定: DERIV 层级是否越界残留")
verdict = ("主线A §2.5 将 α*/G*=0.4773 标为【已证-几何】DERIV('不动点线性关系，无自由参数')属**越界残留**: ",
           "0.4773 的确由不动点线性关系 β_α=0 导出(=-D1/D2≈0.4774, 无自由参数), ",
           "但支撑它的 D1/D2 及全套 β 系数(C1-C4)是 V3.4 硬编码**场内容输入**、非几何首原, ",
           "且附录B M3 已证伪其 su(3) Casimir 首原来源并登记为**方案相关**。",
           "正确降级: α*/G* 由【已证-几何】DERIV 降为 **FIELD(依赖场内容 β 系数)** 或 DEFN(定义闭合/自洽), ",
           "与主线A四层判据'FIELD 需场内容输入'对齐; 0.4773 数值本身为代数关系(有效), 但其'无参数首原'地位被否定。")
for v in verdict: print("    → " + v)
results["verdict"]="".join(verdict)

with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\算法联盟_alphaG不动点比层级审计63_2026-10-25.json","w",encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\njson 已写入：算法联盟_alphaG不动点比层级审计63_2026-10-25.json")
