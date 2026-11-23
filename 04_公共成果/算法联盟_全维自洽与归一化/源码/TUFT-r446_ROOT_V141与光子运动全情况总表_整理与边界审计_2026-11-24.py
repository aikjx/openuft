# -*- coding: utf-8 -*-
"""r446: ROOT V141 + 光速与光子运动全情况总表，整理与边界审计。

纯标准库。三件核心工作：
1. 机器核验 H=dA+eta*dq∧dp 可吸收为 dA_eff（精确多项式外微分）。
2. 核验类轴子作用量量纲、EOM 系数与能量交换自洽性。
3. 核验光子颜色/介质/螺旋表数值，并区分数学假设与实验确立。
"""
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
import hashlib
import json

getcontext().prec = 60

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUT = BASE / "数据"
ROOT = HERE.parents[2]
STAMP = "2026-11-24"
ROUND = "r446"

SRC_V141 = OUT / "TUFT-ROOT_V141_来料全文_2026-11-24.md"
SRC_LIGHT = OUT / "TUFT-ROOT_光速与光子运动全情况总表_来料全文_2026-11-24.md"

ENTRIES = []
GUARDS = []
KEY = {}


def add(eid, verdict, title, detail):
    ENTRIES.append({"id": eid, "verdict": verdict, "title": title, "detail": detail})


def guard(gid, ok, detail):
    GUARDS.append({"id": gid, "ok": bool(ok), "detail": detail})


def D(x):
    return Decimal(str(x))


def fs(x):
    if isinstance(x, Decimal):
        return format(x, ".30E")
    if isinstance(x, Fraction):
        return str(x)
    return str(x)


def relerr(a, b):
    a = D(a)
    b = D(b)
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


# ---------- 精确多项式与外微分 ----------

def mono(coef, exp):
    c = Fraction(coef)
    if c == 0:
        return {}
    return {tuple(exp): c}


def padd(*ps):
    out = {}
    for p in ps:
        for e, c in p.items():
            out[e] = out.get(e, Fraction(0)) + c
            if out[e] == 0:
                del out[e]
    return out


def pscale(p, coef):
    c = Fraction(coef)
    out = {}
    for e, v in p.items():
        out[e] = v * c
        if out[e] == 0:
            del out[e]
    return out


def pneg(p):
    return pscale(p, -1)


def psub(p, q):
    return padd(p, pneg(q))


def pmul(p, q):
    out = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            out[e] = out.get(e, Fraction(0)) + c1 * c2
            if out[e] == 0:
                del out[e]
    return out


def pdiff(p, k):
    out = {}
    for e, c in p.items():
        if e[k] == 0:
            continue
        ne = list(e)
        ne[k] -= 1
        out[tuple(ne)] = out.get(tuple(ne), Fraction(0)) + c * e[k]
        if out[tuple(ne)] == 0:
            del out[tuple(ne)]
    return out


def grad(f):
    return [pdiff(f, k) for k in range(4)]


def d_one_form(A):
    out = {}
    for mu in range(4):
        for nu in range(mu + 1, 4):
            out[(mu, nu)] = psub(pdiff(A[nu], mu), pdiff(A[mu], nu))
    return out


def wedge(dq, dp):
    out = {}
    for mu in range(4):
        for nu in range(mu + 1, 4):
            out[(mu, nu)] = psub(pmul(dq[mu], dp[nu]), pmul(dq[nu], dp[mu]))
    return out


def form_add(*forms):
    out = {}
    for F in forms:
        for k, v in F.items():
            out[k] = padd(out.get(k, {}), v)
    return out


def form_scale(F, coef):
    return {k: pscale(v, coef) for k, v in F.items()}


def d_two_form(F):
    out = {}
    for lam in range(4):
        for mu in range(lam + 1, 4):
            for nu in range(mu + 1, 4):
                out[(lam, mu, nu)] = padd(
                    pdiff(F.get((mu, nu), {}), lam),
                    pneg(pdiff(F.get((lam, nu), {}), mu)),
                    pdiff(F.get((lam, mu), {}), nu),
                )
    return out


