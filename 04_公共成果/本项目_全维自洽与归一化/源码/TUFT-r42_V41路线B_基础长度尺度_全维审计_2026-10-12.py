# -*- coding: utf-8 -*-
"""
TUFT-V4.1 修复版（路线B）全套方程组 + 量纲审计 + CODATA 精算验证
=======================================================================
轮次：r42（2026-10-12）
来料：用户提供的《TUFT-V4.1 修复版（路线B）》完整提案
      （新增底层固有长度尺度 l0 公理，修正引力加速度场，解决上一轮
       发现的量纲缺失 L^2 致命缺陷）

审计方式：纯标准库 + mpmath（高精度 CODATA 精算）+ Fraction 三维量纲 (M,L,T)
         每一行量纲断言都机器验证，不手抄。

核心问题意识（承接 r39/r40 同日审计）：
  r40 裁定 G = 2*pi*c^3/(hbar*sin theta) 量纲缺 L^2，反解需 sin theta > 1（无实数解），
  且缺失的 L^2 恰为 l_P^2/(2*pi)，补回后 == l_P^2 = hbar*G/c^3 移项（零信息量）。
  路线B 的修复 = 显式引入新公理“基础固有长度 l0”，令 G_th = c^3*l0^2/(hbar*sin theta)。
  本册目标：① 机器验证该修复是否真的把所有方程量纲闭合；
            ② 诚实判定“CODATA 匹配”是推导还是构造；
            ③ 核查 r40 之后新增的 ADM-BSSN 演化方程自身是否量纲齐次。
=======================================================================
"""
import os, sys, json
import mpmath as mp
from fractions import Fraction

mp.mp.dps = 80

# ----------------------------------------------------------------------------
# 0. 路径
# ----------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)            # 04_公共成果/本项目_全维自洽与归一化
DATA_DIR = os.path.join(BASE, "数据")
os.makedirs(DATA_DIR, exist_ok=True)

# ----------------------------------------------------------------------------
# 1. 量纲系统 (M, L, T) 用 Fraction 三元组
# ----------------------------------------------------------------------------
def D(m, l, t):
    return (Fraction(m), Fraction(l), Fraction(t))

def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))

def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))

def deq(a, b):
    return (a[0] == b[0]) and (a[1] == b[1]) and (a[2] == b[2])

# 基本量量纲
DIM = {
    "c":      D(0, 1, -1),    # 光速
    "hbar":   D(1, 2, -1),    # 约化普朗克常数
    "l0":     D(0, 1, 0),     # 基础固有长度（路线B 新公理5）
    "kappa":  D(0, -1, 0),    # 3D 螺旋曲率
    "tau":    D(0, -1, 0),    # 3D 螺旋挠率
    "omega":  D(0, 0, -1),    # 螺旋本征角频率
    "theta":  D(0, 0, 0),     # 螺旋升角（无量纲）
    "G":      D(-1, 3, -2),   # 引力常数标准量纲
    "m":      D(1, 0, 0),     # 内禀质量
    "g":      D(0, 1, -2),    # 引力加速度场
    "rho":    D(1, -3, 0),    # 质量密度
    "eps":    D(1, -1, -2),   # 能量密度 = 能量/L^3
    "Gexp":   D(-1, 3, -2),   # CODATA 实验 G
}

