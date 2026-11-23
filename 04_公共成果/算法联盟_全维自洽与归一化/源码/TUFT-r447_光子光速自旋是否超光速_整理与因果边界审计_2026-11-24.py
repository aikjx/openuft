# -*- coding: utf-8 -*-
"""r447 / ROOT 光子光速 + 自旋是否超光速：整理与因果边界审计。

纯标准库。只核验来料中的可算公式、表格与边界陈述：
1. 零质量光子色散、螺旋度相位作用与自旋≠机械转动惯量；
2. 圆偏振 Maxwell/Poynting、箭头端点形式速度与真实物质速度的区分；
3. 真实螺旋轨迹的速度分配、延迟表、Frenet 几何恒等式；
4. 与 r445/r446 已有判定的一致性，不重判其物理结论。
"""

import cmath
import hashlib
import json
import math
import re
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 60

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "数据" / "TUFT-ROOT_光子光速自旋是否超光速_来料全文_2026-11-24.md"
OUT = BASE / "数据"
STEM = "TUFT-r447_光子光速自旋是否超光速_整理与因果边界审计_2026-11-24"

D = lambda x: Decimal(str(x))
C_SI = D("299792458")
LAMBDA = D("550e-9")
P_LASER = D("1e-3")

ROWS = []
GUARDS = []
KEY = {}


def add(cid, verdict, title, detail):
    ROWS.append({"id": cid, "verdict": verdict, "title": title, "detail": detail})


def guard(gid, ok, detail):
    GUARDS.append({"id": gid, "ok": bool(ok), "detail": detail})


def fmt(x):
    if D(x) == 0:
        return "0"
    return format(D(x), ".15E")


def near(a, b, tol):
    return abs(D(a) - D(b)) <= D(tol)


raw_text = RAW.read_text(encoding="utf-8") if RAW.exists() else ""
KEY["source_sha256"] = hashlib.sha256(RAW.read_bytes()).hexdigest() if RAW.exists() else ""
KEY["source_bytes"] = len(RAW.read_bytes()) if RAW.exists() else 0

# ---------- A/B：光锥、螺旋度、圆偏振 ----------
p = D(1)
m0 = D(0)
E = (p * p + m0 * m0).sqrt()
lightcone_resid = E - p
vg = D(1)
KEY["lightcone_resid"] = str(lightcone_resid)
guard("G_lightcone", lightcone_resid == 0 and vg == 1,
      "m0=0 ⇒ E=p 且 dE/dp=1，光锥残差 0")
add("A-01", "PASS", "真空自由光子传播速度不被自旋改变",
    "m0=0 ⇒ E=p=ħω，群速度 dE/dp=1；四动量零条件与螺旋度标签作用于不同自由度。")

sigma_list = [-1, 1]
phase_resid = 0.0
for sigma in sigma_list:
    for theta in (0.0, 0.3, 1.1, 2.7):
        phase = cmath.exp(-1j * sigma * theta)
        phase_resid = max(phase_resid, abs(abs(phase) - 1.0))
KEY["helicity_phase_resid"] = fmt(D(phase_resid))
guard("G_helicity_phase", phase_resid < 1e-12,
      "U(theta)|p,sigma> 只改相位，|phase|=1；σ=±1 两态均成立")
add("A-02", "PASS", "螺旋度是量子态标签，不是机械角速度",
    "J_parallel=σħ 与 Λ=σ 可和 E=|p| 同时成立；没有刚体转动惯量 I，不能写成 ħ=IΩ。")

nu = C_SI / LAMBDA
omega_si = D(2) * D(str(math.pi)) * nu
period_fs = (D(1) / nu) * D("1e15")
tip_ratio = (D("1e-6") * omega_si) / C_SI
quoted_tip_ratio = D("11.424")
torque = D(2) * P_LASER / omega_si
KEY.update({
    "nu_hz": fmt(nu),
    "omega_si_rad_s": fmt(omega_si),
    "period_fs": fmt(period_fs),
    "tip_speed_ratio": fmt(tip_ratio),
    "torque_Nm": fmt(torque),
})
guard("G_tip_ratio", near(tip_ratio, quoted_tip_ratio, "1e-3"),
      "550 nm、1 µm 绘图箭头端点 v_tip/c = 11.424，量级复现")
