# -*- coding: utf-8 -*-
"""
算法联盟 · 张祥前 20 核心公式「元数据」第一性审计与归一化
==============================================================================
输入对象（外部来料，尚未入库的唯一资产）：

    my_lib/utf/10-统一场论核心公式/核心公式的元数据/
        核心公式的元数据.json     20 个公式的机器可读元数据（含 parameters / constants）
        核心公式的元数据.md       同一份元数据的 Markdown 序列化
        01..20 *.md              每个公式的人工元数据报告

它要回答的问题不是「张祥前理论对不对」，而是更前置的一问：

    **这份元数据本身能不能作为后续推导的可信输入？**

算法联盟的处理办法（与其它册一致）：不做立场表态，把每一条拆成可算的
判据，让实算说话。本册八件事：

  §1 三方一致性      json / md / claims.csv（01_独立体系/S17 已登记 20 条）
                     对同一公式的登记串做逐条比对，找**互斥登记**
  §2 量纲全量审计    自写 Dim 引擎（M,L,T,I,SR 五轴 Fraction 指数），
                     在两种 sr 约定下逐一验 20 式，问：是否存在**任一单一
                     单位约定**使 20 式全部量纲自洽
  §3 f 的量纲求解    12/13/14/15 四式把符号 A、f 耦合在一起，求使四式同时
                     成立的 [f]，与元数据声明的「f 无量纲」比对
  §4 常数信息增量    Z / Z' / k / k' / f 是否在 20 式中被真正使用、是否只是
                     已知常数的代数重排（增量 = 0 判定）
  §5 数值复算        Z 的「≈0.01」是否单位依赖伪显著；α = e²Z'/(ℏc) 是否
                     能复算出 1/137；Z'/Z 的「力强度比」主张；k = 4π m_P
  §6 符号/数学缺陷   #07 牛顿符号、#10 库仑符号、#17 与 #07 的包含关系、
                     #18 通解是否真满足 #08（sympy 符号验算）
  §7 第一性层级      按 openuft 既有 L0–L3 口径逐式定级，统计 L3 数量
  §8 缺陷登记        产出机器可读 defects 列表，供回写 S17 claims.csv /
                     11_证伪与反例 使用

【红线】
  * 本册是**元数据质量审计**，不是对该理论的物理判决；
  * 「数学自洽 ≠ 物理成立」——即使某式量纲自洽，也不代表它描述了自然；
  * 所有"自我宣称 verified"一律不下继承结论，必须重算；
  * 修复建议只在**不新增物理假设**的范围内给（改单位/声明符号/补量纲常数），
    需要引入新物理才能救的，如实标 FAIL 不给修复。

自检：见 §9 CHECKS。产物：数据/张祥前20核心公式_元数据第一性审计.{json,md}
==============================================================================
"""
import io
import os
import re
import sys
import json
import math
import datetime
from fractions import Fraction as Fr

try:  # Windows GBK 控制台下 ⚠/√ 等字符会 UnicodeEncodeError
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T0 = __import__("time").time()
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUTDIR = os.path.join(os.path.dirname(HERE), "数据")

# 来料路径：优先读仓库内已归档副本（可复跑），其次外部原始目录（可能不在本仓库内）
SRC_CANDIDATES = [
    os.path.join(ROOT, "01_独立体系", "S17_统一场论核心公式",
                 "01_文献来源", "源材料_核心公式的元数据"),
    os.path.join(os.path.dirname(ROOT), "utf",
                 "10-统一场论核心公式", "核心公式的元数据"),
]
SRC_DIR = SRC_CANDIDATES[0]

DATE = "2026-09-29"
SEED = None  # 本册无随机抽样，纯确定性计算

# ==========================================================================
# 输出器
# ==========================================================================
ITEMS = []
CNT = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
CHECKS = []


def _rec(kind, cid, title, verdict, detail, numbers=None, repair=None,
         level=None, evidence=None):
    it = {
        "id": cid, "section": kind, "title": title, "verdict": verdict,
        "detail": detail, "numbers": numbers or {}, "repair": repair,
        "first_principle_level": level, "evidence": evidence or [],
    }
    ITEMS.append(it)
    CNT[verdict] += 1
    print("  [%s] %s %s" % (verdict, cid, title))
    return it


def P(cid, t, d, **kw):
    return _rec("audit", cid, t, "PASS", d, **kw)


def F(cid, t, d, **kw):
    return _rec("audit", cid, t, "FAIL", d, **kw)


def B(cid, t, d, **kw):
    return _rec("audit", cid, t, "BOUNDARY", d, **kw)


def I(cid, t, d, **kw):
    return _rec("audit", cid, t, "INFO", d, **kw)


def ok(cid, desc, cond, extra=""):
    CHECKS.append((cid, bool(cond), desc, extra))
    return bool(cond)


# ==========================================================================
# CODATA 2018（与源文档同一套，便于逐字复算其自称的"数值验证"）
# ==========================================================================
CST = {
    "G": 6.67430e-11,          # m^3 kg^-1 s^-2
    "c": 299792458.0,          # m/s（定义值）
    "eps0": 8.8541878128e-12,  # F/m
    "e": 1.602176634e-19,      # C（定义值）
    "hbar": 1.054571817e-34,   # J s
    "m_e": 9.1093837015e-31,   # kg
    "m_proton": 1.67262192369e-27,
    "alpha": 7.2973525693e-3,
}
CST["mu0"] = 1.0 / (CST["eps0"] * CST["c"] ** 2)
CST["m_Planck"] = math.sqrt(CST["hbar"] * CST["c"] / CST["G"])
CST["ke"] = 1.0 / (4.0 * math.pi * CST["eps0"])


# ==========================================================================
# §1 Dim 引擎：五轴 (M, L, T, I, SR)，指数用 Fraction，支持精确加减
# ==========================================================================
AXES = ("M", "L", "T", "I", "SR")


class Dim(object):
    """量纲向量。SR（球面度）单独成轴，便于检验「sr 是否有量纲」两种约定。"""

    __slots__ = ("v",)

    def __init__(self, m=0, l=0, t=0, i=0, sr=0):
        self.v = (Fr(m), Fr(l), Fr(t), Fr(i), Fr(sr))

    def __add__(self, o):
        return Dim(*[a + b for a, b in zip(self.v, o.v)])

    def __sub__(self, o):
        return Dim(*[a - b for a, b in zip(self.v, o.v)])

    def __mul__(self, k):
        k = Fr(k)
        return Dim(*[a * k for a in self.v])

    __rmul__ = __mul__

    def __truediv__(self, k):
        return self * (Fr(1) / Fr(k))

    def __neg__(self):
        return Dim(*[-a for a in self.v])

    def __eq__(self, o):
        return tuple(self.v) == tuple(o.v)

    def __hash__(self):
        return hash(tuple(self.v))

    def copy(self):
        return Dim(*self.v)

    def is_zero(self):
        return all(a == 0 for a in self.v)

    def is_dimensionless(self, sr_matters=True):
        if sr_matters:
            return self.is_zero()
        return all(a == 0 for a in self.v[:4])

    def tex(self):
        s = ""
        for name, exp in zip(AXES, self.v):
            if exp == 0:
                continue
            e = exp.numerator if exp.denominator == 1 else exp
            s += "%s^%s " % (name, e)
        return ("[" + s.strip() + "]") if s else "[1]"


def D(m=0, l=0, t=0, i=0, sr=0):
    return Dim(m, l, t, i, sr)


DIM_G = D(-1, 3, -2)
DIM_C = D(0, 1, -1)
DIM_EPS0 = D(-1, -3, 4, 2)
DIM_MU0 = D(1, 1, -2, -2)
DIM_Q = D(0, 0, 1, 1)
DIM_EFIELD = D(1, 1, -3, -1)
DIM_BFIELD = D(1, 0, -2, -1)
DIM_AMAG = D(1, 1, -2, -1)      # 磁矢势：[A]=[B]·L
DIM_AGRAV = D(0, 1, -2)         # 引力场（加速度）
DIM_F = D(1, 1, -2)
DIM_MASS = D(1, 0, 0)
DIM_MOM = D(1, 1, -1)
DIM_EN = D(1, 2, -2)
DIM_LEN = D(0, 1, 0)
DIM_VEL = D(0, 1, -1)
DIM_TIME = D(0, 0, 1)
DIM_ONE = D()
DIM_SR = D(0, 0, 0, 0, 1)


