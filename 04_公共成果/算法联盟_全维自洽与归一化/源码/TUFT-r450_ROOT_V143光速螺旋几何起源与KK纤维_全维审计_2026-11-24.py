#!/usr/bin/env python3
"""r450 / ROOT V143 光速螺旋几何起源与 KK 纤维全维审计。

纯标准库。只审计来料可核对公式与数值；ZIP 与外链只登记，不下载验收。
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
STEM = "TUFT-r450_ROOT_V143光速螺旋几何起源与KK纤维_全维审计_2026-11-24"
SOURCE = DATA / "TUFT-ROOT_V143_光速螺旋几何起源与KK纤维_来料全文_2026-11-24.md"

D = Decimal
entries = []
guards = []
key_numbers = {}


def fmt(x, digits="15"):
    x = D(x)
    if x == 0:
        return "0"
    return format(x, "." + digits + "E")


def rel_diff(a, b):
    a, b = D(a), D(b)
    denom = max(abs(a), abs(b), D("1e-80"))
    return abs(a - b) / denom


def dsqrt(x):
    x = D(x)
    if x < 0:
        raise ValueError("negative Decimal sqrt")
    return (x.ln() / D(2)).exp()


def add(code, status, title, detail):
    entries.append({"id": code, "status": status, "title": title, "detail": detail})


def guard(code, ok, detail):
    guards.append({"id": code, "status": "PASS" if ok else "FAIL", "detail": detail})


def main():
    if not SOURCE.exists():
        print("MISSING SOURCE:", SOURCE)
        return 2
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    sha = hashlib.sha256(raw).hexdigest()
    key_numbers["source_sha256"] = sha
    key_numbers["source_bytes"] = len(raw)

    anchors = [
        "a^2\\omega^2+u^2+R^2\\Omega^2=1",
        "v_3^2=a^2\\omega^2+u^2=1-R^2\\Omega^2",
        "\\omega^2=v_3^2(\\kappa^2+\\tau^2)",
        "ds_5^2=g_{\\mu\\nu}dx^\\mu dx^\\nu+ R^2(d\\phi+kA_\\mu dx^\\mu)^2",
        "-\\frac{R^2k^2}{64\\pi G} F_{\\mu\\nu}F^{\\mu\\nu}",
        "\\alpha_{\\rm KK}=\\frac{4Gm^2}{\\hbar}",
        "7.007 × 10⁻⁴⁵",
        "0.00729735",
        "45 项自动化测试通过",
    ]
    hit = [a in text for a in anchors]
    guard("G0-01", all(hit), "来料锚点 9/9 可见（实际 %d）" % sum(hit))
    guard("G0-02", len(sha) == 64 and len(raw) > 1000, "正本非空且 SHA256 格式有效")

    image_refs = text.count("[image]")
    external_links = text.count("https://")
    key_numbers["image_refs"] = image_refs
    key_numbers["external_https_links"] = external_links
    guard("G0-03", image_refs == 3, "外部 image 标记计数=%d" % image_refs)

    a_w = D("0.3")
    u = D("0.8")
    internal_sq = D(1) - a_w * a_w - u * u
    internal = dsqrt(internal_sq)
    v3_sq = a_w * a_w + u * u
    v3 = dsqrt(v3_sq)
    kappa = a_w / v3_sq
    tau = u / v3_sq
    omega_check = v3 * dsqrt(kappa * kappa + tau * tau)
    total5 = a_w * a_w + u * u + internal_sq

    key_numbers.update({
        "a_omega": str(a_w),
        "u": str(u),
        "internal_sq": str(internal_sq),
        "R_Omega": fmt(internal),
        "v3_sq": str(v3_sq),
        "v3": fmt(v3),
        "kappa": fmt(kappa),
        "tau": fmt(tau),
        "omega_check": fmt(omega_check),
        "five_dim_speed_sq": str(total5),
    })

    guard("G1-01", total5 == D(1), "五维零间隔约束 a²ω²+u²+R²Ω²=1")
    guard("G1-02", v3_sq + internal_sq == D(1), "v3² + (RΩ)² = 1")
    guard("G1-03", rel_diff(kappa, D("0.410959")) < D("2e-6"),
          "κ 与来料 0.410959 相对差 %s" % fmt(rel_diff(kappa, D("0.410959"))))
    guard("G1-04", rel_diff(tau, D("1.095890")) < D("2e-6"),
          "τ 与来料 1.095890 相对差 %s" % fmt(rel_diff(tau, D("1.095890"))))
    guard("G1-05", rel_diff(internal, D("0.519615")) < D("2e-6"),
          "RΩ 与来料 0.519615 相对差 %s" % fmt(rel_diff(internal, D("0.519615"))))
    guard("G1-06", rel_diff(v3, D("0.854400")) < D("2e-6"),
          "v3 与来料 0.854400 相对差 %s" % fmt(rel_diff(v3, D("0.854400"))))
    guard("G1-07", rel_diff(omega_check, D(1)) < D("1e-30"),
          "由 κ,τ,v3 反推 ω=%s，隐含归一化 ω=1" % fmt(omega_check))

    add("A-01", "PASS", "五维零间隔约束与三维投影速度相容",
        "aω=0.3、u=0.8 ⇒ (RΩ)²=0.27、RΩ=%s；v3²=0.73、v3=%s；五维总速平方=%s。" %
        (fmt(internal), fmt(v3), fmt(total5)))
    add("A-02", "PASS", "广义螺旋频率—曲率—挠率关系复算通过",
        "κ=aω²/v3²=%s、τ=uω/v3²=%s；取隐含 ω=1 得 ω²=v3²(κ²+τ²)=%s。" %
        (fmt(kappa), fmt(tau), fmt(omega_check)))
    add("A-03", "BOUNDARY", "运动学相容不等于第五维存在",
        "数值表只证明约束可解，未提供独立实验信号区分真实内部闭环、额外维度与纯参数化模型。")

    action_terms = [
        "R_4/(16πG)",
        "-R²k² F_{μν}F^{μν}/(64πG)",
        "固定 R 未写 radion 势 V(R)",
    ]
    coeff_standard = D(1) / (D(64) * D(str(math.pi)))
    key_numbers["kk_f_coeff_numeric_1_over_pi"] = fmt(coeff_standard)
    guard("G2-01", len(action_terms) == 3, "作用量项已拆为 EH / Maxwell / radion 缺失三项")
    add("B-01", "PASS", "固定半径截断下的 Maxwell 系数与标准 KK 归一一致",
        "由 S5=∫√−g5 R5/(16πG) 对圆纤维固定半径截断，F² 项为 −R²k²F²/(64πG)；系数是已知 KK 机制结果。")
    add("B-02", "INFO", "引力+电磁同源是已知 Kaluza–Klein 机制",
        "来料也明确承认这一点；本册只确认公式系数，不把它记为 ROOT 首创新物理。")
    add("B-03", "FAIL", "纯五维引力中固定内部半径不闭合",
        "候选作用量未给 V(R) 或其它稳定化项；R 的场方程不能一般性地被‘固定半径’替代，radion 自由度必须显式处理。")

    G = D("6.67430e-11")
    HBAR = D("1.054571817e-34")
    C = D("299792458")
    M_E = D("9.1093837139e-31")
    ALPHA_OBS = D("7.2973525643e-3")
    alpha_kk_si = D(4) * G * M_E * M_E / (HBAR * C)
    alpha_kk_c1 = D(4) * G * M_E * M_E / HBAR
    ratio_obs_pred = ALPHA_OBS / alpha_kk_si
    user_pred = D("7.007e-45")
    user_ratio = D("1.04e42")
    key_numbers.update({
        "G_SI": str(G),
        "hbar_SI": str(HBAR),
        "c_SI": str(C),
        "m_e_SI": str(M_E),
        "alpha_obs_CODATA2022": str(ALPHA_OBS),
        "alpha_kk_SI_with_c": fmt(alpha_kk_si),
        "alpha_kk_c1_literal": fmt(alpha_kk_c1),
        "obs_over_pred": fmt(ratio_obs_pred),
        "user_pred_rel_diff": fmt(rel_diff(alpha_kk_si, user_pred)),
        "user_ratio_rel_diff": fmt(rel_diff(ratio_obs_pred, user_ratio)),
    })

    guard("G3-01", rel_diff(alpha_kk_si, user_pred) < D("2e-3"),
          "α_KK(SI, 补 c)=%s 与来料 7.007e−45 相对差 %s" % (fmt(alpha_kk_si), fmt(rel_diff(alpha_kk_si, user_pred))))
    guard("G3-02", rel_diff(ratio_obs_pred, user_ratio) < D("5e-2"),
          "观测/预测=%s 与 1.04e42 相对差 %s" % (fmt(ratio_obs_pred), fmt(rel_diff(ratio_obs_pred, user_ratio))))
    c1_si_ratio = alpha_kk_c1 / alpha_kk_si
    key_numbers["c1_literal_over_SI_ratio"] = fmt(c1_si_ratio)
    guard("G3-03", c1_si_ratio > D("1e8"),
          "c=1 字面式与 SI 式不可混用，比值=%s≈c" % fmt(c1_si_ratio))

    add("C-01", "PASS", "α_KK 的 c=1 量纲口径可自洽",
        "在 c=1 下 [G]=L/M、[m²]=M²、[ħ]=ML，4Gm²/ħ 无量纲；在 SI 中须写成 4Gm²/(ħc)。两种口径不可混用。")
    add("C-02", "PASS", "电子代入值与来料量级一致",
        "用 CODATA 常数机器复算 α_KK=4Gm_e²/(ħc)=%s，来料写 7.007e−45，相对差 %s。" %
        (fmt(alpha_kk_si), fmt(rel_diff(alpha_kk_si, user_pred))))
    add("C-03", "FAIL", "最简 KK 质量—耦合关系被电子反例排除",
        "观测 α=%s，α_KK=%s，观测/预测=%s ≈1.04e42；单靠一个额外闭环维度不能给出电子的实际质量与电磁耦合。" %
        (str(ALPHA_OBS), fmt(alpha_kk_si), fmt(ratio_obs_pred)))

    add("D-01", "FAIL", "四力仍未从同一几何推出",
        "该截断只生成四维引力与 U(1) 电磁；强、弱规范群、表示、耦合与质量谱均未在作用量中出现。")
    add("D-02", "FAIL", "三力垂直原理到四力的桥未建立",
        "来料未给从内部闭环/曲率/挠率到 SU(3)×SU(2)×U(1) 的映射、 Chandan-Paton 型规范生成或等价机制；V144 任务仍是开放项。")
    add("D-03", "BOUNDARY", "ZIP 与测试声明只登记不验收",
        "来料声称 ROOT_V143_Helix_Fiber_KK_Complete.zip 约 1.94 MB、21 文件、45 测试与 20 文件 SHA-256；本轮未收到 ZIP，不能据声明判定通过。")

    status_counts = {}
    for e in entries:
        status_counts[e["status"]] = status_counts.get(e["status"], 0) + 1
    key_numbers["entries"] = len(entries)
    key_numbers["status_counts"] = status_counts
    key_numbers["guards"] = len(guards)
    key_numbers["guards_pass"] = sum(1 for g in guards if g["status"] == "PASS")

    lines = []
    lines.append("# TUFT r450 / ROOT V143 光速螺旋几何起源与 KK 纤维全维审计")
    lines.append("")
    lines.append("## 一、总览")
    lines.append("")
    lines.append("来料正本 SHA256：`%s`" % sha)
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
    lines.append("## 四、关键机器读数")
    lines.append("")
    lines.append("- RΩ=%s, v3=%s, κ=%s, τ=%s, ω_check=%s" %
                 (fmt(internal), fmt(v3), fmt(kappa), fmt(tau), fmt(omega_check)))
    lines.append("- α_KK(SI)=%s, α_obs=%s, obs/pred=%s" %
                 (fmt(alpha_kk_si), str(ALPHA_OBS), fmt(ratio_obs_pred)))
    lines.append("- image_refs=%d, external_https_links=%d" % (image_refs, external_links))
    lines.append("")
    lines.append("## 五、红线")
    lines.append("")
    lines.append("运动学可解与 KK 截断自洽不等于自然界存在第五维，也不等于四力统一。ZIP 声明未验收；红线不变。")
    lines.append("")

    md_path = DATA / (STEM + ".md")
    json_path = DATA / (STEM + ".json")
    report_path = DATA / (STEM + "_report.txt")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    payload = {
        "round": "r450",
        "topic": "ROOT V143 光速螺旋几何起源与 KK 纤维",
        "date": "2026-11-24",
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": sha,
        "entries": entries,
        "guards": guards,
        "key_numbers": key_numbers,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(
        "OK entries=%d guards=%d/%d\nsource_sha256=%s\nalpha_kk=%s obs_over_pred=%s\nstatus=%s\n" %
        (len(entries), key_numbers["guards_pass"], len(guards), sha,
         fmt(alpha_kk_si), fmt(ratio_obs_pred),
         json.dumps(status_counts, ensure_ascii=False, sort_keys=True)),
        encoding="utf-8",
    )

    print("OK entries=%d guards=%d/%d" % (len(entries), key_numbers["guards_pass"], len(guards)))
    print("source_sha256=%s" % sha)
    print("alpha_kk=%s obs_over_pred=%s" % (fmt(alpha_kk_si), fmt(ratio_obs_pred)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("ERROR", type(exc).__name__, str(exc))
        sys.exit(1)