# 派生量（用于演化方程）
DIM["c2"] = dmul(DIM["c"], DIM["c"])                       # L^2 T^-2
DIM["c3"] = dmul(DIM["c2"], DIM["c"])                      # L^3 T^-3
DIM["c4"] = dmul(DIM["c2"], DIM["c2"])                    # L^4 T^-4
DIM["l02"] = dmul(DIM["l0"], DIM["l0"])                   # L^2
DIM["k2"] = dmul(DIM["kappa"], DIM["kappa"])              # L^-2
DIM["Gc4"] = ddiv(DIM["G"], DIM["c4"])                    # M^-1 L^-1
DIM["Box"] = D(0, -2, 0)                                  # 协变达朗贝尔（4维）L^-2
DIM["Box_kappa"] = dmul(DIM["Box"], DIM["kappa"])         # L^-3
# 势 V = 1/2 (c^2(kappa^2+tau^2) - omega^2)^2
_D_bracket = dmul(DIM["c2"], DIM["k2"])                   # T^-2
DIM["V"] = dmul(_D_bracket, _D_bracket)                   # T^-4
DIM["dV_dkappa"] = ddiv(DIM["V"], DIM["kappa"])           # L T^-4
# 源项 S_kappa = (4*pi*G/c^4) * sin theta * eps
DIM["S_kappa"] = dmul(dmul(DIM["Gc4"], DIM["theta"]), DIM["eps"])  # L^-2
DIM["Pi_kappa"] = ddiv(DIM["kappa"], DIM["c"])            # L^-2  (= (1/alpha)*dt kappa, alpha~c)
DIM["alpha_lapse"] = DIM["c"]                             # 时移函数量纲 ~ c
DIM["beta_shift"] = DIM["c"]                             # 位移矢量量纲 ~ c

# ----------------------------------------------------------------------------
# 2. 方程条目（机器逐条量纲核对）
# ----------------------------------------------------------------------------
entries = []
def chk(eid, name, lhs, rhs, note=""):
    ok = deq(lhs, rhs)
    entries.append({
        "id": eid, "name": name,
        "verdict": "PASS" if ok else "FAIL",
        "lhs_dim": str(lhs), "rhs_dim": str(rhs), "note": note,
    })
    return ok

def note_item(eid, name, verdict, text):
    entries.append({"id": eid, "name": name, "verdict": verdict, "note": text})

# --- 一、基础几何恒等式 ---
chk("G01", "eq(1) kappa^2+tau^2 = omega^2/c^2",
    DIM["k2"],
    ddiv(dmul(DIM["omega"], DIM["omega"]), DIM["c2"]),
    "L^-2 = L^-2，自洽")
chk("G02", "eq(2) tau = kappa*cot(theta)",
    DIM["tau"], dmul(DIM["kappa"], DIM["theta"]),
    "L^-1 = L^-1 * 1")
chk("G03", "eq(3) omega = c*kappa*sin(theta)",
    DIM["omega"], dmul(dmul(DIM["c"], DIM["kappa"]), DIM["theta"]),
    "T^-1 = (L T^-1)(L^-1)")

# --- 二、本源质量 ---
chk("G04", "eq(4) m = hbar*omega/c^2",
    DIM["m"], ddiv(dmul(DIM["hbar"], DIM["omega"]), DIM["c2"]),
    "M = (M L^2 T^-1)(T^-1)/(L^2 T^-2)")
chk("G05", "eq(5) m = hbar*kappa*sin(theta)/c",
    DIM["m"], ddiv(dmul(dmul(DIM["hbar"], DIM["kappa"]), DIM["theta"]), DIM["c"]),
    "M = (M L^2 T^-1)(L^-1)/(L T^-1)")
chk("G06", "eq(6) kappa = m*c/(hbar*sin theta)",
    DIM["kappa"], ddiv(dmul(DIM["m"], DIM["c"]), dmul(DIM["hbar"], DIM["theta"])),
    "L^-1 = (M)(L T^-1)/((M L^2 T^-1))")

# --- 三、引力场公理修正 & G_th 推导（核心修复） ---
chk("G07", "eq(7) g = -c^2*l0^2*kappa*Rhat/R^2（L^2 修复点）",
    DIM["g"], dmul(dmul(dmul(DIM["c2"], DIM["l02"]), DIM["kappa"]), D(0, -2, 0)),
    "L T^-2 = (L^2 T^-2)(L^2)(L^-1)(L^-2)  -- 上一轮缺失的 L^2 在此补回")
chk("G08", "eq(8) G_th = c^3*l0^2/(hbar*sin theta)",
    DIM["G"], ddiv(dmul(DIM["c3"], DIM["l02"]), dmul(DIM["hbar"], DIM["theta"])),
    "M^-1 L^3 T^-2 = (L^3 T^-3)(L^2)/((M L^2 T^-1))")

# --- 四、高斯引力定理 ---
chk("G09", "eq(9) nabla.g = -4*pi*G_th*rho",
    dmul(D(0, -1, 0), DIM["g"]), dmul(DIM["G"], DIM["rho"]),
    "T^-2 = (M^-1 L^3 T^-2)(M L^-3)")

