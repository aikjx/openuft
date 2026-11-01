# -*- coding: utf-8 -*-
"""
TUFT-r361 · 临界面维数定理与阈值计数 —— 攻 A1（全系统固定点的自由度下界）
守卫式机算，退出码 0 = 全过。产物：数据/TUFT-r361_*.json + _report.txt
"""
import io
import json
import os
import sys

import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAME = "TUFT-r361_临界面维数与阈值计数_攻A1_全系统固定点自由度下界_2026-11-02"
sys.path.insert(0, HERE)
from _audit_acceptance import NumberReserver, discriminate  # noqa: E402

LOG = []
ENTRIES = []
GUARDS = []


def log(s=""):
    LOG.append(s)
    print(s)


def entry(eid, layer, verdict, detail, kv=None):
    ENTRIES.append({"id": eid, "layer": layer, "verdict": verdict,
                    "detail": detail, "kv": kv or {}})
    log("  [%s] %-4s %s" % (verdict, eid, detail))


def guard(gid, ok, detail):
    GUARDS.append({"id": gid, "pass": bool(ok), "detail": detail})
    log("  [%s] %-40s %s" % ("PASS" if ok else "FAIL", gid, detail))


# 撞号防御（排除自身三件产物）
res = NumberReserver(ROOT)
self_files = {NAME + ".py", NAME + ".json", "判定_" + NAME + ".md", "_out_r361.txt"}
free, hits = res.is_free(361, self_files=self_files)
log("r361 占号扫描: %s %s" % ("FREE" if free else "TAKEN", hits if not free else ""))

# ---------------------------------------------------------------------------
log("=" * 78)
log("§0 临界面维数定理（符号层）")
log("=" * 78)
# 严格命题：δ(t)=Σ C_i e^{λ_i t}v_i；t→+∞ 时 δ→0 ⟺ 所有 λ_i>0 的系数为 0
# ⇒ 严格 UV 临界流形 = span{v_i: λ_i<0}，dim=#{λ_i<0}
# 边缘方向（λ=0）：δ 恒定，不衰减也不吹飞 ⇒ 不在严格流形上，但幅度仍自由
# ⇒ 可自由选择的连续幅度下界 = #{λ_i≤0}
log("  命题 1（严格）：dim S_UV = #{λ_i<0}")
log("  命题 2（可操作）：|P_cont| ≥ #{λ_i≤0} + |P_UV^other|")
log("  证明：δ(t)=Σ C_i e^{λ_i t}v_i；t=lnμ→+∞ 时 e^{λ_i t}→0 仅当 λ_i<0；")
log("        λ_i=0 给常数幅度（如高斯固定点的 1/α 平移），不衰减 ⇒ 仍是自由输入。")

# 2x2 机检：B=[[0.1,0.6],[0.6,0.1]]，谱 0.7 / -0.5
J2 = sp.Matrix([[sp.Rational(1, 10), sp.Rational(6, 10)],
                [sp.Rational(6, 10), sp.Rational(1, 10)]])
w = J2.eigenvals()
wv = sorted([float(k) for k in w])
log("  机检矩阵谱: %s ⇒ #(λ<0)=1, #(λ=0)=0, #(λ≤0)=1" % ["%.2f" % x for x in wv])


def flow(J, g0, t0, t1):
    """解析解：δ(t)=expm(J t)·δ0（sympy 精确 expm）"""
    return (sp.exp(J * (t1 - t0)) * sp.Matrix(g0)).evalf(30)


neg_vec = [sp.Matrix(v[2][0]) for v in J2.eigenvects() if float(v[0].evalf()) < 0][0]
pos_vec = [sp.Matrix(v[2][0]) for v in J2.eigenvects() if float(v[0].evalf()) > 0][0]
tests = [("v_neg", neg_vec, True), ("v_pos", pos_vec, False),
         ("mix", neg_vec + pos_vec, False)]
ok_pattern = True
for tag, v0, expect_decay in tests:
    d = flow(J2, list(v0), 0, 40)
    norm = float(sp.sqrt((d.T * d)[0, 0]))
    log("    δ0=%-6s ⇒ |δ(t=40)|=%.3e （预期%s）" % (tag, norm, "→0" if expect_decay else "发散"))
    ok_pattern &= (norm < 1e-6) == expect_decay
guard("UV_SURFACE_DIM_EQ_NEG_EIG", ok_pattern,
      "严格流形 = span{v_neg}，dim=1=#{λ<0}；混合方向发散（判据非恒真）")

