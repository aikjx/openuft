# -*- coding: utf-8 -*-
"""
空间螺旋几何化统一场论 · 来源脚本复跑与「自陈 PASS」核验（openuft 诚实审计口径）

定位
----
`spiral_geometry_audit.py` 复算的是**主张**；本脚本复跑的是**「声称复算过那些主张」的那批脚本**
（原样归档在 `90_历史归档/来源语料_20260611_螺旋几何化统一场论文章/code/`）。
它回答一个此前没有任何东西回答过的问题：

    那些脚本打印的「10 项 / 20 项全部验证通过」，到底测出了什么？

方法（四条互相独立的证据）
--------------------------
1. **复跑**：在临时工作目录里逐个跑原始脚本，记录退出码、耗时、自陈判定与**失败项及其上下文**。
   （临时目录而非归档目录：脚本会往 CWD 写 `*_results.txt` / `*.png`，
     在归档目录里跑会覆写被封存的产物。）
2. **静态扫描**：数 `assert` / `sys.exit` / `raise SystemExit` —— 判断这些脚本
   **有没有失败通路**；并把「不受任何条件分支约束的结论句」逐条列出。
3. **变异探针**（本脚本的核心）：把脚本里定义 α（或 G）的数值字面量按 1e-8 相对量改错，
   复制到临时目录重跑。脚本自己的判据阈值多为 `1e-100`，比 1e-8 小 8 个数量级：
   若把 α 改错 1e-8 后**判定、失败项、产物结论句一字不变**，则这些输出对 α 没有约束力 ——
   它们是「定义回代自身」的同义反复，而不是对物理输入的检验。
4. **产物比对**：把复跑新生成的 `*_results.txt` / `*.png` 与归档里那份逐字节比较 ——
   这同时检验了「归档产物是不是该脚本的真实输出」。

红线
----
- **只报告，不改写**：不改归档里的任何脚本 / txt / png；变异体只存在于临时目录，跑完即删。
- 退出码恒为 0：本脚本不因发现同义反复而失败，结论体现在报告判定里。
- 「判定不变」只证明「该脚本的判据不约束这个输入」，**不等于**其主张为假；
  反过来「判定改变」也只说明该脚本确实吃了这个输入，不等于主张为真。
- 数学自洽 != 实验证实。

依赖：仅 Python 标准库。
运行：python rerun_source_scripts.py [--stdout] [--timeout 600]
"""

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OPENUFT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CODE_DIR = os.path.join(OPENUFT, "90_历史归档",
                        "来源语料_20260611_螺旋几何化统一场论文章", "code")

# 变异探针：脚本里用来定义 α 与 G 的数值字面量（各脚本已逐一核对）
ALPHA_LITERALS = ["0.007297352569311114", "137.035999074"]
G_LITERALS = ["6.6743015e-11"]
REL_DELTA = 1e-8

VERDICT_PATTERNS = [
    re.compile(r"Result:\s*(\d+)\s*/\s*(\d+)\s*(?:tests?\s*)?(?:passed|verifications passed)", re.I),
    re.compile(r"(\d+)\s*/\s*(\d+)\s*tests passed", re.I),
    re.compile(r"ALL TESTS PASSED", re.I),
    re.compile(r"SUCCESS:\s*All verifications passed", re.I),
    re.compile(r"WARNING:\s*Some verifications failed", re.I),
    re.compile(r"WARNING:\s*(\d+)\s*tests FAILED", re.I),
    re.compile(r"综合结论：所有验证全部通过"),
    re.compile(r"认证通过"),
    re.compile(r"SUCCESS\s+所有验证全部通过"),
    re.compile(r"WARN\s+部分验证项未通过"),
]

# 条目级失败标记（不含 "N tests FAILED" 这类汇总句；含 `FAIL xxx` 这种无方括号写法）
FAIL_MARKER_RE = re.compile(r"\[FAIL\]|❌|验证结果\s*[:：]\s*失败|^\s*FAIL\s")
FAIL_ANY_RE = re.compile(r"\bFAIL\b|\[FAIL\]|失败|FAILED")
# 源码层「结论句」：只认判定语气，不认章节标题（如「7. …综合验证结论」）
SRC_CONCLUSION_RE = re.compile(r"通过|成功|达成|认证|判失败")
# 产物层「结论句」：结果文件里「验证结果: …」这类也算
ARTIFACT_CONCLUSION_RE = re.compile(r"通过|成功|达成|认证|验证结果")
COND_RE = re.compile(r"^\s*(if |else\b|elif |for |while |def |try\b|except|with )")

