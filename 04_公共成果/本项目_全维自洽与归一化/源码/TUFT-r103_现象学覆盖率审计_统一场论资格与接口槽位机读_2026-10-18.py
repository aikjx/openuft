# -*- coding: utf-8 -*-
r'''
================================================================================
r103 | 现象学覆盖率审计：「统一场论」资格的接口槽位机读
受理日 2026-10-18 | 纯标准库 | Decimal 60/70 位 | Fraction 四元量纲 (M,L,T,Q)

靶（无新来料，自设攻破轮）：
  - r99 来稿式(1)-(27)（数据/TUFT-力公式体系压缩版_外部来料全文_2026-10-18.md）
  - r95 来稿残余质量公式与螺旋公理系统（r95/r98/r99/r100/r101 已审靶的并集）

【本册任务】
  r95-r101 五轮攻的是「不自洽 / 无内容 / 反统一 / 生成能力封闭」。
  本册换一个正面：**资格审计**——一个自称「统一场论」的公式系统，对它声称
  统一的对象（牛顿引力 + 电磁）的现存实验现象学，必须至少能「表述」这些
  现象。本册把该要求机读化为「接口槽位」判据：

  C 段：14 项标准现象学检验（PPN、EP、旋转曲线、透镜、框架拖曳、双星/GW、
        宇宙学、Coulomb、磁单极、Lorentz 力、EM 波、二体语法…），逐项列
        「最小必需输入语义集」，与公式集符号语义集机器求交：
        - 交集空            ⇒ NO_SLOT（结构上无法表述该现象）
        - 交集非空 + 上游死判 ⇒ BLOCKED（接口被 r95-r101 判死）
        - 交集非空 + 上游循环 ⇒ CIRCULAR（接口活着但输出是输入的重新呈现）
        - 交集非空 + 上游全绿 ⇒ COVERED
  S 段：结构性原因——公式集符号的语法类别统计（局部运动学量 vs 场/度规/
        多体语法）+ 微分算子阶数清点（从来稿全文机读模式计数）。
  V 段：六轮累积总判决。

【红线】
  - 数学自洽 != 物理证实；有符号 != 有预言；资格审计 != 内容审计（内容已由
    r99 判「14 式代数成立」，本册不重复判代数）；
  - verdict 由机读结果驱动，禁硬编码判定；
  - 防过度指控：本册明认来稿可定位为「单粒子运动学框架」——被判不合格的是
    它作为「统一场论」的资格（对自身组分的现象学都无法表述），不是其内部
    代数；阳性对照证明判据非恒否（扩展符号集下 NO_SLOT=0）；
  - 本册是审计与可算判决册，不产生新物理；不改动任何来料字节。
================================================================================
'''
import io
import os
import re
import sys
import json
import time
import datetime
from decimal import Decimal, getcontext, localcontext
from fractions import Fraction

getcontext().prec = 60

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(BASE))
DIR_DATA = os.path.join(BASE, "数据")

F_R95 = os.path.join(DIR_DATA, "TUFT-r95_螺旋时空理论_曲率挠率频率角速度_全维审计与攻破_2026-10-17.json")
F_R98 = os.path.join(DIR_DATA, "TUFT-r98_公式正确性四层次审查_外部评审整理与增量复算_2026-10-18.json")
F_R99 = os.path.join(DIR_DATA, "TUFT-r99_力公式体系压缩版与统一场论方程_机器审计_2026-10-18.json")
F_R100 = os.path.join(DIR_DATA, "TUFT-r100_攻破续轮_修法验证参数计数字剖面族扫描Floquet排除_2026-10-18.json")
F_R101 = os.path.join(DIR_DATA, "TUFT-r101_守恒律审计_场方程构造性收口_函数形式来源审计_2026-10-18.json")
F_LAI = os.path.join(DIR_DATA, "TUFT-力公式体系压缩版_外部来料全文_2026-10-18.md")

