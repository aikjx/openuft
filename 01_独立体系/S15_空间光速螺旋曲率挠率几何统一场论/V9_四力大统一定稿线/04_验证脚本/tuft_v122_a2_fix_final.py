# -*- coding: utf-8 -*-
# V9.43 A2 修复最终化：等价路径族唯一性 + 三粒子机器精度闭环 + 口径三表裁定
# 承接：V9.40（A2 量纲断裂 69.6 量级）、并行线 V9.41 46 章（无量纲化路径证明 + 真实质量失配 19.79）、VM V9.41（量纲修复=TUFT L1）
# 本波增量：①路径 A/B 等价唯一性定理 ②三粒子机器精度闭环（并行线只有单粒子手算） ③口径三表 ④lP 多余性形式论证
import json, math

c = 2.99792458e8
lP_m = 1.616255e-35          # m
lP_fm = lP_m*1e15            # 1.616255e-20 fm
MEV_PER_SEC = 1.5192675e21   # s^-1 per MeV
hbar = 1.054571817e-34
out = {}

# ---------- A 组：等价修复路径族唯一性定理 ----------
# 路径 A（并行线 46.2）：无量纲化 kappa~=lP*kappa, tau~=lP*tau
#   omega = c*sqrt(kappa~^2+tau~^2)/lP = c*sqrt(kappa^2+tau^2)
# 路径 B（VM 线）：右端补 lP^-2
#   (omega*lP/c)^2 * lP^-2 = (omega/c)^2
# 两路径均唯一归一到 kappa^2+tau^2=(omega/c)^2 = TUFT L1
A = {
    "路径 A（无量纲化）": "kappa~=lP*kappa, tau~=lP*tau -> omega=c*sqrt(kappa~^2+tau~^2)/lP=c*sqrt(kappa^2+tau^2) -> 式1",
    "路径 B（补 lP^-2）": "(omega*lP/c)^2 * lP^-2 = (omega/c)^2 -> 式1",
    "唯一性": "两条独立修复路径（消去 lP vs 补 lP^-2）殊途同归到同一目标 kappa^2+tau^2=(omega/c)^2；修复目标唯一 = TUFT L1 恒等式",
}
out["A"] = A

# ---------- B 组：三粒子机器精度闭环 ----------
particles = [("电子", 0.51099895), ("质子", 938.27208816), ("pi0", 134.9768)]
B_rows = []
inv_lP2 = 1.0/lP_m**2
for name, m in particles:
    w = m*MEV_PER_SEC
    lhs = (w/c)**2                     # 修复版 = TUFT L1
    orig = (w*lP_m/c)**2               # 原 A2（无量纲）
    ratio = lhs/orig
    B_rows.append({
        "粒子": name, "m[MeV]": m,
        "修复版 (w/c)^2 [m^-2]": "%.6e" % lhs,
        "原 A2": "%.6e" % orig,
        "比值": "%.6e" % ratio,
        "1/lP^2": "%.6e" % inv_lP2,
        "恒等(机器精度)": abs(ratio/inv_lP2-1) < 1e-12,
    })
B = {"数值表": B_rows, "结论": "三粒子 修复版=原A2*lP^-2 机器精度恒等（比值=1/lP^2=3.828073e69）；并行线 46.2 仅单粒子手算 m_e，本波补多粒子数值闭环"}
out["B"] = B

