# -*- coding: utf-8 -*-
"""进门闸 v13：平坦背景 + 宇宙项的显式二阶变分 ⇒ 逐 York 通道的阈值宗量系数 a 的【读数】。

被审的对象是本仓库自己的一条承诺（不是别人的代码）：
  S14/04_理论推导/TUFT_卷十九_背景场Hessian结构.md §3 假设 A1
    「宗量 u = 1 + a*lambda；a 为 Hessian 中 -2Lambda 与 R 的组合系数（标准取 a = -2）」
    §8 卷二十闭合清单第 4 项「阈值宗量系数 a」；r79 已证：盘上 a 的窄口径数值读数 0 行
  ⇒ 本册不引用任何人的数值，直接从二阶变分按通道把 a 算出来，并判「a 是单值」那一句。

约定（印在面上；判决只建立在约定无关的事实上——谱是否简并、哪些通道规范不变）：
  被积式 sqrt(g)*(R - 2*Lam)，总因子 -1/(32 pi G) 取 1（广义本征值是比值，与它无关）
  背景 = 平坦 delta（⇒ Rbar = 0：本册只测得 a 定义里 Lam 那一半，R 那一半是债 P）
  动量沿 e3、|k|=1：g = delta + eps*c*f(x3) ⇒ 两导数项 = k^2*f^2，无导数项 = f^2
  规范固定 F_nu = d^mu h_{mu nu} - 1/2 d_nu h，S_gf = (1/(2*xi))*delta^{mu nu}*F_mu*F_nu
  读数货币：通道分母 k^2*A_ch + Lam*B_ch 的广义本征根 rho_ch；a_ch = rho_ch/Lam；u_ch = 1 + a_ch*lambda

用法：python 源码/进门闸_v13_*.py --check     零写入，跑十条控制
      python 源码/进门闸_v13_*.py --land      写 数据/*.json 与 判定_*.md（拒绝覆盖）
      python 源码/进门闸_v13_*.py --mutant=mN 换尺／换对象，打印指定控制红
"""
import hashlib
import io
import json
import os
import re
import shutil
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = r"D:\a10\aikjx\code\my_lib\openuft"
NAME = u"进门闸_v13_平坦背景York通道阈值宗量a逐格读数_2026-10-19"
A_NARROW = re.compile(u"宗量系数\\s*a[\\s\\S]{0,40}?a\\s*=\\s*[-+]?[\\d.]+")
A_MENTION = re.compile(u"阈值宗量系数\\s*a")
EXPECTED_RED = {
    "m1": "X6",    # sigma-h 动能混合被丢掉：两格各按 1x1 求根
    "m2": "X5",    # 把 a_V = xi 在 xi=1 处的数值当规范不变读数
    "m3": "X8",    # 把鬼动能矩阵的对角 1 读成质量项（a_gh = 1）
    "m4": "X9",    # 断言 eps^1 恒零（平坦背景其实是带 tadpole 的非驻点）
    "m5": "X7",    # 全谱按「逐块 1x1 行列式相乘」拼装（标量两格被拆开）
    "m6": "X4",    # 撤掉 TT 通道的矩阵级成比例判定（只按特征值同值记账）
    "m7": "X2",    # 微分同胚轨道取错方向（k 沿 e0 而非 e3）：维数对、方向错
    "m8": "X10",   # 「标准 a」不现读卷十九，而由本轮 TT 读数回填当独立期望
    "m9": "X1",    # eps^2 分家时不把 f*f'' 分部积分
    "m10": "X3",   # 撤掉规范固定项却宣布传播子可逆
}


class Bad(Exception):
    pass


def find_root():
    p = HERE
    for _ in range(6):
        if os.path.isdir(os.path.join(p, u"01_独立体系")):
            return p
        q = os.path.dirname(p)
        if q == p:
            break
        p = q
    if os.path.isdir(os.path.join(DEFAULT_ROOT, u"01_独立体系")):
        return DEFAULT_ROOT
    raise Bad(u"找不到仓库根（没有 01_独立体系）")


ROOT = find_root()
PROJ = os.path.join(ROOT, u"04_公共成果", u"本项目_全维自洽与归一化")
S14 = os.path.join(ROOT, u"01_独立体系", u"S14_挠率统一场论TUFT")
VOL19 = os.path.join(S14, u"04_理论推导", u"TUFT_卷十九_背景场Hessian结构.md")
CAT = os.path.join(ROOT, u"00_项目治理", u"资料索引", "material_catalog.md")
MAN = os.path.join(ROOT, u"00_项目治理", u"资料索引", "structure_manifest.json")
INSTR = os.path.join(PROJ, u"源码", NAME + u".py")
FACE = os.path.join(PROJ, u"数据", NAME + u".json")
VOL = os.path.join(PROJ, u"判定_" + NAME + u".md")


def img(p):
    b = open(p, "rb").read()
    return {"bytes": len(b), "md5": hashlib.md5(b).hexdigest(),
            "crlf": b.count(b"\r\n"), "lf": b.count(b"\n")}


def txt(p):
    return open(p, "rb").read().decode("utf-8", "replace")


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


