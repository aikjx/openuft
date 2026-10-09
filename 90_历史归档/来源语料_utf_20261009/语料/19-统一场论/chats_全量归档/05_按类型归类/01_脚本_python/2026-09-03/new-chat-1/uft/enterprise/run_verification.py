# -*- coding: utf-8 -*-
"""
企业级统一验证入口（run_verification.py）
==========================================
按验收标准运行全部验证并生成 Markdown 报告。

用法：
  python run_verification.py            # 标准模式：企业级精算 + 单元测试
  python run_verification.py --legacy   # 同时复跑历史 5 套脚本（KK/变分/数值/三重奏/自检）
  python run_verification.py --report <path>   # 自定义报告输出路径

验收标准（企业级 QA 门）：
  [QA-1] CODATA 2022 Planck 单位核算相对差 < 1e-6
  [QA-2] κℓ_P=E/E_P 恒等式 250 位对标相对差 < 1e-12
  [QA-3] 三重奏量纲修复：修复式比值 = 1（1e-20 内）
  [QA-4] 单元测试 100% 通过
  [QA-5] 历史验证套件（KK/变分/数值）无 Traceback/Error/Exception
  [QA-6] KK 额外维一致性给出明确可证伪判定（排除 5+ 数量级矛盾）
"""
import os, sys, subprocess, datetime
import mpmath as mp
mp.mp.dps = 250

HERE = os.path.dirname(os.path.abspath(__file__))
UFT  = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from pkg import constants as C
from pkg import triad as T

def qa_gate(name, passed, detail=""):
    mark = "PASS" if passed else "FAIL"
    print(f"  [{mark}] {name}  {detail}")
    return passed

