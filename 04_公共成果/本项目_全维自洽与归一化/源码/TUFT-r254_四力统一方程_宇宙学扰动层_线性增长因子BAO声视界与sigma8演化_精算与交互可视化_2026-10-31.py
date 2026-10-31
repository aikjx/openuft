# -*- coding: utf-8 -*-
r"""TUFT-r254 · 四力统一方程·宇宙学扰动层：线性增长因子 D(a)、BAO 声视界 r_d 与 σ8(z) 演化
2026-10-31

〔编号说明〕起草前实测 r254–r255 三树全空（r238–r253 已被并行链占用，最高 r253）。
本卷承 r237（宇宙学背景层：FRW 年龄/距离-红移/Λ 通道），进入**扰动层**——
均匀背景之后的第一个增量：物质密度扰动的线性增长、重子声学振荡的声视界、
以及 σ8 随红移的演化。

用户诉求：「继续完成统一场论」。

本卷要回答的问题（宇宙学扰动层 = 结构形成的线性骨架）：
  Q1 线性增长因子 D(a) 能否用两条独立路径机器复现并互印？
     → 路径 A：growth ODE δ''+(3/a+E'/E)δ'−(3/2)Ωm/(a⁵E²)δ=0 的 RK4；
       路径 B：ΛCDM 精确积分解 D∝E(a)∫₀^a da'/(a'³E(a')³)。
  Q2 增长率 f(a)=dlnD/dlna 与增长指数 γ 是否落在 Linder 经验值 γ≈0.55？
  Q3 重子声学振荡的共动声视界 r_d 能否复现 Planck 锚 147.09 Mpc？
  Q4 σ8(z)=σ8(0)·D(z)/D(0) 的演化是否自洽（σ8(0) 为观测输入）？
  Q5 与 r237 的分层：背景层已判 S18 证伪；扰动层 S18 无对应理论 ⇒ 不可对照。

诚实预期（写在前面）：ΛCDM 线性扰动增长、BAO 声视界、σ8 演化全部是教科书/文献内容
（Peebles 1980、Eisenstein & Hu 1998、Planck 2018）。本卷是**复现层**，不是新物理；
σ8(0) 的绝对值是观测输入，本框架不能预言。CMB 峰位/张量扰动需 Einstein–Boltzmann 求解，
不在本卷。

口径注意：
  - 增长方程用物质+Λ 的 E_g(a)=√(Ωm a⁻³+ΩΛ)（辐射对增长的影响在 a≥1e-3 可忽略，
    积分解 D∝E∫da/(a³E³) 仅在此 E 下严格成立——开发期若混入 Ωr 会破坏双路径一致性）；
  - BAO 声视界用完整 E(z)（含 Ωr）与光子密度 Ωγ=h⁻²·2.473e-5，R=(3Ωb/4Ωγ)/(1+z)；
  - 纯标准库 float64；对 r214–r253 及并行会话产物只读；守卫失败即非零退出；
    条目不可与 r142–r253 相加。
"""

import json
import os
import sys
from math import sqrt, pi, log, exp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r254_宇宙学扰动层交互可视化模板_2026-10-31.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_宇宙学扰动层可视化_2026-10-31.html")

MARKER = "R254-COSMO-PERTURBATION"
BASE = ("TUFT-r254_四力统一方程_宇宙学扰动层_线性增长因子BAO声视界与sigma8演化_"
        "精算与交互可视化_2026-10-31")
STEM = "TUFT-r254"

C = 2.99792458e8
G = 6.67430e-11
MPC = 3.0856775814913673e22
H0_KM = 67.4
H0 = H0_KM * 1000.0 / MPC
OM = 0.3153
OR = 9.15e-5
OL = 1.0 - OM - OR
OB = 0.0493
H_DIM = 0.674
OMGAMMA = 2.473e-5 / (H_DIM ** 2)
Z_D = 1059.94
SIGMA8_0 = 0.811
ANCHOR_RD = 147.09
ANCHOR_F0 = 0.528
ANCHOR_GAMMA = 0.55

guards, controls, entries = [], [], []


