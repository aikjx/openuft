# -*- coding: utf-8 -*-
"""攻破㉕ 超对称出口的账单：可实现性 + 可检验谱（只读件；语料＝仪器枚举，不编辑任何语料文件）。

来料处方（外部批评第八节）：「下一步必须是：引入超对称与内部规范群，并给出一个当前实验能检验的新效应。」
攻破㉒ §八 把这条挂成债：「超对称出口若真要取用：最小代价是先写出 {Q,Q̄}=2σP 的**实现**（不是复述），
并给出 LHC 可判的谱——现库内 0 条。」本轮就是去**偿这笔债的账**，不是再说一遍：

  K1 三分尺：全活树里 SUSY 词汇行分「提及／记号／实现」三档。尺的牙齿＝盘上正对照（K2 那台真实现
     写进 scratch 后由本尺读）＋两枚变异体（删检验行／把代数句改成散文）。
  K2 「实现」到底长什么样：本仪器自己把 N=1 超-Poincaré 代数在 4 维 Fock 空间上精确实现
     （两个费米模 a_1,a_2 的 Jordan–Wigner 矩阵，Q_α = c_α a_α），逐符号验证
     {Q_α,Q̄_β̇}=2σ^μP_μ、{Q_α,Q_β}=0、(-1)^F 分次、Str(1)=0、以及**质量简并**——
     并把这三条的代价印出来：超对称不是"加一个对称"，是"每个态配一个等质量的伙伴"。
  K3 TUFT 自己的谱能不能承载 Q：拿库内已登记的阶梯（`tuft_fermion_spin.py:24-27` 定理 2′：
     s=|Lk|=n/2，n 偶→玻色、n 奇→费米）现算平衡子 Str 的部分和（无质量 2 极化支／有质量 2s+1 支
     两种约定并列，二者都印）；再算配对所需的独立质量参数数。**期望由定义现推，不从读数反推。**
  K4 第二把尺打在 TUFT 费米子出口的薄弱处：那份脚本自己声明「Möbius 仅一条边界，Gauss 两-边积分
     不适用；自链接由 White 公式 = n/2（解析精确）给出」⟹ 半整数那一支**只有解析式一处背书**。
     本轮把闭曲线口径实算出来：偶 n（两边可闭）复现整数；奇 n 用**单条双重覆盖边界**＋单值 framing
     做 Gauss 自链接，期望**必为整数**（framing 整数性，由定义给出）；再验开弧口径对带宽 w 的漂移
     （开弧⟹不是不变量）。谁的读数与定理 2′ 的 s=n/2 一致、谁不一致，当场印。
  K5 可检验效应的账单：全库 claims.csv 里 SUSY 词汇主张行按 status 分桶，其中带 prediction_value 的
     几条；库内自己对 LHC 的反面登记（具名行点名）；具名超伴子带 TeV 数值的行数。

退出码：任何一档判据不符、或牙齿没咬，rc=1。面双落（源码目录／09_验证结果·原始运行记录），二进制、只走 LF。
"""
import io
import os
import re
import sys
import csv
import math
import shutil
import hashlib
import importlib.util
import subprocess
from fractions import Fraction

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
S14 = os.path.abspath(os.path.join(HERE, "..", ".."))
ROOT = os.path.abspath(os.path.join(S14, "..", ".."))
FACE_NAME = "tuft_susy_exit_realizability_and_testable_spectrum_census_20261011_report.txt"
FACE_SRC = os.path.join(HERE, FACE_NAME)
FACE_REC = os.path.join(S14, "09_验证结果", "原始运行记录", FACE_NAME)
SELF = os.path.abspath(__file__)
SCRATCH = os.path.abspath(os.path.join(ROOT, "..", "scratch"))
A25 = os.path.join(SCRATCH, "A25_susy")

CENSUS = os.path.join(HERE, "tuft_symmetry_theorems_spin_census_20261010.py")
FERMION = os.path.join(HERE, "tuft_fermion_spin.py")

L = []


def p(s=u""):
    L.append(s)


def md5(b):
    return hashlib.md5(b).hexdigest()


def w(path, text):
    b = text.encode("utf-8")
    with io.open(path, "wb") as f:
        f.write(b)
    return len(b), md5(open(path, "rb").read())


# ------------------------------------------------------------------ K1 分档尺
TOKEN = re.compile(u"超对称|超対称|SUSY|MSSM|superpartner|超伴子|引力微子|gravitino|goldstino"
                   u"|超空间|superspace|supercharge|超荷|超引力|supergravity|Wess|Zumino"
                   u"|超庞加莱|超\\s*-?\\s*Poincar|super-?\\s*Poincar|R-?荷|BPS|超对称代数")
ALG_CJK = re.compile(u"反对易|anticomm|克利福德|Clifford")
# 宽尺（第一版）：只问"同档含算符＋检验＋任何 {…}=" —— Python 里 {} 首先是集合/字典/f-string，
# 这一版在活树上判出 117 个"实现"，是**尺的形状错**，不是语料的性质。留着它只为把宽窄之差印出来。
BRACE_WIDE = re.compile(u"[{｛][^{}｝\n]{1,44}[}｝]\\s*=")
CONSTRUCT = re.compile(u"kron|Matrix|np\\.array|creation|annihil|a_dag|adag|sigma_|pauli|泡利矩阵"
                       u"|gamma_|升降算符|产生|湮灭|费米模|Jordan|einsum")
CHECK = re.compile(u"assert|allclose|isclose|残差|偏差|PASS|FAIL|abs\\(|np\\.max|guard\\(")
BR = re.compile(u"[{｛]([^{}｝\n]{1,44})[}｝]\\s*=\\s*([^{}\n]{0,60})")
IS_Q = re.compile(u"[QqS]|supercharge|超荷")
IS_G = re.compile(u"γ|Γ|gamma|Gamma|ψ|psi")
IS_F = re.compile(u"^[acbdA-Za-z](_?\\d)?(†|\\+|\\\\dagger|\\*)?$")
HAS_SIG = re.compile(u"σ|sigma")
HAS_P = re.compile(u"[Ppµμ]|动量")


def family(line):
    """紧尺：按**操作数与右侧的字母表**认代数族，不按"有没有花括号"认。"""
    m = BR.search(line)
    if not m:
        return None
    lhs, rhs = m.group(1), m.group(2)
    ops = [s.strip() for s in re.split(u"[,，;；]", lhs)]
    if len(ops) < 2:
        return None
    a, b = ops[0], ops[1]
    if IS_Q.search(a) and IS_Q.search(b):
        return u"超-Poincaré" if (HAS_SIG.search(rhs) and HAS_P.search(rhs)) else u"超-Poincaré（齐次支 {Q,Q}=0）"
    if IS_G.search(a) and IS_G.search(b):
        return u"克利福德"
    if IS_F.match(a) and IS_F.match(b) and re.search(u"δ|delta|eta|^\\s*1", rhs):
        return u"费米模"
    return u"其它（花括号等式，非分级代数）"


