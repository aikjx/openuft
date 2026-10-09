# -*- coding: utf-8 -*-
# v33_精细结构常数α_螺旋螺距比量子化正面攻击.py
# 主题：α=1/137.036 能否由框架的「螺旋螺距比 τ/κ = α」经拓扑/几何量化推出？
#       框架本源方程(v5)诚实标注 α 为测量锚(非导出)。本版正面攻击该开放项，
#       并审计一份旧声称「从拓扑本征值推出 N=137 完成 α 本源推导」的文件。
# 方法：mpmath 60 位高精度；6 个独立子攻击，每个带诚实 verdict。
# 红线：不粉饰负面结果为 PASS；循环论证/自相矛盾一律 FAIL。
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import mpmath as mp
mp.mp.dps = 60

# ---- CODATA 锚 ----
G = mp.mpf('6.67430e-11')
hbar = mp.mpf('1.054571817e-34')
c = mp.mpf('299792458')
k_e = mp.mpf('8.9875517923e9')
e_charge = mp.mpf('1.602176634e-19')
alpha = e_charge**2 * k_e / (hbar * c)          # 精细结构常数
lP = mp.sqrt(hbar * G / c**3)
m_e = mp.mpf('9.1093837015e-31')
R_e = hbar / (m_e * c)                            # 电子世界线曲率半径(Compton 类)
inv_alpha = 1/alpha

RESULTS = []

def run_check(name, verdict, detail, residual=None, note=None):
    RESULTS.append({"name": name, "verdict": verdict, "detail": detail,
                    "residual": (str(residual) if residual is not None else None),
                    "note": note})
    tag = {"PASS": "✅", "FAIL": "❌", "部分闭合": "⚠️", "INFO": "ℹ️"}.get(verdict, "·")
    print(f"  {tag} {name}: {verdict} | {detail}")

# ============================================================
# Q18 本源方程自洽：κ̃²+τ̃²=1, α=τ̃/κ̃（框架内部机器零）
# ============================================================
def q18_origin_equation():
    kappa_t = 1/mp.sqrt(1+alpha**2)
    tau_t = alpha/mp.sqrt(1+alpha**2)
    r1 = abs(kappa_t**2 + tau_t**2 - 1)
    r2 = abs(tau_t/kappa_t - alpha)
    if r1 < mp.mpf('1e-50') and r2 < mp.mpf('1e-50'):
        return ("PASS",
                "本源方程 κ̃²+τ̃²=1 与 α=τ̃/κ̃ 自洽(残差均机器零)；κ̃=%.7f, τ̃=%.7f，"
                "与 v5 报告『万物同构』一致(所有带电粒子共享同一 κ̃,τ̃，差异仅在质量标度 R=ℏ/mc)。" % (float(kappa_t), float(tau_t)),
                r1, "框架内部自洽")
    return ("FAIL", "本源方程不自洽", r1)

# ============================================================
# Q19 审计「N=137 文件」：同一推导给出三个互相冲突的 N
# ============================================================
def q19_audit_n137():
    # 该文件 §2.2 证 b/ρ = √N；§2.3 称 α = b/ρ = tanθ ⇒ α = √N ⇒ N = α²
    # §5.4 又称 α = sin(1/√N) ≈ 1/√N ⇒ N = 1/α²
    # §9.3 又称 N=137（直接从 1/α=137.036 反读）
    # 三者互相冲突：
    N_A = alpha**2                       # α=√N 支路
    N_B = 1/alpha**2                     # α=1/√N 支路
    N_C = mp.mpf('137')                  # 反读支路
    # 冲突比
    ratio_BC = abs(N_B - N_C)/N_C        # 应 ~136 (18779 vs 137)
    ratio_AC = abs(N_A - N_C)/N_C        # 应 ~1 (但因 N_A<<1，绝对差≈137)
    # Δ_top 审计：文件公式 Δ_top = 1/(4π²)(1+α/√(1+α²))，实测需 0.035999
    delta_top_formula = 1/(4*mp.pi**2)*(1 + alpha/mp.sqrt(1+alpha**2))
    delta_top_needed = inv_alpha - N_C   # 0.035999...
    delta_resid = abs(delta_top_formula - delta_top_needed)/delta_top_needed
    inconsistent = (ratio_BC > mp.mpf('10'))  # N_B 与 N_C 差两个数量级
    if inconsistent:
        return ("FAIL",
                "N=137 文件自相矛盾：同推导给出 N=α²=%.2e(α=√N 支)、N=1/α²=%.1f(α=1/√N 支)、"
                "N=137(反读支)，三者互差 10^2 倍；且 Δ_top 公式=%.4f 与所需 %.4f 差 %.0f%%。"
                "N=137 系从实验 1/α 反读，属循环论证。" % (float(N_A), float(N_B), float(delta_top_formula), float(delta_top_needed), float(delta_resid*100)),
                ratio_BC, "循环论证+自相矛盾")
    return ("INFO", "N=137 自洽", ratio_BC)

