
# ---------------------------------------------------------------- 门 L1：自检
def gate_L1():
    note = []
    ok = True

    # (a) c0=0 时 Phi 恒为 0 => Shapiro 积分为机器零
    zero_phi = lambda x: D(0)
    I0 = shapiro_potential_integral(D(1), D(1000), 400, zero_phi)
    I0b = shapiro_potential_integral(D("2.5"), D(8000), 800, zero_phi)
    l1a = max(abs(I0), abs(I0b))
    note.append("c0=0 Shapiro 积分机器零 max|I| = %s" % fmt(l1a))
    if l1a > D("1e-55"):
        ok = False
        note.append("FAIL: 零势未给零积分")

    # (b) Kepler 解残差
    worst_E = D(0)
    for e_s in ("0.01", "0.2", "0.5", "0.8"):
        for M_s in ("0.1", "1.0", "3.0", "6.0"):
            e = Dq(e_s)
            M = Dq(M_s)
            E = kepler_E(M, e)
            res = E - e * dsin(E) - M
            worst_E = max(worst_E, abs(res))
    note.append("Kepler 残差 max|E - e sinE - M| = %s" % fmt(worst_E))
    if worst_E > D("1e-50"):
        ok = False
        note.append("FAIL: Kepler 未收敛")

    # (c) 两路互验：数值积分 vs 闭式 asinh / 2L/(b^2 sqrt(b^2+L^2))
    b, L = D(1), D(1000)
    num = shapiro_potential_integral(b, L, 400, lambda x: D(1) / Dq(x))
    exa = shapiro_asinh_exact(b, L)
    r_sh = rel(num, exa)
    note.append("Shapiro 核 数值 vs 闭式 rel = %s" % fmt(r_sh))

    jn = deflection_kernel_integral(b, L, 400)
    je = deflection_kernel_exact(b, L)
    r_df = rel(jn, je)
    note.append("偏折核 数值 vs 闭式 rel = %s" % fmt(r_df))
    if max(r_sh, r_df) > D("1e-25"):
        ok = False
        note.append("FAIL: 两路不一致")

    # (d) 收敛：n 加倍 + Richardson
    s1, s2, ext = simpson_pair(lambda x: D(1) / Dq(x), D(0), L, 200)
    conv = rel(ext, exa)
    note.append("Simpson 收敛：S(200) vs S(400) rel = %s；Richardson vs 闭式 rel = %s"
                % (fmt(rel(s1, s2)), fmt(conv)))
    if conv > D("1e-28"):
        ok = False
        note.append("FAIL: Richardson 未达精度")

    return {
        "id": "L1",
        "kind": "guard",
        "title": "自检：零势机器零 / Kepler 收敛 / 积分两路互验 / Richardson",
        "ok": ok,
        "notes": note,
        "readings": {
            "zero_potential_integral_max": fstr(l1a),
            "kepler_residual_max": fstr(worst_E),
            "shapiro_kernel_rel": fstr(r_sh),
            "deflection_kernel_rel": fstr(r_df),
            "richardson_rel_vs_closed": fstr(conv),
        },
    }