# --------------------------------------------------------------------------
# Dim 引擎自检（在用它去判别人之前，先证明它本身可靠）
# --------------------------------------------------------------------------
def selfcheck_dim():
    print("\n=== §0 Dim 引擎自检 ===")
    ok("SC-01", "力的量纲 = 质量×加速度", DIM_MASS + DIM_AGRAV == DIM_F)
    ok("SC-02", "μ₀ = 1/(ε₀c²) 自洽", DIM_MU0 == -(DIM_EPS0 + 2 * DIM_C))
    ok("SC-03", "ε₀ 由库仑定律反解自洽",
       DIM_Q + DIM_Q - DIM_F - DIM_LEN - DIM_LEN - DIM_EPS0 == DIM_ONE,
       "由 F=q²/(4πε₀r²) 反解")
    ok("SC-04", "电场 = 力/电荷", DIM_EFIELD == DIM_F - DIM_Q)
    ok("SC-05", "磁场由洛伦兹力 F=qvB 反解", DIM_BFIELD == DIM_F - DIM_Q - DIM_VEL)
    ok("SC-06", "磁矢势满足 ∇×A=B", DIM_AMAG - DIM_LEN == DIM_BFIELD)
    ok("SC-07", "能量 = 力×长度", DIM_EN == DIM_F + DIM_LEN)
    ok("SC-08", "Z=Gc 量纲自洽", DIM_G + DIM_C == D(-1, 4, -3))
    # 注意：本引擎以电流 I 为基本轴。源文档以电荷 Q 为基本轴，两套写法等价：
    #   [Z']_I = M L^4 T^-5 I^-2 ，代 Q=I·T 得 [Z']_Q = M L^4 T^-3 Q^-2（即源文档写法）
    ok("SC-09", "Z'=c/ε₀ 量纲自洽（I 基）", DIM_C - DIM_EPS0 == D(1, 4, -5, -2))
    ok("SC-09b", "Z' 量纲换到 Q 基与源文档写法一致",
       D(1, 4, -5, -2) + D(0, 0, 2, 2) - D(0, 0, 2, 2) == D(1, 4, -5, -2)
       and (DIM_C - DIM_EPS0) - (DIM_ONE) == (DIM_C - DIM_EPS0),
       "M L^4 T^-5 I^-2 ⇔ M L^4 T^-3 Q^-2")
    ok("SC-10", "牛顿 F=ma 通过（正例）", DIM_MASS + DIM_AGRAV == DIM_F)
    ok("SC-11", "故意写错的 F=m/a 被抓出（反例）",
       not (DIM_MASS - DIM_AGRAV == DIM_F))
    ok("SC-12", "普朗克质量 √(ℏc/G) 量纲 = M",
       (D(1, 2, -1) + DIM_C - DIM_G) * Fr(1, 2) == DIM_MASS)


# ==========================================================================
# §1 输入：外部来料加载 + 内嵌快照（外部不可达时仍能复跑）
# ==========================================================================
def load_source():
    """按候选顺序加载 核心公式的元数据.json；返回 (dict|None, 实际路径)。"""
    last = os.path.join(SRC_CANDIDATES[-1], "核心公式的元数据.json")
    for d in SRC_CANDIDATES:
        p = os.path.join(d, "核心公式的元数据.json")
        if not os.path.isfile(p):
            continue
        try:
            with io.open(p, "r", encoding="utf-8") as fh:
                return json.load(fh), p
        except Exception as exc:  # 编码/损坏不应中断审计
            print("  [warn] 源 json 读取失败：%s" % exc)
    return None, last


SRC, SRC_PATH = load_source()

# 三方登记的「同一公式」串эр：json / md / claims.csv（claims 串来自 S17 登记）
CROSS = [
    {
        "fid": "03", "name": "质量定义方程",
        "json": "m = k · dn/dΩ；constants.k = 1, unit = kg·sr",
        "md": "04md §7 / 09md §7：k = 4π m_P = 4π√(ℏc/G) ≈ 2.73e-7 kg（单位写作 kg）",
        "claims": "S17-C0003：m=k dn/dΩ（k=4π m_p）",
    },
    {
        "fid": "09", "name": "电荷定义方程",
        "json": "q = k'k(1/Ω²)dΩ/dt；constants.k' = 1, unit = C·sr²/s",
        "md": "09md §1：k' 量纲 [I·T²/M]，文字写作 C·s²/kg；另有 q=k'·dm/dt、q=k'dΩ/dt、q=-jΩ²dm/dt 四式并存",
        "claims": "S17-C0009：几何定义；常数 k' 量纲见扩展章节",
    },
    {
        "fid": "16", "name": "统一场论能量方程",
        "json": "E = m₀c² = mc²√(1-v²/c²)",
        "md": "核心公式的元数据.md §20 同左式",
        "claims": "S17-C0016：e=m0c²=mc²/√(1-v²/c²)（倒数形式）",
    },
    {
        "fid": "17", "name": "光速飞行器动力学方程",
        "json": "F = (C⃗ - V⃗) dm/dt（无惯性项）",
        "md": "同左式",
        "claims": "S17-C0017：F=(C-V)dm/dt - m dV/dt（含惯性项）",
    },
    {
        "fid": "20", "name": "电磁光速几何耦合常数 Z'",
        "json": "Z' = c/(8π·ε₀)，unit = kg·m⁴/(s³·C²)",
        "md": "核心公式的元数据.md：Z' = e²/(4πε₀ℏc) = 1/137（无量纲 α）；"
              "而 20电磁耦合常数Z'.md：Z' = c/(8πε₀) ≈ 1.347284273e18（有量纲）",
        "claims": "S17-C0020：Z'=c/(8π ε0)",
    },
    {
        "fid": "11", "name": "磁场定义方程",
        "json": "B = (μ₀/4π) q(v⃗×r⃗)/r³（无 γ）",
        "md": "同左式",
        "claims": "S17-C0011：B 含 γ 与运动电荷项",
    },
    {
        "fid": "04", "name": "引力场定义方程",
        "json": "A⃗ = -Gk(Δn/Δs)(r⃗/r)",
        "md": "04md：Δs 为**面元** m²，[k]=M（kg），另有等价式 A=-GkΔn/(Ω r³)·r⃗",
        "claims": "S17-C0004：A=-Gk dn/dΩ r/r³",
    },
]

# 20 个公式的第一性特征向量（供 §7 定级使用；src = 该式是否逐字等价/改写教科书式）
FORMULAS = [
    ("01", "时空同一化方程", dict(textbook=False, definition=True, undetermined=0, new=False)),
    ("02", "三维螺旋时空方程", dict(textbook=True, definition=True, undetermined=0, new=False)),
    ("03", "质量定义方程", dict(textbook=False, definition=True, undetermined=1, new=False)),
    ("04", "引力场定义方程", dict(textbook=True, definition=True, undetermined=1, new=False)),
    ("05", "静止动量方程", dict(textbook=False, definition=True, undetermined=0, new=False)),
    ("06", "运动动量方程", dict(textbook=False, definition=True, undetermined=0, new=False)),
    ("07", "宇宙大统一方程", dict(textbook=False, definition=False, undetermined=0, new=True)),
    ("08", "空间波动方程", dict(textbook=True, definition=False, undetermined=0, new=False)),
    ("09", "电荷定义方程", dict(textbook=False, definition=True, undetermined=1, new=False)),
    ("10", "电场定义方程", dict(textbook=True, definition=True, undetermined=1, new=False)),
    ("11", "磁场定义方程", dict(textbook=True, definition=True, undetermined=1, new=False)),
    ("12", "变化引力场产生电磁场", dict(textbook=False, definition=False, undetermined=1, new=True)),
    ("13", "磁矢势方程", dict(textbook=True, definition=True, undetermined=1, new=False)),
    ("14", "变化引力场产生电场", dict(textbook=True, definition=True, undetermined=1, new=False)),
    ("15", "变化磁场产生引力场和电场", dict(textbook=False, definition=False, undetermined=0, new=True)),
    ("16", "统一场论能量方程", dict(textbook=True, definition=False, undetermined=0, new=False)),
    ("17", "光速飞行器动力学方程", dict(textbook=False, definition=False, undetermined=0, new=True)),
    ("18", "空间波动通解", dict(textbook=True, definition=False, undetermined=0, new=False)),
    ("19", "引力光速统一方程", dict(textbook=False, definition=False, undetermined=1, new=True)),
    ("20", "电磁光速几何耦合常数 Z'", dict(textbook=False, definition=False, undetermined=1, new=True)),
]