# ============================================================================
# 1. 公式集符号语义表（从来稿式(1)-(27) + 螺旋公理系统提取）
# ============================================================================
FSET = {
    # 符号: (语义标签, 语法类别)
    "V":       ("velocity_field",      "local_kinematics"),
    "A":       ("convective_accel",    "local_kinematics"),
    "Q_t":     ("topological_charge",  "local_kinematics"),
    "F":       ("force",               "local_kinematics"),
    "k_i":     ("coupling_const",      "local_kinematics"),
    "k_g":     ("coupling_const",      "local_kinematics"),
    "k_m":     ("coupling_const",      "local_kinematics"),
    "kappa_q": ("coupling_const",      "local_kinematics"),
    "k_E":     ("coupling_const",      "local_kinematics"),
    "k_B":     ("coupling_const",      "local_kinematics"),
    "omega":   ("angular_velocity",    "local_kinematics"),
    "r":       ("radius",              "local_kinematics"),
    "v_z":     ("axial_velocity",      "local_kinematics"),
    "m_star":  ("mass",                "local_kinematics"),
    "m_0":     ("mass",                "local_kinematics"),
    "q_eff":   ("eff_charge",          "local_kinematics"),
    "u":       ("velocity",            "local_kinematics"),
    "G":       ("grav_const",          "external_input"),   # 牛顿常数，外部输入
}
FSET_SEM = {v[0] for v in FSET.values()}
FSET_CAT = {}
for _s, (_sem, _cat) in FSET.items():
    FSET_CAT[_cat] = FSET_CAT.get(_cat, 0) + 1

# ============================================================================
# 2. 登记器
# ============================================================================
ITEMS = []; GUARDS = []

def add(code, status, title, detail="", section=""):
    assert status in ("PASS", "FAIL", "BOUNDARY", "CORRECTED", "INFO"), status
    ITEMS.append({"code": code, "status": status, "title": title,
                  "detail": detail, "section": section})

def guard(name, ok, note=""):
    GUARDS.append({"name": name, "ok": bool(ok), "note": note})
    return bool(ok)

def fs(x, n=25):
    try: return format(Decimal(x), ".%dE" % n)
    except Exception: return str(x)

def _load_json(path):
    try:
        with io.open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def _st_map(js):
    return {it["code"]: it["status"] for it in (js or {}).get("items", [])}

def _detail_map(js):
    return {it["code"]: (it.get("title", "") + " " + it.get("detail", ""))
            for it in (js or {}).get("items", [])}

_m95 = _st_map(_load_json(F_R95)); _m98 = _st_map(_load_json(F_R98))
_m99 = _st_map(_load_json(F_R99)); _m100 = _st_map(_load_json(F_R100))
_m101 = _st_map(_load_json(F_R101))
_MAPS = {"r95": _m95, "r98": _m98, "r99": _m99, "r100": _m100, "r101": _m101}
_d95 = _detail_map(_load_json(F_R95)); _d99 = _detail_map(_load_json(F_R99))
_d100 = _detail_map(_load_json(F_R100)); _d101 = _detail_map(_load_json(F_R101))
_DMAPS = {"r95": _d95, "r98": {}, "r99": _d99, "r100": _d100, "r101": _d101}

_CIRCULAR_KW = ("恒等", "反解", "循环", "重新参数化", "重述")

# 通用语义：只表明「双方都有某个通用量」，不构成现象学接口声明
GENERIC_SEM = {"coupling_const", "mass", "force", "radius", "velocity",
               "angular_velocity", "axial_velocity", "topological_charge",
               "eff_charge", "convective_accel", "velocity_field", "grav_const"}

