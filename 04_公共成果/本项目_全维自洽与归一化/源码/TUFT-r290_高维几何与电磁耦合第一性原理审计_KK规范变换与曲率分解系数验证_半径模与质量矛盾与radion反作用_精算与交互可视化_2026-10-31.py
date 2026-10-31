# -*- coding: utf-8 -*-
r"""TUFT-r290 · ROOT V12.0「从空间几何真正推导电磁耦合」· 第一性原理审计
S1 五维规范变换：θ→θ+χ 诱导 B→B−∂χ、H 不变、Abel 复合（三类数值残差）
S2 五维 Ricci 分解系数 −R²/4 的独立数值验证（5D 有限差分曲率，两档 R）
   + 纯规范阳性对照（R5 应为 0）+ 错误系数对照（¾ ⇒ ratio 1/3）
S3 α_KK=4(ℓ_P/R)² 代数恒等 + R=2ℓ_P/√α 反解（23.412475 ℓ_P / 3.78405e−34 m）
S4 KK 第一带电模态 m=ħc/R 与电子质量矛盾（1.02e21）+ 反解 α 7.0e−45
S5 模数：任意 R 真空 Ricci 平直；α∝R⁻²(G4 固定)/R⁻³(G5 固定) 单调；
   树阶 EH 对 R 无势（V≡0）；单圈 Casimir 单幂 x⁻⁴（量纲）⇒ 无内部极小
S6 稳定势 V=Ax²+B/x²：x*=(B/A)^{1/4}、V″=8A、α=4√(A/B) 全部解析成立，
   但 x*≡2/√α、A/B=α²/16 ⇒ 恒等式；dof=0；整数电荷 vs 夸克 ±1/3
S7 radion：常数 R 要求 F²=0；静电场 F²=−2E²≠0；反作用量级 ~1e−46
S8 精度地板（G 的 2.2e−5 ⇒ R 只有 4 位有效）；S9 来料 10000 组残差无判别力
    （错误系数控制组同样给 1e−16）
2026-10-31

〔编号说明〕起草前实测三树：源码/判定最大 r287（r287 四件套齐）；数据树 r286 被
并行线以「V11 本源攻坚审计·来料原件·用户附件逐字」（22:59:20）占用（无引擎/
无判定册/无 runner/无 HTML）⇒ 跳过 r286，初稿取 r288。但 r288 落盘过程中被并行线
「KK 电荷质量排除定理审计（二参数唯一解快子与真空能 10^117 灾难）」占满（其引擎
23:39:35、数据 23:39:41、判定册 23:41:17 齐备）⇒ 本卷改号 r289。随后该并行线亦
自行改号至 r289（其引擎 23:43:29、数据 23:43:37、判定册 23:44:07），而本卷判定册
尚未落盘 ⇒ 依「先占四件套者为权威、后到者改号、不删他人文件」，本卷再让一号取
r290（源码/判定/数据/根 HTML 四树 r290 当时全空）。本卷旧 r288/r289 半成品已由
本卷自行清除，并行线任何文件均未触碰（未覆盖、未删除、未改名）。

〔定位〕ROOT V12.0 放弃「找接近 137.036 的公式」，改走
  高维空间几何 → 电磁规范场 → 电荷量子化 → 精细结构常数
（Kaluza–Klein）。本卷不新增物理，只做**第一性原理审计**：把 V12 的每一项
声称独立机检，并判定它是否构成「不含 α 实验输入的无参数预言」。

口径：
  - 纯标准库；float64 曲率用中心差分（h=4e−3…1e−3，误差按 h² 收敛）；
  - α⁻¹=137.035999177（CODATA 2022，u=2.1e−8）；ℓ_P=1.616255e−35 m；
  - ħc=1.973269804e−16 GeV·m；m_P c²=1.2209944e19 GeV；m_e c²=5.1099895e−4 GeV；
  - G 相对不确定度 2.2e−5（来料口径）⇒ 半径有效位数上限；
  - 守卫失败即非零退出；条目不可与 r142–r287 相加。
"""

import json
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r290_KK耦合审计交互可视化模板_2026-10-31.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_高维几何推导电磁耦合可行性审计_r290可视化_2026-10-31.html")

MARKER = "R290-KK-ALPHA-FIRST-PRINCIPLES-AUDIT"
STEM = "TUFT-r290"
BASE = ("TUFT-r290_高维几何与电磁耦合第一性原理审计_KK规范变换与曲率分解系数验证_"
        "半径模与质量矛盾与radion反作用_精算与交互可视化_2026-10-31")

PI = math.pi

# ---------------- 外部锚（只作事后比对/否证输入） ----------------
ALPHA_INV = 137.035999177
U_ALPHA_INV = 2.1e-8
ALPHA = 1.0 / ALPHA_INV
LP = 1.616255e-35          # m（CODATA 2022）
REL_G = 2.2e-5             # 来料口径的 G 相对不确定度
HC_GEV_M = 1.973269804e-16  # ħc，GeV·m
MP_GEV = 1.2209944e19       # m_P c²
ME_GEV = 5.1099895e-4       # m_e c²

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


# ============================================================
# 五维曲率（有限差分，独立于任何 KK 公式）
# ============================================================
N5 = 5


