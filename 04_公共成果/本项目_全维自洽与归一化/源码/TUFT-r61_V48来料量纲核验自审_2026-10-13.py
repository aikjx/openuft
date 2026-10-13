# -*- coding: utf-8 -*-
"""
TUFT-r61 · V4.8「来料量纲核验报告」自审引擎（纯标准库）

任务：对用户提供的《TUFT-V4.8 量纲核验报告》做机器化复核。
该来料声称 S_spiral 体作用量系数 ℏ/(2c) 有量纲错误，并给出修正
ℏc/l0^2 + 一处「干净」最终作用量。本引擎逐项复算，并检验：

  (a) 来料对「原系数错在哪」的诊断是否自洽；
  (b) 来料给出的「修正系数 ℏc/l0^2」是否真的修复；
  (c) 来料「干净版最终作用量」的方括号内两项能否相减（量纲是否同族）；
  (d) 与既有 r45（T12 缺口=c^2、最小修复 ℏc/2）、r42（l0 撞 Ω5）是否一致。

量纲基：(M, L, T)，指数用 Fraction（本册全为整数，Fraction 仅为自检稳健）。
约定：∇ 取长度约定 [L^-1]（与 r45 T12 一致；混合约定下 g^{μν}∇_μκ∇_νκ 同为 [L^-4]）。
"""

from fractions import Fraction as F
import json
import os
import runpy  # noqa

# ----------------------------------------------------------------------------
# 量纲表示
# ----------------------------------------------------------------------------
BASES = ("M", "L", "T")


class Dim:
    """简单量纲，基向量 (M, L, T)。"""

    def __init__(self, m=0, l=0, t=0):
        self.e = {"M": F(m), "L": F(l), "T": F(t)}

    def __eq__(self, other):
        return all(self.e[b] == other.e[b] for b in BASES)

    def __hash__(self):
        return hash(tuple(self.e[b] for b in BASES))

    def __repr__(self):
        parts = []
        for b in BASES:
            e = self.e[b]
            if e == 0:
                continue
            s = ("^%s" % e) if e != 1 else ""
            parts.append("%s%s" % (b, s))
        return "·".join(parts) if parts else "1"

    # 运算：乘法=指数加，除法=指数减，幂=指数乘
    def __mul__(self, other):
        return Dim(*(self.e[b] + other.e[b] for b in BASES))

    def __add__(self, other):
        if self != other:
            raise TypeError("量纲异族不可相加: %s + %s" % (self, other))
        return Dim(*(self.e[b] for b in BASES))

    def __sub__(self, other):
        if self != other:
            raise TypeError("量纲异族不可相减: %s - %s" % (self, other))
        return Dim(*(self.e[b] for b in BASES))

    def __truediv__(self, other):
        return Dim(*(self.e[b] - other.e[b] for b in BASES))

    def __pow__(self, n):
        return Dim(*(self.e[b] * n for b in BASES))

    def is_dimensionless(self):
        return all(self.e[b] == 0 for b in BASES)


# ----------------------------------------------------------------------------
# 基本量纲
# ----------------------------------------------------------------------------
M, L, T = Dim(m=1), Dim(l=1), Dim(t=1)
ZERO = Dim()

hbar = Dim(m=1, l=2, t=-1)          # [J·s] = [M L^2 T^-1]
c = Dim(l=1, t=-1)                  # [L T^-1]
kappa = Dim(l=-1)                   # Frenet: κ=[L^-1]
nabla = Dim(l=-1)                   # 长度约定 ∇=[L^-1]
omega = Dim(t=-1)                   # ω=[T^-1]
theta = ZERO                        # 倾角无量纲
l0 = Dim(l=1)                       # 来料引入的特征长度

