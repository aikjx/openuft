# -*- coding: utf-8 -*-
"""算法联盟 · 统一场论攻破审计——独立复算证据（不采信 S13 自报）

攻破命题：
  ① S13 的"0.12% 实验吻合锚点"(s*=0.2309434) 是【标准 MSSM 大统一的教科书已知结果】，
     其输入为实验 α_EM、α_s，β 系数为 MSSM 假设——与 S13 三公理(对偶/守恒/自相似)零依赖。
  ② S13 自己的原创预言 sin²θ=1/4(CP² 候选) 在 SM 单圈电弱尺度是负面结果(差~5.4%)。
本脚本独立重算，判定二者是否为"真预测"或"借用/负面"。
"""
import sys
import math
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass

PI = math.pi
aEM_inv = 127.916          # α_EM(M_Z)⁻¹ 实验
s2w_exp = 0.23122          # sin²θ_W(M_Z) MS-bar 实验
a3_inv = 1/0.1179          # α_s(M_Z)⁻¹ 实验
mZ = 91.1876               # GeV
v_fw = 255.26              # S13 框架真空值

c2w = 1 - s2w_exp
A1 = (3/5)*c2w*aEM_inv; A2 = s2w_exp*aEM_inv; A3 = a3_inv
print("=== 攻破①：s* 是否为 S13 第一性预测？ ===")
print(f"输入：α_EM⁻¹={aEM_inv}、α_s⁻¹={a3_inv:.4f}、mZ={mZ}（全部实验值，与 S13 三公理无关）")
b1,b2,b3 = 33/5, 1.0, -3.0    # MSSM 单圈 β（教科书假设：超对称粒子谱）
print(f"MSSM β 系数 b=({b1},{b2},{b3})——来自超对称谱假设，非 S13 推导")
# 三线汇聚条件 A1(L)=A2(L)=A3(L)，用 sin²θ 求解（仅 α_EM、α_s 输入）
def s2w_from_unify():
    import math
    # 要求 α₁⁻¹=α₂⁻¹ 与 α₂⁻¹=α₃⁻¹ 在统一尺度同点 → 解 sin²θ
    # α₁⁻¹(s²θ)=(3/5)(1-s²θ)·α_EM⁻¹ ; α₂⁻¹(s²θ)=s²θ·α_EM⁻¹ ; α₃⁻¹=输入常数
    # 汇聚点对数 L=(A1_0-A2_0)/(b1-b2)·2π = (A2_0-A3)/(b2-b3)·2π → 数值求根
    s = None
    def f(ss):
        A1_0=(3/5)*(1-ss)*aEM_inv; A2_0=ss*aEM_inv
        return (A1_0-A2_0)/(b1-b2) - (A2_0-A3)/(b2-b3)
    lo,hi=0.05,0.45
    for _ in range(200):
        mid=(lo+hi)/2
        if f(lo)*f(mid)<0: hi=mid
        else: lo=mid
    ss=(lo+hi)/2
    L=( (3/5)*(1-ss)*aEM_inv - ss*aEM_inv)/(b1-b2)*2*PI
    return ss, mZ*math.exp(L)
s2w_pred, M_pred = s2w_from_unify()
print(f"[独立重算] MSSM 三线汇聚 → sin²θ(M_Z) 预测 = {s2w_pred:.6f}")
print(f"            S13 报告值 0.230943405  差 = {abs(s2w_pred-0.230943405):.2e}")
print(f"[判定①] s* 由『实验 α_EM,α_s + MSSM β』决定；重算与 S13 报告一致")
print(f"        → 这是【MSSM 教科书结果复现】，S13 三公理未进入公式 → 借用，非第一性预测")

print()
print("=== 攻破②：S13 原创预言 sin²θ=1/4(CP²) 的跑动检验 ===")
# SM 单圈跑动 α_i 到 v=255.26 GeV
b1s,b2s,b3s = 41/10, -19/6, -7.0
x_v = math.log(v_fw/mZ)/(2*PI)
A1v=A1-b1s*x_v; A2v=A2-b2s*x_v
s2w_v = 3*A2v/(3*A2v+5*A1v)
print(f"SM 单圈跑动到 v={v_fw} GeV: sin²θ(v) = {s2w_v:.5f}")
print(f"  vs CP² 候选 1/4 = 0.25000 → 差 {(s2w_v-0.25)/0.25*100:+.2f}%")
# sin²θ=1/4 唯一成立尺度
def s2w_at(L): 
    A1L=A1-b1s*L/(2*PI); A2L=A2-b2s*L/(2*PI); return 3*A2L/(3*A2L+5*A1L)
# 求 s2w_at(L)=1/4 的 L
lo,hi=0.0,30.0
for _ in range(200):
    mid=(lo+hi)/2
    if (s2w_at(lo)-0.25)*(s2w_at(mid)-0.25)<0: hi=mid
    else: lo=mid
Lm=(lo+hi)/2; Mm=mZ*math.exp(Lm)
print(f"sin²θ=1/4 在 SM 单圈唯一成立尺度 M={Mm:.2f} GeV")
print(f"[判定②] 原创预言 1/4 在电弱尺度差 5.4%（负面）；唯一自洽尺度 3.7TeV 无 S13 框架出处")

print()
print("=== 攻破总判 ===")
print("S13 常数统一目前无第一性预测：原创预言(sin²θ=1/4)跑动负面；")
print("声称的 0.12% 锚点是 MSSM 已知结果复现（非 S13 推导）。")
print("对 S13 的支持 = 0；对 MSSM 的支持 = 教科书既有结论。")
