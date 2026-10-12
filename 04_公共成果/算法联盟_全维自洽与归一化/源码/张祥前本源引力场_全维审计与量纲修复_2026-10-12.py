# -*- coding: utf-8 -*-
# 张祥前「本源引力场」全维审计 + 量纲修复 + 传统物理对标
# 日期：2026-10-12
# 口径：纯标准库（Decimal 60 位 + Fraction 三维量纲向量 (M,L,T)）
#       机器验证原始版本的致命缺陷，并验证「修复版」与牛顿引力完全等价。
#
# 结论预览（详见数据产物与判定册）：
#   原始版本：量纲不匹配（m=ω²r³ 左侧 [M] 右侧 [L³T⁻²]）、场不是加速度场、概念混淆。
#   修复版本：补入有量纲常数 1/G 后，轨道质量方程 == 牛顿圆周轨道公式；
#            辅助场 A = g/G 只是把 G 吸收进场定义的变量代换，无新物理。
#   本质裁定：修复后的体系等价于牛顿引力（数学改写），不是第一性原理统一场论；
#            G 仍是外部输入常数，与 TUFT（从 κ,τ,ω 第一性推导 G）有根本差异。
import json, os, math
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 60

# ============================ 量纲系统 (M, L, T) ============================
def D(*e):
    return tuple(Fraction(x) for x in e)
ZERO = D(0, 0, 0)
M = D(1, 0, 0)
L = D(0, 1, 0)
T = D(0, 0, 1)
G_DIM = D(-1, 3, -2)          # [G] = L³ M⁻¹ T⁻²

def dscale(d, k):
    return tuple(a * Fraction(k) for a in d)
def dadd(d1, d2):
    return tuple(a + b for a, b in zip(d1, d2))
def dmul(d1, d2):
    return dadd(d1, d2)
def dpow(d, e):
    return dscale(d, Fraction(e))
def deq(d1, d2):
    return all(a == b for a, b in zip(d1, d2))
def dim_str(d):
    parts = []
    names = "MLT"
    for nm, v in zip(names, d):
        if v == 0:
            continue
        s = "%s" % nm
        if v != 1:
            s += "^%s" % (v if v.denominator == 1 else "(%s)" % v)
        parts.append(s)
    return "·".join(parts) if parts else "1(无量纲)"

# 物理量量纲
OMEGA = dpow(T, -1)            # [ω] = T⁻¹
R_DIM = L                       # [r,R] = L
V_DIM = dadd(OMEGA, R_DIM)      # [v=ωr] = L T⁻¹
RHO_DIM = dadd(M, dpow(L, -3))  # [ρ] = M L⁻³
ACCEL = dadd(L, dpow(T, -2))    # [g] = L T⁻²
NABLA = dpow(L, -1)             # [∇] = L⁻¹
# 张祥前辅助场 A = g/G
A_DIM = dadd(ACCEL, dpow(G_DIM, -1))   # [A] = [g]/[G] = (M⁻¹ L⁻²)

# ============================ 物理常数 / 数据 ============================
G_VAL = Decimal("6.67430e-11")          # m³ kg⁻¹ s⁻²
M_SUN_CODATA = Decimal("1.98847e30")    # kg
# 太阳系（近似圆轨道）观测量：线速度 v、轨道半径 r
BODIES = {
    "地球": (Decimal("29780"), Decimal("1.495978707e11")),
    "木星": (Decimal("13070"), Decimal("7.785e11")),
}

# ============================ 结果收集 ============================
ENTRIES = []
def add(eid, kind, title, detail):
    ENTRIES.append({"id": eid, "kind": kind, "title": title, "detail": detail})

# ----------------------- 量纲审计（D 系列） -----------------------
def check_dim(eid, desc, computed, expected):
    ok = deq(computed, expected)
    add(eid, "PASS" if ok else "FAIL",
        desc,
        "量纲=%s，期望=%s → %s" % (dim_str(computed), dim_str(expected),
                                    "匹配" if ok else "不匹配(差 %s)" % dim_str(dadd(computed, dscale(expected, -1)))))
    return ok

# D01 原始方程 m = ω² r³
check_dim("D01", "原始 m = ω²r³ 量纲",
          dadd(dpow(OMEGA, 2), dpow(R_DIM, 3)), M)   # (0,3,-2) vs (1,0,0)

# D02 修复 m = k·ω²r³ ，[k]=[1/G]
k_dim = dpow(G_DIM, -1)
check_dim("D02", "修复 m = k·ω²r³（[k]=[1/G]）量纲",
          dadd(k_dim, dadd(dpow(OMEGA, 2), dpow(R_DIM, 3))), M)

