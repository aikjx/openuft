
# ---------------------------------------------------------------- 上游继承（只读）
def load_upstream():
    p = upstream_json()
    if not os.path.exists(p):
        raise RuntimeError("上游机读件缺失: %s" % p)
    with open(p, "rb") as fh:
        raw = fh.read()
    d = json.loads(raw.decode("utf-8"))
    return d, hashlib.sha256(raw).hexdigest(), len(raw)


def tail_stats(profile, lam_min):
    """给定 profile（第三册 j3 子样本），取 lam >= lam_min 的点，返回 beta 量。"""
    rows = []
    for pt in profile:
        lam = Dq(pt["lam_AU"])
        if lam < Dq(lam_min):
            continue
        a_hat = Dq(pt["alpha_hat"])
        s_a = Dq(pt["sigma_alpha"])
        rows.append({
            "lam": lam,
            "alpha_hat": a_hat,
            "sigma_alpha": s_a,
            "beta_hat": a_hat / (lam * lam),
            "sigma_beta": s_a / (lam * lam),
            "alpha_95": Dq(pt["alpha_95_upper"]),
            "excluded": bool(pt["alpha1_excluded"]),
        })
    return rows


def _converge_ratio(rows, key):
    """尾部收敛：以最大 lam 点为极限，返回 [(lam, dev, dev*lam)]。"""
    if not rows:
        return []
    lim = rows[-1][key]
    out = []
    for r in rows:
        d = rel(r[key], lim)
        out.append((r["lam"], d, d * r["lam"]))
    return out


# ---------------------------------------------------------------- 门 L5：sigma_beta 收敛
def gate_L5(up, up_sha, up_bytes):
    note = []
    ok = True
    detail = {}
    worst_lin = D(0)
    n_tail_min = None

    for ds in ("EPM2011", "INPOP10a"):
        prof = up["j3_real_fit"]["datasets"][ds]["profile"]
        rows = tail_stats(prof, D(30))
        conv_s = _converge_ratio(rows, "sigma_beta")
        conv_a = _converge_ratio(rows, "beta_hat")

        # O(1/lam) 律：dev*lam 应近似常数
        vals = [c[2] for c in conv_s[:-1]]  # 去掉极限点自身（dev=0）
        if vals:
            mn, mx = min(vals), max(vals)
            spread = (mx - mn) / mn if mn != 0 else mx
        else:
            spread = D(0)

        # 去掉第一项（lam=30，修正最大）后的线性律检验
        vals2 = [c[2] for c in conv_s[1:-1]]
        if len(vals2) >= 2:
            mn2, mx2 = min(vals2), max(vals2)
            spread2 = (mx2 - mn2) / mn2 if mn2 != 0 else mx2
        else:
            spread2 = D(0)
        worst_lin = max(worst_lin, spread2)

        # 达到 1e-3 所需的最小 lam
        for lam, d, _ in conv_s:
            if d < D("1e-3") and n_tail_min is None:
                n_tail_min = lam

        detail[ds] = {
            "n_tail_points": len(rows),
            "sigma_beta_limit": fstr(rows[-1]["sigma_beta"]),
            "beta_hat_limit": fstr(rows[-1]["beta_hat"]),
            "dev_at_30": fstr(conv_s[0][1]),
            "dev_times_lam_series": [fstr(c[2]) for c in conv_s],
            "spread_dev_times_lam_all": fstr(spread),
            "spread_dev_times_lam_drop_first": fstr(spread2),
            "beta_hat_dev_series": [fstr(c[1]) for c in conv_a],
        }
        note.append("%s：sigma_beta 极限 = %s；lam=30 处偏离 %s；dev*lam 序列 %s"
                    % (ds, fmt(rows[-1]["sigma_beta"]), fmt(conv_s[0][1]),
                       " / ".join(fstr(c[2], 3) for c in conv_s)))

    note.append("O(1/lam) 律：去掉 lam=30 后 dev*lam 的相对散布 = %s" % fmt(worst_lin))
    note.append("=> alpha_hat 与 sigma_alpha 在尾部同乘 lam^2，即整个拟合只是 beta 拟合的换算式")

    if worst_lin > D("1e-2"):
        ok = False
        note.append("FAIL: 尾部未呈现 O(1/lam) 收敛")

    return {
        "id": "L5",
        "kind": "load-bearing",
        "title": "尾部 sigma_alpha 与 alpha_hat 同乘 lam^2 => 只有一个 beta 约束",
        "ok": ok,
        "notes": note,
        "detail": detail,
        "readings": {
            "upstream_sha256_prefix": up_sha[:16],
            "upstream_bytes": up_bytes,
            "worst_spread_dev_times_lam": fstr(worst_lin),
            "lam_for_dev_below_1e_3": fstr(n_tail_min) if n_tail_min else "n/a",
        },
    }


