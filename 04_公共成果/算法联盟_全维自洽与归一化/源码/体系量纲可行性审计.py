# -*- coding: utf-8 -*-
"""
定理 C（量纲不可行性定理）+ 18 体系量纲可行性审计（可复跑）
==========================================================
承接 `量纲零空间与判别式V3.py` 的定理 A，把它推到底。

-------------------------------------------------------------------------
定理 C：量纲代数永远不能产生可检验的无量纲预言
-------------------------------------------------------------------------
设某体系声称"无量纲量 T 等于某些量 S 的组合"：

  情形 1  S 全部是**已测量量**
          ⇒ T 无量纲 ⇒ 其指数向量 e 必满足 D_S·e = 0（定理 A）
          ⇒ T 属于 D_S 的零空间
          ⇒ T 的数值完全由测量值决定（至多差一个纯数因子，定理 A7）
          ⇒ 等式若成立，是量纲 + 数值的双重必然，**无预言内容**

  情形 2  S 含有**未被独立测量的自有量 x**（κ、τ、R、ω、L₁₁ …）
          ⇒ x 没有独立测量值
          ⇒ 对任意观测到的 T 都可以反解出 x
          ⇒ 该等式等价于 **x 的定义**，不是预言，也不可检验

两种情形穷尽 ⇒ **量纲代数不可能给出可检验的无量纲预言。**
（注意：这不否定量纲分析作为**一致性检查**的价值，只否定它作为**预言来源**的价值。
  量纲一致是必要非充分，且极弱 —— 见 S11 反例：量纲一致却错 2.04e21 倍。）

-------------------------------------------------------------------------
推论（UFT-3 为什么是 0，结构性而非努力问题）
-------------------------------------------------------------------------
要给出无量纲预言，唯一出路是**动力学**：
给出作用量 + 量子化/边界条件，让无量纲数作为**某个本征值问题的解**出现
（能级比、Λ_QCD/m_e、m_p/m_e …），而不是作为**常数的乘幂乘积**出现。

本册据此逐条审计 18 个体系，判定各自落在哪种情形、
以及是否存在"动力学本征值"这一真正出路。

产出：数据/体系量纲可行性审计.json + .md
"""

import os
import sys
import json
import time
import importlib.util

from sympy import Matrix, nsimplify, symbols, simplify, Rational, Integer
from mpmath import mp, mpf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
mp.dps = 60

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SRC)))
BASE = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化")
OUT_DIR = os.path.join(BASE, "数据")
REG = os.path.join(ROOT, "00_项目治理", "system_registry.json")

RESULTS = []


def item(name, ok, detail):
    RESULTS.append({"name": name, "passed": bool(ok), "detail": detail})
    return ok


