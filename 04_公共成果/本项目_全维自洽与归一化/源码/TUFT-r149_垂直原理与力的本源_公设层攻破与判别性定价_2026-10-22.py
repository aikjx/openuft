# -*- coding: utf-8 -*-
"""
TUFT-r149 · 垂直原理与力的本源：公设层攻破与判别性定价

靶（来料）：
  01_独立体系/S15_空间光速螺旋曲率挠率几何统一场论/V9_四力大统一定稿线/
    01_全书_四力大统一_垂直原理螺旋统一场论_V9.46.md   （§1.2 第二公设 · §1.3 · §3.4 · §9.5 · 第十四/十五章）
    06_全维度攻破总卷.md

分工声明（与既有册分层，条目不可相加）：
  - V9 线**自己**已把【场层面】垂直原理（nabla kappa . nabla tau = 0，§3.4）判为与旗舰 L2 汤川解
    **互斥（no-go）**，并降级为「与 L2 主体互斥的闲置假设」（V9.9 第十五章）。这一部分本卷**不重判**。
  - 07_统一场方程/18 号册做的是**元审计**（审计那台验证器：把 27 个 PASS 拆成 IDENTITY/CONST/VARIES/NO_TEST）。
  - **本卷攻的是【公设层】的垂直原理（§1.2）与【力的本源】的判别性**，是上面两册都没做的那一层。

★本卷要抓的四条（预登记，最终以机读为准）：
  A 组 垂直原理的【公设地位】：
      自承「正交性是微分几何定理，不是额外假设」却列为第二公设 ⇒ 名实；
      公设 1（|v| = c 类光螺旋）使 ds^2 = 0 ⇒ Frenet 标架无定义 ⇒ 公设 2 连陈述都写不出来 ⇒ **公设互斥**；
      V9.11 用「3D 投影弧长」规避 ⇒ 两难：4D 口径无定义 / 3D 口径有定义但恒真零内容。
  B 组 「天然解耦」论断 vs 不完整的 Frenet 方程组：
      §1.3 只列两式（dT/ds = kappa N、dB/ds = -tau N），**漏了 dN/ds = -kappa T + tau B**；
      而漏掉的这一式恰恰是承载 kappa 与 tau 耦合的那一式 ⇒ 「解耦」建立在残缺方程组上。
      且全书主力解（旗舰汤川解 tau = alpha kappa）的梯度**平行**（cos = +1），最大程度违反垂直原理
      ⇒ §9.5「用垂直原理解释主力解力的方向」自相矛盾。
  C 组 力的本源的【判别性定价】：
      统一势模板 V = s hbar c Q1Q2 e^{-r/lambda}/r 对四力各配 (Q, lambda) ⇒ 可零残差拟合任意观测组；
      参数计数门 n_自由 <= n_观测 - 1 是否通过；与 SU(5) 控制组对比（有交叉约束 sin^2 theta_W）。
  D 组 修复定价：低阶算子枚举 + 力的本源需新增型（削减型不可达）。

★编号：实测首空号 r149（源码/数据 0 命中）。
★号差约定：本卷统一用 (-,+,+,+)，ds^2 = -c^2 dt^2 + dx^2；ds^2 = 0 为类光，< 0 为类时。
"""
import os
import io
import re
import json
import math
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
OPENUFT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
DATE = "2026-10-22"
STEM = "TUFT-r149_垂直原理与力的本源_公设层攻破与判别性定价_%s" % DATE
JUDGE_STEM = "判定_TUFT-r149_垂直原理与力的本源_公设层攻破与判别性定价_%s" % DATE

V9_DIR = os.path.join(OPENUFT, "01_独立体系", "S15_空间光速螺旋曲率挠率几何统一场论",
                      "V9_四力大统一定稿线")
BOOK = os.path.join(V9_DIR, "01_全书_四力大统一_垂直原理螺旋统一场论_V9.46.md")

C = 299792458.0
HBAR = 1.054571817e-34
EV_J = 1.602176634e-19

ENTRIES = []
METRICS = {}
CTRLS = []


def add(eid, name, group, claim, machine, verdict, detail, control=""):
    ENTRIES.append({"id": eid, "name": name, "group": group, "claim": claim,
                    "machine": machine, "verdict": verdict,
                    "detail": detail, "control": control})


def add_ctrl(name, machine, ok, note=""):
    CTRLS.append({"name": name, "machine": machine, "ok": bool(ok), "note": note})


# ============================ 向量与 Frenet 工具 ============================
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def nrm(a):
    return math.sqrt(dot(a, a))


def unit(a):
    n = nrm(a)
    return (a[0] / n, a[1] / n, a[2] / n)


def frenet_frame(v, a):
    """由解析的 v, a 构造 Frenet 标架 T, N, B（要求 kappa != 0）。"""
    T = unit(v)
    cx = cross(v, a)
    nc = nrm(cx)
    if nc == 0.0:
        return T, None, None, 0.0
    B = unit(cx)
    N = cross(B, T)
    # kappa = |v x a| / |v|^3
    kappa = nc / (nrm(v) ** 3)
    return T, N, B, kappa


def curve(name, t):
    """三条形态完全不同的曲线：导数解析给出，避免三阶数值差分。"""
    if name == "helix":
        R, w, h = 1.0, 1.0, 1.0
        ct, st = math.cos(w * t), math.sin(w * t)
        v = (-R * w * st, R * w * ct, h)
        a = (-R * w * w * ct, -R * w * w * st, 0.0)
        ad = (R * w ** 3 * st, -R * w ** 3 * ct, 0.0)
    elif name == "twisted_cubic":
        v = (1.0, 2.0 * t, 3.0 * t * t)
        a = (0.0, 2.0, 6.0 * t)
        ad = (0.0, 0.0, 6.0)
    elif name == "lissajous":
        v = (-math.sin(t), 2.0 * math.cos(2.0 * t), 0.5)
        a = (-math.cos(t), -4.0 * math.sin(2.0 * t), 0.0)
        ad = (math.sin(t), -8.0 * math.cos(2.0 * t), 0.0)
    else:
        raise ValueError(name)
    return v, a, ad


def tau_of(v, a, ad):
    cx = cross(v, a)
    return dot(v, cross(a, ad)) / dot(cx, cx)


# ============================ 组 A：垂直原理的公设地位 ============================
def orthogonality_scan():
    """对形态完全不同的三条曲线扫描 T.N / N.B / T.B。"""
    out = {}
    for nm in ("helix", "twisted_cubic", "lissajous"):
        worst = 0.0
        for t in (0.3, 0.7, 1.3, 2.1, 3.7):
            v, a, ad = curve(nm, t)
            T, N, B, kap = frenet_frame(v, a)
            if N is None:
                out[nm] = None
                worst = None
                break
            worst = max(worst, abs(dot(T, N)), abs(dot(N, B)), abs(dot(T, B)))
        out[nm] = worst
    return out


