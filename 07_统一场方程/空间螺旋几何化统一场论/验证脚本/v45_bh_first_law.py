# -*- coding: utf-8 -*-
"""
v45：黑洞热力学第一定律与 Hawking 温度修正（挠率熵自洽）
承接 42 稿：S_H = (A/4G)(1 + 8πG g τ_H)，C = 1+8πG g τ_H。
第一定律 dM = T dS（固定 τ_H、无转动/电荷）：
  Schwarzschild: r_H=2GM, A=4πr_H^2, S=C·4πGM^2, dS/dM=C·8πGM
  => T = 1/(dS/dM) = T_Sch/(1+8πG g τ_H),  T_Sch=1/(8πGM)
Hawking 辐射功率 P~T^4 A（d=4）=> P = P_Sch/C^4；蒸发寿命 τ~M^3/P。
"""
import json
import numpy as np

G = 1.0                      # 自然单位
G_norm = 1.0/(16*np.pi)      # 普朗克归一 16πG=1
M_solar = 1.0                # 基准质量（标度任意）

def C_factor(gv, tv): return 1 + 8*np.pi*G_norm*gv*tv

results = {}
print("第一定律 + Hawking 温度修正（τ_H 固定）：T_H = T_Sch/(1+8πG g τ_H)")
for glab, gv, tv in [("g=0.01",0.01,1.0),("g=0.1",0.1,1.0),("g=1",1.0,1.0),
                     ("g=0.1,τ=-1",0.1,-1.0),("g=0.5,τ=2",0.5,2.0)]:
    C = C_factor(gv, tv)
    T_ratio = 1.0/C          # T_H / T_Sch
    P_ratio = T_ratio**4     # P_H / P_Sch
    life_ratio = 1.0/P_ratio # 寿命比
    results[glab] = {"g":gv,"tau_H":tv,"C":float(C),
                     "T_ratio":float(T_ratio),"P_ratio":float(P_ratio),"life_ratio":float(life_ratio)}
    print("  %-12s C=%+.4f  T修正=%+.4f  P修正=%+.4e  寿命比=%+.2f" %
          (glab, C, T_ratio, P_ratio, life_ratio))

# 第一定律自洽性核对：对固定 τ_H，dM = T dS 精确成立（T=1/(dS/dM)）
# 验证数值：M 扰动 dM -> dS = C·8πGM·dM，T·dS = (1/(C·8πGM))·C·8πGM·dM = dM ✓
rec = {
    "entropy": "S_H = (A/4G)(1 + 8πG g τ_H)",
    "first_law": "dM = T dS (固定 τ_H, 无转动/电荷)",
    "derivation": "S=C·4πGM^2, dS/dM=C·8πGM, T=1/(dS/dM)=T_Sch/(1+8πG g τ_H)",
    "hawking_temp": "T_H = T_Sch/(1+8πG g τ_H), T_Sch=1/(8πGM)",
    "radiation": "P_H = P_Sch/(1+8πG g τ_H)^4 (d=4); 寿命 τ_life 放大 C^4",
    "scan": results,
    "caveats": ["τ_H 固定假设；若 τ_H(M) 依赖需含 dτ_H 项", "仅标量挠率扇区", "Schwarzschild 型"],
}
out = r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\空间螺旋几何化统一场论\V3_16_bh_first_law.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(rec, f, ensure_ascii=False, indent=2)
print("saved V3_16_bh_first_law.json")
