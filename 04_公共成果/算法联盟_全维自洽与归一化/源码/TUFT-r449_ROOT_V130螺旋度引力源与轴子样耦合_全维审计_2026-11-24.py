#!/usr/bin/env python3
"""r449 / ROOT V130 螺旋度引力源与轴子样耦合全维审计。

边界：只审计本次 V130 来料要点，不与归档中 SU(5)/一圈 RG 主题 V130 混同。
输出：数据/TUFT-r449_ROOT_V130螺旋度引力源与轴子样耦合_全维审计_2026-11-24.{json,md,_report.txt}
"""
from __future__ import print_function

import hashlib
import json
import math
import sys
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 60

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "04_公共成果" / "算法联盟_全维自洽与归一化"
DATA = BASE / "数据"
STEM = "TUFT-r449_ROOT_V130螺旋度引力源与轴子样耦合_全维审计_2026-11-24"
SOURCE = DATA / "TUFT-ROOT_V130_螺旋度引力源与轴子样耦合_来料要点_2026-11-24.md"

D = Decimal
entries = []
guards = []
key_numbers = {}


def fmt(x):
    x = D(x)
    if x == 0:
        return "0"
    return format(x, ".15E")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def add(code, status, title, detail):
    entries.append({"id": code, "status": status, "title": title, "detail": detail})


def guard(code, ok, detail):
    guards.append({"id": code, "status": "PASS" if ok else "FAIL", "detail": detail})


def fvec(helicity, phase):
    c = math.cos(phase)
    s = math.sin(phase)
    E = (c, helicity * s, 0.0)
    B = (-helicity * s, c, 0.0)
    return E, B


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm2(a):
    return dot(a, a)


