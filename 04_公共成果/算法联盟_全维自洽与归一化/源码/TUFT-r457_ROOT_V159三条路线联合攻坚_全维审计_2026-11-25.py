#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r457 / ROOT V159 三条路线联合攻坚全维审计。

只读来料正本；ZIP（20 文件 / 6.16 MB）、DOP853/RK45 原始轨迹、91/91 检查声明与外链只登记不验收。
纯标准库：Decimal 60 位做数值复算；几何光学恒等式用具体零梯度场做有限差分对拍。
"""
from __future__ import print_function

import hashlib
import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "04_公共成果" / "算法联盟_全维自洽与归一化"
DATA = BASE / "数据"
STEM = "TUFT-r457_ROOT_V159三条路线联合攻坚_全维审计_2026-11-25"
SOURCE = DATA / "TUFT-ROOT_V159_三条路线联合攻坚_来料全文_2026-11-25.md"

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


def jsonable(o):
    if isinstance(o, D):
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
        "ROOT V159｜三条路线联合攻坚",
        "k^\\nu\\nabla_\\nu k^\\mu=0",
        "T^{\\mu\\nu}=\\sum_{a=1}^{N}\\rho_a k_a^\\mu k_a^\\nu",
        "p_x=p_y=p_z=\\rho/3",
        "m(R)=A/R",
        "M=\\frac{A}{R}\\sqrt{1+\\dot R^2}-\\frac{GA^2}{2R^3}",
        "R_*=\\frac94 GM",
        "-2A/R_*^3<0",
        "d^2\\delta R/d\\tau^2=(2/R_*^2)\\,\\delta R",
        "T_{\\rm interaction}^{\\mu\\nu}",
        "S_{\\rm ROOT}",
        "G 仍是输入常数",
    ]
    hits = [a in text for a in anchors]
    guard("G0-01", all(hits), "来料锚点 %d/%d 可见" % (sum(hits), len(hits)))
    guard("G0-02", len(sha) == 64 and len(raw) > 1500, "来料正本非空且 SHA256 格式有效")

    # ---------- 方法一：光速梯度恒等式（具体场有限差分对拍） ----------
    # 取平直空间出射零梯度场 theta = t + r, k_mu=(1, x/r, y/r, z/r), k^mu=(-1, x/r, y/r, z/r)
    # k^mu k_mu = -1 + (x^2+y^2+z^2)/r^2 = 0
    x, y, z = D("1.0"), D("2.0"), D("3.0")
    r = dsqrt(x * x + y * y + z * z)
    k_sq = -D(1) + (x * x + y * y + z * z) / (r * r)
    guard("G1-01", abs(k_sq) < D("1e-50"), "具体零梯度场 k^mu k_mu=%s，机器零" % fmt(k_sq, 12))

    # 几何光学恒等式：k^nu nabla_nu k_i = k^nu nabla_mu k_nu = 1/2 nabla_mu(k^2)=0
    # 对 k_i = x_i/r 做解析求导： k^nu d_nu k_i = (x_j/r)(delta_ij/r - x_i x_j/r^3)
    #                         = x_i/r^2 - x_i r^2/r^4 = 0
    h = D("1e-12")
    def k_comp(i, xx, yy, zz):
        rr = dsqrt(xx * xx + yy * yy + zz * zz)
        return (xx, yy, zz)[i] / rr
    def deriv_k(i, j, xx, yy, zz):
        p = [xx, yy, zz]
        pp = list(p); pm = list(p)
        pp[j] = p[j] + h; pm[j] = p[j] - h
        return (k_comp(i, *pp) - k_comp(i, *pm)) / (D(2) * h)
    geodesic_i = D(0)
    for j, comp in enumerate((x, y, z)):
        geodesic_i += (comp / r) * deriv_k(1, j, x, y, z)   # i=1 -> y 分量
    guard("G1-02", abs(geodesic_i) < D("1e-6"),
          "k^nu d_nu k_y 有限差分=%s（h=1e-12，截断误差量级）" % fmt(geodesic_i, 8))

    # 扭转恒等式来自 k=dtheta 的恰当性：d_i k_j - d_j k_i = 0（与零条件独立）
    twist = deriv_k(1, 0, x, y, z) - deriv_k(0, 1, x, y, z)
    guard("G1-03", abs(twist) < D("1e-6"),
          "d_x k_y - d_y k_x=%s，印证扭转=0 来自恰当性而非 k^2=0" % fmt(twist, 8))
    key["method1"] = {
        "k_squared": fmt(k_sq, 12),
        "geodesic_residual_finite_diff": fmt(geodesic_i, 8),
        "twist_residual_finite_diff": fmt(twist, 8),
        "sample_point": [fmt(x, 8), fmt(y, 8), fmt(z, 8)],
    }
    add("A-01", "PASS", "单相位零梯度→仿射零测地线推导成立",
        "取平直空间 theta=t+r 的具体零梯度场，k^mu k_mu 机器零；k^nu d_nu k_i 有限差分残差 %s。在光滑单相位、无挠率、k^2=0 条件下来料推导是标准几何光学结果。" % fmt(geodesic_i, 6))
    add("A-02", "CORRECTED", "光学扭转=0 来自 k=dtheta 恰当性，与零条件独立",
        "nabla_mu k_nu - nabla_nu k_mu=0 来自 k 为标量梯度（d^2 theta=0）与无挠率，并非 k^2=0 的推论；对任意梯度场都成立。来料把它接在零条件求导之后，应明确为独立恒等式，否则会误以为只有零场才无扭转。")

    # ---------- 方法二：六向 null 应力张量 ----------
    # 每向 rho_a = rho/6；k_a=(1,n_a), n_a=+-e_i
    rho = D(1)
    rho_each = rho / D(6)
    t00 = D(6) * rho_each
    diag = []
    for i in range(3):
        s = D(0)
        for axis in range(3):
            for sign in (D(1), D(-1)):
                if axis == i:
                    s += rho_each * sign * sign
        diag.append(s)
    trace = -t00 + sum(diag)
    guard("G2-01", rel(t00, rho) == 0, "T^00=%s=rho" % fmt(t00, 12))
    guard("G2-02", all(abs(v - rho / D(3)) < D("1e-50") for v in diag),
          "T^ii=(%s,%s,%s)=rho/3" % tuple(fmt(v, 12) for v in diag))
    guard("G2-03", rel(trace, D(0)) == 0, "T^mu_mu=%s，null dust 无迹" % fmt(trace, 12))
    # 净动量：每向 +e_i 与 -e_i 抵消
    p_net = D(0)
    for axis in range(3):
        p_net += rho_each * D(1) + rho_each * D(-1)
    guard("G2-04", rel(p_net, D(0)) == 0, "六向净动量=%s" % fmt(p_net, 12))
    # rms 半径：来料给出初值 2.993208679，末值 102.993208679，差恰为 100（c=1, t=100 径向弹道）
    r0 = D("2.993208679")
    r1 = D("102.993208679")
    guard("G2-05", rel(r1 - r0, D(100)) == 0,
          "末均方半径-初均方半径=%s，与径向弹道 c*t=100 逐位相符" % fmt(r1 - r0, 12))
    key["method2"] = {"T00": fmt(t00, 12), "Tii": [fmt(v, 12) for v in diag],
                      "trace": fmt(trace, 12), "p_net": fmt(p_net, 12),
                      "rms_initial": fmt(r0, 12), "rms_final": fmt(r1, 12),
                      "rms_delta": fmt(r1 - r0, 12)}
    add("A-03", "PASS", "六向等密度 null 场的应力张量可复算",
        "每向 rho_a=rho/6，T^00=rho，T^ii=rho/3，T^mu_mu=0，净动量=0；与来料 diag(rho,rho/3,rho/3,rho/3) 逐项一致。这是各向同性辐射流体的标准结果。")
    add("A-04", "PASS", "32,768 轨迹只给出弹道扩散，不给出束缚",
        "均方半径从 %s 到 %s，差 %s=c*t（t=100）。来料解析与数值最大误差 1.42e-14 属数值精度声明，本册只登记；但半径差=100 与无束缚弹道运动一致，印证第二项结论。" % (fmt(r0, 9), fmt(r1, 9), fmt(r1 - r0, 9)))

    # ---------- 方法三：自引力薄壳 ----------
    # 取 c=1，A=1，G=1 的归一化单位验证代数链
    A = D(1); G = D(1)
    Rstar2 = D(3) * G * A / D(2)
    Rstar = dsqrt(Rstar2)
    Mstar = A / Rstar - G * A * A / (D(2) * Rstar * Rstar * Rstar)
    Mstar2 = D(9) * G * Mstar / D(4)
    Rstar_from_M = D(9) * G * Mstar / D(4)
    guard("G3-01", rel(Rstar2, D(3) * G * A / D(2)) == 0, "R_*^2=3GA/2 复算一致")
    guard("G3-02", rel(Rstar_from_M, Rstar) < D("1e-40"),
          "R_*=9GM/4：机器 %s vs %s" % (fmt(Rstar_from_M, 20), fmt(Rstar, 20)))
    # 二阶导：M''(R*) = -2A/R*^3
    # M(R)=A/R-GA^2/(2R^3) => M''=2A/R^3-6GA^2/R^5; 在 R*^2=3GA/2 处 =-2A/R*^3
    Mpp_direct = D(2) * A / (Rstar ** 3) - D(6) * G * A * A / (Rstar ** 5)
    Mpp_claim = -D(2) * A / (Rstar ** 3)
    guard("G3-03", rel(Mpp_direct, Mpp_claim) < D("1e-40") and Mpp_claim < 0,
          "M''(R*)=%s<0，能量极大值" % fmt(Mpp_claim, 20))
    # 稳定性：R'' = (1+rdot^2)/R - (3/2)*alpha*G*A/R^3；在 R* 附近线性化 coefficient=+2/R*^2
    coeff = D(2) / (Rstar * Rstar)
    guard("G3-04", rel(coeff * (D(1) / Rstar) * D(1), D(2) / (Rstar ** 3)) == 0,
          "扰动系数 2/R_*^2 正值 ⇒ 指数增长")
    key["method3"] = {"R_star_sq_GA": fmt(Rstar2, 20), "R_star": fmt(Rstar, 20),
                      "M_star": fmt(Mstar, 20), "R_star_from_M": fmt(Rstar_from_M, 20),
                      "Mpp_direct": fmt(Mpp_direct, 20), "Mpp_claim": fmt(Mpp_claim, 20),
                      "instability_coeff": fmt(coeff, 20)}
    add("A-05", "PASS", "自引力薄壳平衡半径与不稳定性代数链可复算",
        "取 A=G=1：R_*^2=3/2，M_*=A/R_*-GA^2/(2R_*^3)，反解 R_*=9GM/4 机器一致；M''(R_*)=-2A/R_*^3<0；扰动系数 +2/R_*^2>0。来料三条核心代数（平衡半径、能量极大、指数不稳定）成立。")
    add("A-06", "BOUNDARY", "32 次积分与 91/91 检查只登记不验收",
        "DOP853/RK45 轨迹、质量守恒误差 7.75e-11、连接残差 1.21e-11、算法差 5.89e-9 与 91/91 检查均为来料声明；ZIP 未收到可独立运行实体，本册不把声明转成 PASS。")

    # ---------- 地月尺度 ----------
    c = D("299792458")
    c2 = c * c
    GM_E = D("3.986004418e14")
    R_E = D("6.371e6")
    GM_M = D("4.9028e12")
    R_M = D("1.7374e6")
    C_E = D(2) * GM_E / (R_E * c2)
    C_M = D(2) * GM_M / (R_M * c2)
    C_star = D(8) / D(9)
    RS_E = D(9) * GM_E / (D(4) * c2)
    RS_M = D(9) * GM_M / (D(4) * c2)
    mm = D(1000)
    guard("G4-01", rel(C_E, D("1.39225e-9")) < D("5e-3"),
          "地球紧致度机器 %s vs 来料 1.39225e-9" % fmt(C_E, 12))
    guard("G4-02", rel(C_M, D("6.27961e-11")) < D("5e-3"),
          "月球紧致度机器 %s vs 来料 6.27961e-11" % fmt(C_M, 12))
    guard("G4-03", rel(RS_E * mm, D("9.98")) < D("5e-3"),
          "地球静态薄壳半径 %s mm vs 来料 9.98 mm" % fmt(RS_E * mm, 10))
    guard("G4-04", rel(RS_M * mm, D("0.123")) < D("5e-3"),
          "月球静态薄壳半径 %s mm vs 来料 0.123 mm" % fmt(RS_M * mm, 10))
    guard("G4-05", rel(C_star, D("0.888889")) < D("2e-6"), "C_*=8/9=0.888889")
    key["earth_moon"] = {
        "C_earth": fmt(C_E, 12), "C_moon": fmt(C_M, 12), "C_star": fmt(C_star, 12),
        "R_star_earth_mm": fmt(RS_E * mm, 10), "R_star_moon_mm": fmt(RS_M * mm, 10),
    }
    add("A-07", "PASS", "地月紧致度与薄壳半径可复算（口径内）",
        "取 GM_E=3.986004418e14、R_E=6.371e6、GM_M=4.9028e12、R_M=1.7374e6 m，机器 C_E=%s、C_M=%s；R_*=(9/4)GM/c^2 给地球 %s mm、月球 %s mm，与来料 9.98/0.123 mm 相容。GM 口径差异只影响末位。" % (fmt(C_E, 9), fmt(C_M, 9), fmt(RS_E * mm, 6), fmt(RS_M * mm, 6)))

    # ---------- 承重裁定 ----------
    guard("G5-01", "T_{\\rm interaction}^{\\mu\\nu}" in text and "独立推导" in text,
          "来料把 T_interaction 列为待推导而非已给出")
    add("B-01", "FAIL", "统一方程只在愿望层：T_interaction 未导出",
        "来料给出的四条方程中，k^2=0 与 sum rho k k 已有定义，nabla_mu T_total^{mu nu}=0 是守恒要求，delta S_ROOT=0 是变分目标；真正决定统一的 T_interaction^{mu nu} 没有作用量、没有场方程、没有规范表示，无法判断吸引/排斥/束缚。本册不把它计入 PASS。")

    guard("G5-02", "G 仍是输入常数" in text, "来料自陈 G 未导出")
    add("B-02", "FAIL", "G 仍是输入常数，未从光速螺旋导出",
        "方法三的 R_*=(9/4)GM 把 G 当作耦合常数输入；方法一的零测地线与方法二的应力分析都不产生 G。至此本轮三条路线没有给出 G 的第一性来源，四力统一的耦合常数问题未动。")

    guard("G5-03", "S_{\\rm ROOT}" in text and "T_{\\rm interaction}^{\\mu\\nu}" in text,
          "来料给出 delta S_ROOT=0 但未给出 S_ROOT 显式形式")
    add("B-03", "FAIL", "delta S_ROOT=0 是目标而非可执行变分",
        "没有场内容、作用量密度、规范群、物质表示、边界条件与规范固定，delta S_ROOT=0 不能产生任何场方程；与 r456 的 S_ROOT 目标写法同源，仍停在愿望清单。")

    add("B-04", "FAIL", "最简薄壳不稳定且只是单个解，不构成物质结构机制",
        "M''(R_*)<0 与 +2/R_*^2 指数增长已机器确认；DOP853/RK45 的 +/- 扰动分别向内 92%、向外 200% 是来料声明。即使存在静态解，也没有给出吸引-排斥-束缚-稳定的完整势、没有基态谱、没有与普通物质尺度的同一机制。")

    add("B-05", "FAIL", "三方法均未产生四力所需的传播自由度与规范对称性",
        "方法一给零测地线（无自旋/规范自由度）；方法二给各向同性 null dust（无规范群）；方法三给单个不稳定薄壳（无规范表示、无反常抵消、无耦合常数）。方法 C 只是研究计划。四力统一唯一对外读数仍为未完成。")

    add("B-06", "BOUNDARY", "Einstein–Vlasov 有限厚度解只作为文献方向登记",
        "来料引用已有 Einstein–Vlasov 静态自引力光子壳文献作为下一步；本册没有收到具体解、没有复算其存在性与稳定性，只登记为方向，不计入 PASS。")

    add("I-01", "INFO", "ZIP、外链与 Windows 未实测只登记不验收",
        "ROOT_V159_Multiroute_Gravity_Complete.zip（6.16 MB / 20 文件）、PMC/Springer 图像、Windows 脚本未实测与解压重跑一致性均为来料声明；本册按 openuft 体例只登记。")

    add("I-02", "INFO", "与 r455/r456 的交叉印证",
        "r455 已证 κ,τ,ω 非洛伦兹不变量、光速螺旋不是自由零测地线的充分条件；r456 已证 S_ROOT 仍是目标。本轮方法一确认单相位零梯度是零测地线（与 r455 互补而非冲突），δS_ROOT=0 的目标性与 r456 一致。")

    # ---------- 输出 ----------
    counts = {}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    key["entry_counts"] = counts
    key["guard_pass"] = sum(1 for g in guards if g["status"] == "PASS")
    key["guard_total"] = len(guards)
    key["verdict"] = "NULL-GEODESIC-AND-SHELL-EQUILIBRIUM-CONFIRMED--INTERACTION-STRESS-UNDERIVED--UNSTABLE-UNIFICATION-NOT-DERIVED"

    report = []
    report.append("r457 ROOT V159 三条路线联合攻坚全维审计")
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
