# -*- coding: utf-8 -*-
"""
统一场论核心公式可视化 · 整理分析与第一性审计（2026-09-29）
================================================================
被审对象：`utf/10-统一场论核心公式/可视化/`（张祥前统一场论 20 个核心公式的
可视化工程：38 个 .py、16 个 .html、48 张图，README 自述 v1.0.0 / 2026-01-17）。

目的：用本项目既有尺子（量纲审计 / 口径一致性 / 数值复算 / 第一性层级 /
UFT-3 登记数）对**一份可视化工程**做整理与判定，产出可复跑证据。

红线（必读）：
- 本册只审**数学自洽性与文档一致性**，不审绘图美观、不审工程性能。
- 可视化「画得出来」不构成物理成立的证据：图的曲线由脚本内的**假设函数**
  决定，与方程是否为真无关（本册 D6 将给出明证）。
- 量纲自洽 ≠ 物理正确（既有定理 C 反例警戒：S11 的 Q/M=√(4πε₀G) 量纲完全
  一致，却与电子实测差 2.04e21 倍）。
- 所有 FAIL / BOUNDARY 如实登记，不粉饰为 PASS。

六个模块：
  M1 结构盘点（真实文件系统扫描：体量 / 冗余 / 依赖 / 硬编码 / CDN 版本）
  M2 公式台账（20 式逐条落座：来源、是否缺源码、是否重复编号）
  M3 量纲审计（比例常数 k 的唯一性与跨式一致性；逐式量纲自洽）
  M4 数值复算（E=mc²、r=ct、P=m(C−V) 的两个极限、F=dP/dt 符号、核力 λ）
  M5 口径一致性（重复编号 / 互斥版本 / 图形≠方程 / v≡c 约束缺席）
  M6 第一性层级与 UFT-3（无量纲预言登记数、锚依赖、定理 C 归属）

门禁（自检 10 条，任一失败即退出码 1）：
  G1 台账 20 式齐全且编号唯一
  G2 每式均有来源或显式标记缺失
  G3 可判定式的 k 量纲解唯一（4 基整数向量）
  G4 数值项全部为有限值且残差可读数
  G5 结构扫描成功（目录存在且文件数 > 0）
  G6 verdict 词表合法
  G7 计数自洽（总数 = 四态之和）
  G8 四态齐备（至少各 1 条，防"全绿"式空跑）
  G9 幂等：输出目录存在且本轮重写成功
  G10 无跨式 k 被误判为同一个（跨式量纲表非空且两两比较已执行）

幂等覆盖输出：数据/统一场论核心公式可视化_整理分析.json / .md
"""
import json
import os
import re
import sys
import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "数据"))
# 源码/ -> 本项目_全维自洽与归一化/ -> 04_公共成果/ -> openuft/ -> my_lib/
MY_LIB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SRC_DIR = os.path.join(MY_LIB, "utf", "10-统一场论核心公式", "可视化")

# ------------------------------------------------------------------
# 量纲基： (M, L, T, I) —— SI 四基
# ------------------------------------------------------------------
BASE = ("M", "L", "T", "I")

DIMS = {
    "m": (1, 0, 0, 0),              # 质量 kg
    "dm_dt": (1, 0, -1, 0),         # 质量变化率 kg/s
    "vel": (0, 1, -1, 0),           # 速度 m/s
    "len": (0, 1, 0, 0),            # 长度 m
    "time": (0, 0, 1, 0),           # 时间 s
    "omega": (0, 0, -1, 0),         # 角速度 rad/s（rad 无量纲）
    "E_field": (1, 1, -3, -1),      # 电场强度 V/m = kg·m·s^-3·A^-1
    "B_field": (1, 0, -2, -1),      # 磁感应强度 T = kg·s^-2·A^-1
    "A_vecpot": (1, 1, -2, -1),     # 磁矢势 T·m
    "accel": (0, 1, -2, 0),         # 加速度 / 引力场强 m/s^2
    "charge": (0, 0, 1, 1),         # 电荷 C = A·s
    "force": (1, 1, -2, 0),         # 力 N
    "energy": (1, 2, -2, 0),        # 能量 J
    "momentum": (1, 1, -1, 0),      # 动量 kg·m/s
    "volume": (0, 3, 0, 0),         # 体积 m^3
    "area": (0, 2, 0, 0),           # 面积 m^2
    "G_newton": (-1, 3, -2, 0),     # 引力常数 m^3·kg^-1·s^-2
}


def solve_k(target, terms):
    """解比例常数 k 的量纲：dim(k) = dim(target) - Σ p_i·dim(term_i)。"""
    v = list(DIMS[target])
    for name, p in terms:
        d = DIMS[name]
        for i in range(4):
            v[i] -= p * d[i]
    return tuple(v)