# --- 五、曲率-挠率耦合演化方程（ADM-BSSN 兼容）---
# 关键：左右两边是否同一量纲
chk("G10", "eq(10) Box*kappa = dV/dkappa + S_kappa  -- 左右量纲一致?",
    DIM["Box_kappa"], DIM["dV_dkappa"],
    "LHS=L^-3 ; RHS潜在项=L T^-4 -- 见 G11/G12")
# 单独核对各项维度
chk("G11", "eq(10) 项A: [Box*kappa] = L^-3",
    DIM["Box_kappa"], D(0, -3, 0), "独立核对")
chk("G12", "eq(10) 项B: [dV/dkappa] = L T^-4",
    DIM["dV_dkappa"], D(0, 1, -4), "独立核对")
chk("G13", "eq(10) 项C: [S_kappa] = L^-2",
    DIM["S_kappa"], D(0, -2, 0), "独立核对（来料自验项）")
# 显式判定三项不可相加
note_item("G14", "eq(10)/(11) 三向量纲互异 -> 非齐次",
    "FAIL",
    "Box*kappa=L^-3 ; dV/dkappa=L T^-4 ; S_kappa=L^-2，三者无共同量纲，"
    "演化方程（10）（11）作为微分方程不合法（与 r40 同类‘源项单点校验但 LHS 未比’缺陷复发）。"
    "dV/dkappa 与 LHS 相差 c^4 因子；S_kappa 与 LHS 相差 L^-1。")

# --- ADM-BSSN 一阶系统 ---
chk("G15", "ADM 运动学: dt*kappa = beta^k d_k kappa + alpha*Pi_kappa",
    dmul(D(0, 0, -1), DIM["kappa"]),
    dmul(DIM["beta_shift"], dmul(D(0, -1, 0), DIM["kappa"])),
    "T^-1 L^-1 = (L T^-1)(L^-2) -- 运动学 OK")
chk("G16", "ADM 动量: dt*Pi_kappa = ... - alpha*dV/dkappa - alpha*S_kappa",
    dmul(D(0, 0, -1), DIM["Pi_kappa"]),
    dmul(DIM["alpha_lapse"], DIM["dV_dkappa"]),
    "LHS=L^-2 T^-1 ; 右端 -alpha*dV/dkappa = L^2 T^-5，与 LHS 差 c^4 -- 继承 G14 失配")
note_item("G17", "ADM 动量方程整体量纲失配",
    "FAIL",
    "dt*Pi_kappa 量纲 L^-2 T^-1；右端 alpha*D2kappa=L^-2 T^-1 一致，"
    "但 alpha*dV/dkappa=L^2 T^-5、alpha*S_kappa=L^-1 T^-1 均不匹配，"
    "演化系统无法数值积分。")

# --- 六、挠率贡献（弱场退化）---
note_item("G18", "六、挠率贡献（弱场 tau<<kappa 退化牛顿）",
    "INFO",
    "tau=kappa*cot theta 与 eq(2) 一致；弱场 tau<<kappa 时退化为纯曲率引力。"
    "此为框架内自洽陈述，不产生新预言，标记 INFO。")

# --- 七、对标表“量纲全部严格自洽”声明 ---
note_item("G19", "七、对标表声明‘全部方程量纲严格自洽’",
    "FAIL",
    "声明与实际审计冲突：一~四节（G01-G09）确实闭合；"
    "但五节演化方程（10）（11）与 ADM 动量方程（G14/G17）量纲非齐次。"
    "‘全部方程量纲严格自洽’仅对静力学/弱场极限成立。")

# --- 八、下一步攻坚（登记，不判）---
note_item("G20", "八、下一步三选项",
    "INFO",
    "①g-2 一阶挠率修正 ②RK4/ADM-BSSN 静态球对称初值演化 ③引力波 TUFT 偏振修正。"
    "三项均依赖 G14/G17 先被修复方可执行。")

