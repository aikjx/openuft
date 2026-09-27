# -*- coding: utf-8 -*-
"""
空间螺旋 CMB 拓扑双谱攻坚审计
==============================

目标：判定空间螺旋纲领能否产出**独立于标准宇宙学**的 CMB 双谱可检验靶。
纪律：与 C53（引力泡）/C54（TUFT-RG）/C60（EHT 光子环）同款——
      ① 标准宇宙学可检验靶基准（公开观测锚点，mpmath 250 位复算）；
      ② 纲领映射审查（几何量逐一检查能否构成 CMB 双谱可观测修正）；
      ③ V 判别式（自由参数 F − 约束 C）。

靶基准来源：Planck Collaboration 2018/2020 系列论文（TT/TE/EE 功率谱、非高斯
形状约束、谱参数）；本模块只把公开报告值作为「靶参考」，不重判标准宇宙学。

产出：数据/空间螺旋CMB拓扑双谱_攻坚审计.json + .md（幂等覆盖）
"""
import os
import io
import sys
import json
import time
import mpmath as mp

mp.mp.dps = 250

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DATA = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

OUT_JSON = os.path.join(DATA, "空间螺旋CMB拓扑双谱_攻坚审计.json")
OUT_MD = os.path.join(DATA, "空间螺旋CMB拓扑双谱_攻坚审计.md")

T0 = time.time()
P = {"title": "空间螺旋 CMB 拓扑双谱攻坚审计",
     "date": "2026-09-26",
     "dps": 250,
     "discipline": "与 C53/C54/C60 同款：标准宇宙学基准复现 + 纲领映射审查 + V 判别式"}

# ============================================================================
# §1 标准宇宙学可检验靶基准（公开观测锚点；mpmath 250 位复算）
# ============================================================================
print("=" * 76)
print("===== 1. CMB 双谱可检验靶基准（标准宇宙学，公开观测锚点） =====")
print("=" * 76)

# 靶1：TT 功率谱第一声峰（Planck 2018 TT，l≈220，峰高 ~5.7e3 μK²）
l_peak = mp.mpf("220")
C_peak_uK2 = mp.mpf("5.7e3")
print("靶1 | 角功率谱第一声峰：l≈%d，C_l≈%.3g μK²（Planck 2018 TT）"
      % (int(l_peak), float(C_peak_uK2)))

# 靶2：非高斯参数 f_NL（局部形状，Planck 2018 T+E 组合：−0.9 ± 5.1）
fNL_center = mp.mpf("-0.9")
fNL_sigma = mp.mpf("5.1")
fNL_sig = abs(fNL_center) / fNL_sigma
print("靶2 | 非高斯 f_NL^local = −0.9 ± 5.1（Planck 2018 T+E）")
print("      |f_NL|/σ = %.6f ⇒ 中心值在 1σ 内，约束量级 |f_NL| ≲ 5" % fNL_sig)

# 靶3：原初标量谱参数（Planck 2018，k*=0.05 Mpc⁻¹）
n_s = mp.mpf("0.965")
n_s_sigma = mp.mpf("0.004")
ns_dev_sig = (mp.mpf("1") - n_s) / n_s_sigma
A_s = mp.mpf("2.105e-9")
print("靶3 | n_s = 0.965 ± 0.004 ⇒ (1−n_s)/σ = %.4fσ（红 tilt 显著）" % ns_dev_sig)
print("      A_s = %.4e（原初幅度；双谱幅度与 A_s² 同阶）" % A_s)

# 靶4：张标比上界（Planck 2018 + BK15，95% CL）
r_upper = mp.mpf("0.036")
print("靶4 | 张标比 r < %.3f（95%% CL，Planck 2018+BK15）——原初张量双谱当前不可分辨" % r_upper)

# 双谱形状因子比较：局部/等边/正交形状（Planck 2018 约束幅值 ~O(1-10)）
shapes = {"局部 (local)": mp.mpf("-0.9"), "等边 (equilateral)": mp.mpf("-26"),
          "正交 (orthogonal)": mp.mpf("-38")}
print("\n双谱形状约束幅值（Planck 2018，中心值，单位 f_NL）：")
for k, v in shapes.items():
    print("   %-18s f_NL ≈ %+6.1f" % (k, v))

# ============================================================================
# §2 纲领映射审查（几何量 → CMB 双谱可观测映射）
# ============================================================================
print("\n" + "=" * 76)
print("===== 2. 纲领映射审查（能否进入 CMB 双谱可检验靶） =====")
print("=" * 76)

mapping = []
def add_map(geom, source, target, evidence, verdict, mode):
    mapping.append({"geom": geom, "source": source, "target": target,
                    "evidence": evidence, "verdict": verdict, "fail_mode": mode})
    mark = "✗" if verdict != "PASS" else "✓"
    print("   %s %-16s | %s | %s" % (mark, geom, source, verdict))
    print("        → %s（%s）" % (target, failmode_cn(mode)))