# ---------------------------------------------------------------- 符号计算
def build():
    import sympy as sp
    D = 4
    eps, Lam, xi = sp.symbols("eps Lam xi", nonnegative=True)
    x3 = sp.Symbol("x3")
    f = sp.Function("f")(x3)
    fp = sp.Derivative(f, x3)
    fpp = sp.Derivative(f, (x3, 2))
    c = sp.symbols("c0:10")
    IDX = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]

    def ci(mu, nu):
        return c[IDX.index((min(mu, nu), max(mu, nu)))]

    C = sp.zeros(D, D)
    for mu in range(D):
        for nu in range(D):
            C[mu, nu] = ci(mu, nu)
    g = sp.zeros(D, D)
    for mu in range(D):
        for nu in range(D):
            g[mu, nu] = (1 if mu == nu else 0) + eps * C[mu, nu] * f
    C2 = C * C
    ginv = sp.zeros(D, D)
    for mu in range(D):
        for nu in range(D):
            ginv[mu, nu] = ((1 if mu == nu else 0) - eps * C[mu, nu] * f
                            + eps**2 * C2[mu, nu] * f**2)
    trC = sum(C[i, i] for i in range(D))
    sqdet = sp.expand(1 + eps * trC * f / 2
                      + eps**2 * (trC**2 * f**2 / 8 - C2.trace() * f**2 / 4))

    def dg(mu, nu, r):
        return eps * C[mu, nu] * fp if r == 3 else sp.Integer(0)

    Gs = {}
    for r in range(D):
        for mu in range(D):
            for nu in range(D):
                s = sum(ginv[r, sig] * (dg(mu, sig, nu) + dg(nu, sig, mu) - dg(mu, nu, sig))
                        for sig in range(D))
                Gs[r, mu, nu] = sp.expand(s / 2)
    Ric = sp.zeros(D, D)
    for mu in range(D):
        for nu in range(D):
            t1 = sp.Derivative(Gs[3, mu, nu], x3).doit()
            t2 = (-sp.Derivative(sum(Gs[r, mu, r] for r in range(D)), x3).doit()
                  if nu == 3 else 0)
            t3 = sum(Gs[r, r, la] * Gs[la, mu, nu] for r in range(D) for la in range(D))
            t4 = -sum(Gs[sig, mu, r] * Gs[r, nu, sig] for sig in range(D) for r in range(D))
            Ric[mu, nu] = sp.expand(t1 + t2 + t3 + t4)
    Rscal = sp.expand(sum(ginv[mu, nu] * Ric[mu, nu]
                          for mu in range(D) for nu in range(D)))
    integrand = sp.expand(sqdet * (Rscal - 2 * Lam))
    e2 = sp.expand(integrand.coeff(eps, 2))
    e1 = sp.expand(integrand.coeff(eps, 1))
    A_ep = sp.expand(e2.coeff(fp, 2))
    B_ep = sp.expand(e2.coeff(f * fpp, 1))
    C_ep = sp.expand(e2.coeff(f, 2))
    resid = sp.expand(e2 - A_ep * fp**2 - B_ep * f * fpp - C_ep * f**2)
    resid_noparts = sp.expand(e2 - A_ep * fp**2 - C_ep * f**2)

    F = [sp.expand(ci(3, nu) - (trC / 2 if nu == 3 else 0)) for nu in range(D)]
    Sgf = sum(F[nu] * F[nu] for nu in range(D)) / xi

    def qmat(expr):
        M = sp.zeros(10, 10)
        for i in range(10):
            for j in range(10):
                M[i, j] = sp.simplify(sp.Derivative(expr, c[i], c[j]).doit() / 2)
        return sp.simplify(M)

    Mk = qmat(A_ep - B_ep)
    ML = qmat(C_ep)
    Mgf = qmat(Sgf)
    Mkxi = sp.simplify(Mk + Mgf)
    rho = sp.Symbol("rho")
    fullchar = sp.factor(sp.together((ML - rho * Mkxi).det()))

    th = sp.symbols("th0:4")
    Gg = sp.zeros(10, 4)          # 对称轨道 k_mu th_nu + k_nu th_mu，k 沿 e3
    Gg_wrong = sp.zeros(10, 4)    # m7：同样 4 个生成元但 k 沿 e0
    for i in range(10):
        a, b = IDX[i]
        for nu in range(4):
            Gg[i, nu] = (1 if a == 3 and nu == b else 0) + (1 if b == 3 and nu == a else 0)
            Gg_wrong[i, nu] = (1 if a == 0 and nu == b else 0) + (1 if b == 0 and nu == a else 0)
    Gh = sp.zeros(4, 4)           # 鬼动能矩阵（k^2 的系数），由 F 对 theta 变分现算
    for mu in range(4):
        ex = sp.expand(F[mu])
        for i in range(10):
            a, b = IDX[i]
            ex = ex.subs(c[i], th[a] * (1 if b == 3 else 0) + th[b] * (1 if a == 3 else 0))
        for nu in range(4):
            Gh[mu, nu] = sp.expand(sp.Derivative(ex, th[nu]).doit())

    tt = sp.symbols("t0 t1 t2 t3 t4")
    vv = sp.symbols("v0 v1 v2")
    sg, hh = sp.symbols("sigma h")
    TT = sp.zeros(D, D)
    TT[0, 0], TT[1, 1] = tt[0], tt[1]
    TT[2, 2] = -tt[0] - tt[1]
    TT[0, 1] = TT[1, 0] = tt[2]
    TT[0, 2] = TT[2, 0] = tt[3]
    TT[1, 2] = TT[2, 1] = tt[4]
    XI = sp.zeros(D, D)
    for i in range(3):
        XI[i, 3] = XI[3, i] = vv[i]
    SG = sp.zeros(D, D)
    for mu in range(D):
        SG[mu, mu] = sp.Rational(1, 4) - (1 if mu == 3 else 0)
    HH = sp.zeros(D, D)
    for mu in range(D):
        HH[mu, mu] = sp.Rational(1, 4)
    CY = sp.zeros(D, D)
    for mu in range(D):
        for nu in range(D):
            CY[mu, nu] = TT[mu, nu] + XI[mu, nu] + SG[mu, nu] * sg + HH[mu, nu] * hh
    sub = {c[i]: sp.expand(CY[IDX[i][0], IDX[i][1]]) for i in range(10)}
    ym = list(tt) + list(vv) + [sg, hh]
    Jm = sp.zeros(10, 10)
    for i in range(10):
        for a in range(10):
            Jm[i, a] = sp.expand(sp.Derivative(sub[c[i]], ym[a]).doit())

    def part(M, rows):
        return sp.simplify(M.extract(rows, rows))

    Ak = sp.simplify(Jm.T * Mkxi * Jm)
    Al = sp.simplify(Jm.T * ML * Jm)
    Ae = sp.simplify(Jm.T * Mk * Jm)
    GRP = [(u"TT", [0, 1, 2, 3, 4]), (u"V", [5, 6, 7]), (u"S", [8]), (u"H", [9])]
    blocks = dict((n2, {"A": part(Ak, ii), "B": part(Al, ii)}) for n2, ii in GRP)
    tad = [sp.expand(sp.Derivative(sp.simplify(e1.subs(sub)), ya).doit()) for ya in ym]

    def iszero(M):
        return all(sp.simplify(M[a, b]) == 0
                   for a in range(M.rows) for b in range(M.cols))

    # 块间零性只对【拼装用的那一层分块】成立：σ 与 h 本来就是同一个 2x2 联合块的两格，
    # 它们之间的非对角项是 X6 的读数，不是 X7 的违规（把 4 组当 4 块来查＝拿错的形状量对象）。
    GRP3 = [(u"TT", [0, 1, 2, 3, 4]), (u"V", [5, 6, 7]), (u"S+H", [8, 9])]
    offdiag = {}
    for i in range(3):
        for j in range(i + 1, 3):
            ri, rj = GRP3[i][1], GRP3[j][1]
            offdiag[GRP3[i][0] + u"/" + GRP3[j][0]] = bool(
                iszero(Ak.extract(ri, rj)) and iszero(Al.extract(ri, rj)))
    return dict(sp=sp, eps=eps, Lam=Lam, xi=xi, rho=rho, c=c, IDX=IDX, sub=sub,
                f=f, fp=fp, fpp=fpp, x3=x3,
                resid=resid, resid_noparts=resid_noparts, e1=e1, e2=e2,
                Mk=Mk, ML=ML, Mgf=Mgf,
                Mkxi=Mkxi, fullchar=fullchar, Gg=Gg, Gg_wrong=Gg_wrong, Gh=Gh, Jm=Jm,
                Ak=Ak, Al=Al, Ae=Ae, blocks=blocks, scal_rows=[8, 9],
                gdir=u"e3", gdir_wrong=u"e0（m7：方向错）",
                sh_off=sp.simplify(Ak[8, 9]), tad=tad, ym=ym, offdiag=offdiag,
                naive_product=False)