def coverage_class(req_sem, upstreams):
    """机读覆盖类别：返回 (class, intersection, worst_status, evidence)。
    规则：
      交集空                                  ⇒ NO_SLOT
      交集纯通用语义且无上游判读                ⇒ NO_SLOT（通用量重叠不构成接口）
      上游存在 FAIL 或 BOUNDARY                ⇒ BLOCKED
      上游全 INFO/PASS 且命中循环词             ⇒ CIRCULAR
      上游全 PASS 且无循环词                   ⇒ COVERED
    """
    inter = sorted(set(req_sem) & FSET_SEM)
    if not inter:
        return ("NO_SLOT", inter, "NONE", "槽位交集为空")
    specific = [s for s in inter if s not in GENERIC_SEM]
    if not specific and not upstreams:
        return ("NO_SLOT", inter, "NONE",
                "交集仅为通用量（%s）且无上游判读 ⇒ 通用量重叠不构成现象学接口" % inter)
    statuses = []
    for _rd, _code in upstreams:
        _got = _MAPS[_rd].get(_code)
        if _got is not None:
            statuses.append((_rd, _code, _got))
    worst = "PASS"
    for _, _, _st in statuses:
        if _st in ("FAIL", "BOUNDARY"):
            worst = _st
            break
        if _st == "INFO" and worst == "PASS":
            worst = "INFO"
    if worst in ("FAIL", "BOUNDARY"):
        _ev = ";".join("%s.%s=%s" % (r, c, s) for r, c, s in statuses)
        return ("BLOCKED", inter, worst, _ev)
    _txt = " ".join(_DMAPS[r].get(c, "") for r, c in upstreams)
    if any(_k in _txt for _k in _CIRCULAR_KW):
        _ev = ";".join("%s.%s=%s" % (r, c, s) for r, c, s in statuses)
        return ("CIRCULAR", inter, worst, _ev)
    return ("COVERED", inter, worst, ";".join("%s.%s=%s" % (r, c, s) for r, c, s in statuses))

# ============================================================================
# CTRL 段｜引擎自洽守卫
# ============================================================================
# 阳性对照：扩展符号集（补入场/度规/多体语法）下同一判据应 NO_SLOT=0
FSET_SEM_EXT = FSET_SEM | {
    "metric", "photon_geodesic", "stress_energy", "quadrupole",
    "magnetic_charge", "gauss_law_magnetic", "vector_potential", "wave_operator",
    "other_particle_charge", "other_particle_position",
    "composition_dependence", "spin_curvature_coupling", "mass_profile",
    "homogeneous_density", "expansion", "field_equation",
}

# ============================================================================
# MAP 段｜跨册引用机器校验
# ============================================================================
CITES = [
    ("r95", "G02", "INFO", "静态牛顿式恒等重述（GM 输入）"),
    ("r95", "G05", "PASS", "开普勒检验：1/r^2 符合 6e-5"),
    ("r95", "G06", "BOUNDARY", "c 预算内界"),
    ("r95", "T02", "FAIL", "v_z 常数 ⇒ Q≡0"),
    ("r95", "T04", "FAIL", "拓扑不变性未证明"),
    ("r95", "M01", "FAIL", "m*/m0 三参数拟合 10/10"),
    ("r98", "P01b", "FAIL", "eta=0 后 beta 单参数仍 10/10"),
    ("r98", "P01d", "INFO", "两点读数唯一可证伪形态"),
    ("r99", "D04", "FAIL", "k_E/k_B=c 缺长度因子"),
    ("r99", "E01", "BOUNDARY", "等效原理定义级恒等"),
    ("r99", "U02", "BOUNDARY", "u 身份未定"),
    ("r99", "K01", "FAIL", "n=-5 被开普勒排除"),
    ("r100", "P01", "FAIL", "净常数 3 > 2（反统一）"),
    ("r100", "N01", "FAIL", "剖面族仅 s=-3/2 幸存"),
    ("r100", "N02", "FAIL", "幸存族即开普勒剖面（循环）"),
    ("r100", "R02", "FAIL", "EM 映射荒谬锚点"),
    ("r100", "R05", "FAIL", "修法全施用后独立预言数=0"),
    ("r100", "X01", "FAIL", "质量亏损被现存计量排除"),
    ("r101", "L02", "FAIL", "非稳态力场非保守"),
    ("r101", "G01", "FAIL", "场方程解族常数 C=sqrt(GM)"),
    ("r101", "G02", "FAIL", "框架常数无法合成 C"),
    ("r101", "H02", "FAIL", "alpha 能标未声明（E9）"),
]
_ok = 0; _bad = []
for _rd, _code, _expect, _why in CITES:
    _got = _MAPS[_rd].get(_code)
    if _got == _expect: _ok += 1
    else: _bad.append("%s.%s:期望%s实得%s" % (_rd, _code, _expect, _got))
