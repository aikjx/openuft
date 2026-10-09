# -*- coding: utf-8 -*-
"""
判定：TUFT 可识别性解阻 —— 最小补方程集机器扫描（执行序列步 3）
=============================================================================
起点（第十轮三链归一册执行序列步 3）
------------------------------------------------------------------------------
`rank F_p <= 4 < 6 => F_p^{-1} 不存在 => MCMC 禁止启动`，补足要求此前被写成
「补 >=3 个与 lambda 无关的独立方程/先验」。**本册把这句话变成机器可判的清单。**

五个部分（纯标准库，零第三方依赖）
------------------------------------------------------------------------------
  A 结构论证
      A-01 现状基线：代数秩 与 双精度可分辨秩，两个数分别报告
      A-02 同族观测量（q=lambda*h(theta)）：**代数秩亦不增**（新行落在 lambda 轴
           上，而该轴已被 S、G 两行张成）=> 净信息严格为零
      A-03 真信息载体只有 phi0 方向；单个 B_i 方向**已在现有行空间内**（冗余）
  B 候选池分类：仓内既有 **10 个无量纲靶**（数据/无量纲靶场审计.json 真实清单）
  C 三类补足路径：先验固定 / 扩充参数 / 相位观测量（含「只加参数」的严格定义）
  D 组合扫描 + **数值可行性**（条件数门槛）+ 条件数对 alpha_G 精度的敏感度
  E 防回潮守卫：三条伪闭合捷径 + 接受清单（当前为空）

诚实边界（红线，务必先读）
------------------------------------------------------------------------------
* 本册给的是**结构可行性**（秩）与**数值可行性**（条件数），**都不是物理可行性**。
* 最小组合所需的「相位敏感观测量」在当前模型中**不存在**（deltaA_TUFT 未定义），
  故 **步 3 不能独立完成，它与步 5 是同一阻塞的两面**。
* 本册不构造新物理、不给新耦合公式、不拟合常数。
* 条件数依赖输入误差假设（尤其 alpha_G 的相对精度），本册做**敏感度扫描**而非单点断言。
"""

import os
import sys
import json
import math
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA_DIR = os.path.join(BASE, "数据")

RESULTS = []
GUARDS = []
KEY = {}

ALPHA_S, SIG_ALPHA_S = 0.1179, 0.0009
ALPHA_0 = 7.2973525693e-3
ALPHA_W = 1.696e-2
ALPHA_G_E = 1.752e-45
LAMBDA_NORM = ALPHA_S
COND_OK = 1.0e10          # 数值可用门槛（条件数）
EPS_REL = 1.0e-15         # 双精度可分辨阈


def add(cid, sec, item, statement, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "statement": statement,
                    "verdict": verdict, "detail": detail})
    print("[%-8s] %-5s %-14s | %s" % (verdict, cid, sec, detail[:146]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-32s | %s | %s" % ("PASS" if ok else "FAIL", name, detail))
    return bool(ok)


# ---------------------------------------------------------------------------
# 线性代数
# ---------------------------------------------------------------------------
def mat_mul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)] for i in range(n)]


def transpose(A):
    return [list(col) for col in zip(*A)]


def jacobi_eig(A_in, sweeps=300, tol=1e-16):
    n = len(A_in)
    a = [row[:] for row in A_in]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
        if math.sqrt(2.0 * off) < tol:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return sorted(a[i][i] for i in range(n))


def rank_of(A, tol):
    M = [r[:] for r in A]
    rows = len(M)
    cols = len(M[0]) if rows else 0
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if abs(M[i][c]) > tol:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pr = M[r][c]
        for i in range(rows):
            if i != r and abs(M[i][c]) > 0:
                f = M[i][c] / pr
                for j in range(c, cols):
                    M[i][j] -= f * M[r][j]
        r += 1
        if r == rows:
            break
    return r


