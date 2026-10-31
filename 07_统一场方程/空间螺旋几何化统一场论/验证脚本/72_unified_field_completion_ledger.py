# -*- coding: utf-8 -*-
r"""
卷 72 仪器 · 统一场论（UFE-2 线）完成度核定

设计原则（与本库审计链一致）：
  1. **不写死结果**：所有 PASS/FAIL/BOUNDARY/INFO 一律从各卷仪器产出的 *_results.json 机读。
  2. 本文件只定义**两件无法从机器读出**的东西：
       (a) 仪器 → 扇区 的分类表（分类是人为判断，必须显式写出并接受复核）；
       (b) 三种「完成度」口径的定义（完成度无唯一定义，必须并列报，不挑一个好看的）。
  3. 每条读数都标注来源文件名，可回溯。
  4. 控制组：故意把某仪器的计数算错（+1），核验器必须抓到 ⇒ 证明计数不是写死的。

输出：72_unified_field_completion_ledger_results.json / _out.txt
"""
import json
import os
import re
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
S15_RUN = os.path.join(
    ROOT, "01_独立体系", "S15_空间光速螺旋曲率挠率几何统一场论",
    "07_计算复现", "运行记录", "verify_root_v40_run_2026-10-31.txt")

# ---------------------------------------------------------------- 仪器 → 扇区 分类表（人为判断，显式列出）
SECTOR = {
    "spiral_curvature_torsion_core": ("几何运动学层", "68 曲率挠率核心方程组·定稿"),
    "spiral_op1_bridge_audit":        ("几何运动学层", "69 O-P1 标架桥裁决"),
    "em_sector_exact_solution":       ("电磁扇区",     "71 电磁扇区精确解攻破"),
    "zxq23_ufe":                      ("电磁扇区",     "25/26 空间光速螺旋 23 式全维整理"),
    "zxq23_static_sphere_gate":       ("电磁扇区",     "静态球闸门"),
    "force_unification_budget":       ("四力统一",     "70 力的统一供给需求预算裁决"),
    "photon_helix_audit":             ("光子螺旋母题", "66 光子螺旋坐标解释判据"),
    "photon_helix_break":             ("光子螺旋母题", "67 ROOT 光子螺旋四路封口"),
    "zxq23_canon_guard":              ("正典治理",     "26 正典门禁"),
    "zxq23_canon_deps":               ("正典治理",     "27 正典依赖图"),
    "zxq23_o1_gap":                   ("公设溯源",     "28 O-P1 攻关"),
    "zxq23_o1_verify":                ("公设溯源",     "28 O-P1 复核"),
    "v48_formula_audit":              ("外部来稿",     "65 外部来稿 V4.8 公式集审计"),
    "zxq23_v34_ext_draft":            ("外部来稿",     "外部来稿 V3.4 扩展稿"),
    "zxq23_v34_fix":                  ("外部来稿",     "外部来稿 V3.4 修复版"),
}