# 边缘方向：3x3 谱 (-0.5, 0, +0.7)，从纯边缘方向出发 ⇒ |δ| 恒定
J3 = sp.diag(sp.Rational(-1, 2), sp.Integer(0), sp.Rational(7, 10))
d_marg = (sp.exp(J3 * 40) * sp.Matrix([0, 1, 0])).evalf(30)
nm = float(sp.sqrt((d_marg.T * d_marg)[0, 0]))
guard("MARGINAL_IS_FREE_NOT_DECAY", abs(nm - 1.0) < 1e-20,
      "λ=0 时 |δ(t=40)|=%.15f（不衰减 ⇒ 边缘幅度是自由输入，不进严格流形）" % nm)

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§1 高斯固定点：SM 规范扇区全谱 λ=0，自由幅度 = 尺度平移")
log("=" * 78)
mp.mp.dps = 50
b = {1: mp.mpf(41) / 10, 2: mp.mpf(-19) / 6, 3: mp.mpf(-7)}
g1, g2, g3 = sp.symbols("g1 g2 g3", real=True)
bg = [b[1] * g1 ** 2 / (2 * sp.pi), b[2] * g2 ** 2 / (2 * sp.pi), b[3] * g3 ** 2 / (2 * sp.pi)]
Jg = sp.Matrix([[sp.diff(bg[i], v) for v in (g1, g2, g3)] for i in range(3)])
Jg0 = Jg.subs({g1: 0, g2: 0, g3: 0})
log("  β_i=(b_i/2π)α_i²，b=(41/10,-19/6,-7)  [SM 一圈]")
log("  J(0) = %s ⇒ 三个特征值全为 0（完全退化边缘）" % Jg0.tolist())
guard("GAUSSIAN_JACOBIAN_ZERO_EXACT", Jg0 == sp.zeros(3, 3), "符号：J(0)=0 矩阵，精确")
sols = sp.solve([sp.Eq(x, 0) for x in bg], [g1, g2, g3], dict=True)
log("  solve(β=0) = %s ⇒ 唯一固定点 α_i=0，无非平凡孤立固定点" % sols)
guard("SM_GAUGE_FP_UNIQUE_ZERO",
      len(sols) == 1 and all(abs(float(sols[0].get(v, 99))) < 1e-30 for v in (g1, g2, g3)),
      "SM 规范扇区只有高斯固定点（此即渐近自由的另一端）")
guard("MARGINAL_COUNT_3", len(sols[0]) == 3, "三个耦合各带 1 个边缘方向 ⇒ #(λ≤0)=3")

# 尺度平移不变性（证明"1 个自由幅度 = Λ"）
k = b[3] / (2 * mp.pi)
a0, a0p = mp.mpf("0.10"), mp.mpf("0.12")
dt = (1 / a0p - 1 / a0) / k
maxdiff = mp.mpf(0)
for tt in [-80, -40, -20, -5, 0]:
    aa = 1 / (1 / a0p - k * mp.mpf(tt))          # 初值 a0p 的轨道
    ab = 1 / (1 / a0 - k * (mp.mpf(tt) - dt))    # 初值 a0 的轨道平移 Δt
    maxdiff = max(maxdiff, abs(aa - ab) / aa)
log("  Δt=2π/b(1/α0'−1/α0)=%.6f；两轨道平移后最大相对差=%.2e" % (float(dt), float(maxdiff)))
guard("SCALE_TRANSLATION_INVARIANCE", maxdiff < mp.mpf("1e-40"),
      "二次 β 的解对 t 平移严格不变 ⇒ 只有 1 个自由幅度（=Λ），无形状自由度")
entry("B1", "临界维数", "INFO",
      "SM 规范扇区高斯固定点：J=0、三个 λ=0 ⇒ #(λ≤0)=3 ⇒ |P_cont|≥3（三个 Λ 等价幅度）",
      {"neg": 0, "zero": 3, "pos": 0})

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§2 阈值计数：每个阈值 = 1 个连续输入（机器定价）")
log("=" * 78)
b_lo = mp.mpf(41) / 10
b_hi = b_lo + mp.mpf(4) / 3          # 加一族费米子 ⇒ Δb1=4/3
mZ = mp.mpf("91.1876")
mIR = mp.mpf("0.00051099895")        # m_e (GeV)
sigma_ainv = mp.mpf("0.000000021")   # CODATA 2022 σ(α⁻¹)=2.1e-8


def ainv0(mth, bl=b_lo, bh=b_hi):
    return (mp.mpf(1) / mp.mpf("127.955")) + (bh / (2 * mp.pi)) * mp.log(mZ / mth) \
        + (bl / (2 * mp.pi)) * mp.log(mth / mIR)


m1, m2 = mp.mpf("1000"), mp.mpf("10000")
shift = ainv0(m2) - ainv0(m1)
formula = -((b_hi - b_lo) / (2 * mp.pi)) * mp.log(m2 / m1)   # 阈值抬高 ⇒ 1/α(0) 降低
log("  阈值 1 TeV→10 TeV（Δb1=4/3）：Δα⁻¹(0)=%.10f（解析式 %.10f，差 %.2e）"
    % (float(shift), float(formula), float(abs(shift - formula))))
guard("THRESHOLD_SHIFT_MATCH_FORMULA", abs(shift - formula) < mp.mpf("1e-25"),
      "分段积分与闭式 Δα⁻¹=−(Δb/2π)ln(M2/M1) 逐位一致")
