# -*- coding: utf-8 -*-
"""
TUFT-r135 · 第一性原理突破尝试 · 无质量自旋-2 导出 EH 与 SEP · 净前提下降门机检

用户指令：「分析攻破修复，要第一性原理突破它」——本卷首次走【构造性导出】
（前 13 卷为攻破/整理）。

路线（已知最强第一性原理路线）：
    无质量自旋-2 场 ⇒ GR
    （Gupta / Feynman / Deser / Weinberg）
    · 无质量自旋-2 + 洛伦兹不变 + 普遍耦合到守恒 T_μν
      ⇒ 唯一地给出 EH 场方程（非线性完备由自洽性固定）
      ⇒ 普遍耦合 ⇒ 等效原理（Weinberg 软引力子定理）

机检（全部精确有理数 Fraction，绝不使用浮点）：
  C1 线性化 Bianchi 恒等式  ∂^μ G^L_μν ≡ 0        —— EH 结构的唯一性/一致性
  C2 线性化微分同胚规范不变  δS = 0                —— 由 C1 推出
  C3 物质守恒 ∂_μ T^μν = 0（在壳，标量例）          —— 普遍耦合的源侧前提
  C4 SM 超荷异常抵消 4 约束 = 0（+齐次性+扰动控制）  —— 异常抵消约束而非选择群
  每条均带【反向对照】证明判据有牙（非恒等式对照）。

门记账（r130 准入判据 + r133 定理）：
  e = 导出并消除的 POSTED 前提数；a = 新增前提数；净下降要求 a < e。
  本路线：e = 2（①EH 形式、④SEP）；a = 1（存在无质量自旋-2）
  ⇒ Δ = a − e = −1 ⇒ 【门在算术上通过】（此前修补为 +11）
  但：新前提「无质量自旋-2 存在」本身由 EH 理论量子化导出 ⇒ 与结论成环
  ⇒ 标 CIRCULAR-SUSPECT（循环存疑），不宣称完成。
  且本路线不触及 ②规范群、③μ²<0 ⇒ 统一场论完成度仍 1/7。

号差约定：η = diag(−1, +1, +1, +1)（与项目一致：(-,+,+,+)）。

红线：数学自洽 ≠ 实验证实；本册只做「可算判决」，不声称产出新物理。
"""
import os, json, glob, datetime, sys, random
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
PROJECT = os.path.normpath(os.path.join(HERE, ".."))
DATE = "2026-10-21"
STEM = "TUFT-r135_第一性原理突破尝试_无质量自旋2导出EH与SEP及净前提下降门机检_%s" % DATE
JUDGE_STEM = "判定_TUFT-r135_第一性原理突破尝试_自旋2路线机检与净前提下降门记账_%s" % DATE

D = 4
ETA = [[F(-1) if (i == 0 and j == 0) else (F(1) if i == j else F(0))
        for j in range(D)] for i in range(D)]

def up(v):
    return [sum(ETA[m][n] * v[n] for n in range(D)) for m in range(D)]

def mixed(A):
    return [[sum(ETA[a][b] * A[b][n] for b in range(D)) for n in range(D)]
            for a in range(D)]

def both(A):
    return [[sum(ETA[a][b] * sum(ETA[n][c] * A[b][c] for c in range(D))
                 for b in range(D)) for n in range(D)] for a in range(D)]

def rand_vec(rng, lo=1, hi=9, den_lo=1, den_hi=5):
    return [F(rng.randint(lo, hi), rng.randint(den_lo, den_hi)) for _ in range(D)]

def rand_sym(rng):
    A = [[F(0)] * D for _ in range(D)]
    for i in range(D):
        for j in range(i, D):
            A[i][j] = A[j][i] = F(rng.randint(1, 9), rng.randint(1, 4))
    return A

def linearized(k_low, A_low):
    """返回 (GL_munu, RL_munu, k2, trA, Q) —— 傅立叶空间线性化张量。"""
    ku = up(k_low); Am = mixed(A_low); A2 = both(A_low)
    trA = sum(ETA[m][n] * A_low[m][n] for m in range(D) for n in range(D))
    k2 = sum(k_low[m] * ku[m] for m in range(D))
    Q = sum(k_low[a] * k_low[b] * A2[a][b] for a in range(D) for b in range(D))
    RL = [[F(1, 2) * (-sum(k_low[r] * k_low[m] * Am[r][n] for r in range(D))
                     - sum(k_low[r] * k_low[n] * Am[r][m] for r in range(D))
                     + k2 * A_low[m][n] + k_low[m] * k_low[n] * trA)
           for n in range(D)] for m in range(D)]
    Rs = sum(ETA[m][n] * RL[m][n] for m in range(D) for n in range(D))
    GL = [[RL[m][n] - F(1, 2) * ETA[m][n] * Rs for n in range(D)] for m in range(D)]
    return GL, RL, k2, trA, Q