def multiset(sp, expr, Lam, rho):
    """把 det(B - rho*A) 拆成 a = rho/Lam 的根重数表（一次因式才认，否则点名）。"""
    facs = sp.factor_list(sp.expand(sp.together(expr).as_numer_denom()[0]), rho)[1]
    out = {}
    deg = 0
    for fac, mult in facs:
        p = sp.Poly(fac, rho)
        m = int(mult)                 # factor_list 的重数在本 sympy 版本里是 Integer，不是 int
        if p.degree() == 1:
            a = sp.cancel(sp.solve(p, rho)[0] / Lam)
            out[str(a)] = out.get(str(a), 0) + m
        else:
            out[u"非一次因式:" + str(fac)] = m
        deg += m
    return out, deg


def readings(S):
    sp, Lam, xi, rho = S["sp"], S["Lam"], S["xi"], S["rho"]
    out = []
    for n2 in (u"TT", u"V"):
        A2 = S["blocks"][n2]["A"]
        B2 = S["blocks"][n2]["B"]
        r = sp.simplify(B2 * A2.inv())
        diag = [sp.simplify(r[i, i]) for i in range(r.rows)]
        offok = all(sp.simplify(r[i, j]) == 0 for i in range(r.rows) for j in range(r.cols)
                    if i != j)
        same = all(sp.simplify(diag[0] - d) == 0 for d in diag)
        ms, deg = multiset(sp, (B2 - rho * A2).det(), Lam, rho)
        # 逐元素求导：对全常数矩阵，sp.Derivative(矩阵, xi).doit() 会退化成标量 0，
        # 与 zeros(n,n) 比较恒 False ⇒ 规范不变那格会被自己的尺判成"随规范走"。
        dz = all(sp.simplify(sp.Derivative(r[i, j], xi).doit()) == 0
                 for i in range(r.rows) for j in range(r.cols))
        out.append({"ch": n2, "mult": r.rows, "proportional": bool(offok and same),
                    "a": sorted(ms.keys()), "mult_of_a": ms, "deg": deg,
                    "diag": [str(d) for d in diag],
                    "da_dxi_zero": bool(dz)})
    A2 = S["Ak"].extract(S["scal_rows"], S["scal_rows"])
    B2 = S["Al"].extract(S["scal_rows"], S["scal_rows"])
    ms, deg = multiset(sp, (B2 - rho * A2).det(), Lam, rho)
    out.append({"ch": u"S+H", "mult": 2, "proportional": None, "a": sorted(ms.keys()),
                "mult_of_a": ms, "deg": deg, "da_dxi_zero": None,
                "mixed": bool(sp.simplify(S["sh_off"]) != 0),
                "naive_1x1": sorted([str(sp.cancel(B2[i, i] / A2[i, i] / Lam)) for i in (0, 1)])})
    gh = S["Gh"]
    kin = [sp.simplify(gh[i, i]) for i in range(4)]
    gm, gdeg = multiset(sp, (-rho * gh).det(), Lam, rho)
    out.append({"ch": u"ghost", "mult": 4, "proportional": bool(all(k == 1 for k in kin)),
                "a": sorted(gm.keys()), "mult_of_a": gm, "deg": gdeg,
                "da_dxi_zero": bool(len(gh.free_symbols) == 0),
                "kin": [str(k) for k in kin]})
    return out