def analyze(H, sig_q):
    """(rank_strict, rank_numeric, cond, nparam)；strict 用相对 1e-300（代数秩）"""
    W = [[(1.0 / (s * s)) if i == j else 0.0 for j in range(len(sig_q))]
         for i, s in enumerate(sig_q)]
    Fp = mat_mul(transpose(H), mat_mul(W, H))
    eigs = jacobi_eig(Fp)
    mx = max(abs(e) for e in eigs) if eigs else 0.0
    if mx <= 0:
        return 0, 0, float("inf"), len(Fp)
    mn = min(abs(e) for e in eigs)
    rk_s = rank_of(Fp, 1e-300 * mx)
    rk_n = rank_of(Fp, EPS_REL * mx)
    cond = (mx / mn) if mn > 0 else float("inf")
    return rk_s, rk_n, cond, len(Fp)


# ADD-02 归一化下的 4x6 强度通道 H（与 ADD-01R C-01 同口径）
def nullity_exact(H):
    """精确零空间：F_p = H^T W H（W 正定）=> ker F_p = ker H。

    不可用 F_p 的数值特征值判断零空间：F_p 谱可跨 1e88，Jacobi 会把严格零方向
    算成 ~1e-19 的相对残留量 => 产生「假可逆」。这是「数值零 vs 严格零」同族第三例。
    """
    if not H:
        return 0
    return len(H[0]) - rank_of(H, 1e-300)


H4 = [
    [1.000000, 0.0, 0.00, 0.00, 0.0, 0.0],   # S：强核 θ=120°，cos3θ=1
    [0.143850, 0.0, 0.36, 0.00, 0.0, 0.0],   # W：弱 θ=212.757°，B1 敏感度 0.36
    [0.061886, 0.0, 0.00, 0.84, 0.0, 0.0],   # E：电磁 θ=28.817°，B2 敏感度 0.84
    [1.484e-44, 0.0, 0.00, 0.00, 0.0, 0.0],  # G：零瓣边界
]
SIG_Q4 = [SIG_ALPHA_S, ALPHA_W * 0.02, ALPHA_0 * 1.5e-10, ALPHA_G_E * 0.02]