def max_diff(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def main():
    if not SOURCE.exists():
        print("MISSING SOURCE:", SOURCE)
        return 2

    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    sha = sha256_bytes(raw)
    key_numbers["source_sha256"] = sha
    key_numbers["source_bytes"] = len(raw)

    anchors = [
        "ROOT V130",
        "I1 = 2(B^2 - E^2) = 0",
        "I2 = -4 E·B = 0",
        "R/(16πG)",
        "θ F \\tilde F",
        "|Δβ| ≃ |η|/2 · |θ_obs - θ_emit|",
        "[Għ]=L²",
        "E⊥B",
        "T^ρ{}_{μν}",
    ]
    anchor_hits = [a in text for a in anchors]
    guard("G0-01", all(anchor_hits), "来料要点锚点 9/9 可见：%s" % sum(anchor_hits))
    guard("G0-02", len(sha) == 64 and len(raw) > 500, "来料正本非空且 SHA256 格式有效")

    add("S-01", "PASS", "来料身份独立登记",
        "本次 V130 主题为螺旋度—经典引力源—轴子样耦合；归档 V130 主题为 SU(5)/Spin(10) 与一圈 RG。两者同名不同题，按 r449 独立登记，未覆盖归档正本。")

    phases = [0.0, 0.37, 1.11, 2.03, 3.00, 4.51, 5.90]
    i1 = []
    i2 = []
    poynt = []
    stress_plus = []
    stress_minus = []
    for phase in phases:
        Ep, Bp = fvec(1, phase)
        Em, Bm = fvec(-1, phase)
        i1.append((2.0 * (norm2(Bp) - norm2(Ep)), 2.0 * (norm2(Bm) - norm2(Em))))
        i2.append((-4.0 * dot(Ep, Bp), -4.0 * dot(Em, Bm)))
        px = Ep[1] * Bp[2] - Ep[2] * Bp[1]
        py = Ep[2] * Bp[0] - Ep[0] * Bp[2]
        pz = Ep[0] * Bp[1] - Ep[1] * Bp[0]
        poynt.append((px, py, pz))

        def stress(E, B):
            e2 = norm2(E)
            b2 = norm2(B)
            half = 0.5 * (e2 + b2)
            return (
                -E[0] * E[0] - B[0] * B[0] + half,
                -E[1] * E[1] - B[1] * B[1] + half,
                -E[2] * E[2] - B[2] * B[2] + half,
                -E[0] * E[1] - B[0] * B[1],
                -E[0] * E[2] - B[0] * B[2],
                -E[1] * E[2] - B[1] * B[2],
            )

        stress_plus.append(stress(Ep, Bp))
        stress_minus.append(stress(Em, Bm))

    i1_res = max(max(abs(a), abs(b)) for a, b in i1)
    i2_res = max(max(abs(a), abs(b)) for a, b in i2)
    poynt_min = min(v[2] for v in poynt)
    poynt_trans = max(max(abs(v[0]), abs(v[1])) for v in poynt)
    stress_res = max(max_diff(a, b) for a, b in zip(stress_plus, stress_minus))

    key_numbers["i1_max_residual"] = i1_res
    key_numbers["i2_max_residual"] = i2_res
    key_numbers["pz_min"] = poynt_min
    key_numbers["transverse_poynting_max"] = poynt_trans
    key_numbers["stress_helicity_flip_max_residual"] = stress_res

    guard("G1-01", i1_res < 1e-12, "I1=2(B²−E²) 在 7 个相位、两螺旋度下残差 ≤ %s" % fmt(D(str(i1_res))))
    guard("G1-02", i2_res < 1e-12, "I2=−4E·B 在 7 个相位、两螺旋度下残差 ≤ %s" % fmt(D(str(i2_res))))
    guard("G1-03", poynt_min > 0.999999999 and poynt_trans < 1e-12,
          "坡印廷矢量横向分量为零、纵向分量恒正（min=%s）" % fmt(D(str(poynt_min))))
    guard("G1-04", stress_res < 1e-12,
          "T_mu_nu 对螺旋度翻转 max|Δ|=%s" % fmt(D(str(stress_res))))

    add("A-01", "PASS", "反向螺旋度不改变两个平面波不变量",
        "取 k沿z、E=(cosφ,s·sinφ,0)、B=k̂×E=(-s·sinφ,cosφ,0)，s=±1。7 个相位下 I1 与 I2 最大残差分别 ≤ %s、%s。" %
        (fmt(D(str(i1_res))), fmt(D(str(i2_res)))))
    add("A-02", "PASS", "经典应力—能量张量对螺旋度翻转不变",
        "同一代表族下 T^{ij}=-EiEj-BiBj+½δij(E²+B²)，两螺旋度 6 个独立分量最大差 %s；E×B 横向分量 ≤ %s、纵向 min=%s。" %
        (fmt(D(str(stress_res))), fmt(D(str(poynt_trans))), fmt(D(str(poynt_min)))))
    add("A-03", "BOUNDARY", "结论适用域限于自由真空平面波或均匀背景",
        "若 θ 为空间依赖的动态场，光子传播与有效耦合可随 θ 梯度/背景改变；“螺旋度不改源”不能直接外推到非均匀轴子背景或近场。")

    scalar_terms = [
        ("EH", "R/(16πG)", "曲率标量，坐标标量密度意义下协变"),
        ("Maxwell", "-F²/4", "规范不变"),
        ("theta", "-(η/4) θ F Ftilde", "θ 取标量时可由协变量构造；η 动力学未给出"),
        ("rest", "L_SM,rest", "外部容器，未展开强/弱扇区"),
    ]
    guard("G2-01", len(scalar_terms) == 4 and all(len(x) == 3 for x in scalar_terms),
          "候选作用量四类项已拆项登记")
    add("B-01", "BOUNDARY", "候选作用量项为已知协变/规范不变构件",
        "EH、Maxwell、θF\\tilde F 均可写成协变/规范不变形式；但 η 的来源、θ 的势与正规化、L_SM,rest 的具体内容均未由 ROOT 推出。")
    add("B-02", "BOUNDARY", "Euler–Lagrange 方程只给已知形式的扩展",
        "对 A_μ 变分预期出现 ∇_μF^{μν} 与 η(∇_μθ)\\tilde F^{μν} 型源；对 θ 变分预期出现 F\\tilde F 与 V'(θ)。符号与系数依赖作用量号规，未在来料中完全固定。")

    eta_theta_pairs = [(D("1"), D("0.001")), (D("2"), D("0.0005")), (D("0.5"), D("0.002"))]
    beta_rows = []
    for eta, dtheta in eta_theta_pairs:
        beta_rows.append({"eta": str(eta), "delta_theta": str(dtheta),
                          "abs_delta_beta": fmt(eta * dtheta / D(2))})
    beta_values = [r["abs_delta_beta"] for r in beta_rows]
    key_numbers["delta_beta_degenerate_rows"] = beta_rows
    guard("G3-01", len(set(beta_values)) == 1, "η·Δθ 三组不同参数给同一 |Δβ|，不可单独辨识")
    add("C-01", "FAIL", "偏振旋转量存在参数简并",
        "|Δβ| ≃ |η|/2·|Δθ| 只约束乘积 ηΔθ；三组 (η,Δθ)=(1,0.001),(2,0.0005),(0.5,0.002) 均给 |Δβ|=%s。" % beta_values[0])
    add("C-02", "FAIL", "尚无独立、唯一的 ROOT 预言",
        "要形成可证伪预言，必须另行给出 η 的第一性数值、θ_obs−θ_emit 的独立模型或观测输入，以及区别于标准轴子样模型的唯一信号；来料未给出。")

    dim_hbar = (1, 1, 0)   # M,L,T: [hbar]=M L
    dim_G = (-1, 1, 0)     # [G]=L/M
    dim_hbarG = tuple(dim_hbar[i] + dim_G[i] for i in range(3))
    guard("G4-01", dim_hbarG == (0, 2, 0), "[ħ][G]=L² 与来料记号一致")
    guard("G4-02", dim_hbarG[0] == 0 and dim_hbarG[1] == 2 and dim_hbarG[2] == 0,
          "量纲向量逐分量为 (M0,L2,T0)")
    add("D-01", "PASS", "c=1 记号下的量纲关系自洽",
        "[ħ]=ML、[G]=L/M，因此 [Għ]=L²，√[Għ]=L；量纲层面与 ℓ_P 的长度维一致。")
    add("D-02", "FAIL", "ℓ_P 定义不构成 G 的独立推导",
        "由 ℓ_P=√(Għ) 反解 G=ℓ_P²/ħ 仍输入 ħ；该关系是定义/换算，不是从螺旋几何独立推出牛顿常数。")

    E_bad = (D(1), D(1), D(0))
    B_bad = (D(1), D(0), D(0))
    e_dot_b_bad = sum((a * b for a, b in zip(E_bad, B_bad)), D(0))
    guard("G5-01", e_dot_b_bad == D(1), "非平面波反例 E·B=1，证明 E⊥B 非普遍公理")
    add("E-01", "BOUNDARY", "E⊥B 的使用需限定自由真空平面波",
        "对来料代表族 E⊥B 成立；但取静态均匀场 E=(1,1,0)、B=(1,0,0) 得 E·B=1，故 E⊥B 不是 Maxwell 场的普遍性质。")

    add("F-01", "FAIL", "Frenet 挠率不可直接等同时空挠率",
        "曲线 Frenet 挠率 τ 描述曲线副法向转动，时空挠率 T^ρ{}_{μν} 是联络反对称部分；仅量纲同为 L⁻¹ 不构成同一对象。")
    add("F-02", "PASS", "保持两者分列时边界清晰",
        "若把 τ 仅用于光子几何轨迹、把 T^ρ{}_{μν} 仅用于 EC/Poincaré 联络，则不产生对象混用；但这同时意味着尚未获得统一机制。")

    add("G-01", "FAIL", "强/弱相互作用仍封存在 L_SM,rest",
        "候选作用量显式含引力与电磁及 θ 耦合；强、弱扇区只由 L_SM,rest 外部承接，未给出从空间/螺旋/曲率/挠率推出其规范群、表示与耦合的过程。")
    add("G-02", "FAIL", "四力统一验收未通过",
        "本册满足“螺旋度翻转不改经典 Maxwell 源”这一局部判据，但没有新增四力共同作用量、独立耦合派生或可证伪数值预言；W3/四力红线不因此改变。")

    status_counts = {}
    for e in entries:
        status_counts[e["status"]] = status_counts.get(e["status"], 0) + 1
    key_numbers["entries"] = len(entries)
    key_numbers["status_counts"] = status_counts
    key_numbers["guards"] = len(guards)
    key_numbers["guards_pass"] = sum(1 for g in guards if g["status"] == "PASS")

    lines = []
    lines.append("# TUFT r449 / ROOT V130 螺旋度引力源与轴子样耦合全维审计")
    lines.append("")
    lines.append("## 一、总览")
    lines.append("")
    lines.append("来料要点 SHA256：`%s`" % sha)
    lines.append("")
    lines.append("条目 %d：%s" % (len(entries), " / ".join("%s=%d" % (k, v) for k, v in sorted(status_counts.items()))))
    lines.append("")
    lines.append("守卫 %d/%d PASS。" % (key_numbers["guards_pass"], len(guards)))
    lines.append("")
    lines.append("## 二、条目")
    lines.append("")
    for e in entries:
        lines.append("- **%s [%s]** %s：%s" % (e["id"], e["status"], e["title"], e["detail"]))
    lines.append("")
    lines.append("## 三、守卫")
    lines.append("")
    for g in guards:
        lines.append("- %s %s：%s" % (g["id"], g["status"], g["detail"]))
    lines.append("")
    lines.append("## 四、机器读数")
    lines.append("")
    lines.append("- I1 max residual = %s" % fmt(D(str(i1_res))))
    lines.append("- I2 max residual = %s" % fmt(D(str(i2_res))))
    lines.append("- Poynting transverse max = %s" % fmt(D(str(poynt_trans))))
    lines.append("- Poynting z min = %s" % fmt(D(str(poynt_min))))
    lines.append("- stress helicity-flip max residual = %s" % fmt(D(str(stress_res))))
    lines.append("")
    lines.append("## 五、红线")
    lines.append("")
    lines.append("数学/数值自洽不等于物理证实。本册只审计来料要点；不改归档 V130，不覆盖并行 r448，不推进四力统一红线。")
    lines.append("")

    md_path = DATA / (STEM + ".md")
    json_path = DATA / (STEM + ".json")
    report_path = DATA / (STEM + "_report.txt")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    payload = {
        "round": "r449",
        "topic": "ROOT V130 螺旋度引力源与轴子样耦合",
        "date": "2026-11-24",
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": sha,
        "entries": entries,
        "guards": guards,
        "key_numbers": key_numbers,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_lines = [
        "OK entries=%d guards=%d/%d" % (len(entries), key_numbers["guards_pass"], len(guards)),
        "source_sha256=%s" % sha,
        "I1_max=%s I2_max=%s stress_flip_max=%s" % (fmt(D(str(i1_res))), fmt(D(str(i2_res))), fmt(D(str(stress_res)))),
        "status=%s" % json.dumps(status_counts, ensure_ascii=False, sort_keys=True),
    ]
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("OK entries=%d guards=%d/%d" % (len(entries), key_numbers["guards_pass"], len(guards)))
    print("source_sha256=%s" % sha)
    print("outputs=%s" % STEM)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("ERROR", type(exc).__name__, str(exc))
        sys.exit(1)
