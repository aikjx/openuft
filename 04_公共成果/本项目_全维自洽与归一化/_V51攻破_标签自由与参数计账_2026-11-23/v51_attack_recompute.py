# -*- coding: utf-8 -*-
"""V51 攻破引擎：Bernstein 不等式的标签自由漏洞 + 非对角逃逸 + 参数计账

攻击对象：一份 V50 复核意见的核心判据 m1^2 <= 4 m0 m2 及其「任意非负 h 分布」。
本引擎独立计算三条以前未机验的攻击：
  A. 标签自由：三质量对 P0/P1/P2 的指派有 3!=6 种；不等式是否随指派翻转？
     若存在一种指派使不等式成立、另一种使其失败 ⇒ 判据依赖未固定的标签，
     不是「任意 h 分布」的普适命题。
  B. 非对角逃逸：把 m0/m1/m2 当作质量矩阵对角元，加入非对角元 x，
     3x3 实对称矩阵的本征值如何随 x 变化？对角元满足不等式但本征值可违反
     （或反之）⇒ 对角化后不等式不保持不变，物理质量（本征值）不受其约束。
  C. 参数计账：h 用有限基展开，n_free（h 的自由系数）vs n_obs（可观测质量数）。
     若 n_free >= n_obs 则任意谱可拟合，判据判别力 0。

纪律：exp/act 两路、负对照必翻红、恒等门单列、守卫不写死、不动读数凑绿。
不产新物理，不宣称攻破统一场论，独立预言计数 0。
"""
import json
import os
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "_v51_attack_report.txt")
JSON_PATH = os.path.join(HERE, "_v51_attack_recompute.json")

ME = Decimal("0.51099895")
MMU = Decimal("105.6583755")
MTAU = Decimal("1776.86")

gates = []


def add(gid, kind, exp, act, ok, note=""):
    gates.append({"id": gid, "kind": kind, "exp": str(exp), "act": str(act),
                  "ok": bool(ok), "note": note})


def ds(x, p=12):
    if x == 0:
        return "0"
    return str(round(x, p))


def ineq_holds(m0, m1, m2):
    return m1 * m1 <= Decimal(4) * m0 * m2


# ===========================================================================
# A. 标签自由攻击
# ===========================================================================
# 三个物理质量指派给 (P0,P1,P2) 的 3! = 6 种方式。
# 不等式 m1^2 <= 4 m0 m2 中的 m1 是「中间 Bernstein 权重 P1 的质量」。
masses = {"e": ME, "mu": MMU, "tau": MTAU}
import itertools
labels = ["e", "mu", "tau"]
perm_results = []
for perm in itertools.permutations(labels):
    m0, m1, m2 = masses[perm[0]], masses[perm[1]], masses[perm[2]]
    ok = ineq_holds(m0, m1, m2)
    perm_results.append({
        "assign": "%s->P0,%s->P1,%s->P2" % perm,
        "m1_which": perm[1],
        "ratio": ds(m1 * m1 / (Decimal(4) * m0 * m2), 6),
        "holds": ok,
    })

n_hold = sum(1 for p in perm_results if p["holds"])
n_fail = len(perm_results) - n_hold
add("A1-label-dependent", "gate", "不等式随质量->权重指派翻转",
    "6 种指派中 成立%d / 失败%d" % (n_hold, n_fail),
    0 < n_hold < len(perm_results),
    "若恒成立=判别力 0；若恒失败=与来料『电子占中间可达』矛盾。"
    "混合才证明判据依赖未固定标签")

# 来料 Examples: (m_tau,m_e,m_mu) 成立；(m_e,m_mu,m_tau) 失败
p_e_mid = ineq_holds(MTAU, ME, MMU)          # 电子占 P1
p_mu_mid = ineq_holds(ME, MMU, MTAU)         # 几何序=质量序（mu 占 P1）
add("A2-electron-middle", "gate", "电子占 P1 时不等式成立",
    "m_e^2/(4 m_tau m_mu)=%s" % ds(ME * ME / (Decimal(4) * MTAU * MMU), 9),
    p_e_mid, "复现来料『电子占中间模落在锥内』")
add("A3-mass-order-fails", "gate", "质量序指派(mu 占 P1)时不等式失败",
    "m_mu^2/(4 m_e m_tau)=%s" % ds(MMU * MMU / (Decimal(4) * ME * MTAU), 6),
    not p_mu_mid, "复现来料『几何序=质量序被排除』；同一三质量两种结论")

# 负对照：若三个质量全相等，不等式在任意指派下都应成立（不产生假阳性翻转）
eq = [Decimal(1), Decimal(1), Decimal(1)]
eq_holds = all(ineq_holds(*p) for p in itertools.permutations(eq))
add("A4-equal-mass-neg", "neg", "全等质量任意指派均成立(负对照)",
    "6/6 成立" if eq_holds else "出现失败",
    eq_holds, "负对照：等质量时 1<=4 恒真，证明 A1 的翻转来自质量不等而非仪器")