hbar_over_c = hbar / c              # [ℏ/c]=[M L]
hbar_c = hbar * c                   # [ℏc]=[M L^3 T^-2]
E = Dim(m=1, l=2, t=-2)            # 能量 [J]=[M L^2 T^-2]
energy_density = E / (L ** 3)      # [J/m^3]=[M L^-1 T^-2]
grad_kappa = nabla * kappa          # [∇κ]=[L^-2]
grad_kappa_sq = grad_kappa ** 2     # [|∇κ|^2]=[L^-4]

# ----------------------------------------------------------------------------
# 计算各项
# ----------------------------------------------------------------------------
kinetic_orig = hbar_over_c * grad_kappa_sq          # [ℏ/(2c)|∇κ|^2]
gap_orig = energy_density / kinetic_orig            # 应为 c^2=[L^2 T^-2]

kinetic_correct = hbar_c * grad_kappa_sq            # 正确系数 ℏc（无 l0）
kinetic_pasted_fix = (hbar_c / (l0 ** 2)) * grad_kappa_sq   # 来料修正 ℏc/l0^2
gap_pasted_fix = energy_density / kinetic_pasted_fix         # 应为 1（修复），实际非 1

# 来料「干净版」方括号：g^{μν}∇_μκ∇_νκ − (κ²/sin²θ − ω²/c²)
clean_term1 = grad_kappa_sq                         # [L^-4]
clean_term2_a = kappa ** 2                          # [κ²]=[L^-2]
clean_term2_b = (omega ** 2) / (c ** 2)             # [ω²/c²]=[L^-2]
clean_term2 = clean_term2_a + clean_term2_b         # [L^-2]（同族可加）
clean_bracket_ok = (clean_term1 == clean_term2)     # 能否相减?

# 正确势项形式：(1/c^4)(c²κ²/sin²θ − ω²)^2
V_inner = (c ** 2) * (kappa ** 2) - (omega ** 2)    # [T^-2]
V = V_inner ** 2                                    # [T^-4]
V_over_c4 = V / (c ** 4)                            # [L^-4]
correct_bracket_ok = (grad_kappa_sq == V_over_c4)   # 正确方括号两项 [L^-4]
action_correct = hbar_c * (grad_kappa_sq - V_over_c4)  # 应=能量密度


# ----------------------------------------------------------------------------
# 来料 §2.1 自洽性检验
#   来料写： [ℏ/(2c)|∇κ|²] = [J·s]/[m/s]·[m^-1]^2·[m^-2]
#            = [kg·m]·[m^-2] = [kg·m^-1]
#   矛盾：其输入列了 [m^-1]^2·[m^-2]=[m^-4]，却只乘了一个 [m^-2]。
# ----------------------------------------------------------------------------
pasted_input_dim = (kappa ** 2) * (kappa ** 2)      # 来料输入写的 [m^-1]^2·[m^-2]=[m^-4]=[L^-4]
pasted_claimed_result = hbar_over_c * (kappa ** 2)  # 若只乘 [m^-2]（κ^2）=> [M L^-1]
pasted_literal_result = hbar_over_c * pasted_input_dim  # 实际按输入应得 [M L^-3]
pasted_gap_claim = Dim(t=-2)                        # 来料声称缺口 [s^-2]=[T^-2]

# ----------------------------------------------------------------------------
# 自检 guard（判据反噬自身）
# ----------------------------------------------------------------------------
guards = []


def guard(name, cond):
    guards.append((name, bool(cond)))
    return bool(cond)


guard("energy_density_is_ML-1T-2", energy_density == Dim(m=1, l=-1, t=-2))
guard("mul_is_additive_not_multiplicative",
      (hbar_over_c * grad_kappa_sq) == kinetic_orig)