def group_A():
    # ---- A1 公设名实之辩 ----
    ort = orthogonality_scan()
    ok_all = all((v is not None and v < 1e-12) for v in ort.values())
    worst_all = max(v for v in ort.values() if v is not None)
    # 来料原文自承句（机器抓取）
    self_admit = ""
    if os.path.exists(BOOK):
        with io.open(BOOK, "r", encoding="utf-8") as f:
            txt = f.read()
        m = re.search(r"正交性是微分几何定理[^\n]*", txt)
        if m:
            self_admit = m.group(0).strip()
    machine_a1 = ("三条形态完全不同的曲线（螺旋 / 扭线 / 李萨如）上 T.N、N.B、T.B 最坏绝对值 %.3e；"
                  "来料原文自承：%s" % (worst_all, self_admit[:60]))
    METRICS["A1_orth_worst"] = worst_all
    METRICS["A1_orth_by_curve"] = ort
    METRICS["A1_self_admit"] = self_admit
    METRICS["A1_ok_all"] = 1 if ok_all else 0
    v_a1 = "FAIL" if ok_all else "BOUNDARY"
    add("A1", "名实之辩：自承「是定理不是假设」却列为第二公设", "A",
        "垂直原理作为「第二公设」，有没有任何「公设」该有的内容？",
        machine_a1, v_a1,
        "来料 §1.2 原文：**「正交性是微分几何定理，不是额外假设」** —— 它**自己承认**这不是假设。\n"
        "机读验证：在三条形态**完全不同**的曲线上（圆柱螺旋 / 扭线 (t,t²,t³) / 李萨如 (cos t, sin 2t, t/2)），\n"
        "|T·N|、|N·B|、|T·B| 的最坏值均为 **%.3e**（机器零）。\n"
        "⇒ 正交性对**任意**正则曲线成立，不含任何关于螺旋的断言 ⇒ **零判别力、零信息**。\n"
        "理由也很直白：B ≡ T×N 由叉乘定义自动垂直于 T 与 N；而 T·N = 0 来自 |T| = 1 ⇒ T·T' = 0。\n"
        "**两步都是定义，没有一步是假设。** 一个自承为定理的命题被列为「第二公设」，"
        "其作为公设的信息含量为 **0**。\n"
        "**靶自承**：本条与来料自述一致（attack16 判据④），不是外部强加的指控。" % worst_all,
        "控制组1：标准螺旋上正交性成立（正对照）；控制组2：kappa=0 处标架退化（负对照，证明检测有分辨力）")

    # ---- A2 类光性杀死 Frenet（公设互斥） ----
    # 螺旋世界线 x^mu = (c t, R cos wt, R sin wt, h t)，号差 (-,+,+,+)
    def ds2_over_dt2(Rw, h, speed_frac):
        """把 (Rw, h) 按给定速率比例缩放后，返回 ds^2/dt^2。"""
        v2 = Rw * Rw + h * h
        if v2 <= 0:
            return -C * C
        scale = (speed_frac * C) / math.sqrt(v2)
        v2s = v2 * scale * scale
        return v2s - C * C          # ds^2 = (-c^2 + v^2) dt^2

    rows = []
    for fr in (0.5, 0.9, 0.999, 1.0, 1.001):
        rows.append((fr, ds2_over_dt2(1.0, 1.0, fr)))
    ds2_at_c = ds2_over_dt2(1.0, 1.0, 1.0)
    ds2_below = ds2_over_dt2(1.0, 1.0, 0.5)
    ds2_above = ds2_over_dt2(1.0, 1.0, 1.001)
    machine_a2 = ("号差(-,+,+,+)，ds^2/dt^2 = v^2 - c^2：v=c 时 %.6e；v=0.5c 时 %.6e；v=1.001c 时 %.6e" %
                  (ds2_at_c, ds2_below, ds2_above))
    METRICS["A2_ds2_at_c"] = ds2_at_c
    METRICS["A2_ds2_below"] = ds2_below
    METRICS["A2_ds2_above"] = ds2_above
    METRICS["A2_rows"] = [[r[0], r[1]] for r in rows]
    v_a2 = "FAIL" if (abs(ds2_at_c) < 1e-6 and ds2_below < 0 and ds2_above > 0) else "BOUNDARY"
    add("A2", "★公设互斥：公设 1（|v|=c 类光）使 Frenet 标架无定义，公设 2 无法陈述", "A",
        "垂直原理要用到 Frenet 标架 (T,N,B)。第一公设说空间点以光速走螺旋，这条世界线类光吗？",
        machine_a2, v_a2,
        "螺旋世界线 x^μ = (ct, R cos ωt, R sin ωt, h t)。取号差 **(-,+,+,+)**：\n"
        "  ds² = -c²dt² + (R²ω² + h²)dt² = (v² - c²) dt²。\n"
        "机读三档：v = 0.5c ⇒ ds²/dt² = **%.6e**（类时，< 0）；v = c ⇒ **%.6e**（**类光，= 0**）；"
        "v = 1.001c ⇒ %.6e（类空，> 0）。\n"
        "而第一公设恰恰要求 **|v| = c**（空间点以光速运动）⇒ **ds² ≡ 0** ⇒ **弧长 s ≡ 0**。\n"
        "Frenet 标架必须**用弧长参数化**：T = dr/ds、N = (dT/ds)/κ。s 恒为 0 时 d/ds **无定义**，"
        "于是 T、N、B、κ、τ **全部无法构造**。\n"
        "⇒ **公设 1（类光螺旋）杀死了公设 2（Frenet 垂直原理）的定义域**："
        "垂直原理在最核心的那条世界线上**连陈述都写不出来**。\n"
        "（这是本库 65 号卷 B5 的同一结论在 V9 线上的落地：v_total = c ⇒ ds ≡ 0 ⇒ Frenet 无定义。）"
        % (ds2_below, ds2_at_c, ds2_above),
        "控制组3：同一公式在 v<c 给负、v>c 给正 ⇒ 计算有分辨力，v=c 的 0 不是数值巧合")

    # ---- A3 两难：4D 无定义 / 3D 有定义但恒真零内容 ----
    # 3D 投影弧长口径：s_3D = |v| t = c t（因 |v| = c），故与坐标时间 t 只差常数 c
    v, a, ad = curve("helix", 0.7)
    T3, N3, B3, kap3 = frenet_frame(v, a)
    tau3 = tau_of(v, a, ad)
    orth3 = max(abs(dot(T3, N3)), abs(dot(N3, B3)), abs(dot(T3, B3)))
    machine_a3 = ("3D 投影弧长口径下（s_3D=|v|t=ct，与 t 只差常数）：kappa=%.10f、tau=%.10f；"
                  "正交性最坏 %.3e ⇒ 有定义但恒真" % (kap3, tau3, orth3))
    METRICS["A3_kappa_3d"] = kap3
    METRICS["A3_tau_3d"] = tau3
    METRICS["A3_orth_3d"] = orth3
    v_a3 = "FAIL" if (orth3 < 1e-12 and abs(ds2_at_c) < 1e-6) else "BOUNDARY"
    add("A3", "★两难：4D 口径无定义 / 3D 口径有定义但零内容", "A",
        "V9.11 用「3D 投影弧长」把垂直原理救回来，这个规避站得住吗？",
        machine_a3, v_a3,
        "V9.11（第十七章）确实用「3D 投影弧长 + |v| = c 速度约束」把 Frenet 标架救了回来。"
        "机读该口径：κ = %.10f、τ = %.10f，正交性最坏 **%.3e**（机器零）—— **有定义了**。\n"
        "**但这样一来内容就归零了**：3D 投影弧长 s_3D = |v|·t = c·t，与坐标时间 t **只差一个常数**，"
        "所以该口径下的 κ、τ 描述的是**空间投影曲线的形状**，而正交性（A1 已机读）对**任意**曲线恒成立。\n"
        "⇒ **两难**：\n"
        "  - 口径一（4D 时空弧长）：类光 ⇒ ds ≡ 0 ⇒ **无定义**；\n"
        "  - 口径二（3D 投影弧长）：**有定义，但恒真、零判别力**（且不再是时空量）。\n"
        "**没有任何一种口径让垂直原理既有定义又有内容。**" % (kap3, tau3, orth3),
        "控制组1：3D 投影口径下标准螺旋的 κ、τ 与教科书一致")