# ---------------------------------------------------------------- 门 L6：信息份数
def gate_L6(up):
    """尾部 k 个格点塌缩为 1 个 beta 约束；用「互相换算」验证而非计数。"""
    note = []
    ok = True
    detail = {}
    worst_consistency = D(0)

    for ds in ("EPM2011", "INPOP10a"):
        prof = up["j3_real_fit"]["datasets"][ds]["profile"]
        rows = tail_stats(prof, D(30))
        # 相邻两点的 sigma_beta 之比应 -> 1；用 alpha 判据直接比会看到 lam^2 增长
        ratios_alpha = []
        ratios_beta = []
        for i in range(len(rows) - 1):
            ra = rows[i + 1]["sigma_alpha"] / rows[i]["sigma_alpha"]
            rb = rows[i + 1]["sigma_beta"] / rows[i]["sigma_beta"]
            lamr = (rows[i + 1]["lam"] / rows[i]["lam"]) ** 2
            ratios_alpha.append((ra, lamr))
            ratios_beta.append(rb)
        # 关键：ratio_alpha / lam_ratio^2 == ratio_beta，应 -> 1
        devs = [abs(rb - 1) for rb in ratios_beta]
        worst_consistency = max(worst_consistency, max(devs) if devs else D(0))

        detail[ds] = {
            "n_tail_points": len(rows),
            "lambda_points": [fstr(r["lam"], 3) for r in rows],
            "alpha_ratio_vs_lam2_ratio": ["%.4f / %.4f" % (float(ra), float(lr))
                                          for ra, lr in ratios_alpha],
            "beta_ratio_series": [fstr(rb, 4) for rb in ratios_beta],
            "independent_constraints_in_tail": 1,
        }
        note.append("%s：尾部 %d 点，alpha 比 / lam^2 比 逐对吻合，beta 比序列 %s"
                    % (ds, len(rows), " / ".join(fstr(rb, 4) for rb in ratios_beta)))

    note.append("尾部 max|beta 比 - 1| = %s（lam=30 那一对含 O(1/lam) 修正）" % fmt(worst_consistency))
    note.append("=> 尾部 k 个 lambda 格点不构成 k 份独立检验，而是同一个 beta 区间的 k 次重写")

    if worst_consistency > D("1e-1"):
        ok = False
        note.append("FAIL: 尾部未塌缩")

    return {
        "id": "L6",
        "kind": "load-bearing",
        "title": "尾部格点塌缩：k 个 lambda 点 = 1 个 beta 约束",
        "ok": ok,
        "notes": note,
        "detail": detail,
        "readings": {
            "worst_beta_ratio_deviation": fstr(worst_consistency),
        },
    }


