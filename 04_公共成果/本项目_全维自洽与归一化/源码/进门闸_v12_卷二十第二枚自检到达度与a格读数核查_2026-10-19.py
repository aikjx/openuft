# -*- coding: utf-8 -*-
"""进门闸 v12 · 卷二十第二枚的「自检到达度」＋「阈值宗量系数 a」格读数核查 · 2026-10-19

上一轮（v11／r78）判的是「自名输出件在不在盘上」，留下债 J：
  卷二十另一枚 `tuft_卷二十_二阶变分管线与规范鬼雅可比.py` 同型缺席，未点火。
本册还这笔债，并且把「缺席」升级成三条可判的事：

  (1) 到达度：它 docstring 承诺「用五个独立自检把管线钉死」（A~E），源码里有 17 个
      `verdict(...)` 调用点。本册把逐字节副本放进沙箱真跑一次，现读它到底执行了几个
      verdict —— 分母由 AST 数出，不由本册打字。
  (2) 归属：如果它跑不完，是「数学错」还是「管线错」？本册自带两把尺子分开这两件事：
      符号侧用 sympy 按定义推出一般 d 的共形平坦 R，与它【自己印在卷面上的解析式】比；
      数值侧本册自写全轴收缩的 Christoffel/Ricci，与同一式比，并与它的 `scalar_curvature`
      在同一张网格上并列。混叠地板一并印出：粗网格上连本册自己的残差都是 O(1)，
      所以归属只能走「他们 vs 本册同格」，不能走「他们 vs 解析」。
  (3) a 格：它对「阈值宗量系数 a」到底有没有读数？窄口径（同一行里既点名 a 又给它赋数值）
      与宽口径（提到即算）各数一遍，口径写进面里；再看承载 a 的那个 payload 键有没有落盘。

另加一条第二来源（还债 I 的一半）：S14 的 `__pycache__` 现读——被 import 过会留 .pyc，
而直接 `python file.py` 运行【不】落 .pyc，所以「没有 pyc」只否证「被 import 过」这一条。

纪律：不跑真源（它顶层 `os.makedirs(ROOT/09_验证结果/原始运行记录)` 是别人的归档目录）；
     不动他人文件；未跑 refresh_catalog.py；`--check` 零写入。
红线：数学自洽 != 实验证实。
"""
import ast
import hashlib
import io
import json
import os
import re
import shutil
import sys
import time
import traceback

import numpy as np
import sympy as sp

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

ROOT = r"D:\a10\aikjx\code\my_lib\openuft"
SCR = r"D:\a10\aikjx\code\my_lib\scratch"
PROJ = os.path.join(ROOT, u"04_公共成果", u"本项目_全维自洽与归一化")
NAME = u"进门闸_v12_卷二十第二枚自检到达度与a格读数核查_2026-10-19"
V11 = u"进门闸_v11_自名输出件对账与卷二十符号核独立复核_2026-10-19"
S14 = os.path.join(ROOT, u"01_独立体系", u"S14_挠率统一场论TUFT")
RAW14 = os.path.join(S14, u"09_验证结果", u"原始运行记录")
SRC_DIR = os.path.join(S14, u"07_计算复现", u"源码")
PYC_DIR = os.path.join(SRC_DIR, "__pycache__")
ENGB = os.path.join(SRC_DIR, u"tuft_卷二十_二阶变分管线与规范鬼雅可比.py")
ENGA = os.path.join(SRC_DIR, u"tuft_卷二十_Hessian二阶变分机器求导.py")
SB = os.path.join(SCR, "v12_sandbox")
SB_DIR = os.path.join(SB, "S14x", u"07_计算复现", u"源码")
SB_ENG = os.path.join(SB_DIR, os.path.basename(ENGB))
SB_RAW = os.path.join(SB, "S14x", u"09_验证结果", u"原始运行记录")
CATALOG = os.path.join(ROOT, u"00_项目治理", u"资料索引", "material_catalog.md")
V11_FACE = os.path.join(PROJ, u"数据", V11 + u".json")
STEM_B = os.path.splitext(os.path.basename(ENGB))[0]

TOL_FINE = 1e-08        # 本册数值路线 vs 解析式（细网格）应达到的量级
COARSE = [8, 4]         # 只用来印混叠地板，不参与归属
A_NARROW = re.compile(u"宗量系数\\s*a[\\s\\S]{0,40}?a\\s*=\\s*[-+]?[\\d.]+")
A_MENTION = re.compile(u"阈值宗量系数\\s*a")


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


def mt(p):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(os.path.getmtime(p)))


class Cap(object):
    """替 engine 的 print 兜住 stdout，并接住它的 sys.stdout.reconfigure(...)。"""

    def __init__(self):
        self.parts = []

    def write(self, s):
        self.parts.append(s)
        return len(s)

    def flush(self):
        pass

    def reconfigure(self, **kw):
        return None

    def isatty(self):
        return False


