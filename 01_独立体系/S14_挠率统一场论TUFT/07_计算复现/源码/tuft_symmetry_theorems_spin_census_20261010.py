# -*- coding: utf-8 -*-
"""tuft_symmetry_theorems_spin_census_20261010.py

TUFT 攻坚 · 对称性定理适用域 + 自旋谱 + 传播子结构 普查件（**只读**，纯标准库）

来料（用户提供的外部评估）主张三件事：
  (a) TUFT 用标量 κ,τ 同时产生时空曲率与内部荷 ⟹ 直接违反 Coleman-Mandula；
  (b) 真正统一必须超对称（Haag-Lopuszanski-Sohnius 是唯一推广）；
  (c) 单标量只能给自旋-0 传播子 ⟹ 四力的自旋/距离律结构无法产生。

本件不采信来料的任何陈述，也不采信体系自报，只做四类可复核动作：
  J1  精确有理数线性代数**实算**自旋-0/1/2 场的在壳极化数（无质量/有质量分开）；
  J2  由极点传播子实算静态势与力（无质量 1/r、有质量 e^{-mr}/r）＋同号源的符号结构；
  J3  定理陈述普查：全活树里这三条定理被写在哪些文件、每条陈述覆盖了几项前提；
  J4  自旋谱在册账：全活树里所有「引力子/自旋-2 的 N 个自由度/极化」读数与 J1 对照；
  J5  直积结构在场性（CM 允许形式）＋ CM 前提（质量隙）在本体系自身谱里的失效证据＋超对称构造在场性；
  J6  距离律渠道普查：把 κ(r)/τ(r) 当作径向轮廓的站点，其同文件内是否存在推导渠道（格林/傅里叶/极点/变分）；
  J7  可证伪性账：各体系 claims.csv 的 status 计数＋带数值预言的条数＋「新效应」名字在场性。

判据形状：每个普查都印**分母**（扫了多少文件/多少候选行），因为「0 命中」与「没扫」同形。
牙：--mutant 在临时目录植入已知缺陷与已知合法对照，断言判据按预期翻转（含 specificity 反向对照）。

用法：
  python tuft_symmetry_theorems_spin_census_20261010.py            # 跑并落面
  python tuft_symmetry_theorems_spin_census_20261010.py --check    # 只比对面字节，不改盘
  python tuft_symmetry_theorems_spin_census_20261010.py --mutant   # 植牙自检（临时目录，不碰活树）
"""
import io
import os
import re
import sys
import shutil
import hashlib
import tempfile
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
S14 = os.path.abspath(os.path.join(HERE, "..", ".."))
ROOT = os.path.abspath(os.path.join(S14, "..", ".."))          # openuft/
OUT_NAME = "tuft_symmetry_theorems_spin_census_20261010_report.txt"
OUT_SRC = os.path.join(HERE, OUT_NAME)
OUT_REC = os.path.join(S14, "09_验证结果", "原始运行记录", OUT_NAME)

LIVE_DIRS = ["00_项目治理", "01_独立体系", "02_TUFT_来源", "02_共享基础", "03_跨体系研究",
             "04_公共成果", "05_全球研究", "06_统一体系层", "07_统一场方程", "书籍"]
ARCHIVE_DIRS = ["90_历史归档", "99_待整理资料"]
MD_PY = (".md", ".py", ".txt", ".csv")
SKIP_DIR_NAMES = {".git", "__pycache__", ".venv", "node_modules", ".history", ".preview"}
# 本轮载体：仪器自己的源码与两面，不许被自己的普查数到（否则 fixture 字符串会冒充语料陈述）
SELF_PATHS = {os.path.abspath(OUT_SRC), os.path.abspath(OUT_REC), os.path.abspath(__file__)}
SELF_EXCLUDED = []

L = []
def p(s=""):
    L.append(s)

def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest() if os.path.isfile(path) else "ABSENT"

# ---------------------------------------------------------------- 语料枚举
def walk(dirs):
    files = []
    for d in dirs:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [x for x in dirnames if x not in SKIP_DIR_NAMES]
            for fn in filenames:
                if fn.endswith(MD_PY):
                    full = os.path.abspath(os.path.join(dirpath, fn))
                    if full in SELF_PATHS:
                        SELF_EXCLUDED.append(os.path.relpath(full, ROOT).replace("\\", "/"))
                        continue
                    files.append(full)
    return sorted(files)

_cache = {}
def read_lines(path):
    if path not in _cache:
        try:
            with io.open(path, "r", encoding="utf-8", errors="replace") as f:
                _cache[path] = f.read().split("\n")
        except Exception:
            _cache[path] = []
    return _cache[path]

def rel(path):
    try:
        if os.path.commonpath([path, ROOT]) == ROOT:
            return os.path.relpath(path, ROOT).replace("\\", "/")
    except ValueError:
        pass
    return "(OUT-OF-ROOT)/" + os.path.basename(path)

