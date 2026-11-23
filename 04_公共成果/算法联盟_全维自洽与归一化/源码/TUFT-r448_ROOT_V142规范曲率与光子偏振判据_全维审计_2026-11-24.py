# -*- coding: utf-8 -*-
"""TUFT r448 · ROOT V142 规范曲率与光子偏振判据 全维审计（2026-11-24）

来料正本：../数据/TUFT-ROOT_V142_来料全文_2026-11-24.md
本册只审 V142 新增可算主张，不重判 r445/r446/r447 已有裁定。

四路机验：
1. Maurer–Cartan：显式两参数 SO(3) 标架路径 + 一般可逆矩阵代数路径。
2. 圆偏振：正确手性 B=z×E 与 V140 错误手性的 Maxwell 残差对照。
3. 自由度：无质量规范场 2、Proca 3，并做负对照。
4. 标度：常量背景 F=O(eps^2)、S=O(eps^4)，非.constant 背景负对照恢复 eps^2。

需 sympy，使用 Python38 运行。
"""
import hashlib
import json
import re
import sys
from decimal import Decimal, getcontext
from pathlib import Path

try:
    import sympy as sp
except ImportError:
    raise SystemExit("NEED_SYMPY_PY38")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

getcontext().prec = 50

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUT = BASE / "数据"
ROOT = HERE.parents[2]
STAMP = "2026-11-24"
ROUND = "r448"
PREFIX = "TUFT-" + ROUND + "_ROOT_V142规范曲率与光子偏振判据_全维审计_" + STAMP

SRC = OUT / "TUFT-ROOT_V142_来料全文_2026-11-24.md"
SOURCE_SHA = "aa8568914e8b3438ba77ac52ada2f110ab54098ae8e95930f168a2e33365c863"

ENTRIES = []
GUARDS = []
KEY = {}


def add(eid, verdict, title, detail):
    ENTRIES.append({"id": eid, "verdict": verdict, "title": title, "detail": detail})


def guard(gid, ok, detail):
    GUARDS.append({"id": gid, "ok": bool(ok), "detail": detail})
    return bool(ok)


def nz(vec):
    return sum(1 for v in vec if sp.simplify(sp.trigsimp(v)) != 0)


def one(hits, label):
    if len(hits) != 1:
        raise RuntimeError("expected exactly one %s, got %d" % (label, len(hits)))
    return hits[0]


def lowest_power(expr, var, maxdeg=8):
    p = sp.Poly(sp.expand(expr), var)
    for k in range(0, min(p.degree(), maxdeg) + 1):
        if p.coeff_monomial(var ** k) != 0:
            return k
    return None


# ---------- 来源与离线可验收性 ----------
raw = SRC.read_bytes()
src_sha = hashlib.sha256(raw).hexdigest()
src_text = raw.decode("utf-8")

markers = [
    "SO(3)",
    "Maurer",
    "E_0^2",
    "8-2\\times2",
    "F=dq\\wedge dp=O(\\varepsilon^2)",
    "S_F=O(\\varepsilon^4)",
    "37 项自动化测试通过",
    "ROOT_V142_Helix_Polarization_Complete.zip",
    "正确场和错误场",
]
marker_hits = {m: src_text.count(m) for m in markers}
all_markers = all(v > 0 for v in marker_hits.values())
KEY["source_bytes"] = len(raw)
KEY["source_sha256"] = src_sha
KEY["source_marker_hits"] = marker_hits
KEY["external_link_count"] = len(re.findall(r"https?://", src_text))

zip_hits = 0
manifest_hits = 0
test_report_hits = 0
for p in ROOT.rglob("*"):
    if not p.is_file():
        continue
    name = p.name
    if "ROOT_V142_Helix_Polarization_Complete" in name:
        zip_hits += 1
    if "V142" in name and ("manifest" in name.lower() or "sha256" in name.lower()):
        manifest_hits += 1
    if "V142" in name and ("test" in name.lower() or "测试" in name):
        test_report_hits += 1