# ---------------------------------------------------------------- AST 分母
def shape_of(path):
    src = txt(path)
    tree = ast.parse(src)
    codes = []
    for nd in ast.walk(tree):
        if isinstance(nd, ast.Call) and isinstance(nd.func, ast.Name) \
                and nd.func.id == "verdict" and nd.args:
            first = nd.args[0]
            if isinstance(first, ast.Str):
                codes.append(first.s)
    spans = {}
    for nd in tree.body:
        if isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef)):
            spans[nd.name] = [nd.lineno, nd.end_lineno]
    doc = ast.get_docstring(tree) or ""
    letters = []
    for m in re.finditer(u"自检\\s+([A-Z])", doc):
        if m.group(1) not in letters:
            letters.append(m.group(1))
    kinds = {}
    top_effect = []
    defect_lines = []
    for nd in ast.walk(tree):
        kinds[type(nd).__name__] = kinds.get(type(nd).__name__, 0) + 1
    for nd in tree.body:
        if isinstance(nd, ast.Expr):
            top_effect.append([nd.lineno, ast.dump(nd.value)[:64]])
    # 缺陷候选：np.sum(dGam[...]..., axis=...) —— 求导轴与被求和轴一起塌
    for nd in ast.walk(tree):
        if isinstance(nd, ast.Call):
            fn = nd.func
            fname = fn.attr if isinstance(fn, ast.Attribute) else \
                (fn.id if isinstance(fn, ast.Name) else "")
            if fname != "sum" or not nd.args:
                continue
            a0 = nd.args[0]
            if not (isinstance(a0, ast.Subscript) and isinstance(a0.value, ast.Name)
                    and a0.value.id == "dGam"):
                continue
            if any(kw.arg == "axis" for kw in nd.keywords):
                defect_lines.append(nd.lineno)
    own_defs = sorted([k for k in spans])
    out_assign = []
    for nd in tree.body:
        if isinstance(nd, ast.Assign):
            for t in nd.targets:
                if isinstance(t, ast.Name) and t.id in ("OUTDIR", "REPORT_PATH", "JSON_PATH"):
                    out_assign.append([t.id, nd.lineno])
    return {
        "lines": src.count("\n") + (0 if src.endswith("\n") else 1),
        "codes": codes, "codes_unique": sorted(set(codes)),
        "selfcheck_letters": letters,
        "spans": spans, "kinds": kinds, "top_effect_lines": top_effect,
        "own_defs": len(own_defs), "own_functions": own_defs,
        "out_assign_lines": out_assign,
        "defect_lines": defect_lines,
        "docstring": doc,
        "sphere_note": [l for l in src.split("\n")
                        if u"独立核对" in l and u"R = +" in l],
        "a_mention_lines": [i + 1 for i, l in enumerate(src.split("\n"))
                            if A_MENTION.search(l)],
        "a_narrow_lines": [i + 1 for i, l in enumerate(src.split("\n"))
                           if A_NARROW.search(l)],
        "payload_keys": sorted({k.s for nd in ast.walk(tree) if isinstance(nd, ast.Assign)
                                for t in nd.targets if isinstance(t, ast.Name)
                                and t.id == "payload"
                                for k in (nd.value.keys if isinstance(nd.value, ast.Dict)
                                          else []) if isinstance(k, ast.Str)}),
    }


# ---------------------------------------------------------------- 真跑一次（沙箱）
def run_sandbox():
    ns = {"__name__": "__main__", "__file__": SB_ENG}
    cap = Cap()
    old = sys.stdout
    sys.stdout = cap
    t0 = time.time()
    err = None
    tb_info = None
    try:
        exec(compile(txt(SB_ENG), SB_ENG, "exec"), ns)
    except BaseException as exc:
        err = exc
        fr = traceback.extract_tb(exc.__traceback__)
        inside = [f for f in fr if os.path.abspath(f.filename) == os.path.abspath(SB_ENG)]
        last = inside[-1] if inside else None
        tb_info = {
            "type": type(exc).__name__,
            "msg": str(exc)[:200],
            "frames_total": len(fr),
            "frames_in_engine": len(inside),
            "raise_lineno": (last.lineno if last else None),
            "raise_name": (last.name if last else None),
            "in_engine": bool(last is not None),
        }
    finally:
        sys.stdout = old
    lines = list(ns.get("LINES") or [])
    items = list(ns.get("ITEMS") or [])
    counts = dict(ns.get("COUNTS") or {})
    steps = [l.strip() for l in lines if l.strip().startswith(u"步骤")]
    return {
        "crash": tb_info, "raised": err is not None,
        "elapsed_s": round(time.time() - t0, 3),
        "verdicts_executed": len(items),
        "codes_executed": [c for c, s, t in items],
        "counts_after": counts,
        "lines_emitted": len(lines),
        "steps_reached": steps,
        "stdout_chars": sum(len(x) for x in cap.parts),
        "has_scalar_curvature": callable(ns.get("scalar_curvature")),
        "ns": ns,
    }


# ---------------------------------------------------------------- 本册的独立几何路线
def fft_d(f, L):
    n = f.shape[0]
    kk = 2.0 * np.pi * np.fft.fftfreq(n, d=L / n)
    return np.real(np.fft.ifft(1j * kk * np.fft.fft(f)))


def ref_curvature(g, L):
    """全轴收缩：dGam[D,:,r,m,n] = ∂_D Γ^r_{mn}，∂_λΓ^λ_{μν} 取 D 与上指标同档的对角和。

    背景只沿 x0 变化（与靶同一族测试场），所以只有 D=0／a=0 那一档导数非零；
    本册与靶的差别只在【收缩方式】：这里对 (D, 上指标) 取对角和，靶对两者一起求和。
    """
    N = g.shape[0]
    d = g.shape[1]
    ginv = np.linalg.inv(g)
    dg = np.zeros((d, N, d, d))
    for i in range(d):
        for j in range(d):
            dg[0, :, i, j] = fft_d(g[:, i, j], L)
    Gam = np.zeros((N, d, d, d))
    for r in range(d):
        for m in range(d):
            for n in range(d):
                s = np.zeros(N)
                for sg in range(d):
                    s += ginv[:, r, sg] * (dg[m, :, n, sg] + dg[n, :, m, sg]
                                          - dg[sg, :, m, n])
                Gam[:, r, m, n] = 0.5 * s
    dGam = np.zeros((d, N, d, d, d))
    for r in range(d):
        for m in range(d):
            for n in range(d):
                dGam[0, :, r, m, n] = fft_d(Gam[:, r, m, n], L)
    Ric = np.zeros((N, d, d))
    for m in range(d):
        for n in range(d):
            t1 = np.zeros(N)
            t2 = np.zeros(N)
            t3 = np.zeros(N)
            t4 = np.zeros(N)
            for l in range(d):
                t1 += dGam[l, :, l, m, n]
                t2 += dGam[n, :, l, l, m]
                for sg in range(d):
                    t3 += Gam[:, l, l, sg] * Gam[:, sg, m, n]
                    t4 += Gam[:, sg, l, m] * Gam[:, l, sg, n]
            Ric[:, m, n] = t1 - t2 + t3 - t4
    R = np.einsum("nij,nij->n", ginv, Ric)
    return R, np.sqrt(np.abs(np.linalg.det(g)))