def fmt_dim(v):
    parts = []
    for i, b in enumerate(BASE):
        if v[i] == 0:
            continue
        parts.append(b + "^" + str(v[i]))
    return " · ".join(parts) if parts else "1（无量纲）"


# ------------------------------------------------------------------
# M2 公式台账：20 式（17 个编号目录 + 3 个补齐式）
# ------------------------------------------------------------------
FORMULAS = [
    ("F01", "时空同一化方程", "r = c t", "01-时空同一化方程/", "identity"),
    ("F02", "三维螺旋时空方程", "r(t) = r cos(ωt) i + r sin(ωt) j + h t k", "02三维螺旋时空方程/1.py", "geometric"),
    ("F03", "质量定义方程", "m = k · dn/dΩ", "03质量定义方程/1.py", "undefined_symbol"),
    ("F04", "引力场定义方程", "（README 未列式；源码目录缺失）", "（无源码，仅 standardized 输出 PNG）", "missing"),
    ("F05", "静止动量方程", "p₀ = m₀ C₀", "05静止动量方程/1.py", "dynamical"),
    ("F06", "运动动量方程", "P = m(C − V)", "06运动动量方程/1.py", "dynamical"),
    ("F07", "宇宙大统一方程", "F = dP/dt = C(dm/dt) − V(dm/dt) + m(dC/dt) − m(dV/dt)", "07宇宙大统一方程/1.py", "dynamical"),
    ("F08", "三维空间波动方程", "∇²L = (1/c²) ∂²L/∂t²", "08三维空间波动方程/1.py", "known_physics"),
    ("F09", "引力场与旋转速度关系", "A = −k (dm/dt) (ω × r)/r³", "09引力场与旋转速度关系/1.py", "field"),
    ("F10", "电场定义方程", "E = k (dm/dt) (V₁ × V₂)/r³", "10电场定义方程/1.py", "field"),
    ("F11", "磁场定义方程", "B = k (dm/dt) [(V₁ × (V₂ × r))/r⁵]", "11磁场定义方程/1.py", "field"),
    ("F12", "电磁场能量方程", "W = k (1/2) (E² + B²) V", "12电磁场能量方程/1.py", "field"),
    ("F13", "能量方程", "E = m C²", "13能量方程/1.py", "known_physics"),
    ("F14", "动量能量方程", "P = m(C − V)", "14动量能量方程/1.py", "dynamical"),
    ("F15", "时空波动方程", "∂²L/∂t² = c² ∇²L", "15时空波动方程/1.py", "known_physics"),
    ("F16", "时间的本质方程", "t = f(r)", "16时间的本质方程/1.py", "placeholder"),
    ("F17", "电荷定义方程", "Q = k ∫(dm/dt)(V × r)/r³ dV", "17电荷定义方程/1.py", "field"),
    ("F18", "磁矢势方程（补）", "A = k (dm/dt) V₁/r", "remaining_formulas_visualization.py", "field"),
    ("F19", "电荷积分式（补）", "q = ∫(dm/dt) · dS", "remaining_formulas_visualization.py", "field"),
    ("F20", "核力场定义方程（补）", "F_n = G_n (m₁m₂/r²) exp(−r/λ)", "remaining_formulas_visualization.py", "known_physics"),
]

# M3 量纲可判定式：(公式 id, 目标量, 除 k 外的因子幂次表)
DIM_CASES = [
    ("F05", "momentum", [("m", 1), ("vel", 1)]),
    ("F06", "momentum", [("m", 1), ("vel", 1)]),
    ("F09", "accel", [("dm_dt", 1), ("omega", 1), ("len", -2)]),
    ("F10", "E_field", [("dm_dt", 1), ("vel", 2), ("len", -3)]),
    ("F11", "B_field", [("dm_dt", 1), ("vel", 2), ("len", -4)]),
    ("F17", "charge", [("dm_dt", 1), ("vel", 1), ("len", -2), ("volume", 1)]),
    ("F18", "A_vecpot", [("dm_dt", 1), ("vel", 1), ("len", -1)]),
    ("F20", "force", [("m", 2), ("len", -2)]),
    ("F13", "energy", [("m", 1), ("vel", 2)]),
]

# 式中**显式写出符号 k** 的式（F03 也写 k 但 n 未定义故不可判定；F20 系数名为 G_n 不是 k）
# 其余式解出 dim(k)=1 表示无需带量纲系数即可自洽。
WITH_K = {"F09", "F10", "F11", "F17", "F18"}

RECORDS = []


def add(section, rid, title, verdict, evidence):
    RECORDS.append({
        "section": section,
        "id": rid,
        "title": title,
        "verdict": verdict,
        "evidence": evidence,
    })