def block_book(S):
    """逐块行列式相乘拼装的全谱；naive_product=True 就是把标量两格拆成 1x1（m5 的坏账）。"""
    sp, Lam, rho = S["sp"], S["Lam"], S["rho"]
    prod = sp.Integer(1)
    for n2 in (u"TT", u"V"):
        A2 = S["blocks"][n2]["A"]
        B2 = S["blocks"][n2]["B"]
        prod = prod * (B2 - rho * A2).det()
    A2 = S["Ak"].extract(S["scal_rows"], S["scal_rows"])
    B2 = S["Al"].extract(S["scal_rows"], S["scal_rows"])
    if S["naive_product"]:
        prod = prod * (B2[0, 0] - rho * A2[0, 0]) * (B2[1, 1] - rho * A2[1, 1])
    else:
        prod = prod * (B2 - rho * A2).det()
    return multiset(sp, prod, Lam, rho)


def full_spectrum(S):
    sp, Lam, rho = S["sp"], S["Lam"], S["rho"]
    expr = sp.factor(sp.together(S["fullchar"]))
    return multiset(sp, expr, Lam, rho) + (str(expr),)


def corpus_a():
    men_w = men_a = nar = 0
    hits = []
    for dirpath, dirnames, filenames in os.walk(S14):
        dirnames[:] = [x for x in dirnames if x not in (".git", "__pycache__")]
        for fn in filenames:
            if not fn.endswith((".md", ".py", ".txt", ".json")):
                continue
            try:
                s = open(os.path.join(dirpath, fn), "rb").read().decode("utf-8")
            except Exception:
                continue
            for line in s.split("\n"):
                if A_MENTION.search(line):
                    men_a += 1
                if u"阈值宗量系数" in line:
                    men_w += 1
                if A_NARROW.search(line):
                    nar += 1
                    hits.append(rel(os.path.join(dirpath, fn)))
    v19 = txt(VOL19)
    m = re.search(u"标准取 \\$a\\s*=\\s*(-?\\d+)\\$", v19)
    single = re.search(u"宗量 \\$u\\s*=\\s*1\\s*\\+\\s*a\\s*\\\\lambda\\$", v19)
    return {"corpus_mention_wide": men_w, "corpus_mention_a": men_a,
            "corpus_narrow_readings": nar, "narrow_files": sorted(set(hits))[:4],
            "doc_standard_a": (int(m.group(1)) if m else None),
            "doc_standard_a_src": (u"卷十九 §3 现读" if m else u"没现读到"),
            "doc_single_u_claim": bool(single),
            "index_at_run": (img(CAT) if os.path.isfile(CAT) else None),
            "index_rows_at_run": (len(re.findall(r"^- \[", txt(CAT), re.M))
                                  if os.path.isfile(CAT) else None),
            "v19": img(VOL19)}