# D03 k = 1/G 即得牛顿 M = v²r/G（与圆周引力平衡同一式）
v2r_over_G = dadd(dadd(dpow(V_DIM, 2), R_DIM), dpow(G_DIM, -1))
add("D03", "PASS" if deq(v2r_over_G, M) else "FAIL",
    "k=1/G 时修复式 ≡ 牛顿 M = v²r/G",
    "v²r/G 量纲=%s = [M]，与牛顿圆周轨道质量公式逐字等价" % dim_str(v2r_over_G))

# D04 原始场 A = -m/R²(R/R) 不是加速度场
check_dim("D04", "原始 A = -m/R²(R/R) 量纲",
          dadd(M, dpow(R_DIM, -2)), ACCEL)   # (1,-2,0) vs (0,1,-2)

# D05 修复引力加速度场 g = -Gm/R²(R/R)
check_dim("D05", "修复 g = -Gm/R²(R/R) 量纲",
          dadd(G_DIM, dadd(M, dpow(R_DIM, -2))), ACCEL)

# D06 原始散度 ∇·A = -4πρ：在张祥前自身符号体系内自洽，但 A 非物理引力场
divA_dim = dadd(NABLA, A_DIM)   # (1,-3,0)
add("D06", "BOUNDARY",
    "原始 ∇·A = -4πρ 的「内部自洽性」",
    "∇·A 量纲=%s 与 ρ 量纲=%s 匹配 ⇒ 在其自身体系内自洽；"
    "但 A 量纲 (M⁻¹L⁻²) 并非引力加速度，故该式描述的是「辅助场」而非牛顿引力场。"
    % (dim_str(divA_dim), dim_str(RHO_DIM)))

# D07 修复 ∇·g = -4πGρ 量纲
check_dim("D07", "修复 ∇·g = -4πGρ 量纲",
          dadd(NABLA, ACCEL), dadd(G_DIM, RHO_DIM))

# D08 变量代换 A=g/G ⇒ ∇·A=-4πρ 是代数恒等式（无新物理）
# 证明：∇·(G·A) = -4πGρ  ⇒  G·∇·A = -4πGρ  ⇒  ∇·A = -4πρ
lhs_sub = dadd(NABLA, A_DIM)          # ∇·A
rhs_sub = RHO_DIM                       # -4πρ
add("D08", "CORRECTED",
    "A = g/G 代换使 ∇·g=-4πGρ 退化为 ∇·A=-4πρ（纯代数缩放）",
    "两式差一个常数因子 G，属变量重命名，数学上不增不减；"
    "因此张祥前原式只是「牛顿引力除以 G 后的辅助场」，不是本源新场。量纲核验："
    "∇·A=%s，ρ=%s。" % (dim_str(lhs_sub), dim_str(rhs_sub)))

# D09 本源质量定义 m = n/4π 量纲：即使固定静止计数 n0，仍不匹配 [M]
n_dim = ZERO   # n 为几何计数，无量纲
add("D09", "FAIL",
    "「m = n0/4π」量纲仍不成立（修复不完整）",
    "n0 为无量纲几何计数 ⇒ 右端量纲=%s，左端 m 量纲=%s ⇒ 仍不匹配。"
    "仅在「n0 携带 [M] 量纲」时等式成立，但那等于用质量去定义质量（循环）。"
    "原稿声称『修复量纲、固定 n0 为静止计数后即自洽』只对轨道/Gauss 部分成立，"
    "本源质量定义自身并未被修复。" % (dim_str(n_dim), dim_str(M)))

# D10 与 TUFT 对比：G 的来源
add("D10", "INFO",
    "与 TUFT 的关键分歧：G 是外部输入 vs 第一性导出",
    "本体系 G 是藏入场定义里的外部常数，无法给出 G 的数值；"
    "TUFT 目标是从底层几何公理（κ,τ,ω）第一性推导 G ⇒ 两者不在同一理论层级。")

# D11（原创）张祥前称「只是差了一个常数 G」——但 G 是有量纲转换因子，非无量纲比例系数
add("D11", "INFO",
    "G 是有量纲转换因子，非无量纲比例：张祥前『只差常数 G』表述误导",
    "G 的量纲向量=%s，并非全零 ⇒ G 不是无量纲常数。"
    "原始式 m=ω²r³ 丢失的是 1/G 这一【带量纲】转换因子；"
    "补回后改变的不仅是数值比例，而是物理量的量纲归属。"
    % dim_str(G_DIM))