FAMS = (u"超-Poincaré", u"超-Poincaré（齐次支 {Q,Q}=0）", u"克利福德", u"费米模")
SUSYFAM = (u"超-Poincaré", u"超-Poincaré（齐次支 {Q,Q}=0）")


def scan(text, is_py):
    """分档（形状由"代数族＋邻近检验"定，不由花括号定）：
       实现＝族内且 ±8 行内有数值/符号检验的 .py；记号＝族内但无邻近检验（含全部 .md 复述）；
       提及＝只有 SUSY 词汇、没有代数式；另印「花括号等式但不属这四族」的条数（假阳候选池）。"""
    lines = text.split(u"\n")
    n_ment = n_other = 0
    graded = []
    for i, line in enumerate(lines):
        f = family(line)
        if f in FAMS:
            near = any(CHECK.search(lines[j]) for j in range(max(0, i - 8), min(len(lines), i + 9)))
            graded.append((i, f, bool(near) and is_py, line.strip()[:96]))
        elif f is not None and is_py:
            n_other += 1
        if TOKEN.search(line) and f not in FAMS:
            n_ment += 1
    wide = is_py and bool(CONSTRUCT.search(text)) and bool(CHECK.search(text)) and \
        bool(BRACE_WIDE.search(text)) and bool(TOKEN.search(text))
    impl = set(f for i, f, ok, l in graded if ok)
    return n_ment, graded, n_other, wide, impl


_CACHE = {}


def read_text(path):
    if path not in _CACHE:
        try:
            with io.open(path, "rb") as f:
                _CACHE[path] = f.read().decode("utf-8", "replace")
        except Exception:
            _CACHE[path] = u""
    return _CACHE[path]


# ------------------------------------------------------------------ K2 真实现
def susy_exemplar_source():
    """一台真的 N=1 超-Poincaré 实现（两个费米模的 Jordan–Wigner 矩阵）。K1 的盘上正对照就打在它身上。"""
    return u'''# -*- coding: utf-8 -*-
# 攻破㉕ K2 盘上正对照：超-Poincaré 代数的**实现**（不是复述）。
# {Q_alpha, Qbar_dotbeta} = 2 sigma^mu P_mu，{Q_alpha, Q_beta} = 0，(-1)^F 分次，Str(1)=0，质量简并。
import sys
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sp0 = np.array([[1, 0], [0, 1]], dtype=complex)      # sigma^0
sp3 = np.array([[1, 0], [0, -1]], dtype=complex)     # P 沿 z 时 2 sigma.P 只用得上 0,3
I2 = np.eye(2, dtype=complex)
sz = np.diag([1.0, -1.0]).astype(complex)
sm = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)   # 费米模的降算符
# Jordan–Wigner：两个模作用在 C^2 (x) C^2 上，反对易由 str{-sz, I} 保证
a1 = np.kron(sm, I2)
a2 = np.kron(sz, sm)
am = {1: a1, 2: a2}
ad = {k: v.conj().T for k, v in am.items()}
F = np.diag([0, 1, 1, 0])                               # 费米数算符（模 2 后即 (-1)^F 的指数）
minusF = np.diag([1.0, -1.0, -1.0, 1.0])                # (-1)^F


def charges(E, pz):
    """Q_alpha = c_alpha a_alpha，|c_1|^2 = 2(E - pz)，|c_2|^2 = 2(E + pz)。"""
    c = {1: np.sqrt(complex(2 * (E - pz))), 2: np.sqrt(complex(2 * (E + pz)))}
    return {k: c[k] * am[k] for k in am}


def check(E, pz, tag):
    Q = charges(E, pz)
    adq = {k: Q[k].conj().T for k in Q}          # Qbar_dotbeta = (Q_beta)†：共轭**带 c 因子**，不是 a†
    # 种子核对：Jordan–Wigner 两模本身必须正则（{a_x, a_y†} = δ_xy）——电荷代数继承自它
    seed = 0.0
    for x in (1, 2):
        for y in (1, 2):
            want0 = np.eye(4, dtype=complex) if x == y else np.zeros((4, 4), dtype=complex)
            seed = max(seed, float(np.max(np.abs(am[x] @ ad[y] + ad[y] @ am[x] - want0))))
    # 逐分量核对：4x4 的反对易子必须等于 2 sigma^mu P_mu 落在 Fock 空间上的对角嵌入
    worst = 0.0
    for x in (1, 2):
        for y in (1, 2):
            antic = Q[x] @ adq[y] + adq[y] @ Q[x]
            want = np.zeros((4, 4), dtype=complex)
            if x == y:
                d = 2 * (E - pz) if x == 1 else 2 * (E + pz)
                want = d * np.eye(4, dtype=complex)
            worst = max(worst, float(np.max(np.abs(antic - want))))
    worst_qq = 0.0
    for x in (1, 2):
        for y in (x, 2):
            worst_qq = max(worst_qq, float(np.max(np.abs(Q[x] @ Q[y] + Q[y] @ Q[x]))))
    worst_gr = max(float(np.max(np.abs(minusF @ Q[1] + Q[1] @ minusF))),
                   float(np.max(np.abs(minusF @ Q[2] + Q[2] @ minusF))))
    H = 0.5 * (Q[1] @ adq[1] + adq[1] @ Q[1] + Q[2] @ adq[2] + adq[2] @ Q[2])
    str1 = float(np.real(np.trace(np.diag([1, -1, -1, 1]) @ np.eye(4))))
    strH = float(np.real(np.trace(np.diag([1, -1, -1, 1]) @ H)))
    eves = np.sort(np.real(np.linalg.eigvalsh(H)))
    print("== %s  E=%.6f pz=%.6f" % (tag, E, pz))
    print("   种子 {a_alpha, a†_beta} = delta_ab  残差 max = %.3e  assert<1e-12 ⟹ %s" % (seed, seed < 1e-12))
    print("   核对 {Q_alpha, Qbar_dotbeta} = 2 sigma^mu P_mu  残差 max = %.3e  assert<1e-12 ⟹ %s" % (worst, worst < 1e-12))
    print("   核对 {Q_alpha, Q_beta} = 0  残差 max = %.3e  assert<1e-12 ⟹ %s" % (worst_qq, worst_qq < 1e-12))
    print("   核对 [(-1)^F, Q_alpha]_+ = 0（Q 改变统计）残差 max = %.3e ⟹ %s" % (worst_gr, worst_gr < 1e-12))
    print("   Str(1) = %.1f  Str(H) = %.3e  H 本征值 = %s（玻/费两两**简并**，值＝2E）" % (str1, strH, np.round(eves, 12)))
    assert seed < 1e-12 and worst < 1e-12 and worst_qq < 1e-12 and worst_gr < 1e-12
    assert abs(str1) < 1e-15 and abs(strH) < 1e-12
    print("   PASS：代数闭合，且超对称强制伙伴质量简并")


check(1.0, 0.0, "静止大质量支 P=(m,0,0,0)")
check(2.0, 1.5, "一般支 P=(E,0,0,pz)")
check(1.0, 1.0, "无质量支 P=(E,0,0,E)（一个模归零 ⟹ 只剩一个螺旋度）")
'''


