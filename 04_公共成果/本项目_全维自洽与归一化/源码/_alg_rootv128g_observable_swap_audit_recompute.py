# -*- coding: utf-8 -*-
"""
ROOT V128 第七册 · 「换观测量」出路的可算自审

性质：可算审计（非判定册）。不占 RID，不入 README，不与任何既有册相加。

本册要判的命题（本链自己提出的，必须反噬自己）
------------------------------------------------
第四册说「整体幅度对近点进动零信息，打破它要换观测量」。
第五册说「换观测量也不行——Eötvös 通道结构性失效」。
第六册说「零假设处 λ 的 Fisher 列精确为零」。
三册都把「换观测量（测距 / GM 独立标定 / Shapiro / LLR / 脉冲星计时）」
列为唯一剩下的出口，但**从未判它**。本册判它。

命题 S：把观测量从近点进动换成别的引力势泛函，
        就能在 beta=0 处测出 λ。

核心论证（严格，且可机读）
--------------------------
势  Phi(r; beta, lambda) = -(mu/r)(1 + beta*lambda^2*exp(-r/lambda))

在 beta = 0 处，Phi ≡ -mu/r  **逐点不含 lambda**，所以

    dPhi/dlambda |_{beta=0} = 0

对任意观测量 Q[Phi]（不必线性！），链式法则给

    dQ/dlambda |_{beta=0} = ∫ (delta Q / delta Phi) * (dPhi/dlambda) = 0

⇒ 命题 S 为假。而且这与「线性泛函」无关：即使 Q = ∫ w Phi^2，
只要 Phi 本身在 beta=0 处不含 lambda，导数仍精确为零。

边界（必须同时给）
------------------
beta != 0 时 Phi 含 λ 的形状，所有观测量的 λ 导数恢复非零 ⇒
「不可辨识」严格限于零假设，不是「Yukawa 的 λ 永远不可测」。
本册用注入-恢复正对照机读这条边界。

红线：不宣称攻破统一场论；不产生新物理；独立实验预言 0。
      本册不引入任何外部读数，纯结构与可辨识性分析。
"""

import ast
import hashlib
import json
import os
import sys
from decimal import Decimal as D, getcontext

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)

STEM = "_ALG_rootv128g_observable_swap_audit"
DATE = "2026-11-22"


def out_json():
    return os.path.join(BASE, "数据", "%s_%s.json" % (STEM, DATE))


def report_path():
    return os.path.join(BASE, "数据", "%s_report_%s.txt" % (STEM, DATE))


def upstream_5():
    return os.path.join(BASE, "数据",
                        "_ALG_rootv128e_largelambda_vacuity_recompute_2026-11-22.json")


def upstream_6():
    return os.path.join(BASE, "数据",
                        "_ALG_rootv128f_beta_fisher_recompute_2026-11-22.json")


# ------------------------------------------------------------------ Decimal
def Dq(x):
    if isinstance(x, D):
        return x
    if isinstance(x, int):
        return D(x)
    return D(str(x))


_PI = {}


def PI():
    if "v" not in _PI:
        def atan_inv(n):
            n = Dq(n)
            x = D(1) / n
            x2 = x * x
            s = D(0)
            t = x
            k = 0
            while True:
                q = t / Dq(2 * k + 1)
                s += q if k % 2 == 0 else -q
                t *= x2
                k += 1
                if abs(q) < D("1e-62"):
                    break
            return s
        _PI["v"] = 16 * atan_inv(5) - 4 * atan_inv(239)
    return _PI["v"]


def fmt(x, nd=6):
    if Dq(x) == 0:
        return "0"
    return ("%." + str(nd) + "E") % Dq(x)


def fstr(x, nd=6):
    """与 fmt 同义，供 JSON 读数使用。"""
    return fmt(x, nd)


def rel(a, b):
    a, b = Dq(a), Dq(b)
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


# ------------------------------------------------------------------ 物理核
AU = D("149597870700")


def phi(r, beta, lam, mu=D(1)):
    """Yukawa 势，用 beta = alpha/lam^2 参数化。r, lam 同单位（AU）。"""
    r, lam, beta = Dq(r), Dq(lam), Dq(beta)
    return -(mu / r) * (D(1) + beta * lam * lam * (-r / lam).exp())


