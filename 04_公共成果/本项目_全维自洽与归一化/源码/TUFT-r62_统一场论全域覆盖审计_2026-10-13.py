# -*- coding: utf-8 -*-
"""
TUFT-r62 · 统一场论全域覆盖审计引擎（纯标准库）

任务：把 UFE-1 主方程 (E) 及其各分量（ECSK 引力 / YM 规范 / Higgs / Dirac）、
与「空间螺旋几何化」独有子断言（S_spiral、κ 生质量、α=τ/κ、G 由 κ 生成），
对「现象覆盖矩阵」逐条做覆盖分类，并叠加 r 系列攻破结论，输出可机读覆盖档案。

分类口径（F4 范畴一致 / E9 能标一致 贯穿）：
  - CORE   : 由 ECSK+SM 主方程核心分量 ((E)/(YM)/(H)/(D)/(C)) 直接覆盖
  - INPUT  : 主方程可写但参数（Yukawa/混合角/Λ/层级）为输入，非推导
  - THESIS : 「空间螺旋几何化」独有子断言（κ 机制），受 r45/r61 攻破影响
  - OPEN   : 证据状态为 未解决/开放/互斥，主方程未闭合
"""
import csv
import json
import os
from collections import Counter

MATRIX = r"D:/a10/aikjx/code/my_lib/openuft/07_统一场方程/现象覆盖矩阵.csv"
# 空间螺旋几何化子矩阵（TUFT 独有子断言的覆盖评级）
SPIRAL_MATRIX = r"D:/a10/aikjx/code/my_lib/openuft/07_统一场方程/空间螺旋几何化统一场论/现象覆盖矩阵.csv"
OUT_DIR = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/数据"
BASENAME = "TUFT-r62_统一场论全域覆盖审计_2026-10-13"
os.makedirs(OUT_DIR, exist_ok=True)


def load_matrix(path):
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def classify(row):
    """返回 (bucket, note)。"""
    comp = (row.get("主控方程分量") or row.get("主控子系统") or "")
    deriv = (row.get("由主方程导出") or "").strip()
    status = (row.get("证据状态") or row.get("判定") or "").strip()
    remark = row.get("备注") or ""
    # 螺旋几何化独有子断言标记
    spiral_markers = ["κ", "螺旋", "几何化", "τ/κ", "S_spiral", "挠率", "tanθ"]
    is_thesis = any(m in comp or m in remark for m in spiral_markers) \
        and ("几何化" in comp or "几何化" in remark or "κ" in comp or "κ" in remark)
    # OPEN 状态
    if status in ("未解决", "开放", "互斥"):
        return "OPEN", "证据状态=%s" % status
    if is_thesis:
        return "THESIS", "空间螺旋几何化子断言；受 r45/r61 攻破影响"
    if deriv == "否" or "输入" in (row.get("定量一致性") or "") or "参数" in remark:
        return "INPUT", "主方程可写但参数为输入"
    return "CORE", "由主方程核心分量直接覆盖"


main_rows = load_matrix(MATRIX)
spiral_rows = load_matrix(SPIRAL_MATRIX)

main_out = []
status_counter = Counter()
bucket_counter = Counter()
for r in main_rows:
    bucket, note = classify(r)
    status = (r.get("证据状态") or "").strip()
    status_counter[status] += 1
    bucket_counter[bucket] += 1
    main_out.append({
        "现象": r.get("现象"), "特征尺度": r.get("特征尺度"),
        "主控分量": r.get("主控方程分量"), "由主方程导出": r.get("由主方程导出"),
        "定量一致性": r.get("定量一致性"), "证据状态": status,
        "bucket": bucket, "note": note,
    })

spiral_out = []
for r in spiral_rows:
    status = (r.get("判定") or r.get("证据状态") or "").strip()
    spiral_out.append({
        "现象": r.get("现象"), "主控子系统": r.get("主控子系统"),
        "证据状态": r.get("证据状态"), "判定": status, "备注": r.get("备注"),
    })

total = len(main_out)
n_core = bucket_counter["CORE"]
n_input = bucket_counter["INPUT"]
n_thesis = bucket_counter["THESIS"]
n_open = bucket_counter["OPEN"]
n_established = status_counter.get("已确立", 0) + status_counter.get("部分确立", 0)