def conformal_case(N, kappa=1.0):
    L = 2.0 * np.pi / kappa
    x = L * np.arange(N) / N
    phi = 0.30 * np.sin(kappa * x) + 0.10 * np.cos(2.0 * kappa * x)
    d1 = fft_d(phi, L)
    d2 = fft_d(d1, L)
    R_ana = -3.0 * np.exp(-2.0 * phi) * (2.0 * d2 + 2.0 * d1 * d1)   # d=4：-(d-1)[2φ''+(d-2)φ'²]
    g = np.zeros((N, 4, 4))
    e2 = np.exp(2.0 * phi)
    for i in range(4):
        g[:, i, i] = e2
    return L, phi, R_ana, g


def rel_err(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    den = max(1.0, float(np.max(np.abs(b))))
    return float(np.max(np.abs(a - b))) / den


# ---------------------------------------------------------------- sympy：一般 d 的恒等式
def sym_R(d, t1_kind="ok"):
    xs = [sp.Symbol("x%d" % i) for i in range(d)]
    x0 = xs[0]
    phi = sp.Function("phi")(x0)
    e2 = sp.exp(2 * phi)
    d1 = sp.diff(phi, x0)
    d2 = sp.diff(phi, x0, 2)

    def g(i, j):
        return e2 if i == j else sp.S.Zero

    def dg(a, i, j):
        return sp.diff(g(i, j), xs[a])

    def gi(r, sg):
        return sp.exp(-2 * phi) if r == sg else sp.S.Zero

    Gam = {}
    for r in range(d):
        for m in range(d):
            for n in range(d):
                s = sp.S.Zero
                for sg in range(d):
                    s += gi(r, sg) * (dg(m, n, sg) + dg(n, m, sg) - dg(sg, m, n))
                Gam[(r, m, n)] = sp.simplify(s / 2)
    Ric = {}
    for m in range(d):
        for n in range(d):
            if t1_kind == "ok":
                t1 = sum(sp.diff(Gam[(l, m, n)], xs[l]) for l in range(d))
            else:
                t1 = sum(sp.diff(Gam[(l, l, n)], xs[m]) for l in range(d))
            t2 = sum(sp.diff(Gam[(l, l, m)], xs[n]) for l in range(d))
            t3 = sum(Gam[(l, l, sg)] * Gam[(sg, m, n)]
                     for l in range(d) for sg in range(d))
            t4 = sum(Gam[(sg, l, m)] * Gam[(l, sg, n)]
                     for l in range(d) for sg in range(d))
            Ric[(m, n)] = sp.simplify(t1 - t2 + t3 - t4)
    R = sp.S.Zero
    for m in range(d):
        for n in range(d):
            R = R + gi(m, n) * Ric[(m, n)]
    return x0, d1, d2, sp.simplify(R)


def sym_sphere_R(d):
    """共形因子 Ω = 2/(1+r²)（球面投影，全坐标依赖，不是只依赖 x0）。"""
    xs = [sp.Symbol("x%d" % i) for i in range(d)]
    r2 = sum(x * x for x in xs)
    Om = 2 / (1 + r2)
    g = [[sp.simplify(Om ** 2) if i == j else sp.S.Zero for j in range(d)]
         for i in range(d)]
    ginv = sp.Matrix(g).inv()
    dg = {(a, i, j): sp.diff(g[i][j], xs[a]) for a in range(d)
          for i in range(d) for j in range(d)}
    Gam = {}
    for r in range(d):
        for m in range(d):
            for n in range(d):
                s = sp.S.Zero
                for sg in range(d):
                    s += ginv[r, sg] * (dg[(m, n, sg)] + dg[(n, m, sg)] - dg[(sg, m, n)])
                Gam[(r, m, n)] = sp.simplify(s / 2)
    Ric = {}
    for m in range(d):
        for n in range(d):
            t1 = sum(sp.diff(Gam[(l, m, n)], xs[l]) for l in range(d))
            t2 = sum(sp.diff(Gam[(l, l, m)], xs[n]) for l in range(d))
            t3 = sum(Gam[(l, l, sg)] * Gam[(sg, m, n)] for l in range(d) for sg in range(d))
            t4 = sum(Gam[(sg, l, m)] * Gam[(l, sg, n)] for l in range(d) for sg in range(d))
            Ric[(m, n)] = sp.simplify(t1 - t2 + t3 - t4)
    R = sp.S.Zero
    for m in range(d):
        for n in range(d):
            R = R + ginv[m, n] * Ric[(m, n)]
    return sp.simplify(sp.expand(R))


# ---------------------------------------------------------------- 编译痕迹 / a 格 / 引用普查
def pyc_readings():
    names = {}
    if os.path.isdir(PYC_DIR):
        for f in os.listdir(PYC_DIR):
            names[f] = os.path.join(PYC_DIR, f)
    out = {"dir_exists": os.path.isdir(PYC_DIR), "files": len(names), "engines": {}}
    for tag, p in ((u"管线(本册靶)", ENGB), (u"Hessian(v11 靶)", ENGA)):
        stem = os.path.splitext(os.path.basename(p))[0]
        hit = [n for n in names if n.startswith(stem + u".")]
        out["engines"][tag] = {
            "pyc": hit,
            "pyc_mtime": [mt(names[h]) for h in hit],
            "src_mtime": (mt(p) if os.path.isfile(p) else None),
            "artifacts_on_disk": [f for f in os.listdir(RAW14)
                                  if stem in f] if os.path.isdir(RAW14) else [],
        }
    return out


def a_scope_readings():
    scopes = {}
    for tag, path in ((u"engine_source", ENGB), (u"engine_sibling", ENGA)):
        ls = txt(path).split("\n")
        scopes[tag] = {
            "mention_lines": [i + 1 for i, l in enumerate(ls) if A_MENTION.search(l)],
            "narrow_lines": [i + 1 for i, l in enumerate(ls) if A_NARROW.search(l)],
        }
    docs = []
    for dirpath, dirnames, filenames in os.walk(S14):
        dirnames[:] = [x for x in dirnames if x not in (".git", "__pycache__")]
        for fn in filenames:
            if not fn.endswith((".md", ".py", ".txt", ".json")):
                continue
            p = os.path.join(dirpath, fn)
            try:
                s = open(p, "rb").read().decode("utf-8")
            except Exception:
                continue
            if u"阈值宗量系数" in s:
                ls = s.split("\n")
                docs.append({
                    "path": rel(p),
                    "mention": sum(1 for l in ls if u"阈值宗量系数" in l),
                    "mention_a": sum(1 for l in ls if A_MENTION.search(l)),
                    "narrow": [i + 1 for i, l in enumerate(ls) if A_NARROW.search(l)],
                })
    v20 = []
    for dirpath, dirnames, filenames in os.walk(S14):
        dirnames[:] = [x for x in dirnames if x not in (".git", "__pycache__")]
        for fn in filenames:
            if not fn.endswith((".md", ".txt")):
                continue
            p = os.path.join(dirpath, fn)
            try:
                s = open(p, "rb").read().decode("utf-8")
            except Exception:
                continue
            hits = sorted(set(re.findall(r"V20-[A-Z]\d", s)))
            if hits:
                v20.append({"path": rel(p), "codes": hits})
    return {"scopes": scopes, "corpus_files": docs,
            "corpus_narrow_total": sum(len(x["narrow"]) for x in docs),
            "corpus_mention_a_total": sum(x["mention_a"] for x in docs),
            "v20_citations": v20}


def mut_desc(m):
    return {
        u"m1": u"到达度按 docstring 承诺记满（把「它说要五个自检」当「它跑了五个」）",
        u"m2": u"在 N=4 粗格上比「引擎 vs 解析式」，拿混叠地板当缺陷归属",
        u"m3": u"用塌轴收缩（∂_μΓ^λ_{λν}）当参考式去核对解析预言",
        u"m4": u"维数错档：拿 3-球（R=6）去坐实卷面那句「单位 4-球 R=+12」",
        u"m5": u"宽口径：把「任何提到 a 的行」当 a 的数值读数",
        u"m6": u"判决之后移动本册自己的输入图像（只读复量失效）",
        u"m7": u"抄隔壁期望：要求两台的 pyc 状态同构（有都有、无都无），否则判仪器坏",
        u"m8": u"期望沙箱归档里已有该引擎的两件报告（把它当跑完了的）",
        u"m9": u"沙箱副本等字节换图（只比字节数的宽尺判不出）",
    }[m]


# ---------------------------------------------------------------- 主判据
def run(mut=None, land=False):
    t0 = time.time()
    F = []
    START = t0

    def C(code, desc, ok):
        F.append((code, desc, bool(ok)))
        return bool(ok)

    def red_now():
        return [c for c, dsc, o in F if not o]

    if os.path.isfile(SB_ENG) and open(SB_ENG, "rb").read() != open(ENGB, "rb").read():
        raise Fatal(u"沙箱副本与源不符（源已漂移或上一轮没还原）")
    if not os.path.isdir(SB_DIR):
        os.makedirs(SB_DIR)
    if not os.path.isfile(SB_ENG):
        shutil.copyfile(ENGB, SB_ENG)

    cat_md5_pre = img(CATALOG)["md5"]
    raw_pre = set(os.listdir(RAW14)) if os.path.isdir(RAW14) else set()
    sb_raw_pre_existed = os.path.isdir(SB_RAW)
    sb_raw_pre_n = len(os.listdir(SB_RAW)) if sb_raw_pre_existed else None
    sh = shape_of(ENGB)
    py = pyc_readings()
    aS = a_scope_readings()

    inputs = [ENGB, ENGA, CATALOG, V11_FACE, SB_ENG]
    for e in py["engines"].values():
        for h in e["pyc"]:
            inputs.append(os.path.join(PYC_DIR, h))
    snap = {p: img(p)["md5"] for p in sorted(set(inputs)) if os.path.isfile(p)}

    res = run_sandbox()
    ns = res.pop("ns")

    # ---- X1 沙箱纪律／零写入
    raw_post = set(os.listdir(RAW14)) if os.path.isdir(RAW14) else set()
    delta = sorted(raw_pre ^ raw_post)
    cat_md5_post = img(CATALOG)["md5"]
    same_img = img(SB_ENG)["md5"] == img(ENGB)["md5"]
    C(u"X1", u"沙箱纪律：副本 md5 逐字节＝源（%s）；真源归档目录 %d 件、前后差集 %d 件；"
      u"资料索引 md5 未动（%s→%s）；本册从不 import 真源"
      % (img(ENGB)["md5"][:8], len(raw_pre), len(delta),
         cat_md5_pre[:8], cat_md5_post[:8]),
      same_img and not delta and cat_md5_pre == cat_md5_post)

    # ---- X2 编译痕迹（第二来源），且限制句成立
    engB = py["engines"][u"管线(本册靶)"]
    engA = py["engines"][u"Hessian(v11 靶)"]
    pycB_absent = len(engB["pyc"]) == 0
    pycA_present_before = (len(engA["pyc"]) == 1
                           and os.path.getmtime(os.path.join(PYC_DIR, engA["pyc"][0])) < START)
    C(u"X2", u"编译痕迹现读：管线这台在 `__pycache__` 里 %s（%d 枚 pyc），Hessian 那台有 1 枚 "
      u"pyc（%s，早于本册启动 %s）⇒ 只能判「未被 import 过」；直接 `python file.py` 运行不落 "
      u"pyc，故本册不据此断言「从未运行」"
      % (u"没有 pyc" if pycB_absent else u"有 pyc " + str(engB["pyc"]),
         len(engB["pyc"]), engA["pyc_mtime"][0] if engA["pyc_mtime"] else u"-",
         pycA_present_before),
      pycB_absent and pycA_present_before and len(engB["artifacts_on_disk"]) == 0)

    # ---- X3 到达度：分母由 AST 现数
    n_codes = len(sh["codes"])
    n_letters = len(sh["selfcheck_letters"])
    reached = res["verdicts_executed"]
    C(u"X3", u"自检到达度 %d／%d：AST 数出 `verdict` 调用点 %d 枚、docstring 承诺自检 %d 条 "
      u"(%s)；沙箱真跑 %s s 后执行到 %d 枚、卷面只走到 %s ⇒ 五条自检一条也没算完，"
      u"H2 里「(a) 管线经逐点校验（V20-A1）」这类句子是被引用不存在的记录"
      % (reached, n_codes, n_codes, n_letters, u"、".join(sh["selfcheck_letters"]),
         res["elapsed_s"], reached, u"／".join(res["steps_reached"])),
      n_codes > 0 and n_letters == 5 and reached == 0 and res["raised"])

    # ---- X4 数值归属（同一条路上，「他们 vs 本册」而不是「他们 vs 解析」）
    fine = []
    for N in (192, 96):
        L, phi, R_ana, g = conformal_case(N)
        R_ref, _ = ref_curvature(g, L)
        fine.append({"N": N, "kind": u"本册全轴 vs 引擎所印解析式",
                     "rel": rel_err(R_ref, R_ana)})
    crash_fine = []
    for N in (192, 96):
        L, phi, R_ana, g = conformal_case(N)
        try:
            ns["scalar_curvature"](g, L)
            crash_fine.append({"N": N, "raised": None})
        except BaseException as exc:
            crash_fine.append({"N": N, "raised": type(exc).__name__,
                               "msg": str(exc)[:120]})
    coarse = []
    for N in COARSE:
        L, phi, R_ana, g = conformal_case(N)
        R_ref, _ = ref_curvature(g, L)
        try:
            R_them, _ = ns["scalar_curvature"](g, L)
            them = {"raised": None, "shape": list(np.shape(R_them)),
                    "rel": rel_err(R_them, R_ana)}
        except BaseException as exc:
            them = {"raised": type(exc).__name__, "shape": None, "rel": None}
        coarse.append({"N": N, "mine_rel": rel_err(R_ref, R_ana), "theirs": them})
    theirs4 = [c for c in coarse if c["N"] == 4]
    floor_ok = all(c["mine_rel"] > TOL_FINE for c in coarse)
    C(u"X4", u"数值归属：本册全轴路线与引擎【自己印的】解析式在 N=192/96 上相对残差 %s／%s；"
      u"同一张网格上引擎的 `scalar_curvature` 抛 %s ⇒ 缺陷在这台管线里，不在它印的公式里。"
      u"混叠地板一并印出：N=8/4 上本册自己也是 %s／%s（O(1)），所以归属不许走粗格"
      % ("%.3e" % fine[0]["rel"], "%.3e" % fine[1]["rel"],
         u"、".join(str(c["raised"]) for c in crash_fine),
         "%.3e" % coarse[0]["mine_rel"], "%.3e" % coarse[1]["mine_rel"]),
      fine[0]["rel"] < TOL_FINE and fine[1]["rel"] < TOL_FINE
      and all(c["raised"] for c in crash_fine)
      and theirs4[0]["theirs"]["raised"] is None
      and theirs4[0]["theirs"]["shape"] == [4]
      and floor_ok)

    # ---- X5 sympy 一般 d 恒等式（带两枚夹具＝牙齿）
    idm = []
    for d in range(2, 7):
        x0, d1, d2, R_ok = sym_R(d, "ok")
        _, _, _, R_dw = sym_R(d, "collapse")
        phi = sp.Function("phi")(x0)
        pred = sp.simplify(-(d - 1) * sp.exp(-2 * phi) * (2 * d2 + (d - 2) * d1 ** 2))
        pred_bad = sp.simplify(-(d - 1) * sp.exp(-2 * phi) * (2 * d2 + (d + 3) * d1 ** 2))
        idm.append({"d": d,
                    "resid_correct_vs_pred": sp.simplify(R_ok - pred) == 0,
                    "coeff_fixture_nonzero": sp.simplify(R_ok - pred_bad) != 0,
                    "collapse_fixture_nonzero": sp.simplify(R_dw - pred) != 0,
                    "collapse_equals_pred": sp.simplify(R_dw - pred) == 0,
                    "R_ok": str(R_ok)})
    all_ok = (all(x["resid_correct_vs_pred"] for x in idm)
              and all(x["coeff_fixture_nonzero"] for x in idm)
              and all(x["collapse_fixture_nonzero"] for x in idm))
    C(u"X5", u"符号侧：按定义（Christoffel→Ricci→g^{μν}）推一般 d 的共形平坦 R，"
      u"与它卷面那个通式在 d=2..6 上残差恒为 0（%s 档全对）；两枚夹具——系数改一档、"
      u"把导数轴绑到下指标——在同样五档上残差全非零 ⇒ 这条恒等式是真约束不是同义反复"
      % sum(1 for x in idm if x["resid_correct_vs_pred"]), all_ok)

    # ---- X6 它卷面自称的第二把刀：单位 4-球 R = +12 = d(d-1)
    note_txt = (sh["sphere_note"][0] if sh["sphere_note"] else u"")
    m_num = re.search(r"R = \+(\d+)", note_txt)
    m_dim = re.search(r"单位\s*(\d)-球", note_txt)
    claimed = int(m_num.group(1)) if m_num else None
    cl_d = int(m_dim.group(1)) if m_dim else None
    R_sp = sym_sphere_R(cl_d or 4)
    dd1 = (cl_d or 4) * ((cl_d or 4) - 1)
    C(u"X6", u"它印在卷面的正对照由本册独立算成：Ω=2/(1+r²) 的共形度规在 d=%s 上 sympy 给出 "
      u"R = %s（化简后），卷面声称 + %s ＝ d(d−1) = %s；平坦背景 R = 0 已在 X5 的 φ≡const "
      u"极限里覆盖 ⇒ 那句话本身是真的，只是它的执行体跑不到那一步"
      % (cl_d, R_sp, claimed, dd1),
      claimed is not None and str(R_sp) == str(claimed) and claimed == dd1)

    # ---- X7 「阈值宗量系数 a」格：窄口径 vs 宽口径 ＋ 承载键
    men = aS["scopes"]["engine_source"]["mention_lines"]
    nar = aS["scopes"]["engine_source"]["narrow_lines"]
    wide_corpus = sum(x["mention"] for x in aS["corpus_files"])
    narrow_corpus = aS["corpus_narrow_total"]
    a_corpus = aS["corpus_mention_a_total"]
    a_key_written = [k for k in sh["payload_keys"] if u"hessian_reduced" in k]
    json_exists = os.path.isfile(os.path.join(RAW14, STEM_B + u".json"))
    C(u"X7", u"a 格读数＝0：口径写死——「窄」＝同一行既点名『阈值宗量系数 a』又写成 `a = <数>`"
      u"（本引擎按 A 尺提及 %s 行、窄口径 %d 行；S14 全库按宽尺提及 %d 行／按 A 尺 %d 行、"
      u"窄口径 %d 行）；"
      u"承载 a 的 payload 键 %s 随 JSON 一起从未落盘（盘上 %s）⇒ a 至今是一格【承诺】，"
      u"不是一格【读数】" % (men, len(nar), wide_corpus, a_corpus, narrow_corpus,
                             u"、".join(a_key_written) or u"（无）",
                             u"无此件" if not json_exists else u"有件"),
      len(nar) == 0 and narrow_corpus == 0 and len(men) >= 1 and not json_exists)

    # ---- X8 副作用落点：目录建了、报告没写
    sb_raw_post_existed = os.path.isdir(SB_RAW)
    sb_raw_n = len(os.listdir(SB_RAW)) if sb_raw_post_existed else -1
    C(u"X8", u"副作用有落点：沙箱那侧 `%s` 目录存在且 0 件（跑前已存在＝%s，"
      u"跑前件数 %s（本册不判目录是谁建的——这条证据只有「0 件」那么强），跑后件数 %d ⇒ 它连自己的 "
      u"REPORT_PATH/JSON_PATH（第 %s 行赋好名）那一步都没到；真源归档目录 %d 件、差集 %d 件（本册不写）"
      % (rel(SB_RAW), sb_raw_pre_existed, sb_raw_pre_n, sb_raw_n,
         u"／".join(str(ln) for _, ln in sh["out_assign_lines"]), len(raw_pre), len(delta)),
      sb_raw_post_existed and sb_raw_n == 0)

    # ---- X9 判决之后复量输入图像
    moved = [p for p, d0 in snap.items() if img(p)["md5"] != d0]
    C(u"X9", u"判决计算后复量 %d 份输入（两台引擎、索引、上一轮面、沙箱副本、pyc），"
      u"移动 %d 份 ⇒ 本面可被下一轮只读复量" % (len(snap), len(moved)), not moved)

    # ---- 变异体
    EXPECTED_RED = {u"m1": u"X3", u"m2": u"X4", u"m3": u"X5", u"m4": u"X6",
                    u"m5": u"X7", u"m6": u"X9", u"m7": u"X2", u"m8": u"X8",
                    u"m9": u"X1"}

    def set_ctl(code, ok, tag):
        for i, (c, dsc, o) in enumerate(F):
            if c == code:
                F[i] = (c, dsc + u"（MUT=%s）" % tag, bool(ok))

    if mut:
        if mut not in EXPECTED_RED:
            raise Fatal(u"未知变异体 %s" % mut)
        tag = EXPECTED_RED[mut] + u":" + mut_desc(mut)
        if mut == u"m1":
            set_ctl(u"X3", n_codes > 0 and n_letters == 5 and n_letters == 0, tag)
        elif mut == u"m2":
            set_ctl(u"X4", theirs4[0]["theirs"]["rel"] is not None
                    and theirs4[0]["theirs"]["rel"] < TOL_FINE, tag)
        elif mut == u"m3":
            set_ctl(u"X5", all(x["collapse_equals_pred"] for x in idm), tag)
        elif mut == u"m4":
            R3 = sym_sphere_R(3)
            set_ctl(u"X6", str(R3) == str(claimed), tag)
        elif mut == u"m5":
            set_ctl(u"X7", wide_corpus == 0, tag)
        elif mut == u"m6":
            keep = open(SB_ENG, "rb").read()
            open(SB_ENG, "ab").write(b"\r\n")
            mv = [p for p, d0 in snap.items() if img(p)["md5"] != d0]
            set_ctl(u"X9", not mv, tag)
            open(SB_ENG, "wb").write(keep)
        elif mut == u"m7":
            set_ctl(u"X2", pycB_absent == (len(engA["pyc"]) == 0), tag)
        elif mut == u"m8":
            set_ctl(u"X8", sb_raw_n == 2, tag)
        elif mut == u"m9":
            keep = open(SB_ENG, "rb").read()
            alt = keep.replace(b"0.5 * s", b"0.6 * s", 1)
            if alt == keep or len(alt) != len(keep):
                raise Fatal(u"m9 夹具落不上（等字节换图失败）")
            open(SB_ENG, "wb").write(alt)
            wide = img(SB_ENG)["bytes"] == img(ENGB)["bytes"]
            narrow = img(SB_ENG)["md5"] == img(ENGB)["md5"]
            set_ctl(u"X1", narrow, tag)
            open(SB_ENG, "wb").write(keep)
            if not (wide and not narrow):
                raise Fatal(u"m9 夹具没做到「等字节不同图」（wide=%s narrow=%s）"
                            % (wide, narrow))
            print(u"m9 夹具：宽尺（只比字节数）判为同图＝%s，真尺（md5）判为异图＝%s "
                  u"⇒ X1 由 md5 那半判红" % (wide, not narrow))
        want = EXPECTED_RED[mut]
        got = red_now()
        if want not in got:
            raise Fatal(u"变异体 %s 没能打破指定控制 %s（当前红＝%s）" % (mut, want, got))
        print(u"MUT=%s（%s）：指定控制 %s 已红；连带红＝%s" % (
            mut, mut_desc(mut), want, [c for c in got if c != want]))

    crash = res["crash"]
    face = {
        "name": NAME, "mode": ("land" if land else ("mutant" if mut else "check")),
        "mutant": mut, "stamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(START)),
        "elapsed_s": round(time.time() - t0, 2),
        "target": {
            "path": rel(ENGB), "bytes": img(ENGB)["bytes"], "md5": img(ENGB)["md5"],
            "crlf": img(ENGB)["crlf"], "lines": sh["lines"], "src_mtime": mt(ENGB),
            "sandbox": rel(SB_ENG), "sandbox_same": same_img,
            "shape": {"verdict_codes": sh["codes"], "verdict_sites": n_codes,
                      "selfcheck_letters": sh["selfcheck_letters"],
                      "spans": sh["spans"], "kinds": sh["kinds"],
                      "top_effect_lines": sh["top_effect_lines"],
                      "own_defs": sh["own_defs"],
                      "out_assign_lines": sh["out_assign_lines"],
                      "defect_lines": sh["defect_lines"],
                      "payload_keys": sh["payload_keys"],
                      "sphere_note": note_txt.strip()},
        },
        "execution": {k: v for k, v in res.items()},
        "arrival": {"denominator_codes": n_codes, "denominator_letters": n_letters,
                    "reached": reached, "counts_after": res["counts_after"],
                    "steps_reached": res["steps_reached"]},
        "crash": crash,
        "numeric": {"fine": fine, "engine_calls_fine": crash_fine, "coarse": coarse,
                    "tol_fine": TOL_FINE},
        "symbolic": idm,
        "sphere_control": {"claimed": claimed, "claimed_dim": cl_d,
                           "d_times_d_minus_1": dd1, "sympy_R": str(R_sp)},
        "a_grid": {"rule_narrow": u"同一行内既含「阈值宗量系数 a」又含 `a = <数字>`",
                   "rule_wide": u"宽尺＝行内含「阈值宗量系数」四字（全库侧的「提及」用的就是它）；"
                                u"A 尺＝「阈值宗量系数」后紧跟（可空格的）a（引擎侧与逐行判定用它）",
                   "engine_mention_lines": men, "engine_narrow_lines": nar,
                   "corpus_files": aS["corpus_files"], "corpus_mention_total": wide_corpus,
                   "corpus_mention_a_total": a_corpus,
                   "corpus_narrow_total": narrow_corpus,
                   "carrier_keys": a_key_written, "json_on_disk": json_exists},
        "pycache": py,
        "v11_face": {"path": rel(V11_FACE), "md5": img(V11_FACE)["md5"],
                     "engine_md5_on_face": json.loads(txt(V11_FACE))["engine"]["md5"]},
        "read_only_sweep": {"inputs": len(snap), "moved": moved},
        "controls_total": len(F), "controls_fired": len(F) - len(red_now()),
        "controls_red": red_now(),
        "control_list": [{"code": c, "desc": dsc, "ok": o} for c, dsc, o in F],
        "governance": {"catalog_md5_pre": cat_md5_pre, "catalog_md5_post": cat_md5_post,
                       "s14_archive_delta": delta, "s14_archive_files": len(raw_pre),
                       "sb_archive": {"pre_existed": sb_raw_pre_existed,
                                      "pre_n": sb_raw_pre_n, "post_n": sb_raw_n}},
    }
    return face, F, ns


def volume(face, F):
    L = []

    def P(s):
        L.append(s)

    tg = face["target"]
    sh = tg["shape"]
    cr = face["crash"]
    P(u"# 判定 · 进门闸 v12：卷二十第二枚的自检到达度 ＋ 「阈值宗量系数 a」格读数（2026-10-19）")
    P(u"")
    P(u"对象：`%s`（%d B／md5 `%s`／CRLF %d，共 %d 行；源 mtime %s）。" % (
        tg["path"], tg["bytes"], tg["md5"], tg["crlf"], tg["lines"], tg["src_mtime"]))
    P(u"上一轮（v11／r78）只把它列为「同型缺席」的债 J；本册把它真跑进沙箱，判三件事："
      u"到达度、缺陷归属（索引错 vs 数学错）、a 格有没有读数。")
    P(u"")
    P(u"## §1 到达度 %d／%d：五条自检一条也没算完" % (
        face["arrival"]["reached"], face["arrival"]["denominator_codes"]))
    P(u"")
    P(u"分母不由本册打字：AST 数出 `verdict(...)` 调用点 **%d 枚**（%s），"
      u"docstring 承诺自检 **%d 条**（%s）。" % (
        face["arrival"]["denominator_codes"],
        u"、".join(u"`%s`" % c for c in sh["verdict_codes"]),
        face["arrival"]["denominator_letters"], u"、".join(sh["selfcheck_letters"])))
    P(u"沙箱真跑 %s s：抛 `%s`（第 %s 行，`%s`，引擎内帧 %d 层），"
      u"执行到的 verdict = **%d 枚**，计数表 %s，卷面只走到「%s」。" % (
        face["execution"]["elapsed_s"], cr["type"], cr["raise_lineno"], cr["raise_name"],
        cr["frames_in_engine"], face["arrival"]["reached"],
        json.dumps(face["arrival"]["counts_after"], ensure_ascii=False),
        u"／".join(face["arrival"]["steps_reached"])))
    P(u"所以这台引擎给不出它自己承诺的任何一条：`V20-A1`（自检 A）从未执行，"
      u"而 `V20-H2` 里那句「(a) 几何管线经共形平坦解析式逐点校验（V20-A1）」"
      u"是一条**引用不存在记录的承诺**。")
    P(u"")
    P(u"## §2 缺陷在索引收缩，不在它印的公式")
    P(u"")
    P(u"`scalar_curvature` 把 ∂_λΓ^λ_{μν} 写成了对「求导轴＋网格轴」一起求和、把上指标留在外面："
      u"候选缺陷语句在第 %s 行（AST 定位：`np.sum(dGam[...]..., axis=...)`），"
      u"报错发生在第 %s 行——两者不同行，报的是后面那次减法。" % (
        u"、".join(str(x) for x in sh["defect_lines"]), cr["raise_lineno"]))
    P(u"网格 N=192 时上指标那一档塌成形状 `(4,)`，与 `(192,)` 撞不上 ⇒ `%s`。" % cr["msg"][:60])
    P(u"")
    P(u"| N | 本册全轴 vs 它印的解析式（相对残差） | 同格上它的 `scalar_curvature` |")
    P(u"|---|---|---|")
    for f, c in zip(face["numeric"]["fine"], face["numeric"]["engine_calls_fine"]):
        P(u"| %d | %.3e | %s |" % (f["N"], f["rel"], c["raised"] or u"未抛"))
    P(u"")
    P(u"混叠地板（同一张网格、只用来说明粗格不可归因）：")
    for c in face["numeric"]["coarse"]:
        th = c["theirs"]
        P(u"- N=%d：本册残差 %.3e；它 %s%s ⇒ 粗格上两边都是 O(1)，任何「它算错了多少」的"
          u"说法在这里都不成立。" % (
              c["N"], c["mine_rel"],
              (u"返回形状 %s、相对残差 %.3e" % (th["shape"], th["rel"]))
              if th["raised"] is None else (u"抛 %s" % th["raised"]),
              u"（形状 (4,)＝上指标那一档恰好被当成网格读）" if th["shape"] == [4] else u""))
    P(u"")
    P(u"符号侧独立核对（一般 d，按定义推，不引任何文献 Hessian 公式）：")
    P(u"")
    P(u"| d | 残差(正确收缩 vs 卷面通式) | 夹具1 系数改档 | 夹具2 导数轴绑到下指标 |")
    P(u"|---|---|---|---|")
    for x in face["symbolic"]:
        P(u"| %d | %s | %s | %s |" % (
            x["d"], u"恒为 0" if x["resid_correct_vs_pred"] else u"非零",
            u"非零" if x["coeff_fixture_nonzero"] else u"（无效夹具）",
            u"非零" if x["collapse_fixture_nonzero"] else u"（无效夹具）"))
    P(u"")
    P(u"⇒ 它卷面印的 `R = -(d-1)e^{-2φ}[2∇²φ + (d-2)|∇φ|²]` **是对的**（5 档全对），"
      u"而它的实现做不到自己印的这句话：两枚夹具（系数改一档、把导数轴绑到下指标）"
      u"在同样 5 档上都非零 ⇒ 这条恒等式是真约束，不是同义反复。")
    P(u"")
    P(u"## §3 它自称的另一把刀：单位 4-球")
    P(u"")
    P(u"卷面那句：`%s`" % sh["sphere_note"])
    P(u"本册独立算：Ω = 2/(1+r²) 的共形度规在 d=%s 上 sympy 化简给 R = %s，"
      u"与声称的 +%s（= d(d−1) = %s）同值 ⇒ 这句话本身成立，只是执行体跑不到。" % (
        face["sphere_control"]["claimed_dim"], face["sphere_control"]["sympy_R"],
        face["sphere_control"]["claimed"], face["sphere_control"]["d_times_d_minus_1"]))
    P(u"")
    P(u"## §4 「阈值宗量系数 a」：一格承诺，不是一格读数")
    P(u"")
    ag = face["a_grid"]
    P(u"口径写死在面上：「窄」＝同一行内既点名『阈值宗量系数 a』又写成 `a = <数字>`；"
      u"「宽尺」＝行内含「阈值宗量系数」四字；「A 尺」＝其后紧跟（可空格的）a。"
      u"引擎侧用 A 尺，全库侧两把都印（同一句里不许住两把无名尺）。")
    P(u"本引擎按 A 尺提及行 %s，窄口径 **%d 行**；S14 全库按宽尺提及 %d 行／按 A 尺 %d 行，"
      u"窄口径 **%d 行**。" % (
        ag["engine_mention_lines"], len(ag["engine_narrow_lines"]),
        ag["corpus_mention_total"], ag["corpus_mention_a_total"],
        ag["corpus_narrow_total"]))
    P(u"承载 a 的那一格本该由 payload 键 `%s` 落盘（各 York 块的 `B_Lambda`），"
      u"而它的 JSON 在盘上%s ⇒ a 到目前为止在整个 S14 里没有数值，只有 %d 处点名。" % (
        u"、".join(ag["carrier_keys"]) or u"（无）",
        u"不存在" if not ag["json_on_disk"] else u"存在", ag["corpus_mention_total"]))
    P(u"提到它的语料文件：%s。" % u"；".join(
        u"`%s`（%d 处）" % (x["path"], x["mention"]) for x in ag["corpus_files"]))
    P(u"")
    P(u"## §5 第二来源：编译痕迹（只否证「被 import 过」）")
    P(u"")
    pc = face["pycache"]
    for tag, e in pc["engines"].items():
        P(u"- %s：`__pycache__` 里 %s；源 mtime %s；归档目录里点名它的产物 %d 件。" % (
            tag, (u"无 pyc" if not e["pyc"] else u"%s（%s）" % (
                u"、".join(e["pyc"]), u"、".join(e["pyc_mtime"]))),
            e["src_mtime"], len(e["artifacts_on_disk"])))
    P(u"限制（本册自己给自己画的线）：CPython 只在 **import** 时落 .pyc，"
      u"`python file.py` 直跑不落。所以「管线这台没有 pyc」只否证「它被 import 过」，"
      u"否不了「它从没被执行过」；债 I 剩下这一半。")
    P(u"")
    P(u"## §6 控制与债")
    P(u"")
    for c, dsc, o in F:
        P(u"- %s `%s`：%s" % (u"绿" if o else u"红", c, dsc))
    P(u"")
    P(u"未偿债（本册立，不在本册还）：")
    P(u"- N 缺陷归属已定（索引收缩），但**修它不在本册**：那台引擎属 S14 文件，本册不代改；"
      u"修完之后五条自检要由作者自己那台跑出产物，才谈得上销债 J。")
    P(u"- O 「V20-*」在语料里的引用普查只印了文件名与命中标号，没逐条判「引用者是否把它当已证」；"
      u"那是下一册的活。")
    P(u"- I 剩一半：没有 pyc ⇒ 未被 import，但脚本直跑不产 pyc，「从未运行」仍未判死。")
    P(u"- K TT（横向无迹）约束下 L1 归零与 a 的闭合仍 OPEN（本册只证明盘上没有任何 a 读数）。")
    P(u"- L 两台引擎的缺陷（Hessian 那台的 `brute_action`、管线这台的 ∂_λΓ^λ 收缩）"
      u"都在他人文件里，不代改。")
    P(u"")
    P(u"WITNESS_LINE：面 `%s` 由驱动器写出后复量；本卷没有产物钉行，收口册一律直接量盘。" % (
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
    face, F, ns = run(mut=mut, land=land)
    if mut:
        print(u"控制 %d/%d 点火，rc=1 收尾（变异体必须留红）" % (
            face["controls_fired"], face["controls_total"]))
        sys.stdout.flush()
        return 1
    print(u"控制 %d/%d 点火、红 %s、mode=%s、耗时 %.2f s" % (
        face["controls_fired"], face["controls_total"], face["controls_red"],
        face["mode"], face["elapsed_s"]))
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
    body = volume(face, F)
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
        print(u"  %-72s %6d B md5 %s" % (rel(p), img(p)["bytes"], img(p)["md5"]))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Fatal as e:
        print(u"FATAL: %s" % e)
        sys.exit(1)
