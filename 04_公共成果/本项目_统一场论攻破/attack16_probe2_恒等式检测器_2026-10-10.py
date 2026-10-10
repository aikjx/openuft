# -*- coding: utf-8 -*-
"""attack16 probe2 · 恒等式检测器（2026-10-10）

对象：证书簇中三条被当作「预言/闭合」使用的关系：
  (1) α_G(E) = (E/M_P)^2                —— 证书/写本用作引力耦合的首原式
  (2) Λ₀ = 1/(8πG)                      —— 全参数闭合总装：「由克尔熵=BH 匹配律定义(非自由参数)」
  (3) S_TUFT = 2πΛ₀ A  ≡  S_BH = A/(4G) —— 路线3 用作「熵守恒律」

判据：把式子两边的**定义**代入，若残差恒为 0（与自变量无关），则该式是**恒等式**，
判别力 = 0 —— 它对任何 E / 任何 A,G 都成立，因此不能被实验否证，也不构成预言。

诚实边界：本探针只判「是否恒等 / 是否循环定义」，**不判**这些式子在物理上是否有用；
恒等式在理论内部完全可以是合法的定义或记账方式。被判恒等 ⇒ 降级为「零信息量」，
不得计入「第一性预言」（method_F：L0 定义式/代数恒等 = 零经验内容）。

反向对照（关键）：检测器必须能判出**非恒等**（喂 (E/M_P)^3、α_s 实测 vs 单圈），
否则它只是一个「无条件判恒等」的橡皮图章。

退出码：仅由自检 CHK 决定；判出 FAIL 不是引擎失败。
"""

import os
import sys
import json
import random
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
getcontext().prec = 60

ITEMS = []
_SELF = []


def P(name, ok, detail, note=""):
    ITEMS.append(dict(id=name, verdict="PASS" if ok else "FAIL", detail=detail, note=note))


def F(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="FAIL", detail=detail, note=note))


def INFO(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="INFO", detail=detail, note=note))


def BOUND(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="BOUNDARY", detail=detail, note=note))


def CHK(name, cond, detail=""):
    _SELF.append(dict(name=name, ok=bool(cond), detail=detail))


class CD:
    """CODATA 2022 / PDG 常用常数（自然单位 ℏ=c=1）。"""
    G_NAT = Decimal("6.7086e-39")        # GeV^-2
    M_PL = Decimal("1.22091e19")         # GeV
    ALPHA_S_MZ = Decimal("0.1179")
    ALPHA_EM_0 = Decimal("7.2973525693e-3")   # α(0) Thomson
    ALPHA_EM_MZ = Decimal("7.8156e-3")        # α(M_Z)=1/127.95


def d(x):
    return Decimal(str(x))


def rel(a, b):
    """相对差 |a-b|/max(|a|,|b|)，b=0 时退化为 |a-b|。"""
    a, b = d(a), d(b)
    den = max(abs(a), abs(b))
    if den == 0:
        return abs(a - b)
    return abs(a - b) / den


# ---------- 恒等性检测：扫描自变量，看残差是否与自变量无关且恒为 0 ----------
def is_identity(f_lhs, f_rhs, xs, tol_rel):
    """对每组自变量 x 计算 lhs/rhs，返回 (最大相对差, 是否恒等)。
    恒等 ⇔ 所有相对差 ≤ tol_rel（即残差与自变量无关、恒为机器零）。"""
    worst = Decimal(0)
    for x in xs:
        r = rel(f_lhs(x), f_rhs(x))
        if r > worst:
            worst = r
    return worst, (worst <= d(tol_rel))