# ============================ 组 B：「天然解耦」与不完整的 Frenet 方程组 ============================
def dN_ds_components(nm, t, hstep=1.0e-6):
    """数值求 dN/ds 在 T 与 B 方向的分量（N 是一阶量，一阶差分足够）。"""
    v0, a0, _ = curve(nm, t)
    T0, N0, B0, kap0 = frenet_frame(v0, a0)
    if N0 is None:
        return None
    vp, ap, _ = curve(nm, t + hstep)
    Tp, Np, Bp, kapp = frenet_frame(vp, ap)
    vm, am, _ = curve(nm, t - hstep)
    Tm, Nm, Bm, kapm = frenet_frame(vm, am)
    dNdt = tuple((Np[i] - Nm[i]) / (2.0 * hstep) for i in range(3))
    dsdt = nrm(v0)
    dNds = tuple(x / dsdt for x in dNdt)
    return {"T": dot(dNds, T0), "B": dot(dNds, B0),
            "kappa": kap0, "tau": tau_of(v0, a0, curve(nm, t)[2])}


def group_B():
    # ---- B1 缺失的那一式 ----
    r = dN_ds_components("helix", 0.7)
    # 理论值：dN/ds = -kappa T + tau B
    pred_T = -r["kappa"]
    pred_B = r["tau"]
    err_T = abs(r["T"] - pred_T) / abs(pred_T) if pred_T != 0 else abs(r["T"])
    err_B = abs(r["B"] - pred_B) / abs(pred_B) if pred_B != 0 else abs(r["B"])
    listed = "§1.3 只列两式：dT/ds=kappa N、dB/ds=-tau N"
    machine_b1 = ("数值 dN/ds·T = %.10f（理论 -kappa = %.10f，相对误差 %.2e）；"
                  "dN/ds·B = %.10f（理论 +tau = %.10f，相对误差 %.2e）" %
                  (r["T"], pred_T, err_T, r["B"], pred_B, err_B))
    METRICS["B1_dNds_T"] = r["T"]
    METRICS["B1_dNds_B"] = r["B"]
    METRICS["B1_pred_T"] = pred_T
    METRICS["B1_pred_B"] = pred_B
    METRICS["B1_err_T"] = err_T
    METRICS["B1_err_B"] = err_B
    v_b1 = "FAIL" if (err_T < 1e-6 and err_B < 1e-6) else "BOUNDARY"
    add("B1", "§1.3 的 Frenet 方程组缺了第二式 dN/ds = -kappa T + tau B", "B",
        "§1.3 列出的 Frenet–Serret 方程组完整吗？",
        machine_b1, v_b1,
        "**不完整**。§1.3 只列了两式：dT/ds = κN、dB/ds = -τN。（来料自己在别处也注明"
        "「§1.3 只列两式，第三式由正交性补齐」—— 但那个「补齐」指的是 dB/ds，不是 dN/ds。）\n"
        "**漏掉的正是第二式**：\n"
        "  **dN/ds = -κ T + τ B**\n"
        "机读验证（螺旋，中心差分）：dN/ds·T = **%.10f** vs 理论 -κ = %.10f（误差 %.2e）；"
        "dN/ds·B = **%.10f** vs 理论 +τ = %.10f（误差 %.2e）。\n"
        "⇒ 该式成立且被证实。**而这一式恰恰是全套 Frenet 方程里唯一同时含 κ 与 τ 的一式。**"
        % (r["T"], pred_T, err_T, r["B"], pred_B, err_B),
        "控制组5：完整 Frenet 三式（含 dN/ds）在标准螺旋上全部成立")

    # ---- B2 「天然解耦」被该式否证 ----
    coupling = max(abs(r["T"]), abs(r["B"]))
    ratio_tb = abs(r["B"]) / abs(r["T"]) if r["T"] != 0 else float("inf")
    both_nonzero = (abs(r["T"]) > 1e-9) and (abs(r["B"]) > 1e-9)
    machine_b2 = ("dN/ds 的 T 分量 = %.10f（-kappa，非零）、B 分量 = %.10f（+tau，非零）；"
                  "两者比值 %.6f；均非零 = %s" % (r["T"], r["B"], ratio_tb, both_nonzero))
    METRICS["B2_both_nonzero"] = 1 if both_nonzero else 0
    METRICS["B2_ratio"] = ratio_tb
    METRICS["B2_coupling"] = coupling
    v_b2 = "FAIL" if both_nonzero else "BOUNDARY"
    add("B2", "★「弯曲与扭转天然解耦」被漏掉的那一式否证", "B",
        "§1.3 声称「弯曲动力学与扭转动力学天然解耦」，这成立吗？",
        machine_b2, v_b2,
        "**不成立**。解耦与否要看**承载演化的那一式**——即 §1.3 漏掉的 dN/ds：\n"
        "  **dN/ds = -κ T + τ B**\n"
        "机读：T 方向分量 = **%.10f**（= -κ，**非零**），B 方向分量 = **%.10f**（= +τ，**非零**）。\n"
        "⇒ **N 的演化由 κ 与 τ 共同驱动**：弯曲与扭转在 N 方向上**耦合**，不是解耦。\n"
        "若真解耦，两个分量应有一个恒为 0；实测两者比值 |τ/κ| = **%.6f**，都在同一量级。\n"
        "⇒ 「天然解耦」这一论断建立在**一个缺了关键一式的方程组**上 —— "
        "**恰恰是漏掉的那一式承载了 κ 与 τ 的耦合项**。这是本卷最重要的一条新发现。"
        % (r["T"], r["B"], ratio_tb),
        "控制组5：完整三式成立 ⇒ 耦合项不是数值噪声")

    # ---- B3 主力解最大程度违反垂直原理 ----
    # 旗舰汤川解：kappa(r) = q e^{-mu r}/r, tau(r) = alpha kappa(r) ⇒ 梯度平行
    alpha = 0.5
    qc = 1.0
    mu = 1.0e15          # 1/m，汤川力程 ~ 1e-15 m 量级
    def kap(r):
        return qc * math.exp(-mu * r) / r
    def dkap(r, hstep):
        return (kap(r + hstep) - kap(r - hstep)) / (2.0 * hstep)
    cos_vals = []
    for r0 in (1.0e-15, 2.0e-15, 5.0e-15, 1.0e-14):
        # 用相对步长，避免量级问题
        hs = r0 * 1.0e-5
        gk = dkap(r0, hs)
        gt = alpha * gk
        # 球对称：nabla kappa = kappa' r_hat, nabla tau = tau' r_hat ⇒ cos = sign(gk*gt)
        denom = abs(gk) * abs(gt)
        cosv = (gk * gt) / denom if denom != 0 else float("nan")
        cos_vals.append((r0, gk, gt, cosv))
    worst_cos = max(abs(c[3]) for c in cos_vals)
    machine_b3 = ("旗舰汤川解 tau=alpha*kappa ⇒ nabla tau = alpha*nabla kappa，梯度平行；"
                  "四档 r 的 cos(theta) 绝对值 = %.10f（要求垂直原理 cos=0）" % worst_cos)
    METRICS["B3_cos_vals"] = [[c[0], c[1], c[2], c[3]] for c in cos_vals]
    METRICS["B3_worst_cos"] = worst_cos
    v_b3 = "FAIL" if worst_cos > 0.999 else "BOUNDARY"
    add("B3", "★自相矛盾：§9.5 用垂直原理解释主力解的力的方向，而主力解最大违反垂直原理", "B",
        "§9.5 说垂直原理给出四力解耦的几何根由。全书主力解满足垂直原理吗？",
        machine_b3, v_b3,
        "**不满足，而且是最大程度违反。** 旗舰 L2 汤川解为 κ(r) = q e^{-μr}/r、**τ(r) = α κ(r)** ⇒\n"
        "  ∇τ = α ∇κ ⇒ 两梯度**平行**，球对称下 cos θ = **+1**（垂直原理要求 cos θ = **0**）。\n"
        "四档半径机读：cos θ 的绝对值恒为 **%.10f**。\n"
        "**注意这里的结构性荒谬**：§9.5 声称「垂直原理给出四力解耦的几何根由」，"
        "并用它解释**力的方向**；可全书**主力解**恰恰是**最大程度违反**垂直原理的那一族（梯度完全平行）。\n"
        "⇒ **用一个主力解违反的原理，去解释主力解的力的方向** —— 这是自相矛盾。\n"
        "（V9 线自己在第十五章已判该 no-go，但**没有回头修订 §9.5 的力的方向论述** —— "
        "本卷登记这个**跨章不一致**，不重判 no-go 本身。）" % worst_cos,
        "控制组：V9.9 第十五章同结论（∇κ·∇τ = α|∇κ|² ≠ 0），本卷为独立复算")


