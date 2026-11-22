
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
    def f(l):
        return phi(Dq("sqrt(1+l^2)") if False else (D(1) + l * l).sqrt(),
                   D("1e-3"), D(10))
    e = []
    for n in (100, 200, 400, 800):
        v = simpson(f, D(0), D(20), n)
        e.append(v)
    orders = [(e[i] - e[i + 1]) / (e[i + 1] - e[i + 2]) for i in (0, 1)]
    note.append("积分误差逐次比 = %s / %s（四阶应约 16）" % (fmt(orders[0], 3), fmt(orders[1], 3)))

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