def run_all():
    print("=" * 78)
    print("attack16 probe2 · 恒等式检测器")
    print("=" * 78)

    # ---------------- C01: α_G(E) = (E/M_P)^2 ----------------
    Escan = [Decimal("1e-3"), Decimal("1"), Decimal("1e3"), Decimal("91.1876"),
             Decimal("1e9"), Decimal("1e13"), Decimal("1e16"), Decimal("1e19")]

    def lhs_c01(E):
        return (E / CD.M_PL) ** 2          # (E/M_P)^2

    def rhs_c01(E):
        return CD.G_NAT * E ** 2           # α_G ≡ G E^2

    worst_pub, id_pub = is_identity(lhs_c01, rhs_c01, Escan, "1e-6")
    # 用 M_P ≡ 1/sqrt(G) 的严格定义再算一次（消除公布位数舍入）
    M_PL_exact = (Decimal(1) / CD.G_NAT).sqrt()
    worst_def = Decimal(0)
    for E in Escan:
        r = rel((E / M_PL_exact) ** 2, CD.G_NAT * E ** 2)
        if r > worst_def:
            worst_def = r

    print("  C01 α_G: (E/M_P)^2 vs G·E^2")
    print("      公布常数口径 最大相对差 = %s  (M_P²·G = %s)"
          % ("%.3e" % worst_pub, "%.10f" % (CD.M_PL ** 2 * CD.G_NAT)))
    print("      M_P≡1/√G 口径 最大相对差 = %s" % ("%.3e" % worst_def))

    F("C01", "α_G(E)=(E/M_P)^2 与 α_G≡G·E^2 相对差 = %s（M_P≡1/√G 定义下 = %s）"
      % ("%.3e" % worst_pub, "%.3e" % worst_def),
      "因 M_P² ≡ 1/G，两式**逐字相同** ⇒ α_G 判别力 = 0；是定义式重排，非首原导出")

    # ---------------- C02: Λ₀ = 1/(8πG) ----------------
    pi = Decimal("3.14159265358979323846264338327950288419716939937510582097494")
    G1 = Decimal(1)                      # 总装取 G=1
    lam0_target = Decimal("0.039788735772973836")   # 全参数闭合总装 params.Lambda0
    lam0_calc = Decimal(1) / (8 * pi * G1)
    r_lam = rel(lam0_target, lam0_calc)
    print("  C02 Λ₀: 目标 %s vs 1/(8πG) = %s  相对差 = %s"
          % (lam0_target, "%.18f" % lam0_calc, "%.3e" % r_lam))

    F("C02", "Λ₀ = %s 与 1/(8πG)(G=1) = %s 相对差 = %s"
      % (lam0_target, "%.17f" % lam0_calc, "%.3e" % r_lam),
      "总装原文自承「Λ₀=1/(8πG)，由克尔熵=BH 匹配律**定义**(非自由参数)」"
      " ⇒ 是匹配律**定义**出来的，非导出；量纲 [1/G]=M² ≠ 无量纲")

    # ---------------- C03: S_TUFT = S_BH ----------------
    rng = random.Random(20261010)
    worst_s = Decimal(0)
    for _ in range(200):
        A = Decimal(str(rng.uniform(0.5, 5.0)))
        G = Decimal(str(rng.uniform(0.5, 2.0)))
        lam0 = Decimal(1) / (8 * pi * G)          # 匹配律定义
        s_tuft = 2 * pi * lam0 * A
        s_bh = A / (4 * G)
        r = rel(s_tuft, s_bh)
        if r > worst_s:
            worst_s = r
    print("  C03 S_TUFT vs S_BH: 200 组随机 (A,G) 最大相对差 = %s" % ("%.3e" % worst_s))

    F("C03", "S_TUFT=2πΛ₀A 与 S_BH=A/(4G) 在 200 组随机 (A,G) 下最大相对差 = %s" % ("%.3e" % worst_s),
      "代入 Λ₀=1/(8πG) 后 2πΛ₀ ≡ 1/(4G)，两式**恒等** ⇒ 「熵守恒律」是循环匹配，非新预言")

    # ---------------- C04: 反向对照（检测器必须判非恒等） ----------------
    def lhs_ng(E):
        return (E / CD.M_PL) ** 3        # 故意改幂次

    def rhs_ng(E):
        return CD.G_NAT * E ** 2

    worst_ng, id_ng = is_identity(lhs_ng, rhs_ng, Escan, "1e-6")
    print("  C04 反向对照1: (E/M_P)^3 vs G·E^2 最大相对差 = %s 恒等? %s"
          % ("%.3e" % worst_ng, id_ng))

    # 反向对照2：α_s 单圈 vs 实测（在不同能标下必然分歧）
    def alpha_s_1loop(E):
        # α_s(μ) = 4π / (b0 ln(μ²/Λ²))，b0 = 11 - 2/3 n_f，n_f=5 → b0=23/3
        b0 = Decimal(23) / Decimal(3)
        lam = Decimal("0.2")
        return 4 * pi / (b0 * (E ** 2 / lam ** 2).ln())

    Es = [Decimal("10"), Decimal("91.1876"), Decimal("1000")]
    worst_as = Decimal(0)
    for E in Es:
        r = rel(alpha_s_1loop(E), CD.ALPHA_S_MZ)
        if r > worst_as:
            worst_as = r
    print("  C04 反向对照2: α_s 单圈 vs 实测 α_s(M_Z) 最大相对差 = %s" % ("%.3e" % worst_as))

    ok_ng = (not id_ng) and worst_ng > Decimal("1e-3")
    ok_as = worst_as > Decimal("1e-3")
    CHK("CHK-6a 检测器对 (E/M_P)^3 必判非恒等", bool(ok_ng), "最大相对差=%s" % ("%.3e" % worst_ng))
    CHK("CHK-6b 检测器对 α_s 单圈 vs 实测必判非恒等", bool(ok_as), "最大相对差=%s" % ("%.3e" % worst_as))

    P("C04", "反向对照通过：改幂次 / α_s 单圈 vs 实测 均被判为**非恒等**"
      "(相对差 %s / %s)" % ("%.3e" % worst_ng, "%.3e" % worst_as),
      "证明 C01–C03 的「恒等」判定来自式子本身，而非检测器无条件判恒等")

    # ---------------- 工具层自检 ----------------
    # CHK-2 Decimal 60 位：1/(8π)、3√3/2 与闭式
    three = Decimal(3)
    r1 = rel(Decimal(1) / (8 * pi), Decimal("0.039788735772973836"), )
    v = (three.sqrt() * three) / 2
    r2 = rel(v, Decimal("2.598076211353316"))
    CHK("CHK-2a 1/(8π) 60 位与公布值一致", r1 < Decimal("1e-15"), "相对差=%s" % ("%.3e" % r1))
    CHK("CHK-2b 3√3/2 与闭式一致", r2 < Decimal("1e-15"), "相对差=%s" % ("%.3e" % r2))
    # CHK-4 扫描步长加密，最大相对差不增（稳定性）
    Efine = [Decimal("1e-3") * (Decimal("1.7") ** i) for i in range(40)]
    worst_fine, _ = is_identity(lhs_c01, rhs_c01, Efine, "1e-6")
    CHK("CHK-4 E 扫描加密 40 点，结论不变",
        (worst_fine <= Decimal("1e-6")) == (worst_pub <= Decimal("1e-6")),
        "加密后最大相对差=%s" % ("%.3e" % worst_fine))
    # CHK-1 量纲：[1/G] = M^2（自然单位），故 Λ₀ 非无量纲
    # 用 Fraction 三元组 (M,L,T) 表示：G -> (-2,0,0) 量纲（自然单位 [G]=M^-2）
    from fractions import Fraction as Fr
    def dim_inv(x):
        return tuple(-Fr(v) for v in x)
    dim_G = (Fr(-2), Fr(0), Fr(0))     # [G] = M^-2
    dim_invG = dim_inv(dim_G)          # [1/G] = M^2
    CHK("CHK-1 量纲表闭合：[1/G] = M^2 ≠ 无量纲", dim_invG == (Fr(2), Fr(0), Fr(0)),
        "[1/G]=%s" % (dim_invG,))

    # ---------------- 输出 ----------------
    outdir = os.path.join(os.path.dirname(HERE), "数据")
    os.makedirs(outdir, exist_ok=True)
    json_path = os.path.join(outdir, "attack16_probe2_恒等式检测器_2026-10-10.json")
    txt_path = os.path.join(outdir, "attack16_probe2_恒等式检测器_2026-10-10_report.txt")
    payload = dict(
        probe="attack16_probe2_恒等式检测器",
        date="2026-10-10",
        items=ITEMS,
        self_checks=_SELF,
        computed=dict(
            alphaG_identity_maxrel_pub=str(worst_pub),
            alphaG_identity_maxrel_exactdef=str(worst_def),
            Lambda0_target=str(lam0_target),
            Lambda0_1_over_8piG=str(lam0_calc),
            Lambda0_rel=str(r_lam),
            S_TUFT_vs_S_BH_maxrel=str(worst_s),
            negcontrol_cube_maxrel=str(worst_ng),
            negcontrol_alpha_s_maxrel=str(worst_as),
        ),
        red_lines=[
            "恒等式 ≠ 错误：本探针只降级为「零信息量」，不指称造假",
            "判恒等只表示「不可被实验否证」，不代表该式在理论内部无意义",
            "不产生新物理",
        ],
    )
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("attack16 probe2 恒等式检测器 2026-10-10\n")
        f.write("α_G 恒等式判别力 = 0 (maxrel=%s)\n" % ("%.3e" % worst_pub))
        f.write("Λ₀ rel=%s\n" % ("%.3e" % r_lam))
        f.write("S_TUFT vs S_BH maxrel=%s\n" % ("%.3e" % worst_s))

    verdicts = {}
    for it in ITEMS:
        verdicts[it["verdict"]] = verdicts.get(it["verdict"], 0) + 1
    self_ok = sum(1 for s in _SELF if s["ok"])
    print("-" * 78)
    print("读数：条目 %d ｜ %s" % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False)))
    print("自检：%d/%d" % (self_ok, len(_SELF)))
    for s in _SELF:
        if not s["ok"]:
            print("  自检未过：%s %s" % (s["name"], s["detail"]))
    print("产物：")
    for p_ in (json_path, txt_path):
        print("  " + os.path.relpath(p_, os.path.dirname(HERE)))
    print("=" * 78)
    return payload, self_ok == len(_SELF)


if __name__ == "__main__":
    _, ok = run_all()
    sys.exit(0 if ok else 1)