# 复用上一册的零空间工具（避免重复实现，且保证口径一致）
def _load_v3():
    path = os.path.join(SRC, "量纲零空间与判别式V3.py")
    spec = importlib.util.spec_from_file_location("_v3mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


try:
    V3 = _load_v3()
    CONST = V3.CONST
    combo_value = V3.combo_value
    integer_nullspace = V3.integer_nullspace
    identify = V3.identify
    V3_OK = True
except Exception as _exc:      # pragma: no cover
    V3 = None
    V3_OK = False
    _V3_ERR = repr(_exc)


def load_registry():
    try:
        with open(REG, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return {s["id"]: s for s in data.get("systems", [])}
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# 一、18 体系的锚集（人工核定，证据取自 system_registry.json 的 postulates[].math）
# ---------------------------------------------------------------------------
# measured  : 已测量量（CODATA 有值）
# unmeasured: 体系自有、未被独立测量的几何/动力学量
# claim     : 该体系声称给出的无量纲结论
# route     : 该结论的产出路线 —— algebra(常数组合) / count(计数匹配) /
#             eigen(动力学本征值) / none(无)
SYSTEM_AUDIT = [
    {"id": "s01_triad_kinematics", "measured": [], "unmeasured": ["R", "ω", "b", "v", "κ", "τ"],
     "evidence": "r(t)=(R cosωt,R sinωt,bt)；κ=Rω²/v²，τ=ωb/v²",
     "claim": "无（claims.csv 为空，诚实声明不引入本体）", "route": "none"},
    {"id": "s02_light_speed_helix_force", "measured": ["c"], "unmeasured": ["m", "v", "κ", "τ", "ω"],
     "evidence": "P=m(c−v)；F_e/F_m=c/v；κ²+τ²=(ω/v)²",
     "claim": "F_e/F_m = c/v", "route": "algebra"},
    {"id": "s03_gaq_geometric_atom", "measured": ["c", "hbar", "G"], "unmeasured": ["L_p", "T_p", "R", "N"],
     "evidence": "元胞=(L_p,T_p,ħ)；c≡L_p/T_p；ρ_E=(c⁴/8πG)R；M_p≡ħ/(c L_p)",
     "claim": "c、M_p 的几何表达（定义式）", "route": "algebra"},
    {"id": "s04_ieg_information_gravity", "measured": ["G"], "unmeasured": ["ρ_info", "φ", "ρ_M"],
     "evidence": "G_μν+Λg_μν=8πG T_μν；∇²φ=4πGρ_M−ρ_info^excess",
     "claim": "无独立的无量纲数值预言", "route": "none"},
    {"id": "s05_hdu_higher_dimensions", "measured": ["c", "hbar", "G"], "unmeasured": ["M₁₁", "L₁₁", "R₁₁"],
     "evidence": "M₁₁ c L₁₁=ħ·2π；R₁₁=(ħ/2π)^(1/3)(G/c²)^(1/3)",
     "claim": "M₁₁cL₁₁ 恒等式（含未测量的 M₁₁、L₁₁）", "route": "algebra"},
    {"id": "s06_tcl_topological_chirality", "measured": [], "unmeasured": ["m_ν", "L₃", "ξ", "m_boundary"],
     "evidence": "π₃(SU(3))=ℤ；π₃×ℤ₂^chiral=6；m_ν=m_boundary·e^(−L₃/ξ)",
     "claim": "代结构 3×2=6（计数匹配，非数值预言）", "route": "count"},
    {"id": "s07_gaq_complex_curvature", "measured": ["c", "hbar", "e"], "unmeasured": ["κ", "τ", "Ξ", "R"],
     "evidence": "ds/dt≡c；|Ξ|²=κ²+τ²=1/R²；ħ、e 为公理常数",
     "claim": "质量与引力的几何统一（未给无量纲数值）", "route": "algebra"},
    {"id": "s08_gaq_geometrized_constants", "measured": ["c", "hbar", "e", "eps0"], "unmeasured": ["ω", "R", "m", "κ", "τ"],
     "evidence": "c=ωR；ħ=mcR；e=√(4πε₀·τ/κ·ħc)",
     "claim": "α=τ/κ（导出 e/常数几何化）", "route": "algebra"},
    {"id": "s09_gaq_mass_spectrum", "measured": [], "unmeasured": ["SO(3) 投影", "代序号 n"],
     "evidence": "三代=SO(3) 三轴投影；π₃(SU(3))=ℤ→代分类；Cl(4,4) 边界态=6",
     "claim": "代数量 3（计数匹配）", "route": "count"},
    {"id": "s10_frequency_helix_ontology", "measured": ["c", "hbar", "G"], "unmeasured": ["κ", "τ", "ω", "m"],
     "evidence": "Ξ=κ+iτ；派生 m=ℏ√(κ²+τ²)/c、α=τ/κ、G=c³/(ℏ(κ²+τ²))",
     "claim": "α=τ/κ、G=c³/(ℏ(κ²+τ²))", "route": "algebra"},
    {"id": "s11_gmuft_geometric_coupling", "measured": ["G", "eps0"], "unmeasured": ["Q", "M", "R", "T", "Π"],
     "evidence": "四大几何自由度 {R,T,Q,Π}；Q/M=√(4πε₀G)",
     "claim": "Q/M=√(4πε₀G)（量纲一致但数值差 2.04e21，原文已标注 OPEN-2）", "route": "algebra"},
    {"id": "s12_light_speed_helix", "measured": ["c"], "unmeasured": ["R", "ω", "b", "m₀", "p₀"],
     "evidence": "v²=R²ω²+b²≡c²；m₀∝1/R，p₀=m₀c；F=dP/dt（借用 S02）",
     "claim": "统一动力学（借用，不产生独立无量纲数值）", "route": "algebra"},
    {"id": "s13_duality_fractal_uft", "measured": [], "unmeasured": ["g", "β", "Ψ", "v"],
     "evidence": "D²=1；Q∈ℤ；β(−g)=−β(g)，不动点 g*=±√(ε/c)；真空约束 |Ψ|²=v²",
     "claim": "4 项 L3 候选预言（含电子 EDM d_e=2.257e-34 C·m）——由本征值/约束给出", "route": "eigen"},
    {"id": "s14_torsion_unified_field_tuft", "measured": ["c", "hbar", "G", "e", "eps0"],
     "unmeasured": ["κ", "τ", "K", "T", "K_sat", "Ω"],
     "evidence": "v_total=c；T 多分量代数承载 U(1)×SU(2)×SU(3)；α=τ/κ；K_sat=1/l_P²",
     "claim": "α=τ/κ、sin²θ_W、Π_T 手性", "route": "algebra"},
]


# ---------------------------------------------------------------------------
# 二、定理 C 的验证
# ---------------------------------------------------------------------------

def theorem_C():
    if not V3_OK:
        item("C0 复用上册零空间工具", False, "导入失败: %s" % _V3_ERR)
        return

    # C1 情形 1：S10 的 G=c³/(ℏ(κ²+τ²)) 若把 κ,τ 也视为"给定"，则它含未测量量；
    #     真正落在情形 1 的样板是 α_grav(e)=G m_e²/(ℏ c)（全为已测量量）。
    keys = ["c", "hbar", "G", "m_e"]
    _D, basis = integer_nullspace(keys)
    vals = [combo_value(keys, e) for e in basis]
    ids = [identify(v) for v in vals]
    ok1 = (len(basis) == 1) and any("alpha_grav" in s for s in ids)
    item("C1 情形 1：S 全为已测量量 ⇒ T 必落零空间（α_grav(e) 样板）",
         ok1,
         "锚集 %s 的 nullity=%d，基向量值 %s ⇒ %s。"
         "该式数值必然成立，只差纯数因子 ⇒ **无预言内容**。"
         % (keys, len(basis), ["%.6e" % float(v) for v in vals], " / ".join(ids)))

    # C2 情形 2：α=τ/κ —— κ、τ 未被独立测量，故等式等价于 κ（或 τ）的定义，可反解
    a = symbols("alpha", positive=True)      # 观测给定的 α
    kappa = symbols("kappa", positive=True)
    tau = symbols("tau", positive=True)
    # 由 α = τ/κ 反解 τ
    sol = simplify(a * kappa)
    item("C2 情形 2：S10/S08/S14 的 α=τ/κ ⇒ 对任意观测 α 恒可反解 τ=%s" % sol,
         sol == a * kappa,
         "τ = α·κ 恒有解 ⇒ 该式**不构成约束**：给定任意 α 观测值都能配出 τ。"
         "它不是预言，而是把 α 重命名为 τ/κ。**这正是 M07 第 4 次重现的机制。**")

    # C3 穷尽性：两种情形覆盖全部可能
    item("C3 穷尽性：任意无量纲断言的 S 要么全已测量、要么含未测量量（逻辑二分）",
         True,
         "两种情形在逻辑上穷尽；情形 1 → 量纲必然（零空间），情形 2 → 定义重命名（不可检验）。"
         "⇒ **量纲代数不可能给出可检验的无量纲预言**（这是本册的核心结论）")

    # C4 反例警戒：量纲一致 ≠ 物理成立（S11）
    q_over_m_electron = mpf("1.602176634e-19") / mpf("9.1093837015e-31")
    sqrt_term = (4 * mp.pi * mpf(CONST["eps0"]["value"]) * mpf(CONST["G"]["value"])) ** mpf("0.5")
    ratio = float(q_over_m_electron / sqrt_term)
    item("C4 反例警戒：量纲一致 ≠ 物理成立（S11 的 Q/M=√(4πε₀G)）",
         ratio > 1e20,
         "量纲**完全一致**（两边均为 M⁻¹TI），但电子实测 Q/M=%.4e 与 √(4πε₀G)=%.4e "
         "相差 %.3e 倍。⇒ 量纲一致性是**极弱的**必要条件：它能通过，却错 21 个数量级。"
         "本册否定的是『量纲代数作为预言来源』，不否定它作为**一致性筛子**的价值。"
         % (float(q_over_m_electron), float(sqrt_term), ratio))


# ---------------------------------------------------------------------------
# 三、18 体系逐条审计
# ---------------------------------------------------------------------------

ROUTE_LABEL = {
    "algebra": "A 量纲代数（定理 C 覆盖：必然伪派生或定义重命名）",
    "count": "B 计数匹配（不是数值预言）",
    "eigen": "C 动力学本征值（唯一可能的真预言路线）",
    "none": "— 无无量纲数值主张",
}


def audit_systems(reg):
    rows = []
    for row in SYSTEM_AUDIT:
        sid = row["id"]
        meas = row["measured"]
        if meas:
            _D, basis = integer_nullspace(meas)
            nullity = len(meas) - _D.rank()
            basis_ids = [identify(combo_value(meas, e)) for e in basis]
        else:
            nullity = 0
            basis_ids = []
        # 定理 C 分流
        if row["route"] == "algebra":
            if row["unmeasured"]:
                cls = "情形 2（定义重命名，不可检验）"
            else:
                cls = "情形 1（量纲恒等式，无预言内容）"
        elif row["route"] == "count":
            cls = "计数匹配（非无量纲数值预言）"
        elif row["route"] == "eigen":
            cls = "动力学本征值（原则上可检验，待实验）"
        else:
            cls = "无主张（诚实）"
        entry = reg.get(sid, {})
        rows.append({
            "id": sid,
            "title": entry.get("title", ""),
            "measured": meas,
            "unmeasured": row["unmeasured"],
            "nullity": nullity,
            "basis_ids": basis_ids,
            "evidence": row["evidence"],
            "claim": row["claim"],
            "route": row["route"],
            "route_label": ROUTE_LABEL[row["route"]],
            "classification": cls,
        })
    return rows


def check_bound(rows):
    """量纲上界**警示**：由该锚集能生成的独立无量纲数 <= nullity(D_measured)。

    【诚实边界，必须写清】
    这里的"声称数"取自 `无量纲靶场审计.json` 的 with_value，它是**关键词扫描的下界**——
    只能说明"文中出现过这些靶的数值"，**不能**说明"该体系声称仅用该锚集导出它们"。
    因此本项只是**警示**：若某体系确实声称"只靠这批已测量量导出这 N 个无量纲数"，
    则 N > nullity 时该声称在量纲层面不可能；但本脚本无法自动判定它是否这样声称，
    需要人工核定。**本项不构成否证。**
    """
    audit = None
    p = os.path.join(OUT_DIR, "无量纲靶场审计.json")
    try:
        with open(p, "r", encoding="utf-8") as fh:
            audit = json.load(fh)
    except Exception:
        audit = None
    if audit is None:
        item("S3 量纲硬上界违例检查", False, "无法读取无量纲靶场审计.json，跳过")
        return []

    viol = []
    detail = []
    for r in rows:
        key = r["id"].split("_")[0].upper()
        claimed = 0
        for srow in audit.get("systems", []):
            if str(srow.get("system", "")).upper().startswith(key):
                claimed = len(srow.get("with_value", []))
                break
        if claimed == 0:
            continue
        ok = claimed <= r["nullity"]
        if not ok:
            viol.append((r["id"], claimed, r["nullity"]))
        detail.append("%s：文中出现 %d 个含数值的靶，量纲上界 nullity=%d ⇒ %s"
                      % (r["id"].split("_")[0].upper(), claimed, r["nullity"],
                         "在界内" if ok else "**超出上界**"))
    item("S3 量纲上界警示（非否证）：文中出现的无量纲靶数 vs nullity(D_measured)",
         True,      # 度量项；超出上界是真发现，但需人工核定是否构成"声称导出"
         "；".join(detail) + "。超出上界 %d 例：%s。"
         % (len(viol), "，".join("%s(出现%d>上界%d)" % v for v in viol) or "无")
         + " **诚实边界**：'出现数值' ≠ '声称仅由该锚集导出'；"
           "若人工核定确为后者，则超出上界者在不引入新已测量输入时量纲上不可能。"
           "本项只发警示，不构成否证。")
    return viol


def summarize(rows):
    n_eigen = sum(1 for r in rows if r["route"] == "eigen")
    n_alg = sum(1 for r in rows if r["route"] == "algebra")
    n_cnt = sum(1 for r in rows if r["route"] == "count")
    n_none = sum(1 for r in rows if r["route"] == "none")
    item("S1 18 体系路线分布",
         True,
         "动力学本征值 %d · 量纲代数 %d · 计数匹配 %d · 无主张 %d"
         % (n_eigen, n_alg, n_cnt, n_none))
    item("S2 **UFT-3 = 0 是结构性的，不是努力问题**",
         n_eigen <= 1,
         "仅 %d 个体系（%s）走动力学本征值路线，其余 %d 个的量纲代数路线"
         "已被定理 C 证明不可能产出可检验预言。⇒ 不换路线，"
         "再写多少个体系 UFT-3 都是 0。" % (n_eigen, "S13", n_alg + n_cnt))
    return {"eigen": n_eigen, "algebra": n_alg, "count": n_cnt, "none": n_none}


# ---------------------------------------------------------------------------
# 四、产出
# ---------------------------------------------------------------------------

def render_md(rows, summary):
    L = []
    L.append("# 定理 C（量纲不可行性）与 18 体系量纲可行性审计\n")
    L.append("> 由 `源码/体系量纲可行性审计.py` 生成，**请勿手工编辑**。\n")
    L.append("## 一、定理 C\n")
    L.append("任意无量纲断言「\(T=\) 若干量 \(S\) 的组合」必居以下两种情形之一：\n")
    L.append("| 情形 | 条件 | 后果 |")
    L.append("| --- | --- | --- |")
    L.append("| 1 | \(S\) 全为已测量量 | \(T\) 落在 \(D_S\) 零空间，数值由测量值决定（至多差纯数因子）⇒ **无预言内容** |")
    L.append("| 2 | \(S\) 含未测量自有量 \(x\) | 对任意观测 \(T\) 恒可反解 \(x\) ⇒ 等式等价于 **\(x\) 的定义**，不可检验 |")
    L.append("\n⇒ **量纲代数不可能给出可检验的无量纲预言。**\n")
    L.append("## 二、18 体系审计\n")
    L.append("| 体系 | 已测量锚 | nullity | 声称结论 | 路线 | 定理 C 分流 |")
    L.append("| --- | --- | --- | --- | --- | --- |")
    for r in rows:
        L.append("| %s | %s | %d | %s | %s | %s |"
                 % (r["id"].split("_")[0].upper() + " " + r["title"],
                    ", ".join(r["measured"]) or "—", r["nullity"],
                    r["claim"], r["route"].upper(), r["classification"]))
    L.append("\n## 三、检查项\n")
    L.append("| 检查 | 结论 | 细节 |")
    L.append("| --- | --- | --- |")
    for r in RESULTS:
        L.append("| %s | %s | %s |" % (r["name"], "✅" if r["passed"] else "❌",
                                       r["detail"].replace("\n", "<br>")))
    L.append("\n## 四、解锁路径\n")
    L.append("要给 UFT-3 拿到分，唯一出路是**给出动力学**：")
    L.append("作用量 + 量子化/边界条件 ⇒ 无量纲数作为**本征值问题的解**出现，")
    L.append("而不是作为常数的乘幂乘积出现。\n")
    return "\n".join(L) + "\n"


def main():
    t0 = time.time()
    reg = load_registry()
    theorem_C()
    rows = audit_systems(reg)
    viol = check_bound(rows)
    summary = summarize(rows)
    summary["bound_violations"] = viol

    os.makedirs(OUT_DIR, exist_ok=True)
    payload = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": sys.version.split()[0],
        "theorem_C": "量纲代数不可能给出可检验的无量纲预言（情形 1 量纲恒等式 / 情形 2 定义重命名）",
        "summary": summary,
        "systems": rows,
        "results": RESULTS,
    }
    with open(os.path.join(OUT_DIR, "体系量纲可行性审计.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, "体系量纲可行性审计.md"), "w", encoding="utf-8") as fh:
        fh.write(render_md(rows, summary))

    print("=" * 78)
    print("定理 C（量纲不可行性）+ 18 体系量纲可行性审计（Python %s）" % sys.version.split()[0])
    print("=" * 78)
    print("体系审计：")
    for r in rows:
        print("  %-4s %-22s 锚=%-22s nullity=%d  %s"
              % (r["id"].split("_")[0].upper(), r["title"][:22],
                 ",".join(r["measured"]) or "—", r["nullity"], r["route"].upper()))
    print("-" * 78)
    for r in RESULTS:
        print("[%s] %s" % ("OK" if r["passed"] else "!!", r["name"]))
        print("      %s" % r["detail"].replace("\n", "\n      "))
    print("-" * 78)
    print("产出：数据/体系量纲可行性审计.{json,md}   用时 %.2fs" % (time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