def failmode_cn(m):
    return {"量纲死亡": "量纲非法，不可进入任何场方程",
            "零内容": "与标准宇宙学/GR 恒等，无独立内容",
            "无映射方程": "缺「几何量→可观测」的中间结构",
            "已证伪": "对应 claims 已被引擎定罪"}[m]

# 1. κ/τ → 引力涨落场/密度扰动源
add_map("κ/τ（Frenet 曲率/挠率）", "C26（falsified）",
        "原初密度扰动 δρ/ρ 与曲率扰动源",
        "涨落源需度规场方程；纲领无作用量（C53/C54/C60 同型）",
        "FAIL", "无映射方程")
# 2. ω、A（基底参数）→ 声学尺度/声峰位置
add_map("ω、A（基底参数）", "C24/C25（|R'|=c 修复；α 公式欠定）",
        "声学视界/第一声峰 l≈220",
        "ω 只进入电磁精细结构 α 公式；与宇宙学尺度无方程连接",
        "FAIL", "无映射方程")
# 3. N（拓扑绕数）→ 角尺度/l 谱
add_map("N（拓扑绕数）", "C27（falsified）/C50（外部输入）",
        "角功率谱 l 谱峰位与形状",
        "只调制 LB 本征谱（退化 1e-75）；与涨落谱无连接",
        "FAIL", "无映射方程")
# 4. Φ₀（相位场）→ 涨落相位/非高斯相位
add_map("Φ₀（相位场）", "C36（falsified）",
        "非高斯双谱相位结构",
        "[Φ₀]=[Φ]/L 量纲冲突（量纲死亡）",
        "FAIL", "量纲死亡")
# 5. ρ、K₀、α²K 类 → 能量密度/曲率扰动
add_map("ρ、K₀、α²K 类", "C12/C29/C30/C31/C32/C33（falsified）",
        "密度扰动源 ρ_pert 与曲率扰动 ζ",
        "尽数定罪（量纲失败/循环/孤儿场）",
        "FAIL", "已证伪")
# 6. GravBubble → 原初非高斯源
add_map("GravBubble κ0/τ0/σ/αg", "C53（falsified）",
        "原初双谱（局部/等边形状）非高斯源",
        "量纲非法×4 + 无作用量（ansatz 非孤子）",
        "FAIL", "已证伪")
# 7. RG 系数 b1..b6 → 谱指数跑动
add_map("RG 系数 b1..b6", "C54（falsified）",
        "谱指数跑动 n_s−running / 原初谱斜率",
        "无映射方程 + 无紫外固定点",
        "FAIL", "无映射方程")
# 8. β（Binet 修正参数）→ 引力修正
add_map("β（Binet 修正参数）", "C49/C51（open·零判别力）",
        "张标比 r / 引力波原初谱",
        "β0≡GR 1PN 零内容；β_correct 无外推映射",
        "FAIL", "零内容")

pass_count = sum(1 for m in mapping if m["verdict"] == "PASS")
fail_count = len(mapping) - pass_count
print("\n映射审查：%d/%d 通过" % (pass_count, len(mapping)))

# ============================================================================
# §3 判别式与判定
# ============================================================================
print("\n" + "=" * 76)
print("===== 3. 判别式与判定 =====")
print("=" * 76)

F = 0   # 自由参数：无映射成立 ⇒ 无可调入参数
C = 0   # 约束：无场方程/涨落谱方程可被观测约束
V = F - C
print("自由参数 F=%d，约束 C=%d，判别式 V=F−C=%d" % (F, C, V))
if V <= 0:
    verdict = "falsified"
    conclusion = ("V≤0 ⇒ 伪派生（无映射方程层）：纲领无作用量→无场方程→无引力涨落谱→"
                  "无原初功率谱/双谱预言。与 C53（V=−4）、C54、C60 同模式。")
else:
    verdict = "open"
    conclusion = "存在映射层，可继续攻坚"
print("判定：%s | V=%d | 映射 %d/%d 通过" % (verdict, V, pass_count, len(mapping)))
print(conclusion)
print("体系级开放问题：空间螺旋纲领若先由作用量导出场方程，再导出引力涨落谱（原初功率谱/双谱），"
      "CMB 预言可重启；当前无此结构。")

# ============================================================================
# §4 台账登记建议
# ============================================================================
suggestion = {
    "C61": {
        "module": "CMB 拓扑双谱攻坚",
        "verdict": verdict,
        "reason": "无映射方程层（8/8 映射 FAIL）：几何量无一能构成 CMB 双谱修正；"
                  "标准宇宙学靶（f_NL/n_s/A_s/r）为公开观测，纲领无独立预言",
        "system_level": "open（先由作用量导出场方程与引力涨落谱则重启）"},
    "CMB_raw": {
        "module": "CMB 功率谱/双谱仿真本体（Boltzmann 求解）",
        "verdict": "未提交",
        "reason": "无模块无公式无脚本；延续纪律：不得凭声明登记"}}

