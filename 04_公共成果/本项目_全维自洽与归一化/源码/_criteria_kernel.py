# -*- coding: utf-8 -*-
"""
判据联盟 · 共享内核（ASCII 文件名，便于 import）

目的（优化/修复）：消除 r61–r69 各引擎中的重复样板，统一门禁语义，
避免"同一判据在不同册里实现不一致"的维护隐患。

提供：
  Dim          —— 极简 (M,L,T) 量纲类
  GuardBook    —— guard 登记表（判据反噬自身 + 正对照强制）
  surplus_of / passes_threshold —— 超定判据（r69）
  is_circular                   —— 循环检测器（O ∈ M，r69）
  write_triplet                —— json / md / report 三件套写出
  dec_sqrt                     —— Decimal 开方（无 numpy/sympy 环境）

纪律（固化）：
  1. guard 必须可复跑、可机读；门槛常量不得写死 True。
  2. 任何"零"结论必须配正对照（GuardBook.require_control）。
  3. 中文文案一律用「」，源码内 ASCII 双引号只作字符串定界（r68 踩坑三次）。
"""
import json
import math
import os
from decimal import Decimal, getcontext

getcontext().prec = 50


# ---------------------------------------------------------------------------
# 量纲
# ---------------------------------------------------------------------------
class Dim:
    __slots__ = ("M", "L", "T")

    def __init__(self, M, L, T):
        self.M, self.L, self.T = M, L, T

    def __mul__(self, o):
        return Dim(self.M + o.M, self.L + o.L, self.T + o.T)

    def __truediv__(self, o):
        return Dim(self.M - o.M, self.L - o.L, self.T - o.T)

    def __pow__(self, n):
        return Dim(self.M * n, self.L * n, self.T * n)

    def __eq__(self, o):
        return (self.M, self.L, self.T) == (o.M, o.L, o.T)

    def __hash__(self):
        return hash((self.M, self.L, self.T))

    def __repr__(self):
        return "Dim(M%d L%d T%d)" % (self.M, self.L, self.T)


M, L, T = Dim(1, 0, 0), Dim(0, 1, 0), Dim(0, 0, 1)


def dec_sqrt(x):
    """Decimal 开方（纯标准库）。"""
    return Decimal(str(math.sqrt(float(x))))


# ---------------------------------------------------------------------------
# guard 登记
# ---------------------------------------------------------------------------
class GuardBook:
    """判据登记表：强制记录、强制正对照。"""

    def __init__(self, subject=""):
        self.rows = []
        self.subject = subject

    def guard(self, name, cond):
        self.rows.append((name, bool(cond)))
        return bool(cond)

    def require_control(self, control_name, cond):
        """正对照：证明判据能识别"是"，非恒否。"""
        return self.guard("POSCTRL_" + control_name, cond)

    def all_pass(self):
        return all(c for _, c in self.rows)

    @property
    def n(self):
        return len(self.rows)

    def exit_code(self, min_guards=8):
        return 0 if (self.all_pass() and self.n >= min_guards) else 1


# ---------------------------------------------------------------------------
# 判据：循环检测 + 超定（r69）
# ---------------------------------------------------------------------------
def is_circular(output, fixing_set):
    """循环检测器：预言量 O 是否出现在定参集合 M 中。"""
    return output in fixing_set


def surplus_of(n_matched, n_free, circular=False):
    """surplus = n_matched − n_free；循环者一律判 0（O∈M 无预测内容）。"""
    if circular:
        return 0
    return n_matched - n_free


def threshold_of(n_free):
    """真预测要求 n_matched ≥ n_free + 1。"""
    return n_free + 1


def passes_threshold(n_matched, n_free, circular=False):
    return (not circular) and (n_matched >= threshold_of(n_free))


# ---------------------------------------------------------------------------
# 输出三件套
# ---------------------------------------------------------------------------
def write_triplet(out_dir, basename, payload, md_lines, report_lines):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, basename + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(os.path.join(out_dir, basename + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")
    with open(os.path.join(out_dir, basename + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")