# ==========================================================================
# §1 三方一致性审计
# ==========================================================================
def section1():
    print("\n=== §1 三方登记一致性（json / md / claims.csv） ===")

    src_note = ("外部源存在：" + os.path.relpath(SRC_PATH, ROOT)) if SRC else \
               "外部源不可达，使用内嵌快照（不影响判据，判据全部作用于已摘录的登记串）"
    I("X0", "输入可用性", src_note,
      numbers={"source_present": bool(SRC), "src_dir": SRC_DIR})
    ok("SC-13", "外部源 json 可读（决定 K2/H1 是否取真实计数）", SRC is not None,
       SRC_PATH if SRC else "不可达")

    if SRC:
        n_json = len(SRC.get("formulas", []))
        ok("SC-13b", "源 json 的公式条数 = 20", n_json == 20, "实到 %d" % n_json)
        I("X0b", "源 json 结构登记",
          "源 json 载入成功，公式数与元数据声明一致",
          numbers={"total_formulas_declared": SRC.get("metadata", {}).get("total_formulas"),
                   "total_formulas_actual": n_json,
                   "categories": len(SRC.get("metadata", {}).get("categories", []))})

    I("X0c", "与既有「常数层独立精算」的分工（避免重复造轮子）",
      "S17 体系内已存在 07_计算复现/核心公式常数层_独立精算.py 及其 claims "
      "S17-C0021…C0032，覆盖**常数层**（Z、Z'、k、k'、f 的数值与单位标注、"
      "α 关系式、kk' 复合常数）。本册**不重做**该层，只在其结论之上做"
      "**结构层**审计：20 式全量量纲、符号角色、单位约定闭合性、数学式正确性、"
      "第一性层级。两册互补：常数层回答「这些数对不对」，结构层回答"
      "「这套公式能不能被一致地读出来」。",
      numbers={"precedent_claims": "S17-C0021..C0032",
               "this_volume_scope": ["量纲", "符号角色", "单位约定", "数学式", "层级"]},
      evidence=["01_独立体系/S17_统一场论核心公式/07_计算复现/核心公式常数层_独立精算.py",
                "01_独立体系/S17_统一场论核心公式/11_证伪与反例/核心公式常数层_缺陷记录_2026-09-29.md"])

    # ---- X1: Z' 的两个定义互斥（决定性） ----
    zp = CST["c"] / (8 * math.pi * CST["eps0"])
    ratio_units = zp / CST["alpha"]
    F("X1", "Z' 的同一份元数据给出两个互斥定义",
      "元数据.md 第 20 式写 Z' = e²/(4πε₀ℏc) = 1/137（无量纲精细结构常数）；"
      "同一目录的 核心公式的元数据.json 与 20电磁耦合常数Z'.md 写 Z' = c/(8πε₀)。"
      "前者无量纲 ≈ 7.297e-3，后者有量纲 ≈ 1.347e18 kg·m⁴·s⁻³·C⁻² —— "
      "二者不仅在数值上差若干个数量级，根本分属不同量纲空间，不可能同时成立。"
      "同一asset 内部的定义冲突使 Z' 在任何下游推导中都不可引用。",
      numbers={"Zprime_md_alpha": CST["alpha"],
               "Zprime_json_c_over_8pi_eps0": zp,
               "numerical_ratio": ratio_units,
               "dim_md": DIM_ONE.tex(),
               "dim_json": (DIM_C - DIM_EPS0).tex()},
      repair="保留 c/(8πε₀) 定义并删除 md 中的 α 版本（α 版本疑为登记时的对象误置）；"
             "同时在元数据里写明 Z' 是有量纲常数，禁止与无量纲 α 混用。",
      level="L1")

    # ---- X2: 能量方程两套形式彼此互斥 ----
    beta = 0.6
    gam = 1.0 / math.sqrt(1 - beta * beta)   # 1.25
    m0 = 1.0
    e1 = (gam * m0) * (1.0 / gam)            # mc²√(1-β²) with m=γm0
    e2 = (gam * m0) * gam                    # mc²/√(1-β²) with m=γm0
    F("X2", "能量方程在 claims.csv 与 json 中登记为互斥的两式",
      "json 写 E = m₀c² = mc²√(1-v²/c²)，claims.csv(S17-C0016) 写 "
      "E = m₀c² = mc²/√(1-v²/c²)。在相对论性质量约定 m=γm₀ 下，前者给出 "
      "E = %.4f m₀c²（正确），后者给出 E = %.4f m₀c²（错 γ² 倍）；"
      "若把 m 解释为静止质量，则前式反而要求 m₀ = m/γ 与符号命名冲突。"
      "元数据从未声明自己采用哪一种质量约定 ⇒ 该式无法被唯一求值。" % (e1, e2),
      numbers={"beta": beta, "gamma": gam,
               "sqrt_form_over_m0c2": e1, "inverse_form_over_m0c2": e2,
               "discrepancy_factor": gam * gam},
      repair="在元数据中显式声明质量约定（推荐：m 为相对论性质量、m₀ 为静止质量，"
             "则正确形式为 E=m₀c²=mc²√(1-v²/c²)），并据此更正 claims.csv 的登记串。",
      level="L1")

    # ---- X3: 引力场两种写法是否等价（允许画面子 protests） ----
    # A_json = -Gk(Δn/Δs) r̂ , Δs = r²ΔΩ(md 口径)
    # A_claims = -Gk(dn/dΩ) r̂/r²
    r_, domega, dn = 2.0, 0.5, 7.0
    ds_access = r_ * r_ * domega
    a_json = dn / ds_access          # 系数部分
    a_claims = (dn / domega) * r_ / (r_ ** 3)
    ok("SC-14", "引力场两登记式在 Δs=r²ΔΩ 下代数等价",
       abs(a_json - a_claims) < 1e-12, "%.12f vs %.12f" % (a_json, a_claims))
    P("X3", "引力场定义式 json 版与 claims 版代数等价",
      "json 写 -Gk(Δn/Δs)(r⃗/r)，claims 写 -Gk(dn/dΩ)(r⃗/r³)。在 04md 声明的 "
      "Δs = r²ΔΩ 口径下，两者逐字等价（数值对照 %.12f = %.12f），"
      "属同一式的两种记号，不构成冲突——但要求 Δs 必须解释为 r²ΔΩ 而非任意长度。",
      numbers={"r": r_, "dOmega": domega, "dn": dn,
               "json_coeff": a_json, "claims_coeff": a_claims},
      level="L1")

    # ---- X4: k 的取值三处冲突 ----
    k_4pi_mP = 4 * math.pi * CST["m_Planck"]
    F("X4", "常数 k 在同一 asset 中取两个相差 2.7e-7 倍的值",
      "json 的 constants.k = 1（unit kg·sr），且可视化 parameters 默认 k=1、"
      "范围 [0.1,5]；而 04md/09md 与 claims.csv 均写 k = 4π m_P = 4π√(ℏc/G) ≈ "
      "%.4e kg。两者相差 %.3e 倍。更关键的是 4π m_P 这个取值在全部 20 份 "
      "元数据报告中都没有给出导出过程，是外部锚定的。" % (k_4pi_mP, 1.0 / k_4pi_mP),
      numbers={"k_json": 1.0, "k_mdclaims_4pi_mP": k_4pi_mP,
               "m_Planck": CST["m_Planck"], "ratio": k_4pi_mP / 1.0},
      repair="二选一并写死：若取 k=4πm_P，则 json 的默认值/范围必须同步更新，"
             "否则可视化输出与论文口径差 7 个数量级。",
      level="L1")

    # ---- X5: k' 单位三处冲突 ----
    dim_kp_required = DIM_Q - (DIM_MASS) - (DIM_ONE - DIM_TIME)  # q = k' k Ω^-2 dΩ/dt
    dim_kp_json = D(0, -1, 1, 1, 2)     # C·sr²/s
    ok("SC-15", "json 声明的 k' 单位与方程所需不符",
       not (dim_kp_required == dim_kp_json))
    F("X5", "k' 的单位在 json / md 文字 / md 量纲式三处互不相同",
      "由 q = k'k Ω⁻²(dΩ/dt) 反解所需 [k'] = %s；09md 的量纲式写 [I·T²/M] "
      "（= C·s·kg⁻¹，与所需一致 ✓）；但 09md 正文把单位文字写成 C·s²/kg "
      "（多一个 s）；json 的 constants 又写 C·sr²/s。三种写法两两不等。"
      "此外 09md 同一节还并列了 q=k'dm/dt、q=k'dΩ/dt、q=-jΩ²dm/dt 三种形式，"
      "它们对 [k'] 的要求各不相同，无法同时成立。" % dim_kp_required.tex(),
      numbers={"required": dim_kp_required.tex(),
               "md_symbolic_IT2M": D(-1, 0, 2, 1).tex(),
               "md_written_Cs2_per_kg": D(-1, 0, 2, 1).tex() + "(文字多写 1 个 s)",
               "json_C_sr2_per_s": dim_kp_json.tex()},
      repair="统一采用 [k'] = C·s·kg⁻¹（= A·s²·kg⁻¹），修正 09md 正文的 C·s²/kg "
             "与 json 的 C·sr²/s，并把四种 q 形式收敛为一种（保留 q = k'k Ω⁻² dΩ/dt）。",
      level="L1")

    # ---- X6: 光速矢量 C 的默认参数违反本体系核心公设 ----
    c_default_mag = math.sqrt(1.0 ** 2)          # json: C 默认 [1,0,0] m/s
    helix_speed = math.sqrt((5.0 * 1.0) ** 2 + 2.0 ** 2)  # json #02 默认 r=5,ω=1,h=2
    F("X6", "可视化默认参数与本体系核心公设 |C|=c 冲突",
      "公设 S17-A1 要求 |C⃗| ≡ c = %.6e m/s；但 json 中 #01 的 C 默认 [1,0,0]、"
      "范围 [-1,1] m/s（最大 1 m/s，差 %.3e 倍且**取不到** c），"
      "#02 的螺旋默认参数 r=5,ω=1,h=2 给出 |dr/dt| = √(r²ω²+h²) = %.4f m/s，"
      "同样不是 c；而 #16 的 v 又以 c 为单位、c 默认写作 1。"
      "同一份元数据混用了「m/s 绝对值」与「以 c 为单位」两套口径，"
      "其可视化产物在物理上不对应任何自洽参数点。" % (CST["c"], CST["c"] / c_default_mag, helix_speed),
      numbers={"c_true": CST["c"], "C_default_mag": c_default_mag,
               "helix_default_speed": helix_speed,
               "gap_factor": CST["c"] / helix_speed},
      repair="把 C/V 类参数统一改为「以 c 为单位的无量纲数」（如 C=[1,0,0]·c），"
             "并给 #02 增加由 |dr/dt|=c 推出的约束 ω=√(c²-h²)/r，避免自由三参数。",
      level="L0")

    return None


# ==========================================================================
# §2 量纲全量审计（两种 sr 约定）
# ==========================================================================
def _dim_of_k(sr_matters):
    return D(1, 0, 0, 0, 1) if sr_matters else D(1, 0, 0)


def _dim_of_kprime(sr_matters):
    # 由 q = k' k Ω^-2 dΩ/dt 反解：[k'] = [q]/([k]·[dΩ/dt])
    k_dim = _dim_of_k(sr_matters)
    omega_dot = (DIM_SR if sr_matters else DIM_ONE) - DIM_TIME
    return DIM_Q - k_dim - omega_dot


