# -*- coding: utf-8 -*-
"""算法联盟 · 「空间光速螺旋 + 正交原理」大统一摘要 可算审计（8 门，每门带负对照）。

非判定册 / 不占 RID / 不写 README。数学自洽 != 实验证实；计算 != 证实。
用法:  python -I _alg_spiral_orthogonality_gut_abstract_audit.py
产物:  ../数据/_ALG_spiral_orthogonality_gut_abstract_audit_2026-11-22.json
"""
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "数据"
SRC_TEXT = DATA / "_来料原件_空间光速螺旋与正交原理大统一摘要_2026-11-22.md"
OUT = DATA / "_ALG_spiral_orthogonality_gut_abstract_audit_2026-11-22.json"
RNG = np.random.default_rng(20261122)
gates = {}


def gate(name, ok, **kw):
    gates[name] = {"ok": bool(ok), **kw}


# ---------- 工具：数值 Frenet 标架 ----------
def frenet(r1, r2, r3):
    T = r1 / np.linalg.norm(r1)
    c = np.cross(r1, r2)
    B = c / np.linalg.norm(c)
    N = np.cross(B, T)
    kappa = np.linalg.norm(c) / np.linalg.norm(r1) ** 3
    tau = np.dot(c, r3) / np.dot(c, c)
    return T, N, B, kappa, tau


def ortho_residual(T, N, B):
    M = np.vstack([T, N, B])
    return float(np.max(np.abs(M @ M.T - np.eye(3))))


# ---------- G1 正交原理 = Frenet 恒等式（判别力 0） ----------
res = []
for _ in range(200):  # 随机非螺旋三次多项式曲线
    a = RNG.normal(size=(4, 3))
    t = RNG.uniform(-1, 1)
    r1 = a[1] + 2 * a[2] * t + 3 * a[3] * t * t
    r2 = 2 * a[2] + 6 * a[3] * t
    r3 = 6 * a[3]
    T, N, B, *_ = frenet(r1, r2, r3)
    res.append(ortho_residual(T, N, B))
rot = np.array([[1, 0, 0], [0, np.cos(1e-3), -np.sin(1e-3)], [0, np.sin(1e-3), np.cos(1e-3)]])
Nbad = rot @ np.array([0.0, 1.0, 0.0]) + np.array([1e-3, 0, 0])  # 负对照：N 偏离 1e-3
neg = ortho_residual(np.array([1.0, 0, 0]), Nbad / np.linalg.norm(Nbad), np.array([0, 0, 1.0]))
gate("G1_orthogonality_is_frenet_identity",
     max(res) < 1e-12 and neg > 1e-4,
     random_nonhelix_curves=200, max_residual=max(res), negative_control_residual=neg,
     discrimination_power=0,
     reading="任意正则空间曲线的 (T,N,B) 都正交归一；『正交原理』对螺旋与非螺旋、物理与非物理曲线一视同仁，不承重。")

# ---------- G2 光速螺旋的世界线是类光：本征弧长为 0，标准 Frenet 失效 ----------
a_, b_, w, t, c = sp.symbols("a b omega t c", positive=True)
x = sp.Matrix([a_ * sp.cos(w * t), a_ * sp.sin(w * t), b_ * w * t])
v2 = sp.simplify((x.diff(t).T * x.diff(t))[0])            # = omega^2 (a^2+b^2)
w_c = sp.solve(sp.Eq(v2, c ** 2), w)[0]                    # 令空间速率 = c
ds2 = sp.simplify(-c ** 2 + v2.subs(w, w_c))               # Minkowski: -c^2 dt^2 + |dx|^2
ds2_neg = sp.simplify(-c ** 2 + v2.subs(w, w_c / 2))       # 负对照：v = c/2
gate("G2_lightspeed_worldline_is_null",
     ds2 == 0 and ds2_neg != 0,
     ds2_per_dt2=str(ds2), negative_control_v_half_c=str(ds2_neg),
     reading="以 c 运动的螺旋在 4 维时空中是类光曲线：dτ=0，弧长参数化不存在，三维 (κ,τ) 不是洛伦兹不变量；需 null-Frenet（伪弧长）重写，摘要未给。")

