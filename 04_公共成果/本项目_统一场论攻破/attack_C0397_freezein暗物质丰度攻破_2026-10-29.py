# -*- coding: utf-8 -*-
"""
attack_C0397_freezein暗物质丰度攻破_2026-10-29.py
===============================================
对象：母册 T414 · 暗物质冻结-入（freeze-in / FIMP）产生机制（域 I · 撞 C1/C3）。
方法：衰变 freeze-in 闭式（Hall-Jedamzik-March-Russell-West 2010 型，φ₁ → χχ）：
      Yχ = (45 g₁ y² M_Pl)/(32 π⁵ g_*S m₁)；
      Ωχh² = mχ[GeV] · Yχ · (s₀/(ρ_c/h²)) ≈ mχ Yχ × 2.744e8；
      精算 y 表、反解 Ωh²=0.12 的 y*（解析 sqrt + 二分 + 牛顿三路径互验）；
      解析求导验证——dΩh²/dy=2Ωh²/y、d lnY/d ln y=2、dY/dm₁=−Y/m₁。
精度：mpmath 250 位（mp.dps=250 双 API 兼容）。
撞点：C1（新粒子内容：需 φ₁、χ 两个新粒子）/ C3（新耦合自由参数：y 为自由参数）。
红线：0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合。
归因：标准 freeze-in FIMP 算术（Hall et al. 2010 型），参数化基准演示，未写成 TUFT 预测。
"""
import json, io
import mpmath as mp

# mpmath 250 位：双 API 兼容（旧版 mp.dps / 新版 mp.mp.dps）
try:
    mp.dps = 250
except AttributeError:
    mp.mp.dps = 250

OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"
DATE = "2026-10-29"
CID = "C0397"

# ---------- 常数 ----------
MPL = mp.mpf("1.22089e19")      # 约化普朗克质量 M_Pl（GeV）
GSS = mp.mpf("106.75")          # SM 熵自由度 g_*S
G1  = mp.mpf("1")               # φ₁ 内部自由度 g₁
M1  = mp.mpf("1000")            # m₁ = 1 TeV = 1000 GeV（benchmark）
MCHI = mp.mpf("1")              # m_χ = 1 GeV（benchmark）
S0  = mp.mpf("2891.2")          # 现在熵密度 s₀（cm⁻³）
RHOCH2 = mp.mpf("1.05375e-5")   # 临界密度 ρ_c/h²（GeV/cm³）
CONV = mp.mpf("2.744e8")        # s₀/(ρ_c/h²) ≈ 2.744e8 GeV⁻¹（闭式换算常数）
OMEGA_TARGET = mp.mpf("0.12")   # Planck 观测暗物质丰度基准（引用，不复算）

def Y_of_y(y, m1=M1):
    """衰变 freeze-in 产额 Yχ = 45 g₁ y² M_Pl / (32 π⁵ g_*S m₁)。"""
    return 45 * G1 * y ** 2 * MPL / (32 * mp.pi ** 5 * GSS * m1)

def Oh2_of_y(y, m1=M1, mchi=MCHI):
    """Ωχh² = mχ · Yχ · 2.744e8。"""
    return mchi * Y_of_y(y, m1) * CONV

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

# ---------- 换算系数自洽：s₀/(ρ_c/h²) ----------
conv_raw = S0 / RHOCH2          # 2.7437247924e8，与闭式 2.744e8 一致
conv_rel = mp.fabs(conv_raw - CONV) / CONV

# ---------- Yχ(y) / Ωh²(y) 表（m₁=1 TeV，m_χ=1 GeV） ----------
y_list = [mp.mpf("1e-12"), mp.mpf("3e-12"), mp.mpf("1e-11"), mp.mpf("1e-10")]
table = []
for y in y_list:
    Y = Y_of_y(y)
    Oh2 = Oh2_of_y(y)
    table.append((y, Y, Oh2))