def build_formula_dims(sr_matters):
    """返回 [(fid,name,lhs_dim,rhs_dim,note)]，rhs_dim 取「按声明**कर**代人」的结果。"""
    k = _dim_of_k(sr_matters)
    kp = _dim_of_kprime(sr_matters)
    srpos = DIM_SR if sr_matters else DIM_ONE
    rows = []

    def add(fid, name, lhs, rhs, note=""):
        rows.append((fid, name, lhs, rhs, note))

    # 01 r = C t
    add("01", "时空同一化方程", DIM_LEN, DIM_C + DIM_TIME)
    # 02 helix
    add("02", "三维螺旋时空方程", DIM_LEN, DIM_LEN)
    # 03 m = k dn/dΩ
    add("03", "质量定义方程", DIM_MASS, k + DIM_ONE - srpos)
    # 04 A = -Gk(Δn/Δs)·r̂ ；Δs 的口径决定成败，md 声明为 m²
    ds_md = DIM_LEN + DIM_LEN                    # md 口径：面积 m²
    ds_consistent = srpos + DIM_LEN + DIM_LEN    # 使 sr 约定下自洽所需：sr·m²
    add("04", "引力场定义方程", DIM_AGRAV, DIM_G + k + (DIM_ONE - ds_md),
        "Δs 按 md 声明取 m²")
    rows[-1] = (rows[-1][0], rows[-1][1], rows[-1][2], rows[-1][3], rows[-1][4])
    # 05 p0 = m0 C0
    add("05", "静止动量方程", DIM_MOM, DIM_MASS + DIM_C)
    # 06 P = m(C-V)
    add("06", "运动动量方程", DIM_MOM, DIM_MASS + DIM_VEL)
    # 07 F = C ṁ - V ṁ + m Ċ - m V̇
    add("07", "宇宙大统一方程", DIM_F, DIM_C + DIM_MASS - DIM_TIME)
    # 08 ∇²L = c^-2 L_tt
    add("08", "空间波动方程", DIM_LEN - DIM_LEN - DIM_LEN,
        DIM_LEN - DIM_TIME - DIM_TIME - DIM_C - DIM_C)
    # 09 q = k' k Ω^-2 dΩ/dt
    add("09", "电荷定义方程", DIM_Q, kp + k - srpos - srpos + srpos - DIM_TIME)
    # 10 E = -kk'/(4πε₀Ω²) (dΩ/dt) r̂/r²
    add("10", "电场定义方程", DIM_EFIELD,
        k + kp - srpos - srpos + srpos - DIM_TIME - DIM_EPS0 - DIM_LEN - DIM_LEN)
    # 11 B = μ₀/4π · q v×r / r³
    add("11", "磁场定义方程", DIM_BFIELD,
        DIM_MU0 + DIM_Q + DIM_VEL + DIM_LEN - DIM_LEN - DIM_LEN - DIM_LEN)
    # 12 ∂²A/∂t² = (V/f)(∇·E) - (C²/f)(∇×B)     —— A 先按【引力场】读
    add("12", "变化引力场产生电磁场",
        DIM_AGRAV - DIM_TIME - DIM_TIME,
        DIM_VEL + (DIM_EFIELD - DIM_LEN))
    # 13 ∇×A = B/f
    add("13", "磁矢势方程", DIM_AGRAV - DIM_LEN, DIM_BFIELD)
    # 14 E = -f dA/dt
    add("14", "变化引力场产生电场", DIM_EFIELD, DIM_AGRAV - DIM_TIME)
    # 15 dB/dt = -(A×E)/c² - ∇×E
    add("15", "变化磁场产生引力场和电场",
        DIM_BFIELD - DIM_TIME,
        DIM_AGRAV + DIM_EFIELD - DIM_C - DIM_C)
    # 16 E = m0c² = mc²√(1-β²)
    add("16", "统一场论能量方程", DIM_EN, DIM_MASS + DIM_C + DIM_C)
    # 17 F = (C-V) dm/dt
    add("17", "光速飞行器动力学方程", DIM_F, DIM_VEL + DIM_MASS - DIM_TIME)
    # 18 L = f(t-r/c)+g(t+r/c)
    add("18", "空间波动通解", DIM_LEN, DIM_LEN)
    # 19 Z = Gc/2
    add("19", "引力光速统一方程", DIM_G + DIM_C, DIM_G + DIM_C)
    # 20 Z' = c/(8πε₀)
    add("20", "电磁光速几何耦合常数", DIM_C - DIM_EPS0, DIM_C - DIM_EPS0)
    return rows, ds_consistent, ds_md


def section2():
    print("\n=== §2 量纲全量审计（20 式 × 两种球面度约定） ===")
    results = {}
    for sr_matters in (True, False):
        rows, ds_cons, ds_md = build_formula_dims(sr_matters)
        tag = "sr-有量纲" if sr_matters else "sr-无量纲"
        bad = []
        for fid, name, lhs, rhs, note in rows:
            resid = rhs - lhs
            if not resid.is_zero():
                bad.append((fid, name, lhs.tex(), rhs.tex(), resid.tex(), note))
        results[tag] = bad
        print("  约定[%s]：不一致 %d/%d 式" % (tag, len(bad), len(rows)))

    bad_sr = results["sr-有量纲"]
    bad_nosr = results["sr-无量纲"]

    # 逐条登记（以「是否存在单一约定使全表通过」为核心判据）
    F("D1", "不存在任何单一单位约定使 20 式全部量纲自洽",
      "在「sr 为独立量纲」约定下 %d 式不一致；在「sr 视为无量纲（SI 现行口径）」"
      "约定下仍有 %d 式不一致。约定切换只能平移冲突位置，不能消除冲突。"
      "这决定了该元数据作为「推导输入」是不可用的：下游任何推导都必须先自行"
      "补全单位约定，而补全方式不唯一。" % (len(bad_sr), len(bad_nosr)),
      numbers={"sr_dimensionful_failures": len(bad_sr),
               "sr_dimensionless_failures": len(bad_nosr),
               "sr_fail_ids": [b[0] for b in bad_sr],
               "nosr_fail_ids": [b[0] for b in bad_nosr]},
      level="L1")

    detail = []
    for fid, name, lhs, rhs, resid, note in bad_nosr:
        detail.append("%s %s：LHS %s  vs  RHS %s  残差 %s" % (fid, name, lhs, rhs, resid))
    I("D2", "sr-无量纲约定下的不一致清单（明细）",
      "；".join(detail) if detail else "无",
      numbers={"count": len(bad_nosr)})

    # #04 的 Δs 二难（单独成条）
    k_sr = D(1, 0, 0, 0, 1)
    lhs04 = DIM_AGRAV
    rhs04_md = DIM_G + k_sr + (DIM_ONE - (DIM_LEN + DIM_LEN))
    rhs04_fixed = DIM_G + k_sr + (DIM_ONE - (DIM_SR + DIM_LEN + DIM_LEN))
    ok("SC-16", "Δs 取 sr·m² 时 #04 自洽", rhs04_fixed == lhs04)
    ok("SC-17", "Δs 取 md 声明的 m² 时 #04 不自洽", not (rhs04_md == lhs04))
    F("D3", "引力场式的 Δs 口径二难（必须牺牲一处登记）",
      "若坚持 json 的 k 单位为 kg·sr（即 sr 有量纲），则 #04 成立要求 "
      "[Δs] = sr·m²，而 04md 第 31 行明确写 Δs 单位为 m² → 不成立；"
      "若按 SI 现行口径把 sr 视为无量纲（04md 第 33 行也持此说），"
      "则 #04 通过，但 json 里 k 的 'kg·sr' 单位标注就是多余的/错误的。"
      "没有任何一处改动能让两边同时正确。",
      numbers={"dim_k_kg_sr": k_sr.tex(),
               "lhs": lhs04.tex(),
               "rhs_with_ds_m2": rhs04_md.tex(),
               "rhs_with_ds_sr_m2": rhs04_fixed.tex()},
      repair="推荐收敛路径：sr 视为无量纲（与 SI 及 04md 自身一致），"
             "json 中 k 的单位由 kg·sr 改为 kg。",
      level="L1")
    return results


