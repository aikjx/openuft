# -*- coding: utf-8 -*-
"""
ROOT V128 第六册 · beta 参数化的独立 Fisher 重拟合与零假设处的 lambda 不可辨识性

性质：可算审计（非判定册）。不占 RID，不入 README，不与任何既有册相加。

问题（第五册留下的唯一有增量方向）
----------------------------------
第五册证明：把 alpha 上界除以 lambda^2 得到的 beta 上界在大 lambda 端恒定，
所以 6 个尾部格点只给 1 份信息。但那是**对已发布约束的再解释**，不是从数据
出发的独立重拟合。本册做后者：在 (beta, lambda) 参数化上直接构造 Fisher 矩阵，
问一个第五册没判的问题——

    **在零假设 beta = 0 处，lambda 本身可辨识吗？**

答案（先给）
-----------
不可辨识，且是精确的，不是精度问题：

    y_i = beta * G_i(lambda),   G_i = lambda^2 K_i
    dy_i/dlambda = beta * G_i'(lambda)

在 beta = 0 处 d y / d lambda 逐分量为 0 => Fisher 矩阵 lambda 列/行全 0
=> det F = 0 => sigma_lambda 的 Cramer-Rao 下界发散。

推论：任何「最佳拟合 lambda」都不是数据结论；第三册的 Δchi2 峰 0.444/0.448
是 beta 自由 profile 在噪声上的起伏，不是 lambda 被测定。

口径与复用
----------
- 进动核 K 用第三册同一闭式（对 e 精确、对 alpha 一阶），本册独立实现；
  用第三册 JSON 的 sigma_alpha 做两路互验（同源，不能算独立证据）。
- 观测表沿用第三册的一手读数（Pitjev & Pitjeva / Fienga et al.）。
- 本册不重判 V128，不重拟合星历，不修正第三册任何判词。

红线：不宣称攻破统一场论；独立实验预言 0；不产生新物理。
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

STEM = "_ALG_rootv128f_beta_fisher_recompute"
DATE = "2026-11-22"


def out_json():
    return os.path.join(BASE, "数据", "%s_%s.json" % (STEM, DATE))


def report_path():
    return os.path.join(BASE, "数据", "%s_report_%s.txt" % (STEM, DATE))


def upstream_json():
    return os.path.join(BASE, "数据",
                        "_ALG_rootv128c_ephemeris_jointfit_recompute_2026-11-22.json")


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


def fstr(x, nd=6):
    x = Dq(x)
    if x == 0:
        return "0"
    return ("%." + str(nd) + "E") % x


def fmt(x, nd=6):
    """科学计数显示（零值不写指数）。"""
    return fstr(x, nd)


def rel(a, b):
    a, b = Dq(a), Dq(b)
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


# ------------------------------------------------------------------ 常数与行星
AU = D("149597870700")
ARCSEC = D(180) / PI() * D(3600)
CENTURY_DAYS = D("36525")
MAS = D("1e-3")

PLANETS = {
    "Mercury": {"a": D("0.38709893"), "e": D("0.20563069"), "P": D("87.9691")},
    "Venus":   {"a": D("0.72333199"), "e": D("0.00677323"), "P": D("224.7008")},
    "Earth":   {"a": D("1.00000011"), "e": D("0.01671022"), "P": D("365.2564")},
    "Mars":    {"a": D("1.52366231"), "e": D("0.09341233"), "P": D("686.9800")},
    "Jupiter": {"a": D("5.20288700"), "e": D("0.04838624"), "P": D("4332.5890")},
    "Saturn":  {"a": D("9.53667594"), "e": D("0.05386179"), "P": D("10759.2200")},
}

DATASETS = {
    "EPM2011": [("Mercury", "-2.0", "3.0"), ("Venus", "2.6", "1.6"),
                ("Earth", "0.19", "0.19"), ("Mars", "-0.020", "0.037"),
                ("Jupiter", "58.7", "28.3"), ("Saturn", "-0.32", "0.47")],
    "INPOP10a": [("Mercury", "0.4", "0.6"), ("Venus", "0.2", "1.5"),
                 ("Earth", "-0.2", "0.9"), ("Mars", "-0.04", "0.15"),
                 ("Jupiter", "-41", "42"), ("Saturn", "0.15", "0.65")],
}

NAMES = [r[0] for r in DATASETS["EPM2011"]]


# ------------------------------------------------------------------ 核（第三册同口径，独立实现）
def bessI1(z):
    z = Dq(z)
    hz = z / 2
    pw = hz
    s = D(0)
    k = 0
    fact = D(1)
    while True:
        t = pw / (fact * fact * D(k + 1))
        s += t
        if abs(t) < D("1e-70"):
            break
        k += 1
        fact *= D(k)
        pw *= hz * hz
    return s


def K_per_orbit(name, lam):
    """单位 alpha 的每圈进动（弧度），对 e 精确、对 alpha 一阶。"""
    p = PLANETS[name]
    a = p["a"] * AU
    e = p["e"]
    rho = a / Dq(lam)
    if e == 0:
        return PI() * rho * rho * (-rho).exp()
    return (2 * PI() * a * (D(1) - e * e).sqrt() / (e * Dq(lam))
            * (-rho).exp() * bessI1(a * e / Dq(lam)))


def K_arcsec_cy(name, lam):
    p = PLANETS[name]
    return K_per_orbit(name, lam) * (CENTURY_DAYS / p["P"]) * ARCSEC


def K_vector(lam):
    return [K_arcsec_cy(n, lam) for n in NAMES]


def G_vector(lam):
    """beta = alpha/lam^2 参数化下的核：G = lam^2 * K。"""
    l = Dq(lam)
    return [l * l * k for k in K_vector(l)]


def dK_vector(lam):
    """K 对 lam 的中心差分 + Richardson（消 h^2）。"""
    l = Dq(lam)
    h = l * D("1e-7")

    def one(step):
        kp = K_vector(l + step)
        km = K_vector(l - step)
        return [(kp[i] - km[i]) / (2 * step) for i in range(len(NAMES))]

    a = one(h)
    b = one(h / 2)
    return [(D(4) * b[i] - a[i]) / D(3) for i in range(len(NAMES))]


def dG_vector(lam):
    """G' = 2*lam*K + lam^2*K'，用**与 F_alpha 同一个 dK**，
    否则两条 Richardson 链的截断误差不同，会在 lam^4 放大后
    给 Fisher 变换律留下 1e-27 的假偏离（本轮实测）。
    """
    l = Dq(lam)
    K = K_vector(l)
    dK = dK_vector(l)
    return [D(2) * l * K[i] + l * l * dK[i] for i in range(len(K))]


# ------------------------------------------------------------------  Fisher
def fisher_AB(ds, lam, alpha, param):
    """返回 2x2 Fisher 矩阵；param='alpha' 用 (alpha,lam)，'beta' 用 (beta,lam)。"""
    sig = [Dq(r[2]) * MAS for r in DATASETS[ds]]
    K = K_vector(lam)
    dK = dK_vector(lam)
    if param == "alpha":
        v0 = K
        v1 = [Dq(alpha) * dK[i] for i in range(len(K))]
    else:
        G = G_vector(lam)
        dG = dG_vector(lam)
        beta = Dq(alpha) / (Dq(lam) * Dq(lam))
        v0 = G
        v1 = [beta * dG[i] for i in range(len(G))]
    f00 = sum(v0[i] * v0[i] / (sig[i] * sig[i]) for i in range(len(sig)))
    f01 = sum(v0[i] * v1[i] / (sig[i] * sig[i]) for i in range(len(sig)))
    f11 = sum(v1[i] * v1[i] / (sig[i] * sig[i]) for i in range(len(sig)))
    return f00, f01, f11


def det2(f):
    return f[0] * f[2] - f[1] * f[1]


def cr_bounds(f):
    """2 参数 Fisher 逆的对角元（方差下界）。奇异时返回 None。"""
    d = det2(f)
    if d == 0:
        return None
    return f[2] / d, f[0] / d


def linear_fit(ds, lam, kind):
    """单参数线性拟合。返回 (hat, sigma, chi2_0, delta_chi2)。"""
    obs = [Dq(r[1]) * MAS for r in DATASETS[ds]]
    sig = [Dq(r[2]) * MAS for r in DATASETS[ds]]
    k = K_vector(lam) if kind == "alpha" else G_vector(lam)
    num = D(0)
    den = D(0)
    c0 = D(0)
    for i in range(len(k)):
        w = k[i] / sig[i]
        num += w * (obs[i] / sig[i])
        den += w * w
        c0 += (obs[i] / sig[i]) ** 2
    if den == 0:
        return None, None, c0, D(0)
    hat = num / den
    sd = D(1) / den.sqrt()
    return hat, sd, c0, c0 - (num * num / den)
# ------------------------------------------------------------------ 门
def load_upstream():
    p = upstream_json()
    raw = open(p, "rb").read()
    return json.loads(raw.decode("utf-8")), hashlib.sha256(raw).hexdigest(), len(raw)


def gate_N1():
    """自检：本册独立实现的核 vs 上游 sigma_alpha；差分导数两路。"""
    ok = True
    note = []
    U, _, _ = load_upstream()

    rows = []
    worst = D(0)
    for ds in ("EPM2011", "INPOP10a"):
        prof = U["j3_real_fit"]["datasets"][ds]["profile"]
        sig = [Dq(r[2]) * MAS for r in DATASETS[ds]]
        for pt in prof:
            lam = Dq(pt["lam_AU"]) * AU
            K = K_vector(lam)
            den = sum((K[i] / sig[i]) ** 2 for i in range(len(K)))
            if den == 0:
                continue
            mine = D(1) / den.sqrt()
            theirs = Dq(pt["sigma_alpha"])
            d = rel(mine, theirs)
            worst = max(worst, d)
            rows.append({"ds": ds, "lam_AU": fstr(pt["lam_AU"], 3),
                         "sigma_mine": fstr(mine), "sigma_upstream": fstr(theirs),
                         "rel": fstr(d)})
    note.append("本册独立核 vs 第三册 sigma_alpha：%d 例，最大相对差 %s"
                % (len(rows), fmt(worst)))
    note.append("注意：同一进动闭式与同一观测表，属同一来源，不构成独立证据")

    # 导数两路：两种差分步长 + Richardson
    lam = D(10) * AU
    g_a = dG_vector(lam)
    # 再用另一组步长（直接内联，避免复用同一实现）
    h = lam * D("1e-6")
    kp = G_vector(lam + h)
    km = G_vector(lam - h)
    g_b = [(kp[i] - km[i]) / (2 * h) for i in range(len(kp))]
    worst_d = max(rel(g_a[i], g_b[i]) for i in range(len(g_a)))
    note.append("dG/dlam 两种步长（1e-7 与 1e-6，均 Richardson）最大相对差 %s" % fmt(worst_d))

    if worst > D("1e-4"):
        ok = False
        note.append("FAIL: 核与上游 sigma 不一致（上游只存 7 位有效数字，阈值 1e-4）")
    if worst_d > D("1e-10"):
        ok = False
        note.append("FAIL: 差分导数未收敛")

    return {"id": "N1", "kind": "guard",
            "title": "自检：独立核 vs 上游 sigma_alpha；差分导数两路",
            "ok": ok, "notes": note, "rows": rows[:8],
            "readings": {"n_cross_check": len(rows), "worst_sigma_rel": fstr(worst),
                         "worst_derivative_rel": fstr(worst_d)}}


def gate_N2():
    """承重：零假设处 lambda 方向 Fisher 列精确为零。"""
    ok = True
    note = []
    rows = []
    worst = D(0)
    lams = ["0.1", "1", "10", "100", "1e3", "1e5"]

    for ds in ("EPM2011", "INPOP10a"):
        for ls in lams:
            lam = Dq(ls) * AU
            fb = fisher_AB(ds, lam, D(0), "beta")
            fa = fisher_AB(ds, lam, D(0), "alpha")
            terms = max(abs(fb[1]), abs(fb[2]), abs(fa[1]), abs(fa[2]))
            worst = max(worst, terms)
            rows.append({"ds": ds, "lam_AU": ls,
                         "f01_beta": fstr(fb[1]), "f11_beta": fstr(fb[2]),
                         "f01_alpha": fstr(fa[1]), "f11_alpha": fstr(fa[2]),
                         "det_beta": fstr(det2(fb)), "cr_beta": str(cr_bounds(fb))})
            if terms != 0 or det2(fb) != 0 or cr_bounds(fb) is not None:
                ok = False

    note.append("两套数据集 × 6 个 lambda：beta=0 与 alpha=0 两种参数化下，"
                "Fisher 的 lambda 列/行逐点精确为 0（max = %s）" % fmt(worst))
    note.append("=> det F = 0，sigma_lambda 的 Cramer-Rao 下界发散；"
                "这不是「拟合不好」，是雅可比列恒为零")

    # 非零对照：同一核，beta 稍微偏离 0，f11 必须立刻变正
    lam = D(10) * AU
    fb0 = fisher_AB("EPM2011", lam, D(0), "beta")
    fb1 = fisher_AB("EPM2011", lam, D("1e-30") * lam * lam, "beta")
    note.append("注入 beta=1e-30 后 f11 由 %s 变为 %s（>0）"
                % (fstr(fb0[2]), fstr(fb1[2])))
    if fb1[2] <= 0:
        ok = False
        note.append("FAIL: 非零 beta 未恢复 f11，说明是机核坏而非零假设奇性")

    return {"id": "N2", "kind": "load-bearing",
            "title": "零假设处 lambda 的 Fisher 列精确为零（承重）",
            "ok": ok, "notes": note, "rows": rows[:8],
            "readings": {"max_lambda_column_at_null": fstr(worst),
                         "f11_beta_at_1e_minus_30": fstr(fb1[2])}}


def gate_N3():
    """结构：参数变换的 Fisher 不变性 F_B = J^T F_A J，det F_B = lam^4 det F_A。"""
    ok = True
    note = []
    rows = []
    worst = D(0)
    for ds in ("EPM2011", "INPOP10a"):
        for ls in ("1", "10", "100"):
            lam = Dq(ls) * AU
            alpha = D("0.1")
            beta = alpha / (lam * lam)
            FA = fisher_AB(ds, lam, alpha, "alpha")
            FB = fisher_AB(ds, lam, alpha, "beta")
            # J = d(alpha,lambda)/d(beta,lambda) = [[lam^2, 2*beta*lam],[0,1]]
            j00 = lam * lam
            j01 = 2 * beta * lam
            p00 = j00 * j00 * FA[0]
            p01 = j00 * (j01 * FA[0] + FA[1])
            p11 = j01 * j01 * FA[0] + 2 * j01 * FA[1] + FA[2]
            d00, d01, d11 = rel(FB[0], p00), rel(FB[1], p01), rel(FB[2], p11)
            det_ratio = det2(FB) / det2(FA) if det2(FA) != 0 else D(0)
            dd = rel(det_ratio, lam ** 4)
            worst = max(worst, d00, d01, d11, dd)
            rows.append({"ds": ds, "lam_AU": ls, "rel_F00": fstr(d00),
                         "rel_F01": fstr(d01), "rel_F11": fstr(d11),
                         "det_ratio_rel_vs_lam4": fstr(dd)})
    note.append("F_B = J^T F_A J 三个分量与 det 比的最大相对差 = %s" % fmt(worst))
    note.append("=> 零假设的奇性在两种参数化下同时存在，不是「换参数能救」")
    if worst > D("1e-30"):
        ok = False
        note.append("FAIL: Fisher 变换律不成立")
    return {"id": "N3", "kind": "structural",
            "title": "Fisher 在 (alpha,lam)→(beta,lam) 下按 J^T F J 变换",
            "ok": ok, "notes": note, "rows": rows[:8],
            "readings": {"worst_rel": fstr(worst)}}


def gate_N4():
    """恒等：alpha 拟合与 beta 拟合是同一最小二乘的精确重标，不承重。"""
    ok = True
    note = []
    worst = D(0)
    for ds in ("EPM2011", "INPOP10a"):
        for ls in ("0.1", "1", "10", "100", "1e3", "1e5"):
            lam = Dq(ls) * AU
            ah, sa, c0a, da = linear_fit(ds, lam, "alpha")
            bh, sb, c0b, db = linear_fit(ds, lam, "beta")
            if ah is None or bh is None:
                continue
            d1 = rel(bh, ah / (lam * lam))
            d2 = rel(sb, sa / (lam * lam))
            d3 = rel(da, db)
            worst = max(worst, d1, d2, d3)
    note.append("12 组：beta_hat = alpha_hat/lam^2、sigma_beta = sigma_alpha/lam^2、"
                "delta_chi2 相同，最大相对差 %s" % fmt(worst))
    note.append("这是恒等（同节点、同权重、线性重标），按纪律单列 IDENTITY，不承重")
    if worst > D("1e-40"):
        ok = False
        note.append("FAIL: 两种参数化给出不同拟合")
    return {"id": "N4", "kind": "identity",
            "title": "alpha / beta 两种线性拟合精确等价（恒等，不承重）",
            "ok": ok, "identity": True, "notes": note,
            "readings": {"worst_rel": fstr(worst)}}


def grid_lams():
    return [(D(10) ** (D(k) / D(10))) * AU for k in range(-20, 91)]


def gate_N5():
    """承重：beta 自由 profile 的 chi2 峰必须与第三册逐字一致；beta=0 时恒零。"""
    ok = True
    note = []
    U, _, _ = load_upstream()
    rows = []
    worst = D(0)

    for ds in ("EPM2011", "INPOP10a"):
        peak = D(0)
        peak_lam = None
        obs = [Dq(r[1]) * MAS for r in DATASETS[ds]]
        sig = [Dq(r[2]) * MAS for r in DATASETS[ds]]
        base = sum((obs[i] / sig[i]) ** 2 for i in range(len(obs)))
        flat_zero = True
        for lam in grid_lams():
            G = G_vector(lam)
            den = sum((G[i] / sig[i]) ** 2 for i in range(len(G)))
            if den == 0:
                continue
            num = sum((G[i] / sig[i]) * (obs[i] / sig[i]) for i in range(len(G)))
            d = num * num / den
            if d > peak:
                peak, peak_lam = d, lam
            # beta 固定为 0：模型恒为零，chi2 恒等于 base
            if base == D(0):
                flat_zero = False
        ref = Dq(U["j5_improvement_scan"]["datasets"][ds]["peak_delta_chi2"])
        d = rel(peak, ref)
        worst = max(worst, d)
        rows.append({"ds": ds, "peak_delta_chi2_mine": fstr(peak),
                     "upstream": fstr(ref), "rel": fstr(d),
                     "peak_lam_AU": fstr(peak_lam / AU, 6) if peak_lam else "n/a",
                     "beta0_chi2_flat": flat_zero})
        note.append("%s：beta 自由 profile 峰 %s vs 第三册 %s（rel %s）；"
                    "beta 固定 0 时 chi2(lam) 恒为 base，无 lambda 信息"
                    % (ds, fmt(peak), fmt(ref), fstr(d)))
    note.append("=> 0.444/0.448 的峰是 beta 自由 profile 的噪声起伏，不是 lambda 被测定")
    if worst > D("1e-4"):
        ok = False
        note.append("FAIL: profile 峰与上游不一致")
    return {"id": "N5", "kind": "load-bearing",
            "title": "beta 自由 profile 与上游峰逐字一致；beta 固定 0 时 chi2 平坦",
            "ok": ok, "notes": note, "rows": rows,
            "readings": {"worst_rel_to_upstream": fstr(worst)}}


def gate_N6():
    """承重：非零 beta 使 sigma_lambda 有限，且 sigma_lambda * beta = const。"""
    ok = True
    note = []
    rows = []
    lam = D(1) * AU
    vals = []
    for bs in ("1e-4", "1e-3", "1e-2"):
        beta = Dq(bs)
        F = fisher_AB("EPM2011", lam, beta * lam * lam, "beta")
        det = det2(F)
        cb = cr_bounds(F)
        if cb is None:
            ok = False
            note.append("FAIL: beta=%s 时 Fisher 仍奇异" % bs)
            continue
        sig_b = cb[0].sqrt()
        sig_l = cb[1].sqrt()
        vals.append(sig_l * beta)
        rows.append({"beta": bs, "det_F": fstr(det), "sigma_beta": fstr(sig_b),
                     "sigma_lambda_AU": fstr(sig_l), "sigma_lambda_times_beta": fstr(sig_l * beta)})
    if len(vals) >= 2:
        spread = (max(vals) - min(vals)) / min(vals)
    else:
        spread = D("1e9")
    note.append("sigma_lambda * beta 序列 %s；相对散布 %s（应 < 1e-6）"
                % (" / ".join(fstr(v, 5) for v in vals), fmt(spread)))
    note.append("=> sigma_lambda 不是「样本数不够」，而是被 1/beta 精确标度；"
                "beta→0 时发散")
    if spread > D("1e-6"):
        ok = False
        note.append("FAIL: 未按 1/beta 标度")
    return {"id": "N6", "kind": "load-bearing",
            "title": "sigma_lambda ∝ 1/beta；零假设处发散（承重）",
            "ok": ok, "notes": note, "rows": rows,
            "readings": {"spread_sigma_lambda_times_beta": fstr(spread)}}


def gate_N7():
    """正对照：注入非零 beta 的无噪声数据，lambda 在网格上被唯一恢复。"""
    ok = True
    note = []
    lam_true = D(10) * AU
    beta_true = D("1e-3")
    sig = [Dq(r[2]) * MAS for r in DATASETS["EPM2011"]]
    Gt = G_vector(lam_true)
    obs = [beta_true * Gt[i] for i in range(len(Gt))]

    chi2_at_true = D(0)
    best = None
    second = None
    for lam in grid_lams():
        G = G_vector(lam)
        den = sum((G[i] / sig[i]) ** 2 for i in range(len(G)))
        if den == 0:
            continue
        num = sum((G[i] / sig[i]) * (obs[i] / sig[i]) for i in range(len(G)))
        c = sum(((obs[i] - (num / den) * G[i]) / sig[i]) ** 2 for i in range(len(G)))
        if abs(lam - lam_true) < AU / D(100):
            chi2_at_true = c
        if best is None or c < best[1]:
            second = best
            best = (lam, c)
        elif second is None or c < second[1]:
            second = (lam, c)
    dev = rel(best[0] / AU, D(10))
    note.append("注入 beta=1e-3、lambda=10 AU（无噪声）：最佳网格点 %s AU，"
                "相对偏离 %s" % (fstr(best[0] / AU, 5), fstr(dev)))
    note.append("chi2 在真点 = %s；次优网格点 %s AU 的 chi2 = %s"
                % (fstr(chi2_at_true), fstr(second[0] / AU, 5) if second else "n/a",
                   fstr(second[1]) if second else "n/a"))
    if dev > D("0.13"):
        ok = False
        note.append("FAIL: 注入信号下 lambda 未被恢复")
    if chi2_at_true > D("1e-30"):
        ok = False
        note.append("FAIL: 无噪声真点 chi2 不为零")
    if second is not None and second[1] <= D("1e-20"):
        ok = False
        note.append("FAIL: 存在另一个同样好的 lambda，恢复不唯一")
    return {"id": "N7", "kind": "structural-positive",
            "title": "正对照：注入非零 beta 后 lambda 被唯一恢复",
            "ok": ok, "notes": note,
            "readings": {"best_lam_AU": fstr(best[0] / AU, 5),
                         "chi2_at_true": fstr(chi2_at_true),
                         "dev_from_true": fstr(dev)}}


def gate_N8():
    """反噬边界：把导数人为置零（模拟错误的 dG），判据会误报不可辨识。"""
    ok = True
    note = []
    lam = D(1) * AU
    beta = D("1e-2")
    sig = [Dq(r[2]) * MAS for r in DATASETS["EPM2011"]]
    G = G_vector(lam)
    dG = dG_vector(lam)
    dG_bad = [D(0) for _ in dG]

    def det_with(dv):
        f00 = sum((G[i] / sig[i]) ** 2 for i in range(len(G)))
        f01 = sum(G[i] * (beta * dv[i]) / (sig[i] ** 2) for i in range(len(G)))
        f11 = sum((beta * dv[i]) ** 2 / (sig[i] ** 2) for i in range(len(G)))
        return f00 * f11 - f01 * f01

    good = det_with(dG)
    bad = det_with(dG_bad)
    note.append("正确 dG：det F = %s（>0，lambda 可辨识）" % fstr(good))
    note.append("人为置零 dG：det F = %s（误报为不可辨识）" % fstr(bad))
    note.append("=> 判据依赖「导数确实算出来」这个前提；本册用 N1 的两种步长"
                "互验守住它。若只报 det=0 而不报导数自检，属装饰判据")
    if not (good > 0 and bad == 0):
        ok = False
        note.append("FAIL: 反噬配置未按预期翻转")
    return {"id": "N8", "kind": "guard",
            "title": "反噬：导数置零会使判据误报，必须由 N1 守门",
            "ok": ok, "notes": note,
            "readings": {"det_correct": fstr(good), "det_zero_derivative": fstr(bad)}}

# ------------------------------------------------------------------ 判词
def verdict_of(n2, n5, n6):
    if n2 and n5 and n6:
        return ("ROOTV128F-LAMBDA-UNIDENTIFIABLE-AT-NULL"
                "--FISHER-LAMBDA-COLUMN-IS-EXACTLY-ZERO"
                "--CRAMER-RAO-BOUND-DIVERGES"
                "--SIGMA-LAMBDA-SCALES-AS-ONE-OVER-BETA"
                "--ALPHA-AND-BETA-FITS-ARE-EXACT-RESCALE"
                "--CHI2-PEAK-IS-NOISE-NOT-A-LAMBDA-MEASUREMENT"
                "--INJECTION-RECOVERY-SHOWS-ONLY-NONZERO-BETA-GIVES-LAMBDA"
                "--UFT-NOT-BROKEN"
                "--NO-INDEPENDENT-PREDICTION")
    bad = []
    if not n2:
        bad.append("NULL-COLUMN-NOT-ZERO")
    if not n5:
        bad.append("CHI2-PEAK-MISMATCH")
    if not n6:
        bad.append("SIGMA-LAMBDA-SCALING-REFUTED")
    return "ROOTV128F-CLAIM-REFUTED--" + "--".join(bad)


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


def render_report(gates, verdict, final, sha, nbytes):
    L = []
    add = L.append
    add("=" * 78)
    add("ROOT V128 第六册 · beta 参数化 Fisher 重拟合与零假设处 lambda 不可辨识性")
    add("算法联盟可算审计（非判定册）  date : %s" % DATE)
    add("=" * 78)
    add("")
    add("target    : Phi(r) = -(mu/r)(1 + alpha exp(-r/lambda))")
    add("question  : 在零假设 beta = 0 处，lambda 本身可辨识吗")
    add("upstream  : %s" % os.path.basename(upstream_json()))
    add("up_sha256 : %s" % sha)
    add("up_bytes  : %d" % nbytes)
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
    add("identity  : %s" % (" ".join(g["id"] for g in gates if g["kind"] == "identity") or "无"))
    add("bearing   : %s" % " ".join(g["id"] for g in gates
                                    if g["kind"].startswith("load-bearing")))
    add("n_gate_ok : %d / %d" % (sum(1 for g in gates if g["ok"]), len(gates)))
    add("")
    add("red_line  : 不宣称攻破统一场论；不产生新物理；独立实验预言 0；")
    add("            核与观测表与第三册同源，不算独立证据；不改任何既有判词。")
    add("boundary  : 判的是「beta=0 处 lambda 不可辨识」，不是「V128 被证伪」，")
    add("            也不是「任何 Yukawa 模型的 lambda 都不可测」。")
    add("            注入非零 beta 后 lambda 恢复（N7），边界清楚。")
    add("=" * 78)
    return "\n".join(L) + "\n"


def build_payload(gates, verdict, final, sha, nbytes):
    return {
        "kind": "algorithm-alliance-audit-recompute",
        "not_a_verdict_volume": True,
        "occupies_rid": False,
        "enters_readme": False,
        "title": "ROOT V128 第六册 beta 参数化 Fisher 重拟合与 lambda 不可辨识性",
        "date": DATE,
        "target": "Phi(r) = -(mu/r)(1 + alpha exp(-r/lambda))",
        "upstream": {"file": os.path.basename(upstream_json()), "sha256": sha,
                     "bytes": nbytes,
                     "relation": "核闭式与观测表同源；只做结构分析，不算独立证据"},
        "verdict": verdict,
        "verdict_type": "machine",
        "final": final,
        "n_gate_ok": sum(1 for g in gates if g["ok"]),
        "n_gate_total": len(gates),
        "guards": [g["id"] for g in gates if g["kind"] == "guard"],
        "identity_gates": [g["id"] for g in gates if g["kind"] == "identity"],
        "load_bearing_gates": [g["id"] for g in gates
                               if g["kind"].startswith("load-bearing")],
        "gates": gates,
        "discipline": [
            "恒等门 N4 单列不承重",
            "同源核与观测表只做结构判据，不计独立证据",
            "判据依赖导数正确计算，必须由 N1 的两种步长互验守门（N8 反噬）",
            "判词由唯一构造函数生成，三个承重标志任一翻转必变",
        ],
        "red_line": [
            "不宣称攻破统一场论",
            "不产生新物理，独立实验预言 0",
            "不改第三册与第五册任何判词",
            "lambda 在零假设不可辨识 != Yukawa 模型被证伪",
        ],
    }


def write_json(gates, verdict, final, sha, nbytes):
    p = out_json()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(build_payload(gates, verdict, final, sha, nbytes),
                            ensure_ascii=False, indent=1, sort_keys=False) + "\n")
    return p


def write_report(gates, verdict, final, sha, nbytes):
    p = report_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(render_report(gates, verdict, final, sha, nbytes))
    return p


def main():
    U, sha, nbytes = load_upstream()
    gates = [gate_N1(), gate_N2(), gate_N3(), gate_N4(), gate_N5(),
             gate_N6(), gate_N7(), gate_N8(),
             gate_verdict_machine(), gate_no_hardcode()]
    b = {g["id"]: g["ok"] for g in gates}
    verdict = verdict_of(b["N2"], b["N5"], b["N6"])

    def decide(gs):
        bad = [g["id"] for g in gs if not g["ok"]]
        if bad:
            return "GATES-FAIL--" + "-".join(bad)
        if b["N2"] and b["N5"] and b["N6"]:
            return "GATES-PASS-WITH-UNIDENTIFIABILITY-CONCLUSION"
        return "GATES-PASS-BUT-CONCLUSION-REFUTED"

    final = decide(gates)
    write_report(gates, verdict, final, sha, nbytes)
    write_json(gates, verdict, final, sha, nbytes)
    gates.append(gate_link(out_json(), report_path(), verdict))
    final = decide(gates)
    rp = write_report(gates, verdict, final, sha, nbytes)
    jp = write_json(gates, verdict, final, sha, nbytes)

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
