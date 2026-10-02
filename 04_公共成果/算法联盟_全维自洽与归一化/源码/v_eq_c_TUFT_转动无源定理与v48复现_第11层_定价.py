# -*- coding: utf-8 -*-
"""
v = c 求导验证链 · 第 ⑪ 层：转动能否给挠率供源 + v48 旋转 QNM 的可复现性
============================================================================

位置：承接第 ⑩ 层。⑩ 层在 C-06／B-02 证了「最小 EC 下**静态**外区挠率恒零」，并把卷十四 §B
的 T_B 扫描判成「没有经典源」。用户提的方向一（转动 Kerr–EC 黑洞 + 自旋-挠率耦合 ⇒ 旋转 QNM）
必须回答 ⑩ 层没答的那一问：**把背景换成转动的，外区还恒零吗？**
本层答这一问，并把方向一脚下另一块砖（v48 那批**照抄进合并报告**的旋转极点）改成现场再生。

三件事
------
[V 复现层] 现场调用 S16 的 `_audit_v48_rotating_qnm.py` 两次（cwd 在临时目录 ⇒ **绝不覆盖**
          档案那份 out.txt），两跑互比、再与 2026-09-24 存档图像逐字节比，并把报告照抄的
          每一枚数分类（逐字符可再生／同值异形／值已随环境移动／不在任何 v48 图像里）。
          问的不是「v48 算得对不对」，是「它抄进报告的数今天还能不能长出来」。
[R 结构层] sympy 现算 BL 度规行列式（复现闸：det g 必须恰为 −Σ²sin²θ）与 Carter 式标架
          （复现闸：标架必须逐分量重建同一度规，且 det e = Σsinθ），再把「挠率 EOM 代数」
          一般化成**任意**代数块 M：K=−M⁻¹J ⇒ J=0 ⇒ K=0 与 a 无关；
          ξ≠0 的极点同样与 a 无关。⇒ **转动既供不出外区挠率，也不生出力程**。
[G 比价层] 就算要让 Cartan 道填上 v48 现读的 GR 门 B 缺口 Δ，反解所需视界半径与质量
          （全部以 Planck 单位表示，**不引外部天体数**）。

不做的事
--------
不提出新方程，不宣称统一场论被推进；不写 S14 claims.csv、不写算法联盟 README.md（并发写者持有）。
"""
from __future__ import print_function

import os
import re
import sys
import json
import time
import ast
import shutil
import tempfile
import subprocess

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import sympy as sp
import mpmath as mp

T_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(BASE))
PROJ = os.path.dirname(ROOT)
OUT_DIR = os.path.join(BASE, "数据")
SCRATCH = os.path.join(PROJ, "scratch", "L11")
STEM = "v_eq_c_TUFT_转动无源定理与v48复现_第11层_定价"
MD_PATH = os.path.join(OUT_DIR, STEM + ".md")
JSON_PATH = os.path.join(OUT_DIR, STEM + ".json")

mp.mp.dps = 50

WANT = ["hbar", "c", "e", "G", "Ggev", "alpha", "m_e", "m_e_gev", "GF", "GEV_J"]
CONST_FILE = os.path.join(ROOT, "02_共享基础", "公共计算", "dimensional_transmutation_open7.py")
TEN_MD = os.path.join(OUT_DIR, "v_eq_c_TUFT_Cartan自旋耦合通道_第10层_定价.md")
AUDIT_DIR = os.path.join(ROOT, "01_独立体系", "S16_TUFT归一化主册", "07_计算复现",
                         "源码", "审计轮次")
V48_PY = os.path.join(AUDIT_DIR, "_audit_v48_rotating_qnm.py")
V48_OUT = os.path.join(AUDIT_DIR, "_audit_v48_rotating_qnm_out.txt")
V48_RPT = os.path.join(ROOT, "01_独立体系", "S16_TUFT归一化主册", "13_论文与成果",
                       "合并报告", "TUFT_v48_旋转QNM合并报告.md")
V14_PLAN = os.path.join(ROOT, "01_独立体系", "S14_挠率统一场论TUFT", "00_研究立项",
                        "卷十四_CMB与黑洞QNM联合约束_研究计划.md")
LEDGER = os.path.join(ROOT, "01_独立体系", "S16_TUFT归一化主册", "13_论文与成果",
                      "台账", "TUFT_归一化台账_v1.0.json")
LEDGER_KEY = "main_agent_v58_v48_rerun"
PIN_MIN_SIG = 4              # 台账块里参与比对的数至少几位有效数字（版本号／单双位小数不算）

# 判据里显式声明的门槛（手感不算判据，全部印进版面）
SEMI_FLOOR = mp.mpf(1000)        # 经典区视界半径下限（本轮声明，非外部天体数）
DEC_BAR = mp.mpf(1)              # 双路互校的十年门（与 ⑩ 层同值）
SYMFLOOR = mp.mpf("1e-30")       # 符号恒等式的数值判据（40 位 evalf 下的相对差上限）
SIX_BAR = mp.mpf("0.10")         # 报告 §6「数值接近」的门：相对差 10%（本轮声明）
NPTS = 4                         # 恒等式要在几个独立格点上验（下面现构造，不硬编值）

GATE_TOKENS = ["GATE A (n0>=6 digits): PASS", "GATE B (split slope >=4 digits): FAIL",
               "NOT read as physical (iron law)", "split/a = 0.096236",
               "target c_rot = 0.0628831"]
# 合并报告里照抄的数（逐枚取自报告原文；桶别由 classify() 现判）
REP_TOKENS = ["0.373671684418", "0.096236", "0.0481181", "0.2515323", "1.538×10⁻²",
              "0.376860600", "0.366412304", "0.345849701", "0.104483", "4.5×10⁻⁹"]
BUCKET_NAME = {1: "逐字符可再生", 2: "同值异形（字形或精度）可再生",
               3: "值已随环境移动（只在存档图像里找得到）",
               4: "不在任何 v48 图像里（来源须另有载体）", 5: "非数值 token，无从判定"}


def read_constants(path, names):
    got = {}
    for node in ast.walk(ast.parse(open(path, encoding="utf-8").read())):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id in names and tgt.id not in got:
                    try:
                        val = ast.literal_eval(node.value)
                    except Exception:
                        continue
                    if isinstance(val, (int, float)):
                        got[tgt.id] = (val, node.lineno)
    return got


def anchor(path, needle):
    if not os.path.exists(path):
        return []
    return [i for i, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1)
            if needle in line]


def ns(x, n=8):
    if x is None:
        return "NA"
    return mp.nstr(mp.mpf(x), n)


CONST = read_constants(CONST_FILE, WANT)
MISSING = [k for k in WANT if k not in CONST]

NEEDLES = {
    "v48_seed循环": (V48_PY, "for seed in (0,1,2):"),
    "v48_rng": (V48_PY, "rng = np.random.default_rng(seed)"),
    "v48_自写输出": (V48_PY, 'open("_audit_v48_rotating_qnm_out.txt","w"'),
    "v48_缺交叉项": (V48_PY, "Teukolsky"),
    "报告_照抄纪律": (V48_RPT, "核对后照抄"),
    "报告_门B数字": (V48_RPT, "0.096236"),
    "报告_§6一致性句": (V48_RPT, "数值接近"),
    "报告_v44一阶值": (V48_RPT, "splitR/a_TUFT"),
    "台账_v58自证句": (LEDGER, "ALL numbers reproduced"),
    "10层_外区无源": (TEN_MD, "代数解 K=J/A 无齐次自由度"),
    "卷十四_T_B背景": (V14_PLAN, "背景挠率"),
}


# =========================================================================
# 复现机器
# =========================================================================
def read_pair(path):
    """**按字节读**再解码：文本模式会把 CRLF 折成 LF，于是「字节数」实为归一化字符数
    （本层第一次正式运行的版面上自抓到；那份版面已被后续运行覆盖，故此处不复述它的数字）。"""
    raw = open(path, "rb").read() if os.path.exists(path) else b""
    txt = raw.decode("utf-8", "replace")
    return txt, len(raw), txt.count("\r\n")


def read_ledger_block():
    """从 S16 归一化台账 json 里现读 v5.8 那一块，提取它**自印**的十进制 token。
    提取规则（全部印进版面）：NUMRE 形如 `[+-]?d+.d+`；跳过科学计数（指数位会被 val_of
    误算进有效位数，宁可不判）；跳过有效数字不足 PIN_MIN_SIG 的（版本号、单双位小数）。"""
    raw = open(LEDGER, "rb").read() if os.path.exists(LEDGER) else b""
    txt_all = raw.decode("utf-8-sig", "replace")
    try:
        blk = json.loads(txt_all).get(LEDGER_KEY)
    except Exception:
        blk = None
    if not isinstance(blk, dict):
        return "", [], [], "NA（台账或该块没读到）", len(raw), txt_all.count("\r\n")
    btxt = json.dumps(blk, ensure_ascii=False)
    claim = re.sub(r"\s+", " ", str(blk.get("method", "")))[:320]
    pins, skipped, seen = [], [], set()
    for m in NUMRE.finditer(btxt):
        tok = m.group(0)
        if tok in seen:
            continue
        seen.add(tok)
        v, s = val_of(tok)
        if "e" in tok.lower() or "E" in tok:
            skipped.append(tok)
        elif v is None or s < PIN_MIN_SIG:
            skipped.append(tok)
        else:
            pins.append((tok, v, s))
    return btxt, pins, skipped, claim, len(raw), txt_all.count("\r\n")