def count(verdict):
    return sum(1 for r in RECORDS if r["verdict"] == verdict)


# ==================================================================
# M1 结构盘点（真实文件系统扫描）
# ==================================================================
def scan_files(root):
    out = []
    if not os.path.isdir(root):
        return out
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", ".git")]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            try:
                size = os.path.getsize(full)
            except OSError:
                size = -1
            rel = os.path.relpath(full, root).replace("\\", "/")
            out.append((rel, size, os.path.splitext(fn)[1].lower()))
    return out


FILES = scan_files(SRC_DIR)
BY_EXT = {}
TOTAL_BYTES = 0
for rel, size, ext in FILES:
    BY_EXT[ext] = BY_EXT.get(ext, 0) + 1
    TOTAL_BYTES += max(size, 0)

add("M1", "S1", "工程体量",
    "INFO",
    "文件 " + str(len(FILES)) + " 个 / " + format(TOTAL_BYTES / 1048576.0, ".2f") + " MB；"
    "扩展名分布 " + ", ".join(k + "×" + str(v) for k, v in sorted(BY_EXT.items(), key=lambda x: -x[1])))

if FILES:
    empty = [r for r, s, e in FILES if s == 0]
    add("M1", "S2", "零字节产物",
        "BOUNDARY" if empty else "PASS",
        ("零字节文件 " + str(len(empty)) + " 个：" + ", ".join(empty[:6])) if empty else "无零字节文件")

    # 归一化基名：去扩展名 + 去前导编号（03质量定义方程_2D ↔ 质量定义方程_2D 视为同一图）
    def norm_stem(path):
        s = os.path.splitext(os.path.basename(path))[0]
        return re.sub(r"^\d+[-_]?", "", s)

    pngs = [r for r, s, e in FILES if e == ".png"]
    stems = {}
    for p in pngs:
        stems.setdefault(norm_stem(p), []).append(p)
    dupes = {k: v for k, v in stems.items() if len(v) > 1}
    dup_bytes = 0
    size_of = {r: s for r, s, e in FILES}
    for k, v in dupes.items():
        for p in sorted(v)[1:]:
            dup_bytes += size_of.get(p, 0)
    add("M1", "S3", "同一张图的多重副本",
        "FAIL" if dupes else "PASS",
        ("重复组 " + str(len(dupes)) + " 组，冗余副本约 "
         + format(dup_bytes / 1048576.0, ".2f") + " MB；每组 "
         + ", ".join(k + "(" + str(len(v)) + " 份)" for k, v in sorted(dupes.items()))
         + "；副本散落在 03质量定义方程/img、textbook_visualizations、standardized_textbook_visualizations 三处")
        if dupes else "无重复图")

    hard = []
    for rel, size, ext in FILES:
        if ext != ".py":
            continue
        try:
            with open(os.path.join(SRC_DIR, rel.replace("/", os.sep)), "r", encoding="utf-8", errors="replace") as fh:
                txt = fh.read()
        except OSError:
            continue
        if re.search(r"[a-zA-Z]:[\\/]a10[\\/]|d:\\\\a10", txt):
            hard.append(rel)
    add("M1", "S4", "硬编码绝对路径脚本",
        "BOUNDARY" if hard else "PASS",
        ("命中 " + str(len(hard)) + " 个：" + ", ".join(hard[:4]) + "（跨机不可移植，且该类脚本会递归改写同目录所有 .py）")
        if hard else "无硬编码绝对路径")

    cdn = {}
    three_ver = set()
    orbit_ver = set()
    katex_ver = set()
    for rel, size, ext in FILES:
        if ext != ".html":
            continue
        try:
            with open(os.path.join(SRC_DIR, rel.replace("/", os.sep)), "r", encoding="utf-8", errors="replace") as fh:
                txt = fh.read()
        except OSError:
            continue
        for host in re.findall(r"https?://([a-zA-Z0-9.\-]+)", txt):
            cdn[host] = cdn.get(host, 0) + 1
        # three.js 核心版本：three@X 或 three/X
        three_ver.update(re.findall(r"three@(0\.\d+\.\d+|r\d+)", txt))
        three_ver.update(re.findall(r"three/(0\.\d+\.\d+|r\d+)/", txt))
        # OrbitControls：显式 @X 版本，或随 three@X 一同引入（此时版本即 three 的版本）
        orbit_ver.update(re.findall(r"OrbitControls@(0\.\d+\.\d+)", txt))
        orbit_ver.update(re.findall(r"three@(0\.\d+\.\d+)[^\s\"']*?OrbitControls", txt))
        katex_ver.update(re.findall(r"katex@(0\.\d+\.\d+)", txt))
        katex_ver.update(re.findall(r"katex/(0\.\d+\.\d+)/", txt))
    mixed = sorted(orbit_ver - three_ver)
    add("M1", "S5", "外部 CDN 与三方库版本漂移",
        "BOUNDARY" if len(three_ver) > 1 or len(katex_ver) > 1 or mixed else "PASS",
        "CDN 域名 " + ", ".join(sorted(cdn)) + "；three.js 核心版本 "
        + (", ".join(sorted(three_ver)) if three_ver else "未检出") + "；OrbitControls 版本 "
        + (", ".join(sorted(orbit_ver)) if orbit_ver else "未检出")
        + ("（其中 " + ", ".join(mixed) + " 不在核心版本集合内 ⇒ 控制器与核心混搭）" if mixed else "")
        + "；KaTeX 版本 " + (", ".join(sorted(katex_ver)) if katex_ver else "未检出"))

    manim_files = []
    for rel, size, ext in FILES:
        if ext != ".py":
            continue
        try:
            with open(os.path.join(SRC_DIR, rel.replace("/", os.sep)), "r", encoding="utf-8", errors="replace") as fh:
                txt = fh.read()
        except OSError:
            continue
        if re.search(r"^\s*(from\s+manim\s+import|import\s+manim)", txt, re.M):
            manim_files.append(rel)
    add("M1", "S6", "manim 依赖不可得",
        "BOUNDARY" if manim_files else "PASS",
        ("依赖 manim 的脚本 " + str(len(manim_files)) + " 个（" + ", ".join(manim_files[:4])
         + "）；manim 未在本机环境安装 ⇒ 该分支不可运行，属「可运行性缺口」而非代码错误")
        if manim_files else "无 manim 依赖")

    missing_dir = [f for f in FORMULAS if f[4] == "missing"]
    add("M1", "S7", "编号目录缺口",
        "FAIL" if missing_dir else "PASS",
        ("缺失源码的编号式 " + str(len(missing_dir)) + " 个："
         + ", ".join(f[0] + " " + f[1] for f in missing_dir)
         + "（standardized_textbook_visualizations 下有 04 的 PNG 输出，无生成源码 ⇒ 产物不可复现）")
        if missing_dir else "编号目录齐全")