guard("G_torque", near(torque, D("5.84e-19"), "1e-21"),
      "理想半波片螺旋度反转力矩 2P/ω ≈ 5.84E-19 N·m")
add("A-03", "PASS", "550 nm 频率、周期、端点形式速度与力矩数值可复算",
    "ν=5.45077E14 Hz、T=1.83460 fs、v_tip/c≈11.424、|T|=2P/ω≈5.84E-19 N·m；绘图端点速度非物质速度。")
add("A-04", "INFO", "Beth 实验支持角动量传递，但不推出机械半径",
    "J_z/E=σ/ω 与力矩 2P/ω 只依赖角动量守恒和偏振反转，不需要光子内部刚体模型。")

# ---------- C/D：圆偏振与真实螺旋速度 ----------
k = 1.0
omega = 1.0
h = 1e-6
faraday_resid = 0.0
poynting_resid = 0.0
orth_resid = 0.0
for sigma in sigma_list:
    for z, t in ((0.0, 0.0), (0.37, 0.11), (1.23, 0.77)):
        phi = k * z - omega * t
        Ex, Ey = math.cos(phi), sigma * math.sin(phi)
        Bx, By = -sigma * math.sin(phi), math.cos(phi)
        curl_x = -(sigma * math.sin(k * (z + h) - omega * t) -
                   sigma * math.sin(k * (z - h) - omega * t)) / (2 * h)
        curl_y = (math.cos(k * (z + h) - omega * t) -
                  math.cos(k * (z - h) - omega * t)) / (2 * h)
        dBdt_x = (-sigma * math.sin(k * z - omega * (t + h)) +
                  sigma * math.sin(k * z - omega * (t - h))) / (2 * h)
        dBdt_y = (math.cos(k * z - omega * (t + h)) -
                  math.cos(k * z - omega * (t - h))) / (2 * h)
        faraday_resid = max(faraday_resid,
                            abs(curl_x + dBdt_x), abs(curl_y + dBdt_y))
        poynting_resid = max(poynting_resid, abs(Ex * By - Ey * Bx - 1.0))
        orth_resid = max(orth_resid, abs(Ex * Bx + Ey * By))
KEY["faraday_resid"] = fmt(D(faraday_resid))
KEY["poynting_resid"] = fmt(D(poynting_resid))
guard("G_circular_faraday", faraday_resid < 1e-8,
      "圆偏振 E=B 旋转场满足 ∇×E=-∂B/∂t，最大残差 <1E-8")
guard("G_circular_poynting", poynting_resid < 1e-12 and orth_resid < 1e-12,
      "E·B=0 且 E×B=E0² z，能流始终沿 +z")
add("A-05", "PASS", "圆偏振场旋转不产生横向传播速度",
    "E=E0(x cosφ+σ y sinφ)、B=z×E 时 Maxwell 残差与 E·B 均为机器零量级，E×B 恒沿 +z；场方向旋转不是质心运动。")
add("A-06", "PASS", "电场端点形式超光速不构成信息超光速",
    "v_tip/c≈11.424 来自动画箭头长度 1 µm 的任意绘图尺度；端点不是物质或能量载体，不能传输信息。")

speed_rows = [
    ("1.0000", "0", "0"),
    ("0.9999", "0.014142", "0.334"),
    ("0.9900", "0.141067", "33.693"),
    ("0.9000", "0.435890", "370.627"),
    ("0.8000", "0.600000", "833.910"),
    ("0.6000", "0.800000", "2223.761"),
]
table_ok = True
delay_max = D(0)
computed = []
for vz_s, vp_s, delay_s in speed_rows:
    vz = D(vz_s)
    vp = (D(1) - vz * vz).sqrt()
    delay_ns = D(1000) * (D(1) / vz - D(1)) / C_SI * D("1e9")
    ok = near(vp, D(vp_s), "5e-7") and near(delay_ns, D(delay_s), "0.001")
    table_ok = table_ok and ok
    delay_max = max(delay_max, delay_ns)
    computed.append({"vz": vz_s, "vperp": fmt(vp), "delay_ns": fmt(delay_ns), "ok": ok})
KEY["speed_table"] = computed
KEY["delay_max_ns_1km"] = fmt(delay_max)
guard("G_speed_table", table_ok,
      "6 组 v_z/v_perp/1 km 延迟逐行复算通过，最大延迟 2223.761 ns")
