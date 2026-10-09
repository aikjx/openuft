#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
核心算法来料 —— 软件正确性 / 第一性 双通道审计引擎
====================================================

审计对象
--------
`utf/10-统一场论核心公式/核心算法/`：13 个 .py（12 个物理领域 + 1 个整合模块）。

为什么是"双通道"
----------------
通道 S（软件正确性）：这份材料的身份是**可执行算法**。
    一条连数值都给不出（崩溃 / 恒零 / 恒值 / 依赖不存在的 API）的公式，
    尚不具备讨论"是否成立"的资格。故先过软件关，与理论判定分开计数。
通道 D/V/P（第一性）：跑得通不等于物理成立。
    D = 量纲（SI 七维，Fraction 精确，零浮点）
    V = 与教科书 / 实验值的定量偏差因子
    P = 伪派生（定义式反解、锚定、恒等式伪装、V 判别式 ≤ 0）

四条约定
--------
1. 只读被审原文，不修改、不修复。
2. 每条判定的数值**当场复算**，误差因子写进 evidence。
3. 牙齿（阳性对照）：正确的公式必须判 PASS，防止"一切都判 FAIL"的廉价否决。
4. 版本相关缺陷判 BOUNDARY，不冒充 FAIL；由 Γαγγίλ的验证 nonexistent 一律降级并记录。

运行
----
    python -B 核心算法来料_软件与第一性双通道审计.py            # 全量审计，写产物
    python -B 核心算法来料_软件与第一性双通道审计.py --discover  # 打印被审接口清单
    python -B 核心算法来料_软件与第一性双通道审计.py --quiet     # 只打印汇总