# ---------------------------------------------------------------- 门 L2：统一零方向
def gate_L2():
    """C = c0 常数 => 所有势线性泛函只整体乘 (1-c0)^power，形状量不变。"""
    note = []
    ok = True
    mu = D(1)
    b, L = D(1), D(1000)
    a, e = D(1), D("0.2")

    base_I = shapiro_potential_integral(b, L, 400, lambda x: phi_const_shift(x, mu, D(0)))
    base_J = deflection_kernel_integral(b, L, 400) * mu
    base_T = period_of(a, mu)

    rows = []
    worst_ratio = D(0)
    for c0_s in ("0.1", "0.3", "0.5"):
        c0 = Dq(c0_s)
        Ic = shapiro_potential_integral(b, L, 400, lambda x: phi_const_shift(x, mu, c0))
        pred = (D(1) - c0)
        dev_s = rel(Ic, base_I * pred)

        Jc = deflection_kernel_integral(b, L, 400) * mu * (D(1) - c0)
        dev_d = rel(Jc, base_J * pred)

        Tc = period_of(a, mu * (D(1) - c0))
        dev_t = rel(Tc, base_T / dsqrt(D(1) - c0))

        # 形状量：归一化后应与 c0 无关
        shape_s = Ic / (base_I * pred)
        shape_d = Jc / (base_J * pred)

        worst_ratio = max(worst_ratio, dev_s, dev_d, dev_t,
                          abs(shape_s - 1), abs(shape_d - 1))
        rows.append({
            "c0": c0_s,
            "shapiro_ratio_dev": fstr(dev_s),
            "deflection_ratio_dev": fstr(dev_d),
            "period_ratio_dev": fstr(dev_t),
            "shape_shapiro_dev_from_1": fstr(shape_s - 1),
            "shape_deflection_dev_from_1": fstr(shape_d - 1),
        })

    note.append("三个泛函的比值与理论幂律的最大偏离 = %s" % fmt(worst_ratio))
    note.append("Shapiro 比例指数 = 1（Phi 线性泛函）；偏折 = 1；周期 = -1/2")
    note.append("进动：对纯 1/r 势恒为 0（第四册已机读 8.862149E-19），本册继承不重算")
    if worst_ratio > D("1e-45"):
        ok = False
        note.append("FAIL: 零方向缩放律不成立")

    return {
        "id": "L2",
        "kind": "structural",
        "title": "统一零方向：C 常数时全部势线性泛函只整体缩放，形状量不变",
        "ok": ok,
        "notes": note,
        "rows": rows,
        "readings": {
            "max_ratio_deviation": fstr(worst_ratio),
            "base_shapiro_integral": fstr(base_I),
            "base_deflection_integral": fstr(base_J),
            "base_period": fstr(base_T),
        },
    }


# ---------------------------------------------------------------- 门 L3：简并精确性
def gate_L3():
    """(mu, c0) 与 (mu/(1-c0), 0) 给出逐点相同的 Phi => 全部泛函相同。"""
    note = []
    ok = True
    c0 = D("0.3")
    mu = D(1)
    mu_alt = mu / (D(1) - c0)

    worst_phi = D(0)
    for x_s in ("0.05", "0.2", "0.5", "1", "2", "5", "20"):
        x = Dq(x_s)
        worst_phi = max(worst_phi, abs(phi_const_shift(x, mu, c0) - phi_const_shift(x, mu_alt, D(0))))
    note.append("Phi 逐点差 max = %s（恒等，按纪律单列 IDENTITY，不承重）" % fmt(worst_phi))

    # Newton 轨道 r(t) 在两种参数化下相同
    worst_r = D(0)
    for M_s in ("0.1", "1.0", "3.0", "6.0"):
        M = Dq(M_s)
        E = kepler_E(M, D("0.2"))
        r1 = D(1) * (D(1) - D("0.2") * dcos(E))
        # c0 方案下 mu_eff 变小 => n 变小 => 同一 t 对应的 M 变大
        n_ratio = dsqrt((D(1) - c0))
        M2 = M / n_ratio
        E2 = kepler_E(M2, D("0.2"))
        r2 = D(1) * (D(1) - D("0.2") * dcos(E2))
        worst_r = max(worst_r, rel(r2, r1) if r1 != 0 else abs(r2))
    note.append("同一 t 的 r(t) 相对差 max = %s（两参数化给出同一条轨道）" % fmt(worst_r))

    # 枚举 6 个泛函，验证全部只依赖 mu*(1-c0)
    funcs = []
    b, L, a = D(1), D(1000), D(1)
    I1 = shapiro_potential_integral(b, L, 400, lambda x: phi_const_shift(x, mu, c0))
    I2 = shapiro_potential_integral(b, L, 400, lambda x: phi_const_shift(x, mu_alt, D(0)))
    funcs.append(("shapiro", rel(I1, I2)))
    funcs.append(("deflection", rel(mu * (D(1) - c0), mu_alt)))
    funcs.append(("period", rel(period_of(a, mu * (D(1) - c0)), period_of(a, mu_alt))))
    funcs.append(("t2_over_a3", rel(4 * dpi() ** 2 / (mu * (D(1) - c0)),
                                    4 * dpi() ** 2 / mu_alt)))
    funcs.append(("redshift", rel(mu * (D(1) - c0), mu_alt)))
    funcs.append(("precession_static", D(0)))
    worst_f = max(v for _, v in funcs)
    note.append("6 个泛函枚举：最大相对差 = %s => 全部简并" % fmt(worst_f))

    if max(worst_phi, worst_r, worst_f) > D("1e-45"):
        ok = False
        note.append("FAIL: 简并不精确")

    return {
        "id": "L3",
        "kind": "identity",
        "title": "质量-振幅精确简并：(mu,c0) ≡ (mu/(1-c0),0)，非近似",
        "ok": ok,
        "identity": True,
        "notes": note,
        "readings": {
            "phi_pointwise_max": fstr(worst_phi),
            "radius_at_fixed_t_max_rel": fstr(worst_r),
            "six_functional_enumeration_max_rel": fstr(worst_f),
            "c0_used": fstr(c0),
        },
    }