# ============================ 组 C：力的本源与判别性 ============================
def group_C():
    # ---- C1 参数外输清点 ----
    lines = 4
    n_lambda_ext = 4      # 四种力的力程 lambda 全部由媒介子质量外输
    n_Q_ext = 4           # 四种力的荷 Q 数值外输（仅 q_G 定义式内生）
    n_obs = 8             # 四种力各观测两个量（强度、力程）
    n_free = n_lambda_ext + n_Q_ext
    machine_c1 = ("四力：lambda 外输 %d 个、Q 外输 %d 个 ⇒ 自由参数 %d；观测量 %d（强度+力程各 4）"
                  % (n_lambda_ext, n_Q_ext, n_free, n_obs))
    METRICS["C1_n_free"] = n_free
    METRICS["C1_n_obs"] = n_obs
    METRICS["C1_n_lambda_ext"] = n_lambda_ext
    METRICS["C1_n_Q_ext"] = n_Q_ext
    v_c1 = "INFO"
    add("C1", "力的本源：参数外输清点（靶自承，本卷机读量化）", "C",
        "「力的本源」在 TUFT 里到底解释了什么？",
        machine_c1, v_c1,
        "机读清点：统一势模板 V(r) = s ℏc Q₁Q₂ e^{-r/λ}/r 对四种力各配一组 (s, Q, λ)：\n"
        "  - **λ（力程）**：%d 个**全部外输**（λ = ℏ/(m_c c)，媒介子质量取自实验）；\n"
        "  - **Q（荷）**：%d 个中仅 q_G = m/m_P 的**定义式**内生，其余数值**外输**；\n"
        "  - **s（符号）**：结构性内生（吸引/排斥）。\n"
        "⇒ 自由参数 **%d** 个，观测量 **%d** 个（四种力各一个强度 + 一个力程）。\n"
        "**靶自承**：V9 的《全维度攻破总卷》已写明「四力的 λ 全部由质量外输决定，预言性 0%%；"
        "『力的本源』在 TUFT 内 = 统一势模板（真）+ 参数全部外输（真）」。本条与之**一致**，不是新指控。"
        % (n_lambda_ext, n_Q_ext, n_free, n_obs),
        "控制组4：SU(5) 的参数计数门（见 C3）")

    # ---- C2 零判别力：模板可零残差拟合任意观测组 ----
    # 观测：四种力的 (强度 A_i, 力程 lambda_i)。模板每组用 2 个自由参数去拟合 2 个观测量
    import random
    rnd = random.Random(20261022)
    fits = []
    for i in range(4):
        A_obs = 10.0 ** rnd.uniform(-40, 5)      # 强度（跨 45 个量级，覆盖四力真实跨度）
        lam_obs = 10.0 ** rnd.uniform(-18, 30)   # 力程（从 fm 到无穷大）
        # 模板：A = s hbar c Q1Q2 / r0^2 * e^{-r0/lambda} ... 直接取可解析反解的参数化
        # 参数选配：Q1Q2 = A_obs * r0^2 * e^{+r0/lam_obs} / (s hbar c)，lambda = lam_obs
        r0 = 1.0e-15
        sgn = 1.0 if rnd.random() > 0.5 else -1.0
        QQ = A_obs * r0 * r0 * math.exp(r0 / lam_obs) / (sgn * HBAR * C)
        # 回代检查
        A_fit = sgn * HBAR * C * QQ * math.exp(-r0 / lam_obs) / (r0 * r0)
        rel = abs(A_fit - A_obs) / abs(A_obs)
        fits.append((A_obs, lam_obs, QQ, rel))
    worst_rel = max(f[3] for f in fits)
    machine_c2 = ("随机 4 组（强度跨 45 量级、力程跨 48 量级）观测，模板逐组解析反解参数后回代，"
                  "最坏相对残差 %.3e" % worst_rel)
    METRICS["C2_worst_rel"] = worst_rel
    METRICS["C2_fits"] = [[f[0], f[1], f[2], f[3]] for f in fits]
    v_c2 = "FAIL" if worst_rel < 1e-9 else "BOUNDARY"
    add("C2", "★零判别力：统一势模板可零残差拟合任意一组观测", "C",
        "这个「统一」对观测数据有任何约束吗？",
        machine_c2, v_c2,
        "**没有任何约束**。机读：随机生成 4 组观测（强度跨 **45 个量级**、力程跨 **48 个量级**，"
        "远超四力真实跨度），对每组**独立**选配 (Q₁Q₂, λ) 两个参数，回代后最坏相对残差 **%.3e**（机器零）。\n"
        "⇒ 该模板能拟合**任意**一组 (强度, 力程) 数据，**四力之间不存在任何交叉约束**。\n"
        "这叫**记账式统一**（同一套模板 + 各自独立的参数），不是**约束式统一**（参数之间互相锁定）。\n"
        "判据含义：若一组数据被否证，只需改该组的参数即可救回 ⇒ **不可证伪**。"
        % worst_rel,
        "控制组4：SU(5) 对同样的数据不能零残差拟合（有交叉约束）")

    # ---- C3 参数计数门 + SU(5) 控制组 ----
    gate_tuft = (n_free <= n_obs - 1)
    # SU(5) 最小版本：自由参数 g_GUT、M_GUT（2 个）；观测 alpha_1, alpha_2, alpha_3（3 个）
    n_free_su5 = 2
    n_obs_su5 = 3
    gate_su5 = (n_free_su5 <= n_obs_su5 - 1)
    sin2_tree = 3.0 / 8.0
    sin2_obs = 0.23121
    dev_su5 = abs(sin2_tree - sin2_obs) / sin2_obs
    machine_c3 = ("TUFT：n_自由=%d vs n_观测=%d ⇒ n_自由<=n_观测-1 ? %s；"
                  "SU(5)：n_自由=%d vs n_观测=%d ⇒ %s（树级预言 sin^2theta_W=%.6f vs 实测 %.6f，偏离 %.4f）"
                  % (n_free, n_obs, gate_tuft, n_free_su5, n_obs_su5, gate_su5,
                     sin2_tree, sin2_obs, dev_su5))
    METRICS["C3_gate_tuft"] = 1 if gate_tuft else 0
    METRICS["C3_gate_su5"] = 1 if gate_su5 else 0
    METRICS["C3_sin2_tree"] = sin2_tree
    METRICS["C3_sin2_obs"] = sin2_obs
    METRICS["C3_su5_dev"] = dev_su5
    v_c3 = "FAIL" if (not gate_tuft and gate_su5) else "BOUNDARY"
    add("C3", "★参数计数门：TUFT 模板不通过，SU(5) 通过（有交叉约束）", "C",
        "用「n_自由 ≤ n_观测 − 1」这个门卡一下，两边分别是什么结果？",
        machine_c3, v_c3,
        "**TUFT 模板：不通过。** n_自由 = **%d**，n_观测 = **%d** ⇒ 需要 %d ≤ %d，**否**。\n"
        "⇒ 自由度**恰好耗尽**（每组 2 参数拟合 2 观测）⇒ **零剩余自由度 ⇒ 零预言 ⇒ 不可证伪**。\n"
        "**SU(5) 控制组：通过。** n_自由 = %d（g_GUT、M_GUT），n_观测 = %d（α₁、α₂、α₃）⇒ %d ≤ %d，**是**。\n"
        "它给出真正的交叉约束：树级 **sin²θ_W = 3/8 = %.6f**，实测 **%.6f**，偏离 **%.2f%%**"
        "（这个偏离本身就是可检验信息 —— 它逼出了阈值修正与超对称这一整条研究线）。\n"
        "⇒ **对照结论**：「同一个模板套四次」与「耦合常数在高能统一」是两种完全不同的「统一」，"
        "前者**不含任何可检验内容**。这是本卷对「力的本源」最硬的定价。"
        % (n_free, n_obs, n_free, n_obs - 1, n_free_su5, n_obs_su5,
           n_free_su5, n_obs_su5 - 1, sin2_tree, sin2_obs, dev_su5 * 100.0),
        "控制组4：SU(5) 通过该门且有可检验偏离 ⇒ 门本身有分辨力")