def run_v48(tag):
    tmp = tempfile.mkdtemp(prefix="L11_" + tag + "_")
    proc = subprocess.run([sys.executable, V48_PY], cwd=tmp,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p = os.path.join(tmp, "_audit_v48_rotating_qnm_out.txt")
    img, nbytes, ncrlf = read_pair(p)
    return {"tag": tag, "rc": proc.returncode, "tmp": tmp, "image": img,
            "bytes": nbytes, "crlf": ncrlf, "lines": img.count("\n") + 1}


def diff_rows(a, b):
    la, lb = a.split("\n"), b.split("\n")
    n = max(len(la), len(lb))
    return [i + 1 for i in range(n)
            if (la[i] if i < len(la) else None) != (lb[i] if i < len(lb) else None)]


def read_split(image, prefix):
    for line in image.split("\n"):
        if line.strip().startswith(prefix):
            m = re.search(r"split/a = ([+\-0-9.]+)", line)
            if m:
                return mp.mpf(m.group(1))
    return None


def delta_from(image):
    ray = read_split(image, "(i) Rayleigh")
    tgt = read_split(image, "target c_rot")
    if ray is None or tgt is None or tgt == 0:
        return None, None, None
    return ray, tgt, abs(tgt - ray) / abs(tgt)


def poles(image):
    got = {}
    for line in image.split("\n"):
        m = re.search(r"a=([0-9.]+) m=([+\-]2)\s+pole=([+\-0-9.]+)\s*([+\-][0-9.]+)i", line)
        if m:
            got[(m.group(1), m.group(2))] = complex(float(m.group(3)), float(m.group(4)))
    return got


def worst_pole_move(d1, d2):
    ks = [k for k in d1 if k in d2]
    if not ks:
        return None, None
    return max(abs(d1[k] - d2[k]) for k in ks), max(ks, key=lambda k: abs(d1[k] - d2[k]))


NUMRE = re.compile(r"[+\-]?[0-9]+\.[0-9]+(?:[eE][+\-]?[0-9]+)?")
SUP = {"\u2070": "0", "\u00b9": "1", "\u00b2": "2", "\u00b3": "3", "\u2074": "4",
       "\u2075": "5", "\u2076": "6", "\u2077": "7", "\u2078": "8", "\u2079": "9",
       "\u207b": "-", "\u2212": "-", "\u00d710": "e", "×10": "e"}


def ascii_form(tok):
    out = tok
    for k in ("\u00d710", "\u2212", "\u207b"):
        out = out.replace(k, SUP[k])
    for ch in "\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079":
        out = out.replace(ch, SUP[ch])
    return out


def val_of(tok):
    m = NUMRE.match(ascii_form(tok).replace("E", "e"))
    if not m:
        return None, 0
    v = mp.mpf(m.group(0))
    sig = len(re.sub(r"[^0-9]", "", m.group(0)).lstrip("0")) or 1
    return v, sig


def numlist(image):
    out = []
    for m in NUMRE.finditer(image):
        try:
            out.append(mp.mpf(m.group(0)))
        except Exception:
            pass
    return out


def same_print(v, cands, sig):
    p = mp.nstr(mp.mpf(v), sig)
    for c in cands:
        if mp.nstr(mp.mpf(c), sig) == p:
            return True
    return False


def classify(tok, fresh_img, fresh_vals, arch_vals):
    if tok in fresh_img:
        return 1
    v, sig = val_of(tok)
    if v is None:
        return 5
    if same_print(v, fresh_vals, sig):
        return 2
    if same_print(v, arch_vals, sig):
        return 3
    return 4


# =========================================================================
# 结构机器（sympy）
# =========================================================================
r, th, a, Mm, q2, xi = sp.symbols("r theta a M q2 xi", positive=True, real=True)
Sig = r ** 2 + a ** 2 * sp.cos(th) ** 2
Del = r ** 2 - 2 * Mm * r + a ** 2
Acart = (r ** 2 + a ** 2) ** 2 - Del * a ** 2 * sp.sin(th) ** 2
S2 = sp.sin(th) ** 2

# 恒等式的四个独立检验格点（全部有理数；根号在格点上按 40 位求值）
GRID = [{r: sp.Integer(6), a: sp.Rational(7, 10), th: sp.Integer(1), Mm: sp.Integer(1)},
        {r: sp.Rational(21, 10), a: sp.Rational(9, 10), th: sp.Rational(3, 2), Mm: sp.Rational(1, 2)},
        {r: sp.Integer(4), a: sp.Rational(1, 3), th: sp.Rational(11, 10), Mm: sp.Integer(1)},
        {r: sp.Integer(50), a: sp.Rational(1, 2), th: sp.Integer(2), Mm: sp.Integer(1)}]


def ev(expr, p):
    return mp.mpf(expr.subs(p).evalf(40))


def bl_metric(mut=None):
    """Boyer–Lindquist（−+++，几何单位）。
    M_BL_FACTOR2 把 g_{tφ} 的模放大 2 倍。**符号写反是不可测的**——det g 只吃它的平方，
    这一条就是本轮把变异体从 SIGN_TYPO 换成 FACTOR2 的原因（登记在版面诚实边界）。"""
    gtf = (2 * a * Mm * r * S2 / Sig) * (2 if mut == "M_BL_FACTOR2" else 1)
    return sp.Matrix([[-(1 - 2 * Mm * r / Sig), 0, 0, -gtf],
                      [0, Sig / Del, 0, 0],
                      [0, 0, Sig, 0],
                      [-gtf, 0, 0, Acart * S2 / Sig]])


def tetrad(mut=None):
    """Carter 式对角标架（余标架 1-形式，行=a、列=μ）：
       θ^0 = √(Δ/Σ)(dt − a sin²θ dφ)、θ^1 = √(Σ/Δ)dr、θ^2 = √Σ dθ、
       θ^3 = (sinθ/√Σ)[(r²+a²)dφ − a dt]。
    转动指纹是两根与 a 成正比的非对角元 e^0_φ、e^3_t；M_TETRAD_TRIVIAL 把它们设零＝假装不转。"""
    d0 = sp.sqrt(Del / Sig)
    e0p, e3t = -a * S2 * d0, -a * sp.sin(th) / sp.sqrt(Sig)
    if mut == "M_TETRAD_TRIVIAL":
        e0p, e3t = sp.Integer(0), sp.Integer(0)
    E = sp.Matrix([[d0, 0, 0, e0p],
                   [0, sp.sqrt(Sig / Del), 0, 0],
                   [0, 0, sp.sqrt(Sig), 0],
                   [e3t, 0, 0, (r ** 2 + a ** 2) * sp.sin(th) / sp.sqrt(Sig)]])
    return E, sp.simplify(e3t), sp.simplify(e0p)


def algebraic_block(mut=None):
    """把 ⑩ 层 C-05 的「A 是代数系数」一般化成任意 3×3 代数块 M（含 a），实测三件事：
    (1) e=√−g 整体乘出 ⇒ 解里被约掉；(2) det M≠0（且此处实测 det M 与 a 无关）⇒ 唯一解；
    (3) J=0 ⇒ K 逐分量恒零，与 a 无关。M_HOMO_BRANCH 给解外挂一个与 J 无关的背景项（＝外冻结 T_B）。"""
    n = 3
    Me = sp.Matrix(n, n, lambda i, j: sp.Symbol("m%d%d" % (i, j)))
    Ke = sp.Matrix(n, 1, lambda i, j: sp.Symbol("k%d" % i))
    Je = sp.Matrix(n, 1, lambda i, j: sp.Symbol("j%d" % i))
    ee = sp.Symbol("sqrt_minus_g")
    L = ee * (sp.Rational(1, 2) * (Ke.T * Me * Ke)[0] + (Je.T * Ke)[0])
    eom = [sp.diff(L, Ke[i]) for i in range(n)]
    sol = sp.solve(eom, [sp.Symbol("k%d" % i) for i in range(n)], dict=True)
    kk = sp.Matrix([sol[0][sp.Symbol("k%d" % i)] for i in range(n)]) if sol else None
    e_cancel = bool(kk is not None and all(sp.simplify(sp.diff(x, ee)) == 0 for x in kk))
    blk = sp.Matrix([[1 + a ** 2 / r ** 2, a / r, 0],
                     [a / r, 1, 0],
                     [0, 0, 1 + Mm / r]])
    det_blk = sp.simplify(blk.det())
    krot = -blk.inv() * Je
    if mut == "M_HOMO_BRANCH":
        krot = krot + sp.Matrix([sp.Symbol("Tbg"), 0, 0])
    zero_J = [sp.simplify(x.subs({sp.Symbol("j%d" % i): 0 for i in range(n)})) == 0
              for x in krot]
    a_free_det = det_blk.free_symbols.isdisjoint({a})
    return {"eom": eom, "kk": kk, "e_cancel": e_cancel, "det_blk": det_blk,
            "krot": [sp.simplify(x) for x in krot], "zero_J": zero_J,
            "a_free_det": a_free_det, "homo": mut == "M_HOMO_BRANCH"}


def propagator(mode, mut=None):
    """把 ⑩ 层的代数系数 A 取成 R-03 那块里**带 a 的分量** A(a)=1+a²/r²，
    于是「极点存不存在」被真的拿去和 a 比，而不是和我手写的符号比。
    mode="contact" ⇒ ξ=0（分母不含 q² ⇒ 无力程）；mode="kinetic" ⇒ ξ≠0（含 q² ⇒ 有极点）。
    M_FORCE_CONTACT 把 kinetic 模式的 ξ 也设成 0（＝把有极点的分母声明成接触项）。"""
    A_of_a = 1 + a ** 2 / r ** 2
    off = mode == "contact" or mut == "M_FORCE_CONTACT"
    xi_eff = sp.Integer(0) if off else xi
    den = 2 * A_of_a - 2 * q2 * xi_eff
    q2_star = sp.solve(sp.Eq(den, 0), q2)
    pole_a0 = bool(sp.solve(sp.Eq(den.subs(a, 0), 0), q2))
    return {"mode": mode, "den": sp.simplify(den), "q2_star": q2_star,
            "pole": bool(q2_star), "pole_at_a0": pole_a0,
            "q2_in_den": q2 in den.atoms(sp.Symbol)}


def required_horizon(delta, c0, mut=None):
    """η(r₊)=8πc₀(ℓ_Pl/r₊)² ≥ Δ ⇒ r₊ ≤ √(8πc₀/Δ)（可行集是**上**界）。
    M_INVERT_RATIO 把不等号方向解反（⇒ 可行集变成下界，于是「任何大黑洞都够」）。"""
    if delta is None or delta <= 0:
        return None, None
    k = 8 * mp.pi * c0
    rr = mp.sqrt(k / delta)
    return rr, (">=" if mut == "M_INVERT_RATIO" else "<=")


def feasible_meets_classical(rr, sense):
    """可行集 A 与经典窗口 B=[SEMI_FLOOR,∞) 是否相交（区间算术，不写死结论）。"""
    if rr is None:
        return None, None, None
    if sense == ">=":
        lo, hi = max(rr, SEMI_FLOOR), mp.inf
    else:
        lo, hi = SEMI_FLOOR, rr
    return lo, hi, (lo <= hi)


def eta_route_A(rr, c0):
    return 8 * mp.pi * c0 / (rr ** 2)


def eta_route_B(rr, c0, mut=None):
    """独立第二路：x 不由「r₊ 以 Planck 长度计」给出，而由 SI 三常数造 ℓ_Pl、E_Pl，
    再取视界能量 E_H=ħc/r₊ 求比值 x=E_H/E_Pl。η=8πc₀x²。
    M_RATIO_INVERT 把 x 写成 E_Pl/E_H（＝比值取倒）。"""
    hbar = mp.mpf(CONST["hbar"][0])
    cc = mp.mpf(CONST["c"][0])
    G = mp.mpf(CONST["G"][0])
    GEV_J = mp.mpf(CONST["GEV_J"][0])
    lpl = mp.sqrt(hbar * G / cc ** 3)
    E_Pl = mp.sqrt(hbar * cc ** 5 / G) / GEV_J
    E_H = (hbar * cc / (rr * lpl)) / GEV_J
    x = E_Pl / E_H if mut == "M_RATIO_INVERT" else E_H / E_Pl
    return 8 * mp.pi * c0 * x ** 2, lpl, E_Pl, E_H, x


# =========================================================================
# 判定：每行都由谓词函数出，变异臂走**同一条路**
# =========================================================================
def P_A00(ctx, mut=None):
    ok = not MISSING
    detail = "现读 " + str(len(CONST)) + " 枚于 " + os.path.basename(CONST_FILE) + "："
    detail += "；".join(k + "@" + str(CONST[k][1]) for k in sorted(CONST, key=lambda x: CONST[x][1]))
    if MISSING:
        detail += "｜缺 " + ",".join(MISSING)
    return ("PASS" if ok else "FAIL"), detail


def P_A01(ctx, mut=None):
    anch = {k: anchor(p, (s + "错字") if mut == "M_NEEDLE_TYPO" else s)
            for k, (p, s) in NEEDLES.items()}
    ctx["ANCH"] = anch
    lost = [k for k, v in anch.items() if not v]
    detail = "现读行号：" + "；".join(k + "@" + ",".join(map(str, v)) for k, v in anch.items())
    if lost:
        detail += "｜未命中 " + ",".join(lost)
    return ("PASS" if not lost else "FAIL"), detail


def P_A02(ctx, mut=None):
    ex = [(p, os.path.exists(p)) for p in (V48_PY, V48_OUT, V48_RPT)]
    ok = all(x for _, x in ex)
    return ("PASS" if ok else "FAIL"), \
        "；".join(os.path.basename(p) + ("=在盘" if e else "=缺失") for p, e in ex)


def P_V01(ctx, mut=None):
    img_b = ctx["arc"] if mut == "M_DRAW_VS_ARCHIVE" else ctx["d2"]["image"]
    rows = diff_rows(ctx["d1"]["image"], img_b)
    ok = (ctx["d1"]["rc"] == 0 and ctx["d2"]["rc"] == 0 and not rows)
    detail = "两跑 rc=" + str(ctx["d1"]["rc"]) + "/" + str(ctx["d2"]["rc"]) + "，图像（盘上字节）"
    detail += str(ctx["d1"]["bytes"]) + "/" + str(ctx["d2"]["bytes"]) + " B、CRLF " \
              + str(ctx["d1"]["crlf"]) + "/" + str(ctx["d2"]["crlf"]) + "，不同行数=" + str(len(rows))
    if rows:
        detail += "（行 " + str(rows[:8]) + "）"
    if mut == "M_DRAW_VS_ARCHIVE":
        detail += "｜本臂把「两跑互比」的第二跑换成 2026-09-24 存档图像"
    return ("PASS" if ok else "FAIL"), detail


def P_V02(ctx, mut=None):
    b = ctx["arc"] if mut == "M_SELF_COMPARE_PROBE" else ctx["d1"]["image"]
    rows = diff_rows(ctx["arc"], b)
    mv, where = worst_pole_move(poles(ctx["arc"]), poles(ctx["d1"]["image"]))
    ok = not rows
    detail = "存档不同行数=" + str(len(rows)) + "（行号 " + str(rows[:10]) + "）；"
    detail += "存档盘上 " + str(ctx["ARC_BYTES"]) + " B、CRLF " + str(ctx["ARC_CRLF"])
    detail += " 对现抽盘上 " + str(ctx["d1"]["bytes"]) + " B、CRLF " + str(ctx["d1"]["crlf"]) + "；"
    detail += "旋转极点最大位移 |Δpole|=" + ns(mv, 6)
    if where:
        detail += "（格点 a=" + str(where[0]) + ", m=" + str(where[1]) + "）"
    if mut == "M_SELF_COMPARE_PROBE":
        detail += "｜本臂把存档与**自己**相比（恒同，故必然判可复现）"
    return ("PASS" if ok else "FAIL"), detail


def P_V03(ctx, mut=None):
    hay = ctx["rpt"] if mut == "M_SEARCH_WRONG_IMAGE" else ctx["d1"]["image"]
    hit = [t for t in GATE_TOKENS if t in hay]
    ok = len(hit) == len(GATE_TOKENS)
    detail = "现抽图像命中判决级 token " + str(len(hit)) + "/" + str(len(GATE_TOKENS))
    if not ok:
        detail += "｜未命中 " + ",".join(t for t in GATE_TOKENS if t not in hit)
    if mut == "M_SEARCH_WRONG_IMAGE":
        detail += "｜本臂把「在哪份图像里找判决 token」换成合并报告"
    return ("PASS" if ok else "FAIL"), detail


def in_image_value(tok, vals, img):
    """这枚 token 是不是「某幅 v48 图像里的数」——按该 token 自己的有效位数比，不放宽。"""
    if tok in img:
        return True
    v, sig = val_of(tok)
    if v is None:
        return False
    return same_print(v, vals, sig)


def P_V04(ctx, mut=None):
    """受检主张：报告照抄的那些**住在 v48 图像里**的数，今天现抽仍可再生。
    「以哪幅图像判可再生」是这一行唯一的自由：基线以现抽判，
    M_JUDGE_VS_ARCHIVE 改成以存档判（＝拿抄件对着原稿核，而不是对着今天重长的东西核）。"""
    from_img = [t for t in REP_TOKENS
                if in_image_value(t, ctx["FVALS"], ctx["d1"]["image"])
                or in_image_value(t, ctx["AVALS"], ctx["arc"])]
    ctx["OFF"] = [t for t in REP_TOKENS if t not in from_img]
    judge_img = ctx["arc"] if mut == "M_JUDGE_VS_ARCHIVE" else ctx["d1"]["image"]
    judge_vals = ctx["AVALS"] if mut == "M_JUDGE_VS_ARCHIVE" else ctx["FVALS"]
    buckets = {t: classify(t, judge_img, judge_vals, ctx["AVALS"]) for t in from_img}
    ctx["BUCKET"] = buckets
    gone = sorted(t for t in from_img if buckets[t] not in (1, 2))
    tally = "；".join(BUCKET_NAME[b] + " " + str(sum(1 for x in from_img if buckets[x] == b)) + " 枚"
                      for b in sorted(set(buckets.values())))
    detail = "在图像里的报告 token " + str(len(from_img)) + "/" + str(len(REP_TOKENS)) + " 枚；桶别：" + tally
    detail += "｜不可再生清单 " + (",".join(gone) or "<无>")
    detail += "｜不在任何 v48 图像里的（须另有载体）：" + (",".join(ctx["OFF"]) or "<无>")
    if mut == "M_JUDGE_VS_ARCHIVE":
        detail += "｜本臂改成以 2026-09-24 存档图像判「可再生」（对着原稿核抄件，而非对着今天重长的核）"
    return ("PASS" if not gone else "FAIL"), detail


def P_V06(ctx, mut=None):
    """审查面完整性：分桶判据的分母必须是**声明的全数** token，且每枚都真在报告里。
    M_TOKENS_ONLY_GATE 把审查面缩到最靠得住的前两枚——它不改结论，只改「有几枚被看过」。"""
    toks = REP_TOKENS[:2] if mut == "M_TOKENS_ONLY_GATE" else REP_TOKENS
    in_rep = [t for t in toks if t in ctx["rpt"]]
    ok = (len(toks) == len(REP_TOKENS)) and (len(in_rep) == len(toks))
    detail = ("审查面 " + str(len(toks)) + "/" + str(len(REP_TOKENS))
              + " 枚（须全数）；其中真在报告里的 " + str(len(in_rep)) + " 枚")
    if not ok:
        detail += "｜本臂把分母缩成 " + str(len(toks))
        detail += " 枚 ⇒ V-04 的「不可再生清单」会跟着变短（分母被挪走，不是结论变硬）"
    return ("PASS" if ok else "FAIL"), detail


def read_measured_split(image, a_tag):
    for line in image.split("\n"):
        m = re.search(r"measured TUFT split/a @a=" + re.escape(a_tag) + r" = ([+\-0-9.]+)", line)
        if m:
            return mp.mpf(m.group(1))
    return None


def read_v44_first_order(report):
    """v44 的一阶估计必须从报告里**现读**（本层没有 v44 的任何脚本）。"""
    m = re.search(r"splitR/a_TUFT = \*\*([0-9.]+)\*\*", report)
    return mp.mpf(m.group(1)) if m else None


def P_V07(ctx, mut=None):
    """受检主张：报告 §6「a=0.10 的非微扰 split/a 与 v44 一阶（那枚数从报告正文现读，本层不复述）」
    数值接近——这一致性读数今天仍可从 v48 长出。基线拿现抽图像里的那枚，
    M_SIX_AGREEMENT_ARCHIVE 改拿 2026-09-24 存档里的那枚（＝把「可再生」偷偷换成「当初确实接近」）。"""
    src = ctx["arc"] if mut == "M_SIX_AGREEMENT_ARCHIVE" else ctx["d1"]["image"]
    which = "存档图像" if mut == "M_SIX_AGREEMENT_ARCHIVE" else "现抽图像"
    v44 = read_v44_first_order(ctx["rpt"])
    val = read_measured_split(src, "0.10")
    if v44 is None or val is None:
        return "BOUNDARY", "一致性判据的两枚入参没齐（v44=" + str(v44) + "，split/a@0.10=" + str(val) + "）"
    rel = abs(val - v44) / abs(v44)
    ok = rel <= SIX_BAR
    ctx["SIX"] = {"val": val, "v44": v44, "rel": rel, "which": which}
    detail = which + "里 measured split/a@a=0.10 = " + ns(val, 6) + "；v44 一阶（报告现读）= " + ns(v44, 5)
    detail += " ⇒ 相对差 = " + ns(rel, 4) + " 对门 " + ns(SIX_BAR, 3) \
              + (" ⇒ 报告 §6 那句「数值接近」（锚点 报告_§6一致性句）今天不成立" if not ok
                 else " ⇒ 该句在这份图像上成立")
    detail += "；符号对照：现抽 " + ("负" if val < 0 else "正") + " 对 v44 " + ("正" if v44 > 0 else "负")
    if mut == "M_SIX_AGREEMENT_ARCHIVE":
        detail += "｜本臂改判存档那枚（＝用当年的一致性冒充今天的可再生）"
    return ("PASS" if ok else "FAIL"), detail


def P_V08(ctx, mut=None):
    """受检主张：S16 台账 v5.8 块自印「re-ran ... ALL numbers reproduced digit-for-digit
    (incl. rewritten _audit_v48_rotating_qnm_out.txt identical)」——它钉住的那些数今天还能从 v48 长出吗。
    基线以现抽图像判；M_LEDGER_SELF_PROVES 改成以**台账块自己**判（拿断言对着自己核 ⇒ 恒真）。"""
    pins = ctx["LEDGER_PINS"]
    if "ALL numbers reproduced" not in ctx["LEDGER_CLAIM"]:
        return "BOUNDARY", ("台账块里那句「ALL numbers reproduced digit-for-digit」断言没现读到"
                            "（摘录被截断或该块已改写）⇒ 受检主张本身不在场，不许拿硬编文案顶上")
    if not pins:
        return "BOUNDARY", ("台账块里一枚可比数都没提取到（≥" + str(PIN_MIN_SIG)
                            + " 位、不含科学计数）⇒ 判据空转，不许当成通过")
    judge = ctx["LVALS"] if mut == "M_LEDGER_SELF_PROVES" else ctx["FVALS"]
    who = "台账块自己" if mut == "M_LEDGER_SELF_PROVES" else "本层现抽图像"
    miss = [t for t, v, s in pins if not same_print(v, judge, s)]
    detail = ("台账 " + os.path.basename(LEDGER) + " 的 " + LEDGER_KEY + " 块现读可比数 "
              + str(len(pins)) + " 枚：" + ("、".join(t for t, v, s in pins) or "<无>")
              + "；被排除 " + str(len(ctx["LEDGER_SKIPPED"])) + " 枚（科学计数或位数不足）："
              + ("、".join(ctx["LEDGER_SKIPPED"]) or "<无>")
              + "；对" + who + "判不能再生 " + str(len(miss)) + " 枚："
              + ("、".join(miss) or "<无>"))
    detail += "｜台账自印的断言（锚点 台账_v58自证句）：" + ctx["LEDGER_CLAIM"]
    if mut == "M_LEDGER_SELF_PROVES":
        detail += "｜本臂把判据换成台账块自己（自证：每枚数当然在它自己的文本里）"
    return ("PASS" if not miss else "FAIL"), detail


def P_V05(ctx, mut=None):
    ray, tgt, dd = delta_from(ctx["d1"]["image"])
    ray2, tgt2, dd2 = delta_from(ctx["d2"]["image"])
    if mut == "M_GAP_FROM_MEMORY":
        dd2 = mp.mpf("0.62")
    same = (dd is not None and dd2 is not None and abs(dd - dd2) < mp.mpf("1e-12"))
    ctx["DELTA"] = dd
    detail = "现读 split/a=" + ns(ray, 6) + " 对 GR 靶=" + ns(tgt, 7) + " ⇒ Δ=" + ns(dd, 6)
    detail += "；第二跑 Δ=" + ns(dd2, 6) + " ⇒ 不可复现的是**极点**，不是**缺口**"
    if mut == "M_GAP_FROM_MEMORY":
        detail += "｜本臂的第二跑 Δ 改成硬编记忆值而不是现读"
    return ("PASS" if same else "BOUNDARY"), detail


def P_R01(ctx, mut=None):
    g = bl_metric(mut=mut)
    gd = sp.simplify(g.det())
    tgt = -Sig ** 2 * sp.sin(th) ** 2
    rel = [abs(ev(gd - tgt, p) / ev(-tgt, p)) for p in GRID]
    worst = max(rel) if rel else None
    exact = bool(sp.simplify(gd - tgt) == 0)
    ctx["GDET"] = gd
    omega = sp.simplify(-g[0, 3] / g[3, 3])
    ok = exact and worst is not None and worst == 0
    detail = "det g = " + str(gd) + "；对 −Σ²sin²θ 的差(符号 simplify) = " + str(sp.simplify(gd - tgt))
    detail += "；" + str(len(GRID)) + " 个有理格点上最大相对差 = " + ns(worst, 3)
    detail += "；帧拖曳 ω=−g_tφ/g_φφ = " + str(omega) + "（对 2aMr/𝒜 的差 = " \
              + str(sp.simplify(omega - 2 * a * Mm * r / Acart)) + "）"
    if mut == "M_BL_FACTOR2":
        detail += "｜本臂把 g_tφ 放大 2 倍（注：符号写反**测不出来**，det g 只吃它的平方）"
    return ("PASS" if ok else "FAIL"), detail


def P_R02(ctx, mut=None):
    E, e3t, e0p = tetrad(mut=mut)
    ed = sp.simplify(E.det())
    eta_m = sp.diag(-1, 1, 1, 1)
    rec = E.T * eta_m * E
    g = bl_metric()
    rel_det, rel_rec = [], []
    for p in GRID:
        scale = abs(ev(Sig * sp.sin(th), p))
        rel_det.append(abs(ev(ed, p) - ev(Sig * sp.sin(th), p)) / scale)
        rel_rec.append(max(abs(ev(rec[i, j] - g[i, j], p)) for i in range(4) for j in range(4)) / scale)
    wd, wr = max(rel_det), max(rel_rec)
    rotating = bool(e3t != 0 and e0p != 0)
    ctx["EDE"] = ed
    ok = wd < SYMFLOOR and wr < SYMFLOOR and rotating
    detail = "det e = " + str(ed) + "（" + str(len(GRID)) + " 格点上对 Σsinθ 最大相对差 " + ns(wd, 3)
    detail += "，门 " + ns(SYMFLOOR, 1) + "）；e^Tηe 逐分量重建 g 的最大相对差 " + ns(wr, 3)
    detail += "；转动指纹 e^3_t=" + str(e3t) + "、e^0_φ=" + str(e0p) + \
              (" ⇒ 转动真的在标架里" if rotating else " ⇒ 转动项被设零，标架退化成不转")
    if mut == "M_TETRAD_TRIVIAL":
        detail += "｜本臂把两根含 a 的非对角元设零（＝假装不转）"
    return ("PASS" if ok else "FAIL"), detail


def P_R03(ctx, mut=None):
    ec = algebraic_block(mut=mut)
    zj = ec["zero_J"]
    ok = (bool(zj) and all(zj) and ec["det_blk"] != 0 and ec["e_cancel"]
          and ec["a_free_det"] and not ec["homo"])
    ctx["EC"] = ec
    detail = "e 在解里被约掉=" + str(ec["e_cancel"]) + "；带 a 的块 det M = " + str(ec["det_blk"])
    detail += "（与 a 无关=" + str(ec["a_free_det"]) + "）⇒ 唯一解 K=−M⁻¹J；"
    detail += "J=0 时逐分量恒零（一般 J 的解 = " + str(ec["krot"]) + "，代入 J=0 的逐分量判真 " + str(zj) + "）"
    if mut == "M_HOMO_BRANCH":
        detail += "｜本臂在解上外挂与 J 无关的背景项 Tbg（＝外冻结 T_B）"
    return ("PASS" if ok else "FAIL"), detail


def P_R04(ctx, mut=None):
    con, kin = propagator("contact", mut=mut), propagator("kinetic", mut=mut)
    ctx["PR"] = {"contact": con, "kinetic": kin}
    ok = ((not con["q2_in_den"]) and (not con["pole"])
          and kin["pole"] and kin["pole_at_a0"] and (not con["pole_at_a0"]))
    detail = "接触侧（ξ=0）分母 = " + str(con["den"]) + "，含 q²? " + str(con["q2_in_den"]) \
             + " ⇒ 无极点；动能侧（ξ≠0）分母 = " + str(kin["den"]) + "，q²* = " \
             + str(kin["q2_star"]) + " ⇒ 极点存在"
    detail += "；把 a 设零后 q²* 仍在? " + str(kin["pole_at_a0"]) \
             + " ⇒ 极点是 ξ 的性质、不是 a 的性质（转动既不生力程也不灭力程）"
    if mut == "M_FORCE_CONTACT":
        detail += "｜本臂把 ξ≠0 的分母也声明成接触项（＝把极点抹掉）"
    return ("PASS" if ok else "FAIL"), detail


def P_R05(ctx, mut=None):
    delta = ctx.get("DELTA")
    c0 = mp.mpf(3) / 4
    rr, sense = required_horizon(delta, c0, mut=mut)
    if rr is None:
        return "BOUNDARY", "Δ 未从现抽图像读到，所需视界无从反解"
    lo, hi, meets = feasible_meets_classical(rr, sense)
    ctx["RR"], ctx["SENSE"] = rr, sense
    tab = [(k, required_horizon(delta, v, mut=mut)[0]) for k, v in
           (("3/16", mp.mpf(3) / 16), ("3/8", mp.mpf(3) / 8),
            ("3/4", c0), ("3/2", mp.mpf(3) / 2))]
    detail = "Δ=" + ns(delta, 6) + " ⇒ 供上它需 r₊ " + str(sense) + " " + "；".join(
        "c₀=" + k + ":" + ns(v, 5) + "ℓ_Pl" for k, v in tab)
    detail += "（c₀=3/4 时 M ≤ " + ns(rr / 2, 4) + "M_Pl，用 r₊=2GM/c²）；经典窗口 r₊ ≥ " \
             + ns(SEMI_FLOOR, 4) + "ℓ_Pl ⇒ 交集 [" + ns(lo, 5) + ", " \
             + ("∞" if hi == mp.inf else ns(hi, 5)) + "] " \
             + ("非空 ⇒ 主张还有活路" if meets else "为空 ⇒ 「Cartan 道可在经典黑洞区填 Δ」判 FAIL")
    if mut == "M_INVERT_RATIO":
        detail += "｜本臂把不等号方向解反（可行集从上半轴换成下半轴 ⇒ 交集恒非空）"
    return ("PASS" if meets else "FAIL"), detail


def P_R06(ctx, mut=None):
    rr = ctx.get("RR") or mp.mpf(5)
    c0 = mp.mpf(3) / 4
    ea = eta_route_A(rr, c0)
    eb, lpl, epl, eh, x = eta_route_B(rr, c0, mut=mut)
    gap = abs(mp.log10(eb) - mp.log10(ea))
    ok = gap < DEC_BAR
    detail = "路 A（纯长度比 8πc₀/r₊²，r₊ 以 ℓ_Pl 计）η = " + ns(ea, 8)
    detail += "；路 B（SI 造 ℓ_Pl=" + ns(lpl, 8) + " m、E_Pl=" + ns(epl, 8) + " GeV、E_H=" \
             + ns(eh, 8) + " GeV ⇒ x=E_H/E_Pl=" + ns(x, 8) + "）η = " + ns(eb, 8)
    detail += "；|log10 差| = " + ns(gap, 4) + " 对门 " + ns(DEC_BAR, 3)
    if mut == "M_RATIO_INVERT":
        detail += "｜本臂把路 B 的 x 写成 E_Pl/E_H（＝比值取倒）"
    return ("PASS" if ok else "BOUNDARY"), detail


ROWS = [
    ("A-00", "A 载体层", "常数载体", "常数须由载体文件 AST 现读", P_A00),
    ("A-01", "A 载体层", "v48／⑩层／卷十四 锚点", "每个锚点须在其载体里现读到行号", P_A01),
    ("A-02", "A 载体层", "v48 三件在盘", "脚本／存档图像／合并报告都得存在", P_A02),
    ("V-01", "V 复现层", "两次现抽是否逐字节相同", "同环境同码两跑应可再生", P_V01),
    ("V-02", "V 复现层", "受检主张『存档图像今天可再生』", "存档对现抽逐字节比", P_V02),
    ("V-03", "V 复现层", "判决级内容是否复现", "门 A／门 B／铁律／缺口 token 须在现抽图像", P_V03),
    ("V-04", "V 复现层", "受检主张『报告照抄的数可再生』", "审查面须为全数且每枚桶别为可再生", P_V04),
    ("V-05", "V 复现层", "缺口 Δ 是否可复现", "两跑各自现读 Δ 须相同", P_V05),
    ("V-06", "V 复现层", "审查面完整性（分母须为声明全数）", "分桶判据不许只看能过的那几枚", P_V06),
    ("V-07", "V 复现层", "受检主张『报告 §6 的微扰—非微扰一致性可再生』", "a=0.10 那枚须与 v44 一阶现读值同门", P_V07),
    ("V-08", "V 复现层", "受检主张『台账 v5.8 块自印的全数逐位复现』", "台账钉住的数须在今天的现抽图像里再生", P_V08),
    ("R-01", "R 结构层", "BL 度规行列式（复现闸）", "det g 须恰为 −Σ²sin²θ 并在格点上为 0", P_R01),
    ("R-02", "R 结构层", "Carter 标架重建 g 且转动项非零", "det e=Σsinθ、e^Tηe=g、含 a 元非零", P_R02),
    ("R-03", "R 结构层", "受检主张『换成转动背景外区仍有挠率』", "代数块唯一解在 J=0 时必须恒零", P_R03),
    ("R-04", "R 结构层", "转动能否把接触项救成有力程", "ξ=0 无 q²、ξ≠0 有极点、极点与 a 无关", P_R04),
    ("R-05", "R 结构层", "受检主张『Cartan 道可在经典黑洞区填 Δ』", "反解所需视界并与经典窗口求交", P_R05),
    ("R-06", "R 结构层", "双路互校（长度比 vs SI 常数）", "两路 η 须落在同一年代", P_R06),
]

MUT = {
    "M_NEEDLE_TYPO": (["A-01"], ["A-00", "A-02"], "锚点串各加一个错字（证明 A-01 不是无条件 PASS）"),
    "M_DRAW_VS_ARCHIVE": (["V-01"], ["V-02", "V-03"], "把「两跑互比」的第二跑换成存档图像"),
    "M_SELF_COMPARE_PROBE": (["V-02"], ["V-01"], "把存档与**自己**相比（恒同⇒必然判可复现）"),
    "M_SEARCH_WRONG_IMAGE": (["V-03"], ["V-02"], "把「在哪份图像里找判决 token」换成合并报告"),
    "M_TOKENS_ONLY_GATE": (["V-06"], ["V-03"], "只查报告 token 里最靠得住的前两枚（缩审查面＝挪分母）"),
    "M_JUDGE_VS_ARCHIVE": (["V-04"], ["V-06"], "把「可再生」改判为「对着 2026-09-24 存档核抄件」"),
    "M_SIX_AGREEMENT_ARCHIVE": (["V-07"], ["V-04", "V-06"], "§6 的一致性改拿存档那枚来判"),
    "M_LEDGER_SELF_PROVES": (["V-08"], ["V-02", "V-04", "V-07"], "台账自印的「全数逐位复现」改拿台账自己核（自证）"),
    "M_GAP_FROM_MEMORY": (["V-05"], ["V-04"], "第二跑的 Δ 用硬编记忆值而不是现读"),
    "M_BL_FACTOR2": (["R-01"], ["R-04"], "g_{tφ} 放大 2 倍（符号写反不可测，故换成模）"),
    "M_TETRAD_TRIVIAL": (["R-02"], ["R-01"], "把两根含 a 的非对角元设零＝假装不转"),
    "M_HOMO_BRANCH": (["R-03"], ["R-02"], "解上外挂与 J 无关的背景项 Tbg"),
    "M_FORCE_CONTACT": (["R-04"], ["R-03"], "把 ξ≠0 的分母也声明成接触项"),
    "M_INVERT_RATIO": (["R-05"], ["R-04"], "所需视界的不等号方向解反"),
    "M_RATIO_INVERT": (["R-06"], ["R-05"], "路 B 把 x=E_H/E_Pl 写成 E_Pl/E_H"),
}


def compute(ctx, mut=None):
    """基线与变异体都走这一条路：返回 {id: (verdict, detail)}。"""
    out = {}
    for cid, sec, item, stmt, fn in ROWS:
        out[cid] = fn(ctx, mut=mut)
    return out


def narrative_rows(ctx, base):
    ec = ctx["EC"]
    kin = ctx["PR"]["kinetic"]
    con = ctx["PR"]["contact"]
    delta, rr, sense = ctx.get("DELTA"), ctx.get("RR"), ctx.get("SENSE")
    anch = ctx["ANCH"]
    v3 = base["V-03"][0]
    b01 = "FAIL" if (base["R-03"][0] == "PASS" and base["R-04"][0] == "PASS") else "BOUNDARY"
    b02 = "FAIL" if base["R-05"][0] == "FAIL" else "BOUNDARY"
    return [
        ("B-01", "B 接口层", "受检主张『卷十四 §B 的 T_B 在转动外区可有源』判 FAIL",
         "R-03／R-04 的推广（判定由这两行的判决推出）", b01,
         "带 a 的代数块唯一解 J=0⇒K=0（det M=" + str(ec["det_blk"]) + "、与 a 无关="
         + str(ec["a_free_det"]) + "）；动能侧极点与 a 无关（ξ=0 时 pole=" + str(con["pole"])
         + "、ξ≠0 且 a=0 时 pole=" + str(kin["pole_at_a0"]) + "）⇒ 转动既供不出外区挠率也不生力程。"
         "要让 T_B≠0 只剩两条：(i) 加动能项 ⇒ 极点 ⇒ 长程力（⑩ 层 B-03 的第五力账仍未取数），"
         "(ii) 外冻结背景 ⇒ 特设，与被否证的 0.00404 同族。卷十四 §B 的 T_B 扫描在转动情形"
         "同样没有经典源（锚点 卷十四_T_B背景@" + ",".join(map(str, anch["卷十四_T_B背景"])) + "）"),
        ("B-02", "B 接口层", "受检主张『门 B 缺的那一成住在挠率账上』判 FAIL",
         "缺因归属（判定由 R-05 的判决推出）", b02,
         "v48 自己点名的缺因是 Teukolsky 的 O(a) 虚部交叉项（锚点 v48_缺交叉项@"
         + ",".join(map(str, anch["v48_缺交叉项"])) + "，脚本内多处），住**度量／算符**通道；"
         "R-05 说 Cartan 道要填 Δ=" + ns(delta, 6) + " 需 r₊ " + str(sense) + " " + ns(rr, 4)
         + "ℓ_Pl（即 M ≲ " + ns((rr or 0) / 2, 4) + "M_Pl），与经典窗口不相交；"
         "而在声明的经典下限 r₊=" + ns(SEMI_FLOOR, 4) + "ℓ_Pl 处 η=" + ns(eta_route_A(SEMI_FLOOR, mp.mpf(3) / 4), 8)
         + "，欠缺口 " + ns(mp.log10((delta or 1) / eta_route_A(SEMI_FLOOR, mp.mpf(3) / 4)), 5)
         + " 个十年——注意这个「十年」是**推论**（由两个现读量相除），不是独立测得"
         "（同句两次调用 eta_route_A，非第二来源）"),
        ("T-01", "T 自由度层", "交换定理在本档案的第三次实测", "自由度账", "INFO",
         "本层闭合的是「转动能否救挠率」（答否：R-03 唯一解 + R-04 的极点与 a 无关），"
         "支付的是方向一的全部内容：旋转 EC 黑洞若坚持最小耦合，挠率对旋转谱的贡献恒零；"
         "想要非零就买动能项（进第五力实验区）或买冻结背景（进特设桶）——与 ⑨ 层 T-01、⑩ 层 T-01 同形"),
        ("T-02", "T 自由度层", "本轮未推进清单（不得记为已解决）", "诚实边界", "INFO",
         "①门 B 为何 FAIL 的**修法**未做（要补的是完整 Teukolsky–Chandrasekhar 嵌入）；"
         "②存档图像不可再生的**根因**未归因到具体 BLAS/LAPACK/NumPy/Python 版本"
         "（只实测两跑逐字节相同、与存档不同，且脚本用固定 seed 的 default_rng；"
         "V-08 另证该「存档」本身是 09-24 重跑改写过的产物，故根因要比的是两个环境而非一份原始输出）；"
         "③ξ≠0 的第五力比价仍未取数；④v54 那条腿未做同样复现（本轮只判 v48）；"
         "⑤v48 报告的照抄数已分桶，但**报告之外**是否还有别的档案引这些数未普查；"
         "⑥TUFT 的 g-2 映射、绝对标度、质量层级、β 缺口一字未动；⑦未提出新方程；"
         "⑧S14 claims.csv 与算法联盟 README.md 未写（登记债）"),
    ]


def md_cell(s):
    return s.replace("\n", " ").replace("|", "\\|")


def build_face(ctx, base, counts, mutant_rows, armed, unarmed, elapsed, v3):
    L = []
    L.append("# v = c 求导验证链 第 ⑪ 层：转动无源定理 + v48 旋转 QNM 可复现性")
    L.append("")
    L.append("> 脚本：`04_公共成果/算法联盟_全维自洽与归一化/源码/" + STEM + ".py`  ")
    L.append("> 上游：`数据/v_eq_c_TUFT_Cartan自旋耦合通道_第10层_定价.md`（第 ⑩ 层，其 C-06／B-02 只判了**静态**外区）  ")
    L.append("> 被测对象：`01_独立体系/S16_TUFT归一化主册/07_计算复现/源码/审计轮次/_audit_v48_rotating_qnm.py` 与其存档输出、合并报告  ")
    L.append("> 现抽图像快照（本层写、不作第二权威源）：`scratch/L11/draw_d1.txt`、`scratch/L11/draw_d2.txt`、逐行差异清单 `scratch/L11/archive_vs_draw_diff.txt`  ")
    L.append("> 精度：sympy 符号恒等式 + 4 个有理格点 40 位求值；mpmath 50 位；常数与图像全部现读  ")
    L.append("> 总计 " + str(len(base) + len(ctx["NARR"])) + " 项："
             + " ".join(k + "=" + str(counts[k]) for k in sorted(counts))
             + "（耗时 " + str(elapsed) + " s，含现场两次调用 v48）")
    L.append("")
    L.append("**一句话结论**：把背景换成转动的，挠率**仍**给不出来——含 a 的代数块唯一解在 J=0 时逐位恒零、"
             "帧拖曳不进传播分母（极点是 ξ 的性质）；而要让 Cartan 道填上 v48 现读的 GR 门 B 缺口，"
             "所需视界与声明的经典窗口交集为空。另：v48 抄进合并报告的旋转极点数值在今天的环境下**不可再生**"
             "（两跑互相同、与存档 " + str(v3["rows"]) + " 行不同），"
             "但门 A／门 B／铁律与缺口 Δ 可再生。报告 §6 那句「微扰与非微扰数值接近」所依赖的 a=0.10 读数"
             "另由 V-07 判，其读数与判决只活在上面的表里，本行不复述。"
             "本层未提出新方程，也不宣称推进统一场论。")
    L.append("")
    L.append("**判定极性约定**：每行的「判定」判的是**被审主张**（属 TUFT／S16／卷十四）成不成立，"
             "不是本脚本措辞的对错 ⇒ `FAIL` 读作「该主张在本层被否证」，`PASS` 读作「该主张（或本层的复现闸）通过」。"
             "`BOUNDARY` 表示判据本身还没资格下判决，`INFO` 是自由度／诚实边界账（不是判决）。")
    L.append("")
    L.append("## 判决表")
    L.append("")
    L.append("| 编号 | 分支 | 项 | 判定 | 细节 |")
    L.append("|---|---|---|---|---|")
    for cid, sec, item, stmt, fn in ROWS:
        v, d = base[cid]
        L.append("| " + cid + " | " + sec + " | " + item + " | " + v + " | " + md_cell(d) + " |")
    for row in ctx["NARR"]:
        L.append("| " + row[0] + " | " + row[1] + " | " + row[2] + " | " + row[4] + " | " + md_cell(row[5]) + " |")
    L.append("")
    L.append("## 关键数（只活在印它的本面里；现抽图像另存于上面点名的 scratch 快照）")
    L.append("")
    L.append("| 量 | 值 | 来源/载体 |")
    L.append("|---|---|---|")
    ray, tgt, delta = delta_from(ctx["d1"]["image"])
    L.append("| v48 现读 split/a（Rayleigh，实侧） | " + ns(ray, 6) + " | 本层现抽 `scratch/L11/draw_d1.txt` |")
    L.append("| v48 现读 GR 靶 split/a | " + ns(tgt, 7) + " | 同上 |")
    L.append("| 缺口 Δ = \\|靶−实\\|/靶 | " + ns(delta, 6) + " | 由本表前两枚现读值现算 |")
    L.append("| 报告照抄 token 分桶 | " + "；".join(BUCKET_NAME[b] + " " + str(c) + " 枚"
                                                   for b, c in sorted(v3["buckets"].items()))
             + " | V-04 现判 |")
    L.append("| 报告内但不属于任何 v48 图像的 token | " + ("、".join(v3["off"]) or "<无>")
             + " | V-04 现判（这类数须另点名载体，本层不替它认账） |")
    L.append("| 存档对现抽的不同行数 | " + str(v3["rows"]) + " 行（共 " + str(v3["nline"])
             + " 行；两枚都由 `diff_rows()` 在同一次 LF 切分上数出） | V-02 现测 |")
    L.append("| 旋转极点最大位移 \\|Δpole\\| | " + ns(v3["mv"], 6) + "（a=" + str(v3["where"][0])
             + ", m=" + str(v3["where"][1]) + "） | V-02 现测 |")
    six = ctx.get("SIX") or {}
    L.append("| 报告 §6 一致性三元组 | 现抽 a=0.10 那枚 " + ns(six.get("val"), 6)
             + "；v44 一阶从报告现读 " + ns(six.get("v44"), 6)
             + "；相对差 " + ns(six.get("rel"), 4) + " 对门 " + ns(SIX_BAR, 3)
             + " | V-07 现判（v44 那个数是**读**来的，本层不重推） |")
    L.append("| 三份图像的盘上字节与 CRLF | 现抽 d1 " + str(ctx["d1"]["bytes"]) + " B、CRLF "
             + str(ctx["d1"]["crlf"]) + "；现抽 d2 " + str(ctx["d2"]["bytes"]) + " B、CRLF "
             + str(ctx["d2"]["crlf"]) + "；存档 " + str(ctx["ARC_BYTES"]) + " B、CRLF "
             + str(ctx["ARC_CRLF"]) + " | A-01／V-01／V-02 同一 read_pair() 现读 |")
    pins = ctx["LEDGER_PINS"]
    miss8 = [t for t, v, s in pins if not same_print(v, ctx["FVALS"], s)]
    L.append("| 台账 " + LEDGER_KEY + " 块的可比数 | 现读 " + str(len(pins)) + " 枚（提取规则见诚实边界）"
             + "；今天在现抽图像里不能再生 " + str(len(miss8)) + " 枚："
             + ("、".join(miss8) or "<无>") + " | V-08 现判 |")
    L.append("| 台账文件盘上尺寸 | " + str(ctx["LEDGER_BYTES"]) + " B、CRLF " + str(ctx["LEDGER_CRLF"])
             + "（本层只读不写） | read_ledger_block() 现读 |")
    L.append("| 所需视界 r₊（c₀=3/4） | r₊ " + str(ctx.get("SENSE")) + " " + ns(ctx.get("RR"), 5)
             + " ℓ_Pl | R-05 反解（8πc₀(ℓ_Pl/r₊)² ≥ Δ） |")
    L.append("| 所需质量上界 | M ≲ " + ns((ctx.get("RR") or 0) / 2, 4)
             + " M_Pl | r₊=2GM/c² ⇒ M/M_Pl=r₊/(2ℓ_Pl) |")
    L.append("| 声明的经典窗口下限 | r₊ ≥ " + ns(SEMI_FLOOR, 4) + " ℓ_Pl | 本轮显式声明（`SEMI_FLOOR`） |")
    L.append("| 该下限处的 η | " + ns(eta_route_A(SEMI_FLOOR, mp.mpf(3) / 4), 8)
             + " | 现算（与 Δ 同式） |")
    L.append("| det M（含 a 的代数块） | " + str(ctx["EC"]["det_blk"]) + " | R-03 sympy 现算 |")
    L.append("| det g（BL） | " + str(ctx["GDET"]) + " | R-01 sympy 现算 |")
    L.append("| det e（Carter 标架） | " + str(ctx["EDE"]) + " | R-02 sympy 现算 |")
    L.append("| 符号恒等式格点数与门 | " + str(NPTS) + " 个有理格点、相对差门 " + ns(SYMFLOOR, 1)
             + " | 本轮显式声明（`GRID`/`SYMFLOOR`） |")
    L.append("")
    L.append("## 报告照抄 token 的逐枚分桶（V-04 的判决拆开印；桶名与台账 json 同一批字符串）")
    L.append("")
    L.append("| 报告里的 token | V-04 判它的桶 |")
    L.append("|---|---|")
    for t in sorted(ctx["BUCKET"]):
        L.append("| " + t + " | " + BUCKET_NAME[ctx["BUCKET"][t]] + " |")
    for t in sorted(ctx.get("OFF", [])):
        L.append("| " + t + " | 不在任何 v48 图像里（须另有载体，本层不替它认账） |")
    L.append("")
    L.append("## 牙齿")
    L.append("")
    L.append("| 变异体 | 应打红 | 应不红（刻意探针） | 实打红 | 同臂未打红 | 结果 |")
    L.append("|---|---|---|---|---|---|")
    for m in mutant_rows:
        L.append("| " + m["mutant"] + " | " + ",".join(m["must_redden"]) + " | "
                 + (",".join(m["must_stay"]) or "<无>") + " | "
                 + (",".join(m["reddened"]) or "<无>") + " | "
                 + (",".join(x for x in m["must_redden"] if x not in m["reddened"]) or "<无>") + " | "
                 + ("OK" if m["clean"] else "BAD") + " |")
    L.append("")
    L.append("变异臂覆盖 " + str(len(armed)) + " / " + str(len(base) + len(ctx["NARR"])) + " 行（"
             + ",".join(armed) + "）；**无臂行 " + str(len(unarmed)) + " 行不得当作已被见证**："
             + ",".join(unarmed) + "。")
    L.append("")
    L.append("## 诚实边界与红线")
    L.append("")
    L.append("- 本层**没有提出新方程**，也没有修 v48 的门 B；它判的是「转动能否给挠率供源」与「抄进去的数能否再生」。")
    L.append("- R-03 的机器形态是**结构定理**：对任意代数块 M（det M≠0）成立，不依赖 EC 具体系数；"
             "它的**适用前提**是「最小 EC 的挠率 EOM 是代数的」——该前提由 ⑩ 层 C-05 的配平方实测，本层不重证。")
    L.append("- R-01／R-02 的恒等式同时给了符号 simplify 与 " + str(NPTS) + " 个格点上的 40 位求值；"
             "格点值由 `GRID` 现构造（全部有理、a≠0），不是挑出来的。")
    L.append("- 变异体 `M_BL_SIGN_TYPO` 被**撤下**并换成 `M_BL_FACTOR2`：g_tφ 在 det g 里只以平方出现，"
             "符号写反是**测不出来**的缺陷——这是一处「针打不红不等于闸门稳」的自抓，登记在牙齿表外。")
    L.append("- V-02 只实测「两跑相同、与存档不同」，**没有**把根因归到某个 BLAS/LAPACK/NumPy/Python 版本"
             "（登记在 T-02 ②）；因此「存档那份在今天的机器上不可再生」是可复现性判决，不是对 v48 算法正确性的判决。")
    L.append("- 门 A／门 B／铁律／Δ 在两份图像里都在（V-03、V-05）⇒ 不可复现的是**旋转极点诊断数值**一族，"
             "不是 S16 那句「TUFT 旋转极不宣告」。")
    L.append("- B-02 里那个「欠若干十年」是 Δ 与 η 的**商的对数**（同式两次调用），不是第二来源测得；"
             "版面把它写成推论。")
    L.append("- 运行 v48 时 cwd 指向临时目录：它按相对路径写自己的 out.txt（锚点 v48_自写输出@见 A-01），"
             "**档案那份一个字节没动**；现抽图像另存 scratch 快照，临时目录跑完即删。")
    L.append("- 比价全程以 Planck 单位表示，不引外部天体数；`SEMI_FLOOR`、`DEC_BAR`、`SYMFLOOR` 三个门槛由本轮显式声明。")
    L.append("- V-07 只把报告 §6 那句一致性的**两端各现读一次**（a=0.10 那枚从本层现抽图像读、v44 一阶从报告正文读），"
             "因此它判的是「这个一致性**读数**能否再生」，**不是** v44 那一阶算得对不对——后者本层没有重推。")
    L.append("- 尺寸通道的自抓：本层第一次正式运行的版面把「字节数」印成了**归一化字符数**——起因是图像用文本模式读，"
             "CRLF 被折成 LF，于是数字对、单位假。本轮改成 `read_pair()` 按字节读、并把 CRLF 条数与字节数**并排印出**"
             "（见关键数表末行与 A-01／V-01／V-02 的细节），第一次运行那份版面的具体读数随它一起被覆盖、此处不复述。")
    L.append("- V-08 的**来源**：台账 json 的 `" + LEDGER_KEY + "` 块自印「re-ran in project .venv, exit 0, "
             "ALL numbers reproduced digit-for-digit (incl. **rewritten** " + os.path.basename(V48_OUT)
             + " identical）」⇒ 本层所比的「存档图像」本身就是 2026-09-24 那次重跑的产物，不是 v48 的原始输出。"
             "所以 V-02 那句要读成「今天的环境 ≠ 09-24 的环境」，而「09-24 重跑逐位相同」这一条今天由 V-08 否证。")
    L.append("- V-08 的提取规则（现场执行、不手抄）：只取形如 `[+-]?d+.d+` 的 token，要求有效数字 ≥ "
             + str(PIN_MIN_SIG) + " 位，**跳过科学计数**（指数位会被 `val_of` 误算进有效数字，宁可不判）。"
             "被跳过的枚数与清单印在本层 stdout 的 `[台账]` 行。代价明写：静锚位移 `|d|` 与条件壁 `sigma_min` "
             "两枚科学计数因此**不在 V-08 的覆盖面里**——它们是未判，不是通过。")
    L.append("- 本轮未写 S14 `claims.csv`、未写算法联盟 `README.md`（并发写者持有）⇒ 登记是欠账。")
    L.append("")
    L.append("**红线**：数学自洽 != 物理成立；判死一条路 != 否证 TUFT 本体；"
             "「不可复现」!=「算错」——它只说明那份图像不再是任何当前环境的产物。")
    L.append("")
    return L


def write_json(ctx, all_rows, counts, mutant_rows, armed, unarmed, delta, v3):
    # 与版面同宽：json 里那些「版面上也印着的量」一律用版面用的 ns() 位数，
    # 否则同一量在两个载体上是两种精度，截前缀那一枚就是引用债（本层写后审计第 1 版就抓到两处）。
    payload = {"meta": {"script": STEM + ".py", "layer": "第 ⑪ 层（v=c 求导验证链）",
                        "elapsed_sec": round(time.time() - T_START, 1),
                        "counts": counts,
                        "guard_baseline": {q["id"]: q["verdict"] for q in all_rows},
                        "prose_anchor_lines": {k: v for k, v in ctx["ANCH"].items()},
                        "gap_delta_from_image": ns(delta, 6) if delta is not None else None,
                        "report_token_buckets": {t: BUCKET_NAME[b] for t, b in
                                                 sorted(ctx["BUCKET"].items(), key=lambda x: x[0])},
                        "declared_thresholds": {"SEMI_FLOOR_planck": ns(SEMI_FLOOR, 4),
                                                "DEC_BAR": ns(DEC_BAR, 3),
                                                "SYMFLOOR": ns(SYMFLOOR, 1),
                                                "SIX_BAR": ns(SIX_BAR, 3),
                                                "GRID_points": NPTS},
                        "v48_run_rc": [ctx["d1"]["rc"], ctx["d2"]["rc"]],
                        "v48_bytes": [ctx["d1"]["bytes"], ctx["d2"]["bytes"]],
                        "v48_disk": {"draw_d1_bytes": ctx["d1"]["bytes"],
                                     "draw_d1_crlf": ctx["d1"]["crlf"],
                                     "draw_d2_bytes": ctx["d2"]["bytes"],
                                     "draw_d2_crlf": ctx["d2"]["crlf"],
                                     "archive_bytes": ctx["ARC_BYTES"],
                                     "archive_crlf": ctx["ARC_CRLF"],
                                     "channel": "read_pair(): len(raw bytes) 与 CRLF 条数，文本模式已弃用"},
                        "six_agreement": {"a010_from_draw": ns((ctx.get("SIX") or {}).get("val"), 6),
                                          "v44_first_order_from_report": ns((ctx.get("SIX") or {}).get("v44"), 5),
                                          "relative_gap": ns((ctx.get("SIX") or {}).get("rel"), 4),
                                          "verdict": {q["id"]: q["verdict"] for q in all_rows}.get("V-07", "NA"),
                                          "note": "v44 那枚是从报告正文**读**的，本层未重推其外"},
                        "v48_archive_vs_draw": {"diff_rows": v3["rows"],
                                                "total_lines": v3["nline"],
                                                "diff_row_numbers": v3["rowlist"],
                                                "worst_pole_move": ns(v3["mv"], 6),
                                                "worst_cell": list(v3["where"])},
                        "ledger_v58": {"file_bytes": ctx["LEDGER_BYTES"],
                                       "file_crlf": ctx["LEDGER_CRLF"],
                                       "pin_min_sig": PIN_MIN_SIG,
                                       "pins": [t for t, v, s in ctx["LEDGER_PINS"]],
                                       "not_regenerated":
                                           [t for t, v, s in ctx["LEDGER_PINS"]
                                            if not same_print(v, ctx["FVALS"], s)],
                                       "skipped": ctx["LEDGER_SKIPPED"],
                                       "claim_excerpt": ctx["LEDGER_CLAIM"],
                                       "verdict": {q["id"]: q["verdict"] for q in all_rows}.get("V-08", "NA")},
                        "mutant_report": mutant_rows,
                        "teeth_coverage": {"armed_rows": armed, "unarmed_rows": unarmed,
                                           "rows_total": len(all_rows),
                                           "note": "无臂行不得当作已被见证"},
                        "carriers": {"constants": {k: {"value": v[0], "line": v[1]} for k, v in CONST.items()},
                                     "files": {"v48_script": V48_PY, "v48_archived_out": V48_OUT,
                                               "v48_report": V48_RPT, "const_file": CONST_FILE,
                                               "s16_ledger": LEDGER, "l11_postwrite_audit": "scratch/_L11_postwrite_audit.py",
                                               "draw_d1": os.path.join(SCRATCH, "draw_d1.txt"),
                                               "draw_d2": os.path.join(SCRATCH, "draw_d2.txt"),
                                               "diff_list": os.path.join(SCRATCH, "archive_vs_draw_diff.txt")}},
                        "red_line": "数学自洽 != 物理成立；判死一条路 != 否证 TUFT 本体；不可复现 != 算错"},
               "results": all_rows}
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)


