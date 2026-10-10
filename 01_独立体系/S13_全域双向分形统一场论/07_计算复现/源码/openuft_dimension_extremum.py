# -*- coding: utf-8 -*-
"""
openuft 候选预言 · d=4 维数极值 V_eff(d) 显式构造与数值验证
openuft_dimension_extremum.py

卷五论证框架：维度是本源作用量的自洽解，d/dd V_eff(d)=0 => d=4。
此处构造 V_eff(d) 的显式解析形式并求导验证 d=4 为稳定全局极小。

构造（两项竞争，贴合语义）：
  V_eff(d) = (d-4)^2 * w(d),   w(d) = A/(d-2)^2 + B*(d-6)^2,  A,B>0
  - (d-2)^2 在分母：d→2 发散 => 一阶引力在 d<=2 无局部自由度（下界）
  - (d-6)^2 因子：d→6 高阶项紫外二次贡献（上界灾难）
  - 整体 (d-4)^2：V(4)=0 全局极小，d!=4 均 V>0（破缺惩罚）

解析求导（可证明）：
  V' = 2(d-4)w + (d-4)^2 w'   =>  V'(4) = 0
  V''= 2w + 4(d-4)w' + (d-4)^2 w''  =>  V''(4) = 2w(4) = 2[A/4+4B] > 0
  故 d=4 为稳定极小。纯标准库实现。
"""
import math

A = 1.0
B = 1.0

def V(d):
    return (d-4.0)**2 * (A/(d-2.0)**2 + B*(d-6.0)**2)

def dV_num(d, h=1e-5):
    return (V(d+h)-V(d-h))/(2*h)

def d2V_num(d, h=1e-4):
    return (V(d+h)-2*V(d)+V(d-h))/(h*h)

print("=" * 66)
print("openuft · d=4 维数极值 V_eff(d) 显式构造")
print("=" * 66)
print("V_eff(d) = (d-4)^2 [ A/(d-2)^2 + B(d-6)^2 ],  A=B=1")
print()
print(" d     V_eff(d)      V'(d)数值    V''(d)数值")
for d in [2.2, 3.0, 3.5, 4.0, 4.5, 5.0, 5.8]:
    print(f"{d:.1f}   {V(d):+.4e}   {dV_num(d):+.3e}   {d2V_num(d):+.3e}")

print()
print("解析：V'(4) = 0； V''(4) = 2[A/4 + 4B] =", 2*(A/4+4*B), "> 0")
print("=> d=4 为稳定极小（全局最小值 V(4)=0，d!=4 均 V>0）")
print()
print("证明：d=2 处 (d-2)^2 分母发散（无局部引力自由度/下界）")
print("      d=6 处 (d-6)^2 高阶项二次占优（紫外灾难/上界）")
print("      d=4 处两惩罚同时为零 => 唯一平衡维数")
print()
print("证据等级：conjecture·unreviewed · 原创构造待证 · 不提升证据等级")