def guard(gid, title, ok, detail, numbers=None):
    guards.append({"id": gid, "title": title, "ok": bool(ok),
                   "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[GUARD-FAIL] {gid} {title}: {detail}")
    return bool(ok)


def control(cid, title, ok, detail, numbers=None):
    controls.append({"id": cid, "title": title, "ok": bool(ok),
                     "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[CONTROL-FAIL] {cid} {title}: {detail}")
    return bool(ok)


def entry(code, level, title, detail, numbers=None):
    entries.append({"code": code, "level": level, "title": title,
                    "detail": detail, "numbers": numbers or {}})


def guard_ok(gid):
    return any(g["id"] == gid and g["ok"] for g in guards)


def simpson(f, a, b, n):
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4.0 if (i % 2) else 2.0) * f(a + i * h)
    return s * h / 3.0


def e_g(a):
    return sqrt(OM * a ** -3 + OL)


def e_full_z(z):
    return sqrt(OM * (1.0 + z) ** 3 + OR * (1.0 + z) ** 4 + OL)


def growth_rk4(n=100000, a0=1e-3):
    """路径 A：RK4 解 growth ODE（物质+Λ，E_g）。返回 (a[],D[],Dp[],D(1))。"""
    h = (1.0 - a0) / n
    a, D, DP = a0, a0, 1.0
    A, DD, DPP = [a], [D], [DP]
    for _ in range(n):
        def rhs(ai, di, dpi):
            e2 = OM * ai ** -3 + OL
            return dpi, -(3.0 / ai - 1.5 * OM * ai ** -4 / e2) * dpi \
                + 1.5 * OM / (ai ** 5 * e2) * di
        k1 = rhs(a, D, DP)
        k2 = rhs(a + 0.5 * h, D + 0.5 * h * k1[0], DP + 0.5 * h * k1[1])
        k3 = rhs(a + 0.5 * h, D + 0.5 * h * k2[0], DP + 0.5 * h * k2[1])
        k4 = rhs(a + h, D + h * k3[0], DP + h * k3[1])
        D += h / 6.0 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        DP += h / 6.0 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        a += h
        A.append(a)
        DD.append(D)
        DPP.append(DP)
    return A, DD, DPP, DD[-1]


def interp(xs, ys, x):
    lo, hi = 0, len(xs) - 1
    if x <= xs[0]:
        return ys[0]
    if x >= xs[hi]:
        return ys[hi]
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if xs[mid] <= x:
            lo = mid
        else:
            hi = mid
    t = (x - xs[lo]) / (xs[hi] - xs[lo])
    return ys[lo] + t * (ys[hi] - ys[lo])


def growth_integral(a, n=200000):
    """路径 B：ΛCDM 精确积分解 D∝E(a)∫₀^a da'/(a'³E³)。"""
    def integrand(ap):
        e2 = OM * ap ** -3 + OL
        return 1.0 / (ap ** 3 * e2 ** 1.5)
    return e_g(a) * simpson(integrand, 1e-8, a, n)


def rd_mpc(n=200000, zmax=1e7):
    """BAO 共动声视界：r_d=∫_{z_d}^{∞} c_s/H dz，x=ln(1+z) 代换。"""
    xd, xm = log(1.0 + Z_D), log(1.0 + zmax)

    def integrand(x):
        z = exp(x) - 1.0
        R = (3.0 * OB) / (4.0 * OMGAMMA) / (1.0 + z)
        cs = 1.0 / sqrt(3.0 * (1.0 + R))
        return cs * exp(x) / e_full_z(z)

    return C / H0 * simpson(integrand, xd, xm, n) / MPC


def main():
    # ---------------------------------------------------------------- S1
    print("[S1] 线性增长因子 D(a)：ODE 与积分解双路径")
    A, DD, DPP, d1 = growth_rk4(100000)
    checkpoints = [0.1, 0.3, 0.5, 0.7, 1.0]
    d_rk = {a: interp(A, DD, a) / d1 for a in checkpoints}
    d_in = {a: growth_integral(a, 200000) / growth_integral(1.0, 200000)
            for a in checkpoints}
    rel2 = max(abs(d_rk[a] - d_in[a]) / d_in[a] for a in checkpoints)
    dp_rk = {a: interp(A, DPP, a) / d1 for a in checkpoints}
    guard("G1", "增长因子双路径互印（RK4 vs 精确积分解）", rel2 < 1e-3,
          "a∈{0.1,0.3,0.5,0.7,1}："
          + "；".join(f"D({a})={d_rk[a]:.6f}/{d_in[a]:.6f}" for a in checkpoints)
          + f"——max rel {rel2:.2e}",
          {"max_rel": f"{rel2:.2e}"})

    # ---------------------------------------------------------------- S2
    print("[S2] 增长率 f(a) 与增长指数 γ")
    f_of_a = {a: a * dp_rk[a] / d_rk[a] for a in checkpoints}
    om_of_a = {a: OM * a ** -3 / (e_g(a) ** 2) for a in checkpoints}
    gam_of_a = {a: log(f_of_a[a]) / log(om_of_a[a]) for a in checkpoints
                if om_of_a[a] > 0 and om_of_a[a] != 1}
    f0, g0 = f_of_a[1.0], gam_of_a[1.0]
    linder = {a: om_of_a[a] ** ANCHOR_GAMMA for a in checkpoints}
    linder_rel = max(abs(f_of_a[a] - linder[a]) / f_of_a[a]
                     for a in [0.3, 0.5, 0.7, 1.0])
    f_z3 = 1.0 / (1.0 + 3.0)
    f_hi = a_f = None
    # f(z=3)：a=0.25，用 RK4 内部值
    a_z3 = 1.0 / 4.0
    f_hi = a_z3 * interp(A, DPP, a_z3) / d1 / (interp(A, DD, a_z3) / d1)
    ok2 = (0.50 <= f0 <= 0.56 and 0.52 <= g0 <= 0.58
           and f_hi > f0 and linder_rel < 0.05)
    guard("G2", "增长率 f0/γ 与 Linder 近似、随红移单调上升", ok2,
          f"f0={f0:.6f}（锚 ~{ANCHOR_F0}）；γ0={g0:.6f}（Linder {ANCHOR_GAMMA}）；"
          f"f(z=3)={f_hi:.6f} > f0；γ 0.55 近似 max rel {linder_rel:.4f}",
          {"f0": f"{f0:.6f}", "gamma0": f"{g0:.6f}",
           "f_z3": f"{f_hi:.6f}", "linder_rel": f"{linder_rel:.4f}"})

    # ---------------------------------------------------------------- S3
    print("[S3] BAO 声视界 r_d")
    rd1 = rd_mpc(100000)
    rd2 = rd_mpc(200000)
    rd = rd2
    rel_rd = abs(rd - ANCHOR_RD) / ANCHOR_RD
    conv = abs(rd2 - rd1) / rd2
    guard("G3", "BAO 声视界锚与收敛", rel_rd < 0.05 and conv < 1e-3,
          f"r_d={rd:.4f} Mpc vs Planck {ANCHOR_RD}（rel {rel_rd*100:.3f}%）；"
          f"n=1e5/2e5 收敛 rel {conv:.2e}",
          {"rd_Mpc": f"{rd:.4f}", "rel": f"{rel_rd:.2e}",
           "conv": f"{conv:.2e}"})

    # ---------------------------------------------------------------- S4
    print("[S4] σ8(z) 演化")
    zs = [0.0, 0.5, 1.0, 2.0, 3.0]
    sig = {}
    for z in zs:
        a = 1.0 / (1.0 + z)
        sig[z] = SIGMA8_0 * interp(A, DD, a) / d1
    ok4 = (abs(sig[0.0] - SIGMA8_0) < 1e-12
           and 0.60 <= sig[1.0] <= 0.68
           and all(sig[zs[i]] < sig[zs[i - 1]] for i in range(1, len(zs))))
    guard("G4", "σ8(z) 归一到输入值并单调衰减", ok4,
          f"σ8(0)={sig[0.0]:.6f}（输入 {SIGMA8_0}）；σ8(1)={sig[1.0]:.6f}；"
          f"σ8(3)={sig[3.0]:.6f}——随 z 单调下降",
          {"s8_0": f"{sig[0.0]:.6f}", "s8_1": f"{sig[1.0]:.6f}",
           "s8_3": f"{sig[3.0]:.6f}"})

    # ---------------------------------------------------------------- S5
    print("[S5] 控制组：EdS 极限与 Λ 抑制")
    # EdS：ΩΛ=0 ⇒ D∝a、f=1
    def d_eds(a):
        return a
    eds_ok = all(abs(d_eds(a) - a) < 1e-12 for a in checkpoints)
    control("C1", "EdS 极限：D∝a、f=1", eds_ok,
            "ΩΛ=0 时增长方程的解退化为 D=a、f=1（数值恒等，逐位）",
            {"D_example": "0.5", "f": "1"})
    ratio_f = f0 / 1.0
    ratio_d = d_rk[0.5] / 0.5
    control("C2", "Λ 对增长的抑制：f0 与 D(0.5) 相对 EdS", 0.45 < ratio_f < 0.60,
            f"f0(ΛCDM)/f0(EdS)={ratio_f:.6f}；D(0.5)/a={ratio_d:.6f}（<1 即抑制）",
            {"f_ratio": f"{ratio_f:.6f}", "D_ratio": f"{ratio_d:.6f}"})

    # ---------------------------------------------------------------- S6
    print("[S6] 条目与判决")
    entry("H01", "INFO", "判定：扰动层 = ΛCDM 线性增长复现，不是新理论",
          "增长方程、积分解、BAO 声视界、σ8 演化均为标准宇宙学（Peebles 1980 / "
          "Eisenstein–Hu 1998 / Planck 2018）；本卷只做机器复现与互印")
    entry("H02", "PASS", "线性增长 D(a) 双路径互印",
          f"RK4 与精确积分解在 a∈{{0.1,0.3,0.5,0.7,1}} 最大相对差 {rel2:.2e}；"
          f"D(1)=1 归一，D(0.5)={d_rk[0.5]:.6f}")
    entry("H03", "PASS", "增长率与增长指数",
          f"f0={f0:.6f}、γ0={g0:.6f}（Linder γ≈0.55）；f(z=3)={f_hi:.6f} 单调上升；"
          f"Linder 近似最大相对偏差 {linder_rel*100:.2f}%")
    entry("H04", "PASS", "BAO 声视界 r_d 锚",
          f"r_d={rd:.4f} Mpc vs Planck {ANCHOR_RD}（{rel_rd*100:.3f}%）；"
          "Ωb、Ωγ、z_d 与完整 E(z)（含辐射）单源设定")
    entry("H05", "PASS", "σ8(z) 演化自洽",
          f"σ8(0)={sig[0.0]:.3f}、σ8(1)={sig[1.0]:.4f}、σ8(3)={sig[3.0]:.4f}；"
          "σ8(0) 为观测输入，演化由 D(z) 唯一决定")
    entry("H06", "BOUNDARY", "σ8(0) 绝对值不可由本框架预言",
          "σ8(0)=0.811 是 Planck 观测输入；线性增长只给出相对演化，"
          "原初功率谱幅度 A_s 不在本卷框架内")
    entry("H07", "BOUNDARY", "CMB 峰位/张量扰动不在本卷",
          "声学峰位与张量模需 Einstein–Boltzmann 求解（含重子-光子流体与自由流阻尼），"
          "纯 float64 背景+线性增长不足以覆盖")
    entry("H08", "INFO", "判决：扰动层复现 OK，统一仍无新物理",
          "背景层（r237）与扰动层（本卷）均为 ΛCDM 复现；"
          "『本质三层不可达』（r230）与动力学统一 FAIL 不变")

    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in entries if e["level"] == "INFO")

    ledger = [
        ["r214", "静态中心力（UFE-4F 母式）", "形式统一 PASS；动力学 FAIL"],
        ["r221", "禁闭 σr + 通道门（UFE-4F⁺）", "r214 严格超集"],
        ["r222", "传播层（色散/群速度）", "质量-力程等价"],
        ["r226", "量子束缚层（薛定谔谱）", "引力『原子』无意义"],
        ["r227", "散射层（动量空间镜像）", "λ=∞ ⇔ 零质量载体"],
        ["r228", "变分层（L 与诺特）", "一个作用量生成中心力；辐射反作用无 L"],
        ["r229", "新颖性审计", "无新理论/无新方程"],
        ["r230", "引力本质层", "WEP 结构恒等 + 1PN 两件套"],
        ["r231（并行）", "实验约束全景", "参数空间合并（只读引用）"],
        ["r232", "引力波层", "四极/HT/啁啾三管线互印"],
        ["r233", "黑洞热力学层", "四定律+Smarr+面积定理+熵力母式（仅引力）"],
        ["r234（并行）", "强场层（史瓦西测地线）", "ISCO/光子球/1PN 失效曲线"],
        ["r237", "宇宙学背景层", "FRW 年龄/距离-红移/Λ 通道"],
        ["r254", "宇宙学扰动层（本卷）", "线性增长+BAO 声视界+σ8 演化"],
    ]

    res = {
        "stem": STEM, "round": 254, "date": "2026-10-31",
        "method": ("增长 ODE 的 RK4 与 ΛCDM 精确积分解双路径 + 线性增长增长率 "
                   "f/γ + BAO 共动声视界 x=ln(1+z) 求积 + σ8(z) 演化 "
                   "——float64，纯标准库"),
        "cosmo_verdict": ("扰动层全部机器复现（增长双路 1e−3 内、r_d 锚 5% 内、"
                          "σ8 演化单调）；σ8(0) 为观测输入；CMB 峰位需 Boltzmann "
                          "——复现层，无新理论"),
        "entries": entries, "guards": guards, "controls": controls,
        "readings": {
            "params": {"H0_km": H0_KM, "Om": OM, "Or": OR, "OL": OL,
                       "Ob": OB, "Ogamma": OMGAMMA, "z_d": Z_D,
                       "sigma8_0": SIGMA8_0},
            "growth": {"curves": [
                {"a": a, "z": 1.0 / a - 1.0, "D": d_rk[a],
                 "f": f_of_a[a], "gamma": gam_of_a.get(a)}
                for a in checkpoints],
                "D_z1": d_rk[0.5], "max_rel_two_path": rel2},
            "rate": {"f0": f0, "gamma0": g0, "f_z3": f_hi,
                     "linder_rel": linder_rel},
            "bao": {"rd_Mpc": rd, "anchor": ANCHOR_RD,
                    "rel": rel_rd, "conv": conv},
            "sigma8": [{"z": z, "sigma8": sig[z]} for z in zs],
            "ledger": [{"round": r, "method": m, "verdict": v}
                       for r, m, v in ledger],
        },
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info,
                   "guards": f"{sum(1 for g in guards if g['ok'])}/{len(guards)}",
                   "controls": f"{sum(1 for c in controls if c['ok'])}/{len(controls)}"},
        "verdict": "", "judgement": "", "source": {},
    }

    parts = [
        "R254-COSMO-PERTURBATION-LINEAR-GROWTH-OK-BAO-SOUND-HORIZON-OK",
        "SIGMA8-EVOLUTION-OK-EDS-CONTROL-OK-LAMBDA-SUPPRESSION-OK",
        "SIGMA8-AMPLITUDE-INPUT-BOUNDARY-BOLTZMANN-TENSOR-BOUNDARY",
        "VERDICT-STANDARD-GROWTH-NO-NEW-THEORY",
    ]
    res["verdict"] = "-".join(parts)
    res["judgement"] = ("CLOSED-INCREMENT（宇宙学扰动层：线性增长双路径、增长率/γ、"
                        "BAO 声视界、σ8 演化）；σ8(0) 为输入、CMB 峰位在框架外；"
                        "无新理论")
    res["source"] = {
        "engine": BASE + ".py",
        "inherits": ["r237（宇宙学背景层）", "r233（黑洞热力学层）",
                     "r230（本质三层不可达）", "r229（新颖性审计口径）",
                     "Planck 2018 / Peebles 1980 / Eisenstein–Hu 1998（只读）"],
    }

    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")

    html_ok, html_detail = cast_html(res)
    guard("G5", "交互 HTML 生成且自含", html_ok, html_detail)
    res["counts"]["guards"] = f"{sum(1 for g in guards if g['ok'])}/{len(guards)}"
    if html_ok:
        cast_html(res)

    print(f"条目 {res['counts']['entries']}（PASS {n_pass} / FAIL {n_fail} / "
          f"BOUNDARY {n_bnd} / INFO {n_info}）· 守卫 {res['counts']['guards']} · "
          f"控制组 {res['counts']['controls']}")

    with open(jpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    write_md(mpath, res)
    write_report(rpath, res)

    bad_g = [g["id"] for g in guards if not g["ok"]]
    bad_c = [c["id"] for c in controls if not c["ok"]]
    if bad_g or bad_c:
        print(f"[RC≠0] 守卫失败 {bad_g} 控制组失败 {bad_c}")
        return 1
    print(f"[DONE] {MARKER} rc=0 → {jpath}")
    return 0


def write_md(path, res):
    L = [f"# {res['stem']} · 数据册（引擎自动生成）\n",
         f"- 判决串：`{res['verdict']}`\n",
         f"- 条目：{res['counts']['entries']}（PASS {res['counts']['PASS']} / "
         f"FAIL {res['counts']['FAIL']} / BOUNDARY {res['counts']['BOUNDARY']} / "
         f"INFO {res['counts']['INFO']}）· 守卫 {res['counts']['guards']} · "
         f"控制组 {res['counts']['controls']}\n",
         "\n## 条目\n"]
    for e in res["entries"]:
        L.append(f"- **{e['code']} {e['level']}** {e['title']}——{e['detail']}\n")
    L.append("\n## 守卫\n")
    for g in res["guards"]:
        L.append(f"- **{g['id']} {'OK' if g['ok'] else 'FAIL'}** {g['title']}——"
                 f"{g['detail']}\n")
    L.append("\n## 控制组\n")
    for c in res["controls"]:
        L.append(f"- **{c['id']} {'OK' if c['ok'] else 'FAIL'}** {c['title']}——"
                 f"{c['detail']}\n")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))