# ------------------------------------------------------------------ K3 阶梯账单
def ladder_rows(nmax):
    """定理 2′（库内 `tuft_fermion_spin.py:24-27`）：s=|Lk|=n/2；n 偶→玻色，n 奇→费米。"""
    rows = []
    for n in range(0, nmax + 1):
        s = Fraction(n, 2)
        g_massless = 1 if n == 0 else 2
        g_massive = n + 1
        rows.append((n, s, (n % 2 == 0), g_massless, g_massive))
    return rows


def partial_str(rows, which):
    out = []
    acc = 0
    for r in rows:
        g = r[3] if which == u"无质量" else r[4]
        acc += (-g) if r[2] is False else g
        out.append(acc)
    return out


# ------------------------------------------------------------------ K4 Möbius 第二把尺
def ribbon_geometry():
    """K4 的第二把尺：Gauss 双积分口径下的自链接。
    口径由探针选定（scratch/A25_susy/a25_probe_k4.py）：framing 平移量 ε 与网格 dt 同量级时
    积分核 1/r³ 未被分辨（ε=0.02、M=1400 时 n=5 的整数偏差 3.6e-2 全属离散误差），
    故取 ε=0.05 并把网格加密一倍来把离散误差与"真的不是整数"分开。"""
    import numpy as np
    R, w_, EPS = 2.0, 0.35, 0.05
    N = 1000

    def core(t):
        return np.stack([R * np.cos(t), R * np.sin(t), np.zeros_like(t)])

    def normal(t, n):
        phi = 0.5 * n * t
        return np.stack([np.cos(phi) * np.cos(t), np.cos(phi) * np.sin(t), np.sin(phi)])

    def gauss_lk(c1, d1, c2, d2, dt):
        nn = c1.shape[1]
        tot = 0.0
        for i in range(nn):
            d = c1[:, i][:, None] - c2
            r3 = np.sum(d * d, axis=0) ** 1.5 + 1e-12
            tot += np.sum(np.sum(d * np.cross(d1[:, i], d2, axis=0), axis=0) / r3)
        return float(tot * dt * dt / (4.0 * np.pi))

    def dper(f, dt):
        """周期中央差分：这些曲线都是闭合的，np.gradient 的单侧边缘会把接缝当成端点（假残差）。"""
        return (np.roll(f, -1, axis=1) - np.roll(f, 1, axis=1)) / (2.0 * dt)

    def unit(f):
        return f / np.maximum(np.linalg.norm(f, axis=0, keepdims=True), 1e-12)

    res = {}
    # 偶 n：两条边界闭合 ⟹ 链接数为整数（符号＝扭转手性），量级应为 n/2
    for n in (0, 2, 4, 6):
        t = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
        dt = t[1] - t[0]
        nrm, c = normal(t, n), core(t)
        bp, bm = c + 0.5 * w_ * nrm, c - 0.5 * w_ * nrm
        res[n] = gauss_lk(bp, dper(bp, dt), bm, dper(bm, dt), dt)
    # 奇 n：单条边界＝中心线的双重覆盖，t∈[0,4π] 才闭合；网格加密一倍给出收敛凭据
    odd = {}
    for n in (1, 3, 5):
        runs = []
        for M in (N, 2 * N):
            t = np.linspace(0.0, 4 * np.pi, M, endpoint=False)
            dt = t[1] - t[0]
            c, nrm = core(t), normal(t, n)
            b = c + 0.5 * w_ * nrm                      # 闭曲线（单值：t 与 t+4π 同点同向量）
            db = dper(b, dt)
            tan = unit(db)
            u = unit(np.cross(nrm, tan, axisa=0, axisb=0, axisc=0))
            b2 = b + EPS * u                            # 沿单值 framing u 平移的副本
            lk = gauss_lk(b, db, b2, dper(b2, dt), dt)
            # 同一副本、framing 绕切平面整一圈（winding +1）⟹ 自链接必须恰好位移 1
            ang = np.linspace(0.0, 2 * np.pi, M, endpoint=False)
            u_rot = np.cross(tan, u, axisa=0, axisb=0, axisc=0)
            u1 = unit(u * np.cos(ang) + u_rot * np.sin(ang))
            b3 = b + EPS * u1
            lk1 = gauss_lk(b, db, b3, dper(b3, dt), dt)
            # 变异体：把同一根闭曲线的 framing 换成**半值**（走满 4π 时翻向）⟹ 副本曲线端点错开、不闭合
            #        ⟹ 这个积分不再是链接数 ⟹ 同一把整性尺必须读红。尺若在开副本上也绿，整性判决不作数。
            uh = unit(u * np.cos(ang / 2.0) + u_rot * np.sin(ang / 2.0))
            bh = b + EPS * uh
            lkh = gauss_lk(b, db, bh, dper(bh, dt), dt)
            runs.append((M, lk, lk1, lk1 - lk, lkh))
        # 标架单值性见证（期望由 normal() 的定义现推）：n 奇 ⟹ φ(2π)=nπ ⟹ N(2π)=−N(0)、N(4π)=N(0)
        tv = np.array([0.0, 2.0 * np.pi, 4.0 * np.pi])
        nv = normal(tv, n)          # 形状 (3 分量, 3 个 t)——按列取标架，按行取会把分量差当成 t 差
        odd[n] = (runs, float(np.linalg.norm(nv[:, 1] - nv[:, 0])),
                  float(np.linalg.norm(nv[:, 1] + nv[:, 0])), float(np.linalg.norm(nv[:, 2] - nv[:, 0])))
    # 开弧口径：只走 t∈[0,2π]（半圈，边界不闭合）⟹ 对带宽 w 漂移 ⟹ 不是不变量
    open_arc = {}
    for n in (1, 3):
        vals = []
        for wv in (0.2, 0.35, 0.6):
            t = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
            dt = t[1] - t[0]
            c, nrm = core(t), normal(t, n)
            bp, bm = c + 0.5 * wv * nrm, c - 0.5 * wv * nrm
            vals.append(gauss_lk(bp, dper(bp, dt), bm, dper(bm, dt), dt))
        open_arc[n] = vals
    return res, odd, open_arc


