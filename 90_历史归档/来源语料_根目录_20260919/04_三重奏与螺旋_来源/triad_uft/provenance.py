# -*- coding: utf-8 -*-
"""
triad_uft.provenance — 诚实审计元数据
=====================================
每个定理/函数的验证状态、精度、来源轮次。
严格区分：已严格证明(PROVEN) / 数值验证(VERIFIED) / 开放(OPEN) / 已证伪(FALSIFIED)。
"""
from enum import Enum


class ValidationStatus(Enum):
    PROVEN = "严格证明"        # 解析证明闭合
    VERIFIED = "数值验证"      # 高精度数值确认
    OPEN = "开放问题"          # 未解决
    FALSIFIED = "已证伪"       # 被实验/数学排除
    CONJECTURE = "推测"        # 理论自洽但未验证


class TheoremRecord:
    """单条定理的审计记录"""
    def __init__(self, name, status, precision=None, round_ref=None, note=""):
        self.name = name
        self.status = status
        self.precision = precision
        self.round_ref = round_ref
        self.note = note

    def __repr__(self):
        s = f"[{self.status.value}] {self.name}"
        if self.precision:
            s += f" (精度={self.precision})"
        if self.round_ref:
            s += f" [R{self.round_ref}]"
        return s


# 定理注册表
THEOREMS = {
    "helix_triad": TheoremRecord(
        "螺旋三重奏 κ²+τ²=(ω/v)²",
        ValidationStatus.PROVEN, "sympy精确差=0", "R4",
        "匀速螺旋的运动学必然关系"),
    "alldim_triad": TheoremRecord(
        "全维三重奏 Σκᵢ²=(Σωⱼ²)/v²",
        ValidationStatus.PROVEN, "≤1.94e-29 (12组随机)", "R9",
        "D维匀速多平面超螺旋，四步严格证明闭合"),
    "adiabatic_triad": TheoremRecord(
        "绝热三重奏（缓变频率二阶修正）",
        ValidationStatus.VERIFIED, "斜率≈2.00（一阶消去）", "R10",
        "θ(t)=ω₀t+½εt²，修正~O(ε²)"),
    "pure_circle_exact": TheoremRecord(
        "纯圆周精确性（b=0任意时变角速度）",
        ValidationStatus.PROVEN, "3.9e-31", "R10",
        "κ=1/R纯几何常数，τ=0，恒等"),
    "gradient_b_field_exact": TheoremRecord(
        "梯度磁场三重奏精确性",
        ValidationStatus.PROVEN, "1.17e-18 (mpmath 50位)", "R11",
        "方向不变的任意空间梯度磁场B(x)中精确恒等"),
    "lorentz_dictionary": TheoremRecord(
        "洛伦兹力字典 ω=qB/(γm)",
        ValidationStatus.VERIFIED, "电子B=1T相对差0.0", "R6",
        "三重奏ω=相对论回旋频率"),
    "codata_constants": TheoremRecord(
        "CODATA 2022常数对标",
        ValidationStatus.VERIFIED, "δ=1.1e-5 (G的误差传播)", "R3",
        "ℓ_P, M_P, E_P等250位"),
    "constant_generation": TheoremRecord(
        "三重奏反向生成物理常数",
        ValidationStatus.FALSIFIED, "sympy解空集", "R2",
        "欠定+循环论证，不可能"),
    "kk_extra_dimension": TheoremRecord(
        "KK绑额外维解读（R_curv=R_c/n）",
        ValidationStatus.FALSIFIED, "矛盾6.8–11数量级", "R3",
        "与亚毫米引力+观测曲率下界冲突"),
    "isotropic_form": TheoremRecord(
        "各向同性形式 (D−1)κ²=(ω/c)²",
        ValidationStatus.FALSIFIED, "6维偏差45%, 8维123%", "R6",
        "高维下不成立"),
    "curved_spacetime": TheoremRecord(
        "弯曲时空推广",
        ValidationStatus.OPEN, None, None,
        "GR弯曲时空中世界线Frenet结构未推导"),
    "quantization": TheoremRecord(
        "三重奏量子化",
        ValidationStatus.OPEN, None, None,
        "路径积分/算符形式未建立"),
    "relativistic_gradient": TheoremRecord(
        "相对论/磁场方向变化/漂移",
        ValidationStatus.OPEN, None, "R11",
        "当前为经典非相对论、方向不变磁场"),
}


def honesty_statement():
    """返回诚实声明文本"""
    return (
        "【诚实声明】triad_uft 封装的是已严格证明的几何-运动学定理，"
        "不是已完成的'万有理论'。引力的量子化、暗物质/暗能量、"
        "弯曲时空推广等仍为开放问题。所有函数的验证状态见 provenance.THEOREMS。"
    )


def audit_report():
    """生成完整审计报告文本"""
    lines = [honesty_statement(), "", "=== 定理审计表 ==="]
    for key, rec in THEOREMS.items():
        lines.append(f"  {rec}")
        if rec.note:
            lines.append(f"      → {rec.note}")
    return "\n".join(lines)