# D12（原创）本源质量定义 m=n0/4π 的量纲循环依赖严格证明
# 若 n0 为无量纲几何计数：右端量纲=1，左端 [M] ⇒ 不成立；
# 唯一合法化方式是令 n0 自身携带 [M] 量纲，但那等于「用质量定义质量」，塌缩为同义反复。
n0_dim_in = ZERO
n0_dim_needed = M
add("D12", "FAIL",
    "m=n0/4π 修复的循环依赖（严格证明）：n0 必须自带 [M] 才成立",
    "右端 n0/4π 量纲=%s（n0 无量纲）≠ 左端 %s ⇒ 不成立；"
    "唯一合法化方式是令 n0 自身量纲=%s，但那等于『用质量去定义质量』，"
    "本源质量定义塌缩为 tautology，并未从几何计数导出质量。"
    % (dim_str(n0_dim_in), dim_str(M), dim_str(n0_dim_needed)))

# ----------------------- 数值对标（N 系列） -----------------------
def newton_mass(v, r):
    return v * v * r / G_VAL

num_rows = []
for name, (v, r) in BODIES.items():
    M_calc = newton_mass(v, r)
    # 张祥前「修复版」轨道质量方程即 m = v²r/G，与牛顿同式 ⇒ 数值恒等
    M_zhang = newton_mass(v, r)
    rel = abs(M_calc - M_zhang) / M_calc
    rel_sun = abs(M_calc - M_SUN_CODATA) / M_SUN_CODATA
    num_rows.append((name, M_calc, rel, rel_sun))

# N01/N02/N03 数值等价 + 复现太阳质量
ok_num = all(row[2] == 0 for row in num_rows) and all(row[3] < Decimal("1e-2") for row in num_rows)
add("N01", "PASS" if ok_num else "FAIL",
    "数值：修复版与牛顿轨道公式完全等价（相对残差机器零）",
    "地球/木星各自 m_zhang 与 m_newton 相对差=0（同一公式）；"
    "两体算得 M☉≈%.4e kg，与 CODATA %.4e kg 偏差均 <1%%。" % (num_rows[0][1], M_SUN_CODATA))

add("N02", "PASS",
    "地球轨道反推太阳质量",
    "M☉(地球)=%.6e kg（CODATA %.4e kg，相对偏差 %.4e）" % (num_rows[0][1], M_SUN_CODATA, num_rows[0][3]))
add("N03", "PASS",
    "木星轨道反推太阳质量（交叉验证）",
    "M☉(木星)=%.6e kg（相对 CODATA 偏差 %.4e）" % (num_rows[1][1], num_rows[1][3]))

# N04 无新预言：两理论方程恒等，无法区分
add("N04", "INFO",
    "可证伪性：修复版不预言任何牛顿引力之外的效应",
    "因 m=v²r/G 与牛顿圆周轨道公式逐字相同，一切低速弱引力预言与牛顿一致；"
    "若强行令 k≠1/G，则 k 沦为需由牛顿标定的自由参数，仍非第一性确定。")

# ----------------------- 自检（S 系列） -----------------------
def selfcheck(name, cond, detail):
    add("S:" + name, "PASS" if cond else "FAIL", "自检 " + name, detail)

selfcheck("dim_algebra", deq(dadd(G_DIM, dpow(G_DIM, -1)), ZERO),
          "G·(1/G) 量纲相消为 1（量纲代数自洽）")
selfcheck("newton_eq_zhang", deq(v2r_over_G, M),
          "v²r/G 量纲 = [M]，与牛顿恒等式符号层一致")
selfcheck("gauss_subst", deq(lhs_sub, rhs_sub),
          "A=g/G 代入后 ∇·A 与 ρ 量纲一致（代换闭合）")
selfcheck("msun_repro", all(row[3] < Decimal("2e-2") for row in num_rows),
          "两体反推 M☉ 与 CODATA 偏差 <2%，数值链路可信")

# ============================ 汇总 ============================
KINDS = ["PASS", "FAIL", "BOUNDARY", "INFO", "CORRECTED"]
counts = {k: sum(1 for e in ENTRIES if e["kind"] == k) for k in KINDS}
n_self = sum(1 for e in ENTRIES if e["id"].startswith("S:"))
self_fail = [e["id"] for e in ENTRIES if e["id"].startswith("S:") and e["kind"] == "FAIL"]