# ============================================================
# Q20 框架拓扑不变量能否命中 1/α ≈ 137.036？
# ============================================================
def q20_topo_invariant():
    # 框架实有拓扑不变量：SU(2)_k 量子维数 d_j=2cos(π(j+1)/(k+2))（v28/v29），
    # 代际 k=2，黄金比 k=3。这些量为 O(1)（最大 2），远小于 137。
    # 另扫简单整数公式 k+2 / 2(k+2) / (k+2)²（k=框架层级 2,3,4,6,8）：均 << 137。
    best_err = mp.mpf('1')
    best_desc = ""
    for k in [2, 3, 4, 6, 8, 12]:
        for form, val in [("k+2", k+2), ("2(k+2)", 2*(k+2)), ("(k+2)^2", (k+2)**2),
                           ("2cos(pi/(k+2))", 2*mp.cos(mp.pi/(k+2)))]:
            err = abs(val - inv_alpha)/inv_alpha
            if err < best_err:
                best_err = err; best_desc = "k=%d,%s=%.4f" % (k, form, float(val))
    # 1/α 距最近整数 137 仅 0.036，但 137 在框架中无理论地位(框架整数=2,3,4,6 代/层)
    nearest_int = mp.floor(inv_alpha + mp.mpf('0.5'))
    int_err = abs(nearest_int - inv_alpha)
    if best_err > mp.mpf('0.1'):  # 无任何拓扑不变量在 10% 内命中
        return ("FAIL",
                "框架拓扑不变量(SU(2)_k 维数 O(1)、层级 2/3/4/6)均远小于 137；"
                "1/α=%.3f 距整数 %d 仅 %.3f，但 137 在框架中无理论地位(框架整数=2,3,4,6)。"
                "最近匹配 %s，误差 %.0f%%。α 值未被框架拓扑量化推出。" % (float(inv_alpha), int(nearest_int), float(int_err), best_desc, float(best_err*100)),
                best_err, "无拓扑起源")
    return ("INFO", "意外匹配", best_err)

# ============================================================
# Q21 审计「相位闭合 ⇒ n=N=137」：实际给出 n=1
# ============================================================
def q21_phase_closure():
    # 文件 §4.2：p=mc, 又 p=ℏ/ρ ⇒ mc=ℏ/ρ ⇒ ρ=ℏ/(mc)=R；
    # 相位闭合 ∮p·ds = p·2πρ = 2πnℏ ⇒ pρ=nℏ ⇒ (ℏ/R)·R = nℏ ⇒ n=1。
    # 即相位闭合给出 n=1，而非 N=137。其「n=N_twist=137」系错用。
    rho = R_e
    p = hbar/rho
    n = p*rho/hbar
    resid = abs(n - 1)
    if resid < mp.mpf('1e-50'):
        return ("FAIL",
                "相位闭合条件 ∮p·ds=2πnℏ 在框架几何下严格给出 n=pρ/ℏ=(ℏ/R)·R/ℏ=1（机器零），"
                "而非该文件声称的 N=137。其『n=N_twist=137』系代数错用循环论证。",
                resid, "相位闭合⇒n=1(非137)")
    return ("INFO", "相位闭合异常", resid)

# ============================================================
# Q22 最小半径 √2 ℓ_P 能否约束螺距比 α=h/R？
# ============================================================
def q22_min_radius_constraint():
    # Frenet 螺旋：τ/κ = h/R（h=螺距参数, R=曲率半径）。框架 α=τ/κ ⇒ h = α·R。
    # 最小半径约束 R_min=√2 ℓ_P（v31 Q04 最优截断）。对电子 R=R_e=ℏ/(m_e c)。
    R_min = mp.sqrt(2)*lP
    h = alpha * R_e
    ratio = h / R_min
    # 若 α 受最小半径约束应有 h ~ R_min，即 ratio ~ O(1)；实际 h >> R_min 多个量级
    if ratio > mp.mpf('1e10'):
        return ("FAIL",
                "电子螺旋 h=αR_e=%.2e m，最小半径 √2ℓ_P=%.2e m，h/√2ℓ_P=10^%.1f ≫1；"
                "最小半径约束对 α 完全松弛，不提供任何量化机制。α 值仍自由。" % (float(h), float(R_min), float(mp.log(ratio,10))),
                ratio, "最小半径不约束α")
    return ("INFO", "最小半径约束 α", ratio)

# ============================================================
print("=== v33: 精细结构常数 α · 螺旋螺距比量子化正面攻击 ===")
run_check("Q18_本源方程自洽", *q18_origin_equation())
run_check("Q19_审计N=137文件", *q19_audit_n137())
run_check("Q20_拓扑不变量匹配", *q20_topo_invariant())
run_check("Q21_相位闭合审计", *q21_phase_closure())
run_check("Q22_最小半径约束", *q22_min_radius_constraint())

n_pass = sum(1 for r in RESULTS if r["verdict"] == "PASS")
n_fail = sum(1 for r in RESULTS if r["verdict"] == "FAIL")
n_part = sum(1 for r in RESULTS if r["verdict"] == "部分闭合")
n_info = sum(1 for r in RESULTS if r["verdict"] == "INFO")
print(f"\n=== v33 合计 {len(RESULTS)} 项: PASS {n_pass} / FAIL {n_fail} / 部分闭合 {n_part} / INFO {n_info} ===")

with open("v33_精细结构常数α_螺旋螺距比量子化正面攻击_核验结果.json", "w", encoding="utf-8") as f:
    json.dump({"suite": "v33", "mp_dps": mp.mp.dps, "counts": {"pass": n_pass, "fail": n_fail,
              "partial": n_part, "info": n_info, "total": len(RESULTS)}, "results": RESULTS},
              f, ensure_ascii=False, indent=2)
print("产物已写 v33_精细结构常数α_螺旋螺距比量子化正面攻击_核验结果.json")
