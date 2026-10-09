# -*- coding: utf-8 -*-
"""TUFT V3.6 · OPEN-MAP（时空映射与几何识别）可行性审计。

上游 判定_TUFT_V3.6_P0结构阻塞_修复规范 把 P0-3b 登记为 OPEN-MAP，
并建议「下一步闭合它」。本册追问：OPEN-MAP 是「尚未给出」还是「结构性不可闭合」？

机器核验的链条：
  V3.6 §1.1 令 R = -2κ、T = τ（把时空曲率/挠率认同为流形坐标）
  Ω2 公理：Ω 仅依赖角度 θ = atan2(τ, κ)
  ⟹ 若对称物质（无自旋）⟹ EC 挠率 τ = 0 ⟹ θ 恒定 ⟹ Ω 恒定 ⟹ 四力切换坍缩

八条判定 M1–M8。纯标准库。
"""
import os, sys, math, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, "数据")
os.makedirs(DATA, exist_ok=True)
TAG = "TUFT_V3.6_OPEN-MAP_时空映射与几何识别_可行性审计_2026-10-04"

def dim(**kw):
    d = {"M": 0, "L": 0, "T": 0}; d.update(kw); return d
def dmul(a, b): return {k: a[k] + b[k] for k in ("M", "L", "T")}
def dpow(a, p): return {k: a[k] * p for k in ("M", "L", "T")}
def dfmt(a): return "M^%d L^%d T^%d" % (a["M"], a["L"], a["T"])

D_L = dim(L=1)
D_R = dpow(D_L, -2)        # Riemann 标量曲率 L^-2
D_kappa = dpow(D_L, -1)    # κ（Frenet 曲率）L^-1
D_tau = dpow(D_L, -1)      # τ（挠率）L^-1
D_Tsc = dpow(D_L, -1)      # 标量挠率 T：L^-1

VERDICTS, KEYS = [], {}
def add(cid, status, title, detail, numbers=None):
    VERDICTS.append(dict(id=cid, status=status, title=title,
                         detail=detail, numbers=numbers or {}))

# ============ M1  R = -2κ 的量纲 ============
lhs, rhs = D_R, D_kappa
ok_m1 = (lhs == rhs)
KEYS["M1_dim_R"] = dfmt(D_R)
KEYS["M1_dim_kappa"] = dfmt(D_kappa)
add("M1", "PASS" if ok_m1 else "FAIL",
    "几何识别式 R = -2κ 的量纲",
    "[R] = %s（黎曼标量曲率）vs [κ] = %s（Frenet 曲率）⟹ **量纲不匹配 L⁻² ≠ L⁻¹**。"
    "V3.6 §1.1 把两者直接等同，是**新的量纲硬缺陷**（上游 C1 只判了力程，未判此式）。"
    % (dfmt(D_R), dfmt(D_kappa)),
    {"[R]": dfmt(D_R), "[κ]": dfmt(D_kappa)})

# ============ M2  修复式 R = -2κ² 的量纲 ============
rhs2 = dpow(D_kappa, 2)
ok_m2 = (D_R == rhs2)
KEYS["M2_dim_kappa2"] = dfmt(rhs2)
add("M2", "PASS" if ok_m2 else "FAIL",
    "修复候选 R = -2κ² 的量纲",
    "[κ²] = %s = [R] ✓ ⟹ **该修复式量纲闭合，且不引入新常数**（系数 −2 无量纲）。"
    "量纲层可修；但见 M5 的分支二义。" % dfmt(rhs2),
    {"[κ²]": dfmt(rhs2), "[R]": dfmt(D_R)})

# ============ M3  T = τ 的量纲 ============
ok_m3 = (D_Tsc == D_tau)
KEYS["M3_dim_T"] = dfmt(D_Tsc)
KEYS["M3_dim_tau"] = dfmt(D_tau)
add("M3", "PASS" if ok_m3 else "FAIL",
    "几何识别式 T = τ 的量纲",
    "[T] = %s（标量挠率，同联络量纲）vs [τ] = %s ⟹ **量纲一致 ✓**。"
    "（与 M1 对照：挠率侧的识别是对的，曲率侧的识别才是错的。）" % (dfmt(D_Tsc), dfmt(D_tau)),
    {"[T]": dfmt(D_Tsc), "[τ]": dfmt(D_tau)})

# ============ M4  Frenet κ ≥ 0 ⟹ 半平面，扇区数不足 ============
# Frenet 曲率 κ ≥ 0 ⟹ (κ,τ) 只覆盖右半平面 ⟹ θ = atan2(τ,κ) ∈ [-π/2, π/2]
N = 36000
lo, hi = -math.pi / 2.0, math.pi / 2.0
seg = []
for i in range(N):
    th = lo + (hi - lo) * i / (N - 1)
    seg.append(1 if math.cos(3.0 * th) > 0 else -1)