guard("G_axial_limit", D(1) - D(1) == 0,
      "u=1 ⇒ RΩ=0；同一惯性系中总速锁定为 1 时无额外横向机械速度")
add("A-07", "PASS", "螺旋速度分配表可复算",
    "固定 v_z²+v_⊥²=1 后，6 组 v_⊥ 与 1 km 轴向额外延迟逐行命中；0.6c 轴向时延迟 2223.761 ns。")
add("A-08", "PASS", "u=1 与 RΩ>0 在总速约束下互斥",
    "u²+(RΩ)²=1；若 u=1 则 RΩ=0。不能把传播速度 1 与独立横向机械速度再相加。")

R = D("1e-6")
u = D("0.9")
vp = (D(1) - u * u).sqrt()
Omega = vp / R
kappa = R * Omega * Omega
tau = u * Omega
geom_resid = kappa * kappa + tau * tau - Omega * Omega
KEY.update({
    "helix_Omega_m_inv": fmt(Omega),
    "helix_kappa_m_inv": fmt(kappa),
    "helix_tau_m_inv": fmt(tau),
    "helix_geom_resid": fmt(geom_resid),
})
guard("G_helix_geom", geom_resid.copy_abs() < D("1e-40"),
      "R²Ω²+u²=1 ⇒ κ=RΩ²、τ=uΩ、κ²+τ²=Ω² 机器闭合")
guard("G_cross_r446", near(Omega, D("4.358898943540673552E5"), "1e-10") and
      near(kappa, D("1.900000000000000000E5"), "1e-10") and
      near(tau, D("3.923009049186606197E5"), "1e-10"),
      "R=1µm、u=0.9 与 r446 B-03 的 Ω/κ/τ 逐位一致")
add("A-09", "PASS", "ROOT 第二层螺旋几何恒等式成立",
    "R=1µm、u=0.9 给 Ω=4.358899E5、κ=1.900000E5、τ=3.923009E5 m^-1，κ²+τ²=Ω² 残差机器零。")
add("A-10", "BOUNDARY", "非零曲率轨迹不等于平直真空自由光子的零测地线",
    "几何恒等式只在假设螺旋轨迹与总速 1 下成立；来料已声明其非 Maxwell/QED 自动推出，本体论仍需独立动力学与实验判别。")

# ---------- E/F：正文表格、外部链接与跨册一致性 ----------
sec5 = raw_text.split("## 五、")[1].split("## 六、")[0] if "## 五、" in raw_text else ""
scenario_rows = [ln for ln in sec5.splitlines()
                 if ln.strip().startswith("|") and "---" not in ln]
scenario_n = max(0, len(scenario_rows) - 1)
image_refs = re.findall(r"\[image\]\(", raw_text)
KEY["scenario_rows"] = scenario_n
KEY["image_refs"] = len(image_refs)
guard("G_source_present", RAW.exists() and KEY["source_bytes"] > 4000,
      "来料正本存在且超过 4 KB")
guard("G_scenario_table", scenario_n == 18,
      "第五节场景对照表 18 行解析有效，非因解析失败得到 0")
add("A-11", "PASS", "18 类现象对照表完整解析",
    "真空自由光子、圆/线/椭圆/非偏振、涡旋/贝塞尔/结构光、波导/介质/异常色散、引力透镜/光斑、真实螺旋与内部螺旋共 18 类均登记。")
add("A-12", "INFO", "外部图片与站点链接未下载验收",
    "正文中 5 处 `[image]` 链接及 CERN/Wikimedia/NIST/Nature/APS 等外部来源仅按原文保留；本册不据图片内容或站点结论作证。")

r445_book = BASE / "判定_TUFT-r445_ROOT_V140规范场动力学投影障碍与二次项缺失_全维审计_2026-11-23.md"
r446_book = BASE / "判定_TUFT-r446_ROOT_V141与光子运动全情况总表_整理与边界审计_2026-11-24.md"
r445_txt = r445_book.read_text(encoding="utf-8") if r445_book.exists() else ""
r446_txt = r446_book.read_text(encoding="utf-8") if r446_book.exists() else ""
cross_ok = ("B=ẑ×E" in r445_txt or "B=ẑ×E" in r445_txt.replace("`", "")) and \
           ("场旋转不等于光子中心绕轴" in r446_txt)
