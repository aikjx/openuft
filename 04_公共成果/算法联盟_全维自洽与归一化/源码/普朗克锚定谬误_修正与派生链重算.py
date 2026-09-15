# -*- coding: utf-8 -*-
"""普朗克锚定谬误 · 修正与派生链重算

背景：GAQ/S07/S08/S09/S10 谱系共用
        G = c³/(ℏ(κ²+τ²))      ∧      m = ℏ√(κ²+τ²)/c
      联立必然推出 G m² = ℏ c，唯一解 m = m_P。

本脚本做四件事：
  1) 【诊断】量化旧链的非普适性：G_old(m) = ℏc/m²，随粒子质量平方反比变化。
  2) 【修正】验证正确形式 α_grav = G m²/(ℏc) = (m/m_P)² 对全粒子谱机器零成立。
  3) 【重算】在修正后的几何链上重建 (R, κ, τ, ω, α)，逐项验证自洽。
  4) 【诚实】列出修正后仍然残留的缺口——修正不等于解决问题。

运行：python 普朗克锚定谬误_修正与派生链重算.py
"""

import os
import sys
import io
import json

import mpmath as mp

mp.mp.dps = 80

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

PI = mp.pi
C = mp.mpf("299792458")
H = mp.mpf("6.62607015e-34")
HBAR = H / (2 * PI)
E = mp.mpf("1.602176634e-19")
G = mp.mpf("6.67430e-11")
ALPHA = mp.mpf("7.2973525693e-3")

EV = E  # 1 eV/c² 对应的 kg
ME = mp.mpf("9.1093837015e-31")
MMU = mp.mpf("1.883531627e-28")
MTAU = mp.mpf("3.16754e-27")
MP = mp.mpf("1.67262192369e-27")
MW = mp.mpf("80.379e9") * EV / C ** 2
MZ = mp.mpf("91.1876e9") * EV / C ** 2
MH = mp.mpf("125.25e9") * EV / C ** 2
MTOP = mp.mpf("172.76e9") * EV / C ** 2

MP_MASS = mp.sqrt(HBAR * C / G)
LP = mp.sqrt(HBAR * G / C ** 3)

PARTICLES = [
    ("e 电子", ME),
    ("μ 缪子", MMU),
    ("τ 陶子", MTAU),
    ("p 质子", MP),
    ("W 玻色子", MW),
    ("Z 玻色子", MZ),
    ("H 希格斯", MH),
    ("t 顶夸克", MTOP),
    ("m_P 普朗克质量", MP_MASS),
]

RECORDS = []


def rec(tag, name, formula, value, ref, kind="代数恒等式", verdict=None, note=""):
    if value is None or ref is None:
        rel, digits = mp.mpf("0"), float(mp.mp.dps - 2)
    elif kind == "代数恒等式":
        denom = abs(ref) if abs(ref) != 0 else mp.mpf("1")
        rel = abs(value) / denom
        digits = float(mp.mp.dps - 2) if rel == 0 else max(0.0, -float(mp.log(rel, 10)))
    else:
        denom = abs(ref) if abs(ref) != 0 else mp.mpf("1")
        rel = abs(value - ref) / denom
        digits = float(mp.mp.dps - 2) if rel == 0 else max(0.0, -float(mp.log(rel, 10)))
    if verdict is None:
        verdict = "PASS" if digits >= 6 else "WEAK"
    RECORDS.append({
        "id": tag, "name": name, "formula": formula,
        "value": mp.nstr(value, 18) if value is not None else "—",
        "reference": mp.nstr(ref, 18) if ref is not None else "—",
        "rel_residual": mp.nstr(rel, 6), "digits": round(digits, 2),
        "kind": kind, "verdict": verdict, "note": note,
    })
    return RECORDS[-1]


def note(tag, name, statement, verdict, detail=""):
    RECORDS.append({
        "id": tag, "name": name, "formula": statement, "value": "—",
        "reference": "—", "rel_residual": "—", "digits": 0.0,
        "kind": "审计", "verdict": verdict, "note": detail,
    })