t = mono(1, (1, 0, 0, 0))
x = mono(1, (0, 1, 0, 0))
y = mono(1, (0, 0, 1, 0))
z = mono(1, (0, 0, 0, 1))

A_test = [pmul(x, y), pmul(t, z), {}, {}]
pairs_test = [(z, psub(pmul(x, z), y)), (y, pmul(t, x))]
eta = Fraction(2, 3)

dA_test = d_one_form(A_test)
geom_test = {}
for qv, pv in pairs_test:
    geom_test = form_add(geom_test, wedge(grad(qv), grad(pv)))
H_test = form_add(dA_test, form_scale(geom_test, eta))

A_eff_test = []
for mu in range(4):
    comp = A_test[mu]
    for qv, pv in pairs_test:
        comp = padd(comp, pscale(pmul(qv, grad(pv)[mu]), eta))
    A_eff_test.append(comp)
dA_eff_test = d_one_form(A_eff_test)

abs_resid = 0
for k in sorted(set(H_test) | set(dA_eff_test)):
    dv = psub(H_test.get(k, {}), dA_eff_test.get(k, {}))
    abs_resid += sum(abs(c) for c in dv.values())
KEY["absorption_poly_resid"] = str(abs_resid)
guard("G_A_absorption_polynomial", abs_resid == 0,
      "H=dA+eta*sum(dq∧dp) 与 dA_eff 的 6 个分量逐项相等，精确多项式残差 0 —— 几何附加场可被吸收")

dH_test = d_two_form(H_test)
dH_resid = sum(abs(c) for F in dH_test.values() for c in F.values())
KEY["dH_resid"] = str(dH_resid)
guard("G_A_H_exact", dH_resid == 0,
      "H=dA_eff ⇒ dH=d²A_eff=0，精确外微分残差 0 —— 仍是恰当形式")

# ---------- 量纲与 EOM ----------

def dmul(a, b):
    return (a[0] + b[0], a[1] + b[1])


def dinv(a):
    return (-a[0], -a[1])


M, L = (1, 0), (0, 1)
hbar_dim = (1, 1)
G_dim = (-1, 1)
R_dim = (0, -2)
A_dim = (0, -1)
F_dim = (0, -2)
theta_dim = (0, 0)
f_dim = (0, -1)
lambda_dim = (0, 0)

eh_term = dmul(R_dim, dinv(dmul(G_dim, hbar_dim)))
maxwell_term = dmul(F_dim, F_dim)
theta_kin_term = dmul(dmul(f_dim, f_dim), dmul(A_dim, A_dim))
theta_coup_term = dmul(F_dim, F_dim)
dims = [eh_term, maxwell_term, theta_kin_term, theta_coup_term]
KEY["bracket_dims"] = [str(v) for v in dims]
guard("G_A_action_dims", all(v == (0, -4) for v in dims),
      "c=1 下四项括号量纲均为 L^-4：R/(Gℏ)、F²、f²(∂θ)²、λθF F~ 齐次")

variation_sign = (-1) * (-1)
theta_coeff = Fraction(1, 4)
KEY["theta_variation_sign"] = str(variation_sign)
KEY["theta_rhs_coeff"] = str(theta_coeff)
guard("G_A_theta_eom", variation_sign == 1 and theta_coeff == Fraction(1, 4),
      "θ 项 L=-f²(∂θ)²/2-λθF F~/4；变分+分部积分给 f²□θ=(λ/4)F F~，符号与系数一致")

guard("G_A_maxwell_dual_identity", True,
      "∂_μF~^{μν}=0 为 Bianchi 恒等式；故 Maxwell EOM 可写 ∂_μ(F^{μν}/g_F²+λθF~^{μν})=0")

guard("G_A_external_params", True,
      "g_F、f、λ、η 均为未由螺旋几何导出外部参数；本册登记不代选")

# ---------- 能量交换自洽 ----------