def simpson(f, a, b, n):
    a, b = Dq(a), Dq(b)
    if n % 2:
        n += 1
    h = (b - a) / Dq(n)
    s = f(a) + f(b)
    for i in range(1, n):
        s += (D(4) if i % 2 else D(2)) * f(a + h * Dq(i))
    return s * h / D(3)


# ------------------------------------------------------------------ 五类观测量（势的泛函）
# 单位刻意统一为「势的量纲 × 路径长度」，只比较可辨识性结构，不冒充物理读数。
OBSERVABLES = [
    ("shapiro",      "Shapiro 延迟（沿视线积分势）"),
    ("light_bend",   "光线偏折（横向梯度积分）"),
    ("redshift",     "引力红移（两端势差）"),
    ("range",        "雷达测距往返（沿路径积分势的一阶修正）"),
    ("orbital_T",    "轨道周期（势决定的特征时标）"),
]


def observable(name, beta, lam, weight=1):
    """Q[Phi]。weight 只用于制造不同权重，不改变可辨识性结论。"""
    w = Dq(weight)
    lam = Dq(lam)
    if name == "shapiro":
        b = D("1")
        return w * 2 * simpson(lambda l: phi((b * b + l * l).sqrt(), beta, lam),
                               D(0), D(20), 400)
    if name == "light_bend":
        b = D("1")

        def integrand(l):
            r = (b * b + l * l).sqrt()
            # 横向梯度：dPhi/dr * b/r；用中心差分避免解析式混入 lambda
            h = D("1e-7")
            d = (phi(r + h, beta, lam) - phi(r - h, beta, lam)) / (2 * h)
            return d * b / r
        return w * 2 * simpson(integrand, D(0), D(20), 400)
    if name == "redshift":
        return w * (phi(D("1.2"), beta, lam) - phi(D("1.0"), beta, lam))
    if name == "range":
        return w * simpson(lambda l: phi(D("1.0") + l, beta, lam), D(0), D(2), 200)
    if name == "orbital_T":
        # T ∝ a^{3/2}/sqrt(mu_eff)；mu_eff 由 r=1 处的势给出（只做结构比较）
        mu_eff = -phi(D(1), beta, lam)
        return w / mu_eff.sqrt()
    raise ValueError(name)


def nonlinear_observable(beta, lam):
    """非线性泛函 Q = ∫ Phi^2 dl：验证结论与泛函是否线性无关。"""
    return simpson(lambda l: phi(D("1.0") + l, beta, lam) ** 2, D(0), D(2), 200)


def d_lambda(Qfun, beta, lam, rel_step=D("1e-5")):
    """中心差分 + Richardson 求 dQ/dlambda。"""
    l = Dq(lam)
    h = l * rel_step

    def one(step):
        return (Qfun(l + step) - Qfun(l - step)) / (2 * step)

    a, b = one(h), one(h / 2)
    return (D(4) * b - a) / D(3)


def d_beta(Qfun, beta, lam, h=D("1e-7")):
    b = Dq(beta)

    def one(step):
        return (Qfun(b + step) - Qfun(b - step)) / (2 * step)

    a, bb = one(h), one(h / 2)
    return (D(4) * bb - a) / D(3)
# ------------------------------------------------------------------ 门
def load_upstream():
    out = {}
    for tag, p in (("V", upstream_5()), ("F", upstream_6())):
        raw = open(p, "rb").read()
        out[tag] = (json.loads(raw.decode("utf-8")), hashlib.sha256(raw).hexdigest(), len(raw))
    return out