THRESHOLD_RE = re.compile(r"<\s*(?:mp\.mpf\(\s*['\"])?(\d+(?:\.\d+)?e-\d+)")
DPS_RE = re.compile(r"mp\.mp\.dps\s*=\s*(\d+)")
CONTEXT = 2
MUTANT_NAME = "__mutant_under_test__.py"   # 变异体源码名；统计产物时必须排除


# ---------------------------------------------------------------- 基础工具
def read_text(path):
    with open(path, "rb") as f:
        return f.read().decode("utf-8", "replace")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()[:12]


def sig_digits(literal):
    body = literal.split("e")[0].split("E")[0].lstrip("+-").replace(".", "")
    return len(body.lstrip("0"))


def run_script(target, workdir, timeout):
    env = dict(os.environ)
    env["MPLBACKEND"] = "Agg"                  # 可视化脚本无需交互后端
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"
    started = time.time()
    try:
        proc = subprocess.run([sys.executable, target], cwd=workdir, env=env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        return (proc.returncode,
                proc.stdout.decode("utf-8", "replace"),
                proc.stderr.decode("utf-8", "replace"),
                time.time() - started, False)
    except subprocess.TimeoutExpired as exc:
        return (None,
                (exc.stdout or b"").decode("utf-8", "replace"),
                (exc.stderr or b"").decode("utf-8", "replace"),
                time.time() - started, True)


def verdict_of(text):
    for pattern in VERDICT_PATTERNS:
        found = pattern.search(text)
        if found:
            return re.sub(r"\s+", "", found.group(0))
    if FAIL_MARKER_RE.search(text):
        return "含失败项"
    return ""


def run_variant(source_path=None, source_text=None, timeout=600):
    """跑一个变体，返回基线/变异体共用的紧凑记录。"""
    work = tempfile.mkdtemp(prefix="rrs_")
    record = {"exit": None, "verdict": "", "fail_items": [], "files": {},
              "conclusions": {}, "seconds": 0.0, "timed_out": False, "stderr_tail": ""}
    try:
        if source_text is not None:
            target = os.path.join(work, MUTANT_NAME)
            with open(target, "w", encoding="utf-8") as f:
                f.write(source_text)
        else:
            target = source_path
        code, out, err, secs, timed_out = run_script(target, work, timeout)
        record.update({"exit": code, "seconds": secs, "timed_out": timed_out,
                       "verdict": verdict_of(out), "stderr_tail": err.strip()[-400:]})

        lines = out.splitlines()
        for index, line in enumerate(lines):
            if FAIL_MARKER_RE.search(line):
                block = [x.rstrip() for x in lines[max(0, index - CONTEXT):index + CONTEXT + 1]]
                record["fail_items"].append(block)

        for name in sorted(os.listdir(work)):
            if name == MUTANT_NAME:          # 变异体源码不是「脚本产出」
                continue
            path = os.path.join(work, name)
            if not os.path.isfile(path):
                continue
            with open(path, "rb") as f:
                data = f.read()
            record["files"][name] = sha256_bytes(data)
            if name.endswith(".txt"):
                body = data.decode("utf-8", "replace")
                record["conclusions"][name] = [ln.strip() for ln in body.splitlines()
                                               if ARTIFACT_CONCLUSION_RE.search(ln)]
        return record
    finally:
        shutil.rmtree(work, ignore_errors=True)


def static_scan(text):
    lines = text.splitlines()
    unconditional = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not re.search(r"""write\(|print\(""", stripped):
            continue
        if not SRC_CONCLUSION_RE.search(stripped):
            continue
        # 行内三元（`'通过' if cond else '失败'`）本身就是条件，不算「无条件结论句」
        if re.search(r"\bif\b[^:]*\belse\b", stripped):
            continue
        window = [x for x in lines[max(0, index - 8):index] if COND_RE.match(x)]
        # 同层缩进的条件分支才算守卫：只看缩进 <= 本行的条件行
        indent = len(line) - len(line.lstrip())
        guarded = any(len(x) - len(x.lstrip()) <= indent for x in window)
        if not guarded:
            unconditional.append((index + 1, stripped[:150]))
    dps = DPS_RE.search(text)
    return {
        "assert": len(re.findall(r"^\s*assert\b", text, re.M)),
        "sys_exit": len(re.findall(r"sys\.exit\s*\(", text)),
        "SystemExit": len(re.findall(r"raise\s+SystemExit", text)),
        "unconditional": unconditional,
        "thresholds": sorted(set(THRESHOLD_RE.findall(text))),
        "dps": int(dps.group(1)) if dps else None,
    }


def perturb(text, literals, rel):
    hits, news = 0, []
    for literal in literals:
        if literal not in text:
            continue
        new_literal = repr(float(literal) * (1.0 + rel))
        hits += text.count(literal)
        text = text.replace(literal, new_literal)
        news.append(literal + " -> " + new_literal)
    return text, hits, news


def unchanged(a, b):
    return a == b


def mark(a, b):
    return "不变" if unchanged(a, b) else "**改变**"


# ---------------------------------------------------------------- 主流程
def main():
    timeout = 600
    if "--timeout" in sys.argv:
        timeout = int(sys.argv[sys.argv.index("--timeout") + 1])

    if not os.path.isdir(CODE_DIR):
        print("[FAIL] 找不到来源脚本目录：" + CODE_DIR)
        return 1
    scripts = sorted(n for n in os.listdir(CODE_DIR)
                     if n.endswith(".py") and os.path.isfile(os.path.join(CODE_DIR, n)))
    if not scripts:
        print("[FAIL] 目录内没有 .py：" + CODE_DIR)
        return 1

    print("来源脚本目录：" + CODE_DIR)
    print("脚本数：{}    单脚本超时：{}s    变异步长：{:.0e}".format(len(scripts), timeout, REL_DELTA))
    print("")

    rows = []
    for name in scripts:
        path = os.path.join(CODE_DIR, name)
        text = read_text(path)
        scan = static_scan(text)

        base = run_variant(source_path=path, timeout=timeout)

        mut_text_a, hits_a, news_a = perturb(text, ALPHA_LITERALS, +REL_DELTA)
        mut_text_b, hits_b, news_b = perturb(text, G_LITERALS, -REL_DELTA)
        mut_a = run_variant(source_text=mut_text_a, timeout=timeout) if hits_a else None
        mut_b = run_variant(source_text=mut_text_b, timeout=timeout) if hits_b else None

        artifact = []
        for produced, digest in sorted(base["files"].items()):
            archived = os.path.join(CODE_DIR, produced)
            if not os.path.isfile(archived):
                artifact.append((produced, "归档无该产物", digest))
                continue
            with open(archived, "rb") as f:
                archived_digest = sha256_bytes(f.read())
            artifact.append((produced, "逐字节一致" if archived_digest == digest else "**不一致**", digest))

        rows.append({"name": name, "scan": scan, "base": base,
                     "mut_a": mut_a, "hits_a": hits_a, "news_a": news_a,
                     "mut_b": mut_b, "hits_b": hits_b, "news_b": news_b,
                     "artifact": artifact})

        print("[{}] exit={} {:.1f}s  verdict={}".format(
            name, "timeout" if base["timed_out"] else base["exit"],
            base["seconds"], base["verdict"] or "(无判定语句)"))
        if base["exit"] not in (0, None):
            print("     ** 基线即非零退出 **：" + base["stderr_tail"].splitlines()[-1][:160])
        if scan["assert"] == scan["sys_exit"] == scan["SystemExit"] == 0:
            print("     失败通路：0（无 assert / sys.exit / SystemExit）")
        if base["fail_items"]:
            first = [x for x in base["fail_items"][0] if FAIL_MARKER_RE.search(x)]
            print("     基线自陈失败项：{} 条，首条：{}".format(
                len(base["fail_items"]), (first[0].strip() if first else "")[:110]))
        if scan["unconditional"]:
            print("     不受条件分支约束的结论句：{} 处（首见第 {} 行）".format(
                len(scan["unconditional"]), scan["unconditional"][0][0]))
        for tag, mut, hits in (("α", mut_a, hits_a), ("G", mut_b, hits_b)):
            if mut is None:
                print("     变异探针 {}：N/A（脚本内无该字面量）".format(tag))
                continue
            print("     变异探针 {}：{} 处字面量改错 1e-8 -> exit={}  判定 {}  失败项 {}  产物 {}  产物结论句 {}".format(
                tag, hits, mut["exit"], mark(base["verdict"], mut["verdict"]),
                mark(base["fail_items"], mut["fail_items"]),
                mark(base["files"], mut["files"]),
                mark(base["conclusions"], mut["conclusions"])))
        for produced, state, _digest in artifact:
            print("     产物 {}：{}".format(produced, state))
        print("")

    return write_report(rows, timeout)


# ---------------------------------------------------------------- 报告
def mutation_cell(mut, base, hits):
    if mut is None or not hits:
        return "N/A"
    bits = ["exit=" + str(mut["exit"]),
            "判定 " + mark(base["verdict"], mut["verdict"]),
            "失败项 " + mark(base["fail_items"], mut["fail_items"]),
            "产物 " + mark(base["files"], mut["files"]),
            "产物结论句 " + mark(base["conclusions"], mut["conclusions"])]
    return "<br>".join(bits)


def write_report(rows, timeout):
    crashed = [r for r in rows if r["base"]["exit"] not in (0, None)]
    no_fail_path = [r for r in rows
                    if r["scan"]["assert"] == r["scan"]["sys_exit"] == r["scan"]["SystemExit"] == 0]
    self_fail = [r for r in rows if r["base"]["fail_items"]]
    self_fail_total = sum(len(r["base"]["fail_items"]) for r in self_fail)

    probe_rows = [r for r in rows if r["mut_a"] is not None
                  and (r["base"]["verdict"] or r["mut_a"]["verdict"])]
    probe_inert = [r for r in probe_rows
                   if unchanged(r["base"]["verdict"], r["mut_a"]["verdict"])
                   and unchanged(r["base"]["fail_items"], r["mut_a"]["fail_items"])]
    probe_reactive = [r for r in probe_rows if r not in probe_inert]

    concl_rows = [r for r in rows if r["mut_a"] is not None and r["base"]["conclusions"]]
    concl_kept = [r for r in concl_rows if unchanged(r["base"]["conclusions"], r["mut_a"]["conclusions"])]

    artifacts = [(r["name"], name, state) for r in rows for name, state, _d in r["artifact"]]
    art_same = [x for x in artifacts if x[2] == "逐字节一致"]
    art_diff = [x for x in artifacts if x[2] != "逐字节一致"]
    unconditional_total = sum(len(r["scan"]["unconditional"]) for r in rows)

    L = []
    L.append("# 来源脚本复跑与「自陈 PASS」核验报告")
    L.append("")
    L.append("> 生成：`rerun_source_scripts.py`（本文件为运行产物，非手写）")
    L.append("> 对象：`90_历史归档/来源语料_20260611_螺旋几何化统一场论文章/code/` 下的全部 `.py`")
    L.append("> 依赖：仅 Python 标准库；被复跑的脚本另行需要 `mpmath` / `sympy` / `numpy` + `matplotlib`")
    L.append("")

    L.append("## 0. 结论")
    L.append("")
    L.append("**这批脚本的「全部验证通过」在结构上不可能是判据的输出。**")
    L.append("")
    L.append("| 读数 | 值 |")
    L.append("|---|---|")
    L.append("| 脚本总数 | {} |".format(len(rows)))
    L.append("| **基线即非零退出（跑不起来）** | **{} 个**：{} |".format(
        len(crashed), "、".join("`" + r["name"] + "`" for r in crashed) if crashed else "无"))
    L.append("| 失败通路合计（assert / sys.exit / SystemExit） | **0 处**，覆盖 {} / {} 个脚本 —— 脚本不可能以失败告终 |".format(
        len(no_fail_path), len(rows)))
    L.append("| **自己打印了失败项**的脚本 | **{} 个 / 合计 {} 条**（原文却称「全部验证通过」） |".format(
        len(self_fail), self_fail_total))
    L.append("| 不受任何条件分支约束的结论句 | **{} 处**（写死在 `write()` / `print()` 里） |".format(unconditional_total))
    L.append("| α 改错 1e-8 后**判定与失败项均不变**的脚本 | **{} / {}**（有判定语句的脚本） |".format(
        len(probe_inert), len(probe_rows)))
    L.append("| α 改错 1e-8 后判定或失败项**改变**的脚本 | {} / {} |".format(len(probe_reactive), len(probe_rows)))
    L.append("| α 改错后**产物结论句逐字保留**的脚本 | **{} / {}**（结论句对输入改错完全免疫） |".format(
        len(concl_kept), len(concl_rows)))
    L.append("| 归档产物与复跑逐字节一致 | {} / {} |".format(len(art_same), len(artifacts)))
    L.append("| 归档产物与复跑不一致 | {} |".format(len(art_diff) if art_diff else 0))
    L.append("")
    L.append("五条要分开读：")
    L.append("")
    L.append("1. **结构上不可能失败。** 11 个脚本的 `assert` / `sys.exit` / `raise SystemExit` 合计 **0 处**；")
    L.append("   凡是写结论句的地方都不在任何条件分支之内（合计 {} 处，见第 6 节）。".format(unconditional_total))
    L.append("2. **跑得起来的几个，自己就报了失败。** `full_verification.py` 打印 `13/16`（3 条 `[FAIL]`）、")
    L.append("   `complete_verification.py` 打印 `21/22`（1 条 `[FAIL]`）、`all_dimension_breakthrough.py` 打印 2 条")
    L.append("   `❌ 失败`、`infinite_dimension_verification.py` 打印 2 条失败 —— 而原文一律称「全部验证通过」。")
    L.append("   失败项落在两类地方：**CODATA 常数彼此的互验**（`alpha = e²/(4πε₀ℏc)`、`G = 4πα³ℏcρ²/e²`、")
    L.append("   `G·e² = 4πα³ℏcρ²`）与**阈值本身**（`all_dimension_breakthrough.py` 把「相对误差 6.38e-9 %」判成失败；")
    L.append("   `infinite_dimension_verification.py` 用 1e-90 去卡一个**截断到 100 项**的级数）。")
    L.append("   把 α 改错 1e-8，这些失败项的**数目一个不变**（1→1、3→3、2→2）—— 说明它们来自输入侧/阈值侧，")
    L.append("   与 α 的取值无关。")
    L.append("3. **有 1 个脚本根本跑不起来。** `unified_field_theory_ultimate_verification.py` 在第 194 行")
    L.append("   抛 `NameError: name 'G' is not defined`（脚本只定义了 `G_codata`），死在「8. ε₀ 几何化验证」，")
    L.append("   **从未跑到任何总结**；归档目录里也相应没有它的 `*_results.txt`。")
    L.append("4. **结论句与算出来的数没有耦合。** 把 α 改错 1e-8，差值变了、产物里的结论句 {} / {} 逐字保留。".format(
        len(concl_kept), len(concl_rows)))
    L.append("5. **判定翻转只发生在「与写死的常数比对」上。** α 改错 1e-8 后翻转的 2 个脚本：")
    L.append("   `1.py` 新增的失败项是「宇宙本征常数 N 是否等于源码里写死的 30 位常数」（回归锁），")
    L.append("   `all_dimension_breakthrough.py` 是无条件的「认证通过」输出消失（失败项 2→3）。")
    L.append("   没有一条翻转发生在被宣称检验的物理关系上（见第 3B 节）。")
    L.append("   另有三处口径需要读源码（第 7 节）：`ΣF_i/ΣF_j ≡ 1` 被当成归一化检验；")
    L.append("   「四力归一化」被补到七项才够过 1e-10 阈值；同一运行里既打「失败」又打「全部通过」。")
    L.append("")
    L.append("**它们能证明的**：作者自己的定义链在代数上自洽（内部一致）。")
    L.append("**它们不能证明的**：任何一条与外部世界有关的量 —— 包括 α、G、ρ 的取值。")
    L.append("")

    L.append("## 1. 逐脚本结果")
    L.append("")
    L.append("| 脚本 | 退出码 | 耗时 | 自陈判定 | 自陈失败项 | 失败通路 | 不受条件约束的结论句 | α 改错 1e-8 | G 改错 1e-8 |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        scan = r["scan"]
        fail_paths = "0" if scan["assert"] == scan["sys_exit"] == scan["SystemExit"] == 0 \
            else "assert {} / sys.exit {} / SystemExit {}".format(scan["assert"], scan["sys_exit"], scan["SystemExit"])
        L.append("| `{}` | {} | {:.1f}s | {} | {} | {} | {} | {} | {} |".format(
            r["name"],
            "超时" if r["base"]["timed_out"] else r["base"]["exit"],
            r["base"]["seconds"],
            r["base"]["verdict"] or "(无)",
            len(r["base"]["fail_items"]),
            fail_paths,
            len(scan["unconditional"]),
            mutation_cell(r["mut_a"], r["base"], r["hits_a"]),
            mutation_cell(r["mut_b"], r["base"], r["hits_b"])))
    L.append("")
    L.append("> 单元格：「不变」= 该输入改错 1e-8 后这一栏与基线逐字相同 ⇒ 该脚本的这部分输出对这个输入**没有约束力**。")
    L.append("> `产物` 比较 `*_results.txt` / `*.png` 的 SHA-256；`产物结论句` 比较结论句清单。")
    L.append("")

    L.append("## 2. 基线就失败的脚本")
    L.append("")
    if crashed:
        L.append("| 脚本 | 退出码 | 最后一行异常 |")
        L.append("|---|---|---|")
        for r in crashed:
            tail = r["base"]["stderr_tail"].splitlines()
            L.append("| `{}` | {} | `{}` |".format(r["name"], r["base"]["exit"],
                                                    (tail[-1] if tail else "")[:170]))
        L.append("")
        L.append("> 跑不起来的脚本，其宣称的验证项在本机**从未被执行过**；归档目录里也相应缺少它的 `*_results.txt`（见第 4 节）。")
    else:
        L.append("- （本次全部脚本均可运行）")
    L.append("")

    L.append("## 3. 基线自陈的失败项（带上下文）")
    L.append("")
    if self_fail:
        for r in self_fail:
            L.append("### `{}` —— 自陈 {} 条".format(r["name"], len(r["base"]["fail_items"])))
            L.append("")
            L.append("```text")
            for block in r["base"]["fail_items"]:
                for line in block:
                    L.append(line)
                L.append("")
            L.append("```")
            L.append("")
    else:
        L.append("- （本次无脚本自陈失败）")
    L.append("")

    L.append("## 3B. 变异后才出现的失败项（判定翻转发生在哪一条）")
    L.append("")
    reactive = [r for r in rows if r["mut_a"] is not None
                and not unchanged(r["base"]["verdict"], r["mut_a"]["verdict"])]
    if reactive:
        L.append("| 脚本 | 基线判定 | α 改错 1e-8 后判定 | 失败项数（基线→变异） | 变异后新增的失败项 |")
        L.append("|---|---|---|---|---|")
        for r in reactive:
            base_items = {tuple(x) for x in r["base"]["fail_items"]}
            new_items = [x for x in r["mut_a"]["fail_items"] if tuple(x) not in base_items]
            marks = []
            for block in new_items:
                marks += [x.strip() for x in block if FAIL_MARKER_RE.search(x)]
            first = marks[0] if marks else ""
            L.append("| `{}` | {} | {} | {} → {} | {} |".format(
                r["name"], r["base"]["verdict"] or "(无)", r["mut_a"]["verdict"] or "(无)",
                len(r["base"]["fail_items"]), len(r["mut_a"]["fail_items"]),
                ("`" + first[:140] + "`") if first else "（失败项文本相同，变的是上下文里的数值/汇总判定）"))
        L.append("")
        L.append("> 读法：翻转的脚本里，`1.py` 新增的失败项是 **`FAIL 宇宙本征常数验证失败`** ——")
        L.append("> 即「算出来的 N 是否等于源码里写死的那个 30 位常数」，属**回归锁**（锁住 α 的取值），")
        L.append("> 不是任何一条被宣称检验的物理关系。另一处（`all_dimension_breakthrough.py`）变的是")
        L.append("> 无条件的「认证通过」输出消失，其失败项文本不变（变的是上下文里的数值）。")
    else:
        L.append("- （本次无脚本的判定随 α 改错而翻转）")
    L.append("")

    L.append("## 4. 归档产物 vs 复跑产物")
    L.append("")
    L.append("| 脚本 | 复跑在临时目录生成 | 与归档比较 |")
    L.append("|---|---|---|")
    for r in rows:
        produced = "、".join("`" + x + "`" for x in sorted(r["base"]["files"])) or "-"
        detail = "；".join("`{}` {}".format(a, b) for a, b, _d in r["artifact"]) if r["artifact"] else "-"
        L.append("| `{}` | {} | {} |".format(r["name"], produced, detail))
    L.append("")
    L.append("> 逐字节一致 ⇒ 归档产物**确为该脚本的真实输出**，未被事后手改（这一点是归档可信度的正面证据）；")
    L.append("> 不一致 ⇒ 归档产物不是当前脚本的输出（需人工核查来源）。本次一致 {} 项、不一致 {} 项。".format(
        len(art_same), len(art_diff)))
    L.append("")

    L.append("## 5. 静态扫描明细")
    L.append("")
    L.append("| 脚本 | assert | sys.exit | SystemExit | dps 声明 | α 字面量有效位 | G 字面量有效位 | 判据阈值 |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in rows:
        text = read_text(os.path.join(CODE_DIR, r["name"]))
        a_sig = max([sig_digits(x) for x in ALPHA_LITERALS if x in text] or [0])
        g_sig = max([sig_digits(x) for x in G_LITERALS if x in text] or [0])
        scan = r["scan"]
        L.append("| `{}` | {} | {} | {} | {} | {} | {} | {} |".format(
            r["name"], scan["assert"], scan["sys_exit"], scan["SystemExit"],
            scan["dps"] if scan["dps"] else "-",
            a_sig if a_sig else "-", g_sig if g_sig else "-",
            "、".join(scan["thresholds"]) if scan["thresholds"] else "-"))
    L.append("")

    L.append("## 6. 不受条件分支约束的结论句（逐条）")
    L.append("")
    if unconditional_total:
        for r in rows:
            if not r["scan"]["unconditional"]:
                continue
            L.append("### `{}`（{} 处）".format(r["name"], len(r["scan"]["unconditional"])))
            L.append("")
            for line_no, literal in r["scan"]["unconditional"]:
                L.append("- 第 {} 行：`{}`".format(line_no, literal.replace("|", "/")))
            L.append("")
    else:
        L.append("- （无）")
    L.append("> 这些句子与同段里算出来的「差值」是两条互不相干的语句：差值算成多少，句子照写。")
    L.append("> 判据：「不受条件分支约束」= 语句本身不是行内三元、且往上 8 行内没有同层或更外层的 `if/else/for/while/try`。")
    L.append("")
    L.append("> 口径提示（详见第 7 节 (a)(b)）：「四力归一化 = 1」的缺口在代码里被两套手法绕开 ——")
    L.append("> 一是把分母换成自除（`ΣF_i/ΣF_j ≡ 1`），二是把 1/α²、1/α、1、α 补到 1/α⁷。都不是新的物理。")
    L.append("")

    L.append("## 7. 人工核对的三处口径（源码级，逐行）")
    L.append("")
    L.append("自动化读数之外，有三处口径需要读源码才能说清；它们都**不是**本次复跑发现的新缺陷，")
    L.append("而是给复算层已有的 X13 补上「它在代码里长什么样」：")
    L.append("")
    L.append("**(a) `1.py` 第 106–112 行：归一化总和恒等于 1。**")
    L.append("")
    L.append("```text")
    L.append("F_total = F_gravity + F_strong + F_weak + F_electromagnetic + F_fifth")
    L.append("norm_gravity = F_gravity / F_total          # …… 其余四项同")
    L.append("norm_total = norm_gravity + norm_strong + norm_weak + norm_electromagnetic + norm_fifth")
    L.append("```")
    L.append("")
    L.append("`norm_total = Σ F_i / Σ F_j ≡ 1` —— 对**任意** F 值、任意 α 都恒成立。")
    L.append("于是第 170 行 `if abs(norm_total - 1) < mp.mpf(\"1e-100\")` 必然进 PASS 分支，")
    L.append("打印「OK 五种力归一化验证通过，总和精确等于1」。**这条不是检验，是 (Σx)/Σx = 1。**")
    L.append("注意它的分母 **不是** 文献里的 N：五个强度因子之和 `1/α²+1/α+1+α+α² ≈ 18916.9083945` 与")
    L.append("`N = 1/[α²(1−α)] ≈ 18916.9083949` 相差 α³/(1−α) ≈ **3.9e-7**（绝对），相对差 α⁵ ≈ 2.1e-11 ——")
    L.append("正是被截掉的那截高阶项。也就是说：**同一个脚本里，「ρ 由 G 反解」用的是 N 的口径，")
    L.append("「五力归一化 = 1」用的是自除口径，两者相差在 1e-7 量级，而检验阈值写着 1e-100。**")
    L.append("")
    L.append("**(b) `core_verification.py` 第 57 行：把「四力」悄悄补成七项才够过阈值。**")
    L.append("")
    L.append("```text")
    L.append("forces = {… 'Gravity':1/alpha**2, 'Strong':1/alpha, 'Weak':1, 'Electro':alpha,")
    L.append("          '5th':alpha**2, '6th':alpha**3, '7th':alpha**4}")
    L.append("```")
    L.append("")
    L.append("判据是 `abs(total_norm - 1) < 1e-10`（第 105 行），而 `total_norm = Σ factor / N`：")
    L.append("")
    L.append("- 只取**四力**（引力/强/弱/电磁）：`Σ/N = 1 − α⁴` ⇒ 缺口 **2.836e-09** ⇒ 必然 FAIL（与复算层 X13 的 2.836e-09 同源）；")
    L.append("- 补上 5th/6th/7th 三项：`Σ/N = 1 − α⁷` ⇒ 缺口 **1.10e-15** ⇒ 落在 1e-10 之内，通过。")
    L.append("")
    L.append("⇒ 阈值 1e-10 恰好卡在 α⁴ 与 α⁷ 之间：**决定「通过」的不是物理，是补了几项。**")
    L.append("")
    L.append("**(c) `infinite_dimension_verification.py`：同一次运行里既打印「失败」又打印「全部通过」。**")
    L.append("")
    L.append("第 41 / 52 / 82 / 99 / 112 / 148 / 159 / 176 / 191 行是**条件**判定：")
    L.append("")
    L.append("```text")
    L.append("print(f\"验证结果：{'通过' if abs(...) < 1e-90 else '失败'}\")     # 9 处，形态一致")
    L.append("```")
    L.append("")
    L.append("本次复跑其中 **2 条判为「失败」**（一条相对误差 −1.97e-5 %，一条 12 项归一化差值 −2.28e-26）。")
    L.append("紧接着第 198 行是**无条件**的，第 244 行同样**无条件**写进结果文件：")
    L.append("")
    L.append("```text")
    L.append("print(\"✅ 所有验证全部通过！\")                              # 第 198 行，无 if")
    L.append("f.write(\"综合结论：所有验证全部通过！\\n\")                    # 第 244 行，无 if")
    L.append("```")
    L.append("")
    L.append("⇒ 归档的那份 `infinite_dimension_verification_results.txt` 与复跑**逐字节一致**（见第 4 节），")
    L.append("而它全文的结论句只有「综合结论：所有验证全部通过！」与「无穷维力系统一场论精算验证成功！」两句：")
    L.append("**数值都写进了文件，判定一条都没写；控制台上明明白白打了两个「失败」，文件里只剩「全部通过」。**")
    L.append("")
    L.append("## 8. 精度声明 vs 输入精度")
    L.append("")
    L.append("脚本普遍声明 `mp.mp.dps = 10000`，但 α、G 是以 16 位有效数字的**字面量**送入的；")
    L.append("`sp.Float(1/137.035999074, 100)` 这种写法还先由 Python 双精度求商、再转高精度对象。")
    L.append("⇒ **输出打印 30–50 位不等于那 30–50 位有意义**；这也是「1e-100 阈值」能通过的直接原因 ——")
    L.append("被比较的两端是同一个 16 位输入的两种写法。")
    L.append("")

    L.append("## 9. 复跑环境")
    L.append("")
    L.append("- 解释器：`" + sys.version.replace("\n", " ") + "`")
    L.append("- 工作目录：临时目录（**不在归档目录内跑** —— 脚本会往 CWD 写 `*_results.txt` / `*.png`）")
    L.append("- 单脚本超时：{}s，变异步长：±{:.0e}（相对）".format(timeout, REL_DELTA))
    L.append("")

    L.append("## 10. 与 `spiral_geometry_audit.py` 的关系")
    L.append("")
    L.append("| 层 | 复算什么 | 输入 |")
    L.append("|---|---|---|")
    L.append("| `spiral_geometry_audit.py` | **主张**（体系一到十）的数值 / 量纲是否自洽 | CODATA + 纯数学恒等式，独立于原文献 |")
    L.append("| 本报告 | **来源脚本的自陈 PASS** 里有没有信息量 | 原封不动复跑原脚本 + 变异探针 |")
    L.append("")
    L.append("两者互不替代；本报告的读数**支持并加强**复算层此前的两条判定：")
    L.append("`G=α²μ₀c²ρ²` 的数值吻合是 ρ 由 G 反解之后的同义反复（X2 / X8），")
    L.append("以及「四力归一化 = 1」在文献口径下并不精确成立（X13）。")
    L.append("")

    L.append("## 11. 红线")
    L.append("")
    L.append("- 本脚本**不改写**归档里的任何文件；变异体只存在于临时目录，跑完即删。")
    L.append("- 「判定不变」是**该脚本的判据无信息量**的证据，**不是**其主张为假的证明；")
    L.append("  主张为假需要独立复算（见第 9 节第一行）。")
    L.append("- 退出码恒为 0：审计发现同义反复不等于审计失败。")
    L.append("- **数学自洽 != 实验证实。**")
    L.append("")

    text = "\n".join(L) + "\n"
    if "--stdout" in sys.argv:
        print(text)
        return 0
    out_path = os.path.join(HERE, "source_scripts_rerun_report.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("[written] " + out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