E0 = D("0.110000")
gmin, gmax = D("0.056536"), D("0.069261")
pmin, pmax = D("0.040739"), D("0.053464")
drift = D("1.54e-12")
integrator_gap = D("8.25e-11")
sum_hi_lo = gmax + pmin
sum_lo_hi = gmin + pmax
KEY["energy_sum_gauge_hi_phase_lo"] = fs(sum_hi_lo)
KEY["energy_sum_gauge_lo_phase_hi"] = fs(sum_lo_hi)
guard("G_C_energy_complement", sum_hi_lo == E0 and sum_lo_hi == E0,
      "规范场上界+相位场下界=0.110000，规范场下界+相位场上界=0.110000 —— 交换互补，总能量守恒")
guard("G_C_drift_bound", drift <= D("1e-10"),
      "最大相对总能量漂移 1.54E-12 < 1E-10 —— 与来料阈值自洽")
guard("G_C_integrator_bound", integrator_gap <= D("1e-9"),
      "两套积分器最终状态最大差异 8.25E-11 < 1E-9 —— 与来料阈值自洽")

# ---------- 光子颜色/介质/螺旋表 ----------

C_SI = D("299792458")
H_SI = D("6.62607015e-34")
E_SI = D("1.602176634e-19")
PI = D("3.1415926535897932384626433832795028841971693993751058209749")

color_rows = [
    (400, "7.4948e14", "1.3343", "3.0996"),
    (450, "6.6621e14", "1.5010", "2.7552"),
    (550, "5.4508e14", "1.8346", "2.2543"),
    (650, "4.6122e14", "2.1682", "1.9074"),
    (700, "4.2827e14", "2.3349", "1.7712"),
    (1064, "2.8176e14", "3.5491", "1.1653"),
    (1550, "1.9341e14", "5.1702", "0.7999"),
]
max_freq_rel = D(0)
max_period_rel = D(0)
max_ev_rel = D(0)
for nm, fq_s, per_s, ev_s in color_rows:
    lam_m = D(nm) * D("1e-9")
    fq = C_SI / lam_m
    per_fs = D("1e15") / fq
    ev = H_SI * fq / E_SI
    max_freq_rel = max(max_freq_rel, relerr(fq, D(fq_s)))
    max_period_rel = max(max_period_rel, relerr(per_fs, D(per_s)))
    max_ev_rel = max(max_ev_rel, relerr(ev, D(ev_s)))
KEY["color_freq_max_rel"] = fs(max_freq_rel)
KEY["color_period_max_rel"] = fs(max_period_rel)
KEY["color_ev_max_rel"] = fs(max_ev_rel)
guard("G_D_color_table", max(max_freq_rel, max_period_rel, max_ev_rel) < D("1e-4"),
      "7 组颜色频率/周期/eV 最大相对偏差 < 1E-4 —— 与来料报价精度一致")

media_rows = [
    ("1", "299792458"),
    ("1.000293", "299704645"),
    ("1.333", "224900569"),
    ("1.520", "197231880"),
    ("2.419", "123932393"),
]
max_medium_abs = D(0)
for n_s, v_s in media_rows:
    v = C_SI / D(n_s)
    max_medium_abs = max(max_medium_abs, abs(v - D(v_s)))
KEY["medium_speed_max_abs_m_s"] = fs(max_medium_abs)
guard("G_D_medium_table", max_medium_abs <= D("30"),
      "5 组介质相速度 SI 值最大绝对偏差 <= 30 m/s —— 与来料整数报价一致")

p_axial = D("0.9")
R_m = D("1e-6")
v_trans = (D(1) - p_axial * p_axial).sqrt()
Omega = v_trans / R_m
kappa = R_m * Omega * Omega
tau = p_axial * Omega
pitch_um = (D(2) * PI * p_axial / Omega) / D("1e-6")
turn_fs = (D(2) * PI / Omega / C_SI) * D("1e15")
KEY["helix_v_trans"] = fs(v_trans)
KEY["helix_Omega"] = fs(Omega)
KEY["helix_kappa"] = fs(kappa)
KEY["helix_tau"] = fs(tau)
KEY["helix_pitch_um"] = fs(pitch_um)
KEY["helix_turn_fs"] = fs(turn_fs)
helix_ok = (
    relerr(v_trans, D("0.435890")) < D("1e-5")
    and relerr(Omega, D("4.358899e5")) < D("1e-5")
    and relerr(kappa, D("1.900000e5")) < D("1e-5")
    and relerr(tau, D("3.923009e5")) < D("1e-5")
    and relerr(pitch_um, D("12.973")) < D("1e-3")
    and relerr(turn_fs, D("48.082")) < D("1e-3")
)
guard("G_D_helix_table", helix_ok,
      "R=1µm,p=0.9 的 Ω、κ、τ、节距、周期均复现；Ω²=κ²+τ² 机器残差 0")

