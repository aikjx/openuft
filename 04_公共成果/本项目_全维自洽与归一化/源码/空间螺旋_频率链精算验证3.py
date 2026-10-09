# -*- coding: utf-8 -*-
"""
空间螺旋几何化统一场论 · 频率链精算验证·三期（2026-09-27）
================================================================
覆盖与交叉验证：
  C15   第五力 F₅=(ℏ/2)dω/dt：匀速螺旋分支恒零验证（核心发现候选）
        解析：R(t)=(ρcosωt, ρsinωt, bωt)，ω 为常数参数 ⇒ dω/dt≡0 ⇒ F₅≡0
        数值：mpmath 250 位对常数函数求导（mp.diff）交叉验证 = 机器零
        量纲复核：原体系 X11 已承认 [F₅]=M·L²·T⁻³=功率(W)≠力
  C14   影响面扫描：C14 字面公式被 C62 否定后，下游依赖 ω 公式的
        claims（C10/C15/C25/C26）在「正确组合 c√(κ²+τ²)=c/L」下的重核对
方法：解析证明 + mpmath 250 位数值交叉验证
幂等覆盖输出：数据/空间螺旋频率链_精算验证3.json / .md
"""
import mpmath as mp
import json, io, os

mp.mp.dps = 250

c   = mp.mpf("299792458")
hbar = mp.mpf("1.0545718176461565e-34")
rho = mp.mpf("1")
b   = mp.mpf("0.0072973525693")   # b/ρ = α（C03）
L   = mp.sqrt(rho*rho + b*b)
omega0 = mp.mpf("1.23558996e20")  # C25 螺旋特征频率（常数参数）

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "数据")
OUT_DIR = os.path.abspath(OUT_DIR)

res = {
    "title": "空间螺旋几何化统一场论 · 频率链精算验证·三期",
    "date": "2026-09-27",
    "dps": 250,
    "method": "解析证明 + mpmath 250 位数值交叉验证",
    "checks": [],
}

def fmt(x, n=16):
    return mp.nstr(x, n)

def rel_err(a, e):
    return abs(a - e) / abs(e) if e != 0 else abs(a)

# =================================================================
# 1. C15 第五力恒零验证（核心）
# =================================================================
# 运动学：R(t)=(ρcosωt, ρsinωt, bωt)；ω 为常数参数（纲领唯一构造，
#         无「频率如何被控制」机制——02_全维分析合订本诚实边界）
# dω/dt ≡ 0（常数导数）⇒ F₅ = (ℏ/2)·dω/dt ≡ 0（任意 t）
# 数值交叉：mp.diff(常数函数, t) 应为机器零
t0 = mp.mpf("1.0")
domega_dt_num = mp.diff(lambda t: omega0, t0)      # 常数函数数值导数
F5 = (hbar / 2) * domega_dt_num
# 匀速交叉验证：极角 φ(t)=ωt ⇒ d²φ/dt²=0（匀速圆周投影）
d2phi = mp.diff(lambda t: omega0 * t, t0, 2)
# 量纲复核（X11 原体系自查）：[ℏ]=M·L²·T⁻¹、[dω/dt]=T⁻² ⇒ [F₅]=M·L²·T⁻³=功率
# R(t) 三阶导（匀速螺旋特征）：|R'''| = ω³√(ρ²+b²) = ω³L（频率恒定 ⇒ 高阶导同频）

res["checks"].append({
    "id": "C15", "name": "第五力 F₅=(ℏ/2)dω/dt 匀速螺旋恒零",
    "analytic": "R(t)=(ρcosωt,ρsinωt,bωt)，ω=const ⇒ dω/dt≡0 ⇒ F₅≡0（任意 t）；"
                "纲领无变速机制（无「频率如何被控制」）⇒ F₅ 无任何非零落点",
    "domega_dt_numeric": fmt(domega_dt_num),
    "F5_numeric": fmt(F5),
    "d2phi_dt2": fmt(d2phi) + "（匀速：极角二阶导=0）",
    "dimension_note": "[ℏ]=M·L²·T⁻¹、[dω/dt]=T⁻² ⇒ [F₅]=M·L²·T⁻³=功率(W)，非力（原体系 X11 已承认）",
    "conclusion": "双重失效：匀速分支 F₅≡0（恒等消去，暗能量关联零内容）+ 量纲为功率非力 ⇒ falsified",
})

# =================================================================
# 2. C14 影响面扫描（下游依赖 ω 公式的 claims 重核对）
# =================================================================
# C14 字面公式已由 C62 否定；正确组合 ω=c√(κ²+τ²)=c/L
kappa = rho / (rho*rho + b*b)
tau   = b / (rho*rho + b*b)
w_correct = c * mp.sqrt(kappa**2 + tau**2)   # = c/L
w_cons = c / L
rel_ok = rel_err(w_correct, w_cons)

# C10：E=ℏω=ℏc/ℓ（已验证 PASS）；此处快照重核
ell = 1 / mp.sqrt(kappa**2 + tau**2)
E_ell = hbar * c / ell
E_omega = hbar * w_correct
rel_c10 = rel_err(E_ell, E_omega)

# C25：LB 本征谱 ω 为独立自由参数（ω=1.23558996e20），E_n=(ω²/c²)(V₀+n²ℏ²/N²)
#     不依赖 C14 频率公式；核对 E_n 定义与光速约束无直接冲突（ω 是输入参数）
En1 = (omega0**2 / c**2) * (mp.mpf("1.0") + (hbar**2) / (mp.mpf("18907")**2))
# C26：κ_drive=ρω²/c² 曲率驱动（几何类比，已复核 PASS）；字面 ω 取 c/L 时
#     κ_drive=ρ/L²=κ（与 C02 曲率一致，量纲 [L⁻¹] 合法）——复核 PASS
w_L = w_correct
kappa_drive = rho * w_L**2 / c**2
rel_kdrive = rel_err(kappa_drive, kappa)

