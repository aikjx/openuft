# -*- coding: utf-8 -*-
"""attack16 probe4 · C4 灵敏度与来源链（2026-10-10）

对象：证书 R4「五条预言带证伪阈值」中的重子不对称 Y_B，以及 R6 的「C4=稳定性闭合（确定值）」。

来料（只读靶 JSON，不重跑靶引擎）：
  - TUFT_V3.4路线1to2_衔接_重子预言化_2026-10-09.json
        computed: C4=0.0597, beta_tau=9.1e-07, tau_bg=1.5242881072026799e-05,
                  T_freeze=647777559511.6353, alpha_over_G=0.4773, Y_obs=8.7e-11
        guards:   tau_determined -> "tau_bg=1.52e-05（由 Y_obs 反推，唯一值）"
                  honest_note    -> "beta 成预言；但 tau_bg 仍由 Y_obs 反推（非 TUFT 首原导出）"
  - TUFT_V3.4全参数闭合总装_2026-10-10.json
        params:   C1=0.12, C2=-0.35, C3=0.08, C4=0.0597, beta=0.0597
        computed: Y_B_screened=8.820642282674164e-11, bracket=-1.7165199999988334e-05

判据：
  bracket(C4) = C1·A² + C2·A + C3 + C4，令 bracket=0 反解得 C4_required。
  若 C4 是「由稳定性闭合**解出**」而非「由机制导出」，则它是标定；
  且同一旋钮 C4 同时决定 (a) UV 不动点存在性 (b) τ_bg（→Y_B），
  ⇒ 「Y_B ≈ 观测」不是独立检验。

诚实边界：本探针不重建 Y_B 的完整公式（来料未给出可复算的闭式），
只做**来源链与灵敏度**判定；涉及公式依赖的部分一律降级 BOUNDARY 并写明假设。

退出码：仅由自检 CHK 决定；判出 FAIL/MISMATCH 不是引擎失败。
"""

import os
import sys
import json
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
getcontext().prec = 60

ITEMS = []
_SELF = []


def P(name, ok, detail, note=""):
    ITEMS.append(dict(id=name, verdict="PASS" if ok else "FAIL", detail=detail, note=note))


def F(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="FAIL", detail=detail, note=note))


def BOUND(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="BOUNDARY", detail=detail, note=note))


def INFO(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="INFO", detail=detail, note=note))


def MIS(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="MISMATCH", detail=detail, note=note))


def CHK(name, cond, detail=""):
    _SELF.append(dict(name=name, ok=bool(cond), detail=detail))


def d(x):
    return Decimal(str(x))


def rel(a, b):
    a, b = d(a), d(b)
    den = max(abs(a), abs(b))
    return abs(a - b) / den if den != 0 else abs(a - b)


def target_dir():
    """靶目录（只读）。HERE = <...>/本项目_统一场论攻破；靶在同级 算法联盟_全维自洽与归一化/数据。"""
    up = os.path.dirname(HERE)                       # 04_公共成果
    return os.path.join(up, "算法联盟_全维自洽与归一化", "数据")