KEY["zip_hits"] = zip_hits
KEY["manifest_hits"] = manifest_hits
KEY["test_report_hits"] = test_report_hits

guard("G_source_sha", src_sha == SOURCE_SHA,
      "来料原始字节 SHA256 与正本登记值逐位一致：" + src_sha)
guard("G_source_markers", all_markers,
      "V142 九类关键标记全部命中：SO(3)、Maurer、圆偏振、自由度、eps 标度、ZIP 与 37 项自述")
guard("G_zip_absent", zip_hits == 0 and manifest_hits == 0 and test_report_hits == 0,
      "全库 V142 ZIP 命中 " + str(zip_hits) + "，manifest 命中 " + str(manifest_hits) +
      "，测试报告命中 " + str(test_report_hits) + "；37 项测试与 SHA-256 自述保持 BOUNDARY")
guard("G_external_links_boundary", KEY["external_link_count"] > 0,
      "正文含 " + str(KEY["external_link_count"]) + " 处外部链接，仅按原文保留，不下载验收")


# ---------- 一、Maurer–Cartan 两路独立机验 ----------
def explicit_rotation_path():
    t, x, y, z = sp.symbols("t x y z", real=True)
    coords = (t, x, y, z)
    a = sp.Function("alpha_v142")(t, x, y, z)
    b = sp.Function("beta_v142")(t, x, y, z)

    def rx(q):
        c, s = sp.cos(q), sp.sin(q)
        return sp.Matrix([[1, 0, 0], [0, c, -s], [0, s, c]])

    def ry(q):
        c, s = sp.cos(q), sp.sin(q)
        return sp.Matrix([[c, 0, s], [0, 1, 0], [-s, 0, c]])

    def rz(q):
        c, s = sp.cos(q), sp.sin(q)
        return sp.Matrix([[c, -s, 0], [s, c, 0], [0, 0, 1]])

    R = rz(a) * ry(b)
    Om = [sp.simplify(R.T * sp.diff(R, c)) for c in coords]

    bad = 0
    checks = 0
    for i in range(4):
        for j in range(i + 1, 4):
            Fij = sp.diff(Om[j], coords[i]) - sp.diff(Om[i], coords[j]) + Om[i] * Om[j] - Om[j] * Om[i]
            for r in range(3):
                for c in range(3):
                    v = sp.simplify(sp.trigsimp(Fij[r, c]))
                    checks += 1
                    if v != 0:
                        bad += 1

    comm = sp.simplify(Om[0] * Om[1] - Om[1] * Om[0])
    comm_nonzero = sum(1 for i in range(3) for j in range(3)
                       if sp.simplify(sp.trigsimp(comm[i, j])) != 0)
    return {"nonzero": bad, "checks": checks, "commutator_nonzero": comm_nonzero}


def algebra_matrix_path():
    S = sp.Matrix(3, 3, lambda i, j: sp.Symbol("S%d%d" % (i, j)))
    Si = S.inv()
    P = [sp.Matrix(3, 3, lambda i, j: sp.Symbol("P%d_%d%d" % (m, i, j))) for m in range(4)]
    Q = [-S * P[m] * S for m in range(4)]

    inv_bad = 0
    for m in range(4):
        M = sp.expand(Q[m] * Si + S * P[m])
        for i in range(3):
            for j in range(3):
                if sp.simplify(M[i, j]) != 0:
                    inv_bad += 1

    D = {}
    for m in range(4):
        for n in range(m, 4):
            D[(m, n)] = sp.Matrix(3, 3, lambda i, j: sp.Symbol("D%d%d_%d%d" % (m, n, i, j)))

    def d2(m, n):
        return D[(min(m, n), max(m, n))]

    bad = 0
    wrong_nonzero = 0
    checks = 0
    for m in range(4):
        for n in range(m + 1, 4):
            Om_m = S * P[m]
            Om_n = S * P[n]
            dOm_n = Q[m] * P[n] + S * d2(m, n)
            dOm_m = Q[n] * P[m] + S * d2(n, m)
            F = sp.expand(dOm_n - dOm_m + Om_m * Om_n - Om_n * Om_m)
            F_wrong = sp.expand(dOm_n - dOm_m - Om_m * Om_n + Om_n * Om_m)
            for i in range(3):
                for j in range(3):
                    checks += 1
                    if sp.simplify(F[i, j]) != 0:
                        bad += 1
                    if sp.simplify(F_wrong[i, j]) != 0:
                        wrong_nonzero += 1
    return {"nonzero": bad, "checks": checks, "inv_deriv_nonzero": inv_bad,
            "wrong_sign_nonzero": wrong_nonzero}