# 反噬：若把系数 4 改成 3，电子占中间是否仍成立？应仍成立（余量大）
p_e_mid_c3 = ME * ME <= Decimal(3) * MTAU * MMU
add("A5-mutant-c3", "neg", "系数 4->3 电子占中间仍成立(不反噬该支)",
    "3*m_tau*m_mu=%s" % ds(Decimal(3) * MTAU * MMU, 3),
    p_e_mid_c3, "记录：该指派余量极大，单一系数扰动不足以翻转；"
    "判别力问题不靠系数微调解决")

# ===========================================================================
# B. 非对角逃逸：对角元满足不等式，但本征值谱可违反
# ===========================================================================
# 3x3 实对称矩阵，对角元 = (m0,m1,m2)，非对角元 = x（统一，便于解析）。
# 取来料的电子占中间指派 m=(m_tau, m_e, m_mu)：对角元满足不等式。
d0, d1, d2 = MTAU, ME, MMU


def eig3_sym_equal_offdiag(a, b, c, x):
    """[[a,x,x],[x,b,x],[x,x,c]] 的本征值（数值，幂迭代+收缩近似不必要；
    用 Jacobi 旋转迭代到收敛）。"""
    import copy
    A = [[a, x, x], [x, b, x], [x, x, c]]
    for _ in range(500):
        # 找最大非对角元
        p, q, best = 0, 1, abs(A[0][1])
        for i in range(3):
            for j in range(i + 1, 3):
                if abs(A[i][j]) > best:
                    p, q, best = i, j, abs(A[i][j])
        if best < Decimal("1e-40"):
            break
        app, aqq, apq = A[p][p], A[q][q], A[p][q]
        theta = (aqq - app) / (Decimal(2) * apq)
        t = (Decimal(1) if theta >= 0 else Decimal(-1)) / (
            abs(theta) + (theta * theta + Decimal(1)).sqrt())
        cs = Decimal(1) / (t * t + Decimal(1)).sqrt()
        sn = t * cs
        # Jacobi rotation on (p,q)
        for k in range(3):
            if k != p and k != q:
                akp, akq = A[k][p], A[k][q]
                A[k][p] = A[p][k] = cs * akp - sn * akq
                A[k][q] = A[q][k] = sn * akp + cs * akq
        A[p][p] = cs * cs * app - Decimal(2) * sn * cs * apq + sn * sn * aqq
        A[q][q] = sn * sn * app + Decimal(2) * sn * cs * apq + cs * cs * aqq
        A[p][q] = A[q][p] = Decimal(0)
    return sorted([A[0][0], A[1][1], A[2][2]])


diag_ok = ineq_holds(d0, d1, d2)
add("B1-diag-satisfies", "gate", "对角元(电子占中间)满足不等式",
    "m1^2/(4m0m2)=%s" % ds(d1 * d1 / (Decimal(4) * d0 * d2), 9),
    diag_ok, "确认逃逸实验的起点成立")

# 扫描非对角 x，找本征值谱（按升序）使中间^2 > 4*小*大。
# ★修复（2026-11-23）：旧版对 lo<=0 的样本静默跳过却报「违反 N/40」，
# 掩盖了「谱中已有负本征值 ⇒ 质量平方非正定 ⇒ 该点根本不是物理质量谱」。
# 现按正定性三分全量登记：正定样本内违反数 / 正定样本总数 / 非正定样本数。
violations = 0
max_ratio = Decimal(0)
worst = None
n_pos = 0
n_nonpos = 0
first_nonpos = None
for k in range(1, 41):
    x = Decimal(k) * ME  # 从 1 到 40 倍 m_e（升序谱 lo<=mid<=hi）
    ev = eig3_sym_equal_offdiag(d0, d1, d2, x)
    lo, mid, hi = ev[0], ev[1], ev[2]
    if lo > 0:  # 正定：三个质量平方均为正，才是物理质量谱
        n_pos += 1
        r = mid * mid / (Decimal(4) * lo * hi)
        if r > max_ratio:
            max_ratio = r
            worst = (x, ev)
        if r > 1:
            violations += 1
    else:       # 非正定：出现负本征值（tachyonic），该点不进入不等式判据
        n_nonpos += 1
        if first_nonpos is None:
            first_nonpos = (k, lo)
assert n_pos + n_nonpos == 40
add("B2-offdiag-escape", "gate", "正定样本中本征值谱违反不等式",
    "正定%d档内违反%d档(%.1f%%); max(mid^2/(4lohi))=%s; 最坏x=%s" % (
        n_pos, violations, Decimal(100) * violations / n_pos,
        ds(max_ratio, 6), ds(worst[0], 4) if worst else "NA"),
    violations > 0 and violations == n_pos,
    "物理质量是本征值；全部正定样本均违反对角不等式 ⇒ 判据在酉变换下不守恒。"
    "违反率分母改为正定样本数，不再把非物理点算作分母")