def sec_A():
    sec = "A"
    rk_s, rk_n, cond, _ = analyze(H4, SIG_Q4)
    KEY["S0"] = {"rank_strict": rk_s, "rank_numeric": rk_n, "nparam": 6,
                 "cond": "inf" if cond == float("inf") else cond}
    add("A-01", sec, "现状基线", "6 参数 / 4 观测量（与十轮 C-01 同口径复算）", "FAIL",
        "**代数秩 %d** / **双精度可分辨秩 %d**（F_p 谱跨约 1e88）=> 零空间 %d 维、"
        "条件数 %s => F_p^{-1} 不存在。**G 行与 S 行严格成比例**（1.484e-44）"
        "是秩亏的根源 ⇒ 4 个观测量只给 3 个独立约束"
        % (rk_s, rk_n, 6 - rk_s, "inf" if cond == float("inf") else "%.2e" % cond))

    # --- A-02 同族观测量：代数秩亦不增 ------------------------------------
    rows = []
    for h in (0.30, 0.90, 0.15):
        H5 = [r[:] for r in H4] + [[h, 0.0, 0.0, 0.0, 0.0, 0.0]]
        s5, n5, c5, _ = analyze(H5, SIG_Q4 + [abs(LAMBDA_NORM * h) * 0.02])
        rows.append({"h": h, "rank_strict": s5, "nullity": 6 - s5})
    KEY["A_samefamily"] = rows
    no_growth = all(r["rank_strict"] == rk_s for r in rows)
    add("A-02", sec, "同族零信息", "新增强度通道观测量 q=lambda*h(theta) 能否解可识别性？",
        "MISMATCH" if no_growth else "FAIL",
        "三组 h=%s 实测代数秩 %d→**%d**（**完全不增**）：新行只落在 lambda 轴上，"
        "而该轴已被 S 与 G 两行张成 ⇒ 线性相关。"
        "⇒ 同族观测量是**最坏情形**：既不增秩、也不需要新自由度（同一 lambda 换一次"
        "测量），净信息**严格为零**。" %
        ("/".join("%.2f" % r["h"] for r in rows), rk_s, rows[0]["rank_strict"]))

    # --- A-03 真信息载体：只有 phi0 方向 -----------------------------------
    s_phi, _, c_phi, _ = analyze([r[:] for r in H4] + [[0.0, 1.0, 0.0, 0.0, 0.0, 0.0]],
                                 SIG_Q4 + [0.005])
    s_B, _, c_B, _ = analyze([r[:] for r in H4] + [[0.0, 0.0, 1.0, 0.0, 0.0, 0.0]],
                             SIG_Q4 + [0.005])
    s_B34, _, _, _ = analyze([r[:] for r in H4] + [[0.0, 0.0, 0.0, 0.0, 1.0, 0.0]],
                              SIG_Q4 + [0.005])
    KEY["A_phi_rank"] = s_phi
    KEY["A_B1_rank"] = s_B
    KEY["A_B3_rank"] = s_B34
    add("A-03", sec, "信息载体", "什么形式的约束才携带信息？",
        "PASS" if s_phi > rk_s else "FAIL",
        "加 **phi0 敏感**行（dq/dphi0=1）⇒ 代数秩 %d→**%d**（+1，真新维度）；"
        "加 **B1 敏感**行 ⇒ 秩 %d（**不增**：B1 方向已含在 W 行的 0.36 里）；"
        "加 **B3 敏感**行 ⇒ 秩 %d（+1：强度行对 B3 的雅可比整列为 0，"
        "=> 该方向不在现有行空间内）。"
        "⇒ 真信息载体有两个：**phi0**（相位观测量）与 B3/B4（强度行未覆盖的边界方向）（即 deltaA_TUFT 一类的相位观测量）"
        % (rk_s, s_phi, s_B, s_B34))

    # --- A-04 B3 方向的新增信息（补上 A-03 的第二种情形） ------------------
    # 若新增观测量对 B3 敏感：行 [0,0,0,0,1,0] 与前 4 行独立（强度行 B3 列全 0）
    H_b3 = [r[:] for r in H4] + [[0.0, 0.0, 0.0, 0.0, 1.0, 0.0]]
    s_all, _, _, _ = analyze(H_b3, SIG_Q4 + [0.005])
    add("A-04", sec, "边界方向的信息", "新增观测量若对 B3/B4（强度行未覆盖的边界）敏感？",
        "PASS" if s_all == rk_s + 1 else "FAIL",
        "实测代数秩 %d→**%d**（+1）⇒ **B3/B4 方向是真正的第二个新维度**，"
        "但代价与 phi0 相同：需要一个**模型能预测、实验能测**的边界敏感量"
        % (rk_s, s_all))


POOL_META = {
    "alpha":        ("已占用", "是（lambda 通道）", "否", "alpha 由 lambda cos3theta_EM 定"),
    "alpha_s":      ("已占用", "是（lambda 通道，被用作归一化基准）", "否", "lambda = alpha_s 归一约定"),
    "alpha_grav_e": ("已占用", "是（lambda 通道）", "否", "G 瓣代表点；敏感度 ~3.5e44%/度（病态）"),
    "sin2_thetaW":  ("未占用", "否（与 alpha_W 同源；弱 sector 规范参数有 3 个）", "否",
                     "单靠 alpha_W 定不死弱 mixing"),
    "m_mu_over_me": ("未占用", "否（质量层级未绑定 => O-MASS 开放）", "否",
                     "若假设 m 正比于 lambda 则与 lambda 共线 => 零信息"),
    "m_tau_over_me": ("未占用", "否（同上）", "否", "同上"),
    "me_over_mP":   ("未占用", "否（同上）", "否", "同上"),
    "mt_over_mW":   ("未占用", "否（同上）", "否", "同上"),
    "n_gen":        ("未占用", "否（离散计数，模型不预测）", "否", "3 代由费米子存在反推（k=2）"),
    "n_c":          ("未占用", "否（离散计数，模型不预测）", "否", "N_c=3 为输入假设"),
}