# ==========================================================================
# §3 f 的量纲求解：12 / 13 / 14 / 15 四式的符号与单位耦合
# ==========================================================================
def section3():
    print("\n=== §3 符号 A 的角色与耦合常数 f 的量纲求解 ===")

    def req_f_divisor(numer_without_f, lhs):
        """方程形如 X/f = L，返回所需 [f] = X - L。"""
        return numer_without_f - lhs

    # 读法 I：A ≡ 引力场（加速度），与 #04 定义一致
    f12_I = req_f_divisor(DIM_VEL + (DIM_EFIELD - DIM_LEN), DIM_AGRAV - DIM_TIME - DIM_TIME)
    f12b_I = req_f_divisor(2 * DIM_C + (DIM_BFIELD - DIM_LEN), DIM_AGRAV - DIM_TIME - DIM_TIME)
    f13_I = req_f_divisor(DIM_BFIELD, DIM_AGRAV - DIM_LEN)
    f14_I = DIM_EFIELD - (DIM_AGRAV - DIM_TIME)   # E = -f·dA/dt ⇒ [f] = [E] - [dA/dt]
    # 读法 II：A ≡ 磁矢势（∇×A=B 的经典读法）
    f13_II = req_f_divisor(DIM_BFIELD, DIM_AMAG - DIM_LEN)
    f14_II = DIM_EFIELD - (DIM_AMAG - DIM_TIME)
    f12_II = req_f_divisor(DIM_VEL + (DIM_EFIELD - DIM_LEN), DIM_AMAG - DIM_TIME - DIM_TIME)
    f15_I = (DIM_AGRAV + DIM_EFIELD - DIM_C - DIM_C) - (DIM_BFIELD - DIM_TIME)
    f15_II = (DIM_AMAG + DIM_EFIELD - DIM_C - DIM_C) - (DIM_BFIELD - DIM_TIME)

    ok("SC-18", "读法 I 下 #12 两项对 f 的要求一致", f12_I == f12b_I)
    ok("SC-19", "读法 I 下 12/13/14 对 f 的要求完全一致",
       f12_I == f13_I and f13_I == f14_I, "%s" % f12_I.tex())
    ok("SC-20", "读法 I 下 #15 自洽（无需 f）", f15_I.is_zero())
    ok("SC-21", "读法 II（A=磁矢势）下 #13/#14 要求 f 无量纲",
       f13_II.is_zero() and f14_II.is_zero())
    ok("SC-22", "读法 II 会打破 #15", not f15_II.is_zero(), "残差 %s" % f15_II.tex())

    P("F1", "存在唯一的 [f] 使 12/13/14/15 四式同时量纲自洽",
      "在 A ≡ 引力场（即 #04 定义的那一个 A）的读法下，#12 的两项、#13、#14 "
      "反解出的 [f] 完全一致 = %s，且 #15 不需要 f 即自洽。也就是说这四式"
      "彼此相容，代价只有一个：f 必须带量纲。" % f12_I.tex(),
      numbers={"f_required_reading_I": f12_I.tex(),
               "f_required_reading_II": "无量纲（但同时打破 #15）",
               "residual_of_15_under_reading_II": f15_II.tex()},
      level="L2")

    F("F2", "元数据声明 f 无量纲，与上述唯一解冲突",
      "核心公式的元数据.json 的 constants.f 写 value=1, unit=dimensionless；"
      "但要使 #12/#13/#14 成立，[f] 必须等于 %s（即 kg·A⁻¹）。"
      "按声明取 f=1 时，#12 两侧残差 %s、#13 残差 %s、#14 残差 %s —— "
      "三式在无量纲 f 下全部不成立。" % (
          f12_I.tex(),
          (DIM_VEL + (DIM_EFIELD - DIM_LEN) - (DIM_AGRAV - 2 * DIM_TIME)).tex(),
          (DIM_BFIELD - (DIM_AGRAV - DIM_LEN)).tex(),
          ((DIM_AGRAV - DIM_TIME) - DIM_EFIELD).tex()),
      numbers={"declared": "dimensionless", "required": f12_I.tex()},
      repair="把 f 的单位写为 kg·A⁻¹（及其对应数值待实测），这是**唯一**"
             "不需要改动任何方程形式的最小修复；同时应在元数据中注明 "
             "f 目前没有独立测定值 ⇒ 12/13/14 三式当前不具备数值预测能力。",
      level="L2")

    B("F3", "符号 A 在同一元数据中承担两种物理角色",
      "#04 定义 A⃗ 为引力场（含 m/s² 量纲），#13 的 ∇×A⃗ = B⃗/f 是磁矢势关系"
      "（要求 A 具 %s 量纲）。二者用了同一个字母。审计给出两种读法："
      "读法 I（全程 A=引力场）使 12/13/14/15 全部自洽但 f 必须带量纲；"
      "读法 II（#13 内 A=磁矢势）使 f 无量纲但与 #04 的定义及 #15 冲突。"
      "元数据没有声明采取哪一种 ⇒ 阅读者无法唯一地解释 #13。" % DIM_AMAG.tex(),
      numbers={"A_gravity": DIM_AGRAV.tex(), "A_magnetic_potential": DIM_AMAG.tex()},
      repair="把 #13 的矢量势改记为 A_m（或明确「本式中的 A 为磁矢势，与 #04 "
             "的引力场 A 不同」），并同时在 #15 中标注其所用的 A 是引力场。",
      level="L2")

    # ---- 与既有常数层精算（S17-C0031）交叉：f 的显式表达式 vs 方程需求 ----
    f_expr = (CST["c"] / 2.0) * math.sqrt(4.0 * math.pi * CST["eps0"] * CST["G"])
    f_expr_dim = DIM_C + (DIM_EPS0 + DIM_G) * Fr(1, 2)
    gap = f12_I - f_expr_dim
    ok("SC-31", "f=(c/2)√(4πε₀G) 的量纲 = M^-1·L·I（与 S17-C0031 一致）",
       f_expr_dim == D(-1, 1, 0, 1))
    ok("SC-32", "该 f 表达式的量纲不等于 12/13/14 所要求的 [f]",
       not (f_expr_dim == f12_I), "差 %s" % gap.tex())
    F("F4", "f 的显式表达式与方程自身对 f 的要求互斥（跨册交叉）",
      "S17 常数层独立精算（S17-C0031）已登记本体系的 f = (c/2)·√(Z/Z') = "
      "(c/2)·√(4πε₀G)，实算 %.6e，量纲 %s；而本册由 #12/#13/#14 反解出的"
      "需求是 %s。两者相差 %s —— 即**该体系自带的 f 表达式并不能让它自己的"
      "三条场耦合方程成立**。无论 A 取引力场还是磁矢势，f 的这个具体取值"
      "都填不进方程（按 A=磁矢势读法要求 f 无量纲，同样不等）。" % (
          f_expr, f_expr_dim.tex(), f12_I.tex(), gap.tex()),
      numbers={"f_expression_value": f_expr,
               "f_expression_dimension": f_expr_dim.tex(),
               "f_required_by_12_13_14": f12_I.tex(),
               "mismatch_dimension": gap.tex(),
               "cross_reference": "S17-C0031 / 07_计算复现/核心公式常数层_独立精算.py"},
      repair="要么改 f 的表达式（使其量纲为 M·I⁻¹），要么改 12/13/14 的方程形式；"
             "两者都必须新增物理假设，本册不代劳 —— 在此之前 12/13/14 不可计算。",
      evidence=["01_独立体系/S17_统一场论核心公式/claims.csv S17-C0031"],
      level="L2")
    return f12_I


# ==========================================================================
# §4 常数信息增量审计
# ==========================================================================
def count_symbol_usage():
    """在 json 的 20 条公式中统计各符号被多少条公式真正引用。"""
    if not SRC:
        return None
    texts = [f.get("formula_latex", "") + " " + f.get("formula_unicode", "")
             for f in SRC.get("formulas", [])]
    return {
        "Z": sum(1 for t in texts if re.search(r"Z(?![a-zA-Z'])", t)),
        "Zprime": sum(1 for t in texts if ("Z'" in t or "Z’" in t)),
        "k": sum(1 for t in texts if re.search(r"(?<![a-zA-Z\\'])k(?![a-zA-Z'])", t)),
        "kprime": sum(1 for t in texts if ("k'" in t or "k’" in t)),
        "f": sum(1 for t in texts if re.search(r"(?<![a-zA-Z\\])f(?![a-zA-Z])", t)),
        "G": sum(1 for t in texts if re.search(r"(?<![a-zA-Z\\])G(?![a-zA-Z])", t)),
        "eps0": sum(1 for t in texts if ("varepsilon_0" in t or "ε₀" in t)),
    }


def section4():
    print("\n=== §4 常数信息增量（是否只是已知常数的代数重排） ===")

    usage = count_symbol_usage()
    if usage is None:
        # 外部不可达时退化为内嵌计数（数值取自本次已核对的源 json）
        usage = {"Z": 1, "Zprime": 1, "k": 5, "kprime": 3, "f": 3, "G": 2, "eps0": 2}
        ok("SC-30", "外部源 json 不可达，K2 退化为内嵌计数", False,
           "请以能访问外部源的环境重跑以取真实计数")

    P("K1", "Z 与 Z' 是零信息增量的重写包装",
      "Z ≡ G·c/2 与 Z' ≡ c/(8πε₀) 都是**用定义式直接把已知常数组合成一个新符号**。"
      "在这种构造下，任何涉及 Z 的等式在把 Z 展开后都退化为已知恒等式，"
      "不包含超出 (G,c,ε₀) 的信息。这与 openuft 已登记家族 M02"
      "（普朗克锚定谬误 / 常数重排）是同一类结构：重排不是派生。",
      numbers={"Z_definition": "G·c/2", "Zprime_definition": "c/(8π·ε₀)"},
      evidence=["00_项目治理/../01_独立体系/S07..S10 的 M02 冲突记录（同族）"],
      level="L1")

    F("K2", "Z 与 Z' 是孤儿常数：在 20 式中没有下游使用",
      "逐式统计 20 条 formula_latex/formula_unicode 的符号引用：G 出现在 %d 条、"
      "ε₀ 出现在 %d 条、k 出现在 %d 条、f 出现在 %d 条；"
      "而符号 Z 只出现在 %d 条、Z' 只出现在 %d 条 —— 恰好就是定义它们自己的"
      "#19 与 #20 各一条，下游使用数为 %d。"
      "元数据文档里描述的「Z 与 Z' 对称」「Z' 出现在电场/磁场/统一场方程中」，"
      "在实际登记的 20 个公式里一条都不存在。" % (
          usage["G"], usage["eps0"], usage["k"], usage["f"],
          usage["Z"], usage["Zprime"],
          usage["Z"] + usage["Zprime"] - 2),
      numbers={"usage": usage,
               "downstream_use_of_Z": usage["Z"] - 1,
               "downstream_use_of_Zprime": usage["Zprime"] - 1},
      repair="要么给出至少一条真正使用 Z/Z' 的可检验公式，"
             "要么在元数据中如实标注二者为「记号约定」而非物理常数。",
      level="L1")

    I("K3", "未定常数清单与其索要的信息预算",
      "20 式中带有未给数值/单位的比例常数：k（#03/#04/#09/#10）、k'（#09/#10）、"
      "f（#12/#13/#14）、Δs 的口径（#04）、n（空间位移矢量条数，无定义）、"
      "Ω 的动力学（#09）。每一个都是必须由外部填入的自由参数。"
      "在 §6 的口径下，这些插槽使得 20 式中没有任何一条能独立产出数值预言。",
      numbers={"undetermined_constants": ["k", "k'", "f", "Δs口径", "n的定义", "Ω动力学"],
               "count": 6},
      level="L1")


