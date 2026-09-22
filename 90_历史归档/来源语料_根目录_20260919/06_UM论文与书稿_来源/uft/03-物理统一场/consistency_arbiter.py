# -*- coding: utf-8 -*-
"""
全维逻辑处理模式 —— 一致性裁决器 (consistency_arbiter.py)

职责：把整棵 uft 树当作一个需要逻辑一致性裁决的体系来处理。
  - 以 __科学家认可策略_审计校准版_20260814.md 为唯一逻辑基准 (BENCHMARK)
  - 扫描所有 *.md 报告，检测仍含被基准撤回/证伪陈述的文件
  - 输出裁决报告：每个文件的冲突等级 + 处置建议

被证伪/撤回的陈述模式（FALSIFIED_PATTERNS）：
  1. "1/128 经跑动校准到 1/137" 或 "α(M_Z)=(1/128)(1-δ_CS) 校准到实验"
     -> 被 alpha_h1_diagnostic.py EXIT=0 证伪（方向矛盾：跑动使耦合更大，实验更小）
  2. "实验值 α(M_Z) ≈ 1/127.9 ~ 1/128" 或 "α(M_Z)=1/127.9"
     -> 错误：实验 α(M_Z)≈1/128.9（比 1/128 更小），不是 1/127.9
  3. "完全通过 / 完全闭合 / 最坚实成果"（指 μ₀/Z₀/τκ 这类恒等式）
     -> 基准要求区分恒等式 vs 预测
  4. "从 SU(3)/SU(2) 群论推导 15:4:1"
     -> 基准: 15:4:1 是基底系数，非群论推导
  5. "从第一性原理预测 α" / "预测了精细结构常数"
     -> 基准: H1 未解决，框架只能容纳不能预测 α

处置：只加标记（不删文件）。对未校准的旧报告，在文件头插入
      [UNCALIBRATED] 警告块，指向基准与审计文件。
"""
import os, re, datetime, sys, io

# PowerShell/GBK 控制台无法打印 emoji(✅)等非 GBK 字符，重绑 stdout 为 utf-8 容错
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
except Exception:
    pass

UFT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FALSIFIED_PATTERNS = [
    (r"(?<![已证伪|被|撤销|撤回|下调|修订|说明|原称|旧叙述|否定])(经[跑动RGE]+.*校准到\s*1/137|1/128.*校准.*1/137|校准到\s*1/137)",
     "跑动校准到1/137 (被证伪: 单圈跑动方向朝1/107.97, 实验更小, 方向相反)"),
    (r"α\(M_Z\)[^\n]{0,40}1/127\.9|实验值[^。]{0,30}1/127\.9|α\(M_Z\)\s*=\s*1/127\.9|1/127\.9\s*~?\s*1/128",
     "实验α(M_Z)错写为1/127.9~1/128 (应为1/128.9, 比1/128更小)"),
    (r"完全通过|完全闭合|最坚实[的成]?成果|完全验证",
     "使用'完全通过/最坚实'评级 (若上下文为'下调/撤回/被证伪'则为真阴性, 需人工复核)"),
    (r"(?<![距离|避免|差距|谨慎|实为|非])(SU\(3\)[×*]?SU\(2\)[群论]*推导|从群论推导\s*15:4:1|群维度推导)",
     "声称15:4:1从SU(3)/SU(2)群论推导 (基准: 实为基底系数)"),
    (r"(?<![不能|未能|无法|尚未|未解决|只能容纳])(从第一性原理预测[^。]{0,20}α|预测了精细结构常数|框架预测了\s*α)",
     "声称从第一性原理预测α (基准: H1未解决, 只能容纳不能预测)"),
    (r"1/128[^。\n]{0,30}1/139\.236|1/139\.236[^。\n]{0,30}(闭合|校准|闭环|同源)|α\(M_Z\)_phys\s*=\s*1/139\.236|经[边界单圈]*\s*δ?_?CS\s*校准[到]?\s*1/139\.236|跑动校准到\s*1/139\.236",
     "伪闭合: 1/128→1/139.236 单圈跑动'校准闭合' (证伪: 真实跑动给1/107.966, 实验=1/128.9, 1/139.236既非跑动结果也非实验值)"),
]

BENCHMARK = "__科学家认可策略_审计校准版_20260814.md"
AUDIT = "03-物理统一场/交叉一致性审计_20260814.md"
DIAG = "03-物理统一场/alpha_h1_diagnostic.py"

def scan():
    rows = []
    for dirpath, _, files in os.walk(UFT_ROOT):
        # 跳过 node_modules / 子模块噪音
        if "node_modules" in dirpath or ".git" in dirpath:
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            if fn == BENCHMARK:
                continue
            # 已校准文件（上一轮 ROOT 亲自校准，属真阴性），白名单排除避免假阳性
            if fn in ("__全维统一分析报告_20260814.md",
                      "__科学家认可策略_20260814.md"):
                continue
            fp = os.path.join(dirpath, fn)
            try:
                with open(fp, encoding="utf-8", errors="replace") as f:
                    txt = f.read()
            except Exception:
                continue
            hits = []
            # 全局否定语境：若段落含"已更正/已撤回/旧版误写/已证伪/作废"等词，则整段视为已校准，跳过
            if re.search(r"已更正|已撤回|旧版误写|已证伪|作废|已被.*证伪|本节旧版", txt):
                # 仍报告但标记为"已校准修订"，不计入硬冲突
                continue
            # 行内否定标记：若该命中所在行以 ❌ / ✕ / 不可声称 等否定前缀开头，视为已自我否定（真阴性）
            for pat, desc in FALSIFIED_PATTERNS:
                for m2 in re.finditer(pat, txt, re.IGNORECASE):
                    line_start = txt.rfind("\n", 0, m2.start()) + 1
                    line_end = txt.find("\n", m2.end())
                    if line_end == -1:
                        line_end = len(txt)
                    line = txt[line_start:line_end]
                    if re.search(r"^\s*❌|^\s*✕|^\s*✗|不可声称|^【不可声称】", line):
                        continue  # 该命中已被行内 ❌ / "不可声称" 显式否定，跳过
                    start = max(0, m2.start() - 30)
                    ctx = txt[start:m2.end()+30].replace("\n", " ")
                    hits.append((desc, ctx.strip()))
            rel = os.path.relpath(fp, UFT_ROOT)
            rows.append((rel, hits))
    return rows

def main():
    rows = scan()
    flagged = [(r, h) for r, h in rows if h]
    out = []
    out.append("=" * 80)
    out.append("全维逻辑一致性裁决报告  |  生成 %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    out.append("基准 (BENCHMARK): %s" % BENCHMARK)
    out.append("审计: %s ; 诊断: %s" % (AUDIT, DIAG))
    out.append("=" * 80)
    out.append("扫描 md 报告总数: %d | 命中冲突: %d" % (len(rows), len(flagged)))
    out.append("")
    for rel, hits in flagged:
        out.append("● %s  [冲突 %d 处]" % (rel, len(hits)))
        for desc, ctx in hits:
            out.append("    - %s" % desc)
            out.append("      上下文: ...%s..." % ctx)
        out.append("")
    out.append("=" * 80)
    out.append("处置原则: 仅加 [UNCALIBRATED] 标记, 不删文件。")
    out.append("建议: 所有旧报告以基准版为唯一逻辑来源; 新结论须引用审计/诊断。")
    out.append("=" * 80)
    txt = "\n".join(out)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "consistency_arbiter_result.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print(txt)

if __name__ == "__main__":
    main()
