#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r456 / ROOT V149 深层攻破审计：精细结构常数、h 与光速螺旋。

只读来料正本；ZIP、外链、66+12 测试与 55 位交叉计算声明只登记不验收。
纯标准库：Decimal 60 位做数值复算，Fraction 四元组量纲 (M,L,T,Q) 做 h 可达性判据。
"""
from __future__ import print_function

import hashlib
import json
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "04_公共成果" / "算法联盟_全维自洽与归一化"
DATA = BASE / "数据"
STEM = "TUFT-r456_ROOT_V149精细结构常数与光速螺旋_深层攻破_全维审计_2026-11-24"
SOURCE = DATA / "TUFT-ROOT_V149_精细结构常数与光速螺旋的高精度审计_来料全文_2026-11-24.md"

D = Decimal
entries = []
guards = []
key = {}


def fmt(x, digits="18"):
    x = D(x)
    if x == 0:
        return "0"
    return format(x, "." + str(digits) + "E")


def rel(a, b):
    a, b = D(a), D(b)
    return abs(a - b) / max(abs(a), abs(b), D("1e-80"))


def dsqrt(x):
    x = D(x)
    if x < 0:
        raise ValueError("sqrt of negative Decimal")
    return (x.ln() / D(2)).exp()


def add(code, status, title, detail):
    entries.append({"id": code, "status": status, "title": title, "detail": detail})


def guard(code, ok, detail):
    guards.append({"id": code, "status": "PASS" if ok else "FAIL", "detail": detail})


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dscale(k, a):
    return tuple(k * x for x in a)


def dim_product(terms):
    out = (0, 0, 0, 0)
    for base, power in terms:
        out = dadd(out, dscale(power, base))
    return out


def jsonable(o):
    if isinstance(o, Fraction):
        return [o.numerator, o.denominator]
    if isinstance(o, Decimal):
        return fmt(o, 30)
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    return o


def main():
    if not SOURCE.exists():
        print("MISSING SOURCE:", SOURCE)
        return 2
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    sha = hashlib.sha256(raw).hexdigest()
    key["source_sha256"] = sha
    key["source_bytes"] = len(raw)

    anchors = [
        "ROOT V149｜精细结构常数与光速螺旋的高精度审计",
        "h\\ \\text{是否与空间光速螺旋的曲率、挠率有关？}",
        "\\alpha\\ \\text{能否由曲率、挠率和角速度独立推导？}",
        "\\alpha_{\\rm guess}=\\frac{\\kappa^2}{\\kappa^2+\\tau^2}",
        "\\alpha_{\\rm guess}=(a\\omega)^2",
        "\\alpha_{\\rm guess}'=1",
        "\\alpha_G=\\frac{Gm_e^2}{\\hbar c}",
        "S_{\\rm ROOT}[\\Psi,g_{\\mu\\nu}]",
        "四力统一仍然没有获得完整证明",
        "全维整理写进openuft",
    ]
    hits = [a in text for a in anchors]
    guard("G0-01", all(hits), "来料锚点 %d/%d 可见" % (sum(hits), len(hits)))
    guard("G0-02", len(sha) == 64 and len(raw) > 800, "来料正本非空且 SHA256 格式有效")

    # ---------- CODATA 与候选公式复算 ----------
    alpha = D("0.0072973525643")
    alpha_inv = D(1) / alpha
    alpha_inv_claim = D("137.035999177")
    guard("G1-01", rel(alpha_inv, alpha_inv_claim) < D("1e-9"),
          "alpha^{-1}=%s，与来料 137.035999177 在 1e-9 相对阈值内一致" % fmt(alpha_inv, 15))
    key["alpha"] = fmt(alpha, 25)
    key["alpha_inverse"] = fmt(alpha_inv, 25)
    add("A-01", "PASS", "CODATA α 与 α^{-1} 可复算",
        "取 α=0.0072973525643，机器反演 α^{-1}=%s；与来料 137.035999177 相容。该条只确认常数口径，不确认几何推导。" % fmt(alpha_inv, 18))

    # 理想螺旋 boost 反例：a=0.6, omega=1, u=0.8, beta=u。
    a = D("0.6")
    omega = D(1)
    u = D("0.8")
    beta = u
    gamma = D(1) / dsqrt(D(1) - beta * beta)
    fac = gamma * (D(1) - beta * u)
    omega_p = omega / fac
    u_p = (u - beta) / (D(1) - beta * u)
    kappa = a * omega * omega
    tau = u * omega
    kappa_p = a * omega_p * omega_p
    tau_p = u_p * omega_p
    guess = kappa * kappa / (kappa * kappa + tau * tau)
    guess_p = D(1) if tau_p == 0 else kappa_p * kappa_p / (kappa_p * kappa_p + tau_p * tau_p)
    guard("G1-02", rel(kappa, D("0.6")) == 0 and rel(tau, D("0.8")) == 0,
          "原系 κ=0.6、τ=0.8 复算成功")
    guard("G1-03", rel(fac, D("0.6")) < D("1e-50") and rel(omega_p, D(5) / D(3)) < D("1e-50"),
          "β=u=0.8 时 boost 因子 D=0.6、ω'=5/3")
    guard("G1-04", rel(tau_p, D(0)) == 0 and rel(guess_p, D(1)) == 0,
          "boost 后 τ'=0，α_guess'=1")
    guard("G1-05", rel(guess, D("0.36")) == 0 and rel(guess_p - guess, D("0.64")) == 0,
          "同一对象 α_guess 从 0.36 跳到 1，差 0.64")
    key["helix_boost"] = {
        "a": fmt(a, 18), "omega": fmt(omega, 18), "u": fmt(u, 18),
        "boost_factor": fmt(fac, 25), "omega_prime": fmt(omega_p, 25),
        "u_prime": fmt(u_p, 18), "kappa": fmt(kappa, 18), "tau": fmt(tau, 18),
        "kappa_prime": fmt(kappa_p, 25), "tau_prime": fmt(tau_p, 18),
        "alpha_guess": fmt(guess, 18), "alpha_guess_prime": fmt(guess_p, 18),
    }
    add("A-02", "PASS", "候选式 κ²/(κ²+τ²) 与轴向 boost 反例可复算",
        "示例 a=0.6、ω=1、u=0.8、β=u 给 D=0.6、ω'=5/3、u'=0、κ'=5/3、τ'=0；候选式从 0.36 跳为 1，来料反例成立。")

    # α_G 与量级差。
    G = D("6.67430e-11")
    m_e = D("9.1093837139e-31")
    hbar = D("1.054571817e-34")
    c = D("299792458")
    alpha_g = G * m_e * m_e / (hbar * c)
    ratio = alpha / alpha_g
    guard("G1-06", D("1e-46") < alpha_g < D("1e-44"),
          "alpha_G=%s 落在 1e-46~1e-44" % fmt(alpha_g, 18))
    guard("G1-07", D("1e42") < ratio < D("1e43"),
          "alpha/alpha_G=%s 落在 1e42~1e43" % fmt(ratio, 18))
    key["alpha_G_electron"] = fmt(alpha_g, 25)
    key["alpha_over_alpha_G"] = fmt(ratio, 25)
    add("A-03", "PASS", "电子引力耦合 α_G 与 10^42 量级差可复算",
        "取 CODATA/2018 常用口径 G、m_e、ℏ、c，机器给 α_G=%s，α/α_G=%s；量级差承重。" % (fmt(alpha_g, 15), fmt(ratio, 15)))

    # 量纲：κ,τ ~ L^-1；ω ~ T^-1；a ~ L；只有这些变量无法生成 h 的 M^1 L^2 T^-1。
    DIM = {
        "kappa": (0, -1, 0, 0),
        "tau": (0, -1, 0, 0),
        "omega": (0, 0, -1, 0),
        "a": (0, 1, 0, 0),
        "c": (0, 1, -1, 0),
        "hbar": (1, 2, -1, 0),
        "h": (1, 2, -1, 0),
    }
    geom = [DIM[k] for k in ("kappa", "tau", "omega", "a", "c")]
    mass_powers = [d[0] for d in geom]
    guard("G1-08", all(p == 0 for p in mass_powers),
          "κ/τ/ω/a/c 的质量维均为 0，任意幂乘积质量维恒为 0")
    guard("G1-09", DIM["h"][0] == 1 and DIM["hbar"][0] == 1,
          "h 与 ℏ 的质量维为 1，几何基组不可达")
    dim_guess1 = dim_product([(DIM["kappa"], 2), (dadd(DIM["kappa"], DIM["kappa"]), -1)])
    dim_guess2 = dim_product([(DIM["a"], 2), (DIM["omega"], 2), (DIM["c"], -2)])
    guard("G1-10", dim_guess1 == (0, 0, 0, 0) and dim_guess2 == (0, 0, 0, 0),
          "κ²/(κ²+τ²) 与 SI 口径 (aω/c)²（自然单位写作 (aω)²）均为无量纲，不能等同于 h")
    key["dimensions"] = {k: list(v) for k, v in DIM.items()}
    add("A-04", "PASS", "h 的几何不可达性由量纲机器判定",
        "κ、τ 为 L^-1，ω 为 T^-1，a 为 L，c 为 LT^-1，质量维全为 0；κ²/(κ²+τ²) 与 SI 口径 (aω/c)² 均无量纲，h/ℏ 的质量维为 1。仅用几何/运动学变量无法生成 h，必须外加质量或作用量标度。")

    # 圆偏振不变量：Maxwell 平面波标准结果。
    E0 = D(1)
    dot = E0 * D(0) + D(0) * E0
    cross_z = E0 * E0
    guard("G1-11", dot == 0 and cross_z == 1, "圆偏振代表场 E·B=0、E×B=E0² z")
    add("A-05", "PASS", "圆偏振 Maxwell 不变量可复算",
        "取 E=E0(cosφ,sinφ,0)、B=E0(-sinφ,cosφ,0)，则 E·B=0、E×B=E0² z；这是标准平面波结果。")

    # ---------- 深层攻破 ----------
    guard("G2-01", "不是洛伦兹不变量" in text, "来料承认 κ/τ/ω/a 非洛伦兹不变量")
    add("B-01", "FAIL", "α_guess 不构成洛伦兹不变量公式",
        "α_guess=κ²/(κ²+τ²) 使用参考系相关的 Frenet 量。沿轴 boost 到 u'=0 时 τ'=0，公式给 1；同一物理态给出不同 α_guess。α 的不变性要求公式必须由作用量与协变场构造，不能由某系曲线参数直接拼装。")

    guard("G2-02", dim_guess2 == (0, 0, 0, 0), "(aω)^2 无量纲，未固定 a 与 ω")
    add("B-02", "FAIL", "(aω)² 只是在选择 aω≈√α 后重述结果",
        "aω 可随螺旋半径和角速度连续重标；来料未给出 a 与 ω 的场方程或选择原理。把 (aω)² 调等于 α 是拟合，不是从几何独立推导 α。")

    guard("G2-03", DIM["h"] != dim_product([(DIM["kappa"], 1), (DIM["tau"], 1)]),
          "κ·τ 的量纲不等于 h")
    add("B-03", "FAIL", "h 与 κ、τ 的“关系”缺少作用量层级定义",
        "h 是作用量量子，量纲 ML²T^-1；κ、τ 是曲线几何量，量纲 L^-1。没有质量/作用量标度、正则动量或 Noether 结构时，h 与 κ、τ 之间没有可定义映射。")

    guard("G2-04", ratio > D("1e42"), "α 与 α_G 相差超过 42 个数量级")
    add("B-04", "FAIL", "α 与 α_G 的量级桥接需要外部质量标度",
        "α_G=Gm_e²/(ℏc)=%s，α/α_G=%s；两者相差约 42 个数量级。要从电子引力耦合得到 α，必须引入 m_e、m_P 或某新标度的选择规则；来料未给出。" % (fmt(alpha_g, 15), fmt(ratio, 15)))

    guard("G2-05", dot == 0 and "圆偏振" in text, "来料含圆偏振段且不变量复算正确")
    add("B-05", "FAIL", "圆偏振解不证明空间路径具有物理螺旋",
        "E·B=0 与 E×B≠0 只说明圆偏振平面波具有旋向与能流；场的偏振相位不等同于点粒子或空间介质中的一条 Frenet 螺旋轨迹。由 Maxwell 解不能反推光沿螺旋路径传播。")

    guard("G2-06", "S_{\\rm ROOT}[\\Psi,g_{\\mu\\nu}]" in text and "没有给出该作用量" in text,
          "来料给出 S_ROOT 目标写法但未给出显式作用量")
    add("B-06", "BOUNDARY", "S_ROOT[Ψ,g] 仍是目标而非已构造作用量",
        "文本只写出目标箭头：由 S_ROOT 得到引力、规范场、物质与耦合。没有给出场内容、对称群、作用量密度、变分方程、边界条件与规范固定；因此不能据此判定四力统一。")

    guard("G2-07", "四力统一仍然没有获得完整证明" in text, "来料自陈四力统一未完成")
    add("B-07", "FAIL", "V149 排除简单公式，但没有生成统一动力学",
        "本轮能确认的是负结果：简单 α_guess 不协变、h 不可由几何量直接生成、α 与 α_G 桥接缺标度、圆偏振不代表空间轨迹。正向结果需要显式作用量与可证伪预言，当前未提供。")

    add("I-01", "INFO", "ZIP、66+12 测试、55 位交叉计算与外链只登记不验收",
        "来料声明存在 ZIP、66+12 测试、55 位交叉计算与外部 NIST 链接；本册未收到可独立运行的实体与源码，按 openuft 体例只登记声明，不把声明转成 PASS。")

    # ---------- 输出 ----------
    counts = {}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    key["entry_counts"] = counts
    key["guard_pass"] = sum(1 for g in guards if g["status"] == "PASS")
    key["guard_total"] = len(guards)
    key["verdict"] = "ALPHA-GEOMETRY-GUESS-REFUTED--COVARIANCE-BLOCKED--H-ACTION-SCALE-REQUIRED--UNIFICATION-NOT-DERIVED"

    report = []
    report.append("r456 ROOT V149 深层攻破全维审计")
    report.append("source_sha256=%s" % sha)
    report.append("entries=%d guards=%d/%d" % (len(entries), key["guard_pass"], key["guard_total"]))
    for e in entries:
        report.append("%s\t%s\t%s" % (e["id"], e["status"], e["title"]))
    report.append("VERDICT=%s" % key["verdict"])

    lines = []
    lines.append("# " + STEM.replace("_", " "))
    lines.append("")
    lines.append("- 来料 SHA256：`%s`" % sha)
    lines.append("- 裁定：`%s`" % key["verdict"])
    lines.append("- 条目：%d；守卫：%d/%d" % (len(entries), key["guard_pass"], key["guard_total"]))
    lines.append("")
    lines.append("| ID | 状态 | 标题 | 摘要 |")
    lines.append("|---|---|---|---|")
    for e in entries:
        lines.append("| %s | %s | %s | %s |" % (e["id"], e["status"], e["title"], e["detail"].replace("|", "\\|")))
    lines.append("")
    lines.append("## 关键读数")
    for k in sorted(key.keys()):
        lines.append("- `%s`: `%s`" % (k, json.dumps(jsonable(key[k]), ensure_ascii=False, sort_keys=True)))
    lines.append("")

    (DATA / (STEM + ".json")).write_text(
        json.dumps({"stem": STEM, "source_sha256": sha, "entries": entries,
                    "guards": guards, "key_numbers": key},
                   ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    (DATA / (STEM + ".md")).write_text("\n".join(lines), encoding="utf-8")
    (DATA / (STEM + "_report.txt")).write_text("\n".join(report) + "\n", encoding="utf-8")

    print("ENTRIES=%d" % len(entries))
    print("COUNTS=%s" % json.dumps(counts, ensure_ascii=False, sort_keys=True))
    print("GUARDS=%d/%d" % (key["guard_pass"], key["guard_total"]))
    print("VERDICT=%s" % key["verdict"])
    ok = all(g["status"] == "PASS" for g in guards)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