res["checks"].append({
    "id": "C14-impact", "name": "C14 影响面扫描（正确组合重核对）",
    "w_correct": fmt(w_correct),
    "rel_vs_constraint": fmt(rel_ok),
    "C10": "PASS（ℏc/ℓ vs ℏω 偏差 %s）" % fmt(rel_c10),
    "C15": "独立失效（匀速恒零，见 §1）",
    "C25": "独立自由参数（ω=1.2356e20 输入，不依赖 C14 公式）；E₁=%.10e" % En1,
    "C26": "κ_drive=ρ(ω=c/L)²/c²=κ（C02 曲率精确一致，偏差 %s）⇒ PASS 复核" % fmt(rel_kdrive),
    "conclusion": "C14 字面公式否定不污染下游：正确组合 c√(κ²+τ²) 与 C10/C24/C39 全链相容；C15 独立死亡；C25/C26 不受影响",
})

# ---------------- 汇总 ----------------
verdict = ("频率链精算验证·三期：C15 第五力双重失效（匀速螺旋 F₅≡0 恒等消去 + 量纲功率非力）"
           "⇒ 建议登记 C63（falsified）；C14 影响面扫描无新增污染（正确组合全链相容）" % ())
res["verdict"] = verdict

os.makedirs(OUT_DIR, exist_ok=True)
json_path = os.path.join(OUT_DIR, "空间螺旋频率链_精算验证3.json")
md_path  = os.path.join(OUT_DIR, "空间螺旋频率链_精算验证3.md")

with io.open(json_path, "w", encoding="utf-8", newline="") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)

md = []
md.append("# 空间螺旋几何化统一场论 · 频率链精算验证·三期")
md.append("")
md.append("| 项 | 值 |")
md.append("|---|---|")
md.append("| 日期 | 2026-09-27 |")
md.append("| 精度 | mpmath **250 位** |")
md.append("| 结论 | C15 双重失效 ⇒ 建议登记 C63；C14 影响面无新增污染 |")
md.append("")
md.append("## 1. C15 · 第五力 F₅=(ℏ/2)dω/dt 匀速螺旋恒零（核心发现）")
md.append("")
md.append("运动学（C39 修复版）：R(t)=(ρcosωt, ρsinωt, bωt)，**ω 为常数参数**——纲领无「频率如何被控制」的机制（02_全维分析合订本诚实边界），不存在变速分支。")
md.append("")
md.append("$$\\frac{d\\omega}{dt} \\equiv 0 \\quad\\Rightarrow\\quad F_5 = \\frac{\\hbar}{2}\\,\\frac{d\\omega}{dt} \\equiv 0 \\quad(\\forall\\,t)$$")
md.append("")
md.append("| 量 | 数值（250 位） |")
md.append("|---|---|")
md.append("| dω/dt（mp.diff 交叉验证） | %s |" % fmt(domega_dt_num))
md.append("| F₅=(ℏ/2)·dω/dt | %s（机器零） |" % fmt(F5))
md.append("| d²φ/dt²（匀速交叉） | %s（=0） |" % fmt(d2phi))
md.append("")
md.append("**量纲复核**（原体系 X11 已承认）：[ℏ]=M·L²·T⁻¹、[dω/dt]=T⁻² ⇒ [F₅]=M·L²·T⁻³=**功率(W)，非力**。")
md.append("")
md.append("**双重失效**：① 匀速分支 F₅≡0（恒等消去）⇒「对应暗能量」零内容；② 量纲为功率非力（X11）。⇒ **建议登记 C63（falsified）**。")
md.append("")
md.append("## 2. C14 影响面扫描（正确组合重核对）")
md.append("")
md.append("C14 字面公式已被 C62 否定；正确组合 ω=c√(κ²+τ²)=c/L 与光速约束偏差 %s（相容）。" % fmt(rel_ok))
md.append("")
md.append("| claim | 依赖关系 | 重核对 |")
md.append("|---|---|---|")
md.append("| C10 | ℏω=ℏc/ℓ | PASS（偏差 %s） |" % fmt(rel_c10))
md.append("| C15 | dω/dt 因子 | 独立失效（§1） |")
md.append("| C25 | ω 独立自由参数 | 不受影响（E₁=%.10e） |" % En1)
md.append("| C26 | κ_drive=ρω²/c² | PASS 复核（取 ω=c/L 得 κ_drive=κ，偏差 %s） |" % fmt(rel_kdrive))
md.append("")
md.append("**结论**：C14 否定不污染下游；正确组合与 C10/C24/C39 全链相容。")
md.append("")
md.append("---")
md.append("")
md.append("*本项目审计组 · 频率链精算验证·三期 · 2026-09-27*")

with io.open(md_path, "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(md) + "\n")

print("===== 频率链精算验证·三期 =====")
print("C15 dω/dt(数值)=", fmt(domega_dt_num), " F5=", fmt(F5), " d2phi=", fmt(d2phi))
print("C15 量纲复核: [F₅]=M·L²·T⁻³=功率(W) 非力（X11）")
print("C14影响面: w_correct=", fmt(w_correct), " 约束偏差=", fmt(rel_ok), " C10偏差=", fmt(rel_c10),
      " E1=", fmt(En1), " C26偏差=", fmt(rel_kdrive))
print("结论:", verdict)
print("产出:", json_path, "|", md_path)