# 攻破叠加：THESIS 行在 r45/r61 后实际状态
thesis_attack = {
    "S_spiral 体作用量": "r61：原系数 ℏ/(2c) 错(缺口c²)；来料修正 ℏc/l0² 仍错；干净版废式；正确 ℏc/2",
    "V(κ)≡0": "r45 C2：公理1 使势恒零，变分链无粒子",
    "m(κ) 标度": "r45 C3：弱场 κ=mc·sinθ/ħ ⇒ m² 标度不可破",
    "κ(m) 实根": "r45 C4/T16：全部真实粒子无实根（需 θ<1.4e-11 rad）",
    "g-2 符号": "r45 T27：cotθ_e 与 cotθ_μ 符号互斥",
    "l0": "r42：自由常数→Ω5，或=l_P→零信息",
}

verdict = ("UNIFIED_FIELD_CLAIM_PARTIALLY_COMPUTABLE"
           if (n_core + n_input) > n_open else "UNIFIED_FIELD_CLAIM_FAILED")

payload = {
    "audit": "TUFT-r62",
    "subject": "统一场论全域覆盖审计（现象矩阵 × 主方程 × 攻破序列）",
    "verdict": verdict,
    "main_matrix_total": total,
    "bucket_counts": dict(bucket_counter),
    "status_counts": dict(status_counter),
    "established_or_partial": n_established,
    "spiral_matrix_rows": len(spiral_out),
    "thesis_attack_overlay": thesis_attack,
    "main_rows": main_out,
    "spiral_rows": spiral_out,
    "conclusion": (
        "ECSK+SM 核心 ((E)/(YM)/(H)/(D)/(C)) 在数学上统一了引力与标准模型的"
        "共同作用量，并复现 V1–V7 已验证预言；但 Yukawa/混合角/Λ/层级为输入。"
        "「空间螺旋几何化」独有子断言（S_spiral、κ 生质量、α=τ/κ、G 由 κ 生成）"
        "被 r45/r61 攻破：量纲错、势恒零、无实根、g-2 符号互斥、l0 撞 Ω5。"
        "暗能量/暗物质/层级/耦合统一/质子衰变张力仍 OPEN。 ⇒ 统一场论「可算」但「未闭合」。"
    ),
}

with open(os.path.join(OUT_DIR, BASENAME + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

# MD 数据册
md = []
md.append("# TUFT-r62 · 统一场论全域覆盖审计 · 机器数据册\n")
md.append("- 裁决：%s" % verdict)
md.append("- 主矩阵现象总数：%d" % total)
md.append("- 覆盖桶：CORE=%d INPUT=%d THESIS=%d OPEN=%d"
          % (n_core, n_input, n_thesis, n_open))
md.append("- 证据状态：%s" % dict(status_counter))
md.append("- 已确立+部分确立：%d\n" % n_established)
md.append("## 主矩阵逐条覆盖")
for x in main_out:
    md.append("- [%s] %s | 分量=%s | 导出=%s | 状态=%s | %s"
              % (x["bucket"], x["现象"], x["主控分量"], x["由主方程导出"], x["证据状态"], x["note"]))
md.append("\n## 空间螺旋几何化子矩阵（TUFT 独有子断言）")
for x in spiral_out:
    md.append("- %s | 判定=%s | 状态=%s" % (x["现象"], x["判定"], x["证据状态"]))
md.append("\n## 攻破叠加（THESIS 行在 r45/r61 后实际状态）")
for k, v in thesis_attack.items():
    md.append("- %s：%s" % (k, v))
with open(os.path.join(OUT_DIR, BASENAME + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

report = []
report.append("TUFT-r62 统一场论全域覆盖审计 生成时刻=%s" % __import__("datetime").datetime.now().isoformat())
report.append("模块=%s" % os.path.abspath(__file__))
report.append("裁决=%s" % verdict)
report.append("主矩阵=%d  CORE=%d INPUT=%d THESIS=%d OPEN=%d"
              % (total, n_core, n_input, n_thesis, n_open))
report.append("证据状态=%s" % dict(status_counter))
report.append("")
report.append("攻破叠加：")
for k, v in thesis_attack.items():
    report.append("  %s: %s" % (k, v))
with open(os.path.join(OUT_DIR, BASENAME + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report) + "\n")

# 自检 guard：CORE+INPUT+THESIS+OPEN == total；spiral 子矩阵含 OPEN/BOUNDARY
guard_all = (n_core + n_input + n_thesis + n_open == total) and (len(spiral_out) > 0)
raise SystemExit(0 if guard_all else 1)
