# -*- coding: utf-8 -*-
"""
修复版核心方程集 v2.0 —— 精算守卫 (68_fix_v2_numerics)
============================================================

配套文档：07_统一场方程/68_修复版核心方程集_v2.0_2026-10-20.md

纪律（openuft 红线）：
  * 本脚本是文档 §6「精算结果」的唯一数字来源；文档里的每个数字都从这里注入，
    不接受“先算数、再把判定写死”的死代码。
  * 每道守卫的 PASS/FAIL 由计算结果实时驱动；任一守卫 FAIL，脚本以非 0 退出码离场。
  * 恒等式（如 F1 c=1/sqrt(μ0ε0)、F3 vev 回代、F5c r_s(m_P)=2ℓ_P）明确标注为
    INFO 级（定义重排，零信息增量），不与“新物理预言”混为一谈。

精度：mpmath mp.dps = 250（十进制 250 位）。
外部常数：CODATA 2022 / PDG 2024 / IAU 2015 名义值，均在脚本头部声明，来源可复核。
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import mpmath as mp

mp.mp.dps = 250  # 250 位十进制精度

# ----------------------------------------------------------------------------
# 头部常数（来源可复核；除 c 为 SI 定义精确外，其余为最新实验/名义值）
# ----------------------------------------------------------------------------
C       = mp.mpf('299792458')                 # 真空中光速，SI 长度/时间定义精确
MU0     = 4 * mp.pi * mp.mpf('1e-7')          # 真空磁导率（2019-SI 前定义精确；现代 SI 为导出量，此处取定义身份）
ALPHA   = mp.mpf('0.0072973525693')           # 精细结构常数 1/137.035999084
SIN2TW  = mp.mpf('0.23122')                   # 弱混合角 sin²θ_W（on-shell 有效）
MZ      = mp.mpf('91.1876')                   # Z 玻色子质量 [GeV]
MW_MEAS = mp.mpf('80.3692')                   # W 玻色子测量质量 [GeV]（PDG 2024 世界平均）
V_HIGGS = mp.mpf('246.22')                    # Higgs 真空期望值 [GeV]
MH      = mp.mpf('125.25')                    # Higgs 质量 [GeV]（PDG 2024）
NC      = mp.mpf('3')                         # 色数
NF      = mp.mpf('5')                         # 活跃味数（MSbar 5 味）
G_N     = mp.mpf('6.67430e-11')               # 牛顿引力常数 [m³ kg⁻¹ s⁻²]
GM_SUN  = mp.mpf('1.3271244e20')              # 太阳引力参数（IAU 2015 名义值）[m³ s⁻²]
GM_EARTH= mp.mpf('3.986004418e14')            # 地球引力参数 [m³ s⁻²]
MP_MASS = mp.mpf('2.176434e-8')               # Planck 质量 [kg]
LP      = mp.mpf('1.616255e-35')              # Planck 长度 [m]
MPROT_MEV = mp.mpf('938.27208816')            # 质子质量 [MeV]
MU_Q    = mp.mpf('2.16')                      # u 夸克流质量 [MeV]（MSbar，PDG）
MD_Q    = mp.mpf('4.67')                      # d 夸克流质量 [MeV]（MSbar，PDG）
E_CHG   = mp.mpf('1.602176634e-19')           # 元电荷 [C]（SI 定义精确）
MPROT_KG= mp.mpf('1.67262192369e-27')         # 质子质量 [kg]
EPS0    = 1 / (MU0 * C ** 2)                  # 真空介电常数（由 μ0、c 定义导出）[F/m]

HERE = Path(__file__).resolve().parent


def guard(name, value, target, tol, level, info):
    """构造一道守卫记录；passed 由 |value-target|<=tol 实时判定。"""
    diff = mp.fabs(value - target)
    passed = bool(diff <= tol)
    return {
        "name": name,
        "value": mp.nstr(value, 20),
        "target": mp.nstr(target, 20),
        "diff": mp.nstr(diff, 12),
        "tol": mp.nstr(tol, 12),
        "passed": passed,
        "level": level,            # INFO=定义重排/零信息；PHYS=有经验内容
        "info": info,
    }


def main():
    guards = []

    # ---- F1 · Maxwell 波速（定义恒等，INFO 级）----
    # ε0 由 1/(μ0 c²) 定义导出 ⇒ μ0·ε0 = 1/c² ⇒ c_chk = 1/sqrt(μ0·ε0) = c 精确。
    c_chk = 1 / mp.sqrt(MU0 * EPS0)
    guards.append(guard("F1_c_wave_speed", c_chk, C, mp.mpf('1e-240'),
                       "INFO", "定义恒等式：residual=0，无新物理；仅验证量纲/定义自洽"))

    # ---- F2 · 树图 W 质量 m_W = m_Z·cosθ_W ----
    cos_tw = mp.sqrt(1 - SIN2TW)
    mW_tree = MZ * cos_tw
    guards.append(guard("F2_mW_tree", mW_tree, MW_MEAS, MW_MEAS * mp.mpf('0.01'),
                       "PHYS", "树图关系 m_W=m_Z·cosθ_W 在 1% 内复现测量值；残差 0.5% 归为圈图修正"))

    # ---- F3 · Higgs λ 与 vev 回代（定义自洽，INFO 级）----
    lambda_h = MH ** 2 / (2 * V_HIGGS ** 2)
    v_back = MH / mp.sqrt(2 * lambda_h)        # 代数上 ≡ V_HIGGS
    guards.append(guard("F3_vev_roundtrip", v_back, V_HIGGS, V_HIGGS * mp.mpf('1e-12'),
                       "INFO", "vev 回代精确闭合（代数恒等式）；物理内容为 λ_H≈0.1294"))
    # 单独记录 λ_H 数值（不进守卫判定，仅作机读事实）
    lambda_h_value = mp.nstr(lambda_h, 12)

    # ---- F4 · QCD β 函数括号（结构事实，PHYS 级）----
    bracket = (mp.mpf('11') / 3) * NC - (mp.mpf('2') / 3) * NF   # = 23/3 ≈ 7.6667
    guards.append(guard("F4_qcd_beta_bracket", bracket, mp.mpf('23') / 3, mp.mpf('1e-240'),
                       "PHYS", "括号=23/3≈7.67>0 ⇒ β<0 ⇒ 渐近自由（结构事实）"))

    # ---- F5 · Schwarzschild 半径（三体）----
    rs_sun = 2 * GM_SUN / C ** 2
    guards.append(guard("F5_rs_sun", rs_sun, mp.mpf('2953.3'), mp.mpf('1.0'),
                       "PHYS", "r_s(☉)≈2953 m（IAU 名义 GM☉）"))
    rs_earth = 2 * GM_EARTH / C ** 2
    guards.append(guard("F5_rs_earth", rs_earth, mp.mpf('8.87e-3'), mp.mpf('1e-4'),
                       "PHYS", "r_s(⊕)≈8.87 mm"))
    # F5c：r_s(m_P)=2ℓ_P 是定义恒等式（m_P≡√(ℏc/G)，ℓ_P≡√(ℏG/c³)）。
    # 用单一 ℏ 自洽构造 ⇒ 代数精确闭合；独立四舍五入的 CODATA 输入仅作交叉核对。
    HBAR = mp.mpf('1.054571817e-34')           # 约化 Planck 常数 [J·s]（CODATA 2022）
    lp_def = mp.sqrt(HBAR * G_N / C ** 3)       # ≡ ℓ_P（定义构造）
    mp_def = mp.sqrt(HBAR * C / G_N)            # ≡ m_P（定义构造）
    rs_planck = 2 * G_N * mp_def / C ** 2       # ≡ 2·lp_def（代数精确）
    ratio_planck = rs_planck / (2 * lp_def)
    # 交叉核对：独立 CODATA 四舍五入值（G_N、MP_MASS、LP）重建 ratio，偏差仅 ~1.4e-7，
    # 远小于 ~6 位有效数字的输入精度 ⇒ 无结构矛盾。
    codata_ratio = (2 * G_N * MP_MASS / C ** 2) / (2 * LP)
    guards.append(guard("F5_rs_planck", ratio_planck, mp.mpf('1'), mp.mpf('1e-230'),
                       "INFO",
                       "r_s(m_P)=2ℓ_P 精确（单一 ℏ 自洽构造，定义恒等式）；"
                       "独立 CODATA 重建 ratio=%s（1.4e-7，=输入精度噪声，非矛盾）" % mp.nstr(codata_ratio, 12)))

    # ---- F6 · 质子质量胶子占比（PHYS 级；方案依赖）----
    sigma_q = 2 * MU_Q + MD_Q                  # uud 价夸克流质量 [MeV]
    frac_gluon = 1 - sigma_q / MPROT_MEV
    guards.append(guard("F6_proton_gluon_frac", frac_gluon, mp.mpf('0.99'), mp.mpf('0.02'),
                       "PHYS", "胶子/迹反常贡献≈99%（MSbar 5 味 u,d 流质量方案；方案依赖 ±0.5%）"))

    # ---- F7 · 量纲/量级 sanity：两质子(r=1m)电磁/引力强度比 ----
    r = mp.mpf('1')
    Fe = E_CHG ** 2 / (4 * mp.pi * EPS0 * r ** 2)
    Fg = G_N * MPROT_KG ** 2 / r ** 2
    log_ratio = mp.log(Fe / Fg, 10)
    guards.append(guard("F7_log_Fe_over_Fg", log_ratio, mp.mpf('36.092'), mp.mpf('1e-2'),
                       "PHYS", "log10(F_e/F_g)|_{r=1m,pp}=36.092 → 量级 sanity 守卫，确认 SI 单位约定自洽"))

    # ---- 汇总 ----
    n_pass = sum(1 for g in guards if g["passed"])
    n_total = len(guards)
    exit_code = 0 if n_pass == n_total else 2

    result = {
        "doc": "修复版核心方程集 v2.0",
        "script": "68_fix_v2_numerics.py",
        "mpmath_dps": mp.mp.dps,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "constants_sources": {
            "C": "SI 定义精确", "MU0": "2019-SI 前定义精确",
            "ALPHA": "CODATA 2022 (1/137.035999084)", "SIN2TW": "on-shell 有效 0.23122",
            "MZ": "PDG 2024", "MW_MEAS": "PDG 2024 世界平均 80.3692 GeV",
            "V_HIGGS": "246.22 GeV", "MH": "PDG 2024 125.25 GeV",
            "G_N": "CODATA 2022 6.67430e-11", "GM_SUN": "IAU 2015 名义值",
            "GM_EARTH": "EGM96/IAU 名义值 3.986004418e14", "MP_MASS": "CODATA 2022",
            "LP": "CODATA 2022", "MPROT_MEV": "PDG 2024 938.27208816 MeV",
            "MU_Q/MD_Q": "MSbar 5 味 (PDG)", "E_CHG": "SI 定义精确",
            "MPROT_KG": "CODATA 2022 1.67262192369e-27 kg",
        },
        "lambda_H": lambda_h_value,
        "rs_planck_m": mp.nstr(rs_planck, 12),
        "codata_ratio_rs_planck": mp.nstr(codata_ratio, 12),
        "guards_total": n_total,
        "guards_passed": n_pass,
        "exit_code": exit_code,
        "guards": guards,
    }

    # ---- 落盘（同目录，机读证据）----
    out_json = HERE / "68_fix_v2_results.json"
    out_md = HERE / "68_fix_v2_results.md"
    out_txt = HERE / "68_fix_v2_report.txt"

    out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = ["# 修复版核心方程集 v2.0 —— 精算守卫结果", "",
             f"- 生成时间（UTC）：{result['generated_at']}",
             f"- mpmath 精度：{result['mpmath_dps']} 位",
             f"- 守卫：{n_pass}/{n_total} 通过，退出码 {exit_code}",
             f"- λ_H = {lambda_h_value}（由 m_H=125.25 GeV, v=246.22 GeV 机算）", ""]
    lines.append("| 守卫 | 级别 | 计算值 | 目标/容差 | 状态 |")
    lines.append("|---|---|---|---|---|")
    for g in guards:
        status = "PASS" if g["passed"] else "FAIL"
        lines.append(f"| {g['name']} | {g['level']} | {g['value']} | {g['target']} (±{g['tol']}) | {status} |")
    lines.append("")
    lines.append("## 说明")
    for g in guards:
        lines.append(f"- **{g['name']}**：{g['info']}")
    out_md.write_text("\n".join(lines), encoding="utf-8")

    with out_txt.open("w", encoding="utf-8") as f:
        f.write("修复版核心方程集 v2.0 精算守卫\n")
        f.write(f"mpmath dps={result['mpmath_dps']}  guards={n_pass}/{n_total}  exit={exit_code}\n\n")
        for g in guards:
            f.write(f"[{'PASS' if g['passed'] else 'FAIL'}] {g['name']:24s} "
                    f"val={g['value']:>22s} tgt={g['target']:>22s} "
                    f"diff={g['diff']:>14s} ({g['level']})\n")
        f.write(f"\nlambda_H = {lambda_h_value}\n")

    # ---- 终端摘要 ----
    print(f"修复版 v2.0 精算守卫：{n_pass}/{n_total} 通过，退出码 {exit_code}")
    for g in guards:
        print(f"  [{'PASS' if g['passed'] else 'FAIL'}] {g['name']:24s} = {g['value']:>20s}  ({g['level']})")
    print(f"  λ_H = {lambda_h_value}")
    print(f"  产物：{out_json.name} / {out_md.name} / {out_txt.name}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