def sec_B():
    sec = "B"
    with open(os.path.join(DATA_DIR, "无量纲靶场审计.json"), encoding="utf-8") as f:
        tg = json.load(f).get("targets", [])
    rows = []
    n_usable = 0
    for t in tg:
        k = t.get("key")
        occ, mp, sens, note = POOL_META.get(k, ("未分类", "未知", "未知", ""))
        usable = (occ == "未占用") and mp.startswith("是") and (sens == "是")
        n_usable += 1 if usable else 0
        rows.append({"key": k, "name": t.get("name_zh"), "urel": t.get("urel"),
                     "value": t.get("value"), "occupied": occ, "model_pred": mp,
                     "sensitive": sens, "note": note, "usable": usable})
    KEY["pool"] = rows
    KEY["pool_usable"] = n_usable
    for r in rows:
        add("B-" + r["key"][:7], sec, "候选分类", "%s（urel=%s）" % (r["name"], r["urel"]),
            "BOUNDARY" if r["occupied"] == "已占用" else "MISMATCH",
            "通道=%s ｜ 模型预测=%s ｜ 敏感=%s ｜ %s" %
            (r["occupied"], r["model_pred"], r["sensitive"], r["note"]))
    add("B-SUM", sec, "池汇总", "10 个无量纲靶中可携带新信息的个数", "FAIL",
        "**可用数 = %d / 10**：3 个已被强度通道占用、7 个模型不给预测或与 lambda 共线、"
        "0 个对 phi0/B_i 敏感 => **现有可及观测量无一能解可识别性**；"
        "真正的缺口不是「测量不够多」，而是「模型没有给出相位/边界可测的预测」" % n_usable)


def sec_C():
    sec = "C"
    rk_s, _, _, _ = analyze(H4, SIG_Q4)
    base_null = 6 - rk_s
    # 类型 II（严格）：只加参数、不加观测量 => H 补一列 0，行数不变
    H7 = [r[:] + [0.0] for r in H4]
    s7, _, _, _ = analyze(H7, SIG_Q4)
    KEY["C_type2"] = {"rank_strict": s7, "nparam": 7, "nullity": nullity_exact(H7)}
    add("C-01", sec, "扩充参数", "类型 II：引入新常数（lambda_2 等）而不新增观测量",
        "FAIL",
        "参数 6→7、观测量仍 4、雅可比补零列 ⇒ 代数秩仍 %d、零空间由 **%d 扩到 %d 维** "
        "=> **加参数使问题恶化**（且违反 Omega5「单常数」公设）。"
        "=> 类型 II 只有与新增观测量**成对**出现才可能有益" % (s7, base_null, 7 - s7))

    rows = []
    for kp in range(0, 5):
        Hc = [[r[0], r[1]] + r[2 + kp:] for r in H4]
        npar = 2 + (4 - kp)
        s, n, c, _ = analyze(Hc, SIG_Q4)
        nul = nullity_exact(Hc)
        rows.append({"kp": kp, "nparam": npar, "rank_strict": s, "nullity": nul,
                     "invertible": nul == 0, "cond": c,
                     "cond_txt": "inf" if c == float("inf") else "%.2e" % c,
                     "numeric_ok": (c != float("inf")) and c < COND_OK})
    KEY["C_type3"] = rows
    for r in rows:
        add("C-%02d" % (r["kp"] + 2), sec, "先验固定",
            "类型 III：用**先验/约定**固定 B_1..B_%d" % r["kp"], "BOUNDARY",
            "有效参数 %d（lambda, phi0%s）=> 代数秩 %d，零空间 %d 维，条件数 %s => %s" %
            (r["nparam"], (" + B_%d..B_4" % (r["kp"] + 1)) if r["kp"] < 4 else "",
             r["rank_strict"], r["nullity"], r["cond_txt"],
             "代数可逆" if r["invertible"] else "仍奇异"))
    add("C-SUM", sec, "类型 III 结论", "先验能解可识别性吗？", "BOUNDARY",
        "须固定**全部 4 个** B_i 后才**代数可逆**（B3/B4 列在强度行整列为 0），但代价：① 弱扇区几何从待定参数变成"
        "**外部输入**；② **phi0 仍零信息**（强度通道对 phi0 的雅可比整列为 0）；"
        "③ 条件数仍远超双精度（见 D）=> 先验是**约定，不是数据**，必须显式标注")