# ----------------------------------------------------------------------------
# 3. CODATA 精算（数值）
# ----------------------------------------------------------------------------
c = mp.mpf('299792458')
hbar = mp.mpf('1.0545718176461565e-34')
Gexp = mp.mpf('6.67430e-11')

lP = mp.sqrt(Gexp * hbar / c**3)                      # 路线B 取 sin theta=1 时 l0 = l_P
Gth_sin1 = c**3 * lP**2 / (hbar * mp.mpf('1'))       # G_th 当 l0=l_P, sin theta=1
rel_G = abs(Gth_sin1 - Gexp) / Gexp

# CODATA 标称普朗克长度（2018）
lP_nominal = mp.mpf('1.616255e-35')
rel_lP = abs(lP - lP_nominal) / lP_nominal

# 若 l0 为独立公理、要匹配 Gexp 对任意 sin theta 所需关系
# G_th = c^3 l0^2/(hbar sin theta) = Gexp  =>  l0^2 = Gexp*hbar*sin theta / c^3 = lP^2 * sin theta
# => l0 = l_P * sqrt(sin theta)
ratio_l0_over_lP = mp.mpf('1')  # sin theta = 1

numeric = {
    "c": str(c),
    "hbar": str(hbar),
    "Gexp": str(Gexp),
    "l_P_computed": str(lP),
    "l_P_CODATA_nominal": str(lP_nominal),
    "l_P_relative_error": mp.nstr(rel_lP, 6),
    "G_th_sin1": str(Gth_sin1),
    "Gexp": str(Gexp),
    "G_th_relative_error_vs_Gexp": mp.nstr(rel_G, 40),
    "l0_over_lP_for_universal_G": "l0 = l_P * sqrt(sin theta); sin theta=1 => l0=l_P",
    "note": ("G_th == G_exp 是构造性等式：令 l0=l_P 且 sin theta=1 时 "
             "G_th = c^3*l_P^2/hbar = c^3*(Gexp*hbar/c^3)/hbar = Gexp。"
             "这不是从 kappa,tau,omega,c,hbar 导出 G，而是用 G 定义 l0（或反之）。"),
}

# ----------------------------------------------------------------------------
# 4. 自检守卫（guard）-- 全部必须 True
# ----------------------------------------------------------------------------
guards = []
def guard(gid, cond, text):
    guards.append({"id": gid, "ok": bool(cond), "text": text})

guard("G1", deq(DIM["c"], D(0, 1, -1)), "c 量纲正确")
guard("G2", deq(DIM["hbar"], D(1, 2, -1)), "hbar 量纲正确")
guard("G3", deq(DIM["G"], D(-1, 3, -2)), "G 标准量纲正确")
guard("G4", deq(DIM["g"], D(0, 1, -2)), "g 加速度量纲正确")
guard("G5", deq(dmul(dmul(dmul(DIM["c2"], DIM["l02"]), DIM["kappa"]), D(0, -2, 0)), DIM["g"]),
      "eq(7) 量纲闭合（L^2 修复点）：c^2*l0^2*kappa*(1/R^2) = g = L T^-2")
guard("G6", deq(ddiv(dmul(DIM["c3"], DIM["l02"]), DIM["hbar"]), D(-1, 3, -2)),
      "eq(8) G_th 量纲闭合")
guard("G7", deq(DIM["Box_kappa"], D(0, -3, 0)), "Box*kappa = L^-3")
guard("G8", deq(DIM["dV_dkappa"], D(0, 1, -4)), "dV/dkappa = L T^-4")
guard("G9", deq(DIM["S_kappa"], D(0, -2, 0)), "S_kappa = L^-2")
guard("G10", (not deq(DIM["Box_kappa"], DIM["dV_dkappa"]))
      and (not deq(DIM["Box_kappa"], DIM["S_kappa"])),
      "演化方程三项量纲互异被正确检出（非齐次）")
guard("G11", rel_lP < mp.mpf('1e-3'), "l_P 精算与 CODATA 标称相差 < 1e-3")
guard("G12", rel_G < mp.mpf('1e-30'), "G_th(sin1,l0=lP) 与 Gexp 相对差 < 1e-30（构造性相等）")
guard("G13", deq(DIM["theta"], D(0, 0, 0)), "theta 无量纲")