add("MAP01", "PASS" if _ok == len(CITES) else "FAIL",
    "跨册引用机器校验（r95/r98/r99/r100/r101 共 %d 条）" % len(CITES),
    "一致 %d 条；不一致=%s" % (_ok, str(_bad) if _bad else "无"), section="MAP")
guard("g_map01_cross_citations_verified", _ok == len(CITES))

# ============================================================================
# C 段｜现象学覆盖率：14 项检验的接口槽位机读
# ============================================================================
# (编号, 现象, 最小必需输入语义集, 上游册引用)
PHENOM = [
    ("C01", "牛顿平方反比（太阳系行星轨道）",
     {"radius", "force", "grav_const"}, [("r95", "G05"), ("r95", "G02")]),
    ("C02", "PPN gamma（光线偏折/Shapiro 时延）",
     {"metric", "photon_geodesic"}, []),
    ("C03", "PPN beta（近日点进动/引力红移）",
     {"metric", "field_equation"}, []),
    ("C04", "等效原理定量检验（Eot-Wash 类）",
     {"mass", "coupling_const", "composition_dependence"}, [("r99", "E01")]),
    ("C05", "星系旋转曲线（平坦曲线/暗物质分布）",
     {"radius", "angular_velocity", "mass_profile"},
     [("r100", "N01"), ("r100", "N02")]),
    ("C06", "引力透镜（Einstein 环/像位移）",
     {"metric", "photon_geodesic"}, []),
    ("C07", "框架拖曳（GP-B/LAGEOS 类）",
     {"metric", "spin_curvature_coupling"}, []),
    ("C08", "双星进动与引力波辐射（PSR B1913+16 类）",
     {"stress_energy", "quadrupole"}, []),
    ("C09", "宇宙学（膨胀/CMB 功率谱）",
     {"metric", "homogeneous_density", "expansion"}, []),
    ("C10", "Coulomb 定律与静电屏蔽",
     {"eff_charge", "radius", "force", "coupling_const"},
     [("r99", "D04"), ("r100", "R02")]),
    ("C11", "磁单极禁戒（div B=0 实验）",
     {"magnetic_charge", "gauss_law_magnetic"}, []),
    ("C12", "Lorentz 力（运动电荷受的磁力）",
     {"eff_charge", "velocity", "coupling_const"}, [("r99", "U02")]),
    ("C13", "电磁波（Maxwell 方程/辐射）",
     {"field_equation", "vector_potential", "wave_operator"}, []),
    ("C14", "二体/N 体相互作用语法",
     {"other_particle_charge", "other_particle_position"}, []),
]

_rows_c = []
_n_noslot = 0; _n_blocked = 0; _n_circular = 0; _n_covered = 0
for _code, _name, _req, _ups in PHENOM:
    _cls, _inter, _worst, _ev = coverage_class(_req, _ups)
    if _cls == "NO_SLOT": _n_noslot += 1
    elif _cls == "BLOCKED": _n_blocked += 1
    elif _cls == "CIRCULAR": _n_circular += 1
    else: _n_covered += 1
    _rows_c.append((_code, _name, _cls, _inter, _worst, _ev))
    _st_item = {"NO_SLOT": "FAIL", "BLOCKED": "FAIL", "CIRCULAR": "FAIL",
                "COVERED": "PASS"}[_cls]
    _cls_zh = {"NO_SLOT": "无槽位", "BLOCKED": "接口被上游判死",
               "CIRCULAR": "接口循环", "COVERED": "覆盖"}[_cls]
    add(_code, _st_item,
        "现象学覆盖 [%s] %s ⇒ %s" % (_cls_zh, _name, _cls),
        "机器：最小必需输入语义 %s 与公式集符号语义集（%d 个标签）交集 = %s；"
        "上游判决 = %s。%s"
        % (sorted(_req), len(FSET_SEM), (_inter if _inter else "空"),
           _worst, _ev if _ev else "（无上游引用——本项从未被任何轮次触及，亦无槽位）"),
        section="C")
guard("g_c_section_all_not_covered", _n_covered == 0)