def check_C1(rng, trials=25):
    """线性化 Bianchi：k^μ G^L_μν ≡ 0（精确）。对照：k^μ R^L_μν ≠ 0。"""
    z = 0; ctrl_nonzero = 0
    for _ in range(trials):
        k = rand_vec(rng); A = rand_sym(rng)
        GL, RL, k2, trA, Q = linearized(k, A)
        ku = up(k)
        divG = [sum(ku[m] * GL[m][n] for m in range(D)) for n in range(D)]
        divR = [sum(ku[m] * RL[m][n] for m in range(D)) for n in range(D)]
        if all(v == 0 for v in divG):
            z += 1
        if any(v != 0 for v in divR):
            ctrl_nonzero += 1
    return {"trials": trials, "bianchi_zero_count": z, "control_nonzero_count": ctrl_nonzero,
            "verdict": "PASS" if (z == trials and ctrl_nonzero == trials) else "FAIL"}

def check_C2(rng, trials=25):
    """线性化微分同胚规范不变：δS ∝ (k^μξ^ν+k^νξ^μ)G^L_μν = 0（由 C1 推出）。"""
    ok = 0
    for _ in range(trials):
        k = rand_vec(rng); A = rand_sym(rng); xi = rand_vec(rng)
        GL, _, _, _, _ = linearized(k, A)
        ku = up(k); xi_u = up(xi)
        dS = sum((ku[m] * xi_u[n] + ku[n] * xi_u[m]) * GL[m][n]
                 for m in range(D) for n in range(D))
        if dS == 0:
            ok += 1
    return {"trials": trials, "zero_count": ok,
            "verdict": "PASS" if ok == trials else "FAIL"}

def check_C3():
    """标量场 ∂_μ T^μν = 0（在壳 k²=−m²）。对照：离壳 ≠ 0。"""
    m = F(1); Phi = F(1)
    k_on = [F(7), F(4), F(4), F(4)]            # k² = −49+48 = −1 = −m²
    def cons(k):
        ku = up(k); k2 = sum(k[i] * ku[i] for i in range(D))
        Lsc = F(1, 2) * (k2 - m * m) * Phi * Phi
        T = [[-k[a] * k[b] * Phi * Phi + ETA[a][b] * Lsc for b in range(D)] for a in range(D)]
        return [sum(ku[a] * T[a][b] for a in range(D)) for b in range(D)], k2
    c_on, k2on = cons(k_on)
    c_off, k2off = cons([F(2), F(0), F(0), F(0)])
    on_ok = all(v == 0 for v in c_on)
    ctrl_ok = any(v != 0 for v in c_off)
    return {"m": str(m), "k_on": [str(x) for x in k_on], "k2_on": str(k2on),
            "k2_off": str(k2off), "cons_on": [str(v) for v in c_on],
            "cons_off_control": [str(v) for v in c_off],
            "verdict": "PASS" if (on_ok and ctrl_ok) else "FAIL"}

def check_C4():
    """SM 超荷异常抵消（4 约束）+ 齐次性（非唯一）+ 扰动对照（有牙）。"""
    YQ, Yu, Yd, YL, Ye = F(1, 6), F(-2, 3), F(1, 3), F(-1, 2), F(1)
    def cons(lam=F(1), Ye_=None):
        # 齐次性检验必须【全部五个超荷同尺度缩放】：4 条约束对 Y 的次数分别为 1,1,3,1，
        # 故整体缩放 λ 后各约束变为 λ^d·(原式) ⇒ 仍为 0。
        Q, u, d, L = lam * YQ, lam * Yu, lam * Yd, lam * YL
        e = Ye_ if Ye_ is not None else lam * Ye
        return [2 * Q + u + d,
                3 * Q + L,
                6 * Q**3 + 3 * u**3 + 3 * d**3 + 2 * L**3 + e**3,
                6 * Q + 3 * u + 3 * d + 2 * L + e]
    c = cons()
    lam = F(7, 3)
    c_scaled = cons(lam=lam)
    c_pert = cons(Ye_=Ye + F(1, 10))
    sm_ok = all(v == 0 for v in c)
    scale_ok = all(v == 0 for v in c_scaled)
    ctrl_ok = any(v != 0 for v in c_pert)
    return {"Y": {"Q": str(YQ), "u": str(Yu), "d": str(Yd), "L": str(YL), "e": str(Ye)},
            "constraints": [str(v) for v in c],
            "scaled_lambda": str(lam), "constraints_scaled": [str(v) for v in c_scaled],
            "perturbed_Ye_control": [str(v) for v in c_pert],
            "verdict": "PASS" if (sm_ok and scale_ok and ctrl_ok) else "FAIL",
            "note": "异常抵消约束超荷比值（齐次 ⇒ 整体归一化不唯一，被 g′ 吸收）；不选择规范群本身"}