guard_all_ok = all(g["ok"] for g in guards)

# ----------------------------------------------------------------------------
# 5. 汇总
# ----------------------------------------------------------------------------
def tally():
    t = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0, "CORRECTED": 0, "MISMATCH": 0}
    for e in entries:
        t[e["verdict"]] = t.get(e["verdict"], 0) + 1
    return t

T = tally()
exit_code = 0 if guard_all_ok else 1

summary = {
    "round": "r42",
    "title": "TUFT-V4.1 修复版（路线B）基础长度尺度 l0 全维审计",
    "date": "2026-10-12",
    "approach": "纯标准库 + mpmath + Fraction(M,L,T)",
    "tally": T,
    "guard_total": len(guards),
    "guard_pass": sum(1 for g in guards if g["ok"]),
    "exit_code": exit_code,
    "one_line": (
        "路线B 用新公理 l0 真实补回了上一轮缺失的 L^2（一~四节量纲全闭合、"
        "G_th 构造性等於 CODATA）；但五节演化方程(10)(11)与 ADM 动量方程仍量纲非齐次"
        "（LHS=L^-3，潜在项=L T^-4，源项=L^-2），且‘CODATA 匹配’是令 l0=l_P 的构造而非推导。"
    ),
}

# ----------------------------------------------------------------------------
# 6. 落盘（json / md / report.txt）
# ----------------------------------------------------------------------------
stem = "TUFT-r42_V41路线B_基础长度尺度_全维审计_2026-10-12"
out_json = os.path.join(DATA_DIR, stem + ".json")
out_md = os.path.join(DATA_DIR, stem + ".md")
out_txt = os.path.join(DATA_DIR, stem + "_report.txt")

payload = {
    "summary": summary,
    "entries": entries,
    "guards": guards,
    "numeric": numeric,
}
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

with open(out_md, "w", encoding="utf-8") as f:
    f.write("# %s\n\n" % stem)
    f.write("**轮次**：r42（2026-10-12）\n\n")
    f.write("## 一句话结论\n\n%s\n\n" % summary["one_line"])
    f.write("## 条目汇总 %s\n\n" % json.dumps(T, ensure_ascii=False))
    f.write("## 条目明细\n\n")
    for e in entries:
        f.write("- **%s** [%s] %s\n" % (e["id"], e["verdict"], e["name"]))
        if e.get("note"):
            f.write("  - %s\n" % e["note"])
        if e.get("lhs_dim"):
            f.write("  - lhs=%s rhs=%s\n" % (e["lhs_dim"], e["rhs_dim"]))
    f.write("\n## 自检守卫 %d/%d\n\n" % (summary["guard_pass"], summary["guard_total"]))
    for g in guards:
        f.write("- [%s] %s : %s\n" % ("OK" if g["ok"] else "FAIL", g["id"], g["text"]))
    f.write("\n## CODATA 精算\n\n")
    for k, v in numeric.items():
        f.write("- %s: %s\n" % (k, v))

with open(out_txt, "w", encoding="utf-8") as f:
    f.write("TUFT-r42 V4.1 routeB audit report\n")
    f.write("tally=%s guards=%d/%d exit=%d\n" % (
        json.dumps(T, ensure_ascii=False), summary["guard_pass"],
        summary["guard_total"], exit_code))
    f.write("one_line: %s\n" % summary["one_line"])
    for e in entries:
        f.write("[%s] %s %s\n" % (e["verdict"], e["id"], e["name"]))

# ----------------------------------------------------------------------------
# 7. 打印（ASCII，避免 GBK 截断）
# ----------------------------------------------------------------------------
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

print("=== TUFT-r42 V4.1 routeB audit ===")
print("tally=%s" % json.dumps(T, ensure_ascii=False))
print("guards=%d/%d exit=%d" % (summary["guard_pass"], summary["guard_total"], exit_code))
print("l_P=%.6e  l_P_err=%.3e" % (float(lP), float(rel_lP)))
print("G_th(sin1)=%.6e Gexp=%.6e rel=%.3e" % (float(Gth_sin1), float(Gexp), float(rel_G)))
print("one_line:", summary["one_line"])

sys.exit(exit_code)
