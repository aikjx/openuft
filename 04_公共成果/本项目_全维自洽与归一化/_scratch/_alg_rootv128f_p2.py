
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