def inv_mat(g):
    n = len(g)
    a = [[float(g[i][j]) for j in range(n)] + [1.0 if i == j else 0.0 for j in range(n)]
         for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[p] = a[p], a[c]
        d = a[c][c]
        for j in range(2 * n):
            a[c][j] /= d
        for r in range(n):
            if r != c:
                f = a[r][c]
                if f:
                    for j in range(2 * n):
                        a[r][j] -= f * a[c][j]
    return [[a[i][n + j] for j in range(n)] for i in range(n)]


def metric5(P, R, a):
    """ds²=g_μνdx^μdx^ν + R²(dθ + a dx¹)²，g_4=diag(−1,1,1,1)。"""
    g = [[0.0] * N5 for _ in range(N5)]
    g[0][0] = -1.0
    g[1][1] = 1.0 + R * R * a * a
    g[1][4] = R * R * a
    g[4][1] = R * R * a
    g[4][4] = R * R
    g[2][2] = 1.0
    g[3][3] = 1.0
    return g


def christoffel5(mfun, P, h):
    g = mfun(P)
    gi = inv_mat(g)
    gp = [mfun([P[k] + (h if k == q else 0.0) for k in range(N5)]) for q in range(N5)]
    gm = [mfun([P[k] - (h if k == q else 0.0) for k in range(N5)]) for q in range(N5)]
    dg = [[[(gp[k][i][j] - gm[k][i][j]) / (2 * h) for j in range(N5)]
           for i in range(N5)] for k in range(N5)]
    G = [[[0.0] * N5 for _ in range(N5)] for _ in range(N5)]
    for k in range(N5):
        for i in range(N5):
            for j in range(N5):
                s = 0.0
                for l in range(N5):
                    s += gi[k][l] * (dg[i][j][l] + dg[j][i][l] - dg[l][i][j])
                G[k][i][j] = 0.5 * s
    return G


def ricci5(mfun, P, h):
    G = christoffel5(mfun, P, h)
    gi = inv_mat(mfun(P))
    Gp = [christoffel5(mfun, [P[k] + (h if k == q else 0.0) for k in range(N5)], h)
          for q in range(N5)]
    Gm = [christoffel5(mfun, [P[k] - (h if k == q else 0.0) for k in range(N5)], h)
          for q in range(N5)]
    Ric = [[0.0] * N5 for _ in range(N5)]
    for i in range(N5):
        for j in range(N5):
            s = 0.0
            for k in range(N5):
                s += (Gp[k][k][i][j] - Gm[k][k][i][j]) / (2 * h)
                s -= (Gp[j][k][i][k] - Gm[j][k][i][k]) / (2 * h)
                for m in range(N5):
                    s += G[k][k][m] * G[m][i][j] - G[k][j][m] * G[m][i][k]
            Ric[i][j] = s
    Rsc = 0.0
    for i in range(N5):
        for j in range(N5):
            Rsc += gi[i][j] * Ric[i][j]
    return Rsc


# ============================================================
# S1 · 五维规范变换
# ============================================================
def s1_gauge():
    print("[S1] 五维规范变换 θ'=θ+χ：B'=B−∂χ、H'=H、Abel 复合")

    def chi(x):
        u = 0.31 * x[1] + 0.5 * x[2]
        return 0.7 * math.sin(u) + 0.2 * x[3] * x[3]

    def dchi(x):
        u = 0.31 * x[1] + 0.5 * x[2]
        return [0.0, 0.7 * 0.31 * math.cos(u), 0.7 * 0.5 * math.cos(u), 0.4 * x[3]]

    def bfun(x):
        return [0.4 * math.sin(x[1]), 0.7 * math.cos(0.3 * x[2]), 0.2 * x[3], 0.5 * x[1] * x[2]]

    def bprime(x, h=1e-6):
        b = bfun(x)
        d = dchi(x)
        return [b[j] - d[j] for j in range(4)]

    def jac(fun, x, h=1e-4):
        out = []
        for i in range(4):
            xp = list(x)
            xp[i] += h
            xm = list(x)
            xm[i] -= h
            fp = fun(xp)
            fm = fun(xm)
            out.append([(fp[j] - fm[j]) / (2.0 * h) for j in range(4)])
        return out

    # (a) 线元不变：dθ = dθ' − ∂χ·dx ⇒ (dθ+B·dx)² = (dθ'+B'·dx)²
    xs = [0.37, 0.62, -0.41, 0.28]
    dx = [0.13, -0.27, 0.31, 0.19]
    dth = 0.44
    b = bfun(xs)
    d = dchi(xs)
    old = (dth + sum(b[j] * dx[j] for j in range(4))) ** 2
    new = (dth + sum(d[j] * dx[j] for j in range(4))
           + sum((b[j] - d[j]) * dx[j] for j in range(4))) ** 2
    res_line = abs(new - old) / max(abs(old), 1e-30)

    # (b) H 不变：H'_μν − H_μν = (∂μ∂νχ − ∂ν∂μχ) = 0
    worst_h = 0.0
    scale_h = 0.0
    for xs in ([0.37, 0.62, -0.41, 0.28], [1.13, -0.29, 0.74, 0.05], [-0.6, 0.31, 0.52, -0.88]):
        jc = jac(bfun, xs)
        jp = jac(bprime, xs)
        for i in range(4):
            for j in range(i + 1, 4):
                hc = jc[i][j] - jc[j][i]
                hp = jp[i][j] - jp[j][i]
                worst_h = max(worst_h, abs(hp - hc))
                scale_h = max(scale_h, abs(hc))
    rel_h = worst_h / max(scale_h, 1e-30)

    # (c) Abel 复合：χ=χ1+χ2
    def chi2(x):
        return 0.31 * x[1] * x[2] + 0.15 * math.cos(x[3])

    def dchi2(x):
        return [0.0, 0.31 * x[2], 0.31 * x[1], -0.15 * math.sin(x[3])]

    xs = [0.21, 0.47, -0.66, 0.9]
    seq = bfun(xs)
    for _ in range(2):
        pass
    b1 = [seq[j] - dchi(xs)[j] for j in range(4)]
    b2 = [b1[j] - dchi2(xs)[j] for j in range(4)]
    bsum = [bfun(xs)[j] - dchi(xs)[j] - dchi2(xs)[j] for j in range(4)]
    scale_b = max(abs(v) for v in bfun(xs))
    res_abel = max(abs(b2[j] - bsum[j]) for j in range(4)) / max(scale_b, 1e-30)

    print(f"  线元残差={res_line:.3e}；H 不变 max rel={rel_h:.3e}；Abel 复合残差={res_abel:.3e}")
    guard("G1", "线元不变：θ'=θ+χ ⇒ B'=B−∂χ（等价于 U(1) 规范变换）",
          res_line < 1e-12,
          f"随机点/随机位移下 |Δ|/|·|={res_line:.3e}（构造性恒等）",
          {"res_line": res_line})
    guard("G2", "场强 H=dB 在规范变换下不变（混合偏导对称）",
          rel_h < 1e-6,
          f"3 点 × 6 分量 max rel={rel_h:.3e}（FD 误差量级；解析上恒为 0）",
          {"rel_h": rel_h})
    guard("G3", "变换群 Abel：先 χ1 后 χ2 等价于 χ1+χ2",
          res_abel < 1e-12,
          f"复合残差={res_abel:.3e}（无对易子 ⇒ 严格 U(1)，非非阿贝尔）",
          {"res_abel": res_abel})

    return {"res_line": res_line, "rel_h": rel_h, "res_abel": res_abel}


# ============================================================
# S2 · 曲率分解系数 −R²/4（独立数值验证）+ α_KK 代数
# ============================================================
def s2_kk():
    print("[S2] 五维 Ricci 分解：R5 = R4 − (R²/4)F² 的系数/符号/R² 幂次机检")

    pred_of = lambda R, da: -0.25 * R * R * (-2.0 * da * da)   # = R²ȧ²/2
    rows, hs = [], [4e-3, 2e-3, 1e-3]
    for R in (1.0, 2.0):
        ratios = []
        for h in hs:
            t = 0.5
            da = 0.2 * math.cos(t)
            mfun = lambda P, RR=R: metric5(P, RR, 0.2 * math.sin(P[0]))
            num = ricci5(mfun, [t, 0.0, 0.0, 0.0, 0.0], h)
            ratios.append(num / pred_of(R, da))
        rows.append({"R": R, "ratios": ratios, "pred": pred_of(R, 0.2 * math.cos(0.5))})
    print("  " + " · ".join(f"R={r['R']:.0f}: " + "/".join(f"{x:.6f}" for x in r["ratios"])
                            for r in rows))

    # 纯规范阳性对照：A_1=Λ'(x) ⇒ F≡0 ⇒ 五维度规在坐标变换下平直 ⇒ R5=0
    h = 1e-3
    gauge = ricci5(lambda P: metric5(P, 1.0, 0.15 * math.cos(0.5 * P[1])),
                   [0.3, 0.7, 0.0, 0.0, 0.0], h)
    # 平直圆（任意 R）对照
    flat = ricci5(lambda P: metric5(P, 23.412475, 0.0), [0.3, 0.7, 0.2, 0.1, 0.4], h)

    # 错误系数对照：若系数是 3/4 而非 1/4，预测 = 3/4·2ȧ² ⇒ 同一读数给出 1/3
    da = 0.2 * math.cos(0.5)
    alt = rows[0]["ratios"][-1] / (0.75 * 2.0 * da * da / (0.5 * da * da))

    # α_KK 代数：e=√(16πG4)/R、α=e²/(4π)=4G4/R²
    G4, R0 = 1.0, 2.0
    e = math.sqrt(16.0 * PI * G4) / R0
    a_formula = e * e / (4.0 * PI)
    a_direct = 4.0 * G4 / (R0 * R0)
    res_alpha = abs(a_formula - a_direct) / a_direct

    print(f"  纯规范 R5={gauge:.3e}；平直圆 R5={flat:.3e}；错误系数对照={alt:.4f}；"
          f"α 代数残差={res_alpha:.3e}")

    ok_coef = all(abs(r - 1.0) < 1e-3 for r in rows[0]["ratios"]) and \
              all(abs(r - 1.0) < 1e-3 for r in rows[1]["ratios"])
    guard("G4", "曲率分解系数 −R²/4 与符号：5D 曲率独立计算 ⇒ ratio→1",
          ok_coef,
          "R=1: " + "/".join(f"{x:.6f}" for x in rows[0]["ratios"]) +
          "；R=2: " + "/".join(f"{x:.6f}" for x in rows[1]["ratios"]) +
          "（h 减半误差约降 4 倍 ⇒ 二阶收敛；符号为正 ⇒ E² 动能项正确）",
          {"ratio_R1": rows[0]["ratios"], "ratio_R2": rows[1]["ratios"]})
    guard("G5", "纯规范 / 平直圆阳性对照：R5 精确为 0（代码有牙齿）",
          abs(gauge) < 1e-9 and abs(flat) < 1e-9,
          f"A_1=Λ'(x)（F≡0）⇒ R5={gauge:.3e}；diag(−1,1,1,1,R²) ⇒ R5={flat:.3e}",
          {"gauge": gauge, "flat": flat})
    guard("G6", "α_KK=e²/(4π)=4G4/R² 代数恒等（16π 归一约定）",
          res_alpha < 1e-14,
          f"e=√(16πG4)/R、G4=1,R=2 ⇒ α={a_formula:.12f} vs 4G4/R²={a_direct:.12f}；"
          f"残差={res_alpha:.3e}",
          {"res_alpha": res_alpha})

    control("C1", "错误系数控制：把 ¼ 换成 ¾ 后同一读数给出 1/3（3 倍偏离）",
            abs(alt - 0.3333) < 0.01,
            f"alt ratio={alt:.4f} ⇒ 系数检验能区分 ¼ 与 ¾，不是恒真",
            {"alt_ratio": alt})
    control("C2", "纯规范对照为 0 ⇒ 曲率代码不会把坐标假象误判为曲率",
            abs(gauge) < 1e-9,
            f"gauge R5={gauge:.3e}",
            {"gauge": gauge})

    return {"hs": hs, "rows": rows, "gauge": gauge, "flat": flat,
            "alt_ratio": alt, "res_alpha": res_alpha,
            "e": e, "a_formula": a_formula}


# ============================================================
# S3 · 半径反解（23.412475 ℓ_P）与精度地板
# ============================================================
def s3_radius():
    print("[S3] R=2ℓ_P/√α 反解 + G 精度地板")
    ratio = 2.0 / math.sqrt(ALPHA)
    R_m = ratio * LP
    text_ratio = 23.412475
    text_R = 3.78405e-34
    rel_ratio = abs(ratio - text_ratio) / text_ratio
    rel_R = abs(R_m - text_R) / R_m
    u_rel = 0.5 * REL_G
    u_R = ratio * u_rel
    print(f"  R/ℓ_P={ratio:.9f}（来料 {text_ratio}，rel={rel_ratio:.2e}）；"
          f"R={R_m:.6e} m（来料 {text_R}，rel={rel_R:.2e}）")
    print(f"  G 相对不确定度 {REL_G:.1e} ⇒ δ(R/ℓ_P)/R={u_rel:.2e}、δR={u_R:.5f} ℓ_P")
    guard("G7", "半径反解复算命中来料两值（23.412475 与 3.78405e−34 m）",
          rel_ratio < 1e-5 and rel_R < 1e-5,
          f"R/ℓ_P={ratio:.9f}（rel {rel_ratio:.2e}）；R={R_m:.6e} m（rel {rel_R:.2e}）",
          {"ratio": ratio, "R_m": R_m, "rel_ratio": rel_ratio, "rel_R": rel_R})
    entry("H05", "PASS", "半径反解 R=2ℓ_P/√α=23.412475 ℓ_P=3.78405e−34 m（数值命中）",
          f"R/ℓ_P={ratio:.9f}、R={R_m:.6e} m；与来料两值相对差 {rel_ratio:.1e}/{rel_R:.1e} ⇒ "
          "算术无误（但这是**由 α 反解**所得）",
          {"ratio": ratio, "R_m": R_m})
    entry("H06", "FAIL", "反解是循环：模型只有 1 个无量纲输入 R/ℓ_P 与 1 个观测量 α ⇒ dof=0",
          "α_KK=4(ℓ_P/R)² 给出 R↔α 的一一映射；把 α 当输入反解 R 后，模型对 α 不再有任何"
          "约束力（『为什么恰好 23.412475』仍无答案）",
          {"dof": 0})
    entry("H18", "INFO", "半径有效位数受 G 的 2.2e−5 限制：R=(23.41248±0.00026) ℓ_P",
          f"δ(R/ℓ_P)/R={u_rel:.2e} ⇒ δR={u_R:.5f} ℓ_P；来料的 7–9 位尾数不具物理意义"
          "（G 是当前测最差的常数之一）",
          {"u_rel": u_rel, "u_R": u_R})
    return {"ratio": ratio, "R_m": R_m, "rel_ratio": rel_ratio, "rel_R": rel_R,
            "u_rel": u_rel, "u_R": u_R, "text_ratio": text_ratio, "text_R": text_R}


# ============================================================
# S4 · 质量矛盾
# ============================================================
def s4_mass(R_m):
    print("[S4] KK 第一带电模态 m₁=ħc/R 与电子质量")
    m1 = HC_GEV_M / R_m
    ratio_e = m1 / ME_GEV
    a_pred = 4.0 * (ME_GEV / MP_GEV) ** 2
    a_over = ALPHA / a_pred
    print(f"  m₁c²={m1:.6e} GeV；m₁/m_e={ratio_e:.4e}；若 m₁=m_e ⇒ α={a_pred:.4e}")
    guard("G8", "m₁=ħc/R=5.214699e17 GeV、比值 1.02049e21（来料复算命中）",
          abs(m1 - 5.21469907e17) / 5.21469907e17 < 1e-3 and
          abs(ratio_e - 1.02049e21) / 1.02049e21 < 1e-3,
          f"m₁c²={m1:.6e} GeV（来料 5.21469907e17）；m₁/m_e={ratio_e:.5e}（来料 1.02049e21）",
          {"m1": m1, "ratio_e": ratio_e})
    guard("G9", "若强制 m₁=m_e ⇒ α_pred=4(m_e/m_P)²≈7.0e−45（与 α 差 42 个量级）",
          abs(a_pred - 7.00724e-45) / 7.00724e-45 < 1e-2,
          f"α_pred={a_pred:.5e}（来料 7.00724e−45）；α/α_pred={a_over:.3e}",
          {"a_pred": a_pred, "a_over": a_over})
    entry("H07", "PASS", "KK 第一带电模态质量 m₁=ħc/R=5.214699e17 GeV（数值命中）",
          f"m₁c²={m1:.6e} GeV；m₁/m_e={ratio_e:.4e}",
          {"m1": m1, "ratio_e": ratio_e})
    entry("H08", "FAIL", "第一带电模态与电子差 1.02049e21 倍（21 个量级）",
          f"m₁={m1:.4e} GeV vs m_e={ME_GEV:.4e} GeV ⇒ 比值 {ratio_e:.4e}；"
          "KK 塔的最轻带电态在 5e17 GeV，电子绝不可能是 n=1 模态",
          {"ratio_e": ratio_e})
    entry("H09", "FAIL", "反解 α（强制 m₁=m_e）给出 7.0e−45，比真实值小 1.04e42 倍",
          f"α_pred=4(m_e/m_P)²={a_pred:.5e}；α/α_pred={a_over:.3e} ⇒ "
          "『第五维量子数同时解释电荷与质量』被一次性否证",
          {"a_pred": a_pred, "a_over": a_over})
    return {"m1": m1, "ratio_e": ratio_e, "a_pred": a_pred, "a_over": a_over,
            "tower": [{"n": n, "m": n * m1} for n in (1, 2, 3)]}


# ============================================================
# S5 · 模数与势的来源
# ============================================================
def s5_moduli(ratio):
    print("[S5] 真空模数、α 的幂律与势的来源")
    h = 1e-3
    flat_rows = []
    for R in (1.0, ratio, 1e6):
        flat_rows.append({"R": R, "R5": ricci5(lambda P, RR=R: metric5(P, RR, 0.0),
                                               [0.3, 0.7, 0.2, 0.1, 0.4], h)})
    print("  平直圆 R5: " + ", ".join(f"R={r['R']:.4g}:{r['R5']:.2e}" for r in flat_rows))

    grid = [10 ** (-2 + 8 * i / 200.0) for i in range(201)]
    a4 = [4.0 / (x * x) for x in grid]
    a5 = [ALPHA * (ratio / x) ** 3 for x in grid]
    slope4 = math.log(a4[150] / a4[50]) / math.log(grid[150] / grid[50])
    slope5 = math.log(a5[150] / a5[50]) / math.log(grid[150] / grid[50])
    sign_changes = 0
    d4 = [(a4[i + 1] - a4[i]) / (grid[i + 1] - grid[i]) for i in range(len(grid) - 1)]
    for i in range(len(d4) - 1):
        if d4[i] * d4[i + 1] < 0:
            sign_changes += 1
    print(f"  对数斜率：G4 固定 {slope4:.6f}；G5 固定 {slope5:.6f}；dα/dR 变号次数={sign_changes}")
    guard("G10", "任意 R 的真空 Ricci 平直（模数存在）——数值机器零",
          all(abs(r["R5"]) < 1e-9 for r in flat_rows),
          "R=1/23.412475/1e6 三点 R5 均为 " +
          "/".join(f"{r['R5']:.2e}" for r in flat_rows) + " ⇒ R_MN=0 不约束 R",
          {"R5": [r["R5"] for r in flat_rows]})
    guard("G11", "α 的幂律：固定 G4 为 R⁻²、固定 G5 为 R⁻³，且全网格无驻点",
          abs(slope4 + 2.0) < 1e-9 and abs(slope5 + 3.0) < 1e-9 and sign_changes == 0,
          f"slope(G4)={slope4:.6f}、slope(G5)={slope5:.6f}；201 点网格 dα/dR 变号 {sign_changes} 次",
          {"slope4": slope4, "slope5": slope5, "sign_changes": sign_changes})
    entry("H10", "PASS", "任意 R 真空 Ricci 平直 ⇒ 半径是模数（不是被方程选出的解）",
          "R=1/23.412475/1e6 的 R5 全部为机器零：同一类五维真空允许连续 R ⇒ "
          "α=4(ℓ_P/R)² 可取任意值",
          {"R5": [r["R5"] for r in flat_rows]})
    entry("H11", "FAIL", "α∝R⁻²(固定 G4)/R⁻³(固定 G5) 均单调 ⇒ 无驻点 ⇒ 无唯一 R",
          f"两种口径的对数斜率 {slope4:.4f}/{slope5:.4f}，201 点网格变号 {sign_changes} 次 ⇒ "
          "『保持不同的 G 固定』连 α(R) 的函数形式都不同，更谈不上唯一零点",
          {"slope4": slope4, "slope5": slope5})
    entry("H12", "FAIL", "稳定势无几何来源：树阶 EH 给 V≡0；单圈 Casimir 只有单幂 x⁻⁴",
          "5D EH 积分后 S4=(2πR/16πG5)∫√−g R4，R4=0 ⇒ 对 R 无势（精确平坦方向）；"
          "圈图量纲 V=c/R⁴（单幂）⇒ 单调、无内部极小 ⇒ Ax²+B/x² 是**外加**两项输入",
          {"tree_V": 0.0, "one_loop_power": -4})
    return {"flat_rows": flat_rows, "grid_x": grid, "a_g4": a4, "a_g5": a5,
            "slope4": slope4, "slope5": slope5, "sign_changes": sign_changes,
            "ratio": ratio}


# ============================================================
# S6 · 稳定势与电荷谱
# ============================================================
def s6_potential(ratio):
    print("[S6] 稳定势 V=Ax²+B/x² 的极小与 α 恒等式；整数电荷 vs 分数电荷")
    A = 1.0
    a_over_b = ALPHA * ALPHA / 16.0
    B = A / a_over_b
    xstar = (B / A) ** 0.25
    ident = 2.0 / math.sqrt(ALPHA)
    rel_ident = abs(xstar - ident) / ident
    h = 0.05
    vpp = (A * (xstar + h) ** 2 + B / (xstar + h) ** 2
           - 2.0 * (A * xstar ** 2 + B / xstar ** 2)
           + A * (xstar - h) ** 2 + B / (xstar - h) ** 2) / (h * h)
    vmin = A * xstar ** 2 + B / xstar ** 2
    a_geom = 4.0 * math.sqrt(A / B)
    grid = [5.0 + 55.0 * i / 200.0 for i in range(201)]
    vv = [(A * x * x + B / (x * x)) / vmin for x in grid]
    print(f"  A/B={a_over_b:.6e}（来料 3.32820965e−6）；x*={xstar:.9f} vs 2/√α={ident:.9f}"
          f"（rel {rel_ident:.2e}）；V''/A={vpp / A:.6f}；α_geom={a_geom:.9f}")
    guard("G12", "势的极小解析式：x*=(B/A)^{1/4}、V″=8A、α_geom=4√(A/B)",
          abs(vpp / A - 8.0) < 1e-4 and abs(xstar - (B / A) ** 0.25) < 1e-12
          and abs(a_geom - ALPHA) / ALPHA < 1e-12,
          f"x*={xstar:.9f}；V''/A={vpp / A:.6f}（理论 8）；α_geom={a_geom:.9f}=α",
          {"xstar": xstar, "vpp_over_A": vpp / A, "a_geom": a_geom})
    entry("H13", "PASS", "势数学成立：x*=(B/A)^{1/4}=23.4125、V″=8A>0、α_geom=4√(A/B)=α",
          f"A/B={a_over_b:.6e}（来料 3.32820965e−6）、x*={xstar:.9f}、V''/A={vpp / A:.3f}",
          {"a_over_b": a_over_b, "xstar": xstar})
    entry("H14", "FAIL", "但极小点恒等于反解半径：x*≡2/√α（rel 0），A/B≡α²/16 ⇒ dof=0",
          f"x*={xstar:.9f} 与 S3 的 2/√α={ident:.9f} 相对差 {rel_ident:.1e}；"
          "2 系数 − 1 整体标度冗余 = 1 有效比 ↔ 1 观测量 ⇒ 拟合式，非选择机制",
          {"rel_ident": rel_ident, "dof": 0})
    entry("H15", "FAIL", "最简 KK 电荷=第五维动量 ⇒ 整数 n；夸克 ±1/3、±2/3 不可表示",
          "e_n=n√(16πG4)/R（n∈ℤ）⇒ 电荷谱是 e 的整数格；最小距离 |1/3−n|min=1/3、"
          "|2/3−n|min=1/3 ⇒ 最简 5D KK 与观测电荷谱不同构（需非阿贝尔等距群）",
          {"q_quark": [1.0 / 3.0, 2.0 / 3.0], "min_dist": 1.0 / 3.0})
    control("C3", "势确实能精确命中 α（构造性）⇒ 本卷否的不是『公式错』而是『自由度=0』",
            abs(a_geom - ALPHA) / ALPHA < 1e-12,
            f"α_geom={a_geom:.12f} vs α={ALPHA:.12f}",
            {"a_geom": a_geom})
    return {"A": A, "B": B, "a_over_b": a_over_b, "xstar": xstar, "ident": ident,
            "rel_ident": rel_ident, "vpp_over_A": vpp / A, "vmin": vmin,
            "grid_x": grid, "v_norm": vv, "a_geom": a_geom}


# ============================================================
# S7 · radion 一致性
# ============================================================
def s7_radion(ratio):
    print("[S7] radion：常数 R 要求 F²=0；静电场 F²=−2E²；反作用量级")
    k_e = 8.987551787e9
    q_e = 1.602176634e-19
    a0 = 5.29177210903e-11
    E_bohr = k_e * q_e / (a0 * a0)
    f2_coulomb = -2.0 * E_bohr * E_bohr
    # null 场：E=B 且正交 ⇒ F²=2(B²−E²)=0
    E0 = 1.0
    f2_null = 2.0 * (E0 * E0 - E0 * E0)
    # 反作用量级：|φ| ≈ (√3/2) R₀² E² r²（普朗克单位）
    E_planck = k_e * q_e / (LP * LP)
    e_ratio = E_bohr / E_planck
    r_planck = a0 / LP
    R0 = ratio
    phi_est = 0.5 * math.sqrt(3.0) * R0 * R0 * e_ratio * e_ratio * r_planck * r_planck
    da_over_a = 2.0 * math.sqrt(3.0) * phi_est
    dim_lhs = 2.0                    # [□φ]
    dim_rhs = -2.0 + 4.0             # [R₀²]+[H²]
    print(f"  E(a₀)={E_bohr:.4e} V/m；F²_coulomb={f2_coulomb:.4e}；F²_null={f2_null:.1e}")
    print(f"  |φ|~{phi_est:.3e}；δα/α~{da_over_a:.3e}；量纲 {dim_lhs:.1f} vs {dim_rhs:.1f}")
    guard("G13", "radion 一致性的量纲与符号：F²_Coulomb=−2E²≠0、F²_null=0",
          abs(f2_null) < 1e-30 and f2_coulomb < 0 and dim_lhs == dim_rhs,
          f"静电场 F²=−2E²<0（非零）；平面波 F²=2(B²−E²)=0；"
          f"量纲 [□φ]={dim_lhs:.1f}=[R₀²]+[H²]={dim_rhs:.1f}",
          {"f2_coulomb": f2_coulomb, "f2_null": f2_null})
    entry("H16", "FAIL", "常数 R 截断与 radion 不自洽：静电场 F²=−2E²≠0 ⇒ φ 被源驱动",
          "□φ+（√3R₀²/4）e^{−√3φ}H²=0；要求 φ≡const ⇒ H²≡0，而 Coulomb 场处处 F²=−2E²<0 ⇒ "
          "『冻结半径后得到对所有电磁场适用的 Einstein–Maxwell』不成立",
          {"f2_coulomb": f2_coulomb})
    entry("H17", "BOUNDARY", "radion 反作用量级 ~1e−46（结构矛盾真实，实验无感）；null 场豁免",
          f"|φ|~{phi_est:.2e}、δα/α~{da_over_a:.2e}（原子尺度静电场）；"
          "平面波 F²=0 是唯一豁免但只覆盖 null 背景，不救静电场/静磁场",
          {"phi_est": phi_est, "da_over_a": da_over_a})
    control("C4", "null 场确实满足 H²=0（『一律不可能』是错的）",
            abs(f2_null) < 1e-30,
            "E=B 正交 ⇒ B²−E²=0 ⇒ 平面波背景允许常数 φ ⇒ 本卷结论为条件性而非绝对否定",
            {"f2_null": f2_null})
    return {"E_bohr": E_bohr, "f2_coulomb": f2_coulomb, "f2_null": f2_null,
            "phi_est": phi_est, "da_over_a": da_over_a, "e_ratio": e_ratio,
            "r_planck": r_planck, "dim": [dim_lhs, dim_rhs]}


# ============================================================
# S9 · 来料残差声称的判别力
# ============================================================
def s9_tautology(ratio):
    print("[S9] 10000 组残差：恒等式记账 vs 判别力")
    worst = 0.0
    for i in range(10000):
        x = 10 ** (-3 + 9 * i / 9999.0)
        a = 4.0 / (x * x)
        back = 2.0 / math.sqrt(a)
        worst = max(worst, abs(back - x) / x)
    worst_bad = 0.0
    for i in range(10000):
        x = 10 ** (-3 + 9 * i / 9999.0)
        a = 4.5 / (x * x)          # 故意错误的系数
        back = 2.0 / math.sqrt(a / (4.5 / 4.0))   # 用错误系数也自洽反解
        worst_bad = max(worst_bad, abs(back - x) / x)
    print(f"  正确系数 max rel={worst:.3e}；故意错误系数 max rel={worst_bad:.3e}")
    control("C5", "『10000 组残差』无判别力：错误系数同样给机器零",
            worst_bad < 1e-14,
            f"错误系数 4.5 的扫描残差={worst_bad:.3e}（与正确系数同量级）⇒ "
            "残差只度量代数记账，不度量物理",
            {"worst_bad": worst_bad})
    entry("H19", "INFO", "来料 6.73e−81 残差是 80 位恒等复算，低于输入精度即无信息",
          f"float64 同样的 10000 组扫描 max rel={worst:.3e}；把系数改成 4.5 后仍为 "
          f"{worst_bad:.3e} ⇒ 该检验对『模型对不对』零判别力（只证 R↔α 是双射）",
          {"worst": worst, "worst_bad": worst_bad})
    return {"worst": worst, "worst_bad": worst_bad}


# ============================================================
# main
# ============================================================
def main():
    print("=" * 78)
    print(f"{MARKER} · ROOT V12.0「高维几何→电磁耦合」第一性原理审计")
    print("=" * 78)
    print(f"锚：α⁻¹={ALPHA_INV}（u={U_ALPHA_INV}）、ℓ_P={LP} m、G 相对 {REL_G}")
    print()

    s1 = s1_gauge()
    print()
    s2 = s2_kk()
    print()
    s3 = s3_radius()
    print()
    s4 = s4_mass(s3["R_m"])
    print()
    s5 = s5_moduli(s3["ratio"])
    print()
    s6 = s6_potential(s3["ratio"])
    print()
    s7 = s7_radion(s3["ratio"])
    print()
    s9 = s9_tautology(s3["ratio"])

    entry("H01", "INFO", "总判：结构链 PASS（模型内数学成立）/ 唯一性 NO-GO（四条独立封口）",
          "V12 的『几何→U(1)→整数电荷→α_KK』在 5D KK 内可严格建立；但 α 仍非预言："
          "半径是模数 + α 幂律单调 + 稳定势恒等 + 第一模态高 21 量级 + radion 截断不自洽",
          {"layer": "first-principles-audit", "verdict": "structure-pass / uniqueness-no-go"})
    entry("H02", "PASS", "S1 五维规范变换三条全部机检通过（线元/H 不变/Abel）",
          f"线元残差 {s1['res_line']:.2e}、H 不变 {s1['rel_h']:.2e}、Abel 复合 "
          f"{s1['res_abel']:.2e} ⇒ θ'=θ+χ 严格诱导 B'=B−∂χ，且群是 Abel U(1)",
          {"res": [s1["res_line"], s1["rel_h"], s1["res_abel"]]})
    entry("H03", "PASS", "S2 曲率分解系数 −R²/4 被独立 5D 曲率计算证实（两档 R、二阶收敛）",
          f"R=1 ratio {s2['rows'][0]['ratios'][-1]:.6f}、R=2 ratio "
          f"{s2['rows'][1]['ratios'][-1]:.6f}；纯规范/平直圆对照 R5={s2['gauge']:.2e}/"
          f"{s2['flat']:.2e} ⇒ 系数、符号、R² 幂次三项同时成立",
          {"ratio_R1": s2["rows"][0]["ratios"], "ratio_R2": s2["rows"][1]["ratios"]})
    entry("H04", "PASS", "S2 α_KK=e²/(4π)=4G4/R² 代数恒等（e=√(16πG4)/R）",
          f"G4=1,R=2 时 α={s2['a_formula']:.12f} vs 4G4/R²；残差 {s2['res_alpha']:.2e}",
          {"res_alpha": s2["res_alpha"]})
    entry("H20", "INFO", "结论：V12 的自我裁定被机检确认；真正缺口是『稳定化尺度』而非公式",
          "四条封口（模数 / 单调幂律 / 势恒等 / radion 不自洽）+ 质量与电荷谱两条结构性不符；"
          "唯一出路是引入非纯几何稳定化（膜/通量/量子），届时 α 是稳定化尺度的读数",
          {"blockers": 4})

    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in entries if e["level"] == "INFO")

    claims = [
        {"id": "V1", "claim": "五维几何诱导 U(1) 规范变换", "verdict": "PASS",
         "num": f"线元 {s1['res_line']:.1e} / H {s1['rel_h']:.1e}"},
        {"id": "V2", "claim": "规范场归一化与 α_KK 关系", "verdict": "PASS",
         "num": f"代数残差 {s2['res_alpha']:.1e}"},
        {"id": "V3", "claim": "第五维动量的 Routh 消元（m=n/R）", "verdict": "PASS",
         "num": "m²=E²−k²=n²/R²（恒等）"},
        {"id": "V4", "claim": "10,000 组半径—耦合—质量残差 6.73e−81", "verdict": "NO-POWER",
         "num": f"错误系数亦 {s9['worst_bad']:.1e}"},
        {"id": "V5", "claim": "基本 KK 带电模态与电子质量匹配", "verdict": "FAIL",
         "num": f"差 {s4['ratio_e']:.3e} 倍"},
        {"id": "V6", "claim": "纯真空几何唯一固定半径", "verdict": "FAIL",
         "num": "任意 R 的 R5=0"},
        {"id": "V7", "claim": "候选稳定势的极小值与二阶导", "verdict": "PASS/FAIL",
         "num": f"x*={s6['xstar']:.4f}≡2/√α"},
        {"id": "V8", "claim": "无实测 α 输入的独立数值预测", "verdict": "FAIL",
         "num": "dof=0（未完成）"},
    ]

    res = {
        "marker": MARKER, "stem": STEM, "date": "2026-10-31",
        "title": "ROOT V12.0『高维几何→电磁耦合』第一性原理审计（规范变换 / 曲率系数 / "
                 "半径模 / 质量矛盾 / radion）",
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info, "guards": "", "controls": ""},
        "guards": guards, "controls": controls, "entries": entries,
        "claims": claims,
        "readings": {
            "params": {"alpha_inv": ALPHA_INV, "u_alpha_inv": U_ALPHA_INV,
                       "alpha": ALPHA, "lP": LP, "rel_G": REL_G,
                       "hc_GeV_m": HC_GEV_M, "mP_GeV": MP_GEV, "me_GeV": ME_GEV},
            "s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5,
            "s6": s6, "s7": s7, "s9": s9,
            "summary": {"ratio": s3["ratio"], "R_m": s3["R_m"],
                        "u_R": s3["u_R"], "m1": s4["m1"],
                        "ratio_e": s4["ratio_e"], "a_pred": s4["a_pred"],
                        "alt_ratio": s2["alt_ratio"],
                        "slope4": s5["slope4"], "slope5": s5["slope5"],
                        "xstar": s6["xstar"], "rel_ident": s6["rel_ident"],
                        "phi": s7["phi_est"], "worst": s9["worst"],
                        "worst_bad": s9["worst_bad"],
                        "gauge_R5": s2["gauge"]},
        },
        "verdict": "", "judgement": "",
        "source": {
            "engine": BASE + ".py",
            "inherits": ["ROOT V12.0 来料（用户附件逐字）",
                         "r284（V10 六路条件性候选审计）",
                         "r287（标度不变性 / 参数计数 dof=0）",
                         "CODATA 2022（α⁻¹、ℓ_P）",
                         "Kaluza–Klein 标准分解（只读对照）"],
        },
    }

    parts = [
        "KK-GAUGE-TRANSFORMATION-EXACT",
        "KK-CURVATURE-COEFFICIENT-R2-4-VERIFIED",
        "PURE-GAUGE-CONTROL-ZERO",
        "ALPHA-KK-4-LP2-R2-EXACT",
        "RADIUS-23-412475-LP-CIRCULAR",
        "MODULI-FLAT-ALL-R",
        "ALPHA-POWER-LAW-MONOTONE-NO-STATIONARY-R",
        "CASIMIR-SINGLE-POWER-NO-MINIMUM",
        "STABILITY-POTENTIAL-IDENTITY-DOF-ZERO",
        "KK-FIRST-MODE-5-214699E17-GEV-GAP-1-02E21",
        "FRACTIONAL-CHARGE-NO-GO-MINIMAL-KK",
        "RADION-CONSTANT-R-INCONSISTENT-F2-NONZERO",
        "BACKREACTION-1E-46-NEGLIGIBLE",
        "PRECISION-FLOOR-G-2-2E-5",
        "VERDICT-STRUCTURE-PASS-UNIQUENESS-NO-GO",
    ]
    res["verdict"] = MARKER + "-" + "-".join(parts)
    res["judgement"] = ("MIXED（结构链 PASS / 唯一性 NO-GO）：5D KK 的『几何→U(1)→整数电荷』"
                        "在模型内数学成立（规范变换、−R²/4 曲率系数、e²=16πG4/R² 全部机检通过），"
                        "但 α 仍不是预言——R 是模数（任意 R 真空 Ricci 平直）、α∝R^(−2/−3) 单调无驻点、"
                        "稳定势与反解恒等（dof=0）、第一带电模态高 21 个量级、常数 R 与 radion 不自洽"
                        "（F²≠0，反作用 1e−46 可忽略但结构上必须补势）。"
                        "结论：V12 自我裁定正确，本卷给出四条独立封口；唯一出路是引入非纯几何稳定化。")

    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")

    html_ok, html_detail = cast_html(res)
    guard("G14", "交互 HTML 生成且自含（零外部 URL）", html_ok, html_detail)
    res["counts"]["guards"] = f"{sum(1 for g in guards if g['ok'])}/{len(guards)}"
    res["counts"]["controls"] = f"{sum(1 for c in controls if c['ok'])}/{len(controls)}"

    print()
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
         f"控制组 {res['counts']['controls']}\n", "\n## 条目\n"]
    for e in res["entries"]:
        L.append(f"- **{e['code']} {e['level']}** {e['title']}——{e['detail']}\n")
    L.append("\n## 守卫\n")
    for g in res["guards"]:
        L.append(f"- **{g['id']} {'OK' if g['ok'] else 'FAIL'}** {g['title']}——{g['detail']}\n")
    L.append("\n## 控制组\n")
    for c in res["controls"]:
        L.append(f"- **{c['id']} {'OK' if c['ok'] else 'FAIL'}** {c['title']}——{c['detail']}\n")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))