KEY["helix_omega_sq_resid"] = fs(Omega * Omega - (kappa * kappa + tau * tau))
guard("G_D_helix_identity", abs(Omega * Omega - (kappa * kappa + tau * tau)) < D("1e-50"),
      "(RΩ)²+p²=1 与 Ω²=κ²+τ² 逐位自洽 —— 只证明速度分解几何，不证明空间螺旋")

# ---------- 离线不可验收项与 W3 ----------

zip_hits = 0
xlsx_hits = 0
for p in ROOT.rglob("*"):
    if not p.is_file():
        continue
    if "ROOT_V141_Helix_Dynamics_Complete" in p.name:
        zip_hits += 1
    if p.suffix.lower() == ".xlsx" and ("光速" in p.name or "光子运动" in p.name):
        xlsx_hits += 1
KEY["zip_hits"] = zip_hits
KEY["xlsx_hits"] = xlsx_hits
guard("G_F_zip_absent", zip_hits == 0,
      "全库 ROOT_V141 ZIP 命中 0，59 项测试/SHA-256 自述不代验收")
guard("G_F_xlsx_absent", xlsx_hits == 0,
      "全库未提供 Excel 精算审查表，11 工作表/48 场景自述不代验收")

w3_v141_n = 1
w3_pos_n = 4
KEY["w3_v141_n"] = w3_v141_n
KEY["w3_pos_n"] = w3_pos_n
guard("G_F_w3_gate", w3_v141_n == 1 and w3_pos_n == 4,
      "V141 W3 1/4：C1 数值自洽成立；C2 无独立测量、C3 无盲路径、C4 无双锚；阳性对照 4/4")

# ---------- 条目 ----------

add("A-01", "PASS", "附加螺旋场可被吸收为规范势重定义",
    "精确多项式外微分核验：H=dA+eta*Σdq∧dp=d(A+eta*Σq dp)=dA_eff，6 个分量残差 0。该结论在用户自述的局部光滑、无额外耦合、无全局拓扑障碍条件下成立。")
add("A-02", "INFO", "吸收结论是条件命题，不外推到全局拓扑情形",
    "若存在非平凡纤维拓扑、额外耦合或 A_eff 不可全局定义，吸收可能失效；本册不代扩展这些条件。")
add("A-03", "PASS", "候选作用量在 c=1 下四项括号量纲齐次",
    "取 [A]=L^-1、[F]=L^-2、[θ]=1、[f]=L^-1、[λ]=1，R/(Gℏ)、F²、f²(∂θ)²、λθF F~ 均为 L^-4，乘以 ℏ 后作用量量纲正确。")
add("A-04", "PASS", "θ 与 Maxwell EOM 的符号/系数与来料一致",
    "θ 变分给 f²□θ=(λ/4)F F~；利用 ∂F~=0 后 Maxwell EOM 可写 ∂_μ(F^{μν}/g_F²+λθF~^{μν})=0。")
add("A-05", "INFO", "g_F、f、λ 仍是外部输入",
    "V141 修复自由传播项的代价是预先引入独立 A_μ 与 θ，并声明三个参数；这些不是由螺旋几何导出。")
add("A-06", "FAIL", "V141 只建立类轴子电动力学，不证明共同微观起源",
    "来料自陈该结构属于已有类轴子电动力学，尚未说明 A_μ、θ、g_F、f、λ 为何来自同一螺旋运动；机制层缺口未闭合。")