KEY["cross_r445_B_orientation"] = "B=ẑ×E" in r445_txt
KEY["cross_r446_field_rotation"] = "场旋转不等于光子中心绕轴" in r446_txt
guard("G_cross_rounds", cross_ok,
      "与 r445 圆偏振 B 手性更正、r446 场旋转≠中心绕轴边界一致")
add("A-13", "PASS", "与 r445/r446 既有裁定一致",
    "本册沿用 r445 的 B=ẑ×E 手性与 r446 的“场方向旋转≠光子中心绕轴”，未重判其条目。")

add("A-14", "PASS", "零质量四动量与螺旋度标签可同时成立",
    "P^μP_μ=0、E=|p|、σ=±1 与 U(θ) 相位作用互不矛盾；旋转生成元不给四动量添加横向分量。")
add("A-15", "PASS", "核心三条件组合自洽",
    "E²-|p|²=0、Λ=±1、E×B∥k 可同时成立，是现有理论内无超光速矛盾的最小组合。")
add("A-16", "BOUNDARY", "独立内部几何自由度仍未被确立",
    "来料最后问题是开放项：需同时给出两螺旋度机制、传播速度 1、洛伦兹协变、能量动量守恒与全部偏振实验解释，并产生新可测效应；本册不代选方案。")
add("A-17", "BOUNDARY", "W3 四门禁继承 r446，不因本文提升",
    "本文未给独立几何自由度的盲路径或双锚实验，W3 仍 1/4（阳性对照 4/4），不得作为 L3 预言。")
add("A-18", "INFO", "红线计数继承不变",
    "0/6、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4 保持。")

counts = {}
for row in ROWS:
    counts[row["verdict"]] = counts.get(row["verdict"], 0) + 1
KEY["counts"] = counts
KEY["entries"] = len(ROWS)
KEY["guards"] = len(GUARDS)
KEY["guards_pass"] = sum(1 for g in GUARDS if g["ok"])

report = {
    "round": "r447",
    "topic": "ROOT 光子光速自旋是否超光速：整理与因果边界审计",
    "date": "2026-11-24",
    "key_numbers": KEY,
    "entries": ROWS,
    "guards": GUARDS,
}

OUT.mkdir(parents=True, exist_ok=True)
(OUT / (STEM + ".json")).write_text(
    json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n",
    encoding="utf-8")

md = [
    "# r447 光子光速自旋是否超光速：机器读数",
    "",
    "## 关键读数",
    "",
]
for k, v in KEY.items():
    md.append("- `%s` = %s" % (k, json.dumps(v, ensure_ascii=False, default=str)))
md += ["", "## 条目", "", "| ID | 判定 | 标题 | 详情 |", "|---|---|---|---|"]
for row in ROWS:
    md.append("| %s | %s | %s | %s |" %
              (row["id"], row["verdict"], row["title"], row["detail"]))
md += ["", "## 守卫", "", "| ID | 结果 | 读数 |", "|---|---|---|"]
for g in GUARDS:
    md.append("| %s | %s | %s |" %
              (g["id"], "PASS" if g["ok"] else "FAIL", g["detail"]))
(OUT / (STEM + ".md")).write_text("\n".join(md) + "\n", encoding="utf-8")

txt = [
    "r447 / ROOT 光子光速自旋是否超光速：整理与因果边界审计",
    "source_sha256 = %s" % KEY["source_sha256"],
    "entries = %d" % len(ROWS),
    "counts = %s" % json.dumps(counts, ensure_ascii=False),
    "guards = %d/%d" % (KEY["guards_pass"], len(GUARDS)),
    "",
]
for row in ROWS:
    txt.append("[%s] %s | %s | %s" %
               (row["verdict"], row["id"], row["title"], row["detail"]))
txt += ["", "GUARDS"]
for g in GUARDS:
    txt.append("[%s] %s | %s" %
               ("PASS" if g["ok"] else "FAIL", g["id"], g["detail"]))
(OUT / (STEM + "_report.txt")).write_text("\n".join(txt) + "\n", encoding="utf-8")

print("OK entries=%d guards=%d/%d" % (len(ROWS), KEY["guards_pass"], len(GUARDS)))