def dump_scratch(ctx, rows):
    if not os.path.isdir(SCRATCH):
        os.makedirs(SCRATCH)
    for name, txt in (("draw_d1.txt", ctx["d1"]["image"]), ("draw_d2.txt", ctx["d2"]["image"])):
        with open(os.path.join(SCRATCH, name), "w", encoding="utf-8", newline="") as f:
            f.write(txt)
    la, lb = ctx["arc"].split("\n"), ctx["d1"]["image"].split("\n")
    with open(os.path.join(SCRATCH, "archive_vs_draw_diff.txt"), "w", encoding="utf-8", newline="") as f:
        f.write("# 存档图像 vs 本层现抽（draw_d1）逐行差异；行号 1 起\r\n")
        for i in rows:
            f.write("L" + str(i) + "\r\n  ARC  : " + (la[i - 1] if i - 1 < len(la) else "<无>") + "\r\n")
            f.write("  FRESH: " + (lb[i - 1] if i - 1 < len(lb) else "<无>") + "\r\n")


def _declared_keys(name):
    """从**本文件源码**（不是运行时 dict）数出字面声明项。
    dict 会静默吃掉重复键——本轮就在 NEEDLES 上撞过一次（同一块锚点被两次 Edit 各插一遍）。"""
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in node.targets):
            if isinstance(node.value, ast.Dict):
                return [k.value for k in node.value.keys if isinstance(k, ast.Constant)]
            if isinstance(node.value, ast.List):
                return [k.value for k in node.value.elts if isinstance(k, ast.Constant)]
    return None


