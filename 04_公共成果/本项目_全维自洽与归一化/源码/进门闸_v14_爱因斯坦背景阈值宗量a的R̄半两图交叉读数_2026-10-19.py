# -*- coding: utf-8 -*-
r"""进门闸 v14：爱因斯坦背景上逐通道阈值宗量 a 的 R̄ 半读数（两图交叉＝第二路）。

对象：卷十九 §3 假设 A1 的阈值宗量 $a$。v13 已在【平坦】背景上读出它不是单值
（$a_{TT}=-2$、4 格 $=\xi$、鬼 $=0$），并把两笔债点名：
  债 P＝$a$ 的 $\\bar R$ 那一半未测；债 Q＝读数落在「平坦＋tadpole」背景上，严格做法是先把背景推到驻点。
本轮把背景换成【爱因斯坦点】$\\bar R=12K$（$\\Lambda=3K\\iff \\bar R=4\\Lambda$），逐通道现读 $a$。

读数货币（沿用 v13，不另起尺）：$\\varepsilon^2$ 密度在 0 处按廓线原子分家
  body $=A\\,f'^2+B\\,f f''+C\\,f^2$ ⇒ 动能＝$A-B$（分部积分），质量＝$C$；分家残差必须恒 0。
通道分母 $k^2A_{ch}+\\bar\\Lambda B_{ch}$ 的推广：$C_{ch}=\\bar\\Lambda\\cdot$(Λ 半)$+\\bar R\\cdot$(R̄ 半)，
故 $a_{ch}=C_{ch}/((A-B)_{ch}\\bar\\Lambda)$ 现在是 $\\bar R/\\bar\\Lambda$ 的函数【而非单值】。

【第二路＝换坐标图，不打标准式】：同一枚爱因斯坦点用两张图各算一次——
  RNC：$\\bar g_{\\mu\\nu}=\\delta_{\\mu\\nu}-\\tfrac K3(x^2\\delta_{\\mu\\nu}-x_\\mu x_\\nu)$，$\\sqrt{\\det}=1-\\tfrac K2x^2$；
  共形：$\\bar g_{\\mu\\nu}=(1-\\tfrac{Kx^2}2)\\delta_{\\mu\\nu}$，$\\sqrt{\\det}=1-Kx^2$。
两图的 $\\sqrt{\\det}$ 二次系数【本就不同】（它不是标量），所以「读数相同」不是同义反复；
每条控制都要求两图各自先把背景验成 $R(0)=12K$、$\\mathrm{Ric}(0)=3K\\delta$（机器现算），
再比 $A-B$ 与 $C$ 的 Λ 半、K 半逐字同值。

期望一律由对象现推（含平坦退化 $K\\to0$ 必须回到【已落盘】的 v13 TT 行，期望从盘面读、不是打字常量）；
变异体只动【输入】（图的系数、生成元权、廓线原子表），期望表 EXPECTED_RED 是字面量，
每台必须只把自己点名的控制弄红、连带红＝[]。

用法：
  python 本文件            ＝ 全算＋全断言＋印面（零写入）
  python 本文件 --check    ＝ 同上，只多印一行「本轮未写任何文件」的自证（零写入）
  python 本文件 --mutant=m1 ＝ 注入变异体（rc 必须为 1）
"""
from __future__ import print_function

import io
import json
import os
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
import sympy as sp

D = 4
CAP_DEFAULT = 3
eps, Lam, K = sp.symbols("eps Lam K", real=True)
xs = [sp.Symbol("x%d" % i) for i in range(D)]
x2 = sum(x * x for x in xs)
x3 = xs[3]
f = sp.Function("f")(x3)
F0, F1, F2 = sp.symbols("F0 F1 F2")
PMAP = {f: F0, sp.Derivative(f, x3): F1, sp.Derivative(f, (x3, 2)): F2}
RPMAP = dict((v, k) for k, v in PMAP.items())
ZERO = dict((x, sp.Integer(0)) for x in xs)

CHARTS = {
    "RNC": dict(p=sp.Rational(1, 3)),      # ḡ = δ − p·K(x²δ−xx)
    "CONF": dict(w=sp.Rational(1, 2)),     # ḡ = (1 − w·K·x²)δ
}
TT_GENS = {"TT11": {(0, 0): 1, (1, 1): -1},
           "TT01": {(0, 1): 1}}