# ---------------------------------------------------------------- 控制
def run_controls(S, R, CU, FS):
    sp, Lam, xi, rho = S["sp"], S["Lam"], S["xi"], S["rho"]
    ctl = []

    def add(code, ok, desc):
        ctl.append({"code": code, "ok": bool(ok), "desc": desc})

    tt = [x for x in R if x["ch"] == u"TT"][0]
    vv = [x for x in R if x["ch"] == u"V"][0]
    sc = [x for x in R if x["ch"] == u"S+H"][0]
    gh = [x for x in R if x["ch"] == u"ghost"][0]
    a_tt = tt["a"][0]

    r1 = bool(sp.simplify(S["resid"]) == 0)
    add("X1", r1,
        u"eps^2 分家（f'^2 / f f'' / f^2，且把 f f'' 分部积分并回 f'^2）残差恒等 0＝%s；"
        u"eps^2 项数 %d、eps^1 项数 %d" % (r1,
                                        len(sp.Add.make_args(S["e2"])),
                                        len(sp.Add.make_args(S["e1"]))))
    ns = S["Mk"].nullspace()
    spanok = len(ns) == S["Gg"].rank() and all((S["Gg"].row_join(v)).rank() == S["Gg"].rank()
                                               for v in ns)
    add("X2", S["Mk"].rank() == 6 and spanok,
        u"EH 动能秩 %d／10、核 %d 维；核向量逐个落在【对称】微分同胚轨道（$k$ 沿 %s，轨道矩阵 %d×%d、"
        u"秩 %d，逐个并进去后秩不升）＝%s（广义协变性在动能里的位置）"
        % (S["Mk"].rank(), len(ns), S["gdir"], S["Gg"].rows, S["Gg"].cols, S["Gg"].rank(), spanok))
    add("X3", S["Mkxi"].rank() == 10 and (S["Mk"] + S["Mgf"].subs(xi, 1)).rank() == 10,
        u"加规范固定后秩：一般 xi %d／10、xi=1 %d／10（撤掉规范固定那一项就不可逆，"
        u"EH 单独只有 %d／10）" % (S["Mkxi"].rank(), (S["Mk"] + S["Mgf"].subs(xi, 1)).rank(),
                                 S["Mk"].rank()))
    add("X4", tt["proportional"] and len(tt["a"]) == 1 and tt["mult"] == 5 and a_tt == u"-2",
        u"TT 5 格：B*A^-1 是对角同值矩阵（矩阵级成比例，不是只看特征值）⇒ 该通道确有单一 u，"
        u"a_TT = %s" % a_tt)
    add("X5", tt["da_dxi_zero"] is True and vv["da_dxi_zero"] is False
        and vv["a"] == [str(xi)],
        u"a_TT 对 xi 的偏导恒 0（规范不变）；a_V = %s 随 xi 走（偏导≠0）⇒ 它不是物理读数，"
        u"把它在 xi=1 的值当 a 的读数是换尺" % vv["a"])
    add("X6", sc["mixed"] is True and sc["a"] == sorted([str(xi), u"-2"]) and sc["deg"] == 2,
        u"sigma-h 动能混合项 %s ≠ 0 ⇒ 两格必须 2x2 联合求根，得 a ∈ {%s}；"
        u"分开按 1x1 求得的是 %s（另一对数，且次数账只有 1+1）"
        % (S["sh_off"], u"、".join(sc["a"]), u"、".join(sc["naive_1x1"])))
    BB = block_book(S)
    add("X7", FS[1] == 10 and BB[1] == 10 and FS[0] == BB[0] and all(S["offdiag"].values()),
        u"全 10x10 特征多项式根重数 %s（次数 %d）与逐块拼装账 %s（次数 %d）同值＝%s；"
        u"拼装用分块（TT／V／$\\sigma$-$h$ 联合）的 %d 个块间配对全零＝%s（$\\sigma$-$h$ 内部混合是 "
        u"X6 的读数，不在这一层）⇒ 度规 10 格闭合，鬼另 4 格"
        % (u"{%s}" % u", ".join(u"%s:%d" % kv for kv in sorted(FS[0].items())), FS[1],
           u"{%s}" % u", ".join(u"%s:%d" % kv for kv in sorted(BB[0].items())), BB[1],
           FS[0] == BB[0], len(S["offdiag"]), all(S["offdiag"].values())))
    add("X8", gh["proportional"] and gh["a"] == [u"0"]
        and Lam not in S["Gh"].free_symbols and gh["mult"] == 4,
        u"鬼动能 = k^2*I4（对角 %s）、自由符号 %s ⇒ 质量项恒 0、a_gh = 0（4 格）；"
        u"把对角 1 读成质量项＝把动能当质量" % (u"、".join(gh["kin"]),
                                             sorted(str(s) for s in S["Gh"].free_symbols) or u"无"))
    nz = bool(sp.simplify(S["e1"]) != 0)
    only_sc = (all(sp.simplify(t) == 0 for t in S["tad"][:8])
               and any(sp.simplify(t) != 0 for t in S["tad"][8:]))
    add("X9", nz and only_sc,
        u"eps^1（tadpole）非零＝%s：平坦背景 + Lam≠0 不是驻点；一次项在 York 基下只住在 sigma/h "
        u"两格（前 8 格全 0＝%s）⇒ 标量格的二阶读数带一阶污染，TT／矢量格不受影响" % (nz, only_sc))
    add("X10", CU["doc_standard_a"] == -2 and CU["doc_standard_a_src"] == u"卷十九 §3 现读"
        and a_tt == str(CU["doc_standard_a"]) and CU["corpus_narrow_readings"] == 0,
        u"独立期望：卷十九 §3 现读「标准取 a=%s」（来源＝%s）与本轮推导 a_TT=%s 同值＝HIT；"
        u"S14 全库 a 窄口径数值读数 %d 行（本轮之前盘上没有任何 a 读数）"
        % (CU["doc_standard_a"], CU["doc_standard_a_src"], a_tt, CU["corpus_narrow_readings"]))
    return ctl


def apply_mutant(S, R, CU, m):
    sp, xi = S["sp"], S["xi"]
    get = lambda ch: [x for x in R if x["ch"] == ch][0]
    if m == "m1":
        sc = get(u"S+H")
        sc["mixed"] = False
        sc["a"] = sc["naive_1x1"]
        sc["deg"] = 1
    elif m == "m2":
        vv = get(u"V")
        vv["a"] = [u"1"]
        vv["da_dxi_zero"] = True
    elif m == "m3":
        get(u"ghost")["a"] = list(get(u"ghost")["kin"])
    elif m == "m4":
        S["e1"] = sp.Integer(0)
        S["tad"] = [sp.Integer(0)] * 10
    elif m == "m5":
        S["naive_product"] = True
    elif m == "m6":
        get(u"TT")["proportional"] = False
    elif m == "m7":
        S["Gg"] = S["Gg_wrong"]
        S["gdir"] = S["gdir_wrong"]
    elif m == "m8":
        CU["doc_standard_a"] = -2
        CU["doc_standard_a_src"] = u"本轮 TT 读数回填"
    elif m == "m9":
        S["resid"] = S["resid_noparts"]
    elif m == "m10":
        S["Mkxi"] = S["Mk"]
    else:
        raise Bad(u"没有这枚变异体：%s" % m)
    return S, R, CU