# ============================================================================
# 落盘
# ============================================================================
payload = {"title": P["title"], "date": P["date"], "dps": 250,
           "targets": {
               "l_peak": str(l_peak), "C_peak_uK2": str(C_peak_uK2),
               "fNL_center": str(fNL_center), "fNL_sigma": str(fNL_sigma),
               "fNL_sigma_ratio": str(fNL_sig),
               "n_s": str(n_s), "n_s_sigma": str(n_s_sigma),
               "ns_dev_sig": str(ns_dev_sig), "A_s": str(A_s),
               "r_upper": str(r_upper),
               "shape_centers": {k: str(v) for k, v in shapes.items()}},
           "mapping": {"items": mapping, "pass_count": pass_count, "fail_count": fail_count},
           "verdict": {"F": F, "C": C, "V": V, "verdict": verdict, "conclusion": conclusion},
           "claims_register_suggestion": suggestion,
           "runtime_sec": round(time.time() - T0, 3)}

with io.open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
print("\n   JSON 已写出：数据/空间螺旋CMB拓扑双谱_攻坚审计.json")

md = []
md.append("# 空间螺旋 CMB 拓扑双谱攻坚审计（2026-09-26）")
md.append("")
md.append("> 纪律：与 C53/C54/C60 同款——标准宇宙学基准复现 + 纲领映射审查 + V 判别式；mpmath dps=250")
md.append("")
md.append("## §1 标准宇宙学可检验靶基准（公开观测锚点，仅作靶参考）")
md.append("")
md.append("| 靶 | 量 | 值 | 来源口径 |")
md.append("|---|---|---|---|")
md.append("| 角功率谱第一声峰 | l / C_l | %d / ~%.3g μK² | Planck 2018 TT |" % (int(l_peak), float(C_peak_uK2)))
md.append("| 非高斯参数（局部形状） | f_NL | −0.9 ± 5.1（|f_NL|/σ=%.4f） | Planck 2018 T+E |" % fNL_sig)
md.append("| 原初谱参数 | n_s | 0.965 ± 0.004（(1−n_s)/σ=%.4fσ） | Planck 2018 |" % ns_dev_sig)
md.append("| 原初幅度 | A_s | %.4e（k*=0.05 Mpc⁻¹） | Planck 2018 |" % A_s)
md.append("| 张标比 | r | < 0.036（95% CL） | Planck 2018+BK15 |")
md.append("| 双谱形状中心值 | 局部/等边/正交 | %+5.1f / %+5.1f / %+5.1f | Planck 2018 |"
          % (shapes["局部 (local)"], shapes["等边 (equilateral)"], shapes["正交 (orthogonal)"]))
md.append("")
md.append("## §2 纲领映射审查（8/8 FAIL）")
md.append("")
md.append("| 几何量 | 来源 | 映射目标 | 证据 | 结论 |")
md.append("|---|---|---|---|---|")
for m in mapping:
    md.append("| %s | %s | %s | %s | **%s（%s）** |"
              % (m["geom"], m["source"], m["target"], m["evidence"], m["verdict"], m["fail_mode"]))
md.append("")
md.append("**失败模式总结**：量纲死亡（Φ₀）、零内容（β0≡GR 1PN）、无映射方程（κ/ω/N/ρ类/GravBubble/RG）——"
          "纲领无「几何对象→引力涨落场→原初功率谱/双谱」的中间结构。")
md.append("")
md.append("## §3 判定")
md.append("")
md.append("F=%d、C=%d、**V=F−C=%d ≤ 0 ⇒ %s（无映射方程层）**" % (F, C, V, verdict))
md.append("")
md.append(conclusion)
md.append("")
md.append("**体系级 open（如实保留）**：若纲领先给出作用量并导出场方程，再导出引力涨落谱，"
          "CMB 预言可重启——当前无此结构。")
md.append("")
md.append("## §4 台账登记建议")
md.append("")
md.append("- **C61**：CMB 拓扑双谱攻坚模块 → **%s**（无映射方程层；体系级前置 open）。" % verdict)
md.append("- **CMB 仿真本体**（Boltzmann 求解 C_l/B_l）：未提交（无模块无公式无脚本），不得凭声明登记。")
md.append("")
md.append("## §5 复跑说明")
md.append("")
md.append("- `python 空间螺旋CMB拓扑双谱_攻坚审计.py`：幂等覆盖 json/md；靶基准为公开观测值（Planck 2018 系列），"
          "仅作靶参考，不重判标准宇宙学。")
md.append("- 本模块不构造新物理；只做基准复现 + 映射证据审查；台账登记待用户确认后执行。")

with io.open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")
print("   MD 已写出：数据/空间螺旋CMB拓扑双谱_攻坚审计.md")

print("\n" + "=" * 76)
print("判定：%s | V=%d | 映射 %d/%d 通过 | 靶基准 4 项 | 用时 %.2f s"
      % (verdict, V, pass_count, len(mapping), time.time() - T0))
print("=" * 76)