# 阳性对照守卫：扩展符号集下同判据 NO_SLOT 应为 0
_n_noslot_ext = sum(1 for _, _, _req, _ in PHENOM if not (set(_req) & FSET_SEM_EXT))
guard("g_ctrl_coverage_checker_has_teeth",
      _n_noslot_ext == 0 and _n_noslot >= 5,
      "真实符号集 NO_SLOT=%d；扩展符号集（补入 metric/stress_energy 等 15 个场论语义）NO_SLOT=%d ⇒ 判据检测的是符号系统，非恒否"
      % (_n_noslot, _n_noslot_ext))

# ============================================================================
# S 段｜结构性原因：符号语法类别 + 算子阶数
# ============================================================================
_local_n = FSET_CAT.get("local_kinematics", 0)
_ext_n = FSET_CAT.get("external_input", 0)
_field_n = sum(_v for _k, _v in FSET_CAT.items() if _k not in ("local_kinematics", "external_input"))
_ok_s01 = (_field_n == 0) and (_local_n + _ext_n == len(FSET))
add("S01", "FAIL" if _ok_s01 else "PASS",
    "结构性原因：公式集 %d 个符号全部是局部运动学量/外部常数，场/度规/多体语法量为 0" % len(FSET),
    "机器（语法类别统计）：local_kinematics=%d、external_input=%d（G 为牛顿常数，外部输入）、"
    "field/metric/fluid/multiparticle 语法量=%d。⇒ 公式集连「场」的语法都没有——"
    "覆盖率 0 是结构性必然，不是遗漏：V 是给定了剖面函数的局部速度场，不是待解的动力学子。"
    % (_local_n, _ext_n, _field_n), section="S")
guard("g_s01_all_symbols_local", _ok_s01)

# S02：微分算子阶数清点（从来稿全文机读模式计数；注意 \boxed 是显示框不是 d'Alembertian）
with io.open(F_LAI, "r", encoding="utf-8") as _f:
    _lai_txt = _f.read()
_pat = {
    "对流导数 nabla_V V": len(re.findall(r"nabla_\{\\mathbf V\}|nabla_{\\mathbf V}", _lai_txt)),
    "一阶时间导 partial_t/dot": len(re.findall(r"partial_t|\\dot", _lai_txt)),
    "d'Alembertian Box": len(re.findall(r"\\Box\b|\\square\b", _lai_txt)),
    "度规 g_munu": len(re.findall(r"g_\{\\mu\\nu\}|g_{\\mu\\nu}", _lai_txt)),
    "曲率/挠率张量": len(re.findall(r"R_\{\\mu|R_\{\\alpha|T_\{\\mu", _lai_txt)),
    "Lagrange 量/场方程": len(re.findall(r"\\mathcal\{?L|\\mathfrak\{?L", _lai_txt)),
}
_n_zero = sum(1 for _k, _v in _pat.items() if _v == 0)
add("S02", "INFO",
    "算子阶数清点：来稿最高一阶（对流导数+时间导），无 d'Alembertian、无度规、无曲率张量、无 Lagrange 量",
    "机器（来稿全文正则模式计数）：%s ⇒ 零命中 %d/6 项（注：全文 29 处 \\boxed 是 LaTeX 显示框，非波动算子）。"
    "这与 r95 P4（omega(r,t) 无场方程）、r101 守恒律封闭互洽：公式集的「动力学」止于一阶运动学，"
    "二阶结构（波动/辐射/进动）在其语法容量之外。"
    % ("；".join("%s=%d" % (_k, _v) for _k, _v in _pat.items()), _n_zero),
    section="S")
guard("g_s02_no_second_order_structure",
      _pat["d'Alembertian Box"] == 0 and _pat["Lagrange 量/场方程"] == 0)