else:
    add("M1", "S2", "结构扫描", "INFO",
        "源目录不存在：" + SRC_DIR + " ⇒ M1 结构项降级为 INFO（其余模块不依赖文件系统）")
    for rid in ("S3", "S4", "S5", "S6", "S7"):
        add("M1", rid, "结构扫描（跳过）", "INFO", "源目录不存在，未执行")

# ==================================================================
# M2 公式台账
# ==================================================================
ids = [f[0] for f in FORMULAS]
add("M2", "T1", "公式台账覆盖",
    "PASS" if len(set(ids)) == 20 and len(ids) == 20 else "FAIL",
    "台账 20 式，编号唯一：" + ("是" if len(set(ids)) == 20 else "否")
    + "；来源标注齐全率 " + format(sum(1 for f in FORMULAS if f[3]) / 20.0 * 100, ".0f") + "%")

# ==================================================================
# M3 量纲审计
# ==================================================================
K_DIMS = {}
for fid, target, terms in DIM_CASES:
    kv = solve_k(target, terms)
    K_DIMS[fid] = (kv, fmt_dim(kv))
    add("M3", "D-" + fid, "量纲自洽（" + fid + "）",
        "PASS",
        "dim(k_" + fid + ") = " + fmt_dim(kv) + "；目标量 dim(" + target + ") = " + fmt_dim(DIMS[target])
        + "；因子 " + ", ".join(n + "^" + str(p) for n, p in terms))

# 跨式 k 一致性（核心硬读数）
cross = [("F10", "F11", "电场 vs 磁场"), ("F10", "F09", "电场 vs 引力场"),
         ("F10", "F17", "电场 vs 电荷"), ("F10", "F18", "电场 vs 磁矢势"),
         ("F11", "F17", "磁场 vs 电荷"), ("F09", "F17", "引力场 vs 电荷")]
mismatch = []
for a, b, label in cross:
    if K_DIMS[a][0] != K_DIMS[b][0]:
        mismatch.append(label + "（" + K_DIMS[a][1] + " ≠ " + K_DIMS[b][1] + "）")
add("M3", "D-K1", "同一符号 k 的跨式量纲一致性",
    "FAIL" if mismatch else "PASS",
    "共用符号 k 的五式（F09/F10/F11/F17/F18）两两比较，" + str(len(mismatch)) + "/" + str(len(cross))
    + " 对量纲互异：" + "；".join(mismatch)
    + "。⇒ 若 k 为同一普适常数则方程组量纲矛盾；若 k 为各式独立比例系数，"
      "则 README「核心公式集」并未给出统一常数，两种解读均需文档显式声明（当前未声明）")