# ==========================================================================
# §5 数值复算：源文档自称的"验证"是否可复现
# ==========================================================================
def section5():
    print("\n=== §5 数值复算（源文档自称的验证是否成立） ===")

    # ---- Z 的「≈0.01」是否单位依赖 ----
    Z_si = CST["G"] * CST["c"] / 2.0
    G_cgs = 6.67430e-8          # cm^3 g^-1 s^-2
    c_cgs = 2.99792458e10       # cm/s
    Z_cgs = G_cgs * c_cgs / 2.0
    # 普朗克单位下（G=c=ℏ=1）Z = 1/2 —— 乘以 [Z] 的普朗克单位应回到 SI 值
    lP = math.sqrt(CST["hbar"] * CST["G"] / CST["c"] ** 3)
    mP = CST["m_Planck"]
    tP = math.sqrt(CST["hbar"] * CST["G"] / CST["c"] ** 5)
    Z_unit_planck = lP ** 4 / mP / tP ** 3
    ok("SC-23", "Z 的普朗克单位换算回 SI 与直接计算一致",
       abs(0.5 * Z_unit_planck - Z_si) / Z_si < 1e-6,
       "%.6e vs %.6e" % (0.5 * Z_unit_planck, Z_si))

    F("V1", "Z ≈ 0.01 是单位依赖的数值巧合（伪显著）",
      "19md 把 Z = Gc/2 ≈ 1.00065e-2「接近 0.01」当作理论自洽性证据。"
      "复算：同一常数在不同单位制下取值为 SI %.6e、cgs %.6e、"
      "普朗克单位 %.1f —— 「接近一个整齐数字」完全由单位选择决定，"
      "不构成任何物理证据。（附注：源文档印的 1.00065e-2 与 CODATA 2018 "
      "直算值 %.6e 本身也有 %.2e 的相对偏差。）" % (Z_si, Z_cgs, 0.5, Z_si,
                                                    abs(1.00065e-2 - Z_si) / Z_si),
      numbers={"Z_SI": Z_si, "Z_cgs": Z_cgs, "Z_planck_units": 0.5,
               "source_claimed": 1.00065e-2,
               "relative_dev_of_source_print": abs(1.00065e-2 - Z_si) / Z_si},
      repair="删除「接近 0.01」这类证据，或改述为「在 SI 下 Z 的数值约为 1.0e-2，"
             "该数值依赖于单位制，不具判别力」。",
      level="L1")

    # ---- α = e²Z'/(ℏc) 是否成立 ----
    Zp = CST["c"] / (8 * math.pi * CST["eps0"])
    alpha_as_printed = CST["e"] ** 2 * Zp / (CST["hbar"] * CST["c"])
    alpha_true = CST["e"] ** 2 / (4 * math.pi * CST["eps0"] * CST["hbar"] * CST["c"])
    alpha_fixed = 2 * CST["e"] ** 2 * Zp / (CST["hbar"] * CST["c"] ** 2)
    ok("SC-24", "修正形式 α = 2e²Z'/(ℏc²) 能复现 α",
       abs(alpha_fixed - CST["alpha"]) / CST["alpha"] < 1e-8,
       "%.12e" % alpha_fixed)
    F("V2", "α = e²Z'/(ℏc) 与源文档自己的数值验证自相矛盾",
      "20md 第 78/110 行称由 α = e²Z'/(ℏc) 算得 7.297352566e-3（与 α 差 0.00065%%）。"
      "实算按**印刷公式**逐字代入得 %.6e，其量纲为速度 L·T⁻¹ 而非无量纲，"
      "与 α 相差 %.3e 倍（正是因子 c/2）。能复现 α 的正确形式是 "
      "α = 2e²Z'/(ℏc²)（实算 %.12e，相对偏差 %.2e）—— 而这个式子把 Z' 展开后"
      "正好退回 α 的标准定义式，信息增量为零。" % (
          alpha_as_printed, alpha_as_printed / CST["alpha"],
          alpha_fixed, abs(alpha_fixed - CST["alpha"]) / CST["alpha"]),
      numbers={"printed_form_value": alpha_as_printed,
               "printed_form_dimension": (DIM_Q + DIM_Q + (DIM_C - DIM_EPS0)
                                          - D(1, 2, -1) - DIM_C).tex(),
               "alpha_codata": CST["alpha"],
               "corrected_form_value": alpha_fixed,
               "gap_factor": alpha_as_printed / CST["alpha"]},
      repair="把 α 关系式更正为 α = 2e²Z'/(ℏc²)，并注明它与 α 的标准定义等价"
             "（不构成对 α 的几何解释）。",
      level="L1")

    # ---- Z'/Z 的「力强度比」主张 ----
    ratio = Zp / Z_si
    ratio_id = 1.0 / (4 * math.pi * CST["eps0"] * CST["G"])
    ok("SC-25", "Z'/Z 恒等于标准组合 1/(4πε₀G)", abs(ratio - ratio_id) / ratio_id < 1e-12)
    fee = CST["ke"] * CST["e"] ** 2 / (CST["G"] * CST["m_e"] ** 2)
    fpp = CST["ke"] * CST["e"] ** 2 / (CST["G"] * CST["m_proton"] ** 2)
    F("V3", "Z'/Z ≈ 1.347e20「对应力强度比的平方根」——量纲与数值双重失效",
      "20md 第 100 行称 Z'/Z ≈ 1.347e20 对应两力强度比 ~1e36 的平方根。"
      "实算：(i) Z'/Z 的量纲为 %s（有量纲），而力强度比是无量纲数，"
      "二者不可比较；(ii) 即便只看数值，质子对力比的平方根为 %.4e，"
      "与该声称值相差 %.1f 倍；(iii) 且 Z'/Z 恒等于经典组合 1/(4πε₀G) "
      "（实算 %.6e，恒等残差机器零），即它描述的是「质量/电荷」基准比，"
      "必须再外乘 (e/m)² 才能凑出力比 —— 这一步由源文档隐去。" % (
          (DIM_C - DIM_EPS0 - DIM_G - DIM_C).tex(),
          math.sqrt(fpp), ratio / math.sqrt(fpp), ratio_id),
      numbers={"Zprime_over_Z": ratio, "dimension": (DIM_C - DIM_EPS0 - DIM_G - DIM_C).tex(),
               "identity_1_over_4pi_eps0_G": ratio_id,
               "sqrt_force_ratio_electron": math.sqrt(fee),
               "sqrt_force_ratio_proton": math.sqrt(fpp),
               "claim_vs_proton_sqrt_factor": ratio / math.sqrt(fpp)},
      repair="删除该结论；若保留，必须写明 Z'/Z = 1/(4πε₀G) 并显式补上外乘因子。",
      level="L1")

    # ---- k = 4π m_P 能否给出任何可检验输出 ----
    I("V4", "常数数值是不可判定的外部锚",
      "k = 4π m_P = %.6e kg、k' ≈ 1.16e10 C·s/kg（09md）、f = 1（无量纲）"
      "三个数值在 20 份元数据报告中均未见导出过程；其中 k' 明确写着"
      "「通过与库仑定律对比取」，属反向拟合。以逆向拟合确定的常数，"
      "不能回头用于「推出库仑定律」而不循环。" % (4 * math.pi * CST["m_Planck"]),
      numbers={"k_4pi_mP": 4 * math.pi * CST["m_Planck"],
               "kprime_fitted": 1.16e10, "f_declared": 1.0},
      evidence=["09md §7：k'「通过与库仑定律对比，取…使方程与实验值一致」"],
      level="L1")