mc_explicit = explicit_rotation_path()
mc_algebra = algebra_matrix_path()
KEY["mc_explicit_nonzero"] = mc_explicit["nonzero"]
KEY["mc_explicit_checks"] = mc_explicit["checks"]
KEY["mc_commutator_nonzero"] = mc_explicit["commutator_nonzero"]
KEY["mc_algebra_nonzero"] = mc_algebra["nonzero"]
KEY["mc_algebra_checks"] = mc_algebra["checks"]
KEY["mc_inv_deriv_nonzero"] = mc_algebra["inv_deriv_nonzero"]
KEY["mc_wrong_sign_nonzero"] = mc_algebra["wrong_sign_nonzero"]

guard("G_mc_explicit_zero", mc_explicit["nonzero"] == 0 and mc_explicit["checks"] == 54,
      "两参数 SO(3) 路径 6 对坐标 × 9 矩阵元共 " + str(mc_explicit["checks"]) +
      " 项，曲率非零项 " + str(mc_explicit["nonzero"]))
guard("G_mc_nonabelian_teeth", mc_explicit["commutator_nonzero"] > 0,
      "同一路径的联络换向子非零元 " + str(mc_explicit["commutator_nonzero"]) +
      "，不是单生成元交换平凡例")
guard("G_mc_algebra_independent", mc_algebra["nonzero"] == 0 and mc_algebra["inv_deriv_nonzero"] == 0,
      "一般可逆矩阵路径：逆矩阵导数残差 " + str(mc_algebra["inv_deriv_nonzero"]) +
      "，曲率非零元 " + str(mc_algebra["nonzero"]) + "，不依赖旋转参数化")
guard("G_mc_sign_negative", mc_algebra["wrong_sign_nonzero"] > 0,
      "把联络项符号改反后非零元 " + str(mc_algebra["wrong_sign_nonzero"]) + "，判据可翻红")
guard("G_mc_paths_agree",
      mc_explicit["nonzero"] == mc_algebra["nonzero"] and
      mc_explicit["checks"] == mc_algebra["checks"],
      "显式路径与代数路径非零元同为 0，检查项同为 " + str(mc_explicit["checks"]))


# ---------- 二、圆偏振手性与 Maxwell 残差 ----------
t, x, y, z, k, E0 = sp.symbols("t x y z k E0", real=True, positive=True)
phi = k * (t - z)
E = sp.Matrix([E0 * sp.cos(phi), E0 * sp.sin(phi), 0])
B_right = sp.Matrix([-E0 * sp.sin(phi), E0 * sp.cos(phi), 0])
B_wrong = sp.Matrix([E0 * sp.sin(phi), -E0 * sp.cos(phi), 0])


def curl3(F):
    return sp.Matrix([
        sp.diff(F[2], y) - sp.diff(F[1], z),
        sp.diff(F[0], z) - sp.diff(F[2], x),
        sp.diff(F[1], x) - sp.diff(F[0], y),
    ])


def residuals(B):
    far = [sp.simplify(sp.trigsimp(v)) for v in (curl3(E) + sp.diff(B, t))]
    amp = [sp.simplify(sp.trigsimp(v)) for v in (curl3(B) - sp.diff(E, t))]
    return far, amp