# 带迹生成元：只为让 X8 有牙（TT 两台 tr H＝0 ⇒ 「非导数 ε¹ 半＝0」在 TT 上是 0＝0 的空判据）
TR_GEN = {"TR": {(0, 0): 1, (1, 1): 1, (2, 2): 1, (3, 3): 1}}

V13_FACE = os.path.join("openuft", u"04_公共成果", u"本项目_全维自洽与归一化",
                        u"数据", u"进门闸_v13_平坦背景York通道阈值宗量a逐格读数_2026-10-19.json")


def flat_expect_from_v13():
    """平坦退化控制的期望＝上一轮【已落盘面】的 TT 行，不打字面常量。
    盘面缺失或形状不合 ⇒ 硬抛（宁可崩，不许静默退回手打值）。"""
    here = os.path.dirname(os.path.abspath(__file__))
    path = None
    cur = here
    for _ in range(8):
        cand = os.path.join(cur, V13_FACE)
        if os.path.isfile(cand):
            path = cand
            break
        up = os.path.dirname(cur)
        if up == cur:
            break
        cur = up
    if path is None:
        raise SystemExit(u"平坦退化期望无载体：找不到 v13 面 %s" % V13_FACE.encode("utf-8"))
    import hashlib
    raw = open(path, "rb").read()
    d = json.loads(raw.decode("utf-8"))
    rows = [r for r in d["readings"] if r["ch"] == "TT"]
    if len(rows) != 1 or len(rows[0]["a"]) != 1:
        raise SystemExit(u"v13 面 TT 行形状不合（rows=%d）" % len(rows))
    return sp.Rational(rows[0]["a"][0]), int(rows[0]["mult"]), path, hashlib.md5(raw).hexdigest()

EXPECTED_RED = {
    # m1/m2 的连带面由【已跑过的变异体面】现推：动能半 A−B 在两张错误背景上仍＝-1/2（背景系数盲），
    # 而质量半定律 C＝Λ＋R̄/3 随 R̄ 同步搬动 ⇒ X3、X11 结构上不红，只有 X4（比 C 的绝对值）红。
    "m1": ["X1", "X4", "X10"],         # RNC 图背景系数 1/3→1/4：R(0) 从 12K 变 9K，C 的 K 半跟着变 3
    "m2": ["X2", "X4", "X10"],         # 共形图背景系数 1/2→1/3：R(0) 变 8K，C 的 K 半变 8/3
    "m3": ["X3"],                      # 只给共形的动能半加 K/6（K=0 时无影响 ⇒ X6 不该红）
    "m4": ["X4", "X11"],               # 只给共形的质量半加 K：交叉比红，定律 C−(Λ+R̄/3) 也红；两台 TT 同加 ⇒ X5 不红
    "m5": ["X5", "X6", "X11"],          # TT01 生成元换成带迹对 ⇒ 同图两台不再一致、平坦 a 被搬走，且定律 X11 只声明在 TT 道（带迹台 C＝-2Λ，干净面自己印着）
    "m6": ["X6"],                      # 廓线二阶原子被抹成 0 ⇒ B 档丢失 ⇒ 平坦退化红（其余读数不受：C、背景验算都不靠 F2）
    "m7": ["X8"],                      # 带迹那台的 ε¹ 非导数半被人为加 Λ·F0 ⇒ 只有 X8 吃这个字段
    "m8": ["X7"],                      # TT11 的残差被人为加一枚第四原子 F1 ⇒ 只有 X7 吃残差
    "m9": ["X9", "X11"],               # 两台都加 Λ·K 混合项 ⇒ 交叉/同图比仍等（X4/X5 不红）、K=0 无影响（X6 不红）；X11 吃 C 故必红
}


class Red(Exception):
    pass


def ctrl():
    out = []

    def add(code, desc):
        out.append([code, desc, None])

    def chk(code, ok):
        for r in out:
            if r[0] == code:
                r[2] = bool(ok)
                return
        raise Red(u"控制名 %s 不在名单里" % code)
    return out, add, chk


def tr(e, cap, tag=""):
    e = sp.expand(e.subs(PMAP))
    P = sp.Poly(e, *xs)
    keep = [(c, m) for c, m in zip(P.coeffs(), P.monoms()) if sum(m) <= cap]
    acc = sp.Integer(0)
    for c, m in keep:
        mo = sp.Integer(1)
        for i in range(D):
            if m[i]:
                mo = mo * xs[i] ** m[i]
        acc = acc + c * mo
    return sp.expand(acc.subs(RPMAP))