# ---------------------------------------------------------------- 产物
def make_face(ctl, S, R, CU, FS, mode, mut, t0):
    bb = block_book(S)
    return {
        "name": NAME, "mode": mode, "mutant": mut,
        "stamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
        "elapsed_s": round(time.time() - t0, 3),
        "conventions": {
            "action_density": u"sqrt(g)*(R - 2*Lam)，总因子 -1/(32 pi G) 取 1",
            "background": u"平坦 delta（Rbar=0 ⇒ 只测 a 定义里的 Lam 那一半）",
            "momentum": u"k 沿 e3、|k|=1 ⇒ 两导数项 = k^2*f^2",
            "gauge": u"F_nu = d^mu h_{mu nu} - 1/2 d_nu h，S_gf = (1/(2 xi)) F^2",
            "currency": u"a_ch = rho_ch/Lam；rho_ch 是 (k^2*A_ch + Lam*B_ch) 的广义本征根"},
        "readings": R,
        "full_spectrum_mult": FS[0], "full_spectrum_degree": FS[1],
        "full_char_poly": FS[2], "block_book_mult": bb[0], "block_book_degree": bb[1],
        "sigma_h_mixed": str(S["sh_off"]), "york_offdiag_all_zero": S["offdiag"],
        "tadpole": {"nonzero": bool(S["sp"].simplify(S["e1"]) != 0),
                    "york_grad": [str(t) for t in S["tad"]]},
        "corpus": dict((k, v) for k, v in CU.items() if k != u"v19"),
        "corpus_v19_img": CU["v19"],
        "control_list": ctl,
        "controls_total": len(ctl),
        "controls_fired": len([x for x in ctl if x["ok"]]),
        "controls_red": [x["code"] for x in ctl if not x["ok"]],
        "expected_red": EXPECTED_RED,
        "judgment": {
            "a_is_single_valued": False,
            "a_TT": u"-2（5 格，规范不变）",
            "a_ghost": u"0（4 格，规范不变）",
            "a_V": u"xi（3 格，随规范走）",
            "a_scalar_joint": u"-2 与 xi（sigma-h 2x2 联合，不可分格）",
            "single_u_claim_in_doc": CU["doc_single_u_claim"]}}