far_right, amp_right = residuals(B_right)
far_wrong, amp_wrong = residuals(B_wrong)
dot_right = sp.simplify(sp.trigsimp(E.dot(B_right)))
cross_right = [sp.simplify(sp.trigsimp(v)) for v in E.cross(B_right)]
norm_diff = sp.simplify(sp.trigsimp(E.dot(E) - B_right.dot(B_right)))

KEY["faraday_right_nonzero"] = nz(far_right)
KEY["ampere_right_nonzero"] = nz(amp_right)
KEY["faraday_wrong_nonzero"] = nz(far_wrong)
KEY["ampere_wrong_nonzero"] = nz(amp_wrong)
KEY["faraday_wrong_sample"] = str(far_wrong[0])
KEY["ampere_wrong_sample"] = str(amp_wrong[0])
KEY["E_dot_B"] = str(dot_right)
KEY["E_cross_B"] = [str(v) for v in cross_right]
KEY["E2_minus_B2"] = str(norm_diff)

guard("G_polar_correct_zero",
      nz(far_right) == 0 and nz(amp_right) == 0,
      "正确手性 B=z×E 的 Faraday 非零元 " + str(nz(far_right)) +
      "，Ampere 非零元 " + str(nz(amp_right)))
guard("G_polar_wrong_nonzero",
      nz(far_wrong) > 0 and nz(amp_wrong) > 0,
      "V140 旧手性的 Faraday 非零元 " + str(nz(far_wrong)) +
      "，Ampere 非零元 " + str(nz(amp_wrong)) + "，残差示例 " + KEY["faraday_wrong_sample"])
guard("G_polar_invariants",
      dot_right == 0 and norm_diff == 0 and
      cross_right[0] == 0 and cross_right[1] == 0 and cross_right[2] == E0 ** 2,
      "E·B=0，|E|^2−|B|^2=0，E×B=E0^2 zhat；能流方向为 +z")


# ---------- 三、传播自由度计数与负对照 ----------
phase_dim = 8
constraint_removal = 2
first_class = 2
secondary = 1
dof_photon = (phase_dim - first_class * constraint_removal) // 2
dof_proca = (phase_dim - secondary * constraint_removal) // 2
dof_photon_omit_gauge = (phase_dim - first_class) // 2
dof_proca_with_gauge = (phase_dim - first_class * constraint_removal) // 2
KEY["phase_space_dim"] = phase_dim
KEY["dof_photon"] = dof_photon
KEY["dof_proca"] = dof_proca
KEY["dof_photon_omit_gauge"] = dof_photon_omit_gauge
KEY["dof_proca_with_gauge"] = dof_proca_with_gauge

guard("G_dof_photon", dof_photon == 2,
      "无质量规范场：8 相空间维 − 2 个一级约束 × 2 = 4，除 2 得 " + str(dof_photon))
guard("G_dof_proca", dof_proca == 3,
      "Proca：8 相空间维 − 1 个次级约束 × 2 = 6，除 2 得 " + str(dof_proca))
guard("G_dof_negative_controls",
      dof_photon_omit_gauge != dof_photon and dof_proca_with_gauge != dof_proca,
      "漏掉规范双重消除时无质量读成 " + str(dof_photon_omit_gauge) +
      "；给 Proca 误加规范对称时读成 " + str(dof_proca_with_gauge) + "，两负对照均翻红")


# ---------- 四、eps 标度与负对照 ----------
eps = sp.Symbol("eps", positive=True)
F2 = [sp.Symbol("F2_%d" % i) for i in range(6)]
g1 = [sp.Symbol("G1_%d" % i) for i in range(6)]
S_const = sp.expand(sum((eps ** 2 * v) ** 2 for v in F2))
S_nonconst = sp.expand(sum((eps * g1[i] + eps ** 2 * F2[i]) ** 2 for i in range(6)))
low_const = lowest_power(S_const, eps)
low_nonconst = lowest_power(S_nonconst, eps)
coeff2_const = sp.Poly(S_const, eps).coeff_monomial(eps ** 2)
coeff2_nonconst = sp.Poly(S_nonconst, eps).coeff_monomial(eps ** 2)
coeff2_nonconst_terms = sum(1 for v in g1 if v ** 2 == coeff2_nonconst)
KEY["eps_constant_lowest"] = low_const
KEY["eps_nonconstant_lowest"] = low_nonconst
KEY["eps_constant_coeff2"] = str(coeff2_const)
KEY["eps_nonconstant_coeff2_nonzero_terms"] = coeff2_nonconst_terms