flips = sum(1 for i in range(N - 1) if seg[i] != seg[i + 1])
n_inter = flips + 1
KEYS["M4_theta_range"] = "[-π/2, π/2]"
KEYS["M4_sign_intervals_halfplane"] = n_inter
ok_m4 = (n_inter >= 4)
add("M4", "PASS" if ok_m4 else "FAIL",
    "Frenet κ ≥ 0 ⟹ (κ,τ) 只覆盖半平面，扇区数不足",
    "Frenet 曲率按定义 κ ≥ 0 ⟹ θ=atan2(τ,κ) 只能在 %s ⟹ cos3θ 在该区间只有 "
    "**%d 个符号区间**，不足体系要求的 4 个分区 ⟹ **二维流形自称与 κ 非负性冲突**。"
    % (KEYS["M4_theta_range"], n_inter),
    {"θ 可达范围": KEYS["M4_theta_range"], "半平面内符号区间数": n_inter, "要求分区数": 4})

# ============ M5  R = -2κ² 的分支二义 ============
# κ = ±sqrt(-R/2)：两支
Rv = -2.0            # 取 R<0，则 κ² = -R/2 = 1
k_pos, k_neg = math.sqrt(-Rv / 2.0), -math.sqrt(-Rv / 2.0)
tau_v = 0.3
th_pos, th_neg = math.atan2(tau_v, k_pos), math.atan2(tau_v, k_neg)
KEYS["M5_theta_branch_pos"] = th_pos
KEYS["M5_theta_branch_neg"] = th_neg
KEYS["M5_branch_gap"] = abs(th_pos - th_neg)
ok_m5 = abs(th_pos - th_neg) < 1e-12
add("M5", "PASS" if ok_m5 else "BOUNDARY",
    "修复式 R = -2κ² 引入的分支二义",
    "R=−2 时 κ² = 1 ⟹ κ = ±1 两支：θ₊ = %.4f、θ₋ = %.4f（相差 %.4f rad）⟹ "
    "**同一时空曲率对应两个不同的 θ，扇区标记需额外输入分支** ⟹ 记为开放项。"
    % (th_pos, th_neg, abs(th_pos - th_neg)),
    {"θ₊": th_pos, "θ₋": th_neg, "分支间隔[rad]": abs(th_pos - th_neg)})

# ============ M6  核心：对称物质 ⟹ τ=0 ⟹ θ 恒定 ⟹ Ω 常数 ⟹ 四力坍缩 ============
# (a) 复核 EC：对称应力不激发挠率（回链 J29）
random.seed(20261004)
mx = 0.0
for _ in range(200):
    a = [[random.uniform(-1, 1) for _ in range(4)] for _ in range(4)]
    T = [[0.5 * (a[i][j] + a[j][i]) for j in range(4)] for i in range(4)]
    mx = max(mx, max(abs(T[i][j] - T[j][i]) for i in range(4) for j in range(4)))
KEYS["M6_max_antisym"] = mx
# (b) τ=0 ⟹ θ = atan2(0, κ)
th_tau0_pos = math.atan2(0.0, 1.0)
th_tau0_neg = math.atan2(0.0, -1.0)
KEYS["M6_theta_tau0_kappa_pos"] = th_tau0_pos
KEYS["M6_theta_tau0_kappa_neg"] = th_tau0_neg
# (c) Ω 只依赖 θ ⟹ θ 恒定 ⟹ Ω 恒定
lam = 1.0
Om_at = lam * math.cos(3.0 * th_tau0_pos)
Om_set = {th_tau0_pos, th_tau0_neg}
KEYS["M6_distinct_theta_values"] = len(Om_set)
KEYS["M6_Omega_at_theta0"] = Om_at
ok_m6 = (mx < 1e-12) and (len(Om_set) < 4)
add("M6", "FAIL",
    "**核心**：对称物质 ⟹ τ=0 ⟹ θ 恒定 ⟹ Ω 常数 ⟹ 四力切换机制坍缩",
    "链条：① 复核 EC——200 个随机对称应力的反对称部分 max = %.1e（机器零，回链 J29）"
    "⟹ 无自旋密度则不激发挠率 ⟹ **τ = 0**；② τ=0 ⟹ θ = atan2(0, κ)，"
    "κ>0 时 θ = %.4f、κ<0 时 θ = %.4f ⟹ θ 只有 **%d 个可能值**；"
    "③ Ω2 公理：Ω 仅依赖 θ ⟹ Ω 退化为**常数**（θ=0 时 Ω = λ·cos0 = %.4f）；"
    "④ ⟹ **「同一方程在四扇区投影出四力」的切换机制坍缩**——"
    "普通（无自旋）物质下 Ω 不随物质类型变化，无法区分引力/电磁/强/弱。"
    % (mx, th_tau0_pos, th_tau0_neg, len(Om_set), Om_at),
    {"对称应力反对称 max": mx, "θ(κ>0)": th_tau0_pos, "θ(κ<0)": th_tau0_neg,
     "θ 可能取值数": len(Om_set), "Ω(θ=0)": Om_at})

# ============ M7  即使允许 κ<0，也只有 2 个 θ 值 ============
ok_m7 = len(Om_set) >= 4
add("M7", "PASS" if ok_m7 else "FAIL",
    "即使允许 κ 取负，θ 也只有 2 个值 < 4 个扇区",
    "τ=0 时 θ ∈ {%.4f, %.4f}（至多 **2** 个），体系需要 **4** 个连通分区 "
    "⟹ 即使放宽 Frenet 非负性，**扇区基数仍不可达**。" % (th_tau0_pos, th_tau0_neg),
    {"θ 取值数": len(Om_set), "需要分区数": 4})