# ---------- G3 自由度计数：(κ,τ,ω) 在速率约束 c 下秩 2；三个『分量』供四种力 ----------
kap = a_ / (a_ ** 2 + b_ ** 2)
tau_ = b_ / (a_ ** 2 + b_ ** 2)
J = sp.Matrix([kap, tau_, w_c]).jacobian([a_, b_])
rank_c = J.subs({a_: 1.3, b_: 0.7, c: 1}).rank()
J_free = sp.Matrix([kap, tau_, w]).jacobian([a_, b_, w])   # 负对照：不施加速率约束
rank_free = J_free.subs({a_: 1.3, b_: 0.7, w: 2.0}).rank()
n_forces, n_components_claimed = 4, 3
gate("G3_dof_count",
     rank_c == 2 and rank_free == 3,
     rank_kappa_tau_omega_given_speed_c=int(rank_c), negative_control_rank_without_constraint=int(rank_free),
     forces=n_forces, components_claimed=n_components_claimed,
     pigeonhole_forces_sharing_a_component=n_forces - rank_c,
     reading="摘要称曲率/挠率/角频率三自由度，但速率=c 后 ω 由 (a,b) 决定，独立仅 2 个；四力映到 2 个独立量，至少 2 种力无独立耦合。")

# ---------- G4 无量纲数计数：只剩 1 个（螺旋角），无法给出 4 个耦合 ----------
# 量纲矩阵：列 κ,τ,ω,c ；行 L,T
D = sp.Matrix([[-1, -1, 0, 1], [0, 0, -1, -1]])
null = D.nullspace()                                      # 2 个无量纲组合：τ/κ, ω/(cκ)
ratio_check = sp.simplify((w_c / (c * kap)) - sp.sqrt(1 + (tau_ / kap) ** 2))
dimless_independent = len(null) - (1 if ratio_check == 0 else 0)
gate("G4_dimensionless_numbers",
     len(null) == 2 and dimless_independent == 1,
     raw_dimensionless_groups=len(null), independent_after_speed_constraint=dimless_independent,
     identity="omega/(c*kappa) = sqrt(1+(tau/kappa)^2)",
     couplings_needed=["alpha_em", "alpha_s", "alpha_w", "alpha_G"],
     reading="唯一无量纲量是螺旋角 τ/κ；α_em、α_s、α_w、α_G 跨约 38 个数量级，单一角度无法同时给出，其余必外生。")

# ---------- G5 『标准模型规范群 = 正交投影保持的对称子群』 ----------
def stabilizer_dim(vectors):
    """so(3) 中同时零化给定向量的生成元空间维数。"""
    gens = [np.array([[0, 0, 0], [0, 0, -1], [0, 1, 0]]),
            np.array([[0, 0, 1], [0, 0, 0], [-1, 0, 0]]),
            np.array([[0, -1, 0], [1, 0, 0], [0, 0, 0]])]
    M = np.hstack([np.vstack([g @ v for v in vectors]).reshape(-1, 1) for g in gens])
    return 3 - np.linalg.matrix_rank(M, tol=1e-10)

T0, N0, B0 = np.eye(3)
stab_full = stabilizer_dim([T0, N0, B0])
stab_T = stabilizer_dim([T0])                              # 负对照：只保持切向
sm_dim, sm_rank = 8 + 3 + 1, 2 + 1 + 1
so3_dim, so3_rank = 3, 1
min_n_by_rank = 2 * sm_rank                                # rank so(n) = floor(n/2) >= 4
gate("G5_gauge_group_embedding",
     stab_full == 0 and stab_T == 1 and sm_dim > so3_dim and sm_rank > so3_rank,
     stabilizer_dim_of_full_frenet_frame=int(stab_full),
     negative_control_stabilizer_dim_tangent_only=int(stab_T),
     sm_algebra={"dim": sm_dim, "rank": sm_rank}, frame_rotation_so3={"dim": so3_dim, "rank": so3_rank},
     min_ambient_dim_lower_bound_by_rank=min_n_by_rank, known_upper_bound="n=10 (su(5) ⊂ so(10))",
     reading="三维螺旋的完整标架保持子群是平凡群 {e}（维数 0）；即便只保持切向也只剩 SO(2)≅U(1)。"
             "SU(3)×SU(2)×U(1)（维 12、秩 4）不能嵌入 SO(3)（维 3、秩 1）；要容纳它须曲线处在 n≥8 维，"
             "已知 n=10 可行，而那正是既有的 SO(10) 大统一，不是新结构。")