guard("orig_gap_is_c^2", gap_orig == (c ** 2))
guard("correct_coeff_hbar_c_closes", kinetic_correct == energy_density)
guard("pasted_fix_does_NOT_close", kinetic_pasted_fix != energy_density)
guard("pasted_fix_off_by_L^2", gap_pasted_fix == (L ** 2))
guard("clean_bracket_mismatched_cannot_subtract", not clean_bracket_ok)
guard("clean_term1_is_L-4", clean_term1 == Dim(l=-4))
guard("clean_term2_is_L-2", clean_term2 == Dim(l=-2))
guard("correct_potential_form_L-4", correct_bracket_ok)
guard("correct_action_closes", action_correct == energy_density)
guard("pasted_step3_input_L-4", pasted_input_dim == Dim(l=-4))
guard("pasted_step3_claimed_result_WRONG",
      pasted_claimed_result != pasted_literal_result)
guard("pasted_gap_claim_WRONG", pasted_gap_claim != gap_orig)

# ----------------------------------------------------------------------------
# 逐条读数（T 系列）
# ----------------------------------------------------------------------------
tests = []
tests.append(("T01", "FAIL", "来料 §2.1 称 [ℏ/(2c)|∇κ|²]=[kg·m⁻¹]",
              "机器(按来料输入 [m⁻⁴]): %s；按来料结论 [m⁻²]: %s"
              % (pasted_literal_result, pasted_claimed_result),
              "输入与结论自相矛盾：列了 [m⁻⁴] 却得出 [kg·m⁻¹]=[M L⁻¹]"))
tests.append(("T02", "FAIL", "来料称缺口=[s⁻²]",
              "机器缺口=%s；应为 %s" % (gap_orig, c ** 2),
              "缺口实为 c²=[L²T⁻²]，与 r45 T12 一致；[s⁻²] 错"))
tests.append(("T03", "PASS", "原系数 ℏ/(2c) 确有量纲错误",
              "动能项=%s vs 能量密度 %s" % (kinetic_orig, energy_density),
              "来料『原系数错』的诊断方向对，但论据错"))
tests.append(("T04", "FAIL", "来料修正系数 ℏc/l0² 修复作用量",
              "动能项=%s ≠ 能量密度 %s（差 %s）"
              % (kinetic_pasted_fix, energy_density, gap_pasted_fix),
              "ℏc/l0² 仍差 L²；正确系数应为 ℏc（无 l0）"))
tests.append(("T05", "FAIL", "来料「干净版」方括号可相减",
              "项1 %s=[L⁻⁴]；项2 %s=[L⁻²]" % (clean_term1, clean_term2),
              "两项目纲异族，不可相减 → 最终式本身不合法"))
tests.append(("T06", "PASS", "正确最小修复 ℏc/2（r45 P1）量纲闭合",
              "动能项=%s = 能量密度" % kinetic_correct,
              "零新参数；与 r45 T13 同型"))
tests.append(("T07", "PASS", "正确势项形式 (1/c⁴)(c²κ²/sin²θ−ω²)²",
              "势内项=%s=[L⁻⁴]，与作用量梯度项同族" % V_over_c4,
              "来料漏 c⁴ 与平方，导致 [L⁻²]"))
tests.append(("T08", "FAIL", "来料 §6 引入 l0 为新基本长度",
              "l0 量纲=%s" % l0,
              "r42 已裁：l0 要么自由常数(外部输入+1,撞Ω5)，要么=l_P(零信息)"))
tests.append(("T09", "INFO", "来料「全部量纲验证通过 ✓」结论",
              "引擎实测：T04/T05 直接推翻该结论",
              "来料自评结论不成立"))

n_pass = sum(1 for t in tests if t[1] == "PASS")
n_fail = sum(1 for t in tests if t[1] == "FAIL")
n_info = sum(1 for t in tests if t[1] == "INFO")
n_guard = sum(1 for g in guards if g[1])
guard_all = (n_guard == len(guards))

verdict = ("FAIL" if n_fail else "PASS")  # 来料整体未通过自审
rating = "来料 C/L1：诊断方向对、论据与修正均错；与 r45/r42 同结论但更退步"

