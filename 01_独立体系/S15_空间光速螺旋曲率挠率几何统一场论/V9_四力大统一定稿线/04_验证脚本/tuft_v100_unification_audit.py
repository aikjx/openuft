# -*- coding: utf-8 -*-
"""TUFT V9.12 统一度成色审计：
A 组：形式统一平凡性判定（模板统一检验）
  A1 十二参数来源矩阵（四力 × {λ,q,s} → 内部结构固定 vs 外部输入）
  A2 模板共享检验（任意参数组共享同一普适曲线 F~(x)——模板判定）
  A3 跨力约束搜索（统计跨力耦合方程数 → 模板统一 vs 动力学统一）
B 组：力程统一恒等式判定（λ=ħ/mc 复算四力力程；预言性=输入质量恒等式）
C 组：双口径总账（实现度 50% 维持 + 预言性统一度新口径）
用法：python tuft_v100_unification_audit.py
"""
import json, math

HBARC = 197.3269804  # MeV·fm

# ---------- A1 十二参数来源矩阵 ----------
# 来源类别：内部结构固定 / 结构+数值外输 / 外部质量谱 / 外部常数 / 外部符号
params = [
    ("电磁", "λ",  "∞（Proca 无质量极限 m→0）", "内部结构"),
    ("引力", "λ",  "∞（同上）",                 "内部结构"),
    ("弱核力", "λ", "1/m_W = 2.455e-3 fm",       "外部质量谱"),
    ("剩余强核力", "λ", "1/m_π = 1.414 fm",      "外部质量谱"),
    ("电磁", "q",  "√α·Z（α=b/ρ 几何但数值外输 B02）", "结构+数值外输"),
    ("引力", "q",  "m/m_P（m、m_P 外部）",        "外部常数"),
    ("弱核力", "q", "g_W（α_W≈1/29）",           "外部常数"),
    ("剩余强核力", "q", "α_s（≈0.12，能标依赖）", "外部常数"),
    ("电磁", "s",  "−1（异号相吸）",              "外部符号"),
    ("引力", "s",  "+1（同号相吸）",              "外部符号"),
    ("弱核力", "s", "结构（± 依手征）",           "外部符号"),
    ("剩余强核力", "s", "+1",                    "外部符号"),
]
src_count = {}
for (f, p, v, c) in params:
    src_count[c] = src_count.get(c, 0) + 1

# ---------- A2 模板共享检验 ----------
# F~(x) = (1/x² + 1/x)e^{−x}：四力共享；对任意参数组曲线相同
def Ft(x):
    return (1.0/(x*x) + 1.0/x) * math.exp(-x)

x_pts = [0.3, 0.5, 1.0, 2.0, 5.0]
curve = {("x=%.1f" % x): Ft(x) for x in x_pts}
# 模板判定：同一模板、参数独立 → 形式共享 100%，跨力约束 0
A2_verdict = ("模板统一：四力共享 F~(x)（数学恒等式：势形 U∝q1q2·e^(−r/λ)/r 自动导出该曲线），"
              "普适曲线不含任何跨力参数约束——共享的是函数形式，不是参数关系")

# ---------- A3 跨力约束搜索 ----------
# 全书方程清单（核心场方程/势/力/映射），统计其中同时含 ≥2 个力的独立参数的方程数
eqs = [
    "统一势 U = s·ħc·q1q2·e^(−r/λ)/r（单力自身）",
    "统一力 F = s·ħc·q1q2·(1/r²+1/(λr))·e^(−r/λ)·r̂（单力自身）",
    "普适曲线 F~(x)（无量纲化后无参数）",
    "Proca 方程 (∇²−μ²)κ=0（λ=1/μ，单力）",
    "m = ħω/c²（质量-频率恒等式）",
    "α = b/ρ（螺旋几何恒等式）",
    "q_EM = √α·Z（定义式）",
    "q_G = m/m_P（定义式）",
    "Liénard 辐射 P ∝ κ²（单源）",
]
cross = [e for e in eqs if ("q1q2" in e and ("m_W" in e or "m_π" in e or "α_s" in e or "g_W" in e))]

# ---------- B1 力程恒等式复算 ----------
# λ = ħc/(mc²)（Compton 型恒等式）：用外部质量计算力程
masses = {"W": 80369.0, "π": 139.570, "p": 938.272}  # MeV
ranges = {k: HBARC/m for (k, m) in masses.items()}   # fm
# 预言性判定：力程全部由输入质量给出，质量谱本身 0% 内生（量子层 FAIL）
B1_verdict = ("力程 λ=ħ/mc 是恒等式：力程谱 100% 由外部输入质量决定，无独立预言；"
              "「力程统一」= 质量谱外输前提下的力程律还原（实现度 100%、预言性 0%）")

# ---------- C 双口径总账 ----------
# 实现度口径（原 V9.5，11.4 盘点表）：形式 100%、力程 100%、本源 50%、常数 0%、量子 0%
impl = {"形式层": 4.0, "力程层": 4.0, "本源层": 2.0, "常数层": 0.0, "量子层": 0.0}
# 预言性口径（新）：每层计"独立于输入的预言能力"（/4）
# 形式层：Yukawa 同形断言真实但强核力裸 Yukawa 不符（需 σr 外源 4.7/14.5）→ 3/4
# 力程层：λ=ħ/mc 恒等式，无独立预言 → 0/4
# 本源层：m=ħω/c² 是结构映射（真实但为恒等式）；q 欠定（V9.11）→ 1/4
# 常数层：0/4；量子层：0/4
pred = {"形式层": 3.0, "力程层": 0.0, "本源层": 1.0, "常数层": 0.0, "量子层": 0.0}
impl_total = sum(impl.values())/20.0
pred_total = sum(pred.values())/20.0

out = {
    "A1_param_matrix": {"rows": params, "source_counts": src_count,
                        "internal_fixed": sum(v for k, v in src_count.items() if k.startswith("内部"))},
    "A2_template": {"curve": curve, "F_tilde_1": Ft(1.0), "verdict": A2_verdict},
    "A3_cross_force": {"total_equations": len(eqs), "cross_force_equations": len(cross), "list": cross},
    "B1_range_identity": {"ranges_fm": ranges, "verdict": B1_verdict},
    "C_dual_ledger": {
        "实现度口径(原)": {"形式": "100%", "力程": "100%", "本源": "50%", "常数": "0%", "量子": "0%", "总账": "%.0f%%" % (impl_total*100)},
        "预言性口径(新)": {"形式": "%.0f%%" % (pred["形式层"]/4*100), "力程": "0%", "本源": "25%", "常数": "0%", "量子": "0%", "总账": "%.0f%%" % (pred_total*100)},
    },
    "summary": ("模板统一成立：12 参数中内部结构固定 %d 个、其余外部输入（%s）；跨力约束方程 0 条；"
                "力程为输入质量恒等式。实现度总账维持 50%%（原口径），预言性统一度新口径 %.0f%%。"
                % (sum(v for k, v in src_count.items() if k.startswith("内部")),
                   "内部结构" in src_count, pred_total*100)),
}

with open(r"D:\a10\aikjx\code\my_lib\tuft_v100_unification_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