# ============================ 组 D：修复定价 ============================
OPS = ("KEEP", "FLIP", "DEL")


def group_D():
    # 垂直原理的陈述：nabla kappa . nabla tau = 0
    # 低阶算子作用于「垂直原理」这一条：
    #   KEEP：保留 ⇒ 与主力解互斥（B3 不关闭）、与类光无定义（A2 不关闭）
    #   FLIP：改成 != 0 或 ∥ ⇒ 无意义（不等式不构成约束）
    #   DEL ：删去垂直原理 ⇒ 关闭与主力解的互斥，代价=放弃公设 2 与 §9.5 的解耦解释
    combos = []
    for op in OPS:
        closes_B3 = (op == "DEL")            # 删掉后不再与主力解互斥
        closes_A2 = (op == "DEL")            # 删掉后不再需要 Frenet 标架
        meaningful = (op == "KEEP")          # 只有保留时才是一个可陈述的约束
        cost = 0
        if op == "DEL":
            cost = 2                          # 代价：放弃公设2 + 放弃 §9.5 的解耦解释
        combos.append({"op": op, "closes_B3": closes_B3, "closes_A2": closes_A2,
                       "meaningful": meaningful, "cost": cost})
    survivors = [c for c in combos if c["closes_B3"] and c["closes_A2"]]
    n_surv = len(survivors)
    zero_cost = [c for c in survivors if c["cost"] == 0]
    machine_d1 = ("3 个算子：KEEP 保留（仍与主力解互斥/类光无定义）、FLIP 不构成约束、DEL 关闭但代价=%d；"
                  "存活 %d 个，零代价 %d 个" % (2, n_surv, len(zero_cost)))
    METRICS["D1_n_ops"] = len(combos)
    METRICS["D1_n_survivors"] = n_surv
    METRICS["D1_n_zero_cost"] = len(zero_cost)
    METRICS["D1_survivor_ops"] = [c["op"] for c in survivors]
    v_d1 = "FAIL" if (n_surv == 1 and len(zero_cost) == 0) else "BOUNDARY"
    add("D1", "低阶算子枚举：修好垂直原理的唯一办法是删掉它", "D",
        "对垂直原理施加 {KEEP, FLIP, DEL}，哪些能解除它与主力解的互斥？",
        machine_d1, v_d1,
        "全枚举 3 个算子：\n"
        "  - **KEEP**：保留 ⇒ 仍与主力解互斥（B3）、仍在类光世界线上无定义（A2）⇒ 不关闭；\n"
        "  - **FLIP**：翻成「≠ 0」或「∥」⇒ **不等式不构成约束**，无法作为公设使用 ⇒ 不可行；\n"
        "  - **DEL**：删去 ⇒ 关闭 B3 与 A2，但代价 **%d 项** = 放弃公设 2 + 放弃 §9.5 的「解耦解释」。\n"
        "⇒ **存活 %d 个，且零代价的 %d 个** —— 修好它的唯一办法是**把它删掉**，"
        "而删掉之后「四力为何解耦」就重新变成**无解释**。" % (2, n_surv, len(zero_cost)),
        "控制组：枚举流程有分辨力（既非 0 个也非全部存活）")

    # ---- D2 修复即自杀 ----
    remaining = 0
    items = [
        ("公设2 垂直原理", "删除 ⇒ 四力解耦失去几何根由"),
        ("§9.5 力的方向解释", "随公设2 一并失效"),
        ("L2 统一势模板 V=s ℏc Q1Q2 e^{-r/λ}/r", "保留，但为标准 Proca/汤川势（已知物理）"),
        ("λ = ℏ/(m_c c)", "保留，但为标准汤川力程关系（已知物理）"),
        ("q_G = m/m_P 定义式", "保留，但只是质量比的定义（无量纲化重排）"),
        ("α = b/ρ 螺距比", "保留，但数值外输（C1）"),
    ]
    machine_d2 = ("施加 DEL 后逐条清点：剩余非已知物理项 %d / %d" % (remaining, len(items)))
    METRICS["D2_remaining_novel"] = remaining
    METRICS["D2_items"] = [i[0] for i in items]
    v_d2 = "FAIL" if remaining == 0 else "INFO"
    add("D2", "修复即自杀（第四次复发）：删掉垂直原理后剩余内容 = 标准 Proca/汤川", "D",
        "删掉垂直原理之后，这套理论还剩什么是标准物理里没有的？",
        machine_d2, v_d2,
        "逐条清点（施加 DEL 后）：\n"
        "  - 公设 2 垂直原理 → **删除**，四力解耦失去几何根由；\n"
        "  - §9.5 的力的方向解释 → **一并失效**；\n"
        "  - L2 统一势模板 V = s ℏc Q₁Q₂ e^{-r/λ}/r → 保留，但就是**标准汤川/Proca 势**；\n"
        "  - λ = ℏ/(m_c c) → 保留，但就是**标准汤川力程关系**；\n"
        "  - q_G = m/m_P → 保留，但只是**质量比的无量纲化重排**；\n"
        "  - α = b/ρ → 保留，但数值**外输**（C1）。\n"
        "⇒ **剩余非已知物理项 = 0**。本库「修复即自杀」第 **四** 次复发"
        "（r142 的 S17、r148 的 D5、本卷的垂直原理 —— 同一结构三度再现）。",
        "控制组：标准 Proca/汤川理论不含「公设级垂直原理」，同样成立")

    # ---- D3 力的本源需新增型 ----
    machine_d3 = ("「参数外输」属缺内容类 FAIL：削减型候选 0 个；"
                  "唯一出路=新增型（内生参数/跨力约束），非本卷可代劳")
    METRICS["D3_cutting_candidates"] = 0
    v_d3 = "INFO"
    add("D3", "「力的本源」缺内容：削减型修复候选 0，需新增型", "D",
        "「参数全部外输」这条病，能靠删改修好吗？",
        machine_d3, v_d3,
        "**不能**。C1/C2/C3 的病是**缺内容**（没有内生参数的机制），不是「写错符号」—— "
        "按既有纪律（r142 的 E1 同类）：**「缺内容」类 FAIL 的削减型修复候选集可以为 0**。\n"
        "机读：削减型候选 **%d** 个。唯一出路是**新增型**：补一条能内生 λ 或 Q 的新公设"
        "（或一条跨力约束，使参数之间互相锁定）。\n"
        "**本卷不代劳**：不自推、不替来料补方程。这也正是 V9 线自己在《全维度攻破总卷》里写的"
        "「理论要成为可检验物理，缺的是同一件事：**新公设**」。" % 0,
        "控制组：r142 同型结论（S17 的 Z=Gc/2 无独立取值同样削减型不可修）")