def make_vol(ctl, S, R, CU, FS, t0):
    get = lambda ch: [x for x in R if x["ch"] == ch][0]
    tt, vv, sc, gh = get(u"TT"), get(u"V"), get(u"S+H"), get(u"ghost")
    bb = block_book(S)
    L = []
    P = L.append
    P(u"# 判定 · 进门闸 v13：平坦背景二阶变分的逐通道阈值宗量系数 a（读数格首次填上）")
    P(u"")
    P(u"- 承接：r79（进门闸 v12）判「$a$ 至今是一格【承诺】，不是一格【读数】」；本轮去量那一格。")
    P(u"- 被审对象：[%s](../../%s) §3 假设 A1 与 §8 闭合清单第 4 项" % (rel(VOL19), rel(VOL19)))
    v19t = txt(VOL19)
    P(u"- 对象图像（本册现场量）：%s（%d B／md5 `%s`／CRLF %d，共 %d 行；行口径＝剥去尾部换行后的"
      u"行数，即 `count(n)`−[文件以换行收尾]）"
      % (os.path.basename(VOL19), CU["v19"]["bytes"], CU["v19"]["md5"],
         CU["v19"]["crlf"], v19t.count("\n") + (0 if v19t.endswith("\n") else 1)))
    P(u"- 本册性质：符号推导＋盘上语料现扫；除本册三件产物外零写入；不动他人文件；未跑 refresh_catalog.py")
    P(u"- 运行：stamp %s；控制 %d/%d 点火、红 %s"
      % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
         len([x for x in ctl if x["ok"]]), len(ctl),
         u"、".join(x["code"] for x in ctl if not x["ok"]) or u"无"))
    P(u"")
    P(u"## §0 这一格要填的是什么")
    P(u"")
    P(u"卷十九 §3 把 NGFP 流方程的阈值宗量写成 $u=1+a\\lambda$，并说 $a$ 是「Hessian 中 $-2\\Lambda$ 与")
    P(u"$R$ 的组合系数（标准取 $a=-2$，即 $w=-2\\lambda$）」。那句话里有两个断言：")
    P(u"（一）$a$ 有**一个数**；（二）那个数是 $-2$。r79 已证盘上没有任何 $a$ 的数值读数（窄口径 0 行）")
    P(u"⇒ 两个断言都没被算过。本册从显式二阶变分把它们各自量一遍。")
    P(u"")
    P(u"## §1 约定（判决只吃约定无关的事实）")
    P(u"")
    P(u"| 项 | 取值 |")
    P(u"|---|---|")
    P(u"| 被积式 | $\\sqrt{g}(R-2\\Lambda)$，整体因子 $-1/(32\\pi G)$ 取 $1$（广义本征值是比值，与它无关） |")
    P(u"| 背景 | 平坦 $\\delta_{\\mu\\nu}$ ⇒ $\\bar R=0$：只测得 $a$ 定义里 $\\Lambda$ 那一半，$R$ 那一半是债 P |")
    P(u"| 动量 | 沿 $e_3$、$\\|k\\|=1$：$g=\\delta+\\varepsilon c f(x_3)$ ⇒ 两导数项 $=k^2f^2$，无导数项 $=f^2$ |")
    P(u"| 规范固定 | $F_\\nu=\\partial^\\mu h_{\\mu\\nu}-\\tfrac12\\partial_\\nu h$，$S_{gf}=(2\\xi)^{-1}\\delta^{\\mu\\nu}F_\\mu F_\\nu$ |")
    P(u"| 读数货币 | 通道分母 $k^2A_{ch}+\\Lambda B_{ch}$ 的广义本征根 $\\rho_{ch}$；$a_{ch}=\\rho_{ch}/\\Lambda$ |")
    P(u"")
    P(u"## §2 读数（全部由本册 sympy 现场算，无一处打字）")
    P(u"")
    P(u"| 通道 | 简并度 | $a_{ch}$ | 规范不变？ |")
    P(u"|---|---|---|---|")
    P(u"| TT（横迹） | %d | %s | 是（$\\partial/\\partial\\xi\\equiv0$） |" % (tt["mult"], tt["a"][0]))
    P(u"| 横矢量 | %d | %s | **否**（随 $\\xi$ 走） |" % (vv["mult"], vv["a"][0]))
    P(u"| $\\sigma$–$h$ 联合 | 2（不可分格） | %s | **否** |" % u"、".join(sc["a"]))
    P(u"| 鬼 | %d | %s | 是（动能 $=k^2I_4$，完全不含 $\\Lambda$） |" % (gh["mult"], gh["a"][0]))
    P(u"")
    P(u"全 $10\\times10$ 特征多项式（不经 York 基的第二条路）＝%s；根重数 %s、次数 %d。"
      % (FS[2], u"{%s}" % u", ".join(u"%s:%d" % kv for kv in sorted(FS[0].items())), FS[1]))
    P(u"逐块拼装账（$5+3+2$，标量按 $2\\times2$ 联合）＝%s（次数 %d），与上式同值（X7）。"
      % (u"{%s}" % u", ".join(u"%s:%d" % kv for kv in sorted(bb[0].items())), bb[1]))
    P(u"")
    P(u"## §3 判定")
    P(u"")
    P(u"1. **$a$ 不是单值（FAIL）**：度规 10 格的全谱根重数＝%s（次数 %d）⇒ 阈值宗量在这十格里至少"
      u"取两个不同值，其中 $a=%s$ 那一组随规范参数 $\\xi$ 走；鬼另 %d 格 $a=%s$。"
      u"假设 A1 的「单一 $u$」不是 Hessian 的结构。"
      % (u"{%s}" % u", ".join(u"%s:%d" % kv for kv in sorted(FS[0].items())), FS[1],
         vv["a"][0], gh["mult"], gh["a"][0]))
    P(u"2. **$a_{\\rm TT}=%s$ 成立（HIT）**：TT 通道 $B\\cdot A^{-1}$ 的 %d 个对角元逐格同值 $=%s$、"
      u"非对角全 $0$（矩阵级成比例，X4）⇒ 该通道确有单一 $u$；此读数与卷十九 §3 现读的「标准取 "
      u"$a=%s$」同值——本卷系里第一次由二阶变分复现的引用值。"
      % (tt["a"][0], tt["mult"], tt["diag"][0], CU["doc_standard_a"]))
    P(u"3. **$\\sigma$ 与 $h$ 不能分格读数（FAIL 的成因之一）**：动能混合项 $=%s\\neq0$，"
      u"分格按 $1\\times1$ 求得 %s，与联合根 %s 不同——若拿前者记账，简并度与全谱账都错。"
      % (S["sh_off"], u"、".join(sc["naive_1x1"]), u"、".join(sc["a"])))
    P(u"4. **平坦背景带 tadpole（BOUNDARY）**：$\\varepsilon^1$ 项非零，且在 York 基下只住在 $\\sigma,h$ 两格")
    P(u"   ⇒ 标量格的二阶读数与一阶污染同格；TT／矢量格不受影响。")
    P(u"5. **推论**：假设 A1 的「单一 $u$」不是 Hessian 的结构，而是**额外**的截断假设。任何由它算出的")
    P(u"   $(g_*,\\lambda_*)$ 要么只算 TT 通道（此时 $u=1-2\\lambda$、极点给出 T19-5 的 $\\lambda<\\tfrac12$，")
    P(u"   与本册读数自洽），要么把 $\\xi$ 依赖带进预言。")
    P(u"")
    P(u"## §4 语料侧对账（现扫，不吃任何人的字面量）")
    P(u"")
    P(u"- S14 全库「阈值宗量系数」宽口径 %d 行、按 A 尺 %d 行、窄口径数值读数 %d 行；"
      % (CU["corpus_mention_wide"], CU["corpus_mention_a"], CU["corpus_narrow_readings"]))
    P(u"  本轮的数只住在自己的面与卷里，不回填他人文件。")
    P(u"- 卷十九 §3 那句标准值由正则从盘上现读：$a=%s$（来源＝%s）；「宗量 $u=1+a\\lambda$」现读命中＝%s。"
      % (CU["doc_standard_a"], CU["doc_standard_a_src"], CU["doc_single_u_claim"]))
    P(u"- 本册落库时刻的资料索引图像＝%d B／md5 `%s`／条目行 %d（注册步要与注册前备份做两源核对；"
      u"并发写者同窗动过索引时以行数增量为准）。" % (CU["index_at_run"]["bytes"],
        CU["index_at_run"]["md5"], CU["index_rows_at_run"]))
    P(u"")
    P(u"## §5 控制逐条（期望由对象与现算给，题面由本册印）")
    P(u"")
    for x in ctl:
        P(u"- %s %s：%s" % (u"绿" if x["ok"] else u"红", x["code"], x["desc"]))
    P(u"")
    P(u"## §6 变异体（十枚，各顶一枚指定控制；期望由 EXPECTED_RED 字面量现推）")
    P(u"")
    P(u"| 变异 | 换掉的尺／对象 | 指定红 |")
    P(u"|---|---|---|")
    MUTDESC = {
        "m1": u"丢掉 $\\sigma$–$h$ 混合，两格各按 $1\\times1$ 求根",
        "m2": u"把 $a_V=\\xi$ 在 $\\xi=1$ 处的数值当规范不变读数",
        "m3": u"把鬼动能矩阵的对角 $1$ 读成质量项（$a_{\\rm gh}=1$）",
        "m4": u"断言 $\\varepsilon^1$ 恒零（无视 tadpole）",
        "m5": u"全谱按逐块 $1\\times1$ 行列式拼装（标量两格被拆开）",
        "m6": u"撤掉 TT 通道的矩阵级成比例判定（只按特征值同值记账，非对角全零不再验）",
        "m7": u"微分同胚轨道取错方向（$k$ 沿 $e_0$）：维数对、方向错",
        "m8": u"「标准 $a$」不现读卷十九，而由本轮 TT 读数回填",
        "m9": u"$\\varepsilon^2$ 分家不把 $ff''$ 分部积分（残差不闭）",
        "m10": u"撤掉规范固定项却宣布传播子可逆"}
    for m in sorted(EXPECTED_RED, key=lambda s: int(s[1:])):
        P(u"| %s | %s | %s |" % (m, MUTDESC[m], EXPECTED_RED[m]))
    P(u"")
    P(u"## §7 诚实边界与未偿债")
    P(u"")
    P(u"- 债 P：$\\bar R\\neq0$ 的爱因斯坦背景上 $a$ 的 $R$ 那一半未测（本册只到 $\\Lambda$ 那一半）；")
    P(u"  卷十九 §3 那句定义要两半都测完才算复现。")
    P(u"- 债 Q：本轮读数在**平坦 + tadpole** 背景上；严格做法是先把背景推到驻点（$\\bar R=4\\Lambda$）")
    P(u"  再展开——债 P 与债 Q 同一轮可并。")
    P(u"- 债 R：系数组 $(c_i,d_i)$ 仍未定（卷十九 V19-H1 的第 1–3 项：迹计算、鬼的 $\\bar R$ 耦合、")
    P(u"  York 雅可比）⇒ 本册**不给** $(g_*,\\lambda_*)$，红线不动。")
    P(u"- 债 K（承接 r79）：TT 约束下 $\\mathfrak L_1$ 归零仍未闭合——本轮只把 $a$ 从承诺变成读数，")
    P(u"  并证明它不是单值。")
    P(u"- 本轮无四力词表新增、无晋升数新增；减掉一条假确定（「$a$ 是单值」），补上一格真读数")
    P(u"  （$a_{\\rm TT}=-2$、$a_{\\rm gh}=0$、$a$ 的 $\\xi$ 依赖谱）。统一场论仍 OPEN。")
    P(u"")
    P(u"WITNESS_LINE：本卷数字只住在①本判定卷 §2／§5／§6、②同名数据面 JSON、③见证册三处；")
    P(u"§5 每条题面由仪器当场重跑逐字复现。")
    P(u"")
    return u"\r\n".join(L) + u"\r\n"


