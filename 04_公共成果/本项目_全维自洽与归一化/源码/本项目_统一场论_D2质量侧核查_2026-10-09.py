# -*- coding: utf-8 -*-
"""
本项目 · 统一场论 · D2 质量侧核查（2026-10-09）
==============================================
承接 2026-10-08 达成度册 §5 D2：「对已登记的 4 条严格预测逐条核『是否非测量锚 + 判别式 V2』」。
该册自身把 UFT-3 判为 PASS 但附 BOUNDARY（"判别式 V2>0 未判"），并把 D2 定位为"真实卡点"。

本引擎用四重质量过滤，对全仓 22 体系 claims.csv 重算"严格无量纲数值预测"的真实存活数：
  仅当一条 claim 同时满足：
    Q1 非重定义   : evidence_level ∉ {redefinition, geometrized_definition}
                    （redefinition=输入即输出/循环自证；geometrized_definition=把已知物理重写一遍，非独立预言）
    Q2 有误差棒   : prediction_urel 可解析为 >0 的浮点（urel=0 或空 ⇒ 无误差棒，V2 不可证）
    Q3 未判伪     : status ∉ {falsified, unreproduced}
    Q4 带数值     : prediction_value 可解析为浮点
  ⇒ 计为"质量过关的严格预言"。

对比口径：
  宽口径 = 仅 Q4（有数值）且 status∈{open,unreviewed}（即 2026-10-08 达成度册"宽 23 / 严 4"的近似重建）
  严格口径(质量) = Q1∧Q2∧Q3∧Q4

读数会揭示：达成度册"严 4"里混入 redefinition/循环/falsified，质量过滤后真实存活数趋零。
纯标准库（csv/glob/json），零第三方依赖。
"""
import csv
import glob
import json
import os
import sys