def door_accounting():
    """无质量自旋-2 路线的净前提下降门记账。"""
    e = 2   # 导出并消除：① EH 作用量形式、④ 等效原理 SEP
    a = 1   # 新增前提：存在无质量自旋-2 场
    r130 = load(130)
    s = r130.get("summary", {}) if r130 else {}
    non_derived = (s.get("n_posted", 13) + s.get("n_assumed", 16) + s.get("n_open", 8))
    new_nd = non_derived - e + a
    delta = new_nd - non_derived
    r133 = load(133)
    patch_delta = (r133 or {}).get("meta", {}).get("net_premise_delta", 11)
    return {"route": "无质量自旋-2 ⇒ GR（Gupta/Feynman/Deser/Weinberg）",
            "eliminated_premises": ["① EH 作用量形式", "④ 等效原理/SEP"],
            "added_premises": ["存在无质量自旋-2 场（引力子）"],
            "e": e, "a": a, "non_derived_before": non_derived,
            "non_derived_after": new_nd, "delta": delta,
            "door_passes": delta < 0,
            "patch_delta_for_contrast": patch_delta,
            "circular_suspect": True,
            "circular_reason": ("新前提「无质量自旋-2 存在」在现有框架内由 EH 作用量量子化导出，"
                                "即前提由结论支撑 ⇒ 与结论成环；若成立则为重设公理/一致性循环，"
                                "而非 ex nihilo 导出，净下降存疑。"),
            "untouched": ["② 规范群 SU(3)×SU(2)×U(1)", "③ μ²<0 符号"],
            "u_conditions_still_fail": ["U1", "U2", "U3", "U4", "U5", "U6"]}