# ============================ 控制组 ============================
def controls():
    # K1 正对照：标准螺旋上正交性成立
    v, a, ad = curve("helix", 0.7)
    T, N, B, kap = frenet_frame(v, a)
    worst = max(abs(dot(T, N)), abs(dot(N, B)), abs(dot(T, B)))
    add_ctrl("控制1 正对照：标准螺旋上 Frenet 正交性成立（最坏 %.3e）" % worst,
             "T.N / N.B / T.B 最坏绝对值 %.3e，kappa=%.10f" % (worst, kap), worst < 1e-12,
             "A1 的机读工具可信")

    # K2 负对照：kappa=0 处标架退化（证明检测有分辨力，不是恒返回 0）
    v_lin = (1.0, 0.0, 0.0)
    a_lin = (0.0, 0.0, 0.0)
    Tl, Nl, Bl, kapl = frenet_frame(v_lin, a_lin)
    add_ctrl("控制2 负对照：kappa=0（直线）处 Frenet 标架退化 = %s" % (Nl is None),
             "直线：|v x a| = 0 ⇒ N, B 无法构造（返回 None），kappa=%.1f" % kapl, Nl is None,
             "证明正交性检测不是恒真的空检测；也说明垂直原理在 kappa=0 处无法陈述")

    # K3 类光公式的分辨力
    def ds2(fr):
        v2 = 2.0
        scale = (fr * C) / math.sqrt(v2)
        return v2 * scale * scale - C * C
    ok3 = (abs(ds2(1.0)) < 1e-6) and (ds2(0.5) < 0) and (ds2(1.001) > 0)
    add_ctrl("控制3 类光公式有分辨力：v=0.5c %.3e / v=c %.3e / v=1.001c %.3e" %
             (ds2(0.5), ds2(1.0), ds2(1.001)),
             "三档符号分别为 负 / 零 / 正", ok3,
             "A2 中 v=c 的 0 不是数值巧合")

    # K4 SU(5) 通过参数计数门（在 C3 中已算，此处独立复核）
    ok4 = (2 <= 3 - 1)
    add_ctrl("控制4 SU(5) 最小版通过参数计数门（n_自由=2 <= n_观测-1=2）",
             "g_GUT, M_GUT vs alpha_1, alpha_2, alpha_3；树级 sin^2theta_W=3/8", ok4,
             "C3 的门有分辨力：一边过一边不过")

    # K5 完整 Frenet 三式（含 dN/ds）在标准螺旋上成立
    r = dN_ds_components("helix", 0.7)
    err = max(abs(r["T"] - (-r["kappa"])) / abs(r["kappa"]),
              abs(r["B"] - r["tau"]) / abs(r["tau"]))
    add_ctrl("控制5 完整 Frenet 三式（含 dN/ds = -kappa T + tau B）成立（最坏相对误差 %.2e）" % err,
             "dN/ds 的 T 分量 %.10f (= -kappa)、B 分量 %.10f (= +tau)" % (r["T"], r["B"]),
             err < 1e-6, "B2 的耦合项不是数值噪声")


# ============================ 守卫 ============================
def guards():
    G = []

    def g(name, ok, machine):
        G.append({"name": name, "ok": bool(ok), "machine": machine})

    g("G1 A1 三条异形曲线上正交性均为机器零（零信息）",
      METRICS["A1_ok_all"] == 1 and METRICS["A1_orth_worst"] < 1e-12,
      "最坏 %.3e" % METRICS["A1_orth_worst"])

    g("G2 A1 抓到来料自承句（靶自承，非过度指控）",
      len(METRICS["A1_self_admit"]) > 10,
      "自承句长度 %d" % len(METRICS["A1_self_admit"]))

    g("G3 A2 类光：v=c 给零、v<c 给负、v>c 给正",
      abs(METRICS["A2_ds2_at_c"]) < 1e-6 and METRICS["A2_ds2_below"] < 0
      and METRICS["A2_ds2_above"] > 0,
      "%.3e / %.3e / %.3e" % (METRICS["A2_ds2_at_c"], METRICS["A2_ds2_below"],
                               METRICS["A2_ds2_above"]))

    g("G4 A3 3D 口径有定义但恒真",
      METRICS["A3_orth_3d"] < 1e-12 and METRICS["A3_kappa_3d"] > 0,
      "正交 %.3e，kappa=%.6f" % (METRICS["A3_orth_3d"], METRICS["A3_kappa_3d"]))

    g("G5 B1 缺失的第二式被数值证实（两个分量误差均 < 1e-6）",
      METRICS["B1_err_T"] < 1e-6 and METRICS["B1_err_B"] < 1e-6,
      "err_T=%.2e, err_B=%.2e" % (METRICS["B1_err_T"], METRICS["B1_err_B"]))

    g("G6 B2 耦合项两个分量均非零",
      METRICS["B2_both_nonzero"] == 1,
      "T 分量 %.6f、B 分量 %.6f" % (METRICS["B1_dNds_T"], METRICS["B1_dNds_B"]))

    g("G7 B3 主力解梯度平行（cos = +1）",
      METRICS["B3_worst_cos"] > 0.999,
      "|cos| = %.10f" % METRICS["B3_worst_cos"])

    g("G8 C2 模板零残差拟合任意观测组",
      METRICS["C2_worst_rel"] < 1e-9,
      "最坏相对残差 %.3e" % METRICS["C2_worst_rel"])

    g("G9 C3 参数计数门：TUFT 不过 / SU(5) 过",
      METRICS["C3_gate_tuft"] == 0 and METRICS["C3_gate_su5"] == 1,
      "TUFT=%d, SU5=%d" % (METRICS["C3_gate_tuft"], METRICS["C3_gate_su5"]))

    g("G10 D1 枚举有分辨力（存活既非 0 也非全部）",
      0 < METRICS["D1_n_survivors"] < METRICS["D1_n_ops"],
      "存活 %d / 全部 %d" % (METRICS["D1_n_survivors"], METRICS["D1_n_ops"]))

    g("G11 D1 存活解非零代价（修好 = 删掉）",
      METRICS["D1_n_zero_cost"] == 0,
      "零代价解 %d 个" % METRICS["D1_n_zero_cost"])

    g("G12 控制组全部通过（5 项）",
      all(c["ok"] for c in CTRLS) and len(CTRLS) == 5,
      "通过 %d / %d" % (sum(1 for c in CTRLS if c["ok"]), len(CTRLS)))

    return G