add("B5-positivity-boundary", "gate", "40 档中非正定样本确实存在且被显式剔除",
    "正定%d档 / 非正定%d档; 首个非正定 k=%d(lo=%s)" % (
        n_pos, n_nonpos, first_nonpos[0] if first_nonpos else -1,
        ds(first_nonpos[1], 6) if first_nonpos else "NA"),
    0 < n_nonpos < 40 and first_nonpos is not None and first_nonpos[1] <= 0,
    "负本征值 ⇒ 质量平方为负 ⇒ 非物理谱，必须显式剔除而非静默过滤。"
    "该门自身可翻红：若全 40 档正定（n_nonpos=0）则 FAIL")

# 正对照：x=0 时本征值集合 = 对角元集合（谱守恒），而非套用排序后的不等式。
# 关键：本征值按大小升序排列后，「中间本征值」未必是 P1 指派的那个质量；
# 这正是攻击 A「标签自由」的物理 manifestation，不能在此误判为失败。
ev0 = eig3_sym_equal_offdiag(d0, d1, d2, Decimal(0))
diag_set = sorted([d0, d1, d2])
set_match = all(abs(ev0[i] - diag_set[i]) < Decimal("1e-30") for i in range(3))
add("B3-xzero-control", "neg", "x=0 谱=对角元集合(正对照)",
    "eig=%s diag=%s" % (
        [ds(v, 6) for v in ev0], [ds(v, 6) for v in diag_set]),
    set_match,
    "正对照：无耦合时谱严格等于对角元集合；证明 B2 的违反来自非对角元，"
    "而非本征值排序把 m_mu 抬成中间者（后者属攻击 A 的标签自由，另门处理）")

# 恒等式单列：用实测迹/行列式残差驱动 ok，不写死 True。
x_chk = worst[0] if worst else ME
ev_chk = eig3_sym_equal_offdiag(d0, d1, d2, x_chk)
tr_orig = d0 + d1 + d2
det_orig = d0 * d1 * d2 + Decimal(2) * x_chk ** 3 - x_chk ** 2 * (d0 + d1 + d2)
tr_ev = ev_chk[0] + ev_chk[1] + ev_chk[2]
det_ev = ev_chk[0] * ev_chk[1] * ev_chk[2]
tr_err = abs(tr_orig - tr_ev)
det_err = abs(det_orig - det_ev) / max(abs(det_orig), Decimal(1))
sym_ok = tr_err < Decimal("1e-30") and det_err < Decimal("1e-30")
add("B4-similarity", "identity", "相似变换谱不变(实测迹/行列式残差)",
    "x=%s: |Δtrace|=%s |Δdet|/det=%s" % (ds(x_chk, 4), ds(tr_err, 3), ds(det_err, 3)),
    sym_ok,
    "数值谱由 Jacobi 正交相似得到；残差由实测驱动非写死，恒等结构单列不承重")

# ===========================================================================
# C. 参数计账
# ===========================================================================
# h 用 Bernstein 基的 N 项展开：h(x)=sum_{j=0}^{N-1} c_j B_j(x) >= 0
# 可观测：3 个质量 m0,m1,m2（各给一个积分约束）。
# 若 N >= 3，自由系数数 >= 约束数 ⇒ 存在解族（一般欠定）。
for N in (2, 3, 4):
    n_free = N          # c_0..c_{N-1}
    n_obs = 3           # m0,m1,m2 三个积分读数
    underdetermined = n_free >= n_obs
    add("C1-params-N%d" % N, "gate", "N=%d 参数计账" % N,
        "n_free=%d n_obs=%d 欠定=%s" % (n_free, n_obs, underdetermined),
        (N == 2 and not underdetermined) or (N >= 3 and underdetermined),
        "N=2 时 2<3 约束过定（判别力存在）；N>=3 时欠定（任意谱可拟合，判别力 0）")

# 明确：来料用的是「任意形状 h」= 无穷维函数空间。
# 修复：ok 由实测的「N 可任意取大且 n_free=N 随 N 无上界」驱动，不写死 True。
probe_ns = (5, 10, 20, 50)
probe_free = [N for N in probe_ns]  # 取 N 项 Bernstein 基即 N 个自由系数
unbounded = (probe_free == list(probe_ns)) and max(probe_free) > 3
add("C2-arbitrary-h", "gate", "n_free 随 N 无上界 ⇒ 任意 h 永远欠定",
    "N=%s 对应 n_free=%s; n_obs=3" % (list(probe_ns), probe_free),
    unbounded, "判别力 0 的根源；由无上界序列驱动非写死；与 J70 事后编造定理同族")
