# -*- coding: utf-8 -*-
"""进门闸 v11 · 「自名输出件」对账 ＋ 卷二十从未点火的符号核独立复核 · 2026-10-19

问题只有两句：
  (a) 全仓有多少脚本**自己在源码里印出了它该产出的文件名**，而那些文件在盘上不存在？
  (b) 其中唯一成系列的缺席者（S14 卷二十两枚）里，那张声称给出「阈值宗量系数 a 的推导」的
      Hessian 引擎，它的**符号核**到底对不对？

尺子的来历（本册自己欠的两笔，都印在面上）：
  v2 把任意顶层 `Expr` 当执行 ⇒ docstring 也算「在跑」，读数 477/586 与卷二十实测矛盾；
  v3 把「点火」定义成「顶层 Expr 调本模块自己的 def」⇒ 漏掉主体写在顶层的脚本与
     `sys.exit(main())`（被调者是 `sys.exit`），读数 112 枚「从不点火」里绝大多数真在跑。
  两把坏尺都留档，因为「缺席」这件事只有用**盘上文件名存在性**才判得动：
     候选 = 源码里印了以自身文件名为前缀的 .txt/.json/.md/.csv 件名；判决 = 那个名在不在盘上。
本册不跑真源（它会 `os.makedirs(ROOT/09_验证结果/原始运行记录)`，那是别人的归档目录），
而是把它逐字节复制进沙箱后 import；S14 归档目录前后件数与集合差由 X4 现场量。
符号核对的期望值不拍脑袋：第三路线（本册自写的显式 Christoffel/Ricci）先用 X5 的正对照
验刀（eps=0 时逐点 R₀＝d(d−1)、平坦背景 R₀＝0），再与引擎的符号 L2、引擎的数值蛮力并列三档 d。
"""
import ast
import glob
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import sys
import time
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

ROOT = r"D:\a10\aikjx\code\my_lib\openuft"
SCR = r"D:\a10\aikjx\code\my_lib\scratch"
PROJ = os.path.join(ROOT, u"04_公共成果", u"本项目_全维自洽与归一化")
NAME = u"进门闸_v11_自名输出件对账与卷二十符号核独立复核_2026-10-19"
V10 = u"进门闸_v10_D5外部验证流程可执行性核查_2026-10-19"
S14 = os.path.join(ROOT, u"01_独立体系", u"S14_挠率统一场论TUFT")
RAW14 = os.path.join(S14, u"09_验证结果", u"原始运行记录")
SRC_DIR = os.path.join(S14, u"07_计算复现", u"源码")
ENG20 = os.path.join(SRC_DIR, u"tuft_卷二十_Hessian二阶变分机器求导.py")
ENG20B = os.path.join(SRC_DIR, u"tuft_卷二十_二阶变分管线与规范鬼雅可比.py")
STEM20 = os.path.splitext(os.path.basename(ENG20))[0]
SB = os.path.join(SCR, "v11_sandbox")
SB_DIR = os.path.join(SB, "S14x", u"07_计算复现", u"源码")
SB_ENG = os.path.join(SB_DIR, os.path.basename(ENG20))
CATALOG = os.path.join(ROOT, u"00_项目治理", u"资料索引", "material_catalog.md")
VERIFY = os.path.join(ROOT, u"verify.py")
MCAT = os.path.join(ROOT, u"00_项目治理", u"维护工具", "module_catalog.py")
V10_FACE = os.path.join(PROJ, u"数据", V10 + ".json")
PATTERNS = [u"01_独立体系/*/07_计算复现/源码/*.py",
            u"04_公共成果/*/源码/*.py",
            u"04_公共成果/*/*.py",
            u"04_公共成果/*/数据/*.py"]
TOL_AGREE = 1e-5          # 符号↔第三路：三档 d 一致到此以内
TOL_BLADE = 1e-9         # X5 刀自己的正对照
SERIES = [u"卷十七", u"卷十八", u"卷十九", u"卷二十"]


class Fatal(Exception):
    pass


def img(p):
    b = open(p, "rb").read()
    return {"bytes": len(b), "md5": hashlib.md5(b).hexdigest(),
            "crlf": b.count(b"\r\n"), "lf": b.count(b"\n"), "raw": b}


def txt(p):
    return img(p)["raw"].decode("utf-8", "replace")


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def sweep_inputs(paths):
    return {str(p): img(p)["md5"] for p in paths if os.path.isfile(p)}


def load_engine():
    """逐字节副本进沙箱再 import：真源顶层会 makedirs 别人的归档目录。"""
    a = open(ENG20, "rb").read()
    if os.path.exists(SB_ENG):
        if open(SB_ENG, "rb").read() != a:
            raise Fatal(u"沙箱副本与源不符（源已漂移）")
    else:
        os.makedirs(SB_DIR)
        shutil.copyfile(ENG20, SB_ENG)
    if img(SB_ENG)["md5"] != img(ENG20)["md5"]:
        raise Fatal(u"沙箱副本 md5 与源不符")
    spec = importlib.util.spec_from_file_location(STEM20, SB_ENG)
    m = importlib.util.module_from_spec(spec)
    sys.modules[STEM20] = m
    spec.loader.exec_module(m)
    return m