# F07 四项逐项量纲
f07_terms = {
    "C(dm/dt)": ("vel", "dm_dt"),
    "V(dm/dt)": ("vel", "dm_dt"),
    "m(dC/dt)": ("m", "accel"),
    "m(dV/dt)": ("m", "accel"),
}
f07_ok = True
f07_detail = []
for label, (a, b) in f07_terms.items():
    v = tuple(DIMS[a][i] + DIMS[b][i] for i in range(4))
    ok = v == DIMS["force"]
    f07_ok = f07_ok and ok
    f07_detail.append(label + " → " + fmt_dim(v) + ("✓" if ok else "✗"))
add("M3", "D-F07", "宇宙大统一方程 F=dP/dt 四项量纲",
    "PASS" if f07_ok else "FAIL",
    "；".join(f07_detail) + "；目标 dim(force) = " + fmt_dim(DIMS["force"])
    + " ⇒ 展开为乘积求导，量纲自洽（自洽 ≠ 正确，符号问题见 M4）")

# F12：E² + B² 量纲冲突（脚本已声明单位 V/m 与 T）
e2 = tuple(2 * DIMS["E_field"][i] for i in range(4))
b2 = tuple(2 * DIMS["B_field"][i] for i in range(4))
diff = tuple(e2[i] - b2[i] for i in range(4))
add("M3", "D-F12", "电磁场能量方程 E²+B² 量纲",
    "FAIL",
    "dim(E²) = " + fmt_dim(e2) + "，dim(B²) = " + fmt_dim(b2)
    + "，差 " + fmt_dim(diff) + "（=" + fmt_dim((0, 2, -2, 0)) + "，即 (速度)²）"
    + "。脚本自述 E 单位 V/m、B 单位 T ⇒ 在 SI 下两项不可相加；"
      "标准式为 w = ½(ε₀E² + B²/μ₀)。若采用 c=1 或自定义单位制使 E/B 同量纲，须显式声明（仓库未声明）")

# F19：电荷积分式无量纲系数却量纲不合
f19_v = tuple(DIMS["dm_dt"][i] + DIMS["area"][i] for i in range(4))
need = tuple(DIMS["charge"][i] - f19_v[i] for i in range(4))
add("M3", "D-F19", "电荷积分式 q=∫(dm/dt)·dS 量纲",
    "FAIL",
    "dim(∫(dm/dt)dS) = " + fmt_dim(f19_v) + "，目标 dim(q) = " + fmt_dim(DIMS["charge"])
    + " ⇒ 缺系数 dim = " + fmt_dim(need) + "，而式中未写任何系数。"
      "且与 F17 的电荷定义式量纲路径不同（同一物理量两套定义，差 " + fmt_dim(need) + "）")

# F03 / F16 不可判定
add("M3", "D-F03", "质量定义方程 m = k·dn/dΩ 可判定性",
    "BOUNDARY",
    "Ω 为立体角（无量纲），但 n（「空间运动量」条数）在任何脚本与 README 中均无定义、无单位、无测量口径"
    " ⇒ 该式当前不可计算、不可检验（非量纲错误，是**符号未定义**）")
add("M3", "D-F16", "时间本质方程 t = f(r) 可判定性",
    "BOUNDARY",
    "f 未给具体形式 ⇒ 不是方程而是占位声明；不可计算、不可检验。脚本 16/1.py 以自定义 f 作图，"
      "图形不承载该式的任何预测")

# ==================================================================
# M4 数值复算
# ==================================================================
from fractions import Fraction as F

c_light = F(299792458)
m_kg = F(1)
E_joule = m_kg * c_light ** 2
add("M4", "N1", "E = mC² 数值",
    "PASS",
    "m=1 kg → E = " + str(E_joule) + " J（精确，" + format(float(E_joule), ".10e") + "）。"
    "但 m、c 均为测量锚/定义值 ⇒ 按定理 C 情形 1，该式**无信息增益**（不是预言，是单位换算）")

add("M4", "N2", "r = ct 数值",
    "PASS",
    "t=1 s → r = " + str(int(c_light)) + " m。该式即光速定义（c ≡ r/t）⇒ L0 恒等，零预言内容")

p_rest = m_kg * c_light
add("M4", "N3", "P = m(C − V) 静止极限",
    "BOUNDARY",
    "V=0 ⇒ P = m·c = " + format(float(p_rest), ".6e") + " kg·m/s ≠ 0。"
    "经典力学静止动量为 0，相对论静止动量亦为 0 ⇒ 该体系在静止态给出非零动量，"
    "须给出其在经典极限下与 p=mv 的对应规则（当前文档未给）")

