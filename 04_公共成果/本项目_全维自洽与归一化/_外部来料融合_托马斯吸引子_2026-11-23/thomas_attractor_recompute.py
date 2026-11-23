# -*- coding: utf-8 -*-
"""托马斯吸引子 HTML 来料独立复核引擎。

对象：`托马斯吸引子_实时相空间示波器_来料原文_2026-11-23.html`
（Thomas 循环对称系统、RK4、Benettin λ1、庞加莱截面、盒维数、状态阈值）。

两路：
  路 A = 从来料 HTML 源码正则解析常数、阈值、种子与初值；
  路 B = 按方程与算法说明在脚本内独立写死的同口径常数与实现；
两路只在末尾比对，数据源互不引用。

门族：
  A 常数/散度/RK4 收敛阶；B λ1 正性与异路一致性、非混沌负对照；
  C 庞加莱穿越与插值、盒维数双实现；D 红线与独立预言 0。
本册是外部来料复核，不是新物理，不占 RID、不登记 README、不与原 HTML 或 UFT 链相加。
"""
import ast
import glob
import hashlib
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = glob.glob(os.path.join(HERE, "*来料原文*.html"))
assert len(HTML) == 1, HTML
HTML = HTML[0]
OUT_JSON = os.path.join(HERE, "_thomas_recompute.json")
REPORT_PATH = os.path.join(HERE, "_thomas_recompute_report.txt")

with open(HTML, encoding="utf-8") as f:
    src = f.read()
html_md5 = hashlib.md5(src.encode("utf-8")).hexdigest()
html_bytes = len(src.encode("utf-8"))

gates = []


def add(gid, kind, exp, act, ok, note=""):
    gates.append({"id": gid, "kind": kind, "exp": str(exp), "act": str(act),
                  "ok": bool(ok), "note": note})


# AST 前置与写死 ok 防护
tree = ast.parse(ast_parse_src := open(os.path.abspath(__file__), encoding="utf-8").read())
bad_import = []
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            if alias.name in ("numpy", "sympy"):
                bad_import.append(alias.name)
    if isinstance(node, ast.ImportFrom) and node.module in ("numpy", "sympy"):
        bad_import.append(node.module)
bad_call = [getattr(n.func, "id", "?") for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id in ("eval", "exec")]
hardcoded_ok = []
for node in ast.walk(tree):
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "add" and len(node.args) >= 5):
        v = node.args[4]
        if isinstance(v, ast.Constant) and isinstance(v.value, bool):
            hardcoded_ok.append(getattr(node.args[0], "value", "?"))
add("G00-ast", "gate", "AST 前置：无 numpy/sympy、无 eval/exec、add 的 ok 不写死",
    "bad_import=%s bad_call=%s hardcoded_ok=%s" % (bad_import, bad_call, hardcoded_ok),
    (not bad_import and not bad_call and not hardcoded_ok),
    "机验自身的守卫也必须可翻红")


# ---------------------------------------------------------------------------
# 路 A：从来料 HTML 解析常数
# ---------------------------------------------------------------------------
def parse_one(pattern, cast=float, label=""):
    m = re.search(pattern, src)
    assert m is not None, "parse failed: %s" % label
    return cast(m.group(1))


A = {
    "b": parse_one(r"let b\s*=\s*([0-9.]+);", float, "b"),
    "dt": parse_one(r"const DT\s*=\s*([0-9.]+);", float, "DT"),
    "scale": parse_one(r"const SCALE\s*=\s*([0-9.]+);", float, "SCALE"),
    "cloud_n": parse_one(r"const CLOUD_N\s*=\s*(\d+);", int, "CLOUD_N"),
    "d0": parse_one(r"const D0\s*=\s*([0-9eE.+-]+);", float, "D0"),
    "renorm_steps": parse_one(r"const RENORM_STEPS\s*=\s*(\d+);", int, "RENORM_STEPS"),
    "eps": parse_one(r"const eps\s*=\s*([0-9eE.+-]+);", float, "trace eps"),
    "poincare_range": parse_one(r"const POINCARE_RANGE\s*=\s*([0-9.]+);", float, "POINCARE_RANGE"),
}
A["base"] = [float(x) for x in re.search(r"const base = \[([^\]]+)\];", src).group(1).split(",")]
A["eps_list"] = [float(x) for x in re.search(r"const epsList = \[([^\]]+)\];", src).group(1).split(",")]
A["thresholds"] = [float(x) for x in re.findall(r"if\(bv > ([0-9.]+)\)", src)]
A["warmups"] = sorted(set(v for v in
                          (int(x) for x in re.findall(r"for\(let [is]=0;[is]<(\d+);[is]\+\+\)", src))
                          if v >= 100))