def run():
    args = sys.argv[1:]
    report_path = None
    if "--report" in args:
        report_path = args[args.index("--report")+1]
    report_path = report_path or os.path.join(HERE, "reports", "verification_report.md")

    print("="*74)
    print(" 算法联盟 · 全维三重奏 · 企业级验证与精算")
    print(f" 时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*74)
    results = {}

    # ---------------- QA-1: CODATA 2022 Planck 核算 ----------------
    print("\n[QA-1] CODATA 2022 Planck 单位核算（250 位）")
    ok1 = (abs((C.LP - mp.mpf("1.616255e-35"))/mp.mpf("1.616255e-35")) < mp.mpf("1e-6") and
           abs((C.MP_PL - mp.mpf("2.176434e-8"))/mp.mpf("2.176434e-8")) < mp.mpf("1e-6") and
           abs((C.TP_ - mp.mpf("5.391247e-44"))/mp.mpf("5.391247e-44")) < mp.mpf("1e-6"))
    codata_lines = [C.CODATA_SUMMARY()]
    qa_gate("QA-1", ok1, "ℓ_P/M_P/t_P 对标 CODATA 2022")

    # ---------------- QA-2: 三重奏恒等式 ----------------
    print("\n[QA-2] κℓ_P = E/E_P 恒等式（250 位）")
    id_lines = []
    ok2 = True
    for name, mkg in [("电子", C.ME), ("质子", C.MP),
                      ("W", mp.mpf("80.369")*C.GEV2KG),
                      ("Higgs", mp.mpf("125.10")*C.GEV2KG),
                      ("Planck", C.MP_PL)]:
        kl, r, rel = T.triad_identity_check(mkg)
        ok2 &= rel < mp.mpf("1e-12")
        id_lines.append(f"  {name:8s} κℓ_P={mp.nstr(kl,12)}  E/E_P={mp.nstr(r,12)}  相对差={mp.nstr(rel,3)}")
        print(id_lines[-1])
    qa_gate("QA-2", ok2, "5 粒子恒等式")

    # ---------------- QA-3: 量纲修复 ----------------
    print("\n[QA-3] 三重奏量纲修复自检")
    lhs, rhs_orig, rhs_fix, ratio, fix2diff = T.dimension_audit(C.ME)
    ok3 = abs(ratio-1) < mp.mpf("1e-20") and abs(fix2diff) < mp.mpf("1e-70")
    print(f"  原式断裂: κ²={mp.nstr(lhs,6)} m⁻² vs (ωℓ_P/c)²={mp.nstr(rhs_orig,6)}（差 {mp.nstr(mp.log10(lhs/rhs_orig),2)} 个数量级）")
    print(f"  修复式: (ω/c)²/κ²={mp.nstr(ratio,10)}；修复式2差={mp.nstr(fix2diff,4)}")
    qa_gate("QA-3", ok3, "量纲修复一致")

    # ---------------- QA-4: 单元测试 ----------------
    print("\n[QA-4] 单元测试")
    test_file = os.path.join(HERE, "tests", "test_triad.py")
    r4 = subprocess.run([sys.executable, test_file], capture_output=True, text=True, encoding="utf-8")
    ok4 = r4.returncode == 0
    print("  " + r4.stdout.replace("\n", "\n  ").strip())
    if r4.stderr.strip():
        print("  STDERR: " + r4.stderr.strip()[:500])
    qa_gate("QA-4", ok4, "tests/test_triad.py")

    # ---------------- QA-5: 历史验证套件 ----------------
    print("\n[QA-5] 历史验证套件复跑")
    ok5 = True
    legacy_lines = []
    if "--legacy" in args:
        legacy_scripts = ["test0_validate_toolkit.py", "verify_kk.py",
                          "verify_variation.py", "verify_numeric.py", "verify_triad.py"]
        for s in legacy_scripts:
            p = os.path.join(UFT, s)
            if not os.path.exists(p):
                print(f"  跳过（不存在）: {s}")
                continue
            r = subprocess.run([sys.executable, p], capture_output=True, text=True, encoding="utf-8")
            bad = any(k in (r.stdout + r.stderr) for k in ["Traceback", "Error", "Exception"])
            ok5 &= (r.returncode == 0) and (not bad)
            print(f"  {'PASS' if (r.returncode==0 and not bad) else 'FAIL'}  {s}")
            legacy_lines.append(f"  {s}: {'PASS' if (r.returncode==0 and not bad) else 'FAIL'}")
    else:
        ok5 = None
        print("  （未指定 --legacy，跳过；QA-5 记为 N/A）")

    # ---------------- QA-6: KK 一致性可证伪判定 ----------------
    print("\n[QA-6] KK 额外维一致性（可证伪判定）")
    kk_lines = []
    ok6 = True
    for Rc in [mp.mpf("1e-4"), mp.mpf("1e-3"), mp.mpf("1.0")]:
        v = T.kk_consistency_verdict(Rc)
        ok6 &= (v["consistent"] is False) and v["contradiction_orders_of_magnitude"] > 5
        ln = (f"  R_c={mp.nstr(Rc,3)} m → 三重奏要求 R_curv={mp.nstr(v['R_curv_required_m'],3)} m"
              f" vs 观测≥{mp.nstr(v['R_obs_min_m'],3)} m → "
              f"{'一致' if v['consistent'] else '排除'}（矛盾 {mp.nstr(v['contradiction_orders_of_magnitude'],2)} 数量级）")
        kk_lines.append(ln); print(ln)
    qa_gate("QA-6", ok6, "三重奏×额外维被观测排除")

    # ---------------- 报告生成 ----------------
    print("\n[报告] 生成验证报告 ...")
    triad_text = T.triad_report()
    gates = [
        ("QA-1 CODATA2022 Planck核算", "PASS" if ok1 else "FAIL", ok1),
        ("QA-2 三重奏恒等式 250位", "PASS" if ok2 else "FAIL", ok2),
        ("QA-3 量纲修复", "PASS" if ok3 else "FAIL", ok3),
        ("QA-4 单元测试", "PASS" if ok4 else "FAIL", ok4),
        ("QA-5 历史套件", ("PASS" if ok5 else "FAIL") if ok5 is not None else "N/A", ok5),
        ("QA-6 KK可证伪判定", "PASS" if ok6 else "FAIL", ok6),
    ]
    all_pass = all(g[2] for g in gates if g[2] is not None)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 企业级验证报告：算法联盟 · 全维三重奏精算\n\n")
        f.write(f"- 生成时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- 精度：mpmath {mp.mp.dps} 位有效数字\n")
        f.write(f"- 总体结论：**{'全部通过（GREEN）' if all_pass else '存在失败项（RED）'}**\n\n")
        f.write("## 验收标准（QA 门）\n\n| 门 | 名称 | 结果 |\n|---|---|---|\n")
        for n, s, _ in gates:
            f.write(f"| {n} | {s} | {'✅' if s=='PASS' else ('—' if s=='N/A' else '❌')} |\n")
        f.write("\n## 1. CODATA 2022 Planck 单位核算\n\n```\n" + C.CODATA_SUMMARY() + "\n```\n\n")
        f.write("## 2. 三重奏恒等式对标（250 位）\n\n```\n" + "\n".join(id_lines) + "\n```\n\n")
        f.write("## 3. 量纲修复\n\n")
        f.write(f"- 原式断裂：κ²={mp.nstr(lhs,6)} m⁻² vs (ωℓ_P/c)²={mp.nstr(rhs_orig,6)}（差 {mp.nstr(mp.log10(lhs/rhs_orig),2)} 数量级）\n")
        f.write(f"- 修复式：(ω/c)²/κ²={mp.nstr(ratio,10)}；修复式2差={mp.nstr(fix2diff,4)}\n\n")
        f.write("## 4. KK 额外维一致性（可证伪判定）\n\n```\n" + "\n".join(kk_lines) + "\n```\n\n")
        f.write("## 5. 单元测试\n\n```\n" + r4.stdout.strip() + "\n```\n\n")
        if legacy_lines:
            f.write("## 6. 历史验证套件\n\n```\n" + "\n".join(legacy_lines) + "\n```\n\n")
        f.write("## 7. 诚实审计（OPEN）\n\n")
        f.write("- 三重奏已验：v≡c 恒等式、量纲修复、κℓ_P=E/E_P、零质量极限；均为已知物理的重组。\n")
        f.write("- 未闭合：常数生成欠定+循环论证；κ 映射双义（引力/固有加速度）；从公理到场方程缺场论化。\n")
        f.write("- 可证伪新结论（本轮）：三重奏若绑定 KK 额外维解释，则与亚毫米引力实验矛盾（5+ 数量级）。\n")
    print(f"  报告已写入: {report_path}")
    print("\n" + "="*74)
    print(" 最终验收: " + ("全部通过 GREEN" if all_pass else "存在失败项 RED"))
    print("="*74)
    return 0 if all_pass else 1

if __name__ == "__main__":
    raise SystemExit(run())