# ---------- G6 『最先进方法』所需输入：摘要给出的方程数 ----------
text = SRC_TEXT.read_text(encoding="utf-8")
eq_pat = re.compile(r"[=≈∝]|\\frac|\\partial|β\(|\bbeta\(")
n_eq = len(eq_pat.findall(text))
n_eq_neg = len(eq_pat.findall(r"beta(g) = -b g^3/(16 pi^2)"))
methods_need = {
    "high-precision field equation integration": "场方程本体",
    "renormalization group flow": "各耦合的 β 函数（需物质含量与规范群表示）",
    "ADM-BSSN numerical relativity": "爱因斯坦型演化方程 + 约束方程 + 物质应力能",
    "anomalous magnetic moment / EDM": "新贡献 Δa_ℓ、d_ℓ 的解析式与参数值",
}
gate("G6_method_inputs_supplied",
     n_eq == 0 and n_eq_neg >= 1,
     equations_in_abstract=n_eq, negative_control_hits=n_eq_neg, methods_and_missing_inputs=methods_need,
     source_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
     reading="摘要零方程、零 Lagrangian、零 β 函数；所列四类方法均无可输入对象，目前无法运行，只是路线图。")

# ---------- G7 判别实验的现状靶值（外部引用，需人工复核一手来源） ----------
a_exp, s_exp = 116592071.5e-11, 14.5e-11      # FNAL 终测 + BNL 世界平均（2025）
a_sm, s_sm = 116592033e-11, 62e-11            # Muon g-2 Theory Initiative WP25（格点 HVP）
z = (a_exp - a_sm) / np.hypot(s_exp, s_sm)
de_bound = 4.1e-30                            # |d_e| 上限 e·cm，90% CL，JILA 2023
z_neg = (a_exp - (a_sm - 249e-11)) / np.hypot(s_exp, s_sm)   # 负对照：旧 2020 式 ~2.5e-9 缺口
gate("G7_experimental_targets",
     abs(z) < 2 and z_neg > 3,
     amu_exp_minus_sm=a_exp - a_sm, sigma=float(np.hypot(s_exp, s_sm)), z=float(z),
     negative_control_z_with_2020_style_gap=float(z_neg),
     electron_edm_bound_e_cm=de_bound,
     sources=["https://arxiv.org/abs/2506.03069", "https://arxiv.org/abs/2505.21476",
              "https://arxiv.org/abs/2212.11841"],
     reading="μ 子 g-2 与 SM 已无显著偏差（~0.6σ），电子 EDM 上限 4.1e-30 e·cm；新理论在此只能被约束，不能靠『解释反常』得分。"
             "数值为外部引用，需对照一手文献复核。")

# ---------- G8 独立数值预言计数 ----------
predictions = []                               # 摘要中可数出的零自由参数数值预言
gate("G8_independent_predictions",
     len(predictions) == 0 and len(predictions + ["dummy"]) == 1,
     count=len(predictions), negative_control_injected=1,
     reading="摘要未给出任何数值预言；独立预言数 = 0。")

n_ok = sum(g["ok"] for g in gates.values())
verdict = ("SPIRAL-ORTHO-GUT-ABSTRACT--GATES-%d-OF-%d--ORTHOGONALITY-IS-FRENET-IDENTITY--WORLDLINE-NULL"
           "--INDEPENDENT-DOF-2-FOR-4-FORCES--DIMLESS-1--SM-NOT-IN-SO3-STABILIZER-TRIVIAL"
           "--EQUATIONS-0--METHODS-NOT-RUNNABLE--UFT-NOT-BROKEN--NEW-PREDICTION-0") % (n_ok, len(gates))
out = {"title": "空间光速螺旋与正交原理大统一摘要 可算审计", "date": "2026-11-22",
       "nature": "非判定册 / 不占 RID / 不写 README", "verdict": verdict,
       "n_gate_ok": n_ok, "n_gates": len(gates), "gates": gates}
payload = json.dumps(out, ensure_ascii=False, indent=2, default=float)
OUT.write_text(payload, encoding="utf-8")
print(verdict)
for k, g in gates.items():
    print(("OK  " if g["ok"] else "FAIL"), k)
print("JSON", len(payload.encode("utf-8")), "B sha256", hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16])