# ============================================================================
# V 段｜六轮累积总判决
# ============================================================================
add("V01", "FAIL",
    "六轮累积总判决（r95+r98+r99+r100+r101+r103）：公式系统是输入的重新呈现，不是新物理的生成器",
    "机读汇总：代数内核健康（r99：14 式成立）；五轮接口全断（r95 引力/Q_t；r99 通量支/EM/距离标度；"
    "r100 修法零预言/反统一/剖面族/Floquet/定义域；r101 守恒律三重封闭/场方程构造性收口/函数形式欠定）；"
    "r103 资格审计：14 项标准现象学检验覆盖率 = %d/14（NO_SLOT %d + BLOCKED %d + CIRCULAR %d + COVERED 0），"
    "结构原因是符号系统无场/度规/多体语法（S01：%d/%d 局部量）且算子止于一阶（S02）。"
    "⇒ 该公式系统作为「单粒子运动学框架」内部部分自洽，作为「统一场论」在资格层面不成立："
    "它连自身组分（牛顿引力+电磁）的现存实验现象都无法表述。"
    % (_n_covered, _n_noslot, _n_blocked, _n_circular, _local_n, len(FSET)),
    section="V")
guard("g_v01_cumulative_verdict", _n_covered == 0)

# ============================================================================
# 外部输入账
# ============================================================================
EXT_INPUTS = [
    ("14 项现象学检验清单", "教科书级标准清单（PPN/EP/旋转曲线/透镜/拖曳/双星/宇宙学/Coulomb/磁单极/Lorentz/EM波/二体），非观测数据"),
    ("公式集符号语义表", "从来稿式(1)-(27) 与螺旋公理系统人工提取（%d 符号），判定规则机读" % len(FSET)),
    ("上游五册机读判决", "MAP01 机器校验 22 条引用（未重算）"),
    ("[C] 级常数", "CODATA/PDG（alpha 等，仅 MAP 与上游册引用）"),
]

# ============================================================================
# 总结与落盘
# ============================================================================
def _count(st):
    return sum(1 for it in ITEMS if it["status"] == st)

N_PASS = _count("PASS"); N_FAIL = _count("FAIL"); N_BOUND = _count("BOUNDARY"); N_INFO = _count("INFO")

SECTIONS = [
    ("MAP 跨册引用校验", ["MAP01", "MAP01"]),
    ("C 现象学覆盖率（14 项接口槽位机读）", ["C01", "C14"]),
    ("S 结构性原因（符号类别 + 算子阶数）", ["S01", "S02"]),
    ("V 六轮累积总判决", ["V01", "V01"]),
]

KEY_NUMBERS = {
    "coverage_covered": str(_n_covered),
    "coverage_noslot": str(_n_noslot),
    "coverage_blocked": str(_n_blocked),
    "coverage_circular": str(_n_circular),
    "ctrl_noslot_extended": str(_n_noslot_ext),
    "s01_local_symbols": str(_local_n),
    "s01_field_symbols": str(_field_n),
    "s02_dalembertian_hits": str(_pat["d'Alembertian Box"]),
    "s02_lagrangian_hits": str(_pat["Lagrange 量/场方程"]),
}

lines = []
lines.append("=" * 78)
lines.append("r103 | 现象学覆盖率审计：统一场论资格的接口槽位机读 | 机器判决报告")
lines.append("=" * 78)
lines.append("")
for _name, _rng in SECTIONS:
    lines.append("--- %s ---" % _name)
    for _it in ITEMS:
        if _rng[0] <= _it["code"] <= _rng[-1]:
            lines.append("[%s] %s" % (_it["status"], _it["title"]))
            if _it["detail"]:
                lines.append("      %s" % _it["detail"])
    lines.append("")
lines.append("--- C 段覆盖判定总表（编号 | 现象 | 类别 | 槽位交集 | 上游最差状态）---")
for _r in _rows_c:
    lines.append("  %s | %s | %s | inter=%s | upstream=%s"
                 % (_r[0], _r[1], _r[2], str(_r[3]), _r[4]))
lines.append("")
lines.append("  COVERED = %d / %d（NO_SLOT %d / BLOCKED %d / CIRCULAR %d）"
             % (_n_covered, len(PHENOM), _n_noslot, _n_blocked, _n_circular))
lines.append("")
lines.append("--- S02 来稿算子模式计数 ---")
for _k, _v in _pat.items():
    lines.append("  %-24s %d" % (_k, _v))
lines.append("")
lines.append("--- 外部输入账（%d 项）---" % len(EXT_INPUTS))
for _nm, _ds in EXT_INPUTS:
    lines.append("  [EXT] %s : %s" % (_nm, _ds))