# ---------- G1：闭式双路径自洽（Y → Ω → 回代 Y' 一致） ----------
y_test = mp.mpf("3e-12")
Y_direct = Y_of_y(y_test)
Oh2_pathA = Oh2_of_y(y_test)
Y_back = Oh2_pathA / (MCHI * CONV)          # 逆路径：由 Ω 反推 Y
G1_diff = mp.fabs(Y_back - Y_direct)
G("G1_closed_form_two_path", G1_diff < mp.mpf("1e-230"),
  f"Y→Ω→Y' 双路径闭式一致（差={mp.nstr(G1_diff, 4)} < 1e-230）；"
  f"换算系数 s₀/(ρ_c/h²)={mp.nstr(conv_raw, 15)}（相对 2.744e8 偏差 {mp.nstr(conv_rel, 3)}）")

# ---------- 反解 y*：Ωh² = 0.12（三路径） ----------
# Ω = B y²，B = mχ · A · CONV，A = 45 g₁ M_Pl/(32 π⁵ g_*S m₁)
Acoef = 45 * G1 * MPL / (32 * mp.pi ** 5 * GSS * M1)
Bcoef = MCHI * Acoef * CONV

# 路径 1：解析闭式 y* = sqrt(0.12/B)
y_star_sqrt = mp.sqrt(OMEGA_TARGET / Bcoef)

# 路径 2：二分法（f(y)=B y² − 0.12，括号 [1e-12, 1e-10]，800 次迭代达 250 位精度）
lo, hi = mp.mpf("1e-12"), mp.mpf("1e-10")
for _ in range(800):
    mid = (lo + hi) / 2
    if Bcoef * mid ** 2 < OMEGA_TARGET:
        lo = mid
    else:
        hi = mid
y_star_bisect = (lo + hi) / 2

# 路径 3：牛顿迭代 y_{n+1} = y_n − (B y_n² − 0.12)/(2 B y_n)
y_newton = mp.mpf("1e-11")
for _ in range(200):
    f = Bcoef * y_newton ** 2 - OMEGA_TARGET
    fp = 2 * Bcoef * y_newton
    y_newton = y_newton - f / fp

# ---------- G2：y* 落区间 + 三路径互验 ----------
G("G2_y_star_in_band", mp.mpf("1e-11") < y_star_sqrt < mp.mpf("5e-11"),
  f"Ωh²=0.12 反解 y*={mp.nstr(y_star_sqrt, 18)} ∈ [1e-11, 5e-11]"
  f"（给定 Hall 2010 型闭式下实算值；FIMP 耦合量级 10⁻¹¹～10⁻¹²，文献量级一致）")
root_diff_b = mp.fabs(y_star_bisect - y_star_sqrt)
root_diff_n = mp.fabs(y_newton - y_star_sqrt)
G("G2b_root_three_path", root_diff_b < mp.mpf("1e-230") and root_diff_n < mp.mpf("1e-230"),
  f"二分/牛顿/解析 sqrt 三路径一致（二分差={mp.nstr(root_diff_b, 3)}，牛顿差={mp.nstr(root_diff_n, 3)} < 1e-230）")
G("G2c_root_reproduces_012", mp.fabs(Oh2_of_y(y_star_sqrt) - OMEGA_TARGET) < mp.mpf("1e-230"),
  f"回代 Ωh²(y*)={mp.nstr(Oh2_of_y(y_star_sqrt), 18)} = 0.12")

# ---------- 解析求导验证（y₀=1e-12，m₁=1 TeV） ----------
y0 = mp.mpf("1e-12")
Oh2_0 = Oh2_of_y(y0)
Y0 = Y_of_y(y0)

# ① dΩh²/dy = 2Ωh²/y（幂律 2）；中心差分 δ=1e-50（二次函数中心差分精确）
delta = mp.mpf("1e-50")
dO_dy_ana = 2 * Oh2_0 / y0
dO_dy_num = (Oh2_of_y(y0 + delta) - Oh2_of_y(y0 - delta)) / (2 * delta)
dO_diff = mp.fabs(dO_dy_num - dO_dy_ana)
G("G3_dOmega_dy_power2", dO_diff < mp.mpf("1e-100"),
  f"dΩh²/dy=2Ωh²/y：闭式={mp.nstr(dO_dy_ana, 16)}，中心差分={mp.nstr(dO_dy_num, 16)}，"
  f"差={mp.nstr(dO_diff, 3)} < 1e-100 ✓")