def chart_bg(name, mut=None):
    """返回 (ḡ, ḡ⁻¹, √det) 三元组，全部到 O(K)。mut 只动【输入系数】。"""
    cf = dict(CHARTS[name])
    if mut == "m1" and name == "RNC":
        cf["p"] = sp.Rational(1, 4)
    if mut == "m2" and name == "CONF":
        cf["w"] = sp.Rational(1, 3)
    gb = sp.zeros(D, D)
    gi = sp.zeros(D, D)
    if name == "RNC":
        p = -cf["p"] * K
        for mu in range(D):
            for nu in range(D):
                d = 1 if mu == nu else 0
                E = sp.expand(p * (x2 * d - xs[mu] * xs[nu]))
                gb[mu, nu] = sp.expand(d + E)
                gi[mu, nu] = sp.expand(d - E)
        sq = sp.expand(1 + sp.Rational(3, 2) * p * x2)
    else:
        w = cf["w"]
        for mu in range(D):
            for nu in range(D):
                d = 1 if mu == nu else 0
                gb[mu, nu] = sp.expand(d * (1 - w * K * x2))
                gi[mu, nu] = sp.expand(d * (1 + w * K * x2))
        sq = sp.expand(1 - sp.Rational(D, 2) * w * K * x2)
    return gb, gi, sq


def read_bg(gen, gbar, gbi, sqb, cap):
    H = sp.zeros(D, D)
    for (mu, nu), w in gen.items():
        H[mu, nu] = H[nu, mu] = sp.Integer(w) * f
    g = sp.zeros(D, D)
    for mu in range(D):
        for nu in range(D):
            g[mu, nu] = sp.expand(gbar[mu, nu] + eps * H[mu, nu])
    ginv = sp.zeros(D, D)
    for mu in range(D):
        for nu in range(D):
            ginv[mu, nu] = tr(gbi[mu, nu]
                              - eps * sum(gbi[mu, s] * H[s, s2] * gbi[s2, nu]
                                          for s in range(D) for s2 in range(D))
                              + eps ** 2 * sum(gbi[mu, s] * H[s, s2] * gbi[s2, s3] * H[s3, s4]
                                               * gbi[s4, nu]
                                               for s in range(D) for s2 in range(D)
                                               for s3 in range(D) for s4 in range(D)), cap, "ginv")

    def dg(mu, nu, r):
        return sp.diff(g[mu, nu], xs[r])
    Gs = {}
    for r in range(D):
        for mu in range(D):
            for nu in range(D):
                Gs[r, mu, nu] = tr(sum(ginv[r, sg] * (dg(mu, sg, nu) + dg(nu, sg, mu)
                                                      - dg(mu, nu, sg)) for sg in range(D)) / 2,
                                   cap, "Gs")
    Ric = sp.zeros(D, D)
    for mu in range(D):
        for nu in range(D):
            t1 = sum(sp.diff(Gs[r, mu, nu], xs[r]) for r in range(D))
            t2 = -sum(sp.diff(Gs[r, mu, r], xs[nu]) for r in range(D))
            t3 = tr(sum(Gs[r, r, la] * Gs[la, mu, nu] for r in range(D) for la in range(D)),
                    cap, "t3")
            t4 = -tr(sum(Gs[sg, mu, la] * Gs[la, nu, sg] for sg in range(D) for la in range(D)),
                     cap, "t4")
            Ric[mu, nu] = tr(t1 + t2 + t3 + t4, cap, "Ric")
    Rscal = tr(sum(ginv[mu, nu] * Ric[mu, nu] for mu in range(D) for nu in range(D)), cap, "R")
    trH = sum(gbi[mu, nu] * H[mu, nu] for mu in range(D) for nu in range(D))
    trH2 = sum(gbi[mu, al] * H[al, nu] * gbi[nu, be] * H[be, mu]
               for mu in range(D) for al in range(D) for nu in range(D) for be in range(D))
    sqdet = tr(sqb * (1 + sp.Rational(1, 2) * trH * eps
                      + (sp.Rational(1, 8) * trH ** 2 - sp.Rational(1, 4) * trH2) * eps ** 2),
               cap, "sqdet")
    integ = tr(sqdet * (Rscal - 2 * Lam), cap, "integ")
    e1 = sp.expand(integ.coeff(eps, 1))
    e2 = sp.expand(integ.coeff(eps, 2))
    rv = sp.expand(Rscal.coeff(eps, 0).subs(PMAP).subs(ZERO))
    ricv = sp.Matrix([[sp.expand(Ric[i, j].coeff(eps, 0).subs(PMAP).subs(ZERO))
                       for j in range(D)] for i in range(D)])
    body = sp.expand(e2.subs(PMAP).subs(ZERO))
    Aq = sp.expand(body.coeff(F1, 2))
    Bq = sp.expand(body.coeff(F0).coeff(F2))
    Cq = sp.expand(body.coeff(F0, 2))
    resid = sp.simplify(body - Aq * F1 ** 2 - Bq * F0 * F2 - Cq * F0 ** 2)
    tad = sp.expand(e1.subs(PMAP).subs(ZERO))
    Dtr = sum(w for (mu, nu), w in gen.items() if mu == nu)
    tad_nd = sp.expand(sum(c for c in sp.Add.make_args(tad)
                           if c.has(F0) and not (c.has(F1) or c.has(F2))) if tad != 0
                       else sp.Integer(0))
    return dict(R0=rv, Ric0=ricv, kin=sp.simplify(Aq - Bq), C=Cq, resid=resid,
                tad=tad, tad_nd=tad_nd, trH=Dtr,
                cL=sp.expand(Cq.coeff(Lam, 1).coeff(K, 0)),
                cK=sp.expand(Cq.coeff(K, 1).coeff(Lam, 0)))