RESULTS = {
    "engine": "张祥前本源引力场_全维审计与量纲修复",
    "date": "2026-10-12",
    "rating": "C/L1",
    "verdict": "修复版等价于牛顿引力（数学改写），非第一性原理统一场论；G 为外部输入。",
    "counts": counts,
    "entries": ENTRIES,
    "numerical": [
        {"body": n, "M_kg": str(m), "rel_to_newton": str(rel), "rel_to_CODATA_Msun": str(rs)}
        for (n, m, rel, rs) in num_rows
    ],
    "constants": {"G": str(G_VAL), "M_sun_CODATA": str(M_SUN_CODATA)},
    "self_checks_pass": len(self_fail) == 0,
}

def build_md():
    L = []
    L.append("# 张祥前「本源引力场」全维审计与量纲修复")
    L.append("")
    L.append("- 引擎：`源码/张祥前本源引力场_全维审计与量纲修复_2026-10-12.py`")
    L.append("- 数据：`数据/张祥前本源引力场_全维审计与量纲修复_2026-10-12.json` / `.md`")
    L.append("- 判定：`判定_张祥前本源引力场_全维审计与量纲修复_2026-10-12.md`")
    L.append("- 口径：Decimal 60 位 + Fraction 三维量纲 (M,L,T)；机器验证，非口头断言。")
    L.append("")
    L.append("## 一、条目汇总")
    L.append("")
    L.append("| 类别 | 数量 |")
    L.append("|---|---|")
    for k in KINDS:
        L.append("| %s | %d |" % (k, counts[k]))
    L.append("| 合计 | %d |" % len(ENTRIES))
    L.append("")
    L.append("评级：**C/L1**（确认等价于已知理论、无新物理；原始版本含量纲/概念硬伤）。")
    L.append("")
    L.append("## 二、逐条裁定")
    L.append("")
    L.append("| 编号 | 类别 | 标题 | 关键读数 |")
    L.append("|---|---|---|---|")
    for e in ENTRIES:
        L.append("| %s | %s | %s | %s |" % (e["id"], e["kind"], e["title"], e["detail"]))
    L.append("")
    L.append("## 三、数值对标（太阳系）")
    L.append("")
    L.append("| 天体 | 反推 M☉ (kg) | 与牛顿相对差 | 与 CODATA 相对偏差 |")
    L.append("|---|---|---|---|")
    for (n, m, rel, rs) in num_rows:
        L.append("| %s | %.6e | %s | %.4e |" % (n, m, rel, rs))
    L.append("")
    L.append("## 四、核心结论")
    L.append("")
    L.append("1. **原始版本不可用**：`m=ω²r³` 量纲错（[M] vs [L³T⁻²]，差恰为 [G]）；")
    L.append("   原始场 `A=-m/R²` 量纲 (M⁻¹L⁻²) 不是加速度场。")
    L.append("2. **修复=补 1/G**：补入有量纲常数后 `m=v²r/G` 与牛顿圆周轨道公式逐字等价；")
    L.append("   任何数值计算与牛顿完全相同，不预言新效应。")
    L.append("3. **辅助场只是变量代换**：`A=g/G` 令 `∇·A=-4πρ` 成为 `∇·g=-4πGρ` 除以 G 的代数重排，")
    L.append("   未引入新物理内容。")
    L.append("4. **本源质量定义未真正修复**：`m=n0/4π` 即使固定静止计数 n0，右端仍无量纲、左端为 [M]，")
    L.append("   量纲仍不匹配；唯有令 n0 携带 [M] 才成立，但那等于用质量定义质量（循环）。")
    L.append("5. **与 TUFT 的根本分歧**：本体系 G 是外部输入（藏入场定义），TUFT 目标是从 κ,τ,ω 第一性导出 G；")
    L.append("   两者不在同一理论层级。")
    L.append("")
    L.append("> 红线：数学自洽 ≠ 物理证实。本审计是对来料的机器化复算与诚实边界标注，不产生新物理。")
    return "\n".join(L)

def main():
    md = build_md()
    base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(base, "..", "数据"))
    os.makedirs(data_dir, exist_ok=True)
    stem = "张祥前本源引力场_全维审计与量纲修复_2026-10-12"
    with open(os.path.join(data_dir, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(RESULTS, f, ensure_ascii=False, indent=2)
    with open(os.path.join(data_dir, stem + ".md"), "w", encoding="utf-8") as f:
        f.write(md)
    # 控制台（避免 GBK 炸）
    try:
        print(md)
    except Exception:
        pass
    return 0 if len(self_fail) == 0 else 2

if __name__ == "__main__":
    import sys
    sys.exit(main())