def gate_P1():
    """自检：beta=0 时势与五类泛函对 lambda 逐点不变；四阶收敛。"""
    ok = True
    note = []
    rows = []
    worst_phi = D(0)
    for r in ("0.1", "1", "5", "20"):
        for l1, l2 in (("0.5", "3"), ("3", "100"), ("100", "1e5")):
            a = phi(Dq(r), D(0), Dq(l1))
            b = phi(Dq(r), D(0), Dq(l2))
            worst_phi = max(worst_phi, abs(a - b))
    note.append("beta=0 时 Phi 对不同 lambda 逐点差 max = %s（机器零）" % fmt(worst_phi))

    worst_Q = D(0)
    for name, label in OBSERVABLES:
        a = observable(name, D(0), D(1))
        b = observable(name, D(0), D(100))
        d = abs(a - b)
        worst_Q = max(worst_Q, d)
        rows.append({"name": name, "Q_lam1": fmt(a), "Q_lam100": fmt(b), "diff": fmt(d)})
    note.append("五类泛函在 beta=0、lambda=1 与 100 AU 上的差 max = %s" % fmt(worst_Q))

    # 四阶收敛（用一个非零 beta 的 Shapiro 积分，检查积分器）
    # n=100 段仍在预渐近区（该解析 integrand 早期收敛快于 h^4），
    # 只作诊断登记；四阶判据取渐近段 n=200/400/800/1600，不放宽门限。
    def f(l):
        return phi((D(1) + l * l).sqrt(), D("1e-3"), D(10))
    n_pre = 100
    ns = (200, 400, 800, 1600)
    e_pre = simpson(f, D(0), D(20), n_pre)
    e = [simpson(f, D(0), D(20), n) for n in ns]
    ratio_pre = (e_pre - e[0]) / (e[0] - e[1])
    orders = [(e[i] - e[i + 1]) / (e[i + 1] - e[i + 2]) for i in (0, 1)]
    note.append("预渐近诊断（不作门）：逐次比(n=100,200,400) = %s，早期收敛快于四阶，故自检取 n=%s"
                % (fmt(ratio_pre, 3), "/".join(str(x) for x in ns)))
    note.append("渐近段积分误差逐次比 = %s / %s（四阶应约 16，门限 12<o<20 不放宽）"
                % (fmt(orders[0], 3), fmt(orders[1], 3)))

    if worst_phi > D("1e-55") or worst_Q > D("1e-45"):
        ok = False
        note.append("FAIL: beta=0 的势/泛函仍依赖 lambda")
    if not all(D(12) < o < D(20) for o in orders):
        ok = False
        note.append("FAIL: 积分器不是四阶")
    return {"id": "P1", "kind": "guard",
            "title": "自检：beta=0 势与五泛函逐点不变；积分四阶",
            "ok": ok, "notes": note, "rows": rows,
            "readings": {"worst_phi_diff": fmt(worst_phi),
                         "worst_functional_diff": fmt(worst_Q),
                         "pre_asymptotic_ratio_diagnostic_only": fmt(ratio_pre, 3),
                         "error_ratios": [fmt(o, 3) for o in orders]}}


def gate_P2():
    """承重：五类势泛函在 beta=0 处 dQ/dlambda 全零、dQ/dbeta 非零。"""
    ok = True
    note = []
    rows = []
    worst_dl = D(0)
    min_db = None

    for name, label in OBSERVABLES:
        dl_vals = []
        db_vals = []
        for ls in ("0.5", "1", "10", "100"):
            Q_lam = lambda l, nm=name: observable(nm, D(0), l)
            Q_beta = lambda b, nm=name: observable(nm, b, Dq(ls))
            dl = abs(d_lambda(Q_lam, D(0), Dq(ls)))
            db = abs(d_beta(Q_beta, D(0), Dq(ls)))
            dl_vals.append(dl)
            db_vals.append(db)
            worst_dl = max(worst_dl, dl)
            min_db = db if min_db is None else min(min_db, db)
        rows.append({"name": name, "label": label,
                     "max_abs_dQ_dlambda_at_beta0": fmt(max(dl_vals)),
                     "min_abs_dQ_dbeta_at_beta0": fmt(min(db_vals))})

    note.append("五类观测量 × 4 个 lambda：max|dQ/dlambda|_(beta=0) = %s" % fmt(worst_dl))
    note.append("同一批配置中 min|dQ/dbeta|_(beta=0) = %s（>0，说明观测量对信号本身敏感）"
                % fmt(min_db))
    note.append("链式法则：dQ/dlambda = ∫ (deltaQ/deltaPhi)(dPhi/dlambda)，"
                "而 beta=0 时 dPhi/dlambda 逐点为零")
    if worst_dl > D("1e-40"):
        ok = False
        note.append("FAIL: 存在观测量在 beta=0 处仍对 lambda 敏感")
    if min_db <= 0:
        ok = False
        note.append("FAIL: 观测量连 beta 都不敏感，判据退化")
    return {"id": "P2", "kind": "load-bearing",
            "title": "五类势泛函在 beta=0 处 dQ/dlambda 恒零（承重）",
            "ok": ok, "notes": note, "rows": rows,
            "readings": {"max_abs_dQ_dlambda_at_null": fmt(worst_dl),
                         "min_abs_dQ_dbeta_at_null": fmt(min_db)}}