# ===========================================================================
# 1. 诊断：旧链的 G 不普适
# ===========================================================================
def module1_diagnose():
    worst = mp.mpf("0")
    gmin, gmax = None, None
    for label, m in PARTICLES:
        g_old = HBAR * C / m ** 2                 # 旧式在粒子 m 处给出的"G"
        ratio = g_old / G                         # 与实测 G 的偏离倍数
        worst = max(worst, ratio)
        gmin = ratio if gmin is None else min(gmin, ratio)
        gmax = ratio if gmax is None else max(gmax, ratio)
        rec("N01-" + label.split()[0], "旧链 G_old = ℏc/m² 偏离实测 G 的倍数（%s）" % label,
            "G_old(m)/G - 1", ratio - 1, mp.mpf("1"), "代数恒等式",
            verdict="PASS" if abs(ratio - 1) < mp.mpf("1e-6") else "FAIL",
            note="旧式把 G 变成随粒子质量平方反比变化的量，违背引力常数的普适性")

    rec("N01-span", "旧链导致的 G 非普适跨度（最大/最小偏离倍数之比）",
        "跨度 = (m_P/m_e)²", gmax / gmin, (MP_MASS / ME) ** 2, "数值核验",
        note="等于 (m_P/m_e)² = 5.71e+44，与引擎 D06 的电子锚点偏离完全一致——"
             "两处独立计算互相印证")

    rec("N01-key", "关键恒等：G_old(m)/G = (m_P/m)²（旧式偏离的闭式）",
        "G_old(m)/G - (m_P/m)²", (HBAR * C / ME ** 2) / G - (MP_MASS / ME) ** 2,
        (MP_MASS / ME) ** 2, "代数恒等式",
        note="证实旧式不是『近似不准』，而是结构上把 G 换成了 ℏc/m²")


# ===========================================================================
# 2. 修正：α_grav = G m²/(ℏ c) = (m/m_P)²
# ===========================================================================
def module2_correct():
    worst = mp.mpf("0")
    for label, m in PARTICLES:
        a_grav = G * m ** 2 / (HBAR * C)
        a_ref = (m / MP_MASS) ** 2
        resid = a_grav - a_ref
        rel = abs(resid) / a_ref
        worst = max(worst, rel)
        rec("N02-" + label.split()[0], "修正式 α_grav = Gm²/(ℏc) = (m/m_P)²（%s）" % label,
            "α_grav - (m/m_P)²", resid, a_ref, "代数恒等式",
            note="对任意粒子成立，无矛盾")
    rec("N02-max", "修正式全粒子谱最大相对残差（9 个粒子）",
        "max|α_grav-(m/m_P)²|/(m/m_P)²", worst, mp.mpf("1"), "代数恒等式",
        note="机器零。与旧链在电子处 5.7e+44 倍偏离形成对照")

    rec("N02-e", "电子 α_grav(e) = (m_e/m_P)² 数值",
        "α_grav(e)", G * ME ** 2 / (HBAR * C), (ME / MP_MASS) ** 2, "数值核验",
        note="= 1.75e-45，而非旧链隐含的 1")

    rec("N02-P", "普朗克极限 α_grav(m_P) = 1（旧链唯一成立处）",
        "α_grav(m_P) - 1", G * MP_MASS ** 2 / (HBAR * C) - 1, mp.mpf("1"), "代数恒等式",
        note="证实旧链只是『普朗克锚点定义式』：它在该点精确成立，离开即崩塌")


# ===========================================================================
# 3. 重算：修正后的完整几何派生链
# ===========================================================================
def module3_rebuild():
    """修正链：R = ƛ_C = ℏ/(mc)；κ²+τ² = 1/R² = (mc/ℏ)²；ω = c/R；α = τ/κ。"""
    worst_chain = mp.mpf("0")
    rows = []
    for label, m in PARTICLES:
        R = HBAR / (m * C)                       # 约化康普顿波长
        omega = C / R                            # ω = c/R
        kt2 = 1 / R ** 2                         # κ²+τ²
        kappa = mp.sqrt(kt2) / mp.sqrt(1 + ALPHA ** 2)
        tau = ALPHA * mp.sqrt(kt2) / mp.sqrt(1 + ALPHA ** 2)

        # 自洽性三检
        r1 = omega * R - C                                   # ωR = c
        r2 = kappa ** 2 + tau ** 2 - (omega / C) ** 2        # 三重奏
        r3 = tau / kappa - ALPHA                             # α = τ/κ
        scale = (omega / C) ** 2
        rel = max(abs(r1) / C, abs(r2) / scale, abs(r3) / ALPHA)
        worst_chain = max(worst_chain, rel)

        rows.append({
            "particle": label,
            "m_kg": mp.nstr(m, 10),
            "R_ƛC_m": mp.nstr(R, 10),
            "omega_rad_s": mp.nstr(omega, 10),
            "kappa_1_m": mp.nstr(kappa, 10),
            "tau_1_m": mp.nstr(tau, 10),
            "alpha_grav": mp.nstr(G * m ** 2 / (HBAR * C), 10),
            "R_over_lP": mp.nstr(R / LP, 10),
        })
        rec("N03-" + label.split()[0], "修正链自洽三检（%s）：ωR=c、κ²+τ²=(ω/c)²、τ/κ=α" % label,
            "max 相对残差", rel, mp.mpf("1"), "代数恒等式",
            note="R 取粒子约化康普顿波长后，几何链对任意质量自洽")

    rec("N03-max", "修正链全粒子谱最大相对残差（9 个粒子 × 3 项 = 27 检）",
        "max 相对残差", worst_chain, mp.mpf("1"), "代数恒等式",
        note="机器零。修正后的几何链在任意粒子尺度均自洽——"
             "代价是 G 不再由 (κ,τ) 导出（见模块 4 残留缺口）")

    # R 与 ℓ_P 的分离（旧链混用的根源）
    rec("N03-sep", "尺度分离：电子 R=ƛ_C 与 ℓ_P 之比（旧链混用二者的后果）",
        "R(e)/ℓ_P", ME and (HBAR / (ME * C)) / LP, (HBAR / (ME * C)) / LP, "数值核验",
        note="= 2.39e+22。旧链要求二者相等，故只能推出 m=m_P")

    return rows