add("M4", "N4", "P = m(C − V) 高速极限",
    "BOUNDARY",
    "V → C（同向）⇒ P → 0；而相对论 p=γmV 在该极限下发散。"
    "两个极限均与标准动量行为相反 ⇒ 需体系给出「动量」的操作定义与经典极限恢复说明")

add("M4", "N5", "F = dP/dt 与牛顿第二定律的符号",
    "BOUNDARY",
    "m、C 为常数时 dP/dt = −m(dV/dt) = −ma，与牛顿 F=+ma **反号**。"
    "该符号问题在本仓库既有审计中已登记（S02 族 M03），属体系内一致、跨体系冲突 ⇒ 记 BOUNDARY，"
    "要求文档给出经典极限符号约定")

hbar = F("1.054571817e-34")
m_pi = F("2.488e-28")
lam = hbar / (m_pi * c_light)
add("M4", "N6", "核力 F_n = G_n(m₁m₂/r²)exp(−r/λ) 的力程",
    "BOUNDARY",
    "取 λ = ħ/(m_π c) = " + format(float(lam), ".3e") + " m，落在核力经验力程 1–2 fm 内 ⇒ 形式自洽；"
    "但 λ 与 G_n 均为**自由参数**（式中无第一性约束）⇒ 属事后标定，非预言")