# ----------------------------------------------------------------------------
# 输出
# ----------------------------------------------------------------------------
OUT_DIR = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/数据"
BASENAME = "TUFT-r61_V48来料量纲核验自审_2026-10-13"
os.makedirs(OUT_DIR, exist_ok=True)

payload = {
    "audit": "TUFT-r61",
    "subject": "V4.8 来料《量纲核验报告》自审",
    "verdict": verdict,
    "rating": rating,
    "counts": {"PASS": n_pass, "FAIL": n_fail, "INFO": n_info},
    "guard": {"n_pass": n_guard, "n_total": len(guards), "all_pass": guard_all},
    "dimensions": {
        "hbar_over_c": str(hbar_over_c),
        "hbar_c": str(hbar_c),
        "grad_kappa_sq": str(grad_kappa_sq),
        "energy_density": str(energy_density),
        "kinetic_orig": str(kinetic_orig),
        "gap_orig": str(gap_orig),
        "kinetic_correct": str(kinetic_correct),
        "kinetic_pasted_fix": str(kinetic_pasted_fix),
        "gap_pasted_fix": str(gap_pasted_fix),
        "clean_term1": str(clean_term1),
        "clean_term2": str(clean_term2),
        "V_over_c4": str(V_over_c4),
        "pasted_input_dim": str(pasted_input_dim),
        "pasted_claimed_result": str(pasted_claimed_result),
        "pasted_literal_result": str(pasted_literal_result),
        "pasted_gap_claim": str(pasted_gap_claim),
    },
    "tests": [
        {"id": t[0], "judge": t[1], "claim": t[2], "machine": t[3], "note": t[4]}
        for t in tests
    ],
    "guards": [{"name": g[0], "pass": g[1]} for g in guards],
}

with open(os.path.join(OUT_DIR, BASENAME + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

# MD 数据册
md_lines = []
md_lines.append("# TUFT-r61 · V4.8 来料量纲核验 · 机器数据册\n")
md_lines.append("- 裁决：**%s** · 评级：%s" % (verdict, rating))
md_lines.append("- 条目：PASS %d / FAIL %d / INFO %d" % (n_pass, n_fail, n_info))
md_lines.append("- 自检 guard：%d/%d 全过=%s\n" % (n_guard, len(guards), guard_all))
md_lines.append("## 关键量纲")
for k, v in payload["dimensions"].items():
    md_lines.append("- `%s` = %s" % (k, v))
md_lines.append("\n## 逐条读数")
for t in tests:
    md_lines.append("- **%s [%s]** %s — 机器：%s | %s" % (t[0], t[1], t[2], t[3], t[4]))
md_lines.append("\n## 自检 guard")
for g in guards:
    md_lines.append("- [%s] %s" % ("PASS" if g[1] else "FAIL", g[0]))
with open(os.path.join(OUT_DIR, BASENAME + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines) + "\n")

# report.txt（与 md 同口径）
report = []
report.append("TUFT-r61 V4.8 来料量纲核验自审 生成时刻=%s" % __import__("datetime").datetime.now().isoformat())
report.append("模块=%s" % os.path.abspath(__file__))
report.append("裁决=%s  评级=%s" % (verdict, rating))
report.append("条目 PASS=%d FAIL=%d INFO=%d   guard=%d/%d" % (n_pass, n_fail, n_info, n_guard, len(guards)))
report.append("")
for t in tests:
    report.append("%s %s | %s" % (t[0], t[1], t[2]))
    report.append("    machine: %s" % t[3])
    report.append("    note:    %s" % t[4])
report.append("")
report.append("GUARDS:")
for g in guards:
    report.append("  [%s] %s" % ("PASS" if g[1] else "FAIL", g[0]))
with open(os.path.join(OUT_DIR, BASENAME + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report) + "\n")

# 退出码：guard 全过 且 自检全过 才算完成
raise SystemExit(0 if (guard_all and verdict == "FAIL") else 1)