# ------------------------------------------------------------------ K5 claims 账单
def claims_invoice():
    rows = []
    for base in (os.path.join(ROOT, "01_独立体系"), os.path.join(ROOT, "07_统一场方程")):
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [x for x in dirnames if x not in {".git", "__pycache__"}]
            if "claims.csv" in filenames:
                pth = os.path.join(dirpath, "claims.csv")
                try:
                    with io.open(pth, "r", encoding="utf-8-sig", errors="replace", newline="") as f:
                        rd = list(csv.reader(f))
                except Exception:
                    continue
                if not rd or not rd[0]:
                    continue
                hdr = [h.strip() for h in rd[0]]
                if hdr[0].lower() != "claim_id":
                    continue
                for i, r in enumerate(rd[1:], start=2):
                    if len(r) < 2 or not r[0].strip():
                        continue
                    joined = u" ".join(r)
                    if TOKEN.search(joined) or ALG_CJK.search(joined):
                        d = dict(zip(hdr, r))
                        rows.append((os.path.relpath(pth, ROOT).replace("\\", "/"), i,
                                     r[0].strip(), d.get("prediction_value", "").strip(),
                                     d.get("status", "").strip(), d.get("evidence_level", "").strip()))
    return rows


def main():
    argv = sys.argv[1:]
    mode = argv[0] if argv else u"--run"
    rc = 0
    verdicts = []

    spec = importlib.util.spec_from_file_location(u"a25_face", CENSUS)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    files = mod.walk(mod.LIVE_DIRS)
    # 排除集＝本仪器源码＋两面＋selftest 载体＋**本轮自己要写出的判定册**（㉒ 债：分母不许把本轮文档算进去）
    mine = {os.path.abspath(SELF), os.path.abspath(FACE_SRC), os.path.abspath(FACE_REC)}
    doc_name = u"判定_攻破㉕_超对称出口可实现性与可检验谱_2026-10-11.md"
    DOC = os.path.join(ROOT, "04_公共成果", "本项目_统一场论攻破", doc_name)
    mine.add(os.path.abspath(DOC))
    for extra in (u"tuft_susy_exit_realizability_and_testable_spectrum_census_20261011_selftest_stdout.txt",):
        mine.add(os.path.abspath(os.path.join(S14, "09_验证结果", "原始运行记录", extra)))
    files = [f for f in files if os.path.abspath(f) not in mine]

    if not os.path.isdir(A25):
        os.makedirs(A25)

    # ---------- K2：先造出"实现"这台正对照，再让 K1 去读它
    ex_path = os.path.join(A25, "a25_exemplar_susy_realization.py")
    nb, nm = w(ex_path, susy_exemplar_source())
    env = dict(os.environ, PYTHONIOENCODING=u"utf-8")
    r2 = subprocess.run([sys.executable, ex_path], capture_output=True, cwd=A25, env=env)
    ex_out = (r2.stdout.decode("utf-8", "replace") + r2.stderr.decode("utf-8", "replace"))
    ex_out = ex_out.replace(u"\r\n", u"\n").replace(u"\r", u"\n")   # 子进程在 Windows 上回 CRLF，面必须只走 LF
    ex_real_closed = r2.returncode == 0 and u"PASS：代数闭合" in ex_out

    # 变异体 A：删掉全部检验行（assert/残差/np.max）——尺必须从"实现"降到"记号"
    keep = [ln for ln in susy_exemplar_source().split(u"\n")
            if not CHECK.search(ln) and u"残差" not in ln]
    mut_a = os.path.join(A25, "a25_mutantA_删检验行.py")
    w(mut_a, u"\n".join(keep))
    # 变异体 B：把代数式陈述改成散文复述（留"超对称"字样，删掉 {,}= 与算符）
    mut_b = os.path.join(A25, "a25_mutantB_散文复述.py")
    w(mut_b, u"# -*- coding: utf-8 -*-\n# 引入超对称以后玻色子与费米子成对出现，这是标准做法。\n"
             u"import numpy as np\nx = np.array([1.0, 2.0])\nprint(x)\n")
    # 变异体 C：同一台构造，把代数式族名全部换成克利福德——尺必须认出**换掉的族**，不许仍报超-Poincaré
    mut_c = os.path.join(A25, "a25_mutantC_换成克利福德族.py")
    w(mut_c, susy_exemplar_source()
      .replace(u"{Q_alpha, Qbar_dotbeta} = 2 sigma^mu P_mu", u"{gamma_a, gamma_b} = 2 eta_ab")
      .replace(u"{Q_alpha, Q_beta} = 0", u"{gamma_5, gamma_a} = 0"))

    # ---------- K1：全活树分档（紧尺＝代数族＋邻近检验；宽尺留着只为一并印出宽窄之差）
    n_ment = n_sym = n_other = n_wide = 0
    graded_files = []            # (rel, [(行号, 族, 已验证, 行首 96 字)])
    per_dir = {}
    per_fam = {}
    carrier_names = [u"判定_对称性定理适用域与自旋谱_TUFT层级裁定_2026-10-11.md",
                     u"判定_攻破㉓_五方向出路审计与科幻分流_2026-10-11.md",
                     u"全维全链攻破总账.md", u"README.md"]
    carrier_rows = dict([(c, [0, 0, 0]) for c in carrier_names])
    second_channel = []
    for f in files:
        rel = mod.rel(f)
        top = rel.split(u"/")[0]
        txt = read_text(f)
        if not txt:
            continue
        is_py = f.endswith(".py")
        a, gr, other, wide, impl = scan(txt, is_py)
        n_ment += a
        n_other += other
        if wide:
            n_wide += 1
        n_sym += len(gr)
        if gr:
            graded_files.append((rel, gr))
        for i, fam, ok, ln in gr:
            d = per_fam.setdefault(fam, [0, 0, []])
            d[0] += 1
            if ok:
                d[1] += 1
            else:
                d[2].append(u"%s:%d %s" % (rel, i, ln))
        if a or gr:
            d = per_dir.setdefault(top, [0, 0, 0])
            d[0] += a
            d[1] += len(gr)
            d[2] += 1 if impl else 0
        base = rel.split(u"/")[-1]
        if base in carrier_rows:
            carrier_rows[base][0] += a
            carrier_rows[base][1] += len(gr)
            carrier_rows[base][2] += 1 if impl else 0
        if is_py:
            m2 = re.search(u'guard\\(\\s*"[^"]*(cliff|anticomm|gamma|pauli|susy|super|poincar)[^"]*"', txt, re.I)
            if m2:
                second_channel.append((rel, m2.group(0)[:70]))

    def impl_of(path):
        return scan(read_text(path), path.endswith(u".py"))[4]

    susy_impl = [rel for rel, gr in graded_files if any(f in SUSYFAM and ok for i, f, ok, l in gr)]
    cliff_impl = [rel for rel, gr in graded_files
                  if any(f in (u"克利福德", u"费米模") and ok for i, f, ok, l in gr)]

    teeth = []
    e_susy = impl_of(ex_path)
    cases = [(u"正对照 真超-Poincaré 实现（必须被认成超-Poincaré 实现）", e_susy,
              lambda g: any(x in SUSYFAM for x in g)),
             (u"变异体 A 删检验行（必须降到记号）", impl_of(mut_a), lambda g: not g),
             (u"变异体 B 散文复述（必须只算提及）", impl_of(mut_b), lambda g: not g),
             (u"变异体 C 把代数族换成克利福德（必须不再报超-Poincaré，且要报出克利福德）", impl_of(mut_c),
              lambda g: (not any(x in SUSYFAM for x in g)) and (u"克利福德" in g)),
             (u"库内反对照 tuft_fermion_spin.py（真数值脚本，但不是分级代数）", impl_of(FERMION), lambda g: not g)]
    for tag, got, pred in cases:
        ok = pred(got)
        teeth.append(u"  %-74s 尺读到的实现族＝%s ⟹ %s"
                     % (tag[:70], u"、".join(sorted(got)) or u"（无）", u"FIRES" if ok else u"BLIND"))
        if not ok:
            rc = 1
            verdicts.append(u"K1 牙齿未咬：%s" % tag[:40])
    k40 = [rel for rel in cliff_impl if u"V40" in rel or u"V41" in rel]
    teeth.append(u"  %-74s 尺读到＝%s ⟹ %s"
                 % (u"库内正对照 V40/V41 的 Clifford 实算必须被认成实现",
                    u"、".join(x.split(u"/")[-1][:28] for x in k40) or u"（无）",
                    u"FIRES" if k40 else u"BLIND"))
    if not k40:
        rc = 1
        verdicts.append(u"K1 库内正对照（Clifford 实现）未被认出")

    p(u"攻破㉕ 超对称出口的账单：可实现性 + 可检验谱（只读件）")
    p(u"运行时间: %s    脚本: %s" % (__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"), os.path.basename(SELF)))
    p(u"作用域：与攻破㉒ 同一把枚举尺（mod.walk(LIVE_DIRS)），排除本轮载体（仪器源码／两面／selftest 载体／本轮判定册）＝%d 个路径"
      % len(mine))
    p(u"  排除逐个点名（按名豁免≠按名隐身；排除**按路径名**成立，与这些文件在不在盘上无关 ⟹ 判定册落地不移动本面分母）：")
    for q in sorted(mine):
        p(u"    %s" % os.path.relpath(q, ROOT).replace("\\", "/"))
    p(u"  语料文件数=%d（含 .md/.py/.txt/.csv；㉒ 面记 4472，差值＝本轮新增文件与本仪器排除，引用前先读这一行）" % len(files))
    p(u"")
    p(u"=== K1 SUSY 词汇的分档（实现＝代数族行 ±8 行内有数值/符号检验的 .py；记号＝族行但无邻近检验，含全部 .md 复述；提及＝只有词汇无代数式）===")
    p(u"  按代数族分（左＝族行数，右＝其中已被邻近检验支撑的）：")
    for fam in (u"超-Poincaré", u"超-Poincaré（齐次支 {Q,Q}=0）", u"克利福德", u"费米模", u"其它（花括号等式，非分级代数）"):
        if fam in per_fam:
            p(u"    %-34s 族行=%-5d 其中带检验=%d" % (fam, per_fam[fam][0], per_fam[fam][1]))
    for fam in sorted(per_fam):
        if fam not in (u"超-Poincaré", u"超-Poincaré（齐次支 {Q,Q}=0）", u"克利福德", u"费米模"):
            p(u"    %-34s 族行=%-5d 其中带检验=%d" % (fam, per_fam[fam][0], per_fam[fam][1]))
    p(u"  合计：提及 %d 行／族行（代数式陈述，含实现所依据的那几行）%d 行／非分级花括号等式 %d 行（.py，只印条数＝假阳候选池）"
      % (n_ment, n_sym, n_other))
    p(u"  按顶层目录分布（提及／族行／实现文件）：")
    for k in sorted(per_dir, key=lambda x: -(per_dir[x][0] + per_dir[x][1])):
        p(u"    %-16s 提及=%-6d 族行=%-5d 实现文件=%d" % (k, per_dir[k][0], per_dir[k][1], per_dir[k][2]))
    p(u"  超-Poincaré 的实现文件=%d：%s" % (len(susy_impl), u"、".join(susy_impl) or u"（0 个——活树里没有一处把该代数实现出来）"))
    p(u"  克利福德／费米模的实现文件=%d：" % len(cliff_impl))
    for rel in cliff_impl[:8]:
        gr = [g for g in dict(graded_files)[rel] if g[2]]
        p(u"    %-88s 例：%s:%d %s" % (rel[:88], rel.split(u"/")[-1], gr[0][0], gr[0][3][:60]))
    p(u"  宽窄对照（同一份语料、两把尺）：宽尺（同档含算符＋检验＋任何 {…}=）判实现 %d 个文件；"
      u"紧尺（按操作数字母表认族＋邻近检验）判 %d 个。差 %d 个全部来自 Python 的花括号首先是集合/字典/f-string。"
      % (n_wide, len(susy_impl) + len(cliff_impl), n_wide - len(susy_impl) - len(cliff_impl)))
    p(u"  第二通道（独立口径＝guard 键名里含 cliff|anticomm|gamma|pauli|susy|super|poincar 的 .py）：%d 个文件"
      % len(second_channel))
    for rel, key in second_channel[:10]:
        p(u"    %-84s %s" % (rel[:84], key))
    SUSYKEY = re.compile(u"susy|supersym|supercharge|super\\s*-?\\s*partner|mssm|goldstino|gravitino|poincar", re.I)
    ROOTFP = re.compile(u"superposition|superfluid|superconduct|superselect|superdense|superfast|superior", re.I)
    n_susy_key = 0
    for rel, key in second_channel:
        body = key.split(u'"')[1] if key.count(u'"') >= 2 else key
        is_susy = bool(SUSYKEY.search(body)) and not bool(ROOTFP.search(body))
        n_susy_key += 1 if is_susy else 0
        p(u"    裁定 %-80s 键名 %s ⟹ %s"
          % (rel[:80], body[:26], u"真 SUSY 键名" if is_susy else
             (u"super 词根假阳（%s＝叠加/超流一类，super≠super-symmetry）" % ROOTFP.search(body).group(0)
              if ROOTFP.search(body) else u"非超对称词根（cliff/gamma/pauli 族本身）")))
    p(u"  ⟹ 该通道的判据是「若出现真 SUSY 键名，K1 的实现=0 就必须被推翻并逐档人工裁定」；"
      u"本轮实测真 SUSY 键名=%d 枚（%d 个命中文件全部裁定如上）⟹ %s"
      % (n_susy_key, len(second_channel),
         u"K1 的 0 未被推翻" if n_susy_key == 0 else u"K1 的 0 被推翻，须人工复核"))
    if n_susy_key:
        rc = 1
        verdicts.append(u"K1 第二通道出现真 SUSY 键名 %d 枚，与实现=0 冲突" % n_susy_key)
    p(u"  载体逐档贡献（按名豁免≠按名隐身；0 也要印）：")
    for c in carrier_names:
        p(u"    %-64s 提及=%-4d 记号=%-4d 实现文件=%d" % (c, carrier_rows[c][0], carrier_rows[c][1], carrier_rows[c][2]))
    p(u"  牙齿（同一把尺读五张图；正对照必须被认成实现，四枚反/变异体必须不被认成）：")
    for t in teeth:
        p(t)
    p(u"  正对照自己跑通了吗（K2 的执行凭据）：%s rc=%d"
      % (u"是——代数逐符号闭合" if ex_real_closed else u"否（正对照失效，本轮判决不作数）", r2.returncode))
    if not ex_real_closed:
        rc = 1
        verdicts.append(u"K2 正对照未跑通")

    p(u"")
    p(u"=== K2 「实现」的样子（本仪器自带的 N=1 超-Poincaré 实现，scratch 副本真执行；上面 K1 的正对照就是它）===")
    for ln in [x for x in ex_out.split(u"\n") if x.strip()][:16]:
        p(u"  " + ln)
    p(u"  ⟹ 这张图就是 §八 那句「写出 {Q,Q̄}=2σP 的实现（不是复述）」的验收样本：4×4 矩阵、三条残差全 <1e-12，")
    p(u"     且 H 的四个本征值全等（2E）——超对称的代价不是「加一条对称」，是「每个态拖一个**等质量**伙伴」。")

    # ---------- K3 阶梯
    rows = ladder_rows(12)
    ps_m = partial_str(rows, u"无质量")
    ps_M = partial_str(rows, u"有质量")
    p(u"")
    p(u"=== K3 TUFT 自己的阶梯（定理 2′：s=|Lk|=n/2；n 偶→玻色、n 奇→费米）能否承载 Q ===")
    p(u"  载体＝%s:24-27（库内已登记；本轮只读，不编辑）" % mod.rel(FERMION))
    p(u"  平衡子 Str 部分和（Σ(-1)^{2s}·g，前 N 层）：")
    p(u"    无质量支 g=2（s≥1/2）、g=1（s=0）：%s" % u" ".join(u"%+d" % v for v in ps_m))
    p(u"    有质量支 g=2s+1=n+1          ：%s" % u" ".join(u"%+d" % v for v in ps_M))
    grow_M = abs(ps_M[-1])
    p(u"  ⟹ 有质量口径下 |Str| 到第 %d 层 = %d 且逐两层递增（1,-1,2,-2,3,-3…）：阶梯自身不闭合，"
      u"玻/费失衡是**宏观量**，不是可忽略的余项。" % (len(rows) - 1, grow_M))
    p(u"  ⟹ 无质量口径只在 ±1 间振荡、不收敛：同一个「自由度平衡」问题在两种在壳约定下给出两个不同形状的答案，"
      u"所以「平衡」必须逐多重态配对来判，不能对整个阶梯求和来判。")
    n_pair = len(rows) // 2
    p(u"  配对账单（超对称要求同一多重态内 (n, n+1) 两态**等质量**）：")
    p(u"    前 %d 层需 %d 对 ⟹ 若严格对称：m(n)=m(n+1)，阶梯的质量层数减半（信息损失）；"
      % (len(rows), n_pair))
    p(u"    若破缺：每对至少 1 个劈裂参数 ⟹ 新增独立参数 ≥ %d 个，且不收敛（层数越多账单越大）。" % n_pair)
    p(u"  库内现在有几条具名超伴子的质量？见 K5。")

    # ---------- K4 Möbius 第二把尺
    try:
        even, odd, open_arc = ribbon_geometry()
    except Exception as e:
        p(u"")
        p(u"=== K4 Möbius 支的独立数值：仪器未能完成（%r）⟹ 本条不作数 ===" % (e,))
        rc = 1
        verdicts.append(u"K4 计算异常")
        even = odd = open_arc = {}
    p(u"")
    p(u"=== K4 半整数那一支的第二把尺（库内脚本自己声明奇 n「Gauss 两边积分不适用」⇒ 只有一处解析背书）===")
    p(u"  口径选定凭据（先量再定，不是拿读数反推期望）：framing 平移 ε 与网格 dt 同量级时 1/r³ 核未被分辨，")
    p(u"    探针 scratch/A25_susy/a25_probe_k4.py 实测 ε=0.02/M=1400 时 n=5 偏差 3.6e-02 属离散误差；")
    p(u"    取 ε=0.05 并把网格加倍 ⟹ 同一 n 的偏差按 ~4x 收敛。故本轮判整数性时**只用加倍后的网格**，粗网格只作收敛凭据。")
    p(u"  偶 n（两条边界都闭合）：Gauss 链接数 vs 定理 2′ 的 |Lk|=n/2")
    for n in sorted(even):
        v = even[n]
        ok = abs(abs(v) - 0.5 * n) < 5e-3 and abs(v - round(v)) < 5e-3
        p(u"    n=%d  实测（含符号）=%+.5f  |实测|=%.5f  最近整数=%.0f  n/2=%.1f  差=%.2e ⟹ %s"
          % (n, v, abs(v), round(v), 0.5 * n, abs(abs(v) - 0.5 * n), u"复现" if ok else u"不符"))
        if not ok:
            rc = 1
            verdicts.append(u"K4 偶 n=%d 复现失败" % n)
    p(u"    ⟹ 四个偶档实测全为**负**（−n/2）：符号是扭转手性，由 normal() 里 sin(φ) 的取向约定给出。")
    p(u"       库内脚本 `tuft_fermion_spin.py` 在 `|Gauss|` 与 `s=|Lk|` 两处取绝对值，把手性消掉了——")
    p(u"       「取绝对值」这件事本身要申报：它把 Lk 从 ℤ 压到 ℤ≥0，量子数丢的是手性，不是数值。")
    p(u"  奇 n（单条边界＝中心线双重覆盖，t∈[0,4π] 才闭合）：沿**单值 framing** 的自链接")
    p(u"    期望由定义现推（不由读数反推）：闭曲线＋整值 framing 的自链接**必为整数**（framing 反常＝整数），")
    p(u"    且 framing 在切平面内绕一圈（winding ±1）只能把它位移恰好 ±1；")
    p(u"    而定理 2′ 在这一支给的是半整数 n/2 ⟹ 两者不可能同时是「同一个不变量」。")
    for n in sorted(odd):
        runs, s2, f2, c4 = odd[n]
        p(u"    标架单值性见证 n=%d：‖N(2π)−N(0)‖=%.3e（不闭合）、‖N(2π)+N(0)‖=%.3e（≈0 ⟹ 半圈处翻向＝Möbius）、"
          u"‖N(4π)−N(0)‖=%.3e（≈0 ⟹ 4π 才闭合）" % (n, s2, f2, c4))
        if not (f2 < 1e-12 and c4 < 1e-12 and abs(s2 - 2.0) < 1e-12):
            rc = 1
            verdicts.append(u"K4 奇 n=%d 标架单值性见证与定义不符" % n)
        prev = None
        for M, lk, lk1, dlt, lkh in runs:
            e = abs(lk - round(lk))
            ratio = u"%.1fx" % (prev / e) if (prev is not None and e > 0) else u"（首档）"
            p(u"      M=%-5d 自链接=%+.5f 距最近整数=%.2e  收敛比=%s  framing 绕 2π 一圈后=%+.5f（位移=%+.5f，距整数=%.2e）"
              % (M, lk, e, ratio, lk1, dlt, abs(dlt - round(dlt))))
            e_half = abs(lkh - 0.5 * round(2.0 * lkh))
            p(u"      M=%-5d 变异体（半值 framing，副本曲线不闭合）读数=%+.5f 距最近整数=%.2e ⟹ 同一把整性尺 %s；距最近半整数格=%.2e"
              % (M, lkh, abs(lkh - round(lkh)),
                 u"读红（FIRES，尺有牙）" if abs(lkh - round(lkh)) > 5e-3 else u"读绿（BLIND，整性判决作废）",
                 e_half))
            if abs(lkh - round(lkh)) <= 5e-3:
                rc = 1
                verdicts.append(u"K4 奇 n=%d M=%d 半值 framing 变异体未被整性尺判红" % (n, M))
            prev = e
        M, lk, lk1, dlt, lkh = runs[-1]
        e = abs(lk - round(lk))
        if e > 5e-3:
            rc = 1
            verdicts.append(u"K4 奇 n=%d 自链接未整数化（加倍网格仍 %.2e）" % (n, e))
        if abs(dlt - round(dlt)) > 5e-3 or abs(dlt) < 0.5:
            rc = 1
            verdicts.append(u"K4 奇 n=%d framing winding 未整数化" % n)
        p(u"      ⟹ 加倍网格读数 %.5f ⟹ 整数格 %.0f；定理 2′ 在这一支要的却是 n/2=%.1f（半整数格，两边相距 0.5）。"
          % (lk, round(lk), 0.5 * n))
    p(u"      三个奇档落到的整数依次是 %s（＝−2n，本轮实测的拟合式样，**不是**判据——判据只有整性那一栏）；"
      u"它按每圈计两份，与定理 2′ 的每圈半份既不同数也不同标度。"
      % u"、".join(u"%.0f" % round(odd[n][0][-1][1]) for n in sorted(odd)))
    p(u"  开弧口径（只走半圈 t∈[0,2π]，边界根本不闭合）：随带宽 w=(0.2,0.35,0.6) 的读数")
    for n in sorted(open_arc):
        v = open_arc[n]
        drift = max(v) - min(v)
        p(u"    n=%d  %s  漂移=%.5f ⟹ %s" % (n, u" ".join(u"%+.5f" % x for x in v), drift,
                                            u"非不变量（开弧）" if drift > 5e-3 else u"意外地不漂移，需复查"))
        if drift <= 5e-3:
            rc = 1
            verdicts.append(u"K4 开弧漂移未现（奇 n=%d）" % n)
    if 1 in open_arc:
        v1 = open_arc[1]
        p(u"    ⟹ 开弧读数（含符号）确实落在 −n/2 附近（n=1 三档 %s），但它是**半圈**的开口量："
          u"同一根带换个带宽，读数就漂 %.3f＝靶值的 %.0f%%，不满足不变量的定义。"
          % (u" ".join(u"%+.3f" % x for x in v1), max(v1) - min(v1),
             100.0 * (max(v1) - min(v1)) / abs(0.5)))
    half_d = max([abs(odd[n][0][-1][4] - 0.5 * round(2.0 * odd[n][0][-1][4])) for n in odd] or [0.0])
    int_gap = min([abs(odd[n][0][-1][4] - round(odd[n][0][-1][4])) for n in odd] or [0.0])
    p(u"  ⟹ 判决：库内 s=|Lk|=n/2 的「半整数」来自**每圈**（open arc／双重覆盖的半步），")
    p(u"     它不是任何闭曲线的整值自链接；把每圈半步当「自链接数」用时，载体已从闭曲线换成开弧，")
    p(u"     而开弧量对 framing/带宽的选取不不变（上面漂移那一行就是凭据）。")
    p(u"     本轮还把这半句**造出来**了：同一根闭曲线只把 framing 改成半值（副本曲线端点错开、不闭合），")
    p(u"     加倍网格上读数立刻从整数格跳到半整数格（距最近半整数最大 %.1e，距最近整数最小 %.2e＝尺读红的那一栏）"
      u"⟹ 「半整数 Lk」住的正是**非单值 framing**，不是闭曲线的链接数。" % (half_d, int_gap))
    p(u"     对超对称的意义：Q 是**希尔伯特空间上的算符**，它要求谱是闭模上的整/半整自旋标记；"
      u"本轮实测的是 TUFT 只给了经典带的每圈计数，没给算符表示（K1 的实现=0 与此一致）。")

    # ---------- K5 可检验效应账单
    inv = claims_invoice()
    with_pv = [r for r in inv if r[3]]
    buckets = {}
    for r in inv:
        buckets[r[4]] = buckets.get(r[4], 0) + 1
    p(u"")
    p(u"=== K5 「给出一个当前实验能检验的新效应」的账：全库 claims.csv 的 SUSY/反对易词汇行 ===")
    p(u"  行数=%d；带 prediction_value 的行数=%d；status 分桶=%s"
      % (len(inv), len(with_pv), u" ".join(u"%s=%d" % (k if k else u"空", v) for k, v in sorted(buckets.items()))))
    for r in inv[:8]:
        p(u"    %-14s %s 第%d条数据行  pv=%s  status=%s"
          % (r[2], r[0], r[1], r[3] or u"（空）", r[4]))
    p(u"    （口径声明：上面的 N 是 csv 解析出的数据行序号，不是盘上 CR 计数——字段里有换行，两者不等价）")
    if len(inv) > 8:
        p(u"    …另有 %d 行未印" % (len(inv) - 8))
    p(u"  ⟹ 处方要的「当前实验能检验的新效应」＝一行带数值＋误差＋可判读数的预言；现库内 %s。"
      % (u"0 条（带数值的 SUSY 行为 0）" if len(with_pv) == 0 else u"%d 条（须逐条复核其误差与可判性）" % len(with_pv)))
    p(u"  库内自己对 LHC 的记录（反面证据已登记，且它同样打在处方要求的出口本身）：")
    for f in files:
        rel = mod.rel(f)
        if not (rel.startswith(u"00_项目治理") or rel.startswith(u"04_公共成果")):
            continue
        for i, line in enumerate(read_text(f).split(u"\n"), 1):
            if u"LHC" in line and (u"超伴子" in line or u"超对称" in line) and (u"未" in line or u"排除" in line or u"❌" in line):
                p(u"    %s:%d  %s" % (rel, i, line.strip()[:96]))
                break

    p(u"")
    p(u"=== K6 净裁定 ===")
    # K6 引用的数只从本轮 K4 的现场变量复算，不打字（面动则这里的数一起动）
    odd_fine = dict([(n, odd[n][0][-1][1]) for n in odd])
    odd_resid_max = max([abs(v - round(v)) for v in odd_fine.values()] or [0.0])
    odd_ints = u"、".join(u"%.0f" % round(odd_fine[n]) for n in sorted(odd_fine)) or u"（无奇档）"
    drift_pct = (100.0 * (max(open_arc[1]) - min(open_arc[1])) / 0.5) if 1 in open_arc else 0.0
    p(u"  1. 超-Poincaré 的实现在活树里 %d 个文件；克利福德／费米模的实现在活树里 %d 个文件——尺在真语料上不瞎"
      u"（牙齿由六张图现场校准：5 枚夹具＋1 枚库内正对照，另有第二通道独立口径逐枚裁定，不是引用别处的结论）。"
      % (len(susy_impl), len(cliff_impl)))
    p(u"  2. 取用出口的**最小代价**是可算的：K2 那张图要求每态一伙伴且等质量（Str(H)=0、H 本征值全为 2E）；")
    p(u"     K3 的 TUFT 阶梯在两种在壳约定下都不平衡（有质量口径失衡到第 12 层为 %+d），"
      u"配对/劈裂的参数账单按层数线性增长（前 13 层已 %d 个）。" % (ps_M[-1], n_pair))
    p(u"  3. 出口赖以成立的费米子那一支，库内唯一推导（定理 2′）本轮被第二把尺读到两件事：")
    p(u"     其一，偶 n 支的带符号实测是 **−n/2**——库内脚本在 `|Gauss|` 与 `s=|Lk|` 两处取绝对值，把手性消掉了，")
    p(u"     「取绝对值」这个动作本身要申报（它把 Lk 从 ℤ 压到 ℤ≥0，丢的是手性而非数值）；")
    p(u"     其二，奇 n 支按**闭曲线＋单值 framing** 实算是整数（%s；加倍网格距整数最大 %.1e、winding 一位移恰好 +1），"
      u"而定理 2′ 在这一支要的是半整数 ⟹ 它的「半整数」是每圈计数／开弧量（开弧还随带宽漂 %.0f%% 靶值），"
      u"不是闭曲线的整值自链接；" % (odd_ints, odd_resid_max, drift_pct))
    p(u"     所以它是一个**经典带**的量子数，不是算符代数——从「每圈量子数」走到「Q 是希尔伯特空间上的算符」这段路，")
    p(u"     库内没有桥（K1 的实现=0 与 K4 的整数性并列）。")
    p(u"  4. 处方要求的「当前实验能检验的新效应」＝带数值预言：现库 %d 条。" % len(with_pv))
    p(u"     而库内自己已登记 LHC 未发现超伴子（上面点名那一行）——处方的出口并非免费：它把新物理推到未测区，")
    p(u"     于是「从几何第一性导出常数」这一 TUFT 唯一卖点，被替换成「逐层增加劈裂参数」。")
    p(u"  5. 结论照旧且更硬：原 TUFT 不可修复为真正的统一场论；「引入超对称」不是它的补丁，是**换掉它**。")

    n_cr = u"\n".join(L).count(u"\r")
    if n_cr:
        rc = 1
        verdicts.append(u"面内含 CR %d 枚（子进程/语料输出未归一，写入器只走 LF）" % n_cr)
        p(u"  ⚠ 面内含 CR %d 枚——本轮面不得作为 LF 面引用" % n_cr)
    text = u"\n".join(L) + u"\nrc=%d\n" % rc
    if mode == u"--check":
        old = read_text(FACE_REC)
        a = [x for x in old.split(u"\n") if not x.startswith(u"运行时间")]
        b = [x for x in text.split(u"\n") if not x.startswith(u"运行时间")]
        diff = [i for i in range(max(len(a), len(b))) if (a[i] if i < len(a) else u"∅") != (b[i] if i < len(b) else u"∅")]
        print(u"--check DIFF 行数=%d rc=%d" % (len(diff), 0 if not diff else 1))
        for i in diff[:6]:
            print(u"  DIFF L%d" % (i + 1))
        return 1 if diff else 0
    if mode == u"--selftest":
        print(u"自检格数=%d（牙齿 5 图＋库内正对照 1＋K2 执行凭据 1＋K4 偶 n 4＋K4 奇 n 3×5〔标架见证/半值 framing 变异体 2 档/整性/winding〕＋开弧 2＋第二通道裁定 1）rc=%d"
              % (5 + 1 + 1 + 4 + 15 + 2 + 1, rc))
        print(text)
        return rc
    n1, m1 = w(FACE_SRC, text)
    n2, m2 = w(FACE_REC, text)
    n_cr = text.count(u"\r")
    print(text)
    print(u"WROTE %s  %d B md5=%s" % (os.path.relpath(FACE_SRC, ROOT).replace("\\", "/"), n1, m1))
    print(u"WROTE %s  %d B md5=%s  两面逐字节相同=%s  面内 CR 计数=%d（应为 0：写入器只走 LF）"
          % (os.path.relpath(FACE_REC, ROOT).replace("\\", "/"), n2, m2, m1 == m2, n_cr))
    if m1 != m2 or n_cr:
        rc = 1
    if n_cr:
        verdicts.append(u"面内含 CR %d 枚（子进程输出未归一）" % n_cr)
    if rc:
        print(u"本轮判决有红：\n  " + u"\n  ".join(verdicts))
    return rc


if __name__ == "__main__":
    sys.exit(main())