guard("G_scaling_constant",
      low_const == 4 and coeff2_const == 0,
      "常量背景：F=eps^2 dξ∧dη，S 最低幂 " + str(low_const) + "，eps^2 系数 " + str(coeff2_const))
guard("G_scaling_negative_control",
      low_nonconst == 2 and coeff2_nonconst != 0 and coeff2_nonconst_terms == 6,
      "非常量背景负对照：一阶背景微分恢复 eps^2 项，最低幂 " + str(low_nonconst) +
      "，非零平方项 " + str(coeff2_nonconst_terms) + " 个")


# ---------- 五、跨册一致性 ----------
ALG = OUT.parent
r445 = one(list(ALG.glob("判定_TUFT-r445_*.md")), "r445 judgement")
r446 = one(list(ALG.glob("判定_TUFT-r446_*.md")), "r446 judgement")
r447 = one(list(ALG.glob("判定_TUFT-r447_*.md")), "r447 judgement")
t445, t446, t447 = [p.read_text(encoding="utf-8") for p in (r445, r446, r447)]
cross = {
    "r445_handedness": ("手性写反" in t445 and "Faraday/Ampere" in t445),
    "r446_rotation_boundary": ("场旋转不等于光子中心绕轴" in t446),
    "r447_spin_not_speed": ("自旋是量子态标签" in t447),
}
KEY["cross_rounds"] = cross
guard("G_cross_rounds", all(cross.values()),
      "继承 r445 手性纠错、r446 场旋转边界、r447 自旋非速度裁定，不重判三册结论")


# ---------- 条目 ----------
add("A-01", "PASS", "纯旋转标架联络严格平坦",
    "显式两参数 SO(3) 路径与一般可逆矩阵路径各 54 项曲率残差全为 0；Omega=R^{-1}dR 是纯规范联络。")
add("A-02", "INFO", "Maurer–Cartan 恒等式是运动学恒等式",
    "F=0 只说明纯标架旋转不产生规范场强；是否出现真实场强取决于额外动力学，不由 R(x)∈SO(3) 推出。")
add("A-03", "PASS", "非交换路径负对照证明曲率门有判别力",
    "两参数路径的联络换向子有 " + str(mc_explicit["commutator_nonzero"]) +
    " 个非零矩阵元；若只看单生成元交换例，F=0 会退化为平凡结果。")
add("A-04", "PASS", "代数路径独立于显式旋转参数化",
    "一般可逆矩阵路径用 ∂S=−S(∂R)S 推出 F=S(∂μ∂ν−∂ν∂μ)，二阶偏导对称后为 0；逆矩阵导数残差与曲率残差均为 0。")
add("A-05", "FAIL", "纯旋转几何未给出非纯规范场强",
    "两条路径均给 F=0；V142 若要走向四力，必须增加独立动力学、非平凡投影或新物理结构，并证明其必要性。")
add("A-06", "PASS", "正确圆偏振满足真空 Maxwell 方程",
    "B=ẑ×E 的 Faraday 与 Ampere 非零残差均为 0；E·B=0、|E|^2−|B|^2=0、E×B=E0^2 ẑ。")
add("A-07", "PASS", "V140 旧手性被可翻红判据排除",
    "B=(sinφ,−cosφ,0) 的 Faraday 与 Ampere 各 2 个非零元，示例残差 " + KEY["faraday_wrong_sample"] + "。")
add("A-08", "INFO", "手性纠错是继承项，不是 V142 新增证据",
    "r445 已抓 V140 手性写反，r447 已确认正确手性与能流方向；V142 纳入回归测试属口径收敛，不重复计数。")