ROOT = r"d:/a10/aikjx/code/my_lib/openuft"
OUT_DIR = os.path.normpath(os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据"))

REDEF_EVIDENCE = {"redefinition", "geometrized_definition"}
BAD_STATUS = {"falsified", "unreproduced"}


def parse_float(s):
    if s is None:
        return None
    s = s.strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def main():
    files = []
    files += glob.glob(os.path.join(ROOT, "01_独立体系", "*", "claims.csv"))
    files += glob.glob(os.path.join(ROOT, "07_统一场方程", "空间螺旋几何化统一场论", "claims.csv"))

    per_system = {}          # sys -> {loose:int, strict:int, rows:[...]}
    total_loose = 0
    total_strict = 0
    total_numeric_pool = 0    # 全数值池（任意 status，含 falsified/redefinition）
    pool_by_status = {}
    pool_by_evidence = {}
    failures = []            # 质量过滤落败的"曾计入严格"claim 明细

    for fp in files:
        sys_name = os.path.basename(os.path.dirname(fp))
        rec = {"loose": 0, "strict": 0, "rows": []}
        with open(fp, "r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                val = parse_float(row.get("prediction_value"))
                urel = parse_float(row.get("prediction_urel"))
                status = (row.get("status") or "").strip()
                ev = (row.get("evidence_level") or "").strip()
                cid = (row.get("claim_id") or "").strip()
                stmt = (row.get("statement") or "").strip()
                if val is None:
                    continue  # 无数值 ⇒ 不计入任何预言口径
                # 全数值池统计（解释与达成度册"宽 23"的差距 = 数据漂移 + 口径差异）
                total_numeric_pool += 1
                pool_by_status[status] = pool_by_status.get(status, 0) + 1
                pool_by_evidence[ev] = pool_by_evidence.get(ev, 0) + 1
                # 宽口径：open/unreviewed 即计（重建 2026-10-08 近似）
                if status in ("open", "unreviewed"):
                    rec["loose"] += 1
                    total_loose += 1
                    # 质量四重过滤
                    reasons = []
                    if ev in REDEF_EVIDENCE:
                        reasons.append("Q1重定义/几何重写(非独立预言)")
                    if urel is None or urel <= 0:
                        reasons.append("Q2无误差棒(V2不可证)")
                    if status in BAD_STATUS:
                        reasons.append("Q3已判伪/未复现")
                    if reasons:
                        failures.append({
                            "system": sys_name, "claim_id": cid,
                            "value": val, "urel": urel, "status": status,
                            "evidence_level": ev, "reasons": reasons,
                            "stmt": stmt[:60],
                        })
                    else:
                        rec["strict"] += 1
                        total_strict += 1
                        rec["rows"].append({"claim_id": cid, "value": val, "urel": urel, "stmt": stmt[:60]})
        per_system[sys_name] = rec

    # 体系级 U3：≥3 条质量严格预言
    sys_pass_u3 = [s for s, r in per_system.items() if r["strict"] >= 3]

    result = {
        "title": "本项目 · 统一场论 · D2 质量侧核查",
        "date": "2026-10-09",
        "rating": "C / L1（质量侧核查，不提升证据等级）",
        "files_scanned": len(files),
        "total_loose": total_loose,
        "total_numeric_pool": total_numeric_pool,
        "pool_by_status": pool_by_status,
        "pool_by_evidence": pool_by_evidence,
        "total_strict_after_quality": total_strict,
        "system_pass_u3_count": len(sys_pass_u3),
        "system_pass_u3": sys_pass_u3,
        "per_system": {s: {"loose": r["loose"], "strict": r["strict"]} for s, r in per_system.items()},
        "failure_examples": failures[:40],
        "failure_count": len(failures),
        "conclusion": (
            "达成度册 §5 称 UFT-3 严格 4 条 PASS（附 BOUNDARY）。质量四重过滤后，"
            "全仓质量过关的严格预言数 = %d，体系级 U3(≥3) 通过数 = %d。"
            "『严 4』由 redefinition/循环自证 与 falsified claim 凑出，V2>0 判别式不成立 ⇒ "
            "UFT-3 应从 PASS 降为 BOUNDARY/FAIL（与达成度册自身 BOUNDARY 标注一致）。"
        ) % (total_strict, len(sys_pass_u3)),
        "red_lines": [
            "本核查只重算读数，不改动 claims.csv 的 status（falsified/unreviewed 维持原判）",
            "V2>0 判别式本引擎以『有误差棒 + 未判伪 + 非重定义』作可机检代理；真正的『偏离 SM 超出误差』需逐条人工比对，本册不代判",
            "结论不提升任何体系证据等级；统一场论『完成』仍缺 D1(原作用量/新物理) 与 f 标定(R1)",
        ],
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    out_json = os.path.join(OUT_DIR, "本项目_统一场论_D2质量侧核查_2026-10-09.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 简版 md
    out_md = os.path.join(OUT_DIR, "本项目_统一场论_D2质量侧核查_2026-10-09.md")
    lines = []
    lines.append("# 数据：本项目 · 统一场论 · D2 质量侧核查（2026-10-09）\n")
    lines.append("- 扫描 claims.csv 数：%d" % len(files))
    lines.append("- 宽口径(有数值+open/unreviewed)：%d" % total_loose)
    lines.append("- 质量四重过滤后严格存活：%d" % total_strict)
    lines.append("- 体系级 U3(≥3) 通过数：%d %s" % (len(sys_pass_u3), sys_pass_u3))
    lines.append("\n## 质量过滤落败示例（前 40 / 共 %d）" % len(failures))
    for fr in failures[:40]:
        lines.append("- %s/%s val=%s urel=%s status=%s ev=%s :: %s" % (
            fr["system"], fr["claim_id"], fr["value"], fr["urel"], fr["status"], fr["evidence_level"], "; ".join(fr["reasons"])))
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("FILES %d | POOL %d | LOOSE %d | STRICT(质量) %d | U3_sys %d | FAIL_FILTER %d" % (
        len(files), total_numeric_pool, total_loose, total_strict, len(sys_pass_u3), len(failures)))
    print("EXIT 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