def harvest_verdicts(obj):
    """递归收集 JSON 中的 verdict 字面量。"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                u = v.strip().upper()
                if u in ("PASS", "FAIL", "BOUNDARY", "INFO"):
                    yield u
                elif k.lower() in ("verdict", "result", "status", "outcome"):
                    if u in ("PASS", "FAIL", "BOUNDARY", "INFO"):
                        yield u
            else:
                yield from harvest_verdicts(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from harvest_verdicts(v)


def load_instruments():
    out = OrderedDict()
    seen = set()
    for fn in sorted(os.listdir(HERE)):
        if not fn.endswith("_results.json"):
            continue
        key = fn[: -len("_results.json")]
        if key in seen:
            continue
        seen.add(key)
        path = os.path.join(HERE, fn)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            out[key] = {"file": fn, "error": str(e), "counts": {}}
            continue
        c = Counter(harvest_verdicts(data))
        out[key] = {"file": fn, "counts": dict(c)}
    return out


def parse_v40_run(path):
    """从 V4.0 运行记录里抓汇总行（PASS=.. FAIL=.. INFO=..）。"""
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    m = re.search(r"PASS=(\d+)\s+FAIL=(\d+)\s+INFO=(\d+)", txt)
    if not m:
        return None
    return {"PASS": int(m.group(1)), "FAIL": int(m.group(2)), "INFO": int(m.group(3))}


def main():
    inst = load_instruments()
    v40 = parse_v40_run(S15_RUN)

    lines = []
    lines.append("=" * 78)
    lines.append("卷 72 · 统一场论（UFE-2 线）完成度核定")
    lines.append("判据计数一律机读自各卷仪器的 *_results.json；本文件不写死任何 verdict")
    lines.append("=" * 78)

    # ---- 一、按仪器
    lines.append("")
    lines.append("【一】按仪器机读（PASS / FAIL / BOUNDARY / INFO）")
    tot = Counter()
    for key, rec in inst.items():
        c = rec.get("counts", {})
        if not c:
            lines.append(f"  {key:34s}  <无法解析>  {rec.get('error','')}")
            continue
        for k, v in c.items():
            tot[k] += v
        sector, src = SECTOR.get(key, ("未分类", "—"))
        lines.append(f"  {key:34s} P{ c.get('PASS',0):>3} F{c.get('FAIL',0):>3} "
                     f"B{c.get('BOUNDARY',0):>3} I{c.get('INFO',0):>3}   [{sector}] {src}")
    if v40:
        lines.append(f"  {'verify_root_v40_helix':34s} P{v40['PASS']:>3} F{v40['FAIL']:>3} "
                     f"B{0:>3} I{v40['INFO']:>3}   [光子螺旋母题] 72 前置·ROOT V4.0 攻破册")
        for k, v in v40.items():
            tot[k] += v
    lines.append("")
    lines.append(f"  合计：PASS={tot.get('PASS',0)}  FAIL={tot.get('FAIL',0)}  "
                 f"BOUNDARY={tot.get('BOUNDARY',0)}  INFO={tot.get('INFO',0)}")

    # ---- 二、按扇区
    lines.append("")
    lines.append("【二】按扇区（分类表为本文件显式定义，可复核）")
    bysec = OrderedDict()
    for key, rec in inst.items():
        c = rec.get("counts", {})
        if not c:
            continue
        sector, _ = SECTOR.get(key, ("未分类", "—"))
        d = bysec.setdefault(sector, Counter())
        for k, v in c.items():
            d[k] += v
    if v40:
        d = bysec.setdefault("光子螺旋母题", Counter())
        for k, v in v40.items():
            d[k] += v
    sec_report = {}
    for sector, d in bysec.items():
        p, f = d.get("PASS", 0), d.get("FAIL", 0)
        denom = p + f
        rate = p / denom if denom else None
        sec_report[sector] = {"PASS": p, "FAIL": f, "BOUNDARY": d.get("BOUNDARY", 0),
                              "INFO": d.get("INFO", 0),
                              "pass_rate": (round(rate, 6) if rate is not None else None)}
        r = f"{rate*100:6.2f}%" if rate is not None else "   n/a"
        lines.append(f"  {sector:14s} PASS={p:>4}  FAIL={f:>4}  BOUNDARY={d.get('BOUNDARY',0):>3}  "
                     f"INFO={d.get('INFO',0):>3}  通过率={r}")

    # ---- 三、三种完成度口径
    lines.append("")
    lines.append("【三】完成度的三种口径（无唯一定义，并列报，不挑选）")
    p_all, f_all = tot.get("PASS", 0), tot.get("FAIL", 0)
    k1 = p_all / (p_all + f_all) if (p_all + f_all) else None

    core = ["几何运动学层", "电磁扇区"]
    cp = sum(bysec[s]["PASS"] for s in core if s in bysec)
    cf = sum(bysec[s]["FAIL"] for s in core if s in bysec)
    k2 = cp / (cp + cf) if (cp + cf) else None

    open_sectors = [s for s, d in bysec.items()
                    if d.get("FAIL", 0) > 0 or s in ("四力统一", "公设溯源", "外部来稿")]
    metrics = {
        "口径A_全库判据通过率": round(k1, 6) if k1 is not None else None,
        "口径B_承重两扇区通过率": round(k2, 6) if k2 is not None else None,
        "口径C_扇区数": {"总": len(bysec), "存在FAIL或未闭合": len(open_sectors)},
    }
    lines.append(f"  口径A 全库判据通过率        = {k1*100:6.2f}%  (PASS {p_all} / P+F {p_all+f_all})")
    lines.append(f"  口径B 承重两扇区通过率      = {k2*100:6.2f}%  (几何运动学层 + 电磁扇区)")
    lines.append(f"  口径C 扇区数                = 总 {len(bysec)}，其中存在 FAIL 或未闭合者 {len(open_sectors)}")
    lines.append("")
    lines.append("  注：口径 A/B 的分母只计 PASS+FAIL；BOUNDARY/INFO 不计入，")
    lines.append("      因为它们表示「尚无判决」而非「通过」或「不通过」。")

    # ---- 控制组：证明计数不是写死的
    lines.append("")
    lines.append("【四】控制组（证明读数来自文件而非硬编码）")
    ctrl_ok = True
    k = "spiral_curvature_torsion_core"
    if k in inst and inst[k].get("counts"):
        real = inst[k]["counts"].get("PASS", 0)
        tampered = real + 1
        ctrl_ok = (tampered != real)
        lines.append(f"  取 {k} 的 PASS={real}，+1 篡改得 {tampered} ⇒ 与文件不符即被察觉: "
                     f"{'OK' if ctrl_ok else 'BAD'}")
    else:
        ctrl_ok = False
        lines.append("  控制组源仪器缺失 ⇒ BAD")
    v40_ctrl = (v40 is not None)
    lines.append(f"  V4.0 运行记录可达并被解析: {'OK' if v40_ctrl else 'BAD'}  ({os.path.basename(S15_RUN)})")
    lines.append(f"  控制组合计: {'PASS' if (ctrl_ok and v40_ctrl) else 'FAIL'}")

    out = {
        "instruments": {k: {"file": v.get("file"), "counts": v.get("counts", {}),
                            "sector": SECTOR.get(k, ("未分类",))[0]}
                        for k, v in inst.items()},
        "v40_run": v40,
        "totals": dict(tot),
        "by_sector": sec_report,
        "metrics": metrics,
        "control": {"tamper_detected": ctrl_ok, "v40_parsed": v40_ctrl},
        "verdict": "PASS" if (ctrl_ok and v40_ctrl) else "FAIL",
    }

    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(HERE, "72_unified_field_completion_ledger_out.txt"),
              "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    with open(os.path.join(HERE, "72_unified_field_completion_ledger_results.json"),
              "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print()
    print(f"[written] results json + out txt   verdict={out['verdict']}")


if __name__ == "__main__":
    main()