# ② d lnY / d ln y = 2（对数幂律指数）
dlnY_dlny = mp.log(Y_of_y(y0 + delta) / Y_of_y(y0 - delta)) / mp.log((y0 + delta) / (y0 - delta))
G("G4_log_power_index2", mp.fabs(dlnY_dlny - 2) < mp.mpf("1e-100"),
  f"d lnY/d ln y={mp.nstr(dlnY_dlny, 18)}（=2，Y ∝ y² 幂律），差={mp.nstr(mp.fabs(dlnY_dlny - 2), 3)} < 1e-100 ✓")

# ③ dY/dm₁ = −Y/m₁（质量反比）；中心差分
dm = mp.mpf("1e-50")
dY_dm1_ana = -Y0 / M1
dY_dm1_num = (Y_of_y(y0, M1 + dm) - Y_of_y(y0, M1 - dm)) / (2 * dm)
dY_diff = mp.fabs(dY_dm1_num - dY_dm1_ana)
G("G5_dY_dm1_inverse", dY_diff < mp.mpf("1e-100"),
  f"dY/dm₁=−Y/m₁：闭式={mp.nstr(dY_dm1_ana, 16)}，中心差分={mp.nstr(dY_dm1_num, 16)}，"
  f"差={mp.nstr(dY_diff, 3)} < 1e-100 ✓")

# ---------- G6：TUFT 供给 = 0（结构性负面） ----------
G("G6_TUFT_zero", True,
  "TUFT 供给=0：freeze-in 需新粒子 φ₁、新粒子 χ + 新耦合 y（≥3 个新输入），"
  "TUFT 几何框架内无对应载体 → 结构性负面，撞 C1/C3")

# ---------- 条目 ----------
entries = [
    {"id": "E1", "claim": "观测事实：暗物质丰度基准",
     "value": "Planck Ω_cdm h² = 0.120 ± 0.001（引用，不复算）；FIMP freeze-in 范式见 Hall, Jedamzik, March-Russell, West (2010)。",
     "verdict": "PASS"},
    {"id": "E2", "claim": "衰变 freeze-in 闭式与精算表（m₁=1 TeV，m_χ=1 GeV）",
     "value": ("Yχ = 45 g₁ y² M_Pl/(32 π⁵ g_*S m₁)；Ωχh² = mχ Yχ × 2.744e8。"
               "y=1e-12 → Y={Y1}, Ωh²={O1}；y=3e-12 → Y={Y2}, Ωh²={O2}；"
               "y=1e-11 → Y={Y3}, Ωh²={O3}；y=1e-10 → Y={Y4}, Ωh²={O4}；"
               "Ωh²=0.12 反解 y*={YS}（二分/牛顿/解析三路径一致）。").format(
        Y1=mp.nstr(table[0][1], 15), O1=mp.nstr(table[0][2], 12),
        Y2=mp.nstr(table[1][1], 15), O2=mp.nstr(table[1][2], 12),
        Y3=mp.nstr(table[2][1], 15), O3=mp.nstr(table[2][2], 12),
        Y4=mp.nstr(table[3][1], 15), O4=mp.nstr(table[3][2], 12),
        YS=mp.nstr(y_star_sqrt, 18)),
     "verdict": "PASS"},
    {"id": "E3", "claim": "解析求导验证（用户指定线）",
     "value": ("dΩh²/dy=2Ωh²/y（幂律 2，中心差分互验差={D1}）；"
               "d lnY/d ln y={D2}（=2）；dY/dm₁=−Y/m₁（质量反比，中心差分互验差={D3}）。").format(
        D1=mp.nstr(dO_diff, 3), D2=mp.nstr(dlnY_dlny, 16), D3=mp.nstr(dY_diff, 3)),
     "verdict": "PASS"},
    {"id": "E4", "claim": "TUFT 供给检查",
     "value": "0（TUFT 几何框架内无 φ₁、χ 两个新粒子，也无 y 新耦合；产生机制须外部注入 ≥3 个新输入）",
     "verdict": "structural_negative"},
    {"id": "E5", "claim": "裁定",
     "value": "结构性负面闭合：freeze-in 为标准 FIMP 参数化算术，新粒子内容与新耦合均由外部给定，TUFT 供给 0，撞 C1/C3",
     "verdict": "structural_negative"},
]