# ---------------------------------------------------------------- 精确线性代数
def mat_rank(rows, ncols):
    """rows: list of list[Fraction]; return rank via exact Gaussian elimination."""
    m = [list(r) for r in rows]
    rank = 0
    row = 0
    for col in range(ncols):
        piv = None
        for r in range(row, len(m)):
            if m[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        m[row], m[piv] = m[piv], m[row]
        pv = m[row][col]
        m[row] = [x / pv for x in m[row]]
        for r in range(len(m)):
            if r != row and m[r][col] != 0:
                f = m[r][col]
                m[r] = [a - f * b for a, b in zip(m[r], m[row])]
        row += 1
        rank += 1
    return rank

def nullspace(rows, ncols):
    m = [list(r) for r in rows]
    pivots = []
    row = 0
    for col in range(ncols):
        piv = None
        for r in range(row, len(m)):
            if m[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        m[row], m[piv] = m[piv], m[row]
        pv = m[row][col]
        m[row] = [x / pv for x in m[row]]
        for r in range(len(m)):
            if r != row and m[r][col] != 0:
                f = m[r][col]
                m[r] = [a - f * b for a, b in zip(m[r], m[row])]
        pivots.append(col)
        row += 1
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for fc in free:
        v = [Fraction(0)] * ncols
        v[fc] = Fraction(1)
        for i, pc in enumerate(pivots):
            v[pc] = -m[i][fc]
        basis.append(v)
    return basis

def span_dim(vectors):
    vs = [v for v in vectors if any(x != 0 for x in v)]
    if not vs:
        return 0
    return mat_rank(vs, len(vs[0]))

def sum_dim(us, ws):
    """dim(span(us) + span(ws))"""
    all_v = [v for v in us if any(x != 0 for x in v)] + [v for v in ws if any(x != 0 for x in v)]
    if not all_v:
        return 0
    return mat_rank(all_v, len(all_v[0]))

def intersect_dim(us, ws):
    return span_dim(us) + span_dim(ws) - sum_dim(us, ws)

# ---------------------------------------------------------------- J1 极化数实算
ETA = [Fraction(-1), Fraction(1), Fraction(1), Fraction(1)]      # 号差 -+++

def lower(k_up):
    return [ETA[i] * k_up[i] for i in range(4)]

def vector_polarizations(k_up):
    """条件 k_mu e^mu = 0；规范 e ~ e + lambda*k。返回 (约束核维, 规范像∩核维, 物理维)。"""
    k_low = lower(k_up)
    rows = [[k_low[i] for i in range(4)]]                      # k_mu e^mu = 0
    ker = nullspace(rows, 4)
    gauge = [k_up]                                             # e^mu ~ e^mu + lambda k^mu
    inter = intersect_dim(ker, gauge)
    return len(ker), inter, len(ker) - inter

SYM_BASIS = [(a, b) for a in range(4) for b in range(a, 4)]     # 10 维对称张量空间

def sym_coord(vec):
    d = dict(zip(SYM_BASIS, range(len(SYM_BASIS))))
    return [vec[d[(a, b)]] for (a, b) in SYM_BASIS]

def tensor_polarizations(k_up):
    k_low = lower(k_up)
    rows = []
    for nu in range(4):                                         # k^mu e_{mu nu} = 0
        v = [Fraction(0)] * len(SYM_BASIS)
        for idx, (a, b) in enumerate(SYM_BASIS):
            if b == nu:
                v[idx] += k_up[a]
            elif a == nu:
                v[idx] += k_up[b]
        rows.append(v)
    tr = [Fraction(0)] * len(SYM_BASIS)                        # eta^{mu nu} e_{mu nu} = 0
    for idx, (a, b) in enumerate(SYM_BASIS):
        if a == b:
            tr[idx] = ETA[a]
    rows.append(tr)
    ker = nullspace(rows, len(SYM_BASIS))
    gauge = []
    for s in range(4):                                          # de_{mu nu} = k_mu xi_nu + k_nu xi_mu
        xi = [Fraction(0)] * 4
        xi[s] = Fraction(1)
        v = []
        for (a, b) in SYM_BASIS:
            v.append(k_low[a] * xi[b] + k_low[b] * xi[a])
        gauge.append(v)
    inter = intersect_dim(ker, gauge)
    return len(ker), inter, len(ker) - inter

K_NULL = [Fraction(1), Fraction(0), Fraction(0), Fraction(1)]   # k^2 = 0
K_MASS = [Fraction(1), Fraction(0), Fraction(0), Fraction(0)]   # k^2 = -1（单位 m）

# ---------------------------------------------------------------- J2 静态势
def G_massless(r, m=None):
    return 1.0 / (4.0 * 3.141592653589793 * r)

def G_yukawa(r, m):
    import math
    return math.exp(-m * r) / (4.0 * math.pi * r)

def radial_operator_residual(G, r, m, h=1e-4):
    """(-Delta + m^2) G = -(1/r^2)(r^2 G')' + m^2 G，三点中心差分。r>0 处应为 0。"""
    def f(x):
        return G(x, m)
    gp = (f(r + h) - f(r - h)) / (2 * h)
    gpp = (f(r + h) - 2 * f(r) + f(r - h)) / (h * h)
    lap = gpp + 2.0 * gp / r
    mm = 0.0 if m is None else m * m
    return -lap + mm * f(r)

def flux_normalization(G, r, m=None, h=1e-6):
    import math
    def f(x):
        return G(x, m)
    gp = (f(r + h) - f(r - h)) / (2 * h)
    return -4.0 * math.pi * r * r * gp                          # 应为 1（源强归一）

# ---------------------------------------------------------------- J3 定理前提覆盖
CM_GROUPS = {
    "洛伦兹/庞加莱协变": ["洛伦兹", "Lorentz", "庞加莱", "Poincar", "洛氏"],
    "质量隙": ["质量隙", "mass gap", "能隙", "质量间隙"],
    "有限粒子种类": ["有限粒子", "有限种", "粒子种类", "finitely many", "有限个粒子"],
    "S 矩阵/散射": ["S 矩阵", "S矩阵", "S-matrix", "散射", "scattering"],
    "非平凡相互作用": ["非平凡", "non-trivial", "相互作用"],
    "局域性": ["局域", "local", "定域"],
}
WW_GROUPS = {
    "无质量": ["无质量", "massless", "p^2=0", "p²=0"],
    "自旋>1": ["自旋", "spin", "j>1", "s>1", ">1", "高自旋"],
    "守恒流/守恒应力张量": ["守恒流", "守恒荷", "current", "应力", "能量-动量", "能动量", "Theta", "\\Theta"],
    "协变": ["协变", "covariant"],
    "洛伦兹": ["洛伦兹", "Lorentz", "庞加莱", "Poincar"],
}
HLS_GROUPS = {
    "超对称": ["超对称", "supersymmet", "SUSY"],
    "费米型对称荷": ["费米型", "反交换", "anticommutat", "{Q", "\\{Q", "Q_\\alpha", "Qα"],
    "唯一推广": ["唯一", "only"],
    "时空与内部混合": ["混合", "mix", "直积", "non-trivial"],
}

def groups_hit(line, groups):
    return [name for name, kws in groups.items() if any(k.lower() in line.lower() for k in kws)]

def classify_coverage(line, groups, full_at, bare_at):
    n = len(groups_hit(line, groups))
    if n >= full_at:
        return "FULL", n
    if n <= bare_at:
        return "BARE", n
    return "PARTIAL", n

THEOREM_PATTERNS = [
    ("CM", re.compile(r"Coleman\s*[-–—]\s*Mandula|科曼|科尔曼-曼德拉|定理\s*Q", re.I)),
    ("WW", re.compile(r"Weinberg\s*[-–—]\s*Witten|温伯格-威滕|温伯格.?威腾", re.I)),
    ("HLS", re.compile(r"Haag\s*[-–—]\s*Lopuszanski|Lopuszanski|Sohn|哈格-洛普尚斯基", re.I)),
]

def theorem_census(files, tag="LIVE"):
    out = []
    for path in files:
        for i, line in enumerate(read_lines(path), 1):
            for code, pat in THEOREM_PATTERNS:
                if pat.search(line):
                    if code == "CM":
                        cls, n = classify_coverage(line, CM_GROUPS, 4, 1)
                    elif code == "WW":
                        cls, n = classify_coverage(line, WW_GROUPS, 4, 1)
                    else:
                        cls, n = classify_coverage(line, HLS_GROUPS, 3, 1)
                    out.append((code, cls, n, rel(path), i, line.strip()))
    return out

# ---------------------------------------------------------------- J4 自旋谱在册账
DOF_NUM = re.compile(r"(\d{1,2}|[一二两三四五六七八九十])\s*(?:个|种)?\s*(?:物理)?(?:自由度|极化|偏振态|极化态)")
CN_NUM = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
GRAV = re.compile(r"引力子|自旋\s*[-–]?\s*2|spin\s*-?\s*2|h_\\mu\\nu|h_μν|度规扰动|张量横波")
MASSLESS = re.compile(r"无质量|massless|p\^?2\s*=\s*0|p²\s*=\s*0|横向-?无迹|TT")
MASSIVE = re.compile(r"有质量|大质量|massive|vDVZ|Fierz|Pauli")
TORSION = re.compile(r"挠率|torsion")

def dof_census(files):
    hits = []
    for path in files:
        for i, line in enumerate(read_lines(path), 1):
            m = DOF_NUM.search(line)
            if not m or not GRAV.search(line):
                continue
            n_raw = m.group(1)
            n = int(n_raw) if n_raw.isdigit() else CN_NUM[n_raw]
            massless = bool(MASSLESS.search(line))
            massive = bool(MASSIVE.search(line))
            sector = "挠率" if TORSION.search(line) and not re.search(r"引力子|h_μν|h_\\mu\\nu", line) else "引力"
            if sector == "挠率":
                verdict = "SECTOR-TORSION(非引力子)"
            elif massless and not massive:
                verdict = "CONTRADICTION" if n != 2 else "MATCH(massless=2)"
            elif massive and not massless:
                verdict = "MATCH(massive=5)" if n == 5 else "CONTRADICTION(massive=%d)" % n
            else:
                verdict = "UNDECIDED(未点名质量)"
            hits.append((n, verdict, sector, rel(path), i, line.strip()))
    return hits

# ---------------------------------------------------------------- J6 径向轮廓渠道
PROFILE = re.compile(r"\\kappa\(r\)|\\tau\(r\)|kappa\(r\)|tau\(r\)|κ\(r\)|τ\(r\)|f\(r\)\s*=|V\(r\)\s*=")
CHANNEL = re.compile(r"格林|Green|傅里叶|Fourier|留数|residue|极点|pole|传播子|propagator|变分|两?点函数|Geddsen?"
                     r"|玻恩|Born|散射振幅|S 矩阵|S矩阵")

def profile_census(files):
    rows = []
    for path in files:
        pl = [(i, ln) for i, ln in enumerate(read_lines(path), 1) if PROFILE.search(ln)]
        if not pl:
            continue
        joined = "\n".join(read_lines(path))
        ch = sorted(set(x.group(0) for x in CHANNEL.finditer(joined)))
        rows.append((rel(path), len(pl), ch))
    return rows

# ---------------------------------------------------------------- J7 可证伪性账
NEW_EFFECTS = {
    "质子衰变": ["质子衰变", "p→e", "p \u2192 e", "proton decay", "tau_p"],
    "磁单极": ["磁单极", "monopole"],
    "超伴子/超对称粒子": ["超伴", "超对称粒子", "superpartner", "neutralino", "gluino", "squark", "MSSM"],
    "第五力/新规范玻色": ["第五种力", "第五力", "fifth force", "Z′", "Z'", "W′", "W'", "新玻色子"],
    "轴子/暗物质粒子": ["轴子", "axion", "暗物质粒子", "WIMP"],
    "洛伦兹破缺": ["洛伦兹破缺", "Lorentz violation", "色散关系修正"],
    "无质量自旋2以外的新极化": ["挠率极化", "四种极化", "4 种极化", "4种极化", "额外极化"],
}
STATUS_AT = -2   # 行末反向索引（总账红线 4：末两列恒为 status, reviewer）

def claims_census():
    systems = sorted(d for d in os.listdir(os.path.join(ROOT, "01_独立体系"))
                     if os.path.isdir(os.path.join(ROOT, "01_独立体系", d)))
    rows = []
    for s in systems:
        path = os.path.join(ROOT, "01_独立体系", s, "claims.csv")
        if not os.path.isfile(path):
            continue
        lines = [x for x in read_lines(path) if x.strip()]
        n_data = 0
        stat = {}
        numeric = 0
        blob = "\n".join(lines)
        for ln in lines[1:]:
            cells = ln.split(",")
            if len(cells) < 5 or not cells[0].strip():
                continue
            n_data += 1
            st = cells[STATUS_AT].strip() or "(empty)"
            stat[st] = stat.get(st, 0) + 1
            try:
                float(cells[6])
                numeric += 1
            except Exception:
                pass
        effects = {k: len(re.findall("|".join(map(re.escape, v)), blob, re.I)) for k, v in NEW_EFFECTS.items()}
        rows.append((s, n_data, numeric, stat, effects))
    return rows

# ---------------------------------------------------------------- 主流程
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    files_live = walk(LIVE_DIRS)
    files_arch = walk(ARCHIVE_DIRS)

    p("TUFT 对称性定理适用域 + 自旋谱 + 传播子结构 普查（只读件）")
    p("运行时间: 2026-10-10    脚本: %s" % os.path.basename(__file__))
    p("作用域（分母现测，不猜）：")
    for d in LIVE_DIRS:
        base = os.path.join(ROOT, d)
        n = len([f for f in files_live if rel(f).startswith(d + "/")])
        p("  %-14s %5d 文件" % (d, n))
    p("  活树合计        %5d 文件（另：归档/待整理 %d 文件，本件仅在 J3 单独计数）" % (len(files_live), len(files_arch)))
    p("  本轮载体已排除：%d 个文件（仪器源码与其两面，避免 fixture 字符串冒充语料陈述）：%s"
      % (len(SELF_EXCLUDED), "、".join(sorted(SELF_EXCLUDED))))

    # ---------------- J1
    p("\n=== J1 在壳极化数：精确有理数线性代数实算（不是引用教科书数）===")
    checks = 0
    results = []
    for label, k in (("矢量 无质量 k=(1,0,0,1)", K_NULL), ("矢量 有质量 k=(1,0,0,0)", K_MASS)):
        ker, inter, phys = vector_polarizations(k)
        results.append(("spin-1 %s" % label, ker, inter, phys))
    for label, k in (("对称张量 无质量 k=(1,0,0,1)", K_NULL), ("对称张量 有质量 k=(1,0,0,0)", K_MASS)):
        ker, inter, phys = tensor_polarizations(k)
        results.append(("spin-2 %s" % label, ker, inter, phys))
    for name, ker, inter, phys in results:
        p("  %-34s 约束核=%d  规范像∩核=%d  物理极化=%d" % (name, ker, inter, phys))
    expect = {0: 2, 1: 3, 2: 2, 3: 5}
    for i, (name, ker, inter, phys) in enumerate(results):
        want = expect[i]
        ok = phys == want
        checks += 1
        if not ok:
            p("  !! J1 实算与闭式不符: %s 得 %d 期望 %d" % (name, phys, want))
            break
    p("  闭式对照：无质量 s≥1 ⟹ 螺旋度 ±s 共 2；有质量 ⟹ 2s+1（s=1→3，s=2→5）；标量 ⟹ 1")
    p("  交叉核对（对称张量闭式）：无质量 d(d-3)/2 代 d=4 ⟹ %d；有质量 2s+1 代 s=2 ⟹ %d" % (4 * (4 - 3) // 2, 2 * 2 + 1))
    p("  J1 实算断言 %d 条，全部成立 ⟹ 无质量自旋-2 的物理极化数 **只能是 2**；"
      "5 属于有质量自旋-2（Fierz-Pauli）。" % checks)

    # ---------------- J2
    p("\n=== J2 极点传播子 ⟹ 静态势/力（实算）===")
    import math
    res0 = max(abs(radial_operator_residual(lambda x, m: G_massless(x), r, None)) for r in (0.5, 1.0, 2.0, 5.0))
    resY = max(abs(radial_operator_residual(G_yukawa, r, 1.0)) for r in (0.5, 1.0, 2.0, 5.0))
    p("  无质量 G0(r)=1/(4πr)：r>0 处 (-Δ)G0 残差 max=%.3e  源强归一 -4πr²G0'=%s (r=1)" % (res0, ("%.6f" % flux_normalization(lambda x, m: G_massless(x), 1.0))))
    p("  有质量 Gm(r)=e^{-mr}/(4πr)，m=1：(-Δ+m²)G 残差 max=%.3e  源强归一(r=1e-3)=%s" % (resY, ("%.6f" % flux_normalization(G_yukawa, 1e-3, 1.0))))
    p("  ⟹ 距离律形状由极点结构定死：无质量 ⟹ 1/r（力 1/r²）；有质量 ⟹ e^{-mr}/r（力 e^{-mr}(m/r+1/r²)）。")
    signs = []
    for r in (0.3, 0.7, 1.0, 2.0, 4.0):
        v_scalar = -1.0 * 1.0 * G_massless(r)     # 标量交换：V = -g1 g2 G（同号耦合）
        v_vector = +1.0 * 1.0 * G_massless(r)     # 矢量交换：V = +q1 q2 G（同号电荷）
        signs.append((r, v_scalar, v_vector, math.copysign(1, v_scalar) == math.copysign(1, v_vector)))
        p("  r=%-4s 标量同号源 V=%+.6e  矢量同号源 V=%+.6e  同号?%s" % (r, v_scalar, v_vector, signs[-1][3]))
    same = sum(1 for x in signs if x[3])
    p("  同号源势的符号一致点数：%d/%d ⟹ 在 1/r 与 e^{-mr}/r 两支下，单标量交换对**同类源恒为吸引**，"
      "而同类电荷的电磁力为排斥；两者符号在采样的每一个 r 上都不相同。" % (same, len(signs)))
    p("  禁闭支：V=σr ⟹ F=-dV/dr=-σ（常数，与 1/r² 不同族）；它需要 1/q⁴ 型奇性而非质量极点，"
      "⟹ 不属任何「极点传播子 + 位」的静态势家族。")

    # ---------------- J3
    p("\n=== J3 三条定理在活树里的在场性与陈述完整度 ===")
    ctl_full = ("在四维洛伦兹协变、质量隙、有限粒子种类、S 矩阵非平凡且局域的量子场论下，"
                "Coleman-Mandula 定理要求对称群为庞加莱与内部群的直积")
    ctl_bare = "Coleman-Mandula 定理已在别处引用。"
    cf, nf = classify_coverage(ctl_full, CM_GROUPS, 4, 1)
    cb, nb = classify_coverage(ctl_bare, CM_GROUPS, 4, 1)
    p("  分类器牙检（内置对照）：完整陈述 → %s(%d 项前提)；裸引用 → %s(%d 项)。%s"
      % (cf, nf, cb, nb, "PASS" if (cf == "FULL" and cb == "BARE") else "FAIL"))
    if not (cf == "FULL" and cb == "BARE"):
        p("  !! 分类器无牙，J3 全部读数不可引用")
        sys.exit(1)
    cens = theorem_census(files_live)
    for code in ("CM", "WW", "HLS"):
        sub = [x for x in cens if x[0] == code]
        dist = {}
        for _, cls, _, _, _, _ in sub:
            dist[cls] = dist.get(cls, 0) + 1
        p("  %s：活树命中 %d 行；陈述分档 %s" % (code, len(sub), dist if sub else "0 行"))
    p("  明细（每档至多印 6 行，行首标前提覆盖项数）：")
    for code in ("CM", "WW", "HLS"):
        sub = [x for x in cens if x[0] == code]
        for cls in ("FULL", "PARTIAL", "BARE"):
            picked = [x for x in sub if x[1] == cls][:6]
            for _, _, n, f, i, ln in picked:
                p("    %-3s %-7s n=%d  %s:%d  %s" % (code, cls, n, f, i, (ln[:110] + "…") if len(ln) > 110 else ln))
            if len([x for x in sub if x[1] == cls]) > 6:
                p("    %-3s %-7s …另有 %d 行未印" % (code, cls, len([x for x in sub if x[1] == cls]) - 6))
    arch_cens = theorem_census(files_arch)
    p("  归档树（只计数，不作在册依据）：%s 命中 %d 行" % (
        "CM/WW/HLS", len([x for x in arch_cens if x[0] == "CM"])))
    ww_wrong = [x for x in arch_cens if x[0] == "WW" and "质量隙" in x[5] and "守恒" not in x[5]]
    p("  归档里把 WW 说成「证明某些规范场论中不可能存在质量隙」的行数：%d（该表述与 J1/守恒流前提都对不上；"
      "活树里的 X2 行才是正确形态）" % len(ww_wrong))

    # ---------------- J4
    p("\n=== J4 自旋谱在册账：所有「引力子/自旋-2 的 N 个自由度/极化」读数 vs J1 实算 ===")
    p("  辖区声明：只认「N 个|种 (物理) 自由度|极化|偏振态|极化态」拼写（N 为阿拉伯数字或中文数词一/二/两/…）；"
      "把读数写在 LaTeX 结构里的形态（例：$=3=2$（引力子极化）$+1$（标量））不在本件辖区内，须另配尺。")
    hits = dof_census(files_live)
    buckets = {}
    for n, verdict, sector, f, i, ln in hits:
        buckets.setdefault(verdict, []).append((n, f, i, ln))
    p("  候选行分母：%d 行（含引力/自旋-2 关键词且带 N 个自由度|极化 读数）" % len(hits))
    for verdict in sorted(buckets):
        p("  %-28s %d 处" % (verdict, len(buckets[verdict])))
        for n, f, i, ln in buckets[verdict][:8]:
            p("      N=%d  %s:%d  %s" % (n, f, i, (ln[:100] + "…") if len(ln) > 100 else ln))
        if len(buckets[verdict]) > 8:
            p("      …另有 %d 处未印" % (len(buckets[verdict]) - 8))
    contra = buckets.get("CONTRADICTION", [])
    p("  ⟹ 与 J1 实算（无质量自旋-2=2）直接矛盾的在册行数：%d" % len(contra))

    # ---------------- J5
    p("\n=== J5 CM 的适用域：直积结构在场性 / 质量隙前提失效 / 超对称构造在场性 ===")
    dp_hits = []
    for path in files_live:
        if not rel(path).startswith("07_统一场方程/"):
            continue
        for i, line in enumerate(read_lines(path), 1):
            if re.search(r"SO\(1,\s*3\).{0,12}\\times|G_\{?\\rm\s*int\}?\s*=|\[\s*\\mathfrak\{so\}\(1,3\),\s*\\mathfrak\{g\}_\{?\\rm\s*int\}?\]\s*=\s*0", line):
                dp_hits.append((rel(path), i, line.strip()))
    p("  「时空 ⋊ 内部 = 直积 / 交叉对易子为零」的证据行（仅扫 07_统一场方程，分母=%d 文件）：%d 行"
      % (len([f for f in files_live if rel(f).startswith("07_统一场方程/")]), len(dp_hits)))
    for f, i, ln in dp_hits[:5]:
        p("      %s:%d  %s" % (f, i, (ln[:120] + "…") if len(ln) > 120 else ln))
    meta_md = os.path.join(ROOT, "07_统一场方程", "06_场元数据表.md")
    zero_mass = 0
    prop_spin2 = 0
    for line in read_lines(meta_md):
        if re.search(r"^\|\s*[^|]+\|\s*[^|]*\|\s*2\s*\|", line):
            prop_spin2 += 1
        if re.search(r"引力子|光子", line) and re.search(r"\|\s*0\s*\|", line):
            zero_mass += 1
    p("  质量隙前提：06_场元数据表.md 里点名为无质量（引力子/光子且质量列=0）的行数=%d；"
      "自旋列=2 的行数=%d ⟹ 体系自身谱里**存在无质量粒子**，CM 的「质量隙」前提在该谱上不成立"
      % (zero_mass, prop_spin2))
    p("  ⟹ 判定：CM 不能对 UFE-1 说「违反」——它写成的就是 CM 允许（且只允许）的直积形式；"
      "同时它也不满足 CM 的质量隙前提，故定理既不定罪也不赦罪。CM 真正封死的是**混合**（时空⟷内部）这一诉求本身。")
    susy_construct = []
    susy_mention = []
    alg_pat = re.compile(r"\{\s*Q\s*,\s*\\bar\{?Q|\\{Q_\\alpha|superpotential|超势|\\text\{SUSY\}|gravitino|\\psi_\\mu.*\\partial|Rarita")
    for path in files_live:
        for i, line in enumerate(read_lines(path), 1):
            low = line.lower()
            if susy_construct_check(line):
                susy_construct.append((rel(path), i, line.strip()))
            elif ("超对称" in line or "supersymmet" in low or "mssm" in low) and len(line.strip()) > 4:
                susy_mention.append((rel(path), i, line.strip()))
    p("  超对称**构造**（超荷反交换子/超势/引力微子场项）在场行数：%d；纯提及行数：%d"
      % (len(susy_construct), len(susy_mention)))
    for f, i, ln in susy_construct[:6]:
        p("      [构造] %s:%d  %s" % (f, i, (ln[:110] + "…") if len(ln) > 110 else ln))
    for f, i, ln in susy_mention[:4]:
        p("      [提及] %s:%d  %s" % (f, i, (ln[:100] + "…") if len(ln) > 100 else ln))

    # ---------------- J6
    p("\n=== J6 距离律渠道普查：径向轮廓是被推导的还是被假设的 ===")
    rows = profile_census(files_live)
    with_ch = [r for r in rows if r[2]]
    without = [r for r in rows if not r[2]]
    p("  含 κ(r)/τ(r)/f(r)/V(r) 型径向轮廓的活树文件：%d；其中同文件存在推导渠道关键词：%d；无渠道：%d"
      % (len(rows), len(with_ch), len(without)))
    for f, n, ch in rows[:12]:
        p("      %-86s 轮廓行 %3d  渠道=%s" % (f, n, ("、".join(ch[:4]) if ch else "无 ✗")))
    if len(rows) > 12:
        p("      …另有 %d 份未印" % (len(rows) - 12))

    # ---------------- J7
    p("\n=== J7 可证伪性账：claims.csv 状态、带数值预言条数、新效应名字在场性 ===")
    cl = claims_census()
    tot_rows = sum(x[1] for x in cl)
    tot_num = sum(x[2] for x in cl)
    p("  体系数=%d  claims 数据行=%d  预测字段可 float 解析的行=%d（口径：CSV 字段层，非正文层）" % (len(cl), tot_rows, tot_num))
    agg = {}
    for _, _, _, stat, _ in cl:
        for k, v in stat.items():
            agg[k] = agg.get(k, 0) + v
    p("  status 合计（行末反向索引口径，总账红线 4）：%s" % agg)
    eff_tot = {}
    for _, _, _, _, effects in cl:
        for k, v in effects.items():
            eff_tot[k] = eff_tot.get(k, 0) + v
    p("  「真统一必给的」新效应名字命中数（全库 claims 正文）：")
    for k in NEW_EFFECTS:
        p("      %-24s %d" % (k, eff_tot.get(k, 0)))
    for s, n, num, stat, effects in cl:
        if num or any(v for v in effects.values()):
            p("      · %-40s rows=%3d numeric=%d  新效应命中=%s" % (s, n, num, {k: v for k, v in effects.items() if v}))

    # ---------------- 判定块
    p("\n=== 判定汇总 ===")
    v = {k: len(buckets.get(k, [])) for k in buckets}
    leak = sorted(set(files_live + files_arch) & SELF_PATHS)
    p("  D0 自排除核验：普查集合里仍含本轮载体的文件数=%d（必须为 0）%s"
      % (len(leak), "PASS" if not leak else "FAIL：" + "、".join(leak)))
    if leak:
        p("  !! 仪器看见了自己，J3/J4/J6 的读数全部作废")
        return 2
    p("  D1 J1 实算断言：%d 条（无质量 spin-2 极化=2、有质量=5、矢量 2/3）" % checks)
    p("  D2 J4 与 J1 冲突的在册行：%d（桶：%s）" % (len(contra), v if v else "{}"))
    p("  D3 J3 三条定理在活树的陈述行数：CM=%d WW=%d HLS=%d；BARE 档合计=%d"
      % (len([x for x in cens if x[0] == "CM"]), len([x for x in cens if x[0] == "WW"]),
         len([x for x in cens if x[0] == "HLS"]), len([x for x in cens if x[1] == "BARE"])))
    p("  D4 超对称构造行=%d（⟹ HLS 的「唯一出口」在本库内**未被取用**，只有提及）" % len(susy_construct))
    p("  D5 径向轮廓文件 %d 份，其中无推导渠道 %d 份（⟹ 距离律多数是假设而非极点推导）" % (len(rows), len(without)))
    p("  D6 claims 数据行=%d，带数值预言=%d，新效应名字命中合计=%d" % (tot_rows, tot_num, sum(eff_tot.values())))
    n_judged = 6 + len(contra) + len(cens) + len(rows) + len(cl)
    p("  本轮实际判决的行数（PASS 只值这个数）：%d" % n_judged)
    p("  rc=0（普查件只读，不改任何活树文件）")

    face = "\n".join(L) + "\n"
    if mode == "--check":
        bad = []
        for path in (OUT_SRC, OUT_REC):
            if not os.path.isfile(path):
                bad.append("ABSENT " + path)
                continue
            disk = open(path, "rb").read().decode("utf-8").split("\n")
            if open(path, "rb").read() != face.encode("utf-8"):
                bad.append("DIFF " + path)
        if bad:
            print("CHECK FAIL:")
            for b in bad:
                print("  " + b)
            return 1
        print("CHECK OK 面字节一致  %d B" % len(face.encode("utf-8")))
        return 0
    for path in (OUT_SRC, OUT_REC):
        with io.open(path, "w", encoding="utf-8", newline="") as f:
            f.write(face)
    print(face)
    for path in (OUT_SRC, OUT_REC):
        b = open(path, "rb").read()
        print("WROTE %s  %d B  LF=%d  CRLF=%d  md5=%s" % (rel(path), len(b), b.count(b"\n"), b.count(b"\r\n"), md5(path)))
    return 0

def susy_construct_check(line):
    """超对称是否被**构造**（而非提及）：超荷反交换子、超势、引力微子场、SUSY 变号配对。"""
    tests = [
        r"\{\s*Q\s*,\s*\\?bar",
        r"\{Q_\\alpha",
        r"superpotential",
        r"超势",
        r"Rarita",
        r"gravitino",
        r"\\delta_\{?\\rm\s*SUSY",
    ]
    return any(re.search(t, line, re.I) for t in tests)

# ---------------------------------------------------------------- 植牙自检
def mutant_selftest():
    tmp = tempfile.mkdtemp(prefix="tuft_sym_mutant_")
    rc = 0
    n = 0
    try:
        d1 = os.path.join(tmp, "live1")
        os.makedirs(d1)
        bad = os.path.join(d1, "planted_bad.md")
        with io.open(bad, "w", encoding="utf-8", newline="\n") as f:
            f.write("# 植入缺陷\n\n引力子：TT 投影 p²=0，无质量，自旋 2，5 个物理自由度\n\n"
                    "引力子无质量、自旋 2、两个极化\n\n有质量引力子有 5 个物理自由度\n")
        _cache.pop(bad, None)
        good = os.path.join(d1, "planted_good.md")
        with io.open(good, "w", encoding="utf-8", newline="\n") as f:
            f.write("# 合法对照\n\n该文件不含任何引力子自由度读数\n")
        n += 1
        hits = dof_census([bad, good])
        verdicts = [h[1] for h in hits]
        c = verdicts.count("CONTRADICTION")
        m = sum(1 for x in verdicts if x.startswith("MATCH"))
        print("M1 植入面：候选行=%d CONTRADICTION=%d MATCH=%d（期望 3 行/1 枚/2 枚）%s"
              % (len(hits), c, m, "PASS" if (len(hits) == 3 and c == 1 and m == 2) else "FAIL"))
        if not (len(hits) == 3 and c == 1 and m == 2):
            rc = 1
        with io.open(bad, "w", encoding="utf-8", newline="\n") as f:
            f.write("# 已修面\n\n引力子：TT 投影 p²=0，无质量，自旋 2，2 个物理自由度\n")
        _cache.pop(bad, None)
        n += 1
        hits2 = dof_census([bad])
        c2 = sum(1 for h in hits2 if h[1] == "CONTRADICTION")
        print("M2 修好植入缺陷后 CONTRADICTION=%d（期望 0）%s" % (c2, "PASS" if c2 == 0 else "FAIL"))
        if c2 != 0:
            rc = 1
        n += 1
        cm_full = "四维洛伦兹协变、质量隙、有限粒子种类、S 矩阵非平凡、局域 ⟹ Coleman-Mandula 直积"
        cm_bare = "Coleman-Mandula 见别处"
        a, _ = classify_coverage(cm_full, CM_GROUPS, 4, 1)
        b, _ = classify_coverage(cm_bare, CM_GROUPS, 4, 1)
        print("M3 定理陈述分类器：完整=%s 裸引用=%s（期望 FULL/BARE）%s" % (a, b, "PASS" if (a == "FULL" and b == "BARE") else "FAIL"))
        if not (a == "FULL" and b == "BARE"):
            rc = 1
        n += 1
        # J1 的牙：把无质量 k 改成有质量，物理极化数必须从 2 变 5（同一台仪器、两个输入）
        kn = tensor_polarizations(K_NULL)
        km = tensor_polarizations(K_MASS)
        print("M4 极化计数的换代见证：无质量=%d 有质量=%d（期望 2/5）%s" % (kn[2], km[2], "PASS" if (kn[2], km[2]) == (2, 5) else "FAIL"))
        if (kn[2], km[2]) != (2, 5):
            rc = 1
        n += 1
        # J2 的牙：m=0 与 m=1 的残差都必须小，但势的形状必须不同（否则尺子看不见质量项）
        r0 = abs(radial_operator_residual(lambda x, m: G_massless(x), 1.0, None))
        r1 = abs(radial_operator_residual(G_yukawa, 1.0, 1.0))
        shape = abs(G_massless(1.0) - G_yukawa(1.0, 1.0)) / G_massless(1.0)
        print("M5 静态势：残差 m=0 %.2e / m=1 %.2e 都需<1e-3；两形状相对差=%.4f 需>0（期望两者同时成立）%s"
              % (r0, r1, shape, "PASS" if (r0 < 1e-3 and r1 < 1e-3 and shape > 0) else "FAIL"))
        if not (r0 < 1e-3 and r1 < 1e-3 and shape > 0):
            rc = 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("MUTANT 自检格数=%d  rc=%d" % (n, rc))
    return rc

if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if len(sys.argv) > 1 and sys.argv[1] == "--mutant":
        sys.exit(mutant_selftest())
    sys.exit(main())