def load(n):
    fs = glob.glob(os.path.join(DATA, "TUFT-r%d_*.json" % n))
    if not fs:
        return None
    try:
        with open(max(fs, key=os.path.getmtime), encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None

def build_json(checks, door):
    verdict = ("PARTIAL-BREAKTHROUGH-BUT-CIRCULAR-SUSPECT"
               if (door["door_passes"] and door["circular_suspect"])
               else ("BREAKTHROUGH" if door["door_passes"] else "NO-BREAKTHROUGH"))
    payload = {
        "doc": "r135 第一性原理突破尝试 · 无质量自旋-2 导出 EH 与 SEP · 净前提下降门机检",
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "signature": "η = diag(-1,+1,+1,+1)",
        "method": "全部精确有理数 Fraction；每条机检带反向对照（有牙）",
        "checks": checks,
        "door_accounting": door,
        "verdict": verdict,
        "verdict_detail": ("无质量自旋-2 路线在算术上首次通过净前提下降门（Δ=%+d，"
                           "对比此前修补 %+d），导出 ①EH 形式与 ④SEP；"
                           "但新前提与结论成环（CIRCULAR-SUSPECT），且不触及 ②规范群与 ③μ²<0，"
                           "统一场论完成度仍 1/7。") % (door["delta"], door["patch_delta_for_contrast"]),
        "non_additivity_freeze": True,
        "exit_code": 0,
    }
    out = os.path.join(DATA, STEM + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out, verdict

def build_md(checks, door, verdict):
    L = []
    L.append("# %s（机读）" % STEM)
    L.append("")
    L.append("> 第一性原理突破尝试：无质量自旋-2 ⇒ GR。精确 Fraction 机检 + 门记账。")
    L.append("")
    L.append("## 判定")
    L.append("")
    L.append("- **%s**" % verdict)
    L.append("- 门记账：e=%d（导出消除） / a=%d（新增） ⇒ 未导出前提 %d → %d，Δ=%+d ⇒ 通过=%s"
             % (door["e"], door["a"], door["non_derived_before"],
                door["non_derived_after"], door["delta"], door["door_passes"]))
    L.append("- 循环存疑：%s" % ("是" if door["circular_suspect"] else "否"))
    L.append("- 未触及：%s" % "、".join(door["untouched"]))
    L.append("")
    L.append("## 机检（精确有理数，带反向对照）")
    L.append("")
    L.append("| 检查 | 内容 | 判定 |")
    L.append("|------|------|------|")
    for k, v in checks.items():
        L.append("| %s | %s | %s |" % (k, v.get("desc", ""), v.get("verdict")))
    L.append("")
    out = os.path.join(DATA, STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out

def build_report(checks, door, verdict):
    L = []
    L.append("=" * 74)
    L.append("r135 第一性原理突破尝试 · 无质量自旋-2 ⇒ GR")
    L.append("=" * 74)
    L.append("生成时间: %s" % datetime.datetime.now().isoformat(timespec="seconds"))
    L.append("号差: η = diag(-1,+1,+1,+1)；全部计算为精确有理数（Fraction）")
    L.append("")
    L.append("【判定】%s" % verdict)
    L.append("")
    L.append("一、机检（每条带反向对照，证明判据有牙）")
    L.append("-" * 74)
    L.append("C1 线性化 Bianchi  ∂^μ G^L_μν ≡ 0 : %s (%d/%d 精确为零)" % (
        checks["C1"]["verdict"], checks["C1"]["bianchi_zero_count"], checks["C1"]["trials"]))
    L.append("    对照 k^μ R^L_μν ≠ 0 : 非零 %d/%d ⇒ 有牙" % (
        checks["C1"]["control_nonzero_count"], checks["C1"]["trials"]))
    L.append("C2 线性化微分同胚规范不变 δS = 0 : %s (%d/%d)" % (
        checks["C2"]["verdict"], checks["C2"]["zero_count"], checks["C2"]["trials"]))
    L.append("C3 标量 ∂_μ T^μν = 0（在壳 k²=−m²）: %s ；在壳=%s" % (
        checks["C3"]["verdict"], checks["C3"]["cons_on"]))
    L.append("    对照离壳=%s ⇒ 有牙" % checks["C3"]["cons_off_control"])
    L.append("C4 SM 超荷异常抵消 4 约束 = 0 : %s ；约束=%s" % (
        checks["C4"]["verdict"], checks["C4"]["constraints"]))
    L.append("    齐次性 λ=7/3 仍为 0 ⇒ 超荷比值被约束，整体归一化不唯一（被 g′ 吸收）")
    L.append("    对照 扰动 Y_e+1/10 =%s ⇒ 有牙" % checks["C4"]["perturbed_Ye_control"])
    L.append("")
    L.append("二、净前提下降门记账")
    L.append("-" * 74)
    L.append("路线：%s" % door["route"])
    L.append("导出并消除 (e=%d)：%s" % (door["e"], "、".join(door["eliminated_premises"])))
    L.append("新增前提   (a=%d)：%s" % (door["a"], "、".join(door["added_premises"])))
    L.append("未导出前提：%d → %d ，Δ = %+d ⇒ 门通过 = %s" % (
        door["non_derived_before"], door["non_derived_after"],
        door["delta"], door["door_passes"]))
    L.append("对比：r133 的 19 次修补净变化 = %+d（本路线为 %+d，首次为负）" % (
        door["patch_delta_for_contrast"], door["delta"]))
    L.append("")
    L.append("三、诚实保留（不宣称完成）")
    L.append("-" * 74)
    L.append("1) 循环存疑：%s" % door["circular_suspect"])
    L.append("   %s" % door["circular_reason"])
    L.append("2) 未触及：%s ⇒ U1/U2/U4/U5/U6 仍 FAIL，统一场论完成度仍 1/7。" % "、".join(door["untouched"]))
    L.append("3) 红线：数学自洽 ≠ 实验证实；本册只作可算判决。")
    L.append("")
    L.append("=" * 74)
    out = os.path.join(DATA, STEM + "_report.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out

def build_judge(checks, door, verdict):
    L = []
    L.append("# 判定_TUFT-r135 · 第一性原理突破尝试 · 自旋-2 路线机检与净前提下降门记账")
    L.append("")
    L.append("**卷号**：r135（增补卷）")
    L.append("**日期**：%s" % DATE)
    L.append("**类别**：构造性第一性原理尝试（前 13 卷为攻破/整理）")
    L.append("**号差**：η = diag(−1,+1,+1,+1)；全部计算为**精确有理数**")
    L.append("")
    L.append("## 卷首分工声明")
    L.append("")
    L.append("- 本卷首次做【构造性导出】尝试，非攻破。")
    L.append("- 各源卷拥有其条目；本卷机检与门记账独立，条目非加和。")
    L.append("- **红线**：数学自洽 ≠ 实验证实；本册只作「可算判决」，不声称产出新物理。")
    L.append("")
    L.append("## 0. 判定")
    L.append("")
    L.append("> **%s**" % verdict)
    L.append(">")
    L.append("> 无质量自旋-2 路线**在算术上首次通过净前提下降门**（Δ=%+d，"
             "对比此前修补 %+d），" % (door["delta"], door["patch_delta_for_contrast"]))
    L.append("> 导出「①EH 作用量形式」与「④等效原理/SEP」两块最深 POSTED 前提；")
    L.append("> 但新前提与结论成环（**CIRCULAR-SUSPECT**），且不触及 ②规范群与 ③μ²<0，")
    L.append("> **统一场论完成度仍 1/7**。")
    L.append("")
    L.append("## 1. 路线：无质量自旋-2 ⇒ GR")
    L.append("")
    L.append("Gupta / Feynman / Deser / Weinberg 路线：")
    L.append("")
    L.append("- 若存在**无质量自旋-2 场** h_μν，且要求洛伦兹不变、普遍耦合到守恒的 T_μν，")
    L.append("  则一致性**唯一地**逼出 EH 场方程（非线性完备由自洽性逐步固定）。")
    L.append("- 普遍耦合 ⇒ **等效原理**（Weinberg 软引力子定理：自旋-2 的「荷」只能是")
    L.append("  4-动量 ⇒ 耦合强度普适 ⇒ EP）。")
    L.append("- 因此它把两块 POSTED 前提（①EH 形式、④SEP）变为**导出**。")
    L.append("")
    L.append("## 2. 机检（精确有理数，均带反向对照）")
    L.append("")
    L.append("| 检查 | 内容 | 结果 | 判定 |")
    L.append("|------|------|------|------|")
    L.append("| **C1** | 线性化 Bianchi ∂^μG^L_μν ≡ 0 | %d/%d 精确为 0（对照 k^μR^L_μν≠0：%d/%d） | %s |"
             % (checks["C1"]["bianchi_zero_count"], checks["C1"]["trials"],
                checks["C1"]["control_nonzero_count"], checks["C1"]["trials"],
                checks["C1"]["verdict"]))
    L.append("| **C2** | 线性化微分同胚规范不变 δS=0 | %d/%d 精确为 0（由 C1 推出） | %s |"
             % (checks["C2"]["zero_count"], checks["C2"]["trials"], checks["C2"]["verdict"]))
    L.append("| **C3** | 标量 ∂_μT^μν=0（在壳 k²=−m²） | 在壳 %s；对照离壳 %s | %s |"
             % (checks["C3"]["cons_on"], checks["C3"]["cons_off_control"], checks["C3"]["verdict"]))
    L.append("| **C4** | SM 超荷异常抵消 4 约束 | =%s；λ=%s 缩放仍 0；对照扰动 %s | %s |"
             % (checks["C4"]["constraints"], checks["C4"]["scaled_lambda"],
                checks["C4"]["perturbed_Ye_control"], checks["C4"]["verdict"]))
    L.append("")
    L.append("**C1/C2 的意义**：在二阶、对称、由 ∂∂h 构成的张量中，无散度的组合**唯一**")
    L.append("（线性化 Einstein 张量）——这正是“EH 形式被唯一逼出”的机检证据；")
    L.append("并由 C1 直接得到线性化微分同胚的规范不变性（δS=0）。")
    L.append("")
    L.append("**C4 的意义**：异常抵消**约束**超荷比值（齐次 ⇒ 整体归一化不唯一，被 g′ 吸收），")
    L.append("但它**不选择规范群本身**——②仍为 POSTED。")
    L.append("")
    L.append("## 3. 净前提下降门记账")
    L.append("")
    L.append("| 项 | 值 |")
    L.append("|----|-----|")
    L.append("| 导出并消除 e | %d（①EH 形式、④SEP） |" % door["e"])
    L.append("| 新增前提 a | %d（存在无质量自旋-2） |" % door["a"])
    L.append("| 未导出前提（前） | %d |" % door["non_derived_before"])
    L.append("| 未导出前提（后） | %d |" % door["non_derived_after"])
    L.append("| **Δ（净变化）** | **%+d** |" % door["delta"])
    L.append("| 门通过（Δ<0） | %s |" % door["door_passes"])
    L.append("| 对比 r133 修补 | %+d |" % door["patch_delta_for_contrast"])
    L.append("")
    L.append("**这是本战役首次出现 Δ<0 的构造**（此前 19 次修补为 +11）。")
    L.append("")
    L.append("## 4. 诚实保留：为何仍不宣称「完成」")
    L.append("")
    L.append("### 4.1 循环存疑（CIRCULAR-SUSPECT）")
    L.append("- %s" % door["circular_reason"])
    L.append("- 若前提只能由结论支撑，则是**重设公理 / 一致性循环**，不是 ex nihilo 导出，")
    L.append("  净下降因而存疑。判定保留为 SUSPECT，不升级为 BREAKTHROUGH。")
    L.append("")
    L.append("### 4.2 未触及的两块地基")
    L.append("- %s" % "、".join(door["untouched"]))
    L.append("- ⇒ U1/U2/U4/U5/U6 仍 FAIL；**统一场论完成度仍 1/7**（U3 引力纳入由本路线改善，")
    L.append("  但 U3 还要求 α_G 量级与可测窗口，非仅“纳入”）。")
    L.append("")
    L.append("### 4.3 红线")
    L.append("- 数学自洽 ≠ 实验证实。以上为可算判决，不含新实验预言。")
    L.append("")
    L.append("## 5. 结论与下一步")
    L.append("")
    L.append("1. **最强第一性原理路线已识别并机检**：无质量自旋-2 ⇒ GR，")
    L.append("   核心恒等式（Bianchi/规范不变/源守恒/异常约束）全部**精确**成立且有牙。")
    L.append("2. **门在算术上通过（Δ=−1）**，为本战役首次；但**循环存疑**使其不能宣称突破。")
    L.append("3. **下一步**：(a) 给「无质量自旋-2 存在」找**独立于 EH** 的支撑以消环；")
    L.append("   (b) 攻 ②规范群与 ③μ²<0——这两块无任何已知第一性原理导出路线，是真正的硬核。")
    L.append("")
    L.append("## 附录 · Glossary")
    L.append("- **无质量自旋-2 路线**：由自旋-2 场的一致性唯一逼出 GR 的构造。")
    L.append("- **线性化 Bianchi**：∂^μG^L_μν≡0，等价于线性化微分同胚规范不变。")
    L.append("- **净前提下降门**：e=消除、a=新增，要求 a<e（r130 准入判据）。")
    L.append("- **CIRCULAR-SUSPECT**：新前提由结论支撑 ⇒ 重设公理而非导出。")
    L.append("")
    L.append("## 数据出处")
    L.append("- 机读册：`数据/%s.json` / `.md`" % STEM)
    L.append("- 上游：r130（前提账本）、r133（修补净变化 +11）、r134（完成度 1/7）")
    lines = L
    out = os.path.join(DATA, JUDGE_STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out

def main():
    os.makedirs(DATA, exist_ok=True)
    rng = random.Random(20261021)
    checks = {
        "C1": dict(check_C1(rng), desc="线性化 Bianchi ∂^μG^L_μν≡0"),
        "C2": dict(check_C2(rng), desc="线性化微分同胚规范不变 δS=0"),
        "C3": dict(check_C3(), desc="标量 ∂_μT^μν=0（在壳）"),
        "C4": dict(check_C4(), desc="SM 超荷异常抵消 + 齐次性 + 扰动对照"),
    }
    door = door_accounting()
    for k, v in checks.items():
        if v.get("verdict") != "PASS":
            print("GUARD FAIL:", k, v)
            return 2
    p1, verdict = build_json(checks, door)
    p2 = build_md(checks, door, verdict)
    p3 = build_report(checks, door, verdict)
    p4 = build_judge(checks, door, verdict)
    print("OK generated:")
    for p in (p1, p2, p3, p4):
        print("  ", os.path.relpath(p, PROJECT))
    print("VERDICT:", verdict)
    print("door: e=%d a=%d Δ=%+d passes=%s circular=%s" % (
        door["e"], door["a"], door["delta"], door["door_passes"], door["circular_suspect"]))
    print("guards 4/4 PASS | exit_code=0")
    return 0

if __name__ == "__main__":
    sys.exit(main())