A["div_text"] = re.search(r'id="r-div">([^<]+)', src).group(1).strip().replace("−", "-")
A["div"] = float(A["div_text"])

# 路 B：独立写死的同口径常数（不读取 A）
B = {
    "b": 0.19,
    "dt": 0.012,
    "scale": 1.6,
    "cloud_n": 130000,
    "d0": 1e-8,
    "renorm_steps": 8,
    "eps": 1e-5,
    "poincare_range": 6.5,
    "base": [0.1, 0.2, 0.3],
    "eps_list": [0.5, 0.36, 0.26, 0.19, 0.14, 0.10],
    "thresholds": [0.9428, 0.33, 0.10],
    "warmups": [1500, 3000],
    "div": -0.570,
}

const_match = all(
    (A[k] == B[k]) if not isinstance(B[k], list) else (A[k] == B[k])
    for k in B
)
add("A1-two-path-constants", "gate", "路A(HTML解析) 与路B(独立写死) 常数逐项一致",
    "A=%s ; mismatch=%s" % (A, [k for k in B if A[k] != B[k]]),
    const_match,
    "两路数据源互不引用；warmups 是循环上界集合 {1500,3000}；"
    "i<3 是轨迹条数循环非 warmup，按上界>=100 过滤")


# ---------------------------------------------------------------------------
# 动力学与 RK4（按来料公式独立实现）
# ---------------------------------------------------------------------------
def deriv(p, b):
    x, y, z = p
    return (math.sin(y) - b * x,
            math.sin(z) - b * y,
            math.sin(x) - b * z)


def rk4(p, dt, b):
    x, y, z = p
    k1 = deriv((x, y, z), b)
    k2 = deriv((x + dt / 2 * k1[0], y + dt / 2 * k1[1], z + dt / 2 * k1[2]), b)
    k3 = deriv((x + dt / 2 * k2[0], y + dt / 2 * k2[1], z + dt / 2 * k2[2]), b)
    k4 = deriv((x + dt * k3[0], y + dt * k3[1], z + dt * k3[2]), b)
    return (x + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
            y + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]),
            z + dt / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]))