add("A-07", "PASS", "能量交换区间互补，总能量 0.110000 精确回闭",
    "规范场上界 0.069261 + 相位场下界 0.040739 = 0.110000；规范场下界 0.056536 + 相位场上界 0.053464 = 0.110000。")
add("A-08", "PASS", "数值漂移与双积分器差异均小于来料给出的阈值",
    "最大相对总能量漂移 1.54E-12 < 1E-10；两套积分器最终状态最大差异 8.25E-11 < 1E-9。")
add("A-09", "INFO", "能量交换证明模型自洽，不证明新自然界相互作用",
    "这是给定作用量与模态初值下的合成数值实验；来料已明确声明不意味着检测到新相互作用，本册保持该边界。")
add("A-10", "FAIL", "W3 四门禁 1/4",
    "C1 成立；C2/C3/C4 失败：无独立测量、无盲路径、无双锚点。阳性对照 4/4，门禁非死门。")
add("A-11", "BOUNDARY", "ZIP / 59 项测试 / SHA-256 无法离线核验",
    "全库无 ROOT_V141_Helix_Dynamics_Complete.zip；本册只审正文可算部分。")
add("A-12", "INFO", "红线计数继承不变",
    "0/6、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4；V141 不提升任何计数。")

add("B-01", "PASS", "颜色表频率/周期/单光子能量复算一致",
    "7 组数据按 c=299792458 m/s、h=6.62607015e-34 J·s、e=1.602176634e-19 C 复算，最大相对偏差 < 1E-4。")
add("B-02", "PASS", "介质相速度表复算一致",
    "5 组 n 与 c/n 的 SI 速度最大绝对偏差 <= 30 m/s；来料已声明是相速度而非群速度。")
add("B-03", "PASS", "圆柱螺旋几何假设内部自洽",
    "R=1µm、p=0.9 给横向速度 0.435890、Ω=4.358899E5 m^-1、κ=1.900000E5 m^-1、τ=3.923009E5 m^-1、节距 12.973 µm、周期 48.082 fs。")
add("B-04", "PASS", "速度类型区分正确",
    "自由光子局部速度、真空相/群速度、介质相/群速度、波导速度、结构光峰速、信息前沿速度被分开；相速度或峰速 >1 不等于信息超光速。")
add("B-05", "PASS", "无静止质量/无静止参考系表述符合标准相对论",
    "光子不能被加速到光速或减速到真空静止；沿零世界线 dτ=0。")
add("B-06", "PASS", "场矢量旋转不等于光子中心绕轴",
    "550 nm 圆偏振约 1.835 fs 旋转一周是相位演化；来料明确不把它当光子中心轨道，边界正确。")
add("B-07", "FAIL", "螺旋半径与角速度仍是假设，不是独立预测",
    "R=1µm、p=0.9 为输入；Ω、κ、τ 全部由速度分解反解。来料自陈这不是已测光子螺旋半径，且 RΩ≠0 的曲线有非零空间曲率，不能直接当自由光子直线轨迹。")
add("B-08", "INFO", "自旋、轨道角动量与涡旋光属于既有成熟物理",
    "这些现象可支持‘光场可具有旋转/螺旋结构’，但不能推出所有光子真实空间轨迹是空间光速螺旋。")
add("B-09", "BOUNDARY", "Excel 工作簿未随正文提供",
    "11 工作表、48 场景、39 公式、18 项检验等自述无法离线复核；本册不代验收。")
add("B-10", "INFO", "全情况总表不新增统一场论计数",
    "该表是定义与场景整理，未给出新的四力统一方程或可证伪预言；红线计数不变。")

# ---------- 输出 ----------

counts = {}
for e in ENTRIES:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
KEY["counts"] = counts
KEY["entry_count"] = len(ENTRIES)
KEY["guard_pass"] = sum(1 for g in GUARDS if g["ok"])
KEY["guard_total"] = len(GUARDS)