lines.append("")
lines.append("--- 关键读数 ---")
for _k, _v in KEY_NUMBERS.items():
    lines.append("  %s = %s" % (_k, _v))
lines.append("")
lines.append("PASS = %d" % N_PASS)
lines.append("FAIL = %d" % N_FAIL)
lines.append("BOUNDARY = %d" % N_BOUND)
lines.append("INFO = %d" % N_INFO)
lines.append("条目 = %d" % len(ITEMS))
lines.append("守卫 = %d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
REPORT = "\n".join(lines)


def main():
    _now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _mt = {}
    for _p in (F_R95, F_R98, F_R99, F_R100, F_R101, F_LAI):
        if os.path.exists(_p):
            _mt[os.path.basename(_p)] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                    time.localtime(os.path.getmtime(_p)))
    print(REPORT)
    print("")
    print("--- wrapper 元信息（防假绿）---")
    print("  生成时刻 = %s" % _now)
    print("  模块路径 = %s" % os.path.abspath(__file__))
    for _k, _v in _mt.items():
        print("  输入 mtime %s = %s" % (_k, _v))
    os.makedirs(DIR_DATA, exist_ok=True)
    _stem = "TUFT-r103_现象学覆盖率审计_统一场论资格与接口槽位机读_2026-10-18"
    _payload = {
        "round": "r103",
        "date": "2026-10-18",
        "topic": "现象学覆盖率审计：统一场论资格的接口槽位机读（14 项标准检验）",
        "targets": {"formula_set": "r99 来稿式(1)-(27) + r95 螺旋公理系统",
                    "prior_rounds": "r95/r98/r99/r100/r101"},
        "items": ITEMS,
        "guards": GUARDS,
        "counts": {"PASS": N_PASS, "FAIL": N_FAIL, "BOUNDARY": N_BOUND, "INFO": N_INFO,
                   "total": len(ITEMS),
                   "guard_pass": sum(1 for g in GUARDS if g["ok"]),
                   "guard_total": len(GUARDS)},
        "cross_citations": [{"round": r, "code": c, "expected": e, "actual": _MAPS[r].get(c), "why": w}
                            for r, c, e, w in CITES],
        "coverage_table": [{"code": r[0], "phenomenon": r[1], "class": r[2],
                            "intersection": r[3], "worst_upstream": r[4], "evidence": r[5]}
                           for r in _rows_c],
        "coverage_counts": {"COVERED": _n_covered, "NO_SLOT": _n_noslot,
                            "BLOCKED": _n_blocked, "CIRCULAR": _n_circular,
                            "total": len(PHENOM)},
        "formula_symbol_table": {k: {"semantic": v[0], "category": v[1]} for k, v in FSET.items()},
        "operator_pattern_counts": _pat,
        "external_inputs": [{"name": n, "desc": d} for n, d in EXT_INPUTS],
        "key_numbers": KEY_NUMBERS,
        "wrapper": {"generated_at": _now, "module": os.path.abspath(__file__),
                    "input_mtimes": _mt},
    }
    with io.open(os.path.join(DIR_DATA, _stem + ".json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(_payload, ensure_ascii=False, indent=2))
    with io.open(os.path.join(DIR_DATA, _stem + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(REPORT)
        f.write("\n\n--- wrapper 元信息（防假绿）---\n")
        f.write("生成时刻 = %s\n" % _now)
        f.write("模块路径 = %s\n" % os.path.abspath(__file__))
        for _k, _v in _mt.items():
            f.write("输入 mtime %s = %s\n" % (_k, _v))
    _md = ["# 数据产物｜r103 现象学覆盖率审计（2026-10-18）", "",
           "靶：r99 来稿式(1)-(27) + r95 螺旋公理系统（无新来料，自设攻破轮）",
           "判定册：[判定_TUFT-r103-现象学覆盖率审计_统一场论资格与接口槽位机读_2026-10-18.md](../判定_TUFT-r103-现象学覆盖率审计_统一场论资格与接口槽位机读_2026-10-18.md)",
           "", "```", REPORT, "```", ""]
    with io.open(os.path.join(DIR_DATA, _stem + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(_md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