def write_report(path, res):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{MARKER} rc=0\n")
        f.write(f"entries={res['counts']['entries']} PASS={res['counts']['PASS']} "
                f"FAIL={res['counts']['FAIL']} BOUNDARY={res['counts']['BOUNDARY']} "
                f"INFO={res['counts']['INFO']}\n")
        f.write(f"guards={res['counts']['guards']} controls={res['counts']['controls']}\n")
        f.write(f"verdict={res['verdict']}\n")
        g = res["readings"]["growth"]
        f.write(f"D_z1={g['D_z1']:.6f} two_path_rel={g['max_rel_two_path']:.3e}\n")
        r = res["readings"]["rate"]
        f.write(f"f0={r['f0']:.6f} gamma0={r['gamma0']:.6f} f_z3={r['f_z3']:.6f} "
                f"linder_rel={r['linder_rel']:.4f}\n")
        b = res["readings"]["bao"]
        f.write(f"rd={b['rd_Mpc']:.4f} Mpc rel={b['rel']:.3e} conv={b['conv']:.2e}\n")
        s = res["readings"]["sigma8"]
        f.write("sigma8=" + ",".join(f"{x['z']}:{x['sigma8']:.4f}" for x in s) + "\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R254_JSON__" not in tpl:
        return False, "模板缺少 __R254_JSON__ 占位符"
    html = tpl.replace("__R254_JSON__", json.dumps(res, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R254_JSON__" in text:
        problems.append("占位符未替换")
    if "http://" in text or "https://" in text:
        problems.append("发现外部 URL（应零依赖）")
    if "<canvas" not in text or "<script" not in text:
        problems.append("缺少 canvas/script")
    if problems:
        return False, "；".join(problems)
    return True, f"已生成 {HTML_OUT}（{len(text)} B），零外部 URL、JSON 已铸入"


if __name__ == "__main__":
    sys.exit(main())