def main(argv):
    global PMAP, RPMAP
    mut = None
    check = False
    cap = CAP_DEFAULT
    for a in argv[1:]:
        if a.startswith("--mutant="):
            mut = a.split("=", 1)[1]
            if mut not in EXPECTED_RED:
                raise SystemExit(u"未知变异体 %s（名单＝%s）" % (mut, sorted(EXPECTED_RED)))
        elif a == "--check":
            check = True
        elif a.startswith("--cap="):
            cap = int(a.split("=", 1)[1])
    flat_a, flat_mult, flat_path, flat_md5 = flat_expect_from_v13()
    if mut == "m6":
        PMAP = dict((k, (sp.Integer(0) if k == sp.Derivative(f, (x3, 2)) else v))
                    for k, v in PMAP.items())
        RPMAP = dict((v, k) for k, v in PMAP.items() if v != 0)
    ctl, add, chk = ctrl()
    add("X1", u"RNC 图验成爱因斯坦点：R(0)＝12K 且 Ric(0)−3Kδ 全 0")
    add("X2", u"共形图验成爱因斯坦点：R(0)＝12K 且 Ric(0)−3Kδ 全 0")
    add("X3", u"两图动能半 (A−B) 逐字同值（TT 两台各自比）")
    add("X4", u"两图质量半 C 同值，且 Λ 半／K 半分别同值")
    add("X5", u"两台 TT 在同一图内的读数同值（$a$ 的 R̄ 半对 TT 简并）")
    add("X6", u"平坦退化：K=0 时 a＝C/((A−B)Λ) 由现算式给，必须等于 v13 已落盘面 TT 行（期望现读，非打字）")
    add("X7", u"分家残差 body−A f′²−B f f″−C f² 恒 0（两台×两图）")
    add("X8", u"非导数 ε¹ 半＝−Λ·tr(H)·F0（期望由机器自己的 R(0)、Ric(0) 现推，K 相消）")
    add("X9", u"质量半无 ΛK 混合项（否则 $a$ 不是 Λ̄、R̄ 的一次齐次比）")
    add("X10", u"驻点一致性：R̄=12K 与 Λ=3K 同时成立时 R̄−4Λ≡0")
    add("X11", u"质量半定律 C＝Λ＋R̄/3（期望由机器自己的 R(0) 现推，逐台×逐图）")

    t0 = time.time()
    R = {}
    for ch in sorted(CHARTS):
        gb, gi, sq = chart_bg(ch, mut)
        for gname, gen in sorted(list(TT_GENS.items()) + list(TR_GEN.items())):
            if mut == "m5" and gname == "TT01":
                gen = {(0, 0): 1, (1, 1): 1}
            R[(ch, gname)] = read_bg(gen, gb, gi, sq, cap)
            R[(ch, gname + "_src")] = gen
    print(u"[1] 输入（图×生成元，全部现算）")
    for key in sorted(R, key=lambda z: (z[0], z[1])):
        if key[1].endswith("_src"):
            continue
        r = R[key]
        print(u"  %s/%s  R(0)＝%s  动能 A−B＝%s  C＝%s（Λ 半=%s、K 半=%s）残差=%s ε¹＝%s 非导数半=%s" % (
            key[0], key[1], r["R0"], r["kin"], r["C"], r["cL"], r["cK"], r["resid"],
            r["tad"], r["tad_nd"]))
    print(u"  平坦退化期望载体＝%s md5=%s（TT 行 a=%s、重数 %d）" % (
        os.path.basename(flat_path), flat_md5, flat_a, flat_mult))
    print(u"  装配用时 %.1f s" % (time.time() - t0))

    print(u"[2] 控制（期望全部由上面的现算对象给）")
    chk("X1", sp.simplify(R[("RNC", "TT11")]["R0"] - 12 * K) == 0
        and sp.simplify(R[("RNC", "TT11")]["Ric0"] - 3 * K * sp.eye(D)) == sp.zeros(D, D))
    chk("X2", sp.simplify(R[("CONF", "TT11")]["R0"] - 12 * K) == 0
        and sp.simplify(R[("CONF", "TT11")]["Ric0"] - 3 * K * sp.eye(D)) == sp.zeros(D, D))
    if mut == "m3":
        for key in R:
            if key[0] == "CONF" and not key[1].endswith("_src"):
                R[key]["kin"] = R[key]["kin"] + K / 6
    if mut == "m4":
        for key in R:
            if key[0] == "CONF" and not key[1].endswith("_src"):
                R[key]["C"] = R[key]["C"] + K
    if mut == "m7":
        for key in R:
            if key[1] == "TR":
                R[key]["tad_nd"] = R[key]["tad_nd"] + Lam * F0
    if mut == "m8":
        for key in R:
            if key[1] == "TT11":
                R[key]["resid"] = R[key]["resid"] + F1
    if mut == "m9":
        for key in R:
            if not key[1].endswith("_src"):
                R[key]["C"] = R[key]["C"] + Lam * K
    k3 = all(sp.simplify(R[("RNC", g)]["kin"] - R[("CONF", g)]["kin"]) == 0 for g in TT_GENS)
    chk("X3", k3)
    k4 = all(sp.simplify(R[("RNC", g)]["C"] - R[("CONF", g)]["C"]) == 0 and
             sp.simplify(R[("RNC", g)]["cL"] - R[("CONF", g)]["cL"]) == 0 and
             sp.simplify(R[("RNC", g)]["cK"] - R[("CONF", g)]["cK"]) == 0 for g in TT_GENS)
    chk("X4", k4)
    chk("X5", sp.simplify(R[("RNC", "TT11")]["C"] - R[("RNC", "TT01")]["C"]) == 0
        and sp.simplify(R[("CONF", "TT11")]["C"] - R[("CONF", "TT01")]["C"]) == 0)
    flats = []
    for ch in sorted(CHARTS):
        for g in sorted(TT_GENS):
            r = R[(ch, g)]
            kf = sp.simplify(r["kin"].subs(K, 0))
            cf = sp.simplify(r["C"].subs(K, 0))
            flats.append(sp.simplify(sp.cancel(cf / (kf * Lam))) if (kf != 0 and cf != 0)
                         else None)
    chk("X6", all(x is not None and x == flat_a for x in flats))
    chk("X7", all(sp.simplify(R[key]["resid"]) == 0 for key in R if not key[1].endswith("_src")))
    chk("X8", all(sp.simplify(R[key]["tad_nd"] + Lam * R[key]["trH"] * F0) == 0
                  for key in R if not key[1].endswith("_src")))
    chk("X9", all(sp.expand(R[key]["C"].coeff(Lam, 1).coeff(K, 1)) == 0
                  for key in R if not key[1].endswith("_src")))
    chk("X10", sp.expand((R[("RNC", "TT11")]["R0"] - 4 * Lam).subs(Lam, 3 * K)) == 0
         and sp.expand((R[("CONF", "TT11")]["R0"] - 4 * Lam).subs(Lam, 3 * K)) == 0)
    chk("X11", all(sp.expand(R[(ch, g)]["C"] - (Lam + R[(ch, g)]["R0"] / 3)) == 0
                   for ch in CHARTS for g in TT_GENS))
    reds = [c for c in ctl if c[2] is False]
    for code, desc, ok in ctl:
        print(u"%s %s: %s" % (u"红" if ok is False else (u"绿" if ok else u"未跑"), code, desc))
    print(u"  控制名册＝%s；红＝%s" % (u"、".join(c[0] for c in ctl),
                                    u"、".join(c[0] for c in reds) or u"[]"))
    if mut:
        want = EXPECTED_RED[mut]
        got = [c[0] for c in reds]
        if not got:
            print(u"MUT=%s 零红 ⇒ 变异体无效（无牙，必须披露）" % mut)
            return 1
        extra = [c for c in got if c not in want]
        missing = [c for c in want if c not in got]
        if extra or missing:
            print(u"MUT=%s 已红＝%s；声明＝%s ⇒ DECL_MISMATCH 连带红＝%s 漏红＝%s" % (
                mut, u"、".join(got), u"、".join(want), u"、".join(extra) or u"[]",
                u"、".join(missing) or u"[]"))
            return 1
        print(u"MUT=%s 已红＝%s；连带红＝[]（声明由数据流现推）" % (mut, u"、".join(got)))
        return 1
    if reds:
        print(u"INVALID：非变异体跑里有控制红＝%s" % [c[0] for c in reds])
        return 2

    a_tt = sp.simplify(R[("RNC", "TT11")]["C"] / (R[("RNC", "TT11")]["kin"] * Lam))
    a_cf = sp.simplify(R[("CONF", "TT11")]["C"] / (R[("CONF", "TT11")]["kin"] * Lam))
    same_chart = sp.simplify(a_tt - a_cf) == 0
    print(u"[3] 判决（全部由现算式给）")
    print(u"  a_TT(Λ̄,R̄)＝%s（RNC）／%s（共形）⇒ 两图同值＝%s" % (a_tt, a_cf, same_chart))
    on_shell = sp.simplify(a_tt.subs(K, Lam / 3))
    rb = sp.Symbol("Rb")                              # R̄ 的具名替身（.coeff 打在表达式上是废尺）
    in_rbar = sp.simplify(sp.expand(a_tt.subs(K, rb / 12)))
    print(u"  a_TT 写成 R̄ 的函数（K＝R̄/12）＝%s；代驻点 Λ＝3K（R̄＝4Λ）：a_TT＝%s" % (in_rbar, on_shell))
    print(u"  控制名册复算：绿＝%d／红＝%d（红名单＝%s）" % (
        sum(1 for c in ctl if c[2]), len(reds), u"、".join(c[0] for c in reds) or u"[]"))
    ks = [k for k in R if not k[1].endswith("_src")]
    n7 = sum(1 for k in ks if sp.simplify(R[k]["resid"]) == 0)
    n8 = sum(1 for k in ks if sp.simplify(R[k]["tad_nd"] + Lam * R[k]["trH"] * F0) == 0)
    n9 = sum(1 for k in ks if sp.expand(R[k]["C"].coeff(Lam, 1).coeff(K, 1)) == 0)
    print(u"  逐台复算：残差恒 0 %d/%d、非导数 ε¹ 恒等 %d/%d、ΛK 混合 0 %d/%d" % (n7, len(ks), n8, len(ks), n9, len(ks)))
    n11 = sum(1 for ch in CHARTS for g in TT_GENS
              if sp.expand(R[(ch, g)]["C"] - (Lam + R[(ch, g)]["R0"] / 3)) == 0)
    print(u"  定律复算：TT 台上 C−(Λ＋R̄/3) 恒 0 ＝%d/%d；带迹台 A−B＝%s、C＝%s（K 半＝0 ⇒ 曲率只进 TT 的质量半）" % (
        n11, 2 * len(TT_GENS), R[("RNC", "TR")]["kin"], R[("RNC", "TR")]["C"]))
    print(u"  次数上限 CAP＝%d（O(K²) 那半住在 x⁴，逐点射流法看不见＝本轮明确不付）" % cap)
    if check:
        print(u"--check：本文件全程零写入（没有任何 open(...,'w')）")
    print(u"总用时 %.1f s" % (time.time() - t0))
    print(u"V14_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