def gate_P3():
    """承重：非线性泛函同样不行 => 不是「线性泛函」的缺陷。"""
    ok = True
    note = []
    rows = []
    worst_dl = D(0)
    for ls in ("0.5", "1", "10", "100"):
        lam = Dq(ls)
        Q = lambda l: nonlinear_observable(D(0), l)
        dl = abs(d_lambda(Q, D(0), lam))
        Qb = lambda b: nonlinear_observable(b, lam)
        db = abs(d_beta(Qb, D(0), lam))
        worst_dl = max(worst_dl, dl)
        rows.append({"lam_AU": ls, "dQ2_dlambda": fmt(dl), "dQ2_dbeta": fmt(db)})
    note.append("非线性泛函 Q = ∫Phi^2 dl：max|dQ/dlambda|_(beta=0) = %s" % fmt(worst_dl))
    note.append("=> 障碍不是泛函的线性性，而是 beta=0 时 Phi 本身不含 lambda")
    if worst_dl > D("1e-40"):
        ok = False
        note.append("FAIL: 非线性泛函恢复了 lambda 灵敏度")
    return {"id": "P3", "kind": "load-bearing",
            "title": "非线性势泛函同样零导数：障碍与线性性无关（承重）",
            "ok": ok, "notes": note, "rows": rows,
            "readings": {"max_abs_dQ2_dlambda_at_null": fmt(worst_dl)}}


def gate_P4():
    """边界正对照：beta != 0 时五类泛函的 lambda 导数必须恢复。"""
    ok = True
    note = []
    rows = []
    beta = D("1e-3")
    worst = D("1e9")
    for name, label in OBSERVABLES:
        vals = []
        for ls in ("0.5", "1", "10"):
            lam = Dq(ls)
            Q = lambda l, nm=name: observable(nm, beta, l)
            vals.append(abs(d_lambda(Q, beta, lam)))
        mn = min(vals)
        worst = min(worst, mn)
        rows.append({"name": name, "min_abs_dQ_dlambda_at_beta1e3": fmt(mn)})
    note.append("注入 beta=1e-3 后，五类泛函的最小 |dQ/dlambda| = %s（全部 >0）" % fmt(worst))
    note.append("=> 「不可辨识」严格限于零假设，不是 Yukawa 的 lambda 永远不可测")
    if worst <= 0:
        ok = False
        note.append("FAIL: 非零 beta 下仍无 lambda 信息")
    return {"id": "P4", "kind": "structural-positive",
            "title": "边界：注入非零 beta 后所有泛函恢复 lambda 灵敏度",
            "ok": ok, "notes": note, "rows": rows,
            "readings": {"min_over_observables_abs_dQ_dlambda": fmt(worst)}}


def gate_P5(flags):
    """自噬：把本链自己提出的命题 S 判为 REFUTED。"""
    ok = True
    note = []
    note.append("命题 S（本链第四/五/六册留下的出路）："
                "「把观测量从近点进动换成 Shapiro / 测距 / LLR / 红移 / 周期，"
                "就能在 beta=0 处测出 lambda」")
    note.append("机读判决：P2（五类泛函 dQ/dlambda 全零）+ P3（非线性泛函同样零）"
                "⇒ S = REFUTED")
    note.append("这不是实验否证，是可辨识性的代数否证："
                "beta=0 时 Phi 不含 lambda，任何 Phi 的泛函都不可能携带 lambda 信息")
    claim = "REFUTED" if (flags["P2"] and flags["P3"]) else "NOT-REFUTED"
    if claim != "REFUTED":
        ok = False
        note.append("FAIL: 承重门未同时成立，不能判 S 被否证")
    return {"id": "P5", "kind": "load-bearing-negative",
            "title": "自噬：本链自己的「换观测量」出路被判 REFUTED",
            "ok": ok, "notes": note,
            "readings": {"claim_S": claim,
                         "source_volumes": "V128 第四/五/六册"}}