def declared_names(path):
    text = txt(path)
    stem = os.path.splitext(os.path.basename(path))[0]
    out = set()
    for mm in re.finditer(r"""["']([^"'\\/\r\n]{4,140}?\.(?:txt|json|md|csv))["']""", text):
        n = mm.group(1)
        if n.startswith(stem) or stem in n:
            out.add(n)
    return sorted(out)


def engine_shape(path):
    """从 AST 找回那台引擎自己的形状：顶层副作用在第几行、有几个自有函数、文件止于什么。"""
    raw = img(path)["raw"].decode("utf-8", "replace")
    t = ast.parse(raw)
    body = t.body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]
    tops = []
    src_lines = raw.replace("\r\n", "\n").split("\n")
    for n in body:
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call):
            tops.append((n.lineno, src_lines[n.lineno - 1].strip()[:64]))
    own = [n.name for n in body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
    kinds = Counter(type(n).__name__ for n in body)
    span = {}
    for n in body:
        if isinstance(n, ast.FunctionDef):
            end = max(getattr(x, "lineno", n.lineno) for x in ast.walk(n)
                      if hasattr(x, "lineno"))
            span[n.name] = (n.lineno, end)
    last = body[-1] if body else None
    out_assign = []
    for n in body:
        if isinstance(n, ast.Assign):
            for tg in n.targets:
                if isinstance(tg, ast.Name) and re.match(
                        u"(OUTDIR|REPORT_PATH|JSON_PATH|OUT_PATH)$", tg.id):
                    out_assign.append((tg.id, n.lineno))
    return {"lines": raw.replace("\r\n", "\n").count("\n") + 1,
            "top_effect_lines": tops, "own_defs": len([
                n for n in body if isinstance(n, ast.FunctionDef)]),
            "own_functions": [n.name for n in body if isinstance(n, ast.FunctionDef)],
            "own_classes": len([n for n in body if isinstance(n, ast.ClassDef)]),
            "class_names": [n.name for n in body if isinstance(n, ast.ClassDef)],
            "out_assign_lines": out_assign,
            "kinds": dict(kinds), "fn_span": span,
            "last_stmt": type(last).__name__ if last else None,
            "last_lineno": getattr(last, "lineno", 0),
            "guard": any(isinstance(n, ast.If) and "__main__" in ast.dump(n.test) for n in body),
            "names": own}


# ---------------------------------------------------------------- 第三路线（本册自写）
def metric_and_derivs(np, d, sphere, amps, kvec, phase, eps, L, N):
    xs = np.linspace(-L, L, N)
    mesh = np.meshgrid(*([xs] * d), indexing="ij")
    shape = mesh[0].shape
    r2 = sum(mm ** 2 for mm in mesh)
    if sphere:
        Om = 2.0 / (1.0 + r2)
        df = [-2.0 * mesh[t] / (1.0 + r2) for t in range(d)]
        dOm = [Om * df[t] for t in range(d)]
        ddOm = np.zeros(shape + (d, d))
        for a in range(d):
            for b in range(d):
                ddOm[..., a, b] = (Om * (-2.0 * (1.0 if a == b else 0.0) / (1.0 + r2)
                                         + 4.0 * mesh[a] * mesh[b] / (1.0 + r2) ** 2)
                                   + dOm[a] * df[b])
    else:
        Om = np.ones(shape)
        dOm = [np.zeros(shape) for _ in range(d)]
        ddOm = np.zeros(shape + (d, d))
    ang = np.array(phase, dtype=float) + sum(kvec[t] * mesh[t] for t in range(d))
    c, s = np.cos(ang), np.sin(ang)
    g = np.zeros(shape + (d, d))
    dg = np.zeros(shape + (d, d, d))
    ddg = np.zeros(shape + (d, d, d, d))
    for mu in range(d):
        for nu in range(d):
            a = amps[mu][nu]
            base = (1.0 if mu == nu else 0.0) + eps * a * c
            g[..., mu, nu] = Om ** 2 * base
            for p in range(d):
                dg[..., p, mu, nu] = (2 * Om * dOm[p] * base
                                      + Om ** 2 * eps * (-a * kvec[p] * s))
                for q in range(d):
                    ddg[..., p, q, mu, nu] = (
                        (2 * dOm[q] * dOm[p] + 2 * Om * ddOm[..., q, p]) * base
                        + 2 * Om * dOm[q] * eps * (-a * kvec[p] * s)
                        + 2 * Om * dOm[p] * eps * (-a * kvec[q] * s)
                        + Om ** 2 * eps * (-a * kvec[p] * kvec[q] * c))
    return mesh, shape, g, dg, ddg


def curvature(np, shape, d, g, dg, ddg):
    ginv = np.linalg.inv(g)
    detg = np.linalg.det(g)
    sqrtg = np.sqrt(np.abs(detg)) * np.sign(detg)
    dginv = np.zeros(shape + (d, d, d))
    for D in range(d):
        for a in range(d):
            for b in range(d):
                acc = np.zeros(shape)
                for p in range(d):
                    for q in range(d):
                        acc = acc - ginv[..., a, p] * dg[..., D, p, q] * ginv[..., q, b]
                dginv[..., D, a, b] = acc
    Gam = np.zeros(shape + (d, d, d))
    for l in range(d):
        for mu in range(d):
            for nu in range(d):
                acc = np.zeros(shape)
                for sg in range(d):
                    acc = acc + ginv[..., l, sg] * (dg[..., mu, sg, nu]
                                                    + dg[..., nu, sg, mu]
                                                    - dg[..., sg, mu, nu])
                Gam[..., l, mu, nu] = 0.5 * acc
    dGam = np.zeros(shape + (d, d, d, d))
    for D in range(d):
        for l in range(d):
            for mu in range(d):
                for nu in range(d):
                    acc = np.zeros(shape)
                    for sg in range(d):
                        acc = acc + dginv[..., D, l, sg] * (dg[..., mu, sg, nu]
                                                            + dg[..., nu, sg, mu]
                                                            - dg[..., sg, mu, nu])
                        acc = acc + ginv[..., l, sg] * (ddg[..., D, mu, sg, nu]
                                                        + ddg[..., D, nu, sg, mu]
                                                        - ddg[..., D, sg, mu, nu])
                    dGam[..., D, l, mu, nu] = 0.5 * acc
    Ric = np.zeros(shape + (d, d))
    for mu in range(d):
        for nu in range(d):
            acc = np.zeros(shape)
            for D in range(d):
                acc = acc + dGam[..., D, D, nu, mu] - dGam[..., nu, D, D, mu]
            for D in range(d):
                for E in range(d):
                    acc = acc + Gam[..., D, D, E] * Gam[..., E, nu, mu]
                    acc = acc - Gam[..., D, nu, E] * Gam[..., E, D, mu]
            Ric[..., mu, nu] = acc
    Rsc = np.zeros(shape)
    for mu in range(d):
        for nu in range(d):
            Rsc = Rsc + ginv[..., mu, nu] * Ric[..., mu, nu]
    return sqrtg, Rsc


def ref_action(np, m, d, sphere, lam, amps, kvec, phase, eps, L, N):
    _, shape, g, dg, ddg = metric_and_derivs(np, d, sphere, amps, kvec, phase, eps, L, N)
    sqrtg, Rsc = curvature(np, shape, d, g, dg, ddg)
    return float(np.mean(sqrtg * (2.0 * lam - Rsc)) * (2.0 * L) ** d)


def blade_R(np, m, d, sphere, amps, kvec, phase, L, N):
    _, shape, g, dg, ddg = metric_and_derivs(np, d, sphere, amps, kvec, phase, 0.0, L, N)
    _, Rsc = curvature(np, shape, d, g, dg, ddg)
    return float(Rsc.min()), float(Rsc.max()), float(Rsc.mean())


def symbolic_S2(sp, np, h, L2, amps, kvec, phase, L, N):
    xs = h.xs
    mesh = np.meshgrid(*([np.linspace(-L, L, N)] * h.d), indexing="ij")
    shape = mesh[0].shape
    kx = sum(kvec[i] * xs[i] for i in range(h.d))
    cache = {}

    def atom_value(fid, dv):
        key = (fid, dv)
        if key not in cache:
            a_mu, a_nu = h.fields[fid]
            e = amps[a_mu][a_nu] * sp.cos(kx + phase)
            for mu in dv:
                e = sp.diff(e, xs[mu])
            f = sp.lambdify(list(xs), sp.simplify(e), modules="numpy")
            cache[key] = np.asarray(f(*mesh), dtype=float)
        return cache[key]

    acc = np.zeros(shape, dtype=float)
    n_terms = 0
    for term, coeff in L2.t.items():
        if len(term) != 2:
            continue
        n_terms += 1
        gv = np.asarray(sp.lambdify(list(xs), sp.simplify(coeff), modules="numpy")(*mesh),
                        dtype=float)
        if gv.shape != shape:
            gv = np.broadcast_to(gv, shape)
        prod = np.array(gv, dtype=float)
        for fid, dv in term:
            av = atom_value(fid, dv)
            prod = prod * (av if av.shape == shape else np.full(shape, float(av)))
        acc = acc + prod
    return float(np.mean(acc) * (2.0 * L) ** h.d), n_terms, len(cache)


def richardson(fn, hh=0.05):
    f0 = fn(0.0)

    def D(x):
        return (fn(x) - 2 * f0 + fn(-x)) / (x * x)

    d1, d2, d3 = D(hh), D(hh / 2), D(hh / 4)
    return ((4 * d3 - d2) / 3.0) / 2.0, ((4 * d2 - d1) / 3.0) / 2.0


def run(mut=None, land=False):
    t0 = time.time()
    F = []
    red = []

    def C(code, desc, ok):
        F.append((code, desc, bool(ok)))
        if not ok:
            red.append(code)
        return bool(ok)

    # ---- 输入快照（只读复量的底）----
    files = []
    for pat in PATTERNS:
        files += glob.glob(os.path.join(ROOT, pat.replace("/", os.sep)))
    files = sorted(set(files))
    name_index = Counter()
    dir_seen = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [dd for dd in dirnames if dd not in (".git", "__pycache__")]
        for fn in filenames:
            name_index[fn] += 1
        dir_seen.append(dirpath)
    parse_fail = []
    for p in files:
        try:
            ast.parse(open(p, "rb").read().decode("utf-8", "replace"))
        except (SyntaxError, ValueError) as e:
            parse_fail.append((rel(p), type(e).__name__))
    C(u"X1", u"语料非空：三类 glob 并集 %d 枚（解析失败 %d 枚）、全仓文件名索引 %d 个不同名，"
      u"都不许塌成零" % (len(files), len(parse_fail), len(name_index)),
      len(files) > 0 and len(name_index) > 0)

    pop = []
    for p in files:
        nms = declared_names(p)
        if nms:
            pop.append((p, nms, {n: name_index[n] for n in nms}))
    absent = [(p, nms, hits) for p, nms, hits in pop if all(v == 0 for v in hits.values())]
    present = [(p, nms, hits) for p, nms, hits in pop if any(v > 0 for v in hits.values())]

    # X2：缺席集必须真由「卷二十系」构成——不是恒真，m3 把靶换成卷十九时该红
    absent_paths = sorted([rel(p) for p, _, _ in absent])
    only20 = len(absent) > 0 and all(u"卷二十" in a for a in absent_paths)
    C(u"X2", u"缺席者非空且全部属卷二十系（%d／%d 候选）" % (len(absent), len(pop)), only20)

    # X3：同系列相邻卷在盘上有产物，唯独卷二十 0 件
    fs14 = sorted(os.listdir(RAW14)) if os.path.isdir(RAW14) else []
    series_count = {}
    for sg in SERIES:
        series_count[sg] = sum(1 for f in fs14 if sg in f)
    C(u"X3", u"归档分母非空（%d 件）且卷十七/十八/十九各有产物、卷二十件数严格小于它们" % len(fs14),
      len(fs14) > 0 and series_count.get(u"卷二十", 0) == 0
      and all(series_count.get(k, 0) > 0 for k in (u"卷十七", u"卷十八", u"卷十九")))

    # X4：沙箱纪律——import 前后 S14 归档目录一字不动
    pre14 = set(fs14)
    pre_cat = img(CATALOG)["md5"]
    m = load_engine()
    post14 = set(sorted(os.listdir(RAW14)))
    C(u"X4", u"点火只发生在沙箱：S14 归档目录前后差 %d 件、资料目录 md5 未动、"
      u"沙箱那侧的 09_验证结果 确实被建出（副作用有落点）＝%s" % (
        len(pre14 ^ post14), os.path.isdir(os.path.join(SB, "S14x", u"09_验证结果"))),
      (pre14 ^ post14) == set() and img(CATALOG)["md5"] == pre_cat
      and os.path.isdir(os.path.join(SB, "S14x", u"09_验证结果", u"原始运行记录")))
    esh = engine_shape(ENG20)

    np, sp = m.np, m.sp
    amps0 = [[0.0] * 3 for _ in range(3)]
    kv3 = [1.0, 0.0, 0.0]
    L, N, phase, lam = 2.0, 8, 0.37, 0.3
    rmin, rmax, rmean = blade_R(np, m, 3, True, amps0, kv3, phase, L, N)
    fmin, fmax, fmean = blade_R(np, m, 3, False, amps0, kv3, phase, L, N)
    C(u"X5", u"刀自己的正对照：本册显式 Christoffel/Ricci 在 eps=0 时逐点 R₀＝6（球面）／0（平坦）"
      u"（实测球面 %.3e／平坦 %.3e）" % (abs(rmean - 6.0), abs(fmean)),
      abs(rmin - 6.0) < TOL_BLADE and abs(rmax - 6.0) < TOL_BLADE and abs(fmean) < TOL_BLADE)

    # ---- 三档 d 的三路并列 ----
    rows = []
    for d in (2, 3, 4):
        amps = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
        kvec = [1.0] + [0.0] * (d - 1)
        _, shape, g, dg, ddg = metric_and_derivs(np, d, True, amps, kvec, phase, 0.0, L, N)
        _, Rsc = curvature(np, shape, d, g, dg, ddg)
        h = m.Hess(d, True, str(lam))
        L1, L2 = h.build()
        sym, n_terms, n_atoms = symbolic_S2(sp, np, h, L2, amps, kvec, phase, L, N)
        ref_hi, ref_lo = richardson(
            lambda e: ref_action(np, m, d, True, lam, amps, kvec, phase, e, L, N))
        eng_hi, eng_lo = m.extract_S2(
            lambda e: m.brute_action(d, True, lam, amps, kvec, phase, e, L=L, N=N), h=0.05)
        rel_sym = abs(sym - ref_hi) / max(abs(ref_hi), 1e-30)
        rel_eng = abs(eng_hi - ref_hi) / max(abs(ref_hi), 1e-30)
        rows.append({"d": d, "R0_pointwise": rmean_of(Rsc), "S2_symbolic": sym,
                     "S2_third_route": ref_hi, "S2_engine_brute": eng_hi,
                     "rel_sym_vs_third": rel_sym, "rel_engine_vs_third": rel_eng,
                     "ratio_engine_over_third": eng_hi / ref_hi if ref_hi else None,
                     "terms_L2": n_terms, "atoms": n_atoms, "L1_terms": len(L1.t)})
    agree_all = len(rows) >= 3 and all(r["rel_sym_vs_third"] < TOL_AGREE for r in rows)
    C(u"X6", u"符号 L2 ↔ 第三路线 三档 d 全部一致（最大相对差 %.3e < %g，档数 %d）" % (
        max(r["rel_sym_vs_third"] for r in rows), TOL_AGREE, len(rows)), agree_all)
    DISAGREE = 100 * TOL_AGREE
    break_all = all(r["rel_engine_vs_third"] > DISAGREE for r in rows)
    C(u"X7", u"引擎自己的数值蛮力 ↔ 第三路线 三档 d 全部超出符合容差（相对差 %s > %g）；"
      u"不符的成因在别人文件里，本册不代改" % (
        u"／".join(u"d%d:%.3e" % (r["d"], r["rel_engine_vs_third"]) for r in rows), DISAGREE),
      break_all)

    # ---- 背景条件（L1）：Λ 能否单独消掉线性项 ----
    ecc = []
    for d in (2, 3, 4, 5):
        h = m.Hess(d, True, "lam")
        L1, _ = h.build()
        nz = []
        for k, v in sorted(L1.t.items(), key=lambda x: str(x[0])):
            r = sp.simplify(sp.sympify(v).subs({"lam": sp.Rational(d * (d - 1), 2)}))
            if r != 0:
                nz.append(((k[0][0], k[0][1]), str(r)[:40]))
        ecc.append({"d": d, "L1_terms": len(L1.t), "terms_after_Lambda": len(nz),
                    "Lambda_einstein": d * (d - 1) / 2.0, "sample": nz[:2]})
    C(u"X8", u"背景条件可判：每档 d 都能算出 L1 项数与代入 Λ＝d(d−1)/2 后的非零项数，"
      u"且档数不少于 %d（%s）" % (4, u"、".join(
          u"d%d:%d→%d" % (e["d"], e["L1_terms"], e["terms_after_Lambda"]) for e in ecc)),
      len(ecc) >= 4 and all(e["L1_terms"] > 0 and e["terms_after_Lambda"] >= 0 for e in ecc))

    inputs = sorted(set([ENG20, ENG20B, CATALOG, VERIFY, MCAT, V10_FACE, SB_ENG]
                        + [p for p, _, _ in absent]
                        + [p for p, _, _ in present[:12]]))
    snap = sweep_inputs(inputs)
    moved = [p for p, d0 in snap.items() if img(p)["md5"] != d0]
    C(u"X9", u"判决计算后复量 %d 份输入，移动 %d 份" % (len(snap), len(moved)), not moved)

    # ---- 变异体：每枚只打破一枚指定控制，打破不了则仪器自己 FATAL ----
    EXPECTED_RED = {u"m1": u"X5", u"m2": u"X6", u"m3": u"X2", u"m4": u"X9", u"m5": u"X8"}

    def set_ctl(code, ok, tag):
        for i, (c, dsc, o) in enumerate(F):
            if c == code:
                F[i] = (c, dsc + u"（MUT=%s）" % tag, bool(ok))
        return bool(ok)

    if mut:
        if mut not in EXPECTED_RED:
            raise Fatal(u"未知变异体 %s" % mut)
        tag = EXPECTED_RED[mut] + u":" + mut_desc(mut)
        if mut == u"m1":
            set_ctl(u"X5", False, tag)          # 撤掉刀自己的正对照＝用一把没验过的刀
        elif mut == u"m2":
            for r in rows:
                r["rel_sym_vs_third"] = abs(r["S2_symbolic"] - r["S2_engine_brute"]) \
                    / max(abs(r["S2_engine_brute"]), 1e-30)
            set_ctl(u"X6", all(r["rel_sym_vs_third"] < TOL_AGREE for r in rows), tag)
        elif mut == u"m3":
            nineteen = sum(1 for f in fs14 if u"卷十九" in f)
            set_ctl(u"X2", only20 and nineteen == 0, tag)
        elif mut == u"m4":
            keep = open(SB_ENG, "rb").read()
            open(SB_ENG, "ab").write(b"\r\n")   # 判决之后动了本册自己的输入图像
            mv = [p for p, d0 in snap.items() if img(p)["md5"] != d0]
            set_ctl(u"X9", not mv, tag)
            open(SB_ENG, "wb").write(keep)      # 还原，否则下一轮的 md5 自证会假崩
        elif mut == u"m5":
            set_ctl(u"X8", len(ecc[:2]) >= 4, tag)
        want = EXPECTED_RED[mut]
        got = [c for c, dsc, o in F if not o]
        if want not in got:
            raise Fatal(u"变异体 %s 没能打破指定控制 %s（当前红＝%s）" % (mut, want, got))
        print(u"MUT=%s（%s）：指定控制 %s 已红；连带红＝%s" % (
            mut, mut_desc(mut), want, [c for c in got if c != want]))

    moved = [p for p, d0 in snap.items() if img(p)["md5"] != d0]
    face_inputs = {"inputs": len(snap), "moved": moved}

    elapsed = time.time() - t0
    face = {
        "name": NAME, "mode": ("land" if land else ("mutant" if mut else "check")),
        "mutant": mut, "stamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_s": round(elapsed, 2),
        "denominator": {
            "glob_union": len(files), "parse_fail": len(parse_fail),
            "parse_fail_sample": parse_fail[:3],
            "name_index_unique": len(name_index),
            "name_index_total": sum(name_index.values()),
            "self_naming_candidates": len(pop),
            "candidates_with_artifact": len(present),
            "candidates_all_absent": len(absent),
            "absent_paths": absent_paths,
            "absent_declared": {rel(p): nms for p, nms, _ in absent},
            "s14_raw_archive": len(fs14), "series_counts": series_count,
        },
        "discarded_rulers": {
            "v2": u"顶层任意 Expr 当执行（docstring 也算）⇒ 前置探针读数 477/586 与卷二十矛盾",
            "v3": u"点火＝顶层 Expr 调本模块自己的 def ⇒ 漏主体在顶层的脚本与 sys.exit(main())，"
                  u"前置探针把 112 枚判成「从不点火」（它们是 --check 型或主体写在顶层）",
            "口径": u"以下两枚数字来自本册之前的只读探针（_probe_inert_v2/v3），不由本仪器复算，"
                  u"只作「为什么换尺」的留档",
        },
        "engine": {"path": rel(ENG20), "bytes": img(ENG20)["bytes"], "md5": img(ENG20)["md5"],
                   "crlf": img(ENG20)["crlf"], "sandbox": rel(SB_ENG),
                   "sandbox_same": img(SB_ENG)["md5"] == img(ENG20)["md5"],
                   "shape": esh},
        "three_routes": rows,
        "blade": {"sphere_R0_mean": rmean, "sphere_R0_min": rmin, "sphere_R0_max": rmax,
                  "flat_R0_mean": fmean, "tol": TOL_BLADE},
        "ecc": ecc,
        "read_only_sweep": face_inputs,
        "controls_total": len(F), "controls_fired": len(F) - len(red_now(F)),
        "controls_red": red_now(F),
        "control_list": [{"code": c, "desc": dsc, "ok": o} for c, dsc, o in F],
        "tol_agree": TOL_AGREE,
        "governance": {"catalog_md5": img(CATALOG)["md5"],
                       "catalog_rows": len(re.findall(r"^- \[", txt(CATALOG), re.M)),
                       "s14_dir_changed": sorted(pre14 ^ post14)},
    }
    return face, F, rows, ecc, absent_paths, pop, series_count, len(fs14), rmean, fmean, elapsed, m


def rmean_of(Rsc):
    return float(Rsc.mean())


def red_now(F):
    return [c for c, dsc, o in F if not o]


def mut_desc(k):
    return {u"m1": u"撤掉刀自己的正对照",
            u"m2": u"把第三路线换成引擎自己的数值蛮力（差异实验抹平单一变量）",
            u"m3": u"把缺席靶换成盘上真有产物的卷十九",
            u"m4": u"判决之后移动本册自己的输入图像（只读复量失效）",
            u"m5": u"把背景条件的 d 档从四档砍到两档（覆盖分母塌缩）"}[k]


def volume(face, F, rows, ecc, absent_paths, pop, series_count, n14, rmean, fmean, elapsed):
    d0 = face["denominator"]
    L = []
    P = L.append
    P(u"# 判定 · 进门闸 v11 · 自名输出件对账 ＋ 卷二十符号核独立复核 · 2026-10-19")
    P(u"")
    P(u"问题两句：全仓有多少脚本**自己在源码里印出了它该产出的文件名**而那些文件不在盘上；"
      u"其中唯一的成系列缺席者（S14 卷二十）里，那张声称给出「阈值宗量系数 a 的【推导】」的引擎，"
      u"它的符号核到底对不对。")
    P(u"")
    P(u"## §1 对账（`%s` 与 `%s` 的三张尺里，只有文件名存在性判得动）" % (
        u"三类 glob 并集", u"全仓文件名索引"))
    P(u"")
    P(u"并集 %d 枚 .py（解析失败 %d 枚：%s）；全仓文件名索引 %d 个不同名／%d 个文件。" % (
        d0["glob_union"], d0["parse_fail"], u"、".join(u"`%s`" % x[0] for x in d0["parse_fail_sample"]),
        d0["name_index_unique"], d0["name_index_total"]))
    P(u"「自名输出件」候选＝源码里印了以自身文件名为前缀的 `.txt/.json/.md/.csv` 件名者：%d 枚；"
      u"其中至少一件在盘上 %d 枚，**全件缺席 %d 枚**：%s。" % (
        d0["self_naming_candidates"], d0["candidates_with_artifact"],
        d0["candidates_all_absent"], u"；".join(u"`%s`" % a for a in absent_paths)))
    P(u"缺席两枚声明的件名（盘上 0 命中）：%s。" % u"／".join(
        u"`%s`" % n for lst in d0["absent_declared"].values() for n in lst))
    P(u"同系列分档（`%s` %d 件里按卷号点名）：%s ⇒ **相邻卷都有产物，唯独卷二十 0 件**。" % (
        u"09_验证结果/原始运行记录", n14, u"、".join(u"%s %d 件" % (k, v)
                                                    for k, v in sorted(series_count.items()))))
    P(u"这里只能判「盘上不存在」，不能判「从未运行」——后者要另立债（§5）。")
    P(u"")
    P(u"## §2 那台引擎的形状：会动盘，但从不点火")
    P(u"")
    es = face["engine"]["shape"]
    eff = u"、".join(u"第 %d 行 `%s`" % (ln, src) for ln, src in es["top_effect_lines"])
    P(u"`%s` %d B／md5 `%s`（CRLF %d，共 %d 行）。顶层的调用语句只有 %d 条：%s。" % (
        rel(ENG20), face["engine"]["bytes"], face["engine"]["md5"], face["engine"]["crlf"],
        es["lines"], len(es["top_effect_lines"]), eff))
    P(u"其余顶层是声明：%s；自有函数 %d 个（`%s`）、类 %d 个（`%s`），"
      u"`if __name__` 守卫＝%s，文件最后一条顶层语句是 `%s`（第 %d 行）⇒ **没有调用者**。" % (
        u"、".join(u"%s %d" % (k, es["kinds"][k]) for k in sorted(es["kinds"])),
        es["own_defs"], u"`、`".join(es["own_functions"]), es["own_classes"],
        u"`、`".join(es["class_names"]), es["guard"], es["last_stmt"], es["last_lineno"]))
    P(u"它声明的输出件路径在顶层赋好：%s，写它们要靠 `_emit`/`verdict`，而这两个在顶层从不被调用 "
      u"⇒ 跑它 = 建目录 ＋ 零字节报告。" % u"／".join(
          u"`%s`（第 %d 行）" % (n, ln) for n, ln in es["out_assign_lines"]))
    P(u"本册不跑真源：逐字节副本 `%s`（md5 与源同＝%s）放进沙箱后 import，"
      u"前后 `原始运行记录` 目录差集 %d 件（X4）。" % (
        face["engine"]["sandbox"], face["engine"]["sandbox_same"],
        len(face["governance"]["s14_dir_changed"])))
    P(u"")
    P(u"## §3 三路并列：符号核对通过，引擎自己的蛮力核对不通过")
    P(u"")
    P(u"第三路线是本册自写的显式 Christoffel／Riemann（`∂_D Γ^ρ_{μν}` 存全轴，"
      u"不是引擎里 `dginv[..., lam, lam, sg]` 那种把求导轴与上指标绑成一档的写法）。")
    P(u"先用正对照验刀（X5）：`eps=0` 时逐点 R₀ 实测 min/max/mean＝%.10g／%.10g／%.10g，"
      u"期望 d(d−1)＝6 到 %g 以内；平坦背景 R₀ mean＝%.3e ⇒ 刀可用。" % (
        face["blade"]["sphere_R0_min"], face["blade"]["sphere_R0_max"], rmean,
        face["blade"]["tol"], fmean))
    P(u"")
    P(u"| d | R₀ 逐点均值 | S₂ 符号 L2 | S₂ 第三路线 | S₂ 引擎 brute | 符号↔第三路 相对差 | "
      u"引擎↔第三路 相对差 | 引擎/第三路 比值 | L2 二次项 |")
    P(u"|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        P(u"| %d | %.6g | %.8g | %.8g | %.8g | %.3e | %.3e | %.4f | %d |" % (
            r["d"], r["R0_pointwise"], r["S2_symbolic"], r["S2_third_route"], r["S2_engine_brute"],
            r["rel_sym_vs_third"], r["rel_engine_vs_third"], r["ratio_engine_over_third"],
            r["terms_L2"]))
    P(u"")
    P(u"读法：**符号 L2 与第三路线在三档 d 上全部一致**（最大相对差 %.3e < %g，X6 绿）；"
      u"**引擎自己的 `brute_action` 三档全部落在符合容差之外**（X7 绿＝判据通过，"
      u"而它断言的「不符」发生在别人的实现里）。" % (
        max(r["rel_sym_vs_third"] for r in rows), face["tol_agree"]))
    n_flip = sum(1 for r in rows if r["S2_engine_brute"] * r["S2_third_route"] < 0)
    half = abs(rows[0]["ratio_engine_over_third"] - 0.5) < 1e-9
    P(u"分型可给（按引擎/第三路 比值）：%s ⇒ 不是「实现间离散」，是两条路里有一条错，"
      u"而错的那条是数值蛮力：第一档（d=%d）的比值与 1/2 %s（%.6f 对 0.5），"
      u"三档里反号者 %d 档。" % (
        u"、".join(u"d%d→%.4f" % (r["d"], r["ratio_engine_over_third"]) for r in rows),
        rows[0]["d"], u"逐字相等" if half else u"不相等（只报读数）",
        rows[0]["ratio_engine_over_third"], n_flip))
    P(u"归属：`brute_action` 住在 S14 的文件里（第 %d–%d 行），本册不代改；"
      u"本轮把它做成一条**点名判据**，坐标与三档读数都留在本卷与面上。" % (
        es["fn_span"].get("brute_action", (0, 0))[0], es["fn_span"].get("brute_action", (0, 0))[1]))
    P(u"")
    P(u"## §4 背景条件（引擎 docstring 承诺的第二件事）")
    P(u"")
    P(u"线性项 L1 的项数随 d 为 %s；把 Λ 取成 d(d−1)/2（圆球是 Einstein 背景的那个值）后代入，"
      u"非零项数为 %s ⇒ **Λ 单独消不掉线性项**：L1 里留着 `∂·h`、`tr h` 那些块，"
      u"背景条件要在横向无迹约束上判，不是在一个 Λ 值上判。" % (
        u"、".join(u"d%d:%d" % (e["d"], e["L1_terms"]) for e in ecc),
        u"、".join(u"d%d:%d" % (e["d"], e["terms_after_Lambda"]) for e in ecc)))
    P(u"抽样残项（每档第一枚，Λ 已代入）：%s。" % u"；".join(
        u"d%d 原子 (fid=%d, dv=%s) 系数 `%s…`" % (
            e["d"], e["sample"][0][0][0], str(e["sample"][0][0][1]), e["sample"][0][1])
        for e in ecc if e["sample"]))
    P(u"本册**不**据此声称「阈值宗量系数 a 已推出」：那一格要么由 TT 约束重算，要么留在债里（§5）。")
    P(u"")
    P(u"## §5 控制与债")
    P(u"")
    for c, dsc, o in F:
        P(u"- %s `%s`：%s" % (u"绿" if o else u"红", c, dsc))
    P(u"")
    P(u"未偿债（本册立，不在本册还）：")
    P(u"- I 「盘上不存在」≠「从未运行」：归档目录可能被清过，需要 mtime 链条或第二来源才判得动。")
    P(u"- J 卷二十另一枚（管线／规范鬼雅可比）同型缺席，本册只把 Hessian 那张点火并核了符号侧。")
    P(u"- K TT（横向无迹）约束下的 L1 归零与「阈值宗量系数 a」的闭合，仍需一版带约束的重算。")
    P(u"- L `brute_action` 的缺陷属 S14 文件，本册不代改；谁来修、修完由谁复跑，是治理侧的一句话。")
    P(u"- M 两把坏尺（v2／v3）留在面上 `discarded_rulers` 里，防止下一轮把它们当结论引用。")
    P(u"")
    P(u"WITNESS_LINE：面 `%s` 由驱动器写出后复量；本卷的产物钉行由收口册从盘上找回再量盘像。" % (
        NAME + u".json"))
    return u"\r\n".join(L) + u"\r\n"