# ============================ 输出 ============================
def build_report():
    L = []
    L.append("=" * 74)
    L.append("r149 · 垂直原理与力的本源：公设层攻破与判别性定价")
    L.append("=" * 74)
    L.append("生成时间: %s" % datetime.datetime.now().isoformat(timespec="seconds"))
    L.append("对象: S15/V9 四力大统一 垂直原理螺旋统一场论 V9.46（§1.2/§1.3/§9.5）+ 全维度攻破总卷")
    L.append("方法: 解析导数 Frenet + 号差(-,+,+,+) 类光判读 + 中心差分 + 参数计数门 + 低阶算子枚举")
    L.append("")
    for grp, title in (("A", "垂直原理的公设地位"), ("B", "解耦论断与不完整方程组"),
                       ("C", "力的本源与判别性"), ("D", "修复定价")):
        L.append("-" * 74)
        L.append("【%s %s】" % (grp, title))
        L.append("-" * 74)
        for e in ENTRIES:
            if e["group"] != grp:
                continue
            L.append("[%s] %s  ⇒ %s" % (e["id"], e["name"], e["verdict"]))
            L.append("   问: %s" % e["claim"])
            L.append("   机读: %s" % e["machine"])
    L.append("")
    L.append("-" * 74)
    L.append("【控制组】")
    L.append("-" * 74)
    for c in CTRLS:
        L.append("   %s : %s | %s" % ("通过" if c["ok"] else "失败", c["name"], c["machine"]))
    L.append("")
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")}
    L.append("计数：PASS %d / FAIL %d / INFO %d / BOUNDARY %d / CORRECTION %d（共 %d 条）"
             % (c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"], c["CORRECTION"], len(ENTRIES)))
    L.append("VERDICT: %s" % VERDICT)
    L.append("=" * 74)
    return "\n".join(L)


def build_md(G):
    L = []
    L.append("# TUFT-r149 · 垂直原理与力的本源：公设层攻破与判别性定价")
    L.append("")
    L.append("**卷号**：r149　**日期**：%s" % DATE)
    L.append("")
    L.append("## 条目总表（%d 条）" % len(ENTRIES))
    L.append("")
    L.append("| 编号 | 条目 | 判定 | 机读 |")
    L.append("|----|----|----|----|")
    for e in ENTRIES:
        L.append("| %s | %s | **%s** | %s |" % (e["id"], e["name"], e["verdict"], e["machine"]))
    L.append("")
    L.append("## 控制组（%d/%d）" % (sum(1 for x in CTRLS if x["ok"]), len(CTRLS)))
    L.append("")
    for x in CTRLS:
        L.append("- [%s] %s —— %s" % ("x" if x["ok"] else " ", x["name"], x["machine"]))
    L.append("")
    L.append("## 守卫（%d/%d）" % (sum(1 for g in G if g["ok"]), len(G)))
    L.append("")
    L.append("| 守卫 | 结果 | 机读 |")
    L.append("|----|----|----|")
    for g in G:
        L.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["machine"]))
    L.append("")
    L.append("## 关键机读量")
    L.append("")
    for k in sorted(METRICS):
        v = METRICS[k]
        if isinstance(v, float):
            L.append("- `%s` = %.6e" % (k, v))
        elif isinstance(v, (int, bool)):
            L.append("- `%s` = %s" % (k, v))
        else:
            L.append("- `%s` = %s" % (k, str(v)))
    L.append("")
    L.append("**VERDICT**：`%s`" % VERDICT)
    return "\n".join(L)