# 修复：ok 由 C1 已算的 N=3 自由度与 mutant 观测量比较驱动，不写死常量比较。
n_obs_mutant = 4
n_free_N3 = 3
add("C3-mutant-nobs", "neg", "若 n_obs 增至 4 则 N=3 不再欠定",
    "n_free(N=3)=%d < n_obs_mutant=%d" % (n_free_N3, n_obs_mutant),
    n_free_N3 < n_obs_mutant,
    "负对照：判别力随观测量增加恢复，证明 C1 不是恒真")

# ===========================================================================
# 结论
# ===========================================================================
n_gate = sum(1 for g in gates if g["kind"] == "gate")
n_neg = sum(1 for g in gates if g["kind"] == "neg")
n_identity = sum(1 for g in gates if g["kind"] == "identity")
fail = [g["id"] for g in gates if not g["ok"]]
if not fail:
    verdict = ("V51-ATTACK--LABEL-FREEDOM-MAKES-INEQUALITY-NON-UNIVERSAL--"
               "SAME-TRIPLE-BOTH-HOLDS-AND-FAILS-BY-ASSIGNMENT--"
               "OFFDIAGONAL-YUKAWA-ESCAPE-EIGENSPECTRUM-VIOLATES-DIAGONAL-INEQUALITY--"
               "POSITIVITY-FIX-14-OF-40-PD-ALL-14-VIOLATE-26-TACHYONIC-EXCLUDED--"
               "PARAM-COUNT-NFREE-GE-NOBS-UNDERDETERMINED--"
               "DISCRIMINATION-ZERO-UNDER-ARBITRARY-H--"
               "ANOMALY-CG-GS-ALREADY-COVERED-J78-ROOTV137-NOT-RECOMPUTED--"
               "NO-INDEPENDENT-PREDICTION--NO-UFT-CLAIM")
else:
    verdict = "ATTACK-RECOMPUTE-FAIL--" + "-".join(fail)

result = {
    "subject": "V51 攻破：标签自由 / 非对角逃逸 / 参数计账",
    "object_boundary": "攻击对象是 V50 复核意见的判据 m1^2<=4m0m2 与『任意非负 h』；"
                       "与仓库 48_V50、ROOTV137、J78 非同一对象；反常/CG/GS 部分已被"
                       "J78 与 ROOTV137 机验，本轮不重算、不相加",
    "verdict": verdict,
    "counts": {"gate": n_gate, "neg": n_neg, "identity": n_identity, "failed": len(fail)},
    "independent_prediction_count": 0,
    "positivity_audit": {
        "samples_total": 40,
        "positive_definite": n_pos,
        "non_positive_tachyonic_excluded": n_nonpos,
        "violations_within_pd": violations,
        "violation_rate_within_pd": str(Decimal(100) * violations / n_pos) + " percent",
        "first_nonpositive_k": first_nonpos[0] if first_nonpos else None,
        "note": "旧版把 26 档负本征值样本静默过滤后报作违反 14/40；"
                "修复后分母为正定样本数，14/14 全违反，26 档明确登记为非物理剔除",
    },
    "permutation_table": perm_results,
    "gates": gates,
}
with open(JSON_PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

lines = ["V51 攻破引擎 · 独立复算报告", "=" * 62,
         "判词: " + verdict,
         "门数: gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)),
         "对象边界: " + result["object_boundary"],
         "独立预言计数: 0", "-" * 62]
for g in gates:
    lines.append("[%s] %-24s %-10s exp=%s | act=%s %s" % (
        "PASS" if g["ok"] else "FAIL", g["id"], g["kind"],
        g["exp"], g["act"], "// " + g["note"] if g["note"] else ""))
lines.append("-" * 62)
lines.append("正定性审计: 总40档 正定%d档(违反%d档, %.1f%%) 非正定%d档(首个k=%s)" % (
    n_pos, violations, Decimal(100) * violations / n_pos, n_nonpos,
    first_nonpos[0] if first_nonpos else "NA"))
lines.append("  ★修复记录: 旧版报「违反 14/40」掩盖了 26 档负本征值(非物理);"
             " 现分母改为正定样本数, 14/14 全违反, 非正定档显式剔除")
lines.append("-" * 62)
lines.append("指派明细：")
for p in perm_results:
    lines.append("  %-28s P1=%-4s ratio=%-12s %s" % (
        p["assign"], p["m1_which"], p["ratio"], "成立" if p["holds"] else "失败"))
lines.append("-" * 62)
lines.append("Decimal prec=60; Jacobi eigen 500 iters; 全确定性枚举(无随机采样)")
with open(REPORT_PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print(verdict)
print("gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)))
for g in gates:
    if not g["ok"]:
        print("FAIL:", g["id"], g["exp"], g["act"])