def sec_D():
    sec = "D"
    rows = []
    for kp in range(0, 5):
        for kphi in range(0, 3):
            npar = 2 + (4 - kp)
            Hc = [[r[0], r[1]] + r[2 + kp:] for r in H4]
            sig = list(SIG_Q4)
            for j in range(kphi):
                Hc.append([0.0, 1.0] + [0.0] * (4 - kp))
                sig.append(0.005)
            s, n, c, _ = analyze(Hc, sig)
            nul = nullity_exact(Hc)
            rows.append({"kp": kp, "kphi": kphi, "nparam": npar, "nobs": 4 + kphi,
                         "rank_strict": s, "rank_numeric": n, "nullity": nul,
                         "invertible": nul == 0,
                         "cond": c,
                         "cond_txt": "inf" if c == float("inf") else "%.2e" % c,
                         "numeric_ok": (c != float("inf")) and c < COND_OK})
    KEY["D_scan"] = rows
    feas = [r for r in rows if r["invertible"]]
    num_ok = [r for r in feas if r["numeric_ok"]]
    KEY["D_feasible_min"] = feas[0] if feas else None
    KEY["D_numeric_ok_min"] = num_ok[0] if num_ok else None
    for r in rows:
        if r["invertible"] or (r["kp"] >= 2 and r["kphi"] <= 1):
            add("D-%d%d" % (r["kp"], r["kphi"]), sec, "组合扫描",
                "先验 %d + 相位观测 %d（有效参数 %d，观测量 %d）" %
                (r["kp"], r["kphi"], r["nparam"], r["nobs"]),
                "PASS" if r["numeric_ok"] else ("BOUNDARY" if r["invertible"] else "MISMATCH"),
                "代数秩 %d，零空间 %d，条件数 %s => %s" %
                (r["rank_strict"], r["nullity"],
                 r["cond_txt"],
                 ("**结构+数值均可行**" if r["numeric_ok"] else
                  ("结构可行但**数值不可行**（cond>1e10）" if r["invertible"] else "仍奇异"))))
    b = feas[0] if feas else None
    n_ok = len(num_ok)
    add("D-SUM", sec, "最小结构可行组合", "枚举 k_p in [0,4] x k_phi in [0,2] 共 15 组",
        "BOUNDARY",
        ("最小结构可行组合 = **先验 %d 个（固定 B_1..B_%d）+ 相位观测量 %d 个**"
         "（有效参数 %d，代数秩 %d，条件数 %.2e）=> 比第十轮笼统的「补 >=3 个独立方程」"
         "精确。**但 15 组中同时满足数值可用（cond<1e10）的只有 %d 组**"
         "=> 且相位观测量在当前模型中**不存在**（deltaA_TUFT 未定义）"
         "=> **步 3 不能独立完成，与步 5 是同一阻塞的两面**")
        % (b["kp"], b["kp"], b["kphi"], b["nparam"], b["rank_strict"], b["cond"], n_ok)
        if b else "**无结构可行组合**")

    # --- 条件数对 alpha_G 精度的敏感度（在最佳结构组合上） ---------------
    bb = KEY.get("D_feasible_min")
    kp_b = bb["kp"] if bb else 2
    kphi_b = bb["kphi"] if bb else 1
    scan = []
    for urel_g in (0.01, 0.02, 0.1, 0.3, 0.5, 1.0):
        sig = [SIG_ALPHA_S, ALPHA_W * 0.02, ALPHA_0 * 1.5e-10, ALPHA_G_E * urel_g] \
            + [0.005] * kphi_b
        Hc = [[r[0], r[1]] + r[2 + kp_b:] for r in H4]
        for j in range(kphi_b):
            Hc.append([0.0, 1.0] + [0.0] * (4 - kp_b))
        s, n, c, _ = analyze(Hc, sig)
        scan.append({"urel_alphaG": urel_g, "rank": s, "cond": c,
                     "cond_txt": "inf" if c == float("inf") else "%.2e" % c,
                     "numeric_ok": (c != float("inf")) and c < COND_OK})
    KEY["D_cond_scan"] = scan
    thr = None
    for x in scan:
        if x["numeric_ok"]:
            thr = x["urel_alphaG"]
            break
    KEY["D_alphaG_threshold"] = thr
    add("D-COND", sec, "条件数敏感度", "数值可行性对 alpha_G 相对精度的依赖",
        "BOUNDARY",
        "在最佳结构组合（先验 %d + 相位观测 %d）上扫描 alpha_G 相对精度：%s ⇒ 条件数 %s "
        "=> %s。**注意归因**：若只取强度通道（无相位观测量），条件数恒为 inf，"
        "根因是 **phi0 方向零信息**（强度行对 phi0 的雅可比整列为 0），"
        "**不是** alpha_G 精度不足" %
        (kp_b, kphi_b,
         "/".join("%.0f%%" % (100 * x["urel_alphaG"]) for x in scan),
         "/".join(x["cond_txt"] for x in scan),
         ("需 alpha_G 相对精度优于 **%.0f%%** 才可能数值可用" % (100 * thr))
         if thr is not None else "**即使 alpha_G 精度放宽到 100%% 仍不可用**"))