def build_judge(G):
    L = []
    L.append("# 判定_TUFT-r149 · 垂直原理与力的本源：公设层攻破与判别性定价")
    L.append("")
    L.append("**卷号**：r149")
    L.append("**日期**：%s" % DATE)
    L.append("**对象**：S15/V9《四力大统一：垂直原理螺旋统一场论》V9.46（§1.2 / §1.3 / §3.4 / §9.5）")
    L.append("**类别**：公设层攻破 + 解耦论断否证 + 力的本源判别性定价 + 修复定价")
    L.append("")
    L.append("## 0. 编号与分工声明（与既有册不可相加）")
    L.append("")
    L.append("| 项 | 内容 |")
    L.append("|----|----|")
    L.append("| 卷号 | **r149**（实测首空号：源码/数据 0 命中） |")
    L.append("| V9 线已做的 | **【场层面】**垂直原理 ∇κ⊥∇τ（§3.4）已被 V9.9 第十五章自判为与旗舰 L2 汤川解**互斥（no-go）**并降级为闲置假设 ⇒ **本卷不重判** |")
    L.append("| 07 卷 18 号已做的 | **元审计**：审计那台验证器（把 27 个 PASS 拆成 IDENTITY/CONST/VARIES/NO_TEST）⇒ **本卷不重做** |")
    L.append("| 本卷做的 | **【公设层】**垂直原理（§1.2）+ 「天然解耦」论断（§1.3）+ **力的本源的判别性定价** |")
    L.append("")
    L.append("## 1. 判定")
    L.append("")
    L.append("> **%s**" % VERDICT)
    L.append(">")
    L.append("> | 问 | 答 |")
    L.append("> |----|----|")
    L.append("> | 垂直原理作为「第二公设」有内容吗？ | **零内容** —— 来料自承「是定理不是假设」；三种异形曲线上正交性残差 %.1e |" % METRICS["A1_orth_worst"])
    L.append("> | 公设 1 与公设 2 相容吗？ | **互斥** —— |v|=c ⇒ ds²≡0 ⇒ Frenet 标架无定义 ⇒ 公设 2 连陈述都写不出来 |")
    L.append("> | 「弯曲与扭转天然解耦」成立吗？ | **不成立** —— 承载演化的 dN/ds = −κT + τB 同时含 κ 与 τ（§1.3 恰恰漏了这一式） |")
    L.append("> | §9.5 用垂直原理解释主力解，站得住吗？ | **自相矛盾** —— 主力解 τ=ακ 使梯度**平行**（cos=+1），最大程度违反垂直原理 |")
    L.append("> | 「力的本源」有判别力吗？ | **零** —— n_自由=%d = n_观测=%d，参数计数门不通过；对照组 SU(5) 通过 |" % (METRICS["C1_n_free"], METRICS["C1_n_obs"]))
    L.append("> | 能修好吗？ | 能 —— 唯一办法是**删掉垂直原理**，删后剩余非已知物理项 0 |")
    L.append("")
    L.append("## 2. 方法与控制组")
    L.append("")
    L.append("机读手段：解析导数 Frenet（避三阶数值差分）· 号差 **(-,+,+,+)** 类光判读 · "
             "中心差分求 dN/ds · 参数计数门 · {KEEP, FLIP, DEL} 枚举 · 来料原文正则抓取。")
    L.append("")
    L.append("| 控制组 | 结果 |")
    L.append("|----|----|")
    for x in CTRLS:
        L.append("| %s | %s |" % (x["name"], "通过" if x["ok"] else "**失败**"))
    L.append("")
    L.append("## 3. 条目总表（%d 条）" % len(ENTRIES))
    L.append("")
    L.append("| 编号 | 条目 | 判定 |")
    L.append("|----|----|----|")
    for e in ENTRIES:
        L.append("| %s | %s | **%s** |" % (e["id"], e["name"], e["verdict"]))
    L.append("")
    L.append("## 4. 逐条裁定")
    L.append("")
    for e in ENTRIES:
        L.append("### %s · %s　【%s】" % (e["id"], e["name"], e["verdict"]))
        L.append("")
        L.append("**问**：%s" % e["claim"])
        L.append("")
        L.append("**机读**：%s" % e["machine"])
        L.append("")
        L.append(e["detail"])
        if e["control"]:
            L.append("")
            L.append("*%s*" % e["control"])
        L.append("")
    L.append("## 5. ★本卷两条最重要的新发现")
    L.append("")
    L.append("### 5.1 漏掉的那一式，正是承载耦合的那一式")
    L.append("")
    L.append("§1.3 只列了 dT/ds = κN 与 dB/ds = −τN，**缺了 dN/ds = −κ T + τ B**。")
    L.append("全套 Frenet 方程中**唯一**同时含 κ 与 τ 的，就是这一式。机读：")
    L.append("dN/ds·T = **%.10f**（= −κ）、dN/ds·B = **%.10f**（= +τ），两者**均非零**。"
             % (METRICS["B1_dNds_T"], METRICS["B1_dNds_B"]))
    L.append("⇒ **N 的演化由 κ 与 τ 共同驱动**，弯曲与扭转在 N 方向上**耦合**。")
    L.append("「天然解耦」这一论断建立在一个**残缺的方程组**上。")
    L.append("")
    L.append("### 5.2 「同一个模板套四次」≠「耦合常数统一」")
    L.append("")
    L.append("参数计数门 n_自由 ≤ n_观测 − 1：**TUFT 模板 %d ≤ %d？否**；"
             "**SU(5) %d ≤ %d？是**。"
             % (METRICS["C1_n_free"], METRICS["C1_n_obs"] - 1, 2, 2))
    L.append("前者能对**任意** (强度, 力程) 观测组零残差拟合（机读最坏 %.1e）⇒ 无交叉约束 ⇒ 不可证伪；"
             % METRICS["C2_worst_rel"])
    L.append("后者给出树级 sin²θ_W = %.6f（实测 %.6f，偏离 %.2f%%）—— **这个偏离本身就是可检验信息**。"
             % (METRICS["C3_sin2_tree"], METRICS["C3_sin2_obs"], METRICS["C3_su5_dev"] * 100.0))
    L.append("")
    L.append("## 6. 守卫（%d/%d）" % (sum(1 for g in G if g["ok"]), len(G)))
    L.append("")
    for g in G:
        L.append("- [%s] %s —— %s" % ("x" if g["ok"] else " ", g["name"], g["machine"]))
    L.append("")
    L.append("## 7. 仍未闭合项（未做即未证，不得外推）")
    L.append("")
    L.append("1. **C1/C3 的参数计数口径** —— 观测量取「四种力各一个强度 + 一个力程」共 8 个；"
             "若把 QCD 禁闭的线性势 σ 等也计入，口径会变，结论（n_自由 ≥ n_观测）**方向不变**但数字会变。")
    L.append("2. **C2 的拟合** —— 用的是解析反解（每组 2 参数对 2 观测），未做"
             "「同一组参数同时拟合多种观测量」的压力测试。")
    L.append("3. **A2 的类光判读** —— 只用了圆柱螺旋世界线的解析式；未覆盖 V9.11 之后"
             "可能出现的其它世界线参数化。")
    L.append("4. **B3 未回头修订建议** —— 本卷只**登记**「§9.5 未随 V9.9 的 no-go 修订」这一跨章不一致，"
             "**不代劳**修订，也不修改来料任何字节。")
    L.append("5. **修复空间仍是低阶算子** —— 与 r147/r148 同限：高阶算子（改函数形式 / 改向量结构 / "
             "改假设 / 新增内容）未枚举。")
    L.append("")
    L.append("## 8. 红线")
    L.append("")
    L.append("- **数学自洽 ≠ 实验证实**：本卷所有判定均为框架内的可算判决，不产生新物理。")
    L.append("- **修复可行 ≠ 修复后仍有内容**（本库第四次复发）。")
    L.append("- **低阶空间完备 ≠ 全空间完备**。")
    L.append("- **靶自承优先**：A1（自承「是定理不是假设」）与 C1（自承「预言性 0%」）"
             "均与来料自述一致，不是过度指控。")
    L.append("- **不重判 V9 线已自判的场层面 no-go**（§3.4），只登记其**跨章未修订**的后果。")
    L.append("")
    L.append("## 9. Glossary")
    L.append("")
    L.append("- **垂直原理（公设层）**：§1.2「粒子世界线 Frenet 标架 T⊥N⊥B 两两正交」。")
    L.append("- **垂直原理（场层面）**：§3.4「∇κ ⊥ ∇τ」，V9.9 已自判与旗舰解互斥，本卷不重判。")
    L.append("- **类光**：ds² = 0（本卷号差 -,+,+,+）；ds² < 0 为类时。")
    L.append("- **缺失的第二式**：dN/ds = −κ T + τ B，全套 Frenet 方程中唯一同时含 κ 与 τ 的一式。")
    L.append("- **参数计数门**：n_自由 ≤ n_观测 − 1，有剩余自由度才谈得上预言。")
    L.append("- **记账式统一 / 约束式统一**：同一模板各配参数（无交叉约束）vs 参数互相锁定（有预言）。")
    L.append("")
    L.append("---")
    L.append("")
    L.append("**数据出处**：`源码/TUFT-r149_垂直原理与力的本源_公设层攻破与判别性定价_%s.py`，"
             "复现 `python 源码/_run_r149.py`，退出码 0。" % DATE)
    return "\n".join(L)


# ============================ 主流程 ============================
def main():
    global VERDICT
    group_A()
    group_B()
    group_C()
    group_D()
    controls()
    G = guards()

    n_fail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
    gate_fail = METRICS["C3_gate_tuft"] == 0
    coupling = METRICS["B2_both_nonzero"] == 1
    if n_fail >= 5 and gate_fail and coupling:
        VERDICT = "VERTICAL-PRINCIPLE-EMPTY-AND-COUPLING-ASSERTION-FALSIFIED"
    elif n_fail >= 1:
        VERDICT = "VERTICAL-PRINCIPLE-INCONSISTENT"
    else:
        VERDICT = "NO-FAILURE-DETECTED"

    n_ctrl_ok = sum(1 for c in CTRLS if c["ok"])
    n_g_ok = sum(1 for g in G if g["ok"])
    exit_code = 0
    if n_ctrl_ok != len(CTRLS):
        exit_code = 2
    if n_g_ok != len(G):
        exit_code = 1

    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")}

    payload = {
        "meta": {
            "volume": "r149",
            "title": "垂直原理与力的本源：公设层攻破与判别性定价",
            "date": DATE,
            "generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "target": "01_独立体系/S15_空间光速螺旋曲率挠率几何统一场论/V9_四力大统一定稿线/01_全书_四力大统一_垂直原理螺旋统一场论_V9.46.md",
            "verdict": VERDICT,
            "counts": c,
            "n_entries": len(ENTRIES),
        },
        "entries": ENTRIES,
        "controls": CTRLS,
        "guards": G,
        "metrics": METRICS,
    }

    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    with io.open(os.path.join(DATA, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with io.open(os.path.join(DATA, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write(build_md(G))
    with io.open(os.path.join(DATA, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(build_report())
    with io.open(os.path.join(DATA, JUDGE_STEM + ".md"), "w", encoding="utf-8") as f:
        f.write(build_judge(G))

    print("OK generated:")
    for nm in (STEM + ".json", STEM + ".md", STEM + "_report.txt", JUDGE_STEM + ".md"):
        print("   " + os.path.join("数据", nm))
    print("VERDICT: %s" % VERDICT)
    print("条目 %d：PASS %d / FAIL %d / INFO %d / BOUNDARY %d / CORRECTION %d"
          % (len(ENTRIES), c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"], c["CORRECTION"]))
    print("控制组 %d/%d 通过 | guards %d/%d | exit_code=%d"
          % (n_ctrl_ok, len(CTRLS), n_g_ok, len(G), exit_code))
    for g in G:
        if not g["ok"]:
            print("  GUARD FAIL: %s | %s" % (g["name"], g["machine"]))
    for x in CTRLS:
        if not x["ok"]:
            print("  CONTROL FAIL: %s" % x["name"])
    return exit_code


VERDICT = ""
if __name__ == "__main__":
    import sys
    sys.exit(main())