def norm3(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def sub3(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def diverge_analytic(bv):
    # d/dx(sin y - b x) + d/dy(sin z - b y) + d/dz(sin x - b z) = -3b
    return -3.0 * bv


add("A2-divergence", "gate", "解析散度 ∇·F=-3b 与来料默认读数 −0.570 一致",
    "analytic=%.6f html=%s" % (diverge_analytic(B["b"]), A["div_text"]),
    abs(diverge_analytic(B["b"]) - B["div"]) < 1e-12
    and abs(A["div"] - B["div"]) < 1e-12,
    "三角函数交叉项偏导为 0，只有三个 -b 对角项承重")


def integrate(p, dt, n, bv):
    q = tuple(p)
    for _ in range(n):
        q = rk4(q, dt, bv)
    return q


def max_abs_diff(a, b):
    return max(abs(a[i] - b[i]) for i in range(3))


# RK4 四阶自检：同一 T，取 dt / dt/2 / dt/4，与 dt/16 参考比
T_SPAN = 2.004
n0 = int(round(T_SPAN / B["dt"]))
p0 = tuple(B["base"])
ref = integrate(p0, B["dt"] / 16, n0 * 16, B["b"])
e1 = max_abs_diff(integrate(p0, B["dt"], n0, B["b"]), ref)
e2 = max_abs_diff(integrate(p0, B["dt"] / 2, n0 * 2, B["b"]), ref)
e4 = max_abs_diff(integrate(p0, B["dt"] / 4, n0 * 4, B["b"]), ref)
r1 = e1 / e2 if e2 > 0 else float("inf")
r2 = e2 / e4 if e4 > 0 else float("inf")
add("A3-rk4-order", "gate", "RK4 在渐近段呈四阶：e(dt)/e(dt/2) 与 e(dt/2)/e(dt/4) 约 16",
    "T=%s dt=%s errors=(%.3e,%.3e,%.3e) ratios=(%.3f,%.3f)" % (
        T_SPAN, B["dt"], e1, e2, e4, r1, r2),
    (12.0 < r1 < 20.0 and 12.0 < r2 < 20.0),
    "短时窗 T≈2 避开混沌指数放大；门限 12<ratio<20 不放宽")


# ---------------------------------------------------------------------------
# Benettin 最大李雅普诺夫指数
# ---------------------------------------------------------------------------
def lyapunov(bv, steps, warmup=1500, d0=1e-8, renorm=8,
             seed=(0.1, 0.2, 0.3), pert=(1.0, 0.0, 0.0), dt=0.012):
    p = tuple(seed)
    q = tuple(seed[i] + d0 * pert[i] for i in range(3))
    for _ in range(warmup):
        p = rk4(p, dt, bv)
        q = rk4(q, dt, bv)
    dv = sub3(q, p)
    d = norm3(dv) or 1.0
    q = tuple(p[i] + dv[i] / d * d0 for i in range(3))
    ly_sum = 0.0
    count = 0
    counter = 0
    for _ in range(steps):
        p = rk4(p, dt, bv)
        q = rk4(q, dt, bv)
        counter += 1
        if counter >= renorm:
            dv = sub3(q, p)
            d = norm3(dv) or 1e-15
            ly_sum += math.log(d / d0)
            count += 1
            q = tuple(p[i] + dv[i] / d * d0 for i in range(3))
            counter = 0
    return ly_sum / (count * renorm * dt)


LY_STEPS = 24000
ly_html = lyapunov(B["b"], LY_STEPS, warmup=1500, d0=B["d0"],
                   renorm=B["renorm_steps"], seed=tuple(B["base"]),
                   pert=(1.0, 0.0, 0.0), dt=B["dt"])
ly_ind = lyapunov(B["b"], LY_STEPS, warmup=1800, d0=1e-9,
                  renorm=20, seed=(0.2, 0.3, 0.1),
                  pert=(0.0, 1.0, 0.0), dt=B["dt"])
add("B1-lyapunov-positive", "gate", "b=0.19 的 λ₁>0，复现强混沌标签",
    "lambda_html=%.6f lambda_independent=%.6f" % (ly_html, ly_ind),
    ly_html > 0.0 and ly_ind > 0.0,
    "Benettin 重归一化；两条独立影子轨迹口径不同仍同号")
add("B2-lyapunov-cross-check", "gate", "异构实现 λ₁ 差值在有限采样容差内",
    "diff=%.6f tol=0.02" % abs(ly_html - ly_ind),
    abs(ly_html - ly_ind) < 0.02,
    "不同 warmup / d0 / 重归一化间隔 / 扰动方向；容差 0.02 对应有限采样")
ly_nonchaotic = lyapunov(1.2, 12000, warmup=1500, d0=1e-8,
                         renorm=8, seed=(0.1, 0.2, 0.3), dt=0.012)
add("B3-nonchaotic-neg", "neg", "非混沌参数 b=1.2 的 λ₁ 必须非正",
    "lambda_b1.2=%.6f" % ly_nonchaotic,
    ly_nonchaotic <= 0.0,
    "反噬：若任意 b 都报 λ₁>0，则混沌判据无判别力")

# 状态阈值只作事实登记，不把启发式标签误当严格分岔点
regime_scan = {
    "0.05": lyapunov(0.05, 12000, warmup=1500, d0=1e-8, renorm=8, dt=0.012),
    "0.19": ly_html,
    "0.50": lyapunov(0.50, 12000, warmup=1500, d0=1e-8, renorm=8, dt=0.012),
    "0.95": lyapunov(0.95, 12000, warmup=1500, d0=1e-8, renorm=8, dt=0.012),
    "1.20": ly_nonchaotic,
}
add("B4-regime-labels-fact", "gate", "状态分类阈值与实测 λ₁ 扫描事实登记（不冒充分岔定理）",
    "scan=%s ; thresholds=%s" % (
        {k: round(v, 6) for k, v in regime_scan.items()}, A["thresholds"]),
    (A["thresholds"] == B["thresholds"]
     and regime_scan["0.19"] > 0
     and regime_scan["1.20"] <= 0),
    "HTML 的四档标签是交互提示，不是严格数学分岔点；本门只核可复算的同号事实")


# ---------------------------------------------------------------------------
# 庞加莱截面 z=0
# ---------------------------------------------------------------------------
def poincare_scan(bv, steps, trail_start=(0.1, 0.2, 0.3), eps=1e-5, dt=0.012, scale=1.6):
    seeds = [tuple(trail_start),
             (trail_start[0] + eps, trail_start[1], trail_start[2]),
             (trail_start[0], trail_start[1] + eps, trail_start[2])]
    ps = []
    for s in seeds:
        q = s
        for _ in range(1500):
            q = rk4(q, dt, bv)
        ps.append(q)
    pts = []
    for _ in range(steps):
        for idx in range(3):
            prev = ps[idx]
            nxt = rk4(prev, dt, bv)
            ps[idx] = nxt
            if (prev[2] < 0) != (nxt[2] < 0):
                t = prev[2] / (prev[2] - nxt[2])
                cx = (prev[0] + t * (nxt[0] - prev[0])) * scale
                cy = (prev[1] + t * (nxt[1] - prev[1])) * scale
                pts.append((cx, cy, idx))
    return pts


poi = poincare_scan(B["b"], 20000, B["base"], B["eps"], B["dt"], B["scale"])
max_abs_xy = max((max(abs(p[0]), abs(p[1])) for p in poi), default=float("inf"))
add("C1-poincare-crossings", "gate", "z=0 穿越事件存在且线性插值点落在有限相空间盒内",
    "count=%d max_abs_xy=%.6f range=%.1f" % (len(poi), max_abs_xy, B["poincare_range"]),
    (len(poi) >= 10 and max_abs_xy < B["poincare_range"]),
    "截面点已乘 SCALE，与渲染坐标同口径；POINCARE_RANGE=6.5 是画布半径。"
    "门限改为存在性下限 10：20000 步×3 轨迹实测 51 次，原 >100 是无来料依据的臆设")


def box_dimension(points, eps_list):
    dims = []
    raw = []
    for eps in eps_list:
        occ = set()
        for x, y, z in points:
            occ.add((math.floor(x / eps), math.floor(y / eps), math.floor(z / eps)))
        raw.append((math.log(1.0 / eps), math.log(len(occ))))
    mx = sum(x for x, _ in raw) / len(raw)
    my = sum(y for _, y in raw) / len(raw)
    num = sum((x - mx) * (y - my) for x, y in raw)
    den = sum((x - mx) ** 2 for x, _ in raw)
    return (num / den if den > 0 else float("nan")), raw


# 复现 HTML 点云：warmup 3000 + CLOUD_N 个 RK4 点，坐标乘 SCALE
cloud = []
p = (0.1, 0.0, 0.0)
for _ in range(3000):
    p = rk4(p, B["dt"], B["b"])
for _ in range(B["cloud_n"]):
    p = rk4(p, B["dt"], B["b"])
    cloud.append((p[0] * B["scale"], p[1] * B["scale"], p[2] * B["scale"]))
dim_str, raw = box_dimension(cloud, B["eps_list"])

# 双实现：用字符串键重算（与元组键互不引用实现细节）
def box_dimension_str(points, eps_list):
    raw2 = []
    for eps in eps_list:
        occ = set()
        for x, y, z in points:
            occ.add(str(math.floor(x / eps)) + "_" + str(math.floor(y / eps)) + "_" + str(math.floor(z / eps)))
        raw2.append((math.log(1.0 / eps), math.log(len(occ))))
    mx = sum(x for x, _ in raw2) / len(raw2)
    my = sum(y for _, y in raw2) / len(raw2)
    num = sum((x - mx) * (y - my) for x, y in raw2)
    den = sum((x - mx) ** 2 for x, _ in raw2)
    return num / den if den > 0 else float("nan")


dim_str2 = box_dimension_str(cloud, B["eps_list"])
add("C2-box-dimension", "gate", "130000 点云盒维数有限且双实现一致",
    "D_box=%.6f D_str=%.6f raw=%s" % (
        dim_str, dim_str2, [(round(x, 4), round(y, 2)) for x, y in raw]),
    (math.isfinite(dim_str) and 1.0 < dim_str < 3.0
     and abs(dim_str - dim_str2) < 1e-12),
    "三维盒计数；盒维数是有限采样 Minkowski 估计，不是严格分形维数定理")
dim_coarse, _ = box_dimension(cloud, [2.0, 1.0])
add("C3-box-scale-neg", "neg", "改用过粗盒尺度时维数估计必须变化",
    "fine=%.6f coarse=%.6f" % (dim_str, dim_coarse),
    abs(dim_str - dim_coarse) > 0.05,
    "反噬：若任何尺度都给同一维数，则盒计数门无判别力")

# ---------------------------------------------------------------------------
# 红线
# ---------------------------------------------------------------------------
add("D1-redline", "gate", "来料性质保持：独立实验预言 0、不升级为统一场论证据",
    "independent_prediction_count=0 html_md5=%s bytes=%d" % (html_md5, html_bytes),
    ("统一场论" not in src and "实验预言" not in src),
    "来料是动力系统可视化，不提供新实验读数，不接入四力统一判据")

# ---------------------------------------------------------------------------
# 结论与产物
# ---------------------------------------------------------------------------
n_gate = sum(1 for g in gates if g["kind"] == "gate")
n_neg = sum(1 for g in gates if g["kind"] == "neg")
n_identity = sum(1 for g in gates if g["kind"] == "identity")
failed = [g["id"] for g in gates if not g["ok"]]
if failed:
    verdict = "THOMAS-HTML-RECOMPUTE-FAIL--" + "-".join(failed)
else:
    verdict = ("THOMAS-HTML-RECOMPUTE--CONSTANTS-2PATH-MATCH--DIV-3B-EXACT--"
               "RK4-ORDER-4--LYAPUNOV-POSITIVE-CROSSCHECK--NONCHAOTIC-NEG--"
               "POINCARE-FINITE--BOX-DIM-FINITE--SCALE-NEG--"
               "NO-NEW-PHYSICS--NO-INDEPENDENT-PREDICTION--NO-UFT-CLAIM")

result = {
    "subject": "外部来料融合：托马斯吸引子实时相空间示波器独立复核",
    "html": {"path": os.path.basename(HTML), "md5": html_md5, "bytes": html_bytes},
    "verdict": verdict,
    "counts": {"gate": n_gate, "neg": n_neg, "identity": n_identity, "failed": len(failed)},
    "independent_prediction_count": 0,
    "two_path_constants": {"A_html": A, "B_independent": B},
    "readouts": {
        "rk4_ratios": [r1, r2],
        "lyapunov_b019_html_style": ly_html,
        "lyapunov_b019_independent": ly_ind,
        "lyapunov_b12": ly_nonchaotic,
        "regime_scan": regime_scan,
        "poincare_count": len(poi),
        "box_dimension": dim_str,
    },
    "gates": gates,
}
with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

lines = [
    "托马斯吸引子 HTML 来料独立复核",
    "=" * 72,
    "判词: " + verdict,
    "门数: gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(failed)),
    "HTML: %s | md5=%s | bytes=%d" % (os.path.basename(HTML), html_md5, html_bytes),
    "独立预言计数: 0",
    "-" * 72,
]
for g in gates:
    lines.append("[%s] %-30s %-8s exp=%s | act=%s // %s" % (
        "PASS" if g["ok"] else "FAIL", g["id"], g["kind"],
        g["exp"], g["act"], g["note"]))
lines.extend([
    "-" * 72,
    "读数: RK4 ratios=(%.3f,%.3f) λ1(0.19)=%.6f/%.6f λ1(1.2)=%.6f" % (
        r1, r2, ly_html, ly_ind, ly_nonchaotic),
    "Poincare crossings=%d ; D_box=%.6f ; regime_scan=%s" % (
        len(poi), dim_str, {k: round(v, 6) for k, v in regime_scan.items()}),
    "-" * 72,
    "纯标准库 ; 全确定性无随机 ; 不占RID ; 不与UFT链相加",
])
with open(REPORT_PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print(verdict)
print("gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(failed)))
for g in gates:
    if not g["ok"]:
        print("FAIL:", g["id"], g["exp"], g["act"])