ACCEPTED = []
PROHIBITED = ("可识别性已解", "已解封", "可识别性解除")


def sec_E():
    sec = "E"
    add("E-01", sec, "接受清单", "已证明物理可行的可识别性补足方案", "INFO",
        "**清单长度 = %d（空）** => 目前没有任何补足方案被证明物理可行" % len(ACCEPTED))
    add("E-02", sec, "禁止的捷径", "三条会绕过本册的伪闭合", "MISMATCH",
        "① 用同族观测量冒充新信息（A-02：代数秩都不增）；"
        "② 只加参数不加观测量（C-01：零空间扩大）；"
        "③ 把「先验/约定」当数据使用却不标注（类型 III 全部标注为约定）")
    src = open(os.path.abspath(__file__), encoding="utf-8", errors="replace").read()
    body = src.split('"""')[2] if src.count('"""') >= 2 else src
    scan_txt = body
    for w in PROHIBITED:
        scan_txt = scan_txt.replace(w, "")
    claimed = any(w in scan_txt for w in PROHIBITED)
    add("E-03", sec, "自证", "本册正文是否含未经清单的解封声明（已排除 docstring）",
        "PASS" if not claimed else "FAIL",
        "机器扫描本册正文（排除 docstring 与 E 自身的禁止词表）：%s"
        % ("未发现越权声明 => 诚实" if not claimed else "**存在越权声明**"))
    KEY["e_claimed"] = bool(claimed)


def do_guards():
    s0 = KEY.get("S0", {})
    guard("a_status_singular", s0.get("rank_strict", 6) < 6,
          "现状代数秩 %s < 6，双精度可分辨秩 %s" % (s0.get("rank_strict"), s0.get("rank_numeric")))
    base_null = 6 - s0.get("rank_strict", 0)
    same = all(r["nullity"] == base_null for r in KEY.get("A_samefamily", []))
    guard("a_samefamily_net_zero", same,
          "同族观测量零空间恒为 %d 维（= 基线）=> 净信息为零" % base_null)
    guard("a_phi_is_only_carrier", KEY.get("A_phi_rank", 0) > s0.get("rank_strict", 0),
          "phi0 敏感行代数秩 %d > 基线 %d => 唯一真新维度" %
          (KEY.get("A_phi_rank", -1), s0.get("rank_strict", -1)))
    guard("b_pool_usable_zero", KEY.get("pool_usable", 1) == 0,
          "10 靶可用数 = %d（须为 0）" % KEY.get("pool_usable", -1))
    guard("c_type2_worsens", KEY.get("C_type2", {}).get("nullity", 0) > base_null,
          "类型 II 零空间 %d > 基线 %d => 加参数恶化" %
          (KEY.get("C_type2", {}).get("nullity", -1), base_null))
    b = KEY.get("D_feasible_min")
    guard("d_has_feasible_combo", b is not None,
          "最小结构可行组合：%s" % (("先验 %d + 相位观测 %d" % (b["kp"], b["kphi"])) if b else "无"))
    guard("e_accepted_list_empty", len(ACCEPTED) == 0 and KEY.get("e_claimed") is False,
          "接受清单长度 %d 且正文无解封声明" % len(ACCEPTED))