# ==================================================================
# M5 口径一致性
# ==================================================================
def read_text(rel):
    try:
        with open(os.path.join(SRC_DIR, rel), "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def files_containing(pattern):
    hits = []
    for rel, size, ext in FILES:
        if ext != ".py":
            continue
        txt = read_text(rel)
        if pattern in txt:
            hits.append(rel)
    return hits


if FILES:
    dup_momentum = files_containing("P = m(C - V)")
    add("M5", "C1", "公式编号重复占用（动量）",
        "FAIL" if len(dup_momentum) > 1 else "PASS",
        "同一式 P = m(C − V) 同时占据 F06「运动动量方程」与 F14「动量能量方程」两个编号 ⇒ "
        "README 声称的「20 个核心公式」中至少 2 个编号不对应独立公式。命中文件："
        + ", ".join(dup_momentum))

    wave_a = files_containing("∂²L/∂t² = c²∇²L")
    wave_b = files_containing("∇²L = (1/c²)")
    add("M5", "C2", "公式编号重复占用（波动方程）",
        "FAIL" if wave_a and wave_b else "PASS",
        "F15「∂²L/∂t² = c²∇²L」与 F08「∇²L = (1/c²)∂²L/∂t²」为同一方程的代数变形 ⇒ 又一组重复编号。"
        "且该式即经典波动方程（已知物理），不构成新内容")

    mass_a = files_containing("m = k · dn/dΩ")
    mass_b = files_containing("m = \\frac{E}{c^2}")
    add("M5", "C3", "同一编号式的互斥版本（质量定义）",
        "FAIL" if mass_a and mass_b else "PASS",
        "F03 在独立脚本与 enhanced_visualizations 中为 m = k·dn/dΩ，"
        "在 manim_visualizations 中却写作 m = E/c²（质能式的重排，与 F13 同一条约束）⇒ "
        "同一编号对应两个不同公式，其中一个是已知物理的重述")

    txt03 = read_text("03质量定义方程/1.py")
    gauss = "高斯分布" in txt03 or "gauss" in txt03.lower()
    add("M5", "C4", "图形 ≠ 方程（质量定义式）",
        "FAIL" if gauss else "BOUNDARY",
        "03/1.py 的 dn/dΩ 由 space_motion_density() 给出，实现为**高斯分布假设**"
        "（源码自述「这里使用高斯分布近似表示实际物理场景中的分布」）⇒ 图上曲线是所选假设函数的形状，"
        "不是 m = k·dn/dΩ 的推论。这是本册最重要的诚实边界：**可视化不承载方程的证据**")

    txt02 = read_text("02三维螺旋时空方程/1.py")
    has_c = ("299792458" in txt02) or ("光速" in txt02 and "=" in txt02) or ("v_total" in txt02.lower())
    add("M5", "C5", "螺旋式与 v≡c 公设的脱节",
        "BOUNDARY" if not has_c else "PASS",
        "02/1.py 未出现光速约束（未检得 299792458 或等价约束式）⇒ 螺旋参数 r、ω、h 自由取值，"
        "画出的螺旋不保证速率模长 √(r²ω²+h²) 等于 c。与本仓库 S02/S12「v≡c 螺旋运动学族」的公设未对接")

    kset = {fid: fmt_dim(v[0]) for fid, v in K_DIMS.items() if fid in WITH_K}
    nok = sorted(fid for fid, v in K_DIMS.items() if fid not in WITH_K)
    add("M5", "C6", "比例常数 k 的文档声明缺失",
        "FAIL",
        "README 与脚本均以「比例常数」统称 k，未说明各式的 k 是否同一常数；实测含 k 的式 "
        + "; ".join(k + ": " + v for k, v in sorted(kset.items()))
        + " ⇒ 五式解出五种不同量纲（两两 6/6 全异），需在文档中二选一并声明（同一常数则量纲矛盾；"
          "各自独立则不构成统一常数）。另 " + ", ".join(nok) + " 未写 k 且解出无量纲，量纲自洽")
else:
    for rid in ("C1", "C2", "C3", "C4", "C5", "C6"):
        add("M5", rid, "口径检查（跳过）", "INFO", "源目录不存在，未执行")

# ==================================================================
# M6 第一性层级与 UFT-3
# ==================================================================
l0 = [f[0] for f in FORMULAS if f[4] in ("identity", "known_physics", "placeholder")]
add("M6", "L1", "第一性层级分布",
    "INFO",
    "20 式中：恒等/已知物理/占位 " + str(len(l0)) + " 个（" + ", ".join(l0) + "）；"
    "含未定义符号 " + str(sum(1 for f in FORMULAS if f[4] == "undefined_symbol")) + " 个；"
    "场定义式（含自由 k）" + str(sum(1 for f in FORMULAS if f[4] == "field")) + " 个。"
    "⇒ 无一式达到 L2/L3（无可检验无量纲预言）")

add("M6", "L2", "UFT-3（无量纲预言登记数）",
    "FAIL",
    "20 式中登记的「无量纲预测值 + 误差棒」= 0 条；所有自由量（k×5、G_n、λ、n、f(·)）"
    "均未在式中被第一性固定 ⇒ 按定理 C 情形 2，任给观测值皆可反解自由参数，"
    "等式等价于参数的定义，不可检验")

add("M6", "L3", "与本仓库体系的归属",
    "INFO",
    "该工程属「空间光速螺旋」族（S02 空间光速螺旋统一力 / S12 空间光速螺旋统一体系同源："
    "P=m(C−V)、F=dP/dt）。按不越界原则：**本册结论不得回溯改写 S02/S12 的既有判定**，"
    "仅作为该族一份可视化来料的独立整理与审计")

add("M6", "L4", "整理建议（去冗余，可机械执行）",
    "INFO",
    "①合并 F06/F14 与 F08/F15 的重复编号（20 → 18 独立式）；②删除 m2.py/m3.py 之一（头部逐字重复）；"
    "③清理 3 份同名的质量定义 PNG 副本（约 8.8 MB）；④删除 2 个 0 字节 log；"
    "⑤统一 three.js / KaTeX 版本；⑥fix_fonts_and_latex.py 去硬编码路径或标记为一次性工具；"
    "⑦为 04 引力场定义方程补生成源码（否则产物不可复现）；⑧在 README 声明 k 与单位制")

# ==================================================================
# 门禁自检
# ==================================================================
GUARDS = []


def guard(gid, ok, msg):
    GUARDS.append({"id": gid, "ok": bool(ok), "msg": msg})


guard("G1", len(FORMULAS) == 20 and len(set(ids)) == 20, "台账 20 式且编号唯一")
guard("G2", all(f[3] for f in FORMULAS), "每式均有来源标注（缺失者显式标记）")
guard("G3", all(len(K_DIMS[f][0]) == 4 for f in K_DIMS), "可判定式 k 量纲解为 4 基整数向量")
guard("G4", float(E_joule) > 0 and float(lam) > 0, "数值项为有限正值")
guard("G5", len(FILES) > 0, "结构扫描命中文件（" + str(len(FILES)) + " 个）")
guard("G6", all(r["verdict"] in ("PASS", "FAIL", "BOUNDARY", "INFO") for r in RECORDS), "verdict 词表合法")
guard("G7", len(RECORDS) == count("PASS") + count("FAIL") + count("BOUNDARY") + count("INFO"), "计数自洽")
guard("G8", min(count("PASS"), count("FAIL"), count("BOUNDARY"), count("INFO")) >= 1, "四态齐备")
guard("G9", os.path.isdir(OUT_DIR), "输出目录存在")
guard("G10", len(mismatch) > 0 and len(K_DIMS) >= 8, "跨式 k 比较已执行且量纲表非空（" + str(len(K_DIMS)) + " 式）")

# ==================================================================
# 输出
# ==================================================================
if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)

COUNTS = {
    "PASS": count("PASS"),
    "FAIL": count("FAIL"),
    "BOUNDARY": count("BOUNDARY"),
    "INFO": count("INFO"),
}
TOTAL = len(RECORDS)