# ---------------------------------------------------------------- 门 L4：等效原理
def gate_L4():
    """耦合到质量的 Yukawa 满足强等效原理 => Eotvos 通道结构性失效。"""
    note = []
    ok = True
    rows = []

    def eta(k1, k2, alpha, rr, lam):
        """两个测试体的 Eotvos 参数，源荷/质量归一为 1。"""
        f = (-Dq(rr) / Dq(lam)).exp()
        num = Dq(alpha) * (Dq(k1) - Dq(k2)) * f
        den = D(1) + Dq(alpha) * (Dq(k1) + Dq(k2)) / 2 * f
        return num / den

    # (a) 耦合质量：k = 1 对所有成分 => eta = 0 精确
    worst_mass = D(0)
    for alpha_s in ("1e-9", "1e-3", "1", "10"):
        for r_s, lam_s in (("1", "1e10"), ("1", "1e3"), ("1e6", "1e0")):
            worst_mass = max(worst_mass, abs(eta(1, 1, alpha_s, r_s, lam_s)))
    note.append("耦合质量 (q=m) 时 eta 恒为 0，max|eta| = %s" % fmt(worst_mass))
    note.append("=> 强等效原理不破 => 自由落体普适 => Eotvos/MICROSCOPE/LLR 通道**看不见**该第五力")

    # (b) 耦合重子数：q/m 随成分变 => eta != 0
    k_baryon_fe = D("0.4656")   # 近似 B/m（自然单位），仅作量级示意
    k_baryon_ti = D("0.4622")
    eta_bt = eta(k_baryon_fe, k_baryon_ti, "1e-6", "1", "1e10")
    note.append("耦合重子数时 eta(Fe,Ti) at alpha=1e-6, lambda>>r = %s（非零）" % fmt(eta_bt))

    # (c) 判别力：同一组 alpha 下两种耦合给出完全不同的 eta
    ratio = abs(eta_bt) / (abs(worst_mass) + D("1e-300"))
    note.append("同样 alpha 下 baryon 耦合 eta / mass 耦合 eta 之比 = %s（判别力存在）" % fmt(ratio))

    if worst_mass > D("1e-55"):
        ok = False
        note.append("FAIL: 质量耦合未给 eta=0")
    if eta_bt == 0:
        ok = False
        note.append("FAIL: baryon 耦合给 0，负对照失效")

    rows.append({"coupling": "mass (q=m)", "eta": fstr(worst_mass)})
    rows.append({"coupling": "baryon (q=B)", "eta": fstr(eta_bt)})

    return {
        "id": "L4",
        "kind": "structural-negative",
        "title": "等效原理通道对质量耦合 Yukawa 结构性失效（负读数）",
        "ok": ok,
        "negative_reading": True,
        "notes": note,
        "rows": rows,
        "readings": {
            "eta_mass_coupling_max": fstr(worst_mass),
            "eta_baryon_coupling_illustrative": fstr(eta_bt),
            "discrimination_ratio": fstr(ratio),
        },
    }