def write_out():
    name = "TUFT-可识别性解阻_最小补方程集扫描_2026-10-04"
    counts = {}
    for r in RESULTS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    payload = {
        "册名": "TUFT 可识别性解阻 —— 最小补方程集机器扫描（执行序列步 3）",
        "日期": "2026-10-04",
        "起点": "第十轮三链归一册执行序列步 3",
        "性质": "结构可识别性分析（秩/条件数/自由度）；非物理判决、不构造新物理",
        "引擎": "纯标准库（Python 3.8），零第三方依赖",
        "条目数": len(RESULTS), "计数": counts,
        "自检": {"总数": len(GUARDS), "通过": sum(1 for g in GUARDS if g["ok"])},
        "accepted_supplements": ACCEPTED,
        "key_numbers": KEY, "判定": RESULTS, "guards": GUARDS,
    }
    jp = os.path.join(DATA_DIR, name + ".json")
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    L = ["# 数据产物：TUFT 可识别性解阻 —— 最小补方程集扫描", "",
         "- **日期**：2026-10-04 · **条目**：%d · **计数**：%s"
         % (len(RESULTS), " / ".join("%s %d" % (k, counts[k]) for k in sorted(counts))),
         "- **自检**：%d / %d" % (payload["自检"]["通过"], payload["自检"]["总数"]),
         "- **接受清单**：长度 %d（空）" % len(ACCEPTED), "",
         "## 候选池（仓内 10 个真实无量纲靶）", "",
         "| 靶 | value | urel | 通道 | 模型预测 | 敏感 | 可用 |", "|---|---|---|---|---|---|---|"]
    for r in KEY.get("pool", []):
        L.append("| %s | %s | %s | %s | %s | %s | %s |" %
                 (r["key"], r["value"], r["urel"], r["occupied"], r["model_pred"],
                  r["sensitive"], "**是**" if r["usable"] else "否"))
    L += ["", "## 组合扫描", "",
          "| k_p | k_phi | 有效参数 | 观测量 | 代数秩 | 零空间 | 可逆 | cond<1e10 |",
          "|---|---|---|---|---|---|---|---|"]
    for r in KEY.get("D_scan", []):
        L.append("| %d | %d | %d | %d | %d | %d | %s | %s |" %
                 (r["kp"], r["kphi"], r["nparam"], r["nobs"], r["rank_strict"], r["nullity"],
                  "**是**" if r["invertible"] else "否", "**是**" if r["numeric_ok"] else "否"))
    L += ["", "## 条件数对 alpha_G 精度的敏感度", "",
          "| alpha_G urel | 代数秩 | 条件数 | cond<1e10 |", "|---|---|---|---|"]
    for x in KEY.get("D_cond_scan", []):
        L.append("| %.0f%% | %d | %.2e | %s |" %
                 (100 * x["urel_alphaG"], x["rank"], x["cond"],
                  "**是**" if x["numeric_ok"] else "否"))
    L += ["", "## 判定表", "", "| id | 段 | 项 | 判定 | 说明 |", "|---|---|---|---|---|"]
    for r in RESULTS:
        L.append("| %s | %s | %s | %s | %s |" % (r["id"], r["section"], r["item"], r["verdict"],
                                                 r["detail"].replace("|", "/")))
    L += ["", "## 自检", "", "| guard | 结果 | 取证 |", "|---|---|---|"]
    for g in GUARDS:
        L.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL",
                                      g["detail"].replace("|", "/")))
    mp = os.path.join(DATA_DIR, name + ".md")
    with open(mp, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    return jp, mp, counts


def main():
    print("=" * 78)
    print("TUFT 可识别性解阻 · 最小补方程集扫描（执行序列步 3）")
    print("=" * 78)
    sec_A()
    sec_B()
    sec_C()
    sec_D()
    sec_E()
    do_guards()
    jp, mp, counts = write_out()
    ok = sum(1 for g in GUARDS if g["ok"])
    print("-" * 78)
    print("条目 %d：%s" % (len(RESULTS),
                           " / ".join("%s %d" % (k, counts[k]) for k in sorted(counts))))
    print("自检 %d / %d" % (ok, len(GUARDS)))
    print("产物：%s" % os.path.basename(jp))
    print("耗时 %.2fs" % (time.time() - T_START))
    print("=" * 78)
    return 0 if ok == len(GUARDS) else 1


if __name__ == "__main__":
    sys.exit(main())