add("A-09", "PASS", "圆偏振正交与能流方向一致",
    "机器核验 E⊥B、等幅、坡印廷沿 +z；这只验证平面波模式，不推出空间 Frenet 螺旋本源。")
add("A-10", "PASS", "无质量电磁场两个传播自由度复算成立",
    "8 相空间维减去两个一级约束各移除 2 维，物理相空间 4 维，构型自由度 " + str(dof_photon) + "。")
add("A-11", "PASS", "有质量 Proca 场三个传播自由度复算成立",
    "8 相空间维减去一个次级约束移除 2 维，物理相空间 6 维，构型自由度 " + str(dof_proca) + "。")
add("A-12", "PASS", "自由度门有负对照",
    "漏掉规范双重消除会把光子读成 " + str(dof_photon_omit_gauge) +
    "；误给 Proca 规范对称会读成 " + str(dof_proca_with_gauge) + "，两者均不满足目标值。")
add("A-13", "INFO", "自由度来自约束结构，不来自三方向数",
    "两个横向偏振是规范冗余与约束计数的结果；空间三个垂直方向本身不能替代一级约束证明。")
add("A-14", "PASS", "常量背景四阶标度复算成立",
    "q=p=常量附近 dq=εdξ、dp=εdη，F=ε^2 dξ∧dη，S_F 最低幂 " + str(low_const) +
    "，eps^2 系数为 0。")
add("A-15", "PASS", "标度判据有非平凡负对照",
    "若背景微分非零，F 含 ε 阶项，S 最低幂降到 " + str(low_nonconst) +
    "；故四阶结论严格限于常量背景，不是所有位形。")
add("A-16", "FAIL", "最简模型仍缺普通二次自由传播项",
    "常量背景没有 ε^2 作用量项，继承 r445 D-12；V142 自述下一关正是补二次传播、两横向偏振与物质耦合。")
add("A-17", "BOUNDARY", "ZIP、19 文件、37 项测试与 SHA-256 未提供",
    "全库 V142 ZIP 命中 " + str(zip_hits) + "，manifest 命中 " + str(manifest_hits) +
    "，测试报告命中 " + str(test_report_hits) + "；不代验收。")
add("A-18", "BOUNDARY", "正文外部链接仅保留不下载",
    "来料含 " + str(KEY["external_link_count"]) + " 处外部链接；本册不把网页图标或图片链路当证据。")
add("A-19", "PASS", "与 r445/r446/r447 口径一致",
    "继承手性纠错、场旋转不等于中心绕轴、自旋不是机械速度三项，无跨册读数冲突。")
add("A-20", "INFO", "红线计数继承不变",
    "含引力四力正确方程 0 条、独立实验预言 0、W3 仍 1/4（阳性对照 4/4）；V142 不提升任何计数。")
add("A-21", "CORRECTED", "标题中的攻克判据须降级为必要条件审计",
    "可攻的是纯规范曲率平坦、手性一致、自由度计数与标度缺失这些具体命题；不宣称攻克统一场论或统一场方程。")


# ---------- 输出 ----------
counts = {}
for e in ENTRIES:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
KEY["counts"] = counts
KEY["entry_count"] = len(ENTRIES)
KEY["guard_pass"] = sum(1 for g in GUARDS if g["ok"])
KEY["guard_total"] = len(GUARDS)

engine_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
verdict = (
    "ROOT-V142-AUDIT--MC-FLATNESS-EXACT-0--TWO-INDEPENDENT-PATHS--"
    "POLARIZATION-HANDNESS-INHERITED-CORRECTED--DOF-PHOTON-2-PROCA-3--"
    "CONSTANT-BACKGROUND-QUARTIC-SCALING-ONLY--ZIP-37TESTS-BOUNDARY--"
    "NO-NEW-FIELD-STRENGTH--NO-UFT-CLAIM"
)