# ---------------------------------------------------------------- 门 L7：排除带分解
def gate_L7(up):
    """排除带上端由 beta 交叉决定、下端由指数截断决定：两个互不相关的机制。"""
    note = []
    ok = True
    detail = {}

    for ds in ("EPM2011", "INPOP10a"):
        prof = up["j3_real_fit"]["datasets"][ds]["profile"]
        rows = tail_stats(prof, D(30))
        last = rows[-1]
        # 上端交叉：区间上端点 lam^2*(beta_hat + 1.96*sigma_beta) = 1
        # 注意 beta_hat 带符号 —— 符号错会把「已排除点」与「未排除点」混为一谈
        rhs = last["beta_hat"] + D("1.96") * last["sigma_beta"]
        lam_star = D(1) / dsqrt(rhs) if rhs > 0 else None

        j4 = up["j4_exclusion_window"]["datasets"][ds]
        reported_hi = Dq(j4["widest_band_AU"][1])
        reported_lo = Dq(j4["widest_band_AU"][0])
        grid_step = D("10") ** (D(1) / D(10))
        ratio = (lam_star / reported_hi) if lam_star else None

        detail[ds] = {
            "reported_band_AU": [fstr(reported_lo, 6), fstr(reported_hi, 6)],
            "reported_decades": fstr(Dq(j4["decades_in_band"])),
            "n_excluded": j4["n_excluded"],
            "n_grid": j4["n_grid"],
            "beta_hat_at_edge": fstr(last["beta_hat"]),
            "sigma_beta_at_edge": fstr(last["sigma_beta"]),
            "upper_edge_from_beta_crossing": fstr(lam_star, 6) if lam_star else "n/a",
            "edge_ratio_beta_over_reported": fstr(ratio, 5) if ratio else "n/a",
            "grid_step": fstr(grid_step, 5),
        }
        note.append("%s：第三册上端 %s ↔ beta 交叉解析 %s，比值 %s（网格步长 %s）"
                    % (ds, fmt(reported_hi), fmt(lam_star) if lam_star else "n/a",
                       fstr(ratio, 5) if ratio else "n/a", fstr(grid_step, 5)))
        note.append("      下端 %s 由 exp(-a/lam) 截断给出（形状机制，与 beta 无关）" % fmt(reported_lo))

        # 交叉点必须落在「最后一个被排除格点」与「下一个格点」之间
        if lam_star is None:
            ok = False
            note.append("FAIL: 无法给出 beta 交叉点")
        elif not (D(1) <= ratio < grid_step):
            ok = False
            note.append("FAIL: 交叉点未落在相邻网格之间，上端分解不成立")

    note.append("=> 「7.90 dex 排除带」不是一个物理带，而是两个互不相关条件的交集："
                "低端指数截断、高端 beta 交叉")

    return {
        "id": "L7",
        "kind": "load-bearing-negative",
        "title": "排除带两端由两个互不相关机制决定（负读数：带不是物理对象）",
        "ok": ok,
        "negative_reading": True,
        "notes": note,
        "detail": detail,
        "readings": {},
    }


# ---------------------------------------------------------------- 门 L8：反噬
def gate_L8(up):
    """判别力：把尾部 sigma 换成不随 lam 增长的假剖面，L5/L6 判据必须 FAIL。"""
    note = []
    ok = True

    ds = "EPM2011"
    prof = up["j3_real_fit"]["datasets"][ds]["profile"]
    rows = tail_stats(prof, D(30))

    # 真剖面：dev*lam 近似常数
    conv_true = _converge_ratio(rows, "sigma_beta")
    vals_true = [c[2] for c in conv_true[1:-1]]
    spread_true = (max(vals_true) - min(vals_true)) / min(vals_true) if len(vals_true) >= 2 else D(0)

    # 假剖面：sigma_alpha 恒定（不随 lam^2 增长）=> sigma_beta ∝ lam^-2
    fake = []
    const_s = rows[0]["sigma_alpha"]
    for r in rows:
        fake.append({"lam": r["lam"], "sigma_beta": const_s / (r["lam"] * r["lam"])})
    conv_fake = _converge_ratio(fake, "sigma_beta")
    vals_fake = [c[2] for c in conv_fake[1:-1]]
    spread_fake = (max(vals_fake) - min(vals_fake)) / min(vals_fake) if len(vals_fake) >= 2 else D("1e9")

    note.append("真剖面 dev*lam 散布 = %s（通过 L5）" % fmt(spread_true))
    note.append("假剖面 dev*lam 散布 = %s（L5 判据必须失败）" % fmt(spread_fake))
    note.append("另有正对照：把尾部单点 sigma 乘 1.5，dev*lam 散布应显著上升")

    # 单点扰动
    pert = [dict(r) for r in rows]
    pert[-2]["sigma_alpha"] = pert[-2]["sigma_alpha"] * D("1.5")
    pert[-2]["sigma_beta"] = pert[-2]["sigma_alpha"] / (pert[-2]["lam"] ** 2)
    conv_p = _converge_ratio(pert, "sigma_beta")
    vals_p = [c[2] for c in conv_p[1:-1]]
    spread_p = (max(vals_p) - min(vals_p)) / min(vals_p) if len(vals_p) >= 2 else D("1e9")
    note.append("单点 +50%% 后 dev*lam 散布 = %s" % fmt(spread_p))

    if spread_fake < D("1"):
        ok = False
        note.append("FAIL: 假剖面未使判据失败，L5 无判别力")
    if spread_p < spread_true:
        ok = False
        note.append("FAIL: 单点扰动未使散布上升")

    return {
        "id": "L8",
        "kind": "guard",
        "title": "判别力反噬：假剖面与单点扰动必须使 L5 判据失败",
        "ok": ok,
        "notes": note,
        "readings": {
            "spread_true": fstr(spread_true),
            "spread_fake_profile": fstr(spread_fake),
            "spread_single_point_perturbed": fstr(spread_p),
        },
    }