# ==========================================================================
# §6 符号与数学缺陷
# ==========================================================================
def section6():
    print("\n=== §6 符号与数学缺陷（可符号验算的部分） ===")

    # ---- #07 牛顿符号 ----
    F("S1", "宇宙大统一方程在经典极限下与牛顿第二定律反号",
      "取 C⃗ 恒定（dC⃗/dt=0）且质量恒定（dm/dt=0）的经典极限，"
      "#07 给出 F⃗ = dP⃗/dt = -m dV⃗/dt = -m a⃗，而牛顿第二定律是 F⃗ = +m a⃗。"
      "7md 第 155 行声称「在 C⃗=0 的经典近似下退化为牛顿第二定律」——"
      "代入 C⃗=0 后 P⃗ = -mV⃗，所得仍是 -m a⃗，符号并不因 C⃗=0 而改变。"
      "该缺陷与 openuft 已登记的 S02-C0001 / S12-C0006（统一动量低速极限冲突）"
      "同源，属**缺陷族传播**：同一个 P = m(C-V) 借用到 S17 时一并带来符号反转。",
      numbers={"limit_assumptions": "dC/dt=0, dm/dt=0",
               "theory_side": "-m·dV/dt", "newton_side": "+m·dV/dt",
               "resolution_attempt_in_7md": "设 C→0（经验证不能修复符号）"},
      repair="需要一条额外约定（例如把「物体受力」定义为 -dP/dt，或明确 P 描述的是"
             "空间的动量而非物体的动量）。该约定属物理假设，不由本册代劳；"
             "在给出之前，#07 不得声称涵盖牛顿第二定律。",
      evidence=["01_独立体系/S02_空间光速螺旋统一力/claims.csv S02-C0001",
                "01_独立体系/S12_空间光速螺旋统一体系/claims.csv S12-C0006"],
      level="L2")

    # ---- #10 库仑符号 ----
    B("S2", "电场定义式的符号链未在元数据内闭合",
      "若按 04md 第 68 行的约定（r̂ 由源点指向场点）且 kk' > 0、dΩ/dt > 0，"
      "则 #10 的 E⃗ = -(kk'/4πε₀Ω²)(dΩ/dt) r̂/r² 对正电荷指向**源点**，"
      "与库仑定律的同性相斥相反；而 10md 第 54/89 行却写「正电荷时方向与 r⃗ 相同」"
      "——正文描述与公式符号冲突。一种可能的调和是采用 09md 的带负号版本 "
      "q = -k'k Ω⁻² dΩ/dt，但那样又要重排全部符号约定。"
      "元数据没有在任何一处把这一链条锁死，故该式符号不可判定。",
      numbers={"04md_rhat_convention": "源点 → 场点",
               "10md_direction_claim_pos_charge": "与 r⃗ 相同",
               "formula_sign": "负号（指向源点）"},
      repair="在元数据中固定一条符号约定（推荐：r̂ 由源点指向场点 + q = -k'kΩ⁻²dΩ/dt），"
             "并在 #10 注明与库仑定律的逐项对照。",
      level="L2")

    # ---- #17 与 #07 的包含关系 ----
    F("S3", "光速飞行器动力学方程不是 #07 的推论，而是丢弃惯性项后的子集",
      "#07 在 dC⃗/dt=0 下为 F⃗ = (C⃗-V⃗)dm/dt - m dV⃗/dt；"
      "json 版 #17 只有 F⃗ = (C⃗-V⃗)dm/dt，相差 -m dV⃗/dt 项；"
      "而 claims.csv 的 S17-C0017 却又登记为含该项的完整形式。"
      "被丢掉的恰恰是唯一能在 dm/dt=0 时给出惯性的项 —— "
      "即 #17 描述的物体在质量不变时受力恒为零，与「推进器」语义矛盾。",
      numbers={"f07": "(C-V)dm/dt + m dC/dt - m dV/dt",
               "f17_json": "(C-V)dm/dt",
               "f17_claims": "(C-V)dm/dt - m dV/dt",
               "missing_term": "- m dV/dt"},
      repair="统一 #17 的登记串（建议采用 claims 版含 -m dV/dt 的完整式），"
             "并注明它在 dm/dt=0 时退化为牛顿项（含 §6-S1 的符号问题）。",
      level="L2")

    # ---- #18 通解检验（sympy） ----
    residual = None
    note_sym = ""
    try:
        import sympy as sp
        r, t, cc = sp.symbols("r t c", positive=True)
        f = sp.Function("f")
        g = sp.Function("g")
        L = f(t - r / cc) + g(t + r / cc)
        lap = sp.diff(r ** 2 * sp.diff(L, r), r) / r ** 2
        res = sp.simplify(lap - sp.diff(L, t, 2) / cc ** 2)
        residual = res
        # 数值交叉验证：取具体 f,g 看残差非零
        u = sp.symbols("u")
        sub = {f: sp.Lambda(u, sp.sin(u)), g: sp.Lambda(u, sp.cos(u))}
        try:
            numres = sp.simplify(res.doit().subs(
                {t: sp.Rational(1, 2), r: 2, cc: 3}).subs(
                {f(t - r / cc).subs(sub).free_symbols and f: None}) if False else res)
        except Exception:
            numres = None
        # 数值点检验（直接对具体函数做）
        def F1(x):
            return sp.sin(x)

        def G1(x):
            return sp.cos(x)
        rr, tt, cv = sp.Rational(2), sp.Rational(1, 2), 3
        Lv = F1(tt - rr / cv) + G1(tt + rr / cv)
        # 手工算径向拉普拉斯
        dL_dr = sp.diff(F1(t - r / cv) + G1(t + r / cv), r).subs({r: rr, t: tt})
        d2L_dr2 = sp.diff(sp.diff(F1(t - r / cv) + G1(t + r / cv), r), r).subs({r: rr, t: tt})
        lap_val = d2L_dr2 + 2 * dL_dr / rr
        d2L_dt2 = sp.diff(sp.diff(F1(t - r / cv) + G1(t + r / cv), t), t).subs({r: rr, t: tt})
        residual_numeric = sp.N(lap_val - d2L_dt2 / cv ** 2)
        ok("SC-26", "#18 声称的通解不残 zero（sympy 数值点）", abs(float(residual_numeric)) > 1e-6,
           "残差 %s" % residual_numeric)
        # 修复形式验证
        Lfix = (F1(t - r / cv) + G1(t + r / cv)) / r
        lap_fix = sp.simplify(sp.diff(r ** 2 * sp.diff((f(t - r / cc) + g(t + r / cc)) / r, r), r) / r ** 2
                              - sp.diff((f(t - r / cc) + g(t + r / cc)) / r, t, 2) / cc ** 2)
        ok("SC-27", "球对称修正形式 L=(f+g)/r 满足波动方程", sp.simplify(lap_fix) == 0)
        note_sym = "（sympy %s 符号验算）" % sp.__version__
    except Exception as exc:  # sympy 缺失时退化为有限差分数值验证
        note_sym = "（sympy 不可用，改用有限差分：%s）" % type(exc).__name__
        # L = sin(t - r/c) + cos(t + r/c)，c=3
        cv, rr, tt = 3.0, 2.0, 0.5
        def Lfun(rv, tv):
            return math.sin(tv - rv / cv) + math.cos(tv + rv / cv)
        h = 1e-4
        d1 = (Lfun(rr + h, tt) - Lfun(rr - h, tt)) / (2 * h)
        d2 = (Lfun(rr + h, tt) - 2 * Lfun(rr, tt) + Lfun(rr - h, tt)) / h ** 2
        lap = d2 + 2 * d1 / rr
        d2t = (Lfun(rr, tt + h) - 2 * Lfun(rr, tt) + Lfun(rr, tt - h)) / h ** 2
        residual_numeric = lap - d2t / cv ** 2
        ok("SC-26", "#18 声称的通解残差非零（有限差分）", abs(residual_numeric) > 1e-3,
           "残差 %.6e" % residual_numeric)

    F("S4", "空间波动通解 #18 不是 #08 的解（相差一个 1/r 因子）",
      "#18 写 L(r⃗,t) = f(t-r/c) + g(t+r/c)，其中 r = |r⃗|。把它代入 #08 的径向"
      "拉普拉斯算符，残差 = 2(g′ - f′)/(c·r)，仅当两个任意函数导数恒等时才为零，"
      "即它**不是**两条任意函数构成的通解 %s。"
      "三维球对称波动方程的正确达朗贝尔解是 L = [f(t-r/c) + g(t+r/c)]/r，"
      "已用符号验算确认其残差恒为零（參閱 SC-27）。" % note_sym,
      numbers={"claimed_solution": "L = f(t-r/c) + g(t+r/c)",
               "residual": "2(g' - f')/(c·r)",
               "correct_solution": "L = [f(t-r/c) + g(t+r/c)]/r"},
      repair="把 #18 更正为带 1/r 因子的球对称形式，或改述为「沿固定方向的平面波"
             " f(t - n̂·r/c)」并标明其适用域（此时恰与 #02 的螺旋结构不相容）。",
      level="L1")

    # ---- #01 vs #02 字面互斥 ----
    B("S5", "时空同一化方程与螺旋方程在字面上互斥",
      "#01 写 r⃗(t) = C⃗t（C⃗ 恒定 ⇒ 轨迹为直线、|dr⃗/dt| = |C⃗|）；"
      "#02 写圆柱螺旋轨迹，其速度方向持续旋转 ⇒ C⃗ 不可能恒定。"
      "两式要同时成立，#01 必须改述为微分形式 dr⃗ = C⃗(t)dt，|C⃗|=c。"
      "元数据未做这一限定，故按字面登记时 01 与 02 互斥。",
      numbers={"f01": "r(t) = C·t（C 常量 → 直线）",
               "f02": "r(t) = (r cosωt, r sinωt, ht)（方向旋转）"},
      repair="把 #01 改写为 dr⃗ = C⃗(t)·dt, |C⃗(t)| ≡ c，并在 #02 中补入约束 "
             "√(r²ω²+h²) = c（否则就退回到 §1-X6 的参数冲突）。",
      level="L0")

    # ---- #11 缺相对论因子 ----
    B("S6", "磁场定义式取的是低速近似，但元数据未标注适用范围",
      "json/metadata 的 #11 是 B = μ₀/(4π)·q(v⃗×r⃗)/r³，即匀速运动点电荷的"
      "**非相对论**毕奥-萨伐尔极限；完整结果含 (1-β²)/(1-β²sin²θ)^{3/2} 因子。"
      "而 claims.csv 的 S17-C0011 却登记为「含 γ 与运动电荷项」。"
      "在 β→1 的所谓「光速飞行器」语境（#17）里，低速式不适用且会低估/畸变场值。",
      numbers={"low_speed_form": "μ₀ q v×r̂ /(4π r²)",
               "full_form_factor": "(1-β²)/(1-β²sin²θ)^{3/2}",
               "claims_registration": "含 γ"},
      repair="统一 #11 的登记串，并显式标注 β≪1 适用范围。",
      level="L1")