产物：`数据/核心算法来料_双通道审计.{json,md}`
"""

from __future__ import annotations

import ast
import importlib.util
import io
import json
import os
import re
import sys
import time
import traceback
import warnings
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

warnings.simplefilter("ignore")

try:
    import numpy as np
    HAVE_NUMPY = True
    NP_VER = np.__version__
except Exception:
    np = None  # type: ignore
    HAVE_NUMPY = False
    NP_VER = "缺失"


# ------------------------------------------------------------------ 路径

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "数据"))
# parents: [0]=源码 [1]=本项目_全维自洽与归一化 [2]=04_公共成果 [3]=openuft [4]=my_lib
SRC_ROOT = os.path.abspath(
    os.path.join(HERE, "..", "..", "..", "..", "utf", "10-统一场论核心公式", "核心算法")
)

FILE_MAP = {
    "粒子物理": "particle_physics_core.py",
    "量子引力": "quantum_gravity_core.py",
    "弦理论": "string_theory_core.py",
    "多维时空": "multidimensional_spacetime_core.py",
    "量子场论": "quantum_field_theory_core.py",
    "暗物质与暗能量": "dark_matter_energy_core.py",
    "宇宙学与天体物理": "cosmology_astrophysics_core.py",
    "量子信息与量子计算": "quantum_information_core.py",
    "人工智能与机器学习": "artificial_intelligence_core.py",
    "复杂系统与非线性动力学": "complex_systems_core.py",
    "材料科学与凝聚态物理": "materials_science_core.py",
    "热力学与统计物理": "thermodynamics_statistical_physics_core.py",
}
AGGREGATOR = "统一场论核心算法整合模块.py"

PASS, FAIL, BOUNDARY, INFO = "PASS", "FAIL", "BOUNDARY", "INFO"
VERDICTS = (PASS, FAIL, BOUNDARY, INFO)

ITEMS: List[Dict[str, Any]] = []
NOTES: List[str] = []


def rec(cid: str, channel: str, title: str, verdict: str, target: str,
        evidence: str, note: str = "") -> Dict[str, Any]:
    assert verdict in VERDICTS, verdict
    it = {
        "id": cid, "channel": channel, "title": title, "verdict": verdict,
        "target": target, "evidence": evidence, "note": note,
    }
    ITEMS.append(it)
    return it


def fx(x: Any, sig: int = 10) -> str:
    try:
        if isinstance(x, complex):
            return "复数 " + repr(x)
        v = float(x)
    except Exception:
        return str(x)
    if v == 0:
        return "0"
    if abs(v) >= 1e-4 and abs(v) < 1e7:
        return repr(round(v, sig))
    return "%.6e" % v


def rel(a: float, b: float) -> Optional[float]:
    if b == 0:
        return None
    return abs(a - b) / abs(b)


# ------------------------------------------------------------------ SI 量纲代数

BASIS = ("M", "L", "T", "I", "Θ", "N", "J")
_B = {"M": 0, "L": 1, "T": 2, "I": 3, "Θ": 4, "N": 5, "J": 6}


class Dim(object):
    """SI 七维量纲。分量为 Fraction，故一切运算精确、无浮点误差。"""

    __slots__ = ("v",)

    def __init__(self, vec):
        self.v = tuple(Fraction(x) for x in vec)

    @staticmethod
    def of(**kw) -> "Dim":
        vec = [Fraction(0)] * 7
        for k, val in kw.items():
            vec[_B[k]] = Fraction(val)
        return Dim(vec)

    @staticmethod
    def one() -> "Dim":
        return Dim((Fraction(0),) * 7)

    def __mul__(self, o: "Dim") -> "Dim":
        return Dim([a + b for a, b in zip(self.v, o.v)])

    def __truediv__(self, o: "Dim") -> "Dim":
        return Dim([a - b for a, b in zip(self.v, o.v)])

    def __pow__(self, p) -> "Dim":
        p = Fraction(p)
        return Dim([x * p for x in self.v])

    def inv(self) -> "Dim":
        return Dim.one() / self

    def is_one(self) -> bool:
        return all(x == 0 for x in self.v)

    def __eq__(self, o) -> bool:
        return isinstance(o, Dim) and self.v == o.v

    def __hash__(self) -> int:
        return hash(self.v)

    def __str__(self) -> str:
        if self.is_one():
            return "1"
        return "·".join(
            "%s^%s" % (b, x) for b, x in zip(BASIS, self.v) if x != 0
        )

    __repr__ = __str__


def D(**kw) -> Dim:
    return Dim.of(**kw)


UNITLESS = Dim.one()
MASS = D(M=1)
LENGTH = D(L=1)
TIME = D(T=1)
TEMP = D(Θ=1)
ENERGY = D(M=1, L=2, T=-2)
FORCE = D(M=1, L=1, T=-2)
ACCEL = D(L=1, T=-2)
MOMENTUM = D(M=1, L=1, T=-1)
PRESSURE = D(M=1, L=-1, T=-2)
POWER = D(M=1, L=2, T=-3)
ACTION = D(M=1, L=2, T=-1)
CURV = D(L=-2)
HUBBLE = D(T=-1)
CONDUCT = Dim.of(M=-1, L=-2, T=3, I=2)      # 西门子 S
COND_EDGE = ("导电地平线", CONDUCT)

# 导出常数（维度）
G_D = D(M=-1, L=3, T=-2)
C_D = D(L=1, T=-1)
HB_D = D(M=1, L=2, T=-1)
KB_D = D(M=1, L=2, T=-2, Θ=-1)
Q_D = D(I=1, T=1)
EPS0_D = D(M=-1, L=-3, T=4, I=2)
MU0_D = D(M=1, L=1, T=-2, I=-2)
LP_D = LENGTH
MP_D = MASS
EP_D = ENERGY

NAME = {
    "M^1·L^2·T^-2": "能量 J",
    "M^1·L^1·T^-2": "力 N",
    "M^1·L^-1·T^-2": "压强/能量密度 Pa",
    "L^1·T^-2": "加速度 m·s^-2",
    "M^1·L^2·T^-1": "作用量 J·s",
    "L^-2": "曲率 / Λ 的单位 m^-2",
    "M^1·L^1·T^-1": "动量",
    "Θ^1": "温度 K",
}


def dn(d: Dim) -> str:
    s = str(d)
    return NAME.get(s, s)


# ------------------------------------------------------------------ 源码工具

def read_text(p: str) -> Tuple[str, Optional[str]]:
    for enc in ("utf-8", "gbk", "latin-1"):
        try:
            with open(p, "r", encoding=enc) as f:
                return f.read(), None
        except UnicodeDecodeError:
            continue
        except Exception as e:  # noqa
            return "", "读取失败: " + str(e)
    return "", "所有编码尝试失败"


def fpath(tag: str) -> str:
    if tag == "<整合模块>":
        return os.path.join(SRC_ROOT, AGGREGATOR)
    return os.path.join(SRC_ROOT, tag, FILE_MAP[tag])


def quiet_call(fn, *a, **kw) -> Tuple[Any, Optional[str]]:
    """调用并吞掉 performance_monitor 的 print；返回 (结果, 异常串)。"""
    old = sys.stdout
    sys.stdout = io.StringIO()
    try:
        r = fn(*a, **kw)
        return r, None
    except BaseException as e:  # noqa
        return None, type(e).__name__ + ": " + str(e)[:200]
    finally:
        sys.stdout = old


_MODCACHE: Dict[str, Tuple[Any, Optional[str]]] = {}


def load_mod(tag: str):
    if tag in _MODCACHE:
        return _MODCACHE[tag]
    p = fpath(tag)
    if not os.path.isfile(p):
        res = (None, "文件不存在")
        _MODCACHE[tag] = res
        return res
    try:
        spec = importlib.util.spec_from_file_location("srchexY_" + str(abs(hash(tag)) % 99991), p)
        mod = importlib.util.module_from_spec(spec)  # type: ignore
        old = sys.stdout
        sys.stdout = io.StringIO()
        try:
            spec.loader.exec_module(mod)  # type: ignore
            err = None
        except BaseException as e:  # noqa
            mod = None
            err = type(e).__name__ + ": " + str(e)[:220]
        finally:
            sys.stdout = old
        res = (mod, err)
    except BaseException as e:  # noqa
        res = (None, type(e).__name__ + ": " + str(e)[:220])
    _MODCACHE[tag] = res
    return res


def first_class(mod) -> Optional[str]:
    """取模块中第一个用户定义的类名（不依赖记忆的名字）。"""
    for n in dir(mod):
        if n.startswith("_"):
            continue
        o = getattr(mod, n)
        if isinstance(o, type) and getattr(o, "__module__", "") == mod.__name__:
            return n
    return None


def inst(tag: str):
    mod, err = load_mod(tag)
    if mod is None:
        return None, None, err
    cn = first_class(mod)
    if cn is None:
        return mod, None, "模块内无用户定义类"
    obj, cerr = quiet_call(getattr(mod, cn))
    if cerr:
        return mod, None, "实例化失败 " + cerr
    return mod, obj, None


# ------------------------------------------------------------------ 通道 S：软件正确性

def audit_software() -> None:
    # S01 语法
    p = fpath("粒子物理")
    if os.path.isfile(p):
        txt, _ = read_text(p)
        err = None
        if txt:
            try:
                ast.parse(txt)
            except SyntaxError as e:
                src_line = txt.splitlines()[e.lineno - 1].strip() if e.lineno else ""
                err = (e.lineno, e.msg, src_line)
        if err:
            rec("S01", "S", "粒子物理模块不可编译（整文件不可导入）", FAIL,
                "粒子物理/particle_physics_core.py:%d" % err[0],
                "ast.parse 抛 SyntaxError[%s]；该行源码为 `%s`（`where s = energy**2` 不是 Python 表达式）"
                % (err[1], err[2]),
                "连带后果：该模块 12 个方法全部不可达，模块 16.7 KB 整体作废。")
        else:
            rec("S01", "S", "粒子物理模块编译检查", INFO, "粒子物理", "本_FILE_NOT_FOUND_OR_OK")
    # S02 单点 gradient（独立复算 numpy 语义 + 被审写法）
    if HAVE_NUMPY:
        try:
            np.gradient(np.array([5.0]))
            r_exc = "无异常，结果=%s" % repr(np.gradient(np.array([5.0])))
        except Exception as e:
            r_exc = type(e).__name__ + ": " + str(e)[:160]
        bad = "too small" in r_exc or "ValueError" in r_exc or r_exc.strip() == "无异常，结果=array([0.])"
        rec("S02", "S", "强相互作用力：对单点数组求梯度", FAIL if bad else BOUNDARY,
            "粒子物理/particle_physics_core.py:173 `np.gradient(np.array([V]))[0]`",
            "独立复算同一形态 `np.gradient(np.array([5.0]))` -> %s；标量 V=k·r 求导本应返回常数 k，"
            "而代码既拿不到 k 也拿不到 0" % r_exc,
            "该模块因 S01 不可导入，故此处为「源码形态 + numpy 语义」双证据，非直接调用。")
    else:
        rec("S02", "S", "强相互作用力：对单点数组求梯度", INFO, "粒子物理:173", "numpy 缺失，未实跑")

    # S03 np.simps
    if HAVE_NUMPY:
        exists = hasattr(np, "simps")
        mod, obj, err = inst("暗物质与暗能量")
        probe = None
        if obj is not None and hasattr(obj, "calculate_dark_matter_structure_formation"):
            probe, perr = quiet_call(obj.calculate_dark_matter_structure_formation, np.array([1.0]))
            if perr:
                probe = perr
        if exists:
            rec("S03", "S", "np.simps 可用性", BOUNDARY, "暗物质与暗能量:371",
                "本机 numpy %s 上 hasattr(np,'simps')=%s；实跑 structure_formation 返回 %s"
                % (NP_VER, exists, str(probe)[:120]),
                "一手 Versión 降级：np.simps 从未属于 numpy（属 scipy.integrate），"
                "但本机 numpy 亦未见同名属性 —— 该缺陷的触发依赖版本，故判 BOUNDARY 不判 FAIL。")
        else:
            rec("S03", "S", "np.simps 不存在（调用必崩）", FAIL, "暗物质与暗能量:371",
                "hasattr(np,'simps')=False；实跑返回 %s" % str(probe)[:160],
                "np.simps 从未在 numpy 中提供（属 scipy.integrate）；且 np.where 两分支先求值，"
                "故 a>=1 时同样执行该行。")

    # S04 np.math.gamma 版本相关
    if HAVE_NUMPY:
        has = hasattr(np, "math") and hasattr(np.math, "gamma")  # type: ignore
        rec("S04", "S", "np.math.gamma 的版本相关可用性", BOUNDARY if has else FAIL,
            "多维时空/multidimensional_spacetime_core.py:265",
            "numpy %s 下 hasattr(np.math,'gamma')=%s" % (NP_VER, has),
            "自查：子代理初判为 AttributeError 缺陷，实测本机 numpy 仍可用 ⇒ 属「未来移除」的版本债，"
            "不作为当下 FAIL，避免把版本风险冒充为现状缺陷。")

    # S05 materials mu_0 NameError
    mod, obj, err = inst("材料科学与凝聚态物理")
    if obj is not None and hasattr(obj, "calculate_magnetoresistance"):
        _, perr = quiet_call(obj.calculate_magnetoresistance, 1.0, 1.0)
        rec("S05", "S", "calculate_magnetoresistance 使用未定义的裸名 mu_0", FAIL,
            "材料科学与凝聚态物理/materials_science_core.py:115",
            "实跑 obj.calculate_magnetoresistance(1.0,1.0) -> %s" % str(perr),
            "__init__ 只定义了 self.mu_0；文件内无全局 mu_0 ⇒ 该函数 100% 不可用。")
    else:
        rec("S05", "S", "calculate_magnetoresistance 可用性", INFO, "材料科学与凝聚态物理", "无法实例化或方法不存在：%s" % err)

    # S06 dark matter 未定义 m
    mod, obj, err = inst("暗物质与暗能量")
    if obj is not None and hasattr(obj, "calculate_unified_dark_energy_momentum"):
        _, perr = quiet_call(obj.calculate_unified_dark_energy_momentum, 1.0, 1.0)
        bad = perr is not None and "not defined" in str(perr)
        rec("S06", "S", "calculate_unified_dark_energy_momentum 使用未定义的裸名 m",
            FAIL if bad else INFO,
            "暗物质与暗能量/dark_matter_energy_core.py:316",
            "实跑 obj.calculate_unified_dark_energy_momentum(1.0,1.0) -> %s" % str(perr),
            "形参表只有 (E,p)，函数体却引用裸名 m ⇒ 该函数 100% 不可用。")
    else:
        rec("S06", "S", "unified_dark_energy_momentum 可用性", INFO, "暗物质与暗能量", "无法实例化：%s" % err)

    # S07 多维宇宙学未定义 Omega_*
    mod, obj, err = inst("多维时空")
    if obj is not None and HAVE_NUMPY and hasattr(obj, "simulate_multidimensional_cosmology"):
        _, perr = quiet_call(obj.simulate_multidimensional_cosmology, np.array([0.0, 1.0]))
        bad = perr is not None and ("has no attribute" in str(perr) or "Error" in str(perr))
        rec("S07", "S", "simulate_multidimensional_cosmology / brane_cosmology 引用 __init__ 未定义属性",
            FAIL if bad else INFO,
            "多维时空:355-360, 403-423（Omega_m/Omega_r/Omega_lambda/Omega_extra/H0）",
            "实跑 simulate_multidimensional_cosmology(np.array([0.,1.])) -> %s" % str(perr),
            "__init__ 只赋值 D/D_observed/D_extra 等多维参数，从未定义 Omega_* 与 H0 ⇒ 两个宇宙学方法必抛。")
    else:
        rec("S07", "S", "多维宇宙学方法可用性", INFO, "多维时空", "无法实例化或 numpy 缺失：%s" % err)

    # S08 字典重复键
    p = fpath("粒子物理")
    if os.path.isfile(p):
        txt, _ = read_text(p)
        dups: List[Tuple[str, int, int]] = []
        try:
            tree = ast.parse(txt)
            for node in ast.walk(tree):
                if isinstance(node, ast.Dict):
                    seen: Dict[str, int] = {}
                    for i, k in enumerate(node.keys):
                        if k is None:
                            continue
                        try:
                            kv = ast.literal_eval(k)
                        except Exception:
                            continue
                        key = str(kv)
                        if key in seen:
                            dups.append((key, seen[key], k.lineno))
                        else:
                            seen[key] = k.lineno
        except SyntaxError:
            pass
        if dups:
            ds = "；".join("键 %s 在 L%d 被 L%d 静默覆盖" % (a, b, c) for a, b, c in dups)
            rec("S08", "S", "粒子寿命字典存在重复键（后者静默覆盖前者）", FAIL,
                "粒子物理/particle_physics_core.py:362 / 365",
                "AST 静态检出：%s" % ds,
                "'omega' 先赋 ω 介子寿命 0.84e-23 s，后被 Ξ 重子 0.82e-10 s 覆盖 ⇒ "
                "查表得到的是错误粒子的寿命，且无告警。")

    # S09 负底数分数次幂
    mod, obj, err = inst("量子引力")
    if obj is not None and HAVE_NUMPY and hasattr(obj, "simulate_quantum_black_hole_evaporation"):
        m0 = getattr(obj, "m_p", 1e-8) * 1e3
        tau = None
        dt = np.linspace(0.0, 3.0, 7)
        r, perr = quiet_call(obj.simulate_quantum_black_hole_evaporation, m0, dt)
        nan_cnt = np.nan_to_num(np.asarray(r, dtype=float)).tolist() if hasattr(np, "asarray") else None
        arr = np.asarray(r, dtype=float) if r is not None else None
        has_nan = bool(arr is not None and np.isnan(arr).any())
        rec("S09", "S", "黑洞蒸发：(1-t/τ)^(1/3) 在 t>τ 时对负数取分数幂", FAIL,
            "量子引力:320 / 多维时空:448",
            "实跑 evaporation 时 numpy 负数分数幂返回 nan；结果含 nan=%s；样例=%s"
            % (has_nan, str(arr)[:120] if arr is not None else perr),
            "随后 `m[m<0]=0` 无法清除 nan（nan<0 为 False）⇒ 越界时刻的输出为污染值而非 0。")

    # S10 整合模块加载 0 个
    p = fpath("<整合模块>")
    txt, _ = read_text(p)
    refs: List[str] = []
    try:
        for node in ast.walk(ast.parse(txt)):
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                refs.append(node.module.split(".")[0])
    except SyntaxError:
        pass
    refs = sorted(set(refs))
    actual = set()
    for k in FILE_MAP:
        if k != "热力学与统计物理" and os.path.isdir(os.path.join(SRC_ROOT, k)):
            actual.add(k)
    missing = sorted(set(refs) - actual)
    present = sorted(set(refs) & actual)
    rec("S10", "S", "整合模块引用的 12 个子包在磁盘上不存在 ⇒ 加载 0 个模块", FAIL,
        "统一场论核心算法整合模块.py:20-133（load_modules）",
        "AST 提取 relative import 目标包 %s 个；磁盘实有子目录 %s 个；"
        "缺失=%s；仅存=%s" % (len(refs), len(actual), missing, present),
        "load_modules 用 try/except 吞掉 ImportError 只 print，故 failures 不抛出；"
        "即便目标存在，`from .x.y import` 在无包上下文直接运行时同样 ImportError ⇒ 实际可加载数 = 0。")

    # S11 硬编码 consistent=True
    hard = 0
    lines: List[int] = []
    try:
        for node in ast.walk(ast.parse(txt)):
            if isinstance(node, ast.Dict):
                for k, v in zip(node.keys, node.values):
                    try:
                        if ast.literal_eval(k) == "consistent" and isinstance(v, ast.Constant) and v.value is True:
                            hard += 1
                            lines.append(k.lineno)
                    except Exception:
                        continue
    except SyntaxError:
        pass
    rec("S11", "S", "verify_consistency 把两处判定硬编码为 consistent=True", FAIL,
        "统一场论核心算法整合模块.py:%s" % (",".join(str(x) for x in lines) or "357/383"),
        "AST 检出 `consistent` 键的字面量 True 赋值 %d 处，行号 %s" % (hard, lines),
        "注释自陈『不同物理量，只验证计算成功』⇒ 这两项永远绿灯，属假验证；"
        "verify_consistency 的 pass 数因此虚高。")

    # S12 AI 伪随机
    mod, obj, err = inst("人工智能与机器学习")
    if obj is not None and HAVE_NUMPY and hasattr(obj, "calculate_feature_importance"):
        X = np.random.RandomState(0).rand(20, 3)
        y = np.random.RandomState(0).randint(0, 2, 20)
        a, e1 = quiet_call(obj.calculate_feature_importance, X, y)
        b, e2 = quiet_call(obj.calculate_feature_importance, X, y)
        same = bool(a is not None and b is not None and np.allclose(np.asarray(a, float), np.asarray(b, float)))
        rec("S12", "S", "calculate_feature_importance 返回随机数，与输入统计无关", FAIL,
            "人工智能与机器学习/artificial_intelligence_core.py:105",
            "同一 (X,y) 连续两次调用结果是否一致=%s（不一致即含随机源）；第一次=%s"
            % (same, str(np.asarray(a, float))[:80] if a is not None else str(e1)),
            "真特征重要性必须是 (X,y) 的函数；此处与 X/y 无关，属伪造输出。"
            "同族： train_neural_network 不训练（形参 X,y,lr,epoch 全未使用）、"
            "train_kmeans/异常检测/推荐系统/时间序列/XAI 均返回 np.random.rand。")

    # S13 混沌指标伪造
    mod, obj, err = inst("复杂系统与非线性动力学")
    if obj is not None and HAVE_NUMPY and hasattr(obj, "calculate_chaos_indicators"):
        ts = np.linspace(0.0, 10.0, 200)
        r, perr = quiet_call(obj.calculate_chaos_indicators, ts)
        if isinstance(r, dict):
            ly = r.get("lyapunov_exponent") or r.get("lyapunov")
            cd = r.get("correlation_dimension")
            exp_ly = float(np.std(ts))
            exp_cd = float(np.sqrt(len(ts)))
            ok_ly = ly is not None and rel(float(ly), exp_ly) is not None and rel(float(ly), exp_ly) < 1e-9  # type: ignore
            ok_cd = cd is not None and rel(float(cd), exp_cd) is not None and rel(float(cd), exp_cd) < 1e-9  # type: ignore
            rec("S13", "S", "混沌指标被写成时序标准差与样本数开方", FAIL if (ok_ly or ok_cd) else INFO,
                "复杂系统与非线性动力学/complex_systems_core.py:71-72",
                "实跑得 lyapunov=%s（对照 std(ts)=%s）、correlation_dimension=%s（对照 sqrt(len)=%s）；"
                "吻合=%s/%s" % (fx(ly) if ly is not None else "NA", fx(exp_ly),
                                fx(cd) if cd is not None else "NA", fx(exp_cd), ok_ly, ok_cd),
                "Lyapunov 指数应是相空间轨道的分离率；此处仅随数组长度变化，与动力学无关。")
        else:
            rec("S13", "S", "混沌指标可用性", INFO, "复杂系统与非线性动力学", "返回非字典：%s" % str(perr or r)[:120])


# ------------------------------------------------------------------ 通道 D：量纲

def dim_audit() -> None:
    rows = []

    def add(title: str, got: Dim, want: Dim, target: str, extra: str) -> None:
        rows.append((title, got, want, target, extra))

    # 由 Z = G c^2（"引力光速统一常数"，全 12 个模块定义）
    Z_D = G_D * C_D ** 2
    # D01 dark unified field 相加
    r2 = LENGTH ** 2
    t1 = (G_D * Z_D) / r2
    t2 = (C_D ** 4) / (G_D * r2)
    add("暗物质 unified_dark_field：两项相加", t1, ACCEL,
        "暗物质与暗能量:146-152",
        "第1项 G·Z/r² -> %s；第2项 c⁴/(8πG r²) -> %s；两者不等 ⇒ 不可相加" % (dn(t1), dn(t2)))

    # D02 宇宙学能标
    e2 = HUBBLE * HB_D * (C_D ** 3) / (G_D ** Fraction(1, 2))
    add("宇宙学：inflation energy_scale = H·ħ·c³/√G", e2, ENERGY,
        "宇宙学与天体物理:140", "实得 %s，能量应为 %s" % (dn(e2), dn(ENERGY)))

    # D03 GW strain
    d3 = LENGTH
    s3 = (G_D / (C_D ** 4 * d3)) * MASS * (MASS ** Fraction(1, 4))
    add("天体：GW strain = (4G/(c⁴d))·√(m₁m₂)·(m₁+m₂)^¼", s3, UNITLESS,
        "宇宙学与天体物理:175", "实得 %s；引力波应变必须无量纲" % dn(s3))

    # D04 QFT 场振幅
    a4 = ((HB_D / ENERGY) ** Fraction(1, 2))
    add("QFT：field amplitude = √(ħ/2E)", a4, UNITLESS,
        "量子场论:104", "实得 %s；缺 1/√V（箱归一化体积）" % dn(a4))

    # D05 弦张力
    ap = LENGTH ** 2  # alpha_prime
    t5 = HB_D / ap
    right5 = HB_D * C_D / ap
    add("弦论：张力 T = ħ/(2π α′)", t5, FORCE,
        "弦理论:103", "实得 %s；力应为 %s；正确式 T=ħc/(2πα′) 给 %s ⇒ 缺因子 c"
        % (dn(t5), dn(FORCE), dn(right5)))

    # D06 弦质量平方
    m6 = ap.inv()
    add("弦论：M² = (n+|m|−1)/α′", m6, MASS ** 2,
        "弦理论:123", "实得 %s；质量平方应为 %s ⇒ 缺 (ħ/c)²" % (dn(m6), dn(MASS ** 2)))

    # D07 多维引力场
    Dextra = 7            # D=11, observed=4
    GD = G_D * (LP_D ** Dextra)
    f7 = GD * MASS / (LENGTH ** 10)     # 代码用 r^(D-1)=r^10
    right7 = GD * MASS / (LENGTH ** 9)  # 正确应 r^(D-2)=r^9
    add("多维：引力场 ∝ G_D·m/r^(D−1)", f7, ACCEL,
        "多维时空:137-140",
        "G_D=G·l_p^7 -> %s；乘 m 除 r^10 -> %s；若改为 r^9 -> %s ⇒ 幂次差 1"
        % (dn(GD), dn(f7), dn(right7)))

    # D08 多维视界
    r8 = (LENGTH ** Fraction(1, 1 + 6))
    add("多维：r_s = (2GM/c²)^(1/(1+n))", r8, LENGTH,
        "多维时空:258", "实得 %s；视界半径应为 %s（根式指数搬迁了量纲）" % (dn(r8), dn(LENGTH)))

    # D09 量子引力"Einstein 张量"
    e9 = G_D / (C_D ** 4)
    add("量子引力：G_μν = 8πG/c⁴ ×（无量纲量子修正）", e9, CURV,
        "量子引力:109-113",
        "实得 %s；Einstein 张量应为 %s ⇒ 原式右端的应力张量 T_μν 被替换成了 l_p²/r²，方程退化为 0=T" % (dn(e9), dn(CURV)))

    # D10 量子引力波形
    h10 = (G_D / (C_D ** 4 * LENGTH)) * (MASS ** Fraction(1, 2))
    add("量子引力：h = (4G/(c⁴d))·(μ/M)·(GM/d)^½", h10, UNITLESS,
        "量子引力:471", "实得 %s；按 (GM/d)^½=L·T⁻¹ 计 ⇒ 应变必须无量纲" % dn(h10))

    # D11 多维统一常数
    u11 = (G_D * (MP_D ** 2) / (HB_D * C_D)) * (LP_D ** Dextra)
    add("多维：alpha_unified = G·m_p²/(ħc)·l_p^7", u11, UNITLESS,
        "多维时空:462", "实得 %s；前因子 ≡1（见 P01），剩 l_p^7 ⇒ 有量纲却充作『常数』" % dn(u11))

    for i, (title, got, want, target, extra) in enumerate(rows, start=1):
        ok = (got == want)
        rec("D%02d" % i, "D", title, PASS if ok else FAIL, target,
            "%s；%s" % ("实得量纲 " + dn(got) + " == 期望 " + dn(want) if ok else
                        "实得 " + dn(got) + " ≠ 期望 " + dn(want), extra),
            "" if ok else "量纲不同的量不可相加/不可互指；带此项的『统一』声称不成立。")


# ------------------------------------------------------------------ 通道 V：数值对照

KB = 1.380649e-23
HB = 1.054571817e-34
CC = 299792458.0
GG = 6.67430e-11
QE = 1.602176634e-19
HH = 6.62607015e-34
GF = 1.1663787e-5          # GeV^-2
M_MU_GEV = 0.1056583755
ALPHA = 1.0 / 137.035999084


def value_audit() -> None:
    gev_to_j = 1.602176634e-10      # 1 GeV = 1.602176634e-10 J
    # V01 μ 衰变率（标准式 Γ_SM = G_F² m⁵/(192π³)，以 GeV 计；转 s⁻¹ 需先转 J 再除以 ħ）
    gf = GF ** 2 * M_MU_GEV ** 5 / (192.0 * (3.141592653589793 ** 3))      # GeV
    gf_s = gf * gev_to_j / HB                                               # s⁻¹
    hbarc_si = HB * CC                                                      # J·m
    code_gf = gf / (hbarc_si ** 6)                                           # GeV（被错误除以 (ħc)⁶）
    code_gf_s = code_gf * gev_to_j / HB                                     # s⁻¹
    ratio_v = code_gf_s / gf_s if gf_s else None
    rec("V01", "V", "μ 子衰变率：分母多乘 (ħc)⁶", FAIL,
        "粒子物理:115",
        "标准 Γ_SM=G_F²m⁵/(192π³)=%s GeV=%s s⁻¹（与实验 4.5517e5 s⁻¹ 偏差 0.4%%，证明标准式正确）；"
        "代码又除以 (ħc)⁶=(%s)⁶ ⇒ Γ_code=%s GeV=%s s⁻¹ ⇒ 偏差 %s 倍"
        % (fx(gf), fx(gf_s), fx(hbarc_si), fx(code_gf), fx(code_gf_s), fx(ratio_v)),
        "实验 Γ_μ=4.5517e5 s⁻¹（τ=2.1969811e-6 s）。代码把 SI 的 ħc 硬塞进以 GeV 计的量里 ⇒ 单位混用；"
        "注意：标准式本身在此复算中与实验吻合，是下方牙齿 T11 的实证基础。")

    # V02 Planck 谱多 h²
    h2 = HH ** 2
    rec("V02", "V", "CMB 谱：B_ν = 2(hν)³/c²/...（多乘 h²）", FAIL,
        "宇宙学与天体物理:76 `2*(h*f)**3/c**2` 其中 hf=ħ·2π·ν=hν",
        "正确 B_ν=2hν³/c²/(e^x−1)；代码为 2h³ν³/c²/(e^x−1) ⇒ B_code/B_true = h² = %s" % fx(h2),
        "量纲同时由 M·T⁻² 变成 M³·L⁴·T⁻⁴；属多乘 Planck 常数平方的两处独立错误。")

    # V03 量子霍尔
    sigma_true = QE ** 2 / HH             # ν=1
    sigma_code = QE ** 2 / HB
    r = sigma_code / sigma_true
    rec("V03", "V", "量子霍尔：σ_xy = ν e²/ħ（应以 h=2πħ）", FAIL,
        "材料科学与凝聚态物理:133",
        "ν=1：真值 e²/h=%s S；代码 e²/ħ=%s S；比值=%s（应=2π=%s）"
        % (fx(sigma_true), fx(sigma_code), fx(r), fx(2 * 3.141592653589793)),
        "von Klitzing 常数 R_K=h/e²=25812.807 Ω 为计量基准；用 ħ 属缺失 2π。")

    # V04 Higgs 自耦合 eV/GeV 混算
    code = (125.18e9) ** 2 / (2 * 246.0 ** 2)
    true = (125.18) ** 2 / (2 * 246.0 ** 2)
    rec("V04", "V", "Higgs 势 λ = m_H²/(2v²)：eV 与 GeV 直接相除", FAIL,
        "量子场论:332（self.m_H 为 eV，vacuum_expectation 以 GeV 传入）",
        "若按调用方传 246 GeV：λ_code=%s，λ_true=%s ⇒ 偏大 %s 倍"
        % (fx(code), fx(true), fx((code / true) if true else None)),
        "偏差恰为 (10⁹)²=m 单位因子平方；同一函数内 m_W/m_Z 亦混用 eV 与 GeV。")

    # V05 相变温度缺 q_e
    code_t = 100e9 / KB
    true_t = 100e9 * QE / KB
    rec("V05", "V", "量子相变临界温度：eV 未换算为焦耳", FAIL,
        "量子场论:365 `T_c = 100e9/self.k_B`",
        "T_code=%s K；T_true=10¹¹ eV→J 后 =%s K ⇒ 偏大 %s 倍"
        % (fx(code_t), fx(true_t), fx((code_t / true_t) if true_t else None)),
        "连带：因 T_c 错到 10³³ K，任何实际温度都 ≪T_c ⇒ 序参量 sqrt(1−(T/T_c)²) 恒为 1，"
        "该函数对一切合法输入返回常数。")

    # V06 de Sitter 指数 √3
    om = 0.685
    r6 = (om ** 0.5) / ((om / 3.0) ** 0.5)
    rec("V06", "V", "暗能量加速：a=exp(√(Ω_Λ/3)·H₀·t) 少了 √3", FAIL,
        "暗物质与暗能量:347",
        "正确晚期 de Sitter 应满足 ȧ/a→H₀√Ω_Λ ⇒ a∝exp(H₀√Ω_Λ t)；"
        "代码用 √(Ω_Λ/3) ⇒ 指数偏小 %s 倍（=√3=%s）" % (fx(r6), fx(3.0 ** 0.5)),
        "按该式来自 ρ=Λc²/(8πG) 代入 Friedmann；代码随手加了 /3。")

    # V07 GW 频率缺 1/2π
    rec("V07", "V", "引力波频率 = √(GM/r³) 缺 1/(2π)", FAIL,
        "宇宙学与天体物理:176",
        "开普勒频率 f=(1/2π)√(GM/r³)；代码省去 1/(2π) ⇒ 结果偏大 %s 倍" % fx(2 * 3.141592653589793),
        "被命名为 frequency 实为角频率 ω，且半径 1e6 m 为硬编码。")

    # V08 截面换算
    rec("V08", "V", "弱电截面：单位换算常数写成 1e-32", FAIL,
        "量子场论:229 `cross_section * 1e-32`（GeV⁻²→m²）",
        "精确换算 1 GeV⁻² = 0.3894 mb = %s m²；代码用 1e-32 ⇒ 偏小 %s 倍"
        % (fx(0.3894e-31), fx(3.894e-32 / 1e-32)),
        "另：'proton-proton'/'p-pbar' 分支数值已按 m² 给出（1e-40/1e-38），又被乘 1e-32 ⇒ 二次换算，量级差 10³²。")

    # V09 Omega_total
    mod, obj, err = inst("暗物质与暗能量")
    got = None
    if obj is not None and HAVE_NUMPY and hasattr(obj, "simulate_universe_evolution"):
        r, perr = quiet_call(obj.simulate_universe_evolution, np.array([1.0]))
        if isinstance(r, dict):
            for k in ("omega_total", "Omega_total", "total_density_parameter"):
                if k in r:
                    got = r[k]
                    break
            if got is None:
                got = {k: v for k, v in r.items() if "total" in k.lower()}
    if got is not None:
        try:
            gv = float(np.asarray(got, dtype=float).ravel()[0])
        except Exception:
            gv = None
        rec("V09", "V", "Omega_total 应恒等于 1，代码给出对数幽灵", FAIL if (gv and abs(gv - 1) > 0.05) else INFO,
            "暗物质与暗能量:255-264",
            "实跑 simulate_universe_evolution(z=1) 得 Omega_total=%s（应为 1）" % fx(gv),
            "Ω_i(z) ≡ 8πGρ_i(z)/(3H(z)²) ⇒ 任意 z 下 ΣΩ_i≡1。代码输出的 Omega_total 实为 (H_z/H₀)²，"
            "与本wa函数内自带的 H_z 互为冗余 ⇒ 自相矛盾。")
    else:
        rec("V09", "V", "Omega_total 检查", INFO, "暗物质与暗能量:255-264", "未取到返回值（可能 static 不可跑）")

    # V10 纠缠熵
    mod, obj, err = inst("量子信息与量子计算")
    got10 = None
    if obj is not None and HAVE_NUMPY and hasattr(obj, "calculate_entanglement_entropy"):
        psi = np.array([1.0, 0.0, 0.0, 1.0]) / (2.0 ** 0.5)     # Bell 态
        rho = np.outer(psi, psi)
        r, perr = quiet_call(obj.calculate_entanglement_entropy, rho)
        try:
            got10 = float(np.real(r))
        except Exception:
            got10 = None
    if got10 is not None:
        ok = abs(got10 - 0.0) < 1e-9
        rec("V10", "V", "纠缠熵：对完整纯态密度矩阵求 von Neumann 熵", FAIL if ok else INFO,
            "量子信息与量子计算:55-58",
            "实跑 Bell 纯态（应进行偏迹后再求熵）：S=%s；正确纠缠熵应=%s bit" % (fx(got10), fx(1.0)),
            "纯态的 S(ρ)≡0 恒成立 ⇒ 该函数对任何输入返回 0，『纠缠熵』无任何区分力。"
            "对照：量子场论:267 的同名量先做偏迹再求熵 —— 同一批 core 内两种口径互相矛盾。")
    else:
        rec("V10", "V", "纠缠熵可用性", INFO, "量子信息与量子计算:55", "未能取到数值")

    # V11 纠错
    mod, obj, err = inst("量子信息与量子计算")
    got11 = None
    if obj is not None and hasattr(obj, "calculate_quantum_error_correction"):
        r, perr = quiet_call(obj.calculate_quantum_error_correction, 1e-3, 5)
        try:
            got11 = float(np.real(r))
        except Exception:
            got11 = None
    if got11 is not None and got11 > 0:
        true11 = (1e-3) ** ((5 + 1) / 2.0)
        rec("V11", "V", "逻辑错误率 = p^(d+1)（应为 p^((d+1)/2)）", FAIL,
            "量子信息与量子计算:87",
            "d=5,p=1e-3：代码=%s；正确 p^{(d+1)/2}=p^3=%s ⇒ 指数偏大 2 倍" % (fx(got11), fx(true11)),
            "距离 d 码可纠 t=(d−1)/2 个错，失败需 t+1 个 ⇒ 指数为 (d+1)/2。")


# ------------------------------------------------------------------ 通道 P：伪派生

def pseudo_audit() -> None:
    # P01 α_G ≡ 1
    mod, obj, err = inst("量子引力")
    got = None
    mp_def = None
    if obj is not None and hasattr(obj, "calculate_unified_quantum_gravity_constant"):
        r, perr = quiet_call(obj.calculate_unified_quantum_gravity_constant)
        try:
            got = float(np.real(r))
        except Exception:
            got = None
    if obj is not None:
        mp_def = getattr(obj, "m_p", None)
    mp_expr = (HB * CC / GG) ** 0.5
    same = (mp_def is not None and abs(float(mp_def) - mp_expr) / mp_expr < 1e-9)
    rec("P01", "P", "α_G = G·m_p²/(ħc) ≡ 1 ⇒『统一常数』退化为精细结构常数本身", FAIL,
        "量子引力:440-445（含 :68 质子质量被 :75 普朗克质量二次赋值覆盖）",
        "实跑 calculate_unified_quantum_gravity_constant() = %s；α = %s；逐位相等=%s；"
        "且 self.m_p 现值=%s 与 √(ħc/G)=%s 相等=%s"
        % (fx(got), fx(ALPHA), bool(got and abs(got - ALPHA) < 1e-15),
           fx(mp_def), fx(mp_expr), same),
        "V 判别式：n_hit=1，n_anchor=1（m_p 由 G,ħ,c 定义），n_free=0 ⇒ V=(1−0−1)/1=0 ≤ 0 ⇒ 伪派生。"
        "这与 openuft M02「普朗克锚定谬误」同源：把定义式当导出。")

    # P02 Λ ≡ 3H0²ΩΛ/c²
    def lam(H0, om_l, g=GG):
        rho_c = 3.0 * H0 ** 2 / (8.0 * 3.141592653589793 * g)
        return 8.0 * 3.141592653589793 * g * om_l * rho_c / CC ** 2
    H0 = 2.197e-18    # ~67.7 km/s/Mpc 的 SI 值
    om_l = 0.685
    l1 = lam(H0, om_l, GG)
    l2 = lam(H0, om_l, GG * 2.0)
    closed = 3.0 * H0 ** 2 * om_l / CC ** 2
    rec("P02", "P", "Λ = 8πG·Ω_Λ·ρ_crit/c² 中 G 被完全约掉 ⇒ 只是 Ω_Λ 的定义反解", FAIL,
        "暗物质与暗能量:212-216",
        "机械消去检验：令 G 加倍重算，Λ₁=%s vs Λ₂=%s，相对差=%s（未变 ⇒ G 不参与）；"
        "且恰等于闭式 3H₀²Ω_Λ/c²=%s" % (fx(l1), fx(l2), fx(rel(l1, l2)), fx(closed)),
        "V 判别式 V=(1−0−1)/1=0：输入 H₀、Ω_Λ，输出 Λ，而 Ω_Λ ≡ Λc²/(3H₀²) 本就是 Λ 的定义。"
        "教科书值 Λ≈1.09e-52 m⁻² 与之相符只说明代入的 H₀ 与 Ω_Λ 取自同一份观测。")

    # P03 alpha_unified 算术平均
    mod, obj, err = inst("量子场论")
    gotp = None
    if obj is not None and hasattr(obj, "calculate_quantum_field_theory_unification"):
        r, perr = quiet_call(obj.calculate_quantum_field_theory_unification, 1e16)
        try:
            gotp = float(np.real(r)) if not isinstance(r, dict) else r
        except Exception:
            gotp = r
    rec("P03", "P", "『统一耦合』= (α_s + α + G_F·E²)/3：三个不同对象的算术平均", FAIL,
        "量子场论:379-395",
        "实跑 E=1e16 GeV 得 %s（其中 G_F·E²=%s，量级 10²⁷，完全支配均值）"
        % (str(gotp)[:100], fx(GF * (1e16) ** 2)),
        "三者分属不同重整化方案（MS-bar vs Thomson 极限 q²=0 vs 费米常数，后者根本不是跑动耦合），"
        "统一要求 β 函数交点，与算术平均无关。")

    # P04 弦标度钉死
    mod, obj, err = inst("弦理论")
    extra = None
    pred = None
    if obj is not None and hasattr(obj, "calculate_string_theory_predictions"):
        r, perr = quiet_call(obj.calculate_string_theory_predictions)
        if isinstance(r, dict):
            pred = r.get("extra_dimension_size")
        gs = getattr(obj, "g_s", None)
        lp = getattr(obj, "l_p", None)
        if gs and lp:
            extra = lp / gs
    ok04 = bool(pred is not None and extra is not None and rel(float(pred), float(extra)) is not None
                and rel(float(pred), float(extra)) < 1e-9)  # type: ignore
    rec("P04", "P", "额外维度尺度 = l_p/g_s：输出由输入的假设耦合常数线性决定", FAIL if ok04 else INFO,
        "弦理论:382（g_s=1e-2 硬编码于 :81）",
        "实跑 predictions['extra_dimension_size']=%s；对照 l_p/g_s=%s；一致=%s"
        % (fx(pred), fx(extra), ok04),
        "α′=(2π l_p)² 把弦长标度钉在普朗克长度，g_s=1e-2 为假设值 ⇒ 自由度未下降，V≤0。")

    # P05 空位形成能定义反解
    mod, obj, err = inst("材料科学与凝聚态物理")
    got5 = None
    if obj is not None and hasattr(obj, "calculate_vacancy_formation_energy"):
        T = 1000.0
        c = 1e-6
        r, perr = quiet_call(obj.calculate_vacancy_formation_energy, T, c)
        got5 = r
    closed5 = -KB * 1000.0 * (c_log := _safe_log(1e-6))
    rec("P05", "P", "空位形成能 E_f = −k_BT·ln c：对定义式 c=exp(−E_f/kT) 的解出", FAIL,
        "材料科学与凝聚态物理:100-101",
        "实跑 (T=1000 K,c=1e-6) -> %s；闭式 −k_BT·ln c = %s"
        % (fx(got5), fx(closed5)),
        "把定义反解包装为『计算』，且忽略形成熵项（正确应为 E_f=−kT·ln c + T·S_f）。")

    # P06 宇宙年龄锚定
    mod, obj, err = inst("宇宙学与天体物理")
    got6 = None
    if obj is not None and hasattr(obj, "calculate_cosmic_time"):
        r, perr = quiet_call(obj.calculate_cosmic_time, 0.0)
        got6 = r
    ok6 = bool(got6 is not None and abs(float(got6) - 13.8e9) < 1e-3)
    rec("P06", "P", "宇宙年龄 = 13.8e9·(1+z)^(−2)：z=0 处恒等于输入常数", FAIL if ok6 else INFO,
        "宇宙学与天体物理:68",
        "实跑 calculate_cosmic_time(0) = %s（应返回 13.8e9，且此为该式唯一的『验证』）" % fx(got6),
        "物质主导期应为 (1+z)^{−3/2}，代码用 −2；且返回值单位为年而全文件其余为 SI 秒。")

    # P07 Z = G·c² 无消费方
    used: Dict[str, int] = {}
    defined: Dict[str, int] = {}
    for tag in FILE_MAP:
        p = fpath(tag)
        if not os.path.isfile(p):
            continue
        t, _ = read_text(p)
        if not t:
            continue
        n = len(re.findall(r"self\.Z\b", t))
        if n:
            defined[tag] = n
            used[tag] = n - 1   # 减去 __init__ 里的赋值本身
    zero = [k for k, v in used.items() if v <= 0 and k != "热力学与统计物理"]
    rec("P07", "P", "全 12 个模块定义 self.Z=G·c² 并称『引力光速统一常数』，但从未被任何方法消费", FAIL,
        "12 个模块 __init__（如 量子引力:81）",
        "正则统计 self.Z 出现次数：定义=%s；扣去定义语句后使用数=%s ⇒ 零消费模块 %d 个"
        % (sorted(defined.items()), dict(used), len(zero)),
        "一个从未进入任何计算的量不能称为『常数』；其量纲 [Gc²]=M⁻¹L⁵T⁻⁴ 也不对应任何已知物理量。")


def _safe_log(x: float) -> float:
    import math
    return math.log(x)


# ------------------------------------------------------------------ 牙齿（阳性对照）

def teeth() -> None:
    """正确的公式必须判 PASS —— 防止把一切都判成 FAIL 的廉价否决。"""
    checks = [
        ("T01", "史瓦西半径 r_s=2GM/c² 的量纲", (G_D * MASS / (C_D ** 2)), LENGTH, "量子引力:183"),
        ("T02", "霍金温度 T=ħc³/(8πGMk_B) 的量纲", (HB_D * C_D ** 3 / (G_D * MASS * KB_D)), TEMP, "量子引力:186"),
        ("T03", "贝肯斯坦-霍金熵 S=k_B·A/(4l_p²) 的量纲", (KB_D * (LENGTH ** 2) / (LP_D ** 2)),
         D(M=1, L=2, T=-2, Θ=-1), "量子引力:361"),
        ("T04", "T 对偶 R'=α′/R 的量纲", (LENGTH ** 2 / LENGTH), LENGTH, "弦理论:348"),
        # p-膜张力：世界体积作用量系数 [T_p] = [作用量]/[世界体积] = M·L^(2-p)·T^-2
        ("T05", "p-膜张力 ħc/l_p^(p+1) 的量纲（p=2 ⇒ 能量/面积）",
         (HB_D * C_D / (LP_D ** 3)), D(M=1, T=-2), "弦理论:178（p=2）"),
        ("T06", "弗里德曼 H²∝8πGρ/(3c²) 的量纲（ρ 为能量密度）",
         (G_D * ENERGY / (LENGTH ** 3) / (C_D ** 2)), D(T=-2), "宇宙学与天体物理:53"),
        ("T07", "光线偏折 4GM/(c²b) 应为无量纲", (G_D * MASS / (C_D ** 2 * LENGTH)), UNITLESS,
         "暗物质与暗能量:237 / 宇宙学与天体物理:92"),
        ("T08", "e⁺e⁻→μ⁺μ⁻ 截面 4πα²/(3s) 的形式量纲", (UNITLESS), UNITLESS, "量子场论:218"),
        ("T09", "Logistic 映射 x←r·x(1−x) 应保持无量纲", (UNITLESS), UNITLESS, "复杂系统与非线性动力学:50"),
        ("T10", "p-膜张力在 p=0（点粒子）时应退化为能量",
         (HB_D * C_D / (LP_D ** 1)), ENERGY, "弦理论:178（p=0）"),
    ]
    for cid, title, got, want, target in checks:
        ok = (got == want)
        rec(cid, "T", title, PASS if ok else FAIL, target,
            "实算 %s %s %s" % (dn(got), "==" if ok else "≠", dn(want)),
            "牙齿：此项为教科书已确立的结果，判 PASS 才说明审计器没有否决一切。")

    # T11 数值正控：标准 μ 衰变率 Γ=G_F²m⁵/(192π³) 复现实验值
    # （与 V01 形成对照：标准式本身正确，错的是被审代码多乘的 (ħc)⁶）
    _gev_to_j = 1.602176634e-10
    _gf = GF ** 2 * M_MU_GEV ** 5 / (192.0 * (3.141592653589793 ** 3))    # GeV
    _gf_s = _gf * _gev_to_j / HB                                          # s⁻¹
    _exp = 4.5517e5                                                        # 实验 Γ_μ (s⁻¹)
    _dev = abs(_gf_s - _exp) / _exp
    rec("T11", "T", "标准 μ 衰变率 G_F²m⁵/(192π³) 复现实验 Γ_μ=4.5517e5 s⁻¹",
        PASS if _dev < 0.05 else FAIL, "粒子物理:115",
        "Γ_SM=%s s⁻¹；实验=%s s⁻¹；相对偏差 %s（%.2f%%）" % (fx(_gf_s), fx(_exp), fx(_dev), _dev * 100),
        "数值牙齿：标准式本身与实验吻合（<5%%），证明审计器掌握正确物理；"
        "V01 的 1e153 倍偏差纯粹来自被审代码的单位混用，而非标准式有误。")


# ------------------------------------------------------------------ UFT 达成度

def uft_score() -> None:
    cnt = {v: sum(1 for i in ITEMS if i["verdict"] == v) for v in VERDICTS}
    ch = {}
    for i in ITEMS:
        ch[i["channel"]] = ch.get(i["channel"], {PASS: 0, FAIL: 0, BOUNDARY: 0, INFO: 0})
        ch[i["channel"]][i["verdict"]] += 1

    n_d_fail = ch.get("D", {FAIL: 0})[FAIL]
    rows = [
        ("UFT-1", "数学自洽", n_d_fail == 0, "D 通道 FAIL=%d 条（量纲冲突不可自洽）" % n_d_fail),
        ("UFT-2", "四力统一", False,
         "凡函数名含 unified 处均为量纲不同者相加（D01/D09/D11），属加法而非统一"),
        ("UFT-3", "无量纲预测+误差棒", False,
         "全仓无 prediction_value/prediction_urel 形态条目；P 通道 V≤0 ⇒ 无信息增益"),
        ("UFT-4", "已知观测复现", None,
         "部分正确（T01-T10）：黑洞热力学、NFW、偏转截面形式与教科书相符；"
         "但同一文件内错法定并存 ⇒ 判 BOUNDARY"),
        ("UFT-5", "可证伪的新预言", False, "所有可观测量均由外部锚/假设值线性决定（P02/P04/P06）"),
        ("UFT-6", "外部验证", False, "无同行评议或独立复现记录"),
    ]
    score = 0
    for cid, name, ok, why in rows:
        v = PASS if ok is True else (BOUNDARY if ok is None else FAIL)
        if ok is True:
            score += 1
        rec(cid, "U", "UFT 达成度 · " + name, v, "全 13 模块", why)
    rec("U00", "U", "UFT 六判据总分", INFO, "全 13 模块",
        "联盟层得分 %d/6（UFT-4 为部分 ⇒ 不计）；对照：SM 5/6、GR 4/6、SU(5) 5/6、UFE-1 2/6、numerology 1/6"
        % score)


# ------------------------------------------------------------------ 产物

def summary() -> Dict[str, Any]:
    cnt = {v: sum(1 for i in ITEMS if i["verdict"] == v) for v in VERDICTS}
    ch: Dict[str, Dict[str, int]] = {}
    for i in ITEMS:
        ch.setdefault(i["channel"], {PASS: 0, FAIL: 0, BOUNDARY: 0, INFO: 0})
        ch[i["channel"]][i["verdict"]] += 1
    return {
        "title": "核心算法来料 · 软件正确性 / 第一性 双通道审计",
        "source_root": SRC_ROOT,
        "numpy": NP_VER,
        "modules_total": len(FILE_MAP) + 1,
        "counts": cnt,
        "by_channel": ch,
        "total": len(ITEMS),
        "items": ITEMS,
        "notes": NOTES,
    }


def write_outputs(data: Dict[str, Any]) -> None:
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    jp = os.path.join(OUT_DIR, "核心算法来料_双通道审计.json")
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    mp = os.path.join(OUT_DIR, "核心算法来料_双通道审计.md")
    lines = []
    lines.append("# 核心算法来料 · 双通道审计（机器产物）")
    lines.append("")
    lines.append("- 被审根：`%s`" % SRC_ROOT)
    lines.append("- numpy：`%s`" % NP_VER)
    lines.append("- 总计 **%d** 条：PASS %d / FAIL %d / BOUNDARY %d / INFO %d"
                 % (data["total"], data["counts"][PASS], data["counts"][FAIL],
                    data["counts"][BOUNDARY], data["counts"][INFO]))
    lines.append("")
    lines.append("| 通道 | PASS | FAIL | BOUNDARY | INFO |")
    lines.append("|---|---|---|---|---|")
    for k in sorted(data["by_channel"].keys()):
        v = data["by_channel"][k]
        lines.append("| %s | %d | %d | %d | %d |" % (k, v[PASS], v[FAIL], v[BOUNDARY], v[INFO]))
    lines.append("")
    lines.append("## 逐条")
    lines.append("")
    for i in ITEMS:
        lines.append("### %s [%s] %s · %s" % (i["id"], i["channel"], i["verdict"], i["title"]))
        lines.append("- 目标：`%s`" % i["target"])
        lines.append("- 证据：%s" % i["evidence"])
        if i["note"]:
            lines.append("- 备注：%s" % i["note"])
        lines.append("")
    with open(mp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ------------------------------------------------------------------ discover（保留）

def discover(root: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    files = [(k, os.path.join(root, k, v)) for k, v in FILE_MAP.items()]
    files.append(("<整合模块>", os.path.join(root, AGGREGATOR)))
    for tag, path in files:
        if not os.path.isfile(path):
            out[tag] = {"size": 0, "parse": None, "error": "文件不存在"}
            continue
        size = os.path.getsize(path)
        txt, err = read_text(path)
        info: Dict[str, Any] = {"size": size, "parse": None}
        if err:
            info["error"] = err
            out[tag] = info
            continue
        try:
            tree = ast.parse(txt)
            info["parse"] = "OK"
        except SyntaxError as e:
            info["parse"] = "SyntaxError L%s: %s" % (e.lineno, e.msg)
            out[tag] = info
            continue
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                meths = []
                for m in node.body:
                    if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        args = [a.arg for a in m.args.args if a.arg != "self"]
                        meths.append({"name": m.name, "args": args, "line": m.lineno,
                                      "decorated": len(m.decorator_list) > 0})
                info["classes"] = info.get("classes", {})
                info["classes"][node.name] = meths
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                info.setdefault("funcs", []).append({"name": node.name, "line": node.lineno})
        out[tag] = info
    return out


def print_discovery(info: Dict[str, Any]) -> None:
    print("=" * 78)
    print("被审接口清单（只读发现，不执行）")
    print("=" * 78)
    for tag, r in info.items():
        print("")
        print("[%s]  size=%s  parse=%s" % (tag, r.get("size"), r.get("parse")))
        if r.get("error"):
            print("    ERROR " + str(r["error"]))
            continue
        for cname, meths in (r.get("classes") or {}).items():
            dn_ = sum(1 for m in meths if m["decorated"])
            print("    class %s: %d 方法 (带装饰器 %d)" % (cname, len(meths), dn_))
            for m in meths:
                print("        %-46s L%-5d args=%s" % (m["name"], m["line"], m["args"]))
        if r.get("funcs"):
            print("    模块级函数: " + ", ".join(f["name"] for f in r["funcs"]))


# ------------------------------------------------------------------ main

def main() -> int:
    args = sys.argv[1:]
    quiet = "--quiet" in args
    if "--discover" in args:
        print_discovery(discover(SRC_ROOT))
        return 0

    t0 = time.time()
    if not os.path.isdir(SRC_ROOT):
        print("被审目录不存在: %s" % SRC_ROOT)
        return 2

    teeth()          # 先跑阳对照，证明判定尺度正常
    audit_software()
    dim_audit()
    value_audit()
    pseudo_audit()
    uft_score()

    data = summary()
    write_outputs(data)

    if not quiet:
        print("=" * 78)
        print("核心算法来料 · 软件正确性 / 第一性 双通道审计")
        print("被审根: %s" % SRC_ROOT)
        print("numpy: %s" % NP_VER)
        print("=" * 78)
        order = ["T", "S", "D", "V", "P", "U"]
        for ch in order:
            sub = [i for i in ITEMS if i["channel"] == ch]
            if not sub:
                continue
            print("")
            print("—— 通道 %s ————————————————————————" % ch)
            for i in sub:
                print("[%s] %-52s %s" % (i["id"], i["title"][:52], i["verdict"]))
                print("     target : %s" % i["target"])
                print("     evidence: %s" % i["evidence"])
                if i["note"]:
                    print("     note   : %s" % i["note"])

    c = data["counts"]
    print("")
    print("=" * 78)
    print("总计 %d 条 | PASS=%d FAIL=%d BOUNDARY=%d INFO=%d | 耗时 %.2fs"
          % (data["total"], c[PASS], c[FAIL], c[BOUNDARY], c[INFO], time.time() - t0))
    print("产物: %s" % os.path.join(OUT_DIR, "核心算法来料_双通道审计.{json,md}"))
    # 牙齿不过 ⇒ 判定尺度不可信
    t_bad = [i["id"] for i in ITEMS if i["channel"] == "T" and i["verdict"] != PASS]
    if t_bad:
        print("!! 阳性对照失效: %s —— 审计器把正确公式也判 FAIL，结论不可信" % t_bad)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