def main(argv):
    mode = u"check"
    mut = None
    for a in argv[1:]:
        if a == "--land":
            mode = u"land"
        elif a == "--check":
            mode = u"check"
        elif a.startswith("--mutant="):
            mode = u"mutant"
            mut = a.split("=", 1)[1]
            if mut not in EXPECTED_RED:
                raise Bad(u"没有这枚变异体：%s" % mut)
    if mode == u"land":
        for p in (INSTR, FACE, VOL):
            if os.path.isfile(p):
                raise Bad(u"产物已存在，拒绝覆盖：%s" % rel(p))
    t0 = time.time()
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0))
    S = build()
    R = readings(S)
    CU = corpus_a()
    FS = full_spectrum(S)
    if mode == u"mutant":
        S, R, CU = apply_mutant(S, R, CU, mut)
    ctl = run_controls(S, R, CU, FS)
    print(u"进门闸 v13  mode=%s mutant=%s stamp=%s" % (mode, mut, stamp))
    for x in ctl:
        print(u"%s %s: %s" % (u"绿" if x["ok"] else u"红", x["code"], x["desc"]))
    red = [x["code"] for x in ctl if not x["ok"]]
    print(u"控制 %d/%d 点火、红 %s、mode=%s、耗时 %.2f s、stamp %s"
          % (len(ctl) - len(red), len(ctl), red, mode, time.time() - t0, stamp))
    if mode == u"check":
        if red:
            raise Bad(u"--check 有红：%s" % red)
        print(u"CHECK_OK 10/10（本模式不落任何文件）")
        return 0
    if mode == u"mutant":
        want = EXPECTED_RED[mut]
        linked = [x for x in red if x != want]
        print(u"MUT=%s 指定控制 %s %s；连带红＝[%s]；期望由 EXPECTED_RED 字面量现推" % (
            mut, want, u"已红" if want in red else u"未红", u", ".join(linked)))
        if want not in red or linked:
            raise Bad(u"变异体 %s 未按要求只红一枚（实得红 %s）" % (mut, red))
        return 1
    if red or len([x for x in ctl if x["ok"]]) != 10:
        raise Bad(u"--land 控制未全绿：%d/10（不得落任何产物）" % len([x for x in ctl if x["ok"]]))
    face = make_face(ctl, S, R, CU, FS, mode, mut, t0)
    js = json.dumps(face, ensure_ascii=False, indent=1, default=str).replace(u"\n", u"\r\n")
    vol = make_vol(ctl, S, R, CU, FS, t0)
    # 两件文本都算完才动第一次写盘：否则崩在中途会留下「活落了、账半张」的孤儿面
    os.makedirs(os.path.dirname(FACE), exist_ok=True)
    open(FACE, "wb").write(js.encode("utf-8"))
    open(VOL, "wb").write(vol.encode("utf-8"))
    back = json.loads(txt(FACE))
    if (back["controls_fired"], back["controls_total"], len(back["control_list"]),
        back["mode"]) != (10, 10, 10, u"land"):
        raise Bad(u"面回读自证不符：%s" % ((back["controls_fired"], back["controls_total"],
                                          len(back["control_list"]), back["mode"]),))
    src = os.path.abspath(__file__)
    if os.path.abspath(src) != os.path.abspath(INSTR):
        shutil.copyfile(src, INSTR)
    for p in (INSTR, FACE, VOL):
        st = img(p)
        print(u"      %s %d B  md5 %s  CRLF %d / LF %d" % (rel(p), st["bytes"], st["md5"],
                                                          st["crlf"], st["lf"]))
    print(u"LAND_OK 10/10")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Bad as e:
        print(u"FATAL: %s" % e)
        sys.exit(2)
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(3)