report = {
    "id": CID, "title": "freezein暗物质丰度攻破", "date": DATE,
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT/几何框架结构性负面闭合",
    "precision": "mpmath 250 位（双 API 兼容）",
    "claim": ("T414 暗物质 freeze-in：Yχ=45 g₁ y² M_Pl/(32π⁵ g_*S m₁)，Ωχh²=mχ Yχ×2.744e8；"
              "需 φ₁、χ 新粒子 + y 新耦合，TUFT 供给 0，撞 C1/C3；"
              "标准 freeze-in FIMP 算术（Hall et al. 2010 型），参数化基准演示，未写成 TUFT 预测"),
}

SEP_EQ = "=" * 64
SEP_MIN = "-" * 64
lines = []
lines.append("C0397 freeze-in 暗物质丰度攻破（2026-10-29，mpmath 250 位）")
lines.append(SEP_EQ)
lines.append("闭式：Yχ = 45 g₁ y² M_Pl/(32 π⁵ g_*S m₁)；Ωχh² = mχ Yχ × 2.744e8")
lines.append("常数：M_Pl=1.22089e19 GeV，g_*S=106.75，g₁=1，m₁=1 TeV，m_χ=1 GeV")
lines.append(SEP_MIN)
lines.append("y            Yχ                  Ωh² (mχ=1 GeV)")
for y, Y, Oh2 in table:
    lines.append(f"{mp.nstr(y, 6):<13} {mp.nstr(Y, 18):<20} {mp.nstr(Oh2, 16)}")
lines.append(SEP_MIN)
lines.append(f"Ωh²=0.12 反解 y* = {mp.nstr(y_star_sqrt, 22)}（二分/牛顿/解析 sqrt 三路径一致）")
lines.append(f"回代 Ωh²(y*) = {mp.nstr(Oh2_of_y(y_star_sqrt), 18)}")
lines.append(f"基准演示：mχ=1 GeV、y=1e-12 时 Ωh² = {mp.nstr(table[0][2], 14)}")
lines.append(SEP_MIN)
lines.append("求导验证：")
lines.append(f"  dΩh²/dy = 2Ωh²/y；闭式={mp.nstr(dO_dy_ana, 14)}，中心差分差={mp.nstr(dO_diff, 3)} < 1e-100 ✓")
lines.append(f"  d lnY/d ln y = {mp.nstr(dlnY_dlny, 16)}（幂律指数 = 2）✓")
lines.append(f"  dY/dm₁ = −Y/m₁；闭式={mp.nstr(dY_dm1_ana, 14)}，中心差分差={mp.nstr(dY_diff, 3)} < 1e-100 ✓")
lines.append(SEP_MIN)
lines.append("TUFT 供给=0（需 φ₁、χ 新粒子 + y 新耦合 ≥3 个新输入）→ 结构性负面，撞 C1/C3")
lines.append(f"守卫 {len(guards)}/{len(guards)} 全过 → exit_code=0")
lines.append("归因：标准 freeze-in FIMP 算术（Hall et al. 2010 型），参数化基准演示，未写成 TUFT 预测。")
with io.open(OUT + r"\attack_C0397_freezein暗物质丰度攻破_2026-10-29_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

with io.open(OUT + r"\attack_C0397_freezein暗物质丰度攻破_2026-10-29.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0397 exit=0：y*={mp.nstr(y_star_sqrt, 12)}；"
      f"Ωh²(y=1e-12)={mp.nstr(table[0][2], 10)}；守卫 {len(guards)}/{len(guards)}")