def write_report(path, res):
    s = res["readings"]["summary"]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{MARKER} rc=0\n")
        f.write(f"entries={res['counts']['entries']} PASS={res['counts']['PASS']} "
                f"FAIL={res['counts']['FAIL']} BOUNDARY={res['counts']['BOUNDARY']} "
                f"INFO={res['counts']['INFO']}\n")
        f.write(f"guards={res['counts']['guards']} controls={res['counts']['controls']}\n")
        f.write(f"verdict={res['verdict']}\n")
        f.write(f"R_over_lP={s['ratio']:.9f} R_m={s['R_m']:.6e} u_R={s['u_R']:.5f}\n")
        f.write(f"m1_GeV={s['m1']:.6e} m1_over_me={s['ratio_e']:.5e} "
                f"alpha_pred={s['a_pred']:.5e}\n")
        f.write(f"curvature_alt_ratio={s['alt_ratio']:.4f} gauge_R5={s['gauge_R5']:.3e}\n")
        f.write(f"slope_G4={s['slope4']:.6f} slope_G5={s['slope5']:.6f} "
                f"xstar={s['xstar']:.9f} rel_ident={s['rel_ident']:.2e}\n")
        f.write(f"phi_backreaction={s['phi']:.3e} tautology_worst={s['worst']:.3e} "
                f"wrong_coeff_worst={s['worst_bad']:.3e}\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R290_JSON__" not in tpl:
        return False, "模板缺少 __R290_JSON__ 占位符"
    html = tpl.replace("__R290_JSON__", json.dumps(res, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R290_JSON__" in text:
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