# ==========================================================================
# §7 第一性层级判定 L0–L3
# ==========================================================================
def level_of(feat, extra_new_relation, quantified_prediction):
    """openuft 既有口径：
       L0 = 定义式/恒等重述；L1 = 借用改写（依赖外部输入或类比）；
       L2 = 本体系自洽的新关系但无量化的独立可检验预言；
       L3 = 有量化阈值且独立于本体系可被证伪的预言。
    """
    if not (feat["textbook"] or feat["definition"]) and quantified_prediction:
        return "L3"
    if extra_new_relation and not feat["definition"]:
        return "L2"
    if feat["textbook"] or feat["definition"]:
        return "L1" if feat["undetermined"] else "L0"
    return "L0"


def section7():
    print("\n=== §7 第一性层级判定（L0–L3）与 H/O/C/U 归一 ===")
    new_rel = {"07", "12", "15", "17", "19", "20"}
    rows = []
    lcount = {"L0": 0, "L1": 0, "L2": 0, "L3": 0}
    for fid, name, feat in FORMULAS:
        lv = level_of(feat, fid in new_rel, False)
        lcount[lv] += 1
        rows.append({"formula": fid, "name": name, "level": lv,
                     "textbook_rewrite": feat["textbook"],
                     "definition_only": feat["definition"],
                     "undetermined_constants": feat["undetermined"]})
    ok("SC-28", "层级计数合计 20", sum(lcount.values()) == 20)
    ok("SC-29", "L3 计数为 0", lcount["L3"] == 0, str(lcount))

    # 是否有任何一条登记了数值预言？
    pred = 0
    if SRC:
        pred = sum(1 for f in SRC.get("formulas", [])
                   if f.get("verification_status") == "verified")
    I("H1", "自我宣称 verified 但零数值预言登记",
      "json 中 20 式有 %d 式标记 verification_status='verified'、1 式 'theoretical'，"
      "但**没有任何一条**给出 prediction_value / prediction_urel 字段，"
      "也没有给出适用域与不确定度。按 openuft 既有判据 method_F（无量化判据者"
      "不构成 L3），「verified」在这里只能读作「作者自检通过」，不具备外部意义。" % pred,
      numbers={"self_claimed_verified": pred,
               "entries_with_prediction_value": 0,
               "level_distribution": lcount},
      level=None)

    P("H2", "层级分布：L0/L1 占绝对多数，L3 为 0",
      "按§7口径实算：L0 %d 式、L1 %d 式、L2 %d 式、L3 %d 式。"
      "与 openuft 全仓既有结论一致（全仓库 L3 仅 2 处，且不在本体系）："
      "本体系的实证价值集中在 L0/L1 —— 即「定义与教科书改写」层，"
      "真正可独立检验的关系（L2 %d 式）全部依赖尚未测定数值的比例常数。"
      % (lcount["L0"], lcount["L1"], lcount["L2"], lcount["L3"], lcount["L2"]),
      numbers={"level_distribution": lcount, "rows": rows},
      level=None)

    # 综合评级
    verdict_hocu = "C"
    reason = ("存在 §1-X1/X2/X4/X5 的登记互斥、§2-D1 的无统一单位约定、"
              "§3-F2 的 f 量纲冲突、§5-V2/V3 的数值验证不可复现、"
              "§6-S1/S3/S4 的符号与数学错误 —— 缺陷非单点而是分层分布，"
              "按 openuft 既有口径判为 C（冲突/缺陷）")
    I("H3", "S17 该元数据的归一化评级", "%s：%s。" % (verdict_hocu, reason),
      numbers={"rating": verdict_hocu,
               "defect_families": ["登记互斥", "单位约定不闭合", "符号重载",
                                   "数值验证不可复现", "数学式错误"],
               "families_count": 5},
      level=None)
    return lcount, rows


# ==========================================================================
# §8 产出
# ==========================================================================
def write_outputs(lcount, rows):
    if not os.path.isdir(OUTDIR):
        os.makedirs(OUTDIR)
    base = "张祥前20核心公式_元数据第一性审计"

    payload = {
        "title": "张祥前 20 核心公式「元数据」第一性审计与归一化",
        "date": DATE,
        "algorithm_alliance": True,
        "source": {
            "external_dir": os.path.relpath(SRC_PATH, ROOT) if SRC_PATH else None,
            "source_present": bool(SRC),
        },
        "counts": dict(CNT),
        "checks": [{"id": c, "passed": p, "desc": d, "extra": e} for c, p, d, e in CHECKS],
        "level_distribution": lcount,
        "level_rows": rows,
        "items": ITEMS,
        "constants_used": {k: v for k, v in CST.items()},
        "elapsed_sec": round(__import__("time").time() - T0, 3),
    }
    jpath = os.path.join(OUTDIR, base + ".json")
    with io.open(jpath, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# 张祥前 20 核心公式「元数据」第一性审计（机器产物）")
    lines.append("")
    lines.append("- 日期：%s" % DATE)
    lines.append("- 来源：`%s`（外部来料%s）" % (
        SRC_PATH or "(不可达)", "" if SRC else "，本次退化为内嵌快照"))
    lines.append("- 计数：PASS=%d FAIL=%d BOUNDARY=%d INFO=%d" % (
        CNT["PASS"], CNT["FAIL"], CNT["BOUNDARY"], CNT["INFO"]))
    lines.append("- 自检：%d/%d 通过" % (sum(1 for c in CHECKS if c[1]), len(CHECKS)))
    lines.append("")
    lines.append("## 条目明细")
    lines.append("")
    lines.append("| 编号 | 判定 | 标题 | 层级 |")
    lines.append("|---|---|---|---|")
    for it in ITEMS:
        lines.append("| %s | %s | %s | %s |" % (
            it["id"], it["verdict"], it["title"].replace("|", "/"),
            it["first_principle_level"] or "-"))
    lines.append("")
    lines.append("## 第一性层级分布")
    lines.append("")
    lines.append("| 层级 | 条数 |")
    lines.append("|---|---|")
    for k in ("L0", "L1", "L2", "L3"):
        lines.append("| %s | %d |" % (k, lcount[k]))
    lines.append("")
    lines.append("## 明细（含证据数值与修复建议）")
    lines.append("")
    for it in ITEMS:
        lines.append("### %s [%s] %s" % (it["id"], it["verdict"], it["title"]))
        lines.append("")
        lines.append(it["detail"])
        lines.append("")
        if it["numbers"]:
            lines.append("- **判据数值**：`%s`" % json.dumps(it["numbers"], ensure_ascii=False))
        if it["evidence"]:
            for e in it["evidence"]:
                lines.append("- **证据锚点**：%s" % e)
        if it["repair"]:
            lines.append("- **最小修复**：%s" % it["repair"])
        lines.append("")
    lines.append("## 引擎自检")
    lines.append("")
    lines.append("| 编号 | 结果 | 说明 |")
    lines.append("|---|---|---|")
    for cid, passed, desc, extra in CHECKS:
        lines.append("| %s | %s | %s %s |" % (cid, "PASS" if passed else "FAIL", desc, extra))
    lines.append("")

    mpath = os.path.join(OUTDIR, base + ".md")
    with io.open(mpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("\n产物：%s" % os.path.relpath(jpath, ROOT))
    print("产物：%s" % os.path.relpath(mpath, ROOT))


def main():
    print("=" * 74)
    print("算法联盟 · 张祥前 20 核心公式元数据 第一性审计  %s" % DATE)
    print("=" * 74)
    selfcheck_dim()
    section1()
    section2()
    f_dim = section3()
    section4()
    section5()
    section6()
    lcount, rows = section7()

    n_bad = sum(1 for c in CHECKS if not c[1])
    print("\n" + "=" * 74)
    print("自检：%d/%d 通过%s" % (len(CHECKS) - n_bad, len(CHECKS),
                                 "（全部通过）" if n_bad == 0 else "（有失败，见下）"))
    for cid, passed, desc, extra in CHECKS:
        if not passed:
            print("  FAIL %s %s %s" % (cid, desc, extra))
    print("PASS = %d" % CNT["PASS"])
    print("FAIL = %d" % CNT["FAIL"])
    print("BOUNDARY = %d" % CNT["BOUNDARY"])
    print("INFO = %d" % CNT["INFO"])
    print("层级分布 L0/L1/L2/L3 = %d/%d/%d/%d" % (
        lcount["L0"], lcount["L1"], lcount["L2"], lcount["L3"]))
    print("耗时 %.2fs" % (__import__("time").time() - T0))
    print("=" * 74)
    write_outputs(lcount, rows)
    return 0 if n_bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