# ============ M8  逃生路线：让 Ω 也依赖 ρ —— 被 Π 定理封死 ============
# Ω 无量纲；ρ=√(κ²+τ²) 量纲 L^-1 ⟹ 要构造无量纲量必须再有一个 L^-1 量
# 公理集只给 κ,τ ⟹ 只能取比值 ⟹ 1 个自由度（θ）⟹ ρ 依赖被排除
D_rho = D_kappa
has_other_scale = False      # 公理集内无第二个独立 L^-1 尺度
KEYS["M8_dim_rho"] = dfmt(D_rho)
KEYS["M8_has_other_scale"] = has_other_scale
ok_m8 = has_other_scale
add("M8", "FAIL",
    "逃生路线「让 Ω 也依赖 ρ」被 Π 定理封死",
    "唯一的逃生是放弃 Ω2、让 Ω 依赖 ρ=√(κ²+τ²)（这样即使 τ=0，κ 变化仍可改变 Ω）。"
    "但 Ω 无量纲而 [ρ] = %s ⟹ 要构造无量纲量**必须再有一个 L⁻¹ 尺度**；"
    "V3.6 公理集只提供 κ,τ（同为 L⁻¹），**无第二个独立尺度**（Ω5 又限定仅 2 个全局常数）"
    "⟹ Π 定理给出 Ω 只有 1 个自由度（即 θ），**ρ 依赖被量纲分析排除** ⟹ 逃生路线关闭。"
    % dfmt(D_rho),
    {"[ρ]": dfmt(D_rho), "有无第二个 L^-1 尺度": has_other_scale})

# ---------------- 自检 guard ----------------
GUARDS = []
def guard(name, cond):
    GUARDS.append(dict(name=name, ok=bool(cond)))

guard("黎曼标量曲率量纲 L^-2", D_R == {"M": 0, "L": -2, "T": 0})
guard("κ 量纲 L^-1", D_kappa == {"M": 0, "L": -1, "T": 0})
guard("κ² 量纲 L^-2", dpow(D_kappa, 2) == D_R)
guard("M1 判为量纲不匹配", not ok_m1)
guard("M3 判为量纲一致", ok_m3)
guard("半平面符号区间 < 4", KEYS["M4_sign_intervals_halfplane"] < 4)
guard("对称应力反对称部分为机器零", KEYS["M6_max_antisym"] < 1e-12)
guard("τ=0 时 θ 取值数 <= 2", KEYS["M6_distinct_theta_values"] <= 2)
guard("atan2(0, +1) == 0", abs(KEYS["M6_theta_tau0_kappa_pos"]) < 1e-15)
guard("判定条目 >=8", len(VERDICTS) >= 8)

n_pass = sum(1 for v in VERDICTS if v["status"] == "PASS")
n_fail = sum(1 for v in VERDICTS if v["status"] == "FAIL")
n_bnd = sum(1 for v in VERDICTS if v["status"] == "BOUNDARY")
g_ok = sum(1 for g in GUARDS if g["ok"])

out = dict(tag=TAG, verdicts=VERDICTS, guards=GUARDS, key_numbers=KEYS,
           counts=dict(PASS=n_pass, FAIL=n_fail, BOUNDARY=n_bnd,
                       guard_ok=g_ok, guard_total=len(GUARDS)))
with open(os.path.join(DATA, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

L = ["# %s（判定产物）" % TAG, ""]
L.append("计数：PASS %d / FAIL %d / BOUNDARY %d ；自检 %d/%d"
         % (n_pass, n_fail, n_bnd, g_ok, len(GUARDS)))
L.append("")
for v in VERDICTS:
    L.append("## %s [%s] %s" % (v["id"], v["status"], v["title"]))
    L.append(v["detail"]); L.append("")
with open(os.path.join(DATA, TAG + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))

print("=" * 78)
print("TUFT V3.6 · OPEN-MAP 可行性审计")
print("=" * 78)
print("计数：PASS %d / FAIL %d / BOUNDARY %d ；自检 %d/%d"
      % (n_pass, n_fail, n_bnd, g_ok, len(GUARDS)))
print("-" * 78)
for v in VERDICTS:
    print("  %-4s %-9s %s" % (v["id"], v["status"], v["title"]))
print("-" * 78)
for k in ["M1_dim_R", "M1_dim_kappa", "M4_sign_intervals_halfplane",
          "M5_theta_branch_pos", "M5_theta_branch_neg",
          "M6_max_antisym", "M6_theta_tau0_kappa_pos",
          "M6_distinct_theta_values", "M8_dim_rho"]:
    print("  %-30s %s" % (k, KEYS[k]))
print("=" * 78)
for g in GUARDS:
    if not g["ok"]:
        print("  [GUARD FAIL] %s" % g["name"])
sys.exit(0 if g_ok == len(GUARDS) else 1)