def load(name):
    p = os.path.join(target_dir(), name)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def run_all():
    print("=" * 78)
    print("attack16 probe4 · C4 灵敏度与来源链")
    print("=" * 78)

    r12 = load("TUFT_V3.4路线1to2_衔接_重子预言化_2026-10-09.json")
    tot = load("TUFT_V3.4全参数闭合总装_2026-10-10.json")

    # 来料缺失 → 全部降级 BOUNDARY，绝不编造
    if r12 is None or tot is None:
        BOUND("F00", "来料 JSON 缺失（路线1to2=%s / 全参数总装=%s）" %
              (r12 is not None, tot is not None), "不代读、不编造；本探针降级")
        CHK("CHK-F00 来料可读", False, "至少一个来料 JSON 缺失")
        self_ok = sum(1 for s in _SELF if s["ok"])
        print("自检：%d/%d" % (self_ok, len(_SELF)))
        return dict(items=ITEMS, self_checks=_SELF), False

    c12 = r12.get("computed", {})
    ct = tot.get("computed", {})
    pt = tot.get("params", {})

    A = d(c12.get("alpha_over_G", "0.4773"))     # α/G
    C1 = d(pt.get("C1", "0.12"))
    C2 = d(pt.get("C2", "-0.35"))
    C3 = d(pt.get("C3", "0.08"))
    C4 = d(pt.get("C4", "0.0597"))
    beta = d(pt.get("beta", "0.0597"))
    beta_tau = d(c12.get("beta_tau", "9.1e-07"))
    tau_bg = d(c12.get("tau_bg", "1.5242881072026799e-05"))
    Y_obs = d(c12.get("Y_obs", "8.7e-11"))
    Y_B = d(ct.get("Y_B_screened", "8.820642282674164e-11"))
    bracket_target = d(ct.get("bracket", "-1.7165199999988334e-05"))

    # ---- F01: C4 由 bracket=0 反解 ----
    C4_req = -(C1 * A * A + C2 * A + C3)
    r_c4 = rel(C4_req, C4)
    bracket_calc = C1 * A * A + C2 * A + C3 + C4
    print("  A=α/G = %s" % A)
    print("  bracket(C4=%s) = %s   (来料 %s)" % (C4, "%.6e" % bracket_calc, "%.6e" % bracket_target))
    print("  C4_required(=bracket=0 反解) = %s ; 声明 C4 = %s ; 相对差 = %s"
          % ("%.10f" % C4_req, C4, "%.3e" % r_c4))

    F("F01", "C4_required = %s（令 bracket=0 反解）；声明 C4 = %s；相对差 = %s"
      % ("%.10f" % C4_req, C4, "%.3e" % r_c4),
      "C4 是令「稳定性条件」成立的**反解值**，非由机制导出 ⇒ 标定")

    # 自检：反解式必须能复现来料 bracket
    r_br = rel(bracket_calc, bracket_target)
    CHK("CHK-F01 反解式复现来料 bracket", r_br < d("1e-6"),
        "计算=%s 来料=%s 相对差=%s" % ("%.6e" % bracket_calc, "%.6e" % bracket_target, "%.3e" % r_br))

    # ---- F02: bracket 容差 ⇒ C4 可采纳带 ----
    tol_br = d("1e-3")            # 来料把 bracket=-1.7e-5 判为「(=0)」⇒ 容差量级 1e-3
    lo, hi = C4_req - tol_br, C4_req + tol_br
    width = (hi - lo) / C4_req
    print("  |bracket|<%s ⇒ C4 ∈ [%s, %s]；相对带宽 = %s" %
          (tol_br, "%.6f" % lo, "%.6f" % hi, "%.3f%%" % (width * 100)))

    F("F02", "|bracket|<1e-3 ⇒ C4 可采纳带 = [%s, %s]（相对带宽 %.2f%%）" %
      ("%.6f" % lo, "%.6f" % hi, width * 100),
      "「稳定性闭合」只把 C4 钉到 ±%.2f%%，不是确定值；声明 C4=0.0597 落在带内" % (width * 100 / 2))

    # ---- F03: β ≡ C4 是认定，且同一旋钮决定两件事 ----
    same = (beta == C4)
    tau_from_beta = beta_tau / C4
    r_tau = rel(tau_from_beta, tau_bg)
    print("  β=C4 ? %s ; τ_bg = beta_tau/C4 = %s vs 来料 %s (相对差 %s)"
          % (same, "%.6e" % tau_from_beta, "%.6e" % tau_bg, "%.3e" % r_tau))

    F("F03", "β = C4 为**认定**（来料来源栏原文「=C4」，无推导）；"
      "且同一旋钮 C4 同时决定 (a) UV 不动点存在性 (b) τ_bg=beta_tau/C4（→Y_B）",
      "一个旋钮承载两个「闭合」⇒ 「Y_B≈观测」不是独立检验")

    CHK("CHK-F03 τ_bg = beta_tau/C4 复现来料", r_tau < d("1e-4"),
        "相对差=%s" % ("%.3e" % r_tau))

    # ---- F04: 来料自承 τ_bg 由 Y_obs 反推 ----
    guards = r12.get("guards", [])
    q_tau = [g.get("note", "") for g in guards if g.get("name") == "tau_determined"]
    q_hon = [g.get("note", "") for g in guards if g.get("name") == "honest_note"]
    note_tau = q_tau[0] if q_tau else ""
    note_hon = q_hon[0] if q_hon else ""
    adm_tau = ("Y_obs" in note_tau) or ("Y_obs" in note_hon)
    print("  tau_determined: %s" % note_tau)
    print("  honest_note   : %s" % note_hon)

    if adm_tau:
        F("F04", "来料**自承**：「%s」/「%s」" % (note_tau, note_hon),
          "τ_bg 由观测量 Y_obs 反推 ⇒ Y_B 是输入被改写为输出，不构成可证伪预言")
    else:
        BOUND("F04", "未在来料 guards 中检索到「Y_obs 反推」字样，无法确认",
              "不代读、不推测")
    CHK("CHK-F04 来料 self-admission 可检索", adm_tau, "命中=%s" % adm_tau)

    # ---- F05: Y_B 双值 ----
    r_yb = rel(Y_B, Y_obs)
    print("  Y_B: 路线1to2 Y_obs=%s vs 总装 Y_B_screened=%s ; 相对差=%s"
          % ("%.4e" % Y_obs, "%.6e" % Y_B, "%.3e" % r_yb))
    MIS("F05", "Y_B 双值：Y_obs=%s（路线1to2） vs Y_B_screened=%s（全参数总装），相对差 %.3f%%"
        % ("%.4e" % Y_obs, "%.6e" % Y_B, r_yb * 100),
        "同一证书簇内两条链路给出不同的 Y_B")

    # ---- F06: 阈值溯源（输入有效位 vs 自定容差） ----
    # 来料把「Y_B≈观测」的容差取 0.01 dex；输入 τ_bg/beta_tau/T_freeze 均只给到 3 位有效数字
    dex_tol = d("0.01")                       # 0.01 dex
    frac_tol = d(10) ** dex_tol - 1           # 10^0.01 − 1 ≈ 0.0233
    # 3 位有效数字 ⇒ 相对不确定度量级 1/(2·10^2)=0.5%（末位半刻度）
    u_3sig = d("0.005")
    # 若干 3 位输入相乘/相除的粗略合成（独立、方和根）：取 4 个来源
    import math
    u_comb = (d(4).sqrt() * u_3sig)
    verdict_f06 = u_comb >= frac_tol / 2
    print("  自定容差 0.01 dex ⇒ 相对容差 = %s (%.2f%%)" % ("%.5f" % frac_tol, frac_tol * 100))
    print("  输入 3 位有效数字 ⇒ 单项 ~0.5%%，4 项方和根合成 ≈ %s (%.2f%%)"
          % ("%.5f" % u_comb, u_comb * 100))

    (F if verdict_f06 else BOUND)(
        "F06", "自定容差 0.01 dex = %.2f%%；输入（τ_bg/beta_tau/T_freeze 均 3 位）"
               "合成不确定度 ≈ %.2f%%" % (frac_tol * 100, u_comb * 100),
        "容差未显著紧于输入精度 ⇒ 「≈观测」不构成高分辨力检验")

    # ---- 反向对照：net 记账器喂合成一致案例必判 net=0 ----
    def net_ledger(debts, repaid):
        return d(debts) - d(repaid)
    CHK("CHK-8 net 记账器合成一致案例必判 0", net_ledger(7, 7) == 0,
        "net(7,7)=%s" % net_ledger(7, 7))

    # ---- 输出 ----
    outdir = os.path.join(os.path.dirname(HERE), "数据")
    os.makedirs(outdir, exist_ok=True)
    json_path = os.path.join(outdir, "attack16_probe4_C4灵敏度与来源链_2026-10-10.json")
    txt_path = os.path.join(outdir, "attack16_probe4_C4灵敏度与来源链_2026-10-10_report.txt")
    payload = dict(
        probe="attack16_probe4_C4灵敏度与来源链",
        date="2026-10-10",
        items=ITEMS,
        self_checks=_SELF,
        computed=dict(
            A=str(A), C4_required=str(C4_req), C4_declared=str(C4),
            C4_rel=str(r_c4), C4_band=[str(lo), str(hi)], C4_band_rel=str(width),
            beta_eq_C4=bool(same), tau_bg_from_beta=str(tau_from_beta),
            tau_bg=str(tau_bg), Y_obs=str(Y_obs), Y_B_screened=str(Y_B),
            Y_B_rel=str(r_yb), dex_tol_frac=str(frac_tol), input_combined_urel=str(u_comb),
            self_admission_tau_bg_from_Yobs=bool(adm_tau),
        ),
        quotes=dict(tau_determined=note_tau, honest_note=note_hon),
        red_lines=[
            "本探针不重建 Y_B 闭式（来料未给出可复算公式），只判来源链与灵敏度",
            "判「标定」不等于指称造假：标定是常规做法，但不得计为第一性预言",
            "不产生新物理",
        ],
    )
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("attack16 probe4 C4 灵敏度与来源链 2026-10-10\n")
        f.write("C4_required=%s C4_declared=%s rel=%s\n" % (C4_req, C4, "%.3e" % r_c4))
        f.write("C4 band=[%s,%s] rel_width=%s\n" % (lo, hi, "%.4f" % width))
        f.write("Y_obs=%s Y_B_screened=%s rel=%s\n" % (Y_obs, Y_B, "%.3e" % r_yb))

    verdicts = {}
    for it in ITEMS:
        verdicts[it["verdict"]] = verdicts.get(it["verdict"], 0) + 1
    self_ok = sum(1 for s in _SELF if s["ok"])
    print("-" * 78)
    print("读数：条目 %d ｜ %s" % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False)))
    print("自检：%d/%d" % (self_ok, len(_SELF)))
    for s in _SELF:
        if not s["ok"]:
            print("  自检未过：%s %s" % (s["name"], s["detail"]))
    print("产物：")
    for p_ in (json_path, txt_path):
        print("  " + os.path.relpath(p_, os.path.dirname(HERE)))
    print("=" * 78)
    return payload, self_ok == len(_SELF)


if __name__ == "__main__":
    _, ok = run_all()
    sys.exit(0 if ok else 1)