def gate_P6():
    """设计研究：统一假定 sigma_Q/Q=1e-9，比较五类泛函的 sigma_beta。"""
    ok = True
    note = []
    rows = []
    lam = D(1)
    rel_prec = D("1e-9")   # 统一假设，非任何仪器的实际读数
    vals = []
    for name, label in OBSERVABLES:
        Q = observable(name, D(0), lam)
        db = abs(d_beta(lambda b, nm=name: observable(nm, b, lam), D(0), lam))
        if db == 0:
            continue
        sig_beta = rel_prec * abs(Q) / db
        vals.append((sig_beta, name))
        rows.append({"name": name, "Q_at_null": fmt(Q),
                     "dQ_dbeta": fmt(db), "sigma_beta_assumed": fmt(sig_beta)})
    best = min(vals) if vals else (None, None)
    note.append("统一假定相对精度 sigma_Q/|Q| = 1e-9（**设计研究，不是观测约束**）")
    note.append("五类泛函的 sigma_beta 已在表中；最优 = %s（%s）"
                % (fmt(best[0]) if best[0] else "n/a", best[1] or "n/a"))
    note.append("关键：无论哪种观测量，P2 已证 sigma_lambda = infinity 在 beta=0 不改善")
    note.append("=> 换观测量可以改善 beta 的精度，但不能改变 lambda 的不可辨识性")
    if best[0] is None:
        ok = False
        note.append("FAIL: 没有任何观测量给出有限的 sigma_beta")
    return {"id": "P6", "kind": "structural",
            "title": "设计研究：换观测量只改善 beta 精度，不改善 lambda 可辨识性",
            "ok": ok, "notes": note, "rows": rows,
            "readings": {"assumed_relative_precision": fstr(rel_prec),
                         "best_observable": best[1] or "n/a",
                         "best_sigma_beta": fmt(best[0]) if best[0] else "n/a"}}


def gate_P7():
    """反噬：若观测量直接就是参数 lambda 本身，P2 判据必须失败。"""
    ok = True
    note = []
    beta = D(0)
    lam = D(1)
    fake = lambda l: l                      # 不是任何势的泛函，就是参数本身
    dl = d_lambda(fake, beta, lam)
    note.append("伪观测量 Q_fake = lambda（不是势的泛函，而是参数自身）："
                "dQ/dlambda = %s" % fmt(dl))
    note.append("P2 判据在此会 FAIL ⇒ 判别力存在，不是「所有对象都通过」")
    note.append("但这类 Q_fake 若被当成观测，等于把待测量写进仪器，属循环论证")
    if not (dl > 0):
        ok = False
        note.append("FAIL: 反噬配置未使判据翻转")
    return {"id": "P7", "kind": "guard",
            "title": "反噬：直接把参数当观测量会使判据翻转（循环论证）",
            "ok": ok, "notes": note,
            "readings": {"fake_dQ_dlambda": fmt(dl)}}


def gate_P8(U):
    """上游一致性：第五/六册判词存在，且本册结论是推广而非推翻。"""
    ok = True
    note = []
    rows = []
    for tag, (data, sha, nb) in U.items():
        v = data.get("verdict", "")
        rows.append({"volume": tag, "verdict_prefix": v[:40],
                     "sha": sha[:16], "bytes": nb})
        note.append("%s 册判词前缀 %s…，sha %s，%d B" % (tag, v[:32], sha[:16], nb))
        if "UFT-NOT-BROKEN" not in v:
            ok = False
            note.append("FAIL %s: 上游判词缺红线标记" % tag)
    note.append("本册结论是第五册（幅度简并）与第六册（beta=0 处 lambda 奇性）的推广，"
                "不推翻任何上游判词")
    return {"id": "P8", "kind": "structural",
            "title": "上游一致性：第五/六册判词存在且本册只作推广",
            "ok": ok, "notes": note, "rows": rows,
            "readings": {}}

# ------------------------------------------------------------------ 判词
def verdict_of(f2, f3, f5):
    if f2 and f3 and f5:
        return ("ROOTV128G-OBSERVABLE-SWAP-DOES-NOT-RESCUE-LAMBDA"
                "--ALL-POTENTIAL-FUNCTIONALS-HAVE-ZERO-LAMBDA-DERIVATIVE-AT-BETA-ZERO"
                "--NOT-A-LINEARITY-ISSUE-NONLINEAR-FUNCTIONALS-ALSO-DEGENERATE"
                "--CLAIM-S-FROM-OWN-PRIOR-VOLUMES-REFUTED"
                "--SWAPPING-OBSERVABLE-IMPROVES-BETA-PRECISION-ONLY"
                "--NONZERO-BETA-RESTORES-LAMBDA-INFORMATION"
                "--UFT-NOT-BROKEN"
                "--NO-INDEPENDENT-PREDICTION")
    bad = []
    if not f2:
        bad.append("LINEAR-FUNCTIONALS-NOT-DEGENERATE")
    if not f3:
        bad.append("NONLINEAR-FUNCTIONAL-DEGENERACY-REFUTED")
    if not f5:
        bad.append("CLAIM-S-NOT-REFUTED")
    return "ROOTV128G-CLAIM-REFUTED--" + "--".join(bad)