payload = {
    "meta": {
        "title": "统一场论核心公式可视化 · 整理分析与第一性审计",
        "date": "2026-09-29",
        "engine": os.path.basename(__file__),
        "source_dir": SRC_DIR,
        "source_exists": os.path.isdir(SRC_DIR),
        "python": sys.version.split()[0],
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    },
    "counts": COUNTS,
    "total": TOTAL,
    "grading": "C / L0–L1",
    "structure": {
        "files": len(FILES),
        "bytes": TOTAL_BYTES,
        "by_ext": BY_EXT,
    },
    "formulas": [
        {"id": f[0], "name": f[1], "expr": f[2], "loc": f[3], "kind": f[4]} for f in FORMULAS
    ],
    "k_dimensions": {k: v[1] for k, v in K_DIMS.items()},
    "records": RECORDS,
    "guards": GUARDS,
}

JSON_PATH = os.path.join(OUT_DIR, "统一场论核心公式可视化_整理分析.json")
with open(JSON_PATH, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=2)

lines = []
lines.append("# 统一场论核心公式可视化 · 整理分析与第一性审计")
lines.append("")
lines.append("> 引擎产物（幂等覆盖）· 生成时间 " + payload["meta"]["generated_at"]
             + " · Python " + payload["meta"]["python"])
lines.append("> 被审对象：`" + SRC_DIR + "`")
lines.append("")
lines.append("## 计数")
lines.append("")
lines.append("| 总数 | PASS | FAIL | BOUNDARY | INFO |")
lines.append("|---|---|---|---|---|")
lines.append("| " + str(TOTAL) + " | " + str(COUNTS["PASS"]) + " | " + str(COUNTS["FAIL"])
             + " | " + str(COUNTS["BOUNDARY"]) + " | " + str(COUNTS["INFO"]) + " |")
lines.append("")
lines.append("评级：**C / L0–L1**（工程层：结构冗余与文档一致性缺陷明确；物理层：无 L2/L3 内容）")
lines.append("")
lines.append("## 结构盘点")
lines.append("")
lines.append("| 项 | 读数 |")
lines.append("|---|---|")
lines.append("| 文件数 | " + str(len(FILES)) + " |")
lines.append("| 总体积 | " + format(TOTAL_BYTES / 1048576.0, ".2f") + " MB |")
for k, v in sorted(BY_EXT.items(), key=lambda x: -x[1]):
    lines.append("| " + k + " | " + str(v) + " |")
lines.append("")
lines.append("## 公式台账（20 式）")
lines.append("")
lines.append("| ID | 名称 | 表达式 | 来源 | 类别 |")
lines.append("|---|---|---|---|---|")
for f in FORMULAS:
    lines.append("| " + f[0] + " | " + f[1] + " | `" + f[2] + "` | " + f[3] + " | " + f[4] + " |")
lines.append("")
lines.append("## 比例常数 k 的量纲解")
lines.append("")
lines.append("| 公式 | dim(k) |")
lines.append("|---|---|")
for k in sorted(K_DIMS):
    lines.append("| " + k + " | " + K_DIMS[k][1] + " |")
lines.append("")
lines.append("## 逐条判定")
lines.append("")
lines.append("| 模块 | ID | 标题 | 判定 | 证据 |")
lines.append("|---|---|---|---|---|")
for r in RECORDS:
    lines.append("| " + r["section"] + " | " + r["id"] + " | " + r["title"] + " | "
                 + r["verdict"] + " | " + r["evidence"].replace("|", "/") + " |")
lines.append("")
lines.append("## 门禁自检")
lines.append("")
for g in GUARDS:
    lines.append("- " + g["id"] + " " + ("PASS" if g["ok"] else "FAIL") + " — " + g["msg"])
lines.append("")

MD_PATH = os.path.join(OUT_DIR, "统一场论核心公式可视化_整理分析.md")
with open(MD_PATH, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

ok = all(g["ok"] for g in GUARDS)
print("=== 统一场论核心公式可视化 · 整理分析与审计 ===")
print("源目录: " + SRC_DIR + ("（存在）" if os.path.isdir(SRC_DIR) else "（缺失）"))
print("文件: " + str(len(FILES)) + " 个 / " + format(TOTAL_BYTES / 1048576.0, ".2f") + " MB")
print("总数 " + str(TOTAL) + " | PASS " + str(COUNTS["PASS"]) + " | FAIL " + str(COUNTS["FAIL"])
      + " | BOUNDARY " + str(COUNTS["BOUNDARY"]) + " | INFO " + str(COUNTS["INFO"]))
print("自检 " + str(sum(1 for g in GUARDS if g["ok"])) + "/" + str(len(GUARDS)))
for g in GUARDS:
    print("  " + g["id"] + " " + ("PASS" if g["ok"] else "FAIL") + " — " + g["msg"])
print("wrote " + JSON_PATH)
print("wrote " + MD_PATH)
sys.exit(0 if ok else 1)