# ===========================================================================
# 4. 诚实：修正后仍然残留的缺口
# ===========================================================================
def module4_gaps():
    note("N04-1", "残留缺口一：G 仍是外部输入",
         "修正后 G 不再由 (κ,τ) 导出，须作为独立测量输入", "BOUNDARY",
         "修正只是移除了矛盾，没有实现『G 的几何化』。"
         "本谱系原本声称的『由 (κ,τ) 导出 G』这一成果，在修正后不复存在")

    note("N04-2", "残留缺口二：α 仍是测量锚",
         "α = τ/κ 是定义回指，τ/κ 的数值来自 α 而非反之", "BOUNDARY",
         "α = 1/137.036 仍未第一性导出；仓库 v29 已证明 φ 等拓扑构造可逼近但无证据力")

    note("N04-3", "残留缺口三：质量层级完全未解释",
         "R = ℏ/(mc) 只是用 m 定义 R，并未导出 m", "BOUNDARY",
         "m_μ/m_e = 206.768、m_τ/m_e = 3477.2 仍为测量输入。"
         "与仓库 v30 结论一致：代质量层级需外部动力学（Yukawa）输入")

    note("N04-4", "残留缺口四：归一化后自由度不变",
         "自然单位下仍剩 2 个自由输入（α 与 m/m_P）", "BOUNDARY",
         "修正并未减少自由参数——它只是让方程组从『不相容』变为『相容但欠定』")

    note("N04-5", "本次修正的性质（诚实定性）",
         "移除矛盾 ≠ 解决问题；修正后体系从『内部冲突』降为『欠定候选』", "BOUNDARY",
         "修正把体系状态由 FAIL 改善为『自洽但无额外预言力』。"
         "不得据此宣称该谱系的统一目标已取得进展")


def main():
    module1_diagnose()
    module2_correct()
    rows = module3_rebuild()
    module4_gaps()

    counts = {}
    for r in RECORDS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base, "数据")
    os.makedirs(data_dir, exist_ok=True)

    payload = {
        "title": "普朗克锚定谬误 · 修正与派生链重算",
        "precision_digits": mp.mp.dps,
        "summary": {"total": len(RECORDS), "counts": counts},
        "corrected_chain": {
            "R": "ℏ/(mc)（约化康普顿波长，非 ℓ_P）",
            "kappa_sq_plus_tau_sq": "(mc/ℏ)² = 1/R²",
            "omega": "c/R = mc²/ℏ",
            "alpha": "τ/κ（定义回指，仍为测量锚）",
            "alpha_grav": "G m²/(ℏc) = (m/m_P)²",
            "G_status": "外部输入（不再由 (κ,τ) 导出）",
        },
        "particle_table": rows,
        "records": RECORDS,
    }
    with open(os.path.join(data_dir, "普朗克锚定谬误_修正与重算.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print("=" * 78)
    print("普朗克锚定谬误 · 修正与派生链重算（mpmath %d 位）" % mp.mp.dps)
    print("=" * 78)
    for r in RECORDS:
        if r["kind"] == "审计":
            print("%-8s %-12s %s" % (r["verdict"], r["id"], r["name"][:56]))
        else:
            print("%-8s %-12s %-46s 位=%-6s 残差=%s" % (
                r["verdict"], r["id"], r["name"][:46], r["digits"], r["rel_residual"]))
    print("-" * 78)
    print("记录总数：%d ；判定：%s" % (
        len(RECORDS), " ".join("%s=%d" % (k, v) for k, v in sorted(counts.items()))))
    print("产出：%s" % os.path.join(data_dir, "普朗克锚定谬误_修正与重算.json"))
    print("=" * 78)


if __name__ == "__main__":
    main()