nsig = abs(shift) / sigma_ainv
log("  该单一阈值位移 = %.3f = CODATA σ 的 %.3e 倍" % (float(shift), float(nsig)))
guard("THRESHOLD_SHIFT_SUPER_SIGMA", nsig > mp.mpf("1e6"),
      "1 个阈值的连续移动即超 %.1e σ ⇒ 阈值必须是输入" % float(nsig))
entry("C1", "阈值计数", "FAIL",
      "Δα⁻¹(0)=−0.4886（1→10 TeV），= %.2e σ；每个阈值贡献 +1 到 |P_cont|" % float(nsig),
      {"dalpha_inv": float(shift), "n_sigma": float(nsig)})

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§3 控制组：dim=0（全 λ>0）才能预言——闸门非恒否")
log("=" * 78)
# β_a = +A(a−a*) ⇒ λ=+A>0 ⇒ IR 吸引 ⇒ 多初值收敛到 a*
A, astar = mp.mpf("0.5"), mp.mpf("0.04")


def rk4_scalar(fn, x0, t0, t1, h):
    x, tt = x0, t0
    for _ in range(int(abs((t1 - t0) / h))):
        k1 = fn(tt, x)
        k2 = fn(tt + h / 2, x + h * k1 / 2)
        k3 = fn(tt + h / 2, x + h * k2 / 2)
        k4 = fn(tt + h, x + h * k3)
        x += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        tt += h
    return x


res_ids = []
for x0 in (0.01, 0.03, 0.06, 0.09):
    xT = rk4_scalar(lambda tt, xx: A * (xx - astar), mp.mpf(str(x0)), 0, -60, -0.01)
    res_ids.append(float(abs(xT - astar) / astar))
log("  4 个初值经 IR 60 个 e 折后与 a* 最大相对差 = %.2e" % max(res_ids))
guard("DIM0_MODEL_GIVES_PREDICTION", max(res_ids) < 1e-6,
      "λ>0（IR 吸引）⇒ 低能值被钉在 a* ⇒ dim=0 的预言确实可能（判据有牙）")

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§4 权威门禁 + 结论")
log("=" * 78)
cand = 1.0 / 137.035999177
sig = cand * 1.532e-10
g_route = discriminate("A1_FULL_FP_SYSTEM", candidate=cand, center=cand, sigma=sig,
                       n_matched=1, n_free=3, is_fit_to_target=True,
                       predicts_target_quantity=True)
log("  A1 路线（3 个规范边缘幅度）: surplus=%.2f verdict=%s"
    % (g_route["surplus"], g_route["verdict"]))
guard("GATE_A1_RELATION_OR_FIT", g_route["verdict"] == "RELATION_OR_FIT",
      "n_free=3 ⇒ surplus=%.1f<1" % g_route["surplus"])
g_pos = discriminate("POSCTRL_GR", candidate=42.981, center=42.98, sigma=0.02,
                     n_matched=1, n_free=0, is_fit_to_target=False,
                     predicts_target_quantity=True)
guard("GATE_POSCTRL_DISCOVERY", g_pos["is_discovery_of_target"],
      "正对照 GR ⇒ %s（门禁非恒否）" % g_pos["verdict"])

entry("A1", "维数总账", "FAIL",
      "SM 规范扇区 #(λ≤0)=3，加阈值 ⇒ |P_cont|≥4；全系统 dim=0 需非平凡 UV 固定点且全 λ>0（未立）",
      {"dim_strict": 0, "free_marginal": 3})
guard("RESERVE_R361_FREE", free, "落盘前 r361 空闲")

npass = sum(1 for g in GUARDS if g["pass"])
log("")
log("=" * 78)
log("守卫 %d/%d 通过；判词 A1_BOUNDED_BELOW__CRITICAL_SURFACE_DIM_GE_1" % (npass, len(GUARDS)))
log("=" * 78)
for g in GUARDS:
    if not g["pass"]:
        log("FAIL: %s %s" % (g["id"], g["detail"]))

# ---------------------------------------------------------------------------
data = {
    "round": "r361",
    "title": NAME,
    "date": "2026-11-02",
    "verdict": "A1_BOUNDED_BELOW__CRITICAL_SURFACE_DIM_GE_1",
    "exit_code": 0 if npass == len(GUARDS) else 1,
    "entries": ENTRIES,
    "guards": GUARDS,
    "guard_pass": npass,
    "guard_total": len(GUARDS),
    "constants": {"b_sm": [4.1, -19.0 / 6, -7.0], "b_hi_plus_gen": float(b_hi),
                  "sigma_alpha_inv": float(sigma_ainv)},
    "relations": {"dim_strict": "#{lambda<0}",
                  "free_floor": "#{lambda<=0} + |P_uv_other|",
                  "threshold_shift": "(db/2pi) ln(M2/M1)"},
}
dp = os.path.join(ROOT, "数据", NAME + ".json")
with io.open(dp, "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2)
lp = os.path.join(HERE, "_out_r361.txt")
with io.open(lp, "w", encoding="utf-8") as fh:
    fh.write("\n".join(LOG) + "\n")
print("\n产物: %s\n      %s" % (dp, lp))
sys.exit(data["exit_code"])