def static_key_guards():
    ok = True
    for name, runtime in (("NEEDLES", list(NEEDLES.keys())),
                          ("MUT", list(MUT.keys())),
                          ("REP_TOKENS", list(REP_TOKENS))):
        decl = _declared_keys(name)
        if decl is None:
            print("[静态闸] " + name + " 的声明形态没解析出来 ⇒ 该闸空转")
            ok = False
            continue
        if sorted(decl) != sorted(runtime):
            print("[静态闸] " + name + " 声明 " + str(len(decl)) + " 项 vs 运行时 "
                  + str(len(runtime)) + " 项（重复键被 dict 静默吃掉？）"
                  + "；只在声明里的：" + str(sorted(set(decl) - set(runtime)))
                  + "；只在运行时的：" + str(sorted(set(runtime) - set(decl))))
            ok = False
        else:
            print("[静态闸] " + name + " 声明=运行时 " + str(len(runtime)) + " 项（无静默重复）")
    return ok


def main():
    print("=" * 96)
    print("第 ⑪ 层：转动无源定理 + v48 可复现性｜常数与图像全部现读")
    print("=" * 96)
    ctx = {}
    print("=== §V 复现层：现场两次调用 v48（cwd 在临时目录，档案那份不动）===")
    ctx["d1"] = run_v48("d1")
    ctx["d2"] = run_v48("d2")
    arc_img, arc_bytes, arc_crlf = read_pair(V48_OUT)
    ctx["arc"], ctx["ARC_BYTES"], ctx["ARC_CRLF"] = arc_img, arc_bytes, arc_crlf
    ctx["rpt"] = open(V48_RPT, encoding="utf-8").read() if os.path.exists(V48_RPT) else ""
    (ctx["LEDGER_BLOCK"], ctx["LEDGER_PINS"], ctx["LEDGER_SKIPPED"], ctx["LEDGER_CLAIM"],
     ctx["LEDGER_BYTES"], ctx["LEDGER_CRLF"]) = read_ledger_block()
    ctx["LVALS"] = numlist(ctx["LEDGER_BLOCK"])
    ctx["FVALS"] = numlist(ctx["d1"]["image"])
    ctx["AVALS"] = numlist(ctx["arc"])
    print("[现跑] d1 rc=" + str(ctx["d1"]["rc"]) + " 盘上 " + str(ctx["d1"]["bytes"]) + " B、"
          + str(ctx["d1"]["lines"]) + " 行；d2 rc=" + str(ctx["d2"]["rc"]) + " 盘上 "
          + str(ctx["d2"]["bytes"]) + " B；存档（" + os.path.basename(V48_OUT) + "）盘上 "
          + str(arc_bytes) + " B、CRLF " + str(arc_crlf))
    print("[台账] " + os.path.basename(LEDGER) + " 盘上 " + str(ctx["LEDGER_BYTES"])
          + " B、CRLF " + str(ctx["LEDGER_CRLF"]) + "；" + LEDGER_KEY + " 块可比数 "
          + str(len(ctx["LEDGER_PINS"])) + " 枚、被排除 " + str(len(ctx["LEDGER_SKIPPED"]))
          + " 枚：" + "、".join(ctx["LEDGER_SKIPPED"][:10]))

    base = compute(ctx)
    print("")
    for cid, sec, item, stmt, fn in ROWS:
        v, d = base[cid]
        print("[" + v + "] " + cid.ljust(6) + " | " + item.ljust(34) + " | " + d)
        RESULTS.append({"id": cid, "section": sec, "item": item, "statement": stmt,
                        "verdict": v, "detail": d})
    rows = diff_rows(ctx["arc"], ctx["d1"]["image"])
    mv, where = worst_pole_move(poles(ctx["arc"]), poles(ctx["d1"]["image"]))
    v3 = {"rows": len(rows), "nline": len(ctx["arc"].split("\n")), "rowlist": rows,
          "mv": mv, "where": where, "buckets": {}, "off": ctx.get("OFF", [])}
    for t, b in ctx["BUCKET"].items():
        v3["buckets"][b] = v3["buckets"].get(b, 0) + 1
    ctx["NARR"] = narrative_rows(ctx, base)
    for row in ctx["NARR"]:
        print("[" + row[4] + "] " + row[0].ljust(6) + " | " + row[2].ljust(34) + " | " + row[5])
        RESULTS.append({"id": row[0], "section": row[1], "item": row[2], "statement": row[3],
                        "verdict": row[4], "detail": row[5]})
    if mv is None or where is None:
        print("[停手] 旋转极点格点没对上（poles() 在两幅图像里没取到同名格点）——V-02 无从判，不写版面。")
        for d in (ctx["d1"], ctx["d2"]):
            shutil.rmtree(d["tmp"], ignore_errors=True)
        return 3

    print("")
    print("=== §M 变异臂（每臂走 compute() 同一条路）===")
    mutant_rows = []
    for name, (must, must_stay, why) in MUT.items():
        ctx_m = dict(ctx)
        for k in ("DELTA", "RR", "SENSE", "EC", "PR", "GDET", "EDE", "ANCH",
                  "BUCKET", "OFF", "SIX"):
            ctx_m.pop(k, None)
        mvv = compute(ctx_m, mut=name)
        got = sorted(cid for cid in mvv if mvv[cid][0] != base[cid][0])
        stayed_hit = [k for k in must_stay if k in got]
        missed = [k for k in must if k not in got]
        clean = (not missed) and (not stayed_hit)
        mutant_rows.append({"mutant": name, "why": why, "must_redden": must,
                            "must_stay": must_stay, "reddened": got,
                            "extra_reddened": [k for k in got if k not in must],
                            "not_reddened_by_this_mutant": [k for k in must_stay if k in got],
                            "clean": clean})
        print("[牙] " + name.ljust(22) + " 应红 " + ",".join(must) + " 应不红 "
              + (",".join(must_stay) or "<无>") + " 实红 " + (",".join(got) or "<无>")
              + " 同臂未红 " + (",".join(missed) or "<无>") + " => " + ("OK" if clean else "BAD"))
    if not all(m["clean"] for m in mutant_rows):
        print("[牙红] 有变异体未被抓住——版面不写，临时目录清掉，scratch 快照仍留（读数以 stderr 打印为准）。")
        for d in (ctx["d1"], ctx["d2"]):
            shutil.rmtree(d["tmp"], ignore_errors=True)
        return 1

    all_rows = list(RESULTS)
    counts = {}
    for q in all_rows:
        counts[q["verdict"]] = counts.get(q["verdict"], 0) + 1
    armed = sorted({x for v in MUT.values() for x in v[0]})
    unarmed = sorted(set(q["id"] for q in all_rows) - set(armed))
    elapsed = round(time.time() - T_START, 1)
    print("")
    print("=" * 96)
    print("总计 " + str(len(all_rows)) + " 项：" + " ".join(k + "=" + str(v) for k, v in sorted(counts.items())))
    print("[牙账] " + str(len(MUT)) + " 枚变异体覆盖 " + str(len(armed)) + " / " + str(len(all_rows))
          + " 行：" + ",".join(armed))
    print("[牙账] 无变异臂的行（不得当作已被见证）共 " + str(len(unarmed)) + " 行：" + ",".join(unarmed))

    dump_scratch(ctx, rows)
    lines = build_face(ctx, base, counts, mutant_rows, armed, unarmed, elapsed, v3)
    txt = "".join(x + "\r\n" for x in lines)
    with open(MD_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(txt)
    for d in (ctx["d1"], ctx["d2"]):
        shutil.rmtree(d["tmp"], ignore_errors=True)

    face = open(MD_PATH, encoding="utf-8").read()
    leaks = re.findall(r"%[sdifr]|%[0-9]*\.[0-9]+[efd]", face)
    print("[版面闸] 占位符 " + str(len(leaks)) + " 处" + ("（有泄漏 ⇒ 缺陷）" if leaks else "（零泄漏）"))
    renamed = [k for k in NEEDLES if k not in face and md_cell(k) not in face]
    print("[版面闸] " + str(len(NEEDLES) - len(renamed)) + "/" + str(len(NEEDLES))
          + " 个锚点键名在本面可见" + ("；缺 " + ",".join(renamed) if renamed else ""))
    untagged = [q["id"] for q in all_rows if q["id"] not in face]
    print("[版面闸] 判决表编号 " + str(len(all_rows) - len(untagged)) + "/" + str(len(all_rows))
          + " 可在面上找回" + ("；缺 " + ",".join(untagged) if untagged else ""))
    if leaks or renamed or untagged:
        return 2
    if not static_key_guards():
        return 2
    write_json(ctx, all_rows, counts, mutant_rows, armed, unarmed, ctx.get("DELTA"), v3)
    print("已写出：数据/" + STEM + ".md + .json")
    print("登记债：本轮未写 S14 claims.csv 与算法联盟 README.md；S16 的 v48 存档图像**未被本层改动**")
    return 0


RESULTS = []

if __name__ == "__main__":
    sys.exit(main())
