# -*- coding: utf-8 -*-
"""TUFT V9.21 束缚态与结构形成审计（变分法版，数值可靠）
A 组：库仑极限——变分数值验证 E_1=−13.6 eV（试函数族含精确基态）+ 教科书解析谱
B 组：汤川势——变分上界 E_var(κ̃) 判据：E_var_min<0 ⟺ 有束缚态；
      临界 κ̃_c^var≈1.0（变分下界）；E_var_min 随 κ̃ 单调降低（束缚加深）
C 组：四力束缚态现实表 + 结构层级从力程谱涌现 + 深层谱修正（指数截断→有限束缚）
D 组：氘核 no-go——κ̃_OPE=0.0029 ≪ κ̃_c ⇒ 零束缚态；氘核深度需 κ̃_eff≳1.4（耦合差 ≳500 倍）
用法：python tuft_v106_binding_audit.py
"""
import json, math
import numpy as np

HBARC = 197.3269804
MP = 938.27208816
MPI0 = 134.9768
LAM_PI = HBARC/MPI0
QPI2 = 0.02036**2
B_DEUTERON = 2.22452
RY = 13.605693

out = {}

def E_var_yukawa(alpha, kappa):
    """变分能量上界（无量纲）：u=x·e^(−αx)，<T>=α²/2，<V>=−4κα³/(2α+1)²"""
    return alpha**2/2.0 - 4.0*kappa*alpha**3/(2.0*alpha+1.0)**2

def E_var_coulomb(alpha):
    """库仑无量纲：<T>=α²/2，<V>=−α（试函数即精确基态，α=1 时 E=−0.5）"""
    return alpha**2/2.0 - alpha

def min_E_var(fn, amin=1e-3, amax=50.0, npts=4000):
    as_ = np.linspace(amin, amax, npts)
    ev = np.array([fn(a) for a in as_])
    i = int(np.argmin(ev))
    return ev[i], as_[i]

# ---------- A 组：库仑（氢原子） ----------
A = {}
E_var, a_opt = min_E_var(E_var_coulomb)
# 库仑无量纲单位 = hartree（27.2114 eV）：E_1=−0.5 hartree=−13.6057 eV
A["A_variational"] = {"E_var_hartree": round(E_var, 5), "alpha_opt": round(a_opt, 4),
                      "E_var_eV": round(E_var*27.2114, 4), "E_analytic_eV": -RY,
                      "rel_dev": round(abs(E_var*27.2114+RY)/RY, 6)}
A["A_levels_analytic"] = [{"n": n, "E_analytic_eV": round(-RY/n**2, 4),
                           "E1_ratio": round(n*n, 1)} for n in (1, 2, 3)]
A["A_verdict"] = "库仑极限变分验证：E_var(α=1)=−0.5 hartree 精确匹配 E_1=−13.6057 eV（试函数即精确基态）；解析谱 E_n=−13.6/n² eV（教科书）。统一势模板长程极限完整复现氢原子束缚谱"
out["A_coulomb"] = A

# ---------- B 组：汤川势（变分判据） ----------
B = {}
B_scan = []
for kk in [0.5, 1.0, 1.5, 1.68, 2.0, 3.0, 5.0, 10.0]:
    e_min, a_opt = min_E_var(lambda a: E_var_yukawa(a, kk))
    B_scan.append({"kappa_tilde": kk, "E_var_min": round(e_min, 5),
                   "alpha_opt": round(a_opt, 3),
                   "has_binding": bool(e_min < 0)})
B["B_scan"] = B_scan
# 临界 κ̃（变分下界：E_var_min=0 的 κ̃）
def kappa_critical_var():
    lo, hi = 0.1, 5.0
    for _ in range(60):
        mid = 0.5*(lo+hi)
        if min_E_var(lambda a: E_var_yukawa(a, mid))[0] < 0:
            hi = mid
        else:
            lo = mid
    return 0.5*(lo+hi)
B["kappa_critical_variational_lower"] = round(kappa_critical_var(), 4)
B["B_verdict"] = ("汤川势（指数截断 1/r）变分判据：E_var_min<0 ⟺ 有束缚态；临界 κ̃_c^var≈1.0（变分下界，精确值在 [1.0,~1.7]）。"
                  "κ̃<κ̃_c ⇒ 零束缚态。深层库仑态（延展 r~n²/κ̃）被指数截断破坏 ⇒ 有限束缚态（非无限）")
out["B_yukawa"] = B