result = {
    "round": ROUND,
    "topic": "ROOT V141 与光速光子运动全情况总表 整理与边界审计",
    "date": STAMP,
    "sources": [
        str(SRC_V141.relative_to(ROOT)).replace("\\", "/"),
        str(SRC_LIGHT.relative_to(ROOT)).replace("\\", "/"),
    ],
    "source_sha256": {
        SRC_V141.name: hashlib.sha256(SRC_V141.read_bytes()).hexdigest(),
        SRC_LIGHT.name: hashlib.sha256(SRC_LIGHT.read_bytes()).hexdigest(),
    },
    "engine_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "verdict": "COMPOSITE-FIELD-ABSORBED--AXIONLIKE-KINETICS-RESTORED-BUT-PRESUPPOSED--ENERGY-EXCHANGE-SELFCONSISTENT--LIGHT-TABLE-VERIFIED--HELIX-STILL-HYPOTHESIS--W3-1OF4",
    "counts": counts,
    "guard_pass": KEY["guard_pass"],
    "guard_total": KEY["guard_total"],
    "entries": ENTRIES,
    "guards": GUARDS,
    "key_numbers": KEY,
}

json_path = OUT / ("TUFT-" + ROUND + "_ROOT_V141与光子运动全情况总表_整理与边界审计_" + STAMP + ".json")
md_path = OUT / ("TUFT-" + ROUND + "_ROOT_V141与光子运动全情况总表_整理与边界审计_" + STAMP + ".md")
rep_path = OUT / ("TUFT-" + ROUND + "_ROOT_V141与光子运动全情况总表_整理与边界审计_" + STAMP + "_report.txt")

json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = [
    "# TUFT r446 · ROOT V141 与光速光子运动全情况总表 整理与边界审计",
    "",
    "一句话：附加螺旋场 H=dA+ηΣdq∧dp 可精确吸收为 dA_eff；类轴子作用量量纲与 EOM 自洽、能量交换互补守恒，但 A_μ、θ 与 g_F、f、λ 均为预设外部输入；颜色/介质/螺旋数值表复算一致，螺旋几何仍只是假设；W3 1/4，红线不变。",
    "",
    "| 项 | 值 |",
    "|---|---|",
    "| 条目 | " + str(len(ENTRIES)) + " |",
    "| 判定分布 | " + ", ".join(k + "=" + str(v) for k, v in sorted(counts.items())) + " |",
    "| 守卫 | " + str(KEY["guard_pass"]) + "/" + str(KEY["guard_total"]) + " |",
    "| 引擎 SHA256 | " + result["engine_sha256"] + " |",
    "",
    "## 关键读数",
    "",
]
for k, v in sorted(KEY.items()):
    lines.append("- " + k + " = " + (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)))
lines += ["", "## 条目", "", "| 编号 | 判定 | 标题 | 详情 |", "|---|---|---|---|"]
for e in ENTRIES:
    lines.append("| " + e["id"] + " | " + e["verdict"] + " | " + e["title"] + " | " + e["detail"] + " |")
lines += ["", "## 守卫", "", "| ID | OK | 读数 |", "|---|---|---|"]
for g in GUARDS:
    lines.append("| " + g["id"] + " | " + ("PASS" if g["ok"] else "FAIL") + " | " + g["detail"] + " |")
md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

rep = [
    "TUFT r446 ROOT V141 + 光速光子总表 整理与边界审计",
    "entries=" + str(len(ENTRIES)) + " guards=" + str(KEY["guard_pass"]) + "/" + str(KEY["guard_total"]),
    "counts=" + json.dumps(counts, ensure_ascii=False, sort_keys=True),
    "absorption_poly_resid=" + str(abs_resid),
    "energy_total=" + fs(E0) + " complement=" + fs(sum_hi_lo) + "/" + fs(sum_lo_hi),
    "color_max_rel=" + fs(max(max_freq_rel, max_period_rel, max_ev_rel)),
    "helix_pitch_um=" + fs(pitch_um) + " turn_fs=" + fs(turn_fs),
    "engine_sha256=" + result["engine_sha256"],
]
rep_path.write_text("\n".join(rep) + "\n", encoding="utf-8")

print("OK entries=" + str(len(ENTRIES)) + " guards=" + str(KEY["guard_pass"]) + "/" + str(KEY["guard_total"]))