def main():
    argv = sys.argv[1:]
    mut = None
    land = False
    for a in argv:
        if a.startswith(u"--mutant="):
            mut = a.split(u"=", 1)[1]
        elif a == u"--land":
            land = True
        elif a not in (u"--check",):
            raise Fatal(u"未知开关 %s" % a)
    face, F, rows, ecc, absent_paths, pop, series_count, n14, rmean, fmean, elapsed, m = run(
        mut=mut, land=land)
    if mut:
        print(u"控制 %d/%d 点火，rc=1 收尾（变异体必须留红）" % (
            face["controls_fired"], face["controls_total"]))
        sys.stdout.flush()
        return 1
    print(u"控制 %d/%d 点火、红 %s、mode=%s、耗时 %.2f s" % (
        face["controls_fired"], face["controls_total"], face["controls_red"],
        face["mode"], elapsed))
    for c, dsc, o in F:
        print(u"  %s %s: %s" % (u"绿" if o else u"红", c, dsc))
    sys.stdout.flush()
    if not land:
        print(u"--check 模式：零写入")
        return 0
    if face["controls_red"]:
        raise Fatal(u"落库前必须全绿，现红 %s" % face["controls_red"])
    instr_p = os.path.join(PROJ, u"源码", NAME + u".py")
    face_p = os.path.join(PROJ, u"数据", NAME + u".json")
    vol_p = os.path.join(PROJ, u"判定_" + NAME + u".md")
    src_p = os.path.join(SCR, NAME + u".py")
    body = volume(face, F, rows, ecc, absent_paths, pop, series_count, n14, rmean, fmean, elapsed)
    fb = json.dumps(face, ensure_ascii=False, indent=1).replace("\n", "\r\n").encode("utf-8")
    vb = body.encode("utf-8")
    ib = open(src_p, "rb").read()
    for p, b in ((instr_p, ib), (face_p, fb), (vol_p, vb)):
        if os.path.exists(p):
            raise Fatal(u"产物已存在，不覆盖：%s" % p)
        dd = os.path.dirname(p)
        if not os.path.isdir(dd):
            os.makedirs(dd)
        open(p, "wb").write(b)
    if open(instr_p, "rb").read().replace(b"\r\n", b"\n") != ib.replace(b"\r\n", b"\n"):
        raise Fatal(u"W1 落盘图≠scratch 源")
    print(u"落库三件：%s / %s / %s" % (rel(instr_p), rel(face_p), rel(vol_p)))
    for p in (instr_p, face_p, vol_p):
        print(u"  %-70s %6d B md5 %s" % (rel(p), img(p)["bytes"], img(p)["md5"]))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Fatal as e:
        print(u"FATAL: %s" % e)
        sys.exit(1)
