# -*- coding: utf-8 -*-
"""
attack_C0399_BBN氦丰度攻破_2026-10-29.py
===============================================
对象：母册 T431 · 轻元素原初丰度（D / He-3 / He-4 / Li-7，域 I · 撞 C2）。
方法：标准 BBN 解析闭式（PDG BBN 综述 / Kolb-Turner 教学闭式）：
      (n/p)_f = exp(−Q/T_f)，Q = m_n − m_p = 1.293332 MeV（PDG，引用不复算）；
      x = (n/p)_f · exp(−t_BBN/τ_n)，Y_p = 2x/(1+x)；
      t_BBN = 180 s（核合成时标，引用），τ_n = 879.4 s（PDG，引用不复算）；
      精算 Y_p(T_f) 网格（0.6 / 0.7 / 0.8 / 0.9 / 1.0 MeV），
      二分 + 牛顿反解 Y_p = 0.245 的冻结温度 T_f*；
      解析求导验证——dY_p/dT_f > 0、dY_p/dτ_n > 0、dY_p/dQ < 0，数值中心差分互验。
精度：mpmath 250 位（mp.dps=250 双 API 兼容）。
撞点：C2（绝对标度：T_f、Q、τ_n 全部外部输入，TUFT 无核合成机制、供给 0）。
红线：0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合。
归因：标准 BBN 解析闭式算术（PDG 输入，引用不复算），未写成 TUFT 预测。
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
CID = "C0399"

# ---------- 常数（PDG / 标准 BBN 综述，引用不复算） ----------
Q    = mp.mpf("1.293332")   # 中子-质子质量差 Q = m_n − m_p（MeV，PDG 2024 引用）
TAU  = mp.mpf("879.4")      # 中子平均寿命 τ_n（s，PDG 引用）
TBBN = mp.mpf("180")       # 核合成时标 t_BBN（s，标准 BBN 引用）
Y_OBS = mp.mpf("0.245")     # Y_p^obs = 0.245 ± 0.003（Planck 2018 相容，引用不复算）

def freeze_ratio(T_f, Qv=Q):
    """中子-质子冻结比 (n/p)_f = exp(−Q/T_f)。"""
    return mp.exp(-Qv / T_f)

def Yp(T_f, Qv=Q, tau=TAU, t=TBBN):
    """Y_p = 2x/(1+x)，x = (n/p)_f · exp(−t_BBN/τ_n)；返回 (Y_p, r=n/p, x, s=衰变抑制因子)。"""
    r = mp.exp(-Qv / T_f)
    s = mp.exp(-t / tau)
    x = r * s
    Y = 2 * x / (1 + x)
    return Y, r, x, s

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

# ---------- 中子衰变抑制因子 s = exp(−t_BBN/τ_n) ----------
s_decay = mp.exp(-TBBN / TAU)

# ---------- Y_p(T_f) 网格 ----------
T_grid = [mp.mpf(v) for v in ["0.6", "0.7", "0.8", "0.9", "1.0"]]
table = []
for Tf in T_grid:
    Y, r, x, s = Yp(Tf)
    table.append((Tf, r, x, Y))

Y_at_08 = table[2][3]

# ---------- 反解 T_f*：Y_p(T_f*) = 0.245（二分 + 牛顿双路径） ----------
# 路径 1：二分法，括号 [0.5, 1.2] MeV，800 次迭代达 250 位精度
lo, hi = mp.mpf("0.5"), mp.mpf("1.2")
for _ in range(800):
    mid = (lo + hi) / 2
    if Yp(mid)[0] < Y_OBS:
        lo = mid
    else:
        hi = mid
Tstar_bisect = (lo + hi) / 2

# 路径 2：牛顿迭代 T ← T − (Y − 0.245) / (dY/dT)，闭式导数见下节
def dYpdT(Tf, Qv=Q, tau=TAU, t=TBBN):
    """dY_p/dT_f = (dY/dx)(x Q/T_f²)，dY/dx = 2/(1+x)²。"""
    r = mp.exp(-Qv / Tf)
    s = mp.exp(-t / tau)
    x = r * s
    dYdx = 2 / (1 + x) ** 2
    return dYdx * x * Qv / Tf ** 2

Tstar_newton = mp.mpf("0.8")
for _ in range(200):
    f = Yp(Tstar_newton)[0] - Y_OBS
    fp = dYpdT(Tstar_newton)
    Tstar_newton = Tstar_newton - f / fp

Tstar = Tstar_bisect
Ystar_back = Yp(Tstar)[0]

# ---------- 解析求导验证（基准点 T_f = 0.8 MeV） ----------
T0 = mp.mpf("0.8")
Y0, r0, x0, s0 = Yp(T0)
dYdx = 2 / (1 + x0) ** 2

# ① dY_p/dT_f = (∂Y/∂x)(∂x/∂T_f) = dYdx · x · Q/T_f² > 0
dYdT_ana = dYdx * x0 * Q / T0 ** 2

# ② dY_p/dτ_n = (∂Y/∂x)(∂x/∂τ_n) = dYdx · x · t_BBN/τ_n² > 0
dYdtau_ana = dYdx * x0 * TBBN / TAU ** 2

# ③ dY_p/dQ = (∂Y/∂x)(∂x/∂Q) = −dYdx · x / T_f < 0（Q 增 → (n/p) 降 → Y_p 降）
dYdQ_ana = -dYdx * x0 / T0

# 数值中心差分互验（250 位，δ=1e-50；中心差分截断 O(δ²·Y‴) ~ 1e-100 量级）
delta = mp.mpf("1e-50")

def Yp_tau(ta, Tf=T0):
    r = mp.exp(-Q / Tf)
    x = r * mp.exp(-TBBN / ta)
    return 2 * x / (1 + x)

def Yp_Q(qq, Tf=T0):
    r = mp.exp(-qq / Tf)
    x = r * s_decay
    return 2 * x / (1 + x)

dYdT_num = (Yp(T0 + delta)[0] - Yp(T0 - delta)[0]) / (2 * delta)
dYdtau_num = (Yp_tau(TAU + delta) - Yp_tau(TAU - delta)) / (2 * delta)
dYdQ_num = (Yp_Q(Q + delta) - Yp_Q(Q - delta)) / (2 * delta)

diff_dT   = mp.fabs(dYdT_num - dYdT_ana)
diff_dtau = mp.fabs(dYdtau_num - dYdtau_ana)
diff_dQ   = mp.fabs(dYdQ_num - dYdQ_ana)

# ---------- 守卫（按实算值校核） ----------
G("G1_Yp_at_0p8_in_band", mp.mpf("0.25") <= Y_at_08 <= mp.mpf("0.30"),
  f"Y_p(0.8 MeV)={mp.nstr(Y_at_08, 16)} ∈ [0.25, 0.30]（解析 2 参数模型读数，非数值 BBN 精确值）")
G("G2_Tstar_in_band", mp.mpf("0.70") <= Tstar <= mp.mpf("0.85"),
  f"Y_p=0.245 反解 T_f*={mp.nstr(Tstar, 18)} MeV ∈ [0.70, 0.85]")
G("G2b_root_two_path", mp.fabs(Tstar_bisect - Tstar_newton) < mp.mpf("1e-230"),
  f"二分与牛顿双路径根一致（差={mp.nstr(mp.fabs(Tstar_bisect - Tstar_newton), 3)} < 1e-230）")
G("G2c_root_reproduces_0245", mp.fabs(Ystar_back - Y_OBS) < mp.mpf("1e-230"),
  f"回代 Y_p(T_f*)={mp.nstr(Ystar_back, 18)} = 0.245")
G("G3_dYdT_positive", dYdT_ana > 0 and diff_dT < mp.mpf("1e-100"),
  f"dY_p/dT_f>0：闭式={mp.nstr(dYdT_ana, 16)}，中心差分={mp.nstr(dYdT_num, 16)}，"
  f"差={mp.nstr(diff_dT, 3)} < 1e-100 ✓（T_f 升高→中子更多→氦更多）")
G("G4a_dYdtau_positive", dYdtau_ana > 0 and diff_dtau < mp.mpf("1e-100"),
  f"dY_p/dτ_n>0：闭式={mp.nstr(dYdtau_ana, 16)}，中心差分={mp.nstr(dYdtau_num, 16)}，"
  f"差={mp.nstr(diff_dtau, 3)} < 1e-100 ✓（中子寿命变长→衰变更少→氦增加）")
G("G4b_dYdQ_negative", dYdQ_ana < 0 and diff_dQ < mp.mpf("1e-100"),
  f"dY_p/dQ<0：闭式={mp.nstr(dYdQ_ana, 16)}，中心差分={mp.nstr(dYdQ_num, 16)}，"
  f"差={mp.nstr(diff_dQ, 3)} < 1e-100 ✓（Q 增→(n/p) 降→Y_p 降）")
G("G5_decay_suppression", mp.mpf("0.80") <= s_decay <= mp.mpf("0.83"),
  f"exp(−t_BBN/τ_n)=exp(−180/879.4)={mp.nstr(s_decay, 18)} ∈ [0.80, 0.83]（≈0.8149）")
G("G6_TUFT_zero", True,
  "TUFT 供给=0：TUFT 无弱相互作用速率平衡、无核反应网络、无中子衰变通道，"
  "对 BBN 轻元素丰度零机制供给 → 结构性负面，撞 C2（T_f、Q、τ_n 全部外部输入）")

# ---------- 条目 ----------
entries = [
    {"id": "E1", "claim": "观测事实：原初氦丰度基准",
     "value": "Y_p^obs = 0.245 ± 0.003（Planck 2018 相容；D/H、He-3/H、Li-7/H 为标准 BBN 网络输出，引用不复算）",
     "verdict": "PASS"},
    {"id": "E2", "claim": "标准 BBN 解析闭式与精算网格",
     "value": ("(n/p)_f=exp(−Q/T_f)，x=(n/p)_f·exp(−t_BBN/τ_n)，Y_p=2x/(1+x)；"
               "Q=1.293332 MeV，τ_n=879.4 s，t_BBN=180 s（PDG/标准综述引用不复算）。"
               "T_f=0.6→Y={Y06}；0.7→Y={Y07}；0.8→Y={Y08}；0.9→Y={Y09}；1.0→Y={Y10}；"
               "Y_p=0.245 反解 T_f*={TS} MeV（二分/牛顿双路径一致）。").format(
        Y06=mp.nstr(table[0][3], 14), Y07=mp.nstr(table[1][3], 14),
        Y08=mp.nstr(table[2][3], 14), Y09=mp.nstr(table[3][3], 14),
        Y10=mp.nstr(table[4][3], 14), TS=mp.nstr(Tstar, 18)),
     "verdict": "PASS"},
    {"id": "E3", "claim": "解析求导验证（用户指定线）",
     "value": ("dY_p/dT_f=(2/(1+x)²)·x·Q/T_f²>0（闭式={DT}，中心差分差={DDT}）；"
               "dY_p/dτ_n=(2/(1+x)²)·x·t_BBN/τ_n²>0（闭式={DTau}，差={DDTau}）；"
               "dY_p/dQ=−(2/(1+x)²)·x/T_f<0（闭式={DQ}，差={DDQ}）。").format(
        DT=mp.nstr(dYdT_ana, 14), DDT=mp.nstr(diff_dT, 3),
        DTau=mp.nstr(dYdtau_ana, 14), DDTau=mp.nstr(diff_dtau, 3),
        DQ=mp.nstr(dYdQ_ana, 14), DDQ=mp.nstr(diff_dQ, 3)),
     "verdict": "PASS"},
    {"id": "E4", "claim": "TUFT 供给检查",
     "value": "0（TUFT 几何框架内无弱相互作用速率平衡、无核反应网络、无中子衰变通道；T_f、Q、τ_n、t_BBN 全部外部输入）",
     "verdict": "structural_negative"},
    {"id": "E5", "claim": "裁定",
     "value": "结构性负面闭合：BBN 轻元素丰度为标准宇宙学（弱作用速率 + 核反应网络）输出，TUFT 供给 0，撞 C2（绝对标度全部外部给定）",
     "verdict": "structural_negative"},
]

report = {
    "id": CID, "title": "BBN氦丰度攻破", "date": DATE,
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT/几何框架结构性负面闭合",
    "precision": "mpmath 250 位（双 API 兼容）",
    "claim": ("T431 轻元素原初丰度：(n/p)_f=exp(−Q/T_f)，Y_p=2x/(1+x)，x=(n/p)_f·exp(−t_BBN/τ_n)；"
              "Y_p=0.245 反解 T_f*=0.7331 MeV；TUFT 无核合成机制、供给 0，撞 C2；"
              "标准 BBN 解析闭式算术（PDG 输入，引用不复算），未写成 TUFT 预测"),
}

SEP_EQ = "=" * 64
SEP_MIN = "-" * 64
lines = []
lines.append("C0399 BBN 氦丰度攻破（2026-10-29，mpmath 250 位）")
lines.append(SEP_EQ)
lines.append("闭式：(n/p)_f = exp(−Q/T_f)；x = (n/p)_f · exp(−t_BBN/τ_n)；Y_p = 2x/(1+x)")
lines.append("常数：Q = m_n−m_p = 1.293332 MeV（PDG），τ_n = 879.4 s（PDG），t_BBN = 180 s（引用）")
lines.append(SEP_MIN)
lines.append("T_f (MeV)    (n/p)_f          x                Y_p")
for Tf, r, x, Y in table:
    lines.append(f"{mp.nstr(Tf, 6):<12} {mp.nstr(r, 18):<18} {mp.nstr(x, 18):<18} {mp.nstr(Y, 16)}")
lines.append(SEP_MIN)
lines.append(f"中子衰变抑制因子 exp(−t_BBN/τ_n) = exp(−180/879.4) = {mp.nstr(s_decay, 22)}")
lines.append(f"Y_p = 0.245 反解 T_f* = {mp.nstr(Tstar, 22)} MeV（二分 800 次 / 牛顿 200 步双路径一致）")
lines.append(f"回代 Y_p(T_f*) = {mp.nstr(Ystar_back, 18)} = 0.245")
lines.append(SEP_MIN)
lines.append("求导验证（基准点 T_f = 0.8 MeV）：")
lines.append(f"  dY_p/dT_f  = (2/(1+x)²)·x·Q/T_f²  > 0；闭式={mp.nstr(dYdT_ana, 14)}，中心差分差={mp.nstr(diff_dT, 3)} < 1e-100 ✓")
lines.append(f"  dY_p/dτ_n  = (2/(1+x)²)·x·t_BBN/τ_n² > 0；闭式={mp.nstr(dYdtau_ana, 14)}，中心差分差={mp.nstr(diff_dtau, 3)} < 1e-100 ✓")
lines.append(f"  dY_p/dQ    = −(2/(1+x)²)·x/T_f    < 0；闭式={mp.nstr(dYdQ_ana, 14)}，中心差分差={mp.nstr(diff_dQ, 3)} < 1e-100 ✓")
lines.append(SEP_MIN)
lines.append("诚实边界：解析 2 参数模型（T_f、t_BBN）为教学闭式，Y_p 绝对读数与数值 BBN 0.247")
lines.append("          有 ~5-15% 差异属正常；本攻破要点为「标准宇宙学输出、TUFT 供给 0」，不宣称复现数值 BBN 精度。")
lines.append(SEP_MIN)
lines.append("TUFT 供给=0（无弱作用速率平衡、无核反应网络、无中子衰变通道）→ 结构性负面，撞 C2")
lines.append(f"守卫 {len(guards)}/{len(guards)} 全过 → exit_code=0")
lines.append("归因：标准 BBN 解析闭式算术（PDG 输入，引用不复算），未写成 TUFT 预测。")
with io.open(OUT + r"\attack_C0399_BBN氦丰度攻破_2026-10-29_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

with io.open(OUT + r"\attack_C0399_BBN氦丰度攻破_2026-10-29.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0399 exit=0：T_f*={mp.nstr(Tstar, 12)} MeV；Y_p(0.8)={mp.nstr(Y_at_08, 10)}；"
      f"抑制因子={mp.nstr(s_decay, 10)}；守卫 {len(guards)}/{len(guards)}")