def _ok_assigns(fn):
    out = []

    def walk(node, depth):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "ok" for t in ch.targets):
                out.append((ch, depth, ch.value))
            walk(ch, depth + (1 if isinstance(ch, (ast.If, ast.For, ast.While, ast.Try))
                              else 0))
    walk(fn, 0)
    return out


def gate_verdict_machine():
    base = verdict_of(True, True, True)
    vs = [verdict_of(False, True, True), verdict_of(True, False, True),
          verdict_of(True, True, False)]
    ok = all(v != base for v in vs)
    return {"id": "G-VERDICT-MACHINE", "kind": "guard", "ok": ok,
            "title": "判词机读：三个承重标志任一翻转必改判词串",
            "notes": ["基线 %d 字符；变体 %s" % (len(base), [len(v) for v in vs])],
            "readings": {}}


def gate_no_hardcode():
    src = open(os.path.abspath(__file__), "rb").read().decode("utf-8")
    tree = ast.parse(src)
    bad = []
    scanned = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        asg = _ok_assigns(node)
        if not asg:
            continue
        scanned += 1
        top = [a for a in asg if a[1] == 0 and isinstance(a[2], ast.Constant)]
        nested = [a for a in asg if a[1] >= 1]
        if top and not nested:
            bad.append((node.name, node.lineno))
    return {"id": "G-NO-HARDCODE-OK", "kind": "guard", "ok": not bad,
            "title": "AST 守卫：ok 不得顶层赋常量且无条件翻转",
            "notes": ["扫描 %d 个函数" % scanned, str(bad) if bad else "零命中"],
            "readings": {"n_functions_scanned": scanned}}


def gate_link(jp, rp, verdict):
    ok = True
    notes = []
    for p in (jp, rp):
        if not os.path.exists(p):
            ok = False
            notes.append("缺失 %s" % os.path.basename(p))
            continue
        t = open(p, "rb").read().decode("utf-8", "ignore")
        v, d = verdict in t, DATE in t
        ok = ok and v and d
        notes.append("%s: verdict=%s date=%s" % (os.path.basename(p), v, d))
    return {"id": "G-LINK", "kind": "guard", "ok": ok,
            "title": "链接体检：JSON 与报告均含判词串与日期",
            "notes": notes, "readings": {}}


def render_report(gates, verdict, final, ups):
    L = []
    add = L.append
    add("=" * 78)
    add("ROOT V128 第七册 · 「换观测量」出路的可算自审")
    add("算法联盟可算审计（非判定册）  date : %s" % DATE)
    add("=" * 78)
    add("")
    add("claim_S : 换观测量可在 beta=0 处测出 lambda（本链前册留下的出路）")
    for tag, (data, sha, nb) in ups.items():
        add("upstream_%s : %s / %s / %d B" % (tag, data.get("verdict", "")[:40], sha[:16], nb))
    add("")
    add("-" * 78)
    for g in gates:
        add("[%s] %s  %s" % (g["id"], "OK  " if g["ok"] else "FAIL", g["title"]))
        for n in g.get("notes", []):
            add("       " + n)
        for k, v in (g.get("readings") or {}).items():
            add("       .%-40s = %s" % (k, v))
        for r in (g.get("rows") or [])[:8]:
            add("       | " + "  ".join("%s=%s" % (kv, vv) for kv, vv in r.items()))
        add("")
    add("-" * 78)
    add("verdict   : %s" % verdict)
    add("final     : %s" % final)
    add("guards    : %s" % " ".join(g["id"] for g in gates if g["kind"] == "guard"))
    add("bearing   : %s" % " ".join(g["id"] for g in gates
                                    if g["kind"].startswith("load-bearing")))
    add("n_gate_ok : %d / %d" % (sum(1 for g in gates if g["ok"]), len(gates)))
    add("")
    add("red_line  : 不宣称攻破统一场论；不产生新物理；独立实验预言 0；")
    add("            本册判的是本链自己的命题 S，不引入任何外部读数。")
    add("boundary  : beta=0 处所有势泛函对 lambda 零导数；beta!=0 时恢复（P4）。")
    add("            不证明第五力不存在，不证明 Yukawa 的 lambda 永远不可测。")
    add("=" * 78)
    return "\n".join(L) + "\n"