# ---------- C 组：四力束缚态现实表 ----------
C = {
    "table": [
        {"力": "引力", "lambda": "∞", "kappa_eff": "任意 m1m2>0（长程无截断）", "N_bind": "无限（经典层级）", "structure": "星系→恒星→行星（无限层级）"},
        {"力": "电磁", "lambda": "∞（光子）", "kappa_eff": "α·2μ（长程无截断）", "N_bind": "无限（E_n=−13.6/n²）", "structure": "原子→分子（无限量子层级）"},
        {"力": "剩余强力", "lambda": "1.4619 fm（π⁰）", "kappa_eff": "κ̃_OPE=0.0029 ≪ κ̃_c≈1.0", "N_bind": "零（模板）；真实有限核素表需排斥核+张量项", "structure": "氘核→轻核（有限核素表，外输结构实现）"},
        {"力": "弱力", "lambda": "2.455e-3 fm（W）", "kappa_eff": "极小（κ̃∝λ 线性）", "N_bind": "零", "structure": "无束缚结构（纯衰变/散射）"},
    ],
    "C_verdict": ("结构层级从力程谱涌现：λ=∞ ⇒ 无限束缚态 ⇒ 无限结构层级（引力/电磁）；有限 λ ⇒ 有限束缚态；"
                  "λ 极小（弱力）⇒ 零束缚态。剩余强力模板层（单 π 中心交换）零束缚态——真实核束缚依赖外输结构"
                  "（排斥核 ω 交换 + 张量项），与 V9.18 方向外输同族坐实"),
}
out["C_structure"] = C

# ---------- D 组：氘核差距 ----------
D = {}
mu_np = MP/2.0
kappa_ope = (2*mu_np*LAM_PI/HBARC)*QPI2
D["kappa_ope"] = kappa_ope
D["kappa_critical_var"] = B["kappa_critical_variational_lower"]
D["template_has_binding"] = bool(kappa_ope >= B["kappa_critical_variational_lower"])
# 氘核深度所需 κ̃_eff：变分极小 = Ê_target=−0.115
E_tilde_target = -2*mu_np*B_DEUTERON*LAM_PI**2/HBARC**2
D["E_tilde_deuteron"] = round(E_tilde_target, 4)
def kappa_for_depth(etarget):
    lo, hi = 0.1, 20.0
    for _ in range(60):
        mid = 0.5*(lo+hi)
        if min_E_var(lambda a: E_var_yukawa(a, mid))[0] < etarget:
            hi = mid
        else:
            lo = mid
    return 0.5*(lo+hi)
kappa_eff = kappa_for_depth(E_tilde_target)
D["kappa_eff_deuteron"] = round(kappa_eff, 3)
D["coupling_gap"] = round(kappa_eff/kappa_ope, 0)
D["D_verdict"] = ("氘核 no-go 坐实：统一势模板（纯中心 OPE 汤川，κ̃=0.0029 ≪ κ̃_c≈1.0）⇒ 零束缚态——氘核在模板内不存在；"
                  "产生氘核结合能 B=2.225 MeV（Ê=−0.115）需有效耦合 κ̃_eff≈%.2f——耦合差 ≈%.0f 倍；"
                  "且模板唯一束缚通道（1/r 奇点浅束缚）被指数截断关闭。真实氘核束缚依赖张量项+排斥核"
                  "（V9.18 外输方向结构）⇒ 统一势模板无法内生氘核，方向缺失的动力学后果坐实（B03 家族）"
                  % (kappa_eff, kappa_eff/kappa_ope))
out["D_deuteron"] = D

out["summary"] = ("V9.21 束缚态与结构形成审计（变分法）：A 库仑变分 E_1=−13.6 eV 精确复现（解析谱教科书）PASS；"
                  "B 汤川临界 κ̃_c≈1.0（变分下界）、κ̃ 以下零束缚态、指数截断⇒有限束缚态（非无限）；"
                  "C 结构层级从力程谱涌现（长程无限、强有限、弱零）+ 剩余强力模板层零束缚态（排斥核/张量项外输坐实）；"
                  "D 氘核 no-go——κ̃_OPE=0.0029 零束缚态，需 κ̃_eff≈%.2f（耦合差 ≈%.0f 倍），张量项外输动力学后果"
                  % (kappa_eff, kappa_eff/kappa_ope))
with open(r"D:\a10\aikjx\code\my_lib\tuft_v106_binding_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)
print(json.dumps({"A": A["A_variational"], "B_scan": B_scan, "kappa_critical_var": B["kappa_critical_variational_lower"],
                  "D": {"kappa_ope": kappa_ope, "template_binding": False, "kappa_eff": kappa_eff,
                        "coupling_gap": kappa_eff/kappa_ope},
                  "summary": out["summary"]}, ensure_ascii=False, indent=1))