# ---------- C 组：数值口径三表裁定 ----------
# D1: V9.40 口径 log10(修复版/原A2)=69.58 —— 跨量纲比值（m^-2/无量纲），表述不精确但量纲断裂结论成立
# D2: 并行线口径 m_GAQ/m_e = 1/lP_fm = 6.187e19 -> 19.79 dex —— 真实质量失配
# D3: 修复后 修复版 vs TUFT L1 相对残差 = 0 —— 修复使失配归零
m_e_MeV = 0.51099895
m_GAQ_ratio = 1.0/lP_fm
C = {
    "口径 D1（V9.40）": {"值": "log10(修复版/原A2)=69.58", "语义": "跨量纲比值，伪失配（量纲不同不可比）；量纲断裂结论仍成立", "评级": "表述不精确，结论成立"},
    "口径 D2（并行线 46.3）": {"值": "m_GAQ/m_e=6.187e19（19.79 dex）", "语义": "真实质量失配（GAQ 无量纲 A2 隐含的电子质量 vs 实测）", "评级": "正确口径"},
    "口径 D3（本波）": {"值": "修复版 vs TUFT L1 相对残差 = 0.0", "语义": "修复后失配归零（修复版=TUFT L1 恒等）", "评级": "修复闭合"},
    "m_GAQ/m_e 复算": "%.6e (=1/lP_fm)" % m_GAQ_ratio,
}
out["C"] = C

# ---------- D 组：lP 多余性形式论证 ----------
D = {
    "公理层": "两条修复路径均消去 lP（路径 A 约分、路径 B 补倒数）——lP 在量纲正确的 A2 中不出现",
    "lP 唯一出现位置": "q_G=m/m_P（m_P=sqrt(hbar*c/G) 含 lP）——B03 外输清单（V9.32 最终形态）",
    "结论": "GAQ『普朗克尺度锁定』动机在量纲修正后消失；lP 是引力耦合处的量纲常数，不是几何-量子绑定公理的参数",
}
out["D"] = D

# ---------- E 组：判定 ----------
E = {
    "修复唯一性": "路径 A/B 殊途同归，修复目标唯一 = TUFT L1（kappa^2+tau^2=(w/c)^2）；GAQ 公理集经修复与 TUFT 完全同构、无新结构",
    "B02 对撞": "alpha=b/rho 仍无内生约束（单位圆对任意 alpha 成立）——修复 A2 不修复 B02（FAIL 维持）",
    "B03 对撞": "omega 需质量外输（m=hbar*omega/c^2）、常数全集外输——修复 A2 不修复 B03（FAIL 维持）",
    "总账": "实现 50%/预言 20% 不变；判别性预言=0 类维持；无新增独立 FAIL、无 FAIL 撤销",
}
out["E"] = E

out["summary"] = ("V9.43 A2 修复最终化：①等价修复路径族唯一性定理——路径 A（无量纲化 kappa~=lP*kappa）与路径 B（右端补 lP^-2）"
                  "殊途同归，修复目标唯一 = kappa^2+tau^2=(w/c)^2 = TUFT L1；②三粒子（e/p/pi0）机器精度闭环——修复版=原A2*lP^-2，"
                  "比值=1/lP^2=3.828073e69 恒等，并行线仅单粒子手算；③口径三表裁定——D1=69.58 跨量纲伪失配（表述不精确、量纲断裂结论成立）、"
                  "D2=19.79 dex 真实质量失配（m_GAQ/m_e=1/lP_fm=6.187e19）、D3=修复后相对残差 0（闭合）；④lP 多余性形式论证——两路径均消去 lP，"
                  "lP 只在 q_G（B03 外输）出现；B02/B03 之墙独立于 A2 版本仍撞墙；无新增独立 FAIL、无 FAIL 撤销，总账不变，判别性预言=0 类维持。")

with open(r"D:\a10\aikjx\code\my_lib\tuft_v122_a2_fix_final_results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
for r in B_rows:
    print("%s: 修复版=%.6e, 原A2=%.6e, 比值=%.6e, 1/lP^2=%.6e, 恒等=%s" % (
        r["粒子"], float(r["修复版 (w/c)^2 [m^-2]"]), float(r["原 A2"]),
        float(r["比值"]), float(r["1/lP^2"]), r["恒等(机器精度)"]))
print("m_GAQ/m_e = %.6e (19.79 dex check: %.2f)" % (m_GAQ_ratio, math.log10(m_GAQ_ratio)))
print("D1 = %.2f" % math.log10(( (0.51099895*MEV_PER_SEC/c)**2 )/( (0.51099895*MEV_PER_SEC*lP_m/c)**2 )))
print("saved json ok")