def build_payload(gates, verdict, final, ups):
    return {
        "kind": "algorithm-alliance-audit-recompute",
        "not_a_verdict_volume": True,
        "occupies_rid": False,
        "enters_readme": False,
        "title": "ROOT V128 第七册 换观测量出路的可算自审",
        "date": DATE,
        "claim_under_test": "换观测量可在 beta=0 处测出 lambda（本链前册留下的出路）",
        "upstream": {tag: {"verdict": data.get("verdict", ""),
                           "sha256": sha, "bytes": nb}
                     for tag, (data, sha, nb) in ups.items()},
        "verdict": verdict,
        "verdict_type": "machine",
        "final": final,
        "n_gate_ok": sum(1 for g in gates if g["ok"]),
        "n_gate_total": len(gates),
        "guards": [g["id"] for g in gates if g["kind"] == "guard"],
        "load_bearing_gates": [g["id"] for g in gates
                               if g["kind"].startswith("load-bearing")],
        "gates": gates,
        "discipline": [
            "判据必反噬自己：本册判的是本链前册留下的命题 S",
            "结论与泛函线性性无关（P3 用 Phi^2 反证）",
            "必须给边界：非零 beta 时 lambda 恢复可测（P4）",
            "设计研究（P6 的 1e-9 相对精度）不得冒充观测约束",
            "判词由唯一构造函数生成，三个承重标志任一翻转必变",
        ],
        "red_line": [
            "不宣称攻破统一场论",
            "不产生新物理，独立实验预言 0",
            "不引入外部读数，不修改任何上游判词",
            "不可辨识 != 模型被证伪",
        ],
    }


def write_json(gates, verdict, final, ups):
    p = out_json()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(build_payload(gates, verdict, final, ups),
                            ensure_ascii=False, indent=1, sort_keys=False) + "\n")
    return p


def write_report(gates, verdict, final, ups):
    p = report_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(render_report(gates, verdict, final, ups))
    return p


def main():
    U = load_upstream()
    flags = {}
    gates = [gate_P1()]
    for gid, fn in (("P2", gate_P2), ("P3", gate_P3), ("P4", gate_P4),
                    ("P6", gate_P6), ("P7", gate_P7), ("P8", lambda: gate_P8(U))):
        g = fn()
        flags[gid] = g["ok"]
        gates.append(g)
    gates.append(gate_P5(flags))
    flags["P5"] = gates[-1]["ok"]
    gates.append(gate_verdict_machine())
    gates.append(gate_no_hardcode())

    verdict = verdict_of(flags["P2"], flags["P3"], flags["P5"])

    def decide(gs):
        bad = [g["id"] for g in gs if not g["ok"]]
        if bad:
            return "GATES-FAIL--" + "-".join(bad)
        if flags["P2"] and flags["P3"] and flags["P5"]:
            return "GATES-PASS-WITH-CLAIM-REFUTED"
        return "GATES-PASS-BUT-CLAIM-NOT-REFUTED"

    final = decide(gates)
    write_report(gates, verdict, final, U)
    write_json(gates, verdict, final, U)
    gates.append(gate_link(out_json(), report_path(), verdict))
    final = decide(gates)
    rp = write_report(gates, verdict, final, U)
    jp = write_json(gates, verdict, final, U)

    n_ok = sum(1 for g in gates if g["ok"])
    sys.stdout.write("verdict   : %s\n" % verdict)
    sys.stdout.write("final     : %s\n" % final)
    sys.stdout.write("n_gate_ok : %d / %d\n" % (n_ok, len(gates)))
    sys.stdout.write("gates     : %s\n" % ".".join("%s=%s" % (g["id"], g["ok"]) for g in gates))
    sys.stdout.write("report    : %s\n" % rp)
    sys.stdout.write("json      : %s\n" % jp)
    raw = open(jp, "rb").read()
    sys.stdout.write("json_bytes: %d\n" % len(raw))
    sys.stdout.write("json_sha  : %s\n" % hashlib.sha256(raw).hexdigest())
    for g in gates:
        if not g["ok"]:
            sys.stdout.write("FAILED GATE: %s\n" % g["id"])
            for n in g.get("notes", []):
                if n.startswith("FAIL"):
                    sys.stdout.write("    " + n + "\n")
    return 0 if n_ok == len(gates) else 1


if __name__ == "__main__":
    sys.exit(main())