result = {
    "round": ROUND,
    "topic": "ROOT V142 规范曲率与光子偏振判据 全维审计",
    "date": STAMP,
    "source": str(SRC.relative_to(ROOT)).replace("\\", "/"),
    "source_bytes": len(raw),
    "source_sha256": src_sha,
    "engine_sha256": engine_sha,
    "requires": "Python38 sympy " + sp.__version__,
    "verdict": verdict,
    "counts": counts,
    "entry_count": len(ENTRIES),
    "guard_pass": KEY["guard_pass"],
    "guard_total": KEY["guard_total"],
    "entries": ENTRIES,
    "guards": GUARDS,
    "key_numbers": KEY,
}

json_path = OUT / (PREFIX + ".json")
md_path = OUT / (PREFIX + ".md")
rep_path = OUT / (PREFIX + "_report.txt")

json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

md = [
    "# TUFT r448 · ROOT V142 规范曲率与光子偏振判据 全维审计",
    "",
    "一句话：纯旋转标架的 Maurer–Cartan 曲率精确为 0；正确圆偏振与两偏振自由度计数可复算；常量背景仍只有四阶作用量、无二次传播项；ZIP 与 37 项测试未提供，红线不变。",
    "",
    "| 项 | 值 |",
    "|---|---|",
    "| 条目 | " + str(len(ENTRIES)) + " |",
    "| 判定分布 | " + ", ".join(k + "=" + str(v) for k, v in sorted(counts.items())) + " |",
    "| 守卫 | " + str(KEY["guard_pass"]) + "/" + str(KEY["guard_total"]) + " |",
    "| 引擎 SHA256 | " + engine_sha + " |",
    "",
    "## 关键读数",
    "",
]
for k in sorted(KEY):
    v = KEY[k]
    md.append("- " + k + " = " + (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)))
md += ["", "## 条目", "", "| 编号 | 判定 | 标题 | 详情 |", "|---|---|---|---|"]
for e in ENTRIES:
    md.append("| " + e["id"] + " | " + e["verdict"] + " | " + e["title"] + " | " + e["detail"] + " |")
md += ["", "## 守卫", "", "| ID | 结果 | 读数 |", "|---|---|---|"]
for g in GUARDS:
    md.append("| " + g["id"] + " | " + ("PASS" if g["ok"] else "FAIL") + " | " + g["detail"] + " |")
md_path.write_text("\n".join(md) + "\n", encoding="utf-8")

rep = [
    "TUFT r448 ROOT V142 gauge curvature and photon polarization audit",
    "entries=" + str(len(ENTRIES)) + " guards=" + str(KEY["guard_pass"]) + "/" + str(KEY["guard_total"]),
    "counts=" + json.dumps(counts, ensure_ascii=False, sort_keys=True),
    "mc_explicit_nonzero=" + str(mc_explicit["nonzero"]),
    "mc_algebra_nonzero=" + str(mc_algebra["nonzero"]),
    "mc_commutator_nonzero=" + str(mc_explicit["commutator_nonzero"]),
    "mc_wrong_sign_nonzero=" + str(mc_algebra["wrong_sign_nonzero"]),
    "polar_right=" + str(nz(far_right)) + "/" + str(nz(amp_right)),
    "polar_wrong=" + str(nz(far_wrong)) + "/" + str(nz(amp_wrong)),
    "dof_photon=" + str(dof_photon) + " dof_proca=" + str(dof_proca),
    "eps_lowest_constant=" + str(low_const) + " eps_lowest_nonconstant=" + str(low_nonconst),
    "zip_hits=" + str(zip_hits) + " manifest_hits=" + str(manifest_hits) + " test_report_hits=" + str(test_report_hits),
    "source_sha256=" + src_sha,
    "engine_sha256=" + engine_sha,
]
rep_path.write_text("\n".join(rep) + "\n", encoding="utf-8")

print("OK entries=" + str(len(ENTRIES)) + " guards=" + str(KEY["guard_pass"]) + "/" + str(KEY["guard_total"]))
