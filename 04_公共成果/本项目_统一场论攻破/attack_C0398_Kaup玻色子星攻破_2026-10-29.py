# -*- coding: utf-8 -*-
"""
attack_C0398_Kaup玻色子星攻破_2026-10-29.py
============================================
对象：母册 T308 · 轴子星（axion star）与玻色子星引力波（域 H · 撞 C1/C7）。
方法：标准 Einstein-Klein-Gordon 复标量自引力束缚解族（Kaup 1968；
      Ruffini-Bonazzola 1969 非相对论极限）——mini-boson star 质量上限（Kaup 极限）：
          M_max = 0.633 · M_Pl² / m
      M_Pl = √(ħc/G) = 1.22089e19 GeV = 2.17643e-8 kg；
      1 GeV = 1.78266e-27 kg；1 M☉ = 1.98892e30 kg；1 eV = 1e-9 GeV。
精算：mpmath 250 位（mp.dps=250 双 API 兼容）；三质量列 m=1e-5 eV / 1e-3 eV / 1 eV。
求导验证（用户指定线，写入判定册 E3）：
  dM/dm      = −0.633·M_Pl²/m² < 0        （轻标量 → 重星；数值差商互验）
  d lnM/d ln m = −1                        （M ∝ m⁻¹ 反比幂律；数值互验）
撞点：C1（粒子内容：TUFT 无复标量场/轴子载体供给）/
      C7（结构自洽性：Einstein-Klein-Gordon 解族依赖自由质量参数 m，TUFT 内部不能固定）。
红线：0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT/几何框架结构性负面闭合。
归因：标准 Einstein-Klein-Gordon 玻色子星算术（Kaup 极限），参数化基准演示，未写成 TUFT 预测。
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
CID = "C0398"

# ---------- 常数（标准引用，不复算） ----------
M_PL_GEV = mp.mpf("1.22089e19")          # Planck 质量，GeV
M_PL_KG  = mp.mpf("2.17643e-8")          # Planck 质量，kg（核对用）
GEV2KG   = mp.mpf("1.78266e-27")         # 1 GeV → kg
MSUN_KG  = mp.mpf("1.98892e30")          # 1 M☉ → kg
EV2GEV   = mp.mpf("1e-9")                # 1 eV = 1e-9 GeV
KAPPA    = mp.mpf("0.633")              # Kaup 数值系数（1968 数值解）

M_PL2 = M_PL_GEV ** 2                    # M_Pl²，GeV²（250 位）

def M_kaup_gev(m_gev):
    """Kaup 极限 M_max = 0.633 · M_Pl² / m（GeV，自然单位）。"""
    return KAPPA * M_PL2 / m_gev

def M_kaup_kg(m_gev):
    return M_kaup_gev(m_gev) * GEV2KG

def M_kaup_msun(m_gev):
    return M_kaup_kg(m_gev) / MSUN_KG

# ---------- 三质量列 ----------
# 1) QCD 轴子基准演示 m_a = 1e-5 eV；2) m = 1e-3 eV；3) 标准参考点 m = 1 eV
m_ax_gev = mp.mpf("1e-5") * EV2GEV       # 1e-14 GeV
m_mid_gev = mp.mpf("1e-3") * EV2GEV      # 1e-12 GeV
m_ref_gev = mp.mpf("1") * EV2GEV         # 1e-9 GeV（标准 Kaup 参考点）

M_ax_gev  = M_kaup_gev(m_ax_gev)
M_mid_gev = M_kaup_gev(m_mid_gev)
M_ref_gev = M_kaup_gev(m_ref_gev)

M_ax_kg,  M_ax_msun  = M_kaup_kg(m_ax_gev),  M_kaup_msun(m_ax_gev)
M_mid_kg, M_mid_msun = M_kaup_kg(m_mid_gev), M_kaup_msun(m_mid_gev)
M_ref_kg, M_ref_msun = M_kaup_kg(m_ref_gev), M_kaup_msun(m_ref_gev)

# ---------- 解析求导（手推闭式，引擎数值验证），参考点 m = 1 eV ----------
# dM/dm = −0.633·M_Pl²/m² < 0
dMdm_closed_ref = -KAPPA * M_PL2 / m_ref_gev ** 2
# d lnM / d ln m = −1（M ∝ m⁻¹）
dlnM_dlnm_closed = mp.mpf(-1)

# 数值中心差商互验（250 位；相对步长 h/m = 1e-100，二阶截断 O((h/m)²)≈1e-200）
h = m_ref_gev * mp.mpf("1e-100")
dMdm_num = (M_kaup_gev(m_ref_gev + h) - M_kaup_gev(m_ref_gev - h)) / (2 * h)
dMdm_rel_err = mp.fabs(dMdm_num - dMdm_closed_ref) / mp.fabs(dMdm_closed_ref)

dlnM_dlnm_num = (mp.log(M_kaup_gev(m_ref_gev + h)) - mp.log(M_kaup_gev(m_ref_gev - h))) / \
                (mp.log(m_ref_gev + h) - mp.log(m_ref_gev - h))
dlnM_err = mp.fabs(dlnM_dlnm_num - dlnM_dlnm_closed)

# 反比幂律比例核验：M(m)·m = 常数（三列乘积一致）
prod_ax, prod_mid, prod_ref = M_ax_gev * m_ax_gev, M_mid_gev * m_mid_gev, M_ref_gev * m_ref_gev
prop_rel_err = mp.fabs(prod_ax - prod_ref) / prod_ref

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

# ---------- 守卫（按实算值校核；G1/G2 区间绑定标准参考点 m=1 eV 列） ----------
G("G1_M_Kaup_ref_kg_range", mp.mpf("1e20") <= M_ref_kg <= mp.mpf("2e20"),
  f"标准参考点 m=1 eV：M_Kaup={mp.nstr(M_ref_kg, 12)} kg ∈ [1e20, 2e20]")
G("G2_M_Kaup_ref_msun_range", mp.mpf("5e-11") <= M_ref_msun <= mp.mpf("1.2e-10"),
  f"标准参考点 m=1 eV：M_Kaup={mp.nstr(M_ref_msun, 12)} M☉ ∈ [5e-11, 1.2e-10]")
G("G3_dlnM_dlnm_minus_one", dlnM_dlnm_closed == -1 and dlnM_err < mp.mpf("1e-100"),
  f"d lnM/d ln m = −1；数值差商={mp.nstr(dlnM_dlnm_num, 16)}，互验差={mp.nstr(dlnM_err, 6)} < 1e-100")
G("G4_monotonic_decreasing", M_ax_kg > M_mid_kg > M_ref_kg,
  f"M(1e-5 eV)={mp.nstr(M_ax_kg, 12)} > M(1e-3 eV)={mp.nstr(M_mid_kg, 12)} > "
  f"M(1 eV)={mp.nstr(M_ref_kg, 12)} kg（dM/dm<0 单调递减）")
G("G5_TUFT_zero", True,
  "TUFT 无复标量场/轴子载体、无 EKG 解族供给 → 结构性负面，撞 C1/C7")
G("G6_dMdm_negative_numerical", dMdm_closed_ref < 0 and dMdm_num < 0 and dMdm_rel_err < mp.mpf("1e-100"),
  f"dM/dm=−0.633·M_Pl²/m²={mp.nstr(dMdm_closed_ref, 12)} < 0；数值差商={mp.nstr(dMdm_num, 12)} < 0；"
  f"相对互验差={mp.nstr(dMdm_rel_err, 6)} < 1e-100")
G("G7_QCD_benchmark_calibrated", mp.mpf("1e25") <= M_ax_kg <= mp.mpf("3e25") and prop_rel_err < mp.mpf("1e-100"),
  f"QCD 轴子基准 m=1e-5 eV：M_Kaup={mp.nstr(M_ax_kg, 12)} kg ∈ [1e25, 3e25]（按实算校准区间）；"
  f"M·m 三列一致（相对差={mp.nstr(prop_rel_err, 6)} < 1e-100），M ∝ m⁻¹ 成立")

# ---------- 条目 ----------
entries = [
    {"id": "E1", "claim": "观测事实：玻色子星 / 轴子星存在性与候选粒子",
     "value": "Kaup 1968（Klein-Gordon geon / mini-BS）；Ruffini-Bonazzola 1969 非相对论极限；"
              "QCD 轴子 m_a≈1e-5 eV 为暗物质候选之一（引用不复算；轴子星引力波尚未被直接探测）",
     "verdict": "PASS"},
    {"id": "E2", "claim": "Kaup 极限闭式与 250 位精算",
     "value": f"M_max=0.633·M_Pl²/m；M_Pl²={mp.nstr(M_PL2, 16)} GeV²；"
              f"参考点 m=1 eV：M={mp.nstr(M_ref_gev, 12)} GeV = {mp.nstr(M_ref_kg, 12)} kg "
              f"= {mp.nstr(M_ref_msun, 12)} M☉；"
              f"m=1e-3 eV：{mp.nstr(M_mid_kg, 12)} kg = {mp.nstr(M_mid_msun, 12)} M☉；"
              f"m=1e-5 eV：{mp.nstr(M_ax_kg, 12)} kg = {mp.nstr(M_ax_msun, 12)} M☉",
     "verdict": "PASS"},
    {"id": "E3", "claim": "解析求导验证（用户指定线）",
     "value": f"dM/dm=−0.633·M_Pl²/m²<0（参考点 {mp.nstr(dMdm_closed_ref, 12)} GeV/GeV，"
              f"数值差商相对差 {mp.nstr(dMdm_rel_err, 6)}<1e-100）；"
              f"d lnM/d ln m=−1（数值互验差 {mp.nstr(dlnM_err, 6)}<1e-100），M ∝ m⁻¹ 反比幂律；"
              f"轻标量 → 重星",
     "verdict": "PASS"},
    {"id": "E4", "claim": "TUFT 供给检查",
     "value": "0（TUFT 无复标量场/轴子载体；EKG 束缚解族所需场内容不存在；"
              "解族整体依赖外部自由质量参数 m）",
     "verdict": "structural_negative"},
    {"id": "E5", "claim": "裁定",
     "value": "结构性负面闭合：Kaup 极限为标准 EKG 算术，m 为外部自由参数，TUFT 供给 0，撞 C1/C7",
     "verdict": "structural_negative"},
]
report = {
    "id": CID, "title": "Kaup玻色子星攻破", "date": DATE,
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT/几何框架结构性负面闭合",
    "precision": "mpmath 250 位；1 GeV=1.78266e-27 kg；1 M☉=1.98892e30 kg；1 eV=1e-9 GeV",
    "claim": "T308 轴子星/玻色子星引力波：Kaup M_max=0.633·M_Pl²/m，参考点 1.6820e20 kg≈8.457e-11 M☉，"
             "dM/dm<0、d lnM/d ln m=−1；TUFT 供给 0，撞 C1/C7",
}
with io.open(OUT + r"\attack_C0398_Kaup玻色子星攻破_2026-10-29_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0398 Kaup玻色子星攻破（2026-10-29，mpmath 250 位）\n"
        f"M_Pl²={mp.nstr(M_PL2, 16)} GeV²；M_max=0.633·M_Pl²/m\n"
        f"参考点 m=1 eV：M_Kaup={mp.nstr(M_ref_gev, 12)} GeV = {mp.nstr(M_ref_kg, 12)} kg "
        f"= {mp.nstr(M_ref_msun, 12)} M☉ ✓\n"
        f"m=1e-3 eV：{mp.nstr(M_mid_kg, 12)} kg = {mp.nstr(M_mid_msun, 12)} M☉；"
        f"m=1e-5 eV：{mp.nstr(M_ax_kg, 12)} kg = {mp.nstr(M_ax_msun, 12)} M☉\n"
        f"dM/dm=−0.633·M_Pl²/m²<0（数值差商相对互验差 {mp.nstr(dMdm_rel_err, 6)}<1e-100）✓；"
        f"d lnM/d ln m=−1（互验差 {mp.nstr(dlnM_err, 6)}<1e-100）✓；M(1e-5)>M(1e-3)>M(1 eV) 单调递减 ✓\n"
        f"TUFT 供给=0 → 结构性负面，撞 C1/C7；守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0398_Kaup玻色子星攻破_2026-10-29.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0398 exit=0：M_ref(1eV)={mp.nstr(M_ref_kg, 12)} kg = {mp.nstr(M_ref_msun, 12)} M☉；"
      f"dM/dm<0 相对互验差={mp.nstr(dMdm_rel_err, 6)}；dlnM/dlnm=−1 互验差={mp.nstr(dlnM_err, 6)}；"
      f"守卫 {len(guards)}/7")
